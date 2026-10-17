import numpy as np

# SIMULATED pure-noise strategies: no strategy has any skill.
rng = np.random.default_rng(20261017)
n_strategies, n_is, n_oos, n_reps = 100, 630, 630, 100
annualize = np.sqrt(252)

best_is = np.empty(n_reps)
best_oos = np.empty(n_reps)
for rep in range(n_reps):
    r = rng.standard_normal((n_is + n_oos, n_strategies)) * 0.01  # daily excess returns
    is_part, oos_part = r[:n_is], r[n_is:]
    sr_is = is_part.mean(axis=0) / is_part.std(axis=0, ddof=1)
    sr_oos = oos_part.mean(axis=0) / oos_part.std(axis=0, ddof=1)
    k = int(np.argmax(sr_is))  # the researcher keeps the in-sample winner
    best_is[rep] = sr_is[k] * annualize
    best_oos[rep] = sr_oos[k] * annualize

print(f"mean in-sample Sharpe of the selected strategy: {best_is.mean():.3f}")
print(f"mean out-of-sample Sharpe of the same strategy: {best_oos.mean():.3f}")
print(f"share of selections that lose money out of sample: {np.mean(best_oos < 0):.2f}")
