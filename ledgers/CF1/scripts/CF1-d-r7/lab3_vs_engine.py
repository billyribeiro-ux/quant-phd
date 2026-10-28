import importlib.util, statistics
spec = importlib.util.spec_from_file_location("ref", "/tmp/verify6-CF1-d/course/modules/CF/CF1/grader/reference.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
P = {"capex": 900000, "life": 3, "revenue": [600000.0, 650000.0, 700000.0], "cash_costs": [200000.0, 210000.0, 220000.0],
     "tax_rate": 0.25, "nwc_share": 0.10, "inflation": 0.0}
d = ref.npv_monte_carlo(P, 0.10, 2000, 42, 0.2)
dol = [x / 100 for x in d]
m = sum(dol) / len(dol)
sd = statistics.stdev(dol)
print("mean", round(m, 2), "sd", round(sd, 2), "se", round(sd / len(dol) ** 0.5, 2), "neg", sum(1 for x in dol if x < 0), "min", round(min(dol), 2), "max", round(max(dol), 2))
z = ref.npv_monte_carlo(P, 0.10, 10, 42, 0.0)
print("zero vol mean", round(sum(z) / 10 / 100, 2))
print("rung1 npv", round(ref.npv(0.10, ref.after_tax_cash_flows(P)) / 100, 2), "irr check", [round(r, 6) for r in ref.irr_roots(ref.after_tax_cash_flows(P))])
print("payback", round(ref.payback_period(ref.after_tax_cash_flows(P)) , 6), "disc", round(ref.payback_period(ref.after_tax_cash_flows(P), 0.10), 6))
