"""Independent recomputation of CS2 L10 Lab 1 counts with a different deque formulation (verifier round 4)."""
import random
from collections import deque

N = 200
SEED = 1010
rng = random.Random(SEED)
series = [rng.randint(0, 999) for _ in range(N)]


def run(s, w, ismin):
    d = deque()
    ops = 0
    maxrem = 0
    maxsize = 0
    best = []
    for i, x in enumerate(s):
        rem = 0
        while d and ((s[d[-1]] >= x) if ismin else (s[d[-1]] <= x)):
            d.pop()
            rem += 1
        d.append(i)
        ops += 1 + rem
        while d[0] <= i - w:
            d.popleft()
            rem += 1
            ops += 1
        maxrem = max(maxrem, rem)
        maxsize = max(maxsize, len(d))
        best.append(s[d[0]] if ismin else s[d[0]])
    return ops, maxrem, maxsize, best


for w in (1, 2, 5, 13, 30):
    lo = run(series, w, True)
    hi = run(series, w, False)
    ok = all(
        lo[3][i] == min(series[max(0, i - w + 1) : i + 1]) and hi[3][i] == max(series[max(0, i - w + 1) : i + 1])
        for i in range(N)
    )
    print(w, "match", ok, "ops", lo[0], hi[0], "max single-push removals", max(lo[1], hi[1]), "max size", max(lo[2], hi[2]))
ser = list(range(13)) + [-1]
print("Corollary 2.5(c) example, w=13, removals at last push:", run(ser, 13, True)[1])
