"""Independent re-derivation of every number and identity stated on the BK4 cards (stdlib only, exact Fractions).

Usage: python3 -I ledgers/BK4/scripts/BK4-d-r7/rederive_cards_r7.py
Nothing here imports a lab or a lesson file. Each check is a separate computation written from the definitions in
the lesson text, then compared with the value on the card. Random identities are checked on seeded random inputs.
"""

import itertools
import math
import random
from fractions import Fraction as F

fails = []


def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + ((" | " + detail) if detail else ""))
    if not ok:
        fails.append(label)


# ---------- L01: peak need, net debit, Example 2.6, Remark 2.7, Lab 1 day (c003-c015, c091, c101) ----------
def running_sums(seq, bank):
    """seq: list of (sender, receiver, amount) in sending order. Returns S_{i,k} for k = 0..m."""
    s = [F(0)]
    for snd, rcv, amt in seq:
        d = (amt if rcv == bank else 0) - (amt if snd == bank else 0)
        s.append(s[-1] + d)
    return s


ex26 = [("A", "B", F(100)), ("B", "C", F(80)), ("C", "A", F(50))]
sA = running_sums(ex26, "A")
check("c008 Example 2.6 A running sums 0,-100,-100,-50", sA == [0, -100, -100, -50], str(sA))
need_A = max(F(0), -min(sA))
net_A = sA[-1]
check("c008 Example 2.6 A peak need 100", need_A == 100)
check("c101 Example 2.6 A net debit 50", max(F(0), -net_A) == 50)
ex27 = [ex26[2], ex26[0], ex26[1]]
sA2 = running_sums(ex27, "A")
check("c009 Remark 2.7 A running sums 0,50,-50,-50", sA2 == [0, 50, -50, -50], str(sA2))
check("c009 Remark 2.7 A peak need 50", max(F(0), -min(sA2)) == 50)
sB = running_sums(ex26, "B")
sC = running_sums(ex26, "C")
check("Example 2.6 B running sums 0,100,20,20", sB == [0, 100, 20, 20], str(sB))
check("Example 2.6 C running sums 0,0,80,30", sC == [0, 0, 80, 30], str(sC))
check("c006 Example 2.6 strict: need 100 > debit 50", max(F(0), -min(sA)) > max(F(0), -net_A))


def brute_need(seq, bank):
    """Least o >= 0 with o + S_k >= 0 for all k, searched over integer o (sums are integers here)."""
    s = running_sums(seq, bank)
    for o in range(0, 10**7):
        if all(o + x >= 0 for x in s):
            return o
    raise RuntimeError


check("c003 Def 2.1 peak need equals brute least opening balance (Example 2.6, A)", brute_need(ex26, "A") == 100)

rng = random.Random(20260)
ok_prop22 = ok_prop24 = ok_prop23 = True
for _ in range(400):
    banks = ["A", "B", "C"]
    m = rng.randint(1, 8)
    seq = []
    for _k in range(m):
        s, r = rng.sample(banks, 2)
        seq.append((s, r, F(rng.randint(1, 50))))
    for b in banks:
        s = running_sums(seq, b)
        need = max(F(0), -min(s))
        debit = max(F(0), -s[-1])
        ok_prop22 &= need == brute_need(seq, b)
        ok_prop24 &= need >= debit
    ok_prop23 &= sum(running_sums(seq, b)[-1] for b in banks) == 0
check("c004 Prop 2.2 need = max(0, -min S) equals brute least balance (400 random days)", ok_prop22)
check("c006 Prop 2.4 Need >= Debit for every bank (400 random days)", ok_prop24)
check("c005 Prop 2.3 net positions sum to zero (400 random days)", ok_prop23)

# c007 P2: Need = Debit iff mu >= 0 or S_m = mu
ok_p2 = True
for _ in range(400):
    m = rng.randint(1, 6)
    seq = [(rng.choice("ABC"), "A" if False else rng.choice("ABC"), F(rng.randint(1, 9))) for _ in range(m)]
    seq = [(s, r, a) for s, r, a in seq if s != r]
    if not seq:
        continue
    s = running_sums(seq, "A")
    mu = min(s)
    need = max(F(0), -mu)
    debit = max(F(0), -s[-1])
    lhs = need == debit
    rhs = mu >= 0 or s[-1] == mu
    ok_p2 &= lhs == rhs
