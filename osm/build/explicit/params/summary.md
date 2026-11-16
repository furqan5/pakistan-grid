# Day 6 parameters (explicit build)

Rules: builder/parameters.json (commit 747be71, before this ran). All MVAr at 1.0 pu.

## Lines

| class | branches | circuit-km | R+jX range (pu) | charging MVAr at 1 pu |
|---|---|---|---|---|
| 500 kV | 178 | 9,310 | x 0.00001–0.0357 | 9,521 |
| 220 kV | 225 | 12,944 | x 0.00005–0.1144 | 1,745 |
| 132 kV | 1266 | 23,069 | x 0.00005–0.3854 | 1,126 |
| 66 kV | 92 | 2,505 | x 0.00083–0.7943 | 31 |

- **Total line charging at 1.0 pu: 12,422 MVAr** (reported only, H2; TSEP summer 17,517 / winter off-peak 15,897 are PSS/E values at solved voltages for a network that includes KE's 132 kV and the parts OSM lacks).
- Variant 220_twin_rail: total charging 13,037 MVAr (reported only).
- Variant 132_rail: total charging 12,503 MVAr (reported only).

## Transformers

| pair | branches | from PSS 44th | default | total MVA |
|---|---|---|---|---|
| 500-220 | 21 | 15 | 6 | 30,750 |
| 500-132 | 2 | 0 | 2 | 1,000 |
| 220-132 | 67 | 39 | 28 | 35,810 |
| 132-66 | 35 | 0 | 35 | 2,800 |
| 132-110 | 1 | 0 | 1 | 80 |

PSS 44th station rows → model stations:
- 500 kV Gatti Faisalabad: -> S0028 via PER Gatti
- 500 kV Sheikhupura: -> S0079 via PER S.K.P
- 500 kV Yousafwala-Sahiwal: -> S0062 via PER Yousafwala
- 500 kV New Lahore: -> S0705 via PER New Lahore
- 500 kV Nokhar: -> S0083 via PER Nokhar
- 500 kV Rawat: -> S0049 via PER Rawat
- 500 kV Sheikh Muhammadi: -> S0127 via PER Peshawar
- 500 kV Multan: -> S0024 via PER Multan
- 500 kV Muzaffar Garh: -> S0023 via PER M.garh
- 500 kV Dera Ghazi Khan: -> S0729 via PER D.G. Khan
- 500 kV Rahim Yar Khan: -> S0213 via PER RYK
- 500 kV Dadu: -> S0051 via PER Dadu
- 500 kV Guddu: -> S0052 via PER Guddu
- 500 kV Jamshoro: -> S0025 via PER Jamshoro
- 500 kV North Karachi Industrial (NKI): -> S0647 via PER NKI
- 500 kV Shikarpur: -> S0132 via PER Shikarpur
- 220 kV Samundari Road FSD: -> S0142 via PER Sammundri
- 220 kV Jaranwala Road FSD: -> S0084 via PER Jaranwala
- 220 kV Nishatabad FSD: -> S0232 via PER Nishatabad
- 220 kV Bandala FSD: -> S0237 via PER Bandial
- 220 kV T.T Singh: -> S0340 via PER T.T. Singh
- 220 kV Ludewala Sargodha: -> S0316 via PER Ludewala
- 220 kV Sailkot: PER Sialkot has no S3 bus
- 220 kV Gujrat: PER Gujrat has no S3 bus
- 220 kV Ghakhar: -> S0102 via PER Ghakkar
- 220 kV Kala Shah Kaku Lahore: -> S0116 via PER KSK
- 220 kV Ravi Lahore: -> S0117 via PER Ravi
- 220 kV Bund Road Lahore: -> S0114 via PER Band
- 220 kV New Shalamar Lahore: -> S0119 via PER Shalamar
- 220 kV New KotLakhPat Lahore: -> S0724 via PER N.K.L.P
- 220 kV Ghazi Lahore (New GIS): -> S0118 via PER Ghazi Road
- 220 kV Sarfaraz Nagar Lahore: -> S0115 via PER Safdar Nagar
- 220 kV Okara: -> S0264 via PER Okara
- 220 kV Wapda Town Lahore: PER Wapda Town has no S3 bus
- 220 kV Kassowal: -> S0136 via PER Kassowal
- 220 kV Bannu: -> S0149 via PER Bannu
- 220 kV Burhan: -> S0152 via PER Burhan
- 220 kV Daudkhel: -> S0148 via PER Daudkhel
- 220 kV Islamabad University: -> S0430 via PER University
- 220 kV Mardan: -> S0027 via PER Mardan
- 220 kV Sangjani: -> S0405 via PER ISPR
- 220 kV Shahibagh: -> S0163 via PER Shahibagh
- 220 kV Mansehra: -> S0534 via PER Mansehra
- 220 kV Chakdara: -> S0726 via PER Chakdara
- 220 kV DI-Khan: -> S0728 via PER D.I. Khan
- 220 kV Nowshera: -> S0707 via PER Nowshera
- 220 kV Hala Road: -> S0126 via PER Hala Road
- 220 kV Jhampir: -> S0650 via PER Jhimpir 1
- 220 kV T.M.Khan: -> S0618 via PER T.M.K
- 220 kV Rohri: -> S0140 via PER Rohri
- 220 kV Daharki: -> S0058 via PER Daharki
- 220 kV Sibbi: -> S0133 via PER Sibbi
- 220 kV Quetta: -> S0048 via PER Quetta
- 220 kV Khuzdar: -> S0099 via PER Khuzdar
- 220 kV Loralai: PER Loralai has no S3 bus
- 220 kV Dera Murad Jamali: -> S0736 via PER D.M. Jamali
- 220 kV Muzaffar Garh: -> S0023 via PER M.garh
- 220 kV Bahawal Pur: -> S0157 via PER Bahawalpur
- 220 kV Vehari: -> S0050 via PER Vehari
- 220 kV Chishtian: -> S0364 via PER Chistian
- 220 kV Lal Sohanra: -> S0706 via PER Lal Sohanra

## Reactors (nameplate MVAr at 1.0 pu)

- summer_peak: placed 6,162.0 MVAr vs TSEP total 6,162 → **equal**; 58 buses
- winter_offpeak: placed 8,211.0 MVAr vs TSEP total 8,211 → **equal**; 58 buses
  - TSEP T5-9 Sheikh Muhammadi: 111 MVAr at S:S0127@500
  - TSEP T5-9 Rawat: 111 MVAr at S:S0049@500
  - TSEP T5-9 West FSD: 111 MVAr at S:S0765@500
  - TSEP T5-9 D.G. Khan: 111 MVAr at S:S0729@500
  - TSEP T5-9 Shikarpur: 222 MVAr at S:S0132@500
  - TSEP T5-9 D.M. Jamali: 60 MVAr at S:S0736@220
  - TSEP T5-9 Loralai: no bus, into pool: 60 MVAr at — (pooled)
  - TSEP T5-9 Zhob: no bus, into pool: 60 MVAr at — (pooled)
- Pool buses: 52 500 kV station buses. Capacitors (12,192 / 146 MVAr) are placed on Day 8 by the declared rule.

## HVDC

- Fixed transfer: summer 4000 MW, winter off-peak 2000 MW; loss1 0.034 → 136 / 68 MW dcline loss (reported next to H1/H4).

## Winter openings (TSEP Table 5-7)

| kV | circuit | open | status | buses | branch idx | circuits before |
|---|---|---|---|---|---|---|
| 500 | Ghazi Barotha - Gatti | 1 | unmapped | P:P0023@500;S:S0037@500 – S:S0028@500 |  |  |
| 500 | Gujranwala - Rawat | 1 | unmapped |  – S:S0049@500 |  |  |
| 500 | Gujranwala - Neelum Jhelum | 1 | unmapped |  –  |  |  |
| 500 | Maira - Suki Kinari | 1 | unmapped |  – P:P6566@500 |  |  |
| 500 | Maira - Karot | 1 | unmapped |  –  |  |  |
| 500 | Maira - Islamabad West | 1 | unmapped |  –  |  |  |
| 500 | Tarbela - Rawat | 1 | mapped | S:S0036@500 – S:S0049@500 | 714 | 1 |
| 500 | Tarbela - Ghazi Barotha | 1 | unmapped | S:S0036@500 – P:P0023@500;S:S0037@500 |  |  |
| 500 | Rawat - Islamabad West | 1 | unmapped | S:S0049@500 –  |  |  |
| 500 | Matiari - Moro | 2 | unmapped | S:S0675@500;S:S0789@500 – S:S0690@500 |  |  |
| 500 | Moro - Rahim Yar Khan | 2 | unmapped | S:S0690@500 – S:S0213@500 |  |  |
| 220 | Kassowal - Arifwala | 1 | unmapped | S:S0136@220 –  |  |  |
| 220 | Kassowal - Vehari | 1 | mapped | S:S0136@220 – S:S0050@220 | 567 | 2 |
| 220 | KAPCO - Multan | 1 | unmapped |  – S:S0024@220;S:S0069@220 |  |  |
| 220 | KAPCO - Muzaffargarh Solar | 1 | unmapped |  – S:S0023@220 |  |  |
