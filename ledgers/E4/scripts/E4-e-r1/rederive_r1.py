"""Round-1 re-derivation of the numbers in the changed and added E4 cards (slice e, pin 95f3f8cb)."""

import math
from collections.abc import Sequence
from fractions import Fraction
from itertools import product

Vec = tuple[Fraction, ...]
out: list[str] = []


def show(label: str, value: object) -> None:
    out.append(f"{label}: {value}")


def dot(p: Sequence[Fraction], q: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(p, q, strict=True)), Fraction(0))


def lab1_l01() -> None:
    prices = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5))
    probs = (Fraction(1, 8), Fraction(3, 8), Fraction(3, 8), Fraction(1, 8))
    claim = (Fraction(100), Fraction(40), Fraction(0), Fraction(250))
    other = (Fraction(0), Fraction(60), Fraction(120), Fraction(30))
    show("c011 value of claim", dot(prices, claim))
    show("c265 value of second claim", dot(prices, other))
    show("c013 expected payoff", dot(probs, claim))
    combo = tuple(2 * a - Fraction(1, 2) * b for a, b in zip(claim, other, strict=True))
    show("c012 value of combination", dot(prices, combo))
    show("c012 equality", dot(prices, combo) == 2 * dot(prices, claim) - Fraction(1, 2) * dot(prices, other))


def example_2_11() -> None:
    pi = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4))
    e1 = (Fraction(3), Fraction(4), Fraction(1))
    e2 = (Fraction(1), Fraction(4), Fraction(3))
    ebar = tuple(a + b for a, b in zip(e1, e2, strict=True))
    th1 = sum((p * a / e for p, a, e in zip(pi, e1, ebar, strict=True)), Fraction(0))
    th2 = sum((p * b / e for p, b, e in zip(pi, e2, ebar, strict=True)), Fraction(0))
    show("c266 theta1 theta2 sum", (th1, th2, th1 + th2))
    show("Example 2.11 prices", tuple(p / e for p, e in zip(pi, ebar, strict=True)))
    show("Example 2.11 q.ebar", dot(tuple(p / e for p, e in zip(pi, ebar, strict=True)), ebar))


def lab3_grid() -> None:
    pi = (0.5, 0.25, 0.25)
    e1 = (3.0, 4.0, 1.0)
    e2 = (1.0, 4.0, 3.0)
    total = (4.0, 8.0, 4.0)
    eq1 = (2.25, 4.5, 2.25)
    eq2 = (1.75, 3.5, 1.75)

    def util(x: Sequence[float]) -> float:
        return sum(p * math.log(v) for p, v in zip(pi, x, strict=True))

    grid = (0.0, 0.25, 0.5, 0.75, 1.0)
    ref_eq = (util(eq1), util(eq2))
    ref_end = (util(e1), util(e2))
    n_eq = 0
    n_end = 0
    first: tuple[tuple[float, ...], tuple[float, ...]] | None = None
    count = 0
    for f in product(grid, repeat=3):
        count += 1
        a1 = tuple(fr * t for fr, t in zip(f, total, strict=True))
        a2 = tuple(t - x for t, x in zip(total, a1, strict=True))
        if min(a1 + a2) <= 0:
            continue
        u1, u2 = util(a1), util(a2)
        for ref, tag in ((ref_eq, "eq"), (ref_end, "end")):
            ge = u1 >= ref[0] - 1e-12 and u2 >= ref[1] - 1e-12
            strict = u1 > ref[0] + 1e-12 or u2 > ref[1] + 1e-12
            if ge and strict:
                if tag == "eq":
                    n_eq += 1
                else:
                    n_end += 1
                    if first is None:
                        first = (a1, a2)
    show("c048 grid allocations", count)
    show("c048 grid improvements at equilibrium", n_eq)
    show("c214 grid improvements at endowment", n_end)
    show("c214 first improvement", first)
    show("L02/L03 witness gain per agent 1/4 ln(4/3)", 0.25 * math.log(4 / 3))


def l07_rho() -> None:
    def rho2(sig_u: Fraction) -> Fraction:
        kappa = Fraction(1) / Fraction(1, 2)
        sig_eta2 = 1 + kappa * kappa * sig_u * sig_u
        return Fraction(1) / (1 + sig_eta2)

    vals = [rho2(Fraction(s)) for s in ("1/4", "1/2", "1", "2", "4")]
    show("c142 rho2 at sigma_u 1/4 1/2 1 2 4", [str(v) for v in vals])


