from fractions import Fraction as F
from decimal import Decimal as D, getcontext
getcontext().prec=40
print("displayed-digit quotient 0.28579088/0.39125077 =", D("0.28579088")/D("0.39125077"))
print("unrounded ratio to 8dp:", (D("0.2857908849045049")/D("0.3912507700268084")).quantize(D("0.00000001")))
# EZ bisection noise source: evaluate ez_value at the exact CE, compare to target
import math
GAMMA=2.0
def ez_value(c0, date1, psi, beta):
    rho = 1.0 - 1.0/psi
    expectation = sum(p * c1 ** (1.0 - GAMMA) for c1, p in date1)
    inner = (1.0 - beta) * c0**rho + beta * expectation ** (rho / (1.0 - GAMMA))
    return float(inner ** (1.0 / rho))
exact = 1/(0.5/110000 + 0.5/95000)
for psi,beta in ((0.5,0.9),(3.0,0.9),(1.5,0.95)):
    target = ez_value(100000.0, [(110000.0,0.5),(95000.0,0.5)], psi, beta)
    at_exact = ez_value(100000.0, [(exact,1.0)], psi, beta)
    print(psi,beta,"value at exact CE minus target:", at_exact-target)
# Prop 2.4 counterexample: u(W)=-W (strictly decreasing), red bet, W1=110000, W0'=95000
W1,W0=110000.0,95000.0
for k in (0,45,90):
    p=k/90
    Eu = p*(-W1)+(1-p)*(-W0)
    print("k",k,"E u =",Eu)
