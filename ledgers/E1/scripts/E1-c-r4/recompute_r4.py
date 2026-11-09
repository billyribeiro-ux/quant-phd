"""Independent exact recomputation of every number on E1 pages L07, L08 and L09 (verifier round 4).

Written from the page prose and the verifier's own algebra; it does not import or call the lab twins or the pages.
Run: python -I ledgers/E1/scripts/E1-c-r4/recompute_r4.py
Prints one line per check, FAIL lines are counted at the end.
"""

from __future__ import annotations

import math
from fractions import Fraction as F

FAILS: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "ok  " if ok else "FAIL"
    print(f"{status} {name} {detail}")
    if not ok:
        FAILS.append(name)


def half_up(x: F) -> int:
    return math.floor(x + F(1, 2))


# ---------------------------------------------------------------- L07
def l07() -> None:
    # Theorem 1.2 / Lemma 1.4 / Theorem 1.5 over an exact grid of (a, b, c) and Q in [0, a].
    n = 0
    bad = 0
    for b in range(1, 7):
        for c in range(1, 12):
            for a in range(b * c + 1, b * c + 60):
                d = F(a - b * c)
                P = lambda x: (F(a) - x) / b  # noqa: E731
                for Q in (d / 2, F(2, 3) * d, d, F(a, 3), F(a, 7), F(a)):
                    if not (0 <= Q <= a):
                        continue
                    n += 1
                    cs = Q * Q / (2 * b)
                    ps = (P(Q) - c) * Q
                    w = cs + ps
                    integral_margin = (F(a) * Q - Q * Q / 2) / b - c * Q
                    dwl = (d * d - 0) / (2 * b) - w  # W(d) - W(Q), with W(d) = d^2/(2b)
                    ok = (
                        cs == Q * Q / (2 * b)
                        and ps == (d - Q) * Q / b
                        and w == (2 * d * Q - Q * Q) / (2 * b)
                        and w == integral_margin
                        and dwl == (d - Q) ** 2 / (2 * b)
                    )
                    if not ok:
                        bad += 1
    check("L07 Theorem 1.2 and Theorem 1.5 identities", bad == 0, f"over {n} (a,b,c,Q) points, failures={bad}")

    # Corollary 2.1 and Proposition 2.3 in units of d^2/b, for many (a, b, c).
    rows_bad = 0
    for b in range(1, 6):
        for c in range(1, 9):
            for a in range(b * c + 1, b * c + 40):
                d = F(a - b * c)
                structs = {
                    "M": (d / 2, F(a + b * c, 2 * b)),
                    "C": (F(2, 3) * d, F(a + 2 * b * c, 3 * b)),
                    "B": (d, F(c)),
                }
                out = {}
                for k, (Q, fee) in structs.items():
                    assert fee == F(a) / b - Q / b, (k, a, b, c)  # fee lies on the inverse demand
                    cs = Q * Q / (2 * b)
                    ps = (fee - c) * Q
                    w = cs + ps
                    dwl = d * d / (2 * b) - w
                    out[k] = (cs, ps, w, dwl)
                cs_m, ps_m, w_m, dwl_m = out["M"]
                cs_c, ps_c, w_c, dwl_c = out["C"]
                cs_b, ps_b, w_b, dwl_b = out["B"]
                ok = (
                    (dwl_m, dwl_c, dwl_b) == (d * d / (8 * b), d * d / (18 * b), F(0))
                    and (cs_m, ps_m, w_m) == (d * d / (8 * b), d * d / (4 * b), 3 * d * d / (8 * b))
                    and (cs_c, ps_c, w_c) == (2 * d * d / (9 * b), 2 * d * d / (9 * b), 4 * d * d / (9 * b))
                    and (cs_b, ps_b, w_b) == (d * d / (2 * b), F(0), d * d / (2 * b))
                    and 0 < dwl_c < dwl_m
                    and cs_m < cs_c < cs_b
                    and ps_m > ps_c > ps_b == 0
                    and w_m < w_c < w_b
                    and dwl_m / w_b == F(1, 4)
                    and dwl_c / w_b == F(1, 9)
                    and dwl_m / dwl_c == F(9, 4)
                    and (fee_c_check(a, b, c))
                )
                if not ok:
                    rows_bad += 1
    check("L07 Corollary 2.1 and Proposition 2.3 orderings and shares", rows_bad == 0, f"failures={rows_bad}")

    # Example 2.2 and the lab reference case (120, 1, 20).
    a, b, c = 120, 1, 20
    d = F(a - b * c)
    check("L07 Example 2.2 d and d^2/(2b)", d == 100 and d * d / (2 * b) == 5000)
    check("L07 Example 2.2 monopoly values", (d / 2) ** 2 / (2 * b) == 1250 and (d / 2) * (d / 2) / b == 2500)
    cn = F(200, 3)
    check(
        "L07 Example 2.2 Cournot values",
        cn * cn / (2 * b) == F(20000, 9) and (d - cn) * cn / b == F(20000, 9) and F(40000, 9) == F(20000, 9) * 2,
    )
    check("L07 Example 2.2 Cournot DWL 5000/9 and rounding", (d - cn) ** 2 / (2 * b) == F(5000, 9)
          and half_up(F(5000, 9)) == 556 and half_up(F(20000, 9)) == 2222 and half_up(F(40000, 9)) == 4444)

    # Lab 1 Part A and B, Part C: cases (120,1,20), (90,3,10), (200,4,5).
    cases = [(120, 1, 20), (90, 3, 10), (200, 4, 5)]
    for a, b, c in cases:
        d = F(a - b * c)
        for name, Q, fee in (("M", d / 2, F(a + b * c, 2 * b)), ("C", F(2, 3) * d, F(a + 2 * b * c, 3 * b)),
                             ("B", d, F(c))):
            dwl = (d * d / (2 * b)) - (Q * Q / (2 * b) + (fee - c) * Q)
            print(f"      case {(a, b, c)} {name}: volume={Q} fee={fee} DWL={dwl} profit={(fee - c) * Q}")

    # Lab twin's expected-output numbers for the three cases (printed values, compared exactly).
    expect = {
        (120, 1, 20): {"M_loss": F(1250), "C_loss": F(5000, 9), "M_profit": F(2500), "C_profit": F(20000, 9)},
        (90, 3, 10): {"M_loss": F(150), "C_loss": F(200, 3), "M_profit": F(300), "C_profit": F(800, 3)},
        (200, 4, 5): {"M_loss": F(2025, 2), "C_loss": F(450), "M_profit": F(2025), "C_profit": F(1800)},
    }
    for (a, b, c), e in expect.items():
        d = F(a - b * c)
        m_fee = F(a + b * c, 2 * b)
        c_fee = F(a + 2 * b * c, 3 * b)
        m_loss = d * d / (8 * b)
        c_loss = d * d / (18 * b)
        m_profit = (m_fee - c) * (d / 2)
        c_profit = (c_fee - c) * (F(2, 3) * d)
        check(
            f"L07 lab expected losses and profits for {(a, b, c)}",
            (m_loss, c_loss, m_profit, c_profit) == (e["M_loss"], e["C_loss"], e["M_profit"], e["C_profit"]),
            f"loss M={m_loss} C={c_loss} profit M={m_profit} C={c_profit}",
        )
        check(f"L07 loss shares 1/4 and 1/9 for {(a, b, c)}", m_loss / (d * d / (2 * b)) == F(1, 4)
              and c_loss / (d * d / (2 * b)) == F(1, 9))

    # Problem set numbers.
    check("L07 M1 (90,3,10) monopoly", F(90 + 30, 6) == 20 and F(30 * 30, 3) == 300 and F(3600, 6) - 450 == 150)
    check("L07 M2 Cournot loss 200/3 rounds to 67", F(400, 6) == F(200, 3) and half_up(F(200, 3)) == 67)
    check("L07 M3 midpoint two steps", sum((120 - x) * 25 for x in (F(25, 2), F(75, 2))) == 4750
          and 120 * 50 - F(50 * 50, 2) == 4750)
    rr = 1 - math.sqrt(2) / 4
    check("L07 R1 Q = d(1 - sqrt2/4) between d/2 and 2d/3", 0.5 < rr < 2 / 3, f"Q/d={rr:.5f}")
    check("L07 R1 Cournot loss is 4/9 of monopoly", F(1, 18) / F(1, 8) == F(4, 9))
    # R2: fee cap at c: profit (f-c)*max(0,a-bf) <= 0 for f <= c
    a, b, c = 120, 1, 20
    worst = max((f - c) * max(0, a - b * f) for f in [F(k, 4) for k in range(0, 4 * c + 1)])
    check("L07 R2 profit under cap is <= 0 with max 0 at f=c", worst == 0)
    # R3: lambda threshold 2/7, units d^2/b
    diff = lambda lam: (F(2, 9) * lam + F(2, 9)) - (lam * F(1, 8) + F(1, 4))  # noqa: E731
    check("L07 R3 difference (7 lam - 2)/72", all(diff(F(k, 10)) == F(7 * F(k, 10) - 2, 72) for k in range(0, 40)))
    check("L07 R3 zero at lambda = 2/7", diff(F(2, 7)) == 0)
    # Proposition 2.3 accounting: CS rise 7/72, PS fall 2/72, W rise 5/72 (units d^2/b)
    check("L07 accounting 7/72, -2/72, 5/72", F(2, 9) - F(1, 8) == F(7, 72) and F(1, 4) - F(2, 9) == F(2, 72)
          and F(4, 9) - F(3, 8) == F(5, 72))
    # Quiz values
    check("L07 quiz q2 DWL monopoly 1250", (100 - 50) ** 2 / 2 == 1250)
    check("L07 quiz q9 integral 4750", 120 * 50 - F(2500, 2) == 4750)
    # Misconception 1: monopoly profit 2500 vs loss 1250
    check("L07 misconception 1 numbers", F(2500) != F(1250))
    # Lab docstring claim: the midpoint rule is exact for linear integrands for n = 1, 2, 10, 97
    ok = True
    for a, b, c in cases:
        d = F(a - b * c)
        for Q in (d / 2, F(2, 3) * d, d):
            exact = (F(a) * Q - Q * Q / 2) / b
            for n in (1, 2, 10, 97):
                h = Q / n
                s = sum(((F(a) - (i + F(1, 2)) * h) / b) * h for i in range(n))
                ok = ok and s == exact
    check("L07 midpoint rule exact for n=1,2,10,97 on lab cases", ok)


