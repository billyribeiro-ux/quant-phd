import json, sys
sys.path.insert(0, 'tools')
import ledger

def row(i, check, location, status, evidence, fix=None):
    r = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

R = []
G = "ledgers/FC2/scripts/FC2-a-r5/gates.out"
R.append(row("FC2a-cmd-check_pages", "2.9 structure; check_pages --unit FC2", "course/modules/FC/FC2/index.html, L01.html, L02.html, L03.html", "PASS",
  f"`.venv/bin/python tools/check_pages.py --unit FC2` -> 'check_pages FC2: PASS', exit 0 ({G})."))
R.append(row("FC2a-cmd-check_dag", "2.9 DAG; check_dag --unit FC2", "course/modules/FC/FC2/*.html", "PASS",
  f"`tools/check_dag.py --unit FC2` -> 'check_dag FC2: PASS', exit 0 ({G})."))
R.append(row("FC2a-cmd-check_projects", "2.6 project gate, unit level (not judged in slice a)", "course/modules/FC/FC2/project.html", "PASS",
  f"`tools/check_projects.py --unit FC2` -> 'check_projects FC2: PASS', exit 0 ({G})."))
R.append(row("FC2a-cmd-run_labs", "2.9 labs; run_labs --unit FC2 and --page L01/L02/L03", "L01.html, L02.html, L03.html lab sections", "PASS",
  "`tools/run_labs.py --unit FC2` -> 'run_labs FC2: PASS (11/11)'; `--page L01`, `--page L02`, `--page L03` each PASS (1/1) (ledgers/FC2/scripts/FC2-a-r5/run_labs.out, run_labs_pages.out)."))
R.append(row("FC2a-cmd-twin-direct", "2.9 twins alone under python -I -W error", "tests/labs/FC2/lab-FC2-L01-1.py, lab-FC2-L02-1.py, lab-FC2-L03-1.py", "PASS",
  "`.venv/bin/python -I -W error <twin>` exit 0 for all three; stderr 0 bytes; stdout in ledgers/FC2/scripts/FC2-a-r5/twin-L01.out, twin-L02.out, twin-L03.out."))
R.append(row("FC2a-cmd-page_smoke", "2.9 browser smoke for slice pages (alone)", "index.html, L01-L03", "PASS",
  "`tools/page_smoke.py --unit FC2 --pages index.html L01.html L02.html L03.html` -> 'page_smoke FC2: PASS', exit 0 (ledgers/FC2/scripts/FC2-a-r5/page_smoke.out)."))
R.append(row("FC2a-cmd-ruff-mypy", "2.9 ruff check/format; mypy --no-incremental on the three twins", "tests/labs/FC2/lab-FC2-L01-1.py..L03-1.py", "PASS",
  "ruff check: 'All checks passed!'; ruff format --check: '11 files already formatted'; mypy --no-incremental: 'Success: no issues found in 3 source files' (gates.out)."))
R.append(row("FC2a-cmd-pytest", "2.9 relevant pytest", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_curriculum.py, test_docs_figures.py", "PASS",
  "`pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py` exit 0 (pytest.out); `pytest tests/test_curriculum.py tests/test_docs_figures.py` exit 0 (pytest2.out)."))
R.append(row("FC2a-cmd-verify_refs", "2.9 registry; verify_refs --offline", "index.html data-cite list (hull2021options, stoll1969relationship, cox1979option)", "PASS",
  "`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0. references.json: all three keys status 'verified', used_by FC2."))
R.append(row("FC2a-links", "2.9 internal links and anchors", "index.html, L01-L03", "PASS",
  "Script ledgers/FC2/scripts/FC2-a-r5/anchors.py (python -I): 72 hrefs resolved, 0 missing files, 0 missing anchors."))
R.append(row("FC2a-twin-equals-page", "2.9 page code equals twin; expected equals output", "L01.html, L02.html, L03.html lab sections", "PASS",
  "run_labs.py reports no 'not byte-identical' or 'output does not match' problem for L01-L03 (run_labs_pages.out)."))
R.append(row("FC2a-hub-hours", "hours arithmetic", "index.html data-hours-lessons/project; L01-L08 data-hours", "PASS",
  "index.html:29 data-hours-lessons=60, data-hours-project=30; lesson data-hours 6,8,9,7,8,8,8,6 sum to 60; 60+30=90; 66.7%/33.3% split at index.html:38-41; L03 data-hours=9 (L03.html:2)."))
