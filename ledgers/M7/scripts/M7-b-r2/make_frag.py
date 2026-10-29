import json
S = "ledgers/M7/scripts/M7-b-r2/"
P = "Carried"  # not used; all rows re-run or re-derived this round
R = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)

row("M7b-cmd-check-pages", "tools/check_pages.py for M7 and each page",
    "course/modules/M/M7/L04.html, L05.html, L06.html; tools/check_pages.py", "PASS",
    "Re-run on pin 1817191: `.venv/bin/python tools/check_pages.py --unit M7 --page L04|L05|L06` -> 'check_pages M7 L04: PASS', 'L05: PASS', 'L06: PASS'; `--unit M7` -> 'check_pages M7: PASS'.")
row("M7b-cmd-check-dag", "tools/check_dag.py for M7", "course/modules/M/M7/*.html; tools/check_dag.py", "PASS",
    "Re-run: `.venv/bin/python tools/check_dag.py --unit M7` -> 'check_dag M7: PASS'.")
row("M7b-dag-prose-terms", "Concepts named in prose without link or definition (plan section 2, plain prose allowed for undeclared terms)",
    "course/modules/M/M7/L04.html:275, 503; L05.html:89; L06.html:87", "PASS",
    "Re-read all three pages. 'convexity' and 'convex' appear as plain prose (L04.html:275 'no convexity', L04.html:503 'needs convexity', L05.html:89 'convexity clause'); the plan's section 2 table says undeclared terms are plain prose with no dfn and no link. 'Hessian' is linked in the meta rows (L05.html:38, L06.html:38) before its use (L05.html:52, L06.html:52). The Slater-point use before its definition is a separate row (M7b-L04-term-before-definition).")
row("M7b-cmd-run-labs", "tools/run_labs.py --unit M7 for L04, L05, L06",
    "tests/labs/M7/lab-M7-L04-1.py, lab-M7-L05-1.py, lab-M7-L06-1.py", "PASS",
    "Re-run: `.venv/bin/python tools/run_labs.py --unit M7 --page L04` (and L05, L06) -> 'run_labs M7: PASS (1/1)' each.")
row("M7b-lab-L04-twin-run", "Twin L04 run under python -I -W error; output equals the page expected block",
    "tests/labs/M7/lab-M7-L04-1.py", "PASS",
    "`.venv/bin/python -I -W error tests/labs/M7/lab-M7-L04-1.py` exit 0, stderr 0 bytes. Stdout saved to /tmp/M7-v/b/out/L04.txt; ledgers/M7/scripts/M7-b-r2/cmp.py (run with /usr/bin/python3 -I) prints 'L04 match 1'. Output: 1331 dual points, 21 primal, 27951 of 27951 pairs, largest dual -1/2 at (0, 3/10), -1/2, attaining count 1, grid gap 0, g(0,0) = -199/300, KKT True.")
row("M7b-lab-L05-twin-run", "Twin L05 run under python -I -W error; output equals the page expected block",
    "tests/labs/M7/lab-M7-L05-1.py", "PASS",
    "Re-run with -I -W error: exit 0, stderr 0 bytes; cmp.py prints 'L05 match 1'. kkt_determinant 19; x 13/19 3/19 3/19; lambda -36/19 11/19; passing_candidates 1; grid_points 1089; grid_points_below_candidate 0.")
row("M7b-lab-L06-twin-run", "Twin L06 run under python -I -W error; output equals the page expected block",
    "tests/labs/M7/lab-M7-L06-1.py", "PASS",
    "Re-run with -I -W error: exit 0, stderr 0 bytes; cmp.py prints 'L06 match 1'. Part B candidates_passing 1 and zero set {A4} at all five gammas; Part D turnover 0.558861; 20 of 20 perturbations.")
row("M7b-lab-lint-types", "ruff check, ruff format --check and mypy --strict on the three twins",
    "tests/labs/M7/lab-M7-L04-1.py, lab-M7-L05-1.py, lab-M7-L06-1.py", "PASS",
    "`.venv/bin/ruff check tests/labs/M7` -> 'All checks passed!'; `.venv/bin/ruff format --check tests/labs/M7` -> '11 files already formatted'; `.venv/bin/mypy --no-incremental --strict` on the three twins -> 'Success: no issues found in 3 source files'.")
