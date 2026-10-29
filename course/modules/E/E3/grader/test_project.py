"""Acceptance suite for the E3 project: the preference-elicitation engine (elicit.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your elicit.py next to this file. Warnings are failures, as in the browser.

Every expected value below is recomputed here from the definitions in the project specification, by oracle functions
written for this suite (not by elicit.py). The participant is SIMULATED: the answers come from instance.py for the seed.
A failing check names the property it tests and the idea to revisit. It never prints the expected value.
"""

from __future__ import annotations

import ast
import functools
import json
import math
import os
import sys
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import elicit as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
INST2 = make_instance(SEED + 7_919)  # a second participant, so a fixed answer for one seed must also match another
TRUE = {"gamma": float(INST["gamma"]), "lambda": float(INST["lambda"]), "kappa": float(INST["kappa"])}
WEALTH: int = int(INST["wealth_cents"])
RESPONSES: list[dict[str, Any]] = json.loads(str(INST["responses_json"]))
ONE_CENT = 0.5  # the nearest-cent rule moves any exact amount by at most half a cent
TOL = 1e-6


def expect(ok: bool, hint: str) -> None:
    """Fail with a hint that names the property. The message carries no values."""
    __tracebackhide__ = True
    if not ok:
        pytest.fail(hint, pytrace=False)


def must_raise(call: Callable[[], object], condition: str, *, contains: tuple[str, ...] = ()) -> None:
    """Fail unless call() raises ValueError (the named conditions of the specification). Each text in ``contains`` must
    appear in the message; the page quotes a message only where it names one."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError as err:
        for text in contains:
            expect(text in str(err), f"{condition}: the ValueError message must contain the required text")
        return
    except Exception:  # any other exception type is a failure for a named condition
        pytest.fail(f"{condition}: the specification requires ValueError for this input", pytrace=False)
    pytest.fail(f"{condition}: the specification requires a ValueError, and none was raised", pytrace=False)


def nearest(x: Fraction) -> int:
    """The test's own nearest-cent rule for an exact amount: an exact half goes up, floor(x + 1/2)."""
    return math.floor(x + Fraction(1, 2))


def parse(response: dict[str, Any]) -> tuple[list[int], list[Fraction], list[int], list[Fraction], str]:
    """A response's two lotteries with exact probabilities, and the chosen alternative."""
    pa = [int(x) for x in response["prizes_a"]]
    qa = [Fraction(str(s)) for s in response["probs_a"]]
    pb = [int(x) for x in response["prizes_b"]]
    qb = [Fraction(str(s)) for s in response["probs_b"]]
    return pa, qa, pb, qb, str(response["choice"])


PARSED = [parse(r) for r in RESPONSES]


# ---------------------------------------------------------------------------------------------------------------------
# Oracles: independent float implementations of the specification's formulas (unrounded, in cents).
# ---------------------------------------------------------------------------------------------------------------------


def oracle_value(x: int, gamma: float, lam: float) -> float:
    """Prospect value of a change x from the reference point 0: x^(1-gamma) for gains, -lam(-x)^(1-gamma) for losses."""
    if x >= 0:
        return math.pow(float(x), 1.0 - gamma)
    return -lam * math.pow(float(-x), 1.0 - gamma)


def oracle_prospect(prizes: list[int], probs: list[Fraction], gamma: float, lam: float) -> float:
    """The prospect certainty equivalent: the sure change whose value equals the lottery's value, unrounded."""
    total = sum(float(p) * oracle_value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    if total >= 0.0:
        return math.pow(total, 1.0 / (1.0 - gamma))
    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))


def oracle_crra(prizes: list[int], probs: list[Fraction], gamma: float, wealth: int) -> float:
    """The CRRA certainty equivalent as a change from wealth: the sure amount whose utility of final wealth equals the
    lottery's expected utility, unrounded. At gamma = 1 the utility is ln, and the limit form is used."""
    finals = [wealth + x for x in prizes]
    if gamma == 1.0:
        return math.exp(sum(float(p) * math.log(w) for p, w in zip(probs, finals, strict=True))) - wealth
    expected = sum(float(p) * math.pow(float(w), 1.0 - gamma) for p, w in zip(probs, finals, strict=True))
    return math.pow(expected, 1.0 / (1.0 - gamma)) - wealth


def oracle_loglik(parsed: list[tuple[Any, ...]], gamma: float, lam: float, kappa: float) -> float:
    """The logit log-likelihood: each response contributes log P(chosen), where P(A) = 1/(1 + exp(-z)) and
    z = kappa (CE_A - CE_B) / 10000 (cents to units of $100). A response that chose B contributes log(1 - P(A))."""
    total = 0.0
    for pa, qa, pb, qb, choice in parsed:
        z = kappa * (oracle_prospect(pa, qa, gamma, lam) - oracle_prospect(pb, qb, gamma, lam)) / 10_000.0
        # log P(A) = -log(1 + exp(-z)) and log(1 - P(A)) = -log(1 + exp(z)): the stable forms, since 1 - P(A) cancels
        total += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
    return total


