"""Verifier M5-d round 1: writes three new student-error mutants (ledgers/M5/mutants/m15-m21) and three
alternative correct implementations (scratch /tmp/M5-v/d/alt). Each mutant is the grader reference with one
replaced span; every replacement must match exactly once or the script stops.

Usage, from the checkout root: .venv/bin/python ledgers/M5/scripts/M5-d-r1/make_d_variants.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/M/M5/grader/reference.py").read_text(encoding="utf-8")
MUT = ROOT / "ledgers/M5/mutants"
ALT = Path("/tmp/M5-v/d/alt")

MUTANTS: dict[str, tuple[str, str, str]] = {
    "m15_feasibility_strict_drops_the_tie_k_prime_equal_resources.py": (
        "feasibility uses a strict inequality, so a successor equal to k**alpha (zero consumption) is refused",
        "            if successor <= available:",
        "            if successor < available:",
    ),
    "m16_iteration_starts_from_ones_not_zero.py": (
        "the iteration starts from the vector of ones instead of the zero vector V_0 = 0",
        "    values = [0.0] * len(points)\n    iterations = 0",
        "    values = [1.0] * len(points)\n    iterations = 0",
    ),
    "m17_sweep_budget_ignored.py": (
        "the solver ignores max_iter and iterates until the certified error is within tol",
        "    while iterations < budget:",
        "    while True:",
    ),
    "m18_converged_strictly_below_tol.py": (
        "converged and the stop use a strict inequality, so a certified error exactly equal to tol is not accepted",
        "        if certified <= target:\n            break",
        "        if certified < target:\n            break",
    ),
    "m19_operator_overwrites_the_callers_values.py": (
        "bellman_operator writes its image into the caller's values list before returning it",
        "    return _sweep(beta, alpha, points, _values(values, len(points)))",
        "    image = _sweep(beta, alpha, points, _values(values, len(points)))\n    values[:] = image\n    return image",
    ),
    "m20_utility_linear_in_consumption.py": (
        "utility is the consumption itself instead of its square root, so the utility of c is c",
        "best = max(best, math.sqrt(available - successor) + beta * continuation)",
        "best = max(best, (available - successor) + beta * continuation)",
    ),
    "m21_feasibility_tests_the_state_not_the_successor.py": (
        "the feasibility test compares the current capital k with the resources instead of the successor k'",
        "            if successor <= available:",
        "            if k <= available:",
    ),
}


def write_mutants() -> None:
    for name, (doc, old, new) in MUTANTS.items():
        if REF.count(old) != 1:
            sys.exit(f"{name}: the span matches {REF.count(old)} times, expected 1")
        body = REF.split('"""', 2)[2]  # drop the reference module docstring
        text = f'"""{doc}"""' + body
        text = text.replace(old, new, 1)
        (MUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)


def write_alternatives() -> None:
    ALT.mkdir(parents=True, exist_ok=True)
    base = REF.replace("from __future__ import annotations", "from __future__ import annotations")
    # A: different numerical cutoff (relative 1e-12) and a precomputed feasible-index table.
    a = base.replace(
        "        available = k**alpha\n        best = -math.inf\n        for successor, continuation in zip(grid, values, strict=True):\n            if successor <= available:\n                best = max(best, math.sqrt(available - successor) + beta * continuation)\n        out.append(best)",
        "        available = k**alpha\n        table = [j for j, s in enumerate(grid) if s <= available * (1 + 1e-12)]\n        out.append(max(math.sqrt(max(available - grid[j], 0.0)) + beta * values[j] for j in table))",
    )
    assert a != base
    (ALT / "altA_relative_cutoff_index_table.py").write_text(a, encoding="utf-8")
    # B: a different valid certified bound: the a priori-style bound beta**n / (1 - beta) * ||V_1 - V_0||,
    # which the page allows ("another is any bound your proof establishes").
    b = base.replace(
        "    factor = beta / (1 - beta)\n    values = [0.0] * len(points)\n    iterations = 0\n    certified = math.inf\n    while iterations < budget:\n        new = _sweep(beta, alpha, points, values)\n        iterations += 1\n        change = max(abs(a - b) for a, b in zip(new, values, strict=True))\n        values = new\n        certified = factor * change",
        "    values = [0.0] * len(points)\n    iterations = 0\n    certified = math.inf\n    first_change = None\n    while iterations < budget:\n        new = _sweep(beta, alpha, points, values)\n        iterations += 1\n        change = max(abs(a - b) for a, b in zip(new, values, strict=True))\n        if first_change is None:\n            first_change = change\n        values = new\n        certified = beta**iterations / (1 - beta) * first_change",
    )
    assert b != base
    (ALT / "altB_apriori_geometric_bound.py").write_text(b, encoding="utf-8")
    # C: a different loop structure: a fixed-length sweep that builds the successor list once and uses the
    # sorted order with an explicit reverse traversal of the maxima.
    c = base.replace(
        "    out: list[float] = []\n    for k in grid:\n        available = k**alpha\n        best = -math.inf\n        for successor, continuation in zip(grid, values, strict=True):\n            if successor <= available:\n                best = max(best, math.sqrt(available - successor) + beta * continuation)\n        out.append(best)\n    return out",
        "    out: list[float] = []\n    for k in grid:\n        available = k**alpha\n        cands = [(math.sqrt(available - grid[j]) + beta * values[j]) for j in range(len(grid)) if grid[j] <= available]\n        cands.sort(reverse=True)\n        out.append(cands[0])\n    return out",
    )
    assert c != base
    (ALT / "altC_sorted_candidates.py").write_text(c, encoding="utf-8")
    print("wrote alternatives A, B, C")


if __name__ == "__main__":
    write_mutants()
    write_alternatives()
