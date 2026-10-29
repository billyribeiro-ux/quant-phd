import sys, random, math, importlib.util
G = "/Users/billyribeiro/.fanout/wt/verifyB11-M3-d/course/modules/M/M3/grader/"
M = "/Users/billyribeiro/.fanout/wt/verifyB11-M3-d/ledgers/M3/mutants/"
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
ref = load(G + "reference.py", "ref")
mods = {"step_only": load(M + "r11d_m02_projection_stops_on_step_only.py", "m_step"),
        "gap_only": load(M + "r6d_m04_projection_stops_on_gap_only.py", "m_gap")}
random.seed(11)
def rand_unit(n):
    a = [[0.0]*n for _ in range(n)]
    for i in range(n):
        a[i][i] = 1.0
        for j in range(i+1, n):
            v = random.uniform(-0.95, 0.95); a[i][j] = a[j][i] = v
    return a
worst = {k: {"minEig": 0.0, "diag": 0.0, "dist_gap": 0.0, "n_fail_psd1e8": 0} for k in mods}
N = 300
for t in range(N):
    n = random.choice([3, 4, 5])
    a = rand_unit(n)
    r = ref.projection_repair(a)
    rmin = ref.min_eigenvalue(r)
    rd = ref.projection_repair  # reference
    def dist(x): return math.sqrt(sum((x[i][j]-a[i][j])**2 for i in range(n) for j in range(n)))
    for k, m in mods.items():
        x = m.projection_repair(a)
        e = m.min_eigenvalue(x)
        d = max(abs(x[i][i]-1) for i in range(n))
        w = worst[k]
        w["minEig"] = min(w["minEig"], e)
        w["diag"] = max(w["diag"], d)
        w["dist_gap"] = max(w["dist_gap"], dist(x) - dist(r))
        if e < -1e-8: w["n_fail_psd1e8"] += 1
for k in worst: print(k, worst[k])
print("N", N)
