"""Extract the 500/220 kV line and grid-station tables from NTDC Power System Statistics, 44th edition.

Source: sources/ntdc_pss_44th_2020.pdf (SHA-256 24235bdc..., see SOURCES.md). Data to 30 June 2019.
Text comes from xpdf `pdftotext -table` (the -layout mode scrambles the columns of these tables).

Writes sources/extracted/pss44_*.csv and prints a check of row sums against the printed subtotals.
Usage: python builder/extract_pss44.py [path/to/pdf]
"""
import csv
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PDF = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "sources" / "ntdc_pss_44th_2020.pdf"
OUT = ROOT / "sources" / "extracted"

# PDF page numbers (the printed "Page N of 80" numbers are 14 lower).
PAGES = {"lines_500": (58, 59), "lines_220": (60, 62), "gs_500": (69, 69), "gs_220": (70, 71)}

DATE = r"(?:[A-Z][a-z]+-\d{2,4})"
NUM = r"([\d,]+)"
LINE_ROW = re.compile(rf"^\s*(\d+)\s+(.*?)\s+(?:({DATE})\s+)?{NUM}\s+{NUM}\s+{NUM}\s*$")
REGION = re.compile(r"^\s*([A-Za-z/ ]+?)\s+Region\s*$")
SUBTOTAL = re.compile(r"^\s*(?:Sub\s*-?\s*Total|Total)\s+(.*?)\s+(?:{n}\s+{n}\s+)?{n}\s*$".format(n=r"([\d,]+)"))

DISCO = r"(K Electric|[A-Z]{4,5}/?[A-Z]*)"
PROV = r"(/?Punjab|KPK|Sindh|Balochistan|Islamabad)"
GS500_ROW = re.compile(rf"^\s*(\d+)\s+(.*?)\s+{DISCO}\s+{PROV}" + r"\s+(\d+)\s+([\d,]+)" * 3 + r"\s+([\d,]+)\s*$")
GS220_ROW = re.compile(rf"^\s*(\d+)\s+(.*?)\s+{DISCO}\s+{PROV}" + r"\s+(\d+)\s+([\d,]+)" * 2 + r"\s+(\d+)\s+([\d,]+)\s*$")

# Defects found by reading the booklet; see day5/pss_check.md.
DUPLICATE_220_SECTION = "Hyderabad/Quetta"
DUPLICATE_NOTE = "source defect: rows are a copy of the 500 kV Hyderabad table (Table 2.6, printed p.45); not 220 kV data"


def n(s):
    return int(s.replace(",", "")) if s else None


def page_text(first, last):
    out = subprocess.run(["pdftotext", "-table", "-f", str(first), "-l", str(last), str(PDF), "-"],
                         capture_output=True, check=True)
    return out.stdout.decode("utf-8", errors="replace").splitlines()


def parse_lines(kind, kv):
    rows, region, checks = [], None, []
    for raw in page_text(*PAGES[kind]):
        line = raw.rstrip()
        if not line.strip():
            continue
        if "Hyderabad/Quetta Region" in line or (kv == 220 and region == "Lahore" and line.strip().startswith("Hyderabad/Quetta")):
            region = DUPLICATE_220_SECTION
            continue
        m = REGION.match(line)
        if m and not LINE_ROW.match(line):
            region = m.group(1).strip()
            continue
        if re.match(r"^\s*Table\s+2\.[79]\b", line):  # regional summary tables follow; not line rows
            break
        if re.search(r"Total\s+(?:Route\s+)?Length", line):  # repeats the subtotal above it
            continue
        m = SUBTOTAL.match(line)
        if m:
            sc, dc, tot = n(m.group(2)), n(m.group(3)), n(m.group(4))
            got = sum(r["circuit_km"] for r in rows if r["region"] == region)
            checks.append((kv, region, tot, got, sc, dc))
            continue
        m = LINE_ROW.match(line)
        if m:
            sr, name, date, sc, dc, tot = m.groups()
            rows.append({
                "kv": kv, "region": region, "sr": int(sr), "name": re.sub(r"\s+", " ", name.replace("�", "-")).strip(),
                "commissioned": date or "", "sc_route_km": n(sc), "dc_route_km": n(dc), "circuit_km": n(tot),
                "usable": "no" if region == DUPLICATE_220_SECTION else "yes",
                "note": DUPLICATE_NOTE if region == DUPLICATE_220_SECTION else "",
            })
    return rows, checks


