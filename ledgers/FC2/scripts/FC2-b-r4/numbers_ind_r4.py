"""Round-4 independent recomputation of the prose numbers in FC2 L04-L06 (exact Fractions and float where stated)."""
import math
from fractions import Fraction as F

out = []
def check(label, got, want):
    ok = got == want
    out.append(f"{'OK ' if ok else 'BAD'} {label}: got {got} want {want}")

# L04 Example 2.5 and Remark 2.6, Lab 1 Part 2
DF = F(9, 10)
path = [100, 120, 90, 80, 110]
calls = [max(s - 100, 0) for s in path]
puts = [max(100 - s, 0) for s in path]
check("L04 call intrinsic 0..4", calls, [0, 20, 0, 0, 10])
check("L04 put intrinsic 0..4", puts, [0, 0, 10, 20, 0])
check("L04 call hold PV at 0 (10*(9/10)^4)", F(10) * DF**4, F(6561, 1000))
check("L04 exercise call date1 PV at 0", F(20) * DF, 18)
check("L04 put best date3 PV", F(20) * DF**3, F(1458, 100))
check("L04 r = ln(10/9) approx 0.10536", round(math.log(10 / 9), 5), 0.10536)
# R1: S_tau - 100 = 20 (10/9)^3
s_tau = 100 + F(20) * F(10, 9) ** 3
check("L04 R1 threshold 100+20000/729", s_tau, 100 + F(20000, 729))
check("L04 R1 to five decimals", f"{float(s_tau):.5f}", "127.43484")
# R3 path 100, 90, 95, 110, 150
p3 = [100, 90, 95, 110, 150]
check("L04 R3 call intrinsic dates 0..3", [max(s - 100, 0) for s in p3[:4]], [0, 0, 0, 10])
check("L04 R3 exercise date3 PV", F(10) * DF**3, F(729, 100))
check("L04 R3 hold PV 50*(9/10)^4", F(50) * DF**4, F(32805, 1000))
# E2 variant last spot 90
check("L04 E2 put PV at expiry 10*(9/10)^4", F(10) * DF**4, F(6561, 1000))
check("L04 E2 put date3 PV unchanged", F(20) * DF**3, F(1458, 100))
# M1, M2
check("L04 M1 break-even", F(50) + 4, 54)
check("L04 M2 break-even", F(80) - 3, 77)

# L05 Lab 1 synthetic set, D = 9/10 exact, strikes 80..120 USD, spot 100 USD
S = F(100); D = F(9, 10)
K = [F(80), F(90), F(100), F(110), F(120)]
C = [F(max(S - D * k, F(0))) + F(max(F(100) - k, F(0))) / 10 for k in K]
P = [c - S + D * k for c, k in zip(C, K)]
check("L05 calls USD", [str(x) for x in C], ["30", "20", "10", "1", "0"])
check("L05 puts USD", [str(x) for x in P], ["2", "1", "0", "0", "8"])
check("L05 parity residual", [c - p - S + D * k for c, p, k in zip(C, P, K)], [0] * 5)
# planted put +3 USD at 100
pp = list(P); pp[2] += 3
check("L05 planted put parity cost", [c - p - S + D * k for c, p, k in zip(C, pp, K)][2], F(-3))
# planted call/put +5 at 90
cc = list(C); cc[1] += 5; pq = list(P); pq[1] += 5
viol = []
for i in range(5):
    for j in range(i + 1, 5):
        for k in range(j + 1, 5):
            lam = (K[k] - K[j]) / (K[k] - K[i])
            if cc[j] > lam * cc[i] + (1 - lam) * cc[k]:
                viol.append((int(K[i]), int(K[j]), int(K[k])))
