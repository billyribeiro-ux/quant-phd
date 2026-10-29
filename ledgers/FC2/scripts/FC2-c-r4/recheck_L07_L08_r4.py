"""Independent re-derivation of every L07/L08 number the round-4 verifier checks (stdlib only)."""
import math
from decimal import Decimal, getcontext, ROUND_HALF_UP

getcontext().prec = 50


def Phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def d_terms(S, K, r, tau, sig):
    root = sig * math.sqrt(tau)
    d1 = (math.log(S / K) + (r + sig * sig / 2) * tau) / root
    return d1, d1 - root


def C(S, K, r, tau, sig):
    d1, d2 = d_terms(S, K, r, tau, sig)
    return S * Phi(d1) - K * math.exp(-r * tau) * Phi(d2)


def V(n, S=100.0, K=100.0, r=0.05, sig=0.2, tau=1.0):
    h = tau / n
    u = math.exp(sig * math.sqrt(h))
    d = 1 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    vals = [max(S * u**j * d ** (n - j) - K, 0.0) for j in range(n + 1)]
    for _ in range(n):
        vals = [(q * vals[j + 1] + (1 - q) * vals[j]) / R for j in range(len(vals) - 1)]
    return vals[0], (u, d, R, q)


def cents_half_up(x):
    return int((Decimal(repr(x)) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))


closed = C(100, 100, 0.05, 1, 0.2)
print("C=", repr(closed), "cents", closed * 100)
print("Ke^-r=", 100 * math.exp(-0.05))
d1, d2 = d_terms(100, 100, 0.05, 1, 0.2)
print("d1,d2", d1, d2, "Phi(d1)", Phi(d1), "Phi(d2)", Phi(d2))
P = closed - 100 + 100 * math.exp(-0.05)
print("put P", P, "cents", P * 100)
print("put direct", 100 * math.exp(-0.05) * Phi(-d2) - 100 * Phi(-d1))
print("Phi symmetry", [Phi(x) + Phi(-x) - 1 for x in (0.0, 0.35, 1.7, 3.0)])
print("--- L07 tree table: n, V_n cents, error unrounded (currency), error cents")
for n in (1, 2, 5, 10, 25, 50, 100, 200, 400):
    v, (u, d, R, q) = V(n)
    e = v - closed
    print(n, repr(v), cents_half_up(v), repr(e), e * 100, cents_half_up(e),
          "printed-diff", cents_half_up(v) - cents_half_up(closed))
print("--- M3 n=4 params")
u4 = math.exp(0.1); d4 = 1 / u4; R4 = math.exp(0.0125)
print("u4", u4, "d4", d4, "R4", repr(R4), "q4", (R4 - d4) / (u4 - d4), "sig^2/r^2", 0.04 / 0.0025)
print("--- E3 n=1 params")
u1 = math.exp(0.2); d1s = 1 / u1; R1 = math.exp(0.05)
q1 = (R1 - d1s) / (u1 - d1s)
print("u1", u1, "d1", d1s, "R1", R1, "q1", q1, "V1", math.exp(-0.05) * q1 * (100 * u1 - 100), V(1)[0])
print("--- R2 alt inputs tau=4 sig=0.1 r=0.0125", C(100, 100, 0.0125, 4, 0.1))
print("--- L08 bounds")
L = max(100 - 100 * math.exp(-0.05), 0)
print("L", repr(L))
print("C(1e-9)", C(100, 100, 0.05, 1, 1e-9), "C(1e4)", C(100, 100, 0.05, 1, 1e4))
print("C(K=120, sig=0.10) =", C(100, 120, 0.05, 1, 0.10), "cents", C(100, 120, 0.05, 1, 0.10) * 100)
print("120e^-0.05", 120 * math.exp(-0.05))
print("vega 100phi(0.35)", 100 * phi(0.35), "0.01/37.52", 0.01 / 37.52, "0.01/37.5240", 0.01 / 37.5240)
print("width k=36", 10 / 2**36, "k=37", 10 / 2**37, "log2(1e11)", math.log2(1e11))
print("W/tol", (10 - 1e-6) / 1e-10, math.log2((10 - 1e-6) / 1e-10), math.ceil(math.log2((10 - 1e-6) / 1e-10)))
print("C at K=100 price 99.99999 vs C(10):", C(100, 100, 0.05, 1, 10.0))
