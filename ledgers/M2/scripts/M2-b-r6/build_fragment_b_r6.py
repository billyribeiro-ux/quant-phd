"""Round-6 fragment builder for M2 slice b (delta verification from pin dde0486b to e896b7a4).

Writes ledgers/M2/M2-b.json. Every PASS row names the command output or the file read in this round, or carries
the round-5 row with the carry prefix when its subject is byte-identical since dde0486b (carry_identity_r6.out).
"""
import json
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS6-M2-b")
S = "ledgers/M2/scripts/M2-b-r6"
CARRY = "Carried from round 5 (byte-identical since the previous pin dde0486b; carry_identity_r6.out):"
CARD_CARRY = "Carried from round 5 (per-card identity with dde0486b; card_identity_r6.out):"

rows = []


def row(rid, check, location, evidence, status="PASS"):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})


row("RUN-M2-CHECKS", "2.9 gates: check_pages, check_dag, check_projects, run_labs (unit M2), plus --all for the three static gates",
    "tools/check_pages.py --unit M2; tools/check_dag.py --unit M2; tools/check_projects.py --unit M2; tools/run_labs.py --unit M2",
    f"Re-run at e896b7a4 (fresh): {S}/g01_check_pages_M2.out 'check_pages M2: PASS' exit 0; g02_check_dag_M2.out 'check_dag M2: PASS' exit 0; "
    f"g03_check_projects_M2.out 'check_projects M2: PASS' exit 0; g04_run_labs_M2.out 'run_labs M2: PASS (27/27)' exit 0; "
    f"g04b/g04c/g04d (--all): LX1, LX2, PC3 PASS exit 0. Command record: {S}/run_gates_r6.sh.")

row("LAB-GATES", "2.5 labs: ruff check and format, mypy strict, relevant pytest on the slice twins",
    "tests/labs/M2/lab-M2-L07-1.py .. lab-M2-L12-1.py",
    f"Fresh: {S}/g07_ruff_check_M2_twins.out 'All checks passed!' exit 0; g07b_ruff_format_M2_twins.out '27 files already formatted' exit 0; "
    f"g08_mypy_all.out 'Success: no issues found in 385 source files' exit 0 (mypy --no-incremental, whole project); "
    f"g09_pytest_labs_pagechecks.out: pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_refs.py "
    f"tests/test_page_smoke.py -k 'M2 or lab or page or refs' -q, all progress lines passing, exit 0.")

row("PAGE-SMOKE-L07-L12", "2.5 page smoke for the six slice pages, run alone",
    "tools/page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12",
    f"Fresh: {S}/g06_page_smoke_L07_L12.out: page_smoke modules/M/M2/L07..L12.html PASS each, 'page_smoke M2: PASS', exit 0.")

row("TWIN-ISOLATED", "2.5 twins alone under python -I -W error from a scratch directory",
    "tests/labs/M2/lab-M2-L07-1.py .. lab-M2-L12-1.py",
    f"Fresh: {S}/twin_isolated_r6.out: L07 exit 0 (43 stdout lines), L08 exit 0 (17), L09 exit 0 (22), L10 exit 0 (26), L11 exit 0 (10), "
    f"L12 exit 0 (21); stderr 0 bytes for each ({S}/twin_L07..L12.stderr). Twins byte-identical to dde0486b (carry_identity_r6.out).")

row("REFS-OFFLINE", "2.6 references: verify_refs offline and live for M2",
    "tools/verify_refs.py --offline; tools/verify_refs.py --unit M2; course/modules/M/M2/L07.html..L12.html",
    f"Fresh: {S}/g10_verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' exit 0; g12_verify_refs_live_M2.out "
    f"'live re-verification of M2: 2 of 560 entries, 0 problems' exit 0. references/references.json and tools/verify_refs.py byte-identical "
    f"to dde0486b (carry_identity_r6.out). No citation markup in the six pages changed.")

