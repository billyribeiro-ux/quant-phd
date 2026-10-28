# Verifier scratch check for L09 claims (round 5): R2 a priori count, step spread exactness, factor values.
import math, io, contextlib
lab = open("/tmp/verifyB5-M5-c/tests/labs/M5/lab-M5-L09-1.py", encoding="utf-8").read().replace("\nmain()\n", "\n")
ns = {"__name__": "x"}
exec(compile(lab, "lab", "exec"), ns)
d = math.sqrt(3) / 2
for n in (147, 151, 152):
    print("n", n, "bound", 0.9**n / (1 - 0.9) * d)
print("a priori count", next(n for n in range(1, 10**4) if 0.9**n / 0.1 * d <= 1e-6))
print("0.9^10/0.1", 0.9**10 / 0.1)
print("1/9000", 1 / 9000, "1e-3*(1-b)/b", 1e-3 * 0.1 / 0.9)
# exact step spread at each certified stop
for tol in ns["TOLERANCES"]:
    n, v, prev = ns["iterate_until"](ns["certified_stop"](tol))
    steps = [c - p for c, p in zip(v, prev)]
    print("tol", tol, "n", n, "steps", steps, "spread exact", max(steps) - min(steps))
print("ratio naive", 0.0000085808 / 0.0000009534, "3 digits", 9.0002)
