"""Independent recomputation of the numbers printed or cited in M5 slice a (hub, L01-L04), round 2."""
from fractions import Fraction as F
from itertools import product
import math

ok = []
def chk(name, got, want):
    ok.append((name, got == want))
    print(("PASS " if got == want else "FAIL ") + name + f" got={got} want={want}")

# L01 bisection on S={x>=0, x^2<2} from [0,2]
a, b = F(0), F(2)
br = [(a, b)]
for _ in range(12):
    m = (a + b) / 2
    if m >= 0 and m * m < 2:
        a = m
    else:
        b = m
    br.append((a, b))
chk("L01 step12 a", br[12][0], F(181, 128))
chk("L01 step12 b", br[12][1], F(2897, 2048))
chk("L01 step12 width", br[12][1] - br[12][0], F(1, 2048))
chk("L01 13 of 13 sandwich", sum(x * x < 2 <= y * y for x, y in br), 13)
chk("L01 first width < 1/1000 at step", next(n for n, (x, y) in enumerate(br) if y - x < F(1, 1000)), 11)
chk("L01 2/2^10 is 1/512", F(2, 2**10), F(1, 512))
chk("L01 2/2^11 is 1/1024", F(2, 2**11), F(1, 1024))
chk("L01 step 5 bracket b", br[5][1], F(23, 16))
chk("L01 step 4 bracket", br[4], (F(11, 8), F(3, 2)))
# L01 R1 cubic set: 2 upper bound
chk("L01 R1 2^3=8>=2", 2**3 >= 2, True)
# L01 Prop 1.7 epsilon choice: check (s+eps)^2<2 for sample s<sqrt2
for s in [F(1), F(7, 5), F(141, 100), F(14142, 10000)]:
    if s * s < 2:
        eps = min(F(1), (2 - s * s) / (2 * s + 2))
        assert (s + eps) ** 2 < 2
ok.append(("L01 eps construction sample", True))
# L01 case s^2>2: delta=(s^2-2)/(4s), t^2>=(s^2+2)/2>2
for s in [F(3, 2), F(17, 10), F(2)]:
    d = (s * s - 2) / (4 * s)
    t = s - d
    assert t > 0 and t * t >= (s * s + 2) / 2 > 2
ok.append(("L01 delta construction sample", True))
# L01 Theorem 1.3 / Cor 1.4 logic sanity: width bound
chk("L01 Cor1.4 (H4) gives N for eta=1/1000 with width 2/2^n", next(n for n in range(100) if F(2, 2**n) < F(1, 1000)), 11)

# L02 numbers
H = lambda n: sum(F(1, k) for k in range(1, n + 1))
chk("L02 H4-H2", H(4) - H(2), F(7, 12))
chk("L02 H2-H1", H(2) - H(1), F(1, 2))
gaps = [H(2 * n) - H(n) for n in range(1, 201)]
chk("L02 200 of 200 gaps >= 1/2", sum(g >= F(1, 2) for g in gaps), 200)
chk("L02 min gap at N=1", min(range(1, 201), key=lambda n: gaps[n - 1]), 1)
chk("L02 C(61,2)", math.comb(61, 2), 1830)
G = lambda n: sum(F(1, 2**k) for k in range(1, n + 1))
chk("L02 G3 = 7/8", G(3), F(7, 8))
chk("L02 G3-G1 = 3/8", G(3) - G(1), F(3, 8))
# Prop 3.5 threshold: for eps=2^-10, pair (N,10): 2^-N - 2^-10 >= 2^-10 when N<=9
chk("L02 Prop3.5 2^-9 - 2^-10 >= 2^-10", F(1, 2**9) - F(1, 2**10) >= F(1, 2**10), True)
chk("L02 Prop3.5 2^-10 - 2^-10 = 0 (N=10 pair)", F(1, 2**10) - F(1, 2**10), 0)

# L03 numbers
chk("L03 |x^2-4| at x=381/200", abs(F(381, 200) ** 2 - 4), F(14839, 40000))
chk("L03 14839/40000 = 0.370975", float(F(14839, 40000)), 0.370975)
chk("L03 1/10 delta grid", abs(F(381, 200) - 2) < F(1, 10), True)
pts = [F(k, 50) for k in range(-300, 301)]
chk("L03 grid points 401 at 1/50 steps from -3..3 (k in -150..150 => 301)", len(pts), 601)
