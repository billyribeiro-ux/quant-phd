"""Pytest module ensuring all 5 alternative implementations pass across seeds 0 to 49."""

from __future__ import annotations

import math
import statistics
import sys
from typing import Any

import pytest

from coursekit import ROOT

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "course" / "modules" / "S" / "S1" / "grader"))
from instance import make_instance  # type: ignore[import-not-found]
from tests.graders.S1 import alt_1, alt_2, alt_3, alt_4, alt_5

ALTERNATIVES = [alt_1, alt_2, alt_3, alt_4, alt_5]


@pytest.mark.parametrize("alt_idx,alt", enumerate(ALTERNATIVES, start=1))
@pytest.mark.parametrize("seed", range(50))
def test_alternative_passes_instance(alt_idx: int, alt: Any, seed: int) -> None:
    inst = make_instance(seed)
    sr_ann = inst["sr_ann"]
    k = inst["periods_per_year"]
    alpha = inst["alpha"]
    power = inst["power"]
    returns = inst["returns"]

    # 1. sharpe_hat
    n = len(returns)
    mean_val = sum(returns) / n
    var_val = sum((r - mean_val) ** 2 for r in returns) / (n - 1)
    expected_hsr = mean_val / math.sqrt(var_val)
    actual_hsr = alt.sharpe_hat(returns)
    assert abs(actual_hsr - expected_hsr) < 1e-10 * max(1.0, abs(expected_hsr))

    # 2. analytic_years
    years = alt.analytic_years(sr_ann, k, alpha, power)
    assert isinstance(years, float)
    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha)
    t_periods = years * k
    sr_p = sr_ann / math.sqrt(k)
    inflation = math.sqrt(1.0 + (sr_p**2) / 2.0)
    z_stat = (z_alpha - math.sqrt(t_periods) * sr_p) / inflation
    solved_power = 1.0 - dist.cdf(z_stat)
    assert abs(solved_power - power) < 1e-7

    # 3. required_periods
    req_t = alt.required_periods(sr_ann, k, alpha, power)
    assert isinstance(req_t, int)
    assert req_t == math.ceil(years * k)

    # 4. simulated_power
    sim_power = alt.simulated_power(req_t, sr_p, alpha, n_sims=1000, seed=seed + 300)
    se = math.sqrt(power * (1.0 - power) / 1000)
    band = 4.0 * se + 0.035
    assert abs(sim_power - power) <= band
