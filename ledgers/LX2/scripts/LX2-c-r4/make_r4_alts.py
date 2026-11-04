"""LX2-c round 4: writes three correct alternative implementations of the rung-2 completion lab into scripts/LX2-c-r4/alts/.

Each must print the page's expected block exactly (checked by page_vs_twin_r4.py and lab2_r4_check.py); they are
over-constraint probes, not mutants, so they are not written under ledgers/LX2/mutants/.
Run from the checkout root: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r4/make_r4_alts.py
"""

from pathlib import Path

ROOT = Path.cwd()
TWIN = (ROOT / "tests/labs/LX2/lab-LX2-project-2.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/LX2/scripts/LX2-c-r4/alts"
OUT.mkdir(parents=True, exist_ok=True)

OLD_DECIMAL = (
    '    scale = 10**places\n'
    '    magnitude = math.floor(abs(value) * scale + Fraction(1, 2))\n'
    '    sign = "-" if value < 0 and magnitude != 0 else ""\n'
    '    whole, part = divmod(magnitude, scale)\n'
)
assert TWIN.count(OLD_DECIMAL) == 1

ALTS = {
    # 1. integer half-up on numerator and denominator (no Fraction rounding, no float)
    "alt_integer_half_up.py": [
        (
            OLD_DECIMAL,
            '    scale = 10**places\n'
            '    num, den = value.numerator, value.denominator\n'
            '    magnitude = (2 * abs(num) * scale + den) // (2 * den)\n'
            '    sign = "-" if value < 0 and magnitude != 0 else ""\n'
            '    whole, part = divmod(magnitude, scale)\n',
        ),
    ],
    # 2. decimal module, ROUND_HALF_UP on the exact quotient
    "alt_decimal_half_up.py": [
        (
            OLD_DECIMAL,
            '    from decimal import ROUND_HALF_UP, Decimal\n'
            '    q = (Decimal(value.numerator) / Decimal(value.denominator)).quantize(\n'
            '        Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP\n'
            '    )\n'
            '    return format(q, f".{places}f")\n'
            '    scale = 10**places\n'
            '    magnitude = 0\n'
            '    sign = ""\n'
            '    whole, part = divmod(magnitude, scale)\n',
        ),
    ],
    # 3. a class holds the window; the two measures are methods on it (same printed output)
    "alt_class_window.py": [
        (
            "def main() -> None:\n",
            "class Window:\n"
            "    def __init__(self, errors: list[int]) -> None:\n"
            "        self.errors = errors\n"
            "\n"
            "    def hit_rate(self) -> Fraction:\n"
            "        return Fraction(sum(1 for e in self.errors if abs(e) <= HIT_BAND), len(self.errors))\n"
            "\n"
            "    def bias(self) -> Fraction:\n"
            "        return Fraction(sum(self.errors), len(self.errors))\n"
            "\n"
            "\n"
            "def main() -> None:\n",
        ),
        (
            "    hit_rate = ___\n",
            "    window = Window(errors)\n    hit_rate = window.hit_rate()\n",
        ),
        (
            "    bias = ___\n",
            "    bias = window.bias()\n",
        ),
    ],
}

for name, reps in ALTS.items():
    text = TWIN
    for old, new in reps:
        if name == "alt_class_window.py" and old in ("    hit_rate = ___\n", "    bias = ___\n"):
            # the twin is the completed solution, so take the completed lines
            old = old.replace("___", "Fraction(hits, horizon)" if "hit" in old else "Fraction(sum(errors), horizon)")
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
