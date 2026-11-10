"""Lab E7-L08-1: Narrative Monetary Shock Identification (Romer & Romer 2004).

Implements the Romer & Romer (2004) two-step narrative shock derivation:
1. Extract intended policy target changes Delta i_m from historical FOMC minutes.
2. Regress intended changes on internal Federal Reserve Greenbook forecasts of inflation and real activity:
   Delta i_m = alpha + sum_i beta_i * pi^GB_{m, i} + sum_j gamma_j * y^GB_{m, j} + e_m
3. The residual e_m is orthogonal to central bank private information and economic projections.
"""

from __future__ import annotations


def romer_romer_orthogonalization(
    intended_changes: list[float],
    forecast_inflation_t: list[float],
    forecast_inflation_t1: list[float],
    forecast_output_t: list[float],
    forecast_output_t1: list[float],
) -> tuple[list[float], float, float]:
    """Regress intended target changes on Greenbook forecasts using pure OLS."""
    n = len(intended_changes)
    # Design matrix: [1.0, pi_0, pi_1, y_0, y_1]
    x_mat: list[list[float]] = []
    y: list[float] = intended_changes[:]

    for i in range(n):
        x_mat.append(
            [1.0, forecast_inflation_t[i], forecast_inflation_t1[i], forecast_output_t[i], forecast_output_t1[i]]
        )

    k = 5
    # OLS: beta = inv(X'X) * X'y
    xtx = [[sum(x_mat[t][i] * x_mat[t][j] for t in range(n)) for j in range(k)] for i in range(k)]
    xty = [sum(x_mat[t][i] * y[t] for t in range(n)) for i in range(k)]

    # Invert XtX (Gauss-Jordan)
    aug = [[xtx[i][j] for j in range(k)] + [1.0 if i == j else 0.0 for j in range(k)] for i in range(k)]
    for col in range(k):
        pivot = col
        max_val = abs(aug[col][col])
        for row in range(col + 1, k):
            if abs(aug[row][col]) > max_val:
                max_val = abs(aug[row][col])
                pivot = row
        aug[col], aug[pivot] = aug[pivot], aug[col]
        pivot_val = aug[col][col]
        for j in range(2 * k):
            aug[col][j] /= pivot_val
        for row in range(k):
            if row != col:
                factor = aug[row][col]
                for j in range(2 * k):
                    aug[row][j] -= factor * aug[col][j]

    inv_xtx = [[aug[i][k + j] for j in range(k)] for i in range(k)]
    beta = [sum(inv_xtx[i][j] * xty[j] for j in range(k)) for i in range(k)]

    residuals = [y[t] - sum(x_mat[t][j] * beta[j] for j in range(k)) for t in range(n)]

    # Compute R^2
    mean_y = sum(y) / n
    ss_tot = sum((yi - mean_y) ** 2 for yi in y)
    ss_res = sum(ri**2 for ri in residuals)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 1e-12 else 0.0

    return residuals, r2, beta[1]


def main() -> None:
    # Representative sample of 10 FOMC meetings with Greenbook forecasts
    # Intended federal funds rate changes (in bps)
    delta_i = [25.0, 0.0, 50.0, -25.0, 0.0, 25.0, 25.0, 0.0, -50.0, 25.0]

    # Greenbook forecast revisions (inflation and real output growth, in %)
    pi_0 = [2.4, 2.1, 3.2, 1.8, 2.0, 2.7, 2.9, 2.2, 1.5, 2.8]
    pi_1 = [2.5, 2.2, 3.5, 1.9, 2.1, 2.8, 3.0, 2.3, 1.4, 2.9]
    y_0 = [2.8, 2.0, 3.5, 1.0, 2.2, 3.0, 3.2, 2.1, 0.5, 3.1]
    y_1 = [2.9, 2.1, 3.6, 1.2, 2.3, 3.1, 3.3, 2.2, 0.8, 3.2]

    shocks, r2, beta_inf = romer_romer_orthogonalization(delta_i, pi_0, pi_1, y_0, y_1)

    print("Romer & Romer (2004) Narrative Monetary Shock Derivation:")
    print(f"  Greenbook forecast regression R^2: {r2:.4f}")
    print(f"  Inflation forecast response coefficient beta_pi: {beta_inf:.3f}")
    print("\nMeeting | Intended Change (bps) | Systematic Component | Narrative Shock e_m")
    for m in range(len(delta_i)):
        sys_comp = delta_i[m] - shocks[m]
        print(
            f"  M{m + 1:02d}    |        {delta_i[m]:+5.1f}          |        {sys_comp:+5.1f}         |"
            f"       {shocks[m]:+5.1f}"
        )


main()