def fee_c_check(a: int, b: int, c: int) -> bool:
    """Cournot fee lies on inverse demand at volume 2d/3 (checked on the fly)."""
    d = F(a - b * c)
    Q = F(2, 3) * d
    return F(a + 2 * b * c, 3 * b) == (F(a) - Q) / b


# ---------------------------------------------------------------- L08
X, Y = 8, 4


def uA(x: F, y: F) -> F:
    return x * y


def uB(x: F, y: F) -> F:
    return (X - x) * (Y - y)


def grid_pts() -> list[tuple[int, int]]:
    return [(x, y) for x in range(X + 1) for y in range(Y + 1)]


def dominates(z: tuple[F, F], w: tuple[F, F]) -> bool:
    za, zb = uA(*z), uB(*z)
    wa, wb = uA(*w), uB(*w)
    return za >= wa and zb >= wb and (za > wa or zb > wb)


def l08() -> None:
    pts = grid_pts()
    eff = []
    for p in pts:
        w = (F(p[0]), F(p[1]))
        if not any(dominates((F(x), F(y)), w) for x, y in pts):
            eff.append(p)
    check("L08 grid-efficient count 15", len(eff) == 15, f"count={len(eff)}")
    interior = [p for p in eff if 0 < p[0] < X and 0 < p[1] < Y]
    boundary = [p for p in eff if p not in interior]
    check("L08 interior count 13 and boundary (0,0),(8,4)", len(interior) == 13 and sorted(boundary) == [(0, 0), (8, 4)])
    diag = [p for p in interior if p[1] * X == p[0] * Y]
    off = [p for p in interior if p[1] * X != p[0] * Y]
    check("L08 diagonal interior grid-efficient = (2,1),(4,2),(6,3)", diag == [(2, 1), (4, 2), (6, 3)])
    check("L08 off-diagonal count 10", len(off) == 10)
    # Diagonal grid points on the lattice: y*X == x*Y
    dpts = [p for p in pts if p[1] * X == p[0] * Y]
    check("L08 grid diagonal points are (0,0),(2,1),(4,2),(6,3),(8,4)", dpts == [(0, 0), (2, 1), (4, 2), (6, 3), (8, 4)])
    # Interior grid points count
    check("L08 interior grid points 21 = 7 x 3", sum(1 for x, y in pts if 0 < x < X and 0 < y < Y) == 21)
    check("L08 E2 share 13/21 = 0.619", round(13 / 21, 3) == 0.619 and round(100 * 13 / 21, 1) == 61.9)

    # Independent improvement check for each of the 10 off-diagonal interior grid-efficient points:
    # use a different method from the twin: take a trade on a fine rational grid of sizes 1/k and search
    # for an exact rational allocation (denominators up to 60) that strictly raises both utilities.
    for x, y in off:
        found = None
        base_a, base_b = uA(F(x), F(y)), uB(F(x), F(y))
        for den in range(2, 61):
            for nx in range(0, X * den + 1):
                xa = F(nx, den)
                if not (0 <= xa <= X):
                    continue
                for ny in range(0, Y * den + 1):
                    ya = F(ny, den)
                    if uA(xa, ya) > base_a and uB(xa, ya) > base_b:
                        found = (xa, ya)
                        break
                if found:
                    break
            if found:
                break
        check(f"L08 off-diagonal ({x},{y}) has a strict rational improvement (search)", found is not None,
              f"found={found}")
    # Printed improvements from the page output (page lines 311-320): verify each strictly raises both utilities.
    printed = {
        (1, 1): ((F(6, 5), F(6, 7)), (F(34, 5), F(22, 7))),
        (2, 2): ((F(5, 2), F(5, 3)), (F(11, 2), F(7, 3))),
        (3, 1): ((F(18, 7), F(6, 5)), (F(38, 7), F(14, 5))),
        (3, 2): ((F(27, 8), F(9, 5)), (F(37, 8), F(11, 5))),
        (4, 1): ((F(3), F(3, 2)), (F(5), F(5, 2))),
        (4, 3): ((F(5), F(5, 2)), (F(3), F(3, 2))),
        (5, 2): ((F(37, 8), F(11, 5)), (F(27, 8), F(9, 5))),
        (5, 3): ((F(38, 7), F(14, 5)), (F(18, 7), F(6, 5))),
        (6, 2): ((F(11, 2), F(7, 3)), (F(5, 2), F(5, 3))),
        (7, 3): ((F(34, 5), F(22, 7)), (F(6, 5), F(6, 7))),
    }
    for (x, y), (new_a, new_b) in printed.items():
        ok = (
            uA(*new_a) > uA(F(x), F(y))
            and uB(*new_a) > uB(F(x), F(y))
            and new_b == (X - new_a[0], Y - new_a[1])
            and 0 <= new_a[0] <= X and 0 <= new_a[1] <= Y
            and (new_a[0].denominator != 1 or new_a[1].denominator != 1)
        )
        check(f"L08 printed improvement from ({x},{y}) is strict for both, B is the rest, not on grid", ok,
              f"uA {uA(*new_a)} vs {uA(F(x), F(y))}, uB {uB(*new_a)} vs {uB(F(x), F(y))}")
    # Printed utilities
    check("L08 printed utilities at (3,1)->108/35, 76/5", uA(F(18, 7), F(6, 5)) == F(108, 35)
          and uB(F(18, 7), F(6, 5)) == F(76, 5))
    check("L08 printed utilities at (2,2)->25/6, 77/6", uA(F(5, 2), F(5, 3)) == F(25, 6)
          and uB(F(5, 2), F(5, 3)) == F(77, 6))
    check("L08 printed utilities at (1,1)->36/35, 748/35", uA(F(6, 5), F(6, 7)) == F(36, 35)
          and uB(F(6, 5), F(6, 7)) == F(748, 35))
    # Example 2.5
    check("L08 Example 2.5 utilities (6,3)->(18,2), (2,1)->(2,18)", (uA(F(6), F(3)), uB(F(6), F(3))) == (18, 2)
          and (uA(F(2), F(1)), uB(F(2), F(1))) == (2, 18))
    # Lemma 2.1 / Theorem 2.4 spot: for interior rational allocations on a fine grid, r_A == r_B iff yX == xY
    ok = True
    for den in range(1, 13):
        for nx in range(1, X * den):
            for ny in range(1, Y * den):
                x, y = F(nx, den), F(ny, den)
                ra, rb = y / x, (Y - y) / (X - x)
                ok = ok and ((ra == rb) == (y * X == x * Y))
    check("L08 Lemma 2.1 equal rates iff diagonal on fine interior grid", ok)
    # Proposition 2.3 bound: sqrt(uA)+sqrt(uB) <= sqrt(XY) => (uA+uB+2 sqrt(uA uB)) <= XY, check exact
    ok = True
    eq = []
    for x, y in pts:
        ua, ub = uA(F(x), F(y)), uB(F(x), F(y))
        slack = X * Y - ua - ub
        ok = ok and slack >= 0 and 4 * ua * ub <= slack * slack
        if 4 * ua * ub == slack * slack:
            eq.append((x, y))
    check("L08 Prop 2.3 bound and equality set on grid", ok and eq == [(0, 0), (2, 1), (4, 2), (6, 3), (8, 4)])
    # Prop 2.3 on a fine rational grid, all feasible points: (sqrt uA + sqrt uB)^2 <= XY, exact check
    ok = True
    for den in range(1, 9):
        for nx in range(0, X * den + 1):
            for ny in range(0, Y * den + 1):
                x, y = F(nx, den), F(ny, den)
                ua, ub = uA(x, y), uB(x, y)
                slack = X * Y - ua - ub
                ok = ok and slack >= 0 and 4 * ua * ub <= slack * slack
    check("L08 Prop 2.3 bound on fine rational grid", ok)
    # M2: (4,1), X=10, Y=5
    Xm, Ym = 10, 5
    lam = F(11, 24)
    x, y = F(4), F(1)
    ra, rb = y / x, (F(Ym) - y) / (F(Xm) - x)
    h = F(10, 11)
    na = (x - h, y + lam * h)
    nb = (F(Xm) - na[0], F(Ym) - na[1])
    check("L08 M2 rates 1/4 and 2/3, lambda between", ra == F(1, 4) and rb == F(2, 3) and ra < lam < rb)
    check("L08 M2 bound A", (lam * x - y) / lam == F(20, 11))
    check("L08 M2 bound B", (F(4) - lam * 6) / lam == F(30, 11))
    check("L08 M2 holdings and utilities 34/11,17/12; 289/66; 76/11,43/12; 817/33",
          na == (F(34, 11), F(17, 12)) and na[0] * na[1] == F(289, 66) and nb == (F(76, 11), F(43, 12))
          and nb[0] * nb[1] == F(817, 33) and na[0] * na[1] > 4 and nb[0] * nb[1] > 24)
    # R3: X=8, Y=4 allocation A=(0,2)
    a0 = (F(0), F(2))
    b0 = (F(8) - a0[0], F(4) - a0[1])
    na = (F(8, 3), F(1))
    nb = (F(8) - na[0], F(4) - na[1])
    check("L08 R3 (0,2) improved by A=(8/3,1)", uA(*a0) == 0 and uA(*na) == F(8, 3)
          and uB(*a0) == 16 and uB(*na) == 16 and nb == (F(16, 3), F(3)))
    # E1: gains at (3,1)
    check("L08 E1 gains 3/35 and 1/5; shares 1/35 and 1/75",
          uA(F(18, 7), F(6, 5)) - 3 == F(3, 35) and uB(F(18, 7), F(6, 5)) - 15 == F(1, 5)
          and F(3, 35) / 3 == F(1, 35) and F(1, 5) / 15 == F(1, 75))
    check("L08 E1 percentages 2.9 (2.857) and 1.3 (1.333)", round(100 * float(F(1, 35)), 1) == 2.9
          and round(100 * float(F(1, 75)), 1) == 1.3)
    # Quiz
    check("L08 quiz q5 (4,1) not efficient: yX=8 xY=16", (1 * X, 4 * Y) == (8, 16))
    check("L08 quiz q8 ratio y/x on diagonal = 0.5", F(Y, X) == F(1, 2))
    check("L08 quiz q9 sqrt sum at (4,2) = sqrt32 = 5.657 -> 5.66",
          round(math.sqrt(8) + math.sqrt(8), 2) == 5.66 and abs(2 * math.sqrt(8) - math.sqrt(32)) < 1e-12)
    # Misconception-level "(4,2)" check
    check("L08 quiz (4,2) utilities 8 and 8", uA(F(4), F(2)) == 8 and uB(F(4), F(2)) == 8)


