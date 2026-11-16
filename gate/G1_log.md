# G1: structure checks at the end of Day 5 (16 Nov 2026)

**Scored build:** `osm/build/explicit` (explicit voltage tags), OSM snapshot 2026-11-06T18:19:47Z.
**Gate:** `gate/PREREGISTRATION.md` DRAFT v0.3, **still unsigned by Furqan**.

**Order of commits:**
1. S3 match rule and alias table committed **before** S3 was first run (`4a02b3f`).
2. First S3 run committed (`10e4656`).
3. PSS line-check rules committed before their first run (`44a10db`).

| Check | Pass mark | Result | Status |
|---|---|---|---|
| S1: ≥66 kV buses at real stations, main component | ≥ 500 | 904 without KE, 924 with KE | **PASS** |
| S2: share of load and generation in the main component | ≥ 98% each | needs Day 7–8 generator and load placement | **pending** |
| S3: NGC stations matched by name (PER FY2024-25 Fig. 1) | ≥ 65 of 69; no-go < 60 | **62 of 69** (500 kV 17/20, 220 kV 45/49) | **FAIL, above no-go** |
| S4: circuit-km, NGC + KE | ±10% of ≈ 9,320 / ≈ 12,400 | 500 kV 9,310 (−0.1%); 220 kV 12,846 (+3.6%) | **PASS** |

**Day 5 no-go:** not triggered. S1 passes and S3 is at least 60.

**These are the recorded G1 values.** If a later rebuild changes buses or components (for example the Day 6 topology follow-ups):
- rerun S1, S3 and S4;
- report the new values next to these, never in their place.

Any S3 change caused by a station-grouping change is post hoc and must be labelled that way. An example is merging an unnamed 220 kV yard into a nearby named 132 kV station, which would turn the Sialkot or Loralai misses into hits.

## What the S3 failure means

- **Calibrated label ruled out.** Under the decision rule as written, "Go: Pakistan-calibrated" needs S1–S3 to pass. A failed S3 rules that label out, whatever V1–V2 and the holdouts show later.
- **The 60–64 band.** The gate text doesn't cover a result between 60 and 64. The v0.3 proposal (committed before scoring) is to treat it like a failed scored holdout: relabel the test "synthetic Pakistan-topology" and keep building.
  - That is **Furqan's decision**, and he would be signing it **after seeing 62**. G1 doesn't apply it.
- **Margin.** Two of the 62 scored matches rely on structural [VERIFY] aliases: Safdar Nagar ↔ "Sarfraz Nagar" and Bandial ↔ "Bandala".
  - If both are wrong, S3 is 60.
  - One more wrong pair would take it below the no-go line.
- **The 7 misses** (`osm/build/explicit/s3_report.md`):
  - **Rawat and 747 Guddu, 500 kV:** the yards exist in the model but are unnamed in OSM. They're found only by the [VERIFY] location hints.
  - **TPS M.garh, 500 kV:** the builder merged it into the Muzaffargarh station, 0.7 km away. This is a modelling question and was not changed because of S3.
  - **Sialkot, Gujrat and Loralai, 220 kV:** the OSM station carrying the name has only a 132 kV bus.
    - Dated diagnostics (not used, not added as hints): an unnamed 220 kV yard lies 7.5 km from Loralai (S0731), and "Sahowala" (S0312) lies 8.9 km from Sialkot.
    - Gujrat has only 220 kV line junctions about 10 km away.
  - **Wapda Town, 220 kV:** no OSM station carries the name at any voltage.
- **Reported-only tiers.**
  - Name matches anywhere in the build: 62, the same as the scored count.
  - Names plus hints plus near-misses: 64.
  - The first run showed 65 here. That run's near-miss code also accepted identical generic words, which paired TPS M.garh with the Port Qasim coal plant. It was fixed to "exactly one edit", as the written rule says. The scored count didn't change.
- **Same result on the final build.** The Day 5 builder changes didn't alter `buses.csv`. The SHA-256 is unchanged after the dcline change, so S3 = 62 holds for the final Day 5 build.

## S4 and the PSS 44th per-line check (`osm/build/explicit/pss_line_check.md`)

- **Coverage.** 72 of the 138 usable PSS rows (2019 data) could be checked: both endpoints mapped to buses of the build. The rest have a plant endpoint OSM doesn't name, an ambiguous endpoint, or a three-ended name.
- **Where both ends mapped, the OSM path matches the PSS route closely.** 55 of 72 rows are within 10%. Many are within 2%: Multan–Yousafwala 161.7 vs 161 km, NKI–Jamshoro 155 vs 156, Muzaffargarh–Guddu 257.5 vs 256.
- **No circuit corrections.** All 29 checked double-circuit rows (27 distinct corridors) already carry at least 2 circuits on every hop in OSM, from `circuits` or `cables` tags. The correction rule changed nothing, so S4 stays as above.
- **Paths much longer than the PSS route.** These are not gate items; they are topology follow-ups for Day 6.
  - **Direct links absent from the 220 kV layer of both builds.** For each, there is no dangling 220 kV end within 97 km of either station. In the model, Nishatabad 220 kV has only one line, 2 km to Gatti. Not yet ruled out: the line is mapped in OSM but has a wrong voltage tag, or it ends at an adjacent polygon. Day 6 checks both.
    - Samundri Road–Nishatabad: 23 km route, OSM path 177 km.
    - New Kot Lakhpat–Bund Road: 18 km route, path 80 km.
    - KSK–Bandala: 101 km route, path 398 km.
    - Peshawar–Nowshera: 50 km route, path 82 km.
  - **Probably changed since 2019.** OSM line names indicate that Port Qasim–Jamshoro (132 vs 226 km) and Port Qasim–Dadu (285 vs 336 km) now run into the Matiari converter ("Port Qasim CFPP – Matiari I & II") [VERIFY].
  - **PSS-side inconsistency.** Multan–T.T. Singh is listed twice, at 82 and 65 km, but the stations are 137 km apart in a straight line. Neither row can be a full Multan–T.T. Singh route.
- **Checks on the doubtful scored pairs.** These are reported only; no pair was removed.
  - **Sarfraz Nagar (S0115):**
    - It fits two of its three PSS lines: New Kot Lakhpat 47 vs 46 km, New Okara 80 vs 80 km.
    - It sits 1.8 km from New Lahore (S0705), yet PSS lists an 86 km Sarfraz Nagar–New Lahore line. OSM has a 96 km path between them.
    - This checks the PSS name against the OSM position. It doesn't settle whether PER's "Safdar Nagar" is the same station.
  - **Bandala (S0237):** consistent with Bandala–Gatti, 28 vs 31 km.
  - **Moro (S0690), named "Moro Converter Station" in OSM:**
    - Jamshoro–Moro is 202.8 vs 202 km.
    - Dadu–Moro is borderline: path 54.5 vs 45 km route; straight line 47.8 km, under the 1.1× "too far" flag.
    - The builder labels it a converter only because of its OSM name. It is not an HVDC terminal: the only dcline is Matiari ↔ Lahore.

## HVDC

- `dclines.csv` now gives each DC terminal's AC bus: Matiari converter `S:S0675@500` ↔ Lahore converter `S:S0789@500`, 887 km, ±660 kV. Both buses are in the main component.
- TSEP's summer transfer of 4,000 MW is input I3.
- Losses, reactive limits and the winter set-point are Day 6 work.
