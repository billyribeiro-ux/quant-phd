"""Re-derivations for the hunks changed since the previous pin (M2 slice c, round 4).

Covers: L14 branch programs (Section 2 paragraph, Section 6 bullet 1, R3, quiz item 7) executed with the
lab twin's own Dual class; L14 Proposition 3.1 operation formulas (sum, product, quotient) checked against
the dual class on random rationals; L17 E2 third derivative and error bounds; L18 Proposition 3.3 bound
|Ah| <= K|h| with K = sum of |A_ij| on random inputs; L18 Proposition 3.2 uniqueness algebra.
Run: .venv/bin/python -I <this file> <checkout root>.
"""
import math
import random
import sys
from fractions import Fraction

ROOT = sys.argv[1]
random.seed(20261109)

# L14 twin: take the Dual class and helpers from the twin source itself (the lesson's own code, unmodified).
ns: dict[str, object] = {"__name__": "lab_m2_l14_twin_module"}
src = open(f"{ROOT}/tests/labs/M2/lab-M2-L14-1.py", encoding="utf-8").read()
exec(compile(src.split("def main()")[0], "lab-M2-L14-1-head", "exec"), ns)
Dual = ns["Dual"]

print("== L14 branch programs (Section 2 convention, Section 6 bullet 1, R3, quiz item 7)")
x = Dual(0.0, 1.0)  # 0 + 1 eps
prog = {
    "x if x.val > 0 else -x": (lambda x: x if x.val > 0 else -x),
    "x if x.val >= 0 else -x": (lambda x: x if x.val >= 0 else -x),
    "x if x.val > 0 else 0": (lambda x: x if x.val > 0 else Dual(0.0, 0.0)),
    "x if x.val >= 0 else 0": (lambda x: x if x.val >= 0 else Dual(0.0, 0.0)),
}
for name, fn in prog.items():
    r = fn(x)
    print(f"  {name}: value={r.val} tangent={r.dot}")
assert prog["x if x.val > 0 else -x"](x).dot == -1.0
assert prog["x if x.val >= 0 else -x"](x).dot == 1.0
assert prog["x if x.val > 0 else 0"](x).dot == 0.0
assert prog["x if x.val >= 0 else 0"](x).dot == 1.0
for _ in range(2000):
    v = random.uniform(-3, 3)
    got = prog["x if x.val > 0 else 0"](Dual(v, 1.0)).val
    assert got == max(v, 0.0), v
print("  R3 'same function' max(x,0) on 2000 random points: OK")

print("== L14 Proposition 3.1 operations (Definition 2.1) against the dual class")
def fr() -> Fraction:
    return Fraction(random.randint(-9, 9), random.randint(1, 9))
for _ in range(500):
    a, b, c, d = fr(), fr(), fr(), fr()
    if c == 0:
        continue
    s = Dual(float(a), float(b)) + Dual(float(c), float(d))
    assert math.isclose(s.val, float(a + c)) and math.isclose(s.dot, float(b + d), abs_tol=1e-12)
    p = Dual(float(a), float(b)) * Dual(float(c), float(d))
    assert math.isclose(p.val, float(a * c)) and math.isclose(p.dot, float(a * d + b * c), abs_tol=1e-9)
    q = Dual(float(a), float(b)) / Dual(float(c), float(d))
    assert math.isclose(q.val, float(a / c), rel_tol=1e-12)
    assert math.isclose(q.dot, float((b * c - a * d) / (c * c)), rel_tol=1e-9, abs_tol=1e-12)
print("  sum, product, quotient match Definition 2.1 on 500 random cases: OK")
g, gp, k, kp = 3.0, 2.0, 5.0, -1.0
q = Dual(g, gp) / Dual(k, kp)
assert math.isclose(q.dot, (gp * k - g * kp) / k**2)
print(f"  quotient tangent (g'k - gk')/k^2 at (g,g',k,k')=(3,2,5,-1): {q.dot} = {(gp*k - g*kp)/k**2}: OK")

