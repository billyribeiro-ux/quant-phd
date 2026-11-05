"""Proposed tests (verifier scratch, not course content): probes of the upper-bound claim and of the 200-halving cap."""
import importlib
import math

import pytest

sol = importlib.import_module("solver")


def closed(sd: float, cost: float) -> float:
    t = 2.0 * math.exp(-4.0 * cost) - 1.0
    if t <= 0.0:
        return 0.0
    if t >= 1.0 / (1.0 + 4.0 * sd * sd):
        return 1.0
    return 2.0 * sd * math.sqrt(t / (1.0 - t))


@pytest.mark.parametrize("sd", [1e-30, 1e-40])
def test_probe_tiny_root_needs_the_200_cap(sd: float) -> None:
    lam = sol.solve_model(sd, 0.13)["informed_fraction"]
    assert abs(lam - closed(sd, 0.13)) <= 1e-8 * closed(sd, 0.13)


@pytest.mark.parametrize("sd", [10.0, 1000.0])
def test_probe_large_noise_is_accepted(sd: float) -> None:
    out = sol.solve_model(sd, 0.13)
    assert set(out) == {"informed_fraction", "price_informativeness", "indifference_gap"}


@pytest.mark.parametrize("cost", [5.0, 50.0])
def test_probe_large_cost_is_accepted(cost: float) -> None:
    out = sol.solve_model(0.6, cost)
    assert set(out) == {"informed_fraction", "price_informativeness", "indifference_gap"}
    assert out["informed_fraction"] == 0.0
