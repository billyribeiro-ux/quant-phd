"""Round-2 re-derivation of L11: capacities, memory bounds, worked examples, lab 1 excess and deficit, Theorem 2.4 and 2.5 checks."""

import bisect
import itertools
import math
import random
from fractions import Fraction


def cap(h, eps):
    return 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / eps)


class Sketch:
    def __init__(self, eps, keep_odd=False):
        self.eps = eps
        self.keep_odd = keep_odd
        self.levels = []
        self.n = 0
        self.compactions = [0] * 64  # C_h per level
        self.pushed_items = [0] * 64

    def add(self, x):
        self.n += 1
        self._push(0, x)

    def _push(self, h, x):
        while len(self.levels) <= h:
            self.levels.append([])
        buf = self.levels[h]
        buf.append(x)
        self.pushed_items[h] += 1
        if len(buf) == cap(h, self.eps):
            buf.sort()
            kept = buf[0::2] if self.keep_odd else buf[1::2]
            self.levels[h] = []
            self.compactions[h] += 1
            for y in kept:
                self._push(h + 1, y)

    def stored(self):
        return sum(len(b) for b in self.levels)

    def total_weight(self):
        return sum(len(b) * 2**h for h, b in enumerate(self.levels))

    def E(self):
        return sum(c * 2**h for h, c in enumerate(self.compactions))

    def weighted(self):
        return [(v, 2**h) for h, b in enumerate(self.levels) for v in b]

    def quantile(self, q):
        pairs = sorted(self.weighted())
        target = q * self.n
        cum = 0
        for v, w in pairs:
            cum += w
            if cum >= target:
                return v
        raise AssertionError


# A. Prose numbers
print("A. capacities eps=1/10:", [cap(h, Fraction(1, 10)) for h in range(3)], " eps=1/20:", [cap(h, Fraction(1, 20)) for h in range(3)])
for (eps, label) in [(Fraction(1, 10), "1/10"), (Fraction(1, 20), "1/20")]:
    print("   caps h=0..4 eps", label, [cap(h, eps) for h in range(5)])


def mem_closed(L, eps):
    return Fraction((L + 1) * (L + 2) * (L + 3), 3) / eps + (L + 1)


def mem_exact(L, eps):
    return sum(cap(h, eps) - 1 for h in range(L + 1))


