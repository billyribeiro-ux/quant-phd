"""Independent re-derivation of LX1 project figures (round 4). Uses mpmath-free Decimal at 50 digits."""
import csv, json, math, statistics, sys
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().prec = 50
DATA = "/Users/billyribeiro/.fanout/wt/verifyE4-LX1-c/course/assets/data/market/fx_monthly.csv"
MAN = "/Users/billyribeiro/.fanout/wt/verifyE4-LX1-c/course/assets/data/market/MANIFEST.json"
rows = list(csv.DictReader(open(DATA, encoding="utf-8", newline="")))
print("fields:", list(rows[0].keys()))
print("rows:", len(rows), "first:", rows[0]["month"], "last:", rows[-1]["month"])
def col(c):
    out = []
    for r in rows:
        out.append((r["month"], r[c]))
    return out
def blanks(c):
    return [m for m, v in col(c) if v.strip() == ""]
print("GBP blanks:", len(blanks("GBP")), "EUR blanks:", len(blanks("EUR")), "first EUR nonblank:", [m for m, v in col("EUR") if v.strip()][:1])
gbp = [(m, Decimal(v)) for m, v in col("GBP")]
# log changes using Decimal ln via float-free: use math.log on exact ratio converted with 50 digits
from decimal import Decimal as D
def ln_dec(x):
    # high precision natural log using Decimal
    return x.ln()
changes = []
for (pm, pv), (m, v) in zip(gbp, gbp[1:]):
    changes.append((m, ln_dec(v / pv)))
def sd(xs):
    n = len(xs)
    mean = sum(xs) / n
    return (sum((x - mean) ** 2 for x in xs) / (n - 1)).sqrt()
w1 = changes
w2 = [c for c in changes if c[0] >= "2000-01"]
w3 = [c for c in changes if c[0] >= "2025-10"]
for name, w in (("w1", w1), ("w2", w2), ("w3", w3)):
    xs = [x for _, x in w]
    s = sd(xs)
    zeros = [m for m, x in w if x == 0]
    big = max(w, key=lambda t: abs(t[1]))
    print(name, "first", w[0][0], "last", w[-1][0], "n", len(xs), "zeros", len(zeros), zeros, "sd%/mo", (100 * s).quantize(Decimal("0.0001"), ROUND_HALF_UP), "sd exact", s,
          "biggest", (big[0], (100 * big[1]).quantize(Decimal("0.0001"), ROUND_HALF_UP)))
    print(name, "sd 2dp", (100 * s).quantize(Decimal("0.01"), ROUND_HALF_UP), "sd decimal 6dp", s.quantize(Decimal("0.000001"), ROUND_HALF_UP))
s1 = sd([x for _, x in w1]); s2 = sd([x for _, x in w2]); s3 = sd([x for _, x in w3])
print("ratio w2/w1 unrounded:", s2 / s1, "2dp:", (s2 / s1).quantize(Decimal("0.01"), ROUND_HALF_UP))
print("ratio of rounded 2.47/2.79:", Decimal("2.47") / Decimal("2.79"))
print("difference sd w1-w2 %/mo unrounded:", 100 * (s1 - s2), "2dp", (100 * (s1 - s2)).quantize(Decimal("0.01"), ROUND_HALF_UP))
print("window three months:", [m for m, _ in w3])
print("window two zero months", [m for m, x in w2 if x == 0])
print("window one zero months", [m for m, x in w1 if x == 0])
# Lab 1 numbers
print("L1 falling real:", (Decimal(10000000) / Decimal("0.85")), "rising real:", Decimal(10000000) / Decimal("1.15"))
print("L1 diff cents:", Decimal(10000000) / Decimal("0.85") - Decimal(10000000) / Decimal("1.15"))
print("L1 burden falling %:", 100 * (1 / Decimal("0.85") - 1), "rising %:", 100 * (1 / Decimal("1.15") - 1))
print("L2 real t5:", Decimal(4000000) / Decimal("0.93"), "burden %:", 100 * (1 / Decimal("0.93") - 1), "inverted:", 100 * (Decimal("0.93") - 1))
man = json.load(open(MAN, encoding="utf-8"))
print("MANIFEST keys:", list(man.keys())[:10])
fx = [d for d in (man.get("datasets", man) if isinstance(man, dict) else man) ]
print(json.dumps(man, indent=1)[:200])
