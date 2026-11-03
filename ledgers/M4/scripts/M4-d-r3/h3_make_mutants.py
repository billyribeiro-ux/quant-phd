"""Verifier round-3 (M4-d, independent verifier h3): writes four student-error mutants of the M4 reference.

Each mutant is the reference with exactly one edit; every edit must match the reference exactly once.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = ROOT / "course/modules/M/M4/grader/reference.py"
OUT = ROOT / "ledgers/M4/mutants"

EDITS = {
    "v7_01_chi_square_drawn_per_position": (
        "Verifier round-3 student-error mutant (v7). Student-t draws one chi-square variable per position, not one per draw, so the assets of a draw get different scales.",
        """        scale = 1.0
        if student and nu is not None:
            chi_square = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched * nu / chi_square)
        total = 0.0
        for i in range(n):
            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))
""",
        """        scale = 1.0
        total = 0.0
        for i in range(n):
            if student and nu is not None:
                chi_square = rng.gammavariate(nu / 2, 2.0)
                scale = math.sqrt(matched * nu / chi_square)
            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))
""",
    ),
    "v7_02_quantile_index_floor_plus_one": (
        "Verifier round-3 student-error mutant (v7). The 99% index is floor(0.99 n) + 1, one order statistic high whenever 0.99 n is a whole number (n = 100, 200).",
        "    index = (99 * len(losses_cents) + 99) // 100\n",
        "    index = (99 * len(losses_cents)) // 100 + 1\n",
    ),
    "v7_03_loss_rounded_per_position": (
        "Verifier round-3 student-error mutant (v7). Each position's cent amount is rounded before the sum, so the portfolio loss is rounded per position, not once.",
        """            total += position_cents[i] * ret
        losses.append(round(-total))
""",
        """            total += round(position_cents[i] * ret)
        losses.append(-int(total))
""",
    ),
    "v7_04_chi_square_scale_one": (
        "Verifier round-3 student-error mutant (v7). The chi-square draw uses scale 1 instead of 2, so W has half its stated mean nu and the Student-t factor is wrong.",
        "            chi_square = rng.gammavariate(nu / 2, 2.0)\n",
        "            chi_square = rng.gammavariate(nu / 2, 1.0)\n",
    ),
}

ref = REF.read_text(encoding="utf-8")
OUT.mkdir(parents=True, exist_ok=True)
for name, (doc, old, new) in EDITS.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new, 1)
    head, sep, rest = body.partition('"""')
    assert sep, name
    _, sep2, tail = rest.partition('"""')
    assert sep2, name
    body = f'"""{doc}\n\nMutant of the M4 reference (tail_risk.py). All inputs are SIMULATED.\n"""' + tail
    (OUT / f"{name}.py").write_text(body, encoding="utf-8")
    print("wrote", name)
