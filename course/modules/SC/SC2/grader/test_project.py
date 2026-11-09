"""Acceptance suite for the SC2 project: the Itô derivations engine (ito_checks.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your ito_checks.py next to this file. Warnings are failures, as in the browser.

Each test checks mathematical properties, exact invariants, numerical differentiation bounds,
or contract-pinned simulation values. Failing tests name the property violated and provide a concept hint.
They never reveal the expected numerical value.
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable, Iterator
from typing import Any

import ito_checks as sol  # type: ignore[import-not-found]
import pytest
from instance import make_instance  # type: ignore[import-not-found]

pytestmark = pytest.mark.filterwarnings("error")


@pytest.fixture(autouse=True)
def _no_stray_output(capsys: pytest.CaptureFixture[str]) -> Iterator[None]:
    """After every test, no output may have been printed by the engine."""
    yield
    expect(capsys.readouterr().out == "", "no function may print to stdout")


SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(SEED + 7_919)


def expect(condition: bool, message: str) -> None:
    """Fail with message when condition is false. The message never displays expected values."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(message)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError, but none was raised.")


def must_accept(call: Callable[[], Any], condition: str) -> Any:
    """Return call()'s value, failing if ValueError is raised on valid input."""
    __tracebackhide__ = True
    try:
        return call()
    except ValueError:
        pytest.fail(f"{condition}: valid input under the specification must not raise ValueError.")
    return None


def within(value: float, target: float, tolerance: float, message: str) -> None:
    """Fail unless |value - target| is at most the tolerance."""
    __tracebackhide__ = True
    expect(abs(value - target) <= tolerance, message)


# ---------------------------------------------------------------------------
# Instance properties
# ---------------------------------------------------------------------------


def test_make_instance_properties() -> None:
    """The instance generator must be deterministic, valid, and exhibit high variance across seeds."""
    inst_a = make_instance(SEED)
    inst_b = make_instance(SEED)
    expect(inst_a == inst_b, "make_instance must be deterministic for the same seed")
    expect(inst_a["label"] == "SIMULATED", "instance must carry label SIMULATED")
    expect(inst_a["s0"] > 0, "base GBM starting state s0 must be positive")
    expect(inst_a["sigma"] > 0, "diffusion coefficient sigma must be positive")
    expect(inst_a["kappa"] > 0, "mean-reversion speed kappa must be positive")
    expect(inst_a["H"] > 0, "horizon H must be positive")
    expect(inst_a["tbar"] > inst_a["H"], "bond maturity tbar must exceed horizon H")

    sigmas = {make_instance(s)["sigma"] for s in range(50)}
    expect(len(sigmas) >= 45, "seeds 0-49 must generate at least 45 distinct sigma parameters")


# ---------------------------------------------------------------------------
# Transform values and boundary validation
# ---------------------------------------------------------------------------


def test_value_evaluations() -> None:
    """The transform function value() must match the closed-form definitions at interior points."""
    t_val = 0.5 * float(INST["H"])

    # Transform 1: log(x)
    within(sol.value("1", t_val, 1.5, INST), math.log(1.5), 1e-12, "transform 1 must compute log(x)")

    # Transform 2: x^p
    p = float(INST["p"])
    within(sol.value("2", t_val, 1.5, INST), 1.5**p, 1e-12, "transform 2 must compute x^p")

    # Transform 3: 1/x
    within(sol.value("3", t_val, 2.0, INST), 0.5, 1e-12, "transform 3 must compute 1/x")

    # Transform 4: exp(-r*t)*x
    r = float(INST["r"])
    within(
        sol.value("4", t_val, 1.2, INST),
        math.exp(-r * t_val) * 1.2,
        1e-12,
        "transform 4 must compute discounted state",
    )

    # Transform 5: x / (a + x)
    a = float(INST["a"])
    within(sol.value("5", t_val, 1.0, INST), 1.0 / (a + 1.0), 1e-12, "transform 5 must compute x / (a + x)")

    # Transform 6: c + b*x
    b = float(INST["b"])
    c = float(INST["c"])
    within(sol.value("6", t_val, 0.4, INST), c + b * 0.4, 1e-12, "transform 6 must compute c + b*x")

    # Transform 7: x^2
    within(sol.value("7", t_val, -0.8, INST), 0.64, 1e-12, "transform 7 must compute x^2")

    # Transform 8: exp(x)
    within(sol.value("8", t_val, 0.3, INST), math.exp(0.3), 1e-12, "transform 8 must compute exp(x)")

    # Transform 10: exp(kappa*t)*x
    kappa = float(INST["kappa"])
    within(
        sol.value("10", t_val, 0.5, INST),
        math.exp(kappa * t_val) * 0.5,
        1e-12,
        "transform 10 must compute exp(kappa*t)*x",
    )


