"""Round-7 independent re-derivation: Decimal ln (50 digits), no lab code reused."""
import csv, sys
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction
getcontext().prec = 50
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8", newline="")))
months = [r["month"] for r in rows]
gbp = [Decimal(r["GBP"]) for r in rows]
ch = []
for i in range(1, len(rows)):
    ch.append((months[i], (gbp[i] / gbp[i - 1]).ln()))
def sd(xs):
    n = len(xs); m = sum(xs, Decimal(0)) / n
    return (sum(((x - m) ** 2 for x in xs), Decimal(0)) / (n - 1)).sqrt()
def r2(d): return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
w1 = ch; w2 = [c for c in ch if c[0] >= "2000-01"]; w3 = [c for c in ch if c[0] >= "2025-10"]
out = {}
for name, w in [("w1", w1), ("w2", w2), ("w3", w3)]:
    xs = [c for _, c in w]
    s = sd(xs)
    zeros = [m for m, c in w if c == 0]
    big = max(w, key=lambda c: abs(c[1]))
    print(name, w[0][0], w[-1][0], "n", len(xs), "zeros", len(zeros), zeros[:5], "sd%", r2(100 * s), "sd_raw", s.quantize(Decimal("0.000001")),
          "largest", r2(100 * big[1]), big[0])
    out[name] = s
print("ratio w2/w1", r2(out["w2"] / out["w1"]), (out["w2"] / out["w1"]).quantize(Decimal("0.0001")))
print("diff w1-w2 %", r2(100 * (out["w1"] - out["w2"])), (100 * (out["w1"] - out["w2"])).quantize(Decimal("0.000001")))
print("EUR first nonblank", next(r["month"] for r in rows if r["EUR"]), "EUR blanks", sum(1 for r in rows if r["EUR"] == ""))
print("GBP blanks", sum(1 for r in rows if r["GBP"] == ""), "rows", len(rows), months[0], months[-1])
# lab 1 / lab 2 / exemplar arithmetic, exact
D1 = Fraction(10_000_000); P_fall5 = Fraction(85, 100); P_rise5 = Fraction(115, 100)
print("lab1 falling t5 dollars", float(D1 / P_fall5 / 100), "rising", float(D1 / P_rise5 / 100), "diff dollars", float((D1 / P_fall5 - D1 / P_rise5) / 100))
print("lab1 burden fall %", float(100 * (1 / P_fall5 - 1)), "rise %", float(100 * (1 / P_rise5 - 1)))
D2 = Fraction(4_000_000); P2 = Fraction(93, 100)
print("lab2 t5 dollars", float(D2 / P2 / 100), "burden %", float(100 * (1 / P2 - 1)), "inverted", float(100 * (P2 - 1)))
print("exemplar B ratio from rounded 2.47/2.79", 2.47 / 2.79)
print("window3 1.90 check: 1.90 printed; computed above")
