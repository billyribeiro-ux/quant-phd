"""Independent recomputation of every number in FC2 L07 and L08 (verifier round 3, slice c).

Uses only the standard library. Does not import the lab twins.
Prints every quantity the lessons state, unrounded, for comparison with the prose.
"""
from __future__ import annotations

import math
from fractions import Fraction


def Phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def phi(x: float) -> float:
    return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)


def d12(S: float, K: float, r: float, tau: float, sig: float) -> tuple[float, float]:
    s = sig * math.sqrt(tau)
    d1 = (math.log(S / K) + (r + sig * sig / 2.0) * tau) / s
    return d1, d1 - s


def bs(S: float, K: float, r: float, tau: float, sig: float) -> float:
    d1, d2 = d12(S, K, r, tau, sig)
    return S * Phi(d1) - K * math.exp(-r * tau) * Phi(d2)


def tree_bi(S: float, K: float, r: float, tau: float, sig: float, n: int) -> float:
    h = tau / n
    u = math.exp(sig * math.sqrt(h))
    d = 1 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    # Theorem 2.3 closed sum
    s = 0.0
    for k in range(n + 1):
        s += math.comb(n, k) * q**k * (1 - q) ** (n - k) * max(S * u**k * d ** (n - k) - K, 0.0)
    return math.exp(-r * tau) * s


def tree_bi_induction(S: float, K: float, r: float, tau: float, sig: float, n: int) -> float:
    h = tau / n
    u = math.exp(sig * math.sqrt(h))
    d = 1 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    vals = [max(S * u**j * d ** (n - j) - K, 0.0) for j in range(n + 1)]
    for _ in range(n):
        vals = [(q * vals[j + 1] + (1 - q) * vals[j]) / R for j in range(len(vals) - 1)]
    return vals[0]


print("=== L07 numbers")
S, K, r, tau, sig = 100.0, 100.0, 0.05, 1.0, 0.2
C = bs(S, K, r, tau, sig)
print(f"C unrounded = {C:.7f}  cents = {C*100:.4f}")
d1, d2 = d12(S, K, r, tau, sig)
print(f"d1={d1:.7f} d2={d2:.7f} Phi(d1)={Phi(d1):.7f} Phi(d2)={Phi(d2):.7f}")
Kdf = K * math.exp(-r * tau)
print(f"K e^-r = {Kdf:.7f}")
P = C - S + Kdf
print(f"P from parity = {P:.7f} cents = {P*100:.4f}")
P_formula = Kdf * Phi(-d2) - S * Phi(-d1)
print(f"P second formula = {P_formula:.7f}  diff={P - P_formula:.2e}")
print(f"Phi(x)+Phi(-x)-1 at 0,0.35,1.7,3.0: {[Phi(x)+Phi(-x)-1 for x in (0.0,0.35,1.7,3.0)]}")
print(f"Phi(0.35)={Phi(0.35):.6f} Phi(0.15)={Phi(0.15):.6f}")
steps = (1, 2, 5, 10, 25, 50, 100, 200, 400)
errs = {}
print("n tree_cent_unr  err_unr_cent  printed_round_err")
for n in steps:
    t = tree_bi_induction(S, K, r, tau, sig, n)
    tc = tree_bi(S, K, r, tau, sig, n)
    assert abs(t - tc) < 1e-9, (n, t, tc)
    errs[n] = t - C
    print(f"{n:>4} {t*100:>14.4f} {errs[n]*100:>14.4f}")
signs = [(n, 'pos' if errs[n] > 0 else ('neg' if errs[n] < 0 else 'zero')) for n in steps]
print("signs:", signs)
changes = sum(1 for a, b in zip(signs, signs[1:]) if a[1] != b[1])
print("sign changes across printed list (unrounded):", changes)
ab = [abs(errs[n]) for n in steps]
print("abs error nonincreasing:", all(x >= y for x, y in zip(ab, ab[1:])))
print("400-step error cents:", errs[400] * 100, "; 200-step:", errs[200] * 100)
print("sum of positive-count, negative-count:", sum(errs[n] > 0 for n in steps), sum(errs[n] < 0 for n in steps))

print("\n=== M3 tree parameters, four steps")
h = 0.25
u4, d4, R4 = math.exp(sig * math.sqrt(h)), math.exp(-sig * math.sqrt(h)), math.exp(r * h)
q4 = (R4 - d4) / (u4 - d4)
print(f"u4={u4:.7f} d4={d4:.7f} R4={R4:.7f} q4={q4:.7f}  sigma^2/r^2={sig*sig/(r*r)}")

print("\n=== E3 one-step")
u1, d1s, R1 = math.exp(0.2), math.exp(-0.2), math.exp(0.05)
q1 = (R1 - d1s) / (u1 - d1s)
V1 = math.exp(-0.05) * q1 * (100 * u1 - 100)
print(f"u1={u1:.7f} d1={d1s:.7f} R1={R1:.7f} q1={q1:.7f} V1={V1:.6f} cents={V1*100:.3f}")
print(f"tree_bi n=1: {tree_bi(S,K,r,tau,sig,1):.7f}")

print("\n=== R2 Proposition 1.5 example")
print(f"tau=4 sig=0.1 r=0.0125 call={bs(100,100,0.0125,4.0,0.1):.7f} vs {C:.7f}")

print("\n=== L07 Lemma 2.2 condition check at r>0")
for n in (1, 4, 400):
    h = tau / n
    print(n, 0 < math.exp(-sig*math.sqrt(h)) < math.exp(r*h) < math.exp(sig*math.sqrt(h)), h < sig**2 / r**2)
print("r=0 check of Lemma 2.2 relation not defined (r=0 excluded)")

print("\n=== R-style prices at other inputs (sanity, not in lesson)")
print("tau=1 sig=0.2 S=100 K=100 Phi(0.35) x 100 =", 100*phi(0.35))

print("\n=== L08 numbers")
L = max(S - K * math.exp(-r * tau), 0.0)
print(f"L(K=100) unrounded={L:.6f}")
print(f"L(K=120)={max(100 - 120*math.exp(-r*tau),0.0)}; 120e^-0.05={120*math.exp(-r*tau):.5f}")
print(f"100e^-0.05={100*math.exp(-0.05):.6f}")
for K2 in (80.0, 100.0, 120.0):
    for sg in (0.10, 0.20, 0.40):
        print(f"K={K2} sig={sg} C={bs(100.0,K2,0.05,1.0,sg):.8f} cents={bs(100.0,K2,0.05,1.0,sg)*100:.4f}")
print(f"K=120 sig=0.10 cents unrounded = {bs(100.0,120.0,0.05,1.0,0.10)*100:.4f}")
vega = 100 * phi(0.35) * 1.0
print(f"vega at sigma=0.2, K=100: {vega:.6f}  (displayed 37.52)")
print(f"one-cent change dsig = 0.01/vega = {0.01/vega:.7f}; with 37.52 displayed: {0.01/37.52:.7f}; in vol points (x100): {0.01/37.52*100:.5f}")
print(f"  with 37.5240: {0.01/37.5240:.7f} ; points {0.01/37.5240*100:.5f}")
print("halvings: width =", 10 - 1e-6, " log2(W/tol) =", math.log2((10 - 1e-6) / 1e-10))
k = 0
w = 10.0 - 1e-6
while w > 1e-10:
    w /= 2
    k += 1
print("halvings by width loop (no price):", k)
print("width after 36 halvings:", (10 - 1e-6) / 2**36)
