import math, random, sys
sys.path.insert(0, '/Users/billyribeiro/.fanout/wt/verifyS2-FC2-c/ledgers/FC2/scripts/FC2-c-r2')
from scipy.stats import norm
def bs(S, K, r, tau, sig):
    s = sig * math.sqrt(tau)
    d1 = (math.log(S / K) + (r + sig * sig / 2) * tau) / s
    d2 = d1 - s
    return S * norm.cdf(d1) - K * math.exp(-r * tau) * norm.cdf(d2), d1, d2
for K in (80.0, 100.0, 120.0):
    grid = [10 ** (-k / 4) for k in range(40, -1, -1)]
    vals = [bs(100.0, K, 0.05, 1.0, s)[0] for s in grid]
    bad = [(grid[i], grid[i+1], vals[i], vals[i+1]) for i in range(len(vals)-1) if not vals[i] < vals[i+1]]
    print(K, "non-increasing pairs:", bad[:4])
random.seed(1)
worst=(0,None)
for _ in range(300):
    K = random.uniform(60,140); sig_true = random.uniform(0.02,0.9)
    S=100.0; r=0.05; tau=1.0
    Cp = bs(S,K,r,tau,sig_true)[0]
    L = max(S-K*math.exp(-r*tau),0)
    if not (L < Cp < S): continue
    lo, hi = 1e-6, 10.0
    if not (bs(S,K,r,tau,lo)[0] < Cp <= bs(S,K,r,tau,hi)[0]): continue
    while hi-lo > 1e-10:
        m=(lo+hi)/2
        if bs(S,K,r,tau,m)[0] < Cp: lo=m
        else: hi=m
    mid=(lo+hi)/2
    ratio=abs(mid-sig_true)/5e-11
    if ratio>worst[0]:
        d1=(math.log(S/K)+(r+sig_true**2/2)*tau)/(sig_true*math.sqrt(tau))
        vega=S*norm.pdf(d1)*math.sqrt(tau)
        worst=(ratio,(K,sig_true,Cp-L,vega,mid-sig_true))
print("worst", worst)
