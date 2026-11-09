"""Round 18: analytic check of the v17_02 discrepancy. For the reference fraction lam (interior), the mutant reports
Omega(beta_m)^(-1/2) H(lam) and the oracle/reference gap at lam is Omega(beta_r)^(-1/2) H(lam), where
H(lam) = V_U^(1/2) - e^{ac} V_I^(1/2) depends on lam only through tau_y(lam). So the discrepancy is
|H(lam)| * |Omega(beta_m)^(-1/2) - Omega(beta_r)^(-1/2)|. The bisection leaves lam within 0.5e-12*high of lam*,
so the worst discrepancy is bounded by about 0.5e-12 * lam* * |H'(lam*)| * |Delta|. This scan maximises that bound
over the interior region (0 < cbar < tau_y(1)) and checks the identity numerically against the reference."""
import math
import sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/scratch-E4-d-r18/probe")
import solver as ref

A, TV, TE = 2.0, 1.0, 1.0
P = TV + TE

def ty(lam, sd):
    return lam * lam * TE * TE / (lam * lam * TE + A * A * sd * sd)

def omega(beta, lam, sd):
    # Var(v - p) for p = beta*s + b_u*u, b_u = -a beta/(lam tau_e); equals V_I + var_gap of the solver
    bu = -A * beta / (lam * TE)
    return 1.0 / P + (TE / P - beta) ** 2 * (1.0 / TV + 1.0 / TE) + bu * bu * sd * sd

def beta_ref(lam, sd):
    return ref.price_coefficients(lam, sd)[0]

def beta_mut(lam, sd):
    t = ty(lam, sd)
    den = lam * (TV + TE) + (1.0 - lam) * (TV + t)
    return (lam * TE) / den

def H(lam, sd, c):
    t = ty(lam, sd)
    return (TV + t) ** -0.5 - math.exp(A * c) * P ** -0.5

def discrepancy(lam, sd, c):
    return abs(H(lam, sd, c)) * abs(omega(beta_mut(lam, sd), lam, sd) ** -0.5 - omega(beta_ref(lam, sd), lam, sd) ** -0.5)

# 1. identity check: reference gap equals Omega(beta_ref)^(-1/2) H, and mutant gap equals Omega(beta_mut)^(-1/2) H
import random
random.seed(7)
mx = 0.0
for _ in range(300):
    sd = math.exp(random.uniform(math.log(1e-3), math.log(0.6)))
    c = random.uniform(0.0, 0.3)
    lam = random.uniform(0.05, 0.95)
    g_ref = ref.indifference_gap(lam, sd, c)
    g_id = omega(beta_ref(lam, sd), lam, sd) ** -0.5 * H(lam, sd, c)
    mx = max(mx, abs(g_ref - g_id) / max(1.0, abs(g_ref)))
print("identity max rel err reference gap vs Omega^-1/2 H:", mx)

# 2. scan the bound over the interior region
best = (0.0, None)
count = 0
for ic in range(0, 401):
    c = 0.3465 * ic / 400.0
    if c <= 0:
        continue
    cb = (TV + TE) * math.exp(-2 * A * c) - TV
    if cb <= 0:
        continue
    smax = math.sqrt((1.0 / cb - 1.0) / 4.0) if cb < 1 else 1.0
    for isd in range(0, 801):
        sd = 10 ** (-50 + (math.log10(smax) + 50) * isd / 800.0)
        if not (cb < 1.0 / (1.0 + 4 * sd * sd)):
            continue
        lam = A * sd * math.sqrt(cb / (TE * (TE - cb)))
        if not (0.0 < lam < 1.0):
            continue
        count += 1
        h = 1e-9 * lam
        dH = (H(lam + h, sd, c) - H(lam - h, sd, c)) / (2 * h)
        D = omega(beta_mut(lam, sd), lam, sd) ** -0.5 - omega(beta_ref(lam, sd), lam, sd) ** -0.5
        bound = 0.5e-12 * lam * abs(dH) * abs(D)
        if bound > best[0]:
            best = (bound, (sd, c, lam, dH, D))
print("interior grid points", count)
print("max bound 0.5e-12*lam*|H'|*|Delta| =", best[0], "at (sd, c, lam, H', Delta) =", best[1])
