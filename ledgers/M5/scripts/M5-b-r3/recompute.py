"""Independent recomputation of every prose number on L05-L07 (verifier's own code, not the page's)."""
import math
from fractions import Fraction as F
from itertools import combinations

out = []
def say(*a):
    out.append(" ".join(str(x) for x in a))

# ---- L05
say("L05 0.99^10, 0.99^100, 0.99^1000 floats:", f"{0.99**10:.10f}", f"{0.99**100:.10f}", f"{0.99**1000:.6e}")
say("L05 exact 0.99^100 vs 0.366:", float(F(99,100)**100), "ln0.99=", math.log(0.99), "e^(100 ln .99)=", math.exp(100*math.log(0.99)))
say("L05 (1/2)^9, (1/2)^10 vs 1/1000:", F(1,2)**9, float(F(1,2)**9), F(1,2)**10, float(F(1,2)**10), (F(1,2)**9 > F(1,1000)), (F(1,2)**10 < F(1,1000)))
say("L05 sup of x^n on grid k/100:", [max(F(k,100)**n for k in range(101)) for n in (1,2,5,10,50)])
say("L05 sup of x^n on [0,1/2] grid k/200 (k=0..100):", [max((F(k,200))**n for k in range(101)) == F(1,2)**n for n in (1,2,5,10,50)])
say("L05 mech-1: x^3 on [0,1/2] sup:", F(1,8))
say("L05 values at x=1/2:", [F(1,2)**n for n in (1,2,5,10,50)])
say("L05 2^50:", 2**50)
say("L05 emp-1 /1/2^50 check:", F(1, 2**50) == F(1,2)**50)

# ---- L06 Part A bisection (independent)
def term(n):
    return F((n*n) % 1000, 1000)
PREFIX = 4096
vals = [term(n) for n in range(1, PREFIX+1)]
left, right = F(0), F(1)
last = 0
chosen = []
widths = []
for step in range(1, 9):
    mid = (left+right)/2
    pool = [n for n in range(last+1, PREFIX+1) if left <= vals[n-1] <= right]
    lo = [n for n in pool if vals[n-1] < mid]
    hi = [n for n in pool if vals[n-1] >= mid]
    if len(lo) >= len(hi):
        right = mid; half = lo
    else:
        left = mid; half = hi
    idx = half[0]
    last = idx
    chosen.append(idx)
    widths.append(right-left)
say("L06 Part A chosen indices:", chosen)
say("L06 Part A widths:", [str(w) for w in widths])
say("L06 Part A width step 8 =", widths[-1], float(widths[-1]), "== 1/256:", widths[-1] == F(1,256))
# tail check
ok = True
ivs = []
l, r = F(0), F(1); last = 0
for step in range(1,9):
    mid=(l+r)/2
    pool=[n for n in range(last+1,PREFIX+1) if l<=vals[n-1]<=r]
    lo=[n for n in pool if vals[n-1]<mid]; hi=[n for n in pool if vals[n-1]>=mid]
    if len(lo)>=len(hi): r=mid; half=lo
    else: l=mid; half=hi
    last=half[0]; ivs.append((l,r,vals[last-1]))
for j in range(8):
    for (_,_,v) in ivs[j:]:
        if not (ivs[j][0] <= v <= ivs[j][1]): ok=False
say("L06 tail check all True:", ok)

# grid maxima
def f(x): return x*(1-x)
tenths = [F(k,10) for k in range(11)]
sevenths = [F(k,7) for k in range(8)]
mt = max(f(x) for x in tenths); ms = max(f(x) for x in sevenths)
say("L06 tenths max", mt, "argmax", [x for x in tenths if f(x)==mt], "sevenths max", ms, "argmax", [x for x in sevenths if f(x)==ms])
say("L06 1/4 - 12/49 =", F(1,4)-F(12,49), float(F(1,4)-F(12,49)), "1/196 =", F(1,196))
# unit vectors truncated to 20
def unit(i): return [1 if k==i else 0 for k in range(20)]
vs=[unit(i) for i in range(10)]
dists=[max(abs(a-b) for a,b in zip(p,q)) for p,q in combinations(vs,2)]
say("L06 pairs", len(dists), "min", min(dists), "max", max(dists), "C(10,2)=", math.comb(10,2))

