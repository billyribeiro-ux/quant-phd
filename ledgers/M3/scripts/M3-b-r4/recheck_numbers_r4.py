"""Independent re-derivation of the numbers in the L04-L06 prose (round 4). Run with python -I."""
import math
from fractions import Fraction as F
import numpy as np

# L05 Part B: form on the unit circle is 1 + 2 sin 2t; grid of 360 angles t = 2*pi*k/360
def form(t):
    c, s = math.cos(t), math.sin(t)
    return c*c + 4*c*s + s*s
vals = [form(2*math.pi*k/360) for k in range(360)]
neg = [k for k, v in enumerate(vals) if v < -1e-10]
zer = [k for k, v in enumerate(vals) if abs(v) <= 1e-10]
print("L05 grid negative count", len(neg), "zero count", len(zer), "zero angles", zer)
print("L05 negative angle range (first, last)", neg[0], neg[-1], "contiguous", neg == list(range(neg[0], neg[-1]+1)))
print("L05 second arc", [k for k in neg if k > 180][:1], [k for k in neg if k > 180][-1:])
print("L05 1+2 sin2t identity max err", max(abs(form(t) - (1+2*math.sin(2*t))) for t in np.linspace(0, 2*math.pi, 1001)))
print("L05 grid min", min(vals), "ratio 118/360 =", round(118/360, 4), "one third =", round(1/3, 4))

# L05 Example 2.5 exact
A = [[F(2), F(1)], [F(1), F(2)]]
B = [[F(1,1)*0 + F(1), F(1)], [F(1), F(-1)]]  # placeholder for shape check
s3 = math.sqrt(3)
Bn = np.array([[s3, s3], [1.0, -1.0]]) / math.sqrt(2)
print("L05 Ex2.5 B^T B =", np.round(Bn.T @ Bn, 12).tolist())

# L05 Example 2.6 and M3 values
print("L05 Ex2.6 eig", np.linalg.eigvalsh(np.array([[1.,2.],[2.,1.]])).tolist())
print("L05 Remark 3.2 eig", np.linalg.eigvalsh(np.array([[1.,0,1],[0,1,1],[1,1,2]])).tolist())
print("L05 M3 eig", np.linalg.eigvalsh(np.array([[3.,-1],[-1,3]])).tolist(), "x=(1,1) form", np.array([1.,1]) @ np.array([[3.,-1],[-1,3]]) @ np.array([1.,1]))
print("L05 M2 eig", np.linalg.eigvalsh(np.array([[1.,2],[2,4]])).tolist())

# L04 Example 2.6 / Remark 2.7 / M1 / M2 / E3
Q = np.array([[1,1],[1,-1]]) / math.sqrt(2)
print("L04 Ex2.6 QLQ^T", np.round(Q @ np.diag([3.,1.]) @ Q.T, 12).tolist(), "y=Q^T e1 =", np.round(Q.T @ np.array([1.,0]), 6).tolist(), "cor value", 3*0.5+1*0.5)
print("L04 M1 inner product", 1 + ((-1+math.sqrt(5))/2)*((-1-math.sqrt(5))/2), "eig", (7+math.sqrt(5))/2, (7-math.sqrt(5))/2)
print("L04 M2 QLQ^T", np.round(np.array([[1,1],[1,-1]])/math.sqrt(2) @ np.diag([5.,-1]) @ (np.array([[1,1],[1,-1]])/math.sqrt(2)).T, 12).tolist())
print("L04 M3 x^TAx direct", np.array([1.,-2]) @ np.array([[2.,1],[1,2]]) @ np.array([1.,-2]), "via y", (3*(1/2)+1*(9/2)))
print("L04 Remark 2.7 inner product 1/sqrt2 =", 1/math.sqrt(2), round(1/math.sqrt(2), 4))
print("L04 R1 z=(1,-i): Rz", np.array([[0,-1],[1,0]]) @ np.array([1,-1j]), "z*Rz", np.conj(np.array([1,-1j])) @ np.array([[0,-1],[1,0]]) @ np.array([1,-1j]))

# L06 seed-0 singular values unrounded, and boundary distance from rounding
a0 = np.random.default_rng(0).normal(size=(4, 3))
s0 = np.linalg.svd(a0, compute_uv=False)
print("L06 seed-0 singular values unrounded", repr(s0[0]), repr(s0[1]), repr(s0[2]))
print("L06 rounding distance to 4th decimal boundary", [abs((x*1e4) % 1 - 0.5) for x in s0])
pl = np.random.default_rng(7).normal(size=(4, 2)) @ np.random.default_rng(8).normal(size=(2, 3))
sp = np.linalg.svd(pl, compute_uv=False)
print("L06 planted singular values", sp.tolist(), "count>1e-10 rel", int(np.sum(sp > 1e-10*sp[0])))
print("L06 M1 svd check", np.round(np.array([[0,1],[1,0]]) @ np.diag([4.,3]) @ np.array([[0,1],[1,0]]), 12).tolist())
print("L06 M2 eig A^TA", np.linalg.eigvalsh(np.array([[1.,1],[1,1]])).tolist())
print("L06 E3 eig", np.linalg.eigvalsh(np.array([[9.,12],[12,16]])).tolist())
print("L06 Q4 Frobenius", np.sum(np.array([[1.,2],[3,4]])**2), "2I_2", np.sum((2*np.eye(2))**2))
print("L06 Misc A=[[0,1],[0,0]] A^TA", (np.array([[0.,1],[0,0]]).T @ np.array([[0.,1],[0,0]])).tolist(), np.linalg.svd(np.array([[0.,1],[0,0]]), compute_uv=False).tolist())
print("L06 Remark 2.5 I2 SVD check", (np.array([[0.,1],[1,0]]) @ np.eye(2) @ np.array([[0.,1],[1,0]]).T).tolist())
print("L04 seeds check: a 4x4 symmetric sample count C(4,2)=", math.comb(4,2), "x200 =", 200*math.comb(4,2))
