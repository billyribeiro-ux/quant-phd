"""Writes ledgers/LX1/LX1-d.json (round 7, LX1 slice d: all cards.json against L01-L04). Every row cites a script under
ledgers/LX1/scripts/LX1-d-r7/ (or a command and its observed output in .../out/) and a lesson location as extracted by
extract_text.py ([N] = HTML source line of the text block)."""
import json, sys

CK = "course/modules/LX/LX1/cards.json"
R = []


def row(i, check, loc, status, ev, fix=""):
    d = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)


CARD = {
 "001": ("L01.html [65]-[67]", "Def 1.2: F_t = sum_k d_(t+k)/(1+r)^k whenever convergent; benchmark, not a forecast ([67]). Front and back match. Ungraded definition."),
 "002": ("L01.html [72]-[74], proof [79]-[84]", "Thm 1.3: F_t = d_1(1+g)^t/(r-g) = d_(t+1)/(r-g); F_0 = d_1/(r-g). Hypotheses A0, A1 as in [58]-[59]. rederive_r7.py: F_0 = 20000/3, rounded 6667. T matches Key results [396]."),
 "003": ("L01.html [74], proof [83]; out/twin_L01.txt", "Thm 1.3: S_N(t)=F_t(1-q^N) exactly for every N>=1. rederive_r7.py: identity True for N=10,60,200 (exact Fractions); Part A prints True for N=10,60,200 ([281]-[284]). T; Lab 1 Part A (exact check) named in basis."),
 "004": ("L01.html proof [84]", "Under A0, 1+g>0 and 1+r>1+g give 0<q<1, so q^N->0. rederive_r7.py: q=103/109, 0<q<1 True. T matches."),
 "005": ("L01.html Prop 1.4 [91], proof [96]", "Hypotheses (A1) d_1>0, 1+g>0; (A2) r>-1, g>=r; conclusion S_N(0)->+inf so Theorem 1.3 does not apply ([91]). Matches. T."),
 "006": ("L01.html Def 2.1 [105]", "B_t = P_t - F_t, a bubble only when B_t>0, measured in cents ([105]); B_t<=0 has no bubble. Matches. Ungraded definition."),
 "007": ("L01.html Prop 2.2 [110]-[114], proof [119]", "Hypotheses (A3) d_1>0; (A4) growth g<g', one discount rate r, r>g, r>g', 1+g>0, 1+g'>0 ([112]); conclusion F_0(g)<F_0(g') and gap split ([114]). rederive_r7.py: 5000 < 20000/3. T."),
 "008": ("L01.html Def 3.1 [289]", "Mechanism only; states no frequency, trigger or size ([289]). Matches. Graded T as the lesson's own Key results row [401] does (basis 'definition, not an empirical claim'); a labelling note only, see notes."),
 "009": ("L01.html [205]; out/twin_L01.txt; lesson [131]-[132]", "Lab 1 Part B prints 'periods with price above fundamental: 9 of 13'. rederive_r7.py with the same seeded wedges: 9 of 13. C, SIMULATED, named in basis."),
 "010": ("L01.html [221]-[222]", "Lab 1 Part C prints '13 of 13' and 'the count changes with the assumed growth rate: True'. rederive_r7.py: 13 of 13 at 1%. C, SIMULATED."),
 "011": ("L01.html Prop 2.2 witness [120]", "d_1=400, r=9%: F_0(1%)=5000, F_0(3%)=20000/3; at P_0=6000 the gaps are +1000 and -2000/3 ([120]). rederive_r7.py: 1000 and -666.67. T."),
 "012": ("L01.html Section 5 [310], misconception 2 [322]", "d_1=400, d_s=0 for s>=2, r=9%: PV 400/1.09 = 40000/109 = 367 cents ([310]). rederive_r7.py: 40000/109 = 366.97 -> 367. Formula needs (A1) ([322]). T."),
 "013": ("L01.html proof of Prop 1.4 [96], misconception 3 [323]", "Under g>=r with d_1>0 each discounted dividend is at least d_1/(1+r); partial sums grow without bound ([323]). Matches. T."),
 "014": ("L02.html Def 1.1 [57]", "Fixes parity kappa>0 grams per unit and convertibility at the parity on demand ([57]). Matches. Ungraded definition."),
 "015": ("L02.html Prop 1.2 [64]-[67], proof [72]", "Hypothesis (A1) parity kept at every date ([65]); conclusion 1/kappa units per gram at every date ([67]). Matches. T."),
 "016": ("L02.html Remark 1.3 [77], proof [72]", "Prop 1.2 says nothing about P_t; (A1) does not involve P_t, so the conclusion holds whatever path P_t follows ([77]). Matches. T."),
 "017": ("L02.html [82]-[83]", "V_t = D P_0 / P_t; D nominal amount in integer cents (A2, [89]); P_0 base value ([82]). Matches. Ungraded definition."),
 "018": ("L02.html Prop 2.1 hypotheses [89]-[90], conclusion (a) [92], proof [97]", "(A2) D positive integer cents, paid in full, not renegotiated; (A3) P_t>0; V_t/V_(t-1) = P_(t-1)/P_t (D P_0 cancels). Matches. T."),
 "019": ("L02.html Prop 2.1(b) [92], proof [98]", "V_H/V_0 = P_0/P_H for every H>=1, by telescoping (a). Matches. T."),
 "020": ("L02.html Def 3.1 [110]", "Debt deflation: the rise in V_t that a fall in P_t implies with D fixed; an arithmetic consequence, not a cause ([110]). Matches. Ungraded definition."),
 "021": ("L02.html Cor 3.2 [115]-[118], proof [123]", "V_t > V_(t-1) iff P_t < P_(t-1), from Prop 2.1(a) ([123]). Hypotheses (A2),(A3) stated ([116]). Matches. T."),
 "022": ("L02.html proof [123], Remark 3.3 [128]", "Factor P_(t-1)/P_t exceeds one in a fall; Cor 3.2 gives only direction, not size ([128]). Matches. T."),
 "023": ("L02.html Cor 3.2 [118], misconception 1 [318]-[319]", "A fall in P_t raises V_t; the same nominal payment is a larger real burden ([319]). Matches. T."),
 "024": ("L02.html [83]; out/twin_L02.txt [207]-[219]; rederive_r7.py", "V_t = D P_0/P_t is constant iff P_t is constant (algebra). Lab 1 Part B prints 13 real values; all 12 consecutive differences nonzero (rederive_r7.py 'consecutive V all differ: True'). C, Part B named in basis. Misconception 3 [327]."),
 "025": ("L02.html lab Part B line 'identity ... holds exactly for t = 1 to 12: True' [220]", "The identity line is printed by Part B ([220]); the basis now cites Part B only, which fixes the round-6 wrong-locator FAIL. rederive_r7.py: exact identity True for t=1..12. C, SIMULATED."),
 "026": ("L03.html Assumption 1.1 [58]-[60]", "P_t=(1-delta)^min(t,m), P_0=1, 0<=m<=H, 0<delta<1; falls on parity, flat after m ([60]). Matches. Definition."),
 "027": ("L03.html Def 2.1 [82]", "L_t = V_t/N_t, real debt over net worth ([82]). Matches. Definition."),
 "028": ("L03.html Assumption 1.3 [72]-[73]", "psi_t = phi(L_t - L_0), slope phi>0 ([72]). Matches. Definition."),
 "029": ("L03.html Def 2.2 [87]", "Chain A1+A2 (debt), A2 (net worth), A3 (premium, output), 'describes the model' ([87]). Matches the five steps. Definition."),
 "030": ("L03.html Lemma 3.1 [96]-[103]", "Lemma now states Assumption 1.2 so that N_0>0 ([96]); ell(x)=x/(C-x) strictly increasing on [D,C); L_t=ell(V_t) when V_t<C; L_0=D/N_0 ([96]). Card hypotheses match. T."),
 "031": ("L03.html Prop 3.2(a) [109], proof [116]; hypothesis [66]", "V_t<=V_m for 0<=t<=H; V_t=D(1-delta)^(-t) for t<=m, strictly increasing when m>=1; V_t=V_m for t>=m ([109]). Hypothesis V_m<N_0+D of Assumption 1.2 ([66]). Matches. T."),
 "032": ("L03.html Prop 3.2(b) [110]; rederive_r7.py", "depth(m)=beta phi(ell(V_m)-ell(D)) = beta phi(V_m/(N_0+D-V_m)-D/N_0) ([110]). rederive_r7.py: closed form equals max_t f_t for m=0..12 (True). T."),
 "033": ("L03.html Prop 3.2(c) [111], proof [118]; rederive_r7.py", "First maximiser at t=m; for m>=1 no earlier period attains it ([118]). rederive_r7.py: first maximiser for m=7 is t=7. Matches. T."),
 "034": ("L03.html Prop 3.2(c) [111], Problem P2 [471]-[473]", "m=0: P_t=1, V_t=D, L_t=L_0, premium 0, depth 0 ([473]). rederive_r7.py: depth(0)=0. T."),
 "035": ("L03.html Cor 3.3 [125], proof [130]; out/twin_L03.txt", "Hypotheses Assumptions 1.1-1.3 with 0<=m'<m<=H ([125]); depth(m')<depth(m) ([125]). Lab output 'X is deeper than Y: True' (lesson [293]); rederive_r7.py depth(4)<depth(12). T."),
 "036": ("L03.html Cor 3.4 [135]-[137], proof [142]; rederive_r7.py", "Hypotheses 1<=m'<m<=H ([135]); ratio = (ell(V_m)-ell(D))/(ell(V_m')-ell(D)), independent of beta and phi ([137]). rederive_r7.py: card RHS equals the depth ratio exactly. T."),
 "037": ("L03.html lesson printed block [291]; out/twin_L03.txt", "Lab 1 Part B prints 'economy X depth 9.20 percent of baseline output, first reached at t = 12'. rederive_r7.py: exact 9.204597 -> 9.20, first at t=12. C, SIMULATED."),
 "038": ("L03.html lesson printed block [292]; out/twin_L03.txt", "Lab 1 Part B prints 'economy Y depth 2.69 percent ... t = 4'. rederive_r7.py: exact 2.686713 -> 2.69, first at t=4. C, SIMULATED."),
 "039": ("L03.html lesson printed block [313]; out/twin_L03.txt", "Lab 1 Part D prints 'phi = 1, beta = 1, product 1: ratio of depths X to Y 3.4260'. rederive_r7.py: 3.425970 -> 3.4260. C, SIMULATED."),
 "040": ("L03.html Def 4.1 [390]", "'A lender of last resort is a central bank that lends against collateral to institutions that are solvent but illiquid' ([390]). Matches. The same paragraph uses the undefined term 'monetary base'; see row card-lesson-term-monetary-base. The card does not use that term."),
 "041": ("L03.html Def 4.1 [390]", "'Illiquid means that the institution cannot meet its payments from its own resources in the time available' ([390]). Verbatim match. Replaces the round-6 card 'what is a central bank?', which repeated the undefined term; that card is gone."),
 "042": ("L03.html Remark 4.2 [395] (rewritten this round, read in full)", "Assumption 1.2 has no lending term; Assumption 1.3 has no term through which a facility changes a solvent borrower's premium; Prop 3.2 says nothing about a facility ([395]). Matches. T."),
 "043": ("L03.html misconception 1 [414] (reworded this round, read); Assumption 1.2 [65]-[66]", "No bank and no failure; Assumption 1.2 excludes default and other balance-sheet change; proof of Prop 3.2 uses none of these events ([414]). Matches. T."),
 "044": ("L03.html misconception 2 [418]", "Ordering follows from durations 12 and 4 under Assumption 1.1; the model cannot say whether holding parity causes a deeper fall ([418]). Matches. T."),
 "045": ("L03.html Def 4.1 [390], Remark 4.2 [395], misconception 3 [422]", "Lender requires collateral and solvent-but-illiquid borrowers; the model has no facility, so no panic result follows ([422]). Matches. T."),
 "046": ("L03.html Prop 3.2(b) [110], misconception 4 [426]; twin docstring", "The 9.20 percent is a SIMULATED model value under Assumption 1.3 with phi=beta=1; no output series enters the lab; depth scales with beta phi ([426]). Matches. T."),
 "047": ("L03.html honest-pending note [76]; manifest_notation_scope_r7.py", "No redistributable historical series for gold-standard adherence or output depth is embedded; the lab is SIMULATED ([76]). MANIFEST datasets are fx_daily, fx_monthly, ust_daily only. Matches. Ungraded fact."),
 "048": ("L04.html Def 1.1 [59]", "ell_t = ln(x_t/x_(t-1)), per month, not annualized ([59]). Matches. Definition."),
 "049": ("L04.html Def 1.1 [59]", "Dispersion = sample sd with denominator n-1 about the mean; defined only for n>=2 ([59]). Matches. Definition."),
 "050": ("L04.html Prop 1.2 [66]-[71]", "(A1) positive rates from a to b, a<b ([66]); sum of ell_t for t=a+1..b = ln(x_b/x_a); b-a terms ([66]). Matches. T."),
 "051": ("L04.html Remark 1.3 [76]; tests/labs/LX1/lab-LX1-L04-1.py SUM_TOLERANCE", "Exact in real numbers; the lab checks it to 1e-12 in floating point ([76]); the twin defines SUM_TOLERANCE = 1e-12. Matches. T."),
 "052": ("L04.html Prop 2.2 [91]-[94], proof [99]-[100]", "Hypotheses (A2), kappa>0, window of n>=2 changes ([92]); every change 0 and dispersion 0 ([94]). Matches. T."),
 "053": ("L04.html Def 2.1 [85]", "Anchor currency in which every rate is quoted; one foreign currency; kappa>0; x_t>0; fixed-parity model adds (A2) ([85]). Matches. Definition."),
 "054": ("L04.html lesson printed block [252]; out/twin_L04.txt", "Lab 1 Part B prints 'months with an exactly zero change: 3: 1976-07, 2012-07, 2019-11'. rederive_r7.py: same three months, 668 changes. C, named in basis."),
 "055": ("L04.html Part C printed block [254]", "Window one: 668 changes, standard deviation 0.027935 ([254]). rederive_r7.py: 0.02793528 -> 0.027935, denominator 667. C."),
 "056": ("L04.html Part C printed block [257]", "Window two: 321 changes, standard deviation 0.024700 ([257]). rederive_r7.py: 0.02469950 -> 0.024700. C."),
 "057": ("L04.html Part D printed block [262]", "Ratio of window-two to window-one standard deviation, four decimals: 0.8842 ([262]). rederive_r7.py: 0.88416881 -> 0.8842. C."),
 "058": ("L04.html Part C printed block [258]", "Window two largest absolute change 0.096575 at 2008-10, signed -0.096575 ([258]). rederive_r7.py: ('2008-10', -0.09657474). C."),
 "059": ("L04.html Prop 2.2 [91], Remark 2.3 [105], misconception 1 [341]", "Zero change is a model result under (A2); a recorded rate 'need not equal its parity at any month' ([105]). Matches. T."),
 "060": ("L04.html Part D [261], misconception 2 [345], E3 [432]; twin code", "Code computes two sample sds and their difference; no test, no interval, no cause ([432]). Matches the twin code (no test statistic). C, named in basis."),
 "061": ("L04.html misconception 3 [349], Problem M1 [368]; rederive_r7.py", "1.00 to 1.10: simple 0.10, ln 1.1 = 0.0953101798 -> 0.095310; difference 0.004690 ([349]). rederive_r7.py: 0.1 - ln 1.1 = 0.00469. T."),
 "062": ("L04.html Def 2.1 [85], [86], misconception 4 [353], Section 4 [332]", "Definition 2.1 is a model class; 'Bretton Woods system: definition pending' ([86]); no historical fact stated ([353], [332]). Matches. T."),
 "063": ("L04.html Section 3 [321], Section 4 [330]; manifest_notation_scope_r7.py", "Window two starts 2000-01 because fx_daily and ust_daily begin 2000-01-03; start is a convention; no test of another start ([321], [330]). MANIFEST first dates 2000-01-03 for both. Matches."),
 "064": ("L04.html Section 3 [59]; twin docstring lines 62-64; MANIFEST", "fx_monthly.csv, Board of Governors G.5/H.10 (noon buying rates in New York), column GBP in US dollars per pound, each value the last value in its month ([59]). MANIFEST citation and transform (GBP not inverted) match. Matches."),
 "065": ("L04.html Part D printed block [261], interpretation [263]; rederive_r7.py", "Difference -0.003236, computed from unrounded standard deviations ([263]). rederive_r7.py: -0.00323578 -> -0.003236. C."),
 "066": ("L02.html Part C printed block [222]-[224]", "'periods with a falling price index: 6 of 12', 'periods with a rising real value: 6 of 12', 'exactly in the periods where the index falls: True'. rederive_r7.py: falls {1,5,6,8,9,12} equal rises. C, SIMULATED."),
 "067": ("L03.html Part D printed block [312]-[314]", "Ratio printed 3.4260 for products 1/2, 1 and 3 ([312]-[314]). rederive_r7.py: exact ratio equal across the three products. C; Cor 3.4 (T) cited."),
 "068": ("L04.html Part B [252] and interpretation [263]; rederive_r7.py", "3 of 668 changes exactly zero, so 665 nonzero ([263]). rederive_r7.py: 665. C."),
 "069": ("L04.html Section 1 [59]; twin docstring line 65; MANIFEST", "669 months, 1971-01 to 2026-09, one value per month ([59]). manifest_notation_scope_r7.py: rows 669, first 1971-01, last 2026-09; rederive_r7.py: months consecutive. Matches. Ungraded data description (see notes)."),
 "070": ("L04.html Section 4 [328]; twin docstring lines 66-67; manifest_notation_scope_r7.py", "Exchange-rate columns only; no interest-rate or forward-rate column ([328]). CSV header contains no rate, forward, yield or interest column; MANIFEST lists ten currencies. Matches."),
 "071": ("L03.html Assumption 1.2 [65]", "N_t = N_0 - (V_t - V_0); the whole rise in real debt falls on net worth ([65]). Matches. Definition."),
 "072": ("L03.html Assumption 1.3 [73]", "depth(m) = max over 0<=t<=H of f_t; f_t = beta psi_t ([73]). Matches. Definition."),
 "073": ("L02.html Section 2 [82]", "Nominal debt: an amount of currency owed at each date, not indexed to prices; 'Here the amount is D cents' ([82]). Matches verbatim. Definition."),
 "074": ("L02.html Section 2 [82]", "Price index P_t at date t with base date 0; positive values; P_0 is the base value ([82]). Matches. Definition."),
 "075": ("L04.html Section 3 [59]; MANIFEST fx_monthly 'retrieved'", "Retrieved 2026-10-19 ([59]); manifest_notation_scope_r7.py: fx_monthly retrieved 2026-10-19. Matches. Ungraded data fact (see notes)."),
 "076": ("L03.html Def 4.1 [390]", "'Solvent means that the institution's assets, valued as the lender values them, cover its liabilities' ([390]). Verbatim match. New card in this round."),
}