row("M7b-lab-pytest", "tests/test_labs.py", "tests/test_labs.py", "PASS",
    "`.venv/bin/pytest -q tests/test_labs.py` -> three progress lines of dots reaching [100%], no failure or error lines.")
row("M7b-smoke", "tools/page_smoke.py for L04, L05, L06 (Pyodide)", "course/modules/M/M7/L04.html, L05.html, L06.html", "PASS",
    "`.venv/bin/python tools/page_smoke.py --unit M7 --pages L04 L05 L06` -> 'page_smoke M7: PASS', exit 0; runtime boot 1.1 s; each lab 0.0 s (output in /tmp/M7-v/b/smoke.txt).")
row("M7b-refs-live", "tools/verify_refs.py live and offline; slice citations",
    "references/references.json; course/modules/M/M7/L04.html, L05.html, L06.html (data-references lists, lines 508-511, 625-628, 644-647)", "PASS",
    "`.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems'; `--unit M7` -> 'live re-verification of M7: 2 of 560 entries, 0 problems'. The three slice pages now cite no registry key (each references section says so; the data-references lists are empty), so no citation row remains for L04-L06.")
row("M7b-citation-boyd-attribution", "Round-1 attribution of Proposition 3.2 to boyd2004convex with no locator",
    "course/modules/M/M7/L04.html (grep boyd: 0 hits); course/modules/M/M7/cards.json (M7-c066 removed)", "PASS",
    "`grep -c boyd course/modules/M/M7/L04.html` -> 0 (the round-1 Proposition 3.2 passage is gone; L04 line 259 says strong duality is not stated as a numbered result). The card M7-c066 is absent from cards.json. The attribution no longer appears anywhere in the slice, so no attribution is asserted.")
row("M7b-2.2-numbers-L04", "Numbers in prose and quiz, L04 (class a/b/c)",
    "course/modules/M/M7/L04.html:51, 121, 125-135, 249, 259-268, 285-295, 324, 329-402, 417, 457, 471, 491-494; ledgers/M7/scripts/M7-b-r2/num_L04_L06.py", "PASS",
    "Independent Fraction recomputation (num_L04_L06.py): R3 values g(0,-3/5) = g(0,-7/10) = -157/300; continuous maximiser nu = -0.65 with value -209/400 (numpy scan of 10^6 points); grid gap 7/300; g(0,0) = -199/300; mu'Sigma^{-1}mu = 199/150; grid counts 11^3 = 1331, 21, 27951; Example 2.2 r = (2, 1), r'Sigma^{-1}r = 2, g = -1/2 = f(1,0); -199/300 + 150/300 = -49/300. All match the page.")
row("M7b-2.2-numbers-L05", "Numbers in prose, L05 (class a/b/c)",
    "course/modules/M/M7/L05.html:52, 125, 175-177, 390, 482, 489, 496, 507-521, 574, 588, 611; ledgers/M7/scripts/M7-b-r2/num_L05.py", "PASS",
    "num_L05.py (numpy and Fraction): det K = 19.0; x = (13, 3, 3)/19; lambda = (-36, 11)/19; v'Qv = 19 with Qv = (-7, 2, 3); objective 0.7631578947 = 551/722; grid minimum -2.25 over 33x33 points; Remark 2.4 decomposition identity residual below 1e-14. E1 derivation: x'Qx = 817/361 and c'x = -7/19 both recomputed by hand. R3 mu + t1 with t = 0.44 checked by hand.")
row("M7b-2.2-numbers-L06", "Numbers in prose, L06 (class a/b/c), including displayed quotients",
    "course/modules/M/M7/L06.html:150, 359-410 (interpretation 405), 428, 432, 445-462, 477-514, 524-538, 580-625; ledgers/M7/scripts/M7-b-r2/num_L06.py", "PASS",
    "num_L06.py recomputes the lab from its seed with an independent LCG run: mu = 7/100, 1/20, 3/25, 1/50; diagonal 49/40, 27/20, 103/80, 103/80; equality returns, variances, objectives and weights at gamma 1..16 match the printed six-place values; Part B zero set {A4} with weights 0.388425, 0.203679, 0.407895, 0 at gamma 1; E2 unrounded difference 1.3922569654 - 0.8200021339 = 0.5722548315 (rounds to 0.572255); E3 unrounded turnover 0.5588607333 (printed 0.558861), printed-digit sum 0.558860; E1 weights sum to 1.000000. M1 lambda = -37/40, w = (0.5125, 0.4875); M2 f = 17/40; M3 interval [0.2, 0.4]; R2 t = 0.44, minimiser (0.54, 0.46); R3 interval [0.4, 0.6].")
