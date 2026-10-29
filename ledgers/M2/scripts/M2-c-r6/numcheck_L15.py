import math
s=math.sin(math.radians(35)); print("f/r at 35deg", (1-s*s)*s, "at 36", (1-math.sin(math.radians(36))**2)*math.sin(math.radians(36)))
print("exact", 2/(3*math.sqrt(3)))
for ang in (145,215,325):
    t=math.radians(ang); print(ang, abs(math.cos(t)**2*math.sin(t)))
print("E1 grid argmax:")
best=max(range(360), key=lambda k: abs(math.cos(2*math.pi*k/360)**2*math.sin(2*math.pi*k/360)))
print(best, [k for k in range(360) if abs(abs(math.cos(2*math.pi*k/360)**2*math.sin(2*math.pi*k/360))-abs(math.cos(2*math.pi*best/360)**2*math.sin(2*math.pi*best/360)))<1e-12])
print("g at pi/4 grid", max(abs(math.cos(2*math.pi*k/360)*math.sin(2*math.pi*k/360)) for k in range(360)))
print("R1 along parabola", (1*1)/(1+1))