for n in range(1, 77):
    k = f"{n:03d}"
    loc, ev = CARD[k]
    row(f"card-c{k}", "2.7 retrieval card", f"{CK} (LX1-c{k}); {loc}", "PASS",
        "Re-derived this round from the current lesson text. " + ev)

row("card-lesson-term-monetary-base", "2.9 define-before-use (lesson sentence behind card LX1-c040/c041)",
    "course/modules/LX/LX1/L03.html:390 (Definition 4.1)", "FAIL",
    "L03.html line 390 reads '<dfn id=\"def-central-bank\">central bank</dfn> is the public institution that issues the monetary base.' "
    "The term 'monetary base' occurs once under course/ (ledgers/LX1/scripts/LX1-d-r7/term_check_r7.py, out/term_check_r7.txt: "
    "1 occurrence, 0 <dfn> definitions). It is used before and without definition (BUILDER_RULES define-before-use). "
    "The round-6 FAIL on card-c041 was closed by replacing that card, not by fixing the lesson, so the lesson defect remains.",
    "Lesson-side, L03.html line 390: define 'monetary base' with a <dfn> at its first use, or delete the clause and define central bank "
    "without it. Then re-run tools/check_pages.py --unit LX1 and ledgers/LX1/scripts/LX1-d-r7/term_check_r7.py, which must report a <dfn>. "
    "Cards LX1-c040/c041/c076 need no change if the wording of the Definition 4.1 sentences they quote is kept.")

