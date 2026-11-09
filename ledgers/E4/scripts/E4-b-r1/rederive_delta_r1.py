from fractions import Fraction as F

# L06 Example 6.9 base instance (lesson values)
sv2, se2, a, lam, su2 = F(1), F(1), F(1), F(1, 2), F(1, 4)
tv, te = 1 / sv2, 1 / se2
kappa = a / (lam * te)
seta2 = se2 + kappa**2 * su2
taueta = 1 / seta2
taubar = lam * te + (1 - lam) * taueta
ths = taubar / (tv + taubar)
thu = kappa * ths
print("L06 kappa", kappa, "sig_eta2", seta2, "tau_eta", taueta, "tau_bar", taubar, "theta_s", ths, "theta_u", thu)
omega = sv2 / (sv2 + se2)
VI = sv2 * se2 / (sv2 + se2)
varp = ths**2 * (sv2 + se2) + thu**2 * su2
covvp = ths * sv2
b = covvp / varp
VU = sv2 - b * covvp
print("var_p", varp, "cov_vp", covvp, "b (E4-c119 slope)", b, "V_U (c271 posterior var)", VU)
s, u = F(1), F(0)
p = ths * s - thu * u
xI = (omega * s - p) / (a * VI)
xU = (b * p - p) / (a * VU)
print("price at (1,0)", p, "x_I (c120)", xI, "x_U (c220)", xU, "clearing residual", lam * xI + (1 - lam) * xU - u)
# alternative theta_s = 1/2, theta_u unchanged (c123): recompute b, V_U, residual
ths2 = F(1, 2)
varp2 = ths2**2 * (sv2 + se2) + thu**2 * su2
covvp2 = ths2 * sv2
b2 = covvp2 / varp2
VU2 = sv2 - b2 * covvp2
p2 = ths2 * s - thu * u
xI2 = (omega * s - p2) / (a * VI)
xU2 = (b2 * p2 - p2) / (a * VU2)
print("alt residual at (1,0) (c123, expected -9/85):", lam * xI2 + (1 - lam) * xU2 - u)
# Remark 6.10 noise variance and c126/c244 statements
print("sigma_eta^2 (c126 expects 2):", seta2, "sigma_eta^2 >= sigma_eps^2 for sigma_u^2=0,1/4,7:", [se2 + kappa**2 * x >= se2 for x in (F(0), su2, F(7))])
print("Var(v|p) < sigma_v^2 (c129):", VU < sv2, "1/(tau_v+tau_eta) (c117/c271):", 1 / (tv + taueta))
print("c116 E[v|p] coefficient tau_eta/(theta_s (tau_v+tau_eta)) =", taueta / (ths * (tv + taueta)), "equals b:", taueta / (ths * (tv + taueta)) == b)
print("c111 omega", omega, "V_I", VI, "omega/V_I == tau_e", omega / VI == te)

# L05 Proposition 2.2 closed form at the parameter sets of Lab 1 (c090, c219, c263)
for name, (al, be, vs, de) in {"BASE": (F(10), F(2), F(1, 2), F(3, 4)), "EQUAL (c219)": (F(10), F(2), F(2), F(3, 4))}.items():
    c0 = al / (be + vs)
    c1 = -de / (be + vs)
    r0 = (al - vs * c0) / be - c0
    r1 = -(vs * c1 + de) / be - c1
    print("L05", name, "c0*", c0, "c1*", c1, "residuals", r0, r1)
