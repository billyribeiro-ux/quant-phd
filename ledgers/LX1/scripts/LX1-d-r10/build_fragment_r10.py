import json, sys, datetime
root = sys.argv[1]
R = "ledgers/LX1/scripts/LX1-d-r10/out"
DER = f"{R}/rederive_r10.txt"
CS = "course/modules/LX/LX1/cards.json"
L = {"L01": "course/modules/LX/LX1/L01.html", "L02": "course/modules/LX/LX1/L02.html",
     "L03": "course/modules/LX/LX1/L03.html", "L04": "course/modules/LX/LX1/L04.html"}
cards = json.load(open(f"{root}/{CS}", encoding="utf-8"))
byid = {c["id"]: c for c in cards}
rows = []
def row(i, check, loc, ev, status="PASS", fix=None):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if fix: r["fix"] = fix
    rows.append(r)

# gates, fresh this round
row("gate-check-pages", "tools/check_pages.py --unit LX1 (check_cards included)", CS,
    f"Command: .venv/bin/python tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS', exit 0 ({R}/check_pages_LX1.txt).")
row("gate-check-dag", "tools/check_dag.py --unit LX1", "course/modules/LX/LX1/L01-L04.html; " + CS,
    f"Command: .venv/bin/python tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS', exit 0 ({R}/check_dag_LX1.txt).")
row("gate-run-labs", "tools/run_labs.py --unit LX1; twins alone under python -I -W error; page code vs twin; expected block vs output",
    "tests/labs/LX1/lab-LX1-L01-1.py .. L04-1.py; L01-L04.html (data-run and expected blocks)",
    "run_labs LX1: PASS (7/7), exit 0 (" + R + "/run_labs_LX1.txt). Each twin run alone with python -I -W error from a scratch dir (L04 with data/fx_monthly.csv copied from course/assets/data/market): exit 0, empty stderr (" + R + "/twin_L01.txt .. twin_L04.txt). twin_vs_page.py: page data-run code equals the twin byte for byte except the one trailing newline the page omits (checked with code+'\\n' == twin); expected block equals the twin output for L01 (38 lines), L02 (41), L03 (56), L04 (17) (" + R + "/twin_vs_page.txt).")
row("gate-page-smoke", "tools/page_smoke.py --unit LX1 --skip-sweep (alone)", "course/modules/LX/LX1/L01-L04.html, project.html, index.html",
    f"Command: .venv/bin/python tools/page_smoke.py --unit LX1 --skip-sweep -> 'page_smoke LX1: PASS', exit 0 ({R}/page_smoke_LX1.txt).")
row("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json",
    f"Command: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({R}/verify_refs_offline.txt). Live run not run (takes no unit; no card cites a key).")
row("gate-mypy-ruff-pytest", "mypy --no-incremental; ruff on tests/labs/LX1; pytest -k LX1", "tests/labs/LX1/*.py; tests/test_labs.py, tests/test_run_labs.py, tests/test_page_smoke.py, tests/test_memo_exemplars.py",
    f"mypy --no-incremental: 'Success: no issues found in 385 source files', exit 0 ({R}/mypy_full.txt). ruff check and ruff format --check tests/labs/LX1: exit 0, '7 files already formatted' ({R}/ruff_lx1_twins.txt). pytest -k LX1: 7 passed, exit 0 ({R}/pytest_lx1.txt).")
row("gate-notation", "notation/notation.json symbols vs the LX1 lessons and cards", "notation/notation.json; course/modules/LX/LX1/L0[1-4].html; " + CS,
    "notation.json lists 8 entries: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. grep over LX1 lesson math for \\Phi, \\gamma, \\mathbb{Q}, R^, R_f: no hits. In cards.json the token T occurs 37 times: 35 grade values and 2 grade-key references '(T)' in the basis of LX1-c039 and LX1-c067 (" + R + "/card_scan_r10.txt context). Local letters (q, F^*_t, ell, psi, f, V, N, L, D, P) are defined per lesson. PASS.")
