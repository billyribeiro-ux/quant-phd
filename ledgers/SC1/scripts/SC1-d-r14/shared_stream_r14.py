"""Show that grids of different sizes built from random.Random(seed) reuse the same underlying normal draws.

Standard normal number m of the seeded stream is used by the one-step grid as path m (scaled by sqrt(H)), and by the
four-step grid as step (m mod 4) of path floor(m / 4) (scaled by sqrt(H / 4) = sqrt(H) / 2). So every one-step draw is
exactly twice the four-step increment that uses the same normal number, up to rounding. Prints the check.
Usage: shared_stream_r14.py <checkout root>
"""
import math
import random
import sys

root = sys.argv[1]
sys.path.insert(0, f"{root}/course/modules/SC/SC1/grader")
from instance import make_instance  # noqa: E402

inst = make_instance(0)
H, N = inst["H"], inst["n_paths"]
rng1 = random.Random(inst["seed"])
one_step = [rng1.gauss(0.0, math.sqrt(H)) for _ in range(N)]
rng4 = random.Random(inst["seed"])
four = [[rng4.gauss(0.0, math.sqrt(H / 4)) for _ in range(4)] for _ in range(N)]
flat = [x for row in four for x in row]
worst = max(abs(one_step[m] - 2.0 * flat[m]) for m in range(N))
print("H =", H, " N =", N)
print("max |one_step[m] - 2 * four_step_increment[m]| over m < N (same normal number m):", worst)
print("normal number m < N is one-step path m and four-step path m//4 step m%4; e.g. m=5:",
      one_step[5], "vs", 2.0 * flat[5])
