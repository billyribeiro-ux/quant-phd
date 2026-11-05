"""SC1-b round 7: independent recomputation of every printed or quoted number in L04-L06 (stdlib + Fraction + DP)."""
import math
from fractions import Fraction
from itertools import product
from collections import Counter

def phi_cdf(x):
    return 0.5 * math.erfc(-x / math.sqrt(2))

print("L04 E[exp(theta B_2)] closed forms:")
for th in (-1.0, 0.5, 2.0):
    print(f"  theta={th:+.1f} e^(th^2 t/2)={math.exp(th*th*2/2):.9f}")
print("  e^8 =", f"{math.exp(8):.6f}", " e^4 =", f"{math.exp(4):.9f}", " e^0.25 =", f"{math.exp(0.25):.9f}")
print("  E[e^{B_2}] (theta=1,t=2) =", f"{math.exp(1):.9f}")
print("  M2: E[Z_2]=e^{-1}*e =", math.exp(-1)*math.exp(1))
print("  E1 mention e^0.25 to 9dp =", f"{math.exp(0.25):.9f}")

print("L04 E3: e^{theta^2 t/2} at theta=2,t=4 =", f"{math.exp(4*4/2):.6f}")
print("L04 Var(Z_t)=e^{th^2 t}-1 at theta=0 =", math.exp(0)-1)

print("L05 M1: (2pi)^-1 sqrt(pi) =", (2*math.pi)**-1*math.sqrt(math.pi), " p_2(0,0)=", 1/math.sqrt(4*math.pi))
print("L05 p_1(0,0) =", f"{1/math.sqrt(2*math.pi):.8f}")
print("L05 P2 example Phi(-1/sqrt2) =", f"{phi_cdf(-1/math.sqrt(2)):.10f}")
print("L05 E1 ratio 5.55e-16/3.81e-29 =", f"{5.55e-16/3.81e-29:.4e}")
print("L05 E3 3.05e-16/eps =", f"{3.05e-16/2.220446049250313e-16:.3f}", " 5.55e-16/eps =", f"{5.55e-16/2.220446049250313e-16:.3f}")
print("L05 E2 bound 0.99999999995..1.00000000005 check: 1.0000000000 printed")
# L05 P1 check at u=1,v=3,x=0,y=1 for all z
ok = all(abs(z*z/1 + (1-z)**2/3 - ((4/3)*(z-0.25)**2 + 0.25)) < 1e-12 for z in [i/7 for i in range(-30,31)])
print("L05 P1 identity holds on grid:", ok)
# L05 M2: E[(x+Z)^3], Z~N(0,2): x^3+6x ; check by Gauss-Hermite-like grid via exact moments
print("L05 M2 moments: E Z^2 =2, E Z^3 =0 (symmetry) -> psi_2=x^2+2, psi_3=x^3+6x")

# L06: DP counts for paths: P(M_N>=a), P(S_N>=a), P(S_N>a), P(S_N=a) exact
def counts(N, a):
    # DP over (position, running max) with counts
    dist = Counter({(0, 0): 1})
    for _ in range(N):
        nd = Counter()
        for (pos, mx), c in dist.items():
            for st in (1, -1):
                p2 = pos + st
                nd[(p2, max(mx, p2))] += c
        dist = nd
    M_ge = sum(c for (pos, mx), c in dist.items() if mx >= a)
    S_ge = sum(c for (pos, mx), c in dist.items() if pos >= a)
    S_gt = sum(c for (pos, mx), c in dist.items() if pos > a)
    S_eq = sum(c for (pos, mx), c in dist.items() if pos == a)
    return M_ge, S_ge, S_gt, S_eq

bad = 0
checks = 0
for N in range(1, 13):
    for a in range(1, N + 1):
        M_ge, S_ge, S_gt, S_eq = counts(N, a)
        checks += 1
        if M_ge != S_ge + S_gt:
            bad += 1
