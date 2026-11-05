"""Writes the LX1-b round-7 verification fragment (rows and summary). Run from the checkout root with the project venv."""
import json, pathlib
OUT = "ledgers/LX1/scripts/LX1-b-r7/out/"
S = "ledgers/LX1/scripts/LX1-b-r7/"
CARRY = "Carried from round 6 (course/assets/data/market/fx_monthly.csv and MANIFEST.json byte-identical since 4bd8cb9; CSV sha256 re-checked this round against MANIFEST): "
R = []
def row(i, check, loc, status, ev, fix=None):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)

row("lx1b-check-pages", "2.9 structure", "course/modules/LX/LX1/L03.html; L04.html", "PASS",
    "tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS' (" + S + "out/check_pages.out).")
row("lx1b-check-dag", "2.9 DAG", "course/modules/LX/LX1/L03.html; L04.html", "PASS",
    "tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS' (" + S + "out/check_dag.out). Note: the pass depends on the pending dfn at L04.html:86, see lx1b-L04-bretton-definition.")
row("lx1b-dag-links", "2.9 DAG links", "L03.html:37, :54, :90; L04.html:37, :105, :331", "PASS",
    "Every href anchor resolves: L02.html#def-debt-deflation and #def-gold-standard (1 match each in L02.html); L03.html#def-lender-of-last-resort and #def-central-bank (1 each); concepts.html#exponential-and-logarithm (1 match); project.html exists.")
row("lx1b-dag-outside-closure", "2.9 DAG closure", "L03.html:51, :65, :90; L04.html:328", "PASS",
    "Prerequisite closure {E1,E5,FC1,M1,M2,P0.1} (plans/LX1-build-plan.md:45). covered-interest-parity is owned by E8 (curriculum.json concepts); L04.html:328 names it in plain prose with no link and no data-concept, as plan section 4 D5 prescribes.")
row("lx1b-run-labs", "2.5 labs", "tests/labs/LX1/lab-LX1-L03-1.py; lab-LX1-L04-1.py", "PASS",
    "tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)' (" + S + "out/run_labs.out).")
row("lx1b-twin-alone-L03", "2.5 labs", "tests/labs/LX1/lab-LX1-L03-1.py", "PASS",
    "Run alone: python -I -W error <twin> from /tmp/lx1b-r7/L03 (data copied): exit 0, empty stderr (" + S + "out/twin_L03.out, twin_L03.err). Printed values checked by recompute_L03.py (" + S + "out/recompute_L03.out).")
row("lx1b-twin-alone-L04", "2.5 labs", "tests/labs/LX1/lab-LX1-L04-1.py", "PASS",
    "Run alone: python -I -W error <twin> from /tmp/lx1b-r7/L04 (data/fx_monthly.csv copied): exit 0, empty stderr (" + S + "out/twin_L04.out, twin_L04.err). A first run from the checkout root failed with FileNotFoundError 'data/fx_monthly.csv' because the twin reads a cwd-relative path; that is a harness setting, not a lab defect.")
row("lx1b-twin-equals-page-code", "2.5 labs", "L03.html data-run block; L04.html data-run block", "PASS",
    "twin_page_compare.py: page code equals the twin up to one trailing newline (the twin ends with '\\n', the page block ends at 'main()</code>'); expected blocks equal the live output of both twins exactly (" + S + "out/twin_page_compare.out).")
row("lx1b-page-smoke-L03", "2.9 / 2.5 page_smoke", "course/modules/LX/LX1/L03.html", "PASS",
    "tools/page_smoke.py --unit LX1 --pages L03 L04 -> 'page_smoke modules/LX/LX1/L03.html: PASS' (" + S + "out/page_smoke_L03_L04.out). The page filter takes stems, so a first run with 'L03.html' selected no pages and was discarded.")
row("lx1b-page-smoke-L04", "2.9 / 2.5 page_smoke", "course/modules/LX/LX1/L04.html", "PASS",
    "Same run: 'page_smoke modules/LX/LX1/L04.html: PASS' (" + S + "out/page_smoke_L03_L04.out).")
row("lx1b-ruff-mypy", "2.5 gates", "tests/labs/LX1/lab-LX1-L03-1.py; lab-LX1-L04-1.py", "PASS",
    "ruff check: 'All checks passed!'; ruff format --check: '2 files already formatted'; mypy --no-incremental: 'Success: no issues found in 2 source files' (" + S + "out/ruff.out, mypy.out).")
