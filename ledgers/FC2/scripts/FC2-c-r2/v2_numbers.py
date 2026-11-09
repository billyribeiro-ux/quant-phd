"""Independent re-derivation of every number in L07 and L08 (round 2). Uses scipy.stats.norm as a second Phi."""
import math
from scipy.stats import norm
from scipy.optimize import brentq

def Phi(x):
    return float(norm.cdf(x))

def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

def bs(S, K, r, tau, sig):
    s = sig * math.sqrt(tau)
    d1 = (math.log(S / K) + (r + sig * sig / 2) * tau) / s
    d2 = d1 - s
    return S * Phi(d1) - K * math.exp(-r * tau) * Phi(d2), d1, d2

def tree(S, K, r, tau, sig, n):
    h = tau / n
    u = math.exp(sig * math.sqrt(h)); d = 1 / u; R = math.exp(r * h)
    q = (R - d) / (u - d)
    # explicit sum (Theorem 2.3) as a second algorithm
    tot = 0.0
    for k in range(n + 1):
        tot += math.comb(n, k) * q**k * (1 - q)**(n - k) * max(S * u**k * d**(n - k) - K, 0.0)
    return math.exp(-r * tau) * tot, (u, d, R, q)

def cents_half_away(x):
    s = -1 if x < 0 else 1
    return s * math.floor(abs(x) * 100 + 0.5)

def cents_half_up(x):
    return math.floor(x * 100 + 0.5)

print("== L07")
S, K, r, tau, sig = 100.0, 100.0, 0.05, 1.0, 0.20
C, d1, d2 = bs(S, K, r, tau, sig)
print(f"d1={d1:.12f} d2={d2:.12f} Phi(d1)={Phi(d1):.6f} Phi(d2)={Phi(d2):.6f}")
print(f"C={C:.9f} cents={C*100:.6f} cents_rounded={cents_half_away(C)}")
P_parity = C - S + K * math.exp(-r * tau)
P_sep = K * math.exp(-r * tau) * Phi(-d2) - S * Phi(-d1)
print(f"Ke^-rt={K*math.exp(-r*tau):.9f} P_parity={P_parity:.9f} P_sep={P_sep:.9f} P_cents={P_parity*100:.4f} -> {cents_half_away(P_parity)}")
print(f"Phi(x)+Phi(-x)-1 at 0,0.35,1.7,3.0: {[Phi(x)+Phi(-x)-1 for x in (0.0,0.35,1.7,3.0)]}")
print(f"erf identity max err: {max(abs(Phi(x)-0.5*(1+math.erf(x/math.sqrt(2)))) for x in (-3,-1,0,0.35,1.7,3)):.2e}")
print(f"E1 / 400-step: cents error rounded ->")
rows = []
for n in (1, 2, 5, 10, 25, 50, 100, 200, 400):
    v, par = tree(S, K, r, tau, sig, n)
    err_unr = (v - C) * 100  # cents
    rows.append((n, v, err_unr))
    print(f"n={n:>3} tree={v:.9f} tree_cents_up={cents_half_up(v)} tree_cents_away={cents_half_away(v)} "
          f"err_cents_unr={err_unr:+.6f} err_printed={cents_half_away(v-C)} diff_printed={cents_half_away(v)-cents_half_away(C)} "
          f"u={par[0]:.9f} d={par[1]:.9f} R={par[2]:.9f} q={par[3]:.9f}")
signs = [(n, 1 if e > 0 else -1) for n, _, e in rows]
changes = sum(1 for (a, b) in zip(signs, signs[1:]) if a[1] != b[1])
print("sign pattern:", signs, "changes:", changes)
absl = [abs(e) for _, _, e in rows]
print("abs err monotone decreasing from n=1..400:", all(absl[i] > absl[i+1] for i in range(len(absl)-1)))
print("abs err monotone decreasing from n=2..400:", all(absl[i] > absl[i+1] for i in range(1, len(absl)-1)))
print("positive count", sum(1 for _, _, e in rows if e > 0), "negative", sum(1 for _, _, e in rows if e < 0))
print("smallest abs err row:", min(rows, key=lambda t: abs(t[2])))
# M3 q4 two ways
u4 = math.exp(0.1); d4 = 1/u4; R4 = math.exp(0.0125)
q_unr = (R4 - d4) / (u4 - d4)
print(f"M3 unrounded u={u4:.10f} d={d4:.10f} R={R4:.10f} q={q_unr:.10f} rounds6={q_unr:.6f}")
print(f"M3 six-place inputs quotient = {0.107741/0.200334:.10f} rounds6={round(0.107741/0.200334,6):.6f}")
print(f"M3 six-place quotient (R-d)/(u-d) with printed inputs 1.012578,0.904837,1.105171: {(1.012578-0.904837)/(1.105171-0.904837):.10f}")
print(f"M3 checks: h=0.25, sigma^2/r^2={0.2**2/0.05**2}")
# E3
u1 = math.exp(0.2); d1_ = 1/u1; R1 = math.exp(0.05); q1 = (R1 - d1_) / (u1 - d1_)
V1 = math.exp(-0.05) * q1 * (100 * u1 - 100)
print(f"E3 u1={u1:.9f} d1={d1_:.9f} R1={R1:.9f} q1={q1:.9f} up_payoff={100*u1-100:.9f} V1={V1:.9f} cents={V1*100:.6f} -> {cents_half_away(V1)}")
# R2
C2, _, _ = bs(100.0, 100.0, 0.0125, 4.0, 0.1)
print(f"R2 call tau=4 sig=0.1 r=0.0125: {C2:.10f} cents {cents_half_away(C2)}; sig*sqrt(tau)={0.1*2}, r*tau={0.0125*4}")
print(f"L07 Prop1.5 check: C(S=100,K=100,r=0.05,tau=1,sig=0.2)-C2 = {C-C2:.3e}")