row("gate-dag", "DAG: concepts used by cards outside the unit closure", CS + "; L01-L04",
    f"check_dag LX1 PASS ({R}/check_dag_LX1.txt). Card-only terms are defined in the lesson holding the card: fundamental value (L01 [65]), speculative bubble (L01 [105]), financial panic (L01 [289]), central bank (L03 [390], dfn def-central-bank), lender of last resort (L03 [390]), solvent and illiquid (L03 [390]), gold standard (L02 [57]), nominal debt (L02 [82]), price index (L02 [82]), external-finance premium (L03 [82]), monthly log change and dispersion (L04 [59]), anchor currency (L04 [85]). Bretton Woods is named only as pending (L04 [38], [86]; LX1-c062 says so).")
row("data-manifest-facts", "MANIFEST facts cited by cards c063, c064, c070 and c054-c058, c065", "course/assets/data/market/MANIFEST.json (fx_monthly, fx_daily, ust_daily); course/assets/data/market/fx_monthly.csv",
    f"MANIFEST fx_monthly: retrieved 2026-10-19, rows 669, first 1971-01, last 2026-09, columns AUD CAD CHF DKK EUR GBP JPY NOK NZD SEK, transform 'each column's last value in the month', GBP not inverted. fx_daily and ust_daily: first 2000-01-03. sha256 of fx_monthly.csv computed (60572240...3e) equals the MANIFEST sha256; header ['month','AUD',...,'SEK'], 669 rows, consecutive months (rederive_r10.txt). Licence_url of fx_monthly not opened (data slice owns it).")
row("data-register-note", "tools/data_sources.yaml fx_monthly note (supports L04 [328] and c070)", "tools/data_sources.yaml:53-64",
    "fx_monthly note reads 'Each value is the last noon rate of its month ... Spot rates only, as for fx_daily.' (tools/data_sources.yaml line 64). This is the note L04 [328] cites; no interest-rate or forward column is in the header (rederive_r10.txt).")
row("lesson-curriculum-claims", "curriculum entry for LX1 vs lesson claims (L01 [303], L03 [76])", "curriculum/06-profession-capstone.yaml:25, :41",
    "Curriculum core names 'Bubbles and panics from the Dutch Republic to 2008' (line 25) and lab 'Gold-standard adherence vs. depression depth on embedded data' (line 41). L01 [303] and L03 [76] (the honest-pending note: curriculum names embedded data; none is embedded) agree with these lines.")
row("registry-citations", "registry years and titles for keys cited by LX1 lessons", "references/references.json; L02 [537], L03 [640], L04 [350], L01 [488]",
    "friedman1963monetary: 'A monetary history of the United States 1867-1960', 1963; eichengreen1992golden: 'Golden fetters: the gold standard and the Great Depression, 1919-1939', 1992; garber2000famous: 'Famous First Bubbles: The Fundamentals of Early Manias', 2000. Lesson citations match (title and year). No card cites these keys (cite lists empty).")
row("card-coverage", "BUILDER_RULES 7 coverage: one card per definition, theorem, key result and misconception", CS + "; L01-L04.html",
    "Re-mapped every lesson's misconceptions (L01 [321]-[323] -> c011-c013; L02 [318]-[327] -> c016, c023, c024; L03 [413]-[425] -> c043-c046; L04 [340]-[353] -> c059-c062) and every numbered definition, proposition, theorem, corollary and Key-results row. Key results: L01 rows [396]-[400] (c002, c003, c005, c007, c009/c010); L02 [443]-[446] (c015, c018/c019, c021, c025/c066); L03 [542]-[546] (c032/c033, c035, c036, c037-c039); L04 [469]-[472] (c052, c050, c055-c057, c054). Def 3.1 of L01 has no Key-results row any more (removed this round). No required item is missing.")
row("scan-duplicates", "duplicate ids, fronts and near-duplicate facts", CS,
    "78 cards; ids unique; fronts unique (cards_dump / card_scan_r10.txt). Near-duplicate pairs by difflib: c037/c038 (ratio 0.966, same template, economy X vs Y, values 9.20 vs 2.69 and first t 12 vs 4), c018/c019 (0.736, different parts (a) and (b)). No duplicate fact.")
row("scan-process-words", "no process words in learner text (rule 12)", CS,
    "regex over front, back and basis for verif, builder, round, audit, ledger, draft, todo, fragment, pending, reviewer, agent, lab-N: one hit, LX1-c065 'as Section 3 states' (a lesson reference). No process word.")