row("card-basis-l04-manifest", "2.8 data cited by cards", "cards c054-c058, c060, c065, c068 vs course/assets/data/market/MANIFEST.json", "PASS",
    "manifest_notation_scope_r7.py (out/manifest_notation_scope_r7.txt): fx_monthly retrieved 2026-10-19; every fx_monthly basis names 'MANIFEST retrieved 2026-10-19'. c059 basis is model-only (no fx row). PASS.")
row("card-struct-ids-lessons", "2.7 structure", f"{CK}", "PASS",
    "ledgers/LX1/scripts/LX1-d-r7/cards_struct_r7.py (out/cards_struct_r7.txt): 76 cards; ids are exactly LX1-c001..LX1-c076 and unique; lessons L01 13, L02 15, L03 26, L04 22, all of L01-L04. check_pages --unit LX1 PASS (out/check_pages.txt).")
row("card-numeric-tokens", "2.2 numbers in cards", f"{CK} vs L01-L04 extracted text", "PASS",
    "cards_struct_r7.py: 'number tokens absent from card's own lesson text: []' over all 76 fronts and backs.")
row("card-lab-outputs-verbatim", "2.5 labs printed values", "tests/labs/LX1/lab-LX1-L01-1.py .. lab-LX1-L04-1.py vs lesson printed blocks", "PASS",
    "twin_vs_lesson.py (out/twin_vs_lesson.txt): every line of each twin's standalone output appears verbatim in the lesson text: L01 38/38, L02 41/41, L03 56/56, L04 17/17 lines. run_labs.py --unit LX1: 'run_labs LX1: PASS (7/7)' (out/run_labs_unit.txt, exit 0).")