row("M7b-2.2-misc-numbers", "Numbers in prose outside the three main sections",
    "course/modules/M/M7/L06.html:405, 428, 504, 511; course/modules/M/M7/L05.html:390, 482; course/modules/M/M7/L04.html:287, 291", "PASS",
    "Printed values checked against num_L06.py and num_L05.py output: Part A return falls 0.113798 -> 0.106241 (unrounded 0.1137977, 0.1062414); variance falls 0.123809 -> 0.115780; A4 weight negative at all five gammas; constrained objective at least unconstrained at all five (5 True lines); dual value -199/300 is 49/300 below -1/2.")
row("M7b-2.3-grades-L04", "Grades of key-results table and claims, L04",
    "course/modules/M/M7/L04.html:405-421 (key results table), 49-51", "PASS",
    "Each T row is a proof on the page and was re-proved: Prop 1.2 (concavity), 1.3 (weak duality), 1.4 (grid bound), 2.1 (KKT zero gap), Example 2.2, Example 3.4. The lab row is graded C with basis Lab 1. No T row depends on a lab output or on Slater's condition.")
row("M7b-2.3-grades-L05", "Grades of key-results table and claims, L05",
    "course/modules/M/M7/L05.html:527-542 (key results table)", "PASS",
    "All six rows are T with proofs on the page (Lemma 1.3, Prop 2.1, Theorem 2.3, Theorem 3.1, Prop 3.4, Example 3.6); Lab 1 rows are described as checks of one instance, not as the basis of a T claim.")
row("M7b-2.3-grades-L06", "Grades of key-results table and claims, L06",
    "course/modules/M/M7/L06.html:542-556 (key results table), row 5 at line 552; course/modules/M/M7/cards.json M7-c118", "PASS",
    "Round-1 FAIL is fixed: the row 'The closed form of Theorem 1.3 and the KKT solve agree exactly for the simulated inputs' is now graded C with basis 'Lab 1, Part A (SIMULATED)'; the identity itself is Theorem 1.3 (T). Card M7-c118 is also C. Rows 1 to 4 are T with proofs on the page and were re-proved.")
row("M7b-cards-L04-c056-c065", "Cards M7-c056 to c065 against L04 text",
    "course/modules/M/M7/cards.json M7-c056..c065; course/modules/M/M7/L04.html lines 55-268", "PASS",
    "Each card read against its lesson paragraph and proof: Def 1.1 (c056), Prop 1.2 (c057), Prop 1.3 (c058), Prop 1.4 (c059), Remark 1.5 and Problem R3 (c060, value 7/300), Prop 2.1 (c061), Example 2.2 (c062), Lab 1 numbers (c063, including 1331, 21, 27951), M3 (c064), Def 3.1 (c065). No card number is missing from its lesson.")
row("M7b-cards-L04-c066-c072", "Cards M7-c066 to c072 against L04 text (round-1 FAIL on c066 and c071)",
    "course/modules/M/M7/cards.json M7-c067..c071 (c066 and c072 now absent); course/modules/M/M7/L04.html:259-268, 281-295", "PASS",
    "Round-1 FAILs fixed: the card for Proposition 3.2 (c066) is removed, and the card on the zero grid gap (c071) now reads 'The implication uses only Propositions 1.3 and 1.4, and exact arithmetic makes the printed zero exact'. c067 (Remark 3.3), c068 (Example 3.4), c069 and c070 (misconceptions) match the lesson text.")
row("M7b-cards-L05-c073-c084", "Cards M7-c073 to c084 against L05 text",
    "course/modules/M/M7/cards.json M7-c073..c084; course/modules/M/M7/L05.html lines 58-172", "PASS",
    "Each card read against its lesson text. c081 (Theorem 3.1) and c084 (midpoint identity f((x+y)/2) = (f(x)+f(y))/2 - (1/8)(x-y)'Q(x-y)) match L05.html:141-166, verified by expansion. c080 decomposition verified numerically (residual below 1e-14).")
