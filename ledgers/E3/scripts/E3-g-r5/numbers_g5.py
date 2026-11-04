from fractions import Fraction as F
from decimal import Decimal as D, getcontext
import math
getcontext().prec = 60
# L07 weighting
def om(p, eta=0.5):
    return p**eta / (p**eta + (1-p)**eta) ** (1/eta)
def om_closed(p):
    return math.sqrt(p) / (1 + 2*math.sqrt(p*(1-p)))
def om40(p):
    p = D(p)
    s = p.sqrt(); t = (1-p).sqrt()
    return s / (1 + 2*(p*(1-p)).sqrt())
print("omega(3/10) 40d", om40(D(3)/D(10)))
print("omega(3/5) 40d", om40(D(3)/D(5)))
print("omega(2/5) 40d", om40(D(2)/D(5)))
print("omega(1/2) 40d", om40(D("0.5")))
g_a1 = D(50)**1*0 + om40(D(3)/D(10))*(D(50)+D(100)) if False else None
gA = om40(D(3)/D(10))*D(50) + om40(D(3)/D(10))*D(100)
gB = om40(D(3)/D(5))*D(100)
print("Gamma(A) a=1 40d", gA, "Gamma(B) a=1", gB, "diff", gA-gB)
gA5 = om40(D(3)/D(10))*(D(50).sqrt()+D(100).sqrt())
gB5 = om40(D(3)/D(5))*D(100).sqrt()
print("Gamma(A) a=0.5", gA5, "Gamma(B) a=0.5", gB5)
r = om40(D(3)/D(10))/om40(D(3)/D(5))
print("ratio", r)
print("thr a=1", D(2)/D(3), "thr a=1/2", 1/(1+D(2).sqrt()**-1 if False else 1/(1+1/D(2).sqrt())))
print("thr a=1/2 exact", 1/(1+1/D(2).sqrt()))
# omega minus p sign changes and last grid point
grid = [i/1000 for i in range(1001)]
diffs = [om_closed(p) - p for p in grid]
above = [i for i in range(1,1000) if diffs[i] > 0]
print("last grid point with omega>p:", grid[max(above)], "index", max(above))
ch = [i for i in range(1,1000) if (diffs[i]>0) != (diffs[i+1]>0)]
print("sign change interior indices (i, i+1):", [(grid[i], grid[i+1]) for i in range(1,999) if (diffs[i]>0)!=(diffs[i+1]>0)])
# general formula vs closed form gap; eta=1 gap
gap1 = max(abs(p - om_closed(p)) for p in grid)
argmax = max(grid, key=lambda p: abs(p-om_closed(p)))
print("eta=1 vs closed form largest gap", gap1, "at p", argmax)
print("prose-claim gap p=0.862:", abs(0.862-om_closed(0.862)))
print("om(0.01), om(0.99), 100*om(.01)+50*om(.99)", om_closed(0.01), om_closed(0.99), 100*om_closed(0.01)+50*om_closed(0.99))
print("overweight", (om_closed(0.01)-0.01)*100, "underweight", (0.99-om_closed(0.99))*50)
print("omega(1/4)", om_closed(0.25), 2-math.sqrt(3))
# L07 part C unrounded diff
print("unrounded diff 40d", gA-gB)
print("8 decimal diff", D("42.86863274")-D("39.12507700"))
# L05 numbers
print("CE1 values", F(8,5), F(12,5))
print("CE1 check 1/(5/8)", 1/F(5,8), "1/(5/12)", F(12,5))
