# Day 7: generator rules (fixed 18 Nov 2026, before the generator list was built and before any solve)

The values are in `builder/parameters.json` under `generators`. This note gives the reasons. The rules were committed **and pushed to GitHub before** the generator builder first ran, so GitHub's push time dates the order independently of the laptop clock.

## Which plants

- **Included:** IGCEP 2025-35 R2 Annex B-1(i), NGC existing capacity as of Nov 2024. That is 36,424 MW installed and 33,747 MW dependable.
- **Excluded:**
  - **K-Electric's plants (B-1(ii), 2,661 MW).** TSEP models KE as a net export from NTDC (input I2). KE's own plants serve KE's internal load, which isn't in the model.
  - **The 100 MW import from Iran.** It feeds the Makran/Gwadar system, which is off the national grid.
  - **Plants with dependable 0 MW**, such as Neelum Jhelum.

## Snapshot hours (assumptions; TSEP gives no hour)

- **Summer peak:** evening, after sunset. Solar is 0, wind is at dependable.
- **Winter off-peak:** night. Solar is 0, wind is 15% of dependable (an assumption, no source).
- Net-metered solar may move the winter minimum to midday. That isn't modelled.

## Pmax

- **Summer:** IGCEP dependable MW.
  - Bagasse is 0, because summer is outside the crushing season (about November–March) [VERIFY].
- **Winter off-peak:**
  - **Hydro:** 11.3% of dependable. January 2025 hydel generation was 866 GWh ([ProPakistani, 20 Feb 2025](https://propakistani.pk/2025/02/20/power-generation-falls-in-january-2025-despite-22-decline-in-fuel-cost/), citing Arif Habib Ltd). That is a 1,164 MW average, against 10,334 MW of NGC hydro dependable capacity.
  - **Bagasse:** at dependable.
  - **All other thermal and nuclear plants:** at dependable.
- **TSEP may have taken hydro further down.** TSEP Figure 5-9 (winter off-peak, PDF p.70) appears to show Tarbela and Ghazi Barotha at 0 MW [VERIFY by eye]. If so, the 11.3% cap on average energy puts more generation in the north than TSEP's case did.
  - That is reported next to H4. It is **not** tuned away.

## Pmin, reactive limits, costs

- **Source.** All three follow the Microsoft GridSFM US data pipeline (arXiv 2605.04289, §3.4 and Table 13), so the case stays close to the data GridSFM was trained on.
- **Pmin, as a fraction of Pmax:**

  | Type | Fraction |
  |---|---|
  | Nuclear | 50% |
  | Coal | 30% |
  | CCGT | 20% |
  | Engines, gas turbines, hydro and renewables | 0% |

- **Qmax** = Pmax(snapshot) × tan(acos pf), with pf 0.90 for nuclear, 0.85 for coal and gas, 0.80 for hydro and 0.95 for wind and solar.
- **Qmin:** −50% of Qmax for synchronous machines; wind and solar are symmetric.
  - **This rule was chosen for consistency with the GridSFM pipeline, without regard to its effect on H3.**
  - H3's expected bias is recorded in `day6/topology_day6.md`.
- **Costs:**
  - **Thermal c1:** from IGCEP Annex B-2, which is in USD: fuel $/GJ × heat rate GJ/MWh + variable O&M.
    - Plants with two price tranches use the lower one. This understates the cost of Uch and Liberty for most of the month, a minor dispatch effect, logged only.
  - **Fallback c1, from the pipeline's table:** hydro $8/MWh; wind, solar and bagasse 0.
  - c2 = c0 = 0. No exchange rate is needed.

## Where each plant connects

1. **Location:** the OSM plant, or a substation named for it, found by name. Every match is logged in `day7/plant_crosswalk.csv` with its basis.
2. **Bus:** the connection voltage named in a document wins. Those documents are the PSS 44th line tables and the plant labels in TSEP Figure 5-9. Otherwise, take the highest-voltage station bus within 5 km. If there is none within 5 km, take the nearest station bus within 20 km, with the distance logged.
3. **Size check (flag only).** A plant of 500 MW or more below 220 kV, or 1,000 MW or more not at 500 kV, is flagged and resolved in the crosswalk.
4. **Unlocated plants block Day 9.** If they were simply dropped, summer couldn't be supplied: dependable capacity, less solar, bagasse and the Iran import, is about 32,600 MW against a requirement of about 30,300 MW (load + KE + losses + dcline loss). That margin is only about 2,300 MW.
   - GEM's Global Integrated Power Tracker has plant coordinates, but its download form asks for personal details, so **Furqan has to download it**.

## Slack bus

- **Summer:** Tarbela.
- **Winter off-peak:** the bus of the largest-Pmax generator.

## Exit check

- Report installed MW against IGCEP NGC, less the exclusions.
- **The binding check:** located and connected summer Pmax against the summer requirement, by region.
