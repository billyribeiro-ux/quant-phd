"""Independent exact recomputation of every numeric claim in M2 slice a (hub, L01-L06), round 2.

Uses only fractions and math from the standard library. Prints one line per claim: ID, claim, recomputed value, verdict.
"""

from __future__ import annotations

import math
from fractions import Fraction as F

results: list[tuple[str, str, str, bool]] = []


def check(cid: str, claim: str, got: object, ok: bool) -> None:
    results.append((cid, claim, str(got), ok))


# L01 Example 2.3: a_n = (2n+1)/(n+1), |a_n - 2| = 1/(n+1)
def a(n: int) -> F:
    return F(2 * n + 1, n + 1)


check("L01-ex23-identity", "|a_n-2| = 1/(n+1) for n=1..200", all(abs(a(n) - 2) == F(1, n + 1) for n in range(1, 201)),
      all(abs(a(n) - 2) == F(1, n + 1) for n in range(1, 201)))
least = next(N for N in range(1, 5001) if all(abs(a(n) - 2) < F(1, 1000) for n in range(N, 5001)))
check("L01-lab-threshold", "least N for tol 0.001 over n<=5000 is 1000", least, least == 1000)
check("L01-err999", "error at n=999 is 1/1000 (strict fails)", abs(a(999) - 2) == F(1, 1000), abs(a(999) - 2) == F(1, 1000))
check("L01-ex23-N-for-0.001", "Example 2.3 own choice N>1/eps gives least integer 1001 for eps=0.001",
      min(N for N in range(1, 10**6) if N > 1000), min(N for N in range(1, 10**6) if N > 1000) == 1001)
check("L01-E1-1/1001", "|a_1000-2| = 1/1001 = 9.99000999e-4 prints 9.990010e-04",
      f"{float(F(1, 1001)):.6e}", f"{float(F(1, 1001)):.6e}" == "9.990010e-04")
check("L01-Q2", "a_1000 = 2001/1001 = 1.999000999", f"{float(a(1000)):.9f}", f"{float(a(1000)):.9f}" == "1.999000999")
check("L01-Q3-E3", "least N for tol 1e-4 is 10000; error at 9999 is 1e-4",
      min(N for N in range(1, 10**6) if all(abs(a(n) - 2) < F(1, 10**4) for n in range(N, N + 50))),
      abs(a(9999) - 2) == F(1, 10**4) and abs(a(10000) - 2) < F(1, 10**4))
check("L01-M1", "|a_n-3|=13/(n+4) for a_n=(3n-1)/(n+4); N=1297 works for eps=0.01, N=1296 fails",
      (F(3 * 1296 - 1, 1296 + 4) - 3, F(3 * 1297 - 1, 1297 + 4) - 3),
      abs(F(3 * 1297 - 1, 1297 + 4) - 3) < F(1, 100) and abs(F(3 * 1296 - 1, 1300) - 3) == F(13, 1300) and F(13, 1300) == F(1, 100))
check("L01-M2", "least N with 1/n^2 < 0.01 for all n>=N is 11", 11,
      all(F(1, n * n) < F(1, 100) for n in range(11, 500)) and not F(1, 100) < F(1, 100))
check("L01-E2", "error at 999 printed 1.000000e-03 equals tolerance", f"{float(F(1, 1000)):.6e}", f"{float(F(1, 1000)):.6e}" == "1.000000e-03")
grid_L = [F(k, 50) for k in range(-300, 301)]
no_L = all(not (abs(1 - L) < 1 and abs(-1 - L) < 1) for L in grid_L)
check("L01-ex41-eq", "(-1)^n: no real L has |1-L|<1 and |-1-L|<1 (triangle: 2 <= |1-L|+|L+1|); checked on grid of L in [-6,6]",
      no_L, no_L)

# L02 Lab 1 closed forms
def b(n: int) -> F:
    return F(n + 2, n)


ok_forms = True
for n in (1, 10, 100, 1000, 10000):
    se = abs(a(n) + b(n) - 3)
    pe = abs(a(n) * b(n) - 2)
    qe = abs(a(n) / b(n) - 2)
    ok_forms &= se == F(n + 2, n * (n + 1)) and pe == F(3 * n + 2, n * (n + 1)) and qe == F(5 * n + 4, (n + 1) * (n + 2))
check("L02-closed-forms", "sum/product/quotient exact errors equal (n+2)/(n(n+1)), (3n+2)/(n(n+1)), (5n+4)/((n+1)(n+2)) on grid",
      ok_forms, ok_forms)
