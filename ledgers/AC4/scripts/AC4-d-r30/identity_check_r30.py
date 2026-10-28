# L08 identity and sign counts recomputed in exact Fractions from the printed OI and C (the eight SIM rows and the boundary).
from fractions import Fraction as F
divs = [("SIM-A", 59000, 2870), ("SIM-B", 53000, 4070), ("SIM-C", 173000, 14600), ("SIM-D", 124000, 7030),
        ("SIM-E", 78000, 3380), ("SIM-F", 27000, 3600), ("SIM-G", 127000, 13680), ("SIM-H", 161000, 23290)]
r, t = F(9, 100), F(2, 10)
print("gap identity:", sum(1 for n, C, OI in divs if (OI * (1 - t) - r * C) - (OI - r * C) == -t * OI), "/8")
allp = divs + [("BOUNDARY", 1000, 90)]
print("sign:", sum(1 for n, C, OI in allp if ((OI - r * C) >= 0) == (F(OI, C) >= r)), "/9")
