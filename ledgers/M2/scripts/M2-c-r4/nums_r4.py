import math
from decimal import Decimal, getcontext
getcontext().prec = 40
# L14 E1
e1 = math.exp(math.sin(1))
c1 = math.cos(1)
print("L14 exp(sin1)=", repr(e1), "cos1=", repr(c1))
print("product displayed factors *2:", repr(2.3197768247*0.5403023059*2))
print("unrounded 2 exp(sin1) cos1:", repr(2*e1*c1))
print("unrounded to 12 dp:", f"{2*e1*c1:.12f}")
print("2*exp(sin1)*cos1 rounded at 10 dp:", f"{2*e1*c1:.10f}")
print("f2 chain: 2*exp(sin1)*cos1 at 10dp, 'agrees at 9dp?'", f"{2*e1*c1:.9f}")
# L15: sampled angles
best=(0,None)
for d in range(360):
    t=math.radians(d)
    v=abs(math.cos(t)**2*math.sin(t))
    if v>best[0]+1e-15: best=(v,d)
print("L15 sampled max at integer degrees: ", best, "exact", 2/(3*math.sqrt(3)))
vals=[abs(math.cos(math.radians(d))**2*math.sin(math.radians(d))) for d in (35,145,215,325)]
print("35,145,215,325 values", vals, [round(v,4) for v in vals])
print("integer degree nearest max, and 36:", math.cos(math.radians(36))**2*math.sin(math.radians(36)))
# L14 Example 4.1
x=2.0
print("f(2)", 2*math.exp(2)+math.sin(2)/2, "f'(2)", math.exp(2)+2*math.exp(2)+(2*math.cos(2)-math.sin(2))/4)
# L16 numbers
print("F_x(1,2)", 4+2*math.exp(2), "F_y(1,2)", 1+math.exp(2), "4+e^2", 4+math.exp(2))
print("8e^2", 8*math.exp(2), "e^2", math.exp(2), "1e-16*|F|/1e-5", 1e-16*(4+math.exp(2))/1e-5)
# L17
gx=1.0; gy=1.0+math.cos(0.5)
print("grad", gx, gy, "len", math.hypot(gx,gy), "angle", math.degrees(math.atan2(gy,gx)))
L=math.hypot(gx,gy)
u=(gx/L,gy/L); print("g/|g|", u)
m=max(abs(u[0]),abs(u[1])); s=(u[0]/m,u[1]/m)
print("rescaled", s, "value", s[0]*gx+s[1]*gy, "corner value", gx+gy)
print("L17 unrounded value", s[0]*gx+s[1]*gy)
# L17 Example 2.3 formula check with r.
print("sum", 1+ math.cos(0.5))
# L18 remainder example
for k in (1e-1,1e-2,1e-3,1e-4): pass
