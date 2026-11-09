"""Independent exact re-derivation of the numbers quoted in the changed L03 and L06 text and in the cards for the
E4 cards slice, round 16. Uses only fractions and the standard library.

Usage: python3 -I rederive_r16.py
"""

import math
from fractions import Fraction


def mrs(pi: list[Fraction], x: list[Fraction], s: int, t: int) -> Fraction:
    return (pi[s] / x[s]) / (pi[t] / x[t])


def log_utility(pi: list[Fraction], x: list[Fraction]) -> float:
    return sum(float(p) * math.log(float(v)) for p, v in zip(pi, x, strict=True))


def closed(sv2: Fraction, se2: Fraction, a: Fraction, lam: Fraction, su2: Fraction) -> dict[str, Fraction]:
    tv, te = 1 / sv2, 1 / se2
    kappa = a / (lam * te)
    seta2 = se2 + kappa * kappa * su2
    teta = 1 / seta2
    tbar = lam * te + (1 - lam) * teta
    ths = tbar / (tv + tbar)
    return {
        "kappa": kappa,
        "sig_eta2": seta2,
        "tau_eta": teta,
        "tau_bar": tbar,
        "theta_s": ths,
        "theta_u": kappa * ths,
        "tau_v": tv,
        "tau_e": te,
    }


def residual(s: Fraction, u: Fraction, th_s: Fraction, th_u: Fraction, a: Fraction, lam: Fraction) -> Fraction:
    sv2, se2, su2 = Fraction(1), Fraction(1), Fraction(1, 4)
    price = th_s * s - th_u * u
    var_p = th_s * th_s * (sv2 + se2) + th_u * th_u * su2
    cov = th_s * sv2
    slope = cov / var_p
    resid_var = sv2 - slope * cov
    var_i = sv2 * se2 / (sv2 + se2)
    mean_i = sv2 * s / (sv2 + se2)
    dem_i = (mean_i - price) / (a * var_i)
    dem_u = (slope * price - price) / (a * resid_var)
    return lam * dem_i + (1 - lam) * dem_u - u


