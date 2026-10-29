import math
e = math.e
d = 2.0**-52
print("R1 2*sqrt(1e-3/e) =", repr(2*math.sqrt(1e-3/e)), "rounded6", round(2*math.sqrt(1e-3/e), 6))
print("E3 cbrt(3d/e) =", (3*d/e)**(1/3))
print("L13 h*=2sqrt(d/e)=", 2*math.sqrt(d/e), " B(h*)=2sqrt(e d)=", 2*math.sqrt(e*d))
def fwd(h): return (math.exp(1+h)-math.exp(1))/h
def cen(h): return (math.exp(1+h)-math.exp(1-h))/(2*h)
for k in (2,3,5,7):
    h=10.0**-k
    print("k",k,"fwd err", abs(fwd(h)-e), "cen err", abs(cen(h)-e))
# full precision table as the lab computes it
EXACT=math.e
def F(h): return abs((math.exp(1.0+h)-math.exp(1.0))/h-EXACT)
def C(h): return abs((math.exp(1.0+h)-math.exp(1.0-h))/(2.0*h)-EXACT)
for k in (5,7):
    h=10.0**-k
    print("lab-style cen k",k, repr(C(h)), "fwd", repr(F(h)))
print("diff cen 1e-5 vs 1e-7:", abs(C(1e-5)-C(1e-7)))
print("ratio fwd/cen at 1e-2 unrounded:", (F(1e-2))/(C(1e-2)))
print("fwd 1e-2 over 1e-3 ratio:", F(1e-2)/F(1e-3), " central:", C(1e-2)/C(1e-3))
print("fwd 1e-9 / 1e-8:", F(1e-9)/F(1e-8))
print("Ex2.3 fwd bounds", e*0.005, math.exp(1.01)*0.005, "cen", math.exp(0.99)*1e-4/6, math.exp(1.01)*1e-4/6)
print("E1 bounds", 10*math.exp(-0.001), 10*math.exp(0.01), "central", 100*math.exp(-0.011), 100*math.exp(0.011))
print("R3 2^-53/1e-8", 2.0**-53/1e-8, "e*", e*2.0**-53/1e-8, "2sqrt(M d)", 2*math.sqrt(e*d))
print("E2 2d/h", 2*d/1e-8, 2*d/1e-9, "trunc", 0.5e-9*e, (2*d/1e-9)/(0.5e-9*e))
print("M3 sin", math.sin(0.01), math.sin(0.01)/0.01, math.sin(0.01)/0.01-1)
print("cube root decade log10", math.log10((3*d/e)**(1/3)))
