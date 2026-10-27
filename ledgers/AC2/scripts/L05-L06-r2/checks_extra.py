"""Extra verifier checks for AC2 L05-L06 round 2: identity for Prop 3.3 on the lab draw, Prop 3.1 on random designs,
finite-N quintile gap (cause of -2.7937 vs -2.7996), and a Jaccard scan of card fronts.
Run: <checkout>/.venv/bin/python -I ledgers/AC2/scripts/L05-L06-r2/checks_extra.py
"""
import json
import math
import re
import sys

import numpy as np

sys.path.insert(0, "/tmp/verify-ac2-l56/ledgers/AC2/scripts/L05-L06-r2")
from recompute_l06 import gen, ne_solve  # noqa: E402  (verifier's own re-implementation)

# (1) exact identity: b_all - b* = P (d + SD v) and b_nm - b* = P_nm (SD v_nm)
X, y, m, d = gen(606, 0.05)
rng = np.random.default_rng(606)
n = 2000
lag = np.exp(rng.normal(np.log(1000.0), 0.6, n))
drev = lag * rng.normal(0.10, 0.20, n)
drec = drev * rng.uniform(0.10, 0.30, n) + lag * rng.normal(0.0, 0.02, n)
ppe = lag * rng.uniform(0.20, 0.60, n)
mm = np.zeros(n, bool)
mm[rng.permutation(n)[:200]] = True
v = rng.standard_normal(n)
bstar = np.array([0.05, 0.10, -0.08])
ball = ne_solve(X, y)
bnm = ne_solve(X[~m], y[~m])
P = np.linalg.inv(X.T @ X) @ X.T
Pn = np.linalg.inv(X[~m].T @ X[~m]) @ X[~m].T
print("identity all:", np.max(np.abs(ball - bstar - P @ (0.05 * m + 0.01 * v))))
print("identity nm :", np.max(np.abs(bnm - bstar - Pn @ (0.01 * v[~m]))))
print("cond(X'X)", np.linalg.cond(X.T @ X))
print("realised P d", np.round(P @ (0.05 * m), 4), " E[d|X] proj", np.round(P @ np.full(n, 0.005), 4))
print("noise part of all-firm a1", round(float((P @ (0.01 * v))[0]), 4), "nm noise a1", round(float((Pn @ (0.01 * v[~m]))[0]), 4))

# (2) Prop 3.1 on random designs: sum zero for every y iff ones in colspace
rs = np.random.default_rng(1)
Xa = rs.normal(size=(6, 2))
Xa_ones = np.column_stack([np.ones(6), Xa])  # 1 in colspace
ok = []
for _ in range(20):
    yy = rs.normal(size=6)
    b = np.linalg.lstsq(Xa_ones, yy, rcond=None)[0]
    ok.append(abs(np.sum(yy - Xa_ones @ b)) < 1e-9)
print("ones in colspace: sums zero for all 20 y:", all(ok))
ok2 = []
for _ in range(20):
    yy = rs.normal(size=6)
    b = np.linalg.lstsq(Xa, yy, rcond=None)[0]
    ok2.append(abs(np.sum(yy - Xa @ b)) < 1e-9)
print("ones not in colspace: sums zero for some y? ", any(ok2), "count zero", sum(ok2))

# (3) finite-N quintile gap: N=500 vs N=5000, 400 months each, beta 0
def gap(nf, months, seed):
    r = np.random.default_rng(seed)
    z = r.standard_normal((months, nf))
    o = np.argsort(z, axis=1)
    q = nf // 5
    return float((np.take_along_axis(z, o[:, :q], 1).mean(1) - np.take_along_axis(z, o[:, -q:], 1).mean(1)).mean())
print("gap N=500 (400 months)", round(gap(500, 400, 7), 4), " N=5000 (400 months)", round(gap(5000, 400, 8), 4), " analytic", round(-2.799619, 4))

# (4) Jaccard scan of card fronts (all 130 cards)
cards = json.load(open("/tmp/verify-ac2-l56/course/modules/AC/AC2/cards.json"))
def words(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = words(cards[i]["front"]), words(cards[j]["front"])
        if a and b:
            jac = len(a & b) / len(a | b)
            if jac >= 0.5:
                pairs.append((round(jac, 2), cards[i]["id"], cards[j]["id"]))
print("front Jaccard>=0.5 pairs:", sorted(pairs, reverse=True))
