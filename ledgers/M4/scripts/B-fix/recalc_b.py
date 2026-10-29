import math, random, cmath, sys
from pathlib import Path

base = Path("/tmp/quant-b2/tests/labs/M4")

def ns_of(name):
    src = (base / name).read_text(encoding="utf-8")
    src = src.rsplit("\nmain()", 1)[0]
    ns = {}
    exec(compile(src, name, "exec"), ns)
    return ns

# L05: sample matrix, n=20000, unrounded
l05 = ns_of("lab-M4-L05-1.py")
xs = l05["draws"](20000, l05["SEED"])
s = l05["sample_cov"](xs)
s100 = l05["sample_cov"](l05["draws"](100, l05["SEED"]))
sig = [[l05["S1"]**2, l05["RHO"]*l05["S1"]*l05["S2"]], [l05["RHO"]*l05["S1"]*l05["S2"], l05["S2"]**2]]
print("L05 s11 n20000 unrounded", repr(s[0][0]))
print("L05 rel err s11 n20000 (vs 0.0004)", (s[0][0]-0.0004)/0.0004)
print("L05 rel err from printed 0.00039491", (0.00039491-0.0004)/0.0004)
print("L05 errors n100 unrounded", [abs(s100[i][j]-sig[i][j]) for i,j in [(0,0),(0,1),(1,1)]])
vals=[]
for k in range(9):
    a=k*math.pi/8; w=(math.cos(a), math.sin(a))
    vals.append(l05["quadratic_form"](s,w))
print("L05 max/min unrounded", max(vals)/min(vals), vals.index(max(vals)), vals.index(min(vals)))
print("L05 corr unrounded", s[0][1]/math.sqrt(s[0][0]*s[1][1]))

# L06
l06 = ns_of("lab-M4-L06-1.py")
rel = {}
for nu in (5,10):
    rng = random.Random(l06["SEED"]+nu)
    ts=[l06["chi_square_and_t"](rng,nu)[1] for _ in range(l06["N_DRAWS"])]
    m,v = l06["mean_and_variance"](ts)
    ex = l06["t_variance"](nu)
    rel[nu]=(v-ex)/ex
    print("L06 nu",nu,"mean",repr(m),"var",repr(v),"relerr",rel[nu])
print("L06 |rel10|/rel5 unrounded", abs(rel[10])/abs(rel[5]))
print("L06 printed-based ratio", 0.007740/0.001469)
print("L06 rel5 from printed 1.669114,1.666667", (1.669114-1.666667)/1.666667)
rng = random.Random(l06["SEED"]+500)
ws=[];inv=[]
for _ in range(l06["N_DRAWS"]):
    w,_=l06["chi_square_and_t"](rng,5); ws.append(w); inv.append(1.0/w)
mw=sum(ws)/len(ws)
print("L06 meanW", repr(mw), "relerr of mean W", (mw-5)/5, "printed-based", (4.997415-5)/5)

# L07
l07 = ns_of("lab-M4-L07-1.py")
ex = l07["mgf_closed"](2.0, l07["MU"], l07["SIGMA"])
num = l07["mgf_numerical"](2.0, l07["MU"], l07["SIGMA"])
print("L07 abs diff t=2", abs(num-ex), "value", ex, "relerr", abs(num-ex)/ex)
print("L07 eps ratio", (abs(num-ex)/ex)/2.220446049250313e-16)
rng = random.Random(l07["SEED"])
cs=0.0; sn=0.0
for _ in range(l07["N_DRAWS"]):
    x = l07["VALUE_A"] if rng.random() < l07["P_A"] else l07["VALUE_B"]
    cs += math.cos(x); sn += math.sin(x)
phi1 = l07["phi_two_point"](1.0)
print("L07 mean cos", repr(cs/l07["N_DRAWS"]), "re phi1", repr(phi1.real), "diff", cs/l07["N_DRAWS"]-phi1.real)
print("L07 mean sin", repr(sn/l07["N_DRAWS"]), "im phi1", repr(phi1.imag))
print("L07 |phi(1)|", abs(phi1), "sq", abs(phi1)**2)
print("L07 0.25+0.75cos2", 0.25+0.75*math.cos(2))
print("L07 sqrt(0.625+0.375cos(-2))", math.sqrt(0.625+0.375*math.cos(-2)))
print("L07 e^3", math.exp(3), "e^0.5", math.exp(0.5))
print("L07 sqrt(2/pi)", math.sqrt(2/math.pi))
