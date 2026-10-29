"""Independent recomputation for round 5 (slice M7-b): exact Fractions, own solver.
Sigma comes from the lab's generator only to read the off-diagonal entries (printed values are diagonal only);
every other number is recomputed here."""
import importlib.util, sys
from fractions import Fraction as F
spec = importlib.util.spec_from_file_location("lab6", sys.argv[1])
lab6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(lab6)
_, mu, sigma = lab6.simulate_inputs()
print("mu", [str(x) for x in mu])
print("diag", [str(sigma[i][i]) for i in range(4)])

def solve(a, b):
    n = len(b); m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0); m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]; m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]

def eq_point(idx, gamma):
    # minimise gamma/2 w'Sw - mu'w s.t. sum w = 1 over the assets in idx (others fixed at 0)
    S = [[sigma[i][j] for j in idx] for i in idx]; k = len(idx)
    # KKT: gamma S w - mu - nu 1 = 0, 1'w = 1
    M = [[gamma * S[i][j] for j in range(k)] + [F(-1)] for i in range(k)] + [[F(1)] * k + [F(0)]]
    rhs = [mu[i] for i in idx] + [F(1)]
    sol = solve(M, rhs)
    w = [F(0)] * 4
    for t, i in enumerate(idx): w[i] = sol[t]
    return w

def risk(w): return sum(w[i] * sigma[i][j] * w[j] for i in range(4) for j in range(4))
def obj(w, g): return g / 2 * risk(w) - sum(mu[i] * w[i] for i in range(4))

g = F(16)
w_eq = eq_point([0, 1, 2, 3], g)
w_nn = eq_point([0, 1, 2], g)  # A4 fixed at zero (the zero set printed as {A4})
print("eq16 objective exact", float(obj(w_eq, g)), "nn16 objective exact", float(obj(w_nn, g)))
print("difference exact", float(obj(w_nn, g) - obj(w_eq, g)))
print("printed-value difference", round(1.392257 - 0.820002, 6))
print("eq16 weights", [round(float(x), 6) for x in w_eq])
print("nn16 weights", [round(float(x), 6) for x in w_nn], "risk nn16", round(float(risk(w_nn)), 6), "risk eq16", round(float(risk(w_eq)), 6))
print("budget eq", sum(w_eq), "budget nn", sum(w_nn))
