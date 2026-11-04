"""Independent re-derivation of the numbers quoted in E4 L07 and L08 (verifier, round 1).

Written from the page formulas, not from the lab twins. Run with the checkout's .venv python from the checkout root:
    .venv/bin/python ledgers/E4/scripts/E4-c-r1/recheck_l07_l08.py
"""

from __future__ import annotations

import math
from fractions import Fraction as F

import numpy as np


def sigma_eta2(sig_e2: F, a: F, lam: F, sd: F) -> F:
    kappa = a * sig_e2 / lam  # L07 Prop 7.6 / L08 Prop 3.1
    return sig_e2 + kappa * kappa * sd * sd


def rho2_closed(sig_v2: F, sig_e2: F, a: F, lam: F, sd: F) -> F:
    return sig_v2 / (sig_v2 + sigma_eta2(sig_e2, a, lam, sd))


def rho2_moments(sig_v2: F, sig_e2: F, a: F, lam: F, sd: F) -> tuple[F, F]:
    tau_v, tau_e = 1 / sig_v2, 1 / sig_e2
    kappa = a * sig_e2 / lam
    s_eta2 = sig_e2 + kappa * kappa * sd * sd
    tau_eta = 1 / s_eta2
    A = lam * tau_e + (1 - lam) * tau_eta
    theta_s = A / (tau_v + A)
    theta_u = kappa * theta_s
    cov = theta_s * sig_v2
    var_p = theta_s * theta_s * (sig_v2 + sig_e2) + theta_u * theta_u * sd * sd
    return cov * cov / (sig_v2 * var_p), var_p


def l07() -> None:
    one = F(1)
    print("L07 Part A rho2 (moments, closed):", rho2_moments(one, one, one, F(1, 2), F(1, 2))[0], rho2_closed(one, one, one, F(1, 2), F(1, 2)))
    for sd in (F(1, 4), F(1, 2), F(1), F(2), F(4)):
        r, vp = rho2_moments(one, one, one, F(1, 2), sd)
        print(f"L07 B sd={sd} rho2={r} var_p={vp} float var_p={float(vp):.6f}")
    for lam in (F(1, 4), F(1, 2), F(3, 4)):
        print("L07 C lam", lam, "rho2", rho2_closed(one, one, one, lam, F(1, 2)))
    for a in (F(1, 2), F(1), F(2)):
        print("L07 D a", a, "rho2", rho2_closed(one, one, a, F(1, 2), F(1, 2)))
    print("L07 E benchmark", one / (one + one), "tiny", rho2_closed(one, one, one, F(1, 2), F(1, 100)), float(rho2_closed(one, one, one, F(1, 2), F(1, 100))))
    # Remark 7.9 / misconception 1: var_p rises across the sd sweep
    vps = [rho2_moments(one, one, one, F(1, 2), sd)[1] for sd in (F(1, 4), F(1, 2), F(1), F(2), F(4))]
    print("L07 var_p increasing:", all(vps[i] < vps[i + 1] for i in range(4)))
    # E1: 1/3 - 0.330625 and ratio to tolerance 0.02
    d = 1 / 3 - 0.330625
    print("L07 E1 diff", d, "in tol units", d / 0.02)
    # R2: sd at half benchmark, c = a^2 se^4 / lam^2 = 4 at stated values
    c = F(1) * F(1) / F(1, 4)
    print("L07 R2 c", c, "sd", math.sqrt(2 / float(c)))
    # E2: sigma_u for rho2 = 1/4 at sig_v2=sig_e2=1, a=1, lam=1/2 : 1/(1+3)=1/4 requires eta2=3
    print("L07 E2 sigma_u^2 needed", (3 - 1) / 4, "sigma_u", math.sqrt(0.5))
    # Proposition 7.7 sign checks on a grid (floats)
    grid_ok = True
    for sd in np.linspace(0.05, 5, 60):
        for lam in np.linspace(0.05, 0.95, 40):
            for a in np.linspace(0.1, 3, 20):
                r = lambda sd_, lam_, a_: 1.0 / (1.0 + (1.0 + a_ * a_ * 1.0 / lam_**2 * 1.0 * sd_ * sd_ * 0 + a_ * a_ / lam_**2 * sd_ * sd_))
                # general form: rho2 = s_v/(s_v + s_e + c*sd^2), s_v=s_e=1, c=a^2/lam^2 (s_e^4=1)
                base = r(sd, lam, a)
                grid_ok &= r(sd * 1.01, lam, a) < base and r(sd, lam, a * 1.01) < base and r(sd, lam * 1.01, a) > base
    print("L07 Prop 7.7 sign grid (sd, a decreasing; lam increasing):", grid_ok)