row("DELTA-HUNKS", "2.1-2.9 round-6 delta: every hunk in the slice paths between dde0486b and e896b7a4",
    "course/modules/M/M2/L10.html; course/modules/M/M2/cards.json (slice cards); L07-L09, L11, L12 pages and all six twins unchanged",
    "git diff dde0486b e896b7a4 read in full for the slice paths. L10.html: 2 hunks, line 79 (Theorem 2.1 sentence: 'Continuity of f is not a "
    "hypothesis of the theorem') and line 390 (key-results row 5, source cell). cards.json in-slice hunks: M2-c113 (L08, Remark 3.2 / Misconception 2 "
    "citation), M2-c135 (L10, same Theorem 2.1 wording), appended M2-c425 (L09, new T card). Out-of-slice hunks in the same file (M2-c002, c008, c064, "
    "c390, c424 in L01/L06; c233 in L15) are not graded here (FINAL-ARCHITECT-RULINGS 30: delta does not hunt outside the rows). Other changed files "
    "outside the slice: the L01, L05, index.html and plans/* diffs were read as context; other units' diffs are outside this slice and were not read. Byte identity: "
    f"{S}/carry_identity_r6.out; per-card: {S}/card_identity_r6.out.")

# Lab rows: L07, L08, L09, L11, L12 carried (page and twin byte-identical); L10 re-verified.
for n in ("L07", "L08", "L09", "L11", "L12"):
    row(f"LAB-{n}", f"2.5 lab: {n} twin, page code equals twin, expected block equals output",
        f"course/modules/M/M2/{n}.html lab section; tests/labs/M2/lab-M2-{n}-1.py",
        f"{CARRY} {n}.html and its twin. Fresh confirmation in this round: {S}/page_twin_r6.out '{n} code blocks 1 equal to twin [True] | "
        f"expected blocks 1 equal to fresh stdout [True]'; {S}/twin_isolated_r6.out exit 0, stderr 0 bytes.")

row("LAB-L10", "2.5 lab: L10 lab 1 twin, page code equals twin, expected block equals a fresh run, numbers and hypothesis",
    "course/modules/M/M2/L10.html lab section (lines 116-232); tests/labs/M2/lab-M2-L10-1.py",
    f"Re-verified (page changed outside the lab section). {S}/page_twin_r6.out 'L10 code blocks 1 equal to twin [True]; expected blocks 1 equal to fresh stdout [True]'. "
    f"Hypothesis (line 117: 3/n for part A, 3/(4n) for part B, error within 1e-7 for part C) matches the twin (U_n-L_n = 3/n and 3/(4n) asserted in exact Fractions) and the output. "
    f"Interpretation (L10.html:232, 'bracket narrows as 1/n', numerical not a proof) matches the code. Fresh numbers: {S}/numbers_L10_r6.out "
    f"(part A n=8 U-L 0.375 = 3/8; n=128 U-L 0.0234375 = 3/128; part B n=128 L 0.49707921, U 0.50293859, U-L 0.005859375 = 3/512; part C |central - f(0.3)| = 3.3e-12).")

row("LAB-L07-DOC", "2.5 L07 part D docstring and interpretation match the code and output",
    "tests/labs/M2/lab-M2-L07-1.py (g_prime_formula, part D); course/modules/M/M2/L07.html:309 (interpretation)",
    f"{CARRY} L07.html and lab-M2-L07-1.py byte-identical; fresh twin run exit 0 and page_twin_r6.out L07 True/True.")

for n, extra in (("L07", ""), ("L08", ""), ("L09", ""), ("L11", ""), ("L12", "")):
    row(f"STRUCT-{n}", f"2.3 structure of {n}: blocks, sections, hub links, eyebrow",
        f"course/modules/M/M2/{n}.html", f"{CARRY} {n}.html. check_pages M2 and page_smoke re-run fresh at e896b7a4: PASS (g01, g06).")

