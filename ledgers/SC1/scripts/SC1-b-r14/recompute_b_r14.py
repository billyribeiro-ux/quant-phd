"""Independent re-derivation of every number in SC1 slice b (L04, L05, L06) at round 14.

Written by the round-14 verifier for SC1 slice b. It does not import the lab twins.
Each block states the page locator it checks. Run: .venv/bin/python <this file>
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import product

print("== L04 closed forms (page: L04.html Lab 1 output, Lemma 2.1, E2, E3, quiz)")
for name, value in [
    ("e^1", math.exp(1.0)),
    ("e^(1/4)", math.exp(0.25)),
    ("e^4", math.exp(4.0)),
    ("e^8", math.exp(8.0)),
]:
    print(f"{name} = {value:.12f}")

print("\n== L04 quadrature by trapezoid (independent of the twin's Simpson rule)")
N_TRAP = 200_000
LIM = 14.0


def phi(z: float) -> float:
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def trap(f, lo: float, hi: float, n: int) -> float:
    h = (hi - lo) / n
    total = 0.5 * (f(lo) + f(hi))
    for i in range(1, n):
        total += f(lo + i * h)
    return total * h


for theta in (-1.0, 0.5, 2.0):
    t = 2.0
    mgf = trap(lambda z: math.exp(theta * math.sqrt(t) * z) * phi(z), -LIM, LIM, N_TRAP)
    closed = math.exp(theta * theta * t / 2.0)
    mart = trap(lambda z: math.exp(theta * math.sqrt(t) * z - theta * theta * t / 2.0) * phi(z), -LIM, LIM, N_TRAP)
    rel = abs(mgf - closed) / closed
    print(
        f"theta={theta:+.1f}: trap E[exp(theta B_2)]={mgf:.12f} closed={closed:.12f} rel_err={rel:.2e}; "
        f"trap E[Z_2]={mart:.12f} abs_err_vs_1={abs(mart - 1.0):.2e}"
    )

print("\n== L04 Lemma 2.1 check at h=2 (E[exp(th Y)] = exp(th^2 h/2)), exact-moment route")
for theta in (1.0, 2.0):
    # E[e^{theta Y}] = sum_k theta^k E[Y^k]/k! with E[Y^(2m)] = (2m-1)!! h^m
    h = 2.0
    series = 0.0
    for k in range(0, 60):
        if k % 2:
            continue
        m = k // 2
        dfact = 1
        for j in range(1, 2 * m, 2):
            dfact *= j
        series += (theta**k) * dfact * (h**m) / math.factorial(k)
    print(f"theta={theta}: series={series:.12f} closed={math.exp(theta * theta * h / 2):.12f}")

print("\n== L04 E[B_t^4]=3t^2 at t=3 (quiz) and M1 values")
print("E[B_3^4] =", 3 * 3**2)

print("\n== L05 Chapman-Kolmogorov, independent trapezoid on [-12,12] with 4000 cells")


def p(u: float, x: float, y: float) -> float:
    return math.exp(-((y - x) ** 2) / (2.0 * u)) / math.sqrt(2.0 * math.pi * u)


TIMES = (0.5, 1.0, 2.0)
POINTS = (-1.0, -0.25, 0.0, 0.5, 1.0)
worst_gap = 0.0
worst_tail = 0.0
cases = 0
for s in TIMES:
    for t in TIMES:
        for x in POINTS:
            for y in POINTS:
                integral = trap(lambda z: p(s, x, z) * p(t, z, y), -12.0, 12.0, 4000)
                gap = abs(integral - p(s + t, x, y))
                worst_gap = max(worst_gap, gap)
                tail = trap(lambda z: p(s, x, z) * p(t, z, y), 12.0, 40.0, 4000) + trap(
                    lambda z: p(s, x, z) * p(t, z, y), -40.0, -12.0, 4000
                )
                worst_tail = max(worst_tail, tail)
                cases += 1
print(f"cases={cases} largest trapezoid gap={worst_gap:.3e} largest tail mass (12..40)={worst_tail:.3e}")
print(f"ratio gap/tail = {worst_gap / worst_tail if worst_tail else float('inf'):.4e}")
print(f"machine epsilon 2^-52 = {2.0**-52:.3e}; largest gap / eps = {worst_gap / 2.0**-52:.2f}")
print(f"5.55e-16 / 2.2e-16 = {5.55e-16 / 2.2e-16:.3f}; 5.55e-16/3.81e-29 = {5.55e-16 / 3.81e-29:.4e}")
print(f"example -3.05e-16 / 2.2e-16 = {3.05e-16 / 2.2e-16:.3f} (page: about 1.4)")
for t in TIMES:
    print(f"integral p_{t}(0,y) over [-12,12] = {trap(lambda y: p(t, 0.0, y), -12.0, 12.0, 4000):.14f}")

print("\n== L05 quiz / problem values")
Phi = lambda v: 0.5 * math.erfc(-v / math.sqrt(2.0))  # noqa: E731
print(f"Phi(-1/sqrt2) = {Phi(-1 / math.sqrt(2)):.12f} (quiz 0.23975006..., 5 dp 0.23975)")
print(f"p_1(0,0) = {p(1.0, 0.0, 0.0):.12f} (quiz 0.39894..., 4 dp 0.3989)")
print(f"M1: integral p_1(0,z)p_1(z,0) dz vs 1/(2 sqrt pi) = {1 / (2 * math.sqrt(math.pi)):.12f}")
print(f"M2 check: E[(x+Z)^3] with Z~N(0,2) gives x^3+6x; at x=1 -> {1 + 6} ; direct trap:")
Z2 = lambda z: (1 + math.sqrt(2) * z) ** 3 * phi(z)  # noqa: E731
print(f"  trap E[(1+sqrt2 Z)^3] = {trap(Z2, -LIM, LIM, 200_000):.9f}")
print(f"E1: 5.55e-16/3.81e-29 = {5.55e-16 / 3.81e-29:.4e} (page 1.457e13, 'about 1.5e13')")
print(f"E2: unrounded interval [0.99999999995, 1.00000000005] width/2 = 5e-11")

print("\n== L06 exact enumeration by DP over (position, running max) with integers (independent of the twin)")


def dp_counts(n: int) -> dict[tuple[int, int], int]:
    """Map (running max M_n, endpoint S_n) to the number of step sequences of length n."""
    counts: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (mx, pos), c in counts.items():
            for step in (1, -1):
                newpos = pos + step
                newmx = max(mx, newpos)
                key = (newmx, newpos)
                nxt[key] = nxt.get(key, 0) + c
        counts = nxt
    return counts


partA_triples = 0
partA_equal = 0
partB_pairs = 0
partB_equal = 0
for n in range(1, 13):
    cnt = dp_counts(n)
    end_counts: dict[int, int] = {}
    for (_, e), c in cnt.items():
        end_counts[e] = end_counts.get(e, 0) + c
    for a in range(1, n + 1):
        for b in range(-n, a):
            lhs = sum(c for (mx, e), c in cnt.items() if mx >= a and e == b)
            rhs = end_counts.get(2 * a - b, 0)
            partA_triples += 1
            partA_equal += lhs == rhs
        partB_pairs += 1
        maxima = sum(c for (mx, _), c in cnt.items() if mx >= a)
        at_least = sum(c for (_, e), c in cnt.items() if e >= a)
        above = sum(c for (_, e), c in cnt.items() if e > a)
        partB_equal += maxima == at_least + above
print(f"Part A triples={partA_triples} equal={partA_equal} (page 1014/1014)")
print(f"Part B pairs={partB_pairs} equal={partB_equal} (page 78/78)")

cnt12 = dp_counts(12)
ge3 = sum(c for (mx, _), c in cnt12.items() if mx >= 3)
ge3_end2 = sum(c for (mx, e), c in cnt12.items() if mx >= 3 and e == 2)
end4 = sum(c for (_, e), c in cnt12.items() if e == 4)
print(f"Part C: M_12>=3: {ge3} of {2**12}; M_12>=3,S_12=2: {ge3_end2}; S_12=4: {end4} (page 1588, 495, 495)")

cnt10 = dp_counts(10)
total = 2**10
tail = Fraction(sum(c for (mx, _), c in cnt10.items() if mx >= 2), total)
above = Fraction(sum(c for (_, e), c in cnt10.items() if e > 2), total)
at2 = Fraction(sum(c for (_, e), c in cnt10.items() if e == 2), total)
print(f"Part D: P(M_10>=2)={tail} ({float(tail):.6f}); 2P(S_10>2)={2 * above} ({float(2 * above):.6f}); "
      f"P(S_10=2)={at2} ({float(at2):.6f}); identity={tail - 2 * above == at2}")
print(f"  page: 281/512 0.548828; 11/32 0.343750; 105/512 0.205078")
print(f"  binomial(10,6)/1024 = {math.comb(10, 6)}/1024 = {Fraction(math.comb(10, 6), 1024)}")

print("\n== L06 Part E and misconception / quiz values")
print(f"2P(B_1>1) = erfc(1/sqrt2) = {math.erfc(1 / math.sqrt(2)):.12f} (page 0.3173105079)")
print(f"P(B_1>1) = {math.erfc(1 / math.sqrt(2)) / 2:.12f} (page 0.1586552539; unrounded half 0.15865525393)")
print(f"P(B_1>=1) to 4 dp = {math.erfc(1 / math.sqrt(2)) / 2:.4f} (quiz 0.1587)")

print("\n== L06 M1 (N=3, a=1), M2 (N=2, a=2), M3 (path reflection) by brute force")
cnt = 0
for steps in product((1, -1), repeat=3):
    s = 0
    top = 0
    for e in steps:
        s += e
        top = max(top, s)
    cnt += top >= 1
print(f"M1 count = {cnt} of 8 (page 5)")
cnt2 = 0
for steps in product((1, -1), repeat=2):
    s = 0
    top = 0
    for e in steps:
        s += e
        top = max(top, s)
    cnt2 += top >= 2
print(f"M2 count = {cnt2} of 4 -> P = {Fraction(cnt2, 4)} (page 1/4)")
path = [0]
steps = (1, 1, -1, -1, 1)
for e in steps:
    path.append(path[-1] + e)
a = 2
kappa = next(k for k, v in enumerate(path) if v == a)
refl = list(steps[:kappa]) + [-e for e in steps[kappa:]]
rpath = [0]
for e in refl:
    rpath.append(rpath[-1] + e)
print(f"M3 path={path} kappa={kappa} reflected steps={refl} reflected path={rpath}")
print(f"  Lemma 1.2 check S'_k = 2a - S_k for k>=kappa: {[2 * a - path[k] for k in range(kappa, len(path))]} vs {rpath[kappa:]}")

print("\n== L06 Corollary 2.6 closed form at t=1,a=1 and R2/R3 sanity values")
print(f"P(M_1>=1) = erfc(1/sqrt2) = {math.erfc(1 / math.sqrt(2)):.10f}")
