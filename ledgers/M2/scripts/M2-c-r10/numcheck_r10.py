import math, random

# L13 Corollary 4.1 / P3 / R1 / card c187 numbers
for M3, d in [(math.e, 2**-52), (2.0, 1e-3), (0.5, 1e-8)]:
    hs = (3*d/M3)**(1/3)
    B = lambda h: M3/6*h*h + d/h
    print(f"P3 M3={M3:.6g} d={d:.4g} h*={hs:.6e} B(h*)={B(hs):.10e} 3d/(2h*)={3*d/(2*hs):.10e}")
    grid = [hs*(1+1e-3*k) for k in range(-500, 501) if hs*(1+1e-3*k) > 0]
    print("  grid argmin within 2e-3 of h*:", abs(min(grid, key=B)-hs) <= 2e-3*hs)
d, M = 1e-3, math.e
print("R1 h*=2sqrt(d/M)=", 2*math.sqrt(d/M))
M, d = 2.0, 1e-3
hs = 2*math.sqrt(d/M); print("Cor4.1 B(h*)=2sqrt(M d)", 2*math.sqrt(M*d), "B(h*) direct", M/2*hs+2*d/hs)

# L14 Example 4.1 numbers
e2 = math.exp(2)
print("e^2", e2, "2e^2", 2*e2, "sin2", math.sin(2), "cos2", math.cos(2))
fval = 2*e2 + math.sin(2)/2
ftan = (2*e2 + e2) + ((math.cos(2)*2 - math.sin(2))/4)
print("f(2)", fval, "f'(2)", ftan, "closed form", e2 + 2*e2 + (2*math.cos(2)-math.sin(2))/4)

# L17 E3 / R1 / gradient numbers
g = (1.0, 1.8775826)
n = math.hypot(*g); ang = math.degrees(math.atan2(g[1], g[0])); al = math.radians(62-ang)
print("|w|", n, "angle", ang, "alpha deg", 62-ang, "alpha rad", al, "alpha^2/2", al*al/2, "|w|(1-cos)", n*(1-math.cos(al)))
ud = (g[0]/n, g[1]/n); m = max(abs(ud[0]), abs(ud[1])); r = (ud[0]/m, ud[1]/m)
print("unit", ud, "rescaled", r, "value", r[0]*g[0]+r[1]*g[1], "corner", abs(g[0])+abs(g[1]))

# L17 Theorem 3.1 identity for unit u
for _ in range(3):
    w = [random.uniform(-3, 3), random.uniform(-3, 3)]; t = random.uniform(0, 6.2832); u = [math.cos(t), math.sin(t)]
    uw = u[0]*w[0]+u[1]*w[1]; rr = [w[0]-uw*u[0], w[1]-uw*u[1]]
    print("identity", abs((rr[0]**2+rr[1]**2) - ((w[0]**2+w[1]**2) - uw*uw)) < 1e-12)

# L15 card c234: g and f on the diagonal (1/n,1/n), g=xy/(x^2+y^2), f=x^2 y/(x^2+y^2)
for nn in (10, 100, 1000, 10000):
    x = 1/nn; gv = x*x/(2*x*x); fv = x**3/(2*x*x)
    print("n", nn, "g", round(gv, 6), "f", f"{fv:.9f}")

# L17 Section 4 truncation/rounding order at t=1e-6
best = max(abs(6*math.cos(k*math.pi/180)**2*math.sin(k*math.pi/180) - math.cos(0.5)*math.sin(k*math.pi/180)**3) for k in range(360))
print("E2 max |phi'''|", best, "t^2/6*max", (1e-6)**2/6*best)