# ---- L07
beta = math.sin(1.0)
x=0.0
for _ in range(300): x=math.cos(x)
xbar=x
say("L07 fixed point xbar", f"{xbar:.10f}", "cos(xbar)-xbar", math.cos(xbar)-xbar)
d01 = abs(0 - math.cos(0))
x=0.0
rows=[]
allok=True
for n in range(0,31):
    err=abs(x-xbar); bound=beta**n*d01/(1-beta)
    if err>bound: allok=False
    if n in (0,1,2,5,10,20,30): rows.append((n, round(x,6), f"{err:.6e}", f"{bound:.6e}"))
    x=math.cos(x)
say("L07 Part A rows:", rows)
say("L07 bound holds n=0..30:", allok, "d01", d01, "1/(1-beta)", 1/(1-beta))
say("L07 x_2 =", math.cos(math.cos(0.0)), "cos1=", math.cos(1.0))
# proper ratio at n=5
xs=[0.0]
for _ in range(10): xs.append(math.cos(xs[-1]))
err5=abs(xs[5]-xbar); b5=beta**5/(1-beta)
say("L07 n=5 x5", xs[5], "err", err5, "bound", b5, "ratio", b5/err5)
# Part B
G=200
grid=[i/G for i in range(G+1)]
best=0; arg=None
for i,x in enumerate(grid):
    for y in grid[i+1:]:
        q=abs(math.cos(x)-math.cos(y))/(y-x)
        if q>best: best=q; arg=(x,y)
say("L07 Part B max quotient", f"{best:.10f}", "argmax", arg, "sin1-max", f"{beta-best:.10f}")
say("L07 pair (0.995,1) quotient", f"{(math.cos(0.995)-math.cos(1.0))/(1-0.995):.10f}")
# Part C
def ratio_window(half):
    xs=[-half+2*half*i/G for i in range(G+1)]
    f2=lambda t: math.sqrt(t*t+1)
    b=0.0
    for i,x in enumerate(xs):
        for y in xs[i+1:]:
            b=max(b, abs(f2(x)-f2(y))/(y-x))
    gap=min(f2(x)-x for x in xs)
    return b,gap, arg if False else None
for h in (5.0,50.0):
    b,gap,_=ratio_window(h)
    say("L07 Part C window", h, "max ratio", f"{b:.10f}", "min gap", f"{gap:.10f}")
say("L07 f'(5)=5/sqrt26", f"{5/math.sqrt(26):.10f}", "f'(50)", f"{50/math.sqrt(2501):.10f}")
# E1
say("L07 E1 ratio", f"{2.661258/0.05439523:.6f}", "computed", f"{b5/err5:.6f}", "sin1^5/(1-sin1)", f"{beta**5/(1-beta):.6f}")
# M1, M2, M3, R2
say("L07 M2 3*3^-13", 3/3**13, "3*3^-14", 3/3**14, "3^13", 3**13, "3^14", 3**14)
# R2
eps=1e-6
say("L07 R2 n*:", math.log(1/(eps*(1-beta)))/math.log(1/beta))
nmin=min(n for n in range(0,1000) if beta**n/(1-beta) <= eps)
say("L07 R2 smallest n", nmin, "bound at 90", beta**90/(1-beta), "at 91", beta**91/(1-beta))
say("L07 R2 bound at 30", beta**30/(1-beta))
# Example 2.3 and R1
say("Ex2.3 bound n=0..3 vs err", [(3*3**-n, abs((3-3*3**-n)-3)) for n in range(4)])
# R1: phi x = beta x from 1
say("R1 phi x= beta x from 1 n=3:", beta**3 if False else 0.5**3, "bound", 0.5**3*(1-0.5)/(1-0.5))
# L07 Ex 3.3 sup
say("sin1 approx", f"{math.sin(1):.6f}")
# misc ratio from misconception 3: 2.661258/0.05439523
say("misc3 ratio", 2.661258/0.05439523)
print("\n".join(out))
