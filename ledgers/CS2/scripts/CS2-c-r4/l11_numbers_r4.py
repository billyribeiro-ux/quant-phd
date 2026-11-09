"""Independent recomputation for CS2 L11 (Definition 2.1 sketch re-implemented from its wording, not from the twin).

Checks: lab 1 output (stored, compactions, excess, deficit), capacities, per-level compaction counts for the lab
(E2), Theorem 2.2(a),(b) after every add, Theorem 2.4 sign and E <= eps*n, Theorem 2.5 on many streams, the
closed forms 198430 and 18213, the exact sum 18187 (R3, Cor 2.6 sum), E1 (39 values), M3 (40 values), M2 query,
the 1..1000 and 0/1000 examples, the odd-position variant (R2), and the weighted-count identity sign.

Run: python3 -I -W error ledgers/CS2/scripts/CS2-c-r4/l11_numbers_r4.py
"""
import bisect
import math
import random
from fractions import Fraction


def cap(h: int, eps: Fraction) -> int:
    # k_h = 2 * ceil((h+1)(h+2) / (2 eps)), exact rational arithmetic
    return 2 * math.ceil(Fraction((h + 1) * (h + 2)) / (2 * eps))


class Sketch:
    def __init__(self, eps: Fraction, keep_odd: bool = False):
        self.eps = eps
        self.keep_odd = keep_odd
        self.buf: list[list[float]] = []   # buf[h]: items of weight 2**h
        self.n = 0
        self.comp = [0] * 64               # C_h
        self.pushed = [0] * 64             # P_h in weight units

    def _ensure(self, h):
        while len(self.buf) <= h:
            self.buf.append([])

    def _push(self, h: int, x: float):
        self._ensure(h)
        self.buf[h].append(x)
        self.pushed[h] += 2 ** h
        if len(self.buf[h]) == cap(h, self.eps):
            items = sorted(self.buf[h])
            self.buf[h] = []
            self.comp[h] += 1
            # keep 2nd, 4th, ... (1-based) => indices 1,3,5,... ; odd variant keeps 1st,3rd,...
            kept = items[0::2] if self.keep_odd else items[1::2]
            assert len(kept) == cap(h, self.eps) // 2
            for y in kept:
                self._push(h + 1, y)

    def add(self, x: float):
        self.n += 1
        self._push(0, x)

    def weight(self) -> int:
        return sum(len(b) * 2 ** h for h, b in enumerate(self.buf))

    def items(self):
        return [(v, 2 ** h) for h, b in enumerate(self.buf) for v in b]

    def stored(self) -> int:
        return sum(len(b) for b in self.buf)

    def E(self) -> int:
        return sum(c * 2 ** h for h, c in enumerate(self.comp))

    def query(self, q: Fraction) -> float:
        acc = 0
        target = q * self.n
        for v, w in sorted(self.items()):
            acc += w
            if acc >= target:
                return v
        raise AssertionError


def ranks(xs_sorted, v):
    return bisect.bisect_right(xs_sorted, v), bisect.bisect_left(xs_sorted, v)  # R(v), R^-(v)


# ---- Lab 1 recomputation
N = 5000
rng = random.Random(2026)
xs = [rng.random() for _ in range(N)]
srt = sorted(xs)
probes = [Fraction(0), Fraction(1, 100), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2),
          Fraction(3, 4), Fraction(9, 10), Fraction(99, 100), Fraction(1)]
for eps in (Fraction(1, 20), Fraction(1, 10)):
    sk = Sketch(eps)
    for x in xs:
        sk.add(x)
    exc = Fraction(0)
    dfc = Fraction(0)
    ok = True
    for q in probes:
        v = sk.query(q)
        R, Rm = ranks(srt, v)
        if not (Rm <= q * N + eps * N and R >= q * N - eps * N):
            ok = False
        exc = max(exc, Fraction(Rm) - q * N)
        dfc = max(dfc, q * N - Fraction(R))
    print(f"LAB eps={eps} caps={[cap(h, eps) for h in range(3)]} stored={sk.stored()} comp={sum(sk.comp)} "
          f"E={sk.E()} weight={sk.weight()} pass={ok} excess/N={float(exc / N):.6f} deficit/N={float(dfc / N):.6f}")
    print("   per-level compactions", [c for c in sk.comp if c], "per-level stored", [len(b) for b in sk.buf])

# E2: per-level compaction counts for eps=1/20 vs Theorem 2.2(b) floors
sk = Sketch(Fraction(1, 20))
for x in xs:
    sk.add(x)
