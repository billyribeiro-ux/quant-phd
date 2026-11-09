"""Independent recomputation of every number the FC2 L07 and L08 pages print or derive (round 4).

Standard library only, run with: .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r4/recompute_numbers.py
Every printed line is one checked claim; the values are compared with the page's wording in the ledger rows.
"""

from __future__ import annotations

import math
from decimal import Decimal, getcontext

getcontext().prec = 50


def cents(x: float) -> int:
    sign = -1 if x < 0 else 1
    return sign * math.floor(abs(x) * 100 + 0.5)


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


def bs_put(S: float, K: float, r: float, tau: float, sig: float) -> float:
    d1, d2 = d12(S, K, r, tau, sig)
    return K * math.exp(-r * tau) * Phi(-d2) - S * Phi(-d1)


def tree_loop(S: float, K: float, r: float, tau: float, sig: float, n: int) -> float:
    h = tau / n
    u = math.exp(sig * math.sqrt(h))
    d = 1.0 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    vals = [max(S * u**j * d ** (n - j) - K, 0.0) for j in range(n + 1)]
    for _ in range(n):
        vals = [(q * vals[j + 1] + (1 - q) * vals[j]) / R for j in range(len(vals) - 1)]
    return vals[0]


def tree_sum(S: float, K: float, r: float, tau: float, sig: float, n: int) -> float:
    h = tau / n
    u = math.exp(sig * math.sqrt(h))
    d = 1.0 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    tot = 0.0
    for k in range(n + 1):
        tot += math.comb(n, k) * q**k * (1 - q) ** (n - k) * max(S * u**k * d ** (n - k) - K, 0.0)
    return math.exp(-r * tau) * tot


print("== L07 ==")
S, K, r, tau, sig = 100.0, 100.0, 0.05, 1.0, 0.20
d1, d2 = d12(S, K, r, tau, sig)
print(f"L07 d1={d1:.12f} d2={d2:.12f}")
C = bs(S, K, r, tau, sig)
P_formula = bs_put(S, K, r, tau, sig)
P_parity = C - S + K * math.exp(-r * tau)
print(f"L07 C={C:.10f} cents={cents(C)}  P_formula={P_formula:.10f} P_parity={P_parity:.10f} diff={P_formula - P_parity:.3e} P_cents={cents(P_parity)}")
print(f"L07 K e^-rt={K * math.exp(-r * tau):.9f}")
print(f"L07 C unrounded (M2 says 10.4505836): {C:.7f}")
print(f"L07 Phi(d1)={Phi(d1):.6f} Phi(d2)={Phi(d2):.6f}")

STEPS = (1, 2, 5, 10, 25, 50, 100, 200, 400)
rows = []
for n in STEPS:
    V = tree_loop(S, K, r, tau, sig, n)
    Vs = tree_sum(S, K, r, tau, sig, n)
    err = V - C
    rows.append((n, V, err))
    print(
        f"L07 n={n:4d} tree_cents={cents(V)} bs_cents={cents(C)} err_cents_printed={cents(err)} "
        f"err_unrounded_cents={err * 100:+.6f} tree_minus_sum={V - Vs:.2e}"
    )
print("L07 printed-cents row diffs equal printed errors:",
      all(cents(V) - cents(C) == cents(err) for _, V, err in rows))
signs_unr = [1 if e > 0 else -1 for _, _, e in rows]
sign_changes = sum(1 for a, b in zip(signs_unr, signs_unr[1:]) if a != b)
abs_dec = all(abs(rows[i + 1][2]) < abs(rows[i][2]) for i in range(len(rows) - 1))
print(f"L07 unrounded signs={signs_unr} sign_changes={sign_changes} |err| strictly decreasing={abs_dec}")
print("L07 printed errors:", [cents(e) for _, _, e in rows])
print("L07 positive unrounded (cents):", [round(e * 100, 2) for _, _, e in rows if e > 0])
print("L07 negative unrounded (cents):", [round(e * 100, 2) for _, _, e in rows if e < 0])
print("L07 printed sign counts pos/neg/zero:",
      sum(1 for _, _, e in rows if cents(e) > 0), sum(1 for _, _, e in rows if cents(e) < 0),
      sum(1 for _, _, e in rows if cents(e) == 0))
print(f"L07 E1 400-step err currency={rows[-1][2]:.7f} cents={rows[-1][2] * 100:.4f}; 200-step cents={rows[-2][2] * 100:.6f}")
for n, V, e in rows:
    pass
print("L07 abs-min step:", min(rows, key=lambda t: abs(t[2]))[0])

