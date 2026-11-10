"""Lab Project 2 (Rung 2 Completion Problem): Christoffersen Independence Engine.

Twin solution for the completion problem: implements first-order Markov
transition counts, maximum likelihood transition probabilities, and the independence LR statistic.
"""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    # 250-day exception sequence with volatility clustering (hits at t=20, 21, 22)
    hits = np.zeros(250, dtype=np.int64)
    hits[20:23] = 1

    h_prev = hits[:-1]
    h_next = hits[1:]

    # 1. Transition counts
    n00 = int(np.sum((h_prev == 0) & (h_next == 0)))
    n01 = int(np.sum((h_prev == 0) & (h_next == 1)))
    n10 = int(np.sum((h_prev == 1) & (h_next == 0)))
    n11 = int(np.sum((h_prev == 1) & (h_next == 1)))

    # 2. Maximum likelihood transition probabilities
    pi01 = n01 / (n00 + n01) if (n00 + n01) > 0 else 0.0
    pi11 = n11 / (n10 + n11) if (n10 + n11) > 0 else 0.0
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)

    # 3. Log-likelihoods under H0 (independence) vs H1 (first-order Markov)
    def s_log(v: float) -> float:
        return math.log(v) if v > 1e-12 else 0.0

    log_l0 = (n00 + n10) * s_log(1.0 - pi) + (n01 + n11) * s_log(pi)
    log_l1 = n00 * s_log(1.0 - pi01) + n01 * s_log(pi01) + n10 * s_log(1.0 - pi11) + n11 * s_log(pi11)

    # 4. Independence Likelihood Ratio Test Statistic and p-value
    lr_ind = max(0.0, -2.0 * (log_l0 - log_l1))
    p_ind = float(math.erfc(math.sqrt(lr_ind / 2.0)))

    print(f"Transition Matrix: [[n00={n00}, n01={n01}], [n10={n10}, n11={n11}]]")
    print(f"Transition Probabilities: pi01={pi01:.4f}, pi11={pi11:.4f}, pi={pi:.4f}")
    print(f"Christoffersen Independence LR_ind: {lr_ind:.4f}")
    print(f"Independence Test p-value: {p_ind:.4e}")
    print(f"Clustering Rejected at 5%: {p_ind < 0.05}")


main()
