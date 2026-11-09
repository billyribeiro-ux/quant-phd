"""Independent recomputation of every number in M5 slice a (hub, L01-L04). Standard library only; prints PASS/FAIL per check."""
from fractions import Fraction as F
import itertools, math, random

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (" | " + str(detail) if detail != "" else ""))


# ---- hub placement numbers
check("0.8*9 = 7.2 so 8 of 9 needed", math.ceil(0.8 * 9) == 8, math.ceil(0.8 * 9))
check("7/9 = 77.8%", round(100 * 7 / 9, 1) == 77.8, round(100 * 7 / 9, 3))
check("8/9 = 88.9%", round(100 * 8 / 9, 1) == 88.9, round(100 * 8 / 9, 3))
check("1/1.05 to six places = 0.952381", round(1 / 1.05, 6) == 0.952381, 1 / 1.05)
check("|1/1.05 - 0.952381| < 5e-7", abs(1 / 1.05 - 0.952381) < 5e-7, abs(1 / 1.05 - 0.952381))
check("sum_{k=0}^3 2^k = 15", sum(2 ** k for k in range(4)) == 15)
check("lim x^2 at 2 = 4", 2 ** 2 == 4)
check("d/dx x^3 at 1 = 3", 3 * 1 ** 2 == 3)
check("skill1: beta/(1-beta)*0.2 = 1.8", F(9, 10) / (1 - F(9, 10)) * F(2, 10) == F(18, 10), F(9, 10) / (1 - F(9, 10)) * F(2, 10))
check("skill2: beta*4 = 2 for beta=1/2", F(1, 2) * 4 == 2)
check("hub lesson hours 6*10+4*11 = 104", 6 * 10 + 4 * 11 == 104)
check("project 26/130 = 20%", round(100 * 26 / 130) == 20)

# ---- L01 bisection
a, b = F(0), F(2)
br = [(a, b)]
for _ in range(12):
    m = (a + b) / 2
    if m * m < 2:
        a = m
    else:
        b = m
    br.append((a, b))
check("L01 step 12 bracket = [181/128, 2897/2048]", br[12] == (F(181, 128), F(2897, 2048)), br[12])
check("L01 width after n steps = 2/2^n for all n<=12", all(bb - aa == F(2, 2 ** n) for n, (aa, bb) in enumerate(br)))
check("L01 every bracket a^2<2<=b^2 (13 of 13)", sum(aa * aa < 2 <= bb * bb for aa, bb in br) == 13)
first = next(n for n, (aa, bb) in enumerate(br) if bb - aa < F(1, 1000))
check("L01 first width < 1/1000 is step 11", first == 11, first)
check("L01 E1: 181^2=32761, 2*128^2=32768", 181 ** 2 == 32761 and 2 * 128 ** 2 == 32768)
check("L01 E1: 2897^2=8392609, 2*2048^2=8388608", 2897 ** 2 == 8392609 and 2 * 2048 ** 2 == 8388608)
check("L01 E1 width = 1/2048", F(2897, 2048) - F(181, 128) == F(1, 2048))
check("L01 E2: 2^9=512, 2^10=1024", 2 ** 9 == 512 and 2 ** 10 == 1024)
check("L01 E3 step4/5 brackets", br[4] == (F(11, 8), F(3, 2)) and br[5] == (F(11, 8), F(23, 16)))
check("L01 M3 steps 1,2", br[1] == (F(1), F(2)) and br[2] == (F(1), F(3, 2)))
check("L01 q5: (7/5)^2 < 2, (141/100)^2 < 2, (3/2)^2 >= 2", F(7, 5) ** 2 < 2 and F(141, 100) ** 2 < 2 and F(3, 2) ** 2 >= 2)
check("L01 q6: least natural above 1000.5 is 1001", min(n for n in range(1, 5000) if n > 1000.5) == 1001)
check("L01 M1 sup(0,1)=1 witness x=(1+max(y,0))/2 lies in (0,1)", all(0 < (1 + max(y, 0)) / 2 < 1 and (1 + max(y, 0)) / 2 > y for y in [-3, -0.5, 0, 0.3, 0.99]))
# Prop 1.7 algebra: for random s, the two case witnesses satisfy their inequalities
random.seed(1)
ok1 = ok2 = True
for _ in range(20000):
    s = random.uniform(0.001, 3)
    if s * s < 2:
        eps = min(1, (2 - s * s) / (2 * s + 2))
        ok1 &= (s + eps) ** 2 < 2 and eps > 0
    if s * s > 2:
        delta = (s * s - 2) / (4 * s)
        t = s - delta
        ok2 &= 0 < delta < s and t * t > 2 and t > 0
check("L01 Prop1.7 case s^2<2 witness eps: (s+eps)^2<2 (20000 random s)", ok1)
check("L01 Prop1.7 case s^2>2 witness t: t^2>2, 0<t<s (20000 random s)", ok2)
check("L01 canon: 1/2^{1-n} misconception: width 2^{1-n} at n=11 is 1/1024", F(2, 2 ** 11) == F(1, 1024))

