from decimal import Decimal as D, getcontext
getcontext().prec = 80
def p(a): return (D(1)+a).sqrt()-D(1)
a0 = D(120); p0 = p(a0); dp = 1/(2*(D(1)+a0).sqrt())
print("p0", p0, "dp", dp, dp - D(1)/22)
# (a) exact percent change for a from 120 to 121.2
r = (p(D("121.2"))-p0)/p0*100
print("pct_change_121.2", r)
print("p(121.2)", p(D("121.2")))
# forward and central unrounded errors
ferr={}; cerr={}
for h in [D(1), D("0.1"), D("0.01"), D("0.001")]:
    f=(p(a0+h)-p0)/h; c=(p(a0+h)-p(a0-h))/(2*h)
    ferr[h]=abs(f-dp); cerr[h]=abs(c-dp)
    print("h",h,"ferr",ferr[h],"cerr",cerr[h])
hs=[D(1), D("0.1"), D("0.01"), D("0.001")]
for i in range(3):
    print("forward ratio", hs[i], "/", hs[i+1], ferr[hs[i]]/ferr[hs[i+1]], " central ratio", cerr[hs[i]]/cerr[hs[i+1]])
# Example 3.2 leading terms
lead_f = lambda h: h/D(10648)
lead_c = lambda h: h*h/D(2576816)
print("h=0.001 leading forward", lead_f(D("0.001")), "ratio unrounded/leading", ferr[D("0.001")]/lead_f(D("0.001")) )
print("signed ratio forward (f-dp)/lead", ((p(a0+D("0.001"))-p0)/D("0.001")-dp)/(-lead_f(D("0.001"))))
print("h=0.001 leading central", lead_c(D("0.001")), "unrounded", cerr[D("0.001")], "rel diff", (cerr[D("0.001")]-lead_c(D("0.001")))/lead_c(D("0.001")))
print("h=1 central ratio to leading", cerr[D(1)]/lead_c(D(1)))
print("h=1 forward ratio to leading", ferr[D(1)]/lead_f(D(1)))
# Remark 3.3
fe=ferr[D("0.01")]; ce=cerr[D("0.01")]
print("h=0.01 fwd", fe, "cen", ce, "ratio", fe/ce)
print("h=0.01 forward signed", (p(a0+D("0.01"))-p0)/D("0.01")-dp)
print("h=0.1 central", (p(a0+D("0.1"))-p(a0-D("0.1")))/(2*D("0.1"))-dp)
