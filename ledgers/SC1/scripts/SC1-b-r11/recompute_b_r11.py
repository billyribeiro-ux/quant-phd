"""Independent recomputation of the numbers printed or stated in SC1 L04-L06 (round 11, slice b).

Standard library only. Run as: python -I -W error recompute_b_r11.py
"""
import math
from fractions import Fraction
from itertools import product
from collections import Counter

out = []


def say(s):
    out.append(s)
    print(s)


# ---- L06: discrete reflection, exact counts (independent code: explicit sequences, no shared helper)
triples = 0
triples_ok = 0
pairs_checked = 0
pairs_ok = 0
for n in range(1, 13):
    seqs = list(product((1, -1), repeat=n))
    paths = []
    for e in seqs:
        s = 0
        top = 0
        for x in e:
            s += x
            top = max(top, s)
        paths.append((top, s))
    for a in range(1, n + 1):
        cnt_max = sum(1 for t, _ in paths if t >= a)
        cnt_ge = sum(1 for _, s in paths if s >= a)
        cnt_gt = sum(1 for _, s in paths if s > a)
        pairs_checked += 1
        pairs_ok += cnt_max == cnt_ge + cnt_gt
        for b in range(-n, a):
            triples += 1
            lhs = sum(1 for t, s in paths if t >= a and s == b)
            rhs = sum(1 for _, s in paths if s == 2 * a - b)
            triples_ok += lhs == rhs
say(f"L06 Part A triples {triples} ok {triples_ok}  (page: 1014 / 1014)")
say(f"L06 Part B pairs {pairs_checked} ok {pairs_ok}  (page: 78 / 78)")

paths12 = []
for e in product((1, -1), repeat=12):
    s = 0
    top = 0
    for x in e:
        s += x
        top = max(top, s)
    paths12.append((top, s))
say(f"L06 Part C: M12>=3 count {sum(1 for t,_ in paths12 if t>=3)} (page 1588); M12>=3,S12=2 {sum(1 for t,s in paths12 if t>=3 and s==2)} (page 495); S12=4 {sum(1 for _,s in paths12 if s==4)} (page 495)")

# Part D: exact binomial route, independent of enumeration
def binom_prob_s_gt(n, k):  # P(S_n > k) for simple walk, S_n = 2U - n, U ~ Bin(n,1/2)
    total = 0
    for u in range(n + 1):
        if 2 * u - n > k:
            total += math.comb(n, u)
    return Fraction(total, 2 ** n)

