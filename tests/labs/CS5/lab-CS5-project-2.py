"""CS5 Project Rung 2: Completion problem for Monte Carlo pricing kernel.

Standard library only. SIMULATED data. Fills in the Box-Muller normal transform
and unbiased sample variance calculation.
"""

from __future__ import annotations

import math

SPLITMIX_GAMMA: int = 0x9E3779B97F4A7C15
SPLITMIX_MUL1: int = 0xBF58476D1CE4E5B9
SPLITMIX_MUL2: int = 0x94D049BB133111EB
MASK64: int = 0xFFFFFFFFFFFFFFFF
TWO_POW_53: float = 9007199254740992.0


def step_splitmix64(state: int) -> tuple[int, int]:
    state = (state + SPLITMIX_GAMMA) & MASK64
    z = state
    z = ((z ^ (z >> 30)) * SPLITMIX_MUL1) & MASK64
    z = ((z ^ (z >> 27)) * SPLITMIX_MUL2) & MASK64
    out = (z ^ (z >> 31)) & MASK64
    return state, out


def complete_pricer(n_paths: int = 1000, seed: int = 777) -> tuple[float, float, float, float]:
    """Execute completed Monte Carlo pricer for European options."""
    s0 = 100.0
    strike = 100.0
    rate = 0.05
    vol = 0.20
    maturity = 1.0

    state = seed & MASK64
    drift = (rate - 0.5 * vol * vol) * maturity
    vol_sqrt_t = vol * math.sqrt(maturity)
    df = math.exp(-rate * maturity)

    calls: list[float] = [0.0] * n_paths
    puts: list[float] = [0.0] * n_paths

    for i in range(n_paths):
        state, x1 = step_splitmix64(state)
        state, x2 = step_splitmix64(state)
        u1 = ((x1 >> 11) + 0.5) / TWO_POW_53
        u2 = ((x2 >> 11) + 0.5) / TWO_POW_53

        # Completed line 1: Box-Muller transform
        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)

        st = s0 * math.exp(drift + vol_sqrt_t * z)
        calls[i] = df * max(st - strike, 0.0)
        puts[i] = df * max(strike - st, 0.0)

    call_price = sum(calls) / n_paths
    put_price = sum(puts) / n_paths

    # Completed line 2: Unbiased sample variance with n - 1 degrees of freedom
    call_var = sum((c - call_price) ** 2 for c in calls) / (n_paths - 1)
    put_var = sum((p - put_price) ** 2 for p in puts) / (n_paths - 1)

    call_se = math.sqrt(call_var / n_paths)
    put_se = math.sqrt(put_var / n_paths)

    return call_price, call_se, put_price, put_se


def main() -> None:
    cp, c_se, pp, p_se = complete_pricer(n_paths=1000, seed=777)
    print("Paths: 1000, Seed: 777")
    print(f"Call: {cp:.6f} +/- {c_se:.6f}")
    print(f"Put:  {pp:.6f} +/- {p_se:.6f}")


main()
