"""Check the R1 weighted-update recursion (L09 Research problem) on random data, and the R3 zero-one formula."""
import random
from fractions import Fraction as F

def weighted(xs, ws):
    W = ws[0]; M = F(xs[0]); S = F(0)
    for n in range(2, len(xs) + 1):
        x = F(xs[n - 1]); w = F(ws[n - 1])
        W_new = W + w
        d = x - M
        M_new = M + (w / W_new) * d
        S = S + w * d * (x - M_new)
        W, M = W_new, M_new
    return W, M, S

bad = 0
for t in range(300):
    r = random.Random(t)
    n = r.randint(1, 12)
    xs = [r.randint(-20, 20) for _ in range(n)]
    ws = [r.randint(1, 9) for _ in range(n)]
    W, M, S = weighted(xs, ws)
    mean = sum(F(w) * x for x, w in zip(xs, ws)) / W
    ss = sum(F(w) * (x - mean) ** 2 for x, w in zip(xs, ws))
    if M != mean or S != ss:
        bad += 1
print("weighted recursion mismatches over 300 random cases:", bad)
# R1 example
print("R1 example M2, S2:", weighted([1, 2], [1, 3]))
# R3: zero-one, n=10, k=4
xs = [1]*4 + [0]*6
mean = F(sum(xs), 10); ss = sum((x - mean) ** 2 for x in xs)
print("R3 pop var", ss / 10, "S", ss)
