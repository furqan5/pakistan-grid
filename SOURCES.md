# Source documents — Day 0 (6 Nov 2026)

The first seven files were downloaded on 6 Nov 2026 between 05:00 and 05:02 UTC into `sources/`. PSS 44th was downloaded on 16 Nov 2026. Each returned HTTP 200, and each one's first bytes are `%PDF`.
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
| `ntdc_pss_44th_2020.pdf` | NTDC Power System Planning, Power System Statistics 44th ed., Mar 2020 (data to 30 Jun 2019), 94 pp. **Third-party mirror** (Energy Update); downloaded 16 Nov 2026 18:29 UTC with Furqan's approval | 3,678,369 | `24235bdc8e74020a747d9c8e141f662c7c9d7cdd82c8bde2f9d19e6a5649bf3f` | Day 5: S3 name aliases, per-line circuit cross-check (not an S4 reference). Checks in `day5/pss_check.md` |

**PSS 44th provenance.** There is no NTDC-hosted copy to compare the hash with. What was checked:
- the title page reads "National Transmission & Despatch Company, Power System Statistics 44th Edition, March 2020, Power System Planning, NTDC";
- 94 pages;
- produced by Acrobat Distiller 11.0, created 20 Mar 2020 PKT;
- no JavaScript and not encrypted.

The tables are extracted by `builder/extract_pss44.py` into `sources/extracted/pss44_*.csv`.

## Source URLs

- TSEP: https://nepra.org.pk/Admission%20Notices/2024/05%20May/TSEP%202024-34%20Report.pdf
- PER FY2024-25: https://www.nepra.org.pk/M&E/PER/Transmission/2025/PER%20Transmission%20FY%202024-25.pdf
- PER 2023-24: https://nepra.org.pk/M&E/PER/Transmission/2024/Performance%20Evaluation%20Report%20of%20Transmission%20Companies%202023-24.pdf
- IGCEP: https://nepra.org.pk/Admission%20Notices/2025/08%20Aug/IGCEP_2025-35_R2.pdf
- FESCO: https://fesco.com.pk/public/mirad/Current%20allocation%20of%20the%20Capacity/FESCO%20Demand%20Forecasting%20Report%202023-2033.pdf
- MEPCO: https://mepco.com.pk/wp-content/uploads/2025/02/MEPCO-Report-PMS-LOAD-FOREACAST-2021-22.pdf
- World Bank Annex 2: https://documents1.worldbank.org/curated/en/897291610742003819/pdf/Annex-2-Grid-Integration-Analysis.pdf
- PSS 44th (mirror): https://www.energyupdate.com.pk/wp-content/uploads/2020/08/NTDCL-PSS-44th-Edition-March-202.pdf

## OpenStreetMap power data (Day 2)

- **Source:** the Overpass API, queries in `osm/queries/`, area `ISO3166-1=PK`, admin_level 2.
  - The area includes AJK and GB: the boundary check returned Muzaffarabad, Mirpur, Gilgit and Skardu.
  - Retrieval time, endpoint, `timestamp_osm_base`, bytes and SHA-256 for each file are in `logs/osm_fetch.tsv`.
  - The raw JSON is in `osm/raw/` and isn't committed because of its size.
- **Licence:** © OpenStreetMap contributors, **ODbL 1.0** (https://www.openstreetmap.org/copyright). Any derived network that is released (bus/branch tables, PowerModels JSON) must carry ODbL share-alike and this attribution.

## Not downloaded: needs Furqan's decision

- **Global Energy Monitor, Global Integrated Power Tracker (Sept 2026, CC BY 4.0).** Needed on Day 7 for plant coordinates. The download form asks for name and email, so Furqan has to fill it in himself.
- **TSEP 2025-35 addendum (NEPRA, Aug 2025).** Optional, a newer plan. It's an open NEPRA download at https://www.nepra.org.pk/Admission%20Notices/2025/08%20Aug/TSEP%202025-2035.pdf; not fetched yet.
