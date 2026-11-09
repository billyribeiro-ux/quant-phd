import math, random
from fractions import Fraction

def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

S, K, r, tau, sigma = 100.0, 100.0, 0.05, 1.0, 0.20
d1 = (math.log(S / K) + (r + sigma ** 2 / 2) * tau) / (sigma * math.sqrt(tau))
vega = S * phi(d1) * math.sqrt(tau)
print("d1", repr(d1))
print("phi(0.35)", repr(phi(0.35)), "100*phi(0.35)", repr(100 * phi(0.35)))
print("vega (computed)", repr(vega))
dp = 0.01 / vega
print("first-order dsigma (unrounded vega) =", repr(dp), "in points =", repr(dp * 100), "round 4dp points =", round(dp * 100, 4))
print("first-order dsigma (displayed 37.52) =", repr(0.01 / 37.52), "points", repr(0.01 / 37.52 * 100))
print("first-order dsigma (displayed 37.5240) =", repr(0.01 / 37.5240), "points", repr(0.01 / 37.5240 * 100))
print("6dp of unrounded dsigma:", f"{dp:.6f}", " 4dp of points:", f"{dp*100:.4f}")
print("0.0267 vs unrounded points difference:", round(0.0267 - dp * 100, 6))

# Lemma 2.2 iff check: for r>0, sigma>0, h>0: 0<d<R<u iff h < sigma^2/r^2
rng = random.Random(0)
bad = 0
trials = 0
for _ in range(20000):
    rr = rng.uniform(0.001, 0.5)
    ss = rng.uniform(0.001, 1.0)
    hh = rng.uniform(1e-6, 2.0)
    u = math.exp(ss * math.sqrt(hh)); dd = 1 / u; R = math.exp(rr * hh)
    lhs = (0 < dd < R < u)
    rhs = hh < ss ** 2 / rr ** 2
    trials += 1
    if lhs != rhs:
        # tolerate only floating boundary cases
        if abs(hh - ss ** 2 / rr ** 2) > 1e-9:
            bad += 1
print("Lemma 2.2 iff random trials", trials, "mismatches (excluding boundary within 1e-9):", bad)

# Definition 2.1 tree parameters at n steps: check the claim u,d,R fixed and q in (0,1) under condition
for n in (1, 2, 5, 10, 50, 400):
    h = tau / n
    u = math.exp(sigma * math.sqrt(h)); d = math.exp(-sigma * math.sqrt(h)); R = math.exp(r * h)
    q = (R - d) / (u - d)
    print("n", n, "h", h, "A6 holds (0<d<R<u):", 0 < d < R < u, "h<sigma^2/r^2:", h < sigma ** 2 / r ** 2, "q", round(q, 6))
