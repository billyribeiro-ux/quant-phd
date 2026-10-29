import math
from fractions import Fraction
def om(p, eta=0.5): return p**eta/(p**eta+(1-p)**eta)**(1/eta)
def cf(p): return math.sqrt(p)/(1+2*math.sqrt(p*(1-p)))
for p in (0.3,0.6,0.5,0.01,0.99,0.05,0.279,0.278,0.25,0.25):
    print("omega", p, repr(om(p)), repr(cf(p)))
print("ratio", om(0.3)/om(0.6), "thr a=1/2", 1/(1+2**-0.5), "thr a=1", 2/3)
g1 = 2*om(0.3)
print("2w(.3)", g1, "w(.6)", om(0.6))
print("GammaA a=1", om(0.3)*150, "GammaB", om(0.6)*100, "diff", om(0.3)*150-om(0.6)*100)
print("str8 unrounded", f"{om(0.3)*150:.8f}", f"{om(0.6)*100:.8f}")
print("E2 printed-vs-unrounded diff", om(0.3)*150-om(0.6)*100)
print("a=1/2 GA,GB", om(0.3)*(50**0.5+100**0.5), om(0.6)*100**0.5)
print("misc", om(0.01)*100+om(0.99)*50, 0.01*100+0.99*50, om(0.01), om(0.99))
# sign change search
grid=[i/1000 for i in range(1001)]
ch=[(grid[i],grid[i+1]) for i in range(1,999) if (om(grid[i])>grid[i])!=(om(grid[i+1])>grid[i+1])]
print("sign changes", ch)
print("last > p", max(p for p in grid[1:-1] if om(p)>p))
# crossing precisely
lo,hi=0.278,0.279
for _ in range(60):
    m=(lo+hi)/2
    if om(m)>m: lo=m
    else: hi=m
print("crossing", lo)
# eta=1 scratch
print("eta=1 gap", max(abs(om(p,1.0)-cf(p)) for p in grid))
print("eta=1 Gamma", (om(0.3,1.0)*150), om(0.6,1.0)*100)
print("maxgap eta1 check via grid", max(abs(om(p,1.0)-cf(p)) for p in grid))