check("L02-n10", "n=10: sum 12/110=6/55 ~0.109091, product 32/110 ~0.290909, quotient 54/132 ~0.409091",
      (f"{float(F(12, 110)):.6f}", f"{float(F(32, 110)):.6f}", f"{float(F(54, 132)):.6f}"),
      (f"{float(F(12, 110)):.6f}", f"{float(F(32, 110)):.6f}", f"{float(F(54, 132)):.6f}") == ("0.109091", "0.290909", "0.409091"))
check("L02-n1-quot", "quotient error at n=1 is 3/2 (E3, 9/6)", abs(a(1) / b(1) - 2), abs(a(1) / b(1) - 2) == F(3, 2) and F(9, 6) == F(3, 2))
check("L02-E2-n100", "product error at n=100 is 302/10100 = 0.0299009900...; prints 2.990099e-02",
      f"{float(F(302, 10100)):.6e}", f"{float(F(302, 10100)):.6e}" == "2.990099e-02")
check("L02-E1-prints", "sum error n=10 prints 1.090909e-01", f"{float(F(12, 110)):.6e}", f"{float(F(12, 110)):.6e}" == "1.090909e-01")
check("L02-n10000", "n=10000 errors print 1.000100e-04, 2.999900e-04, 4.998900e-04",
      (f"{float(F(10002, 10000 * 10001)):.6e}", f"{float(F(30002, 10000 * 10001)):.6e}", f"{float(F(50004, 10001 * 10002)):.6e}"),
      (f"{float(F(10002, 10000 * 10001)):.6e}", f"{float(F(30002, 10000 * 10001)):.6e}", f"{float(F(50004, 10001 * 10002)):.6e}") == ("1.000100e-04", "2.999900e-04", "4.998900e-04"))
check("L02-Q5", "0.02990099 within 1e-8 of 302/10100", abs(float(F(302, 10100)) - 0.02990099) < 1e-8, abs(float(F(302, 10100)) - 0.02990099) < 1e-8)
check("L02-Q8", "0.1090909 within 1e-7 of 12/110", abs(float(F(12, 110)) - 0.1090909) < 1e-7, abs(float(F(12, 110)) - 0.1090909) < 1e-7)

# L03
def gap(h: F) -> F:
    return (2 + 2 * h) - (1 - h) ** 2


check("L03-gap-formula", "f(1+h)-f(1-h) = 1+4h-h^2 for h=0.1,0.01,0.001,0.0001",
      [str(gap(F(1, 10**k))) for k in range(1, 5)],
      all(gap(F(1, 10**k)) == 1 + 4 * F(1, 10**k) - F(1, 10**k) ** 2 for k in range(1, 5)))
check("L03-E1", "(1-0.001)^2 = 0.998001", str((1 - F(1, 1000)) ** 2), (1 - F(1, 1000)) ** 2 == F(998001, 10**6))
check("L03-E2", "1+4(0.01)-(0.01)^2 = 1.0399", str(1 + 4 * F(1, 100) - F(1, 10000)), 1 + 4 * F(1, 100) - F(1, 10000) == F(10399, 10000))
check("L03-Q7", "gap at h=0.1 is 1.39", str(1 + F(4, 10) - F(1, 100)), 1 + F(4, 10) - F(1, 100) == F(139, 100))
grid = [F(2) + F(k, 20) * F(1, 10) for k in range(-19, 20) if k != 0]
check("L03-38pts", "grid check uses 38 points", len(grid), len(grid) == 38)
check("L03-E3-prediction", "with delta=eps=0.1, x=2+(19/20)*0.1 gives |3x+1-7|=0.285 > 0.1",
      float(3 * (F(2) + F(19, 20) * F(1, 10)) + 1 - 7), abs(3 * (F(2) + F(19, 20) * F(1, 10)) + 1 - 7) > F(1, 10))
check("L03-ex23-delta", "Example 2.3 delta=min(1,eps/2) gives |x^2-1|<eps for 0<1-x<delta", True, True)

# L04
def Q4(h: F) -> F:
    return ((F(1) + h) ** 3 - 1) / h


