import csv, math, statistics
from decimal import Decimal, getcontext
from fractions import Fraction
getcontext().prec = 50
rows = list(csv.DictReader(open('/Users/billyribeiro/.fanout/wt/verifyE8-LX1-c/course/assets/data/market/fx_monthly.csv', encoding='utf-8', newline='')))
print('fields', list(rows[0].keys()))
print('n rows', len(rows), rows[0]['month'], rows[-1]['month'])
blank = {c: sum(1 for r in rows if not (r[c] or '').strip()) for c in rows[0] if c != 'month'}
print('blank counts', blank)
first_eur = next(r['month'] for r in rows if (r['EUR'] or '').strip())
print('first EUR month', first_eur)
# GBP series exact
gbp = [(r['month'], Decimal(r['GBP'])) for r in rows]
# monthly log changes using Decimal ln
def dln(x): return x.ln()
chg = []
for (m0, p0), (m1, p1) in zip(gbp, gbp[1:]):
    chg.append((m1, dln(p1/p0)))
def sd(vals):
    n = len(vals); mu = sum(vals)/n
    return (sum((v-mu)**2 for v in vals)/(n-1)).sqrt()
def win(name, sel):
    vals = [v for m, v in chg if sel(m)]
    s = sd(vals)
    zeros = sum(1 for v in vals if v == 0)
    big = max(vals, key=abs)
    bm = [m for m, v in chg if sel(m) and v == big][0]
    print(name, 'n', len(vals), 'zeros', zeros, 'sd%', (s*100).quantize(Decimal('0.000001')), 'biggest%', (big*100).quantize(Decimal('0.000001')), bm, 'first', [m for m,v in chg if sel(m)][0], 'last', [m for m,v in chg if sel(m)][-1])
    return s
s1 = win('W1', lambda m: True)
s2 = win('W2', lambda m: m >= '2000-01')
s3 = win('W3', lambda m: m >= '2025-10')
print('ratio', (s2/s1).quantize(Decimal('0.000001')))
print('diff pct', (100*(s1-s2)).quantize(Decimal('0.000001')))
# float-based check as lab does
fl = [(m, math.log(float(Decimal(b)/Decimal(a)))) for (a_m,a),(b_m,b) in [((0,0),(0,0))]] if False else None
print('done')
