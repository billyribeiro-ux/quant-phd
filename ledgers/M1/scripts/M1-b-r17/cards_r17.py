import json, sys
from fractions import Fraction
c = {x["id"]: x for x in json.load(open(sys.argv[1]))}
for k in ["M1-c163", "M1-c072"]:
    print(k, c[k]["front"], "|", c[k]["back"])
# witness: m=2, r=0.05; 1 + r_m/m = -e^(r/m) satisfies the factor condition but gives r_m < r
import math
r, m = 0.05, 2
rm = m * (-math.exp(r/m) - 1)
print("even-m witness r_m =", round(rm, 6), "factor", round((1 + rm/m)**m, 10), "e^r", round(math.exp(r), 10), "r_m > r:", rm > r)
print("R3 positive root r_12 =", round(12*(math.exp(0.05/12)-1), 10))
