"""Round-14 verifier: writes three alternative correct implementations of the project labs (not mutants), each a
full twin variant, into ledgers/LX1/scripts/LX1-c-r14/alts/. Argument 1 is the checkout root.
alt1: lab 3 standard deviation by Welford's online algorithm instead of the two-pass formula.
alt2: lab 1 in float arithmetic with Decimal half-up rounding of the printed values.
alt3: lab 2 with every rounding done by Decimal quantize (ROUND_HALF_UP) instead of round_half_up."""
import pathlib, sys
root = pathlib.Path(sys.argv[1])
T = root / "tests/labs/LX1"
A = root / "ledgers/LX1/scripts/LX1-c-r14/alts"
def edit(src, dst, pairs):
    t = (T / src).read_text(encoding="utf-8")
    for old, new in pairs:
        assert t.count(old) == 1, (dst, old[:60], t.count(old))
        t = t.replace(old, new)
    (A / dst).write_text(t, encoding="utf-8")
    print("wrote", dst)
edit("lab-LX1-project-3.py", "alt1_lab3_welford.py", [(
"""    mean = math.fsum(values) / n
    return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / (n - 1))""",
"""    mean = 0.0
    m2 = 0.0
    for count, value in enumerate(values, start=1):
        delta = value - mean
        mean += delta / count
        m2 += delta * (value - mean)
    return math.sqrt(m2 / (n - 1))""")])
edit("lab-LX1-project-1.py", "alt2_lab1_float_arithmetic.py", [
("PATHS: dict[str, tuple[Fraction, ...]] = {\n    \"falling\": tuple(Fraction(p, 100) for p in (100, 97, 94, 91, 88, 85)),\n    \"rising\": tuple(Fraction(p, 100) for p in (100, 103, 106, 109, 112, 115)),\n}",
 "PATHS: dict[str, tuple[float, ...]] = {\n    \"falling\": tuple(p / 100 for p in (100, 97, 94, 91, 88, 85)),\n    \"rising\": tuple(p / 100 for p in (100, 103, 106, 109, 112, 115)),\n}"),
("def real_debt_cents(nominal_cents: int, price_level: Fraction) -> Fraction:", "def real_debt_cents(nominal_cents: int, price_level: float) -> float:"),
("    return Fraction(nominal_cents) / price_level", "    return nominal_cents / price_level"),
("def burden_change_percent(start_price: Fraction, end_price: Fraction) -> Fraction:", "def burden_change_percent(start_price: float, end_price: float) -> float:"),
("def round_half_up(value: Fraction) -> int:\n    \"\"\"The nearest integer to a value of either sign, a tie going away from zero.\"\"\"\n    magnitude = math.floor(abs(value) + Fraction(1, 2))\n    return magnitude if value >= 0 else -magnitude",
 "def round_half_up(value: float) -> int:\n    from decimal import Decimal, ROUND_HALF_UP\n    return int(Decimal(repr(value)).quantize(Decimal(1), rounding=ROUND_HALF_UP))"),
("            cents = round_half_up(real_debt_cents(NOMINAL_DEBT_CENTS, price))\n            print(f\"  t={t} price={fixed_two(int(price * 100))} real debt={fixed_two(cents)}\")",
 "            cents = round_half_up(real_debt_cents(NOMINAL_DEBT_CENTS, price))\n            print(f\"  t={t} price={fixed_two(round(price * 100))} real debt={fixed_two(cents)}\")"),
])
edit("lab-LX1-project-2.py", "alt3_lab2_decimal_quantize.py", [
("    print(f\"Part A, real debt in dollars by period:\")" if False else "        cents = round_half_up(real_debt_cents(NOMINAL_DEBT_CENTS, price))",
 "        from decimal import Decimal, ROUND_HALF_UP\n        cents = int(Decimal(real_debt_cents(NOMINAL_DEBT_CENTS, price).numerator) / Decimal(real_debt_cents(NOMINAL_DEBT_CENTS, price).denominator)).__class__(0) if False else round_half_up(real_debt_cents(NOMINAL_DEBT_CENTS, price))"),
])
