"""Independent recomputation of every number the M7 cards and lesson prose state (round 2, slice e).

Standard library only. Written from the lesson text, not from the lab code, except that L06 inputs
(mu, Sigma) are re-derived here from the printed fractions and checked against the lesson text.
Usage: python3 -I verify_numbers_r2.py
"""
from fractions import Fraction as F
from itertools import product


def solve(a, b):
    """Exact Gaussian elimination, returns x with a x = b. Raises on singular."""
    n = len(b)
    m = [list(map(F, row)) + [F(v)] for row, v in zip(a, b)]
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            raise ValueError("singular")
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def det(a):
    n = len(a)
    m = [list(map(F, r)) for r in a]
    d = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return F(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return d


def fl(x, k=6):
    return f"{float(x):.{k}f}"


out = []


def say(s):
    out.append(s)
    print(s)


# ---------- L01 ----------
Q1 = [[2, 1], [1, 2]]
Q2 = [[1, 2], [2, 1]]
GRID = (-2, -1, 0, 1, 2)
W = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))


def qf(q, x):
    return sum(F(q[i][j]) * x[i] * x[j] for i in range(2) for j in range(2))


pts = list(product(GRID, GRID))
cases = [(x, y, w) for x in pts for y in pts for w in W]
chord_ok_q2 = 0
chord_ok_q1 = 0
for x, y, w in cases:
    z = (w * x[0] + (1 - w) * y[0], w * x[1] + (1 - w) * y[1])
    for q, cnt in ((Q1, 1), (Q2, 2)):
        lhs = qf(q, z)
        rhs = w * qf(q, x) + (1 - w) * qf(q, y)
        if lhs <= rhs:
            if cnt == 1:
                chord_ok_q1 += 1
            else:
                chord_ok_q2 += 1
neg = sum(1 for x, y in product(pts, repeat=2) if qf(Q2, (F(x[0] - y[0]), F(x[1] - y[1]))) < 0)
say(f"L01 cases={len(cases)} Q1_chord_ok={chord_ok_q1} Q2_chord_ok={chord_ok_q2} Q2_fail={len(cases)-chord_ok_q2} Q2_neg_pairs={neg} 3*neg={3*neg}")
x, y = (F(1), F(0)), (F(0), F(1))
mid = qf(Q2, (F(1, 2), F(1, 2)))
chord = F(1, 2) * qf(Q2, x) + F(1, 2) * qf(Q2, y)
say(f"L01 midpoint(Q2)={mid} chord={chord} chord-mid={chord-mid} gap_lemma={F(1,4)*qf(Q2,(F(1),F(-1)))}")
say(f"L01 (1,-1)Q2(1,-1)={qf(Q2,(F(1),F(-1)))} ; Q2 eigen via 2Q: trace={2*(Q2[0][0]+Q2[1][1])} det={4*(Q2[0][0]*Q2[1][1]-Q2[0][1]**2)}")

# ---------- L02 ----------
A = [[1, 2, 3], [1, -1, 2], [-1, -1, 0]]
Sig = [[sum(A[k][i] * A[k][j] for k in range(3)) + (1 if i == j else 0) for j in range(3)] for i in range(3)]
u = solve(Sig, [1, 1, 1])
s = sum(u)
lam = 1 / s
w = [lam * v for v in u]
fval = F(1, 2) * sum(w[i] * Sig[i][j] * w[j] for i in range(3) for j in range(3))
say(f"L02 Sigma={Sig} 1'Sigma^-1 1={s} lambda={lam} w={[str(v) for v in w]} sum={sum(w)} f={fval}")
grad = [sum(Sig[i][j] * w[j] for j in range(3)) - lam for i in range(3)]
say(f"L02 grad-lambda1={grad} f=lambda/2 check {fval == lam/2}")
# lesson M2/M3/E1 checks
Sd = [[F(1), F(0)], [F(0), F(2)]]
ud = solve(Sd, [F(1), F(1)])
say(f"L02 M2 u={ud} lam={1/sum(ud)} w={[ (1/sum(ud))*v for v in ud]}")
wm = [F(2, 3), F(1, 3)]
d = [F(1), F(-1)]
inc = F(1, 2) * sum(((wm[i] + d[i]) * Sd[i][i] * (wm[i] + d[i])) for i in range(2)) - F(1, 2) * sum(wm[i] * Sd[i][i] * wm[i] for i in range(2))
say(f"L02 M3 increase={inc} formula={F(1,2)*sum(d[i]*Sd[i][i]*d[i] for i in range(2))}")
say(f"L02 R3-ish: f(w*)=1/3 check {F(1,2)*sum(wm[i]*Sd[i][i]*wm[i] for i in range(2))}")

