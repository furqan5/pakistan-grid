# Day 5 prep: NTDC Power System Statistics, 44th edition

Checked on 16 Nov 2026 against `sources/ntdc_pss_44th_2020.pdf`. The file is 94 pages, Distiller output dated 20 Mar 2020; its data runs to 30 June 2019. The SHA-256 is in `logs/downloads.tsv`.
It came from a **third-party mirror** (Energy Update), downloaded with Furqan's approval. There is no NTDC-hosted copy to compare the hash with. The title page and the publisher's layout match an NTDC Power System Planning booklet.

## Extraction

- `builder/extract_pss44.py` runs xpdf `pdftotext -table` and writes four files to `sources/extracted/`:

  | File | Source table | PDF pages | Printed pages | Rows |
  |---|---|---|---|---|
  | `pss44_lines_500kv.csv` | 2.6 | 58–59 | 44–45 | 50 |
  | `pss44_lines_220kv.csv` | 2.8 | 60–62 | 46–48 | 102 (14 flagged unusable) |
  | `pss44_gs_500kv.csv` | 2.16 | 69 | 55 | 16 |
  | `pss44_gs_220kv.csv` | 2.17 | 70–71 | 56–57 | 45 |

- `-layout` mode scrambles these tables: the columns slide by a row. Only `-table` mode is used.
- **Checks:**
  - Every regional subtotal matches the sum of its rows to within ±2 km. The rows are rounded.
  - Each station's transformer MVA sums exactly to its printed total: 500 kV 24,410 MVA and 220 kV 24,930 MVA.
  - PDF pages 61 and 69 were also checked by eye against the CSVs.
- **Row conventions:**
  - Each 500 kV row is one circuit, so circuit-km = single-circuit route km + double-circuit route km.
  - Most 220 kV rows named "1 & 2" hold two circuits, so circuit-km = 2 × double-circuit route km.

## Defects in the booklet (source defects, not parsing errors)

1. **The 220 kV "Hyderabad/Quetta Region" section is a copy of the 500 kV Hyderabad table.**
   - Rows 1–14 (Table 2.8, printed p.46–47) repeat Table 2.6 rows "Dadu - Jamshoro - I" to "Dadu - Moro", including the same km and dates. The page image confirms it.
   - **Consequence: the booklet has no 220 kV line list for Sindh or Balochistan.** These 14 rows are kept in the CSV with `usable=no`.
   - Table 2.9 reports this region as 2,213 km, while its own subtotal is 2,103 km.
2. **The 500 kV total disagrees within the booklet.**
   - The Table 2.6 rows sum to 6,584 km, and Table 2.7 totals 6,583 km.
   - Table 2.1 and Table C give 6,290 km for 2018-19.
   - Both values are recorded and **neither is used**.
3. **220 kV "Multan – T.T. Singh 1 & 2" appears twice with different data:**
   - Lahore row 7: March 1960, 82 km double circuit, 164 circuit-km.
   - Multan row 2: July 1995, 65 km double circuit, 130 circuit-km.
   - It could be two corridors or a double entry. [VERIFY on Day 5 by counting the OSM 220 kV circuits between Multan and T.T. Singh.]
4. **500 kV MVA totals differ between tables.** Table 2.15 gives 22,950 MVA and Table 2.16 gives 24,410 MVA. Table 2.16 also counts the 220/132 kV transformers at 500 kV stations, for example Dadu 2×160 + 1×250. Not needed for the model.

## How Day 5 uses it

- **Not an S4 reference.** The data is from 2019: 500 kV was 6,290–6,584 km then, against NGC's 9,313 km in 2025. S4 already passes against PER FY2024-25 (500 kV −0.03%, 220 kV +3.6%).
- **Per-line circuit cross-check (proposed rule).** On Day 5, change an OSM circuit count only where all three of these hold:
  - the OSM segment is `default1`, meaning no circuits or cables tag;
  - PSS lists the line as double circuit;
  - the PSS route km is within about 10% of the OSM corridor length.
  
  Each change is logged. S4 is recomputed **once** afterwards, with no further adjustment toward the target total.
