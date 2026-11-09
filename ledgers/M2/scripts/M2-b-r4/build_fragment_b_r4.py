"""Build the round-4 slice-b ledger fragment (ledgers/M2/M2-b.json) from the verification record in this checkout."""
import json, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS4-M2-b")
S = "ledgers/M2/scripts/M2-b-r4/"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---- gates and whole-slice checks
row("RUN-M2-CHECKS", "2.9 gates: check_pages, check_dag, check_projects, run_labs (unit M2)",
    "tools/check_pages.py --unit M2; tools/check_dag.py --unit M2; tools/check_projects.py --unit M2; tools/run_labs.py --unit M2",
    "PASS", f"{S}g01_check_pages_unit.out: 'check_pages M2: PASS'; {S}g02_check_dag.out: 'check_dag M2: PASS'; "
    f"{S}g03_check_projects.out: 'check_projects M2: PASS'; {S}g04_run_labs_M2.out: 'run_labs M2: PASS (27/27)'.")
row("LAB-GATES", "2.5 labs: ruff, mypy strict, relevant pytest on the six slice twins",
    "tests/labs/M2/lab-M2-L07-1.py .. lab-M2-L12-1.py", "PASS",
    f"{S}g07_ruff_check_twins.out: 'All checks passed!' and '27 files already formatted'; {S}g08_mypy_twins.out: "
    f"'Success: no issues found in 27 source files'; {S}g09_pytest_labs_pagechecks.out: pytest tests/test_labs.py "
    "tests/test_run_labs.py tests/test_page_checks.py tests/test_refs.py -k 'M2 or lab or page' exit 0.")
row("PAGE-SMOKE-L07-L12", "2.5/2.9 page_smoke (Chromium, light and dark, 360 px, figure sweep) for L07-L12 alone",
    "tools/page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12", "PASS",
    f"{S}g06_page_smoke_L07_L12.out: six 'page_smoke modules/M/M2/Lnn.html: PASS' lines, 'page_smoke M2: PASS', exit 0. "
    "Visual inspection of a screenshot at 360 px and in dark mode was not performed (see notes).")
row("TWIN-ISOLATED", "2.5 labs: each twin run alone under python -I -W error, from /tmp",
    "tests/labs/M2/lab-M2-L07-1.py .. lab-M2-L12-1.py", "PASS",
    f"{S}g05_twins_isolated_L07_L12.out: exit 0 for all six, empty stderr; output line counts 43, 17, 22, 26, 10, 21.")
row("REFS-OFFLINE", "2.1 citations: verify_refs offline and live for M2; slice cites no registry key",
    "tools/verify_refs.py --offline; tools/verify_refs.py --unit M2; course/modules/M/M2/L07.html..L12.html", "PASS",
    f"{S}g10_verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'; {S}g15_verify_refs_live_M2.out: "
    "'live re-verification of M2: 2 of 560 entries, 0 problems'. L07-L12 references sections read: 'No registry key is cited'.")
row("DELTA-HUNKS", "2.1-2.9 round-4 delta: every hunk in the slice paths since pin 8196077d",
    "git diff 8196077d edbb7aa8 -- course/modules/M/M2/L07.html..L12.html tests/labs/M2/lab-M2-L07-1.py cards.json",
    "PASS", f"{S}delta_slice_b_8196077d_edbb7aa8.diff read hunk by hunk (346 lines): 'Assuming Assumption 2.1' tags added to "
    "statements and problems, Example 2.2 title and Remark 1.4 title in L09/L11 reworded, L09 R2 delta renamed eta, L07 "
    "Remark 4.3 and canon-breaks wording, L07 lab part D text and expected block. All changed text re-verified in this round.")