R.append(row("FC2a-hub-placement-arithmetic", "placement quiz arithmetic", "index.html #placement (lines 67-128)", "PASS",
  "Nine items; six on M4/CF1/M1 (items 1-6), one FC1 (item 7), two skill checks (items 8-9). Recomputed: -100+60/1.1+60/1.21=4.1322 (4.13); 1/1.1025=0.9070; skill 1 gap 5.75; skill 2 gap 12 (rederive.py). 7/9=77.8% (below 80%), 8/9=88.9%."))
R.append(row("FC2a-hub-prose", "hub prose: lede, prerequisites, ladder, data status", "index.html:33, :35, :59-63, :150-152, :157-159", "PASS",
  "Lede (:33) 'any forward price other than the cost-of-carry price admits a riskless profit' is supported by Proposition 2.2 Cases 1-2 (L02.html:98-100). Prerequisite closure: coursekit.prerequisite_closure('FC2') = AC1, CF1, E1, FC1, M1, M2, M4, P0.1, matching 'adds M1, M2, AC1, E1 and P0.1'. FC1 cost concept: FC1/L03.html:62 defines bid-ask-spread; project.html:333 P6 uses half-spread. Ladder rung 1 'six-strike' matches project.html:44 and :55; rung 2 'three blanks' matches project.html:226, 228, 241. Data status matches project.html:285 and :672."))
R.append(row("FC2a-structure-lessons", "2.5 lesson structure", "L01.html, L02.html, L03.html", "PASS",
  "Sections 1-9, meta-row, grade legend, lab section with hypothesis/interpretation, key-results table, quiz with data-cards, references, lesson-nav present (read in full)."))
R.append(row("FC2a-numbers-prose", "numbers in prose vs unrounded values and displayed digits", "L01-L03 prose, solutions, quizzes, key results, hub", "PASS",
  "Recomputed by rederive.py (python -I; rederive.out): L01 arbitrage counts 0 and 30; dominance pairs 302/0 and 302/38; psi 1/20, 17/20 and -1/5, 11/10. L02 F*=5126.58 cents; V=237.1077 -> 237.11; quote-fair 73.42; M2 profit 0.19599 -> 0.20; M3 5.4888 -> 5.49; R3 e^0.1-1.1025=0.0026709 -> 0.0027; e^0.1 -> 1.1052. L03 margins sum 84, 4 loss days; DF to six places; par 0.04902625 -> 4.9026%; payment 4902624.503 -> 4902625; value -4415468; M3 2.673012 -> 2.67; R3 3.9756%; 0.0267301."))
R.append(row("FC2a-L01-math", "mathematics: Sections 1-3 of L01", "L01.html lines 53-146", "PASS",
  "Props 2.1, 2.2, 3.2, 3.5 proofs checked line by line; Example 2.4 values (2, 19/10); Example 3.4 psi formulas (lines 129); Remark 3.6 boundaries (zero-cost portfolios (-1,1), (3,-1)); no gap found."))
R.append(row("FC2a-L01-problems", "problem sets and quiz of L01", "L01.html lines 319-520", "PASS",
  "M1-M3, P1-P3, E1-E3, R1-R3 solutions recomputed (R1 psi formulas with an extra state; R3 case analysis); quiz Q1-Q10 answers and explanations checked against Definition 1.1 and Proposition 3.5."))
R.append(row("FC2a-L02-math", "mathematics: Sections 1-4 of L02", "L02.html lines 53-268", "PASS",
  "Prop 2.2 Cases 1 and 2 (L02.html:98-100) construct arbitrage for F>F* and F<F*; Prop 3.1 proof (252) and Cor 3.2 (262) recomputed; Remark 2.5 and Example 2.4 values."))
R.append(row("FC2a-L02-problems", "problem sets and quiz of L02", "L02.html lines 300-493", "PASS",
  "P1 income formula (335) recomputed; P2 partials (342); P3 (349); E1-E3 (360, 368, 374 value 237.1077); R1 interval (385); R2 (392); R3 annual compounding (399); M1-M3; quiz Q1-Q9 answers checked."))
