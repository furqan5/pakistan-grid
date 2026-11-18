# Day 9 diagnostics (not the scored case): which constraint family makes DC-OPF infeasible?
# Each variant relaxes one family on a COPY of the case and reports only feasibility.
using PowerModels, Ipopt
PowerModels.silence()
casedir = ARGS[1]
opt = optimizer_with_attributes(Ipopt.Optimizer, "print_level" => 0, "tol" => 1e-6, "max_iter" => 3000)
function variant!(d, which)
    if which in ("no_ratings", "all")
        for (_, b) in d["branch"]; b["rate_a"] = 1e3; b["rate_b"] = 1e3; b["rate_c"] = 1e3; end
    end
    if which in ("angles_90", "all")
        for (_, b) in d["branch"]; b["angmin"] = -pi/2 + 1e-3; b["angmax"] = pi/2 - 1e-3; end
    end
    if which in ("pmin_0", "all")
        for (_, g) in d["gen"]; g["pmin"] = 0.0; end
    end
    if which in ("dcline_free", "all")
        for (_, l) in d["dcline"]; l["pminf"] = 0.0; l["pmaxf"] = 40.0; l["pmint"] = -40.0; l["pmaxt"] = 0.0; end
    end
    if which == "no_dcline"
        d["dcline"] = Dict{String,Any}()
    end
end
for snap in ("winter_offpeak", "summer_peak")
    data = PowerModels.parse_file(joinpath(casedir, "pk_$(snap).json"))
    for which in ("base", "no_ratings", "angles_90", "pmin_0", "dcline_free", "no_dcline", "all")
        d = deepcopy(data); variant!(d, which)
        r = solve_dc_opf(d, opt)
        println("$(rpad(snap, 16)) $(rpad(which, 12)) $(r["termination_status"])")
    end
end
