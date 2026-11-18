# Day 9: expectations written before any solve (18 Nov 2026)

This file is committed and pushed **before** the first DC or AC solve. Its purpose is to put my predictions on record ahead of the results, so a failure can't be explained after the fact. Nothing in it changes a rule.

## Case as assembled (`builder/assemble_case.py`, commit 4104cfa)

- 1,489 buses and 1,852 branches (main component).
- **Summer peak:**
  - 99 generators on, 32,540 MW Pmax;
  - load 28,982 MW (DISCO 26,932 + KE export 2,050);
  - HVDC fixed at 4,000 MW.
- **Winter off-peak:**
  - 109 generators on, 22,254 MW Pmax;
  - load 9,721 MW;
  - HVDC 2,000 MW;
  - 7 branches out, from 5 of the 15 TSEP openings mapped by the path rule.
- **Impedance floor:** 1e-4 pu, applied to 96 lines.

## Deliverability (summer)

Transformer capacity into each DISCO group's 132 kV buses, plus 132/66 kV generation, divided by the group's net load MVA:

| Group | Ratio |
|---|---|
| GEPCO | **0.97** |
| LESCO | **1.02** |
| MEPCO | 1.35 |
| QESCO | 1.41 |
| IESCO | 1.49 |
| PESCO+TESCO | 1.61 |
| FESCO | 1.99 |
| SEPCO | 2.06 |
| HESCO | 3.82 |

132 kV ties between groups are not counted, so GEPCO and LESCO can draw on neighbours, but only over 112 MVA Lynx circuits.

## Predictions

1. **Summer V1.**
   - **L0 (strict) may be infeasible.** The likely binding limits are the 220/132 kV transformers around Lahore and Gujranwala (defaults or PSS 2019 units) and 112 MVA Lynx circuits near load centres and the Jhimpir wind collectors.
   - **Most likely winning rung: L2** (ratings ×1.2), which is still a V1 pass.
   - **Risk: L3**, which needs a logged root cause.
   - **L4/L5 (load shedding) is not expected.** The deliverable generation margin is about 1.4 GW.
2. **Winter V2.**
   - Load is low, so ratings shouldn't bind. Expected **L0 or AC1**.
   - Voltages will sit high, and generators will absorb Q.
   - If AC1 wins, the injected shunts are recorded under the 5% rule.
3. **H3 (scored, computed only on Day 11).** I expect it to **fail**: net generator Q positive, roughly +1,000 to +2,500 MVAr, against TSEP's −800. The arithmetic is in `day6/topology_day6.md`.
   - Two things pull towards a pass: 5 of the 15 openings are now applied, and the winter Pmax pattern differs from TSEP's.
4. **H1 (scored).** Summer losses are probably within 2–5% of generation. 132 kV Lynx is resistive, while the network is shorter than the real one. Low confidence.
5. **AC power flow from a flat start may not converge.** If so, that is recorded, not fixed. The ladder's AC-OPF is the gate's measure, not the plain power flow.

## Addendum, 18 Nov 2026, after the first solves and BEFORE the official ladder runs

- **My pre-solve prediction was wrong.** I expected summer at L2 and winter at L0 or AC1.
- **What happened.** Every first solve was infeasible (`day9/first_solves.log`): DC-OPF, AC power flow and AC-OPF, in both snapshots.
- **DC diagnostics on copies** (`solve/diagnose_*.jl`; the scored case is unchanged):
  - **Binding constraints:** branch ratings.
  - **Smallest rating multiplier that makes DC-OPF feasible:** about **6.0 in summer** and **1.64 in winter**. The ladder's largest multiplier before load shedding is ×1.5 (L3).
  - **The pockets that set it:**
    - Chashma's 1,414 MW leaves through a 1.3 km 220 kV section that OSM leaves untagged, so the model treats it as single circuit (250 MVA).
    - Lahore's 132 kV network (Manga, Sarfraz Nagar) is used as a bulk corridor: 220/132 kV supply is 1.02× load and 220 kV links are missing in OSM.
    - Kot Addu/KAPCO's 132 kV lines.
- **New prediction for the official ladder:**
  - **summer: L5** (no thermal limits). Even with load capped at 70%, ×1.5 is below what's needed.
  - **winter: L4** (load cap 70% with ×1.5).
  - Both are a **no-go for the build** under the signed gate.
- **No repair is made.** Any fix would be chosen after reading flows. Whether to repair, labelled post hoc, is Furqan's decision.
