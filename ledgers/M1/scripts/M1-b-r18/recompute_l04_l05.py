# Independent recomputation of the numbers quoted in L04.html and L05.html (round 18, M1-b).
from decimal import Decimal as D, getcontext, ROUND_HALF_EVEN
from fractions import Fraction
import math
getcontext().prec = 80
r = D("0.05")
def F(rate, m, years=1): return (1 + rate / m) ** (m * years)
print("EAR m=12:", f"{F(r,12)-1:.10f}", "m=1:", f"{F(r,1)-1:.10f}", "m=2:", f"{F(r,2)-1:.10f}", "m=4:", f"{F(r,4)-1:.10f}", "m=365:", f"{F(r,365)-1:.10f}")
ec = (r).exp()
print("e^0.05:", f"{ec:.10f}")
prev = None
errs = {}
for m in (1,2,4,12,52,365,1000,10000,100000,1000000):
    f = F(r,m); errs[m]=ec-f
    print("m", m, f"{f:.10f}", f"{ec-f:.10f}")
print("ratio 1000->10000 unrounded:", f"{errs[1000]/errs[10000]:.5f}", "printed ratio:", f"{D('0.0000013140')/D('0.0000001314'):.3f}")
print("ratio 10000->100000 unrounded:", f"{errs[10000]/errs[100000]:.5f}", "printed:", f"{D('0.0000001314')/D('0.0000000131'):.3f}")
P = 1_000_000
def cents(x): return int(x.quantize(D(1), rounding=ROUND_HALF_EVEN))
a10 = P*F(r,1,10); m10=P*F(r,12,10); d10=P*F(r,365,10); c10=P*(r*10).exp()
print("unrounded cents annual/monthly/daily/cont:", f"{a10:.4f}", f"{m10:.4f}", f"{d10:.4f}", f"{c10:.4f}")
print("rounded:", cents(a10), cents(m10), cents(d10), cents(c10))
print("monthly-annual unrounded:", f"{m10-a10:.2f}", "daily->cont unrounded:", f"{c10-d10:.2f}")
print("monthly-daily printed:", 1648665-1647009, "ratio 1656/56:", f"{1656/56:.4f}", "unrounded gaps:", f"{d10-m10:.2f}", f"{c10-d10:.2f}", f"ratio {(d10-m10)/(c10-d10):.4f}")
print("1-yr factor monthly->daily rise:", f"{F(r,365)-F(r,12):.10f}", "annual->monthly:", f"{F(r,12)-F(r,1):.10f}")
print("EAR cont - F1-1 check: e^0.05 - 1 =", f"{ec-1:.10f}")
print("E2 diff:", f"{F(r,1000000)-ec:.12f}")
# 8% monthly
print("8% monthly EAR:", f"{F(D('0.08'),12)-1:.10f}")
# M2 continuous 6% 3 years
print("M2:", f"{1000*(D('0.18')).exp():.10f}", f"{1000*(D('0.18')).exp()*100:.4f} cents")
# M3 r12
e005_12 = (D('0.05')/12).exp()
print("e^(0.05/12):", f"{e005_12:.12f}", "r12:", f"{12*(e005_12-1):.12f}", f"{12*(e005_12-1):.10f}", f"{12*(e005_12-1):.6f}")
print("check (1+r12/12)^12:", f"{F(12*(e005_12-1),12):.10f}")
# Example 3.2
ex = Fraction(21,20)**10
print("(21/20)^10 =", ex, float(ex), f"{D(ex.numerator)/D(ex.denominator):.20f}")
print("P*factor:", f"{P*D(ex.numerator)/D(ex.denominator):.4f}")
print("cont 0.5 e:", f"{(D('0.5')).exp():.10f}", f"{P*(D('0.5')).exp():.4f}")
# L04 E3 ratio
# L05 numbers
d = D(1)+r
dl = d.ln()
print("delta:", f"{dl:.10f}")
for t in (D('0.5'),D(1),D(2),D(5),D(10)):
    an=1/(1+r)**t; se=1/(1+r/2)**(2*t); co=(-r*t).exp(); eq=(-dl*t).exp()
    print("t",t, f"{an:.10f}", f"{se:.10f}", f"{co:.10f}", f"{eq:.10f}", f"{abs(eq-an):.3e}")
