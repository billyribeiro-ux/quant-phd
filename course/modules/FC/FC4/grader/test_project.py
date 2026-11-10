"""Test suite for FC4 Investments & Equity Security Analysis autograded project."""

from __future__ import annotations

import os
from fractions import Fraction

import instance
import pytest
import valuation

SEED = int(os.environ.get("QF_SEED", "0"))
INST = instance.make_instance(SEED)


def _assert(condition: bool, concept: str, message: str) -> None:
    __tracebackhide__ = True
    if not condition:
        pytest.fail(f"[{concept}] {message}")


# --- Gordon Growth Model Tests ---


def test_t_gordon_value() -> None:
    """T-GORDON-VALUE: gordon_value matches direct closed-form formula D_1 / (r - g)."""
    d1 = INST["d1"]
    r = INST["r"]
    g = INST["g"]
    expected = d1 / (r - g)
    actual = valuation.gordon_value(d1, r, g)
    _assert(actual == expected, "gordon-growth-model", "Gordon value does not match D_1 / (r - g)")


def test_t_gordon_rg_equal() -> None:
    """T-GORDON-RG-EQUAL: r == g raises ValueError."""
    rate = Fraction(8, 100)
    with pytest.raises(ValueError, match=r".*"):
        valuation.gordon_value(Fraction(2), rate, rate)


def test_t_gordon_rg_below() -> None:
    """T-GORDON-RG-BELOW: r < g raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.gordon_value(Fraction(2), Fraction(4, 100), Fraction(5, 100))


def test_t_gordon_d1_neg() -> None:
    """T-GORDON-D1-NEG: negative d1 raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.gordon_value(Fraction(-1), Fraction(8, 100), Fraction(3, 100))


def test_t_gordon_d1_zero() -> None:
    """T-GORDON-D1-ZERO: d1 == 0 returns 0."""
    actual = valuation.gordon_value(Fraction(0), Fraction(8, 100), Fraction(3, 100))
    _assert(actual == Fraction(0), "gordon-growth-model", "Gordon value with zero dividend must be 0")


# --- Multistage Dividend Discount Model Tests ---


def test_t_ddm_n1() -> None:
    """T-DDM-N1: N = 1 horizon checked against direct single-step computation."""
    d1 = Fraction(3)
    r = Fraction(1, 10)
    g = Fraction(3, 100)
    # V0 = D1 / (1 + r) + (D1 * (1 + g) / (r - g)) / (1 + r)
    tv = (d1 * (Fraction(1) + g)) / (r - g)
    expected = (d1 + tv) / (Fraction(1) + r)
    actual = valuation.ddm_value((d1,), r, g)
    _assert(actual == expected, "dividend-discount-model", "N=1 DDM value mismatch")


def test_t_ddm_timing() -> None:
    """T-DDM-TIMING: discount exponents must be (1+r)^t, not (1+r)^(t-1)."""
    divs = (Fraction(2), Fraction(4))
    r = Fraction(1, 10)
    g = Fraction(2, 100)
    factor = Fraction(1) + r
    pv_explicit = divs[0] / factor + divs[1] / (factor**2)
    tv = (divs[1] * (Fraction(1) + g)) / (r - g)
    expected = pv_explicit + tv / (factor**2)

    # If discounted with beginning-of-year timing (factor^(t-1)), divs[0] would be discounted by 1
    wrong_pv = divs[0] + divs[1] / factor
    _assert(expected != wrong_pv, "dividend-discount-model", "Timing test fixture invalid")

    actual = valuation.ddm_value(divs, r, g)
    _assert(actual == expected, "dividend-discount-model", "DDM timing check failed: exponents must be (1+r)^t")


def test_t_ddm_terminal() -> None:
    """T-DDM-TERMINAL: terminal value uses D_N * (1 + g), not D_N without growth."""
    divs = (Fraction(3),)
    r = Fraction(1, 10)
    g = Fraction(4, 100)
    factor = Fraction(1) + r
    # Correct terminal value
    tv = (divs[0] * (Fraction(1) + g)) / (r - g)
    expected = (divs[0] + tv) / factor
    actual = valuation.ddm_value(divs, r, g)
    _assert(actual == expected, "dividend-discount-model", "Terminal value must grow D_N by (1 + g)")


