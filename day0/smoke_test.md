# Day 0/1 — Windows stack reproduces Microsoft's Delaware result

Run on 6 Nov 2026 on Furqan's Windows 11 laptop, natively (no WSL or Docker). The full console log is in `logs/smoke_delaware.log`.

## Stack

| Item | Version / location |
|---|---|
| Julia | 1.11.5 win64, the official zip from julialang-s3. SHA-256 `580ecaf4…4c595b` matches julialang's published checksum. Installed at `C:\Users\furqa\tools\julia-1.11.5` |
| GridSFM | `microsoft/GridSFM` shallow clone at commit `1ca775fd436d7ce013a1c0ab946e61ac7ef59ad6`, in `C:\Users\furqa\src\GridSFM` |
| Packages | Installed from the repo's `topology_solver_pipeline/Manifest.toml`: PowerModels 0.21.5, JuMP 1.29.4, Ipopt.jl 1.14.0, JSON 0.21.4, JSON3 1.14.3, Distributions 0.25.123 |
| Depot | Default `C:\Users\furqa\.julia` |

Pkg warned that "project dependencies or compat requirements have changed since the manifest was last resolved". The Manifest versions were used as-is, without a resolve or update, so the stack stays pinned to what Microsoft shipped.

## Commands (called directly; Make, `taskset` and Docker aren't on this laptop)

```bash
cd C:/Users/furqa/src/GridSFM/power_grid/US/topology_solver_pipeline
julia --project=. docker/patch_model.jl  <data>/16h/delaware_model.json  <out>/delaware_model_patched.json
julia --project=. solve_topo_json.jl     <out>/delaware_model_patched.json <out>/delaware_model.solvable.json
julia --project=. export_gridsfm_data.jl <out>/delaware_model.solvable.json <out>/delaware_base.pyg.json
```

The data is `microsoft/GridSFM_US_power_grid`, files `16h/delaware_model.json` (55,137 bytes) and `16h/delaware_ac_results.json` (11,941 bytes), downloaded from Hugging Face on 6 Nov 2026.
Outputs are in `C:\Users\furqa\src\gridsfm-runs\output\delaware_16h\`.

## Result against Microsoft's published AC result

| | This run | Microsoft (`delaware_ac_results.json`) |
|---|---|---|
| Patch stage | "no patching needed" | — |
| Ladder rung | L0 (Strict), no relaxations | L0 (Strict) |
| Termination | LOCALLY_SOLVED | LOCALLY_SOLVED |
| Objective | 27,531.664499504 | 27,531.664492124 |
| Relative difference | **2.7 × 10⁻¹⁰** | — |
| Total generation / load | 1,510.3 / 1,506.2 MW | 1,510.3 / 1,506.2 MW |
| Ipopt solve time | 15.97 s (ladder), 15.33 s (export) | 17.0 s |
| Size | 33 buses, 77 branches, 9 generators | same |

**Conclusion:** the native Windows stack reproduces Microsoft's Delaware AC-OPF result to solver tolerance. The `.pyg.json` export also works (`feas=true`).
Wall-clock time per stage is 50–70 s, mostly Julia start-up and compilation. Ipopt itself takes about 16 s on a 33-bus case.

## Not yet done (Day 1 remainder)

- The hand-written 10-bus Pakistan JSON: a 500 kV Tarbela–Jamshoro chain plus the HVDC `dcline`.
- The list of fields `solve_topo_json.jl` actually requires.
- Note: Delaware is far below GridSFM's 500-bus floor. This run tests only the solver pipeline, not GridSFM inference, which needs the Python `model/` package and the checkpoint.
