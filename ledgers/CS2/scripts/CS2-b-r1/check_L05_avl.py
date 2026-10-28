"""Verifier round 1 (CS2-b): independent functional AVL insertion (tuples, no shared code with the lab twin)
to recompute the L05 Lab 1 Part A and Part B counts. Run with python -I from the checkout.
"""
import random

SEED = 20261028


def h(t):
    return 0 if t is None else t[1]


def mk(l, k, r):
    return (l, 1 + max(h(l), h(r)), k, r)


def bf(t):
    return h(t[0]) - h(t[3])


def ins(t, k, cnt):
    if t is None:
        return (None, 1, k, None)
    if k < t[2]:
        l = ins(t[0], k, cnt)
        t = mk(l, t[2], t[3])
    elif k > t[2]:
        r = ins(t[3], k, cnt)
        t = mk(t[0], t[2], r)
    else:
        raise ValueError
    b = bf(t)
    if b > 1:
        if bf(t[0]) < 0:
            cnt["LR"] += 1
            L = t[0]
            # left-right: rotate left at L then right at t
            lr = L[3]
            newL = mk(L[0], L[2], lr[0])
            newT = mk(newL, lr[2], mk(lr[3], t[2], t[3]))
            return newT
        cnt["LL"] += 1
        L = t[0]
        return mk(L[0], L[2], mk(L[3], t[2], t[3]))
    if b < -1:
        if bf(t[3]) > 0:
            cnt["RL"] += 1
            R = t[3]
            rl = R[0]
            newR = mk(rl[3], R[2], R[3])
            newT = mk(mk(t[0], t[2], rl[0]), rl[2], newR)
            return newT
        cnt["RR"] += 1
        R = t[3]
        return mk(mk(t[0], t[2], R[0]), R[2], R[3])
    return t


def inorder(t, out):
    if t is not None:
        inorder(t[0], out)
        out.append(t[2])
        inorder(t[3], out)
    return out


def ok(t):
    if t is None:
        return True
    return abs(bf(t)) <= 1 and t[1] == 1 + max(h(t[0]), h(t[3])) and ok(t[0]) and ok(t[3])


rng = random.Random(SEED)
keys = rng.sample(range(1, 1_000_000), 500)
root = None
cnt = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}
zero = 0
for k in keys:
    before = sum(cnt.values())
    root = ins(root, k, cnt)
    zero += sum(cnt.values()) == before
print("final height", h(root), "zero-rotation inserts", zero, "invariant", ok(root), "sorted", inorder(root, []) == sorted(keys))
print("kinds LL RR LR RL", cnt["LL"], cnt["RR"], cnt["LR"], cnt["RL"], "rotation calls", cnt["LL"] + cnt["RR"] + 2 * (cnt["LR"] + cnt["RL"]))
r = None
for k in range(1, 65):
    r = ins(r, k, {"LL": 0, "RR": 0, "LR": 0, "RL": 0})
print("sorted 1..64 AVL height", h(r))
