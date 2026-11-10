"""Lab MS4-project-3: Rung 3 benchmark parameter grid for research memo.

Generates comparative strategy capacity and optimal AUM estimates across varying
market impact prefactors (Y in {0.30, 0.50, 0.70}) and gross alpha levels (alpha in {0.06, 0.10}).
SIMULATED: reference universe calibration for student analytical memo.
"""

from __future__ import annotations

import math


def run_benchmark_parameter_grid() -> None:
    # 5-asset factor portfolio
    universe = [
        (0.20, 0.35, 25000000.0, 0.020),
        (0.20, 0.10, 35000000.0, 0.018),
        (0.20, 0.05, 18000000.0, 0.026),
        (0.20, 0.30, 45000000.0, 0.016),
        (0.20, 0.20, 30000000.0, 0.022),
    ]

    prefactors = [0.30, 0.50, 0.70]
    alphas = [0.06, 0.10]

    print("Factor Strategy Capacity Sensitivity Grid:")
    print("-----------------------------------------------------------------------------------------")
    print("Prefactor Y | Gross Alpha | Friction Kappa | Break-even AUM ($B) | Optimal AUM ($B) | Max Dollar Alpha ($M)")
    print("-----------------------------------------------------------------------------------------")

    for y in prefactors:
        kappa = y * sum(vol * (abs(w_tgt - w_init) ** 1.5) / math.sqrt(adv) for w_init, w_tgt, adv, vol in universe)
        for alpha in alphas:
            a_star = (alpha / kappa) ** 2
            a_opt = (4.0 / 9.0) * a_star
            max_d_alpha = (4.0 / 27.0) * (alpha**3) / (kappa**2)

            a_star_billions = a_star / 1e9
            a_opt_billions = a_opt / 1e9
            max_d_millions = max_d_alpha / 1e6

            print(
                f"{y:11.2f} | {alpha * 100.0:10.1f}% | {kappa:14.6e} | "
                f"{a_star_billions:19.2f} | {a_opt_billions:16.2f} | {max_d_millions:21.2f}"
            )


def main() -> None:
    run_benchmark_parameter_grid()


main()
