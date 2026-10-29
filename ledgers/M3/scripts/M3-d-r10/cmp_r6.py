import importlib.util, random
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("course/modules/M/M3/grader/reference.py", "ref")
mut = load("ledgers/M3/mutants/r6d_m04_projection_stops_on_gap_only.py", "mut")
rng = random.Random(7); worst=(0,None); worst_psd=(1,None)
for trial in range(200):
    n = rng.choice([3,4,5])
    A = [[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            v = rng.uniform(-0.99,0.99); A[i][j]=A[j][i]=v
    r = ref.projection_repair(A); m = mut.projection_repair(A)
    d = max(abs(r[i][j]-m[i][j]) for i in range(n) for j in range(n))
    ml = ref.min_eigenvalue(m)
    if d > worst[0]: worst=(d,trial,n)
    if ml < worst_psd[0]: worst_psd=(ml,trial)
print("max entry diff vs reference:", worst, " min eig of mutant output (worst):", worst_psd)
