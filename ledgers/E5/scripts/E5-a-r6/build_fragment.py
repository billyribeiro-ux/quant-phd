import json
C = "Carried from round 5 (course/modules/E/E5/index.html:35 byte-identical since the previous pin 04626e9): "
rows = []
def R(id_, check, location, status, evidence):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

R("E5a-r3-hub-prereq-titles", "Hub prerequisite titles match curriculum strings", "course/modules/E/E5/index.html:35", "PASS",
  C + "'E1 Microeconomics', 'M1 Precalculus & Mathematical Reasoning', 'M2 Single & Multivariable Calculus' match curriculum/02-economics-finance-core.yaml:19 and curriculum/01-foundations.yaml:88, :123. Line 35 read this round and unchanged in the 04626e9..9fd6aed delta.")
R("E5a-r3-hub-card-titles", "Hub card titles equal lesson h1", "course/modules/E/E5/index.html:145-152", "PASS",
  "Read this round: card titles 'National Accounts, Price Indices and Measured Inflation' (L01), 'Growth Accounting and the Solow Residual' (L02), 'The Solow growth model' (L03) equal L01.html:35, L02.html:35, L03.html:36.")
R("E5a-r3-nav-titles-L02-L03", "Lesson-nav labels equal target h1", "course/modules/E/E5/L02.html:490; L03.html:617", "PASS",
  "Read this round: L02.html:490 'L03 · The Solow growth model' = L03.html:36; L03.html:617 'L02 · Growth Accounting and the Solow Residual' = L02.html:35. Round-5 cited L03.html:612 for this link; the link is at line 617 in this checkout (line 612 is the references list), so the location is corrected here.")
R("E5a-r3-hub-grammar", "Learner prose is grammatical", "course/modules/E/E5/index.html:33", "PASS",
  "index.html:33 reads 'You will be able to derive a growth decomposition, solve a macro model for its equilibrium, trace a policy shock through it, and state what the models cannot say.' Grammatical. See E5a-r6-hub-lede-static-claim for a content error in the same paragraph.")
R("E5a-r3-L02-exactly-when", "Claim about a theorem matches its statement", "course/modules/E/E5/L02.html:104 vs Theorem 2.3 at :107-110", "PASS",
  "grep 'exactly when' over index.html, L01-L03.html: no hit. Theorem 2.3 (L02.html:107-110) states only the one-directional identity Res_t(alpha) = Delta ln A_t under Assumption 1.3; L02.html:104 states sufficiency only.")
R("E5a-r3-L03-attribution-wording", "References paragraph consistent with page naming", "course/modules/E/E5/L03.html:611", "PASS",
  "L03.html:611 'This lesson has not read that paper and attributes no result to it. The name Solow growth model is used on this page as a conventional label for Definition 1.1'. Consistent with the page naming. The overclaim in the same paragraph is E5a-r6-L03-refs-all-T.")
R("E5a-r3-L03-sign-lemma-first-use", "Terms defined before use", "course/modules/E/E5/L03.html:52 vs :138", "PASS",
  "L03.html:52 says 'the sign of g(k) - k for the map g of Definition 1.1 on a grid of 50 values' with no 'sign lemma'. grep 'sign lemma' over L03.html: first hit line 138 ('Step 1, the sign lemma.'). Twin grid: Part C, Decimal(i)/5 for i=1..50 (27 below, 23 above, printed).")
R("E5a-card-uniqueness-contradiction", "Cards agree with the current lesson statement (Prop 2.2 says exactly one POSITIVE steady state)", "course/modules/E/E5/cards.json (E5-c041); L03.html:52, :98, :527", "PASS",
  "E5-c041 back: 'the recursion has exactly one positive steady state'. L03.html:98 Proposition 2.2 and :527 key result say positive. grep 'exactly one' over cards L01-L03 and the three pages: only c041 and L03 lines 52, 98, 527, all positive-only.")
R("E5a-cmd-check-pages", "check_pages L01, L02, L03 and unit", "tools/check_pages.py --unit E5 [--page L01|L02|L03]", "PASS",
  "ledgers/E5/scripts/E5-a-r6/check_pages_{E5,L01,L02,L03}.out: 'check_pages E5: PASS', 'check_pages E5 L01: PASS', 'check_pages E5 L02: PASS', 'check_pages E5 L03: PASS' (exit 0 each).")
