from decimal import Decimal as D, getcontext
getcontext().prec=60
alpha=D('0.3'); s=D('0.2'); delta=D('0.05'); n=D('0.01'); k0=D('1')
kstar=(s/(n+delta))**(1/(1-alpha))
print('kstar', str(kstar)[:20])
k=k0; first=None
for t in range(1,1001):
    k=(s*(k**alpha)+(1-delta)*k)/(1+n)
    gap=abs(k-kstar)
    if first is None and gap<D('1e-12'): first=t
    if t in (1,2,50,100,500,1000): print(t, str(k)[:16], str(gap)[:14])
print('first', first)
