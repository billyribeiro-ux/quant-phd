import math, random, cmath
MU, SIGMA = 0.5, 1.5
def dens(x, mu, s): return math.exp(-((x-mu)**2)/(2*s*s))/(s*math.sqrt(2*math.pi))
def simpson(t, N=20000):
    lo, hi = MU-12*SIGMA, MU+12*SIGMA; h = (hi-lo)/N; tot = 0.0
    for k in range(N+1):
        x = lo+k*h; w = 1.0 if k in (0, N) else (4.0 if k % 2 else 2.0)
        tot += w*math.exp(t*x)*dens(x, MU, SIGMA)
    return tot*h/3
closed = lambda t: math.exp(MU*t + SIGMA*SIGMA*t*t/2)
for t in (-1.0, 0.0, 0.5, 1.0, 2.0):
    n = simpson(t); c = closed(t)
    print("L07 t", t, "abs diff %.6e" % abs(n-c), "rel %.6e" % (abs(n-c)/c))
v = simpson(2.0)
d = abs(v-closed(2.0))
print("L07 t=2 abs %.6e rel %.10e rel/eps %.4f" % (d, d/closed(2.0), d/closed(2.0)/2.220446049250313e-16))
P=0.25
rng = random.Random(20260701)
cs=0.0; ss=0.0
for _ in range(100000):
    x = 0.0 if rng.random() < P else 2.0
    cs += math.cos(x); ss += math.sin(x)
mc, ms = cs/100000, ss/100000
phi1 = P*cmath.exp(1j*0) + (1-P)*cmath.exp(1j*2.0)
print("L07 sample cos %.10f real phi %.10f diff %.4e" % (mc, phi1.real, mc-phi1.real))
print("L07 sample sin %.10f imag phi %.10f diff %.4e" % (ms, phi1.imag, ms-phi1.imag))
print("L07 E1 printed diff", -0.062124-(-0.062110))
print("L07 modulus t=1 %.10f" % abs(phi1), "sqrt(0.625+0.375cos(-2)) %.10f" % math.sqrt(0.625+0.375*math.cos(-2)))
print("L07 cos(-2) %.7f 0.25+0.75cos2 %.7f" % (math.cos(-2), 0.25+0.75*math.cos(2)))
print("L07 sqrt(2/pi) %.7f e^0.5 %.7f e^3 %.4f" % (math.sqrt(2/math.pi), math.exp(0.5), math.exp(3)))
