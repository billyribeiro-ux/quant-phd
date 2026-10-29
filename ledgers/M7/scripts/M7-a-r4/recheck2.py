from fractions import Fraction as F
S=[[F(4),F(2),F(5)],[F(2),F(7),F(4)],[F(5),F(4),F(14)]]
# Cramer's rule for Sigma u = 1
def det(M): return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
D=det(S); u=[]
for c in range(3):
    M=[row[:] for row in S]
    for r in range(3): M[r][c]=F(1)
    u.append(det(M)/D)
s=sum(u); lam=1/s; w=[lam*x for x in u]
print('u',u,'s',s,'lam',lam,'w',w,'sum',sum(w))
Sw=[sum(S[i][j]*w[j] for j in range(3)) for i in range(3)]
print('Sw-lam1',[x-lam for x in Sw])
f=sum(w[i]*Sw[i] for i in range(3))/2
print('f',f, 'lam/2', lam/2)
print('float lam',float(lam), round(float(lam),4))
# L03 grids
def fobj(w1,mu):
    w=(w1,1-w1); Sg=[[2,1],[1,2]]
    sw=(2*w[0]+w[1], w[0]+2*w[1])
    return F(1,2)*(w[0]*sw[0]+w[1]*sw[1])-(mu[0]*w[0]+mu[1]*w[1])
grid=[F(k,100) for k in range(101)]
for mu in ((F(3,2),F(1,5)),(F(1),F(1))):
    vals=[(fobj(g,mu),g) for g in grid]
    m=min(vals); print('mu',mu,'min',m[0],'at',m[1],'count',len(vals), 'candidate',fobj(F(1),mu) if mu[0]==F(3,2) else fobj(F(1,2),mu))
# L03 residual at off-solution
mu=(F(3,2),F(1,5)); w=(F(1,2),F(1,2)); nu=F(-1,2); lam=(F(0),F(3,10))
g=(2*w[0]+w[1]-mu[0], w[0]+2*w[1]-mu[1]); print('stat',(g[0]+nu-lam[0], g[1]+nu-lam[1]))
print('ex4.2 f', F(1,2)*F(3,2)-1 , 'ex4.1 f', F(1,2)*2-F(3,2))
print('P_M2 f(3/5,2/5)', fobj(F(3,5),(F(1),F(1))), 'M3 grad', (F(3,2)-F(3,2), F(3,2)-F(1,5)), 'M3 f', fobj(F(1,2),mu))
