# Day 3 — Topology defects fixed (16 Nov 2026)

The builder is `builder/build_topology.py`; config changes are in `builder/config.json`.
The Day 2 reports are kept in `osm/build/day2/` for comparison; the current ones are in `osm/build/{explicit,inferred}/report.md`.
The OSM input is unchanged (snapshot 6 Nov 2026, `lines.json` SHA-256 `81be29f9…`).

## Fixes

1. **Plant pass-through buses.**
   - A plant polygon now terminates a line only where a way ends inside it, or where two or more ways share a node inside it.
   - 517 crossing nodes are now ignored, and plant buses fell from 281 to 31 (inferred) or 23 (explicit).
2. **HVDC.**
   - DC pieces joined at plain junctions are collapsed. The result is **one ±660 kV link, 887.0 km, between S0675 "Matiari-Lahore HVDC Converter station" (25.71°N 68.52°E) and S0789 (31.26°N 73.83°E)**.
   - That matches PER's 886 km per pole.
3. **Voltage inference without cascades.**
   - Station-based rules now use a station's tag voltages plus the voltages of its incident lines **with tagged voltage**, never inferred ones. On Day 2 inferred voltages fed back into the station levels and spread.
   - A tag-only variant was tried first and dropped: it left 3,204 km unknown, because only 27% of substations carry a voltage tag.
   - Inference counts: 215 junction-neighbour, 148 single-level station, 44 common station level.
4. **Backbone names.**
   - Matching now ignores punctuation, so "N. K. I" matches NKI.
   - Three stations get location-based name hints, keyed by OSM id in `config.json` and **each marked [VERIFY]**:
     - Rawat = `w241957315` ("500kV Grid Station", 132/220/500 kV, 33.48°N 73.19°E);
     - 747 Guddu = `w559254617` (unnamed 500 kV polygon about 1 km from "Guddu");
     - Yousafwala = `w245490150` (OSM "Sahiwal", 220/500 kV; NGC lists no "Sahiwal" 500 kV station).
   - **TPS M.garh** isn't a separate OSM station. It's inside the 4-polygon "Muzaffargarh" group (S0023, 132/220/500 kV), merged by the 250 m rule. It counts once for S3 unless it's split later.
   - Hints affect naming and reporting only, never topology.

## Results

| | Day 2 (inferred) | Day 3 explicit tags | Day 3 inferred |
|---|---|---|---|
| Plant buses | 281 | 23 | 31 |
| DC links | 16 pieces | 1 × 887 km | 1 × 887 km |
| Unknown-voltage edges / km left out | 390 / 1,715 | 706 / 5,085 | 299 / 1,827 |
| Main-component buses | 1,948 | 1,467 | 1,712 |
| 500 kV buses / components | 135 / 1 | 114 / 1 | 124 / 1 |
| **500 kV circuit-km** (NGC 9,313; S4 ≈9,320 ±10%) | 9,430 | **9,308 (−0.1%)** | 9,446 (+1.4%) |
| **220 kV circuit-km** (NGC 11,933 + KE 467 ≈ 12,400 ±10%) | 13,694 | **12,819 (+3.4%)** | 13,635 (+10.0%, borderline) |
| 132 kV circuit-km | 24,736 | 22,585 | 24,698 |
| **Provisional S1** with KE / without KE (floor 500) | 1,287 / 1,236 | **912 / 896** | **1,059 / 1,029** |
| PER 500 kV stations found / in the single 500 kV component | 15 / 15 | 19 / 19 | 19 / 19 |

**Reading.**
- **S1:** clears the 500 floor by a wide margin in both modes, even with KE excluded and every Day 2 artefact removed. It's still provisional; the gate check is at the end of Day 5.
- **500 kV:** the layer reproduces NGC's own circuit-km to within 0.1% on explicit tags, and it's one connected network.
- **220 kV:** circuit-km sits 3–10% above NGC + KE. Some of the excess is expected, because OSM includes 220 kV IPP ties and lines NGC doesn't own. Inference adds about 820 circuit-km at 220 kV, which puts the inferred build right on the S4 ±10% edge.

## The 220 kV bus count

There are 111 (explicit) or 149 (inferred) 220 kV substation buses, against 61 official grid stations (NGC 49 + KE 12). The Day 2 audit split them as follows:
- about 68 named stations with 220 kV tags, consistent with the 61 official ones plus a few 220 kV yards inside power stations;
- about 35 unnamed polygons where *tagged* 220 kV lines end. These are mostly IPP and plant switchyards drawn as `power=substation`. They're real 220 kV buses, but not NGC grid stations;
- about 31 (Day 2) buses that existed only through inferred line voltages. After the Day 3 fix, 71 buses at 220 kV (all provenances) have only inferred lines.

So the gap to 61 is mostly a definitional difference: OSM substations include plant switchyards, while NGC's count is grid stations. It isn't a topology error. S3 (Day 5) matches only the 69 named NGC stations, so it isn't affected.

## Decision needed (builder mode, before any solve)

- **Explicit-tags mode:** the most defensible. It matches NGC at 500 kV to −0.1% and at 220 kV to +3.4%, but leaves 5,085 km of untagged line out.
- **Inferred mode:** a more complete network (1,827 km left out), but it sits at the S4 ±10% edge at 220 kV.
- **Recommendation:** explicit mode as the scored model, with the inferred build reported alongside as a sensitivity check. Both pass the provisional S1.

## Left for Day 4

- **Dangling ends (262):** try snapping to the nearest line node within a tolerance before giving up.
- **Unknown-voltage lines:** 299 or 706 edges depending on mode. Report the share of each DISCO area affected.
- **Data quirks:** 30 series merges with mismatched circuits, and 16–42 self-loops. Inspect a sample of each.
- **K-Electric:** replace the Karachi bbox rule with an interface definition. Cut at the NGC–KE 500/220 kV interface buses, consistent with TSEP's "Export to KE" load.
- **Islands:**
  - A 230 kV Iran-import island near Jiwani (25.4–25.6°N, 61.2–61.7°E). It's correct; Iran's grid uses 230 kV.
  - A 110 kV Patrind spur, which looks like a tagging slip for 132 kV.
  - Both are outside the main component, so they don't affect S1.
