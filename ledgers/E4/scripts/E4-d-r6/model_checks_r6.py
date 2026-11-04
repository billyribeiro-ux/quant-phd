"""Independent re-derivation of the E4 project model (verifier round 6). Usage: python -I model_checks_r6.py

Exact rational checks (fractions.Fraction) of Proposition 1 (clearing identity), Proposition 2 (squared correlation),
and the Lemma 1 demand; float checks of Propositions 3-5, Lemma 2, the box bounds, the grid ratios and the
lab-3 printed values. Every printed line is evidence for a row of the ledger.
"""

from __future__ import annotations

import math
from fractions import Fraction as F


def price_precision_exact(lam: F, sd: F) -> F:
    return lam * lam / (lam * lam + 4 * sd * sd)  # tau_e = 1, a = 2


def prop1_exact(lam: F, sd: F) -> dict[str, F]:
    ty = price_precision_exact(lam, sd)
    d = lam * 2 + (1 - lam) * (1 + ty)  # D = lam (tau_v+tau_e) + (1-lam)(tau_v+tau_y), tau_v = 1
    bs = (lam + (1 - lam) * ty) / d
    kappa = -2 / lam  # b_u / b_s = -a/(lam tau_e)
    return {"ty": ty, "bs": bs, "bu": kappa * bs, "D": d}


def clearing_residual_exact(lam: F, sd: F) -> tuple[F, F]:
    """Linear-in-(s,u) coefficients of lam x_I + (1-lam) x_U - u, with x_I, x_U from Lemma 1 and the conditional means
    of Proposition 1 (step 1 and 2). Both must be zero."""
    q = prop1_exact(lam, sd)
    bs, bu, ty = q["bs"], q["bu"], q["ty"]
    # informed: E[v|s,p] = s/2 (tau_e s/(tau_v+tau_e)), Var = 1/2; x_I = (tau_e s - (tau_v+tau_e) p)/a
    # p = bs s + bu u ; x_I = (s - 2 p)/2
    xi_s, xi_u = (F(1) - 2 * bs) / 2, (F(0) - 2 * bu) / 2
    # uninformed: y = p/bs = s + (bu/bs) u ; E[v|p] = ty y /(1+ty) ; x_U = (ty y - (1+ty) p)/a
    kappa = bu / bs
    xu_s = (ty * 1 - (1 + ty) * bs) / 2
    xu_u = (ty * kappa - (1 + ty) * bu) / 2
    res_s = lam * xi_s + (1 - lam) * xu_s
    res_u = lam * xi_u + (1 - lam) * xu_u - 1  # minus the noise supply u
    return res_s, res_u


def prop2_exact(lam: F, sd: F) -> F:
    """Corr(v,p)^2 from Cov(v,p) and Var(p) computed directly from the linear price (no closed form used)."""
    q = prop1_exact(lam, sd)
    bs, bu = q["bs"], q["bu"]
    var_v = F(1)
    var_s = F(1) + F(1)  # Var(s) = 1/tau_v + 1/tau_e = 2
    cov_vs = F(1)  # Cov(v, s) = Var(v)
    var_p = bs * bs * var_s + bu * bu * sd * sd  # u independent of s, Var(u) = sd^2
    cov_vp = bs * cov_vs
    return cov_vp * cov_vp / (var_v * var_p)


def lam_check(lam: F, sd: F) -> None:
    rs, ru = clearing_residual_exact(lam, sd)
    c2 = prop2_exact(lam, sd)
    closed = price_precision_exact(lam, sd) / (1 + price_precision_exact(lam, sd))
    print(f"prop1 clearing residual at lam={lam}, sd={sd}: s-coef={rs} u-coef={ru} ->", "ZERO" if rs == 0 and ru == 0 else "NONZERO")
    print(f"prop2 Corr^2 from moments = {float(c2):.15f}; tau_y/(1+tau_y) = {float(closed):.15f}; equal exactly: {c2 == closed}")


