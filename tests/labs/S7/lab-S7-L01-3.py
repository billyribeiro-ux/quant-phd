import math
from statistics import NormalDist

import numpy as np

# SIMULATED null research loop. Each round picks the in-sample winner among null
# configurations and checks it on the same one-year holdout. Under the null the
# in-sample choice carries no information about the holdout, so each round's
# holdout Sharpe ratio is a fresh draw; keeping the best round reports a maximum.
rng = np.random.default_rng(11)
n_oos, n_reps = 252, 2000
phi, gamma_e = NormalDist(), 0.5772156649015329

print("rounds  mean_reported_holdout_sharpe  expected_max_approximation")
for rounds in (1, 5, 20):
    holdout = rng.standard_normal((n_reps, rounds, n_oos))
    sharpe = holdout.mean(axis=2) / holdout.std(axis=2, ddof=1) * math.sqrt(252)
    reported = sharpe.max(axis=1).mean()
    if rounds == 1:
        approx = 0.0
    else:
        z = (1 - gamma_e) * phi.inv_cdf(1 - 1 / rounds) + gamma_e * phi.inv_cdf(1 - 1 / (rounds * math.e))
        approx = z * math.sqrt(252 / n_oos)
    print(f"{rounds} {reported:.3f} {approx:.3f}")
