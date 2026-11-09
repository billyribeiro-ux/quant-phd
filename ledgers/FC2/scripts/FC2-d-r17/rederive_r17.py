"""Independent re-derivation of the numbers printed in FC2 project.html (verifier round 17)."""
from fractions import Fraction as F
import math

def rnd(x):  # tie toward +infinity, floor(x + 1/2)
    return math.floor(x + F(1, 2))

def gap(c, p, s, k, df):
    return F(c) - F(p) - (F(s) - F(k) * F(df, 10**6))

def chord_less_call(ks, cs, j):
    lo, mi, hi = ks[j-1], ks[j], ks[j+1]
    wl, wh = F(hi - mi, hi - lo), F(mi - lo, hi - lo)
    return wl * cs[j-1] + wh * cs[j+1] - cs[j]

def scan_numbers(ks, cs, ps, s, df, cost):
    out = []
    for k, strike in enumerate(ks):
        g = gap(cs[k], ps[k], s, strike, df)
        out.append(("parity", strike, rnd(g), rnd(abs(g)), rnd(abs(g)) - cost))
    for j in range(1, len(ks) - 1):
        d = chord_less_call(ks, cs, j)
        out.append(("chord", ks[j], str(d), rnd(-d) if d < 0 else 0, (rnd(-d) - cost) if d < 0 else None))
    return out

print("LAB1 cost 45")
for r in scan_numbers([9000,9500,10000,10500,11000,11500],[1500,1100,800,700,450,350],[410,385,700,1095,1360,1735],10000,990000,45): print(" ", r)
print("LAB3 cost 60")
for r in scan_numbers([4000,4500,5000,6000,6500,7000],[1210,820,500,330,151,90],[10,155,250,1030,1100,1200],5000,950000,60): print(" ", r)
print("LAB1 chord at 10500:", chord_less_call([9000,9500,10000,10500,11000,11500],[1500,1100,800,700,450,350],3), " chord value:", F(800+450,2))
print("LAB3 chord 6000 value:", F(500 + 2*151, 3), " call 330; diff:", chord_less_call([4000,4500,5000,6000,6500,7000],[1210,820,500,330,151,90],3))
print("LAB3 parity 4500 gap:", gap(820,155,5000,4500,950000), "discounted strike 4500*0.95 =", F(4500)*F(950000,10**6))
print("ExemplarB parity 6500 discounted", F(6500)*F(950000,10**6), "gap", gap(151,1100,5000,6500,950000))
print("ExemplarB parity 7000 discounted", F(7000)*F(950000,10**6), "gap", gap(90,1200,5000,7000,950000))
print("188/3 to 2dp", round(188/3, 2), "rnd(188/3)", rnd(F(188,3)))
# new grader test: chain [1,2,7] calls [2,3,5] puts [3,5,12], df=1, spot=0
ks, cs, ps = [1,2,7],[2,3,5],[3,5,12]
print("NEW TEST parity gaps", [gap(cs[k], ps[k], 0, ks[k], 10**6) for k in range(3)], "chord less call at 2:", chord_less_call(ks,cs,1), "gross", rnd(-chord_less_call(ks,cs,1)))
# exemplar convexity at 6000 check and parity gap sign
print("Lab3 parity 6500 gross", rnd(abs(gap(151,1100,5000,6500,950000))), "7000", rnd(abs(gap(90,1200,5000,7000,950000))))
# note: chain parity gap at 4500 check: gap -60 -> gross 60 == cost 60 -> net 0
print("4500 net", rnd(abs(gap(820,155,5000,4500,950000))) - 60)
