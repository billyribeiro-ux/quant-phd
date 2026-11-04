"""Round-6 independent recheck of the GBP column numbers (cards c054-c058, c065, c068-c069) from the embedded CSV, with statistics module."""
import csv, math, statistics, sys
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8", newline="")))
months = [r["month"] for r in rows]
gbp = [float(r["GBP"]) for r in rows]
ch = [(months[i], math.log(gbp[i]/gbp[i-1])) for i in range(1, len(gbp))]
zero = [m for i, m in enumerate(months[1:], 1) if gbp[i] == gbp[i-1]]
print("months", len(rows), months[0], months[-1], "changes", len(ch), "zero", len(zero), zero)
w1 = ch
w2 = [c for c in ch if c[0] >= "2000-01"]
s1 = statistics.stdev([c for _, c in w1]); s2 = statistics.stdev([c for _, c in w2])
print("w1 n", len(w1), "sd", round(s1, 6), s1)
print("w2 n", len(w2), "first", w2[0][0], "sd", round(s2, 6), s2)
print("diff", round(s2 - s1, 6), "ratio", round(s2/s1, 4), s2/s1)
m1 = max(w1, key=lambda c: abs(c[1])); m2 = max(w2, key=lambda c: abs(c[1]))
print("w1 max", m1, "w2 max", m2)
print("nonzero w1", sum(1 for _, c in w1 if c != 0))
print("bounds: w2 starts after 1999-12 rate; prior row", months[months.index('2000-01')-1])
