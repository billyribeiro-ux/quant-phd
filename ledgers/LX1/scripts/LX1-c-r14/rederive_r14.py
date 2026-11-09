"""Round-14 verifier re-derivation (independent of the lab code): Decimal at 60 digits, Fraction for the price paths.
Argument 1 is the checkout root. Prints every number the project page states in prose or in its labs."""
import csv, pathlib, sys
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction
getcontext().prec = 60
root = pathlib.Path(sys.argv[1])

def r2(x):  # round half up to 2 places
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

# Lab 1 (SIMULATED, exact)
debt = Fraction(10_000_000)
falling = [Fraction(p, 100) for p in (100, 97, 94, 91, 88, 85)]
rising = [Fraction(p, 100) for p in (100, 103, 106, 109, 112, 115)]
def cents_to_dollars_str(c):  # c is Fraction in cents, round half up to cent
    v = Decimal(c.numerator) / Decimal(c.denominator)
    return str(v.quantize(Decimal("1"), rounding=ROUND_HALF_UP) / 100)
print("L1 falling real debt $:", [cents_to_dollars_str(debt / p) for p in falling])
print("L1 rising real debt $:", [cents_to_dollars_str(debt / p) for p in rising])
bf = 100 * (falling[0] / falling[-1] - 1); br = 100 * (rising[0] / rising[-1] - 1)
print("L1 burden falling %:", r2(Decimal(bf.numerator) / Decimal(bf.denominator)), " rising %:", r2(Decimal(br.numerator) / Decimal(br.denominator)))
diff = (debt / falling[-1] - debt / rising[-1])
print("L1 part C diff $ (cents->dollars):", cents_to_dollars_str(diff))
print("L1 exact falling period-5 real debt cents:", Decimal(debt.numerator)/Decimal(falling[-1].numerator)*Decimal(falling[-1].denominator), "approx 11764705.882")
print("L1 step-3 exact cents 10000000/0.85:", float(debt/Fraction(85,100)))
print("L1 step-5 exact cents diff:", float(debt/Fraction(85,100) - debt/Fraction(115,100)))

# Lab 2 (SIMULATED)
d2 = Fraction(4_000_000)
p2 = [Fraction(p, 100) for p in (100, 99, 98, 96, 95, 93)]
print("L2 real debt $:", [cents_to_dollars_str(d2 / p) for p in p2])
b2 = 100 * (p2[0] / p2[-1] - 1)
print("L2 burden % (exact):", float(b2), "rounded:", r2(Decimal(b2.numerator)/Decimal(b2.denominator)))

# Lab 3 (snapshot)
rows = list(csv.DictReader(open(root / "course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="")))
print("L3 csv columns:", list(rows[0].keys()))
print("L3 csv rows:", len(rows), "first", rows[0]["month"], "last", rows[-1]["month"])
months = [r["month"] for r in rows]
gbp = [Decimal(r["GBP"]) for r in rows]
eur_first = next(r["month"] for r in rows if r.get("EUR", "") != "")
eur_blank = sum(1 for r in rows if r.get("EUR", "") == "")
print("EUR first non-blank:", eur_first, "EUR blank rows:", eur_blank, "GBP blank:", sum(1 for r in rows if r["GBP"] == ""))
def lchg(i):  # change dated months[i], i>=1
    return (gbp[i] / gbp[i-1]).ln()
idx = list(range(1, len(rows)))
def window(from_m):
    return [i for i in idx if months[i] >= from_m]
def sd(vals):
    n = len(vals); m = sum(vals, Decimal(0)) / n
    return (sum((v - m) ** 2 for v in vals) / (n - 1)).sqrt()
W1 = idx; W2 = window("2000-01"); W3 = window("2025-10")
for name, W in (("W1", W1), ("W2", W2), ("W3", W3)):
    ch = [lchg(i) for i in W]
    s = sd(ch)
    zeros = sum(1 for v in ch if v == 0)
    big = max(ch, key=lambda v: abs(v)); bi = W[ch.index(big)]
    print(f"{name}: n={len(ch)} first={months[W[0]]} last={months[W[-1]]} zeros={zeros} sd={s} pct={100*s} pct2={r2(100*s)}"
          f" largest={100*big} at {months[bi]}")
    globals()["SD_" + name] = s
print("ratio W2/W1 unrounded:", SD_W2 / SD_W1, "rounded:", r2(SD_W2 / SD_W1))
print("diff W1-W2 (percent) unrounded:", 100 * (SD_W1 - SD_W2), "rounded:", r2(100 * (SD_W1 - SD_W2)))
print("W2 minus W1 decimal:", SD_W2 - SD_W1)
print("max W1 abs change month:", months[max(W1, key=lambda i: abs(lchg(i)))], "W2 max abs change month:", months[max(W2, key=lambda i: abs(lchg(i)))])
print("W1 zero months:", [months[i] for i in W1 if lchg(i) == 0])
print("W2 zero months:", [months[i] for i in W2 if lchg(i) == 0])
print("W3 zero months:", [months[i] for i in W3 if lchg(i) == 0])
print("W2 first change uses month:", months[W2[0]-1])
