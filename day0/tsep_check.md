# Day 0 — TSEP 2024-34 by-eye check

Checked 6 Nov 2026 against `sources/tsep_2024-34_report.pdf` (166 pages, created 30 Apr 2024, SHA-256 in `logs/downloads.tsv`).
Method: `pdftotext -layout` was used only to find the pages. Every value below was then read off the rendered page image.
"PDF p." is the PDF page index; "printed p." is the page number printed on the page.

## Table 2-1 — System peak demand forecasts (low-demand scenario), MW — PDF p.22 / printed p.5

| Name | 2025-26 | 2026-27 |
|---|---|---|
| LESCO | 5521 | 5701 |
| GEPCO | 2564 | 2704 |
| FESCO | 3106 | 3296 |
| IESCO | 2794 | 2923 |
| MEPCO | 4663 | 4870 |
| PESCO | 2790 | 2899 |
| HESCO | 1205 | 1232 |
| QESCO | 1128 | 1172 |
| TESCO | 534 | 549 |
| SEPCO | 1005 | 1034 |
| Gwadar | 145 | 162 |
| NTDC | 26226 | 27316 |
| Export to KE | 2050 | 2050 |
| Total NTDC | 28276 | 29366 |

Matches the report (26,226 MW and 28,276 MW for 2025-26). Note: this is the **low**-demand scenario, and the T&T losses exclude HVDC loss.
The July/Aug 2026 base case falls in FY2026-27, and its load (27,097 MW) sits just below the 2026-27 NTDC figure (27,316 MW).

## Table 5-1 — Summer peak, July/August 2026 — PDF p.51 / printed p.34

| Description | MW | MVAR |
|---|---|---|
| NTDC generation | 30180 | 6332 |
| NTDC/DISCOs load | 27097 | 16017 |
| Export to KE | 2050 | 795 |
| Shunt reactors | – | 6162 |
| Shunt capacitors | – | −12192 (excludes HVDC terminal filters) |
| Line charging | – | −17517 |
| Losses | 1033 | 18161 |

The text on the same page gives 4,000 MW on the HVDC link and says loads were studied in PSS/E with ACCC.
Matches the report. The report omits two values that are worth carrying: KE export Q = 795 MVAr, and reactive losses = 18,161 MVAr.

## Table 5-7 — Major line openings, winter peak 2027 (also used for off-peak) — PDF p.65 / printed p.48

The table lists 15 circuits:
- 500 kV: Ghazi Brotha–Gatti S/C; Gujranwala–Rawat S/C; Gujranwala–Neelum Jhelum S/C; Maira–Suki Kinari S/C; Maira–Karot S/C; Maira–Islamabad West S/C; Tarbela–Rawat S/C; Tarbela–Ghazi Brotha S/C; Rawat–Islamabad West S/C; Matiari–Moro D/C; Moro–R.Y. Khan D/C.
- 220 kV: Kassowal–Arifwala S/C; Kassowal–Vehari S/C; KAPCO–Multan S/C; KAPCO–M. Garh Solar S/C.

## Table 5-8 — Winter peak, January 2027 — PDF p.66 / printed p.49

| Description | MW | MVAR |
|---|---|---|
| NTDC generation | 17954 | 1461 |
| NTDC/DISCOs load | 15927 | 7547 |
| Export to KE | 1500 | 107 |
| Shunt reactors | – | 7608 |
| Shunt capacitors | – | −3748 |
| Line charging | – | −15582 |
| Losses | 528 | 10460 |

## Table 5-9 — Proposed new shunt reactors (included in the base case) — PDF p.68 / printed p.51

- 500 kV, 111 MVAr each: Sheikh Muhammadi, Rawat, Faisalabad West, D.G. Khan.
- 500 kV, 222 MVAr: Shikarpur.
- 220 kV, 60 MVAr each: Zhob, D.M. Jamali, Loralai.
- Total: 846 MVAr.

## Table 5-10 — Winter off-peak, January 2027 — PDF p.69 / printed p.52

| Description | MW | MVAR |
|---|---|---|
| NTDC generation | 9982 | −800 |
| NTDC/DISCOs load | 8774 | 4082 |
| Export to KE | 1001 | 68 |
| Shunt reactors | – | 8211 |
| Shunt capacitors | – | −146 |
| Line charging | – | −15897 |
| Losses | 207 | 4220 |

Matches the report.

## Figure 5-8 — Voltages at key 500 kV buses, winter off-peak 2027 — PDF p.69

The figure is a line plot, so these readings are by eye, ±0.003 pu:
- Peshawar 1.040, Nowshera 1.045, Tarbela 1.050, Rewat-N 1.035, Gujranwala 1.038
- G. Brotha 1.053, Lahore 1.042, Gatti 1.047, Fbd-West 1.053, HBS-CCPP 1.056
- Multan 1.051, M. Garh 1.053, D.G. Khan 1.050, R.Y. Khan 1.050, Guddu 1.048
- Shikarpur 1.050, Dadu 1.048, Jamshoro 1.047, SECL CFPP 1.045, K-2/K-3 1.035

This figure is not in the report. It is a candidate extra reported-only holdout (H8 in the gate draft).

## Does TSEP print its own 2026 network circuit-km by voltage?

**No.** A text search of all 166 pages for "circuit-km", "Cct-km" and numeric "km" values found only three kinds of hit:
- the abbreviation list (p.17);
- line-length criteria for ratings (p.51: 80 km thermal/stability split);
- per-project line lengths in the expansion lists (pp.144–158).

No page gives a voltage-wise circuit-km total for the 2026 base-case network.
**Consequence for the gate:** H2 (line charging) is **reported only**, not scored. Normalising it with TIP km would leak the holdout.

## Other facts noticed

- TSEP 2024-34 was prepared by NTDC planning engineers with USAID's Power Sector Improvement Activity (PSIA) team (PDF p.18).
- Ratings rule (p.51): 220 kV lines shorter than 80 km use thermal limits and longer ones use stability limits. 500 kV lines use stability limits depending on length. Transformers get a 10% overload margin.
