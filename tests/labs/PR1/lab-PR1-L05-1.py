"""Lab 5: Black-Litterman model: precision form vs generalized least squares form.

Illustrative inputs in exact Fraction arithmetic.
Computes the Black-Litterman posterior expected return vector using both the
precision representation and the Theil / Woodbury generalized least squares
representation, verifying algebraic equivalence to machine precision.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    # 2 assets, 1 relative view
    s_cov = [
        [Fraction(4, 100), Fraction(1, 100)],
        [Fraction(1, 100), Fraction(9, 100)],
    ]
    w_mkt = [Fraction(6, 10), Fraction(4, 10)]
    gamma = Fraction(3)
    tau = Fraction(5, 100)  # tau = 0.05

    # 1. Equilibrium risk premiums: mu_eq = gamma * S * w_mkt
    mu_eq = [gamma * sum(s_cov[i][j] * w_mkt[j] for j in range(2)) for i in range(2)]

    # Investor view: Asset 0 will outperform Asset 1 by 2% (0.02)
    # P = [1, -1], q = [0.02], Omega = [0.0001]
    p_mat = [[Fraction(1), Fraction(-1)]]
    q_vec = [Fraction(2, 100)]
    omega_val = Fraction(1, 10000)

    # Invert S
    det_s = s_cov[0][0] * s_cov[1][1] - s_cov[0][1] * s_cov[1][0]
    s_inv = [
        [s_cov[1][1] / det_s, -s_cov[0][1] / det_s],
        [-s_cov[1][0] / det_s, s_cov[0][0] / det_s],
    ]

    # 2. Precision form:
    # M = (tau S)^-1 + P' Omega^-1 P
    # v = (tau S)^-1 mu_eq + P' Omega^-1 q
    tau_s_inv = [[s_inv[i][j] / tau for j in range(2)] for i in range(2)]
    p_omega_inv_p = [[p_mat[0][i] * p_mat[0][j] / omega_val for j in range(2)] for i in range(2)]
    m_mat = [[tau_s_inv[i][j] + p_omega_inv_p[i][j] for j in range(2)] for i in range(2)]

    v_prior = [sum(tau_s_inv[i][j] * mu_eq[j] for j in range(2)) for i in range(2)]
    v_view = [p_mat[0][i] * q_vec[0] / omega_val for i in range(2)]
    v_vec = [v_prior[i] + v_view[i] for i in range(2)]

    det_m = m_mat[0][0] * m_mat[1][1] - m_mat[0][1] * m_mat[1][0]
    mu_bl_prec = [
        (m_mat[1][1] * v_vec[0] - m_mat[0][1] * v_vec[1]) / det_m,
        (-m_mat[1][0] * v_vec[0] + m_mat[0][0] * v_vec[1]) / det_m,
    ]

    # 3. Generalized least squares / Woodbury form:
    # mu_bl = mu_eq + tau S P' (P tau S P' + Omega)^-1 (q - P mu_eq)
    tau_s = [[tau * s_cov[i][j] for j in range(2)] for i in range(2)]
    p_tau_s_pt = sum(p_mat[0][i] * sum(tau_s[i][j] * p_mat[0][j] for j in range(2)) for i in range(2))
    denom = p_tau_s_pt + omega_val
    p_mu_eq = sum(p_mat[0][i] * mu_eq[i] for i in range(2))
    innov = q_vec[0] - p_mu_eq
    gain = [sum(tau_s[i][j] * p_mat[0][j] for j in range(2)) / denom for i in range(2)]
    mu_bl_alt = [mu_eq[i] + gain[i] * innov for i in range(2)]

    print(
        "Prior equilibrium mean mu_eq:",
        [round(float(x), 6) for x in mu_eq],
    )
    print(
        "Precision-form posterior mean:",
        [round(float(x), 6) for x in mu_bl_prec],
    )
    print(
        "Woodbury-form posterior mean:",
        [round(float(x), 6) for x in mu_bl_alt],
    )
    print("Exact algebraic equivalence verified:", mu_bl_prec == mu_bl_alt)


main()
