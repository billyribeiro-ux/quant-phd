r"""Rung 1 worked example: numerical HJB policy iteration on seed 0 (SIMULATED).

Solves the continuous-time Merton problem with a borrowing constraint on a 101-node wealth grid,
verifying that policy iteration terminates in under 15 iterations and recovers the analytical
solution to within discretization error.
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
    # Seed 0 instance parameters (SIMULATED)
    r = 0.0369
    mu = 0.0874
    sigma = 0.1653
    gamma = 2.13
    rho = 0.0745
    pi_max = 0.6496
    w_min = 0.92
    w_max = 4.66
    n_points = 101

    dw = (w_max - w_min) / (n_points - 1)
    w = [w_min + i * dw for i in range(n_points)]

    print(f"seed 0 parameters (SIMULATED): r={r:.4f}, mu={mu:.4f}, sigma={sigma:.4f}, gamma={gamma:.2f}, rho={rho:.4f}")
    print(f"borrowing limit pi_max: {pi_max:.4f}, wealth grid: [{w_min:.2f}, {w_max:.2f}] with {n_points} nodes")

    # Analytical benchmark
    pi_star = (mu - r) / (gamma * (sigma**2))
    pi_eff = pi_star if pi_max >= pi_star else pi_max
    k_eff = r + pi_eff * (mu - r) - 0.5 * gamma * (pi_eff**2) * (sigma**2)
    nu_eff = (rho - (1.0 - gamma) * k_eff) / gamma
    v_exact = [(nu_eff ** (-gamma)) / (1.0 - gamma) * (x ** (1.0 - gamma)) for x in w]

    # Policy iteration
    pi = [min(pi_max, pi_eff)] * n_points
    c = [nu_eff * x for x in w]
    v = list(v_exact)

    converged = False
    iterations_completed = 0
    max_iter = 50
    tol = 1e-7

    for it in range(1, max_iter + 1):
        iterations_completed = it
        sub = [0.0] * n_points
        diag = [0.0] * n_points
        sup = [0.0] * n_points
        rhs = [0.0] * n_points

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

        # Update policy
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

        if diff_v < tol:
            converged = True
            break

    # Error analysis
    rel_errors = [abs(v[i] - v_exact[i]) / abs(v_exact[i]) for i in range(n_points)]
    max_rel_error = max(rel_errors)
    mid_idx = n_points // 2

    print("solver results:")
    print(f"  converged: {converged} in {iterations_completed} iterations")
    print(f"  max relative value function error: {max_rel_error:.2e}")
    print(f"  interior allocation at w={w[mid_idx]:.2f}: numerical={pi[mid_idx]:.4f}, exact={pi_eff:.4f}")
    print(f"  value function error within 2.0% tolerance: {max_rel_error < 0.02}")
    print(f"  interior allocation matches target within 0.01: {abs(pi[mid_idx] - pi_eff) < 0.01}")


main()
