"""Round-3 independent recomputation for M5 slice c (L08-L10).

Recomputes the numbers the pages state, with the lab code's own functions where the lab defines them.
Run: .venv/bin/python -I ledgers/M5/scripts/M5-c-r3/recheck_L08_L10.py <checkout>
"""
import importlib.util
import math
import random
import sys
from fractions import Fraction

root = sys.argv[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    return mod


# ---- L08 lab: BETA sensitivity (E1, Misconception 2, card M5-c139)
src8 = open(f"{root}/tests/labs/M5/lab-M5-L08-1.py").read()
# strip the final main() call so we can call solve with other betas
src8_nomain = src8.rsplit("main()", 1)[0]
ns8 = {"__name__": "lab8"}
exec(compile(src8_nomain, "lab8", "exec"), ns8)
for b in (0.5, 0.9, 0.95):
    vals, pol, count = ns8["solve"](ns8["GRID"], b)
    print(f"L08 BETA {b}: solve count {count}")

# ---- L08 Part B unrounded worst ratio (interpretation paragraph, card M5-c137)
rng = random.Random(20261028)
GRID = ns8["GRID"]
BETA = 0.9
worst = 0.0
worst_pair = None
for _ in range(2000):
    v = [rng.uniform(-10.0, 10.0) for _ in GRID]
    w = [rng.uniform(-10.0, 10.0) for _ in GRID]
    bv, _ = ns8["bellman"](v, GRID, BETA)
    bw, _ = ns8["bellman"](w, GRID, BETA)
    num = max(abs(a - b2) for a, b2 in zip(bv, bw, strict=True))
    den = max(abs(a - b2) for a, b2 in zip(v, w, strict=True))
    r = num / den
    if r > worst:
        worst = r
        worst_pair = None
print(f"L08 Part B unrounded worst ratio {worst!r}")
print(f"L08 worst - 0.9 = {worst - 0.9!r}; ulp(0.9) = {math.ulp(0.9)!r}; (worst-0.9)/ulp = {(worst - 0.9) / math.ulp(0.9):.3f}")
print(f"L08 worst - 0.9 as decimal digits: {worst - 0.9:.6e}")
print(f"L08 worst > 0.9 : {worst > 0.9}")

# ---- L08 E1 scaling claim: a priori count vs 1/ln(1/beta)
# a priori count from Theorem 2.2(c) with tau = 1e-12 and d = |V1 - V0| computed on GRID
for b in (0.5, 0.9, 0.95):
    v1, _ = ns8["bellman"]([0.0] * len(GRID), GRID, b)
    d = max(abs(x) for x in v1)
    tau = 1e-12
    n = 1
    while b ** n * d / (1 - b) > tau:
        n += 1
    print(f"L08 E1 beta {b}: a priori n {n}, 1/ln(1/beta) {1 / math.log(1 / b):.4f}, ratio n*ln(1/beta)/... {n / (1 / math.log(1 / b)):.4f}, numerator ln(d/(tau(1-b))) {math.log(d / (tau * (1 - b))):.4f}")

# ---- L08 E2: 0.676097 and 5.176097
print(f"L08 E2 sqrt(0.707107-0.25) = {math.sqrt(0.707107 - 0.25):.6f}; 0.9*5 + that = {0.9 * 5 + math.sqrt(0.707107 - 0.25):.6f}")
print(f"L08 E2 exact: sqrt(sqrt(0.5)-0.25)+4.5 = {math.sqrt(math.sqrt(0.5) - 0.25) + 4.5:.9f}")

# ---- L09 numbers
src9 = open(f"{root}/tests/labs/M5/lab-M5-L09-1.py").read()
ns9 = {"__name__": "lab9"}
exec(compile(src9.rsplit("\nmain()", 1)[0], "lab9", "exec"), ns9)
step_ratio = 0.0000085808 / 0.0000009534
print(f"L09 E2 ratio of printed values {step_ratio:.6f}")
# recompute the naive stop exactly
n, v, prev = ns9["iterate_until"](lambda p, c: ns9["sup_distance"](p, c) <= ns9["NAIVE_TOL"])
step = ns9["sup_distance"](prev, v)
print(f"L09 naive n {n} step {step!r} factor*step {9 * step!r} actual_err {ns9['sup_distance'](v, ns9['iterate_until'](lambda p, c: ns9['certified'](p, c) <= 1e-12)[1]):.12e}")
print(f"L09 exact ratio step-based: (actual)/(step) = {ns9['sup_distance'](v, ns9['iterate_until'](lambda p, c: ns9['certified'](p, c) <= 1e-12)[1]) / step:.6f}")
# a priori count from R2
dd = math.sqrt(3) / 2
for nn in (150, 151, 152, 153):
    print(f"L09 R2 a priori bound at n={nn}: {0.9 ** nn / 0.1 * dd:.6e}")
print(f"L09 V1-V0 sup norm (lab): {ns9['sup_distance'](ns9['bellman']([0.0]*4), [0.0]*4)!r}; sqrt(3)/2 = {dd!r}")
print(f"L09 0.9^10/0.1 = {0.9 ** 10 / 0.1!r}")
print(f"L09 M3 1/9000 = {1 / 9000:.6e}; 1e-3*(0.1/0.9) = {1e-3 * 0.1 / 0.9:.6e}")
print(f"L09 M2 cert = 4*0.016 = {4 * 0.016}")

# ---- L10 numbers
print(f"L10 E1: 29/600 = {29 / 600:.12f}; -31/600 = {-31 / 600:.12f}; gap {31 / 600 - 29 / 600:.12f}")
print(f"L10 E1 printed digits gap: {0.051666666667 - 0.048333333333:.12f}")
print(f"L10 quiz n=1000 closed form {Fraction(1001 * 3999, 6 * 10**6)} = {float(Fraction(1001 * 3999, 6 * 10**6)):.10f}")
print(f"L10 M1 (1/2,1) sum: {Fraction(1,2)*Fraction(1,8)+Fraction(7,8)}")
print(f"L10 M2 int_0^2 x d(x^2) = 2*8/3 = {Fraction(2)*Fraction(8,3)}")
print(f"L10 quiz x d(x^3) = 3*(1/4) = {3*Fraction(1,4)}")
print(f"L10 Part D n=1000: (n+1)/(2n)-1/2 = {Fraction(1001,2000)-Fraction(1,2)}")

# P2 check: |S-2/3| <= m for random partitions (f=x, G=x^2), 20000 trials
rng2 = random.Random(7)
worst_p2 = 0.0
for _ in range(20000):
    m = rng2.randint(1, 40)
    interior = sorted(rng2.random() for _ in range(m))
    bounds = [0.0, *interior, 1.0]
    tags = [lo + rng2.random() * (hi - lo) for lo, hi in zip(bounds, bounds[1:])]
    S = sum(t * (bounds[i] ** 2 - bounds[i - 1] ** 2) for i, t in enumerate(tags, start=1))
    mesh = max(hi - lo for lo, hi in zip(bounds, bounds[1:]))
    worst_p2 = max(worst_p2, abs(S - 2 / 3) / mesh)
print(f"L10 P2 check over 20000 random tagged partitions: max |S-2/3|/mesh = {worst_p2:.6f} (bound 1)")
