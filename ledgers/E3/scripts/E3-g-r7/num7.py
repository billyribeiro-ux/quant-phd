from decimal import Decimal as D, getcontext
import math
getcontext().prec = 60
def om(p):
    p = D(p)
    s = (p*(1-p)).sqrt()
    return p.sqrt()/(1+2*s)
def om_f(p):
    return math.sqrt(p)/(1+2*math.sqrt(p*(1-p)))
o310 = om(D(3)/D(10)); o35 = om(D(3)/D(5)); o12 = om(D(1)/D(2)); o25 = om(D(2)/D(5)); o01 = om(D(1)/D(100)); o099 = om(D(99)/D(100))
print('omega(3/10)', o310)
print('omega(3/5)', o35)
print('omega(1/2)', o12, '1/(2sqrt2)=', 1/(2*D(2).sqrt()))
print('omega(2/5)', o25)
print('omega(0.01)', o01, 'omega(0.99)', o099)
print('ratio', o310/o35)
print('ratio 8dp quotient', D('0.28579088')/D('0.39125077'))
print('threshold a=1', D(1)/(1+D('0.5')), 'a=1/2', 1/(1+D(2).sqrt()/2*0+1/D(2).sqrt()))
G_A1 = 150*o310; G_B1 = 100*o35
print('Gamma_A(1)', G_A1, 'Gamma_B(1)', G_B1, 'diff', G_A1-G_B1)
G_A05 = o310*(D(50).sqrt()+D(100).sqrt()); G_B05 = o35*D(100).sqrt()
print('Gamma_A(.5)', G_A05, 'Gamma_B(.5)', G_B05)
print('8dp gamma A', o310*150, 'gamma B', o35*100)
print('weights sum', o25 + 2*o310)
print('2 o310', 2*o310)
print('M-mis: 100*o12', 100*o12)
print('misconception L:', o01*100 + o099*50, 50.5, (o01-D('0.01'))*100, (D('0.99')-o099)*50)
print('omega(1/4)', om(D(1)/D(4)), 2-D(3).sqrt())
print('mis L 8dp:', D('0.0834030105')*100 + D('0.8298494764')*50)
# grid checks (float)
grid = [i/1000 for i in range(1001)]
ints = [p for p in grid[1:-1] if om_f(p) > p]
print('last above', max(ints), 'count above', len(ints), 'first', min(ints))
signs = [om_f(p) > p for p in grid[1:-1]]
print('sign changes', sum(1 for a,b in zip(signs, signs[1:]) if a!=b))
print('omega(0.279)', om_f(0.279), 0.279, 'omega(0.278)', om_f(0.278))
for p in (0.01,0.05,0.3,0.5,0.6,0.95,0.99):
    print(p, om_f(p), om_f(p) > p)
print('closed-form largest gap float grid max:', max(abs(om_f(p)-math.sqrt(p)/(1+2*math.sqrt(p*(1-p)))) for p in grid))
# eta=1 gap
gaps = [(abs(p - om_f(p)), p) for p in grid]
print('eta=1 closed-form gap max (p-closed):', max(gaps))
print('closed vs p at 0.862:', 0.862-om_f(0.862))