def gain_closed(lam: F | None, var_u: F, sig_v2: F = F(1), sig_e2: F = F(1), a: F = F(2)) -> float:
    """G(lam) of L08 Definition 4.3 from the page formulas; lam None means lam = 0 (Lemma 4.5)."""
    if lam is None:
        q = sig_v2 / sig_e2
        X0 = a * a * var_u * sig_v2
        return math.log(1 + float(q)) / (2 * float(a))
    tau_v, tau_e = 1 / sig_v2, 1 / sig_e2
    kappa = a * sig_e2 / lam
    tau_eta = 1 / (sig_e2 + kappa * kappa * var_u)
    A = lam * tau_e + (1 - lam) * tau_eta
    beta = A / (tau_v + A)
    b_s = tau_e / (tau_v + tau_e)
    b_y = tau_eta / (tau_v + tau_eta)
    V_I = 1 / (tau_v + tau_e)
    V_U = 1 / (tau_v + tau_eta)
    var_DI = float((b_s - beta) ** 2 * (sig_v2 + sig_e2) + (kappa * beta) ** 2 * var_u)
    var_DU = float((b_y - beta) ** 2 * (sig_v2 + 1 / tau_eta))
    return math.log((1 + var_DI / float(V_I)) / (1 + var_DU / float(V_U))) / (2 * float(a))


def l08_closed() -> None:
    print("L08 G(0) =", gain_closed(None, F(1)), "ln2/4 =", math.log(2) / 4)
    print("L08 G(1) =", gain_closed(F(1), F(1)), "ln(5/3)/4 =", math.log(5 / 3) / 4)
    print("L08 G(0.5) =", gain_closed(F(1, 2), F(1)))
    print("L08 G(1e-6)-G(0) =", gain_closed(F(1, 10**6), F(1)) - gain_closed(None, F(1)))
    tau_v, tau_e = 1.0, 1.0
    lam = 0.5
    kappa = 2 * 1.0 / lam
    tau_eta = 1 / (1 + kappa * kappa)
    A = lam * tau_e + (1 - lam) * tau_eta
    beta = A / (tau_v + A)
    b_y = tau_eta / (tau_v + tau_eta)
    print("L08 b_y/beta at lam=1/2 =", b_y / beta)
    print("L08 Corr^2 at lam=1/2 =", b_y, " (quiz expects 1/18 =", 1 / 18, ")")


def bisect_root(cost: float) -> float:
    lo, hi = 0.0, 1.0
    g = lambda x: gain_closed(F(x).limit_denominator(10**15) if x > 0 else None, F(1)) - cost
    while hi - lo > 1e-14:
        mid = 0.5 * (lo + hi)
        if g(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def l08_roots() -> None:
    printed = {0.13: 0.965625410, 0.14: 0.815032329, 0.15: 0.657828572, 0.16: 0.480567912, 0.17: 0.231615819}
    for cost, pv in printed.items():
        r = bisect_root(cost)
        print(f"L08 cost {cost}: independent root {r:.9f} page {pv:.9f} diff {abs(r - pv):.2e}")


def l08_mc(lam: float = 0.5, n: int = 2_000_000, seed: int = 1) -> None:
    """Monte Carlo of the expected utilities of Proposition 4.2 with the posteriors of Corollary 2.4 (independent check)."""
    rng = np.random.default_rng(seed)
    a, sv2, se2, su2, vbar = 2.0, 1.0, 1.0, 1.0, 0.0
    v = rng.normal(0, 1, n)
    e = rng.normal(0, 1, n)
    u = rng.normal(0, 1, n)
    s = v + e
    tau_v, tau_e = 1 / sv2, 1 / se2
    kappa = a * se2 / lam
    tau_eta = 1 / (se2 + kappa**2 * su2)
    A = lam * tau_e + (1 - lam) * tau_eta
    beta = A / (tau_v + A)
    p = (1 - beta) * vbar + beta * s - kappa * beta * u
    V_I = 1 / (tau_v + tau_e)
    V_U = 1 / (tau_v + tau_eta)
    mS = vbar + (sv2 / (sv2 + se2)) * (s - vbar)
    yv = (p - (1 - beta) * vbar) / beta
    mP = vbar + (tau_eta / (tau_v + tau_eta)) * (yv - vbar)
    # conditional draws of v given the info sets (Gaussian, independent of realised v)
    cI = mS + math.sqrt(V_I) * rng.normal(0, 1, n)
    cU = mP + math.sqrt(V_U) * rng.normal(0, 1, n)
    xI = (mS - p) / (a * V_I)
    xU = (mP - p) / (a * V_U)
    # utility of the optimal demand, evaluated on the conditional draw of v
    W0 = 0.0
    EUI = np.mean(-np.exp(-a * (W0 - 0.0 + xI * (cI - p))))
    EUU = np.mean(-np.exp(-a * (W0 + xU * (cU - p))))
    print("L08 MC EU_I", EUI, "EU_U", EUU, "closed-form G(lam)", gain_closed(F(lam).limit_denominator(100), F(1)))
    # the cost at which MC expected utilities are equal, with the same draws: EU_I(c) = -exp(a c) * EUI_0
    # EU_I(c) = exp(a c) * EUI  (since -exp(-a(W0-c)) = -exp(-aW0) exp(ac)); equality with EUU gives c = ln(EUU/EUI)/a
    c_star = math.log(EUU / EUI) / a
    print("L08 MC indifference cost", c_star)


if __name__ == "__main__":
    l07()
    l08_closed()
    l08_roots()
    l08_mc()
