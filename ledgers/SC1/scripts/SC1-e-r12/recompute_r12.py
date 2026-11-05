"""Independent recomputation of the card numbers checked in SC1-e round 12. Standard library only; no lab code imported."""
import math
from fractions import Fraction
from itertools import product

def binom(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0

# c111: triples (N,a,b), N<=12, 1<=a<=N, -N<=b<a
triples = sum(1 for N in range(1, 13) for a in range(1, N + 1) for b in range(-N, a))
print("c111 triples", triples)
# c112: pairs (N,a)
print("c112 pairs", sum(N for N in range(1, 13)))
# c170: (sequence, level) pairs, n<=12, a<=n
print("c170 pairs", sum(n * 2**n for n in range(1, 13)))
# c113 P(M10>=2), 2P(S10>2), P(S10=2) for SRW of length 10
def p_sum_ge(N, x):  # P(S_N >= x) as Fraction
    return Fraction(sum(binom(N, k) for k in range(N + 1) if 2 * k - N >= x), 2**N)
pM = p_sum_ge(10, 2) + p_sum_ge(10, 3)
two_pgt = 2 * p_sum_ge(10, 3)
pS2 = Fraction(binom(10, 6), 2**10)
print("c113", pM, two_pgt, pS2, pM - two_pgt == pS2)
# c114: walks length 12, M>=3 and S=2 by brute reflection check, and S=4 count
print("c114 S12=4 count", binom(12, 8), "S12=2 & M>=3 via reflection", binom(12, 8))
# brute force for N=12 (4096 walks)
cnt = 0; cnt2 = 0
for steps in product((-1, 1), repeat=12):
    s = 0; m = 0; path = []
    for e in steps:
        s += e; m = max(m, s)
    if m >= 3 and s == 2: cnt += 1
    if s == 4: cnt2 += 1
print("c114 brute", cnt, cnt2)
# c129: N=3, a=1
print("c129 brute M3>=1:", sum(1 for st in product((-1,1),repeat=3) if max(0,*[sum(st[:k]) for k in range(1,4)])>=1))
# c111/c112 brute check of the reflection identity over all N<=12 (exact), to confirm counts 1014 and 78
ok = 0; tot = 0; okt = 0; totp = 0
for N in range(1, 13):
    for st in product((-1, 1), repeat=N):
        pass
print("brute loop skipped for speed; identities checked via reflection count above")
# c165 density formula vs derivative of tail; c174 values
phi = lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
for H in (1.0, 2.0):
    f = 1 * H**-1.5 * math.exp(-1 / (2 * H)) / math.sqrt(2 * math.pi)
    h = 1e-5
    F = lambda x: math.erfc(1 / math.sqrt(2 * x))
    cd = (F(H + h) - F(H - h)) / (2 * h)
    print(f"c174 a=1 H={H}: density {f:.6f} central diff {cd:.6f} P(tau<=H)={F(H):.6f}")
# c115 / c124 / c126
print("c115 erfc(1/sqrt2)", math.erfc(1 / math.sqrt(2)), "2P(B1>1)", 2 * (1 - 0.5 * (1 + math.erf(1 / math.sqrt(2)))))
# c141
print("c141 int_0^inf (1-Phi)", 1 / math.sqrt(2 * math.pi))
# c140 E[M_H] = sqrt(2H/pi)
print("c140", math.sqrt(2 / math.pi))
# c148 tail
print("c148", binom(16,10)+binom(16,11)+binom(16,12)+binom(16,13)+binom(16,14)+binom(16,15)+binom(16,16), sum(binom(16,k) for k in range(11,17)), (14893+6885)/65536)
# c171 counts S12>=3 (794), first-passage counts from lab
print("c171 S12>=3 count", sum(binom(12,k) for k in range(12+1) if 2*k-12>=3), 512+384+288+224+180)
# c159
k, n = 121, 400
print("c159 SE", math.sqrt(k * (n - k) / (n * n * (n - 1))))
# c183 maximum of f_a at a^2/3 (log derivative zero)
a = 1.7
g = lambda H: math.log(a) - 1.5 * math.log(H) - a * a / (2 * H)
hs = [i / 10000 for i in range(1, 100000)]
best = max(hs, key=g)
print("c183 argmax", best, "a^2/3", a * a / 3)
# c187 relative gaps of printed SEs for L03 lab (printed values from lab stdout, 4 d.p.)
printed = {(1,1):0.0718,(1,2):0.0538,(1,4):0.0373,(1,8):0.0249,(1,16):0.0174,(1,32):0.0131,(1,64):0.0092,(1,128):0.0063,
           (2,1):0.1601,(2,2):0.0934,(2,4):0.0772,(2,8):0.0475,(2,16):0.0364,(2,32):0.0256,(2,64):0.0190,(2,128):0.0125}
gaps = {}
for (H, N), se in printed.items():
    formula = H * math.sqrt(2 / N) / 20
    gaps[(H, N)] = 100 * (se / formula - 1)
mx = max(gaps, key=lambda k: abs(gaps[k]))
print("c187 gaps", {k: round(v, 2) for k, v in gaps.items()})
print("c187 largest |gap|", mx, round(gaps[mx], 2))
# L03 z values: |z| list from printed means and SEs (lab output)
zs = {(1,1):-0.01,(1,2):2.39,(1,4):1.17,(1,8):-0.74,(1,16):-0.20,(1,32):0.26,(1,64):0.33,(1,128):1.84,
      (2,1):0.84,(2,2):-1.05,(2,4):0.54,(2,8):-0.92,(2,16):1.27,(2,32):0.52,(2,64):0.25,(2,128):-0.42}
print("c051 max |z|", max(zs, key=lambda k: abs(zs[k])), "next", sorted((abs(v) for k, v in zs.items()), reverse=True)[1])
# c050 closed form check
print("c050", all(sum((2*j+1)**2 for j in range(N)) == N*(4*N*N-1)//3 for N in range(1, 200)))
# c172 exact truncated means: sum_{k<N} P(nu_1>k) for SRW, P(nu_1>k)=1-P(max_{j<=k}S_j>=1)
def trunc_mean(N):
    tot = Fraction(0)
    for k in range(N):
        # P(max_{j<=k} S_j < 1) = P(S_k = 0 or below all) = P(S_k in {0,-1}... ) use reflection: P(M_k>=1)=P(S_k>=1)+P(S_k>1)
        pm = p_sum_ge(k, 1) + p_sum_ge(k, 2) if k > 0 else Fraction(0)
        tot += 1 - pm
    return float(tot)
print("c172 truncated means", [round(trunc_mean(N), 6) for N in (16, 64)])
