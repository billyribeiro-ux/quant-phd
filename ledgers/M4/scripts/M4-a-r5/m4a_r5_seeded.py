"""Round-5 independent re-derivation of the seeded sample numbers printed by Labs L02 and L03 (slice a).

Own code, no import of the lab files: reproduces each seeded draw with the same stdlib generator calls and recomputes
the printed sample statistics. Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-a-r5/m4a_r5_seeded.py
"""
import math
import random

out = []

# L02 die: seed 2026, n = 10000, rolls by randint(1, 6)
rng = random.Random(2026)
rolls = [rng.randint(1, 6) for _ in range(10000)]
mean = sum(rolls) / 10000
var = sum((x - mean) ** 2 for x in rolls) / 10000
out.append(f"L02 die seed 2026 n=10000 mean={mean:.3f} var={var:.3f} minus3.5={mean - 3.5:+.3f}")

# L02 loss: seed 2027, losses 250000 with prob 0.05 via random() < 0.05
rng = random.Random(2027)
losses = [250000 if rng.random() < 0.05 else 0 for _ in range(10000)]
count = sum(1 for x in losses if x > 0)
mean_l = sum(losses) / 10000
var_l = sum((x - mean_l) ** 2 for x in losses) / 10000
out.append(f"L02 loss seed 2027 losses={count} total={sum(losses)} mean={mean_l:.1f} var={var_l:.1f}")

# L03 skewed law: seed 2026, rng.choices over values 0,1,2,10 with weights 4,2,1,1, k = 20000
rng = random.Random(2026)
draws = rng.choices([0, 1, 2, 10], weights=(4, 2, 1, 1), k=20000)
n = len(draws)
mu = sum(draws) / n
m2 = sum((x - mu) ** 2 for x in draws) / n
m3 = sum((x - mu) ** 3 for x in draws) / n
m4 = sum((x - mu) ** 4 for x in draws) / n
out.append(f"L03 skewed seed 2026 n=20000 skewness={m3 / m2 ** 1.5:.3f} kurtosis={m4 / m2 ** 2:.3f}")

# Exact values for the same table, from the fractions of Section 3 (independent float check)
p = [0.5, 0.25, 0.125, 0.125]
v = [0, 1, 2, 10]
mu_e = sum(a * b for a, b in zip(v, p))
c = [sum(((a - mu_e) ** k) * b for a, b in zip(v, p)) for k in (2, 3, 4)]
out.append(f"L03 exact mu={mu_e} m2={c[0]} m3={c[1]} m4={c[2]} skew={c[1] / c[0] ** 1.5:.6f} kurt={c[2] / c[0] ** 2:.6f}")
out.append(f"L03 exact skew 4dp={c[1] / c[0] ** 1.5:.4f} kurt 4dp={c[2] / c[0] ** 2:.4f}")

for line in out:
    print(line)
