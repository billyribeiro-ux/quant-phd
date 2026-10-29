"""Independent re-derivation of every prose number in L04-L06 (E5 slice b, round 3). Uses only fractions."""
from fractions import Fraction as F

ok = []
def chk(name, got, want):
    ok.append((name, got == want))
    print(f"{name}: got={got} want={want} {'OK' if got == want else 'MISMATCH'}")

# L04: IS-LM, parameters of Lab 1
c, c0, b0, b, d, h, tax, G, m = F(3,4), F(1), F(1), F(2), F(1,2), F(1), F(0), F(1), F(2)
A = c0 - c*tax + b0 + G
D = h*(1-c) + b*d
Ys = (h*A + b*m)/D; is_ = (d*A - (1-c)*m)/D
chk("L04 A", A, F(3)); chk("L04 D", D, F(5,4)); chk("L04 Y*", Ys, F(28,5)); chk("L04 i*", is_, F(4,5))
chk("L04 IS residual", (1-c)*Ys + b*is_ - A, F(0)); chk("L04 LM residual", d*Ys - h*is_ - m, F(0))
chk("L04 h/D", h/D, F(4,5)); chk("L04 b/D", b/D, F(8,5)); chk("L04 -(1-c)/D", -(1-c)/D, F(-1,5))
chk("L04 dY for G 1->11/10", (h/D)*F(1,10), F(2,25)); chk("L04 di for G 1->11/10", (d/D)*F(1,10), F(1,25))
chk("L04 di for G 1->2", d/D, F(2,5)); chk("L04 benchmark", 1/(1-c), F(4))
chk("L04 b=0 multiplier", h/(h*(1-c)), F(4))
chk("L04 dY per unit m rise 1/2", (b/D)*F(1,2), F(4,5))
chk("L04 E3 share", h*(1-c)/D, F(1,5)); chk("L04 E3 0.8/4", F(4,5)/4, F(1,5))
chk("L04 E1 ratio di/dY", (d/D)/(h/D), F(1,2))
# L04 problem set M1-M3 with c=1/2 b=2 d=1 h=2 A=4 mbar=3
c2, b2, d2, h2, A2, m2 = F(1,2), F(2), F(1), F(2), F(4), F(3)
D2 = h2*(1-c2)+b2*d2
chk("L04 M1 D", D2, F(3)); chk("L04 M1 Y", (h2*A2+b2*m2)/D2, F(14,3)); chk("L04 M1 i", (d2*A2-(1-c2)*m2)/D2, F(5,6))
chk("L04 M2 h/D", h2/D2, F(2,3)); chk("L04 M3 b/D", b2/D2, F(2,3)); chk("L04 M3 -(1-c)/D", -(1-c2)/D2, F(-1,6))
chk("L04 M2 ratio", (F(2,3))/2, F(1,3))

# L05: AD-AS, Lab 1 values
a, eta, Yb, nu, Pe = F(1160), F(100), F(1000), F(200), F(1)
P0 = (a-Yb+nu*Pe)/(eta+nu); Y0 = a-eta*P0
chk("L05 P*", P0, F(6,5)); chk("L05 Y*", Y0, F(1040))
P1 = (a+30-Yb+nu*Pe)/(eta+nu); Y1 = a+30-eta*P1
chk("L05 dP", P1-P0, F(1,10)); chk("L05 dY", Y1-Y0, F(20))
chk("L05 LR price before", (a-Yb)/eta, F(8,5)); chk("L05 LR price after", (a+30-Yb)/eta, F(19,10))
chk("L05 misc 1060 at Pe=1", (a+30) - eta*((a+30-Yb+nu*Pe)/(eta+nu)), F(1060))
chk("L05 misc demand at P=1.6", a-eta*F(8,5), F(1000))
chk("L05 E1 nu=400 share", F(400)/(100+400), F(4,5))
chk("L05 E2 dY 400->800", 30*(F(800,900)-F(4,5)), F(8,3))
chk("L05 R2 P*", (F(190)+nu*F(13,10))/(eta+nu), F(3,2))
chk("L05 R2 Y*", F(1190)-eta*F(3,2), F(1040))
chk("L05 M1 P*", (F(1100)-Yb+F(100)*F(11,10))/(F(100)+F(100)), F(21,20))
chk("L05 M1 Y*", F(1100)-F(100)*F(21,20), F(995))
chk("L05 M2 share", F(150)/(F(50)+F(150)), F(3,4)); chk("L05 M2 dP", F(40)/F(200), F(1,5))
chk("L05 M3 LR after", (F(1140)-Yb)/F(100), F(7,5))
for slope in (50, 100, 200, 400, 800):
    chk(f"L05 D nu={slope} share", F(slope)/(100+slope), F(slope, 100+slope))
    chk(f"L05 D nu={slope} dY", 30*F(slope)/(100+slope), F(30*slope, 100+slope))

# L06: Phillips curve, Lab 1 inputs
nu6, kap, un, P0_6, pi0 = F(200), F(200), F(5,100), F(6,5), F(3,100)
beta = kap/(nu6*P0_6)
chk("L06 beta", beta, F(5,6))
pe = P0_6*(1+pi0); u = F(6,100); Pn = pe - kap*(u-un)/nu6
chk("L06 Part A P1", Pn, F(1226,1000)); chk("L06 Part A pi levels", (Pn-P0_6)/P0_6, F(13,600))
chk("L06 Part A pi form", pi0-beta*(u-un), F(13,600))
chk("L06 misc 4pct change", -beta*(F(4,100)-un), F(1,120))
chk("L06 misc 3pct change", -beta*(F(3,100)-un), F(1,60))
chk("L06 misc gap -0.01", -beta*F(-1,100), F(1,120))
chk("L06 R1 ratio", (1/F(5,6)), F(6,5))
chk("L06 R2 u", un + F(1,100)/beta, F(31,500))
chk("L06 M1 beta", F(100)/(F(200)*1), F(1,2)); chk("L06 M1 pi", F(4,100)-F(1,2)*F(2,100), F(3,100))
chk("L06 M2 beta", F(200)/(F(200)*F(5,4)), F(4,5)); chk("L06 M2 pi", F(4,100)-F(4,5)*F(-1,100), F(48,1000))
chk("L06 M3 pi", F(2,100)-F(1,2)*F(3,100), F(5,1000))
chk("L06 E3 beta1*58bp", -beta*F(58,10000), F(-29,6000))
chk("L06 E3 5.5pct", -beta*F(5,1000), F(-1,240))
# seeded Part B check of period 1 by hand: gap 58bp
price1 = pe - kap*(un+F(58,10000)-un)/nu6
chk("L06 Part B t1 pi", (price1-P0_6)/P0_6, pi0 - beta*F(58,10000))
chk("L06 Part B t1 pi closed form", pi0 - beta*F(58,10000), F(151,6000))
print("ALL_OK" if all(x for _, x in ok) else "MISMATCH")
