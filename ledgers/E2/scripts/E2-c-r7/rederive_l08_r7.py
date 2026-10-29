from fractions import Fraction as Fr
def EM(n,a):
    s=Fr(0)
    for x in range(-a,a):
        F=Fr(x+a+1,2*a+1)
        s+= 1-F**n
    return -a+s
v=EM(5,2000); print('EM n5 a2000', v, float(v), float(v)-1333.66656253)
print('EM n2 a1', EM(2,1), 'cont n2 a1', 1*(2-1)/(2+1))
print('cont n5 a2000', Fr(2000*4,6), float(Fr(2000*4,6)))
print('diff', 1333.66656253-1333.3333333, 'rounded', round(1333.66656253-1333.3333333,4))
print('1333-EM', float(1333-v), '1334-EM', float(1334-v))
print('exact total naive -20000*EM', float(-20000*v))
print('shaded exact 20000*(1334-EM)', float(20000*(1334-v)))
print('1334*20000 diff', 59282+26620718, 1334*20000)
print('E3 1334 per auction', float(1334-v), 'total', float(20000*(1334-v)))
print('check 85418692002000/64048012001 =', 85418692002000/64048012001, 'den check', v==Fr(85418692002000,64048012001))
print('se diff', 52613/79810)
print('sim avg naive', -26620718/20000, 'exact per auction', float(-v))
