"""Re-derive the claims of the changed FC1 cards (c016, c103, c153) with exact arithmetic."""
from fractions import Fraction as F
from itertools import product

# c016: for 0 < rho < 1 and finite n, S_n/d = (1-(1-rho)^(n+1))/rho is strictly below 1/rho; equal at rho = 1.
bad016 = []
rhos = [F(k, 97) for k in range(1, 97)] + [F(1, 10), F(1, 4), F(1, 2), F(9, 10), F(1)]
for rho in rhos:
    for n in range(0, 60):
        mult = sum((1 - rho) ** t for t in range(n + 1))  # recursion sum, D_t = (1-rho)^t d with d = 1
        closed = (1 - (1 - rho) ** (n + 1)) / rho
        assert mult == closed, (rho, n)
        if rho < 1 and not (mult < 1 / rho):
            bad016.append((rho, n))
        if rho == 1 and mult != 1 / rho:
            bad016.append(('rho1', n))
print("c016 grid rho count", len(rhos), "n 0..59; violations:", bad016)
print("c016 stage 10 at rho 1/10 exact:", float(sum((F(9, 10)) ** t for t in range(11))), "limit 1/rho:", 10)

# c103 (Prop 2.2): sum X_t + sum l_t = S_n with X_t = rho D_t, l_t = D_t - X_t, D_{t+1} = l_t (A2), D_0 = d
bad103 = []
for d, rho in product([F(1000), F(7, 3), F(1, 9)], [F(1, 10), F(1, 4), F(1), F(3, 7)]):
    D = d
    sumX = F(0); suml = F(0); S = F(0)
    for t in range(0, 25):
        X = rho * D
        l = D - X
        sumX += X; suml += l; S += D
        if sumX + suml != S:
            bad103.append((d, rho, t))
        D = l  # A2: the whole loan is redeposited at stage t+1
print("c103 identity violations over grid:", bad103)

# c153 (Prop 3.5): limit d/(1 - phi(1-rho)) equals d/rho exactly iff phi = 1 or rho = 1; for 0 < rho <= 1, 0 <= phi <= 1
viol153 = []
grid = [F(k, 20) for k in range(0, 21)]
for phi, rho in product(grid, [F(k, 20) for k in range(1, 21)]):
    kappa = phi * (1 - rho)
    lim = F(1) / (1 - kappa)
    target = F(1) / rho
    if lim > target:
        viol153.append(('above', phi, rho))
    eq = (lim == target)
    if eq != ((1 - phi) * (1 - rho) == 0):
        viol153.append(('iff', phi, rho))
print("c153 grid size", len(grid) * 20, "violations:", viol153)
