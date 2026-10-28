"""Writes the round-6 student-error mutants (m36-m40) from the reference engine by one textual edit each.

Run: python3 ledgers/CF1/scripts/CF1-d-r6/make_mutants_r6.py <checkout>. Each mutant is a complete module whose first line
is a one-line docstring naming the error. Every edit must match exactly once, or the script stops.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = ROOT / "course/modules/CF/CF1/grader/reference.py"
OUT = ROOT / "ledgers/CF1/mutants"
DOC_OLD = '''"""Reference solution for the CF1 capital-budgeting engine (capbudget.py).

Standard library only. Money is whole cents on input; every derived cash flow is a float in cents and is not rounded.
This file is the instructor's solution. It is excluded from publication; the suite never imports it.
"""'''

MUTANTS = {
    "m36_window_low_end_extended_to_one_millionth.py": (
        "The IRR search window is extended at its low end to discount factor 1e-6, so a root at rate 99999, outside the "
        "specified window, is reported.",
        [("_X_LOW, _X_HIGH = 1e-4, 1e4", "_X_LOW, _X_HIGH = 1e-6, 1e4")],
    ),
    "m37_zero_samples_counted_as_sign_changes.py": (
        "The sign-change test uses <= 0, so a grid sample that is exactly zero (a tangent point at x = 1) is reported "
        "as a root.",
        [("if values[k1] * values[k2] < 0.0:", "if values[k1] * values[k2] <= 0.0:"),
         ("nonzero = [k for k in range(_GRID_POINTS) if values[k] != 0.0]",
          "nonzero = list(range(_GRID_POINTS))")],
    ),
    "m38_bisection_absolute_tolerance_in_discount_factor.py": (
        "The root bisection stops when the bracket is within 1e-7 in the discount factor x, not relative to x, so the "
        "rate error near rate 6666 is several units.",
        [("if hi - lo <= 1e-15 * hi:", "if hi - lo <= 1e-7:")],
    ),
    "m39_discounted_payback_fraction_uses_undiscounted_flow.py": (
        "Discounted payback accumulates discounted flows but divides the recovery fraction by the undiscounted flow.",
        [("return (t - 1) + (-cumulative) / discounted[t]",
          "return (t - 1) + (-cumulative) / flows[t]")],
    ),
    "m40_capex_float_accepted.py": (
        "A capex given as a float such as 1000.0 is accepted, so the integer-cents rule is not enforced.",
        [("if not isinstance(capex, int) or isinstance(capex, bool) or capex <= 0:",
          "if not _finite(capex) or capex <= 0:")],
    ),
}


def main() -> None:
    src = REF.read_text(encoding="utf-8")
    if src.count(DOC_OLD) != 1:
        raise SystemExit("reference docstring not found exactly once")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (doc, edits) in MUTANTS.items():
        text = src.replace(DOC_OLD, f'"""{doc}"""')
        for old, new in edits:
            if text.count(old) != 1:
                raise SystemExit(f"{name}: edit anchor count {text.count(old)} for {old!r}")
            text = text.replace(old, new)
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
