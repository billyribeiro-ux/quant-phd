# Round-6 independent re-derivation of every L03 number that the delta touched, plus its neighbours.
from fractions import Fraction as F
import math

def half_up(x):
    return math.floor(x + F(1, 2))

# --- Lab 3 Part A (independent re-simulation is in the twin; here: recompute margins from printed path)
path = [5000, 5039, 5070, 5104, 5069, 5103, 5090, 5054, 5077, 5106, 5084]
margins = [path[i] - path[i-1] for i in range(1, len(path))]
print("A margins", margins)
print("A balance after day 10", sum(margins), "settlement-minus-initial", path[-1]-path[0])
print("A loss days", sum(1 for m in margins if m < 0))
print("A largest loss", min(margins), "on day", margins.index(min(margins)) + 1, "prices day6,day7", path[6], path[7])
print("A balances equal price minus initial on every day:", all(sum(margins[:i+1]) == path[i+1]-path[0] for i in range(10)))

# --- Lab 3 Part B
Z = [F(3,100), F(7,200), F(4,100), F(9,200), F(5,100)]
DF = [F(1)] + [F(1) / (1+z)**i for i, z in enumerate(Z, start=1)]
ann = sum(DF[1:], F(0))
par = (1 - DF[-1]) / ann
N = 100_000_000
print("B DF1..5 six places", ["%.6f" % float(d) for d in DF[1:]])
print("B par exact float", float(par), "six places %.6f" % float(par), "four places %.4f" % (float(par)*100))
print("B par strictly between 4.5 and 5 percent:", F(9,200) < par < F(5,100))
print("B par differs from each zero rate:", all(par != z for z in Z))
print("B payment cents", half_up(par * N), "dollars", half_up(par*N)/100)
print("B value to payer struck +1pt, cents", half_up((1 - DF[-1] - (par + F(1,100))*ann) * N))
print("B -0.01*annuity*N cents", half_up(-F(1,100)*ann*N), "annuity", float(ann))
print("P2 check: value at K=par+h is -h*sum(DF) (h=0.01) cents", half_up(-F(1,100)*ann*N))

# --- flat curve (Example 3.4): par equals flat rate for several n and rates
for rho in [F(6,100), F(3,100), F(0), F(-1,100)]:
    for n in range(1, 8):
        dfs = [F(1)] + [(1+rho)**(-i) for i in range(1, n+1)]
        if rho == 0:
            # par undefined by the flat-curve formula only if annuity 0; here annuity = n > 0
            pass
        p = (1 - dfs[n]) / sum(dfs[1:], F(0))
        assert p == rho, (rho, n, p)
print("Example 3.4: par == flat rate exactly for rho in {6,3,0,-1} percent, n=1..7: True")

# --- M2: flat 6 percent, three years
df3 = F(1) / F(106,100)**3
print("M2 DF3 = %.6f (1/1.191016 = %.6f)" % (float(df3), 1/1.191016))
print("M2 par on flat 6 percent = 0.06 exactly:", ((1 - df3)/sum([F(100,106)**1, F(100,106)**2 if False else F(1)/F(106,100)**2, df3], F(0))) == F(6,100))

# --- M3: flat 6 percent, three periods, payer pays 5 percent, notional 100 dollars
dfs3 = [F(1)/F(106,100)**i for i in (1,2,3)]
s3 = sum(dfs3, F(0))
print("M3 sum DF exact", float(s3), "unrounded 2.6730119 check", "%.7f" % float(s3))
print("M3 displayed factors sum", round(0.943396+0.889996+0.839619, 6))
print("M3 value per unit notional", float((F(6,100)-F(5,100))*s3), "per 100 dollars", float(100*(F(6,100)-F(5,100))*s3))
print("M3 to the cent", "%.2f" % float(100*(F(6,100)-F(5,100))*s3))
print("Q8 value per unit notional seven places", "%.7f" % float((F(6,100)-F(5,100))*s3))

# --- R3: DF1 = 1/1.03, f2 = 5 percent
DF1 = F(1)/F(103,100)
DF2 = DF1/F(105,100)
R3 = (1 - DF2)/(DF1 + DF2)
print("R3 DF1 %.6f DF2 %.6f" % (float(DF1), float(DF2)), "par %.6f four places %.4f" % (float(R3), float(R3)*100))
print("R3 flat 3 percent DF2 = 1.03^-2 = %.6f" % float(F(1)/F(103,100)**2))
print("R3 par strictly between 3 and 5 percent:", F(3,100) < R3 < F(5,100))
# R2 weights
f1 = 1/float(DF1) - 1; f2 = float(DF1/DF2) - 1
w1 = float(DF1/(DF1+DF2)); w2 = float(DF2/(DF1+DF2))
print("R2 check: w1 f1 + w2 f2 = %.9f, par = %.9f" % (w1*f1 + w2*f2, float(R3)))

# --- P1, P3 quick
print("P3 B_n for n=2, eta=0.01, path Delta1=1: (1+eta)^(n-1) =", (1+0.01)**1, "!= 1 when eta != 0 (True)")

# --- Q1.. quiz numerics
print("Q2 balance after day 2 (100 -> 103 -> 99):", 99-100)
print("Q6 DF1 at 3 percent to six places: %.6f" % float(F(1)/F(103,100)))
print("Q7-10 par on flat 6 percent %.4f" % 0.06)

# --- L03 misconception 3 and E3 facts
print("E3 printed par 0.049026 -> four places %.4f percent" % (0.049026*100))
print("E3 printed payment 4902625 cents = %.2f dollars" % (4902625/100))
print("E3 par 4.9026 differs from 3,3.5,4,4.5,5:", all(abs(4.9026 - z) > 0 for z in [3,3.5,4,4.5,5]))
