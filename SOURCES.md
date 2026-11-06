# Source documents — Day 0 (6 Nov 2026)

All files were downloaded on 6 Nov 2026 between 05:00 and 05:02 UTC into `sources/`. Each returned HTTP 200, and each one's first bytes are `%PDF`.
The PDFs are not committed to git because of their size. They are identified by the SHA-256 hashes below; the full log is in `logs/downloads.tsv`.

| File | Publisher, date | Bytes | SHA-256 | Used for |
|---|---|---|---|---|
| `tsep_2024-34_report.pdf` | NTDC via NEPRA, Apr 2024, 166 pp. | 16,470,429 | `253f1ac6f6f5be5dc46c5bee7b4ef4e869f5f20bf60764eba5068e0b9ce2e534` | Inputs I1–I5, holdouts H1–H4 and H8, ratings, line openings (`day0/tsep_check.md`) |
| `per_transmission_fy2024-25.pdf` | NEPRA, 2025 | 3,984,197 | `e8b3be32faeeed63bf270661b07d127c0d20928c4d88596dcd520fda43e41e1c` | S3 station list, S4 circuit-km |
| `per_transmission_2023-24.pdf` | NEPRA, 2024 | 5,636,176 | `f07fa248d193ef93d413aea7beecdd6d9e8db5a8977c32f30f308306131c80c0` | H5 (Gatti), H6 (Table 13 voltages) |
| `igcep_2025-35_r2.pdf` | ISMO via NEPRA, Aug 2025 | 10,235,292 | `d654b17f7cdb486d3a39c74a9e5a75e33df6a5e67ee7c77e61480948c31ba06b` | Day 7 generators: Annex B-1 capacities, B-2 costs |
| `fesco_demand_forecast_2023-33.pdf` | FESCO / NTDC PMS, 2023 | 4,042,598 | `6ab7066f5114c79a6dfa84bdfc33c1b10de979a36dbca316cac41f188d834ccf` | Day 8 loads by grid station (Tables 1-21, 1-22) |
| `mepco_pms_load_forecast_2021-22.pdf` | MEPCO / NTDC PMS, 2021-22 | 5,313,093 | `347b2d574cc414d5101bf10ae0f3a89f6ff5eeb8d6311691b107a02ab6a5a1dd` | Day 8 loads by grid station (Tables 1-28, 1-29) |
| `wb_vre_locational_annex2_grid_integration.pdf` | World Bank / ESMAP (PPI + 8.2), Feb 2021, 4,502 pp. | 116,619,881 | `dcb74b22910d622893bf4fd4fc6c1baf21a637500fbf02eb83d5108f22885cd5` | H7 bus voltages and flows; topology cross-check |

## Source URLs

- TSEP: https://nepra.org.pk/Admission%20Notices/2024/05%20May/TSEP%202024-34%20Report.pdf
- PER FY2024-25: https://www.nepra.org.pk/M&E/PER/Transmission/2025/PER%20Transmission%20FY%202024-25.pdf
- PER 2023-24: https://nepra.org.pk/M&E/PER/Transmission/2024/Performance%20Evaluation%20Report%20of%20Transmission%20Companies%202023-24.pdf
- IGCEP: https://nepra.org.pk/Admission%20Notices/2025/08%20Aug/IGCEP_2025-35_R2.pdf
- FESCO: https://fesco.com.pk/public/mirad/Current%20allocation%20of%20the%20Capacity/FESCO%20Demand%20Forecasting%20Report%202023-2033.pdf
- MEPCO: https://mepco.com.pk/wp-content/uploads/2025/02/MEPCO-Report-PMS-LOAD-FOREACAST-2021-22.pdf
- World Bank Annex 2: https://documents1.worldbank.org/curated/en/897291610742003819/pdf/Annex-2-Grid-Integration-Analysis.pdf

## Not downloaded: needs Furqan's decision

- **NTDC Power System Statistics, 44th edition (2020).** Needed on Day 5 for the station and line tables 2.6, 2.8, 2.16 and 2.17. The only copy found is on a third-party mirror, energyupdate.com.pk. Options: approve the mirror download, or ask NGC for an official copy.
- **Global Energy Monitor, Global Integrated Power Tracker (Sept 2026, CC BY 4.0).** Needed on Day 7 for plant coordinates. The download form asks for name and email, so Furqan has to fill it in himself.
- **TSEP 2025-35 addendum (NEPRA, Aug 2025).** Optional, a newer plan. It's an open NEPRA download at https://www.nepra.org.pk/Admission%20Notices/2025/08%20Aug/TSEP%202025-2035.pdf; not fetched yet.