row("card-twins-standalone", "2.5 labs", "tests/labs/LX1/lab-LX1-L01-1.py .. L04-1.py", "PASS",
    "Each twin run alone with python3 -I -W error in its own scratch directory (L04 with data/fx_monthly.csv only): exit 0 for all four (out/twin_L01.txt .. twin_L04.txt). grep for warn/error/traceback in those outputs: 0 hits.")
row("card-recomputed-numbers", "2.2 / 2.4 re-derived numbers", "ledgers/LX1/scripts/LX1-d-r7/rederive_r7.py (out/rederive_r7.txt)", "PASS",
    "Own code, exact Fractions and Decimal ROUND_HALF_UP, python3 -I: F_0 20000/3 -> 6667; q 103/109; S_N identity True N=10,60,200; seeded 3% count 9 of 13, 1% count 13 of 13; witness 1000 and -666.67; 40000/109 -> 367; L02 identity, falls = rises {1,5,6,8,9,12}, V_12/V_0 = 1.0559093...; L03 depth X 9.204597 -> 9.20 at t=12, Y 2.686713 -> 2.69 at t=4, ratio 3.4259695 -> 3.4260 for all products; L04 668 changes, 3 zeros, sd1 0.02793528, sd2 0.02469950, ratio 0.88416881, difference -0.00323578, max w1 1985-03 0.13584567, max w2 2008-10 -0.09657474.")
