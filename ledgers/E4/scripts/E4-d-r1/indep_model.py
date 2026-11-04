"""Independent re-derivation of the E4 project model (verifier code, stdlib only; written without reading solver code).

Method, distinct from the page's closed forms:
  1. For a candidate linear price p = bs*s + bu*u, compute the investors' conditional means and variances by
     Gaussian regression on the joint moments (no closed forms).
  2. Check market clearing as an identity in (s, u): lam*x_I + (1-lam)*x_U - u must vanish for every (s, u), i.e.
     both coefficients vanish. Use the closed-form (bs, bu) of Proposition 1 and report the residuals.
  3. Expected utilities by 1-D Simpson quadrature over the Gaussian law of the conditional-mean gap (not the
     closed form F_I, F_U), giving the gap, and the informativeness by the squared correlation from moments.
  4. Bisection on the gap with the page's boundary rule, compared to Proposition 4's closed form.
Usage: python -I ledgers/E4/scripts/E4-d-r1/indep_model.py
"""

import math
import random

A, TV, TE = 2.0, 1.0, 1.0


def gauss_expect_exp_quadratic(var_z: float, var_c: float, n: int = 4000, width: float = 14.0) -> float:
    """E[exp(-Z^2/(2 var_c))] for Z ~ N(0, var_z), by Simpson's rule on the standard-normal scale."""
    if var_z == 0.0:
        return 1.0
    sd = math.sqrt(var_z)
    h = 2 * width / n
    total = 0.0
    for i in range(n + 1):
        t = -width + i * h
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        total += w * math.exp(-0.5 * t * t) * math.exp(-(sd * t) ** 2 / (2 * var_c))
    total *= h / 3.0
    return total / math.sqrt(2 * math.pi)


def moments(bs: float, bu: float, sd: float) -> dict:
    """Joint moments of (v, s, p) for p = bs*s + bu*u, with s = v + eps, u ~ N(0, sd^2)."""
    var_v, var_s = 1 / TV, 1 / TV + 1 / TE
    var_p = bs * bs * var_s + bu * bu * sd * sd
    cov_sp = bs * var_s
    cov_vp = bs * var_v
    cov_vs = var_v
    return dict(var_p=var_p, cov_sp=cov_sp, cov_vp=cov_vp, cov_vs=cov_vs, var_s=var_s, var_v=var_v)


def informed_residual_terms(lam: float, bs: float, bu: float, sd: float) -> tuple[float, float, float]:
    """Return (coefficient of s, coefficient of p, conditional variance) of the informed demand x_I = a1*s + a2*p."""
    m = moments(bs, bu, sd)
    # E[v | s, p] = b' Sigma^{-1} (s, p)'; Sigma = [[var_s, cov_sp],[cov_sp, var_p]]
    det = m["var_s"] * m["var_p"] - m["cov_sp"] ** 2
    inv = [[m["var_p"] / det, -m["cov_sp"] / det], [-m["cov_sp"] / det, m["var_s"] / det]]
    b = [m["cov_vs"], m["cov_vp"]]
    gain = [b[0] * inv[0][0] + b[1] * inv[1][0], b[0] * inv[0][1] + b[1] * inv[1][1]]
    cond_var = m["var_v"] - (gain[0] * b[0] + gain[1] * b[1])
    # demand x = (E[v|F] - p) / (a Var(v|F)) with E[v|F] = gain . (s, p)
    a1 = gain[0] / (A * cond_var)
    a2 = (gain[1] - 1.0) / (A * cond_var)
    return a1, a2, cond_var


def uninformed_residual_terms(bs: float, bu: float, sd: float) -> tuple[float, float]:
    """x_U = c1 * p; returns (c1, conditional variance of v given p)."""
    m = moments(bs, bu, sd)
    gain = m["cov_vp"] / m["var_p"]
    cond_var = m["var_v"] - gain * m["cov_vp"]
    c1 = (gain - 1.0) / (A * cond_var)
    return c1, cond_var


def closed_form_price(lam: float, sd: float) -> tuple[float, float]:
    """Proposition 1, transcribed from the page formulas (not from the solver module)."""
    ty = lam * lam * TE * TE / (lam * lam * TE + A * A * sd * sd)
    d = lam * (TV + TE) + (1 - lam) * (TV + ty)
    bs = (lam * TE + (1 - lam) * ty) / d
    return bs, -A * bs / (lam * TE)


def clearing_residual(lam: float, sd: float) -> tuple[float, float]:
    """Coefficients of s and u in lam*x_I + (1-lam)*x_U - u, using the regression demands at the closed-form price."""
    bs, bu = closed_form_price(lam, sd)
    a1, a2, _ = informed_residual_terms(lam, bs, bu, sd)
    c1, _ = uninformed_residual_terms(bs, bu, sd)
    # x_I = a1 s + a2 p, x_U = c1 p, p = bs s + bu u
    coef_s = lam * (a1 + a2 * bs) + (1 - lam) * c1 * bs
    coef_u = lam * a2 * bu + (1 - lam) * c1 * bu - 1.0
    return coef_s, coef_u


