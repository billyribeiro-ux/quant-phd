"""Acceptance suite for the E4 project: the solver for the price-informativeness model (solver.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your solver.py next to this file. Warnings are failures, as in the browser.

Most expected values below are recomputed here by oracle functions written for this suite, which do not read solver.py
and do not use the closed forms of the reference. The small-noise checks compare with the closed form of Proposition 4,
written in this file from the page's formula. The oracle finds the linear price by fixed-point iteration on the
moments of the model (regressions of the payoff on the signal and the price, and on the price), and it evaluates each
expected utility by a quadrature over the standard normal density. The instance is SIMULATED: its two inputs come from
instance.py for the seed. A failing check names the property it tests and the idea to revisit. It never prints the
expected value.
"""

from __future__ import annotations

import ast
import importlib
import math
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

# The solver and the instance generator sit next to this file in both layouts (browser and local run), so they are
# loaded by name at run time: no import statement needs a stub for a module that a type checker cannot see.
sol: Any = importlib.import_module("solver")
make_instance: Callable[[int], dict[str, float]] = importlib.import_module("instance").make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
INST2 = make_instance(SEED + 7_919)  # a second instance, so a fixed answer for one seed must also match another
SD = float(INST["noise_sd"])
COST = float(INST["info_cost"])
KEYS = {"informed_fraction", "price_informativeness", "indifference_gap"}
TOL_GAP = 1e-8  # the indifference gap, and the agreement of the gap with the oracle, in expected-utility units
TOL_ROOT = 1e-10  # the agreement of the informed fraction with the oracle's root
TOL_MOMENT = 1e-8  # the agreement of the price informativeness with the oracle's moment formula


def expect(ok: bool, hint: str) -> None:
    """Fail with a hint that names the property. The message carries no values."""
    __tracebackhide__ = True
    if not ok:
        pytest.fail(hint, pytrace=False)


def must_raise(call: Callable[[], object], condition: str, *, contains: tuple[str, ...] = ()) -> None:
    """Fail unless call() raises ValueError (the named conditions of the specification). Each text in ``contains`` must
    appear in the message; the page quotes a message for each named condition."""
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


# ---------------------------------------------------------------------------------------------------------------------
# Oracles: independent computations of the model at a given informed fraction. The model constants are the page's.
# ---------------------------------------------------------------------------------------------------------------------

A_CARA = 2.0  # the CARA coefficient of the page
TAU_V = 1.0  # the prior precision of the payoff
TAU_E = 1.0  # the precision of the signal's noise
VAR_S = 1.0 / TAU_V + 1.0 / TAU_E  # the variance of the signal s = v + eps
_STEP = 0.02
_NODES: list[tuple[float, float]] = [
    (k * _STEP, _STEP * math.exp(-0.5 * (k * _STEP) ** 2) / math.sqrt(2.0 * math.pi)) for k in range(-500, 501)
]


def oracle_expect_exp(var_z: float, var_v: float) -> float:
    """E[exp(-Z^2 / (2 V))] for Z ~ Normal(0, var_z) and V = var_v, by the trapezoid rule over the standard normal."""
    return sum(w * math.exp(-var_z * z * z / (2.0 * var_v)) for z, w in _NODES)


def oracle_regressions(bs: float, bu: float, sd: float) -> dict[str, float]:
    """The moments of the economy when the price is p = bs s + bu u.

    The regression of v on (s, p) gives an informed agent's conditional mean, the regression of v on p gives an
    uninformed agent's, and alpha_u is the uninformed demand coefficient (x_U = alpha_u p).
    """
    varp = bs * bs * VAR_S + bu * bu * sd * sd
    covsp = bs * VAR_S
    covvp = bs / TAU_V
    var_uv = 1.0 / TAU_V - covvp * covvp / varp
    alpha_u = (covvp / varp - 1.0) / (A_CARA * var_uv)
    det = VAR_S * varp - covsp * covsp
    i11, i12, i22 = varp / det, -covsp / det, VAR_S / det
    beta_s = i11 / TAU_V + i12 * covvp
    beta_p = i12 / TAU_V + i22 * covvp
    var_iv = 1.0 / TAU_V - (beta_s / TAU_V + beta_p * covvp)
    return {
        "varp": varp,
        "covsp": covsp,
        "covvp": covvp,
        "var_uv": var_uv,
        "alpha_u": alpha_u,
        "beta_s": beta_s,
        "beta_p": beta_p,
        "var_iv": var_iv,
    }


