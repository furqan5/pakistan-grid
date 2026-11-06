# Data-request drafts — NOT SENT

These are drafts for Furqan to edit and send himself. Square brackets mark things to fill in or check.
Send the NGC one first. Wait until the gate passes S1–S3 before sending a follow-up with the synthetic model attached.

---

## 1. NGC (ex-NTDC) Transmission / Power System Planning, Lahore

**To:** cetrp@ntdc.com.pk [VERIFY — printed in Energies 2021, before the NGC rename; check on ntdc.gov.pk or by phone]
**Subject:** Research request — TSEP 2024-34 base cases for an AC-OPF model test

Dear Sir/Madam,

I am an energy engineer in Lahore [affiliation / programme]. I am testing Microsoft's open-source GridSFM model, a neural network that predicts AC optimal power flow results, on Pakistan's transmission system. To my knowledge it has never been tested on a South Asian grid.

I am building a synthetic 500/220/132 kV model from public sources. These are OpenStreetMap, NEPRA's Performance Evaluation Reports, IGCEP 2025-35 and the TSEP 2024-34 system summaries (Tables 5-1, 5-8 and 5-10). It will be checked only against system-level totals such as losses, line charging and the winter generator absorption. Line impedances are estimated from conductor datasheets.

Could NGC Planning share either of the following for research use?
1. The July/August 2026 summer peak and January 2027 winter off-peak PSS/E base cases used in TSEP 2024-34; or
2. A reduced 500/220/132 kV equivalent of those cases.

I would sign any confidentiality undertaking you need. I would publish only aggregate error statistics, and only with NGC's written agreement. I would also share the synthetic model and the test results with your team. That may be useful as an independent check of NGC's model against open data.

I am in Lahore and can come to the office if that is easier.

Regards,
Furqan Shakeel
[phone] · [email]

---

## 2. Power Planners International, Lahore

**To:** [find the contact address on the PPI website]
**Subject:** Question about NTDC network modelling conventions — research project

Dear [name],

I am an energy engineer in Lahore. I am building an open-data AC power-flow model of Pakistan's 500/220/132 kV grid to test Microsoft's GridSFM AC-OPF model.

PPI did the PSS/E work behind the World Bank VRE Locational Study (Annex 2, 2021), so you would know NTDC's modelling conventions better than anyone. I have two questions:
1. Which conductor types and per-km R/X/B values does NTDC typically use for 500 kV quad-bundle and 220 kV twin-bundle lines?
2. Do you know of any reduced equivalent of the NTDC system that can be shared for research?

I'd be glad to share the finished model and results with you.

Regards,
Furqan Shakeel

---

## 3. NUST USPCAS-E — authors of Khan et al., Energies 14(8):2283 (2021)

**To:** [corresponding author's email, from the paper's first page]
**Subject:** Your 3,651-bus NTDC MATPOWER model (Energies 2021)

Dear Dr [name],

I read your 2021 Energies paper, which converted NTDC's PSS/E cases to MATPOWER (3,651 buses for 2018 and 6,007 for 2025). I am testing Microsoft's GridSFM AC-OPF model on Pakistan's grid and am building a synthetic model from public data.

I understand the NTDC data cannot be shared without NTDC's consent. Could you tell me two things?
1. Whether NTDC agreed to any research sharing, and through which office.
2. Whether your PSS/E-to-MATPOWER conversion scripts could be shared, since they contain no NTDC data.

Regards,
Furqan Shakeel

---

## 4. University of Bath — Banatwala, Gu & Pei (IET 2025)

**To:** [corresponding author's email, from the manuscript]
**Subject:** Your 173-bus Pakistan 2029 AC/DC case (IET 2025)

Dear [name],

I read your paper on machine-learning-guided OPF for weak hybrid AC/DC grids, which used a 173-bus Pakistan case with the Matiari–Lahore HVDC link. I am building an open-data Pakistan model to test Microsoft's GridSFM.

Could you say where the case data came from? Could the 173-bus case be shared for cross-checking the 500/220 kV backbone? I'd keep it out of anything I publish unless you agree otherwise.

Regards,
Furqan Shakeel

---

## 5. LESCO Planning Department

**To:** [LESCO planning / Power Market Survey section — by letter or in person]
**Subject:** Request for the latest Power Market Survey demand-forecast report

FESCO and MEPCO publish their Power Market Survey demand-forecast reports, which give grid-station MVA and maximum demand. I am asking for LESCO's latest equivalent for an academic power-flow study. I'd use only the grid-station loads, aggregated.

---

## 6. GitHub — PyPSA-PAK author (Abdul-Karim786) and OpenGridPK (saddamchandio)

Short issue or message:
> "I'm building a PowerModels/AC-OPF model of Pakistan's 500/220/132 kV grid from OSM to test Microsoft's GridSFM. Would you share your latest network files, voltage overrides or validation notes? I'll contribute OSM tag fixes back via MapYourGrid and credit your work."