N, A = 10, 2
p_s_gt = binom_prob_s_gt(N, A)
p_s_eq = Fraction(math.comb(N, (N + A) // 2), 2 ** N)  # S = A  <=> U = (N+A)/2
p_max = 2 * p_s_gt + p_s_eq
say(f"L06 Part D: 2P(S10>2) = {2*p_s_gt} (page 11/32); P(S10=2) = {p_s_eq} (page 105/512); P(M10>=2) = {p_max} (page 281/512)")
say(f"L06 Part D: difference equals P(S10=2): {p_max - 2*p_s_gt == p_s_eq}")

# Enumeration cross-check of Part D
cnt = Counter()
for e in product((1, -1), repeat=10):
    s = 0
    top = 0
    for x in e:
        s += x
        top = max(top, s)
    cnt[(top >= 2, s)] += 1
enum_max = Fraction(sum(v for (m, _), v in cnt.items() if m), 1024)
say(f"L06 Part D enumeration P(M10>=2) = {enum_max}: equals binomial route {enum_max == p_max}")

# ---- L06 Part E and misconception values
erfc1 = math.erfc(1 / math.sqrt(2))
say(f"L06 erfc(1/sqrt2) = {erfc1:.10f} (page 0.3173105079); half = {erfc1/2:.11f} (page prints 0.1586552539 for P(B1>1))")
say(f"L06 half unrounded {erfc1/2:.12f}")

# Closed form check of Corollary 2.6 by a direct tail integral (trapezoid, independent of erfc)
def tail_gauss(x, lo=None, hi=12.0, n=200000):
    # P(Z > x) = (1/sqrt(2pi)) int_x^hi exp(-z^2/2) dz
    h = (hi - x) / n
    total = 0.0
    for i in range(n + 1):
        z = x + i * h
        w = 0.5 if i in (0, n) else 1.0
        total += w * math.exp(-z * z / 2)
    return total * h / math.sqrt(2 * math.pi)

p_b1_gt1 = tail_gauss(1.0)
say(f"L06 Corollary 2.6 check: 2*P(B1>1) quadrature = {2*p_b1_gt1:.10f} vs erfc {erfc1:.10f}, diff {abs(2*p_b1_gt1-erfc1):.2e}")

# ---- L05 values
say(f"L05 p_1(0,0) = {1/math.sqrt(2*math.pi):.10f} (page 0.3989)")
say(f"L05 M1 integral = {1/(2*math.sqrt(math.pi)):.12f}; p_2(0,0) = {1/math.sqrt(4*math.pi):.12f}")
phi_m = 0.5 * math.erfc(-(-1 / math.sqrt(2)) / math.sqrt(2))
say(f"L05 q9 Phi(-1/sqrt2) = 0.5*erfc(1/2) = {0.5*math.erfc(0.5):.12f} (page 0.23975006...)")
say(f"L05 E1 ratio 5.55e-16/3.81e-29 = {5.55e-16/3.81e-29:.4e} (page 1.457e13)")
say(f"L05 E3 3.05e-16/eps = {3.05e-16/2.220446049250313e-16:.3f} (page about 1.4)")
say(f"L05 interp 5.55e-16/eps = {5.55e-16/2.220446049250313e-16:.3f} (page about 2.5)")

# Lemma 2.2 exact check at rational points (Fraction)
import random
rng = random.Random(11)
ok = True
for _ in range(2000):
    u = Fraction(rng.randint(1, 40), rng.randint(1, 40))
    v = Fraction(rng.randint(1, 40), rng.randint(1, 40))
    x = Fraction(rng.randint(-50, 50), rng.randint(1, 9))
    y = Fraction(rng.randint(-50, 50), rng.randint(1, 9))
    z = Fraction(rng.randint(-50, 50), rng.randint(1, 9))
    m = (v * x + u * y) / (u + v)
    lhs = (z - x) ** 2 / u + (y - z) ** 2 / v
    rhs = (u + v) / (u * v) * (z - m) ** 2 + (y - x) ** 2 / (u + v)
    ok = ok and lhs == rhs
say(f"L05 Lemma 2.2 identity exact at 2000 rational points: {ok}")
say("L05 P1 identity at u=1,v=3,x=0,y=1, z=0,1,2,3: " + str(all(Fraction(4*z*z-2*z+1,3) == Fraction(4,3)*(z-Fraction(1,4))**2+Fraction(1,4) for z in (0,1,2,3))))

# Exponential martingale and Lemma 2.1 at t=2 via trapezoid (independent of the twin)
def trap_exp(theta, t, shift, L=14.0, n=60000):
    h = 2 * L / n
    s = 0.0
    for i in range(n + 1):
        z = -L + i * h
        w = 0.5 if i in (0, n) else 1.0
        s += w * math.exp(theta * math.sqrt(t) * z - shift) * math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    return s * h

for th in (-1.0, 0.5, 2.0):
    mgf = trap_exp(th, 2.0, 0.0)
    mart = trap_exp(th, 2.0, th * th)
    say(f"L04 theta={th:+.1f}: trapezoid E[exp(theta B2)] = {mgf:.9f} vs e^(theta^2) = {math.exp(th*th):.9f}; E[Z_2]={mart:.9f}")

say(f"L04 e^(1/4) = {math.exp(0.25):.9f}; e^4 = {math.exp(4):.9f}; e^1 = {math.exp(1):.9f}; e^8 = {math.exp(8):.6f}")
say(f"L04 E1 page 1.284025417 vs e^0.25 {math.exp(0.25):.9f}")
say(f"L04 quiz e = {math.e:.12f} (tolerance 1e-9 around 2.718281828): diff {abs(math.e-2.718281828):.2e}")
say(f"L04 quiz e^4 diff {abs(math.exp(4)-54.598150033):.2e}")

# L04 M3 and P-variance formulas quick check: Var(Z)=e^{theta^2 t}-1 at theta=0 is 0
say("L04 M3 Var(Z_t) at theta=0 is 0 by construction (Z_t = 1)")

# L05 Problem M2 polynomial via Gaussian moments: E[(x+Z)^3] with Z~N(0,2)
# E[Z^2]=2, E[Z^3]=0 -> x^3+6x ; E[(x+Z)^2]=x^2+2
say("L05 M2: psi(x)=x^3+6x (k=3), x^2+2 (k=2) from E[Z^2]=2, E[Z^3]=0 (exact)")

# L06 Part E page text: erfc(1/sqrt2) rounded
say(f"L06 misconception: 2P(B1>1)={erfc1:.4f}, P(B1>=1)={erfc1/2:.4f}")
say("ALL DONE")
