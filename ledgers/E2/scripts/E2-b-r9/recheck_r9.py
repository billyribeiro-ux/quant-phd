from fractions import Fraction as F
import math
def rnd(x): return math.floor(x + F(1, 2))
# L04 (cents)
yL, yH, cL, cH = 4_000_000, 6_000_000, 1_000_000, 500_000
D = yH - yL
print("L04 bounds", F(D, cL), F(D, cH), "base thresholds", [t for t in range(1, 7) if F(D, cL) <= t <= F(D, cH)])
print("L04 t=2 high utility", yH - cH * 2, "t=4", yH - cH * 4, "wage gain at t=2", yH - yL, "cost", 2 * cH)
print("L04 m1 bounds", F(2_000_000, 1_000_000), F(2_000_000, 250_000), "m2 high util t=3", yH - 3 * 250_000 if False else yH - 3 * 250_000, "m2 b", yH - 3 * cH if False else "")
print("L04 m2 (cH=500k) high util t=3", yH - 3 * cH, "low at e=3", yH - 3 * cL)
print("L04 c_H=400k bounds", F(2_000_000, 1_000_000), F(2_000_000, 400_000))
print("L04 y_H=5M bounds", F(1_000_000, cL), F(1_000_000, cH))
# L05 menu base case
thL, thH, pL, pH = F(3000), F(6000), F(3, 4), F(1, 4)
qL = thL - pH / pL * (thH - thL); qH = thH
mL = thL * qL; mH = thH * qH - (thH - thL) * qL
UH = thH * qH - mH; UL = thL * qL - mL
C = lambda q: q * q / 2
fbL, fbH = thL, thH
fb = pL * (thL * fbL - C(fbL)) + pH * (thH * fbH - C(fbH))
menu = pL * (mL - C(qL)) + pH * (mH - C(qH))
print("L05 qL*", qL, "qH*", qH, "mL", mL, "mH", mH, "UH", UH, "UL", UL)
print("L05 first best", fb, "menu", menu, "gap", fb - menu)
print("L05 gap split low", pL * (4_500_000 - 4_000_000), "high rent part", pH * UH)
print("L05 pL(thL-qL)", pL * (thL - qL), "pH(thH-thL)", pH * (thH - thL))
print("L05 m2 profit", F(3, 4) * (3_000_000 - C(1000)) + F(1, 4) * (33_000_000 - C(6000)))
print("L05 loss pct", float((fb - menu) / fb * 100), "fb over menu -1", float(fb / menu - 1) * 100)
pH2, pL2 = F(1, 3), F(2, 3)
q1500 = thL - pH2 / pL2 * (thH - thL)
p1500 = pL2 * (thL * q1500 - C(q1500)) + pH2 * (thH * 6000 - (thH - thL) * q1500 - C(6000))
print("L05 var p_H=1/3 q_L*", q1500, "profit at 1500", p1500, "menu at 2000", float(pL2 * (4_000_000 + 0) ) if False else "")
m2000 = pL2 * (thL * 2000 - C(2000)) + pH2 * (thH * 6000 - (thH - thL) * 2000 - C(6000))
print("L05 var menu at 2000", m2000, "first best", pL2 * 4_500_000 + pH2 * 18_000_000, "gap 2000", pL2 * 4_500_000 + pH2 * 18_000_000 - m2000, "gap 1500", pL2 * 4_500_000 + pH2 * 18_000_000 - p1500)
print("L05 rent p_H=1/3", (thH - thL) * q1500)
# L06
EH, EL, cHh = F(750_000), F(250_000), F(100_000)
dE = EH - EL
print("L06 dE", dE, "beta*", cHh / dE, "profit at 0.2", EH * (1 - F(1, 5)), "agent util", F(1, 5) * EH - cHh)
print("L06 beta=0.3 profit", EH * F(7, 10), "beta=0.25 util", F(1, 4) * EH - cHh, F(1, 4) * EL, "profit", EH * F(3, 4))
print("L06 beta=2/15 high util", F(2, 15) * EH - cHh, "low util", F(2, 15) * EL, float(F(2, 15) * EL))
print("L06 alpha=1e4 beta=1/5 profit", EH - (10_000 + F(1, 5) * EH))
print("L06 Remark 1.4 alpha for beta=0.2,0.5,1", [cHh - b * EH for b in (F(1, 5), F(1, 2), F(1))])
print("L06 example: alpha=-1e6 beta=1/2 high", -1_000_000 + F(1, 2) * EH - cHh, "low", -1_000_000 + F(1, 2) * EL)
print("L06 cH=150k beta", F(150_000, 500_000), "profit", EH * F(7, 10), "FB", EH - 150_000, "agency", EH - 150_000 - EH * F(7, 10))
EH8, EL8 = F(800_000), F(200_000)
print("L06 p=0.8/0.2 beta", F(100_000) / (EH8 - EL8), "profit", EH8 * (1 - F(1, 6)), "rounded", rnd(EH8 * (1 - F(1, 6))), "FB", EH8 - 100_000)
print("L06 identity", (EH - F(1,5)*EH) + (F(1,5)*EH - cHh), EH - cHh)
