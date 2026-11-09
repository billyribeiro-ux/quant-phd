"""Independent recomputation of L15 numbers (verifier round 3). Standard library only."""
import math
def g(x, y): return 0.0 if x == 0 and y == 0 else x * y / (x * x + y * y)
def f(x, y): return 0.0 if x == 0 and y == 0 else x * x * y / (x * x + y * y)
exact = 2 / (3 * math.sqrt(3))
print("exact max |cos^2 sin| 2/(3 sqrt3) =", f"{exact:.10f}")
for k in range(1, 7):
    r = 10.0 ** -k
    vals = []
    for deg in range(360):
        t = 2 * math.pi * deg / 360
        x, y = r * math.cos(t), r * math.sin(t)
        vals.append((abs(f(x, y)), deg, abs(g(x, y))))
    mf = max(vals)
    mg = max(v[2] for v in vals)
    argmax_f = sorted(v[1] for v in vals if abs(v[0] - mf[0]) < 1e-15 * max(1, r))
    print(f"r=1e-{k:02d} max|g|={mg:.6f} max|f|/r={mf[0]/r:.4f} argmax deg (|f| within 1e-15 rel)={argmax_f}")
# angles of the sampled maximum with unrounded value
r = 1e-3
ang = []
for deg in range(360):
    t = 2 * math.pi * deg / 360
    ang.append((abs(f(r*math.cos(t), r*math.sin(t)))/r, deg))
ang.sort(reverse=True)
print("top 6 sampled |f|/r at r=1e-3:", [(round(v, 10), d) for v, d in ang[:6]])
# g on grid max
print("g at 45 deg, r=1e-3:", g(r*math.cos(math.pi/4), r*math.sin(math.pi/4)))
# f(1/n,1/n)
for n in (10, 100, 1000, 10000):
    t = 1.0 / n
    print("n", n, "g", g(t, t), "f", f(t, t), "1/(2n)", 1 / (2 * n))
print("sin of 35.264 deg =", math.sin(math.atan(1/math.sqrt(2))), " 1/sqrt3 =", 1/math.sqrt(3))
print("M1 sqrt6 =", math.sqrt(6), " |(1,2,2)|=", math.sqrt(1+4+4))
print("E1 values: (1-s^2)s at 1/sqrt3 =", (1-1/3)/math.sqrt(3), "2/(3sqrt3)=", exact)
print("P1/P2/P3 sanity: sqrt(2) =", math.sqrt(2))
