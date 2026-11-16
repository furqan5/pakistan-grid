# Topology build — explicit voltage tags only

OSM snapshot (Overpass `timestamp_osm_base`): 2026-11-06T18:19:47Z. Data © OpenStreetMap contributors, ODbL 1.0.

## Inputs and rule counts

- dangling_gap_bridge: 4
- dangling_snap_to_line: 78
- dc_links_after_collapse: 1
- dc_pieces_raw: 16
- edges_unknown_kv: 728
- endpoint_rule:dangling: 180
- endpoint_rule:nearest: 158
- endpoint_rule:plant_polygon: 98
- endpoint_rule:shared_node: 2889
- endpoint_rule:station_polygon: 2409
- km_unknown_kv: 5085.1
- plant_pass_through_nodes_ignored: 517
- plants: 6647
- segment_skipped_inside_station: 3597
- segments: 2866
- self_loops_dropped: 16
- series_joints_collapsed: 346
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
| 500 | 44 | 5 | 3 | 61 | 1 | 114 | 114 |
| 230 | 0 | 0 | 0 | 1 | 1 | 2 | 0 |
| 220 | 111 | 6 | 0 | 67 | 4 | 188 | 179 |
| 132 | 681 | 11 | 0 | 382 | 54 | 1128 | 1092 |
| 110 | 1 | 2 | 0 | 0 | 0 | 3 | 1 |
| 66 | 82 | 1 | 0 | 18 | 10 | 111 | 103 |

Buses whose every line has an inferred (not tagged) voltage: none

Transformer stubs (adjacent levels within a station/plant): 126. DC links: 1 (from 16 raw pieces).
- S0675 Matiari-Lahore HVDC Converter station ↔ S0789 Matiari-Lahore HVDC Converter Station: 887.0 km, 16 OSM ways

## Line km by voltage (AC branches after series collapse)

| kV | route km | circuit km | branches |
|---|---|---|---|
| 500 | 7,500 | 9,310 | 178 |
| 230 | 49 | 98 | 1 |
| 220 | 6,819 | 12,846 | 224 |
| 132 | 20,105 | 23,064 | 1265 |
| 110 | 5 | 5 | 1 |
| 66 | 2,394 | 2,505 | 92 |

Unknown-voltage edges left out: 728 (5085.1 km).

## Connected components (AC branches + transformer stubs)

Total components: 24. Largest 15:

| # | buses | km | buses by kV | plant buses |
|---|---|---|---|---|
| 0 | 1489 | 36,401.9 | {500: 114, 220: 179, 132: 1092, 110: 1, 66: 103} | 22 |
| 1 | 7 | 13.8 | {132: 7} | 1 |
| 2 | 4 | 12.0 | {132: 4} | 0 |
| 3 | 4 | 61.0 | {66: 4} | 0 |
| 4 | 4 | 0.8 | {220: 4} | 0 |
| 5 | 3 | 28.1 | {132: 3} | 0 |
| 6 | 2 | 6.7 | {132: 2} | 0 |
| 7 | 2 | 0.9 | {132: 2} | 0 |
| 8 | 2 | 20.9 | {132: 2} | 0 |
| 9 | 2 | 49.1 | {230: 2} | 0 |
| 10 | 2 | 30.1 | {220: 2} | 0 |
| 11 | 2 | 48.9 | {132: 2} | 0 |
| 12 | 2 | 40.0 | {132: 2} | 0 |
| 13 | 2 | 35.8 | {66: 2} | 0 |
| 14 | 2 | 57.6 | {132: 2} | 0 |

## Per-voltage connectivity (no transformers)

| kV | buses | components | 5 largest |
|---|---|---|---|
| 500 | 114 | 1 | [114] |
| 230 | 2 | 1 | [2] |
| 220 | 188 | 10 | [126, 29, 19, 4, 2] |
| 132 | 1128 | 22 | [539, 415, 32, 29, 25] |
| 110 | 3 | 2 | [2, 1] |
| 66 | 111 | 26 | [13, 12, 8, 7, 6] |

## Provisional S1 (gate counts buses at ≥66 kV in the main component with provenance substation/plant/converter)

- With K-Electric: **924**
- Without K-Electric (operator tag or Karachi bbox ≤220 kV): **904**
- Provisional: Days 3–4 still add station splitting checks, voltage fixes and duplicate collapse.

## K-Electric region (working definition in config `ke_region`, [VERIFY])

KE buses in the main component by kV (substation / plant / tee / dangling); PER FY2024-25 KE grid stations: 500 kV 1, 220 kV 12, 132 kV 62, 66 kV 3.

- 220 kV: substation 13, plant 0, tee 7, dangling 0
- 132 kV: substation 6, plant 1, tee 1, dangling 0

Interface edges between KE and the rest of the main grid: 10 (these carry TSEP's 'Export to KE').

| NGC-side bus | KE-side bus | type | kV | km |
|---|---|---|---|---|
| J:11155260024@220  | J:11068174950@220  | line | 220 | 69.4 |
| J:5407572523@132  | J:5407566608@132  | line | 132 | 26.0 |
| J:5407600467@132  | S:S0158@132  | line | 132 | 20.5 |
| J:5407625680@220  | J:11870783812@220  | line | 220 | 43.6 |
| S:S0139@132 Baldia Grid Station | P:P0031@132 Tapal Energy Power Plant | line | 132 | 9.7 |
| S:S0139@220 Baldia Grid Station | J:3898564479@220  | line | 220 | 6.7 |
| S:S0588@132  | S:S0589@132  | line | 132 | 52.6 |
| S:S0647@220 N. K. I | J:3898564479@220  | line | 220 | 6.5 |
| S:S0772@220 Jhimpir II | S:S0128@220 K.D.A-33 | line | 220 | 84.6 |
| S:S1055@500  | S:S1055@220  | transformer |  | 0.0 |

## Snapping and quirks (Day 4)

- Dangling ends snapped to another line's node (≤150 m): 78; end-to-end gaps bridged (≤500 m): 4. Each in snaps.csv.
- Quirks logged in quirks.csv: {'circuit_mismatch': 32, 'self_loop': 16}.

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