row("card-duplicates", "2.7 duplicates", f"{CK}", "PASS",
    "cards_struct_r7.py: duplicate fronts [] and duplicate backs [] (case-insensitive, stripped), 76 unique ids.")
row("card-grades-basis", "2.3 grades", f"{CK}; BLUEPRINT.md §3; BUILDER_RULES.md §7", "PASS",
    "cards_struct_r7.py: grades T 34, C 17, ungraded 25 (sums to 76). Every T or C card has a basis; no ungraded card has one. Each C card names a SIMULATED lab output or an fx_monthly lab output; each T card names its proof, proposition, remark, problem or definition. Grades agree with the lesson Key results tables (L01 [396]-[401]; L02 [443]-[446]; L03 [542]-[546]; L04 [469]-[472]).")
row("card-misconception-and-concept-coverage", "2.7 coverage (BUILDER_RULES §7: definitions, theorems, key formulas, key results, misconceptions)", f"{CK}; L01-L04 misconception sections", "PASS",
    "Misconceptions: L01 [321]-[323] -> c011, c012, c013; L02 [318]-[327] -> c023, c016, c024; L03 [413]-[426] -> c043, c044, c045, c046; L04 [340]-[353] -> c059, c060, c061, c062. Definitions and key results: L01 c001, c002-c005, c006, c007, c008, c009, c010; L02 c014-c022, c025, c066, c073, c074; L03 c026-c036, c037-c039, c040-c042, c067, c071, c072, c076; L04 c048-c053, c050, c054-c058, c065, c068, c069, c070, c075. No missing definition or key result found.")