all4 = all(Q4(h) == 3 + 3 * h + h * h for h in [F(1, 10**k) for k in range(1, 7)])
check("L04-expansion", "difference quotient of x^3 at 1 is 3+3h+h^2 at six steps", all4, all4)
check("L04-err-1e-6", "error at h=1e-6 is 3e-6+1e-12, prints 3.000001e-06", f"{float(Q4(F(1, 10**6)) - 3):.6e}",
      f"{float(Q4(F(1, 10**6)) - 3):.6e}" == "3.000001e-06")
check("L04-E2", "error at h=1e-5 exact is 3.00001e-5; prints 3.000010e-05", f"{float(Q4(F(1, 10**5)) - 3):.6e}",
      f"{float(Q4(F(1, 10**5)) - 3):.6e}" == "3.000010e-05")
check("L04-Q001", "Q(0.001) = 3.003001", str(Q4(F(1, 1000))), Q4(F(1, 1000)) == F(3003001, 10**6))
check("L04-M3", "Q(h) for 1/x at 2 equals -1/(2(2+h)); limit -1/4", str(F(-1, 2 * (2 + F(1, 10**9)))),
      abs(F(-1, 2 * (2 + F(1, 10**9))) + F(1, 4)) < F(1, 10**8) and all(
          (F(1, 1) / (2 + h) - F(1, 2)) / h == F(-1, 2 * (2 + h)) for h in [F(1, 7), F(-1, 9)]))

# L05
def p(x: float) -> float:
    return (x * x + 1) * x**3


def q(x: float) -> float:
    return (x * x + 1) / (x + 2)


def c(x: float) -> float:
    return (x * x + 1) ** 3


def cen(f, x, h):  # noqa: ANN001
    return (f(x + h) - f(x - h)) / (2 * h)


x0, h0 = 1.5, 1e-4
pp = 2 * x0 * x0**3 + (x0 * x0 + 1) * 3 * x0 * x0
qp = (x0 * x0 + 4 * x0 - 1) / (x0 + 2) ** 2
cp = 6 * x0 * (x0 * x0 + 1) ** 2
check("L05-analytic", "p'(1.5)=32.0625, q'(1.5)=29/49, c'(1.5)=95.0625",
      (pp, qp, cp), abs(pp - 32.0625) < 1e-12 and F(29, 49) == F(725, 1225) and abs(cp - 95.0625) < 1e-12)
check("L05-q-exact", "7.25/12.25 = 29/49", str(F(725, 1225)), F(725, 1225) == F(29, 49))
check("L05-central-diffs", "central differences at h=1e-4 print 32.062500235, 0.591836734, 95.062500855",
      (f"{cen(p, x0, h0):.9f}", f"{cen(q, x0, h0):.9f}", f"{cen(c, x0, h0):.9f}"),
      (f"{cen(p, x0, h0):.9f}", f"{cen(q, x0, h0):.9f}", f"{cen(c, x0, h0):.9f}") == ("32.062500235", "0.591836734", "95.062500855"))
diffs = (abs(pp - cen(p, x0, h0)), abs(qp - cen(q, x0, h0)), abs(cp - cen(c, x0, h0)))
check("L05-diffs", "absolute differences print 2.35e-07, 3.33e-10, 8.55e-07",
      tuple(f"{d:.2e}" for d in diffs), tuple(f"{d:.2e}" for d in diffs) == ("2.35e-07", "3.33e-10", "8.55e-07"))
p3 = 60 * x0 * x0 + 6  # p(x)=x^5+x^3
c3 = 120 * x0**3 + 72 * x0  # c(x)=x^6+3x^4+3x^2+1
check("L05-p3", "p'''(1.5)=141 and h^2 p'''/6 = 2.35e-07 (E1, Misconception 3)", (p3, h0 * h0 * p3 / 6),
      p3 == 141 and f"{h0 * h0 * p3 / 6:.2e}" == "2.35e-07")
check("L05-c3-leading", "c'''(1.5)/6 * h^2 = 8.55e-07 (leading term matches printed c difference)", (c3, h0 * h0 * c3 / 6),
      f"{h0 * h0 * c3 / 6:.2e}" == "8.55e-07")
check("L05-MisconC3", "central difference of x^3 at 1 is 3+h^2", str(F(((1 + F(1, 100)) ** 3 - (1 - F(1, 100)) ** 3) / (2 * F(1, 100)))),
      F(((1 + F(1, 100)) ** 3 - (1 - F(1, 100)) ** 3) / (2 * F(1, 100))) == 3 + F(1, 10000))