def gap_pieces(lam: float, sd: float, cost: float) -> tuple[float, float]:
    """Independent float evaluation with the closed forms of Propositions 1 and 3 (not the page or the grader code)."""
    ty = lam * lam / (lam * lam + 4 * sd * sd)
    d = lam * 2 + (1 - lam) * (1 + ty)
    bs = (lam + (1 - lam) * ty) / d
    bu = -2 * bs / lam
    omega = None  # Omega = Var(v-p) = V_U + S_U, computed from the price directly below
    var_p = bs * bs * 2 + bu * bu * sd * sd
    cov_vp = bs * 1.0  # Cov(v, p) = bs Cov(v, s) = bs Var(v) = bs
    omega = 1.0 + var_p - 2.0 * cov_vp  # Omega = Var(v - p)
    v_i = 0.5
    v_u = 1.0 / (1.0 + ty)
    fi = math.sqrt(v_i / omega)
    fu = math.sqrt(v_u / omega)
    return fu, fi


def gap(lam: float, sd: float, cost: float) -> float:
    if lam == 0.0:
        omega = 1.0 + 4 * sd * sd  # Var(v) + Var(p) at lam=0, with p = -2u (tau_v=1)
        fu = math.sqrt(1.0 / omega)
        fi = math.sqrt(0.5 / omega)
        return fu - math.exp(2 * cost) * fi
    fu, fi = gap_pieces(lam, sd, cost)
    return fu - math.exp(2 * cost) * fi


def bisect(sd: float, cost: float) -> float:
    if gap(0.0, sd, cost) <= 0.0:
        return 0.0
    if gap(1.0, sd, cost) >= 0.0:
        return 1.0
    lo, hi = 0.0, 1.0
    while hi - lo > 1e-15 * hi:
        mid = 0.5 * (lo + hi)
        if gap(mid, sd, cost) > 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def closed_form(sd: float, cost: float) -> float:
    t = 2 * math.exp(-4 * cost) - 1
    if t <= 0.0:
        return 0.0
    if t >= 1.0 / (1.0 + 4 * sd * sd):
        return 1.0
    return 2 * sd * math.sqrt(t / (1 - t))


