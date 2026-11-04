"""Independent recomputation of every number in SC1 slice-b prose (L04, L05, L06), by a route other than the labs."""
import math
from fractions import Fraction
from itertools import product

# ---- L06: exact enumeration, independent of the lab's code (walk-by-walk recursion on prefixes)
def walks(n):
    out = []
    for steps in product((1, -1), repeat=n):
        s, top = 0, 0
        for e in steps:
            s += e
            top = max(top, s)
        out.append((top, s))
    return out

tripA = eqA = 0
for n in range(1, 13):
    W = walks(n)
    for a in range(1, n + 1):
        for b in range(-n, a):
            lhs = sum(1 for top, s in W if top >= a and s == b)
            rhs = sum(1 for top, s in W if s == 2 * a - b)
            tripA += 1
            eqA += lhs == rhs
print("L06 partA triples", tripA, "equal", eqA)
print("L06 partA triples with a>N (not in lab, for scope check):", sum(1 for n in range(1,13) for a in range(n+1, n+13) for b in range(-n, a) ) )
W12 = walks(12)
print("L06 C: M12>=3:", sum(1 for t, s in W12 if t >= 3), " M12>=3 & S=2:", sum(1 for t, s in W12 if t >= 3 and s == 2), " S=4:", sum(1 for t, s in W12 if s == 4))
W10 = walks(10)
P_M = Fraction(sum(1 for t, s in W10 if t >= 2), 1024)
P_S = Fraction(sum(1 for t, s in W10 if s > 2), 1024)
P_E = Fraction(sum(1 for t, s in W10 if s == 2), 1024)
print("L06 D: P(M10>=2)=", P_M, float(P_M), " 2P(S10>2)=", 2 * P_S, " P(S10=2)=", P_E, " identity:", P_M - 2 * P_S == P_E)
print("L06 E2 check: 281/512 - 11/32 =", Fraction(281, 512) - Fraction(11, 32), " C(10,6)=", math.comb(10, 6))
print("L06 E: erfc(1/sqrt2)=", f"{math.erfc(1/math.sqrt(2)):.12f}", " half=", f"{math.erfc(1/math.sqrt(2))/2:.12f}")
print("L06 E1: ratio 5.55e-16/3.81e-29 =", f"{5.55e-16/3.81e-29:.4e}")
print("L06 misc: P(M1>=1)=", f"{math.erfc(1/math.sqrt(2)):.6f}", " P(B1>=1)=", f"{math.erfc(1/math.sqrt(2))/2:.6f}")

# ---- L04 numbers
print("L04 e^1", f"{math.e:.9f}", " e^0.25", f"{math.exp(0.25):.9f}", " e^4", f"{math.exp(4):.9f}", " e^8", f"{math.exp(8):.9f}")
print("L04 E[M_t^2] at theta=2,t=2 = e^8 =", f"{math.exp(8):.6f}")

# ---- L05 numbers
print("L05 p1(0,0)=(2pi)^-1/2 =", f"{(2*math.pi)**-0.5:.10f}")
print("L05 Phi(-1/sqrt2) =", f"{0.5*math.erfc((1/math.sqrt(2))/math.sqrt(2)):.10f}")
print("L05 Lemma2.2 identity at u=1,v=3,x=0,y=1:", all(abs((z-0)**2/1 + (1-z)**2/3 - ((4/3)*(z-0.25)**2 + 1/4)) < 1e-12 for z in [-2,-0.5,0,0.3,1.7]))