# ---- lab twins (page code == twin, expected == fresh run)
for L in ["L07", "L08", "L09", "L10", "L11", "L12"]:
    extra = {
        "L07": "Part D quotients (0, 2, -2) and exact fractions in parts A-C recomputed by hand (see NUM-L07).",
        "L08": "Part A 133 pairs and part B 70 pairs are the counts stated in the hypothesis; the bound 2^(n+2)x^(n+1) rechecked.",
        "L09": "Part A table recomputed in exact fractions; part C errors -1/(12n^2) match printed midpoint values.",
        "L10": "Part C central difference recomputed; error budget in L10 E3 recomputed by hand.",
        "L11": "Part A midpoint value 1/60 and part B 8/3 recomputed; N = 100000 midpoint error ~1e-10.",
        "L12": "Parts A and B exact; part C harmonic values recomputed in float (H_16384 - 1 = 9.28130671).",
    }[L]
    row(f"LAB-{L}", f"2.5 lab: {L} lab 1 twin, page code equals twin, expected block equals a fresh run",
        f"course/modules/M/M2/{L}.html lab section; tests/labs/M2/lab-M2-{L}-1.py", "PASS",
        f"{S}g11_lab_match_L07_L12.out: '{L}: page_code_eq_twin=True ... expected_eq_output=True ... run_exit=0'; "
        f"{S}g05_twins_isolated_L07_L12.out; run_labs PASS (g04). {extra} Hypothesis and interpretation sentences checked "
        "against the code and the output.")
row("LAB-L07-DOC", "2.5 lab statements vs code: helper for x != 0 applied at x = 0 (lab docstring and naming)",
    "tests/labs/M2/lab-M2-L07-1.py:233-234 and :250-251; course/modules/M/M2/L07.html:309 (interpretation)", "FAIL",
    "Helper g_prime_for_x_nonzero is documented as 'the derivative of g at x != 0' (line 234) but is called at x = 0 in part D "
    "(line 250, g_prime_for_x_nonzero(Fraction(0))) and returns 0, which equals Example 4.1's g'(0) = 0, so the printed output "
    "is correct. The name and docstring contradict the call. LOW (naming/docstring). Not a wrong output.",
    "Rename the helper to a name that covers 0 (for example g_prime_formula) and change its docstring to say it is the formula "
    "2|x| applied at 0 as well, with g'(0) = 0 from Example 4.1. Then run tools/embed_labs.py course/modules/M/M2/L07.html "
    "--refresh lab-M2-L07-1, rerun the twin under python -I -W error and run_labs --page L07.")

# ---- structure, numbers, mathematics, grades per lesson
for L in ["L07", "L08", "L09", "L10", "L11", "L12"]:
    row(f"STRUCT-{L}", "2.9 structure: template sections, tiers (3 mechanics, 3 proof, 3 empirical, 3 research), quiz 8-15, "
        "key-results table, lesson nav", f"course/modules/M/M2/{L}.html", "PASS",
        f"{S}g01_check_pages_unit.out (check_pages M2 PASS); read in full this round: why-it-matters, sections, four problem "
        "tiers with three problems each, key-results table, quiz, references, nav links resolve.")
for L in ["L07", "L08", "L09", "L10", "L11", "L12"]:
    row(f"NUM-{L}", "2.2 numbers: every number in prose and displayed numbers recomputed",
        f"course/modules/M/M2/{L}.html (prose, solutions, expected blocks)", "PASS",
        f"{S}numbers_b.py with {S}g13_numbers_b.out (unrounded recomputation of each stated value); manual recomputation of "
        "the rest in the verification record (e.g. L08 xi values 0.0693951, 0.1294494, 0.0496772; L09 U-L 0.159334 and "
        "E3 bounds 0.010067/0.009868; L11 E1 N=816 1.00122e-6, N=817 9.98768e-7; L12 H_16384-1 = 9.28130671).")
