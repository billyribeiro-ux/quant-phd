"""Round-5 independent re-derivation of every number printed in prose or in quiz answers of L04-L06.
Uses its own code (not the lab twins) and exact Fractions where the claim is a count or a fraction.
Run as: python3 -I ledgers/SC1/scripts/SC1-b-r5/recompute_r5.py"""

import math
from fractions import Fraction
from itertools import product

out = []


def line(s: str) -> None:
    out.append(s)
    print(s)


# ---- L04 exponentials and quadrature
line(f"e^(1/4) = {math.exp(0.25):.12f} -> 9 dp {math.exp(0.25):.9f} (L04:224, E1 print 1.284025417)")
line(f"e^1 = {math.e:.12f} -> 9 dp {math.e:.9f}; |2.718281828 - e| = {abs(2.718281828 - math.e):.3e} (<=1e-9 Q6 ok)")
line(f"e^4 = {math.exp(4):.12f} -> 9 dp {math.exp(4):.9f}; |54.598150033 - e^4| = {abs(54.598150033 - math.exp(4)):.3e} (Q10 ok)")
line(f"e^8 = {math.exp(8):.12f} -> 6 dp {math.exp(8):.6f} (E2, E3 print 2980.957987)")
# Lemma 2.1 with h=t=2: E[e^{theta B_2}] = e^{theta^2 t/2}; theta=0.5 -> e^{0.25}; theta=2 -> e^4; theta=-1 -> e^1
for th, t in [(-1.0, 2.0), (0.5, 2.0), (2.0, 2.0)]:
    line(f"closed form theta={th}, t={t}: exp(theta^2 t/2) = {math.exp(th * th * t / 2):.9f}")
line(f"E3 check: theta=2, t=4: exp(theta^2 t/2) = exp(8) = {math.exp(8):.6f}")

# ---- L04 Q: E[e^{2 theta B_t}] etc are algebra; check exp identity used in Prop 2.4 second moment
for th in (-1.0, 0.5, 2.0):
    for t in (0.5, 1.0, 2.0):
        lhs = math.exp(-th * th * t) * math.exp((2 * th) ** 2 * t / 2)
        assert abs(lhs - math.exp(th * th * t)) < 1e-12 * lhs
line("Prop 2.4 second moment identity e^{-th^2 t} e^{2 th^2 t} = e^{th^2 t}: holds on grid")

# ---- L05 values
def phi(z: float) -> float:
    return math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)


def Phi(z: float) -> float:
    return 0.5 * math.erfc(-z / math.sqrt(2))


line(f"L05 Q4 p_1(0,0) = 1/sqrt(2pi) = {1 / math.sqrt(2 * math.pi):.10f} -> 4 dp 0.3989 (tol 1e-4: diff {abs(1 / math.sqrt(2 * math.pi) - 0.3989):.2e})")
line(f"L05 M1 p_2(0,0) = (4pi)^(-1/2) = {(4 * math.pi) ** -0.5:.10f}; 1/(2 sqrt(pi)) = {1 / (2 * math.sqrt(math.pi)):.10f}")
line(f"L05 M1 integral (2pi)^-1 sqrt(pi) = {math.sqrt(math.pi) / (2 * math.pi):.10f} vs 1/(2sqrt pi) = {1 / (2 * math.sqrt(math.pi)):.10f}")
line(f"L05 Q9 Phi(-1/sqrt2) = {Phi(-1 / math.sqrt(2)):.10f} -> 5 dp 0.23975; tol 1e-5 diff {abs(Phi(-1 / math.sqrt(2)) - 0.23975):.2e}")
line(f"L05 E3 gap ratio: 3.05e-16/2.22e-16 = {3.05 / 2.22:.3f} (about 1.4); eps = {2.220446049250313e-16:.4e}; 5.55e-16/eps = {5.55e-16 / 2.220446049250313e-16:.3f} (about 2.5)")
line(f"L05 E1 ratio 5.55e-16/3.81e-29 = {5.55e-16 / 3.81e-29:.4e} (1.5e13 to two s.f.)")

# L05 M2 conditional moments: E[(x+Z)^k], Z~N(0,2): k=2 -> x^2+2, k=3 -> x^3+6x
import random  # noqa: E402  (stdlib, deterministic seed for a Monte Check of identity only)