floors = [5000 // (cap(h, Fraction(1, 20)) * 2 ** h) for h in range(6)]
print("E2 eps=1/20 caps k0..k4", [cap(h, Fraction(1, 20)) for h in range(5)], "bounds floors", floors,
      "actual", sk.comp[:6])

# Theorem 2.2(a),(b) and 2.4/2.5 stress on random streams, many n and eps
viol = 0
checked = 0
for seed in range(120):
    r = random.Random(7000 + seed)
    n = r.randint(1, 1500)
    eps = Fraction(r.choice([1, 2, 3, 5, 7, 10, 20]), 40) if r.random() < 0.5 else Fraction(1, r.randint(2, 30))
    if not (0 < eps < 1):
        continue
    s = Sketch(eps)
    data = []
    for i in range(n):
        x = r.random() if r.random() < 0.7 else float(r.randint(0, 5))  # ties too
        data.append(x)
        s.add(x)
        if s.weight() != s.n:
            viol += 1
    srt2 = sorted(data)
    for h in range(len(s.comp)):
        if s.comp[h] * cap(h, eps) * 2 ** h > n:
            viol += 1
    E = s.E()
    if E > eps * n:
        viol += 1
    # Theorem 2.4 for all candidate probe values
    for v in set(data[:50]) | {-1.0, 0.5, 2.0}:
        R = sum(1 for x in data if x <= v)
        Rm = sum(1 for x in data if x < v)
        Rh = sum(w for val, w in s.items() if val <= v)
        Rhm = sum(w for val, w in s.items() if val < v)
        if not (-E <= Rh - R <= 0 and -E <= Rhm - Rm <= 0):
            viol += 1
    for qn in range(0, 21):
        q = Fraction(qn, 20)
        v = s.query(q)
        R = sum(1 for x in data if x <= v)
        Rm = sum(1 for x in data if x < v)
        if not (R >= q * n and Rm <= q * n + eps * n):
            viol += 1
    checked += 1
print("STRESS streams", checked, "violations", viol)

# Odd-position variant (R2): 0 <= Rhat - R <= E and guarantee holds
viol2 = 0
for seed in range(60):
    r = random.Random(9100 + seed)
    n = r.randint(1, 1200)
    eps = Fraction(1, r.randint(2, 25))
    s = Sketch(eps, keep_odd=True)
    data = [r.random() for _ in range(n)]
    for x in data:
        s.add(x)
    E = s.E()
    for v in data[:40]:
        R = sum(1 for x in data if x <= v)
        Rm = sum(1 for x in data if x < v)
        Rh = sum(w for val, w in s.items() if val <= v)
        Rhm = sum(w for val, w in s.items() if val < v)
        if not (0 <= Rh - R <= E and 0 <= Rhm - Rm <= E):
            viol2 += 1
    for qn in range(0, 21):
        q = Fraction(qn, 20)
        v = s.query(q)
        R = sum(1 for x in data if x <= v)
        Rm = sum(1 for x in data if x < v)
        if not (R >= q * n - eps * n and Rm <= q * n + eps * n):
            viol2 += 1
print("R2 odd-variant violations", viol2)

# Closed forms and sums
def closed(L, eps):
    return Fraction((L + 1) * (L + 2) * (L + 3), 3) / eps + (L + 1)

print("closed n=1e9 eps=1/20 L=29:", closed(29, Fraction(1, 20)), "floor(log2 1e9)=", int(math.log2(10**9)))
print("L for n=1e9 exact:", (10**9).bit_length() - 1)
print("closed n=5000 eps=1/20 L=12:", closed(12, Fraction(1, 20)), "L exact", (5000).bit_length() - 1)
print("Cor 2.6 exact sum eps=1/20 n=5000 L=12:", sum(cap(h, Fraction(1, 20)) - 1 for h in range(13)))
print("sum_{m=1}^{13} m(m+1) =", sum(m * (m + 1) for m in range(1, 14)))

# E1: 39 values eps=1/10
s = Sketch(Fraction(1, 10))
for i in range(39):
    s.add(float(i))
print("E1 39 values: stored", s.stored(), "weight", s.weight(), "E", s.E(), "comp", sum(s.comp), "eps*n", 39 / 10)
# M3: 40 values
s = Sketch(Fraction(1, 10))
for i in range(40):
    s.add(float(i))
print("M3 40 values: per-level stored", [len(b) for b in s.buf], "weight", s.weight())
# M1 capacities eps=1/10
print("M1 caps eps=1/10 k0..k2", [cap(h, Fraction(1, 10)) for h in range(3)])
# M2 query
pairs = [(1, 1), (2, 2), (5, 4)]
tot = sum(w for _, w in pairs)
acc = 0
for v, w in sorted(pairs):
    acc += w
    if acc >= Fraction(1, 2) * tot:
        print("M2 query returns", v, "total", tot, "running", acc)
        break
# 1..1000 examples (eps=0 extension and eps=1/20)
vals = list(range(1, 1001))
def ok(v, q, eps):
    R = sum(1 for x in vals if x <= v)
    Rm = sum(1 for x in vals if x < v)
    return Rm <= q * 1000 + eps * 1000 and R >= q * 1000 - eps * 1000
q = Fraction(1, 2)
e = Fraction(1, 20)
print("1..1000 eps=1/20: 450", ok(450, q, e), "500", ok(500, q, e), "501 with eps 0", ok(501, q, 0), "500 eps0", ok(500, q, 0))
print("   R^-(450), R(450):", sum(1 for x in vals if x < 450), sum(1 for x in vals if x <= 450))
print("   R^-(500), R(500):", sum(1 for x in vals if x < 500), sum(1 for x in vals if x <= 500))
print("   R^-(501), R(501):", sum(1 for x in vals if x < 501), sum(1 for x in vals if x <= 501))
# 0/1000 misconception
vals2 = [0.0] * 500 + [1000.0] * 500
print("0/1000 v=1000: R^-", sum(1 for x in vals2 if x < 1000.0), "R", sum(1 for x in vals2 if x <= 1000.0),
      "allowed eps=1/20:", sum(1 for x in vals2 if x < 1000.0) <= 0.5 * 1000 + 0.05 * 1000 and sum(1 for x in vals2 if x <= 1000.0) >= 500 - 50)
print("0/1000 v in [0,1000] eps0 all ok:", all(
    sum(1 for x in vals2 if x < v) <= 500 and sum(1 for x in vals2 if x <= v) >= 500
    for v in (0.0, 0.5, 1.0, 999.0, 1000.0)))
# P3/S3: n < k_0 exact
s = Sketch(Fraction(1, 20))
for i in range(39):
    s.add(float(i))
print("n<k0 comp", sum(s.comp), "E", s.E(), "k0", cap(0, Fraction(1, 20)))
# Canon bullet 3: first compaction at n=k_0
print("first compaction at n = k0 =", cap(0, Fraction(1, 20)))
# R1 equal-capacity bound check numerically: number of nonempty levels <= floor(log2 n)+1
