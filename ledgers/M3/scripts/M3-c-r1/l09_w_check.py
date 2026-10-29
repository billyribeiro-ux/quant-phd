# Checks whether the alternating-projection outputs W are exactly feasible, and tests the L08 R3 zero-column counterexample.
import numpy as np, sys
sys.argv = ["x"]
src = open("/tmp/verifyB1-M3-c/tests/labs/M3/lab-M3-L09-1.py").read().split("def main()")[0]
exec(src)
mats = seeded_matrices(N_MATRICES, SIZE, SEED)
mins = []; asym = []; diag = []
for a in mats:
    if float(np.linalg.eigvalsh(a)[0]) >= -NONPSD_TOL:
        continue
    w = alternating_projections(a)
    mins.append(float(np.linalg.eigvalsh(w)[0])); asym.append(float(np.max(np.abs(w-w.T)))); diag.append(float(np.max(np.abs(np.diag(w)-1))))
print("W min eigenvalue over 23: min", min(mins), "max", max(mins), "count negative", sum(m < 0 for m in mins))
print("W asymmetry max", max(asym), "diag dev max", max(diag))
# L08 R3 counterexample: F with a zero (centred) column
F = np.column_stack([np.array([1.,-1,0,0]), np.array([0.,0,1,-1]), np.zeros(4)])
B = np.eye(3)  # orthonormal columns
M = B @ (F.T @ F / 3) @ B.T
print("R3 counterexample nonzero eigenvalues of M:", np.round(np.linalg.eigvalsh(M)[np.abs(np.linalg.eigvalsh(M))>1e-12],6), "count", int(np.sum(np.abs(np.linalg.eigvalsh(M))>1e-12)))
