"""Day 6: apply the electrical parameter rules (builder/parameters.json, committed before this ran) to a build.

Writes <build>/params/: branch_params.csv (+ variant files), transformer_params.csv, reactors.csv,
dcline.json, winter_openings.csv, and summary.md.
Usage: python builder/make_parameters.py [build_dir]
"""
import cmath
import collections
import csv
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from score_s3 import alias_matches, load_aliases, words  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAR = json.loads((ROOT / "builder" / "parameters.json").read_text(encoding="utf-8"))
SB = PAR["base_mva"]
F = 50.0


def zbase(kv):
    return kv * kv / SB


def line_pu(cls, kv, length_km, n):
    """Exact equivalent pi for one circuit, then n in parallel; per unit on SB at the bus kV."""
    z = complex(cls["r_ohm_km"], cls["x_ohm_km"])
    y = complex(0.0, cls["b_us_km"] * 1e-6)
    L = max(length_km, 1e-3)
    gl = cmath.sqrt(z * y) * L
    zc = cmath.sqrt(z / y)
    Zp = zc * cmath.sinh(gl)
    Yh = cmath.tanh(gl / 2) / zc  # Y'/2
    Zp, Yh = Zp / n, Yh * n
    zb = zbase(kv)
    return Zp.real / zb, Zp.imag / zb, Yh.imag * zb  # r, x, b_half


