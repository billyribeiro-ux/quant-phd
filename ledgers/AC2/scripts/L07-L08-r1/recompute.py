"""Independent recomputation for AC2 slice L07-L08 (verifier round 1).

Written from the page text and the contract formulas, not from the lab code.
Exact rational arithmetic (fractions.Fraction) wherever the page's claim is exact.
Run: <checkout>/.venv/bin/python -I ledgers/AC2/scripts/L07-L08-r1/recompute.py
"""
from fractions import Fraction as Fr
from math import comb

FAIL = []


def check(label, got, want, tol=None):
    ok = (abs(float(got) - float(want)) <= tol) if tol is not None else (got == want)
    print(f"{'OK  ' if ok else 'DIFF'} {label}: got={got} want={want}")
    if not ok:
        FAIL.append(label)


# ---------- L07: worked firm (page section 4) ----------
TA = {2: Fr(1000), 1: Fr(1100), 0: Fr(1200)}          # t-2, t-1, t
REV = {1: Fr(1320), 0: Fr(1560)}
COGS = {1: Fr(924), 0: Fr(1014)}
NI = {1: Fr(66), 0: Fr(117)}
CFO = {1: Fr(90), 0: Fr(96)}
LTD = {1: Fr(330), 0: Fr(264)}
CA = {1: Fr(440), 0: Fr(528)}
CL = {1: Fr(220), 0: Fr(240)}
SH = {1: Fr(50), 0: Fr(50)}


def f_score(NI, CFO, LTD, CA, CL, SH, REV, COGS, TA):
    roa = {t: NI[t] / TA[t + 1] for t in (0, 1)}
    cfo = {t: CFO[t] / TA[t + 1] for t in (0, 1)}
    lev = {t: LTD[t] / ((TA[t] + TA[t + 1]) / 2) for t in (0, 1)}
    cr = {t: CA[t] / CL[t] for t in (0, 1)}
    gm = {t: (REV[t] - COGS[t]) / REV[t] for t in (0, 1)}
    ato = {t: REV[t] / TA[t + 1] for t in (0, 1)}
    s = (
        int(roa[0] > 0), int(cfo[0] > 0), int(roa[0] > roa[1]), int(cfo[0] > roa[0]),
        int(lev[0] < lev[1]), int(cr[0] > cr[1]), int(SH[0] <= SH[1]),
        int(gm[0] > gm[1]), int(ato[0] > ato[1]),
    )
    return s, sum(s), roa, lev


s, F, roa, lev = f_score(NI, CFO, LTD, CA, CL, SH, REV, COGS, TA)
check("worked firm vector", s, (1, 1, 1, 0, 1, 1, 1, 1, 1))
check("worked firm F", F, 8)
check("worked ROA_t", roa[0], Fr(117, 1100))
check("worked ROA_t-1", roa[1], Fr(66, 1000))
check("worked accrual (NI-CFO)/TA_{t-1}", (NI[0] - CFO[0]) / TA[1], Fr(21, 1100))
check("worked LEV_t", lev[0], Fr(264, 1150))
check("worked LEV_t-1", lev[1], Fr(330, 1050))

# M2: NI_t = -20
NI2 = dict(NI); NI2[0] = Fr(-20)
s2, F2, _, _ = f_score(NI2, CFO, LTD, CA, CL, SH, REV, COGS, TA)
check("M2 vector", s2, (0, 1, 0, 1, 1, 1, 1, 1, 1))
check("M2 F", F2, 7)

# M3: scale every money item by 1000 (shares unchanged)
k = Fr(1000)
s3, F3, roa3, _ = f_score({t: v * k for t, v in NI.items()}, {t: v * k for t, v in CFO.items()},
                          {t: v * k for t, v in LTD.items()}, {t: v * k for t, v in CA.items()},
                          {t: v * k for t, v in CL.items()}, SH, {t: v * k for t, v in REV.items()},
                          {t: v * k for t, v in COGS.items()}, {t: v * k for t, v in TA.items()})
check("M3 ROA_t unchanged", roa3[0], Fr(117, 1100))
check("M3 F unchanged", F3, 8)

