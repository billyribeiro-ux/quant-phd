# Independent recomputation of CS2 L09-L11 printed numbers (unrounded), written by the verifier.
import math, random, bisect
from fractions import Fraction

print("== L09 ==")
N = 2000; SEED = 90
def stream(off):
    rng = random.Random(SEED)
    return [off + rng.random() for _ in range(N)]
def exact_var(xs):
    v = [Fraction(x) for x in xs]; n = len(v); m = sum(v, Fraction(0)) / n
    return sum(((x - m) ** 2 for x in v), Fraction(0)) / (n - 1)
def welford(xs):
    c = 0; m = 0.0; s = 0.0
    for x in xs:
        c += 1; d = x - m; m += d / c; s += d * (x - m)
    return s / (c - 1)
def twopass(xs):
    m = sum(xs) / len(xs); return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
def naive(xs):
    t = 0.0; tq = 0.0
    for x in xs:
        t += x; tq += x * x
    n = len(xs); return (tq - t * t / n) / (n - 1), t, tq
rel = {}
for off in (0.0, 1e6, 1e9):
    xs = stream(off); ex = exact_var(xs)
    nv, t, tq = naive(xs)
    rels = {"W": float(abs(Fraction(welford(xs)) - ex) / ex),
            "2P": float(abs(Fraction(twopass(xs)) - ex) / ex),
            "N": float(abs(Fraction(nv) - ex) / ex)}
    rel[off] = rels
    print(f"offset {off!r}: exact={float(ex)!r} rel={rels} naive_estimate={nv!r} naive_is_zero={nv == 0.0}")
    if off == 1e9:
        print("  naive sum_sq t*t etc:", f"sum x^2 = {tq:.6e}", f"(n*offset^2 = {N*off*off:.6e})")
        print("  true S = (n-1)*s^2 =", float((N - 1) * ex))
        print("  ulp at 2e21 =", 2**(math.frexp(tq)[1] - 53))
        print("  welford/twopass checks: welford rel", rels["W"], "2P", rels["2P"])
ex0 = float(exact_var(stream(0.0)))
print("E2 absolute error Welford offset 0 (unrounded):", rel[0.0]["W"] * ex0, "exact unrounded", repr(ex0))
print("factor naive/Welford offset0:", rel[0.0]["N"] / rel[0.0]["W"])
print("factor naive/Welford offset1e6:", rel[1e6]["N"] / rel[1e6]["W"])
print("factor naive/Welford offset1e9:", rel[1e9]["N"] / rel[1e9]["W"])
print("print-based factors:", 7.286e-15/9.258e-16, 1.418e-2/8.852e-11, 1.000/7.449e-8)

print("== L10 ==")
N10 = 200; SEED10 = 1010
rng = random.Random(SEED10)
series = [rng.randint(0, 999) for _ in range(N10)]
for w in (1, 2, 5, 13, 30):
    # independent deque implementation with explicit counts
    def run(is_min):
        dq = []; ops = 0; maxrem = 0; maxsize = 0; best = []
        for i, x in enumerate(series):
            rem = 0
            while dq and ((series[dq[-1]] >= x) if is_min else (series[dq[-1]] <= x)):
                dq.pop(); rem += 1
            dq.append(i)
            while dq[0] <= i - w:
                dq.pop(0); rem += 1
            ops += 1 + rem; maxrem = max(maxrem, rem); maxsize = max(maxsize, len(dq))
            seg = series[max(0, i - w + 1): i + 1]
            best.append(series[dq[0]] == (min(seg) if is_min else max(seg)))
        return ops, maxrem, maxsize, all(best)
    lo = run(True); hi = run(False)
    print(f"w={w}: min ops {lo[0]} max ops {hi[0]} largest removals {max(lo[1],hi[1])} largest size {max(lo[2],hi[2])} allmatch {lo[3] and hi[3]}")

print("== L11 ==")
N11 = 5000; SEED11 = 2026
rng = random.Random(SEED11)
xs = [rng.random() for _ in range(N11)]
ordered = sorted(xs)
def cap(h, eps):
    return 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / eps)
probes = [Fraction(0), Fraction(1,100), Fraction(1,10), Fraction(1,4), Fraction(1,2), Fraction(3,4), Fraction(9,10), Fraction(99,100), Fraction(1)]
for eps in (Fraction(1, 20), Fraction(1, 10)):
    levels = []; comp = 0
    def push(h, x):
        global comp
        while len(levels) <= h: levels.append([])
        b = levels[h]; b.append(x)
        if len(b) == cap(h, eps):
            b.sort(); kept = b[1::2]; levels[h] = []; comp += 1
            for y in kept: push(h + 1, y)
    for x in xs: push(0, x)
    stored = sum(len(b) for b in levels)
    tw = sum(len(b) * 2**h for h, b in enumerate(levels))
    E = None
    exc = Fraction(0); dfc = Fraction(0)
    for q in probes:
        pairs = sorted((v, 2**h) for h, b in enumerate(levels) for v in b)
        tgt = q * N11; cum = 0
        for v, w_ in pairs:
            cum += w_
            if cum >= tgt: break
        below = bisect.bisect_left(ordered, v); atle = bisect.bisect_right(ordered, v)
        ok = below <= q * N11 + eps * N11 and atle >= q * N11 - eps * N11
        exc = max(exc, Fraction(below) - q * N11); dfc = max(dfc, q * N11 - Fraction(atle))
        assert ok
    print(f"eps={eps}: stored={stored} total_weight={tw} compactions={comp} "
          f"excess/N={float(exc / N11)!r} deficit/N={float(dfc / N11)!r} deficit_is_zero={dfc == 0} excess<eps={exc / N11 < eps}")
print("corollary 2.6 sum (eps=1/20):", sum(cap(h, Fraction(1,20)) - 1 for h in range(13)))
print("closed form bound L=12 eps=1/20:", (13*14*15)/(3*0.05)+13)
print("L=29 eps=1/20 closed form:", (30*31*32)/(3*0.05)+30)
print("E2 bound terms:", [5000 // (cap(h, Fraction(1,20)) * 2**h) for h in range(6)])
print("k_h eps=1/20:", [cap(h, Fraction(1,20)) for h in range(5)], "eps=1/10:", [cap(h, Fraction(1,10)) for h in range(3)])