def mixed(prizes: list[int], probs: list[Fraction]) -> bool:
    """A lottery mixes gains and losses when it has a gain and a loss, each with positive probability."""
    gains = any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    losses = any(x < 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    return gains and losses


@functools.cache
def est() -> dict[str, float]:
    """The estimate for this participant, computed once per run."""
    result: dict[str, float] = sol.estimate(RESPONSES)
    return result


# ---------------------------------------------------------------------------------------------------------------------
# certainty_equivalent_cents
# ---------------------------------------------------------------------------------------------------------------------


def test_crra_gamma_zero_is_expected_final_wealth_exactly() -> None:
    """Risk neutrality at gamma = 0: the certainty equivalent is the expected prize, to the cent, exactly."""
    for pa, qa, _, _, _ in PARSED[:40]:
        got = sol.certainty_equivalent_cents("crra", pa, qa, {"gamma": 0.0}, WEALTH)
        expected_change = sum((p * x for p, x in zip(qa, pa, strict=True)), Fraction(0))
        expect(got == nearest(expected_change), "at gamma = 0 the CRRA certainty equivalent is the expected prize")


def test_crra_within_half_cent_of_oracle_for_instance_lotteries() -> None:
    """The instance keeps every CRRA value clear of a half cent, so the rounded integer is fixed: it must equal the
    oracle's rounding, and it must be an int."""
    for pa, qa, _, _, _ in PARSED[:40]:
        got = sol.certainty_equivalent_cents("crra", pa, qa, {"gamma": TRUE["gamma"]}, WEALTH)
        expect(type(got) is int, "every certainty equivalent must be returned as an int number of cents")
        expect(
            got == math.floor(oracle_crra(pa, qa, TRUE["gamma"], WEALTH) + 0.5),
            "the CRRA certainty equivalent must be the expected-utility sure amount, rounded half up",
        )


def test_crra_log_case_matches_the_limit_gamma_to_one() -> None:
    """At gamma = 1 the utility is ln W. The oracle's power form at gamma = 1 - 1e-6 must agree with the log form to
    0.01 cent plus 1e-5 relative, and the integer answer at gamma = 1 must be within half a cent of the log form."""
    for pa, qa, _, _, _ in PARSED[:20]:
        log_form = oracle_crra(pa, qa, 1.0, WEALTH)
        near_limit = oracle_crra(pa, qa, 1.0 - 1e-6, WEALTH)
        expect(
            abs(near_limit - log_form) <= 0.01 + 1e-5 * abs(log_form),
            "the power form must converge to the log form as gamma tends to 1",
        )
        got = sol.certainty_equivalent_cents("crra", pa, qa, {"gamma": 1.0}, WEALTH)
        expect(type(got) is int, "every certainty equivalent must be returned as an int number of cents")
        expect(
            abs(got - log_form) <= ONE_CENT + TOL,
            "at gamma = 1 the answer must be the log-utility certainty equivalent",
        )


def test_crra_risk_aversion_lowers_the_certainty_equivalent() -> None:
    """For gamma > 0 a risky lottery is worth less than its expected prize: the certainty equivalent is at most the
    rounded expected prize, and for a lottery with a large spread it is at least a dollar below it."""
    for pa, qa, _, _, _ in PARSED[:40]:
        got = sol.certainty_equivalent_cents("crra", pa, qa, {"gamma": TRUE["gamma"]}, WEALTH)
        expected_change = sum((p * x for p, x in zip(qa, pa, strict=True)), Fraction(0))
        expect(got <= nearest(expected_change), "risk aversion must not raise the certainty equivalent above E[prize]")
    prizes, probs = [0, 40_000], [Fraction(1, 2), Fraction(1, 2)]
    got = sol.certainty_equivalent_cents("crra", prizes, probs, {"gamma": TRUE["gamma"]}, 100_000)
    exact_expected = 20_000
    expect(
        got <= exact_expected - 100,
        "a 50-50 lottery of $0 or $400 with curvature must be worth at least $1 less than its expected prize",
    )
    expect(
        abs(got - oracle_crra(prizes, probs, TRUE["gamma"], 100_000)) <= ONE_CENT + TOL,
        "the risky lottery's CRRA certainty equivalent must match the expected-utility sure amount",
    )


def test_crra_homogeneity_scales_wealth_and_prizes_together() -> None:
    """Scaling wealth and every prize by the same whole number k scales the certainty equivalent by k."""
    for k in (2, 3, 5):
        for pa, qa, _, _, _ in PARSED[:10]:
            base = oracle_crra(pa, qa, TRUE["gamma"], WEALTH)
            got = sol.certainty_equivalent_cents("crra", [k * x for x in pa], qa, {"gamma": TRUE["gamma"]}, k * WEALTH)
            expect(
                abs(got - k * base) <= ONE_CENT + TOL,
                "the CRRA certainty equivalent must be homogeneous of degree one in (wealth, prizes)",
            )


def test_prospect_matches_oracle_for_instance_lotteries() -> None:
    """The instance keeps every prospect value clear of a half cent: the integer is fixed by the oracle."""
    for pa, qa, _, _, _ in PARSED[:40]:
        got = sol.certainty_equivalent_cents("prospect", pa, qa, TRUE, WEALTH)
        expect(type(got) is int, "every certainty equivalent must be returned as an int number of cents")
        expect(
            got == math.floor(oracle_prospect(pa, qa, TRUE["gamma"], TRUE["lambda"]) + 0.5),
            "the prospect certainty equivalent must be the sure change whose value equals the lottery's value",
        )


def test_prospect_sure_amount_has_the_lottery_value_to_the_cent() -> None:
    """The rounded answer c lies within half a cent of the exact sure amount, and the value is increasing, so the
    lottery's value must lie between the values of c - 1/2 and c + 1/2."""
    gamma, lam = TRUE["gamma"], TRUE["lambda"]
    for pa, qa, _, _, _ in PARSED[:40]:
        got = sol.certainty_equivalent_cents("prospect", pa, qa, TRUE, WEALTH)
        lottery_value = sum(float(p) * oracle_value(x, gamma, lam) for x, p in zip(pa, qa, strict=True))
        at_low = oracle_value_at(got - ONE_CENT, gamma, lam)
        at_high = oracle_value_at(got + ONE_CENT, gamma, lam)
        slack = 1e-9 * (1.0 + abs(lottery_value))
        expect(
            min(at_low, at_high) - slack <= lottery_value <= max(at_low, at_high) + slack,
            "the prospect certainty equivalent must return the sure amount whose value equals the lottery's value",
        )


def oracle_value_at(c: float, gamma: float, lam: float) -> float:
    """The prospect value of a sure change c, for a real c (zero at zero)."""
    if c >= 0:
        return math.pow(c, 1.0 - gamma)
    return -lam * math.pow(-c, 1.0 - gamma)


def test_loss_aversion_weights_losses_not_gains() -> None:
    """Exact case at gamma = 0. With lambda = 2, v(x) = x for gains and v(x) = 2x for losses. The lottery of -100 and
    +100, each with probability 1/2, has value 0.5 * (-200) + 0.5 * 100 = -50, and its sure amount is -50 / 2 = -25.
    With lambda = 1/2 the value is +25 and the sure amount is +25."""
    got = sol.certainty_equivalent_cents(
        "prospect", [-100, 100], [Fraction(1, 2), Fraction(1, 2)], {"gamma": 0.0, "lambda": 2.0}, WEALTH
    )
    expect(got == -25, "with lambda = 2 a loss weighs twice a gain: the sure amount of this lottery is -25 cents")
    got_mirror = sol.certainty_equivalent_cents(
        "prospect", [-100, 100], [Fraction(1, 2), Fraction(1, 2)], {"gamma": 0.0, "lambda": 0.5}, WEALTH
    )
    expect(got_mirror == 25, "with lambda = 1/2 the same lottery's sure amount is +25 cents: the loss weight is lambda")


def test_half_cent_goes_up_on_exact_halves() -> None:
    """An exact half cent goes toward plus infinity in both models. A rule that rounds halves to even fails."""
    half, wealth = Fraction(1, 2), 10
    got_up = sol.certainty_equivalent_cents("prospect", [2, 3], [half, half], {"gamma": 0.0, "lambda": 1.0}, WEALTH)
    expect(got_up == 3, "a sure amount of 2.5 cents must round half up to 3")
    got_up_low = sol.certainty_equivalent_cents("prospect", [0, 1], [half, half], {"gamma": 0.0, "lambda": 1.0}, WEALTH)
    expect(got_up_low == 1, "a sure amount of 0.5 cents must round half up to 1")
    got_neg = sol.certainty_equivalent_cents("prospect", [-1, 0], [half, half], {"gamma": 0.0, "lambda": 1.0}, WEALTH)
    expect(got_neg == 0, "a sure amount of -0.5 cents must round half up to 0")
    got_crra = sol.certainty_equivalent_cents("crra", [2, 3], [half, half], {"gamma": 0.0}, wealth)
    expect(got_crra == 3, "the CRRA certainty equivalent at gamma = 0 must round a 2.5-cent amount half up to 3")


def test_prizes_order_does_not_change_the_answer() -> None:
    """A lottery is the same lottery when its (prize, probability) pairs are listed in another order."""
    for pa, qa, _, _, _ in PARSED[:30]:
        forward = sol.certainty_equivalent_cents("prospect", pa, qa, TRUE, WEALTH)
        backward = sol.certainty_equivalent_cents("prospect", pa[::-1], qa[::-1], TRUE, WEALTH)
        expect(forward == backward, "the certainty equivalent must not depend on the order of the listed outcomes")
        crra_fwd = sol.certainty_equivalent_cents("crra", pa, qa, {"gamma": TRUE["gamma"]}, WEALTH)
        crra_bwd = sol.certainty_equivalent_cents("crra", pa[::-1], qa[::-1], {"gamma": TRUE["gamma"]}, WEALTH)
        expect(
            crra_fwd == crra_bwd, "the CRRA certainty equivalent must not depend on the order of the listed outcomes"
        )


def test_model_name_must_be_crra_or_prospect() -> None:
    """Only the two names are valid, and the message names them. Each invalid name is a ValueError."""
    pa, qa = [100], [Fraction(1)]
    for name in ("crra", "prospect"):
        got = sol.certainty_equivalent_cents(name, pa, qa, {"gamma": 0.5, "lambda": 2.0}, WEALTH)
        expect(type(got) is int, "a valid model name must return an int number of cents")
    for name in ("CRRA", "expected", "", " prospect"):
        must_raise(
            lambda n=name: sol.certainty_equivalent_cents(n, pa, qa, {"gamma": 0.5, "lambda": 2.0}, WEALTH),  # type: ignore[misc]
            f"model {name!r} is not one of the allowed names",
            contains=("crra", "prospect"),
        )


def test_probabilities_must_be_nonnegative_and_sum_to_exactly_one() -> None:
    """Boundary cases: a probability of exactly zero is allowed; a sum one part in a thousand off is not; a sum one
    part in ten trillion above 1 is not (the test is exact, not a tolerance); a negative probability is not."""
    got_zero = sol.certainty_equivalent_cents(
        "prospect", [100, 500], [Fraction(0), Fraction(1)], {"gamma": 0.0, "lambda": 1.0}, WEALTH
    )
    expect(got_zero == 500, "a zero probability is allowed, and the lottery is then its one remaining prize")
    third = Fraction(1, 3)
    got_exact = sol.certainty_equivalent_cents(
        "prospect", [100, 500], [third, 1 - third], {"gamma": 0.0, "lambda": 1.0}, WEALTH
    )
    expect(got_exact == 367, "probabilities that sum to exactly 1 must be accepted")
    must_raise(
        lambda: sol.certainty_equivalent_cents(
            "prospect", [100, 500], [third, Fraction(2, 3) - Fraction(1, 1000)], {"gamma": 0.0, "lambda": 1.0}, WEALTH
        ),
        "probabilities that sum to one part in a thousand below 1",
        contains=("probabilities must sum to 1",),
    )
    must_raise(
        lambda: sol.certainty_equivalent_cents(
            "prospect", [100, 500], [third + Fraction(1, 1000), Fraction(2, 3)], {"gamma": 0.0, "lambda": 1.0}, WEALTH
        ),
        "probabilities that sum to one part in a thousand above 1",
        contains=("probabilities must sum to 1",),
    )
    must_raise(
        lambda: sol.certainty_equivalent_cents(
            "prospect", [100, 500], [Fraction(-1, 4), Fraction(5, 4)], {"gamma": 0.0, "lambda": 1.0}, WEALTH
        ),
        "a negative probability",
        contains=("probabilities must sum to 1",),
    )
    must_raise(
        lambda: sol.certainty_equivalent_cents(
            "prospect",
            [100, 500],
            [Fraction(1, 2), Fraction(1, 2) + Fraction(1, 10**13)],
            {"gamma": 0.0, "lambda": 1.0},
            WEALTH,
        ),
        "probabilities that sum to one part in ten trillion above 1",
        contains=("probabilities must sum to 1",),
    )


def test_crra_requires_wealth_plus_every_prize_to_stay_positive() -> None:
    """Boundary cases for final wealth W + x: exactly 1 cent is allowed; exactly 0 and -1 cents are not. The prospect
    model does not use wealth, so it accepts any wealth."""
    got_one = sol.certainty_equivalent_cents("crra", [-999], [Fraction(1)], {"gamma": 0.5}, 1000)
    expect(got_one == -999, "final wealth of one cent is positive and must be accepted")
    must_raise(
        lambda: sol.certainty_equivalent_cents("crra", [-1000], [Fraction(1)], {"gamma": 0.5}, 1000),
        "final wealth exactly zero",
        contains=("wealth plus prize must stay positive",),
    )
    must_raise(
        lambda: sol.certainty_equivalent_cents("crra", [-1001], [Fraction(1)], {"gamma": 0.5}, 1000),
        "final wealth below zero",
        contains=("wealth plus prize must stay positive",),
    )
    must_raise(
        lambda: sol.certainty_equivalent_cents(
            "crra", [100, -2000], [Fraction(1, 2), Fraction(1, 2)], {"gamma": 0.5}, 1000
        ),
        "one prize of a two-prize lottery takes final wealth below zero",
        contains=("wealth plus prize must stay positive",),
    )
    got_prospect = sol.certainty_equivalent_cents("prospect", [-5000], [Fraction(1)], {"gamma": 0.5, "lambda": 2.0}, 0)
    expect(got_prospect == -5000, "the prospect model must not use wealth, so a zero wealth is not an error")


def test_wrong_types_never_return_money_as_a_float() -> None:
    """Inputs of the wrong type may raise any exception. If one returns, the result must be an int."""
    wrong_inputs: list[Callable[[], object]] = [
        lambda: sol.certainty_equivalent_cents("crra", [100.0], [Fraction(1)], {"gamma": 0.5}, WEALTH),
        lambda: sol.certainty_equivalent_cents("prospect", [100], [0.5, 0.5], {"gamma": 0.0, "lambda": 1.0}, WEALTH),
        lambda: sol.certainty_equivalent_cents("crra", [100], [Fraction(1)], {"gamma": 0.5}, 1000.0),
    ]
    for call in wrong_inputs:
        try:
            out = call()
        except Exception:  # any exception is allowed for an input of the wrong type
            continue
        expect(type(out) is int, "a money output must be an int number of cents, never a float")


# ---------------------------------------------------------------------------------------------------------------------
# log_likelihood
# ---------------------------------------------------------------------------------------------------------------------


def test_log_likelihood_matches_oracle_at_the_true_parameters() -> None:
    """The likelihood at the parameters that generated the answers equals the oracle's, term by term."""
    got = sol.log_likelihood(RESPONSES, TRUE)
    expected = oracle_loglik(PARSED, TRUE["gamma"], TRUE["lambda"], TRUE["kappa"])
    expect(abs(got - expected) <= 1e-9 * max(1.0, abs(expected)), "the logit log-likelihood does not match the oracle")


def test_log_likelihood_is_a_sum_of_log_probabilities() -> None:
    """Each term is the log of a probability, so the total is at most zero. A response that chose B contributes
    log(1 - P(A)), the log-probability of B."""
    got = sol.log_likelihood(RESPONSES, TRUE)
    expect(got <= 0.0, "a log-likelihood of choice probabilities cannot be positive")
    one_only = [RESPONSES[0] | {"choice": "A"}]
    other = [RESPONSES[0] | {"choice": "B"}]
    p_a = 1.0 / (
        1.0
        + math.exp(
            -TRUE["kappa"]
            * (
                oracle_prospect(*PARSED[0][:2], TRUE["gamma"], TRUE["lambda"])
                - oracle_prospect(*PARSED[0][2:4], TRUE["gamma"], TRUE["lambda"])
            )
            / 10_000.0
        )
    )
    expect(
        abs(sol.log_likelihood(one_only, TRUE) - math.log(p_a)) <= 1e-9,
        "a response that chose A must contribute the log of the choice probability P(A)",
    )
    expect(
        abs(sol.log_likelihood(other, TRUE) - math.log(1.0 - p_a)) <= 1e-9,
        "a response that chose B must contribute log(1 - P(A)), the log-probability of B",
    )


# ---------------------------------------------------------------------------------------------------------------------
# estimate
# ---------------------------------------------------------------------------------------------------------------------


def test_estimate_returns_the_named_fields_as_finite_floats() -> None:
    """The keys of the result are the specified ones, and every value is a finite float."""
    expected_keys = {"gamma_hat", "lambda_hat", "kappa_hat", "se_gamma", "se_lambda", "se_kappa", "log_likelihood"}
    expect(set(est()) == expected_keys, "estimate must return exactly the seven named fields")
    expect(all(isinstance(v, float) and math.isfinite(v) for v in est().values()), "every field must be a finite float")


def test_estimates_lie_in_their_domains() -> None:
    """Domain: 0 < gamma < 1, lambda > 0, kappa > 0 (the bounds the specification states for the prospect model)."""
    expect(0.0 < est()["gamma_hat"] < 1.0, "the curvature estimate must lie in (0, 1)")
    expect(est()["lambda_hat"] > 0.0, "the loss-aversion estimate must be positive")
    expect(est()["kappa_hat"] > 0.0, "the choice-precision estimate must be positive")


def test_standard_errors_are_positive_and_finite() -> None:
    """Standard errors from the observed information are positive and finite."""
    for key in ("se_gamma", "se_lambda", "se_kappa"):
        expect(est()[key] > 0.0 and math.isfinite(est()[key]), "each standard error must be positive and finite")


def test_reported_log_likelihood_is_the_likelihood_at_the_estimate() -> None:
    """The log_likelihood field is the likelihood evaluated at the estimate."""
    at = oracle_loglik(PARSED, est()["gamma_hat"], est()["lambda_hat"], est()["kappa_hat"])
    expect(
        abs(est()["log_likelihood"] - at) <= 1e-7 * max(1.0, abs(at)), "the reported likelihood is not at the estimate"
    )


def test_score_is_zero_at_the_estimate() -> None:
    """At an interior maximum the score is zero. Derivatives are taken by central differences in the coordinates
    eta = log(gamma/(1-gamma)), log(lambda) and log(kappa), where the estimate is interior. The log-likelihood has kinks
    (the certainty equivalent changes form where a lottery's value changes sign), and at a kink a central difference
    depends on its step, so the score is computed at steps 1e-5 and 1e-6 and the smaller largest component counts. It
    must be below 2e-5 in absolute value, a tolerance of this suite stated on the page; a search that stops while a
    component is still of order 1e-4 or more has not reached the stationary point."""
    gamma, lam, kappa = est()["gamma_hat"], est()["lambda_hat"], est()["kappa_hat"]
    theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]

    def ll(t: list[float]) -> float:
        return oracle_loglik(PARSED, 1.0 / (1.0 + math.exp(-t[0])), math.exp(t[1]), math.exp(t[2]))

    def largest_component(step: float) -> float:
        worst = 0.0
        for i in range(3):
            up, down = list(theta), list(theta)
            up[i] += step
            down[i] -= step
            worst = max(worst, abs((ll(up) - ll(down)) / (2 * step)))
        return worst

    expect(
        min(largest_component(1e-5), largest_component(1e-6)) <= 2e-5,
        "the score is not zero at the estimate: the estimate is not a stationary point of the likelihood",
    )