def parse_gs(kind, kv):
    rows, region = [], None
    pat = GS500_ROW if kv == 500 else GS220_ROW
    for raw in page_text(*PAGES[kind]):
        line = raw.rstrip()
        s = line.strip()
        if not s:
            continue
        m = re.match(r"^(?:Lahore|Islamabad|Multan|Hyderabad|Hyedrabad|Quetta)\s+Region$", s)
        if m:
            region = s.replace(" Region", "").replace("Hyedrabad", "Hyderabad")
            continue
        m = pat.match(line)
        if m:
            g = m.groups()
            if kv == 500:
                sr, name, disco, prov, n1, c1, n2, c2, n3, c3, total = g
                tx = [(n(n1), n(c1)), (n(n2), n(c2)), (n(n3), n(c3))]
            else:
                sr, name, disco, prov, n1, c1, n2, c2, ntot, total = g
                tx = [(n(n1), n(c1)), (n(n2), n(c2))]
            rows.append({"kv": kv, "region": region, "sr": int(sr), "name": re.sub(r"\s+", " ", name).strip(),
                         "disco": disco, "province": prov.lstrip("/"),
                         "transformers": " + ".join(f"{k}x{c}" for k, c in tx if k),
                         "total_mva": n(total), "check_mva": sum(k * c for k, c in tx if k)})
            continue
        # Continuation lines: a wrapped DISCO ("TESCO", "CO", "SEPCO") or a wrapped name ("(NKI)", "Lahore", "GIS)").
        if rows and re.fullmatch(r"[A-Za-z()]+\)?", s) and s != "(MVA)" \
                and not s.startswith(("Sr", "No", "Name", "Page", "Transmission", "Table", "NTDC")):
            if re.fullmatch(r"[A-Z]+", s) and s not in ("GIS",):
                rows[-1]["disco"] += s
            else:
                rows[-1]["name"] += " " + s
    return rows


def write(name, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    l500, c500 = parse_lines("lines_500", 500)
    l220, c220 = parse_lines("lines_220", 220)
    g500 = parse_gs("gs_500", 500)
    g220 = parse_gs("gs_220", 220)
    write("pss44_lines_500kv.csv", l500)
    write("pss44_lines_220kv.csv", l220)
    write("pss44_gs_500kv.csv", g500)
    write("pss44_gs_220kv.csv", g220)

    print(f"500 kV lines: {len(l500)} rows; 220 kV lines: {len(l220)} rows "
          f"({sum(r['usable'] == 'no' for r in l220)} flagged unusable)")
    print(f"500 kV grid stations: {len(g500)}; 220 kV grid stations: {len(g220)}")
    print("\nRegion subtotal checks (printed total vs sum of rows, circuit-km):")
    for kv, region, tot, got, sc, dc in c500 + c220:
        print(f"  {kv} kV {region:<18} printed {tot:>6,}  rows {got:>6,}  diff {got - tot:+d}")
    for kv, rows in ((500, l500), (220, l220)):
        ok = sum(r["circuit_km"] for r in rows if r["usable"] == "yes")
        print(f"  {kv} kV usable rows total: {ok:,} circuit-km")
        # 500 kV rows are one circuit each (SC + DC route km); 220 kV "1 & 2" rows hold two circuits (2 x DC).
        bad = [r for r in rows if abs(r["sc_route_km"] + r["dc_route_km"] - r["circuit_km"]) > 1
               and abs(r["sc_route_km"] + 2 * r["dc_route_km"] - r["circuit_km"]) > 1]
        for r in bad:
            print(f"    row arithmetic differs: {r['region']} {r['sr']} {r['name']}: "
                  f"SC {r['sc_route_km']} + DC {r['dc_route_km']} vs {r['circuit_km']}")
    print("\nStation MVA checks (sum of transformer rows vs printed total):")
    for r in g500 + g220:
        if r["check_mva"] != r["total_mva"]:
            print(f"  {r['kv']} kV {r['name']}: rows {r['check_mva']} vs printed {r['total_mva']}")
    print(f"  500 kV printed total 24,410; rows {sum(r['total_mva'] for r in g500):,}")
    print(f"  220 kV printed Sub Total (A) 24,930; rows {sum(r['total_mva'] for r in g220):,}")


if __name__ == "__main__":
    main()