row("STRUCT-L10", "2.3 structure of L10: blocks, sections, hub links, eyebrow, key-results table",
    "course/modules/M/M2/L10.html (whole page, 492 lines)",
    "Fresh: check_pages M2 PASS (g01_check_pages_M2.out); page_smoke L10 PASS (g06). The two changed hunks replace text inside existing <p> "
    "(line 79) and <td> (line 390) elements; the section order (s1 to s10), block divs, quiz section and footer were read in full and are unchanged.")

for n in ("L07", "L08", "L09", "L11", "L12"):
    row(f"NUM-{n}", f"2.2 numbers on {n}: prose, solutions, expected blocks recomputed",
        f"course/modules/M/M2/{n}.html", f"{CARRY} {n}.html.")

row("NUM-L10", "2.2 numbers on L10: prose, solutions, expected blocks, quiz answers recomputed",
    "course/modules/M/M2/L10.html (Example 2.2, Example 3.2, Corollary 3.1 row, Lab 1 table, Problems M1-M3, E1-E3, R1-R3, quiz, canon-breaks bullet 2)",
    f"Fresh own script {S}/numbers_L10_r6.py -> numbers_L10_r6.out: F(1)-F(0) = -1 and F(2)-F(0) = 4; part A n=8 L -1.1796875 U -0.8046875 "
    f"U-L 0.375 = 3/8; part B n=8 U-L 0.09375 = 3/32; part B n=128 U-L = 3/512; part C |central - f(0.3)| 3.3e-12; F'''(0.3) 2.1008; "
    f"h^2 F'''/6 3.50e-13; M1 4; M2 26/3; M3 1/6; Example 2.2 1/2; canon-breaks bullet 2 F(1)-F(0) = 1-5 = -4 with integral of F' equal to 1 "
    f"(checked by hand, F(x)=x on (0,1) with F(0)=5, F(1)=1). All match the page text. Quiz q4 (11/2 and 1/2), q5 (1/2), q7 (26/3), q8 (0.375) match.")

row("MATH-L07", "2.4 mathematics: statements, proofs and solutions of L07",
    "course/modules/M/M2/L07.html", f"{CARRY} L07.html.")
row("MATH-L08", "2.4 mathematics: statements, proofs and solutions of L08",
    "course/modules/M/M2/L08.html", f"{CARRY} L08.html. Remark 3.2 (line 246) re-read for the M2-c113 citation.")
row("MATH-L09", "2.4 mathematics: statements, proofs and solutions of L09",
    "course/modules/M/M2/L09.html", f"{CARRY} L09.html. Remark 1.4, Theorem 2.2 and Corollary 2.3 (lines 90-116) re-read for M2-c425.")
row("MATH-L10", "2.4 mathematics: statements, proofs, solutions and canon-breaks of L10 (whole page re-derived)",
    "course/modules/M/M2/L10.html:75-88 (Theorem 2.1 and proof), 92-100 (Example 2.2), 101-112 (Corollary 3.1, Example 3.2), 238-256 (Prop 4.1, canon-breaks), 257-272 (misconceptions), 276-395 (problems and key results)",
    "Re-derived this round from the page text: Theorem 2.1 hypotheses (F continuous on [a,b], differentiable on (a,b), F' = f, f integrable) and the "
    "sentence 'Continuity of f is not a hypothesis of the theorem' (true: the statement has no continuity hypothesis on f, and the why-it-matters "
    "paragraph lists the same two hypotheses). Proof: MVT on each closed subinterval (F continuous on it), f(c_i) between m_i and M_i, telescoping, "
    "L <= F(b)-F(a) <= U for every P, I_* = I^* by integrability. Corollary 3.1 proof, Example 2.2 (quotient rule), Example 3.2 (f' = 6x >= 0; "
    "L06 Corollary 3.1 (i), L06.html:102), Prop 4.1 (H' = 0, MVT), P1 (induction), P2 (sandwich), P3, R1 (two-sided bound), R2, R3 (3/n). "
    "Canon-breaks bullet 2 and misconceptions 1 to 3 checked. No claim depends on the removed 'need not be continuous' sentence.")
