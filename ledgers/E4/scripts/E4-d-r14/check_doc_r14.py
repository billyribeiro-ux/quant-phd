import math, sys, importlib, os
sys.path.insert(0, os.getcwd())
os.environ["QF_SEED"] = "0"
t = importlib.import_module("test_project")
sol = importlib.import_module("solver")
cases = [(0.5, 0.30), (0.6, 0.30), (0.75, 0.30), (0.5, 0.50), (0.6, 0.50), (0.75, 0.50)]
for sd, cost in cases:
    limit = t.oracle_gap(0.0, sd, cost)
    g1e12 = t.oracle_gap(1e-12, sd, cost)
    ref_limit = sol.gap_at_zero(sd, cost)
    print(f"sd={sd} cost={cost} |gap(1e-12)-limit|={abs(g1e12-limit):.3e} |oracle-limit|={abs(limit-ref_limit):.3e} |ref_gap0-oracle|={abs(sol.solve_model(sd,cost)['indifference_gap']-limit):.3e}")
for sd, c in [(2.0, 0.0), (0.6, 0.05)]:
    cl = sol.solve_model(sd, c)
    print("fraction1", sd, c, "ref gap", cl["indifference_gap"], "oracle gap", t.oracle_gap(1.0, sd, c), "diff", abs(cl["indifference_gap"]-t.oracle_gap(1.0, sd, c)))
    print("  ref info", cl["price_informativeness"], "oracle info", t.oracle_informativeness(1.0, sd), "diff", abs(cl["price_informativeness"]-t.oracle_informativeness(1.0, sd)))