R("E5a-cmd-check-dag", "check_dag E5", "tools/check_dag.py --unit E5", "PASS",
  "ledgers/E5/scripts/E5-a-r6/check_dag_E5.out: 'check_dag E5: PASS' (exit 0). check_projects E5: PASS (check_projects_E5.out).")
R("E5a-cmd-run-labs", "run_labs per page", "tools/run_labs.py --unit E5 --page L01|L02|L03", "PASS",
  "run_labs_L01.out, run_labs_L02.out, run_labs_L03.out: 'run_labs E5: PASS (1/1)', exit 0 each.")
R("E5a-cmd-page-smoke", "page_smoke index, L01-L03", "tools/page_smoke.py --unit E5 --pages index L01 L02 L03", "PASS",
  "page_smoke_E5.out: 'page_smoke modules/E/E5/L03.html: PASS', 'page_smoke E5: PASS', exit 0.")
R("E5a-twins-isolated", "Twins run alone under python -I -W error", "tests/labs/E5/lab-E5-L0{1,2,3}-1.py", "PASS",
  "ledgers/E5/scripts/E5-a-r6/twin_L0{1,2,3}.out: exit 0 each; twin_L0n.err is 0 bytes each. Output: L01 ends 'chain product ... 3/2 equals direct ratio 3/2: True'; L02 'log growth is at most simple growth in every period: True'; L03 'equal_within_tolerance True'.")
R("E5a-page-code-equals-twin", "Page code block equals twin", "L01.html, L02.html, L03.html data-run blocks", "PASS",
  "ledgers/E5/scripts/E5-a-r6/twin_vs_page.py: page data-run text equals the twin file for L01, L02 and L03 once the single trailing newline the embed step omits is ignored (exact-match False only by that final newline; twin_vs_page.out).")
R("E5a-expected-equals-output", "Expected block equals output", "L01.html, L02.html, L03.html pre.expected", "PASS",
  "twin_vs_page.out: 'L01 expected==output: True', 'L02 expected==output: True', 'L03 expected==output: True' (exact string match after strip of the twin's stdout).")
R("E5a-lint-and-tests", "Lint, types, tests for the E5 twins", "tests/labs/E5; mypy; pytest -k E5", "PASS",
  "ruff_check.out 'All checks passed!'; ruff_format.out '11 files already formatted'; mypy.out 'Success: no issues found in 229 source files' (mypy --no-incremental, repo); pytest_E5.out '12 passed, 553 deselected'.")
R("E5a-registry-keys", "Reading-list keys exist and match the registry", "course/modules/E/E5/index.html:178-181; references/references.json", "PASS",
  "references.json has solow1956contribution (QJE 70(1), 1956), hicks1937mr (Econometrica 5(2), 1937), phelps1968money (JPE 76(4), 1968), blanchard2020macroeconomics (book; record year 2020; curriculum 8th ed. 2021). used_by includes E5 for each. The page states no edition or year for Blanchard (index.html:181). verify_refs.out: 'offline integrity: 560 entries, 0 problems'.")
R("E5a-no-friedman", "No stray attribution", "index.html, L01-L03", "PASS",
  "grep -i friedman over the four pages: no hit.")
R("E5a-p01-concept-anchors", "P0.1 concept links resolve and read 'not yet released'", "course/modules/E/E5/index.html:60,65; L01.html:37; concepts.html:39,40,44", "PASS",
  "P0.1 ids evidence-grade, project-ladder, notation-conventions are 'not yet released' entries in course/concepts.html:39, :40, :44. L01.html:37 notation-conventions link is consistent with that entry.")
R("E5a-notation", "Symbols match notation/notation.json (no registered symbol reused)", "index.html, L01-L03 math; notation/notation.json", "PASS",
  "Registered symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. grep over the four pages: no \\Phi, \\gamma, R^\\ast, R_f, \\mathbb{Q} or \\E. 'T' appears only as the grade label. No registered meaning is reused.")