row("MATH-L11", "2.4 mathematics: statements, proofs and solutions of L11",
    "course/modules/M/M2/L11.html", f"{CARRY} L11.html.")
row("MATH-L12", "2.4 mathematics: statements, proofs and solutions of L12",
    "course/modules/M/M2/L12.html", f"{CARRY} L12.html.")
row("GRADE-L07-L12", "2.4 grade attributes on L07-L12 and key-results grades",
    "course/modules/M/M2/L07.html..L12.html data-grade spans; L10 key-results table",
    "git diff dde0486b e896b7a4 on L10.html changes text only (two hunks, lines 79 and 390); no data-grade attribute changed. The key-results row 5 grade remains T. Other pages byte-identical (carry_identity_r6.out).")

for n in ("L07", "L08", "L09", "L11", "L12"):
    pass
row("CARD-L07", "2.7 cards of L07 (24 cards): content vs lesson, numbers, grade and basis",
    "course/modules/M/M2/cards.json (lesson L07 objects, 24 cards)",
    f"{CARD_CARRY} all 24 L07 card objects identical to dde0486b ({S}/card_identity_r6.out: 'slice cards identical to dde0486b: 109 of 112'; "
    "changed or added slice cards are only M2-c113, M2-c135, M2-c425). L07.html byte-identical.")

row("CARD-L08", "2.7 cards of L08 (19 cards): content vs lesson, numbers, grade and basis",
    "course/modules/M/M2/cards.json (M2-c113 changed; 18 other L08 cards identical); L08.html:246-249 (Remark 3.2), Misconception 2 (L08.html ~265)",
    "M2-c113 re-verified: front 'Does the Lagrange remainder give the exact error for a general function?' back 'No. The Lagrange form is exact only at the unknown point xi. "
    "The theorem gives the existence of xi and nothing about its value, so the error is bounded rather than computed (Remark 3.2, Misconception 2).' "
    "Remark 3.2 (L08.html:246-249) says xi is not computed in general and Theorem 2.1 gives no formula; Misconception 2 (second item of the list) states the same. "
    "Grade T; no numbers on the card. The other 18 L08 cards are identical to dde0486b (card_identity_r6.out).")

row("CARD-L09", "2.7 cards of L09 (20 cards): content vs lesson, numbers, grades, forward reference",
    "course/modules/M/M2/cards.json (new M2-c425 at the end; 19 other L09 cards identical incl. M2-c423, M2-c129); L09.html:90-91, 114-116",
    "M2-c425 (new, grade T) re-verified: front 'Do the Darboux form of Definition 1.3 and the Riemann-sum form agree?'; back 'For monotone f they agree in the limit "
    "of small mesh. Corollary 2.3 bounds every Riemann sum within delta |f(b) - f(a)| of the integral, so the sums converge to the integral as the mesh tends to 0 "
    "(Remark 1.4).' Remark 1.4 (L09.html:91) says Corollary 2.3 shows agreement for monotone f; Corollary 2.3 (L09.html:114-116, hypothesis: f monotone; "
    "conclusion |R - integral| <= delta |f(b)-f(a)| for every Riemann sum R). The monotone hypothesis is stated in the back. No numbers on the card. "
    f"Observation (not a FAIL): M2-c425 and M2-c122 (Corollary 2.3 bound) state the same bound for different questions; not a duplicate by id or front. "
    f"The other 19 L09 cards are identical ({S}/card_identity_r6.out).")

row("CARD-L10", "2.7 cards of L10 (16 cards): content vs lesson, grades",
    "course/modules/M/M2/cards.json (M2-c135 changed; 15 other L10 cards identical); L10.html:75-80",
    "M2-c135 re-verified: back 'Hypotheses: assuming Assumption 2.1 of Lesson 6, a < b, F is continuous on [a, b] and differentiable on (a, b) with F' = f there, "
    "and f is integrable on [a, b] in the sense of Lesson 9, Definition 1.3. Then the integral of f from a to b equals F(b) - F(a). Continuity of f is not a "
    "hypothesis of the theorem.' This matches the Theorem 2.1 statement at L10.html:75-80. Grade T. The other 15 L10 cards are identical to dde0486b "
    "(card_identity_r6.out).")