def main() -> None:
    print("== exact rational checks (Prop 1 clearing, Prop 2) ==")
    for lam, sd in [(F(1, 2), F(3, 5)), (F(3, 10), F(7, 10)), (F(9, 10), F(1, 4)), (F(1), F(3, 2)), (F(1, 100), F(1, 1))]:
        lam_check(lam, sd)
    print("== Lemma 2 numeric: E[exp(-Z^2/(2V))] vs (V/(V+S))^(1/2), midpoint quadrature ==")
    for s_var, v_var in [(0.3, 1.0), (2.0, 0.5), (0.05, 3.0)]:
        h = 0.001
        tot = 0.0
        z = -12.0
        while z <= 12.0:
            tot += math.exp(-z * z / (2 * s_var)) / math.sqrt(2 * math.pi * s_var) * math.exp(-z * z / (2 * v_var)) * h
            z += h
        print(f"S={s_var} V={v_var}: numeric {tot:.10f} closed {math.sqrt(v_var / (v_var + s_var)):.10f}")
    print("== Prop 3 limit G(0+) closed form vs gap at tiny lam ==")
    for sd, cost in [(0.6, 0.13), (0.7, 0.14)]:
        g0_closed = (1 / 1 + 4 * sd * sd) ** -0.5  # placeholder replaced below
        tv, te, a = 1.0, 1.0, 2.0
        g0_formula = (1 / tv + a * a * sd * sd / (tv * tv)) ** -0.5 * (tv ** -0.5 - math.exp(a * cost) / (tv + te) ** 0.5)
        print(f"sd={sd} c={cost}: G(0+) closed {g0_formula:+.12f}; gap(1e-9) {gap(1e-9, sd, cost):+.12f}; gap(0) {gap(0.0, sd, cost):+.12f}")
    print("== gap values: independent Omega = Var(v-p) form vs the reference module's indifference_gap ==")
    import importlib.util
    spec = importlib.util.spec_from_file_location("ref_r6", "course/modules/E/E4/grader/reference.py")
    assert spec and spec.loader
    ref = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref)
    for sd, cost in [(0.6, 0.13), (0.7, 0.14), (0.5, 0.12), (0.75, 0.15)]:
        for lam in (0.1, 0.3, 0.5, 0.9, 1.0):
            mine = gap(lam, sd, cost)
            theirs = ref.indifference_gap(lam, sd, cost)
            print(f"sd={sd} c={cost} lam={lam}: independent {mine:+.12f} reference {theirs:+.12f} diff {mine - theirs:+.2e}")
    print("== Prop 4 closed form vs bisection on a 9-point grid and tiny noise ==")
    worst = 0.0
    for sd in (0.5, 0.625, 0.75):
        for cost in (0.12, 0.135, 0.15):
            b = bisect(sd, cost)
            c = closed_form(sd, cost)
            worst = max(worst, abs(b - c))
            print(f"sd={sd} c={cost}: bisect {b:.12f} closed {c:.12f} diff {b - c:+.2e}")
    print("worst |bisect - closed| on grid:", f"{worst:.3e}")
    print("== Prop 4 closed form vs bisection, small noise (relative) ==")
    for sd in (1e-6, 1e-9, 1e-12):
        b = bisect(sd, 0.13)
        c = closed_form(sd, 0.13)
        print(f"sd={sd}: rel diff {abs(b - c) / c:.3e}")
    print("== Prop 5 ratios and monotonicity on the grid ==")
    r1 = closed_form(0.625, 0.12) / closed_form(0.5, 0.12)
    r2 = closed_form(0.75, 0.12) / closed_form(0.5, 0.12)
    print(f"ratio 0.625/0.5 = {r1:.12f} (displayed 1.2501), 0.75/0.5 = {r2:.12f} (displayed 1.5000)")
    print("== box bounds ==")
    print(f"tau_bar(0.150) = {2 * math.exp(-0.6) - 1:.10f}; tau_bar(0.120) = {2 * math.exp(-0.48) - 1:.10f}")
    print(f"tau_y(1) at sd=0.75 = {1 / (1 + 4 * 0.75 ** 2):.10f}")
    inside = 0
    for i in range(22):
        for j in range(22):
            sd = 0.5 + 0.25 * i / 21.0
            cost = 0.12 + 0.03 * j / 21.0
            if gap(0.0, sd, cost) > 0.0 and gap(1.0, sd, cost) < 0.0:
                inside += 1
    print("box grid interior count:", inside, "of 484")
    print("== instance seeds 0..49: box, interior, distinct ==")
    import random

    pairs = []
    for seed in range(50):
        rng = random.Random(seed)
        sd = round(rng.uniform(0.5, 0.75), 3)
        cost = round(rng.uniform(0.12, 0.15), 3)
        pairs.append((sd, cost))
        assert 0.5 <= sd <= 0.75 and 0.12 <= cost <= 0.15
        t = 2 * math.exp(-4 * cost) - 1
        assert 0 < t < 1.0 / (1 + 4 * sd * sd), seed
    print("all 50 seeds inside the box with 0 < tau_bar < tau_y(1):", True)
    print("distinct (sd,cost) pairs over seeds 0..49:", len(set(pairs)))
    print("seeds 0..19 (sd, cost, lam*):")
    for seed in range(20):
        sd, cost = pairs[seed]
        print(f"  seed {seed}: sd={sd} c={cost} lam*={bisect(sd, cost):.10f}")


if __name__ == "__main__":
    main()


def lab_roots() -> None:
    """Lab 1 (sd 0.60, c 0.13) and Lab 2 (sd 0.70, c 0.14) numbers printed on project.html, recomputed independently."""
    for label, sd, cost in (("Lab 1", 0.60, 0.13), ("Lab 2", 0.70, 0.14)):
        lam = bisect(sd, cost)
        ty = lam * lam / (lam * lam + 4 * sd * sd)
        tau_bar = 2 * math.exp(-4 * cost) - 1
        print(f"{label}: lambda*={lam:.8f} tau_y={ty:.8f} tau_bar={tau_bar:.8f} informativeness={ty / (1 + ty):.8f} "
              f"b_u/b_s={-2 / lam:.8f} gap(0+)={gap(0.0, sd, cost):+.6f} gap(1)={gap(1.0, sd, cost):+.6f}")


lab_roots()
