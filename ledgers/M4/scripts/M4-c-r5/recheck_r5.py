# Independent recomputation for M4-c round 5 (stdlib + scipy only)
import math
from fractions import Fraction
from scipy import integrate, stats
import numpy as np

print("== L08 exact")
A = np.array([[2,0],[1,1]]); Q = np.array([[0,-1],[1,0]])
S = A@A.T; B = A@Q; print("AA^T", S.tolist(), "BB^T==S", (B@B.T==S).all(), "A^TA", (A.T@A).tolist())
print("A^TA - S entries", (A.T@A-S).tolist(), "max abs", np.abs(A.T@A-S).max())
print("E1 gaps printed X cov:", [round(abs(4.0073-4),4), round(abs(2.0187-2),4), round(abs(1.9936-2),4)])
print("A^TA gap from printed X cov (1,2):", round(2.0187-1,4))
print("Y mean/gap: 4-3.9070 =", round(4-3.9070,4))
print("mean X gaps:", round(1-0.9770,4), round(-2.0055+2,4))
print("Gaussian-free: P(X+Y=0) bound 1/2; (X,X') sum-zero prob 0 (area argument)")
print("Lower-triangular uniqueness: a=2,b=1,c=1 ->", [[2,0],[1,1]])
print("M1 AA^T for [[1,1],[0,2]]:", (np.array([[1,1],[0,2]])@np.array([[1,1],[0,2]]).T).tolist())
print("L08 quiz: w^T S w for w=(1,1):", np.ones(2)@S@np.ones(2))

print("\n== L09")
phi1 = stats.norm.cdf(1.0); print("Phi(1)=", f"{phi1:.6f}")
def mass(n):
    m=[Fraction(1)]
    for _ in range(n):
        new=[Fraction(0)]*(len(m)+6)
        for t,p in enumerate(m):
            for f in range(1,7): new[t+f]+=p/6
        m=new
    return m
mu=3.5; s2=35/12
for n in (1,5,10,20,40):
    m=mass(n); thr=math.floor(mu*n+math.sqrt(s2*n))
    # threshold check: S_n<=thr iff Z_n<=1 with exact real threshold
    real_thr = mu*n+math.sqrt(s2*n)
    ex=sum(m[:thr+1],Fraction(0))
    print(n, thr, round(real_thr,4), f"{float(ex):.6f}", f"{float(ex)-phi1:+.6f}", "unrounded gap", f"{float(ex)-phi1:+.8f}")
print("Chebyshev n=10,100,1000,10000 eps=.5:", [round((35/12)/(n*0.25),6) for n in (10,100,1000,10000)], "7/60=",7/60)
print("M3 two-value: bound", 1/(2*0.25), "exact", 0.5)
print("M2 Var sample mean 4 dice", (35/12)/4, 35/48)
print("E2 SE from printed p: n=5", math.sqrt(0.8552*(1-0.8552)/4000), "gap", 0.8552-phi1, "ratio", (0.8552-phi1)/0.0056)
print("E3 bound n=10000", (35/12)/(10000*0.25), "dist from 3.5 of printed mean", 3.5-3.4689)
print("sanity Phi gap at n=10 exact vs printed 0.843496-phi1=", 0.843496-phi1)

print("\n== L10")
C=stats.cauchy; 
def fV(t): return 2/(math.pi*math.sqrt(3))*(1+t*t/3)**-2
print("t3 density integral [-2,2] quad:", integrate.quad(fV,-2,2,epsabs=1e-13,epsrel=1e-13)[0])
t3=stats.t(3)
print("t3 cdf diff via scipy:", t3.cdf(2)-t3.cdf(-2))
print("closed form F_V(2)-F_V(-2):", 2/math.pi*(math.atan(2/math.sqrt(3))+(2/math.sqrt(3))/(1+4/3)))
print("P(|Z|>10):", 2*stats.norm.sf(10), "P(|C|>10):", 2*C.sf(10), "P(|V|>10):", 2*t3.sf(10))
print("ratio Cauchy/normal tails:", 2*C.sf(10)/(2*stats.norm.sf(10)))
print("(2/pi)atan(0.1)*10 =", 10*2/math.pi*math.atan(0.1))
print("x^3 P(|V|>x) at 10,100,1000:", [x**3*2*t3.sf(x) for x in (10.,100.,1000.)])
print("x P(|C|>x):", [x*2*C.sf(x) for x in (10.,100.,1000.)], "2/pi", 2/math.pi, "4sqrt3/pi", 4*math.sqrt(3)/math.pi)
print("F_V(sqrt3) =", t3.cdf(math.sqrt(3)), 3/4+1/(2*math.pi))
print("arctan(0.1)=", math.atan(0.1))
print("E|C| integral truncated [1,inf) with v-sub: 1/(2pi)*ln(M) ->inf; check quad 1..1e6:", integrate.quad(lambda x: x/(math.pi*(1+x*x)),1,1e6)[0])
print("E[V^4] tail check: integrand 3sqrt3/(2 pi t^4)*t^4 const =", 3*math.sqrt(3)/(2*math.pi))
print("E|V|^3 check: t^3 f_V(t) >= 3sqrt3/(2 pi t) at t=2:", 2**3*fV(2), 3*math.sqrt(3)/(2*math.pi*2))
print("normal tail bound 2exp(-x^2/2) at 10:", 2*math.exp(-50), ">= P(|Z|>10)", 2*stats.norm.sf(10))
print("Cauchy lower bound 1/(pi x) at x=10 vs P(|C|>10)=", 1/(math.pi*10), 2*C.sf(10))
print("Part C standardized var target 1; deviations:", 1.0211-1, 0.9396-1, 0.8807-1, 1.1987-1)
print("IQR ratio 0.4116/0.1279", 0.4116/0.1279, math.sqrt(10))
print("IQR shrink prediction 1.8220/sqrt10", 1.8220/math.sqrt(10))
print("Cauchy exact IQR:", C.ppf(0.75)-C.ppf(0.25))
print("t3 Var check: nu/(nu-2)=", 3/(3-2))
print("lab stats Cauchy path last value 0.9919 - 0 =", 0.9919)
