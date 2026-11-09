"""Round-4 independent recomputation of every printed or quoted number in M5 L08-L10 (slice c)."""

import math
import random
from fractions import Fraction

out = []


def p(*a):
    out.append(" ".join(str(x) for x in a))


# ---------- L08 ----------
ALPHA = 0.5
GRID8 = (0.25, 0.5, 0.75, 1.0)
p("L08 Example 1.2 sqrt(0.75) =", f"{math.sqrt(0.75):.6f}")
p("L08 M1 (BV)(0.25)=0.5 ->", math.sqrt(0.5 - 0.25))
p("L08 E2 sqrt(0.457107)=", f"{math.sqrt(0.457107):.6f}", "sqrt(0.707107-0.25)=", f"{math.sqrt(0.707107 - 0.25):.6f}")
p("L08 E2 0.676097 + 0.9*5 =", 0.676097 + 4.5)


def solve8(beta, tol=1e-12):
    grid = GRID8
    vals = [0.0] * 4
    count = 0
    while True:
        new = []
        for k in grid:
            o = k**ALPHA
            feas = [j for j, kp in enumerate(grid) if kp <= o]
            new.append(max(math.sqrt(o - grid[j]) + beta * vals[j] for j in feas))
        count += 1
        gap = max(abs(a - b) for a, b in zip(new, vals))
        vals = new
        if gap <= tol:
            return vals, count


for beta in (0.5, 0.9, 0.95):
    v, c = solve8(beta)
    p("L08 solver count beta", beta, "=", c, "V*", [f"{x:.6f}" for x in v])

# a priori count (E1): d = ||V1-V0||
d = math.sqrt(3) / 2
for beta in (0.5, 0.9, 0.95):
    thr = math.log(1e-12 * (1 - beta) / d) / math.log(beta)
    n = 0
    while beta**n * d / (1 - beta) > 1e-12:
        n += 1
    p("L08 E1 threshold beta", beta, f"{thr:.2f}", "least n", n)

# one-state checks
p("L08 Ex2.3 V*=", (0.5) / (1 - 0.9), " M2 V*=", 0.5 / 0.05)

# unrounded worst contraction ratio over the lab's seeded pairs (float excess, L08 Part B claim)
rng = random.Random(20261028)
worst = 0.0
for _ in range(2000):
    v = [rng.uniform(-10.0, 10.0) for _ in GRID8]
    w = [rng.uniform(-10.0, 10.0) for _ in GRID8]

    def bell(x):
        res = []
        for k in GRID8:
            o = k**ALPHA
            feas = [j for j, kp in enumerate(GRID8) if kp <= o]
            res.append(max(math.sqrt(o - GRID8[j]) + 0.9 * x[j] for j in feas))
        return res

    bv, bw = bell(v), bell(w)
    num = max(abs(a - b) for a, b in zip(bv, bw))
    den = max(abs(a - b) for a, b in zip(v, w))
    worst = max(worst, num / den)
p("L08 Part B unrounded worst ratio", repr(worst), "excess over beta", worst - 0.9)

# ---------- L09 ----------
BETA = 0.9
GRID = GRID8


def feasible(k):
    o = k**ALPHA
    return [j for j, kp in enumerate(GRID) if kp <= o]


def bellman(vals):
    return [max(math.sqrt(k**ALPHA - GRID[j]) + BETA * vals[j] for j in feasible(k)) for k in GRID]


