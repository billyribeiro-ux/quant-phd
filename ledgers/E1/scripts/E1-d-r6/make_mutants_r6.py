"""Write round-6 student-error mutants of the reference solution, one line changed each (ledgers/E1/mutants/)."""

from pathlib import Path
import sys

CHK = Path(sys.argv[1])
REF = (CHK / "course/modules/E/E1/grader/reference.py").read_text(encoding="utf-8")
OUT = CHK / "ledgers/E1/mutants"

MUTANTS = {
    "e1d_r6_m01_consumer_surplus_without_half.py": (
        "Consumer surplus is Q^2/b, without the one half of the triangle, so it is double the page's Q^2/(2b).",
        "    consumer = volume * volume / (2 * b)\n",
        "    consumer = volume * volume / b\n",
    ),
    "e1d_r6_m02_cournot_profit_one_exchange_share.py": (
        "Cournot profit reports one exchange's share, half the total of the two exchanges, so the total is wrong.",
        "    profit = (fee - c) * volume\n",
        '    profit = (fee - c) * volume / 2 if structure == "cournot" else (fee - c) * volume\n',
    ),
    "e1d_r6_m03_structure_substring_check.py": (
        "Structure check is a substring test, so the empty string and other fragments of a name pass as valid.",
        "    if structure not in STRUCTURES:\n",
        '    if structure not in "monopolycournotbertrand":\n',
    ),
    "e1d_r6_m04_bertrand_fee_is_maximum_fee.py": (
        "Bertrand fee is the largest fee a/b that the demand allows, not the cost c, so it is wrong for every input.",
        "        volume = d\n        fee = Fraction(c)\n",
        "        volume = d\n        fee = Fraction(a, b)\n",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new)
    text = f'"""{doc}"""\n' + body.split('"""', 2)[2].lstrip("\n")
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