MATH = {
    "L07": "Prop 1.4 induction, Lemma 1.6, Prop 2.3, Lemma 3.1 Bernoulli argument, Thm 3.2, Ex 4.1 and Prop 4.2 checked line by line; "
           "Problems M1-M3, P1-P3, E1-E3, R1-R3 solutions recomputed.",
    "L08": "Lemma 1.1, Thm 1.2 (Rolle, cited L06 Thm 2.2), Thm 2.1 Rolle-induction construction, Cor 2.2, Ex 2.3-2.4, Remarks "
           "3.1-3.3 checked; Problems M1-M3, P1-P2, E1-E3, R1-R3 solutions recomputed.",
    "L09": "Lemma 1.1 refinement, Lemma 1.2, Def 1.3, Thm 2.2 (monotone integrability) and Cor 2.3 proofs checked; Lemma 3.1 "
           "algebra; Ex 3.2 U_n-L_n = 1/n and integral 1/3; Problems M1-M3, P1-P3, E1-E3, R1-R3 recomputed.",
    "L11": "Lemma 1.1 linearity (both cases of c), Cor 1.2, Thm 2.1 (IBP) and Ex 2.2-2.3, Thm 3.1 proof (both cases) and Ex 3.2-3.3, "
           "Problems M1-M3, P1-P3, E1-E3, R1-R3 (R1 induction step) recomputed.",
    "L12": "Lemma 2.1, Thm 2.2 (F' = x^{-p} and the truncation error), Lemma 3.1, Lemma 3.2, Thm 3.3, Remark 3.4, Problems "
           "M1-M3, P1-P3, E1-E3, R1-R3 recomputed.",
}
for L, t in MATH.items():
    if L == "L10":
        continue
    row(f"MATH-{L}", "2.4 mathematics: every statement, proof, hypothesis, derivation and worked solution",
        f"course/modules/M/M2/{L}.html (statements, proofs, worked solutions, problem solutions)", "PASS", t)
row("MATH-L10", "2.4 mathematics: statements, proofs and solutions of L10; quantifiers in statements",
    "course/modules/M/M2/L10.html:101-102 (Corollary 3.1); card M2-c137", "FAIL",
    "Proofs of Thm 1.2 (MVT use), Thm 2.1 (sandwich and I_* = I^*), Ex 2.2, Prop 4.1, Ex 3.2, Problems M1-M3, P1-P3, E1-E3 "
    "(E3 error budget recomputed: h^2 F'''/6 = 3.5e-13; rounding bound 5e-11), R1-R3 are correct. Wording defect (LOW): "
    "Corollary 3.1 states 'for every integer k >= 0 and every 0 <= a < b (for a = b, both sides are 0 ...)'. The main "
    "quantifier excludes a = b while the parenthetical includes it.",
    "Change the quantifier to 'every 0 <= a <= b' and keep the a = b parenthetical (both sides 0 by the convention of Lesson 9, "
    "Definition 1.3), or state 'every 0 <= a < b, and when a = b both sides are 0'. Make card M2-c137 say the same.")
row("GRADE-L07-L12", "2.3 grades: every claim span graded T with its proof on the page; examples and remarks ungraded",
    "course/modules/M/M2/L07.html..L12.html (data-grade spans, key-results tables)", "PASS",
    "Every data-grade=T span (Prop 1.4, Lemma 1.6, Prop 2.3, Lemma 3.1, Thm 3.2, Prop 4.2; Lemma 1.1-1.2, Thm 1.2, Thm 2.1, "
    "Cor 2.2; Lemma 1.1, Thm 2.2, Cor 2.3, Lemma 3.1; Thm 1.2, Thm 2.1, Cor 3.1, Prop 4.1; Lemma 1.1, Cor 1.2, Thm 2.1, Thm 3.1; "
    "Lemma 2.1, Thm 2.2, Lemma 3.1, Lemma 3.2, Thm 3.3) has a proof on the page. Key-results rows match their claims. "
    "Page-level grades only; card-level grades are in CARD-* rows.")

