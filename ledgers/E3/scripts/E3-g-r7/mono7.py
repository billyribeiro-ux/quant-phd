import math
def f(p):
    return math.sqrt(p)/(1+2*math.sqrt(p*(1-p)))
N=2_000_000
prev=f(0.0); bad=0; minstep=1e9
for i in range(1,N+1):
    p=i/N
    v=f(p)
    if v < prev: bad+=1
    prev=v
print('non-monotone steps on 2e6-point fine grid:', bad, 'f(1)=', f(1.0))
# analytic derivative sign check: f'(p) proportional to q + 2p^2, q = sqrt(p(1-p))
def fp(p, h=1e-7):
    return (f(p+h)-f(p-h))/(2*h)
for p in (0.01,0.1,0.3,0.5,0.7,0.9,0.99):
    q=math.sqrt(p*(1-p))
    print(p, fp(p) > 0, 'analytic bracket q+2p^2 =', round(q+2*p*p,6))
