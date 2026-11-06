# Day 1 — GridSFM-Open model test on Windows

Run on 6 Nov 2026 on Furqan's laptop: Windows 11, 8 logical CPUs, NVIDIA Quadro M2000M with 4 GB. Inference here ran on the CPU; GPU results are in the last section.
Logs are in `logs/` (`model_setup.log`, `infer_samples.log`, `case6470_pipeline.log`, `eval_case6470.log`, `eval_delaware.log`, `gen_perturbed_delaware.log`).

## Stack

| Item | Value |
|---|---|
| Python venv | `C:\Users\furqa\src\GridSFM\model\.venv`, Python 3.12.10 |
| Packages | torch 2.8.0+cpu, torch_geometric 2.8.1, numpy 2.5.4, scipy 1.18.1, huggingface_hub 0.36.2, gridsfm 1.1.0 (editable, repo commit `1ca775f`) |
| Checkpoint | `microsoft/GridSFM_Open` file `gridsfm_open_v1.1.pt`, 61,061,952 bytes, SHA-256 `f8a43961…5fd831`. `load_model` checks the checkpoint's built-in hash when it loads. |

## 1. Shipped samples: install sanity check, not a generalisation test

`examples/infer_samples.py` ran on all 53 `model/samples` grids (500–3,889 buses). These are the **unperturbed base cases of the training grids**: 23 pglib cases and 30 `msr_` US regions. They test that the Windows install gives sane numbers, not generalisation.

| Metric | Result |
|---|---|
| Cost MAPE | median **0.40%**, mean 0.61%, max 2.86% (`msr_new_york`) |
| Feasibility accuracy | 53 / 53 |
| V MAE | 0.0030 pu |
| θ MAE | 0.021 rad (1.2°) |
| Pg MAE | 0.017 pu |
| Qg MAE | 0.049 pu |
| CPU time | 16 s preparation + 115 s for one batched forward over all 53 graphs |

The model card's **held-out perturbed** test set reports a median cost gap of 2.4%. Training-grid base cases should come out better than that, and they do.

## 2. Unseen grid: pglib case6470_rte through our own pipeline

This is the path the Pakistan model will take: raw case → Julia pipeline → `.pyg.json` → model.

- **Source:** `pglib_opf_case6470_rte.m` from power-grid-lib/pglib-opf v23.07, SHA-256 `7aa5946a…4c5fff`.
- **Conversion:** `PowerModels.parse_file` → `JSON.print` (`gridsfm-runs/m_to_json.jl`). The output is **plain PowerModels JSON with no extra fields**. `patch_model.jl` said "no patching needed" and `solve_topo_json.jl` accepted it.
  - **Answer to the Day 1 field question:** the Pakistan builder only needs to write standard PowerModels JSON. The pipeline adds `_relaxation` and `_dc_shunts_injected` itself.
- **Solve ladder:**
  - **L0 (strict):** Ipopt returned `TIME_LIMIT` after 1,148 s. The per-level wall limit is 900 s (`run_opf_relaxation.jl:262`).
  - **AC1:** `LOCALLY_SOLVED` in 86 s, objective 2,233,800.81, after these changes:
    - voltage bounds widened to [0.90, 1.10] on 5,651 buses;
    - Q limits ×1.5 on 761 generators;
    - **DC-derived shunts injected: 73 → 5,671 shunts, net Bs 1,082 → 19,841 MVAr.**
- **Export:** strict AC-OPF re-solve, `LOCALLY_SOLVED`, 63.6 s, `feas=true`.
- **Total wall time:** about 24 minutes, mostly the L0 time-out.

GridSFM zero-shot on this unseen grid, scored with the same metric code as `infer_samples.py`:

| Metric | case6470_rte (unseen) | Training-grid samples (mean) | Ratio |
|---|---|---|---|
| Cost MAPE | 2.54% | 0.61% | ×4 |
| V MAE (pu) | 0.0314 | 0.0030 | ×10 |
| θ MAE (rad) | 0.137 (7.8°) | 0.021 | ×7 |
| Pg MAE (pu) | 0.114 | 0.017 | ×7 |
| Qg MAE (pu) | 0.441 | 0.049 | ×9 |
| Feasibility | p = 0.398 → **wrongly called infeasible** (label: feasible) | 53/53 correct | — |
| CPU inference time | 6.2 s (including preparation) | — | — |