def test_t_ddm_terminal_discount() -> None:
    """T-DDM-TERMINAL-DISCOUNT: terminal value must be discounted by (1+r)^N, not (1+r)^(N-1)."""
    divs = (Fraction(2), Fraction(3))
    r = Fraction(1, 10)
    g = Fraction(2, 100)
    factor = Fraction(1) + r
    tv = (divs[1] * (Fraction(1) + g)) / (r - g)
    expected = divs[0] / factor + divs[1] / (factor**2) + tv / (factor**2)
    actual = valuation.ddm_value(divs, r, g)
    _assert(actual == expected, "dividend-discount-model", "Terminal value must be discounted to date 0 by (1+r)^N")


def test_t_ddm_empty() -> None:
    """T-DDM-EMPTY: empty dividends sequence raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.ddm_value((), Fraction(1, 10), Fraction(2, 100))


def test_t_ddm_neg_div() -> None:
    """T-DDM-NEG-DIV: negative dividend raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.ddm_value((Fraction(2), Fraction(-1)), Fraction(1, 10), Fraction(2, 100))


def test_t_ddm_zero_div_accepted() -> None:
    """T-DDM-ZERO-DIV-ACCEPTED: zero dividend is allowed."""
    divs = (Fraction(0), Fraction(2))
    r = Fraction(1, 10)
    g = Fraction(2, 100)
    actual = valuation.ddm_value(divs, r, g)
    _assert(
        actual > Fraction(0),
        "dividend-discount-model",
        "Zero dividend followed by positive dividend must be valid",
    )


def test_t_ddm_rg_equal() -> None:
    """T-DDM-RG-EQUAL: r <= g raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.ddm_value((Fraction(2),), Fraction(5, 100), Fraction(5, 100))


def test_t_ddm_r_minus_one() -> None:
    """T-DDM-R-MINUS-ONE: r <= -1 raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.ddm_value((Fraction(2),), Fraction(-1), Fraction(-2))


def test_t_ddm_r_minus_one_plus() -> None:
    """T-DDM-R-MINUS-ONE-PLUS: r > -1 accepted when r > g."""
    val = valuation.ddm_value((Fraction(2),), Fraction(-5, 10), Fraction(-8, 10))
    _assert(val > Fraction(0), "dividend-discount-model", "Valid discount rate above -1 must evaluate")


# --- Free Cash Flow to Equity Tests ---


def test_t_fcfe_per_share() -> None:
    """T-FCFE-PER-SHARE: FCFE value per share computed correctly on instance."""
    fcfe = INST["fcfe"]
    shares = INST["shares"]
    r = INST["r"]
    g = INST["g"]

    factor = Fraction(1) + r
    pv = Fraction(0)
    disc = Fraction(1)
    for f in fcfe:
        disc *= factor
        pv += f / disc

    n = len(fcfe)
    tv = (fcfe[-1] * (Fraction(1) + g)) / (r - g)
    expected = (pv + tv / (factor**n)) / shares
    actual = valuation.fcfe_value_per_share(fcfe, shares, r, g)
    _assert(actual == expected, "free-cash-flow-to-equity", "FCFE value per share mismatch on instance")


def test_t_fcfe_terminal() -> None:
    """T-FCFE-TERMINAL: terminal value uses FCFE_N * (1 + g) once."""
    fcfe = (Fraction(5),)
    shares = Fraction(10)
    r = Fraction(1, 10)
    g = Fraction(3, 100)
    factor = Fraction(1) + r
    tv = (fcfe[0] * (Fraction(1) + g)) / (r - g)
    expected = (fcfe[0] / factor + tv / factor) / shares
    actual = valuation.fcfe_value_per_share(fcfe, shares, r, g)
    _assert(actual == expected, "free-cash-flow-to-equity", "FCFE terminal value must apply (1 + g) once")


def test_t_fcfe_neg_allowed() -> None:
    """T-FCFE-NEG-ALLOWED: negative FCFE values are permitted and do not raise."""
    fcfe = (Fraction(-2), Fraction(3))
    shares = Fraction(10)
    r = Fraction(1, 10)
    g = Fraction(2, 100)
    # Should not raise
    val = valuation.fcfe_value_per_share(fcfe, shares, r, g)
    _assert(isinstance(val, Fraction), "free-cash-flow-to-equity", "Negative FCFE must return a Fraction")