def test_estimate_is_a_local_maximum() -> None:
    """Moving any parameter a little, in either direction, does not raise the likelihood."""
    gamma, lam, kappa = est()["gamma_hat"], est()["lambda_hat"], est()["kappa_hat"]
    here = oracle_loglik(PARSED, gamma, lam, kappa)
    for step in (1e-3, -1e-3):
        moved = [
            oracle_loglik(PARSED, gamma * (1 + step), lam, kappa),
            oracle_loglik(PARSED, gamma, lam * (1 + step), kappa),
            oracle_loglik(PARSED, gamma, lam, kappa * (1 + step)),
        ]
        for value in moved:
            expect(value <= here + 1e-9, "a nearby parameter has a higher likelihood: the estimate is not the maximum")


def test_estimate_recovers_the_true_parameters_within_five_standard_errors() -> None:
    """Each estimate lies within five of its own standard errors of the parameter that generated the answers. Five is
    this suite's tolerance, stated on the project page; it is not a claim about the coverage of the standard errors."""
    for name, key, se in (
        ("gamma", "gamma_hat", "se_gamma"),
        ("lambda", "lambda_hat", "se_lambda"),
        ("kappa", "kappa_hat", "se_kappa"),
    ):
        expect(
            abs(est()[key] - TRUE[name]) <= 5.0 * est()[se],
            f"the estimate of {name} is more than five standard errors from the true value: check the likelihood",
        )


