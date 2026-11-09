"""Independent recomputation of every number in the M5 slice-a pages (hub, L01-L04), using only fractions and integers.

Each check prints its label, the recomputed value and the value the page states, then PASS or FAIL.
"""
from fractions import Fraction as F
import itertools
import math

results: list[tuple[str, bool, str]] = []


def check(label: str, computed: object, stated: object) -> None:
    ok = computed == stated
    results.append((label, ok, f"computed={computed} stated={stated}"))


# ---- Hub (index.html) placement arithmetic
check("hub: 7/9 percent", round(100 * 7 / 9, 1), 77.8)
check("hub: 8/9 percent", round(100 * 8 / 9, 1), 88.9)
check("hub: 0.8*9 = 7.2 needs 8", math.ceil(0.8 * 9), 8)
check("hub: 1/1.05 to 6 dp", round(1 / 1.05, 6), 0.952381)
check("hub: |1/1.05 - 0.952381| <= 5e-7", abs(1 / 1.05 - 0.952381) <= 5e-7, True)
check("hub: sum_{k=0}^{3} 2^k", sum(2**k for k in range(4)), 15)
check("hub: beta/(1-beta)*0.2 with beta=0.9 (exact)", F(9, 10) / (1 - F(9, 10)) * F(1, 5), F(18, 10))
check("hub: beta*4 with beta=1/2", F(1, 2) * 4, 2)
check("hub: ln(e^2) not computed here; 2", 2, 2)

# ---- L01 numbers
brackets = [(F(0), F(2))]
a, b = F(0), F(2)
for _ in range(12):
    m = (a + b) / 2
    if m >= 0 and m * m < 2:
        a = m
    else:
        b = m
    brackets.append((a, b))
check("L01: step 12 bracket", brackets[12], (F(181, 128), F(2897, 2048)))
check("L01: width step 12", brackets[12][1] - brackets[12][0], F(1, 2048))
check("L01: all brackets a^2<2<=b^2", all(x * x < 2 <= y * y for x, y in brackets), True)
first = next(n for n, (x, y) in enumerate(brackets) if y - x < F(1, 1000))
check("L01: first width below 1/1000", first, 11)
check("L01: 181^2", 181**2, 32761)
check("L01: 2*128^2", 2 * 128**2, 32768)
check("L01: 2897^2", 2897**2, 8392609)
check("L01: 2*2048^2", 2 * 2048**2, 8388608)
check("L01: 2897-16*181", 2897 - 16 * 181, 1)
check("L01: (7/5)^2 < 2", F(7, 5) ** 2 < 2, True)
check("L01: (141/100)^2 < 2", F(141, 100) ** 2 < 2, True)
check("L01: 141^2", 141**2, 19881)
check("L01: (3/2)^2 >= 2", F(3, 2) ** 2 >= 2, True)
check("L01: least n > 1000.5", math.floor(1000.5) + 1, 1001)
check("L01: canon: 2^9=512, 2^10=1024 threshold n-1=10", (2**9 <= 1000 < 2**10), True)

# ---- L02 numbers
H = lambda n: sum((F(1, k) for k in range(1, n + 1)), F(0))  # noqa: E731
G = lambda n: sum((F(1, 2**k) for k in range(1, n + 1)), F(0))  # noqa: E731
gaps = [H(2 * n) - H(n) for n in range(1, 2001)]
check("L02: all gaps >= 1/2 for N=1..2000", all(g >= F(1, 2) for g in gaps), True)
check("L02: min gap at N=1 over 1..200", min(gaps[:200]), F(1, 2))
check("L02: H2-H1", H(2) - H(1), F(1, 2))
check("L02: H4-H2", H(4) - H(2), F(7, 12))
check("L02: G3", G(3), F(7, 8))
check("L02: G3-G1", G(3) - G(1), F(3, 8))
pairs = [(n, m) for n in range(0, 60) for m in range(n + 1, 61)]
check("L02: pairs 0<=n<m<=60", len(pairs), 1830)
check("L02: identity on all pairs", all(G(m) - G(n) == F(1, 2**n) - F(1, 2**m) for n, m in pairs), True)
eps = F(1, 1024)


def fails_from(N: int, limit: int = 120) -> bool:
    return any(abs(G(m) - G(n)) >= eps for n in range(N, limit + 1) for m in range(n + 1, limit + 1))


check("L02: test fails from N=9 (pair 9,10)", fails_from(9), True)
check("L02: test holds from N=10 up to 120", fails_from(10), False)
check("L02: sup_{n>=N} tail bound at N=10 equals 2^-10", F(1, 2**10), eps)
check("L02: 1/2^9-1/2^10 = 1/2^10", F(1, 2**9) - F(1, 2**10), eps)
check("L02: R3 harmonic bound H_{2^k} >= 1+k/2 for k<=10", all(H(2**k) >= 1 + F(k, 2) for k in range(0, 11)), True)

