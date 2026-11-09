import math
from fractions import Fraction as F
s1 = math.sin(1.0)
print("sin1", repr(s1))
q = (math.cos(0.995) - math.cos(1.0)) / (1 - 0.995)
print("E3 quotient (0.995,1)", repr(q), "gap", repr(s1 - q))
print("E3 gap printed-form", f"{s1 - q:.10f}")
# R2
eps = 1e-6
beta = s1
val = math.log(1/(eps*(1-beta)))/math.log(1/beta)
print("R2 threshold", val, "smallest n", math.ceil(val))
print("R2 check n=91 bound", beta**91/(1-beta), "n=90 bound", beta**90/(1-beta))
# E1 ratio
b5 = beta**5*1/(1-beta); e5 = abs(0.0 - 0.0)  # placeholder
xstar = 0.0
for _ in range(300): xstar = math.cos(xstar)
x=0.0
for n in range(6):
    if n==5: err5=abs(x-xstar); bnd5=beta**5/(1-beta)
    x=math.cos(x)
print("n=5 err", err5, "bound", bnd5, "ratio", bnd5/err5)
print("xstar", xstar)
# M2
print("M2 n=13", 3*3**-13, "n=14", 3*3**-14)
# E2
print("f'(5)", 5/math.sqrt(26), "f'(50)", 50/math.sqrt(2501))
print("f(5)-5", math.sqrt(26)-5, "f(50)-50", math.sqrt(2501)-50)
# Independent Part B max over all pairs of grid (exact formula check via brute force, different loop)
N=200
xs=[i/N for i in range(N+1)]
best=max(abs(math.cos(a)-math.cos(b))/abs(a-b) for i,a in enumerate(xs) for b in xs[:i])
print("partB max (independent)", best)
# Part C windows, independent code
def win(h):
    xs=[-h+2*h*i/N for i in range(N+1)]
    f=lambda x: math.sqrt(x*x+1)
    best=max(abs(f(a)-f(b))/abs(a-b) for i,a in enumerate(xs) for b in xs[:i])
    return best, min(f(x)-x for x in xs)
print("C5", win(5.0)); print("C50", win(50.0))
# L07 Part A bound check independently
d01 = 1.0
ok=True
x=0.0
for n in range(31):
    err=abs(x-xstar); bnd=beta**n*d01/(1-beta)
    ok = ok and (err<=bnd)
    x=math.cos(x)
print("partA all ok", ok)
# L05 numeric checks
print("0.99^10", f"{0.99**10:.10f}", "0.99^100", f"{0.99**100:.10f}", "0.99^1000", f"{float(F(99,100)**1000):.10f}")
print("ln0.99", math.log(0.99), "e^-1.00503", math.exp(-1.00503), "0.99^100 exact-ish", math.exp(100*math.log(0.99)))
print("1/2^50", F(1,2**50), "1/1024", 1/1024, "1/512", 1/512)
# L06 numeric
print("1/196", 1/196, "12/49", 12/49, "1/4-12/49", 0.25-12/49)
print("binom10_2", math.comb(10,2))
