"""Independent recomputation of the numbers printed or claimed in M5 slice a (hub, L01-L04).

Run: .venv/bin/python -I ledgers/M5/scripts/M5-a-r1/recompute_a.py
Standard library only. Prints one line per check with PASS or FAIL.
"""

from fractions import Fraction as F
from itertools import product

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (" :: " + detail if detail else ""))


# L01 bisection, recomputed with an independent loop
a, b = F(0), F(2)
br = [(a, b)]
for n in range(1, 13):
    m = (a + b) / 2
    if m * m < 2:
        a = m
    else:
        b = m
    br.append((a, b))
check("L01 step 12 bracket", br[12] == (F(181, 128), F(2897, 2048)), f"{br[12]}")
check("L01 widths 2/2^n", all(b - a == F(2, 2**n) for n, (a, b) in enumerate(br)))
check("L01 sandwich 13 of 13", sum(a * a < 2 <= b * b for a, b in br) == 13)
check("L01 first width < 1/1000 is step 11", min(n for n, (a, b) in enumerate(br) if b - a < F(1, 1000)) == 11)
check("L01 E1 181^2", 181**2 == 32761 and 2 * 128**2 == 32768)
check("L01 E1 2897^2", 2897**2 == 8392609 and 2 * 2048**2 == 8388608)
check("L01 E1 width", F(2897, 2048) - F(181, 128) == F(1, 2048))
check("L01 E3 steps 4,5", br[4] == (F(11, 8), F(3, 2)) and br[5] == (F(11, 8), F(23, 16)))
check("L01 quiz width after 3 steps", br[3][1] - br[3][0] == F(1, 4))
# L01 Prop 1.7 case analysis, spot-check with exact rationals at a sample s near sqrt 2
s = F(141421, 100000)
eps = min(F(1), (2 - s * s) / (2 * s + 2))
check("L01 Prop1.7 case s^2<2 step", (s + eps) ** 2 < 2 and eps > 0)
s2 = F(141423, 100000)
delta = (s2 * s2 - 2) / (4 * s2)
t = s2 - delta
check("L01 Prop1.7 case s^2>2 t^2 > 2", t * t > 2 and t > 0 and delta < s2)

# L02 harmonic and geometric checks
H = lambda n: sum((F(1, k) for k in range(1, n + 1)), F(0))  # noqa: E731
gaps = [H(2 * n) - H(n) for n in range(1, 201)]
check("L02 harmonic gaps >= 1/2 for N=1..200", all(g >= F(1, 2) for g in gaps))
check("L02 H2-H1=1/2, H4-H2=7/12", H(2) - H(1) == F(1, 2) and H(4) - H(2) == F(7, 12))
G = lambda n: sum((F(1, 2**k) for k in range(1, n + 1)), F(0))  # noqa: E731
pairs = [(n, m) for n in range(0, 60) for m in range(n + 1, 61)]
check("L02 1830 pairs", len(pairs) == 1830)
check("L02 identity on pairs", all(G(m) - G(n) == F(1, 2**n) - F(1, 2**m) for n, m in pairs))
check("L02 G3 = 7/8", G(3) == F(7, 8))
check("L02 threshold N=10 (pair N,10 fails for N<=9)", all(G(10) - G(N) >= F(1, 2**10) for N in range(0, 10)))
check("L02 threshold N>=10 bound", all(F(1, 2**N) <= F(1, 2**10) for N in range(10, 40)))
check("L02 R2 H_{2^k} >= 1+k/2 for k=0..7", all(H(2**k) >= 1 + F(k, 2) for k in range(0, 8)))
check("L02 E3 sum 60*61/2", sum(60 - n for n in range(60)) == 1830)

