import re, json, pathlib, sys
from fractions import Fraction
ROOT = pathlib.Path("/tmp/verify8-AC1-c/course/modules/AC/AC1")
# macros used in the two pages
macros = set()
for p in ("L07.html", "L08.html"):
    macros |= set(re.findall(r"\\([A-Za-z]+)", (ROOT / p).read_text(encoding="utf-8")))
print("macros:", sorted(macros))
# figure / svg / cite markup
for p in ("L07.html", "L08.html"):
    t = (ROOT / p).read_text(encoding="utf-8")
    print(p, "svg/figure:", len(re.findall(r"<svg|<figure|class=\"figure", t)), "data-cite/http:", len(re.findall(r"data-cite|https?://", t)))
# L07 SBC schedule in integer cents from the grant table printed in the lab (grant lines of L07:251-254)
grants = [  # (grant_year, vest_years, total_cents)
    (2, 3, 2136000), (1, 3, 2978500), (1, 4, 7936500), (3, 3, 6280000)]
def expense(gy, v, C, t):
    i = t - gy
    if i < 0 or i >= v: return 0
    base = C // v
    return base if i < v - 1 else C - (v - 1) * base
sbc = [sum(expense(gy, v, C, t) for gy, v, C in grants) for t in range(1, 7)]
print("L07 SBC cents:", sbc, "sum totals ok:", sum(c for _, _, c in grants) == sum(sbc))
# L08 asset: cost 4,670,000 cents, life 5, tax pct 40,30,20,10,0, pretax per year from lab table, rate 21
cost, L, tp, r = 4670000, 5, [40, 30, 20, 10, 0], 21
pretax = [4824400, 8408500, 4813000, 4633900, 5902500]
b = cost // L; tau = [cost * p // 100 for p in tp]
K = 0; prev = 0; out = []
for t in range(L):
    K += tau[t] - b
    dtl = Fraction(r * K, 100); de = dtl - prev; prev = dtl
    ct = Fraction(r * (pretax[t] - (tau[t] - b)), 100)
    out.append((str(dtl), str(de), str(ct), str(ct + de), str(Fraction(r * pretax[t], 100))))
for row in out: print("L08 year", row)
print("TE equals rP/100 each year:", all(Fraction(o[3]) == Fraction(o[4]) for o in out))
