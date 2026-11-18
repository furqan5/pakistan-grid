# Day 9 diagnostics (not the scored case): smallest rating multiplier k that makes DC-OPF feasible,
# under L2-like settings (angles +/-60 deg) and L3-like settings (angles +/-90 deg, pmin x0.5).
using PowerModels, Ipopt
PowerModels.silence()
casedir = ARGS[1]
opt = optimizer_with_attributes(Ipopt.Optimizer, "print_level" => 0, "tol" => 1e-6, "max_iter" => 3000)
function feas(data, k, ang, pminf)
    d = deepcopy(data)
    for (_, b) in d["branch"]
        b["rate_a"] *= k; b["rate_b"] *= k; b["rate_c"] *= k
        if !b["transformer"]; b["angmin"] = -deg2rad(ang); b["angmax"] = deg2rad(ang); end
    end
    for (_, g) in d["gen"]; g["pmin"] *= pminf; end
    r = solve_dc_opf(d, opt)
    return r["termination_status"] in (PowerModels.LOCALLY_SOLVED, PowerModels.OPTIMAL)
end
for snap in ("summer_peak", "winter_offpeak")
    data = PowerModels.parse_file(joinpath(casedir, "pk_$(snap).json"))
    for (label, ang, pminf) in (("L2-like (60 deg)", 60.0, 1.0), ("L3-like (90 deg, pmin x0.5)", 89.9, 0.5))
        lo, hi = 1.0, 16.0
        if !feas(data, hi, ang, pminf); println("$snap $label: infeasible even at k=16"); continue; end
        if feas(data, lo, ang, pminf); println("$snap $label: feasible at k=1"); continue; end
        for _ in 1:9
            mid = (lo + hi) / 2
            feas(data, mid, ang, pminf) ? (hi = mid) : (lo = mid)
        end
        println("$(rpad(snap, 15)) $(rpad(label, 28)) k_min ~ $(round(hi; digits=2))")
    end
end
