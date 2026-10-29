import math, random

def run(beta, alpha, grid, tol=None, n_sweeps=None, start=None):
    def res(k): return k**alpha
    def B(vals):
        out = []
        for k in grid:
            r = res(k)
            out.append(max(math.sqrt(r - kp) + beta*vals[j] for j, kp in enumerate(grid) if kp <= r))
        return out
    def sd(a, b): return max(abs(x-y) for x, y in zip(a, b))
    return B, sd

# Lab 1 model
beta, alpha = 0.9, 0.5
G1 = [0.5, 0.9, 1.4]
B1, sd1 = run(beta, alpha, G1)
v0 = [0.0]*3
v1 = B1(v0)
print("L1 V1 unrounded", v1)
print("L1 sup|BV0-BV1| =", sd1(B1(v0), B1(v1)), " beta*sup|V0-V1| =", beta*sd1(v0, v1))
vals = v0; n = 0; cert = math.inf; changes=[]
while cert > 1e-6:
    new = B1(vals); ch = sd1(new, vals); cert = beta/(1-beta)*ch; vals = new; n += 1
    changes.append((n, ch, cert))
print("L1 first 3:", changes[:3])
print("L1 stop n", n, "change", changes[-1][1], "cert", changes[-1][2])
ref = v0
for _ in range(100000):
    nxt = B1(ref)
    small = beta/(1-beta)*sd1(nxt, ref) <= 1e-12
    ref = nxt
    if small: break
print("L1 actual error", sd1(vals, ref), "cert", changes[-1][2])
# Lab 2 ratio
w = [0.1, 0.2, 0.3]
print("L2 ratio", sd1(B1([0.0]*3), B1(w))/sd1([0.0]*3, w))
print("L2 diff sup", sd1(B1([0.0]*3), B1(w)))
# Lab 2 loop
vals = [0.0]*3; n=0; cert=math.inf
while cert > 1e-6 and n < 300:
    n += 1; new = B1(vals); ch = sd1(new, vals); cert = beta/(1-beta)*ch; vals = new
print("L2 n", n, "cert %.10e" % cert, "change %.10e" % ch)

# Lab 3
beta3, alpha3 = 0.9, 0.3
G3 = [0.45 + 0.25*j for j in range(10)]
B3, sd3 = run(beta3, alpha3, G3)
gap = min(abs(kp - k**alpha3) for k in G3 for kp in G3)
print("L3 gap %.10f" % gap, "gap>1e-6", gap > 1e-6)
vals = [0.0]*10; n=0; cert=math.inf; ch=math.inf
while cert > 1e-10:
    new = B3(vals); ch = sd3(new, vals); cert = beta3/(1-beta3)*ch; vals = new; n += 1
print("L3 sweeps", n, "change %.6e" % ch, "cert %.6e" % cert)
bu = math.sqrt(max(G3)**alpha3); na = 0
while beta3**na*bu/(1-beta3) > 1e-10: na += 1
print("L3 apriori", na, "U", bu)
res = sd3(B3(vals), vals)
print("L3 residual %.6e" % res, "(1+b)cert %.6e" % ((1+beta3)*cert), "ratio res/cert", res/cert)
rng = random.Random(7); worst = 0.0
for _ in range(200):
    v = [rng.uniform(0.0, 4.0) for _ in G3]; w2 = [rng.uniform(0.0, 4.0) for _ in G3]
    worst = max(worst, sd3(B3(v), B3(w2))/sd3(v, w2))
print("L3 worst ratio %.15f" % worst, "minus beta", worst - 0.9)
print("L3 V", ["%.6f" % x for x in vals])
