"""Round 8 fragment writer for LX1-d. Every card row cites the lesson source lines ([N] = HTML source line of L0x.html,
from out/L0x.txt) and the command output that re-derived it. Writes ledgers/LX1/LX1-d.json only."""
import json, sys

BASE = sys.argv[1]
C = "course/modules/LX/LX1/cards.json"
CARD = {
 "LX1-c001": ("L01", "[65]-[67]", "Def 1.2 F_t = sum_k d_(t+k)/(1+r)^k whenever convergent; benchmark, not a forecast ([67]). Front and back match. Ungraded definition."),
 "LX1-c002": ("L01", "[72]-[74], proof [79]-[84], hypotheses [58]-[59]", "Thm 1.3: F_t = d_1(1+g)^t/(r-g) = d_(t+1)/(r-g); F_0 = d_1/(r-g); A0 and A1 as stated. rederive_r8.py: F_0 = 20000/3, rounds to 6667 (Part A [244]). T."),
 "LX1-c003": ("L01", "[74], proof [83]; Part A [246]-[248]", "S_N(t) = F_t(1-q^N) exactly for every N>=1 ([74]). rederive_r8.py: identity True for N=1,10,60,200 (exact Fractions); Part A prints True for N=10,60,200. T; the lab check is at t=0 only, and the basis says so."),
 "LX1-c004": ("L01", "[84]", "Under A0, 1+r>1+g>0 gives 0<q<1, so q^N->0. rederive_r8.py: q = 103/109, 0<q<1 True. T."),
 "LX1-c005": ("L01", "[91], proof [96]", "Hypotheses (A1) d_1>0, 1+g>0; (A2) r>-1, g>=r; conclusion S_N(0)->+inf, so Theorem 1.3 does not apply ([91]). T."),
 "LX1-c006": ("L01", "[105]", "B_t = P_t - F_t counted as a bubble only when B_t>0, measured in cents; B_t<=0 has no bubble ([105]). Ungraded definition."),
 "LX1-c007": ("L01", "[111]-[114], proof [119]", "Hypotheses (A3) d_1>0 and (A4) g<g', one r with r>g, r>g', 1+g>0, 1+g'>0 ([112]); conclusion F_0(g)<F_0(g') and the gap split ([114]). rederive_r8.py: 5000 < 6666.67. T."),
 "LX1-c008": ("L01", "[289]; Key results [401]", "Mechanism only: sudden collective demand to convert claims; no frequency, trigger or size ([289]). Graded T as the lesson's own Key results row [401] grades it (judgment, see notes)."),
 "LX1-c009": ("L01", "[264] Part B printed line; twin output line 21", "Part B prints 'periods with price above fundamental: 9 of 13'. rederive_r8.py with the lab's seed and wedge rule: 9 of 13. C, SIMULATED, named in basis."),
 "LX1-c010": ("L01", "[280]-[281] Part C printed lines; twin output lines 37-38", "Part C prints '13 of 13' and 'the count changes with the assumed growth rate: True'. rederive_r8.py: 13 of 13 at 1%. C, SIMULATED."),
 "LX1-c011": ("L01", "[120] witness; [322]", "d_1=400, r=9%: F_0(1%)=5000, F_0(3%)=20000/3; at P_0=6000 the gaps are +1000 and -2000/3 ([120]). rederive_r8.py: 1000 and -666.67. T."),
 "LX1-c012": ("L01", "[310] Section 5; misconception 2 [322]", "d_1=400, d_s=0 for s>=2, r=9%: PV 400/1.09 = 40000/109 = 366.97, rounds to 367 ([310]). rederive_r8.py: 367. (A1) needed ([322]). T."),
 "LX1-c013": ("L01", "[96] proof; misconception 3 [323]; Prop 1.4 [91]", "Under (A1) d_1>0, 1+g>0 and (A2) r>-1, g>=r: each discounted dividend >= d_1/(1+r), so partial sums grow without bound ([96], [323]). T."),
 "LX1-c014": ("L02", "[57] Definition 1.1", "Definition 1.1 fixes the parity kappa>0, the quantity of gold in grams for one unit of the currency ([57]). Ungraded definition. Convertibility is split to c078, so this card tests one fact."),
 "LX1-c015": ("L02", "[65]-[67] Prop 1.2; proof [72]", "(A1) issuer keeps the parity at every date; conclusion one gram costs 1/kappa at every date ([65]-[67]). T."),
 "LX1-c016": ("L02", "[77] Remark 1.3; proof [72]; price index [82]", "Prop 1.2 is one price; (A1) does not involve P_t of Section 2, so its conclusion holds whatever path P_t follows ([77]). T."),
 "LX1-c017": ("L02", "[82]-[83] Section 2", "V_t = D P_0 / P_t, D nominal amount in integer cents, P_0 base value ([83]). Ungraded definition."),
 "LX1-c018": ("L02", "[89]-[90] (A2),(A3); [97] proof (a)", "V_t/V_(t-1) = P_(t-1)/P_t; the factor D P_0 cancels ([97]). T."),
 "LX1-c019": ("L02", "[92] conclusion (b); [98] proof", "V_H/V_0 = P_0/P_H for every H>=1 under (A2),(A3); one-period ratios telescope ([98]). T."),
 "LX1-c020": ("L02", "[110] Definition 3.1", "Debt deflation: the rise in V_t implied by a fall in P_t with D fixed; arithmetic consequence, not a claim about cause ([110]). Ungraded definition."),
 "LX1-c021": ("L02", "[116] hypotheses; [118] Corollary 3.2; proof [123]", "For t>=1, V_t > V_(t-1) iff P_t < P_(t-1) ([118]). Hypotheses (A2),(A3) of Prop 2.1 ([116]). T."),
 "LX1-c022": ("L02", "[128] Remark 3.3; [97] Prop 2.1(a)", "Real value multiplied by P_(t-1)/P_t, which exceeds 1 in a fall; Corollary 3.2 gives direction only ([128]). T."),
 "LX1-c023": ("L02", "[118] Corollary 3.2; misconception 1 [318]-[319]", "Fall in P_t raises V_t, so the same nominal payment is a larger real burden ([319]). T."),
 "LX1-c024": ("L02", "[327] misconception 3; Part B printed lines [274]-[286]", "V_t constant iff P_t constant (derivation from V_t=DP_0/P_t, [327]). Part B printed values: each of the 12 changes t=1..12 differs from its predecessor (checked by reading the printed list). C, SIMULATED."),
 "LX1-c025": ("L02", "Part B [287]; twin output line 29", "Part B prints 'identity V_t / V_(t-1) = P_(t-1) / P_t holds exactly for t = 1 to 12: True'. C, SIMULATED, one seeded path."),
 "LX1-c026": ("L03", "[58]-[60] Assumption 1.1", "P_t = (1-delta)^min(t,m), P_0=1, 0<delta<1, 0<=m<=H; flat after m ([59]-[60]). Ungraded definition."),
 "LX1-c027": ("L03", "[82] Definition 2.1", "Leverage L_t = V_t/N_t, real debt over net worth ([82]). Ungraded definition."),
 "LX1-c028": ("L03", "[72] Assumption 1.3", "psi_t = phi (L_t - L_0), slope phi>0 ([72]). Ungraded definition."),
 "LX1-c029": ("L03", "[87] Definition 2.2; [71]-[72] Assumption 1.3", "The chain: price fall raises V_t (A1,A2); rise lowers N_t one for one (A2); higher leverage raises premium (A3); output falls by f_t = beta psi_t (A3). Describes the model only ([87]). Ungraded definition."),
 "LX1-c030": ("L03", "[95]-[103] Lemma 3.1; proof [101]-[103]", "L_t = ell(V_t) whenever V_t<C; L_0 = D/N_0; ell strictly increasing on [D,C) ([95], [102]). T."),
 "LX1-c031": ("L03", "[108]-[109] Prop 3.2(a); proof [116]", "V_t <= V_m for 0<=t<=H; strictly increasing for t<=m when m>=1; V_t=V_m for t>=m ([109]). T."),
 "LX1-c032": ("L03", "[110] Prop 3.2(b); proof [117]", "depth(m) = beta phi (ell(V_m)-ell(D)) = beta phi (V_m/(N_0+D-V_m) - D/N_0) ([110]). T."),
 "LX1-c033": ("L03", "[111] Prop 3.2(c); proof [118]", "Maximum first attained at t=m; when m>=1 no earlier period attains it ([118]). T."),
 "LX1-c034": ("L03", "[111] 'In particular depth(0)=0'; P2 [471]-[473]", "m=0: V_t=D, L_t=L_0, premium 0 in every period ([473]). T."),
 "LX1-c035": ("L03", "[125] Corollary 3.3; proof [130]; Part B [361]", "depth(m') < depth(m) for 0<=m'<m<=H ([125]); X (m=12) deeper than Y (m'=4). Part B prints 'X is deeper than Y: True' (twin output line 35). T; SIMULATED reading named."),
 "LX1-c036": ("L03", "[135]-[137] Corollary 3.4; proof [142]", "Ratio = (ell(V_m)-ell(D))/(ell(V_m')-ell(D)) for 1<=m'<m<=H; independent of beta, phi ([136]-[137]). T."),
 "LX1-c037": ("L03", "Part B [359]", "Part B prints 'economy X depth 9.20 percent of baseline output, first reached at t = 12'. rederive_r8.py exact: 9.204597. C, SIMULATED model value."),
 "LX1-c038": ("L03", "Part B [360]", "Part B prints 'economy Y depth 2.69 percent ... first reached at t = 4'. rederive_r8.py exact: 2.686713. C, SIMULATED model value."),
 "LX1-c039": ("L03", "Part D [380]-[382]", "Part D prints ratio 3.4260 for each product. rederive_r8.py exact: 3.425970 -> 3.4260. C; basis names Corollary 3.4."),
 "LX1-c040": ("L03", "[390] Definition 4.1", "A lender of last resort is a central bank that lends against collateral to institutions that are solvent but illiquid ([390]). Ungraded definition."),
 "LX1-c041": ("L03", "[390] Definition 4.1", "Illiquid: cannot meet payments from its own resources in the time available ([390])."),
 "LX1-c042": ("L03", "[395] Remark 4.2; [65]-[66] Assumption 1.2; [72] Assumption 1.3", "Neither assumption has a lending term; Prop 3.2 says nothing about a facility ([395]). T."),
 "LX1-c043": ("L03", "[413]-[414] misconception 1; [65] Assumption 1.2", "No bank and no failure in the model; Assumption 1.2 excludes default and balance-sheet change; proof of Prop 3.2 uses none of these ([414]). T."),
 "LX1-c044": ("L03", "[418] misconception 2", "Ordering follows from parity durations 12 and 4 assigned under Assumption 1.1; model cannot say whether holding parity causes a deeper fall ([418]). T."),
 "LX1-c045": ("L03", "[421]-[422] misconception 3; [390]; [395]", "Definition 4.1 requires collateral and solvent-but-illiquid borrowers; no lending facility in the model ([422]). T."),
 "LX1-c046": ("L03", "[425]-[426] misconception 4; [110] Prop 3.2(b)", "Depth is a SIMULATED model value, no output series enters the lab; changing beta changes it in proportion ([426]). T."),
 "LX1-c047": ("L03", "[76] honest-pending note; [149] SIMULATED label; docstring [152]-[155]", "No redistributable historical series for gold-standard adherence or output depth is embedded; lab runs the stylised model and is labelled SIMULATED ([76]). MANIFEST lists only fx_daily, fx_monthly, ust_daily (course/assets/data/market/MANIFEST.json ids at lines 5, 32, 63). Ungraded."),
 "LX1-c048": ("L04", "[59] Definition 1.1", "ell_t = ln(x_t/x_(t-1)), per month, not annualised ([59]). Ungraded definition."),
 "LX1-c049": ("L04", "[59] Definition 1.1", "Sample standard deviation with denominator n-1; defined only when n>=2 ([59]). Ungraded definition."),
 "LX1-c050": ("L04", "[66] Prop 1.2; proof [71]", "Sum of ell_t for t=a+1..b equals ln(x_b/x_a); b-a terms, under (A1) ([66]). T."),
 "LX1-c051": ("L04", "[76] Remark 1.3; L04 code [161] SUM_TOLERANCE = 1e-12", "Identity is exact in reals; the lab checks it in floating point to 10^-12 ([76]), matching SUM_TOLERANCE = 1e-12 at [161]. T."),
 "LX1-c052": ("L04", "[92]-[94] Prop 2.2; proof [99]-[100]", "(A2) with kappa>0, n>=2: every change is 0 and dispersion is 0 ([94]). T."),
 "LX1-c053": ("L04", "[85] Definition 2.1", "Anchor currency, one foreign currency, parity kappa>0, market rate x_t>0; A2 holds the rate at parity ([85]). Ungraded definition."),
 "LX1-c054": ("L04", "Part B [307]; twin output line 7", "Part B prints 'months with an exactly zero change: 3: 1976-07, 2012-07, 2019-11'. rederive_fx_r8.py on course/assets/data/market/fx_monthly.csv (sha256 matches MANIFEST line 42): same three months. C, a lab on the embedded GBP column (not SIMULATED)."),
 "LX1-c055": ("L04", "Part C [309]; twin output line 9", "Window one dispersion 0.027935 from 668 changes, denominator 667. rederive_fx_r8.py: 0.0279352779 -> 0.027935. C."),
 "LX1-c056": ("L04", "Part C [312]; twin output line 12", "Window two dispersion 0.024700 from 321 changes. rederive_fx_r8.py: 0.0246995014 -> 0.024700 (n=321). C."),
 "LX1-c057": ("L04", "Part D [317]; twin output line 17", "Ratio window two / window one = 0.8842. rederive_fx_r8.py: 0.8841688 -> 0.8842. C."),
 "LX1-c058": ("L04", "Part C [313]; twin output line 13", "Largest absolute change in window two 0.096575 at 2008-10, signed -0.096575. rederive_fx_r8.py: -0.0965747 at 2008-10. C."),
 "LX1-c059": ("L04", "[105] Remark 2.3; [341] misconception 1; Prop 2.2 [94]", "Zero change in the model under (A2); (A2) describes the model, not a recorded rate ([105]). T."),
 "LX1-c060": ("L04", "[344]-[345] misconception 2; [330] window start; E3 [432]", "Lab computes two SDs and their difference; no test, no cause ([345], [432]). C, names Lab 1 Part D."),
 "LX1-c061": ("L04", "[349] misconception 3; M1 [368]", "1.00->1.10: simple 0.10, log ln 1.1 = 0.095310, difference 0.004690 ([349]). rederive_r8.py: ln 1.1 = 0.0953101798, difference 0.0046898. T."),
 "LX1-c062": ("L04", "[81], [86], [332], [353] misconception 4", "Definition 2.1 is a model class; no historical fact about parities, participants or end ([332]). T."),
 "LX1-c063": ("L04", "[127]-[129] window two start; [321]; [330]", "Start is the first month where fx_daily and ust_daily have data, both starting 2000-01-03 (MANIFEST lines 27 and 81); convention, no test ([330]). Ungraded."),
 "LX1-c064": ("L04", "Lab docstring [117]-[120]; MANIFEST fx_monthly citation (line 39)", "Data is fx_monthly.csv, GBP column, USD per pound; last value in month ([119]); citation matches MANIFEST line 39. Ungraded."),
 "LX1-c065": ("L04", "Part D [316]; [318] 'computed from the unrounded standard deviations'", "Difference -0.003236 from unrounded SDs; rederive_fx_r8.py: -0.0032357765 -> -0.003236. C."),
 "LX1-c066": ("L02", "Part C [289]-[291]; twin output lines 31-33", "Part C prints 6 of 12 falling, 6 of 12 rising, and 'rises exactly in the periods where the index falls: True'. C, SIMULATED, one seeded path."),
 "LX1-c067": ("L03", "Part D [380]-[382]; Corollary 3.4 [135]", "Ratio 3.4260 for products 1/2, 1, 3. C; basis names Part D and Corollary 3.4."),
 "LX1-c068": ("L04", "Part B [307]; E1 [418]", "Window one has 668 changes and 3 exact zeros, so 665 nonzero (E1 [418]; rederive_fx_r8.py: 665). C."),
 "LX1-c069": ("L04", "Docstring [120]; MANIFEST fx_monthly rows (line 44) and first (line 58)", "669 months, 1971-01 to 2026-09 (docstring [120]; rederive_fx_r8.py rows 669). Ungraded."),
 "LX1-c070": ("L04", "Docstring [122]; [321]", "Exchange-rate columns only: no interest-rate column and no forward-rate column ([122]). Ungraded."),
 "LX1-c071": ("L03", "[65] Assumption 1.2; [166] docstring N_t", "N_t = N_0 - (V_t - V_0); whole rise in real debt falls on net worth ([65]). Ungraded."),
 "LX1-c072": ("L03", "[72]-[73] Assumption 1.3", "depth(m) = max over 0<=t<=H of f_t, f_t = beta psi_t ([73]). Ungraded."),
 "LX1-c073": ("L02", "[82] Section 2", "Nominal debt: owed at each date in the currency's units, not indexed; amount D cents ([82]). Ungraded."),
 "LX1-c074": ("L02", "[82] Section 2", "P_t at date t with base date 0; positive values; P_0 is the base value ([82]). Ungraded."),
 "LX1-c075": ("L04", "MANIFEST fx_monthly 'retrieved' (line 40); [114]; [566]-[568]", "retrieved 2026-10-19 at course/assets/data/market/MANIFEST.json line 40. Ungraded."),
 "LX1-c076": ("L03", "[390] Definition 4.1", "Solvent: assets, valued as the lender values them, cover liabilities ([390]). Ungraded definition."),
 "LX1-c077": ("L03", "[390] Definition 4.1 (verbatim)", "Back repeats the lesson sentence verbatim; its term 'monetary base' is used with no definition and no <dfn> anywhere under course/ (out/term_check_r8.txt). See the FAIL row card-lesson-term-monetary-base. A retrieval card cannot be learned from an undefined term."),
 "LX1-c078": ("L02", "[57] Definition 1.1", "Convertibility at the parity: the issuer stands ready to buy and sell gold at the parity on demand ([57]). Ungraded definition."),
}