# ---- cards
row("CARD-L07", "2.7 cards of L07 (23 cards: c075-c096, c395): content vs lesson, numbers, grade and basis",
    "course/modules/M/M2/cards.json:591-600 (M2-c085); other L07 cards read in full", "FAIL",
    f"All 23 cards read against L07.html and checked ({S}cards_slice_b_dump.txt). M2-c085 (grade C, basis 'Lab 1, part B "
    "(exact check, printed decimals)') asserts that the error at degree 10 for x = 3/10 is 0.0000025307 and that it equals "
    "x^11/(1 - x) = (3/10)^11 divided by 7/10 'to five significant figures (Example 2.4)'. L07.html:130 derives exactly this "
    "value by hand in numbered Example 2.4. Under ruling 13 a value derived by hand in a numbered Example is graded T with the "
    "Example as basis, even when a lab also prints it (same class as the M2-a round-3 row L05-CARD-01). LOW (grade label, "
    "under-grade; not an over-grade).",
    "Grade the equality 'error = x^11/(1-x) = 2.5307e-6 to five significant figures' as T with basis 'Example 2.4 (L07.html:130)'. "
    "Keep the printed-output claim as C with basis 'Lab 1, part B' or ask only for the printed value.")
row("CARD-L08", "2.7 cards of L08 (19 cards: c097-c114, c417): content vs lesson, numbers, grade and basis",
    "course/modules/M/M2/cards.json (M2-c097..c114, M2-c417)", "PASS",
    f"All 19 cards read against L08.html; numbers on each card appear in L08.html (g12_cards_checks_b.out: 'numbers not found in "
    f"own lesson page: 0'). Round-3 FAIL (duplicates M2-c416/c417) is resolved: c416 is removed and c417 is a different card "
    "(Remark 1.3). C cards c105-c107 are lab-scoped (sampled pairs and printed rows).")
row("CARD-L09", "2.7 cards of L09 (18 cards: c115-c132): content vs lesson, numbers, grades, and the forward reference",
    "course/modules/M/M2/cards.json:905-914 (M2-c129); L09.html:280 (Misconception 2)", "FAIL",
    "Card M2-c129 is graded T with no basis. Its back says that the left- and right-endpoint sums (both 1/8) 'both lie below the "
    "integral 1/6' and then 'The value 1/6 is a forward reference to Lesson 10, Theorem 2.1, not derived here.' L09.html:280 "
    "says the same: 'That value is a forward reference, not derived here.' Nothing in Lesson 9 derives 1/6, so the claim is "
    "graded above its evidence in this lesson (over-graded claim, blocking under ruling 26). The statements that the sums equal "
    "1/8 are direct computations and are T. The other 17 cards are correct against L09.html and their numbers appear in the page.",
    "Either grade the card T only for 'both sums equal 1/8' (basis: Definition of the sums in L09 Section 1) and move 'both lie "
    "below 1/6' to a separate card graded C with basis 'Lesson 10, Theorem 2.1 with Lesson 11, Lemma 1.1 (forward reference; not "
    "derived in Lesson 9)', or delete the 1/6 comparison from the card. The quiz item q8 may keep its forward-reference wording.")
row("CARD-L10", "2.7 cards of L10 (16 cards: c133-c147 (c144 absent), c418, c421): content vs lesson, grades",
    "course/modules/M/M2/cards.json:960-961 (M2-c137)", "FAIL",
    "All 16 cards read against L10.html and checked; numbers on cards appear in the page; c418 and c421 are not duplicates "
    "(round-3 duplicate c418 is rewritten). M2-c137 repeats the wording defect of MATH-L10: 'for every integer k >= 0 and every "
    "0 <= a < b (for a = b both sides are 0 ...)'. LOW.",
    "Make M2-c137 match the corrected Corollary 3.1 statement (quantifier 0 <= a <= b, or the stated a = b convention).")
row("CARD-L11", "2.7 cards of L11 (16 cards: c148-c163): content vs lesson, numbers, grades",
    "course/modules/M/M2/cards.json (M2-c148..c163)", "PASS",
    f"All 16 read against L11.html; {S}g12_cards_checks_b.out: numbers on each card appear in the lesson. C cards c156-c158 are "
    "lab results (midpoint sums) and are lab-scoped; T cards carry Theorem/Example bases that the page proves.")
