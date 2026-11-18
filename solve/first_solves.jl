# Day 9: first solves of the Pakistan cases (DC-OPF, AC power flow from flat start, AC-OPF), in the order declared in
# builder/parameters.json["assembly"]["solve_order"]. Prints ONLY solver status, iteration time and objective.
# It deliberately does not print or summarise generator Q, losses or voltages: holdouts H1-H8 are computed once, on
# Day 11, by a separate script. Full solutions are saved to <case dir>/solutions/ for that step.
# Usage: julia --project=<GridSFM topology_solver_pipeline> solve/first_solves.jl <case dir>
using PowerModels, Ipopt, JSON
PowerModels.silence()

casedir = ARGS[1]
outdir = joinpath(casedir, "solutions")
mkpath(outdir)
ipopt(tol) = optimizer_with_attributes(Ipopt.Optimizer, "print_level" => 0, "tol" => tol, "max_iter" => 3000, "max_cpu_time" => 900.0)

for snap in ("summer_peak", "winter_offpeak")
    path = joinpath(casedir, "pk_$(snap).json")
    data = PowerModels.parse_file(path)
    println("== $snap: $(length(data["bus"])) buses, $(length(data["branch"])) branches, $(length(data["gen"])) gens, $(length(data["dcline"])) dcline")
    for (label, f, tol) in (("DC-OPF", d -> solve_dc_opf(d, ipopt(1e-6)), 1e-6),
                            ("AC-PF (flat start)", d -> solve_ac_pf(d, ipopt(1e-6)), 1e-6),
                            ("AC-OPF", d -> solve_ac_opf(d, ipopt(1e-4)), 1e-4))
        d = deepcopy(data)
        t = @elapsed res = f(d)
        obj = haskey(res, "objective") && res["objective"] !== nothing ? round(res["objective"]; digits=1) : "n/a"
        println("   $(rpad(label, 20)) $(rpad(string(res["termination_status"]), 22)) primal=$(res["primal_status"])  time=$(round(t; digits=1)) s  objective=$(obj)")
        open(joinpath(outdir, "$(snap)_$(replace(lowercase(label), r"[^a-z0-9]+" => "_")).json"), "w") do io
            JSON.print(io, Dict("termination_status" => string(res["termination_status"]), "primal_status" => string(res["primal_status"]),
                                "objective" => get(res, "objective", nothing), "solve_time" => t, "solution" => get(res, "solution", Dict())))
        end
    end
end