row("M7b-cards-L05-c085-c096", "Cards M7-c085 to c096 against L05 text (round-1 FAIL on c096)",
    "course/modules/M/M7/cards.json M7-c085..c093 (c094-c096 now absent)", "PASS",
    "Round-1 FAIL fixed: the card that said the minimiser is unique for a positive definite Q over a convex set is now the midpoint-convex card (c084), and the card that duplicated it (c096) is removed. Cards c085 to c093 match L05 Remark 3.5, Example 3.6, Lab 1 Part B (c086-c089), the misconceptions (c091-c093) and Remark 3.2 (c082).")
row("M7b-cards-L06-c097-c108", "Cards M7-c097 to c108 against L06 text",
    "course/modules/M/M7/cards.json M7-c097..c108; course/modules/M/M7/L06.html lines 58-146", "PASS",
    "Checked against L06.html: Definitions 1.1, 1.2, 3.1, 3.2; Theorem 1.3 (c100); Remark 1.4 (c101); Prop 2.1 (c102); Prop 2.3 (c103); Prop 3.4 (c106); Remark 3.5 (c107). Card c099 says estimating a covariance matrix is outside M7 (Section 1, L06.html:56). All match.")
row("M7b-cards-L06-c109-c120", "Cards M7-c109 to c120 against L06 text (round-1 FAIL on c118 and c116)",
    "course/modules/M/M7/cards.json M7-c108..c117 (c119, c120 now absent); course/modules/M/M7/L06.html:404-430, 552", "PASS",
    "Round-1 FAILs fixed: c118 is C (basis Lab 1, Part A) matching the page table; c116 lists the four weights of L06.html:428. c109 to c115 and c117 match the printed values (c108 to c115 checked against output in /tmp/M7-v/b/out/L06.txt).")
row("M7b-cards-duplicates", "Full duplicate scan of cards M7-c056 to c117 (same fact asked twice)",
    "course/modules/M/M7/cards.json: c056/c070, c058/c069, c059/c071, c082/c092, c106/c117", "FAIL",
    "The round-1 duplicate pairs (c061/c072, c075/c094, c081/c095, c084/c096, c100/c119, c106/c120) are resolved. Five pairs still test one fact with the same answer: c058 ('for every dual feasible pair g <= p*, hence d* <= p*') and c069 ('weak duality gives only d* <= p*'); c059 ('if the grid left side is zero then p* = d*') and c071 ('a zero grid gap forces the true gap to be zero'); c056 ('the Lagrangian dual problem maximizes g') and c070 ('the dual problem maximizes g'); c082 (Remark 3.2, optimal with negative multiplier?) and c092 ('stationarity does not imply optimality'); c106 ('turnover holds iff t exists, Prop 3.4') and c117 ('turnover cannot be a QP; linearization is equivalent, Prop 3.4').",
    "Merge each pair into one card, or rewrite one card to ask a different fact (for example a numeric check, a hypothesis that fails, or the next step of the proof). Re-check the card count after the change.")
row("M7b-2.9-structure", "Template sections and counts, L04 to L06",
    "course/modules/M/M7/L04.html, L05.html, L06.html", "PASS",
    "Section order in all three pages: why-it-matters, core sections, lab(s), where the canon breaks, misconceptions (3 each), problem set (3 tiers, 3 problems each: L04 M1-M3, P1-P3, E1-E3, R1-R3; L05 and L06 likewise), key results, retrieval quiz (L04 10 items, L05 10 items, L06 11 items), references.")
row("M7b-2.9-banned", "Banned phrases (BUILDER_RULES 1.2 and 1.3) and ellipses",
    "course/modules/M/M7/L04.html:183 (code docstring '{0, 1/10, ..., 1}'); course/modules/M/M7/L06.html:178 (code docstring '(1/4, ..., 1/4)')", "PASS",
    "check_pages banned-string scan PASS for all three pages. grep for TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'roughly', 'about <digit>', 'historically', 'it is important': no prose hit. The only '...' occurrences are list notation inside code docstrings (listed grid values and a repeated vector entry), not omitted content.")
row("M7b-2.9-process-words", "Process words in learner text (build, builder, verifier, round, REQUEST, unit report)",
    "course/modules/M/M7/L04.html, L05.html, L06.html", "PASS",
    "grep -i for build, builder, verifier, round, REQUEST, 'unit report' in the three pages: no process word in learner text.")
row("M7b-hours", "Hub split against declared lesson hours (arithmetic only, architect ruling)",
    "course/modules/M/M7/index.html (data-hours-lessons); course/modules/M/M7/L01..L08.html data-hours", "PASS",
    "index.html data-hours-lessons=\"77\"; lesson data-hours L01 9, L02 9, L03 10, L04 10, L05 10, L06 10, L07 9, L08 10; sum 77. L04 to L06 each 10 h, the hub's L04 to L06 card labels read '10 h'. Pace not judged.")