rng = random.Random(12345)
xs = [0.3, -1.2, 0.0]
for x in xs:
    # exact formulas
    e2 = x * x + 2.0
    e3 = x ** 3 + 6.0 * x
    # Gauss-Hermite-free check: integrate (x+z)^k phi_2(z) by Simpson on wide grid
    def integ(k: int) -> float:
        n = 40000
        a, b = -40.0, 40.0
        h = (b - a) / n
        tot = 0.0
        for i in range(n + 1):
            z = a + i * h
            w = 1 if i in (0, n) else (4 if i % 2 else 2)
            dens = math.exp(-z * z / 4.0) / math.sqrt(4 * math.pi)
            tot += w * ((x + z) ** k) * dens
        return tot * h / 3
    assert abs(integ(2) - e2) < 1e-6 and abs(integ(3) - e3) < 1e-6, (x, integ(2), integ(3))
line("L05 M2 psi(x)=x^2+2 and x^3+6x confirmed by Simpson on N(0,2) for x in {0.3,-1.2,0}")

# Theorem 2.1 and Lemma 2.2 checks at random points (independent of lab code)
def p(u: float, x: float, y: float) -> float:
    return math.exp(-((y - x) ** 2) / (2 * u)) / math.sqrt(2 * math.pi * u)

worst_ck = 0.0
for _ in range(200):
    u, v = rng.uniform(0.2, 3), rng.uniform(0.2, 3)
    x, y = rng.uniform(-2, 2), rng.uniform(-2, 2)
    m = (v * x + u * y) / (u + v)
    for z in (rng.uniform(-3, 3),):
        lhs = (z - x) ** 2 / u + (y - z) ** 2 / v
        rhs = (u + v) / (u * v) * (z - m) ** 2 + (y - x) ** 2 / (u + v)
        assert abs(lhs - rhs) < 1e-9 * max(1, abs(lhs))
    # Chapman-Kolmogorov with a wider Simpson grid than the lab (independent check)
    n = 6000
    a, b = -30.0, 30.0
    h = (b - a) / n
    tot = 0.0
    for i in range(n + 1):
        z = a + i * h
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        tot += w * p(u, x, z) * p(v, z, y)
    tot *= h / 3
    worst_ck = max(worst_ck, abs(tot - p(u + v, x, y)))
line(f"Lemma 2.2 identity: 200 random points, exact to 1e-9 relative (asserted)")
line(f"Theorem 2.1 independent Simpson check, 200 random (u,v,x,y): worst |gap| = {worst_ck:.3e}")

# ---- L05 E2 claim: integral over [-12,12] of p_t(0,y) within 5e-11 of 1 at printed digits
for t in (0.5, 1.0, 2.0):
    n = 20000
    a, b = -12.0, 12.0
    h = (b - a) / n
    tot = 0.0
    for i in range(n + 1):
        y = a + i * h
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        tot += w * p(t, 0.0, y)
    tot *= h / 3
    line(f"integral p_{t}(0,y) over [-12,12] (n=20000) = {tot:.12f}; exceeds 1 by {abs(tot - 1):.2e}")

# ---- L05 Lemma 1.3 / R3: rho_n bounds for a sample of rho values
for rho in (0.0, 0.1234, 0.5, 0.999999):
    for n_ in (1, 3, 8):
        rho_n = math.ceil((2**n_) * rho) / 2**n_
        assert rho <= rho_n < rho + 2 ** (-n_)
line("R3 bounds rho <= rho_n < rho + 2^-n confirmed on sample")

# ---- L06 counts (independent: DP over endpoints and running maximum)
def counts(n: int):
    # dp over (position, running max) -> number of sequences
    from collections import defaultdict

    dp = defaultdict(int)
    dp[(0, 0)] = 1
    for _ in range(n):
        nd = defaultdict(int)
        for (pos, mx), c in dp.items():
            for st in (1, -1):
                np_ = pos + st
                nd[(np_, max(mx, np_))] += c
        dp = nd
    return dp


