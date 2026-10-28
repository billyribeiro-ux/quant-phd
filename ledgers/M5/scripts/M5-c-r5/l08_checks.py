# Verifier scratch check for L08 claims (round 5). Re-runs modified copies of the L08 lab with BETA changed.
import importlib.util, math, random, sys, io, contextlib, re
LAB = sys.argv[1]
src = open(LAB, encoding="utf-8").read().replace("\nmain()\n", "\n")
def run(beta):
    s = src.replace("BETA = 0.9\n", f"BETA = {beta}\n")
    ns = {"__name__": "x"}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(s, "lab", "exec"), ns)
        ns["part_a"]()
    m = re.search(r"= (\d+)$", buf.getvalue().split("\n")[1])
    return int(m.group(1))
for b in (0.5, 0.9, 0.95):
    print("solver count at BETA", b, run(b))
# unrounded largest sampled ratio, same seed and draw order as part_b
ns = {"__name__": "x"}
exec(compile(src.replace("\nmain()\n", "\n"), "lab", "exec"), ns)
rng = random.Random(ns["SEED"]); GRID = ns["GRID"]; BETA = ns["BETA"]
worst = 0.0
for _ in range(ns["PAIRS"]):
    v = [rng.uniform(-10.0, 10.0) for _ in GRID]
    w = [rng.uniform(-10.0, 10.0) for _ in GRID]
    bv, _ = ns["bellman"](v, GRID, BETA); bw, _ = ns["bellman"](w, GRID, BETA)
    num = max(abs(a - b) for a, b in zip(bv, bw)); den = max(abs(a - b) for a, b in zip(v, w))
    worst = max(worst, num / den)
print("unrounded worst ratio", repr(worst), "minus beta", worst - BETA, "in ulps", (worst - BETA) / math.ulp(BETA))