row("M7b-L04-prop32", "Proposition 3.2 (round 1: a theorem with no proof, attributed to boyd2004convex) and the Lesson 3 cross-reference",
    "course/modules/M/M7/L04.html:256 ('It is the hypothesis of Lesson 3, Proposition 3.2.'); course/modules/M/M7/L03.html:134 ('Open item 3.2')", "FAIL",
    "The round-1 unproved Proposition 3.2 and its boyd2004convex attribution are gone (see M7b-citation-boyd-attribution). But L04.html:256 still cites a 'Proposition 3.2' in Lesson 3. Lesson 3 has no Proposition 3.2: the Slater necessity statement is 'Open item 3.2' (L03.html:134), which the Lesson 3 page says is not proved and carries no grade (L03.html:462). The cross-reference names a result that does not exist under that label.",
    "Change L04.html:256 to 'It is the hypothesis of the necessity statement Open item 3.2 in Lesson 3, which this lesson does not use.'")
row("M7b-L04-lab-numbering", "Lab numbering and cross-references to the lab (round-1 FAIL: 'Lab 2' in L04)",
    "course/modules/M/M7/L04.html:125 and all later mentions; course/modules/M/M7/cards.json M7-c060, c063, c071", "PASS",
    "grep -c 'Lab 2' on L04.html, L05.html, L06.html -> 0. grep -o 'Lab [0-9]' L04.html -> only 'Lab 1' (17 occurrences, first at line 7). The cards say Lab 1. The lab's own title is 'Lab 1 · ...' (line 125).")
row("M7b-L04-quiz-hypotheses", "Quiz item 10 and its hypothesis list (round-1 FAIL: differentiability omitted)",
    "course/modules/M/M7/L04.html:497-503 (quiz item 10, option 2 and explain)", "PASS",
    "The correct option now reads 'A KKT point, with differentiable convex f and g_i and affine h_j', matching Proposition 2.1 (L04.html:107). The explanation names Lemma 1.4 of Lesson 3 (convexity) and says Slater's condition is not needed. Distractors (a Slater point alone; finiteness of F) are not sufficient, so the item is correct.")
row("M7b-L04-causal", "Causal claim in Misconception 3 (round-1 FAIL: zero grid gap 'holds because exact fractions')",
    "course/modules/M/M7/L04.html:295; course/modules/M/M7/cards.json M7-c071", "PASS",
    "The text now says the implication 'uses only Propositions 1.3 and 1.4' and that exact arithmetic 'makes the printed zero exact, so no tolerance is needed'. That is a statement about the printed number, not about why the implication holds. The implication itself follows from Propositions 1.3 and 1.4 with no arithmetic assumption.")
row("M7b-L04-term-before-definition", "Term used before its definition (round-1 FAIL at line 51 is fixed; a new use appears at line 126)",
    "course/modules/M/M7/L04.html:126 (Lab 1 hypothesis: 'which is a Slater point (Definition 3.1, Section 3)'); definition at L04.html:255-256; line 51 now has no Slater term", "FAIL",
    "The opening paragraph (L04.html:51) no longer names Slater's condition. But the Lab 1 hypothesis (L04.html:126) uses 'a Slater point' before Definition 3.1 at L04.html:255. BUILDER_RULES 10: 'No concept used before it is introduced.' A pointer to a later definition does not make the term introduced.",
    "Remove the Slater point from the Lab 1 hypothesis (the lab's Slater check is at (1/2, 1/2); state the point's inequalities directly), or move Definition 3.1 before the lab.")
row("M7b-L05-lemma14", "Lemma 1.4 'f is convex' claim and its proof (round-1 FAIL: proof gave only the tangent inequality)",
    "course/modules/M/M7/L05.html:82-89", "PASS",
    "The proof now carries the chord computation: theta f(x) + (1-theta) f(y) - f(z) = (1/2) theta (1-theta) (x-y)'Q(x-y) >= 0 for PSD Q, with the linear terms cancelling. Checked by expansion; the identity for theta||x||^2 + (1-theta)||y||^2 - ||theta x + (1-theta) y||^2 = theta(1-theta)||x-y||^2 is the standard one.")
