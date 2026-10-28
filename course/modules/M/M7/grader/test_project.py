"""Acceptance suite for the M7 project: the constrained allocator (constrained_allocator.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your constrained_allocator.py next to this file. Warnings are failures, as in the browser. The case is SIMULATED.

Every residual below is recomputed here from the case and from the definitions on the project page. Your certificate
is compared with that recomputation; it is not trusted. A failure names the property it checks and the idea to revisit,
and it never prints the value the suite expected.
"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import math
import os
import sys
import warnings
from collections.abc import Callable, Mapping
from functools import cache
from pathlib import Path
from typing import Any

import constrained_allocator as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
TOL = 1e-8  # every residual of the page is compared with this tolerance
FIELDS = ("gamma", "mu", "sigma", "w0", "lower", "upper", "sector", "sector_caps", "turnover_limit")
CERTIFICATE_KEYS = ("primal_residual", "stationarity_residual", "dual_residual", "complementary_slackness")
PRISTINE: dict[str, Any] = json.loads(make_instance(SEED)["payload"])
N: int = len(PRISTINE["mu"])
K: int = len(PRISTINE["sector_caps"])


def case_copy(**changes: Any) -> dict[str, Any]:
    """A deep copy of the seed's case, with top-level fields replaced."""
    case = copy.deepcopy(PRISTINE)
    case.update(changes)
    return case


def changed(mutate: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    """A deep copy of the seed's case, changed in place by mutate."""
    case = copy.deepcopy(PRISTINE)
    mutate(case)
    return case


def sector_sum(case: Mapping[str, Any], w: list[float], k: int) -> float:
    return sum(w[i] for i in range(len(w)) if case["sector"][i] == k)


def turnover_gap(case: Mapping[str, Any], w: list[float]) -> float:
    """Total absolute change from the starting portfolio, less the limit: the page's turnover constraint."""
    return float(sum(abs(w[i] - case["w0"][i]) for i in range(len(w))) - case["turnover_limit"])


def inequality_pairs(case: Mapping[str, Any], w: list[float], mult: Mapping[str, Any]) -> list[tuple[float, float]]:
    """Each inequality multiplier with its constraint g(w, t) <= 0, where t_i = |w_i - w0_i| (page, linearized form)."""
    n = len(w)
    d = [w[i] - case["w0"][i] for i in range(n)]
    t = [abs(v) for v in d]
    pairs: list[tuple[float, float]] = []
    pairs += [(mult["lower"][i], case["lower"][i] - w[i]) for i in range(n)]
    pairs += [(mult["upper"][i], w[i] - case["upper"][i]) for i in range(n)]
    pairs += [
        (mult["sector"][k], sector_sum(case, w, k) - case["sector_caps"][k]) for k in range(len(case["sector_caps"]))
    ]
    pairs += [(mult["turnover_plus"][i], d[i] - t[i]) for i in range(n)]
    pairs += [(mult["turnover_minus"][i], -d[i] - t[i]) for i in range(n)]
    pairs += [(mult["turnover_total"], sum(t) - case["turnover_limit"])]
    return pairs


def stationarity(case: Mapping[str, Any], w: list[float], mult: Mapping[str, Any]) -> tuple[list[float], list[float]]:
    """The residual of the weight equations and of the auxiliary-variable equations, at t_i = |w_i - w0_i|."""
    n = len(w)
    sigma, mu, gamma = case["sigma"], case["mu"], case["gamma"]
    rw = []
    rt = []
    for i in range(n):
        grad = gamma * sum(sigma[i][j] * w[j] for j in range(n)) - mu[i]
        rw.append(
            grad
            + mult["budget"]
            - mult["lower"][i]
            + mult["upper"][i]
            + mult["sector"][case["sector"][i]]
            + mult["turnover_plus"][i]
            - mult["turnover_minus"][i]
        )
        rt.append(mult["turnover_total"] - mult["turnover_plus"][i] - mult["turnover_minus"][i])
    return rw, rt


def recomputed_certificate(case: Mapping[str, Any], w: list[float], mult: Mapping[str, Any]) -> dict[str, float]:
    gaps = [g for _, g in inequality_pairs(case, w, mult)]
    primal = max([0.0, abs(sum(w) - 1.0), *gaps])
    dual = max(0.0, -min(m for m, _ in inequality_pairs(case, w, mult)))
    complementary = max(abs(m * g) for m, g in inequality_pairs(case, w, mult))
    rw, rt = stationarity(case, w, mult)
    return {
        "primal_residual": primal,
        "stationarity_residual": max(max(abs(v) for v in rw), max(abs(v) for v in rt)),
        "dual_residual": dual,
        "complementary_slackness": complementary,
    }


def objective(case: Mapping[str, Any], w: list[float]) -> float:
    n = len(w)
    quadratic = sum(case["sigma"][i][j] * w[i] * w[j] for i in range(n) for j in range(n))
    return float(0.5 * case["gamma"] * quadratic - sum(case["mu"][i] * w[i] for i in range(n)))


def output_shape(case: Mapping[str, Any], out: Any) -> None:
    """The returned object has the fields, names and lengths of the page's contract."""
    __tracebackhide__ = True
    assert isinstance(out, Mapping), "allocate must return a mapping with the three fields of the page."
    assert set(out) == {"weights", "multipliers", "certificate"}, (
        "allocate must return exactly the keys weights, multipliers and certificate."
    )
    n = len(case["mu"])
    k = len(case["sector_caps"])
    weights = out["weights"]
    assert isinstance(weights, list) and len(weights) == n, "weights must be a list with one entry per asset."
    assert all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in weights), (
        "every weight must be a real number."
    )
    mult = out["multipliers"]
    assert isinstance(mult, Mapping) and set(mult) == set(
        ("budget", "lower", "upper", "sector", "turnover_plus", "turnover_minus", "turnover_total")
    ), "multipliers must have the seven frozen names of the page."
    for key, size in (("lower", n), ("upper", n), ("sector", k), ("turnover_plus", n), ("turnover_minus", n)):
        assert isinstance(mult[key], list) and len(mult[key]) == size, (
            f"multipliers[{key!r}] must be a list with one entry per "
            + ("sector cap." if key == "sector" else "asset.")
        )
    assert isinstance(out["certificate"], Mapping) and set(out["certificate"]) == set(CERTIFICATE_KEYS), (
        "the certificate must carry the four residual fields of the page."
    )


