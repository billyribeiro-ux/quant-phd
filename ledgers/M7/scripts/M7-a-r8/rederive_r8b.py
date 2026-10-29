from fractions import Fraction as F
# L02 exact solve by Cramer-like elimination via numpy rational check
Sig=[[F(4),F(2),F(5)],[F(2),F(7),F(4)],[F(5),F(4),F(14)]]
def solve3(M,b):
    import copy
    n=3; R=[row[:]+[b[i]] for i,row in enumerate(M)]
    for c in range(n):
        p=next(r for r in range(c,n) if R[r][c]!=0); R[c],R[p]=R[p],R[c]
        for r in range(n):
            if r!=c and R[r][c]!=0:
                f=R[r][c]/R[c][c]; R[r]=[a-f*bb for a,bb in zip(R[r],R[c])]
    return [R[i][n]/R[i][i] for i in range(n)]
u=solve3(Sig,[F(1)]*3); s=sum(u); lam=1/s; w=[lam*x for x in u]
print("L02 s",s,"lambda",lam,"w",w,"f",sum(w[i]*sum(Sig[i][j]*w[j] for j in range(3)) for i in range(3))/2)
print("L02 Sigma w - lambda 1", [sum(Sig[i][j]*w[j] for j in range(3))-lam for i in range(3)])
print("L02 lambda decimal", float(lam))
# L03 grid minima
def f(w1,mu,Sig2=((2,1),(1,2))):
    w=(w1,1-w1)
    q=sum(Sig2[i][j]*w[i]*w[j] for i in range(2) for j in range(2))/2
    return q-(mu[0]*w[0]+mu[1]*w[1])
for mu in [(F(3,2),F(1,5)),(F(1),F(1))]:
    vals=[(f(F(k,100),mu),F(k,100)) for k in range(101)]
    print("L03 mu",mu,"grid min",min(vals)[0],"at",min(vals)[1])
# L03 Example 4.1 values
print("L03 f(1,0)", f(F(1),(F(3,2),F(1,5))), "f(1/2,1/2) inactive", f(F(1,2),(F(1),F(1))))
print("L03 M3 f(1/2,1/2) active", f(F(1,2),(F(3,2),F(1,5))))
print("L03 remark4.3 w", (F(14,15), F(-11,30)), "sum", F(14,15)+F(-11,30))