row("lx1b-pytest", "gates", "tests/test_labs.py; tests/test_page_checks.py; tests/test_docs_figures.py", "PASS",
    "pytest tests/test_labs.py tests/test_page_checks.py tests/test_docs_figures.py -q: exit 0 (" + S + "out/pytest_full_three.out).")
row("lx1b-verify-refs", "2.1 citations", "references/references.json; L03.html data-cite friedman1963monetary", "PASS",
    "tools/verify_refs.py --offline: '560 entries, 0 problems'; tools/verify_refs.py --unit LX1 (live): '3 of 560 entries, 0 problems'. Registry unchanged by the run (git status clean for references/).")
row("lx1b-fetch-check", "2.8 data", "course/assets/data/market/fx_monthly.csv; MANIFEST.json", "PASS",
    "tools/fetch_data.py --check: '3 datasets, 0 problems' (" + S + "out/fetch_check.out).")
row("lx1b-fx-rebuild", "2.8 data reproducibility", "course/assets/data/market/fx_monthly.csv; MANIFEST.json", "PASS",
    CARRY + "shasum -a 256 of fx_monthly.csv = 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e, equal to the MANIFEST fx_monthly sha256 (re-checked this round). The live --fetch rebuild was not repeated this round.")
row("lx1b-fx-licence", "2.8 licence", "tools/data_sources.yaml fx_monthly; MANIFEST.json fx_monthly licence_url; L04.html:114, :568", "PASS",
    "MANIFEST licence_url https://www.federalreserve.gov/disclaimer.htm; plain curl -> HTTP 200 (" + S + "out/licence_curl.out) and the page contains 'public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.', the quoted MANIFEST licence text. Redistribution is granted.")
row("lx1b-fx-guard", "2.5 honest data", "tests/labs/LX1/lab-LX1-L04-1.py load_column, parse_rate, month_index", "PASS",
    "scripts/guard_L04.sh (out/guard_L04.out): blank cell, skipped month, missing column and exponent-form cell each raise ValueError; no row is skipped or filled.")
row("lx1b-fx-gbp-clean", "2.8 data", "course/assets/data/market/fx_monthly.csv (GBP column)", "PASS",
    "recompute_L04.py asserts every one of the 669 GBP cells is a plain decimal (no blank, no exponent); header GBP present (out/recompute_L04.out).")
row("lx1b-num-L03-depth", "2.2 numbers", "L03.html:149, :359-362, :383, :487-491, :545-546, :574-577, :593-596, :610", "PASS",
    "recompute_L03.py (exact Fractions): depth X 9.204597% first t=12; depth Y 2.686713% first t=4; X-Y 6.517884 -> 6.52, printed difference 6.51; ratio 3.425970 -> 3.4260; V_12 = 1274345.2124 cents (out/recompute_L03.out). All match the page.")
row("lx1b-num-L03-path", "2.2 numbers", "L03.html expected block (327-382), M1-M3 (439-455), E3 (505), quiz (607-611)", "PASS",
    "Every index, real debt, leverage, premium and fall value in both economy tables equals recompute_L03.out at the printed precision (e.g. t=4 leverage 0.276867 -> 0.2769, psi 0.026867 -> 0.0269); M1 V_4 = 1084165.7847 -> 1084166; M2 N_4 = 3915834.2153; M3 L_4 = 0.276867 -> 0.2769; E3 eight unchanged periods.")
row("lx1b-num-L04-stats", "2.2 numbers", "L04.html expected block (301-317), :321, :469-472, quiz (501-520)", "PASS",
    "recompute_L04.py: sd window one 0.027935277918, window two 0.024699501388, n 668/321, zeros 1976-07, 2012-07, 2019-11 (665 nonzero), largest moves 0.135846 at 1985-03 and -0.096575 at 2008-10; telescoping identity holds to 2e-15 in both windows.")
row("lx1b-num-L04-display-diff", "2.2 numbers", "L04.html:318, :343-345, expected line 316", "PASS",
    "Unrounded sd2 - sd1 = -0.003235776530 -> -0.003236 (the printed figure); difference of the printed figures = -0.003235 (as the page says); ratio 0.884169 -> 0.8842 (out/recompute_L04.out).")
