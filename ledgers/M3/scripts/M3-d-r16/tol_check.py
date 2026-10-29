import importlib.util, sys, math
ROOT = sys.argv[1]
def load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ref = load("ref", ROOT + "/course/modules/M/M3/grader/reference.py")
m3 = load("m3", ROOT + "/ledgers/M3/equivalent/r15d_m03_projection_repair_no_final_symmetry.py")
a = [[1.0, 0.8, -0.5, 0.6], [0.8, 1.0, 0.7, -0.6], [-0.5, 0.7, 1.0, 0.2], [0.6, -0.6, 0.2, 1.0]]
for tol in (1e-10, 1e-6, 1e-3):
    r = ref.projection_repair(a, tol=tol)
    x = m3.projection_repair(a, tol=tol)
    d = max(abs(r[i][j]-x[i][j]) for i in range(4) for j in range(4))
    print(f"tol={tol:g}: reference vs ruled mutant max entry diff={d:.3e}; ref dist={math.sqrt(sum((r[i][j]-a[i][j])**2 for i in range(4) for j in range(4))):.6f}; mutant dist={math.sqrt(sum((x[i][j]-a[i][j])**2 for i in range(4) for j in range(4))):.6f}")
