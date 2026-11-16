"""Cross-check PSS 44th 500/220 kV line rows (data to June 2019) against a topology build.

Rules are fixed in builder/config.json ("pss_line_check"). For each PSS row:
  - map both endpoints to buses of the build at the row's voltage (via the S3 match table, else a unique OSM name);
  - compare the straight-line distance and the shortest OSM path at that voltage with the PSS route km;
  - propose circuit corrections only under correct_rule.
Writes <build>/pss_line_check.csv and .md, and builder/circuit_overrides.csv (only with --write-overrides).
Usage: python builder/check_pss_lines.py [build_dir] [--write-overrides]
"""
import collections
import csv
import json
import math
import pathlib
import re
import sys

import networkx as nx

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from score_s3 import alias_matches, load_aliases, words  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "builder" / "config.json").read_text(encoding="utf-8"))["pss_line_check"]
EXT = ROOT / "sources" / "extracted"

PRE = [(r"^\s*220\s*KV\s*", ""), (r"TPS-M/([Gg])arh", r"TPS M/\1arh"), (r"\(Tower # 1 to 150\)", ""),
       (r"\(SKL\)", ""), (r"\(RT-2\)", "")]
MANUAL = {  # rows whose text has no separator between the two endpoints
    (500, "Islamabad", 6): ("Rawat", "Neelum Jehlum"),
    (500, "Islamabad", 7): ("Neelum Jehlum", "Ghakkhar"),
    (220, "Lahore", 3): ("Gatti", "JWR"),
}


def hav_km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(h))


def endpoints(r):
    key = (int(r["kv"]), r["region"], int(r["sr"]))
    if key in MANUAL:
        return MANUAL[key]
    s = r["name"]
    for a, b in PRE:
        s = re.sub(a, b, s)
    s = re.sub(r"\s*\b(?:CCT|Cct)\b.*$", "", s)
    for _ in range(3):
        s = re.sub(r"\s+\d\s*&\s*\d\s*$", "", s)
        s = re.sub(r"[\s-]+(?:I{1,3}|IV|[1-4])\s*$", "", s)
    parts = [p.strip() for p in re.split(r"\s*-\s*", s) if p.strip()]
    return tuple(parts) if len(parts) == 2 else None


def two_circuit_row(r):
    route = int(r["sc_route_km"]) + int(r["dc_route_km"])
    return route > 0 and int(r["circuit_km"]) >= 1.8 * route