check("L05 planted convexity violated triples", viol, [(80, 90, 100), (80, 90, 110), (80, 90, 120)])
# E1 second differences in cents (C in cents = 100*USD)
c_cents = [int(x * 100) for x in C]
check("L05 E1 second differences cents at 90,100,110",
      [c_cents[0] - 2 * c_cents[1] + c_cents[2], c_cents[1] - 2 * c_cents[2] + c_cents[3], c_cents[2] - 2 * c_cents[3] + c_cents[4]],
      [0, 100, 800])
# M1 parity: P = 8 - 100 + 0.97*105
check("L05 M1 put", F(8) - 100 + F(97, 100) * 105, F(985, 100))
# M2 lower bound and position
check("L05 M2 lower bound", max(F(50) - F(95, 100) * 40, 0), 12)
check("L05 M2 receives", F(3) - 50 + F(95, 100) * 40, -9)
# M3 convexity 15, 9, 4 at 90,100,110
check("L05 M3 chord", (F(15) + 4) / 2, F(19, 2))
check("L05 M3 second difference", F(15) - 2 * 9 + 4, 1)
# Section 5 example 100 e^{-0.1} - 50
check("L05 S5 bound 100e^-0.1-50 = 40.48", f"{100 * math.exp(-0.1) - 50:.2f}", "40.48")
# R2 r = -0.1: D = e^{0.1}; bound 120 - 100 e^{0.1}
check("L05 R2 bound 9.48", f"{120 - 100 * math.exp(0.1):.2f}", "9.48")
# E3: 0.9*120-100 = 8 ; put at 120 = 8
check("L05 E3 put bound", F(9, 10) * 120 - 100, 8)
# Corollary/Thm 3.2 butterfly g(s) on a grid of s >= 0
def g(s, k1, k2, k3, lam):
    f = lambda x: max(x, 0)
    return lam * f(s - k1) + (1 - lam) * f(s - k3) - f(s - k2)
ok = True
for k1, k2, k3 in [(80, 90, 100), (80, 90, 120), (1, 5, 6), (3, 7, 20)]:
    lam = F(k3 - k2, k3 - k1)
    assert lam * k1 + (1 - lam) * k3 == k2
    for s in range(0, 200):
        if g(F(s), F(k1), F(k2), F(k3), lam) < 0:
            ok = False
