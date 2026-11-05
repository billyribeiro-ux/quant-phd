from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60
F = 100000; C = 5000; N = 10
def cf(t): return C + (F if t == N else 0)
def P_dec(y):
    v = 1 + Decimal(y)
    return sum(Decimal(cf(t)) / v**t for t in range(1, N+1))
def P1_dec(y):
    v = 1 + Decimal(y)
    return sum(-Decimal(t*cf(t)) / v**(t+1) for t in range(1, N+1))
def P2_dec(y):
    v = 1 + Decimal(y)
    return sum(Decimal(t*(t+1)*cf(t)) / v**(t+2) for t in range(1, N+1))
y0 = Decimal("0.04")
print("P(0.04) =", P_dec(y0))
print("P'(0.04) =", P1_dec(y0), " P''(0.04) =", P2_dec(y0))
print("-P'/P =", -P1_dec(y0)/P_dec(y0), " P''/P =", P2_dec(y0)/P_dec(y0))
# float-based errors as the lab does (exact Fraction on float yields, float sensitivities)
def fl_price(y): 
    v = 1 + Fraction(y); return sum((Fraction(cf(t))/v**t for t in range(1,N+1)), Fraction(0))
def fl_p1(y):
    v = 1 + Fraction(y); return float(-sum((Fraction(t*cf(t))/v**(t+1) for t in range(1,N+1)), Fraction(0)))
def fl_p2(y):
    v = 1 + Fraction(y); return float(sum((Fraction(t*(t+1)*cf(t))/v**(t+2) for t in range(1,N+1)), Fraction(0)))
Y0 = 0.04
P0 = fl_price(Y0); p1 = fl_p1(Y0); p2 = fl_p2(Y0)
def T1(dy): return P0 + Fraction(p1)*Fraction(dy)
def T2(dy): return T1(dy) + Fraction(1,2)*Fraction(p2)*Fraction(dy)**2
prev=None
for dy in (0.01, 0.005, 0.0025):
    e1 = fl_price(Y0+dy) - T1(dy); e2 = fl_price(Y0+dy) - T2(dy)
    print("dy", dy, "e1 %.6e e2 %.6e" % (float(e1), float(e2)), ("ratios %.4f %.4f" % (float(prev[0]/e1), float(prev[1]/e2))) if prev else "")
    prev=(e1,e2)
print("exact-decimal errors at 0.01 (cents): second-order", float(P_dec(y0+Decimal("0.01")) - (P_dec(y0) + P1_dec(y0)*Decimal("0.01") + P2_dec(y0)*Decimal("0.01")**2/2)))
print("unrounded price at float 0.04+0.01:", float(fl_price(0.04+0.01)))
off = Fraction(0.04+0.01) - Fraction(1,20)
print("float 0.04+0.01 exact minus 1/20 =", float(off), "| 0.04+0.01 == 0.05:", 0.04+0.01 == 0.05)
print("P(0.05) exact decimal:", P_dec(Decimal("0.05")))
print("P'(0.05) decimal:", P1_dec(Decimal("0.05")), " P'(0.05)*offset:", float(P1_dec(Decimal("0.05"))*Decimal(str(float(off)))))
print("P(float 0.05) - 100000 =", float(fl_price(0.04+0.01)) - 100000)
print("integer cents at 0.04+0.01:", round(fl_price(0.04+0.01)), " second-order expansion rounding at +0.01:", round(T2(0.01)), "at -0.01:", round(T2(-0.01)), " exact at -0.01:", round(fl_price(Y0-0.01)))
# quiz: c1=-1,c2=1000, N=2 at y=0.04
y=Decimal("0.04"); v=1+y
print("quiz P' (c1=-1,c2=1000) =", -(Decimal(1)*(-1)/v**2 + Decimal(2)*1000/v**3))
print("M1 check:", Decimal(50)/Decimal("1.05") + Decimal(1050)/Decimal("1.05")**2)
print("P'(0.04) two decimal forms:", float(P1_dec(y0)))
print("cents exact at -0.01 from decimal:", P_dec(Decimal("0.03")))
