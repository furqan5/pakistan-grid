# Day 9 case assembly (explicit build)

Rules: builder/parameters.json `assembly` and `winter_openings.rule_v2_18nov` (commit 5bcee71, pushed before this ran).

## Cases

| snapshot | buses | branches | gens on | loads | shunts | load MW | gen Pmax MW | branches out |
|---|---|---|---|---|---|---|---|---|
| summer_peak | 1489 | 1855 | 99 | 709 | 829 | 28,982 | 32,540 | 0 |
| winter_offpeak | 1489 | 1855 | 109 | 709 | 829 | 9,721 | 22,254 | 7 |

- Impedance floor 1e-4 pu applied to 96 lines

## Winter openings (TSEP Table 5-7, path rule)

| kV | circuit | open | status | branches | km |
|---|---|---|---|---|---|
| 500 | Ghazi Barotha - Gatti | 1 | mapped | 3 | 309.6 |
| 500 | Gujranwala - Rawat | 1 | unmapped | 0 | 0 |
| 500 | Gujranwala - Neelum Jhelum | 1 | unmapped | 0 | 0 |
| 500 | Maira - Suki Kinari | 1 | unmapped | 0 | 0 |
| 500 | Maira - Karot | 1 | unmapped | 0 | 0 |
| 500 | Maira - Islamabad West | 1 | unmapped | 0 | 0 |
| 500 | Tarbela - Rawat | 1 | mapped | 1 | 110.9 |
| 500 | Tarbela - Ghazi Barotha | 1 | unmapped | 0 | 0 |
| 500 | Rawat - Islamabad West | 1 | unmapped | 0 | 0 |
| 500 | Matiari - Moro | 2 | mapped | 2 | 155.3 |
| 500 | Moro - Rahim Yar Khan | 2 | mapped | 2 | 333.8 |
| 220 | Kassowal - Arifwala | 1 | unmapped | 0 | 0 |
| 220 | Kassowal - Vehari | 1 | mapped | 1 | 75.0 |
| 220 | KAPCO - Multan | 1 | unmapped | 0 | 0 |
| 220 | KAPCO - Muzaffargarh Solar | 1 | unmapped | 0 | 0 |

Mapped 5 of 15.

## Load deliverability (summer, before any solve)

Per DISCO group: load MVA net of capacitors vs transformer capacity into its 132 kV buses plus generation connected at 132/66 kV. 132 kV lines between groups are not counted.

| group | load MW | net MVAr | net MVA | 220&500/132 kV transformer MVA | 132/66 kV gen MW | (trafo + gen) / load MVA |
|---|---|---|---|---|---|---|
| LESCO | 5,820 | 672 | 5,859 | 5,030 | 938 | 1.02 |
| MEPCO | 4,972 | 699 | 5,021 | 6,760 | 0 | 1.35 |
| PESCO+TESCO | 3,520 | 569 | 3,566 | 4,960 | 771 | 1.61 |
| FESCO | 3,365 | 428 | 3,392 | 6,560 | 196 | 1.99 |
| IESCO | 2,984 | 395 | 3,010 | 4,140 | 343 | 1.49 |
| GEPCO | 2,761 | 395 | 2,789 | 2,140 | 561 | 0.97 |
| HESCO | 1,258 | 213 | 1,276 | 3,530 | 1,346 | 3.82 |
| QESCO | 1,197 | 173 | 1,209 | 1,710 | 0 | 1.41 |
| SEPCO | 1,056 | 183 | 1,071 | 1,980 | 222 | 2.06 |
