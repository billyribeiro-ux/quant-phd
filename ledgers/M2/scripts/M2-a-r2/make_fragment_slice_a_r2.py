"""Writes the round-2 fragment ledgers/M2/M2-a.json for M2 slice a. Row evidence cites the scripts and outputs
kept under ledgers/M2/scripts/M2-a-r2/. Run from the checkout root with -I; it then validates with tools/ledger.py.
"""

from __future__ import annotations

import json
import sys

sys.path.insert(0, "tools")
import ledger  # noqa: E402

S = "ledgers/M2/scripts/M2-a-r2/"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates (2.5, 2.6 labs, 2.9 structure, DAG, references) ----
row("M2a-R1-G01", "2.9 structure gate: check_pages --unit M2", "tools/check_pages.py --unit M2", "PASS",
    f"Run at pin 9294b914: stdout 'check_pages M2: PASS', exit 0. Output kept at {S}g01_check_pages.out.")
row("M2a-R1-G02", "2.9 DAG gate: check_dag --unit M2", "tools/check_dag.py --unit M2", "PASS",
    f"Run at pin: 'check_dag M2: PASS', exit 0. Output kept at {S}g02_check_dag.out.")
row("M2a-R1-G03", "2.5 labs: run_labs --unit M2", "tools/run_labs.py --unit M2 (lab sections of index-linked L01-L06)", "PASS",
    f"Run at pin: 'run_labs M2: PASS (27/27)', exit 0 (the six slice labs are among the 27; code byte-identical to twin, "
    f"stdout matches expected block). Output kept at {S}g03_run_labs.out.")
row("M2a-R1-G04", "2.5 twins alone under python -I -W error", "tests/labs/M2/lab-M2-L01-1.py .. lab-M2-L06-1.py", "PASS",
    f"Each twin run alone from an empty temp directory with python -I -W error: exit 0, stderr 0 bytes, stdout equal to "
    f"the page expected blocks (compared by reading). Output kept at {S}g04_twins_isolated.out.")
row("M2a-R1-G05", "2.5 pytest lab suite for the six slice labs", "tests/test_labs.py -k 'M2 and (L01..L06)'", "PASS",
    f"'6 passed' (dots), exit 0; collect-only for M2 gives 27 lab tests. Output kept at {S}g07_pytest_labs.out.")
row("M2a-R1-G06", "2.9 page_smoke for index and L01-L06", "tools/page_smoke.py --unit M2 --pages index L01 L02 L03 L04 L05 L06 --skip-sweep",
    "PASS", f"All seven pages PASS; lab runtimes 0.0 s; exit 0; no figures on these pages (data-chart count 0, see {S}prose_scan_slice_a_r2.out). Output kept at {S}g08_page_smoke.out.")
row("M2a-R1-G07", "2.5 ruff and mypy on the six slice twins", "ruff check / ruff format --check / mypy --no-incremental on tests/labs/M2/lab-M2-L0[1-6]-1.py",
    "PASS", f"ruff: 'All checks passed!', '6 files already formatted'; mypy: 'Success: no issues found in 6 source files'. Output kept at {S}g05_ruff.out and {S}g06_mypy.out. Not run: the grader and project twins (slices d and e).")
row("M2a-R1-G08", "2.1 citations: verify_refs offline and live for M2", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M2", "PASS",
    f"'offline integrity: 560 entries, 0 problems'; live 'live re-verification of M2: 2 of 560 entries, 0 problems' (M2 keys spivak2008calculus and hubbard2015vector). Output kept at {S}g09_verify_refs_offline.out and {S}g10_verify_refs_live_M2.out.")

row("M2a-R1-G09", "2.6 project structure gate (applies to the unit; slice a has no project rows)", "tools/check_projects.py --unit M2", "PASS",
    f"Run at pin: 'check_projects M2: PASS', exit 0. Output kept at {S}g11_check_projects.out. run_graders and mutate_graders are not run here: they belong to the project slices (d, e), which hold the grader.")

# ---- hub ----
row("M2a-R1-H01", "2.9 hub sections: objectives (4-8), prerequisites, placement, lessons, ladder, data, reading",
    "course/modules/M/M2/index.html:45-194", "PASS",
    "Read in full. Seven objectives with measurable verbs (lines 48-56); prerequisites M1 and P0.1 linked (lines 61-65); placement section with data-mastery 0.8 and two data-skill items (lines 69-137); lesson map L01-L24 (lines 143-168, card text checked against each lesson's sections for L01-L06); four ladder rungs in order (lines 174-179); data status 'No real data' (line 184); core reading as registry keys (lines 190-191).")
