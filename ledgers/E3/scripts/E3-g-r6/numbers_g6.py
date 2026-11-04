# Independent recomputation (E3 slice g, round 6). Exact Fractions and 60-digit Decimal; no code is shared with the builders.
from fractions import Fraction as F
from decimal import Decimal as D, getcontext
getcontext().prec = 60
def sq(x): return D(x).sqrt()
def om(p):  # omega_{1/2}(p) closed form, p a Decimal or Fraction
    p = D(p.numerator)/D(p.denominator) if isinstance(p, F) else D(p)
    return sq(p) / (1 + 2*sq(p*(1-p)))
def om_general(p):  # p^eta/(p^eta+(1-p)^eta)^(1/eta), eta=1/2 ; p Decimal
    e = D("0.5")
    return (sq(p)) / ((sq(p) + sq(1-p)) ** 2)
def show(name, v, digits=12): print(f"{name} = {D(v):.{digits}f}")
print("== L07 weights (closed form and general formula agree)")
for p in [F(3,10), F(3,5), F(1,2), F(2,5), F(1,4), F(1,100), F(99,100)]:
    pd = D(p.numerator)/D(p.denominator)
    show(f"omega({p})", om(p), 12)
    assert abs(om(p) - om_general(pd)) < D("1e-50")
show("omega(3/10) 8dp rounding check", om(F(3,10)), 10)
r = om(F(3,10)) / om(F(3,5))
show("ratio omega(3/10)/omega(3/5)", r, 10)
show("ratio of 8dp displayed values", D("0.28579088")/D("0.39125077"), 10)
show("threshold 1/(1+2^-1/2) (alpha=1/2)", 1/(1+1/sq(D(2))), 10)
show("threshold alpha=1 = 2/3", D(2)/3, 10)
show("Remark 1.6 weight sum omega(2/5)+2omega(3/10)", om(F(2,5)) + 2*om(F(3,10)), 10)
show("2 omega(3/10)", 2*om(F(3,10)), 10)
show("omega(2/5)", om(F(2,5)), 10)
show("M1 2-sqrt3", 2 - sq(D(3)), 10)
show("M2 1/(2 sqrt2)", 1/(2*sq(D(2))), 10)
print("== L07 Gamma values (alpha=1 and alpha=1/2)")
gA1 = om(F(3,10))*150; gB1 = om(F(3,5))*100
show("Gamma(A) alpha=1", gA1, 8); show("Gamma(B) alpha=1", gB1, 8)
show("difference unrounded", gA1-gB1, 8)
show("difference of 8dp displayed", D("42.86863274")-D("39.12507700"), 8)
show("Gamma(A) alpha=1/2", om(F(3,10))*(sq(D(50))+sq(D(100))), 8)
show("Gamma(B) alpha=1/2", om(F(3,5))*sq(D(100)), 8)
print("== L07 crossing omega(p)=p: root of 1 = sqrt(p) + 2 p sqrt(1-p)")
lo, hi = D("0.278"), D("0.279")
f = lambda p: om(None) if False else sq(p)/(1+2*sq(p*(1-p))) - p
print("sign at 0.278:", f(lo) > 0, " sign at 0.279:", f(hi) < 0)
for _ in range(120):
    mid = (lo+hi)/2
    if f(mid) > 0: lo = mid
    else: hi = mid
show("crossing", (lo+hi)/2, 10)
print("== L07 grid facts (floats, mirrors lab)")
import math
grid = [i/1000 for i in range(1001)]
def omf(p): return math.sqrt(p)/(1+2*math.sqrt(p*(1-p))) if 0 < p < 1 else p
vals=[omf(p) for p in grid]
ch = sum(1 for i in range(1,1000) if (omf(grid[i])>grid[i]) != (omf(grid[i+1])>grid[i+1]))
print("interior sign changes", ch, " last grid p with omega>p:", max(p for p in grid[1:-1] if omf(p)>p))
print("max |closed - (1)*p| if eta=1 (omega_1(p)=p) gap of the eta=1/2 closed form:",
      max((abs(omf(p)-p), p) for p in grid[1:-1]))
