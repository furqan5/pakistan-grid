# Topology build — with voltage inference

OSM snapshot (Overpass `timestamp_osm_base`): 2026-11-06T18:19:47Z. Data © OpenStreetMap contributors, ODbL 1.0.

## Inputs and rule counts

- edges_unknown_kv: 390
- endpoint_rule:dangling: 262
- endpoint_rule:nearest: 158
- endpoint_rule:plant_polygon: 850
- endpoint_rule:shared_node: 2657
- endpoint_rule:station_polygon: 2413
- km_unknown_kv: 1714.8
- kv_inferred:common_station_level: 65
- kv_inferred:junction_neighbour: 221
- kv_inferred:single_level_station: 166
- plants: 6647
- segment_skipped_inside_station: 3736
- segments: 3169
- self_loops_dropped: 45
- series_joints_collapsed: 394
- series_merge_circuit_mismatch: 29
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
| 500 | 45 | 20 | 3 | 65 | 2 | 135 | 135 |
| 230 | 0 | 0 | 0 | 1 | 1 | 2 | 0 |
| 220 | 142 | 118 | 0 | 96 | 12 | 368 | 358 |
| 132 | 749 | 138 | 0 | 375 | 116 | 1378 | 1335 |
| 110 | 1 | 2 | 0 | 0 | 0 | 3 | 1 |
| 66 | 97 | 3 | 0 | 18 | 13 | 131 | 119 |

Transformer stubs (adjacent levels within a station/plant): 151. HVDC/DC edges: 16.

## Line km by voltage (AC branches after series collapse)

| kV | route km | circuit km | branches |
|---|---|---|---|
| 500 | 7,581 | 9,430 | 208 |
| 230 | 49 | 98 | 1 |
| 220 | 7,507 | 13,694 | 439 |
| 132 | 22,132 | 24,736 | 1557 |
| 110 | 5 | 5 | 1 |
| 66 | 2,933 | 3,005 | 119 |

Unknown-voltage edges left out: 390 (1714.8 km).

## Connected components (AC branches + transformer stubs)

Total components: 29. Largest 15:

| # | buses | km | buses by kV | plant buses |
|---|---|---|---|---|
| 0 | 1948 | 39,739.3 | {500: 135, 220: 358, 132: 1335, 110: 1, 66: 119} | 274 |
| 1 | 6 | 62.9 | {66: 6} | 0 |
| 2 | 5 | 13.0 | {132: 5} | 2 |
| 3 | 5 | 30.2 | {132: 5} | 2 |
| 4 | 4 | 23.8 | {132: 2, 66: 2} | 0 |
| 5 | 4 | 0.8 | {220: 4} | 0 |
| 6 | 3 | 1.9 | {220: 3} | 1 |
| 7 | 2 | 5.3 | {132: 2} | 0 |
| 8 | 2 | 8.3 | {132: 2} | 0 |
| 9 | 2 | 49.1 | {230: 2} | 0 |
| 10 | 2 | 30.1 | {220: 2} | 0 |
| 11 | 2 | 48.9 | {132: 2} | 0 |
| 12 | 2 | 4.1 | {132: 2} | 0 |
| 13 | 2 | 14.3 | {132: 2} | 0 |
| 14 | 2 | 40.0 | {132: 2} | 0 |

## Per-voltage connectivity (no transformers)

| kV | buses | components | 5 largest |
|---|---|---|---|
| 500 | 135 | 1 | [135] |
| 230 | 2 | 1 | [2] |
| 220 | 368 | 10 | [234, 94, 25, 4, 3] |
| 132 | 1378 | 28 | [1141, 69, 35, 34, 28] |
| 110 | 3 | 2 | [2, 1] |
| 66 | 131 | 25 | [17, 16, 10, 10, 8] |

## Provisional S1 (gate counts buses at ≥66 kV in the main component with provenance substation/plant/converter)

- With K-Electric: **1287**
- Without K-Electric (operator tag or Karachi bbox ≤220 kV): **1236**
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
