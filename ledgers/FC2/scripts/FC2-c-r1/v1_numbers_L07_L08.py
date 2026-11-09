"""Independent recomputation of every number in FC2 L07 and L08 prose, labs, quiz and problems.

Round 1 verifier script for slice c (L07-L08). Standard library only. Run:
    .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r1/v1_numbers_L07_L08.py
Every printed line is a number the verifier compares with the page text.
"""

from __future__ import annotations

import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50


def Phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def phi(x: float) -> float:
    return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)


def d_terms(S: float, K: float, r: float, tau: float, sig: float) -> tuple[float, float]:
    s = sig * math.sqrt(tau)
    d1 = (math.log(S / K) + (r + sig * sig / 2.0) * tau) / s
    return d1, d1 - s


def bs_call(S: float, K: float, r: float, tau: float, sig: float) -> float:
    d1, d2 = d_terms(S, K, r, tau, sig)
    return S * Phi(d1) - K * math.exp(-r * tau) * Phi(d2)


def bs_put(S: float, K: float, r: float, tau: float, sig: float) -> float:
    d1, d2 = d_terms(S, K, r, tau, sig)
    return K * math.exp(-r * tau) * Phi(-d2) - S * Phi(-d1)


def tree_sum(S: float, K: float, r: float, tau: float, sig: float, n: int) -> float:
    """Theorem 2.3 closed sum, independent of the lab's backward induction."""
    h = tau / n
    u = math.exp(sig * math.sqrt(h))
    d = 1.0 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    total = 0.0
    for k in range(n + 1):
        payoff = max(S * u**k * d ** (n - k) - K, 0.0)
        total += math.comb(n, k) * q**k * (1 - q) ** (n - k) * payoff
    return math.exp(-r * tau) * total


def tree_backward(S: float, K: float, r: float, tau: float, sig: float, n: int) -> float:
    h = tau / n
    u = math.exp(sig * math.sqrt(h))
    d = 1.0 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    vals = [max(S * u**j * d ** (n - j) - K, 0.0) for j in range(n + 1)]
    for _ in range(n):
        vals = [(q * vals[j + 1] + (1 - q) * vals[j]) / R for j in range(len(vals) - 1)]
    return vals[0]


def half_up_cents(x: float) -> int:
    return math.floor(x * 100 + 0.5) if x >= 0 else -math.floor(-x * 100 + 0.5)


