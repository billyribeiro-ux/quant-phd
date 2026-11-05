"""Counterexample check for Assumption A1(b), second sentence (L01.html:75), round 11.

Z is N(0,1) and eps is an independent fair sign. W = eps * Z is also N(0,1). Each coordinate of the vector (Z, W)
is a one-term linear combination of an independent normal family, so the literal second sentence of A1(b) would
make (Z, W) multivariate normal. But Z + W = (1 + eps) Z is 0 with probability 1/2, while a non-degenerate normal
variable has no atom. The script estimates P(Z + W = 0) and Var(W).
"""

import random

rng = random.Random(7)
N = 200000
zero = 0
ws = []
for _ in range(N):
    z = rng.gauss(0.0, 1.0)
    eps = 1 if rng.random() < 0.5 else -1
    w = eps * z
    ws.append(w)
    if z + w == 0.0:
        zero += 1
m = sum(ws) / N
var_w = sum((w - m) ** 2 for w in ws) / N
print(f"Var(W) estimate {var_w:.3f} (W is N(0,1), so near 1)")
print(f"P(Z + W = 0) estimate {zero / N:.4f} (near 1/2; a normal variable with positive variance has P(=0) = 0)")
