import math
from fractions import Fraction as F
from decimal import Decimal, getcontext
def nearest(x): return math.floor(x + F(1, 2))
# A: 5e-9 annual, 360 months, principal 13296419
i = F("5e-9") / 12
ex = F(13296419) * i / (1 - (1 + i) ** (-360))
print("A exact", float(ex), "nearest", nearest(ex), "loan/months", 13296419/360)
# B: 480 months, 100000 at 0.05
i = F("0.05") / 12
p = nearest(F(100000) * i / (1 - (1 + i) ** (-480)))
print("B payment", p)
# C: 499 cents at 0.012 month1 interest
print("C", float(F(499) * F("0.012") / 12), nearest(F(499) * F("0.012") / 12))
# D: 1000 at 0.05 one month
print("D", nearest(F(1000)*F("0.05")/12), 1000 + nearest(F(1000)*F("0.05")/12))
# E: 1.2e-11 case
print("E", Decimal(499999999999) * (1 + Decimal("1e-12")))
# F: -0.999 three periods
v = 1/(1-0.999)
print("F sum", v + v**2 + v**3, "closed (1-(1+r)^-3)/r", (1-(1-0.999)**-3)/(-0.999), "comment (1-1e-9)/(-0.999)", (1-1e-9)/(-0.999))
# G: growth
print("G", 1/(0.05-0.0499), 1/(0.05+0.999), 1/0.07)
# Lab3 bound and tail
i = 0.045/12
print("bound", round(300*(1+i)**300+1, 4), "tail", ((1.02)/1.05)**400/0.03, "q", 1.02/1.05)
# effective vs nominal payment
L=30000000; n=300
j=(1.045)**(1/12)-1
def pay(r): return L*r/(1-(1+r)**-n)
print("eff monthly", j, "pay nominal", pay(i), "pay effective", pay(j), "1.045-check", (1+i)**12)
# 1e-6 cutoff N
v=1/1.05; N=1
while v**N/0.05>=1e-6: N+=1
print("N", N, v**(N-1)/0.05, v**N/0.05)
print("5e-8 check", 1e-6*0.05)
