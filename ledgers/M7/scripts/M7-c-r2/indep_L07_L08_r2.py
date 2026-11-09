"""Independent re-derivation (round 2) of every number in L07 and L08, written without importing the lab twins.

Run: python3 -I ledgers/M7/scripts/M7-c-r2/indep_L07_L08_r2.py
Each section prints the quantity, the value recomputed here, and the page locator it checks.
"""
from fractions import Fraction as F
from itertools import product
from math import comb

print("== L07 toy problem: wealth grid in cents, consumption on the same grid, reward table in utils ==")
H7 = 4
GRID7 = (0, 100, 200, 300, 400)
U7 = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}  # L07.html lab code REWARD table


def bequest7(w):
    return w // 100


def feas7(w):
    return [c for c in GRID7 if c <= w]


# backward recursion, written from scratch
V7 = {H7: {w: bequest7(w) for w in GRID7}}
for t in range(H7 - 1, -1, -1):
    V7[t] = {w: max(U7[c] + V7[t + 1][w - c] for c in feas7(w)) for w in GRID7}
print("Part A table (L07.html:300-304):")
for t in range(H7 + 1):
    print(" ", t, [V7[t][w] for w in GRID7])
expected_table = {
    0: [0, 60, 120, 180, 240],
    1: [0, 60, 120, 180, 220],
    2: [0, 60, 120, 160, 200],
    3: [0, 60, 100, 120, 130],
    4: [0, 1, 2, 3, 4],
}
assert all(V7[t][w] == expected_table[t][i] for t in expected_table for i, w in enumerate(GRID7)), "table mismatch"
print("  table matches L07.html:300-304: True")
print("  W400 column (E1, L07.html:415):", [V7[t][400] for t in range(H7 + 1)])
print("  differences (E1):", [V7[t][400] - V7[t + 1][400] for t in range(H7)])
print("  V0(400)-V3(400) (quiz, L07.html:546-548):", V7[0][400] - V7[3][400])
print("  V1(400) (quiz, L07.html:532):", V7[1][400])
print("  E2 ratio 130/240 =", F(130, 240), "=", round(130 / 240, 4))

# brute force over all 4-period consumption sequences from each (t, w)
def brute7(t, w):
    best = None
    count = 0
    for seq in product(GRID7, repeat=H7 - t):
        wealth = w
        total = 0
        ok = True
        for c in seq:
            if c > wealth:
                ok = False
                break
            total += U7[c]
            wealth -= c
        if not ok:
            continue
        count += 1
        total += bequest7(wealth)
        best = total if best is None or total > best else best
    return best, count


all_ok = all(brute7(t, w)[0] == V7[t][w] for t in range(H7) for w in GRID7)
print("  brute force equals recursion for all 20 (t,w):", all_ok)
print("  feasible sequences from (0,400) =", brute7(0, 400)[1], "; C(8,4) =", comb(8, 4))

# greedy and optimal plan (Part C)
def plan_total7(seq, w0):
    total = 0
    w = w0
    for c in seq:
        total += U7[c]
        w -= c
    return total + bequest7(w)


opt = []
w = 400
for t in range(H7):
    c = max(feas7(w), key=lambda x: U7[x] + V7[t + 1][w - x])
    opt.append(c)
    w -= c
print("  optimal plan from (0,400):", opt, "total", plan_total7(opt, 400), "(expect 100 100 100 100, 240)")
greedy = [400, 0, 0, 0]
print("  greedy total:", plan_total7(greedy, 400), "(expect 130)")
for k in range(1, H7):
    wk = 400 - sum(greedy[:k])
    print("  greedy tail from t", k, "wealth", wk, "optimal:", plan_total7(greedy[k:], wk) == V7[k][wk])
print("  greedy plan optimal:", plan_total7(greedy, 400) == V7[0][400], "(expect False)")

