"""Day 7: candidate OSM locations for each IGCEP B-1(i) plant, by distinctive-word name overlap. Review aid only;
the chosen location for each plant is recorded with its basis in day7/plant_crosswalk.csv."""
import csv, pathlib, sys, collections
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from score_s3 import words
ROOT = pathlib.Path(__file__).resolve().parents[1]
GENERIC = {"power", "wind", "solar", "energy", "ltd", "limited", "plant", "project", "hydro", "hydel", "the", "company", "pvt",
           "private", "station", "grid", "farm", "pv", "park", "1", "2", "3", "4", "kv", "220kv", "132kv", "500kv", "ipp", "thermal",
           "power station", "co", "and", "of", "electric", "generation", "unit", "units", "new", "green", "mills", "mil", "sugar"}
def distinct(name):
    return [w for w in words(name.replace("_", " ")) if w not in GENERIC and len(w) >= 3]
build = ROOT / "osm" / "build" / "explicit"
S = list(csv.DictReader(open(build / "stations.csv", encoding="utf-8")))
P = list(csv.DictReader(open(build / "plants.csv", encoding="utf-8")))
buses = collections.defaultdict(list)
for b in csv.DictReader(open(build / "buses.csv", encoding="utf-8")):
    if b["kind"] in "SP":
        buses[b["ref"]].append(b["kv"] + ("" if b["in_main"] == "1" else "x"))
cands = [("S", s["id"], s["all_names"], s["lat"], s["lon"]) for s in S if s["all_names"]] + \
        [("P", p["id"], p["all_names"], p["lat"], p["lon"]) for p in P if p["all_names"]]
cw = [(k, i, n, la, lo, set(w for nm in n.split(" | ") for w in words(nm))) for k, i, n, la, lo in cands]
out = []
for r in csv.DictReader(open(ROOT / "sources" / "extracted" / "igcep_b1_ngc.csv", encoding="utf-8")):
    d = distinct(r["name"])
    hits = []
    if d:
        for k, i, n, la, lo, ws in cw:
            sc = sum(1 for w in d if w in ws) / len(d)
            if sc >= 0.5:
                hits.append((sc, k, i, n[:60], la, lo))
    hits.sort(key=lambda h: (-h[0], h[1]))
    out.append({"sr": r["sr"], "name": r["name"], "fuel": r["fuel"], "dep_mw": r["dependable_mw"], "distinct": " ".join(d),
                "n_hits": len(hits), "top": " || ".join(f"{h[1]}:{h[2]} [{h[3]}] {float(h[4]):.3f},{float(h[5]):.3f} buses={buses.get(h[2], [])}" for h in hits[:3])})
with open(ROOT / "day7" / "plant_candidates.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for o in out:
    print(f"{o['sr']:>3} {o['name'][:24]:<24} {o['fuel'][:8]:<8} {float(o['dep_mw']):>7.0f} n={o['n_hits']:<3} {o['top'][:230]}")
