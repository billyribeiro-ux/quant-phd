"""FC2-b round 3: recompute every number in prose and displayed output of L04-L06 from unrounded values."""
import math
from fractions import Fraction as F

e = math.exp
def r2(x):
    return f"{x:.2f}"

print("L04 Example 2.5 hold at 0:", r2(10 * e(-0.4)), " exercise call date1 PV:", r2(20 * e(-0.1)))
print("L04 Example 2.5 put best date3 PV:", r2(20 * e(-0.3)), " call hold at t=1,2,3:", r2(10*e(-0.3)), r2(10*e(-0.2)), r2(10*e(-0.1)))
print("L04 call exercise t=2 alt put date2 PV:", r2(10 * e(-0.2)))
print("L04 1000e^-0.4 cents:", f"{1000*e(-0.4):.2f}")
print("L04 R1 S_tau:", f"{100 + 20*e(0.3):.5f}", " check: (S-100)e^-0.3 =", f"{(100+20*e(0.3)-100)*e(-0.3):.6f}")
print("L04 R3 call best 10e^-0.3:", r2(10*e(-0.3)), " hold 50e^-0.4:", r2(50*e(-0.4)))
print("L04 E2 put 10e^-0.4:", r2(10*e(-0.4)), " 20e^-0.3:", r2(20*e(-0.3)))
print("L04 E3 10e^-0.2:", r2(10*e(-0.2)))
print("L04 M1 profit/break-even: 12-4=8, 50+4=54 (exact)")
print("L05 M1 P:", F(8) - 100 + F(97, 100) * 105)
print("L05 R2 bound with r=-0.1:", f"{120 - 100*e(0.1):.4f}", r2(120 - 100*e(0.1)))
print("L05 canon example 100e^-0.1-50:", f"{100*e(-0.1)-50:.4f}", r2(100*e(-0.1)-50))
print("L05 canon R2-like: e^-0.1*100 =", f"{100*e(-0.1):.4f}")
print("L05 E3: 0.9*120-100 =", F(9, 10) * 120 - 100)
print("L05 M2: lower bound", max(50 - F(95, 100) * 40, 0), " cash 3-50+38 =", 3 - 50 + 38)
print("L05 M3: chord", (15 + 4) / 2, " second diff", 15 - 2 * 9 + 4)
print("L05 E1 second diffs (cents):", 3000 - 2*2000 + 1000, 2000 - 2*1000 + 100, 1000 - 2*100 + 0)
print("L05 lab D=9/10 call/put tables:")
D = F(9, 10)
for K in (8000, 9000, 10000, 11000, 12000):
    c = max(10000 - D*K, 0) + F(max(10000 - K, 0), 10)
    p = c - 10000 + D*K
    print("  K", K, "C", c, "P", p)
print("L06 q, V0 example 1.5:", F(5,4)-F(1,2), (F(5,4)-F(1,2))/(F(3,2)-F(1,2)), ((F(3,4))*50)/F(5,4))
print("L06 Example 3.4:", (F(3,4)*125)/F(5,4), (F(3,4)*75)/F(5,4), F(16,25)*F(9,16)*125)
print("L06 expected S2 under Q:", F(9,16)*225 + F(6,16)*75 + F(1,16)*25, " discounted:", (F(9,16)*225 + F(6,16)*75 + F(1,16)*25)*F(16,25))
print("L06 payoff at expected price:", max(F(15625,100)-100,0), " discounted:", max(F(15625,100)-100,0)*F(16,25), " E[payoff] before disc:", F(9,16)*125)
print("L06 M1/M2/M3:", F(1,2)*100/(F(5,4)), F(2,3)*100 - F(80,3), F(1,2)*300/F(5,4), F(1,2)*120/F(5,4))
print("L06 E2 price 200 strike:", F(3,4)*100/F(5,4))
print("L06 R2 R_f=1:", (F(1,2)*50)/1)
print("L06 E3 cash:", -28 + 30 - 2, "payoff up", 50 - 75 + 25 + F(5,2), "down", 0 - 25 + 25 + F(5,2))
print("L06 R1 replication:", [F(1)*x - 100 for x in (150,100,50)], "B=", F(-100)/F(5,4))
