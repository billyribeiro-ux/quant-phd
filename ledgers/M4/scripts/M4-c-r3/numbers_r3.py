# Independent re-derivation of every printed number in the L08-L10 pages (verifier round 3).
import math, random
from fractions import Fraction as F

def hdr(x): print("\n== " + x)

# ---------- L09: exact die-sum values and thresholds ----------
hdr("L09 Part A exact")
faces = range(1, 7)
def mass(n):
    m = {0: F(1)}
    for _ in range(n):
        nm = {}
        for s, p in m.items():
            for f in faces:
                nm[s + f] = nm.get(s + f, F(0)) + p / 6
        m = nm
    return m
phi1 = 0.5 * (1 + math.erf(1 / math.sqrt(2)))
print("Phi(1) =", f"{phi1:.6f}", " 7/60 =", float(F(35, 12) / 25), " 35/48 =", float(F(35, 48)))
for n in (1, 5, 10, 20, 40):
    th_real = 3.5 * n + math.sqrt(35 * n / 12)
    th = math.floor(th_real)
    m = mass(n)
    assert sum(m.values()) == 1
    p = sum(v for s, v in m.items() if s <= th)
    print(f"n={n} threshold_real={th_real:.4f} floor={th} P={float(p):.6f} gap={float(p)-phi1:+.6f}")
print("n=10 threshold_real 40.4006? ", round(35 + math.sqrt(35 * 10 / 12), 4))
print("Chebyshev n=10,100,1000,10000:", [round((35/12)/(n*0.25), 4) for n in (10, 100, 1000, 10000)])
print("Chebyshev n=2 two-point bound:", 1 / (2 * 0.25))

# ---------- L09 Part B / Part C (own code, same stated seeds) ----------
hdr("L09 Part B path")
rng = random.Random(2026)
path = [rng.randint(1, 6) for _ in range(10000)]
for n in (10, 100, 1000, 10000):
    mean = sum(path[:n]) / n
    print(f"n={n} mean={mean:.4f} gap={mean-3.5:+.4f}")
hdr("L09 Part C")
for n in (5, 30, 200):
    r = random.Random(2026)
    hits = 0
    for _ in range(4000):
        tot = sum(r.randint(1, 6) for _ in range(n))
        z = (tot / n - 3.5) / (math.sqrt(35 / 12) / math.sqrt(n))
        hits += z <= 1
    p = hits / 4000
    se = math.sqrt(p * (1 - p) / 4000)
    print(f"n={n} hits={hits} est={p:.4f} se={se:.4f} gap={p-phi1:+.4f} unrounded_gap={p-phi1:.6f}")
print("E2 check: gap 0.8552-phi1 =", round(0.8552 - phi1, 6), " se(0.8552)=", round(math.sqrt(0.8552*0.1448/4000), 6), " ratio(0.0139/0.0056)=", round(0.0139/0.0056, 3))
print("E2 unrounded: 3421/4000=", 3421/4000, " gap", round(3421/4000-phi1, 6), " se", round(math.sqrt((3421/4000)*(1-3421/4000)/4000), 6), " ratio", round((3421/4000-phi1)/math.sqrt((3421/4000)*(1-3421/4000)/4000), 3))

