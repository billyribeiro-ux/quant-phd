from fractions import Fraction as F
import math
# L01 Remark 2.4 and E2
px, py, m = F(2), F(3), F(120)
x = F(20); y = (m - px*x)/py
print("L01 y at x=20:", y, "MRS:", y/x, "price ratio:", px/py, "f'(20):", (m-2*px*20)/py)
x1, y1 = F(21), y - F(2, 3)
print("E2 new u:", x1*y1, "old u:", x*y, "change:", x1*y1 - x*y, "first order:", F(40,3), "diff:", (x1*y1 - x*y) - F(40,3))
# L02 Remark 1.6 counterexample: p<c, formula vs truth
p, c, k, Fc = F(1), F(3), F(1), F(0)
qstar = max(F(0), (p-c)/(2*k))
pi = lambda q: p*q - (Fc + c*q + k*q*q)
print("L02 p<c: pi(q*)-pi(0) =", pi(qstar)-pi(F(0)), " claimed (p-c)^2/(4k) =", (p-c)**2/(4*k))
# L02 R3 threshold
print("L02 R3 threshold case1:", float(3*0 + 2 + 2*math.sqrt(12)))
print("L02 mech M1 :", F(12-4, 4), pi(F(0)) if False else (12*F(2) - (4*2 + 2*4)))
# L03 values
a,b,n,cc,kk = F(100),F(2),10,F(2),F(1)
s = F(n)/(2*kk); ps=(a+s*cc)/(b+s); Q=a-b*ps
print("L03", ps, Q, s*(ps-cc), (a-b*cc)/(b+s), float(ps), float(Q))
print("L03 Z(20):", (a-b*20) - s*(20-cc), "one firm:", (ps-cc)/(2*kk))
# hub placement percentages and mastery
print("hub 7/9, 8/9:", round(7/9*100,1), round(8/9*100,1))
print("hub e^0.5:", math.exp(0.5), "100e^-0.1:", 100*math.exp(-0.1), "abs err item4:", abs(1.6487-math.exp(0.5)))
# L03 R3-style; L01 R2 check Cobb-Douglas share algebra with a=0.3, x from tangency
print("L02 E2 16sqrt3-24:", 16*math.sqrt(3)-24, "28-16sqrt3:", 28-16*math.sqrt(3))
