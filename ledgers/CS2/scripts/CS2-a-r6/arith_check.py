"""Recompute the numeric claims in L01-L04 prose from the printed lab rows (values copied from the expected blocks).

Usage: python -I arith_check.py   (no network, standard library only)
"""

import math

print("L03 rows (N, heap_cmp, heap_mov, list_cmp, list_mov)")
rows = [
    (16, 241, 361, 107, 98),
    (32, 648, 929, 279, 284),
    (64, 1625, 2209, 683, 1002),
    (128, 3802, 4933, 1617, 4514),
    (256, 8517, 10623, 3742, 17663),
    (512, 17831, 21095, 8500, 65561),
    (1024, 37178, 42401, 19052, 269578),
    (2048, 78710, 87863, 42192, 1086043),
    (4096, 166912, 181761, 92609, 4378444),
]
hc = [r[1] / p[1] for p, r in zip(rows, rows[1:])]
hm = [r[2] / p[2] for p, r in zip(rows, rows[1:])]
lm = [r[4] / p[4] for p, r in zip(rows, rows[1:])]
print("heap cmp ratios", [f"{x:.4f}" for x in hc])
print("heap move ratios", [f"{x:.4f}" for x in hm])
print("list move ratios", [f"{x:.4f}" for x in lm])
print("heap cmp ratio range over rows 64..4096 (ratios from index 2):", f"{min(hc[2:]):.4f}", f"{max(hc[2:]):.4f}")
print("heap cmp ratio range rows 512..4096:", f"{min(hc[5:]):.4f}", f"{max(hc[5:]):.4f}")
print("heap move ratio range 64..4096:", f"{min(hm[2:]):.4f}", f"{max(hm[2:]):.4f}")
print("list move ratio range 64..4096:", f"{min(lm[2:]):.4f}", f"{max(lm[2:]):.4f}")
N = 4096
print("bound 6N floor log2 N", 6 * N * int(math.log2(N)), "margin", 6 * N * 12 - 166912)
print("2N(N+1)", 2 * N * (N + 1), "list moves fraction", f"{4378444 / (2 * N * (N + 1)):.5f}")
print("sorted cmp per insertion at 4096", f"{92609 / 8192:.3f}")
print("N=16 sorted total", 107 + 98, "heap total", 241 + 361)
print("N=128 sorted total", 1617 + 4514, "heap total", 3802 + 4933)
print("N=256 heap total", 8517 + 10623, "sorted total", 3742 + 17663)

print("L04 numbers")
print("262431/8886 =", f"{262431 / 8886:.7f}", " 5120/8770 =", f"{5120 / 8770:.6f}")
print("4737/8886 =", f"{4737 / 8886:.7f}")
print("ceil log2 1024! via bit_length:", (math.factorial(1024) - 1).bit_length())
print("log2(1000!) =", f"{math.lgamma(1001) / math.log(2):.4f}", " 500*log2(500) =", f"{500 * math.log2(500):.4f}")
print("(n-1).bit_length check n=7 ceil log2 5040:", (5040 - 1).bit_length())

print("L01 numbers")
print("1023/511 =", f"{1023 / 511:.7f}", " 2+1/511 =", f"{2 + 1 / 511:.7f}")
print("1048576 == 1024**2:", 1024 ** 2 == 1048576)
print("first n with n*n > 1000*n:", next(n for n in range(1, 10**6) if n * n > 1000 * n))
print("count of n in 1..1000 with 1000n > n^2:", sum(1000 * n > n * n for n in range(1, 1001)))
print("L01 R1 n in 1..999 check:", all(1000 * n > n * n for n in range(1, 1000)), 1000 * 1000 == 1000 * 1000)