def test_estimate_on_a_second_participant_is_also_a_maximum() -> None:
    """A second SIMULATED participant (another seed): the same two properties hold on it."""
    parsed2 = [parse(r) for r in json.loads(str(INST2["responses_json"]))]
    est2 = sol.estimate(json.loads(str(INST2["responses_json"])))
    gamma, lam, kappa = est2["gamma_hat"], est2["lambda_hat"], est2["kappa_hat"]
    here = oracle_loglik(parsed2, gamma, lam, kappa)
    expect(
        abs(est2["log_likelihood"] - here) <= 1e-7 * max(1.0, abs(here)),
        "the reported likelihood on the second participant is not at its estimate",
    )
    for key in ("se_gamma", "se_lambda", "se_kappa"):
        expect(est2[key] > 0.0 and math.isfinite(est2[key]), "standard errors must be positive and finite")
    expect(oracle_loglik(parsed2, gamma * 1.001, lam, kappa) <= here + 1e-9, "the second estimate is not a maximum")


def test_estimate_needs_responses() -> None:
    """Named condition: an empty set of responses cannot identify anything."""
    must_raise(lambda: sol.estimate([]), "no responses")


def test_estimate_needs_a_mixed_sign_lottery() -> None:
    """Named condition: loss aversion is identified only by a lottery with a gain and a loss, each with positive
    probability. Pure lotteries alone are refused; a loss with probability zero does not count as a loss."""
    pure = [
        {
            "pair_id": 0,
            "choice": "A",
            "prizes_a": [100, 300],
            "probs_a": ["1/4", "3/4"],
            "prizes_b": [200],
            "probs_b": ["1"],
        },
        {
            "pair_id": 1,
            "choice": "B",
            "prizes_a": [500],
            "probs_a": ["1"],
            "prizes_b": [50, 900],
            "probs_b": ["1/2", "1/2"],
        },
    ]
    must_raise(lambda: sol.estimate(pure), "responses with only pure-gain lotteries")
    zero_loss = [
        {
            "pair_id": 0,
            "choice": "A",
            "prizes_a": [-100, 300],
            "probs_a": ["0", "1"],
            "prizes_b": [200],
            "probs_b": ["1"],
        },
        {
            "pair_id": 1,
            "choice": "B",
            "prizes_a": [500],
            "probs_a": ["1"],
            "prizes_b": [50, 900],
            "probs_b": ["1/2", "1/2"],
        },
    ]
    must_raise(lambda: sol.estimate(zero_loss), "a loss with probability zero is not a loss")
    expect(
        mixed([-100, 300], [Fraction(1, 2), Fraction(1, 2)]), "a lottery with a loss of positive probability is mixed"
    )
    expect(
        not mixed([-100, 300], [Fraction(0), Fraction(1)]), "a loss of zero probability does not make a lottery mixed"
    )


