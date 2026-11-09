import math
from math import erf, exp, log, sqrt, pi
def Phi(x): return 0.5*(1+erf(x/sqrt(2)))
def phi(x): return exp(-x*x/2)/sqrt(2*pi)
S=100.0; K=100.0; r=0.05; sig=0.2; tau=1.0
d1=(log(S/K)+(r+sig*sig/2)*tau)/(sig*sqrt(tau)); d2=d1-sig*sqrt(tau)
C=S*Phi(d1)-K*exp(-r*tau)*Phi(d2)
print("d1=%.9f d2=%.9f Phi(d1)=%.6f Phi(d2)=%.6f" % (d1,d2,Phi(d1),Phi(d2)))
print("BS C=%.9f cents=%.7f" % (C, C*100))
P=C-S+K*exp(-r*tau)
print("put P=%.9f cents=%.7f  Ke^-rt=%.9f" % (P,P*100,K*exp(-r*tau)))
def tree(n, S=100.0,K=100.0,r=0.05,sig=0.2,tau=1.0):
    h=tau/n; u=exp(sig*sqrt(h)); d=1/u; R=exp(r*h); q=(R-d)/(u-d)
    V=0.0
    from math import comb
    for k in range(n+1):
        V+=comb(n,k)*q**k*(1-q)**(n-k)*max(S*u**k*d**(n-k)-K,0)
    return V*exp(-r*tau), u,d,R,q
for n in [1,2,4,5,10,25,50,100,200,400]:
    V,u,d,R,q=tree(n)
    print("n=%4d V=%.8f cents=%.6f err_cents=%.6f err_cur=%.9f" % (n,V,V*100,(V-C)*100,V-C))
V,u,d,R,q=tree(1); print("n=1 u=%.9f d=%.9f R=%.9f q=%.9f V=%.9f" % (u,d,R,q,V))
V,u,d,R,q=tree(4); print("n=4 u=%.9f d=%.9f R=%.9f q=%.9f V=%.9f" % (u,d,R,q,V))
# six-place inputs for n=4
u6=1.105171; d6=0.904837; R6=1.012578
print("n=4 q six-place inputs = %.9f" % ((R6-d6)/(u6-d6)))
# halvings
W=10-1e-6; tol=1e-10; k=0; w=W
while w>tol: w/=2; k+=1
print("halvings for [1e-6,10], tol 1e-10:", k, " width at 36 =", W/2**36, " at 37 =", W/2**37)
print("ceil log2(W/tol)=", math.ceil(math.log2(W/tol)))
L=max(S-K*exp(-r*tau),0); print("L(K=100)=%.9f  L(K=120)=max(100-120e^-0.05,0)=%.9f" % (S-K*exp(-r*tau), max(S-120*exp(-r*tau),0)))
print("1/37.524 * 0.01 =", 0.01/37.524, " 0.01/37.52 =", 0.01/37.52, " vol points:", 0.01/37.524/0.01, 0.01/37.52/0.01)
print("vega 100 phi(0.35)=%.6f" % (100*phi(0.35)))
print("Phi check: 1/37.524 =", 1/37.524)