row("M7b-L05-prop34-step", "Proof step of Proposition 3.4 (round-1 FAIL: expansion not shown)",
    "course/modules/M/M7/L05.html:164-166", "PASS",
    "The proof now shows f(x)+f(y) = 2f(z) + u'Qu with u = (x-y)/2, u'Qu = (1/4)(x-y)'Q(x-y), hence f(z) = (f(x)+f(y))/2 - (1/8)(x-y)'Q(x-y). Each line re-derived by hand.")
row("M7b-L05-why-xref", "Cross-reference 'Proposition 3.6' (round-1 FAIL: no such proposition)",
    "course/modules/M/M7/L05.html:52", "PASS",
    "The why-it-matters sentence now cites 'Proposition 3.4' (L05.html:160, the midpoint result). grep -c 'Proposition 3.6' L05.html -> 0. Example 3.6 exists at L05.html:175.")
row("M7b-L05-misc3", "Misconception 3 about stationarity at zero (round-1 FAIL: 'holds only without constraints')",
    "course/modules/M/M7/L05.html:415-417", "PASS",
    "The text now says the gradient is zero exactly when lambda* = 0, because A has full row rank, and is otherwise a combination of constraint rows. Verified: A' has full column rank, so A'lambda = 0 iff lambda = 0.")
row("M7b-L05-canon-heading", "Canon heading 'Indefinite Hessians have no minimum' (round-1 FAIL: false in general)",
    "course/modules/M/M7/L05.html:396", "PASS",
    "Heading now reads 'An indefinite Hessian can leave a QP with no minimiser.', with the body that qualifies it (a QP can have no minimiser, Misconception 1). The Misconception 1 example (Q = diag(1,-1)) is correct.")
row("M7b-L05-lab-variables", "Interpretation count of variables (round-1 FAIL: 'four and two')",
    "course/modules/M/M7/L05.html:390", "PASS",
    "Now: 'The lab uses three variables in Part A and two in Part B, examines four candidate sets'. Output: 'part_a_dimensions variables 3 constraints 2' and four candidate lines in Part B.")
row("M7b-L05-why-scope", "Scope claim in the why-it-matters paragraph (round-1 FAIL: 'Portfolio construction... and many pricing problems')",
    "course/modules/M/M7/L05.html:52", "PASS",
    "The sentence is now 'A quadratic program minimises a quadratic objective under linear constraints.' That is the definition in Definition 1.1, with no application claim.")
row("M7b-L06-why-scope", "Categorical claim 'Choosing portfolio weights is a quadratic program' (round-1 FAIL)",
    "course/modules/M/M7/L06.html:52", "PASS",
    "Now: 'The mean-variance problem of this lesson is a quadratic program', with the problem's data in the same sentence. Scope is the problem of this lesson, not all portfolio choice.")
row("M7b-L06-partB-count", "Part B enumeration count (round-1 FAIL: '16 sets' against 15 enumerated)",
    "course/modules/M/M7/L06.html:150, 168-170, 291-294 of the page code; tests/labs/M7/lab-M7-L06-1.py (docstring Part B, `if not free: continue`)", "PASS",
    "Now '15 sets that leave at least one asset free', with the all-fixed set skipped. The twin code loops over 2^4 masks and skips the mask with no free asset, so 15 candidates are enumerated. Hypothesis, docstring and code agree.")
row("M7b-L06-partD-true", "Misconception 3 claim about Part D printed checks (round-1 FAIL: 'prints True for each check')",
    "course/modules/M/M7/L06.html:431-432", "PASS",
    "Now: 'It prints True for the two linearization checks and 20 of 20 for the perturbation check.' Output lines 401-403: linear_form_feasible True, linear_form_sum_equals_turnover True, feasible_perturbations_at_least_turnover 20 of 20.")
row("M7b-L06-misc2", "Canon bullet and Misconception 2 (round-1 FAIL: only the first three weights listed)",
    "course/modules/M/M7/L06.html:414, 427-428", "PASS",
    "Misconception 2 now lists all four changed weights (0.434783 to 0.388425; 0.526836 to 0.203679; 0.562535 to 0.407895; -0.524154 to 0), and the canon bullet says 'changes all four weights'. Verified against output lines 376-387.")