row("grade-scan", "re-grade every graded card against BLUEPRINT 3", CS,
    "Grades: T 35, C 17, ungraded 26; every card with a grade has a basis and every basis has a grade (card_scan_r10.txt). T = theorem or proof on page or a structural statement about the model: c002-c005, c007, c011-c013, c015, c016, c018, c019, c021-c024, c030-c036, c042-c046, c050-c052, c059, c061, c062, c079. C = Lab 1 output, SIMULATED or fx_monthly: c009, c010, c025, c037-c039, c054-c058, c060, c065-c068, c081 (c066 is C). Ungraded = definitions and data facts (c001, c006, c008, c014, c017, c020, c026-c029, c040, c041, c047, c048, c049, c053, c063, c064, c070-c076, c078, c080). Judgment: c061 (a worked calculation, L04 M1) graded T is accepted as a computation proved on the page.")
row("card-lesson-term-monetary-base", "undefined term 'monetary base' in lesson text (rule 5), round-9 FAIL re-verified", "course/modules/LX/LX1/L03.html:390 (Definition 4.1)",
    f"Round-9 FAIL subject changed: L03.html:390 now reads 'A central bank is the public institution that issues the currency.' (dfn def-central-bank kept). grep -rn 'monetary base' course/modules/LX/LX1 returns no hit; grep over course/ returns no other hit in this checkout (rederive/grep at round 10). PASS.")

