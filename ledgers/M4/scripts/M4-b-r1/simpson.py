import math
MU,SIG=0.5,1.5
def dens(x): return math.exp(-((x-MU)**2)/(2*SIG*SIG))/(SIG*math.sqrt(2*math.pi))
def simp(t,N):
    lo=MU-12*SIG; hi=MU+12*SIG; h=(hi-lo)/N; tot=0.0
    for k in range(N+1):
        x=lo+k*h; w=1.0 if k in (0,N) else (4.0 if k%2==1 else 2.0)
        tot+=w*math.exp(t*x)*dens(x)
    return tot*h/3
for N in (200,400,2000,20000):
    for t in (2.0,):
        cl=math.exp(MU*t+SIG*SIG*t*t/2)
        print(N, t, simp(t,N), abs(simp(t,N)-cl), abs(simp(t,N)-cl)/cl)
