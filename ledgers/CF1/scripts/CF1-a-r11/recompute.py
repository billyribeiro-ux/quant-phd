from decimal import Decimal, getcontext
getcontext().prec=50
r=0.08
flows=[-690,10,0,680]
pv=sum(f/(1+r)**(t+1) for t,f in enumerate(flows))
print('WC PV at 8%', pv)
print('R2 PV', 100*((1+r)**-3-(1+r)**-1))
print('R2 ratio %', 13.2094/100)
print('L02 NPV 8%', sum(f/(1+r)**t for t,f in enumerate([-12000,3135,4360,3600,4130]))) 
print('L02 NPV with sunk', sum(f/(1+r)**t for t,f in enumerate([-12000-2000,3135,4360,3600,4130])))
print('L02 NPV recomputed in dollars: flows -120 base', )
print('L01 A at 0.15', sum(f/100/(1.15)**t for t,f in enumerate([-10000,3000,3200,3400,3600,3800])))
print('L01 A at 0.20', sum(f/100/(1.2)**t for t,f in enumerate([-10000,3000,3200,3400,3600,3800])))
print('L01 A at 0.00', sum(f/100 for f in [-10000,3000,3200,3400,3600,3800]))
print('L01 E at 0.2', sum(f/100/(1.2)**t for t,f in enumerate([-1000,600,600])))
print('P3 A-B at 0.10', 130/1.21-120/1.1, 'A-B diff formula',(1.1**-2)*(10-120*0.1))
print('P3 r=0', 'A',  -100+130/1, 'B', -100+120)
print('P3 at 0.10 A', -100+130/1.21, 'B', -100+120/1.1)
print('P3 at r*', -100+130/(13/12)**2, -100+120/(13/12))
print('misc lines: 1/12 =', 1/12*100)