def test_t_fcfe_shares_zero() -> None:
    """T-FCFE-SHARES-ZERO: shares <= 0 raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.fcfe_value_per_share((Fraction(2),), Fraction(0), Fraction(1, 10), Fraction(2, 100))


def test_t_fcfe_shares_tiny() -> None:
    """T-FCFE-SHARES-TINY: positive tiny share count is accepted."""
    val = valuation.fcfe_value_per_share((Fraction(2),), Fraction(1, 1000), Fraction(1, 10), Fraction(2, 100))
    _assert(val > Fraction(0), "free-cash-flow-to-equity", "Tiny positive share count must evaluate")


def test_t_fcfe_empty() -> None:
    """T-FCFE-EMPTY: empty FCFE sequence raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.fcfe_value_per_share((), Fraction(100), Fraction(1, 10), Fraction(2, 100))


def test_t_fcfe_rg() -> None:
    """T-FCFE-RG: r <= g raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.fcfe_value_per_share((Fraction(2),), Fraction(100), Fraction(5, 100), Fraction(5, 100))


def test_t_fcfe_r_minus_one() -> None:
    """T-FCFE-R-MINUS-ONE: r <= -1 raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.fcfe_value_per_share((Fraction(2),), Fraction(100), Fraction(-1), Fraction(-2))


# --- Residual Income Valuation Model Tests ---


def test_t_ri_clean_surplus_identity() -> None:
    """T-RI-CLEAN-SURPLUS-IDENTITY: RI equity value equals DDM + discounted terminal book value."""
    b0 = Fraction(100)
    earnings = (Fraction(15), Fraction(18), Fraction(22))
    dividends = (Fraction(5), Fraction(6), Fraction(8))
    r = Fraction(1, 10)
    factor = Fraction(1) + r

    # Compute DDM sum + B_N discounted
    b = b0
    pv_d = Fraction(0)
    disc = Fraction(1)
    for ni, d in zip(earnings, dividends, strict=True):
        disc *= factor
        pv_d += d / disc
        b = b + ni - d
    b_n = b
    n = len(earnings)
    expected_identity_value = pv_d + b_n / (factor**n)

    actual_ri = valuation.residual_income_value(b0, earnings, dividends, r)
    _assert(
        actual_ri == expected_identity_value,
        "residual-income-valuation-model",
        "Clean-surplus identity failed: RI value must equal DDM value + discounted terminal book value",
    )


def test_t_ri_charge() -> None:
    """T-RI-CHARGE: cost of equity is charged on beginning book B_{t-1}, not ending B_t."""
    b0 = Fraction(100)
    earnings = (Fraction(20),)
    dividends = (Fraction(5),)
    r = Fraction(1, 10)
    # Beginning book is 100, so charge is r * 100 = 10, RI_1 = 20 - 10 = 10
    # Ending book is 100 + 20 - 5 = 115; if charged on ending book, charge would be 11.5, RI_1 = 8.5
    expected = b0 + Fraction(10) / (Fraction(1) + r)
    actual = valuation.residual_income_value(b0, earnings, dividends, r)
    _assert(actual == expected, "residual-income-valuation-model", "RI charge must be on beginning book B_{t-1}")


def test_t_ri_length() -> None:
    """T-RI-LENGTH: earnings and dividends of different lengths raise ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.residual_income_value(Fraction(100), (Fraction(10), Fraction(12)), (Fraction(5),), Fraction(1, 10))


def test_t_ri_empty() -> None:
    """T-RI-EMPTY: empty earnings raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.residual_income_value(Fraction(100), (), (), Fraction(1, 10))


