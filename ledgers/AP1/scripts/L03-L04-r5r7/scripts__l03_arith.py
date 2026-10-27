# Independent arithmetic recheck of L03 hand-derived numbers (Example 2.3, Example 4.3, M1-M3, P2, Lab 2 values).
from fractions import Fraction as F
# Example 2.3
bond, stock, fund = (1, 1, 1), (1.4, 1.1, 0.6), (2.4, 2.1, 1.6)
th = (141, 140, -140)
pr = (0.96, 0.976, 1.95)
cf = [sum(th[i]*(bond, stock, fund)[i][s] for i in range(3)) for s in range(3)]
print("ex2.3 payoff", [round(x, 9) for x in cf], "cost", round(sum(th[i]*pr[i] for i in range(3)), 9))
print("ex2.3 violation cost 0.96+0.976-1.95 =", round(0.96+0.976-1.95, 9), "; 140*0.014 =", round(140*0.014, 9), "; -1.96+0.96 =", round(-1.96+0.96, 9))
# Example 4.3 with exact fractions
psi1 = (F(1,2), F(0), F(46,100)); psi2 = (F(0), F(8,10), F(16,100)); z = (F(4,10), F(1,10), F(0))
print("sums", sum(psi1), sum(psi2), "pricing", F(14,10)*psi1[0]+F(11,10)*psi1[1]+F(6,10)*psi1[2], F(14,10)*psi2[0]+F(11,10)*psi2[1]+F(6,10)*psi2[2])
print("psi.z", sum(a*b for a,b in zip(psi1,z)), sum(a*b for a,b in zip(psi2,z)))
v = tuple(b-a for a,b in zip(psi1,psi2)); print("v", v)
up = F(1,2)*F(976,1000) - F(3,10)*F(96,100); lo = F(2,10)*F(976,1000) - F(12,100)*F(96,100)
print("upper cost", up, "lower value", lo)
print("0.5 stock - 0.3 bond payoff", [F(5,10)*a - F(3,10)*1 for a in (F(14,10),F(11,10),F(6,10))])
print("0.2 stock - 0.12 bond payoff", [F(2,10)*a - F(12,100) for a in (F(14,10),F(11,10),F(6,10))])
# M1
print("M1 payoff", 4-F(10,3)*F(12,10), 4-F(10,3)*F(9,10), "cost", 4*F(95,100)-F(10,3)*F(116,100), "obj", float(1+ (-(4*F(95,100)-F(10,3)*F(116,100)))))
# M2
print("M2 segment ends", float(F(46,100)*F(4,10)), float(F(16,100)*F(4,10)), "parity", F(976,1000)-F(96,100))
# M3
print("M3 coordinate ranges: e1", float(psi1[0]), float(psi2[0]), "e2", float(psi1[1]), float(psi2[1]), "e3", float(psi2[2]), float(psi1[2]), "upper sum", float(F(5,10)+F(8,10)+F(46,100)))
# Lab 2 interior quote
print("interval width", 0.20-0.08)
