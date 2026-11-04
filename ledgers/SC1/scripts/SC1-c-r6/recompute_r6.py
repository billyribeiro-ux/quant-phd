"""Independent recomputation of every closed-form and exact number printed on SC1 L07 and L08 (round 6).

Uses only the standard library. Written by the round-6 verifier; does not import the lab twins.
Exact arithmetic uses fractions.Fraction or integers; floats are used only where a value is printed.
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import product

out: list[str] = []


def say(line: str) -> None:
    out.append(line)
    print(line)


# ---------- L07 Part A: walk identity and exact tails ----------
def walk_pairs(n: int) -> list[tuple[int, int]]:
    res = []
    for steps in product((1, -1), repeat=n):
        s = 0
        top = 0
        for e in steps:
            s += e
            top = max(top, s)
        res.append((top, s))
    return res


checked = 0
identity = 0
for n in range(1, 13):
    pairs = walk_pairs(n)
    for a in range(1, n + 1):
        checked += 1
        reach = sum(1 for top, _ in pairs if top >= a)
        ge = sum(1 for _, e in pairs if e >= a)
        gt = sum(1 for _, e in pairs if e > a)
        identity += reach == ge + gt
say(f"L07 A: identity pairs {identity} of {checked}; sequences total {sum(2**n for n in range(1, 13))}")


def tail_exact(n: int, m: int) -> Fraction:
    # P(max >= m) for SRW of n steps by reflection: P(S_n >= m) + P(S_n > m), exact via binomial
    def ge(level: int) -> int:
        total = 0
        for u in range(n + 1):
            s = 2 * u - n
            if s >= level:
                total += math.comb(n, u)
        return total

    return Fraction(ge(m) + ge(m + 1), 2**n)


for n in (4, 16, 64, 256, 1024):
    m = math.isqrt(n)
    say(f"L07 A: N={n} m={m} P(M_N>=m)={float(tail_exact(n, m)):.6f}")

# DP cross-check for N = 16 with exact fractions over the walk
def dp_tail(n: int, m: int) -> Fraction:
    dist: dict[tuple[int, int], int] = {(0, 0): 1}  # (position, running max) -> count
    for _ in range(n):
        nd: dict[tuple[int, int], int] = {}
        for (pos, top), c in dist.items():
            for e in (1, -1):
                np_ = pos + e
                nt = max(top, np_)
                nd[(np_, nt)] = nd.get((np_, nt), 0) + c
        dist = nd
    return Fraction(sum(c for (_, top), c in dist.items() if top >= m), 2**n)


say(f"L07 A DP check N=16 m=4: {float(dp_tail(16, 4)):.6f} equal={dp_tail(16, 4) == tail_exact(16, 4)}")
say(f"L07 A DP check N=64 m=8: equal={dp_tail(64, 8) == tail_exact(64, 8)}")

# ---------- closed forms ----------
def Phi(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


say(f"L07 closed 2(1-Phi(1)) = {2 * (1 - Phi(1.0)):.10f}; erfc(1/sqrt2) = {math.erfc(1 / math.sqrt(2)):.10f}")
say(f"L07 1-Phi(1) = {1 - Phi(1.0):.10f}; 2*0.1586552539 = {2 * 0.1586552539:.10f}")
say(f"L07 sqrt(2/pi) = {math.sqrt(2 / math.pi):.10f}")
say(f"L07 M1 2(1-Phi(1)) H=4 a=2 -> {2 * (1 - Phi(2 / math.sqrt(4))):.10f}")
say(f"L07 R1 a=-1 H=1: 2(1-Phi(-1)) = {2 * (1 - Phi(-1.0)):.10f} (>1)")

# ---------- L07 E2 binomial ----------
ge4 = sum(math.comb(16, u) for u in range(16 + 1) if 2 * u - 16 >= 4)
gt4 = sum(math.comb(16, u) for u in range(16 + 1) if 2 * u - 16 > 4)
say(f"L07 E2: #(S16>=4)={ge4} #(S16>4)={gt4} total={ge4 + gt4} ratio={(ge4 + gt4) / 2**16:.6f}")
say(f"L07 E2 terms u>=10: {[math.comb(16, u) for u in range(10, 17)]}")

# ---------- L07 E1 / E3 / Part B counts ----------
for k in (91, 107, 113, 121):
    p = k / 400
    se = math.sqrt(k * (400 - k) / (400**2 * 399))
    say(f"L07 B: k={k} p={p:.4f} se={se:.6f} -> {se:.4f} diff_from_closed={p - 2 * (1 - Phi(1.0)):+.6f}")
say(f"L07 E3 se(121/400) = {math.sqrt(33759 / 63840000):.6f}")

# ---------- L07 Part D Simpson ----------
def dens(x: float) -> float:
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def simpson(f, a: float, b: float, n: int) -> float:  # type: ignore[no-untyped-def]
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


say(f"L07 D simpson = {simpson(dens, 1.0, 13.0, 2000):.12f}; erfc-based 1-Phi(1) = {0.5 * math.erfc(1 / math.sqrt(2)):.12f}")

# ---------- L07 Cor 1.5(b) E[M_1] numerically ----------
# integral of 1 - Phi(u) over [0, 40] by Simpson
i_tail = simpson(lambda u: 1 - Phi(u), 0.0, 40.0, 20000)
say(f"L07 Cor1.5b: int_0^40 (1-Phi) = {i_tail:.10f} vs 1/sqrt(2pi) = {1 / math.sqrt(2 * math.pi):.10f}")
say(f"L07 Cor1.5b: E[M_1] = 2*int = {2 * i_tail:.10f}; sqrt(2/pi)={math.sqrt(2 / math.pi):.10f}")

# ---------- L08 Part A first passage ----------
n, a = 12, 3
first_counts = {k: 0 for k in range(1, n + 1)}
pairs_ok = 0
pairs_tot = 0
for steps in product((1, -1), repeat=n):
    s = 0
    nu = None
    for k, e in enumerate(steps, start=1):
        s += e
        if nu is None and s >= a:
            nu = k
    if nu is not None:
        first_counts[nu] += 1
print_counts = [first_counts[k] for k in range(3, 13)]
say(f"L08 A: counts nu_3 = k for k=3..12: {print_counts} sum={sum(first_counts.values())}")
say(f"L08 A: P(nu_3<=12)={sum(first_counts.values())}/4096={sum(first_counts.values()) / 4096:.6f}")
ends_ge3 = sum(1 for steps in product((1, -1), repeat=12) if sum(steps) >= 3)
say(f"L08 A: #(S12>=3)={ends_ge3} P={ends_ge3 / 4096:.6f} ratio counts={sum(first_counts.values()) / ends_ge3}")
say(f"L08 A: #(S12=3)={sum(1 for steps in product((1, -1), repeat=12) if sum(steps) == 3)}")
for k in range(1, 13):
    pass
# total pairs
tot_pairs = sum(n_ * 2**n_ for n_ in range(1, 13))
say(f"L08 A: sum 2^n n=1..12 = {sum(2**n_ for n_ in range(1, 13))}; sum n2^n = {sum(n_ * 2**n_ for n_ in range(1, 13))}; tot_pairs={tot_pairs}")

# nu_a <= n vs max >= a agreement count over all (sequence, level) pairs
agree = 0
total = 0
for n_ in range(1, 13):
    for steps in product((1, -1), repeat=n_):
        s = 0
        top = 0
        nu_hits = {}
        first = {}
        for k, e in enumerate(steps, start=1):
            s += e
            top = max(top, s)
            for lev in range(1, n_ + 1):
                if lev not in first and s >= lev:
                    first[lev] = k
        for lev in range(1, n_ + 1):
            total += 1
            nu_le_n = lev in first and first[lev] <= n_
            max_ge = top >= lev
            agree += nu_le_n == max_ge
print(f"L08 A: (sequence,level) pairs {total}, agreement {agree}")
out.append(f"L08 A: (sequence,level) pairs {total}, agreement {agree}")

# ---------- L08 Part B exact truncated means via P(nu_1 > k) = P(max_{j<=k} S_j <= 0) ----------
def p_nu1_gt(k: int) -> Fraction:
    # exact DP over positions for paths staying <= 0
    dist = {0: 1}
    for _ in range(k):
        nd: dict[int, int] = {}
        for pos, c in dist.items():
            for e in (1, -1):
                np_ = pos + e
                if np_ <= 0:
                    nd[np_] = nd.get(np_, 0) + c
        dist = nd
    return Fraction(sum(dist.values()), 2**k)


def trunc_mean(N: int) -> Fraction:
    return sum((p_nu1_gt(k) for k in range(N)), Fraction(0))


for N in (16, 64, 256):
    tm = trunc_mean(N)
    say(f"L08 B: E[min(nu_1,{N})] = {float(tm):.9f}")
say(f"L08 B closed check P(nu_1>k)=C(k,floor(k/2))/2^k at k=10: {p_nu1_gt(10) == Fraction(math.comb(10, 5), 2**10)}")

# ---------- L08 Part D ----------
def f_a(a_: float, h: float) -> float:
    return a_ / (math.sqrt(2 * math.pi) * h**1.5) * math.exp(-a_ * a_ / (2 * h))


for H in (1.0, 2.0):
    say(f"L08 D: a=1 H={H:g} P(tau<=H)=2(1-Phi(1/sqrt H))={2 * (1 - Phi(1 / math.sqrt(H))):.10f} density={f_a(1.0, H):.10f}")
say(f"L08 D: 2^(-3/2)={2 ** -1.5:.6f} e^(-1/4)={math.exp(-0.25):.6f}")

# central difference check of density at H=1, 2
for H in (1.0, 2.0):
    h = 1e-5
    F = lambda t: 2 * (1 - Phi(1 / math.sqrt(t)))  # noqa: E731
    cd = (F(H + h) - F(H - h)) / (2 * h)
    say(f"L08 D: H={H:g} central diff {cd:.10f} vs density {f_a(1.0, H):.10f} diff {abs(cd - f_a(1.0, H)):.2e}")

# Remark 1.6 asymptotic claim check: f_a(H) * H^{3/2} * sqrt(2pi)/a -> 1
say(f"L08 R1.6: f_1(1e6)*(1e6)^1.5*sqrt(2pi) = {f_a(1.0, 1e6) * (1e6) ** 1.5 * math.sqrt(2 * math.pi):.8f}")

# R3 mode a^2/3
best = max((f_a(1.0, H / 10000), H / 10000) for H in range(1, 30000))
say(f"L08 R3: argmax of f_1 on grid = {best[1]:.4f} (a^2/3 = {1 / 3:.4f})")

# Quiz L08 Q5 truncated mean to 5 decimals
say(f"L08 quiz Q5 E[min(nu_1,16)] = {float(trunc_mean(16)):.10f}")
say(f"L08 quiz Q6 density = {f_a(1.0, 1.0):.10f}")
say(f"L08 quiz Q2 P(tau_1<=1) = {2 * (1 - Phi(1.0)):.10f}")
say(f"L08 A M3: P(nu_1<=3) = {sum(1 for st in product((1,-1), repeat=3) if max(__import__('itertools').accumulate(st)) >= 1) / 8}")

# Interpretation: 1.05, 0.69, 0.77 z values from printed sample means and exact values
for mean, se, exact in ((5.2850, 0.1868, 5.480560), (11.3840, 0.6288, 11.815731), (23.1240, 1.8497, 24.557203)):
    say(f"L08 C z from printed: {(mean - exact) / se:+.4f}")

# L07 Part B z vs closed: printed gaps
say(f"L07 B printed gaps: {[round(p - 0.3173105079, 4) for p in (0.2275, 0.2675, 0.2825, 0.3025)]}")
say(f"L07 C gaps: {[round(m - math.sqrt(2 / math.pi), 4) for m in (0.5546, 0.6639, 0.7232, 0.7586)]}")
say(f"L07 C finest gap / se: {(math.sqrt(2 / math.pi) - 0.7586) / 0.0317:.3f}")
say(f"L07 M1: 2(1-Phi(1)) to 7 places = {2 * (1 - Phi(1.0)):.7f}; 1-Phi(1) to 7 = {1 - Phi(1.0):.7f}")
say(f"L07 misc: 0.317547 - 0.3173105079 = {0.317547 - 0.3173105079:+.7f}")

with open(__file__.rsplit("/", 1)[0] + "/out/recompute_r6.out", "w") as fh:
    fh.write("\n".join(out) + "\n")
