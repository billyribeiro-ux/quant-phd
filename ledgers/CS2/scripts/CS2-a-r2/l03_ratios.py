"""Recompute the doubling ratios that Lab 3 prints, from the printed integer counts (verifier round 2).

Usage: python3 -I l03_ratios.py
"""

rows = {  # N: (heap comparisons, heap moves, sorted-list comparisons, sorted-list moves), as printed
    16: (241, 361, 107, 98),
    32: (648, 929, 279, 284),
    64: (1625, 2209, 683, 1002),
    128: (3802, 4933, 1617, 4514),
    256: (8517, 10623, 3742, 17663),
    512: (17831, 21095, 8500, 65561),
    1024: (37178, 42401, 19052, 269578),
    2048: (78710, 87863, 42192, 1086043),
    4096: (166912, 181761, 92609, 4378444),
}
sizes = sorted(rows)
r_hc, r_hm, r_sm = {}, {}, {}
for prev, cur in zip(sizes, sizes[1:]):
    r_hc[cur] = rows[cur][0] / rows[prev][0]
    r_hm[cur] = rows[cur][1] / rows[prev][1]
    r_sm[cur] = rows[cur][3] / rows[prev][3]
for n in sizes[1:]:
    print(f"N={n}: heap comparison ratio {r_hc[n]:.4f}, heap move ratio {r_hm[n]:.4f}, sorted move ratio {r_sm[n]:.4f}")
rng_sm = [round(r_sm[n], 4) for n in sizes[2:]]  # N = 64 .. 4096 (rows the page cites)
rng_hm = [round(r_hm[n], 4) for n in sizes[2:]]
rng_hc = [round(r_hc[n], 4) for n in sizes[2:]]
rng_hc512 = [round(r_hc[n], 4) for n in sizes[4:]]  # N = 512 .. 4096
print("sorted move ratios N=64..4096: min", min(rng_sm), "max", max(rng_sm))
print("heap move ratios N=64..4096: min", min(rng_hm), "max", max(rng_hm))
print("heap comparison ratios N=64..4096: min", min(rng_hc), "max", max(rng_hc))
print("heap comparison ratios N=512..4096: min", min(rng_hc512), "max", max(rng_hc512))
print("sorted moves cmp 4378444/33562624", round(4378444 / 33562624, 4))
print("sorted comparisons per insertion at 4096", round(92609 / 8192, 1))
print("N=128 list total", 1617 + 4514, "heap total", 3802 + 4933)
print("N=256 heap total", 8517 + 10623, "list total", 3742 + 17663)
print("N=256 heap moves < list moves:", 10623 < 17663, "; N=128 list moves < heap moves:", 4514 < 4933)
