"""Verifier M5-d round 2: writes six new student-error mutants m32-m37 (ledgers/M5/mutants/) as edits of the
grader reference (course/modules/M/M5/grader/reference.py). Each replaced span must match exactly once or the
script stops. Usage, from the checkout root: .venv/bin/python ledgers/M5/scripts/M5-d-r2/make_r2_mutants.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/M/M5/grader/reference.py").read_text(encoding="utf-8")
MUT = ROOT / "ledgers/M5/mutants"

SOLVE_OLD = (
    "    values = [0.0] * len(points)\n    iterations = 0\n    certified = math.inf\n    while iterations < budget:\n"
    "        new = _sweep(beta, alpha, points, values)\n        iterations += 1\n"
    "        change = max(abs(a - b) for a, b in zip(new, values, strict=True))\n        values = new\n"
    "        certified = factor * change\n        if certified <= target:\n            break\n"
    "    return {\n        \"value\": values,\n        \"iterations\": iterations,\n"
)

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "m32_stop_reads_the_previous_certified_error.py": (
        "the stop tests the certified error of the sweep before the current one, so the solver stops one sweep late",
        [
            (
                SOLVE_OLD,
                "    values = [0.0] * len(points)\n    iterations = 0\n    certified = math.inf\n    previous = math.inf\n"
                "    while iterations < budget:\n        new = _sweep(beta, alpha, points, values)\n        iterations += 1\n"
                "        change = max(abs(a - b) for a, b in zip(new, values, strict=True))\n        values = new\n"
                "        certified, previous = factor * change, certified\n        if previous <= target:\n            break\n"
                "    return {\n        \"value\": values,\n        \"iterations\": iterations,\n",
            ),
        ],
    ),
    "m33_continuation_uses_the_current_states_value.py": (
        "the continuation term beta V(k') is replaced by beta V(k), the value of the state being solved for",
        [
            (
                "        for successor, continuation in zip(grid, values, strict=True):",
                "        for successor, continuation in zip(grid, [values[grid.index(k)]] * len(grid), strict=True):",
            ),
        ],
    ),
    "m34_value_lags_one_sweep_behind_the_certificate.py": (
        "the returned value is the vector before the last sweep, while certified_error refers to the last sweep",
        [
            (
                SOLVE_OLD,
                "    values = [0.0] * len(points)\n    iterations = 0\n    certified = math.inf\n    previous = values\n"
                "    while iterations < budget:\n        new = _sweep(beta, alpha, points, values)\n        iterations += 1\n"
                "        change = max(abs(a - b) for a, b in zip(new, values, strict=True))\n        previous = values\n"
                "        values = new\n        certified = factor * change\n        if certified <= target:\n            break\n"
                "    return {\n        \"value\": previous,\n        \"iterations\": iterations,\n",
            ),
        ],
    ),
    "m35_iterations_reported_one_fewer_when_converged.py": (
        "iterations is reported as one fewer than the sweeps made when the iteration converges",
        [
            (
                "        \"iterations\": iterations,\n",
                "        \"iterations\": iterations - 1 if certified <= target else iterations,\n",
            ),
        ],
    ),
    "m36_successor_cannot_exceed_todays_capital.py": (
        "a successor is feasible only when it does not exceed the current capital k, so capital never grows",
        [
            (
                "            if successor <= available:",
                "            if successor <= available and successor <= k:",
            ),
        ],
    ),
    "m37_strictly_increasing_check_dropped.py": (
        "the check that the grid is strictly increasing is dropped, so a decreasing grid is accepted",
        [
            (
                "    if any(points[i] >= points[i + 1] for i in range(len(points) - 1)):\n"
                "        raise ValueError(\"grid must be strictly increasing\")\n",
                "",
            ),
        ],
    ),
}


def main() -> int:
    for name, (doc, spans) in MUTANTS.items():
        text = REF
        for old, new in spans:
            count = text.count(old)
            if count != 1:
                sys.exit(f"{name}: a span matches {count} times, expected 1")
            text = text.replace(old, new, 1)
        body = text.split('"""', 2)[2]
        (MUT / name).write_text(f'"""{doc}"""' + body, encoding="utf-8")
        print("wrote", name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
