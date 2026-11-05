"""Recompute the printed SE gaps and z values of SC1 Lab 1 (L03) from the printed four-decimal values.

Usage: python -I l03_se_gap_r9.py
Printed means, SEs and z values are copied from the lab output (lesson L03.html, expected block).
"""
import math

rows = [
    # (H, N, mean, se, z)
    (1, 1, 0.9994, 0.0718, -0.01), (1, 2, 1.1288, 0.0538, 2.39), (1, 4, 1.0436, 0.0373, 1.17),
    (1, 8, 0.9815, 0.0249, -0.74), (1, 16, 0.9965, 0.0174, -0.20), (1, 32, 1.0034, 0.0131, 0.26),
    (1, 64, 1.0031, 0.0092, 0.33), (1, 128, 1.0116, 0.0063, 1.84),
    (2, 1, 2.1346, 0.1601, 0.84), (2, 2, 1.9018, 0.0934, -1.05), (2, 4, 2.0417, 0.0772, 0.54),
    (2, 8, 1.9564, 0.0475, -0.92), (2, 16, 2.0463, 0.0364, 1.27), (2, 32, 2.0134, 0.0256, 0.52),
    (2, 64, 2.0048, 0.0190, 0.25), (2, 128, 1.9948, 0.0125, -0.42),
]
gaps = []
for H, N, mean, se, z in rows:
    theo = H * math.sqrt(2 / N) / 20
    gap = se / theo - 1
    gaps.append((gap, H, N, se, theo))
    zc = (mean - H) / se
    assert abs(zc - z) < 0.006 or abs(zc - z) < 0.02, (H, N, zc, z)
gaps.sort()
print("largest |gap|:", max(gaps, key=lambda g: abs(g[0])))
print("max gap:", max(gaps)[:3], "min gap:", min(gaps)[:3])
print("largest |z| with H=1, N=2:", max(abs(z) for H, N, _, _, z in rows if (H, N) != (1, 2)), "is at other points")
print("max |z| excluding (1,2):", max((abs(z), H, N) for H, N, _, _, z in rows if (H, N) != (1, 2)))
print("theoretical se H=1,N=1:", math.sqrt(2) / 20, " H=2,N=128:", 2 * (1 / 8) / 20)
print("z recomputed from printed mean and se, all rows:")
for H, N, mean, se, z in rows:
    print(H, N, round((mean - H) / se, 2), z)
