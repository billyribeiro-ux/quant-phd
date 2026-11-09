"""Independent re-derivation of the SC1 project prose numbers (verifier round 17). Standard library only."""
import math
import random
from fractions import Fraction

def inst(seed):
    r = random.Random(1_000_003 * seed + 54_321)
    H = round(r.uniform(0.25, 4.0), 3)
    a = round(r.uniform(0.25, 2.5), 3)
    n = r.randint(4, 256)
    N = r.randint(400, min(800, 200_000 // n))
    return H, a, n, N

H, a, n0, N = inst(0)
print("instance seed0 H a n_steps N:", H, a, n0, N)
tail = math.erfc(a / math.sqrt(2 * H))
print("tail", repr(tail), "tail/2", repr(tail / 2))
# one-step draws: H_B draws sd sqrt(H) in path order
def one_step(seed, N, H, a):
    r = random.Random(seed)
    sd = math.sqrt(H)
    ind = [1.0 if r.gauss(0.0, sd) >= a else 0.0 for _ in range(N)]
    m = sum(ind) / N
    var = sum((x - m) ** 2 for x in ind) / (N - 1)
    return m, math.sqrt(var) / math.sqrt(N), sum(ind)
def grid(seed, N, H, a, n):
    r = random.Random(seed)
    sd = math.sqrt(H / n)
    maxima = []
    for _ in range(N):
        pos = 0.0
        best = -math.inf
        vals = []
        for _k in range(n):
            pos += r.gauss(0.0, sd)
            vals.append(pos)
        maxima.append(vals)
    return maxima
est, se, hits = one_step(0, N, H, a)
target = tail / 2
tse = math.sqrt(target * (1 - target) / N)
band = 5 * tse + 1 / N
print("one-step est", repr(est), "se", repr(se), "hits", hits)
print("target", repr(target), "target se", repr(tse), "band", repr(band), "diff", repr(abs(est - target)))
print("diff/sample se", (est - target) / se, "diff/target se", (est - target) / tse)
print("bias one step", repr(tail - est), "err vs target/2", repr((tail - est) - target))
print("band margin", band - abs(est - target))
rows = {}
for nn in (1, 4, 16, 64, 256):
    vals = grid(0, N, H, a, nn)
    h = sum(1 for v in vals if max(v) >= a)
    p = h / N
    s = math.sqrt(h / N * (1 - h / N) / (N - 1)) if N > 1 else 0
    rows[nn] = (h, p, s)
    print(f"n={nn} hits={h} est={p:.9f} se={s:.9f} tail-est={tail - p:.9f}")
p64 = rows[64][1]
print("n=64 above tail by", repr(p64 - tail), "in SE units", (p64 - tail) / rows[64][2])
for nn in (4, 16, 64, 256):
    p, s = rows[nn][1], rows[nn][2]
    print("n", nn, "within 5 SE of continuous tail:", abs(p - tail) <= 5 * s, "(|p-tail|/se=%.3f)" % (abs(p - tail) / s))
# nested on 256-step paths
paths = grid(0, N, H, a, 256)
fine = sum(1 for v in paths if max(v) >= a)
for coarse in (64, 16, 4, 1):
    stride = 256 // coarse
    c = sum(1 for v in paths if max(v[stride - 1::stride]) >= a)
    print("nested coarse", coarse, c, "fine", fine, "coarse<=fine", c <= fine)
# walk counts
import itertools
mx = en = 0
for steps in itertools.product((1, -1), repeat=12):
    s = list(itertools.accumulate(steps))
    mx += max(s) >= 3
    en += s[-1] >= 3
print("walk12 a=3 max", mx, "end", en, "identity", mx == en + sum(1 for _ in [0]) * 0 + en)
print("2^12", 2**12)
# Lab 1 Simpson difference
def simpson(level, horizon, intervals=4000):
    top = level + 12 * math.sqrt(horizon)
    step = (top - level) / intervals
    d = lambda x: math.exp(-x * x / (2 * horizon)) / math.sqrt(2 * math.pi * horizon)
    tot = d(level) + d(top)
    for k in range(1, intervals):
        tot += (4 if k % 2 else 2) * d(level + k * step)
    return 2 * tot * step / 3
print("simpson diff", abs(simpson(a, H) - tail))
# seed 32 comment claim in test_project line 472-474
H32, a32, n32, N32 = inst(32)
print("seed32 H a n N", H32, a32, n32, N32)
for g in (16, 32, 64):
    r = random.Random(32)
    sd = math.sqrt(H32 / g)
    h = 0
    for _ in range(N32):
        pos = 0.0; best = -math.inf
        for _k in range(g):
            pos += r.gauss(0.0, sd); best = max(best, pos)
        h += best >= a32
    print("seed32 grid", g, "hits", h, "est", h / N32)
