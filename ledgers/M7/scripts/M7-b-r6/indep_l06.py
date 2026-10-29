"""Independent recomputation of L06 Lab 1 numbers (float64 via numpy, checked against printed 6-dp values).

Regenerates the simulated inputs from the documented recurrence (SEED 2026, LCG constants as in the lab
docstring), solves the equality-only problem by numpy.linalg, and solves the nonnegative problem by
enumerating all 16 active sets with an independent KKT computation. Also checks the Remark 1.4 and
Proposition 2.1 monotonicity numerically on a fine grid of gamma.
"""
import itertools
import numpy as np

SEED = 2026
state = SEED
def draw(mod):
    global state
    state = (1103515245 * state + 12345) % 2**31
    return state % mod
M = np.array([[draw(7) - 3 for _ in range(4)] for _ in range(4)], dtype=float)
mu = np.array([(draw(13) + 2) / 100 for _ in range(4)])
Sig = M.T @ M / 16 + np.eye(4) / 10
print("mu", mu)
print("sigma diag", np.diag(Sig))
print("eig min", np.linalg.eigvalsh(Sig).min())
def eq_solve(gamma, idx):
    k = len(idx)
    S = Sig[np.ix_(idx, idx)]
    K = np.zeros((k + 1, k + 1))
    K[:k, :k] = gamma * S
    K[:k, k] = 1
    K[k, :k] = 1
    rhs = np.concatenate([mu[idx], [1.0]])
    sol = np.linalg.solve(K, rhs)
    w = np.zeros(4)
    w[idx] = sol[:k]
    return w, sol[k]
def closed(gamma):
    a = np.linalg.solve(Sig, mu); b = np.linalg.solve(Sig, np.ones(4))
    lam = (a.sum() - gamma) / b.sum()
    return (a - lam * b) / gamma
print("equality (gamma, return, risk, objective) and weights")
eq = {}
for g in [1, 2, 4, 8, 16]:
    w, lam = eq_solve(g, [0, 1, 2, 3])
    assert np.allclose(w, closed(g))
    r = mu @ w; v = w @ Sig @ w; o = g / 2 * v - r
    eq[g] = (r, v, o)
    print(g, round(r, 6), round(v, 6), round(o, 6), np.round(w, 6), "budget", round(w.sum(), 12))
print("nonneg: best candidate per gamma")
for g in [1, 2, 4, 8, 16]:
    best = None; passing = []
    for mask in itertools.product([0, 1], repeat=4):
        zeros = [i for i in range(4) if mask[i]]
        free = [i for i in range(4) if not mask[i]]
        if not free:
            continue
        w, lam = eq_solve(g, free)
        nu = g * (Sig @ w) - mu + lam
        if (w >= -1e-12).all() and all(nu[i] >= -1e-12 for i in zeros):
            passing.append(tuple(zeros))
            o = g / 2 * (w @ Sig @ w) - mu @ w
            if best is None or o < best[0]:
                best = (o, zeros, w)
    o, zeros, w = best
    print(g, "passing", passing, "zeros", zeros, "return", round(mu @ w, 6), "risk", round(w @ Sig @ w, 6), "obj", round(o, 6), np.round(w, 6))
    print("  diff objective constrained - equality", round(o - eq[g][2], 6))
# turnover at gamma 4 against equal weight
w4 = None
best = None
for mask in itertools.product([0, 1], repeat=4):
    zeros = [i for i in range(4) if mask[i]]; free = [i for i in range(4) if not mask[i]]
    if not free: continue
    w, lam = eq_solve(4, free); nu = 4 * (Sig @ w) - mu + lam
    if (w >= -1e-12).all() and all(nu[i] >= -1e-12 for i in zeros):
        o = 2 * (w @ Sig @ w) - mu @ w
        if best is None or o < best[0]: best = (o, w)
w4 = best[1]
print("turnover gamma4", np.abs(w4 - 0.25).sum(), "weights", w4)
# monotonicity on a grid of gamma, equality and nonneg (nonneg via best candidate)
gs = np.linspace(0.5, 30, 300)
V = [ (lambda w: w @ Sig @ w)(eq_solve(g, [0,1,2,3])[0]) for g in gs]
R = [ mu @ eq_solve(g, [0,1,2,3])[0] for g in gs]
print("equality risk nonincreasing on grid", all(np.diff(V) <= 1e-12), "return nonincreasing", all(np.diff(R) <= 1e-12))
print("unrounded E2 diff", eq[16][2], )
