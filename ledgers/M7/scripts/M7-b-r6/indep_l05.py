"""Independent recomputation of the L05 numbers with sympy-free exact fractions (no lab code reused)."""
from fractions import Fraction as F
import itertools
def det(M):
    n=len(M)
    if n==1: return M[0][0]
    return sum((-1)**j*M[0][j]*det([r[:j]+r[j+1:] for r in M[1:]]) for j in range(n))
Q=[[4,1,0],[1,3,1],[0,1,2]]; A=[[1,1,1],[0,1,-1]]; c=[-1,0,2]; b=[1,0]
K=[[F(Q[i][j]) for j in range(3)]+[F(A[k][i]) for k in range(2)] for i in range(3)]+[[F(A[k][j]) for j in range(3)]+[F(0),F(0)] for k in range(2)]
print("det K", det(K))
# solve K z = (-c, b) by Cramer
rhs=[F(-x) for x in c]+[F(x) for x in b]
D=det(K); sol=[]
for col in range(5):
    M=[row[:] for row in K]
    for r in range(5): M[r][col]=rhs[r]
    sol.append(det(M)/D)
print("x", sol[:3], "lambda", sol[3:])
x=sol[:3]
f=F(1,2)*sum(x[i]*Q[i][j]*x[j] for i in range(3) for j in range(3))+sum(c[i]*x[i] for i in range(3))
print("objective", f, float(f))
v=[-2,1,1]
print("v'Qv", sum(v[i]*Q[i][j]*v[j] for i in range(3) for j in range(3)))
# Part B brute force on grid k/16
Qb=[[2,1],[1,2]]; cb=[-3,1]
def fb(a,bb): return F(1,2)*(Qb[0][0]*a*a+2*Qb[0][1]*a*bb+Qb[1][1]*bb*bb)+cb[0]*a+cb[1]*bb
grid=[F(k,16) for k in range(33)]
vals=[fb(a,bb) for a in grid for bb in grid]
print("grid pts", len(vals), "min", min(vals), "below -9/4", sum(v_<F(-9,4) for v_ in vals))
# Brute force over a finer grid too (k/64 on [0,2]) to test over-claim wording
g2=[F(k,64) for k in range(129)]
print("finer min", min(fb(a,bb) for a in g2 for bb in g2))
