# Day 7 generators (explicit build)

Rules: builder/parameters.json `generators` (commit 42c7533, pushed before this ran). Crosswalk: day7/plant_crosswalk.csv.

## Exit checks

- (a) Installed MW in the model: **35,277** vs IGCEP NGC 36,424 less exclusions (Iran 100, dependable-0 969) = 35,355 → -0.2% (within ±5%)
- (b) **Summer**: located Pmax 32,540 MW vs requirement 30,316 MW (load 27,097 + KE 2,050 + TSEP losses 1,033 + dcline loss) → margin **2,224 MW**
- Winter off-peak: located Pmax 22,254 MW vs requirement 10,050 MW → margin 12,204 MW; sum of Pmin 5,595 MW (must stay below the requirement)
- Unlocated plants (block Day 9): 0, dependable 0 MW; summer Pmax they would add 0 MW
- Slack: summer S:S0036@500; winter S:S0692@500 (China HUBCO, 1249 MW)

## By fuel (in model)

| fuel | plants | dependable MW | summer Pmax | winter Pmax | c1 $/MWh range |
|---|---|---|---|---|---|
| hydro | 25 | 10,257 | 10,257 | 1,159 | 8.0–8.0 |
| ccgt | 17 | 8,697 | 8,697 | 8,697 | 19.3–121.1 |
| coal | 9 | 7,368 | 7,368 | 7,368 | 19.9–60.2 |
| nuclear | 6 | 3,290 | 3,290 | 3,290 | 6.3–6.9 |
| wind | 36 | 1,845 | 1,845 | 277 | 0.0–0.0 |
| engine_rfo_gt | 6 | 1,083 | 1,083 | 1,083 | 118.7–134.8 |
| solar | 8 | 650 | 0 | 0 | 0.0–0.0 |
| bagasse | 10 | 380 | 0 | 380 | 0.0–0.0 |

## By latitude band (in model)

| band | summer Pmax MW | winter Pmax MW |
|---|---|---|
| north of 32°N | 12,370 | 3,352 |
| 30–32°N | 8,127 | 8,331 |
| 27–30°N | 2,001 | 2,097 |
| south of 27°N | 10,042 | 8,474 |

## Connection

- By voltage: 500 kV 25 plants / 23,180 MW, 220 kV 30 plants / 5,434 MW, 132 kV 61 plants / 4,932 MW, 66 kV 1 plants / 24 MW
- Connection distance > 5 km: Chashma 10.24 km (S:S0987@220); Kurram Garhi 8.17 km (S:S0147@132); Renala 15.65 km (S:S0145@132); Sapphire 5.37 km (S:S0984@500); Almoiz 15.83 km (S:S0728@132); Chiniot 11.16 km (S:S0378@132); Hamza 11.78 km (S:S0465@132); Artistic_Wind-2 5.21 km (S:S0656@132); Din Wind Energy 8.77 km (S:S0656@132); Hawa 8.08 km (S:S0653@132); Indus 12.74 km (S:S0656@132); Jhimpir 7.3 km (S:S0653@132); Lakeside Wind 9.36 km (S:S0718@132); Liberty Wind-I 10.19 km (S:S0656@132); Master Green 15.64 km (S:S0334@132); Metro_Wind 12.8 km (S:S0718@132); NASDA Green Wind 7.79 km (S:S0718@132); Tricom 6.89 km (S:S0653@132); Liberty Wind-II 10.19 km (S:S0656@132)
- Flags: SIZE: Nandipur 525 MW at 132 kV

## Unlocated (block Day 9 until placed)


## Plants

