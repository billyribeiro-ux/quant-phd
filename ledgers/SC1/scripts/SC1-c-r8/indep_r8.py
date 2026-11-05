"""Independent re-derivation of every number printed or quoted in SC1 slice c (L07, L08 and their lab twins), round 8.

Written from the mathematics, not from the twins. Uses exact integers and Fractions where the lesson says exact,
a dynamic programme where the twin uses binomial sums, and a separate Simpson rule and erfc for the closed forms.
Run as: .venv/bin/python -I ledgers/SC1/scripts/SC1-c-r8/indep_r8.py
"""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

OUT: list[str] = []


def emit(line: str) -> None:
    OUT.append(line)
    print(line)


# ---------- 1. walk: exact enumeration for N <= 12 (identity and first passage) ----------
identity_ok = 0
identity_total = 0
pathwise_ok = 0
pathwise_total = 0
for n in range(1, 13):
    seqs = list(itertools.product((1, -1), repeat=n))
    for a in range(1, n + 1):
        # count sequences whose running maximum over S_0..S_n reaches a (brute force)
        reach = 0
        ends_ge = 0
        ends_gt = 0
        hit_by_n = 0
        for steps in seqs:
            s = 0
            top = 0
            first = None
            for k, e in enumerate(steps, start=1):
                s += e
                top = max(top, s)
                if first is None and s >= a:
                    first = k
            reach += top >= a
            ends_ge += s >= a
            ends_gt += s > a
            hit_by_n += first is not None and first <= n
            pathwise_total += 1
            pathwise_ok += (first is not None) == (top >= a)
        identity_total += 1
        identity_ok += reach == ends_ge + ends_gt
        assert hit_by_n == reach
emit(f"R1 walk identity brute force (N<=12, a<=N): {identity_ok} of {identity_total}")
emit(f"R1 pathwise first-passage vs maximum agreement: {pathwise_ok} of {pathwise_total}")
emit(f"R1 total (sequence, level) pairs = sum n*2^n = {sum(n * 2**n for n in range(1, 13))}")
emit(f"R1 total sequences = sum 2^n = {sum(2**n for n in range(1, 13))}")


# ---------- 2. walk: exact tails via DP (no binomials), N in lab list ----------
def not_hit_count(n: int, m: int) -> int:
    """Number of length-n step sequences whose walk stays strictly below m (never reaches m)."""
    # dp[x] = number of sequences of current length with position x and never reached m; x < m
    dp = {0: 1} if m > 0 else {}
    for _ in range(n):
        new: dict[int, int] = {}
        for x, c in dp.items():
            for step in (1, -1):
                y = x + step
                if y < m:
                    new[y] = new.get(y, 0) + c
        dp = new
    return sum(dp.values())


for n in (4, 16, 64, 256, 1024):
    m = math.isqrt(n)
    hit = 2**n - not_hit_count(n, m)
    p = Fraction(hit, 2**n)
    emit(f"R2 DP exact P(M_N >= m), N={n}, m={m}: {float(p):.6f}  (count {hit})")

emit(f"R2 N=16 a=4 count: {2**16 - not_hit_count(16, 4)} (lesson E2 says 21778)")
emit(f"R2 N=16 endpoint>=4 count 14893 check, endpoint>4 6885 check:")
ends16 = {}
for u in range(17):
    ends16[2 * u - 16] = math.comb(16, u)
emit(f"  endpoint>=4: {sum(v for s, v in ends16.items() if s >= 4)}; endpoint>4: {sum(v for s, v in ends16.items() if s > 4)}")

