"""Independent recount of L01 and L02 lab numbers with numpy (not the page's Fraction code)."""
import numpy as np

MUL, INC, MOD = 1103515245, 12345, 2**31


class G:
    def __init__(self, seed):
        self.s = seed % MOD

    def step(self):
        self.s = (MUL * self.s + INC) % MOD
        return self.s >> 16


def l01():
    g = G(20261028)

    def ent(b):  # integer from -b..b
        return (g.step() % (2 * b + 1)) - b

    def vec(n):
        return np.array([ent(3) for _ in range(n)], dtype=float)

    def count(n, k, draws):
        hits = 0
        for _ in range(draws):
            M = np.column_stack([vec(n) for _ in range(k)])
            hits += np.linalg.matrix_rank(M) == k
        return hits

    a = count(3, 3, 200)
    b = count(3, 4, 200)
    c = count(4, 4, 200)
    d = count(4, 5, 200)
    dep = tri = r3 = 0
    for _ in range(100):
        v1, v2, v3 = vec(4), vec(4), vec(4)
        v4 = 2 * v1 - v2 + v3
        four = np.column_stack([v1, v2, v3, v4])
        dep += np.linalg.matrix_rank(four) < 4
        t = np.column_stack([v1, v2, v3])
        tri += np.linalg.matrix_rank(t) == 3
        r3 += np.linalg.matrix_rank(four) == 3
    print("L01 numpy recount:", a, b, c, d, "| planted dep", dep, "indep triples", tri, "rank3", r3)


def l02():
    g = G(7)

    def dm(bound, size=3):
        return np.array([[ (g.step() % (2 * bound + 1)) - bound for _ in range(size)] for _ in range(size)], dtype=float)

    rejected = 0
    ok_formula = ok_comp = ok_float = 0
    first = None
    for p in range(50):
        A = dm(4)
        C = dm(4)
        while True:
            S = dm(3)
            if abs(np.linalg.det(S)) > 0.5:  # integer matrix: det is an integer, zero iff singular
                break
            rejected += 1
        Si = np.linalg.inv(S)
        F = Si @ A @ S
        coords = np.column_stack([np.linalg.solve(S, A @ S[:, j]) for j in range(3)])
        ok_formula += np.allclose(coords, F, atol=1e-9)
        ok_comp += np.allclose(Si @ C @ A @ S, (Si @ C @ S) @ (Si @ A @ S), atol=1e-9)
        ok_float += np.all(np.abs(F - F) <= 1e-12)
        if p == 0:
            first = F
    print("L02 numpy recount: rejected", rejected, "formula", ok_formula, "composition", ok_comp, "first", np.round(first, 6).tolist())


l01()
l02()
