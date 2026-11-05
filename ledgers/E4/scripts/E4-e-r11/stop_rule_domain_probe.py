"""Round 11: check the two bisection variants that the equivalent/ README calls output-equivalent on the page's domain
(stop test on the lower end, and a stop test that is not the reference's). For random interior instances with noise
volume from 1e-50 to 1e3 and tau-bar at least 1e-2, compare each variant's informed fraction with an oracle root
computed by 400 bisection halvings on the reference gap. Requirement (project.html Constraints): within the smaller of
1e-10 and 1e-8 times the root. Run from the checkout root with -I."""
import importlib.util
import math
import random

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ref = load("course/modules/E/E4/grader/reference.py", "ref")
lower = load("ledgers/E4/equivalent/mutant_v9_02_stop_rule_relative_to_lower_end.py", "lower")
rng = random.Random(11)
cases = worst_lower = worst_oracle_check = 0
worst_lower = 0.0
tested = 0
while tested < 60:
    sd = 10 ** rng.uniform(-50, 3)
    cost = rng.uniform(0.0, 0.4)
    # oracle root by 400 halvings of the reference gap on (0, 1), with the reference's boundary rule
    if ref.gap_at_zero(sd, cost) <= 0.0 or ref.indifference_gap(1.0, sd, cost) >= 0.0:
        continue
    lo, hi = 0.0, 1.0
    for _ in range(400):
        mid = 0.5 * (lo + hi)
        if mid == lo or mid == hi:
            break
        if ref.indifference_gap(mid, sd, cost) > 0.0:
            lo = mid
        else:
            hi = mid
    root = 0.5 * (lo + hi)
    if not (0.0 < root < 1.0):
        continue
    b_s, _, tau_y = ref.price_coefficients(root, sd)
    tau_bar = b_s / (1.0 - b_s)  # tau_v = 1: b_s = tau_bar / (1 + tau_bar)
    if tau_bar < 1e-2 or sd < 1e-50:
        continue
    tested += 1
    allowed = min(1e-10, 1e-8) * root
    got_ref = ref.solve_model(sd, cost)["informed_fraction"]
    got_lower = lower.solve_model(sd, cost)["informed_fraction"]
    worst_lower = max(worst_lower, abs(got_lower - root) / allowed)
    worst_oracle_check = max(worst_oracle_check, abs(got_ref - root) / allowed)
print(f"cases {tested}")
print(f"largest error of the lower-end variant as a fraction of the allowed error: {worst_lower:.4g}")
print(f"largest error of the reference as a fraction of the allowed error: {worst_oracle_check:.4g}")