def main() -> None:
    S, K, r, tau, sig = 100.0, 100.0, 0.05, 1.0, 0.20
    d1, d2 = d_terms(S, K, r, tau, sig)
    C = bs_call(S, K, r, tau, sig)
    P = bs_put(S, K, r, tau, sig)
    print(f"L07 d1={d1:.9f} d2={d2:.9f} Phi(d1)={Phi(d1):.9f} Phi(d2)={Phi(d2):.9f}")
    print(f"L07 C={C:.9f} cents={C * 100:.6f}")
    print(f"L07 M2 K e^-rt={K * math.exp(-r * tau):.9f} P(parity)={C - S + K * math.exp(-r * tau):.9f} P(formula)={P:.9f}")
    print(f"L07 P cents={C * 100 - 10000 + K * math.exp(-r * tau) * 100:.6f}")
    print(f"L07 Phi(x)+Phi(-x)-1 at 0,0.35,1.7,3.0: {[Phi(x) + Phi(-x) - 1 for x in (0.0, 0.35, 1.7, 3.0)]}")
    print(f"L07 parity residual vs put formula: {(C - S + K * math.exp(-r * tau)) - P:.3e}")

    steps = (1, 2, 5, 10, 25, 50, 100, 200, 400)
    errs = {}
    print("L07 steps: tree(unrounded) tree_cents err_unrounded err_cents  | closed-sum check")
    for n in steps:
        V = tree_backward(S, K, r, tau, sig, n)
        Vs = tree_sum(S, K, r, tau, sig, n)
        e = V - C
        errs[n] = e
        print(
            f"  n={n:>3} V={V:.9f} Vcents={V * 100:.6f} rounded={half_up_cents(V)} "
            f"err_cents={e * 100:+.6f} err_rounded={half_up_cents(e)} "
            f"|backward-sum|={abs(V - Vs):.2e}"
        )
    signs = [(n, "+" if errs[n] > 0 else "-") for n in steps]
    changes = sum(1 for a, b in zip(signs, signs[1:]) if a[1] != b[1])
    print(f"L07 sign pattern (unrounded): {signs}; sign changes = {changes}")
    absolute = [abs(errs[n]) for n in steps]
    print(f"L07 |error| monotone decreasing along list: {all(a > b for a, b in zip(absolute, absolute[1:]))}")
    print(f"L07 smallest |error| step: {min(steps, key=lambda n: abs(errs[n]))}")
    print(f"L07 err(400) unrounded currency={errs[400]:.7f} cents={errs[400] * 100:.5f}")
    print(f"L07 err(200) unrounded cents={errs[200] * 100:.5f}")
    for n in (1, 5, 25, 2, 10, 50, 100, 200, 400):
        print(f"L07 E2 unrounded cents n={n}: {errs[n] * 100:.4f}")
    rounded_closed = half_up_cents(C)
    print(f"L07 printed closed cents={rounded_closed}")

    # E3: one-step tree by hand
    u1, d1s, R1 = math.exp(0.2), math.exp(-0.2), math.exp(0.05)
    q1 = (R1 - d1s) / (u1 - d1s)
    up_payoff = 100 * u1 - 100
    V1 = math.exp(-0.05) * q1 * up_payoff
    print(f"L07 E3 u1={u1:.7f} d1={d1s:.7f} R1={R1:.7f} q1={q1:.7f} payoff={up_payoff:.6f} V1={V1:.7f} V1cents={V1 * 100:.5f}")
    print(f"L07 E3 solution q1 printed 0.577493 vs {q1:.7f}; V1 printed 12.1623 vs {V1:.7f}")

    # M3: four steps
    h4 = 0.25
    u4 = math.exp(0.2 * math.sqrt(h4))
    d4 = 1 / u4
    R4 = math.exp(0.05 * h4)
    q4 = (R4 - d4) / (u4 - d4)
    print(f"L07 M3 u4={u4:.7f} d4={d4:.7f} R4={R4:.7f} q4={q4:.7f} sigma*sqrt(h)={0.2 * math.sqrt(h4)} sigma^2/r^2={0.04 / 0.0025}")

    # R2: alternative inputs with same r*tau and sigma*sqrt(tau)
    C_alt = bs_call(100.0, 100.0, 0.0125, 4.0, 0.1)
    print(f"L07 R2 alt call={C_alt:.9f} sigma*sqrt(tau)={0.1 * math.sqrt(4):.6f} r*tau={0.0125 * 4:.6f}")

    # Lemma 1.2 / 1.1 numeric check at a few points
    for x in (-2.0, -0.5, 0.0, 1.3):
        assert abs(Phi(x) - 0.5 * (1 + math.erf(x / math.sqrt(2)))) < 1e-15

    # Prop 1.5: C depends on S,K,r*tau,sigma*sqrt(tau) only.
    C_scaled = bs_call(200.0, 200.0, 0.05, 1.0, 0.2)
    print(f"L07 Prop1.5 scale check: C(200,200)={C_scaled:.9f} vs C(100,100)={C:.9f}")

    # Lab-claim: mu does not enter (no mu parameter in bs_call) — structural, see script text.

    print("---- L08 ----")
    print(f"L08 lower bound K=100 exact={100 - 100 * math.exp(-0.05):.9f} cents={(100 - 100 * math.exp(-0.05)) * 100:.5f}")
    print(f"L08 lower bound K=120 = {max(100 - 120 * math.exp(-0.05), 0.0):.9f}; 120e^-0.05={120 * math.exp(-0.05):.6f}")
    vega = S * phi(d1) * math.sqrt(tau)
    print(f"L08 vega(sig=0.2,K=100)={vega:.7f} 100*phi(0.35)={100 * phi(0.35):.7f} phi(d1)={phi(d1):.7f}")
    print(f"L08 R2 dsigma (displayed vega 37.52)={0.01 / 37.52:.7f}; unrounded vega={0.01 / vega:.7f}")

    # Lemma 2.1 numeric check via finite difference
    for Kx in (80.0, 100.0, 120.0):
        for sg in (0.05, 0.1, 0.2, 0.4):
            fd = (bs_call(100, Kx, r, tau, sg + 1e-6) - bs_call(100, Kx, r, tau, sg - 1e-6)) / 2e-6
            d1x, _ = d_terms(100, Kx, r, tau, sg)
            an = 100 * phi(d1x) * math.sqrt(tau)
            assert abs(fd - an) < 1e-5, (Kx, sg, fd, an)
    print("L08 Lemma 2.1 finite-difference check: passed for K in {80,100,120}, sigma in {0.05,0.1,0.2,0.4}")

    # Lab rows: price cents, unrounded and recovered
    LOW, HIGH, TOL = 1e-6, 10.0, 1e-10
    cases = [(80.0, 0.10), (80.0, 0.20), (80.0, 0.40), (100.0, 0.10), (100.0, 0.20), (100.0, 0.40), (120.0, 0.10), (120.0, 0.20), (120.0, 0.40)]

    def invert(price: float, Kx: float) -> tuple[float, int]:
        low, high = LOW, HIGH
        n = 0
        while high - low > TOL:
            mid = (low + high) / 2
            if bs_call(100.0, Kx, 0.05, 1.0, mid) - price < 0:
                low = mid
            else:
                high = mid
            n += 1
        return (low + high) / 2, n

    for Kx, st in cases:
        price = bs_call(100.0, Kx, 0.05, 1.0, st)
        sh, n = invert(price, Kx)
        print(f"L08 row K={Kx:.0f} sig={st:.2f} price={price:.9f} cents={half_up_cents(price)} recovered={sh:.10f} halvings={n} abs_err={abs(sh - st):.3e}")

    W = HIGH - LOW
    print(f"L08 M3 W={W:.9f} log2(W/tol)={math.log2(W / TOL):.5f} W/2^36={W / 2**36:.4e} W/2^37={W / 2**37:.4e}")
    print(f"L08 M3 10/2^36={10 / 2**36:.4e}")

    # E2: K=120, sig=0.10 unrounded cents
    p120 = bs_call(100.0, 120.0, 0.05, 1.0, 0.10)
    print(f"L08 E2 K=120 sig=0.10 price={p120:.7f} currency cents={p120 * 100:.4f}; 120e^-0.05={120 * math.exp(-0.05):.4f}")

    # E3: price 0.50 at K=120
    p = 0.50
    print(f"L08 E3 C(1e-6)={bs_call(100.0, 120.0, 0.05, 1.0, LOW):.3e} C(10)={bs_call(100.0, 120.0, 0.05, 1.0, HIGH):.7f}")
    v, n = invert(p, 120.0)
    print(f"L08 E3 implied vol for 0.50 at K=120: {v:.6f} halvings={n} residual={bs_call(100.0, 120.0, 0.05, 1.0, v) - p:.3e}")

    # Probe: price between bounds rejected by bracket (too close to spot)
    near = bs_call(100.0, 100.0, 0.05, 1.0, HIGH)
    print(f"L08 C(K=100, sig=10)={near:.9f}; prices in (C(10), 100) have a volatility above 10 and are rejected by the bracket")

    # Theorem 2.3 monotonicity and limits numerically
    vals = [bs_call(100.0, 100.0, 0.05, 1.0, s) for s in (1e-3, 1e-2, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0)]
    print(f"L08 monotone in sigma: {all(a < b for a, b in zip(vals, vals[1:]))} values={[round(v, 6) for v in vals]}")
    for Kx in (80.0, 100.0, 120.0):
        L = max(100 - Kx * math.exp(-0.05), 0.0)
        lo = bs_call(100.0, Kx, 0.05, 1.0, 1e-6)
        hi = bs_call(100.0, Kx, 0.05, 1.0, 1e3)
        print(f"L08 limits K={Kx:.0f}: C(1e-6)={lo:.9f} L={L:.9f} C(1e3)={hi:.9f} S=100")


if __name__ == "__main__":
    main()