def test_value_domain_validation() -> None:
    """value() must enforce positive domain x > 0 for GBM transforms 1-5 and reject unknown transforms."""
    must_raise(lambda: sol.value("unknown", 0.0, 1.0, INST), "unknown transform name")
    must_raise(lambda: sol.value("11", 0.0, 1.0, INST), "transform index out of bounds")

    def check_val(tid: str, x: float) -> Callable[[], Any]:
        return lambda: sol.value(tid, 0.0, x, INST)

    for t_id in ("1", "2", "3", "4", "5"):
        must_raise(check_val(t_id, 0.0), f"transform {t_id} at x=0")
        must_raise(check_val(t_id, -0.1), f"transform {t_id} at x=-0.1")
        must_accept(check_val(t_id, 1e-9), f"transform {t_id} at x=1e-9")

    # Transforms 6-10 accept x <= 0
    for t_id in ("6", "7", "8", "9", "10"):
        must_accept(check_val(t_id, 0.0), f"transform {t_id} at x=0")
        must_accept(check_val(t_id, -0.5), f"transform {t_id} at x=-0.5")


# ---------------------------------------------------------------------------
# Itô coefficients: exact invariants & numerical differentiation
# ---------------------------------------------------------------------------


def test_coefficients_exact_invariants() -> None:
    """The drift and diffusion coefficients must satisfy exact analytical identities."""
    mu = float(INST["mu"])
    sigma = float(INST["sigma"])
    kappa = float(INST["kappa"])
    theta = float(INST["theta"])
    b = float(INST["b"])

    # Transform 1: Y = log S has constant drift (mu - sigma^2/2) and constant diffusion sigma
    m1, s1 = sol.coefficients("1", 0.0, 1.0, INST)
    within(s1, sigma, 1e-12, "log-price diffusion must equal sigma exactly")
    within(m1, mu - 0.5 * sigma * sigma, 1e-12, "log-price drift must equal mu - sigma^2/2 exactly")

    # Transform 6: affine OU Y = c + b*X has diffusion b*sigma and drift b*kappa*(theta - x)
    x_test = 0.25
    m6, s6 = sol.coefficients("6", 0.0, x_test, INST)
    within(s6, b * sigma, 1e-12, "affine OU diffusion must equal b*sigma exactly")
    within(m6, b * kappa * (theta - x_test), 1e-12, "affine OU drift must equal b*kappa*(theta - x) exactly")

    # Transform 10: Y = exp(kappa*t)*X has drift kappa*theta*exp(kappa*t) and diffusion sigma*exp(kappa*t)
    t_test = 0.5 * float(INST["H"])
    m10, s10 = sol.coefficients("10", t_test, x_test, INST)
    ekt = math.exp(kappa * t_test)
    within(s10, sigma * ekt, 1e-12, "time-scaled OU diffusion must equal sigma*exp(kappa*t)")
    within(m10, kappa * theta * ekt, 1e-12, "time-scaled OU drift must equal kappa*theta*exp(kappa*t)")


