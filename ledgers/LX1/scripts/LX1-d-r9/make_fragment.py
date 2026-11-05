"""Builds ledgers/LX1/LX1-d.json for round 9 (verifier slice d: all cards.json against L01-L04).

Every row's evidence cites a script or output saved under ledgers/LX1/scripts/LX1-d-r9/ or a file:line.
Run: python -I ledgers/LX1/scripts/LX1-d-r9/make_fragment.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LX = "course/modules/LX/LX1/cards.json"
S = "ledgers/LX1/scripts/LX1-d-r9"
OUT = "ledgers/LX1/scripts/LX1-d-r9/out"
RD = f"{S}/rederive_r9.py (output {OUT}/rederive_r9.txt)"

P = "PASS"
rows = []

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)

def card(cid, lesson_loc, evidence, status=P, fix=None, check=None):
    row("card-" + cid.split("-")[1].lower(), check or f"cards.json {cid} against {lesson_loc.split(';')[0].split(' ')[0]} text",
        f"{LX} ({cid}); {lesson_loc}", status, evidence, fix)

# ---- gate and structure rows
row("gate-check-pages", "tools/check_pages.py --unit LX1", "tools/check_pages.py (cards.json check_cards)", P,
    f"Command: .venv/bin/python tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS', exit 0 (output {OUT}/check_pages_LX1.txt).")
row("gate-check-dag", "tools/check_dag.py --unit LX1", "course/modules/LX/LX1/L01-L04.html", P,
    f"Command: .venv/bin/python tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS', exit 0 ({OUT}/check_dag_LX1.txt).")
row("gate-run-labs", "tools/run_labs.py --unit LX1 and twins under python -I -W error", "tests/labs/LX1/lab-LX1-L01-1.py .. L04-1.py", P,
    f"run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)', exit 0 ({OUT}/run_labs_LX1.txt). Each L01-L03 twin run directly with -I -W error: exit 0 ({OUT}/twin_L01.txt, twin_L02.txt, twin_L03.txt); L04 twin run from a scratch dir holding data/fx_monthly.csv: exit 0 ({OUT}/twin_L04.txt).")
row("gate-page-smoke", "tools/page_smoke.py --unit LX1 --skip-sweep (alone)", "course/modules/LX/LX1/L01-L04.html, project.html, index.html", P,
    f"Command: page_smoke.py --unit LX1 --skip-sweep -> 'page_smoke LX1: PASS', exit 0; L01-L04 each PASS ({OUT}/page_smoke_LX1.txt). The figure sweep was skipped; this slice has no live figure and the cards carry no chart.")
row("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", P,
    f"Command: verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({OUT}/verify_refs_offline_all.txt). The live run takes --unit only and was not run; no card cites a key, and the keys named in lesson references (friedman1963monetary, eichengreen1992golden, garber2000famous) were not re-resolved live.")
row("gate-notation", "notation/notation.json symbols vs LX1 pages", "notation/notation.json; course/modules/LX/LX1/L0[1-4].html", P,
    "notation.json registers 9 symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}, ...). grep over LX1 pages for each: the only 'T' tokens are grade-key labels in the Key results and grade legend (L01.html:43, 109, 396-401; L02.html:43, 443-445; L03.html:107, 124 are 'T' grade or Theorem tokens), no symbol reuse. Locally defined letters (N, m, beta, ell, D, V, P, L) are outside the registry (its 'about' says they are defined per lesson). PASS.")
row("gate-dag", "DAG: concepts used by cards outside the unit's closure", "course/modules/LX/LX1/cards.json; L01-L04", P,
    f"check_dag LX1 PASS ({OUT}/check_dag_LX1.txt). Card vocabulary (fundamental value, speculative bubble, panic, gold standard, nominal debt, price index, external-finance premium, lender of last resort, log change, dispersion) is each defined in the lesson that the card sits in (L01 [65], [105], [289]; L02 [57], [82]; L03 [72], [81], [389]; L04 [59], [85]). 'Bretton Woods' is named only as pending (L04 [86]) and card LX1-c062 says so.")
row("data-manifest-facts", "MANIFEST facts used by cards c063, c064, c069, c070, c075", "course/assets/data/market/MANIFEST.json (fx_monthly, fx_daily); fx_monthly.csv header", P,
    f"MANIFEST: fx_monthly retrieved 2026-10-19, rows 669, first 1971-01, last 2026-09, key month, columns AUD CAD CHF DKK EUR GBP JPY NOK NZD SEK (all exchange rates); fx_daily and ust_daily first 2000-01-03 (so window two start, c063). Issuer Board of Governors of the Federal Reserve System, citation string as in c064. Header of fx_monthly.csv read by {RD}: ['month','AUD',...,'SEK'] (c070). Licence_url of fx_monthly NOT opened in this slice (data slice owns rule 2.8).")
row("card-coverage", "BUILDER_RULES §7: one card per definition, theorem, key formula, key result and misconception", f"{LX}", P,
    "Mapped every lesson's misconceptions (L01 [321]-[323] -> c011-c013; L02 [318]-[327] -> c023, c016, c024; L03 [413]-[425] -> c043-c046 and c045; L04 [340]-[352] -> c059, c061, c060, c062), the numbered definitions and results of each lesson (L01 Defs 1.2, 2.1, 3.1, Thm 1.3, Prop 1.4, Prop 2.2; L02 Defs 1.1, 3.1, Prop 1.2, Prop 2.1, Cor 3.2; L03 Defs 2.1, 2.2, 4.1, Lemma 3.1, Prop 3.2, Cors 3.3, 3.4, Rem 4.2; L04 Defs 1.1, 2.1, Props 1.2, 2.2) and the Key results rows. No required item is absent beyond the lab-result rows already carried by c009, c010, c037-c039, c054-c058, c065-c067.")
row("scan-duplicates", "full scan of the 78 fronts and backs for duplicate ids, fronts and near-duplicates", LX, P,
    f"Ids unique and fronts unique (python -I check in {S}/out/cards_dump.txt). difflib ratio on front+back: LX1-c037 vs c038 0.97 (same template, economy X vs economy Y, different values 9.20 vs 2.69), LX1-c055 vs c056 0.73 (different windows). No duplicate fact.")
row("scan-process-words", "no process words in learner text (rule 12)", LX, P,
    "grep -i over cards.json for verif, builder, round, audit, ledger, draft, todo, fragment, pending, reviewer, agent: one hit, LX1-c065 back 'as Section 3 states' (a lesson reference, not a process word).")
row("grade-scan", "re-grade every graded card against BLUEPRINT §3 (T = theorem proved on the page; C = single study or lab result)", LX, P,
    "T cards: c002-c005, c007, c011-c013, c015, c016, c018, c019, c021-c023, c030-c036, c042-c046, c050-c052, c059, c061, c062, c079 re-graded as theorems, definitions-with-proof or structural statements about the model: agree. C cards: c009, c010, c024, c025, c037-c039, c054-c058, c060, c065-c068 rest on Lab 1 output (SIMULATED or fx_monthly): agree. c008 is the exception (see row card-c008).")

# ---- lesson defect carried from round 8, re-verified fresh this round
row("card-lesson-term-monetary-base", "undefined term 'monetary base' in lesson text (define-before-use, rule 5)", "course/modules/LX/LX1/L03.html:390 (Definition 4.1)", "FAIL",
    f"L03.html:390 reads: 'A <dfn id=\"def-central-bank\">central bank</dfn> is the public institution that issues the monetary base.' Fresh grep this round: 'monetary base' occurs only at course/modules/LX/LX1/L03.html:390 across all of course/ (no <dfn>, not in course/assets/data/glossary.json, not in plans/LX1-build-plan.md). The line is byte-identical to round 8 (the L03 diff at c93dd52 changes only line 76, the honest-pending note).",
    fix="Rewrite L03.html:390 to avoid the undefined term, e.g. 'A central bank is the public institution that issues the currency.' (the term is not used anywhere else in the unit). Or, if the term is kept, add a <dfn> at its first use and a glossary entry, and rebuild with tools/build_site.py.")

# ---- cards, one row per card id (78 present, plus LX1-c077 removed)
card("LX1-c001", "L01.html [65]-[67]", "Def 1.2 F_t = sum_k d_(t+k)/(1+r)^k 'whenever the series converges'; 'benchmark, not a forecast' ([67]). Front and back match. Ungraded definition.")
card("LX1-c002", "L01.html [58]-[59], [72]-[74], proof [79]-[82]", f"Thm 1.3 hypotheses A0 and A1 ([58]-[59]); F_t = d_1(1+g)^t/(r-g) = d_(t+1)/(r-g), F_0 = d_1/(r-g), series converges ([72]-[73]). {RD}: F_0 = 20000/3, rounds to 6667 cents. T.")
card("LX1-c003", "L01.html [74], [81]-[83]; Part A [246]-[248]", f"S_N(t) = F_t(1-q^N) exact for every N ([74]). {RD}: identity exact (Fraction) for N = 1..200 at t = 0. Twin prints 'holds exactly: True' for N = 10, 60, 200 (twin lines 'N = 10/60/200'). Basis says the lab checks t = 0 only, which matches the lab. T.")
card("LX1-c004", "L01.html [84]", f"Under A0, 1+r > 1+g > 0 gives 0 < q < 1, so q^N -> 0 and S_N(t) -> F_t ([84]). {RD}: q = 103/109, 0 < q < 1 True. T.")
card("LX1-c005", "L01.html [91], proof [96]", "Hypotheses (A1) d_1 > 0, 1+g > 0 and (A2) r > -1, g >= r ([91]); conclusion S_N(0) -> +inf, Theorem 1.3 does not apply ([91], [96]). T.")
card("LX1-c006", "L01.html [105]", "B_t = P_t - F_t counted as a bubble only when B_t > 0, in cents; B_t <= 0 has no bubble ([105]). Ungraded definition, matches.")
card("LX1-c007", "L01.html [111]-[114], proof [119]", f"Hypotheses (A3) d_1 > 0 and (A4) g < g' with r > g, r > g', 1+g > 0, 1+g' > 0 ([112]); conclusion F_0(g) < F_0(g') and the gap split ([114]). {RD}: F_0(1%) = 5000 < F_0(3%) = 6666.67. T.")
card("LX1-c008", "L01.html [289]; Key results [401]; Def 3.1", "Mechanism only: sudden collective demand to convert claims; no frequency, trigger or size ([289]), matching the lesson. The defect is the grade, not the text: the card is graded T with basis 'a definition; it states no empirical claim'. BLUEPRINT §3 defines T as 'Theorem: proved on the page, or with a precisely cited proof'. A definition is neither, and sibling definition cards LX1-c001, c006, c014, c017, c020 are ungraded. Round 8 accepted T as a judgment; re-graded here as a mismatch.",
     status="FAIL",
     fix="Remove the grade and basis from LX1-c008, as c001/c006/c020 are (ungraded definition). Remove the T grade from the L01.html Key results row at [401] (Definition 3.1), so the lesson does not grade a definition as a theorem.")
card("LX1-c009", "L01.html [264] (Part B printed line); [132]", f"Printed: 'periods with price above fundamental: 9 of 13' (L01.html [264]; twin line 21). {RD}: 9 of 13 with the lab's seed and wedge rule. C, SIMULATED, named in basis.")
card("LX1-c010", "L01.html [280]-[281]; twin lines 37-38", f"Printed '13 of 13' and 'the count changes with the assumed growth rate: True' ([280]-[281]). {RD}: 13 of 13 at 1%. C, SIMULATED.")
card("LX1-c011", "L01.html [120] witness", f"d_1 = 400, r = 9%: F_0(1%) = 5000, F_0(3%) = 20000/3; at P_0 = 6000 gaps +1000 and -2000/3 ([120]). {RD}: 1000 and -2000/3. T.")
card("LX1-c012", "L01.html [310]; misconception 2 [322]", f"d_1 = 400, d_s = 0 for s >= 2 (stated as d_2 = 0, d_s = 0 for s >= 3, [310]), r = 9%: 400/1.09 = 40000/109 -> 367 ([310]). {RD}: 40000/109, rounds to 367. T.")
card("LX1-c013", "L01.html [96] proof; misconception 3 [323]", f"Under (A1) and (A2) g >= r: each term d_1 q^(k-1)/(1+r) >= d_1/(1+r) ([96]), so S_N(0) >= N d_1/(1+r) ([96], [323]). {RD}: each term k = 1..50 >= d_1/(1+r) at g = 9% and g = 10%. T.")
card("LX1-c014", "L02.html [57]", "Def 1.1: parity kappa > 0, grams of gold per unit of currency; matches ([57]). Ungraded definition.")
card("LX1-c015", "L02.html [65]-[67], proof [72]", "Prop 1.2 hypothesis (A1) parity kept at every date; one gram costs 1/kappa units at every date ([65]-[67]). T.")
card("LX1-c016", "L02.html [71]-[77]", "Prop 1.2 gives one price; (A1) does not involve P_t, so the conclusion holds whatever P_t does ([77]). T.")
card("LX1-c017", "L02.html [82]-[83]", "V_t = D P_0/P_t, D nominal in integer cents, P_0 base value ([82]-[83]). Ungraded definition.")
card("LX1-c018", "L02.html [89]-[97]", f"Prop 2.1(a) hypotheses (A2) D fixed positive integer cents, paid in full, not renegotiated; (A3) P_t positive ([89]-[90]); V_t/V_(t-1) = P_(t-1)/P_t, D P_0 cancels ([97]). Lab identity True for t = 1..12 (twin line 287). T.")
card("LX1-c019", "L02.html [92], [98]", "Prop 2.1(b): V_H/V_0 = P_0/P_H by telescoping ([98]). T.")
card("LX1-c020", "L02.html [110]", "Debt deflation: rise in V_t implied by a fall in P_t with D fixed, an arithmetic consequence, not a causal claim ([110]). Ungraded definition.")
card("LX1-c021", "L02.html [118], proof [122]-[123]", "Cor 3.2: V_t > V_(t-1) iff P_t < P_(t-1) ([118]); proof from Prop 2.1(a) ([123]). T.")
card("LX1-c022", "L02.html [128] Remark 3.3; [97]", "Factor P_(t-1)/P_t, larger than one in a fall; Cor 3.2 gives direction, not size ([128]). T.")
card("LX1-c023", "L02.html [318]-[319] (misconception 1); [118]", "Cor 3.2 gives the opposite direction: a fall in P_t raises V_t, so the same nominal payment is a larger real burden ([319]). T.")
card("LX1-c024", "L02.html [82]-[83], [327]; twin lines 274-286", f"Constant iff P_t constant: V_t = D P_0/P_t ([83], [327]). Lab Part B prints the real value (twin lines 274-286). {RD}: all 12 consecutive cent differences are nonzero. Grade C with basis naming Lab 1 Part B, SIMULATED.")
card("LX1-c025", "L02.html twin line 287 (Part B); [135]", f"Printed 'identity ... holds exactly for t = 1 to 12: True' (twin line 287). {RD}: exact Fraction identity True. C, SIMULATED.")
card("LX1-c026", "L03.html [58]-[59]", "Assumption 1.1: P_t = (1-delta)^min(t,m), P_0 = 1, 0 <= m <= H, 0 < delta < 1; falls on parity, flat after m ([58]-[60]). Ungraded.")
card("LX1-c027", "L03.html [82]", "Def 2.1: L_t = V_t/N_t, ratio of real debt to net worth ([82]). Ungraded.")
card("LX1-c028", "L03.html [72], [82]", "psi_t = phi (L_t - L_0), phi > 0 (A3) ([72]); the premium is the rise above baseline ([82]). Ungraded.")
card("LX1-c029", "L03.html [87]", "Def 2.2 chain: price fall raises V_t (A1, A2); rise lowers net worth one for one (A2); higher leverage raises premium (A3); output fall f_t = beta psi_t with beta > 0 (A3); describes the model only ([87]). Ungraded.")
card("LX1-c030", "L03.html [95]-[103]", "Lemma 3.1: C = N_0 + D, ell(x) = x/(C-x) on [D, C), L_t = ell(V_t) when V_t < C, L_0 = D/N_0, ell strictly increasing ([95], [102]-[103]). T.")
card("LX1-c031", "L03.html [108]-[109], proof [116]", "Prop 3.2(a) bound V_t <= V_m for 0 <= t <= H ([109], [116]); hypotheses include V_m < N_0 + D (A2) ([66]). T. The back states only the bound; the rest of (a) is on LX1-c079.")
card("LX1-c032", "L03.html [110], [117]", f"depth(m) = beta phi (ell(V_m) - ell(D)) = beta phi (V_m/(N_0+D-V_m) - D/N_0) ([110]). {RD}: closed form equals the direct max over t of f_t for m = 0..12, exact. T.")
card("LX1-c033", "L03.html [111], [118]", f"Prop 3.2(c): maximum first attained at t = m; no earlier period when m >= 1 ([111], [118]). {RD}: first index 12 for m = 12. T.")
card("LX1-c034", "L03.html [111], [118], P2 [470]-[473]", f"With m = 0, V_t = D, L_t = L_0, premium zero, depth(0) = 0 ([118], [473]). {RD}: depth(0) = 0 exact. T.")
card("LX1-c035", "L03.html [125]-[130]", f"Cor 3.3: 0 <= m' < m <= H gives depth(m') < depth(m); X (m=12) deeper than Y (m'=4) ([125]). {RD}: depth(4) < depth(12). T.")
card("LX1-c036", "L03.html [134]-[137], proof [141]-[142]", f"Cor 3.4 ratio = (ell(V_m) - ell(D))/(ell(V_m') - ell(D)), 1 <= m' < m <= H, independent of beta, phi ([136]-[137]). {RD}: ratio identity holds exactly. T.")
card("LX1-c037", "L03.html [149], [359] (twin line 33)", f"Twin prints 'economy X depth 9.20 percent of baseline output, first reached at t = 12' (twin line 33). {RD}: exact 9.204597 percent, first at t = 12. C, SIMULATED.")
card("LX1-c038", "L03.html [360] (twin line 34)", f"Twin prints 'economy Y depth 2.69 percent ... first reached at t = 4' (twin line 34). {RD}: exact 2.686713 percent, first at t = 4. C, SIMULATED.")
card("LX1-c039", "L03.html [381] (twin line 55 for phi = 1)", f"Printed 'ratio of depths X to Y 3.4260' for beta phi = 1 (twin line 55). {RD}: exact 3.425970, rounds to 3.4260. C with basis Part D and Cor 3.4.")
card("LX1-c040", "L03.html [389]-[390]", "Def 4.1: LOLR is a central bank that lends against collateral to solvent but illiquid institutions ([390]). Ungraded. The card text is accurate; the monetary-base sentence in the same line is row card-lesson-term-monetary-base.")
card("LX1-c041", "L03.html [390]", "Illiquid: cannot meet payments from its own resources in the time available ([390]). Ungraded.")
card("LX1-c042", "L03.html [395] Remark 4.2", "Assumption 1.2 has no lending term; Assumption 1.3 has no term through which a facility changes a solvent borrower's premium; Prop 3.2 says nothing about a facility ([395]). T.")
card("LX1-c043", "L03.html [402], [413]-[414]; Assumption 1.2 [65]", "One borrower and no bank; Assumption 1.2 excludes default and balance-sheet change; proof of Prop 3.2 uses none of these ([413]-[414]). T.")
card("LX1-c044", "L03.html [417]-[418]", "Ordering follows from parity durations 12 and 4 that the lab sets under Assumption 1.1; the model cannot say whether holding parity causes a deeper fall ([418]). T.")
card("LX1-c045", "L03.html [421]-[422] (misconception 3); [395]", "Def 4.1 requires collateral and limits lending to solvent but illiquid institutions; the model has no facility, so no panic result follows ([422], [395]). T.")
card("LX1-c046", "L03.html [425]-[426]; Prop 3.2(b) [110]", "SIMULATED model value under Assumption 1.3 with phi = beta = 1; no output series enters the lab (the L03 lab code, out/L03.txt, contains no open, read, csv or Path call: grep returned no match). Depth scales by beta phi ([110], [426]). T.")
card("LX1-c047", "L03.html [76] honest-pending note", "No redistributable historical series for gold-standard adherence or output depth is embedded; the lab runs the stylised model, labelled SIMULATED ([76]). Ungraded.")
card("LX1-c048", "L04.html [59]", "ell_t = ln(x_t/x_(t-1)), per month, not annualized ([59]). Ungraded definition.")
card("LX1-c049", "L04.html [59]", "Dispersion = sample SD with denominator n - 1 about the mean; defined only when n >= 2 ([59]). Ungraded definition.")
card("LX1-c050", "L04.html [66]-[71]", "Prop 1.2 under (A1) (positive rates a..b, a < b): sum of ell_t for t = a+1..b is ln(x_b/x_a), with b - a terms ([66]); proof ([71]). T.")
card("LX1-c051", "L04.html [76]; lab code SUM_TOLERANCE line (out/L04.txt line 161)", "Remark 1.3: exact in reals; the lab checks in floats to 1e-12 ([76]); the code has SUM_TOLERANCE = 1e-12 (L04 lab code line 161). T.")
card("LX1-c052", "L04.html [92]-[100]", "Prop 2.2 under (A2), kappa > 0, n >= 2: every monthly change is 0 and the dispersion is 0 ([94], [99]-[100]). T.")
card("LX1-c053", "L04.html [85]", "Def 2.1 contents: anchor currency, one foreign currency, parity kappa > 0 in anchor units, market rate x_t > 0; the fixed-parity model adds (A2) ([85]). Ungraded.")
card("LX1-c054", "L04.html twin line 7 (Part B); [318]", f"Printed 'months with an exactly zero change: 3: 1976-07, 2012-07, 2019-11' (twin line 7). {RD}: same 3 months from fx_monthly.csv GBP, 668 changes. C, Lab 1 Part B.")
card("LX1-c055", "L04.html twin line 9 (Part C); [318]", f"Printed 'window one ... standard deviation 0.027935' (twin line 9); L04.html [318] prints 0.027935. {RD}: 0.027935278, n = 668. C.")
card("LX1-c056", "L04.html twin line 12 (Part C); [318]", f"Printed 'window two ... standard deviation 0.024700' (twin line 12). {RD}: 0.024699501, n = 321. C.")
card("LX1-c057", "L04.html twin line 17 (Part D); [318]", f"Printed ratio 0.8842 (twin line 17). {RD}: 0.8842 (4 dp). C.")
card("LX1-c058", "L04.html twin line 13 (Part C); [318]", f"Printed '0.096575 ... at 2008-10 (signed -0.096575)' (twin line 13). {RD}: window two largest |change| 0.0965747, 2008-10, signed negative. C.")
card("LX1-c059", "L04.html [85], [105]", "Prop 2.2 gives zero change in the model; (A2) describes the model, and the recorded rate need not equal parity (Remark 2.3, [105]). T.")
card("LX1-c060", "L04.html [345], E3 [432]", "Lab computes two SDs and their difference; no test, no cause; window start is a convention ([345], [432]). C, Lab 1 Part D.")
card("LX1-c061", "L04.html [349], M1 [368]", f"Rise 1.00 -> 1.10: simple change 0.10, ln 1.1 = 0.095310 to six decimals, difference 0.004690 ([349]). {RD}: ln 1.1 = 0.0953101798, difference 0.0046898 -> 0.004690. T.")
card("LX1-c062", "L04.html [81], [86], [353]", "Def 2.1 defines a model class, not the historical arrangement; 'Bretton Woods system: definition pending' ([86]); no historical fact stated ([353]). T (structural).")
card("LX1-c063", "L04.html [128]; MANIFEST fx_daily, ust_daily first 2000-01-03", "Window two starts at the first month in which fx_daily and ust_daily have data, both starting 2000-01-03 in MANIFEST ([128]; MANIFEST entries). The start is a convention ([330]). Ungraded.")
card("LX1-c064", "L04.html [117]-[121] (lab docstring); MANIFEST fx_monthly", "fx_monthly.csv: Board of Governors, G.5/H.10 (noon buying rates in New York), GBP in USD per pound, last value in its month ([117]-[120]); MANIFEST citation and transform match. Ungraded.")
card("LX1-c065", "L04.html twin line 16 (Part D); [318]", f"Printed difference -0.003236 (twin line 16); lesson [318] states it is computed from unrounded SDs. {RD}: unrounded difference -0.003235777 -> -0.003236. C.")
card("LX1-c066", "L02.html twin lines 31-33 (Part C)", f"Printed 6 of 12 falling index and 6 of 12 rising real value, and 'exactly: True' (twin lines 31-33). {RD}: 6 and 6, sets equal. C, SIMULATED.")
card("LX1-c067", "L03.html twin lines 54-56 (Part D)", f"Printed the same 3.4260 for phi/beta products 1/2, 1, 3 (twin lines 54-56). {RD}: 3.425970 for each. C, SIMULATED.")
card("LX1-c068", "L04.html twin line 7; [318]", f"Printed 3 zeros of 668 in window one, so 665 nonzero ([318]; [341]). {RD}: 665. C.")
card("LX1-c069", "L04.html [120] (lab docstring); MANIFEST fx_monthly rows 669", "The count (669 months, 1971-01 to 2026-09) matches MANIFEST rows and the lab docstring ([120]), and rederive reads 669. The fact is correct, but it is a row count of a data file with no bearing on any concept or lab claim. BUILDER_RULES §7 ('Do not make cards of trivia') and VERIFIER_RULES §2.7 ('not trivia') fail it. Judgment, see notes.",
     status="FAIL",
     fix="Delete LX1-c069 from cards.json. If a card is wanted here, replace it with one on the window-one convention (L04.html [110], [126]: window one holds the 668 changes dated 1971-02 to 2026-09).")
card("LX1-c070", "L04.html [122], [328]; MANIFEST fx_monthly columns", "fx_monthly.csv holds exchange-rate columns only: no interest-rate or forward-rate column ([122]); MANIFEST columns are ten currencies (AUD ... SEK) and the header read in rederive matches. The lab cannot test a rate relation ([328]). Ungraded.")
card("LX1-c071", "L03.html [65]", "N_t = N_0 - (V_t - V_0); whole rise in real debt falls on net worth; no default ([65]). Ungraded.")
card("LX1-c072", "L03.html [73]", "depth(m) = max over 0 <= t <= H of f_t, f_t = beta psi_t, fraction of baseline output ([73]). Ungraded.")
card("LX1-c073", "L02.html [82]", "Nominal debt: amount of currency owed at each date, in the currency's own units, not indexed; here D cents ([82]). Ungraded.")
card("LX1-c074", "L02.html [82]", "Price index P_t at date t, base date 0, positive values, P_0 base value ([82]). Ungraded.")
card("LX1-c075", "L04.html [114], [120]; MANIFEST fx_monthly retrieved", "The retrieval date 2026-10-19 matches MANIFEST 'retrieved' and the lab docstring ([120]). The fact is correct, but a download date of a data file is trivia: it has no bearing on any concept, claim or lab output of the unit, and BUILDER_RULES §7 ('Do not make cards of trivia') and VERIFIER_RULES §2.7 ('not trivia') fail it. Judgment, see notes.",
     status="FAIL",
     fix="Delete LX1-c075 from cards.json. Do not replace it with another provenance card; provenance is already in the lesson's References section (L04.html [566]-[568]).")
card("LX1-c076", "L03.html [390]", "Solvent: assets, valued as the lender values them, cover liabilities ([390]). Ungraded definition. The sentence sits beside the monetary-base wording, row card-lesson-term-monetary-base.")
row("card-c077", "removed card: cards.json has no LX1-c077 at c93dd52", f"{LX} (no LX1-c077)", P,
    "The round-8 card LX1-c077 (back: 'The public institution that issues the monetary base.') is absent at pin c93dd52 (git diff 0dee921a..HEAD removes it; the card ids are not reused). Its defect is recorded in card-lesson-term-monetary-base, which remains FAIL because the lesson sentence is unchanged.")
card("LX1-c078", "L02.html [57]", "Def 1.1 convertibility: issuer stands ready to buy and sell gold at the parity on demand ([57]). Ungraded.")
card("LX1-c079", "L03.html [108]-[109], proof [116]", "Prop 3.2(a) second half: V_t = D(1-delta)^(-t) for t <= m, strictly increasing when m >= 1; V_t = V_m for t >= m ([109], [116]). Hypotheses: Assumptions 1.1 to 1.3 ([108]). T.")

summary = ("Round 9 of LX1-d: 78 cards present (LX1-c077 removed; c079 added since round 8) and 11 gate, structure and scan rows. "
           "Every card re-derived from the current lesson text; no row carried from round 8. 4 non-PASS rows: "
           "card-lesson-term-monetary-base (L03.html:390, undefined 'monetary base', unchanged since round 8), "
           "card-c008 (definition graded T), card-c069 and card-c075 (trivia, judgment). Verdict FAIL.")

frag = {
    "unit": "LX1",
    "slice": "LX1-d",
    "round": 9,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-d (ALL cards.json against L01-L04), round 9. Did not build LX1.",
    "pin": "c93dd526025c6dffd34c54cd2c89eb62a890f885",
    "base": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3 (round-8 pin)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE9-LX1-d",
    "scratch": "/tmp/lx1d9_scratch (twin L04 run); outputs under ledgers/LX1/scripts/LX1-d-r9/out/",
    "scripts": "ledgers/LX1/scripts/LX1-d-r9/",
    "verified_at": "2026-11-05T04:32:31+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since the round-8 pin (0dee921a..c93dd526) in the LX1 slice: cards.json (c013, c021, c031, c060, c061, c067 wording; c077 removed; c078 moved; c079 added), L03.html:76 (honest-pending wording only), project.html (rubric text), and glossary/program.json (M3 entry, not LX1). Every card was re-derived anyway; the round-8 PASS rows were not carried forward.",
        "The round-8 monetary-base row is re-verified fresh: still FAIL, lesson-side (L03.html:390). The fix is a lesson edit, not a card edit.",
        "Judgment, not a mechanical rule: card-c008 is graded T for a definition. BLUEPRINT §3 T means a theorem proved on the page. The round-8 verifier accepted it because the lesson's Key results row grades the definition T too. This verifier does not, and the fix covers both places.",
        "Judgment: LX1-c069 and LX1-c075 are correct but are trivia (a row count and a download date) under BUILDER_RULES §7. If the builder regards them as provenance worth keeping, the orchestrator may overrule this row; the facts themselves were checked against MANIFEST.json and the lab docstring.",
        "Lab twins: every printed line cited by a card was read from a fresh run of the twin under python -I -W error (outputs saved), not only from the page. run_labs.py passed 7/7.",
        "This slice has no project grader cited by any card, so run_graders, mutate_graders and mutants do not apply; mutants is empty by design. No new student-error mutants were written.",
        "Not checked: the licence_url quote for fx_monthly (rule 2.8, data slice); a live verify_refs run (the --unit option needs a live run and was not run; the offline run passed); the figure sweep of page_smoke (skipped with --skip-sweep, which the procedure allows for lesson pages; no card concerns a figure); ruff and mypy (no Python file in this slice changed; the lab twins were run directly); pytest (run_labs and check_pages cover the same checks).",
        "Plain curl was not used in this round; no URL was fetched.",
    ],
    "summary": summary,
}

Path(ROOT / "ledgers/LX1/LX1-d.json").write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "non-PASS", [r["id"] for r in rows if r["status"] != "PASS"])