@cache
def seed_output() -> dict[str, Any]:
    out: dict[str, Any] = sol.allocate(copy.deepcopy(PRISTINE))
    return out


def weights_of(out: Mapping[str, Any]) -> list[float]:
    return [float(v) for v in out["weights"]]


def multipliers_of(out: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: ([float(v) for v in value] if isinstance(value, list) else float(value))
        for key, value in out["multipliers"].items()
    }


def assert_kkt(case: Mapping[str, Any], out: Mapping[str, Any]) -> None:
    """Primal feasibility, dual feasibility, stationarity in weights and in t, and complementary slackness."""
    __tracebackhide__ = True
    w = weights_of(out)
    mult = multipliers_of(out)
    assert abs(sum(w) - 1.0) <= TOL, "budget: the weights must sum to one."
    for i in range(len(w)):
        assert case["lower"][i] - TOL <= w[i] <= case["upper"][i] + TOL, (
            f"box: asset {i} lies outside its lower and upper bounds."
        )
    for k in range(len(case["sector_caps"])):
        assert sector_sum(case, w, k) <= case["sector_caps"][k] + TOL, (
            f"sector cap: sector {k} exceeds its cap; the caps are inequalities on the sector sums."
        )
    assert turnover_gap(case, w) <= TOL, (
        "turnover: the total change from the starting portfolio, measured from w0, exceeds the limit."
    )
    assert all(m >= -TOL for m, _ in inequality_pairs(case, w, mult)), (
        "dual feasibility fails: every inequality multiplier must be non-negative."
    )
    rw, rt = stationarity(case, w, mult)
    assert max(abs(v) for v in rw) <= TOL, (
        "stationarity fails in the weights: check the sign of each bound multiplier and of the budget multiplier."
    )
    assert max(abs(v) for v in rt) <= TOL, (
        "stationarity fails in the turnover auxiliaries: each t_i enters the plus and minus constraints and the total."
    )
    assert max(abs(m * g) for m, g in inequality_pairs(case, w, mult)) <= TOL, (
        "complementary slackness fails: a multiplier is non-zero where its constraint is slack."
    )


def hand_case(**fields: Any) -> dict[str, Any]:
    """A two- or one-asset case written out by hand; each expected answer on the test is worked by hand as well."""
    base: dict[str, Any] = {
        "label": "SIMULATED hand case for the acceptance suite, not a real portfolio",
        "gamma": 1.0,
        "sector": [0, 0],
        "sector_caps": [2.0],
        "turnover_limit": 2.0,
        "sigma": [[1.0, 0.0], [0.0, 1.0]],
        "lower": [-1.0, -1.0],
        "upper": [2.0, 2.0],
    }
    base.update(fields)
    return base


