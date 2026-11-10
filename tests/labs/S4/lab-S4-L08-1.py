"""Lab S4-L08-1: Patton (2011) ranking consistency under imperfect volatility proxies.

SIMULATED: generates true latent conditional variance and a conditionally unbiased
noisy proxy y_t = sigma_t^2 * z_t^2. Compares Model 1 (superior) vs Model 2 (inferior)
under QLIKE, MSE, and non-robust MAE loss to verify ranking robustness.
"""

from __future__ import annotations

import math
import random


def run_patton_experiment(n: int = 5000, seed: int = 42) -> None:
    """Evaluate model rankings on true variance versus proxy."""
    rng = random.Random(seed)

    sigma2 = [1.0]
    for _ in range(n):
        s = 0.20 + 0.80 * sigma2[-1] + rng.gauss(0.0, 0.05)
        sigma2.append(max(0.2, s))
    sigma2 = sigma2[1:]

    # Model 1 (Superior): small zero-mean error
    h1 = [s + rng.gauss(0.0, 0.05) for s in sigma2]
    # Model 2 (Inferior): biased + noisier
    h2 = [s + rng.gauss(0.10, 0.15) for s in sigma2]

    # Unbiased noisy proxy: y_t = sigma_t^2 * z_t^2
    y_proxy = [s * (rng.gauss(0.0, 1.0) ** 2) for s in sigma2]

    def avg_losses(target: list[float], h: list[float]) -> tuple[float, float, float]:
        mse = sum((target[i] - h[i]) ** 2 for i in range(n)) / n
        qlike = sum((target[i] / h[i]) - math.log(target[i] / h[i]) - 1.0 for i in range(n)) / n
        mae = sum(abs(target[i] - h[i]) for i in range(n)) / n
        return mse, qlike, mae

    mse1_true, q1_true, mae1_true = avg_losses(sigma2, h1)
    mse2_true, q2_true, mae2_true = avg_losses(sigma2, h2)

    mse1_prx, q1_prx, mae1_prx = avg_losses(y_proxy, h1)
    mse2_prx, q2_prx, mae2_prx = avg_losses(y_proxy, h2)

    print("Patton (2011) Loss Robustness Verification:")
    print("Loss Metric | True Var Loss (M1 vs M2) | Noisy Proxy Loss (M1 vs M2) | Ranking Preserved?")
    print("-" * 80)

    # MSE
    win_t_mse = "M1 < M2" if mse1_true < mse2_true else "M2 < M1"
    win_p_mse = "M1 < M2" if mse1_prx < mse2_prx else "M2 < M1"
    ok_mse = "YES (Robust)" if win_t_mse == win_p_mse else "NO (Distorted)"
    print(
        f"MSE         |   {mse1_true:.4f} vs {mse2_true:.4f} ({win_t_mse})  |"
        f"   {mse1_prx:.4f} vs {mse2_prx:.4f} ({win_p_mse})   | {ok_mse}"
    )

    # QLIKE
    win_t_q = "M1 < M2" if q1_true < q2_true else "M2 < M1"
    win_p_q = "M1 < M2" if q1_prx < q2_prx else "M2 < M1"
    ok_q = "YES (Robust)" if win_t_q == win_p_q else "NO (Distorted)"
    print(
        f"QLIKE       |   {q1_true:.4f} vs {q2_true:.4f} ({win_t_q})  |"
        f"   {q1_prx:.4f} vs {q2_prx:.4f} ({win_p_q})   | {ok_q}"
    )

    # MAE
    win_t_mae = "M1 < M2" if mae1_true < mae2_true else "M2 < M1"
    win_p_mae = "M1 < M2" if mae1_prx < mae2_prx else "M2 < M1"
    ok_mae = "YES" if win_t_mae == win_p_mae else "NO (Distorted)"
    print(
        f"MAE         |   {mae1_true:.4f} vs {mae2_true:.4f} ({win_t_mae})  |"
        f"   {mae1_prx:.4f} vs {mae2_prx:.4f} ({win_p_mae})   | {ok_mae}"
    )


def main() -> None:
    run_patton_experiment(n=5000, seed=42)


main()