print("== L07 misconception 3 (small prize)")
w01 = om(F(1,100)); w099 = om(F(99,100))
wv = w01*100 + w099*50
ev = F(1,100)*100 + F(99,100)*50
show("weighted value", wv, 6); show("EV", D(ev.numerator)/D(ev.denominator), 2)
show("overweight", (w01-D(1)/100)*100, 4); show("underweight", (D(99)/100 - w099)*50, 4)
show("net", wv - D(ev.numerator)/D(ev.denominator), 4)
print("== L08")
w1, wL = F(110000), F(95000)
def ce(p): return 1/(p/w1 + (1-p)/wL)
print("EU CE 4180000/41 =", float(4180000/41), " ce(1/2) exact:", ce(F(1,2)), "as Fraction ==4180000/41:", ce(F(1,2)) == F(4180000,41))
show("risk premium 102500-CE", D(102500) - D(4180000)/D(41), 6)
print("exact premium 22500/41 =", F(22500,41), float(F(22500,41)))
print("ce(1/4) =", ce(F(1,4)), float(ce(F(1,4))), " ce(3/4)=", float(ce(F(3,4))), " ce(1/3)=", float(ce(F(1,3))))
print("ce(1/4) to 6dp:", "{:.6f}".format(float(ce(F(1,4)))))
print("EXPECTED final wealth at 1/4:", F(1,4)*110000 + F(3,4)*95000)
print("maxmin (p=1/3) =", float(ce(F(1,3))), " 2dp", "{:.2f}".format(float(ce(F(1,3)))))
print("== Example 2.5 (u(w)=-1/w; wealth 110000 vs 100000)")
def ce_b(p): return 1/(p/F(110000) + (1-p)/F(100000))
print("known red", float(ce_b(F(1,3))), " known black", float(ce_b(F(2,3))))
print("ambiguous 30..60 red at p=1/3:", float(ce_b(F(1,3))), " black at red prob 2/3 -> black prob 1/3:", float(ce_b(F(2,3))))
print("E1 difference 103125-100000 =", 103125-100000)
print("== Model 2 (prospect, alpha=delta=1/2, lambda=2; CU)")
Vp = F(1,2)*0 + 0  # placeholder to keep structure explicit
Vp = D(5) - sq(D(50))
print("V_p =", Vp)
ceCU = -((-Vp/2)**2)
show("CE of change CU", ceCU, 6); show("wealth equiv cents", D(100000) + 100*ceCU, 4)
print("== Remark 3.2 lambda_R for p=1/3, EV=400/3, alpha=delta=1/2")
EV = F(1,3)*1000 - F(2,3)*300
print("EV =", EV, float(EV))
lamR = (F(1,3)*(1000-EV)) / (F(2,3)*(300+EV))  # alpha=delta=1/2 -> sqrt of ratio
print("ratio of distances (g-EV)/(l+EV) =", (1000-EV)/(300+EV), " lambda_R = (1/2)*sqrt(2) =", float(D(1)/2*sq(D(2))))
print("== L06 numbers")
print("lambda* sqrt(5/3) =", sq(D(5)/D(3)))
print("W(2), alpha=delta=1/2 =", sq(D(1000))/2 - 2*sq(D(600))/2)
print("== L05 numbers")
print("CE1 {1,4} gamma=2:", F(1)/ (F(1,2)*1 + F(1,2)*F(1,4)), " {2,3}:", F(1)/(F(1,2)*F(1,2)+F(1,2)*F(1,3)))
print("gamma=0.5 CE1 {1,4}:", float(((sq(D(1))+sq(D(4)))/2)**2), " gamma=3 CE1:", float((D(1)/2+D(1)/2*D(1)/16)**D("-0.5")))
V0 = 1/((F(1,20)+F(9,10)*F(5,8)))
print("V0 =", V0, " U =", -(F(1,20)+F(9,16)))
print("E2 V0 =", 1/(F(1,20)+F(9,10)*F(7,16)), " CE =", 1/(F(1,4)*1 + F(3,4)*F(1,4)))
print("V0(1,10) at psi=2 =", float(((D(1)/2 + D(1)/2*sq(D(10)))**2)))
print("V0(4,4) at psi=2 =", ((D(1)/2*sq(D(4)) + D(1)/2*sq(D(4))))**2)
print("theta at gamma=2, psi=2 =", (1-2)/(1-F(1,2)))
