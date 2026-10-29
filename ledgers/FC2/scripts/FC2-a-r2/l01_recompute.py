from fractions import Fraction as F
from itertools import product
X=[[F(1),F(3)],[F(1),F(1)]]
def pay(h,X): return [sum(h[j]*row[j] for j in range(2)) for row in X]
def cost(h,p): return sum(h[j]*p[j] for j in range(2))
def arb(h,p,X):
    c=cost(h,p); r=pay(h,X)
    if c>0 or any(x<0 for x in r): return False
    return c<0 or any(x>0 for x in r)
BOX=range(-10,11); SMALL=range(-2,3)
for name,p in [("consistent",[F(9,10),F(1)]),("mispriced",[F(9,10),F(1,2)])]:
    A=[h for h in product(BOX,BOX) if arb(h,p,X)]
    print(name,"arb in box",len(A), A[:3])
    H=list(product(SMALL,SMALL)); dom=0; bad=0
    for a in H:
        pa=pay(a,X)
        for b in H:
            pb=pay(b,X)
            if all(x>=y for x,y in zip(pa,pb)):
                dom+=1
                if cost(a,p)<cost(b,p): bad+=1
    print(name,"dom",dom,"bad",bad)
# state prices check
for q in [F(1),F(1,2)]:
    pu=(q-F(9,10))/2; pd=F(27,10)-q; pd=pd/2
    print("q",q,"psi",pu,pd, "bond",pu+pd,"stock",3*pu+pd)
