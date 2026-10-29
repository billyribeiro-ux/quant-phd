"""Independent re-derivation of slice-b numbers (Fraction arithmetic, no lab code reused)."""
import math
from fractions import Fraction as F

# L04 Example 2.5 and Remark/R1/R3/E2/E3
D = F(9, 10)
path = [100, 120, 90, 80, 110]
K = 100
call_int = [max(s - K, 0) for s in path]
put_int = [max(K - s, 0) for s in path]
hold_call = [max(path[-1] - K, 0) * D ** (4 - t) for t in range(5)]
pv_call_ex = [call_int[t] * D ** t for t in range(5)]
pv_put_ex = [put_int[t] * D ** t for t in range(5)]
print("L04 call intrinsic", call_int, "put intrinsic", put_int)
print("L04 call hold t=0..4", [float(x) for x in hold_call], "round2", [round(float(x), 2) for x in hold_call])
print("L04 call exercise PV", [float(x) for x in pv_call_ex], "best", max(range(5), key=lambda t: pv_call_ex[t]), float(max(pv_call_ex)))
print("L04 put exercise PV", [float(x) for x in pv_put_ex], "best", max(range(5), key=lambda t: pv_put_ex[t]), float(max(pv_put_ex)))
print("L04 10*(9/10)^4 =", float(10 * D ** 4), " 20*(9/10)^3=", float(20 * D ** 3))
print("L04 r = ln(10/9) =", math.log(10 / 9), "=> per cent", round(100 * math.log(10 / 9), 2))
S_tau = 100 + F(20000, 729)
print("L04 R1 S_tau =", float(S_tau), "exact", S_tau)
# R3 path 100,90,95,110,150
p3 = [100, 90, 95, 110, 150]
intr = [max(s - K, 0) for s in p3]
best_ex = max(intr[t] * D ** t for t in range(4))
hold3 = max(p3[-1] - K, 0) * D ** 4
print("L04 R3 best early PV", float(best_ex), "hold PV", float(hold3))
# E2 last spot 90
print("L04 E2 hold call", max(90 - K, 0) * D ** 4, " put payoff at expiry PV", float(max(K - 90, 0) * D ** 4))
# E3 put at date 2
print("L04 E3 put int t=2 PV", float(10 * D ** 2), "hold", max(K - 110, 0))
# L04 Remark 2.6: sell price >= 20 at date 1 (intrinsic), nothing to compute.
# L04 quiz: break-even
print("L04 M1 payoff/profit/be", 62 - 50, 62 - 50 - 4, 50 + 4)
print("L04 M2 be/payoff/profit", 80 - 3, 80 - 60, 80 - 60 - 3)

# L05
def lam(k1, k2, k3):
    return F(k3 - k2, k3 - k1)
Dd = F(9, 10)
strikes = [80, 90, 100, 110, 120]
S = 100
def call(k, Dv):
    return max(S - Dv * k, 0) + F(max(100 - k, 0), 10)
def put(k, Dv, c):
    return c - S + Dv * k
calls = [call(k, Dd) for k in strikes]
puts = [put(k, Dd, c) for k, c in zip(strikes, calls)]
print("L05 calls", [float(x) for x in calls], "puts", [float(x) for x in puts])
for k, c, p in zip(strikes, calls, puts):
    assert c - p - S + Dd * k == 0
print("L05 parity cost zero at all strikes: True")
# D claims: bounds hold for D>=1/40 on this grid and fail below
def bounds_ok(Dv):
    ok = True
    for k in strikes:
        c = call(k, Dv)
        p = put(k, Dv, c)
        dk = Dv * k
        if not (0 <= c <= S): ok = False
        if c < max(S - dk, 0): ok = False
        if not (0 <= p <= dk): ok = False
        if p < max(dk - S, 0): ok = False
    return ok
for Dv in [F(1, 100), F(1, 50), F(1, 41), F(1, 40), F(1, 39), F(1, 20), F(1, 2), F(9, 10), F(1)]:
    print("L05 D", Dv, "bounds_ok", bounds_ok(Dv), "call80", float(call(80, Dv)))
