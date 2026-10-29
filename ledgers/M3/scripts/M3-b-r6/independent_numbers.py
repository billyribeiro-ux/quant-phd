import math
import numpy as np

# L04 Example 2.6 and Remark 2.7
A = np.array([[2.0, 1.0], [1.0, 2.0]])
Q = np.array([[1, 1], [1, -1]]) / math.sqrt(2)
L = np.diag([3.0, 1.0])
print("L04 Ex2.6 QLQt == A:", np.allclose(Q @ L @ Q.T, A))
y = Q.T @ np.array([1.0, 0.0]); print("L04 Ex2.6 y^T L y:", float(y @ L @ y))
v = np.array([1.0, 0.0]); w = np.array([1.0, 1.0]) / math.sqrt(2)
print("L04 Remark2.7 |<e1, (1,1)/sqrt2>|:", round(abs(float(v @ w)), 4), 1 / math.sqrt(2))
# L04 M1 eigenvectors of [[4,1],[1,3]]
B4 = np.array([[4.0, 1.0], [1.0, 3.0]])
s5 = math.sqrt(5)
vv = np.array([1.0, (-1 + s5) / 2]); ww = np.array([1.0, (-1 - s5) / 2])
print("L04 M1 <v,w>:", float(vv @ ww), "eig check:", np.allclose(B4 @ vv, (7 + s5) / 2 * vv), np.allclose(B4 @ ww, (7 - s5) / 2 * ww))
# L05 Example 2.5 factor
B = np.diag([math.sqrt(3), 1.0]) @ Q.T
print("L05 Ex2.5 B^TB:", np.round(B.T @ B, 12).tolist())
# L05 Part B: grid counts over 360 angles, form = c^2 + 4cs + s^2
ts = [2 * math.pi * k / 360 for k in range(360)]
vals = [math.cos(t) ** 2 + 4 * math.cos(t) * math.sin(t) + math.sin(t) ** 2 for t in ts]
print("L05 PartB neg(<-1e-10):", sum(v < -1e-10 for v in vals), "zero:", sum(abs(v) <= 1e-10 for v in vals), "min:", round(min(vals), 4))
print("L05 E2 analytic interval count 106..164 + 286..344:", len(range(106, 165)) + len(range(286, 345)), 118 / 360)
# L05 Remark 3.2 eigenvalues of G
Bg = np.array([[1.0, 0, 1], [0, 1, 1]]); G = Bg.T @ Bg
print("L05 R3.2 eig:", np.round(np.linalg.eigvalsh(G), 12).tolist(), "(1,1,-1) in null B:", (Bg @ np.array([1, 1, -1])).tolist())
# L06 seed-0 singular values via independent route (sqrt eig of A^T A)
a0 = np.random.default_rng(0).normal(size=(4, 3))
print("L06 seed0 sv via eig:", np.round(np.sqrt(np.linalg.eigvalsh(a0.T @ a0))[::-1], 4).tolist(),
      "svd:", np.round(np.linalg.svd(a0, compute_uv=False), 4).tolist())
# L06 M1, E3, M2, Frobenius quiz
print("L06 E3 sv:", math.sqrt(25), "L06 quiz Fro 1,2;3,4:", float(np.sum(np.array([[1, 2], [3, 4]]) ** 2)))
print("L06 M2 eig of [[1,1],[1,1]]:", np.round(np.linalg.eigvalsh(np.array([[1.0, 1], [1, 1]])), 12).tolist())
# L06 Remark 2.5: swap matrix
P = np.array([[0.0, 1], [1, 0]]); print("L06 R2.5 P I P^T = I:", np.allclose(P @ np.eye(2) @ P.T, np.eye(2)))
# L05 quiz [[2,1],[1,2]] eig, [[1,2],[2,4]] eig (L05 M2)
print("L05 M2 eig [[1,2],[2,4]]:", np.round(np.linalg.eigvalsh(np.array([[1.0, 2], [2, 4]])), 12).tolist())
print("L05 M3 eig [[3,-1],[-1,3]]:", np.round(np.linalg.eigvalsh(np.array([[3.0, -1], [-1, 3]])), 12).tolist())
