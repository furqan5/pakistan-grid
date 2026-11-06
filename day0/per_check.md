# Day 0 — NEPRA PER by-eye check of the gate's structural and voltage numbers

Checked on 6 Nov 2026 against the rendered pages. "PDF p." is the PDF page index.

## PER FY2024-25 (`per_transmission_fy2024-25.pdf`)

**Section 2.2 and Figure 1 "NGC Transmission System" (PDF p.18, printed p.13).** The text gives 20 grid stations at 500 kV and 49 at 220 kV, with 9,313 km of 500 kV and 11,933 km of 220 kV lines.
Figure 1 names all 69 stations by region:
- **500 kV (20)**
  - Islamabad: Rawat, Peshawar.
  - Lahore: Gatti, Nokhar, S.K.P, New Lahore, West FSD, Yousafwala.
  - Multan: Multan, M.garh, D.G. Khan, RYK, TPS M.garh.
  - Hyderabad: Dadu, Guddu, Jamshoro, NKI, Shikarpur, 747 Guddu, Moro.
- **220 kV (49)**
  - Islamabad (11): Bannu, Burhan, Daudkhel, ISPR, Mardan, Nowshera, Shahibagh, University, Mansehra, Chakdara, D.I. Khan.
  - Lahore (20): Band, Ghakkar, Jaranwala, KSK, Ludewala, N.K.L.P, Shalamar, Nishatabad, Ravi, Sammundri, Safdar Nagar, Sialkot, Wapda Town, Ghazi Road, Bandial, T.T. Singh, Gujrat, Lalian, Kassowal, Okara.
  - Multan (6): Bahawalpur, M.garh, Vehari, Chistian, Lal Sohanra, NGPS.
  - Hyderabad (7): Hala Road, Rohri, T.M.K, Daharki, Jhimpir 1, Jhimpir 2, S.Y. Guddu.
  - Quetta (5): Quetta, Sibbi, Khuzdar, Loralai, D.M. Jamali.

This is the **S3 name list**.

Tarbela and Sheikh Muhammadi are 500 kV buses in PER 2023-24 Table 13 and in TSEP, but they are **not** in this NGC list. Tarbela is a generating switchyard. They should be modelled, but they don't count toward S3's 69.

**Table 1 "Progressive NGC Network Statistics" (PDF p.19, printed p.14), source NGC/DXP**

| | 2023-24 | 2024-25 |
|---|---|---|
| Grid stations 500 / 220 kV | 19 / 50 | 20 / 49 |
| Circuit km 500 kV | 9,201 | **9,313** |
| Circuit km 220 kV | 12,136 | **11,933** |
| Transformation MVA, total | 64,410 | **66,630** |

This confirms the gate's S4 inputs: NGC 9,313 km at 500 kV, and 11,933 km at 220 kV plus KE's 467 km, about 12,400 km.
It also confirms the source conflict noted in the report: PER 2023-24 itself reported 9,577 and 12,639 km for 2023-24, while this table restates them as 9,201 and 12,136.

## PER 2023-24 (`per_transmission_2023-24.pdf`)

**Table 13 "Highest voltage incidents recorded at 500 kV grid station under Normal condition" (PDF p.29, printed p.18 of 91)**

| Region | Station | kV | Duration (min) |
|---|---|---|---|
| Multan | Multan | **580** | 180 |
| Multan | D.G. Khan | **559** | 1260 |
| Multan | RY Khan | 552 | 1350 |
| Lahore | WFSD | 546 | 540 |
| Lahore | Gatti | 545 | 180 |
| Lahore | Yousafwala | 546 | 90 |
| Lahore | Sheikhupura | 532 | 60 |
| Lahore | Nokhar | 538 | 240 |
| Lahore | New Lahore | 538 | 180 |
| Islamabad | Tarbela | 543 | 180 |
| Islamabad | Sheikh Muhammadi | 543 | 180 |
| Hyderabad | 747 Guddu | **551** | 60 |
| Hyderabad | Guddu | 549 | 60 |
| Hyderabad | Dadu | 545 | 60 |
| Hyderabad | Shikarpur | 549 | 180 |
| Hyderabad | NKI Karachi | 543 | 30 |
| Hyderabad | Jamshoro | 545 | 30 |

This confirms H6: Multan 580, D.G. Khan 559 and 747 Guddu 551 kV.
These are recorded **incidents**, the highest values in the year. They are not a snapshot, which is why H6 is reported only.

The same page gives the normal band as ±5% (475–525 kV and 209–231 kV) and the N-1 band as ±10%. This confirms register row 28: PER's normal band is stricter than TSEP's +8%/−5%.

**Result: no gate number changes.** The gate's S3, S4 and H6 values all match the source pages.
