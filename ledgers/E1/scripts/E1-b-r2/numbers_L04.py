# Recomputes every unrounded number quoted in L04 prose (Example 3.2, Remark 3.3, Lab 1 interpretation, E1, E2)
from decimal import Decimal as D, getcontext
getcontext().prec = 60
def p(a):
    return (-D(2) + (D(4) + 4*a).sqrt()) / 2
p0 = p(D(120))
dp = 1 / (D(4)+4*D(120)).sqrt()  # 1/sqrt(1+a)/2 -> check below
dp = D(1)/(2*(D(121)).sqrt())
print("dp exact vs 1/22 diff", dp - D(1)/22)
def fwd(h): return (p(D(120)+h)-p0)/h
def cen(h): return (p(D(120)+h)-p(D(120)-h))/(2*h)
hs = [D(1), D("0.1"), D("0.01"), D("0.001")]
fe = [abs(fwd(h)-dp) for h in hs]
ce = [abs(cen(h)-dp) for h in hs]
for h,f,c in zip(hs,fe,ce): print("h",h,"fwd_err",f,"cen_err",c)
print("fwd ratios", [fe[i]/fe[i+1] for i in range(3)])
print("cen ratios", [ce[i]/ce[i+1] for i in range(3)])
print("E1 central ratio h=0.1/h=0.01", ce[1]/ce[2])
print("Remark3.3 ratio h=0.01 fwd/cen", fe[2]/ce[2])
lead_f = D("0.001")/10648; lead_c = D("0.000001")/2576816
print("Ex3.2 fwd leading 0.001/10648", lead_f, "ratio fwd_err(h=.001)/lead", fe[3]/lead_f)
print("Ex3.2 cen leading", lead_c, "ratio cen_err(h=.001)/lead", ce[3]/lead_c, "rel diff", abs(ce[3]/lead_c-1))
print("h=1 central err / leading", ce[0]/(D(1)/2576816), "forward err / leading", fe[0]/(D(1)/10648))
print("E2 p(121.2)", p(D("121.2")), "rise %", (p(D("121.2"))-p0)/p0*100)
print("derivative-based %", dp*12*100/ (D(1)*1) , "(a/p)dp/da %")
print("printed-digit ratio central 0.1/0.01 from printed", D("3.880759e-9")/D("3.880758e-11"))
print("Remark 3.3 printed-digit forward/central", D("9.391047e-7")/D("3.880758e-11"))
print("Remark 3.3 unrounded ratio", fe[2]/ce[2])
print("E2 elasticity 6/11", D(6)/11)
print("Ex 2.4 dQ/da", 20/D(22), 1-D(2)/22)