row("M7b-L06-covariance-docstring", "Covariance wording in lab docstring and page (architect decision B1: covariance only in a no-link disclaimer)",
    "course/modules/M/M7/L06.html:56, 156 (lab docstring, now 'a given symmetric positive definite matrix Sigma'); tests/labs/M7/lab-M7-L06-1.py:6-8", "PASS",
    "grep -n covariance L06.html -> one hit (line 56, a disclaimer: 'The word covariance appears here only to say that estimating a covariance matrix is outside M7.'). grep -n covariance tests/labs/M7/lab-M7-L06-1.py -> no hit. The disclaimer is the permitted no-link use under plans/M7-build-plan.md B1 and the architect decision.")
row("M7b-L06-R1-unproved", "Solution to R1 (round-1 FAIL: uniqueness of the equal-weight portfolio asserted without proof)",
    "course/modules/M/M7/L06.html:518-524 (problem R1 and its solution)", "PASS",
    "R1 is now the large-risk-aversion limit with Sigma = I. Its solution takes the limit of the P3 formula, and it says the mu = 0 case gives 1/n 1 as 'the unique minimiser of (1/2) w'w under the budget'. Uniqueness is Theorem 1.3 (unique minimiser for any gamma > 0, applied with mu = 0) and the formula is P3. Checked: with mu = 0, w = 0 - (0 - 1)/n 1 = 1/n 1.")
row("M7b-L06-term-before-definition", "Term 'turnover constraint' used before Definition 3.2 (round-1 FAIL at line 52)",
    "course/modules/M/M7/L06.html:52, 116, 124-125", "PASS",
    "The why-it-matters paragraph (L06.html:52) now says 'One of them limits total trading, a sum of absolute values', without the term. grep -o 'turnover' L06.html: hits at lines 7 (meta description, not learner prose), 124 (the title of Definition 3.2) and 125 (its meaning). The section 3 heading (line 116) is now 'Linear portfolio constraints', so no prose use precedes the definition.")
row("M7b-L06-lab-claims-ok", "Interpretation claims and hypothesis against the lab output (every sentence about what the lab prints)",
    "course/modules/M/M7/L06.html:150, 168-170 (hypothesis), 404-405 (interpretation)", "PASS",
    "Each sentence checked against the output: budget True at each gamma; A4 negative at five gammas; return falls 0.113798 -> 0.106241; variance falls 0.123809 -> 0.115780; zero set {A4}; constrained objective >= unconstrained at each gamma; Part D turnover 0.558861. Hypothesis: Part A gammas 1, 2, 4, 8, 16 (GAMMAS); Part B 15 sets; Part C monotonicity; Part D at gamma 4.")
row("M7b-2.4-L04-proofs", "Proofs of L04 (re-derived)", "course/modules/M/M7/L04.html:67-115, 254-273, 329-412", "PASS",
    "Re-derived: Prop 1.2 (infimum of a sum >= sum of infima); Prop 1.3 (each lambda_i g_i(x) <= 0, h_j(x) = 0); Prop 1.4 (inequalities between min over F~, max over D~, p*, d*); Prop 2.1 (KKT point: phi convex, gradient zero, Lemma 1.4 of Lesson 3, weak duality); Example 2.2 (Sigma pd via a^2+b^2+(a+b)^2; Sigma^{-1}; r = (2,1); g = -1/2); Remark 3.3; Example 3.4 (g(lambda) = -1/(4 lambda), sup 0 not attained); R2.")
row("M7b-2.4-L05-proofs", "Proofs of L05 (re-derived)", "course/modules/M/M7/L05.html:70-180", "PASS",
    "Re-derived: Lemma 1.3 expansion; Lemma 1.4 (tangent inequality and chord identity); Prop 2.1 (K nonsingular via x'Qx = 0); Remark 2.2 determinant; Theorem 2.3 (d'Qd > 0); Remark 2.4 decomposition and null direction; Theorem 3.1 (the sum of nonnegative terms); Remark 3.2 (f(0)=0, f(1)=-1/2); Prop 3.4 (corrected midpoint identity).")
row("M7b-2.4-L06-proofs", "Proofs of L06 (re-derived)", "course/modules/M/M7/L06.html:68-146", "PASS",
    "Re-derived: Theorem 1.3 (KKT solve, lambda formula, 1'b = b'Sigma b > 0); Remark 1.4; Prop 2.1 (both minimality inequalities, R2 - R1 >= (gamma2/2)(V2 - V1) >= 0); Prop 2.3 (inclusion of feasible sets, with the infimum convention; see notes); Prop 3.4 (two directions, t_i = |d_i|).")