row("CARD-L11", "2.7 cards of L11 (16 cards): content vs lesson, grades",
    "course/modules/M/M2/cards.json (lesson L11 objects)", f"{CARD_CARRY} all 16 L11 card objects identical to dde0486b; L11.html byte-identical.")
row("CARD-L12", "2.7 cards of L12 (17 cards): content vs lesson, grades",
    "course/modules/M/M2/cards.json (lesson L12 objects)", f"{CARD_CARRY} all 17 L12 card objects identical to dde0486b; L12.html byte-identical.")

row("CARD-DUP", "2.7 full scan for duplicate card ids and fronts across the whole deck",
    "course/modules/M/M2/cards.json (all 398 cards)",
    f"Fresh: {S}/card_identity_r6.out: cards old 396, new 398; 'dup ids new none'; 'dup fronts new none' (fronts compared normalised, lower-cased); "
    "removed none; added M2-c424 (L01) and M2-c425 (L09); changed M2-c002, c008, c064, c113, c135, c233, c390.")

row("DAG-L07-L12", "2.8 concept links and DAG closure for L07-L12",
    "course/modules/M/M2/L07.html..L12.html",
    "Fresh: check_dag M2 PASS (g02_check_dag_M2.out). The changed sentences and the new card contain no concept link and introduce no concept name; "
    "L10 'Introduces: no registered concept' (L10.html meta-row) remains true.")

row("XREF-L07-L12", "2.9 internal cross-references (lesson, proposition, example, problem numbers) resolve to the stated result",
    "course/modules/M/M2/L07.html..L12.html; cards M2-c113, M2-c135, M2-c425; L10 key-results row 5",
    "Fresh: M2-c113 -> Remark 3.2 (L08.html:246) and Misconception 2 (L08.html list item 2) OK. M2-c425 -> Remark 1.4 (L09.html:90) and Corollary 2.3 "
    "(L09.html:114) OK. L10 key-results row 5 -> Theorem 2.1 proof (L10.html:82-88), Problem L10-P2 (L10.html:313), Problem L10-R3 (L10.html:370), "
    "Lab 1 part A (L10.html:117) OK. L11.html:124 and L12.html:288 cite Lesson 10 Theorem 2.1 with integrability as the stated hypothesis, consistent with the "
    "changed sentence. L06 Corollary 3.1 (i) (L06.html:102) for Example 3.2 OK.")

row("NOT-L09-R", "2.6 notation and reference statement in L09 Section 1 and Remark 1.4",
    "course/modules/M/M2/L09.html Section 1", f"{CARRY} L09.html (Section 1 and Remark 1.4 re-read in this round; unchanged).")

row("NOT-GLOBAL", "2.6 every symbol vs notation/notation.json (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) and single meaning per symbol",
    "course/modules/M/M2/L07.html..L12.html math; notation/notation.json (8 symbols)",
    "Fresh: fixed-string grep of the eight registered symbols in the six pages returns 0 for every symbol on every page (ledgers/M2/scripts/M2-b-r6/symbols_r6.out). The changed text uses f, F, a, b, "
    "L(f,P), U(f,P), I_*, I^*, delta (mesh), c_i, none of which is a registered symbol with a different meaning. notation/notation.json byte-identical to dde0486b.")

row("PROSE-BANNED", "1.3-1.4 banned strings and filler (BUILDER_RULES 1 items 3-4, 3 item 5)",
    "course/modules/M/M2/L07.html..L12.html; slice cards",
    f"Fresh: {S}/prose_scan_r6.out. No banned string in the changed sentences or the three changed cards. The only hits are the ellipsis at the end of "
    "retrieval-quiz prompts ('equals...', 'is...'), which are fill-in blanks rather than omitted content (the same quiz format as in round 5). "
    "'It can be shown' and 'obviously' absent.")