row("M2a-R1-H02", "2.9 hours split and arithmetic", "course/modules/M/M2/index.html:29, 42, 141-142",
    "PASS", f"data-hours-lessons=240, data-hours-project=60 (line 29); 24 lessons x 10 h (card-grid kicker lines 144-167); 240 + 60 = 300 = curriculum; 60/300 = 20%, inside 10-40%. Recomputed in {S}recompute_slice_a_r2.out (HUB-hours).")
row("M2a-R1-H03", "2.9 placement arithmetic", "course/modules/M/M2/index.html:71", "PASS",
    f"Eight items (6 M1/P0.1 + 2 skill). 80% of 8 = 6.4, so at least 7 correct; 6/8 = 75%, 7/8 = 87.5%. Recomputed in {S}recompute_slice_a_r2.out (HUB-placement).")
row("M2a-R1-H04", "2.2 and 2.9 placement skill-check explanations against the project", "course/modules/M/M2/index.html:135 (skill check 2 explanation)",
    "FAIL",
    "The explanation says: 'The missing step of the rung 2 completion problem is the expansion of (1 + h)^3 - (1 - h)^3, taught in Lesson 5.' "
    "The rung 2 completion problem in course/modules/M/M2/project.html (lab 'Completion problem: the second difference and the dual product') blanks two lines only: the "
    "Dual.__mul__ product line (dot part) and the return of second_difference (the central second difference). It does not blank a cubic expansion. "
    "The item keys themselves are correct (3 + 0.1^2 = 3.01, data-answer 3.01, tolerance 1e-6; recomputed HUB-skill2 in "
    f"{S}recompute_slice_a_r2.out).",
    "Replace the sentence in index.html:135 with: 'This is the central difference of a cubic, worked in Lesson 5 (Misconception 3). The rung 2 completion problem asks for the second difference and the dual-number product line instead.' Owner: builder A (hub).")
row("M2a-R1-H05", "2.9 prerequisite links resolve; P0.1 entries honest", "course/modules/M/M2/index.html:61-65; course/concepts.html",
    "PASS", "M1 links quantifiers, direct-proof, proof-by-contradiction, mathematical-induction and exponential-and-logarithm resolve to concept entries 'defined here' (M1). P0.1 links evidence-grade, notation-conventions and project-ladder resolve to entries marked 'not yet released', as line 64 says. M1 title 'Precalculus & Mathematical Reasoning' matches curriculum/01-foundations.yaml:91-92.")
row("M2a-R1-H06", "2.9 placement explanations cite M1 correctly", "course/modules/M/M2/index.html:80, 89, 98, 107 (Hq1-Hq4)", "PASS",
    "Hq1 'M1, Lesson 1, Theorem 3.2 (a)' is the negation of forall-exists, which is course/modules/M/M1/L01.html Theorem 3.2 (a) (read). Hq2 'M1, Lesson 2' proves the square root of 2 is irrational by contradiction (M1/L02.html Theorem 2.5, read). Hq3 'M1, Lesson 6' is the finite geometric sum by induction (M1/L06.html, Theorem 2.2, read). Hq4 'M1, Lesson 3' defines the natural logarithm (M1/L03.html Definition 1.1, read).")
row("M2a-R1-H07", "2.9 cross-lesson pointer in L04 canon-breaks to Lesson 13 rounding", "course/modules/M/M2/L04.html:156; course/modules/M/M2/L13.html", "PASS",
    "L13.html states that the second error comes from computing with numbers that carry rounding error, and Proposition 3.2 bounds the rounding part by 2 delta/h (read). The pointer in L04 is accurate.")

# ---- visible text and cross-cutting ----
row("M2a-R1-X01", "2.9 banned phrases and placeholders", f"index.html, L01-L06.html visible text ({S}prose_scan_slice_a_r2.out)", "PASS",
    "Scan of visible prose (lab code excluded) for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown: zero hits in all seven pages.")
row("M2a-R1-X02", "2.9 process words in learner text", f"index.html, L01-L06.html visible text ({S}prose_scan_slice_a_r2.out)", "PASS",
    "Scan for builder, verifier, fixer, round, slice, ledger, fragment, orchestrat, subagent: zero hits. Read every sentence of the seven pages; none describes the build or verification process.")
