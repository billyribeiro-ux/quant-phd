import importlib.util, math, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
root = "/tmp/verifyB1-M5-d/"
ref = load(root+"course/modules/M/M5/grader/reference.py", "ref")
m15 = load(root+"ledgers/M5/mutants/m15_feasibility_strict_drops_the_tie_k_prime_equal_resources.py", "m15")
m16 = load(root+"ledgers/M5/mutants/m16_iteration_starts_from_ones_not_zero.py", "m16")
m18 = load(root+"ledgers/M5/mutants/m18_converged_strictly_below_tol.py", "m18")
P = {"beta": 0.9, "alpha": 0.5}
# m15: state k=1.0 on grid [1.0, 2.0] (k_1 = 1 is feasible from every state by the page's convention)
print("ref  bellman([1,2], [0,0]) =", ref.bellman_operator(P, [1.0, 2.0], [0.0, 0.0]))
print("m15  bellman([1,2], [0,0]) =", m15.bellman_operator(P, [1.0, 2.0], [0.0, 0.0]))
print("m15  solve([1,2]) value =", m15.solve(P, [1.0, 2.0], 1e-6, 5)["value"])
# m16: start from ones, one sweep only: the value is B(1-vector), not B(0)
print("ref  solve max_iter=1 value =", ref.solve(P, [0.5, 0.9, 1.4], 1e-6, 1)["value"])
print("m16  solve max_iter=1 value =", m16.solve(P, [0.5, 0.9, 1.4], 1e-6, 1)["value"])
# m18: tol exactly equal to the certified error of sweep 1 on SMALL grid
G = [0.5, 0.9, 1.4]
b0 = [0.0]*3; b1 = ref.bellman_operator(P, G, b0)
tol = (0.9/(1-0.9)) * max(abs(a-b) for a, b in zip(b1, b0))
r = ref.solve(P, G, tol, 10); s = m18.solve(P, G, tol, 10)
print("tol =", repr(tol), "ref iterations", r["iterations"], r["converged"], "| m18 iterations", s["iterations"], s["converged"])
