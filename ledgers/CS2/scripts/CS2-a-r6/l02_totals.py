"""Recompute L02 lab totals from the twin's own functions (main() is not run).

Prints the integer successful totals and unsuccessful totals per load, and checks the rounding-interval
claims of the L02 lesson text: the only integer total that prints as each successful/unsuccessful average.
Usage: l02_totals.py ROOT
"""

import pathlib
import random
import sys

root = pathlib.Path(sys.argv[1])
src = (root / "tests/labs/CS2/lab-CS2-L02-1.py").read_text(encoding="utf-8")
src = src.rsplit("\nmain()", 1)[0]  # drop the top-level call; keep every definition
ns: dict[str, object] = {}
exec(compile(src, "lab-CS2-L02-1-noMain", "exec"), ns)
ChainedHashTable = ns["ChainedHashTable"]
BUCKETS = ns["BUCKETS"]
rng = random.Random(2026)
keys = rng.sample(range(10**9), 256)
stored_all = set(keys)
absent = [x for x in rng.sample(range(10**9), 2000) if x not in stored_all][:500]
print("absent count", len(absent))
for n in (16, 32, 64, 128, 256):
    t = ChainedHashTable(BUCKETS)
    for k in keys[:n]:
        t.insert(k)
    succ = sum(t.lookup(k)[1] for k in keys[:n])
    unsucc = sum(t.lookup(k)[1] for k in absent)
    print(f"n={n} successful_total={succ} avg={succ / n:.10f} unsuccessful_total={unsucc} avg={unsucc / 500:.10f}")
    # integers whose quotient by n rounds (4 dp) to the printed successful average
    printed_s = f"{succ / n:.4f}"
    cands_s = [t_ for t_ in range(0, 5 * n) if f"{t_ / n:.4f}" == printed_s]
    printed_u = f"{unsucc / 500:.4f}"
    cands_u = [t_ for t_ in range(0, 5 * 500) if f"{t_ / 500:.4f}" == printed_u]
    print(f"   succ printed {printed_s} integer totals giving it: {cands_s}; unsucc printed {printed_u} totals: {cands_u}")
colliding = [64 * j for j in range(1, 51)]
t = ChainedHashTable(BUCKETS)
for k in colliding:
    t.insert(k)
print("colliding successful total", sum(t.lookup(k)[1] for k in colliding), "miss", t.lookup(64 * 51))
print("257/128 =", 257 / 128, " 193/64 =", 193 / 64, " 772/256 =", 772 / 256, " 386/128 - 257/128 =", (386 - 257) / 128)
