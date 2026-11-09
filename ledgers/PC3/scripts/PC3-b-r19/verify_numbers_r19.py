"""Round 19 PC3-b: exact re-derivation of L06 numbers and the L04 seed-0 card numbers."""
from fractions import Fraction as F


def A(r: F, n: int = 3) -> F:
    return sum((1 / (1 + r) ** t for t in range(1, n + 1)), F(0))


def be(r: F) -> F:
    return F(3000) / A(r)


for r, label in ((F(8, 100), "8%"), (F(10, 100), "10%"), (F(12, 100), "12%")):
    b = be(r)
    print(label, "A =", float(A(r)), "break-even =", float(b), "round4 =", round(float(b), 4))
print("A(10%) exact", A(F(1, 10)), "== 3310/1331:", A(F(1, 10)) == F(3310, 1331))
print("break-even 10% exact", be(F(1, 10)), "== 399300/331:", be(F(1, 10)) == F(399300, 331))
print("width 8->12", F(round(float(be(F(12, 100))) * 10**4), 10**4) - F(round(float(be(F(8, 100))) * 10**4), 10**4))
b8, b10, b12 = (round(float(be(F(p, 100))), 4) for p in (8, 10, 12))
print("diffs", round(b10 - b8, 4), round(b12 - b10, 4), "per point", (b12 - b8) / 4)
npv = lambda u, r=F(1, 10): -15000000 + 5000 * u * A(r)  # noqa: E731
print("NPV 1200 exact", npv(F(1200)), float(npv(F(1200))), F(-105000000, 1331) == npv(F(1200)))
print("NPV 1300 exact", float(npv(F(1300))), F(1550000000, 1331) == npv(F(1300)))
print("NPV 200", float(npv(F(200))), "NPV 1600", float(npv(F(1600))))
print("m* for break-even 1600:", float(F(15000000) / (F(1600) * A(F(1, 10)))), float(1 - F(15000000) / (F(1600) * A(F(1, 10))) / 5000))
print("M3 u*", F(100000) / (400 * A(F(1, 10))), float(F(100000) / (400 * A(F(1, 10)))), F(33275, 331) == F(100000) / (400 * A(F(1, 10))))
print("E1 A(12%) rounded 7dp", round(float(A(F(12, 100))), 7))
print("Example 4.2 break-even exact", F(399300, 331) == F(3000) / A(F(1, 10)) * 1)
