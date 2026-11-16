# Day 6: electrical parameter rules (fixed 17 Nov 2026, before any Pakistan solve)

All values live in `builder/parameters.json`. This note gives the reasons. The order of work was:
1. These rules were committed first.
2. Only then were any model quantities computed. That includes total line charging, which is reported against H2 only.
3. After the first AC solve, any change to these rules is post hoc for the holdouts.

## Lines (per circuit)

| Class | Conductor | R Ω/km | X Ω/km | B µS/km | rate_a MVA | Why |
|---|---|---|---|---|---|---|
| 500 kV | quad ACSR Drake | 0.0221 | 0.273 | 4.08 | 1,500 | Project documents fix quad Drake/Greeley. 1,500 MVA is the TSEP stability rating of 500 kV Gujranwala–N. Jhelum. |
| 220 kV | single ACSR Rail | 0.0744 | 0.410 | 2.78 | 250 | See below. |
| 132 kV | ACSR Lynx | 0.197 | 0.404 | 2.80 | 112 | See below. |
| 66 kV | ACSR Lynx (assumed) | 0.197 | 0.404 | 2.80 | 56 | No source. Lynx's 490 A at 66 kV. |

- **Where the values come from.** The per-km values are the research report's table (6 Nov 2026). They use datasheet R at 75 °C and assumed tower geometry, cross-checked against the NTDC-attributed IEOM table: X at 500 kV is 0.273 vs 0.277, and at 132 kV 0.404 vs 0.402.
- **Lines with n circuits** get r/n, x/n, b×n and rate×n.
- **Every line uses the exact (hyperbolic) π model.** 27 branches are longer than 150 km.
- **Short-term ratings:** rate_b = 1.1 × rate_a and rate_c = 1.25 × rate_a, as in GridSFM's own files.
- **Odd voltage tags:** OSM's one 230 kV branch takes the 220 kV class, and its one 110 kV branch takes the 132 kV class.
- **No OSM help.** OSM carries no conductor tags, and only 11 of about 2,100 line ways have `wires`. So the class is set by voltage.
- **220 kV is single Rail. The evidence:**
  - TSEP recommends "replacement of existing 220 kV lines of single conductor", so single conductor is the existing norm.
  - Both 220 kV ratings that reconcile in TSEP's contingency tables are 250 MVA (Mardan–Tarbela) and 300 MVA (Sibbi–Quetta). Both are in the single-Rail range: thermal about 345 MVA, against about 690 MVA for twin Rail.
  - The rating used is the pre-written research table value (250), not one picked after seeing the 300.
- **132 kV is Lynx. The evidence:**
  - Of 36 reconciling 132 kV rows in TSEP Tables 5-2/5-4, 23 are rated 112 MVA (Lynx).
  - The NTDC-attributed IEOM "typical 132 kV" row is 175 mm², which is Lynx.
- **The 132 kV conductor is the largest single lever on the loss holdouts H1 and H4.** It covers about 23,000 circuit-km, and Lynx R is 2.6 times Rail's.
  - The Lynx evidence is biased. Contingency tables list overloaded lines, which are the weakest, and the IEOM table is generic.
  - Lynx stays as declared. The **Rail variant** (and twin Rail at 220 kV) is computed and reported **next to** H1 and H4 for comparison, and can never replace the scored result.

## Transformers

- **Branches.** One equivalent branch per voltage pair per station, using the builder's stubs. There are 126 stubs (corrected from 127, which counted the CSV header): 67 at 220/132 kV, 35 at 132/66, 21 at 500/220, 2 at 500/132 and 1 at 132/110.
- **Capacity:**
  - For stations S3 assigned to a PSS 44th station (Tables 2.16/2.17, June 2019), use the PSS units. Units of 450, 600 or 750 MVA go to the 500/220 pair; 160, 250 or 320 MVA to the 220/132 pair.
  - Otherwise use the default.
