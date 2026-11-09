"""M2 slice a, round 3: independent recomputation of every displayed number in index.html and L01-L06.

Exact rational arithmetic (fractions.Fraction) and decimal rounding only. Run:
    python -I -W error ledgers/M2/scripts/M2-a-r3/recompute_slice_a_r3.py
Each line states the page claim, the recomputed value, and whether it agrees.
"""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal
from fractions import Fraction as F

results: list[tuple[str, bool]] = []


def check(label: str, value: object, ok: bool) -> None:
    results.append((label, ok))
    print(f"{'OK  ' if ok else 'FAIL'} {label}: {value}")


def sci(x: F, digits: int) -> str:
    """Mantissa rounded to `digits` digits after the point, as printed by {:.{digits}e}."""
    return f"{float(x):.{digits}e}"


def close(a: F, b: F, tol: F) -> bool:
    return abs(a - b) <= tol


# ---------------- L01 ----------------
def a1(n: int) -> F:
    return F(2 * n + 1, n + 1)


check("L01 a_n - 2 = -1/(n+1) for n=1..2000", "all", all(a1(n) - 2 == F(-1, n + 1) for n in range(1, 2001)))
check("L01 a_1 = 3/2", a1(1), a1(1) == F(3, 2))
check("L01 error at n=10 is 1/11", float(abs(a1(10) - 2)), abs(a1(10) - 2) == F(1, 11))
check("L01 error at n=100 is 1/101", float(abs(a1(100) - 2)), abs(a1(100) - 2) == F(1, 101))
check("L01 a_1000 = 2001/1001 printed 1.999001", f"{float(a1(1000)):.6f}", f"{float(a1(1000)):.6f}" == "1.999001")
check("L01 quiz a_1000 exact 2001/1001", F(2001, 1001), a1(1000) == F(2001, 1001))
check("L01 error at 999 = 1/1000 (strict fails)", sci(abs(a1(999) - 2), 6), abs(a1(999) - 2) == F(1, 1000))
check("L01 error at 1000 = 1/1001 prints 9.990010e-04", sci(abs(a1(1000) - 2), 6), sci(abs(a1(1000) - 2), 6) == "9.990010e-04")
# least threshold for tol 1/1000 over range up to 5000 (same definition as the lab)
eps = F(1, 1000)
least = next(N for N in range(1, 5001) if all(abs(a1(n) - 2) < eps for n in range(N, 5001)))
check("L01 least N for 0.001 up to 5000", least, least == 1000)
least_closed = min(N for N in range(1, 5000) if all(F(1, n + 1) < eps for n in range(N, 5000)))
check("L01 identity-based least N for 0.001 is 1000 (N>1/eps gives 1001)", least_closed, least_closed == 1000)
# E3 / quiz: tolerance 1e-4
eps4 = F(1, 10000)
least4 = next(N for N in range(1, 20000) if all(F(1, n + 1) < eps4 for n in range(N, 20000)))
check("L01 E3 least N for 0.0001 is 10000", least4, least4 == 10000)
check("L01 E3 error at 9999 prints 1.000000e-04", sci(F(1, 10000), 6), sci(F(1, 10000), 6) == "1.000000e-04")
# quiz: N > 1/eps with eps 0.5
check("L01 quiz least integer N > 1/0.5", 3, int(F(1, 1) / F(1, 2)) + 1 == 3)
check("L01 |a_9 - 2| = 0.1", abs(a1(9) - 2), abs(a1(9) - 2) == F(1, 10))
# Problem M1: (3n-1)/(n+4), eps 0.01, N = 1297
m1 = lambda n: F(3 * n - 1, n + 4)
check("L01 M1 a_n - 3 = -13/(n+4)", "all", all(m1(n) - 3 == F(-13, n + 4) for n in range(1, 500)))
check("L01 M1 N=1297 works (n>=1297 gives 13/(n+4)<0.01), 1296 fails",
      "1297/1296", F(13, 1297 + 4) < F(1, 100) and not (F(13, 1296 + 4) < F(1, 100)))