check("L05 Theorem 3.2 butterfly payoff >= 0 on grid s in 0..199", ok, True)
# Theorem 4.1 date-t bound with r>=0 e^{-r(tau-t)}K <= K trivially; Remark 4.2 r<0 example
# L06 numbers
Rf, u, d = F(5, 4), F(3, 2), F(1, 2)
q = (Rf - d) / (u - d)
check("L06 q", q, F(3, 4))
V1u, V1d = F(50), F(0)
Delta = (V1u - V1d) / ((u - d) * 100)
B = (u * V1d - d * V1u) / ((u - d) * Rf)
check("L06 Ex1.5 Delta", Delta, F(1, 2))
check("L06 Ex1.5 B", B, F(-20))
check("L06 Ex1.5 V0", Delta * 100 + B, F(30))
check("L06 Ex1.5 V0 via q", (q * V1u + (1 - q) * V1d) / Rf, F(30))
check("L06 Ex1.6 cash today", F(35) - 50 + 20, F(5))
check("L06 Ex1.6 payoff", F(5) * Rf, F(25, 4))
check("L06 Ex1.6 up state", F(1, 2) * 150 - 25, F(50))
# Example 3.4 two-period tree
V11 = (q * 125) / Rf
V10 = F(0)
V00 = (q * V11 + (1 - q) * V10) / Rf
check("L06 Ex3.4 V(1,1)", V11, 75)
check("L06 Ex3.4 V(0,0)", V00, 45)
check("L06 Ex3.4 closed form", Rf ** -2 * (q**2) * 125, 45)
check("L06 Ex3.4 E^Q[S2]", q**2 * 225 + 2 * q * (1 - q) * 75 + (1 - q) ** 2 * 25, F(625, 4))
check("L06 Ex3.4 E^Q[S2]/Rf^2 = S0", (q**2 * 225 + 2 * q * (1 - q) * 75 + (1 - q) ** 2 * 25) / Rf**2, 100)
check("L06 misc payoff at 156.25", max(F(625, 4) - 100, 0), F(225, 4))
check("L06 misc discounted", F(225, 4) * F(16, 25), 36)
check("L06 misc expected payoff 1125/16", q**2 * 125, F(1125, 16))
# M1 u=2, d=1/2
q1 = (Rf - d) / (2 - d)
check("L06 M1 q", q1, F(1, 2))
check("L06 M1 V0", (q1 * 100) / Rf, 40)
check("L06 M2 Delta", F(100) / ((2 - d) * 100), F(2, 3))
check("L06 M2 B", (2 * 0 - d * 100) / ((2 - d) * Rf), F(-80, 3))
check("L06 M3 S(2,2)", 100 * 2 * 2, 400)
check("L06 M3 V(1,1)", (F(1, 2) * 300) / Rf, 120)
check("L06 M3 V(0,0)", (F(1, 2) * 120) / Rf, 48)
# E2 scaling
check("L06 E2 V0 at spot 200 strike 200", ((q * 100) / Rf) if False else (q * max(F(300) - 200, 0)) / Rf, 60)
# E3 quote 28
check("L06 E3 cash flows", -28 + (50 - 20) - 2, 0)
check("L06 E3 payoff up", F(50) - F(75) + F(25) + F(5, 2), F(5, 2))
check("L06 E3 payoff down", F(0) - F(25) + F(25) + F(5, 2), F(5, 2))
# R1 claim payoff 50,0,-50 with Delta=1, R_f B=-100
check("L06 R1 replication", [150 - F(100), 100 - F(100), 50 - F(100)], [50, 0, -50])
# R2 R_f=1
check("L06 R2 q", (1 - d) / (u - d), F(1, 2))
check("L06 R2 V0", (F(1, 2) * 50) / 1, 25)
check("L06 R2 B", (u * 0 - d * 50) / (u - d), -25)
# Theorem 1.4(b) closed form identity check on random inputs
import random
rng = random.Random(0)
okk = True
for _ in range(200):
    uu = F(rng.randint(11, 30), 10); dd = F(rng.randint(1, 9), 10); rr = F(rng.randint(int(dd * 100) + 1, int(uu * 100) - 1), 100)
    v1u, v1d = F(rng.randint(0, 200)), F(rng.randint(0, 200))
    Dl = (v1u - v1d) / ((uu - dd)); Bb = (uu * v1d - dd * v1u) / ((uu - dd) * rr)
    V = Dl + Bb
    qq = (rr - dd) / (uu - dd)
    if V != (qq * v1u + (1 - qq) * v1d) / rr or not (0 < qq < 1):
        okk = False
check("Theorem 1.4 (b) identity on 200 random exact parameter sets", okk, True)
# Theorem 3.3 closed form vs backward induction, N = 4, random payoff
okk = True
for _ in range(20):
    N = 4
    uu, dd, rr = F(3, 2), F(1, 2), F(5, 4)
    qq = (rr - dd) / (uu - dd)
    f = [F(rng.randint(0, 50)) for _ in range(N + 1)]
    V = {(N, k): f[k] for k in range(N + 1)}
    for n in range(N - 1, -1, -1):
        for k in range(n + 1):
            V[(n, k)] = (qq * V[(n + 1, k + 1)] + (1 - qq) * V[(n + 1, k)]) / rr
    closed = sum(math.comb(N, k) * qq**k * (1 - qq) ** (N - k) * f[k] for k in range(N + 1)) / rr**N
    if closed != V[(0, 0)]:
        okk = False
check("Theorem 3.3 closed form equals backward induction (N=4, 20 random payoffs)", okk, True)

print("\n".join(out))
print("ALL OK" if all(x.startswith("OK") for x in out) else "SOME BAD")
