"""Independent recomputation of every number on SC1 L07 and L08 (round 3). Own code; does not import the labs."""
import math
import random
from fractions import Fraction
from itertools import product

def phi(x):  # standard normal cdf via erf (independent of erfc used in the labs)
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

out = []
def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)

# ---- L07 Part A: enumeration vs binomial counts, N<=12
ok_identity = 0; total = 0
for n in range(1, 13):
    seqs = list(product((1, -1), repeat=n))
    ends = []
    maxes = []
    for s in seqs:
        pos = 0; hi = 0
        for st in s:
            pos += st; hi = max(hi, pos)
        ends.append(pos); maxes.append(hi)
    for m in range(1, n + 1):
        total += 1
        c_max = sum(1 for h in maxes if h >= m)
        c_ge = sum(1 for e in ends if e >= m)
        c_gt = sum(1 for e in ends if e > m)
        ok_identity += (c_max == c_ge + c_gt)
p("L07 A identity pairs holding:", ok_identity, "of", total)
# exact tails via own binomial sum (independent formula: count of u with 2u-n >= m)
for n in (4, 16, 64, 256, 1024):
    m = math.isqrt(n)
    cnt = 0
    for u in range(n + 1):
        s = 2 * u - n
        if s >= m: cnt += math.comb(n, u)
        if s > m: cnt += math.comb(n, u)
    p("L07 A tail N=%d m=%d count=%d prob=%.6f" % (n, m, cnt, cnt / 2 ** n))
p("L07 A N=16 #S>=4:", sum(math.comb(16, u) for u in range(16 + 1) if 2*u-16 >= 4), " #S>4:", sum(math.comb(16, u) for u in range(17) if 2*u-16 > 4))

# ---- constants
closed = 2 * (1 - phi(1.0))
p("2(1-Phi(1)) = %.12f" % closed, " 1-Phi(1)=%.12f" % (1 - phi(1.0)), " 2*0.1586552539=%.10f" % (2*0.1586552539))
p("sqrt(2/pi)=%.9f" % math.sqrt(2/math.pi), " 1/sqrt(2pi)=%.6f" % (1/math.sqrt(2*math.pi)), " e^-1/2=%.6f" % math.exp(-0.5))
p("erfc(1/sqrt2)=%.12f" % math.erfc(1/math.sqrt(2)), " erfc(1/sqrt(2)) 2*(1-Phi(1)) check", abs(math.erfc(1/math.sqrt(2)) - closed) < 1e-12)
p("(0.3173105079 - closed)=%.3e" % (0.3173105079 - closed), " |0.3173105-closed|=%.3e" % abs(0.3173105-closed))
p("|0.158655 - (1-Phi1)|=%.3e" % abs(0.158655 - (1-phi(1.0))), " |0.797885-sqrt(2/pi)|=%.3e" % abs(0.797885-math.sqrt(2/math.pi)))
p("E[M_1] claimed 0.797885 vs %.9f" % math.sqrt(2/math.pi))
p("(1-Phi(1)) doubled on printed digits:", 2*0.1586552539)

# ---- L07 Part B/C: own simulation, same draw order as the lab (400 paths, 256 fine increments each)
SEED = 20260507
rng = random.Random(SEED)
FINE = 256
PATHS = 400
GRIDS = (4, 16, 64, 256)
sd = math.sqrt(1 / FINE)
maxima = {n: [] for n in GRIDS}
for _ in range(PATHS):
    x = [0.0]
    acc = 0.0
    for _ in range(FINE):
        acc += sd * rng.gauss(0.0, 1.0)
        x.append(acc)
    for n in GRIDS:
        step = FINE // n
        maxima[n].append(max(x[i] for i in range(0, FINE + 1, step)))
viol = 0
for a, b in ((4, 16), (16, 64), (64, 256)):
    for ca, fb in zip(maxima[a], maxima[b]):
        viol += ca > fb
p("L07 B nesting violations:", viol)
def mean_se(v):
    n = len(v); mu = sum(v) / n
    var = sum((x - mu) ** 2 for x in v) / (n - 1)
    return mu, math.sqrt(var / n)
for n in GRIDS:
    ind = [1.0 if x >= 1.0 else 0.0 for x in maxima[n]]
    mu, se = mean_se(ind)
    p("L07 B N=%d p=%.6f count=%d se=%.6f diff=%+.6f" % (n, mu, round(mu * PATHS), se, mu - closed))
for n in GRIDS:
    mu, se = mean_se(maxima[n])
    p("L07 C N=%d mean=%.6f se=%.6f diff=%+.6f" % (n, mu, se, mu - math.sqrt(2/math.pi)))

