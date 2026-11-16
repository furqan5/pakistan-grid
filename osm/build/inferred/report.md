# Topology build — with voltage inference

OSM snapshot (Overpass `timestamp_osm_base`): 2026-11-06T18:19:47Z. Data © OpenStreetMap contributors, ODbL 1.0.

## Inputs and rule counts

- dangling_gap_bridge: 4
- dangling_snap_to_line: 78
- dc_links_after_collapse: 1
- dc_pieces_raw: 16
- edges_unknown_kv: 256
- endpoint_rule:dangling: 180
- endpoint_rule:nearest: 158
- endpoint_rule:plant_polygon: 98
- endpoint_rule:shared_node: 2889
- endpoint_rule:station_polygon: 2409
- km_unknown_kv: 1505.0
- kv_inferred:common_station_level: 43
- kv_inferred:junction_neighbour: 288
- kv_inferred:single_level_station: 141
- plant_pass_through_nodes_ignored: 517
- plants: 6647
- segment_skipped_inside_station: 3597
- segments: 2866
- self_loops_dropped: 43
- series_joints_collapsed: 401
- series_merge_circuit_mismatch: 32
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
| 500 | 46 | 7 | 3 | 67 | 3 | 126 | 126 |
| 230 | 0 | 0 | 0 | 1 | 1 | 2 | 0 |
| 220 | 155 | 9 | 0 | 112 | 7 | 283 | 274 |
| 132 | 767 | 14 | 0 | 423 | 82 | 1286 | 1266 |
| 110 | 1 | 2 | 0 | 0 | 0 | 3 | 1 |
| 66 | 97 | 1 | 0 | 24 | 13 | 135 | 127 |

Buses whose every line has an inferred (not tagged) voltage: 500 kV: 11, 220 kV: 83, 132 kV: 149, 66 kV: 24

Transformer stubs (adjacent levels within a station/plant): 143. DC links: 1 (from 16 raw pieces).
- S0675 Matiari-Lahore HVDC Converter station ↔ S0789 Matiari-Lahore HVDC Converter Station: 887.0 km, 16 OSM ways

## Line km by voltage (AC branches after series collapse)

| kV | route km | circuit km | branches |
|---|---|---|---|
| 500 | 7,592 | 9,451 | 193 |
| 230 | 49 | 98 | 1 |
| 220 | 7,564 | 13,763 | 344 |
| 132 | 22,270 | 25,314 | 1487 |
| 110 | 5 | 5 | 1 |
| 66 | 2,961 | 3,073 | 125 |

Unknown-voltage edges left out: 256 (1505.0 km).

## Connected components (AC branches + transformer stubs)

Total components: 18. Largest 15:

| # | buses | km | buses by kV | plant buses |
|---|---|---|---|---|
| 0 | 1794 | 40,038.1 | {500: 126, 220: 274, 132: 1266, 110: 1, 66: 127} | 31 |
| 1 | 6 | 62.9 | {66: 6} | 0 |
| 2 | 4 | 50.0 | {132: 4} | 0 |
| 3 | 4 | 0.8 | {220: 4} | 0 |
| 4 | 3 | 22.1 | {132: 3} | 0 |
| 5 | 2 | 49.1 | {230: 2} | 0 |
| 6 | 2 | 30.1 | {220: 2} | 0 |
| 7 | 2 | 48.9 | {132: 2} | 0 |
| 8 | 2 | 40.0 | {132: 2} | 0 |
| 9 | 2 | 57.6 | {132: 2} | 0 |
| 10 | 2 | 1.5 | {132: 2} | 0 |
| 11 | 2 | 11.1 | {66: 2} | 0 |
| 12 | 2 | 1.7 | {132: 2} | 0 |
| 13 | 2 | 21.1 | {132: 2} | 0 |
| 14 | 2 | 2.2 | {220: 2} | 0 |

## Per-voltage connectivity (no transformers)

| kV | buses | components | 5 largest |
|---|---|---|---|
| 500 | 126 | 1 | [126] |
| 230 | 2 | 1 | [2] |
| 220 | 283 | 10 | [166, 78, 25, 4, 2] |
| 132 | 1286 | 18 | [1074, 63, 35, 30, 28] |
| 110 | 3 | 2 | [2, 1] |
| 66 | 135 | 24 | [16, 16, 12, 10, 9] |

## Provisional S1 (gate counts buses at ≥66 kV in the main component with provenance substation/plant/converter)

- With K-Electric: **1089**
- Without K-Electric (operator tag or Karachi bbox ≤220 kV): **1052**
- Provisional: Days 3–4 still add station splitting checks, voltage fixes and duplicate collapse.

## K-Electric region (working definition in config `ke_region`, [VERIFY])

KE buses in the main component by kV (substation / plant / tee / dangling); PER FY2024-25 KE grid stations: 500 kV 1, 220 kV 12, 132 kV 62, 66 kV 3.

- 220 kV: substation 24, plant 3, tee 17, dangling 0
- 132 kV: substation 9, plant 1, tee 2, dangling 0

Interface edges between KE and the rest of the main grid: 13 (these carry TSEP's 'Export to KE').

| NGC-side bus | KE-side bus | type | kV | km |
|---|---|---|---|---|
| J:11155260024@220  | J:11068174950@220  | line | 220 | 69.4 |
| J:5407572523@132  | S:S0612@132 Gharo Grid Station | K-ELECTRIC | line | 132 | 26.2 |
| J:5407600467@132  | S:S0158@132  | line | 132 | 20.5 |
| J:5407625680@220  | J:11870783812@220  | line | 220 | 43.6 |
| J:5523661818@132  | S:S0589@132  | line | 132 | 45.2 |
| S:S0139@132 Baldia Grid Station | P:P0031@132 Tapal Energy Power Plant | line | 132 | 9.7 |
| S:S0139@220 Baldia Grid Station | J:3898564479@220  | line | 220 | 6.7 |
| S:S0601@132  | S:S1142@132  | line | 132 | 9.2 |
| S:S0647@220 N. K. I | J:3898564479@220  | line | 220 | 6.5 |
| S:S0649@220  | S:S0128@220 K.D.A-33 | line | 220 | 95.5 |
| S:S0739@500  | S:S0739@220  | transformer |  | 0.0 |
| S:S0772@220 Jhimpir II | S:S0128@220 K.D.A-33 | line | 220 | 84.6 |
| S:S1055@500  | S:S1055@220  | transformer |  | 0.0 |

## Snapping and quirks (Day 4)

- Dangling ends snapped to another line's node (≤150 m): 78; end-to-end gaps bridged (≤500 m): 4. Each in snaps.csv.
- Quirks logged in quirks.csv: {'circuit_mismatch': 32, 'self_loop': 43}.

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
