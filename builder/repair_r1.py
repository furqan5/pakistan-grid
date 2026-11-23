"""Repair round 1 (post hoc), declared in builder/parameters.json["repair_r1"] and day9/repair_r1_rules.md.

Reads the as-specified parameter tables in <build>/params/ and writes repaired copies to <build>/params_r1/;
the originals are left untouched.
  RP1  name containment: a branch named "X (parent line)" adopts the higher circuit count of the adjacent
       same-voltage branch whose full name it contains (OSM naming convention).
  RP2  three 220 kV lines from PSS 44th whose OSM path is more than 2x the PSS route (and not 'too far') are added
       as synthetic double-circuit branches at the PSS route length.
  RP3  reactors: TSEP totals kept; Table 5-9 fixed reactors kept; the pool goes to 500 and 220 kV station buses in
       proportion to local half-charging of incident 500/220 kV circuits; each bus is capped at its local
       half-charging (fixed reactor included); any excess is left unplaced and logged.
Usage:  python builder/repair_r1.py [build_dir] [--list]   (--list only writes the RP1/RP2 listing)
"""
import collections
import csv
import json
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from make_parameters import line_pu  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAR = json.loads((ROOT / "builder" / "parameters.json").read_text(encoding="utf-8"))
SB = PAR["base_mva"]
RP2_ROWS = [("220", "Lahore", "9"), ("220", "Lahore", "20"), ("220", "Lahore", "40")]  # PSS 44th 220 kV rows (region, sr)


def rd(p):
    return list(csv.DictReader(open(p, encoding="utf-8")))


def rp1_spans(build_dir):
    """RP1 (name containment): a branch adopts the circuit count of an adjacent same-voltage branch sharing a junction end
    when the branch's normalised OSM name contains the adjacent branch's full normalised name (OSM's 'X (parent line)'
    convention) and the adjacent count is higher."""
    from score_s3 import words
    norm = lambda n: " ".join(words(n.replace("–", " ")))
    br = rd(build_dir / "branches.csv")
    inc = collections.defaultdict(list)
    for i, r in enumerate(br):
        inc[r["from"]].append(i)
        inc[r["to"]].append(i)
    out = []
    for i, r in enumerate(br):
        if not r["name"].strip():
            continue
        ni, best = norm(r["name"]), None
        for e in (r["from"], r["to"]):
            if not e.startswith("J:"):
                continue
            for j in inc[e]:
                s = br[j]
                if j == i or s["kv"] != r["kv"] or not s["name"].strip() or int(s["circuits"]) <= int(r["circuits"]):
                    continue
                ns = norm(s["name"])
                if ns and ns != ni and ns in ni and (best is None or int(s["circuits"]) > int(best["circuits"])):
                    best = s
        if best:
            out.append({"idx": i, "kv": r["kv"], "from": r["from"], "to": r["to"], "len_km": float(r["len_km"]), "circuits": int(r["circuits"]),
                        "new_circuits": int(best["circuits"]), "name": r["name"], "ways": r["ways"],
                        "others": {"parent": [f"{best['circuits']}c '{best['name'][:40]}'"]}})
    return out


def rp2_rows(build_dir):
    chk = {(r["kv"], r["region"], r["sr"]): r for r in rd(build_dir / "pss_line_check.csv")}
    return [chk[k] for k in RP2_ROWS]


