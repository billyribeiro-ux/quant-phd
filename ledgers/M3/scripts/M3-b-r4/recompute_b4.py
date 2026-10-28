import math
import numpy as np
np.set_printoptions(precision=12)
# L06: unrounded singular values of seed-0 4x3 matrix
a0 = np.random.default_rng(0).normal(size=(4, 3))
s0 = np.linalg.svd(a0, compute_uv=False)
print("L06 seed0 s:", repr(s0[0]), repr(s0[1]), repr(s0[2]))
print("L06 rounded:", f"{s0[0]:.4f} {s0[1]:.4f} {s0[2]:.4f}")
# independent: eigenvalues of A^T A
ev = np.sort(np.linalg.eigvalsh(a0.T @ a0))[::-1]
print("L06 sqrt eig:", np.sqrt(ev))
# L04 remark 2.7 inner product exact
print("L04 1/sqrt2 =", 1/math.sqrt(2), "rounded", f"{1/math.sqrt(2):.4f}")
# L05 part B: values of 1+2 sin 2t at integer degrees
vals = [1 + 2*math.sin(2*math.radians(k)) for k in range(360)]
neg = [k for k,v in enumerate(vals) if v < -1e-10]
print("L05 neg count", len(neg), "first/last", neg[0], neg[-1], "min", min(vals), "argmin deg", [k for k,v in enumerate(vals) if abs(v+1)<1e-9])
print("L05 zeros", [k for k,v in enumerate(vals) if abs(v)<=1e-10], "118/360=", 118/360)
# L05 Part C: independent check of Gram eig pass count with an alternate algorithm (cholesky-free: check x^T G x via explicit loops on 3 vectors)
# L05 R1 entries
A = np.array([[2.0,1.0],[1.0,2.0]])
Q = np.array([[1,1],[1,-1]])/math.sqrt(2)
L12 = np.diag([math.sqrt(3),1.0])
B = L12 @ Q.T
print("L05 Ex2.5 B:", B*math.sqrt(2)); print("B^TB:", B.T@B)
# L04 M3 check, L05 M3 eigen, L06 M2/E3
print("L06 E3 AtA eig", np.linalg.eigvalsh(np.array([[9.,12.],[12.,16.]])))
print("L06 M2 AtA eig", np.linalg.eigvalsh(np.array([[1.,1.],[1.,1.]])))
print("L05 M2 eig", np.linalg.eigvalsh(np.array([[1.,2.],[2.,4.]])), "x^TAx", np.array([2,-1])@np.array([[1.,2.],[2.,4.]])@np.array([2,-1]))
print("L05 M3 eig", np.linalg.eigvalsh(np.array([[3.,-1.],[-1.,3.]])))
print("L04 M1 eig/ip", np.linalg.eigh(np.array([[4.,1.],[1.,3.]])))
print("L06 quiz Frob", np.sum(np.array([[1.,2.],[3.,4.]])**2), "F(3 4)", 3**2+4**2)
print("L04 R1 z", np.array([[0,-1],[1,0]])@np.array([1,-1j]), np.conj(np.array([1,-1j]))@(np.array([[0,-1],[1,0]])@np.array([1,-1j])))
