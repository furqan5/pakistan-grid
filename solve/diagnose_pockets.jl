# Day 9 diagnostics (not the scored case): at the minimal feasible rating multiplier, which branches are loaded
# above their original rating (the pockets that set k_min)?
using PowerModels, Ipopt
PowerModels.silence()
casedir = ARGS[1]
opt = optimizer_with_attributes(Ipopt.Optimizer, "print_level" => 0, "tol" => 1e-6, "max_iter" => 3000)
for (snap, k, thr) in (("summer_peak", 6.0, 2.5), ("winter_offpeak", 1.65, 1.15))
    data = PowerModels.parse_file(joinpath(casedir, "pk_$(snap).json"))
    d = deepcopy(data)
    for (_, b) in d["branch"]; b["rate_a"] *= k; if !b["transformer"]; b["angmin"] = -deg2rad(60); b["angmax"] = deg2rad(60); end; end
    r = solve_dc_opf(d, opt)
    println("== $snap at k=$k: $(r["termination_status"])")
    rows = []
    for (key, f) in r["solution"]["branch"]
        b = data["branch"][key]; ratio = abs(f["pf"]) / b["rate_a"]
        ratio > thr && push!(rows, (ratio, abs(f["pf"]) * 100, b["rate_a"] * 100, b["transformer"], get(b, "length_km", 0.0),
                                    data["bus"][string(b["f_bus"])]["name"], data["bus"][string(b["t_bus"])]["name"], data["bus"][string(b["f_bus"])]["base_kv"]))
    end
    sort!(rows, by = x -> -x[1])
    println("   $(length(rows)) branches above $(thr)x original rating")
    for o in rows[1:min(25, end)]
        println("   $(round(o[1]; digits=2))x $(round(Int, o[2])) MW/$(round(Int, o[3])) $(o[4] ? "TR" : "L ") $(round(Int, o[8]))kV $(round(o[5]; digits=1))km  $(first(o[6], 30)) -> $(first(o[7], 30))")
    end
end