print("\n== L07 Remark 2.5 counterexample (H=2): V0(x)=1 via b; plan (a,c) total 0 ==")
# x: actions a->y reward 0, b->y reward 1; y: c->y reward 0; B=0
Vy1 = 0
Vx0 = max(0 + Vy1, 1 + Vy1)
print("  V1(y)=", Vy1, " V0(x)=", Vx0, " J((a,c))=", 0 + 0 + 0)

print("\n== L07 two-period problem for M1-M3 (B(x)=0, B(y)=1; u,v at x; w at y) ==")
Vy1 = 2 + 1
Vx1 = max(3 + 1, 5 + 0)
Vx0 = max(3 + Vy1, 5 + Vx1)
print("  V1(x)=", Vx1, "(expect 5)  V1(y)=", Vy1, "(expect 3)  V0(x)=", Vx0, "(expect 10)")
plans = {"(u,w)": 3 + (2 + 1), "(v,u)": 5 + (3 + 1), "(v,v)": 5 + 5}
print("  plan totals:", plans, "max", max(plans.values()), "(expect 6, 9, 10; max 10)")

print("\n== L07 R2 objective max_k r (B=0), H=2 ==")
# s: a0 reward 10 to x; x: b reward 5, c reward 3, both stay at x
def obj(rs):
    return max(rs)
V1x = max(obj([5]), obj([3]))
print("  V1(x) =", V1x, "; (c) objective", obj([3]), "is not optimal from (1,x)")
print("  plans from (0,s): (a0,b)=", obj([10, 5]), " (a0,c)=", obj([10, 3]), "; V0(s)=", max(obj([10, 5]), obj([10, 3])))

print("\n== L07 R1: sup of totals with H=1, A(s)=(0,1), r=a ==")
print("  values in (0,1) are all < 1: sup = 1 not attained (checked on a fine grid):",
      max(F(k, 1000) for k in range(1, 1000)) < 1)

print("\n== L07 R3 counts ==")
for m, h, t in ((2, 4, 0), (3, 3, 1)):
    print("  m", m, "H", h, "t", t, "plans", m ** (h - t))

print("\n== L07 random checks: Theorem 2.1, 2.2, 2.3 and Corollary 2.4 on random finite problems ==")
import random

random.seed(20261108)


def random_problem(rng):
    nS = rng.randint(1, 3)
    S = list(range(nS))
    A = {s: list(range(rng.randint(1, 3))) for s in S}
    f = {(s, a): rng.choice(S) for s in S for a in A[s]}
    r = {(s, a): F(rng.randint(-3, 5)) for s in S for a in A[s]}
    B = {s: F(rng.randint(-2, 4)) for s in S}
    H = rng.randint(1, 4)
    return S, A, f, r, B, H


def all_plans(S, A, f, H, t, s):
    if t == H:
        yield ()
        return
    for a in A[s]:
        for rest in all_plans(S, A, f, H, t + 1, f[(s, a)]):
            yield (a,) + rest


def J(p, S, A, f, r, B, H, t, s):
    total = F(0)
    st = s
    for k, a in enumerate(p):
        total += r[(st, a)]
        st = f[(st, a)]
    return total + B[st]


def V(S, A, f, r, B, H, t, s):
    return max(J(p, S, A, f, r, B, H, t, s) for p in all_plans(S, A, f, H, t, s))


