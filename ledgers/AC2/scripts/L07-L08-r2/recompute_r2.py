"""Independent recomputation of every number and proof-check in L07 and L08 (AC2), round 2.

Written from the page definitions (L07 Definition 1.1 table; L08 Definition 1.1 index list),
not from the lab code. Lab generators are re-typed from the twins only to regenerate the
SIMULATED firm-years; the signal and index logic here is independent of the twins.
Run: python3 -I recompute_r2.py
"""
import random
from fractions import Fraction as Fr

out = []
def say(*a):
    s = " ".join(str(x) for x in a)
    out.append(s)
    print(s)

# ---------- L07: worked firm (section 4) with exact fractions ----------
TA = {2: Fr(1000), 1: Fr(1100), 0: Fr(1200)}          # t-2, t-1, t
REV = {1: Fr(1320), 0: Fr(1560)}
COGS = {1: Fr(924), 0: Fr(1014)}
NI = {1: Fr(66), 0: Fr(117)}
CFO = {1: Fr(90), 0: Fr(96)}
LTD = {1: Fr(330), 0: Fr(264)}
CA = {1: Fr(440), 0: Fr(528)}
CL = {1: Fr(220), 0: Fr(240)}
SH = {1: Fr(50), 0: Fr(50)}

def worked_signals(NI, CFO, LTD, TA=TA, CA=CA, CL=CL, SH=SH):
    roa0 = NI[0] / TA[1]; roa1 = NI[1] / TA[2]
    cfo0 = CFO[0] / TA[1]
    lev0 = LTD[0] / ((TA[0] + TA[1]) / 2); lev1 = LTD[1] / ((TA[1] + TA[2]) / 2)
    cr0 = CA[0] / CL[0]; cr1 = CA[1] / CL[1]
    gm0 = (REV[0] - COGS[0]) / REV[0]; gm1 = (REV[1] - COGS[1]) / REV[1]
    ato0 = REV[0] / TA[1]; ato1 = REV[1] / TA[2]
    return (int(roa0 > 0), int(cfo0 > 0), int(roa0 > roa1), int(cfo0 > roa0), int(lev0 < lev1),
            int(cr0 > cr1), int(SH[0] <= SH[1]), int(gm0 > gm1), int(ato0 > ato1))

sig = worked_signals(NI, CFO, LTD)
say("L07 worked firm vector:", sig, "F =", sum(sig))
assert sig == (1,1,1,0,1,1,1,1,1) and sum(sig) == 8
say("ROA_t =", NI[0]/TA[1], float(NI[0]/TA[1]), " ROA_t-1 =", float(NI[1]/TA[2]))
say("CFO* =", float(CFO[0]/TA[1]), " accrual (NI-CFO)/TA_{t-1} =", float((NI[0]-CFO[0])/TA[1]))
say("LEV_t =", float(LTD[0]/((TA[0]+TA[1])/2)), " LEV_t-1 =", float(LTD[1]/((TA[1]+TA[2])/2)))
say("CR_t =", float(CA[0]/CL[0]), " CR_t-1 =", float(CA[1]/CL[1]))
say("GM_t =", float((REV[0]-COGS[0])/REV[0]), " GM_t-1 =", float((REV[1]-COGS[1])/REV[1]))
say("ATO_t =", float(REV[0]/TA[1]), " ATO_t-1 =", float(REV[1]/TA[2]))

# M2: NI_t = -20
NI2 = dict(NI); NI2[0] = Fr(-20)
s2 = worked_signals(NI2, CFO, LTD)
say("M2 (NI_t=-20) vector:", s2, "F =", sum(s2)); assert s2 == (0,1,0,1,1,1,1,1,1) and sum(s2)==7
say("M2 ROA_t =", float(NI2[0]/TA[1]))

# E2: smallest integer CFO_t with s4=1
c = 0
while not (worked_signals(NI, {1: CFO[1], 0: Fr(c)}, LTD)[3] == 1):
    c += 1
say("E2 smallest integer CFO_t with s4=1:", c, " ratio", float(Fr(c)/1100), "score", sum(worked_signals(NI, {1: CFO[1], 0: Fr(c)}, LTD)))

# E3: LTD_t = 300
s3 = worked_signals(NI, CFO, {1: LTD[1], 0: Fr(300)})
say("E3 LTD_t=300: LEV_t =", float(Fr(300)/1150), " s5 =", s3[4], " F =", sum(s3))