row("card-notation", "2.4 notation", "notation/notation.json (8 registered symbols); cards; L01-L04", "PASS",
    "manifest_notation_scope_r7.py (2) and (2b): no registered symbol (\\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) appears in cards or lessons; T appears only as a grade label '(T)' in basis strings, 0 math-like uses of T. Lesson-local letters (P_t, N_t, ell, H, m, N) are defined in their lessons, as notation.json 'about' allows.")
row("card-dag-concepts", "2.9 DAG", f"{CK}; tools/check_dag.py --unit LX1", "PASS",
    "check_dag.py --unit LX1: 'check_dag LX1: PASS' (out/check_dag.txt, exit 0). Cards carry no concept links and name no concept outside the unit's closure.")
row("card-banned-words", "2.9 banned process words", f"{CK}; tools/check_pages.py", "PASS",
    "cards_struct_r7.py: process-word hits in front/back/basis: []. check_pages --unit LX1: PASS.")
row("card-scope-words", "2.4 / 2.7 scope words", f"{CK}; manifest_notation_scope_r7.py (scope list)", "PASS",
    "50 scope-word occurrences (only, all, every, any, same, exactly, whenever, never) read in context. Universals are proved on the page (c003 'for every N'; c007 'every price'; c015 'every date'; c019 'every H'; c034 'every period'; c052 'every change') or computed (c025 all 12 dates; c054 all 668 changes). 'only' qualifiers are definitional or the lesson's own words (c011 from [243]; c022 from [128]; c008 from [289]). 'no failure occurs' (c043) follows from Assumption 1.2 ([65]). No unsupported scope word found.")