R.append(row("FC2a-L03-math", "mathematics: Sections 1-3 of L03", "L03.html lines 53-150", "PASS",
  "Prop 1.3 telescoping (77); Prop 3.2 (115-117); Prop 3.3 (122-130); Example 3.4 geometric series (134) with rho=0 case; Prop 3.5 (139-144); n=2 counterexample at line 105 gives 0 = 3/2 (sum DF=0, 1-DF_2=3/2)."))
R.append(row("FC2a-L03-problems", "problem sets of L03", "L03.html:385 (E3 solution); problems lines 311-414", "FAIL",
  "M1-M3, P1-P3, E1, E2, R1-R3 recomputed and correct. E3 solution (L03.html:385) says 'The par rate is not a zero rate because Proposition 3.3 defines it as a ratio that uses all five discount factors'. This is a non-sequitur: Example 3.4 (L03.html:134) shows that the same ratio on a flat curve equals the flat zero rate, rho. The reason the value differs from the typed-in rates here is the number itself (4.9026 percent lies strictly between the 4.5 and 5 percent zero rates), and the solution's second clause states that.",
  "Rewrite the E3 solution's first sentence to state the reason from the printed value: the par rate 4.9026 percent is not one of the five typed-in zero rates (3, 3.5, 4, 4.5, 5 percent). Drop 'because ... ratio that uses all five discount factors' as the reason; if a general remark is kept, say that on a flat curve the par rate equals the flat rate (Example 3.4)."))
R.append(row("FC2a-r5-L03-quiz-q10", "retrieval quiz item Q10 and explanation", "L03.html:503-509", "FAIL",
  "Quiz Q10 asks 'Why is the par rate of Lab 3, Part B, not a typed-in zero rate?' The option marked correct (L03.html:506) is 'Because it is computed from all five discount factors by Proposition 3.3'. That is not a reason: the same computation gives the flat rate on a flat curve (Example 3.4, L03.html:134). The explanation (L03.html:509) repeats the non-sequitur. The other options (rounding; day count 360) are wrong, so the item teaches the wrong reason.",
  "Change the marked option to a fact of the lab: 'Because the value computed from all five discount factors by Proposition 3.3 is 4.9026 percent, which equals none of the five typed-in zero rates'. Change the explanation at L03.html:509 to match, without the word 'because' before the ratio."))
R.append(row("FC2a-lab-L01-claims", "lab hypothesis and interpretation claims", "L01.html lab-FC2-L01-1 hypothesis (line 150), interpretation (286); misconceptions", "PASS",
  "Printed output (run_labs; twin-L01.out): Part A 0 arbitrage, state prices 1/20 and 17/20, dominance 302 pairs and 0 violations; Part B 30 arbitrage portfolios, zero-cost (-5,9) with payoffs 22 and 4, state prices -1/5 and 11/10, 38 violations. Each claim in the hypothesis matches. Misconception 3 (line 314) matches Part B."))
R.append(row("FC2a-lab-L02-claims", "lab hypothesis and interpretation claims", "L02.html lab-FC2-L02-1 hypothesis (line 121), interpretation (238); Example 2.4; Section 3", "PASS",
  "Printed output (run_labs; twin-L02.out): 5126.58; replication equal in four outcomes; net 73.42 in every state; 0 date-0 cash legs; fair quote 0; E value 237.11. Hypothesis and interpretation (floating-point display rounding; typed-in inputs) match the twin docstring."))
R.append(row("FC2a-lab-L03-claims", "lab hypothesis and interpretation claims", "L03.html lab-FC2-L03-1 hypothesis (line 154), interpretation (277); Section 2; misconception 3", "PASS",
  "Printed output (run_labs; twin-L03.out): identities True; 4 loss days; balance 84; par 0.049026 (4.9026 percent, not one of the five zero rates); payment 4902625 cents; value -4415468. Hypothesis's 'SIMULATED', 'seeded' and 'typed-in' statements match the twin docstring (lines 157-166)."))
R.append(row("FC2a-grades", "grades: key-results tables, card grades", "L01.html:430-435; L02.html:411-417; L03.html:422-427; cards.json L01-L03 grade fields", "PASS",
  "Key-results rows all grade T with a source. Cards with grade C name a lab or convention basis (c046, c049, c050). Cards without a grade field are definitions, assumptions or a scope statement (c001-c003, c007, c016-c018, c033-c035, c039-c040, c139-c141, c144, c146, c173)."))
