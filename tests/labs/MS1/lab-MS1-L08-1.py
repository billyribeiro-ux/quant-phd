"""Lab MS1-L08-1: Volume-synchronised probability of informed trading (VPIN).

SIMULATED: generates volume buckets and price changes with a regime shift in order imbalance.
Implements bulk volume classification (BVC) with normal CDF and rolling-window VPIN computation,
verifying that VPIN remains bounded in [0, 1].
"""

from __future__ import annotations

import math
import random


def normal_cdf(x: float) -> float:
    """Compute standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bulk_volume_classification(price_change: float, sigma: float, bucket_vol: float) -> tuple[float, float, float]:
    """Partition bucket volume into buy and sell volume using normal CDF."""
    z = price_change / sigma if sigma > 0 else 0.0
    v_buy = bucket_vol * normal_cdf(z)
    v_sell = bucket_vol - v_buy
    imbalance = abs(v_buy - v_sell)
    return v_buy, v_sell, imbalance


def compute_vpin_series(
    price_changes: list[float], sigma: float, bucket_vol: float, window_size: int
) -> list[tuple[int, float]]:
    """Compute rolling window VPIN over consecutive volume buckets."""
    imbalances: list[float] = []
    for dp in price_changes:
        _, _, imb = bulk_volume_classification(dp, sigma, bucket_vol)
        imbalances.append(imb)

    vpin_values: list[tuple[int, float]] = []
    for i in range(window_size - 1, len(price_changes)):
        window_imb = sum(imbalances[i - window_size + 1 : i + 1])
        vpin = window_imb / (window_size * bucket_vol)
        vpin_values.append((i + 1, vpin))
    return vpin_values


def main() -> None:
    rng = random.Random(42)
    n_buckets = 30
    bucket_vol = 100.0
    window_size = 10
    sigma = 0.30

    # Simulate price changes: tranquil period with zero mean, then directional shock (buckets 12-18)
    price_changes: list[float] = []
    for i in range(n_buckets):
        if 12 <= i <= 18:
            price_changes.append(rng.gauss(-0.80, 0.40))
        else:
            price_changes.append(rng.gauss(0.0, 0.20))

    vpin_results = compute_vpin_series(price_changes, sigma, bucket_vol, window_size)

    print("VPIN Estimation across 30 Volume Buckets:")
    print(f"  Bucket volume V: {bucket_vol:.1f}")
    print(f"  Rolling window size N: {window_size} buckets")
    print(f"  Bulk volume classification scale sigma: {sigma:.2f}")
    print("Selected Rolling VPIN Values:")
    for b_idx, vpin in vpin_results:
        if b_idx in (10, 15, 19, 22, 26, 30):
            print(f"  End of Bucket {b_idx:2d}: VPIN = {vpin:.4f}")

    min_vpin = min(v for _, v in vpin_results)
    max_vpin = max(v for _, v in vpin_results)
    bounds_satisfied = (min_vpin >= 0.0) and (max_vpin <= 1.0)
    print("Bounds and Toxicity Checks:")
    print(f"  Minimum rolling VPIN: {min_vpin:.4f}")
    print(f"  Maximum rolling VPIN: {max_vpin:.4f}")
    print(f"  Mathematical bounds 0 <= VPIN <= 1 satisfied: {bounds_satisfied}")


main()
