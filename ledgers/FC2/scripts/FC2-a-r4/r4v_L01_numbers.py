"""Independent recomputation of the L01 lab counts (integer arithmetic, prices scaled by 10 and 2)."""
from itertools import product

def arb_count(cost_b, cost_s, box=range(-10, 11)):
    n = 0
    for x, y in product(box, box):
        cost = cost_b * x + cost_s * y
        pu = x + 3 * y
        pd = x + y
        if cost <= 0 and pu >= 0 and pd >= 0 and (cost < 0 or pu > 0 or pd > 0):
            n += 1
    return n

def dominance(cost_b, cost_s, small=range(-2, 3)):
    hs = list(product(small, small))
    dom = bad = 0
    for a in hs:
        pa = (a[0] + 3 * a[1], a[0] + a[1])
        for b in hs:
            pb = (b[0] + 3 * b[1], b[0] + b[1])
            if pa[0] >= pb[0] and pa[1] >= pb[1]:
                dom += 1
                if cost_b * a[0] + cost_s * a[1] < cost_b * b[0] + cost_s * b[1]:
                    bad += 1
    return dom, bad

# Part A: bond 9/10 -> 9 (x10), stock 1 -> 10 (x10); scale all by 10
print("A arbitrage in box:", arb_count(9, 10))
print("A dominance pairs, misordered:", dominance(9, 10))
# Part B: stock 1/2 -> 5 (x10)
print("B arbitrage in box:", arb_count(9, 5))
print("B dominance pairs, misordered:", dominance(9, 5))
# Zero-cost, strictly positive both states, in box
zc = [(x, y) for x, y in product(range(-10, 11), repeat=2) if 9 * x + 5 * y == 0 and x + 3 * y > 0 and x + y > 0]
print("B zero-cost strictly positive in box:", zc)
# Scaled arbitrage list check: multiples t*(-5,9) in box
print("B multiples of (-5,9) in box:", [(-5 * t, 9 * t) for t in range(-10, 11) if -10 <= -5 * t <= 10 and -10 <= 9 * t <= 10])
