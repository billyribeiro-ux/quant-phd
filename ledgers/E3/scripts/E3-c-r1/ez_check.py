import math
from fractions import Fraction as F
# closed-form CRRA CE for two-outcome gamble at P(red)=1/2, gamma=2 (exact)
exact = 1/(0.5/110000 + 0.5/95000)
GAMMA=2.0
def ez_value(c0, date1, psi, beta):
    rho = 1.0 - 1.0/psi
    expectation = sum(p * c1 ** (1.0 - GAMMA) for c1, p in date1)
    inner = (1.0 - beta) * c0**rho + beta * expectation ** (rho / (1.0 - GAMMA))
    return float(inner ** (1.0 / rho))
def ez_ce(c0, date1, psi, beta):
    target = ez_value(c0, date1, psi, beta)
    lo, hi = float(-95000 - 1000), float(110000 + 1000)
    for _ in range(200):
        mid = (lo+hi)/2
        if ez_value(c0, [(mid,1.0)], psi, beta) < target: lo = mid
        else: hi = mid
    return (lo+hi)/2
for psi in (0.5,1.5,3.0):
    for beta in (0.9,0.95):
        ce = ez_ce(100000.0, [(110000.0,0.5),(95000.0,0.5)], psi, beta)
        print(psi, beta, repr(ce), "minus exact", ce-exact)
# fine grid check of omega(p) > p on (0, crossing)
def omf(p): return p**0.5/(p**0.5+(1-p)**0.5)**2
bad=[i for i in range(1,2781) if not omf(i/1e4) > i/1e4]
print("fine grid p in (0,0.2781) with omega<=p:", bad[:5], len(bad))
bad2=[i for i in range(2782,10000) if not omf(i/1e4) < i/1e4]
print("fine grid p in (0.2782,1) with omega>=p count:", len(bad2))
print("omega(0.01)", omf(0.01), "omega(0.05)", omf(0.05))