R("E5a-banned-and-process-words", "No process words in learner text", "course/modules/E/E5/L02.html:133, :272; index.html; L01-L03", "PASS",
  "Round-5 FAIL resolved: L02.html:133 no longer cites plans/E5-open-items.md (now 'Honest-pending note ... runs on a generated Cobb-Douglas economy labeled SIMULATED, and no number in it describes a real economy.'); L02.html:272 now reads 'no source for one is embedded in this program yet'. grep -i 'open item|plans/|verif|builder|round |todo|fixme|draft|twin' over index and L01-L03: no learner-text hit. 'Honest-pending' is a visible note label, not a process word; noted, not graded.")
R("E5a-hours-arithmetic", "Hours arithmetic", "index.html:29, :39-42, :146-153", "PASS",
  "8 lessons x 10 h = 80 lesson hours (data-hours=10 on L01-L08); 80 + 30 = 110 h; 80/110 = 72.7%, 30/110 = 27.3% (index.html:40, :42). Meta description '110 hours' matches.")
R("E5a-placement-arithmetic", "Placement counts and fractions", "index.html:70-139 (quiz), :72", "PASS",
  "Nine items: P0.1 x1, E1 x2 (Pq2, Pq6), M1 x2 (ln e^2, ln 1.1), M2 x2 (derivative of ln, implicit dy/dx), skill x2. Seven prerequisite items match the stated split. 7/9 = 77.8%, 8/9 = 88.9%. Implicit answer -0.25 checked (x y = 1: dy/dx = -y/x = -1/x^2 = -0.25 at x=2). Laspeyres skill answer 4/3 = 1.333333 checked (num 2*1+2*1=4, den 1*1+2*1=3).")
R("E5a-data-status-basis", "Data status matches the registry", "index.html:171; tools/data_sources.yaml:91-107", "PASS",
  "data_sources.yaml lists only fx_daily, fx_monthly and ust_daily (no national-accounts, price, unemployment or policy-rate series). tbill_3m discount basis and cmt_10y constant-maturity note at yaml:101-103. git diff 04626e9..9fd6aed on tools/data_sources.yaml is empty.")
R("E5a-r5-index-data-line", "Data line on the hub is accurate", "course/modules/E/E5/index.html:37", "PASS",
  "index.html:37: 'no embedded national-accounts, price, unemployment or policy-rate data. The labs use SIMULATED or illustrative numbers.' Checked against lab labels: L01 SIMULATED (L01.html:156), L02 SIMULATED (L02.html:137), L03 illustrative (L03.html:192), L04 illustrative (L04.html:182), L05 illustrative (L05.html:120), L06 SIMULATED (L06.html:114), L07 illustrative (L07.html:124), L08 illustrative (L08.html:92). Only data-files in the unit is project.html:351 ust_daily.csv.")
R("E5a-r5-hub-prereq-concept-status", "Prereq paragraph agrees with concept index status", "course/modules/E/E5/index.html:60 vs course/concepts.html:39, :40, :44, :70, :120, :125, :129, :302, :303", "PASS",
  "Round-5 FAIL resolved. index.html:60 now says the concepts of P0.1, E1 and M2 are not yet released and their links open 'not yet released' entries. concepts.html: derivative :120, implicit-function-theorem :125, partial-derivative :129 are 'not yet released'; comparative-statics :302 and competitive-equilibrium :303 are 'not yet released'; evidence-grade :39, project-ladder :40, notation-conventions :44 are 'not yet released'. exponential-and-logarithm :70 is 'defined here' (M1/L03), consistent with 'each concept from a built module is defined in that module'. E1 and M2 are not built (course/modules has E2, E3, E5 and M1, M6).")
R("E5a-L01-numbers", "Prose numbers match unrounded values and lab output", "L01.html:107-130, 156, 262-289, 298-310, 336-343, 355-439, 504-530", "PASS",
  "Recomputed by hand with exact fractions: basket A P^L = 50/40 = 5/4, P^P = 54/46 = 27/23, gap 7/92 = 0.076087; basket B P^L = 11/10, P^P = 19/10, gap -4/5; ln 1.25 = 0.223144; ln 1.1 = 0.095310; 1.1 minus ln 1.1 = 0.004690; x-ln(1+x) at 0.01/0.05/0.25 = 0.000050/0.001210/0.026856; nominal 1100/995 - 1 = 0.105528; real -1565/26865 = -0.058254; deflator 4/23 = 0.173913; (25300/26865)(27/23) = 220/199 = 1100/995 exactly; M1 Y = 655; M2 P^L = 9/7 = 1.285714; R2 price per quality 2 -> 1.5 (-25%) vs index +50%. Expected block (L01.html:293-310) equals output.")
