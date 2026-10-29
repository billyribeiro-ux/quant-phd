import importlib.util
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("course/modules/M/M3/grader/reference.py", "ref")
mut = load("ledgers/M3/mutants/r10d_m03_dykstra_never_updates_unit_correction.py", "mut")
A = [[1.0, 0.9, -0.9], [0.9, 1.0, 0.9], [-0.9, 0.9, 1.0]]
print(ref.projection_repair(A))
print(mut.projection_repair(A))
print(ref.clip_repair(A))
