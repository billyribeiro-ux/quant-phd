"""Independent recomputation of L09 Lab 1 quantities, unrounded, with exact Fractions and math.frexp."""
import math
import random
from fractions import Fraction

N, SEED = 2000, 90
def stream(off):
    r = random.Random(SEED)
    return [off + r.random() for _ in range(N)]
def welford(xs):
    c, m, s = 0, 0.0, 0.0
    for x in xs:
        c += 1; d = x - m; m += d / c; s += d * (x - m)
    return s / (c - 1), s
def twopass(xs):
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
def naive_parts(xs):
    t = 0.0; q = 0.0
    for x in xs:
        t += x; q += x * x
    n = len(xs)
    return (q - t * t / n) / (n - 1), q, t
def exact(xs):
    v = [Fraction(x) for x in xs]; n = len(v)
    m = sum(v, Fraction(0)) / n
    return sum(((x - m) ** 2 for x in v), Fraction(0)) / (n - 1)
for off in (0.0, 1e6, 1e9):
    xs = stream(off); e = exact(xs); ef = float(e)
    w, S = welford(xs); tp = twopass(xs); nv, q, t = naive_parts(xs)
    rel = lambda est: float(abs(Fraction(est) - e) / e)
    print(f"offset {off:g}: exact {ef!r} ; naive estimate {nv!r}; welford {w!r}; twopass {tp!r}")
    print(f"   rel W {rel(w):.4e} 2P {rel(tp):.4e} N {rel(nv):.4e}  raw {rel(w)!r} {rel(tp)!r} {rel(nv)!r}")
    print(f"   sum x^2 {q:.6e}; sum x {t:.6e}; (n-1)s^2 exact {float((N-1)*e):.6f}; ulp at sum {math.ulp(q):.0f}")
    print(f"   exact (n-1)s^2 = {float((N-1)*e)}  exact var exact-decimal approx {float(e):.10f}")
xs = stream(1e9)
print("naive==0 exactly at 1e9:", naive_parts(xs)[0] == 0.0)
print("ratios: ", rel := None)