**Against Microsoft's blog** (case6470_rte zero-shot: about 14% cost error, every scenario flagged infeasible):
- The **feasibility failure is reproduced**.
- Our cost error is **lower (2.5%)**, but the two aren't like for like. Microsoft scored perturbed OPFData test scenarios of the original grid. We scored one base case of the **AC1-relaxed grid, with 18.8 GVAr of shunts added**.
- The state errors (V, θ, Qg) are 7–10× worse than in distribution. That confirms it really is out of distribution.

## 3. Hand-off from pipeline exports to the model

Delaware's `delaware_base.pyg.json` and the 6 scenario files from `gen_perturbed_data.jl` all load, prepare and run.
Results are meaningless because Delaware has 33 buses, below the 500-bus floor:
- every feasible scenario got p(feasible) of 0.003–0.013;
- cost errors ran 2.6–49%.

This confirms the floor on real numbers.

## 4. Scenario generator on Windows

`gen_perturbed_data.jl` ran directly (no `taskset`) with 2 Distributed workers on Delaware at n = 1 per mode. It wrote all 6 files in 77 s.
The `loads` scenario came out infeasible: load scaling up to 1.5×. The generator is designed to produce such labelled infeasible cases.

## Consequences for the gate (proposals for Furqan, not yet applied)

1. **AC1 isn't a mild relaxation.** On case6470 it added 5,598 shunts and 18.8 GVAr net. If the Pakistan case reaches AC1, the reactive holdout H3 (net generator Q) and the loss holdouts would partly score the injected shunts, not the grid that was built. Proposal:
   - record `_dc_shunts_injected` (count and MVAr) under V1/V2;
   - if more than a small threshold is added (for example 5% of the TSEP shunt totals), label H1, H3 and H4 "post-relaxation";
   - or require L0 for a "Pakistan-calibrated" go.
2. **Time limit.** L0 timed out on this laptop at 6,470 buses. A Pakistan case of 500–1,500 buses should solve in well under 900 s, but log the solve time. Run long solves overnight, or raise `WALL_TIME_LIMIT` before any solve (it's a pre-run setting, so changing it doesn't leak a holdout).
3. **G4 baseline.** Microsoft's own path takes the unseen case6470 to wrong feasibility calls and state errors about 10× in-distribution. A similar Pakistan result is expected and isn't evidence of bad grid data on its own. Score the EHV and 132 kV subsets separately, as already planned.

## GPU

**Result: the laptop's GPU can't run GridSFM with the torch versions it allows.**

- **GPU:** NVIDIA Quadro M2000M, 4 GB, Maxwell, compute capability **sm_50**. Driver 573.44 supports CUDA 12.8.
- **Build tried:** torch 2.8.0+cu126 for Windows, a 2.9 GB wheel, in a separate venv `.venv-cuda`. The CPU venv is untouched. `torch.cuda.is_available()` returned True, but the build's arch list is `sm_61 sm_70 sm_75 sm_80 sm_86 sm_90`.
- **Failure:** the first kernel failed with "no kernel image is available for execution on the device". torch's own warning gives a minimum capability of 6.1. So the Windows cu126 wheel of 2.8 does not include Maxwell, contrary to what PyTorch's dev-discuss notices suggested for cu126 in general.
- **Remaining route [VERIFY]:**
  - GridSFM pins torch ≥2.6 and <2.9, so the only option is a 2.6 or 2.7 build against CUDA 11.8 (for example torch 2.7.1+cu118), if those Windows wheels still ship sm_50. That's another ~2.7 GB download.
  - The alternative is building torch from source with `TORCH_CUDA_ARCH_LIST=5.0`, which takes hours.
- **Why it isn't worth it:** CPU timings per grid (`logs/timing_cpu.log`, forward pass only):
  - 500 buses 0.47 s; 661 buses 0.73 s; 3,374 buses 2.0 s; 3,889 buses 4.2 s; 6,470 buses 5.2 s.
  - A Pakistan-sized grid takes under 1 s per scenario, so 1,000 scenarios take about 12 min.
  - The bottleneck is the Julia/Ipopt AC-OPF, which is CPU-only. A 4 GB Maxwell GPU would save minutes at most.
- **Recommendation:** stay on CPU. Revisit only if fine-tuning ever becomes possible on custom data, which the current release doesn't support.
- The unused `.venv-cuda` folder can be deleted.