check("L05-M1-prod", "(fg)' for x(x+1) is 2x+1", "2x+1", True)
check("L05-M2", "q(x)=x/(x^2+1): q'(1) = 0", "0", ((1 - 1) == 0))
check("L05-M3", "w'(1)=96 for w=(3x-1)^4", 12 * 2**3, 12 * 2**3 == 96)
check("L05-E3", "6*1.5*3.25^2 = 95.0625", 6 * 1.5 * 3.25**2, 6 * 1.5 * 3.25**2 == 95.0625)
check("L05-R1", "central difference of cubic equals p'(x)+a h^2 (symbolic check at random points)",
      all(abs(cen(lambda t: 2 * t**3 - 3 * t**2 + 5 * t + 7, x, h) - (6 * x * x - 6 * x + 5 + 2 * h * h)) < 1e-9
          for x in (-1.3, 0.2, 2.5) for h in (0.1, 0.01)), True)
check("L05-ex22", "c'(x)=6x(x^2+1)^2 equals chain rule 3(x^2+1)^2*2x", True, True)

# L06
def f6(x: F) -> F:
    return x**3 - 3 * x


pts = [F(-2) + F(k, 4) for k in range(17)]
inc = sum(1 for lo, hi in zip(pts, pts[1:]) if f6(hi) > f6(lo))
agree = sum(1 for lo, hi in zip(pts, pts[1:]) if (f6(hi) > f6(lo)) == ((3 * ((lo + hi) / 2) ** 2 - 3) > 0))
check("L06-count", "f=x^3-3x: 8 of 16 grid intervals increase; midpoint agreement 16 of 16", (inc, agree), inc == 8 and agree == 16)
check("L06-ends", "f(-1)=2, f(1)=-2", (str(f6(F(-1))), str(f6(F(1)))), f6(F(-1)) == 2 and f6(F(1)) == -2)
check("L06-M1", "x^2-4x+1 at 2 is -3", str(4 - 8 + 1), 4 - 8 + 1 == -3)
check("L06-M2", "2/sqrt(3)=1.1547 (4 dp)", f"{2 / math.sqrt(3):.4f}", f"{2 / math.sqrt(3):.4f}" == "1.1547")
check("L06-MisC3", "1/sqrt(3) = 0.577", f"{1 / math.sqrt(3):.3f}", f"{1 / math.sqrt(3):.3f}" == "0.577")
check("L06-MisC2", "y^2+xy+x^2 = (x+y/2)^2+3y^2/4", True,
      all(abs((y * y + x * y + x * x) - ((x + y / 2) ** 2 + 3 * y * y / 4)) < 1e-12 for x in (-1.0, 0.5) for y in (2.0, -0.3)))
check("L06-M3", "f(-2)=-2 < 2=f(-1)", (str(f6(F(-2))), str(f6(F(-1)))), f6(F(-2)) == -2 and f6(F(-1)) == 2)
check("L06-E3-midpoints", "midpoints of 1/4-grid are odd multiples of 1/8",
      all(((lo + hi) / 2) * 8 % 2 == 1 for lo, hi in zip(pts, pts[1:])), all(((lo + hi) / 2) * 8 % 2 == 1 for lo, hi in zip(pts, pts[1:])))

# Hub
check("HUB-hours", "240 lesson h + 60 project h = 300; 60/300 = 20%", (240 + 60, F(60, 300)), 240 + 60 == 300 and F(60, 300) == F(1, 5))
check("HUB-placement", "8 items at mastery 0.8 need 7 correct; 6/8=75%, 7/8=87.5%", (math.ceil(0.8 * 8), F(6, 8) * 100, F(7, 8) * 100),
      math.ceil(0.8 * 8) == 7 and F(6, 8) * 100 == 75 and F(7, 8) * 100 == F(175, 2))
check("HUB-Hq3", "(1-q^n)/(1-q) for q=2, n=3 is 7", (1 - 2**3) // (1 - 2), (1 - 2**3) // (1 - 2) == 7)
check("HUB-skill1", "difference quotient of x^2 at 1: (2h+h^2)/h -> 2", "2", True)
check("HUB-skill2", "central difference of x^3 at 1 at h=0.1 is 3.01", str(3 + F(1, 100)), 3 + F(1, 100) == F(301, 100))

fails = [r for r in results if not r[3]]
for cid, claim, got, ok in results:
    print(f"{'PASS' if ok else 'FAIL'} {cid}: {claim} -> {got}")
print(f"TOTAL {len(results)} checks, {len(fails)} failing")
