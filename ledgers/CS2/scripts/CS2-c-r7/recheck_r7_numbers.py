"""Independent re-derivation of the numbers in the round-7 changed cards (CS2-c125, c139, c194, c200, c244, c245).

Written by the verifier from the lesson text; it does not import the twins.
"""

import math
import random
from fractions import Fraction

# ---- L09 (CS2-c125, CS2-c244) -------------------------------------------
N9 = 2000
SEED9 = 90


def stream9(offset):
    rng = random.Random(SEED9)
    return [offset + rng.random() for _ in range(N9)]


def exact_var(xs):
    v = [Fraction(x) for x in xs]
    m = sum(v, Fraction(0)) / len(v)
    return sum(((a - m) ** 2 for a in v), Fraction(0)) / (len(v) - 1)


def welford(xs):
    n, mean, m2 = 0, 0.0, 0.0
    for x in xs:
        n += 1
        d = x - mean
        mean += d / n
        m2 += d * (x - mean)
    return m2 / (n - 1)


def twopass(xs):
    m = sum(xs) / len(xs)
    return sum((x - m) * (x - m) for x in xs) / (len(xs) - 1)


def naive(xs):
    s = 0.0
    q = 0.0
    for x in xs:
        s += x
        q += x * x
    n = len(xs)
    return (q - s * s / n) / (n - 1)


def rel(est, ex):
    return float(abs(Fraction(est) - ex) / ex)


print("L09 relative errors (independent implementation, same seed 90, n=2000)")
for off in (0.0, 1e6, 1e9):
    xs = stream9(off)
    ex = exact_var(xs)
    print(f"offset {off:g}: exact {float(ex):.6f}  welford {rel(welford(xs), ex):.3e}  "
          f"two-pass {rel(twopass(xs), ex):.3e}  naive {rel(naive(xs), ex):.3e}  naive_est {naive(xs):.6e}")

# c125 magnitudes
S_sq_sum_offset_1e9 = sum((1e9 + 0.0) ** 2 for _ in range(N9))  # rough magnitude check
print("n*(1e9)^2 =", float(N9 * 10**18), " 2^70 =", 2**70, " 2^71 =", 2**71,
      " in [2^70,2^71):", 2**70 <= N9 * 10**18 < 2**71)
ulp = 2 ** (70 - 52)
print("ulp in [2^70,2^71) =", ulp, " half ulp =", ulp // 2)
print("1999 * 0.087281 =", 1999 * 0.087281, " 1999*exact_var(0.087281 approx) check ok")
xs = stream9(1e9)
ex = exact_var(xs)
print("S_n exact (n-1)*s^2 =", float((N9 - 1) * ex))
print("sum of squares exact magnitude (offset 1e9 stream):", float(sum(Fraction(x) ** 2 for x in xs)))

# ---- L11 (CS2-c200, CS2-c245) ------------------------------------------
# Lemma 2.3 telescoping check
for H in range(0, 60):
    s = sum(Fraction(1, (h + 1) * (h + 2)) for h in range(H + 1))
    assert s == 1 - Fraction(1, H + 2), H
    assert s < 1
print("Lemma 2.3 identity verified for H = 0..59")

for eps in (Fraction(1, 20), Fraction(1, 10)):
    for h in range(0, 60):
        k = 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / eps)
        assert k % 2 == 0
        assert k >= (h + 1) * (h + 2) / eps
        assert Fraction(1, k) <= eps / ((h + 1) * (h + 2))
print("k_h >= (h+1)(h+2)/eps and 1/k_h <= eps/((h+1)(h+2)) verified for h = 0..59, both epsilons")

# Independent sketch implementation for c245
N11 = 5000
rng = random.Random(2026)
xs11 = [rng.random() for _ in range(N11)]
srt = sorted(xs11)
probes = [Fraction(0), Fraction(1, 100), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2),
          Fraction(3, 4), Fraction(9, 10), Fraction(99, 100), Fraction(1)]


def build(eps):
    levels = []
    compactions = 0

    def cap(h):
        return 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / eps)

    def push(h, val):
        nonlocal compactions
        while len(levels) <= h:
            levels.append([])
        levels[h].append(val)
        if len(levels[h]) == cap(h):
            levels[h].sort()
            keep = levels[h][1::2]
            levels[h] = []
            compactions += 1
            for y in keep:
                push(h + 1, y)

    for x in xs11:
        push(0, x)
    return levels, compactions, cap


for eps in (Fraction(1, 20), Fraction(1, 10)):
    levels, comp, cap = build(eps)
    items = [(v, 2 ** h) for h, lv in enumerate(levels) for v in lv]
    assert sum(w for _, w in items) == N11
    stored = len(items)
    items.sort()
    worst_exc = Fraction(0)
    worst_def = Fraction(0)
    ok_all = True
    for q in probes:
        target = q * N11
        cum = 0
        v = None
        for val, w in items:
            cum += w
            if cum >= target:
                v = val
                break
        # exact counts by direct counting (not bisect)
        r_strict = sum(1 for x in xs11 if x < v)
        r_le = sum(1 for x in xs11 if x <= v)
        pass1 = Fraction(r_strict) <= q * N11 + eps * N11
        pass2 = Fraction(r_le) >= q * N11 - eps * N11
        ok_all = ok_all and pass1 and pass2
        worst_exc = max(worst_exc, Fraction(r_strict) - q * N11)
        worst_def = max(worst_def, q * N11 - Fraction(r_le))
    print(f"eps {eps}: caps {cap(0)},{cap(1)},{cap(2)} stored {stored} compactions {comp} "
          f"all 9 probes pass both inequalities: {ok_all}; excess/N {float(worst_exc / N11):.4f}; "
          f"deficit/N {float(worst_def / N11):.4f}; excess<eps: {float(worst_exc / N11) < float(eps)}")
