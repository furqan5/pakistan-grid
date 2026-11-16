# Day 6: electrical parameters (17 Nov 2026)

**Scored build: explicit voltage tags.** The rules are in `builder/parameters.json` with reasons in `day6/parameter_rules.md`. They were committed in `747be71` **before** `builder/make_parameters.py` first ran and before any model quantity was computed. The output is `osm/build/explicit/params/` (`summary.md`, `dcline.json`; the CSVs aren't committed). Topology is unchanged from Day 5, so the G1 values stand.

## Results

- **Lines.** 1,761 branches given exact-π parameters.

  | Class | Circuit-km |
  |---|---|
  | 500 kV, quad Drake | 9,310 |
  | 220 kV, single Rail | 12,944 (includes the one OSM 230 kV branch) |
  | 132 kV, Lynx | 23,069 |
  | 66 kV | 2,505 |

  - Two sensitivity tables are written as well: 220 kV twin Rail and 132 kV Rail. They are reported only.
- **Line charging at 1.0 pu: 12,422 MVAr** (500 kV 9,521; 220 kV 1,745; 132 kV 1,126; 66 kV 31). **H2 is reported only.**
  - TSEP prints 17,517 MVAr (summer) and 15,897 (winter off-peak). Those are PSS/E values at solved voltages, for a network that includes K-Electric's 132 kV and the lines OSM lacks.
  - Nothing is changed in response. Changing B, circuits or reactors now would be post hoc for H3.
- **Transformers.** 126 equivalent branches. The commit `2b489ba` message said 127, which counted the CSV header.
  - 54 use PSS 44th unit counts: 15 of 21 at 500/220 kV and 39 of 67 at 220/132 kV. The other 72 use defaults.
  - Totals: 500/220 kV 30,750 MVA; 220/132 kV 35,810 MVA; 500/132 kV 1,000 MVA.
  - **Untuned cross-check:** 500/220 + 500/132 + 220/132 comes to 67,560 MVA, against PER FY2024-25's NGC total of 66,630 MVA (+1.4%). Our figure also includes KE and plant stations, and the PSS units are from 2019, so this is a plausibility check, not a match.
  - PSS stations with no model station: Sialkot, Gujrat, Wapda Town and Loralai, the S3 misses. Their units aren't used.
- **Reactors (nameplate at 1.0 pu).**
  - Summer: 6,162 MVAr placed, **equal** to TSEP.
  - Winter off-peak: 8,211 MVAr placed, **equal** to TSEP.
  - The 846 MVAr of Table 5-9 reactors is placed at S3 buses. The exceptions are Loralai (no bus) and Zhob (not a PER station), whose 120 MVAr goes into the pool.
  - The pool is spread over 52 500 kV station buses. **Exit check met for reactors.** Capacitors are placed on Day 8 by the declared rule.
- **HVDC.** `dcline.json` per snapshot: transfer fixed at 4,000 MW (summer) and 2,000 MW (winter off-peak), loss1 3.4%. That's a dcline loss of 136 and 68 MW, reported next to H1/H4.
- **Winter openings (TSEP Table 5-7).** **2 of 15 map** under the declared rule (direct branch only): Tarbela–Rawat 500 kV, and Kassowal–Vehari 220 kV (1 of 2 circuits opened). The 13 unmapped ones are listed in `summary.md`:
  - **Not matched by name:** the post-2019 stations Maira, Islamabad West, Suki Kinari, Karot and Arifwala, plus Gujranwala (500 kV) and Neelum Jhelum.
  - **"Matiari" is ambiguous:** both converter stations carry it in their OSM name.
  - **No direct branch:** Ghazi Barotha–Gatti, Tarbela–Ghazi Barotha, Moro–RYK and Matiari–Moro all run through tee junctions.

## Expected H3 direction, recorded 17 Nov 2026 before any solve

H3 is scored: winter off-peak net generator Q must be negative (TSEP −800 MVAr). The fixed rules bias it toward failing. This is my arithmetic, written down so that a failed H3 is explained in advance, not afterwards.

- **Less line charging.**
  - Model charging is 12,422 MVAr at 1.0 pu, or about 13,400 MVAr at a typical solved 1.04 pu.
  - TSEP's off-peak charging is 15,897 MVAr, and that figure is *after* its line openings.
  - So the model supplies about **2,500 MVAr less** charging. Causes: lines OSM lacks, K-Electric's 132 kV, and the 132 kV layer generally.
- **More reactor absorption.**
  - Reactors are fixed at TSEP's 8,211 MVAr as nameplate at 1.0 pu.
  - TSEP's figure is already at solved voltages. At about 1.04 pu the model's reactors absorb roughly 8,900 MVAr, about **700 MVAr more**.
  - This pushes in the **same** direction as the charging shortfall: more absorbed by reactors leaves less for the generators to absorb.
- **Net effect.**
  - The surplus is charging minus reactor absorption: TSEP 15,897 − 8,211 ≈ 7,700 MVAr, model 13,400 − 8,900 ≈ 4,500 MVAr. That is about **3,200 MVAr less**.
  - Holding load Q and reactive losses at TSEP's values, generators would absorb that much less. Net generator Q would be about −800 + 3,200 ≈ **+2,400 MVAr**, the wrong sign for H3.
- **Pulling the other way.**
  - 13 of the 15 TSEP winter openings are unmapped, so those lines stay in service and keep their charging. That is several hundred to about 1,500 MVAr, depending on which 500 kV circuits they are.
  - Model reactive losses may differ from TSEP's 4,220 MVAr by thousands, in either direction.
- **TSEP's own balance doesn't close.**
  - Load + KE + reactors − capacitors − charging + losses = +538 MVAr against −800 printed (gap 1,338).
  - In summer the gap is about 5,100 MVAr. HVDC filters are excluded from TSEP's capacitor figure, and that probably explains much of it.
  - So these magnitudes are uncertain to about ±1,500 MVAr.
- **Expectation:** H3 more likely fails than passes. If it does, the cause is the charging shortfall from the incomplete network, not the generator model.
  - **The reactor rule is not changed.** Scaling reactors to model charging would be a change made after seeing charging. It would have to be logged as such, even though it comes before any solve.

## Open before the first solve (Day 9)

These must be declared in writing before any solve. Changing them afterwards is post hoc. Items 1 and 2 are decided on mapping fidelity and numerics only, **without regard to their effect on H3**. Their direction on H3 is now known, so this statement goes in the rule. For item 1, first check how GridSFM's `patch_model.jl` and `solve_topo_json.jl` treat tiny impedances. A minimum-impedance floor keeps the buses unchanged. A merge changes buses, so S1, S3 and S4 would be rerun and reported next to the Day 5 values.

1. **Very short branches.** 194 branches are under 0.5 km, 56 of them at 500 kV. The smallest x is 6e-6 pu. Options:
   - merge buses joined by sub-threshold branches;
   - a minimum impedance floor.
2. **Winter openings mapping.** Keep "direct branch only", which applies 2 of 15, or declare a path-based rule. Either way, decide before the first winter solve. The openings matter for V2 and H3/H4.
3. **Day 7 generator Q rule** (H3 depends on it).
4. **Day 8 capacitor placement** (rule already fixed).

## Waiting on Furqan

- Sign off gate v0.4. Pending items:
  - the S3 60–64 proposal;
  - the H1/H4 loss definition (generation − load, so the dcline loss is included);
  - the AC1 shunt rule;
  - H8.
- Confirm or reject the structural aliases: Safdar Nagar = Sarfraz Nagar, Bandial = Bandala.
