"""Verifier round 3, slice c: L08 bracket and monotonicity claims, recomputed with the stdlib only (no twin import)."""
import math


def Phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs(S, K, r, tau, sig):
    s = sig * math.sqrt(tau)
    d1 = (math.log(S / K) + (r + sig * sig / 2.0) * tau) / s
    d2 = d1 - s
    return S * Phi(d1) - K * math.exp(-r * tau) * Phi(d2)


S, r, tau = 100.0, 0.05, 1.0
# Bracket claim: prices strictly between L and S but within the top of the bracket are rejected by gap(HIGH) >= 0.
for K, p in ((100.0, 99.99999), (100.0, 99.99), (100.0, 99.999971), (120.0, 0.5), (80.0, 23.9100)):
    L = max(S - K * math.exp(-r * tau), 0.0)
    print(f"K={K} price={p}: L={L:.6f} C(1e-6)={bs(S,K,r,tau,1e-6):.10f} C(10)={bs(S,K,r,tau,10.0):.10f} "
          f"bracket_ok={bs(S,K,r,tau,1e-6) < p <= bs(S,K,r,tau,10.0) or bs(S,K,r,tau,1e-6) < p < bs(S,K,r,tau,10.0)}")
# Monotone and limits on a grid
Ks = (80.0, 100.0, 120.0)
for K in Ks:
    vals = [bs(S, K, r, tau, s) for s in [1e-6 * 1.5**i for i in range(60)] if s < 50]
    print(f"K={K} strictly increasing on grid: {all(b > a for a, b in zip(vals, vals[1:]))}; last={vals[-1]:.6f}")
    print(f"   C(1e-9)={bs(S,K,r,tau,1e-9):.8f} C(100)={bs(S,K,r,tau,100.0):.8f} L={max(S-K*math.exp(-r*tau),0):.6f}")
# Vega finite difference vs S phi(d1) sqrt(tau) at sigma=0.2, K=100
h = 1e-6
K, sig = 100.0, 0.2
fd = (bs(S, K, r, tau, sig + h) - bs(S, K, r, tau, sig - h)) / (2 * h)
d1 = (math.log(S / K) + (r + sig * sig / 2) * tau) / (sig * math.sqrt(tau))
print(f"vega finite diff={fd:.6f} formula={S*math.exp(-d1*d1/2)/math.sqrt(2*math.pi)*math.sqrt(tau):.6f}")
# E2 at K=120, sigma 0.10 unrounded cents
print(f"E2 120e^-0.05={120*math.exp(-0.05):.4f}; C(K=120,sig=0.10) cents={bs(S,120.0,r,tau,0.10)*100:.4f}")
# Lemma 2.2 limits
print("C(K=100, sigma=1e-9)=", bs(S,100.0,r,tau,1e-9), " C(K=100, sigma=1e4)=", bs(S,100.0,r,tau,1e4))
