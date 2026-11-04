"""E4-b round 3 checks on the L06 twin (standard library only; run with python -I).

1. Residual of A4 is additive and homogeneous in (s, u) with the price substituted (no constant term).
2. At a FIXED price p (not substituted), the residual has a nonzero (s, u)-constant term (refutes the page sentence).
3. Dimension exponents of kappa and theta_u (money M, asset A), against the docstring units.
"""
from fractions import Fraction
import random
import sys

TWIN = "tests/labs/E4/lab-E4-L06-1.py"
src = open(TWIN, encoding="utf-8").read()
body = src.rsplit("\nmain()", 1)[0]  # drop the top-level call so only definitions run
ns: dict[str, object] = {"__name__": "twin_defs"}
exec(compile(body, TWIN, "exec"), ns)
residual = ns["residual"]
closed_form = ns["closed_form"]
SIG_V2, SIG_E2, A, LAM, SIG_U2 = Fraction(1), Fraction(1), Fraction(1), Fraction(1, 2), Fraction(1, 4)
price = closed_form(SIG_V2, SIG_E2, A, LAM, SIG_U2)
ts, tu = price.theta_s, price.theta_u

def R(s, u):
    return residual(s, u, ts, tu, SIG_V2, SIG_E2, A, LAM, SIG_U2)

rng = random.Random(1)
ok_add = ok_hom = True
for _ in range(200):
    s1, s2 = Fraction(rng.randint(-9, 9), rng.randint(1, 9)), Fraction(rng.randint(-9, 9), rng.randint(1, 9))
    u1, u2 = Fraction(rng.randint(-9, 9), rng.randint(1, 9)), Fraction(rng.randint(-9, 9), rng.randint(1, 9))
    ok_add &= R(s1 + s2, u1 + u2) == R(s1, u1) + R(s2, u2)
    c = Fraction(rng.randint(-5, 5), rng.randint(1, 5))
    ok_hom &= R(c * s1, c * u1) == c * R(s1, u1)
print("1 additive in (s,u) with price substituted:", ok_add)
print("1 homogeneous (R(cs,cu)=cR(s,u)) with price substituted:", ok_hom)
print("1 R(0,0) =", R(Fraction(0), Fraction(0)))

# 2. fixed price p: the (s,u)-free part of the residual at p = 1 (informed + uninformed demand terms).
# Using the twin's own moments: slope = Cov(v,p)/Var(p) and resid_var at the equilibrium price.
var_p = ts * ts * (SIG_V2 + SIG_E2) + tu * tu * SIG_U2
cov_vp = ts * SIG_V2
slope = cov_vp / var_p
resid_var = SIG_V2 - slope * cov_vp
var_inf = SIG_V2 * SIG_E2 / (SIG_V2 + SIG_E2)
p_fixed = Fraction(1)
const_term = LAM * (-p_fixed) / (A * var_inf) + (1 - LAM) * (slope * p_fixed - p_fixed) / (A * resid_var)
print("2 slope", slope, "resid_var", resid_var, "var_inf", var_inf)
print("2 (s,u)-free part of residual at fixed p=1:", const_term, "nonzero:", const_term != 0)
print("2 twin residual at (s,u)=(0,0) with substituted price (must be 0):", R(Fraction(0), Fraction(0)))

# 3. dimensions as (money, asset) exponents
M = lambda m, a: (m, a)  # noqa: E731
def mul(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))
def inv(x):
    return (-x[0], -x[1])
price_u = (1, -1)  # money per unit asset
asset = (0, 1)
money = (1, 0)
a_cara = inv(money)  # CARA coefficient: utility of wealth in money
sig_e2 = mul(price_u, price_u)
kappa_dim = mul(a_cara, sig_e2)  # kappa = a sigma_e^2 / lambda (lambda dimensionless)
theta_s_dim = mul(price_u, inv(price_u))  # theta_s s = p
theta_u_dim = mul(price_u, inv(asset))  # theta_u u = p
print("3 kappa exponents (money, asset):", kappa_dim, "= price per unit asset squared is", (1, -2))
print("3 theta_u exponents:", theta_u_dim, "theta_s exponents:", theta_s_dim)
print("3 kappa*u exponents:", mul(kappa_dim, asset), "(price per unit asset is (1,-1))")
print("3 kappa matches (1,-2):", kappa_dim == (1, -2), "theta_u matches (1,-2):", theta_u_dim == (1, -2))
