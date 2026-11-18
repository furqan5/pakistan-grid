# Day 9 diagnostics (not the scored case): AC-OPF on copies with progressively removed constraint families,
# starting from an L5-like relaxation. Reports feasibility only.
using PowerModels, Ipopt
PowerModels.silence()
casedir = ARGS[1]
opt = optimizer_with_attributes(Ipopt.Optimizer, "print_level" => 0, "tol" => 1e-4, "max_iter" => 3000, "max_cpu_time" => 600.0)
function l5!(d)
    for (_, b) in d["branch"]; b["rate_a"] = 1e3; b["rate_b"] = 1e3; b["rate_c"] = 1e3; b["angmin"] = -pi/2 + 1e-3; b["angmax"] = pi/2 - 1e-3; end
    for (_, bus) in d["bus"]; bus["vmin"] = 0.85; bus["vmax"] = 1.15; end
    for (_, g) in d["gen"]; g["pmin"] = 0.0; g["qmax"] *= 2; g["qmin"] *= 2; end
    for (_, l) in d["load"]; l["pd"] *= 0.7; l["qd"] *= 0.7; end
end
for snap in ("winter_offpeak", "summer_peak")
    data = PowerModels.parse_file(joinpath(casedir, "pk_$(snap).json"))
    steps = [("L5-like", d -> nothing),
             ("+ gen Q unlimited", d -> foreach(g -> (g["qmax"] = 50.0; g["qmin"] = -50.0), values(d["gen"]))),
             ("+ V 0.7-1.3", d -> foreach(b -> (b["vmin"] = 0.7; b["vmax"] = 1.3), values(d["bus"]))),
             ("+ dcline removed", d -> (d["dcline"] = Dict{String,Any}())),
             ("+ shunts removed", d -> (d["shunt"] = Dict{String,Any}())),
             ("+ load Q = 0", d -> foreach(l -> l["qd"] = 0.0, values(d["load"])))]
    d = deepcopy(data); l5!(d)
    for (label, f) in steps
        f(d)
        r = solve_ac_opf(deepcopy(d), opt)
        println("$(rpad(snap, 15)) $(rpad(label, 20)) $(r["termination_status"])")
    end
end
