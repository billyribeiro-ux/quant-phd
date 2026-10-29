import math
e = math.e
d = 2.0**-52
print("ex2.3 fwd lo/hi", e*0.005, e**1.01*0.005)
print("ex2.3 cen lo/hi", math.exp(0.99)*1e-4/6, math.exp(1.01)*1e-4/6)
print("h* fwd", 2*math.sqrt(d/e), "h* cen", (3*d/e)**(1/3))
print("cube root check", (3*d/e)**(1/3), math.log10((3*d/e)**(1/3)))
print("2delta/h at 1e-9", 2*d/1e-9, "trunc at 1e-9", 0.5e-9*e)
print("ratio", 2*d/1e-9/(0.5e-9*e))
print("2sqrt(M d)", 2*math.sqrt(e*d))
print("2^-53/1e-8", 2.0**-53/1e-8, "e*that", e*2.0**-53/1e-8)
print("R1 h*", 2*math.sqrt(1e-3/e))
print("ulp check", math.ulp(2.5), 2.0**-51, math.ulp(1.0), 2.0**-52)
print("e^1.01 vs e: ", math.exp(0.01), "rel diff at h0=2e-8", math.exp(2e-8)-1)
# lab full precision values
def fwd(x,h): return (math.exp(x+h)-math.exp(x))/h
def cen(x,h): return (math.exp(x+h)-math.exp(x-h))/(2*h)
for k in range(1,13):
    h=10.0**(-k)
    print(k, repr(abs(fwd(1.0,h)-e)), repr(abs(cen(1.0,h)-e)))
print("forward/central ratio 1e-2", abs(fwd(1,1e-2)-e)/abs(cen(1,1e-2)-e))
print("misc: 0.1 reference", (1.1**2-1)/0.1)
print("central |t| at 0", (abs(1e-3)-abs(-1e-3))/(2e-3))
