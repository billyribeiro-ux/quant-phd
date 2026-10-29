import math, random
from decimal import Decimal, getcontext
getcontext().prec = 50
# L02 independent recompute (different RNG draw order not needed: same seed, same draws)
rng = random.Random(2026)
A, K, L = [1.0], [100.0], [50.0]
for _ in range(40):
    A.append(A[-1] * math.exp(rng.uniform(0.005, 0.02)))
    K.append(K[-1] * math.exp(rng.uniform(0.02, 0.05)))
    L.append(L[-1] * math.exp(rng.uniform(0.0, 0.015)))
a = 0.3
Y = [A[t] * K[t] ** a * L[t] ** (1 - a) for t in range(41)]
g = lambda x: [math.log(x[t]) - math.log(x[t-1]) for t in range(1, 41)]
dY, dK, dL, dA = g(Y), g(K), g(L), g(A)
mean = lambda v: sum(v) / len(v)
res = lambda al: [y - al*k - (1-al)*l for y, k, l in zip(dY, dK, dL)]
print("gap", max(abs(r - x) for r, x in zip(res(a), dA)))
print("avgY", round(mean(dY), 6), "capT", round(a*mean(dK), 6), "labT", round((1-a)*mean(dL), 6), "res", round(mean(res(a)), 6))
print("shares", round(a*mean(dK)/mean(dY), 6), round((1-a)*mean(dL)/mean(dY), 6), round(mean(res(a))/mean(dY), 6))
r02, r04 = mean(res(0.2)), mean(res(0.4))
print("res0.2", round(r02, 6), "res0.4", round(r04, 6), "diff", round(r02 - r04, 6))
print("implied avg dK", a*0 + 0.010667/0.3, "avg dL", 0.005327/0.7, "0.2*(dK-dL)", 0.2*(0.010667/0.3 - 0.005327/0.7))
print("exact 0.2*(meanK-meanL) from run", 0.2*(mean(dK)-mean(dL)), "vs diff", r02 - r04)
print("avg dK run", mean(dK), "avg dL run", mean(dL))
print("E3 alpha .4 cap term", round(0.4*mean(dK), 6), "run-free", round(0.4*(0.010667/0.3), 6))
simple = [Y[t]/Y[t-1]-1 for t in range(1, 41)]
print("avg simple", round(mean(simple), 6))
print("1.1^0.3", round(1.1**0.3, 6), "0.3*0.1", 0.03, "0.3 ln1.1", round(0.3*math.log(1.1), 6))
print("0.3 ln2", round(0.3*math.log(2), 6))
# misconception 3 check: simple growth 1.1^0.3 - 1
print("simple out", round(1.1**0.3 - 1, 6))
# L03 independent recompute with floats (cross-check of Decimal results)
al, s, d, n = 0.3, 0.2, 0.05, 0.01
ks = (s/(n+d))**(1/(1-al))
print("k*", f"{ks:.10f}", "y*", f"{ks**al:.10f}", "dk/ds", f"{ks/((1-al)*s):.10f}", "dk/dd", f"{-ks/((1-al)*(n+d)):.10f}", "elas", f"{1/(1-al):.10f}")
k = 1.0; first = -1
for t in range(1, 1001):
    k = (s*k**al + (1-d)*k)/(1+n)
    if first < 0 and abs(k-ks) < 1e-12: first = t
print("first period gap<1e-12 (float)", first)
grid = [i/5 for i in range(1, 51)]
below = sum(1 for x in grid if x < ks)
mism = sum(1 for x in grid if ((s*x**al + (1-d)*x)/(1+n) > x) != (x < ks))
print("grid below", below, "above", 50-below, "mismatch", mism)
# E1 ratio, E2 numbers
print("E1 ratio", 0.0805861272/0.6623874908)
print("E2", 0.01*39.8879393156, 0.01*39.8879393156/5.5843115042, 1.4285714286*0.05)
print("E3", 0.001*-132.9597977186)
print("M2 L03 k2", (0.25*math.sqrt(1.15)) + 0.9*1.15, "sqrt1.15", math.sqrt(1.15))
