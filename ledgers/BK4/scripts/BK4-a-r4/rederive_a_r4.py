"""Independent re-derivation of the numbers and claims in BK4 slice a (L01, L02, L03, index). Standard library only."""
import random
from fractions import Fraction
from math import ceil, floor

out = []
def say(s):
    out.append(s)
    print(s)

# ---------- L01 ----------
SEED, PAY = 20260, 12
rng = random.Random(SEED)
day = []
for seq in range(1, PAY + 1):
    s, r = rng.sample(range(3), 2)
    d = rng.randint(100, 5000)
    day.append((seq, s, r, 100 * d))
for seq, s, r, a in day:
    say(f"L01 payment {seq:2d}: {s} -> {r} {a}")
def S_path(bank):
    path = [0]
    acc = 0
    for _, s, r, a in day:
        if s == bank: acc -= a
        elif r == bank: acc += a
        path.append(acc)
    return path
def feasible(o, path):
    return all(o + x >= 0 for x in path)
def need_by_search(bank):
    path = S_path(bank)
    lo, hi = 0, 10**9
    assert feasible(hi, path)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid, path): hi = mid
        else: lo = mid + 1
    return lo
for b in range(3):
    path = S_path(b)
    net = path[-1]
    debit = max(0, -net)
    need = need_by_search(b)
    say(f"L01 bank {b}: need(search)={need} need(formula)={max(0,-min(path))} net={net} debit={debit} need>=debit {need>=debit}")
gross = sum(a for *_, a in day)
moved = sum(max(0, -S_path(b)[-1]) for b in range(3))
say(f"L01 gross={gross} moved={moved} ratio={Fraction(moved, gross)} = {float(Fraction(moved,gross)):.8f}; 4dp={round(float(Fraction(moved,gross)),4)}; pct={float(100*Fraction(moved,gross)):.4f}")

# ---------- L02 ----------
rng = random.Random(2026)
trades = []
for seq in range(1, 7):
    p, r = rng.sample(range(4), 2)
    d = rng.randint(500, 20000)
    trades.append((p, r, 100 * d))
G = sum(a for *_, a in trades)
rec = [sum(a for _, r, a in trades if r == m) for m in range(4)]
pay = [sum(a for p, _, a in trades if p == m) for m in range(4)]
n = [rec[m] - pay[m] for m in range(4)]
A = sum(max(0, x) for x in n)
bps = floor(Fraction(10000 * (G - A), G))
say(f"L02 G={G} rec={rec} pay={pay} n={n} sum_n={sum(n)} A={A} sum_neg={sum(max(0,-x) for x in n)} reduction={G-A} bps={bps} exact={float(Fraction(10000*(G-A),G)):.4f}")
say(f"L02 ratio check 2502700/7596300 = {float(Fraction(2502700,7596300)):.6f}")
# Example 2.4 and M1, M2 by the same formulas
def bps_of(trs):
    G = sum(a for *_, a in trs)
    rec = {}
    pay = {}
    for p, r, a in trs:
        rec[r] = rec.get(r, 0) + a; pay[p] = pay.get(p, 0) + a
    mem = set(rec) | set(pay)
    nn = {m: rec.get(m, 0) - pay.get(m, 0) for m in mem}
    A = sum(max(0, x) for x in nn.values())
    return G, A, nn, floor(Fraction(10000 * (G - A), G))
ex24 = [(0, 1, 100), (1, 2, 80), (2, 0, 50)]
say(f"L02 Example 2.4 (dollars): {bps_of([(p,r,a*100) for p,r,a in ex24])}")
m1 = [(0, 1, 50), (1, 2, 70), (2, 3, 20), (3, 0, 40)]
say(f"L02 M1: {bps_of([(p,r,a*100) for p,r,a in m1])}")
say(f"L02 M2 (doubled ex 2.4): {bps_of([(p,r,a*200) for p,r,a in ex24])}")
m3 = [(0, 1, 100), (0, 2, 100)]
say(f"L02 M3: {bps_of([(p,r,a*100) for p,r,a in m3])}")
# R2 example: X and Y
X = [(0, 1, 100)]
Y = X + [(2, 3, 50), (3, 2, 50)]
say(f"L02 R2 X A={bps_of([(p,r,a*100) for p,r,a in X])[1]} G={bps_of([(p,r,a*100) for p,r,a in X])[0]}; Y A={bps_of([(p,r,a*100) for p,r,a in Y])[1]} G={bps_of([(p,r,a*100) for p,r,a in Y])[0]}")
# P3 cycle check k=2..6
for k in range(2, 7):
    cyc = [(t, (t + 1) % k, 7) for t in range(k)]
    G_, A_, nn_, b_ = bps_of(cyc)
    assert A_ == 0 and b_ == 10000 and all(v == 0 for v in nn_.values())
