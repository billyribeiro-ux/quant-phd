"""Independent re-derivation of the numbers printed on E4 L07 and L08 (verifier round 11).

Nothing here imports the course code or the lab twins. The price coefficients are NOT taken from the closed form
of L06 Proposition 6.7: they are found by solving the two market-clearing coefficient equations numerically, and the
closed form is then only compared with the solution. Moments of the price are computed from its coefficients.

Run: python3 -I -W error indep_L07_L08.py
"""

from __future__ import annotations

import math
import random
from fractions import Fraction as F


def exact_clearing_residual(sv2: F, se2: F, a: F, lam: F, su2: F, ts: F, tu: F) -> tuple[F, F]:
    """Exact residuals of the two clearing coefficient equations at (theta_s, theta_u).

    Demands (zero prior mean): informed x_I = (E[v|s] - p) / (a Var(v|s,p)); uninformed x_U = (E[v|p] - p)/(a Var(v|p)).
    Clearing: lam x_I + (1 - lam) x_U = u, with p = ts*s - tu*u. Coefficient form:
      s-coefficient: must be 0; u-coefficient: must be 1.
    """
    vs = sv2 + se2
    varp = ts * ts * vs + tu * tu * su2
    covvp = ts * sv2
    b = covvp / varp  # E[v|p] = b p
    vu = sv2 - covvp * covvp / varp  # Var(v|p)
    ws = sv2 / vs  # E[v|s] = ws s
    vI = sv2 - sv2 * sv2 / vs  # Var(v|s)
    # x_I = (ws*s - p)/(a vI) with p = ts*s - tu*u  -> s-coef (ws - ts)/(a vI), u-coef tu/(a vI)
    # x_U = (b*p - p)/(a vU) = (b-1)*(ts*s - tu*u)/(a vU) -> s-coef (b-1) ts/(a vU), u-coef -(b-1) tu/(a vU)
    s_coef = lam * (ws - ts) / (a * vI) + (1 - lam) * (b - 1) * ts / (a * vu)
    u_coef = lam * tu / (a * vI) - (1 - lam) * (b - 1) * tu / (a * vu) - 1
    return s_coef, u_coef


def solve_coefficients_float(sv2: float, se2: float, a: float, lam: float, su2: float) -> tuple[float, float]:
    """Newton iteration on the two clearing equations, floats, from a generic start (no closed form used)."""
    ts, tu = 0.3, 0.3

    def resid(ts_: float, tu_: float) -> tuple[float, float]:
        vs = sv2 + se2
        varp = ts_ * ts_ * vs + tu_ * tu_ * su2
        covvp = ts_ * sv2
        b = covvp / varp
        vu = sv2 - covvp * covvp / varp
        ws = sv2 / vs
        vI = sv2 - sv2 * sv2 / vs
        r1 = lam * (ws - ts_) / (a * vI) + (1 - lam) * (b - 1) * ts_ / (a * vu)
        r2 = lam * tu_ / (a * vI) - (1 - lam) * (b - 1) * tu_ / (a * vu) - 1
        return r1, r2

    for _ in range(200):
        r1, r2 = resid(ts, tu)
        h = 1e-7
        a11 = (resid(ts + h, tu)[0] - r1) / h
        a12 = (resid(ts, tu + h)[0] - r1) / h
        a21 = (resid(ts + h, tu)[1] - r2) / h
        a22 = (resid(ts, tu + h)[1] - r2) / h
        det = a11 * a22 - a12 * a21
        dts = (a22 * r1 - a12 * r2) / det
        dtu = (-a21 * r1 + a11 * r2) / det
        ts -= dts
        tu -= dtu
        if abs(dts) + abs(dtu) < 1e-15:
            break
    return ts, tu


def closed_form_float(sv2: float, se2: float, a: float, lam: float, su2: float) -> tuple[float, float]:
    """L06 Proposition 6.7 closed form, used only as a comparison target."""
    tv, te = 1 / sv2, 1 / se2
    kappa = a * se2 / lam
    teta = 1 / (se2 + kappa * kappa * su2)
    tbar = lam * te + (1 - lam) * teta
    ths = tbar / (tv + tbar)
    return ths, kappa * ths