def oracle_price(lam: float, sd: float) -> tuple[float, float]:
    """The linear equilibrium price p = bs s + bu u at informed fraction lam, by fixed-point iteration on the market
    clearing condition lam x_I + (1 - lam) x_U = u, with every demand built from the regressions above."""
    bs, bu = 0.0, -A_CARA / TAU_V
    for _ in range(10_000):
        m = oracle_regressions(bs, bu, sd)
        k_s = lam * m["beta_s"] / (A_CARA * m["var_iv"])
        k_p = lam * (m["beta_p"] - 1.0) / (A_CARA * m["var_iv"]) + (1.0 - lam) * m["alpha_u"]
        new_bs, new_bu = -k_s / k_p, 1.0 / k_p
        converged = abs(new_bs - bs) + abs(new_bu - bu) <= 1e-13
        bs, bu = new_bs, new_bu
        if converged:
            break
    return bs, bu


def oracle_gap(lam: float, sd: float, cost: float) -> float:
    """The expected-utility difference E[U_I] - E[U_U] at informed fraction lam, net of the cost.

    For an informed agent, with conditional mean m and variance V at the optimal demand, E[U | info] is
    -exp(a c) exp(-(m - p)^2 / (2 V)), where m - p is the conditional mean less the price. An uninformed agent pays no
    cost, so the factor exp(a c) is absent for it. At lam = 0 the informed term is the limit as lam tends to 0.
    """
    bs, bu = oracle_price(lam, sd)
    m = oracle_regressions(bs, bu, sd)
    q_s, q_p = m["beta_s"], m["beta_p"] - 1.0
    var_informed_gap = q_s * q_s * VAR_S + 2.0 * q_s * q_p * m["covsp"] + q_p * q_p * m["varp"]
    f_i = oracle_expect_exp(var_informed_gap, m["var_iv"])
    q_u = m["covvp"] / m["varp"] - 1.0
    f_u = oracle_expect_exp(q_u * q_u * m["varp"], m["var_uv"])
    return f_u - math.exp(A_CARA * cost) * f_i


def oracle_informativeness(lam: float, sd: float) -> float:
    """The squared correlation of the payoff and the price, from the population moments of the equilibrium price."""
    bs, bu = oracle_price(lam, sd)
    varp = bs * bs * VAR_S + bu * bu * sd * sd
    return bs * bs / (TAU_V * varp)


def oracle_root(sd: float, cost: float) -> float:
    """The informed fraction by bisection on the oracle's gap, with the boundary rule of the page."""
    if oracle_gap(0.0, sd, cost) <= 0.0:
        return 0.0
    if oracle_gap(1.0, sd, cost) >= 0.0:
        return 1.0
    low, high = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (low + high)
        if oracle_gap(mid, sd, cost) > 0.0:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def run(noise_sd: float, info_cost: float) -> dict[str, float]:
    """The solver's answer for one input, with its shape checked: exactly the three named keys, all floats."""
    __tracebackhide__ = True
    out: dict[str, float] = sol.solve_model(noise_sd, info_cost)
    expect(isinstance(out, dict) and set(out) == KEYS, "solve_model must return exactly the three named keys")
    expect(all(isinstance(out[k], float) for k in KEYS), "every returned value must be a float")
    return out


INSTANCES = {"first": INST, "second": INST2}


