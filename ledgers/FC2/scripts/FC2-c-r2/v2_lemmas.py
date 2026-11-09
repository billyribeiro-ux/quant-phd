"""Round 2 numerical checks of the L07/L08 lemmas that the proofs assert."""
import math, random
from scipy.stats import norm

def bs(S, K, r, tau, sig):
    s = sig * math.sqrt(tau)
    d1 = (math.log(S / K) + (r + sig * sig / 2) * tau) / s
    d2 = d1 - s
    return S * norm.cdf(d1) - K * math.exp(-r * tau) * norm.cdf(d2), d1, d2

phi = norm.pdf
worst_vega = 0.0; worst_ident = 0.0; worst_fd = 0.0
for K in (80.0, 100.0, 120.0):
    for sig in (0.05, 0.1, 0.2, 0.4):
        S, r, tau = 100.0, 0.05, 1.0
        C, d1, d2 = bs(S, K, r, tau, sig)
        vega = S * phi(d1) * math.sqrt(tau)
        h = 1e-6
        fd = (bs(S, K, r, tau, sig + h)[0] - bs(S, K, r, tau, sig - h)[0]) / (2 * h)
        worst_fd = max(worst_fd, abs(fd - vega))
        worst_ident = max(worst_ident, abs(S * phi(d1) - K * math.exp(-r * tau) * phi(d2)) / (S * phi(d1)))
print("Lemma 2.1 finite-difference max abs err:", f"{worst_fd:.3e}", " identity S phi(d1)=K e^{-rt} phi(d2) rel err:", f"{worst_ident:.3e}")
# monotonicity and limits, K in 80,100,120
for K in (80.0, 100.0, 120.0):
    vals = [bs(100.0, K, 0.05, 1.0, s)[0] for s in [10 ** (-k / 4) for k in range(40, -1, -1)]]
    mono = all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))
    print(f"K={K:.0f} strictly increasing on grid: {mono}; C(1e-6)={bs(100.0,K,0.05,1.0,1e-6)[0]:.10f}; C(1e3)={bs(100.0,K,0.05,1.0,1e3)[0]:.10f}")
# Lemma 2.2 (tree): 0<d<R<u iff h < sigma^2/r^2 for r>0
random.seed(0)
bad = 0; n = 0
for _ in range(200000):
    r = random.uniform(1e-4, 0.5); sig = random.uniform(1e-3, 1.0); h = random.uniform(1e-4, 2.0)
    u = math.exp(sig * math.sqrt(h)); d = 1 / u; R = math.exp(r * h)
    cond = (0 < d < R < u)
    iff = h < sig * sig / (r * r)
    n += 1
    if cond != iff: bad += 1
print("Lemma 2.2 mismatches over", n, "random triples:", bad)
# Theorem 2.3: explicit sum vs backward induction (the lab's algorithm), S=K=100
def tree_sum(S, K, r, tau, sig, n):
    h = tau / n; u = math.exp(sig*math.sqrt(h)); d = 1/u; R = math.exp(r*h); q = (R-d)/(u-d)
    return math.exp(-r*tau)*sum(math.comb(n,k)*q**k*(1-q)**(n-k)*max(S*u**k*d**(n-k)-K,0) for k in range(n+1))
def tree_bi(S, K, r, tau, sig, n):
    h = tau / n; u = math.exp(sig*math.sqrt(h)); d = 1/u; R = math.exp(r*h); q = (R-d)/(u-d)
    vals = [max(S*u**j*d**(n-j)-K,0.0) for j in range(n+1)]
    for _ in range(n):
        vals = [(q*vals[j+1]+(1-q)*vals[j])/R for j in range(len(vals)-1)]
    return vals[0]
mx = 0.0
for n_ in (1,2,5,10,25,50,100,200,400):
    mx = max(mx, abs(tree_sum(100.0,100.0,0.05,1.0,0.2,n_)-tree_bi(100.0,100.0,0.05,1.0,0.2,n_)))
print("Theorem 2.3 sum vs backward induction max diff:", f"{mx:.3e}")
# Theorem 2.3 tree quantity sanity: n=1 one step, Lemma 2.2 condition for sigma=0.2, r=0.05, h=1 -> 1<16
print("h=1 < sigma^2/r^2=16:", 1 < 0.04/0.0025)
# Prop 1.4 parity identity check at a grid
mxp = 0.0
for K in (80.,100.,120.):
    for sig in (0.1,0.2,0.4):
        C,d1,d2 = bs(100.,K,0.05,1.,sig)
        P1 = C - 100 + K*math.exp(-0.05); P2 = K*math.exp(-0.05)*norm.cdf(-d2) - 100*norm.cdf(-d1)
        mxp = max(mxp, abs(P1-P2))
print("Prop 1.4 two forms max diff:", f"{mxp:.3e}")
# Prop 3.2 bisection: W/2^k first k, and bound tol/2 holds on random brackets
from scipy.optimize import brentq
random.seed(1)
worst = 0.0
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
    worst=max(worst, abs(mid-sig_true)/5e-11)
print("Prop 3.2 worst |err|/(tol/2) over random cases:", f"{worst:.4f}  (must be <= 1)")