row("M2a-R1-X03", "2.4 notation: macros and registry symbols", f"notation/notation.json; index.html, L01-L06.html ({S}prose_scan_slice_a_r2.out)", "PASS",
    "Only registered macro used is \\R (L02, L03, L04, L05, L06 pages). No \\mathbb in any slice page (round-1 ruling 1 holds). Registry symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q} do not occur in the slice; the page's difference quotient Q(h) (L04.html Definition 1.1) is plain Q, not the registered \\mathbb{Q} (a probability measure), so no registered meaning is reused. Local letters (N, M, c, m, p, q, B, d) are per-lesson, as notation.json says.")
row("M2a-R1-X04", "2.5 quiz numeric answers and tolerances", f"index.html placement; L01-L06 quizzes ({S}prose_scan_slice_a_r2.out, {S}recompute_slice_a_r2.out)", "PASS",
    "Every numeric answer recomputed exactly: index 2 and 3.01 (tol 1e-6); L01 1.999001 (tol 1e-6, 2001/1001), 10000, 0.1, 3; L02 3, 0.02990099 (tol 1e-8, 302/10100), 0.1090909 (tol 1e-7, 12/110); L03 7, 2, 1.39 (tol 5e-4); L04 2, 3.31, -0.25 (tol 1e-7), 0; L05 1, 96, 2, 0; L06 1.1547 (tol 1e-4, 2/sqrt3), -3, 8. All tolerances contain the exact value.")
row("M2a-R1-X05", "2.9 retrieval quiz structure (8-15 items, explanations, correct options)", f"L01-L06 quiz sections ({S}prose_scan_slice_a_r2.out)", "PASS",
    "Item counts 9, 9, 8, 9, 9, 9. Each item has an explain block. For every multiple-choice item the data-correct option matches its explanation (read).")
row("X-GRADE-01", "2.3 grades: every claim, key-results rows, ruling 13", "L01-L06 key-results tables, lab interpretations, cards", "PASS",
    "Proved results are T (Props, Examples, Corollaries, Theorems with proofs on the page; e.g. L05 Example 2.2 derives 95.0625 by hand and card M2-c055 is T). Lab-only values are C naming Lab 1 (L01 threshold 1000, L02 errors at n=10, L03 grid check, L04 quotient at 1e-6, L05 central differences, L06 grid count). Grade legend matches BLUEPRINT section 3 (T theorem, A replicated, B published not settled, C single study or lab result, D lore, X refuted).")
row("X-DEP-01", "2.9 and 2.4 DAG at the prose level", "index.html, L01-L06.html; check_dag output", "PASS",
    f"check_dag PASS ({S}g02_check_dag.out). Read the prose: L01-L06 use only M1 concepts and P0.1 names; continuity is prose in L02 section 2 before Corollary 2.2; central difference is defined in prose at L05.html:91 before Assumption 1.4 and the lab. No later-module concept (Fubini, Lagrange multiplier, Riemann-Stieltjes, Lebesgue, duration, convexity) appears in L01-L06 (scan {S}prose_scan_slice_a_r2.out); the only 'Taylor' in L06 is a navigation link to L07's title.")
row("X-HRS-01", "2.9 hours and why-it-matters length", "L01-L06.html header and why-it-matters paragraphs", "PASS",
    f"data-hours=10 on every lesson (lines 2). Why-it-matters word counts 85, 83, 96, 72, 93, 84 (all at most 120, BUILDER_RULES 4.2). Scan output in {S}prose_scan_slice_a_r2.out.")
row("X-CARD-IDS", "2.7 cards: ids, structure, numbers, duplicates (slice cards)", "course/modules/M/M2/cards.json (82 cards of L01-L06)", "PASS",
    f"390 cards in file, no duplicate id (non-sequential ids allowed, ruling 2). 82 slice cards: L01 16, L02 13, L03 14, L04 11, L05 13, L06 15. Every required field present; every number on a card appears verbatim in its lesson; no pair of slice cards at token-Jaccard >= 0.45 that tests the same fact (the three flagged pairs differ in fact: definitions of two limits, product versus quotient rule, two different theorems). Output {S}cards_scan_r2.out.")
row("X-REF-01", "2.1 core reading and references sections", "index.html:187-194; L01-L06 References sections", "PASS",
    "The only M2 registry keys are spivak2008calculus and hubbard2015vector (references.json used_by M2; status verified). No slice page carries data-cite or attributes a statement to them; each References section says no passage locator is confirmed (read). Registry records carry no edition field, which plan section 6.2 and architect Q14 accept.")

