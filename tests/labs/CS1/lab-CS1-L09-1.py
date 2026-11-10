"""CS1 lab L09: Simple and log returns: vectorized vs loops on real market FX data.

Uses embedded real market snapshot fx_daily.csv from the Federal Reserve
(cleared in course/assets/data/market/MANIFEST.json, noon buying rates in New York, spot EUR/USD).
Compares vectorized NumPy array computation against iterative Python loops, verifying
equivalence to 1e-12, the identity ln(1 + r_t) = ell_t, and multi-period compounding.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


def compute_returns_loop(prices: list[float]) -> tuple[list[float], list[float]]:
    """Compute simple and log returns using iterative Python loops."""
    n = len(prices)
    if n < 2:
        raise ValueError("prices must contain at least 2 values")
    simple_rets: list[float] = [0.0] * (n - 1)
    log_rets: list[float] = [0.0] * (n - 1)
    for t in range(1, n):
        p_prev = prices[t - 1]
        p_curr = prices[t]
        simple_rets[t - 1] = p_curr / p_prev - 1.0
        log_rets[t - 1] = math.log(p_curr / p_prev)
    return simple_rets, log_rets


def compute_returns_vectorized(prices: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Compute simple and log returns using vectorized NumPy operations."""
    if len(prices) < 2:
        raise ValueError("prices must contain at least 2 values")
    # Vectorized ratio: P[1:] / P[:-1]
    p_prev = prices[:-1]
    p_curr = prices[1:]
    simple_rets = p_curr / p_prev - 1.0
    log_rets = np.log(p_curr / p_prev)
    return simple_rets, log_rets


def main() -> None:
    data_dir = Path("data")
    fx_path = data_dir / "fx_daily.csv"

    # Load EUR spot price series
    prices: list[float] = []
    with fx_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            val_str = row["EUR"]
            if val_str and val_str != "ND":
                prices.append(float(val_str))

    n_prices = len(prices)
    price_arr = np.array(prices, dtype=np.float64)

    # 1. Compute returns via both methods
    loop_simple, loop_log = compute_returns_loop(prices)
    vec_simple, vec_log = compute_returns_vectorized(price_arr)

    # 2. Check equivalence to 1e-12
    max_simple_diff = float(np.max(np.abs(np.array(loop_simple) - vec_simple)))
    max_log_diff = float(np.max(np.abs(np.array(loop_log) - vec_log)))
    simple_match = max_simple_diff < 1e-12
    log_match = max_log_diff < 1e-12

    # 3. Check mathematical identity: ln(1 + simple) == log_return
    identity_diffs = np.abs(np.log(1.0 + vec_simple) - vec_log)
    max_identity_diff = float(np.max(identity_diffs))
    identity_holds = max_identity_diff < 1e-12

    # 4. Multi-period aggregation properties
    # Log returns sum: sum(ell_t) == ln(P_T / P_0)
    sum_log_rets = float(np.sum(vec_log))
    total_log_return = math.log(prices[-1] / prices[0])
    log_additivity_holds = abs(sum_log_rets - total_log_return) < 1e-12

    # Simple returns compound: prod(1 + r_t) - 1 == P_T / P_0 - 1
    prod_simple_rets = float(np.prod(1.0 + vec_simple)) - 1.0
    total_simple_return = prices[-1] / prices[0] - 1.0
    simple_compounding_holds = abs(prod_simple_rets - total_simple_return) < 1e-12

    print(f"total EUR spot price observations: {n_prices}")
    print(f"computed return periods: {len(vec_simple)}")
    print(f"first EUR spot price: {prices[0]:.4f}")
    print(f"last EUR spot price: {prices[-1]:.4f}")
    print(f"loop and vectorized simple returns equal to 1e-12: {simple_match}")
    print(f"loop and vectorized log returns equal to 1e-12: {log_match}")
    print(f"identity log(1 + simple) == log_return holds to 1e-12: {identity_holds}")
    print(f"log returns additivity holds to 1e-12: {log_additivity_holds}")
    print(f"simple returns compounding holds to 1e-12: {simple_compounding_holds}")
    print(f"loop iterations: {n_prices - 1}, vectorized calls: 2")


main()
