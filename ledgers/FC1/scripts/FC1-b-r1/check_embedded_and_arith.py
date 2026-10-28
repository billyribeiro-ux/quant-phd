"""Verifier script: (1) every line of the lab run output appears in the lesson text; (2) independent arithmetic for the L04/L05 prose figures."""
import sys
from fractions import Fraction

out_lines = [ln.rstrip("\n") for ln in open(sys.argv[1], encoding="utf-8") if ln.strip()]
page = open(sys.argv[2], encoding="utf-8").read()
missing = [ln for ln in out_lines if ln not in page]
print("output lines", len(out_lines), "not found verbatim in page:", len(missing))
for ln in missing[:5]:
    print("  MISSING:", ln[:120])
print("L04 5600/173 =", float(Fraction(5600, 173)), "exact", Fraction(5600, 173))
print("L04 59700+39600 =", 59700 + 39600, "/100 =", (59700 + 39600) / 100)
print("L04 60*1000+90*1100 =", 60 * 1000 + 90 * 1100, "/150 =", (60 * 1000 + 90 * 1100) / 150)
print("L05 216*10060 =", 216 * 10060, "100*10090 =", 100 * 10090)
NP, G = 14282414, 68398886
print("L05 NP/G =", NP / G, "half-up 3dp check floor(1000*NP/G+1/2) =", (2000 * NP + G) // (2 * G))
print("L05 P5 receipt / G =", 11060360 / G, "-> %.2f%%" % (100 * 11060360 / G))
print("L05 P5 receipt / NP =", 11060360 / NP, "-> %.2f%%" % (100 * 11060360 / NP))
print("L05 net payers sum", 7411991 + 6656379 + 214044, "positives", 3222054 + 11060360, "sum all", -7411991 - 6656379 + 3222054 - 214044 + 11060360)
print("L05 bound check NP<=G", NP <= G)