HAND_CASES: dict[str, tuple[dict[str, Any], list[float]]] = {
    # Budget only: stationarity w - mu + nu 1 = 0 gives w = mu + 0.3 on this grid, so w = (0.6, 0.4).
    "budget only": (hand_case(mu=[0.3, 0.1], w0=[0.5, 0.5]), [0.6, 0.4]),
    # With no turnover allowed, the only feasible point is the starting portfolio.
    "zero turnover": (hand_case(mu=[0.3, 0.1], w0=[0.5, 0.5], turnover_limit=0.0), [0.5, 0.5]),
    # One asset: the budget alone fixes the weight at one.
    "single asset": (
        {
            "label": "SIMULATED hand case for the acceptance suite, not a real portfolio",
            "gamma": 3.0,
            "sigma": [[0.04]],
            "mu": [0.02],
            "w0": [1.0],
            "lower": [0.0],
            "upper": [1.0],
            "sector": [0],
            "sector_caps": [1.0],
            "turnover_limit": 0.5,
        },
        [1.0],
    ),
    # The second upper bound (0.3) binds: the unconstrained answer (0.35, 0.65) is cut to (0.7, 0.3).
    "upper bound binding": (
        hand_case(mu=[0.2, 0.5], w0=[0.8, 0.2], upper=[1.0, 0.3], turnover_limit=0.5),
        [0.7, 0.3],
    ),
    # The turnover limit binds: the unconstrained answer (0.7, 0.3) is cut to (0.6, 0.4), a change of 0.1 each way.
    "turnover binding": (hand_case(mu=[0.4, 0.0], w0=[0.5, 0.5], turnover_limit=0.2), [0.6, 0.4]),
}


# ---------------------------------------------------------------------------------------------------------------------
# Structure and the seed's instance
# ---------------------------------------------------------------------------------------------------------------------


def test_module_defines_allocate_with_one_argument() -> None:
    import inspect

    assert callable(getattr(sol, "allocate", None)), "constrained_allocator.py must define allocate."
    assert list(inspect.signature(sol.allocate).parameters) == ["instance"], (
        "allocate must take exactly one argument, named instance (the decoded case)."
    )


def test_instance_is_simulated_and_deterministic() -> None:
    assert "SIMULATED" in make_instance(SEED)["label"], "every instance is labelled SIMULATED."
    assert json.loads(make_instance(SEED)["payload"]) == PRISTINE, "make_instance must return the same case per seed."


def test_only_standard_library_imports() -> None:
    import ast

    source = Path(sol.__file__).read_text(encoding="utf-8")
    names: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split(".")[0])
    outside = sorted(name for name in names if name not in sys.stdlib_module_names and name != "__future__")
    assert not outside, "constrained_allocator.py must use the standard library only."
    assert "instance" not in names and "test_project" not in names, (
        "constrained_allocator.py must not import a grader file."
    )


def test_output_has_the_three_fields_and_frozen_names() -> None:
    output_shape(PRISTINE, seed_output())


def test_weights_and_multipliers_are_real_numbers() -> None:
    out = seed_output()
    for value in (*out["weights"], *out["certificate"].values()):
        assert isinstance(value, (int, float)) and not isinstance(value, bool), "every returned number must be real."
        assert math.isfinite(value), "every returned number must be finite."


# ---------------------------------------------------------------------------------------------------------------------
# Feasibility and the KKT conditions on the seed's case
# ---------------------------------------------------------------------------------------------------------------------


def test_budget_is_met() -> None:
    assert abs(sum(weights_of(seed_output())) - 1.0) <= TOL, "budget: the weights must sum to one."


def test_box_is_met_for_every_asset() -> None:
    w = weights_of(seed_output())
    for i in range(N):
        assert PRISTINE["lower"][i] - TOL <= w[i] <= PRISTINE["upper"][i] + TOL, (
            f"box: asset {i} lies outside its bounds; a long-only bound is zero, and a short bound is negative."
        )


def test_sector_caps_are_met_for_every_sector() -> None:
    w = weights_of(seed_output())
    for k in range(K):
        assert sector_sum(PRISTINE, w, k) <= PRISTINE["sector_caps"][k] + TOL, (
            f"sector cap: sector {k} exceeds its cap."
        )


def test_turnover_is_within_the_limit_measured_from_w0() -> None:
    assert turnover_gap(PRISTINE, weights_of(seed_output())) <= TOL, (
        "turnover: the sum of absolute changes from w0 exceeds the limit; measure from w0, not from zero."
    )


def test_multipliers_are_non_negative() -> None:
    mult = multipliers_of(seed_output())
    assert all(m >= -TOL for m, _ in inequality_pairs(PRISTINE, weights_of(seed_output()), mult)), (
        "dual feasibility fails: an inequality multiplier is negative."
    )


