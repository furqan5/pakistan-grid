# Pakistan transmission grid from public data, for a GridSFM zero-shot test

This repository builds a synthetic AC power-flow model of Pakistan's 500/220/132 kV transmission network from public data only. The goal is to test Microsoft's [GridSFM](https://github.com/microsoft/GridSFM) optimal-power-flow model zero-shot on it. GridSFM only accepts grids of 500 buses or more, and no such Pakistan case is public, so the model has to be built first.

It is a two-week side research project with a pre-registered go/no-go gate. It is **not** an official NTDC/NGC model and should not be used for planning or operations.

## Status (18 Nov 2026)

- **Days 0–8 of 14 are done:** sources, GridSFM install check, topology builder, station matching, line/transformer/shunt parameters, generators (IGCEP plants placed via OSM and GEM) and loads. **Gate v1.0 signed off 18 Nov 2026.**
- **Gate** (`gate/PREREGISTRATION.md`): **v1.0**, signed off before any solve. The choices made after their result was known are labelled post hoc.
- **Structure checks** (`gate/G1_log.md`):
  - S1 passes: 904 buses without K-Electric, 924 with.
  - S2 passes (load 100%, generation 99.8%), **but largely by construction**: loads and generators are only placed on the main component. Without that filter, the report-only counterfactual is load 97.6%, which is **below** the 98% mark, and generation 99.5%.
  - S3 fails: 62 of 69 NGC stations matched by name, against a pass mark of 65. That is above the no-go line of 60, so the test continues as "synthetic Pakistan-topology".
  - S4 passes: circuit-km at 500 kV −0.1% and at 220 kV +3.6% against NEPRA.
- **No power-flow solve has been run yet.** The rules that affect the scored holdouts were committed before any model quantity was computed.
  - For Days 0–6 that order rests on commit dates set on the author's laptop. The repository was first pushed on 18 Nov 2026.
  - From Day 7 on, each rules commit is pushed to GitHub **before** the run that uses it, so GitHub's push time dates the order independently.

## Method in one paragraph

Lines, substations and plants come from OpenStreetMap through Overpass (`osm/queries/`). `builder/build_topology.py` turns them into a bus–branch network: station grouping, endpoint snapping, voltage levels, series-joint collapse, transformer stubs and the HVDC link. Station names are matched to NEPRA's list of NGC grid stations under a fixed rule (`builder/score_s3.py`, `gate/s3_aliases.csv`). Line lengths are cross-checked against NTDC's Power System Statistics (`builder/check_pss_lines.py`). Electrical parameters follow `builder/parameters.json`, applied by `builder/make_parameters.py`:
- line R/X/B from conductor datasheets;
- ratings from NTDC's TSEP 2024-34 contingency tables;
- reactor totals from TSEP's base cases.

The daily notes in `day0/` … `day6/` record each decision and why it was made.

## Reproducing

1. **Fetch OSM data.** Run the Overpass queries in `osm/queries/`. The full lines query times out, so use the six `lines_tile*` queries and merge them. Save the results as `osm/raw/{lines,substations,plants}.json`.
2. **Get the source PDFs.** Download them from the URLs in `SOURCES.md` into `sources/` and check them against the SHA-256 values in `logs/downloads.tsv`.
3. **Run the pipeline.** Python 3.12 with numpy, scipy, shapely and networkx:

   ```
   python builder/build_topology.py --no-infer     # scored build -> osm/build/explicit
   python builder/build_topology.py                # inferred-voltage sensitivity build
   python builder/score_s3.py --selftest
   python builder/score_s3.py osm/build/explicit
   python builder/check_pss_lines.py osm/build/explicit
   python builder/make_parameters.py osm/build/explicit
   python builder/extract_pss44.py        # PSS 44th tables -> sources/extracted/
   python builder/extract_igcep.py        # IGCEP Annex B-1(i), B-2 -> sources/extracted/
   python -I builder/extract_gem.py        # GEM trackers -> sources/extracted/gem_pk.csv (needs openpyxl)
   python builder/make_generators.py osm/build/explicit
   python builder/extract_disco_tables.py # FESCO/MEPCO station demand -> sources/extracted/
   python builder/make_loads.py osm/build/explicit
   ```

   The extractors use xpdf `pdftotext -table`.

The OSM extract, source PDFs and generated CSVs are not committed, because of their size and their licences.

## Sources

The main documents are listed in `SOURCES.md`, with URLs and hashes:
- NTDC's Transmission System Expansion Plan 2024-34;
- NEPRA's Performance Evaluation Reports for transmission (FY2023-24, FY2024-25);
- ISMO's IGCEP 2025-35;
- NTDC's Power System Statistics, 44th edition (a third-party mirror, as no NTDC-hosted copy was found);
- FESCO and MEPCO load-forecast reports;
- the World Bank's VRE grid integration annex.

None of them is redistributed here. `sources/extracted/` holds tables transcribed from the Power System Statistics booklet, with its known defects recorded in `day5/pss_check.md`.

## Licences

- **Code** (`builder/`): MIT, see `LICENSE`.
- **Network data derived from OpenStreetMap**, including the build reports and any bus/branch tables or PowerModels JSON released later: © OpenStreetMap contributors, available under the [Open Database License (ODbL) 1.0](https://www.openstreetmap.org/copyright). Derived databases must keep this attribution and stay under ODbL.
- **Plant coordinates and `sources/extracted/gem_pk.csv`** come from Global Energy Monitor's Hydropower, Wind, Solar and Bioenergy trackers: © Global Energy Monitor, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- **Figures and tables taken from NTDC, NEPRA, ISMO and DISCO documents** remain those publishers' material. They are cited, not relicensed.

## Author

Furqan Shakeel, Lahore. Feedback and corrections are welcome as issues, especially from anyone who knows the NGC network or the stations marked [VERIFY].
