"""Independent recomputation of the project-page numbers (CS2-d round 1 scratch)."""
import random
from fractions import Fraction

# Lab 1 series, recomputed from the seed
rng = random.Random(12)
series = [rng.randint(0, 99) for _ in range(12)]
print("lab1 series", series)

# Lab 3 values, exact
s3 = ["10003.2","10001.7","10007.5","10000.4","10004.9","10002.1","10009.6","10001.0","10006.3","10003.8","10005.5"]
ex = [Fraction(s) for s in s3]
tot = sum(ex); n = len(ex)
mean = tot / n
var = sum((x-mean)**2 for x in ex)/(n-1)
print("lab3 sum", float(tot), "exact mean unrounded", float(mean), "exact var unrounded", float(var))
# float welford
c=0; m=0.0; m2=0.0
for s in s3:
    x=float(s); c+=1; d=x-m; m+=d/c; m2+=d*(x-m)
print("welford mean", repr(m), "welford var", repr(m2/(c-1)))
print("abs diff welford mean vs exact", abs(m-float(mean)), "within 1e-9:", abs(m-float(mean))<=1e-9)
print("welford var - exact var (unrounded)", float(Fraction(m2/(c-1)) - var))
print("exact var rounded 6dp", f"{float(var):.6f}", "welford var 6dp", f"{m2/(c-1):.6f}")
q=Fraction(1,2); eps=Fraction("0.1")
print("qn - eps n =", q*n - eps*n, "ceil", -(-(q*n-eps*n)//1))

# Lab 2 alternative correct pairs of expressions
stream=[1000002,1000005,1000001,1000004,1000009,1000003,1000006,1000000]
def run(meanf, m2f):
    c=0; m=0.0; m2=0.0
    for x in stream:
        x=float(x); c+=1; d=x-m
        mn=meanf(m,d,c,x); m2=m2f(m2,d,mn,x,c); m=mn
    return f"count {c}\nmean {m:.6f}\nsample variance {m2/(c-1):.6f}"
A = run(lambda m,d,c,x: m + d/c, lambda m2,d,mn,x,c: m2 + d*(x-mn))
B = run(lambda m,d,c,x: (m*(c-1)+x)/c, lambda m2,d,mn,x,c: m2 + (c-1)*d*d/c)
C = run(lambda m,d,c,x: m + d/c, lambda m2,d,mn,x,c: m2 + (c-1)*d*d/c)
print("pair A identical:", A==B==C, "\n", A)