R.append(row("FC2a-notation", "notation registry conflicts", "L01-L03, index.html, cards.json for slice a", "PASS",
  "notation/notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. Slice a uses T only in the note at L02.html:55 (T reserved for observations, consistent with the registry). Phi, gamma, R^*, R_f and Q do not occur in slice-a pages or cards (grep). Macros used (\\E, \\Var, \\Prob) are registered. tau, DF, F, S, r, L_i, Delta, psi, theta, eta, rho are defined in the lesson where used."))
R.append(row("FC2a-dag-closure", "DAG: concepts used outside the prerequisite closure", "index.html, L01-L03", "PASS",
  "coursekit.prerequisite_closure('FC2') = {AC1, CF1, E1, FC1, M1, M2, M4, P0.1}. Concept links in slice-a pages: normal-distribution, expectation, variance, present-value, discount-factor, continuous-compounding, geometric-series, annuity, net-present-value, exchange-vs-otc, clearing-and-settlement, arbitrage-opportunity (L01) and forward-contract (L02, L03), all inside the closure or the unit. check_dag FC2 PASS."))
R.append(row("FC2a-data", "data status and sources", "index.html #data (157-159); L01-L03 labs", "PASS",
  "No data-files attribute and no data/ read in L01-L03 (grep). Hub statement matches project.html:285 ('No market data is embedded'), :360 and :672. Lab 3 Part A is SIMULATED (L03.html:157)."))
R.append(row("FC2a-L02-why-only-price", "why-it-matters claim vs Proposition 2.2", "L02.html:51", "PASS",
  "Round-4 FAIL is fixed: the sentence now reads 'Under stated conditions, a forward price other than the cost-of-carry price admits an arbitrage.' Supported by Proposition 2.2 Cases 1-2 (L02.html:98-100). The 'only price' sentence no longer appears (grep)."))
R.append(row("FC2a-cards-accuracy", "cards agree with current lesson text", "cards.json FC2-c050 (lines 321-325)", "FAIL",
  "c050 front 'Is the par rate of a swap the market's interest rate?' is answered 'No.' as a general statement. Its back says R_par 'equals none of the typed-in zero rates'. That holds only for Lab 3, Part B. Example 3.4 (L03.html:134) gives R_par = rho on a flat curve, which equals the market's flat rate. Other L01-L03 cards read in full and checked against their lessons: c005, c015, c019 and c154 are qualified by lesson; c007 is an honest scope statement; c025 and c172 ask different questions; c027 and c172 carry hypotheses; c138, c164, c165, c168, c169, c177, c178 match.",
  "Replace the back with: 'Not in general. On a flat curve R_par equals the flat rate (Example 3.4). In Lab 3, Part B, R_par = 4.9026 percent equals none of the five typed-in zero rates (Lab 3, Part B).'"))
R.append(row("FC2a-cards-coverage", "card coverage of L01-L03", "cards.json (61 cards for L01-L03)", "PASS",
  "Cards: L01 18, L02 23, L03 20. Cover Definition 1.1, Props 2.1, 2.2, 3.2, 3.5, Example 3.4, Remarks 2.3, 3.3, 3.6, Problems E2, E3, M3, P1-P3, R1, Lab 1-3 parts. All ids unique (python check; no duplicates)."))
R.append(row("FC2a-cards-trivia", "cards test understanding, not trivia", "cards.json FC2-c021, c046", "PASS",
  "Numeric cards ask a computed value with its basis (c021 = Example 2.4; c046 = Problem P2 and Lab 3 Part B). No card asks a restated label alone."))
R.append(row("FC2a-cards-hypotheses", "cards carry the hypotheses of the proposition they cite", "cards.json FC2-c046 (lines 290-294)", "FAIL",
  "c046 front: 'On the 1,000,000-dollar notional of Lab 3, Part B, what is the value to the payer of a swap struck one percentage point above the par rate, in cents?' It cites Problem P2, which uses Proposition 3.5, and Proposition 3.5 says 'Assume A8' (L03.html:138). The par rate is defined under A8 (Proposition 3.3, L03.html:121). The card omits the hypothesis; its sibling FC2-c044 states 'Under A8'.",
  "Front should read: 'Under A8, on the 1,000,000-dollar notional of Lab 3, Part B, what is the value to the payer of a swap struck one percentage point above the par rate, in cents?'"))