def gap_quadrature(lam: float, sd: float, cost: float) -> float:
    """E[U_I] - E[U_U] by quadrature over the conditional-mean gaps (lam in (0,1]); lam = 1 uses the hypothetical
    uninformed agent who faces the price of the lam = 1 economy."""
    bs, bu = closed_form_price(lam, sd)
    m = moments(bs, bu, sd)
    a1, a2, cvi = informed_residual_terms(lam, bs, bu, sd)
    # conditional mean of v for informed minus price = (a1 s + a2 p) * a*cvi ... recompute directly
    det = m["var_s"] * m["var_p"] - m["cov_sp"] ** 2
    inv = [[m["var_p"] / det, -m["cov_sp"] / det], [-m["cov_sp"] / det, m["var_s"] / det]]
    b = [m["cov_vs"], m["cov_vp"]]
    gain = [b[0] * inv[0][0] + b[1] * inv[1][0], b[0] * inv[0][1] + b[1] * inv[1][1]]
    # m_I - p = gain0*s + (gain1 - 1)*p, a linear form in (s, u); its variance and the conditional variance
    q_s, q_p = gain[0], gain[1] - 1.0
    var_gap_I = (q_s + q_p * bs) ** 2 * m["var_s"] + 2 * (q_s + q_p * bs) * q_p * bu * 0.0
    # Var of q_s*s + q_p*(bs*s + bu*u) = (q_s + q_p bs)^2 var_s + (q_p bu)^2 sd^2 (s, u independent, cov(s,u)=0)
    var_gap_I = (q_s + q_p * bs) ** 2 * m["var_s"] + (q_p * bu) ** 2 * sd * sd
    f_i = gauss_expect_exp_quadratic(var_gap_I, cvi)
    # uninformed
    c_gain = m["cov_vp"] / m["var_p"]
    cvu = m["var_v"] - c_gain * m["cov_vp"]
    q_u = c_gain - 1.0
    var_gap_U = (q_u) ** 2 * m["var_p"]
    f_u = gauss_expect_exp_quadratic(var_gap_U, cvu)
    # E[U_I] = -exp(a c) f_i, E[U_U] = -f_u  (utility -exp(-a w) integrated; Lemma 1/2 of the page)
    return f_u - math.exp(A * cost) * f_i


def informativeness(lam: float, sd: float) -> float:
    if lam == 0.0:
        return 0.0
    bs, bu = closed_form_price(lam, sd)
    m = moments(bs, bu, sd)
    return m["cov_vp"] ** 2 / (m["var_v"] * m["var_p"])


def proposition4(sd: float, cost: float) -> float:
    t = (TV + TE) * math.exp(-2 * A * cost) - TV
    if t <= 0:
        return 0.0
    if t >= TE * TE / (TE + A * A * sd * sd):
        return 1.0
    return A * sd * math.sqrt(t / (TE * (TE - t)))


def independent_root(sd: float, cost: float) -> float:
    """Bisection on the quadrature gap with the page's boundary rule (tolerance 1e-12 relative)."""
    g0 = gap_quadrature(1e-9, sd, cost)  # the gap tends to its limit as lam -> 0
    g1 = gap_quadrature(1.0, sd, cost)
    if g0 <= 0:
        return 0.0
    if g1 >= 0:
        return 1.0
    lo, hi = 0.0, 1.0
    while hi - lo > 1e-12 * hi:
        mid = 0.5 * (lo + hi)
        if gap_quadrature(mid, sd, cost) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


if __name__ == "__main__":
    print("== 1. Proposition 1 clearing residuals (should be ~0) at sampled (lam, sd)")
    worst = 0.0
    for lam in (0.1, 0.3, 0.5, 0.7, 0.9, 1.0):
        for sd in (0.5, 0.6, 0.75):
            cs, cu = clearing_residual(lam, sd)
            worst = max(worst, abs(cs), abs(cu))
    print("max |residual| over 18 points:", f"{worst:.3e}")

    print("== 2. Lab 1 instance (sd 0.60, cost 0.13)")
    sd, c = 0.60, 0.13
    print("gap at 0 (1e-9 proxy):", f"{gap_quadrature(1e-9, sd, c):+.6f}", "gap at 1:", f"{gap_quadrature(1.0, sd, c):+.6f}")
    r = independent_root(sd, c)
    print("root:", f"{r:.8f}", "closed form:", f"{proposition4(sd, c):.8f}", "gap at root:", f"{gap_quadrature(r, sd, c):+.3e}")
    print("informativeness at root:", f"{informativeness(r, sd):.8f}")

    print("== 3. Lab 2 instance (sd 0.70, cost 0.14)")
    sd, c = 0.70, 0.14
    print("gap at 0:", f"{gap_quadrature(1e-9, sd, c):+.6f}", "gap at 1:", f"{gap_quadrature(1.0, sd, c):+.6f}")
    r = independent_root(sd, c)
    print("root:", f"{r:.8f}", "informativeness:", f"{informativeness(r, sd):.8f}")

    print("== 4. Lab 3 grid")
    worst_closed = 0.0
    for sd in (0.500, 0.625, 0.750):
        for c in (0.120, 0.135, 0.150):
            r = independent_root(sd, c)
            pi = informativeness(r, sd)
            cf = proposition4(sd, c)
            worst_closed = max(worst_closed, abs(r - cf))
            print(f"{sd:.3f} {c:.3f} lam={r:.6f} closed={cf:.6f} inf={pi:.6f} gap={gap_quadrature(r, sd, c):+.2e}")
    print("max |indep root - Prop 4 closed form| on grid:", f"{worst_closed:.2e}")
