# Independent re-derivation of M7 L01-L03 numbers (own code, not the lab twins).
from fractions import Fraction as F
from itertools import product
import numpy as np
# L01: Q2 chord count over grid {-2..2}^2 x weights
G=range(-2,3); W=[F(0),F(1,4),F(1,2),F(3,4),F(1)]
Q2=[[1,2],[2,1]]; Q1=[[2,1],[1,2]]
def qf(Q,x): return sum(Q[i][j]*x[i]*x[j] for i in range(2) for j in range(2))
pts=list(product(G,G))
def chord_ok(Q):
    c=0
    for x in pts:
        for y in pts:
            for w in W:
                z=(w*x[0]+(1-w)*y[0], w*x[1]+(1-w)*y[1])
                if qf(Q,z) <= w*qf(Q,x)+(1-w)*qf(Q,y): c+=1
    return c
print("L01 Q1 chord ok", chord_ok(Q1), "Q2 chord ok", chord_ok(Q2))
neg=sum(1 for x in pts for y in pts if qf(Q2,(x[0]-y[0],x[1]-y[1]))<0)
print("L01 Q2 negative ordered pairs", neg)
print("L01 eig Q1", np.linalg.eigvalsh(np.array(Q1,float)), "eig Q2", np.linalg.eigvalsh(np.array(Q2,float)))
print("L01 Q2 gap at (1,0),(0,1), 1/2:", F(1,2)*qf(Q2,(1,0))+F(1,2)*qf(Q2,(0,1))-qf(Q2,(F(1,2),F(1,2))))
# L02: Sigma from LCG seed 1
st=1; vals=[]
for _ in range(9):
    st=(1103515245*st+12345)%2**31; vals.append(st%7-3)
A=np.array(vals,float).reshape(3,3)
print("L02 A entries", vals)
S=A.T@A+np.eye(3)
print("L02 Sigma\n", S.astype(int))
import sympy as sp
