"""Independent re-derivation of the numbers printed or stated on BK4 slice a (index, L01, L02, L03).

Written by the BK4-a round-2 verifier. It re-implements the arithmetic from the page text (Fraction and
integer floor/ceiling), not by calling the lab twins. The seeded draws follow the lab's documented call
order (random.Random(seed).sample / randint), because the printed day is the seeded output.
Run: python3 -I ledgers/BK4/scripts/BK4-a-r2/rederive_slice_a.py
"""

import math
import random
from fractions import Fraction

OK = []
BAD = []


def check(name: str, got: object, want: object) -> None:
    (OK if got == want else BAD).append(f"{name}: got {got!r} want {want!r}")


# ---------- L01: seeded day (seed 20260), Propositions 2.2-2.4, Example 2.6, Remark 2.7, Remark 3.1 ----------
rng = random.Random(20260)
day = []
for seq in range(1, 13):
    sender, receiver = rng.sample(range(3), 2)
    dollars = rng.randint(100, 5000)
    day.append((seq, sender, receiver, 100 * dollars))

def net(bank: int, d: list) -> int:
    return sum(a for _, s, r, a in d if r == bank) - sum(a for _, s, r, a in d if s == bank)

def rtgs_need(bank: int, d: list) -> int:
    bal = 0
    low = 0
    for _, s, r, a in d:
        if s == bank:
            bal -= a
        elif r == bank:
            bal += a
        low = min(low, bal)
    return -low

nets = [net(b, day) for b in range(3)]
needs = [rtgs_need(b, day) for b in range(3)]
debits = [max(0, -n) for n in nets]
check("L01 net positions", nets, [379800, -1533900, 1154100])
check("L01 RTGS need", needs, [112500, 1533900, 0])
check("L01 DNS debit", debits, [0, 1533900, 0])
check("L01 sum of nets zero", sum(nets), 0)
check("L01 need >= debit each bank", all(n >= d for n, d in zip(needs, debits)), True)
gross = sum(a for *_, a in day)
check("L01 gross cents", gross, 2841600)
check("L01 moved under DNS", sum(debits), 1533900)
ratio = Fraction(1533900, 2841600)
check("L01 ratio 4dp half-up", math.floor(ratio * 10000 + Fraction(1, 2)) / 10000, 0.5398)
check("L01 ratio first digits", float(ratio) > 0.539801 and float(ratio) < 0.539802, True)
check("L01 banks positive debit", sum(1 for d in debits if d > 0), 1)
check("L01 banks need>debit", sum(1 for n, d in zip(needs, debits) if n > d), 1)

# Example 2.6 (A pays B 100, B pays C 80, C pays A 50) and Remark 2.7 (payment 3 first)
ex = [(1, 0, 1, 10000), (2, 1, 2, 8000), (3, 2, 0, 5000)]
check("Ex2.6 Need_A", rtgs_need(0, ex), 10000)
check("Ex2.6 Debit_A", max(0, -net(0, ex)), 5000)
check("Ex2.6 Need_B Need_C", (rtgs_need(1, ex), rtgs_need(2, ex)), (0, 0))
check("Ex2.6 gross", sum(a for *_, a in ex), 23000)
rem = [(1, 2, 0, 5000), (2, 0, 1, 10000), (3, 1, 2, 8000)]
check("Rem2.7 Need_A after reorder", rtgs_need(0, rem), 5000)
check("Rem2.7 Debit_A unchanged", max(0, -net(0, rem)), 5000)

# Remark 3.1 wording test: does the order of OTHER banks' payments leave S_{i,k} unchanged?
# Bank 0 (=i) receives 100 at position 2; a payment between banks 1 and 2 sits at position 1.
seq_a = [(1, 1, 2, 5000), (2, 2, 0, 10000)]
seq_b = [(1, 2, 0, 10000), (2, 1, 2, 5000)]
def running(bank: int, d: list) -> list:
    out = [0]
    s = 0
    for _, snd, rcv, a in d:
        if snd == bank:
            s -= a
        elif rcv == bank:
            s += a
        out.append(s)
    return out
print("Remark 3.1 probe: S_{A,k} with other-bank payment first:", running(0, seq_a))
print("Remark 3.1 probe: S_{A,k} with other-bank payment second:", running(0, seq_b))
# FINDING (not a script error): the Remark 3.1 sentence "the order of the other banks' payments does not change S_{i,k}" is false
# when the lists below differ; the check records the observed inequality.
check("FINDING Remark 3.1 claim: other-bank reorder leaves S_{A,k} unchanged (expected False)",
      running(0, seq_a) == running(0, seq_b), False)

