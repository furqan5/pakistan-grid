"""Day 9: assemble PowerModels-native JSON cases (summer peak, winter off-peak) from the parameter tables, under
builder/parameters.json ("assembly", "winter_openings".rule_v2_18nov), declared and pushed before any solve.
Also runs the load-deliverability check. Writes <build>/case/pk_<snapshot>.json and case_summary.md.
Usage: python builder/assemble_case.py [build_dir]
"""
import collections
import csv
import json
import math
import pathlib
import sys

import networkx as nx

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from score_s3 import alias_matches, load_aliases, words  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAR = json.loads((ROOT / "builder" / "parameters.json").read_text(encoding="utf-8"))
SB = PAR["base_mva"]
SNAPS = ("summer_peak", "winter_offpeak")


def rd(path):
    return list(csv.DictReader(open(path, encoding="utf-8")))


def main(build_dir, params_sub="params", case_sub="case"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    P = build_dir / params_sub
    B = {b["bus"]: b for b in rd(build_dir / "buses.csv")}
    main_buses = sorted(k for k, b in B.items() if b["in_main"] == "1")
    idx = {k: i + 1 for i, k in enumerate(main_buses)}
    lines = [r for r in rd(P / "branch_params.csv") if r["f_bus"] in idx and r["t_bus"] in idx]
    trafos = [r for r in rd(P / "transformer_params.csv") if r["f_bus"] in idx and r["t_bus"] in idx]
    gens = [g for g in rd(P / "generators.csv") if g["status"] == "1" and g["bus"] in idx]
    loads = [l for l in rd(P / "loads.csv") if l["bus"] in idx]
    reac = [r for r in rd(P / "reactors.csv") if r["bus"] in idx]
    caps = [r for r in rd(P / "capacitors.csv") if r["bus"] in idx]
    dcl = json.loads((P / "dcline.json").read_text(encoding="utf-8"))
    A = PAR["assembly"]
    xmin = A["short_branch_floor"]["x_min_pu"]
    notes = []

    # ---- lines as dicts (+ impedance floor)
    L = []
    n_floor = 0
    for r in lines:
        d = {k: float(r[k]) for k in ("br_r", "br_x", "b_fr", "b_to", "rate_a", "rate_b", "rate_c", "angmin", "angmax")}
        if abs(d["br_x"]) < xmin:
            f = xmin / abs(d["br_x"])
            d["br_x"] *= f
            d["br_r"] *= f
            n_floor += 1
        d.update(f_bus=r["f_bus"], t_bus=r["t_bus"], kv=int(float(r["kv"])), circuits=int(r["circuits"]), length_km=float(r["length_km"]),
                 idx=int(r["idx"]), name=r["name"])
        L.append(d)
    notes.append(f"Impedance floor 1e-4 pu applied to {n_floor} lines")

    # ---- winter openings, path rule (rule_v2_18nov)
    from check_pss_lines import CFG as LCFG
    ep_alias = {" ".join(words(k)): v for k, v in LCFG["endpoint_aliases"].items()}
    per = load_aliases()
    s3 = {f"{m['per_name']}@{m['kv']}": m["bus"] for m in rd(build_dir / "s3_matches.csv") if m["bus"]}
    S = {r["id"]: r for r in rd(build_dir / "stations.csv")}
    Pl = {r["id"]: r for r in rd(build_dir / "plants.csv")}
    names_of = {}
    for k, b in B.items():
        if b["kind"] in "SP" and k in idx:
            src = S[b["ref"]] if b["kind"] == "S" else Pl[b["ref"]]
            names_of[k] = [n for n in src["all_names"].split(" | ") if n]

    def cands(name, kv):
        if " ".join(words(name)) == "matiari":
            return {"S:S0675@500"} if kv == 500 else set()
        e2 = ep_alias.get(" ".join(words(name)), name)
        out = set()
        best = [(len(words(a)), r) for r in per for a in r["alias_list"] if alias_matches(a, e2)]
        if best:
            top = max(x[0] for x in best)
            for ln, r in best:
                bus = s3.get(r["key"]) if ln == top else None
                if bus and f"{bus.split('@')[0]}@{kv}" in idx:
                    out.add(f"{bus.split('@')[0]}@{kv}")
        out |= {k for k, ns in names_of.items() if k.endswith(f"@{kv}") and any(alias_matches(e2, n) for n in ns)}
        return out

    G = {kv: nx.MultiGraph() for kv in (500, 220)}
    for i, d in enumerate(L):
        if d["kv"] in G:
            G[d["kv"]].add_edge(d["f_bus"], d["t_bus"], key=i, length=d["length_km"])
    winter_status = {}  # line list index -> (new circuits)
    open_rows = []
    for c in PAR["winter_openings"]["circuits"]:
        kv = c["kv"]
        ca, cb = cands(c["a"], kv), cands(c["b"], kv)
        sets = set()
        for a in ca:
            for b in cb:
                if a == b or a not in G[kv] or b not in G[kv]:
                    continue
                try:
                    path = nx.shortest_path(G[kv], a, b, weight="length")
                except nx.NetworkXNoPath:
                    continue
                if all(p.split(":")[0] in ("J", "D") for p in path[1:-1]):
                    hops = []
                    for u, v in zip(path, path[1:]):
                        es = G[kv].get_edge_data(u, v)
                        k = min(es, key=lambda kk: es[kk]["length"])
                        hops.append(k)
                    sets.add(tuple(sorted(hops)))
        if len(sets) == 1:
            hops = list(sets.pop())
            for k in hops:
                cur = winter_status.get(k, L[k]["circuits"])
                winter_status[k] = cur - c["n"]
            open_rows.append((kv, f"{c['a']} - {c['b']}", c["n"], "mapped", len(hops), round(sum(L[k]["length_km"] for k in hops), 1)))
        else:
            open_rows.append((kv, f"{c['a']} - {c['b']}", c["n"], "unmapped" if not sets else f"ambiguous ({len(sets)})", 0, 0))

    # ---- deliverability check (summer), by DISCO group
    grp = {l["bus"]: l["group"] for l in loads if l["kind"] == "disco"}
    load_xy = [(float(B[b]["lat"]), float(B[b]["lon"]), g) for b, g in grp.items()]

    def group_at(bus):
        if bus in grp:
            return grp[bus]
        la, lo = float(B[bus]["lat"]), float(B[bus]["lon"])
        return min(load_xy, key=lambda t: (t[0] - la) ** 2 + ((t[1] - lo) * math.cos(math.radians(la))) ** 2)[2]

    cap_by = collections.defaultdict(float)
    for r in caps:
        if r["snapshot"] == "summer_peak":
            cap_by[r["bus"]] += float(r["mvar_nameplate"])
    P_g, Q_g, T_g, G_g = (collections.defaultdict(float) for _ in range(4))
    for l in loads:
        if l["kind"] == "disco":
            P_g[l["group"]] += float(l["pd_summer_peak"])
            Q_g[l["group"]] += float(l["qd_summer_peak"]) - cap_by.get(l["bus"], 0.0)
    for t in trafos:
        if t["t_bus"].endswith("@132"):
            T_g[group_at(t["t_bus"])] += float(t["rate_a"]) * SB
    for g in gens:
        if g["bus"].endswith("@132") or g["bus"].endswith("@66"):
            G_g[group_at(g["bus"])] += float(g["pmax_summer"])

    # ---- write cases
    bus_kind = {}
    for snap in SNAPS:
        slack = "S:S0036@500" if snap == "summer_peak" else "S:S0692@500"
        gen_buses = {g["bus"] for g in gens if float(g[f"pmax_{snap.split('_')[0]}"]) > 0}
        case = {"name": f"pakistan_synthetic_{snap}", "per_unit": True, "baseMVA": SB, "source_type": "matpower",
                "source_version": "2", "target_snapshot": snap, "bus": {}, "branch": {}, "gen": {}, "load": {}, "shunt": {},
                "dcline": {}, "storage": {}, "switch": {}}
        for k in main_buses:
            b = B[k]
            t = 3 if k == slack else (2 if k in gen_buses else 1)
            case["bus"][str(idx[k])] = {"index": idx[k], "bus_i": idx[k], "bus_type": t, "vm": 1.0, "va": 0.0,
                                        "vmin": PAR["buses"]["vmin"], "vmax": PAR["buses"]["vmax"], "base_kv": float(b["kv"]),
                                        "zone": 1, "area": 1, "name": f"{k} {b['name']}".strip(), "lat": float(b["lat"]), "lon": float(b["lon"])}
        n = 0
        for i, d in enumerate(L):
            c0 = d["circuits"]
            c1 = winter_status.get(i, c0) if snap == "winter_offpeak" else c0
            n += 1
            if c1 <= 0:
                st, fz, fy = 0, 1.0, 1.0
            else:
                st, fz, fy = 1, c0 / c1, c1 / c0
            case["branch"][str(n)] = {"index": n, "f_bus": idx[d["f_bus"]], "t_bus": idx[d["t_bus"]], "br_r": d["br_r"] * fz, "br_x": d["br_x"] * fz,
                                      "g_fr": 0.0, "g_to": 0.0, "b_fr": d["b_fr"] * fy, "b_to": d["b_to"] * fy, "rate_a": d["rate_a"] * fy,
                                      "rate_b": d["rate_b"] * fy, "rate_c": d["rate_c"] * fy, "tap": 1.0, "shift": 0.0, "angmin": d["angmin"],
                                      "angmax": d["angmax"], "transformer": False, "br_status": st, "length_km": d["length_km"],
                                      "circuit_key": f"L{d['idx']}_{d['kv']}"}
        for t in trafos:
            n += 1
            case["branch"][str(n)] = {"index": n, "f_bus": idx[t["f_bus"]], "t_bus": idx[t["t_bus"]], "br_r": float(t["br_r"]), "br_x": float(t["br_x"]),
                                      "g_fr": 0.0, "g_to": 0.0, "b_fr": 0.0, "b_to": 0.0, "rate_a": float(t["rate_a"]), "rate_b": float(t["rate_b"]),
                                      "rate_c": float(t["rate_c"]), "tap": float(t["tap"]), "tap_min": float(t["tap_min"]), "tap_max": float(t["tap_max"]),
                                      "shift": 0.0, "angmin": float(t["angmin"]), "angmax": float(t["angmax"]), "transformer": True, "br_status": 1,
                                      "transformer_hv_kv": float(t["transformer_hv_kv"]), "transformer_lv_kv": float(t["transformer_lv_kv"]),
                                      "length_km": 0.0, "circuit_key": f"T_{t['f_bus']}_{t['t_bus']}"}
        s = snap.split("_")[0]
        for j, g in enumerate(gens, 1):
            pmax, pmin = float(g[f"pmax_{s}"]) / SB, float(g[f"pmin_{s}"]) / SB
            case["gen"][str(j)] = {"index": j, "gen_bus": idx[g["bus"]], "gen_status": 1 if pmax > 0 else 0, "pg": (pmin + pmax) / 2, "qg": 0.0,
                                   "pmax": pmax, "pmin": pmin, "qmax": float(g[f"qmax_{s}"]) / SB, "qmin": float(g[f"qmin_{s}"]) / SB,
                                   "vg": 1.0, "mbase": float(g["installed_mw"]), "model": 2, "ncost": 3, "startup": 0.0, "shutdown": 0.0,
                                   "cost": [0.0, float(g["c1_usd_mwh"]) * SB, 0.0], "fuel_type": g["fuel"], "name": g["name"]}
        for j, l in enumerate(loads, 1):
            case["load"][str(j)] = {"index": j, "load_bus": idx[l["bus"]], "pd": float(l[f"pd_{snap}"]) / SB, "qd": float(l[f"qd_{snap}"]) / SB,
                                    "status": 1, "name": f"{l['kind']}:{l['group']}"}
        j = 0
        for r in reac + caps:
            if r["snapshot"] != snap:
                continue
            j += 1
            case["shunt"][str(j)] = {"index": j, "shunt_bus": idx[r["bus"]], "gs": 0.0, "bs": float(r["bs_pu"]), "status": 1}
        d = dict(dcl[snap])
        d.update(index=1, f_bus=idx[d["f_bus"]], t_bus=idx[d["t_bus"]])
        case["dcline"]["1"] = d
        out = build_dir / case_sub
        out.mkdir(exist_ok=True)
        (out / f"pk_{snap}.json").write_text(json.dumps(case), encoding="utf-8")
        bus_kind[snap] = (len(case["bus"]), len(case["branch"]), sum(1 for x in case["gen"].values() if x["gen_status"]), len(case["load"]), len(case["shunt"]),
                          sum(x["pd"] for x in case["load"].values()) * SB, sum(x["pmax"] for x in case["gen"].values() if x["gen_status"]) * SB,
                          sum(1 for x in case["branch"].values() if x["br_status"] == 0))

    Lx = [f"# Day 9 case assembly ({build_dir.name} build)\n", "Rules: builder/parameters.json `assembly` and `winter_openings.rule_v2_18nov` (commit 5bcee71, pushed before this ran).\n", "## Cases\n",
          "| snapshot | buses | branches | gens on | loads | shunts | load MW | gen Pmax MW | branches out |", "|---|---|---|---|---|---|---|---|---|"]
    for snap, v in bus_kind.items():
        Lx.append(f"| {snap} | {v[0]} | {v[1]} | {v[2]} | {v[3]} | {v[4]} | {v[5]:,.0f} | {v[6]:,.0f} | {v[7]} |")
    Lx += ["", "- " + "; ".join(notes), "\n## Winter openings (TSEP Table 5-7, path rule)\n", "| kV | circuit | open | status | branches | km |", "|---|---|---|---|---|---|"]
    for r in open_rows:
        Lx.append("| " + " | ".join(str(x) for x in r) + " |")
    Lx.append(f"\nMapped {sum(1 for r in open_rows if r[3] == 'mapped')} of {len(open_rows)}.\n")
    Lx += ["## Load deliverability (summer, before any solve)\n",
           "Per DISCO group: load MVA net of capacitors vs transformer capacity into its 132 kV buses plus generation connected at 132/66 kV. 132 kV lines between groups are not counted.\n",
           "| group | load MW | net MVAr | net MVA | 220&500/132 kV transformer MVA | 132/66 kV gen MW | (trafo + gen) / load MVA |", "|---|---|---|---|---|---|---|"]
    for g in sorted(P_g, key=lambda k: -P_g[k]):
        mva = math.hypot(P_g[g], Q_g[g])
        Lx.append(f"| {g} | {P_g[g]:,.0f} | {Q_g[g]:,.0f} | {mva:,.0f} | {T_g[g]:,.0f} | {G_g[g]:,.0f} | {(T_g[g] + G_g[g]) / mva:.2f} |")
    (build_dir / case_sub / "case_summary.md").write_text("\n".join(Lx) + "\n", encoding="utf-8")
    print("\n".join(Lx))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(pathlib.Path(a[0]) if a else ROOT / "osm" / "build" / "explicit", *(a[1:3]))
