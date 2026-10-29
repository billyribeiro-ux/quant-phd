# Compares projection_repair of reference and of each moved mutant on random unit-diagonal inputs.
import importlib.util, random, math, sys
ROOT = sys.argv[1]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("ref", ROOT + "/course/modules/M/M3/grader/reference.py")
muts = {n: load(n, ROOT + "/ledgers/M3/equivalent/" + f) for n, f in [
    ("r6d_m04", "r6d_m04_projection_stops_on_gap_only.py"),
    ("r11d_m02", "r11d_m02_projection_stops_on_step_only.py"),
    ("r15d_m03", "r15d_m03_projection_repair_no_final_symmetry.py")]}
def frob(a, b): return math.sqrt(sum((a[i][j]-b[i][j])**2 for i in range(len(a)) for j in range(len(a))))
def props(x, tol=1e-8):
    n=len(x); sym=max(abs(x[i][j]-x[j][i]) for i in range(n) for j in range(n))
    dg=max(abs(x[i][i]-1) for i in range(n)); ev=ref.min_eigenvalue(x)
    return sym, dg, ev
worst = {k: [0.0, 0.0, 1e9] for k in muts}
count = 0
for seed in range(0, 200):
    rng = random.Random(seed)
    n = rng.choice([3,4,5,6])
    a = [[0.0]*n for _ in range(n)]
    for i in range(n):
        a[i][i] = 1.0
        for j in range(i+1, n):
            v = rng.uniform(-0.99, 0.99) if rng.random() < 0.7 else rng.gauss(0, 0.6)
            v = max(-0.999, min(0.999, v)); a[i][j]=a[j][i]=v
    r = ref.projection_repair(a)
    count += 1
    for k, m in muts.items():
        x = m.projection_repair(a)
        d = max(abs(x[i][j]-r[i][j]) for i in range(n) for j in range(n))
        sym, dg, ev = props(x)
        w = worst[k]
        w[0] = max(w[0], d); w[1] = max(w[1], abs(dg)); w[2] = min(w[2], ev)
        # property check: symmetric to 1e-12, unit diag to 1e-12, eigen >= -1e-8
        if sym > 1e-12 or dg > 1e-12 or ev < -1e-8:
            print("PROPERTY VIOLATION", k, seed, sym, dg, ev)
print("inputs", count)
for k, w in worst.items():
    print(f"{k}: max|mutant-reference| entry diff={w[0]:.3e}  max diag dev={w[1]:.3e}  min eigenvalue={w[2]:.3e}")
# Lab 3 matrix printed numbers
