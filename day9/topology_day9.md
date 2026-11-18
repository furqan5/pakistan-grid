# Day 9: pre-solve declarations, case assembly, first solves (18 Nov 2026)

## Declared and pushed before any solve

- **Short-branch impedance floor (5bcee71).** Line reactance below 1e-4 pu is raised to 1e-4 pu, keeping R/X. The smallest reactance in PGLib's RTE case is 8.8e-5 pu. 96 lines were affected, none longer than 1.8 km.
- **Winter openings by a path rule (5bcee71).** A circuit maps if the path between its two stations passes only through junction buses. 5 of 15 map, taking 7 branches out. "Matiari" is the southern HVDC terminal.
- **Gate: no manual fixes.** Only GridSFM's ladder relaxes the case. Any manual change after the first AC solve is post hoc for H1–H4.
- **Case assembly (4104cfa)** and a summary with **predictions** (3b6fa9f): summer L2, winter L0/AC1.

## Case

- 1,489 buses and 1,852 branches.
- **Summer:** load 28,982 MW, generator Pmax 32,540 MW, HVDC 4,000 MW.
- **Winter off-peak:** load 9,721 MW, generator Pmax 22,254 MW, HVDC 2,000 MW.

## First solves (started 08:12:33 UTC; the first AC solve of the project)

- DC-OPF, AC power flow from a flat start, and AC-OPF were all **LOCALLY_INFEASIBLE**, in both snapshots (`day9/first_solves.log`).
- The script prints only status, time and objective. No holdout quantity was looked at.

## Diagnostics on copies (the scored case is unchanged; `solve/diagnose_*.jl`)

- **Ratings are what bind.** With ratings removed, winter DC-OPF becomes feasible. Summer also needs wider angles.
- **Smallest rating multiplier that makes DC-OPF feasible:** about **6.0 in summer** and **1.64 in winter**. The ladder allows ×1.5 at most before it starts shedding load.
- **The pockets that set it:**
  1. **Chashma.** 1,414 MW of nuclear (C-1 to C-4) and hydro leaves S0987 through a **1.3 km 220 kV section that OSM leaves untagged**. The model treats it as single circuit at 250 MVA, although its own OSM name, "C-1/C-2 PP – Ludewala", belongs to a double-circuit line.
     - The Day 4 carry rule only bridges two-way joints, and this one is a three-way junction.
  2. **Lahore 132 kV.** Manga, Sarfraz Nagar and Bund Road act as a bulk corridor.
     - LESCO's 220/132 kV supply is 1.02× its load.
     - 220 kV links are missing in OSM, among them New Kot Lakhpat–Bund Road (Day 5).
     - So power has to pass through 112 MVA Lynx circuits.
  3. **Kot Addu (KAPCO)** 132 kV lines, plus several smaller 132 kV pockets.
- **The cause** is OSM data gaps (untagged circuits at junctions, missing 220 kV links, unnamed stations), combined with the conservative declared defaults (Lynx 132 kV, single-Rail 220 kV, equal-split load).
- **My pre-solve prediction (L2/L0) was wrong.** The corrected prediction, pushed before the ladder in 7783b78, is summer **L5** and winter **L4**.

## Official ladder (V1/V2)

- **Run:** GridSFM `solve_topo_json.jl`, 08:21–08:39 UTC. Logs are in `day9/ladder_*.txt`, pushed in 841402d.
- **Result:** **no rung solves either snapshot.** DC-OPF solves at L5. AC-OPF is LOCALLY_INFEASIBLE at L0, AC1 and L1–L5. The pipeline warns of a SHUNT_BS_MAX clamp on one bus.
- **AC diagnostic on copies** (`solve/diagnose_ac.jl`). Starting from L5-like relaxations, constraint families were removed one at a time:
  - **Winter** becomes feasible once the shunts are removed.
    - Reactors are fixed at TSEP's 8,211 MVAr nameplate, but model charging is much smaller.
    - At Nokhar 500 kV the reactors are 805 MVAr against 488 MVAr of local half-charging; at Gatti, 643 against 246.
  - **Summer** stays infeasible even without shunts, reactive load, thermal limits or generator Q limits. That is a real-power transfer limit through the pockets above.
- **No assembly fault was found:**
  - the shunt totals and signs match the declared rules (winter −8,065 MVAr net, summer +6,030);
  - per-unit bases are consistent.
- **Verdict:** **V1 and V2 FAIL. Under the signed gate this is a no-go for the build as specified** (`gate/G1_log.md`, G2 section).

## Findings that stand regardless

- **Public data reproduces the EHV skeleton very well:** 500 kV circuit-km within 0.03% of NGC, and booklet line lengths within 2% on most named corridors.
- **It doesn't give a deliverable 132 kV network.** The causes:
  - unnamed stations;
  - circuit counts left untagged at junctions;
  - missing 220 kV links;
  - no conductor data, so the defaults are conservative.
- **Reactors need sizing to the network that is actually modelled.** Taking TSEP's system totals onto a network with about 25% less line charging makes winter AC infeasible.

## Options for Furqan (no model change made)

1. **Stop.** The two-week data gate has done its job, and the findings above are the result.
2. **Repair, labelled post hoc for good.** Use generic rules only, declared and pushed before any re-solve, never pocket-by-pocket fixes. For example:
   - carry a tagged circuit count across a junction when the OSM line names match;
   - size reactors to model charging rather than TSEP's totals;
   - reconsider the 132 kV and 220 kV conductor defaults with evidence.
   
   Every V and H result would then carry the post-hoc label. The test would be a synthetic case and nothing more.
3. **Ask NGC for data.** Use the documented gaps as a concrete request (`requests/data_requests_DRAFT.md`), for example circuit counts and conductors on named corridors, and 220/132 kV station supply in Lahore.

A GridSFM run on the ladder output (the earlier "report-only" option) isn't possible, because no rung produced a solvable case.
