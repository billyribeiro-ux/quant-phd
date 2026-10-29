from decimal import Decimal as D, getcontext
from fractions import Fraction as F
getcontext().prec = 60
a0 = D(120)
def p(a): return (-D(2) + (D(4) + 4*a).sqrt())/2
p0 = p(a0)
dp = D(1)/22
print("p0", p0, "dp", dp)
steps=[D(1),D("0.1"),D("0.01"),D("0.001")]
fe=[];ce=[]
for h in steps:
    up=p(a0+h); lo=p(a0-h)
    f=(up-p0)/h; c=(up-lo)/(2*h)
    fe.append(abs(f-dp)); ce.append(abs(c-dp))
    print("h",h,"fwd",f,"fe",fe[-1],"cen",c,"ce",ce[-1])
for i in range(3):
    print("fwd ratio",i, fe[i]/fe[i+1], " cen ratio", ce[i]/ce[i+1])
print("fwd h=0.01 unrounded", fe[2], "cen", ce[2], "ratio", fe[2]/ce[2])
print("price elasticity a-change 1.2:", (p(a0+D("1.2"))-p0)/p0*100, "p(121.2)", p(D("121.2")))
print("ratio(1%)", ((p(D("121.2"))-p0)/p0*100))
print("eps in a", a0/p0*dp)
# leading terms
lead_f_h1 = D(1)/10648; lead_c_h1 = D(1)/2576816
print("lead fwd h=0.001", D("0.001")/10648, "ratio fwd err/lead", fe[3]/(D("0.001")/10648))
print("lead cen h=0.001", D("1e-6")/2576816, "ratio cen/lead", ce[3]/(D("1e-6")/2576816), "minus1", ce[3]/(D("1e-6")/2576816)-1)
print("h=1 cen/lead", ce[0]/lead_c_h1, "fwd/lead", fe[0]/lead_f_h1)
print("D(1e-6/2576816)", D("1e-6")/2576816)
print("ratio 0.1->0.01 cen printed", D("3.880759e-9")/D("3.880758e-11"))
print("ratio fe/ce at 0.01", fe[2]/ce[2])