# E2: smallest integer CFO_t making s4 = 1 (needs CFO_t > NI_t = 117)
cfo_min = next(c for c in range(0, 1000) if Fr(c) > NI[0])
check("E2 smallest integer CFO", cfo_min, 118)
check("E2 CFO*/ROA check 118/1100 > 117/1100", Fr(118, 1100) > Fr(117, 1100), True)
CFO_E2 = dict(CFO); CFO_E2[0] = Fr(118)
s4, F4, _, _ = f_score(NI, CFO_E2, LTD, CA, CL, SH, REV, COGS, TA)
check("E2 score", F4, 9)

# E3: LTD_t = 300
LTD_E3 = dict(LTD); LTD_E3[0] = Fr(300)
s5, F5, _, lev5 = f_score(NI, CFO, LTD_E3, CA, CL, SH, REV, COGS, TA)
check("E3 LEV_t", lev5[0], Fr(300, 1150))
check("E3 s5", s5[4], 1)
check("E3 F", F5, 8)

# P3: average-assets example
TA3 = {2: Fr(1100), 1: Fr(1000), 0: Fr(900)}
LEV_t = Fr(300) / ((TA3[0] + TA3[1]) / 2)
LEV_t1 = Fr(310) / ((TA3[1] + TA3[2]) / 2)
check("P3 LEV_t", LEV_t, Fr(300, 950))
check("P3 LEV_t-1", LEV_t1, Fr(310, 1050))
check("P3 s5 = 0 (LEV_t > LEV_t-1)", int(LEV_t < LEV_t1), 0)

# E1 (L07): count of score 8 or 9 in the printed distribution
dist = {0: 0, 1: 0, 2: 2, 3: 16, 4: 60, 5: 108, 6: 109, 7: 74, 8: 24, 9: 7}
check("E1 total firm-years", sum(dist.values()), 400)
check("E1 score 8 or 9 count", dist[8] + dist[9], 31)
check("E1 fraction 31/400", Fr(dist[8] + dist[9], 400), Fr(31, 400))
check("L07 mean score", Fr(sum(k2 * v for k2, v in dist.items()), 400), Fr(2259, 400), tol=None)

# ---------- L08: worked firm (page section 3) ----------
R1, R0 = Fr(1000), Fr(1200)
REC1, REC0 = Fr(100), Fr(180)
COGS1, COGS0 = Fr(600), Fr(780)
CA1, CA0 = Fr(400), Fr(480)
PPE1, PPE0 = Fr(300), Fr(330)
TA1, TA0 = Fr(1000), Fr(1200)
DEP1, DEP0 = Fr(30), Fr(30)
SGA1, SGA0 = Fr(150), Fr(180)
CL1, CL0 = Fr(200), Fr(250)
LTD1, LTD0 = Fr(200), Fr(220)
NI1, NI0 = Fr(40), Fr(60)
CFO1, CFO0 = Fr(45), Fr(20)

gm1 = (R1 - COGS1) / R1
gm0 = (R0 - COGS0) / R0
a1 = 1 - (CA1 + PPE1) / TA1
a0 = 1 - (CA0 + PPE0) / TA0
idx = {
    "DSRI": (REC0 / R0) / (REC1 / R1),
    "GMI": gm1 / gm0,
    "AQI": a0 / a1,
    "SGI": R0 / R1,
    "DEPI": (DEP1 / (DEP1 + PPE1)) / (DEP0 / (DEP0 + PPE0)),
    "SGAI": (SGA0 / R0) / (SGA1 / R1),
    "LVGI": ((CL0 + LTD0) / TA0) / ((CL1 + LTD1) / TA1),
    "TATA": (NI0 - CFO0) / TA0,
}
check("DSRI", idx["DSRI"], Fr(3, 2))
check("GMI", idx["GMI"], Fr(40, 35), tol=1e-12)
check("AQI", idx["AQI"], Fr(13, 12), tol=1e-12)
check("SGI", idx["SGI"], Fr(6, 5))
check("DEPI", idx["DEPI"], Fr(12, 11), tol=1e-12)
check("SGAI", idx["SGAI"], Fr(1))
check("LVGI", idx["LVGI"], Fr(470, 480), tol=1e-12)
check("TATA", idx["TATA"], Fr(1, 30), tol=1e-12)

# Candidate (UNCONFIRMED) constants, as printed on the page, TATA 4.679
CONST = -4.84
W = {"DSRI": 0.920, "GMI": 0.528, "AQI": 0.404, "SGI": 0.892, "DEPI": 0.115,
     "SGAI": -0.172, "LVGI": -0.327, "TATA": 4.679}