- **Defaults.** Own-base reactance; R = X / X-to-R ratio.

  | Pair | Units | Own-base X | X/R | Source |
  |---|---|---|---|---|
  | 500/220 kV | 2 × 750 MVA | 10% | 40 | TSEP standard unit, "two initially"; X is the midpoint of 7.5–12% |
  | 220/132 kV | 2 × 250 MVA | 12% | 40 | TSEP standard unit; pandapower 220/110 kV is 12% |
  | 500/132 kV | 2 × 250 MVA | 13% | 40 | research notes, 12–14% |
  | 132/66 kV and 132/110 kV | 2 × 40 MVA | 10% | 30 | **assumption, no source** |

- **Settings.** rate_a = total MVA. Tap 1.0, with a 0.9–1.1 range. Angle limit ±60°.

## Shunts (TSEP input I4)

- **Totals are nameplate MVAr at 1.0 pu.** PSS/E reports MVAr at solved voltages, and TSEP's winter 500 kV voltages are 1.035–1.056 pu, so delivered MVAr will be about 7–11% higher at those buses.
  - That gap is about the size of the −800 MVAr net generator Q that H3 tests. It is reported after the solve and **never iterated away**.
- **Reactors.** Summer 6,162 MVAr; winter off-peak 8,211.
  - The Table 5-9 reactors (846 MVAr; read by eye from PDF p.68) are placed at their S3-assigned buses. Any without a bus join the pool.
  - The rest go to 500 kV station buses in proportion to half the charging of their incident 500 kV circuits.
- **Capacitors.** Summer 12,192 MVAr; winter off-peak 146.
  - They go to 132 kV load buses in proportion to reactive load, placed on **Day 8** once loads exist.
  - **The Day 6 exit check is therefore split:** reactor totals are checked today and capacitor totals on Day 8.

## Buses

- vmin 0.95 and vmax 1.08 pu. This is TSEP's grid-code criterion for normal operation: +8% / −5% up to 500 kV.
- It is declared now, not left to the Day 9 fix list, because a change after the first solve would be post hoc.

## HVDC (Matiari–Lahore, ±660 kV, 4,000 MW)

- **Terminals.** Matiari converter `S:S0675@500` to Lahore converter `S:S0789@500`.
- **Transfer is fixed per snapshot:**
  - summer 4,000 MW (TSEP p.34, I3);
  - winter off-peak 2,000 MW. TSEP Figure 5-9 is annotated "Power Flow on Matiari-Lahore HVDC Link = 2000 MW" (PDF p.70). This value is added to I3.
- **Losses.** loss1 = 3.4% of transfer, loss0 = 0. NTDC reported an actual T&T loss on the PMLTC line in November 2024 of 19.528 GWh = 3.391% ([Express Tribune, 8 Jan 2025](https://tribune.com.pk/story/2520733/entertainment)). NEPRA allows up to 4.3% ([Business Recorder, 10 Mar 2018](https://www.brecorder.com/news/amp/4583804)).
  - The November figure is at partial loading, so the split between fixed and variable loss is unknown.
  - The dcline loss is reported as its own line next to H1.
- **Reactive range** at each terminal: ±200 MVAr. **Assumption:** LCC terminals with switched filters.

## Winter line openings (TSEP Table 5-7)

- The 15 circuits are listed in `parameters.json` and applied to the winter off-peak snapshot only, on direct branches between the mapped buses.
- Matiari–Moro and Moro–RYK depend on the doubtful Moro pairing (S0690, "Moro Converter Station").
- Several endpoints are post-2019 stations (Maira, Islamabad West, Suki Kinari, Karot). They may be unmapped; they are listed, not guessed.

## Topology follow-ups from Day 5 (diagnosed, not changed)

- **Samundri Road–Nishatabad:** no 220 kV way near either station. Only 132 kV ways and one 8 km untagged way near Nishatabad.
- **New Kot Lakhpat–Bund Road:** an untagged 12 km way (561025264) leaves New Kot Lakhpat and ends 3.8 km short of Bund Road. It's partly mapped, so not even voltage inference connects it.
- **KSK–Bandala and Peshawar–Nowshera:** no candidate way was found.
- **Decision:** the model is not changed. Adding lines from 2019 data would also re-add lines that have since been rerouted, such as Port Qasim into Matiari. These gaps stay as known limitations.