# Twelve pairs whose A lotteries are pure (one sure amount each) and whose B lotteries each mix a gain and a loss.
B_SIDE_SURE_A: list[int] = [700, 1900, 0, 2600, -300, 1500, 900, 2100, -600, 1100, 400, 1800]
B_SIDE_CHOICES: list[str] = ["A", "B", "B", "A", "B", "A", "A", "B", "A", "A", "B", "B"]
B_SIDE_LOTTERIES: list[tuple[list[int], list[str]]] = [
    ([2000, -1500], ["1/2", "1/2"]),
    ([3000, -2500], ["2/5", "3/5"]),
    ([1500, -1000], ["3/4", "1/4"]),
    ([4000, -3000], ["1/3", "2/3"]),
    ([2500, -4000], ["1/2", "1/2"]),
    ([1000, -500], ["4/5", "1/5"]),
    ([3500, -2000], ["1/4", "3/4"]),
    ([800, -1200], ["1/2", "1/2"]),
    ([5000, -3000], ["3/10", "7/10"]),
    ([2200, -2800], ["3/5", "2/5"]),
    ([1200, -600], ["1/2", "1/2"]),
    ([4500, -5000], ["2/3", "1/3"]),
]


def test_estimate_accepts_a_mixed_lottery_on_the_b_side_alone() -> None:
    """Named condition: the set is refused only when no response has a lottery that mixes a gain and a loss, each with
    positive probability. Here every A lottery is pure but every B lottery mixes, so the condition is not met: the
    estimate must return the seven named fields as finite floats, and must not refuse the set for want of a mix."""
    responses: list[dict[str, object]] = [
        {
            "pair_id": i,
            "choice": B_SIDE_CHOICES[i],
            "prizes_a": [B_SIDE_SURE_A[i]],
            "probs_a": ["1"],
            "prizes_b": B_SIDE_LOTTERIES[i][0],
            "probs_b": B_SIDE_LOTTERIES[i][1],
        }
        for i in range(len(B_SIDE_CHOICES))
    ]
    try:
        result = sol.estimate(responses)
    except ValueError:
        expect(False, "a set with a mixed B lottery must not be refused for want of a mixed-sign lottery")
    expect(
        set(result) == {"gamma_hat", "lambda_hat", "kappa_hat", "se_gamma", "se_lambda", "se_kappa", "log_likelihood"},
        "estimate must return exactly the seven named fields",
    )
    expect(
        all(isinstance(v, float) and math.isfinite(v) for v in result.values()),
        "a set with a mixed B lottery is valid: every field must be a finite float",
    )