# convexity at D = 9/10 and at a few random D (ensure claim holds for every D)
import random
random.seed(1)
def convex_ok(Dv):
    cs = [call(k, Dv) for k in strikes]
    for i in range(5):
        for j in range(i + 1, 5):
            for kk in range(j + 1, 5):
                l = lam(strikes[i], strikes[j], strikes[kk])
                if cs[j] > l * cs[i] + (1 - l) * cs[kk]:
                    return False
    return True
print("L05 convexity at D=9/10", convex_ok(Dd), " random D sample all true:", all(convex_ok(F(random.randint(1, 200), 100)) for _ in range(200)))
# planted convexity: call and put at 90 raised 500 cents (= 5 USD)
planted = [c + (F(5) if k == 90 else 0) for k, c in zip(strikes, calls)]
viol = []
for i in range(5):
    for j in range(i + 1, 5):
        for kk in range(j + 1, 5):
            l = lam(strikes[i], strikes[j], strikes[kk])
            if planted[j] > l * planted[i] + (1 - l) * planted[kk]:
                viol.append((strikes[i], strikes[j], strikes[kk]))
print("L05 planted convexity violated triples (USD)", viol)
# intrinsic check D<=1 printed as zero violations
print("L05 R2 bound r=-0.1:", 120 - math.exp(0.1) * 100, "intrinsic 20")
print("L05 canon put example:", round(100 * math.exp(-0.1) - 50, 4))
print("L05 M1 put:", 8 - 100 + F(97, 100) * 105, "M2 bound", 50 - F(95, 100) * 40, "M3 chord", F(15 + 4, 2))
print("L05 E1 second diffs", 3000 - 2 * 2000 + 1000, 2000 - 2 * 1000 + 100, 1000 - 2 * 100 + 0)
print("L05 E3 put 120:", F(9, 10) * 120 - 100, "call bound", max(100 - F(9, 10) * 120, 0))

# L06
q = (F(5, 4) - F(1, 2)) / (F(3, 2) - F(1, 2))
print("L06 q", q)
V1u, V1d = F(50), F(0)
Delta = (V1u - V1d) / ((F(3, 2) - F(1, 2)) * 100)
B = (F(3, 2) * V1d - F(1, 2) * V1u) / ((F(3, 2) - F(1, 2)) * F(5, 4))
print("L06 Ex1.5 Delta", Delta, "B", B, "V0", Delta * 100 + B, "q-form", (q * V1u + (1 - q) * V1d) / F(5, 4))
# Example 1.6 pi=35
print("L06 Ex1.6 surplus", 35 - 50 + 20, "x5/4", (35 - 50 + 20) * F(5, 4), "up", F(1, 2) * 150 - 25 - 50 + 0, "down", F(1, 2) * 50 - 25)
# Example 3.4
uu, ud, dd = 225, 75, 25
pay = {"uu": 125, "ud": 0, "dd": 0}
v_up = (q * pay["uu"] + (1 - q) * pay["ud"]) / F(5, 4)
v_dn = (q * pay["ud"] + (1 - q) * pay["dd"]) / F(5, 4)
v0 = (q * v_up + (1 - q) * v_dn) / F(5, 4)
print("L06 Ex3.4 V(1,1)", v_up, "V(1,0)", v_dn, "V(0,0)", v0)
ex = q * q * 225 + 2 * q * (1 - q) * 75 + (1 - q) ** 2 * 25
print("L06 E[S2]", ex, "E[payoff]", q * q * 125, "payoff at E", max(ex - 100, 0), "disc", max(ex - 100, 0) * F(16, 25))
print("L06 closed", F(16, 25) * q * q * 125)
# M1, M2, M3
q1 = (F(5, 4) - F(1, 2)) / (2 - F(1, 2))
print("L06 M1 q", q1, "V0", (q1 * 100) / F(5, 4))
print("L06 M2 Delta", (100 - 0) / ((2 - F(1, 2)) * 100), "B", (2 * 0 - F(1, 2) * 100) / ((2 - F(1, 2)) * F(5, 4)))
print("L06 M3 V11", (F(1, 2) * 300) / F(5, 4), "V00", (F(1, 2) * ((F(1, 2) * 300) / F(5, 4))) / F(5, 4))
print("L06 E2 V0 doubled", (q * 100) / F(5, 4) * 2, "E3 quote 28 surplus", 30 - 28)
print("L06 R2 R_f=1 q", (1 - F(1, 2)) / (F(3, 2) - F(1, 2)), "V0", (F(1, 2) * 50))
