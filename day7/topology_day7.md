# Day 7: generators (18 Nov 2026)

- **Rules:** `builder/parameters.json` → `generators`. They were committed and **pushed to GitHub (42c7533) before** any generator code ran.
- **Crosswalk and builder:** `day7/plant_crosswalk.csv` and `builder/make_generators.py`, pushed in a4243df before their first run.
- **Output:** `osm/build/explicit/params/generators_summary.md` (the CSV isn't committed). Reasons are in `day7/generator_rules.md`.

## Sources extracted

- **IGCEP 2025-35 R2 Annex B-1(i):** 124 NGC plants, 36,424 MW installed and 33,747 MW dependable. The row sums **equal the printed totals**.
- **IGCEP Annex B-2:** costs for 52 existing thermal plants, in USD. c1 = fuel × heat rate + variable O&M.
- **Seasonal hydro:** neither IGCEP nor TSEP prints it. Winter hydro uses January 2025 hydel generation of 866 GWh ([ProPakistani, 20 Feb 2025](https://propakistani.pk/2025/02/20/power-generation-falls-in-january-2025-despite-22-decline-in-fuel-cost/)), which gives 11.3% of dependable.

## Results (scored build)

- **106 plants in the model**, 34,687 MW installed, against IGCEP NGC less exclusions of 35,355 MW: **−1.9%, within ±5%**.
  - Excluded: the Iran import (100 MW, off-grid Makran) and Neelum Jhelum (969 MW, dependable 0).
- **Summer, the binding check:** located Pmax is **32,158 MW**, against a requirement of 30,316 MW (load + KE + TSEP losses + dcline loss). **Margin 1,842 MW.**
- **Winter off-peak:** located Pmax is 22,052 MW against 10,050 MW required. The sum of Pmin is 5,595 MW, which stays below the requirement.
- **By fuel:**

  | Fuel | Dependable MW |
  |---|---|
  | Hydro | 10,074 |
  | CCGT | 8,697 |
  | Coal | 7,368 |
  | Nuclear | 3,290 |
  | Wind | 1,646 |
  | Engines | 1,083 |
  | Solar | 600 (0 in both snapshots, by the hour assumption) |
  | Bagasse | 229 (winter only) |

- **Where the capacity is.** North of 32°N there is 12,187 MW at summer peak and 3,296 MW in winter.
  - TSEP's winter off-peak plot appears to show Tarbela and Ghazi Barotha at 0 MW [VERIFY]. If so, the model has more northern generation available in winter than TSEP dispatched.
  - This is reported next to H4. It is **not tuned**.
- **Connections:**

  | Voltage | Plants | MW |
  |---|---|---|
  | 500 kV | 25 | 23,180 |
  | 220 kV | 29 | 5,835 |
  | 132 kV | 50 | 3,972 |

  - 33 plants use the documented connection voltage. These are the 500/220 kV plants named in the PSS line tables or TSEP Figure 5-9: K-2/K-3, the Thar plants, Port Qasim, China HUBCO, Lucky, Sahiwal, Haveli, Balloki, Bhikki, Tarbela, Ghazi Barotha, Suki Kinari, Karot, Guddu 747, Chashnupp, KAPCO, Mangla and Allai Khwar.
- **Size-check flag, resolved after the first generator run** (the rule requires flags to be resolved in the crosswalk):
  - Nandipur, 525 MW, first landed on 132 kV.
  - It was moved to 220 kV Ghakhar, 12.6 km away. The reason is engineering, not a document: 525 MW can't run out over 112 MVA Lynx circuits [VERIFY].
- **Quirk of the declared rule, logged and not changed.** "Highest voltage within 5 km" puts a few small plants on EHV buses when a large plant's yard is nearby:
  - Chichoki (13 MW) and Sapphire (204 MW) on 500 kV;
  - Halmore and Saif (200 MW each) on 500 kV;
  - Shadiwal, JDW-III and five Jhimpir wind farms on 220 kV.
  
  The electrical effect is small.
- **Slack bus:** summer Tarbela 500 kV; winter China HUBCO 500 kV.

## Unlocated: 18 plants, 660 MW dependable (459 MW at summer peak). They block Day 9

- **Hydro:** Khan Khwar 72, Malakand-III 81, Jagran-I 30, Jabban 22, Dargai 20, Ranolia 17, Gomal Zam 17 (located, but no bus within 20 km), Chitral 1.
- **Wind:** Artistic 1 and 2 (100), UEP 99.
- **Bagasse:** Almoiz, Chanar, Hamza, JDW-II, RYK Mills, Thal Layyah (151).
- **Solar:** HNDS 50.

**To place them:** download GEM's Global Integrated Power Tracker (CC BY 4.0). The download form asks for name and email, so **Furqan has to fill it in**. Save it to `sources/`; the coordinates then go into the crosswalk as a logged change. Without them, summer still has a margin of about 1,840 MW, but the rule says unlocated plants aren't silently dropped.

## Open item for S2 (generation share, evaluated with loads on Day 8)

- The gate doesn't say what S2's generation denominator is.
- Measured against IGCEP NGC less the documented exclusions (35,355 MW), the model holds 98.1%, which passes the 98% mark narrowly.
- Against the full 36,424 MW, it holds 95.2%, a fail.
- **This number was seen before any definition was fixed.** Whichever definition Furqan signs off is post hoc with respect to it, and must be labelled so.
- Placing the unlocated plants would take the first figure to about 100%.

## Day 8 next

- **Loads:**
  - TSEP Table 2-1 DISCO shares, scaled to 27,097 MW (summer) and 8,774 MW (winter off-peak);
  - power factor 0.861 (summer) and 0.907 (winter off-peak);
  - FESCO and MEPCO by grid-station MW;
  - K-Electric export at the interface buses.
- **Capacitors** by the declared rule.
- **S2.**
