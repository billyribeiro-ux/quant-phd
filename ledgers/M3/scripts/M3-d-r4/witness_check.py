import sys, importlib.util
sys.path.insert(0, sys.argv[1])
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("ref", sys.argv[1] + "/reference.py")
mut = load("mut", sys.argv[2])
a = [[-0.5, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
print("reference is_psd(diag(-0.5,1,1), tol=0.5):", ref.is_psd(a, tol=0.5), "min_eig", ref.min_eigenvalue(a))
print("mutant    is_psd(diag(-0.5,1,1), tol=0.5):", mut.is_psd(a, tol=0.5))
