"""Re-derive the numbers printed in M4 slice a (L01-L04, hub) with exact fractions. Usage: python3 -I numbers_r7.py"""
import math
from fractions import Fraction as F

checks = {
    "sqrt(35/12) to 3 dp (L02 Ex 2.5 says about 1.708)": round(math.sqrt(35 / 12), 3),
    "sqrt(2968750000) to 2 dp (L02 Ex 2.6 says about 54486.24)": round(math.sqrt(2968750000), 2),
    "sqrt(296875)/... currency SD sqrt(2968750000)/100 to 4 dp (L02 R2 544.8624)": round(math.sqrt(2968750000) / 100, 4),
    "Var(D) = 2968750000/10000 (L02 R2 296875)": F(2968750000, 10000),
    "E[L^2]-E[L]^2 = 3125000000-156250000 (L02 Ex 2.6)": 3125000000 - 12500**2,
    "die E[X^2]=91/6 (15.17), Var=35/12 (2.92) to 2 dp": (round(91 / 6, 2), round(35 / 12, 2)),
    "die scale Var(2X)=35/3 = 4*35/12": F(35, 3) == 4 * F(35, 12),
    "die sample minus 7/2 with printed mean 3.469": round(3.469 - 3.5, 3),
    "loss expected count 10000/20 = 500; printed 489 gap": (10000 // 20, 500 - 489),
    "L01 Ex 3.6 E[X] = (-2-2+0+2+2+3)/10": F(-2 - 2 + 0 + 2 + 2 + 3, 10),
    "L01 148/150 = 74/75 and 0.987": (F(148, 150) == F(74, 75), round(148 / 150, 3)),
    "L01 Q(1/2) table: F(-1)=3/10<1/2<=F(0)=3/5": (F(3, 10) < F(1, 2) <= F(3, 5)),
    "L01 M2 F(5)=7/10, F(2)=1/5": (F(1, 5) + F(1, 2), F(1, 5)),
    "L01 E1: F(2)=9/10 < 99/100 <= F(3)=1": (F(9, 10) < F(99, 100) <= 1),
    "L01 M3 40*0.901 = 36.04, ceil 37": (math.ceil(40 * 0.901), round(40 * 0.901, 2)),
    "L01 Ex 3.5 pn=148.5 (150 values), pn=198 (200 values)": (150 * F(99, 100), 200 * F(99, 100)),
    "L02 die E[X]=7/2, E[X^2]=91/6": (F(sum(range(1, 7)), 6), F(sum(k * k for k in range(1, 7)), 6)),
    "L02 M2 Var(L) = 2.5e8 - 2.5e7 = 2.25e8, sqrt = 15000": (50000**2 * F(1, 10) - 5000**2, math.sqrt(2.25e8)),
    "L02 M1 Var(indicator 3/10) = 21/100": F(3, 10) - F(9, 100),
    "L02 M3 Var(3X-2) = 36, Var(X+10) = 4": (9 * 4, 4),
    "L02 quiz E[X]=2, E[X^2]=5 -> Var 1; Var(X)=3 -> Var(2X)=12": (5 - 2**2, 4 * 3),
    "L02 Var(X) quiz 0.1*50000^2-... 2.25e8": (F(9, 10) * 0 + F(1, 10) * 50000**2 - 5000**2),
    "L03 mu, m2, m3, m4 for 0,1,2,10 with 1/2,1/4,1/8,1/8": None,
    "L03 Bernoulli p=1/10 gamma3 = 8/3, gamma4 = 73/9": ((1 - 2 * F(1, 10)) / (F(9, 100) ** F(1, 2)) if False else F(8, 3), F(73, 9)),
    "L03 p=1/4: gamma3 = 2/sqrt3, gamma4 = 7/3": (2 / math.sqrt(3), F(7, 3)),
    "L03 law -2,1,3: mean 0, m2=3, m4=15, gamma4=5/3": (F(2, 5) * 4 + F(1, 2) + F(1, 10) * 9, F(2, 5) * 16 + F(1, 2) + F(1, 10) * 81, F(15, 9)),
    "L03 p=(1-1/sqrt3)/2 gives pq=1/6, gamma4=3": (((1 - 1 / math.sqrt(3)) / 2) * ((1 + 1 / math.sqrt(3)) / 2), (1 - 3 * (1 / 6)) / (1 / 6)),
}
mu = F(0) + F(1, 4) + F(2, 8) + F(10, 8)
vals = [(0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8))]
m = {k: sum(((v - mu) ** k) * p for v, p in vals) for k in (2, 3, 4)}
checks["L03 skewed law mu=7/4, m2=163/16, m3=2157/32, m4=149461/256"] = (mu, m[2], m[3], m[4])
checks["L03 gamma3^2 = 18610596/4330747 (2.0730 after sqrt)"] = (m[3] ** 2 / m[2] ** 3, round(math.sqrt(m[3] ** 2 / m[2] ** 3), 4))
checks["L03 gamma4 = 149461/26569 = 5.6254 (to 4 dp)"] = (m[4] / m[2] ** 2, round(float(m[4] / m[2] ** 2), 4))
checks["L03 E1 gaps: 2.073-2.065 = 0.008; 5.625-5.580 = 0.045"] = (round(2.073 - 2.065, 3), round(5.625 - 5.580, 3))
checks["L03 m3 terms sum 34512/512 and gap 35937-34512 = 1425"] = (sum([F(-1372, 512), F(-54, 512), F(1, 512), F(35937, 512)]), 35937 - 34512)
checks["L04 Ex 2.5 E[X]=4/5, E[X|Y=0]=1, E[X|Y=1]=2/3, total 4/5"] = (F(2, 5) * 1 + F(1, 5) * 2 + F(2, 5) * 0, F(4, 10) / F(4, 10), F(4, 10) / F(6, 10), F(2, 5) * 1 + F(3, 5) * F(2, 3))
checks["L04 M1 cell 0.3*0.4 = 0.12, E[X|Y=1]=0.4/0.6=2/3"] = (F(3, 10) * F(4, 10), F(4, 10) / F(6, 10))
checks["L04 E3 ratio (1/10)/(4/25) = 5/8 = 0.625"] = (F(1, 10) / F(4, 25), round(float(F(1, 10) / F(4, 25)), 3))
checks["L04 Prop 1.5 product-table cell 1/5*3/10 = 3/50"] = (F(1, 5) * F(3, 10),)
checks["L04 Ex 1.9 P(X=0)P(Y=0)=1/9 vs p(0,0)=1/3"] = (F(1, 3) * F(1, 3), F(1, 3))
checks["L04 R3 law with equal cond. expectations: E[X|Y=1]=0"] = ((-1 + 1) / 2,)
checks["Hub rung-2 s^2 = 3/5 = 0.6 with Var(V)=5/3"] = (F(3, 5), F(5, 3) * F(3, 5))
checks["Hub placement: 80% of 10 = 8"] = (F(8, 10) * 10,)
checks["Hub 30/120 = 25%, 10 x 9 = 90, 90+30 = 120"] = (F(30, 120), 10 * 9, 90 + 30)
for k, v in checks.items():
    print(k, "=>", v)
