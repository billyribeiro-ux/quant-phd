from decimal import Decimal as D, getcontext
getcontext().prec = 60
def p(a):
    b=D(2); d=D(1)
    return (-b + (b*b+4*a*d).sqrt())/(2*d)
p0=p(D(120)); dp=D(1)/D(22)
hs=[D(1),D("0.1"),D("0.01"),D("0.001")]
fe={};ce={}
for h in hs:
    f=(p(D(120)+h)-p0)/h; c=(p(D(120)+h)-p(D(120)-h))/(2*h)
    fe[h]=abs(f-dp); ce[h]=abs(c-dp)
    print("h",h,"fwd",f,"fe",fe[h],"ce",ce[h])
print("fwd ratios",[float(fe[hs[i]]/fe[hs[i+1]]) for i in range(3)])
print("cen ratios",[str(ce[hs[i]]/ce[hs[i+1]]) for i in range(3)])
print("ratio fwd/cen at 0.01", fe[D("0.01")]/ce[D("0.01")])
print("ratio fwd err to leading at 0.001", fe[D("0.001")]/(D("0.001")/10648))
print("central err to leading at 0.001", ce[D("0.001")]/(D("1e-6")/2576816))
print("central at 1 to leading", ce[D(1)]/(D(1)/2576816), "fwd at 1", fe[D(1)]/(D(1)/10648))
print("leading fwd 0.001", D("0.001")/10648, "central leading", D("1e-6")/2576816)
q=p(D("121.2")); print("exact p(121.2)",q, "pct", (q-p0)/p0*100, "deriv pct", dp*120/p0)
print("lead ratio at 0.01 fwd err/ce", )
