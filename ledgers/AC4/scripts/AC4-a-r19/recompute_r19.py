import math
from fractions import Fraction as Fr
# L01 R3: cost(h) = 4000 * ceil(h/400) for h>=1, 0 at h=0; high-low on (0,0),(1200,12000)
def cost(h):
    return 0 if h == 0 else 4000 * math.ceil(h / 400)
v = Fr(12000, 1200); F = Fr(0)
errs = {h: abs(cost(h) - (F + v * h)) for h in range(0, 1201)}
mx = max(errs.values())
print("whole hours counted", len(errs), "max abs error", mx, "at", [h for h, e in errs.items() if e == mx], "share of step", float(Fr(mx, 4000)) * 100)
print("line at 1,401,801:", [float(F + v*h) for h in (1, 401, 801)], "cost", [cost(h) for h in (1, 401, 801)])
# L02 numbers
p, vc, F_, step, T = 2500, 1150, 120000, 2700000, 2000  # cents: price 25.00, var 11.50, fixed 1200.00
m = p - vc
print("margin cents", m, "ratio", Fr(m, p))
q_star = Fr(F_, m); print("Q* lower", float(q_star), "ceil", math.ceil(q_star))
q_up = Fr(F_ + step, m); print("upper", float(q_up), "ceil", math.ceil(q_up))
OI = lambda Q: m * Q - F_ - (step if Q > T else 0)
print("OI(88)", OI(88), "OI(89)", OI(89), "OI(2001)", OI(2001), "OI(2088)", OI(2088), "OI(2089)", OI(2089))
neg = [Q for Q in range(0, 5001) if OI(Q) < 0]
runs = []
for Q in neg:
    if runs and runs[-1][1] == Q - 1: runs[-1][1] = Q
    else: runs.append([Q, Q])
print("loss runs", runs)
Q = 2500
print("OI(2500)", OI(Q) / 100, "MoS units", Q - float(q_up), "share", (Q - float(q_up)) / Q * 100, "DOL", m * Q / OI(Q))
print("zero check  ceil(2088.89)=", math.ceil(q_up), "OI(2089) >=0", OI(2089) >= 0)
print("fixed +10000c moves BE by", 10000 / m)
# R3 L02: products margins 10 and 30, shares
for label, mbar, bev in [("below 1000", 10, Fr(60000, 10)), ("above 1000", 20, Fr(60000, 20))]:
    print(label, "BE", float(bev))
