# Topology build — explicit voltage tags only

OSM snapshot (Overpass `timestamp_osm_base`): 2026-11-06T18:19:47Z. Data © OpenStreetMap contributors, ODbL 1.0.

## Inputs and rule counts

- edges_unknown_kv: 842
- endpoint_rule:dangling: 262
- endpoint_rule:nearest: 158
- endpoint_rule:plant_polygon: 850
- endpoint_rule:shared_node: 2657
- endpoint_rule:station_polygon: 2413
- km_unknown_kv: 5079.5
- plants: 6647
- segment_skipped_inside_station: 3736
- segments: 3169
- self_loops_dropped: 16
- series_joints_collapsed: 317
- series_merge_circuit_mismatch: 31
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
| 500 | 44 | 18 | 3 | 61 | 1 | 127 | 127 |
| 230 | 0 | 0 | 0 | 1 | 1 | 2 | 0 |
| 220 | 111 | 101 | 0 | 64 | 7 | 283 | 273 |
| 132 | 681 | 109 | 0 | 358 | 80 | 1228 | 1169 |
| 110 | 1 | 2 | 0 | 0 | 0 | 3 | 1 |
| 66 | 82 | 3 | 0 | 17 | 11 | 113 | 101 |

Transformer stubs (adjacent levels within a station/plant): 137. HVDC/DC edges: 16.

## Line km by voltage (AC branches after series collapse)

| kV | route km | circuit km | branches |
|---|---|---|---|
| 500 | 7,497 | 9,304 | 195 |
| 230 | 49 | 98 | 1 |
| 220 | 6,812 | 12,816 | 336 |
| 132 | 20,096 | 22,576 | 1353 |
| 110 | 5 | 5 | 1 |
| 66 | 2,394 | 2,466 | 93 |

Unknown-voltage edges left out: 842 (5079.5 km).

## Connected components (AC branches + transformer stubs)

Total components: 35. Largest 15:

| # | buses | km | buses by kV | plant buses |
|---|---|---|---|---|
| 0 | 1671 | 36,290.1 | {500: 127, 220: 273, 132: 1169, 110: 1, 66: 101} | 226 |
| 1 | 9 | 13.6 | {132: 9} | 3 |
| 2 | 4 | 12.0 | {132: 4} | 0 |
| 3 | 4 | 23.8 | {132: 2, 66: 2} | 0 |
| 4 | 4 | 61.0 | {66: 4} | 0 |
| 5 | 4 | 0.8 | {220: 4} | 0 |
| 6 | 4 | 28.1 | {132: 4} | 1 |
| 7 | 3 | 1.9 | {220: 3} | 1 |
| 8 | 2 | 5.3 | {132: 2} | 0 |
| 9 | 2 | 8.3 | {132: 2} | 0 |
| 10 | 2 | 6.7 | {132: 2} | 0 |
| 11 | 2 | 0.9 | {132: 2} | 0 |
| 12 | 2 | 20.9 | {132: 2} | 0 |
| 13 | 2 | 49.1 | {230: 2} | 0 |
| 14 | 2 | 30.1 | {220: 2} | 0 |

## Per-voltage connectivity (no transformers)

| kV | buses | components | 5 largest |
|---|---|---|---|
| 500 | 127 | 1 | [127] |
| 230 | 2 | 1 | [2] |
| 220 | 283 | 10 | [201, 48, 19, 4, 3] |
| 132 | 1228 | 33 | [577, 368, 79, 33, 30] |
| 110 | 3 | 2 | [2, 1] |
| 66 | 113 | 27 | [13, 13, 8, 7, 6] |

## Provisional S1 (gate counts buses at ≥66 kV in the main component with provenance substation/plant/converter)

- With K-Electric: **1116**
- Without K-Electric (operator tag or Karachi bbox ≤220 kV): **1082**
- Provisional: Days 3–4 still add station splitting checks, voltage fixes and duplicate collapse.

## 500 kV backbone check (PER FY2024-25 Figure 1, 20 NGC stations)

Found as a 500 kV bus by name: 15/20; in the largest 500 kV component: 15/20.

| PER name | matched OSM stations (500 kV bus) | in main 500 kV component |
|---|---|---|
| Rawat | — | no |
| Peshawar | S0127 Peshawar | yes |
| Gatti | S0028 Gatti | yes |
| Nokhar | S0083 500KV Nokhar Grid Station NTDC | yes |
| S.K.P (Sheikhupura) | S0079 500KV Grid Station NTDCL, Sheikhupura | yes |
| New Lahore | S0705 New Lahore | yes |
| West FSD | S0765 Faisalabad West | yes |
| Yousafwala | — | no |
| Multan | S0024 Multan | yes |
| M.garh | S0023 Muzaffargarh | yes |
| D.G. Khan | S0729 Dera Ghazi Khan | yes |
| RYK | S0213 Rahim Yar Khan | yes |
| TPS M.garh | — | no |
| Dadu | S0051 New Dadu | yes |
| Guddu | S0052 Guddu | yes |
| Jamshoro | S0025 NTDC 500KV Grid Station Jamshoro | yes |
| NKI | — | no |
| Shikarpur | S0132 Shikarpur | yes |
| 747 Guddu | — | no |
| Moro | S0690 Moro Converter Station | yes |
