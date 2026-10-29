"""Alternative A7 (plan 6.5 item 4, float money): exact Fraction probabilities, expectation rounded from a float."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any



def doubling_outcome(instance: dict[str, Any]) -> dict[str, int | Fraction]:
    out = dict(exact_outcome(instance))
    out["expected_final_wealth_cents"] = math.floor(float(out["win_probability"]) * (int(instance["capital_cents"]) + int(instance["base_stake_cents"])) + float(out["ruin_probability"]) * int(out["wealth_on_ruin_cents"]) + 0.5)
    return out