def l05_fixed_point() -> None:
    alpha, beta, vs, delta = Fraction(10), Fraction(2), Fraction(1, 2), Fraction(3, 4)
    c0 = alpha / (beta + vs)
    c1 = -delta / (beta + vs)
    r0 = (alpha - vs * c0) / beta - c0
    r1 = -(vs * c1 + delta) / beta - c1
    show("c090 c263 fixed point and residuals", (c0, c1, r0, r1))
    alpha2, beta2, vs2 = Fraction(10), Fraction(2), Fraction(2)
    show("c219 fixed point at varsigma=2", (alpha2 / (beta2 + vs2), -Fraction(3, 4) / (beta2 + vs2)))


def l08_gain() -> None:
    show("c186 c270 G(0) at Example 1.1 = ln2/4", math.log(2) / 4)
    show("c270 G(0) > 0.15 and G(1)=0 < 0.15", (math.log(2) / 4 > 0.15, 0.0 < 0.15))


def var_du(lam: float, a: float, sv2: float, se2: float, su2: float) -> tuple[float, float]:
    kappa = a * se2 / lam
    tau_v = 1 / sv2
    tau_e = 1 / se2
    tau_eta = 1 / (se2 + kappa * kappa * su2)
    big_a = lam * tau_e + (1 - lam) * tau_eta
    beta = big_a / (tau_v + big_a)
    b_y = tau_eta / (tau_v + tau_eta)
    sig_eta2 = 1 / tau_eta
    v_u = 1 / (tau_v + tau_eta)
    vd = (b_y - beta) ** 2 * (sv2 + sig_eta2)
    return vd, vd / v_u


def l08_limit() -> None:
    for lam in (1e-4, 1e-6):
        show(
            f"c260 Var(D_U), Var(D_U)/V_U at lam={lam} (a=2, sv2=3, se2=0.5, su2=1.5)", var_du(lam, 2.0, 3.0, 0.5, 1.5)
        )
    show("c260 predicted Var(D_U) a^2 su2 sv^4 = 54, ratio a^2 su2 sv^2 = 18", (4 * 1.5 * 9, 4 * 1.5 * 3))


def l09_example() -> None:
    x = {1: -1, 2: 2, 3: -2, 4: -2, 5: -2, 6: -2}
    p1 = [{1, 2}, {3}, {4, 5, 6}]
    p2 = [{1, 2, 3}, {4, 5}, {6}]

    def post(part: list[set[int]], w: int, r: dict[int, int]) -> Fraction:
        cell = next(c for c in part if w in c)
        return Fraction(sum(r[k] for k in cell), len(cell))

    neg = {k: -v for k, v in x.items()}
    show("c200 g_1(1)", post(p1, 1, x))
    show("c269 g_2(1)", post(p2, 1, neg))
    show("c269 g_1(3)", post(p1, 3, x))
    meet = {1}
    grown = True
    while grown:
        grown = False
        for part in (p1, p2):
            for c in part:
                if meet & c and not c <= meet:
                    meet |= c
                    grown = True
    show("c200 meet M(1)", sorted(meet))


def lemma_7_4() -> None:
    import random

    rng = random.Random(1)
    for _ in range(3):
        xs = [rng.gauss(0, 1) for _ in range(2000)]
        ys = [0.6 * x + rng.gauss(0, 1) for x in xs]
        mx = sum(xs) / len(xs)
        my = sum(ys) / len(ys)
        xs = [x - mx for x in xs]
        ys = [y - my for y in ys]
        n = len(xs)
        vx = sum(x * x for x in xs) / n
        vy = sum(y * y for y in ys) / n
        cxy = sum(x * y for x, y in zip(xs, ys, strict=True)) / n
        b = cxy / vy
        mse = sum((x - b * y) ** 2 for x, y in zip(xs, ys, strict=True)) / n
        show("c264 Lemma 7.4 check (mse, Var(X)-Cov^2/Var(Y))", (round(mse, 9), round(vx - cxy * cxy / vy, 9)))


if __name__ == "__main__":
    lab1_l01()
    example_2_11()
    lab3_grid()
    l07_rho()
    l05_fixed_point()
    l08_gain()
    l08_limit()
    l09_example()
    lemma_7_4()
    print("\n".join(out))
