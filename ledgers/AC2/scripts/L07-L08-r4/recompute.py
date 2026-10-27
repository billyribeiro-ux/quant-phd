"""Round-4 independent recomputation (exact Fractions) of the worked numbers in L07 and L08."""
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

def r(x, n):
    q = Decimal(1).scaleb(-n)
    return Decimal(str(float(x))).quantize(q, rounding=ROUND_HALF_UP)

# ---- L07 worked firm ----
TA = {2: F(1000), 1: F(1100), 0: F(1200)}
REV = {1: F(1320), 0: F(1560)}
COGS = {1: F(924), 0: F(1014)}
NI = {1: F(66), 0: F(117)}
CFO = {1: F(90), 0: F(96)}
LTD = {1: F(330), 0: F(264)}
CA = {1: F(440), 0: F(528)}
CL = {1: F(220), 0: F(240)}
SH = {1: F(50), 0: F(50)}
roa = {0: NI[0] / TA[1], 1: NI[1] / TA[2]}
cfo_s = CFO[0] / TA[1]
lev = {0: LTD[0] / ((TA[0] + TA[1]) / 2), 1: LTD[1] / ((TA[1] + TA[2]) / 2)}
cr = {t: CA[t] / CL[t] for t in (0, 1)}
gm = {t: (REV[t] - COGS[t]) / REV[t] for t in (0, 1)}
ato = {0: REV[0] / TA[1], 1: REV[1] / TA[2]}
s = [int(roa[0] > 0), int(cfo_s > 0), int(roa[0] > roa[1]), int(cfo_s > roa[0]), int(lev[0] < lev[1]),
     int(cr[0] > cr[1]), int(SH[0] <= SH[1]), int(gm[0] > gm[1]), int(ato[0] > ato[1])]
print("L07 worked signals", s, "F =", sum(s))
print("ROA_t", float(roa[0]), "ROA_t-1", float(roa[1]), "CFO*", float(cfo_s), "LEV_t", float(lev[0]), "LEV_t-1", float(lev[1]))
print("accrual (117-96)/1100 =", float(F(21, 1100)))
# M2: NI_t = -20
roa_m2 = F(-20) / TA[1]
s2 = [int(roa_m2 > 0), int(cfo_s > 0), int(roa_m2 > roa[1]), int(cfo_s > roa_m2), 1, 1, 1, 1, 1]
print("M2 vector", s2, "F =", sum(s2), "ROA_m2", float(roa_m2))
# E2: smallest integer CFO making s4=1
print("E2 118/1100 =", float(F(118, 1100)), "> ROA", float(roa[0]), F(118, 1100) > roa[0])
# E3: LTD_t=300
print("E3 LEV_t", float(F(300, 1150)), "< LEV_t-1", float(lev[1]), F(300, 1150) < lev[1])
# P3 example
TA3 = {2: F(1100), 1: F(1000), 0: F(900)}
LTD3 = {1: F(310), 0: F(300)}
lt = F(300) / ((F(900) + F(1000)) / 2)
lp = F(310) / ((F(1000) + F(1100)) / 2)
print("P3 LEV_t", float(lt), "LEV_t-1", float(lp), "s5 =", int(lt < lp))
# ---- L07 misconception example: ROA 0.20 -> 0.15 ----
print("L07 misconception: ROA 0.15 vs 0.20 means s3 =", int(F(15, 100) > F(20, 100)))