row("card-registry-offline", "2.1 registry", "references/references.json; tools/verify_refs.py --offline", "PASS",
    "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline.txt). All 76 cards have cite [] (cards_struct_r7.py). The registry is unchanged since the round-6 pin (git diff 4bd8cb94..06994db lists no references file).")
row("card-data-manifest", "2.8 data", "course/assets/data/market/MANIFEST.json; fx_monthly.csv; fx_daily; ust_daily", "PASS",
    "manifest_notation_scope_r7.py (out/manifest_notation_scope_r7.txt): MANIFEST datasets fx_daily, fx_monthly, ust_daily only (so c047 holds); fx_monthly rows 669, first 1971-01, last 2026-09, retrieved 2026-10-19; fx_daily and ust_daily first 2000-01-03; fx_monthly columns are ten currencies; csv header has no interest or forward column; transform inverts CAD, CHF, DKK, JPY, NOK, SEK only (GBP direct quote). The licence_url quote is outside this slice (see notes).")
row("card-gates-ruff-mypy-pytest", "gates", "tests/labs/LX1; tests/test_labs.py; tests/test_page_checks.py", "PASS",
    "ruff check tests/labs/LX1: 'All checks passed!' (out/ruff_check_labs.txt, exit 0); ruff format --check: '7 files already formatted' (exit 0); mypy --no-incremental tests/labs/LX1: 'Success: no issues found in 7 source files' (exit 0); pytest tests/test_labs.py: all passed (exit 0); pytest tests/test_page_checks.py: all passed (41 dots, exit 0). The tests -k 'card' filter collects nothing (exit 5), so the whole file was run.")
row("card-page-smoke-lessons", "2.9 page smoke", "tools/page_smoke.py --unit LX1 --pages L01 L02 L03 L04 --skip-sweep", "PASS",
    "Run alone: L01, L02, L03, L04 each 'PASS' including each lab; 'page_smoke LX1: PASS', exit 0 (out/page_smoke_L01_L04.txt).")
row("card-check-pages-dag-projects", "2.9 structure gates", "tools/check_pages.py, check_dag.py, check_projects.py --unit LX1", "PASS",
    "check_pages LX1: PASS; check_dag LX1: PASS; check_projects LX1: PASS (out/check_pages.txt, out/check_dag.txt, out/check_projects.txt; each exit 0).")