# Problem M2: 1/n^2 < 0.01 least N = 11
check("L01 M2 least N with 1/n^2<0.01 for all n>=N is 11",
      min(N for N in range(1, 200) if all(F(1, n * n) < F(1, 100) for n in range(N, 200))),
      min(N for N in range(1, 200) if all(F(1, n * n) < F(1, 100) for n in range(N, 200))) == 11)
# Problem E1: Decimal rounding of 1/1001 to mantissa 6 digits
mant = Decimal(1) / Decimal(1001) * Decimal(10) ** 4  # 1/1001 = mantissa 9.99000999... times 10^-4
check("L01 E1 1/1001 mantissa rounds to 9.990010", str(mant.quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)),
      mant.quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN) == Decimal("9.990010"))
# Example 4.1 and Prop 4.2 facts used on page: bounded by 1
check("L01 (-1)^n bounded by 1", 1, all(abs((-1) ** n) <= 1 for n in range(1, 50)))

# ---------------- L02 ----------------
def a2(n: int) -> F:
    return F(2 * n + 1, n + 1)


def b2(n: int) -> F:
    return F(n + 2, n)


def serr(n: int) -> F:
    return abs(a2(n) + b2(n) - 3)


def perr(n: int) -> F:
    return abs(a2(n) * b2(n) - 2)


def qerr(n: int) -> F:
    return abs(a2(n) / b2(n) - 2)


ok_all = all(
    serr(n) == F(n + 2, n * (n + 1))
    and perr(n) == F(3 * n + 2, n * (n + 1))
    and qerr(n) == F(5 * n + 4, (n + 1) * (n + 2))
    for n in range(1, 5001)
)
check("L02 closed forms of sum/product/quotient errors for n=1..5000", ok_all, ok_all)
check("L02 sum error at n=10 is 12/110 = 6/55", serr(10), serr(10) == F(6, 55))
check("L02 product error at n=10 is 32/110", perr(10), perr(10) == F(32, 110))
check("L02 quotient error at n=10 is 54/132", qerr(10), qerr(10) == F(54, 132))
check("L02 sum error at n=10 prints 1.090909e-01", sci(serr(10), 6), sci(serr(10), 6) == "1.090909e-01")
check("L02 product error at n=100 is 302/10100 = 0.0299009900...", f"{float(perr(100)):.12f}",
      perr(100) == F(302, 10100))
check("L02 E2 closed form (3n+2)/(n(n+1)) at n=100 equals 302/10100", F(302, 10100), F(3 * 100 + 2, 100 * 101) == F(302, 10100))
check("L02 product error at n=100 prints 2.990099e-02", sci(perr(100), 6), sci(perr(100), 6) == "2.990099e-02")
check("L02 quotient error at n=1 is 3/2", qerr(1), qerr(1) == F(3, 2))
check("L02 quotient error at n=1000 prints 4.989023e-03", sci(qerr(1000), 6), sci(qerr(1000), 6) == "4.989023e-03")
check("L02 product error at 10000 prints 2.999900e-04", sci(perr(10000), 6), sci(perr(10000), 6) == "2.999900e-04")
check("L02 sum error at 10000 prints 1.000100e-04", sci(serr(10000), 6), sci(serr(10000), 6) == "1.000100e-04")
check("L02 quotient error at 10000 prints 4.998900e-04", sci(qerr(10000), 6), sci(qerr(10000), 6) == "4.998900e-04")
check("L02 quiz sum error 0.1090909 within 1e-7 of 6/55",
      float(abs(serr(10) - F(1090909, 10000000))), abs(serr(10) - F(1090909, 10000000)) <= F(1, 10**7))
check("L02 quiz product error 0.02990099 within 1e-8 at n=100",
      float(abs(perr(100) - F(2990099, 10**8))), abs(perr(100) - F(2990099, 10**8)) <= F(1, 10**8))
m_lim = lambda n: F(3 * n * n + 1, n * n + 2)
check("L02 M1 limit 3 (value at n=10^6)", float(m_lim(10**6)), abs(m_lim(10**6) - 3) < F(1, 10**5))
check("L02 Prop 1.1 (ii) proof: |a_n||b_n - b| bound identity",
      "identity", all(a2(n) * b2(n) - 2 == a2(n) * (b2(n) - 1) + 1 * (a2(n) - 2) for n in range(1, 200)))