def test_estimate_refuses_probabilities_that_sum_below_one() -> None:
    """Named condition, in a response: the probabilities of a lottery must sum to exactly 1. This response is otherwise
    valid (mixed-sign, non-negative), and its probabilities sum to 999/1000."""
    bad = [RESPONSES_BASE | {"probs_a": ["1/2", "499/1000"]}]
    must_raise(
        lambda: sol.estimate(bad),
        "a response whose probabilities sum below one",
        contains=("probabilities must sum to 1",),
    )


def test_estimate_refuses_probabilities_that_sum_above_one() -> None:
    """Named condition, in a response: the sum is 1001/1000 here, otherwise valid. A check that looks at one side only
    fails this test."""
    bad = [RESPONSES_BASE | {"probs_a": ["1/2", "501/1000"]}]
    must_raise(
        lambda: sol.estimate(bad),
        "a response whose probabilities sum above one",
        contains=("probabilities must sum to 1",),
    )


def test_estimate_refuses_a_negative_probability_even_when_the_sum_is_one() -> None:
    """Named condition, in a response: the probabilities -1/4 and 5/4 sum to exactly 1, so only the sign is wrong."""
    bad = [RESPONSES_BASE | {"probs_a": ["-1/4", "5/4"]}]
    must_raise(
        lambda: sol.estimate(bad), "a response with a negative probability", contains=("probabilities must sum to 1",)
    )


