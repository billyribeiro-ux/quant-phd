"""Brute-force equilibrium and best-response checks (float, finer than the exact algebra; supplements Props 2-3).

Cournot: the closed-form reaction max(0, (d - q_j)/2) is compared with a fine grid maximiser of the profit.
Bertrand: each coarse fee profile (step 1/4) is tested for a profitable deviation on a fine grid (step 1/200).
"""

import itertools

CASES = [(9, 1, 1), (12, 2, 3), (20, 2, 6), (31, 1, 10), (120, 1, 20), (11, 1, 5), (121, 1, 20)]
worst_br = 0.0
for a, b, c in CASES:
    d = a - b * c
    # Cournot reaction check on a grid
    for qj10 in range(0, 2 * d + 1, 3):
        qj = qj10 / 10
        grid = [i / 20 for i in range(0, 20 * a + 1)]
        prof = lambda qi: ((a - qi - qj) / b - c) * qi
        best = max(grid, key=prof)
        formula = max(0.0, (d - qj) / 2)
        worst_br = max(worst_br, abs(best - formula))
    # Bertrand: coarse profiles, fine deviations (only for small cases, for run time)
    if a > 31:
        continue
    coarse = [c + i / 4 for i in range(0, int((a / b - c) * 4) + 1)]
    fine = [c + i / 200 for i in range(0, int((a / b - c) * 200) + 1)]
    fine = [f for f in fine if f <= a / b]

    def pr(fi, fj):
        if fi < fj:
            return (fi - c) * (a - b * fi)
        if fi == fj:
            return (fi - c) * (a - b * fi) / 2
        return 0.0

    eqs = []
    for f1, f2 in itertools.product(coarse, repeat=2):
        p1, p2 = pr(f1, f2), pr(f2, f1)
        if max(pr(g, f2) for g in fine) <= p1 + 1e-12 and max(pr(g, f1) for g in fine) <= p2 + 1e-12:
            eqs.append((f1, f2))
    print(f"case a={a} b={b} c={c}: Bertrand coarse-profile equilibria {eqs}")
print("max |grid best response - closed form reaction| =", round(worst_br, 6))
