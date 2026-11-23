# Repair round 1: post hoc, declared 23 Nov 2026 before any repaired build or solve

On 18 Nov the case as specified failed V1 and V2: no ladder rung solved. That is a no-go under the signed gate (`gate/G1_log.md`, G2). On 23 Nov Furqan chose **"Repair, post hoc"**. This file declares the repair before it is built or solved. It is pushed to GitHub before any run that uses it.

## Status of everything that follows

- These rules were **chosen after reading the Day 9 diagnostic flows**. Every V and H result from this case is labelled **"repair round 1, post hoc"**, permanently. None can support the "Pakistan-calibrated" label.
- **The as-specified case is kept.** It stays in `params/` and `case/`. The repair writes to `params_r1/` and `case_r1/`.
- **Stopping rule:**
  - This is **one round**: one rebuild and one ladder run.
  - If V1 or V2 still fails, the failure is recorded and the work **stops**. A round 2 needs Furqan's explicit go.
  - After the ladder, the DC rating-multiplier diagnostic runs once, as a report only. It doesn't feed any new rule.
- **H3 (winter generator Q) is not assessable after the repair.** The reactor change (RP3) moves it in the passing direction, so post-repair H3 isn't a test of the model's reactive balance. It will be reported as **"not assessable"**, neither pass nor fail.

## Rules (`builder/repair_r1.py`; listing in `day9/repair_r1_listing.md`)

### RP1: circuit count by OSM name containment

- **Rule.** A branch adopts the higher circuit count of an adjacent same-voltage branch (sharing a junction end) when its OSM name contains that branch's full name. This follows OSM's "X (parent line)" naming convention.
- **Disclosure.** I wrote this rule after seeing the Chashma bottleneck, and it reaches **exactly two branches, both at Chashma:**
  - "C-1/C-2 PP – Ludewala (Chashma PP – Ludewala)", 1.34 km;
  - "C-3/C-4 PP – Ludewala (Chashma PP – Ludewala)", 0.46 km.
  
  Both go from 1 to 2 circuits. **In effect it is a targeted fix for one pocket, and it's reported as one.**
- **Rejected draft.** A broader version (≤2 km junction spans take the summed circuits of the adjacent branches) would have reached 51 spans. The listing showed it would also raise genuine crossings and loop-ins (Tarbela–Burhan III & IV 2 → 4; the KSK–Mangla loop-ins 1 → 3), so it was dropped before declaration.

### RP2: three missing 220 kV links from PSS 44th

- **Rule.** Add PSS 44th lines whose OSM path at that voltage is more than **2×** the PSS route, and whose endpoints are not "too far" apart, as synthetic branches. Each is double circuit, at the PSS route length, with the declared 220 kV class parameters.
- **The three lines:**

  | Line | PSS route | OSM path |
  |---|---|---|
  | Samundari Road–Nishatabad | 23 km | 177 km |
  | New Kot Lakhpat–Bund Road | 18 km | 80 km |
  | KSK–Bandala | 101 km | 398 km |

- **Disclosure.** The 2× cutoff was set after seeing these ratios. It **excludes** two lines:
  - Port Qasim–Jamshoro (1.71×), which OSM line names show was rerouted into Matiari;
  - Peshawar–Nowshera (1.65×).
  
  The three added lines are **2019 data** and may have been re-looped since.

### RP3: reactors capped at local line charging

- **Totals.** TSEP's reactor totals are kept: 6,162 MVAr in summer, 8,211 MVAr in winter off-peak. Table 5-9's fixed reactors are kept.
- **Pool.** The rest goes to 500 **and 220 kV** station buses, in proportion to the local half-charging of the 500/220 kV circuits at each bus.
- **Cap.** No bus gets more reactor than its local half-charging, its fixed reactor included. Any excess is **left unplaced and logged**, never redistributed.
- **No TSEP ratio is imported.** The only change from the declared rule is a physical bound: a bank larger than the charging it compensates.

## Unchanged

- Topology buses.
- Conductor classes and ratings.
- Transformers.
- Generators.
- Loads.
- Capacitors.
- HVDC.
- Voltage limits.
- The winter-openings rule.

There is no new evidence for changing any of them.
