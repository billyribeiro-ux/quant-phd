"""Re-derive the changed L04 and L06 numbers in exact arithmetic (run with python -I)."""
from fractions import Fraction as F
import math

# L04: discount 9/10 per year (exact), path 100,120,90,80,110, strike 100, expiry 4
D = F(9, 10)
K = 100
path = [100, 120, 90, 80, 110]
print("r = ln(10/9) =", round(math.log(F(10, 9)), 5), "; e^-r =", round(math.exp(-math.log(10 / 9)), 12))
for t, s in enumerate(path):
    call_ex = max(s - K, 0)
    put_ex = max(K - s, 0)
    print("t", t, "call_ex", call_ex, "call_hold_at_t", float(max(path[4] - K, 0) * D ** (4 - t)),
          "put_ex", put_ex, "put_hold_at_t", float(max(K - path[4], 0) * D ** (4 - t)))
print("call PV0 at t=1:", F(20) * D, "=", float(F(20) * D))
print("put PV0 at t=3:", F(20) * D**3, "=", float(F(20) * D**3))
print("call hold PV0:", F(10) * D**4, "=", float(F(10) * D**4))
print("R1 S_tau:", F(100) + F(20) * (F(10, 9)) ** 3, "=", float(F(100) + F(20) * (F(10, 9)) ** 3))
print("R3 put/call:", F(10) * D**3, float(F(10) * D**3), F(50) * D**4, float(F(50) * D**4))
print("E1 hold values t0..t4:", [float(F(10) * D ** (4 - t)) for t in range(5)])
print("E2 put at t2 PV0:", F(10) * D**2, "; hold at expiry 0 (110>100)")
print("L04 1000*(9/10)^4 cents:", F(1000) * D**4, "=", float(F(1000) * D**4))

# L06: u=3/2, d=1/2, R_f=5/4, S0=100, K=100
u, d, Rf, S0, Kc = F(3, 2), F(1, 2), F(5, 4), 100, 100
q = (Rf - d) / (u - d)
print("q =", q, "0<q<1:", 0 < q < 1)
V1u, V1d = max(u * S0 - Kc, 0), max(d * S0 - Kc, 0)
Delta = (V1u - V1d) / ((u - d) * S0)
B = (u * V1d - d * V1u) / ((u - d) * Rf)
V0 = Delta * S0 + B
print("Delta", Delta, "B", B, "V0", V0, "q-formula", (q * V1u + (1 - q) * V1d) / Rf)
# two-period: S(2) values uu, ud, dd
Suu, Sud, Sdd = u * u * S0, u * d * S0, d * d * S0
Pu, Pd, Pdd = max(Suu - Kc, 0), max(Sud - Kc, 0), max(Sdd - Kc, 0)
Vuu = (q * Pu + (1 - q) * 0) / Rf
Vud = (q * Pd + (1 - q) * 0) / Rf  # uses V at ud after u-move, ud value from payoffs
Vdd = (q * Pd + (1 - q) * Pdd) / Rf
V00 = (q * Vuu + (1 - q) * Vud) / Rf
print("V(1,1)", Vuu, "V(0,0)", V00)
EV_S2 = q * q * Suu + 2 * q * (1 - q) * Sud + (1 - q) ** 2 * Sdd
print("E_Q[S2]", EV_S2, "R_f^2 S0", Rf**2 * S0, "discounted", EV_S2 / Rf**2)
print("payoff at E[S2]", max(EV_S2 - Kc, 0), "discounted", max(EV_S2 - Kc, 0) / Rf**2)
EV_pay = q * q * Pu + 2 * q * (1 - q) * Pd + (1 - q) ** 2 * Pdd
print("E_Q[payoff]", EV_pay, float(EV_pay), "as fraction 1125/16 =", F(1125, 16) == EV_pay)
print("closed form 45:", (q * q * Pu + 2 * q * (1 - q) * Pd + (1 - q) ** 2 * Pdd) / Rf**2)
