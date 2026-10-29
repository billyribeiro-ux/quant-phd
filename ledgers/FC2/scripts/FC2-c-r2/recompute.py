"""Independent recomputation of the numbers in L07 and L08 (run with -I from the checkout)."""
import math
import pathlib
import sys

root = pathlib.Path(sys.argv[1])


def load(name):
    src = (root / f"tests/labs/FC2/{name}.py").read_text(encoding="utf-8")
    src = src.rstrip().removesuffix("main()")
    ns: dict = {}
    exec(compile(src, name, "exec"), ns)
    return ns


def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def npdf(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def bs(S, K, r, t, s):
    rt = s * math.sqrt(t)
    d1 = (math.log(S / K) + (r + s * s / 2) * t) / rt
    d2 = d1 - rt
    return S * ncdf(d1) - K * math.exp(-r * t) * ncdf(d2), d1, d2


def tree(S, K, r, t, s, n):
    h = t / n
    u = math.exp(s * math.sqrt(h))
    d = 1 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    v = [max(S * u**j * d ** (n - j) - K, 0.0) for j in range(n + 1)]
    for _ in range(n):
        v = [(q * v[j + 1] + (1 - q) * v[j]) / R for j in range(len(v) - 1)]
    return v[0], u, d, R, q


C, d1, d2 = bs(100, 100, 0.05, 1, 0.2)
print("L07 C unrounded", repr(C), "cents", C * 100)
print("L07 d1,d2", d1, d2)
print("L07 Ke^-rt", 100 * math.exp(-0.05))
print("L07 put parity", C - 100 + 100 * math.exp(-0.05))
errs = {}
for n in (1, 2, 5, 10, 25, 50, 100, 200, 400):
    V = tree(100, 100, 0.05, 1, 0.2, n)[0]
    errs[n] = (V - C) * 100
    print(f"L07 n={n:4d} tree={V*100:.6f} err_cents={errs[n]:.6f}")
signs = {n: ("+" if e > 0 else "-" if e < 0 else "0") for n, e in errs.items()}
print("L07 signs unrounded", signs)
ch = sum(1 for a, b in zip(list(errs.values()), list(errs.values())[1:]) if (a > 0) != (b > 0))
print("L07 sign changes unrounded", ch)
absv = [abs(e) for e in errs.values()]
print("L07 abs errors nonincreasing", all(x >= y for x, y in zip(absv, absv[1:])))
print("L07 smallest abs", min(errs, key=lambda n: abs(errs[n])))
print("L07 next smallest 200", errs[200])
V1 = tree(100, 100, 0.05, 1, 0.2, 1)
print("L07 E3 V1", V1, "u", V1[1], "d", V1[2], "R", V1[3], "q", V1[4], "payoff up", 100 * V1[1] - 100)
print("L07 M3", [tree(100, 100, 0.05, 1, 0.2, 4)[k] for k in (1, 2, 3, 4)], "h*s", 0.25 ** 0.5 * 0.2)
print("L07 R2 check", bs(100, 100, 0.0125, 4, 0.1)[0], "sqrt-tau-s", 0.1 * 2, "r tau", 0.0125 * 4)
print("L07 M3 cond", 0.04 / 0.0025)
print("L07 positive-at-400? unrounded", errs[400] < 0)

# L08
print("---L08")
print("L08 lower bound", 100 - 100 * math.exp(-0.05))
print("L08 120e^-0.05", 120 * math.exp(-0.05))
c120, _, _ = bs(100, 120, 0.05, 1, 0.10)
print("L08 K120 sigma0.10 price", c120, "cents", c120 * 100)
vega = 100 * npdf(0.35)
print("L08 vega", vega, "dsigma from 0.01/37.52", 0.01 / 37.52, "dsigma unrounded", 0.01 / vega)
print("L08 M3 log2", math.log2((10 - 1e-6) / 1e-10), "width36", (10 - 1e-6) / 2**36, "width37", (10 - 1e-6) / 2**37)
print("L08 k for W/tau", math.ceil(math.log2((10 - 1e-6) / 1e-10)))
print("L08 W=tau/2 ceil log2", math.ceil(math.log2(0.5)))
L08 = load("lab-FC2-L08-1")
s, n = L08["implied_volatility"](0.50, 120.0)
print("L08 E3 price 0.50 K120 ->", s, "halvings", n)
for K, p in ((100.0, 0.0), (100.0, 4.0), (100.0, 100.0), (100.0, 120.0)):
    try:
        L08["implied_volatility"](p, K)
        print("accepted", p)
    except ValueError as e:
        print("rejected", p, str(e)[:60])
# price between bounds but near spot: find where bracket check fails
for p in (99.0, 99.9, 99.99):
    try:
        print("price", p, "->", L08["implied_volatility"](p, 100.0))
    except ValueError as e:
        print("price", p, "rejected:", str(e)[:70])
print("L08 C(10) strike100", bs(100, 100, 0.05, 1, 10)[0], "C(1e-6)", bs(100, 100, 0.05, 1, 1e-6)[0])
print("L08 C(10) strike120", bs(100, 120, 0.05, 1, 10)[0], "C(1e-6) K120", bs(100, 120, 0.05, 1, 1e-6)[0])