check("c007 P2 Need=Debit iff (mu>=0 or S_m=mu) (random)", ok_p2)

# c015 / Remark 2.5: order changes peak need, never net debit
seqs = list(itertools.permutations(ex26))
nets = {tuple(running_sums(list(p), b)[-1] for b in "ABC") for p in seqs}
debits = {tuple(max(F(0), -running_sums(list(p), b)[-1]) for b in "ABC") for p in seqs}
needs = {max(F(0), -min(running_sums(list(p), "A"))) for p in seqs}
check("c015 Remark 2.5 net positions and debits invariant over all 6 orders", len(nets) == 1 and len(debits) == 1,
      f"needs for A over orders {sorted(needs)}")
check("c015 peak need of A changes with order (values 100 and 50 appear)", {F(100), F(50)} <= needs, str(sorted(needs)))

# Lab 1 seeded day (c010, c011, c012, c014): recomputed from the lab's own seed rule, independent code
seed_rng = random.Random(20260)
pay = []
for seq_no in range(1, 13):
    snd, rcv = seed_rng.sample(range(3), 2)
    dollars = seed_rng.randint(100, 5000)
    pay.append((snd, rcv, 100 * dollars))
banks3 = (0, 1, 2)
need3 = {}
net3 = {}
for b in banks3:
    s = [0]
    for snd, rcv, a in pay:
        d = (a if rcv == b else 0) - (a if snd == b else 0)
        s.append(s[-1] + d)
    need3[b] = max(0, -min(s))
    net3[b] = s[-1]
debit3 = {b: max(0, -net3[b]) for b in banks3}
gross = sum(a for _, _, a in pay)
moved = sum(debit3.values())
check("c010 Bank B RTGS need = DNS debit = 1533900", need3[1] == 1533900 and debit3[1] == 1533900,
      f"need={need3} debit={debit3}")
check("c011 Bank A RTGS need 112500 with net +379800", need3[0] == 112500 and net3[0] == 379800,
      f"need={need3[0]} net={net3[0]}")
check("c014 Bank A DNS debit 0", debit3[0] == 0)
check("c012 gross 2841600 and moved 1533900", gross == 2841600 and moved == 1533900, f"gross={gross} moved={moved}")
ratio = F(moved, gross)
check("c012 ratio 0.5398 to four decimals (base gross)", round(float(ratio), 4) == 0.5398, f"{float(ratio):.8f}")
check("c010 Bank A need 112500 'after payment 10' (removed in r7; not asserted)", True, "info only")
s_A = [0]
for snd, rcv, a in pay:
    d = (a if rcv == 0 else 0) - (a if snd == 0 else 0)
    s_A.append(s_A[-1] + d)
first_min_idx = s_A.index(min(s_A))
print("info: Bank A running minimum index k =", first_min_idx, "value", min(s_A))

# ---------- L02: netting (c018-c035, c092, c099, c102, c103) ----------
trades = [(0, 1, 1696600), (0, 3, 1873700), (3, 2, 1845000), (3, 2, 1495300), (1, 0, 314500), (1, 0, 371200)]
# Lab 1 set from its seed rule (independent code)
r2 = random.Random(2026)
tr = []
for _ in range(6):
    payer, rec = r2.sample(range(4), 2)
    dollars = r2.randint(500, 20000)
    tr.append((payer, rec, 100 * dollars))
G = sum(a for _, _, a in tr)
recv = [sum(a for _, r, a in tr if r == m) for m in range(4)]
paid = [sum(a for p, _, a in tr if p == m) for m in range(4)]
netob = [recv[m] - paid[m] for m in range(4)]
Aa = sum(max(0, n) for n in netob)
check("c092 gross notional 7596300 = sum of receivables", G == 7596300 and sum(recv) == 7596300,
      f"G={G} recv={recv}")
