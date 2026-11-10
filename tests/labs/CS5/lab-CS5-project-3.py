"""CS5 Project Rung 3: Independent verification driver and performance baseline.

Standard library only. SIMULATED data. Runs the reference pricing kernel over
10,000 paths, validating stream integrity, option values, and put-call parity.
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


def run_benchmark(n_paths: int = 10000, seed: int = 20261110) -> None:
    s0 = 100.0
    strike = 100.0
    rate = 0.05
    vol = 0.20
    maturity = 1.0

    state = seed & MASK64
    first_four: list[str] = []
    for _ in range(4):
        state, val = step_splitmix64(state)
        first_four.append(f"0x{val:016x}")

    # Reset state for path pricing
    state = seed & MASK64
    drift = (rate - 0.5 * vol * vol) * maturity
    vol_sqrt_t = vol * math.sqrt(maturity)
    df = math.exp(-rate * maturity)

    calls: list[float] = [0.0] * n_paths
    puts: list[float] = [0.0] * n_paths
    st_sum = 0.0

    for i in range(n_paths):
        state, x1 = step_splitmix64(state)
        state, x2 = step_splitmix64(state)
        u1 = ((x1 >> 11) + 0.5) / TWO_POW_53
        u2 = ((x2 >> 11) + 0.5) / TWO_POW_53

        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        st = s0 * math.exp(drift + vol_sqrt_t * z)
        st_sum += st

        calls[i] = df * max(st - strike, 0.0)
        puts[i] = df * max(strike - st, 0.0)

    call_price = sum(calls) / n_paths
    put_price = sum(puts) / n_paths
    mean_st = st_sum / n_paths

    call_var = sum((c - call_price) ** 2 for c in calls) / (n_paths - 1)
    put_var = sum((p - put_price) ** 2 for p in puts) / (n_paths - 1)
    call_se = math.sqrt(call_var / n_paths)
    put_se = math.sqrt(put_var / n_paths)

    parity_lhs = call_price - put_price
    parity_rhs = df * (mean_st - strike)

    print(f"Rung 3 Benchmark Results (Paths: {n_paths}, Seed: {seed}):")
    print(f"Generator first 4 outputs: {', '.join(first_four)}")
    print(f"Call Price: {call_price:.6f} (SE: {call_se:.6f})")
    print(f"Put Price:  {put_price:.6f} (SE: {put_se:.6f})")
    print(f"Put-Call Parity: LHS={parity_lhs:.6f}, RHS={parity_rhs:.6f}, Diff={abs(parity_lhs - parity_rhs):.2e}")


def main() -> None:
    run_benchmark()


main()