# ---------- L08 matrices ----------
hdr("L08 matrices")
A = [[2, 0], [1, 1]]; Q = [[0, -1], [1, 0]]
def mm(X, Y): return [[sum(X[i][k]*Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def tr(X): return [[X[j][i] for j in range(2)] for i in range(2)]
Sig = mm(A, tr(A)); B = mm(A, Q); ATA = mm(tr(A), A)
print("AA^T", Sig, " B", B, " BB^T", mm(B, tr(B)), " A^TA", ATA, " A^TA-Sig", [[ATA[i][j]-Sig[i][j] for j in range(2)] for i in range(2)])
print("QQ^T", mm(Q, tr(Q)), " w^T Sig w (1,1)=", sum(Sig[i][j] for i in range(2) for j in range(2)))
print("M1 A=[[1,1],[0,2]] AA^T:", mm([[1,1],[0,2]], tr([[1,1],[0,2]])))
hdr("L08 Part B")
r = random.Random(2026)
rows_x = []; rows_y = []
for _ in range(20000):
    z1 = r.gauss(0.0, 1.0); z2 = r.gauss(0.0, 1.0)
    rows_x.append((1 + 2*z1, -2 + z1 + z2))
    rows_y.append((1 + 0*z1 + (-2)*z2, -2 + 1*z1 + (-1)*z2))
def smean(rows): n = len(rows); return (sum(a for a, b in rows)/n, sum(b for a, b in rows)/n)
def scov(rows):
    n = len(rows); m = smean(rows)
    c11 = sum((a-m[0])**2 for a, b in rows)/(n-1)
    c22 = sum((b-m[1])**2 for a, b in rows)/(n-1)
    c12 = sum((a-m[0])*(b-m[1]) for a, b in rows)/(n-1)
    return [[c11, c12], [c12, c22]]
mx = smean(rows_x); cx = scov(rows_x); cy = scov(rows_y)
print("mean X", [round(v, 4) for v in mx], "cov X", [[round(v, 4) for v in row] for row in cx])
gapX = max(abs(cx[i][j]-Sig[i][j]) for i in range(2) for j in range(2))
gapXA = max(abs(cx[i][j]-ATA[i][j]) for i in range(2) for j in range(2))
gapY = max(abs(cy[i][j]-Sig[i][j]) for i in range(2) for j in range(2))
print("gapX", round(gapX, 4), "gapX_ATA", round(gapXA, 4), "cov Y", [[round(v, 4) for v in row] for row in cy], "gapY", round(gapY, 4))
print("E1 gaps from printed X:", [round(abs(v-s), 4) for v, s in ((4.0073, 4), (2.0187, 2), (1.9936, 2))])

# ---------- L10 tails, closed forms, Part D ----------
hdr("L10 tails")
def arctan(x): return math.atan(x)
print("P(|C|>10)=", (2/math.pi)*math.atan(0.1), " 10*=", 10*(2/math.pi)*math.atan(0.1))
print("P(|Z|>10)=", math.erfc(10/math.sqrt(2)))
y = 10/math.sqrt(3)
print("P(|V|>10)=", 2*(math.atan(math.sqrt(3)/10) - (10*math.sqrt(3)/(3+100)))/math.pi, " ratio C/Z=", ((2/math.pi)*math.atan(0.1))/math.erfc(10/math.sqrt(2)))
print("2/pi=", 2/math.pi, " 4sqrt3/pi=", 4*math.sqrt(3)/math.pi, " F_V(sqrt3)=", 0.5+(math.atan(1)+0.5)/math.pi, " 3/4+1/(2pi)=", 0.75+1/(2*math.pi))
for x in (10.0, 100.0, 1000.0):
    pc = (2/math.pi)*math.atan(1/x)
    ys = x/math.sqrt(3)
    pv = 2*(math.atan(1/ys) - ys/(1+ys*ys))/math.pi
    print(f"x={x:.0f} xP(C)={x*pc:.6f} x^3P(V)={x**3*pv:.6f}")
print("arctan(0.1)=", math.atan(0.1))
# Cross-check Prop 1.3 F_V integral by fine midpoint on [-2,2]
def fv(t): return 2/(math.pi*math.sqrt(3))*(1+t*t/3)**-2
N=400000; h=4/N
mid=h*sum(fv(-2+(k+0.5)*h) for k in range(N))
Fv=lambda x: 0.5+(math.atan(x/math.sqrt(3))+(x/math.sqrt(3))/(1+x*x/3))/math.pi
print("midpoint", round(mid, 9), "closed", round(Fv(2)-Fv(-2), 9))
# Prop 2.3 bound f_V >= 3 sqrt3/(2 pi t^4) for t^2>=3
ok = all(fv(t) >= 3*math.sqrt(3)/(2*math.pi*t**4) - 1e-15 for t in [math.sqrt(3)+0.01*k for k in range(1, 20000)])
print("f_V >= 3sqrt3/(2pi t^4) on t>=sqrt3 sample:", ok)
print("P(V>x) bound check at x=2: exact", (1-Fv(2)), " lower bound sqrt3/(2 pi x^3)=", math.sqrt(3)/(2*math.pi*8))

# ---------- L10 Part C (own code; seeds 2026,2027,2028 and seed+100n) ----------
hdr("L10 Part C")
def incl_quartiles(v):
    s = sorted(v); n = len(s)
    def q(p):
        pos = (n - 1) * p
        lo = math.floor(pos); frac = pos - lo
        return s[lo] + frac * (s[min(lo+1, n-1)] - s[lo])
    return q(0.25), q(0.75)
def draw_t(r):
    z = r.gauss(0, 1); w = sum(r.gauss(0, 1)**2 for _ in range(3)); return z/math.sqrt(w/3)
def draw_c(r):
    return math.tan(math.pi*(r.random()-0.5))
laws = (("normal", lambda r: r.gauss(0, 1), 2026, 1.0), ("t3", draw_t, 2027, math.sqrt(3)), ("cauchy", draw_c, 2028, None))
for name, d, sd, sigma in laws:
    for n in (10, 100):
        r = random.Random(sd + 100*n)
        means = [sum(d(r) for _ in range(n))/n for _ in range(400)]
        q1, q3 = incl_quartiles(means)
        line = f"{name} n={n} IQR={q3-q1:.4f}"
        if sigma:
            st = [math.sqrt(n)*m/sigma for m in means]
            mu_ = sum(st)/len(st)
            var = sum((s_-mu_)**2 for s_ in st)/(len(st)-1)
            line += f" var={var:.4f}"
        print(line)
hdr("L10 Part B running means")
for name, d, sd in (("normal", lambda r: r.gauss(0, 1), 2026), ("t3", draw_t, 2027), ("cauchy", draw_c, 2028)):
    r = random.Random(sd); tot = 0.0; cnt = 0; out = []
    for tgt in (10, 100, 1000, 10000):
        while cnt < tgt:
            tot += d(r); cnt += 1
        out.append(f"{tot/tgt:+.4f}")
    print(name, out)
