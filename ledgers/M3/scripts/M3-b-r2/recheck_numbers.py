"""Independent recomputation of the numbers printed or stated in M3 L04-L06 (verifier round 2)."""
import math
import numpy as np

# L06: singular values of seed-0 4x3 matrix, unrounded, and rounding check
a0 = np.random.default_rng(0).normal(size=(4, 3))
s = np.linalg.svd(a0, compute_uv=False)
print("L06 seed0 singular values (unrounded):", [repr(float(x)) for x in s])
print("L06 rounded 4dp:", " ".join(f"{x:.4f}" for x in s))
# independent route: sqrt of eigenvalues of a0^T a0 (not SVD)
ev = np.sort(np.linalg.eigvalsh(a0.T @ a0))[::-1]
print("L06 sqrt eig(A^T A):", [f"{math.sqrt(x):.10f}" for x in ev])
# Frobenius identity
print("L06 frob gap:", abs(float(np.sum(s**2)) - float(np.sum(a0*a0))))
# planted rank-2 count, independent threshold check
p = np.random.default_rng(7).normal(size=(4, 2)) @ np.random.default_rng(8).normal(size=(2, 3))
sp = np.linalg.svd(p, compute_uv=False)
print("L06 planted sv:", [f"{x:.3e}" for x in sp], "count above 1e-10*s1:", int(np.sum(sp > 1e-10*sp[0])))
print("L06 count above 1e-6*s1:", int(np.sum(sp > 1e-6*sp[0])), " above 1e-14*s1:", int(np.sum(sp > 1e-14*sp[0])))

# L05 Part B: exact grid count with the closed form 1 + 2 sin 2t
neg = zero = 0
mn = 1e9
for k in range(360):
    t = 2*math.pi*k/360
    v = 1 + 2*math.sin(2*t)
    mn = min(mn, v)
    neg += v < -1e-10
    zero += abs(v) <= 1e-10
print("L05 B negatives:", neg, "zeros:", zero, "min:", round(mn, 6))
# direct quadratic form at unit vectors agrees with closed form
ok = all(abs((math.cos(t)**2 + 4*math.cos(t)*math.sin(t) + math.sin(t)**2) - (1+2*math.sin(2*t))) < 1e-12
         for t in [2*math.pi*k/360 for k in range(360)])
print("L05 closed form agrees:", ok)
# closed form negative set measure: 120 degrees of 360
print("L05 measure fraction:", 120/360, " grid 118/360 =", round(118/360, 4))

# L05 Part C: independent recount with a different solver (eigvals of symmetric matrix via det/minors not needed; use eigvalsh and min Rayleigh quotient)
rng = np.random.default_rng(2604)
pass_eig = pass_form = total = 0
for _ in range(500):
    b = rng.standard_normal((4, 3))
    g = b.T @ b
    lam_min = np.linalg.eigvalsh(g)[0]
    pass_eig += lam_min >= -1e-10
    x = rng.standard_normal((200, 3))
    q = np.sum((x @ g) * x, axis=1)
    nrm = np.sum(x*x, axis=1)
    pass_form += int(np.sum(q >= -1e-10*nrm))
    total += 200
print("L05 C recount: eig pass", pass_eig, "/500; form pass", pass_form, "/", total)

# L04 Remark 2.7 inner product
print("L04 |<(1,0),(1,1)/sqrt2>| =", f"{abs(1/math.sqrt(2)):.8f}")
# L04 Example 2.6 and Lesson 4 numbers
Q = np.array([[1, 1], [1, -1]])/math.sqrt(2); L = np.diag([3.0, 1.0])
print("L04 Ex2.6 QLQ^T:", np.round(Q @ L @ Q.T, 12).tolist(), " x=(1,0): ", float(np.array([1,0]) @ (Q@L@Q.T) @ np.array([1,0])))
# L05 Example 2.5 factor B
B = np.diag([math.sqrt(3), 1.0]) @ Q.T
print("L05 Ex2.5 B^TB:", np.round(B.T @ B, 12).tolist())
# L05 Remark 3.2
G = np.array([[1,0,1],[0,1,1],[1,1,2]], float)
print("L05 R3.2 eig:", np.round(np.linalg.eigvalsh(G), 12).tolist(), "charpoly coeffs:", np.round(np.poly(G), 12).tolist())
# L05 E2 interval endpoints: sin(2t) = -1/2 at 105,165,285,345 deg
print("L05 E2 zeros:", [round(1+2*math.sin(2*math.radians(d)), 12) for d in (105,165,285,345)])
# L06 M1 SVD of diag(3,4)
print("L06 M1 svd diag(3,4):", np.linalg.svd(np.diag([3.0,4.0]), compute_uv=False).tolist())
# L06 E3 one-row
print("L06 E3 sv (3 4):", np.linalg.svd(np.array([[3.0,4.0]]), compute_uv=False).tolist())
# L06 Remark 2.5 V = U = swap gives valid SVD of I2
Sw = np.array([[0.0,1.0],[1.0,0.0]])
print("L06 swap SVD check:", np.allclose(Sw @ np.eye(2) @ Sw.T, np.eye(2)))
# L06 Prop 2.4 example: A = [[1,2],[3,4]] Frobenius
print("L06 quiz frob 30:", float(np.sum(np.array([[1.,2.],[3.,4.]])**2)))
# L04 M2 check Q Lambda Q^T for Lambda=diag(5,-1)
Q2 = np.array([[1,1],[1,-1]])/math.sqrt(2)
print("L04 M2:", np.round(Q2 @ np.diag([5.0,-1.0]) @ Q2.T, 12).tolist())
# L04 M3 quadratic form x=(1,-2)
A3 = np.array([[2.,1.],[1.,2.]]); x3 = np.array([1.,-2.])
print("L04 M3 x^TAx:", float(x3 @ A3 @ x3))
# L05 M3 A=[[3,-1],[-1,3]] eigen and form at (1,1)
print("L05 M3:", np.round(np.linalg.eigvalsh(np.array([[3.,-1.],[-1.,3.]])),12).tolist(), float(np.array([1.,1.]) @ np.array([[3.,-1.],[-1.,3.]]) @ np.array([1.,1.])))
# L04 M1 orthogonality of the two eigenvectors of [[4,1],[1,3]]
v = np.array([1, (-1+5**0.5)/2]); w = np.array([1, (-1-5**0.5)/2])
print("L04 M1 <v,w>:", float(v@w))
print("L04 M1 eig:", np.round(np.linalg.eigvalsh(np.array([[4.,1.],[1.,3.]])),12).tolist())