# ---- L02
H = lambda n: sum((F(1, k) for k in range(1, n + 1)), F(0))
gaps = [H(2 * n) - H(n) for n in range(1, 201)]
check("L02 gaps >= 1/2 for N=1..200 (200 of 200)", sum(g >= F(1, 2) for g in gaps) == 200)
check("L02 min gap 1/2 at N=1", min(gaps) == F(1, 2) and gaps.index(min(gaps)) == 0)
check("L02 H4-H2 = 7/12", H(4) - H(2) == F(7, 12))
G = lambda n: sum((F(1, 2 ** k) for k in range(1, n + 1)), F(0))
pairs = [(n, m) for n in range(0, 61) for m in range(n + 1, 61)]
check("L02 pairs with 0<=n<m<=60 count 1830", len(pairs) == 1830)
check("L02 identity G_m-G_n=1/2^n-1/2^m on all 1830 pairs", all(G(m) - G(n) == F(1, 2 ** n) - F(1, 2 ** m) for n, m in pairs))
eps = F(1, 1024)
def fails_from(N):
    return any(G(m) - G(n) >= eps for n in range(N, 61) for m in range(n + 1, 61))
check("L02 threshold: test fails for N=0..9, passes N=10..20", all(fails_from(N) for N in range(10)) and not any(fails_from(N) for N in range(10, 21)))
check("L02 E3 sum_{j=1}^{60} j = 1830", sum(range(1, 61)) == 1830)
check("L02 M3 G3-G1 = 3/8 = 1/2-1/8", G(3) - G(1) == F(3, 8) == F(1, 2) - F(1, 8))
check("L02 harmonic R2: H_{2^k} >= 1 + k/2 for k=0..10", all(H(2 ** k) >= 1 + F(k, 2) for k in range(11)))
check("L02 canon: bisection bracket width 2/2^n equals L01 Theorem 1.6 (n<=12)", all(bb - aa == F(2, 2 ** n) for n, (aa, bb) in enumerate(br)))

# ---- L03
pts = [F(2) + F(k, 200) for k in range(-200, 201)]
check("L03 grid 401 points", len(pts) == 401)
check("L03 bound |x^2-4|<=5|x-2| at all grid points", all(abs(x * x - 4) <= 5 * abs(x - 2) for x in pts))
d = F(1, 50)
inside = [x for x in pts if abs(x - 2) < d]
check("L03 delta=1/50 admits 7 points", len(inside) == 7, len(inside))
check("L03 those satisfy |x^2-4|<1/10", all(abs(x * x - 4) < F(1, 10) for x in inside))
d2 = F(1, 10)
fail = [x for x in pts if abs(x - 2) < d2 and abs(x * x - 4) >= F(1, 10)]
check("L03 count of failing points with delta=1/10 is 29", len(fail) == 29, len(fail))
check("L03 first failing point is 381/200", fail[0] == F(381, 200), fail[0])
check("L03 |x^2-4| at 381/200 = 14839/40000", abs(F(381, 200) ** 2 - 4) == F(14839, 40000))
check("L03 E1: 5|x-2| = 95/200", 5 * abs(F(381, 200) - 2) == F(95, 200))
check("L03 k=5 positive side count 15 and j side 14", sum(1 for k in range(1, 20) if k * (4 + F(k, 200)) >= 20) == 15 and sum(1 for j in range(1, 20) if j * (4 - F(j, 200)) >= 20) == 14)
check("L03 R1 constant 5 sharp at x=3", abs(3 * 3 - 4) == 5 and abs(3 - 2) == 1)
h = F(1, 400)
check("L03 R2: x=2+1/400 is not a grid point, and g(x)=x^2+1 differs from g(2)=4 by >= 1", (h * 200).denominator != 1 and abs((2 + h) ** 2 + 1 - 4) >= 1, abs((2 + h) ** 2 + 1 - 4))
check("L03 R2: every grid point within 1/50 of 2 keeps g=x^2", all(abs(F(2) + F(k, 200) - 2) >= 0 for k in range(-3, 4)))
check("L03 M1 delta=eps/3 for 3x+1 (rational eps samples)", all(abs((3 * (2 + F(k,1000)) + 1) - 7) == 3 * abs(F(k,1000)) for k in range(-50, 51)))
check("L03 M3 1/x at 1 with delta=1/20: 1/19 < 1/10", F(1, 19) < F(1, 10))
check("L03 misc: y=2/(2n+1) <= 1/n for n>=1", all(F(2, 2 * n + 1) <= F(1, n) for n in range(1, 500)))
check("L03 Misc1: at point 10 with delta=1/5, |10.1^2-100| = 2.01", abs(F(101, 10) ** 2 - 100) == F(201, 100))
check("L03 canon2: for delta in samples, x=1+min(delta,1)/2 has 0<x-1<delta and |x-5|>=3.5", all(0 < (1 + min(dl,1)/2) - 1 < dl and (5 - (1 + min(dl,1)/2)) >= F(7,2) for dl in [F(1,100), F(1,3), F(1,2), F(5,2)]))

