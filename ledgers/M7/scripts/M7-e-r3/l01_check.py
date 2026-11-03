from fractions import Fraction as F
from itertools import product
Q1=[[2,1],[1,2]]; Q2=[[1,2],[2,1]]
grid=[(F(a),F(b)) for a,b in product(range(-2,3),repeat=2)]
W=[F(0),F(1,4),F(1,2),F(3,4),F(1)]
def q(Q,x): return sum(x[i]*Q[i][j]*x[j] for i in range(2) for j in range(2))
def comb(l,x,y): return (l*x[0]+(1-l)*y[0], l*x[1]+(1-l)*y[1])
res={}
for name,Q in (("Q1",Q1),("Q2",Q2)):
    ident=0; chord=0; n=0
    for x in grid:
        for y in grid:
            for l in W:
                n+=1
                lhs=l*q(Q,x)+(1-l)*q(Q,y)-q(Q,comb(l,x,y))
                rhs=l*(1-l)*q(Q,(x[0]-y[0],x[1]-y[1]))
                ident+= lhs==rhs
                chord+= (q(Q,comb(l,x,y))<=l*q(Q,x)+(1-l)*q(Q,y))
    print(name,"cases",n,"identity",ident,"chord",chord,"fail",n-chord)
neg=sum(1 for x in grid for y in grid if q(Q2,(x[0]-y[0],x[1]-y[1]))<0)
print("ordered pairs with (x-y)'Q2(x-y)<0:",neg,"3*neg=",3*neg)
x=(F(1),F(0)); y=(F(0),F(1)); l=F(1,2)
print("Q2 example: midpoint value",q(Q2,comb(l,x,y)),"chord",l*q(Q2,x)+(1-l)*q(Q2,y),"chord minus midpoint",l*q(Q2,x)+(1-l)*q(Q2,y)-q(Q2,comb(l,x,y)),"identity term",F(1,4)*q(Q2,(x[0]-y[0],x[1]-y[1])))
print("Q1 eigen 3,1 ; Q2 eigen 3,-1 ; (1,-1)'Q2(1,-1)=",q(Q2,(1,-1)),"(1,1)'Q1(1,1)=",q(Q1,(1,1)))
print("(1,-1)'Q1(1,-1)=",q(Q1,(1,-1)))
print("R1 Q=[[1,1],[-1,1]]: x'Qx = x1^2+x2^2 check:", all(1*x[0]*x[0]+1*x[0]*x[1]-1*x[1]*x[0]+1*x[1]*x[1]==x[0]**2+x[1]**2 for x in grid))
print("L01 M3: q(1,1)=6, gap at lam 1/2 between (1,1),(-1,-1):", F(1,2)*6+F(1,2)*6-0, "Lemma (1/4)(2,2)Q1(2,2)=", F(1,4)*q(Q1,(2,2)))
print("P1 example f=x^2 set {x^2>=1}: 2,-2 in set, midpoint 0 not in set")
print("Example 1.2 circle midpoint of (1,0),(0,1): norm^2", (F(1,2))**2*2)
print("Lab 1 Hessian eigen Q2 2Q2: 6,-2; Q1: 6,2")
print("R3 check a,c>=0 etc skip")