| sr | plant | fuel | dep MW | bus | how | dist km | c1 $/MWh |
|---|---|---|---|---|---|---|---|
| 1 | Allai Khwar | hydro | 121 | P:P0137@220 | documented 220 kV, own bus | 0.0 | 8 |
| 2 | Chashma | hydro | 184 | S:S0987@220 | crosswalk voltage 220 kV (see basis), nearest 220 kV bus | 10.24 | 8 |
| 3 | Dubair Khwar | hydro | 130 | S:S0457@132 | highest kV within 5 km | 0.09 | 8 |
| 4 | Ghazi Brotha | hydro | 1450 | P:P0023@500 | documented 500 kV, own bus | 0.0 | 8 |
| 5 | Golen Gol | hydro | 108 | S:S0678@132 | highest kV within 5 km | 0.78 | 8 |
| 6 | Jinnah | hydro | 36 | S:S0479@220 | highest kV within 5 km | 0.16 | 8 |
| 7 | Khan Khwar | hydro | 72 | S:S0751@132 | highest kV within 5 km | 2.45 | 8 |
| 8 | Mangla | hydro | 960 | P:P0024@220 | documented 220 kV, own bus | 0.0 | 8 |
| 9 | Neelum Jehlum | hydro | 0 | S:S0677@500 | excluded: dependable 0 MW; crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.27 | 8 |
| 10 | Tarbela 1-14 | hydro | 3478 | S:S0036@500 | documented 500 kV, own bus | 0.0 | 8 |
| 11 | Tarbela_Ext_04 | hydro | 1410 | S:S0036@500 | documented 500 kV, own bus | 0.0 | 8 |
| 12 | Warsak | hydro | 160 | S:S0160@132 | highest kV within 5 km | 4.25 | 8 |
| 13 | Gomal Zam | hydro | 17 | — | EXCLUDED: OSM location but no bus within 20 km; GEM has no record |  | 8 |
| 14 | Rasul | hydro | 22 | P:P0113@132 | highest kV within 5 km | 0.0 | 8 |
| 15 | Dargai | hydro | 20 | — | EXCLUDED: no OSM or GEM location |  | 8 |
| 16 | Nandipur | hydro | 14 | S:S0303@132 | highest kV within 5 km | 0.43 | 8 |
| 17 | Shadiwal | hydro | 14 | S:S0918@220 | highest kV within 5 km | 4.36 | 8 |
| 18 | Chichoki | hydro | 13 | S:S0984@500 | highest kV within 5 km | 4.0 | 8 |
| 19 | Kurram Garhi | hydro | 4 | S:S0147@132 | nearest bus within 20 km | 8.17 | 8 |
| 20 | Renala | hydro | 1 | S:S0145@132 | nearest bus within 20 km | 15.65 | 8 |
| 21 | Chitral | hydro | 1 | — | EXCLUDED: no OSM or GEM location |  | 8 |
| 22 | Jabban | hydro | 22 | — | EXCLUDED: no OSM or GEM location |  | 8 |
| 23 | Guddu 747 | ccgt | 486 | S:S0207@500 | documented 500 kV, own bus | 0.0 | 32.811 |
| 24 | Nandipur | ccgt | 525 | S:S0303@132 | crosswalk voltage 132 kV (see basis), nearest 132 kV bus | 0.33 | 104.266 |
| 25 | CHASHNUPP - I | nuclear | 300 | S:S0987@220 | crosswalk voltage 220 kV (see basis), nearest 220 kV bus | 0.55 | 6.873 |
| 26 | CHASHNUPP-II | nuclear | 300 | S:S0987@220 | crosswalk voltage 220 kV (see basis), nearest 220 kV bus | 0.55 | 6.873 |
| 27 | CHASHNUPP-III | nuclear | 315 | S:S0987@220 | crosswalk voltage 220 kV (see basis), nearest 220 kV bus | 0.55 | 6.873 |
| 28 | CHASHNUPP-IV | nuclear | 315 | S:S0987@220 | crosswalk voltage 220 kV (see basis), nearest 220 kV bus | 0.55 | 6.873 |
| 29 | K-2 | nuclear | 1030 | S:S0691@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.42 | 6.3 |
| 30 | K-3 | nuclear | 1030 | S:S0691@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.42 | 6.3 |
| 31 | Jagran - I | hydro | 30 | S:S0900@132 | highest kV within 5 km | 0.61 | 8 |
| 32 | Malakand - III | hydro | 81 | S:S0166@132 | highest kV within 5 km | 1.55 | 8 |
| 33 | New Bong | hydro | 84 | S:S0386@132 | highest kV within 5 km | 2.5 | 8 |
| 34 | Daral Khwar | hydro | 37 | S:S0838@132 | highest kV within 5 km | 0.07 | 8 |
| 35 | Gul Pur | hydro | 103 | P:P0389@132 | highest kV within 5 km | 0.0 | 8 |
| 36 | Patrind | hydro | 149 | S:S0746@132 | highest kV within 5 km | 4.37 | 8 |
| 37 | Ranolia | hydro | 17 | — | EXCLUDED: no OSM or GEM location |  | 8 |
| 38 | Suki Kinari | hydro | 883 | P:P6566@500 | documented 500 kV, own bus | 0.0 | 8 |
| 39 | Karot | hydro | 713 | S:S0747@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.23 | 8 |
| 40 | AGL | engine_rfo_gt | 156 | S:S0496@132 | highest kV within 5 km | 3.98 | 118.712 |
| 41 | Balloki | ccgt | 1157 | S:S0704@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.19 | 82.337 |
| 42 | Bhikki | ccgt | 1130 | S:S0752@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.2 | 83.091 |
| 43 | China HUBCO | coal | 1249 | S:S0692@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.64 | 48.465 |
| 44 | Engro | ccgt | 215 | S:S0060@220 | highest kV within 5 km | 0.18 | 44.265 |
| 45 | Engro Thar | coal | 602 | S:S0743@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.34 | 21.885 |
| 46 | FKPCL | ccgt | 151 | S:S0061@220 | highest kV within 5 km | 0.08 | 121.081 |
| 47 | Foundation | ccgt | 174 | S:S0058@220 | highest kV within 5 km | 0.17 | 37.673 |
| 48 | Halmore | ccgt | 200 | S:S0752@500 | highest kV within 5 km | 4.89 | 101.39 |
| 49 | Haveli | ccgt | 1180 | S:S0757@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.19 | 81.308 |
| 50 | HuB N | engine_rfo_gt | 216 | S:S0778@132 | highest kV within 5 km | 0.1 | 134.806 |
| 51 | KAPCO | ccgt | 495 | S:S0053@220 | crosswalk voltage 220 kV (see basis), nearest 220 kV bus | 0.4 | 107.967 |
| 52 | Kohinoor | engine_rfo_gt | 124 | P:P0039@132 | highest kV within 5 km | 0.0 | 122.354 |
| 53 | Liberty | ccgt | 222 | S:S0057@132 | highest kV within 5 km | 0.12 | 19.322 |
| 54 | Liberty Tech | engine_rfo_gt | 196 | S:S0539@132 | highest kV within 5 km | 0.12 | 131.98 |
| 55 | Nishat C | engine_rfo_gt | 196 | S:S0089@132 | highest kV within 5 km | 0.26 | 125.752 |
| 56 | Nishat P | engine_rfo_gt | 195 | S:S0089@132 | highest kV within 5 km | 0.22 | 125.082 |
| 57 | Orient | ccgt | 206 | S:S0090@132 | highest kV within 5 km | 0.12 | 100.595 |
| 58 | Port Qasim | coal | 1243 | P:P0082@500 | documented 500 kV, own bus | 0.0 | 49.739 |
| 59 | JPCL | coal | 620 | S:S0025@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 1.06 | 60.201 |
| 60 | Sahiwal Coal | coal | 1231 | S:S0549@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.96 | 58.367 |
| 61 | Saif | ccgt | 204 | S:S0549@500 | highest kV within 5 km | 2.52 | 102.843 |
| 62 | Sapphire | ccgt | 204 | S:S0984@500 | nearest bus within 20 km | 5.37 | 102.425 |
| 63 | Trimmu | ccgt | 1244 | S:S0757@500 | highest kV within 5 km | 1.11 | 83.57 |
| 64 | Uch | ccgt | 549 | P:P0447@220 | highest kV within 5 km | 0.0 | 25.63 |
| 65 | Uch-II | ccgt | 355 | S:S0583@220 | highest kV within 5 km | 0.0 | 56.194 |
| 66 | Lucky Coal | coal | 607 | S:S0739@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.22 | 45.789 |
| 67 | Thal Nova | coal | 301 | S:S0742@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.33 | 21.895 |
| 68 | Thar TEL | coal | 301 | S:S0741@500 | crosswalk voltage 500 kV (see basis), nearest 500 kV bus | 0.34 | 21.895 |
| 69 | Thar-I (SSRL) | coal | 1214 | P:P0391@500 | documented 500 kV, own bus | 0.0 | 19.919 |
| 70 | Shahtaj | bagasse | 32 | S:S0951@132 | highest kV within 5 km | 0.1 | 0 |
| 71 | Almoiz | bagasse | 36 | S:S0728@132 | nearest bus within 20 km | 15.83 | 0 |
| 72 | Chanar | bagasse | 21 | S:S1105@132 | highest kV within 5 km | 0.16 | 0 |
| 73 | Chiniot | bagasse | 63 | S:S0378@132 | nearest bus within 20 km | 11.16 | 0 |
| 74 | Fatima Energy (FEL) | bagasse | 108 | S:S0732@132 | highest kV within 5 km | 0.21 | 0 |
| 75 | Hamza | bagasse | 15 | S:S0465@132 | nearest bus within 20 km | 11.78 | 0 |
| 76 | JDW - II | bagasse | 25 | S:S0060@220 | highest kV within 5 km | 4.96 | 0 |
| 77 | JDW - III | bagasse | 26 | S:S0060@220 | highest kV within 5 km | 5.0 | 0 |
| 78 | Ryk_Mills | bagasse | 30 | S:S0851@132 | highest kV within 5 km | 0.18 | 0 |
| 79 | Thal_Layyah | bagasse | 24 | S:S0500@66 | highest kV within 5 km | 3.99 | 0 |
| 80 | Act/Tapal Wind | wind | 30 | S:S0656@132 | highest kV within 5 km | 0.0 | 0 |
| 81 | Artistic_Wind | wind | 50 | S:S0656@132 | highest kV within 5 km | 1.24 | 0 |
| 82 | Artistic_Wind-2 | wind | 50 | S:S0656@132 | nearest bus within 20 km | 5.21 | 0 |
| 83 | Dawood | wind | 50 | S:S0667@220 | highest kV within 5 km | 0.0 | 0 |
| 84 | Din Wind Energy | wind | 50 | S:S0656@132 | nearest bus within 20 km | 8.77 | 0 |
| 85 | FFC | wind | 50 | S:S0653@132 | highest kV within 5 km | 2.84 | 0 |
| 86 | FWEL-I | wind | 50 | S:S0670@220 | highest kV within 5 km | 0.0 | 0 |
| 87 | FWEL-II | wind | 50 | S:S0669@220 | highest kV within 5 km | 0.0 | 0 |
| 88 | Gul Ahmed | wind | 50 | S:S0652@132 | highest kV within 5 km | 0.0 | 0 |
| 89 | Gul Ahmed-II | wind | 50 | S:S0652@132 | highest kV within 5 km | 0.0 | 0 |
| 90 | Hawa | wind | 50 | S:S0653@132 | nearest bus within 20 km | 8.08 | 0 |
| 91 | Indus | wind | 50 | S:S0656@132 | nearest bus within 20 km | 12.74 | 0 |
| 92 | Jhimpir | wind | 50 | S:S0653@132 | nearest bus within 20 km | 7.3 | 0 |
| 93 | Lakeside Wind | wind | 50 | S:S0718@132 | nearest bus within 20 km | 9.36 | 0 |
| 94 | Liberty Wind-I | wind | 50 | S:S0656@132 | nearest bus within 20 km | 10.19 | 0 |
| 95 | Master | wind | 50 | S:S0653@132 | highest kV within 5 km | 0.0 | 0 |
| 96 | Master Green | wind | 50 | S:S0334@132 | nearest bus within 20 km | 15.64 | 0 |
| 97 | Metro_Wind | wind | 50 | S:S0718@132 | nearest bus within 20 km | 12.8 | 0 |
| 98 | Metro_Wind-II | wind | 60 | S:S0651@132 | highest kV within 5 km | 0.0 | 0 |
| 99 | NASDA Green Wind | wind | 50 | S:S0718@132 | nearest bus within 20 km | 7.79 | 0 |
| 100 | Sachal | wind | 50 | S:S0655@132 | highest kV within 5 km | 0.0 | 0 |
| 101 | Sapphire_Wind | wind | 50 | S:S0723@132 | highest kV within 5 km | 2.29 | 0 |
| 102 | Tapal Wind-2 | wind | 50 | S:S0656@132 | highest kV within 5 km | 0.0 | 0 |
| 103 | Tenaga | wind | 50 | S:S0668@220 | highest kV within 5 km | 0.0 | 0 |
| 104 | Three_Gorges_I | wind | 50 | S:S0723@132 | highest kV within 5 km | 4.93 | 0 |
| 105 | Three_Gorges_II | wind | 50 | S:S0650@220 | highest kV within 5 km | 4.91 | 0 |
| 106 | Three_Gorges_III | wind | 50 | S:S0721@132 | highest kV within 5 km | 0.0 | 0 |
| 107 | Tricom | wind | 50 | S:S0653@132 | nearest bus within 20 km | 6.89 | 0 |
| 108 | Tricon_A | wind | 50 | S:S0772@220 | highest kV within 5 km | 3.42 | 0 |
| 109 | Tricon_B | wind | 50 | S:S0772@220 | highest kV within 5 km | 3.41 | 0 |
| 110 | Tricon_C | wind | 50 | S:S0718@132 | highest kV within 5 km | 0.0 | 0 |
| 111 | UEP | wind | 99 | S:S0650@220 | highest kV within 5 km | 3.3 | 0 |
| 112 | Yunus | wind | 50 | S:S0666@132 | highest kV within 5 km | 0.0 | 0 |
| 113 | Zephyr | wind | 50 | S:S0708@220 | highest kV within 5 km | 0.0 | 0 |
| 114 | Zorlu_Wind | wind | 56 | S:S0331@132 | highest kV within 5 km | 3.63 | 0 |
| 115 | Liberty Wind-II | wind | 50 | S:S0656@132 | nearest bus within 20 km | 10.19 | 0 |
| 116 | Helios | solar | 50 | S:S0461@132 | highest kV within 5 km | 1.04 | 0 |
| 117 | HNDS | solar | 50 | S:S0461@132 | highest kV within 5 km | 1.61 | 0 |
| 118 | Meridian | solar | 50 | S:S0461@132 | highest kV within 5 km | 1.04 | 0 |
| 119 | Appolo Solar | solar | 100 | S:S0662@132 | highest kV within 5 km | 0.79 | 0 |
| 120 | Best | solar | 100 | S:S0706@220 | highest kV within 5 km | 4.27 | 0 |
| 121 | Crest | solar | 100 | S:S0706@220 | highest kV within 5 km | 2.98 | 0 |
| 122 | QA_Solar | solar | 100 | S:S0706@220 | highest kV within 5 km | 4.64 | 0 |
| 123 | Zhenfa | solar | 100 | S:S0706@220 | highest kV within 5 km | 4.19 | 0 |
| 0 | Import from Iran | import | 100 | — | excluded: Makran/Gwadar off-grid |  | 0 |
