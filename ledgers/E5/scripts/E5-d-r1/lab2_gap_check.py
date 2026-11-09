"""Recompute lab-2 log gap and percent-of-trend gap at the latest quarter (independent of the twin's helpers)."""
import math, random
SEED, Q, W = 2026, 24, 20
rng = random.Random(SEED)
gdp = [20000.0]
for _ in range(Q - 1):
    gdp.append(gdp[-1] * (1 + 0.004 + 0.012 * (rng.random() - 0.5)))
t_end = Q - 1
first = t_end - W + 1
xs = list(range(W)); ys = [math.log(gdp[first + k]) for k in range(W)]
mx = sum(xs) / W; my = sum(ys) / W
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
intercept = my - slope * mx
trend_log = intercept + slope * (W - 1)
log_gap = 100 * (math.log(gdp[t_end]) - trend_log)
pct_gap = 100 * (gdp[t_end] / math.exp(trend_log) - 1)
print(f"log_gap {log_gap:.6f} pct_gap {pct_gap:.6f} printed_2dp {log_gap:.2f} {pct_gap:.2f}")
