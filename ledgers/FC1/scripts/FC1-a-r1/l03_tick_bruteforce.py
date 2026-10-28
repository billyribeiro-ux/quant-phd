# Independent brute force of the tick game of L03 section 3 (B1-B4), written from the page statement.
def profit(ai, aj, c, Q):
    if ai < aj: return (ai - c) * Q
    if ai == aj: return (ai - c) * Q / 2
    return 0
def equilibria(c, Q, lo, hi):
    asks = range(lo, hi + 1)
    out = []
    for a1 in asks:
        for a2 in asks:
            ok = all(profit(d, a2, c, Q) <= profit(a1, a2, c, Q) for d in asks) and \
                 all(profit(d, a1, c, Q) <= profit(a2, a1, c, Q) for d in asks)
            if ok: out.append((a1, a2))
    return out
for Q in (0, 2, 1000):
    eqs = equilibria(100, Q, 100, 130)
    print("Q=%d equilibria in grid 100..130: %d; symmetric: %s; asymmetric count: %d" % (
        Q, len(eqs), [p for p in eqs if p[0] == p[1]], len([p for p in eqs if p[0] != p[1]])))
print("Q=0 witnesses (100,105) and (103,103) are equilibria:", (100, 105) in equilibria(100, 0, 100, 130), (103, 103) in equilibria(100, 0, 100, 130))
