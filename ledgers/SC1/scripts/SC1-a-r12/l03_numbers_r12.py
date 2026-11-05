"""Re-derives the L03 Lab 1 claims (largest |z|, SE gap vs H*sqrt(2/N)/20, 13.2 percent, 14 percent bound).

Runs the twin's functions from its source (the trailing main() call removed), with the same seeded RNG order as main().
Usage: python -I l03_numbers_r12.py <checkout>
"""
import math
import random
import sys

src = open(sys.argv[1] + "/tests/labs/SC1/lab-SC1-L03-1.py", encoding="utf-8").read()
src = src.rsplit("\nmain()", 1)[0]
ns: dict[str, object] = {}
exec(compile(src, "twin", "exec"), ns)
squared_increment_sums = ns["squared_increment_sums"]
mean_and_standard_error = ns["mean_and_standard_error"]
SEED, PATHS, LEVELS, HORIZONS = ns["SEED"], ns["PATHS"], ns["LEVELS"], ns["HORIZONS"]

rng = random.Random(SEED)
rows = []
for horizon in HORIZONS:
    for k in LEVELS:
        steps = 2**k
        mean, se = mean_and_standard_error(squared_increment_sums(horizon, steps, PATHS, rng))
        z = (mean - horizon) / se
        theo = horizon * math.sqrt(2 / steps) / 20
        rows.append((horizon, steps, mean, se, z, theo, se / theo - 1))
print(f"{'H':>3} {'N':>4} {'mean':>10} {'se':>10} {'z':>8} {'theo_se':>10} {'gap%':>8}")
for h, n, m, se, z, th, g in rows:
    print(f"{h:>3g} {n:>4d} {m:>10.6f} {se:>10.6f} {z:>8.4f} {th:>10.6f} {100*g:>8.3f}")
print("max |z| =", max(abs(r[4]) for r in rows), "at (H,N)=", max(rows, key=lambda r: abs(r[4]))[:2])
second = sorted(rows, key=lambda r: -abs(r[4]))[1]
print("second max |z| =", abs(second[4]), "at (H,N)=", second[:2])
print("max |gap| % =", max(abs(r[6]) for r in rows) * 100, "at (H,N)=", max(rows, key=lambda r: abs(r[6]))[:2])
print("all |z| <= 3:", all(abs(r[4]) <= 3 for r in rows))
print("all |gap| < 14%:", all(abs(r[6]) < 0.14 for r in rows))
# printed-value gap check (four-decimal printed SE, as the interpretation says)
printed = {(1.0, 1): 0.0718, (2.0, 1): 0.1601, (2.0, 128): 0.0125}
for (h, n), p in printed.items():
    print(f"printed se for H={h:g} N={n}: {p}; theo {h*math.sqrt(2/n)/20:.6f}; gap {100*(p/(h*math.sqrt(2/n)/20)-1):.3f}%")
print("theo H=1 N=1:", math.sqrt(2) / 20, " theo H=2 N=128:", 2 * math.sqrt(2 / 128) / 20)
