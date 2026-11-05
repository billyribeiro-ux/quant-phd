from fractions import Fraction as F
# L04 Part A table as printed (forecast, realised)
pairs = [(99,95),(99,96),(99,97),(105,94),(105,98),(105,105),(99,95),(100,101),(105,99),(102,96),(104,99),(102,105),(100,101),(105,97),(97,95),(101,95),(105,97),(100,101),(103,95),(97,99),(104,95),(100,96),(101,103),(97,98)]
e = [f - r for f, r in pairs]
H = len(e)
h = [1 if abs(x) <= 2 else 0 for x in e]
print("H", H, "errors", e, "sum", sum(e))
print("hits", sum(h), "hit rate", F(sum(h), H), float(F(sum(h), H)))
print("bias", F(sum(e), H), float(F(sum(e), H)))
print("MAE", F(sum(abs(x) for x in e), H))
# Part B windows
for name, sl in [("first12", slice(0, 12)), ("last12", slice(12, 24))]:
    ee = e[sl]; hh = h[sl]
    print(name, "hit", F(sum(hh), len(ee)), "bias", F(sum(ee), len(ee)), float(F(sum(ee), len(ee))))
# Part C
ec = [3, -3, 3, -3]
print("PartC hits", sum(1 if abs(x) <= 2 else 0 for x in ec), "bias", F(sum(ec), 4), "MAE", F(sum(abs(x) for x in ec), 4))
# Part D enumeration
cnt = sum(1 for V in range(-4, 5) for U in range(-6, 7) if -3 <= V - U <= 1)
tot = 9 * 13
mean = sum(1 + V - U for V in range(-4, 5) for U in range(-6, 7)) / tot
print("P(hit)", F(cnt, tot), float(F(cnt, tot)), "E[e]", F(sum(1 + V - U for V in range(-4, 5) for U in range(-6, 7)), tot))
# rounding rule: sign(x) floor(|x|*1e4 + 1/2)/1e4
import math
def disp(x):
    s = -1 if x < 0 else 1
    return s * math.floor(abs(x) * 10**4 + F(1, 2)) / 10**4
print("disp 41/12", disp(F(41, 12)), "disp 3/8", disp(F(3, 8)), "disp -1/2*0.00005", disp(F(-1, 20000)))
# L03 ratios
print("3/104 vs 6/97", F(3,104) < F(6,97), 3*97, 6*104)
print("21/37 < 2", F(21,37) < 2)
