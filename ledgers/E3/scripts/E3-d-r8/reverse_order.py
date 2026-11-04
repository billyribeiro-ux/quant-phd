import sys, math, json
sys.argv = ["x"]
exec(open("/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/ledgers/E3/scripts/E3-d-r8/rederive.py").read().split("# (1)")[0])
inst = make_instance(49)
resp = json.loads(inst["responses_json"])
parsed = [parse(r) for r in resp]
g, l, k = 0.706253, 20.686351, 2.279683
import reference
est = reference.estimate(resp)
g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
theta = [math.log(g / (1 - g)), math.log(l), math.log(k)]
def f_order(t, order):
    ps = order(parsed)
    return ll(ps, 1 / (1 + math.exp(-t[0])), math.exp(t[1]), math.exp(t[2]))
def info(h, order):
    def at(*moves):
        y = list(theta)
        for idx, amt in moves:
            y[idx] += amt
        return f_order(y, order)
    f0 = at()
    M = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        M[i][i] = -(at((i, h)) - 2 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4 * h * h)
            M[i][j] = M[j][i] = v
    return M
def inv3(M):
    A = [list(r) + [1.0 if i == j else 0.0 for j in range(3)] for i, r in enumerate(M)]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(A[r][c])); A[c], A[p] = A[p], A[c]
        d = A[c][c]; A[c] = [x / d for x in A[c]]
        for r in range(3):
            if r != c:
                fac = A[r][c]; A[r] = [x - fac * y for x, y in zip(A[r], A[c])]
    return [row[3:] for row in A]
fwd = lambda p: p
rev = lambda p: list(reversed(p))
for h in (1e-5, 1e-6):
    for name, o in (("forward", fwd), ("reverse", rev)):
        C = inv3(info(h, o))
        print(h, name, "se_lambda", round(l * math.sqrt(C[1][1]), 4), "se_gamma", round(g * (1 - g) * math.sqrt(C[0][0]), 6))