# P2 check: Need = Debit iff min S >= 0 or S_m = min S (exhaustive small integer grid)
def iff_holds() -> bool:
    for mu in range(-3, 4):
        for sm in range(-3, 4):
            if mu > sm:
                continue
            need = max(0, -mu)
            debit = max(0, -sm)
            lhs = need == debit
            rhs = (mu >= 0) or (sm == mu)
            if lhs != rhs:
                return False
    return True
check("P2 equivalence on grid", iff_holds(), True)

# M1 - M3, P-R numbers
check("M1 need (300 in, 500 out, cents)", max(0, -min(0, 30000, -20000)), 20000)
check("M3 need", max(0, -min(0, 4000, -3000, -2000)), 3000)
check("M3 debit", max(0, -(-2000)), 2000)

# R3 example
r3 = [(1, 0, 1, 10000), (2, 1, 2, 10000), (3, 2, 0, 10000)]
check("R3 nets zero", [net(b, r3) for b in range(3)], [0, 0, 0])
check("R3 need A", rtgs_need(0, r3), 10000)

# ---------- L02: seed 2026, six trades among four members ----------
rng = random.Random(2026)
trades = []
for seq in range(1, 7):
    payer, receiver = rng.sample(range(4), 2)
    dollars = rng.randint(500, 20000)
    trades.append((seq, payer, receiver, 100 * dollars))
