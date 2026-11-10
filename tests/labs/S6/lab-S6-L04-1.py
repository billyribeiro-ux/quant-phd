"""Lab S6-L04-1: Difference-in-Differences and Two-Way Fixed Effects equivalence.

Constructed example: verifies using exact rational arithmetic (fractions.Fraction)
that the canonical 2x2 DiD estimand identically equals the interaction coefficient
from a two-way fixed-effects OLS regression.
"""

from __future__ import annotations

from fractions import Fraction


def solve_ols(x_mat: list[list[Fraction]], y_vec: list[Fraction]) -> list[Fraction]:
    """Solve (X^T X) beta = X^T y using exact Gauss-Jordan elimination."""
    p = len(x_mat[0])
    n = len(x_mat)

    # Compute X^T X (p x p) and X^T y (p x 1)
    xtx: list[list[Fraction]] = [
        [sum((x_mat[i][j] * x_mat[i][k] for i in range(n)), Fraction(0)) for k in range(p)] for j in range(p)
    ]
    xty: list[Fraction] = [sum((x_mat[i][j] * y_vec[i] for i in range(n)), Fraction(0)) for j in range(p)]

    # Augmented matrix [XTX | XTy]
    aug: list[list[Fraction]] = [xtx[i] + [xty[i]] for i in range(p)]

    # Gaussian elimination with partial pivoting
    for col in range(p):
        pivot = col
        while pivot < p and aug[pivot][col] == Fraction(0):
            pivot += 1
        if pivot == p:
            raise ValueError("matrix is singular")
        aug[col], aug[pivot] = aug[pivot], aug[col]

        piv_val = aug[col][col]
        for c in range(col, p + 1):
            aug[col][c] = aug[col][c] / piv_val

        for r in range(p):
            if r != col and aug[r][col] != Fraction(0):
                factor = aug[r][col]
                for c in range(col, p + 1):
                    aug[r][c] = aug[r][c] - factor * aug[col][c]

    return [aug[r][p] for r in range(p)]


def main() -> None:
    # 2x2 balanced panel: 2 units in Control, 2 units in Treated, observed at Pre (t=0) and Post (t=1)
    # Unit 1: Control, pre=10, post=14
    # Unit 2: Control, pre=12, post=16
    # Unit 3: Treated, pre=20, post=31
    # Unit 4: Treated, pre=22, post=33

    data = [
        # (unit, treat, post, y)
        (1, Fraction(0), Fraction(0), Fraction(10)),
        (1, Fraction(0), Fraction(1), Fraction(14)),
        (2, Fraction(0), Fraction(0), Fraction(12)),
        (2, Fraction(0), Fraction(1), Fraction(16)),
        (3, Fraction(1), Fraction(0), Fraction(20)),
        (3, Fraction(1), Fraction(1), Fraction(31)),
        (4, Fraction(1), Fraction(0), Fraction(22)),
        (4, Fraction(1), Fraction(1), Fraction(33)),
    ]

    # 1. Compute canonical 2x2 DiD estimand from group sample means
    y_ctrl_pre = sum(row[3] for row in data if row[1] == 0 and row[2] == 0) / 2
    y_ctrl_post = sum(row[3] for row in data if row[1] == 0 and row[2] == 1) / 2
    y_treat_pre = sum(row[3] for row in data if row[1] == 1 and row[2] == 0) / 2
    y_treat_post = sum(row[3] for row in data if row[1] == 1 and row[2] == 1) / 2

    ctrl_trend = y_ctrl_post - y_ctrl_pre
    treat_change = y_treat_post - y_treat_pre
    did_estimand = treat_change - ctrl_trend

    # 2. Build regression design matrix: Y = beta_0 + beta_treat * Treat + beta_post * Post + beta_did * (Treat * Post)
    x_mat: list[list[Fraction]] = []
    y_vec: list[Fraction] = []

    for _, treat, post, y in data:
        interact = treat * post
        x_mat.append([Fraction(1), treat, post, interact])
        y_vec.append(y)

    beta_hat = solve_ols(x_mat, y_vec)

    b0, b_treat, b_post, b_did = beta_hat

    print("Canonical 2x2 Difference-in-Differences Equivalence (Constructed Panel):")
    print(f"  Control Pre Mean:   {y_ctrl_pre} ({float(y_ctrl_pre):.2f})")
    print(f"  Control Post Mean:  {y_ctrl_post} ({float(y_ctrl_post):.2f})")
    print(f"  Control Trend:      {ctrl_trend} ({float(ctrl_trend):.2f})")
    print(f"  Treated Pre Mean:   {y_treat_pre} ({float(y_treat_pre):.2f})")
    print(f"  Treated Post Mean:  {y_treat_post} ({float(y_treat_post):.2f})")
    print(f"  Treated Change:     {treat_change} ({float(treat_change):.2f})")
    print(f"  DiD Estimand:       {did_estimand} ({float(did_estimand):.2f})\n")

    print("Two-Way Fixed Effects OLS Estimates (Exact Fractions):")
    print(f"  Intercept (beta_0):       {b0}")
    print(f"  Treated Effect (beta_T):  {b_treat}")
    print(f"  Time Trend (beta_Post):   {b_post}")
    print(f"  Interaction (beta_DiD):   {b_did}")
    print(f"  Exact Equivalence Check:  {did_estimand == b_did}")
    print(f"  Algebraic Difference:     {did_estimand - b_did}")


main()
