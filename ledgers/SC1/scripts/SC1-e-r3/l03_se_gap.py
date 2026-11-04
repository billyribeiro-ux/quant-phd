"""Recompute the population standard error gap printed by SC1 L03 Lab 1 (read-only, stdlib only).

Usage: l03_se_gap.py  (prints printed se, population se H*sqrt(2/N)/20, relative gap, and z values from the printed run)
"""
import math

printed = {
    (1, 1): (0.9994, 0.0718), (1, 2): (1.1288, 0.0538), (1, 4): (1.0436, 0.0373), (1, 8): (0.9815, 0.0249),
    (1, 16): (0.9965, 0.0174), (1, 32): (1.0034, 0.0131), (1, 64): (1.0031, 0.0092), (1, 128): (1.0116, 0.0063),
    (2, 1): (2.1346, 0.1601), (2, 2): (1.9018, 0.0934), (2, 4): (2.0417, 0.0772), (2, 8): (1.9564, 0.0475),
    (2, 16): (2.0463, 0.0364), (2, 32): (2.0134, 0.0256), (2, 64): (2.0048, 0.0190), (2, 128): (1.9948, 0.0125),
}
gaps = []
for (h, n), (mean, se) in sorted(printed.items()):
    pop = h * math.sqrt(2 / n) / 20
    gap = se / pop - 1
    z = (mean - h) / se
    gaps.append((abs(gap), h, n, gap))
    print(f"H={h} N={n:3d} printed se={se:.4f} population se={pop:.6f} gap={gap*100:+.2f}% z={z:+.2f}")
print("largest |gap|:", f"{max(g[0] for g in gaps)*100:.2f}%", "at", [(g[1], g[2]) for g in gaps if g[0] == max(x[0] for x in gaps)])
print("largest signed gap:", f"{max(g[3] for g in gaps)*100:+.2f}%", "at", [(g[1], g[2]) for g in gaps if g[3] == max(x[3] for x in gaps)])
