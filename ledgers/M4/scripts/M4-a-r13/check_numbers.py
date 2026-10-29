from fractions import Fraction as F
import math
die=[(F(k),F(1,6)) for k in range(1,7)]
loss=[(F(0),F(19,20)),(F(250000),F(1,20))]
def mom(d,k,c=None):
    c = sum(x*p for x,p in d) if c is None else c
    return sum(((x-c)**k)*p for x,p in d)
print("die mean",mom(die,1,0),"E2",sum(x*x*p for x,p in die),"var",mom(die,2))
print("loss mean",sum(x*p for x,p in loss),"E2",sum(x*x*p for x,p in loss),"var",mom(loss,2))
sk=[(F(0),F(1,2)),(F(1),F(1,4)),(F(2),F(1,8)),(F(10),F(1,8))]
mu=sum(x*p for x,p in sk)
m={k:mom(sk,k,mu) for k in (2,3,4)}
print("mu",mu,"m2",m[2],"m3",m[3],"m4",m[4])
print("skew^2",m[3]**2/m[2]**3, "kurt",m[4]/m[2]**2, float(m[3]/m[2]**1.5), float(m[4]/m[2]**2))
p=F(1,10);q=1-p
print("bern skew^2",(1-2*p)**2/(p*q),"kurt",(1-3*p*q)/(p*q))
bern=[(F(0),q),(F(1),p)]
print("bern m2 check", mom(bern,2), "skew^2 from moments", mom(bern,3)**2/mom(bern,2)**3, "kurt", mom(bern,4)/mom(bern,2)**2)
print("sd loss", math.sqrt(2968750000))
# Phi(1) gaps not in slice
