import numpy as np, math
from fractions import Fraction
# L04 Example 2.6 and Remark 2.7
A=np.array([[2.,1],[1,2]]); Q=np.array([[1,1],[1,-1]])/math.sqrt(2); L=np.diag([3.,1])
print("L04 Ex2.6 QLQt-A max", np.max(np.abs(Q@L@Q.T-A)), " x'Ax at (1,0):", np.array([1,0])@A@np.array([1,0]))
N=np.array([[1.,2],[0,3]]); w,V=np.linalg.eig(N); print("L04 Rem2.7 eig", sorted(w), "|ip| of normalised", abs(V[:,0]@V[:,1]), 1/math.sqrt(2))
# L04 M1 eigenvectors of [[4,1],[1,3]]
B=np.array([[4.,1],[1,3]]); v=np.array([1,(-1+5**.5)/2]); ww=np.array([1,(-1-5**.5)/2])
print("L04 M1 <v,w>", v@ww, "Av/v:", (B@v)/v, "eig", (7+5**.5)/2,(7-5**.5)/2)
# L04 M2 Q diag(5,-1) Q^T
Q2=np.array([[1,1],[1,-1]])/math.sqrt(2); print("L04 M2", Q2@np.diag([5.,-1])@Q2.T)
# L04 M3
print("L04 M3 x'Ax", np.array([1,-2])@A@np.array([1,-2]))
# L05 Example 2.5 factor and B^TB
Bf=np.diag([3**.5,1])@Q.T; print("L05 Ex2.5 B^TB", Bf.T@Bf)
# L05 Remark 3.2
G=np.array([[1.,0,1],[0,1,1],[1,1,2]]); print("L05 R3.2 eig", np.linalg.eigvalsh(G), "charpoly check at 2:", np.linalg.det(G-2*np.eye(3)), (1-2)*2*(2-3))
# L05 M1,M2,M3
print("L05 M1 eig", np.linalg.eigvalsh(np.array([[2.,1],[1,2]])), "M2 eig", np.linalg.eigvalsh(np.array([[1.,2],[2,4]])), "M3 eig", np.linalg.eigvalsh(np.array([[3.,-1],[-1,3]])))
print("L05 M2 x=(2,-1):", np.array([2,-1.])@np.array([[1.,2],[2,4]])@np.array([2,-1.]))
# L05 Part B exact count and zero set (independent)
vals=[1*math.cos(2*math.pi*k/360)**2+4*math.cos(2*math.pi*k/360)*math.sin(2*math.pi*k/360)+math.sin(2*math.pi*k/360)**2 for k in range(360)]
print("L05 partB negatives", sum(v< -1e-10 for v in vals), "zeros", sum(abs(v)<=1e-10 for v in vals), "min", min(vals), "118/360=", 118/360)
# L05 R1 O_pi B = -B
# L06 seed-0 singular values and Frobenius, M1, M2, E3
a0=np.random.default_rng(0).normal(size=(4,3)); print("L06 seed0 s", np.linalg.svd(a0,compute_uv=False))
print("L06 M1 svd", np.linalg.svd(np.diag([3.,4])))
print("L06 M2 svd", np.linalg.svd(np.array([[1.,1],[0,0]]),compute_uv=False), "E3", np.linalg.svd(np.array([[3.,4]]),compute_uv=False))
print("L06 nilpotent", np.linalg.svd(np.array([[0.,1],[0,0]]),compute_uv=False), np.linalg.eigvals(np.array([[0.,1],[0,0]])))
print("L06 quiz Fro", np.sum(np.array([[1.,2],[3,4]])**2), np.sum((2*np.eye(2))**2))
print("L04 E3 1/sqrt2 =", 1/math.sqrt(2), "rounded", round(1/math.sqrt(2),4))
print("L06 Thm2.3 diag", np.linalg.eigvalsh(np.array([[1.,0,1],[0,1,1],[1,1,2]])))
