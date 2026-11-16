# Pakistan synthetic grid for a GridSFM test — pre-registered gate

**Status: DRAFT v0.4, 17 Nov 2026 (v0.3: 16 Nov; v0.2: 6 Nov). Not yet approved by Furqan.** v0.3 added the S3 match rule. v0.4 adds the winter HVDC input and a proposed loss definition for H1 and H4. Neither version changes a threshold.
v0.2 adds no threshold changes. Every TSEP and NEPRA number in this file was checked by eye against the source PDFs (`day0/tsep_check.md`, `day0/per_check.md`). The S3 name list is PER FY2024-25 Figure 1 (69 stations). It becomes binding only once he signs it off.
Any edit before the first Pakistan AC solve is allowed but gets a new dated commit. After the first Pakistan AC solve, changes are logged and the affected holdouts are reported as "post hoc".

The source is `E:\Startup\reports\Pakistan grid model data.md` (Verdict section). The Day 0 by-eye checks of TSEP are in `day0/tsep_check.md`.
The thresholds were designed in that report, not taken from a source, except where a reference is named.

## Snapshots (fixed)

- **Summer peak:** TSEP 2024-34 base case, July/August 2026 (Table 5-1).
- **Winter off-peak:** TSEP 2024-34 base case, January 2027 (Table 5-10), with the Table 5-7 line openings applied.
- Both are NTDC **planning forecasts, not observations**.

## Model build choice (fixed before the first Pakistan solve)

- **Scored model:** the explicit-voltage-tags OSM build (`osm/build/explicit`). Decided by Furqan on 16 Nov 2026.
  - The inferred-voltage build is reported as a sensitivity case only. Its results can't replace a failed scored check.
  - Day 3 values on the scored build: provisional S1 896 (without KE) / 912 (with KE); 500 kV 9,308 circuit-km; 220 kV 12,819 circuit-km.

## Inputs (set from the sources; matching them proves nothing)

| ID | Summer peak | Winter off-peak | Source |
|---|---|---|---|
| I1 | Load 27,097 MW / 16,017 MVAr (PF ≈ 0.861) | Load 8,774 MW / 4,082 MVAr (PF ≈ 0.907) | TSEP T5-1, T5-10 |
| I2 | KE export 2,050 MW / 795 MVAr | KE export 1,001 MW / 68 MVAr | TSEP T5-1, T5-10 |
| I3 | HVDC Matiari–Lahore 4,000 MW | 2,000 MW (added 17 Nov 2026) | TSEP p.34 text; winter: Figure 5-9 annotation, PDF p.70 |
| I4 | Reactors 6,162 MVAr; capacitors 12,192 MVAr | Reactors 8,211 MVAr; capacitors 146 MVAr | TSEP T5-1, T5-10 |
| I5 | DISCO shares from Table 2-1 (2026-27 column), scaled to I1 | same shares, scaled to I1 | TSEP T2-1 |

## Structure checks (Day 5)

| ID | Check | Pass | Reference | On failure |
|---|---|---|---|---|
| S1 | AC buses at ≥66 kV in the main component, each tied to a real OSM substation, plant switchyard or converter. Line-ending nodes, degree-2 junctions and 11 kV buses do not count. | **≥ 500** | GridSFM floor | **No-go** at end of Day 5: switch to the PyPSA-Earth route or wait for NGC data |
| S2 | Share of load and of installed generation in the main component | ≥ 98% each | design | Fix islands |
| S3 | NGC 500/220 kV stations matched by name | ≥ 65 of 69 | NEPRA PER FY2024-25 | **No-go** if < 60 |
| S4 | Model circuit-km at 500 kV and at 220 kV (NGC + KE) | within ±10% of ≈ 9,320 and ≈ 12,400 | NEPRA PER FY2024-25 | Correct circuits before solving (calibration, not a holdout) |

### S3 match rule (added 16 Nov 2026, v0.3 draft, fixed before S3 was first scored)

