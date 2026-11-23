# Repair round 1: expectations written before the rebuild (23 Nov 2026)

These are pushed before `params_r1/` and `case_r1/` exist.

- **Summer (V1): I expect it still fails.**
  - Possible outcomes: no rung, or L4/L5 at best.
  - Reasons:
    - Before the repair, summer AC-OPF failed even with thermal limits removed, shunts removed and reactive load at zero.
    - No rule touches the Kot Addu 132 kV pinch.
    - RP2 only partly relieves the Lahore 132 kV corridor. New Kot Lakhpat–Bund Road adds a 220 kV path, but LESCO's 220/132 kV transformer supply stays at 1.02× its load.
  - The DC rating multiplier was about 6.0. I expect it to fall, but stay above the ladder's ×1.5.
- **Winter (V2): uncertain, L3 or L4 most likely.**
  - RP1 removes the Chashma pocket, which bound at 1.65× in winter.
  - RP3 removes the reactive over-absorption that made AC infeasible.
  - The remaining 132 kV pockets bound at 1.23–1.65×: Manga, Chakdara, Daharki–Guddu.
- **H3 after the repair:** not assessable, as declared.