# ---------------------------------------------------------------------------------------------------------------------
# The named conditions of the specification, each in both directions of its inequality.
# ---------------------------------------------------------------------------------------------------------------------


def test_noise_volume_zero_is_rejected() -> None:
    must_raise(lambda: sol.solve_model(0.0, COST), "noise volume zero", contains=("noise volume must be positive",))


def test_noise_volume_negative_is_rejected() -> None:
    must_raise(lambda: sol.solve_model(-SD, COST), "noise volume negative", contains=("noise volume must be positive",))


def test_noise_volume_infinite_is_rejected() -> None:
    must_raise(
        lambda: sol.solve_model(math.inf, COST), "noise volume not finite", contains=("noise volume must be positive",)
    )


def test_noise_volume_nan_is_rejected() -> None:
    must_raise(
        lambda: sol.solve_model(math.nan, COST),
        "noise volume not a number",
        contains=("noise volume must be positive",),
    )


def test_noise_volume_tiny_positive_is_accepted() -> None:
    out = run(1e-12, COST)
    expect(0.0 <= out["informed_fraction"] <= 1.0, "the informed fraction must lie in [0, 1] for a tiny noise volume")
    expect(0.0 <= out["price_informativeness"] <= 1.0, "the informativeness must lie in [0, 1] for a tiny noise volume")
    expect(all(math.isfinite(out[k]) for k in KEYS), "every output must be finite for a tiny positive noise volume")


def test_info_cost_negative_is_rejected() -> None:
    must_raise(
        lambda: sol.solve_model(SD, -0.01),
        "information cost negative",
        contains=("information cost must be nonnegative",),
    )


def test_info_cost_just_below_zero_is_rejected() -> None:
    must_raise(
        lambda: sol.solve_model(SD, -1e-12),
        "information cost just below zero",
        contains=("information cost must be nonnegative",),
    )


def test_info_cost_zero_is_accepted() -> None:
    out = run(SD, 0.0)
    expect(0.0 <= out["informed_fraction"] <= 1.0, "the informed fraction must lie in [0, 1] at zero information cost")
    expect(all(math.isfinite(out[k]) for k in KEYS), "every output must be finite at zero information cost")


# ---------------------------------------------------------------------------------------------------------------------
# Properties on the instance (run for the first and the second instance).
# ---------------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("which", list(INSTANCES))
def test_outputs_are_finite_and_in_range(which: str) -> None:
    inst = INSTANCES[which]
    out = run(float(inst["noise_sd"]), float(inst["info_cost"]))
    expect(all(math.isfinite(out[k]) for k in KEYS), "every output must be finite")
    expect(0.0 <= out["informed_fraction"] <= 1.0, "the informed fraction must lie in [0, 1]")
    expect(0.0 <= out["price_informativeness"] <= 1.0, "the price informativeness must lie in [0, 1]")


@pytest.mark.parametrize("which", list(INSTANCES))
def test_indifference_holds_at_an_interior_fraction(which: str) -> None:
    inst = INSTANCES[which]
    out = run(float(inst["noise_sd"]), float(inst["info_cost"]))
    if 0.0 < out["informed_fraction"] < 1.0:
        expect(
            abs(out["indifference_gap"]) <= TOL_GAP,
            "the indifference gap should vanish at an interior fraction: check the informed-minus-uninformed utility",
        )


@pytest.mark.parametrize("which", list(INSTANCES))
def test_gap_is_the_oracle_gap_at_the_reported_fraction(which: str) -> None:
    inst = INSTANCES[which]
    sd, cost = float(inst["noise_sd"]), float(inst["info_cost"])
    out = run(sd, cost)
    expect(
        abs(out["indifference_gap"] - oracle_gap(out["informed_fraction"], sd, cost)) <= TOL_GAP,
        "the reported gap must be the informed-minus-uninformed expected utility at the reported fraction",
    )


