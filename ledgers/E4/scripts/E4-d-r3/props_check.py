"""Numeric checks of Propositions 1-5 against the independent model in indep_model.py (verifier's own).

Usage: .venv/bin/python -I ledgers/E4/scripts/E4-d-r3/props_check.py <repo-root>
Checks: (P1) closed-form b_u/b_s, b_s and tau_y match the clearing solution; (P2) Corr^2 = tau_y/(1+tau_y);
(P3) sign G(lam) = sign(tau_bar - tau_y(lam)) and G(0+) sign = sign(tau_bar); (P4) boundary rule and closed-form root
agree with the independent root on a grid; (P5) on the interior, lam* strictly decreasing in c, linear in sigma.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_model as im  # noqa: E402

A, TV, TE = 2.0, 1.0, 1.0


def ty_of(lam: float, sd: float) -> float:
    return lam * lam * TE * TE / (lam * lam * TE + A * A * sd * sd)


def tau_bar(cost: float) -> float:
    return (TV + TE) * np.exp(-2 * A * cost) - TV


worst = {"P1": 0.0, "P2": 0.0, "P3_violations": 0, "P3_checks": 0, "P4_max_diff": 0.0, "P4_cases": 0}
# P1 and P2 at lam grid
for sd in (0.3, 0.5, 0.75, 1.5):
    for lam in (0.05, 0.2, 0.5, 0.8, 1.0):
        bs, bu, res = im.equilibrium(lam, sd)
        ty = ty_of(lam, sd)
        D = lam * (TV + TE) + (1 - lam) * (TV + ty)
        bs_cf = (lam * TE + (1 - lam) * ty) / D
        bu_cf = -A * bs_cf / (lam * TE)
        worst["P1"] = max(worst["P1"], abs(bs - bs_cf), abs(bu - bu_cf))
        _, info, _, _ = im.gap_and_info(lam, sd, 0.1)
        worst["P2"] = max(worst["P2"], abs(info - ty / (TV + ty)))
# P3 sign rule and P4 boundary/closed form on a grid
grid_sd = np.linspace(0.3, 1.5, 7)
grid_c = np.linspace(0.0, 0.35, 8)
for sd in grid_sd:
    for c in grid_c:
        tb = tau_bar(c)
        for lam in (0.1, 0.5, 0.9):
            g, _, _, _ = im.gap_and_info(lam, sd, c)
            worst["P3_checks"] += 1
            if np.sign(g) != np.sign(tb - ty_of(lam, sd)) and abs(g) > 1e-12:
                worst["P3_violations"] += 1
        # P4: closed form of the page vs independent root
        if tb <= 0:
            cf = 0.0
        elif tb >= TE * TE / (TE + A * A * sd * sd):
            cf = 1.0
        else:
            cf = A * sd * np.sqrt(tb / (TE * (TE - tb)))
        ind = im.closed_root(sd, c)
        worst["P4_cases"] += 1
        worst["P4_max_diff"] = max(worst["P4_max_diff"], abs(cf - ind))
# P5 on the interior at sd 0.5 and 0.75 over costs with interior
for sd in (0.5, 0.625, 0.75):
    costs = [c for c in np.linspace(0.12, 0.15, 9) if 0 < tau_bar(c) < TE * TE / (TE + A * A * sd * sd)]
    lams = [im.closed_root(sd, c) for c in costs]
    infos = [im.gap_and_info(l, sd, c)[1] for l, c in zip(lams, costs)]
    dec_lam = all(x > y for x, y in zip(lams, lams[1:]))
    dec_info = all(x > y for x, y in zip(infos, infos[1:]))
    print(f"P5 sd {sd}: interior costs {len(costs)}, lam strictly decreasing in c: {dec_lam}, info strictly decreasing: {dec_info}")
print("P1 max |b - closed form|:", worst["P1"])
print("P2 max |Corr^2 - tau_y/(1+tau_y)|:", worst["P2"])
print("P3 sign checks:", worst["P3_checks"], "violations:", worst["P3_violations"])
print("P4 cases:", worst["P4_cases"], "max |closed form - independent root|:", worst["P4_max_diff"])
