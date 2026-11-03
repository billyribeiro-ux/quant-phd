"""Write three new alternative correct implementations (verifier D2, round 2) from grader/reference.py.

Each replaces only the price computation (and, for alt_decimal, the rounding helper) with a different valid algorithm:
  alt_decimal:   decimal.Decimal in a 60-digit context, ROUND_HALF_UP (ties away from zero for Decimal), price by Decimal division
  alt_recurrence: exact Fraction discount factors built by the recurrence v_t = v_{t-1} / (1 + y), no power call
  alt_integer:   integer-only arithmetic: the price over the common denominator (10000 + yield_bps) ** N, one integer rounding
Validation and events() are unchanged from the reference, so the named conditions behave as the page states.
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = ROOT / "ledgers/FC1/scripts/FC1-c-r2/alt"
REF = (ROOT / "course/modules/FC/FC1/grader/reference.py").read_text(encoding="utf-8")

PRICE_OLD = REF[REF.index("def bond_price_cents"): REF.index("class CashTrade")]

ALT_DECIMAL_PRICE = '''def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    """Decimal algorithm: present value in a 60-digit context, rounded half up (away from zero) once."""
    from decimal import ROUND_HALF_UP, Context, Decimal

    rate = _whole(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    ctx = Context(prec=60, rounding=ROUND_HALF_UP)
    base = ctx.add(Decimal(1), ctx.divide(Decimal(rate), Decimal(10_000)))
    total = Decimal(0)
    for period, amount in bond.events():
        total = ctx.add(total, ctx.divide(Decimal(amount), ctx.power(base, Decimal(period))))
    return int(total.quantize(Decimal(1), rounding=ROUND_HALF_UP, context=ctx))


'''

ALT_RECURRENCE_PRICE = '''def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    """Recurrence algorithm: discount factors built one period at a time as v_t = v_(t-1) / (1 + y), exactly."""
    rate = _whole(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    step = 1 / (1 + Fraction(rate, 10_000))
    factor = Fraction(1)
    reached = 0
    total = Fraction(0)
    for period, amount in bond.events():
        while reached < period:
            factor = factor * step
            reached += 1
        total = total + amount * factor
    return _half_away(total)


'''

ALT_INTEGER_PRICE = '''def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    """Integer algorithm: the present value over the common denominator (10000 + yield_bps) ** N, one integer rounding."""
    rate = _whole(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    base = 10_000 + rate
    events = bond.events()
    last = max(period for period, _ in events)
    numerator = sum(amount * 10_000**period * base ** (last - period) for period, amount in events)
    denominator = base**last
    magnitude = abs(numerator)
    rounded = (2 * magnitude + denominator) // (2 * denominator)
    return rounded if numerator >= 0 else -rounded


'''

ALTS = {
    "alt_decimal.py": ALT_DECIMAL_PRICE,
    "alt_recurrence.py": ALT_RECURRENCE_PRICE,
    "alt_integer.py": ALT_INTEGER_PRICE,
}
for name, price in ALTS.items():
    text = REF.replace(PRICE_OLD, price, 1)
    assert text != REF, name
    head = name.replace(".py", "").replace("alt_", "").replace("_", " ")
    text = text.replace(
        REF[: REF.index('"""', 3) + 3],
        f'"""Alternative correct implementation (verifier D2, round 2): {head} price; validation and events as the reference."""',
        1,
    )
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", OUT / name)