@pytest.mark.parametrize("which", list(INSTANCES))
def test_boundary_rule_holds(which: str) -> None:
    inst = INSTANCES[which]
    sd, cost = float(inst["noise_sd"]), float(inst["info_cost"])
    lam = run(sd, cost)["informed_fraction"]
    gap_0, gap_1 = oracle_gap(0.0, sd, cost), oracle_gap(1.0, sd, cost)
    if lam == 0.0:
        expect(
            gap_0 <= TOL_GAP,
            "a zero fraction is the answer only when the gap is nonpositive as the fraction tends to 0",
        )
    elif lam == 1.0:
        expect(gap_1 >= -TOL_GAP, "a unit fraction is the answer only when the gap is nonnegative at 1")
    else:
        expect(
            gap_0 > 0.0 and gap_1 < 0.0,
            "an interior fraction needs a gap that is positive as the fraction tends to 0 and negative at 1",
        )


@pytest.mark.parametrize("which", list(INSTANCES))
def test_fraction_is_the_oracle_root(which: str) -> None:
    inst = INSTANCES[which]
    sd, cost = float(inst["noise_sd"]), float(inst["info_cost"])
    lam = run(sd, cost)["informed_fraction"]
    expect(
        abs(lam - oracle_root(sd, cost)) <= TOL_ROOT,
        "the informed fraction should be the root of the gap, found by a different method: check the bisection",
    )


@pytest.mark.parametrize("which", list(INSTANCES))
def test_informativeness_is_the_squared_correlation(which: str) -> None:
    inst = INSTANCES[which]
    sd, cost = float(inst["noise_sd"]), float(inst["info_cost"])
    out = run(sd, cost)
    lam = out["informed_fraction"]
    if lam == 0.0:
        expect(
            abs(out["price_informativeness"]) <= 1e-12,
            "with no informed investors the price carries no signal about the payoff: its correlation is zero",
        )
        return
    expect(
        abs(out["price_informativeness"] - oracle_informativeness(lam, sd)) <= TOL_MOMENT,
        "the informativeness should be the squared correlation of the payoff and the price at the reported fraction",
    )


def test_zero_fraction_is_reported_above_the_cost_threshold() -> None:
    out = run(0.6, 0.30)
    expect(
        out["informed_fraction"] == 0.0,
        "the informed fraction must be 0 when the gap at 0 is nonpositive: check the boundary rule",
    )
    expect(
        abs(out["price_informativeness"]) <= 1e-12,
        "with no informed investors the price carries no signal about the payoff",
    )
    expect(
        abs(out["indifference_gap"] - oracle_gap(0.0, 0.6, 0.30)) <= TOL_GAP,
        "the reported gap at fraction 0 must be the limit of the gap as the fraction tends to 0",
    )


def test_unit_fraction_is_reported_at_zero_cost() -> None:
    out = run(2.0, 0.0)
    expect(
        out["informed_fraction"] == 1.0,
        "the informed fraction must be 1 when the gap at 1 is nonnegative: check the boundary rule",
    )
    expect(
        abs(out["price_informativeness"] - oracle_informativeness(1.0, 2.0)) <= TOL_MOMENT,
        "the informativeness at fraction 1 should be the squared correlation of the payoff and the price",
    )
    expect(
        abs(out["indifference_gap"] - oracle_gap(1.0, 2.0, 0.0)) <= TOL_GAP,
        "the reported gap at fraction 1 must be the informed-minus-uninformed expected utility there",
    )


# ---------------------------------------------------------------------------------------------------------------------
# Hard-coded answers, determinism and the solver's conduct.
# ---------------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("which", list(INSTANCES))
def test_fraction_falls_with_the_cost(which: str) -> None:
    """Proposition 5: on the interior, the informed fraction does not rise when the information cost rises."""
    inst = INSTANCES[which]
    sd, cost = float(inst["noise_sd"]), float(inst["info_cost"])
    lam = run(sd, cost)["informed_fraction"]
    lam_dearer = run(sd, cost + 0.005)["informed_fraction"]
    expect(
        lam_dearer <= lam + 1e-9,
        "a higher information cost should not raise the informed fraction: check the sign of the cost in the gap",
    )


