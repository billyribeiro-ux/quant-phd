from decimal import Decimal as D, getcontext, ROUND_HALF_UP
from fractions import Fraction as F
getcontext().prec = 60
def q(x, p): return D(x).quantize(D(1).scaleb(-p), rounding=ROUND_HALF_UP)
ln = lambda x: D(x).ln()
l11 = ln(D("1.1")); print("ln1.1", l11, q(l11, 6), "| 0.1-ln1.1", q(D("0.1") - l11, 6), D("0.1") - l11)
# M2
v = [D("0.01"), D("0.03"), D("-0.02")]; mean = sum(v) / 3
ss = sum((x - mean) ** 2 for x in v); print("M2 mean", q(mean, 6), "SS", ss, "19/15000=", float(F(19, 15000)), "sd", q((ss / 2).sqrt(), 6), (ss/2).sqrt())
# R2/E: L = 0.135846 -> h = tanh(L/2); use exact printed-unrounded L from recheck (0.13584567 printed as 0.135846)
for L in (D("0.13584567"), D("0.135846")):
    h = ((L).exp() - 1) / ((L).exp() + 1)
    print("L", L, "h", h, "->", q(h, 6), "4dp", q(h, 4))
b = ln((D("1.0678")) / D("0.9322")); print("bound at h=0.0678", b, q(b, 6), q(b, 4))
bound_exact = ln(D(1) + D("0.067819") ) - ln(D(1) - D("0.067819")); print("bound at h=0.067819", bound_exact, q(bound_exact, 6))
e = D("-0.09657474"); print("2008-10 simple change", (e.exp() - 1), q(e.exp() - 1, 6))
print("ln(1.0678/0.9322) for quiz", q(b, 6))
# P2/R2: 0.0678 bound vs L
print("0.0678 bound 0.135808 <0.135846 ->", b < D("0.13584567"))
print("h=tanh(0.13584567/2)", ((D("0.13584567")/2).exp()*0 ) )