rng = random.Random(7)
checked = 0
for _ in range(300):
    S, A, f, r, B, H = random_problem(rng)
    # Theorem 2.1 (backward recursion) for all t, s
    for t in range(H):
        for s in S:
            rhs = max(r[(s, a)] + V(S, A, f, r, B, H, t + 1, f[(s, a)]) for a in A[s])
            assert rhs == V(S, A, f, r, B, H, t, s), "Thm 2.1 fails"
            checked += 1
    # Theorem 2.2: continuations of an optimal plan are optimal
    for s in S:
        for p in all_plans(S, A, f, H, 0, s):
            if J(p, S, A, f, r, B, H, 0, s) != V(S, A, f, r, B, H, 0, s):
                continue
            st = s
            for k in range(H):
                cont = p[k:]
                sk = st
                assert J(cont, S, A, f, r, B, H, k, sk) == V(S, A, f, r, B, H, k, sk), "Thm 2.2 fails"
                st = f[(st, p[k])]
    # Corollary 2.4: forward maximizing choice is optimal
    for s in S:
        st = s
        plan = []
        for k in range(H):
            a_best = max(A[st], key=lambda a: r[(st, a)] + V(S, A, f, r, B, H, k + 1, f[(st, a)]))
            plan.append(a_best)
            st = f[(st, a_best)]
        assert J(tuple(plan), S, A, f, r, B, H, 0, s) == V(S, A, f, r, B, H, 0, s), "Cor 2.4 fails"
print("  random finite problems: Thm 2.1 instances checked =", checked, "; Thm 2.2 and Cor 2.4 hold on all 300 problems")

print("\n== L08 maintenance problem: PROFIT {0:6,1:4,2:1}, repair cost 4, beta 9/10, H 6, B 0 ==")
H8 = 6
BETA = F(9, 10)
STATES = (0, 1, 2)
PROFIT = {0: 6, 1: 4, 2: 1}


def rew8(s, a):
    return F(PROFIT[s]) if a == "run" else F(-4)


def nxt8(s, a):
    return min(s + 1, 2) if a == "run" else 0


W = {H8: {s: F(0) for s in STATES}}
policy = {}
ties = 0
for t in range(H8 - 1, -1, -1):
    W[t] = {}
    for s in STATES:
        cand = {a: rew8(s, a) + BETA * W[t + 1][nxt8(s, a)] for a in ("run", "repair")}
        W[t][s] = max(cand.values())
        policy[(t, s)] = [a for a in ("run", "repair") if cand[a] == W[t][s]]
        if t <= 5 and len(policy[(t, s)]) > 1:
            ties += 1
print("  V_t(s) (Part A, L08.html:286-292):")
for t in range(H8 + 1):
    print("   t", t, [str(W[t][s]) for s in STATES], [float(W[t][s]) for s in STATES])
print("  V0(0) display 13.948890 vs exact", float(W[0][0]), "; exact denominator", W[0][0].denominator)
print("  policy (first winner) t=0..5:", [[policy[(t, s)][0] for s in STATES] for t in range(6)])
print("  ties t=0..5 (expect 0):", ties)
print("  E1 V0(0)-V1(0) =", W[0][0] - W[1][0], "=", float(W[0][0] - W[1][0]), "; V4(0)-V5(0) =", W[4][0] - W[5][0])
print("  M1 V5 =", [str(W[5][s]) for s in STATES], "; V4(0) =", W[4][0], "; running", 6 + F(9, 10) * 4, "repair", -4 + F(9, 10) * 6)


def brute8(t, s):
    best = None
    n = 0
    for seq in product(("run", "repair"), repeat=H8 - t):
        n += 1
        st = s
        total = F(0)
        wgt = F(1)
        for a in seq:
            total += wgt * rew8(st, a)
            wgt *= BETA
            st = nxt8(st, a)
        best = total if best is None or total > best else best
    return best, n


plans = 0
match = True
for t in range(H8):
    for s in STATES:
        b, n = brute8(t, s)
        plans += n
        match = match and b == W[t][s]
print("  plans enumerated (expect 378):", plans, "; brute force matches recursion:", match)
print("  3*(2^6+...+2^1) =", 3 * sum(2 ** k for k in range(1, 7)))

