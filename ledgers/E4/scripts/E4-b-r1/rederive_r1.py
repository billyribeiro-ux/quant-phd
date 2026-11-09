# Exact re-derivation of the L06 noisy-REE algebra changed in this delta (Lemma 6.3, Lemma 6.4, Prop 6.7 Step 3, Cor 6.8, Example 6.9).
import random
from fractions import Fraction as F

def model(sv2, se2, a, lam, su2, th_s, th_u):
    # price p = th_s s - th_u u; Var(p), Cov(v,p) from A1 (v, eps, u independent, mean zero)
    varp = th_s**2 * (sv2 + se2) + th_u**2 * su2
    covvp = th_s * sv2
    b = covvp / varp
    VU = sv2 - b * covvp
    omega = sv2 / (sv2 + se2)
    VI = sv2 * se2 / (sv2 + se2)
    def residual(s, u):
        p = th_s * s - th_u * u
        xI = (omega * s - p) / (a * VI)          # Lemma 6.2 + 6.3
        xU = (b * p - p) / (a * VU)              # Lemma 6.2 + 6.4 (Remark 6.5)
        return lam * xI + (1 - lam) * xU - u     # A4 residual
    return residual, dict(varp=varp, b=b, VU=VU, omega=omega, VI=VI)

def closed(sv2, se2, a, lam, su2):
    tau_v, tau_e = 1 / sv2, 1 / se2
    kappa = a / (lam * tau_e)
    s_eta2 = se2 + kappa**2 * su2
    tau_eta = 1 / s_eta2
    taubar = lam * tau_e + (1 - lam) * tau_eta
    ths = taubar / (tau_v + taubar)
    thu = kappa * ths
    return ths, thu, kappa, s_eta2, tau_eta, taubar

rng = random.Random(20261109)
def rq():
    return F(rng.randint(1, 40), rng.randint(1, 40))

bad = []
trials = 0
for _ in range(400):
    sv2, se2, a, su2 = rq(), rq(), rq(), rq()
    lam = F(rng.randint(1, 99), 100)
    ths, thu, kappa, s_eta2, tau_eta, taubar = closed(sv2, se2, a, lam, su2)
    R, info = model(sv2, se2, a, lam, su2, ths, thu)
    trials += 1
    # (1) closed form clears the market at every (s,u) on a grid (linear residual, so 4 corner-ish points suffice; check a grid too)
    pts = [(F(s), F(u)) for s in (-2, -1, 0, 1, 2, 3) for u in (-2, -1, 0, 1, 2, 3)]
    if any(R(s, u) != 0 for s, u in pts):
        bad.append(("closed form does not clear", sv2, se2, a, lam, su2))
    # (2) residual is linear with no constant term: R(0,0)=0 and R(s,u)=R(1,0)*s+R(0,1)*u
    if R(F(0), F(0)) != 0: bad.append(("constant term",))
    for s, u in [(F(2), F(-3)), (F(5, 7), F(11, 3))]:
        if R(s, u) != R(F(1), F(0)) * s + R(F(0), F(1)) * u:
            bad.append(("not linear", s, u))
    # (3) Step 3 coefficient identities: Q th_s = lam tau_eps and Q th_u = a with Q from the proof
    tau_v, tau_e = 1 / sv2, 1 / se2
    Q = tau_v + taubar - (1 - lam) * tau_eta / ths
    if Q * ths != lam * tau_e or Q * thu != a:
        bad.append(("step3 identity", sv2, se2, a, lam, su2))
    # (4) Corollary 6.8 slope and posterior variance
    if info["b"] != tau_eta / (ths * (tau_v + tau_eta)) or info["VU"] != 1 / (tau_v + tau_eta):
        bad.append(("cor 6.8", sv2, se2, a, lam, su2))
    # (5) Lemma 6.3 variance identity sigma_v^2 (1 - omega) = V_I, and 1/V_I = tau_v + tau_e
    if info["VI"] != sv2 * (1 - info["omega"]) or 1 / info["VI"] != tau_v + tau_e:
        bad.append(("lemma 6.3", sv2, se2))
    # (6) Step 3 pointwise: at (1,0) and (0,1) the residual is zero exactly at the closed form (uniqueness of the two evaluations)
    if R(F(1), F(0)) != 0 or R(F(0), F(1)) != 0:
        bad.append(("pointwise", sv2, se2, a, lam, su2))
print("trials", trials, "failures", len(bad))
for b in bad[:10]:
    print("FAIL", b)

# Example 6.9 base instance
sv2, se2, a, lam, su2 = F(1), F(1), F(1), F(1, 2), F(1, 4)
ths, thu, kappa, s_eta2, tau_eta, taubar = closed(sv2, se2, a, lam, su2)
R, info = model(sv2, se2, a, lam, su2, ths, thu)
print("Example 6.9:", dict(kappa=kappa, sigma_eta2=s_eta2, tau_eta=tau_eta, taubar=taubar, theta_s=ths, theta_u=thu))
print("  varp", info["varp"], "b", info["b"], "VU", info["VU"], "VI", info["VI"], "omega", info["omega"])
print("  xI(1,0)", (info["omega"] * 1 - ths) / (a * info["VI"]), "xU(1,0)", (info["b"] * ths - ths) / (a * info["VU"]), "R(1,0)", R(F(1), F(0)))
print("  rho2 = tau_eta/(tau_v+tau_eta) =", tau_eta / (1 / sv2 + tau_eta))
# Alternative slope theta_s = 1/2 with theta_u = 6/7 unchanged: residual at (1,0) (card c123 / lab Part D)
Ra, _ = model(sv2, se2, a, lam, su2, F(1, 2), F(6, 7))
print("  alt residual(1,0) theta_s=1/2:", Ra(F(1), F(0)))
