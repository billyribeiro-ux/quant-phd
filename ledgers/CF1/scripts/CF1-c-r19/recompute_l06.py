"""Independent recomputation of L06 Lab 1 quantities (round 19). Run with python -I."""
import math
import random
import statistics

SEED, RATE, YEARS, INV, LOW, HIGH, N = 6, 0.10, 5, 300_000, 50_000, 150_000, 50_000

# closed forms (Proposition 2.3), recomputed independently with a plain loop
mu = (LOW + HIGH) / 2
A = sum((1 + RATE) ** -t for t in range(1, YEARS + 1))
m = HIGH - LOW + 1
var_x = (m * m - 1) / 12
expected = -INV + mu * A
sd_exact = math.sqrt(sum(var_x * (1 + RATE) ** (-2 * t) for t in range(1, YEARS + 1)))
print(f"closed_expected {expected:.4f} closed_sd {sd_exact:.4f}")
print(f"closed_expected_E {expected:.2f} (page says 79078.68)")

# draws: same generator order as the twin (rng.randint per year, per draw)
rng = random.Random(SEED)
npvs = []
for _ in range(N):
    rec = [rng.randint(LOW, HIGH) for _ in range(YEARS)]
    npvs.append(-INV + sum(x / (1 + RATE) ** (t + 1) for t, x in enumerate(rec)))
s = sorted(npvs)
def q(p):
    k = math.ceil(p * N)
    return s[k - 1]
q10, q50, q90 = q(0.10), q(0.50), q(0.90)
print(f"q10 {q10:.6f} q50 {q50:.6f} q90 {q90:.6f}")
width = q90 - q10
print(f"width_unrounded_cents {width:.6f} rounds_to {width:.2f} width_currency {width/100:.6f} -> {width/100:.2f}")
print(f"printed_width {round(143406.13-14896.62,2):.2f} printed_currency {(143406.13-14896.62)/100:.4f}")
print(f"gap_printed_minus_unrounded {(143406.13-14896.62) - width:.6f}")
neg = sum(1 for x in npvs if x < 0) / N
se = math.sqrt(neg * (1 - neg) / N)
print(f"share_neg {neg:.6f} se {se:.6f}")
print(f"sd_sample {statistics.stdev(npvs):.4f} ratio {statistics.stdev(npvs)/sd_exact:.6f}")
z = (math.fsum(npvs[:N]) / N - expected) / (statistics.stdev(npvs) / math.sqrt(N))
print(f"z_50000 {z:.4f}")
