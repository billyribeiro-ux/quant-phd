from fractions import Fraction as F
import random
# L04: IS-LM
c,c0,b0,b,d,h,tax,G,mbar = F(3,4),F(1),F(1),F(2),F(1,2),F(1),F(0),F(1),F(2)
A = c0 - c*tax + b0 + G; D = h*(1-c) + b*d
Y = (h*A + b*mbar)/D; i = (d*A - (1-c)*mbar)/D
print("L04 A",A,"D",D,"Y",Y,"i",i, "IS res", (1-c)*Y + b*i - A, "LM res", d*Y - h*i - mbar)
print("L04 h/D",h/D,"b/D",b/D,"-(1-c)/D",-(1-c)/D,"bench",1/(1-c))
Y2=((h*(A+F(1,10))+b*mbar)/D); print("dY G->11/10", Y2-Y, "di", ((d*(A+F(1,10))-(1-c)*mbar)/D)-i)
print("M1 check", (F(1,2)*F(14,3)+2*F(5,6)), (F(14,3)-2*F(5,6)))
# L05
a,eta,ybar,nu,pe = F(1160),F(100),F(1000),F(200),F(1)
P=(a-ybar+nu*pe)/(eta+nu); Yy=a-eta*P
P1=(a+30-ybar+nu*pe)/(eta+nu); Y1=a+30-eta*P1
print("L05 P",P,"Y",Yy,"dP",P1-P,"dY",Y1-Yy, float(P1-P), float(Y1-Yy))
for s in [50,100,200,400,800]:
    s=F(s); print("nu",s, float(s/(eta+s)), float(F(30)/(eta+s)), float(F(30)*s/(eta+s)))
print("LR", float((a-ybar)/eta), float((a+30-ybar)/eta))
# L06
kappa, un, nuu = F(200), F(5,100), F(200)
P0, pi0 = F(6,5), F(3,100)
pe0 = P0*(1+pi0); P1_ = pe0 - kappa*(F(6,100)-un)/nuu
print("L06 A pe",pe0,"P1",P1_,"pi",(P1_-P0)/P0, float((P1_-P0)/P0), "form", float(pi0 - (kappa/(nuu*P0))*(F(6,100)-un)))
rng = random.Random(20261028)
price, pi = P0, pi0
for t in range(1,13):
    draw = rng.randint(-100,100); gap=F(draw,10000); u=un+gap
    pe = price*(1+pi); newp = pe - kappa*(u-un)/nuu; newpi=(newp-price)/price
    form = pi - (kappa/(nuu*price))*(u-un)
    print(t, draw, float(newpi), float(newpi-pi), newpi==form)
    price, pi = newp, newpi
print("slope 5/6 change at 4%:", float(-(F(5,6))*(F(4,100)-un)), "at 3%", float(-(F(5,6))*(F(3,100)-un)))
print("R2 u", float(un + F(1,100)/(F(5,6))))
