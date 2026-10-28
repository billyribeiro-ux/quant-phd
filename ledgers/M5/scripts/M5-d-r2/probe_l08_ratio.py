import sys, runpy, random
src = open("/tmp/verifyB2-M5-d/tests/labs/M5/lab-M5-L08-1.py", encoding="utf-8").read()
src = src.replace("\nmain()\n", "\n")
ns = {"__name__": "probe"}
exec(compile(src, "lab08", "exec"), ns)
rng = random.Random(ns["SEED"])
worst = 0.0; above = 0
for _ in range(ns["PAIRS"]):
    v = [rng.uniform(-10.0, 10.0) for _ in ns["GRID"]]
    w = [rng.uniform(-10.0, 10.0) for _ in ns["GRID"]]
    bv, _ = ns["bellman"](v, ns["GRID"], ns["BETA"])
    bw, _ = ns["bellman"](w, ns["GRID"], ns["BETA"])
    num = max(abs(a - b) for a, b in zip(bv, bw, strict=True))
    den = max(abs(a - b) for a, b in zip(v, w, strict=True))
    r = num / den
    if r > ns["BETA"]: above += 1
    worst = max(worst, r)
print("BETA", ns["BETA"], "worst unrounded", repr(worst), "worst-beta", worst - ns["BETA"], "pairs above beta", above)