def main() -> None:
    print("== L02 Example 2.11 (L02 line 189; L03 Example 3.6)")
    pi = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)]
    e1 = [Fraction(3), Fraction(4), Fraction(1)]
    e2 = [Fraction(1), Fraction(4), Fraction(3)]
    ebar = [a + b for a, b in zip(e1, e2, strict=True)]
    print("ebar", [str(v) for v in ebar])
    theta1 = sum(p * a / t for p, a, t in zip(pi, e1, ebar, strict=True))
    theta2 = sum(p * a / t for p, a, t in zip(pi, e2, ebar, strict=True))
    print("theta1", theta1, "theta2", theta2, "sum", theta1 + theta2)
    q = [p / t for p, t in zip(pi, ebar, strict=True)]
    print("q*", [str(v) for v in q], "q*.ebar", sum(a * b for a, b in zip(q, ebar, strict=True)))
    x1 = [theta1 * t for t in ebar]
    x2 = [theta2 * t for t in ebar]
    print("x1*", [str(v) for v in x1], "x2*", [str(v) for v in x2])
    summed = [a + b for a, b in zip(x1, x2, strict=True)]
    print("x1*+x2* =", [str(v) for v in summed], "equals ebar:", summed == ebar)
    print("wealth w1 = q.e1 =", sum(a * b for a, b in zip(q, e1, strict=True)))

    print("== L03 Example 3.6 MRS values against price ratios 4, 2, 1/2")
    for name, x in (("agent1", x1), ("agent2", x2)):
        print(name, "MRS12", mrs(pi, x, 0, 1), "MRS13", mrs(pi, x, 0, 2), "MRS23", mrs(pi, x, 1, 2))
    print("price ratios", q[0] / q[1], q[0] / q[2], q[1] / q[2])
    print("endowment MRS12 agent1", mrs(pi, e1, 0, 1), "(text R2: 8/3)", "agent2", mrs(pi, e2, 0, 1), "(text R2: 8)")
    print("endowment MRS13 agent1", mrs(pi, e1, 0, 2), "agent2", mrs(pi, e2, 0, 2))

    print("== L03 R2 trade y1 = (3-e, 4+4e, 1), y2 = (1+e, 4-4e, 3)")
    d1 = pi[0] * Fraction(-1, 3) + pi[1] * Fraction(4, 4)
    d2 = pi[0] * Fraction(1, 1) + pi[1] * Fraction(-4, 4)
    print("dU1/de at 0 =", d1, "(text 1/12)", "dU2/de at 0 =", d2, "(text 1/4)")
    y1 = [Fraction(3) - 0, Fraction(4), Fraction(1)]
    new1 = [Fraction(3) - Fraction(1, 10), Fraction(4) + Fraction(4, 10), Fraction(1)]
    new2 = [Fraction(1) + Fraction(1, 10), Fraction(4) - Fraction(4, 10), Fraction(3)]
    print("new bundles sum to ebar:", [a + b for a, b in zip(new1, new2, strict=True)] == ebar)
    print(
        "witness (2,4,3),(2,4,1) gains:",
        round(log_utility(pi, [Fraction(2), Fraction(4), Fraction(3)]) - log_utility(pi, e1), 12),
        round(log_utility(pi, [Fraction(2), Fraction(4), Fraction(1)]) - log_utility(pi, e2), 12),
        "vs 1/4 ln(4/3) =",
        round(0.25 * math.log(4 / 3), 12),
    )
    print(
        "witness sums to ebar:",
        [
            a + b
            for a, b in zip(
                [Fraction(2), Fraction(4), Fraction(3)], [Fraction(2), Fraction(4), Fraction(1)], strict=True
            )
        ],
    )
    print("y1 unused var", y1[0])

    print("== L06 Example 6.9 base instance (a = 1, lambda = 1/2, sig_u2 = 1/4)")
    c = closed(Fraction(1), Fraction(1), Fraction(1), Fraction(1, 2), Fraction(1, 4))
    print({k: str(v) for k, v in c.items()})
    ths, thu = c["theta_s"], c["theta_u"]
    var_p = ths * ths * Fraction(2) + thu * thu * Fraction(1, 4)
    cov_vp = ths
    b = cov_vp / var_p
    vu = Fraction(1) - b * cov_vp
    print("Var(p)", var_p, "Cov(v,p)", cov_vp, "slope b", b, "V_U", vu, "rho2", cov_vp**2 / var_p)
    print(
        "tau_eta/(theta_s(tau_v+tau_eta))",
        c["tau_eta"] / (ths * (c["tau_v"] + c["tau_eta"])),
        "1/(tau_v+tau_eta)",
        1 / (c["tau_v"] + c["tau_eta"]),
    )
    grid_s = [Fraction(-1), Fraction(0), Fraction(1), Fraction(2)]
    grid_u = [Fraction(-1), Fraction(0), Fraction(1, 2), Fraction(2)]
    res = [residual(s, u, ths, thu, Fraction(1), Fraction(1, 2)) for s in grid_s for u in grid_u]
    print("equilibrium residuals zero:", sum(1 for r in res if r == 0), "of", len(res))
    print(
        "alternative slope 1/2 residual at (1,0):",
        residual(Fraction(1), Fraction(0), Fraction(1, 2), thu, Fraction(1), Fraction(1, 2)),
        "(text -9/85)",
    )
    p10 = ths
    xi10 = (Fraction(1, 2) * Fraction(1) - p10) / (Fraction(1) * Fraction(1, 2))
    xu10 = (b * p10 - p10) / (Fraction(1) * vu)
    print("at (1,0): price", p10, "x_I", xi10, "x_U", xu10, "clear", Fraction(1, 2) * xi10 + Fraction(1, 2) * xu10)

    print("== L06 M1-M3 (a = 2, sig_v2 = sig_e2 = 1, lambda = 1/2, sig_u2 = 1/4)")
    m = closed(Fraction(1), Fraction(1), Fraction(2), Fraction(1, 2), Fraction(1, 4))
    print({k: str(v) for k, v in m.items() if k in ("kappa", "sig_eta2", "tau_eta", "tau_bar", "theta_s", "theta_u")})
    mt, mu = m["theta_s"], m["theta_u"]
    mvar = mt * mt * 2 + mu * mu * Fraction(1, 4)
    mb = mt / mvar
    print("M2 Var(p)", mvar, "b", mb, "Var(v|p)", 1 - mb * mt, "1/(tv+teta)", 1 / (m["tau_v"] + m["tau_eta"]))
    print("M2 rho2", mt * mt / mvar, "sv2/(sv2+seta2)", Fraction(1) / (Fraction(1) + m["sig_eta2"]))
    s0, u0 = Fraction(2), Fraction(1)
    p0 = mt * s0 - mu * u0
    xi = (s0 * m["tau_e"] - (m["tau_v"] + m["tau_e"]) * p0) / Fraction(2)
    yy = p0 / mt
    xu = (m["tau_eta"] * yy - (m["tau_v"] + m["tau_eta"]) * p0) / Fraction(2)
    print("M3 price", p0, "x_I", xi, "Y", yy, "x_U", xu, "clear", Fraction(1, 2) * xi + Fraction(1, 2) * xu, "u", u0)

    print("== L06 Lab 1 base-instance text values")
    print(
        "slope 7/9:",
        b == Fraction(7, 9),
        " posterior 2/3:",
        vu == Fraction(2, 3),
        " E[v|p] slope closed form equals b:",
        c["tau_eta"] / (ths * (c["tau_v"] + c["tau_eta"])) == b,
    )
    print("x_I (s=1,u=0) = 1/7:", (Fraction(1, 2) - Fraction(3, 7)) / Fraction(1, 2) == Fraction(1, 7))
    print("x_U (s=1,u=0) = -1/7:", (b * Fraction(3, 7) - Fraction(3, 7)) / vu == Fraction(-1, 7))
    print(
        "E2 numbers: 0.426617 - 3/7 =",
        round(0.426617 - 3 / 7, 6),
        "tolerance 0.006497; SE = 0.006497/3 =",
        round(0.006497 / 3, 6),
        "difference in SE:",
        round((0.426617 - 3 / 7) / (0.006497 / 3), 3),
    )
    print("E1 numbers: (0.80 - 7/9)/0.05 =", round((0.80 - 7 / 9) / 0.05, 3))


if __name__ == "__main__":
    main()
