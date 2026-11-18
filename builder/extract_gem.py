"""Pakistan rows of the GEM hydro, wind, solar and bioenergy trackers -> sources/extracted/gem_pk.csv.
Source: sources/gem/gem-data.zip (Global Energy Monitor, CC BY 4.0; SHA-256 in logs/downloads.tsv).
Needs openpyxl (system Python). Usage: python -I builder/extract_gem.py"""
import csv, pathlib, sys
import openpyxl
ROOT = pathlib.Path(__file__).resolve().parents[1]
D = ROOT / "sources" / "gem" / "extracted"
FILES = {"hydro": ("Global-Hydropower-Tracker-March-2026.xlsx", ["Data", "Below Threshold"], "Country/Area 1"),
         "wind": ("Global-Wind-Power-Tracker-February-2026.xlsx", ["Data", "Below Threshold"], "Country/Area"),
         "solar": ("Global-Solar-Power-Tracker-February-2026.xlsx", ["Utility-Scale (1 MW+)"], "Country/Area"),
         "bioenergy": ("Global Bioenergy Power Tracker (GBPT) - v4.xlsx", ["Data"], "Country/Area")}
out = []
for tech, (fn, sheets, ckey) in FILES.items():
    wb = openpyxl.load_workbook(D / fn, read_only=True)
    for sn in sheets:
        it = wb[sn].iter_rows(values_only=True)
        hdr = list(next(it))
        ix = {h: i for i, h in enumerate(hdr) if h}
        def g(row, *keys):
            for k in keys:
                if k in ix and row[ix[k]] not in (None, ""):
                    return row[ix[k]]
            return ""
        for row in it:
            if g(row, ckey) != "Pakistan":
                continue
            out.append({"tech": tech, "sheet": sn, "name": g(row, "Project Name"), "unit": g(row, "Phase Name", "Unit Name"),
                        "other_names": g(row, "Other name(s)", "Other Name(s)"), "capacity_mw": g(row, "Capacity (MW)"),
                        "status": g(row, "Status"), "lat": g(row, "Latitude"), "lon": g(row, "Longitude"),
                        "accuracy": g(row, "Location Accuracy", "Location accuracy"), "owner": g(row, "Owner", "Owner(s)"),
                        "operator": g(row, "Operator", "Operator(s)"), "gem_id": g(row, "GEM location ID", "GEM phase ID", "GEM unit/phase ID", "GEM location ID")})
with open(ROOT / "sources" / "extracted" / "gem_pk.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
sys.stdout.reconfigure(encoding="utf-8")
import collections
print(collections.Counter((o["tech"], o["status"]) for o in out))