print("t=5 cents:", cents(P/(1+r)**5), cents(P/(1+r/2)**10), cents(P*(-r*5).exp()))
print("t=5 unrounded:", f"{P/(1+r)**5:.4f}", f"{P/(1+r/2)**10:.4f}", f"{P*(-r*5).exp():.4f}")
print("annual-semi printed cents:", 783526-781198, "unrounded:", f"{P/(1+r)**5 - P/(1+r/2)**10:.4f}")
print("semi-cont printed:", 781198-778801, "unrounded:", f"{P/(1+r/2)**10 - P*(-r*5).exp():.4f}")
print("annual-cont printed:", 783526-778801)
print("E1 CU:", (781198-778801)/100)
print("E2 diff:", f"{D('0.9759000729')-D('0.9756097561'):.10f}", f"{(1/(1+r)**D('0.5')) - (1/(1+r/2)**1):.12f}")
print("E2 unrounded:", f"{(1/(1+r)**D('0.5')) - (1/(1+r/2)**1):.10f}")
print("E3 10y annual cents:", f"{P*(1/(1+r)**10):.4f}")
print("M1 L05 1.04^-3:", f"{1/D('1.04')**3:.10f}", f"{1/D('1.04')**3:.6f}", "1.04^3=", D('1.04')**3)
print("M2 L05 250000/1.06^2:", f"{D(250000)/D('1.06')**2:.4f}", f"{D(250000)/D('1.06')**2:.0f}", "1/1.1236=", f"{1/D('1.1236'):.12f}", f"{250000*D('0.88999644'):.4f}")
print("M3 L05:", f"{(D('-0.06')).exp():.10f}", f"{500000*(D('-0.06')).exp():.4f}")
print("R2 L05 root:", f"{(1/D('0.6'))**(D(1)/10):.12f}", f"{(D(1)/D('0.6')).ln()/10:.7f}", f"{(D(1)/D('0.6'))**(D(1)/10)-1:.8f}")
print("R2 check:", f"{(D('1.052409779149'))**10:.10f}", f"{1/(D('1.052409779149')**10):.10f}", f"{(D('1.0524097791'))**10:.10f}")
print("R2 10(1+r)^9:", f"{10*D('1.052409779149')**9:.4f}", "error in 1+r:", f"{D('1.052409779149')-D('1.0524097791'):.3e}")
print("R3 L05 e^0.05-1:", f"{ec-1:.10f}", "5.1271%:", f"{(ec-1)*100:.4f}")
print("L05 misc: 0.7835261665 ", f"{1.05**-5:.10f}", "e^-0.25", f"{math.exp(-0.25):.10f}")
print("2328 gap unrounded check:", f"{P/(1+r)**5 - P/(1+r/2)**10:.2f}")
print("L05 E3 613913:", f"{P*(1/(1+r)**10):.2f}")
print("Example 3.1 semi PV:", f"{P/(1+r/2)**10:.2f}", "cont PV:", f"{P*(-r*5).exp():.2f}", f"{math.exp(-0.25):.10f}")
print("misc: ln(1.05)<0.05", dl < r, "Prop 2.2 ratio check", float(dl))
print("L05 M1 M2 printed 0.88999644:", f"{1/(1.06**2):.12f}")
print("L04 Remark: 0.0001055986:", f"{F(r,365)-F(r,12):.10f}", "0.0011618979:", f"{F(r,12)-1-r:.10f}")
print("L04 misc: 0.0106 pp:", f"{(F(r,365)-F(r,12))*100:.8f}")
print("L04 E3 ratio:", f"{1656/56:.10f}")
print("L04 E2 e^0.05 digits:", f"{ec:.12f}", f"{F(r,1000000):.12f}")
print("R3 L04 1+r/m check e^(r/m)m", f"{(D(r)/12).exp()**12:.10f}")
