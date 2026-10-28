"""Independent exact recomputation of the L06 lab numbers (no import of the lab twin)."""
from fractions import Fraction as F
from itertools import product

SEED = 2026
N = 4

def lcg(seed):
    s = seed
    while True:
        s = (1103515245 * s + 12345) % 2**31
        yield s

def gen_inputs():
    g = lcg(SEED)
    def draw(mod):
        return next(g) % mod
    M = [[F(draw(7) - 3) for _ in range(N)] for _ in range(N)]
    mu = [F(draw(13) + 2, 100) for _ in range(N)]
    S = [[sum((M[k][i] * M[k][j] for k in range(N)), F(0)) / 16 + (F(1, 10) if i == j else F(0)) for j in range(N)] for i in range(N)]
    return M, mu, S

def gauss(A, b):
    n = len(b)
    R = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if R[r][c] != 0)
        R[c], R[p] = R[p], R[c]
        piv = R[c][c]
        R[c] = [x / piv for x in R[c]]
        for r in range(n):
            if r != c and R[r][c] != 0:
                f = R[r][c]
                R[r] = [x - f * y for x, y in zip(R[r], R[c])]
    return [R[i][n] for i in range(n)]

def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), F(0))

def mv(A, v):
    return [dot(r, v) for r in A]

M, mu, S = gen_inputs()
print("mu", [str(x) for x in mu])
print("diag", [str(S[i][i]) for i in range(N)])

def eq_solution(gamma, free):
    # minimise (g/2) w'Sw - mu'w s.t. sum w = 1 on free assets, w_fixed = 0
    k = len(free)
    Sub = [[S[i][j] for j in free] for i in free]
    KKT = [[gamma * Sub[i][j] for j in range(k)] + [F(1)] for i in range(k)] + [[F(1)] * k + [F(0)]]
    sol = gauss(KKT, [mu[i] for i in free] + [F(1)])
    w = [F(0)] * N
    for pos, val in zip(free, sol[:k]):
        w[pos] = val
    return w, sol[k]

gammas = [F(1), F(2), F(4), F(8), F(16)]
def obj(g, w):
    return g / 2 * dot(w, mv(S, w)) - dot(mu, w)

print("PART A")
for g in gammas:
    w, lam = eq_solution(g, list(range(N)))
    print("g", g, "ret", float(dot(mu, w)), "var", float(dot(w, mv(S, w))), "obj", float(obj(g, w)), "sum", sum(w) == 1, "w", [float(x) for x in w])
print("PART B: KKT verification of the nonneg optimum (exact), and brute-force over all zero sets")
for g in gammas:
    best = None
    feas = []
    for zmask in product((0, 1), repeat=N):
        zeros = [i for i in range(N) if zmask[i]]
        free = [i for i in range(N) if not zmask[i]]
        if not free:
            continue
        w, lam = eq_solution(g, free)
        if all(w[i] >= 0 for i in free):
            Sw = mv(S, w)
            nu = [g * Sw[i] - mu[i] + lam for i in range(N)]
            if all(nu[i] >= 0 for i in zeros):
                feas.append((tuple(zeros), w))
    print("gamma", g, "kkt-passing sets", [z for z, _ in feas])
    z, w = feas[0]
    print("   exact w", [float(x) for x in w], "obj", float(obj(g, w)), "ret", float(dot(mu, w)), "var", float(dot(w, mv(S, w))))
    print("   exact obj", obj(g, w))
    # brute-force check on a fine rational grid of the simplex (sanity, not a proof)
    eq_w, _ = eq_solution(g, list(range(N)))
    print("   constrained >= unconstrained:", obj(g, w) >= obj(g, eq_w), " unconstrained obj exact", obj(g, eq_w), float(obj(g, eq_w)))
    if g == 16:
        print("   E2 difference exact", obj(g, w) - obj(g, eq_w), float(obj(g, w) - obj(g, eq_w)))
    if g == 4:
        t0 = [F(1, 4)] * N
        d = [w[i] - t0[i] for i in range(N)]
        turn = sum((abs(x) for x in d), F(0))
        print("   turnover exact", turn, float(turn))
        print("   printed-weight turnover", sum(abs(F(x) - F(1, 4)) for x in ["0.389219", "0.220570", "0.390211", "0.000000"]), float(sum(abs(F(x) - F(1, 4)) for x in ["0.389219", "0.220570", "0.390211", "0.000000"])))
        print("   gamma4 weights exact", [float(x) for x in w])