R.append(row("FC2a-L01-assumption-first-use", "assumption first-use claims", "L01.html:65-66 (A3 block), :75", "PASS",
  "A3 block says it is used alone; first use is Proposition 2.1 (L01.html:75). A1 and A2 are defined in L02 Section 1 and first used in Proposition 2.2 (L02.html:93), as stated at L01.html:66."))
R.append(row("FC2a-lab-hypothesis-SIMULATED", "SIMULATED labelling", "L03.html lab-FC2-L03-1 (lines 154-158); index.html #data", "PASS",
  "Part A is labelled SIMULATED in the hypothesis, the twin docstring (line 157) and the output header; no FC2 lab reads market data."))
R.append(row("FC2a-r3-ex34-hypothesis", "Example 3.4 hypotheses", "L03.html:134; cards FC2-c043 (line 276)", "PASS",
  "Example 3.4 begins 'Assume A8' and gives rho > -1; rho = 0 handled in the same example; c043 front says 'Under A8'."))
R.append(row("FC2a-r3-prop32-title", "Proposition 3.2 title and hypothesis", "L03.html:109-110", "PASS",
  "'Proposition 3.2 (value of the floating leg)', 'Assume A8'; statement 1 - DF_n matches proof (lines 113-118)."))
R.append(row("FC2a-r3-card-c037-remark14", "card c037 vs Remark 1.4 and Section 4", "cards.json FC2-c037 (lines 245-249); L03.html:82, :286", "PASS",
  "Back cites Remark 1.4 (L03.html:82) and 'Section 4' (canon-breaks, L03.html:286), both of which say margin requirements are not modelled and A8' does not cover a requirement's payment."))
R.append(row("FC2a-r3-L02-sec1-forward-ref", "forward references in L02 Section 1", "L02.html:70-71 (A2), :79-82 (A4)", "PASS",
  "A2 refers to A4 of this lesson, which is defined at L02.html:79-82 with the rate, compounding and discount factor."))
R.append(row("FC2a-r3-L03-def31-forward-ref", "forward reference from Definition 3.1 to A8", "L03.html:100, :104-105", "PASS",
  "Definition 3.1 says the floating coupon is set 'by the relation of Assumption A8 below'; A8 is at L03.html:104-105."))
R.append(row("FC2a-r4-L03-positivity-sentence", "A8 sentence on which hypothesis each proposition uses", "L03.html:105 (A8 block); proofs at :115, :129, :144", "PASS",
  "Round-4 FAIL is fixed. The sentence now says non-vanishing of each DF_i is used in Proposition 3.2 (division by DF_i in the proof, line 115) and positivity in Propositions 3.3 (sum strictly positive, line 129) and 3.5 (line 144). The n = 2 counterexample: DF_1 = 1/2, DF_2 = -1/2 gives sum 0 and 1 - DF_2 = 3/2, so the Proposition 3.3 equation reads 0 = 3/2."))
R.append(row("FC2a-r4-card-c007-scope", "card c007 scope words", "cards.json FC2-c007 (lines 43-46)", "PASS",
  "Round-4 FAIL is fixed. c007 is now a question with the answer 'No. Proposition 3.2 runs one way; the lesson does not prove the converse (Remark 3.3).' This matches L01.html:123-124. The card carries no grade, so it asserts no theorem."))
R.append(row("FC2a-r4-card-c025-c172-overlap", "duplicate cards", "cards.json FC2-c025 (line 164) and FC2-c172 (line 1131)", "PASS",
  "Round-4 FAIL is fixed in substance. c025 asks the value V_t of a long forward; c172 asks at which spot S_t the value is zero. The second is a distinct question with a distinct answer (S_t = F* e^{-r(tau-t)}), derived from the same Corollary 3.2 (L02.html:257). Not a duplicate."))
R.append(row("FC2a-r4-hub-six-contract", "hub rung text vs project page", "index.html:150; project.html:44, :55", "PASS",
  "Round-4 FAIL is fixed: index.html:150 now says 'six-strike SIMULATED chain', matching project.html:44 ('one six-strike SIMULATED chain') and :55 (six strikes)."))
R.append(row("FC2a-r4-L02-lab-floats", "lab docstring vs printed values (float vs integer cents)", "tests/labs/FC2/lab-FC2-L02-1.py docstring; L02.html:238", "PASS",
  "Round-4 FAIL is fixed: docstring now says typed-in prices are integer cents and formula prices are floating-point values in cents. Page code is byte-identical to the twin (run_labs PASS); interpretation matches."))
