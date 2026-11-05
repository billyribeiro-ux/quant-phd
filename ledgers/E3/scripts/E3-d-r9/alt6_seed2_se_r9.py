# Round 9: alternative 6 (FD step 1e-4) at seed 2. For the reference and alt6 estimates, the observed information by central
# differences at steps 1e-4, 1e-5, 1e-6 in the transformed coordinates, and the page's standard errors from it.
import sys, json, math
from pathlib import Path
sys.path.insert(0, "ledgers/E3/scripts")
sys.path.insert(0, "/tmp/E3d_r9_ws")  # holds alt6_elicit.py (alt6 source) and instance.py
import importlib.util
G = Path("course/modules/E/E3/grader")
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
ref = load("ref", G / "reference.py")
alt = load("alt6", "/tmp/E3d_r9_ws/alt6_elicit.py")
from instance import make_instance
inst = make_instance(2)
resp = json.loads(inst["responses_json"])
parsed = [ref._parse(x) for x in resp]
def obj(t): return ref._objective(t, parsed)
def coords(e):
    g, l, k = e["gamma_hat"], e["lambda_hat"], e["kappa_hat"]
    return [math.log(g / (1 - g)), math.log(l), math.log(k)], (g, l, k)
def hess_neg(t, h):
    H = [[0.0] * 3 for _ in range(3)]
    def sh(*moves):
        x = list(t)
        for i, d in moves: x[i] += d
        return x
    for i in range(3):
        H[i][i] = -(obj(sh((i, h))) - 2 * obj(t) + obj(sh((i, -h)))) / (h * h)
        for j in range(i + 1, 3):
            v = -(obj(sh((i, h), (j, h))) - obj(sh((i, h), (j, -h))) - obj(sh((i, -h), (j, h))) + obj(sh((i, -h), (j, -h)))) / (4 * h * h)
            H[i][j] = H[j][i] = v
    return H
def inv3(A):
    a = A; n = 3
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        pv = M[c][c]; M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [row[n:] for row in M]
for name, mod in (("reference", ref), ("alt6", alt)):
    e = mod.estimate(resp)
    t, (g, l, k) = coords(e)
    print(name, "estimate gamma=%.6f lambda=%.6f kappa=%.6f" % (g, l, k), "reported se_gamma=%.6f" % e["se_gamma"], "se_lambda=%.6f" % e["se_lambda"], "se_kappa=%.6f" % e["se_kappa"])
    for h in (1e-4, 1e-5, 1e-6):
        Ci = inv3(hess_neg(t, h))
        se_g = g * (1 - g) * math.sqrt(Ci[0][0]); se_l = l * math.sqrt(Ci[1][1]); se_k = k * math.sqrt(Ci[2][2])
        print("  step %g: se_gamma=%.6f se_lambda=%.6f se_kappa=%.6f" % (h, se_g, se_l, se_k))
