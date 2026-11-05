"""Round 9, slice e: numeric check behind the E4-c185 finding (G(lambda) > 0 on (0, 1] at one instance).

Instance: a = 2, sigma_v^2 = sigma_eps^2 = 1, sigma_u^2 = 1 (the Example 1.1 values of L08). Formulas from L08
Definition 4.3, Corollary 2.4, Proposition 3.1 and Proposition 4.1. Prints the grid minimum; this supports the truth
of the claim at one instance and is not a proof.
"""
import math


def G(lam: float, a: float = 2.0, sv: float = 1.0, se: float = 1.0, su2: float = 1.0) -> float:
    tv, te = 1 / sv, 1 / se
    kap = a * se / lam
    tau_eta = 1 / (se + kap * kap * su2)
    A = lam * te + (1 - lam) * tau_eta
    beta = A / (tv + A)
    bs = te / (tv + te)
    by = tau_eta / (tv + tau_eta)
    VI = 1 / (tv + te)
    VU = 1 / (tv + tau_eta)
    var_DI = (bs - beta) ** 2 * (sv + se) + kap * kap * beta * beta * su2
    var_DU = (by - beta) ** 2 * (sv + 1 / tau_eta)
    return (1 / (2 * a)) * math.log((1 + var_DI / VI) / (1 + var_DU / VU))


vals = [(G(k / 10000), k / 10000) for k in range(1, 10001)]
print("grid minimum (G, lambda) over 10000 points in (0, 1]:", min(vals))
print("G(1e-6) =", G(1e-6), " G(1) =", G(1.0), " ln(5/3)/4 =", math.log(5 / 3) / 4)
print("points with G <= 0:", sum(1 for g, _ in vals if g <= 0))