def main(build_dir):
    out = build_dir / "params"
    out.mkdir(exist_ok=True)
    B = {b["bus"]: b for b in csv.DictReader(open(build_dir / "buses.csv", encoding="utf-8"))}
    br = list(csv.DictReader(open(build_dir / "branches.csv", encoding="utf-8")))
    tr = list(csv.DictReader(open(build_dir / "transformers.csv", encoding="utf-8")))
    s3 = list(csv.DictReader(open(build_dir / "s3_matches.csv", encoding="utf-8")))
    LP = PAR["lines"]
    rb, rc = LP["rate_b_factor"], LP["rate_c_factor"]
    ang = math.radians(LP["angle_limit_deg"])

    # ---------------- lines
    def line_rows(classes):
        rows = []
        for i, b in enumerate(br):
            kv_tag = b["kv"]
            cname = LP["voltage_class_map"][kv_tag]
            cls = classes[cname]
            kv_bus = float(kv_tag)
            n = int(b["circuits"])
            r, x, bh = line_pu(cls, kv_bus, float(b["len_km"]), n)
            rate = cls["rate_a_mva"] * n / SB
            rows.append({"idx": i, "f_bus": b["from"], "t_bus": b["to"], "kv": kv_tag, "class": cname, "circuits": n,
                         "length_km": b["len_km"], "br_r": r, "br_x": x, "g_fr": 0.0, "g_to": 0.0, "b_fr": bh, "b_to": bh,
                         "rate_a": rate, "rate_b": rate * rb, "rate_c": rate * rc, "angmin": -ang, "angmax": ang,
                         "transformer": False, "ways": b["ways"], "name": b["name"]})
        return rows

    scored = line_rows(LP["classes"])
    variants = {}
    for vname, vcls in PAR["line_sensitivity_variants"].items():
        if vname.startswith("_"):
            continue
        cls = {k: dict(v) for k, v in LP["classes"].items()}
        key = vname.split("_")[0]
        cls[key].update({k: v for k, v in vcls.items()})
        variants[vname] = line_rows(cls)

    def wcsv(path, rows):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    wcsv(out / "branch_params.csv", scored)
    for vname, rows in variants.items():
        wcsv(out / f"branch_params_variant_{vname}.csv", rows)

    # ---------------- transformers: PSS units by station (via PER aliases and the S3 assignment)
    per = load_aliases()
    s3_bus = {f"{m['per_name']}@{m['kv']}": m["bus"] for m in s3 if m["bus"]}
    pss_units = collections.defaultdict(list)  # station ref -> [(units, mva, pss_name)]
    pss_log = []
    for kv, fname in ((500, "pss44_gs_500kv.csv"), (220, "pss44_gs_220kv.csv")):
        for g in csv.DictReader(open(ROOT / "sources" / "extracted" / fname, encoding="utf-8")):
            hits = []
            for r in per:
                for a in r["alias_list"]:
                    if alias_matches(a, g["name"]):
                        hits.append((len(words(a)), r["kv"] == kv, r))
            if not hits:
                pss_log.append((g["name"], kv, "no PER station"))
                continue
            top = max(hits, key=lambda h: (h[0], h[1]))
            bus = s3_bus.get(top[2]["key"])
            if not bus:
                pss_log.append((g["name"], kv, f"PER {top[2]['per_name']} has no S3 bus"))
                continue
            ref = bus.split(":")[1].split("@")[0]
            for part in g["transformers"].split(" + "):
                k, mva = part.split("x")
                pss_units[ref].append((int(k), int(mva), g["name"]))
            pss_log.append((g["name"], kv, f"-> {ref} via PER {top[2]['per_name']}"))

    TP = PAR["transformers"]
    trows = []
    used_pss = collections.defaultdict(set)
    for t in tr:
        hv, lv = int(t["hv_kv"]), int(t["lv_kv"])
        pair = f"{hv}-{lv}"
        ref = t["hv_bus"].split(":")[1].split("@")[0]
        units = []
        if pair in ("500-220", "220-132"):
            for k, mva, nm in pss_units.get(ref, []):
                if (pair == "500-220" and mva >= 450) or (pair == "220-132" and mva in (160, 250, 320)):
                    units.append((k, mva))
                    used_pss[ref].add(nm)
        d = TP["defaults"][pair]
        if units:
            s_total = sum(k * m for k, m in units)
            x_own = TP["pss_pair_x_own"][pair]
            src = "PSS44 " + " + ".join(f"{k}x{m}" for k, m in units)
        else:
            s_total = d["units"] * d["unit_mva"]
            x_own = d["x_own"]
            src = f"default {d['units']}x{d['unit_mva']}"
        x = x_own * SB / s_total
        r = x / d["xr"]
        rate = s_total / SB
        trows.append({"f_bus": t["hv_bus"], "t_bus": t["lv_bus"], "pair": pair, "source": src, "s_total_mva": s_total,
                      "x_own": x_own, "br_r": r, "br_x": x, "g_fr": 0.0, "g_to": 0.0, "b_fr": 0.0, "b_to": 0.0,
                      "rate_a": rate, "rate_b": rate * TP["rate_b_factor"], "rate_c": rate * TP["rate_c_factor"],
                      "tap": TP["tap"], "tap_min": TP["tap_min"], "tap_max": TP["tap_max"], "shift": 0.0,
                      "angmin": -math.radians(TP["angle_limit_deg"]), "angmax": math.radians(TP["angle_limit_deg"]),
                      "transformer": True, "transformer_hv_kv": hv, "transformer_lv_kv": lv})
    wcsv(out / "transformer_params.csv", trows)

    # ---------------- reactors
    SH = PAR["shunts"]
    fixed, pooled_extra = [], 0
    for e in SH["reactors_fixed_table_5_9"]:
        bus = s3_bus.get(f"{e['per_name']}@{e['kv']}")
        if bus and bus in B:
            fixed.append((bus, e["mvar"], f"TSEP T5-9 {e.get('tsep_name', e['per_name'])}"))
        else:
            pooled_extra += e["mvar"]
            fixed.append((None, e["mvar"], f"TSEP T5-9 {e['per_name']}: no bus, into pool"))
    weight = collections.defaultdict(float)
    for row in scored:
        if row["kv"] != "500":
            continue
        q_half = row["b_fr"] * SB  # MVAr at 1 pu at each end (half of total charging)
        for end in (row["f_bus"], row["t_bus"]):
            b = B[end]
            if b["kind"] in "SP" and b["prov"] in ("substation", "plant", "converter") and b["in_main"] == "1":
                weight[end] += q_half
    wsum = sum(weight.values())
    rrows = []
    for snap, total in SH["reactor_total_mvar"].items():
        placed = sum(m for b, m, _ in fixed if b)
        pool = total - placed
        for b, m, src in fixed:
            if b:
                rrows.append({"snapshot": snap, "bus": b, "mvar_nameplate": m, "bs_pu": -m / SB, "source": src})
        for b, w in sorted(weight.items()):
            m = pool * w / wsum
            rrows.append({"snapshot": snap, "bus": b, "mvar_nameplate": round(m, 3), "bs_pu": -m / SB,
                          "source": "pool: half charging of incident 500 kV circuits"})
    wcsv(out / "reactors.csv", rrows)

    # ---------------- dcline
    DC = PAR["dcline"]
    dcl = {}
    for snap, p in DC["setpoint_mw"].items():
        dcl[snap] = {"f_bus": DC["f_bus"], "t_bus": DC["t_bus"], "br_status": 1, "model": 2, "ncost": 0, "cost": [],
                     "pf": p / SB, "pt": -p * (1 - DC["loss1"]) / SB, "pminf": p / SB, "pmaxf": p / SB,
                     "pmint": -p / SB, "pmaxt": 0.0,
                     "qf": 0.0, "qt": 0.0, "qminf": -DC["q_range_mvar"] / SB, "qmaxf": DC["q_range_mvar"] / SB,
                     "qmint": -DC["q_range_mvar"] / SB, "qmaxt": DC["q_range_mvar"] / SB,
                     "loss0": DC["loss0_mw"] / SB, "loss1": DC["loss1"], "vf": DC["vf"], "vt": DC["vt"],
                     "length_km": 887.04, "_note": "transfer fixed at the snapshot set-point; pt bounds follow PowerModels' loss convention"}
    (out / "dcline.json").write_text(json.dumps(dcl, indent=1), encoding="utf-8")

    # ---------------- winter openings (direct branches only)
    from check_pss_lines import CFG as LCFG  # endpoint aliases
    ep_alias = {" ".join(words(k)): v for k, v in LCFG["endpoint_aliases"].items()}
    names_of = {}
    S = {r["id"]: r for r in csv.DictReader(open(build_dir / "stations.csv", encoding="utf-8"))}
    P = {r["id"]: r for r in csv.DictReader(open(build_dir / "plants.csv", encoding="utf-8"))}
    for bus, b in B.items():
        if b["kind"] in "SP":
            srcrow = S[b["ref"]] if b["kind"] == "S" else P[b["ref"]]
            names_of[bus] = [n for n in srcrow["all_names"].split(" | ") if n]

    def cands(name, kv):
        e2 = ep_alias.get(" ".join(words(name)), name)
        out_ = set()
        best = []
        for r in per:
            for a in r["alias_list"]:
                if alias_matches(a, e2):
                    best.append((len(words(a)), r))
        if best:
            top = max(x[0] for x in best)
            for ln, r in best:
                bus = s3_bus.get(r["key"]) if ln == top else None
                if bus:
                    cand = f"{bus.split('@')[0]}@{kv}"
                    if cand in B:
                        out_.add(cand)
        out_ |= {bus for bus, ns in names_of.items() if bus.endswith(f"@{kv}") and any(alias_matches(e2, n) for n in ns)}
        return out_

    direct = collections.defaultdict(list)
    for row in scored:
        direct[frozenset((row["f_bus"], row["t_bus"]))].append(row)
    orows = []
    for c in PAR["winter_openings"]["circuits"]:
        ca, cb = cands(c["a"], c["kv"]), cands(c["b"], c["kv"])
        pairs = [(a, b) for a in ca for b in cb if a != b and direct.get(frozenset((a, b)))]
        if len(pairs) == 1:
            a, b = pairs[0]
            rows = direct[frozenset((a, b))]
            orows.append({"kv": c["kv"], "circuit": f"{c['a']} - {c['b']}", "n_open": c["n"], "status": "mapped",
                          "bus_a": a, "bus_b": b, "branch_idx": ";".join(str(r["idx"]) for r in rows),
                          "circuits_before": sum(r["circuits"] for r in rows), "candidates_a": len(ca), "candidates_b": len(cb)})
        else:
            orows.append({"kv": c["kv"], "circuit": f"{c['a']} - {c['b']}", "n_open": c["n"],
                          "status": "unmapped" if not pairs else f"ambiguous ({len(pairs)} direct pairs)",
                          "bus_a": ";".join(sorted(ca))[:80], "bus_b": ";".join(sorted(cb))[:80], "branch_idx": "",
                          "circuits_before": "", "candidates_a": len(ca), "candidates_b": len(cb)})
    wcsv(out / "winter_openings.csv", orows)

    # ---------------- summary
    def charging(rows):
        tot = collections.defaultdict(float)
        for r in rows:
            tot[r["class"]] += 2 * r["b_fr"] * SB
        return tot

    L = [f"# Day 6 parameters ({build_dir.name} build)\n",
         "Rules: builder/parameters.json (commit 747be71, before this ran). All MVAr at 1.0 pu.\n",
         "## Lines\n", "| class | branches | circuit-km | R+jX range (pu) | charging MVAr at 1 pu |", "|---|---|---|---|---|"]
    ch = charging(scored)
    for cname in ("500", "220", "132", "66"):
        rs = [r for r in scored if r["class"] == cname]
        ckm = sum(float(r["length_km"]) * r["circuits"] for r in rs)
        L.append(f"| {cname} kV | {len(rs)} | {ckm:,.0f} | x {min(r['br_x'] for r in rs):.5f}–{max(r['br_x'] for r in rs):.4f} | {ch[cname]:,.0f} |")
    L.append(f"\n- **Total line charging at 1.0 pu: {sum(ch.values()):,.0f} MVAr** (reported only, H2; TSEP summer 17,517 / winter off-peak 15,897 are PSS/E values at solved voltages for a network that includes KE's 132 kV and the parts OSM lacks).")
    for vname, rows in variants.items():
        chv = charging(rows)
        L.append(f"- Variant {vname}: total charging {sum(chv.values()):,.0f} MVAr (reported only).")
    L += ["\n## Transformers\n", "| pair | branches | from PSS 44th | default | total MVA |", "|---|---|---|---|---|"]
    for pair in ("500-220", "500-132", "220-132", "132-66", "132-110"):
        rs = [t for t in trows if t["pair"] == pair]
        if rs:
            L.append(f"| {pair} | {len(rs)} | {sum(t['source'].startswith('PSS') for t in rs)} | {sum(t['source'].startswith('default') for t in rs)} | {sum(t['s_total_mva'] for t in rs):,} |")
    L.append("\nPSS 44th station rows → model stations:")
    for nm, kv, how in pss_log:
        L.append(f"- {kv} kV {nm}: {how}")
    L += ["\n## Reactors (nameplate MVAr at 1.0 pu)\n"]
    for snap, total in SH["reactor_total_mvar"].items():
        got = sum(r["mvar_nameplate"] for r in rrows if r["snapshot"] == snap)
        L.append(f"- {snap}: placed {got:,.1f} MVAr vs TSEP total {total:,} → {'**equal**' if abs(got - total) < 0.5 else '**MISMATCH**'}; "
                 f"{sum(1 for r in rrows if r['snapshot'] == snap)} buses")
    for b, m, src in fixed:
        L.append(f"  - {src}: {m} MVAr at {b or '— (pooled)'}")
    L.append(f"- Pool buses: {len(weight)} 500 kV station buses. Capacitors (12,192 / 146 MVAr) are placed on Day 8 by the declared rule.")
    L += ["\n## HVDC\n", f"- Fixed transfer: summer {DC['setpoint_mw']['summer_peak']} MW, winter off-peak {DC['setpoint_mw']['winter_offpeak']} MW; loss1 {DC['loss1']} "
          f"→ {DC['setpoint_mw']['summer_peak'] * DC['loss1']:.0f} / {DC['setpoint_mw']['winter_offpeak'] * DC['loss1']:.0f} MW dcline loss (reported next to H1/H4)."]
    L += ["\n## Winter openings (TSEP Table 5-7)\n", "| kV | circuit | open | status | buses | branch idx | circuits before |", "|---|---|---|---|---|---|---|"]
    for o in orows:
        L.append(f"| {o['kv']} | {o['circuit']} | {o['n_open']} | {o['status']} | {o['bus_a']} – {o['bus_b']} | {o['branch_idx']} | {o['circuits_before']} |")
    (out / "summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main(pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "osm" / "build" / "explicit")
