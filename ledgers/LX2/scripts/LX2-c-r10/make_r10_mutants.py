"""Generate round-10 lab-2 student-error mutants and correct alternatives from the twin (round 10, slice c).

Each file is the completed twin with (a) its long docstring replaced by one line that names the mutation, and
(b) one targeted substitution. Every substitution is asserted to match exactly once, so no mutant is a no-op.
Run from the checkout root: python -I -W error ledgers/LX2/scripts/LX2-c-r10/make_r10_mutants.py
"""

import pathlib
import re

ROOT = pathlib.Path(".")
TWIN = (ROOT / "tests/labs/LX2/lab-LX2-project-2.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/LX2/mutants"

# The completed twin has the expected code on its hit-rate and bias lines (the page shows ___ there).
COMPLETED_HIT = "    hit_rate = Fraction(hits, horizon)"
COMPLETED_BIAS = "    bias = Fraction(sum(errors), horizon)"
assert TWIN.count(COMPLETED_HIT) == 1 and TWIN.count(COMPLETED_BIAS) == 1

MUTANTS = {
    "r10_lab2_hit_rate_integer_division": (
        "Student error (hit rate): the hit count is divided with integer division, so the hit rate prints 0.0000.",
        [(COMPLETED_HIT, "    hit_rate = Fraction(hits // horizon, 1)")],
    ),
    "r10_lab2_edge_list_prints_all_hits": (
        "Student error (Part D): the edge list prints every hit month instead of the months at |error| = 2.",
        [("    edge = [START_MONTH + i for i, e in enumerate(errors) if abs(e) == HIT_BAND]",
          "    edge = [START_MONTH + i for i, e in enumerate(errors) if abs(e) <= HIT_BAND]")],
    ),
    "r10_lab2_bias_subtracts_hit_count": (
        "Student error (bias): the hit count is subtracted from the error sum before dividing by H.",
        [(COMPLETED_BIAS, "    bias = Fraction(sum(errors) - hits, horizon)")],
    ),
    "r10_lab2_bias_absolute_value_of_sum_per_H": (
        "Student error (sign convention): the bias takes the absolute value of the error sum.",
        [(COMPLETED_BIAS, "    bias = Fraction(abs(sum(errors)), horizon)")],
    ),
}

# Correct alternatives: must SURVIVE the whole-block compare.
ALTERNATIVES = {
    "alt_r10_lab2_squared_error_band": (
        "Alternative (correct): the hit test compares the squared error with 4, which is the same band.",
        [("    return abs(predicted - realised) <= HIT_BAND", "    return (predicted - realised) ** 2 <= HIT_BAND * HIT_BAND")],
    ),
    "alt_r10_lab2_decimal_half_up_quantize": (
        "Alternative (correct): the printed values use Decimal quantize with ROUND_HALF_UP on the exact value.",
        [
            ("def decimal_text(value: Fraction, places: int) -> str:",
             "from decimal import ROUND_HALF_UP, Decimal\n\n\ndef decimal_text(value: Fraction, places: int) -> str:\n"
             "    q = (Decimal(value.numerator) / Decimal(value.denominator)).quantize(\n"
             "        Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)\n"
             "    return format(q, f\".{places}f\")\n\n\ndef _unused(value: Fraction, places: int) -> str:"),
        ],
    ),
}


def build(name: str, description: str, subs: list[tuple[str, str]]) -> str:
    text = TWIN
    body_start = text.index('"""', text.index('"""') + 3) + 3  # end of the long docstring
    text = f'"""{description}"""' + text[body_start:]
    for old, new in subs:
        n = text.count(old)
        assert n == 1, (name, old, n)
        text = text.replace(old, new)
    return text


for name, (desc, subs) in {**MUTANTS, **ALTERNATIVES}.items():
    (OUT / f"{name}.py").write_text(build(name, desc, subs), encoding="utf-8")
    print("wrote", name)