print("A. closed form L=29 eps=1/20:", mem_closed(29, Fraction(1, 20)), "(page 198430)")
print("A. closed form L=12 eps=1/20:", mem_closed(12, Fraction(1, 20)), "(page 18213)")
print("A. exact sum L=12 eps=1/20 (Cor 2.6 sum):", mem_exact(12, Fraction(1, 20)), "(page 18187)")
print("A. sum_{m=1}^{13} m(m+1) =", sum(m * (m + 1) for m in range(1, 14)), " 20*910-13 =", 20 * 910 - 13)
print("A. L for n=5000:", int(math.floor(math.log2(5000))), " L for 10^9:", int(math.floor(math.log2(10**9))))
print("A. 2730/0.15+13 =", 2730 / 0.15 + 13)
print("A. sum_{h=0}^{12} (k_h-1) with eps=1/20, exact:", sum(cap(h, Fraction(1, 20)) - 1 for h in range(13)))
print("A. E2 capacities k0..k4 eps=1/20:", [cap(h, Fraction(1, 20)) for h in range(5)])
print("A. E2 level bounds floor(5000/(k_h 2^h)):", [5000 // (cap(h, Fraction(1, 20)) * 2**h) for h in range(5)], "sum", sum(5000 // (cap(h, Fraction(1, 20)) * 2**h) for h in range(5)))
print("A. ceiling check: closed form upper bound >= exact for L 0..40 eps 1/20:", all(mem_closed(L, Fraction(1, 20)) >= mem_exact(L, Fraction(1, 20)) for L in range(41)))

# B. Lab 1 run (exact same code path as the twin) and its printed numbers
N = 5000
SEED = 2026
PROBES = (Fraction(0), Fraction(1, 100), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(9, 10), Fraction(99, 100), Fraction(1))
rng = random.Random(SEED)
xs = [rng.random() for _ in range(N)]
ordered = sorted(xs)
for eps in (Fraction(1, 20), Fraction(1, 10)):
    sk = Sketch(eps)
    for x in xs:
        sk.add(x)
    worst_exc = Fraction(0)
    worst_def = Fraction(0)
    for q in PROBES:
        v = sk.quantile(q)
        below = bisect.bisect_left(ordered, v)
        atb = bisect.bisect_right(ordered, v)
        assert below <= q * N + eps * N and atb >= q * N - eps * N
        worst_exc = max(worst_exc, Fraction(below) - q * N)
        worst_def = max(worst_def, q * N - Fraction(atb))
    print(f"B. eps {eps}: stored {sk.stored()} compactions {sum(sk.compactions)} total_weight {sk.total_weight()} E {sk.E()} "
          f"excess {float(worst_exc / N):.6f} N deficit {float(worst_def / N):.6f} N  (eps*N={float(eps):.2f})")
    print(f"   C_h {sk.compactions[:6]}  stored by level {[len(b) for b in sk.levels]}")

# C. Section 3 example: values 1..1000, q=1/2, eps=1/20 (counts only; exact)
vals = list(range(1, 1001))
n = 1000
q = Fraction(1, 2)
eps = Fraction(1, 20)
R = lambda v: sum(1 for x in vals if x <= v)
Rm = lambda v: sum(1 for x in vals if x < v)
ok = lambda v: Rm(v) <= q * n + eps * n and R(v) >= q * n - eps * n
print("C. v=500 ok:", ok(500), "R-(500)", Rm(500), "R(500)", R(500))
print("C. v=450 ok:", ok(450), "R-(450)", Rm(450), "R(450)", R(450), "bounds", q*n+eps*n, q*n-eps*n)
print("C. v=501 with eps 0:", Rm(501) <= q * n and R(501) >= q * n, "R-(501)", Rm(501), "R(501)", R(501))
print("C. v=500 with eps 0:", Rm(500) <= q * n and R(500) >= q * n)
print("C. v=450 with eps 0 (should fail):", Rm(450) <= q * n and R(450) >= q * n)
# Misconception 2: 500 zeros and 500 thousands
mvals = [0] * 500 + [1000] * 500
Rm2 = lambda v: sum(1 for x in mvals if x < v)
R2f = lambda v: sum(1 for x in mvals if x <= v)
ok2 = lambda v, e: Rm2(v) <= 500 + e and R2f(v) >= 500 - e
print("C. misc2 v=1000 with eps=1/20:", ok2(1000, 50), Rm2(1000), R2f(1000))
print("C. misc2 all v in [0,1000] satisfy eps=0 version:", all(ok2(v, 0) for v in range(0, 1001)), "outside:", ok2(-1, 0), ok2(1001, 0))

# D. Worked examples
sk = Sketch(Fraction(1, 10))
for i in range(40):
    sk.add(float(i))
    if i + 1 in (20, 39, 40):
        print(f"D. after {i+1} adds: levels sizes {[len(b) for b in sk.levels]} total_weight {sk.total_weight()} stored {sk.stored()} E {sk.E()} C {sk.compactions[:3]}")
sk = Sketch(Fraction(1, 10))
for i in range(39):
    sk.add(float(i))
print(f"D. 39 values eps 1/10: stored {sk.stored()} total_weight {sk.total_weight()} E {sk.E()} C0 {sk.compactions[0]} bound eps*n {float(Fraction(1,10)*39)}")
# M2 quantile from pairs
pairs = [(1, 1), (2, 2), (5, 4)]
tot = sum(w for _, w in pairs)
cum = 0
for v, w in pairs:
    cum += w
    if cum >= Fraction(tot, 2):
        print("D. M2 total", tot, "qn", Fraction(tot, 2), "answer", v, "running", cum)
        break

# E. Theorem 2.4 sign claims and the E bound; Theorem 2.5 guarantee on random streams (both eps, varied n, orders)
def rhat(sk, v, strict):
    if strict:
        return sum(w for x, w in sk.weighted() if x < v)
    return sum(w for x, w in sk.weighted() if x <= v)


rng2 = random.Random(11)
viol = 0
checked = 0
for trial in range(120):
    eps = rng2.choice([Fraction(1, 2), Fraction(1, 3), Fraction(1, 5), Fraction(1, 10), Fraction(1, 20)])
    n = rng2.randint(1, 400)
    order = rng2.choice(["random", "sorted", "dup"])
    if order == "random":
        data = [rng2.random() for _ in range(n)]
    elif order == "sorted":
        data = sorted(rng2.random() for _ in range(n))
    else:
        data = [float(rng2.randint(0, 5)) for _ in range(n)]
    sk = Sketch(eps)
    for x in data:
        sk.add(x)
    assert sk.total_weight() == n
    E = sk.E()
    assert E <= eps * n, (eps, n, E)
    so = sorted(data)
    for v in set(data) | {-1.0, 2.0}:
        Rv = sum(1 for x in data if x <= v)
        Rmv = sum(1 for x in data if x < v)
        d1 = rhat(sk, v, False) - Rv
        d2 = rhat(sk, v, True) - Rmv
        assert -E <= d1 <= 0 and -E <= d2 <= 0, (eps, n, v, d1, d2, E)
        checked += 1
    for q in [Fraction(k, 20) for k in range(21)]:
        v = sk.quantile(q)
        Rv = sum(1 for x in data if x <= v)
        Rmv = sum(1 for x in data if x < v)
        if not (Rv >= q * n - eps * n and Rmv <= q * n + eps * n):
            viol += 1
print("E. Theorem 2.4/2.5/E<=eps n checks on 120 random streams: pointwise checks", checked, "quantile violations", viol)

# F. R2 variant (keep odd positions): sign reversal claims
rng3 = random.Random(5)
bad = 0
for trial in range(60):
    eps = Fraction(1, 5)
    n = rng3.randint(1, 300)
    data = [rng3.random() for _ in range(n)]
    sk = Sketch(eps, keep_odd=True)
    for x in data:
        sk.add(x)
    E = sk.E()
    assert sk.total_weight() == n
    for v in data:
        Rv = sum(1 for x in data if x <= v)
        Rmv = sum(1 for x in data if x < v)
        d1 = rhat(sk, v, False) - Rv
        d2 = rhat(sk, v, True) - Rmv
        if not (0 <= d1 <= E and 0 <= d2 <= E):
            bad += 1
print("F. R2 keep-odd variant: sign-reversed bounds 0 <= Rhat-R <= E on 60 streams, violations:", bad)
print("F. R2 odd-variant change lies in {0,+2^h}: c=3 -> 2*ceil(1.5)-3 =", 2 * math.ceil(3 / 2) - 3, "; c=2 -> ", 2 * math.ceil(2 / 2) - 2)
print("G. P2 check: 2*floor(c/2)-c for c=0..6:", [2 * (c // 2) - c for c in range(7)])
print("G. Lemma 2.3 partial sums H=0..6:", [Fraction(1, 1) - Fraction(1, H + 2) for H in range(7)], "check:", all(sum(Fraction(1, (h + 1) * (h + 2)) for h in range(H + 1)) == 1 - Fraction(1, H + 2) for H in range(50)))
print("G. R3 exact sum formula check:", sum(20 * (h + 1) * (h + 2) - 1 for h in range(13)))