# ---- lessons ----
row("L01-MATH-01", "2.4 mathematics: sections 2-4", "course/modules/M/M2/L01.html:55-189",
    "PASS", "Definition 2.1; Proposition 2.2 (epsilon/2 and max(N1,N2) argument, read line by line); Example 2.3 (1/(n+1) identity re-derived, recompute L01-ex23-identity); Proposition 3.1; Example 4.1 (2 < 2 contradiction, recompute L01-ex41-eq); Proposition 4.2 with B = max(|a_1|..|a_{N-1}|, |L|+1). All hypotheses stated.")
row("L01-MATH-02", "2.2 and 2.4 problem set and key-results rows", "L01.html:219-322 and key results 324-339", "PASS",
    f"M1 (N=1297 for 0.01, recompute L01-M1), M2 (N=11, L01-M2), M3, P1-P3, E1 (1/1001 prints 9.990010e-04, L01-E1-1/1001), E2, E3 (N=10000, L01-Q3-E3), R1-R3 read; key rows T/C as stated.")
row("L01-LAB-01", "2.5 lab: page code, expected block, hypothesis values", "course/modules/M/M2/L01.html:87-150; tests/labs/M2/lab-M2-L01-1.py", "PASS",
    f"Code equals twin and expected equals output (run_labs, {S}g03_run_labs.out). Hypothesis values 1/2, 1/11, 1/101, N=1000, error at 999 = 1.000000e-3 recomputed (L01-lab-threshold, L01-err999). Interpretation and C grade name Lab 1.")
row("L01-GRADE-01", "2.3 grade of the threshold row", "L01.html:335; cards.json M2-c006", "PASS",
    "The 1000 threshold is graded C naming Lab 1. Its hand derivation sits in the lab hypothesis and E2/E3, not in a numbered Example, so C is the grade ruling 13 gives. Card and row share grade and basis (see L01-CARD-02).")
row("L01-PROSE-01", "2.2 and 2.9: problem-set intro against problem E3", "L01.html:221 and E3 at 289-294", "PASS",
    "Intro now reads 'Problems marked E use the output of Lab 1, except E3, which predicts a value from the formula of Example 2.3.' E3 predicts from the formula and says Lab 1 does not print the value. Round-1 FAIL is fixed.")
row("L01-QUIZ-01", "2.9 retrieval quiz", "L01.html:341-411", "PASS",
    "Nine items; correct options (eps first; a sequence with at most one limit; no change to the limit; (-1)^n no; nothing from boundedness) match explanations; numeric answers verified (X04).")
row("L01-CARD-01", "2.7 cards of L01", "cards.json lesson L01 (16 cards)", "PASS",
    "Read every L01 card against L01.html. Each definition, theorem, key formula and misconception of L01 has a card (M2-c001..c013, c376, c390, c391). Each card's back matches the current text, including the section references, the Misconception numbers, and the proof of Proposition 4.2 (c376).")
row("L01-CARD-02", "2.7 card grade and basis mirror the key-results row", "course/modules/M/M2/cards.json:40 (M2-c006); L01.html:335",
    "PASS", "Card basis is now 'Lab 1, a finite search over 1 to 5000; the identity |a_n - 2| = 1/(n+1) in Example 2.3', the same substance as the row (round-1 FAIL, identity missing, is fixed).")
row("L02-MATH-01", "2.4 mathematics: Proposition 1.1 (i)-(iii), Corollary 2.2, Examples 2.1 and 2.3", "course/modules/M/M2/L02.html:55-176",
    "PASS", "Proofs of (i), (ii) and (iii) re-derived line by line, including the bounds |a_n| < |a|+1 and |b|/(|b|+1) < 1 and the choices of N. The identity a_n/b_n - a/b = (b(a_n-a) - a(b_n-b))/(b b_n) and the epsilon bookkeeping in (iii) are correct. Corollary 2.2 hypotheses (continuity at a point of D) are stated.")
row("L02-MATH-02", "2.4 remark, canon-breaks, misconceptions, problems, key results", "L02.html:178-333",
    "PASS", "Remark 3.1 (a_n = 1, b_n = 1/n gives n); Misconception 2 (b_n = -(-1)^n diverges, sum 0); Misconception 3 (f(1) = 0 with formula limit 2); M1-M3, P1-P3, E1-E3 and R1-R3 read and re-derived (recompute L02-n1-quot, L02-E2-n100, L02-n10); key rows T/C as stated.")
row("L02-LAB-01", "2.5 lab: page code, expected block, interpretation", "course/modules/M/M2/L02.html:76-152; tests/labs/M2/lab-M2-L02-1.py",
    "PASS", f"run_labs and isolated run pass; errors at n = 1 (1.5), 10, 10000 recomputed (L02-closed-forms, L02-n10000). Interpretation says 'five indices' and the proof covers all n, both correct.")
