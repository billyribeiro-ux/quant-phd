"""Independent recomputation of the numbers that project.html prints or states (python -I)."""
import math
from fractions import Fraction as F

# Lab 3 stream (as written in project.html lab 3)
s = ["10003.2", "10001.7", "10007.5", "10000.4", "10004.9", "10002.1", "10009.6", "10001.0", "10006.3", "10003.8", "10005.5"]
x = [F(v) for v in s]
n = len(x)
mean = sum(x) / n
var = sum((a - mean) ** 2 for a in x) / (n - 1)
print("sum", float(sum(x)), "mean", f"{float(mean):.6f}", "sample var", f"{float(var):.6f}")
print("last4 min/max", min(s[-4:]), max(s[-4:]))
tgt = max(1, math.ceil(F(1, 2) * n - F(1, 10) * n))
print("median target", tgt, "5th smallest", sorted(x)[tgt - 1])
print("qn-eps n for q=1/2, n=11, eps=0.1 exact:", F(1, 2) * n - F(1, 10) * n, "float:", 0.5 * 11 - 0.1 * 11)
# rank-target witness in the project text
print("witness float target q=0.1 n=20 eps=0.05:", math.ceil(0.1 * 20 - 0.05 * 20), "exact:", math.ceil(F(0.1) * 20 - F(0.05) * 20))
print("witness 0.2500004 exact qn-eps n:", float(F(0.2500004) * 20 - F(0.05) * 20), "target", math.ceil(F(0.2500004) * 20 - F(0.05) * 20))
print("six-place q 0.25 target", math.ceil(F(0.25) * 20 - F(0.05) * 20))
# Lab 1 op count bound check and lab 2 statement: mean 1000003.75, variance 8.5
st = [1000002, 1000005, 1000001, 1000004, 1000009, 1000003, 1000006, 1000000]
m = F(sum(st), 8)
print("lab2 mean", float(m), "sample var", float(sum((F(v) - m) ** 2 for v in st) / 7))
# Exemplar B proof identity check: S_{n+1} = S_n + delta (x_{n+1} - mean_{n+1}) on random rationals
import random
rng = random.Random(3)
ok = True
for _ in range(2000):
    k = rng.randint(1, 12)
    xs = [F(rng.randint(-50, 50), rng.randint(1, 9)) for _ in range(k + 1)]
    old = xs[:k]
    mo = sum(old) / k
    So = sum((a - mo) ** 2 for a in old)
    d = xs[k] - mo
    mn = (sum(old) + xs[k]) / (k + 1)
    Sn = sum((a - mn) ** 2 for a in xs)
    ok = ok and (Sn == So + d * (xs[k] - mn))
print("exemplar B S-update identity holds on 2000 rational cases:", ok)
# L10 lab-3 style numbers are in lab twins; ops bound 4n for Lab 1 check