R("E5a-L01-theorems", "Theorems, propositions and proofs are correct", "L01.html:70-152", "PASS",
  "Theorem 1.4 proof (exports added once, imports removed once), Proposition 1.7 (tax cancels; closed-economy S_p+S_g = I, with 160+20 = 180 = I at the lab inputs), Proposition 2.4 (both baskets), Proposition 2.5 (f' = x/(1+x), minimum at 0), Proposition 2.6 (product telescopes to N1/N0) all check on paper.")
R("E5a-L01-lab-claims", "Sentences about what the lab prints and checks match code and output", "L01.html:156, :157-292, :311", "PASS",
  "Hypothesis (L01.html:156): expenditure GDP 995, operating surplus 300, saving = investment 180, Laspeyres 5/4 vs Paasche 27/23, gap 7/92, basket B sign reversal, simple and log inflation of basket A. All match expected output lines 293-310 and the code. Interpretation (:311) says the lab does not say which sign real data show: consistent with the code (no real data).")
R("E5a-L01-simulated-label", "Lab labelled SIMULATED where it is generated", "L01.html:51, :156, :161, :311, :546", "PASS",
  "Accounts table and basket prices are typed integers and labelled SIMULATED in the docstring (L01.html:160-161) and in the hypothesis and interpretation.")
R("E5a-L02-numbers", "Prose numbers match unrounded values and lab output", "course/modules/E/E5/L02.html:368 (E3 solution); other L02 numbers PASS", "FAIL",
  "Recomputed independently (ledgers/E5/scripts/E5-a-r6/recompute.py): lab shares 0.362162 / 0.180872 / 0.456966; residual averages 0.016254 (alpha 0.2), 0.010665 (alpha 0.4), difference 0.005589 (unrounded 0.00558916); avg dlnK 0.0355562, avg dlnL 0.0076104; avg simple growth 0.029907; 1.1^0.3 = 1.029006; 0.3 ln 1.1 = 0.028593; 0.3 ln 2 = 0.207944; gap 1.3e-15. FAIL is E3 (L02.html:368): the solution says 'At alpha = 0.4 the average capital term is 0.4 x 0.035557 = 0.014223, to six decimal places'. The unrounded value 0.4 x 0.0355562 = 0.0142225 rounds to 0.014222 (recompute.out: 0.014222). The page's own basis is the printed 0.010667, which gives 0.014223 only through the rounded intermediate 0.035557. Fix: state the unrounded result 0.014222 and note that 0.014223 is obtained from the rounded intermediate 0.035557.")
R("E5a-L02-theorems", "Theorems and proofs are correct", "L02.html:72-131", "PASS",
  "Theorem 1.4 (log of product, same alpha subtracted per period), Proposition 1.5 (lambda^alpha lambda^(1-alpha) = lambda), Theorem 2.3 (rearrangement), Proposition 2.4 (Res(alpha) - Res(alpha') = -(alpha-alpha')(dlnK - dlnL); average equality iff average growth equal, given alpha != alpha') all check on paper.")
R("E5a-L02-lab-claims", "Sentences about what the lab prints and checks match code and output", "L02.html:137, :138-247, :262, :51", "PASS",
  "Hypothesis: gap zero to floating-point precision and True line; shares sum to 1; alpha 0.2 vs 0.4 change. Expected output (L02.html:248-261) equals output. Interpretation prints 0.029907 / 0.029453 and True. Twin docstring (L02 lines 140-149) matches the code (seed 2026, uniform draws, six-decimal printing).")
R("E5a-L02-simulated-label", "Lab labelled SIMULATED where it is generated; honest-pending note accurate", "L02.html:51, :133, :137, :138-141, :494", "PASS",
  "Round-5 FAIL resolved (open-items reference removed at :133). The note states no redistributable national-accounts series is embedded (true: data_sources.yaml lists none), and the lab is labelled SIMULATED throughout.")
