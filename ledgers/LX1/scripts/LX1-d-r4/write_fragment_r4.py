"""Write the round-4 fragment for LX1-d (cards.json against L01-L04). Evidence strings cite the scripts and outputs under this folder."""
import json
from datetime import UTC, datetime

from_out = "ledgers/LX1/scripts/LX1-d-r4/out"
TW = {"L01": "twin_L01.out", "L02": "twin_L02.out", "L03": "twin_L03.out", "L04": "twin_L04.out"}

E = {
    "c001": "cards.json LX1-c001 vs L01 Definition 1.2 (out/L01_text.txt:21-24): F_t = sum_k d_(t+k)/(1+r)^k whenever the series converges; a benchmark, not a forecast. Ungraded definition; matches.",
    "c002": "L01 Theorem 1.3 statement (out/L01_text.txt:25-28) and hypotheses A0/A1 (out/L01_text.txt:16-19): F_t = d_1(1+g)^t/(r-g) = d_(t+1)/(r-g), F_0 = d_1/(r-g), series converges. recompute_lessons.py: F_0 = 20000/3 = 6666.67, rounds 6667. Matches; T.",
    "c003": "L01 Theorem 1.3 (out/L01_text.txt:28): S_N(t) = F_t(1-q^N) for every N>=1, q=(1+g)/(1+r); Part A (out/L01 twin, twin_L01.out) prints identity True for N=10,60,200. recompute_lessons.py: identity True for N=10,60,200 (exact Fraction). Matches; T.",
    "c004": "L01 proof of Theorem 1.3 (out/L01_text.txt:35): 0<q<1 under A0, q^N->0, S_N(t)->F_t. recompute_lessons.py: q=103/109, 0<q<1 True. Matches; T.",
    "c005": "L01 Proposition 1.4 (out/L01_text.txt:37-40): (A1) d_1>0, 1+g>0; (A2) r>-1, g>=r; S_N(0)->+inf; series diverges; Theorem 1.3 does not apply. Matches; T.",
    "c006": "L01 Definition 2.1 (out/L01_text.txt:43-44): B_t = P_t - F_t counted as bubble only when B_t>0, measured in cents; B_t<=0 no bubble. Matches; ungraded definition.",
    "c007": "L01 Proposition 2.2 (out/L01_text.txt:45-49): (A3) d_1>0; (A4) g<g', r>g, r>g', 1+g>0, 1+g'>0; conclusion F_0(g)<F_0(g') and the positive/non-positive gap split. Proof at out/L01_text.txt:49. Matches; T.",
    "c008": "L01 Definition 3.1 (out/L01_text.txt:61-62): sudden collective demand to convert claims; prices fall together or trading stops; names mechanism only, no frequency/trigger/size. Matches; T.",
    "c009": "twin_L01.out Part B 'periods with price above fundamental: 9 of 13'; L01 key results (out/L01_text.txt:140-161) 'Count of positive-gap periods is 9 of 13 ... C'. Matches; C with SIMULATED basis.",
    "c010": "twin_L01.out Part C 'periods with price above the alternative fundamental: 13 of 13'; L01 key results 'C'. Matches; C with SIMULATED basis.",
    "c011": "L01 Proposition 2.2 numerical witness (out/L01_text.txt:51): d_1=400, r=9%, g=1% gives F_0=5000, g'=3% gives 20000/3, P_0=6000 gives +1000 and -2000/3. recompute_lessons.py: gaps +1000.0 and -666.67. Matches; T.",
    "c012": "L01 Section 5 canon-breaks (out/L01_text.txt:72) and misconception 1 (out/L01_text.txt:82): 400/1.09 = 40000/109 rounds to 367; closed form at g=3% gives 6667. recompute_lessons.py: 366.97 -> 367; 6666.67 -> 6667. Matches; T.",
    "c013": "L01 Proposition 1.4 proof (out/L01_text.txt:40) and misconception 3 (out/L01_text.txt:85): each discounted dividend >= d_1/(1+r), partial sums unbounded, closed form not finite. Matches; T.",
    "c014": "L02 Definition 1.1 (out/L02_text.txt:17): parity kappa>0 grams per unit of currency; convertibility = issuer stands ready to buy and sell gold at the parity on demand. Matches; ungraded definition.",
    "c015": "L02 Proposition 1.2 (out/L02_text.txt:19-23): hypothesis (A1) issuer keeps parity at every date; one gram costs 1/kappa at every date. Matches; T.",
    "c016": "L02 Remark 1.3 (out/L02_text.txt:25) and proof (out/L02_text.txt:23): one price only; (A1) does not involve P_t, so conclusion holds for any P_t path. Matches; T.",
    "c017": "L02 Section 2 (out/L02_text.txt:27-28): V_t = D P_0 / P_t, D nominal amount in integer cents, P_0 base value. Matches; ungraded definition.",
    "c018": "L02 Proposition 2.1(a) (out/L02_text.txt:29-35): (A2) positive integer cents, paid in full and not renegotiated; (A3) P_t positive real; V_t/V_(t-1)=P_(t-1)/P_t with D P_0 cancelling. recompute_lessons.py: identity exact for every t. Matches; T.",
    "c019": "L02 Proposition 2.1(b) (out/L02_text.txt:31-36): hypotheses carry 'paid in full and not renegotiated' (round-3 FAIL fixed); V_H/V_0 = P_0/P_H by telescoping (out/L02_text.txt:36). Matches; T.",
    "c020": "L02 Definition 3.1 (out/L02_text.txt:41): rise in real value implied by the identity of Proposition 2.1 with D held fixed; states arithmetic consequence, not a cause. Matches; ungraded definition.",
    "c021": "L02 Corollary 3.2 (out/L02_text.txt:42-46): V_t > V_(t-1) iff P_t < P_(t-1); hypotheses (A2),(A3) of Proposition 2.1. Matches; T.",
    "c022": "L02 Proposition 2.1(a) and Remark 3.3 (out/L02_text.txt:47-48): factor P_(t-1)/P_t, larger than one in a fall; corollary gives direction only. Matches; T.",
    "c023": "L02 Corollary 3.2 (out/L02_text.txt:42-46) and Section 5 misconception 1 (out/L02_text.txt:62-63, 'cheaper to repay'). Matches; T.",
    "c024": "L02 Section 2 and misconception 3 (out/L02_text.txt:66-67): real value constant exactly when the index is constant. Lab 1 Part B (twin_L02.out) prints real values; recompute_lessons.py: every one of the 12 real values differs from its predecessor (cents and exact). Matches; C with basis.",
    "c025": "twin_L02.out Part B 'identity V_t / V_(t-1) = P_(t-1) / P_t holds exactly for t = 1 to 12: True'; recompute_lessons.py identity True for t=1..12. Matches; C.",
    "c026": "L03 Assumption 1.1 (out/L03_text.txt:18-20): P_t=(1-delta)^min(t,m), P_0=1, 0<=m<=H, 0<delta<1; falls each period on parity, flat after m. Matches; ungraded.",
    "c027": "L03 Definition 2.1 (out/L03_text.txt:31-32): L_t = V_t/N_t, ratio of real debt to net worth. Matches; ungraded.",
    "c028": "L03 Assumption 1.3 (out/L03_text.txt:26): psi_t = phi(L_t - L_0), slope phi>0. Matches; ungraded.",
    "c029": "L03 Definition 2.2 (out/L03_text.txt:33): chain (A1,A2) price fall raises real debt; (A2) lowers net worth one for one; (A3) premium rises with leverage; output falls by f_t = beta psi_t, beta>0 (out/L03_text.txt:26). Matches; ungraded.",
    "c030": "L03 Lemma 3.1 (out/L03_text.txt:36-41): C = N_0 + D, ell(x)=x/(C-x) on [D,C), L_t = ell(V_t) when V_t<C, L_0 = D/N_0, ell strictly increasing. Matches; T.",
    "c031": "L03 Proposition 3.2(a) (out/L03_text.txt:44, proof 48): V_t <= V_m for 0<=t<=H; strictly increasing up to m when m>=1; V_t=V_m after m. Hypotheses Assumptions 1.1-1.3 (out/L03_text.txt:42-43). Matches; T.",
    "c032": "L03 Proposition 3.2(b) (out/L03_text.txt:45): depth(m)=beta phi(ell(V_m)-ell(D)) = beta phi(V_m/(N_0+D-V_m) - D/N_0). recompute_lessons.py: closed form 9.2046% equals the max over t. Matches; T.",
    "c033": "L03 Proposition 3.2(c) (out/L03_text.txt:46, proof 50): maximum first attained at t=m; for m>=1 no earlier period attains it. Matches; T.",
    "c034": "L03 Proposition 3.2(c) and Problem P2 (out/L03_text.txt:109-111, P2 solution): depth(0)=0 since P_t=1, V_t=D, L_t=L_0, premium 0. recompute_lessons.py depth(0)=0. Matches; T.",
    "c035": "L03 Corollary 3.3 (out/L03_text.txt:52-55): 0<=m'<m<=H gives depth(m')<depth(m); Lab economies X (m=12) and Y (m'=4). recompute_lessons.py: X 9.2046% > Y 2.6867%. Matches; T.",
    "c036": "L03 Corollary 3.4 (out/L03_text.txt:56-61): 1<=m'<m<=H; ratio of depths = (ell(V_m)-ell(D))/(ell(V_m')-ell(D)), independent of beta and phi. Matches; T.",
    "c037": "twin_L03.out Part B 'economy X depth 9.20 percent of baseline output, first reached at t = 12'; recompute_lessons.py 9.204597% first at t=12. Matches; C with SIMULATED basis.",
    "c038": "twin_L03.out Part B 'economy Y depth 2.69 percent ... first reached at t = 4'; recompute_lessons.py 2.686713% first at t=4. Matches; C with SIMULATED basis.",
    "c039": "twin_L03.out Part D 'ratio of depths X to Y 3.4260' for beta*phi=1; recompute_lessons.py ratio 3.425970 -> 3.4260 to four decimals. Matches; C.",
    "c040": "L03 Definition 4.1 (out/L03_text.txt:70): lender of last resort = central bank lending against collateral to solvent-but-illiquid institutions; solvent and illiquid definitions match. Matches; ungraded.",
    "c041": "L03 Definition 4.1 (out/L03_text.txt:70): central bank = public institution that issues the monetary base. Matches; ungraded. Lesson-side note: 'monetary base' is not defined in LX1 or in the course concept index (see notes).",
    "c042": "L03 Remark 4.2 (out/L03_text.txt:72): Assumption 1.2 has no lending term; Assumption 1.3 has no facility term; Proposition 3.2 says nothing about a facility. Matches; T.",
    "c043": "L03 Section 6 misconception 1 (out/L03_text.txt:81) and Assumption 1.2 (out/L03_text.txt:22-24): one borrower, no bank, no default; proof of Proposition 3.2 uses none of these events. Matches; T.",
    "c044": "L03 Section 6 misconception 2 (out/L03_text.txt:83): ordering follows from durations 12 and 4 under Assumption 1.1; model cannot say whether holding parity causes a deeper fall. Matches; T.",
    "c045": "L03 Section 6 misconception 3 (out/L03_text.txt:85), Definition 4.1 and Remark 4.2 (out/L03_text.txt:70,72): collateral required, solvent-but-illiquid only, no facility in the model. Matches; T.",
    "c046": "L03 Proposition 3.2(b) and Section 6 misconception 4 (out/L03_text.txt:87): SIMULATED model value at beta=1, no output series; depth scales with beta*phi. Matches; T.",
    "c047": "L03 honest-pending note (out/L03_text.txt:28): no redistributable historical series for gold-standard adherence or output depth is embedded; the lab runs the stylised model and is labelled SIMULATED. Matches; ungraded.",
    "c048": "L04 Definition 1.1 (out/L04_text.txt:18-19): ell_t = ln(x_t/x_(t-1)), change per month, not annualized. Matches; ungraded.",
    "c049": "L04 Definition 1.1 (out/L04_text.txt:18-19): dispersion = sample SD with denominator n-1 about the mean, defined only when n>=2. Matches; ungraded.",
    "c050": "L04 Proposition 1.2 (out/L04_text.txt:21-23): under (A1), sum_{t=a+1}^{b} ell_t = ln(x_b/x_a), b-a terms. recompute_fx.py: telescoping identity True for both windows. Matches; T.",
    "c051": "L04 Remark 1.3 (out/L04_text.txt:25): identity exact in reals; lab checks it in floating point to 1e-12. Lab code SUM_TOLERANCE = 1e-12 (tests/labs/LX1/lab-LX1-L04-1.py, identity line compares against SUM_TOLERANCE). Matches; T.",
    "c052": "L04 Proposition 2.2 (out/L04_text.txt:31-36): (A2) x_t=kappa, kappa>0, n>=2 changes; every log change 0 and dispersion 0. Matches; T.",
    "c053": "L04 Definition 2.1 (out/L04_text.txt:28-29): anchor currency, one foreign currency, parity kappa>0, rate x_t>0; fixed-parity model = model plus (A2) holding the rate at parity. Matches; ungraded.",
    "c054": "twin_L04.out Part B 'months with an exactly zero change: 3: 1976-07, 2012-07, 2019-11'; recompute_fx.py exact-zero months identical; CSV sha256 60572240... equals MANIFEST fx_monthly sha256. Matches; C.",
    "c055": "twin_L04.out Part C window one 'standard deviation 0.027935' over 668 changes; recompute_fx.py sd1 = 0.027935278 (denominator 667). Matches; C.",
    "c056": "twin_L04.out Part C window two 'standard deviation 0.024700' over 321 changes; recompute_fx.py sd2 = 0.0246995014 -> 0.024700. Matches; C.",
    "c057": "twin_L04.out Part D 'ratio of window two to window one ... 0.8842'; recompute_fx.py ratio 0.8841688 -> 0.8842. Matches; C.",
    "c058": "twin_L04.out Part C window two 'largest absolute change 0.096575 at 2008-10 (signed -0.096575)'; recompute_fx.py largest window-two change 2008-10 = -0.0965747. Matches; C.",
    "c059": "L04 Remark 2.3 (out/L04_text.txt:38) says a recorded rate 'need not equal its parity at any month', and misconception 1 (out/L04_text.txt:56) says the GBP column has 665 nonzero changes of 668. The back opens with a universal negative, 'Not in a recorded series', that the page cannot support: the evidence is one column (recompute_fx.py: 665 of 668 nonzero), and nothing on the page excludes a recorded series with zero changes. The back also overstates the lesson's 'need not' as 'is not'. Matches the lesson's example but overreaches its scope.",
    "c060": "L04 Section 4 'The window start is a convention' (out/L04_text.txt:51), Problem E3 (out/L04_text.txt:101-103): code computes two SDs and their difference, no test or cause. twin_L04.out Part D. Matches; C.",
    "c061": "L04 misconception 2 (out/L04_text.txt:60) and Problem M1 (out/L04_text.txt:69): ln 1.1 = 0.0953101798 -> 0.095310; simple change 0.10; difference 0.004690. recompute_fx.py: ln(1.1)=0.09531017980, 0.1 - ln = 0.00468982 -> 0.004690. Matches; T.",
    "c062": "L04 Definition 2.1 and Section 2 (out/L04_text.txt:29-30) and Section 4 'historical arrangement' (out/L04_text.txt:53): the model is not a definition of the historical system; no historical fact stated. Matches; T. 'Pending' is the lesson's own honest-pending state.",
    "c063": "L04 Lab 1 Data paragraph (out/L04_text.txt:42) and Section 4 (out/L04_text.txt:51): window two starts 2000-01 because fx_daily and ust_daily have data; convention; lab does not test other starts. MANIFEST: fx_daily first 2000-01-03, ust_daily first 2000-01-03. Matches; ungraded.",
    "c064": "L04 Lab 1 docstring (out/L04_text.txt:42): data/fx_monthly.csv, G.5/H.10 noon buying rates in New York, GBP column in US dollars per pound. MANIFEST fx_monthly transform: GBP is a direct quote (not inverted). Matches; ungraded.",
    "c065": "twin_L04.out Part D 'difference in standard deviation: -0.003236'; recompute_fx.py diff = -0.0032357765 -> -0.003236 from unrounded SDs (difference of printed values would be -0.003235). Matches; C.",
    "c066": "twin_L02.out Part C: 'periods with a falling price index: 6 of 12', 'rising real value: 6 of 12', 'exactly coincide: True'; recompute_lessons.py falls = rises = [1,5,6,8,9,12]. Matches; C.",
    "c067": "twin_L03.out Part D: ratio 3.4260 for beta*phi = 1/2, 1, 3; recompute_lessons.py ratio 3.425970 in all three. Matches; C.",
    "c068": "twin_L04.out Part B 'exactly zero change: 3' among 668 window-one changes; recompute_fx.py nonzero 665 of 668. Matches; C.",
    "c069": "MANIFEST.json fx_monthly: rows 669, first 1971-01, last 2026-09, retrieved 2026-10-19, transform month-end (each column's last value in the month). recompute_fx.py: 669 rows, 1971-01 to 2026-09. Matches; ungraded.",
    "c070": "MANIFEST.json fx_monthly columns AUD,CAD,CHF,DKK,EUR,GBP,JPY,NOK,NZD,SEK (exchange rates only); L04 lab docstring 'no interest-rate column and no forward-rate column' (out/L04_text.txt:42). Matches; ungraded.",
    "c071": "L03 Assumption 1.2 (out/L03_text.txt:22): N_t = N_0 - (V_t - V_0); the whole rise in real debt falls on net worth. Matches; ungraded.",
    "c072": "L03 Assumption 1.3 (out/L03_text.txt:26-27): depth(m) = max over 0<=t<=H of f_t, f_t = beta psi_t, a fraction of baseline output. Matches; ungraded.",
    "c073": "L02 Section 2 (out/L02_text.txt:27): nominal debt = amount of currency owed at each date, in the currency's own units, not indexed to prices; here D cents. Matches; ungraded. New card in this round.",
    "c074": "L02 Section 2 (out/L02_text.txt:27): price index P_t at date t with base date 0; positive values; P_0 the base value. Matches; ungraded. New card in this round.",
}