# Scale check on worked firm x1000 (exact)
k = Fr(1000)
TAk = {i: v*k for i, v in TA.items()}; REVk = {i: v*k for i, v in REV.items()}; COGSk = {i: v*k for i, v in COGS.items()}
NIk = {i: v*k for i, v in NI.items()}; CFOk = {i: v*k for i, v in CFO.items()}
LTDk = {i: v*k for i, v in LTD.items()}; CAk = {i: v*k for i, v in CA.items()}; CLk = {i: v*k for i, v in CL.items()}
REV_s, COGS_s = REV, COGS
REV.update(REVk); COGS.update(COGSk)
sk = worked_signals(NIk, CFOk, LTDk, TA=TAk, CA=CAk, CL=CLk)
REV.update(REV_s); COGS.update(COGS_s)
say("M3 scale x1000 vector:", sk, "F =", sum(sk)); assert sk == sig

# P3: TA(t-2)=1100, TA(t-1)=1000, TA(t)=900, LTD(t-1)=310, LTD(t)=300
TAp = {2: Fr(1100), 1: Fr(1000), 0: Fr(900)}
lev_t = Fr(300) / ((TAp[0] + TAp[1]) / 2); lev_t1 = Fr(310) / ((TAp[1] + TAp[2]) / 2)
say("P3 LEV_t =", float(lev_t), " LEV_t-1 =", float(lev_t1), " s5 =", int(lev_t < lev_t1))
assert not (lev_t < lev_t1)

# P1 and misconception 1 (ROA 0.15 from 0.20, CFO>0 but < NI, rising leverage, falling CR, rising shares, falling GM, falling ATO)
# Build a concrete instance satisfying the page's words; show F = 2.
TAm = {2: Fr(1000), 1: Fr(1000), 0: Fr(1000)}
NIm = {1: Fr(200), 0: Fr(150)}          # ROA_{t-1}=0.20 (NI_{t-1}/TA_{t-2}), ROA_t = 0.15 (NI_t/TA_{t-1})
CFOm = {1: Fr(100), 0: Fr(120)}         # CFO_t > 0 but < NI_t? 120 < 150 yes
LTDm = {1: Fr(100), 0: Fr(120)}         # rising leverage
CAm = {1: Fr(300), 0: Fr(250)}; CLm = {1: Fr(100), 0: Fr(120)}   # CR falls 3.0 -> 2.08
SHm = {1: Fr(50), 0: Fr(52)}            # shares rise
REVm = {1: Fr(1000), 0: Fr(1000)}; COGSm = {1: Fr(600), 0: Fr(650)}  # GM 0.40 -> 0.35 falls
TOTm = {2: Fr(1000), 1: Fr(1000), 0: Fr(1000)}
# ATO_t = REV_t/TA_{t-1} = 1000/1000 =1.0 ; ATO_{t-1} = REV_{t-1}/TA_{t-2} = 1000/1000 =1.0 -> need falling: make REV_t 950
REVm[0] = Fr(950)
sm = worked_signals(NIm, CFOm, LTDm, TA=TOTm, CA=CAm, CL=CLm, SH=SHm) if False else None
# worked_signals reads REV/COGS globals; compute with local substitutes
REV_g, COGS_g = dict(REV), dict(COGS)
REV.update(REVm); COGS.update(COGSm)
sm = worked_signals(NIm, CFOm, LTDm, TA=TOTm, CA=CAm, CL=CLm, SH=SHm)
REV.clear(); REV.update(REV_g); COGS.clear(); COGS.update(COGS_g)
say("Misconception 1 instance (ROA_t 0.15 from 0.20) vector:", sm, "F =", sum(sm))
say("  ROA_t =", float(NIm[0]/TOTm[1]), "ROA_t-1 =", float(NIm[1]/TOTm[2]), "CFO_t/TA_t-1 =", float(CFOm[0]/TOTm[1]))

# M2 in the page: s1=0 (ROA negative), others as stated
# ---------- L07 Lab output recomputation (generator re-typed from the twin) ----------
SEED = 20260527
def gen(rng):
    assets = rng.uniform(800.0, 1200.0); margin = rng.uniform(0.03, 0.12); gm = rng.uniform(0.25, 0.55)
    turn = rng.uniform(0.8, 1.6); ltd_share = rng.uniform(0.10, 0.45); shares = rng.uniform(40.0, 60.0)
    years = []
    for _ in range(3):
        growth = rng.uniform(0.92, 1.10); assets = assets * growth
        revenue = assets * turn * rng.uniform(0.9, 1.1)
        cogs = revenue * (1.0 - gm * rng.uniform(0.9, 1.1))
        net_income = revenue * margin * rng.uniform(0.6, 1.4)
        accrual = rng.uniform(-0.04, 0.04) * assets
        cfo = net_income - accrual
        ca = assets * rng.uniform(0.25, 0.45); cl = assets * rng.uniform(0.15, 0.35)
        ltd = assets * ltd_share * rng.uniform(0.9, 1.1)
        shares = shares * rng.choice((1.0, 1.0, 1.0, 1.02))
        years.append(dict(rev=revenue, cogs=cogs, ni=net_income, cfo=cfo, ta=assets, ca=ca, cl=cl, ltd=ltd, sh=shares))
        margin = max(0.005, margin + rng.uniform(-0.01, 0.01))
        gm = min(0.9, max(0.05, gm + rng.uniform(-0.02, 0.02)))
        turn = max(0.3, turn + rng.uniform(-0.1, 0.1))
    return years[0], years[1], years[2]

