"""Spot check of Proposition 2.8 (logarithmic demand x_s = pi_s w / q_s is the unique maximizer on the budget set)
and of Proposition 2.5 (Walras' law) for random economies. Seeded; standard library only."""
import math
import random

rng = random.Random(20261104)
worst_gap = -math.inf
violations = 0
trials = 300
for _ in range(trials):
    S = rng.randint(2, 4)
    raw = [rng.random() + 0.05 for _ in range(S)]
    pi = [r / sum(raw) for r in raw]
    q = [rng.uniform(0.05, 2.0) for _ in range(S)]
    w = rng.uniform(0.1, 3.0)
    xstar = [pi[s] * w / q[s] for s in range(S)]
    U = lambda x: sum(pi[s] * math.log(x[s]) for s in range(S))
    best = U(xstar)
    for _ in range(400):
        # random bundle on or inside the budget set: draw positive weights, scale to spend w (or less)
        raw_x = [rng.random() + 1e-9 for _ in range(S)]
        scale = rng.uniform(0.0, 1.0) * w / sum(raw_x[s] * q[s] for s in range(S))
        x = [raw_x[s] * scale for s in range(S)]
        assert sum(q[s] * x[s] for s in range(S)) <= w + 1e-9
        gap = U(x) - best
        worst_gap = max(worst_gap, gap)
        if gap > 1e-12:
            violations += 1
    # budget binds at x*
    assert abs(sum(q[s] * xstar[s] for s in range(S)) - w) < 1e-12
print("trials", trials, "random_bundles_per_trial", 400, "violations_of_maximality", violations)
print("max_U(random)-U(x*) over all draws (should be <= 0)", worst_gap)
