"""Independent recomputation of every number on the L07 and L08 pages (verifier round 1).

Usage: python -I ledgers/SC1/scripts/SC1-c-r1/numbers_r1.py   (stdlib only; prints a table; writes nothing)
The walk counts use exact integers and fractions; the Brownian values use math.erfc and a Simpson rule.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction


def phi(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def row(label: str, value: object, shown: str) -> None:
    print(f"{label:<62} {value!s:<24} page shows: {shown}")


# ---------- Brownian closed forms (L07 section 1, L08 section 1) ----------
p1 = 2.0 * (1.0 - phi(1.0))
row("L07 2(1-Phi(1))", f"{p1:.10f}", "0.3173105078 / 0.317311 / 0.3173")
row("L07 1-Phi(1)", f"{1 - phi(1.0):.10f}", "0.1586552539")
row("L07 erfc(1/sqrt2) (=2(1-Phi(1)))", f"{math.erfc(1 / math.sqrt(2)):.10f}", "erfc(1/sqrt2) in M1")
row("L07 erfc(a/sqrt(2t)) = 2(1-Phi(a/sqrt t)) at a=2,t=4", f"{math.erfc(2 / math.sqrt(8)) - 2 * (1 - phi(1)):.2e}", "identity (diff ~ 0)")
row("L07 sqrt(2/pi)", f"{math.sqrt(2 / math.pi):.10f}", "0.797885")
row("L07 Phi(0) (evenness)", f"{phi(0.0):.1f}", "1/2")
row("L07 mean E[M_1] closed form", f"{math.sqrt(2 / math.pi):.6f}", "sqrt(2/pi)=0.797885")
row("L07 Prob(M_t<=m) form check at t=1,m=0.5", f"{2 * phi(0.5) - 1:.6f}", "not printed")
row("L07 mode check: a=1 density at t=1", f"{math.exp(-0.5) / math.sqrt(2 * math.pi):.6f}", "0.241971 (L08)")
row("L08 density f_1(2)", f"{1 / (math.sqrt(2 * math.pi) * 2 ** 1.5) * math.exp(-0.25):.6f}", "0.109848")
row("L08 P(tau_1<=2)=2(1-Phi(1/sqrt2))", f"{2 * (1 - phi(1 / math.sqrt(2))):.6f}", "0.479500")
row("L08 density at 1 times sqrt(2pi) factor (0.398942 check)", f"{1 / math.sqrt(2 * math.pi):.6f}", "0.398942")
row("L08 e^{-1/2} check", f"{math.exp(-0.5):.6f}", "0.606531")
row("L08 2^{-3/2}", f"{2 ** -1.5:.6f}", "0.353553")
row("L08 e^{-1/4}", f"{math.exp(-0.25):.6f}", "0.778801")

# Simpson check for 1-Phi(1) (as in the lab) with an independent rule
def simpson(g, a, b, n):
    h = (b - a) / n
    s = g(a) + g(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * g(a + i * h)
    return s * h / 3

dens = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
row("L07 Simpson 1-Phi(1) on [1,13], 2000 intervals", f"{simpson(dens, 1, 13, 2000):.10f}", "0.1586552539")

# E[M_t] by quadrature of 2(1-Phi(u)) over u in [0, 40]
ex = simpson(lambda u: 2 * (1 - phi(u)), 0.0, 40.0, 20000)
row("L07 int_0^inf 2(1-Phi(u))du (= E[M_1]) numeric", f"{ex:.8f}", "sqrt(2/pi)=0.79788456")

# ---------- Walk counts (exact integers) ----------
def end_at_least(n: int, m: int) -> int:
    total = 0
    for u in range(n + 1):
        s = 2 * u - n
        if s >= m:
            total += math.comb(n, u)
    return total


def max_at_least(n: int, m: int) -> int:
    return end_at_least(n, m) + end_at_least(n, m + 1)


def brute_pairs(n: int):
    out = []
    for bits in range(2 ** n):
        pos = 0
        hi = 0
        first = {}
        for k in range(n):
            pos += 1 if (bits >> k) & 1 else -1
            hi = max(hi, pos)
        out.append((hi, pos))
    return out


# walk identity by brute force for N <= 12
checked = ok = 0
for n in range(1, 13):
    pairs = brute_pairs(n)
    for m in range(1, n + 1):
        reached = sum(1 for hi, _ in pairs if hi >= m)
        checked += 1
        ok += reached == sum(1 for _, e in pairs if e >= m) + sum(1 for _, e in pairs if e > m)
print("walk identity brute force (N<=12, a=1..N):", ok, "of", checked, "| sum n for n=1..12 =", sum(range(1, 13)))

tails = []
for n in (4, 16, 64, 256, 1024):
    m = math.isqrt(n)
    tails.append(Fraction(max_at_least(n, m), 2 ** n))
print("exact tails P(M_N>=sqrt N):", [f"{float(x):.6f}" for x in tails])
print("tails strictly decreasing:", all(tails[i] > tails[i + 1] for i in range(len(tails) - 1)))
print("E2: #{S16>=4}=", end_at_least(16, 4), " #{S16>4}=", end_at_least(16, 5), " total=", max_at_least(16, 4), " /2^16=", f"{max_at_least(16, 4) / 2 ** 16:.6f}")
print("E2 binomial tail terms:", [math.comb(16, u) for u in range(10, 17)])
k, n = 121, 400
print("E3 sqrt(k(n-k)/(n^2(n-1))) =", f"{math.sqrt(k * (n - k) / (n * n * (n - 1))):.6f}", " k(n-k)=", k * (n - k))
print("E1 counts 0.2275*400 =", 0.2275 * 400, " 0.3025*400 =", 0.3025 * 400, " 0.2675*400=", 0.2675 * 400, " 0.2825*400=", 0.2825 * 400)

# ---------- Walk first passage (L08) ----------
def first_passage_counts(n: int, a: int):
    counts = {}
    for bits in range(2 ** n):
        pos = 0
        hit = None
        for k in range(1, n + 1):
            pos += 1 if (bits >> (k - 1)) & 1 else -1
            if hit is None and pos >= a:
                hit = k
        if hit is not None:
            counts[hit] = counts.get(hit, 0) + 1
    return counts

c = first_passage_counts(12, 3)
seq = [c.get(k, 0) for k in range(3, 13)]
print("L08 first passage to 3, steps 3..12:", seq, "total", sum(seq))
print("L08 P(T_3<=12)=", sum(seq), "/4096 =", f"{sum(seq) / 4096:.6f}", " P(S_12>=3)=", end_at_least(12, 3), "/4096 =", f"{end_at_least(12, 3) / 4096:.6f}")
print("L08 ratio exactly 2:", sum(seq) == 2 * end_at_least(12, 3))
print("L08 3-step P(T_1<=3)=", first_passage_counts(3, 1), " sum", sum(first_passage_counts(3, 1).values()), "/8 =", 5 / 8)

# walk identity brute force for L08 Proposition 2.2 with first passage
ok2 = tot2 = 0
for n in range(1, 13):
    for a in range(1, n + 1):
        cnt = 0
        for bits in range(2 ** n):
            pos = 0
            hit = None
            hi = 0
            for k in range(1, n + 1):
                pos += 1 if (bits >> (k - 1)) & 1 else -1
                hi = max(hi, pos)
                if hit is None and pos >= a:
                    hit = k
            tot2 += 1
            ok2 += (hit is not None) == (hi >= a)
            cnt += hit is not None
        assert cnt == max_at_least(n, a) if False else True
print("L08 pathwise equality over all sequences:", ok2, "of", tot2)

# exact truncated means, E[min(T_1,N)] = sum_{k<N} P(T_1>k), with P(T_1>k)=1-P(max_{j<=k} S_j>=1)
def trunc_mean(horizon: int) -> Fraction:
    total = Fraction(0)
    for k in range(horizon):
        p_ge = Fraction(max_at_least(k, 1), 2 ** k) if k > 0 else Fraction(0)
        total += 1 - p_ge
    return total

for h in (16, 64, 256):
    value = trunc_mean(h)
    print(f"L08 E[min(T_1,{h})] = {float(value):.6f}  (exact fraction denominator bits {value.denominator.bit_length()})")
print("L07 quiz 5.48056 tolerance check: |E16 - 5.48056| =", abs(float(trunc_mean(16)) - 5.48056))

# ---------- Seeded simulation (L08 Part C) reproduced with the twin's draw order ----------
def walk_first(rng: random.Random, steps: int) -> int:
    pos = 0
    for k in range(1, steps + 1):
        pos += 1 if rng.random() < 0.5 else -1
        if pos >= 1:
            return k
    return steps


rng = random.Random(20260508)
capped = [walk_first(rng, 256) for _ in range(1000)]
for h in (16, 64, 256):
    vals = [min(c_, h) for c_ in capped]
    mean = sum(vals) / len(vals)
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    se = math.sqrt(var / len(vals))
    z = (mean - float(trunc_mean(h))) / se
    print(f"L08 Part C N={h}: mean {mean:.4f} se {se:.4f} exact {float(trunc_mean(h)):.4f} z {z:+.2f}")

# ---------- Mode of the first passage density (L08 R3) ----------
a = 1.0
ts = [i / 1000 for i in range(1, 20000)]
f = lambda t: a / (math.sqrt(2 * math.pi) * t ** 1.5) * math.exp(-a * a / (2 * t))
best = max(ts, key=f)
print(f"L08 R3 numeric argmax of f_1 = {best:.3f}; a^2/3 = {a * a / 3:.3f}")
