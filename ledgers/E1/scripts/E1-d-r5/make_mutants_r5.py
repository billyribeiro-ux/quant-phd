"""Write round-5 student-error mutants of the reference solution, one line changed each (ledgers/E1/mutants/)."""

from pathlib import Path
import sys

CHK = Path(sys.argv[1])
REF = (CHK / "course/modules/E/E1/grader/reference.py").read_text(encoding="utf-8")
OUT = CHK / "ledgers/E1/mutants"

MUTANTS = {
    "e1d_r5_m01_monopoly_fee_denominator_two.py": (
        "Monopoly fee (a + bc)/2 forgets the b in the denominator, so the fee is right only when b = 1.",
        "        fee = Fraction(a + b * c, 2 * b)\n",
        "        fee = Fraction(a + b * c, 2)\n",
    ),
    "e1d_r5_m02_bertrand_volume_gap_over_b.py": (
        "Bertrand volume is the gap divided by b, not the gap, so the volume is wrong for every b above 1.",
        "        volume = d\n        fee = Fraction(c)\n",
        "        volume = d / b\n        fee = Fraction(c)\n",
    ),
    "e1d_r5_m03_consumer_surplus_triangle_at_fee.py": (
        "Consumer surplus taken as a triangle with the fee as its height, fee times volume over two, not Q^2/(2b).",
        "    consumer = volume * volume / (2 * b)\n",
        "    consumer = fee * volume / 2\n",
    ),
    "e1d_r5_m04_cournot_fee_from_bertrand_formula.py": (
        "Cournot fee uses the Bertrand volume in the inverse demand, (a - d)/b, so the Cournot fee is always the cost.",
        "        fee = Fraction(a + 2 * b * c, 3 * b)\n",
        "        fee = (a - d) / b\n",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new)
    text = f'"""{doc}"""\n' + body.split('"""', 2)[2].lstrip("\n")
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