row("lx1b-num-L04-derived", "2.2 numbers", "L04.html:368, :375, :400, :425, :450, :536, :559", "PASS",
    "derived_L04.py (out/derived_L04.out): M1 ln 1.1 = 0.095310, simple minus log = 0.004690; M2 mean 1/150, sum of squared deviations 19/15000, dispersion 0.025166; E2 simple change -0.092058; R2 tanh(0.135846/2) = 0.067819, bound at h=0.0678 is 0.135808 (does not reach 0.135846); quiz bound 0.1358.")
row("lx1b-scope-start", "2.9 scope", "L04.html:330 (window start bullet); :321; card LX1-c063", "PASS",
    "The page calls the start a convention, says no other start is computed and no test of survival is made; twin computes only WINDOW_TWO_FROM='2000-01' (twin line 44). Scope matches.")
row("lx1b-math-L03", "2.4 mathematics", "L03.html:94-143, :393-396, :67, :121, :145", "PASS",
    "Re-derived myself: Lemma 3.1 identity l(y)-l(x) = C(y-x)/((C-x)(C-y)) with C>0 (L03:96 now states C>0); Prop 3.2(a)-(c) incl. the m=0 and m>=1 cases of (c); Cor 3.3 via V_m' < V_m; Cor 3.4 needs m'>=1 for a positive denominator (L03:135, :140-142). Every hypothesis used appears in the statement (L03:67 bound V_m < N0+D).")
row("lx1b-math-L04", "2.4 mathematics", "L04.html:58-107 (Def 1.1, Prop 1.2, Remark 1.3, Def 2.1, Prop 2.2, Remark 2.3); :398", "PASS",
    "Re-derived Prop 1.2 telescoping (cancellation of interior ln x_t) and Prop 2.2 (zero changes, zero dispersion, n-1 >= 1); Def 1.1 uses n-1 and requires n>=2 (L04:59).")
row("lx1b-math-problems", "2.4 / 2.9 problems", "L03.html:437-531; L04.html:364-459", "PASS",
    "Re-worked every problem: L03 M1-M3, P1-P3, E1-E3, R1-R3; L04 mech-1..3, proof-1..3 (band bound P2 and ln(1+u) <= u P3 re-derived), emp-1..3, res-1..3. All solutions agree with the printed numbers.")
row("lx1b-grades", "2.3 grades", "L03.html:542-546; L04.html:469-472; L03.html:82-89, :405; L04.html:105", "PASS",
    "Proved results are T (Prop 3.2, Cor 3.3, Cor 3.4 with conditional wording at :543; Prop 2.2, Prop 1.2); lab outputs are C with SIMULATED or real-data basis; each claim re-graded independently, no mismatch.")
row("lx1b-citations-L03", "2.1 citations / 2.3 claim scope", "L03.html:405, :630, :640; references/references.json friedman1963monetary and gertler2015monetary", "FAIL",
    "Friedman record re-resolved live (verify_refs --unit LX1, 0 problems): title, year 1963, ISBN 0691041474 and publisher agree with the page; the page cites the key and title only and types no second author (PASS part). FAIL: L03.html:405 says 'The course's reference list holds no admitted source for an empirical credit-channel claim', unqualified. The registry holds gertler2015monetary (Gertler and Karadi 2015, AEJ: Macroeconomics 7(1), DOI 10.1257/mac.20130329, status verified, used_by E7), whose title is 'Monetary Policy Surprises, Credit Costs, and Economic Activity', a record about credit costs; the sentence is contradicted as a general statement. The same unqualified sentence is in the quiz option at L03.html:630.",
    "Scope the sentence to the subject of this lesson, for example: 'The course's reference list holds no admitted source for an empirical claim about the credit channel of the Great Depression' (at L03.html:405 and in the option text at L03.html:630), or read gertler2015monetary and state its scope with a locator. Do not change the registry.")
row("lx1b-citations-L04", "2.1 citations", "L04.html:566-568 (section 9)", "PASS",
    "Section 9 cites the MANIFEST citation (Board of Governors, G.5/H.10, snapshot fx_monthly.csv, retrieved 2026-10-19) and matches the MANIFEST entry; it names no registry key.")
row("lx1b-notation", "2.4 notation", "L03.html (277 math segments); L04.html (149 math segments)", "PASS",
    "notation/notation.json registers T, Phi, R^*, R^{e*}, R_f, gamma_3, gamma_4 and Q; none occurs in the math of either page (scan). Local symbols (N, C, D, ell, kappa, psi, f_t, L, h, s, n) are lesson-local per the registry 'about' field; ell is a function in L03 and a log change in L04, each defined in its own lesson.")
