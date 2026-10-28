import importlib.util, math, sys
spec = importlib.util.spec_from_file_location("ref", "/tmp/verify15-CF1-d/course/modules/CF/CF1/grader/reference.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
proj = {"capex": 900000, "life": 3, "revenue": [600000, 650000, 700000], "cash_costs": [200000, 210000, 220000], "tax_rate": 0.25, "nwc_share": 0.10, "inflation": 0.0}
d = ref.npv_monte_carlo(proj, 0.10, 2000, 42, 0.2)
n = len(d); m = sum(d)/n; sd = math.sqrt(sum((x-m)**2 for x in d)/(n-1))
print(f"mean {m/100:.2f} sd {sd/100:.2f} se {sd/math.sqrt(n)/100:.2f} neg {sum(1 for x in d if x<0)} lo {min(d)/100:.2f} hi {max(d)/100:.2f}")
z = ref.npv_monte_carlo(proj, 0.10, 10, 42, 0.0); print(f"zero vol mean {sum(z)/10/100:.2f}")
print("irr two-root", ref.irr_roots([-10000.0, 23000.0, -13200.0]))
print("irr rung1", ref.irr_roots([-900000.0, 315000.0, 400000.0, 500000.0]))
print("payback", ref.payback_period([-900000.0, 315000.0, 400000.0, 500000.0]), ref.payback_period([-900000.0, 315000.0, 400000.0, 500000.0], 0.10))
