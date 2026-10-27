"""Round-28 part C: independent pure-Python recomputation of the L08 Lab 3 PBO test matrix (tests/test_labs.py lines
173-184): 8 rows = 4 blocks of 2 rows, 3 configurations (columns), mean return as the performance measure,
all C(4,2) = 6 in-sample/out-of-sample splits, rank 1 = best, omega = rank / (N + 1), logit = ln(omega / (1 - omega)),
PBO = share of splits with logit <= 0 (the page's convention). Performance = Sharpe ratio mean/sd(ddof=1), as in
the twin (tests/labs/S7/lab-S7-L08-3.py lines 8-27), with mid-rank for ties. Run: python -I l08_lab3_pbo_C.py"""
import itertools
import math

M = [
    [0.35, 0.82, 0.33],
    [-1.3, 0.91, 0.45],
    [-0.54, 0.58, 0.36],
    [0.29, 0.03, 0.55],
    [-0.74, -0.16, -0.48],
    [0.6, 0.04, -0.29],
    [-0.78, -0.26, 0.01],
    [-0.28, 1.29, 1.01],
]
blocks = [M[2 * i: 2 * i + 2] for i in range(4)]
N = 3
logits = []
for ins in itertools.combinations(range(4), 2):
    out = [b for b in range(4) if b not in ins]
    rows_in = [r for b in ins for r in blocks[b]]
    rows_out = [r for b in out for r in blocks[b]]
    def sr(rows, c):
        xs = [r[c] for r in rows]
        mu = sum(xs) / len(xs)
        sd = (sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5
        return mu / sd
    sr_in = [sr(rows_in, c) for c in range(N)]
    sr_out = [sr(rows_out, c) for c in range(N)]
    winner = max(range(N), key=lambda c: sr_in[c])
    greater = sum(1 for c in range(N) if sr_out[c] > sr_out[winner])
    ties = sum(1 for c in range(N) if sr_out[c] == sr_out[winner])
    rank = 1 + greater + 0.5 * (ties - 1)
    omega = rank / (N + 1)
    logit = math.log(omega / (1 - omega))
    logits.append(logit)
    print(f"in {ins} out {tuple(out)}: winner {winner + 1}, out-of-sample rank {rank} of {N}, omega {omega:.3f}, logit {logit:.6f}")
pbo = sum(1 for x in logits if x <= 0) / len(logits)
print(f"splits {len(logits)}, every logit exactly 0: {all(abs(x) < 1e-12 for x in logits)}, PBO {pbo}")
