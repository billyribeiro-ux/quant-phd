import importlib.util, random
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
mut = load("ledgers/M3/mutants/r9d_m02_projection_returns_last_psd_iterate.py", "mut")
rng = random.Random(3); worst = 0.0
for trial in range(300):
    n = rng.choice([3,4,5])
    A = [[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            A[i][j]=A[j][i]=rng.uniform(-0.99,0.99)
    m = mut.projection_repair(A)
    worst = max(worst, max(abs(m[i][i]-1.0) for i in range(n)))
print("max diagonal deviation of r9d_m02 output over 300 random inputs:", worst)