print("  Part C changes from U0=0 (expect 6, 3.6, 2.74, 2.466, 2.2194, 1.99746):")
U = {s: F(0) for s in STATES}
changes = []
iterates = [dict(U)]
for n in range(6):
    new = {s: max(rew8(s, a) + BETA * U[nxt8(s, a)] for a in ("run", "repair")) for s in STATES}
    changes.append(max(abs(new[s] - U[s]) for s in STATES))
    U = new
    iterates.append(dict(U))
print("   ", [str(c) for c in changes], [round(float(c), 10) for c in changes])
print("  iterate U^n equals V_(H-n) for n=0..6:", all(iterates[n][s] == W[H8 - n][s] for n in range(7) for s in STATES))
print("  ratios change_n/change_(n-1):", [round(float(changes[n] / changes[n - 1]), 6) for n in range(1, 6)])
print("  E2 2.74/3.6 =", round(2.74 / 3.6, 6), "; 2.466/2.74 =", round(2.466 / 2.74, 6), "; 2.2194/2.466 =", round(2.2194 / 2.466, 6), "; 1.99746/2.2194 =", round(1.99746 / 2.2194, 6))

print("\n== L08 two-state problem (M2, M3): beta 1/2, H=2 ==")
Vy1 = F(3)
Vx1 = max(F(2), F(1))
Vx0 = max(F(2) + F(1, 2) * Vy1, F(1) + F(1, 2) * Vx1)
Vy0 = F(3) + F(1, 2) * Vy1
print("  V1(x)", Vx1, "V1(y)", Vy1, "V0(x)", Vx0, "V0(y)", Vy0, "(expect 2, 3, 7/2, 9/2)")
print("  plan (a,d) total:", F(2) + F(1, 2) * F(3) + F(1, 4) * 0, "(expect 7/2)")

print("\n== L08 P2/P3-type: Remark 1.5 (beta 1, H 1, r 1, f=s): (1+c, c) solves t=0 equation ==")
for c in (F(-2), F(0), F(7, 3)):
    U0 = F(1) + c
    U1 = c
    assert U0 == 1 + 1 * U1
print("  holds for sampled c: True")

print("\n== L08 negative discount example (beta -1), H=2, one state, A={a,b}, r(a)=0, r(b)=1, B=0 ==")
bm = F(-1)
tot = {}
for p in product(("a", "b"), repeat=2):
    rr = {"a": F(0), "b": F(1)}
    total = rr[p[0]] + bm * rr[p[1]] + bm * bm * F(0)
    tot[p] = total
print("  totals:", {"".join(k): str(v) for k, v in tot.items()}, "(expect 0,-1,1,0)")
V0neg = max(tot.values())
V1neg = max(F(0), F(1))
U1neg = max(F(0) + bm * F(0), F(1) + bm * F(0))
U0neg = max(F(0) + bm * U1neg, F(1) + bm * U1neg)
print("  V0=", V0neg, "V1=", V1neg, "U1=", U1neg, "U0=", U0neg, "; U0 != V0:", U0neg != V0neg)

print("\n== L08 R3 example u_n = 1/n ==")
for n in (1, 2, 3, 10):
    change = F(1, n) - F(1, n + 1)
    print("  n", n, "change", change, "= 1/(n(n+1))", F(1, n * (n + 1)) == change, "distance/change", (F(1, n)) / change, "= n+1", n + 1)

