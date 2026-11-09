"""Round-2 check of lab-probe survivor m2 (brute force drops the bequest) on the L07 instance.

Run: python3 -I ledgers/M7/scripts/M7-c-r2/bequest_check_r2.py
"""
from itertools import product

GRID = (0, 100, 200, 300, 400)
U = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}
H = 4


def seqs(t, w):
    for seq in product(GRID, repeat=H - t):
        wl = w
        tot = 0
        ok = True
        for c in seq:
            if c > wl:
                ok = False
                break
            tot += U[c]
            wl -= c
        if ok:
            yield tot, wl


rows = []
for t in range(H):
    for w in GRID:
        allv = list(seqs(t, w))
        with_b = max(tot + wl // 100 for tot, wl in allv)
        without = max(tot for tot, wl in allv)
        zero_arg = any(tot + wl // 100 == with_b and wl == 0 for tot, wl in allv)
        rows.append((t, w, with_b, without, zero_arg))
print("pairs (t, w) with t = 0..3:", len(rows))
print("max with bequest == max without bequest at every pair:", all(a == b for _, _, a, b, _ in rows))
print("pairs where some optimal plan (with bequest) leaves zero wealth:", sum(1 for r in rows if r[4]), "of", len(rows))
