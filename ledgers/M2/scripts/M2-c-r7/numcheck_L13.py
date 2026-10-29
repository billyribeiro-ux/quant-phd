import math
e = math.e
def fwd(h): return (math.exp(1+h)-math.exp(1))/h
def cen(h): return (math.exp(1+h)-math.exp(1-h))/(2*h)
ef2, ec2 = abs(fwd(1e-2)-e), abs(cen(1e-2)-e)
print("fwd err 1e-2 unrounded", ef2, "cen err 1e-2 unrounded", ec2, "ratio", ef2/ec2)
print("printed ratio", 1.364e-2/4.530e-5)
print("ratio fwd 1e-8/1e-9 printed", 2.154e-7/6.603e-9)
print("fwd err 1e-8 unrounded", abs(fwd(1e-8)-e), "1e-9", abs(fwd(1e-9)-e))
print("cen 1e-5", abs(cen(1e-5)-e), "1e-7", abs(cen(1e-7)-e))
d = 2.0**-52
print("h* fwd", 2*math.sqrt(d/e), "h* cen", (3*d/e)**(1/3))
print("2sqrt(M delta)", 2*math.sqrt(e*d))
print("2^-53/1e-8 =", 2.0**-53/1e-8, " times e", e*2.0**-53/1e-8)
print("2delta/h at 1e-9", 2*d/1e-9, "trunc", e*0.5*1e-9, "ratio", 2*d/1e-9/(e*0.5*1e-9))
print("R1 h*", 2*math.sqrt(1e-3/e))
print("Ex2.3 fwd bounds", 0.005*e, 0.005*math.exp(1.01), "cen", math.exp(0.99)*1e-4/6, math.exp(1.01)*1e-4/6)
print("M3 sin bound", 0.005*math.sin(0.01)*2, "err", math.sin(0.01)/0.01-1)
