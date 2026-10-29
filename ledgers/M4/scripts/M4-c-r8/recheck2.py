# Round 8 extra checks: L10 Part B running means (independent replay), L09 Prop 2.2 inequality on the die, L08 Prop 2.1 algebra.
import math, random, cmath
import numpy as np
def draw_normal(rng): return rng.gauss(0.0, 1.0)
def draw_t3(rng):
    z = rng.gauss(0.0, 1.0); w = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(3)); return z / math.sqrt(w / 3.0)
def draw_cauchy(rng):
    u = rng.random(); return math.tan(math.pi * (u - 0.5))
for name, f, seed in (("normal", draw_normal, 2026), ("t3", draw_t3, 2027), ("cauchy", draw_cauchy, 2028)):
    rng = random.Random(seed); tot = 0.0; cnt = 0; out = []
    for tgt in (10, 100, 1000, 10000):
        while cnt < tgt:
            tot += f(rng); cnt += 1
        out.append(f"{tot / tgt:+.4f}")
    print("L10 partB", name, out)
# L09 Prop 2.2 on the fair die: Y=(X-3.5)/sigma
vals = np.arange(1, 7); p = np.full(6, 1/6)
mu = 3.5; s2 = 35/12; sig = math.sqrt(s2)
Y = (vals - mu) / sig
M = np.max(np.abs(Y))
EY3 = np.sum(p * np.abs(Y) ** 3)
worst = 0.0
for s in np.linspace(-1/M, 1/M, 2001):
    phi = np.sum(p * np.exp(1j * s * Y))
    lhs = abs(phi - (1 - s * s / 2)); rhs = abs(s) ** 3 * EY3 / 3
    worst = max(worst, lhs / rhs if rhs > 0 else 0)
print("L09 Prop2.2 die: max lhs/rhs =", round(worst, 4), "(<=1 needed)")
# L10 Prop 1.5(c) pointwise claim e^{sx}1{Z>x} <= e^{sZ} for s>0, sample check
rng = np.random.default_rng(1)
z = rng.standard_normal(100000); x = 0.7; s = 1.3
print("pointwise Markov ok:", bool(np.all(np.exp(s*x)*(z > x) <= np.exp(s*z) + 1e-12)))
