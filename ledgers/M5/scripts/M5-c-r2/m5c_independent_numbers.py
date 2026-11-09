"""Round-2 independent recomputation of the numbers printed or quoted in M5 L08, L09, L10 (not copied from the twins)."""
import math
import random
from fractions import Fraction

GRID = [0.25, 0.5, 0.75, 1.0]
ALPHA = 0.5


def feas(k, grid):
    out = k ** ALPHA
    return [j for j, kp in enumerate(grid) if kp <= out]


def B(V, beta, grid=GRID):
    res = []
    for k in grid:
        out = k ** ALPHA
        res.append(max(math.sqrt(out - grid[j]) + beta * V[j] for j in feas(k, grid)))
    return res


def iterate_gap(beta, tol=1e-12, grid=GRID):
    V = [0.0] * len(grid)
    n = 0
    while True:
        W = B(V, beta, grid)
        n += 1
        gap = max(abs(a - b) for a, b in zip(W, V))
        V = W
        if gap <= tol:
            return V, n


# L08 Part A
V, n = iterate_gap(0.9)
print("L08 A: iterations (gap<=1e-12):", n)
print("L08 A: V*", [round(x, 6) for x in V])
res = max(abs(a - b) for a, b in zip(B(V, 0.9), V))
print("L08 A: residual", f"{res:.3e}")
# L08 E1 / Misconception 2 counts
for beta in (0.5, 0.9, 0.95):
    _, n = iterate_gap(beta)
    print(f"L08 counts beta={beta}: solver iterations {n}")
# a priori thresholds (E1)
d = math.sqrt(3) / 2
tau = 1e-12
for beta in (0.5, 0.9, 0.95):
    thr = math.log(tau * (1 - beta) / d) / math.log(beta)
    nmin = math.ceil(thr)
    chk = beta ** nmin * d / (1 - beta) <= tau and beta ** (nmin - 1) * d / (1 - beta) > tau
    print(f"L08 E1 beta={beta}: threshold {thr:.4f} least n {nmin} check {chk}")
# unrounded largest ratio on seeded pairs (lab draw order: v then w, 4 uniforms each, 2000 pairs)
rng = random.Random(20261028)
worst = 0.0
for _ in range(2000):
    v = [rng.uniform(-10.0, 10.0) for _ in GRID]
    w = [rng.uniform(-10.0, 10.0) for _ in GRID]
    bv, bw = B(v, 0.9), B(w, 0.9)
    num = max(abs(a - b) for a, b in zip(bv, bw))
    den = max(abs(a - b) for a, b in zip(v, w))
    worst = max(worst, num / den)
print(f"L08 B: worst ratio {worst!r} minus beta {worst - 0.9!r}")
# one-point grid: fixed point and iterates at beta=1
V1, n1 = iterate_gap(0.9, grid=[0.25])
print("L08 C: one point fixed point", V1, n1)
# L08 M2 / E2 checks
print("L08 E2: sqrt(0.707107-0.25)+4.5 =", math.sqrt(0.707107 - 0.25) + 0.9 * 5.0)
print("L08 example 1.2 sqrt(.75)=", math.sqrt(0.75))

# L09 numbers
def cert(prev, cur, beta):
    return beta / (1 - beta) * max(abs(a - b) for a, b in zip(cur, prev))


def run(beta=0.9):
    seq = [[0.0] * 4]
    while True:
        seq.append(B(seq[-1], beta))
        yield len(seq) - 1, seq


gen = run()
seq = None
# reference: first n>=1 with cert_n <= 1e-12
prev = [0.0] * 4
cur = B(prev, 0.9)
n = 1
hist = [prev, cur]
while cert(hist[-2], hist[-1], 0.9) > 1e-12:
    hist.append(B(hist[-1], 0.9))
    n += 1
print("L09 reference iterations", n, "reference certified", f"{cert(hist[-2], hist[-1], 0.9):.3e}")
ref = hist[-1]
print("L09 reference values", [f"{x:.10f}" for x in ref])
for tol in (1e-2, 1e-4, 1e-6):
    h = [[0.0] * 4, B([0.0] * 4, 0.9)]
    n = 1
    while cert(h[-2], h[-1], 0.9) > tol:
        h.append(B(h[-1], 0.9))
        n += 1
    c = cert(h[-2], h[-1], 0.9)
    err = max(abs(a - b) for a, b in zip(h[-1], ref))
    print(f"L09 stop tol {tol:g}: n {n} cert {c:.10f} actual_error {err:.10f} bound_holds {err <= c + 1e-12}")