row("lx1b-concepts-defs", "2.9 DAG defs", "L03.html:82, :87, :390; L04.html:59, :85, :86", "PASS",
    "check_dag passes: each introduced concept defined once (L03: credit-channel-depression at :87, lender-of-last-resort at :390; L04: bretton-woods-system at :86, pending, see its own row). Plain dfn terms (leverage, central bank, dispersion) carry no data-concept (plan decision 14).")
row("lx1b-banned-phrases", "2.9 banned phrases", "L03.html; L04.html", "PASS",
    "Scanned for BUILDER_RULES 1.3-1.4 strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, can be shown, roughly, historically, about <digit>): zero hits. The only '...' are math ellipses (L03.html:162, :254).")
row("lx1b-process-words", "2.9 process words", "L03.html; L04.html", "PASS",
    "Scanned for builder, verifier, round N, this section will, we will: no hits in learner text. 'pending' occurs only at L04.html:38, :86 (the Bretton row) and the honest-pending note L03.html:76, which states a fact about data.")
row("lx1b-structure", "2.9 structure", "L03.html sections 1-10; L04.html sections 1-9", "PASS",
    "Headings in order: L03 s1 :53, s2 :78, s3 :92, s4 :386, s5 :398, s6 :409, s7 :431, s8 :536, s9 :552, s10 :638; L04 s1 :53, s2 :79, s3 :108, s4 :323, s5 :336, s6 :358, s7 :463, s8 :478, s9 :564. data-hours=10 on both; check_pages PASS.")
row("lx1b-quiz-explanations", "2.9 quiz", "L03.html quiz (556-636); L04.html quiz (478-562)", "PASS",
    "Each explanation checked against the numbers and text: L03 q3 2.69 (exact 2.6867), q4 12, q6 3.426 (exact 3.42597, tolerance 0.0005), q8 1274345 (exact 1274345.2124), q9 8; L04 q3 3, q4 321, q7 no test, q8 0.095310, q9 window start, q10 no historical fact. The unscoped option at L03.html:630 is in row lx1b-citations-L03.")
row("lx1b-honest-data", "2.5 honest data", "L03.html:76, :148-152; L04.html:7, :113-114, :568", "PASS",
    "L03 is SIMULATED throughout (lab heading :148, honest-pending note :76); no historical series embedded for gold adherence or output depth (tools/data_sources.yaml lists only fx_daily, fx_monthly, ust_daily). L04 Part A is SIMULATED, Parts B-D read the embedded GBP column.")
row("lx1b-L03-remark42-solvency", "2.4 / 2.9 changed text", "L03.html:395 (Remark 4.2); :67 (Assumption 1.2 text)", "PASS",
    "Changed this round and re-derived: with V_t <= V_m (Prop 3.2(a)) and V_m < N0+D (Assumption 1.2), V_t < C and N_t = C - V_t > 0 in every period. The text now states both inequalities correctly.")
row("lx1b-L03-ratio-claims", "2.3 / 2.4 claims", "L03.html:404 (functional-form bullet); :523 (R2); :130 (Cor 3.3 proof)", "PASS",
    "Changed bullet re-derived: with premium phi*(L_t-L_0)^2 each depth is beta*phi*(bracket)^2, so the ratio is the square of the Corollary 3.4 ratio (numerically 3.426^2 = 11.737), and it differs from the ratio whenever the ratio is not 1. Problem R2 proof checked for a general strictly increasing G.")
row("lx1b-L03-r1-no-result", "2.9 scope", "L03.html:513-517 (R1)", "PASS",
    "R1 states no result: it says the proposition does not carry over without a new proof, which is a scope statement, not a claim.")
row("lx1b-L04-bretton-definition", "2.9 DAG / plan binding", "L04.html:38, :86; plans/LX1-build-plan.md section 9 item 9 (line 599) and line 143; plans/LX1-open-items.md; tools/check_dag.py lines 8, 73-75", "FAIL",
    "Plan section 9 item 9 (binding under the Architect decisions at plans/LX1-build-plan.md:632) says L04 states only the lab's facts and the first MANIFEST month until B3 (no source for Bretton Woods in references.json; grep count 0). L04.html:86 nonetheless carries <dfn id='def-bretton-woods-system' data-concept='bretton-woods-system'> with 'definition pending', and L04.html:38 introduces the concept. check_dag requires a dfn for each introduced concept, so the check passes only because of this pending dfn. plans/LX1-open-items.md asks the architect to confirm that reading, and plans/FINAL-ARCHITECT-RULINGS.md has no ruling on it (its delta adds item 12, about M3 only).",
    "Architect ruling required, recorded in plans/FINAL-ARCHITECT-RULINGS.md: either (a) a pending dfn satisfies check_dag and plan item 9 is amended to allow it, or (b) check_dag is changed to exempt a concept whose definition waits for a source. Until then the builder should not remove the dfn unilaterally, because check_dag then fails.")
