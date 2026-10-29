import math
from fractions import Fraction as F
def om(p, eta=0.5):
    return p**eta/((p**eta+(1-p)**eta)**(1/eta))
def cf(p): return math.sqrt(p)/(1+2*math.sqrt(p*(1-p)))
print("w.3", repr(om(0.3)), "w.6", repr(om(0.6)), "w.5", repr(om(0.5)), "2/(2sqrt2)", 1/(2*math.sqrt(2)))
print("w1/4", repr(om(0.25)), "2-sqrt3", 2-math.sqrt(3))
print("2*w.3", 2*om(0.3), "w.6", om(0.6))
print("ratio", repr(om(0.3)/om(0.6)), "ratio from printed", 0.28579088/0.39125077)
print("thr a=1", 1/(1+2**-1), "thr a=.5", 1/(1+2**-0.5))
print("w.01", repr(om(0.01)), "w.05", om(0.05), "w.99", repr(om(0.99)), "w.95", om(0.95), "w.6", om(0.6))
for p in (0.01,0.05,0.3,0.5,0.6,0.95,0.99): print("p",p,"w",round(om(p),4),"above" if om(p)>p else "below", om(p)-p)
v1 = 100*om(0.01)+50*om(0.99); print("L value",v1, "EV",0.01*100+0.99*50, "over-adds",(om(0.01)-0.01)*100,"under",(0.99-om(0.99))*50, "net", v1-50.5)
print("8.3403", om(0.01)*100, "41.4925", om(0.99)*50)
# grid
N=1001; grid=[i/(N-1) for i in range(N)]
ch=[om(p)>p for p in grid[1:-1]]
print("sign changes interior", sum(1 for a,b in zip(ch,ch[1:]) if a!=b))
ab=[p for p in grid[1:-1] if om(p)>p]; print("last above", max(ab))
print("p=0.279", om(0.279), 0.279, om(0.279)<0.279, "p=.278", om(0.278)-0.278)
print("gap closed", max(abs(om(p)-cf(p)) for p in grid))
print("eta=1 closed-form gap", max(abs(p - cf(p)) for p in grid))
print("eta=1 omega", om(0.3,1.0), om(0.3,1.0)==0.3)
A=[(0,F(2,5)),(50,F(3,10)),(100,F(3,10))]; B=[(0,F(2,5)),(100,F(3,5))]
for al in (1.0,0.5):
    va=sum(om(float(p))*float(x)**al for x,p in A if x>0); vb=sum(om(float(p))*float(x)**al for x,p in B if x>0)
    print("alpha",al,"GA",repr(va),"GB",repr(vb),"diff",va-vb)
    vae=sum(float(p)*float(x)**al for x,p in A); vbe=sum(float(p)*float(x)**al for x,p in B)
    print(" eta=1 GA GB", vae, vbe)
print("eta1 printed diff", 45-60)
