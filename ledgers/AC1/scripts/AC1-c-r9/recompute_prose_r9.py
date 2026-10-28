"""Independent recomputation of the worked numbers in L07 and L08 prose, in integer cents with Fraction checks."""
from fractions import Fraction as F

def cents(x):  # dollars -> cents
    return round(x * 100)

# L07 Example 1.4 and M1-M3, E1 expense per year
C = 1000 * 1200
assert C == 1_200_000 and C // 4 == 300_000
C1 = 500 * 800
b = C1 // 3
sched = {2: b, 3: b, 4: C1 - 2 * b}
assert sched == {2: 133333, 3: 133333, 4: 133334} and sum(sched.values()) == C1 == 400000
assert 400000 // 4 == 100000 and 400000 - 3 * 100000 == 100000
assert 2000000 - 133333 == 1866667  # NI2 in cents: 20000.00 - 1333.33 = 18666.67
assert 2000000 - 133333 == 1866667
# L07 lab peak year 3 expense 57,822.92 from grants: G1 21360 (yr2-4, 3 yrs), G2 29785 (yr1-3), G3 79365 (yr1-4), G4 62800 (yr3-5)
G = [(2, 2136000, 3), (1, 2978500, 3), (1, 7936500, 4), (3, 6280000, 3)]
def e(g, t):
    gy, val, v = g
    i = t - gy
    if i < 0 or i >= v: return 0
    base = val // v
    return val - base * (v - 1) if i == v - 1 else base
print("L07 year expenses (cents):", [sum(e(g, t) for g in G) for t in range(1, 7)])
assert sum(e(g, 3) for g in G) == 5782292
# L07 Example 2.3: NI = 50000-3000=47000 etc (dollars)
assert 50000 - 3000 == 47000

# L08 Example 1.4 at r=21
C8, L = 100000, 5
pct = (40, 30, 20, 10, 0)
b8 = C8 / L
tau = [C8 * p / 100 for p in pct]
diff = [t - b8 for t in tau]
K = []
s = 0
for d in diff:
    s += d
    K.append(s)
assert K == [20000, 30000, 30000, 20000, 0]
assert [round(21 * k / 100) for k in K] == [4200, 6300, 6300, 4200, 0]
# Example 2.2, P=50000
P = 50000
prev = 0
for t in range(5):
    ct = F(21, 100) * (P - diff[t]); dtl = F(21, 100) * K[t]; de = dtl - prev; prev = dtl
    print("ex2.2 yr", t + 1, "CT", float(ct), "DE", float(de), "TE", float(ct + de))
# M2 cost 60000, L 3, pct 50,30,20
b2 = 20000; tau2 = [30000, 18000, 12000]; d2 = [t - b2 for t in tau2]
K2 = [10000, 8000, 0]; assert [sum(d2[:i+1]) for i in range(3)] == K2
dtl2 = [F(21, 100) * k for k in K2]; de2 = [dtl2[0], dtl2[1] - dtl2[0], dtl2[2] - dtl2[1]]
print("M2 DTL", [float(x) for x in dtl2], "DE", [float(x) for x in de2])
ct2 = [F(21, 100) * (50000 - d) for d in d2]
print("M3 CT", [float(x) for x in ct2], "TE", [float(ct2[i] + de2[i]) for i in range(3)])
# R2: rate 25 in year 3 on K2=30000
te3 = F(25, 100) * (50000 - 0) + (F(25, 100) * 30000 - F(21, 100) * 30000)
print("R2 TE3", float(te3), "gap", float(te3 - F(25, 100) * 50000))
# E1 L08 peak balance and 46,700 check
K_lab = 14010; print("L08 DTL 21% of 14010 =", 0.21 * K_lab, "; K/cost =", K_lab / 46700)
print("L08 E2 yr1:", 8169.84 + 1961.40, "vs 0.21*48244 =", round(0.21 * 48244, 2))
print("L08 M1 DTL2 at 25%:", 25 * 30000 / 100)