def main(build_dir, write_overrides):
    B = {b["bus"]: b for b in csv.DictReader(open(build_dir / "buses.csv", encoding="utf-8"))}
    S = {r["id"]: r for r in csv.DictReader(open(build_dir / "stations.csv", encoding="utf-8"))}
    P = {r["id"]: r for r in csv.DictReader(open(build_dir / "plants.csv", encoding="utf-8"))}
    s3 = {f"{m['per_name']}@{m['kv']}": m for m in csv.DictReader(open(build_dir / "s3_matches.csv", encoding="utf-8"))}
    per = load_aliases()
    ep_alias = {" ".join(words(k)): v for k, v in CFG["endpoint_aliases"].items()}

    names_of = {}
    for bus, b in B.items():
        if b["kind"] in "SP":
            src = S[b["ref"]] if b["kind"] == "S" else P[b["ref"]]
            names_of[bus] = [n for n in src["all_names"].split(" | ") if n]

    def map_ep(e, kv):
        e2 = ep_alias.get(" ".join(words(e)), e)
        # 1) a PER station (most specific alias wins; same voltage first), via its S3 bus
        best = []
        for r in per:
            for a in r["alias_list"]:
                if alias_matches(a, e2):
                    best.append((len(words(a)), r["kv"] == kv, r))
        if best:
            top = max(best, key=lambda x: (x[0], x[1]))
            tied = {x[2]["key"] for x in best if (x[0], x[1]) == (top[0], top[1])}
            m = s3.get(top[2]["key"])
            if m and m["bus"]:
                ref = m["bus"].split(":")[1].split("@")[0]
                kind = m["bus"][0]
                cand = f"{kind}:{ref}@{kv}"
                if cand in B and len({s3[k]["bus"].split("@")[0] for k in tied if s3.get(k) and s3[k]["bus"]}) == 1:
                    return cand, f"PER {top[2]['per_name']} ({m['tier'].split(' ')[0]})"
                if cand not in B:
                    return None, f"PER {top[2]['per_name']}: station has no {kv} kV bus"
        # 2) a unique OSM station/plant with a bus at this voltage whose name matches
        hits = sorted({bus for bus, ns in names_of.items() if bus.endswith(f"@{kv}") and any(alias_matches(e2, n) for n in ns)})
        if len(hits) == 1:
            return hits[0], f"OSM name '{names_of[hits[0]][0]}'"
        return None, ("ambiguous: " + ", ".join(hits[:3])) if hits else "no OSM match"

    G = {kv: nx.MultiGraph() for kv in (500, 220)}
    for i, br in enumerate(csv.DictReader(open(build_dir / "branches.csv", encoding="utf-8"))):
        kv = int(br["kv"])
        if kv in G:
            G[kv].add_edge(br["from"], br["to"], key=i, len_km=float(br["len_km"]), circuits=int(br["circuits"]),
                           src=br["circuits_src"], ways=br["ways"], name=br["name"])

    def simple(kv):
        H = nx.Graph()
        for u, v, d in G[kv].edges(data=True):
            if not H.has_edge(u, v) or d["len_km"] < H[u][v]["len_km"]:
                H.add_edge(u, v, len_km=d["len_km"])
        return H

    H = {kv: simple(kv) for kv in G}
    rows, pairs = [], collections.defaultdict(list)
    for kv in (500, 220):
        for r in csv.DictReader(open(EXT / f"pss44_lines_{kv}kv.csv", encoding="utf-8")):
            if r["usable"] != "yes":
                continue
            route = int(r["sc_route_km"]) + int(r["dc_route_km"])
            out = {"kv": kv, "region": r["region"], "sr": r["sr"], "pss_name": r["name"], "route_km": route,
                   "sc_km": r["sc_route_km"], "dc_km": r["dc_route_km"], "two_circuit_row": int(two_circuit_row(r)),
                   "a": "", "b": "", "bus_a": "", "bus_b": "", "map_a": "", "map_b": "", "straight_km": "",
                   "path_km": "", "path_ratio": "", "flags": "", "path_hops": ""}
            ep = endpoints(r)
            if not ep:
                out["flags"] = "not checked: endpoints not parseable (one or three names)"
                rows.append(out)
                continue
            out["a"], out["b"] = ep
            (ba, ma), (bb, mb) = map_ep(ep[0], kv), map_ep(ep[1], kv)
            out.update(bus_a=ba or "", bus_b=bb or "", map_a=ma, map_b=mb)
            if not (ba and bb) or ba == bb:
                out["flags"] = "not checked: endpoint not mapped" if not (ba and bb) else "not checked: both ends map to one bus"
                rows.append(out)
                continue
            pa, pb = (float(B[ba]["lat"]), float(B[ba]["lon"])), (float(B[bb]["lat"]), float(B[bb]["lon"]))
            st = hav_km(pa, pb)
            out["straight_km"] = round(st, 1)
            flags = []
            if st > CFG["too_far_ratio"] * route:
                flags.append("too far (straight line > 1.1 x route)")
            if route > CFG["too_close_factor"] * st + CFG["too_close_plus_km"]:
                flags.append("too close (route > 2 x straight + 10 km)")
            try:
                path = nx.shortest_path(H[kv], ba, bb, weight="len_km")
                pk = sum(H[kv][u][v]["len_km"] for u, v in zip(path, path[1:]))
                out["path_km"] = round(pk, 1)
                out["path_ratio"] = round(pk / route, 3)
                hops = []
                for u, v in zip(path, path[1:]):
                    par = list(G[kv].get_edge_data(u, v).values())
                    hops.append({"u": u, "v": v, "n_par": len(par), "circ": sum(d["circuits"] for d in par),
                                 "srcs": ";".join(sorted({d["src"] for d in par})), "ways": [d["ways"] for d in par],
                                 "km": min(d["len_km"] for d in par)})
                out["path_hops"] = " / ".join(f"{h['circ']}c[{h['srcs']}] {h['km']:.0f}km" for h in hops)
                if abs(pk - route) > CFG["corridor_tolerance"] * route:
                    flags.append(f"path differs from route by more than 10%")
                pairs[(kv, frozenset((ba, bb)))].append((r, out, hops, pk))
            except nx.NetworkXNoPath:
                flags.append("no path at this voltage")
            out["flags"] = "; ".join(flags) or "ok"
            rows.append(out)

    # ---- circuit corrections (correct_rule)
    overrides = []
    for (kv, pair), items in pairs.items():
        rs = [it[0] for it in items]
        if not all(int(r["sc_route_km"]) == 0 and int(r["dc_route_km"]) > 0 and two_circuit_row(r) for r in rs):
            continue
        route = max(int(r["dc_route_km"]) for r in rs)
        hops, pk = items[0][2], items[0][3]
        if abs(pk - route) > CFG["corridor_tolerance"] * route:
            continue
        for h in hops:
            if h["n_par"] == 1 and h["srcs"] == "default1":
                for w in h["ways"][0].split(";"):
                    overrides.append({"way": w, "circuits": 2, "kv": kv, "hop": f"{h['u']}-{h['v']}", "hop_km": h["km"],
                                      "reason": f"PSS44 {kv} kV '{rs[0]['name']}' ({rs[0]['region']} {rs[0]['sr']}): "
                                                f"double circuit {route} km; OSM path {pk:.0f} km"})
    seen, uniq = set(), []
    for o in overrides:
        if o["way"] not in seen:
            seen.add(o["way"])
            uniq.append(o)

    cols = list(rows[0].keys())
    with open(build_dir / "pss_line_check.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    if write_overrides:
        with open(ROOT / "builder" / "circuit_overrides.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["way", "circuits", "kv", "hop", "hop_km", "reason"])
            w.writeheader()
            w.writerows(uniq)

    c = collections.Counter()
    for o in rows:
        c[(o["kv"], "checked" if o["flags"] and not o["flags"].startswith("not checked") else "not checked")] += 1
    L = [f"# PSS 44th line cross-check ({build_dir.name} build)\n",
         "Rules: builder/config.json `pss_line_check` (fixed before the first run). PSS data is to June 2019; flags are for review, nothing is removed.\n"]
    for kv in (500, 220):
        rk = [o for o in rows if o["kv"] == kv]
        chk = [o for o in rk if not o["flags"].startswith("not checked")]
        L.append(f"- {kv} kV: {len(rk)} usable rows; {len(chk)} checked; ok {sum(o['flags'] == 'ok' for o in chk)}; "
                 f"too far {sum('too far' in o['flags'] for o in chk)}; too close {sum('too close' in o['flags'] for o in chk)}; "
                 f"path differs >10% {sum('path differs' in o['flags'] for o in chk)}; no path {sum('no path' in o['flags'] for o in chk)}")
    hop_km = sum(o["hop_km"] for o in {o["hop"]: o for o in uniq}.values())
    L.append(f"- Circuit corrections under correct_rule: {len({o['hop'] for o in uniq})} branches ({len(uniq)} OSM ways), "
             f"{hop_km:.0f} route-km raised from 1 to 2 circuits\n")
    L += ["| kV | region | sr | PSS line | route km | bus A | bus B | straight km | path km | ratio | flags |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for o in rows:
        L.append(f"| {o['kv']} | {o['region']} | {o['sr']} | {o['pss_name']} | {o['route_km']} | {o['bus_a'] or o['map_a'] or '—'} | "
                 f"{o['bus_b'] or o['map_b'] or '—'} | {o['straight_km']} | {o['path_km']} | {o['path_ratio']} | {o['flags']} |")
    (build_dir / "pss_line_check.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[2:5]))
    return rows, uniq


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(pathlib.Path(args[0]) if args else ROOT / "osm" / "build" / "explicit", "--write-overrides" in sys.argv)
