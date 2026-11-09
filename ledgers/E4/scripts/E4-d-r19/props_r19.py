"""Round 19 (E4-d): Propositions 1 to 5 checked against the suite's quadrature/fixed-point oracle, and the Constraints
accuracy claim swept over the page's domain. Run with SOLVER_DIR set to a workspace holding solver.py (= reference),
test_project.py and instance.py: SOLVER_DIR=... python -I props_r19.py
"""

import math
import os
import random
import sys

SOLVER_DIR = os.environ["SOLVER_DIR"]
sys.path.insert(0, SOLVER_DIR)
import solver as ref  # noqa: E402
import test_project as tp  # noqa: E402

rng = random.Random(19)
A = 2.0

# Proposition 1: the oracle's fixed point on the market-clearing condition gives (b_s, b_u); compare with the formulas.
worst_b = 0.0
worst_ty = 0.0
worst_pi = 0.0
worst_gap = 0.0
n = 0
for _ in range(300):
    lam = rng.uniform(0.02, 0.98)
    sd = rng.uniform(0.5, 2.0)  # the oracle's fixed point is only checked where the suite uses it (sd 0.5 to 2)
    bs_f, bu_f, ty_f = ref.price_coefficients(lam, sd)
    bs_o, bu_o = tp.oracle_price(lam, sd)
    worst_b = max(worst_b, abs(bs_f - bs_o) / abs(bs_o), abs(bu_f - bu_o) / abs(bu_o))
    # Proposition 2: informativeness from the oracle's population moments equals tau_y/(tau_v+tau_y)
    pi_o = tp.oracle_informativeness(lam, sd)
    pi_f = ref.price_informativeness(lam, sd)
    worst_pi = max(worst_pi, abs(pi_f - pi_o))
    # Proposition 3: the reference gap equals the oracle's expected-utility gap
    cost = rng.uniform(0.0, 0.3)
    worst_gap = max(worst_gap, abs(ref.indifference_gap(lam, sd, cost) - tp.oracle_gap(lam, sd, cost)))
    n += 1
print("oracle domain: sd in [0.5, 2.0]; below about sd 0.1 the oracle fixed point returns b_s near 0 and is not used by the suite")
print(f"Prop1 max rel diff (b_s, b_u) vs oracle fixed point over {n} points: {worst_b:.3e}")
print(f"Prop2 max abs diff informativeness vs oracle moments: {worst_pi:.3e}")
print(f"Prop3 max abs diff gap vs oracle quadrature: {worst_gap:.3e}")

# Proposition 1 coefficient identity: b_u/b_s = -a/(lam tau_e) and tau_y = lam^2 tau_e^2/(lam^2 tau_e + a^2 sd^2)
worst_ratio = 0.0
for _ in range(300):
    lam = rng.uniform(0.01, 1.0)
    sd = 10 ** rng.uniform(-2, 1)
    bs, bu, ty = ref.price_coefficients(lam, sd)
    worst_ratio = max(worst_ratio, abs(bu / bs + A / (lam * 1.0)) / (A / lam))
print(f"Prop1 max relative error of b_u/b_s + a/lam: {worst_ratio:.3e}")

# Proposition 4: the reference's root (interior) equals the closed form; boundary cases.
worst_p4 = 0.0
cases = 0
for _ in range(400):
    sd = 10 ** rng.uniform(-2, 0.5)
    cost = rng.uniform(0.0, 0.3)
    out = ref.solve_model(sd, cost)
    cf = tp.closed_form_root(sd, cost)
    t = 2 * math.exp(-4 * cost) - 1
    if 0.0 < t < 1.0 / (1.0 + 4 * sd * sd):
        cases += 1
        worst_p4 = max(worst_p4, abs(out["informed_fraction"] - cf) / cf)
print(f"Prop4 interior cases {cases}: max relative |bisection - closed form| = {worst_p4:.3e}")

# Proposition 5: d lambda*/d sigma = lambda*/sigma (finite difference), lambda* decreasing in c, informativeness
# independent of sigma on the interior.
worst_d = 0.0
worst_mono = 0.0
worst_info = 0.0
for _ in range(200):
    cost = rng.uniform(0.05, 0.16)
    sd = rng.uniform(0.3, 0.9)
    t = 2 * math.exp(-4 * cost) - 1
    if not (0.0 < t < 1.0 / (1.0 + 4 * sd * sd)):
        continue
    h = 1e-6 * sd
    l0 = tp.closed_form_root(sd, cost)
    dl = (tp.closed_form_root(sd + h, cost) - tp.closed_form_root(sd - h, cost)) / (2 * h)
    worst_d = max(worst_d, abs(dl - l0 / sd) / (l0 / sd))
    c2 = cost + 0.001
    if 0.0 < 2 * math.exp(-4 * c2) - 1 < 1.0 / (1.0 + 4 * sd * sd):
        worst_mono = max(worst_mono, tp.closed_form_root(sd, c2) - l0)
    i1 = ref.solve_model(sd, cost)["price_informativeness"]
    i2 = ref.solve_model(sd * 1.1, cost)["price_informativeness"] if (2 * math.exp(-4 * cost) - 1) < 1.0 / (1.0 + 4 * (1.1 * sd) ** 2) else i1
    worst_info = max(worst_info, abs(i1 - i2))
print(f"Prop5 max relative |dlambda/dsigma - lambda/sigma|: {worst_d:.3e}")
print(f"Prop5 max (lambda(c+0.001) - lambda(c)) on interior (must be <= 0): {worst_mono:.3e}")
print(f"Prop5 max |informativeness(sigma) - informativeness(1.1 sigma)| on interior: {worst_info:.3e}")

# Constraints: relative accuracy 1e-10 of the reported root for sd >= 1e-50 and tau_bar >= 1e-2 (interior).
worst_acc = 0.0
worst_at = None
cnt = 0
for i in range(120):
    sd = 10 ** (-50 + 52 * i / 119)
    for j in range(120):
        cost = 0.0 + (math.log(2 / 1.01) / 4 + 0.0005) * 0 + j * (math.log(2 / 1.01) / 4) / 119
        t = 2 * math.exp(-4 * cost) - 1
        if t < 1e-2 or t >= 1.0 / (1.0 + 4 * sd * sd):
            continue
        cnt += 1
        out = ref.solve_model(sd, cost)["informed_fraction"]
        cf = tp.closed_form_root(sd, cost)
        rel = abs(out - cf) / cf
        if rel > worst_acc:
            worst_acc, worst_at = rel, (sd, cost)
print(f"Constraints accuracy sweep: {cnt} interior points with sd in [1e-50, 1e2] and tau_bar >= 1e-2; "
      f"max relative error {worst_acc:.3e} at {worst_at}")