# ---- L07 Part D: simpson with own rule (composite Simpson, 2000 intervals on [1,13])
def dens(x): return math.exp(-x*x/2)/math.sqrt(2*math.pi)
h = 12.0 / 2000
s = dens(1.0) + dens(13.0)
for i in range(1, 2000):
    s += (4 if i % 2 else 2) * dens(1.0 + i*h)
s *= h / 3
p("L07 D simpson 1-Phi(1)=%.10f erfc=%.10f" % (s, 0.5*math.erfc(1/math.sqrt(2))))

# ---- L08 Part A: first passage via brute force, a=3,n=12
def first_passage_counts(n, a):
    counts = {}
    total_hit = 0
    for s in product((1, -1), repeat=n):
        pos = 0; hit = None
        for k, st in enumerate(s, 1):
            pos += st
            if hit is None and pos >= a: hit = k
        if hit is not None:
            counts[hit] = counts.get(hit, 0) + 1
    return counts
c = first_passage_counts(12, 3)
p("L08 A counts k=3..12:", [c.get(k, 0) for k in range(3, 13)], "sum", sum(c.values()))
p("L08 A P(nu3<=12)=%d/4096=%.6f" % (sum(c.values()), sum(c.values())/4096))
endge = sum(math.comb(12, u) for u in range(13) if 2*u-12 >= 3)
p("L08 A #{S12>=3}=%d prob=%.6f ratio=%s" % (endge, endge/4096, sum(c.values()) == 2*endge))
p("L08 A total sequences:", sum(n*2**n for n in range(1, 13)), " pairs:", sum(range(1, 13)))
# pathwise check (nu<=n iff max>=a) over all n<=12, a<=n
agree = 0; seqs_total = 0
for n in range(1, 13):
    for a in range(1, n+1):
        for s in product((1, -1), repeat=n):
            pos = 0; hit = False; hi = 0
            for st in s:
                pos += st; hi = max(hi, pos)
                if pos >= a: hit = True
            seqs_total += 1
            agree += (hit == (hi >= a))
p("L08 A pathwise agree %d of %d" % (agree, seqs_total))

# ---- L08 Part B: E[min(nu_1,N)] by DP on positions staying below 1 (independent of walk identity)
def trunc_means(horizons, largest):
    dist = {0: Fraction(1)}  # positions, not yet reached level 1
    running = Fraction(0)
    res = {}
    for k in range(largest):
        running += sum(dist.values())  # P(nu_1 > k) = P(not reached by step k)
        new = {}
        for pos, pr in dist.items():
            for st in (1, -1):
                q = pos + st
                if q >= 1: continue
                new[q] = new.get(q, Fraction(0)) + pr / 2
        dist = new
        if k + 1 in horizons: res[k+1] = running
    return res
tm = trunc_means((16, 64, 256), 256)
for n in (16, 64, 256):
    p("L08 B N=%d E=%.6f exact_fraction_den_bits=%d" % (n, float(tm[n]), tm[n].denominator.bit_length()))

# ---- L08 Part C: own simulation of capped first passage (draw order: rng.random() until hit)
rng2 = random.Random(20260508)
caps = []
for _ in range(1000):
    pos = 0; first = 256
    for k in range(1, 257):
        pos += 1 if rng2.random() < 0.5 else -1
        if pos >= 1:
            first = k; break
    caps.append(first)
for n in (16, 64, 256):
    v = [min(x, n) for x in caps]
    mu, se = mean_se([float(x) for x in v])
    z = (mu - float(tm[n])) / se
    p("L08 C N=%d mean=%.6f se=%.6f exact=%.6f z=%+.4f" % (n, mu, se, float(tm[n]), z))

# ---- L08 Part D
def F(a, t): return math.erfc(a / math.sqrt(2*t))
def f(a, t): return a/(math.sqrt(2*math.pi)*t**1.5)*math.exp(-a*a/(2*t))
for t in (1.0, 2.0):
    d = 1e-5
    num = (F(1, t+d) - F(1, t-d)) / (2*d)
    p("L08 D t=%g F=%.6f f=%.9f central=%.9f diff=%.2e" % (t, F(1,t), f(1,t), num, abs(f(1,t)-num)))
p("L08 D f_1(1) claim 0.241971 vs %.9f; f_1(2) claim 0.109848 vs %.9f" % (f(1,1.0), f(1,2.0)))
p("L08 D 1/sqrt(2pi)=%.6f 2^-1.5=%.6f e^-0.25=%.6f" % (1/math.sqrt(2*math.pi), 2**-1.5, math.exp(-0.25)))
p("L08 D erfc(0.5)=%.10f  P(tau<=2)" % math.erfc(0.5))
p("L08 Remark: mode a^2/3 check: f_1 at 1/3 vs neighbours", f(1,1/3), f(1,0.30), f(1,0.36))
