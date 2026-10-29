from fractions import Fraction as Fr
import itertools, math
def EM(n,a):
    t=Fr(-a)
    for x in range(-a,a):
        t+= 1-Fr(x+a+1,2*a+1)**n
    return t
def enum(n,a):
    vals=range(-a,a+1); tup=list(itertools.product(vals,repeat=n))
    return Fr(sum(max(t) for t in tup),len(tup))
def hu(x): return math.floor(x+Fr(1,2))
e=EM(5,2000)
print('EM(5,2000)=',e, float(e))
print('claimed 85418692002000/64048012001 equal:', e==Fr(85418692002000,64048012001))
print('EM(2,1)=',EM(2,1),'enum',enum(2,1),'EM(3,1)=',EM(3,1),'EM(2,2)',EM(2,2),'enum(2,2)',enum(2,2),'EM(3,2)',EM(3,2),enum(3,2))
print('cont 4000/3 =',Fr(4000,3), float(Fr(4000,3)), 'diff', float(e-Fr(4000,3)), '1334-EM', float(1334-e), '1333-EM', float(1333-e))
print('diff decimal', 1333.66656253-1333.33333333)
print('exact naive total -20000*EM', float(-20000*e), 'half_up', hu(-20000*e))
print('exact shaded 20000*(1334-EM)', float(20000*(1334-e)), hu(20000*(1334-e)))
print('shade', hu(e))
print('1334-EM per auction', float(1334-e), 'total', float(20000*(1334-e)))
print('1333-EM', float(1333-e), float(1333-e)*1)
print('R1 n2a1 cont',Fr(1*1,3), 'disc', EM(2,1), 'diff', EM(2,1)-Fr(1,3))
print('M2 n3a1', EM(3,1))
print('52613/79810', 52613/79810, 'per-auction SE', 79810/20000, 'naive avg', -26620718/20000, 'diff', -26620718+26673331)
print('E1 unrounded total diff', float(-20000*e))
print('E3 6668.749', float(20000*(1334-e)))
print('E2 share 228/256',228/256)
print('check EM(4-case?) not needed')