tot_triples = 0
eq_triples = 0
tot_pairs = 0
eq_pairs = 0
for n in range(1, 13):
    dp = counts(n)
    for a in range(1, n + 1):
        tot_pairs += 1
        m_ge = sum(c for (pos, mx), c in dp.items() if mx >= a)
        s_ge = sum(c for (pos, mx), c in dp.items() if pos >= a)
        s_gt = sum(c for (pos, mx), c in dp.items() if pos > a)
        eq_pairs += int(m_ge == s_ge + s_gt)
        for b in range(-n, a):
            tot_triples += 1
            lhs = sum(c for (pos, mx), c in dp.items() if mx >= a and pos == b)
            rhs = sum(c for (pos, mx), c in dp.items() if pos == 2 * a - b)
            eq_triples += int(lhs == rhs)
line(f"L06 Part A (DP): triples {tot_triples}, equal {eq_triples} (expect 1014, 1014)")
line(f"L06 Part B (DP): pairs {tot_pairs}, equal {eq_pairs} (expect 78, 78)")
dp12 = counts(12)
m12 = sum(c for (pos, mx), c in dp12.items() if mx >= 3)
m12s2 = sum(c for (pos, mx), c in dp12.items() if mx >= 3 and pos == 2)
s12_4 = sum(c for (pos, mx), c in dp12.items() if pos == 4)
line(f"L06 Part C (DP, N=12, a=3): M>=3: {m12} of {2**12} (expect 1588); M>=3&S=2: {m12s2}; S=4: {s12_4} (expect 495, 495)")

# Part D exact fractions by independent binomial route
N = 10
tail_fr = Fraction(sum(c for (pos, mx), c in counts(N).items() if mx >= 2), 2**N)
above = Fraction(sum(c for (pos, mx), c in counts(N).items() if pos > 2), 2**N)
at = Fraction(sum(c for (pos, mx), c in counts(N).items() if pos == 2), 2**N)
binom_at = Fraction(math.comb(10, 6), 2**10)
line(f"L06 Part D: P(M10>=2)={tail_fr} (281/512); 2P(S10>2)={2 * above} (11/32); P(S10=2)={at} (105/512); C(10,6)/1024={binom_at}")
assert tail_fr - 2 * above == at == binom_at
line("L06 Part D identity holds exactly; 281/512 - 11/32 = 105/512 = C(10,6)/1024 (E2 arithmetic)")
line(f"L06 E2 arithmetic: 562/1024 - 352/1024 = {Fraction(562 - 352, 1024)} = 210/1024")

# Enumerated M1 (N=3,a=1) and M2 (N=2,a=2) by brute force
cnt = 0
for steps in product((1, -1), repeat=3):
    s = 0
    mx = 0
    for st in steps:
        s += st
        mx = max(mx, s)
    cnt += mx >= 1
line(f"L06 M1 brute force: {cnt} of 8 have M_3>=1 (expect 5)")
cnt2 = sum(1 for steps in product((1, -1), repeat=2) if max(0, steps[0], steps[0] + steps[1]) >= 2)
line(f"L06 M2 brute force: {cnt2} of 4 have M_2>=2 (expect 1)")

# Part E
two_tail = math.erfc(1 / math.sqrt(2))
line(f"L06 Part E: erfc(1/sqrt2) = {two_tail:.10f} (expect 0.3173105079); half = {two_tail / 2:.11f}; 0.3173105079/2 = {0.3173105079 / 2:.11f}")
line(f"L06 Cor 2.6 check: 2P(B_1>1) via Phi: {2 * (1 - Phi(1.0)):.10f}")
line(f"L06 P(B_1>=1) = {1 - Phi(1.0):.10f} -> 4 dp 0.1587 (quiz tol 1e-4 diff {abs(1 - Phi(1.0) - 0.1587):.2e})")
line(f"L06 M1 example P(M_1>=1) = erfc value {two_tail:.6f} -> 4 dp 0.3173")

# Remark: S_N parity check R1
line("R1 parity: every S_N has parity of N (brute force N<=8 checked below)")
for N_ in range(1, 9):
    for steps in product((1, -1), repeat=N_):
        assert sum(steps) % 2 == N_ % 2
line("R1 parity holds for N<=8 (brute force)")

with open("/Users/billyribeiro/.fanout/wt/verifyE5-SC1-b/ledgers/SC1/scripts/SC1-b-r5/out/recompute_r5.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
