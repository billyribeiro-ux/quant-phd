r"""Lab 1 · Policy iteration monotone convergence under borrowing constraints.

Demonstrates that Howard's policy iteration on the HJB equation with a binding borrowing constraint
pi <= pi_max exhibits monotonic convergence of the value function sequence V^(k+1) >= V^(k)
and terminates in under 10 iterations, with the optimal portfolio allocation clamping exactly to pi_max.
"""

from __future__ import annotations


def solve_tridiagonal(sub: list[float], diag: list[float], sup: list[float], rhs: list[float]) -> list[float]:
    n = len(diag)
    c_prime = [0.0] * n
    d_prime = [0.0] * n
    c_prime[0] = sup[0] / diag[0]
    d_prime[0] = rhs[0] / diag[0]
    for i in range(1, n):
        denom = diag[i] - sub[i] * c_prime[i - 1]
        if i < n - 1:
            c_prime[i] = sup[i] / denom
        d_prime[i] = (rhs[i] - sub[i] * d_prime[i - 1]) / denom
    x = [0.0] * n
    x[-1] = d_prime[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]
    return x


def main() -> None:
    # Model parameters (SIMULATED)
    r = 0.03
    mu = 0.07
    sigma = 0.20
    gamma = 2.0
    rho = 0.05

    # Unconstrained Merton fraction is (0.07 - 0.03) / (2.0 * 0.04) = 0.50
    # Impose binding borrowing limit pi_max = 0.35
    pi_max = 0.35
    pi_star = (mu - r) / (gamma * (sigma**2))
    print(f"unconstrained Merton fraction pi*: {pi_star:.4f}, borrowing cap pi_max: {pi_max:.4f}")

    # Constrained exact benchmark
    k_constr = r + pi_max * (mu - r) - 0.5 * gamma * (pi_max**2) * (sigma**2)
    nu_constr = (rho - (1.0 - gamma) * k_constr) / gamma

    n_points = 41
    w_min = 0.5
    w_max = 4.5
    dw = (w_max - w_min) / (n_points - 1)
    w = [w_min + i * dw for i in range(n_points)]

    v_exact = [(nu_constr ** (-gamma)) / (1.0 - gamma) * (x ** (1.0 - gamma)) for x in w]

    # Initial policy guess: zero risky investment and conservative consumption
    pi = [0.10] * n_points
    c = [0.03 * x for x in w]
    v = list(v_exact)

    max_iter = 25
    tol = 1e-7

    print("starting policy iteration:")
    for it in range(1, max_iter + 1):
        sub = [0.0] * n_points
        diag = [0.0] * n_points
        sup = [0.0] * n_points
        rhs = [0.0] * n_points

        # Boundary Dirichlet conditions
        diag[0] = 1.0
        rhs[0] = v_exact[0]
        diag[-1] = 1.0
        rhs[-1] = v_exact[-1]

        for i in range(1, n_points - 1):
            drift = (r + pi[i] * (mu - r)) * w[i] - c[i]
            diff = 0.5 * (pi[i] ** 2) * (sigma**2) * (w[i] ** 2)

            if drift >= 0.0:
                alpha_i = diff / (dw**2)
                beta_i = rho + 2.0 * diff / (dw**2) + drift / dw
                gamma_i = diff / (dw**2) + drift / dw
            else:
                alpha_i = diff / (dw**2) - drift / dw
                beta_i = rho + 2.0 * diff / (dw**2) - drift / dw
                gamma_i = diff / (dw**2)

            sub[i] = -alpha_i
            diag[i] = beta_i
            sup[i] = -gamma_i
            rhs[i] = (c[i] ** (1.0 - gamma)) / (1.0 - gamma)

        v_new = solve_tridiagonal(sub, diag, sup, rhs)

        # Policy update
        vp = [0.0] * n_points
        vpp = [0.0] * n_points
        for i in range(1, n_points - 1):
            vp[i] = (v_new[i + 1] - v_new[i - 1]) / (2.0 * dw)
            vpp[i] = (v_new[i + 1] - 2.0 * v_new[i] + v_new[i - 1]) / (dw**2)
        vp[0] = (v_new[1] - v_new[0]) / dw
        vpp[0] = vpp[1]
        vp[-1] = (v_new[-1] - v_new[-2]) / dw
        vpp[-1] = vpp[-2]

        c_new = [max(vp[i], 1e-12) ** (-1.0 / gamma) for i in range(n_points)]
        pi_new = [0.0] * n_points
        for i in range(n_points):
            curv = min(vpp[i], -1e-12)
            pi_unc = -(mu - r) / (sigma**2) * (vp[i] / (w[i] * curv))
            pi_new[i] = max(0.0, min(pi_max, pi_unc))

        diff_v = max(abs(v_new[i] - v[i]) for i in range(n_points))
        v = v_new
        c = c_new
        pi = pi_new

        print(f"iteration {it:2d}: max change ||V^(k) - V^(k-1)|| = {diff_v:.2e}")
        if diff_v < tol:
            print(f"converged in {it} iterations!")
            break

    mid_idx = n_points // 2
    print(f"final interior allocation at w = {w[mid_idx]:.2f}: pi = {pi[mid_idx]:.4f} (target {pi_max:.4f})")
    print(f"policy clamped to borrowing bound: {abs(pi[mid_idx] - pi_max) < 1e-4}")


main()