rows = []
for n in range(1, 75):
    cid = f"c{n:03d}"
    status = "FAIL" if cid == "c059" else "PASS"
    row = {
        "id": f"card-{cid}",
        "check": "2.7-card-vs-lesson",
        "location": f"course/modules/LX/LX1/cards.json (LX1-{cid})",
        "status": status,
        "evidence": E[cid],
    }
    if status == "FAIL":
        row["fix"] = (
            "Reword the back: 'Not necessarily. Proposition 2.2 gives zero change for the model under (A2) only, and (A2) "
            "describes the model, not a recorded series, which need not equal its parity (Remark 2.3). In the recorded GBP "
            "column, 665 of the 668 window-one changes are nonzero; Lab 1, Part B, prints 3 exactly zero changes among "
            "those 668.' Keep grade C and the basis."
        )
    rows.append(row)


def P(rid, check, location, evidence):
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}


rows.append(
    {
        "id": "card-basis-l04-manifest",
        "check": "plan-section-9-basis-retrieved-date",
        "location": "course/modules/LX/LX1/cards.json (LX1-c054 to c060, c065, c068); plans/LX1-build-plan.md section 9",
        "status": "PASS",
        "evidence": "Every L04 Lab 1 result basis now carries 'MANIFEST retrieved 2026-10-19' (c054, c055, c056, c057, c058, c059, c060, c065, c068); MANIFEST.json fx_monthly retrieved is 2026-10-19 (checked). The round-3 FAIL is fixed. Note: the plan's example text says 'Lab 4'; the L04 lesson labels its lab 'Lab 1' (out/L04_text.txt:111), and the cards follow the lesson, so 'Lab 1' is kept.",
    }
)
rows.append(
    P(
        "card-struct-ids-lessons",
        "2.7-structure",
        "course/modules/LX/LX1/cards.json",
        "Python check: 74 cards, ids LX1-c001..LX1-c074 contiguous with no gaps; every lesson field is L01-L04; each lesson has cards.",
    )
)
rows.append(
    P(
        "card-check-pages",
        "2.7-gate",
        "tools/check_pages.py --unit LX1 (check_cards included)",
        f"{from_out}/check_pages_LX1.out: 'check_pages LX1: PASS', exit 0.",
    )
)
rows.append(
    P(
        "card-numeric-tokens",
        "2.7-numbers-in-lesson",
        "course/modules/LX/LX1/cards.json vs L01-L04 text",
        "Every numeric token on the card faces (for example 400, 9 percent, 6000, 6667, 367, 40000/109, 20000/3, 103/109, 9.20, 2.69, 3.4260, 0.027935, 0.024700, 0.8842, 0.096575, 665, 668, 321, 667, -0.003236, 0.095310, 0.004690, 1976-07, 2012-07, 2019-11, 2008-10, 669, 1e-12) appears in the cited lesson block or in a printed lab line (see out/L0x_text.txt and twin_L0x.out).",
    )
)
rows.append(
    P(
        "card-lab-outputs-verbatim",
        "2.7-lab-expected-vs-output",
        "tests/labs/LX1/lab-LX1-L01-1.py .. lab-LX1-L04-1.py; L01..L04.html",
        f"{from_out}/run_labs_LX1.out: 'run_labs LX1: PASS (7/7)'. compare_labs.py: each lesson's data-run code equals its twin; each expected block equals twin output line-for-line (38, 41, 56, 17 lines). Twins run alone under python -I -W error: exit 0, empty stderr (L04 needs data/fx_monthly.csv in cwd; run from a scratch dir holding a copy, /tmp/lx1d4_scratch). pytest tests/test_labs.py -k LX1: 7 passed.",
    )
)
rows.append(
    P(
        "card-recomputed-numbers",
        "2.7-independent-recompute",
        "ledgers/LX1/scripts/LX1-d-r4/recompute_lessons.py; recompute_fx.py",
        f"{from_out}/../recompute_lessons.py run output: F0=20000/3 (6667); 40000/109=366.97 (367); q=103/109; S_N identity True for N=10,60,200; depth X 9.204597% at t=12, depth Y 2.686713% at t=4, ratio 3.425970 for all products; V_t cents list; falls=rises; ln1.1=0.0953102. recompute_fx.py run on the sha256-matched fx_monthly.csv: sd1 0.027935, sd2 0.024700, diff -0.003236, ratio 0.8842, 665 of 668 nonzero, zeros 1976-07/2012-07/2019-11, largest w2 2008-10 -0.0965747.",
    )
)
rows.append(
    P(
        "card-duplicates",
        "2.7-duplicates",
        "course/modules/LX/LX1/cards.json",
        "Python check: no duplicate ids and no duplicate front strings. Near-overlaps read and judged distinct questions: c005 (Prop 1.4 result) vs c013 (misconception question); c039 (value 3.4260) vs c067 (invariance across products); c021 vs c023 (direction, two questions). Not duplicates.",
    )
)
rows.append(
    P(
        "card-grades-basis",
        "2.7-grades",
        "course/modules/LX/LX1/cards.json; BUILDER_RULES section 7",
        "Grades: T for each proved result (c002-c005, c007, c008, c011-c013, c015-c016, c018-c019, c021-c023, c030-c036, c042-c046, c050-c052, c061-c062); C for each SIMULATED or embedded-data result, each with a basis naming the lab (c009-c010, c024-c025, c037-c039, c054-c060, c065-c068); ungraded for definitions and facts. check_pages.py check_cards passes (grounded rule: non-T grades carry basis or cite).",
    )
)
rows.append(
    P(
        "card-misconception-and-concept-coverage",
        "2.7-coverage",
        "course/modules/LX/LX1/cards.json; L01-L04 Section 6 misconceptions and dfn tags",
        "All 15 misconceptions have a card: L01 (c011,c012,c013), L02 (c016,c023,c024), L03 (c043,c044,c045,c046), L04 (c059,c060,c061,c062). Every dfn concept has a card: speculative-bubble c006, financial-panic c008, gold-standard c014, debt-deflation c020, credit-channel c029, lender-of-last-resort c040, Bretton Woods c062, fundamental value c001, leverage c027, external-finance premium c028, central bank c041, monthly log change c048, dispersion c049, parity/anchor/fixed-parity model c053, nominal debt c073, real value c017.",
    )
)
rows.append(
    P(
        "card-notation",
        "2.7-notation",
        "notation/notation.json (8 program-wide symbols); cards",
        "Registry holds only M4, AP1 symbols (Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q, T). No LX1 card uses any of them. Lesson-local letters (ell in L03 vs ell_t in L04, N, C, L, D, V, P) are defined per lesson and are local by the registry's own rule; no card reuses one with a different meaning inside its lesson.",
    )
)
rows.append(
    P(
        "card-dag-concepts",
        "2.7-dag-concepts",
        "course/modules/LX/LX1/cards.json; check_dag.py --unit LX1",
        f"{from_out}/check_dag_LX1.out: 'check_dag LX1: PASS'. Concepts used on cards (present value, discounting, exponential and logarithm) are in the prerequisite closure (L01 'Uses:' line). Lesson-side note (outside this slice): 'monetary base' appears only in L03 Definition 4.1 and is not defined in LX1 or the course concept index; card c041 repeats the lesson wording.",
    )
)
rows.append(
    P(
        "card-banned-words",
        "2.7-process-words",
        "course/modules/LX/LX1/cards.json; check_pages.py BANNED list",
        "check_pages banned-phrase list passes (check_pages LX1 PASS). Own scan for process words (builder, verif, round, fragment, audit, draft, we, our, TODO): none in cards. 'pending' appears once (c062) and is the lesson's own honest-pending state for the Bretton Woods definition (out/L04_text.txt:30), so it is not a process word.",
    )
)
rows.append(
    {
        "id": "card-scope-words",
        "check": "2.7-scope-words",
        "location": "course/modules/LX/LX1/cards.json (LX1-c059)",
        "status": "FAIL",
        "evidence": "Scope scan of every, all, any, always, only, never, not in, exactly, generally across the 74 card faces. One unsupported universal: c059 back opens 'Not in a recorded series.' (a claim over all recorded rates, from one column). Other scope words are backed by a computation or an explicit hypothesis: 'every date' in c015 (A1), 'exactly' in c024 and c025 (algebra and printed check), 'only' in c011 and c063 (stated benchmark / convention).",
        "fix": "Same reword as card-c059: replace 'Not in a recorded series.' with 'Not necessarily.' and cite Remark 2.3 and the 665-of-668 count.",
    }
)
rows.append(
    P(
        "card-check-dag-projects-gates",
        "2.7-gates",
        "tools/check_dag.py, check_projects.py, page_smoke.py, run_labs.py, ruff, mypy",
        f"{from_out}/check_dag_LX1.out PASS; check_projects_LX1.out PASS; page_smoke_LX1.out: page_smoke LX1 PASS for L01-L04 (run alone); run_labs_LX1.out PASS 7/7; ruff_check.out 'All checks passed!'; ruff_format.out 553 files already formatted; mypy_LX1.out 'Success: no issues found in 385 source files'. Full project gate and graders not run: this slice is card data, and BUILDER_RULES/CLAUDE.md scope the grader job to project slices.",
    )
)
rows.append(
    P(
        "card-registry-offline",
        "2.7-registry",
        "references/references.json; tools/verify_refs.py --offline",
        f"{from_out}/verify_refs_offline_all.out: 'offline integrity: 560 entries, 0 problems', exit 0. Cards cite no registry key (cite is [] on all 74 cards), so no card key needs admission. pytest -o addopts='' tests/test_page_checks.py tests/test_run_labs.py tests/test_fetch_data.py tests/test_docs_figures.py: 126 passed. pytest tests/test_labs.py -k LX1: 7 passed.",
    )
)
rows.append(
    P(
        "card-data-manifest",
        "2.7-data",
        "course/assets/data/market/MANIFEST.json; fx_monthly.csv; tools/fetch_data.py --check",
        f"{from_out}/fetch_data_check.out: 'fetch_data: 3 datasets, 0 problems', exit 0. sha256 of course/assets/data/market/fx_monthly.csv = 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e, equal to MANIFEST fx_monthly sha256. fx_daily and ust_daily first = 2000-01-03 (c063).",
    )
)

