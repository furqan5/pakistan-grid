# NGC data request: draft, NOT SENT (23 Nov 2026)

This replaces section 1 of `data_requests_DRAFT.md`. It is for Furqan to check, edit and send himself.
- Square brackets mark things to fill in or verify.
- Send it by email and, if possible, as a printed letter to the Power System Planning office in Lahore.

---

**To:** General Manager, Power System Planning, National Grid Company of Pakistan (formerly NTDC), [office address, WAPDA House, Lahore: VERIFY]
**Email:** cetrp@ntdc.com.pk [VERIFY: printed in a 2021 paper, before the NGC rename; confirm on the NGC website or by phone]
**Subject:** Research request: five factual questions about the 500/220/132 kV network, from an open-data model test

Dear Sir/Madam,

I am an electrical/energy engineer in Lahore. Over the past three weeks I have built a 500/220/132 kV power-flow model of Pakistan's transmission network using only public data. The aim was to test Microsoft's open-source GridSFM, an AI model that approximates AC optimal power flow, on a grid it has not seen before.

**Sources.** The model uses:
- OpenStreetMap for the network;
- TSEP 2024-34 base-case totals and ratings;
- NEPRA's transmission Performance Evaluation Reports;
- IGCEP 2025-35 for generation;
- the 44th Power System Statistics for line and station data.

**How the test was run.** I wrote the pass and fail rules before running it, and published every rule and result openly as I went: [github.com/furqan5/pakistan-grid].

**What matched.** The 500 kV network agrees closely with NGC's own figures: 9,310 circuit-km in the model against 9,313 in NEPRA's FY2024-25 report.

**What failed.** The model could not be solved for either the July/August 2026 summer peak or the January 2027 winter off-peak. The causes are specific, and they are what this letter asks about:
1. **Chashma.** About 1.4 GW from the Chashma nuclear and hydro plants leaves through a 1.3 km 220 kV section ("C-1/C-2 PP – Ludewala") that the public map records as a single circuit, inside a double-circuit corridor.
2. **Lahore 132 kV.** In the Lahore area the model has too little 220/132 kV supply. It ends up pushing bulk power through the 132 kV network, worst on a 2 km single-circuit 132 kV link into the Manga grid station.
3. **Missing 220 kV links.** Three double-circuit 220 kV lines listed in the 44th Power System Statistics (2019) are missing from the public map or only partly mapped: Samundari Road–Nishatabad, New Kot Lakhpat–Bund Road and KSK–Bandala.

I am not asking for confidential base cases. I would be grateful for answers to the factual questions below, even partial ones:
1. **Chashma.** How many circuits run on the 220 kV section between the Chashma C-1/C-2 switchyard and the Chashma–Ludewala line, and on the C-3/C-4 connection? Which conductor do they use?
2. **Lahore 220/132 kV supply.** Which 220 kV grid stations supply the 132 kV network south-west of Lahore, around Manga and Raiwind, and what 220/132 kV transformer capacity is installed at each?
3. **The three 220 kV lines.** Are Samundari Road–Nishatabad, New Kot Lakhpat–Bund Road and KSK–Bandala still in service as double-circuit lines, or have they been looped in elsewhere since 2019?
4. **Conductors and ratings.** Which conductor and normal rating does NGC usually assume for 132 kV and 220 kV lines in planning studies? Is Lynx still common at 132 kV, and single Rail at 220 kV?
5. **Station names.** Are the following the same stations?
   - "Safdar Nagar" (NEPRA's 220 kV list) and "Sarfaraz Nagar";
   - "Bandial" and "Bandala";
   - the 500 kV "Peshawar" station and Sheikh Muhammadi.

**If NGC is willing to go further,** a reduced 500/220/132 kV equivalent of a TSEP 2024-34 base case would settle all of this. Even the bus-branch topology with ratings but without impedances would help. I would sign any confidentiality undertaking you require. I would publish only aggregate results, and only with NGC's written agreement.

**What I can offer in return:**
- the full open model;
- a list of the gaps and errors I found in the public map, which I would also correct on OpenStreetMap;
- a short briefing for your team if that is useful.

I am in Lahore and can visit the office at a time that suits you.

Yours faithfully,

Furqan Shakeel
[phone] · [email]
[LinkedIn profile URL]

---

## Notes for Furqan (not part of the letter)

- **Facts in the letter, and where they come from:**

  | Fact | Source |
  |---|---|
  | 9,310 vs 9,313 circuit-km | `gate/G1_log.md`, PER FY2024-25 Table 1 |
  | The Chashma section and its tags | OSM way named "C-1/C-2 PP – Ludewala (Chashma PP – Ludewala)", `cables=3` |
  | The Manga link | `day9/topology_day9.md` |
  | The three PSS lines | PSS 44th Table 2.8, Lahore rows 9, 20 and 40 |
  | The three station pairs | `gate/s3_aliases.csv` |

- **Questions 2 and 3 are the ones that would matter most** if a repair round 2 is ever run. They address the pocket that still binds.
- **A shorter LESCO version** (question 2 only, plus LESCO's Power Market Survey station loads) would also help, because the binding pocket is inside LESCO.
- **The repository is public.** If you'd rather NGC read the findings in a document than on GitHub, attach a two-page PDF summary. It can be made from `README.md` and `day9/topology_day9.md`.
