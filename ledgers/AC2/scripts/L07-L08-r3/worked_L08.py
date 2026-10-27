"""Exact recomputation of the L08 worked firm (section 3) and of the displayed M sum (Fractions)."""
from fractions import Fraction as F
import math

# Worked firm, SCU (from L08.html section 3, line 417)
t1 = dict(rev=F(1000), rec=F(100), cogs=F(600), ca=F(400), ppe=F(300), ta=F(1000), dep=F(30), sga=F(150), cl=F(200), ltd=F(200), ni=F(40), cfo=F(45))
t0 = dict(rev=F(1200), rec=F(180), cogs=F(780), ca=F(480), ppe=F(330), ta=F(1200), dep=F(30), sga=F(180), cl=F(250), ltd=F(220), ni=F(60), cfo=F(20))
# t0 is year t, t1 is year t-1 in the page's notation
t, p = t0, t1
gm = lambda f: (f['rev'] - f['cogs']) / f['rev']
idx = {}
idx['DSRI'] = (t['rec'] / t['rev']) / (p['rec'] / p['rev'])
idx['GMI'] = gm(p) / gm(t)
a_t = 1 - (t['ca'] + t['ppe']) / t['ta']
a_p = 1 - (p['ca'] + p['ppe']) / p['ta']
idx['AQI'] = a_t / a_p
idx['SGI'] = t['rev'] / p['rev']
idx['DEPI'] = (p['dep'] / (p['dep'] + p['ppe'])) / (t['dep'] / (t['dep'] + t['ppe']))
idx['SGAI'] = (t['sga'] / t['rev']) / (p['sga'] / p['rev'])
idx['LVGI'] = ((t['cl'] + t['ltd']) / t['ta']) / ((p['cl'] + p['ltd']) / p['ta'])
idx['TATA'] = (t['ni'] - t['cfo']) / t['ta']
coef = {'DSRI': F('0.920'), 'GMI': F('0.528'), 'AQI': F('0.404'), 'SGI': F('0.892'), 'DEPI': F('0.115'), 'SGAI': F('-0.172'), 'LVGI': F('-0.327'), 'TATA': F('4.679')}
intercept = F('-4.84')
M = intercept + sum(coef[k] * idx[k] for k in coef)
print('exact indices:')
for k in idx:
    print(f'  {k:5s} {idx[k]} = {float(idx[k]):.6f}')
print('exact M =', M, '=', float(M))
print('M rounded 4dp (round half even on float):', round(float(M), 4))
# Displayed terms: indices rounded to 4 dp, as the page displays them
disp = {'DSRI': F('1.5000'), 'GMI': F('1.1429'), 'AQI': F('1.0833'), 'SGI': F('1.2000'), 'DEPI': F('1.0909'), 'SGAI': F('1.0000'), 'LVGI': F('0.9792'), 'TATA': F('0.0333')}
terms = {k: coef[k] * disp[k] for k in coef}
for k in terms:
    print(f'  term {k:5s} coef {coef[k]} x {disp[k]} = {float(terms[k]):.6f}')
disp_sum = intercept + sum(terms.values())
print('displayed-terms sum =', float(disp_sum), '=', round(float(disp_sum), 6))
# Each page display line shows terms rounded to 4dp
print('M from unrounded indices minus displayed-terms sum =', float(M - disp_sum))