def test_stationarity_holds_in_the_weights() -> None:
    rw, _ = stationarity(PRISTINE, weights_of(seed_output()), multipliers_of(seed_output()))
    assert max(abs(v) for v in rw) <= TOL, (
        "stationarity fails in the weights: check the sign of the lower and upper bound multipliers and the budget."
    )


def test_stationarity_holds_in_the_turnover_auxiliaries() -> None:
    _, rt = stationarity(PRISTINE, weights_of(seed_output()), multipliers_of(seed_output()))
    assert max(abs(v) for v in rt) <= TOL, (
        "stationarity fails in the auxiliaries: the total multiplier must equal the plus and minus "
        "multipliers of each t_i."
    )


def test_complementary_slackness_holds() -> None:
    pairs = inequality_pairs(PRISTINE, weights_of(seed_output()), multipliers_of(seed_output()))
    assert max(abs(m * g) for m, g in pairs) <= TOL, (
        "complementary slackness fails: a multiplier is positive while its constraint is slack."
    )


def test_certificate_agrees_with_the_recomputed_residuals() -> None:
    out = seed_output()
    recomputed = recomputed_certificate(PRISTINE, weights_of(out), multipliers_of(out))
    for key in CERTIFICATE_KEYS:
        assert abs(float(out["certificate"][key]) - recomputed[key]) <= 1e-9, (
            f"certificate: {key} does not match the residual recomputed from your weights and multipliers."
        )


def test_certificate_residuals_are_within_tolerance() -> None:
    for key in CERTIFICATE_KEYS:
        assert float(seed_output()["certificate"][key]) <= TOL, (
            f"certificate: {key} is above the tolerance; the page states the bound on each residual."
        )


@pytest.mark.parametrize("y_weight", [0.0, 0.25, 0.75], ids=["start", "quarter", "three-quarter"])
def test_no_feasible_comparator_beats_the_solution(y_weight: float) -> None:
    """Each comparator is a convex mix of the solution and the starting portfolio, so it is feasible."""
    w = weights_of(seed_output())
    y = [(1 - y_weight) * w[i] + y_weight * PRISTINE["w0"][i] for i in range(N)]
    assert objective(PRISTINE, w) <= objective(PRISTINE, y) + 1e-9, (
        "optimality: a feasible comparator has a lower objective than the returned weights."
    )


# ---------------------------------------------------------------------------------------------------------------------
# Hand-worked cases with known answers
# ---------------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("name", list(HAND_CASES), ids=list(HAND_CASES))
def test_hand_case_matches_its_worked_answer(name: str) -> None:
    case, expected = HAND_CASES[name]
    out = sol.allocate(copy.deepcopy(case))
    output_shape(case, out)
    got = weights_of(out)
    for i, value in enumerate(expected):
        assert abs(got[i] - value) <= TOL, (
            f"{name}: weight {i} differs from the worked answer; re-derive the stationarity equation for this case."
        )
    assert_kkt(case, out)


# ---------------------------------------------------------------------------------------------------------------------
# Named ValueError conditions: each has an invalid case, and a valid case on or just inside its limit
# ---------------------------------------------------------------------------------------------------------------------