def test_coefficients_numerical_ito_agreement() -> None:
    """All 10 transforms must match Itô's formula via numerical differentiation of value()."""
    h = 1e-5
    t = 0.3 * float(INST["H"])

    mu = float(INST["mu"])
    sigma = float(INST["sigma"])
    kappa = float(INST["kappa"])
    theta = float(INST["theta"])

    for tid in range(1, 11):
        t_key = str(tid)
        x = 1.2 if tid <= 5 else 0.2

        # Base drift and diffusion
        if tid <= 5:
            a_base = mu * x
            b_base = sigma * x
        else:
            a_base = kappa * (theta - x)
            b_base = sigma

        # Numerical partial derivatives
        f_mid = sol.value(t_key, t, x, INST)
        f_t_plus = sol.value(t_key, t + h, x, INST)
        f_t_minus = sol.value(t_key, t - h, x, INST)
        df_dt = (f_t_plus - f_t_minus) / (2.0 * h)

        f_x_plus = sol.value(t_key, t, x + h, INST)
        f_x_minus = sol.value(t_key, t, x - h, INST)
        df_dx = (f_x_plus - f_x_minus) / (2.0 * h)
        d2f_dx2 = (f_x_plus - 2.0 * f_mid + f_x_minus) / (h * h)

        expected_drift = df_dt + a_base * df_dx + 0.5 * (b_base**2) * d2f_dx2
        expected_diff = b_base * df_dx

        cand_drift, cand_diff = sol.coefficients(t_key, t, x, INST)
        tol_drift = 1e-5 * max(1.0, abs(expected_drift))
        tol_diff = 1e-5 * max(1.0, abs(expected_diff))

        within(cand_drift, expected_drift, tol_drift, f"transform {t_key} drift violates Itô's lemma formula")
        within(cand_diff, expected_diff, tol_diff, f"transform {t_key} diffusion violates Itô's lemma formula")


def test_coefficients_validation() -> None:
    """coefficients() must validate transform names and positive states for GBM."""
    must_raise(lambda: sol.coefficients("invalid", 0.0, 1.0, INST), "unknown transform name")
    must_raise(lambda: sol.coefficients("1", 0.0, 0.0, INST), "x = 0 for transform 1")
    must_accept(lambda: sol.coefficients("1", 0.0, 1e-9, INST), "x = 1e-9 for transform 1")


# ---------------------------------------------------------------------------
# Itô residuals: exact cases, statistical bands, and pinned fixture
# ---------------------------------------------------------------------------


def test_residual_exact_invariants() -> None:
    """Transforms 1 and 6 must exhibit zero residual pathwise under their exact discrete dynamics."""
    # Transform 1 on exact GBM base has pathwise residual identically zero
    mean1, _ = sol.residual("1", INST, int(INST["n_steps"]))
    within(mean1, 0.0, 1e-10, "transform 1 residual mean must vanish pathwise")

    # Transform 6 on Euler OU base has pathwise residual identically zero
    mean6, _ = sol.residual("6", INST, int(INST["n_steps"]))
    within(mean6, 0.0, 1e-10, "transform 6 residual mean must vanish pathwise")


def test_residual_pinned_fixture_seed0() -> None:
    """On seed 0, transform 7 residual must reproduce the pinned reference numbers exactly."""
    if SEED != 0:
        return
    # Pinned values from lab-SC2-project-3 (seed 0 contract)
    target_mean = -6.0421482183347994e-05
    target_se = 4.397907245216925e-05

    mean7, se7 = sol.residual("7", INST, int(INST["n_steps"]))
    within(mean7, target_mean, 1e-11, "seed 0 transform 7 residual mean violates draw-order contract")
    within(se7, target_se, 1e-11, "seed 0 transform 7 standard error violates draw-order contract")


def test_residual_statistical_bands() -> None:
    """Residual means for nonlinear transforms must lie within 5 standard errors plus discretization allowance."""
    n_steps = int(INST["n_steps"])
    discretization_allowance = 0.05

    for tid in ("2", "3", "4", "5", "7", "8", "9", "10"):
        mean_res, se_res = sol.residual(tid, INST, n_steps)
        band = 5.0 * se_res + discretization_allowance
        expect(
            abs(mean_res) <= band,
            f"transform {tid} residual mean exceeded 5*se + allowance (bias or formula defect)",
        )


def test_residual_validation() -> None:
    """residual() must reject invalid transform names, n_steps < 1, and n_paths < 2."""
    must_raise(lambda: sol.residual("bad_id", INST, 16), "unknown transform")
    must_raise(lambda: sol.residual("1", INST, 0), "n_steps = 0")
    must_accept(lambda: sol.residual("1", INST, 1), "n_steps = 1")

    inst_one_path = {**INST, "n_paths": 1}
    must_raise(lambda: sol.residual("1", inst_one_path, 16), "n_paths = 1")

    inst_two_paths = {**INST, "n_paths": 2}
    must_accept(lambda: sol.residual("1", inst_two_paths, 16), "n_paths = 2")
