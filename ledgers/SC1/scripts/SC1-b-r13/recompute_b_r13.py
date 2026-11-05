"""Independent recomputation of every number printed or quoted on SC1 L04-L06 (slice b, round 13).

Uses only the standard library. Exact values come from fractions, math.comb and decimal;
floating-point values from math with the stated tolerance.
"""

import math
from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb

getcontext().prec = 40

print("== L04: Lemma 2.1 and Lab 1 closed forms (t = 2)")
for theta in (-1.0, 0.5, 2.0):
    closed = math.exp(theta * theta * 2 / 2)
    print(f"theta={theta:+.1f} exp(theta^2 t/2)={closed:.12f}")
print(f"e^1={math.e:.12f}  e^(1/4)={math.exp(0.25):.12f}  e^4={math.exp(4):.12f}")
print(f"e^8={math.exp(8):.12f}  (E2/E3 decimal, six places: {math.exp(8):.6f})")
print(f"e^4 check (quiz tolerance 1e-9 vs printed 54.598150033): {abs(math.exp(4) - 54.598150033):.3e}")
print(f"e (quiz tolerance 1e-9 vs printed 2.718281828): {abs(math.e - 2.718281828):.3e}")

print("== L04: second moment and variance identities (exact, symbolic by hand; numeric spot check)")
for th, t in [(0.5, 2.0), (2.0, 2.0), (2.0, 4.0), (1.0, 2.0)]:
    print(f"theta={th} t={t}: E[Z^2]=exp(theta^2 t)={math.exp(th*th*t):.6f}, Var(Z)={math.exp(th*th*t)-1:.6f}")

print("== L05: Gaussian quantities")
inv_sqrt_2pi = 1 / math.sqrt(2 * math.pi)
print(f"p_1(0,0)=(2pi)^(-1/2)={inv_sqrt_2pi:.10f} (quiz 0.3989, tol 1e-4)")
phi_neg = 0.5 * math.erfc((1 / math.sqrt(2)) / math.sqrt(2))  # Phi(-x) = erfc(x/sqrt2)/2
print(f"Phi(-1/sqrt2)={phi_neg:.10f} (quiz 0.23975, tol 1e-5; page says 0.23975006)")
print(f"erfc(1/sqrt2)={math.erfc(1 / math.sqrt(2)):.10f} (page 0.3173105079)")
print(f"P(B_1>1)=erfc(1/sqrt2)/2={math.erfc(1 / math.sqrt(2)) / 2:.12f} (page 0.1586552539)")
print(f"erfc(1/sqrt2)/2 halved from printed 0.3173105079 = {0.3173105079 / 2:.11f}")
print(f"P(B_1>=1) to four places = {math.erfc(1 / math.sqrt(2)) / 2:.4f} (quiz 0.1587 tol 1e-4)")
print(f"M1 integral: (2pi)^-1 sqrt(pi) = {math.sqrt(math.pi) / (2 * math.pi):.12f}; 1/(2 sqrt pi) = {1 / (2 * math.sqrt(math.pi)):.12f}")
print(f"E1 (A4(e)) check sqrt(pi)= {math.sqrt(math.pi):.12f}, int e^(-w^2) = {math.sqrt(math.pi):.12f}")

print("== L05 Lab 1 gaps: recompute with the same Simpson rule, then at higher precision for the printed magnitudes")


def density(u, x, y):
    return math.exp(-((y - x) ** 2) / (2.0 * u)) / math.sqrt(2.0 * math.pi * u)


def simpson(g, a, b, n):
    h = (b - a) / n
    total = g(a) + g(b)
    for i in range(1, n):
        total += (4.0 if i % 2 == 1 else 2.0) * g(a + i * h)
    return total * h / 3.0


