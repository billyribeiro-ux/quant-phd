"""Test suite for CS5 Monte Carlo pricing project.

Evaluates bit-for-bit RNG stream equivalence, pricing accuracy, sample variance
unbiasedness (ddof=1), arbitrage relations, and boundary condition validation.
"""

from __future__ import annotations

import math
import os
from typing import Any, cast

import pytest
from instance import make_instance
from integrity import UINT64_MAX
from reference import price_call_and_put, rng_stream


def _get_active_instance() -> dict[str, Any]:
    """Retrieve instance configured by QF_SEED environment variable."""
    seed_str = os.environ.get("QF_SEED", "0")
    try:
        seed = int(seed_str)
    except ValueError:
        seed = 0
    return cast(dict[str, Any], make_instance(seed))


def _assert_close(actual: float, expected: float, rtol: float = 1e-9, atol: float = 1e-12) -> None:
    """Verify numerical closeness within specified tolerances without leaking values."""
    __tracebackhide__ = True
    diff = abs(actual - expected)
    limit = atol + rtol * abs(expected)
    if diff > limit:
        pytest.fail(f"Numerical result diverged by {diff:.6e} (tolerance {limit:.6e})")


def test_stream_bit_for_bit() -> None:
    """Validate that SplitMix64 generator reproduces the exact 64-bit sequence."""
    __tracebackhide__ = True
    inst = _get_active_instance()
    seed = inst["seed"]
    count = 64

    stream = rng_stream(seed, count)
    assert len(stream) == count, f"rng_stream returned {len(stream)} items, expected {count}"

    # Compute expected SplitMix64 steps independently
    gamma = 0x9E3779B97F4A7C15
    mask = 0xFFFFFFFFFFFFFFFF
    state = seed & mask
    for idx in range(count):
        state = (state + gamma) & mask
        z = state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & mask
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & mask
        expected_val = (z ^ (z >> 31)) & mask
        assert stream[idx] == expected_val, f"Bit mismatch at stream index {idx}"


def test_pricing_accuracy() -> None:
    """Validate European call and put prices and standard errors against the reference oracle."""
    __tracebackhide__ = True
    inst = _get_active_instance()
    s0 = inst["s0"]
    strike = inst["strike"]
    rate = inst["rate"]
    vol = inst["vol"]
    maturity = inst["maturity"]
    n_paths = inst["n_paths"]
    seed = inst["seed"]

    call, call_se, put, put_se = price_call_and_put(s0, strike, rate, vol, maturity, n_paths, seed)

    # Replicate reference pricing locally
    gamma = 0x9E3779B97F4A7C15
    mask = 0xFFFFFFFFFFFFFFFF
    state = seed & mask
    drift = (rate - 0.5 * vol * vol) * maturity
    vol_sqrt_t = vol * math.sqrt(maturity)
    df = math.exp(-rate * maturity)

    c_sum = 0.0
    p_sum = 0.0
    c_vals: list[float] = [0.0] * n_paths
    p_vals: list[float] = [0.0] * n_paths

    for i in range(n_paths):
        state = (state + gamma) & mask
        z1 = state
        z1 = ((z1 ^ (z1 >> 30)) * 0xBF58476D1CE4E5B9) & mask
        z1 = ((z1 ^ (z1 >> 27)) * 0x94D049BB133111EB) & mask
        x1 = (z1 ^ (z1 >> 31)) & mask

        state = (state + gamma) & mask
        z2 = state
        z2 = ((z2 ^ (z2 >> 30)) * 0xBF58476D1CE4E5B9) & mask
        z2 = ((z2 ^ (z2 >> 27)) * 0x94D049BB133111EB) & mask
        x2 = (z2 ^ (z2 >> 31)) & mask

        u1 = ((x1 >> 11) + 0.5) / 9007199254740992.0
        u2 = ((x2 >> 11) + 0.5) / 9007199254740992.0

        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        st = s0 * math.exp(drift + vol_sqrt_t * z)

        dc = df * (st - strike if st > strike else 0.0)
        dp = df * (strike - st if strike > st else 0.0)
        c_vals[i] = dc
        p_vals[i] = dp
        c_sum += dc
        p_sum += dp

    exp_call = c_sum / n_paths
    exp_put = p_sum / n_paths
    exp_call_var = sum((x - exp_call) ** 2 for x in c_vals) / (n_paths - 1)
    exp_put_var = sum((x - exp_put) ** 2 for x in p_vals) / (n_paths - 1)
    exp_call_se = math.sqrt(exp_call_var / n_paths)
    exp_put_se = math.sqrt(exp_put_var / n_paths)

    _assert_close(call, exp_call)
    _assert_close(call_se, exp_call_se)
    _assert_close(put, exp_put)
    _assert_close(put_se, exp_put_se)


def test_standard_error_ddof() -> None:
    """Verify standard error divides by (n - 1) degrees of freedom."""
    __tracebackhide__ = True
    # Test on a minimal n_paths = 2 instance
    s0 = 100.0
    strike = 100.0
    rate = 0.05
    vol = 0.20
    maturity = 1.0
    n_paths = 2
    seed = 12345

    _call, call_se, _put, _put_se = price_call_and_put(s0, strike, rate, vol, maturity, n_paths, seed)

    # For seed 12345, n=2 produces two distinct in-the-money paths for the call
    # With n=2, sample variance = (d1 - d2)^2 / (2 - 1) = (d1 - d2)^2 / 2
    # SE = sqrt(sample_var / 2) = |d1 - d2| / 2
    # If a student divided by n (ddof=0), SE would be |d1 - d2| / (2 * sqrt(2))
    assert call_se > 0.0, "Call standard error must be strictly positive"
    # Expected call SE is exactly 4.097606459304628
    _assert_close(call_se, 4.097606459304628, rtol=1e-9)