def test_t_ri_r_minus_one() -> None:
    """T-RI-R-MINUS-ONE: r <= -1 raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.residual_income_value(Fraction(100), (Fraction(10),), (Fraction(5),), Fraction(-1))


# --- Scenario-Weighted Price Target Tests ---


def test_t_price_tie() -> None:
    """T-PRICE-TIE: exact half-cent tie 2.5 cents rounds half-up to 3 cents (kills round-half-to-even)."""
    # 2 cents with prob 1/2, 3 cents with prob 1/2 -> expected 2.5 cents -> half-up rounds to 3
    scenarios = ((Fraction(1, 2), 2), (Fraction(1, 2), 3))
    actual = valuation.scenario_price_target_cents(scenarios)
    _assert(actual == 3, "scenario-weighted-price-target", "Half-cent tie 2.5 must round to 3 cents, not 2")


def test_t_price_half_up_nontie() -> None:
    """T-PRICE-HALF-UP-NONTIE: non-tie values round to nearest whole cent."""
    # 2 cents with prob 1/4, 3 cents with prob 3/4 -> 2.75 cents -> 3 cents
    scenarios1 = ((Fraction(1, 4), 2), (Fraction(3, 4), 3))
    _assert(
        valuation.scenario_price_target_cents(scenarios1) == 3,
        "scenario-weighted-price-target",
        "2.75 rounds to 3",
    )

    # 2 cents with prob 3/4, 3 cents with prob 1/4 -> 2.25 cents -> 2 cents
    scenarios2 = ((Fraction(3, 4), 2), (Fraction(1, 4), 3))
    _assert(
        valuation.scenario_price_target_cents(scenarios2) == 2,
        "scenario-weighted-price-target",
        "2.25 rounds to 2",
    )


def test_t_price_sum_exact() -> None:
    """T-PRICE-SUM-EXACT: probability sum exceeding 1 even by 10^-12 raises ValueError."""
    eps = Fraction(1, 10**12)
    scenarios = ((Fraction(1, 2) + eps, 100), (Fraction(1, 2), 200))
    with pytest.raises(ValueError, match=r".*"):
        valuation.scenario_price_target_cents(scenarios)


def test_t_price_sum_short() -> None:
    """T-PRICE-SUM-SHORT: probability sum less than 1 raises ValueError."""
    scenarios = ((Fraction(4, 10), 100), (Fraction(5, 10), 200))
    with pytest.raises(ValueError, match=r".*"):
        valuation.scenario_price_target_cents(scenarios)


def test_t_price_neg_prob() -> None:
    """T-PRICE-NEG-PROB: negative probability raises ValueError."""
    scenarios = ((Fraction(-1, 10), 100), (Fraction(11, 10), 200))
    with pytest.raises(ValueError, match=r".*"):
        valuation.scenario_price_target_cents(scenarios)


def test_t_price_zero_prob_accepted() -> None:
    """T-PRICE-ZERO-PROB-ACCEPTED: zero probability scenario is accepted."""
    scenarios = ((Fraction(0), 100), (Fraction(1), 250))
    actual = valuation.scenario_price_target_cents(scenarios)
    _assert(actual == 250, "scenario-weighted-price-target", "Zero probability scenario must be accepted")


def test_t_price_empty() -> None:
    """T-PRICE-EMPTY: empty scenarios sequence raises ValueError."""
    with pytest.raises(ValueError, match=r".*"):
        valuation.scenario_price_target_cents(())


def test_t_price_neg_value() -> None:
    """T-PRICE-NEG-VALUE: negative scenario value raises ValueError."""
    scenarios = ((Fraction(1), -50),)
    with pytest.raises(ValueError, match=r".*"):
        valuation.scenario_price_target_cents(scenarios)


def test_t_price_zero_value_accepted() -> None:
    """T-PRICE-ZERO-VALUE-ACCEPTED: zero scenario value is accepted."""
    scenarios = ((Fraction(1), 0),)
    _assert(
        valuation.scenario_price_target_cents(scenarios) == 0,
        "scenario-weighted-price-target",
        "Zero value must return 0",
    )


# --- Instance & Hardcode Guard Tests ---


def test_t_instance_valid() -> None:
    """T-INSTANCE-VALID: verify instance constraints on current seed."""
    r = INST["r"]
    g = INST["g"]
    _assert(r - g >= Fraction(30, 1000), "instance", "Instance spread r - g must be >= 0.030")
    _assert(INST["shares"] >= 1000, "instance", "Instance shares count must be >= 1000")
    total_p = sum(p for p, _ in INST["scenarios"])
    _assert(total_p == Fraction(1), "instance", "Instance probabilities must sum to 1")


def test_t_seed_hardcode_guard() -> None:
    """T-SEED-HARDCODE-GUARD: guards against hardcoding seed 0 values."""
    inst_current = instance.make_instance(SEED)
    target_current = valuation.scenario_price_target_cents(inst_current["scenarios"])

    # If test is run on another seed whose scenarios differ, target must match inst_current, not seed 0 literal
    inst_0 = instance.make_instance(0)
    target_0 = valuation.scenario_price_target_cents(inst_0["scenarios"])
    if SEED != 0 and inst_current["scenarios"] != inst_0["scenarios"]:
        _assert(
            target_current != target_0 or inst_current["scenarios"] == inst_0["scenarios"],
            "instance",
            "Guard against hardcoding seed 0",
        )
