"""Round 8: independent Fraction re-derivation of the project lab 1 and lab 2 printed numbers and of the prose numbers."""
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
def r2(x):  # x: Fraction, round half up to 2 decimals
    return (Decimal(x.numerator)/Decimal(x.denominator)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
def cents(x): return (Decimal(x.numerator)/Decimal(x.denominator)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
D1 = F(10**7, 100)  # dollars 100000
for name, path in {'falling': [F(p,100) for p in (100,97,94,91,88,85)], 'rising': [F(p,100) for p in (100,103,106,109,112,115)]}.items():
    print(name, [str(cents(D1/P)) for P in path], 'burden%', str(r2(100*(path[0]/path[-1]-1))))
f5 = D1/F(85,100); r5 = D1/F(115,100)
print('period5 falling exact cents', float(f5*100), 'rising', float(r5*100), 'diff dollars', str(cents(f5-r5)), 'diff exact cents', float((f5-r5)*100))
D2 = F(4*10**6, 100)
path2=[F(p,100) for p in (100,99,98,96,95,93)]
print('lab2', [str(cents(D2/P)) for P in path2], 'burden%', str(r2(100*(path2[0]/path2[-1]-1))))
print('inverted burden', str(r2(100*(path2[-1]/path2[0]-1))), 'burden as ratio of end', str(r2(100*(path2[0]/path2[-1]-1)*0+100*(path2[-1]-path2[0])/path2[-1])))
print('exemplar A 17.65 check', str(r2(100*(F(1)/F(85,100)-1))))
print('exemplar B ratio 2.47/2.79', float(F(247,279)), 'unrounded ratio', 0.024699/0.027935)