row("PROSE-PROCESS", "12 no process words in learner text",
    "course/modules/M/M2/L07.html..L12.html; slice cards",
    f"Fresh: {S}/prose_scan_r6.out. Changed text has no process word (round, verifier, ledger, fix, corrected, earlier version). Hits are mathematical "
    "uses only (delta as mesh, 'a fixed positive number', proof step 'Fix x').")

row("HOURS-L07-L12", "2.9 hours: each lesson's declared hours and the hub split",
    "course/modules/M/M2/L07.html..L12.html eyebrow and data-hours; course/modules/M/M2/index.html data-hours-lessons, data-hours-project",
    f"Fresh: {S}/hours_r6.out: data-hours=10 on L07-L12; index.html data-hours-lessons=240, data-hours-project=60; sum of lesson data-hours L01-L24 = 240 "
    "(24 x 10). index.html changed only in the rung-2 explain text (outside these attributes). check_pages M2 PASS.")

row("LINK-L11-chain", "2.9 L11 cross-links to Lesson 10 and the derivative chain",
    "course/modules/M/M2/L11.html:38 and Sections 2-3", f"{CARRY} L11.html. L11.html:124 Lesson 10 Theorem 2.1 use re-read against the changed L10 sentence: consistent.")
row("PROOF-L11-hyp", "2.4 L11 proofs and their hypotheses (substitution, L11.html:83-124)",
    "course/modules/M/M2/L11.html:83-124", f"{CARRY} L11.html.")
row("PROOF-L12-integrability", "2.4 L12 integrability arguments (L12.html:81-92, 217-220)",
    "course/modules/M/M2/L12.html:81-92 and 217-220", f"{CARRY} L12.html. L12.html:288 and 349 cite Lesson 10 Theorem 2.1 with integrability as a hypothesis: consistent.")

row("QUIZ-L07-L12", "2.2/2.7 retrieval quizzes L07-L12: each correct option and explanation recomputed",
    "course/modules/M/M2/L07.html, L08.html, L09.html, L10.html, L11.html, L12.html quiz sections",
    "L10 quiz re-read in full this round (L10.html:400-475, nine items): q1 F(b)-F(a); q2 4; q3 integrability of f (explanation cites Misconception 1, L10.html:260-262, consistent); "
    "q4 1/2 with 11/2 and 5 as distractors; q5 1/2; q6 last step I_* = I^*; q7 26/3; q8 0.375 (U_8-L_8 = 3/8); q9 MVT. Other quizzes byte-identical "
    f"to dde0486b ({S}/carry_identity_r6.out) and carried from round 5.")

row("MUTANTS-NA", "2.10 mutants for this slice (lab twins; project mutation testing not applicable)",
    "ledgers/M2/mutants/ (175 files, project-grader mutants of another slice)",
    "ledgers/M2/mutants unchanged between dde0486b and e896b7a4 (git diff empty). No mutant of a slice-b lab; lab twins are demonstrations (ruling on lab twins). "
    "Carried from round 5: none for this slice.")

row("KR-L10", "2.4 key-results row 5 (bracket of 3x^2-2 for every partition), source precision",
    "course/modules/M/M2/L10.html:390 (key-results row 5, source cell)",
    "Round-5 FAIL re-verified from scratch. New source cell: 'Theorem 2.1 proof; Problem L10-P2; Problem L10-R3 (U_n - L_n); Lab 1, part A (exact fractions, sampled n)'. "
    "Theorem 2.1 proof (L10.html:82-88) proves L(f,P) <= F(b)-F(a) <= U(f,P) for every partition P, and Example 3.2 (L10.html:111-112) supplies the integrability "
    "hypothesis for f = 3x^2 - 2, so the bracket of -1 holds for every P. Problem L10-P2 (L10.html:313-318) is the same sandwich for one partition. "
    "Problem L10-R3 (L10.html:370-375) proves U_n - L_n = 3/n for the uniform partition of a nondecreasing f. Lab 1 part A (twin lines 156-168) uses "
    f"Fraction sums and asserts the bracket and 3/n at n = 1..256 (sampled); {S}/numbers_L10_r6.out confirms True at each sampled n. PASS.")


