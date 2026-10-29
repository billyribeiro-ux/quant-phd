import math
c = 1 + math.cos(0.5)
print("grad y", c, "length", math.sqrt(1+c*c), "angle deg", math.degrees(math.atan(c)), math.degrees(math.atan2(c,1)))
L = math.sqrt(1+c*c)
e = (1/L, c/L)
print("g/|g|", e)
s = e[1]
v = (e[0]/s, e[1]/s)
print("rescaled sup-norm unit dir", v, "value", v[0]+c*v[1], "g.v", 1*v[0]+c*v[1])
print("sup-norm max of u1+c u2 over square", 1+c)
print("R1 0.5326+1.8776 =", 0.5326+1.8776)
# E3 delta
ang = math.degrees(math.atan2(c,1))
print("delta deg", 62-ang, "rad", math.radians(62-ang), "1-cos", 1-math.cos(math.radians(62-ang)), "times |g|", L*(1-math.cos(math.radians(62-ang))))
# lab
import importlib.util
src=open("tests/labs/M2/lab-M2-L17-1.py").read().replace("\nmain()\n","\n")
ns={"__name__":"x"}; exec(compile(src,"l17","exec"),ns)
worst=0; bestv=-1e9; ba=0
for ang2 in range(360):
    u=ns["unit"](ang2); num=ns["directional_central"]((1.0,0.5),u,1e-6)
    ex=1*u[0]+ (1+math.cos(0.5))*u[1]
    worst=max(worst,abs(num-ex))
    if num>bestv: bestv=num; ba=ang2
print("lab worst err", worst, "best angle", ba, "best val", bestv, "gap to L", abs(bestv-L))
# R2 check of partial and directional
f=lambda x,y: 0 if x==0 and y==0 else x*x*y/(x*x+y**4)
for th in (0.3,1.0):
    t=1e-6; u=(math.cos(th),math.sin(th)); print("R2 D_u", th, f(t*u[0],t*u[1])/t, math.sin(th))
