"""Independent recomputation of the L09 numbers (verifier, round 3)."""
import itertools
from fractions import Fraction as F

def rank(bids):
    # independent ranking: sort by bid descending, index ascending
    return [i for _, i in sorted(((-b, i) for i, b in enumerate(bids)))]

def rev_u(bids, k):
    order = rank(bids)
    return k * bids[order[k]]

def rev_d(bids, k):
    order = rank(bids)
    return sum(bids[i] for i in order[:k])

grid = list(itertools.product(range(4), repeat=4))
above = eq = below = 0
eq_top3 = 0
for b in grid:
    b = list(b)
    du, dd = rev_u(b, 2), rev_d(b, 2)
    if dd > du: above += 1
    elif dd == du: eq += 1
    else: below += 1
    order = rank(b)
    top3equal = b[order[0]] == b[order[1]] == b[order[2]]
    if top3equal != (dd == du):
        print("MISMATCH equality condition", b)
    if top3equal: eq_top3 += 1
print("profiles", len(grid), "above", above, "equal", eq, "below", below, "top3-equal count", eq_top3)
print("share above:", F(above, 256), float(F(above,256)))

# k=1 identity
ok = 0
for b in grid:
    b = list(b); order = rank(b); w = order[0]
    if rev_u(b,1) == b[order[1]] and rev_d(b,1) == b[w]:
        ok += 1
print("k=1 identity holds on", ok, "of 256")

# Part A
bids = [8000, 9500, 6500, 7000]; vals = [9000, 5000, 6000, 7000]
order = rank(bids); print("ranking", order, "winners", sorted(order[:2]))
print("uniform rev", rev_u(bids, 2), "disc rev", rev_d(bids, 2), "gap", rev_d(bids,2)-rev_u(bids,2), "gap share", F(rev_d(bids,2)-rev_u(bids,2), rev_u(bids,2)))
won = sum(vals[i] for i in order[:2]); best = sum(sorted(vals, reverse=True)[:2])
print("won", won, "best", best, "eff", F(won, best), float(F(won,best)))
# M1/M2/M3
mb = [5000, 8000, 6000, 7000]; o = rank(mb)
print("M1 ranking", o, "clearing", mb[o[2]], "winners", sorted(o[:2]))
print("M2 uniform", rev_u(mb,2), "disc", rev_d(mb,2), "diff", rev_d(mb,2)-rev_u(mb,2))
print("M3 k=1 winner pays uniform", rev_u(mb,1)/1, "own", rev_d(mb,1))
# R1 formula check
def count_v(v):
    return sum(1 for b in grid if b.count(v) >= 3 and max(b) <= v and sorted(b)[-3:] == [v,v,v])
print("R1 counts per v:", [ (v, sum(1 for b in grid if sorted(b, reverse=True)[:3] == [v,v,v])) for v in range(4)], "claimed 4v+1:", [4*v+1 for v in range(4)])
# the fourth-bid x<=v: check the R1 claim count total 28
print("R1 sum:", sum(4*v+1 for v in range(4)))
