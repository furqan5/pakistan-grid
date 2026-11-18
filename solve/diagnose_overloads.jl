# Day 9 diagnostics (not the scored case): in DC-OPF with ratings removed (winter) or all families relaxed (summer),
# list branches whose flow exceeds their rate_a, and generators whose pmin was relaxed below.
using PowerModels, Ipopt
PowerModels.silence()
casedir = ARGS[1]
opt = optimizer_with_attributes(Ipopt.Optimizer, "print_level" => 0, "tol" => 1e-6, "max_iter" => 3000)
for (snap, fams) in (("winter_offpeak", ("no_ratings",)), ("summer_peak", ("no_ratings", "angles_90")), ("summer_peak", ("no_ratings", "angles_90", "pmin_0")))
    data = PowerModels.parse_file(joinpath(casedir, "pk_$(snap).json"))
    d = deepcopy(data)
    for (_, b) in d["branch"]
        "no_ratings" in fams && (b["rate_a"] = 1e3)
        "angles_90" in fams && (b["angmin"] = -pi/2 + 1e-3; b["angmax"] = pi/2 - 1e-3)
    end
    "pmin_0" in fams && foreach(g -> g["pmin"] = 0.0, values(d["gen"]))
    r = solve_dc_opf(d, opt)
    println("== $snap relaxed $(fams): $(r["termination_status"])")
    r["termination_status"] in (PowerModels.LOCALLY_SOLVED, PowerModels.OPTIMAL) || continue
    over = []
    for (k, f) in r["solution"]["branch"]
        b = data["branch"][k]
        ra = b["rate_a"]; p = abs(f["pf"])
        if p > ra * 1.001
            push!(over, (p / ra, p * 100, ra * 100, b["transformer"], data["bus"][string(b["f_bus"])]["name"], data["bus"][string(b["t_bus"])]["name"]))
        end
    end
    sort!(over, by = x -> -x[1])
    println("   $(length(over)) branches over rate_a; worst 15:")
    for o in over[1:min(15, end)]
        println("   $(round(o[1]; digits=2))x  flow $(round(o[2]; digits=0)) MW / rate $(round(o[3]; digits=0)) MVA  $(o[4] ? "TRAFO" : "line ")  $(first(o[5], 34)) -> $(first(o[6], 34))")
    end
end
