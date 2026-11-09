# Independent round-4 recomputation of every number in the changed L02 text and its problems/quiz (exact Fractions).
import random
from fractions import Fraction as F
def H(n): return sum((F(1, k) for k in range(1, n + 1)), F(0))
def G(n): return sum((F(1, 2**k) for k in range(1, n + 1)), F(0))
checks = []
def chk(label, ok): checks.append((label, bool(ok)))
# Proposition 3.3: H_{2N}-H_N >= 1/2 for N = 1..400
chk("Prop 3.3 bound N=1..400", all(H(2*N) - H(N) >= F(1, 2) for N in range(1, 401)))
chk("H_2-H_1 = 1/2 (quiz, E2, Lab 1 minimum)", H(2) - H(1) == F(1, 2))
chk("H_4-H_2 = 7/12 (E2)", H(4) - H(2) == F(7, 12))
chk("min over N=1..200 of H_2N-H_N is 1/2 at N=1", min((H(2*N) - H(N), N) for N in range(1, 201)) == (F(1, 2), 1))
chk("Prop 3.3 proof: sum of 1/(N+1)..1/(2N) is N terms, each >= 1/(2N)", all(sum((F(1, j) for j in range(N+1, 2*N+1)), F(0)) >= F(1, 2) and len(range(N+1, 2*N+1)) == N for N in range(1, 60)))
chk("Lemma 3.4 identity G_m-G_n = 1/2^n-1/2^m, 0<=n<m<=60, count 1830", sum(1 for n in range(0, 60) for m in range(n+1, 61) if G(m)-G(n) == F(1, 2**n)-F(1, 2**m)) == 1830 and sum(1 for n in range(0,60) for m in range(n+1,61)) == 1830)
chk("sum_{j=1}^{60} j = 1830", sum(range(1, 61)) == 1830)
chk("G_3 = 7/8 (quiz)", G(3) == F(7, 8))
chk("G_3 - G_1 = 3/8 (M3)", G(3) - G(1) == F(3, 8))
def passes_from(N):
    return all(abs(G(m) - G(n)) < F(1, 1024) for n in range(N, 60) for m in range(n + 1, 61))
chk("Prop 3.5 (finite search m<=60): test with eps=2^-10 passes from N iff N>=10, N=0..20", all(passes_from(N) == (N >= 10) for N in range(0, 21)))
chk("Lemma 3.4 bound: G_m-G_n < 1/2^n for all pairs m<=60", all(G(m)-G(n) < F(1, 2**n) for n in range(0, 60) for m in range(n+1, 61)))
chk("R2: H_{2^k} >= 1 + k/2 for k=0..10", all(H(2**k) >= 1 + F(k, 2) for k in range(0, 11)))
chk("R3 identity sum_{k=n}^{m-1} b^k = b^n(1-b^(m-n))/(1-b) (b=1/3, n=2, m=7)", sum(F(1,3)**k for k in range(2, 7)) == F(1,3)**2 * (1 - F(1,3)**5) / (1 - F(1,3)))
# R3: beta^N <= 1/(N h) with beta = 1/(1+h)
rnd = random.Random(4)
ok = True
for _ in range(2000):
    h = F(rnd.randint(1, 500), rnd.randint(1, 500)); N = rnd.randint(1, 60)
    beta = 1 / (1 + h)
    ok &= beta**N <= 1 / (N * h)
chk("R3 beta^N <= 1/(Nh) on 2000 random (h,N)", ok)
# Canon break 1: bisection from [0,2] on S={x>=0: x^2<2}; endpoints rational; width 2/2^n; sup^2 = 2 (numerically via bracket)
def inS(x): return x >= 0 and x * x < 2
a, b = F(0), F(2); widths = []; rat = True
for n in range(0, 13):
    widths.append(b - a)
    if n == 12: break
    m = (a + b) / 2
    if inS(m): a = m
    else: b = m
chk("bisection widths are 2/2^n for n=0..12", all(w == F(2, 2**n) for n, w in enumerate(widths)))
chk("bracket after 12 steps is [181/128, 2897/2048]", (a, b) == (F(181, 128), F(2897, 2048)))
chk("bracket endpoints 181/128 and 2897/2048 satisfy a^2<2<=b^2", F(181, 128)**2 < 2 <= F(2897, 2048)**2)
chk("first width below 1/1000 is step 11 (width 1/1024)", F(2, 2**11) < F(1, 1000) and F(2, 2**10) >= F(1, 1000))
# Misconception 2: sqrt(n) gap bound
chk("|sqrt(n+1)-sqrt(n)| <= 1/sqrt(n+1) for n=1..10000", all(abs((n+1)**0.5 - n**0.5) <= 1/((n+1)**0.5) + 1e-15 for n in range(1, 10001)))
n_fail = [a for a in checks if not a[1]]
for label, ok in checks: print("PASS" if ok else "FAIL", label)
print("SUMMARY pass=%d total=%d" % (sum(ok for _, ok in checks), len(checks)))