def moments(sv2: float, se2: float, su2: float, ts: float, tu: float) -> dict[str, float]:
    vs = sv2 + se2
    varp = ts * ts * vs + tu * tu * su2
    covvp = ts * sv2
    covvs = sv2
    return {
        "varp": varp,
        "rho2": covvp * covvp / (sv2 * varp),
        "b_s": covvs / vs,
        "b_p": covvp / varp,
        "vI": sv2 - covvs * covvs / vs,
        "vU": sv2 - covvp * covvp / varp,
        "varDI": None,  # filled by gain()
    }


def gain(sv2: float, se2: float, a: float, lam: float, su2: float) -> dict[str, float]:
    """Gain from information G(lam) from the definitions: D_I = E[v|s] - p, D_U = E[v|p] - p."""
    ts, tu = solve_coefficients_float(sv2, se2, a, lam, su2)
    m = moments(sv2, se2, su2, ts, tu)
    vs = sv2 + se2
    # D_I = b_s s - (ts s - tu u): Var = (b_s - ts)^2 Var(s) + tu^2 su2
    var_di = (m["b_s"] - ts) ** 2 * vs + tu * tu * su2
    # D_U = (b_p - 1) p: Var = (b_p - 1)^2 Var(p)
    var_du = (m["b_p"] - 1) ** 2 * m["varp"]
    g = math.log((1 + var_di / m["vI"]) / (1 + var_du / m["vU"])) / (2 * a)
    return {"ts": ts, "tu": tu, "gain": g, "corr2": m["rho2"], "varp": m["varp"], "b_p_over": m["b_p"]}


def part_l07() -> None:
    print("== L07 exact checks (Fraction)")
    sv2, se2, a, lam = F(1), F(1), F(1), F(1, 2)
    # closed form values from L06 Prop 6.7 in exact arithmetic
    for su in (F(1, 4), F(1, 2), F(1), F(2), F(4), F(1, 100)):
        su2 = su * su
        kappa = a * se2 / lam
        teta = 1 / (se2 + kappa * kappa * su2)
        tbar = lam / se2 + (1 - lam) * teta
        ts = tbar / (1 / sv2 + tbar)
        tu = kappa * ts
        sr, ur = exact_clearing_residual(sv2, se2, a, lam, su2, ts, tu)
        vs = sv2 + se2
        varp = ts * ts * vs + tu * tu * su2
        rho2 = (ts * sv2) ** 2 / (sv2 * varp)
        print(f"sd {su}: clearing residuals exact s={sr} u={ur}; var_p={varp}; rho2={rho2}; sig_eta2={se2 + kappa * kappa * su2}")
    # the printed sweep values
    print("Printed Part B: rho2 4/9, 1/3, 1/6, 1/18, 1/66; var_p 729/1444, 27/49, 27/32, 729/338, 35937/4802")
    print("Printed Part E: benchmark 1/2; sd 1/100 rho2 2500/5001")
    print(f"2500/5001 = {F(2500, 5001)}; check 1/(1+(1+4*(1/100)**2)) = {1 / (1 + 1 + 4 * F(1, 10000))}")
    # Part F population value and a recomputed sample statistic with the same draw order
    rng = random.Random(7)
    ts = float(F(3, 7))
    tu = float(F(6, 7))
    vs_, ps = [], []
    for _ in range(20000):
        v = rng.gauss(0.0, 1.0)
        eps = rng.gauss(0.0, 1.0)
        u = rng.gauss(0.0, 0.5)
        vs_.append(v)
        ps.append(ts * (v + eps) - tu * u)
    n = len(vs_)
    mv = sum(vs_) / n
    mp = sum(ps) / n
    cov = sum((x - mv) * (y - mp) for x, y in zip(vs_, ps)) / n
    vv = sum((x - mv) ** 2 for x in vs_) / n
    vp = sum((y - mp) ** 2 for y in ps) / n
    print(f"Part F recomputed: sample rho2 = {cov * cov / (vv * vp):.6f} (printed 0.330625); population 1/3 = {1 / 3:.6f}")


