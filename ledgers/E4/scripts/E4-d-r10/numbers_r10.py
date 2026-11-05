import math
from decimal import Decimal, getcontext
getcontext().prec = 50
A, TV, TE = 2.0, 1.0, 1.0

def ty(lam, sd):
    return lam*lam*TE*TE/(lam*lam*TE + A*A*sd*sd)

def coeffs(lam, sd):
    t = ty(lam, sd)
    d = lam*(TV+TE) + (1-lam)*(TV+t)
    bs = (lam*TE + (1-lam)*t)/d
    return bs, -A*bs/(lam*TE), t

def FU(lam, sd):
    bs, bu, t = coeffs(lam, sd)
    r = t/(TV+t) - bs
    return math.pow(1 + r*r*(TV+t)*(1/TV+1/t), -0.5)

def FI(lam, sd):
    bs, bu, t = coeffs(lam, sd)
    P = TV+TE
    slope = TE/P - bs
    vg = slope*slope*(1/TV+1/TE) + bu*bu*sd*sd
    return math.pow(1 + P*vg, -0.5)

def G(lam, sd, c):
    return FU(lam, sd) - math.exp(A*c)*FI(lam, sd)

def G0(sd, c):
    u = math.pow(1 + A*A*sd*sd/TV, -0.5)
    i = math.pow(1 + TE/TV + (TV+TE)*A*A*sd*sd/(TV*TV), -0.5)
    return u - math.exp(A*c)*i

# high-precision limit via Decimal for G at small lam is hard; use exact-limit formula in Decimal for G0 check
def G0_dec(sd, c):
    sd = Decimal(repr(sd)); c = Decimal(repr(c))
    a2s2 = 4*sd*sd
    u = (1 + a2s2)**Decimal(-0.5)
    i = (1 + 1 + 2*a2s2)**Decimal(-0.5)
    e = (2*c).exp()
    return u - e*i

print("tau_bar(0.150)=%.10f tau_bar(0.120)=%.10f" % (2*math.exp(-0.6)-1, 2*math.exp(-0.48)-1))
print("tau_y(1) min over sd<=0.75: %.8f" % (1/(1+4*0.75**2)))
# test pairs: diff of G(1e-12) from G(0) and G0 vs Decimal limit
for sd, c in [(0.5,0.30),(0.6,0.30),(0.75,0.30),(0.5,0.50),(0.6,0.50),(0.75,0.50)]:
    g0 = G0(sd, c)
    g_small = G(1e-12, sd, c)
    print(f"sd={sd} c={c}: G0={g0:+.17e} G(1e-12)={g_small:+.17e} |diff|={abs(g_small-g0):.3e} ; G(1e-9)-G0={G(1e-9,sd,c)-g0:+.3e}; dec-limit-minus-G0={float(G0_dec(sd,c))-g0:+.3e}")

print("--- Lab 3 table re-derived (independent float code in numbers_r10.py) ---")
def closed(sd, c):
    t = 2*math.exp(-4*c) - 1
    if t <= 0: return 0.0
    if t >= 1/(1+4*sd*sd): return 1.0
    return 2*sd*math.sqrt(t/(1-t))
def bisect(sd, c):
    if G0(sd, c) <= 0: return 0.0
    if G(1.0, sd, c) >= 0: return 1.0
    lo, hi = 0.0, 1.0; n = 0
    while hi - lo > 1e-12*hi and n < 200:
        m = 0.5*(lo+hi)
        if G(m, sd, c) > 0: lo = m
        else: hi = m
        n += 1
    return 0.5*(lo+hi)
worst = 0.0
for sd in (0.5, 0.625, 0.75):
    for c in (0.120, 0.135, 0.150):
        lam = bisect(sd, c); cf = closed(sd, c)
        tyv = lam*lam/(lam*lam+4*sd*sd)
        pi = tyv/(1+tyv) if lam>0 else 0.0
        gap = G(lam, sd, c) if 0 < lam < 1 else G0(sd,c)
        worst = max(worst, abs(lam-cf))
        print(f"{sd:.3f} {c:.3f} lam={lam:.6f} pi={pi:.4f} closed={cf:.6f} gap={gap:+.2e} ratio_pi_closed={1-math.exp(2*A*c)/2 - pi:+.1e}")
print("max |bisect - closed| = %.2e" % worst)
print("ratios at c=0.120:", bisect(0.625,0.120)/bisect(0.5,0.120), bisect(0.75,0.120)/bisect(0.5,0.120))
print("displayed ratios:", round(0.6978/0.5582,5), round(0.8373/0.5582,5))
inside = sum(1 for i in range(22) for j in range(22) if G0(0.5+0.25*i/21, 0.12+0.03*j/21) > 0 and G(1.0, 0.5+0.25*i/21, 0.12+0.03*j/21) < 0)
print("box grid interior:", inside, "of 484")
