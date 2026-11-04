"""Find a waterfall input (integer cents above 2**53 range) where float division differs from integer floor (BK4-c r1).

Run: .venv/bin/python ledgers/BK4/scripts/BK4-c-r1/float_probe.py
Prints the exact survivor payments (integer arithmetic) and the float-based payments for the same input.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course" / "modules" / "BK" / "BK4" / "grader"))
import reference as ref  # noqa: E402

R = 6_585_696_953_829_388
FUND_1 = 585_467_024_498_971
FUND_2 = 7_278_398_114_431_529 - FUND_1
margins = {1: 0, 2: 0, 3: 0}
funds = {1: FUND_1, 2: FUND_2, 3: 0}
exact = ref.waterfall(R, 3, margins, funds, 0)
float_share = {m: int(R * funds[m] / (FUND_1 + FUND_2)) for m in (1, 2)}
print("reference survivor payments:", exact.survivor_cents, "uncovered", exact.uncovered_cents)
print("float share before leftover:", float_share)
print("exact share before leftover:", {m: R * funds[m] // (FUND_1 + FUND_2) for m in (1, 2)})
print("float-based sum:", sum(float_share.values()), "residual", R, "reference sum:", sum(exact.survivor_cents.values()))
