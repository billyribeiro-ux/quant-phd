import math, random
from scipy.stats import norm
def bs(S, K, r, tau, sig):
    s = sig * math.sqrt(tau)
    d1 = (math.log(S / K) + (r + sig * sig / 2) * tau) / s
    d2 = d1 - s
    return S * norm.cdf(d1) - K * math.exp(-r * tau) * norm.cdf(d2), d1, d2
random.seed(1); worst=0; n=0; skipped=0
for _ in range(2000):
    K = random.uniform(60,140); sig_true = random.uniform(0.02,0.9)
    S=100.0; r=0.05; tau=1.0
    Cp = bs(S,K,r,tau,sig_true)[0]
    L = max(S-K*math.exp(-r*tau),0)
    if not (L < Cp < S): continue
    d1=(math.log(S/K)+(r+sig_true**2/2)*tau)/(sig_true*math.sqrt(tau))
    vega=S*norm.pdf(d1)*math.sqrt(tau)
    if vega < 1e-2: skipped+=1; continue
    lo, hi = 1e-6, 10.0
    if not (bs(S,K,r,tau,lo)[0] < Cp <= bs(S,K,r,tau,hi)[0]): continue
    while hi-lo > 1e-10:
        m=(lo+hi)/2
        if bs(S,K,r,tau,m)[0] < Cp: lo=m
        else: hi=m
    mid=(lo+hi)/2; n+=1
    worst=max(worst, abs(mid-sig_true)/5e-11)
print("cases", n, "skipped (vega<1e-2)", skipped, "worst |err|/(tol/2):", worst)
