# Independent re-derivation of every number on the LX1 project page (round 13). Reads the snapshot CSV by absolute path.
import csv, math, statistics, sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

CSV = sys.argv[1]
rows = list(csv.DictReader(open(CSV, encoding='utf-8', newline='')))
print('rows', len(rows), rows[0]['month'], rows[-1]['month'])
# month continuity
def mi(m):
    y, mo = m.split('-'); return int(y) * 12 + int(mo) - 1
gaps = [(a['month'], b['month']) for a, b in zip(rows, rows[1:]) if mi(b['month']) != mi(a['month']) + 1]
print('gaps', gaps)
blank = {c: [r['month'] for r in rows if r[c].strip() == ''] for c in rows[0] if c != 'month'}
print('blank counts', {c: len(v) for c, v in blank.items()}, 'EUR first nonblank', next(r['month'] for r in rows if r['EUR'].strip()))
gbp = [(r['month'], r['GBP']) for r in rows]
# unrounded log changes in float (independent code path: use Decimal ln via math on exact Fraction ratio)
ch = []
for (pm, pv), (m, v) in zip(gbp, gbp[1:]):
    ratio = Fraction(Decimal(v)) / Fraction(Decimal(pv))
    ch.append((m, math.log(float(ratio))))
def sd(vals):
    n = len(vals); mu = sum(vals) / n
    return math.sqrt(sum((x - mu) ** 2 for x in vals) / (n - 1))
def r2(x):
    return Decimal(repr(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
W1 = ch
W2 = [c for c in ch if c[0] >= '2000-01']
W3 = [c for c in ch if c[0] >= '2025-10']
for name, W in [('W1', W1), ('W2', W2), ('W3', W3)]:
    vals = [x for _, x in W]
    s = sd(vals)
    big = max(W, key=lambda t: abs(t[1]))
    zeros = sum(1 for x in vals if x == 0.0)
    print(name, W[0][0], W[-1][0], 'n', len(vals), 'zeros', zeros, 'sd_pct', 100 * s, 'r2', r2(100 * s),
          'stdev_diff', abs(100 * (s - statistics.stdev(vals))), 'biggest', big[0], 100 * big[1], r2(100 * big[1]))
    print('   decimal sd', s)
s1, s2, s3 = sd([x for _, x in W1]), sd([x for _, x in W2]), sd([x for _, x in W3])
print('ratio W2/W1', s2 / s1, r2(s2 / s1))
print('diff W1-W2 pct', 100 * (s1 - s2), r2(100 * (s1 - s2)))
# largest absolute change in whole column (must equal W1 max since W1 holds every change)
print('column max abs', max(W1, key=lambda t: abs(t[1])))
# window 3 zero or near zero listing
print('W3 values pct', [(m, round(100 * x, 4)) for m, x in W3])
# Parity claim: count of exact zero changes in window 2 vs rate equality
eq = [m for (pm, pv), (m, v) in zip(gbp, gbp[1:]) if Decimal(v) == Decimal(pv)]
print('equal-rate months', eq)
# Lesson 4 decimals check
print('W1 sd decimal 6dp', round(s1, 6), 'W2', round(s2, 6))
# L1: whole-column: sanity for '1985-03' value
print('1985-03', [x for x in ch if x[0] == '1985-03'])
print('2008-10', [x for x in ch if x[0] == '2008-10'])
print('2026-04', [x for x in ch if x[0] == '2026-04'])