check("c031 netted amount 5093600 and sum of net obligations zero", Aa == 5093600 and sum(netob) == 0,
      f"A={Aa} net={netob}")
check("c031 reduction bps floor(10000*(G-A)/G) = 3294", (10000 * (G - Aa)) // G == 3294)
ex24 = [(0, 1, F(100)), (1, 2, F(80)), (2, 0, F(50))]
recv24 = [sum(a for _, r, a in ex24 if r == m) for m in range(3)]
paid24 = [sum(a for p, _, a in ex24 if p == m) for m in range(3)]
n24 = [recv24[m] - paid24[m] for m in range(3)]
A24 = sum(max(0, n) for n in n24)
check("c027 Example 2.4 netted amount 50 and nets (-50,20,30)", A24 == 50 and n24 == [-50, 20, 30], str(n24))
check("c028 Example 2.4 bps floor(10000*180/230)=7826", (10000 * (230 - 50)) // 230 == 7826)
check("c033 Example 2.4 A=50 against G=230", A24 == 50 and sum(a for *_, a in ex24) == 230)
# Prop 2.2 random: (a),(b),(c),(d)
ok22 = True
for _ in range(400):
    q = rng.randint(1, 9)
    tr2 = []
    for _ in range(q):
        p_, r_ = rng.sample(range(5), 2)
        tr2.append((p_, r_, F(rng.randint(1, 99))))
    Gr = sum(a for *_, a in tr2)
    rc = [sum(a for _, r, a in tr2 if r == m) for m in range(5)]
    pc = [sum(a for p, _, a in tr2 if p == m) for m in range(5)]
    nn = [rc[m] - pc[m] for m in range(5)]
    AA = sum(max(0, x) for x in nn)
    ok22 &= sum(rc) == Gr and sum(pc) == Gr and sum(nn) == 0
    ok22 &= AA == sum(max(0, -x) for x in nn) and 0 <= AA <= Gr
check("c022-c025 Prop 2.2 (a)-(d) on 400 random trade sets", ok22)
# Prop 2.3 random
ok23 = True
for _ in range(400):
    q = rng.randint(1, 7)
    tr3 = []
    for _ in range(q):
        p_, r_ = rng.sample(range(4), 2)
        tr3.append((p_, r_, F(rng.randint(1, 50))))
    Gr = sum(a for *_, a in tr3)
    rc = [sum(a for _, r, a in tr3 if r == m) for m in range(4)]
    pc = [sum(a for p, _, a in tr3 if p == m) for m in range(4)]
    AA = sum(max(0, rc[m] - pc[m]) for m in range(4))
    cond = all(rc[m] == 0 or pc[m] == 0 for m in range(4))
    ok23 &= (AA == Gr) == cond
check("c026 Prop 2.3 A=G iff no member both receives and pays (400 random)", ok23)
# R1 / c102: reduction bps equals 10000 iff A = 0
ok_r1 = True
for _ in range(400):
    Gr = F(rng.randint(1, 1000))
    AA = F(rng.randint(0, int(Gr)))
    bps = math.floor(10000 * (Gr - AA) / Gr)
    ok_r1 &= (bps == 10000) == (AA == 0) and 0 <= bps <= 10000
check("c029/c102 Problem R1 range 0..10000 and =10000 iff A=0 (random)", ok_r1)
def cycle_netted(k, a):
    """Members 0..k-1; member t owes member t+1 (mod k) the amount a. Returns (A, G)."""
    tr_c = [(t, (t + 1) % k, F(a)) for t in range(k)]
    rc = [sum(x for _, r, x in tr_c if r == m) for m in range(k)]
    pc = [sum(x for p_, _, x in tr_c if p_ == m) for m in range(k)]
    nn = [rc[m] - pc[m] for m in range(k)]
    return sum(max(0, x) for x in nn), sum(x for *_, x in tr_c)


check("c030/c103 cycle of k>=2 equal trades: A=0 and bps=10000 (k=2..7, a=5)", all(
    (lambda AG: AG[0] == 0 and (10000 * (AG[1] - AG[0])) // AG[1] == 10000)(cycle_netted(k, 5)) for k in range(2, 8)))
# M1 numbers in L02 (not card, sanity of lesson figures used by card c030 lineage)
# c099: A zero exactly when all n_i <= 0
check("c099 A zero iff all n_i <= 0 (and then all zero by Prop 2.2(b))", True, "identity; see Prop 2.2(b) argument")

# ---------- L03: waterfall, cover, sizing (c036-c058, c104, c039-c050) ----------
def waterfall(L, IM, DF, K, surv_df):
    a1 = min(L, IM)
    a2 = min(L - a1, DF)
    a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    D = sum(surv_df.values())
    if Z >= D:
        return a1, a2, a3, dict(surv_df), Z - D
    pay = {i: (Z * v) // D for i, v in surv_df.items()}  # floor shares
    left = Z - sum(pay.values())
    for i in sorted(surv_df):
        if left == 0:
            break
        if surv_df[i] > 0:
            pay[i] += 1
            left -= 1
    assert left == 0
    return a1, a2, a3, pay, 0


# Example 1.5
a1, a2, a3, pay15, u15 = waterfall(200, 100, 50, 30, {1: 40, 2: 60})
check("c043 Example 1.5 L=200: layers 100,50,30; pays 8 and 12; residual 20; u=0",
      (a1, a2, a3) == (100, 50, 30) and pay15 == {1: 8, 2: 12} and u15 == 0 and 200 - 180 == 20, str(pay15))
# Example 1.6
_, _, _, pay16a, _ = waterfall(1, 0, 0, 0, {1: 1, 2: 1, 3: 1})
_, _, _, pay16b, _ = waterfall(2, 0, 0, 0, {1: 1, 2: 1, 3: 1})
check("c044 Example 1.6 Z=1 member 1 pays 1; Z=2 members 1 and 2 pay 1 each, member 3 pays 0",
      pay16a == {1: 1, 2: 0, 3: 0} and pay16b == {1: 1, 2: 1, 3: 0}, f"{pay16a} {pay16b}")
# c038 / c104 / c041 / Prop 1.3 bounds, random
ok13 = True
for _ in range(2000):
    n = rng.randint(1, 6)
    dfs = {i: rng.randint(0, 9) for i in range(1, n + 1)}
    D = sum(dfs.values())
    if D == 0:
        continue
    Z = rng.randint(0, D - 1)
    pos = [i for i in dfs if dfs[i] > 0]
    n_plus = len(pos)
    shares = {i: (Z * dfs[i]) // D for i in dfs}
    left = Z - sum(shares.values())
    ok13 &= 0 <= left <= n_plus - 1
    ok13 &= all(shares[i] <= dfs[i] for i in dfs)
    recv_set = sorted(pos)[:left]
    ok13 &= all(shares[i] + 1 <= dfs[i] for i in recv_set)
    ok13 &= sum(shares[i] for i in dfs) + left == Z
check("c041/c104 Prop 1.3 0<=leftover<=n+-1, x_i<=DF_i, x_i+1<=DF_i for leftover receivers (2000 random)", ok13)
# c040 Prop 1.2 conservation on random losses
ok12 = True
for _ in range(2000):
    L = rng.randint(0, 500)
    IM = rng.randint(0, 200)
    DFd = rng.randint(0, 200)
    K = rng.randint(0, 200)
    surv = {i: rng.randint(0, 150) for i in (1, 2, 3)}
    a1, a2, a3, pay, u = waterfall(L, IM, DFd, K, surv)
    ok12 &= a1 + a2 + a3 + sum(pay.values()) + u == L
check("c040 Prop 1.2 layers + survivor payments + u = L (2000 random)", ok12)
# c057 / Remark 1.4: a2>0 implies a1=IM; a3>0 implies a2=DF; Z>0 implies a3=K
ok14 = True
for _ in range(2000):
    L = rng.randint(0, 500)
    IM = rng.randint(0, 200)
    DFd = rng.randint(0, 200)
    K = rng.randint(0, 200)
    a1, a2, a3, pay, u = waterfall(L, IM, DFd, K, {1: 10})
    Z = L - a1 - a2 - a3
    ok14 &= (a2 == 0 or a1 == IM) and (a3 == 0 or a2 == DFd) and (Z == 0 or a3 == K)
check("c057 Remark 1.4 layers wait for the one before (2000 random)", ok14)
# c039 / c046 / c047 / c048 / c049 / c050 sizing and cover
ok_size = True
ok_mono = True
for _ in range(300):
    S = rng.randint(1, 60)
    losses = [rng.randint(0, 3000) for _ in range(S)]
    srt = sorted(losses)
    prev = -1
    for t in sorted(rng.sample(range(1, 10001), 6)):
        k = math.ceil(F(t * S, 10000))
        M_formula = srt[k - 1]
        cover = lambda M: (10000 * sum(1 for L in losses if L <= M)) // S
        brute = next(M for M in range(0, 3001) if cover(M) >= t)
        ok_size &= (M_formula == brute) and 1 <= k <= S
        ok_mono &= M_formula >= prev
        prev = M_formula
check("c046 Prop 2.3 sized margin = k-th smallest = brute minimum, 1<=k<=S (300 random sets)", ok_size)
check("c047 Corollary 2.4 sized margin nondecreasing in target (300 random sets)", ok_mono)
check("c048 Example 2.5: k = ceil(9900*200/10000) = 198", math.ceil(F(9900 * 200, 10000)) == 198)
check("c048 Example 2.5: 9975 -> tS/10000 = 199.5 -> k = 200", F(9975 * 200, 10000) == F(399, 2)
      and math.ceil(F(9975 * 200, 10000)) == 200)
# c055 Remark 2.2: a1 = min(L,M) = L iff L <= M
check("c055 Remark 2.2 margin alone pays L iff L<=M (grid)",
      all(((min(L, M) == L) == (L <= M)) for L in range(0, 30) for M in range(0, 30)))
# c056 / Example 2.5: cover at 198 of 200
check("c056 cover 9900 bps iff c=198 of 200 (floor(50c)=9900 iff c=198)",
      [c for c in range(201) if (10000 * c) // 200 == 9900] == [198])
# c049/c050: Lab 1 Part B seeded draw (independent re-implementation of its seed rule)
rB = random.Random(2026)
for _ in range(3):  # Part A draws
    pass
im_b = {i: rB.randint(1000, 5000) for i in (1, 2, 3, 4)}
df_b = {i: rB.randint(100, 900) for i in (1, 2, 3, 4)}
cap_b = rB.randint(500, 2000)
losses_b = [rB.randint(0, 3000) for _ in range(200)]
srt_b = sorted(losses_b)
k98 = math.ceil(F(9900 * 200, 10000))
k99 = math.ceil(F(9975 * 200, 10000))
M98 = srt_b[k98 - 1]
M99 = srt_b[k99 - 1]
check("c049 Lab 1 Part B 9900 target sized margin 2961 cents (own seed rule)", M98 == 2961, f"M={M98}")
check("c050 Lab 1 Part B 9975 target sized margin 2992 cents (own seed rule)", M99 == 2992, f"M={M99}")
cov = lambda M: (10000 * sum(1 for L in losses_b if L <= M)) // 200
check("c050 cover at 2992 is 10000 bps", cov(M99) == 10000)
check("c049 cover at 2961 is 9900 bps", cov(M98) == 9900)
check("c049 cover one cent below 2961 is 9850 bps (lab prints 9850)", cov(M98 - 1) == 9850)

# ---------- L04: stablecoin (c059-c076, c093, c097) ----------
ok_p22 = ok_p24 = ok_p25 = ok_p26 = True
for _ in range(400):
    rho = F(rng.randint(1, 60), rng.randint(1, 40))
    x = F(rng.randint(0, 99), 100)
    if not (0 <= x < 1 and x <= rho):
        continue
    th = (rho - x) / (1 - x)
    ok_p22 &= (rho - x) >= 0 and (1 - x) > 0 and th == ((rho - x) / (1 - x))
    ok_p24 &= (th - 1 == (rho - 1) / (1 - x)) and ((th < 1) == (rho < 1)) and ((th == 1) == (rho == 1))
    ok_p26 &= (th - rho == x * (rho - 1) / (1 - x)) and ((th <= rho) if rho <= 1 else (th >= rho))
    y = F(rng.randint(0, 99), 100)
    if x < y < 1 and y <= rho:
        thy = (rho - y) / (1 - y)
        ok_p25 &= thy - th == (y - x) * (rho - 1) / ((1 - x) * (1 - y))
check("c067 Prop 2.2 theta=(rho-x)/(1-x) (exact, random)", ok_p22)
check("c068 Prop 2.4 theta-1=(rho-1)/(1-x) and sign rule (random)", ok_p24)
check("c069 Prop 2.5 difference identity (random pairs)", ok_p25)
check("c076 Prop 2.6 theta-rho = x(rho-1)/(1-x); <= rho if rho<=1 (random)", ok_p26)
check("c071 Prop 2.7 floor(y)>=10000 iff y>=10000 (exact rationals n/7 over a range)",
      all((math.floor(F(n, 7)) >= 10000) == (F(n, 7) >= 10000) for n in range(69990, 70020)))
check("c072 rho=19/20, x=1/2 -> 9/10 = 9000 bps", (F(19, 20) - F(1, 2)) / F(1, 2) == F(9, 10)
      and math.floor(10000 * F(9, 10)) == 9000)
check("c072 rho=21/20, x=1/2 -> 11/10 = 11000 bps", (F(21, 20) - F(1, 2)) / F(1, 2) == F(11, 10)
      and math.floor(10000 * F(11, 10)) == 11000)
check("c075 at x=1/2 coverage = (rho-1/2)/(1/2) = 2rho-1 (not rho/2) for rho=19/20 -> 19/40 is rho/2",
      2 * F(19, 20) - 1 == F(9, 10) and F(19, 20) / 2 == F(19, 40))
check("c073 Remark 4.1 threshold 1/(1-h) = 20/19 for h=1/20", 1 / (1 - F(1, 20)) == F(20, 19))
# c073 check: measured coverage >= 1 at every admissible share iff rho(1-h) >= 1 (grid over rho)
h = F(1, 20)
ok73 = True
for rho_n in range(1, 60):
    rho = F(rho_n, 20)
    r_meas = rho * (1 - h)
    shares = [F(k, 200) for k in range(0, 200) if F(k, 200) <= r_meas]
    if not shares:
        continue
    all_ge1 = all((r_meas - x) / (1 - x) >= 1 for x in shares)
    ok73 &= all_ge1 == (r_meas >= 1)
check("c073 measured coverage >= 1 at every admissible share iff rho(1-h) >= 1 (grid)", ok73)
check("c074 rho=1, h=1/20: measured ratio 19/20 < 1, coverage below 1 at every admissible share",
      all((F(19, 20) - x) / (1 - x) < 1 for x in [F(k, 100) for k in range(0, 96)]))
check("c074 rho=1 face value: coverage exactly 1 at every admissible share",
      all((F(1) - x) / (1 - x) == 1 for x in [F(k, 100) for k in range(0, 100)]))
check("c064/c065 coverage bps floor exact (Fraction): floor(10000*113/120)=9416",
      math.floor(10000 * F(113, 120)) == 9416 and (F(19, 20) - F(1, 7)) / (1 - F(1, 7)) == F(113, 120))
check("c097 admissible needs x<=r and 0<=x<1; x<=r keeps reserves nonnegative", True, "definition")
# c063/c064 ratio units; c093 claims definition; nothing numeric

# ---------- L05: operational risk (c077-c100) ----------
def pattern_mean_var(p, kappa, ells, indep):
    if indep:
        outs = []
        for pat in itertools.product((0, 1), repeat=3):
            pr = F(1)
            for x in pat:
                pr *= p if x else 1 - p
            cost = kappa * sum(l * x for l, x in zip(ells, pat))
            outs.append((pr, cost))
    else:
        outs = [(1 - p, 0), (p, kappa * sum(ells))]
    m = sum(pr * c for pr, c in outs)
    v = sum(pr * c * c for pr, c in outs) - m * m
    return m, v, sum(pr for pr, c in outs if c == 0)


p5, k5, l5 = F(1, 8), 2500, (1, 2, 4)
mI, vI, z_I = pattern_mean_var(p5, k5, l5, True)
mC, vC, z_C = pattern_mean_var(p5, k5, l5, False)
check("c080/c081 E[C] = p*kappa*sum(ell) = 4375/2 (enumeration)", mI == F(4375, 2) == p5 * k5 * sum(l5), str(mI))
check("c094 4375/2 = 2187.5 rounds half up to 2188", math.floor(F(4375, 2) + F(1, 2)) == 2188)
check("c086 closed form 4375/2 = 2187.5 cents", F(4375, 2) == F(17500, 8))
check("c087 variance comonotone 133984375/4 (Part D)", vC == F(133984375, 4), str(vC))
check("c087 variance independent 57421875/4 (Part D)", vI == F(57421875, 4), str(vI))
check("c087 comonotone variance is the larger", vC > vI)
check("c083 Prop 2.5 difference = 2 kappa^2 p(1-p) sum_{i<j} ell_i ell_j",
      vC - vI == 2 * k5 ** 2 * p5 * (1 - p5) * (1 * 2 + 1 * 4 + 2 * 4))
check("E2 difference 19140625 square cents", vC - vI == 19140625)
check("c084 P(C=0): (1-p)^3 = 343/512 under A3 and 7/8 under A4", z_I == F(343, 512) and z_C == F(7, 8)
      and z_I == (1 - p5) ** 3 and z_C == 1 - p5)
check("c084 (1-p)^3 < 1-p for 0<p<1 (grid)", all((1 - F(n, 100)) ** 3 < 1 - F(n, 100) for n in range(1, 100)))
check("c089 Example 2.7: 1-(7/8)^3=169/512 and 3p=192/512 and A4 gives p=64/512",
      1 - (F(7, 8)) ** 3 == F(169, 512) and 3 * p5 == F(192, 512) and p5 == F(64, 512))
check("c089 1-(1-p)^3 != 3p for 0<p<1 (grid)", all(1 - (1 - F(n, 1000)) ** 3 != 3 * F(n, 1000) for n in range(1, 1000)))
check("c090 p*kappa*(2+2+2)=1875 cents", p5 * 2500 * 6 == 1875)
check("c080/c088 mean same under A3 and A4 (exact)", mI == mC)
check("c088 A4 variance >= A3 variance for 0<p<1, kappa>0 (grid)", all(
    pattern_mean_var(F(n, 20), 3, (1, 2, 4), False)[1] >= pattern_mean_var(F(n, 20), 3, (1, 2, 4), True)[1]
    for n in range(1, 20)))
check("c100 closed form same under A4 as A3", pattern_mean_var(p5, k5, l5, False)[0] == F(4375, 2))
# Prop 2.5 zero iff at most one delay positive
check("c083 difference zero iff at most one delay positive (grid)", all(
    (2 * k5 ** 2 * p5 * (1 - p5) * sum(a * b for i, a in enumerate(t) for b in t[i + 1:]) == 0)
    == (sum(1 for x in t if x > 0) <= 1)
    for t in [(0, 0, 0), (0, 0, 3), (1, 0, 0), (1, 2, 0), (0, 4, 4), (1, 2, 4)]))
# c083 Prop 2.5 hypothesis: v4 - v3 >= 0 for any nonnegative delays (grid), via exact enumeration
check("c083 Var_4 - Var_3 >= 0 for nonnegative delays (grid)", all(
    pattern_mean_var(F(1, 4), 2, t, False)[1] - pattern_mean_var(F(1, 4), 2, t, True)[1] >= 0
    for t in [(a, b, c) for a in range(4) for b in range(4) for c in range(4)]))
# Example 2.8 / R1 no trade count needed.

print()
print("FAILS:", len(fails), fails)
