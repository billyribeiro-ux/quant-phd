from fractions import Fraction as F
import math
c=F(3,5); dG=10000
S=lambda N: sum(dG*c**k for k in range(N))
print("S5", S(5), "S1/total", S(1)/(F(dG)/(1-c)))
print("share20", float(1-c**20), round(float(1-c**20),6), "gap20", float(25000*c**20), "gap10", float(25000*c**10), "gap30", float(25000*c**30))
print("9stages", float(c**9), "10stages", float(c**10), float(c**10)<=0.01, float(c**9)>0.01)
print("tax/spend", F(-15000,25000))
print("R2 mult", 1/(1-c*(1-F(1,2))), "lump", 1/(1-c))
print("M1 L08", 1/(1-F(1,2)), 40*F(1,2)**0)
print("R2 L07", 1/F(3,2), float(F(1,1)/F(3,2)))
print("L07 y for i=4", (4-(1+3+F(3,2)*1))/F(1,2))
print("L07 neg gap threshold", "y<-1 at pi=1 ->", [ (y, F(1,2)+F(1,2)*y) for y in (-1,-2)])
# percent-of-trend ranking witness
print("ranking witness: date1 gap 2 trend 10 ->", 100*F(2,10), "; date2 gap 3 trend 100 ->", 100*F(3,100), "; units ranking date2>date1:", 3>2, "pct ranking date1>date2:", 100*F(2,10)>100*F(3,100))
# Prop 2.3 bound check
bad=[]
for cc in [F(1,10),F(3,5),F(9,10),F(99,100)]:
    for N in range(1,200):
        if cc**N > 1/(1+N*(1/cc-1)): bad.append((cc,N))
print("prop2.3 bound violations", bad[:3], len(bad))
# Prop 2.2 without A2: iff holds for negative phi
for phi in [F(-1,2),F(0),F(1,2)]:
    d=phi*(F(3)-F(1)); print("phi",phi,"diff",d,"strictly increasing", d>0)
# R1 L08 c=1 check: S_N = N dG
print("c=1 S3", 3*dG)
# L07 part D/B/C
phi=F(3,2); r=F(1);t=F(2)
i=lambda p,y,ph,py: r+p+ph*(p-t)+py*y
print("L07 nominal at 1..5 y0", [i(F(p),0,phi,F(1,2)) for p in range(1,6)])
print("L07 E1", i(F(5),F(2),phi,F(1,2)))
print("L07 P3/Q2", i(F(3),F(-1),phi,F(1,2)))
