"""Independent re-derivation of the LX1 L03 model numbers (verifier round 20, slice b).

Uses the closed form of Proposition 3.2(b) and an independent path computation, both with Fraction.
Prints the exact values and the half-up displayed values for the page's claims.
"""
from fractions import Fraction as F
import math

D = 1_000_000          # nominal debt, cents
K0 = 4_000_000         # baseline net worth, cents
C = K0 + D             # Proposition 3.2 constant
delta = F(1, 50)
H = 12


def half_up(x, places=0):
    s = math.floor(x * 10**places + F(1, 2))
    return s


def disp(x, places):
    s = half_up(x, places)
    w, f = divmod(s, 10**places)
    return f"{w}.{f:0{places}d}"


def V(m, t):
    # P_t = (1-delta)^min(t,m); V_t = D / P_t
    P = (1 - delta) ** min(t, m)
    return F(D) / P


def lam(x):
    return x / (C - x)


def depth_closed(m, phi=F(1), beta=F(1)):
    Vm = V(m, m)
    assert Vm < C, "Assumption 1.2 violated"
    return beta * phi * (lam(Vm) - lam(F(D)))


def depth_path(m, phi=F(1), beta=F(1)):
    best = None
    for t in range(H + 1):
        Vt = V(m, t)
        Kt = K0 - (Vt - D)
        Lt = Vt / Kt
        L0 = F(D) / K0
        ft = beta * phi * (Lt - L0)
        best = ft if best is None or ft > best else best
    return best


ok = True
for m in range(H + 1):
    a, b = depth_closed(m), depth_path(m)
    if a != b:
        ok = False
        print("MISMATCH closed vs path m", m)
print("closed form equals path maximum for all m 0..12:", ok)

dX, dY = depth_closed(12), depth_closed(4)
print("depth X exact (percent):", float(100 * dX), "displayed", disp(100 * dX, 2))
print("depth Y exact (percent):", float(100 * dY), "displayed", disp(100 * dY, 2))
print("difference X-Y exact (pp):", float(100 * (dX - dY)), "displayed", disp(100 * (dX - dY), 2))
print("difference of displayed depths:", disp(100 * dX, 2), disp(100 * dY, 2))
print("X deeper:", dX > dY)
for m in range(H + 1):
    print("m", m, "depth pct", disp(100 * depth_closed(m), 2), float(100 * depth_closed(m)))
print("never falls:", all(depth_closed(m) <= depth_closed(m + 1) for m in range(H)))
print("strict every step:", all(depth_closed(m) < depth_closed(m + 1) for m in range(H)))

for phi in (F(1, 2), F(1), F(3)):
    r = depth_closed(12, phi, F(1)) / depth_closed(4, phi, F(1))
    print("product", phi, "ratio exact", float(r), "displayed", disp(r, 4))

# Corollary 3.4 check: ratio is independent of beta and phi for several products
vals = set()
for phi in (F(1, 7), F(2), F(5, 3)):
    for beta in (F(1, 3), F(4)):
        vals.add(depth_closed(12, phi, beta) / depth_closed(4, phi, beta))
print("distinct ratios over 6 (phi,beta) pairs:", len(vals), "=", [float(v) for v in vals])

# Part A table independent check
print("baseline leverage", disp(F(D) / K0, 4))
for m in (12, 4):
    for t in range(H + 1):
        Vt = V(m, t)
        Kt = K0 - (Vt - D)
        Lt = Vt / Kt
        psi = Lt - F(D) / K0
        P = (1 - delta) ** min(t, m)
        print(f"m={m} t={t:2d} index {disp(P, 4)} realdebt {half_up(Vt)} lev {disp(Lt, 4)} prem {disp(psi, 4)} fall {disp(100*psi, 2)}")