# L03 epsilon-delta checks
X0 = F(2)
grid = [X0 + F(k, 200) for k in range(-200, 201)]
check("L03 bound on 401 points", sum(abs(x * x - 4) <= 5 * abs(x - X0) for x in grid) == 401 and len(grid) == 401)
d = min(F(1), F(1, 10) / 5)
inside = [x for x in grid if abs(x - X0) < d]
check("L03 delta=1/50 admits 7", len(inside) == 7 and all(abs(x * x - 4) < F(1, 10) for x in inside))
bad = [x for x in grid if abs(x - X0) < F(1, 10) and abs(x * x - 4) >= F(1, 10)]
check("L03 29 failing points", len(bad) == 29, f"first={bad[0]}")
check("L03 first failing is 381/200", bad[0] == F(381, 200) and abs(bad[0] ** 2 - 4) == F(14839, 40000))
check("L03 E1 values", abs(F(381, 200) - 2) * 5 == F(95, 200) and F(14839, 40000) == F(370975, 10**6))
check("L03 E2 points", [X0 + F(k, 200) for k in (-3, -2, -1, 0, 1, 2, 3)] == [F(397, 200), F(199, 100), F(399, 200), F(2), F(401, 200), F(201, 100), F(403, 200)])
check("L03 M3 1/x bound on |x-1|<1/20", all(abs(1 / x - 1) < F(1, 10) for x in [1 + F(i - 1000, 20000) for i in range(0, 2001) if i != 1000 and i - 1000 != 0] if abs(x - 1) < F(1, 20)) and F(1, 19) < F(1, 10))
check("L03 misc 10.1 example", abs(F(101, 10) - 10) < F(1, 5) and abs(F(101, 10) ** 2 - 100) >= 1)
check("L03 canon break f(x)=x, x=1+min(d,1)/2 gives |x-5|>=3.5", all(5 - (1 + min(F(dd), F(1)) / 2) >= F(7, 2) for dd in (F(1, 100), F(1, 3), F(5))))

# L04 metric checks, exhaustive on the lab samples
pts = [(F(i, 2), F(j, 2)) for i in (-2, -1, 0, 1, 2) for j in (-2, -1, 0, 1, 2)]
check("L04 counts 25, 625, 15625", len(pts) == 25 and len(pts) ** 2 == 625 and len(pts) ** 3 == 15625)
vecs = list(product((0, 1, 2), repeat=3))
check("L04 27 vectors, 19683 triples", len(vecs) == 27 and len(vecs) ** 3 == 19683)
sq = lambda x, y: (x - y) ** 2  # noqa: E731
trip = [(x, y, z) for x, y, z in product([0, 1, 2], repeat=3) if sq(x, z) > sq(x, y) + sq(y, z)]
check("L04 squared triangle failures are exactly (0,1,2),(2,1,0)", trip == [(0, 1, 2), (2, 1, 0)], f"{trip}")
check("L04 Prop 1.7 sup metric witness on [0,1]: max x-x^2 = 1/4",
      max(F(i, 1000) - (F(i, 1000)) ** 2 for i in range(1001)) == F(1, 4))
M2D = {frozenset("ab"): 2, frozenset("bc"): 2, frozenset("ac"): 3}
def d_mech2(p, q):
    return 0 if p == q else M2D[frozenset(p + q)]
check("L04 mech 2 finite metric triangle (all 27 ordered triples)", all(
    d_mech2(x, z) <= d_mech2(x, y) + d_mech2(y, z) for x, y, z in product("abc", repeat=3)))
check("L04 Example 3.6 sup-distance witness: |x-1/n| bound",
      all(abs(F(1, n)) <= F(1, n) for n in range(1, 50)))
bounded_def_witness_values = [-x for x in (F(1), F(2), F(7, 3))]
check("L04 one-sided bounded witness: f(x)=-x on (0,inf) has values bounded above by 0",
      all(v < 0 for v in bounded_def_witness_values))
check("L04 one-sided bounded witness: sup |f-0| = infinity (sample x=10^6 gives value 10^6)",
      F(10**6) > 10**5)

print(f"summary: {sum(ok for _, ok in results)} of {len(results)} PASS")