# cards
ev = {}
ev["c001"] = ("L01.html [65]-[67]", "Def 1.2: F_t = sum over k of d_(t+k)/(1+r)^k, whenever the series converges; 'benchmark ... not a forecast' ([67]). Ungraded definition, matches.")
ev["c002"] = ("L01.html [72]-[74], proof [79]-[83]", "Thm 1.3 hypotheses A0, A1 ([58]-[59]); F_t = d_1(1+g)^t/(r-g) = d_(t+1)/(r-g) ([73]); F_0 = d_1/(r-g) ([74]). " "Re-derived F_0 = 20000/3 -> 6667 cents (" + DER + "). T.")
ev["c003"] = ("L01.html [74], [82]-[83]; Part A [244]-[248]", "S_N(t) = F_t(1-q^N) exactly for every N>=1, q=(1+g)/(1+r) ([74]). Exact Fraction identity True at N=10,60,200 (" + DER + "; twin line 'identity ... True'). Basis says t=0 only; Part A is t=0 only (L01 lab code). T.")
ev["c004"] = ("L01.html [84]", "Under A0, 1+r > 1+g > 0 gives 0<q<1, q^N->0, S_N->F_t ([84]). Re-derived q=103/109, 0<q<1 True (" + DER + "). T.")
ev["c005"] = ("L01.html [91], [96]", "Prop 1.4: (A1) d_1>0, 1+g>0; (A2) r>-1, g>=r ([91]); S_N(0)->+inf and Thm 1.3 does not apply ([91], [96]). T.")
ev["c006"] = ("L01.html [105]", "Def 2.1: B_t = P_t - F_t, a bubble only when B_t>0, in cents ([105]); B_t<=0 has no bubble. Ungraded definition, matches.")
ev["c007"] = ("L01.html [111]-[114], proof [119]", "Prop 2.2 (A3) d_1>0; (A4) g<g', r>g, r>g', 1+g>0, 1+g'>0 ([112], verified text); conclusion F_0(g)<F_0(g') and the gap split ([114]). Re-derived F_0(1%)=5000 < F_0(3%)=6666.67 (" + DER + "). T.")
ev["c008"] = ("cards.json (grade removed); L01.html [289]; Key results [396]-[400]", "Round-9 FAIL subject changed: card has no grade or basis (ungraded definition like c001, c006, c020). Back matches [289] ('mechanism only ... no frequency, trigger or size'). L01 Key-results table has no Def 3.1 row any more (rows [396]-[400] are the five results).")
ev["c009"] = ("L01.html [264] (printed Part B line); [313], [132]", "Printed 'periods with price above fundamental: 9 of 13' (L01 [264]; twin output). Seeded SIMULATED draw ([313]). C, named Lab 1 Part B.")
ev["c010"] = ("L01.html [280]-[281]; [282]", "Printed '13 of 13' and 'the count changes ...: True' ([280]-[281]); 9 of 13 under 3% ([264]). C, SIMULATED.")
ev["c011"] = ("L01.html [120] witness", "d_1=400, r=9%: F_0(1%)=5000, F_0(3%)=20000/3; at P_0=6000 gaps +1000 and -2000/3 ([120]). Re-derived in " + DER + ". T.")
ev["c012"] = ("L01.html [310]; misconception [322]", "d_1=400, d_2=0, d_s=0 for s>=3, r=9%: 400/1.09 = 40000/109 -> 367 cents ([310]). Re-derived 366.97 -> 367 (" + DER + "). T.")
ev["c013"] = ("L01.html [96] proof; misconception [323]", "Under A1 and A2, each term d_1 q^(k-1)/(1+r) >= d_1/(1+r) ([96]), so S_N(0) >= N d_1/(1+r) ([96], [323]). Checked k=1..50 at g=r=9% in " + DER + ". T.")
ev["c014"] = ("L02.html [57]", "Def 1.1: parity kappa>0 grams of gold per unit of currency; convertible at parity ([57]). Ungraded, matches.")
ev["c015"] = ("L02.html [65]-[67], proof [72]", "Prop 1.2 hypothesis (A1): parity kept at every date ([65]); one gram costs 1/kappa units ([67]). T.")
ev["c016"] = ("L02.html [71]-[77]; Remark 1.3 [77]", "Prop 1.2 gives one price; (A1) does not involve P_t, so the conclusion holds whatever P_t does ([77]). T.")
ev["c017"] = ("L02.html [82]-[83]", "V_t = D P_0 / P_t, D nominal in integer cents, P_0 base value ([82]-[83]). Ungraded definition, matches.")
ev["c018"] = ("L02.html [89]-[90], [97]; Part B printed [287]", "Prop 2.1(a): (A2) D fixed positive integer cents, paid in full, not renegotiated ([89]); (A3) P_t>0 ([90]); V_t/V_(t-1) = P_(t-1)/P_t, DP_0 cancels ([97]). Identity printed True for t=1..12 ([287]). T.")
ev["c019"] = ("L02.html [92], [98]", "Prop 2.1(b): V_H/V_0 = P_0/P_H by telescoping ([98]); (A2), (A3) as in [92]. T.")
ev["c020"] = ("L02.html [110]", "Debt deflation: rise in V_t implied by a fall in P_t with D fixed; arithmetic, not a causal claim ([110]). Ungraded definition, matches.")
ev["c021"] = ("L02.html [118], proof [123]", "Cor 3.2: V_t > V_(t-1) iff P_t < P_(t-1) ([118]); proof from Prop 2.1(a) ([123]). T.")
ev["c022"] = ("L02.html [128] Remark 3.3; [97]", "Factor P_(t-1)/P_t, larger than one in a fall ([97], [128]); Cor 3.2 gives direction, not size ([128]). Back and basis as edited this round match. T.")
ev["c023"] = ("L02.html [318]-[319] (misconception 1); [118]", "Cor 3.2 gives the opposite direction: a fall in P_t raises V_t, a larger real burden ([319]). T.")
ev["c024"] = ("L02.html [83], [327]; Part B printed [274]-[286]", "Grade changed C->T this round. V_t = D P_0/P_t constant exactly when P_t constant ([327]: 'the real value is constant exactly when the index is constant, because V_t = D P_0/P_t equals V_0 = D only when P_t = P_0'); changes whenever P_t changes by Prop 2.1(a) ([97]). The one-line proof is on page; misconception 3 is its location. T accepted.")
ev["c025"] = ("L02.html Part B printed line [287]; [135]", "Printed 'identity V_t / V_(t-1) = P_(t-1) / P_t holds exactly for t = 1 to 12: True' (L02 [287]). Re-derived exact Fraction identity (twin run). C, SIMULATED.")
ev["c026"] = ("L03.html [58]-[60]", "Assumption 1.1: P_t = (1-delta)^min(t,m), P_0=1, 0<=m<=H, 0<delta<1 ([58]-[59]); deflates in periods 1..m and flat after ([60]). Ungraded definition, matches.")
ev["c027"] = ("L03.html [82]", "Def 2.1: L_t = V_t/N_t, real debt over borrower net worth ([82]). Ungraded definition, matches.")
ev["c028"] = ("L03.html [72]", "Assumption 1.3: psi_t = phi(L_t - L_0), slope phi>0 ([72]). Ungraded, matches.")
ev["c029"] = ("L03.html [87]", "Def 2.2 chain: fall in P_t raises V_t (A1, A2); raises net-worth loss (A2); leverage raises premium (A3); f_t = beta psi_t, beta>0 (A3); describes the model only ([87]). Matches card.")
ev["c030"] = ("L03.html [96], [103]", "Lemma 3.1: C = N_0 + D; ell(x) = x/(C-x) strictly increasing on [D,C); L_t = ell(V_t) whenever V_t<C; L_0 = D/N_0 ([96], proof [101]-[103]). T.")
ev["c031"] = ("L03.html [108]-[109], proof [116]", "Prop 3.2(a): V_t <= V_m for 0<=t<=H under Assumptions 1.1-1.3 including V_m < N_0+D ([66], [109]). T.")
ev["c032"] = ("L03.html [110]; proof [117]", "Prop 3.2(b): depth(m) = beta phi(ell(V_m)-ell(D)) = beta phi(V_m/(N_0+D-V_m) - D/N_0) ([110]). T.")
ev["c033"] = ("L03.html [111], [118]", "Prop 3.2(c): maximum first attained at t=m; for m>=1 no earlier period attains it ([111], proof [118]). T.")
ev["c034"] = ("L03.html [111], [118]; P2 [473]", "depth(0)=0: m=0 gives P_t=1, V_t=D, L_t=L_0, psi=0 ([118], P2 [473]). T.")
ev["c035"] = ("L03.html [125]; proof [130]", "Cor 3.3: depth(m') < depth(m) for 0<=m'<m<=H; X (m=12) deeper than Y (m'=4) ([125]); proof uses V_m' < V_m and Lemma 3.1 ([130]). T.")
ev["c036"] = ("L03.html [135]-[137]; proof [142]", "Cor 3.4: ratio = (ell(V_m)-ell(D))/(ell(V_m')-ell(D)) for 1<=m'<m<=H, independent of beta and phi ([136]-[137]); m'>=1 gives positive denominator ([142]). T.")
ev["c037"] = ("L03.html [149]; printed Part B [359]", "Printed 'economy X depth 9.20 percent ..., first reached at t = 12' ([359]); exact 9.204597 (" + DER + "). C, SIMULATED.")
ev["c038"] = ("L03.html [149]; printed Part B [360]", "Printed 'economy Y depth 2.69 percent ..., first reached at t = 4' ([360]); exact 2.686713, first maximising t = 4 ([491]; " + DER + "). C, SIMULATED.")
ev["c039"] = ("L03.html [381] (printed Part D line)", "Printed 'phi = 1, beta = 1, product 1: ratio of depths X to Y 3.4260' ([381]); exact 3.425970 -> 3.4260 (" + DER + "). C, SIMULATED; basis cites Corollary 3.4 (T).")
ev["c040"] = ("L03.html [390]", "Def 4.1: LOLR = central bank that lends against collateral to institutions solvent but illiquid ([390]). Ungraded definition, matches.")
ev["c041"] = ("L03.html [390]", "Illiquid: cannot meet payments from its own resources in the time available ([390]). Ungraded, matches.")
ev["c042"] = ("L03.html [395] Remark 4.2", "Assumption 1.2 has no lending term; Assumption 1.3 has no facility term; Prop 3.2 says nothing about a facility ([395]). T, structural.")
ev["c043"] = ("L03.html [402], [414]; Assumption 1.2 [65]-[66]", "Model has one borrower and no bank; Assumption 1.2 excludes default and balance-sheet change; the proof of Prop 3.2 uses none of these events ([414], [402]). T.")
ev["c044"] = ("L03.html [418]; [125]", "Ordering follows from parity durations 12 and 4 assigned under Assumption 1.1; model cannot say whether parity causes a deeper fall ([418]). T.")
ev["c045"] = ("L03.html [422] (misconception 3); [395]", "Def 4.1 requires collateral and solvent-but-illiquid; model has no facility (Remark 4.2 [395]). T.")
ev["c046"] = ("L03.html [426] (misconception 4); [110]; printed Part D [380]-[382]", "Lab 1 is SIMULATED; depth is the model's value at beta=1; beta phi factor in Prop 3.2(b) [110]. T.")
ev["c047"] = ("L03.html [76] honest-pending note", "No redistributable historical series embedded; lab runs the stylised model, labelled SIMULATED ([76]); curriculum lab line matches (curriculum yaml line 41). Ungraded data fact.")
ev["c048"] = ("L04.html [59]", "Def 1.1: ell_t = ln(x_t/x_(t-1)), per month, not annualized ([59]). Ungraded, matches.")
ev["c049"] = ("L04.html [59]", "Dispersion: sample sd with denominator n-1, defined only when n>=2 ([59]). Ungraded, matches.")
ev["c050"] = ("L04.html [66]-[71]", "Prop 1.2 under (A1): sum_{t=a+1}^{b} ell_t = ln(x_b/x_a); b-a terms ([66], proof [71]). T.")
ev["c051"] = ("L04.html [76]; twin SUM_TOLERANCE line", "Remark 1.3: exact in reals, checked in floats to 1e-12 ([76]); twin SUM_TOLERANCE = 1e-12 (" + "tests/labs/LX1/lab-LX1-L04-1.py). T.")
ev["c052"] = ("L04.html [92]-[100]", "Prop 2.2 under (A2), kappa>0, window n>=2: every log change 0 and dispersion 0 ([92]-[100]). T.")
ev["c053"] = ("L04.html [85]", "Def 2.1: anchor currency, one foreign currency, parity kappa>0, market rate x_t>0; fixed-parity = plus (A2) ([85]). Ungraded, matches.")
ev["c054"] = ("twin output line 'months with an exactly zero change: 3: 1976-07, 2012-07, 2019-11'; L04.html [307]", "Re-derived with exact decimals: zero months 1976-07, 2012-07, 2019-11 (" + DER + "). C, recorded fx_monthly data, Lab 1 Part B.")
ev["c055"] = ("L04.html [309] printed; [318]", "Printed 'window one ... standard deviation 0.027935' (L04 [309]); re-derived 0.027935277... with 668 changes, denominator 667 (" + DER + "). C.")
ev["c056"] = ("L04.html [312] printed; [318]", "Printed 'window two ... standard deviation 0.024700' ([312]); re-derived 0.0246995 with 321 changes (" + DER + "). C.")
ev["c057"] = ("L04.html [317] printed; [318]", "Printed ratio 0.8842 ([317]); re-derived 0.884169 (" + DER + "). C.")
ev["c058"] = ("L04.html [313] printed; [318]", "Printed '0.096575 ... at 2008-10 (signed -0.096575)' ([313]); re-derived largest window-two change 2008-10, -0.096575 (" + DER + "). C.")
ev["c059"] = ("L04.html [105], [341]", "Prop 2.2 gives zero change in the model under (A2); a recorded rate need not equal its parity (Remark 2.3, [105]); misconception 1 [341]. T.")
ev["c060"] = ("L04.html [345]; E3 [432]; printed Part D [316]", "Lab computes two sample sds and their difference; no test; no cause; window start is a convention ([345], [432]); code has no test (lab code, Part D). C, recorded fx_monthly data, Lab 1 Part D.")
ev["c061"] = ("L04.html [349], M1 [368]", "ln 1.1 = 0.0953101798 -> 0.095310; 0.1 - ln1.1 = 0.0046898 -> 0.004690 (" + DER + "). Worked calculation on page. T, judgment accepted.")
ev["c062"] = ("L04.html [81], [86], [353]; Section 4 [332]", "Def 2.1 defines a model class; L04 states no historical fact about Bretton Woods parities, participants or end; Section 4 lists what is open ([332]). T, structural.")
ev["c063"] = ("L04.html [128], [321], [330]; MANIFEST fx_daily/ust_daily", "Window two starts 2000-01 because fx_daily and ust_daily first = 2000-01-03 (MANIFEST); lab does not test other starts ([330]). Ungraded convention; matches.")
ev["c064"] = ("L04.html lab docstring [117]-[121] (twin lines 1-10); [318]", "fx_monthly.csv, G.5/H.10 Foreign Exchange Rates (noon buying rates in New York), GBP in USD per pound, each value the column's last value in its month (lab docstring; MANIFEST citation and transform). Ungraded data fact, matches.")
ev["c065"] = ("L04.html printed Part D [316]; [318]", "Printed difference -0.003236 ([316]); lesson [318] says computed from unrounded sds (subtracting printed figures gives -0.003235); re-derived -0.0032358 -> -0.003236 (" + DER + "). C.")
ev["c066"] = ("L02.html printed Part C [289]-[291]; [319]", "Printed '6 of 12' falling, '6 of 12' rising, 'True' ([289]-[291]); falling set {1,5,6,8,9,12} equals rising set (" + DER + "). C, SIMULATED.")
ev["c067"] = ("L03.html printed Part D [380]-[382]; [383]", "Printed the ratio 3.4260 for phi/beta products 1/2, 1, 3 (Part D lines [380]-[382]); the same ratio for each product ([383]). C, SIMULATED.")
ev["c068"] = ("L04.html printed Part B [307]; [318]", "Re-derived: 668 changes, 3 exactly zero, so 665 nonzero ([318]; " + DER + "). C.")
ev["c070"] = ("L04.html [122], [328]; data_sources.yaml:64; MANIFEST", "fx_monthly holds 10 exchange-rate columns; no interest-rate or forward column (header and MANIFEST columns); spot-only note (data_sources.yaml line 64; L04 [328]). Ungraded data fact.")
ev["c071"] = ("L03.html [65]", "N_t = N_0 - (V_t - V_0), whole rise in real debt falls on net worth (Assumption 1.2, [65]). Ungraded definition, matches.")
ev["c072"] = ("L03.html [73]", "depth(m) = max over 0<=t<=H of f_t, f_t = beta psi_t, fraction of baseline output (Assumption 1.3, [73]). Ungraded, matches.")
ev["c073"] = ("L02.html [82]", "Nominal debt: amount in currency units owed at each date, not indexed; here D cents ([82]). Ungraded, matches.")
ev["c074"] = ("L02.html [82]", "Price index P_t, base date 0, positive values, P_0 base value ([82]). Ungraded, matches.")
ev["c076"] = ("L03.html [390]", "Solvent: assets valued as the lender values them cover liabilities ([390]). Ungraded, matches.")
ev["c078"] = ("L02.html [57]", "Convertibility: issuer stands ready to buy and sell gold at parity on demand ([57]). Ungraded, matches.")
ev["c079"] = ("L03.html [109], proof [116]", "Prop 3.2(a) real-debt path: V_t = D(1-delta)^(-t) for t<=m, strictly increasing when m>=1; V_t = V_m for t>=m ([109], [116]). T.")
ev["c080"] = ("L03.html [390] (raw HTML: dfn def-central-bank)", "Changed this round: 'A central bank is the public institution that issues the currency.' ([390]). Front 'Definition 4.1: what is a central bank?' matches the Definition 4.1 block. Ungraded definition, matches. (Round-9 'monetary base' wording gone.)")
ev["c081"] = ("L02.html printed Part B [274]-[286]; misconception 3 [327]", "Re-derived: all 12 consecutive real values differ (1000000, 1010101, 1000100, 990198, 961357, 1001414, 1011529, 991695, 1033016, 1064965, 1033946, 1013673, 1055909 cents; no equal consecutive pair, " + DER + "). C, SIMULATED, one seeded path.")

