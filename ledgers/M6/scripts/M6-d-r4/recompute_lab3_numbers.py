from fractions import Fraction as F
import itertools, math
# independent recomputation of Lab 3 numbers and Lab 1/2 values
def paths(n):
    return itertools.product((1, -1), repeat=n)
def prob(steps, p):
    w = F(1)
    for s in steps:
        w *= p if s == 1 else 1 - p
    return w
# Lab 3: stopped walk tau=min(first k>=1 with S_k=1, 4), N=6
def stopped(p, N=6, lvl=1, cap=4):
    tot = F(0)
    for st in paths(N):
        pos = 0; val = None
        for k, s in enumerate(st[:cap], 1):
            pos += s
            if pos == lvl:
                val = pos; break
        if val is None:
            val = sum(st[:cap])
        tot += prob(st, p) * val
    return tot
print("fair stopped", stopped(F(1, 2)))
print("control stopped", stopped(F(1, 3)))
# Doob, N=6, lam=3 on |S|, max over k=1..6 (k=0 gives 0 < 3)
hits = F(0); eabs = F(0)
for st in paths(6):
    pos = 0; mx = 0
    for s in st:
        pos += s; mx = max(mx, abs(pos))
    if mx >= 3: hits += F(1, 64)
    eabs += F(1, 64) * abs(pos)
print("doob prob", hits, "bound", eabs / 3, "E|S6|", eabs)
# doubling: capital 100 base 1, every bet placed until stake > wealth
def doubling(p, K=100, s=1):
    # dynamic programming over (wealth, bet index)
    def rec(w, k):
        st = s * 2 ** (k - 1)
        if st > w:
            return (F(1) - p) ** 0 * 0, [(F(1), w)]  # ruin branch
        # win branch: leaves w + st
        outs = [(p, w + st)]
        # lose branch
        _, sub = rec(w - st, k + 1)
        for q, ww in sub:
            outs.append(((1 - p) * q, ww))
        return None, outs
    _, outs = rec(K, 1)
    # outs is list of (weight, final wealth); the lose branch weights are multiplied by (1-p) at each level already
    return outs
for p in (F(1, 2), F(1, 3)):
    outs = doubling(p)
    # fix: ruin leaf weight should be the product (1-p)^J accumulated; in rec the leaf returns weight 1 times parent's (1-p) factors
    tot = sum(w for w, _ in outs)
    ev = sum(w * ww for w, ww in outs)
    print("p", p, "total weight", tot, "E", ev, "half-up cents", math.floor(ev + F(1, 2)))