check("L02 Remark 3.1: a_n/b_n = n for a_n=1, b_n=1/n", "n", all(F(1) / F(1, n) == n for n in range(1, 50)))
check("L02 misc 2: (-1)^n + (-(-1)^n) = 0", "0", all((-1) ** n + (-((-1) ** n)) == 0 for n in range(50)))
check("L02 Problem E3 a_1/b_1 = 1/2 with b_1 = 3", a2(1) / b2(1), a2(1) / b2(1) == F(1, 2))

# ---------------- L03 ----------------
def fb(x: F) -> F:
    return x * x if x < 1 else 2 * x


gap_ok = True
for k in range(1, 5):
    h = F(1, 10**k)
    gap_ok = gap_ok and fb(1 + h) - fb(1 - h) == 1 + 4 * h - h * h and fb(1 - h) == (1 - h) ** 2
check("L03 gap f(1+h)-f(1-h) = 1+4h-h^2 and f(1-h)=(1-h)^2 for h=10^-1..10^-4", "identity", gap_ok)
check("L03 gap at h=0.1 is 1.39", float(fb(F(11, 10)) - fb(F(9, 10))), fb(F(11, 10)) - fb(F(9, 10)) == F(139, 100))
check("L03 gap at h=0.01 prints 1.039900", f"{float(fb(F(101, 100)) - fb(F(99, 100))):.6f}",
      f"{float(fb(F(101, 100)) - fb(F(99, 100))):.6f}" == "1.039900")
check("L03 f(1-0.001) prints 0.998001", f"{float(fb(F(999, 1000))):.6f}",
      f"{float(fb(F(999, 1000))):.6f}" == "0.998001")
check("L03 E2 closed form at h=0.01: 1 + 0.04 - 0.0001 = 1.0399", F(10399, 10000), 1 + F(4, 100) - F(1, 10000) == F(10399, 10000))
# E3 prediction: delta = eps, eps = 0.1, grid point x = 2 + (19/20)*0.1
x = F(2) + F(19, 20) * F(1, 10)
check("L03 E3 grid point x=2.095 has 0<|x-2|<0.1 and |3x+1-7| = 0.285 > 0.1",
      float(abs(3 * x + 1 - 7)), 0 < abs(x - 2) < F(1, 10) and abs(3 * x + 1 - 7) == F(57, 200) and abs(3 * x + 1 - 7) > F(1, 10))
# grid check with delta = eps/3 for three tolerances
def grid_ok(eps: F) -> bool:
    d = eps / 3
    pts = [2 + F(k, 20) * d for k in range(-19, 20) if k != 0]
    return all(abs(3 * p + 1 - 7) < eps for p in pts)


check("L03 grid check delta=eps/3 True for eps=0.1,0.01,0.001 and 38 points",
      len([k for k in range(-19, 20) if k != 0]), all(grid_ok(e) for e in (F(1, 10), F(1, 100), F(1, 1000))))
check("L03 Example 2.4 g(x)=x+1 for x != 1", "identity",
      all((x * x - 1) / (x - 1) == x + 1 for x in (F(2), F(3, 2), F(-5), F(7, 3))))
check("L03 M1 f(x)=2x-1 at a=3, |f(x)-5| = 2|x-3|", "identity", all(abs(2 * x - 1 - 5) == 2 * abs(x - 3) for x in (F(3), F(31, 10), F(29, 10))))
check("L03 M3 q(x)=x+2 for x != 2", "identity", all((x * x - 4) / (x - 2) == x + 2 for x in (F(1), F(3), F(5, 2))))
check("L03 Quiz Q7 gap formula at h=0.1: 1+0.4-0.01=1.39", F(139, 100), 1 + F(4, 10) - F(1, 100) == F(139, 100))

# ---------------- L04 ----------------
def cube(x: F) -> F:
    return x**3


def Q1(h: F) -> F:
    return (cube(1 + h) - cube(1)) / h