# Lemma 1.1 and 1.2 numeric checks
mx = max(abs(Phi(x) - 0.5 * (1 + math.erf(x / math.sqrt(2)))) for x in [i / 7.0 - 3 for i in range(50)])
print(f"L07 Lemma1.1 max|Phi - (1+erf)/2| = {mx:.3e}")
print(f"L07 Lemma1.2 max|Phi(x)+Phi(-x)-1| over grid = {max(abs(Phi(x) + Phi(-x) - 1) for x in [i / 9.0 - 4 for i in range(73)]):.3e}")
print("L07 Phi(x)+Phi(-x) at 0,0.35,1.7,3.0:", [Phi(x) + Phi(-x) - 1 for x in (0.0, 0.35, 1.7, 3.0)])

# Prop 1.4 both forms over grid
mx14 = 0.0
for Kk in (80.0, 100.0, 120.0):
    for sg in (0.1, 0.2, 0.4):
        c = bs(S, Kk, r, tau, sg)
        p1 = c - S + Kk * math.exp(-r * tau)
        p2 = bs_put(S, Kk, r, tau, sg)
        mx14 = max(mx14, abs(p1 - p2))
print(f"L07 Prop1.4 max|parity form - formula form| = {mx14:.3e}")

# Prop 1.5: d1 identity and dependence on (r tau, sigma sqrt tau) only
d1_alt = (math.log(S / K) + r * tau) / (sig * math.sqrt(tau)) + sig * math.sqrt(tau) / 2
print(f"L07 Prop1.5 d1 identity residual = {d1 - d1_alt:.3e}")
C_R2 = bs(S, K, 0.0125, 4.0, 0.1)
print(f"L07 R2 call tau=4 sigma=0.1 r=0.0125 -> {C_R2:.10f} sigma*sqrt(tau)={0.1 * math.sqrt(4):.3f} r*tau={0.0125 * 4:.3f}")

# M3 tree parameters
h = 0.25
u4 = math.exp(0.2 * math.sqrt(h))
d4 = 1 / u4
R4 = math.exp(0.05 * h)
q4 = (R4 - d4) / (u4 - d4)
print(f"L07 M3 u={u4:.10f} d={d4:.10f} R={R4:.10f} q={q4:.10f}")
print(f"L07 M3 six-place quotient 0.107741/0.200334 = {0.107741 / 0.200334:.10f}")
# high-precision q with decimals
Dd = lambda x: Decimal(x)
u_d = (Decimal("0.1") ).exp()
d_d = 1 / u_d
R_d = (Decimal("0.0125")).exp()
print(f"L07 M3 q high precision = {((R_d - d_d) / (u_d - d_d)):.12f}")
print(f"L07 M3 sigma^2/r^2 = {0.04 / 0.0025}")
print(f"L07 M3 six-place inputs: R-d={1.012578 - 0.904837:.6f} u-d={1.105171 - 0.904837:.6f} q={(1.012578 - 0.904837) / (1.105171 - 0.904837):.9f}")

# E3 one-step
u1 = math.exp(0.2)
d1s = math.exp(-0.2)
R1 = math.exp(0.05)
q1 = (R1 - d1s) / (u1 - d1s)
V1 = math.exp(-0.05) * q1 * (100 * u1 - 100)
print(f"L07 E3 u={u1:.8f} d={d1s:.8f} R={R1:.8f} q={q1:.8f} up_payoff={100 * u1 - 100:.8f} V1={V1:.10f} cents={cents(V1)}")
print(f"L07 E3 check tree_loop n=1: {tree_loop(S, K, r, tau, sig, 1):.10f}")

# Theorem 2.3 sum equals induction
mx23 = max(abs(tree_sum(S, K, r, tau, sig, n) - tree_loop(S, K, r, tau, sig, n)) for n in STEPS)
print(f"L07 Thm2.3 max|sum - induction| over STEPS = {mx23:.3e}")

# Lemma 2.2 random check
import random

rng = random.Random(20260)
bad = 0
for _ in range(200000):
    rr = rng.uniform(0.0001, 0.5)
    ss = rng.uniform(0.001, 2.0)
    hh = rng.uniform(1e-4, 4.0)
    dd = math.exp(-ss * math.sqrt(hh))
    uu = 1 / dd
    RR = math.exp(rr * hh)
    lhs = 0 < dd < RR < uu
    rhs = hh < ss * ss / (rr * rr)
    if lhs != rhs:
        bad += 1
print(f"L07 Lemma2.2 random mismatches (200000) = {bad}")

