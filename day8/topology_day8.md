# Day 8: loads, K-Electric export, capacitors, S2 (18 Nov 2026)

Rules: `builder/parameters.json` → `loads`, pushed in 8c77814 **before** any load was placed. `builder/make_loads.py` was pushed in 8dc5111 before its first run. Output: `osm/build/explicit/params/loads_summary.md` (the CSVs aren't committed).

## Same day, before loads (Day 7b)

- **GEM.** Furqan downloaded the Global Energy Monitor tracker bundle. It placed 13 of the 18 unlocated plants: Khan Khawar, Jaggran-I, Malakand-3, six bagasse plants, Artistic 1 and 2, UEP, and HNDS at the Sukkur solar farm.
- **Excluded by a logged rule amendment:** 5 small hydro plants (77 MW) that neither OSM nor GEM can place.
- **Result:** 35,277 MW of generation in the model (−0.2% against IGCEP less exclusions). Summer margin 2,224 MW, or 1,412 MW of deliverable capacity.
- **Gate v1.0 signed off** (48327b6). Furqan instructed the sign-off and delegated the open choices; the choices made after their result was known are labelled post hoc in the gate.

## Results

- **DISCO load.**
  - Summer 26,932 MW and winter off-peak 8,720 MW. That is I1 × 26,380/26,542, because Gwadar's 162 MW share is off-grid and not placed.
  - Placed on **700 load stations**: 657 at 132 kV and 43 at 66 kV.
  - Power factor is uniform from I1: Q/P 0.591 in summer, 0.465 in winter.
- **DISCO assignment.** Each station goes to the DISCO of the nearest of 56 PSS-labelled NTDC stations.

  | Group | TSEP MW | Load stations | MW per station | Median distance to its anchor |
  |---|---|---|---|---|
  | LESCO | 5,701 | 74 | 78.7 | 16 km |
  | MEPCO | 4,870 | 114 | 43.6 | 33 km |
  | PESCO+TESCO | 3,448 | 93 | 37.9 | 34 km |
  | FESCO | 3,296 | 81 | 41.5 | 33 km |
  | IESCO | 2,923 | 84 | 35.5 | 19 km |
  | GEPCO | 2,704 | 52 | 53.1 | 31 km |
  | HESCO | 1,232 | 79 | 15.9 | 45 km |
  | QESCO | 1,172 | 65 | 18.4 | 80 km |
  | SEPCO | 1,034 | 58 | 18.2 | 30 km |

- **Plausibility, reported only.** The booklet gives 132 kV grid stations by province for 2019. The model has more stations now because the network has grown, and its counts include 66 kV.

  | Province | Model load stations | PSS 44th, 2019 |
  |---|---|---|
  | Punjab (incl. IESCO) | 405 | 446 |
  | Sindh (HESCO, SEPCO) | 137 | 116 |
  | Khyber Pakhtunkhwa | 93 | 88 |
  | Balochistan | 65 | 72 |

  The 14-day plan's "NEPRA Table 60" isn't held, so these PSS counts are used instead.
- **FESCO and MEPCO station demand tables.**
  - The extraction is complete: 195 and 183 stations, 2026-27 column, no numbering gaps.
  - But **OSM names only 10 of FESCO's 81 and 21 of MEPCO's 114 load stations**, and 164 table stations in each DISCO match no OSM station at all.
  - So only 4 and 7 stations, covering 237 and 423 MW of table demand, are weighted by the tables. The rest fall back to an even share of the unmatched demand.
  - This is an OSM naming gap, not a matching fault. **Within-DISCO load is therefore mostly an equal split per station in every DISCO.**
- **K-Electric export.** 2,050 MW / 795 MVAr (summer) and 1,001 / 68 (winter) on the 9 KE-side interface buses, split by interface rate_a.
- **Capacitors.** 12,192 MVAr (summer) and 146 (winter) on the 132 kV DISCO load buses, nameplate at 1.0 pu. **Equal to the TSEP totals. The Day 6 exit check is now complete for capacitors as well.**

## S2: PASS (signed-off denominators)

- **Load in the main component: 100%.** Every load station is in the main component by construction.
- **Installed generation in the main component: 99.8%**, 35,277 of 35,355 MW. The 5 excluded hydro plants count as missing.
- The S2 denominators were fixed at sign-off **after** earlier values had been seen (see the gate). The result is recorded in `gate/G1_log.md` next to the Day 5 values.

## Before the first solve (Day 9), still to declare and push

1. **Short branches:** 194 branches are under 0.5 km. Choose a minimum-impedance floor or bus merges. First check how GridSFM's `patch_model.jl` treats them.
2. **Winter openings:** keep "direct branch only" (2 of 15 applied) or declare a path rule.
3. **Assembly:** build the PowerModels JSON from the parameter tables for both snapshots, then run a DC-OPF smoke test.

The gate is signed. The holdouts H1–H8 are computed only on Day 11.