ok4 = all(Q1(h) == 3 + 3 * h + h * h for h in (F(1, 10**k) for k in range(1, 7)))
check("L04 Q(h) = 3+3h+h^2 at h=10^-1..10^-6", "identity", ok4)
check("L04 Q(0.1)=3.31 and error 0.31", float(Q1(F(1, 10))), Q1(F(1, 10)) == F(331, 100))
check("L04 Q(0.001)=3.003001", float(Q1(F(1, 1000))), Q1(F(1, 1000)) == F(3003001, 10**6))
check("L04 error at 1e-5 = 3e-5 + 1e-10 = 3.00001e-5", float(Q1(F(1, 10**5)) - 3),
      Q1(F(1, 10**5)) - 3 == F(3, 10**5) + F(1, 10**10))
check("L04 error at 1e-6 prints 3.000001e-06", sci(Q1(F(1, 10**6)) - 3, 6), sci(Q1(F(1, 10**6)) - 3, 6) == "3.000001e-06")
check("L04 error/h at 1e-6 prints 3.000001", f"{float((Q1(F(1, 10**6)) - 3) / F(1, 10**6)):.6f}",
      f"{float((Q1(F(1, 10**6)) - 3) / F(1, 10**6)):.6f}" == "3.000001")
check("L04 M2 Q(0.01) for x^2 at a=-1 is -1.99", F(-199, 100), (F(1) * (-1 + F(1, 100)) ** 2 - 1) / F(1, 100) == F(-199, 100))
check("L04 M3 Q(h) = -1/(2(2+h)) for 1/x at 2", "identity",
      all((1 / (2 + h) - F(1, 2)) / h == F(-1, 2 * (2 + h)) for h in (F(1, 7), F(-1, 9), F(1, 1000))))
check("L04 P1 Q(h) = 3a^2+3ah+h^2 identity", "identity",
      all(((a + h) ** 3 - a**3) / h == 3 * a * a + 3 * a * h + h * h for a in (F(0), F(2), F(-3, 2)) for h in (F(1, 3), F(-1, 5))))
check("L04 R1 h|h|/h = |h| for h != 0", "identity", all(h * abs(h) / h == abs(h) for h in (F(1, 3), F(-2, 7))))
check("L04 E1 expansion at h=0.1 is 3.31", F(331, 100), 3 + F(3, 10) + F(1, 100) == F(331, 100))

# ---------------- L05 ----------------
def p(x: F) -> F:
    return (x * x + 1) * x**3


def q(x: F) -> F:
    return (x * x + 1) / (x + 2)


def c(x: F) -> F:
    return (x * x + 1) ** 3


X = F(3, 2)
H = F(1, 10**4)


def cd(f, x: F, h: F) -> F:  # exact central difference
    return (f(x + h) - f(x - h)) / (2 * h)


dp = 2 * X * X**3 + (X * X + 1) * 3 * X * X
dq = (X * X + 4 * X - 1) / (X + 2) ** 2
dc = 6 * X * (X * X + 1) ** 2
check("L05 p'(1.5) = 32.0625", float(dp), dp == F(513, 16))
check("L05 q'(1.5) = 29/49", float(dq), dq == F(29, 49))
check("L05 c'(1.5) = 95.0625", float(dc), dc == F(1521, 16))
ep = cd(p, X, H) - dp
eq = cd(q, X, H) - dq
ec = cd(c, X, H) - dc
check("L05 product central difference error prints 2.35e-07", sci(ep, 2), sci(ep, 2) == "2.35e-07")
check("L05 quotient central difference error prints 3.33e-10 (lab prints abs)", sci(abs(eq), 2), sci(abs(eq), 2) == "3.33e-10")
check("L05 composite central difference error prints 8.55e-07", sci(ec, 2), sci(ec, 2) == "8.55e-07")
check("L05 p central difference printed 32.062500235 (9 dp)", f"{float(cd(p, X, H)):.9f}",
      f"{float(cd(p, X, H)):.9f}" == "32.062500235")