def _set(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
    def apply(case: dict[str, Any]) -> None:
        target: Any = case
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value

    return apply


def _sigma_rank_one(case: dict[str, Any]) -> None:
    """Every entry 0.01: the second LDL pivot is exactly zero, so Sigma is singular."""
    case["sigma"] = [[0.01] * N for _ in range(N)]


def _sigma_small_eigenvalue(case: dict[str, Any]) -> None:
    """0.01 everywhere plus 0.0001 on the diagonal: the smallest eigenvalue is 0.0001, just above zero."""
    case["sigma"] = [[0.01 + (0.0001 if i == j else 0.0) for j in range(N)] for i in range(N)]


def _sigma_negative_definite(case: dict[str, Any]) -> None:
    case["sigma"] = [[-0.01 if i == j else 0.0 for j in range(N)] for i in range(N)]


def _sigma_indefinite(case: dict[str, Any]) -> None:
    """Symmetric, with a positive diagonal, but the leading 2x2 block [[0.01, 0.02], [0.02, 0.01]] is indefinite."""
    case["sigma"][0][0] = 0.01
    case["sigma"][1][1] = 0.01
    case["sigma"][0][1] = 0.02
    case["sigma"][1][0] = 0.02


def _sigma_asymmetric(case: dict[str, Any]) -> None:
    case["sigma"][0][1] = case["sigma"][1][0] + 0.0001


def _sigma_asymmetric_other_sign(case: dict[str, Any]) -> None:
    case["sigma"][0][1] = case["sigma"][1][0] - 0.0001


def _sigma_symmetric_exact(case: dict[str, Any]) -> None:
    """The boundary of symmetry: the two entries are equal."""
    case["sigma"][0][1] = case["sigma"][1][0]


def _start_sum_off(case: dict[str, Any]) -> None:
    """Sum one-and-2e-9: outside the 1e-9 tolerance the page states for the starting portfolio, so refused."""
    case["w0"][0] = case["w0"][0] + 0.000000002


def _start_sum_low(case: dict[str, Any]) -> None:
    """Sum one-less-2e-9: outside the tolerance on the low side, so refused."""
    case["w0"][0] = case["w0"][0] - 0.000000002


def _start_sum_within_tolerance(case: dict[str, Any]) -> None:
    """Sum one-and-5e-10: inside the 1e-9 tolerance, so accepted."""
    case["w0"][0] = case["w0"][0] + 0.0000000005


def _start_sum_within_tolerance_low(case: dict[str, Any]) -> None:
    """Sum one-less-5e-10: inside the 1e-9 tolerance on the low side, so accepted."""
    case["w0"][0] = case["w0"][0] - 0.0000000005


def _upper_below_start(case: dict[str, Any]) -> None:
    case["upper"][0] = case["w0"][0] - 0.000000002


def _upper_within_tolerance(case: dict[str, Any]) -> None:
    case["upper"][0] = case["w0"][0] - 0.0000000005


def _lower_above_start(case: dict[str, Any]) -> None:
    case["lower"][0] = case["w0"][0] + 0.000000002
    case["upper"][0] = max(case["upper"][0], case["w0"][0] + 0.000001)


def _lower_within_tolerance(case: dict[str, Any]) -> None:
    case["lower"][0] = case["w0"][0] + 0.0000000005
    case["upper"][0] = max(case["upper"][0], case["w0"][0] + 0.000000001)


def _cap_below_start(case: dict[str, Any]) -> None:
    k = case["sector"][0]
    in_sector = sum(case["w0"][i] for i in range(N) if case["sector"][i] == k)
    case["sector_caps"][k] = in_sector - 0.000000002


def _cap_within_tolerance(case: dict[str, Any]) -> None:
    k = case["sector"][0]
    in_sector = sum(case["w0"][i] for i in range(N) if case["sector"][i] == k)
    case["sector_caps"][k] = in_sector - 0.0000000005


def _lower_over_upper(case: dict[str, Any]) -> None:
    case["lower"][0] = case["upper"][0] + 0.000001


def _lower_equal_upper(case: dict[str, Any]) -> None:
    """The boundary of the bound order: lower equal to upper, both at the starting weight."""
    case["lower"][0] = case["w0"][0]
    case["upper"][0] = case["w0"][0]


def _sector_label_out_of_range(case: dict[str, Any]) -> None:
    case["sector"][0] = K


def _sector_label_below_range(case: dict[str, Any]) -> None:
    case["sector"][0] = -1


def _sector_without_assets(case: dict[str, Any]) -> None:
    case["sector"] = [0] * N


def _sector_cap_without_assets(case: dict[str, Any]) -> None:
    """One more cap than there are labels: the added sector has no asset, and the other sectors are unchanged."""
    case["sector_caps"] = [*case["sector_caps"], 0.5]


def _one_entry_short(case: dict[str, Any]) -> None:
    case["mu"] = case["mu"][:-1]


def _one_entry_too_many(field: str) -> Callable[[dict[str, Any]], None]:
    def apply(case: dict[str, Any]) -> None:
        case[field] = [*case[field], case[field][-1]]

    return apply


def _sigma_row_too_long(case: dict[str, Any]) -> None:
    case["sigma"][0] = [*case["sigma"][0], 0.0]


def _sigma_row_too_short(case: dict[str, Any]) -> None:
    case["sigma"][0] = case["sigma"][0][:-1]


def _sigma_extra_row(case: dict[str, Any]) -> None:
    case["sigma"] = [*case["sigma"], case["sigma"][-1]]


# (identifier, invalid mutation, valid mutation); the invalid mutation must be refused with ValueError and the valid
# mutation must be accepted. Where the limit is a tolerance, the valid form sits just inside it; where it is an
# equality, the valid form is the boundary itself; otherwise the valid form is the seed case.
NAMED_CONDITIONS: list[tuple[str, Callable[[dict[str, Any]], None], Callable[[dict[str, Any]], None]]] = [
    ("sigma-symmetric", _sigma_asymmetric, _sigma_symmetric_exact),
    ("sigma-positive-definite", _sigma_rank_one, _sigma_small_eigenvalue),
    ("gamma-positive-zero", _set(("gamma",), 0.0), _set(("gamma",), 0.000001)),
    ("gamma-positive-negative", _set(("gamma",), -1.0), _set(("gamma",), 0.000001)),
    ("turnover-limit-not-negative", _set(("turnover_limit",), -0.000001), _set(("turnover_limit",), 0.0)),
    ("lower-not-above-upper", _lower_over_upper, _lower_equal_upper),
    ("start-sums-to-one", _start_sum_off, _start_sum_within_tolerance),
    ("start-within-upper", _upper_below_start, _upper_within_tolerance),
    ("start-within-lower", _lower_above_start, _lower_within_tolerance),
    ("start-within-sector-cap", _cap_below_start, _cap_within_tolerance),
    ("sector-label-in-range", _sector_label_out_of_range, lambda case: None),
    ("every-sector-has-an-asset", _sector_without_assets, lambda case: None),
    ("one-entry-per-asset", _one_entry_short, lambda case: None),
]


def _gamma_just_inside_zero(case: dict[str, Any]) -> None:
    """Gamma one-billionth: positive, so accepted (the lower end of the valid range is zero, excluded)."""
    case["gamma"] = 0.000000001


# The exact boundary values the page names as valid: a bound equal to the starting weight, a cap equal to the starting
# sector weight, and the starting sum just inside the 1e-9 tolerance on the low side.
def _lower_equal_start(case: dict[str, Any]) -> None:
    case["lower"][0] = case["w0"][0]


def _upper_equal_start(case: dict[str, Any]) -> None:
    case["upper"][0] = case["w0"][0]


def _cap_equal_start(case: dict[str, Any]) -> None:
    k = case["sector"][0]
    case["sector_caps"][k] = sum(case["w0"][i] for i in range(N) if case["sector"][i] == k)


EXACT_BOUNDARIES: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
    ("lower-equals-start", _lower_equal_start),
    ("upper-equals-start", _upper_equal_start),
    ("cap-equals-start", _cap_equal_start),
    ("start-sum-inside-low-side", _start_sum_within_tolerance_low),
    ("gamma-just-inside-zero", _gamma_just_inside_zero),
]


