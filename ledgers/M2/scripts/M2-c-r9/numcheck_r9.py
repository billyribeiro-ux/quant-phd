import math
# central bound B(h) = M3/6 h^2 + d/h ; h* = (3d/M3)^(1/3); B(h*) = 3d/(2h*)
for M3, d in [(math.e, 2**-52), (2.0, 1e-3), (0.5, 1e-8)]:
    hs = (3*d/M3)**(1/3)
    B = lambda h: M3/6*h*h + d/h
    grid = [hs*(1+1e-3*k) for k in range(-500, 501) if hs*(1+1e-3*k) > 0]
    print(f"M3={M3:.6g} d={d:.4g} h*={hs:.6e} B(h*)={B(hs):.10e} 3d/(2h*)={3*d/(2*hs):.10e} min-on-grid-at-h*={min(grid,key=B)==min(grid,key=B) and abs(min(grid,key=B)-hs)<=2e-3*hs}")
# case h* > h0: B decreasing on (0,h0], minimum on (0,h0] at h0
M3, d, h0 = 2.0, 1e-3, 0.01
hs=(3*d/M3)**(1/3); print("h*>h0 case", hs > h0, min([h0*k/1000 for k in range(1,1001)], key=lambda h: M3/6*h*h+d/h))
# w-rename proof check: |w-(u.w)u|^2 = |w|^2-(u.w)^2 for unit u
import random
for _ in range(3):
    w=[random.uniform(-3,3) for _ in range(2)]; t=random.uniform(0,6.28); u=[math.cos(t),math.sin(t)]
    uw=u[0]*w[0]+u[1]*w[1]; r=[w[0]-uw*u[0], w[1]-uw*u[1]]
    print("identity", abs((r[0]**2+r[1]**2)-((w[0]**2+w[1]**2)-uw*uw))<1e-12)
# L15 card: g(1/n,1/n)=1/2, f(1/n,1/n)=1/(2n) by definition, lab printed n only
for n in (10,100,1000,10000):
    x=1/n; g=x*x/(2*x*x); f=x**3/(2*x*x); print(n, round(g,6), f"{f:.9f}")
