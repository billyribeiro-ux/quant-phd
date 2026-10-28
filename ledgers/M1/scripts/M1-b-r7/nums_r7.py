from decimal import Decimal as D, getcontext
getcontext().prec = 60
def exp(x): return x.exp()
r = D("0.05")
ec = exp(r)
errs = {}
for m in [1000, 10000, 100000]:
    f = (1 + r/m) ** m
    errs[m] = ec - f
    print("m", m, "err", round(errs[m], 14), "err10", errs[m].quantize(D("1e-10")))
print("ratio 1000/10000 unrounded", errs[1000]/errs[10000])
print("ratio 10000/100000 unrounded", errs[10000]/errs[100000])
M = D(1000000)
ann = M * (1 + r) ** 10
mon = M * (1 + r/12) ** 120
day = M * (1 + r/365) ** 3650
con = M * exp(r*10)
print("annual", ann, "monthly", mon, "daily", day, "cont", con)
print("mon-ann", mon-ann, "cont-day", con-day, "day-mon", day-mon)
print("ratio (day-mon)/(cont-day)", (day-mon)/(con-day))
print("printed ratio 1656/56", D(1656)/D(56))
# L05
Mv = D(1000000)
semi = Mv * (D("1.025")) ** (-10)
cont = Mv * exp(D("-0.25"))
print("semi5", semi, "cont5", cont, "gap", semi-cont)
a = (D("1.05")) ** (D("-0.5"))
b = D("1.025") ** (-1)
print("t=0.5 annual", a, "semi", b, "diff", a-b, "diff10", (a-b).quantize(D("1e-10")))
print("ann5", Mv*D("1.05")**(-5), "ann-cont", Mv*D("1.05")**(-5)-cont)
# Prop 1.4 check numeric for -1<r<0
r2 = D("-0.05")
print("neg r factor t=1", D("1")+r2, (D(1)+r2)**(-1))
