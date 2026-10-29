"""Write round-12 student-error mutants of the FC1 reference into ledgers/FC1/mutants/.

Each mutant is the reference with one string replacement; the script asserts that every replacement matched once.
Run from the checkout root: python3 ledgers/FC1/scripts/FC1-c-r12/make_mutants.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/FC/FC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/FC1/mutants"

MUTANTS = {
    "r12n01_face_as_separate_event_same_period.py": (
        "Student error: Bond.events() appends the face as a second event in the last period instead of adding it to "
        "the coupon event, which the page's events rule forbids (the face is in the same event).",
        [
            (
                "        last_period, last_amount = out[-1]\n        out[-1] = (last_period, last_amount + self.face_cents)\n",
                "        last_period, last_amount = out[-1]\n        out.append((last_period, self.face_cents))\n",
            ),
        ],
    ),
    "r12n02_exponent_is_list_position.py": (
        "Student error: bond_price_cents discounts the k-th event by (1 + y) ** k, counting events from 0, not by its "
        "own period t as the page's discounting rule requires.",
        [
            (
                "    for period, amount in bond.events():\n        total += Fraction(amount) / (1 + y) ** period\n",
                "    for index, (_period, amount) in enumerate(bond.events()):\n        total += Fraction(amount) / (1 + y) ** index\n",
            ),
        ],
    ),
    "r12n03_float_discounting_then_half_up.py": (
        "Student error: bond_price_cents discounts in floats and rounds the float sum half up, not from exact Fractions "
        "as the page's money convention requires.",
        [
            (
                "    y = Fraction(rate, 10_000)\n    total = Fraction(0)\n    for period, amount in bond.events():\n"
                "        total += Fraction(amount) / (1 + y) ** period\n    return _half_away(total)\n",
                "    y = rate / 10_000\n    total = 0.0\n    for period, amount in bond.events():\n"
                "        total += amount / (1 + y) ** period\n    return int(total + 0.5) if total >= 0 else -int(-total + 0.5)\n",
            ),
        ],
    ),
}

for name, (description, replacements) in MUTANTS.items():
    text = REF
    for old, new in replacements:
        assert text.count(old) == 1, f"{name}: replacement target found {text.count(old)} times"
        text = text.replace(old, new)
    module = text.replace('"""Reference solution', '"""' + description + '\n\nReference solution', 1)
    (OUT / name).write_text(module, encoding="utf-8")
    print("wrote", name)
