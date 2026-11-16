# PSS 44th line cross-check (inferred build)

Rules: builder/config.json `pss_line_check` (fixed before the first run). PSS data is to June 2019; flags are for review, nothing is removed.

- 500 kV: 50 usable rows; 22 checked; ok 17; too far 0; too close 0; path differs >10% 5; no path 0
- 220 kV: 88 usable rows; 50 checked; ok 38; too far 3; too close 1; path differs >10% 12; no path 0
- Circuit corrections under correct_rule: 2 branches (2 OSM ways), 2 route-km raised from 1 to 2 circuits

| kV | region | sr | PSS line | route km | bus A | bus B | straight km | path km | ratio | flags |
|---|---|---|---|---|---|---|---|---|---|---|
| 500 | Lahore | 1 | Tarbela-Barotha 1 | 73 | S:S0036@500 | ambiguous: P:P0023@500, S:S0037@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 2 | Tarbela-Barotha 2 | 77 | S:S0036@500 | ambiguous: P:P0023@500, S:S0037@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 3 | Barotha-Gatti 1 | 309 | ambiguous: P:P0023@500, S:S0037@500 | S:S0028@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 4 | Barotha-Gatti 2 | 308 | ambiguous: P:P0023@500, S:S0037@500 | S:S0028@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 5 | Gatti-QATPL | 83 | S:S0028@500 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 6 | QATPL-Lahore(Skp) | 16 | no OSM match | S:S0079@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 7 | H.B.Shah-Gatti 2 | 165 | no OSM match | S:S0028@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 8 | H.B.Shah-Multan | 162 | no OSM match | S:S0024@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 9 | Gatti-Rousch | 150 | S:S0028@500 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 10 | Rousch-Multan | 62 | no OSM match | S:S0024@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 11 | Muzafargarh-H.B.Shah | 174 | S:S0023@500 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 12 | H.B.Shah-Gatti 1 | 111 | no OSM match | S:S0028@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 13 | Multan-Yousafwala | 161 | S:S0024@500 | S:S0062@500 | 156.3 | 161.7 | 1.005 | ok |
| 500 | Lahore | 14 | Yousafwala-CFPP | 27 | S:S0062@500 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 15 | CFPP-New Lahore | 95 | no OSM match | S:S0705@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 16 | New Lahore-Lahore (SKP) II | 67 | S:S0705@500 | S:S0079@500 | 46.2 | 52.3 | 0.78 | path differs from route by more than 10% |
| 500 | Lahore | 17 | Balloki-New Lahore-I | 31 | no OSM match | S:S0705@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 18 | Balloki-New Lahore-II | 31 | no OSM match | S:S0705@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Lahore | 19 | New Lahore-Lahore (SKP) I | 57 | S:S0705@500 | S:S0079@500 | 46.2 | 52.3 | 0.917 | ok |
| 500 | Lahore | 20 | New Lahore-New Ghakkar | 54 | S:S0705@500 | PER Ghakkar: station has no 500 kV bus |  |  |  | not checked: endpoint not mapped |
| 500 | Islamabad | 1 | Tarbela- Sheikh Muhammadi Peshawar | 117 | S:S0036@500 | S:S0127@500 | 107.2 | 117.4 | 1.004 | ok |
| 500 | Islamabad | 2 | Tarbela- New Rawat | 111 | S:S0036@500 | S:S0049@500 | 81.8 | 110.9 | 0.999 | ok |
| 500 | Islamabad | 3 | Ghazi Brotha - New Rawat- I | 107 | ambiguous: P:P0023@500, S:S0037@500 | S:S0049@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Islamabad | 4 | Ghazi Brotha - New Rawat- II | 108 | ambiguous: P:P0023@500, S:S0037@500 | S:S0049@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Islamabad | 5 | New Rawat - New Ghakkar-I | 180 | S:S0049@500 | PER Ghakkar: station has no 500 kV bus |  |  |  | not checked: endpoint not mapped |
| 500 | Islamabad | 6 | Rawat Neelum Jehlum | 214 | S:S0049@500 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 500 | Islamabad | 7 | Neelum Jehlum Ghakkhar | 285 | no OSM match | PER Ghakkar: station has no 500 kV bus |  |  |  | not checked: endpoint not mapped |
| 500 | Islamabad | 8 | Ghakkar-Lahore-I (Tower # 1 to 150) | 56 | PER Ghakkar: station has no 500 kV bus | ambiguous: S:S0675@500, S:S0705@500, S:S0789@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Islamabad | 9 | Ghakkar-Lahore-II (SKL) | 64 | PER Ghakkar: station has no 500 kV bus | ambiguous: S:S0675@500, S:S0705@500, S:S0789@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Hyderabad | 1 | Dadu - Jamshoro - I | 152 | S:S0051@500 | S:S0025@500 | 147.6 | 152.7 | 1.005 | ok |
| 500 | Hyderabad | 2 | Port Qasim-Dadu | 285 | P:P0082@500 | S:S0051@500 | 218.2 | 335.8 | 1.178 | path differs from route by more than 10% |
| 500 | Hyderabad | 3 | Port Qasim- Jamshoro | 132 | P:P0082@500 | S:S0025@500 | 118.8 | 225.8 | 1.711 | path differs from route by more than 10% |
| 500 | Hyderabad | 4 | Guddu-Shikarpur-I | 123 | S:S0052@500 | S:S0132@500 | 113.3 | 122.2 | 0.994 | ok |
| 500 | Hyderabad | 5 | Shikarpur- Dadu -I | 195 | S:S0132@500 | S:S0051@500 | 170.1 | 191.0 | 0.98 | ok |
| 500 | Hyderabad | 6 | Guddu - Shikarpur - II | 124 | S:S0052@500 | S:S0132@500 | 113.3 | 122.2 | 0.986 | ok |
| 500 | Hyderabad | 7 | Shikarpur - Dadu - II | 194 | S:S0132@500 | S:S0051@500 | 170.1 | 191.0 | 0.985 | ok |
| 500 | Hyderabad | 8 | HUBCO - NKI | 27 | no OSM match | S:S0647@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Hyderabad | 9 | NKI- Jamshoro | 156 | S:S0647@500 | S:S0025@500 | 146.1 | 155.2 | 0.995 | ok |
| 500 | Hyderabad | 10 | CPHGC - Jamshoro | 181 | no OSM match | S:S0025@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Hyderabad | 11 | CPHGC-HUBCO | 1 | no OSM match | no OSM match |  |  |  | not checked: endpoint not mapped |
| 500 | Hyderabad | 12 | Engro thar- Jamshoro | 288 | no OSM match | S:S0025@500 |  |  |  | not checked: endpoint not mapped |
| 500 | Hyderabad | 13 | Jamshoro- Moro | 202 | S:S0025@500 | S:S0690@500 | 157.4 | 202.8 | 1.004 | ok |
| 500 | Hyderabad | 14 | Dadu - Moro | 45 | S:S0051@500 | S:S0690@500 | 47.8 | 54.5 | 1.211 | path differs from route by more than 10% |
| 500 | Multan | 1 | Muzaffargarh - Guddu | 256 | S:S0023@500 | S:S0052@500 | 234.3 | 257.5 | 1.006 | ok |
| 500 | Multan | 2 | Guddu 747 - R.Y Khan | 103 | S:S0207@500 | S:S0213@500 | 82.7 | 111.1 | 1.078 | ok |
| 500 | Multan | 3 | R.Y Khan - Multan | 258 | S:S0213@500 | S:S0024@500 | 200.4 | 261.4 | 1.013 | ok |
| 500 | Multan | 4 | Guddu 747 - Guddu Old | 2 | S:S0207@500 | S:S0052@500 | 1.1 | 2.5 | 1.236 | path differs from route by more than 10% |
| 500 | Multan | 5 | Guddu - D.G.Khan | 215 | S:S0052@500 | S:S0729@500 | 189.8 | 223.2 | 1.038 | ok |
| 500 | Multan | 6 | D.G.Khan - Multan | 127 | S:S0729@500 | S:S0024@500 | 113.4 | 133.0 | 1.047 | ok |
| 500 | Multan | 7 | Multan - Muzaffargarh | 62 | S:S0024@500 | S:S0023@500 | 46.2 | 63.5 | 1.023 | ok |
| 220 | Lahore | 1 | Bandala-Gatti 1 & 2 | 31 | S:S0237@220 | S:S0028@220 | 25.2 | 28.0 | 0.902 | ok |
| 220 | Lahore | 2 | Gatti-Nishatabad 1 & 2 | 2 | S:S0028@220 | S:S0232@220 | 2.3 | 2.2 | 1.121 | too far (straight line > 1.1 x route); path differs from route by more than 10% |
| 220 | Lahore | 3 | Gatti JWR 1 & 2 | 16 | S:S0028@220 | S:S0084@220 | 8.4 | 9.6 | 0.599 | path differs from route by more than 10% |
| 220 | Lahore | 4 | Gatti-Y/Wala 1 & 2 | 96 | S:S0028@220 | S:S0062@220 | 89.5 | 95.2 | 0.991 | ok |
| 220 | Lahore | 5 | Gatti-L/Wala 1 & 2 | 99 | S:S0028@220 | S:S0316@220 | 91.6 | 98.8 | 0.998 | ok |
| 220 | Lahore | 6 | Chashma-L/Wala 1 & 2 | 125 | no OSM match | S:S0316@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 7 | Multan-T.T. Singh 1 & 2 | 82 | S:S0024@220 | S:S0340@220 | 137.2 | 142.2 | 1.734 | too far (straight line > 1.1 x route); path differs from route by more than 10% |
| 220 | Lahore | 8 | T.T.Singh-SRD 1 & 2 | 52 | S:S0340@220 | S:S0142@220 | 45.8 | 50.8 | 0.977 | ok |
| 220 | Lahore | 9 | SRD-Nishatabad 1 & 2 | 23 | S:S0142@220 | S:S0232@220 | 20.5 | 176.8 | 7.686 | path differs from route by more than 10% |
| 220 | Lahore | 10 | 220 KV GKR - Mangla | 37 | S:S0102@220 | ambiguous: P:P0024@220, S:S0054@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 11 | 220 KV KSK - Mangla 3 | 96 | S:S0116@220 | ambiguous: P:P0024@220, S:S0054@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 12 | 220 KV GKR - SKT | 36 | S:S0102@220 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 13 | 220KV KSK - SKT | 97 | S:S0116@220 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 14 | 220 KV GKR - Gujrat | 32 | S:S0102@220 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 15 | 220 KV New GKR - Gujrat | 63 | S:S0102@220 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 16 | 220 KV New GKR - Gakkhar | 44 | S:S0102@220 | S:S0102@220 |  |  |  | not checked: both ends map to one bus |
| 220 | Lahore | 17 | 220 KV Gujrat-Mangla 1 & 2 | 4 | no OSM match | ambiguous: P:P0024@220, S:S0054@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 18 | 220 KV Kala Shah Kaku - Bund Road 1 & 2 | 27 | S:S0116@220 | S:S0114@220 | 27.9 | 29.9 | 1.106 | path differs from route by more than 10% |
| 220 | Lahore | 19 | 220 KV Kala Shah Kaku - Mangla 1 & 2 | 97 | S:S0116@220 | ambiguous: P:P0024@220, S:S0054@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 20 | 220KV New Kot Lakhpat - Bund Road 1 & 2 | 18 | S:S0724@220 | S:S0114@220 | 12.3 | 80.1 | 4.449 | path differs from route by more than 10% |
| 220 | Lahore | 21 | 220KV New Kot Lakhpat - Sarfraz Nagar | 47 | S:S0724@220 | S:S0115@220 | 42.2 | 46.2 | 0.983 | ok |
| 220 | Lahore | 22 | 220KV New Kot Lakhpat - New LHR 2 | 52 | S:S0724@220 | S:S0705@220 | 42.8 | 50.1 | 0.964 | ok |
| 220 | Lahore | 23 | 220KV Sarfraz Nagar - New LHR | 86 | S:S0115@220 | S:S0705@220 | 1.8 | 96.3 | 1.12 | too close (route > 2 x straight + 10 km); path differs from route by more than 10% |
| 220 | Lahore | 24 | 220KV Sarfraz Nagar - New Okara 1 & 2 | 80 | S:S0115@220 | S:S0264@220 | 69.4 | 80.4 | 1.004 | ok |
| 220 | Lahore | 25 | 220KV New Okara - Yousafwala 1 & 2 | 39 | S:S0264@220 | S:S0062@220 | 33.9 | 37.8 | 0.97 | ok |
| 220 | Lahore | 26 | 220KV Yousafwala - Kassowal 1 & 2 | 100 | S:S0062@220 | S:S0136@220 | 64.4 | 98.6 | 0.986 | ok |
| 220 | Lahore | 27 | 220KV Bund Road - Sheikhupura 1 & 2 | 26 | S:S0114@220 | S:S0079@220 | 25.9 | 27.3 | 1.05 | ok |
| 220 | Lahore | 28 | 220KV Bund Road - Sheikhupura 3 & 4 | 28 | S:S0114@220 | S:S0079@220 | 25.9 | 27.3 | 0.975 | ok |
| 220 | Lahore | 29 | 220KV New Kot Lakhpat - Sheikhupura | 53 | S:S0724@220 | S:S0079@220 | 38.2 | 52.8 | 0.996 | ok |
| 220 | Lahore | 30 | 220KV New Kot Lakhpat - New LHR 1 | 51 | S:S0724@220 | S:S0705@220 | 42.8 | 50.1 | 0.983 | ok |
| 220 | Lahore | 31 | 220KV New Lahore - Wapda Town | 40 | S:S0705@220 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 32 | 220KV Wapda Town - Sheikhupura | 42 | no OSM match | S:S0079@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 33 | 220KV Ravi - Sheikhupura | 38 | S:S0117@220 | S:S0079@220 | 27.0 | 37.7 | 0.993 | ok |
| 220 | Lahore | 34 | 220KV Altas P/H - Sheikhupura | 8 | P:P0041@220 | S:S0079@220 | 5.5 | 7.0 | 0.878 | path differs from route by more than 10% |
| 220 | Lahore | 35 | 220KV Altas P/H - Ravi | 36 | P:P0041@220 | S:S0117@220 | 23.1 | 35.3 | 0.98 | ok |
| 220 | Lahore | 36 | 220KV Kala Shah Kaku - Ravi | 24 | S:S0116@220 | S:S0117@220 | 18.2 | 23.6 | 0.982 | ok |
| 220 | Lahore | 37 | 220KV Kala Shah Kaku - Ghazi | 50 | S:S0116@220 | ambiguous: S:S0037@220, S:S0118@220, S:S0729@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 38 | 220KV Ghazi - Shalamar | 29 | ambiguous: S:S0037@220, S:S0118@220, S:S0729@220 | S:S0119@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Lahore | 39 | 220KV Ravi - Shalamar | 12 | S:S0117@220 | S:S0119@220 | 7.1 | 11.4 | 0.948 | ok |
| 220 | Lahore | 40 | KSK-Bandala 1 & 2 | 101 | S:S0116@220 | S:S0237@220 | 84.6 | 375.0 | 3.713 | path differs from route by more than 10% |
| 220 | Lahore | 41 | PTPL 1&2 | 47 | — | — |  |  |  | not checked: endpoints not parseable (one or three names) |
| 220 | Lahore | 42 | PTPL 3&4 | 46 | — | — |  |  |  | not checked: endpoints not parseable (one or three names) |
| 220 | Islamabad | 1 | Tarbela - Mardan CCT-I & II | 67 | S:S0036@220 | S:S0027@220 | 61.4 | 66.7 | 0.996 | ok |
| 220 | Islamabad | 2 | Sheikh Muhammadi Peshawar - Mari Daudkhel Cct I & II | 123 | S:S0127@220 | S:S0148@220 | 110.3 | 123.0 | 1.0 | ok |
| 220 | Islamabad | 3 | Mari Daudkhel - Chashnupp Cct I & II | 70 | S:S0148@220 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Islamabad | 4 | Mari Daudkhel - Domale Bannu Cct I & II | 110 | S:S0148@220 | S:S0149@220 | 79.4 | 110.3 | 1.002 | ok |
| 220 | Islamabad | 5 | Sheikh Muhammadi Peshawar - Shahibagh | 38 | S:S0127@220 | S:S0163@220 | 17.3 | 37.6 | 0.988 | ok |
| 220 | Islamabad | 6 | Ghazi Brotha - Nowshera Cct I & II | 45 | S:S0037@220 | S:S0707@220 | 44.1 | 47.2 | 1.048 | ok |
| 220 | Islamabad | 7 | Nowshera - Mardan | 46 | S:S0707@220 | S:S0027@220 | 31.7 | 43.6 | 0.947 | ok |
| 220 | Islamabad | 8 | Peshawar - Nowshera | 50 | S:S0127@220 | S:S0707@220 | 24.9 | 82.4 | 1.648 | path differs from route by more than 10% |
| 220 | Islamabad | 9 | Mardan - Chakdara | 70 | S:S0027@220 | S:S0726@220 | 50.9 | 67.9 | 0.969 | ok |
| 220 | Islamabad | 10 | Chakdara-ShahiBagh | 105 | S:S0726@220 | S:S0163@220 | 75.8 | 110.7 | 1.054 | ok |
| 220 | Islamabad | 11 | Chashnupp - Domale Bannu Cct I & II | 126 | no OSM match | S:S0149@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Islamabad | 12 | Chashnupp - D.I Khan Cct I & II | 84 | no OSM match | S:S0728@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Islamabad | 13 | Allai Khawar - New Mansehra Cct I & II | 83 | no OSM match | S:S0534@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Islamabad | 14 | Tarbela - Burhan Cct I & II | 35 | S:S0036@220 | S:S0152@220 | 29.7 | 33.4 | 0.954 | ok |
| 220 | Islamabad | 15 | Tarbela - Burhan Cct III (RT-2) | 35 | S:S0036@220 | S:S0152@220 | 29.7 | 33.4 | 0.954 | ok |
| 220 | Islamabad | 16 | Burhan - Sangjani (ISPR) Cct 4 (RT-2) | 27 | S:S0152@220 | S:S0405@220 | 26.2 | 27.6 | 1.022 | ok |
| 220 | Islamabad | 17 | Terbela - Sangjani (ISPR) | 63 | S:S0036@220 | S:S0405@220 | 47.7 | 61.0 | 0.968 | ok |
| 220 | Islamabad | 18 | New Rawat - Sangjani (ISPR) | 43 | S:S0049@220 | S:S0405@220 | 39.4 | 46.1 | 1.071 | ok |
| 220 | Islamabad | 19 | New Rawat - Bahria Town | 10 | S:S0049@220 | S:S0153@220 | 8.7 | 10.6 | 1.064 | ok |
| 220 | Islamabad | 20 | Bahria Town - Sangjani (ISPR) | 33 | S:S0153@220 | S:S0405@220 | 32.1 | 35.4 | 1.073 | ok |
| 220 | Islamabad | 21 | New Rawat - Islamabad University Cct I & II | 50 | S:S0049@220 | S:S0430@220 | 29.0 | 49.2 | 0.983 | ok |
| 220 | Islamabad | 22 | Mangla - New Rawat Cct I & II | 80 | ambiguous: P:P0024@220, S:S0054@220 | S:S0049@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Islamabad | 23 | Mangla - New Ghakkar - Kala Shah Kaku (KSK) Cct I | 76 | — | — |  |  |  | not checked: endpoints not parseable (one or three names) |
| 220 | Islamabad | 24 | Mangla - New Ghakkar - Kala Shah Kaku (KSK) Cct III | 76 | — | — |  |  |  | not checked: endpoints not parseable (one or three names) |
| 220 | Islamabad | 25 | Mangla - Gujrat Cct I & II | 78 | ambiguous: P:P0024@220, S:S0054@220 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Islamabad | 26 | Mangla - Kala Shah Kaku (KSK) Cct I & II | 74 | ambiguous: P:P0024@220, S:S0054@220 | S:S0116@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Islamabad | 27 | Sangjani (ISPR) - New Mansehra Cct I & II | 100 | S:S0405@220 | S:S0534@220 | 79.2 | 99.8 | 0.998 | ok |
| 220 | Multan | 1 | Multan - N.G.P.S 1&2 | 14 | S:S0024@220 | S:S0069@220 | 7.0 | 12.5 | 0.889 | path differs from route by more than 10% |
| 220 | Multan | 2 | Multan - T.T singh. 1&2 | 65 | S:S0024@220 | S:S0340@220 | 137.2 | 142.2 | 2.187 | too far (straight line > 1.1 x route); path differs from route by more than 10% |
| 220 | Multan | 3 | TPS-M/Garh-Multan CCT 1&4 | 58 | no OSM match | S:S0024@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 4 | TPS-M/Garh-Multan CCT 3 | 56 | no OSM match | S:S0024@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 5 | TPS-M/Garh-Multan CCT 2 | 55 | no OSM match | S:S0024@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 6 | TPS-M/Garh-M/Garh G/S | 1 | no OSM match | S:S0023@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 7 | M/Garh - Lalpir CCT 1&2 | 18 | S:S0023@220 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 8 | M/garh - Pak Gen CCT 1 | 18 | S:S0023@220 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 9 | M/garh - PARCO CCT 1 | 32 | S:S0023@220 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 10 | M/garh - PARCO CCT 2 | 24 | S:S0023@220 | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 11 | TPS-M/garh-Bahawalpur CCT 1&2 | 109 | no OSM match | S:S0157@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 12 | KAPCO - Multan CCT 3&4 | 100 | no OSM match | S:S0024@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 13 | KAPCO - Multan CCT 5&6 | 79 | no OSM match | S:S0024@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 14 | KAPCO - M/garh CCT 1 | 49 | no OSM match | S:S0023@220 |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 15 | KAPCO - Pak Gen CCT 2 | 67 | no OSM match | no OSM match |  |  |  | not checked: endpoint not mapped |
| 220 | Multan | 16 | Vehari-Multan CCT 1&2 | 79 | S:S0050@220 | S:S0024@220 | 70.9 | 79.1 | 1.001 | ok |
| 220 | Multan | 17 | Vehari - Kassowal CCT 1&2 | 75 | S:S0050@220 | S:S0136@220 | 49.8 | 75.0 | 1.0 | ok |
| 220 | Multan | 18 | Vehari - Chishtian CCT 1&2 | 88 | S:S0050@220 | S:S0364@220 | 68.0 | 87.8 | 0.997 | ok |
| 220 | Multan | 19 | Bahawalpur-Laal Sohanra | 37 | S:S0157@220 | S:S0706@220 | 21.1 | 36.4 | 0.984 | ok |