row("CARD-L12", "2.7 cards of L12 (17 cards: c165-c180, c398): content vs lesson, numbers, grades",
    "course/modules/M/M2/cards.json (M2-c165..c180, M2-c398)", "PASS",
    f"All 17 read against L12.html; {S}g12_cards_checks_b.out: numbers on each card appear in the lesson. Assumption 2.2 card "
    "(c398) matches the statement in L12 R3. C cards c170-c172 are lab-scoped printed values.")
row("CARD-DUP", "2.7 cards: full-deck duplicate scan (all 394 cards) and near-duplicate scan involving slice cards",
    "course/modules/M/M2/cards.json (all 394 cards)", "PASS",
    f"{S}g12_cards_checks_b.out: 'cards 394 unique ids 394 unique fronts 394', 'duplicate ids []'. difflib front similarity "
    ">= 0.75 gives 22 pairs, all distinct facts (the L07 pair M2-c085/c086 is two different lab questions; the L10/L11 integral "
    "pairs are different integrals). Back similarity >= 0.70: 0 pairs.")

# ---- structure, notation, prose, dag, misc
row("DAG-L07-L12", "2.9 DAG: check_dag and concept links resolve; later-module names used only as prose",
    "course/modules/M/M2/L07.html..L12.html", "PASS",
    f"{S}g02_check_dag.out PASS. Links resolve: L01.html#def-limit, L04.html#def-derivative, L09.html#def-definite-integral, "
    "#def-taylor-theorem (L08 dfn), concepts.html#mathematical-induction. Each dfn appears once (taylor-theorem in L08, "
    "definite-integral in L09). Names of later-module concepts (monotone convergence, M6; linear map, M3) appear only as plain "
    "prose; the architect's rulings Q5-Q7 allow later-module concepts as plain prose.")
row("XREF-L07-L12", "2.9 cross-references to earlier lessons and problems point to what they say",
    "course/modules/M/M2/L07.html..L12.html", "PASS",
    "Checked against the pages: L06 Assumption 2.1 (EVT), Thm 2.2 (Rolle), Thm 2.3 (MVT), Cor 3.1 (monotonicity); L05 Prop 1.2 "
    "(product), Prop 1.3 (quotient), Problem P1 (power rule), Prop 2.1 (chain); L04 Prop 2.1 (differentiable implies continuous); "
    "L03 Prop 2.2 (two-sided limit needs both one-sided limits); L01 Problem M3 (solution shows 1/n -> 0); L02 limit laws; "
    "L07 Lemma 3.1, Problem L07-P3, Example 1.3; L09 Thm 2.2, Lemma 1.1, Def 1.3; L10 Thm 2.1; L11 Lemma 1.1.")
row("NOT-L09-R", "2.4/2.9 notation: no registered symbol with another meaning (rule 13) in L09 Riemann sums and partitions",
    "course/modules/M/M2/L09.html Section 1 (R, P, Q, S, M_i, m_i, I_*, I^*)", "PASS",
    f"{S}notation_scan_b.py -> {S}g16_notation_scan_b.out: registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, Q "
    "appear 0 times in L07-L12; \\R is used (17 times, L11). R, P, S in L09 are local letters defined in the lesson.")
row("NOT-GLOBAL", "2.4/2.9 notation: macros used vs the registry (notation/notation.json)",
    f"course/modules/M/M2/L07.html..L12.html math", "PASS",
    f"{S}g16_notation_scan_b.out: no \\mathbb in the slice; every non-standard command is \\R (registered); standard commands "
    "only otherwise. Local letters (N, m, n, k, h, h_m, B(m,n), J, H_N, F, G, H, g, K, w, c, delta, eta, xi) are defined where used.")
