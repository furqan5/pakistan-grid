"""Day 7: build the generator table from IGCEP B-1(i)/B-2 and day7/plant_crosswalk.csv, under the rules in
builder/parameters.json["generators"] (commit 42c7533, pushed before this ran).
Writes <build>/params/generators.csv and generators_summary.md.
Usage: python builder/make_generators.py [build_dir]
"""
import collections
import csv
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAR = json.loads((ROOT / "builder" / "parameters.json").read_text(encoding="utf-8"))
G = PAR["generators"]
SB = PAR["base_mva"]
FUEL = {"Hydro": "hydro", "Gas": "ccgt", "RLNG": "ccgt", "Nuclear": "nuclear", "RFO": "engine_rfo_gt", "Imp. Coal": "coal",
        "Local Coal": "coal", "Bagasse": "bagasse", "Wind": "wind", "Solar PV": "solar", "Import": "import"}
SYNC = {"hydro", "ccgt", "nuclear", "engine_rfo_gt", "coal", "bagasse"}


def hav(a, b, c, d):
    p1, p2 = math.radians(a), math.radians(c)
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(d - b) / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(h))


def main(build_dir):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ext = ROOT / "sources" / "extracted"
    b1 = list(csv.DictReader(open(ext / "igcep_b1_ngc.csv", encoding="utf-8")))
    b2 = {r["name"]: float(r["c1_usd_mwh"]) for r in csv.DictReader(open(ext / "igcep_b2_costs.csv", encoding="utf-8"))}
    cw = {int(r["sr"]): r for r in csv.DictReader(open(ROOT / "day7" / "plant_crosswalk.csv", encoding="utf-8"))}
    S = {r["id"]: r for r in csv.DictReader(open(build_dir / "stations.csv", encoding="utf-8"))}
    P = {r["id"]: r for r in csv.DictReader(open(build_dir / "plants.csv", encoding="utf-8"))}
    B = list(csv.DictReader(open(build_dir / "buses.csv", encoding="utf-8")))
    cand = [b for b in B if b["in_main"] == "1" and b["kind"] in "SP" and b["prov"] in ("substation", "plant", "converter")]
    con = G["connection"]

    rows, flags = [], []
    for r in b1:
        sr = int(r["sr"])
        c = cw[sr]
        fuel = FUEL[r["fuel"]]
        dep = float(r["dependable_mw"])
        inst = float(r["installed_mw"])
        out = {"sr": sr, "name": r["name"], "fuel": fuel, "installed_mw": inst, "dependable_mw": dep, "location": c["location"],
               "doc_kv": c["doc_kv"], "bus": "", "bus_kv": "", "dist_km": "", "how": "", "status": 1, "basis": c["basis"]}
        if fuel == "import":
            out.update(status=0, how="excluded: Makran/Gwadar off-grid")
            rows.append(out)
            continue
        if dep == 0:
            out.update(status=0, how="excluded: dependable 0 MW")
        if not c["location"]:
            out.update(how="UNLOCATED", status=0)
            rows.append(out)
            continue
        kind, ref = c["location"].split(":")
        src = S[ref] if kind == "S" else P[ref]
        la, lo = float(src["lat"]), float(src["lon"])
        dists = [(hav(la, lo, float(b["lat"]), float(b["lon"])), b) for b in cand]
        bus = None
        if c["doc_kv"]:
            kv = c["doc_kv"]
            own = [b for b in cand if b["kind"] == kind and b["ref"] == ref and b["kv"] == kv]
            if own:
                bus, d, how = own[0], 0.0, f"documented {kv} kV, own bus"
            else:
                near = sorted((d, b) for d, b in dists if b["kv"] == kv and d <= 20)
                if near:
                    d, bus = near[0]
                    how = f"crosswalk voltage {kv} kV (see basis), nearest {kv} kV bus"
                else:
                    flags.append(f"{r['name']}: no {kv} kV bus within 20 km; general rule used")
        if bus is None:
            min_kv = 66 if dep < 50 else 132
            within = [(d, b) for d, b in dists if d <= 5 and int(b["kv"]) >= min_kv]
            if within:
                top = max(int(b["kv"]) for _, b in within)
                d, bus = min(((d, b) for d, b in within if int(b["kv"]) == top), key=lambda x: x[0])
                how = "highest kV within 5 km"
            else:
                near = sorted(((d, b) for d, b in dists if d <= 20 and int(b["kv"]) >= 66), key=lambda x: x[0])
                if near:
                    d, bus = near[0]
                    how = "nearest bus within 20 km"
        if bus is None:
            out.update(how="no bus within 20 km", status=0)
            rows.append(out)
            continue
        out.update(bus=bus["bus"], bus_kv=bus["kv"], dist_km=round(d, 2), how=how if out["status"] else out["how"] + "; " + how)
        kvb = int(bus["kv"])
        if dep >= 1000 and kvb != 500:
            flags.append(f"SIZE: {r['name']} {dep:.0f} MW at {kvb} kV")
        elif dep >= 500 and kvb < 220:
            flags.append(f"SIZE: {r['name']} {dep:.0f} MW at {kvb} kV")
        rows.append(out)

    # ---- snapshot values
    pm = G["pmax"]
    for o in rows:
        f, dep = o["fuel"], o["dependable_mw"]
        s = pm["summer_peak"].get(f, 1.0) if f in ("solar", "bagasse", "wind") else 1.0
        w = pm["winter_offpeak"].get(f, pm["winter_offpeak"]["other"])
        o["pmax_summer"] = round(dep * s, 3) if o["status"] else 0.0
        o["pmax_winter"] = round(dep * w, 3) if o["status"] else 0.0
        o["pmin_frac"] = G["pmin_fraction"].get(f, 0.0)
        pf = G["reactive"]["pf"].get(f, 0.85)
        o["q_per_p"] = math.tan(math.acos(pf))
        o["qmin_factor"] = G["reactive"]["qmin_synchronous"] if f in SYNC else -1.0
        b2n = cw[o["sr"]]["b2_name"]
        if b2n and b2n in b2:
            o["c1_usd_mwh"], o["cost_src"] = b2[b2n], f"IGCEP B-2 {b2n}"
        else:
            o["c1_usd_mwh"], o["cost_src"] = G["cost"]["c1_fallback_usd_mwh"].get(f, 0), "fallback table"
        for snap in ("summer", "winter"):
            pmax = o[f"pmax_{snap}"]
            o[f"qmax_{snap}"] = round(pmax * o["q_per_p"], 3)
            o[f"qmin_{snap}"] = round(o["qmin_factor"] * pmax * o["q_per_p"], 3)
            o[f"pmin_{snap}"] = round(pmax * o["pmin_frac"], 3)

    cols = ["sr", "name", "fuel", "installed_mw", "dependable_mw", "status", "location", "doc_kv", "bus", "bus_kv", "dist_km", "how",
            "pmax_summer", "pmin_summer", "qmax_summer", "qmin_summer", "pmax_winter", "pmin_winter", "qmax_winter", "qmin_winter",
            "c1_usd_mwh", "cost_src", "basis"]
    with open(build_dir / "params" / "generators.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(rows)

    # ---- checks
    on = [o for o in rows if o["status"] == 1]
    excl_import = sum(o["installed_mw"] for o in rows if o["fuel"] == "import")
    excl_zero = sum(o["installed_mw"] for o in rows if o["dependable_mw"] == 0)
    unloc = [o for o in rows if o["how"].startswith("UNLOCATED") or o["how"].startswith("no bus")]
    ref_inst = 36424 - excl_import - excl_zero
    inst_model = sum(o["installed_mw"] for o in on)
    req_s = 27097 + 2050 + 1033 + 4000 * PAR["dcline"]["loss1"]
    req_w = 8774 + 1001 + 207 + 2000 * PAR["dcline"]["loss1"]
    ps, pw = sum(o["pmax_summer"] for o in on), sum(o["pmax_winter"] for o in on)
    pmin_w = sum(o["pmin_winter"] for o in on)
    slack_s = next(o["bus"] for o in on if o["name"].startswith("Tarbela"))
    slack_w = max(on, key=lambda o: o["pmax_winter"])
    L = [f"# Day 7 generators ({build_dir.name} build)\n", "Rules: builder/parameters.json `generators` (commit 42c7533, pushed before this ran). Crosswalk: day7/plant_crosswalk.csv.\n",
         "## Exit checks\n",
         f"- (a) Installed MW in the model: **{inst_model:,.0f}** vs IGCEP NGC 36,424 less exclusions (Iran {excl_import:.0f}, dependable-0 {excl_zero:.0f}) = {ref_inst:,.0f} → {100 * (inst_model / ref_inst - 1):+.1f}% ({'within' if abs(inst_model / ref_inst - 1) <= 0.05 else 'OUTSIDE'} ±5%)",
         f"- (b) **Summer**: located Pmax {ps:,.0f} MW vs requirement {req_s:,.0f} MW (load 27,097 + KE 2,050 + TSEP losses 1,033 + dcline loss) → margin **{ps - req_s:,.0f} MW**",
         f"- Winter off-peak: located Pmax {pw:,.0f} MW vs requirement {req_w:,.0f} MW → margin {pw - req_w:,.0f} MW; sum of Pmin {pmin_w:,.0f} MW (must stay below the requirement)",
         f"- Unlocated plants (block Day 9): {len(unloc)}, dependable {sum(o['dependable_mw'] for o in unloc):,.0f} MW; summer Pmax they would add "
         f"{sum(o['dependable_mw'] * (G['pmax']['summer_peak'].get(o['fuel'], 1.0) if o['fuel'] in ('solar', 'bagasse', 'wind') else 1.0) for o in unloc):,.0f} MW",
         f"- Slack: summer {slack_s}; winter {slack_w['bus']} ({slack_w['name']}, {slack_w['pmax_winter']:.0f} MW)\n"]
    L += ["## By fuel (in model)\n", "| fuel | plants | dependable MW | summer Pmax | winter Pmax | c1 $/MWh range |", "|---|---|---|---|---|---|"]
    byf = collections.defaultdict(list)
    for o in on:
        byf[o["fuel"]].append(o)
    for f, os_ in sorted(byf.items(), key=lambda x: -sum(o["dependable_mw"] for o in x[1])):
        c1 = [o["c1_usd_mwh"] for o in os_]
        L.append(f"| {f} | {len(os_)} | {sum(o['dependable_mw'] for o in os_):,.0f} | {sum(o['pmax_summer'] for o in os_):,.0f} | {sum(o['pmax_winter'] for o in os_):,.0f} | {min(c1):.1f}–{max(c1):.1f} |")
    L += ["\n## By latitude band (in model)\n", "| band | summer Pmax MW | winter Pmax MW |", "|---|---|---|"]
    bus_lat = {b["bus"]: float(b["lat"]) for b in B}
    for name, lo, hi in (("north of 32°N", 32, 99), ("30–32°N", 30, 32), ("27–30°N", 27, 30), ("south of 27°N", 0, 27)):
        sel = [o for o in on if lo <= bus_lat[o["bus"]] < hi]
        L.append(f"| {name} | {sum(o['pmax_summer'] for o in sel):,.0f} | {sum(o['pmax_winter'] for o in sel):,.0f} |")
    L += ["\n## Connection\n", f"- By voltage: " + ", ".join(f"{kv} kV {sum(1 for o in on if o['bus_kv'] == kv)} plants / {sum(o['dependable_mw'] for o in on if o['bus_kv'] == kv):,.0f} MW" for kv in ("500", "220", "132", "66")),
          f"- Connection distance > 5 km: " + "; ".join(f"{o['name']} {o['dist_km']} km ({o['bus']})" for o in on if o["dist_km"] != "" and o["dist_km"] > 5) or "none",
          "- Flags: " + ("; ".join(flags) if flags else "none"),
          "\n## Unlocated (block Day 9 until placed)\n"]
    for o in unloc:
        L.append(f"- {o['name']} ({o['fuel']}, dependable {o['dependable_mw']:.0f} MW)")
    L += ["\n## Plants\n", "| sr | plant | fuel | dep MW | bus | how | dist km | c1 $/MWh |", "|---|---|---|---|---|---|---|---|"]
    for o in rows:
        L.append(f"| {o['sr']} | {o['name']} | {o['fuel']} | {o['dependable_mw']:.0f} | {o['bus'] or '—'} | {o['how']} | {o['dist_km']} | {o.get('c1_usd_mwh', '')} |")
    (build_dir / "params" / "generators_summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:40]))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "osm" / "build" / "explicit")