row("lx1b-L04-simulated-label", "2.5 / 2.8 SIMULATED", "L04.html:7, :113-114, :568; twin lines 23-28; output line 1", "PASS",
    "Part A carries the SIMULATED label in the heading (:113), hypothesis (:114) and twin docstring (line 23); output line 1 reads 'Part A: SIMULATED model check, not data'.")
row("lx1b-L04-manifest-note", "2.8 data", "tests/labs/LX1/lab-LX1-L04-1.py docstring lines 3-8; L04.html code block (115-122)", "PASS",
    "Docstring matches MANIFEST fx_monthly: 669 months 1971-01 to 2026-09, retrieved 2026-10-19, transform (month-end, last value in month), inverted CAD, CHF, DKK, JPY, NOK, SEK so GBP is direct, exchange-rate columns only.")
row("lx1b-open-items-missing", "2.9 open items", "plans/LX1-open-items.md", "PASS",
    "The file is present and lists D-1 (L03 data), the Bretton Woods definition, B2 (credit-channel attribution), N1 and N2 (Friedman and Schwartz). It is the record for the open items above.")
row("lx1b-L04-prediction-tested", "2.5 labs", "L04.html:114 (hypothesis); lab-LX1-L04-1.py Parts A and C", "PASS",
    "The hypothesis predicts zero dispersion for the model (Part A prints True and 0.000000) and nonzero dispersion for the column (Part C prints 0.027935 and 0.024700); the text says the lab does not assert the second prediction, and it does not.")
row("lx1b-L03-lab-checks-overreach", "2.5 labs", "L03.html:145, :383; twin Parts B-D", "PASS",
    "Part B prints ordering and difference; Part C checks monotone and adjacent steps; Part D prints three ratios with no equality test (the twin uses none). The page says so (:145). No claim beyond these checks.")
row("lx1b-L03-misconception-scope", "2.9 prose", "L03.html:418 (misconception 2); proof L03.html:130", "PASS",
    "The misconception's claim (the ordering follows from the parity durations and the proof uses no failures) matches the proof of Corollary 3.3 at :130.")
row("lx1b-L04-A2-before-defined", "2.9 terms", "L04.html:85 (Definition 2.1), :92-99, :398, :446", "PASS",
    "(A2) is defined in Definition 2.1 at :85 before its first use in Prop 2.2 (:92) and the proof (:99). (A1) and (A3) are stated inline where used.")
row("lx1b-L04-keyresults-locator", "2.3 / 2.2", "L04.html:471 (key results row 3)", "PASS",
    "Row values 0.027935, 0.024700 and 0.8842 match the expected block (L04.html:301-317) and recompute_L04.out.")
row("lx1b-cards-l03-l04", "2.6 cards", "course/modules/LX/LX1/cards.json (48 L03/L04 cards; 76 cards in the file)", "PASS",
    "All 48 L03/L04 cards read (out/cards_L03_L04.out) and checked against the current lesson text: hypotheses carried (Lemma 3.1 :96; Prop 3.2 :108; Cor 3.3 :125; Cor 3.4 :135); numbers appear in the lesson (9.20, 2.69, 3.4260, 0.027935, 0.024700, 0.8842, 0.096575, 0.095310, 0.004690, 665, 669); changed cards c040, c041, c064 and new c076 agree with L03.html:390 and the MANIFEST. Duplicate scan over all 76 cards: 0 duplicate ids, 0 duplicate fronts.")
row("lx1b-delta-hunks", "delta 4bd8cb9..06994db", "L03.html (6 hunks: :51, :95, :395, :404, :414, :605); L04.html (:321, :328); cards.json (:212, :336-349, :538, :625-636)", "PASS",
    "git diff 4bd8cb9 06994db over the slice: every hunk read and checked (see rows above for each changed statement). Other changes in the unit (project.html, lab-LX1-project-3.py, FINAL-ARCHITECT-RULINGS item 12) are outside this slice; the twins L03 and L04 are byte-identical to 4bd8cb9.")