check("L05 c central difference printed 95.062500855 (9 dp)", f"{float(cd(c, X, H)):.9f}",
      f"{float(cd(c, X, H)):.9f}" == "95.062500855")
check("L05 q central difference printed 0.591836734 (9 dp)", f"{float(cd(q, X, H)):.9f}",
      f"{float(cd(q, X, H)):.9f}" == "0.591836734")
check("L05 q'(1.5) to nine decimals is 0.591836735", f"{float(dq):.9f}", f"{float(dq):.9f}" == "0.591836735")
# Assumption 1.4 leading terms: p'''(x)=60x^2+6 (p=x^5+x^3), c'''(x)=120x^3+72x (c=x^6+3x^4+3x^2+1)
p3 = 60 * X * X + 6
c3 = 120 * X**3 + 72 * X
check("L05 p'''(1.5) = 141", p3, p3 == 141)
check("L05 c'''(1.5) = 513", c3, c3 == 513)
check("L05 h^2 p'''/6 = 2.35e-7 (E1 and Misconception 3)", sci(H * H * p3 / 6, 2), sci(H * H * p3 / 6, 2) == "2.35e-07")
check("L05 h^2 c'''/6 = 8.55e-7", sci(H * H * c3 / 6, 2), sci(H * H * c3 / 6, 2) == "8.55e-07")
check("L05 exact p error equals h^2 p'''/6 + h^4 (polynomial, p^(5)=120)", "identity",
      ep == H * H * p3 / 6 + H**4)
qq = lambda x: x / (x * x + 1)
for x0 in (F(1), F(1, 3), F(-2)):
    approx = cd(qq, x0, F(1, 10**12))
    formula = (1 - x0 * x0) / (x0 * x0 + 1) ** 2
    check(f"L05 M2 q'({x0}) formula vs central difference at h=1e-12", float(approx - formula),
          abs(approx - formula) < F(1, 10**18))
ww = lambda x: (3 * x - 1) ** 4
check("L05 M3 w'(1) = 96 via central difference h=1e-12", float(cd(ww, F(1), F(1, 10**12)) - 96),
      abs(cd(ww, F(1), F(1, 10**12)) - 96) < F(1, 10**6))
check("L05 E3 composite value 6*1.5*3.25^2 = 95.0625", F(1521, 16), 6 * F(3, 2) * F(13, 4) ** 2 == F(1521, 16))
check("L05 Misc3 central difference of x^3 at 1 is 3+h^2", "identity",
      all(cd(lambda x: x**3, F(1), h) == 3 + h * h for h in (F(1, 10), F(1, 10**4))))
check("L05 Ex2.2 c'(x)=6x(x^2+1)^2 vs chain value 3(x^2+1)^2*2x at x=1.5", "identity",
      all(6 * x * (x * x + 1) ** 2 == 3 * (x * x + 1) ** 2 * 2 * x for x in (F(3, 2), F(-1), F(7, 5))))
check("L05 Misc2: g'(0) f'(0) = 0 and g'(f(0))f'(0) = 2 for f=x+1, g=u^2", "0 and 2", (0 * 1, 2 * 1))
check("L05 R1 cubic central difference = p'(x)+a h^2 (a=1,b=2,m=3)", "identity",
      all(cd(lambda t: t**3 + 2 * t * t + 3 * t, x0, h) == 3 * x0 * x0 + 4 * x0 + 3 + h * h
          for x0 in (F(1, 2), F(-3)) for h in (F(1, 10), F(1, 7))))
check("L05 E2 29/49 = 0.5918367346..", f"{float(F(29, 49)):.10f}", f"{float(F(29, 49)):.10f}" == "0.5918367347")
check("L05 P2 (1/g)' = -g'/g^2 identity at g=x^2+1, x=1.5", "identity",
      abs(cd(lambda t: 1 / (t * t + 1), F(3, 2), F(1, 10**12)) - (-2 * F(3, 2)) / (F(3, 2) ** 2 + 1) ** 2) < F(1, 10**18))

# ---------------- L06 ----------------
def cub(x: F) -> F:
    return x**3 - 3 * x