def sig_of(y2, y1, y0):
    roa0 = y0['ni'] / y1['ta']; roa1 = y1['ni'] / y2['ta']; cfo0 = y0['cfo'] / y1['ta']
    lev0 = y0['ltd'] / ((y0['ta'] + y1['ta']) / 2); lev1 = y1['ltd'] / ((y1['ta'] + y2['ta']) / 2)
    gm0 = (y0['rev'] - y0['cogs']) / y0['rev']; gm1 = (y1['rev'] - y1['cogs']) / y1['rev']
    ato0 = y0['rev'] / y1['ta']; ato1 = y1['rev'] / y2['ta']
    cr0 = y0['ca'] / y0['cl']; cr1 = y1['ca'] / y1['cl']
    return (int(roa0 > 0), int(cfo0 > 0), int(roa0 > roa1), int(y0['cfo'] > y0['ni']), int(lev0 < lev1),
            int(cr0 > cr1), int(y0['sh'] <= y1['sh']), int(gm0 > gm1), int(ato0 > ato1))

rng = random.Random(SEED)
firms = [gen(rng) for _ in range(400)]
sigs = [sig_of(*f) for f in firms]
dist = [0]*10
for s in sigs: dist[sum(s)] += 1
say("L07 lab: score distribution", dist, " mean", round(sum(sum(s) for s in sigs)/400, 4))
say("L07 lab: first six vectors", ["".join(map(str, s)) for s in sigs[:6]])
say("L07 lab: scores 8 or 9 =", dist[8]+dist[9], " fraction", (dist[8]+dist[9])/400)

# ---------- L08 ----------
SEED8 = 20260528
def gen_clean(rng):
    assets = rng.uniform(900.0, 1100.0); revenue = assets * rng.uniform(0.9, 1.3); gm = rng.uniform(0.3, 0.5)
    years = []
    for _ in range(2):
        assets *= rng.uniform(0.97, 1.05); revenue *= rng.uniform(0.97, 1.06)
        ppe = assets * rng.uniform(0.25, 0.35); dep = ppe * rng.uniform(0.09, 0.12)
        sga = revenue * rng.uniform(0.15, 0.22); cogs = revenue * (1.0 - gm * rng.uniform(0.97, 1.03))
        rec = revenue * rng.uniform(0.11, 0.14); ca = assets * rng.uniform(0.3, 0.4)
        cl = assets * rng.uniform(0.2, 0.3); ltd = assets * rng.uniform(0.1, 0.2)
        ni = revenue * rng.uniform(0.02, 0.06); cfo = ni + rng.uniform(-0.03, 0.03) * assets
        years.append(dict(rev=revenue, cogs=cogs, rec=rec, ca=ca, ppe=ppe, ta=assets, dep=dep, sga=sga, cl=cl, ltd=ltd, ni=ni, cfo=cfo))
    return years[0], years[1]

def gen_planted(rng):
    p, t = gen_clean(rng)
    t_rec = t['rec'] * rng.uniform(1.35, 1.6)
    gm_p = (p['rev'] - p['cogs']) / p['rev']
    t_cogs = t['rev'] * (1.0 - gm_p * rng.uniform(0.7, 0.85))
    t_dep = p['dep'] * rng.uniform(0.7, 0.85)
    t_cfo = t['ni'] - rng.uniform(0.06, 0.1) * t['ta']
    tt = dict(t); tt.update(rec=t_rec, cogs=t_cogs, dep=t_dep, cfo=t_cfo)
    return p, tt

W = {'DSRI': 0.920, 'GMI': 0.528, 'AQI': 0.404, 'SGI': 0.892, 'DEPI': 0.115, 'SGAI': -0.172, 'LVGI': -0.327, 'TATA': 4.679}
INTERCEPT = -4.84

