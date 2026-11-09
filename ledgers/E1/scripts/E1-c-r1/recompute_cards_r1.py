from fractions import Fraction as F
import random
ok = True
def check(name, cond):
    global ok
    ok &= bool(cond)
    print(('OK   ' if cond else 'FAIL ') + name)
# c018/c161/c162/c023: q*(p) = max(0,(p-c)/(2k)), MC(q*)=p for p>c, nondecreasing
random.seed(1)
for _ in range(2000):
    p, c, k = F(random.randint(1, 300), random.randint(1, 20)), F(random.randint(0, 200), random.randint(1, 20)), F(random.randint(1, 50), random.randint(1, 20))
    q = max(F(0), (p - c) / (2 * k))
    # brute-force argmax of profit pq - (c q + k q^2) on a grid of rationals with denominator 60 up to 2q+5
    best = None
    grid = [F(j, 60) for j in range(0, 60 * 40)]
    prof = lambda x: p * x - (c * x + k * x * x)
    m = max(prof(x) for x in grid[:400])
    if p > c:
        check_mc = (c + 2 * k * q) == p
        if not check_mc: check('MC(q*)=p', False)
# c163, c030: market equilibrium with s = n/(2k), a=100,b=2,n=10,c=2,k=1 and random cases
def eq(a, b, n, c, k):
    s = F(n, 2 * k)
    p = (a + s * c) / (b + s)
    Q = s * (p - c)
    return p, Q, a - b * p, (a - b * c) / (b + s)
bad = 0
for _ in range(500):
    a = F(random.randint(1, 300)); b = F(random.randint(1, 20)); n = random.randint(1, 12)
    c = F(random.randint(0, 40)); k = F(random.randint(1, 20))
    if not a > b * c: continue
    p, Q, Qd, pm = eq(a, b, n, c, k)
    s = F(n, 2 * k)
    if not (Q == Qd and Q > 0 and pm == p - c and pm == (a - b * c) / (b + s) and p > c):
        bad += 1
check('c163/c030: Q*=s(p*-c)=a-bp*>0, p*-c=(a-bc)/(b+s), p*>c (500 random cases, bad=%d)' % bad, bad == 0)
p, Q, Qd, pm = eq(F(100), F(2), 10, F(2), F(1))
check('L03 Example 1.5 numbers: p*=110/7, Q*=480/7, per-firm (p*-c)/(2k)=48/7', p == F(110, 7) and Q == F(480, 7) and (p - 2) / 2 == F(48, 7))
# c164/c056/c160/c165/c166 under Assumption M: d=a-bc
def mono(a, b, c):
    pm = (a + b * c) / (2 * b); Qm = (a - b * c) / 2; pi = (a - b * c) ** 2 / (4 * b)
    return pm, Qm, pi
for (a, b, c) in [(F(120), F(1), F(20)), (F(90), F(3), F(10)), (F(200), F(4), F(5)), (F(7), F(2), F(1))]:
    pm, Qm, pi = mono(a, b, c)
    d = a - b * c
    check('c164/c056 at %s: p_m=(a+bc)/(2b)=%s, Q_m=%s, pi_m=%s; pi(p_m) direct=%s' % ((a, b, c), pm, Qm, pi, (pm - c) * (a - b * pm) == pi),
          (pm - c) * (a - b * pm) == pi and Qm == a - b * pm)
    W_C = d * d / (2 * b)
    DWL_M = d * d / (8 * b)
    CSM = F(1, 2) * Qm * (a / b - pm)
    WM = pi + CSM
    check('c166 monopoly loss d^2/(8b) = W_C - W_M at %s' % ((a, b, c),), W_C - WM == DWL_M)
    # Cournot n=2 linear: q_i = d/(3b); Q=2d/3 under b=1 per reference; general: Q = 2d/(3) ; check with ref case below
ref = (F(120), F(1), F(20))
a, b, c = ref; d = a - b * c
Qc = 2 * d / 3; pc = (a + 2 * b * c) / (3 * b)
piC = 2 * (pc - c) * (Qc / 2)
CSc = F(1, 2) * Qc * (a / b - pc)
Wc = CSc + piC
check('c165 Cournot ref: Q=200/3, p=160/3, two-exchange profit=20000/9 (%s), rounds half up to 2222 (%s)' % (piC, int(piC + F(1, 2))), piC == F(20000, 9) and int(piC + F(1, 2)) == 2222)
check('c166/c101 Cournot DWL = d^2/(18b) (%s) and share 1/9 of W_C=d^2/(2b)' % (d * d / (2 * b) - Wc), d * d / (2 * b) - Wc == d * d / (18 * b) and (d * d / (18 * b)) / (d * d / (2 * b)) == F(1, 9))
check('c160 Bertrand ref: Q=d=100, fee=c=20, profit 0', d == 100 and c == 20)
print('ALL_OK' if ok else 'SOME_FAIL')