row("L02-PROSE-01", "2.2 Example 2.1 title and its sentence", "course/modules/M/M2/L02.html:159-160", "PASS",
    "Title now '(the identity)'; the sentence now says 'Corollary 2.2 below, applied to the identity with itself, gives the square (Example 2.3).' Corollary 2.2 is about sums and products, and Example 2.3 uses it. Round-1 FAIL is fixed.")
row("L02-PROSE-02", "2.9 banned rhetorical-question opener (BUILDER_RULES 1.4)", "course/modules/M/M2/L02.html:51 (why-it-matters opener)", "FAIL",
    "The opener is the rhetorical question 'If each part settles down, does the combination settle down, and to what value?' followed by 'The limit laws answer this for sequences.' BUILDER_RULES 1.4 bans rhetorical-question transitions. The scan in " + S + "prose_scan_slice_a_r2.out lists it as the only question in slice prose outside prompts.",
    "Replace the two sentences at L02.html:51 with a declarative one, for example: 'The limit laws state when a sum, product or quotient of two convergent sequences converges, and to what value, under a stated hypothesis.' Owner: builder A (L02).")
row("L02-E-01", "2.2 problems E1-E3 use Lab 1 output", "course/modules/M/M2/L02.html:269-291", "PASS",
    "E1 sum error 12/110 = 6/55 printed 1.090909e-01; E2 302/10100 prints 2.990099e-02; E3 quotient error 3/2 at n=1 from (5n+4)/((n+1)(n+2)) = 9/6 — all verified (recompute L02-E1-prints, L02-E2-n100, L02-n1-quot).")
row("L02-QUIZ-01", "2.9 retrieval quiz", "L02.html:338-408", "PASS",
    "Nine items; options and explanations agree (quotient needs b != 0; (1,1/n) gives n; both (-1)^n and -(-1)^n diverge; continuity needs f(a) and sequences; identity; converse of product law). Numeric answers verified (X04).")
row("L02-CARD-01", "2.7 cards of L02", "cards.json lesson L02 (13 cards)", "PASS",
    "All thirteen read against L02.html. c025 and c026 basis 'Lab 1, exact values from the closed forms' has the same substance as the key row ('on the page' added there); judged a wording difference, not a basis difference.")
row("L03-MATH-01", "2.4 mathematics: sections 1-2", "course/modules/M/M2/L03.html:53-108", "PASS",
    "Definition 1.1; Example 1.2 (delta = eps/3, read); Proposition 1.3 proof; Corollary 1.4 proof (x_n = a case handled); Definition 2.1; Proposition 2.2 both directions; Example 2.3 bounds (|x+1| < 2 on (0,1); 2|x-1| on the right); Example 2.4.")
row("L03-MATH-02", "2.2 and 2.4 problem set and key rows", "L03.html:208-328", "PASS",
    "M1 (delta = 0.01 for eps = 0.02), M2 (sign function), M3 (q = x + 2, limit 4), P1-P3, E1-E3, R1-R3 read and re-derived; key rows T/C as stated.")
row("L03-MATH-03", "2.4 problem R2 (bounded factor and zero limit)", "course/modules/M/M2/L03.html:300", "PASS",
    "The solution now reads |f g| <= M|g| <= M eps/(M+1) < eps. The first inequality is non-strict, so M = 0 is covered. Round-1 FAIL is fixed.")
row("L03-LAB-01", "2.5 lab: page code, expected block, grid claim", "course/modules/M/M2/L03.html:112-173; tests/labs/M2/lab-M2-L03-1.py",
    "PASS", "run_labs and isolated run pass; table values 0.81, 2.2, 1.39 and the h = 0.0001 row recomputed exactly (L03-gap-formula); 38 grid points (L03-38pts). Docstring and interpretation match the code (the code prints True/False for three tolerances).")
row("L03-PROSE-01", "2.2 and 2.9: problem-set intro against E3", "L03.html:210 and E3 at 278-284", "PASS",
    "Intro now reads '... except E3, which predicts a result from the formula of Example 1.2.' E3 predicts whether the grid check would print True for delta = eps (recomputed: x = 2.095 gives 0.285 > 0.1). Round-1 FAIL is fixed.")
row("L03-QUIZ-01", "2.9 retrieval quiz", "L03.html:330-395", "PASS",
    "Eight items; correct options match explanations; numeric answers 7, 2, 1.39 (tol 5e-4) verified (X04).")
row("L03-CARD-01", "2.7 cards of L03", "cards.json lesson L03 (14 cards)", "PASS",
    "All read. c038 now uses w and matches misconception 2 and quiz item L03q6; c392 matches Section 1 (open interval).")