say("L02 P3 cycle k=2..6: A=0, bps=10000 verified")
# Prop 2.3 random check: A==G iff every member has Rec==0 or Pay==0
rr = random.Random(7)
bad = 0
for _ in range(3000):
    m = rr.randint(2, 5)
    q = rr.randint(1, 6)
    trs = []
    for _ in range(q):
        p, r = rr.sample(range(m), 2)
        trs.append((p, r, rr.randint(1, 50)))
    G_, A_, nn_, _ = bps_of(trs)
    rec_ = {}; pay_ = {}
    for p, r, a in trs:
        rec_[r] = rec_.get(r, 0) + a; pay_[p] = pay_.get(p, 0) + a
    cond = all(rec_.get(x, 0) == 0 or pay_.get(x, 0) == 0 for x in range(m))
    if (A_ == G_) != cond: bad += 1
    # Prop 2.2(c)
    if sum(max(0, -x) for x in nn_.values()) != A_: bad += 1
    if not (0 <= A_ <= G_): bad += 1
say(f"L02 random Prop 2.2/2.3 check (3000 cases) mismatches={bad}")
# R1 bps range with G>0
rr = random.Random(9)
badr = 0
for _ in range(2000):
    m = rr.randint(2, 5); q = rr.randint(1, 6)
    trs = []
    for _ in range(q):
        p, r = rr.sample(range(m), 2); trs.append((p, r, rr.randint(1, 50)))
    G_, A_, _, b_ = bps_of(trs)
    if not (0 <= b_ <= 10000) or ((b_ == 10000) != (A_ == 0)): badr += 1
say(f"L02 random R1 check mismatches={badr}")

