import math
gx, gy = 1.0, 1 + math.cos(0.5)
print("grad", gx, gy, "len", math.hypot(gx, gy), "angle deg", math.degrees(math.atan2(gy, gx)))
ang = math.degrees(math.atan2(gy, gx))
d = math.radians(62 - ang)
print("E3 delta deg", 62 - ang, "rad", d, "1-cos", 1 - math.cos(d), "delta^2/2", d*d/2, "|g|(1-cos)", math.hypot(gx,gy)*(1-math.cos(d)))
g = math.hypot(gx, gy)
print("R1 max-norm corner value", 1 + gy, "gradient dir", gx/g, gy/g, "rescaled", (gx/g)/(gy/g), "value", (gx/g)/(gy/g) + gy, "unrounded", (gx/g)/(gy/g) + gy)
# R2 check
import random
def f(x,y): return 0.0 if (x,y)==(0,0) else x*x*y/(x*x+y**4)
for th in (0.3, 1.0):
    u=(math.cos(th), math.sin(th))
    for t in (1e-3,1e-6):
        print("R2 th",th,"t",t,"(f(tu))/t", f(t*u[0],t*u[1])/t, "sin", math.sin(th))
print("R2 partial x at (y^2,y), y=1e-3", (2*(1e-6)*(1e-3)**5)/((1e-6)**2+(1e-3)**4)**2, "1/(2y)", 1/(2*1e-3))
