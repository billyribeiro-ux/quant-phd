"""Student error: omits Ito convexity correction in drift term (uses r instead of r - 0.5 * sigma^2)."""

from __future__ import annotations

import math

from integrity import validate_pricing_inputs, validate_stream_inputs

SPLITMIX_GAMMA: int = 0x9E3779B97F4A7C15
SPLITMIX_MUL1: int = 0xBF58476D1CE4E5B9
SPLITMIX_MUL2: int = 0x94D049BB133111EB
MASK64: int = 0xFFFFFFFFFFFFFFFF
TWO_POW_53: float = 9007199254740992.0


def _splitmix64_step(state: int) -> tuple[int, int]:
    state = (state + SPLITMIX_GAMMA) & MASK64
    z = state
    z = ((z ^ (z >> 30)) * SPLITMIX_MUL1) & MASK64
    z = ((z ^ (z >> 27)) * SPLITMIX_MUL2) & MASK64
    out = (z ^ (z >> 31)) & MASK64
    return state, out


def rng_stream(seed: int, count: int) -> list[int]:
    validate_stream_inputs(seed, count)
    state = seed & MASK64
    result: list[int] = []
    for _ in range(count):
        state, val = _splitmix64_step(state)
        result.append(val)
    return result


def price_call_and_put(
    s0: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_paths: int,
    seed: int,
) -> tuple[float, float, float, float]:
    validate_pricing_inputs(s0, strike, rate, vol, maturity, n_paths, seed)
    state = seed & MASK64
    # BUG: Omitted -0.5 * vol * vol
    drift = rate * maturity
    vol_sqrt_t = vol * math.sqrt(maturity)
    df = math.exp(-rate * maturity)

    discounted_calls: list[float] = [0.0] * n_paths
    discounted_puts: list[float] = [0.0] * n_paths

    for i in range(n_paths):
        state, x1 = _splitmix64_step(state)
        state, x2 = _splitmix64_step(state)
        u1 = ((x1 >> 11) + 0.5) / TWO_POW_53
        u2 = ((x2 >> 11) + 0.5) / TWO_POW_53
        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        s_t = s0 * math.exp(drift + vol_sqrt_t * z)
        c_payoff = s_t - strike if s_t > strike else 0.0
        p_payoff = strike - s_t if strike > s_t else 0.0
        discounted_calls[i] = df * c_payoff
        discounted_puts[i] = df * p_payoff

    call_mean = sum(discounted_calls) / n_paths
    put_mean = sum(discounted_puts) / n_paths
    denom = n_paths - 1
    call_var = sum((x - call_mean) ** 2 for x in discounted_calls) / denom
    put_var = sum((x - put_mean) ** 2 for x in discounted_puts) / denom
    call_se = math.sqrt(call_var / n_paths)
    put_se = math.sqrt(put_var / n_paths)
    return call_mean, call_se, put_mean, put_se