G = sum(a for *_, a in trades)
rec = [sum(a for _, p, r, a in trades if r == m) for m in range(4)]
pay = [sum(a for _, p, r, a in trades if p == m) for m in range(4)]
n = [rec[m] - pay[m] for m in range(4)]
A = sum(max(0, x) for x in n)
check("L02 gross", G, 7596300)
check("L02 receivables", rec, [314500, 2067800, 3340300, 1873700])
check("L02 payables", pay, [3941500, 314500, 0, 3340300])
check("L02 net", n, [-3627000, 1753300, 3340300, -1466600])
check("L02 sum net zero", sum(n), 0)
check("L02 netted", A, 5093600)
check("L02 netted = sum max(0,-n)", A == sum(max(0, -x) for x in n), True)
check("L02 reduction", G - A, 2502700)
check("L02 bps floor", (10000 * (G - A)) // G, 3294)
check("L02 both receive and pay", [m + 1 for m in range(4) if rec[m] > 0 and pay[m] > 0], [1, 2, 4])

# Example 2.4, M1, M2, R2 text
check("Ex2.4 bps", (10000 * 180) // 230, 7826)
check("M1 bps", (10000 * 130) // 180, 7222)
check("M2 bps", (10000 * 360) // 460, 7826)
check("L02 reduction share 4dp", round(Fraction(2502700, 7596300), 4), Fraction(3295, 10000))

# ---------- L03: seed 2026 waterfall inputs and scenario losses ----------
def layers(loss, im_d, df_d, cap, df_surv):
    a1 = min(loss, im_d)
    a2 = min(loss - a1, df_d)
    a3 = min(loss - a1 - a2, cap)
    Z = loss - a1 - a2 - a3
    D = sum(df_surv.values())
    if Z >= D:
        pay = dict(df_surv)
        u = Z - D
    else:
        pay = {i: (Z * v) // D for i, v in sorted(df_surv.items())}
        left = Z - sum(pay.values())
        for i in sorted(df_surv):
            if left == 0:
                break
            if df_surv[i] > 0:
                pay[i] += 1
                left -= 1
        assert left == 0
        u = 0
    assert a1 + a2 + a3 + sum(pay.values()) + u == loss
    return a1, a2, a3, pay, u

# fixture (Example 1.5)
fx = {1: 40, 2: 60}
check("Ex1.5 L=200 pays", layers(200, 100, 50, 30, fx)[3], {1: 8, 2: 12})
check("Ex1.5 L=300 uncovered", layers(300, 100, 50, 30, fx)[4], 20)
check("Ex1.5 L=181 leftover to 1", layers(181, 100, 50, 30, fx)[3], {1: 1, 2: 0})
check("Ex1.5 L=180 nobody pays", layers(180, 100, 50, 30, fx)[3], {1: 0, 2: 0})
# Ex 1.6
check("Ex1.6 Z=1", layers(1, 0, 0, 0, {1: 1, 2: 1, 3: 1})[3], {1: 1, 2: 0, 3: 0})
check("Ex1.6 Z=2", layers(2, 0, 0, 0, {1: 1, 2: 1, 3: 1})[3], {1: 1, 2: 1, 3: 0})

rng = random.Random(2026)
im = {i: rng.randint(1000, 5000) for i in (1, 2, 3, 4)}
df = {i: rng.randint(100, 900) for i in (1, 2, 3, 4)}
capital = rng.randint(500, 2000)
losses = [rng.randint(0, 3000) for _ in range(200)]
check("L03 IM", im, {1: 1487, 2: 2308, 3: 3058, 4: 4896})
check("L03 DF", df, {1: 624, 2: 762, 3: 205, 4: 328})
check("L03 capital", capital, 1730)
surv = {i: df[i] for i in (1, 2, 4)}
check("A3 within margin loss", im[3] // 2, 1529)
check("A3 DF loss", im[3] + df[3] // 2, 3160)
check("A3 surv loss", im[3] + df[3] + capital + sum(surv.values()) // 2, 5850)
a1, a2, a3, p, u = layers(5850, im[3], df[3], capital, surv)
check("A3 surv pays", p, {1: 312, 2: 381, 4: 164})
check("A3 residual 857 = D/2", (5850 - 3058 - 205 - 1730, sum(surv.values()) / 2), (857, 857.0))
a1, a2, a3, p, u = layers(3160, im[3], df[3], capital, surv)
check("A3 DF loss layers", (a1, a2, a3), (3058, 102, 0))


def sized(ls, t):
    S = len(ls)
    k = math.ceil(Fraction(t * S, 10000))
    return sorted(ls)[k - 1], k


def cover(ls, m):
    return (10000 * sum(1 for x in ls if x <= m)) // len(ls)


def brute(ls, t):
    for m in range(0, max(ls) + 1):
        if cover(ls, m) >= t:
            return m
    raise RuntimeError


m99, k99 = sized(losses, 9900)
m9975, k9975 = sized(losses, 9975)
check("B 9900 k", k99, 198)
check("B 9900 margin", m99, 2961)
check("B 9975 k", k9975, 200)
check("B 9975 margin", m9975, 2992)
check("B brute 9900", brute(losses, 9900), 2961)
check("B brute 9975", brute(losses, 9975), 2992)
check("B cover at 2961", cover(losses, 2961), 9900)
check("B cover one below 2961", cover(losses, 2960), 9850)
check("B cover at 2992", cover(losses, 2992), 10000)
check("B cover one below 2992", cover(losses, 2991), 9950)
check("B scenarios above 2961", sum(1 for x in losses if x > 2961), 2)
check("B largest is 2992", max(losses), 2992)
# Example 2.5 arithmetic
check("Ex2.5 9900*200/10000", Fraction(9900 * 200, 10000), 198)
check("Ex2.5 9975*200/10000", Fraction(9975 * 200, 10000), Fraction(399, 2))

# M2, M3, E3, R2, R3, quiz numbers
check("M2 cover(4000)", cover([1000, 2000, 3000, 5000], 4000), 7500)
check("M2 sized 7500", sized([1000, 2000, 3000, 5000], 7500), (3000, 3))
check("M2 cover 2999", cover([1000, 2000, 3000, 5000], 2999), 5000)
check("M3 8000", sized([10, 20, 30, 40, 50], 8000), (40, 4))
check("M3 8001", sized([10, 20, 30, 40, 50], 8001), (50, 5))
check("M3 10000", sized([10, 20, 30, 40, 50], 10000), (50, 5))
check("Quiz 9975 S=400 k", -((-9975 * 400) // 10000), 399)
check("R3 smallest S with k<S for 9975", min(S for S in range(1, 2000) if -((-9975 * S) // 10000) < S), 400)
check("R2 9900 S=100 k", -((-9900 * 100) // 10000), 99)
check("E3 9900 cover count c=198", [c for c in range(201) if (10000 * c) // 200 == 9900], [198])

print("PASS rows:", len(OK))
for line in OK:
    print("  OK  ", line)
print("FAIL rows:", len(BAD))
for line in BAD:
    print("  BAD ", line)
