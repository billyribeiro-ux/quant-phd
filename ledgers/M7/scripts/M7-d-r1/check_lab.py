from fractions import Fraction as F
G=F(2); S=[[F(4,100),F(1,100),F(0)],[F(1,100),F(9,100),F(2,100)],[F(0),F(2,100),F(16,100)]]
mu=[F(5,100),F(3,100),F(-2,100)]
def res(w,nu,lo,up):
    st=[G*sum(S[i][j]*w[j] for j in range(3))-mu[i]+nu-lo[i]+up[i] for i in range(3)]
    return st
w=[F(9,11),F(2,11),F(0)]; nu=F(-21,1100); lam=[F(0),F(0),F(9,1100)]
print("A stat", res(w,nu,lam,[0,0,0]))
print("B stat", res(w,nu,[0,0,-F(9,1100)],[0,0,0]))
m=[F(9,11)+F(1,1000),F(2,11)-F(1,1000),F(0)]
print("C stat", res(m,nu,lam,[0,0,0]), "budget", sum(m)-1)
print("obj", F(1)*sum(S[i][j]*w[i]*w[j] for i in range(3) for j in range(3)) - sum(mu[i]*w[i] for i in range(3)), float(F(-3,220)))
# check budget-only solution: 2 Sigma w - mu + nu 1 = 0, sum w=1
import itertools
# solve 4x4
A=[[G*S[i][j] for j in range(3)]+[F(1)] for i in range(3)]+[[F(1),F(1),F(1),F(0)]]
b=[mu[0],mu[1],mu[2],F(1)]
import copy
M=[A[i]+[b[i]] for i in range(4)]
for c in range(4):
    p=next(r for r in range(c,4) if M[r][c]!=0); M[c],M[p]=M[p],M[c]
    for r in range(4):
        if r!=c and M[r][c]!=0:
            f=M[r][c]/M[c][c]; M[r]=[x-f*y for x,y in zip(M[r],M[c])]
print("budget-only", [str(M[i][4]/M[i][i]) for i in range(3)], "nu", str(M[3][4]/M[3][3]))
