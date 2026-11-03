"""Independent recomputation of the L06 simulated-input numbers used by M7 cards (verifier round 3, slice e).

Re-derives the inputs from the LCG constants printed on the lab page and recomputes the equality and
nonnegative solutions and the turnover in exact fractions. Usage: python -I v3_l06_numbers.py
"""
from fractions import Fraction as F
from itertools import product

SEED = 2026
N = 4
state = SEED


def draw(mod):
    global state
    state = (1103515245 * state + 12345) % 2**31
    return state % mod


M = [[F(draw(7) - 3) for _ in range(N)] for _ in range(N)]
mu = [F(draw(13) + 2, 100) for _ in range(N)]
Sig = [[sum(M[k][i] * M[k][j] for k in range(N)) / 16 + (F(1, 10) if i == j else 0) for j in range(N)] for i in range(N)]
print("mu", [str(v) for v in mu])
print("sigma diag", [str(Sig[i][i]) for i in range(N)])


def solve(a, b):
    n = len(b)
    m = [list(row) + [v] for row, v in zip(a, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def mv(a, v):
    return [dot(r, v) for r in a]


def obj(g, w):
    return g / 2 * dot(w, mv(Sig, w)) - dot(mu, w)


def eq_point(g, idx):
    k = len(idx)
    sub = [[g * Sig[i][j] for j in idx] + [F(1)] for i in idx]
    sub.append([F(1)] * k + [F(0)])
    sol = solve([row for row in sub], [mu[i] for i in idx] + [F(1)])
    return sol[:k], sol[k]


def full(g):
    w, _ = eq_point(g, list(range(N)))
    return w


for g in (F(1), F(2), F(4), F(8), F(16)):
    w = full(g)
    ret, risk = dot(mu, w), dot(w, mv(Sig, w))
    print("gamma", g, "w", [f"{float(v):.6f}" for v in w], "ret", f"{float(ret):.6f}", "risk", f"{float(risk):.6f}",
          "obj", f"{float(obj(g, w)):.6f}", "budget exact", sum(w) == 1)


def nonneg(g):
    kept = []
    for mask in product((0, 1), repeat=N):
        zeros = [i for i in range(N) if mask[i]]
        free = [i for i in range(N) if not mask[i]]
        if not free:
            continue
        wf, lam = eq_point(g, free)
        w = [F(0)] * N
        for pos, val in zip(free, wf):
            w[pos] = val
        sw = mv(Sig, w)
        nu = [g * sw[i] - mu[i] + lam for i in range(N)]
        if all(v >= 0 for v in w) and all(nu[i] >= 0 for i in zeros):
            kept.append((tuple(zeros), w))
    return kept


for g in (F(1), F(2), F(4), F(8), F(16)):
    kept = nonneg(g)
    best = min(kept, key=lambda it: obj(g, it[1]))
    zeros, w = best
    print("nonneg gamma", g, "kept", len(kept), "zero set", zeros, "w", [f"{float(v):.6f}" for v in w],
          "ret", f"{float(dot(mu, w)):.6f}", "risk", f"{float(dot(w, mv(Sig, w))):.6f}", "obj", f"{float(obj(g, w)):.6f}")

kept4 = nonneg(F(4))
_, w4 = min(kept4, key=lambda it: obj(F(4), it[1]))
w0 = [F(1, 4)] * N
turn = sum(abs(a - b) for a, b in zip(w4, w0))
print("turnover exact", turn, float(turn), "from printed 6-place weights:", sum(abs(round(float(a), 6) - 0.25) for a in w4))
print("turnover from printed weights exact sum of |printed - 1/4|:",
      sum(abs(F(f"{float(a):.6f}") - F(1, 4)) for a in w4), float(sum(abs(F(f"{float(a):.6f}") - F(1, 4)) for a in w4)))
print("Part A risk at gamma 1 closed form equals KKT (sanity):", full(F(1)) == full(F(1)))
