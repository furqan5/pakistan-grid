# Topology build — explicit voltage tags only

OSM snapshot (Overpass `timestamp_osm_base`): 2026-11-06T18:19:47Z. Data © OpenStreetMap contributors, ODbL 1.0.

## Inputs and rule counts

- dc_links_after_collapse: 1
- dc_pieces_raw: 16
- edges_unknown_kv: 706
- endpoint_rule:dangling: 262
- endpoint_rule:nearest: 158
- endpoint_rule:plant_polygon: 98
- endpoint_rule:shared_node: 2657
- endpoint_rule:station_polygon: 2409
- km_unknown_kv: 5085.1
- plant_pass_through_nodes_ignored: 517
- plants: 6647
- segment_skipped_inside_station: 3597
- segments: 2791
- self_loops_dropped: 16
- series_joints_collapsed: 317
- series_merge_circuit_mismatch: 30
- stations_after_grouping: 1160
- substation_features: 1212
- way_excluded:below_min_kv: 14
- way_excluded:line=bay: 31
- way_excluded:line=busbar: 15
- ways_fetched: 3471
- ways_kept: 3411

## Buses by voltage × provenance

| kV | substation | plant | converter | tee_junction | dangling_end | total | in main component |
|---|---|---|---|---|---|---|---|
| 500 | 44 | 5 | 3 | 61 | 1 | 114 | 114 |
| 230 | 0 | 0 | 0 | 1 | 1 | 2 | 0 |
| 220 | 111 | 6 | 0 | 64 | 7 | 188 | 179 |
| 132 | 681 | 11 | 0 | 358 | 80 | 1130 | 1074 |
| 110 | 1 | 2 | 0 | 0 | 0 | 3 | 1 |
| 66 | 82 | 1 | 0 | 17 | 11 | 111 | 99 |

Buses whose every line has an inferred (not tagged) voltage: none

Transformer stubs (adjacent levels within a station/plant): 126. DC links: 1 (from 16 raw pieces).
- S0675 Matiari-Lahore HVDC Converter station ↔ S0789 Matiari-Lahore HVDC Converter Station: 887.0 km, 16 OSM ways

## Line km by voltage (AC branches after series collapse)

| kV | route km | circuit km | branches |
|---|---|---|---|
| 500 | 7,500 | 9,308 | 178 |
| 230 | 49 | 98 | 1 |
| 220 | 6,819 | 12,819 | 223 |
| 132 | 20,105 | 22,585 | 1243 |
| 110 | 5 | 5 | 1 |
| 66 | 2,394 | 2,467 | 91 |

Unknown-voltage edges left out: 706 (5085.1 km).

## Connected components (AC branches + transformer stubs)

Total components: 35. Largest 15:

| # | buses | km | buses by kV | plant buses |
|---|---|---|---|---|
| 0 | 1467 | 36,309.4 | {500: 114, 220: 179, 132: 1074, 110: 1, 66: 99} | 22 |
| 1 | 7 | 13.8 | {132: 7} | 1 |
| 2 | 4 | 12.0 | {132: 4} | 0 |
| 3 | 4 | 23.8 | {132: 2, 66: 2} | 0 |
| 4 | 4 | 61.0 | {66: 4} | 0 |
| 5 | 4 | 0.8 | {220: 4} | 0 |
| 6 | 3 | 28.1 | {132: 3} | 0 |
| 7 | 2 | 5.3 | {132: 2} | 0 |
| 8 | 2 | 8.3 | {132: 2} | 0 |
| 9 | 2 | 6.7 | {132: 2} | 0 |
| 10 | 2 | 0.9 | {132: 2} | 0 |
| 11 | 2 | 20.9 | {132: 2} | 0 |
| 12 | 2 | 49.1 | {230: 2} | 0 |
| 13 | 2 | 30.1 | {220: 2} | 0 |
| 14 | 2 | 48.9 | {132: 2} | 0 |

## Per-voltage connectivity (no transformers)

| kV | buses | components | 5 largest |
|---|---|---|---|
| 500 | 114 | 1 | [114] |
| 230 | 2 | 1 | [2] |
| 220 | 188 | 10 | [126, 29, 19, 4, 2] |
| 132 | 1130 | 33 | [527, 330, 77, 32, 29] |
| 110 | 3 | 2 | [2, 1] |
| 66 | 111 | 27 | [13, 12, 8, 7, 6] |

## Provisional S1 (gate counts buses at ≥66 kV in the main component with provenance substation/plant/converter)

- With K-Electric: **912**
- Without K-Electric (operator tag or Karachi bbox ≤220 kV): **896**
- Provisional: Days 3–4 still add station splitting checks, voltage fixes and duplicate collapse.

## 500 kV backbone check (PER FY2024-25 Figure 1, 20 NGC stations)

Found as a 500 kV bus by name: 19/20; in the largest 500 kV component: 19/20.

| PER name | matched OSM stations (500 kV bus) | in main 500 kV component |
|---|---|---|
| Rawat | S0049 500kV Grid Station / Rawat 500 kV [hint] | yes |
| Peshawar | S0127 Peshawar | yes |
| Gatti | S0028 Gatti | yes |
| Nokhar | S0083 500KV Nokhar Grid Station NTDC | yes |
| S.K.P (Sheikhupura) | S0079 500KV Grid Station NTDCL, Sheikhupura | yes |
| New Lahore | S0705 New Lahore | yes |
| West FSD | S0765 Faisalabad West | yes |
| Yousafwala | S0062 Sahiwal / Yousafwala 500 kV [hint] | yes |
| Multan | S0024 Multan | yes |
| M.garh | S0023 Muzaffargarh | yes |
| D.G. Khan | S0729 Dera Ghazi Khan | yes |
| RYK | S0213 Rahim Yar Khan | yes |
| TPS M.garh | — | no |
| Dadu | S0051 New Dadu | yes |
| Guddu | S0052 Guddu | yes |
| Jamshoro | S0025 NTDC 500KV Grid Station Jamshoro | yes |
| NKI | S0647 N. K. I | yes |
| Shikarpur | S0132 Shikarpur | yes |
| 747 Guddu | S0207 (unnamed) / 747 Guddu 500 kV [hint] | yes |
| Moro | S0690 Moro Converter Station | yes |
