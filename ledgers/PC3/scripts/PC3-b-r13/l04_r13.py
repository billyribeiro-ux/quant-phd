import random
from fractions import Fraction as F
def game(seed, N=20):
    r = random.Random(seed)
    v = [10000]; arr = []
    for t in range(N):
        mv = 5 if r.random() < 0.5 else -5
        v.append(v[-1] + mv)
        u = r.random()
        arr.append("ub" if u < 0.25 else ("us" if u < 0.5 else "inf"))
    return v, arr
def run(seed, N=20, L=10):
    v, arr = game(seed, N)
    inv = 0; cash = 0; last = None; fills = []; informed = 0; log = []
    for t in range(1, N+1):
        mid = 10000 if last is None else last
        b, a = mid-10, mid+10
        A = arr[t-1]
        informed += A == "inf"
        if A == "ub": side = -1
        elif A == "us": side = 1
        else:
            side = -1 if v[t] > a else (1 if v[t] < b else 0)
        filled = side != 0 and abs(inv+side) <= L
        if filled:
            price = a if side < 0 else b
            cf = -side*price; inv += side; cash += cf; last = price; fills.append(cf)
        log.append((t, b, a, A, filled, inv, cash))
    settle = v[N]
    return dict(v=v, fills=len(fills), cf=sum(fills), inv=inv, settle=settle, pnl=cash+inv*settle, informed=informed, maxinv=max(abs(x[5]) for x in log), log=log)
r0 = run(0); r1 = run(1)
print("seed0 fills", r0["fills"], "cf", r0["cf"], "inv", r0["inv"], "settle", r0["settle"], "pnl", r0["pnl"], "informed", r0["informed"], "maxinv", r0["maxinv"])
print("seed1 fills", r1["fills"], "cf", r1["cf"], "inv", r1["inv"], "settle", r1["settle"], "pnl", r1["pnl"])
print("seed0 path first 6", r0["v"][:6], "mid final", 10000-10*0 if False else None)
# final mid per rule and mark check
last_mid = None
# Remark 2.4: final mid of seed 0 = last fill price + quote rule
mid_final = 10000 - 10*r0["inv"] if False else (10000 - 10*r0["log"][-2][5])  # quote mid at turn 20 = 10000 - 10*I_19
print("seed0 final quote mid", mid_final, "marked at mid vs settle diff", (mid_final-r0["settle"]) * r0["inv"])
# mid identity 10000 - 10*I_{t-1}
ok = True; inv=0; last=None
for t,(tt,b,a,A,f,iv,c) in enumerate(r0["log"], start=1):
    mid = 10000 if last is None else last
    if mid != 10000-10*inv: ok=False
    if f:
        pass
    inv_before = inv
    inv = iv
    if f:
        last = a if iv < inv_before else b
print("mid == 10000-10*I_{t-1} along seed 0:", ok)
# Part 2 closed form check over grid with exact Fraction (independent)
ARR = {"ub": F(1,4), "us": F(1,4), "inf": F(1,2)}
def one(v, b, a):
    tot = F(0)
    for A,p in ARR.items():
        if A=="ub": side=-1
        elif A=="us": side=1
        else: side = -1 if v>a else (1 if v<b else 0)
        if side==0: continue
        price = a if side<0 else b
        tot += p*(-side*price + side*v)
    return tot
def cf(v,b,a):
    h = F(a-b,2)
    return h/2 - F(max(v-a,0)+max(b-v,0),2)
print("grid", [(v, str(one(v,9990,10010)), one(v,9990,10010)==cf(v,9990,10010)) for v in range(9980,10025,5)])
# broader grid for the closed form (checks Prop 3.1 beyond the page's grid)
bad = [v for v in range(9900,10100) if one(v,9990,10010)!=cf(v,9990,10010)]
print("Prop3.1 mismatches on 9900..10099 (1-cent grid):", bad[:5], len(bad))
# Example 3.2 values
print("Ex3.2", cf(10000,10010,9990) if False else cf(10000,9990,10010), cf(10020,9990,10010), cf(9985,9990,10010))
# inventory 10 case: quote 9990/10010, v=10000, uninformed buy only -> 10 * 1/4
print("I=10 expected trade term", F(10,4) if True else None)
# Remark 4.2: fill refused at |I|=L; check informed and sell refusal not needed here
# Sample alternatives: check informed count and P&L for seed 0 again from its own log
print("seed0 informed positions", [t for t,(tt,b,a,A,f,iv,c) in enumerate(r0["log"],1) if A=="inf"])
