# Day 8 loads (explicit build)

Rules: builder/parameters.json `loads` (commit 8c77814, pushed before this ran).

## Totals

- summer_peak: DISCO load 26,931.6 MW (target 26,931.6 = I1 27,097 x 26,380/26,542, Gwadar not placed); KE export 2,050.0 MW; Q 16,714.3 MVAr; capacitors 12,192.0 MVAr (TSEP 12,192)
- winter_offpeak: DISCO load 8,720.4 MW (target 8,720.4 = I1 8,774 x 26,380/26,542, Gwadar not placed); KE export 1,001.0 MW; Q 4,124.7 MVAr; capacitors 146.0 MVAr (TSEP 146)

## S2 (signed-off denominators)

- Load in the main component: **100.0%** (all load is placed on main-component buses by construction; a DISCO group with no load station would count as missing)
- Installed generation in the main component: **99.8%** (35,277 of 35,355 MW; the 5 excluded small hydro plants count as missing)
- **S2 PASS** (≥ 98% each)

## DISCO groups

| group | TSEP MW (2026-27) | load stations | summer MW | MW per station | 66 kV stations | median anchor km |
|---|---|---|---|---|---|---|
| LESCO | 5,701 | 74 | 5,820 | 78.7 | 0 | 16.1 |
| MEPCO | 4,870 | 114 | 4,972 | 43.6 | 6 | 33.4 |
| PESCO+TESCO | 3,448 | 93 | 3,520 | 37.9 | 9 | 33.7 |
| FESCO | 3,296 | 81 | 3,365 | 41.5 | 2 | 32.9 |
| IESCO | 2,923 | 84 | 2,984 | 35.5 | 3 | 19.4 |
| GEPCO | 2,704 | 52 | 2,761 | 53.1 | 3 | 31.2 |
| HESCO | 1,232 | 79 | 1,258 | 15.9 | 9 | 44.8 |
| QESCO | 1,172 | 65 | 1,197 | 18.4 | 4 | 80.1 |
| SEPCO | 1,034 | 58 | 1,056 | 18.2 | 7 | 29.7 |

- Load stations: 700; excluded: {'K-Electric flagged': 6, 'generation subtype': 4}; anchors: 56 PSS-labelled NTDC stations
- KE export buses: 9 (J:11068174950@220, J:11870783812@220, J:3898564479@220, J:5407566608@132, P:P0031@132, S:S0128@220, S:S0158@132, S:S0589@132, S:S1055@220)

## FESCO / MEPCO station matching

- **FESCO**: 4 of 175 table stations matched; 237 of 4,809 MW; 77 of 81 model stations unmatched
- **MEPCO**: 7 of 180 table stations matched; 423 of 6,949 MW; 107 of 114 model stations unmatched

| DISCO | table station | model station | OSM name | MW 2026-27 |
|---|---|---|---|---|
| FESCO | JARANWALA | S0084 | Jaranwala Road | 72.4 |
| FESCO | NISHATABAD | S0232 | Nishatabad Grid Station | 63.1 |
| FESCO | BANDALA | S0237 | Bandala | 61.4 |
| FESCO | LALIAN | S0771 | Lalian | 40.4 |
| MEPCO | Mian Channu | S0167 | Mian Channu Grid Station | 97.6 |
| MEPCO | Muzaffar Garh | S0023 | Muzaffargarh | 93.8 |
| MEPCO | Pakpattan | S0295 | Pakpattan | 77.7 |
| MEPCO | Hasil Pur | S0124 | Hasilpur | 64.9 |
| MEPCO | Chishtian | S0364 | Chishtian | 62.1 |
| MEPCO | Chuna Wala | S0737 | Chunawala | 7.8 |
| MEPCO | Kassowal | S0136 | Kassowal | 18.6 |