row("PROSE-BANNED", "2.9 prose: banned phrases (BUILDER_RULES 1.3-1.4), placeholders, filler, rhetorical transitions",
    "course/modules/M/M2/L07.html..L12.html (visible text, cards)", "PASS",
    f"{S}prose_scan_b.py -> {S}g14_prose_scan_b.out: banned_hits={{}} for all six pages and for the slice cards; question marks "
    "occur only in quiz prompts.")
row("PROSE-PROCESS", "2.9 no process words in learner text (builder, verifier, ledger, ruling, plan)",
    "course/modules/M/M2/L07.html..L12.html; slice cards", "PASS",
    f"{S}g14_prose_scan_b.out: process_hits=[] for all six pages and all slice cards. Scope words (only, always, every, exactly, "
    "small, most, same) were read in context (see verification record): each sits next to a computation, hypothesis or quoted "
    "misconception.")
row("HOURS-L07-L12", "1 hours: 10 study hours per lesson; slice share of the hub split (240 lesson hours)",
    "course/modules/M/M2/L07.html..L12.html eyebrow; course/modules/M/M2/index.html data-hours-lessons", "PASS",
    f"Each eyebrow reads '10 study hours' ({S}g01_check_pages_unit.out: check_pages M2 PASS, which enforces the hub split of "
    "240 and 60 hours).")
row("LINK-L11-chain", "2.9 DAG/prose: L11 Uses line and forward-free chain of results",
    "course/modules/M/M2/L11.html:38 (Uses meta-row) and Section 2-3 dependencies", "PASS",
    "Uses: L09 definite integral and Darboux sums, L10 FTC, L05 product and chain rules, L04 continuity of differentiable "
    "functions, L06 Assumption 2.1. Each result cited (L09 Thm 2.2, L10 Thm 2.1, L10 Cor 3.1) appears earlier in the sequence.")
row("PROOF-L11-hyp", "2.4 hypotheses: L11 Theorem 2.1 (integration by parts) and Theorem 3.1 (change of variables) list every hypothesis",
    "course/modules/M/M2/L11.html:83-124", "PASS",
    "Thm 2.1 hypotheses: a<b, u and v differentiable on open I containing [a,b], u'v and uv' integrable (listed). Thm 3.1: "
    "a<b, g(a)<=g(b), hypotheses 1-3 listed; proof uses F continuous on [g(a),g(b)] (subset of J) and H = F o g continuous on [a,b]. "
    "Examples 2.2-2.3 and 3.2-3.3 verify each listed hypothesis.")
row("PROOF-L12-integrability", "2.4 hypotheses: L12 Theorem 2.2 and Lemma 3.2 (integrability of x^(-p) and 1/x on finite intervals)",
    "course/modules/M/M2/L12.html:81-92 and 217-220", "PASS",
    "x^(-p) and 1/x are positive and nonincreasing on [1,b] and [1,N]; integrable by L09 Thm 2.2 (listed as the source); "
    "F(x) = -1/((p-1)x^(p-1)) is continuous on [1,b] and differentiable on (1,b) with F' = x^(-p) (quotient rule verified).")
row("QUIZ-L07-L12", "2.9 retrieval quiz: correct options and numeric answers with tolerances (six pages, 66 items read)",
    "course/modules/M/M2/L07.html..L12.html quiz sections", "PASS",
    "Each data-correct option is correct and each numeric answer matches its explanation within its tolerance (e.g. L07 "
    "0.128571 vs 9/70; L08 0.0693951; L09 0.0651042 vs 25/384; L11 0.0166667 vs 1/60; L12 0.0000010 at 1/10^6 with tol 1e-7). "
    "L09 q8 has the forward-referenced value 1/6 as part of its correct option; the option and the explanation say it is a forward "
    "reference, so the item is not counted as an over-grade (see CARD-L09).")
row("MUTANTS-NA", "2.6 mutation: slice b has no project grader", "ledgers/M2/mutants/ (not created for this slice)", "PASS",
    "Slice b is lessons L07-L12 and their labs and cards; the M2 project grader belongs to the project slice. Ruling: mutation "
    "testing applies to project graders only; lab twins are demonstrations. mutants list is empty by design.")