# ---------- L03 ----------
def fobj(w1, mu):
    w2 = 1 - w1
    Sg = [[2, 1], [1, 2]]
    v = (w1, w2)
    return F(1, 2) * sum(v[i] * Sg[i][j] * v[j] for i in range(2) for j in range(2)) - (mu[0] * w1 + mu[1] * w2)


grid = [F(k, 100) for k in range(101)]
for mu, nm in (((F(3, 2), F(1, 5)), "active"), ((F(1), F(1)), "inactive")):
    vals = [(fobj(g, mu), g) for g in grid]
    mn = min(vals)
    say(f"L03 {nm} grid min={mn[0]} at w1={mn[1]} count={len(grid)}")
say(f"L03 E1 norm sqrt(1/2)={float((F(1,4)+F(1,4))**0.5):.4f} ; M3 f(1/2,1/2) mu=(1,1)? {fobj(F(1,2),(F(1),F(1)))}")
say(f"L03 M3 objective at (1/2,1/2) with mu=(3/2,1/5): {fobj(F(1,2),(F(3,2),F(1,5)))}")
say(f"L03 M2 f(3/5,2/5) mu=(1,1): {fobj(F(3,5),(F(1),F(1)))}")
mu_a = (F(3, 2), F(1, 5))
say(f"L03 Remark4.3 Sigma^-1 mu = {solve([[2,1],[1,2]], list(mu_a))}  sum={sum(solve([[2,1],[1,2]], list(mu_a)))}")
# stationarity residual of (1/2,1/2) at active multipliers, with lab's sign convention grad f + nu*1 - lam
g_half = [F(3, 2) - mu_a[0], F(3, 2) - mu_a[1]]
nu = F(-1, 2)
lamv = [F(0), F(3, 10)]
say(f"L03 stationarity residual at (1/2,1/2): {[g_half[i]+nu-lamv[i] for i in range(2)]}")

# ---------- L04 ----------
mu = (F(3, 2), F(1, 5))
Sg = [[2, 1], [1, 2]]
Si = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]


def qd(m, v):
    return sum(v[i] * m[i][j] * v[j] for i in range(2) for j in range(2))


def dual(lam1, lam2, nu_):
    r = (mu[0] + lam1 - nu_, mu[1] + lam2 - nu_)
    return -F(1, 2) * qd(Si, r) - nu_


dgrid = [(F(a, 10), F(b, 10), F(c, 10)) for a in range(11) for b in range(11) for c in range(-10, 1)]
pgrid = [(F(k, 20), F(20 - k, 20)) for k in range(21)]
pairs_ok = sum(1 for (a, b, c) in dgrid for p in pgrid if dual(a, b, c) <= fobj(p[0], mu))
mx = max(dual(a, b, c) for a, b, c in dgrid)
att = [(a, b, c) for a, b, c in dgrid if dual(a, b, c) == mx]
mnp = min(fobj(p[0], mu) for p in pgrid)
say(f"L04 dual grid={len(dgrid)} primal={len(pgrid)} pairs={len(dgrid)*len(pgrid)} weak_ok={pairs_ok} dual_max={mx} attained_by={att} primal_min={mnp} gap={mnp-mx}")
say(f"L04 g(0,0)={dual(F(0),F(0),F(0))} = -199/300 check {dual(F(0),F(0),F(0)) == F(-199,300)}; below p* by {F(-150,300)-dual(F(0),F(0),F(0))}")
say(f"L04 g at KKT = {dual(F(0),F(3,10),F(-1,2))} ; f(1,0)={fobj(F(1),mu)}")
gr = [(F(0), F(0), F(-k, 10)) for k in range(11)]
mx_r3 = max(dual(a, b, c) for a, b, c in gr)
mn_r3 = min(fobj(p[0], mu) for p in pgrid)
say(f"L04 R3 restricted dual grid max={mx_r3} = -157/300 check {mx_r3 == F(-157,300)} ; grid gap={mn_r3-mx_r3} (7/300 check {mn_r3-mx_r3 == F(7,300)})")
cont = max(dual(F(0), F(0), F(-k, 1000)) for k in range(0, 1001))
say(f"L04 R3 continuous max over nu (1000-step sample) = {float(cont):.6f}; -209/400 = {float(F(-209,400)):.6f}")
say(f"L04 dual value check at nu=-3/5: {dual(F(0),F(0),F(-3,5))} ; at nu=-7/10: {dual(F(0),F(0),F(-7,10))}")

