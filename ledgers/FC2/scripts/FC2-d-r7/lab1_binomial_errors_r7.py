import math
S=K=100.0; r=0.05; s=0.2; tau=1.0
def bs():
    d1=(math.log(S/K)+(r+s*s/2)*tau)/(s*math.sqrt(tau)); d2=d1-s*math.sqrt(tau)
    Phi=lambda x: 0.5*(1+math.erf(x/math.sqrt(2)))
    return S*Phi(d1)-K*math.exp(-r*tau)*Phi(d2)
def binom(n):
    h=tau/n; u=math.exp(s*math.sqrt(h)); d=1/u; R=math.exp(r*h); q=(R-d)/(u-d)
    from math import comb
    return math.exp(-r*tau)*sum(comb(n,k)*q**k*(1-q)**(n-k)*max(S*u**k*d**(n-k)-K,0) for k in range(n+1))
b=bs()
print("BS", b)
for n in [1,2,5,10,25,50,100,200,400]:
    print(n, binom(n)-b)