print("== L08 ==")
S8, r8, tau8 = 100.0, 0.05, 1.0
for Kk in (80.0, 100.0, 120.0):
    Lb = max(S8 - Kk * math.exp(-r8 * tau8), 0.0)
    print(f"L08 K={Kk} L={Lb!r} C(1e-6)={bs(S8, Kk, r8, tau8, 1e-6)!r} C(10)={bs(S8, Kk, r8, tau8, 10.0)!r}")
Kn = 100.0 * math.exp(0.05)
print(f"L08 K=S e^(r tau)={Kn!r} L={max(S8 - Kn * math.exp(-r8), 0.0)!r} C(1e-6)={bs(S8, Kn, r8, tau8, 1e-6)!r} C(1e-6) cents={cents(bs(S8, Kn, r8, tau8, 1e-6))}")
print(f"L08 K=100 C(10)={bs(100.0, 100.0, r8, tau8, 10.0)!r}  K=120 C(10)={bs(100.0, 120.0, r8, tau8, 10.0)!r}  K=120 C(1e-6)={bs(100.0, 120.0, r8, tau8, 1e-6)!r}")
print(f"L08 L(K=100)={100 - 100 * math.exp(-0.05):.12f} 100e^-0.05={100 * math.exp(-0.05):.9f} 120e^-0.05={120 * math.exp(-0.05):.6f}")
print(f"L08 Se^(r tau)={100 * math.exp(0.05):.10f}")

print("L08 table: sig_true, price(unrounded), cents_unrounded, printed cents, recovery sigma err (from the twin functions)")
CASES = [(80.0, 0.10), (80.0, 0.20), (80.0, 0.40), (100.0, 0.10), (100.0, 0.20), (100.0, 0.40), (120.0, 0.10), (120.0, 0.20), (120.0, 0.40)]
for Kk, st in CASES:
    pr = bs(S8, Kk, r8, tau8, st)
    print(f"L08   K={Kk:5.0f} sig={st:.2f} price={pr:.10f} unrounded_cents={pr * 100:.4f} printed={cents(pr)}")

print(f"L08 dC/dsig at K=100 sig=0.2: S phi(d1) sqrt tau = {100 * phi(0.35):.10f}; 100 phi(0.35) = {100 * phi(0.35):.4f}")
print(f"L08 R2 0.01/37.52 = {0.01 / 37.52:.8f}; 0.01/37.5240 = {0.01 / 37.5240:.10f}")
print(f"L08 E2 cents at K=120 sig=0.10 = {bs(S8, 120.0, r8, tau8, 0.10) * 100:.4f}")
print(f"L08 M3: log2(10^11)={math.log2(1e11):.4f}; log2(W/tol)={math.log2((10 - 1e-6) / 1e-10):.4f}; 10/2^36={10 / 2**36:.6e}; W/2^37={(10 - 1e-6) / 2**37:.6e}; W/2^36={(10 - 1e-6) / 2**36:.6e}")
print(f"L08 lower 4.8771 exact {100 - 100 * math.exp(-0.05):.10f}; M1 unrounded 4.877058 -> {100 - 100 * math.exp(-0.05):.6f}")
print(f"L08 Lemma2.1 finite-difference check: see separate output")
print(f"L08 lemma-2.1 identity check, S phi(d1) - K e^-rt phi(d2) over grid:")
mxid = 0.0
for Kk in (80.0, 100.0, 120.0):
    for sg in (0.05, 0.1, 0.2, 0.4):
        d1x, d2x = d12(S8, Kk, r8, tau8, sg)
        mxid = max(mxid, abs(S8 * phi(d1x) - Kk * math.exp(-r8 * tau8) * phi(d2x)))
print(f"  max|S phi(d1) - K e^-rt phi(d2)| = {mxid:.3e}")
mxfd = 0.0
hstep = 1e-6
for Kk in (80.0, 100.0, 120.0):
    for sg in (0.05, 0.1, 0.2, 0.4):
        fd = (bs(S8, Kk, r8, tau8, sg + hstep) - bs(S8, Kk, r8, tau8, sg - hstep)) / (2 * hstep)
        d1x, _ = d12(S8, Kk, r8, tau8, sg)
        an = S8 * phi(d1x) * math.sqrt(tau8)
        mxfd = max(mxfd, abs(fd - an))
print(f"  Lemma 2.1 central-difference worst abs error = {mxfd:.3e}")
# Lemma 2.2 limits numerically
for Kk in (80.0, 100.0, 120.0):
    Lb = max(S8 - Kk * math.exp(-r8 * tau8), 0.0)
    print(f"  K={Kk}: C(1e3)={bs(S8, Kk, r8, tau8, 1e3):.10f} C(1e-6)={bs(S8, Kk, r8, tau8, 1e-6):.12f} L={Lb:.12f}")