# ---- L08 worked firm ----
t = dict(rev=F(1200), rec=F(180), cogs=F(780), ca=F(480), ppe=F(330), ta=F(1200), dep=F(30), sga=F(180), cl=F(250), ltd=F(220), ni=F(60), cfo=F(20))
p = dict(rev=F(1000), rec=F(100), cogs=F(600), ca=F(400), ppe=F(300), ta=F(1000), dep=F(30), sga=F(150), cl=F(200), ltd=F(200), ni=F(40), cfo=F(45))
gm_t = (t["rev"] - t["cogs"]) / t["rev"]
gm_p = (p["rev"] - p["cogs"]) / p["rev"]
idx = {}
idx["DSRI"] = (t["rec"] / t["rev"]) / (p["rec"] / p["rev"])
idx["GMI"] = gm_p / gm_t
aq_t = 1 - (t["ca"] + t["ppe"]) / t["ta"]
aq_p = 1 - (p["ca"] + p["ppe"]) / p["ta"]
idx["AQI"] = aq_t / aq_p
idx["SGI"] = t["rev"] / p["rev"]
idx["DEPI"] = (p["dep"] / (p["dep"] + p["ppe"])) / (t["dep"] / (t["dep"] + t["ppe"]))
idx["SGAI"] = (t["sga"] / t["rev"]) / (p["sga"] / p["rev"])
idx["LVGI"] = ((t["cl"] + t["ltd"]) / t["ta"]) / ((p["cl"] + p["ltd"]) / p["ta"])
idx["TATA"] = (t["ni"] - t["cfo"]) / t["ta"]
w = {"DSRI": F("0.920"), "GMI": F("0.528"), "AQI": F("0.404"), "SGI": F("0.892"), "DEPI": F("0.115"), "SGAI": F("-0.172"), "LVGI": F("-0.327"), "TATA": F("4.679")}
M = F("-4.84") + sum(w[k] * idx[k] for k in w)
for k in idx:
    print("index", k, float(idx[k]), "displayed 4dp", r(idx[k], 4))
print("M exact (unrounded indices) =", float(M), "->", r(M, 4))
# displayed-term sum: each index rounded to 4 dp, each product rounded to 4 dp? Test both conventions
disp = {k: r(v, 4) for k, v in idx.items()}
term_sum_disp_idx = F("-4.84") + sum(w[k] * F(str(disp[k])) for k in w)
print("M with 4dp indices, unrounded product =", float(term_sum_disp_idx), "->", r(term_sum_disp_idx, 4))
# the line-436 display: terms with their printed values
printed_terms = [F("0.920") * F("1.5"), F("0.528") * F("1.1429"), F("0.404") * F("1.0833"), F("0.892") * F("1.2"),
                 F("0.115") * F("1.0909"), F("-0.172") * F("1.0"), F("-0.327") * F("0.9792"), F("4.679") * F("0.0333")]
print("printed-term sum with intercept:", float(F("-4.84") + sum(printed_terms)), "->", r(F("-4.84") + sum(printed_terms), 4))
print("printed-term terms (each rounded to 4dp):", [str(r(x, 4)) for x in printed_terms])
print("sum of 4dp-rounded terms with intercept:", sum(r(x, 4) for x in printed_terms) + Decimal("-4.84"))

# ---- Base-rate table ----
print("PPV table")
for prev in (F(1, 1000), F(1, 100), F(5, 100)):
    for spec in (F(90, 100), F(95, 100), F(99, 100)):
        sens = F(1, 2)
        fpr = 1 - spec
        ppv = prev * sens / (prev * sens + (1 - prev) * fpr)
        flags = 1000 * (1 - prev) * fpr
        print(float(prev), float(spec), float(fpr), round(float(ppv), 6), float(flags))
print("E2 ratio 0.3448/0.0099 =", 0.3448 / 0.0099, "exact PPV ratio", float((F(5,100)*F(1,2)/(F(5,100)*F(1,2)+F(95,100)*F(5,100)))/(F(1,1000)*F(1,2)/(F(1,1000)*F(1,2)+F(999,1000)*F(5,100)))))
print("E1 gap", -1.5067 - (-2.4747))
# AND/OR
print("AND/OR independence", F(10,100)*F(5,100), 1 - (1 - F(10,100))*(1 - F(5,100)))
print("never-overlap OR", F(10,100)+F(5,100))
# growth witness
print("growth witness DSRI", (F(150)/F(1500))/(F(100)/F(1000)), "SGAI", (F(225)/F(1500))/(F(150)/F(1000)), "SGI", F(1500)/F(1000))
# PPV at prevalence .01 spec .95 sens .5
print("PPV quiz", float(F(1,100)*F(1,2)/(F(1,100)*F(1,2)+F(99,100)*F(5,100))))
# E3 check
print("E3 1000*(1-0.01)*0.05 =", 1000*(1-0.01)*0.05)
