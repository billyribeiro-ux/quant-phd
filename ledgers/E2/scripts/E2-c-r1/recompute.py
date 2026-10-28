"""Independent recomputation of the numbers printed in E2 L07-L09 pages (verifier slice E2-c, round 1)."""
from fractions import Fraction as Fr
import itertools, math

def half_up(x):
    return math.floor(x + Fr(1, 2))

# ---- L08: E[M] exact, two ways
def EM_formula(n, a):
    return -a + sum(1 - Fr(x + a + 1, 2 * a + 1) ** n for x in range(-a, a))

def EM_enum(n, a):
    vals = range(-a, a + 1)
    tup = list(itertools.product(vals, repeat=n))
    return Fr(sum(max(t) for t in tup), len(tup))

print("L08 EM(2,1) formula", EM_formula(2, 1), "enum", EM_enum(2, 1))
print("L08 EM(3,1) formula", EM_formula(3, 1), "(page: 2/3)")
print("L08 EM(5,2000) exact", EM_formula(5, 2000), float(EM_formula(5, 2000)))
em = EM_formula(5, 2000)
print("L08 20000*EM exact", float(20000 * em), "as Fraction", 20000 * em)
print("L08 half_up(-20000*EM) =", half_up(-20000 * em), "(lab prints -26673331)")
print("L08 unrounded -20000*EM =", float(-20000 * em))
print("L08 continuous a(n-1)/(n+1) n=5 a=2000 =", Fr(2000 * 4, 6), float(Fr(2000 * 4, 6)))
print("L08 displayed diff discrete 1333.67 - continuous 1333.33 =", round(1333.67 - 1333.33, 2))
print("L08 unrounded diff =", float(em - Fr(4000, 3)))
print("L08 shade half_up(EM) =", half_up(em))
print("L08 1334*20000 - (-26620718) =", 1334 * 20000 + (-26620718))
print("L08 exact shaded total 20000*(1334-EM) =", float(20000 * (1334 - em)), half_up(20000 * (1334 - em)))
print("L08 1333 - EM =", float(1333 - em))
print("L08 diff naive sim vs exact", -26620718 - half_up(-20000 * em), (-26620718 - half_up(-20000*em))/79810)
print("L08 diff unrounded", float(-26620718 - (-20000 * em)), float((-26620718 - (-20000*em))/79810))
print("L08 SE per auction 79810/20000 =", 79810/20000)
print("L08 simulated mean per auction", -26620718/20000)
print("L08 E1 check EM*20000 vs printed 26673331.25 ->", float(20000*em))

# ---- L08 Example 2.4 and M1/M2
print("L08 example n2a1 EM", EM_formula(2, 1), " M2 n3a1", EM_formula(3, 1), " R1 n2a1 cont", Fr(1*1, 3), "diff", EM_formula(2,1)-Fr(1,3))

# ---- L07 numbers: Part B grid and revenue formula
VL, VH = 6000, 10000
pL, pH = Fr(3, 10), Fr(7, 10)
steps = [Fr(k, 4) for k in range(5)]
pairs = [(a, b) for a in steps for b in steps if a <= b]
def check(m):
    ic = ir = True
    for th, v in (("L", VL), ("H", VH)):
        truthful = v * m[th][0] - m[th][1]
        if truthful < 0:
            ir = False
        for r in ("L", "H"):
            if v * m[r][0] - m[r][1] > truthful:
                ic = False
    rev = pL * m["L"][1] + pH * m["H"][1]
    return ic, ir, rev
passing = []
for ql, qh in pairs:
    tl = int(VL * ql); th = int(VH * qh - (VH - VL) * ql)
    ic, ir, rev = check({"L": (ql, tl), "H": (qh, th)})
    if ic and ir:
        passing.append((ql, qh, rev))
print("L07 pairs with ql<=qh", len(pairs), "passing", len(passing))
print("L07 best", max(passing, key=lambda t: t[2]))
# Prop 3.2 closed form check over a fine grid of q_L,q_H with exact fractions (q in k/40)
best = None
for i in range(41):
    for j in range(41):
        ql, qh = Fr(i, 40), Fr(j, 40)
        if ql > qh:
            continue
        tl = VL * ql
        th = VH * qh - (VH - VL) * ql
        ic, ir, rev = check({"L": (ql, tl), "H": (qh, th)})
        if ic and ir and (best is None or rev > best[2]):
            best = (ql, qh, rev)
print("L07 fine-grid optimum (40 steps) with payments from binding constraints:", best, "vs Prop3.2 p_H*v_H =", pH*VH)
# Fine-grid check on a c>0 case p_H=1/2
pL2 = pH2 = Fr(1, 2)
best2 = None
for i in range(41):
    for j in range(41):
        ql, qh = Fr(i, 40), Fr(j, 40)
        if ql > qh: continue
        tl = VL*ql; th = VH*qh-(VH-VL)*ql
        rev = pL2*tl + pH2*th
        ic, ir, _ = check({"L": (ql, tl), "H": (qh, th)})
        if ic and ir and (best2 is None or rev > best2[2]):
            best2 = (ql, qh, rev)
print("L07 p_H=1/2 fine-grid optimum", best2, "(Prop 3.2 says v_L=6000)")
# threshold
print("L07 R3 p_H threshold", Fr(6000, 10000))
# Remark 2.3 cents
print("L07 part C tie-break revenue 0.7*6000 =", Fr(7,10)*6000)

# ---- L09: Part B counts and R1
from itertools import product
def rank(bids):
    return sorted(range(len(bids)), key=lambda i: (-bids[i], i))
def pay(fmt, bids, k):
    o = rank(bids); paid = [0]*len(bids); cl = bids[o[k]]
    for i in o[:k]:
        paid[i] = cl if fmt == "u" else bids[i]
    return paid
def rev(fmt, bids, k): return sum(pay(fmt, bids, k))
grid = list(product(range(4), repeat=4))
hi = eq = lo = 0
for p in grid:
    b = list(p)
    d, u = rev("d", b, 2), rev("u", b, 2)
    hi += d > u; eq += d == u; lo += d < u
print("L09 k=2 counts above/equal/below", hi, eq, lo, "of", len(grid))
sec_ok = sum(pay("u", list(p), 1)[rank(list(p))[0]] == sorted(p, reverse=True)[1] for p in grid)
own_ok = sum(pay("d", list(p), 1)[rank(list(p))[0]] == sorted(p, reverse=True)[0] for p in grid)
print("L09 k=1 second-price ok", sec_ok, "own bid ok", own_ok)
print("L09 share 228/256", 228/256)
# Part A numbers
b = [8000, 9500, 6500, 7000]; v = [9000, 5000, 6000, 7000]
print("L09 A ranking", rank(b), "uniform rev", rev("u", b, 2), "disc rev", rev("d", b, 2), "gap", rev("d", b, 2)-rev("u", b, 2), "gap share", (rev("d", b, 2)-rev("u", b, 2))/rev("u", b, 2))
print("L09 A efficiency", Fr(9000+5000, 9000+7000))
# R1 formula check: count equal-revenue profiles equals 4v+1 sum
print("L09 R1 sum 4v+1 for v=0..3:", sum(4*v_+1 for v_ in range(4)))
# Prop 3.2 zero-value counterexample: all values 0, truthful bids, k=2
print("L09 all-zero values: top-k sum =", sum(sorted([0,0,0,0], reverse=True)[:2]), "=> efficiency denominator 0")