row("lx1b-L03-line121-lab-formula", "2.2 / 2.5", "L03.html:121 (Prop 3.2 paragraph); :145; tests/labs/LX1/lab-LX1-L03-1.py depth() and first_period_at_depth()", "PASS",
    "The paragraph says the lab does not evaluate part (b). The twin computes depth as max over the path (depth_path, depth) and never evaluates the closed form. The statement 'At t = m it equals the output fall that Lab 1 computes' holds: the path's maximum is at t = m (Prop 3.2(c)).")
row("lx1b-L03-why-ordering", "2.9 prose", "L03.html:51 (why-it-matters)", "PASS",
    "Changed this round: the chain is now stated with 'In the model below'. The ordering claim cites Assumptions 1.1-1.3 and Corollary 3.3, which is the proved statement; 'Definition 4.1' and 'Assumption 1.3' are forward references to numbered items.")
row("lx1b-L04-spot-only", "2.1 / 2.9 scope", "L04.html:328 ('Exchange rates only' bullet); tools/data_sources.yaml:62-64 (fx_monthly note)", "PASS",
    "Changed this round: 'The course's data register note for fx_monthly' is locatable at tools/data_sources.yaml:62-64, which reads 'Spot rates only, as for fx_daily.' The page's spot-only statement matches it.")

frag = {
    "unit": "LX1",
    "slice": "LX1-b",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b, round 7 (did not build LX1 or LX1-b; full read of L03.html and L04.html and both lab twins; delta 4bd8cb9..06994db hunk by hunk; every round-6 non-PASS row re-verified from scratch; all 48 L03/L04 cards checked)",
    "pin": "06994db1",
    "base": "4bd8cb9 (round-6 pin); delta limited to L03.html (6 hunks), L04.html (2 changed lines), cards.json (4 hunks); both twins byte-identical",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-LX1-b",
    "scratch": "/tmp/lx1b-r7 (labs run in /tmp/lx1b-r7/L03 and /tmp/lx1b-r7/L04; guard copies in /tmp/lx1b-r7/guard)",
    "verified_at": "2026-11-04T20:30:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [
        "friedman1963monetary: registry record lists Friedman only; the curriculum string is 'Friedman & Schwartz (1963)' (plan N2). The pages cite the key and the title only. The architect may correct the record through tools/add_reference.py.",
        "Bernanke (1983), AER 73(3), the credit-channel source named at curriculum/06-profession-capstone.yaml:38: no registry record (plan B2, REFERENCE_REQUEST 2). L03 makes no empirical attribution to it.",
        "No Bretton Woods source in references.json (grep count 0): plan B3, REFERENCE_REQUEST 3, still open.",
    ],
    "freshness_flags": [],
    "notes": [
        "Round-6 non-blocking notes: L03.html:395 restatement is fixed (now states both inequalities); L04.html:328 now names the data register note and it is locatable at tools/data_sources.yaml:62-64; the first-date clause in Prop 2.2 (L04.html:92) is unchanged and reads correctly.",
        "Lab twins are demonstrations; mutation testing does not apply to them (architect ruling), and this slice has no grader. No mutants were written.",
        "Could not check: a live rebuild of fx_monthly.csv from the Federal Reserve feed (fetch_data --fetch) was not repeated this round; the carried row rests on the byte-identical CSV and MANIFEST sha256. The Gertler and Karadi abstract was not read; the FAIL at lx1b-citations-L03 rests on the registry record's title and fields.",
    ],
    "summary": "LX1-b round 7 on 06994db1 (delta from 4bd8cb9): verdict FAIL. 54 rows: pass=52 fail=2 unverifiable=0. Non-PASS: lx1b-L04-bretton-definition (architect ruling still outstanding, unchanged since round 4) and lx1b-citations-L03 (the unqualified 'no admitted source for an empirical credit-channel claim' at L03.html:405 and the option at :630 conflicts with the admitted record gertler2015monetary). Both twins run clean under python -I -W error, page code equals the twins, expected blocks equal live output, every number, proof, card and the data licence were re-checked.",
}
pathlib.Path("ledgers/LX1/LX1-b.json").write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(R), "pass", sum(r["status"] == "PASS" for r in R), "fail", sum(r["status"] == "FAIL" for r in R))