R.append(row("FC2a-r4-proposition-numbering", "Proposition numbering across lessons", "L01.html and L02.html Proposition 2.2; cards c005, c015, c019, c154", "PASS",
  "Round-4 FAIL is fixed: c005 and c154 fronts now begin 'In Lesson 1'; c015 says 'Proposition 2.2 of Lesson 1'; c019 says 'In Lesson 2'. Cross-lesson references in the pages are qualified (L02.html:243 'Proposition 2.1 of Lesson 1'; L01.html:66 'Lesson 2, Section 1')."))
R.append(row("FC2a-r4-card-c027-hypothesis", "card c027 carries Proposition 3.1 hypotheses", "cards.json FC2-c027 (line 178)", "PASS",
  "Round-4 FAIL is fixed: the front now reads 'Under A1 to A4 and A3 at each date', the hypothesis of Proposition 3.1 (L02.html:247)."))
R.append(row("FC2a-r5-delta-hunks", "delta read hunk by hunk (edbb7aa8..dde0486b) for slice a", "L01.html:51; L02.html:51, :62, :123-130; L03.html:105, :149; index.html:33, :150; tests/labs/FC2/lab-FC2-L02-1.py; cards.json (FC2-c005, c007, c015, c016, c019, c027, c037, c154, c172, c177, c178)", "PASS",
  "git diff edbb7aa8 dde0486b read for every slice-a file: all changed hunks were read and re-verified above. cards.json hunks for L04-L08 (c052, c059, c060, c064, c103-c113, c122, c145, c152, c159, c179-c183) are not in slice a and were not judged here. L06, L07, L08 pages and tests/labs/FC2/lab-FC2-L06-1.py also changed in this delta and belong to other slices."))
R.append(row("FC2a-r5-rederive", "independent re-derivation of every printed number in the L01-L03 labs and prose", "ledgers/FC2/scripts/FC2-a-r5/rederive.py", "PASS",
  "`python3 -I rederive.py` output in rederive.out reproduces the L01 counts (0, 30, 302/0, 302/38), L02 values (5126.58, 237.11, 73.42, 0.20, 5.49, 0.0027, 1.1052) and L03 values (84, 4 loss days, 4.9026%, 4902625, -4415468, 2.67, 3.9756%, 0.026730)."))
R.append(row("FC2a-r5-build-site", "generated site data current", "course/assets/data/program.json; course/index.html; course/concepts.html", "PASS",
  "`tools/build_site.py --check` -> 'site data current: 6 outputs', exit 0 (build_site_check.out). Lede text does not appear in generated data (grep)."))

frag = {
  "unit": "FC2", "slice": "a", "round": 5,
  "verifier": "Haiku independent verifier, FC2-a round 5 (delta verification; did not build FC2; re-verified every round-4 non-PASS row and every row whose subject changed)",
  "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
  "base": "edbb7aa8de20e6d2f3035c463a79a318c22623c4 (round-4 pin, per ~/.fanout/frags/S-FC2-a.round4.json)",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyS5-FC2-a (detached at dde0486b, .venv symlinked)",
  "scratch": "/Users/billyribeiro/.fanout/wt/verifyS5-FC2-a/ledgers/FC2/scripts/FC2-a-r5",
  "verified_at": "2026-11-09T10:07:13Z",
  "verdict": "FAIL",
  "rows": R,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": "No project grader is in slice a, so no student-error mutants were built; the lab twins are demonstrations (ruling). Not run: full run_graders/mutate_graders (not a project slice); full gate (ruff on whole repo, mypy strict on whole repo, full pytest suite, render_curriculum) (scoped to this slice as the procedure directs). Hours are design targets; arithmetic consistency checked and OK.",
  "summary": "Delta round 5 for FC2 slice a. Round-4 FAILs fixed except as listed. Two new defects: the par-rate 'not a zero rate because' reasoning (L03 E3, quiz Q10, card c050 overgeneralisation) and card c046 missing the A8 hypothesis."
}
problems = ledger.validate(frag, "FC2-a")
print("validation problems:", problems)
n_fail = sum(1 for r in R if r["status"] != "PASS")
print("rows", len(R), "non-pass", n_fail)
json.dump(frag, open("ledgers/FC2/FC2-a.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote ledgers/FC2/FC2-a.json")
