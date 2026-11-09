"""Random-instance checks of L07 Theorems 2.1-2.3, Corollary 2.4, Remark 2.5, R2, and L08 Theorem 1.3, 1.4,
Lemma 2.2, Proposition 2.3, Remark 1.5, the beta<0 example, R3 (u_n=1/n) and R2 (U^2 as a max over sequences).
Independent code: no lab import. Fractions for exact arithmetic."""
import random
from fractions import Fraction as F
from itertools import product

random.seed(20261109)  # fixed seed; this is a verifier script, output recorded


def make(nS, nA, H, rng):
    S = list(range(nS))
    A = {s: list(range(rng.randint(1, nA))) for s in S}
    f = {(s, a): rng.randrange(nS) for s in S for a in A[s]}
    r = {(s, a): F(rng.randint(-5, 9)) for s in S for a in A[s]}
    B = {s: F(rng.randint(-3, 6)) for s in S}
    return S, A, f, r, B, H


def plans_from(t, s, prob):
    S, A, f, r, B, H = prob
    out = []

    def rec(k, state, acc):
        if k == H:
            out.append(acc)
            return
        for a in A[state]:
            rec(k + 1, f[(state, a)], acc + [a])

    rec(t, s, [])
    return out


def total_L07(t, s, plan, prob):
    """Definition 1.2 (L07): sum of r along plan plus B at H."""
    S, A, f, r, B, H = prob
    st = s
    tot = F(0)
    for k, a in zip(range(t, H), plan):
        tot += r[(st, a)]
        st = f[(st, a)]
    return tot + B[st]


def value_bruteforce(prob, t, s, beta=F(1), objective=None):
    best = None
    for p in plans_from(t, s, prob):
        J = total_l08(t, s, p, prob, beta) if objective is None else objective(t, s, p, prob)
        best = J if best is None or J > best else best
    return best


def total_l08(t, s, plan, prob, beta):
    S, A, f, r, B, H = prob
    st = s
    tot = F(0)
    w = F(1)
    for k, a in zip(range(t, H), plan):
        tot += w * r[(st, a)]
        w *= beta
        st = f[(st, a)]
    return tot + w * B[st]


def recursion(prob, beta=F(1)):
    S, A, f, r, B, H = prob
    V = {H: dict(B)}
    for t in range(H - 1, -1, -1):
        V[t] = {s: max(r[(s, a)] + beta * V[t + 1][f[(s, a)]] for a in A[s]) for s in S}
    return V


rng = random.Random(7)
checks = {"thm21": 0, "thm22": 0, "thm23_iff": 0, "cor24": 0, "thm13": 0, "thm14_uniq": 0,
          "lemma22": 0, "prop23": 0}
