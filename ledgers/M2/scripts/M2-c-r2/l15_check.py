import math
# L15 lab recomputation
def f(x,y):
    if x==0 and y==0: return 0.0
    return x*x*y/(x*x+y*y)
def g(x,y):
    if x==0 and y==0: return 0.0
    return x*y/(x*x+y*y)
best=(0,None)
for count_k in range(360):
    th=2*math.pi*count_k/360
    v=abs(f(math.cos(th),math.sin(th)))
    if v>best[0]: best=(v,count_k)
print("f sampled argmax index", best[1], "deg", best[1], "value", repr(best[0]), "exact", 2/(3*math.sqrt(3)))
for deg in (34,35,36,215,325):
    th=math.radians(deg); print(deg, abs(math.cos(th)**2*math.sin(th)))
print(math.degrees(math.asin(1/math.sqrt(3))))