ids = [f"LX1-c{n:03d}" for n in range(1, 82)]
for n in range(1, 82):
    cid = f"LX1-c{n:03d}"
    key = f"c{n:03d}"
    if cid in byid:
        c = byid[cid]
        loc, evidence = ev[key]
        loc = f"{CS} ({cid}); " + loc
        grade = c.get("grade", "ungraded")
        rows.append({"id": f"card-{key}", "check": f"cards.json {cid} ({c['lesson']}, grade {grade}) against the lesson text", "location": loc, "status": "PASS", "evidence": evidence})
    elif key in ("c069", "c075"):
        rows.append({"id": f"card-{key}", "check": f"card {cid} (round-9 FAIL, judgment: trivia)", "location": CS + " (no " + cid + ")", "status": "PASS",
                     "evidence": f"{cid} is absent from cards.json at pin 00a84795 (ids 69, 75, 77 missing from the 1..81 sequence; " + R + "/card_scan_r10.txt). Round-9 subject was removed by the builder, so the row is closed: no card, no claim to check. The facts it stated (row count 669, retrieval 2026-10-19) remain verified by data-manifest-facts."})
    elif key == "c077":
        rows.append({"id": "card-c077", "check": "no LX1-c077 (kept from round 9)", "location": CS, "status": "PASS",
                     "evidence": "No LX1-c077 in cards.json at pin 00a84795 (missing id, scan in card_scan_r10.txt)."})

