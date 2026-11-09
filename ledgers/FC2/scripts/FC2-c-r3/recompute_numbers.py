"""Verifier recomputation (FC2 slice c, round 3) of every number in L07.html and L08.html.

Independent of the twins: written from the definitions on the pages. Double precision via math and scipy.special.
Run: .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r3/recompute_numbers.py
"""

from __future__ import annotations

import math
import random

from scipy.special import ndtr, ndtri

SQ2 = math.sqrt(2.0)


def Phi(x: float) -> float:
    return float(ndtr(x))


def phi(x: float) -> float:
    return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)


def cents_half_up(x: float) -> int:
    return math.floor(x * 100 + 0.5)


def cents_away(x: float) -> int:
    s = -1 if x < 0 else 1
    return s * math.floor(abs(x) * 100 + 0.5)


def d_terms(S: float, K: float, r: float, tau: float, sig: float) -> tuple[float, float]:
    root = sig * math.sqrt(tau)
    d1 = (math.log(S / K) + (r + sig * sig / 2) * tau) / root
    return d1, d1 - root


def bs_call(S: float, K: float, r: float, tau: float, sig: float) -> float:
    d1, d2 = d_terms(S, K, r, tau, sig)
    return S * Phi(d1) - K * math.exp(-r * tau) * Phi(d2)


def bs_put(S: float, K: float, r: float, tau: float, sig: float) -> float:
    d1, d2 = d_terms(S, K, r, tau, sig)
    return K * math.exp(-r * tau) * Phi(-d2) - S * Phi(-d1)


def tree_call(S: float, K: float, r: float, tau: float, sig: float, n: int) -> float:
    h = tau / n
    u = math.exp(sig * math.sqrt(h))
    d = 1.0 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    # explicit sum (Theorem 2.3) and backward induction, both
    explicit = 0.0
    for k in range(n + 1):
        payoff = max(S * u**k * d ** (n - k) - K, 0.0)
        explicit += math.comb(n, k) * q**k * (1 - q) ** (n - k) * payoff
    explicit *= math.exp(-r * tau)
    vals = [max(S * u**j * d ** (n - j) - K, 0.0) for j in range(n + 1)]
    for _ in range(n):
        vals = [(q * vals[j + 1] + (1 - q) * vals[j]) / R for j in range(len(vals) - 1)]
    assert abs(explicit - vals[0]) < 1e-9, (n, explicit, vals[0])
    return vals[0]