# ---------- L03 ----------
def wf(L, IM, DF, K, defaulter):
    a1 = min(L, IM[defaulter]); a2 = min(L - a1, DF[defaulter]); a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    surv = sorted(i for i in DF if i != defaulter)
    D = sum(DF[i] for i in surv)
    if Z >= D:
        x = {i: DF[i] for i in surv}; u = Z - D
    else:
        x = {i: Z * DF[i] // D for i in surv}; ell = Z - sum(x.values())
        for i in surv:
            if ell == 0: break
            if DF[i] > 0: x[i] += 1; ell -= 1
        assert ell == 0
        u = 0
    return a1, a2, a3, x, u
IM = {1: 0, 2: 0, 3: 100}; DF = {1: 40, 2: 60, 3: 50}
for L in (80, 120, 170, 180, 181, 200, 205, 300):
    a1, a2, a3, x, u = wf(L, IM, DF, 30, 3)
    say(f"L03 Ex1.5 L={L}: margin={a1} df={a2} cap={a3} m1={x[1]} m2={x[2]} u={u} sum_ok={a1+a2+a3+sum(x.values())+u==L}")
IM2 = {4: 0, 1: 0, 2: 0, 3: 0}; DF2 = {1: 1, 2: 1, 3: 1, 4: 0}
for L in (1, 2):
    a1, a2, a3, x, u = wf(L, IM2, DF2, 0, 4)
    say(f"L03 Ex1.6 L={L}: x={x} u={u}")
# Prop 1.2 / 1.3 / Remark 1.4 random checks
rr = random.Random(11)
bad = 0
for _ in range(20000):
    m = rr.randint(2, 5)
    dflt = rr.randint(1, m)
    IMr = {i: rr.randint(0, 60) for i in range(1, m + 1)}
    DFr = {i: rr.randint(0, 40) for i in range(1, m + 1)}
    Kr = rr.randint(0, 50)
    L = rr.randint(0, 250)
    a1, a2, a3, x, u = wf(L, IMr, DFr, Kr, dflt)
    if a1 + a2 + a3 + sum(x.values()) + u != L: bad += 1
    surv = [i for i in DFr if i != dflt]
    D = sum(DFr[i] for i in surv)
    Z = L - a1 - a2 - a3
    if Z < D:
        if any(x[i] > DFr[i] for i in surv): bad += 1
        npos = sum(1 for i in surv if DFr[i] > 0)
        ell = Z - sum(x.values())
        if not (0 <= ell <= max(npos - 1, 0)) and D > 0: bad += 1
        for i in surv:
            if DFr[i] > 0 and x[i] + 1 > DFr[i] and False: bad += 1
    if a2 > 0 and a1 != IMr[dflt]: bad += 1
    if a3 > 0 and a2 != DFr[dflt]: bad += 1
    if Z > 0 and a3 != Kr: bad += 1
say(f"L03 random Prop1.2/1.3/Rem1.4 mismatches={bad}")

# Prop 2.3 and Cor 2.4 check, brute force
def k_of(t, S): return ceil(Fraction(t * S, 10000))
rr = random.Random(13)
bad = 0
for _ in range(400):
    S = rr.randint(1, 60)
    losses = [rr.randint(0, 200) for _ in range(S)]
    srt = sorted(losses)
    for t in [rr.randint(1, 10000), 9900, 9975, 10000, 1]:
        k = k_of(t, S)
        assert 1 <= k <= S
        sized = srt[k - 1]
        def cover(M): return floor(Fraction(10000 * sum(1 for l in losses if l <= M), S))
        brute = next(M for M in range(0, max(losses) + 1) if cover(M) >= t)
        if brute != sized or cover(sized) < t or (sized > 0 and cover(sized - 1) >= t): bad += 1
say(f"L03 random Prop 2.3 brute-force mismatches={bad}")
# R3: k==S iff S<=399 for 9975
first = [S for S in range(1, 2000) if k_of(9975, S) != S]
say(f"L03 R3: first S with k<S for 9975 is {first[0]}; all S<=399 have k=S: {all(k_of(9975,S)==S for S in range(1,400))}")
say(f"L03 R3: k(400)={k_of(9975,400)} ; Quiz 400 scenarios k={k_of(9975,400)}")
# R2 S=100
say(f"L03 R2: S=100 k(9900)={k_of(9900,100)} k(10000)={k_of(10000,100)}")
# Example 2.5
say(f"L03 Ex2.5 S=200: k(9900)={k_of(9900,200)} (9900*200/10000={Fraction(9900*200,10000)}), k(9975)={k_of(9975,200)} ({Fraction(9975*200,10000)})")
# Lab Part B values
rng = random.Random(2026)
IMl = {i: rng.randint(1000, 5000) for i in (1, 2, 3, 4)}
DFl = {i: rng.randint(100, 900) for i in (1, 2, 3, 4)}
Kl = rng.randint(500, 2000)
say(f"L03 lab inputs IM={IMl} DF={DFl} K={Kl}")
losses = [rng.randint(0, 3000) for _ in range(200)]
srt = sorted(losses)
for t in (9900, 9975):
    k = k_of(t, 200)
    M = srt[k - 1]
    c_at = sum(1 for l in losses if l <= M)
    say(f"L03 lab Part B t={t}: k={k} sized={M} count_le_sized={c_at} count_above={200-c_at} count_le_sized_minus1={sum(1 for l in losses if l<=M-1)}")
    above = sorted(losses)[-2:] if t == 9900 else []
    if t == 9900:
        say(f"L03 t=9900 two largest losses {above}; both strictly above sized: {all(x > M for x in above)}")
        # claim: changing the two largest, keeping each >= sized margin, leaves sized margin unchanged
        rr2 = random.Random(5)
        ok = True
        for _ in range(2000):
            new = losses[:]
            idx = sorted(range(200), key=lambda i: new[i])[-2:]
            for i in idx:
                new[i] = rr2.randint(M, 3000)
            if sorted(new)[k - 1] != M: ok = False; break
        say(f"L03 claim 'stays at or above keeps sized margin' holds on 2000 random edits: {ok}")
        # lowering one below margin changes it?
        new = losses[:]
        new[idx[0]] = M - 1
        say(f"L03 lowering a top loss below margin changes sized margin: {sorted(new)[k-1] != M}")
        # Example 2.5 check: 'Lab 1 prints cover 9900 at sized margin' => 198 at or below
        say(f"L03 cover at sized (9900) = {floor(Fraction(10000*c_at,200))} bps")