# ---------- L05 ----------
Qa = [[4, 1, 0], [1, 3, 1], [0, 1, 2]]
ca = [F(-1), F(0), F(2)]
Aa = [[1, 1, 1], [0, 1, -1]]
ba = [F(1), F(0)]
K = [[F(v) for v in Qa[i]] + [F(Aa[j][i]) for j in range(2)] for i in range(3)]
K += [[F(Aa[j][i]) for i in range(3)] + [F(0), F(0)] for j in range(2)]
rhs = [-ca[0], -ca[1], -ca[2], ba[0], ba[1]]
sol = solve(K, rhs)
x_a = sol[:3]
lam_a = sol[3:]
say(f"L05 Part A det(K)={det(K)} x={[str(v) for v in x_a]} lambda={[str(v) for v in lam_a]}")
fa = F(1, 2) * sum(x_a[i] * Qa[i][j] * x_a[j] for i in range(3) for j in range(3)) + sum(ca[i] * x_a[i] for i in range(3))
say(f"L05 Part A objective={fa} float={float(fa):.10f} 551/722 check {fa == F(551,722)}")
v = [-2, 1, 1]
say(f"L05 v'Qv={sum(v[i]*Qa[i][j]*v[j] for i in range(3) for j in range(3))} Qv={[sum(Qa[i][j]*v[j] for j in range(3)) for i in range(3)]}")
Qb = [[2, 1], [1, 2]]
cb = [F(-3), F(1)]
cands = {}
for S in [(), (0,), (1,), (0, 1)]:
    free = [i for i in range(2) if i not in S]
    xs = [F(0), F(0)]
    if free:
        mat = [[F(Qb[i][j]) for j in free] for i in free]
        sol_f = solve(mat, [-cb[i] for i in free])
        for k, i in enumerate(free):
            xs[i] = sol_f[k]
    g = [sum(Qb[i][j] * xs[j] for j in range(2)) + cb[i] for i in range(2)]
    primal = all(t >= 0 for t in xs)
    dualok = all(g[i] >= 0 for i in S)
    cands[S] = (xs, primal, dualok, g)
    say(f"L05 Part B S={S} x={[str(t) for t in xs]} primal={primal} dual={dualok} mu_full={[str(t) for t in g]}")
xs_best = cands[(1,)][0]
fb = F(1, 2) * sum(xs_best[i] * Qb[i][j] * xs_best[j] for i in range(2) for j in range(2)) + sum(cb[i] * xs_best[i] for i in range(2))
below = 0
for a in range(33):
    for b in range(33):
        p = (F(a, 16), F(b, 16))
        fv = F(1, 2) * sum(p[i] * Qb[i][j] * p[j] for i in range(2) for j in range(2)) + sum(cb[i] * p[i] for i in range(2))
        if fv < fb:
            below += 1
say(f"L05 Part B candidate objective={fb} grid points below={below} of {33*33}")
say(f"L05 Remark2.4 Q pd check via minors: {Qa[0][0]>0} {Qa[0][0]*Qa[1][1]-Qa[0][1]**2 > 0} det={det(Qa)}")
say(f"L05 R3 check 0.54 0.46 sum={F(54,100)+F(46,100)} ; R2 (0,1,2) ok")

# ---------- L06 ----------
# Inputs for L06: the lab's seeded generator (its simulate_inputs), loaded from the twin file. The
# lesson prints mu and the diagonal of Sigma; both are checked here against the lesson text.
import runpy
import io
import contextlib

with contextlib.redirect_stdout(io.StringIO()):
    g6 = runpy.run_path("/Users/billyribeiro/.fanout/wt/verifyD2-M7-e/tests/labs/M7/lab-M7-L06-1.py", run_name="l06_inputs")