fragment = {
    "unit": "M2",
    "slice": "b",
    "round": 4,
    "verifier": "independent Haiku verifier, M2 slice b (L07-L12, lab twins and cards), round 4 (FINAL FULL); fresh context, no builder context",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "8196077d5f56c3919d33e69888176d197d378ad4 (round-3 pin; round-3 fragment /Users/billyribeiro/.fanout/frags/S-M2-b.round3.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS4-M2-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyS4-M2-b/ledgers/M2/scripts/M2-b-r4",
    "verified_at": "2026-11-09T07:45:00Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Full re-verification (rule: FINAL FULL). Every page L07-L12 and every slice card was read in full; no previous PASS row was carried. The 109 slice cards (L07 23, L08 19, L09 18, L10 16, L11 16, L12 17) were checked individually.",
        "Blocking (ruling 26) rows: CARD-L09 only. LOW rows: CARD-L07 (grade under-stated, c085), CARD-L10 and MATH-L10 (Corollary 3.1 quantifier wording, c137), LAB-L07-DOC (helper name vs call at 0).",
        "Round-3 FAIL rows CARD-L08, CARD-L10, CARD-DUP are re-verified and PASS: duplicate cards M2-c416 (removed) and the rewritten M2-c417 and M2-c418 no longer duplicate L06 cards; the full deck has no duplicate id or front.",
        "Judged lab-scoped and graded C correctly (not rows): M2-c086, c092, c093, c105-c107, c125, c126, c127, c139, c140, c141, c156-c158, c170-c172. Each asks what the lab printed or checked at tabulated or sampled points; the mathematical identities they touch are T on the pages (Example 2.3/2.4, Example 3.2, Problem L10-R3, Corollary 1.2, Proposition 4.2). Architect may prefer a T split for c125 and c170-c171; not required by ruling 13 as worded.",
        "Repository note: ledgers/M2/M2-b.json as tracked in this checkout was a round-10 fragment (pin e8b10b8); this round's fragment replaces it in the checkout only. Nothing was committed or pushed.",
        "Numbers in L07-L12 that the lab prints (e.g. U_128 = 0.33724976, H_16384 - 1 = 9.28130671) reproduce by formula or by the printed code; no number was found that the code does not produce.",
        "L07 lab interpretation sentence ('together with the definition at 0') is accurate in aggregate: part D's first loop uses the definition at 0; the second loop applies the formula at 0 (value 0). Recorded as LAB-L07-DOC for the naming only.",
        "Later-module names used in slice prose: 'monotone convergence property' (L12 Assumption 2.2; M6 concept name) and 'linear map' (L11 problem title; M3 concept name). Both are plain prose under the architect's Q5-Q7 and are not rows.",
        "Mutants: none. Slice b has no project grader (ruling: mutation testing is for project graders; lab twins are demonstrations).",
    ],
    "summary": ("M2-b round 4 on pin edbb7aa8: 47 rows; FAIL 4 (blocking 1: CARD-L09 over-graded T card M2-c129; LOW 3: CARD-L07 "
                "c085 under-grade, MATH-L10/CARD-L10 Corollary 3.1 quantifier wording, LAB-L07-DOC helper name). Verdict FAIL. "
                "All gates (check_pages, check_dag, check_projects, run_labs 27/27, twins isolated, page_smoke L07-L12, ruff, mypy, "
                "pytest subset, verify_refs offline and live M2) PASS."),
}
n = len(rows)
fails = [r for r in rows if r["status"] != "PASS"]
fragment["summary"] = fragment["summary"].replace("47 rows", f"{n} rows").replace("FAIL 4", f"FAIL {len(fails)}")
out = ROOT / "ledgers/M2/M2-b.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", n, "pass", n - len(fails), "fail", len(fails), [r["id"] for r in fails])
