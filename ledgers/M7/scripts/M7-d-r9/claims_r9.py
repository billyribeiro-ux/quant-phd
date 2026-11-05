"""Round 9: independent recomputation of the numbers in project.html Lab 3, Lab 1 interpretation and test_project.py hand-case comments."""
import sys, importlib.util
from fractions import Fraction as F
GAMMA = F(2)
SIGMA = [[F(4,100), F(1,100), F(0)], [F(1,100), F(9,100), F(2,100)], [F(0), F(2,100), F(16,100)]]
MU = [F(5,100), F(3,100), F(-2,100)]
def stat(w, budget, lower, upper):
    return [GAMMA*sum(SIGMA[i][j]*w[j] for j in range(3)) - MU[i] + budget - lower[i] + upper[i] for i in range(3)]
w = [F(9,11), F(2,11), F(0)]; nu = F(-21,1100); lam = [F(0),F(0),F(9,1100)]; up = [F(0)]*3
A = stat(w, nu, lam, up); print("A stationarity", [str(x) for x in A], "budget gap", sum(w)-1, "budget-only weights", )
flipped = [F(0),F(0),-F(9,1100)]
B = stat(w, nu, flipped, up); print("B stationarity", [str(x) for x in B], "max abs", str(max(abs(x) for x in B)), "dual", str(max(F(0), -min(flipped+up))))
moved = [F(9,11)+F(1,1000), F(2,11)-F(1,1000), F(0)]
C = stat(moved, nu, lam, up); print("C stationarity", [str(x) for x in C], "max abs", str(max(abs(x) for x in C)), "sum-1", str(sum(moved)-1))
# Lab 1 steps: budget-only weights, held asset
def solve(M, r):
    n=len(r); R=[list(M[i])+[r[i]] for i in range(n)]
    for c in range(n):
        p=next(k for k in range(c,n) if R[k][c]!=0); R[c],R[p]=R[p],R[c]
        for k in range(n):
            if k!=c and R[k][c]!=0:
                f=R[k][c]/R[c][c]; R[k]=[x-f*y for x,y in zip(R[k],R[c])]
    return [R[i][n]/R[i][i] for i in range(n)]
M=[[GAMMA*SIGMA[i][j] for j in range(3)]+[F(1)] for i in range(3)]+[[F(1),F(1),F(1),F(0)]]
sol=solve([row[:3]+[row[3]] for row in []] or [[GAMMA*SIGMA[i][j] if j<3 else None for j in range(3)] for i in range(3)], [])  if False else None
# budget-only KKT: gamma*Sigma w - mu + nu*1 = 0, sum w = 1
Mb=[[GAMMA*SIGMA[i][j] for j in range(3)]+[F(1)] for i in range(3)]+[[F(1),F(1),F(1),F(0)]]
x=solve(Mb,[MU[0],MU[1],MU[2],F(1)]); print("budget-only weights", [str(v) for v in x[:3]], "nu", str(x[3]))
