# Day 4 — Dangling ends, K-Electric interface, data quirks (16 Nov 2026)

**Scored build: explicit voltage tags** (`osm/build/explicit`, decided 16 Nov). Inferred-build numbers are given only as sensitivity.
The Day 3 reports are kept in `osm/build/day3/`. New per-build outputs are `snaps.csv` and `quirks.csv`.

## Changes

1. **Dangling-end snapping** (`config.dangling_snap`).
   - Applies to a way end that is not inside a station or plant, not shared with another way, and has no voltage-compatible station within 1 km. Such an end is:
     - joined to the nearest node of **another** line with a compatible voltage within **150 m**, splitting that line there; or, failing that,
     - joined to another such dangling end within **500 m** (the gap length is ignored).
   - Result: **78 snapped to a line + 4 gaps bridged**. Snap distance median 80 m, maximum 409 m (gap bridges).
   - Dangling endpoints fell 262 → 180, and components 29 → 24 in the explicit build.
2. **Circuits across series joints.** When one side of a joint is untagged (default 1 circuit) and the other side is tagged, the tagged count carries across. Before, the minimum was taken.
   - 25 of the 30 mismatches were this case: an untagged segment next to a double-circuit tagged section.
   - Effect: 132 kV +479 circuit-km, 220 kV +27, 500 kV +2.
3. **K-Electric region** (`config.ke_region`, a working definition, [VERIFY]):
   - buses at ≤220 kV inside 24.55–25.90°N, 66.30–67.70°E;
   - excluding stations whose operator says NTDC/NGC/WAPDA.
   - The east edge was first 67.85°E. That cut through the Gharo–Jhimpir wind corridor and reported six wind-farm 132 kV yards (67.82–68.01°E) as KE interface points, so it was moved to 67.70°E.

## Results (explicit = scored)

| | Day 3 explicit | **Day 4 explicit** | Day 4 inferred (sensitivity) |
|---|---|---|---|
| Dangling endpoints | 262 | **180** | 180 |
| Components | — | **24** | 18 |
| Main-component buses | 1,467 | **1,489** | 1,794 |
| 500 kV circuit-km (NGC 9,313) | 9,308 | **9,310 (−0.03%)** | 9,451 |
| 220 kV circuit-km (NGC + KE ≈ 12,400) | 12,819 | **12,846 (+3.6%)** | 13,763 (+11%) |
| 132 kV circuit-km | 22,585 | **23,064** | 25,314 |
| **Provisional S1** with KE / without KE | 912 / 896 | **924 / 904** | 1,089 / 1,052 |
| PER 500 kV stations found | 19/20 | 19/20 | 19/20 |

## K-Electric

- **KE buses in the main component, explicit build:**
  - 220 kV: 13 substations, against PER's 12 KE 220 kV grid stations.
  - 132 kV: only **6 substations against PER's 62**.
- **Why so few:** OSM's KE 132 kV layer mostly lacks voltage tags. 566 km of untagged line (11% of all untagged km) lies inside the KE box. KE is a gap in the scored build; that's a data limitation, not a builder fault.
- **Interface edges (KE ↔ rest), 10 in the explicit build. These carry TSEP's "Export to KE" (I2):**
  - 220 kV: N.K.I → KE junction; Baldia (NTDC-tagged) → KE; Jhimpir II → K.D.A-33 (84.6 km); two unnamed 220 kV ties (69.4 and 43.6 km).
  - The Port Qasim 500/220 kV yard (S1055), via its transformer.
  - 132 kV:
    - Baldia → Tapal Energy;
    - Uthal (S0589, 25.84°N) → a station near Bela (S0588, 26.20°N), 52.6 km. This may be a KE–QESCO boundary line, [VERIFY];
    - two unnamed ties.
- **Gate consequence:** S1 is reported with and without KE, and both are far above the 500 floor. For the TSEP balance, KE is a load of 2,050 MW (summer) / 1,001 MW (winter off-peak) spread over these interface buses (I2).

## Quirks reviewed

- **Self-loops: 16, 6.6 km in total, all at station buses.** These are short yard loops (a line leaving and re-entering the same station, at most 0.95 km). Dropping them is correct.
- **Circuit mismatches: 30.** Handled by change 2. The rest are genuine tag disagreements (for example 1 vs 2 circuits, both from `cables/3`); the smaller count is kept.
- **Untagged lines (5,131 km, left out of the scored build):** spread across the country, not concentrated. Largest 1° cells:
  - 31°N 73°E, Faisalabad: 435 km;
  - 24°N 67°E, Karachi: 380 km;
  - 33°N 72°E: 296 km;
  - 25°N 67°E: 285 km;
  - 31°N 72°E: 265 km;
  - 31°N 74°E, Lahore: 261 km;
  - 30°N 71°E, Multan: 260 km.

## Status against the gate's structure checks (provisional, scored build)

- **S1** (≥500 ≥66 kV buses at real stations in the main component): **904 without KE / 924 with KE**. Comfortably above the floor.
- **S3** (≥65 of 69 NGC stations matched by name): not yet run, Day 5. The 500 kV half is at 19/20, three of them via [VERIFY] location hints.
- **S4** (circuit-km within ±10%): 500 kV −0.03%, 220 kV +3.6%. Within the band.
- **S2** (≥98% of load and generation in the main component): needs the Day 7–8 generator and load placement.

## Day 5 next

- **S3:** match all 69 NGC station names from PER FY2024-25 Figure 1. The 49 at 220 kV need aliases and location checks.
- **S4 refinement:** correct circuits on named lines against the PSS 44th edition line tables. That needs the PSS file, still waiting on Furqan's decision about the mirror.
- Exclude 765 kV and under-construction assets, which are already dropped as lifecycle tags. Add the HVDC link as a PowerModels `dcline`.
- Run G1 (S1–S4) and log the result.