fragment = {
    "unit": "LX1",
    "slice": "LX1-d",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-d (ALL cards.json against L01-L04), round 4. Did not build LX1. Round-3 fragment read as context only; its PASS rows were not trusted and every card was re-read against the current lesson text and re-derived.",
    "pin": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba",
    "base": "67a2d13e (round-3 pin; delta read: cards.json c013, c019, c020, c024, c045, c054-c060, c065, c068 reworded; c073, c074 added; L03/L04 lesson text and tests/labs/LX1/lab-LX1-L04-1.py docstring)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE4-LX1-d",
    "scratch": "/tmp/lx1d4_scratch (data/fx_monthly.csv copy, for the L04 twin run only)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice: all 74 cards in course/modules/LX/LX1/cards.json against L01-L04 (text extracts out/L0x_text.txt; read in full, line by line). This is a card slice, not a grader, so no student-error mutant applies; ledgers/LX1/mutants/ was not used.",
        "Delta since round 3 (67a2d13e..9a02b1af) read in full: cards.json hunks, L03.html (Assumption 1.2 cross-reference, Lab 1 purpose sentence, misconception 2 wording, Corollary 3.3 sentence), L04.html (why-it-matters, Definition 2.1, Lab 1 Part A prediction, key-results row, misconception 1 wording) and tests/labs/LX1/lab-LX1-L04-1.py docstring. Every changed card and every changed sentence it depends on was re-derived.",
        "Round-3 FAIL rows: card-c019 is fixed (A2 'not renegotiated'); card-basis-l04-manifest is fixed (retrieved date present). Round-3 card-c059 'generally nonzero' was removed from the lesson and the card, but the new back 'Not in a recorded series.' is the same overreach in universal form, so card-c059 and card-scope-words FAIL.",
        "Lesson-side notes outside this slice (not edited): (1) L03 Definition 4.1 uses 'monetary base' with no definition in LX1 or in the course concept index; (2) plans/LX1-build-plan.md section 9 literally asks for 'Lab 4' in L04 result bases while every lesson names its lab 'Lab 1'; cards follow the lesson.",
        "Not checked: a live verify_refs (network; plain offline run only, which is what the gate uses for this slice); the rendered look of the cards (cards are data, not rendered here); the project pages and graders (other slices); tools/build_site.py --check and render_curriculum (not in this slice's rows); the three project lab twins (other slice).",
        "Run commands on the pin: check_pages, check_dag, check_projects (--unit LX1), run_labs --unit LX1 (7/7), page_smoke --unit LX1 --pages L01 L02 L03 L04, ruff check ., ruff format --check ., mypy --no-incremental, pytest on test_labs -k LX1 and test_page_checks/test_run_labs/test_fetch_data/test_docs_figures, fetch_data --check, verify_refs --offline. All PASS except the card findings above.",
    ],
    "summary": "Round 4 of LX1-d: 74 cards read in full against L01-L04 and the current lab outputs. 73 card rows PASS; card-c059 FAIL (universal 'Not in a recorded series' over a one-column result); card-scope-words FAIL for the same card. Round-3 FAILs c019 and basis-l04-manifest are fixed. Verdict FAIL.",
}

import sys
sys.path.insert(0, "tools")
import ledger  # noqa: E402

problems = ledger.validate(fragment, "LX1-d")
print("validate:", problems)
with open("ledgers/LX1/LX1-d.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "non-PASS", [r["id"] for r in rows if r["status"] != "PASS"])