row("L04-MATH-01", "2.4 mathematics: sections 1-3", "course/modules/M/M2/L04.html:53-148", "PASS",
    "Definition 1.1 (difference quotient, differentiability, dfn); Example 1.2 (Q(h) = 2a + h, delta = eps); Proposition 2.1 proof (tolerance 1 then min(delta_1, eps/(|f'(a)|+1)), re-derived); Example 3.1 (|h|/h = +1 or -1; continuity via Lesson 1 Definition 2.1).")
row("L04-MATH-02", "2.2 and 2.4 problem set and key rows", "L04.html:178-296", "PASS",
    "M1 (f' = 5), M2 (f'(-1) = -2, Q(0.01) = -1.99), M3 (f'(2) = -1/4, recompute L04-M3), P1 (3a^2 with delta = min(1, eps/(3|a|+1))), P2, P3, E1-E3 (3.31, 3.00001e-5 at h = 1e-5, 3.000001 ratio), R1-R3; key rows as stated.")
row("L04-LAB-01", "2.5 lab: page code, expected block, hypothesis values", "course/modules/M/M2/L04.html:67-123; tests/labs/M2/lab-M2-L04-1.py",
    "PASS", f"run_labs and isolated run pass; Q(h) = 3 + 3h + h^2 at six steps (L04-expansion, recomputed exactly); error at 1e-6 prints 3.000001e-06 and error/h prints 3.000001 (L04-err-1e-6); Q(0.001) = 3.003001 (L04-Q001).")
row("L04-CARD-01", "2.7 duplicate scan of L04 cards (round-1 FAIL)", "cards.json:297 (M2-c044), cards.json:327 (M2-c048)", "PASS",
    f"M2-c048 was rewritten: it now asks whether a formula that looks smooth guarantees a derivative and answers with the rule (Misconception 1), using Example 3.1 as the instance. M2-c044 asks the specific derivative of |x| at 0. They no longer test the same fact in the same wording, and the scan {S}cards_scan_r2.out shows no L04 pair above Jaccard 0.45. Judgement: not a duplicate. Round-1 FAIL is fixed.")
row("L04-QUIZ-01", "2.9 retrieval quiz", "L04.html:298-368", "PASS",
    "Nine items; explanations agree (difference quotient; f'(1) = 2; x^3 quotient 3.31; |x| no derivative; Proposition 2.1 direction; constant derivative 0; 3.003001; 1/x gives -1/4; definition uses Q(h) as h to 0). Numeric answers verified (X04).")
row("L04-CARD-02", "2.7 cards of L04 (ids c040-c050)", "cards.json lesson L04 (11 cards)", "PASS",
    "All eleven read against L04.html. c048 is now the misconception card, not a duplicate of c044.")
row("L05-MATH-01", "2.4 mathematics: Lemma 1.1, Propositions 1.2, 1.3, 2.1", "course/modules/M/M2/L05.html:53-89, 175-187",
    "PASS", "Lemma 1.1 (c) identity (M(F-L) - L(G-M))/(MG) re-derived and the bound 2/|M|^2 checked; product-rule identity f(a+h)Q_g + g(a)Q_f re-derived; quotient-rule identity (g(a)Q_f - f(a)Q_g)/(g(a)g(a+h)) re-derived; chain rule with G(k) and k(h) re-derived.")
row("L05-MATH-02", "2.4 Assumption 1.4 and every use of it", "L05.html:91-95, 99, 105, 219, 282", "PASS",
    "Assumption 1.4 states the central-difference expansion f' + h^2 f'''/6 + o(h^2), labelled assumed and not proved. Every use begins with 'Assuming Assumption 1.4' (lab hypothesis line 99, docstring line 105, Misconception 3 line 219, E1 line 282). p'''(1.5) = 141 and h^2 p'''/6 = 2.35e-7 (recompute L05-p3).")
row("L05-MATH-03", "2.2 and 2.4 problem set", "L05.html:224-327", "PASS",
    "M1 (x(x+1) derivative 2x+1), M2 (q'(1) = 0), M3 (w'(1) = 96), P1 power rule by induction, P2 reciprocal rule, P3 square, E1-E3, R1 (central difference of a cubic, identity checked symbolically at points, recompute L05-R1), R2, R3 (quotient from product and reciprocal). All correct.")