# fixed count 10
h = [[0.0] * 4, B([0.0] * 4, 0.9)]
for _ in range(9):
    h.append(B(h[-1], 0.9))
print("L09 fixed count 10 cert", f"{cert(h[-2], h[-1], 0.9):.10f}", "err", f"{max(abs(a-b) for a,b in zip(h[-1], ref)):.10f}")
# naive stop
h = [[0.0] * 4, B([0.0] * 4, 0.9)]
while max(abs(a - b) for a, b in zip(h[-1], h[-2])) > 1e-6:
    h.append(B(h[-1], 0.9))
step = max(abs(a - b) for a, b in zip(h[-1], h[-2]))
err = max(abs(a - b) for a, b in zip(h[-1], ref))
print(f"L09 naive: n {len(h)-1} step {step:.10f} err {err:.10f} ratio err/step {err/step:.6f} 9*step {9*step:.10f}")
# L09 R2 a priori count: smallest n with beta^n d/(1-beta) <= 1e-6
n = 1
while 0.9 ** n * d / 0.1 > 1e-6:
    n += 1
print("L09 R2 a priori n", n, "bound at 151", f"{0.9**151*d/0.1:.4e}", "at 152", f"{0.9**152*d/0.1:.4e}")
print("L09 R2 V1 max", max(math.sqrt(k ** ALPHA - GRID[0]) for k in GRID), "sqrt3/2", d)
print("L09 E1 quotient 0.0000085808/0.0000009534 =", 0.0000085808 / 0.0000009534)
print("L09 M2 cert 0.8/0.2*0.016 =", 0.8 / 0.2 * 0.016, "M3 1e-3*0.1/0.9 =", 1e-3 * 0.1 / 0.9, "1/9000", 1 / 9000)
print("L09 quiz 0.9**10/0.1 =", 0.9 ** 10 / 0.1)

# L10 numbers (exact, Fractions)
def S_right(n):
    return sum(Fraction(i, n) * (Fraction(i, n) ** 0 * 0 + (Fraction(i, n) ** 2 - Fraction(i - 1, n) ** 2)) for i in range(1, n + 1))


def S_left(n):
    return sum(Fraction(i - 1, n) * (Fraction(i, n) ** 2 - Fraction(i - 1, n) ** 2) for i in range(1, n + 1))


for n in (4, 10, 100, 1000):
    r, l = S_right(n), S_left(n)
    print(f"L10 A n {n}: right-2/3 = {r - Fraction(2,3)} (formula (3n-1)/(6n^2) = {Fraction(3*n-1, 6*n*n)}), "
          f"left-2/3 = {l - Fraction(2,3)} (formula -(3n+1)/(6n^2) = {-Fraction(3*n+1, 6*n*n)})")
print("L10 E1 n=10 gap", float(Fraction(31, 600) - Fraction(29, 600)), 1 / 300)
print("L10 quiz L10q6 (1001)(3999)/(6e6)", 1001 * 3999 / 6e6, "S_right(1000) exact", float(S_right(1000)))
# part B recomputation with the lab's draw order
rng = random.Random(20261028)
worst = 0.0
mx = 0.0
allok = True
for _ in range(200):
    m = rng.randint(1, 30)
    interior = sorted(rng.random() for _ in range(m))
    bounds = [0.0] + interior + [1.0]
    tags = [lo + rng.random() * (hi - lo) for lo, hi in zip(bounds[:-1], bounds[1:])]
    tot = sum(t * (bounds[i] ** 2 - bounds[i - 1] ** 2) for i, t in enumerate(tags, start=1))
    mesh = max(hi - lo for lo, hi in zip(bounds[:-1], bounds[1:]))
    err = abs(tot - 2 / 3)
    allok = allok and err <= 2 * mesh + 1e-12
    worst = max(worst, err / mesh)
    mx = max(mx, mesh)
print(f"L10 B: largest mesh {mx:.6f} worst err/mesh {worst:.6f} all_ok {allok}")