times = (0.5, 1.0, 2.0)
points = (-1.0, -0.25, 0.0, 0.5, 1.0)
worst = 0.0
worst_tail = 0.0
cases = 0
worst_case = None
for s in times:
    for t in times:
        for x in points:
            for y in points:
                gap = simpson(lambda z: density(s, x, z) * density(t, z, y), -12.0, 12.0, 2000) - density(s + t, x, y)
                tail = simpson(lambda z: density(s, x, z) * density(t, z, y), 12.0, 40.0, 2000) + simpson(
                    lambda z: density(s, x, z) * density(t, z, y), -40.0, -12.0, 2000
                )
                cases += 1
                if abs(gap) > worst:
                    worst = abs(gap)
                    worst_case = (s, t, x, y)
                worst_tail = max(worst_tail, tail)
print(f"cases={cases} largest |gap|={worst:.3e} at {worst_case} largest tail mass={worst_tail:.3e}")
print(f"machine epsilon 2^-52={2.0**-52:.3e}; ratio largest gap / eps = {worst / 2.0**-52:.2f} (page: about 2.5 times eps 2.2e-16)")
print(f"ratio tail/gap = {worst_tail / worst:.3e}; page E1 ratio 5.55e-16/3.81e-29 = {5.55e-16 / 3.81e-29:.4e}")
example = simpson(lambda z: density(1.0, 0.5, z) * density(2.0, z, -0.25), -12.0, 12.0, 2000) - density(3.0, 0.5, -0.25)
print(f"example gap (s=1,t=2,x=0.5,y=-0.25) = {example:+.3e} (page -3.05e-16)")
print(f"E3 ratio |gap|/eps = {abs(example) / 2.0**-52:.3f} (page: about 1.4)")
for t in times:
    m = simpson(lambda y: density(t, 0.0, y), -12.0, 12.0, 2000)
    print(f"int p_{t:g}(0,y) over [-12,12] = {m:.12f}  (printed 1.0000000000)")

print("== L05 P2 and E2 bound: unrounded interval for printed 1.0000000000")
print(f"[{1.0 - 5e-11:.11f}, {1.0 + 5e-11:.11f}]")

print("== L06 exact enumerations by binomial counts (no walks listed)")
# S_N = 2u - N with u up-steps; count of sequences with S_N = b is comb(N, (N+b)//2) when parity matches.


