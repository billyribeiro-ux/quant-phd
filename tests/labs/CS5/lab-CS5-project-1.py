"""CS5 Project Rung 1: Worked example tracing Monte Carlo path generation.

Standard library only. SIMULATED data. Traces exact SplitMix64 state transitions,
uniform extraction, Box-Muller normal generation, and discounted payoffs.
"""

from __future__ import annotations

import math

SPLITMIX_GAMMA: int = 0x9E3779B97F4A7C15
SPLITMIX_MUL1: int = 0xBF58476D1CE4E5B9
SPLITMIX_MUL2: int = 0x94D049BB133111EB
MASK64: int = 0xFFFFFFFFFFFFFFFF
TWO_POW_53: float = 9007199254740992.0


def step_splitmix64(state: int) -> tuple[int, int]:
    """Advance 64-bit state by one step and return (new_state, output_64bit)."""
    state = (state + SPLITMIX_GAMMA) & MASK64
    z = state
    z = ((z ^ (z >> 30)) * SPLITMIX_MUL1) & MASK64
    z = ((z ^ (z >> 27)) * SPLITMIX_MUL2) & MASK64
    out = (z ^ (z >> 31)) & MASK64
    return state, out


def trace_two_paths() -> None:
    """Trace a 2-path Monte Carlo option pricing calculation step by step."""
    s0 = 100.0
    strike = 100.0
    rate = 0.05
    vol = 0.20
    maturity = 1.0
    seed = 42

    drift = (rate - 0.5 * vol * vol) * maturity
    vol_sqrt_t = vol * math.sqrt(maturity)
    df = math.exp(-rate * maturity)

    state = seed & MASK64
    discounted_calls: list[float] = []
    discounted_puts: list[float] = []

    print(f"Parameters: S0={s0:.1f}, K={strike:.1f}, r={rate:.2f}, sigma={vol:.2f}, tau={maturity:.1f}, seed={seed}")
    print(f"Drift term: (r - 0.5*sigma^2)*tau = {drift:.6f}")
    print(f"Diffusion multiplier: sigma*sqrt(tau) = {vol_sqrt_t:.6f}")
    print(f"Discount factor: exp(-r*tau) = {df:.6f}")

    for path_idx in range(2):
        state, x1 = step_splitmix64(state)
        state, x2 = step_splitmix64(state)
        u1 = ((x1 >> 11) + 0.5) / TWO_POW_53
        u2 = ((x2 >> 11) + 0.5) / TWO_POW_53

        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        st = s0 * math.exp(drift + vol_sqrt_t * z)
        c_payoff = max(st - strike, 0.0)
        p_payoff = max(strike - st, 0.0)
        dc = df * c_payoff
        dp = df * p_payoff
        discounted_calls.append(dc)
        discounted_puts.append(dp)

        print(
            f"Path {path_idx + 1}: x1=0x{x1:016x} x2=0x{x2:016x} u1={u1:.6f} u2={u2:.6f} "
            f"z={z:+.6f} ST={st:.4f} CallPayoff={c_payoff:.4f} PutPayoff={p_payoff:.4f}"
        )

    call_mean = sum(discounted_calls) / 2.0
    put_mean = sum(discounted_puts) / 2.0
    # Sample variance with ddof = 1
    call_var = sum((x - call_mean) ** 2 for x in discounted_calls) / 1.0
    put_var = sum((x - put_mean) ** 2 for x in discounted_puts) / 1.0
    call_se = math.sqrt(call_var / 2.0)
    put_se = math.sqrt(put_var / 2.0)

    print(f"Estimated Call Price: {call_mean:.6f} (SE: {call_se:.6f})")
    print(f"Estimated Put Price:  {put_mean:.6f} (SE: {put_se:.6f})")


def main() -> None:
    trace_two_paths()


main()
