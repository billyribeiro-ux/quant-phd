from fractions import Fraction as F
# L08 section 3 worked firm (SCU): t-1 and t values from L08.html line 418
p = dict(rev=F(1000), rec=F(100), cogs=F(600), ca=F(400), ppe=F(300), ta=F(1000), dep=F(30), sga=F(150), cl=F(200), ltd=F(200), ni=F(40), cfo=F(45))
t = dict(rev=F(1200), rec=F(180), cogs=F(780), ca=F(480), ppe=F(330), ta=F(1200), dep=F(30), sga=F(180), cl=F(250), ltd=F(220), ni=F(60), cfo=F(20))
gm = lambda x: (x['rev'] - x['cogs']) / x['rev']
dsri = (t['rec']/t['rev'])/(p['rec']/p['rev'])
gmi = gm(p)/gm(t)
aqi = (1-(t['ca']+t['ppe'])/t['ta'])/(1-(p['ca']+p['ppe'])/p['ta'])
sgi = t['rev']/p['rev']
depi = (p['dep']/(p['dep']+p['ppe']))/(t['dep']/(t['dep']+t['ppe']))
sgai = (t['sga']/t['rev'])/(p['sga']/p['rev'])
lvgi = ((t['cl']+t['ltd'])/t['ta'])/((p['cl']+p['ltd'])/p['ta'])
tata = (t['ni']-t['cfo'])/t['ta']
idx = dict(DSRI=dsri,GMI=gmi,AQI=aqi,SGI=sgi,DEPI=depi,SGAI=sgai,LVGI=lvgi,TATA=tata)
for k,v in idx.items(): print(k, float(v), round(float(v),4))
W = dict(DSRI=F('0.920'),GMI=F('0.528'),AQI=F('0.404'),SGI=F('0.892'),DEPI=F('0.115'),SGAI=F('-0.172'),LVGI=F('-0.327'),TATA=F('4.679'))
b0 = F('-4.84')
M = b0 + sum(W[k]*idx[k] for k in W)
print('M exact-index =', float(M), round(float(M),6))
# displayed-index arithmetic as printed on page (indices rounded to 4 dp, weights exact)
disp = dict(DSRI=F('1.5'),GMI=F('1.1429'),AQI=F('1.0833'),SGI=F('1.2'),DEPI=F('1.0909'),SGAI=F('1.0'),LVGI=F('0.9792'),TATA=F('0.0333'))
terms = {k: W[k]*disp[k] for k in W}
for k in W: print('term',k, float(terms[k]), round(float(terms[k]),4))
print('sum of displayed terms (intercept included) =', float(b0+sum(terms.values())), round(float(b0+sum(terms.values())),6))
# page's own displayed-term sum (as written with 4-dp term values)
print('page term-by-term 4dp:', round(-4.84+1.38+0.6035+0.4377+1.0704+0.1255-0.172-0.3202+0.1560,6))
# check claim: M from unrounded indices rounds to -1.5593?
print('M from unrounded indices, 4dp =', round(float(M),4))
