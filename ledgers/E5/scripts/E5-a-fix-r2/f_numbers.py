import math
from fractions import Fraction
from pathlib import Path

src = Path("/Users/billyribeiro/dev/quant-phd/tests/labs/E5/lab-E5-L02-1.py").read_text()
src = src.rsplit("\nmain()", 1)[0]
ns: dict = {}
exec(compile(src, "twin", "exec"), ns)
sim, log_growth, residual_growth, mean = ns["simulate_economy"], ns["log_growth"], ns["residual_growth"], ns["mean"]
A, K, L, Y = sim(2026, 40)
dy, dk, dl = log_growth(Y), log_growth(K), log_growth(L)
mk, ml, my = mean(dk), mean(dl), mean(dy)
print("mean dlnK", repr(mk), "mean dlnL", repr(ml), "mean dlnY", repr(my))
print("0.3*mean dlnK", 0.3 * mk, "0.7*mean dlnL", 0.7 * ml)
print("0.4*mean dlnK", 0.4 * mk, "0.4*mean dlnK 6dp", f"{0.4*mk:.6f}")
print("0.3*mean dlnK / 0.3 check rounded 0.035557 * 0.4 =", 0.4 * 0.035557)
r2 = residual_growth(dy, dk, dl, 0.2); r4 = residual_growth(dy, dk, dl, 0.4)
m2, m4 = mean(r2), mean(r4)
print("mean res 0.2", repr(m2), "mean res 0.4", repr(m4), "diff", m2 - m4, "prop 2.4 pred", 0.2 * (mk - ml))
print("diff 6dp", f"{m2-m4:.6f}")
print("printed diff from rounded", round(m2,6)-round(m4,6))
print("mean simple", mean([y1/y0-1 for y0,y1 in zip(Y[:-1],Y[1:])]))
print("1.1^0.3", 1.1**0.3, "1.1^0.3-1", 1.1**0.3-1, "0.3 ln1.1", 0.3*math.log(1.1), "0.3*0.1", 0.03)
print("0.3 ln2", 0.3*math.log(2), "ln2", math.log(2))
print("shares unrounded", 0.3*mk/my, 0.7*ml/my, mean(r2 if False else residual_growth(dy,dk,dl,0.3))/my)
# exact check of Prop 2.4 per period
r3 = residual_growth(dy, dk, dl, 0.3)
print("per-period diff check max", max(abs((x - y) - (-(0.2))*(a-b)) for x,y,a,b in zip(r2,r4,dk,dl)))
