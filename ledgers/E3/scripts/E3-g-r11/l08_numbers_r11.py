"""Re-derive the L08 numbers with Fractions and the registry titles for the two cited keys."""
import json
from fractions import Fraction as F
W1, WL, W0 = 110000, 95000, 100000
def ce(p):  # CRRA gamma=2, u=-1/w, red prob p, gamble final wealth W1 / WL
    return 1 / (p / W1 + (1 - p) / WL)
print("EU CE at 1/2 =", ce(F(1, 2)), float(ce(F(1, 2))))
print("CE at 1/3 =", float(ce(F(1, 3))), " at 2/3 =", float(ce(F(2, 3))), " at 1/4 =", float(ce(F(1, 4))), " at 3/4 =", float(ce(F(3, 4))))
print("M2 maxmin {1/4,3/4} =", float(min(ce(F(1, 4)), ce(F(3, 4)))))
print("M3 tau=0 {1/4,3/4} = ", float(max(ce(F(1, 4)), ce(F(3, 4)))))
print("1672000/17 =", float(F(1672000, 17)), " 8360000/85 =", float(F(8360000, 85)))
print("risk premium 102500 - CE =", F(102500) - ce(F(1, 2)), float(F(102500) - ce(F(1, 2))), " /100 =", float((F(102500) - ce(F(1, 2))) / 100))
print("22500/41 =", float(F(22500, 41)))
# two-urn: prize 10000 on win, 0 otherwise, wealth 110000/100000
def cb(p):
    return 1 / (p / 110000 + (1 - p) / 100000)
print("known red 30/90 CE =", float(cb(F(30, 90))), " known black (60/90 black) CE =", float(1 / (F(2, 3) / 110000 + F(1, 3) / 100000)))
print("known black CE exact:", 1 / (F(2, 3) / 110000 + F(1, 3) / 100000), float(1 / (F(2, 3) / 110000 + F(1, 3) / 100000)))
print("R2: ambiguous set 30..60 red CE min at 1/3 =", float(min(cb(F(k, 90)) for k in range(30, 61))), " black min at black prob 1/3 =", float(min(cb(F(k, 90)) for k in range(30, 61))))
print("E1 difference 103125-100000 =", 103125 - 100000, "cents =", (103125 - 100000) / 100, "CU")
# prospect model numbers
import math
Vp = 0.5 * math.sqrt(100) + 0.5 * (-2 * math.sqrt(50))
print("Vp =", Vp, " 5 - sqrt50 =", 5 - math.sqrt(50))
inv = -((-Vp / 2) ** 2)
print("CE of change CU =", inv, " wealth =", W0 + 100 * inv)
# EZ at psi=1/2, beta 0.95, gamma 2 via closed form: CE = EU CE
a = 1 - 1 / 0.5
print("a =", a)
# registry titles
reg = json.load(open("references/references.json", encoding="utf-8"))
for e in reg["entries"]:
    if e.get("key") in ("ellsberg1961risk", "gilboa1989maxmin", "kahneman1979prospect", "epstein1989substitution"):
        print(e.get("key"), "|", e.get("title"), "|", e.get("year"), "|", e.get("venue", e.get("journal")), "| used_by", e.get("used_by"))
print("keys present:", [k for k in ("ellsberg1961risk", "gilboa1989maxmin") if any(e.get("key") == k for e in reg["entries"])])
