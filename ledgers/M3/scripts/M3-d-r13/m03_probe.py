import sys, importlib.util, math
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB13-M3-d/course/modules/M/M3/grader")
import instance
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("/Users/billyribeiro/.fanout/wt/verifyB13-M3-d/course/modules/M/M3/grader/reference.py", "ref")
mut = load("/Users/billyribeiro/.fanout/wt/verifyB13-M3-d/ledgers/M3/mutants/r13d_m03_projection_unit_diagonal_correction_sign_flipped.py", "mut")
worst = 0.0; worst_pos = 0.0; n_ok = 0
for seed in range(50):
    inst = instance.make_instance(seed) if hasattr(instance, "make_instance") else None
    keys = list(inst.keys()) if isinstance(inst, dict) else None
    if seed == 0: print("instance keys:", keys)
    C = inst["pairwise"] if "pairwise" in inst else None
    if C is None: raise SystemExit("no pairwise key")
    a = ref.projection_repair(C); b = mut.projection_repair(C)
    d = lambda X, Y: math.sqrt(sum((X[i][j]-Y[i][j])**2 for i in range(len(X)) for j in range(len(X))))
    diff = d(a, b)
    worst = max(worst, diff)
    n_ok += 1
print("seeds", n_ok, "max Frobenius |ref - mut| over seeds:", worst)