def count_end(n, b):
    if (n + b) % 2 or abs(b) > n:
        return 0
    return comb(n, (n + b) // 2)


def count_max_ge(n, a):
    # reflection principle, but computed here independently by a DP over (position, max>=a flag)
    dp = {(0, False): 1}
    for _ in range(n):
        nxt = {}
        for (pos, hit), c in dp.items():
            for step in (1, -1):
                p2 = pos + step
                h2 = hit or (p2 >= a)
                nxt[(p2, h2)] = nxt.get((p2, h2), 0) + c
        dp = nxt
    return sum(c for (pos, hit), c in dp.items() if hit)


partA_total = 0
partA_equal = 0
for n in range(1, 13):
    for a in range(1, n + 1):
        for b in range(-n, a):
            partA_total += 1
            partA_equal += count_max_ge(n, a) >= 0 and sum(
                c for (pos, hit), c in _dp_max_end(n, a, b).items()
            ) == count_end(n, 2 * a - b) if False else 0
print("(Part A is checked below with an explicit DP over (position, hit) states)")


def dp_hits_end(n, a):
    dp = {(0, False): 1}
    for _ in range(n):
        nxt = {}
        for (pos, hit), c in dp.items():
            for step in (1, -1):
                p2 = pos + step
                h2 = hit or (p2 >= a)
                nxt[(p2, h2)] = nxt.get((p2, h2), 0) + c
        dp = nxt
    out = {}
    for (pos, hit), c in dp.items():
        if hit:
            out[pos] = out.get(pos, 0) + c
    return out


partA_total = 0
partA_equal = 0
partB_pairs = 0
partB_equal = 0
for n in range(1, 13):
    for a in range(1, n + 1):
        hits = dp_hits_end(n, a)
        for b in range(-n, a):
            partA_total += 1
            partA_equal += hits.get(b, 0) == count_end(n, 2 * a - b)
        partB_pairs += 1
        maxima = sum(hits.values())
        at_least = sum(count_end(n, b) for b in range(a, n + 1))
        above = sum(count_end(n, b) for b in range(a + 1, n + 1))
        partB_equal += maxima == at_least + above
print(f"Part A triples={partA_total} equal={partA_equal} (page 1014/1014)")
print(f"Part B pairs={partB_pairs} equal={partB_equal} (page 78/78)")
print(f"Part C N=12 a=3: #M>=3 = {sum(dp_hits_end(12, 3).values())} (page 1588 of 4096); #M>=3,S=2 = {dp_hits_end(12, 3).get(2, 0)} (page 495); #S=4 = {count_end(12, 4)} (page 495)")
print(f"Part D N=10 a=2: P(M>=2)={Fraction(sum(dp_hits_end(10, 2).values()), 1024)} (page 281/512); 2P(S>2)={Fraction(2*sum(count_end(10,b) for b in range(3,11)),1024)} (page 11/32); P(S=2)={Fraction(count_end(10,2),1024)} (page 105/512)")
print(f"Part D decimals: {float(Fraction(281,512)):.6f} {float(Fraction(11,32)):.6f} {float(Fraction(105,512)):.6f}")
print(f"Part D difference check: {Fraction(281,512) - Fraction(11,32) == Fraction(105,512)}")
print(f"E2 binomial: C(10,6)/1024 = {Fraction(comb(10,6),1024)}; 562/1024 - 352/1024 = {Fraction(562-352,1024)}")
print(f"M1 (N=3,a=1): #M>=1 = {sum(dp_hits_end(3,1).values())} of 8 (page 5); #S>=1={sum(count_end(3,b) for b in range(1,4))}, #S>1={sum(count_end(3,b) for b in range(2,4))}")
print(f"M2 (N=2,a=2): #M>=2 = {sum(dp_hits_end(2,2).values())} of 4 (page 1)")
print(f"Lab Part B pair count: sum_{{N=1..12}} N = {sum(range(1,13))} (page 78)")
print(f"Lab Part A triple count: {sum(a+n for n in range(1,13) for a in range(1,n+1))} (page 1014)")
print(f"Parity R1 example: count_end(3,2)={count_end(3,2)} count_end(3,2*1-2=0? b=2 a=1 -> 2a-b=0)={count_end(3,0)}")

print("== L06 M3 walk: steps (+1,+1,-1,-1,+1), a=2")
steps = (1, 1, -1, -1, 1)
S = [0]
for e in steps:
    S.append(S[-1] + e)
kappa = next(k for k, v in enumerate(S) if v == 2)
ref = list(steps[:kappa]) + [-e for e in steps[kappa:]]
Sp = [0]
for e in ref:
    Sp.append(Sp[-1] + e)
print(f"S={S} kappa={kappa} reflected steps={tuple(ref)} S'={Sp} (page: (0,1,2,3,4,3))")
print(f"2a-S_k for k>=kappa: {[4 - v for v in S[kappa:]]} vs S'[kappa:]={Sp[kappa:]}")

print("== L06 R2 sign flip and R3 positivity: nothing numeric beyond the above")
print("== L06 Part E: erfc(1/sqrt2) and half", f"{math.erfc(1/math.sqrt(2)):.10f}", f"{math.erfc(1/math.sqrt(2))/2:.10f}")
print("== L06 misconception 1 values", f"{math.erfc(1/math.sqrt(2)):.4f}", f"{math.erfc(1/math.sqrt(2))/2:.4f}")
print("== L06 Corollary 2.6 check by quadrature of the Gaussian tail (t=1,a=1)")
def tail_q(a, t, n=200000, upper=12.0):
    h = (upper - a / math.sqrt(t)) / n
    lo = a / math.sqrt(t)
    f = lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    total = f(lo) + f(lo + n * h)
    for i in range(1, n):
        total += (4 if i % 2 else 2) * f(lo + i * h)
    return total * h / 3
print(f"2*P(Z>1) by Simpson = {2 * tail_q(1.0, 1.0):.10f} vs erfc(1/sqrt2)={math.erfc(1/math.sqrt(2)):.10f}")
print(f"erfc(a/sqrt(2t)) at a=2,t=3 vs 2P(B_3>2): {math.erfc(2/math.sqrt(6)):.10f} vs {2*tail_q(2.0,3.0):.10f}")
