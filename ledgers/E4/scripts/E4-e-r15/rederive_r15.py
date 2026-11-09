"""Verifier r15 (E4 cards slice): exact re-derivation of the numbers in the lines changed since 8e5751c."""
from fractions import Fraction as F
import math

# L03 R2 (Example 2.11 endowment): pi=(1/2,1/4,1/4), e1=(3,4,1), e2=(1,4,3)
pi = (F(1, 2), F(1, 4), F(1, 4))
e1 = (F(3), F(4), F(1))
e2 = (F(1), F(4), F(3))
def mrs(pi, x, s, t):  # log utility: u'(x)=1/x
    return (pi[s] / x[s]) / (pi[t] / x[t])
print("L03 MRS^1_12 at endowment =", mrs(pi, e1, 0, 1))   # expect 8/3
print("L03 MRS^2_12 at endowment =", mrs(pi, e2, 0, 1))   # expect 8
print("L03 R2 claimed '3/8' equals MRS^1_12 ?", F(3, 8) == mrs(pi, e1, 0, 1))
# compensation needed by agent 1 to give up one unit of state 1 at the same utility = MRS_12
print("L03 R2 compensation per unit of state 1 (agent 1) =", mrs(pi, e1, 0, 1))
# Derivatives of the trade in R2
d1 = pi[0] * F(-1, 3) + pi[1] * F(1, 1)   # d/de U1(y1) at eps=0: y1=(3-e,4+4e,1)
d2 = pi[0] * F(1, 1) + pi[1] * F(-1, 1)   # d/de U2(y2) at eps=0: y2=(1+e,4-4e,3)
print("R2 dU1/de =", d1, " dU2/de =", d2)
# Utility change at the grid witness (2,4,3)/(2,4,1): both equal (1/4) ln(4/3)
g1 = pi[0] * math.log(F(2, 3)) if False else None
du1 = float(pi[0]) * math.log(2 / 3) + float(pi[2]) * math.log(3)
du2 = float(pi[0]) * math.log(2) + float(pi[2]) * math.log(1 / 3)
print("grid witness dU1 =", round(du1, 12), " dU2 =", round(du2, 12), " (1/4)ln(4/3) =", round(0.25 * math.log(4 / 3), 12))

# L06 base instance (Example 6.9) and Problems M1-M3, R1 residual
sv2, se2, a, lam, su2 = F(1), F(1), F(1), F(1, 2), F(1, 4)
tv, te = 1 / sv2, 1 / se2
kappa = a * se2 / lam
seta2 = se2 + kappa**2 * su2
taueta = 1 / seta2
taubar = lam * te + (1 - lam) * taueta
ths = taubar / (tv + taubar)
thu = kappa * ths
print("L06 kappa, sig_eta2, tau_eta, taubar, theta_s, theta_u =", kappa, seta2, taueta, taubar, ths, thu)
varp = ths**2 * (sv2 + se2) + thu**2 * su2
covvp = ths * sv2
b = covvp / varp
VU = sv2 - b * covvp
print("L06 Var(p), Cov(v,p), b, V_U =", varp, covvp, b, VU)
# residual at (s,u)=(1,0) with theta_s=1/2, theta_u=6/7 (Lab 1 Part D)
ts_alt, tu = F(1, 2), F(6, 7)
varp_alt = ts_alt**2 * (sv2 + se2) + tu**2 * su2
b_alt = ts_alt * sv2 / varp_alt
VU_alt = sv2 - b_alt * ts_alt * sv2
p_alt = ts_alt * 1 - tu * 0
omega = sv2 / (sv2 + se2)
VI = sv2 * se2 / (sv2 + se2)
xI = (omega * 1 - p_alt) / (a * VI)
xU = (b_alt * p_alt - p_alt) / (a * VU_alt)
print("L06 alt residual at (1,0) =", lam * xI + (1 - lam) * xU, " expect -9/85")
# Step 3 identity: residual (lam*tau_e - Q theta_s) s + (Q theta_u - a) u vanishes at (1,0),(0,1) only if Q theta_s = lam tau_e and Q theta_u = a
Q = tv + taubar - (1 - lam) * taueta / ths
print("L06 Q*theta_s - lam*tau_e =", Q * ths - lam * te, "  Q*theta_u - a =", Q * thu - a)
# M1-M3 (L06 Problem set)
a2 = F(2)
kap = a2 * F(1) / F(1, 2); se = F(1) + kap**2 * F(1, 4); tau_e = 1 / se
tb = F(1, 2) * 1 + F(1, 2) * tau_e; tsm = tb / (1 + tb); tum = kap * tsm
print("M1 kappa, sig_eta2, tau_eta, taubar, theta_s, theta_u =", kap, se, tau_e, tb, tsm, tum)
