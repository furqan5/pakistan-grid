# S3 — NGC station name match (inferred build)

Rule: gate/PREREGISTRATION.md, "S3 match rule". Aliases: gate/s3_aliases.csv. Doubtful pairs are reported, never removed.

- **Scored S3 (name matches, main component): 62 / 69 → FAIL (60-64: decision rule open, see gate)** (pass ≥ 65; no-go < 60)
  - 500 kV: 17 / 20; 220 kV: 45 / 49
  - scored matches that rely on a structural alias: 2
- Name matches anywhere in the build: 62 / 69
- Name + location hints + near-misses (reported only): 64 / 69

| PER station | kV | tier | bus | OSM names | how | lat, lon |
|---|---|---|---|---|---|---|
| Rawat | 500 | hint | S:S0049@500 | 500kV Grid Station | hint: 'Rawat 500 kV' | 33.479319, 73.192047 |
| Peshawar | 500 | scored (name, main component) | S:S0127@500 | Peshawar | name: alias 'peshawar' ~ 'Peshawar' | 33.92884, 71.544454 |
| Gatti | 500 | scored (name, main component) | S:S0028@500 | Gatti | name: alias 'gatti' ~ 'Gatti' | 31.473235, 73.150105 |
| Nokhar | 500 | scored (name, main component) | S:S0083@500 | 500KV Nokhar Grid Station NTDC | name: alias 'nokhar' ~ '500KV Nokhar Grid Station NTDC' | 32.103155, 73.897848 |
| S.K.P | 500 | scored (name, main component) | S:S0079@500 | 500KV Grid Station NTDCL, Sheikhupura | name: alias 'sheikhupura' ~ '500KV Grid Station NTDCL, Sheikhupura' | 31.653688, 74.033384 |
| New Lahore | 500 | scored (name, main component) | S:S0705@500 | New Lahore | name: alias 'new lahore' ~ 'New Lahore' | 31.241536, 73.969077 |
| West FSD | 500 | scored (name, main component) | S:S0765@500 | Faisalabad West | name: alias 'west faisalabad' ~ 'Faisalabad West' | 31.404441, 72.772432 |
| Yousafwala | 500 | scored (name, main component) | S:S0062@500 | Sahiwal | Yousafwala | name: alias 'yousafwala' ~ 'Yousafwala' | 30.668448, 73.1707 |
| Multan | 500 | scored (name, main component) | S:S0024@500 | Multan | name: alias 'multan' ~ 'Multan' | 30.247171, 71.615364 |
| M.garh | 500 | scored (name, main component) | S:S0023@500 | Muzaffargarh | name: alias 'muzaffargarh' ~ 'Muzaffargarh' | 30.101978, 71.16551 |
| D.G. Khan | 500 | scored (name, main component) | S:S0729@500 | Dera Ghazi Khan | name: alias 'dera ghazi khan' ~ 'Dera Ghazi Khan' | 29.997319, 70.471835 |
| RYK | 500 | scored (name, main component) | S:S0213@500 | Rahim Yar Khan | name: alias 'rahim yar khan' ~ 'Rahim Yar Khan' | 28.748437, 70.465789 |
| TPS M.garh | 500 | unmatched | — | — | — | — |
| Dadu | 500 | scored (name, main component) | S:S0051@500 | New Dadu | name: alias 'dadu' ~ 'New Dadu' | 26.717988, 67.743388 |
| Guddu | 500 | scored (name, main component) | S:S0052@500 | Guddu | name: alias 'guddu' ~ 'Guddu' | 28.430738, 69.694247 |
| Jamshoro | 500 | scored (name, main component) | S:S0025@500 | NTDC 500KV Grid Station Jamshoro | name: alias 'jamshoro' ~ 'NTDC 500KV Grid Station Jamshoro' | 25.477619, 68.268765 |
| NKI | 500 | scored (name, main component) | S:S0647@500 | N. K. I | name: alias 'nki' ~ 'N. K. I' | 24.974224, 66.92683 |
| Shikarpur | 500 | scored (name, main component) | S:S0132@500 | Shikarpur | name: alias 'shikarpur' ~ 'Shikarpur' | 28.028068, 68.632007 |
| 747 Guddu | 500 | hint | S:S0207@500 | — | hint: '747 Guddu 500 kV' | 28.424322, 69.703047 |
| Moro | 500 | scored (name, main component) | S:S0690@500 | Moro Converter Station | name: alias 'moro' ~ 'Moro Converter Station' | 26.891215, 68.184153 |
| Bannu | 220 | scored (name, main component) | S:S0149@220 | Bannu | name: alias 'bannu' ~ 'Bannu' | 33.018072, 70.715873 |
| Burhan | 220 | scored (name, main component) | S:S0152@220 | Burhan | name: alias 'burhan' ~ 'Burhan' | 33.825438, 72.619736 |
| Daudkhel | 220 | scored (name, main component) | S:S0148@220 | Daud Khel | name: alias 'daudkhel' ~ 'Daud Khel' | 32.936584, 71.561139 |
| ISPR | 220 | scored (name, main component) | S:S0405@220 | Islamabad Peshawar Road | ISPR | name: alias 'ispr' ~ 'ISPR' | 33.674596, 72.837222 |
| Mardan | 220 | scored (name, main component) | S:S0027@220 | Mardan | name: alias 'mardan' ~ 'Mardan' | 34.158976, 72.03123 |
| Nowshera | 220 | scored (name, main component) | S:S0707@220 | 220 KV Grid Station Nowshera | name: alias 'nowshera' ~ '220 KV Grid Station Nowshera' | 33.937964, 71.81442 |
| Shahibagh | 220 | scored (name, main component) | S:S0163@220 | Shahi Bagh | name: alias 'shahibagh' ~ 'Shahi Bagh' | 34.082207, 71.576268 |
| University | 220 | scored (name, main component) | S:S0430@220 | University Islamabad | name: alias 'university' ~ 'University Islamabad' | 33.739462, 73.16623 |
| Mansehra | 220 | scored (name, main component) | S:S0534@220 | Mansehra | name: alias 'mansehra' ~ 'Mansehra' | 34.336261, 73.155995 |
| Chakdara | 220 | scored (name, main component) | S:S0726@220 | Chakdara | name: alias 'chakdara' ~ 'Chakdara' | 34.61349, 72.092932 |
| D.I. Khan | 220 | scored (name, main component) | S:S0728@220 | Dera Ismail Khan | D.I. Khan | name: alias 'di khan' ~ 'D.I. Khan' | 32.062564, 70.81161 |
| Band | 220 | scored (name, main component) | S:S0114@220 | Bund Road | name: alias 'bund road' ~ 'Bund Road' | 31.512921, 74.251064 |
| Ghakkar | 220 | scored (name, main component) | S:S0102@220 | Ghakhar Grid Station | name: alias 'ghakkar' ~ 'Ghakhar Grid Station' | 32.292601, 74.147735 |
| Jaranwala | 220 | scored (name, main component) | S:S0084@220 | Jaranwala Road | name: alias 'jaranwala' ~ 'Jaranwala Road' | 31.397415, 73.147599 |
| KSK | 220 | scored (name, main component) | S:S0116@220 | Kala Shah Kaku | name: alias 'kala shah kaku' ~ 'Kala Shah Kaku' | 31.764155, 74.257153 |
| Ludewala | 220 | scored (name, main component) | S:S0316@220 | Ludewala | name: alias 'ludewala' ~ 'Ludewala' | 32.177101, 72.6461 |
| N.K.L.P | 220 | scored (name, main component) | S:S0724@220 | New Kot Lakhpat | name: alias 'new kot lakhpat' ~ 'New Kot Lakhpat' | 31.443938, 74.352535 |
| Shalamar | 220 | scored (name, main component) | S:S0119@220 | New Shalamar | name: alias 'shalamar' ~ 'New Shalamar' | 31.590779, 74.385456 |
| Nishatabad | 220 | scored (name, main component) | S:S0232@220 | Nishatabad Grid Station | name: alias 'nishatabad' ~ 'Nishatabad Grid Station' | 31.459299, 73.131667 |
| Ravi | 220 | scored (name, main component) | S:S0117@220 | Ravi | name: alias 'ravi' ~ 'Ravi' | 31.60811, 74.313451 |
| Sammundri | 220 | scored (name, main component) | S:S0142@220 | Samundri Road | name: alias 'sammundri' ~ 'Samundri Road' | 31.279354, 73.086036 |
| Safdar Nagar | 220 | scored (name, main component) | S:S0115@220 | Sarfraz Nagar | name: alias 'sarfraz nagar' ~ 'Sarfraz Nagar' | 31.231691, 73.984708 |
| Sialkot | 220 | unmatched | — | — | — | — |
| Wapda Town | 220 | unmatched | — | — | — | — |
| Ghazi Road | 220 | scored (name, main component) | S:S0118@220 | Ghazi Road | name: alias 'ghazi road' ~ 'Ghazi Road' | 31.538341, 74.492695 |
| Bandial | 220 | scored (name, main component) | S:S0237@220 | Bandala | name: alias 'bandala' ~ 'Bandala' | 31.547498, 73.400797 |
| T.T. Singh | 220 | scored (name, main component) | S:S0340@220 | Toba Tek Singh | name: alias 'toba tek singh' ~ 'Toba Tek Singh' | 31.099327, 72.652413 |
| Gujrat | 220 | unmatched | — | — | — | — |
| Lalian | 220 | scored (name, main component) | S:S0771@220 | Lalian | name: alias 'lalian' ~ 'Lalian' | 31.849724, 72.849241 |
| Kassowal | 220 | scored (name, main component) | S:S0136@220 | Kassowal | name: alias 'kassowal' ~ 'Kassowal' | 30.486046, 72.532065 |
| Okara | 220 | scored (name, main component) | S:S0264@220 | Okara | name: alias 'okara' ~ 'Okara' | 30.759351, 73.509217 |
| Bahawalpur | 220 | scored (name, main component) | S:S0157@220 | Bahawalpur | name: alias 'bahawalpur' ~ 'Bahawalpur' | 29.314313, 71.581995 |
| M.garh | 220 | scored (name, main component) | S:S0023@220 | Muzaffargarh | name: alias 'muzaffargarh' ~ 'Muzaffargarh' | 30.101978, 71.16551 |
| Vehari | 220 | scored (name, main component) | S:S0050@220 | وہاڑی | Vehari | name: alias 'vehari' ~ 'Vehari' | 30.074971, 72.325692 |
| Chistian | 220 | scored (name, main component) | S:S0364@220 | Chishtian | name: alias 'chistian' ~ 'Chishtian' | 29.755276, 72.927379 |
| Lal Sohanra | 220 | scored (name, main component) | S:S0706@220 | Lal Sohanra | name: alias 'lal sohanra' ~ 'Lal Sohanra' | 29.284514, 71.796537 |
| NGPS | 220 | scored (name, main component) | S:S0069@220 | NGPS Multan | name: alias 'ngps' ~ 'NGPS Multan' | 30.207635, 71.558623 |
| Hala Road | 220 | scored (name, main component) | S:S0126@220 | 220KV NTDC Grid Station Hala Road | name: alias 'hala road' ~ '220KV NTDC Grid Station Hala Road' | 25.42513, 68.382986 |
| Rohri | 220 | scored (name, main component) | S:S0140@220 | Rohri New | name: alias 'rohri' ~ 'Rohri New' | 27.666968, 68.966479 |
| T.M.K | 220 | scored (name, main component) | S:S0618@220 | Tando Muhammad Khan Road | name: alias 'tando muhammad khan' ~ 'Tando Muhammad Khan Road' | 25.359737, 68.393283 |
| Daharki | 220 | scored (name, main component) | S:S0058@220 | Daharki | name: alias 'daharki' ~ 'Daharki' | 27.978946, 69.673362 |
| Jhimpir 1 | 220 | scored (name, main component) | S:S0650@220 | Jhimpir | name: alias 'jhimpir' ~ 'Jhimpir' | 25.113565, 67.868661 |
| Jhimpir 2 | 220 | scored (name, main component) | S:S0772@220 | Jhimpir II | name: alias 'jhimpir 2' ~ 'Jhimpir II' | 25.049146, 67.865647 |
| S.Y. Guddu | 220 | scored (name, main component) | S:S0052@220 | Guddu | name: alias 'guddu' ~ 'Guddu' | 28.430738, 69.694247 |
| Quetta | 220 | scored (name, main component) | S:S0048@220 | Quetta | name: alias 'quetta' ~ 'Quetta' | 30.069467, 66.980851 |
| Sibbi | 220 | scored (name, main component) | S:S0133@220 | Sibbi | name: alias 'sibbi' ~ 'Sibbi' | 29.517422, 67.855816 |
| Khuzdar | 220 | scored (name, main component) | S:S0099@220 | Khuzdar | name: alias 'khuzdar' ~ 'Khuzdar' | 27.763057, 66.628394 |
| Loralai | 220 | unmatched | — | — | — | — |
| D.M. Jamali | 220 | scored (name, main component) | S:S0736@220 | Dera Murad Jamali | name: alias 'dera murad jamali' ~ 'Dera Murad Jamali' | 28.606863, 68.165383 |
