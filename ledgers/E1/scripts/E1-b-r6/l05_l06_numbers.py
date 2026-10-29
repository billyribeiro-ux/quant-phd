"""Recompute the L05 and L06 prose numbers with exact Fractions, and check twin imports (RNG, network, file reads)."""
from fractions import Fraction as F
import re
from pathlib import Path

root = Path(__file__).resolve().parents[4]
# L05 monopoly closed forms for the three lab cases
for a, b, c in [(120, 1, 20), (90, 3, 10), (200, 4, 5), (100, 2, 10), (60, 3, 4), (50, 1, 0)]:
    pm = F(a + b * c, 2 * b); q = a - b * pm; pi = (pm - c) * q
    lerner = (pm - c) / pm; eps = -F(b) * pm / (a - b * pm)
    print("L05", (a, b, c), "p_m", pm, "Q_m", q, "pi_m", pi, "pi_closed", F((a - b * c) ** 2, 4 * b),
          "lerner", lerner, "1/|eps|", 1 / abs(eps), "(a-bc)/(a+bc)", F(a - b * c, a + b * c),
          "p_m-a/2b", pm - F(a, 2 * b), "c/2", F(c, 2))
print("L05 |eps(70)| for (120,1,20):", -F(70) / (120 - 70), " 1/|eps| at 70:", F(50, 70))
print("L05 |eps(27.5)| (200,4,5):", -F(4) * F(55, 2) / (200 - 4 * F(55, 2)), " 11/9 =", F(11, 9))
print("L05 Lerner Lab values 5/7, 1/2, 9/11:", F(100, 140), F(60, 120), F(180, 220))
# L05 M1-M3 and R1
print("M1", F(100 + 20, 4), 100 - 2 * 30, (30 - 10) * 40, F(80 ** 2, 8))
print("M2", F(60 + 12, 6), F(60 - 36), F(12 - 4, 12), -F(3) * 12 / 24, F(48, 72))
print("M3 (50,1,0)", F(50, 2), F(50 - 25), -F(25) / 25)
# L06 Cournot/Bertrand/Prop 4.1 at (120,1,20) and general d
for a, b, c in [(120, 1, 20), (90, 3, 10), (200, 4, 5)]:
    d = F(a - b * c)
    qm = d / 2; fm = F(a + b * c, 2 * b); pim = d * d / (4 * b)
    qc = d / 3; Qc = 2 * d / 3; fc = F(a + 2 * b * c, 3 * b); pic = 2 * d * d / (9 * b)
    print("L06", (a, b, c), "d", d, "Qm", qm, "fm", fm, "pim", pim, "Qc", Qc, "fc", fc, "picourn", pic,
          "Qc-Qm", Qc - qm, "d/6", d / 6, "Qb-Qc", d - Qc, "d/3", d / 3, "fm-fc", fm - fc, "d/(6b)", d / (6 * b),
          "fc-c", fc - c, "d/(3b)", d / (3 * b), "pim-pic", pim - pic, "d^2/(36b)", d * d / (36 * b))
print("Example 2.7 each earns", F(100 * 100, 9), "fee", F(160, 3), "volume total", F(200, 3))
print("M2 L06 (90,3,10): q", F(60, 3), "fee", F(90 + 60, 9), "each earns", 20 * F(50, 3) - 200 * 0 if False else F(20) * (F(50, 3) - 10))
print("E3 L06 at 45:", F(120 - 45, 2) * (45 - 20) , "undercut", (120 - 45) * (45 - 20))
# iteration first step within 1e-6 of d/3 for d=100 and d=180
for d in (F(100), F(180)):
    x = F(0); t_first = None
    for t in range(31):
        if t_first is None and abs(x - d / 3) < F(1, 10**6):
            t_first = t
        x = (d - x) / 2 if d - x > 0 else F(0)
    print("iteration d", d, "first t within 1e-6:", t_first)
x = F(0); d = F(100)
for _ in range(30):
    x = max(F(0), (d - x) / 2)
print("reference gap after 30 steps", x - d / 3, " -25/805306368 =", F(-25, 805306368))
print("x_2 =", (F(100, 3)) * (1 - F(1, 4)))
print("L06 fee grid count:", 1201, "zero-profit fees from 20 to 120:", (120 - 20) * 10 + 1)
print("Undercut check (120,1,20) rival 25:", F(95001, 1000) * F(4999, 1000), " sharing:", F(95, 2) * 5)
# twin imports and RNG / file / network use
for f in sorted((root / "tests/labs/E1").glob("lab-E1-L0[456]-1.py")):
    src = f.read_text(encoding="utf-8")
    imports = sorted(set(re.findall(r"^(?:from|import) (\S+)", src, re.M)))
    bad = [w for w in ("random", "open(", "urllib", "socket", "requests", "pathlib", "os.") if w in src]
    print(f.name, "imports", imports, "forbidden-hits", bad)