rows.append({"id": "card-c069", "check": "", "location": "", "status": "PASS", "evidence": "x"}) if False else None
# drop the placeholder logic above (not appended)
frag = {
    "unit": "LX1",
    "slice": "LX1-d",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-d (ALL cards.json against L01-L04), round 10. Did not build LX1.",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (round-9 pin)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-LX1-d",
    "scratch": "/tmp/lx1d10 (tag-stripped lesson text, twin runs /tmp/lx1d10/run_L0x)",
    "scripts": "ledgers/LX1/scripts/LX1-d-r10/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since the round-9 pin (c93dd526): cards.json (c008 grade removed; c022, c024 back and grade edited; c069, c075 removed; c080, c081 added; c077 absent), L01.html (Proof 2 wording; Research 1 solution; Key-results row for Def 3.1 removed), L02.html (bullet and references wording), L03.html (why-it-matters; Part D print line; Def 4.1 'issues the currency'; R1 solution), L04.html (why-it-matters; Def 2.1 wording; Prop 2.2 hypothesis; R3 solution), tests/labs/LX1/lab-LX1-L03-1.py (Part D print line, matches the page). Every hunk in the slice was read. MANIFEST, fx_monthly.csv, data_sources.yaml, references.json, notation.json, tools unchanged since round 9 (not in the delta stat). Since cards.json changed, no card row is carried from round 9; every card was re-derived this round.",
        "Round-9 FAIL rows closed by fix: card-lesson-term-monetary-base (L03.html:390 now 'issues the currency'; grep finds no 'monetary base' in LX1); card-c008 (grade and basis removed, Key-results row removed); card-c069 and card-c075 (cards removed). Each is re-verified here, not carried.",
        "Judgment: LX1-c024 is graded T after round 9 graded it C. Its proof is one sentence in misconception 3 (L02 [327]) plus the identity in Section 2; accepted as a theorem on the page.",
        "Judgment: LX1-c061 (T, computed monthly log change vs simple change) rests on the worked calculation in L04 Problem M1; accepted as proved on the page.",
        "Judgment: LX1-c081 is new and graded C; the claim (every consecutive real value differs) was re-derived with exact Fractions and the page's printed block agrees.",
        "Mutants: none. This is a cards slice; no card cites a project grader (LX1 project graders are not in this slice). tools/mutate_graders.py was not run and no student-error mutant was written, as the rules apply to project slices.",
        "Not checked: hours arithmetic (hub split vs lesson hours) is not in the cards slice; check_projects.py, run_graders.py and the project lab twins were not run; verify_refs live run not run (offline only, 560 entries, 0 problems); fx_monthly licence_url not opened (data slice owns it); the curriculum's other sources (Kindleberger and Aliber; Bernanke 1983) are not cited by any lesson or card and were not checked against the registry; no visual page render was taken (not in scope for this slice).",
    ],
    "summary": "",
}
n = len(rows)
frag["summary"] = (f"Round 10 of LX1-d: {n} rows; 78 cards present (c001-c081 with ids 69, 75, 77 absent) re-derived from the pin's lesson text and lab twins; "
                   "all gate, structure and scan rows re-run this round. Verdict PASS: every row PASS. The round-9 FAIL rows (monetary base, c008 grade, c069, c075) are closed by the builder's fixes and re-verified.")
json.dump(frag, open("ledgers/LX1/LX1-d.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", n, "statuses", {s: sum(1 for r in rows if r['status'] == s) for s in ('PASS', 'FAIL', 'UNVERIFIABLE')})