def test_zero_probability_prize_contributes_nothing_to_the_likelihood() -> None:
    """Allowed: a probability of exactly zero. A response whose loss has probability zero has the same likelihood as the
    same response with that prize removed, so the zero-probability prize adds nothing."""
    with_zero = [RESPONSES_BASE | {"probs_a": ["0", "1"]}]
    without = [RESPONSES_BASE | {"prizes_a": [300], "probs_a": ["1"]}]
    gap = abs(sol.log_likelihood(with_zero, TRUE) - sol.log_likelihood(without, TRUE))
    expect(gap <= 1e-12, "a prize of probability zero must not change the likelihood")


RESPONSES_BASE: dict[str, Any] = {
    "pair_id": 0,
    "choice": "A",
    "prizes_a": [-100, 300],
    "probs_a": ["1/2", "1/2"],
    "prizes_b": [200],
    "probs_b": ["1"],
}


def test_prospect_gain_branch_is_the_power_inverse_without_a_loss_weight() -> None:
    """Exact case at gamma = 1/2, lambda = 2. Gains: v(x) = sqrt(x). The lottery of 100 and 400, each with probability
    1/2, has value (10 + 20) / 2 = 15, and the sure amount with value 15 is 15^2 = 225 cents. A loss weight in this
    branch would give 225 / 2 instead."""
    got = sol.certainty_equivalent_cents(
        "prospect", [100, 400], [Fraction(1, 2), Fraction(1, 2)], {"gamma": 0.5, "lambda": 2.0}, WEALTH
    )
    expect(got == 225, "a lottery with a positive value is inverted by the power 1/(1 - gamma), with no loss weight")


def test_prospect_loss_branch_divides_the_value_by_lambda() -> None:
    """Exact case at gamma = 1/2, lambda = 2. Losses: v(x) = -2 sqrt(-x). The lottery of -100 and -400, each with
    probability 1/2, has value (-20 - 40) / 2 = -30. The sure amount c with v(c) = -30 has sqrt(-c) = 15, so c = -225
    cents. Without the division by lambda the answer would be -900."""
    got = sol.certainty_equivalent_cents(
        "prospect", [-100, -400], [Fraction(1, 2), Fraction(1, 2)], {"gamma": 0.5, "lambda": 2.0}, WEALTH
    )
    expect(got == -225, "a lottery with a negative value is inverted by -(-V/lambda)^(1/(1-gamma))")