row("L05-LAB-01", "2.5 lab: page code, expected block, analytic and central values", "course/modules/M/M2/L05.html:97-173; tests/labs/M2/lab-M2-L05-1.py",
    "PASS", f"Analytic values 32.0625, 29/49, 95.0625 and central differences 32.062500235, 0.591836734, 95.062500855 recomputed (L05-analytic, L05-central-diffs); absolute differences 2.35e-07, 3.33e-10, 8.55e-07 (L05-diffs). run_labs and isolated run pass.")
row("L05-PROSE-01", "2.2 and 2.4 Misconception 3 numbers and assumption wording", "course/modules/M/M2/L05.html:218-219", "PASS",
    "Central difference of x^3 at 1 is 3 + h^2 (L05-MisconC3); error h^2 = 1e-8 at h = 1e-4; printed errors 2.35e-07, 3.33e-10, 8.55e-07 are not h^2; the leading term for p gives 2.35e-07 (L05-p3) and for c gives 8.55e-07 (L05-c3-leading), consistent with the printed c difference. Assumption 1.4 is not proved on the page.")
row("L05-QUIZ-01", "2.9 retrieval quiz", "L05.html:344-414", "PASS",
    "Nine items; correct options agree with explanations (product rule; quotient needs g(a) != 0; chain rule at f(a); x^3 central difference 3 + h^2; power rule by induction). Numeric answers 1, 96, 2, 0 verified (X04).")
row("L05-CARD-01", "2.7 cards of L05", "cards.json lesson L05 (13 cards: c051-c061, c379, c393)", "PASS",
    "All read. c055 (T) derives 95.0625 by hand as Example 2.2 does; c056-c058 (C) match the lab output and carry the same basis wording as the key-results row (substance equal).")
row("L06-MATH-01", "2.4 mathematics: Proposition 1.1, Theorem 2.2, Theorem 2.3, Corollary 3.1", "course/modules/M/M2/L06.html:55-109",
    "PASS", "Proposition 1.1 proof (Q(h) signs for h > 0 and h < 0, f'(c) <= 0 and >= 0); Rolle proof (max/min via Assumption 2.1, M != f(a) and c in (a,b)); MVT proof via g(x) = f(x) - f(a) - s(x-a); Corollary 3.1 (i)-(iii) from Theorem 2.3 with c in (x,y).")
row("L06-MATH-02", "2.4 misconceptions and section 4 canon-breaks", "L06.html:183-208", "PASS",
    "Misconception 1 (x^3 at 0, not an extremum); Misconception 2 (y^2 + xy + x^2 = (x + y/2)^2 + 3y^2/4 re-derived; x^3 strictly increasing with f'(0) = 0); Misconception 3 (c = 1/sqrt3 ~ 0.577, recompute L06-MisC3); section 4 counterexamples x on [0,1) and |x| on [-1,1] checked.")
row("L06-MATH-03", "2.2 and 2.4 problem set", "L06.html:210-313", "PASS",
    "M1 (critical point 2, f(2) = -3), M2 (c = 2/sqrt3 = 1.1547, recompute L06-M2), M3 (f'>0 on (-2,-1)), P1-P3 (P2 injectivity via Rolle; P3 via Corollary 3.1 (i)), E1 (count 8), E2 (f(-1) = 2, f(1) = -2), E3 (midpoints odd multiples of 1/8, recompute L06-E3-midpoints), R1 (x on [0,1) with f(1) = 0), R2 (|x-1| chord slope 0), R3 (Lipschitz from MVT).")
row("L06-LAB-01", "2.5 lab docstring claim against code", "course/modules/M/M2/L06.html:116-122 (page code block); tests/labs/M2/lab-M2-L06-1.py:116-125 (docstring)", "FAIL",
    "The docstring says: 'It checks three things: the sign of f' at each grid point ..., the direction of f on each grid interval ..., and the values f(-1) and f(1).' The code checks the first two (Compare nodes; signs_agree and the increasing and agreement counts). The only code that touches f(-1) and f(1) is print(f\"f(-1) = ...; f(1) = ...\"), with no comparison (scan " + S + "lab_claims_r2.out). Run results are correct: run_labs PASS, isolated run exit 0, expected block equal to output.",
    "In tests/labs/M2/lab-M2-L06-1.py docstring replace 'It checks three things: ... and the values f(-1) and f(1).' with 'It checks two things: ... and it prints the values f(-1) and f(1).' Then run tools/embed_labs.py course/modules/M/M2/L06.html --refresh lab-M2-L06-1 and tools/run_labs.py --unit M2. Owner: builder A (L06). Keep the expected block as is.")