R("E5a-L02-table-row-simple-growth", "Key-results rows match the page", "L02.html:405-408", "PASS",
  "Row 405 'residual equals Delta ln A inside the model' (T; Theorem 2.3; Lab 1 gap line) and row 408 'simple growth of output is not in general the capital-weighted sum' (T; Misconception 3) both match the page. Row 409 is C (single SIMULATED sample), consistent with L02.html:262.")
R("E5a-L03-numbers", "Prose numbers match unrounded values and lab output", "L03.html:52, :116, :147, :161-187, :383, :402-410, :430-500", "PASS",
  "ledgers/E5/scripts/E5-a-r6/recompute.out: k* = 5.5843115042, y* = 1.6752934513, dk/ds = 39.8879393156, dk/ddelta = -132.9597977186, elasticity 1.4285714286, first period gap < 1e-12 = 692, grid 27 below / 23 above / 0 mismatches. Problem values by hand: M1 k* = 25/4, y* = 5/2, c* = 15/8; M2 k1 = 23/20, k2 = 1.3030951324; M3 dk/ds = 50, dk/ddelta = -125; E1 ratio 0.1217 (0.12166); E2 0.3988793932, 7.14%, 1.4285714286 x 0.05 = 0.0714; E3 -0.1329597977. All match.")
R("E5a-L03-theorems", "Theorems, propositions and proofs are correct", "L03.html:70-187, 184-187, 527-531", "PASS",
  "Derivation 1.2, Remark 1.3, Proposition 2.2 (chain of equivalences; k^(1-alpha) = s/(n+delta)), Remark 2.3, Remark 2.5 (i)-(ii), Proposition 3.1 Steps 1-5 (sign lemma, monotonicity, induction, limits), Proposition 4.2 (H_k = -(1-alpha)(n+delta); -H_s/H_k = k*/((1-alpha)s); -H_delta/H_k = -k*/((1-alpha)(n+delta))) and Remark 4.3 all check on paper. Assumption 3.1 and 4.1 are used as stated and named.")
R("E5a-L03-lab-claims", "Sentences about what the lab prints and checks match code and output", "L03.html:52, :192, :376-381, :383", "PASS",
  "Hypothesis (L03.html:192): Part A residual zero, Part B ordered path and gap below 1e-12, Part C no sign mismatch, Part D IFT derivatives agree, Part E n and delta derivatives equal; expected output (L03.html:347-382) matches (sign_mismatches 0; within_tolerance True; equal_within_tolerance True). Interpretation (:383) names the one parameter set and grid of 50, and does not claim a rate.")
R("E5a-r5-L03-misconceptions", "Misconceptions and their numbers", "course/modules/E/E5/L03.html:399-411", "PASS",
  "401-402: dk/ds = 39.8879393156 printed by Part D; 406: Y_{t+1}/Y_t = 1+n, lab does not print aggregate output (true, no such line); 409-410: n and delta enter only via n+delta, Part E prints -132.9597977186 for both.")
R("E5a-r5-L03-R1-solution", "R1 solution is correct and states the right step", "course/modules/E/E5/L03.html:497-500", "PASS",
  "With delta = 1: n+delta = n+1 > 0 for n > -1, g(k) = s k^alpha/(1+n); sign lemma uses only n+delta > 0 and 1+n > 0; Step 2 needs 1-delta >= 0 (coefficient on k) and s/(1+n) > 0 on k^alpha; the statement correctly identifies Step 2 as the step that depends on 1-delta.")
R("E5a-r5-L03-remark-4.3", "Remark 4.3 elasticity", "course/modules/E/E5/L03.html:187", "PASS",
  "(s/k*) d k*/ds = (s/k*)(k*/((1-alpha)s)) = 1/(1-alpha) = 10/7 = 1.4285714286, printed by Part D (expected line 377). Lab prints both derivatives at Example 2.4 parameters (lines 370, 373).")
R("E5a-r5-L01-R2-cards", "Cards that restate L01 propositions match the lesson", "course/modules/E/E5/cards.json:88, :104 (E5-c014, E5-c016)", "PASS",
  "c014 (Proposition 2.4 both baskets, A1) and c016 (Proposition 2.6 hypotheses A1, A2, identity) match L01.html:125 and :146.")