# ---------------------------------------------------------------- L09
def l09() -> None:
    n = 0
    bad = 0
    for a in (50, 100, 600, 1000):
        for b in (1, 2, 5, 10):
            for c in (0, 50, 100, 200):
                for e in (0, 10, 50, 120):
                    if not (c < a and c + e < a):
                        continue
                    n += 1
                    qp = F(a - c, b)
                    qs = F(a - c - e, b)
                    V = lambda q: a * q - F(b, 2) * q * q - (c + e) * q  # noqa: E731
                    loss = V(qs) - V(qp)
                    ok = (
                        qp - qs == F(e, b)
                        and V(qs) - F(b, 2) * (qp - qs) ** 2 == V(qp)
                        and loss == F(e * e, 2 * b)
                        and all(V(qs) - F(b, 2) * (F(q, 4) - qs) ** 2 == V(F(q, 4)) for q in range(-40, 400))
                        and qs >= 0
                    )
                    if not ok:
                        bad += 1
    check("L09 Prop 1.3, Prop 1.4, Cor 1.5 identities", bad == 0, f"over {n} parameter sets, failures={bad}")

    # Prop 1.6: q(t) = q_s iff t = e
    ok = True
    for a, b, c, e in [(1000, 10, 200, 120), (600, 5, 100, 50), (50, 1, 0, 10)]:
        qs = F(a - c - e, b)
        for t in range(0, 201):
            if (F(a - c - t, b) == qs) != (t == e):
                ok = False
    check("L09 Prop 1.6 tax equals e only", ok)

    # Lab numbers
    a, b, c, e = 1000, 10, 200, 120
    qp = F(a - c, b)
    qs = F(a - c - e, b)
    check("L09 lab qp=80, qs=68, tax 120 unique in 0..200", qp == 80 and qs == 68
          and [t for t in range(201) if F(a - c - t, b) == qs] == [120])
    check("L09 lab revenue 120*68 = 8160 cents = 81.60 CU", e * qs == 8160 and F(8160, 100) == F("81.6"))
    check("L09 lab loss 720 by wedge and surplus", F(e * e, 2 * b) == 720)

    def W(q: F) -> F:
        return F(a + (a - b * q), 2) * q - (c + e) * q  # ∫0^q (a - b s) ds - (c+e) q, as trapezoid (exact)

    def wedge(q: F) -> F:
        return (c + e) - (a - b * q)

    by_w = (wedge(qs) + wedge(qp)) / 2 * (qp - qs)
    check("L09 lab wedge area 720", by_w == 720)
    check("L09 lab surplus difference 720", W(qs) - W(qp) == 720)
    check("L09 misconception 1 price below 320 on (68,80]",
          all((a - b * F(k, 10)) < 320 for k in range(681, 801)))
    best = max(range(0, 101), key=lambda q: F(a) * q - F(b, 2) * q * q - (c + e) * q)
    check("L09 integer quantity maximising V over 0..100 is 68", best == 68, f"best={best}")
    # M1 numbers
    a, b, c, e = 600, 5, 100, 50
    check("L09 M1 q_p=100, q_s=90, tax 50, loss 250", F(a - c, b) == 100 and F(a - c - e, b) == 90
          and F(e * e, 2 * b) == 250 and F(1, 2) * 10 * 50 == 250)
    # Public good: A(g) = w1 + w2, cost 400
    w1 = lambda g: 1000 - 100 * g  # noqa: E731
    w2 = lambda g: max(F(0), 600 - 200 * g)  # noqa: E731
    A = lambda g: w1(g) + w2(g)  # noqa: E731

    def S(g: F) -> F:
        # exact area of the piecewise linear A over [0, g] (kink at 3), less 400 g
        area = F(0)
        lo = F(0)
        for kink in (F(3),):
            hi = min(g, kink)
            if hi > lo:
                area += (A(lo) + A(hi)) / 2 * (hi - lo)
            lo = max(lo, kink) if g > kink else lo
        if g > F(3):
            area += (A(F(3)) + A(g)) / 2 * (g - F(3))
        return area - 400 * g

    check("L09 vertical sum at 3 is 700", A(F(3)) == 700)
    check("L09 consumer 2 at 6 is 0; consumer 1 at 6 is 400", w2(F(6)) == 0 and w1(F(6)) == 400)
    ints = [g for g in range(0, 11) if A(F(g)) == 400]
    check("L09 integer vertical sum = 400 only at 6", ints == [6])
    check("L09 S(6)=2700, S(7)=2650, S(4)=2500, S(3)=2250", S(F(6)) == 2700 and S(F(7)) == 2650
          and S(F(4)) == 2500 and S(F(3)) == 2250)
    check("L09 argmax of S over integers 0..10 is 6", max(range(11), key=lambda g: S(F(g))) == 6)
    # continuous maximiser is 6 (S' = A - 400 with unique zero)
    fine = [F(k, 100) for k in range(0, 1001)]
    check("L09 argmax of S over grid of 1/100 on [0,10] is 6", max(fine, key=S) == 6)
    h = max(F(0), F(600 - 400, 200)) + F(1000 - 400, 100)
    check("L09 horizontal sum at price 400 is 7", h == 7)
    check("L09 E2 share 2650/2700 = 0.9815 and 2500/2700 = 0.9259",
          round(2650 / 2700, 4) == 0.9815 and round(2500 / 2700, 4) == 0.9259)
    check("L09 E2 S(4)=3450+650-1600", 3450 + 650 - 1600 == 2500)
    check("L09 E2 pieces: int_0^3 (1600-300s) = 3450, int_3^4 (1000-100s) = 650",
          (F(1600) * 3 - F(300, 2) * 9) == 3450 and (F(1000) * 1 - F(100, 2) * (16 - 9)) == 650)
    # E1 (tax 100): q=70, loss 20, wedge check
    qt = F(1000 - 200 - 100, 10)
    check("L09 E1 tax 100 gives 70 units; loss 20 by Prop 1.4 and by wedge", qt == 70
          and F(10, 2) * (qt - 68) ** 2 == 20 and (320 - (1000 - 10 * qt)) == 20 and F(1, 2) * (0 + 20) * 2 == 20)
    # R1: tax t = k q_s with q_s=(a-c)/(b+k)
    for (a1, b1, c1, k) in [(1000, 10, 200, 5), (600, 5, 100, 2), (300, 3, 30, F(1, 2))]:
        qs1 = F(a1 - c1) / (b1 + k)
        t = F(a1 - c1) - b1 * qs1
        check(f"L09 R1 tax equals damage at efficient quantity for {(a1, b1, c1, k)}", t == k * qs1)
    # R2: 40 units and 800/15
    qp2 = F(1000 - 200, 10)
    t2 = 5 * qp2
    q2 = (F(1000 - 200) - t2) / 10
    check("L09 R2 tax 400, quantity 40, efficient 800/15 = 53.33", t2 == 400 and q2 == 40
          and round(float(F(800, 15)), 1) == 53.3 and round(float(F(800, 15) - 40), 1) == 13.3)
    # R2 general claim: k^2 = 0 needed
    ok = True
    for (a1, b1, c1) in [(1000, 10, 200), (600, 5, 100)]:
        for k in (F(1), F(5), F(1, 3)):
            qp1 = F(a1 - c1, b1)
            qq = (a1 - c1 - k * qp1) / b1
            qs1 = F(a1 - c1) / (b1 + k)
            ok = ok and qq != qs1
    check("L09 R2 quantities differ for k>0 on samples", ok)
    # E3 claims
    check("L09 E3 consumer 2 line at 6 is -600", 600 - 200 * 6 == -600)
    check("L09 E3 vertical sum on [0,3] >= 700", all(A(F(k, 100)) >= 700 for k in range(0, 301)))
    # R3 derivative sign: A(g)-400 positive below 6, negative above, on [0,10]
    check("L09 R3 sign of A-400 on [0,10]", all((A(F(k, 100)) - 400) > 0 for k in range(0, 600))
          and all((A(F(k, 100)) - 400) < 0 for k in range(601, 1001)))
    # M2 public good example: A(g)=1200-200g; g*=3.5; S=1225
    B = lambda g: (800 - 100 * g) + (400 - 100 * g)  # noqa: E731
    gstar = F(7, 2)
    check("L09 M2 vertical sum 1200-200g and g*=3.5", B(gstar) == 500 and B(F(0)) == 1200)
    val = F(1200) * gstar - 100 * gstar * gstar - 500 * gstar
    check("L09 M2 total surplus 1225", val == 1225)
    # M3 horizontal at 500: q1=3, q2 = max(0, -1) = 0
    check("L09 M3 horizontal 3 units at 500", (800 - 500) / F(100) == 3 and max(F(0), (400 - 500) / F(100)) == 0)
    # P3-like claim and key-result numbers


if __name__ == "__main__":
    l07()
    l08()
    l09()
    print(f"TOTAL FAILS: {len(FAILS)}")
    for f in FAILS:
        print("  FAILED:", f)
