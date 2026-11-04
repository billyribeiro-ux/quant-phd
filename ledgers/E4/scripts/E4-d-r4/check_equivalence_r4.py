"""Equivalence check for the price-slope candidate (round 4). Usage: python -I check_equivalence_r4.py <repo-root>.

Proof sketch checked numerically: for any scalar b in place of b_s (with b_u = kappa b, kappa = -a/(lam tau_e) unchanged),
Var(v - p_b) = Omega_b equals V_I + S_I(b) = V_U + S_U(b), so F_I(b) = (V_I/Omega_b)^(1/2), F_U(b) = (V_U/Omega_b)^(1/2) and
the gap has the sign of tau_bar - tau_y(lam) for every b. Prints the identity residuals, the sign mismatches on a grid,
and the largest output difference over random inputs.
"""

import importlib.util
import math
import random
import sys
from pathlib import Path

root = Path(sys.argv[1])


def load(path: str, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, root / path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


ref = load("course/modules/E/E4/grader/reference.py", "ref")
cand = load("ledgers/E4/scripts/E4-d-r4/equivalent_candidate_price_slope.py", "cand")
A, TV, TE = 2.0, 1.0, 1.0

random.seed(11)
worst_id = 0.0
for _ in range(2000):
    sd = random.uniform(0.05, 3.0)
    lam = random.uniform(0.001, 0.999)
    b = random.uniform(-2.0, 2.0)
    kappa = -A / (lam * TE)
    tau_y = ref.price_precision(lam, sd)
    Q = TV + tau_y
    Vy = 1 / TV + 1 / tau_y
    Omega = (1 - b) ** 2 / TV + b * b / TE + b * b * kappa * kappa * sd * sd
    VI = 1 / (TV + TE)
    SI = (TE / (TV + TE) - b) ** 2 * (1 / TV + 1 / TE) + b * b * kappa * kappa * sd * sd
    rU = tau_y / Q - b
    SU = rU * rU * Vy
    VU = 1 / Q
    worst_id = max(worst_id, abs(VI + SI - Omega), abs(VU + SU - Omega))
print("max |V_I + S_I - Omega|, |V_U + S_U - Omega| over 2000 draws of (lam, sd, b):", f"{worst_id:.2e}")

mism = 0
total = 0
for _ in range(300):
    sd = random.uniform(0.2, 1.5)
    cost = random.uniform(0.0, 0.4)
    for k in range(1, 300):
        lam = k / 300
        total += 1
        if (ref.indifference_gap(lam, sd, cost) > 0) != (cand.indifference_gap(lam, sd, cost) > 0):
            mism += 1
print("sign mismatches of the gap on the interior grid:", mism, "of", total)

worst = 0.0
for _ in range(3000):
    sd = random.uniform(0.05, 3.0)
    cost = random.uniform(0.0, 0.5)
    a = ref.solve_model(sd, cost)
    b = cand.solve_model(sd, cost)
    worst = max(worst, max(abs(a[k] - b[k]) for k in a))
print("largest |difference| in any solver output over 3000 random inputs:", f"{worst:.2e}")
print("finite:", math.isfinite(worst))