def supd(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def cert(prev, cur):
    return BETA / (1 - BETA) * supd(prev, cur)


# sequence
seq = [[0.0] * 4]
for _ in range(400):
    seq.append(bellman(seq[-1]))
# reference: first n>=1 with cert_n <= 1e-12 ; cert_n uses V_n, V_{n-1}
ref_n = next(n for n in range(1, 400) if cert(seq[n - 1], seq[n]) <= 1e-12)
p("L09 reference n", ref_n, "cert", f"{cert(seq[ref_n - 1], seq[ref_n]):.4e}")
vref = seq[ref_n]
p("L09 ref values", [f"{x:.10f}" for x in vref])
for tol in (1e-2, 1e-4, 1e-6):
    n = next(n for n in range(1, 400) if cert(seq[n - 1], seq[n]) <= tol)
    c = cert(seq[n - 1], seq[n])
    err = supd(seq[n], vref)
    p("L09 stop tol", tol, "n", n, "cert", f"{c:.10f}", "actual", f"{err:.10f}", "diff", f"{err - c:.3e}",
      "bound", err <= c + 1e-12)
c10 = cert(seq[9], seq[10])
p("L09 fixed count 10 cert", f"{c10:.10f}", "actual", f"{supd(seq[10], vref):.10f}")
# naive
n = next(n for n in range(1, 400) if supd(seq[n - 1], seq[n]) <= 1e-6)
step = supd(seq[n - 1], seq[n])
err = supd(seq[n], vref)
p("L09 naive n", n, "step", f"{step:.10e}", "actual", f"{err:.10e}", "9*step", f"{9 * step:.10e}",
  "actual-9*step", f"{err - 9 * step:.3e}", "ratio", err / step)
p("L09 E2 printed ratio 0.0000085808/0.0000009534 =", 0.0000085808 / 0.0000009534)
# spread on last step at each stop
for tol in (1e-2, 1e-4, 1e-6):
    n = next(n for n in range(1, 400) if cert(seq[n - 1], seq[n]) <= tol)
    steps = [a - b for a, b in zip(seq[n], seq[n - 1])]
    p("L09 step spread tol", tol, max(steps) - min(steps))

# a priori count (R2): bound beta^n/(1-beta) * ||V1-V0||
d1 = supd(seq[0], seq[1])
p("L09 R2 ||V1-V0||", d1, "sqrt3/2", math.sqrt(3) / 2)
for n in (150, 151, 152):
    b = BETA**n / (1 - BETA) * d1
    p("L09 R2 bound n", n, f"{b:.6e}")
n_apr = next(n for n in range(0, 1000) if BETA**n / (1 - BETA) * d1 <= 1e-6)
p("L09 R2 least a priori n", n_apr)
p("L09 quiz 0.9^10/0.1 =", 0.9**10 / 0.1)
p("L09 M3 step at 1e-3:", 1e-3 * (1 - 0.9) / 0.9, "1/9000 =", 1 / 9000)

# ---------- L10 ----------
def rs(points, tags, integ, f):
    return sum((f(t) * (integ(points[i]) - integ(points[i - 1])) for i, t in enumerate(tags, start=1)), Fraction(0))


def uni(n):
    return [Fraction(i, n) for i in range(n + 1)]


fx = lambda x: x  # noqa: E731
gsq = lambda x: x * x  # noqa: E731
gid = lambda x: x  # noqa: E731
target = Fraction(2, 3)
for n in (4, 10, 100, 1000):
    pts = uni(n)
    right = rs(pts, pts[1:], gsq, fx)
    left = rs(pts, pts[:-1], gsq, fx)
    ok_r = right == Fraction((n + 1) * (4 * n - 1), 6 * n * n)
    ok_l = left == Fraction(4 * n * n - 3 * n - 1, 6 * n * n)
    p("L10 A n", n, f"right {float(right):.12f} left {float(left):.12f}", "errs",
      f"{float(right - target):.12f} {float(left - target):.12f}", ok_r, ok_l,
      "right_err==(3n-1)/(6n^2)", right - target == Fraction(3 * n - 1, 6 * n * n),
      "left_err==-(3n+1)/(6n^2)", left - target == -Fraction(3 * n + 1, 6 * n * n))
# symbolic check of Example 3.3 for n in 1..60
bad = []
for n in range(1, 61):
    pts = uni(n)
    right = rs(pts, pts[1:], gsq, fx)
    left = rs(pts, pts[:-1], gsq, fx)
    if right != Fraction((n + 1) * (4 * n - 1), 6 * n * n) or left != Fraction(4 * n * n - 3 * n - 1, 6 * n * n):
        bad.append(n)
    if abs(right - target) > Fraction(1, n) or abs(left - target) > Fraction(1, n):
        bad.append(("bound1/n", n))
p("L10 Example 3.3 closed forms and 1/n bound fail list n=1..60:", bad)
p("L10 E1 errors 29/600, -31/600, gap 1/300:",
  float(Fraction(29, 600)), float(-Fraction(31, 600)), Fraction(31, 600) - Fraction(29, 600) == Fraction(1, 300))
p("L10 n=1000 identity sums:", float(rs(uni(1000), uni(1000)[1:], gid, fx)),
  float(rs(uni(1000), uni(1000)[:-1], gid, fx)))
p("L10 right n=1000 closed form (1001)(3999)/(6e6):", float(Fraction(1001 * 3999, 6 * 10**6)))

# Part C: step integrator sums at n=10,100 (exact)
def step_g(x):
    return 1 if x >= Fraction(1, 2) else 0


def step_f(x):
    return 1 if x >= Fraction(1, 2) else 0


for n in (10, 100):
    pts = uni(n)
    lt = rs(pts, pts[:-1], step_g, step_f)
    rt = rs(pts, pts[1:], step_g, step_f)
    p("L10 C n", n, "left", lt, "right", rt)

# Prop 4.2 and P2 and R2 random checks
rng = random.Random(7)
worst42 = 0.0
worstP2 = 0.0
for _ in range(3000):
    m = rng.randint(1, 12)
    interior = sorted(Fraction(rng.randint(1, 10**6 - 1), 10**6) for _ in range(m))
    bounds = [Fraction(0), *interior, Fraction(1)]
    if len(set(bounds)) != len(bounds):
        continue
    tags = [lo + Fraction(rng.randint(0, 10**6), 10**6) * (hi - lo) for lo, hi in zip(bounds, bounds[1:])]
    mesh = max(hi - lo for lo, hi in zip(bounds, bounds[1:]))
    # Prop 4.2: f=x, G=step at 1/2
    s42 = sum((t * ((1 if hi >= Fraction(1, 2) else 0) - (1 if lo >= Fraction(1, 2) else 0)))
              for t, lo, hi in zip(tags, bounds, bounds[1:]))
    worst42 = max(worst42, float(abs(s42 - Fraction(1, 2)) / mesh))
    # P2: f=x, G=x^2, |S-2/3| <= mesh
    s2 = sum((t * (hi * hi - lo * lo)) for t, lo, hi in zip(tags, bounds, bounds[1:]))
    worstP2 = max(worstP2, float(abs(s2 - Fraction(2, 3)) / mesh))
p("L10 Prop4.2 worst |S-1/2|/mesh (must be <=1):", round(worst42, 6))
p("L10 P2 worst |S-2/3|/mesh (must be <=1):", round(worstP2, 6))

# R2 check: continuous f, step at c, S -> f(c); numeric sample
def fc(x):
    return math.cos(3 * x) + x * x


for c in (0.3, 0.77):
    for mesh_n in (100, 1000):
        pts = [i / mesh_n for i in range(mesh_n + 1)]
        # tagged partition: tag at right endpoint of the interval containing c
        k = next(i for i in range(1, mesh_n + 1) if pts[i - 1] < c <= pts[i])
        p("L10 R2 c", c, "n", mesh_n, "S", round(fc(pts[k]), 9), "f(c)", round(fc(c), 9))

print("\n".join(out))