row("card-delta-readthrough", "2.7 delta since round-6 pin", "git diff 4bd8cb94 06994db -- cards.json, L03.html, L04.html", "PASS",
    "Every hunk read. cards.json: c025 basis (Part B only); c040 back shortened and c041 replaced (central bank -> illiquid); c064 back expanded; new c076 (solvent). L03.html: why-it-matters [31]; Lemma 3.1 [96]; Remark 4.2 [395]; canon-breaks functional-form bullet [404]; misconception 1 [414]; L03q7 explanation [605]. L04.html: Section 3 window paragraph [321]; Section 4 'Exchange rates only' bullet [328]. Cards whose subject changed (c025, c030, c040, c041, c042, c043, c064, c070, c076) were re-verified from the new text; all other cards are byte-identical to the round-6 pin. project.html and lab-LX1-project-3.py changed but no card cites them (grep of cards.json).")
row("card-verify-cards-lessons-subject", "2.7 cards agree with CURRENT lesson text", "course/modules/LX/LX1/L01.html .. L04.html", "PASS",
    "Every card re-derived from the current extracted text (extract_text.py -> /tmp/lx1d7_scratch; line numbers [N] are HTML source lines). L01.html and L02.html are byte-identical to the round-6 pin (git diff --stat 4bd8cb94 06994db lists only L03, L04, cards.json, project.html, lab-LX1-project-3.py). No PASS row was carried forward from round 6; all 76 card rows were re-verified in this round.")

notes = [
    "Verdict FAIL: one non-PASS row, card-lesson-term-monetary-base. It is a lesson sentence (L03.html line 390) that the card set paraphrases. The round-6 card-c041 FAIL is closed (the card was replaced), but the undefined term remains in the lesson.",
    "card-c025 (round-6 FAIL, wrong locator) is closed: the basis now names Lab 1 Part B, where the identity line is printed.",
    "card-c041 (round-6 FAIL) is closed by replacement: the old card repeated the undefined term; the new card LX1-c041 is the illiquid definition, verbatim from L03.html line 390.",
    "Out of this slice: project.html and tests/labs/LX1/lab-LX1-project-3.py changed since the round-6 pin; no card cites the project page. Not verified here.",
    "Out of this slice: the licence_url quote for fx_monthly, fx_daily and ust_daily (rule 2.8) and the rebuild of fx_monthly.csv sha256 from the live feed. Not checked in this slice; the data slice owns them. Plain curl was not used.",
    "Judgment, not a defect: LX1-c008 is graded T although it is a definition; the lesson's own Key results row [401] grades it the same way with the basis 'definition, not an empirical claim'.",
    "Judgment, not a defect: LX1-c069 and LX1-c075 are data-description cards (month span, retrieval date) and sit near BUILDER_RULES section 7's 'not trivia' rule. They are kept because the lessons quote those facts and the pages depend on the retrieval date.",
    "Judgment, not a defect: several cards state a list (c002 proof output, c029 five-step chain, c053 Definition 2.1 contents). They test one definition or result each, not single atomic facts.",
    "Not run: run_graders and mutate_graders (LX1 has no autograded project in this slice); the project mutant requirement does not apply to cards. No student-error mutants were written for this slice.",
    "Not run: live verify_refs (only --offline); Chromium page_smoke sweep (--skip-sweep used, as the procedure allows for the lesson pages).",
]

frag = {
    "unit": "LX1",
    "slice": "LX1-d",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-d (ALL cards.json against L01-L04), round 7. Did not build LX1. Round-6 fragment read as context only; no PASS row carried forward; every card re-derived from the current lesson text.",
    "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "base": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (round-6 pin)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-LX1-d",
    "scratch": "/tmp/lx1d7_scratch (extract_text.py output); /tmp/lx1d7_run (twin runs)",
    "scripts": "ledgers/LX1/scripts/LX1-d-r7/",
    "verified_at": "2026-11-04T22:42:33+00:00",
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in R) else "PASS",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": ("Round 7 of LX1-d: 76 cards and 21 gate/structure rows (97 rows). 96 PASS, 1 FAIL: card-lesson-term-monetary-base "
                "(L03.html line 390 uses 'monetary base' with no definition; lesson-side fix). Every card re-derived; no round-6 PASS carried forward. "
                "Round-6 card-c025 and card-c041 FAILs are closed. Verdict FAIL."),
}
out = sys.argv[1]
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(out, "a", encoding="utf-8").write("\n")
print("rows", len(R), "PASS", sum(r["status"] == "PASS" for r in R), "non-PASS", [r["id"] for r in R if r["status"] != "PASS"])