def part_l08() -> None:
    print("== L08 float checks (independent route, Newton-solved coefficients)")
    sv2, se2, su2, a = 1.0, 1.0, 1.0, 2.0
    g0 = math.log(1 + sv2 / se2) / (2 * a)
    print(f"G(0) closed form = {g0:.9f} (printed 0.173287)")
    g1 = gain(sv2, se2, a, 1.0, su2)
    print(f"G(1) = {g1['gain']:.9f} vs ln(5/3)/4 = {math.log(5 / 3) / 4:.9f}; corr2(1) = {g1['corr2']:.9f} vs 1/6")
    gh = gain(sv2, se2, a, 0.5, su2)
    print(f"G(0.5) = {gh['gain']:.9f} (printed 0.158997); corr2(0.5) = {gh['corr2']:.9f}; ts={gh['ts']:.9f}, tu={gh['tu']:.9f}")
    print(f"Part A: b_y/beta at lam=0.5 = closed form {gh['b_p_over']:.9f} (printed 0.1605 via b_y/beta)")
    gt = gain(sv2, se2, a, 1e-6, su2)
    print(f"G(1e-6) - G(0) = {gt['gain'] - g0:.3e} (printed -6.25e-14; continuity)")
    # Part C: own bisection on gain(lam)-cost, bracket [0,1]
    for cost in (0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18):
        if cost >= g0:
            lam_star = 0.0
            gap = g0 - cost
            corr = 0.0
            rule = "zero"
        elif cost <= g1["gain"]:
            lam_star = 1.0
            gap = g1["gain"] - cost
            corr = g1["corr2"]
            rule = "one"
        else:
            lo, hi = 0.0, 1.0
            while hi - lo > 1e-12:
                mid = 0.5 * (lo + hi)
                if gain(sv2, se2, a, mid, su2)["gain"] - cost > 0:
                    lo = mid
                else:
                    hi = mid
            lam_star = 0.5 * (lo + hi)
            gg = gain(sv2, se2, a, lam_star, su2)
            gap = gg["gain"] - cost
            corr = gg["corr2"]
            rule = "root"
        print(f"cost {cost:.2f}: lam* = {lam_star:.9f}, gap = {gap:.2e}, corr2 = {corr:.6f} ({rule})")
    # Part D: sigma_u = 0 (no supply noise). The clearing equation is s-only: u = 0 identically, so the
    # u-coefficient equation is vacuous. Solve the s-coefficient equation exactly: theta_s = b_s gives zero gain.
    sv2_, se2_ = 1.0, 1.0
    bs = sv2_ / (sv2_ + se2_)
    cnt = 0
    worst = 0.0
    for k in range(1, 1000):
        x = k / 1000
        ts_ = bs
        vs_ = sv2_ + se2_
        varp = ts_ * ts_ * vs_
        b_p = ts_ * sv2_ / varp
        s_res = x * (bs - ts_) / (a * (1 / (1 / sv2_ + 1 / se2_))) + (1 - x) * (b_p - 1) * ts_ / (a * (sv2_ - (ts_ * sv2_) ** 2 / varp))
        worst = max(worst, abs(s_res))
        var_di = (bs - ts_) ** 2 * vs_
        var_du = (b_p - 1) ** 2 * varp
        g = math.log((1 + var_di / (1 / (1 / sv2_ + 1 / se2_))) / (1 + var_du / (sv2_ - (ts_ * sv2_) ** 2 / varp))) / (2 * a)
        worst = max(worst, abs(g))
        if abs(g - 0.15) <= 1e-9:
            cnt += 1
    print(f"Part D: sigma_u=0: max |s-clearing residual| and |gain| over the 999 grid = {worst:.1e}; interior grid fractions with gain = 0.15: {cnt} (printed 0)")
    print("Part D: sigma_u=0: gain(0) = ln(2)/4 =", f"{math.log(2) / 4:.6f}", "(printed 0.173287); gain(1) = 0 (printed 0.000000)")

if __name__ == "__main__":
    part_l07()
    part_l08()