- **Reference list.** The 69 stations of PER FY2024-25 Figure 1 at their PER voltage: 20 at 500 kV, 49 at 220 kV.
- **Aliases.** `gate/s3_aliases.csv` gives each station's aliases with a source for each.
  - The sources are PER Figure 1, the PSS 44th station and line tables, and plain abbreviation expansions (FSD = Faisalabad, T.T. = Toba Tek, and so on).
  - Three aliases rest on the structure of the two lists, not on a document that states the equivalence: Peshawar ↔ Sheikh Muhammadi, Safdar Nagar ↔ Sarfaraz Nagar and Bandial ↔ Bandala. They are marked "structural [VERIFY]".
  - **What OSM names were already seen.** The table was written from the documents, but the 500 kV half isn't blind:
    - The Day 3 backbone check had already shown OSM names such as "Faisalabad West", "New Dadu" and "Sahiwal", with 500 kV at 19 of 20 by the Day 3 aliases.
    - The Day 4 K-Electric section printed some 220 kV names: N.K.I, Baldia and Jhimpir II.
    - No other 220 kV OSM name was looked at.
    - The bare alias `sahiwal` was left out on purpose. Every other row keeps the station part of a compound PSS name and drops the city; for Yousafwala, `sahiwal` would have turned a known location hint into a name match.
  - The table isn't edited after scoring. Any later change is reported as post hoc.
- **Self-test.** `python builder/score_s3.py --selftest` must pass before scoring. Every station has to match its own PER spelling and every PSS spelling quoted in its source column. On 16 Nov it passed: 129 spellings, 0 failures.
- **Candidates.** Buses of the scored build (`osm/build/explicit`) at the station's PER voltage:
  - Substation and converter buses can be matched to any station.
  - Plant buses can be matched only to the three PER entries that are plant switchyards: TPS M.garh, S.Y. Guddu and NGPS.
- **Names compared.** Every `name`, `name:en`, `alt_name`, `official_name`, `old_name` and `short_name` value across all OSM members of the station or plant (`all_names` in `stations.csv` and `plants.csv`).
  - Name counts before scoring (scored build, main component):
    - 220 kV: 68 station buses carry a Latin-script name and 41 carry none.
    - 500 kV: 23 named, 24 unnamed.
    - No candidate has a non-Latin name only.
  - Unnamed stations can only be found by location hint, so they don't count toward the scored S3.
- **Name normalisation**, applied the same way to both sides:
  1. lower-case and fold accents;
  2. turn punctuation into spaces and split into words;
  3. merge runs of single letters ("N. K. I" → "nki");
  4. map lone roman numerals i–iv to 1–4;
  5. inside each word, drop an "h" that follows a consonant and collapse doubled letters ("Ghakkar" and "Gakhar" both → "gakar").
- **Name match.** An alias matches a bus name if every word of the alias appears as a whole word in the name. It also matches if the alias, with spaces removed, is at least 6 characters long and appears inside the name with spaces removed.
- **One to one.** Each bus can serve at most one station at a given voltage. The S3 count is the size of the maximum bipartite matching between stations and buses.
- **Scored S3 = name matches only, to buses in the main component.** The gate says "matched by name".
  - These are reported but don't count:
    - name matches anywhere in the build;
    - near-misses, meaning one edit within a word of 5 or more letters;
    - location hints from `builder/config.json`.
  - A hint never counts toward the scored S3.
- **Output.** `s3_report.md` and `s3_matches.csv` in the build folder list, for every station:
  - the bus assigned;
  - the alias and OSM name that matched;
  - the tier;
  - the coordinates;
  - whether a structural alias was used.
  
  The report also states how many scored matches rely on a structural alias. Doubtful pairs are reported, never removed.
- **Proposed, needs sign-off.** The decision rule doesn't say what happens when S3 lands between 60 and 64, which fails the ≥65 pass mark but is above the no-go line. Proposal: treat it like a failed scored holdout. The test is relabelled "synthetic Pakistan-topology" and the build continues.

## Solvability (Day 10)

| ID | Check | Pass | On failure |
|---|---|---|---|
| V1 | GridSFM `solve_topo_json.jl` ladder rung reached at summer peak | L0, AC1, L1 or L2. L3 only with a logged root cause. L4/L5 (load shed) fails. | **No-go** at end of Day 10 |
| V2 | Same at winter off-peak with the Table 5-7 openings | L2 or better | as V1 |

