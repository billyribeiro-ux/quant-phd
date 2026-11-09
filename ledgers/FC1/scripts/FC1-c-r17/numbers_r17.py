"""Round 17 fixer scratch: recompute the numbers on project.html from unrounded Fraction values."""

from decimal import Decimal, getcontext
from fractions import Fraction


def half_away(x: Fraction) -> int:
    m = abs(x)
    w = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return w if x >= 0 else -w


def pv(events: list[tuple[int, int]], yield_bps: int) -> Fraction:
    y = Fraction(yield_bps, 10000)
    return sum((Fraction(a) / (1 + y) ** t for t, a in events), Fraction(0))


getcontext().prec = 40
lab1 = [(1, 5000), (2, 5000), (3, 105000)]
p1 = pv(lab1, 400)
print(
    "lab1 PV 6dp",
    f"{float(p1):.6f}",
    "decimal",
    Decimal(p1.numerator) / Decimal(p1.denominator),
    "rounded",
    half_away(p1),
)
rnd = [(1, 500), (2, 500), (3, 10500)]
p2 = pv(rnd, 400)
print("rounding fixture PV decimal", Decimal(p2.numerator) / Decimal(p2.denominator), "rounded once", half_away(p2))
terms = [half_away(Fraction(a) / (1 + Fraction(400, 10000)) ** t) for t, a in rnd]
print("term-by-term", terms, sum(terms))
print("fixture A price", half_away(pv([(1, 10500)], 500)))
print("fixture B exact", Decimal(210000) / Decimal(19), "price", half_away(pv([(1, 10500)], -500)))
print("fixture F", pv([(1, 1)], 10000), half_away(pv([(1, 1)], 10000)))
print("fixture G", pv([(1, 10001)], 10000), half_away(pv([(1, 10001)], 10000)))
print("fixture C events", [(1, half_away(Fraction(10001 * 5000, 10000)))])
print("relative tolerance 1e-6 on 102775.09 cents", 1e-6 * (1 + 102775.091033), "cents")
