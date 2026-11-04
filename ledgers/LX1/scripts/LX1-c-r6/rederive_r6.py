"""Round-6 independent re-derivation of every number on project.html (Decimal ln at 60 digits, Fraction arithmetic)."""
import csv, math, statistics, pathlib
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction
getcontext().prec = 60
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE6-LX1-c")

def q(x, places):
    return Decimal(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)

# Lab 1 and Lab 2 (exact)
D = Fraction(10_000_000, 100)  # dollars
for name, path in {"falling": (100, 97, 94, 91, 88, 85), "rising": (100, 103, 106, 109, 112, 115)}.items():
    rd = [Fraction(10_000_000) / Fraction(p, 100) for p in path]
    print(name, "real cents t5", float(rd[-1]), "dollars", q(Decimal(rd[-1].numerator)/Decimal(rd[-1].denominator)/100, 2),
          "burden %", q(Decimal(100*(Fraction(path[0],100)/Fraction(path[-1],100)-1).numerator)/Decimal((100*(Fraction(path[0],100)/Fraction(path[-1],100)-1)).denominator), 2))
diff = Fraction(10_000_000)/Fraction(85,100) - Fraction(10_000_000)/Fraction(115,100)
print("lab1 difference cents", float(diff), "dollars", q(Decimal(diff.numerator)/Decimal(diff.denominator)/100, 2))
print("lab1 falling-real-value unrounded cents 10000000/0.85 =", q(Decimal(10000000)/Decimal("0.85"), 6))
print("lab1 burden falling exact 100*(1/0.85-1) =", q(Decimal(100)*(Decimal(1)/Decimal("0.85")-1), 6))
print("lab1 burden rising exact 100*(1/1.15-1) =", q(Decimal(100)*(Decimal(1)/Decimal("1.15")-1), 6))
lab2 = (100, 99, 98, 96, 95, 93)
print("lab2 t5 real dollars", q(Decimal(4000000)/Decimal("0.93")/100, 6), "burden", q(Decimal(100)*(Decimal(1)/Decimal("0.93")-1), 6))
print("lab2 inverted burden", q(Decimal(100)*(Decimal("0.93")/Decimal(1)-1), 6))

# Lab 3 windows from the snapshot
rows = list(csv.DictReader(open(ROOT / "course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="")))
print("cols", list(rows[0].keys())[:12], "nrows", len(rows), rows[0]["month"], rows[-1]["month"])
gbp_raw = [(r["month"], r["GBP"]) for r in rows]
gbp = [(m, Decimal(v)) for m, v in gbp_raw if v.strip() != ""]
blank = [m for m, v in gbp_raw if v.strip() == ""]
print("GBP blanks", len(blank))
changes = []
for (m0, v0), (m1, v1) in zip(gbp, gbp[1:]):
    changes.append((m1, (v1 / v0).ln()))
def sd(vals):
    n = len(vals); mean = sum(vals) / n
    return (sum((v - mean) ** 2 for v in vals) / (n - 1)).sqrt()
W = {
 "one": [c for c in changes],
 "two": [c for c in changes if c[0] >= "2000-01"],
 "three": [c for c in changes if c[0] >= "2025-10"],
}
sds = {}
for k, w in W.items():
    vals = [v for _, v in w]
    s = sd(vals); sds[k] = s
    zeros = [m for m, v in w if v == 0]
    big = max(w, key=lambda t: abs(t[1]))
    print(f"window {k}: first {w[0][0]} last {w[-1][0]} n={len(vals)} zeros={len(zeros)} {zeros if len(zeros)<6 else ''} sd%={q(100*s,4)} -> {q(100*s,2)} largest={q(100*big[1],4)} at {big[0]} -> {q(100*big[1],2)}")
    # cross-check with float statistics.stdev
    fv = [float(v) for v in vals]
    print("   float stdev agree (1e-9 %):", abs(100*(statistics.stdev(fv) - float(s))) <= 1e-9)
print("ratio two/one", q(sds["two"]/sds["one"], 4), "->", q(sds["two"]/sds["one"], 2))
print("difference one-two (%)", q(100*(sds["one"]-sds["two"]), 6), "->", q(100*(sds["one"]-sds["two"]), 2))
print("sd one (decimal)", q(sds["one"], 6), "sd two", q(sds["two"], 6))
print("sum identity check window one:", q(sum(v for _, v in W["one"]) - (gbp[-1][1]/gbp[0][1]).ln(), 20))
print("float ln check window three n=12 first/last", W["three"][0][0], W["three"][-1][0])
# largest in window one signed
w1 = W["one"]
print("largest window one signed", max(w1, key=lambda t: t[1]), "min", min(w1, key=lambda t: t[1]))
# check 1999-12 rate exists for window two's first change
print("rate 1999-12 exists:", any(m == "1999-12" for m, _ in gbp), "first 2000-01 change uses 1999-12:", [m for m,_ in changes if m=="2000-01"])
# non-decimal cells check
import re
bad = [m for m, v in gbp_raw if not re.fullmatch(r"\d+(\.\d+)?", v)]
print("non-decimal cells", bad[:5], len(bad))
