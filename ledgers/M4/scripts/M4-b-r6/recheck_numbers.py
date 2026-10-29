import math, random

# L05: independent re-derivation of Part A-C unrounded values
S1, S2, RHO, SEED = 0.02, 0.03, 0.6, 20260501
def draws(n):
    rng = random.Random(SEED); out = []
    for _ in range(n):
        z1 = rng.gauss(0.0, 1.0); z2 = rng.gauss(0.0, 1.0)
        out.append((S1*z1, S2*(RHO*z1 + math.sqrt(1-RHO*RHO)*z2)))
    return out
def scov(xs):
    n = len(xs); m1 = sum(x for x,_ in xs)/n; m2 = sum(y for _,y in xs)/n
    s11 = sum((x-m1)**2 for x,_ in xs)/(n-1); s22 = sum((y-m2)**2 for _,y in xs)/(n-1)
    s12 = sum((x-m1)*(y-m2) for x,y in xs)/(n-1)
    return s11, s12, s22
sig = (S1*S1, RHO*S1*S2, S2*S2)
for n in (100, 20000):
    s11, s12, s22 = scov(draws(n))
    errs = [abs(s11-sig[0]), abs(s12-sig[1]), abs(s22-sig[2])]
    print("L05 n", n, "entry errors", ["%.10g" % e for e in errs], "max", "%.10g" % max(errs))
s11, s12, s22 = scov(draws(20000))
corr = s12/math.sqrt(s11*s22)
print("L05 corr unrounded", "%.10f" % corr, "err", "%.10f" % (corr-RHO))
qs = []
for k in range(9):
    a = k*math.pi/8; w = (math.cos(a), math.sin(a))
    q = w[0]*w[0]*s11 + 2*w[0]*w[1]*s12 + w[1]*w[1]*s22
    qs.append(q)
print("L05 max/min quad", "%.6f" % (max(qs)/min(qs)), "argmax", qs.index(max(qs)), "argmin", qs.index(min(qs)))
print("L05 E1 rel err s11", "%.8f" % ((s11-sig[0])/sig[0]), "printed-based", "%.8f" % ((0.00039491-0.0004)/0.0004))
print("L05 Part C min value", "%.10g" % min(qs))

# L06
def chi_t(rng, nu):
    z = rng.gauss(0.0, 1.0)
    w = sum(rng.gauss(0.0, 1.0)**2 for _ in range(nu))
    return w, z/(w/nu)**0.5
N = 100000
res = {}
for nu in (5, 10):
    rng = random.Random(20260602 + nu); ts = [chi_t(rng, nu)[1] for _ in range(N)]
    m = sum(ts)/N; v = sum((t-m)**2 for t in ts)/(N-1); ex = nu/(nu-2)
    res[nu] = (m, v, (v-ex)/ex)
    print("L06 nu", nu, "mean %.10f var %.10f relerr %.10f" % (m, v, (v-ex)/ex))
print("L06 E1 relerr printed-based %.8f" % ((1.669114-1.666667)/1.666667))
print("L06 E2 ratio |err10|/|err5| %.6f" % (abs(res[10][2])/abs(res[5][2])))
rng = random.Random(20260602 + 500)
ws = []
for _ in range(N):
    w, _ = chi_t(rng, 5); ws.append(w)
mw = sum(ws)/N
print("L06 mean W %.10f diff %.10f rel %.8f pct %.6f" % (mw, mw-5, (mw-5)/5, 100*(mw-5)/5))