## Holdouts (computed once, on Day 11, against these thresholds)

| ID | Quantity | Pass | Reference | Role |
|---|---|---|---|---|
| H1 | Summer-peak MW losses ÷ generation | 2.0–5.0% (TSEP 3.4%) | TSEP T5-1 | **scored** |
| H2 | Summer line charging (TSEP 17,517 MVAr) | — | TSEP T5-1 | **reported only**. Day 0 check: TSEP does not print its 2026 circuit-km by voltage, so it can't be normalised without leaking. |
| H3 | Winter off-peak net generator Q | negative (TSEP −800 MVAr) | TSEP T5-10 | **scored** |
| H4 | Winter off-peak MW losses ÷ generation | 1.0–3.5% (TSEP 2.1%) | TSEP T5-10 | **scored** |
| H5 | Rank of the Gatti 500/220 kV bank among 500/220 kV banks at summer peak | top quartile | NEPRA PER 2023-24 | reported only |
| H6 | Multan, D.G. Khan and Guddu 747 voltages at winter off-peak | in top third of 500 kV bus voltages | NEPRA PER 2023-24 Table 13 | reported only |
| H7 | Voltages and flows at buses name-matched to World Bank Annex 2 | median V error and flow-sign agreement reported; no pass mark (different years) | WB Annex 2 (2021) | reported only |
| H8 | *(proposed on Day 0, needs sign-off)* 20 key 500 kV bus voltages at winter off-peak | median abs. error reported; no pass mark (values read by eye from a plot, ±0.003 pu) | TSEP Fig 5-8 | reported only |

### Loss definition for H1 and H4 (proposed 17 Nov 2026, v0.4 draft, needs sign-off)

- **TSEP's losses are generation minus load minus KE export.** Its balances close exactly:
  - summer: 30,180 = 27,097 + 2,050 + 1,033;
  - winter off-peak: 9,982 = 8,774 + 1,001 + 207.
  
  So TSEP's losses include any HVDC loss.
- **Proposal.** Compute model losses as (Σ generator P − Σ load P) / Σ generator P, with KE export counted as load. Shunt conductances are zero, so they don't enter.
  - The dcline loss is then included automatically.
  - It is also reported as its own line next to H1 and H4.
- **Parameters.** These are fixed in `builder/parameters.json` before the first solve: lines, transformers, shunt rules, bus limits 0.95–1.08 pu, and the HVDC set-points and losses. Reasons are in `day6/parameter_rules.md`.
  - The 132 kV Rail variant is reported next to H1 and H4 for comparison only. It can't replace the scored result.

## Decision rule

- **Go: "Pakistan-calibrated" GridSFM test** if S1–S3, V1–V2 and the scored holdouts H1, H3 and H4 all pass.
- **Go, relabelled: "synthetic Pakistan-topology" test** if any scored holdout fails. No retuning is allowed, and the NGC data request is escalated.
- **No-go for the build:**
  - S1 fails, or S3 is below 60, at the end of Day 5; or
  - V1 or V2 needs L4 or L5 at the end of Day 10.

## G4 — GridSFM zero-shot comparison (Day 12)

- **Metrics against the Ipopt AC-OPF solution of the same scenario:**
  - objective gap (%);
  - bus voltage-magnitude MAE (pu);
  - branch-flow error (MW);
  - share of buses and branches violating limits;
  - agreement of the feasibility flag.
- **Scope:** report each metric for the whole grid, the 500/220 kV subset and the 132 kV subset separately.
- **Scenarios:** use the base snapshots plus scenarios from `gen_perturbed_data.jl`. Fix the count on Day 11 before running.
- **Costs:** convert to USD at a dated exchange rate, recorded here before the run (rate: ____ on ____).
- **Comparison:** use GridSFM's published in-distribution errors for grids of similar size [VERIFY: figures still to be collected].
- **Interpretation:** good EHV accuracy combined with bad 132 kV accuracy points to the synthetic 132 kV layer, not to Pakistan.

## Sign-off

- [ ] Furqan approved this version (date: ______). Edits: ______