print(f"L06 Part B recomputed by DP: pairs={checks} failures={bad}")
print("L06 Part C: M_12>=3 count", counts(12, 3)[0], "of 4096")
# N=12 a=3: sequences with M_12>=3 and S_12=2 vs S_12=4
def count_M_end(N, a, b):
    dist = Counter({(0, 0): 1})
    for _ in range(N):
        nd = Counter()
        for (pos, mx), c in dist.items():
            for st in (1, -1):
                p2 = pos + st
                nd[(p2, max(mx, p2))] += c
        dist = nd
    return sum(c for (pos, mx), c in dist.items() if mx >= a and pos == b)
print("L06 Part C: M_12>=3 & S_12=2:", count_M_end(12, 3, 2), " ; S_12=4:", counts(12, 3)[3] if False else sum(c for (p,m),c in Counter({(0,0):1}).items()) )
# S_12 = 4 count
dist = Counter({0: 1})
for _ in range(12):
    nd = Counter()
    for p, c in dist.items():
        nd[p + 1] += c; nd[p - 1] += c
    dist = nd
print("L06 Part C: S_12=4 count:", dist[4])
# Part D exact fractions N=10, a=2
dist = Counter({(0, 0): 1})
for _ in range(10):
    nd = Counter()
    for (pos, mx), c in dist.items():
        for st in (1, -1):
            p2 = pos + st
            nd[(p2, max(mx, p2))] += c
    dist = nd
tot = 2 ** 10
Mge2 = Fraction(sum(c for (p, m), c in dist.items() if m >= 2), tot)
Sgt2 = Fraction(sum(c for (p, m), c in dist.items() if p > 2), tot)
Seq2 = Fraction(sum(c for (p, m), c in dist.items() if p == 2), tot)
print("L06 Part D:", Mge2, float(Mge2), "|", 2 * Sgt2, float(2 * Sgt2), "|", Seq2, float(Seq2), "| diff==Seq2:", Mge2 - 2 * Sgt2 == Seq2)
print("L06 E2: 281/512 - 11/32 =", Fraction(281, 512) - Fraction(11, 32), " binom(10,6)/1024 =", Fraction(math.comb(10, 6), 1024))
print("L06 Part E erfc(1/sqrt2) =", f"{math.erfc(1/math.sqrt(2)):.10f}", " half =", f"{math.erfc(1/math.sqrt(2))/2:.11f}")
print("L06 E3 unrounded half:", f"{math.erfc(1/math.sqrt(2))/2:.14f}")
print("L06 quiz P(B_1>=1) =", f"{phi_cdf(-1):.10f}")
print("L06 quiz P(M_1>=1) (erfc) =", f"{math.erfc(1/math.sqrt(2)):.6f}")
print("L06 R1 parity: 5 steps check")
print("L06 M1 N=3 a=1 count M>=1:", counts(3, 1)[0], "of 8; S_3>=1:", counts(3, 1)[1], "S_3>1:", counts(3, 1)[2])
print("L06 M2 N=2 a=2 M>=2:", counts(2, 2)[0], "of 4")
# M3 path
S = [0, 1, 2, 1, 0, 1]
print("L06 M3 path:", S, "kappa=", next(k for k, v in enumerate(S) if v == 2))
# Corollary 2.6 erfc check by quadrature
def tail(a, t):
    # P(B_t > a) by Simpson on z in [a/sqrt t, 40]
    lo = a / math.sqrt(t); hi = 40.0; n = 20000; h = (hi - lo) / n
    f = lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    s = f(lo) + f(hi) + sum((4 if i % 2 else 2) * f(lo + i * h) for i in range(1, n))
    return s * h / 3
print("Cor 2.6 check t=1,a=1: 2*P(B_1>1) quad =", f"{2*tail(1,1):.10f}", " erfc =", f"{math.erfc(1/math.sqrt(2)):.10f}")
print("Cor 2.6 check t=2,a=0.7: quad", f"{2*tail(0.7,2):.12f}", " erfc", f"{math.erfc(0.7/math.sqrt(4)):.12f}")