@pytest.mark.parametrize(
    ("mutate", "_valid"), [(m, v) for _, m, v in NAMED_CONDITIONS], ids=[c[0] + "-invalid" for c in NAMED_CONDITIONS]
)
def test_named_condition_is_refused_with_value_error(
    mutate: Callable[[dict[str, Any]], None], _valid: Callable[[dict[str, Any]], None]
) -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    case = changed(mutate)
    with pytest.raises(ValueError, match=r"\S"):
        sol.allocate(case)


@pytest.mark.parametrize(
    ("_mutate", "valid"), [(m, v) for _, m, v in NAMED_CONDITIONS], ids=[c[0] + "-boundary" for c in NAMED_CONDITIONS]
)
def test_named_condition_boundary_is_accepted(
    _mutate: Callable[[dict[str, Any]], None], valid: Callable[[dict[str, Any]], None]
) -> None:
    case = changed(valid)
    out = sol.allocate(case)
    output_shape(case, out)
    assert_kkt(case, out)


def _gamma_just_below_zero(case: dict[str, Any]) -> None:
    """Gamma one-millionth below zero: not positive, so refused (the boundary of the sign, from the other side)."""
    case["gamma"] = -0.000000000001


def _turnover_just_below_zero(case: dict[str, Any]) -> None:
    """A turnover limit one-trillionth below zero: negative, so refused."""
    case["turnover_limit"] = -0.000000000001


def _lower_just_above_upper(case: dict[str, Any]) -> None:
    """Asset 0: upper bound equal to the start, lower bound one-trillionth above it. The start stays inside the box
    within its tolerance, so the order of the two bounds is the only condition broken."""
    case["upper"][0] = case["w0"][0]
    case["lower"][0] = case["w0"][0] + 0.000000000001


def _lower_above_upper_last_asset(case: dict[str, Any]) -> None:
    """The order check applies to every asset, not only the first: asset n-1 has its lower bound one-trillionth above
    its upper bound, with the upper bound equal to the start so that no other condition is broken."""
    case["upper"][N - 1] = case["w0"][N - 1]
    case["lower"][N - 1] = case["w0"][N - 1] + 0.000000000001


