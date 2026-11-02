"""Independent re-derivation of M7 numeric claims used by slice e cards (exact fractions)."""
from fractions import Fraction as F
from itertools import product

def mat_vec(m, v):
    return [sum(m[i][j] * v[j] for j in range(len(v))) for i in range(len(m))]

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def quad(q, x):
    return dot(x, mat_vec(q, x))

def solve(a, b):
    n = len(b)
    m = [list(map(F, row)) + [F(bi)] for row, bi in zip(a, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]

def det(m):
    n = len(m)
    if n == 1:
        return F(m[0][0])
    return sum((-1) ** j * F(m[0][j]) * det([row[:j] + row[j+1:] for row in m[1:]]) for j in range(n))

out = []
# L01 counts
GRID = (-2, -1, 0, 1, 2)
W = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
Q2 = [[1, 2], [2, 1]]
pts = list(product(GRID, GRID))
cases = [(x, y, w) for x in pts for y in pts for w in W]
def comb(w, x, y):
    return [w * x[0] + (1 - w) * y[0], w * x[1] + (1 - w) * y[1]]
fails = sum(1 for x, y, w in cases if not (quad(Q2, comb(w, x, y)) <= w * quad(Q2, x) + (1 - w) * quad(Q2, y)))
neg = sum(1 for x, y in product(pts, pts) if quad(Q2, [x[0]-y[0], x[1]-y[1]]) < 0)
out.append(("L01 Q2 fails", fails, "card c012/c016 says 552, passes 2573"))
out.append(("L01 negative ordered pairs", neg, "card c178 says 184"))
out.append(("L01 gap at x=(1,0),y=(0,1),w=1/2", F(1,2)*quad(Q2,[1,0])+F(1,2)*quad(Q2,[0,1])-quad(Q2,[F(1,2),F(1,2)]), "card c010 says -1/2"))
# L02
A = [[1, 2, 3], [1, -1, 2], [-1, -1, 0]]
Sig = [[sum(A[k][i]*A[k][j] for k in range(3)) + (1 if i == j else 0) for j in range(3)] for i in range(3)]
u = solve(Sig, [1, 1, 1]); s = sum(u); lam = 1 / s; w = [lam * x for x in u]
out.append(("L02 Sigma", Sig, "card c027 rows (4,2,5),(2,7,4),(5,4,14)"))
out.append(("L02 lambda", lam, "c028 177/55"))
out.append(("L02 w", w, "c181 (47/55,17/55,-9/55)"))
out.append(("L02 f(w)", F(1,2)*quad(Sig,w), "c168 177/110"))
# L03 Example 4.1/4.2/Remark 4.3
S3 = [[2, 1], [1, 2]]
out.append(("L03 mu'Sinv mu-part value at (14/15,-11/30)", solve(S3, [F(3,2), F(1,5)]), "c048 (14/15,-11/30)"))
# L04 dual grid counts and g(0,0), R3 gap
mu = [F(3,2), F(1,5)]
SI = [[F(2,3), F(-1,3)], [F(-1,3), F(2,3)]]
def g(lam, nu):
    r = [mu[0] + lam[0] - nu, mu[1] + lam[1] - nu]
    return -F(1,2) * quad(SI, r) - nu
duals = [((F(a,10), F(b,10)), F(nu,10)) for a in range(11) for b in range(11) for nu in range(-10, 1)]
primals = [(F(k,20), 1 - F(k,20)) for k in range(21)]
pf = lambda w: F(1,2)*quad(S3, w) - dot(mu, w)
holds = sum(1 for lam, nu in duals for w_ in primals if g(lam, nu) <= pf(w_))
out.append(("L04 pairs weak duality", (len(duals), len(primals), holds, len(duals)*len(primals)), "c063 1331,21,27951"))
bestg = max(g(l, n) for l, n in duals)
out.append(("L04 largest dual grid", bestg, "c170 -1/2"))
out.append(("L04 g(0,0)", g((F(0),F(0)), F(0)), "c064 -199/300"))
r3duals = [g((F(0),F(0)), F(-k,10)) for k in range(11)]
r3gap = min(pf(w_) for w_ in primals) - max(r3duals)
out.append(("L04 R3 grid gap (lambda=0)", r3gap, "c060 7/300"))
out.append(("L04 R3 g at nu=-3/5", g((F(0),F(0)), F(-3,5)), "lesson -157/300"))
# L05
QA = [[4, 1, 0], [1, 3, 1], [0, 1, 2]]
KKT = [[4,1,0,1,1],[1,3,1,1,0],[0,1,2,0,1],[1,1,1,0,0],[0,1,-1,0,0]]
out.append(("L05 det KKT", det(KKT), "c171 19"))
sol = solve(KKT, [1,0,0,1,0] and [1,-0,0,1,0])  # placeholder overwritten below
rhs = [1, 0, -2 * 0 + 0, 1, 0]
rhs = [-(-1), 0, -2, 1, 0]
sol = solve(KKT, rhs)
out.append(("L05 x,lambda", sol, "c087 x=(13/19,3/19,3/19), c182 lambda=(-36/19,11/19)"))
x = sol[:3]
out.append(("L05 objective", F(1,2)*quad(QA, x) + dot([-1,0,2], x), "c088 551/722"))
out.append(("L05 x'Qx", quad(QA, x), "lesson 817/361"))
out.append(("L05 v'Qv", quad(QA, [-2,1,1]), "lesson 19"))
# L05 Part B grid
QB = [[2,1],[1,2]]; CB=[-3,1]
fB = lambda a,b: F(1,2)*quad(QB,[a,b]) + dot(CB,[a,b])
grid = [F(k,16) for k in range(33)]
below = sum(1 for a in grid for b in grid if fB(a,b) < F(-9,4))
out.append(("L05 grid points below -9/4", below, "c172 0"))
out.append(("L05 f(3/2,0)", fB(F(3,2),F(0)), "c086 -9/4"))
# L06
Sig6 = None
import sys
M = None
# reproduce lab inputs from lab source
def lcg(seed):
    st = seed
    while True:
        st = (1103515245 * st + 12345) % 2**31
        yield st
g_ = lcg(2026)
Mm = [[F(next(g_) % 7 - 3) for _ in range(4)] for _ in range(4)]
mu6 = [F(next(g_) % 13 + 2, 100) for _ in range(4)]
Sig6 = [[sum(Mm[k][i]*Mm[k][j] for k in range(4))/16 + (F(1,10) if i==j else 0) for j in range(4)] for i in range(4)]
out.append(("L06 mu", mu6, "c108 7/100,1/20,3/25,1/50"))
out.append(("L06 diag Sigma", [Sig6[i][i] for i in range(4)], "c109 49/40,27/20,103/80,103/80"))
def closed(gam):
    ones=[F(1)]*4
    y=solve(Sig6,mu6); z=solve(Sig6,ones)
    lam_=(sum(y)-gam)/sum(z)
    return [(y[i]-lam_*z[i])/gam for i in range(4)]
def f_(gam, w):
    return gam/2*quad(Sig6,w) - dot(mu6,w)
for gam in [F(1),F(16)]:
    wq = closed(gam)
    out.append(("L06 eq gamma=%s w" % gam, [float(v) for v in wq], "c110/c111 at gamma=1; c113 at 16"))
    out.append(("L06 eq gamma=%s obj" % gam, float(f_(gam, wq)), "c113 0.820002 at 16"))
g1 = closed(F(1))
out.append(("L06 gamma=1 return, risk", (float(dot(mu6,g1)), float(quad(Sig6,g1))), "c110 0.113798, 0.123809"))
out.append(("L06 gamma=16 return", float(dot(mu6, closed(F(16)))), "c115 0.106241"))
# constrained gamma=4 and gamma=16 via brute enumeration over zero sets
def nn_best(gam):
    best=None
    for mask in product((0,1),repeat=4):
        free=[i for i in range(4) if not mask[i]]
        if not free: continue
        sub=[[gam*Sig6[i][j] for j in free] for i in free]
        # KKT with budget
        k=len(free)
        Kmat=[sub[i]+[F(1)] for i in range(k)]+[[F(1)]*k+[F(0)]]
        sol_=solve(Kmat,[mu6[i] for i in free]+[F(1)])
        wv=[F(0)]*4
        for p_,v in zip(free,sol_[:k]): wv[p_]=v
        lam_=sol_[k]
        Sw=mat_vec(Sig6,wv)
        nu=[gam*Sw[i]-mu6[i]+lam_ for i in range(4)]
        if all(v>=0 for v in wv) and all(nu[i]>=0 for i in range(4) if mask[i]):
            val=f_(gam,wv)
            if best is None or val<best[0]: best=(val,wv,mask)
    return best
b16=nn_best(F(16)); b4=nn_best(F(4))
out.append(("L06 constrained gamma=16 obj", float(b16[0]), "c113 1.392257"))
out.append(("L06 diff at 16 exact", float(b16[0]-f_(F(16),closed(F(16)))), "c113 0.5722548"))
w4=b4[1]
w0=[F(1,4)]*4
turn=sum(abs(w4[i]-w0[i]) for i in range(4))
out.append(("L06 turnover gamma=4 exact", float(turn), "c114 0.5588607"))
out.append(("L06 turnover from 6dp weights", sum(abs(F(s_)-F(1,4)) for s_ in ["0.389219","0.220570","0.390211","0.000000"]), "c114 0.558860"))
# L07 values
REW={0:0,100:60,200:100,300:120,400:130}
H=4; GR=(0,100,200,300,400)
V=[{} for _ in range(H+1)]
V[H]={w:w//100 for w in GR}
for t in range(H-1,-1,-1):
    for w in GR:
        V[t][w]=max(REW[c]+V[t+1][w-c] for c in GR if c<=w)
out.append(("L07 V_t(400) t=0..4", [V[t][400] for t in range(5)], "c130 240,220,200,130,4"))
out.append(("L07 V_3(400)", V[3][400], "c137 130"))
# brute check count
cnt=sum(1 for p_ in product(GR,repeat=4) if all(sum(p_[:k+1])<=400 for k in range(4)))
out.append(("L07 feasible sequences from 400", cnt, "c132 70"))
# L08
DIS=F(9,10); RW={(0,'run'):6,(1,'run'):4,(2,'run'):1}
def rew(s,a): return F(RW[(s,'run')]) if a=='run' else F(-4)
def nx(s,a): return min(s+1,2) if a=='run' else 0
U=[{s:F(0) for s in range(3)}]
for t in range(6):
    prev=U[-1]
    U.append({s: max(rew(s,a)+DIS*prev[nx(s,a)] for a in ('run','repair')) for s in range(3)})
# U[n] value iteration from 0
out.append(("L08 V0(0) via iteration n=6", float(U[6][0]), "c151 13.948890"))
diffs=[max(abs(U[n+1][s]-U[n][s]) for s in range(3)) for n in range(6)]
out.append(("L08 changes", [float(d) for d in diffs], "c154 6.0,3.6,2.74,2.466,2.2194,1.99746"))
seqs=sum(2**(6-t) for t in range(6))*3
out.append(("L08 plans enumerated", seqs, "c153 378"))
for n_,row in enumerate(U):
    pass
out.append(("L08 ratios", [float(diffs[i+1]/diffs[i]) for i in range(5)], "0.6,0.7611,0.9,0.9,0.9"))
for line in out:
    print(line)
