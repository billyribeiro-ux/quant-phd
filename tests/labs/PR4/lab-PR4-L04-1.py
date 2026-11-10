"""Lab 4: Christoffersen Independence and Conditional Coverage Backtest.

Demonstrates that unconditional coverage (Kupiec) fails to detect exception
clustering, while Christoffersen (1998) likelihood ratio tests reveal volatility clustering.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def christoffersen_framework(
    hits: np.ndarray[Any, Any],
    alpha: float = 0.99,
) -> dict[str, float]:
    """Execute Kupiec POF and Christoffersen independence and conditional coverage tests."""
    arr = np.asarray(hits, dtype=np.int64)
    t = len(arr)
    x = int(np.sum(arr))
    p = 1.0 - alpha
    p_hat = x / t

    # 1. Unconditional Coverage (Kupiec 1995)
    if x == 0:
        lr_uc = -2.0 * t * math.log(1.0 - p)
    elif x == t:
        lr_uc = -2.0 * t * math.log(p)
    else:
        lr_uc = -2.0 * (
            (t - x) * math.log(1.0 - p) + x * math.log(p) - (t - x) * math.log(1.0 - p_hat) - x * math.log(p_hat)
        )
    lr_uc = max(0.0, float(lr_uc))
    p_uc = float(math.erfc(math.sqrt(lr_uc / 2.0)))

    # 2. Independence of Exceptions (Christoffersen 1998)
    h_prev = arr[:-1]
    h_next = arr[1:]
    n00 = int(np.sum((h_prev == 0) & (h_next == 0)))
    n01 = int(np.sum((h_prev == 0) & (h_next == 1)))
    n10 = int(np.sum((h_prev == 1) & (h_next == 0)))
    n11 = int(np.sum((h_prev == 1) & (h_next == 1)))

    pi01 = n01 / (n00 + n01) if (n00 + n01) > 0 else 0.0
    pi11 = n11 / (n10 + n11) if (n10 + n11) > 0 else 0.0
    pi = (n01 + n11) / (n00 + n01 + n10 + n11) if (n00 + n01 + n10 + n11) > 0 else 0.0

    def safe_log(v: float) -> float:
        return math.log(v) if v > 1e-12 else 0.0

    log_l0 = (n00 + n10) * safe_log(1.0 - pi) + (n01 + n11) * safe_log(pi)
    log_l1 = n00 * safe_log(1.0 - pi01) + n01 * safe_log(pi01) + n10 * safe_log(1.0 - pi11) + n11 * safe_log(pi11)

    lr_ind = max(0.0, -2.0 * (log_l0 - log_l1))
    p_ind = float(math.erfc(math.sqrt(lr_ind / 2.0)))

    # 3. Joint Conditional Coverage
    lr_cc = lr_uc + lr_ind
    p_cc = float(math.exp(-lr_cc / 2.0))

    return {
        "n00": float(n00),
        "n01": float(n01),
        "n10": float(n10),
        "n11": float(n11),
        "pi01": pi01,
        "pi11": pi11,
        "lr_uc": lr_uc,
        "p_uc": p_uc,
        "lr_ind": lr_ind,
        "p_ind": p_ind,
        "lr_cc": lr_cc,
        "p_cc": p_cc,
    }


def main() -> None:
    t_days = 500
    alpha = 0.99
    expected_hits = int(t_days * (1.0 - alpha))  # 5 hits

    # Sequence A: Evenly spaced (iid-like) violations
    hits_spread = np.zeros(t_days, dtype=np.int64)
    hits_spread[[50, 150, 250, 350, 450]] = 1

    # Sequence B: Clustered violations during a volatility regime shock
    hits_clustered = np.zeros(t_days, dtype=np.int64)
    hits_clustered[100:105] = 1

    res_a = christoffersen_framework(hits_spread, alpha)
    res_b = christoffersen_framework(hits_clustered, alpha)

    print(f"Total Observations: {t_days} | Nominal 99% Expected Exceptions: {expected_hits}")
    print("=" * 70)
    print("Sequence A: Independent Spaced Exceptions")
    n00_a, n01_a = int(res_a["n00"]), int(res_a["n01"])
    n10_a, n11_a = int(res_a["n10"]), int(res_a["n11"])
    print(f"  Transitions: n00={n00_a}, n01={n01_a}, n10={n10_a}, n11={n11_a}")
    print(f"  pi01={res_a['pi01']:.4f}, pi11={res_a['pi11']:.4f}")
    print(f"  LR_uc  = {res_a['lr_uc']:.4f} (p={res_a['p_uc']:.4f})")
    print(f"  LR_ind = {res_a['lr_ind']:.4f} (p={res_a['p_ind']:.4f})")
    print(f"  LR_cc  = {res_a['lr_cc']:.4f} (p={res_a['p_cc']:.4f})")
    print("=" * 70)
    print("Sequence B: Clustered Contagion Exceptions")
    n00_b, n01_b = int(res_b["n00"]), int(res_b["n01"])
    n10_b, n11_b = int(res_b["n10"]), int(res_b["n11"])
    print(f"  Transitions: n00={n00_b}, n01={n01_b}, n10={n10_b}, n11={n11_b}")
    print(f"  pi01={res_b['pi01']:.4f}, pi11={res_b['pi11']:.4f}")
    print(f"  LR_uc  = {res_b['lr_uc']:.4f} (p={res_b['p_uc']:.4f})")
    print(f"  LR_ind = {res_b['lr_ind']:.4f} (p={res_b['p_ind']:.4e})")
    print(f"  LR_cc  = {res_b['lr_cc']:.4f} (p={res_b['p_cc']:.4e})")


main()
