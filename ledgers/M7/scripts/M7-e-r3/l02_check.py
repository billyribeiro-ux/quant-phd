from fractions import Fraction as F
A=[[1,2,3],[1,-1,2],[-1,-1,0]]
n=3
S=[[sum(A[k][i]*A[k][j] for k in range(n))+(1 if i==j else 0) for j in range(n)] for i in range(n)]
print("Sigma",S)
def solve(M,b):
    M=[[F(x) for x in row]+[F(bb)] for row,bb in zip(M,b)]
    for c in range(n):
        p=next(r for r in range(c,n) if M[r][c]!=0)
        M[c],M[p]=M[p],M[c]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]/M[c][c]
                M[r]=[a-f*bb for a,bb in zip(M[r],M[c])]
    return [M[i][n]/M[i][i] for i in range(n)]
u=solve(S,[1,1,1]); s=sum(u); lam=1/s
w=[lam*x for x in u]
print("u",u,"s",s,"lambda",lam,"w",w,"budget",sum(w))
Sw=[sum(S[i][j]*w[j] for j in range(n)) for i in range(n)]
print("Sw-lam1",[x-lam for x in Sw])
f=F(1,2)*sum(w[i]*S[i][j]*w[j] for i in range(n) for j in range(n))
print("f(w)",f,"lam/2",lam/2)
# increase identity over six directions with 1'd=0 and six steps
dirs=[(1,-1,0),(0,1,-1),(1,0,-1),(2,-1,-1),(-1,2,-1),(1,1,-2)]
ok_id=ok_nn=0; tot=0
for d in dirs:
    dd=sum(d); assert dd==0
    dSd=sum(d[i]*S[i][j]*d[j] for i in range(n) for j in range(n))
    for t in [F(1),F(-1),F(2),F(1,2),F(-3,2),F(3)]:
        wt=[w[i]+t*d[i] for i in range(n)]
        ft=F(1,2)*sum(wt[i]*S[i][j]*wt[j] for i in range(n) for j in range(n))
        inc=ft-f
        tot+=1
        ok_id+= (inc==F(1,2)*t*t*dSd); ok_nn+=(inc>=0)
print("identity holds",ok_id,"of",tot,"nonneg",ok_nn)
# also check the 'six directions' are what the lab uses: see labout

# Problem M2 (diag(1,2), budget): u, s, lambda, w*, f(w*), gradient, and M3 increase
Sd=[[F(1),F(0)],[F(0),F(2)]]
ud=[F(1),F(1,2)]; sd=sum(ud); ld=1/sd; wd=[ld*x for x in ud]
fd=F(1,2)*sum(wd[i]*Sd[i][j]*wd[j] for i in range(2) for j in range(2))
print("M2 u",ud,"s",sd,"lambda",ld,"w*",wd,"f(w*)",fd,"Sigma w*",[Sd[i][i]*wd[i] for i in range(2)])
dd=[F(1),F(-1)]; w1=[wd[0]+dd[0],wd[1]+dd[1]]
f1=F(1,2)*sum(w1[i]*Sd[i][j]*w1[j] for i in range(2) for j in range(2))
inc=f1-fd
print("M3 f(w*+d)",f1,"increase",inc,"formula 1/2 d'Sd d",F(1,2)*sum(dd[i]*Sd[i][j]*dd[j] for i in range(2) for j in range(2)))