- **S3 aliases.** The crosswalk below maps PER FY2024-25 Figure 1's 69 NGC stations to PSS 44th names. The S3 match rule must be written down before S3 is scored: name stem, alias with a cited source, or location hint at a matching voltage within a fixed distance. S3 is then reported **strict** (names and cited aliases only) and **with hints**.
- **Hint evidence.** `builder/config.json` now records the PSS evidence for the three [VERIFY] location hints under the key `pss44_16nov`:
  - Table 2.16 names "Yousafwala-Sahiwal".
  - Table 2.6 lists "Guddu 747 - Guddu Old" at 2 circuit-km.
  - Table 2.16 lists "Rawat".
  
  PSS has no coordinates, so the hint locations stay [VERIFY].

### PER Figure 1 (69 stations) ↔ PSS 44th

| | 500 kV (20) | 220 kV (49) |
|---|---|---|
| **Same station, same or abbreviated name in PSS** | 15: Rawat, Gatti (Gatti Faisalabad), Nokhar, S.K.P (Sheikhupura), New Lahore, Yousafwala (Yousafwala-Sahiwal), Multan, M.garh (Muzaffar Garh), D.G. Khan, RYK, Dadu, Guddu, Jamshoro, NKI (North Karachi Industrial), Shikarpur | 43, listed below |
| **Alias or spelling variant, [VERIFY]** | 1: Peshawar ↔ Sheikh Muhammadi | 2: Safdar Nagar ↔ "Sarfaraz Nagar Lahore"; Bandial ↔ "Bandala FSD" |
| **Named only in PSS line lists** | 3: TPS M.garh (220 kV "TPS-M/Garh-Multan", "TPS-M/garh-Bahawalpur"); 747 Guddu ("Guddu 747 - Guddu Old"); Moro ("Jamshoro- Moro", "Dadu - Moro") | 1: NGPS ("Multan - N.G.P.S 1&2", 14 km) |
| **Not in PSS (built after June 2019)** | 1: West FSD | 3: Lalian, Jhimpir 2, S.Y. Guddu |

- **The 43 direct 220 kV matches.** PSS spellings are in brackets where they differ.
  - Islamabad: Bannu, Burhan, Daudkhel, ISPR (Sangjani; lines say "Sangjani (ISPR)"), Mardan, Nowshera, Shahibagh, University (Islamabad University), Mansehra, Chakdara, D.I. Khan (DI-Khan).
  - Lahore: Band (Bund Road), Ghakkar (Ghakhar), Jaranwala (Jaranwala Road FSD), KSK (Kala Shah Kaku), Ludewala (Ludewala Sargodha), N.K.L.P (New KotLakhPat), Shalamar (New Shalamar), Nishatabad, Ravi, Sammundri (Samundari Road FSD), Sialkot (Sailkot), Wapda Town, Ghazi Road (Ghazi Lahore, New GIS), T.T. Singh, Gujrat, Kassowal, Okara.
  - Multan: Bahawalpur, M.garh, Vehari, Chistian (Chishtian), Lal Sohanra.
  - Hyderabad: Hala Road, Rohri, T.M.K (T.M.Khan), Daharki, Jhimpir 1 (Jhampir).
  - Quetta: Quetta, Sibbi, Khuzdar, Loralai, D.M. Jamali (Dera Murad Jamali).
- **Peshawar and Sheikh Muhammadi are probably one station.**
  - In 2019 PSS lists exactly two 500 kV stations in the Islamabad region, Rawat and Sheikh Muhammadi. PER lists Rawat and Peshawar.
  - PSS also calls the line "Tarbela- Sheikh Muhammadi Peshawar".
  - `day0/per_check.md` treats Sheikh Muhammadi as a separate bus to model. That is probably wrong, but it's left unchanged until verified [VERIFY].
  - S3 isn't affected: OSM station S0127 is named "Peshawar".
- PSS gives 61 of the 69 a station-table name: 58 direct and 3 by alias. The other 8 need OSM names, PER or other sources.

## Context only (not model inputs, not gate numbers)

- **132 kV:** 27,775 circuit-km in 2018-19 (Table 2.1). The series has breaks in 2008 and 2017, and the figure is six years old. The scored OSM build has 23,064 km at 132 kV. That comparison is only a rough sense of coverage, not a check.
- **Table C losses and demand:** transmission losses of 2.8% and recorded maximum demand. These sit close to holdouts H1 and H4, so they are **not used** to set or tune anything.