def idx(t, p):
    gm = lambda f: (f['rev'] - f['cogs']) / f['rev']
    dsri = (t['rec']/t['rev']) / (p['rec']/p['rev'])
    gmi = gm(p) / gm(t)
    aq_t = 1 - (t['ca'] + t['ppe'] if 'ppe' in t else 0)/t['ta']
    aqi = (1 - (t['ca'] + t['ppe'])/t['ta']) / (1 - (p['ca'] + p['ppe'])/p['ta'])
    sgi = t['rev']/p['rev']
    depi = (p['dep']/(p['dep']+p['ppe'])) / (t['dep']/(t['dep']+t['ppe']))
    sgai = (t['sga']/t['rev']) / (p['sga']/p['rev'])
    lvgi = ((t['cl']+t['ltd'])/t['ta']) / ((p['cl']+p['ltd'])/p['ta'])
    tata = (t['ni']-t['cfo'])/t['ta']
    return dict(DSRI=dsri, GMI=gmi, AQI=aqi, SGI=sgi, DEPI=depi, SGAI=sgai, LVGI=lvgi, TATA=tata)

def M(ix):
    return INTERCEPT + sum(W[k]*ix[k] for k in W)

# worked firm of L08 section 3
t1 = dict(rev=1000, cogs=600, rec=100, ca=400, ppe=300, ta=1000, dep=30, sga=150, cl=200, ltd=200, ni=40, cfo=45)
t0 = dict(rev=1200, cogs=780, rec=180, ca=480, ppe=330, ta=1200, dep=30, sga=180, cl=250, ltd=220, ni=60, cfo=20)
ix = idx(t0, t1)
for k, v in ix.items(): say(f"  worked {k} = {v:.6f}")
Mw = M(ix)
say("L08 worked-firm M (candidate constants) =", f"{Mw:.6f}")
say("  page term check: -4.84+0.92*1.5+0.528*1.1429+0.404*1.0833+0.892*1.2+0.115*1.0909-0.172*1-0.327*0.9792+4.679*0.0333 =",
    f"{-4.84+0.92*1.5+0.528*1.1429+0.404*1.0833+0.892*1.2+0.115*1.0909-0.172*1-0.327*0.9792+4.679*0.0333:.6f}")
# rounded-from-page computation (exactly as the page prints the indices)
ixr = dict(DSRI=1.5, GMI=1.1429, AQI=1.0833, SGI=1.2, DEPI=1.0909, SGAI=1.0, LVGI=0.9792, TATA=0.0333)
say("  using page-rounded indices: M =", f"{M(ixr):.6f}")

# Lab-style generation and medians
rng8 = random.Random(SEED8)
clean = [gen_clean(rng8) for _ in range(300)]
planted = [gen_planted(rng8) for _ in range(300)]
def med(xs):
    s = sorted(xs); n = len(s); m = n//2
    return s[m] if n % 2 else (s[m-1]+s[m])/2
mc = [M(idx(t, p)) for p, t in clean]
mp = [M(idx(t, p)) for p, t in planted]
say("L08 lab: clean median M =", f"{med(mc):.4f}", " planted median M =", f"{med(mp):.4f}", " gap =", f"{med(mp)-med(mc):.4f}")
p0, t0p = planted[0]
ix0 = idx(t0p, p0)
say("L08 lab planted firm 0 indices:", {k: round(v, 4) for k, v in ix0.items()}, " M =", f"{M(ix0):.4f}")
say("L08 lab: planted median minus clean median (page E1 says 0.9680) =", f"{med(mp)-med(mc):.4f}")

# base-rate PPV formula with Bayes: PPV = p s/(p s + (1-p)(1-spec)), s=0.5
for pr in (0.001, 0.01, 0.05):
    for sp in (0.90, 0.95, 0.99):
        fpr = 1 - sp
        ppv = pr*0.5/(pr*0.5 + (1-pr)*fpr)
        say(f"  prev {pr} spec {sp} FPR {fpr:.3f} PPV {ppv:.4f} flags/1000 {1000*(1-pr)*fpr:.2f}")
say("E2 ratio PPV(0.05)/PPV(0.001) at spec 0.95:", round((0.05*0.5/(0.05*0.5+0.95*0.05))/(0.001*0.5/(0.001*0.5+0.999*0.05)), 2))
say("PPV at prev 0.01 spec 0.95 =", 0.005/0.0545, " quiz answer check")
say("AND/OR at f1=0.10,f2=0.05 under independence:", 0.10*0.05, 1-(0.9*0.95))
# dependence witness: never flag the same clean firm
say("Witness (disjoint flags): AND =", 0.0, " OR =", 0.10+0.05-0.0)
# covariance sign check: AND = f1 f2 + c, OR = f1+f2-(f1 f2 + c)
for c in (0.002, 0.0, -0.003):
    say(f"  cov {c:+.3f}: AND {0.005+c:.4f}  OR {0.15-(0.005+c):.4f}")

# Sensitivity bounds (P3) check on a discrete example
# Proposition 4.2 numeric: PPV is increasing in prevalence
vals = [pr*0.5/(pr*0.5+(1-pr)*0.05) for pr in (0.001, 0.01, 0.05)]
say("PPV increasing in prevalence at spec 0.95:", vals == sorted(vals))
