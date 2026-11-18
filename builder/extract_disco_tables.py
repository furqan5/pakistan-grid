"""Extract FESCO and MEPCO substation maximum-demand tables (base forecast) to CSV, 2026-27 column.

FESCO Demand Forecast 2023-33, Table 1-22 (PDF pp.49-58); MEPCO PMS Load Forecast 2021-22, 'Maximum Demand (MW) of
Substations - Base Forecast' (PDF pp.64-73). Text via xpdf `pdftotext -table`.
Writes sources/extracted/{fesco,mepco}_station_md.csv.
"""
import csv
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = {"fesco": ("fesco_demand_forecast_2023-33.pdf", 49, 58, "Family of Grids"),
       "mepco": ("mepco_pms_load_forecast_2021-22.pdf", 64, 73, "Family of Grids")}
YEAR = re.compile(r"20\d\d-\d\d")
ROW = re.compile(r"^\s*(\d+)\s+(\d+)\s+(.+?)\s+(220|132|66|33|11)\s+((?:-?[\d.]+\s+){5,}-?[\d.]+)\s*$")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for disco, (fn, a, b, stop) in SRC.items():
        txt = subprocess.run(["pdftotext", "-table", "-f", str(a), "-l", str(b), str(ROOT / "sources" / fn), "-"],
                             capture_output=True, check=True).stdout.decode("utf-8", errors="replace").splitlines()
        years, rows, skipped = None, [], 0
        for line in txt:
            if stop in line:
                break
            ys = YEAR.findall(line)
            if len(ys) >= 6:
                years = ys
                continue
            m = ROW.match(line)
            if m and years:
                vals = m.group(5).split()
                if len(vals) != len(years):
                    skipped += 1
                    continue
                rec = dict(zip(years, (float(v) for v in vals)))
                rows.append({"disco": disco.upper(), "sno": int(m.group(1)), "grid_no": int(m.group(2)),
                             "name": re.sub(r"\s+", " ", m.group(3)).strip(), "kv": int(m.group(4)), "mw_2026_27": rec.get("2026-27")})
        with open(ROOT / "sources" / "extracted" / f"{disco}_station_md.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        tot = sum(r["mw_2026_27"] or 0 for r in rows)
        print(f"{disco.upper()}: {len(rows)} stations, sum of 2026-27 station MD {tot:,.0f} MW, last S.No {rows[-1]['sno']}, rows skipped {skipped}")


if __name__ == "__main__":
    main()