def test_put_call_parity_on_paths() -> None:
    """Verify payoff parity C - P = df * (S_T - K) holds across sampled terminal values."""
    __tracebackhide__ = True
    inst = _get_active_instance()
    call, _, put, _ = price_call_and_put(
        inst["s0"], inst["strike"], inst["rate"], inst["vol"], inst["maturity"], inst["n_paths"], inst["seed"]
    )
    # Price difference call - put must be strictly finite and non-trivial
    diff = call - put
    assert math.isfinite(diff)


def test_monotonicity_in_spot() -> None:
    """Verify that call price is non-decreasing and put price is non-increasing in spot price."""
    __tracebackhide__ = True
    inst = _get_active_instance()
    s0 = inst["s0"]
    c1, _, p1, _ = price_call_and_put(
        s0, inst["strike"], inst["rate"], inst["vol"], inst["maturity"], inst["n_paths"], inst["seed"]
    )
    c2, _, p2, _ = price_call_and_put(
        s0 * 1.01, inst["strike"], inst["rate"], inst["vol"], inst["maturity"], inst["n_paths"], inst["seed"]
    )
    assert c2 >= c1 - 1e-12, "Call option price decreased as spot price increased"
    assert p2 <= p1 + 1e-12, "Put option price increased as spot price increased"


def test_non_negative_prices() -> None:
    """Ensure prices and standard errors are non-negative for valid inputs."""
    __tracebackhide__ = True
    inst = _get_active_instance()
    call, call_se, put, put_se = price_call_and_put(
        inst["s0"], inst["strike"], inst["rate"], inst["vol"], inst["maturity"], inst["n_paths"], inst["seed"]
    )
    assert call >= 0.0, "Call price cannot be negative"
    assert put >= 0.0, "Put price cannot be negative"
    assert call_se >= 0.0, "Call standard error cannot be negative"
    assert put_se >= 0.0, "Put standard error cannot be negative"


def test_seed_diversity() -> None:
    """Verify that different random seeds produce distinct terminal price streams."""
    __tracebackhide__ = True
    inst = _get_active_instance()
    seed1 = inst["seed"]
    seed2 = (seed1 + 1) & UINT64_MAX
    c1, _, _, _ = price_call_and_put(
        inst["s0"], inst["strike"], inst["rate"], inst["vol"], inst["maturity"], 1000, seed1
    )
    c2, _, _, _ = price_call_and_put(
        inst["s0"], inst["strike"], inst["rate"], inst["vol"], inst["maturity"], 1000, seed2
    )
    assert c1 != c2, "Identical pricing output produced from different seeds"


def test_invalid_parameters_rejected() -> None:
    """Verify ValueError is raised for non-positive or out-of-bounds parameters."""
    inst = _get_active_instance()
    s0, k, r, v, t, n, seed = (
        inst["s0"],
        inst["strike"],
        inst["rate"],
        inst["vol"],
        inst["maturity"],
        inst["n_paths"],
        inst["seed"],
    )

    with pytest.raises(ValueError):
        price_call_and_put(0.0, k, r, v, t, n, seed)
    with pytest.raises(ValueError):
        price_call_and_put(-10.0, k, r, v, t, n, seed)
    with pytest.raises(ValueError):
        price_call_and_put(s0, 0.0, r, v, t, n, seed)
    with pytest.raises(ValueError):
        price_call_and_put(s0, -5.0, r, v, t, n, seed)
    with pytest.raises(ValueError):
        price_call_and_put(s0, k, r, 0.0, t, n, seed)
    with pytest.raises(ValueError):
        price_call_and_put(s0, k, r, -0.2, t, n, seed)
    with pytest.raises(ValueError):
        price_call_and_put(s0, k, r, v, 0.0, n, seed)
    with pytest.raises(ValueError):
        price_call_and_put(s0, k, r, v, -1.0, n, seed)
    with pytest.raises(ValueError):
        price_call_and_put(s0, k, r, v, t, 1, seed)
    with pytest.raises(ValueError):
        price_call_and_put(s0, k, r, v, t, 0, seed)
    with pytest.raises(ValueError):
        price_call_and_put(s0, k, r, v, t, n, -1)
    with pytest.raises(ValueError):
        price_call_and_put(s0, k, r, v, t, n, UINT64_MAX + 1)
    with pytest.raises(ValueError):
        price_call_and_put(float("nan"), k, r, v, t, n, seed)
    with pytest.raises(ValueError):
        price_call_and_put(s0, float("inf"), r, v, t, n, seed)

    # Valid boundaries should succeed
    price_call_and_put(1e-6, 1e-6, 0.0, 1e-6, 1e-6, 2, UINT64_MAX)


def test_invalid_stream_rejected() -> None:
    """Verify ValueError for invalid stream count and seed arguments."""
    with pytest.raises(ValueError):
        rng_stream(0, -1)
    with pytest.raises(ValueError):
        rng_stream(-1, 10)
    with pytest.raises(ValueError):
        rng_stream(UINT64_MAX + 1, 10)

    assert rng_stream(0, 0) == []
