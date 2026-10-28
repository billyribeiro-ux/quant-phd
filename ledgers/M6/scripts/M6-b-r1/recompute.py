from fractions import Fraction as F
import math
# L07 independent recomputation
P=[F(n,16) for n in (1,2,1,3,2,3,2,2)]; X=[F(v) for v in (2,-1,4,0,3,-2,1,5)]
cells=[(0,1,2),(3,4),(5,6,7)]
Y=[None]*8; avgs=[]
for c in cells:
    pb=sum(P[w] for w in c); ex=sum(P[w]*X[w] for w in c); a=ex/pb; avgs.append(a)
    for w in c: Y[w]=a
print("avgs",avgs, "P(cells)",[str(sum(P[w] for w in c)) for c in cells])
mse=sum(P[w]*(X[w]-Y[w])**2 for w in range(8)); print("mse",mse, float(mse))
# minimality over a fine grid of cell-constant functions (exact rationals, step 1/20)
best=None; cnt=0
import itertools
grid=[F(i,20) for i in range(-60,61)]
bestv=None
for t in itertools.product(grid, repeat=3):
    e=sum(P[w]*(X[w]-t[ci])**2 for ci,c in enumerate(cells) for w in c)
    if bestv is None or e<bestv: bestv=e; bt=t
print("grid best",bestv,bt, "exceeds avg mse:", bestv>=mse)
# L05 closed-form integrals (independent): integral over (0,1]x(0,1] of f via sympy-free numeric check
def f(x,y): return (x*x-y*y)/(x*x+y*y)**2
def simpson(g,a,b,n):
    h=(b-a)/n; s=g(a)+g(b)
    for i in range(1,n): s+= (4 if i%2 else 2)*g(a+i*h)
    return s*h/3
# block integral arctan2 - pi/4
print("block", math.atan(2)-math.pi/4)
blk=simpson(lambda x: simpson(lambda y: f(x,y),0.0,0.5,400),0.5,1.0,400)
print("block numeric", blk, blk-(math.atan(2)-math.pi/4))
# blocks k=1,2 numeric (lab does not check these)
for k in (1,2):
    a=0.5**(k+1)
    v=simpson(lambda x: simpson(lambda y: f(x,y),0.0,a,400),a,2*a,400)
    print("block k",k,v, v-(math.atan(2)-math.pi/4))
# L06 density
mu=[F(1,8),F(1,4),F(1,4),F(3,8)]; nu=[F(1,4),F(1,8),F(1,2),F(1,8)]
print("density",[n/m for n,m in zip(nu,mu)])
# L08 biased: expected S_10 under p=1/3
p=F(1,3); print("E S_10 biased", 10*(2*p-1))
