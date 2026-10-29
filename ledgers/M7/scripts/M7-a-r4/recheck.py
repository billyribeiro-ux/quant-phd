from fractions import Fraction as F
from itertools import product
# L01 counts, independent
G=[(a,b) for a in range(-2,3) for b in range(-2,3)]
W=[F(0),F(1,4),F(1,2),F(3,4),F(1)]
def q(Q,x): return sum(Q[i][j]*x[i]*x[j] for i in range(2) for j in range(2))
def comb(l,x,y): return (l*x[0]+(1-l)*y[0], l*x[1]+(1-l)*y[1])
Q1=((2,1),(1,2)); Q2=((1,2),(2,1))
cases=[(x,y,l) for x in G for y in G for l in W]
print('cases',len(cases))
for name,Q in (('Q1',Q1),('Q2',Q2)):
    ident=sum(q(Q,comb(l,x,y))==l*q(Q,x)+(1-l)*q(Q,y)-l*(1-l)*q(Q,(x[0]-y[0],x[1]-y[1])) for x,y,l in cases)
    chord=sum(q(Q,comb(l,x,y))<=l*q(Q,x)+(1-l)*q(Q,y) for x,y,l in cases)
    print(name,'identity',ident,'chord',chord,'fail',len(cases)-chord)
neg=sum(1 for x,y in product(G,G) if q(Q2,(x[0]-y[0],x[1]-y[1]))<0)
print('neg pairs',neg, 'fails==3*neg', len(cases)-sum(q(Q2,comb(l,x,y))<=l*q(Q2,x)+(1-l)*q(Q2,y) for x,y,l in cases)==3*neg)
print('midpoint',q(Q2,(F(1,2),F(1,2))),'chord',F(1,2)*q(Q2,(1,0))+F(1,2)*q(Q2,(0,1)))
print('eig Q1 Hessian 2Q1: trace/det', 2*(2+2), 4*(4-1))
# L02 independent: lcg
def lcg(seed,n):
    s=seed; out=[]
    for _ in range(n):
        s=(1103515245*s+12345)%2**31; out.append(s%7-3)
    return out
e=lcg(1,9); print('entries',e)
A=[e[0:3],e[3:6],e[6:9]]
S=[[sum(A[k][i]*A[k][j] for k in range(3))+(1 if i==j else 0) for j in range(3)] for i in range(3)]
print('Sigma',S)
import sympy
