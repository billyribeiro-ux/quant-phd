"""Re-run the worked examples of L09-L11 problem sets (CS2 slice c round 1). Standard library only."""
import math
from collections import deque
from fractions import Fraction


def min_deque(xs, w, looser=False):
    dq = deque()
    ops = 0
    trace = []
    for i, x in enumerate(xs):
        rem = 0
        while dq:
            back = dq[-1][1]
            cond = back > x if looser else back >= x
            if not cond:
                break
            dq.pop()
            rem += 1
        dq.append((i, x))
        while dq[0][0] <= i - w:
            dq.popleft()
            rem += 1
        ops += 1 + rem
        trace.append((rem, list(dq)))
    return trace, ops


# L10 M2: series 3,1,4,1,5 w=3
t, _ = min_deque([3, 1, 4, 1, 5], 3)
print("L10 M2 deques:", [d for _, d in t])
print("L10 M2 removals per position:", [r for r, _ in t], "total removals", sum(r for r, _ in t))
# L10 M3 operations: 5 appends + removals = 8?
_, ops = min_deque([3, 1, 4, 1, 5], 3)
print("L10 M3 total ops:", ops, "bound 2n =", 2 * 5)
# L10 E2: 1,2,3,4,5,0 with w=5
t, ops = min_deque([1, 2, 3, 4, 5, 0], 5)
print("L10 E2 removals per position:", [r for r, _ in t])
# L10 R2: 4,1,4 with w=2
t, _ = min_deque([4, 1, 4], 2)
print("L10 R2 deques:", [d for _, d in t])
# L10 R1 looser rule: min front equals window min, values non-decreasing
import random
rng = random.Random(5)
ok = True
for trial in range(300):
    n = rng.randint(1, 25)
    w = rng.randint(1, 8)
    xs = [rng.randint(0, 5) for _ in range(n)]
    t, _ = min_deque(xs, w, looser=True)
    for i, (_, dq) in enumerate(t):
        win = xs[max(0, i - w + 1): i + 1]
        if dq[0][1] != min(win):
            ok = False
        vals = [v for _, v in dq]
        if any(vals[k] > vals[k + 1] for k in range(len(vals) - 1)):
            ok = False
print("L10 R1 looser rule front=min and non-decreasing over 300 random series:", ok)
# L10 E1: w=1, total ops 2n-1
for n in (1, 2, 5, 200):
    xs = [random.Random(n + k).randint(0, 999) for k in range(n)]
    _, ops = min_deque(xs, 1)
    print("L10 E1 w=1 n=", n, "ops", ops, "2n-1", 2 * n - 1)
# L10 E3: strictly decreasing
for w in (1, 3, 10):
    xs = list(range(10, 0, -1))
    _, ops = min_deque(xs, w)
    print("L10 E3 decreasing n=10 w=", w, "ops", ops, "2n-1 =", 19)
# L10 R3 / Cor 2.5(c): increasing series max step-(3) removals = n-w
for n, w in ((10, 3), (12, 4)):
    xs = list(range(n))
    t, _ = min_deque(xs, w)
    print("L10 R3 n=", n, "w=", w, "removals", sum(r for r, _ in t), "n-w", n - w)
# Cor 2.5(c): w increasing then one below -> removes w
for w in (1, 2, 5):
    xs = list(range(w)) + [-1]
    t, _ = min_deque(xs, w)
    print("L10 Cor2.5c w=", w, "last removals", t[-1][0])

# L11 M3 and E1 sketch checks
def cap(h, eps):
    return 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / eps)


class Sk:
    def __init__(self, eps):
        self.eps = eps
        self.levels = []

    def add(self, x):
        self._push(0, x)

    def _push(self, h, x):
        while len(self.levels) <= h:
            self.levels.append([])
        b = self.levels[h]
        b.append(x)
        if len(b) == cap(h, self.eps):
            b.sort()
            kept = b[1::2]
            self.levels[h] = []
            for y in kept:
                self._push(h + 1, y)

    def summary(self):
        return [len(b) for b in self.levels], sum(len(b) * 2 ** h for h, b in enumerate(self.levels))


for n in (40, 39):
    sk = Sk(Fraction(1, 10))
    for k in range(n):
        sk.add(Fraction(k))
    print("L11 n=", n, "items per level", sk.summary()[0], "total weight", sk.summary()[1])