def main(build_dir, list_only):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    spans = rp1_spans(build_dir)
    adds = rp2_rows(build_dir)
    if list_only:
        L = ["# Repair round 1: RP1 and RP2 listing (names and end buses only; written before any repaired solve)\n",
             f"## RP1: {len(spans)} branches (name containment), {sum(s['len_km'] for s in spans):.1f} km\n",
             "| # | kV | km | circuits now -> after | from | to | OSM name | other same-kV branches at the two ends |", "|---|---|---|---|---|---|---|---|"]
        for n, s in enumerate(sorted(spans, key=lambda s: (s["kv"], -s["len_km"])), 1):
            oth = " ; ".join(f"{e.split('@')[0][-12:]}: " + ", ".join(v) for e, v in s["others"].items())
            L.append(f"| {n} | {s['kv']} | {s['len_km']:.2f} | {s['circuits']} -> {s['new_circuits']} | {s['from']} | {s['to']} | {s['name'][:50] or '(unnamed)'} | {oth} |")
        L += ["\n## RP2: three PSS 44th 220 kV lines added\n", "| PSS row | line | route km (PSS) | straight km | OSM path km | ratio | buses |", "|---|---|---|---|---|---|---|"]
        for r in adds:
            L.append(f"| {r['region']} {r['sr']} | {r['pss_name']} | {r['route_km']} | {r['straight_km']} | {r['path_km']} | {r['path_ratio']} | {r['bus_a']} – {r['bus_b']} |")
        (ROOT / "day9" / "repair_r1_listing.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L[:3]), f"\n... {len(spans)} RP1 spans; RP2 rows: {[r['pss_name'] for r in adds]}")
        return

    src, dst = build_dir / "params", build_dir / "params_r1"
    dst.mkdir(exist_ok=True)
    for f in ("transformer_params.csv", "generators.csv", "loads.csv", "capacitors.csv", "dcline.json"):
        shutil.copy(src / f, dst / f)
    LP = PAR["lines"]
    rows = rd(src / "branch_params.csv")
    by_idx = {int(r["idx"]): r for r in rows}
    cls_of = lambda kv: LP["classes"][LP["voltage_class_map"][kv]]
    changed = []
    for s in spans:
        r = by_idx[s["idx"]]
        n = s["new_circuits"]
        rr, xx, bh = line_pu(cls_of(r["kv"]), float(r["kv"]), float(r["length_km"]), n)
        rate = cls_of(r["kv"])["rate_a_mva"] * n / SB
        r.update(circuits=n, br_r=rr, br_x=xx, b_fr=bh, b_to=bh, rate_a=rate, rate_b=rate * LP["rate_b_factor"], rate_c=rate * LP["rate_c_factor"],
                 ways=r["ways"] + " [RP1]")
        changed.append(s)
    nxt = 100000
    for a in adds:
        kv, n, length = "220", 2, float(a["route_km"])
        rr, xx, bh = line_pu(cls_of(kv), 220.0, length, n)
        rate = cls_of(kv)["rate_a_mva"] * n / SB
        rows.append({"idx": nxt, "f_bus": a["bus_a"], "t_bus": a["bus_b"], "kv": kv, "class": "220", "circuits": n, "length_km": length,
                     "br_r": rr, "br_x": xx, "g_fr": 0.0, "g_to": 0.0, "b_fr": bh, "b_to": bh, "rate_a": rate, "rate_b": rate * LP["rate_b_factor"],
                     "rate_c": rate * LP["rate_c_factor"], "angmin": rows[0]["angmin"], "angmax": rows[0]["angmax"], "transformer": False,
                     "ways": "RP2 synthetic from PSS 44th", "name": f"RP2: {a['pss_name']} (PSS 44th, {a['region']} {a['sr']})"})
        nxt += 1
    with open(dst / "branch_params.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # RP3 reactors
    B = {b["bus"]: b for b in rd(build_dir / "buses.csv")}
    cap = collections.defaultdict(float)
    for r in rows:
        if r["kv"] not in ("500", "220"):
            continue
        for e in (r["f_bus"], r["t_bus"]):
            x = B[e]
            if x["kind"] in "SP" and x["prov"] in ("substation", "plant", "converter") and x["in_main"] == "1":
                cap[e] += float(r["b_fr"]) * SB
    old = rd(src / "reactors.csv")
    fixed = [r for r in old if r["source"].startswith("TSEP T5-9")]
    totals = PAR["shunts"]["reactor_total_mvar"]
    new, log = [], []
    for snap, total in totals.items():
        fx = [r for r in fixed if r["snapshot"] == snap]
        fixed_at = collections.defaultdict(float)
        for r in fx:
            fixed_at[r["bus"]] += float(r["mvar_nameplate"])
            new.append(r)
        pool = total - sum(fixed_at.values())
        wsum = sum(cap.values())
        placed = 0.0
        for bus, c in sorted(cap.items()):
            share = pool * c / wsum
            room = max(0.0, c - fixed_at.get(bus, 0.0))
            m = min(share, room)
            placed += m
            new.append({"snapshot": snap, "bus": bus, "mvar_nameplate": round(m, 3), "bs_pu": -m / SB,
                        "source": "RP3 pool: share of local half-charging, capped at local half-charging"})
        log.append((snap, total, sum(fixed_at.values()), pool, placed, pool - placed, sum(cap.values())))
    with open(dst / "reactors.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["snapshot", "bus", "mvar_nameplate", "bs_pu", "source"])
        w.writeheader()
        w.writerows(new)

    ch = collections.defaultdict(float)
    for r in rows:
        ch[r["kv"]] += 2 * float(r["b_fr"]) * SB * 0 + float(r["length_km"]) * float(r["circuits"])
    L = ["# Repair round 1 (post hoc): applied\n", f"- RP1: {len(changed)} spans raised ({sum(s['len_km'] for s in changed):.1f} km)",
         f"- RP2: {len(adds)} synthetic 220 kV double-circuit lines added ({sum(float(a['route_km']) for a in adds):.0f} route km)",
         "- RP3 reactors (nameplate at 1.0 pu):"]
    for snap, total, fx, pool, placed, unplaced, capsum in log:
        L.append(f"  - {snap}: TSEP total {total:,}; fixed {fx:,.0f}; pool {pool:,.0f}; placed {placed:,.0f} (cap sum {capsum:,.0f}); "
                 f"**unplaced {unplaced:,.0f}**; reactors in model {fx + placed:,.0f} MVAr")
    L.append("- S4 after repair (circuit-km): " + ", ".join(f"{kv} kV {ch[kv]:,.0f}" for kv in ("500", "220")))
    (dst / "repair_summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(pathlib.Path(args[0]) if args else ROOT / "osm" / "build" / "explicit", "--list" in sys.argv)
