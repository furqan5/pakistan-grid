# Day 2 — First OSM topology build (6–9 Nov 2026)

The code is in `builder/build_topology.py` and its rules in `builder/config.json`. Outputs are in `osm/build/{explicit,inferred}/`: `report.md`, plus CSVs that aren't committed.
Data © OpenStreetMap contributors, ODbL 1.0.

## Data fetch

- **Boundary:** Overpass area `ISO3166-1=PK`. It includes AJK and GB: Muzaffarabad, Mirpur, Gilgit and Skardu are all inside.
- **Substations and plants:** fetched in full, with no `remark`. Counts are identical to the 5 Nov audit: 1,212 substation features and 6,651 plants (6,647 have geometry).
- **Lines:**
  - The whole-country query failed on 24 attempts across 4 mirrors (502/504 overload).
  - It was fetched as 6 bbox tiles, each still clipped to the PK area, and merged by way id.
  - The `overpass.private.coffee` mirror served **stale data (osm_base 24 Jul 2026) and returned an empty Quetta tile**. That tile was refetched from overpass-api.de. **Don't use that mirror.**
  - Merged result: 3,471 ways, SHA-256 `81be29f9…ba0ef0`, snapshot 6 Nov 2026 18:19–18:46 UTC.
  - Route-km by voltage matches the 5 Nov audit: 500 kV 7,522 km, 132 kV 20,083 km, 66 kV 2,399 km and HVDC 887 km are identical. 220 kV is +1 km and untagged +84 km, from edits made since.

## First build: two modes

| | Explicit voltage tags only | With voltage inference |
|---|---|---|
| Ways kept (after dropping 31 bay, 15 busbar and 14 below-66 kV ways) | 3,411 | 3,411 |
| Stations after grouping (1,212 features) | 1,160 | 1,160 |
| Unknown-voltage edges left out | 842 (5,080 km) | 390 (1,715 km) |
| Buses in the main component | 1,671 | 1,948 |
| Components (AC + transformer stubs) | — | 29. The main one holds 99% of buses and 39,739 km |
| 500 kV buses / components | 127 / 1 | 135 / **1** |
| Circuit-km at 500 kV (NGC 9,313) | **9,304 (−0.1%)** | 9,430 (+1.3%) |
| Circuit-km at 220 kV (NGC + KE ≈ 12,400) | 12,816 (+3.4%) | 13,694 (+10.4%) |
| Provisional S1 with KE / without KE | **1,116 / 1,082** | 1,287 / 1,236 |
| 500 kV backbone: PER Figure 1 stations found by name | 15/20, all in the single 500 kV component | 15/20, same |

Endpoint resolution in the inferred build:
- inside a station polygon: 2,413;
- shared OSM node: 2,657;
- inside a plant polygon: 850;
- nearest station within 1 km with a matching voltage: 158;
- dangling: 262.

Voltage inference used three rules: junction neighbour (221), single-level station (166), and a voltage shared by both end stations (65).

**Reading.** The S1 floor (≥500 buses) looks comfortably reachable even after the fixes below remove spurious buses. This is **not** the gate result, which is due at the end of Day 5.
The 500 kV layer closely matches NGC's own statistics: −0.1% circuit-km on explicit tags, and one connected component.

## Defects found (Day 3–4 work, in order)

1. **Plant pass-through buses.**
   - 180 of 281 plant buses have degree 2 and are fed by a single OSM way. Those are lines crossing a plant polygon (solar farms, plant boundaries), not ending in it.
   - Fix: split ways at plant polygons only where the way ends inside one, then collapse the rest. This lowers S1 by up to about 180.
2. **HVDC.** The ±660 kV Matiari–Lahore link (20 ways, 887 km) comes out as 16 chained DC pieces between S0675 and S0789.
   - Fix: collapse it into one `dcline` and check that both ends are the converter stations.
3. **220 kV substation buses: 142, of which 72 are named, against 61 official stations** (NGC 49 + KE 12).
   - Audit for 220 kV IPP switchyards tagged as substations, split station groups, and voltages assigned wrongly by the single-level-station rule.
   - The inferred build adds 878 circuit-km at 220 kV over the explicit build, so the inference rules need checking against S4.
4. **Backbone names not matched:** Rawat, Yousafwala, TPS M.garh, NKI and 747 Guddu. Check by location; the polygons may be unnamed or named differently (e.g. "Rewat", "Yusufwala").
5. **Odd voltages:** one 230 kV line (49 km) and three 110 kV buses. Probably tagging slips for 220 and 132 kV. Retag with a log entry.
6. **Leftovers:**
   - 45 self-loops dropped;
   - 29 series merges with mismatched circuits;
   - 262 dangling ends;
   - 390 unknown-voltage edges (1,715 km) still out.
7. **K-Electric.** KE is currently flagged by operator tag or by a Karachi bbox at ≤220 kV, which is approximate. S1 is reported with and without KE, as the gate needs.

## Method notes

- **Endpoint order:** inside a station polygon (75 m buffer) wins over a shared OSM node. This keeps two ways that meet inside a substation from becoming a junction outside it. After that come a shared node, then the nearest station within 1 km with a matching voltage, then dangling.
- **Station grouping:** polygons within 250 m, or with the same name stem within 1.5 km, become one station, with one bus per voltage level and transformer stubs between adjacent levels. 1,212 features → 1,160 stations.
  - Known risk: 747 Guddu and Guddu (500 kV) sit close together and may merge.
- **Circuits:** the `circuits` tag, else `cables/3`, else 1. Multi-voltage ways split their circuits across voltages.
- **Geometry:** lengths are haversine along the OSM geometry. Snapping uses an equirectangular projection at 30°N (up to about 8% E-W scale error at the extremes, which matters only for tolerances).