print("== L17 E2 (central difference of f = x^2 y + sin y along a unit direction u)")
def f(x1: float, y: float) -> float:
    return x1 * x1 * y + math.sin(y)
def psi3(u1: float, u2: float, y: float) -> float:
    return 6 * u1 * u1 * u2 - u2**3 * math.cos(y)
worst_rel = 0.0
for _ in range(200):
    th = random.uniform(0, 2 * math.pi)
    u1, u2 = math.cos(th), math.sin(th)
    a1, a2 = random.uniform(-2, 2), random.uniform(-2, 2)
    hs = 1e-2
    vals = {j: f(a1 + j * hs * u1, a2 + j * hs * u2) for j in range(-3, 4)}
    d3 = (vals[2] - 2 * vals[1] + 2 * vals[-1] - vals[-2]) / (2 * hs**3)
    worst_rel = max(worst_rel, abs(d3 - psi3(u1, u2, a2)) / max(1.0, abs(d3)))
    assert abs(psi3(u1, u2, a2)) <= 7.0 + 1e-12
print(f"  psi''' = 6 u1^2 u2 - u2^3 cos y vs 7-point difference: max relative error {worst_rel:.2e}; |psi'''| <= 7 on 200 unit u: OK")
t = 1e-6
print(f"  truncation bound (t^2/6)*7 = {(t*t/6)*7:.6e} (lesson: about 1.2e-12)")
delta = 2.0**-53
print(f"  half spacing 2^-53 = {delta:.6e}; rounding delta/t = {delta/t:.6e} (lesson: order 1e-10)")
worst = 0.0
for _ in range(200):
    th = random.uniform(0, 2 * math.pi)
    u1, u2 = math.cos(th), math.sin(th)
    a1, a2 = random.uniform(-2, 2), random.uniform(-2, 2)
    cd = (f(a1 + t * u1, a2 + t * u2) - f(a1 - t * u1, a2 - t * u2)) / (2 * t)
    exact = (2 * a1 * a2) * u1 + (a1 * a1 + math.cos(a2)) * u2  # grad f = (2xy, x^2 + cos y), dotted with u
    worst = max(worst, abs(cd - exact))
print(f"  measured central-difference error over 200 directions at t=1e-6: max {worst:.3e}; below 1e-6: {worst < 1e-6}")

print("== L18 Proposition 3.3 bound and Proposition 3.2 uniqueness algebra")
for _ in range(2000):
    m, n = random.randint(1, 3), random.randint(1, 3)
    A = [[random.uniform(-5, 5) for _ in range(n)] for _ in range(m)]
    h = [random.uniform(-2, 2) for _ in range(n)]
    Ah = [sum(A[i][j] * h[j] for j in range(n)) for i in range(m)]
    K = sum(abs(A[i][j]) for i in range(m) for j in range(n))
    assert math.sqrt(sum(v * v for v in Ah)) <= K * math.sqrt(sum(v * v for v in h)) + 1e-12
print("  |Ah| <= K|h| with K = sum |A_ij| on 2000 random matrices: OK")
A = [[1.0, 2.0], [0.5, -1.0]]
C = [[0.3, 2.0], [0.5, 4.0]]
v = [0.6, 0.8]
t_ = 0.01
D = [0.2, -0.1]  # stands for F(a+tv)-F(a) (any values)
lhs = [t_ * sum((A[i][j] - C[i][j]) * v[j] for j in range(2)) for i in range(2)]
r1 = [D[i] - t_ * sum(A[i][j] * v[j] for j in range(2)) for i in range(2)]
r2 = [D[i] - t_ * sum(C[i][j] * v[j] for j in range(2)) for i in range(2)]
assert all(math.isclose(lhs[i], r2[i] - r1[i], abs_tol=1e-12) for i in range(2))
print("  (A - C)tv = [F(a+tv)-F(a)-Ctv] - [F(a+tv)-F(a)-Atv] identity: OK")
print("ALL CHECKS PASSED")