def test_choice_probability_points_toward_the_higher_certainty_equivalent() -> None:
    """Sure 3000 cents for A against sure 0 for B, at the true parameters: z = kappa * 3000 / 10000 > 0, so P(A) > 1/2.
    A response that chose A contributes more than log(1/2); one that chose B contributes less."""
    a = [{"pair_id": 0, "choice": "A", "prizes_a": [3000], "probs_a": ["1"], "prizes_b": [0], "probs_b": ["1"]}]
    b = [a[0] | {"choice": "B"}]
    expect(
        sol.log_likelihood(a, TRUE) > math.log(0.5),
        "a choice of the alternative with the higher certainty equivalent must be more likely than one half",
    )
    expect(
        sol.log_likelihood(b, TRUE) < math.log(0.5),
        "a choice of the alternative with the lower certainty equivalent must be less likely than one half",
    )


def _invert3(m: list[list[float]]) -> list[list[float]]:
    """Inverse of a 3 by 3 matrix by Gauss-Jordan elimination with partial pivoting (standard library only)."""
    aug = [list(row) + [1.0 if i == j else 0.0 for j in range(3)] for i, row in enumerate(m)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        div = aug[col][col]
        aug[col] = [x / div for x in aug[col]]
        for r in range(3):
            if r != col:
                factor = aug[r][col]
                aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col], strict=True)]
    return [row[3:] for row in aug]


def _observed_information(theta: list[float]) -> list[list[float]]:
    """Negative Hessian of the oracle log-likelihood in (eta, log lambda, log kappa), by central differences, step 1e-5.
    The step is not smaller: for some questionnaires the second differences are sensitive to the step below 1e-5."""
    h = 1e-5

    def at(*moves: tuple[int, float]) -> float:
        y = list(theta)
        for idx, amount in moves:
            y[idx] += amount
        gamma = 1.0 / (1.0 + math.exp(-y[0]))
        return oracle_loglik(PARSED, gamma, math.exp(y[1]), math.exp(y[2]))

    f0 = at()
    info = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(at((i, h)) - 2.0 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            value = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (
                4.0 * h * h
            )
            info[i][j] = info[j][i] = value
    return info


def test_standard_errors_match_the_delta_method_oracle() -> None:
    """The standard errors are the square roots of the diagonal of the inverse observed information in
    (eta, log lambda, log kappa), carried to the parameters by the delta method: d gamma / d eta = gamma (1 - gamma),
    d lambda / d log lambda = lambda, d kappa / d log kappa = kappa. The oracle recomputes this at the reported
    estimate. The tolerance is 10% relative. For a poorly identified parameter the standard error is sensitive to
    round-off in the finite-difference information (for seed 49 the standard error of lambda changes by about 1% with
    the evaluation order of the same log-likelihood, and by about 12% between steps 1e-5 and 1e-6 at the optimum), so a
    tighter tolerance would test the implementation's round-off. A missing or wrong delta factor (gamma (1 - gamma),
    lambda or kappa, or a missing square root) changes a standard error by much more than 10%."""
    gamma, lam, kappa = est()["gamma_hat"], est()["lambda_hat"], est()["kappa_hat"]
    theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
    cov = _invert3(_observed_information(theta))
    want = {
        "se_gamma": gamma * (1.0 - gamma) * math.sqrt(cov[0][0]),
        "se_lambda": lam * math.sqrt(cov[1][1]),
        "se_kappa": kappa * math.sqrt(cov[2][2]),
    }
    for key, value in want.items():
        expect(
            abs(est()[key] - value) <= 1e-1 * value,
            "each standard error must be the delta-method value from the observed information at the estimate",
        )


NETWORK_MODULES = frozenset(
    {"socket", "ssl", "http", "urllib", "ftplib", "smtplib", "xmlrpc", "requests", "httpx", "aiohttp", "urllib3"}
)


def test_engine_imports_only_the_standard_library_with_no_network_and_prints_nothing(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The engine's imports are read from its source: each top-level module is in the standard library and none is a
    network module. Then each function is called on valid input, and nothing may reach stdout or stderr."""
    path = getattr(sol, "__file__", None)
    expect(isinstance(path, str), "the engine must be a module file the suite can read")
    tree = ast.parse(Path(str(path)).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names = [node.module]
        else:
            names = []
        for name in names:
            top = name.split(".")[0]
            expect(top in sys.stdlib_module_names, "elicit.py may import only the standard library")
            expect(top not in NETWORK_MODULES, "elicit.py may not import a network module")
    capsys.readouterr()
    sol.certainty_equivalent_cents("crra", [100, -50], [Fraction(1, 2), Fraction(1, 2)], {"gamma": 0.5}, WEALTH)
    sol.certainty_equivalent_cents("prospect", [100, -50], [Fraction(1, 2), Fraction(1, 2)], TRUE, WEALTH)
    sol.log_likelihood(RESPONSES[:3], TRUE)
    sol.estimate(RESPONSES)
    captured = capsys.readouterr()
    expect(captured.out == "" and captured.err == "", "no function may print to stdout or stderr")
