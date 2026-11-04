"""For every window start in fx_monthly GBP (LX1 slice b, round 1): dispersion of changes dated from that month to the end.

Tests the L04 canon-breaks sentence 'A different start gives a different dispersion' against all starts in the file.
"""
import csv, math, sys
rows = [(r["month"], float(r["GBP"])) for r in csv.DictReader(open(sys.argv[1], encoding="utf-8", newline=""))]
ch = [(rows[i][0], math.log(rows[i][1] / rows[i - 1][1])) for i in range(1, len(rows))]
def sd(v):
    n = len(v); mu = math.fsum(v) / n
    return math.sqrt(math.fsum((x - mu) ** 2 for x in v) / (n - 1))
target = sd([c for m, c in ch if m >= "2000-01"])
res = []
for k in range(len(ch) - 1):  # starts with at least 2 changes
    s = sd([c for _, c in ch[k:]])
    res.append((ch[k][0], s))
ties = [(m, s) for m, s in res if abs(s - target) < 1e-12 and m != "2000-01"]
print("starts checked:", len(res), "first", res[0][0], "last", res[-1][0])
print("window-two sd:", round(target, 6))
print("starts whose sd equals window-two sd within 1e-12 (excluding 2000-01):", ties)
print("count of distinct sd values at 1e-12:", len({round(s, 12) for _, s in res}))
print("start 1971-02 (window one) sd:", round(res[0][1], 6))
