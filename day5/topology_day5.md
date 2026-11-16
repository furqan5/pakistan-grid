# Day 5: S3 station match, PSS line check, HVDC, G1 (16–17 Nov 2026)

**Scored build: explicit voltage tags** (`osm/build/explicit`). The G1 result is in `gate/G1_log.md`; the PSS 44th source checks are in `day5/pss_check.md`.

## Done

1. **PSS 44th downloaded and checked.** Tables were extracted, and defects in the booklet were recorded (`day5/pss_check.md`).
2. **The S3 match rule was fixed before scoring** (gate v0.3 draft, commit `4a02b3f`).
   - The alias table `gate/s3_aliases.csv` covers all 69 stations, each alias with a source.
   - The matcher is `builder/score_s3.py`. It normalises names, matches one to one by maximum bipartite matching, and allows plant buses only for the three plant-switchyard entries.
   - The self-test passed: 129 PER/PSS spellings, 0 failures.
3. **Two builder fixes** (`cbee766`). Topology and reports are unchanged.
   - `stations.csv` gained `all_names`: every name-like tag across all of a station's members. `plants.csv` is now written as well.
   - The station display name was chosen at random when two names tied, because Python's string hashing changes per run. Example: "Siranwali 1" vs "Siranwali 2". The tie-break now uses the name itself, and both builds are byte-identical across reruns.
4. **S3 first run: 62 / 69.**
   - 500 kV: 17 of 20. 220 kV: 45 of 49.
   - **FAIL, above the no-go line.** Details are in `gate/G1_log.md`.
5. **PSS per-line check** (`builder/check_pss_lines.py`, rules committed in `44a10db` before the first run).
   - 72 rows checked; 55 have the OSM path within 10% of the PSS route.
   - **No circuit corrections were needed.**
   - Four missing direct 220 kV links were found and are listed for Day 6.
6. **HVDC.** `dclines.csv` now gives each terminal's AC bus: Matiari `S:S0675@500` ↔ Lahore `S:S0789@500`.

## G1 summary

- **S1:** PASS, 904 / 924.
- **S2:** pending until Days 7–8.
- **S3:** FAIL at 62, in the 60–64 band. The decision rule doesn't cover this band; a proposal waits for Furqan.
- **S4:** PASS. 500 kV is −0.1% from the reference and 220 kV is +3.6%.
- **No-go:** not triggered.
- **Label:** a failed S3 rules out the "Pakistan-calibrated" label under the rule as written.

## Day 6 next

- **Line parameters.** Per-km R, X and B by voltage and conductor class, from documented assumptions; NTDC publishes none. Ratings from the TSEP tables.
- **Topology follow-ups.** These are not gate items; the changes must be rule-based and logged.
  - Look into the four missing 220 kV links: Samundri Road–Nishatabad, New Kot Lakhpat–Bund Road, KSK–Bandala and Peshawar–Nowshera. Check whether the lines are unmapped or mapped without voltage tags.
- **HVDC dcline parameters.** Losses and reactive limits, with sources.

## Waiting on Furqan

- **Sign off gate v0.3**, including three pending decisions:
  - the S3 60–64 proposal, signed after seeing 62;
  - the AC1 shunt rule from Day 1;
  - H8.
- **Three structural aliases to confirm or reject:** Safdar Nagar = Sarfraz Nagar, Bandial = Bandala, Peshawar = Sheikh Muhammadi.
