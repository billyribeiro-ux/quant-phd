from fractions import Fraction as F
import math
OUT=15000000; M=5000
def ann(r): return sum((1+r)**-t for t in (1,2,3))
def npv(units, r): return -OUT + sum(F(units*M)*(1+r)**-t for t in (1,2,3)) if False else -F(OUT) + sum(F(units*M)/(F(1+r))**t for t in (1,2,3))
rates={'8':F(8,100),'10':F(10,100),'12':F(12,100)}
be={}
for k,r in rates.items():
    a=sum(1/(1+float(r))**t for t in (1,2,3))
    be[k]=3000/a
    print('rate',k,'annuity',a,'breakeven',be[k])
print('diff 8->10', be['10']-be['8'], 'diff 10->12', be['12']-be['10'])
print('displayed diff 8->10', round(1206.34-1164.10,2), 'displayed diff 10->12', round(1249.05-1206.34,2))
print('displayed-from-unrounded diff', round(be['10']-be['8'],2), round(be['12']-be['10'],2))
print('exact fraction 10%', F(399300,331), float(F(399300,331)))
r10=F(1,10)
A=sum(1/(1+r10)**t for t in (1,2,3))
print('annuity exact 10%', A)
for k,r in rates.items():
    lo=float(npv(200,r)); hi=float(npv(1600,r))
    print(k,'NPV lower',lo,'upper',hi)
print('exact lower 10', float(npv(200,r10)), 'exact upper 10', float(npv(1600,r10)))
print('break-even exact check nums', float(F(3000)/sum(1/(1+r10)**t for t in (1,2,3))))
