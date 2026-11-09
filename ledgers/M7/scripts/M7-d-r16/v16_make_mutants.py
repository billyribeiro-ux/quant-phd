"""Write three round-16 student-error mutants of the M7 reference into ledgers/M7/mutants/ (round-16 verifier).

Each mutant is the committed reference with one planted change at the start-snap step (reference.py:197-229), and its
docstring's first line names the student error. Run from the repository root with -I.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M7/mutants"

PLANS = {
    "v16d_01_snap_ignores_sector_caps.py": (
        "Student error v16d_01: the starting portfolio's sector caps are not repaired before the search, so a sector "
        "breach inside the starting tolerance reaches the active-set search unrepaired.",
        [
            (
                "    for k, cap in enumerate(problem.caps):\n        members = [i for i in range(n) if problem.sector[i] == k]\n        excess",
                "    for k, cap in enumerate(problem.caps[:0]):\n        members = [i for i in range(n) if problem.sector[i] == k]\n        excess",
            ),
        ],
    ),
    "v16d_02_turnover_guard_dropped_from_snap.py": (
        "Student error v16d_02: the snapped start is used even when it moves further from w0 than the turnover limit, "
        "so the search starts outside the turnover limit it is meant to respect.",
        [
            ("    return x if moved <= problem.tau else list(problem.w0)", "    return x"),
        ],
    ),
    "v16d_03_sector_excess_all_from_first_member.py": (
        "Student error v16d_03: a sector's excess over its cap is taken entirely from its first member, without checking "
        "that member's room above its lower bound, so that member can be pushed below its bound.",
        [
            (
                "        for i in members:\n            x[i] -= excess * (x[i] - problem.lower[i]) / room",
                "        x[members[0]] -= excess",
            ),
        ],
    ),
}

for name, (first_line, edits) in PLANS.items():
    text = REF
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60])
        text = text.replace(old, new)
    # the docstring's first line names the student error; the reference docstring follows it
    body = text.split('"""', 2)
    assert body[0] == "" and body[1].startswith("Reference solution")
    text = '"""' + first_line + "\n\n" + body[1] + '"""' + body[2]
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