def _cap_below_start_last_sector(case: dict[str, Any]) -> None:
    """Every sector cap is checked, not only the one of asset 0: the cap of sector K-1 lies 2e-9 below its start."""
    k = K - 1
    in_sector = sum(case["w0"][i] for i in range(N) if case["sector"][i] == k)
    case["sector_caps"][k] = in_sector - 0.000000002


def _sigma_asymmetric_last_pair(case: dict[str, Any]) -> None:
    """Symmetry is checked for every pair: the pair (n-2, n-1) is asymmetric by 1e-4."""
    case["sigma"][N - 1][N - 2] = case["sigma"][N - 2][N - 1] + 0.0001


def _sector_label_out_of_range_last_asset(case: dict[str, Any]) -> None:
    case["sector"][N - 1] = K


def _start_above_upper_last_asset(case: dict[str, Any]) -> None:
    """The starting weight of asset n-1 lies 2e-9 above its upper bound, outside the 1e-9 tolerance."""
    case["upper"][N - 1] = case["w0"][N - 1] - 0.000000002


# The other side of each named condition: the same condition, violated in the opposite direction or by a different
# count, is also refused with ValueError.
OTHER_SIDE_REFUSED: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
    ("sigma-symmetric-other-sign", _sigma_asymmetric_other_sign),
    ("sigma-positive-definite-negative", _sigma_negative_definite),
    ("sigma-positive-definite-indefinite", _sigma_indefinite),
    ("every-sector-has-an-asset-extra-cap", _sector_cap_without_assets),
    ("start-sums-to-one-low", _start_sum_low),
    ("sector-label-below-range", _sector_label_below_range),
    ("w0-one-entry-too-many", _one_entry_too_many("w0")),
    ("lower-one-entry-too-many", _one_entry_too_many("lower")),
    ("upper-one-entry-too-many", _one_entry_too_many("upper")),
    ("sector-one-entry-too-many", _one_entry_too_many("sector")),
    ("sigma-row-one-entry-too-many", _sigma_row_too_long),
    ("sigma-row-one-entry-too-few", _sigma_row_too_short),
    ("sigma-one-row-too-many", _sigma_extra_row),
    ("mu-one-entry-too-many", _one_entry_too_many("mu")),
    ("gamma-positive-just-below-zero", _gamma_just_below_zero),
    ("turnover-limit-just-below-zero", _turnover_just_below_zero),
    ("lower-over-upper-by-1e-12", _lower_just_above_upper),
    ("lower-over-upper-last-asset", _lower_above_upper_last_asset),
    ("sigma-symmetric-last-pair", _sigma_asymmetric_last_pair),
    ("sector-label-out-of-range-last-asset", _sector_label_out_of_range_last_asset),
    ("start-within-upper-last-asset", _start_above_upper_last_asset),
    ("start-within-sector-cap-last-sector", _cap_below_start_last_sector),
]


@pytest.mark.parametrize("mutate", [m for _, m in OTHER_SIDE_REFUSED], ids=[i for i, _ in OTHER_SIDE_REFUSED])
def test_named_condition_other_side_is_refused_with_value_error(mutate: Callable[[dict[str, Any]], None]) -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    with pytest.raises(ValueError, match=r"\S"):
        sol.allocate(changed(mutate))


@pytest.mark.parametrize("mutate", [m for _, m in EXACT_BOUNDARIES], ids=[i for i, _ in EXACT_BOUNDARIES])
def test_named_exact_boundary_is_accepted(mutate: Callable[[dict[str, Any]], None]) -> None:
    case = changed(mutate)
    out = sol.allocate(case)
    output_shape(case, out)
    assert_kkt(case, out)


def _poison(field: str, value: float) -> Callable[[dict[str, Any]], None]:
    def apply(case: dict[str, Any]) -> None:
        if field in ("gamma", "turnover_limit"):
            case[field] = value
        elif field == "sigma":
            case["sigma"][0][0] = value
        else:
            case[field][0] = value

    return apply


NON_FINITE_FIELDS = ("gamma", "turnover_limit", "mu", "w0", "lower", "upper", "sector_caps", "sigma")


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf], ids=["nan", "plus-infinity", "minus-infinity"])
@pytest.mark.parametrize("field", NON_FINITE_FIELDS)
def test_non_finite_value_is_refused_with_value_error(field: str, value: float) -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    with pytest.raises(ValueError, match=r"\S"):
        sol.allocate(changed(_poison(field, value)))


@pytest.mark.parametrize("field", FIELDS)
def test_missing_field_is_refused_with_value_error(field: str) -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    case = case_copy()
    del case[field]
    with pytest.raises(ValueError, match=r"\S"):
        sol.allocate(case)


