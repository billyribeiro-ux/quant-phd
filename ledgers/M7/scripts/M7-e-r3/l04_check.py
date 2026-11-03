from fractions import Fraction as F
S=[[F(2),F(1)],[F(1),F(2)]]
Si=[[F(2,3),F(-1,3)],[F(-1,3),F(2,3)]]
mu=(F(3,2),F(1,5))
def g(lam,nu):
    r=[mu[i]+lam[i]-nu for i in range(2)]
    q=sum(r[i]*Si[i][j]*r[j] for i in range(2) for j in range(2))
    return -q/2-nu
def f(w): 
    q=sum(w[i]*S[i][j]*w[j] for i in range(2) for j in range(2))/2
    return q-(mu[0]*w[0]+mu[1]*w[1])
dual=[]
for a in range(11):
  for b in range(11):
    for c in range(-10,1):
      dual.append(((F(a,10),F(b,10)),F(c,10)))
prim=[(F(k,20),1-F(k,20)) for k in range(21)]
print("dual points",len(dual),"primal",len(prim),"pairs",len(dual)*len(prim))
ok=sum(1 for (l,n) in dual for w in prim if g(l,n)<=f(w))
print("weak duality pairs holding",ok)
mx=max(g(l,n) for (l,n) in dual)
print("max dual",mx,"attained at",[(l,n) for (l,n) in dual if g(l,n)==mx])
print("min primal grid",min(f(w) for w in prim),[w for w in prim if f(w)==min(f(x) for x in prim)])
print("g(0,0)",g((F(0),F(0)),F(0)),"diff",g((F(0),F(0)),F(0))+F(1,2))
print("g at lam=(0,3/10),nu=-1/2",g((F(0),F(3,10)),F(-1,2)))
print("R3: g(0,nu) at -3/5,-7/10,-13/20:",g((F(0),F(0)),F(-3,5)),g((F(0),F(0)),F(-7,10)),g((F(0),F(0)),F(-13,20)))
# grid max over nu with lam=(0,0)
grid_nu=[F(-k,10) for k in range(11)]
gm=max(g((F(0),F(0)),n) for n in grid_nu)
print("R3 grid max (lam=0)",gm,"grid gap", F(-1,2)-gm)
# Example 2.2 closed-form equal
print("gap via R3 claim 7/300:", F(-1,2)-(-F(157,300)), F(7,300))
# dual value at (1/2,1/2)
print("f(1/2,1/2)",f((F(1,2),F(1,2))))
print("E2 -199/300 =",float(F(-199,300)), "minus p*", F(-199,300)+F(1,2))
