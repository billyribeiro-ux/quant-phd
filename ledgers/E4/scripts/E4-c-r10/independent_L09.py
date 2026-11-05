"""Round 10, slice E4-c: independent recount of the L09 bet enumeration (integer arithmetic, own code, no twin imports)."""
import itertools

P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]
W = [1, 2, 3, 4, 5, 6]


def cell(part, w):
    return next(c for c in part if w in c)


def meet(w):
    seen, stack = {w}, [w]
    while stack:
        x = stack.pop()
        for part in (P1, P2):
            for y in cell(part, x):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
    return seen


def sum_over(part, w, vals):
    c = cell(part, w)
    return sum(vals[k] for k in c), len(c)  # 6 * (sum of x over cell) / (6*|cell|) -> sign and value use sums


def counts(state):
    M = meet(state)
    strict = nonneg_meet = both_zero = 0
    first = None
    for vals in itertools.product([-2, -1, 0, 1, 2], repeat=6):
        x = dict(zip(W, vals))
        neg = {k: -v for k, v in x.items()}
        # posterior sign tests use exact integer sums; a positive/negative sum over a cell has the sign of the posterior
        g1 = {w: sum(x[k] for k in cell(P1, w)) for w in W}
        g2 = {w: sum(neg[k] for k in cell(P2, w)) for w in W}
        if g1[state] > 0 and g2[state] > 0:
            strict += 1
            if first is None:
                first = vals
        if all(g1[w] >= 0 and g2[w] >= 0 for w in M):
            nonneg_meet += 1
            if all(g1[w] == 0 and g2[w] == 0 for w in M):
                both_zero += 1
        # theorem check: strict at state and nonneg on the meet cannot coexist
        if g1[state] > 0 and g2[state] > 0 and all(g1[w] >= 0 and g2[w] >= 0 for w in M):
            raise SystemExit("theorem violated")
    return sorted(M), strict, nonneg_meet, both_zero, first


for s in (1, 4):
    m, strict, nn, bz, first = counts(s)
    print(f"state {s}: meet {m} strict-both {strict} nonneg-on-meet {nn} all-zero-on-meet {bz} first {first}")
