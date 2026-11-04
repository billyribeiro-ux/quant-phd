"""Recompute Corr(v,p)^2 = tau_eta/(tau_v+tau_eta) at the printed informed fractions of L08 Part C (verifier, round 1)."""

lams = {0.12: 1.0, 0.13: 0.965625410, 0.14: 0.815032329, 0.15: 0.657828572, 0.16: 0.480567912, 0.17: 0.231615819}
for cost, lam in lams.items():
    kappa = 2.0 / lam  # a * sigma_eps^2 / lam with a = 2, sigma_eps^2 = 1
    tau_eta = 1.0 / (1.0 + kappa * kappa * 1.0)  # sigma_u^2 = 1
    corr2 = tau_eta / (1.0 + tau_eta)  # tau_v = 1
    print(f"cost {cost:.2f} lam {lam:.9f} Corr^2 {corr2:.6f}")