row("M7b-2.4-quiz", "Quiz answers and explanations (L04, L05, L06)",
    "course/modules/M/M7/L04.html:423-506; course/modules/M/M7/L05.html:544-623; course/modules/M/M7/L06.html:558-641", "PASS",
    "Numeric keys re-derived: L04 -0.5, 2, -0.6633 (tolerance 5e-5 holds: -199/300 = -0.66333); L05 19, 0.7632 (551/722 = 0.763158, within 5e-5), -2.25, 19; L06 0.113798, 0.184631, 0.007996, 0.2, 0.5125 (M1). Multiple-choice keys checked against the lesson statements.")
row("M7b-2.5-L04-misc", "Interpretation and lab-output sentences, L04", "course/modules/M/M7/L04.html:249, 285-295, 372-374", "PASS",
    "'the grid happens to contain the dual optimum (lambda*, nu*)': (0, 3/10) and -1/2 are grid points (lambda_2 = 3/10 and nu = -1/2 on the 1/10 grid). 'The grid gap of 0 is exact' holds with exact Fractions in the printed output. The sentence about the value -199/300 as a lower bound is correct by Proposition 1.3.")
row("M7b-footer-L05-L06", "Page footer claim 'Every claim carries an evidence grade and a registry citation' against the references section of the same page",
    "course/modules/M/M7/L05.html:638 and :627 ('This lesson cites no outside source'); course/modules/M/M7/L06.html:657 and :646 ('This lesson cites no outside source')", "FAIL",
    "The footer states every claim carries a registry citation. Both pages say in their references section that they cite no outside source, and the data-references lists are empty. The footer contradicts the page. (L04's footer 'Each graded result carries a proof or a lab result labelled C' is accurate and is not in this row.)",
    "Change the footer on L05 and L06 to match the references section, for example 'Every claim carries an evidence grade and a proof or a lab result.'")

frag = {
    "unit": "M7",
    "slice": "M7-b",
    "round": 2,
    "verifier": "round-2 independent verifier for slice M7-b (L04-L06 and their lab twins); did not build M7 and shares no context with its builders",
    "pin": "1817191",
    "base": "c11ae01",
    "checkout": "/tmp/verifyB2-M7-b (detached worktree at 1817191; .venv symlink)",
    "scratch": "/tmp/M7-v/b",
    "verified_at": "2026-10-28T15:30:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since round-1 pin c11ae01: L04.html, L05.html, L06.html, cards.json, lab-M7-L04-1.py, lab-M7-L06-1.py, plans/M7-build-plan.md (one line). lab-M7-L05-1.py byte-identical; its rows were re-run anyway, not carried.",
        "Every round-1 non-PASS row was re-verified from scratch against the pin. Rows whose subject did not change were re-run (commands) or re-derived (numbers, cards).",
        "Mutation testing does not apply to lab slices (architect ruling); mutants list is empty by design. No alternative implementations: project slices only.",
        "Hours judged on arithmetic only (architect ruling).",
        "Proposition 2.3 (L06.html:108) says 'the minimum of f over F+ is at least the minimum over F0'. The proof uses only inclusion of feasible sets. It is true under the infimum convention, and F+ is non-empty (equal weights 1/4 each, in F+). The page does not state the existence of the minima; not a FAIL on the infimum reading, noted for the builder.",
        "The three slice pages cite no registry key, so no registry row is needed; verify_refs --unit M7 was run live (2 of 560 entries, 0 problems), which covers the unit's entries.",
        "Not checked: the Lesson 3 Definition 1.1 wording for the Lagrangian (L04.html:55 cites it); L03 was checked only for the labels that L04-L06 cite (Lemma 1.4, Theorem 2.1, Example 3.1, Example 4.1, Definition 1.2, Open item 3.2). Figures: none on L04-L06. No external source was read; no bibliographic claim remains in the slice.",
    ],
    "summary": {},
}
counts = {}
for r in R:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
frag["summary"] = {"rows": len(R), "pass": counts.get("PASS", 0), "fail": counts.get("FAIL", 0), "unverifiable": counts.get("UNVERIFIABLE", 0)}
with open("/tmp/verifyB2-M7-b/ledgers/M7/M7-b.json", "w", encoding="utf-8") as f:
    json.dump(frag, f, ensure_ascii=False, indent=2)
print(frag["summary"])