# ---- assemble and write the fragment -------------------------------------------------------------------------------
fragment = {
    "unit": "M2",
    "slice": "b",
    "round": 6,
    "verifier": "independent Haiku verifier, M2 slice b, round 6 (delta verification from pin dde0486b); fresh context, no builder context",
    "pin": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a",
    "base": "dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-5 pin; round-5 fragment /Users/billyribeiro/.fanout/frags/S-M2-b.round5.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS6-M2-b (detached at e896b7a4, .venv symlinked)",
    "scratch": f"{ROOT}/{S}",
    "verified_at": "2026-11-09T11:50:00Z",
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta verification (round 6) per FINAL-ARCHITECT-RULINGS 30. Slice paths changed since dde0486b: course/modules/M/M2/L10.html (2 hunks), course/modules/M/M2/cards.json (slice cards M2-c113, M2-c135 changed; M2-c425 added). Lesson pages L07, L08, L09, L11, L12, all six twins, notation/notation.json, references/references.json, BUILDER_RULES.md, VERIFIER_RULES.md, tools/** used by the gates are byte-identical (carry_identity_r6.out).",
        "Round-5 non-PASS row KR-L10 (citation precision) is fixed at e896b7a4 and re-verified from scratch: PASS.",
        "Correction to round 5: the round-5 note justified the removed sentence 'The function f need not be continuous' with a Volterra-type example. Volterra's derivative is bounded but not Riemann integrable, so that example does not show a Riemann-integrable discontinuous derivative. The sentence is gone at e896b7a4 ('Continuity of f is not a hypothesis of the theorem'), which is true of the statement, so no row depends on the old justification.",
        "Out of slice, not graded (ruling 30): cards M2-c002, c008, c064, c390, c424 (L01, L06), M2-c233 (L15; now cites 'Problem E1' and the constant 0.3849002); index.html rung-2 explain text (cites Lesson 13); L01 and L05 page hunks; plans/FINAL-ARCHITECT-RULINGS.md rulings 30-34; plans/KNOWN-ISSUES.md additions.",
        "Observation (not a finding): M2-c425 and M2-c122 both state the Corollary 2.3 bound for monotone f. They ask different questions (Darboux versus Riemann-sum agreement, and the size of a Riemann sum's error), so they are not duplicates by id or front.",
        "Observation: pytest -q printed progress lines and exit 0 but no summary count line in g09_pytest_labs_pagechecks.out, so the collect count is not recorded here.",
        "Scratch directory ledgers/M2/scripts/M2-b-r6/ contains four files tracked at e896b7a4 before this round (dump_slice_cards.py, extract_text.py, recheck_numbers.py, twins_alone.sh; commit 7aa909e9). They were not authored or relied on in this verification.",
    ],
    "summary": (f"M2-b round 6 on pin e896b7a4 (delta from dde0486b): {len(rows)} rows; PASS {sum(r['status']=='PASS' for r in rows)}; "
                f"FAIL {sum(r['status']!='PASS' for r in rows)}. Gates re-run this round at e896b7a4: check_pages, check_dag, check_projects, run_labs 27/27, "
                "check_pages/dag/projects --all, twins isolated under python -I -W error, page_smoke L07-L12, ruff, mypy, pytest subset, build_site --check, "
                "verify_refs offline and live M2. Changed subjects re-verified: L10 page, M2-c113, M2-c135, M2-c425, cards CARD-DUP, index hours. Unchanged subjects carried with the prefix."),
}
out = ROOT / "ledgers/M2/M2-b.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "verdict", fragment["verdict"])