def test_a_non_mapping_is_refused_with_value_error() -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    with pytest.raises(ValueError, match=r"\S"):
        not_a_mapping: Any = [PRISTINE]
        sol.allocate(not_a_mapping)


def test_no_assets_is_refused_with_value_error() -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    empty = case_copy(mu=[], w0=[], lower=[], upper=[], sector=[], sigma=[])
    with pytest.raises(ValueError, match=r"\S"):
        sol.allocate(empty)


def test_an_empty_mu_alone_is_refused_as_no_assets() -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    with pytest.raises(ValueError, match=r"\S"):
        sol.allocate(case_copy(mu=[]))


def _drop_last_entry(field: str) -> Callable[[dict[str, Any]], None]:
    def apply(case: dict[str, Any]) -> None:
        if field == "sigma":
            case["sigma"] = case["sigma"][:-1]
        else:
            case[field] = case[field][:-1]

    return apply


@pytest.mark.parametrize("field", ("w0", "lower", "upper", "sector", "sigma"))
def test_list_with_one_entry_too_few_is_refused_with_value_error(field: str) -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    with pytest.raises(ValueError, match=r"\S"):
        sol.allocate(changed(_drop_last_entry(field)))


# Other invalid inputs: the page names no exception type for these, so any exception that carries a message is
# accepted; a returned answer is not.
WRONG_TYPES: list[tuple[str, Callable[[dict[str, Any], Any], None]]] = [
    ("gamma", lambda c, v: c.__setitem__("gamma", v)),
    ("turnover_limit", lambda c, v: c.__setitem__("turnover_limit", v)),
    ("mu", lambda c, v: c["mu"].__setitem__(0, v)),
    ("sigma", lambda c, v: c["sigma"][0].__setitem__(0, v)),
    ("w0", lambda c, v: c["w0"].__setitem__(0, v)),
    ("lower", lambda c, v: c["lower"].__setitem__(0, v)),
    ("upper", lambda c, v: c["upper"].__setitem__(0, v)),
    ("sector_caps", lambda c, v: c["sector_caps"].__setitem__(0, v)),
    ("sector", lambda c, v: c["sector"].__setitem__(0, v)),
]


@pytest.mark.parametrize("bad", [True, "0.1", None], ids=["boolean", "text", "nothing"])
@pytest.mark.parametrize(("field", "poke"), WRONG_TYPES, ids=[f for f, _ in WRONG_TYPES])
def test_wrong_type_is_refused_with_an_exception(
    field: str, poke: Callable[[dict[str, Any], Any], None], bad: Any
) -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    case = case_copy()
    poke(case, bad)
    with pytest.raises(Exception, match=r"\S") as info:
        sol.allocate(case)
    assert str(info.value), f"{field}: the refusal must carry a message."


@pytest.mark.parametrize("field", ("mu", "w0", "lower", "upper", "sector", "sector_caps", "sigma"))
def test_a_number_where_a_list_belongs_is_refused_with_an_exception(field: str) -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    with pytest.raises(Exception, match=r"\S") as info:
        sol.allocate(case_copy(**{field: 0.5}))
    assert str(info.value), f"{field}: the refusal must carry a message."


def test_a_float_sector_label_is_refused_with_an_exception() -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    case = case_copy()
    case["sector"][0] = float(case["sector"][0])
    with pytest.raises(Exception, match=r"\S") as info:
        sol.allocate(case)
    assert str(info.value), "sector: the refusal must carry a message."


def test_empty_sector_caps_is_refused_with_an_exception() -> None:
    output_shape(PRISTINE, sol.allocate(case_copy()))  # control: the valid case is accepted first
    with pytest.raises(Exception, match=r"\S") as info:
        sol.allocate(case_copy(sector_caps=[]))
    assert str(info.value), "sector_caps: the refusal must carry a message."


# ---------------------------------------------------------------------------------------------------------------------
# Purity and silence
# ---------------------------------------------------------------------------------------------------------------------


def test_allocate_does_not_change_its_argument() -> None:
    case = case_copy()
    before = copy.deepcopy(case)
    sol.allocate(case)
    assert case == before, "allocate must not change the case it is given."


def test_allocate_prints_nothing_and_warns_nothing() -> None:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        sol.allocate(case_copy())
    assert buffer.getvalue() == "", "allocate must not print."
    assert not caught, "allocate must not emit warnings."


def test_the_same_case_gives_the_same_answer() -> None:
    first = sol.allocate(case_copy())
    second = sol.allocate(case_copy())
    assert first == second, "allocate must be deterministic: the same case gives the same output."