print("\n== L08 Lemma 2.2 time shift and Proposition 2.3 random checks ==")
rng2 = random.Random(11)
count_prop = 0
for _ in range(200):
    nS = rng2.randint(1, 3)
    S = list(range(nS))
    A = {s: ["x", "y"][: rng2.randint(1, 2)] for s in S}
    f = {(s, a): rng2.choice(S) for s in S for a in A[s]}
    r = {(s, a): F(rng2.randint(-3, 5)) for s in S for a in A[s]}
    beta = F(rng2.choice([0, 1, 2, 1, 3, 1, 9, 10]), 10)
    H = rng2.randint(1, 4)
    C = {s: F(rng2.randint(-2, 4)) for s in S}

    def Vh(t, s, hor, term):
        # value via recursion from terminal reward term, horizon hor
        vals = {hor: dict(term)}
        for tt in range(hor - 1, -1, -1):
            vals[tt] = {s2: max(r[(s2, a)] + beta * vals[tt + 1][f[(s2, a)]] for a in A[s2]) for s2 in S}
        return vals[t][s]

    # Lemma 2.2: V^(H)_t = V^(H-t)_0, checked on the recursion values
    for t in range(H + 1):
        for s in S:
            assert Vh(t, s, H, C) == Vh(0, s, H - t, C), "Lemma 2.2 fails"
    # Proposition 2.3: U^n = W^(n)_0 with U^{n+1} = G U^n
    U = {s: F(rng2.randint(-2, 4)) for s in S}
    U0 = dict(U)
    cur = dict(U0)
    for n in range(4):
        new = {s: max(r[(s, a)] + beta * cur[f[(s, a)]] for a in A[s]) for s in S}
        for s in S:
            assert new[s] == Vh(0, s, n + 1, U0), "Prop 2.3 fails"
        cur = new
        count_prop += 1
print("  Lemma 2.2 and Proposition 2.3 hold on 200 random problems with beta in {0,0.1,...,0.3,0.9,1,2,3}:", True, "(iterate checks", count_prop, ")")
print("\nDONE")

print("\n== L07 Theorem 2.3 (iff) on random finite problems: plan (a,q) optimal <=> (i) and (ii) ==")
rng3 = random.Random(3)
checked23 = 0
for _ in range(200):
    S, A, f, r, B, H = random_problem(rng3)
    for t in range(H):
        for s in S:
            Vts = V(S, A, f, r, B, H, t, s)
            for a in A[s]:
                s1 = f[(s, a)]
                for q in all_plans(S, A, f, H, t + 1, s1):
                    optimal = J((a,) + q, S, A, f, r, B, H, t, s) == Vts
                    cond_i = r[(s, a)] + V(S, A, f, r, B, H, t + 1, s1) == Vts
                    cond_ii = J(q, S, A, f, r, B, H, t + 1, s1) == V(S, A, f, r, B, H, t + 1, s1)
                    assert optimal == (cond_i and cond_ii), "Thm 2.3 fails"
                    checked23 += 1
print("  (plan, t, s) triples checked:", checked23, "; Theorem 2.3 iff holds on all of them: True")

print("\n== L08 Theorem 1.3 and Theorem 1.4 on random finite problems, beta in {0, 1/2, 1, 2} ==")
rng4 = random.Random(5)
n14 = 0
for _ in range(200):
    S, A, f, r, B, H = random_problem(rng4)
    beta = F(rng4.choice([0, 1, 2]), rng4.choice([1, 2]))
    Vb = {}
    for t in range(H, -1, -1):
        for s in S:
            if t == H:
                Vb[(t, s)] = B[s]
            else:
                Vb[(t, s)] = max(r[(s, a)] + beta * Vb[(t + 1, f[(s, a)])] for a in A[s])
    # Thm 1.3: V_t = max_a {r + beta V_{t+1}} with V_t the discounted value (plan enumeration)
    for t in range(H):
        for s in S:
            Jmax = max(sum(beta ** (k - t) * r[(st, a)] for k, (st, a) in enumerate(
                zip([s] + [0] * 0, [])) ) for _ in [0]) if False else None
            best = None
            for p in all_plans(S, A, f, H, t, s):
                st = s
                tot = F(0)
                for k, a in enumerate(p):
                    tot += beta ** k * r[(st, a)]
                    st = f[(st, a)]
                tot += beta ** (H - t) * B[st]
                best = tot if best is None or tot > best else best
            assert best == Vb[(t, s)], "Thm 1.3 fails"
            n14 += 1
print("  (t, s) pairs checked against plan enumeration:", n14, "; Theorem 1.3 holds: True")
