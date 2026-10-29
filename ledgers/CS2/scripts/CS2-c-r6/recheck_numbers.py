import math, random
from fractions import Fraction
import importlib.util, sys, io, contextlib

def load(path):
    spec = importlib.util.spec_from_file_location("twin_" + str(abs(hash(path))), path)
    m = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(m)
    return m, buf.getvalue()

# L09 numbers
N = 2000
rng = random.Random(90)
xs = [0.0 + rng.random() for _ in range(N)]
ex = [Fraction(x) for x in xs]
mean = sum(ex, Fraction(0)) / N
exact = sum(((x - mean) ** 2 for x in ex), Fraction(0)) / (N - 1)
print("L09 exact sample variance (unrounded float):", repr(float(exact)))
print("L09 (n-1)s^2 offset 0 =", float(exact) * (N - 1))
rel0_welford = 9.25811790803366e-16
print("E2 abs error offset0 = exact*relerr =", float(exact) * rel0_welford)
for off in (1e9,):
    rng = random.Random(90)
    ys = [off + rng.random() for _ in range(N)]
    total = 0.0; total_sq = 0.0
    for y in ys:
        total += y; total_sq += y * y
    print("L09 naive running sum of squares at offset 1e9 =", repr(total_sq), "%.10e" % total_sq)
    print("math.ulp(2e21) =", math.ulp(2e21))
    e = Fraction(off)
    exy = [Fraction(y) for y in ys]
    m = sum(exy, Fraction(0)) / N
    S = sum(((y - m) ** 2 for y in exy), Fraction(0))
    print("L09 S_n true at offset 1e9 (exact) =", float(S))
# ratios from printed three-digit values
print("ratio offset0", 7.286e-15 / 9.258e-16, "ratio 1e6", 1.418e-2 / 8.852e-11, "ratio 1e9", 1.0 / 7.449e-8)
# L09 claim exact unrounded ratios
print("unrounded ratio offset0 (naive relerr 7.286e-15 vs welford 9.258e-16):", 7.286e-15/9.258e-16)

# L11 numbers
def bound(L, eps):
    return (L+1)*(L+2)*(L+3)/(3*eps) + (L+1)
print("L11 closed form n=1e9 eps=1/20:", bound(29, 1/20), "L=", int(math.log2(10**9)), "floor log2 1e9 check", 2**29 <= 10**9 < 2**30)
print("L11 closed form n=5000 eps=1/20:", bound(12, 1/20), "L check", 2**12 <= 5000 < 2**13)
print("L11 exact sum n=5000 eps=1/20:", sum(math.ceil(0) for _ in [])+sum(2*math.ceil(Fraction((h+1)*(h+2),2)/Fraction(1,20)) - 1 for h in range(13)))
print("L11 exact sum for eps=1/10 n=5000:", sum(2*math.ceil(Fraction((h+1)*(h+2),2)/Fraction(1,10)) - 1 for h in range(13)))
print("L11 n=1e9 eps=1/20 exact sum:", sum(2*math.ceil(Fraction((h+1)*(h+2),2)/Fraction(1,20)) - 1 for h in range(30)))
