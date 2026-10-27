"""AC2 L05-L06 round-4 verifier: independent recomputation of the printed and derived figures on the L05 and L06 pages.

Run with: <checkout>/.venv/bin/python -I <this file>. Reads no files; prints one line per check.
"""

import math
from statistics import NormalDist

N = NormalDist()
phi = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)  # noqa: E731


def show(label: str, value: float, fmt: str = ".5f") -> None:
    print(f"{label} {format(value, fmt)}")


# L05 Proposition 2.3 and quiz/key results
q = N.inv_cdf(0.2)
gap = -2 * phi(q) / 0.2
show("L05 P2.3 q", q, ".6f")
show("L05 P2.3 gap (analytic)", gap, ".5f")
show("L05 P2.3 low-quintile mean", -phi(q) / 0.2, ".4f")

# L05 E2: sd of the two-leg spread and expected t
sd_unr = 0.08 * math.sqrt(2 / 100)
show("L05 E2 sd unrounded", sd_unr, ".6f")
show("L05 E2 se120 unrounded", sd_unr / math.sqrt(120), ".7f")
show("L05 E2 expected t, unrounded sd, planted 0.0022350", 0.0022350 / (sd_unr / math.sqrt(120)), ".4f")
show("L05 E2 expected t as WRITTEN (sd 0.01131, planted 0.0022350)", 0.0022350 / (0.01131 / math.sqrt(120)), ".4f")
for n, g in ((50, -2.7437), (100, -2.7728), (500, -2.7912), (5000, -2.7991)):
    show(f"L05 E2 distance from analytic, n={n}", gap - g, ".4f")

# L05 E3: seed-0 distance in SE units
se120 = sd_unr / math.sqrt(120)
show("L05 E3 unrounded distance (lab prints -1.433)", (0.00075 - 0.002235) / se120, ".4f")
show("L05 E3 ROUNDED inputs 0.00075 and 0.00223, unrounded SE", (0.00075 - 0.00223) / se120, ".4f")
show("L05 E3 rounded SE 0.00103", (0.00075 - 0.00223) / 0.00103, ".4f")
show("L05 E3 planted 0.002235 with SE 0.0010328", (0.00075 - 0.002235) / 0.0010328, ".4f")

# L05 R1: months for 80 percent power
zsum = 1.959964 + N.inv_cdf(0.8)
show("L05 R1 sqrt(T)", zsum * 0.01131 / 0.0022350, ".3f")
show("L05 R1 T", (zsum * 0.01131 / 0.0022350) ** 2, ".2f")

# L05 E1 binomial SE
se_rate = math.sqrt(0.05 * 0.95 / 200)
show("L05 E1 se of rate", se_rate, ".5f")
show("L05 E1 standard errors above 5 percent", (0.060 - 0.05) / se_rate, ".3f")

# L06 E3: a2 z-score, rounded and unrounded
show("L06 E3 unrounded z (0.103076 - 0.10)/0.001467", (0.103076 - 0.10) / 0.001467, ".4f")
show("L06 E3 two-sided tail at lab z 2.096", 2 * (1 - N.cdf(2.096)), ".4f")
show("L06 E3 rounded inputs 0.0031/0.0015", 0.0031 / 0.0015, ".4f")
show("L06 E3 two-sided tail at 2.067", 2 * (1 - N.cdf(2.067)), ".4f")

# L06 section 4 and R1 scale arithmetic
show("L06 s4 0.2824/0.05", 0.2824 / 0.05, ".4f")
show("L06 contamination in SE units 0.2084/0.2824", 0.2084 / 0.2824, ".4f")
show("L06 se scaling sqrt-rule 0.2781*sqrt(1800/57600)", 0.2781 * math.sqrt(1800 / 57600), ".5f")
show("L06 R1 rows for 0.05", 1800 * (0.2781 / 0.05) ** 2, ".1f")
show("L06 R1 firm-years at 10 percent share", 1800 * (0.2781 / 0.05) ** 2 / 0.9, ".1f")

# L06 M1 and M2
nda = 0.05 / 1000 + 0.10 * (120 - 30) / 1000 - 0.08 * 400 / 1000
show("L06 M1 NDA", nda, ".5f")
show("L06 M1 DA", -30 / 1000 - nda, ".5f")
c = 0.01 * N.inv_cdf(0.95)
show("L06 M2 c", c, ".5f")
show("L06 M2 detection", N.cdf((0.05 - c) / 0.01), ".4f")

# L06 lab flag arithmetic
show("L06 E1 precision", 71 / 200, ".3f")
show("L06 E1 false flags 0.0717*1800", 0.0717 * 1800, ".2f")
show("L06 E2 precision", 197 / 200, ".3f")
show("L06 E2 false flags 0.0017*1800", 0.0017 * 1800, ".2f")
show("L06 a1 difference printed", 0.3891 - 0.1806, ".4f")
show("L06 a1 decomposition 0.1425+0.1965-0.1306", 0.1425 + 0.1965 - 0.1306, ".4f")