R("E5a-r5-cards-L01-L03", "Cards agree with the current lesson text and carry the hypotheses", "course/modules/E/E5/cards.json E5-c001 to E5-c052", "PASS",
  "All 52 L01-L03 cards read this round. Hypotheses carried: c009 (A0-A2), c014/c015/c016 (A1, A2), c026/c027 (Assumption 1.3, A1 for c027), c041 (A1 to A3), c042/c044/c043 (A1 to A3, Assumption 4.1 where used), c046 (Assumption 3.1 and A1 to A4), c050/c051 (Assumption 4.1, A1 to A3). Each card's grade matches the lesson (T for propositions and derivations, C for lab numbers). No duplicate ids or fronts (cards.json: 130 cards, 0 duplicate ids, 0 duplicate fronts). Card c041 and c040 are consistent with L03.html:98 and :111.")
R("E5a-r5-cards-numbers-in-lessons", "Every card number appears in its lesson", "cards.json E5-c019..c052", "PASS",
  "Numbers on cards and their lesson locations: 0.026856 (L01.html:338), 105/995 and 0.105528 (L01:342), 4/23 and 0.173913 (L01:342), -0.058254 (L01:342), 160/20/180 (L01 expected block :296-297), 7/92 (L01:130), 0.016254 and 0.010665 (L02:281, expected :257-258), 0.005589 (L02:285), 0.362162/0.180872/0.456966 (L02:255, :354), 0.030000/1.029006/0.029006/0.028593 (L02:289), 692 (L03:364, :572), 39.8879393156 (L03:370, :402), -132.9597977186 (L03:373, :410), 1.4285714286 (L03:377, :507), 5.5843115042 and 1.6752934513 (L03:116, :348-349). All appear.")
R("E5a-r5-DAG-concept-links", "Concept links and DAG closure", "index.html; L01-L03 data-concept links", "PASS",
  "check_dag E5: PASS. Links used in L01-L03 resolve: national-accounts (L01.html:57 anchor), price-index-inflation (L01:115), growth-accounting (L02:97), total-factor-productivity (L02:104), solow-model (L03:60), mathematical-induction (concepts.html:77 -> M1/L06), partial-derivative and implicit-function-theorem (not yet released, concepts.html:125, :129), exponential-and-logarithm (defined in M1/L03), derivative (not yet released, :120), notation-conventions and evidence-grade (P0.1, not yet released).")

# new round-6 rows
R("E5a-r6-delta-read", "Round-6 delta read hunk by hunk", "index.html:37, :60; L02.html:133, :272; cards.json c042-c051 (lines 295-370); L03 unchanged", "PASS",
  "git diff 04626e9..9fd6aed for the slice: index.html (2 hunks: 37, 60), L02.html (2 hunks: 133, 272), cards.json (E5-c042, c043, c044, c045, c051, c058, c068, c116; c058/c068/c116 are not L01-L03 cards). L01.html, L03.html and twins tests/labs/E5/lab-E5-L0{1,2,3}-1.py are byte-identical to the previous pin. Every hunk read; the changed sentences were re-verified above.")
R("E5a-r6-hub-lede-static-claim", "Hub lede claims about the model's dynamics are accurate", "course/modules/E/E5/index.html:33 ('closed-economy and static, except for the Solow recursion'); L06.html:73, :183, :234", "FAIL",
  "index.html:33: 'The module is closed-economy and static, except for the Solow recursion'. Lesson 6 has a dynamic model: Assumption A3 is 'adaptive expectations' (L06.html:73), and Lab 1 Part B prints 'seeded SIMULATED path of 12 periods, adaptive expectations' (L06.html:183, :234). A path over periods is not static. Fix: 'except for the Solow recursion and the adaptive-expectations path of Lesson 6'.")
R("E5a-r6-L03-refs-all-T", "Grade claims in the references paragraph are accurate", "course/modules/E/E5/L03.html:611", "FAIL",
  "L03.html:611 says 'Each result on this page is derived here (grade T) from Assumptions A1 to A4'. But the page also reports values Lab 1 prints and that are not derived on the page: 'first period ... is 692' (cards E5-c048 graded C, L03.html:364), k* and y* to ten decimal places (L03.html:116, card E5-c052 graded C), and the Part D/E derivatives matched by central differences (L03.html:383). These are lab readings, graded C per the unit's convention (cards c048, c052). Fix: 'Each result proved on this page is graded T from Assumptions A1 to A4; the values that Lab 1 prints are graded C and name the lab.'")

