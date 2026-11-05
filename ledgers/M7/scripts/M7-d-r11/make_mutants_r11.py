"""Write round-11 student-error mutants of the M7 reference into ledgers/M7/mutants/.

Each mutant is reference.py with exactly one replacement; every replacement must match exactly once.
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
REF = ROOT / "course/modules/M/M7/grader/reference.py"
OUT = ROOT / "ledgers/M7/mutants"
src = REF.read_text(encoding="utf-8")
OPEN = '"""Reference solution for the M7 constrained allocator (constrained_allocator.py): an exact active-set solver.\n'
assert src.count(OPEN) == 1

MUTANTS = {
    "r11_01_turnover_multipliers_are_positive_and_negative_parts_of_net.py": (
        "Student error: the turnover multipliers are split as the positive and negative parts of the net sign multiplier "
        "(plus = max(net, 0), minus = max(-net, 0)) instead of (kappa +/- net) / 2, so kappa - plus - minus is not zero.",
        [
            ("        plus[i] = (kappa + net) / 2\n        minus[i] = (kappa - net) / 2\n",
             "        plus[i] = max(net, Fraction(0))\n        minus[i] = max(-net, Fraction(0))\n"),
        ],
    ),
    "r11_03_vertex_working_set_rejected_as_an_error.py": (
        "Student error: the solver raises once the working set holds n - 1 inequality rows (a vertex, with the budget), "
        "so every answer that the bounds pin to a vertex is refused.",
        [
            ("        gradient = [_dot(hessian[i], x) - problem.mu[i] for i in range(n)]\n",
             "        if len(working) >= n - 1:\n            raise ValueError('vertex working set is not supported')\n"
             "        gradient = [_dot(hessian[i], x) - problem.mu[i] for i in range(n)]\n"),
        ],
    ),
    "r11_05_turnover_sign_forms_only_half_the_orthants.py": (
        "Student error: the turnover limit is enforced only through the 2**(n-1) sign forms whose first entry is +1, so the "
        "sign constraints of the other orthants are never imposed.",
        [
            ("    for signs in product((1, -1), repeat=n):\n",
             "    for signs in (s for s in product((1, -1), repeat=n) if s[0] == 1):\n"),
        ],
    ),
    "r11_06_sector_caps_assigned_to_sectors_in_reverse_order.py": (
        "Student error: the sector caps are read in reverse order, so sector k is bounded by the cap of sector Z-1-k.",
        [
            ("    for k, cap in enumerate(problem.caps):\n        rows.append(",
             "    for k, cap in enumerate(reversed(problem.caps)):\n        rows.append("),
        ],
    ),
}

for name, (description, replacements) in MUTANTS.items():
    text = src.replace(OPEN, f'"""{description}\n', 1)
    for old, new in replacements:
        count = text.count(old)
        assert count == 1, (name, count, old[:60])
        text = text.replace(old, new, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
