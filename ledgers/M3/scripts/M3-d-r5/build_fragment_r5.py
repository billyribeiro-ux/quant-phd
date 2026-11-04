"""Round-5 verifier: assemble ledgers/M3/M3-d.json (fragment) from the round-5 gate outputs and the row evidence below."""
import json
import re
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "ledgers/M3/scripts/M3-d-r5/out"
PIN = "440ed3c8216725d498d9c6d7c746907d4d418198"

C4 = "Carried from round 4 (course/modules/M/M3/L01.html..L06.html, tests/labs/M3 lab twins L01-L08 and the cards they cite byte-identical since the round-4 pin 4eb6788):"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# gates (fresh at 440ed3c)
row("gate-check-pages", "2.9-structure", "tools/check_pages.py --unit M3", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/check_pages_M3.out: 'check_pages M3: PASS', exit 0")
row("gate-check-dag", "2.9-dag", "tools/check_dag.py --unit M3", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/check_dag_M3.out: 'check_dag M3: PASS', exit 0")
row("gate-check-projects", "2.6-spec-structure", "tools/check_projects.py --unit M3", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/check_projects_M3.out: 'check_projects M3: PASS', exit 0")
row("gate-run-labs", "2.5-labs", "tools/run_labs.py --unit M3", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/run_labs_M3.out: 'run_labs M3: PASS (12/12)', exit 0")
row("gate-run-graders", "2.6-autograder-1", "tools/run_graders.py --unit M3 --seeds 0-49", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/run_graders_M3_0-49.out: 'run_graders M3: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0")
row("gate-page-smoke", "2.9-page-smoke", "tools/page_smoke.py --unit M3", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/page_smoke_M3.out: 'page_smoke modules/M/M3/project.html: PASS'; 'in-browser grader: All 163 tests pass on seed 2044752901'; lab-M3-project-1..3 run; exit 0")
row("gate-ruff", "gate", "ruff check and ruff format --check tests/labs/M3 course/modules/M/M3/grader", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/ruff_check.out: 'All checks passed!', '16 files already formatted', exit 0 for both")
row("gate-mypy", "gate", "mypy --no-incremental", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/mypy.out: 'Success: no issues found in 331 source files', exit 0")
row("gate-verify-refs", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. No live Crossref run.")
row("gate-collect-only", "2.6-test-count", "course/modules/M/M3/grader/test_project.py", "PASS",
    "pytest --co in scratch workspace /private/tmp/verifyD5-M3-d-ws (test_project.py, instance.py, reference.py as covariance_doctor.py): '163 tests collected'; project.html line 237 says 163")
row("gate-pytest-relevant", "gate", "tests/test_labs.py tests/test_memo_exemplars.py tests/test_page_checks.py -k M3", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/pytest_relevant.out: 12 passed, exit 0")
row("gate-mutate-m3", "2.6-mutation", "tools/mutate_graders.py --unit M3 --seeds 0-9 (ledgers/M3/mutants/, 150 files)", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/mutate_M3_seeds0-9_r5b.out: 'mutate_graders M3: PASS (150/150 killed)', exit 0. Earlier run mutate_M3_seeds0-9_r5.out exposed two surviving candidates, both now classified (see mutants-v5d-01-equivalent-moved and mutants-v5d-04-accepted-stop-rule).")
row("gate-reference-starter", "2.6-autograder-1", "course/modules/M/M3/grader/reference.py; starter.py", "PASS",
    "Scratch run: reference.py as covariance_doctor.py -> 163 passed; starter.py -> 162 failed, 1 passed (test_module_imports_only_standard_library_or_numpy; the other 162 raise NotImplementedError)")
row("gate-alternatives-seeds-0-49", "2.6-autograder-alternatives", "ledgers/M3/alternatives/alt1..alt9 (seeds 0-9 fresh; seeds 0-49 carried)", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/alts_seeds0-9.out: alt1..alt9 all PASS on seeds 0-9 (163 passed each). Seeds 0-49 carried from round 4 (alternatives/ byte-identical in the round-4..round-5 delta).")

# grader
row("grader-instance", "2.6-autograder-2", "course/modules/M/M3/grader/instance.py", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/instances_check_r5.out: seeds 0-199 checked for k in {3,4,5}, volatilities in [0.05,0.40], unit-diagonal symmetric corr with min eigenvalue < -0.02 (max over seeds -0.020514), psd_corr positive definite, eigenvectors orthonormal, psd_spectrum[0] = 0: problems 0")
row("grader-test-count-and-purity", "2.6-autograder-purity", "grader/test_project.py lines 793-830 (test_functions_print_nothing, test_inputs_are_not_mutated)", "PASS",
    "Read in full at 440ed3c. Killed by these tests in the r5b gate: vd3_01..03 (test_inputs_are_not_mutated), r16d_m02 (test_functions_print_nothing).")
row("grader-standard-library-only", "2.6-autograder-constraints", "grader/test_project.py lines 833-848; project.html line 235", "PASS",
    "test_module_imports_only_standard_library_or_numpy checks every import against sys.stdlib_module_names or numpy; killed vd3_04 in r5b. project.html line 235: 'The standard library and NumPy only.'")
row("grader-lab3-reference-numbers", "2.6-autograder-1", "grader/test_project.py lines 502-542; project.html lines 461-469", "PASS",
    "Test constants LAB3_CORR and LAB3_VOLS match project.html Lab 3 input; expected numbers -0.142113, 0.176573, 0.175003, 0.011516, 1.778929, -1.096718, -0.255613, 0.573402 match the Lab 3 expected block (run_labs and project_labs_check_r5.out). Killed by test_lab3_reference_numbers_are_matched in 29 of the 150 mutants (count of killer lines in mutate_M3_seeds0-9_r5b.out).")
row("grader-failure-messages-leak-answers", "2.6-autograder-messages", "grader/test_project.py lines 247-265, 328-329, 396-398, 409-410, 547-552, 582-584 and every assert/pytest.fail message", "PASS",
    "Round-4 leaks ('must be -2', 'must be -0.5', 'off-diagonal 1', 'the one-by-one repair of [[1]] is [[1]]', 'must have off-diagonal 1') are replaced by property messages (diff 4eb6788..440ed3c lines 247-410, 547-552). Scan of all assert and must_raise/pytest.fail messages for numbers: remaining numbers are the tests' inputs or tolerances, not expected outputs (e.g. 'a smallest eigenvalue of -0.9e-10' names the input). --assert=plain shows the message only.")
row("grader-named-conditions", "2.6-autograder-named-errors", "grader/test_project.py lines 158-229 (non-square, asymmetry), 751-783 (volatility, length)", "PASS",
    "ValueError is asserted only for the four conditions of project.html line 248 (non-square; asymmetry beyond 1e-9 with exact-tolerance accepted; volatility not > 0 incl. NaN; length mismatch). No assertion for any other input.")
row("grader-browser-timeout", "2.6-autograder-limit", "project.html line 235; course/assets/js/python.js line 4", "PASS",
    "project.html line 235: 'A run in your browser stops after 120 seconds'; python.js: TIMEOUT_MS = 120000. Measured browser run 1.1 s (page_smoke_M3.out).")
row("grader-reference-docstring", "2.6-autograder-reference", "course/modules/M/M3/grader/reference.py lines 1-5", "PASS",
    "Carried from round 4 (reference.py byte-identical since 4eb6788). Not shipped to learners; line 4 reads 'is Alternating projections' (capital A, article) - cosmetic, not learner-facing.")
row("grader-spec-rubric-counts", "2.6-spec-structure", "project.html lines 237, 489-499", "PASS",
    "project.html line 237 '163 tests' = collected 163; rubric table has five criteria (C1..C5) with four levels each (lines 491-497).")

# spec / mutants
row("spec-projection-tol-undefined", "2.6-spec", "project.html lines 233, 246; grader/starter.py lines 31-35", "PASS",
    "Round-4 defect resolved: project.html line 246 defines tol as the stopping tolerance ('An implementation may stop early, after a step whose gap and change are both at most tol'); line 233 refers to 'tol the stopping tolerance defined there'; starter docstring says the stopping rule is the student's choice.")
row("mutants-v3d-01-max-iter-plus-one", "2.6-mutation", "ledgers/M3/mutants/v3d_01_projection_repair_runs_one_extra_step.py", "PASS",
    "Killed in r5b by test_projection_repair_runs_exactly_max_iter_steps[1-seed] (test_project.py lines 585-618, tol=0 and 1..3 steps, reference iterate). Architect question resolved by the test; the convention fixes the step count when tol=0.")
row("mutants-v4d-01-clip-skips-rescale", "2.6-mutation", "ledgers/M3/mutants/v4d_01_clip_repair_skips_rescale_when_nearly_unit_diagonal.py", "PASS",
    "Killed in r5b by test_clip_repair_rescales_a_positive_definite_matrix_whose_diagonal_is_not_one (test_project.py lines 413-417; input [[1.0004,0.3],[0.3,1]]).")
row("mutants-existing-140", "2.6-mutation", "ledgers/M3/mutants/ (all pre-existing files)", "PASS",
    "All 146 pre-existing mutant files are KILLED in ledgers/M3/scripts/M3-d-r5/out/mutate_M3_seeds0-9_r5b.out (fresh run, not carried).")
row("mutants-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/v4d_02..v4d_04", "PASS",
    "All three KILLED in r5b (v4d_02 test_is_psd_sign_of_smallest_eigenvalue[negative]; v4d_03 and v4d_04 test_lab3_reference_numbers_are_matched).")
row("mutants-v2d-01-05", "2.6-mutation", "ledgers/M3/mutants/v2d_01..v2d_05", "PASS", "All KILLED in r5b.")
row("mutants-v2d-06", "2.6-mutation", "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py", "PASS",
    "Carried from round 4: file byte-identical; retired (not in the gate), its killer is the stdlib-only test.")
row("mutants-v3d-02-05", "2.6-mutation", "ledgers/M3/mutants/v3d_02..v3d_05", "PASS", "All KILLED in r5b.")
row("equivalent-r6d-m04", "2.6-accepted-alternative", "ledgers/M3/alternatives/alt7_dykstra_gap_only_stop.py", "PASS",
    "alts_seeds0-9.out: PASS on seeds 0-9 (163 passed each). Gap-only stop is an accepted stopping rule (project.html line 246: 'The stopping rule is an implementation choice').")
row("equivalent-r11d-m02", "2.6-accepted-alternative", "ledgers/M3/alternatives/alt8_dykstra_step_only_stop.py", "PASS",
    "alts_seeds0-9.out: PASS on seeds 0-9.")
row("equivalent-r15d-m03-label", "2.6-accepted-alternative", "ledgers/M3/alternatives/alt9_dykstra_runs_full_budget.py", "PASS",
    "alts_seeds0-9.out: PASS on seeds 0-9.")
row("equivalent-readme-citation", "2.6-accepted-alternative", "ledgers/M3/equivalent/ (absent at 440ed3c)", "PASS",
    "No ledgers/M3/equivalent/ directory exists at 440ed3c (ls ledgers/M3); its alternatives are in ledgers/M3/alternatives/ (alt7..alt9) and this round's accepted variants are under ledgers/M3/scripts/M3-d-r5/equivalent/.")

# project page
row("project-numbers", "1.prose-numbers", "course/modules/M/M3/project.html lines 57, 138, 143, 221, 460-470, 575-611", "PASS",
    "Lab 1/2/3 interpretive numbers equal the expected blocks (project_labs_check_r5.out). Arithmetic: 0.176573 - 0.175003 = 0.001570; weights 1.778929 - 1.096718 - 0.255613 + 0.573402 = 1.000000; det input = -0.261600 nonzero, (0.1*0.2*0.15*0.3)^2 det C invertibility; Exemplar A rounded weights 1.78, -1.10, -0.26, 0.57 sum to 0.99 as stated.")
row("project-lab1-memo-sentence", "2.5-labs", "course/modules/M/M3/project.html lines 53-57, 138", "PASS",
    "Carried from round 4 (lines 53-57 and 138 are outside every round-5 hunk of project.html); fresh: project_labs_check_r5.out lab 1 stdout equals expected block, step 3 prints False, step 6 prints True.")
row("project-lab2-completion", "2.5-labs", "course/modules/M/M3/project.html lines 141-222; tests/labs/M3/lab-M3-project-2.py", "PASS",
    "project_labs_check_r5.out: twin stdout equals expected block; page code differs from the twin only at the two ___ blanks (diff lines 193 and 201), as designed.")
row("project-lab3-check", "2.5-labs", "course/modules/M/M3/project.html lines 287-470; tests/labs/M3/lab-M3-project-3.py", "PASS",
    "project_labs_check_r5.out: twin stdout equals expected block; page code equals twin; expected numbers match the grader's Lab 3 checks.")
row("project-lab3-diagonal-positivity-sentence", "1.prose-claim", "course/modules/M/M3/project.html line 470 (also lines 598, 610)", "PASS",
    "Re-derived. Lab 3 clip_repair divides by math.sqrt(d[i]*d[j]) for every pair (Lab 3 source, clip_repair). math.sqrt of a negative raises ValueError and a zero product gives ZeroDivisionError, so a completed run implies d[i]*d[j] > 0 for all i, j; hence every d[i] is nonzero and the signs agree. A1 gives d[i] >= 0 (take z = e_i), so d[i] > 0, which is A2's hypothesis. Lab 3 prints no clipped diagonal (project.html lines 461-469), so the page says so.")
row("project-spec-grader", "2.6-spec", "course/modules/M/M3/project.html lines 230-237", "PASS",
    "Read. Instance description matches grader/instance.py (see grader-instance); test count 163; in-browser run stated as 120 s limit (grader-browser-timeout).")
row("project-conventions-math", "1.prose-numbers", "course/modules/M/M3/project.html lines 242-249", "PASS",
    "Alternating-step convention (line 246) matches grader/reference.py lines 109-128 step by step (J=P(X+E), E=X+E-J, N=J+H with diagonal 1, H=J+H-N, X=N, gap=||N-J||, change=||N-X_prev||). Equivalence check ledgers/M3/scripts/M3-d-r5/out/equiv_check_r5.out: 360 cases, max difference 0.0 between reference and a variant without H. Weights formula and the 1e-9/1e-8 PSD tolerances match the tests.")
row("project-conventions-link", "2.4-dag", "course/modules/M/M3/project.html line 243 (concept link positive-semidefinite-matrix to L05.html#def-positive-semidefinite-matrix)", "PASS",
    "check_dag M3 PASS and check_pages M3 PASS (r5 out); the anchor resolves.")
row("project-proof-A1", "3.proof", "course/modules/M/M3/project.html lines 482, 636", "PASS",
    "Re-derived: X = V Lambda_f V^T symmetric; z^T X z = sum max(lambda_i,f)(V^T z)_i^2 >= 0 since max >= f >= 0. Hypotheses named (real symmetric A, f >= 0, F1-F4 for the spectral theorem).")
row("project-proof-A2", "3.proof", "course/modules/M/M3/project.html lines 482, 637", "PASS",
    "Re-derived: Y_ii = X_ii/(sqrt(d_i))^2 = 1; z^T Y z = q^T X q with q = D^{-1/2} z >= 0; positivity of d_i stated as needed for the division.")
row("project-proof-A3", "3.proof", "course/modules/M/M3/project.html lines 482, 638", "PASS",
    "Re-derived: det Sigma = a^2 b^2 (1 - rho^2) > 0; Sigma^{-1} iota = (b(b-rho a), a(a-rho b))/det; normaliser a^2+b^2-2rho ab = (a-b)^2 + 2ab(1-rho) > 0; scaling by c>0 multiplies numerator and normaliser by c^2. The grader test_weights_two_asset_closed_form checks the same formula numerically.")
row("project-proof-A4", "3.proof", "course/modules/M/M3/project.html lines 482, 638", "PASS",
    "Re-derived: X u_i = V Lambda_0 e_i = 0 (lambda_i < 0), so X singular; with Y = D^{-1/2} X D^{-1/2}, z = D^{1/2} u_i gives Y z = 0; with Sigma = S Y S, S^{-1} z gives Sigma S^{-1} z = 0. Hypotheses named: F1-F4, diagonal positive.")
row("project-hours", "1.arithmetic", "course/modules/M/M3/project.html lines 252-268; course/modules/M/M3/index.html line 29; lesson data-hours attributes", "PASS",
    "Project table 2+3+14+8+12+6 = 45 (project.html line 33 and line 265). Lesson data-hours: L01 12, L02 11, L03 12, L04 12, L05 12, L06 11, L07 11, L08 12, L09 12 = 105. Hub index.html data-hours-lessons 105, data-hours-project 45, total 150. Design-target ruling: arithmetic only.")
row("project-exemplars", "3.rubric-calibration", "course/modules/M/M3/project.html lines 502-647", "PASS",
    "Each annotation read against the rubric text (lines 491-497). Exemplar A (official 2,2,2,1,2) and B (4,4,4,3,3) are consistent with the descriptors; B's C4 and C5 level-4 misses name the absent elements. Scored by this verifier from the rubric text, not blind to the official scoring.")
row("project-rubric", "3.rubric", "course/modules/M/M3/project.html lines 486-500", "PASS",
    "Five criteria, four levels, all observable. C4 level-2 descriptor changed (see rubric-C4-level2-vague).")
row("rubric-C4-level2-vague", "3.rubric", "course/modules/M/M3/project.html line 496 (criterion C4, level 2 cell)", "PASS",
    "Round-4 FAIL resolved: level 2 now reads 'Labels some inputs, or states a conclusion about a portfolio or a market from a printed result.' Both clauses are observable in a report. Exemplar A (no labels, recommendation 'Use the projection') still scores C4 = 1.")
row("project-references", "2.1-citations", "course/modules/M/M3/project.html lines 665-677", "PASS",
    "Carried from round 4 (lines 665-677 outside every round-5 hunk; references/ and curriculum unchanged in the delta); verify_refs offline PASS.")
row("project-no-process-words", "4.process-words", "course/modules/M/M3/project.html; cards.json; grader/*.py", "PASS",
    "grep -i for round, verif, fixer, builder, architect, ruling, revised, corrected, updated: no matches.")
row("project-stretch", "3.prose", "course/modules/M/M3/project.html lines 656-663", "PASS",
    "Read. Learner tasks only; no claimed result. Carried wording unchanged in this delta.")

row("scope-repair-weights-vs-brief", "3.scope", "curriculum/01-foundations.yaml lines 185-188 (brief); course/modules/M/M3/project.html lines 469-470 (Lab 3 interpretation), 479 (brief section 4), 493 (rubric C2 level 3), 610 (exemplar B)", "FAIL",
    "The curriculum brief asks to 'Compare the effect of each repair on downstream portfolio weights.' project.html reports the weights of the input only (lines 457, 469) and states that the repairs' weights are not reported (lines 470, 493, 610). The architect's B3 decision (plans/M3-build-plan.md lines 369-371 and 454; plans/M3-open-items.md line 32) chose closed-form weights, but no ruling removes the brief's repair-comparison requirement. Round 5 left the scope unchanged.",
    "Architect ruling required: either a curriculum change request that narrows brief line 185-188 to the input's closed-form weights (the verifier may not edit curriculum/), or the page must report each repair's weights where Sigma is invertible and state the singular case. No builder change alone resolves it.")
row("notation-registry", "1.notation", "course/modules/M/M3/project.html; notation/notation.json", "PASS",
    "Registered program-wide symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) and macros are not reused on the page. Local symbols (Sigma, S, N, E, H, J, X, Y, P(M), iota) are defined at first use (iota defined at project.html line 247). No \\mathbb in the page.")
row("notation-R-macro", "1.notation", "course/modules/M/M3/project.html; L07-L09.html; cards.json", "PASS",
    "grep mathbb: 0 matches in these files.")
row("dag-linked-concepts", "2.4-dag", "course/modules/M/M3/project.html concept links (eigendecomposition L03, spectral-theorem L04, positive-semidefinite-matrix L05)", "PASS",
    "check_dag M3 PASS (r5 out).")
row("dag-m4-concepts-by-name", "2.4-dag", "course/modules/M/M3/project.html; cards.json", "PASS",
    "grep for cholesky, ieee, 754, markowitz, minimum-variance, mean-variance, quadratic programming: no matches. 'portfolio' appears only as plain prose (project.html lines 47, 496, 623), covered by architect ruling 3.")

# cards
row("cards-structure", "3.cards", "course/modules/M/M3/cards.json (203 cards)", "PASS",
    "203 cards, unique ids, unique fronts and backs; keys id, lesson, front, back, and optional grade/basis; check_pages M3 PASS.")
row("cards-id-sequence", "3.cards", "course/modules/M/M3/cards.json ids", "PASS",
    "Unique ids. Gaps (c102, c148, c191) and the out-of-order appended M3-c207 are permitted by FINAL-ARCHITECT-RULINGS item 2.")
row("cards-numbers-cited", "3.cards", "course/modules/M/M3/cards.json; lesson text re-extracted at 440ed3c (ledgers/M3/scripts/M3-d-r5/out/text)", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/card_numbers_r5.out: numbers checked 267, misses 0.")
row("cards-labels-cited", "3.cards", "course/modules/M/M3/cards.json; lesson text at 440ed3c", "PASS",
    "ledgers/M3/scripts/M3-d-r5/out/card_labels_r5.out: 198 labels; the two cross-lesson labels name their lesson in the card (M3-c054 'Lesson 1, Proposition 3.12'; M3-c090 'Lesson 4, Theorem 2.3').")
row("cards-duplicate-scan", "3.cards", "course/modules/M/M3/cards.json M3-c101 and M3-c204", "FAIL",
    "Round-4 duplicate M3-c206 is removed, but M3-c101 ('What is an orthogonal matrix?', L06 Definition 1.1) and M3-c204 ('which two identities make a real n x n matrix Q orthogonal?', L09 Definition 1.2a) test the same definition of the same term. The term is defined twice in the unit (L06.html line 59; L09.html line 69).",
    "Delete M3-c204 (its two-sided identity content is covered by M3-c101 with M3-c205) or rewrite it to test a fact that M3-c101 does not. Separately, L09.html Definition 1.2a duplicates L06.html Definition 1.1 (lesson-level, outside this slice).")
row("cards-sample-10", "3.cards", "course/modules/M/M3/cards.json (all 203 cards read)", "PASS",
    "Every card was read at 440ed3c (not only every tenth). Each card that changed was checked against its lesson text (see cards-L05, cards-L08, cards-L09 rows).")
row("cards-lab-numbers", "3.cards", "cards.json grade-C cards (39); tests/labs/M3 twins", "PASS",
    "Fresh: L05 cards (M3-c094..c097, c173, c176, c179) against ledgers/M3/scripts/M3-d-r5/out/lab_L05_1_r5.out; L09 cards (M3-c161..c164, c167, c175) against lab_L09_1_r5.out and l09_numbers_r5.out. L01-L04, L06-L08 labs and their cards byte-identical since the round-4 pin (carried).")
row("cards-L01", "3.cards", "cards.json L01 cards (24)", "PASS",
    "Carried from round 4 (L01.html and tests/labs/M3/lab-M3-L01-1.py byte-identical; all L01 cards byte-identical since round 4).")
row("cards-L02", "3.cards", "cards.json L02 cards (22)", "PASS",
    "Carried from round 4 (L02.html and its lab byte-identical; L02 cards byte-identical).")
row("cards-L03", "3.cards", "cards.json L03 cards (23)", "PASS",
    "Carried from round 4 (L03.html and its lab byte-identical; L03 cards byte-identical).")
row("cards-L04", "3.cards", "cards.json L04 cards (19 after removal of M3-c206)", "PASS",
    "Carried from round 4 for the 19 remaining L04 cards (byte-identical). The removed M3-c206 was the duplicate of M3-c101 (see cards-duplicate-scan for the remaining duplicate).")
row("cards-L05", "3.cards", "cards.json M3-c100 and the L05 cards", "PASS",
    "Round-4 FAIL was M3-c100 stating a lab result without a basis. The new back ('...Definition 3.1 uses a tolerance for that reason.') states no lab result. Verified against L05 Definition 3.1 (tolerance test) and Remark 3.2 (G has eigenvalue 0). Lab outputs in lab_L05_1_r5.out support the remaining L05 grade-C cards.")
row("cards-L06", "3.cards", "cards.json L06 cards (15)", "PASS",
    "Carried from round 4 (L06.html and its lab byte-identical; L06 cards byte-identical). M3-c101 is covered by cards-duplicate-scan.")
row("cards-L07", "3.cards", "cards.json L07 cards (20); course/modules/M/M3/L07.html", "PASS",
    "Carried from round 4 for the cards: none cites the only changed L07 text (research problem R1, L07.html line 318, which no card cites). Cited L07 results (Theorem 1.2, Remark 1.4, Theorem 2.2) unchanged.")
row("cards-L08", "3.cards", "cards.json M3-c142, M3-c207, M3-c145, M3-c200; L08.html lines 136-141, 292, 507-511", "PASS",
    "M3-c142 (match rule with the tie clause) matches L08 Definition 3.1 as now written (L08.html line 141). M3-c207 (labels and shapes) matches L08 lines 136-141. Shape wording 'centred squared tenors, orthogonalized against the first two' is L08 line 137. M3-c145 and M3-c200 unchanged and their lesson text unchanged in the cited parts.")
row("cards-L09", "3.cards", "cards.json M3-c162, c163, c164, c175; tests/labs/M3/lab-M3-L09-1.py", "PASS",
    "Round-4 FAIL resolved: the four cards now use 'smallest eigenvalue below -1e-9', matching the lab's NONPSD_TOL and the printed count. Fresh run: lab_L09_1_r5.out: 23 of 40 not PSD; 23 of 23 pass is_correlation; 23 of 23 closer than R; index 0 distances 0.175527 (R) and 0.163280 (W). Independent numpy recomputation l09_numbers_r5.out agrees.")
row("cards-L01-L09-changed-in-round3", "3.cards", "cards.json M3-c101, c127, c142, c168, c178, c202, c205 (c206 removed)", "PASS",
    "All re-read at 440ed3c; c142 re-checked; c206 removed; c101 duplicate recorded under cards-duplicate-scan.")
row("cards-c131", "3.cards", "cards.json M3-c131; L08.html Proposition 1.1", "PASS", "Carried from round 4 (card and cited text byte-identical).")
row("cards-c204", "3.cards", "cards.json M3-c204; L09.html Definition 1.2a (line 69-70)", "PASS",
    "Card content is exact: Q^T Q = I and Q Q^T = I (Definition 1.2a). Its duplication with M3-c101 is recorded under cards-duplicate-scan, not as an accuracy error.")

# new rows this round
row("mutants-v5d-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/v5d_02, v5d_03, v5d_05, v5d_06 (generator ledgers/M3/scripts/M3-d-r5/make_mutants_r5.py)", "PASS",
    "All four KILLED in r5b: v5d_02 (PSD correction starts at the input) by test_projection_repair_is_no_farther_than_clipping; v5d_03 (unit-diagonal projection first) by test_projection_repair_has_unit_diagonal_after_one_iteration; v5d_05 (PSD correction dropped) by test_lab3_reference_numbers_are_matched; v5d_06 (final rescaled PSD iterate returned) by test_projection_repair_runs_exactly_max_iter_steps[1-seed].")
row("mutants-v5d-01-equivalent-moved", "2.6-mutation-equivalence", "ledgers/M3/scripts/M3-d-r5/equivalent/alt10_equivalent_no_unit_diagonal_correction.py (was v5d_01)", "PASS",
    "Not a grader gap: dropping the unit-diagonal correction H leaves the output unchanged. Off-diagonal entries of H are zero by induction (H_k = J_k + H_{k-1} - N_k, and N_k has the off-diagonal entries of J_k + H_{k-1}), and the diagonal of N_k is reset to 1. equiv_check_r5.out: 360 cases, max difference 0.0. alt10 passes seeds 0-9.")
row("mutants-v5d-04-accepted-stop-rule", "2.6-mutation-equivalence", "ledgers/M3/scripts/M3-d-r5/equivalent/alt11_stop_when_either_gap_or_change.py (was v5d_04)", "PASS",
    "Survives because project.html line 246 says 'The stopping rule is an implementation choice', and the suite is built to accept stopping rules (alt7 gap-only and alt8 step-only pass). alt11 passes seeds 0-9. Ambiguity noted: the sentence before it reads 'may stop early, after a step whose gap and change are both at most tol'; the page should say which reading is meant.")


def mutant_entries():
    text = (OUT / "mutate_M3_seeds0-9_r5b.out").read_text(encoding="utf-8")
    entries = []
    for line in text.splitlines():
        m = re.match(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*) \(seed (\d+)\)$", line)
        if not m:
            continue
        status, name, desc, killer, seed = m.groups()
        entries.append({"id": name, "description": desc, "killed_by": f"{killer} (seed {seed})" if status == "KILLED" else None})
    return entries


mutants = mutant_entries()
killed = sum(1 for m in mutants if m["killed_by"])
frag = {
    "unit": "M3",
    "slice": "d",
    "round": 5,
    "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, round 5; shares no context with the builders",
    "pin": f"{PIN} (440ed3c)",
    "base": "round-4 pin 4eb6788 (ledger /Users/billyribeiro/.fanout/frags/D-M3-d.round4.json, read as context; its PASS rows re-verified or carried by byte-identity)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-M3-d",
    "scratch": "ledgers/M3/scripts/M3-d-r5/ (scripts and out/)",
    "verified_at": "2026-11-03T20:30:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta 4eb6788..440ed3c read for slice d: project.html hunks (lines 230-237, 243-249, 466-470, 493-495, 597-611), grader/test_project.py (+54/-8 lines: new tests, reworded messages), starter.py docstring, cards.json (c100, c142, c162-c164, c175 changed; c206 removed; c207 added), L07/L08/L09 hunks (cards depend on L08 Def 3.1 and L09 text), tests/labs/M3/lab-M3-L09-1.py (docstring only, output unchanged), ledgers/M3 (mutants v4d/v5d, alternatives alt7-9 unchanged). "
        "Scripts: M3-d-r5/*.py; outputs in M3-d-r5/out/. Mutant gate: 150 files in ledgers/M3/mutants, 150 killed, exit 0. Round-5 new mutants written: v5d_02, v5d_03, v5d_05, v5d_06 (killed). v5d_01 and v5d_04 were moved to M3-d-r5/equivalent/ as accepted variants (not grader gaps; see rows). "
        "Not checked: (1) the 146 pre-existing mutant files were not read line by line; each was checked by the gate and the killer test. (2) Live Crossref (verify_refs online) not run. (3) Browser run timing only measured as 1.1 s by page_smoke; the 120 s limit is taken from python.js and project.html. (4) Lesson pages outside the slice (L01-L09) were read only where cards or project.html cite them. (5) Card sentences were checked against lesson text by claim, not word by word, for the cards that did not change (carried by byte-identity). (6) The convergence of the alternating-projection iteration to the Frobenius-nearest matrix is not proved here; the page does not claim it (it says approximation). (7) Hours checked for arithmetic only (design-target ruling). (8) Exemplars scored by this verifier from the rubric text, not blind to the official scoring."
    ),
    "summary": (
        f"M3 slice d round 5 on pin 440ed3c: verdict FAIL. Rows: {len(rows)}; PASS {sum(1 for r in rows if r['status']=='PASS')}; FAIL {sum(1 for r in rows if r['status']=='FAIL')}; UNVERIFIABLE 0. "
        f"Mutants killed {killed}/{len(mutants)}. Non-PASS rows: scope-repair-weights-vs-brief (architect ruling needed; curriculum brief lines 185-188 conflict with the page's repair-weights scope) and cards-duplicate-scan (M3-c101 vs M3-c204, same definition of orthogonal matrix). "
        "Round-4 FAIL rows resolved on fresh evidence: gate-mutate-m3, mutants-v3d-01, mutants-v4d-01, grader-failure-messages-leak-answers, spec-projection-tol-undefined, rubric-C4-level2-vague, project-lab3-diagonal-positivity-sentence, cards-L05, cards-L09."
    ),
}
Path(ROOT / "ledgers/M3/M3-d.json").write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "killed", killed)
