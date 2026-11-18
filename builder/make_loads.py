"""Day 8: place DISCO loads, the K-Electric export and capacitors under builder/parameters.json["loads"]
(commit 8c77814, pushed before this ran). Writes <build>/params/loads.csv, capacitors.csv, loads_summary.md.
Usage: python builder/make_loads.py [build_dir]
"""
import collections
import csv
import json
import math
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from score_s3 import alias_matches, load_aliases, words  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAR = json.loads((ROOT / "builder" / "parameters.json").read_text(encoding="utf-8"))
L8 = PAR["loads"]
SB = PAR["base_mva"]


def hav(a, b, c, d):
    p1, p2 = math.radians(a), math.radians(c)
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(d - b) / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(h))


def group_of(label):
    ds = re.findall(r"LESCO|GEPCO|FESCO|IESCO|MEPCO|PESCO|HESCO|QESCO|TESCO|SEPCO|K Electric", label)
    if not ds or ds[0] == "K Electric":
        return None
    if ds[0] in ("PESCO", "TESCO"):
        return "PESCO+TESCO"
    return ds[0]


def main(build_dir):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ext = ROOT / "sources" / "extracted"
    B = {b["bus"]: b for b in csv.DictReader(open(build_dir / "buses.csv", encoding="utf-8"))}
    S = {r["id"]: r for r in csv.DictReader(open(build_dir / "stations.csv", encoding="utf-8"))}
    s3 = {f"{m['per_name']}@{m['kv']}": m["bus"] for m in csv.DictReader(open(build_dir / "s3_matches.csv", encoding="utf-8")) if m["bus"]}
    per = load_aliases()

    # ---- anchors: PSS 44th NTDC stations with DISCO labels, mapped to model stations via S3
    anchors = []
    for kv, fn in ((500, "pss44_gs_500kv.csv"), (220, "pss44_gs_220kv.csv")):
        for g in csv.DictReader(open(ext / fn, encoding="utf-8")):
            grp = group_of(g["disco"])
            if not grp:
                continue
            hits = [(len(words(a)), r["kv"] == kv, r) for r in per for a in r["alias_list"] if alias_matches(a, g["name"])]
            if not hits:
                continue
            top = max(hits, key=lambda h: (h[0], h[1]))[2]
            bus = s3.get(top["key"])
            if not bus:
                continue
            ref = bus.split(":")[1].split("@")[0]
            st = S.get(ref)
            if st:
                anchors.append({"group": grp, "pss": g["name"], "ref": ref, "lat": float(st["lat"]), "lon": float(st["lon"])})

    # ---- load stations
    by_station = collections.defaultdict(dict)
    for b in B.values():
        if b["kind"] == "S" and b["prov"] == "substation" and b["in_main"] == "1" and b["kv"] in ("132", "66"):
            by_station[b["ref"]][b["kv"]] = b
    stations = []
    excluded = collections.Counter()
    for ref, kvs in by_station.items():
        st = S[ref]
        if "generation" in st["subtypes"]:
            excluded["generation subtype"] += 1
            continue
        bus = kvs.get("132") or kvs.get("66")
        if bus["ke"] == "1" or any(x["ke"] == "1" for x in kvs.values()):
            excluded["K-Electric flagged"] += 1
            continue
        la, lo = float(bus["lat"]), float(bus["lon"])
        a = min(anchors, key=lambda x: hav(la, lo, x["lat"], x["lon"]))
        stations.append({"ref": ref, "bus": bus["bus"], "kv": bus["kv"], "group": a["group"], "anchor": a["pss"],
                         "anchor_km": round(hav(la, lo, a["lat"], a["lon"]), 1),
                         "names": [n for n in st["all_names"].split(" | ") if n], "lat": la, "lon": lo})

    # ---- DISCO group totals
    dm = L8["disco_mw_2026_27"]
    grid = {k: v for k, v in dm.items() if k != "Gwadar"}
    gsum, allsum = sum(grid.values()), sum(dm.values())
    groups = collections.defaultdict(float)
    for k, v in grid.items():
        groups["PESCO+TESCO" if k in ("PESCO", "TESCO") else k] += v
    totals = {snap: L8["total_mw"][snap] * gsum / allsum for snap in L8["total_mw"]}

    # ---- within-DISCO weights
    match_log = []
    for st in stations:
        st["weight"], st["wsrc"] = 1.0, "equal"
    for disco, fn in (("FESCO", "fesco_station_md.csv"), ("MEPCO", "mepco_station_md.csv")):
        tab = [r for r in csv.DictReader(open(ext / fn, encoding="utf-8")) if r["mw_2026_27"] and float(r["mw_2026_27"]) > 0]
        mine = [s for s in stations if s["group"] == disco]
        cand = {}
        for r in tab:
            alias = re.sub(r"\(.*?\)", " ", r["name"])
            cand[r["name"] + "#" + r["sno"]] = [s for s in mine if any(alias_matches(alias, n) for n in s["names"])]
        claims = collections.Counter(s["ref"] for c in cand.values() if len(c) == 1 for s in c)
        matched_refs, matched_mw = {}, 0.0
        for r in tab:
            c = cand[r["name"] + "#" + r["sno"]]
            if len(c) == 1 and claims[c[0]["ref"]] == 1:
                matched_refs[c[0]["ref"]] = float(r["mw_2026_27"])
                matched_mw += float(r["mw_2026_27"])
                match_log.append((disco, r["name"], c[0]["ref"], " | ".join(c[0]["names"])[:40], r["mw_2026_27"]))
        unmatched_mw = sum(float(r["mw_2026_27"]) for r in tab) - matched_mw
        un = [s for s in mine if s["ref"] not in matched_refs]
        for s in mine:
            if s["ref"] in matched_refs:
                s["weight"], s["wsrc"] = matched_refs[s["ref"]], f"{disco} table"
            else:
                s["weight"], s["wsrc"] = (unmatched_mw / len(un) if un else 0.0), f"{disco} residual share"
        match_log.append((disco, f"SUMMARY: {len(matched_refs)} of {len(tab)} table stations matched; {matched_mw:,.0f} of {matched_mw + unmatched_mw:,.0f} MW; "
                                 f"{len(un)} of {len(mine)} model stations unmatched", "", "", ""))

    # ---- loads per snapshot
    rows = []
    gw = collections.defaultdict(float)
    for s in stations:
        gw[s["group"]] += s["weight"]
    placed = collections.defaultdict(float)
    for s in stations:
        r = {"bus": s["bus"], "station": s["ref"], "name": (s["names"] or [""])[0], "group": s["group"], "anchor": s["anchor"],
             "anchor_km": s["anchor_km"], "weight_src": s["wsrc"], "kind": "disco"}
        for snap, tot in totals.items():
            share = groups[s["group"]] / gsum
            pd = tot * share * s["weight"] / gw[s["group"]] if gw[s["group"]] else 0.0
            r[f"pd_{snap}"] = round(pd, 4)
            r[f"qd_{snap}"] = round(pd * L8["q_over_p"][snap], 4)
            placed[snap] += pd
        rows.append(r)

    # ---- KE export at interface buses, by rate_a
    br = list(csv.DictReader(open(build_dir / "params" / "branch_params.csv", encoding="utf-8"))) + \
        list(csv.DictReader(open(build_dir / "params" / "transformer_params.csv", encoding="utf-8")))
    kw = collections.defaultdict(float)
    for x in br:
        a, b = B[x["f_bus"]]["ke"] == "1", B[x["t_bus"]]["ke"] == "1"
        if a != b:
            kw[x["f_bus"] if a else x["t_bus"]] += float(x["rate_a"]) * SB
    ksum = sum(kw.values())
    for bus, w in sorted(kw.items()):
        r = {"bus": bus, "station": B[bus]["ref"], "name": B[bus]["name"], "group": "KE export", "anchor": "", "anchor_km": "",
             "weight_src": f"interface rate_a {w:.0f} MVA", "kind": "ke_export"}
        for snap in L8["total_mw"]:
            ke = L8["ke_export"][snap]
            r[f"pd_{snap}"] = round(ke["mw"] * w / ksum, 4)
            r[f"qd_{snap}"] = round(ke["mvar"] * w / ksum, 4)
        rows.append(r)

    cols = ["bus", "station", "name", "group", "kind", "anchor", "anchor_km", "weight_src", "pd_summer_peak", "qd_summer_peak", "pd_winter_offpeak", "qd_winter_offpeak"]
    with open(build_dir / "params" / "loads.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    # ---- capacitors (Day 6 rule): 132 kV DISCO load buses, by reactive load
    cap_tot = PAR["shunts"]["capacitor_total_mvar"]
    caps = []
    q132 = {snap: sum(r[f"qd_{snap}"] for r in rows if r["kind"] == "disco" and B[r["bus"]]["kv"] == "132") for snap in L8["total_mw"]}
    for r in rows:
        if r["kind"] == "disco" and B[r["bus"]]["kv"] == "132":
            for snap in L8["total_mw"]:
                m = cap_tot[snap] * r[f"qd_{snap}"] / q132[snap]
                caps.append({"snapshot": snap, "bus": r["bus"], "mvar_nameplate": round(m, 4), "bs_pu": m / SB})
    with open(build_dir / "params" / "capacitors.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["snapshot", "bus", "mvar_nameplate", "bs_pu"])
        w.writeheader()
        w.writerows(caps)

    # ---- S2 and summary
    gens = list(csv.DictReader(open(build_dir / "params" / "generators.csv", encoding="utf-8")))
    gen_in = sum(float(g["installed_mw"]) for g in gens if g["status"] == "1" and g["bus"] and B[g["bus"]]["in_main"] == "1")
    gen_den = 36424 - sum(float(g["installed_mw"]) for g in gens if g["fuel"] == "import" or float(g["dependable_mw"]) == 0)
    Lx = [f"# Day 8 loads ({build_dir.name} build)\n", "Rules: builder/parameters.json `loads` (commit 8c77814, pushed before this ran).\n", "## Totals\n"]
    for snap in L8["total_mw"]:
        dl = sum(r[f"pd_{snap}"] for r in rows if r["kind"] == "disco")
        ke = sum(r[f"pd_{snap}"] for r in rows if r["kind"] == "ke_export")
        Lx.append(f"- {snap}: DISCO load {dl:,.1f} MW (target {totals[snap]:,.1f} = I1 {L8['total_mw'][snap]:,} x {gsum:,}/{allsum:,}, Gwadar not placed); "
                  f"KE export {ke:,.1f} MW; Q {sum(r[f'qd_{snap}'] for r in rows):,.1f} MVAr; capacitors {sum(c['mvar_nameplate'] for c in caps if c['snapshot'] == snap):,.1f} MVAr "
                  f"(TSEP {cap_tot[snap]:,})")
    s2_load = sum(r["pd_summer_peak"] for r in rows) / (totals["summer_peak"] + L8["ke_export"]["summer_peak"]["mw"])
    Lx += ["\n## S2 (signed-off denominators)\n",
           f"- Load in the main component: **{100 * s2_load:.1f}%** (all load is placed on main-component buses by construction; a DISCO group with no load station would count as missing)",
           f"- Installed generation in the main component: **{100 * gen_in / gen_den:.1f}%** ({gen_in:,.0f} of {gen_den:,.0f} MW; the 5 excluded small hydro plants count as missing)",
           f"- **S2 {'PASS' if s2_load >= 0.98 and gen_in / gen_den >= 0.98 else 'FAIL'}** (≥ 98% each)\n",
           "## DISCO groups\n", "| group | TSEP MW (2026-27) | load stations | summer MW | MW per station | 66 kV stations | median anchor km |", "|---|---|---|---|---|---|---|"]
    for g in sorted(groups, key=lambda k: -groups[k]):
        ss = [s for s in stations if s["group"] == g]
        mw = sum(r["pd_summer_peak"] for r in rows if r["group"] == g)
        ak = sorted(s["anchor_km"] for s in ss)
        Lx.append(f"| {g} | {groups[g]:,.0f} | {len(ss)} | {mw:,.0f} | {mw / len(ss) if ss else 0:,.1f} | {sum(1 for s in ss if s['kv'] == '66')} | {ak[len(ak) // 2] if ak else '—'} |")
    Lx += [f"\n- Load stations: {len(stations)}; excluded: {dict(excluded)}; anchors: {len(anchors)} PSS-labelled NTDC stations",
           f"- KE export buses: {len(kw)} ({', '.join(sorted(kw))})", "\n## FESCO / MEPCO station matching\n"]
    for d, a, ref, nm, mw in match_log:
        if a.startswith("SUMMARY"):
            Lx.append(f"- **{d}**: {a[9:]}")
    Lx.append("\n| DISCO | table station | model station | OSM name | MW 2026-27 |\n|---|---|---|---|---|")
    for d, a, ref, nm, mw in match_log:
        if not a.startswith("SUMMARY"):
            Lx.append(f"| {d} | {a} | {ref} | {nm} | {mw} |")
    (build_dir / "params" / "loads_summary.md").write_text("\n".join(Lx) + "\n", encoding="utf-8")
    print("\n".join(Lx[:30]))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "osm" / "build" / "explicit")