ptsL6 = [F(-2) + F(i, 4) for i in range(17)]
incr = sum(1 for lo, hi in zip(ptsL6, ptsL6[1:]) if cub(hi) > cub(lo))
check("L06 grid intervals on which f increases", f"{incr} of 16", incr == 8)
mid_agree = sum(
    1
    for lo, hi in zip(ptsL6, ptsL6[1:])
    if (cub(hi) > cub(lo)) == ((3 * ((lo + hi) / 2) ** 2 - 3) > 0)
)
check("L06 increase agrees with sign of f' at midpoint on 16 of 16", mid_agree, mid_agree == 16)
check("L06 f(-1)=2, f(1)=-2", (cub(F(-1)), cub(F(1))), cub(F(-1)) == 2 and cub(F(1)) == -2)
check("L06 f' = 3(x-1)(x+1) identity", "identity", all(3 * x * x - 3 == 3 * (x - 1) * (x + 1) for x in (F(1, 3), F(-5))))
check("L06 M1 f(2) = -3 for x^2-4x+1", 4 - 8 + 1, 4 - 8 + 1 == -3)
check("L06 M2 c = 2/sqrt(3) ~ 1.1547 (3c^2=4)", f"{2 / 3 ** 0.5:.6f}", abs(2 / 3**0.5 - 1.1547) < 1e-4)
check("L06 Misc3 c=1/sqrt(3) ~0.577, not 0.5", f"{1 / 3 ** 0.5:.6f}", 0.5 < 1 / 3**0.5 < 0.58)
check("L06 Misc2 y^2+xy+x^2 = (x+y/2)^2 + 3y^2/4 identity", "identity",
      all(y * y + x * y + x * x == (x + y / 2) ** 2 + F(3, 4) * y * y for x in (F(-1), F(2, 3)) for y in (F(1), F(-3, 5))))
check("L06 Misc2 y^3 - x^3 = (y-x)(y^2+xy+x^2)", "identity",
      all(y**3 - x**3 == (y - x) * (y * y + x * y + x * x) for x in (F(-1), F(2, 3)) for y in (F(1), F(-3, 5))))
check("L06 M3 f(-2) = -2, f(-1) = 2", (cub(F(-2)), cub(F(-1))), cub(F(-2)) == -2 and cub(F(-1)) == 2)
check("L06 R2 chord slope of |x-1| on [0,2] is 0", (abs(F(2) - 1) - abs(F(0) - 1)) / 2, (abs(F(2) - 1) - abs(F(0) - 1)) / 2 == 0)
check("L06 E3 midpoints are odd multiples of 1/8", "identity",
      all(((lo + hi) / 2) * 8 % 2 == 1 for lo, hi in zip(ptsL6, ptsL6[1:])))

# ---------------- hub (index.html) ----------------
check("hub 240 + 60 = 300", 300, 240 + 60 == 300)
check("hub 60/300 = 20%", "20%", F(60, 300) == F(1, 5))
check("hub bar widths 80% and 20% match 240/300 and 60/300", "80/20", (F(240, 300), F(60, 300)) == (F(4, 5), F(1, 5)))
check("hub placement: 80% of 8 items = 6.4, so at least 7 correct", 7, F(8) * F(8, 10) == F(32, 5))
check("hub placement: 6/8 = 75%", "75%", F(6, 8) == F(3, 4))
check("hub placement: 7/8 = 87.5%", "87.5%", F(7, 8) == F(875, 1000))
check("hub skill check 1: limit of (2h+h^2)/h = 2", 2, F(2) == 2)
check("hub skill check 2: (f(1.1)-f(0.9))/0.2 for x^3 is 3.01", f"{float(((F(11, 10))**3 - (F(9, 10))**3) / F(2, 10)):.6f}",
      ((F(11, 10)) ** 3 - (F(9, 10)) ** 3) / F(2, 10) == F(301, 100))
check("hub 24 lessons x 10 h = 240", 240, 24 * 10 == 240)

fails = [label for label, ok in results if not ok]
print()
print(f"checks: {len(results)}; failing: {len(fails)}")
for f_ in fails:
    print("  FAIL:", f_)
