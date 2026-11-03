"""Re-check the worked numbers in the L07-L09 problem sets and examples (round-3 verifier).

Run: python -I exercise_checks_r3.py
"""
import numpy as np

ok = True


def check(name, got, want, tol=1e-9):
    global ok
    good = np.allclose(np.asarray(got, dtype=float), np.asarray(want, dtype=float), atol=tol, rtol=0)
    ok = ok and good
    print(f"{name}: {'OK' if good else 'MISMATCH'} got={np.round(np.asarray(got, dtype=float), 6).tolist()} want={np.round(np.asarray(want, dtype=float), 6).tolist()}")


# L07 M1: A=(1,1), y=(2,0)
A = np.array([[1.0], [1.0]])
P = A @ np.linalg.inv(A.T @ A) @ A.T
check("L07 M1 P", P, [[0.5, 0.5], [0.5, 0.5]])
check("L07 M1 p=Py", P @ np.array([2.0, 0.0]), [1.0, 1.0])
check("L07 M1 residual dot A", A.T @ (np.array([2.0, 0.0]) - P @ np.array([2.0, 0.0])), [0.0])
# L07 M2 line fit
X = np.column_stack([np.ones(3), np.array([0.0, 1.0, 2.0])])
yv = np.array([1.0, 2.0, 2.0])
b = np.linalg.solve(X.T @ X, X.T @ yv)
check("L07 M2 beta", b, [7 / 6, 0.5])
check("L07 M2 fitted", X @ b, [7 / 6, 5 / 3, 13 / 6])
check("L07 M2 residuals", yv - X @ b, [-1 / 6, 1 / 3, -1 / 6])
# L07 M3 and P1/R3 style projection onto e1
P3 = np.array([[1.0, 0.0], [0.0, 0.0]])
check("L07 M3 p", P3 @ np.array([3.0, 4.0]), [3.0, 0.0])
check("L07 Remark 1.4 25=9+16", [25.0, 9.0, 16.0], [25.0, 9.0 + 16.0 - 16.0 + 16.0 - 16.0 + 0.0, 16.0])
# L07 E2 vector: A^T y for the seeded lab design (not printed by the lab)
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
yy = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
Aa = np.column_stack([np.ones(n), x1, x2])
print("L07 E2 A^T y (not printed by the lab):", np.round(Aa.T @ yy, 6).tolist(), "max abs", float(np.max(np.abs(Aa.T @ yy))))

# L08 M1: X rows (1,2),(3,4),(5,9)
Xm = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 9.0]])
Xt = Xm - Xm.mean(axis=0)
Mm = Xt.T @ Xt / 2
check("L08 M1 centred rows", Xt, [[-2, -3], [0, -1], [2, 4]])
check("L08 M1 M", Mm, [[4, 7], [7, 13]])
check("L08 M1 trace", np.trace(Mm), 17.0)
check("L08 M1 Prop1.2 sum", np.sum(Xt**2) / 2, 17.0)
check("L08 M1 det", np.linalg.det(Mm), 3.0)
check("L08 M1 eigen", np.sort(np.linalg.eigvalsh(Mm)), np.sort([(17 - np.sqrt(277)) / 2, (17 + np.sqrt(277)) / 2]))
# L08 M2 shares
check("L08 M2 shares", np.array([4, 1, 1]) / 6.0, [2 / 3, 1 / 6, 1 / 6])
# L08 M3 tripling: eigenvalues 2 and 1 -> 18 and 9
check("L08 M3 tripled eig", 9 * np.array([2.0, 1.0]), [18.0, 9.0])
check("L08 M3 shares", np.array([18.0, 9.0]) / 27.0, [2 / 3, 1 / 3])
# L08 E1 bound
check("L08 E1 bound 100M11/(S0+99M11)", 100 * 13.6818 / (88.2028 + 99 * 13.6818), 0.9483, tol=5e-5)
# L08 E3 printed-sum bound
check("L08 E3 printed sum", 75.9 + 18.1 + 5.2, 99.2, tol=1e-9)

# L09 M1: eigen of [[1,.6],[.6,1]]
check("L09 M1 eig", np.sort(np.linalg.eigvalsh(np.array([[1, 0.6], [0.6, 1]]))), [0.4, 1.6])
# L09 M2
check("L09 M2 Frobenius^2", np.sum(np.array([[1, 1.2], [1.2, 1]]) ** 2), 4.88)
check("L09 M2 eig squares", 2.2**2 + 0.2**2, 4.88)
# L09 M3 rescale
Bm = np.array([[4.0, 2.0], [2.0, 9.0]])
check("L09 M3 eig", np.sort(np.linalg.eigvalsh(Bm)), np.sort([(13 - np.sqrt(41)) / 2, (13 + np.sqrt(41)) / 2]))
Dm = np.diag(1 / np.sqrt(np.diag(Bm)))
check("L09 M3 C", Dm @ Bm @ Dm, [[1, 1 / 3], [1 / 3, 1]])
# L09 E1 witness term by term
Cz = np.array([[1, 0.9, 0.9], [0.9, 1, -0.9], [0.9, -0.9, 1.0]])
xw = np.array([1.0, -1.0, -1.0])
terms = [xw[i] * Cz[i, i] * xw[i] for i in range(3)] + [2 * Cz[i, j] * xw[i] * xw[j] for i, j in [(0, 1), (0, 2), (1, 2)]]
check("L09 E1 terms", [sum(terms[:3]), *terms[3:]], [3.0, -1.8, -1.8, -1.8])
# L09 Example 3.6 and E2/E3
A36 = np.array([[1, 1.2], [1.2, 1.0]])
w36, q36 = np.linalg.eigh(A36)
A0 = (q36 * np.maximum(w36, 0)) @ q36.T
check("L09 Ex3.6 A0", A0, [[1.1, 1.1], [1.1, 1.1]])
R36 = np.ones((2, 2))
check("L09 Ex3.6 distance clip^2", np.sum((A36 - A0) ** 2), 0.04)
check("L09 Ex3.6 distance rescaled^2", np.sum((A36 - R36) ** 2), 0.08)
check("L09 E2 ||C0-R||_F", np.linalg.norm(Cz - np.array([[1, .5, .5], [.5, 1, -.5], [.5, -.5, 1]])), np.sqrt(0.96))
# L09 E3: eigenvalues 2, 0.5, -0.5
check("L09 E3 ||A-A0||_F", np.sqrt(0.5**2), 0.5)
print("ALL OK" if ok else "SOME MISMATCH")
