"""Round-5 independent re-derivation of every number on project.html (slice c). Uses Fraction and 40-digit Decimal,
not the lab code. Reads the snapshot CSV from the checkout's market folder (argument 1, read-only)."""

import csv
import statistics
import sys
from decimal import ROUND_HALF_UP, Decimal, getcontext
from fractions import Fraction

getcontext().prec = 40
CSV_PATH = sys.argv[1]


def q(x: Decimal, places: int) -> Decimal:
    return x.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


print("== Lab 1 / Lab 2 closed forms (exact)")
fal = [Fraction(p, 100) for p in (100, 97, 94, 91, 88, 85)]
ris = [Fraction(p, 100) for p in (100, 103, 106, 109, 112, 115)]
D1 = Fraction(10_000_000)
for name, path in (("falling", fal), ("rising", ris)):
    for t, p in enumerate(path):
        v = D1 / p
        print(f"  L1 {name} t={t} p={p} real cents={float(v):.6f} dollars2={q(Decimal(v.numerator) / Decimal(v.denominator) / 100, 2)}")
    print(f"  L1 {name} burden 100*(P0/P5-1) = {q(Decimal(100) * (Decimal(path[0].numerator)/Decimal(path[0].denominator) / (Decimal(path[-1].numerator)/Decimal(path[-1].denominator)) - 1), 2)}")
e5 = D1 / fal[-1]
r5 = D1 / ris[-1]
print(f"  L1 period-5 falling real value cents = {float(e5):.6f}; rising = {float(r5):.6f}; diff cents = {float(e5 - r5):.6f}; dollars = {q(Decimal((e5 - r5).numerator)/Decimal((e5-r5).denominator)/100, 2)}")
print(f"  L1 1/0.85 - 1 in percent = {float(100*(1/Fraction(85,100)-1)):.6f}")

D2 = Fraction(4_000_000)
path2 = [Fraction(p, 100) for p in (100, 99, 98, 96, 95, 93)]
for t, p in enumerate(path2):
    v = D2 / p
    print(f"  L2 t={t} price={p} real cents={float(v):.6f} dollars2={q(Decimal(v.numerator)/Decimal(v.denominator)/100, 2)}")
print(f"  L2 burden 100*(1/0.93 - 1) = {float(100*(Fraction(1)/path2[-1]-1)):.6f}")
print(f"  L2 wrong inverted burden 100*(0.93/1 - 1) = {float(100*(path2[-1]/path2[0]-1)):.6f}")

print("== Lab 3 from snapshot CSV, Decimal ln, 40 digits")
rows = []
with open(CSV_PATH, encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    cols = rd.fieldnames
    print("  header:", cols)
    for r in rd:
        rows.append((r["month"], r["GBP"], r["EUR"]))
print("  rows:", len(rows), "first", rows[0][0], "last", rows[-1][0])
blank_gbp = [m for m, g, e in rows if g.strip() == ""]
print("  GBP blank cells:", len(blank_gbp))
eur_first = next(m for m, g, e in rows if e.strip() != "")
eur_blank_before = [m for m, g, e in rows if m < eur_first and e.strip() == ""]
print("  EUR first non-blank:", eur_first, "; blank rows before:", len(eur_blank_before), "last blank before:", eur_blank_before[-1])
print("  EUR non-blank after first:", all(e.strip() != "" for m, g, e in rows if m >= eur_first))
# month contiguity
def idx(m):
    y, mm = m.split("-")
    return int(y) * 12 + int(mm) - 1
contig = all(idx(rows[i][0]) + 1 == idx(rows[i + 1][0]) for i in range(len(rows) - 1))
print("  months contiguous:", contig)

changes = []
for i in range(1, len(rows)):
    m, g, _ = rows[i]
    prev = rows[i - 1][1]
    ratio = Decimal(g) / Decimal(prev)
    changes.append((m, ratio.ln(), Decimal(g) == Decimal(prev)))


def sd_dec(vals):
    n = len(vals)
    mean = sum(vals) / n
    return (sum((v - mean) ** 2 for v in vals) / (n - 1)).sqrt()


W1 = changes
W2 = [c for c in changes if c[0] >= "2000-01"]
W3 = [c for c in changes if c[0] >= "2025-10"]
for name, W in (("W1", W1), ("W2", W2), ("W3", W3)):
    vals = [c[1] for c in W]
    s = sd_dec(vals)
    zeros = sum(1 for c in W if c[2])
    big = max(W, key=lambda c: abs(c[1]))
    print(f"  {name}: first {W[0][0]} last {W[-1][0]} n={len(W)} zeros={zeros} sd_pct={q(100*s, 2)} sd_pct_unrounded={100*s:.12f}")
    print(f"       largest by size {q(100*big[1], 2)} ({big[0]}) unrounded={100*big[1]:.12f}")
    print(f"       exact zero months: {[c[0] for c in W if c[2]]}")
    print(f"       stdev float agreement |diff| pct = {abs(float(100*s) - statistics.stdev([float(v) for v in vals])*100):.3e}")
s1 = sd_dec([c[1] for c in W1])
s2 = sd_dec([c[1] for c in W2])
print(f"  ratio W2/W1 unrounded = {s2/s1:.15f} -> {q(s2/s1, 2)}")
print(f"  W1 minus W2 pct unrounded = {100*(s1-s2):.12f} -> {q(100*(s1-s2), 2)}")
print(f"  W1 sd decimal = {q(s1, 6)} ; W2 sd decimal = {q(s2, 6)}")
print(f"  W2 minus W1 decimal (L04 check) = {s2 - s1:.7f}")
print(f"  sd W1 printed-then-subtracted: {Decimal('0.027935') - Decimal('0.024700')}")
print(f"  ratio of printed sds 0.024700/0.027935 = {Decimal('0.024700')/Decimal('0.027935'):.6f}")
print(f"  W1 window start 1971-02 check: first change month {W1[0][0]}; rate before 1999-12 used for W2 first change: {[c[0] for c in W2][:1]}")
print(f"  exemplar A: window3 last month {W3[-1][0]}")
