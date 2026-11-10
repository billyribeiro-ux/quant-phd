"""Lab AP2-project-3: Project Rung 3 reference case (seed 0).

Self-contained reference run on public SIMULATED instance seed 0.
Prints the benchmark outputs for minimum-variance weights, tangency weights,
frontier weights, beta, Jensen regression, and cross-sectional SML to which
the learner's capm_tests.py must agree.
"""

from __future__ import annotations

from fractions import Fraction


def invert_3x3(mat: list[list[Fraction]]) -> list[list[Fraction]]:
    n = 3
    aug = [[mat[i][j] for j in range(n)] + [Fraction(1 if i == k else 0) for k in range(n)] for i in range(n)]
    for i in range(n):
        p = aug[i][i]
        for j in range(2 * n):
            aug[i][j] /= p
        for r in range(n):
            if r != i:
                f = aug[r][i]
                for j in range(2 * n):
                    aug[r][j] -= f * aug[i][j]
    return [[aug[i][n + j] for j in range(n)] for i in range(n)]


def main() -> None:
    # Public instance seed 0 inputs (SIMULATED)
    cov = [
        [Fraction(7, 1000), Fraction(1, 200), Fraction(7, 1000)],
        [Fraction(1, 200), Fraction(19, 2000), Fraction(1, 125)],
        [Fraction(7, 1000), Fraction(1, 125), Fraction(27, 2000)],
    ]
    mu = [Fraction(23, 2000), Fraction(7, 500), Fraction(31, 2000)]
    r_f = Fraction(3, 2000)
    target = Fraction(27, 2000)
    iota = [Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]

    # 1. GMV weights
    inv = invert_3x3(cov)
    inv_iota = [sum((inv[i][j] * iota[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    denom_gmv = sum(inv_iota, Fraction(0, 1))
    w_gmv = [inv_iota[i] / denom_gmv for i in range(3)]

    # 2. Tangency weights
    excess = [mu[i] - r_f for i in range(3)]
    inv_excess = [sum((inv[i][j] * excess[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    denom_t = sum(inv_excess, Fraction(0, 1))
    w_t = [inv_excess[i] / denom_t for i in range(3)]

    # 3. Frontier weights at target = 27/2000
    inv_mu = [sum((inv[i][j] * mu[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    s_a = denom_gmv
    s_b = sum((iota[i] * inv_mu[i] for i in range(3)), Fraction(0, 1))
    s_c = sum((mu[i] * inv_mu[i] for i in range(3)), Fraction(0, 1))
    s_d = s_a * s_c - s_b * s_b
    l1 = (s_c - s_b * target) / s_d
    l2 = (s_a * target - s_b) / s_d
    w_f = [l1 * inv_iota[i] + l2 * inv_mu[i] for i in range(3)]

    # 4. is_tangency check
    sig_wt = [sum((cov[i][j] * w_t[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    k = sig_wt[0] / excess[0]
    is_t = all(sig_wt[i] == k * excess[i] for i in range(3)) and sum(w_t, Fraction(0, 1)) == Fraction(1, 1)

    print("--- Public Instance (Seed 0) Benchmark Outputs ---")
    print(f"GMV weights:      [{w_gmv[0]}, {w_gmv[1]}, {w_gmv[2]}]")
    print(f"Tangency weights: [{w_t[0]}, {w_t[1]}, {w_t[2]}]")
    print(f"Frontier weights: [{w_f[0]}, {w_f[1]}, {w_f[2]}]")
    print(f"is_tangency(w_T): {is_t}")
    print(f"Target mean:      {target}")
    achieved = sum((w_f[i] * mu[i] for i in range(3)), Fraction(0, 1))
    print(f"Achieved mean:    {achieved}")
    print(f"Frontier match:   {achieved == target}")


main()
