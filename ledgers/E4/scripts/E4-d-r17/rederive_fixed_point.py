"""Round 17 independent re-derivation (verifier): the linear price is found by a numerical fixed point on the
clearing condition, not by the closed forms of the page. For each (lam, sigma, cost):
  - informed posterior: m_I = tau_e s/(tau_v+tau_e), V_I = 1/(tau_v+tau_e);
  - uninformed observe y = p/b_s = s + kappa u, precision of (eps + kappa u) is tau_y = 1/(1/tau_e + kappa^2 sigma^2),
    m_U = tau_y y/(tau_v+tau_y), V_U = 1/(tau_v+tau_y);
  - demands x = (m - p)/(a V); clearing lam x_I + (1-lam) x_U = u is linear in (s, u); its two coefficients
    are solved as a 2x2 linear system for (b_s, b_u) at the current kappa, and kappa is iterated to a fixed point;
  - Omega = Var(v - p) = V + Var(m - p) (Lemma 3 of the page), Var(m - p) computed from the coefficients;
  - E[U_I] = -exp(a c) sqrt(V_I/Omega') with Omega' = V_I + Var(m_I - p) (Lemma 2 applied to the informed posterior),
    E[U_U] = -sqrt(V_U/Omega'') with Omega'' = V_U + Var(m_U - p);
  - the informed fraction is the zero of G = E[U_I] - E[U_U] found by bisection on (0, 1], with the boundary rule.
Prints the numbers the page's labs state, to be compared by hand against the page and the twins."""
import math

A, TV, TE = 2.0, 1.0, 1.0


def solve_linear_price(lam, sd, kappa_iter=500):
    kappa = 0.0
    for _ in range(kappa_iter):
        ty = 1.0 / (1.0 / TE + kappa * kappa * sd * sd) if lam > 0 else 0.0
        # clearing: lam*(b_s s - ...) -- write x_I, x_U as linear functions of (s, u) with p = bs*s + bu*u
        # x_I = (TE/(TV+TE) s - p) / (A VI),  VI = 1/(TV+TE)
        # x_U = (mU - p)/(A VU),  mU = ty (s + kappa u)/(TV+ty),  VU = 1/(TV+ty)
        VI = 1.0 / (TV + TE)
        VU = 1.0 / (TV + ty)
        # coefficients on s and u of lam*x_I + (1-lam)*x_U - u = 0, unknowns bs, bu
        # x_I = [ (TE/(TV+TE)) - bs ]/(A VI) s + [ -bu ]/(A VI) u
        # x_U = [ ty/(TV+ty) - bs ]/(A VU) s + [ ty kappa/(TV+ty) - bu ]/(A VU) u
        # Equations: s-coefficient = 0 and u-coefficient = 1 (since the u term of the sum must equal u)
        a11 = lam / (A * VI) * (-1.0) + (1 - lam) / (A * VU) * (-1.0)  # coefficient of bs in s-eq (from -bs terms)
        # Write the s-equation and u-equation as linear in (bs, bu):
        # s-eq: lam*TE/((TV+TE) A VI) + (1-lam)*ty/((TV+ty) A VU) - bs*(lam/(A VI) + (1-lam)/(A VU)) = 0
        c_s = lam * (TE / (TV + TE)) / (A * VI) + (1 - lam) * (ty / (TV + ty)) / (A * VU)
        k_s = lam / (A * VI) + (1 - lam) / (A * VU)
        bs = c_s / k_s
        # u-eq: lam*(-bu)/(A VI) + (1-lam)*(ty*kappa/(TV+ty) - bu)/(A VU) = 1
        # with bu = kappa*bs (kappa is the current guess), solve for bu directly:
        bu = (1.0 - (1 - lam) * (ty * kappa / (TV + ty)) / (A * VU)) / (-(lam / (A * VI)) - (1 - lam) / (A * VU))
        new_kappa = bu / bs
        if abs(new_kappa - kappa) < 1e-15:
            kappa = new_kappa
            break
        kappa = new_kappa
    ty = 1.0 / (1.0 / TE + kappa * kappa * sd * sd)
    return bs, bu, ty


def gap(lam, sd, cost):
    if lam == 0.0:
        raise ValueError
    bs, bu, ty = solve_linear_price(lam, sd)
    VI = 1.0 / (TV + TE)
    VU = 1.0 / (TV + ty)
    # Var(m_I - p): m_I - p = (TE/(TV+TE)) s - bs s - bu u
    var_mi_p = (TE / (TV + TE) - bs) ** 2 * (1.0 / TV + 1.0 / TE) + bu * bu * sd * sd
    # Var(m_U - p): m_U = ty (bs s ... ) use y = p/bs: m_U = ty*y/(TV+ty), y = p/bs
    # m_U - p = p (ty/(bs (TV+ty)) - 1)
    var_p = bs * bs / (TV + TE) + 0.0  # placeholder, replaced below
    var_s = 1.0 / TV + 1.0 / TE
    var_p = bs * bs * var_s + bu * bu * sd * sd
    var_mu_p = (ty / (TV + ty) / bs - 1.0) ** 2 * var_p
    omega_i = VI + var_mi_p
    omega_u = VU + var_mu_p
    uI = -math.exp(A * cost) * math.sqrt(VI / omega_i)
    uU = -math.sqrt(VU / omega_u)
    return uI - uU, bs, bu, ty


def fraction(sd, cost):
    g0 = None
    lo, hi = 1e-300, 1.0
    g1 = gap(1.0, sd, cost)[0]
    if g1 >= 0:
        return 1.0
    lo_lam, hi_lam = 1e-12, 1.0
    # gap at small lambda
    for _ in range(200):
        mid = 0.5 * (lo_lam + hi_lam)
        if gap(mid, sd, cost)[0] > 0:
            lo_lam = mid
        else:
            hi_lam = mid
    return 0.5 * (lo_lam + hi_lam)


if __name__ == "__main__":
    for sd, c, label in [(0.60, 0.13, "lab1"), (0.70, 0.14, "lab2")]:
        lam = fraction(sd, c)
        g, bs, bu, ty = gap(lam, sd, c)
        ti = (TV + TE) * math.exp(-2 * A * c) - TV
        print(label, "lambda* %.8f" % lam, "gap %+.3e" % g, "bu/bs %.8f" % (bu / bs), "tau_y %.8f" % ty,
              "tau_bar %.8f" % ti, "informativeness %.8f" % (ty / (TV + ty)))
    for sd in (0.500, 0.625, 0.750):
        for c in (0.120, 0.135, 0.150):
            lam = fraction(sd, c)
            ty = 1.0 / (1.0 / TE + 0)  # placeholder not used
            g, bs, bu, ty = gap(lam, sd, c)
            print("grid sd=%.3f c=%.3f lambda*=%.4f informativeness=%.4f gap=%+.2e" % (sd, c, lam, ty / (TV + ty), g))