print("== L08")
def L_bound(S, K, r, tau):
    return max(S - K * math.exp(-r * tau), 0.0)
print(f"L(K=100)={L_bound(100,100,0.05,1):.9f} L(K=80)={L_bound(100,80,0.05,1):.9f} L(K=120)={L_bound(100,120,0.05,1):.9f}")
print(f"100e^-0.05={100*math.exp(-0.05):.9f}, 120e^-0.05={120*math.exp(-0.05):.9f}")
print(f"vega K=100 sig=0.2: S*phi(d1)*sqrt(tau)={100*phi(0.35):.9f} ; 0.01/37.52={0.01/37.52:.10f}; 0.01/37.5240={0.01/37.5240:.10f}")
def bisect(price, K, tol=1e-10):
    lo, hi = 1e-6, 10.0
    gap = lambda s: bs(100.0, K, 0.05, 1.0, s)[0] - price
    if not (L_bound(100.0, K, 0.05, 1.0) < price < 100.0):
        raise ValueError("bounds")
    if not gap(lo) < 0 <= gap(hi):
        raise ValueError("bracket")
    halv = 0
    while hi - lo > tol:
        m = (lo + hi) / 2
        if gap(m) < 0: lo = m
        else: hi = m
        halv += 1
    return (lo + hi) / 2, halv
worst = 0
for K in (80.0, 100.0, 120.0):
    for sig in (0.10, 0.20, 0.40):
        p = bs(100.0, K, 0.05, 1.0, sig)[0]
        sh, hv = bisect(p, K)
        worst = max(worst, abs(sh - sig))
        print(f"K={K:.0f} sig={sig:.2f} price={p:.10f} cents={p*100:.4f} -> {cents_half_up(p)} recovered={sh:.10f} halvings={hv} abs_err={abs(sh-sig):.3e}")
print("worst", worst)
print(f"C(1e-6)-L at K=80,100,120: {[bs(100.0,K,0.05,1.0,1e-6)[0]-L_bound(100.0,K,0.05,1.0) for K in (80.0,100.0,120.0)]}")
print(f"C(1e-6) at K=80,100,120: {[repr(bs(100.0,K,0.05,1.0,1e-6)[0]) for K in (80.0,100.0,120.0)]}")
print(f"C(10) at K=100: {bs(100.0,100.0,0.05,1.0,10.0)[0]:.10f}; C(10)<99.99995? {bs(100.0,100.0,0.05,1.0,10.0)[0] < 99.99995}")
print(f"C(10) at K=100 rounded 6dp: {bs(100.0,100.0,0.05,1.0,10.0)[0]:.6f}")
try:
    print("bisect(99.99995,100):", bisect(99.99995, 100.0))
except ValueError as e:
    print("bisect(99.99995,100) raises ValueError:", e)
print("C(10) at K=80, K=120:", bs(100.0,80.0,0.05,1.0,10.0)[0], bs(100.0,120.0,0.05,1.0,10.0)[0])
p120 = bs(100.0, 120.0, 0.05, 1.0, 0.10)[0]
print(f"K=120 sig=0.10 price {p120:.10f} cents {p120*100:.4f}")
try:
    s05, h05 = bisect(0.50, 120.0)
    print(f"E3 price 0.50 K=120: sigma={s05:.8f} halvings={h05} residual={bs(100.0,120.0,0.05,1.0,s05)[0]-0.50:.3e}")
except ValueError as e:
    print("E3 raises", e)
print("E3 C(1e-6) at K=120:", bs(100.0,120.0,0.05,1.0,1e-6)[0], " C(10):", bs(100.0,120.0,0.05,1.0,10.0)[0])
W = 10 - 1e-6
print(f"M3 log2(W/tol)={math.log2(W/1e-10):.4f} W/2^36={W/2**36:.4e} W/2^37={W/2**37:.4e} 10/2^36={10/2**36:.4e}")
k = 0
while W / 2**k > 1e-10: k += 1
print("first k with W/2^k<=tol:", k)
print("ceil log2:", math.ceil(math.log2(W/1e-10)))
print(f"100 at strike 100 vs bounds; L=4.8771 display check: {L_bound(100,100,0.05,1):.4f}")
print(f"4.90 in (L,S)? {L_bound(100,100,0.05,1) < 4.90 < 100}")
# Lower-end reachability: any price p with L < p <= C(1e-6)?
for K in (80.0, 100.0, 120.0):
    Lb = L_bound(100.0, K, 0.05, 1.0); c = bs(100.0, K, 0.05, 1.0, 1e-6)[0]
    print(f"K={K:.0f}: L={Lb!r} C(1e-6)={c!r} window (L, C(1e-6)] nonempty: {Lb < c}")
