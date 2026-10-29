import math, random, sys
from fractions import Fraction
sys.argv = ["x"]
src = open("/Users/billyribeiro/.fanout/wt/verifyB8-M5-d/tests/labs/M5/lab-M5-L08-1.py").read()
src = src.replace("\nmain()", "\n")
g = {"__name__": "lab"}
exec(compile(src, "lab08", "exec"), g)
GRID, BETA, PAIRS, SEED = g["GRID"], g["BETA"], g["PAIRS"], g["SEED"]
bellman, solve = g["bellman"], g["solve"]
# Part B unrounded worst ratio
rng = random.Random(SEED)
worst = 0.0
for _ in range(PAIRS):
    v = [rng.uniform(-10.0, 10.0) for _ in GRID]
    w = [rng.uniform(-10.0, 10.0) for _ in GRID]
    bv, _ = bellman(v, GRID, BETA)
    bw, _ = bellman(w, GRID, BETA)
    num = max(abs(a - b) for a, b in zip(bv, bw, strict=True))
    den = max(abs(a - b) for a, b in zip(v, w, strict=True))
    worst = max(worst, num / den)
print("worst unrounded", repr(worst), "excess over beta", worst - BETA, "in ulps of beta", (worst - BETA) / (math.ulp(BETA)))
# Part E1 analogue: iteration counts at other betas on the four-point grid
for b in (0.5, 0.9, 0.95):
    vals, pol, cnt = solve(GRID, b)
    print("beta", b, "iterations", cnt)
# lab L09 numbers: a priori bound at n=151,152 for four-point grid, beta 0.9
