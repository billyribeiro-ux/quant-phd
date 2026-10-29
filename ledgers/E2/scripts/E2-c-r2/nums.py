from fractions import Fraction as F
import math, itertools
def EM(n,a):
    t=F(-a)
    for x in range(-a,a):
        t+= 1-F(x+a+1,2*a+1)**n
    return t
e=EM(5,2000)
print("EM(5,2000)=",e, float(e))
print("claimed 85418692002000/64048012001 equal:", e==F(85418692002000,64048012001))
print("20000*EM=",float(20000*e), " half_up floor(-20000*E+1/2)=", math.floor(-20000*e+F(1,2)), " exact unrounded -20000E=",float(-20000*e))
print("E-1333.33333=", float(e-F(4000,3)), " 1333-E=", float(1333-e), " 1334-E=", float(1334-e), " 20000*(1334-E)=", float(20000*(1334-e)))
print("continuous 4000/3=",float(F(4000,3)), "diff shown", float(e-F(4000,3)))
print("n=2,a=1:", EM(2,1), " n=3,a=1:", EM(3,1))
print("shade", math.floor(e+F(1,2)))
print("display 1333.67-1333.33=", round(1333.67-1333.33,2), " 1333.66656-1333.33333 round4=", round(float(e)-1333.33333333,4))
print("52613/79810=", 52613/79810, " 79810/20000=", 79810/20000, " -26620718/20000=", -26620718/20000)
print("-20000E unrounded -26673331.25 vs", float(-20000*e))
print("E[M] 2dp", round(float(e),2), "E 4dp", round(float(e),4))
# Lemma 3.1 / Prop 3.2 check on a grid with lab numbers
# L09 R1 counting
import itertools
cnt=sum(1 for b in itertools.product(range(4),repeat=4) if (lambda s: s[0]==s[1]==s[2])(sorted(b,reverse=True)))
print("L09 equal-rev count (top3 equal)", cnt)
# Def 3.1 witness: values (3,-3,-4,-5), k=2
v=[3,-3,-4,-5]; k=2
top=sorted(v,reverse=True)[:k]; print("witness top-k", top, "sum", sum(top))
# Ratio check on allowable values in L09 with negative values