rows = []
for cid in sorted(CARD):
    lesson, loc, ev = CARD[cid]
    status = "PASS"
    if cid == "LX1-c077":
        status = "FAIL"
    row = {"id": f"card-{cid[4:]}", "check": f"cards.json entry {cid} against {lesson} text",
           "location": f"{C} ({cid}); {lesson}.html {loc}", "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = ("Define 'monetary base' at its first use with a <dfn> in L03.html (or rewrite the sentence in L03.html line 390 "
                      "using only defined terms), rebuild the page, and make card LX1-c077 cite that defined term or drop the card. "
                      "c040 and c076 already test the same definition.")
        row["evidence"] = ev + " Not PASS: the card carries an undefined term."
    rows.append(row)

GATE = [
 ("card-lesson-term-monetary-base", "2.9 define-before-use (lesson sentence behind cards c040, c076, c077)",
  "course/modules/LX/LX1/L03.html:390 (Definition 4.1)", "FAIL",
  "L03.html line 390 reads '<dfn id=\"def-central-bank\">central bank</dfn> is the public institution that issues the monetary base.' "
  "Round-8 grep (out/term_check_r8.txt): 'monetary base' occurs at L03.html:390 and cards.json:640 only; zero <dfn> definitions; "
  "course/assets/data/glossary.json has no monetary-base entry. Unchanged since round 7, which recorded the same FAIL.",
  "Define 'monetary base' at first use with a <dfn> in L03.html, or rewrite line 390 without it; rebuild the page; re-run check_pages --unit LX1."),
 ("card-basis-l04-manifest", "2.8 data cited by cards",
  "cards c054-c058, c060, c064, c065, c068, c069, c075 vs course/assets/data/market/MANIFEST.json",
  "PASS",
  "MANIFEST fx_monthly: 'retrieved': '2026-10-19' (line 40), 'rows': 669 (line 44), first 1971-01 (line 58), sha256 60572240...8bffe3e (line 42). shasum -a 256 fx_monthly.csv matches line 42. fx_daily and ust_daily first 2000-01-03 (lines 27, 81). Every fx_monthly card basis names Lab 1 with 'MANIFEST retrieved 2026-10-19'. Note: ust_daily retrieved 2026-10-20 (line 71), not cited by any card."),
 ("card-struct-ids-lessons", "2.7 structure",
  "course/modules/LX/LX1/cards.json", "PASS",
  "out/cards_struct_r8.txt: 78 cards; ids exactly LX1-c001..LX1-c078, unique; lessons L01 13, L02 16, L03 27, L04 22 (all four lessons). tools/check_pages.py --unit LX1: 'check_pages LX1: PASS' (out/check_pages_LX1.out)."),
 ("card-numeric-tokens", "2.2 numbers in cards",
  "course/modules/LX/LX1/cards.json vs L01-L04 extracted text", "PASS",
  "ledgers/LX1/scripts/LX1-d-r8/number_tokens_r8.py (out/number_tokens_r8.out): 'tokens checked over 78 cards; absent from own lesson text: []'."),
 ("card-lab-outputs-verbatim", "2.5 labs printed values",
  "tests/labs/LX1/lab-LX1-L01-1.py .. L04-1.py vs lesson printed blocks", "PASS",
  "twin_vs_lesson_r8.py (out/twin_vs_lesson_r8.out): L01 38/38, L02 41/41, L03 56/56, L04 17/17 twin output lines verbatim in lesson text (whitespace-normalised). run_labs.py --unit LX1: 'run_labs LX1: PASS (7/7)' (out/run_labs_LX1.out, exit 0)."),
 ("card-twins-standalone", "2.5 labs run alone",
  "tests/labs/LX1/lab-LX1-L01-1.py .. L04-1.py", "PASS",
  "Each twin run alone: python3 -I -W error in a scratch dir (L04 with data/fx_monthly.csv only), exit 0 for all four; outputs in out/twin_lab-LX1-L0x-1.out. Lab-level mutation testing is not applied to lab twins (BLUEPRINT/verifier ruling)."),
 ("card-recomputed-numbers", "2.2 / 2.4 re-derived numbers",
  "ledgers/LX1/scripts/LX1-d-r8/rederive_r8.py (out/rederive_r8.out); rederive_fx_r8.py (out/rederive_fx_r8.out)", "PASS",
  "Own exact-Fraction code, python3 -I. F_0 = 20000/3 -> 6667; F_2 -> 7073; q = 103/109; S_N identity True N=1,10,60,200; PV 40000/109 -> 367; witness 1000 and -666.67; g* = 7/300 = 0.023333; seeded counts 9 of 13 (3%) and 13 of 13 (1%); depth X 9.204597, Y 2.686713 (9.20, 2.69); ratio 3.425970 -> 3.4260 for all three products; V_12 = 1274345.21 -> 1274345. fx_monthly: zero months 1976-07, 2012-07, 2019-11; 668 and 321 changes; SD 0.0279353 and 0.0246995; ratio 0.8841688; difference -0.0032358; largest 0.0965747 at 2008-10; 665 nonzero."),
 ("card-duplicates", "2.7 duplicates",
  "course/modules/LX/LX1/cards.json", "PASS",
  "78 unique ids, fronts and backs (no exact duplicate). Pairs from the same definition test different facts: c014 (parity) vs c078 (convertibility); c040 (LOLR) vs c077 (central bank) vs c041, c076 (illiquid, solvent)."),
 ("card-grades-basis", "2.3 grades",
  "course/modules/LX/LX1/cards.json; BUILDER_RULES.md section 7", "PASS",
  "grades: T 34, C 17, ungraded 27 (sum 78). Every graded card has a basis and no ungraded card has one. Every C card (c009, c010, c024, c025, c037, c038, c039, c054-c060, c065-c068) names a SIMULATED lab or the embedded fx_monthly lab output. Every cite list is []."),
 ("card-misconception-and-concept-coverage", "2.7 coverage (misconceptions, key results, definitions)",
  "course/modules/LX/LX1/cards.json; L01-L04 misconception sections", "PASS",
  "Misconceptions: L01 [321]-[323] -> c011, c012, c013; L02 [318]-[327] -> c023, c016, c024; L03 [413]-[426] -> c043, c044, c045, c046; L04 [340]-[353] -> c059, c060, c061, c062. Key results: L01 [396]-[401] -> c002-c011; L02 [443]-[446] -> c015, c018, c019, c021, c025, c066; L03 [542]-[546] -> c031-c039; L04 [469]-[472] -> c050, c052, c054-c057."),
 ("card-notation", "2.4 notation",
  "notation/notation.json (8 registered symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); cards; L01-L04", "PASS",
  "No registered symbol appears in any card or lesson math (out/notation_scan_r8.txt). 'T' occurs only as a grade label. Cards use plain ASCII (no macros). Lesson-local letters (q, N, C, H, D, L, ell) are defined in their lessons, as notation.json's 'about' allows."),
 ("card-dag-concepts", "2.9 DAG",
  "course/modules/LX/LX1/cards.json; tools/check_dag.py --unit LX1", "PASS",
  "check_dag LX1: PASS (out/check_dag_LX1.out). Cards carry no concept links and name no concept outside the unit's closure. L04 names covered interest parity in prose only (L04 [328]); no card cites it."),
 ("card-banned-words", "2.9 process words",
  "course/modules/LX/LX1/cards.json", "PASS",
  "Grep for builder, verifier, round, fixer, todo, architect, planner, plan, draft, PASS, FAIL in cards.json: no process-word hits in front, back or basis (the only hits are the word 'misconception' and 'Section 3 states')."),
 ("card-scope-words", "2.4 / 2.7 scope words",
  "course/modules/LX/LX1/cards.json", "PASS",
  "Scope words (only, all, every, any, same, exactly, never, always) read in context. Universals are proved on the page or in the lab's exact check: c003 'for every N'; c007 'every price'; c019 'for every H'; c033 'no earlier period'; c013 'each discounted dividend'; c052 'every change'. Lab-scope words ('exactly', 'the same') are tied to a named lab in basis."),
 ("card-registry-offline", "2.1 registry",
  "references/references.json; tools/verify_refs.py --offline", "PASS",
  "verify_refs --offline: 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline.out). All 78 cards have cite []; no citation to check."),
 ("card-data-manifest", "2.8 data",
  "course/assets/data/market/MANIFEST.json; fx_monthly.csv", "PASS",
  "MANIFEST datasets: fx_daily (id line 5), fx_monthly (line 32), ust_daily (line 63) only, so c047 holds. fx_monthly sha256 and retrieval as in card-basis-l04-manifest."),
 ("card-gates-ruff-mypy-pytest", "gates",
  "tests/labs/LX1; tests/test_labs.py -k LX1; repo ruff", "PASS",
  "ruff check . : 'All checks passed!' ; ruff format --check . : '553 files already formatted' (out/ruff.out, exit 0). mypy --no-incremental tests/labs/LX1: 'Success: no issues found in 7 source files' (out/mypy_labs_LX1.out). pytest tests/test_labs.py -k LX1: 7 passed, exit 0 (out/pytest_labs_LX1.out)."),
 ("card-page-smoke-lessons", "2.9 page smoke",
  "tools/page_smoke.py --unit LX1 --skip-sweep", "PASS",
  "Run alone: page_smoke modules/LX/LX1/L01..L04 PASS including each lab; project.html, index.html, concepts.html, review.html PASS; 'page_smoke LX1: PASS', exit 0 (out/page_smoke_LX1.out). Chromium figure sweep skipped as the procedure allows for lesson pages."),
 ("card-delta-readthrough", "2.7 delta since round-7 pin",
  "git diff 06994db..0dee921 -- course/modules/LX/LX1", "PASS",
  "Only L03.html (6 lines: honest-pending [76], Section 3 credit-channel bullet [405] (now 'cites no source'), quiz option L03q11 [630]) and cards.json (c014 split, c016 'Section 2', c051 '10^-12', c077 and c078 added) changed. L01, L02, L04, project.html, index.html are byte-identical to the round-7 pin. Every hunk read. The L03 changes touch no sentence a card states; c047 still matches [76]; c042, c043 and c045 match unchanged text. The new c077 is read in the FAIL row above. The rest of cards.json re-verified from scratch."),
 ("card-verify-cards-lessons-subject", "2.7 cards agree with CURRENT lesson text",
  "course/modules/LX/LX1/L01.html .. L04.html", "PASS",
  "No card is carried from round 7. Every card was re-derived from the current extracted text (ledgers/LX1/scripts/LX1-d-r8/extract_text.py -> out/L01.txt .. L04.txt; [N] = HTML source line). Full read of L01 (35 KB text), L02 (30 KB), L03 (42 KB), L04 (37 KB) and the cards."),
]
for rid, check, loc, status, ev, *rest in [(g[0], g[1], g[2], g[3], g[4], g[5] if len(g) > 5 else None) for g in GATE]:
    row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = rest[0]
    rows.append(row)

frag = {
 "unit": "LX1",
 "slice": "LX1-d",
 "round": 8,
 "verifier": "Claude Haiku 5.5, independent verifier for LX1-d (ALL cards.json against L01-L04), round 8. Did not build LX1. Round-7 fragment read as context only; no PASS row carried forward; every card re-derived from the current lesson text.",
 "pin": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3",
 "base": "06994db16d1ab449bcf29898a7f56cfa999dce57 (round-7 pin)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE8-LX1-d",
 "scratch": "/tmp/lx1d8_scratch (twin runs); ledgers/LX1/scripts/LX1-d-r8/out (extracted text, outputs)",
 "scripts": "ledgers/LX1/scripts/LX1-d-r8/",
 "verified_at": "2026-11-05T01:26:06+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [
   "ust_daily.csv MANIFEST entry says retrieved 2026-10-20 (course/assets/data/market/MANIFEST.json line 71); fx_monthly and fx_daily say 2026-10-19. No card cites ust_daily's retrieval date; not a finding in this slice."
 ],
 "notes": [
   "Verdict FAIL: two non-PASS rows. card-lesson-term-monetary-base (L03.html line 390 uses 'monetary base' with no definition; lesson-side fix; carried unchanged from round 7) and card-c077 (the new card repeats that undefined term). The round-6 precedent is card-c041 FAIL for the same reason.",
   "The round-7 notes about card-c025 and card-c041 are closed as before. The new card-c077 is the same defect as the round-7 lesson row, so the lesson fix closes both.",
   "Judgment, not a defect: LX1-c008 is graded T although it is a definition; the lesson's own Key results row [401] grades it the same way, with the basis 'definition, not an empirical claim'.",
   "Judgment, not a defect: several cards state a list (c002, c029, c053). Each tests one definition or result.",
   "Judgment, lesson owner to consider: L04 uses 'forward-rate column' (card c070) first inside the Lab 1 docstring at [122], and defines 'forward rate' in prose at [321]. The first prose use is at [321], so no define-before-use violation is recorded here.",
   "Not in this slice: project.html and tests/labs/LX1/lab-LX1-project-*.py (changed since round 6, not cited by any card). run_graders and mutate_graders were not run because no card cites a graded project; the project-grader mutant requirement does not apply to this slice. No student-error mutants were written: the slice is cards, and the card-level numeric re-derivation is the test.",
   "Not checked: the licence_url quote for fx_monthly (rule 2.8) and a live fetch of the Federal Reserve feed. Plain curl was not used. The data slice owns them. verify_refs was run offline only.",
   "Not run: live verify_refs; the Chromium figure sweep of page_smoke (--skip-sweep, as the procedure allows for lesson pages)."
 ],
 "summary": "Round 8 of LX1-d: 78 cards and 20 gate/structure rows (98 rows). 96 PASS, 2 FAIL: card-lesson-term-monetary-base (L03.html:390, undefined 'monetary base', lesson-side) and card-c077 (new card repeats the undefined term). Every card re-derived from the current text; no row carried from round 7. Verdict FAIL."
}
out = f"{BASE}/ledgers/LX1/LX1-d.json"
with open(out, "w", encoding="utf-8") as h:
    json.dump(frag, h, indent=2, ensure_ascii=False)
    h.write("\n")
print("wrote", out, len(rows), "rows")
