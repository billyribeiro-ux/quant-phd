"""Round-10 verifier: independent re-derivation of every number on project.html (labs 1-3) and the MANIFEST and CSV
facts the page states. Uses exact Fractions for labs 1-2 and the CSV; the log changes are float with a mpmath-free
high-precision check (Decimal ln via series is avoided: float ln error is ~1e-16, far below the 0.005 print grid)."""
import csv, math, statistics, json, sys
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP
root = sys.argv[1]
def half_up(x, places):
    return Decimal(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
# Lab 1 (exact)
D = Fraction(10_000_000)
fall = [Fraction(p, 100) for p in (100, 97, 94, 91, 88, 85)]
rise = [Fraction(p, 100) for p in (100, 103, 106, 109, 112, 115)]
print("lab1 falling real debt t=5 cents exact:", float(D / fall[-1]), "dollars 2dp:", half_up(float(D / fall[-1]) / 100, 2))
print("lab1 rising real debt t=5 dollars 2dp:", half_up(float(D / rise[-1]) / 100, 2))
print("lab1 burden falling pct 2dp:", half_up(float(100 * (fall[0] / fall[-1] - 1)), 2), " rising:", half_up(float(100 * (rise[0] / rise[-1] - 1)), 2))
print("lab1 difference dollars 2dp:", half_up(float((D / fall[-1] - D / rise[-1]) / 100), 2), "exact cents:", float(D / fall[-1] - D / rise[-1]))
# Lab 2 (exact)
N = Fraction(4_000_000)
path = [Fraction(p, 100) for p in (100, 99, 98, 96, 95, 93)]
print("lab2 real debt dollars 2dp:", [str(half_up(float(N / p) / 100, 2)) for p in path])
print("lab2 burden pct 2dp:", half_up(float(100 * (path[0] / path[-1] - 1)), 2), "exact", float(100 * (path[0] / path[-1] - 1)))
print("lab2 inverted burden pct:", float(100 * (path[-1] / path[0] - 1)))
# CSV and MANIFEST facts
rows = list(csv.DictReader(open(f"{root}/course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="")))
print("csv header:", list(rows[0].keys()))
print("csv rows:", len(rows), rows[0]["month"], rows[-1]["month"])
blank = {c: sum(1 for r in rows if r[c] == "") for c in rows[0] if c != "month"}
print("blank cells per column:", blank)
eur_blank = [r["month"] for r in rows if r["EUR"] == ""]
print("EUR blank months first/last:", eur_blank[0], eur_blank[-1], "count", len(eur_blank), "prefix:", all(rows[i]["EUR"] == "" for i in range(len(eur_blank))))
gbp = [(r["month"], Fraction(r["GBP"])) for r in rows]
months = [m for m, _ in gbp]
# gap check
def idx(m): y, mm = m.split("-"); return int(y) * 12 + int(mm)
print("month gaps:", sum(1 for a, b in zip(months, months[1:]) if idx(b) != idx(a) + 1))
ch = [(m, math.log(float(v / gbp[i][1]))) for i, (m, v) in enumerate(gbp[1:])]
def sd(vals):
    mean = sum(vals) / len(vals)
    return math.sqrt(sum((x - mean) ** 2 for x in vals) / (len(vals) - 1))
w1 = ch
w2 = [c for c in ch if c[0] >= "2000-01"]
w3 = [c for c in ch if c[0] >= "2025-10"]
for name, w in (("w1", w1), ("w2", w2), ("w3", w3)):
    vals = [v for _, v in w]
    zeros = [m for m, v in w if v == 0.0]
    big = max(w, key=lambda t: abs(t[1]))
    s = sd(vals)
    print(name, "first", w[0][0], "last", w[-1][0], "n", len(vals), "zeros", len(zeros), zeros[:5], "sd pct", half_up(100 * s, 2),
          "sd exact", 100 * s, "stdev-agree", abs(100 * (s - statistics.stdev(vals))) < 1e-9,
          "largest", half_up(100 * big[1], 2), big[0])
    if name == "w1": sd1 = s
    if name == "w2": sd2 = s
    if name == "w3": sd3 = s
print("ratio w2/w1 unrounded", sd2 / sd1, "2dp", half_up(sd2 / sd1, 2))
print("difference w1-w2 pct unrounded", 100 * (sd1 - sd2), "2dp", half_up(100 * (sd1 - sd2), 2))
print("lesson4 decimals check: sd1", sd1, "sd2", sd2)
print("w2 first change month", w2[0][0], "w1 first", w1[0][0])
print("parity claim: nonzero changes w2", sum(1 for _, v in w2 if v != 0.0), "of", len(w2))
print("max abs over w1 is 1985-03 check:", max(w1, key=lambda t: abs(t[1]))[0])
print("sd ratio pct:", 100 * sd1)
json.dump({"ok": True}, open("/dev/null", "w"))
