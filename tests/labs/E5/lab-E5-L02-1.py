"""E5 L02 lab 1: growth accounting on a seeded SIMULATED Cobb-Douglas economy.

SIMULATED. The economy is generated from random.Random(2026) with uniform draws only, so every run prints the same
lines. Its levels are illustrative and are not national-accounts data. No redistributable national-accounts series is
embedded in this program yet, so the lesson's curriculum lab runs on this generated economy and says so on the page.

The economy has output Y_t = A_t * K_t**ALPHA * L_t**(1 - ALPHA) for periods t = 0 to HORIZON, with capital share
ALPHA = 0.3. Output is computed from the levels. The growth of Y is then measured from the Y levels, and the three-term
growth-accounting identity is checked against the generated growth of A.

Logs are natural logs. Growth rates are log growth, ln x_t - ln x_(t-1), unless a line says simple. Each printed number
is shown to six decimal places; the comparisons use the unrounded floats.
"""

from __future__ import annotations

import math
import random

ALPHA = 0.3
HORIZON = 40
SEED = 2026


def simulate_economy(seed: int, horizon: int) -> tuple[list[float], list[float], list[float], list[float]]:
    """Generate levels of A, K, L and Y for periods 0 to horizon.

    A, K and L grow at seeded uniform log rates: A between 0.005 and 0.02, K between 0.02 and 0.05, and L between 0 and
    0.015 per period. Output is Y = A * K**ALPHA * L**(1 - ALPHA), computed from the levels. Returns (A, K, L, Y).
    """
    rng = random.Random(seed)
    a_levels, k_levels, l_levels = [1.0], [100.0], [50.0]
    for _ in range(horizon):
        a_levels.append(a_levels[-1] * math.exp(rng.uniform(0.005, 0.02)))
        k_levels.append(k_levels[-1] * math.exp(rng.uniform(0.02, 0.05)))
        l_levels.append(l_levels[-1] * math.exp(rng.uniform(0.0, 0.015)))
    y_levels = [
        a_t * k_t**ALPHA * l_t ** (1 - ALPHA) for a_t, k_t, l_t in zip(a_levels, k_levels, l_levels, strict=True)
    ]
    return a_levels, k_levels, l_levels, y_levels


def log_growth(levels: list[float]) -> list[float]:
    """Log growth ln x_t - ln x_(t-1) for t = 1 to len(levels) - 1, one value per period."""
    return [math.log(levels[t]) - math.log(levels[t - 1]) for t in range(1, len(levels))]


def simple_growth(levels: list[float]) -> list[float]:
    """Simple growth x_t / x_(t-1) - 1 for t = 1 to len(levels) - 1, one value per period."""
    return [levels[t] / levels[t - 1] - 1.0 for t in range(1, len(levels))]


def residual_growth(dln_y: list[float], dln_k: list[float], dln_l: list[float], alpha: float) -> list[float]:
    """Solow residual per period: dln Y - alpha * dln K - (1 - alpha) * dln L, for capital share alpha in (0, 1)."""
    return [y - alpha * k - (1.0 - alpha) * lab for y, k, lab in zip(dln_y, dln_k, dln_l, strict=True)]


def mean(values: list[float]) -> float:
    """Arithmetic mean of a non-empty list."""
    return sum(values) / len(values)


def main() -> None:
    """Print the identity check, the average decomposition, the sensitivity to alpha and the growth conventions."""
    a_levels, k_levels, l_levels, y_levels = simulate_economy(SEED, HORIZON)
    dln_y = log_growth(y_levels)
    dln_k = log_growth(k_levels)
    dln_l = log_growth(l_levels)
    dln_a = log_growth(a_levels)
    residual = residual_growth(dln_y, dln_k, dln_l, ALPHA)

    print(f"SIMULATED economy: seed {SEED}, horizon {HORIZON} periods, capital share alpha {ALPHA}")
    identity_gap = max(abs(r - a) for r, a in zip(residual, dln_a, strict=True))
    print(f"largest gap between the residual and the generated growth of A: {identity_gap:.6f}")
    print(f"residual equals the generated growth of A to 1e-12 in every period: {identity_gap < 1e-12}")

    mean_y = mean(dln_y)
    mean_k = mean(dln_k)
    mean_l = mean(dln_l)
    capital_term = ALPHA * mean_k
    labour_term = (1.0 - ALPHA) * mean_l
    mean_residual = mean(residual)
    print(f"average log growth of Y {mean_y:.6f}")
    print(f"average capital term alpha * dln K {capital_term:.6f}")
    print(f"average labour term (1 - alpha) * dln L {labour_term:.6f}")
    print(f"average residual {mean_residual:.6f}")
    share_capital = capital_term / mean_y
    share_labour = labour_term / mean_y
    share_residual = mean_residual / mean_y
    print(
        f"shares of average log growth of Y: capital {share_capital:.6f}, labour {share_labour:.6f}, "
        f"residual {share_residual:.6f}"
    )
    print(f"the three shares sum to 1: {abs(share_capital + share_labour + share_residual - 1.0) < 1e-12}")

    for alpha in (0.2, 0.4):
        alt = mean(residual_growth(dln_y, dln_k, dln_l, alpha))
        print(f"average residual with alpha {alpha}: {alt:.6f}")
    print(
        f"the residual depends on the chosen alpha: "
        f"{mean(residual_growth(dln_y, dln_k, dln_l, 0.2)) != mean(residual_growth(dln_y, dln_k, dln_l, 0.4))}"
    )

    simple_y = simple_growth(y_levels)
    never_above = all(math.log(1.0 + s) <= s for s in simple_y)
    print(f"average simple growth of Y {mean(simple_y):.6f}; average log growth of Y {mean_y:.6f}")
    print(f"log growth is at most simple growth in every period: {never_above}")


main()