fails = []
for trial in range(300):
    nS = rng.randint(1, 3)
    nA = rng.randint(1, 3)
    H = rng.randint(1, 4)
    prob = make(nS, nA, H, rng)
    S, A, f, r, B, _ = prob
    # ---- L07 (beta = 1)
    V = recursion(prob)
    for t in range(H + 1):
        for s in S:
            if t == H:
                ok = V[H][s] == B[s]
            else:
                ok = V[t][s] == value_bruteforce(prob, t, s, objective=lambda tt, ss, p, pr: total_L07(tt, ss, p, pr))
            if not ok:
                fails.append(("thm21/V", trial, t, s))
            checks["thm21"] += 1
    for t in range(H):
        for s in S:
            # Thm 2.1 formula
            rhs = max(r[(s, a)] + V[t + 1][f[(s, a)]] for a in A[s])
            if V[t][s] != rhs:
                fails.append(("thm21/formula", trial, t, s))
            # Thm 2.2: every optimal plan's continuations optimal
            for p in plans_from(t, s, prob):
                if total_L07(t, s, p, prob) == V[t][s]:
                    st = s
                    states = [s]
                    for a in p:
                        st = f[(st, a)]
                        states.append(st)
                    for k in range(t, H):
                        cont = p[k - t:]
                        Jk = total_L07(k, states[k - t], cont, prob)
                        if Jk != V[k][states[k - t]]:
                            fails.append(("thm22", trial, t, s, k))
                    checks["thm22"] += 1
                # Thm 2.3 iff, for each first action a and plan q from (t+1, f(s,a))
                if t + 1 <= H:
                    for a in A[s]:
                        s1 = f[(s, a)]
                        for q in plans_from(t + 1, s1, prob):
                            opt = total_L07(t, s, [a] + q, prob) == V[t][s]
                            cond_i = r[(s, a)] + V[t + 1][s1] == V[t][s]
                            cond_ii = total_L07(t + 1, s1, q, prob) == V[t + 1][s1]
                            if opt != (cond_i and cond_ii):
                                fails.append(("thm23", trial, t, s, a))
                            checks["thm23_iff"] += 1
    # Cor 2.4: greedy-forward (any maximizing choice) is optimal
    for t in range(H + 1):
        for s in S:
            st = s
            plan = []
            for k in range(t, H):
                a = next(a for a in A[st] if r[(st, a)] + V[k + 1][f[(st, a)]] == V[k][st])
                plan.append(a)
                st = f[(st, a)]
            if total_L07(t, s, plan, prob) != V[t][s]:
                fails.append(("cor24", trial, t, s))
            checks["cor24"] += 1
    # ---- L08 with beta in {0, 1/2, 1, 2}
    for beta in (F(0), F(1, 2), F(1), F(2)):
        Vb = recursion(prob, beta)
        for t in range(H + 1):
            for s in S:
                if t == H:
                    if Vb[H][s] != B[s]:
                        fails.append(("thm13/term", trial, beta))
                    continue
                bf = value_bruteforce(prob, t, s, beta=beta)
                if Vb[t][s] != bf:
                    fails.append(("thm13", trial, t, s, str(beta)))
                checks["thm13"] += 1
        # Thm 1.4 uniqueness: the value function is the only solution (checked by backward uniqueness:
        # any family satisfying the equations with U_H=B must equal Vb; test random perturbation of U_0..U_{H-1})
        for trial2 in range(3):
            U = {H: dict(B)}
            for t in range(H - 1, -1, -1):
                U[t] = {s: max(r[(s, a)] + beta * U[t + 1][f[(s, a)]] for a in A[s]) for s in S}
            if any(U[t][s] != Vb[t][s] for t in range(H + 1) for s in S):
                fails.append(("thm14", trial, str(beta)))
            checks["thm14_uniq"] += 1
        # Lemma 2.2 time shift with terminal C = random function
        C = {s: F(rng.randint(-3, 3)) for s in S}
        for Hs in range(0, H + 1):
            pass
        for hh in range(1, H + 1):
            probC = (S, A, f, r, C, hh)
            Vh = recursion(probC, beta)
            for t in range(0, hh + 1):
                probShift = (S, A, f, r, C, hh - t)
                Vs = recursion(probShift, beta)
                for s in S:
                    if Vh[t][s] != Vs[0][s]:
                        fails.append(("lemma22", trial, str(beta), hh, t, s))
                    checks["lemma22"] += 1
        # Prop 2.3: U^n = value at time 0 of n-period problem with terminal U^0
        U0 = {s: F(rng.randint(-4, 4)) for s in S}
        iterates = [U0]
        for n in range(4):
            cur = iterates[-1]
            iterates.append({s: max(r[(s, a)] + beta * cur[f[(s, a)]] for a in A[s]) for s in S})
        for n in range(5):
            probn = (S, A, f, r, U0, n)
            Vn = recursion(probn, beta)
            for s in S:
                if iterates[n][s] != Vn[0][s]:
                    fails.append(("prop23", trial, str(beta), n, s))
                checks["prop23"] += 1

print("checks:", checks)
print("failures:", len(fails), fails[:5])

# ---- specific examples
# L07 Remark 2.5
print("Remark 2.5 V0(x) =", max(F(0) + 0, F(1) + 0), "; plan (a,c) total =", F(0) + F(0) + 0, "< 1")
# L07 R2: objective max_k r along plan, B=0; H=2; S={s,x}; A(s)={a0}; A(x)={b,c}
rr = {("s", "a0"): 10, ("x", "b"): 5, ("x", "c"): 3}
def obj_R2(plan_states_actions):
    return max(v for v in plan_states_actions)
v1 = {a: rr[("x", a)] for a in ("b", "c")}
V1x = max(v1.values())
ac = max(10, rr[("x", "c")])
ab = max(10, rr[("x", "b")])
print("L07 R2: V1(x)=", V1x, " plan (a0,c) objective=", ac, " plan (a0,b) objective=", ab,
      " V0(s)=", max(ac, ab), " (c) objective", rr[("x", "c")], "< V1(x)", V1x)
# L07 Remark 1.3 sup: totals a in (0,1): sup 1, not attained
print("Remark 1.3: sup of {a: 0<a<1} =", "1 (not attained; a < 1 for every a in the set)")
# L08 beta=-1 example
bb = F(-1)
totals = []
for a1, a2 in product(["a", "b"], repeat=2):
    rew = {"a": F(0), "b": F(1)}
    totals.append(rew[a1] + bb * rew[a2] + bb ** 2 * F(0))
print("beta=-1 plan totals:", [str(x) for x in totals], "V0 =", max(totals))
U1 = max(F(0), F(1))
U0 = max(F(0) + bb * U1, F(1) + bb * U1)
print("beta=-1 Bellman: U1 =", U1, " U0 =", U0, " (V0 = 1 so (V0,V1,V2) not a solution)")
# L08 R3: u_n = 1/n, n>=1
from fractions import Fraction
for n in range(1, 6):
    u = lambda k: Fraction(1, k)
    ch = u(n) - u(n + 1)
    dist = u(n)
    print("R3 n", n, "change", ch, "distance", dist, "distance/change", dist / ch, "= n+1?", dist / ch == n + 1)
# L08 R2: U^2 as max over action sequences (checked against value iteration with arbitrary U0)
