from decimal import Decimal as D, getcontext
import math
getcontext().prec = 60
def om(p):
    p = D(p)
    s = p.sqrt(); t = (1 - p).sqrt()
    return s / (1 + 2 * (p * (1 - p)).sqrt())
def om_general(p, eta=D("0.5")):
    p = D(p)
    return (p**eta) / ((p**eta + (1 - p)**eta) ** (1 / eta))
D3 = D(3)/D(10); D35 = D(3)/D(5); D25 = D(2)/D(5)
print("omega(0.3) 40dp", om(D3))
print("omega(0.6) ", om(D35))
print("omega(0.5)", om(D(1)/D(2)), 1/(2*D(2).sqrt()))
print("omega(2/5)", om(D25))
print("Remark1.6 sum A", om(D25)+2*om(D3), " 2w(.3)", 2*om(D3), " w(.6)", om(D35))
print("ratio w(.3)/w(.6)", om(D3)/om(D35))
print("printed quotient", D("0.28579088")/D("0.39125077"))
print("thr a=1", D(1)/(1+D(1)/D(2)), "thr a=.5", 1/(1+D(2)**D("-0.5")))
g_a1 = 150*om(D3); g_b1 = 100*om(D35)
print("Gamma(A) a=1", g_a1, " Gamma(B) a=1", g_b1, " diff", g_a1-g_b1)
rA = D(50).sqrt()+D(100).sqrt()
print("Gamma(A) a=.5", om(D3)*rA, " Gamma(B) a=.5", om(D35)*D(10))
print("grid 0.01 and 0.99", om(D(1)/D(100)), om(D(99)/D(100)))
print("counterexample", om(D(1)/D(100))*100 + om(D(99)/D(100))*50, 0.01*100+0.99*50)
print("over", (om(D(1)/D(100))-D(1)/D(100))*100, "under", (D(99)/D(100)-om(D(99)/D(100)))*50)
print("M1", om(D(1)/D(4)), 1/(2+D(3).sqrt()), 2-D(3).sqrt())
print("p=1/2 M2 weight", om(D(1)/D(2)), 100*om(D(1)/D(2)))
# float grid
GRID=1001
grid=[i/(GRID-1) for i in range(GRID)]
def omf(p): return float(p**0.5/((p**0.5+(1-p)**0.5)**2))
vals=[omf(p) for p in grid]
print("nondecr float", all(vals[i]<=vals[i+1] for i in range(GRID-1)))
interior=grid[1:-1]
above=[omf(p)>p for p in interior]
ch=sum(1 for a,b in zip(above,above[1:]) if a!=b)
ap=[p for p in interior if omf(p)>p]
print("sign changes", ch, "last above", max(ap), "next", grid[grid.index(max(ap))+1], omf(grid[grid.index(max(ap))+1]))
# closed form gap at eta=1 (identity) vs closed form
gapmax=max((abs(p-math.sqrt(p)/(1+2*math.sqrt(p*(1-p)))),p) for p in grid)
print("eta=1 gap max (gap,p)", gapmax)
# closed form gap at eta 1/2
print("eta=1/2 closed gap max", max(abs(omf(p)-math.sqrt(p)/(1+2*math.sqrt(p*(1-p)))) for p in grid))
# monotone of derivative formula numerically
def dom(p):
    q=math.sqrt(p*(1-p)); return (q+2*p*p)/(2*math.sqrt(p)*q*(1+2*q)**2)
def num_deriv(p,h=1e-7): return (omf(p+h)-omf(p-h))/(2*h)
print("deriv check", max(abs(dom(p)-num_deriv(p)) for p in [0.05*i for i in range(1,20)]))
print("min deriv on grid", min(dom(p) for p in grid[1:-1]))