def main() -> None:
    out: list[str] = []

    def p(*a: object) -> None:
        out.append(" ".join(str(x) for x in a))

    # ---- L07 ----
    S, K, r, tau, sig = 100.0, 100.0, 0.05, 1.0, 0.20
    d1, d2 = d_terms(S, K, r, tau, sig)
    C = bs_call(S, K, r, tau, sig)
    P = bs_put(S, K, r, tau, sig)
    p("L07 d1", f"{d1:.9f}", "d2", f"{d2:.9f}", "Phi(d1)", f"{Phi(d1):.6f}", "Phi(d2)", f"{Phi(d2):.6f}")
    p("L07 C unrounded", f"{C:.10f}", "cents", cents_half_up(C))
    p("L07 K e^-rt", f"{K*math.exp(-r*tau):.9f}")
    p("L07 P (formula)", f"{P:.10f}", "P (parity)", f"{C - S + K*math.exp(-r*tau):.10f}", "P cents", cents_half_up(P))
    p("L07 parity-put diff", abs(P - (C - S + K * math.exp(-r * tau))))
    steps = (1, 2, 5, 10, 25, 50, 100, 200, 400)
    errs = []
    tot = []
    for n in steps:
        t = tree_call(S, K, r, tau, sig, n)
        e = t - C
        errs.append(e)
        tot.append(t)
        p(f"L07 n={n:>3} tree_unrounded={t:.6f} tree_cents={cents_half_up(t)} "
          f"err_unrounded_cents={e*100:.6f} err_printed={cents_away(e)} "
          f"printed_diff={cents_half_up(t)-cents_half_up(C)}")
    signs = [1 if e > 0 else (-1 if e < 0 else 0) for e in errs]
    changes = sum(1 for a, b in zip(signs, signs[1:]) if a != b and a != 0 and b != 0)
    p("L07 sign changes (nonzero):", changes, "signs", signs)
    p("L07 |err| decreasing:", all(abs(errs[i + 1]) < abs(errs[i]) for i in range(len(errs) - 1)))
    p("L07 positive count", sum(1 for e in errs if e > 0), "negative count", sum(1 for e in errs if e < 0))
    p("L07 printed-cents row diffs equal printed errors:",
      all(cents_half_up(t) - cents_half_up(C) == cents_away(e) for t, e in zip(tot, errs)))
    p("L07 errors in cents unrounded:", [round(e * 100, 6) for e in errs])
    p("L07 n=400 error currency", errs[-1], "cents", errs[-1] * 100)
    p("L07 n=200 error cents", errs[-2] * 100)
    # symmetry
    p("L07 Phi(x)+Phi(-x)-1 at 0,0.35,1.7,3.0:", [Phi(x) + Phi(-x) - 1 for x in (0.0, 0.35, 1.7, 3.0)])
    # Lemma 1.1 erf identity
    import scipy.special as sp

    p("L07 Lemma1.1 max |Phi - (1+erf)/2| over points:",
      max(abs(Phi(x) - 0.5 * (1 + math.erf(x / SQ2))) for x in (-3, -1, -0.3, 0, 0.7, 1.9, 2.5)))
    p("L07 scipy erf check", sp.erf(0.5))
    # Prop 1.4 two forms and Prop 1.5 check
    worst = 0.0
    for Kx in (80.0, 100.0, 120.0):
        for sx in (0.1, 0.2, 0.4):
            c = bs_call(S, Kx, r, tau, sx)
            d1x, d2x = d_terms(S, Kx, r, tau, sx)
            f1 = c - S + Kx * math.exp(-r * tau)
            f2 = Kx * math.exp(-r * tau) * Phi(-d2x) - S * Phi(-d1x)
            worst = max(worst, abs(f1 - f2))
    p("L07 Prop1.4 two forms worst diff:", worst)
    p("L07 R2 call tau=4 sig=0.1 r=0.0125:", f"{bs_call(100.0, 100.0, 0.0125, 4.0, 0.1):.10f}",
      "sig*sqrt(tau)", 0.1 * 2, "r*tau", 0.0125 * 4)
    p("L07 Prop1.5 d1 identity (K=100 S=100): d1 vs (ln(S/K)+rt)/(s)+s/2:",
      abs(d1 - ((math.log(S / K) + r * tau) / (sig * math.sqrt(tau)) + sig * math.sqrt(tau) / 2)))
    # M3 tree parameters
    h = 0.25
    u4 = math.exp(0.2 * math.sqrt(h))
    d4 = 1 / u4
    R4 = math.exp(0.05 * h)
    q4 = (R4 - d4) / (u4 - d4)
    p("L07 M3 u4", f"{u4:.10f}", "d4", f"{d4:.10f}", "R4", f"{R4:.10f}", "q4 unrounded", f"{q4:.10f}",
      "q4 rounded6", f"{q4:.6f}")
    p("L07 M3 q4 from six-place printed inputs", f"{(1.012578 - 0.904837) / (1.105171 - 0.904837):.10f}")
    p("L07 M3 q4 from 8-place inputs", f"{(1.01257845 - 0.90483742) / (1.10517092 - 0.90483742):.10f}")
    p("L07 M3 sigma^2/r^2", 0.04 / 0.0025)
    p("L07 M3 e^0.0125", f"{math.exp(0.0125):.8f}", "e^0.1", f"{math.exp(0.1):.8f}")
    # E3 one step
    u1 = math.exp(0.2)
    d1s = 1 / u1
    R1 = math.exp(0.05)
    q1 = (R1 - d1s) / (u1 - d1s)
    V1 = math.exp(-0.05) * q1 * (100 * u1 - 100)
    p("L07 E3 u1", f"{u1:.8f}", "d1", f"{d1s:.8f}", "R1", f"{R1:.8f}", "q1", f"{q1:.8f}", "V1", f"{V1:.10f}",
      "V1 cents", cents_half_up(V1))
    p("L07 E3 up payoff", f"{100*u1-100:.8f}")
    # Lemma 2.2 random check
    rng = random.Random(12345)
    bad = 0
    for _ in range(200000):
        rr = rng.uniform(1e-4, 0.3)
        ss = rng.uniform(1e-3, 1.0)
        hh = 10 ** rng.uniform(-4, 1)
        dd = math.exp(-ss * math.sqrt(hh))
        RR = math.exp(rr * hh)
        uu = math.exp(ss * math.sqrt(hh))
        cond = 0 < dd < RR < uu
        pred = hh < ss * ss / (rr * rr)
        if cond != pred:
            bad += 1
    p("L07 Lemma2.2 random mismatches:", bad, "of 200000")
    # E1/E2 values
    p("L07 E2 unrounded positive:", [round(errs[i] * 100, 2) for i in range(len(errs)) if errs[i] > 0])
    p("L07 E2 unrounded negative:", [round(errs[i] * 100, 2) for i in range(len(errs)) if errs[i] < 0])
    p("L07 R1/M3 log2(10^11)", math.log2(1e11))

    # ---- L08 ----
    S8, r8, tau8 = 100.0, 0.05, 1.0
    Lb = max(S8 - 100.0 * math.exp(-r8 * tau8), 0.0)
    p("L08 L(K=100) unrounded", f"{Lb:.9f}", "100e^-0.05", f"{100*math.exp(-0.05):.6f}")
    for Kx in (80.0, 100.0, 105.12710963760241, 120.0):
        Lk = max(S8 - Kx * math.exp(-r8 * tau8), 0.0)
        c1 = bs_call(S8, Kx, r8, tau8, 1e-6)
        c10 = bs_call(S8, Kx, r8, tau8, 10.0)
        p("L08 K=", f"{Kx:.6f}", "L=", repr(Lk), "C(1e-6)=", repr(c1), "C(10)=", f"{c10:.10f}",
          "C(1e-6)==L", c1 == Lk, "C(1e-6)<=L", c1 <= Lk)
    p("L08 K=120 L", max(S8 - 120 * math.exp(-0.05), 0.0), "120e^-0.05", 120 * math.exp(-0.05))
    p("L08 K=100e^{rt} value", f"{100*math.exp(0.05):.10f}", "S e^{r tau} for K", f"{S8*math.exp(r8*tau8):.10f}")
    p("L08 C(10) at K=100", f"{bs_call(S8, 100.0, r8, tau8, 10.0):.10f}")
    p("L08 C(10) at K=100 vs 99.99995 (price rejected by bracket iff > C(10))",
      99.99995 > bs_call(S8, 100.0, r8, tau8, 10.0))
    # Lab-1 prices and cents
    for Kx, sx in [(80.0, 0.10), (80.0, 0.20), (80.0, 0.40), (100.0, 0.10), (100.0, 0.20), (100.0, 0.40),
                   (120.0, 0.10), (120.0, 0.20), (120.0, 0.40)]:
        pr = bs_call(S8, Kx, r8, tau8, sx)
        p("L08 table K", Kx, "sig", sx, "price unrounded", f"{pr:.8f}", "cents", f"{pr*100:.4f}",
          "printed", cents_half_up(pr))
    # Quoted price 4.00 etc
    p("L08 M2: L(4.90 between)", Lb < 4.90 < 100)
    # M3 halvings
    W = 10.0 - 1e-6
    k = 0
    while W / 2**k > 1e-10:
        k += 1
    p("L08 M3 halvings", k, "log2(W/tol)", f"{math.log2(W/1e-10):.4f}", "10/2^36", f"{10/2**36:.4e}",
      "W/2^36", f"{W/2**36:.4e}", "W/2^37", f"{W/2**37:.4e}")
    # Lemma 2.1 finite difference and vega values
    p("L08 vega=100 phi(0.35)", f"{100*phi(0.35):.6f}")
    p("L08 R2 0.01/37.52", f"{0.01/37.52:.8f}", "0.01/37.5240", f"{0.01/37.5240:.8f}")
    fd_worst = 0.0
    for Kx in (80.0, 100.0, 120.0):
        for sx in (0.05, 0.1, 0.2, 0.4):
            hstep = 1e-6
            num = (bs_call(S8, Kx, r8, tau8, sx + hstep) - bs_call(S8, Kx, r8, tau8, sx - hstep)) / (2 * hstep)
            an = S8 * phi(d_terms(S8, Kx, r8, tau8, sx)[0]) * math.sqrt(tau8)
            fd_worst = max(fd_worst, abs(num - an))
    p("L08 Lemma2.1 finite-difference worst abs:", fd_worst)
    # bisection as on the twin
    LOW, HIGH, TOL = 1e-6, 10.0, 1e-10

    def bisect(price: float, Kx: float) -> tuple[float, int]:
        def gap(s: float) -> float:
            return bs_call(S8, Kx, r8, tau8, s) - price

        low, high, hal = LOW, HIGH, 0
        while high - low > TOL:
            mid = (low + high) / 2
            if gap(mid) < 0:
                low = mid
            else:
                high = mid
            hal += 1
        return (low + high) / 2, hal

    # E3: price 0.50 at K=120
    s3, h3 = bisect(0.50, 120.0)
    p("L08 E3 price 0.50 at K=120 sigma", f"{s3:.8f}", "halvings", h3,
      "C(1e-6) at K=120", repr(bs_call(S8, 120.0, r8, tau8, 1e-6)),
      "C(10) at K=120", f"{bs_call(S8, 120.0, r8, tau8, 10.0):.8f}")
    # E2 unrounded price at K=120 sigma .10
    p("L08 E2 K=120 sig=0.10 unrounded", f"{bs_call(S8, 120.0, r8, tau8, 0.10):.10f}",
      "cents", f"{bs_call(S8, 120.0, r8, tau8, 0.10)*100:.4f}")
    # Lower-end claim at K = S e^{r tau}
    Kst = S8 * math.exp(r8 * tau8)
    Lst = max(S8 - Kst * math.exp(-r8 * tau8), 0.0)
    c1st = bs_call(S8, Kst, r8, tau8, 1e-6)
    p("L08 K=Se^{rt} L repr", repr(Lst), "C(1e-6) repr", repr(c1st), "C(1e-6) approx 0.0000399:",
      f"{c1st:.9e}", "0.00001 > L:", 0.00001 > Lst, "bracket fails (C(lo) >= price):", c1st >= 0.00001)
    # the twin code's rejection path at K=Se^{rt}, price 1e-5
    try:
        bisect(1e-5, Kst)
        p("L08 price 1e-5 at Se^{rt}: NOT rejected by bracket (unexpected)")
    except Exception as exc:  # noqa: BLE001
        p("L08 price 1e-5 at Se^{rt}: exception", type(exc).__name__)
    # Quick check of Prop 3.2 error bound on well-conditioned random cases
    rng2 = random.Random(777)
    worst_ratio = 0.0
    n_ok = 0
    for _ in range(1900):
        Kx = rng2.uniform(60, 140)
        sx = rng2.uniform(0.05, 1.0)
        pr = bs_call(S8, Kx, r8, tau8, sx)
        lo_b = max(S8 - Kx * math.exp(-r8 * tau8), 0.0)
        if not (lo_b < pr < S8):
            continue
        vega = S8 * phi(d_terms(S8, Kx, r8, tau8, sx)[0]) * math.sqrt(tau8)
        if vega < 1e-2:
            continue
        if not (bs_call(S8, Kx, r8, tau8, LOW) < pr <= bs_call(S8, Kx, r8, tau8, HIGH)):
            continue
        n_ok += 1
        sh, _ = bisect(pr, Kx)
        worst_ratio = max(worst_ratio, abs(sh - sx) / (TOL / 2))
    p("L08 Prop3.2 random well-conditioned cases:", n_ok, "worst |err|/(tol/2):", f"{worst_ratio:.4f}")
    p("L08 Prop3.2 bound 5e-11 =", TOL / 2)

    print("\n".join(out))


if __name__ == "__main__":
    main()
