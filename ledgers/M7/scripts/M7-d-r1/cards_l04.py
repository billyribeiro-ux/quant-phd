from fractions import Fraction as F
S=[[F(2),F(1)],[F(1),F(2)]]; mu=[F(3,2),F(1,5)]
Si=[[F(2,3),F(-1,3)],[F(-1,3),F(2,3)]]
def g(l,nu):
    r=[mu[i]+l[i]-nu for i in range(2)]
    q=sum(r[i]*Si[i][j]*r[j] for i in range(2) for j in range(2))
    return -q/2-nu
vals=[(g([F(0),F(0)],F(-k,10)),k) for k in range(0,11)]
best=max(vals)
print("c060: max over nu grid at lambda=0 of g:", best, "gap vs p*=-1/2:", F(-1,2)-best[0])
# dual grid of Lab 2: lambda in {0..1}^2 steps 1/10, nu in [-1,0] steps 1/10
allv=[]
for a in range(11):
  for b in range(11):
    for k in range(11):
      allv.append((g([F(a,10),F(b,10)],F(-k,10)),a,b,k))
mx=max(allv)
cnt=sum(1 for v in allv if v[0]==mx[0])
print("lab2-like grid max g:", mx[0], float(mx[0]), "attained at", cnt, "points; first:", mx[1:], "count of dual points", len(allv))
print("g(0,0) active:", g([F(0),F(0)],F(0)))
