"""Re-derive the L09 numbers: Lab 1 printed values, the naive-stop ratio, the a priori count, and the quiz values.

Usage: python3 -I l09_numbers.py <repo-root>
"""

import math
import pathlib
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
twin = root / "tests/labs/M5/lab-M5-L09-1.py"
out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=False)
print("twin exit", out.returncode, "stderr", repr(out.stderr))
print(out.stdout)

src = twin.read_text(encoding="utf-8")
head = src.split("def main()")[0]
g: dict[str, object] = {"__name__": "lab_head"}
exec(compile(head, "head", "exec"), g)
bellman = g["bellman"]
sup = g["sup_distance"]
BETA = g["BETA"]
GRID = g["GRID"]

# reference: iterate until certified <= 1e-12
prev = [0.0] * 4
cur = bellman(prev)
n = 1
while (BETA / (1 - BETA)) * sup(prev, cur) > 1e-12:
    prev, cur = cur, bellman(cur)
    n += 1
v_ref = cur
print("reference n", n, "cert", (BETA / (1 - BETA)) * sup(prev, cur))

# naive stop: sup-step <= 1e-6, unrounded step and error
prev = [0.0] * 4
cur = bellman(prev)
m = 1
while sup(prev, cur) > 1e-6:
    prev, cur = cur, bellman(cur)
    m += 1
step = sup(prev, cur)
err = sup(cur, v_ref)
print("naive n", m, "unrounded step", repr(step), "actual error", repr(err))
print("ratio error/step", err / step, " 9*step", 9 * step, " ratio of printed values", 0.0000085808 / 0.0000009534)
print("error - 9*step (should be ~0 to printed digits):", err - 9 * step)

# fixed count 10
prev = [0.0] * 4
cur = bellman(prev)
for _ in range(9):
    prev, cur = cur, bellman(cur)
print("fixed10 cert", (BETA / (1 - BETA)) * sup(prev, cur), "actual", sup(cur, v_ref))

# certified stops: actual error vs certified error (exact equality expected in this instance)
for tol in (1e-2, 1e-4, 1e-6):
    prev = [0.0] * 4
    cur = bellman(prev)
    k = 1
    while (BETA / (1 - BETA)) * sup(prev, cur) > tol:
        prev, cur = cur, bellman(cur)
        k += 1
    cert = (BETA / (1 - BETA)) * sup(prev, cur)
    actual = sup(cur, v_ref)
    steps = [c - p for c, p in zip(cur, prev, strict=True)]
    print("stop tol", tol, "n", k, "cert", repr(cert), "actual", repr(actual), "spread", max(steps) - min(steps))

# a priori count (R2): least n with 0.9^n / 0.1 * sqrt(3)/2 <= 1e-6, and values at 151, 152
d = math.sqrt(3) / 2
for k in (151, 152):
    print("a priori bound at", k, BETA**k / (1 - BETA) * d)
nmin = next(k for k in range(1, 1000) if BETA**k / (1 - BETA) * d <= 1e-6)
print("a priori least n", nmin)
print("V1 max over grid", max(bellman([0.0] * 4)), "sqrt(3)/2", d)

# quiz / problem values
print("M1 factors", 0.5 / 0.5, 0.9 / 0.1, 0.99 / 0.01)
print("M2 cert2", 0.8 / 0.2 * 0.016)
print("M3 step", 1e-3 * (1 - 0.9) / 0.9)
print("L09q4 0.9^10/0.1", 0.9**10 / 0.1)
print("L09q2 cert", 0.5 / 0.5 * 0.02)
