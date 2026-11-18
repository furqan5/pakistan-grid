"""Extract IGCEP 2025-35 R2 Annex B-1(i) (NGC existing plants) and B-2 (thermal cost data) to CSV.

Source: sources/igcep_2025-35_r2.pdf (SHA-256 in logs/downloads.tsv). Text via xpdf `pdftotext -table`.
Writes sources/extracted/igcep_b1_ngc.csv and igcep_b2_costs.csv, and checks section subtotals.
"""
import csv
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PDF = ROOT / "sources" / "igcep_2025-35_r2.pdf"
OUT = ROOT / "sources" / "extracted"


def text(first, last):
    r = subprocess.run(["pdftotext", "-table", "-f", str(first), "-l", str(last), str(PDF), "-"], capture_output=True, check=True)
    return r.stdout.decode("utf-8", errors="replace").splitlines()


def num(s):
    return float(s.replace(",", ""))


def b1():
    rows, section, checks = [], None, []
    row_re = re.compile(r"^\s*(\d+)\s+(.+?)\s{2,}(Hydro|Gas|RLNG|Nuclear|RFO|Imp\. Coal|Local Coal|Bagasse|Wind|Solar PV|HSD)\s+([\d,.]+)\s+([\d,.]+)\s*$")
    for line in text(149, 153):
        if "B-1 (ii)" in line or "B-1  (ii)" in line or "K-Electric System" in line:
            break
        s = line.strip()
        m = row_re.match(line)
        if m:
            sr, name, fuel, inst, dep = m.groups()
            rows.append({"sr": int(sr), "name": re.sub(r"\s+", " ", name).strip(), "fuel": fuel, "section": section,
                         "installed_mw": num(inst), "dependable_mw": num(dep)})
            continue
        m = re.match(r"^(Sub\s*Total.*?|Total.*?)\s{2,}([\d,.]+)\s+([\d,.]+)\s*$", s)
        if m:
            checks.append((m.group(1).strip(), num(m.group(2)), num(m.group(3))))
            continue
        m = re.match(r"^(Import from Iran)\s+([\d,.]+)\s+([\d,.]+)$", s)
        if m:
            rows.append({"sr": 0, "name": "Import from Iran", "fuel": "Import", "section": "Import",
                         "installed_mw": num(m.group(2)), "dependable_mw": num(m.group(3))})
            continue
        if s and not re.search(r"\d", s) and len(s) < 40 and not s.startswith(("Name", "Sr", "Project", "(MW)", "Annex")):
            section = s
    return rows, checks


def b2():
    rows = []
    row_re = re.compile(r"^\s*(\d+)\s+(.+?)\s{2,}(\S+(?:\s\S+)?)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$")
    stop = False
    for line in text(154, 156):
        if re.search(r"Committed|Candidate", line) and rows:
            stop = True
        if stop:
            break
        m = row_re.match(line)
        if m:
            sr, name, cat, fom, vom, fuel, hr = m.groups()
            rows.append({"sr": int(sr), "name": re.sub(r"\s+", " ", name).strip(), "category": cat, "fixed_om_usd_kw_yr": float(fom),
                         "vom_usd_mwh": float(vom), "fuel_usd_gj": float(fuel), "heat_rate_gj_mwh": float(hr),
                         "c1_usd_mwh": round(float(fuel) * float(hr) + float(vom), 3)})
    return rows


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    r1, checks = b1()
    r2 = b2()
    for name, rows in (("igcep_b1_ngc.csv", r1), ("igcep_b2_costs.csv", r2)):
        with open(OUT / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    inst = sum(r["installed_mw"] for r in r1)
    dep = sum(r["dependable_mw"] for r in r1)
    print(f"B-1(i): {len(r1)} rows, installed {inst:,.1f} MW, dependable {dep:,.1f} MW (printed total 36,424 / 33,747)")
    by = {}
    for r in r1:
        by.setdefault(r["fuel"], [0, 0])
        by[r["fuel"]][0] += r["installed_mw"]
        by[r["fuel"]][1] += r["dependable_mw"]
    for k, v in sorted(by.items(), key=lambda x: -x[1][0]):
        print(f"   {k:<11} installed {v[0]:>9,.1f}  dependable {v[1]:>9,.1f}")
    print("Printed subtotals:", "; ".join(f"{a} {b:,.0f}/{c:,.0f}" for a, b, c in checks))
    print(f"B-2 existing: {len(r2)} rows")


if __name__ == "__main__":
    main()