row("L06-ASSUME-01", "2.4 Assumption 2.1 wording and dependence", "L06.html:71-73, 77-78, 86-88, 102-103, 324-325", "PASS",
    "Assumption 2.1 (extreme value theorem) is stated as an assumption with no grade (line 73). Theorem 2.2 (line 78), Theorem 2.3 (line 88) and Corollary 3.1 (line 103) begin 'Assuming Assumption 2.1'. Proposition 1.1 does not use it. Key row 'not graded' (line 325). Misconception 2 and 3 and Problem R3 use it only under the stated assumption.")
row("L06-QUIZ-01", "2.9 retrieval quiz", "L06.html:332-406", "PASS",
    "Nine items; correct options agree with explanations (Proposition 1.1 gives f'(c)=0; Rolle needs continuity on [a,b] and differentiability on (a,b); x^3 at 0 has zero derivative and no extremum; EVT is assumed; midpoint is not c). Numeric answers 1.1547 (tol 1e-4), -3, 8 verified (X04).")
row("L06-CARD-01", "2.7 cards of L06", "cards.json lesson L06 (15 cards: c062-c074, c394, c414)", "PASS",
    "All read. c414 (critical point) is a new card, and c062 no longer repeats it, so no duplicate. c394 matches the current R3. c064 matches Assumption 2.1 and its use in Theorems 2.2 and 2.3.")

fragment = {
    "unit": "M2",
    "slice": "a",
    "round": 2,
    "verifier": "independent verifier (Haiku 5.5), unit M2 slice a, round 2 (final full verification)",
    "pin": "9294b914 (detached checkout HEAD)",
    "base": "round 1 fragment /Users/billyribeiro/.fanout/frags/S-M2-a.round1.json (pin aeb512b6). Since aeb512b6, index.html, L04.html and the six lab twins are byte-identical. L01, L02, L03, L05, L06 and cards.json changed (diff read in full). Every row was re-verified in round 2 with fresh evidence; no row is carried from round 1.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS2-M2-a",
    "scratch": S,
    "verified_at": "2026-11-08",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice a = index.html, L01-L06 with their six lab twins, and the 82 cards of L01-L06. No project grader in this slice, so mutation testing does not apply (ruling: mutation is for project graders; lab twins are demonstrations) and mutants is empty. "
        "Three rows are FAIL: H04 (hub skill-check explanation contradicts project.html rung 2), L02-PROSE-02 (rhetorical question in an opener), L06-LAB-01 (lab docstring says it checks f(-1) and f(1) but the code only prints them). Six round-1 FAIL rows are fixed and re-verified: L01-PROSE-01, L01-CARD-02, L02-PROSE-01, L03-MATH-03, L03-PROSE-01, L04-CARD-01. "
        "Judgements recorded: (a) the 1000 threshold, f(-1)=2 and the lab-only values are graded C because their hand derivation sits in lab hypotheses or problem solutions, not in a numbered Example (ruling 13); (b) card basis wording differs from key-row wording in c025/c026/c035/c036/c046/c047/c056-c058/c069/c070 while the substance is the same, and this matches round 1; (c) M2-c048 is no longer a duplicate of M2-c044; (d) the placement skill check 1 is labelled the worked-example task of rung 1, but project rung 1 is a bond sensitivity by central difference, so the link is loose, not false; (e) M is a local letter used both as a limit (Proposition 2.2) and as an index (Proposition 3.1) in L01, which notation.json allows and is not a registry collision. "
        "Not checked: the Lab 1 figures of the project and the grader (other slices); live Crossref/Open Library record content beyond what verify_refs reports; the rendered page in light and dark mode at 360 px (page_smoke ran with --skip-sweep and these pages have no figures); spot-reading of Spivak or Hubbard (no locator is claimed, so none is needed). "
        "Repository state: scripts and outputs are under ledgers/M2/scripts/M2-a-r2/. A tracked file in that directory (recompute_r2.py, from an earlier round) was overwritten by mistake during this run, then restored from git (git checkout); my script is recompute_slice_a_r2.py. No course, test or reference file was edited."
    ),
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = (
    f"M2 slice a, round 2: verdict FAIL. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
    f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Non-PASS: H04 (index.html:135), L02-PROSE-02 (L02.html:51), L06-LAB-01 (L06.html lab docstring). "
    "All gates that can run on the slice pass (check_pages, check_dag, run_labs 27/27, twins under python -I -W error, pytest lab tests, page_smoke, ruff, mypy, verify_refs offline and live)."
)
problems = ledger.validate(fragment, "M2-a")
print("validation problems:", problems)
with open("ledgers/M2/M2-a.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows:", len(rows), counts)
