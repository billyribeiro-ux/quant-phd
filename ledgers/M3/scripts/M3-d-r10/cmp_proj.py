import importlib.util, sys, math
sys.path.insert(0, "course/modules/M/M3/grader")
from instance import make_instance
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("course/modules/M/M3/grader/reference.py", "ref")
mut = load("ledgers/M3/mutants/r10d_m03_dykstra_never_updates_unit_correction.py", "mut")
worst = 0.0; worst_seed=None
for s in range(50):
    inst = make_instance(s)
    A = inst.get("pairwise") or inst.get("matrix") or None
    keys = list(inst.keys())
    a = inst["pairwise"] if "pairwise" in inst else None
    if a is None:
        print("keys", keys); break
    r = ref.projection_repair(a); m = mut.projection_repair(a)
    d_r = ref._frobenius(ref._as_matrix(a), r); d_m = ref._frobenius(ref._as_matrix(a), m)
    diff = max(abs(r[i][j]-m[i][j]) for i in range(len(a)) for j in range(len(a)))
    if diff > worst: worst, worst_seed = diff, s
    if s < 3: print(s, "dist ref", round(d_r,9), "dist mut", round(d_m,9), "maxdiff", diff)
print("worst entry diff", worst, "seed", worst_seed)
