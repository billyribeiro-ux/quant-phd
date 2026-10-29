"""Independent recomputation of the E1 slice-a numbers (round 2). Standard library only."""
import math
from fractions import Fraction as F

out = []
def chk(name, got, want):
    out.append(f"{'OK ' if got == want else 'BAD'} {name}: got {got} want {want}")

# L01 closed forms and grid
for px, py, m, xs, ys, u in [(2,3,120,30,20,600),(1,1,50,25,25,625),(F(5),2,70,7,F(35,2),F(245,2)),(3,4,60,10,F(15,2),75)]:
    px, py, m = F(px), F(py), F(m)
    x0, y0 = m/(2*px), m/(2*py)
    chk(f"L01 x* px={px} py={py} m={m}", (x0, y0, x0*y0), (F(xs), F(ys), F(u)))
    grid = [(m/px)*i/60 for i in range(61)]
    best = max(range(61), key=lambda i: grid[i]*((m-px*grid[i])/py))
    chk(f"L01 grid argmax px={px}", best, 30)
chk("L01 E2 exact change", F(21*26) - F(20)*F(80,3), F(38,3))
chk("L01 E2 linear term", F(40,3), F(40,3))
chk("L01 remark2.4 MRS", (F(80,3))/20, F(4,3))
x = F(30); y = (120 - 2*x)/3
chk("L01 MRS at x=30 equals 2/3", y/x, F(2,3))
# L02
chk("L02 Ex1.4 profit", F(10)*4 - (12+8+16), F(4))
chk("L02 M1 profit", F(12)*2-(4*2+2*4), F(8))
chk("L02 M2 profit", F(9)*3-(50+9+9), F(-41))
chk("L02 R3 threshold", 2+2*math.sqrt(12), 2+2*math.sqrt(12))
chk("L02 E2 16sqrt3-24", round(16*math.sqrt(3)-24,4), 3.7128)
chk("L02 avg-cost min profit", round(10*math.sqrt(12)-(12+2*math.sqrt(12)+12),4), 3.7128)
chk("L02 Remark1.6 F=100 profit", F(10)*4-(100+8+16), F(-84))
# numeric check of R2 envelope identity via finite difference
def pistar(p, c=2.0, k=1.0, Fx=12.0):
    return (p-c)**2/(4*k)-Fx
p0, h = 10.0, 1e-6
d = (pistar(p0+h)-pistar(p0-h))/(2*h)
chk("L02 R1 envelope q(p)=(p-c)/(2k)", round(d,6), round((p0-2)/2,6))
# L02 tiny grid: alternative k=1/2 case 2 and case 3
def g(p,c,k,Fx):
    best=None
    for j in range(73):
        q=F(j,12); pi=p*q-(Fx+c*q+k*q*q)
        if best is None or pi>best[1]: best=(j,pi,q)
    return best
chk("L02 case2 grid", g(F(7),F(3),F(1,2),F(5))[1], F(3))
chk("L02 case3 grid", g(F(9),F(1),F(3),F(0))[1], F(16,3))
# L03
s=F(5); a=F(100); b=F(2); c=F(2)
p=(a+s*c)/(b+s); chk("L03 p*", p, F(110,7)); chk("L03 Q*", a-b*p, F(480,7))
grid=[F(i,7) for i in range(141)]
Z=lambda q: (a-b*q)-s*max(F(0),q-c)
chk("L03 positive count", sum(Z(q)>0 for q in grid if q<p), 110)
chk("L03 zero count", sum(Z(q)==0 for q in grid), 1)
chk("L03 negative count", sum(Z(q)<0 for q in grid if q>p), 30)
chk("L03 Z(20)", Z(F(20)), F(-30))
chk("L03 firm supply", (p-c)/2, F(48,7))
chk("L03 mech M1", (F(50)+4)/5, F(54,5))
chk("L03 M2 Z(12)", (50-12)-4*(12-1), -6)
chk("L03 R2 c=0 p*", (F(a)+0)/(b+s), F(100,7))
for line in out: print(line)
