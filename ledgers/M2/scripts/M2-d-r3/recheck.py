import math
from fractions import Fraction as Fr
# L23 bond: independent recomputation with a different method (direct summation of closed-form derivatives via finite steps and mpmath-free Decimal)
from decimal import Decimal, getcontext
getcontext().prec = 50
c = [Decimal(5000)]*9 + [Decimal(105000)]
def P(y):
    return sum(c[t-1] / (1+y)**t for t in range(1,11))
y0 = Decimal('0.04')
print('P(y0) =', P(y0))
print('round', round(P(y0)))
h = Decimal('1e-12')
P1 = -sum(t*c[t-1]/(1+y0)**(t+1) for t in range(1,11))
P2 = sum(t*(t+1)*c[t-1]/(1+y0)**(t+2) for t in range(1,11))
print("P'  =", P1, ' cd', (P(y0+h)-P(y0-h))/(2*h))
print("P'' =", P2)
for dy in (Decimal('0.01'), Decimal('-0.01'), Decimal('0.005'), Decimal('0.0025')):
    T1 = P(y0) + P1*dy
    T2 = T1 + Decimal('0.5')*P2*dy*dy
    print('shift',dy,'e1',P(y0+dy)-T1,'e2',P(y0+dy)-T2)
print('exact at +0.01', P(y0+Decimal('0.01')), 'at -0.01', P(y0-Decimal('0.01')))
print('-P1/P', -P1/P(y0), 'P2/P', P2/P(y0))
# L24 minimisers
d = 2.220446049250313e-16
print('2sqrt(d/e)=', 2*math.sqrt(d/math.e), ' (3d/e)^(1/3)=', (3*d/math.e)**(1/3))
print('half ulp near e =', math.ulp(math.e)/2)
# L24 central/forward truncation at h: exp
for k in range(1,16):
    h=10.0**-k
    fe=abs((math.exp(1+h)-math.exp(1))/h-math.e)
    ce=abs((math.exp(1+h)-math.exp(1-h))/(2*h)-math.e)
    if k in (5,7,8,9): print('k',k,'%.3e %.3e'%(fe,ce))
# L20 midpoint sums with exact fractions (independent formula)
def mid(n):
    xs=[Fr(2*i+1,2*n) for i in range(n)]
    ys=[Fr(2*(2*j+1),2*n) for j in range(n)]  # midpoints of [0,2] with n cells: (2j+1)/n
    ys=[Fr(2*j+1, n) for j in range(n)]
    dx=Fr(1,n); dy=Fr(2,n)
    return sum((x*y+x*x)*dx*dy for x in xs for y in ys)
for n in (1,2,4,8): print('L20 n',n,mid(n), mid(n)-Fr(5,3))
# L22 V' and f_xx
a=1.5; xs=a-1; print('f_xx', -a/(1+xs)**2, '0.5*0.6667*1e-16', 0.5*abs(-a/(1+xs)**2)*1e-16)
print('golden sqrt eps estimate', math.sqrt(2*2.22e-16*(a*math.log(1+0.5)-0.5)/(a/(1.5**2))))
# L21 lab residual formula check at x=1
y=0.6823278038; print('dy/dx formula x=1', -y/(3*y*y+1))
# L19 closed-form numbers
x,yy=0.5,0.25; e=math.exp(x)
print('grad', e*yy+yy*yy, e+2*x*yy, 'hess', e*yy, e+2*yy, 2*x)
