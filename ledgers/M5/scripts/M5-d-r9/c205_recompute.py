import sys, random
src = open(sys.argv[1], encoding="utf-8").read()
src = src.replace("\nmain()", "\n")
ns = {"__name__": "x"}
exec(compile(src, sys.argv[1], "exec"), ns)
rng = random.Random(ns["SEED"])
worst = 0.0
for _ in range(ns["PAIRS"]):
    v = [rng.uniform(-10.0, 10.0) for _ in ns["GRID"]]
    w = [rng.uniform(-10.0, 10.0) for _ in ns["GRID"]]
    bv, _ = ns["bellman"](v, ns["GRID"], ns["BETA"])
    bw, _ = ns["bellman"](w, ns["GRID"], ns["BETA"])
    num = max(abs(a - b) for a, b in zip(bv, bw, strict=True))
    den = max(abs(a - b) for a, b in zip(v, w, strict=True))
    worst = max(worst, num / den)
print(repr(worst), worst - 0.9, (worst - 0.9) / 2.220446049250313e-16)
