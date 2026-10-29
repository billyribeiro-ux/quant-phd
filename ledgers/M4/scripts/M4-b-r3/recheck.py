import math, random, sys
# L05 independent recomputation
S1, S2, RHO, SEED = 0.02, 0.03, 0.6, 20260501
def draws(n):
    rng = random.Random(SEED); xs = []
    for _ in range(n):
        z1 = rng.gauss(0, 1); z2 = rng.gauss(0, 1)
        xs.append((S1*z1, S2*(RHO*z1 + math.sqrt(1-RHO**2)*z2)))
    return xs
def cov(xs):
    n=len(xs); a=sum(x for x,_ in xs)/n; b=sum(y for _,y in xs)/n
    s11=sum((x-a)**2 for x,_ in xs)/(n-1); s22=sum((y-b)**2 for _,y in xs)/(n-1)
    s12=sum((x-a)*(y-b) for x,y in xs)/(n-1); return s11,s12,s22
sig=(S1*S1, RHO*S1*S2, S2*S2)
for n in (100,20000):
    s=cov(draws(n)); errs=[abs(s[0]-sig[0]),abs(s[1]-sig[1]),abs(s[2]-sig[2])]
    print("L05 n",n,"s",["%.10g"%v for v in s],"errs",["%.10g"%e for e in errs],"max",max(errs))
s=cov(draws(20000)); print("L05 corr", s[1]/math.sqrt(s[0]*s[2]), "err", s[1]/math.sqrt(s[0]*s[2])-RHO)
qs=[]
for k in range(9):
    a=k*math.pi/8; w=(math.cos(a),math.sin(a))
    q=w[0]*w[0]*s[0]+2*w[0]*w[1]*s[1]+w[1]*w[1]*s[2]; qs.append(q)
print("L05 quad", ["%.10f"%q for q in qs], "max/min", max(qs)/min(qs), "argmax",qs.index(max(qs)),"argmin",qs.index(min(qs)))
print("L05 E1 rel", (s[0]-0.0004)/0.0004 if False else None)
s100=cov(draws(100)); print("L05 E1 rel err at 20000 (s11):", (cov(draws(20000))[0]-0.0004)/0.0004)
print("L05 E3 printed-digit ratio", 0.0010539032/0.0002187758, "unrounded", qs[3]/qs[7])
# L06 relative error
def mean_var(xs):
    n=len(xs); m=sum(xs)/n; return m, sum((x-m)**2 for x in xs)/(n-1)
N=100000
for nu in (5,10):
    rng=random.Random(20260602+nu); ts=[]
    for _ in range(N):
        z=rng.gauss(0,1); w=0.0
        for _ in range(nu): g=rng.gauss(0,1); w+=g*g
        ts.append(z/math.sqrt(w/nu))
    m,v=mean_var(ts); ex=nu/(nu-2)
    print("L06 nu",nu,"mean %.10f var %.10f rel %.10f"%(m,v,(v-ex)/ex))
rng=random.Random(20261102); ws=[]; iw=[]
for _ in range(N):
    z=rng.gauss(0,1); w=0.0
    for _ in range(5): g=rng.gauss(0,1); w+=g*g
    ws.append(w); iw.append(1/w)
print("L06 meanW %.10f meanInvW %.10f"%(sum(ws)/N, sum(iw)/N))
print("L06 E2 ratio", 0.007740/0.001469, "rel-int", 0.0014682)
# L07
print("L07 eps ratio", 7.11e-13/244.69193226, sys.float_info.epsilon, (7.11e-13/244.69193226)/sys.float_info.epsilon)
print("L07 e^3", math.exp(3), "e^0.5", math.exp(0.5), "sqrt(2/pi)", math.sqrt(2/math.pi))
phi1=0.25+0.75*complex(math.cos(2),math.sin(2))
print("L07 phi1", phi1, "abs", abs(phi1), "|phi|^2 formula", 0.625+0.375*math.cos(-2), math.sqrt(0.625+0.375*math.cos(-2)))
print("L07 real part 0.25+0.75cos2", 0.25+0.75*math.cos(2))
rng=random.Random(20260701); cs=0; ss=0
for _ in range(100000):
    x = 0.0 if rng.random()<0.25 else 2.0
    cs+=math.cos(x); ss+=math.sin(x)
print("L07 sample mean cos %.10f sin %.10f"%(cs/100000, ss/100000))
print("L07 E1 diff", -0.062124-(-0.062110))