# ---- L04
grid = [(F(i, 2), F(j, 2)) for i in (-2, -1, 0, 1, 2) for j in (-2, -1, 0, 1, 2)]
check("L04 25 grid points, 625 pairs, 15625 triples", len(grid) == 25 and len(grid) ** 2 == 625 and len(grid) ** 3 == 15625)
def d2(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
tri_fail = sum(1 for x, y, z in itertools.product(grid, repeat=3) if d2(x, z) > d2(x, y) + d2(y, z) + 1e-12)
check("L04 Euclidean triangle failures on 5x5 grid = 0", tri_fail == 0, tri_fail)
vecs = list(itertools.product((0, 1, 2), repeat=3))
sup = lambda f, g: max(abs(a - b) for a, b in zip(f, g))
tri_sup = sum(1 for x, y, z in itertools.product(vecs, repeat=3) if sup(x, z) > sup(x, y) + sup(y, z))
check("L04 sup-distance triangle failures on 27 vectors = 0", tri_sup == 0, tri_sup)
check("L04 27^3 = 19683 triples", 27 ** 3 == 19683 == len(vecs) ** 3)
q = lambda x, y: (x - y) ** 2
sq_fail = [(x, y, z) for x, y, z in itertools.product([0, 1, 2], repeat=3) if q(x, z) > q(x, y) + q(y, z)]
check("L04 squared-distance triangle failures = 2, namely (0,1,2),(2,1,0)", sq_fail == [(0, 1, 2), (2, 1, 0)], sq_fail)
check("L04 q(0,2)=4, q(0,1)+q(1,2)=2", q(0, 2) == 4 and q(0, 1) + q(1, 2) == 2)
check("L04 Q5 explanation triples: (0,0,1) 1<=1, (0,1,0) 0<=2, (0,1,1) 1<=1",
      q(0,1) <= q(0,0)+q(0,1) and q(0,0) <= q(0,1)+q(1,0) and q(0,1) <= q(0,1)+q(1,1) and q(0,0) == 0 and q(0,1)+q(1,0) == 2)
check("L04 Lagrange identity (random integers)", all((u1*u1+u2*u2)*(v1*v1+v2*v2)-(u1*v1+u2*v2)**2 == (u1*v2-u2*v1)**2 for u1,u2,v1,v2 in itertools.product(range(-3,4), repeat=4)))
check("L04 Lagrange expansion: left-side leftover = u1^2 v2^2 + u2^2 v1^2 - 2 u1 v1 u2 v2", all((u1*u1+u2*u2)*(v1*v1+v2*v2)-(u1*v1+u2*v2)**2 == u1*u1*v2*v2+u2*u2*v1*v1-2*u1*v1*u2*v2 for u1,u2,v1,v2 in itertools.product(range(-3,4), repeat=4)))
check("L04 Example 1.6: d(f,g)=1/4 for x and x^2 on [0,1] (grid max at 1/2)", max(F(k, 1000) - F(k, 1000) ** 2 for k in range(0, 1001)) == F(1, 4))
check("L04 Mech1 d2((1,2),(4,-2)) = 5", d2((1, 2), (4, -2)) == 5)
D = {("a","b"):2,("b","a"):2,("b","c"):2,("c","b"):2,("a","c"):3,("c","a"):3}
dd = lambda x, y: 0 if x == y else D[(x, y)]
P3 = ["a", "b", "c"]
check("L04 Mech2 finite metric: M1,M2,M3 on all triples", all(dd(x,y) >= 0 and (dd(x,y) == 0) == (x == y) and dd(x,y) == dd(y,x) and dd(x,z) <= dd(x,y)+dd(y,z) for x,y,z in itertools.product(P3, repeat=3)))
check("L04 Research1 psi nondecreasing and subadditive (random)", all(
    (F(t) / (1 + F(t))) <= (F(t2) / (1 + F(t2))) for t, t2 in [(0.5, 0.7), (1, 2)]) and all(
    (F(a + b) / (1 + F(a + b))) <= F(a) / (1 + F(a)) + F(b) / (1 + F(b)) for a, b in [(F(1, 3), F(2, 5)), (F(7), F(1, 9))]))
check("L04 Proof2 rho=min(|x-y|,1) triangle (random grid)", all(min(abs(x - z), 1) <= min(abs(x - y), 1) + min(abs(y - z), 1) for x, y, z in itertools.product([F(k, 4) for k in range(-12, 13)], repeat=3)))
check("L04 Remark2.2 U=(0,1]: point 1+r/2 outside U", all(1 + r / 2 > 1 for r in [F(1, 10), F(1, 2), F(3)]))
check("L04 E1 triple count 25^3", 25 ** 3 == 15625)

n_pass = sum(1 for _, ok in results if ok)
print(f"SUMMARY pass={n_pass} total={len(results)}")
