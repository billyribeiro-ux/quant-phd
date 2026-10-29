"""Builds ledgers/M7/M7-b.json (round 3, slice M7-b) from rows decided in this round; validates it with tools/ledger.py."""
import json, sys
from pathlib import Path

ROOT = Path("/tmp/verifyB3-M7-b")
P = "PASS"; FL = "FAIL"
CARRY = "Re-verified in round 3 on pin aa3c26c (L04-L06 pages and cards changed since 1817191; lab-L05 twin unchanged but re-run): "
rows = []
def R(id_, check, loc, status, ev, fix=None):
    r = {"id": id_, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != P:
        r["fix"] = fix
    rows.append(r)

R("M7b-cmd-check-pages", "tools/check_pages.py (command row)", "course/modules/M/M7/L04.html, L05.html, L06.html; tools/check_pages.py", P,
  CARRY + "`.venv/bin/python tools/check_pages.py --unit M7 --page L04|L05|L06` -> 'check_pages M7 L04: PASS', 'L05: PASS', 'L06: PASS'; `--unit M7` -> 'check_pages M7: PASS'.")
R("M7b-cmd-check-dag", "tools/check_dag.py (command row)", "course/modules/M/M7/*.html; tools/check_dag.py", P,
  CARRY + "`.venv/bin/python tools/check_dag.py --unit M7` -> 'check_dag M7: PASS'.")
R("M7b-dag-prose-terms", "DAG: out-of-closure concepts by link or name (plan section 2, section 8.2 item 5)", "L04.html:275, 503; L05.html:89; L05.html:52; L06.html:60, 548-549", P,
  CARRY + "Links on L04-L06 point only to closure or own-unit concepts: gradient, hessian, positive-semidefinite-matrix (M2/M3), kkt-conditions, lagrange-multiplier, convex-function (L01-L03), quadratic-programming and linear-portfolio-constraints, mean-variance-optimization (own unit). No link to covariance-matrix, variance, correlation, contraction, efficient-frontier, convexity, newtons-method. 'convexity' (L04.html:275, 503; L05.html:89) and 'variance' (L06 passim) are plain prose with no dfn and no link, which plan section 8.2 item 5 allows. 'covariance' occurs once on L06.html:56, inside the no-link disclaimer that Architect decision B1/Q1 permits.")
R("M7b-cmd-run-labs", "tools/run_labs.py (command row)", "tests/labs/M7/lab-M7-L04-1.py, lab-M7-L05-1.py, lab-M7-L06-1.py", P,
  CARRY + "`.venv/bin/python tools/run_labs.py --unit M7 --page L04` (and L05, L06) -> 'run_labs M7: PASS (1/1)' each.")
R("M7b-lab-L04-twin-run", "L04 twin under python -I -W error", "tests/labs/M7/lab-M7-L04-1.py", P,
  CARRY + "`.venv/bin/python -I -W error tests/labs/M7/lab-M7-L04-1.py` exit 0. ledgers/M7/scripts/M7-b-r3/embed_compare.py: page code == twin: True; 'L04 expected == run output: True'. Output: 1331 dual points, 21 primal, 27951 of 27951 pairs, largest dual -1/2 at lambda (0, 3/10), nu -1/2, one attaining point, grid gap 0, g(0,0) -199/300, KKT check True.")
R("M7b-lab-L05-twin-run", "L05 twin under python -I -W error", "tests/labs/M7/lab-M7-L05-1.py", P,
  CARRY + "exit 0; embed_compare.py: page code == twin: True; 'L05 expected == run output: True' (kkt_determinant 19; x 13/19 3/19 3/19; lambda -36/19 11/19; residual maxima 0.0e+00; passing_candidates 1; grid_points 1089; grid_points_below_candidate 0).")
R("M7b-lab-L06-twin-run", "L06 twin under python -I -W error", "tests/labs/M7/lab-M7-L06-1.py", P,
  CARRY + "exit 0; embed_compare.py: page code == twin: True; 'L06 expected == run output: True'. Part B candidates_passing 1 and zero set {A4} at all five gammas; Part D turnover 0.558861; 20 of 20 perturbations.")
R("M7b-lab-lint-types", "ruff and mypy strict on the three twins", "tests/labs/M7/lab-M7-L04-1.py, lab-M7-L05-1.py, lab-M7-L06-1.py", P,
  CARRY + "`.venv/bin/ruff check tests/labs/M7` -> 'All checks passed!'; `.venv/bin/ruff format --check tests/labs/M7` -> '11 files already formatted'; `.venv/bin/mypy --no-incremental --strict` on the three twins -> 'Success: no issues found in 3 source files'.")
R("M7b-lab-pytest", "pytest tests/test_labs.py", "tests/test_labs.py", P,
  CARRY + "`.venv/bin/pytest -q tests/test_labs.py` -> progress reaches [100%] with no failure or error line.")
R("M7b-smoke", "page_smoke in Pyodide timing", "course/modules/M/M7/L04.html, L05.html, L06.html", P,
  CARRY + "`.venv/bin/python tools/page_smoke.py --unit M7 --pages L04 L05 L06` -> 'page_smoke M7: PASS', exit 0; lab-M7-L06-1 0.0 s, lab-M7-L04-1 and L05 also PASS.")
R("M7b-refs-live", "registry checks for the slice", "references/references.json; course/modules/M/M7/L04.html, L05.html, L06.html (data-references lists, empty)", P,
  CARRY + "`.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems'; `.venv/bin/python tools/verify_refs.py --unit M7` (live) -> 'live re-verification of M7: 2 of 560 entries, 0 problems'. The three pages cite no registry key: `<ol data-references></ol>` on each.")
R("M7b-citation-boyd-attribution", "no bibliographic attribution in the slice", "course/modules/M/M7/L04.html, L05.html, L06.html, cards.json", P,
  CARRY + "`grep -ci boyd` on L04.html, L05.html, L06.html and cards.json -> 0 each. No Boyd or Stokey locator, theorem number or coefficient appears in the slice.")
R("M7b-2.2-numbers-L04", "numbers in prose, L04", "course/modules/M/M7/L04.html:118-125, 126, 147-160, 267-268, 275, 283-295, 329-402; ledgers/M7/scripts/M7-b-r3/num_L04_indep.py", P,
  "Independent exact recomputation (Fraction, num_L04_indep.py): g(0,0) = -199/300; mu'Sigma^{-1}mu = 199/150 (M3, L04.html:357-361); g(0,-3/5) = g(0,-7/10) = -157/300; g(0,-13/20) = -209/400; restricted grid gap 7/300 (R3, L04.html:396-402); -199/300 - (-1/2) = -49/300 (E2, misconception 1); grid 1331 x 21 = 27951 (E1); largest grid dual -1/2 attained at 1 point; smallest primal -1/2; grid gap 0 (E3). Displayed decimal -0.6633 (-0.66333...) is consistent.")
R("M7b-2.2-numbers-L05", "numbers in prose, L05", "course/modules/M/M7/L05.html:156, 175-179, 390, 398-399, 439, 462-496; ledgers/M7/scripts/M7-b-r3/num_L05_indep.py", P,
  "num_L05_indep.py: det K = 19 (numpy 18.999999999999996 agrees); x = (13,3,3)/19; lambda = (-36,11)/19; stationarity and constraint residuals exactly 0; objective 29/38 = 551/722 = 0.7631578947...; Qv = (-7,2,3) for v = (-2,1,1) and v'Qv = 19; null-line identity exact; Part B: {} (primal False), {2} (both True, x = (3/2,0), objective -9/4), {1} (both False), {1,2} (dual False); grid 33 x 33 = 1089, none below -9/4. E1 derivation: x'Qx = 817/361, c'x = -7/19 = -266/722, sum 551/722 verified.")
R("M7b-2.2-numbers-L06", "numbers in prose, L06", "course/modules/M/M7/L06.html:405, 428, 432, 445-462, 477-514, 524-538, 580-625; ledgers/M7/scripts/M7-b-r3/num_L06_indep.py", P,
  "num_L06_indep.py (independent LCG and Fraction solves): mu = 7/100, 1/20, 3/25, 1/50; diagonal 49/40, 27/20, 103/80, 103/80; Part A returns 0.113798 ... 0.106241 and variances 0.123809 ... 0.115780 match; objective 0.820002 at gamma 16; constrained 1.392257; unrounded difference 0.57225483 -> 0.572255 (E2); turnover at gamma 4 exact 67597/120955 = 0.5588607 -> 0.558861 (E3/Part D); printed-weight turnover 27943/50000 = 0.558860 (E3); weights at gamma 1 (0.388425, 0.203679, 0.407895, 0) match.")
R("M7b-2.2-misc-numbers", "remaining numeric claims in interpretations and misconceptions", "course/modules/M/M7/L06.html:405, 414, 428, 504, 511; L05.html:390, 482; L04.html:287, 291", P,
  "Checked against exact output and num_L06_indep.py: A4 weight negative at all five gammas (-0.524154 ... -0.409145); return falls 0.113798 -> 0.106241 and variance 0.123809 -> 0.115780 (monotone, 5 values); constrained objective >= unconstrained at 5 gammas (5 True lines); all four weights change at gamma 1 (misconception 2). L05 0.7632 vs 551/722 (within 5e-5).")
R("M7b-2.3-grades-L04", "grades of L04 claims", "course/modules/M/M7/L04.html:405-421 (key results), 49-51", P,
  CARRY + "T rows Prop 1.2, 1.3, 1.4, 2.1, Example 2.2, Example 3.4 each re-proved from the page (see M7b-2.4-L04-proofs). The lab row and the grid row are C with basis Lab 1. No T row depends on a lab output or on Slater's condition.")
R("M7b-2.3-grades-L05", "grades of L05 claims", "course/modules/M/M7/L05.html:527-542 (key results)", P,
  CARRY + "All six rows are T with proofs on the page (Lemma 1.4, Theorem 2.3, Remark 2.4 minimiser line, Theorem 3.1, Proposition 3.4, Example 3.6). Lab rows are described as checks of one instance.")
R("M7b-2.3-grades-L06", "grades of L06 claims", "course/modules/M/M7/L06.html:542-556 (key results); course/modules/M/M7/cards.json M7-c118", P,
  CARRY + "Rows 1 to 4 are T with proofs on the page (Theorem 1.3, Proposition 2.1, Proposition 2.3, Proposition 3.4). Row 5 ('closed form and KKT solve agree exactly for the simulated inputs') is C with basis Lab 1, Part A, and the identity itself is Theorem 1.3 (T). Card M7-c118 is C with the same basis.")
R("M7b-cards-L04-c056-c065", "cards M7-c056 to c065 against L04 text", "course/modules/M/M7/cards.json M7-c056..c065; course/modules/M/M7/L04.html:55-268", P,
  CARRY + "Each card read against its lesson paragraph and proof: Def 1.1 (c056), Prop 1.2 (c057), Prop 1.3 (c058), Prop 1.4 (c059), Remark 1.5 and Problem R3 (c060, 7/300), Prop 2.1 (c061), Example 2.2 (c062), Lab 1 numbers (c063, 1331, 21, 27951, C), M3 (c064, 199/150), Def 3.1 (c065). Duplicate status is in M7b-cards-duplicates.")
R("M7b-cards-L04-c066-c072", "cards M7-c067 to c071 against L04 text", "course/modules/M/M7/cards.json M7-c067..c071; course/modules/M/M7/L04.html:259-295", P,
  CARRY + "c066 and c072 are absent. c067 (Remark 3.3), c068 (Example 3.4: g(0) = -infinity, g(lambda) = -1/(4 lambda)), c069 and c070 (misconceptions) and c071 (the implication uses only Propositions 1.3 and 1.4) match L04.html:267-295.")
R("M7b-cards-L05-c073-c084", "cards M7-c073 to c084 against L05 text", "course/modules/M/M7/cards.json M7-c073..c084; course/modules/M/M7/L05.html:58-172", P,
  CARRY + "Each card read against its L05 statement or proof. c080 decomposition and v'Qv = 19 recomputed exactly. c084 midpoint identity f((x+y)/2) = (f(x)+f(y))/2 - (1/8)(x-y)'Q(x-y) re-derived, matching L05.html:164-166. c083 repeats the Theorem 2.3 sentence that M7b-r3-L05-def33-theorem23-hypothesis fails.")
R("M7b-cards-L05-c085-c096", "cards M7-c085 to c093 against L05 text", "course/modules/M/M7/cards.json M7-c085..c093; L05.html:128-180, 390-496", P,
  CARRY + "c085 to c093 match Remark 3.5, Example 3.6, Lab 1 Part B (c086-c089, C), misconceptions (c091-c093) and Remark 2.4 (c093 C with basis Lab 1 Part A). c094 to c096 are absent. The duplicate pair c082/c092 is recorded in M7b-cards-duplicates.")
R("M7b-cards-L06-c097-c108", "cards M7-c097 to c108 against L06 text", "course/modules/M/M7/cards.json M7-c097..c108; course/modules/M/M7/L06.html:58-146", P,
  CARRY + "Definitions 1.1, 1.2, 3.1, 3.2; Theorem 1.3 (c100); Remark 1.4 (c101); Prop 2.1 (c102); Prop 2.3 (c103); Prop 3.4 (c106 and c107 via Remark 3.3 and 3.5); c099 says estimating a covariance matrix is outside M7 (L06.html:56). c108 values match the printed mu (C, SIMULATED).")
R("M7b-cards-L06-c109-c120", "cards M7-c108 to c118 against L06 text and output", "course/modules/M/M7/cards.json M7-c108..c118; course/modules/M/M7/L06.html:404-430, 552", P,
  CARRY + "c109 to c115 and c117 match the printed values (c110 objective -0.051893; c112 weights 0.388425, 0.203679, 0.407895, 0.000000; c113 difference 0.5722548 before rounding; c114 turnover 0.5588607 before rounding and 0.558860 from printed weights, both recomputed). c116 lists the four weights of L06.html:428. c118 is C. c119 and c120 are absent.")
R("M7b-cards-duplicates", "full duplicate scan of L04-L06 cards (VERIFIER_RULES 2.7)", "course/modules/M/M7/cards.json: c058/c069, c059/c071, c082/c092", FL,
  "Full scan of the 63 cards M7-c056..c118 (all read). Pairs with the same locator and the same answer: c058 (weak duality, Prop 1.3: 'g <= p*, hence d* <= p*') and c069 (misconception: a dual value strictly below p* is not a violation, Prop 1.3); c059 (grid bound, Prop 1.4 with weak duality: 'p* - d* >= 0') and c071 (a zero grid gap forces zero gap, Prop 1.4 and Prop 1.3); c082 (Remark 3.2: x = 0 has multiplier -1, not optimal) and c092 (Remark 3.2: a stationary point with a negative multiplier is not optimal). Round-2 pairs c056/c070 (c056 no longer says 'maximizes g'; locator Def 1.1 vs Prop 1.3) and c106/c117 (locators Remark 3.3 vs Prop 3.4) are not duplicates in the current text.",
  "Merge each pair into one card: keep c058 and delete c069 (or reword c069 to test the misconception 'a dual value below p* violates weak duality' with a different answer such as the grid-gap question); keep c059 and reword c071 as the misconception card with the zero-gap consequence only if it is not the same answer, otherwise delete it; keep c082 and delete c092 (or change c092 to test the sign convention of the KKT multiplier, a different fact).")
R("M7b-2.9-structure", "template sections of L04-L06", "course/modules/M/M7/L04.html, L05.html, L06.html", P,
  CARRY + "Section order in all three: why-it-matters, core sections, lab, where the canon breaks, misconceptions (3 each), problem set (Mechanics, Proof, Empirical, Research, 3 each, every solution in details.solution), key results, retrieval quiz (L04 10 items, L05 10, L06 11), references. check_pages PASS.")
R("M7b-2.9-banned", "banned phrases and ellipses", "course/modules/M/M7/L04.html, L05.html, L06.html", P,
  CARRY + "check_pages banned-string scan PASS on all three pages. Remaining '...' are list notation in code docstrings (L04 grid docstring, L06 docstring) and decimal ellipses (E2 in L04, 0.6633...). No TODO, TBD, lorem, 'roughly', 'about <digit>', 'historically', 'it is important'.")
R("M7b-2.9-process-words", "no process words in learner text", "course/modules/M/M7/L04.html, L05.html, L06.html", P,
  CARRY + "grep -in for build, builder, verifier, round, REQUEST, unit report in the three pages: no process-word hit ('rounding' and 'rounds' are arithmetic).")
R("M7b-hours", "hours arithmetic (rule only; pace not judged, architect ruling)", "course/modules/M/M7/index.html (data-hours-lessons); L01..L08.html data-hours", P,
  CARRY + "index.html data-hours-lessons=77; lesson data-hours L01 9, L02 9, L03 10, L04 10, L05 10, L06 10, L07 9, L08 10; sum 77. Hub card labels L03-L06 read 10 h. Pace not judged.")
R("M7b-L04-prop32", "cross-reference to Lesson 3 result", "course/modules/M/M7/L04.html:256; course/modules/M/M7/L03.html:134", P,
  CARRY + "L04.html:256 now reads 'It is the hypothesis of Open item 3.2 in Lesson 3, the necessity statement'. L03.html:134 is 'Open item 3.2 (KKT necessity under Slater's condition)'. grep -c 'Proposition 3.2' L04.html -> 0.")
R("M7b-L04-lab-numbering", "lab numbering in L04-L06", "course/modules/M/M7/L04.html:125 and later; cards M7-c060, c063, c071", P,
  CARRY + "grep -c 'Lab 2' on L04.html, L05.html, L06.html -> 0 each; 'Lab 1' is the only lab label. Cards say Lab 1.")
R("M7b-L04-quiz-hypotheses", "quiz item 10 and its explanation", "course/modules/M/M7/L04.html:497-503", P,
  CARRY + "Correct option 'A KKT point, with differentiable convex f and g_i and affine h_j' matches Proposition 2.1 (L04.html:83-87). Explanation names Lemma 1.4 of Lesson 3 and says Slater's condition is not needed. Distractors are not sufficient.")
R("M7b-L04-causal", "causal and directional claims", "course/modules/M/M7/L04.html:295; cards M7-c071", P,
  CARRY + "'The implication uses only Propositions 1.3 and 1.4' is a statement about the proof: grid gap 0 gives p*-d* <= 0 by Prop 1.4 and >= 0 by Prop 1.3. 'exact arithmetic makes the printed zero exact' is about the printed number and is correct.")
R("M7b-L04-term-before-definition", "terms used before definition (BUILDER_RULES 10)", "course/modules/M/M7/L04.html:7, 252, 255-256, 126 (lab hypothesis)", P,
  CARRY + "'Slater' first appears at L04.html:7 (meta description), then in the section heading (252) and Definition 3.1 (255-256). The Lab 1 hypothesis (line 126) now says 'should satisfy both inequality constraints strictly and the budget exactly' with no Slater term. 'Dual feasible' is defined in Definition 1.1 before its later use.")
R("M7b-L05-lemma14", "Lemma 1.4 convexity proof", "course/modules/M/M7/L05.html:83-89", P,
  CARRY + "Chord identity theta f(x) + (1-theta) f(y) - f(z) = (1/2) theta (1-theta) (x-y)'Q(x-y) re-derived by expansion; linear terms cancel; theta - theta^2 = theta(1-theta) used correctly.")
R("M7b-L05-prop34-step", "Proposition 3.4 proof step", "course/modules/M/M7/L05.html:160-166", P,
  CARRY + "f(x)+f(y) = 2f(z)+u'Qu with u = (x-y)/2 and u'Qu = (1/4)(x-y)'Q(x-y) re-derived, so f(z) = (f(x)+f(y))/2 - (1/8)(x-y)'Q(x-y).")
R("M7b-L05-why-xref", "cross-reference in why-it-matters", "course/modules/M/M7/L05.html:52, 160", P,
  CARRY + "L05.html:52 cites Proposition 3.4 (midpoint result, at L05.html:160). grep -c 'Proposition 3.6' L05.html -> 0. Example 3.6 is at L05.html:175.")
R("M7b-L05-misc3", "misconception 3 sign and rank claim", "course/modules/M/M7/L05.html:417", P,
  CARRY + "Gradient at the minimiser is -A'lambda*, zero exactly when lambda* = 0 because A has full row rank (A' has full column rank). Remark 2.4 multipliers (-36/19, 11/19) checked: Qx* + c = (36,25,47)/19 = -A'lambda*.")
R("M7b-L05-canon-heading", "canon-breaks heading and first bullet", "course/modules/M/M7/L05.html:396", P,
  CARRY + "Heading 'An indefinite Hessian can leave a QP with no minimiser' is qualified by the body (a QP can have no minimiser, Misconception 1). Misconception 1 example Q = diag(1,-1) gives f(0,t) = -t^2/2 (unbounded) as stated.")
R("M7b-L05-lab-variables", "lab description of variables and candidates", "course/modules/M/M7/L05.html:390", P,
  CARRY + "'three variables in Part A and two in Part B, examines four candidate sets': output 'part_a_dimensions variables 3 constraints 2' and four candidate lines in Part B.")
R("M7b-L05-why-scope", "scope of why-it-matters sentence", "course/modules/M/M7/L05.html:52", P,
  CARRY + "'A quadratic program minimises a quadratic objective under linear constraints' matches Definition 1.1; no application claim.")
R("M7b-L06-why-scope", "scope of why-it-matters sentence", "course/modules/M/M7/L06.html:52", P,
  CARRY + "'The mean-variance problem of this lesson is a quadratic program' is scoped to this problem; no claim about all portfolio choice.")
R("M7b-L06-partB-count", "Part B enumeration count", "course/modules/M/M7/L06.html:150, 168-170, 291-294; tests/labs/M7/lab-M7-L06-1.py (nonnegative_candidates)", P,
  CARRY + "'15 sets that leave at least one asset free': the twin loops over 2^4 masks and skips the all-fixed mask with 'if not free: continue'. Page hypothesis, docstring and code agree.")
R("M7b-L06-partD-true", "Part D printed checks", "course/modules/M/M7/L06.html:431-432, 401-403 output", P,
  CARRY + "Output lines: linear_form_feasible True, linear_form_sum_equals_turnover True, feasible_perturbations_at_least_turnover 20 of 20. Page text matches.")
R("M7b-L06-misc2", "misconception 2 weights", "course/modules/M/M7/L06.html:427-428; output lines 376-387", P,
  CARRY + "All four changed weights (0.434783 to 0.388425; 0.526836 to 0.203679; 0.562535 to 0.407895; -0.524154 to 0) match the output.")
R("M7b-L06-covariance-docstring", "covariance wording in lab docstring and prose", "course/modules/M/M7/L06.html:56; tests/labs/M7/lab-M7-L06-1.py:1-30", P,
  CARRY + "grep -n covariance on L06.html gives one hit (line 56, the permitted disclaimer). grep -n covariance on the twin gives no hit.")
R("M7b-L06-R1-unproved", "Research problem R1 proof", "course/modules/M/M7/L06.html:518-524", P,
  CARRY + "R1 takes the limit of P3 (mu/gamma -> 0 and 1'mu/gamma -> 0) and cites Theorem 1.3 for uniqueness at mu = 0; the limit 1/n 1 is correct.")
R("M7b-L06-term-before-definition", "terms used before definition in L06", "course/modules/M/M7/L06.html:52, 124-125", P,
  CARRY + "Why-it-matters (line 52) says 'a sum of absolute values' without the term 'turnover'; 'turnover' is first defined in Definition 3.2 (line 124). Meta description (line 7) is not learner prose.")
R("M7b-L06-lab-claims-ok", "claims about what the L06 lab prints", "course/modules/M/M7/L06.html:404-405 (interpretation), 150, 168-170", P,
  CARRY + "Each sentence checked against the output: budget True at each gamma; A4 negative at five gammas; return falls 0.113798 -> 0.106241; variance falls 0.123809 -> 0.115780; zero set {A4}; constrained objective >= unconstrained at each gamma; Part D turnover 0.558861. Hypothesis: gammas 1, 2, 4, 8, 16; 15 sets; Part D at gamma 4; all match.")
R("M7b-2.4-L04-proofs", "proof re-derivation, L04", "course/modules/M/M7/L04.html:67-115, 254-273, 329-412", P,
  CARRY + "Prop 1.2 (infimum of a sum >= sum of infima); Prop 1.3 (lambda_i g_i <= 0, h_j = 0); Prop 1.4 (inequalities between min over F~, max over D~, p*, d*; finiteness used only for existence of min and max); Prop 2.1 (phi convex, gradient zero by K1, Lemma 1.4 and Theorem 2.1 of L03, weak duality); Example 2.2 (Sigma pd by a^2+b^2+(a+b)^2; g formula); Example 3.4 (g(lambda) = -1/(4 lambda), sup 0 not attained); KKT check of (lambda*, nu*) = ((0,3/10), -1/2) at w* = (1,0) (stationarity (1/2 - 1/2, 4/5 - 3/10 - 1/2) = 0).")
R("M7b-2.4-L05-proofs", "proof re-derivation, L05", "course/modules/M/M7/L05.html:70-180", P,
  CARRY + "Lemma 1.3 expansion; Lemma 1.4 tangent and chord inequalities; Prop 2.1 (K nonsingular via x'Qx = 0 and full row rank); Remark 2.2 determinant (rows 3 and 4 coincide); Theorem 2.3 (d'Qd > 0 when d != 0); Remark 2.4 decomposition and null direction; Theorem 3.1 (sum of nonnegative terms); Remark 3.2; Prop 3.4 (midpoint identity); Remark 3.5; Example 3.6; R1 and R2 (separable with R1).")
R("M7b-2.4-L06-proofs", "proof re-derivation, L06", "course/modules/M/M7/L06.html:68-146", P,
  CARRY + "Theorem 1.3 (KKT solve, lambda formula, 1'b = b'Sigma b > 0 from Sigma b = 1); Remark 1.4; Prop 2.1 (two minimality inequalities; R2 - R1 >= (gamma2/2)(V2 - V1) >= 0); Prop 2.3 (inclusion of feasible sets, infimum convention, recorded in notes); Prop 3.4 (both directions, t_i = |d_i|, no sign assumption on tau: both sides false for tau < 0).")
R("M7b-2.4-quiz", "numeric and multiple-choice keys", "course/modules/M/M7/L04.html:423-506; L05.html:544-623; L06.html:558-641", P,
  CARRY + "L04 numeric keys -0.5 (exact), 2 (exact), -0.6633 with tolerance 5e-5 (-199/300 = -0.663333, diff 3.3e-5); L05 19 (exact), 0.7632 (551/722 = 0.763158, diff 4.2e-5 < 5e-5), -2.25 (exact), 19 (exact); L06 0.113798 (exact 0.1137977, diff 2.7e-7 < 5e-7), 0.184631 (0.1846313, diff 3e-7), 0.007996 (0.0079963, diff 3e-7), 0.2 (exact), 0.5125 (exact). Multiple-choice keys checked against lesson statements.")
R("M7b-2.5-L04-misc", "lab-hypothesis and interpretation claims, L04", "course/modules/M/M7/L04.html:126, 249, 285-295, 372-374", P,
  CARRY + "The grid contains (0, 3/10) and -1/2 (lambda_2 = 3/10, nu = -1/2 on the 1/10 grid): 'the grid happens to contain the dual optimum' holds. 'The grid gap of 0 is exact' holds with exact Fractions. -199/300 as a lower bound strictly below p* is correct by Proposition 1.3.")
R("M7b-footer-L05-L06", "footer claims against the page", "course/modules/M/M7/L05.html:627, 638; L06.html:646, 657; L04.html footer", P,
  CARRY + "L05 and L06 footers now read 'Each lemma, proposition and theorem carries an evidence grade, and this lesson cites no registry source', matching their references sections ('cites no outside source'; empty data-references). L04 footer 'Each graded result carries a proof or a lab result labelled C' is accurate.")
R("M7b-r3-L05-def33-theorem23-hypothesis", "Definition 3.3 uses Theorem 2.3 without its positive definiteness hypothesis", "course/modules/M/M7/L05.html:156 ('When it exists, it is found from Theorem 2.3 if the rows used are independent.'); Theorem 2.3 at L05.html:114-115 requires Q symmetric positive definite and A full row rank; card M7-c083 back repeats the sentence", FL,
  "Theorem 2.3 needs Q positive definite AND A of full row rank (L05.html:114-115, card M7-c079). The sentence in Definition 3.3 gives only the independence of the rows used and omits positive definiteness of Q (restricted to the free components). A reader applying the sentence to an indefinite Q would apply Theorem 2.3 outside its hypotheses. The sentence is not graded, but it is a precise method claim.",
  "Change L05.html:156 to: 'When it exists, it is found from Theorem 2.3 if the restriction of Q to the free components is positive definite and the rows used are independent.' Make the same change in cards.json M7-c083 back.")
R("M7b-r3-L06-def11-variance-identity", "Definition 1.1 identifies w'Sigma w with a portfolio variance without the hypothesis that Sigma is the return covariance matrix", "course/modules/M/M7/L06.html:60 ('The first term is gamma times half the variance of the portfolio return'); L06.html:412 ('the variance of the return'); Section 1 at L06.html:56 declares Sigma a given SPD input", FL,
  "The identity 'w'Sigma w is the variance of the portfolio return' holds only when Sigma is the covariance matrix of the one-period returns. Section 1 (L06.html:56) declares Sigma a given symmetric positive definite input and never states that it is that covariance matrix; it only says estimating a covariance matrix is outside M7. The claim in Definition 1.1 and the canon-breaks line at L06.html:412 therefore rest on an unstated hypothesis. Definition text is not a graded theorem, but the identity is asserted as fact.",
  "State the hypothesis where the identity is made: 'If Sigma is the covariance matrix of the one-period returns, which this unit takes as an input, the first term is gamma times half the variance of the portfolio return.' Keep the covariance word to the existing no-link disclaimer sentence if the architect's B1 limit still applies (the builder may instead write 'the quadratic form w'Sigma w, which is the portfolio variance when Sigma is the return covariance matrix', using the same sentence).")
R("M7b-r3-L01-convexity-definition", "Lemma 1.4 relies on 'convex in the sense defined in L01'", "course/modules/M/M7/L05.html:83-89; course/modules/M/M7/L01.html:82", P,
  CARRY + "L01.html:82 defines a convex function on S by f(lambda x + (1-lambda) y) <= lambda f(x) + (1-lambda) f(y) for x, y in S and lambda in [0,1]; L05 Lemma 1.4's convexity clause proves exactly this inequality for f on R^n with Q psd.")
R("M7b-r3-L05-remark24-decomposition", "Remark 2.4 positive definiteness and null direction", "course/modules/M/M7/L05.html:124-125 (Remark 2.4)", P,
  "Completed square (2x1 + x2/2)^2 + (11/4)(x2 + 4x3/11)^2 + (18/11) x3^2 expanded and equal to 4x1^2 + 3x2^2 + 2x3^2 + 2x1x2 + 2x2x3 (exact check). A v = 0 for v = (-2,1,1): rows (1,1,1)·v = 0 and (0,1,-1)·v = 0. Lab Part A null-line identity holds exactly.")
R("M7b-r3-L06-prop34-no-sign", "Proposition 3.4 with no sign assumption on tau and w0", "course/modules/M/M7/L06.html:134-141", P,
  "Proof works for any real tau: if sum|d_i| <= tau take t_i = |d_i|; conversely sum|d_i| <= sum t_i <= tau. If tau < 0 both the turnover inequality (LHS >= 0) and the existence of t (sum t_i >= 0) fail, so the equivalence holds. Definition 3.2 (tau >= 0) is narrower and consistent.")
R("M7b-r3-L06-def31-scope", "Definition 3.1 scope sentence", "course/modules/M/M7/L06.html:120", P,
  "'This lesson uses only the budget and nonnegativity constraints; the general box and the sector constraint are not used.' grep for box and sector and u_i on L06 finds them only in Definition 3.1; the lab twin has no box or sector term; Part B and D use only w >= 0 and the turnover linearization (Definition 3.2 / Proposition 3.4, which is not one of the three kinds listed).")
R("M7b-r3-lab-hypothesis-vs-output", "lab hypotheses and interpretations, L04 and L05 (what the lab prints/checks vs code and output)", "course/modules/M/M7/L04.html:126, 249; L05.html:183, 390; tests/labs/M7/lab-M7-L04-1.py docstring; lab-M7-L05-1.py docstring", P,
  "L04 hypothesis predicts 1331, 21, 27951, one grid point attaining -1/2, grid gap 0, -199/300, KKT True: all printed. L04 docstring says the lab checks weak duality on dual and feasible primal grids and reports the grid gap: matches. L05 hypothesis predicts nonzero determinant, zero residuals, exact null-line identity at 17 t values, exactly one passing candidate, 33x33 grid: all printed (17 values of t: range(-8,9) over Fraction(k,4)). L05 docstring: Part B keeps candidates with x >= 0 and mu_i >= 0 on S: matches code.")
R("M7b-r3-notation", "notation registry conformity (notation/notation.json, BUILDER_RULES 3.1)", "course/modules/M/M7/L04.html, L05.html, L06.html (KaTeX source)", P,
  "No registered symbol is given a different meaning. L04 uses the registered macro \\R; L05 uses \\mathbb{R} five times and L06 twice (raw KaTeX for the same set; \\R maps to \\mathbb{R} in notation.json). M2 uses both forms, so the repository does not enforce the macro form. Not a failure of the registry rule as applied to this slice; noted for the builder. No \\Var or \\Cov use.")

fragment = {
    "unit": "M7", "slice": "M7-b", "round": 3,
    "verifier": "round-3 independent verifier for slice M7-b (L04 to L06 and their lab twins); did not build M7 and shares no context with its builders",
    "pin": "aa3c26c", "base": "1817191",
    "checkout": "/tmp/verifyB3-M7-b (detached worktree at aa3c26c; .venv symlink)",
    "scratch": "/tmp/M7-v/b", "verified_at": "2026-10-28T18:00:00+00:00",
    "verdict": "FAIL", "registry_flags": [], "freshness_flags": [],
    "rows": rows, "mutants": [],
    "notes": [
        "Delta since round-2 pin 1817191 (git diff --stat): L04.html, L05.html, L06.html, cards.json, lab-M7-L04-1.py, lab-M7-L06-1.py, plus L01-L03, L07, L08, grader and plan changes outside the slice. lab-M7-L05-1.py and the L05 page text changed (L05.html changed; lab-M7-L05-1.py is byte-identical). Because each changed subject was re-read and re-checked, no row is carried from round 2 by byte identity; every row states what was re-run this round.",
        "Round-2 FAIL rows fixed in this round: M7b-L04-prop32 (now 'Open item 3.2'), M7b-L04-term-before-definition (no Slater term before Definition 3.1), M7b-footer-L05-L06 (footers now match 'cites no source'). Round-2 duplicate pairs c056/c070 and c106/c117 are no longer duplicates. Round-2 duplicate pairs c058/c069, c059/c071, c082/c092 remain (M7b-cards-duplicates).",
        "Hunt results: every numeric claim recomputed from unrounded exact values (num_L04_indep.py, num_L05_indep.py, num_L06_indep.py); the only rounding-sensitive statements (L06 E2 difference 0.5722548 -> 0.572255; L06 E3 turnover 0.5588607 vs 0.558860 from printed weights; quiz tolerances) are correct on the unrounded basis stated.",
        "Mutation testing is not applicable: lab slice (architect ruling). mutants list is empty by design. No alternative implementations: project slices only.",
        "Hours judged on arithmetic only (architect ruling).",
        "Not checked: no external source was read or cited in the slice (no registry key, no locator), so no access statement is made. The Lesson 3 items cited by L04-L06 (Definition 1.1, 1.2, Lemma 1.4, Theorem 2.1, Example 3.1, Example 4.1, Open item 3.2, K1-K4) were read at their L03 locations only as far as needed for the cross-references; the rest of L03 is M7-a's slice. Pyodide itself was not run; page_smoke (the project's Pyodide timing tool) was used. Live reference re-verification covers only the two M7 registry entries the tool selects.",
    ],
    "summary": None,
}
rows_pass = sum(1 for r in rows if r["status"] == P)
rows_fail = sum(1 for r in rows if r["status"] == FL)
fragment["summary"] = {"rows": len(rows), "pass": rows_pass, "fail": rows_fail, "unverifiable": 0,
                      "fail_ids": [r["id"] for r in rows if r["status"] == FL]}
out = ROOT / "ledgers/M7/M7-b.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, len(rows), rows_pass, rows_fail)