# ---------- 3. Lab L07 Part B and C: same seeded process, independent statistics ----------
SEED7 = 20260507
PATHS = 400
FINE = 256
rng = random.Random(SEED7)
sd = math.sqrt(1.0 / FINE)
grids = (4, 16, 64, 256)
grid_max = {g: [] for g in grids}
for _ in range(PATHS):
    incr = [rng.gauss(0.0, sd) for _ in range(FINE)]
    b = [0.0]
    for x in incr:
        b.append(b[-1] + x)
    for g in grids:
        idx = [k * (FINE // g) for k in range(g + 1)]
        grid_max[g].append(max(b[i] for i in idx))


def mean_se(xs: list[float]) -> tuple[float, float]:
    n = len(xs)
    mu = sum(xs) / n
    var = sum((x - mu) ** 2 for x in xs) / (n - 1)
    return mu, math.sqrt(var / n)


def simpson(f, lo: float, hi: float, k: int) -> float:
    h = (hi - lo) / k
    s = f(lo) + f(hi)
    for i in range(1, k):
        s += (4 if i % 2 else 2) * f(lo + i * h)
    return s * h / 3


phi_pdf = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)  # noqa: E731
closed = erfc_val = math.erfc(1 / math.sqrt(2))
closed_prob_grid = 2 * (1 - 0.5 * (1 + math.erf(1 / math.sqrt(2))))
emit(f"R3 2(1-Phi(1)) via erfc = {erfc_val:.12f}; via erf = {closed_prob_grid:.12f}")
emit(f"R3 1-Phi(1) via Simpson on [1,13], 20000 intervals = {simpson(phi_pdf, 1.0, 13.0, 20000):.12f}")
for g in grids:
    p_hat, se = mean_se([1.0 if m >= 1.0 else 0.0 for m in grid_max[g]])
    emit(f"R3 B N={g}: P(grid max>=1)={p_hat:.4f} se={se:.4f} diff={p_hat - erfc_val:+.4f} count={round(p_hat * PATHS)}")
viol = 0
for c, f_ in ((4, 16), (16, 64), (64, 256)):
    viol += sum(1 for x, y in zip(grid_max[c], grid_max[f_]) if x > y)
emit(f"R3 B pathwise nesting violations: {viol}")
target = math.sqrt(2 / math.pi)
emit(f"R3 sqrt(2/pi) = {target:.9f}")
for g in grids:
    mu, se = mean_se(grid_max[g])
    emit(f"R3 C N={g}: mean={mu:.4f} se={se:.4f} diff={mu - target:+.4f} gap/se={(target - mu) / se:.2f}")

# ---------- 4. L07 Part D and other closed forms ----------
emit(f"R4 sqrt(2/pi)=0.797885 check, |diff|={abs(target - 0.797885):.2e} (quiz tolerance 1e-6)")
emit(f"R4 2(1-Phi(1)) - 0.3173105 = {erfc_val - 0.3173105:+.3e} (quiz tolerance 1e-6)")
emit(f"R4 1-Phi(1) - 0.158655 = {erfc_val / 2 - 0.158655:+.3e} (quiz tolerance 1e-6)")
emit(f"R4 SE E3: sqrt(121*279/(400^2*399)) = {math.sqrt(121 * 279 / (400**2 * 399)):.6f}")
emit(f"R4 E3 exact: 121*279/(400^2*399) = {Fraction(121 * 279, 400**2 * 399)}; 33759/63840000 check {Fraction(33759, 63840000) == Fraction(121 * 279, 400**2 * 399)}")
emit(f"R4 density f_1(1) = e^(-1/2)/sqrt(2 pi) = {math.exp(-0.5) / math.sqrt(2 * math.pi):.7f}")

# ---------- 5. L08: exact truncated means by DP (absorbing at level 1) ----------
def truncated_mean_exact(cap: int, level: int = 1) -> Fraction:
    alive = {0: 1}  # sequences not yet at level, by position (positions < level)
    total = Fraction(0)
    for k in range(cap):
        # P(nu > k) = (#alive at step k) / 2^k
        total += Fraction(sum(alive.values()), 2**k)
        new: dict[int, int] = {}
        for x, c in alive.items():
            for step in (1, -1):
                y = x + step
                if y < level:
                    new[y] = new.get(y, 0) + c
        alive = new
    return total


for cap in (16, 64, 256):
    e = truncated_mean_exact(cap)
    emit(f"R5 exact E[min(nu_1,{cap})] = {float(e):.6f}  fraction_denominator_power2={e.denominator & (e.denominator - 1) == 0}")
e16 = truncated_mean_exact(16)
emit(f"R5 E[min(nu_1,16)] as fraction = {e16}; 179587/32768 = {179587 / 32768:.7f}; equal: {e16 == Fraction(179587, 32768)}")

# ---------- 6. L08 Part A numbers at n=12, a=3 ----------
n12 = 12
first_hist = [0] * (n12 + 1)
ge3_end = 0
for steps in itertools.product((1, -1), repeat=n12):
    s = 0
    first = None
    for k, e in enumerate(steps, start=1):
        s += e
        if first is None and s >= 3:
            first = k
    if first is not None:
        first_hist[first] += 1
    ge3_end += s >= 3
emit(f"R6 first passage to 3 at steps 3..12: {first_hist[3:]}; sum={sum(first_hist)}")
emit(f"R6 P(nu_3<=12)={sum(first_hist)}/4096={sum(first_hist) / 4096:.6f}; P(S_12>=3)={ge3_end}/4096={ge3_end / 4096:.6f}")
emit(f"R6 ratio exact: {Fraction(sum(first_hist), ge3_end)}")

# ---------- 7. L08 Part C: same seeded walk process, independent statistics ----------
rng8 = random.Random(20260508)
SIM_PATHS = 1000
SIM_STEPS = 256
capped = []
for _ in range(SIM_PATHS):
    pos = 0
    first = SIM_STEPS
    for k in range(1, SIM_STEPS + 1):
        pos += 1 if rng8.random() < 0.5 else -1
        if pos >= 1:
            first = k
            break
    capped.append(first)
for n_ in (16, 64, 256):
    xs = [float(min(c, n_)) for c in capped]
    mu, se = mean_se(xs)
    ex = float(truncated_mean_exact(n_))
    emit(f"R7 C N={n_}: mean={mu:.4f} se={se:.4f} exact={ex:.4f} z={(mu - ex) / se:+.3f} gap/se={(ex - mu) / se:.3f}")

# ---------- 8. L08 Part D ----------
def fp_cdf(a: float, h: float) -> float:
    return math.erfc(a / math.sqrt(2 * h))


def fp_den(a: float, h: float) -> float:
    return a / (math.sqrt(2 * math.pi) * h**1.5) * math.exp(-a * a / (2 * h))


for h in (1.0, 2.0):
    d = 1e-5
    num = (fp_cdf(1, h + d) - fp_cdf(1, h - d)) / (2 * d)
    emit(f"R8 H={h:g}: P(tau<=H)={fp_cdf(1, h):.6f}; density={fp_den(1, h):.6f}; central={num:.6f}; |diff|={abs(num - fp_den(1, h)):.2e}")
emit(f"R8 f_1(1) unrounded = {fp_den(1, 1.0):.10f}")
emit(f"R8 cdf(1,1) = erfc(1/sqrt2) = {fp_cdf(1, 1.0):.10f}; 2*(1-Phi(1)) with 1-Phi(1)=0.1586552539 -> {2 * 0.1586552539:.10f}")
emit(f"R8 Remark 1.6 asymptotic: f_a(H)*H^(3/2) at H=1e6, a=1 -> {fp_den(1, 1e6) * (1e6) ** 1.5 * math.sqrt(2 * math.pi):.6f} (should -> a=1)")

# ---------- 9. Corollary 1.3/1.5 consistency and M3 one-step, Lemma cross-checks ----------
emit(f"R9 M3 L07: 1-Phi(1)={0.5 * math.erfc(1 / math.sqrt(2)):.10f}")
emit(f"R9 L07 M1 H=4,a=2 -> 2(1-Phi(1)) = {math.erfc(2 / math.sqrt(8)):.10f} = erfc(1/sqrt2)")

with open("/Users/billyribeiro/.fanout/wt/verifyE8-SC1-c/ledgers/SC1/scripts/SC1-c-r8/out/indep_r8.txt", "w") as fh:
    fh.write("\n".join(OUT) + "\n")
