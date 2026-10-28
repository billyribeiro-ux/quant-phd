# Independent recomputation for CF1-c round 11 (own formulas; twins exec'd only for the lab constants)
import math
from fractions import Fraction as F
CK = "/tmp/verify11-CF1-c"
ns6 = {"__name__": "l06"}
src6 = open(f"{CK}/tests/labs/CF1/lab-CF1-L06-1.py").read().replace("\nmain()\n", "\n")
exec(compile(src6, "l06", "exec"), ns6)
ns5 = {"__name__": "l05"}
src5 = open(f"{CK}/tests/labs/CF1/lab-CF1-L05-1.py").read().replace("\nmain()\n", "\n")
exec(compile(src5, "l05", "exec"), ns5)
# L06 closed forms, exact
a, m = 50000, 100001
mu = F(a) + F(m - 1, 2)
var = (F(m * m) - 1) / 12
r = F(1, 10)
v = [1 / (1 + r) ** t for t in range(1, 6)]
A = sum(v)
enpv = -300000 + mu * A
vsum2 = sum(x * x for x in v)
varnpv = var * vsum2
print("mu", mu, "E[NPV] exact", float(enpv), "-> 2dp", round(float(enpv), 2))
print("sd", math.sqrt(varnpv), "-> 2dp", round(math.sqrt(varnpv), 2))
# Section 4 bullet 3 / Lab: quantile etc. not recomputed here
# L05 numbers from the twin's constants
A_, B_, D_ = ns5["PROJECT_A"], ns5["PROJECT_B"], ns5["PROJECT_D"]
pb, npv = ns5["payback"], ns5["npv"]
print("npv A,B", round(npv(A_, .1), 2), round(npv(B_, .1), 2), "gap", round(npv(A_, .1) - npv(B_, .1), 2))
print("payback A simple", pb(A_), "B", pb(B_), "D", pb(D_))
print("tail npv min/max from twin lab run (cents)", "see run output")