M = CONST + sum(W[k] * float(idx[k]) for k in W)
check("M worked firm, TATA 4.679 (page -1.5593)", round(M, 4), -1.5593, tol=1e-9)
M_697 = M + (4.697 - 4.679) * float(idx["TATA"])
print(f"info: M with TATA 4.697 instead = {M_697:.4f} (page does not print this)")

# ---------- L08: base-rate table (Proposition 4.2) ----------
SENS = Fr(1, 2)
printed = {  # prevalence, spec -> (PPV printed, flags printed)
    (Fr(1, 1000), Fr(9, 10)): (0.0050, 99.90), (Fr(1, 1000), Fr(95, 100)): (0.0099, 49.95),
    (Fr(1, 1000), Fr(99, 100)): (0.0477, 9.99), (Fr(1, 100), Fr(9, 10)): (0.0481, 99.00),
    (Fr(1, 100), Fr(95, 100)): (0.0917, 49.50), (Fr(1, 100), Fr(99, 100)): (0.3356, 9.90),
    (Fr(5, 100), Fr(9, 10)): (0.2083, 95.00), (Fr(5, 100), Fr(95, 100)): (0.3448, 47.50),
    (Fr(5, 100), Fr(99, 100)): (0.7246, 9.50),
}
ppv_exact = {}
for (p, sp), (ppv_p, flags_p) in printed.items():
    fpr = 1 - sp
    ppv = p * SENS / (p * SENS + (1 - p) * fpr)
    flags = 1000 * (1 - p) * fpr
    ppv_exact[(p, sp)] = ppv
    check(f"PPV p={float(p)} spec={float(sp)}", round(float(ppv), 4), ppv_p, tol=1e-9)
    check(f"flags p={float(p)} spec={float(sp)}", round(float(flags), 2), flags_p, tol=1e-9)

check("PPV p=0.01 spec=0.95 page example 0.005/0.0545", ppv_exact[(Fr(1, 100), Fr(95, 100))],
      Fr(5, 1000) / Fr(545, 10000))
ratio = ppv_exact[(Fr(5, 100), Fr(95, 100))] / ppv_exact[(Fr(1, 1000), Fr(95, 100))]
print(f"info: E2 ratio exact = {float(ratio):.4f} (page says about 35, 34.8)")
check("E2 ratio to 2 significant figures", round(float(ratio)), 35)
check("E2 printed-ratio 0.3448/0.0099", round(0.3448 / 0.0099, 1), 34.8, tol=1e-9)

# E1 (L08): planted minus clean median
check("E1 L08 gap", round(-1.5067 - (-2.4747), 4), 0.9680, tol=1e-9)

# Proposition 4.3: AND and OR FPR for f1=0.10, f2=0.05
f1, f2 = Fr(1, 10), Fr(1, 20)
check("AND under independence", f1 * f2, Fr(1, 200))
check("OR under independence", 1 - (1 - f1) * (1 - f2), Fr(29, 200))

# Dependence witnesses: a joint law on (F1, F2) among clean firms with marginals f1, f2.
# P(both) = b. P(F1 only) = f1-b, P(F2 only) = f2-b, P(neither) = 1-f1-f2+b. Feasible for b in [max(0,f1+f2-1), min(f1,f2)].
def joint(b):
    return {"both": b, "only1": f1 - b, "only2": f2 - b, "none": 1 - f1 - f2 + b}
for label, b in [("positive dependence b=0.02", Fr(2, 100)), ("negative dependence b=0", Fr(0))]:
    j = joint(b)
    and_fpr = j["both"]
    or_fpr = 1 - j["none"]
    print(f"info: {label}: AND FPR={float(and_fpr):.4f} (product {float(f1*f2):.4f}), "
          f"OR FPR={float(or_fpr):.4f} (independence {float(1-(1-f1)*(1-f2)):.4f})")
check("positive dependence raises AND above product", joint(Fr(2, 100))["both"] > f1 * f2, True)
check("negative dependence lowers AND below product (page claims higher under correlated)",
      joint(Fr(0))["both"] < f1 * f2, True)

print("\nFAILED LABELS:", FAIL if FAIL else "none")