@pytest.mark.parametrize("which", list(INSTANCES))
def test_fraction_is_proportional_to_the_noise_volume(which: str) -> None:
    """Proposition 5: on the interior, the informed fraction is proportional to the noise volume at a fixed cost."""
    inst = INSTANCES[which]
    sd, cost = float(inst["noise_sd"]), float(inst["info_cost"])
    lam = run(sd, cost)["informed_fraction"]
    lam_scaled = run(1.02 * sd, cost)["informed_fraction"]
    expect(
        abs(lam_scaled - 1.02 * lam) <= 1e-6,
        "at a fixed cost the informed fraction should scale with the noise volume: check how sigma enters the price",
    )


def test_answers_change_across_seeds_zero_to_forty_nine() -> None:
    fractions = set()
    for seed in range(50):
        inst = make_instance(seed)
        fractions.add(round(run(float(inst["noise_sd"]), float(inst["info_cost"]))["informed_fraction"], 9))
    expect(len(fractions) > 1, "the answer does not change with the instance: check that the inputs enter the solution")


def test_same_inputs_give_the_same_answer() -> None:
    first = run(SD, COST)
    second = run(SD, COST)
    expect(first == second, "the same inputs must give the same answer every time")


def test_solver_imports_only_the_standard_library() -> None:
    tree = ast.parse(Path(sol.__file__).read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    extra = sorted(names - set(sys.stdlib_module_names))
    expect(not extra, "the solver may use only the standard library: remove the import of a package outside it")


def test_solver_prints_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    run(SD, COST)
    run(SD, 0.0)
    expect(capsys.readouterr().out == "", "no function may print: remove the print call from solver.py")


# ---------------------------------------------------------------------------------------------------------------------
# The stop rule is relative to the bracket's upper end, so a small root is as accurate as a large one.
# ---------------------------------------------------------------------------------------------------------------------


def closed_form_root(sd: float, cost: float) -> float:
    """The informed fraction of Proposition 4 in closed form, from the page's formula (not from reference.py)."""
    t = (TAU_V + TAU_E) * math.exp(-2.0 * A_CARA * cost) - TAU_V
    if t <= 0.0:
        return 0.0
    if t >= TAU_E * TAU_E / (TAU_E + A_CARA * A_CARA * sd * sd):
        return 1.0
    return A_CARA * sd * math.sqrt(t / (TAU_E * (TAU_E - t)))


@pytest.mark.parametrize("sd", [1e-6, 1e-9])
def test_small_noise_root_is_relatively_accurate(sd: float) -> None:
    """The bisection stops at a relative width of 1e-12, so a root near 1e-9 is as precise as one near 0.5."""
    lam = run(sd, 0.13)["informed_fraction"]
    exact = closed_form_root(sd, 0.13)
    expect(
        exact > 0.0 and abs(lam - exact) <= 1e-8 * exact,
        "the informed fraction must be accurate relative to its size: check the stop rule of the bisection",
    )


@pytest.mark.parametrize("sd", [1e-11, 1e-12])
def test_tiny_noise_root_is_relatively_accurate(sd: float) -> None:
    """A root near 1e-12 is as precise as one near 0.5: the bracket starts at 0, and its stop rule is relative to its
    upper end, so no absolute width (such as a fixed number of halvings) limits the accuracy of a small root."""
    lam = run(sd, 0.15)["informed_fraction"]
    exact = closed_form_root(sd, 0.15)
    expect(
        exact > 0.0 and abs(lam - exact) <= 1e-8 * exact,
        "the informed fraction must be accurate relative to its size: check the bracket and the bisection stop rule",
    )
