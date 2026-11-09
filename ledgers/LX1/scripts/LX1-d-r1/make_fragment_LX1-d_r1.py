"""Build ledgers/LX1/LX1-d.json (round 1 closing delta) from the round-12 base fragment.

Every base row id is kept. Card rows are re-verified from scratch where the card object or its lesson changed
since 5db69a9b (and for every L01, L03, L04 card); L02 cards are carried (object and L02.html byte-identical).
"""
import json
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyF31-LX1-d"
BASE = "/Users/billyribeiro/.fanout/frags/E-LX1-d.round12.json"
OUT = f"{ROOT}/ledgers/LX1/LX1-d.json"
PIN = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672"
BASE_PIN = "5db69a9bee460736c318ebfacc7200ee5a6eb0f0"
S = "ledgers/LX1/scripts/LX1-d-r1"

base = json.load(open(BASE, encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

CARRY_L02 = "Carried from round 12 (course/modules/LX/LX1/cards.json object {cid} and course/modules/LX/LX1/L02.html byte-identical since the previous pin 5db69a9b, git diff empty): "

RE = {
 # L01 cards (re-verified this round against L01.html, source line numbers)
 "card-c001": "Re-verified round 1: L01.html:65-67 Definition 1.2 (F_t = sum d_(t+k)/(1+r)^k, 'whenever the series converges', 'not a forecast'); card matches.",
 "card-c002": "Re-verified round 1: L01.html:72-74 Theorem 1.3 (A0, A1; F_t = d_1(1+g)^t/(r-g) = d_(t+1)/(r-g); F_0 = d_1/(r-g)); the convergence clause was removed from the back, the statement still holds (L01.html:72).",
 "card-c003": "Re-verified round 1: L01.html:74 S_N(t) = F_t(1-q^N) for every N>=1; Lab 1 Part A prints the identity True for N=10, 60, 200 (out_L01.txt lines 1-6, output equal to page expected block).",
 "card-c004": "Re-verified round 1: L01.html:83-84 (1-q = (r-g)/(1+r) > 0 and 0<q<1 under A0; q^N -> 0); recomputed 1-q = (r-g)/(1+r).",
 "card-c005": "Re-verified round 1: L01.html:91 Proposition 1.4 hypotheses (A1 with d_1>0, 1+g>0; A2 r>-1, g>=r) and conclusion S_N(0) -> +infinity; proof line 96.",
 "card-c006": "Re-verified round 1: L01.html:105 Definition 2.1 with A_t (ruling 16 notation, P_t replaced) B_t = A_t - F_t counted only when B_t>0, in cents; no card-lesson mismatch.",
 "card-c007": "Re-verified round 1: L01.html:111-114 Proposition 2.2 hypotheses (A3) d_1>0, (A4) g<g', r>g, r>g', 1+g>0, 1+g'>0; conclusion line 114 F_0(g)<F_0(g'); card back is the conclusion only, which is the line-114 conclusion.",
 "card-c008": "Re-verified round 1: L01.html:290 Definition 3.1 (mechanism only; 'does not say how often, what triggers, how large'); card matches.",
 "card-c009": "Re-verified round 1: lab output 'periods with price above fundamental: 9 of 13' (L01.html:265; out_L01.txt; expected block equals twin output, lab_compare.txt).",
 "card-c010": "Re-verified round 1: lab output L01.html:281-282 '13 of 13' and 'the count changes ... True'; 9 of 13 at line 265.",
 "card-c011": "Re-verified round 1: L01.html:120 witness: F_0(1%)=5000, F_0(3%)=20000/3; price 6000 gives +1000 and -2000/3 (recomputed in recompute_r1.txt).",
 "card-c012": "Re-verified round 1: L01.html:311 Section 5 bullet: d_1=400, d_2=0, d_s=0 for s>=3, r=9%: 400/1.09 = 40000/109 = 366.97, rounds to 367 (recompute_r1.txt); misconception 2 at line 323.",
 "card-c013": "Re-verified round 1: L01.html:96 proof of Proposition 1.4 (q>=1, each term >= d_1/(1+r) > 0); misconception 3 at line 324.",
 "card-c085": "Re-verified round 1 (new card): L01.html:352-353 Proof 2 (Assumption 1.1 gives F_t = (1+g) F_(t-1) for t>=1, using 1+g>0 from A0); section 7 is 'Problem set' (L01.html:329).",
 "card-c086": "Re-verified round 1 (new card): L01.html:119 proof of Proposition 2.2: r-g > r-g' > 0 gives 1/(r-g) < 1/(r-g'), and d_1>0 (A3) keeps the order; matches.",
 "card-c092": "Re-verified round 1 (new card): L01.html:91, 96 and misconception 3 at line 324: at g=r undefined, at g>r negative; 400/(0.09-0.10) = -40000 cents (recompute_r1.txt) matches line 324.",
 "card-c093": "Re-verified round 1 (new card): L01.html:111-114 and 119: F_0(g) < A_0 <= F_0(g') gives gap A_0 - F_0(g) > 0 and A_0 - F_0(g') <= 0 (matches Proposition 2.2 conclusion, line 114).",
 # L03 cards
 "card-c026": "Re-verified round 1: L03.html:58-60 Assumption 1.1: P_t = (1-delta)^min(t,m), P_0 = 1, flat after m; card matches.",
 "card-c027": "Re-verified round 1: L03.html:82 Definition 2.1 L_t = V_t/K_t (K replaces N); card matches.",
 "card-c028": "Re-verified round 1: L03.html:72 Assumption 1.3 psi_t = phi(L_t - L_0), phi>0; card matches.",
 "card-c029": "Re-verified round 1: L03.html:87 Definition 2.2 chain (A1, A2, A3) and 'describes the model'; card matches.",
 "card-c030": "Re-verified round 1: L03.html:96 Lemma 3.1 (A1 and A2 so K_0>0; C = K_0 + D; lambda(x) = x/(C-x); L_t = lambda(V_t) for V_t<C, L_0 = D/K_0); card matches the statement.",
 "card-c031": "Re-verified round 1: L03.html:66, 109 Proposition 3.2(a) (V_m < K_0 + D in Assumption 1.2; conclusion V_t <= V_m for 0<=t<=H); card matches.",
 "card-c032": "Re-verified round 1: L03.html:110 Proposition 3.2(b): depth(m) = beta phi(lambda(V_m) - lambda(D)) = beta phi(V_m/(K_0+D-V_m) - D/K_0); card matches.",
 "card-c033": "Re-verified round 1: L03.html:111 and proof 118 Proposition 3.2(c): maximum first attained at t=m; no earlier period when m>=1; card matches.",
 "card-c034": "Re-verified round 1: L03.html:473 Problem P2 (m=0 gives P_t=1, V_t=D, K_t=K_0, premium 0, depth 0) and Proposition 3.2(c) line 111; card matches.",
 "card-c035": "Re-verified round 1: L03.html:125 Corollary 3.3 hypotheses (two economies sharing D, K_0, delta, phi, beta; 0<=m'<m<=H) and conclusion; proof 130; X (m=12) deeper than Y (m'=4) per Part B.",
 "card-c036": "Re-verified round 1: L03.html:135-137 Corollary 3.4 (1<=m'<m<=H; ratio = (lambda(V_m)-lambda(D))/(lambda(V_m')-lambda(D)), independent of beta, phi); card matches.",
 "card-c037": "Re-verified round 1: L03.html:359 'economy X depth 9.20 percent of baseline output'; exact 9.204597 (recompute_r1.txt) rounds to 9.20.",
 "card-c038": "Re-verified round 1: L03.html:360 'economy Y depth 2.69 percent'; exact 2.686713 (recompute_r1.txt) rounds to 2.69.",
 "card-c039": "Re-verified round 1: L03.html:381 Part D 'product 1: ratio of depths X to Y 3.4260'; exact ratio 3.425970 (recompute_r1.txt) rounds to 3.4260.",
 "card-c040": "Re-verified round 1: L03.html:390 Definition 4.1 (central bank lends against collateral to institutions solvent but illiquid); card matches.",
 "card-c041": "Re-verified round 1: L03.html:390 Definition 4.1 illiquid = cannot meet payments from own resources in the time available; card matches.",
 "card-c042": "Re-verified round 1: L03.html:395 Remark 4.2 (no lending term in Assumption 1.2 or 1.3); card matches.",
 "card-c043": "Re-verified round 1: L03.html:414 misconception 1 ('The model has no bank and no failure'); Assumption 1.2 excludes default; card matches.",
 "card-c044": "Re-verified round 1: L03.html:418 misconception 2 (ordering follows from durations 12 and 4; cannot say whether parity causes deeper fall); card matches.",
 "card-c045": "Re-verified round 1: L03.html:422 misconception 3 and Definition 4.1 / Remark 4.2 at line 395; card matches.",
 "card-c046": "Re-verified round 1: L03.html:426 misconception 4 (SIMULATED, beta=1, no output series); Proposition 3.2(b) factor beta phi; card matches.",
 "card-c047": "Re-verified round 1: L03.html:76 honest-pending note (no redistributable historical series embedded; lab stays SIMULATED); card matches.",
 "card-c067": "Re-verified round 1: L03.html:381-382 Part D prints 3.4260 for each product (1/2, 1, 3); Corollary 3.4 at line 135-137; card matches.",
 "card-c071": "Re-verified round 1: L03.html:65 Assumption 1.2 K_t = K_0 - (V_t - V_0); card matches.",
 "card-c072": "Re-verified round 1: L03.html:73 depth(m) = max over 0<=t<=H of f_t; Assumption 1.3 f_t = beta psi_t (line 72); card matches.",
 "card-c076": "Re-verified round 1: L03.html:390 Definition 4.1 solvent (assets valued as the lender values them cover liabilities); card matches.",
 "card-c079": "Re-verified round 1: L03.html:109 and proof 116 Proposition 3.2(a): V_t = D(1-delta)^(-t) for t<=m, strictly increasing when m>=1, V_t = V_m for t>=m; card matches.",
 "card-c080": "Re-verified round 1: L03.html:390 Definition 4.1 central bank = public institution that issues the currency; card matches.",
 "card-c082": "Re-verified round 1: L03.html:66-67 Assumption 1.2 (V_m < K_0 + D) and Remark 4.2 at line 395 (V_t <= V_m gives V_t < K_0 + D and K_t > 0); card matches.",
 "card-c087": "Re-verified round 1 (new card): L03.html:102 Lemma 3.1 proof: lambda(y)-lambda(x) = C(y-x)/((C-x)(C-y)) > 0 for D<=x<y<C; recomputed symbolically.",
 "card-c090": "Re-verified round 1 (new card): L03.html:359 'first reached at t = 12' (Part B) and Proposition 3.2(c) at line 111; matches.",
 "card-c091": "Re-verified round 1 (new card): L03.html:360 'first reached at t = 4' (Part B) and Proposition 3.2(c) at line 111; premium flat after period 4 (L03.html:350-357).",
 # L04 cards
 "card-c048": "Re-verified round 1: L04.html:59 Definition 1.1 ell_t = ln(x_t/x_(t-1)), per month, not annualized; card matches.",
 "card-c049": "Re-verified round 1: L04.html:59 Definition 1.1 dispersion = sample sd with denominator n-1 about the mean; the n>=2 condition moved to card c088, which matches line 59.",
 "card-c050": "Re-verified round 1: L04.html:66 Proposition 1.2 sum_{t=a+1}^{b} ell_t = ln(x_b/x_a), b-a terms; card matches.",
 "card-c051": "Re-verified round 1: L04.html:76 Remark 1.3 (exact in reals; lab checks to 1e-12); twin SUM_TOLERANCE = 1e-12 at tests/labs/LX1/lab-LX1-L04-1.py:48; card matches.",
 "card-c052": "Re-verified round 1: L04.html:92 Proposition 2.2 hypotheses (A2 with xbar>0, n>=2) and conclusion lines 94; proof 99-100; card matches.",
 "card-c053": "Re-verified round 1: L04.html:85 Definition 2.1 (anchor currency; one foreign currency; fixed exchange rate xbar>0; market rate x_t>0 in the same units); card matches.",
 "card-c054": "Re-verified round 1: L04.html:312 'months with an exactly zero change: 3: 1976-07, 2012-07, 2019-11' (lab_compare.txt: expected equals output).",
 "card-c055": "Re-verified round 1: L04.html:314 window one sd 0.027935, 668 changes; recompute_r1.txt sd1 = 0.027935277917784617.",
 "card-c056": "Re-verified round 1: L04.html:317 window two sd 0.024700, 321 changes; recompute_r1.txt sd2 = 0.024699501387683342.",
 "card-c057": "Re-verified round 1: L04.html:322 ratio 0.8842; recompute_r1.txt ratio = 0.8841688 -> 0.8842.",
 "card-c058": "Re-verified round 1: L04.html:318 largest absolute change window two 0.096575 at 2008-10, signed -0.096575; recompute_r1.txt max2 = ('2008-10', -0.0965747).",
 "card-c059": "Re-verified round 1: L04.html:92, 105 Proposition 2.2 under (A2) and Remark 2.3 (model, not a recorded rate; xbar replaces kappa); card matches.",
 "card-c060": "Re-verified round 1: L04.html:350 misconception 2; L04.html:437 Problem E3 (no test, no inference); lab computes no test (twin code); card matches.",
 "card-c061": "Re-verified round 1: L04.html:354 misconception 3 (ln 1.1 = 0.095310; difference 0.004690) and Problem M1 at L04.html:373; recompute_r1.txt 0.1-ln1.1 = 0.0046898.",
 "card-c062": "Re-verified round 1: L04.html:357-358 misconception and Section 4 (L04.html:337) state no historical fact; card matches (fixed exchange rates wording).",
 "card-c063": "Re-verified round 1: L04.html:129-130 (window two starts where fx_daily and ust_daily begin, both 2000-01-03 in MANIFEST.json); card matches.",
 "card-c064": "Re-verified round 1: L04.html:117-121 twin docstring and L04.html:114 (fx_monthly.csv, Board G.5/H.10, GBP in USD per pound); MANIFEST.json fx_monthly entry.",
 "card-c065": "Re-verified round 1: L04.html:321 'difference in standard deviation: -0.003236'; L04.html:323 says computed from unrounded values; recompute_r1.txt diff = -0.0032357765.",
 "card-c068": "Re-verified round 1: L04.html:312 (3 zero changes of 668) and L04.html:323 (665 nonzero); card matches.",
 "card-c070": "Re-verified round 1: CSV header of course/assets/data/market/fx_monthly.csv is month,AUD,CAD,CHF,DKK,EUR,GBP,JPY,NOK,NZD,SEK (exchange-rate columns only); tools/data_sources.yaml:50-66 'Spot rates only'; L04.html:122-123 and 333 match.",
 "card-c083": "Re-verified round 1 (new card): L04.html:85-86 Definition 2.1 with (A2) fixed rate held (x_t = xbar from the month before the first change to the last); Remark 2.3 at line 105; matches.",
 "card-c084": "Re-verified round 1 (new card): L04.html:334 monthly value = last value in month (MANIFEST transform, line 'month-end'); the 'not the monthly average the Board publishes' claim is supported by tools/data_sources.yaml fx_monthly note: 'the release's own monthly series are monthly averages'.",
 "card-c088": "Re-verified round 1 (new card): L04.html:59 Definition 1.1 'defined only when n >= 2' and denominator n-1; matches.",
 "card-c089": "Re-verified round 1 (new card): L04.html:315 window one largest absolute change 0.135846 at 1985-03 (signed 0.135846); recompute_r1.txt max1 = ('1985-03', 0.1358457).",
}

NONCARD = {
 "gate-check-pages": "Re-run round 1 at 95f3f8cb: .venv/bin/python tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS' (ledgers/LX1/scripts/LX1-d-r1/out/check_pages_LX1.txt, exit 0). Cards schema and ids checked by the tool.",
 "gate-check-dag": "Re-run round 1: .venv/bin/python tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS' (out/check_dag_LX1.txt, exit 0).",
 "gate-run-labs": "Re-run round 1: .venv/bin/python tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)' (out/run_labs.txt, exit 0). Also lab_compare.txt: each L01, L03, L04 twin under python -I -W error exits 0 with empty stderr; page code equals twin; output equals the page expected block.",
 "gate-page-smoke": "Re-run round 1: .venv/bin/python tools/page_smoke.py --unit LX1 --pages L01 L02 L03 L04 --skip-labs -> L01..L04 PASS, 'page_smoke LX1: PASS' (out/page_smoke.txt, exit 0).",
 "gate-verify-refs-offline": "Re-run round 1: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs.txt). The --unit live run was not run.",
 "gate-mypy-ruff-pytest": "Re-run round 1 (the twins changed): ruff check course tools tests/labs/LX1 -> 'All checks passed!' (out/ruff_check.txt); ruff format --check tests/labs/LX1 -> '7 files already formatted'; mypy --no-incremental tests/labs/LX1 -> 'Success: no issues found in 7 source files' (out/mypy_twins.txt); pytest tests/test_page_checks.py tests/test_run_labs.py -> exit 0; pytest tests/test_labs.py -k LX1 -> 7 passed, exit 0. Out of this slice: tests/test_lx1_project_lab3.py has 1 failing test (see notes); tests/labs/LX1 contains no test module (pytest exit 5).",
 "gate-notation": "Re-verified round 1: notation/notation.json symbols are T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (none changed); grep of LX1 pages and cards finds none of them. New symbols used this delta: K_t (net worth), lambda(x), xbar, A_t, z, h, G; none is registered, none collides with a registered meaning. Ell is now used only as a log change (L04); the L03 ell of the base round was renamed lambda.",
 "gate-dag": "Re-verified round 1: check_dag LX1 PASS (out/check_dag_LX1.txt). Card text scanned for other-unit identifiers (E1-E5, M1-M9, C*, S*, AP1, FC*, DV*): only L04 Problem E3 and Problem M1 in card c060 and c061, both in L04.",
 "data-manifest-facts": "Carried from round 12 (course/assets/data/market byte-identical since the previous pin 5db69a9b; git diff empty; sha256 of fx_monthly.csv matches MANIFEST as recorded in round 12): MANIFEST fx_monthly retrieved 2026-10-19, rows 669 1971-01..2026-09.",
 "data-register-note": "Re-verified round 1: tools/data_sources.yaml fx_monthly note (lines 50-66) reads 'Each value is the last noon rate of its month, sampled from the daily series (the release's own monthly series are monthly averages). ... Spot rates only, as for fx_daily.' This supports L04.html:334 and 333 and card c084.",
 "lesson-curriculum-claims": "Re-verified round 1: curriculum/06-profession-capstone.yaml byte-identical since 5db69a9b (git diff empty). sed -n '25p;41p' prints the Dutch Republic to 2008 sentence (line 25) and the lab title 'Gold-standard adherence vs. depression depth on embedded data' (line 41); L01 Section 4 and L03 honest-pending note are consistent with it.",
 "registry-citations": "Re-verified round 1 with a script over references/references.json (changed since the pin only by generated_at and the black-scholes entry's used_by, which is not an LX1 key): eichengreen1992golden 'Golden fetters: the gold standard and the Great Depression, 1919-1939' (1992); friedman1963monetary 'A monetary history of the United States 1867-1960' (1963); garber2000famous 'Famous First Bubbles: The Fundamentals of Early Manias' (2000). Lesson citations: L01.html:304 and 489 (Garber, title only), L02.html (Eichengreen), L03.html:640 (Friedman, book level only), each matching.",
 "card-coverage": "Re-verified round 1: every Definition, Theorem, Proposition, Lemma, Corollary and misconception of L01 (Defs 1.2, 2.1, 3.1; Thm 1.3; Props 1.4, 2.2; misconceptions 1-3), L03 (Assumptions 1.1-1.3; Defs 2.1, 2.2, 4.1; Lemma 3.1; Props 3.2(a)-(c); Cors 3.3, 3.4; Remark 4.2; misconceptions 1-4) and L04 (Defs 1.1, 2.1; Props 1.2, 2.2; Remark 1.3; misconceptions 1-4) has a card. Cards: L01 17, L02 17, L03 32, L04 24 = 90.",
 "scan-duplicates": "Re-verified round 1: 90 cards, 90 unique ids, 90 unique fronts (cards_cur_dump.txt). difflib front ratio > 0.6 pairs reviewed; the closest (c037/c038, c090/c091, c055/c056, c035/c036, c018/c019, c009/c010, c057/c065, c058/c089, c041/c076) each ask a different fact (another economy, window, corollary, part or sign). c053/c083 both describe Definition 2.1: c053 asks its contents, c083 asks the model with (A2); distinct facts, no duplicate.",
 "scan-process-words": "Re-verified round 1: scan of card fronts and backs and of L01, L03, L04 text for revis|verif|builder|batch|round|previous|earlier|corrected|renamed|changed|fix|now|updated gives only domain uses ('fixed nominal debt', 'fixed exchange rate', 'what a gold standard fixes', 'agreed now for delivery'). No process word.",
 "grade-scan": "Re-verified round 1: grades T 41, C 20, none 29 (cards_cur_dump.txt; script in card audit). Every T card has a basis (proof, proposition, worked calculation or remark). Every C card names a SIMULATED lab output or an embedded-data output: c009, c010, c025, c037, c038, c039, c054-c058, c060, c065-c068, c081, c089-c091. The 29 ungraded cards are definitions or factual claims about code and data (c047, c063, c064, c070, c084).",
 "card-lesson-term-monetary-base": "Re-verified round 1: grep 'monetary base' over course/modules/LX/LX1/cards.json returns 0 hits; the L03 solvency and illiquidity terms are defined at L03.html:390 (Definition 4.1), which cards c040, c041, c076, c080 take them from.",
 "card-numbers": "Re-verified round 1 (script in out/): 305 number tokens across the 90 cards; each token appears in its own lesson text (lab outputs included) or, for L02 cards, in L02; 0 missing.",
 "lab-text-compare": "Re-verified round 1: lab_compare.txt. L01, L03, L04 twins under python -I -W error: exit 0, stderr empty, page code equals the twin (L01 5663 chars, L03 8548, L04 9404), output equals the page expected block (L01 38 lines, L03 56, L04 17). Every number a card quotes from a lab is on a printed line (out_L01.txt, out_L03.txt; L04 expected block).",
 "recompute-l04-cards": "Re-verified round 1 (recompute_r1.txt, own script on course/assets/data/market/fx_monthly.csv): 669 rows 1971-01..2026-09; 668 changes; exact-zero months 1976-07, 2012-07, 2019-11; window one sd 0.027935277917784617 (n=668); window two sd 0.024699501387683342 (n=321); ratio 0.8841688 -> 0.8842; difference -0.0032357765 -> -0.003236; largest window-one 0.1358457 at 1985-03; largest window-two -0.0965747 at 2008-10.",
 "card-claims-recompute": "Re-verified round 1 (recompute_r1.txt): F_0 = 20000/3 -> 6667; q = 103/109; 400/1.09 = 366.97 -> 367; ln 1.1 = 0.0953102, 0.1 - ln 1.1 = 0.0046898; 400/(0.09-0.10) = -40000; 250/0.06 = 4166.67 -> 4167; 250*1.04^3/0.06 = 4686.93 -> 4687; 9/13 = 0.6923; 2175/8698 = 0.250057 -> 25.01%; 8698.49 fundamental at t=9; g* = 0.0233333; L_4 = 0.2768671 -> 0.2769; V_12 X = 1274345.2124 -> 1274345; depth X 9.204597, Y 2.686713, difference 6.517884 -> 6.52, ratio 3.425970 -> 3.4260; simple change at 2008-10 = -0.0920579 -> -0.092058; h = tanh(0.0679227) = 0.0678187 -> 0.067819; bound at h=0.0678 = 0.1358084 -> 0.135808.",
 "delta-hunks": "Re-verified round 1: git diff 5db69a9b..95f3f8cb over the slice paths: course/modules/LX/LX1/L01.html (55 lines), L03.html (88), L04.html (92), cards.json (161), tests/labs/LX1/lab-LX1-L01-1.py, L03, L04, references/references.json (generated_at; one non-LX1 used_by), and project.html plus lab-LX1-project-3.py (outside this slice; no card cites them). Every hunk of L01, L03, L04, the three twins and cards.json was read; the changes are notation (P_t->A_t in L01 per ruling 16, N->K, ell->lambda, kappa->xbar), wording, and the new cards c083-c093.",
 "round11-fragment": "Round-11 fragment: ~/.fanout/frags/E-LX1-d.round11.json is absent (listing shows rounds 1-10 and 12 only), as the round-12 notes say. The delta base is the round-12 fragment (pin 5db69a9b). Nothing to verify; no finding.",
 "mutants": "Not a project slice. Ruling 37: a closing round authors no new mutants; the standing mutant set for this slice is empty (base mutants []). Nothing to re-run.",
 "card-c069": "No card with id LX1-c069 exists in cards.json at 5db69a9b or at 95f3f8cb (ids need not be sequential, ruling 2). Nothing to verify; carried from round 12.",
 "card-c075": "No card with id LX1-c075 exists in cards.json at 5db69a9b or at 95f3f8cb (ids need not be sequential, ruling 2). Nothing to verify; carried from round 12.",
 "card-c077": "No card with id LX1-c077 exists in cards.json at 5db69a9b or at 95f3f8cb (ids need not be sequential, ruling 2). Nothing to verify; carried from round 12.",
}

L02_CARDS = ["card-c014","card-c015","card-c016","card-c017","card-c018","card-c019","card-c020","card-c021","card-c022",
             "card-c023","card-c024","card-c025","card-c066","card-c073","card-c074","card-c078","card-c081"]

rows = []
for rid, brow in base_rows.items():
    if rid in L02_CARDS:
        cid = rid.replace("card-", "LX1-")
        ev = CARRY_L02.format(cid=cid) + brow["evidence"]
        rows.append({"id": rid, "check": brow["check"], "location": brow["location"], "status": "PASS", "evidence": ev})
    elif rid in RE:
        rows.append({"id": rid, "check": brow["check"], "location": brow["location"], "status": "PASS", "evidence": RE[rid]})
    elif rid in NONCARD:
        rows.append({"id": rid, "check": brow["check"], "location": brow["location"], "status": "PASS", "evidence": NONCARD[rid]})
    else:
        raise SystemExit(f"row {rid} has no round-1 evidence")

NEW_IDS = ["card-c083","card-c084","card-c085","card-c086","card-c087","card-c088","card-c089","card-c090","card-c091","card-c092","card-c093"]
for rid in NEW_IDS:
    rows.append({"id": rid, "check": "2.7 card vs lesson (new card this delta)", "location": f"course/modules/LX/LX1/cards.json (LX1-{rid[5:]})",
                 "status": "PASS", "evidence": RE[rid]})

order = [r["id"] for r in base["rows"]] + NEW_IDS
by = {r["id"]: r for r in rows}
rows = [by[i] for i in order]
missing = [i for i in base_rows if i not in by]
assert not missing, missing

frag = {
 "unit": "LX1",
 "slice": "LX1-d",
 "round": 1,
 "verifier": "Claude Haiku 5.5, independent verifier for LX1-d (closing delta, ruling 30), round 1. Did not build LX1.",
 "pin": PIN,
 "base": f"{BASE_PIN} (round-12 pin, fragment ~/.fanout/frags/E-LX1-d.round12.json, verdict PASS, 106 rows). Delta: git diff {BASE_PIN[:8]}..{PIN[:8]}.",
 "checkout": ROOT,
 "scratch": "/Users/billyribeiro/.fanout/scratch-LX1-d-r1 (line-numbered plain-text dumps L01-L04.txt, lab outputs, chk/recompute_r1.py)",
 "scripts": S + "/",
 "verified_at": subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%S+00:00"], capture_output=True, text=True).stdout.strip(),
 "verdict": "PASS",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Scope (ruling 30): slice d is cards.json against L01-L04 and their twins. Changed subjects were re-verified from scratch: 24 changed cards (c002, c006, c007, c013, c027, c030-c032, c035-c038, c049, c052, c053, c058, c059, c062-c064, c067, c070, c071, c082), 11 new cards (c083-c093), and every other L01, L03 and L04 card, because each cites a lesson whose text changed (notation P_t->A_t, N->K, ell->lambda, kappa->xbar and wording). The 17 L02 cards are carried: cards.json objects and L02.html are byte-identical since 5db69a9b.",
  "Closing-round rule (ruling 37): no new mutants written. Mutant set for this non-project slice is empty.",
  "OUT OF SLICE, route to the LX1 project slice owner: tests/test_lx1_project_lab3.py::test_a_population_sd_variant_of_the_two_pass_check_raises FAILS at this pin (out/pytest_lx1_project_lab3.txt). Cause: commit 4540351d removed the statistics.stdev agreement check from tests/labs/LX1/lab-LX1-project-3.py (and project.html no longer states it), but the test still asserts that the check raises. Either the test is stale and must be retired or rewritten, or the check must be restored; this verifier did not change either file. The other two tests in that module pass. Slice LX1-d does not depend on this.",
  "Observation (not a finding): L03 Lemma 3.1 lists hypotheses A1 and A2 only, but uses L_t = V_t/K_t, defined in Assumption 1.3 and Definition 2.1. The identity L_t = lambda(V_t) needs no A3, so the omission is harmless.",
  "Observation: the L03 Lab 1 title and honest-pending note do not match the curriculum lab title ('Gold-standard adherence vs. depression depth on embedded data', curriculum/06-profession-capstone.yaml:41). L03.html:76 states the lab is SIMULATED and that no redistributable series is embedded; this is a disclosed gap, not a card defect.",
  "Not checked: the full gate chain (mypy over all tooling, the complete pytest suite, verify_refs --unit live run, fetch_data --check, render_curriculum, build_site --check, run_graders, mutate_graders, check_projects, the hub and project pages) because they belong to other slices; the L02 lesson text itself was not re-read this round (unchanged, carried); the MANIFEST rebuild from the live feed (no curl used); the hours arithmetic against the hub (hub not in slice); project.html and lab-LX1-project-3.py were not audited for slice d.",
 ],
 "summary": "LX1-d closing delta (round 1, pin 95f3f8cb, base 5db69a9b): 117 rows, all PASS. 73 non-L02 card rows re-verified from scratch against L01, L03, L04 with line citations; 11 new cards verified; 17 L02 cards carried (byte-identical). Gates re-run on this pin: check_pages, check_dag, run_labs 7/7, page_smoke L01-L04, verify_refs --offline, ruff, mypy on tests/labs/LX1, pytest test_page_checks, test_run_labs, test_labs -k LX1; lab twins compared to page expected blocks. One out-of-slice failing test (project lab 3) is routed to its slice owner in notes.",
}

json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
open(OUT, "a", encoding="utf-8").write("\n")
print("wrote", OUT, len(rows), "rows")
