"""Independent re-derivation of every project-page number. Exact Fractions for Labs 1-2; float (as the lab) for Lab 3 SDs."""
import csv
import math
import statistics
from fractions import Fraction as F

def rhu(x, places=2):
    """Round half up (away from zero) of a Fraction, returned as a string with `places` decimals."""
    scaled = F(x) * 10**places
    n = math.floor(abs(scaled) + F(1, 2))
    n = n if scaled >= 0 else -n
    sign = "-" if n < 0 else ""
    whole, part = divmod(abs(n), 10**places)
    return f"{sign}{whole}.{part:0{places}d}" if places else f"{sign}{whole}"

def fl_rhu(x, places=2):
    return rhu(F(x), places)  # exact binary value of the float, half up

# Lab 1 (exact, cents)
D = F(10_000_000)
for name, path in {"falling": (100, 97, 94, 91, 88, 85), "rising": (100, 103, 106, 109, 112, 115)}.items():
    P = [F(p, 100) for p in path]
    real = [rhu(D / p / 100) for p in P]
    burden = rhu(100 * (P[0] / P[-1] - 1))
    print(f"lab1 {name} real_dollars={real} burden_pct={burden}")
diff = D / F(85, 100) - D / F(115, 100)
print("lab1 diff exact cents", float(diff), "dollars", rhu(diff / 100))
print("lab1 1/0.85 cents exact", float(D / F(85, 100)))
print("lab1 unrounded burden", float(100 * (F(100, 100) / F(85, 100) - 1)))

# Lab 2 (exact)
P5 = F(93, 100)
print("lab2 real dollars:", [rhu(F(4_000_000) / F(p, 100) / 100) for p in (100, 99, 98, 96, 95, 93)])
print("lab2 burden", rhu(100 * (F(1) / P5 - 1)), "inverted-ratio mutant", rhu(100 * (P5 / F(1) - 1)))
print("lab2 real at t5 exact cents", float(F(4_000_000) / P5))

# Lab 3 (CSV)
rows = list(csv.DictReader(open("course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="")))
print("cols", list(rows[0].keys()), "rows", len(rows), rows[0]["month"], rows[-1]["month"])
print("blank cells per column", {c: sum(1 for r in rows if not (r[c] or "").strip()) for c in rows[0] if c != "month"})
print("EUR first non-blank month", next(r["month"] for r in rows if r["EUR"].strip()))
print("EUR last blank month", [r["month"] for r in rows if not r["EUR"].strip()][-1])
gbp = [(r["month"], F(r["GBP"])) for r in rows]
def idx(m): return int(m[:4]) * 12 + int(m[5:7])
print("consecutive months", all(idx(b) == idx(a) + 1 for (a, _), (b, _) in zip(gbp, gbp[1:])))
logs = [(m, math.log(float(r / p))) for (_, p), (m, r) in zip(gbp, gbp[1:])]
def sd2(vals):
    n = len(vals); mu = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mu) ** 2 for v in vals) / (n - 1))
def rep(name, win):
    vals = [v for _, v in win]
    s, s2 = sd2(vals), statistics.stdev(vals)
    zeros = sum(v == 0.0 for v in vals)
    bm, bv = max(win, key=lambda t: abs(t[1]))
    print(f"{name}: n={len(vals)} zeros={zeros} first={win[0][0]} last={win[-1][0]} sd_decimal={s:.6f} sd_pct={100*s:.6f} -> {fl_rhu(100*s)} agree={abs(100*(s-s2))<=1e-9}; largest={100*bv:.6f} at {bm} -> {fl_rhu(100*bv)}")
    return s
w1, w2 = logs, [t for t in logs if t[0] >= "2000-01"]
w3 = [t for t in logs if t[0] >= "2025-10"]
s1, s2, s3 = rep("w1", w1), rep("w2", w2), rep("w3", w3)
print("ratio w2/w1 unrounded", s2 / s1, "->", fl_rhu(F(s2 / s1)))
print("diff (w1-w2)*100 unrounded", 100 * (s1 - s2), "->", fl_rhu(F(100 * (s1 - s2))))
print("w2 zero changes", sum(v == 0.0 for _, v in w2), "of", len(w2))
print("w3 zero changes", sum(v == 0.0 for _, v in w3), "of", len(w3))
print("w1 zero changes", sum(v == 0.0 for _, v in w1), "of", len(w1))
print("w1 sd decimal", s1, "w2 sd decimal", s2)
