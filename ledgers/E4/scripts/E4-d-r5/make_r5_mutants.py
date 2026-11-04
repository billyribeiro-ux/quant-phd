"""Write three verifier-authored student-error mutants of the E4 reference (round 5).

Usage: python -I make_r5_mutants.py <checkout-root>. Each mutant is the reference with one edit; the docstring's first
line names the error. The edits are asserted to match exactly once.
"""

from __future__ import annotations

import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
out_dir = root / "ledgers/E4/mutants"

edits = {
    "mutant_r5_bracket_floor_1e-12.py": (
        "Bisection starts at a lower end of 1e-12 instead of 0, so a root below 1e-12 is reported as 1e-12.",
        "        low, high = 0.0, 1.0  # invariant",
        "        low, high = 1e-12, 1.0  # invariant",
    ),
    "mutant_r5_sixty_halvings_no_tolerance.py": (
        "Bisection runs a fixed 60 halvings and never checks the relative stop rule of 1e-12 times the upper end.",
        "        while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:",
        "        while steps < 60:",
    ),
    "mutant_r5_uninformed_posterior_precision_informed.py": (
        "Uninformed posterior variance uses the informed posterior precision 1/(tau_v + tau_e) instead of 1/(tau_v + tau_y).",
        "    return math.pow(1.0 + r * r * (tau_v + tau_y) * (1.0 / tau_v + 1.0 / tau_y), -0.5)",
        "    return math.pow(1.0 + r * r * (tau_v + tau_e) * (1.0 / tau_v + 1.0 / tau_y), -0.5)",
    ),
}

for name, (doc, old, new) in edits.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new)
    first_doc_end = body.index('"""', 3) + 3
    header = f'"""{doc}\n\nVerifier mutant (E4 slice d, round 5). Built from reference.py by one edit.\n"""'
    body = header + body[first_doc_end:]
    (out_dir / name).write_text(body, encoding="utf-8")
    print("wrote", name)