FIXES = {
 "E5a-L02-numbers": "Edit L02.html:368 to state 0.014222 (0.4 x unrounded 0.0355562 = 0.0142225) and say that 0.014223 follows only from the rounded intermediate 0.035557. Then re-run the twin check.",
 "E5a-r6-hub-lede-static-claim": "Edit index.html:33 to read 'closed-economy, and static except for the Solow recursion and the adaptive-expectations path of Lesson 6' (or drop 'static' and state the dynamic element), so it matches L06.html:73 and :183.",
 "E5a-r6-L03-refs-all-T": "Edit L03.html:611 to: 'Each result proved on this page is graded T from Assumptions A1 to A4; the values Lab 1 prints (for example the first period 692 and the printed derivatives) are graded C and name the lab.'",
}
for r in rows:
    if r["status"] != "PASS":
        r["fix"] = FIXES[r["id"]]
rows_sorted = rows
fragment = {
 "unit": "E5",
 "slice": "a",
 "round": 6,
 "verifier": "Haiku independent verifier, E5-a round 6 (did not build E5)",
 "pin": "9fd6aed",
 "base": "04626e9 (round-5 pin). Delta in slice: index.html (lines 37, 60), L02.html (lines 133, 272), cards.json (E5-c042, c043, c044, c045, c051 in L03; c058, c068, c116 outside slice). L01.html, L03.html and the three twins are byte-identical to 04626e9.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC6-E5-a",
 "scratch": "/tmp",
 "verified_at": "2026-10-29",
 "verdict": "FAIL",
 "rows": rows_sorted,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [
   "Outside slice a (noted, not graded here): course/modules/E/E5/project.html:343 still cites 'plans/E5-open-items.md' in learner text ('the request for a redistributable source is recorded in the DATA_REQUEST entry of plans/E5-open-items.md'). This is the same class of process reference fixed at L02.html:133 and :272 in this round; it belongs to the project slice.",
   "Outside slice a (noted, not graded here): cards.json E5-c058 and E5-c068 (L04) and E5-c116 (L07) changed in 9fd6aed; they are not L01-L03 cards."
 ],
 "notes": "Mutants: none. Lesson pages carry no project graders, and lab twins are demonstrations under the rulings, so no mutants were required or run. Every page and twin was read line by line (index.html 1-188; L01.html 1-559; L02.html 1-496; L03.html 1-624; twins L01 136 lines, L02 110, L03 154). Prose numbers were recomputed by hand and by ledgers/E5/scripts/E5-a-r6/recompute.py. Alternative correct implementations were not run because no project grader is in this slice. Not checked: project.html, L04-L08 (other slices); full pytest suite (only -k E5, 12 tests); run_graders and mutate_graders (not applicable to lessons). The rule-(9) question of whether lab-read values should be C is applied to L03.html:611 as a FAIL row; the 'honest-pending' label is kept as a visible note label and not graded as a process word.",
 "summary": "E5-a round 6: FAIL. 3 new non-PASS rows: E5a-r6-hub-lede-static-claim (index.html:33 says the module is static except the Solow recursion, but Lesson 6 uses adaptive expectations with a 12-period path); E5a-r6-L03-refs-all-T (L03.html:611 says each result is T, but lab-read values such as 692 are graded C); E5a-L02-numbers (L02.html:368 gives 0.014223 for the average capital term at alpha = 0.4, the unrounded value is 0.014222). The three round-5 FAIL rows (banned process words at L02:133/:272, L02 SIMULATED label, hub prereq concept status at index:60) are fixed and PASS. All commands pass on 9fd6aed (check_pages, check_dag, check_projects, run_labs, page_smoke, twins under -I -W error, ruff, mypy, pytest -k E5, verify_refs --offline)."
}
json.dump(fragment, open("ledgers/E5/E5-a.json", "w"), indent=1, ensure_ascii=False)
print("rows", len(rows), "fails", sum(1 for r in rows if r["status"] != "PASS"))
