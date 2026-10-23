import numpy as np
from numpy.typing import NDArray

# SIMULATED: N risky payoffs plus a riskless one, priced by a known SDF; x* estimated on T draws and evaluated
# on a fresh sample of 4,000 draws. In sample the pricing errors are zero by construction (Proposition 2.1).
rng = np.random.default_rng(707)
n_reps, n_test = 100, 4_000


def draw(n_obs: int, n_risky: int) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """n_obs draws of (payoffs, SDF): lognormal SDF, payoffs loaded on the SDF shock plus noise."""
    shock = rng.standard_normal(n_obs)
    m = np.exp(-0.02 - 0.5 * 0.3**2 - 0.3 * shock)  # E[m] = exp(-0.02)
    loads = np.linspace(0.02, 0.10, n_risky)
    x = 1.0 + np.outer(shock, loads) + 0.15 * rng.standard_normal((n_obs, n_risky))
    return np.column_stack([np.ones(n_obs), x]), m


def true_prices(n_risky: int) -> NDArray[np.float64]:
    """Prices E[m x] computed on one large sample (400,000 draws), the 'population' for this lab."""
    x, m = draw(400_000, n_risky)
    return np.asarray(x.T @ m / m.size)


print("N risky  T    in-sample errors < 1e-12  out-of-sample rms error (median)  s.d. of x* (median)")
for n_risky in (2, 8):
    p = true_prices(n_risky)
    for n_obs in (60, 240, 960):
        ins: list[float] = []
        outs: list[float] = []
        sds: list[float] = []
        for _ in range(n_reps):
            xt, _m = draw(n_obs, n_risky)
            b = np.linalg.solve(xt.T @ xt / n_obs, p)
            xs, _m = draw(n_test, n_risky)
            ins.append(float(np.sqrt(np.mean((xt.T @ (xt @ b) / n_obs - p) ** 2))))
            outs.append(float(np.sqrt(np.mean((xs.T @ (xs @ b) / n_test - p) ** 2))))
            sds.append(float((xt @ b).std()))
        print(f"{n_risky:7d}  {n_obs:4d} {max(ins) < 1e-12}                      {np.median(outs):.5f}", end="")
        print(f"                           {np.median(sds):.4f}")