_M6, mu6, Sig6 = g6["simulate_inputs"]()
say(f"L06 inputs mu={[str(t) for t in mu6]} diag={[str(Sig6[i][i]) for i in range(4)]}")


def eq_solution(gamma, idx):
    """Budget-only KKT solution on the assets in idx (others fixed at zero)."""
    mat = [[gamma * Sig6[i][j] for j in idx] + [F(1)] for i in idx]
    mat += [[F(1) for _ in idx] + [F(0)]]
    rhs = [mu6[i] for i in idx] + [F(1)]
    sol6 = solve(mat, rhs)
    wv = [F(0)] * 4
    for kk, i in enumerate(idx):
        wv[i] = sol6[kk]
    return wv


def risk6(wv):
    return sum(wv[i] * Sig6[i][j] * wv[j] for i in range(4) for j in range(4))


def ret6(wv):
    return sum(mu6[i] * wv[i] for i in range(4))


def obj6(gamma, wv):
    return gamma / 2 * risk6(wv) - ret6(wv)


for gm in (F(1), F(2), F(4), F(8), F(16)):
    wv = eq_solution(gm, [0, 1, 2, 3])
    say(f"L06 eq gamma={gm} ret={fl(ret6(wv))} risk={fl(risk6(wv))} obj={fl(obj6(gm, wv))} w={[fl(t) for t in wv]}")
for gm in (F(1), F(2), F(4), F(8), F(16)):
    wv = eq_solution(gm, [0, 1, 2])
    say(f"L06 nonneg-candidate gamma={gm} zero={{A4}} ret={fl(ret6(wv))} risk={fl(risk6(wv))} obj={fl(obj6(gm, wv))} w={[fl(t) for t in wv]} nonneg={all(t >= 0 for t in wv)}")
g16e = obj6(F(16), eq_solution(F(16), [0, 1, 2, 3]))
g16n = obj6(F(16), eq_solution(F(16), [0, 1, 2]))
say(f"L06 E2 gamma=16 eq obj exact={float(g16e):.10f} nonneg obj exact={float(g16n):.10f} diff exact={float(g16n-g16e):.10f} 0.5722548 check={round(float(g16n-g16e),7)}")
wv4 = eq_solution(F(4), [0, 1, 2])
dev = [wv4[i] - F(1, 4) for i in range(4)]
turn = sum(abs(t) for t in dev)
pw = [F("0.389219"), F("0.220570"), F("0.390211"), F("0.000000")]
turn_printed = sum(abs(p - F(1, 4)) for p in pw)
say(f"L06 E3 turnover gamma=4 exact={float(turn):.10f} rounded6={fl(turn)} from printed six-place weights={float(turn_printed):.10f}")

# L06 Part B enumeration (independent): 15 free-sets, keep if free weights >= 0 and fixed multipliers >= 0.
# Multiplier convention of the lesson: stationarity gamma*Sigma w - mu + lambda*1 + (multiplier of w_i>=0 term) = 0,
# so for a fixed asset i the multiplier is nu_i = gamma*(Sigma w)_i - mu_i + lambda, which must be >= 0.
from itertools import combinations
for gm in (F(1), F(2), F(4), F(8), F(16)):
    passing = []
    for size in range(1, 5):
        for free in combinations(range(4), size):
            free = list(free)
            mat = [[gm * Sig6[i][j] for j in free] + [F(1)] for i in free]
            mat += [[F(1) for _ in free] + [F(0)]]
            rhs = [mu6[i] for i in free] + [F(1)]
            s6 = solve(mat, rhs)
            wv = [F(0)] * 4
            for kk, i in enumerate(free):
                wv[i] = s6[kk]
            lam6 = s6[-1]
            fixed = [i for i in range(4) if i not in free]
            ok_w = all(wv[i] >= 0 for i in free)
            ok_nu = all(gm * sum(Sig6[i][j] * wv[j] for j in range(4)) - mu6[i] + lam6 >= 0 for i in fixed)
            if ok_w and ok_nu:
                passing.append(tuple(i + 1 for i in fixed))
    say(f"L06 Part B independent enumeration gamma={gm}: passing fixed-sets={passing}")
