import importlib.util, sys, random, math
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("course/modules/M/M3/grader/reference.py", "ref")
mut = load("ledgers/M3/mutants/r10d_m03_dykstra_never_updates_unit_correction.py", "mut")
rng = random.Random(1)
worst = (0.0, None)
for trial in range(300):
    n = rng.choice([2,3,4,5])
    B = [[rng.gauss(0,1) for _ in range(n)] for _ in range(n)]
    A = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            A[i][j] = 0.5*(B[i][j]+B[j][i])
    # unit diagonal random symmetric in (-1,1) off-diagonal
    for i in range(n):
        A[i][i]=1.0
        for j in range(i+1,n):
            v = rng.uniform(-0.99,0.99); A[i][j]=A[j][i]=v
    r = ref.projection_repair(A); m = mut.projection_repair(A)
    d = max(abs(r[i][j]-m[i][j]) for i in range(n) for j in range(n))
    dr = ref._frobenius(A, r); dm = ref._frobenius(A, m)
    if d > worst[0]: worst = (d, (trial, n, round(dr,6), round(dm,6)))
print("max entry diff over random unit-diagonal inputs:", worst)
