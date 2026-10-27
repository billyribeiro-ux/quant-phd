from fractions import Fraction as F
# worked firm, page L08 section 3 (lines 418)
p = dict(rev=1000, rec=100, cogs=600, ca=400, ppe=300, ta=1000, dep=30, sga=150, cl=200, ltd=200, ni=40, cfo=45)
t = dict(rev=1200, rec=180, cogs=780, ca=480, ppe=330, ta=1200, dep=30, sga=180, cl=250, ltd=220, ni=60, cfo=20)
gm = lambda f: (f['rev'] - f['cogs']) / f['rev']
idx = {}
idx['DSRI'] = (t['rec']/t['rev'])/(p['rec']/p['rev'])
idx['GMI'] = gm(p)/gm(t)
at = 1-(t['ca']+t['ppe'])/t['ta']; ap = 1-(p['ca']+p['ppe'])/p['ta']
idx['AQI'] = at/ap
idx['SGI'] = t['rev']/p['rev']
idx['DEPI'] = (p['dep']/(p['dep']+p['ppe']))/(t['dep']/(t['dep']+t['ppe']))
idx['SGAI'] = (t['sga']/t['rev'])/(p['sga']/p['rev'])
idx['LVGI'] = ((t['cl']+t['ltd'])/t['ta'])/((p['cl']+p['ltd'])/p['ta'])
idx['TATA'] = (t['ni']-t['cfo'])/t['ta']
for k,v in idx.items(): print(k, round(v,4), v)
W = dict(DSRI=0.920, GMI=0.528, AQI=0.404, SGI=0.892, DEPI=0.115, SGAI=-0.172, LVGI=-0.327, TATA=4.679)
M = -4.84 + sum(W[k]*idx[k] for k in W)
print('M exact-index =', round(M,6), ' four-dp index M =', end=' ')
disp = dict(DSRI=1.5,GMI=1.1429,AQI=1.0833,SGI=1.2,DEPI=1.0909,SGAI=1.0,LVGI=0.9792,TATA=0.0333)
Md = -4.84 + sum(W[k]*disp[k] for k in W)
print(round(Md,6))
terms = [(-4.84)] + [W[k]*disp[k] for k in W]
print('sum of displayed terms (products of 4dp values) =', round(sum(terms),6))
print('displayed terms rounded to 4dp then summed:', round(sum(round(x,4) for x in terms),4))
# page E1 / lab: medians from twin output