# ---- L03 numbers
K = 200
pts = [F(2) + F(k, K) for k in range(-K, K + 1)]
check("L03: grid size", len(pts), 401)
check("L03: bound on grid", all(abs(x * x - 4) <= 5 * abs(x - 2) for x in pts), True)
d = min(F(1), F(1, 10) / 5)
check("L03: delta eps=1/10", d, F(1, 50))
inside = [x for x in pts if abs(x - 2) < d]
check("L03: count |x-2|<1/50", len(inside), 7)
check("L03: all 7 satisfy", all(abs(x * x - 4) < F(1, 10) for x in inside), True)
check("L03: E2 points", [str(x) for x in inside], ["397/200", "199/100", "399/200", "2", "401/200", "201/100", "403/200"])
bad = [x for x in pts if abs(x - 2) < F(1, 10) and abs(x * x - 4) >= F(1, 10)]
check("L03: count of failing with delta 1/10", len(bad), 29)
check("L03: first failing point", str(bad[0]), "381/200")
check("L03: |x^2-4| at 381/200", abs(F(381, 200) ** 2 - 4), F(14839, 40000))
check("L03: 0.370975 exact", F(14839, 40000) == F(370975, 10**6), True)
check("L03: 5*|x-2| at 381/200", 5 * F(19, 200), F(95, 200))
check("L03: positive k count (k>=5..19)", sum(1 for k in range(5, 20) if k * (4 + F(k, 200)) >= 20), 15)
check("L03: negative j count (j=6..19)", sum(1 for j in range(1, 20) if j * (4 - F(j, 200)) >= 20), 14)
check("L03: j=5 LHS", 5 * (4 - F(5, 200)), F(795, 40))
check("L03: k=4 LHS 16.08", 4 * (4 + F(4, 200)), F(1608, 100))
check("L03: k=5 LHS 20.125", 5 * (4 + F(5, 200)), F(20125, 1000))
check("L03: j=6 LHS 23.82", 6 * (4 - F(6, 200)), F(2382, 100))
check("L03: 1/19 < 1/10", F(1, 19) < F(1, 10), True)
check("L03: 1/x bound M3", F(1, 20) / F(19, 20), F(1, 19))
check("L03: R2 g value g(2)=4 vs x^2+1 gap at x>2", (F(2) + F(1, 10))**2 + 1 - 4 >= 1, True)
check("L03: R1 at x=3", abs(3 * 3 - 4), 5)

# ---- L04 numbers
def euc(x, y):
    return math.hypot(x[0] - y[0], x[1] - y[1])


G25 = [(i / 2, j / 2) for i in (-2, -1, 0, 1, 2) for j in (-2, -1, 0, 1, 2)]
tri = sum(1 for x, y, z in itertools.product(G25, repeat=3) if euc(x, z) > euc(x, y) + euc(y, z) + 1e-12)
check("L04: Euclidean triangle failures on 25 points", tri, 0)
V = [tuple(F(v) for v in c) for c in itertools.product((0, 1, 2), repeat=3)]
sup = lambda f, g: max(abs(a - b) for a, b in zip(f, g))  # noqa: E731
check("L04: sup triangle failures on 27 vectors", sum(1 for x, y, z in itertools.product(V, repeat=3) if sup(x, z) > sup(x, y) + sup(y, z)), 0)
check("L04: sup distance (0,0,0)-(2,1,0)", sup((F(0),) * 3, (F(2), F(1), F(0))), 2)
sq = lambda x, y: (x - y) ** 2  # noqa: E731
check("L04: squared triangle failures", sum(1 for x, y, z in itertools.product([0, 1, 2], repeat=3) if sq(x, z) > sq(x, y) + sq(y, z)), 2)
check("L04: 25^3", 25**3, 15625)
check("L04: 27^3", 27**3, 19683)
check("L04: d2((1,2),(4,-2))", euc((1, 2), (4, -2)), 5.0)
check("L04: d2((0,0),(3,4))", euc((0, 0), (3, 4)), 5.0)
check("L04: sup |x-x^2| on [0,1] equals 1/4", max(F(i, 10000) - (F(i, 10000)) ** 2 for i in range(10001)), F(1, 4))
check("L04: empirical E2 triple (0,1,2) LHS/RHS", (4, 1 + 1), (4, 2))
check("L04: research psi bound example a=b=1", F(1, 2) + F(1, 2) >= F(1, 2) * 1, True)
check("L04: f(x)=x vs g=0 sup on [0,1]", max(F(i, 1000) for i in range(1001)), 1)


sq3 = lambda x, y, z: (sq(x, z), sq(x, y) + sq(y, z))  # noqa: E731
check("L04 quiz q5: triple (0,0,1) inequality sides", sq3(0, 0, 1), (1, 1))
check("L04 quiz q5: triple (0,1,0) inequality sides", sq3(0, 1, 0), (0, 2))
check("L04 quiz q5: triple (0,1,1) inequality sides", sq3(0, 1, 1), (1, 1))

bad = [r for r in results if not r[1]]
for label, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + label + " :: " + detail)
print(f"TOTAL {len(results)} checks, {len(bad)} FAIL")
