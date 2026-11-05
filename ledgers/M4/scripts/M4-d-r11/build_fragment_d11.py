"""Round-11 verifier d: write ledgers/M4/M4-d.json (round 11). Row ids and checks are kept from the round-10 fragment
(/Users/billyribeiro/.fanout/frags/D-M4-d.round10.json); each row's evidence names the script or gate output that backs it
(paths under ledgers/M4/scripts/M4-d-r11/). Mutants are parsed from gates/mutate_M4_0-9_final.out."""

import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/M4/scripts/M4-d-r11"
PREV = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-M4-d.round10.json").read_text(encoding="utf-8"))
prev = {r["id"]: r for r in PREV["rows"]}

CARRY = "Carried from round 10 (byte-identical since the round-10 pin 47a36d8c): "
FRESH = "Re-verified in round 11: "
PASS = "PASS"

# id -> (status, evidence) ; check and location come from the round-10 row
E: dict[str, tuple[str, str]] = {
    "d1-2.6-hours": (PASS, FRESH + "project.html:33 data-hours-project=30 and the table#hours rows (lines 234-245) re-read: 2+2+12+8+4+2 = 30, equal to the hub figure. My own estimate of each component (verifier judgment, not measured): rung 1 about 2 h, rung 2 about 1.5 h, simulator with 25 validation conditions, the Cholesky factor, both streams and the quantile about 10 h, proof appendix A1-A4 about 6.5 h, report with run_report.py and self-assessment about 4 h, self-check about 2 h; total 26 h, 13% below 30 (the 30% band is 21 to 39 h)."),
    "d1-2.6-instances": (PASS, FRESH + f"{S}/instances_d11.py -> gates/instances_d11.out: 40 seeds (0-19 and 20 others) all valid (n in {{2,3}}, positions whole cents 100000..5000000, cov symmetric and Cholesky-positive, nu in 3..8, draws in the fixed set and not a multiple of 100); 38 distinct (positions, nu, draws) tuples; 38 distinct 99% losses from the reference (2000 draws, seed 2026)."),
    "d1-2.6-starter": (PASS, FRESH + f"{S}/gates/starter_m17_signprobe_d11.out: harness on grader/starter.py seeds 0 and 1: exit 1, '154 failed, 1 passed, 1 skipped' (the suite fails on the starter). Starter signatures (starter.py:15-34) read and equal project.html's three signatures."),
    "d1-rubric-observable": (PASS, FRESH + "project.html:330-343 (table#rubric) read in full: every descriptor names an element a reader can check (a formula, a printed number, a named element, a unit, a word count); the scoring rule at project.html:328 defines each level from the level below."),
    "d1-rubric-calibration": (PASS, FRESH + "Blind scoring from the rubric (project.html:330-343) before the annotations were compared: Exemplar A C1 2, C2 2, C3 2, C4 2, C5 2 (official 2,2,2,2,2); Exemplar B C1 4, C2 4, C3 4, C4 4, C5 3 (official 4,4,4,4,3). Every score matches. Exemplar word counts: " + f"{S}/checks/exemplar_words_d11.out (A body 90 words, 100 with headings; B Summary 70 words; limits 80 and 300-700 met)."),
    "d1-rubric-question-bank": (PASS, FRESH + "project.html grading mode (line 206) is autograder plus rubric and the page is not an adversarial review (no IC defence, debate or referee report), so BUILDER_RULES §5.4(4) does not apply; no question bank required."),
    "d1-atlas": (PASS, CARRY + "curriculum/meta.yaml:194-276 and index.html:37 (no Atlas milestone for M4); git diff 47a36d8c HEAD shows no change to curriculum/meta.yaml."),
    "d1-studio": (PASS, CARRY + "curriculum/01-foundations.yaml:73-76 (no studio change); the M4 entry (lines 186-200) re-read this round and matches the project scope (lines 218-229 in spirit: simulate Gaussian and Student-t losses with matched covariance, 99% loss, prove the moment conditions)."),
    "d1-cites": (PASS, FRESH + f"{S}/gates/verify_refs_offline_d11.out: 'offline integrity: 560 entries, 0 problems'. project.html:482-486 reads the reading list (blitzstein2019introduction) and states no attribution or locator; the key is in references/references.json."),
    "d1-cards-c191-grade": (PASS, FRESH + "cards.json M4-c191 (read this round): grade T; back states the covariance [[S1^2, rho S1 S2], [rho S1 S2, S2^2]] (checked by hand against X1 = S1 Z1, X2 = S2(rho Z1 + sqrt(1-rho^2) Z2)) and the hypotheses of L05 Example 2.5 with 'not proved here'."),
    "d1-data": (PASS, FRESH + "project.html:37, 200, 271-275 read: no data file is read, every input is SIMULATED; grader/instance.py:1-14 and 42 read: label 'SIMULATED', no file access."),
    "d1-tools-structure": (PASS, CARRY + "tools/*.py: git diff 47a36d8c HEAD -- tools is empty; all tools were run this round (check_pages, check_dag, check_projects, run_labs, run_graders, mutate_graders, page_smoke, verify_refs), see the d11-gate rows."),
    "d6-2.6-equivalence-float-ceil": (PASS, FRESH + f"{S}/checks/float_ceil_d11.py -> checks/float_ceil_d11.out: 'n in 1..2000000 where float ceiling differs from exact index: none'. The page's float-free index (project.html:214, reference.py:99) is therefore equivalent on every list length the page can reach; no float-index mutant is listed."),
    "d6-prose-exemplar-words": (PASS, FRESH + f"{S}/checks/exemplar_words_d11.out: Exemplar A memo text 100 words with headings (10 in headings), body 90, matching the annotation at project.html:359; Exemplar B Summary 70 words, matching 'Summary of 80 words or fewer' at project.html:411."),
    "d6-cards-sample": (PASS, FRESH + "cards.json read in full this round (227 cards); the 14 sampled cards c001, c011, c030, c040, c063, c074, c098, c105, c120, c133, c141, c149, c157, c162 checked against the block index of their lessons (" + f"{S}/checks/L01.txt ... L10.txt" + ") and the lab outputs in " + f"{S}/checks/lab_outputs/."),
    "d1-2.6-ladder": (PASS, FRESH + "project.html:40-49 (ladder) and 51-192 (rungs 1 and 2) re-read in full. Rung 1: numbered comments, printed output and an interpretation; rung 2: completion lab with expected block; rung 3 scope matches curriculum/01-foundations.yaml:218-229 (simulate Gaussian and Student-t losses with matched covariance, 99% loss, prove the moment conditions); rung 4 (project.html:471-478) is open-ended."),
    "d1-2.6-spec-questions": (PASS, FRESH + "project.html:194-229 re-read in full. Questions a competent student would still have to ask: none that the page leaves open. The Student-t draw order and source are stated as open and not graded (Conventions item 5; the suite fixes only the Gaussian order); the sign convention is in Conventions item 2 and Conditions; the quantile index is in Conventions item 4; the cent rule is in Conventions item 2; 'symmetric' is exact equality (test_project.py:464-472, the mathematical definition)."),
    "d1-2.6-autograder-reference": (PASS, FRESH + f"{S}/gates/run_graders_M4_0-49.out: 'run_graders M4: PASS (reference 50/50 seeds, slowest 0.9 s)', exit 0 (tools/run_graders.py --unit M4 --seeds 0-49)."),
    "d1-2.6-mut-own": (PASS, FRESH + f"Four new student-error mutants written this round: ledgers/M4/mutants/d11_01_short_positions_rejected_as_invalid.py, d11_02_gaussian_normals_drawn_position_major.py, d11_03_gaussian_normals_from_inverse_cdf_of_random.py, d11_04_quantile_index_from_n_minus_one.py (generated by {S}/make_d11.py). Each is killed on all 10 seeds 0-9 (gates/new_mutants_d11_fail_counts.out: exit 1 on every seed; gates/mutate_M4_0-9_final.out: KILLED lines, test names in the mutants list)."),
    "d1-2.6-mut-existing": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'mutate_graders M4: PASS (159/159 killed)', exit 0, run after the four new mutants were added (the earlier run, gates/mutate_M4_0-9.out, had 155/155)."),
    "d1-2.6-mut-m11": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'KILLED m11_loss_sign_flipped.py ... -> test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return (seed 0)'."),
    "d1-2.6-mut-r9_03": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'KILLED r9_03_student_t_chi_square_reused_every_second_draw.py' (killed on seed 0 by test_student_t_draws_do_not_share_chi_square)."),
    "d1-2.6-mut-v4_m02": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'KILLED v4_m02_matched_factor_skipped_for_small_nu.py'."),
    "d1-2.6-mut-m17": (PASS, CARRY + "ledgers/M4/equivalent/m17_student_t_second_seed.py. Round 11 re-check: the candidate passes the full suite on seeds 0, 1 and 2 (" + f"{S}/gates/starter_m17_signprobe_d11.out" + "): it is a conforming Student-t stream (the page leaves the Student-t source open, Conventions item 5), so it is kept out of the mutants list, as a conforming alternative and not a fault."),
    "d1-2.6-alternatives": (PASS, FRESH + f"{S}/gates/alts_d11_seeds0-9.out: reference 10/10; 16 correct alternatives 10/10 each: alt_d11_1 (Student-t chi-square before normals), alt_d11_2 (chi-square from a second generator), alt_d11_3 (heapq selection, Fraction index, 1 - 2/nu, isfinite pivot test), alt_d10_1, alt_d10_2, alt_r10_a, alt_r9_1..3, alt1..alt6 (all run through the same harness)."),
    "d1-2.6-messages": (PASS, FRESH + "every check() and expect_value_error() message in grader/test_project.py (lines 1-696) read this round. Each names the violated property and gives a hint at the concept; none prints a computed value. The two test names that carry the wrong magnitude (1e16 for 1e-16) are recorded under d11-test-names-1e16, not here."),
    "d1-2.6-count-and-pyodide": (PASS, FRESH + f"{S}/gates/reference_seeds_0-9.out: 156 passed (seeds 3-6, 8), 155 passed and 1 skipped where nu is 3 or 4 (seeds 0-2, 7, 9). {S}/gates/page_smoke_project_d11.out: 'in-browser grader: All 155 tests pass on seed 317153361'; local run of the same seed (gates/reference_pyodide_seed_local.out) gives 155 passed, 1 skipped. project.html:206 states 156 checks with one skipped at nu 3 or 4: consistent."),
    "d1-2.6-grader-comment-numbers": (PASS, FRESH + f"{S}/gates/variance_d11.out (seeds 0-1999): reference error 1.0220 at seed 1093 (nu 3); reference maxima 0.1259 (nu 5), 0.0967 (nu 6), 0.0728 (nu 7), 0.0624 (nu 8); missing-factor seeds over 0.30: 347/347, 317/317, 342/343, 288/317 (test_project.py:31-39). {S}/gates/cross_mutants_d11.out: reference cross-term max 0.0239 over seeds 0-49; r8_03 0.0677-0.0860; r9_02 0.1406-0.1605 (test_project.py:43-47)."),
    "d1-prose-numbers": (PASS, FRESH + f"project.html:228 now reads '+3 % ... none of the 50 seeds, -3 % on one (seed 38), +5 % on 19, -5 % on 30 (seeds 0 to 49)'. {S}/gates/cross_d11.out (100,000 draws, nu 5, factor entry scaled by 1+eps): eps +0.03 failing 0/50; eps -0.03 failing 1/50 [38]; eps +0.05 failing 19/50; eps -0.05 failing 30/50. All four counts match the page. The other numbers in the same group re-checked: {S}/gates/chi_probes_d11.out (lag-1 50/50, lag-2 50/50, lag-3 39/50, even-indexed 44/50, chain at lag 4 38/50, disjoint lag-4 pairs 0/50) and project.html:215 chain 38 of 50."),
    "d1-prose-scope": (PASS, FRESH + "project.html:215 and 228 re-read: 'all 50 seeds', 'none', 'every' and 'only' are each a count from " + f"{S}/gates/cross_d11.out or {S}/gates/chi_probes_d11.out, or a formula (fourth moment infinite at nu 3 and 4, Appendix A3). The sentence at project.html:215 now names the family ('For the Student-t family at nu = 3 only')."),
    "d1-prose-process-words": (PASS, FRESH + "grep (case-insensitive) over project.html, L01-L10.html and cards.json for 'verifier', 'round N', 'builder', 'agent': 0 hits in each file (ledgers/M4/scripts/M4-d-r11/checks/banned_and_process_words_d11.out: 0 matches)."),
    "d1-prose-banned-phrases": (PASS, FRESH + "BUILDER_RULES §1.3-1.4 phrases ('TODO', 'TBD', 'lorem', 'for brevity', 'left as an exercise', 'important to note', 'obviously', 'clearly', 'well known', 'studies show', 'experts agree', 'you can add', 'beyond the scope', 'details omitted'): 0 hits in project.html, cards.json and L01-L10.html. check_pages M4 PASS (" + f"{S}/gates/check_pages_M4.out)."),
    "d1-dag": (PASS, FRESH + f"{S}/gates/check_dag_M4.out: 'check_dag M4: PASS'. plans/M4-build-plan.md 'Architect decisions' Q2-Q3 (no M3 prerequisite; moment, chi-square, Cauchy, determinant and order statistic are plain prose): project.html uses 'order statistic' and 'chi-square' in prose only; the Gamma function and 'positive definite' are defined inline (Conventions item 1, Assumption 1)."),
    "d1-notation": (PASS, FRESH + "notation/notation.json read (macros and symbols T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q-blackboard). M4 pages use \\Phi as the standard normal CDF (registered meaning), gamma_3 and gamma_4 as E[Z^3], E[Z^4] (registered meaning, not excess), \\E, \\Var, \\Cov, \\R (registered macros); T is not used as a symbol; R (return), W, Z, L, V, C, F, Q and w are local and unregistered (no collision)."),
    "d1-structure": (PASS, FRESH + f"{S}/gates/check_pages_M4.out PASS and {S}/gates/check_projects_M4.out PASS for project.html: ladder rungs 1-4 in order, spec, autograder, rubric, exemplars, self-assessment, stretch, reading list, in BUILDER_RULES §5 order."),
    "d1-cards-schema": (PASS, FRESH + "cards.json: 227 objects, unique ids (M4-c001 to M4-c244, gaps where cards were removed: c014, c046, c066, c124 and others), keys {id, lesson, front, back, grade} plus basis on 34 cards (all 25 C cards and 9 T cards), grades only T (202) and C (25), every lesson L01-L10 present; ids run M4-c001 to M4-c244 with 17 unused numbers (c014, c046, c066, c123, c124, c156, c163, c164, c184, c196, c202, c203, c206, c211, c213, c219, c220), left by removed or renumbered cards."),
    "d1-cards-numbers-in-lesson": (PASS, FRESH + f"{S}/checks/card_numbers_in_lesson_d11.py -> checks/card_numbers_in_lesson_d11.out: 'numbers not found: 0' (every decimal or multi-digit number on a card occurs in its lesson, or for a basis card in that lesson's lab output)."),
    "d1-cards-labs": (PASS, FRESH + f"Every lab-backed card compared with the output of its lesson twin run alone under python -I -W error ({S}/gates/lesson_twins_python_I.out: all 10 exit 0, empty stderr; outputs in {S}/checks/lab_outputs/): c030 3.469; c033 489 (the count of losses > 0, 250000 cents each, expected 500); c047 2.065 and 2.073; c082 0.00002223; c083 0.592936 and -0.007064; c098 1.669114 and 0.001469; c112 7.11e-13 at t = 2 and 244.69193226; c113 -0.062124 and -0.062110; c126 0.0187 (off-diagonal); c143 0.8552, c167 0.8548, c238 0.8518 (SE 0.0056, 4000 replications, seed 2026); c162 1.8220 and c237 1.8838 (400 replications); c166 3.4689; c169 +0.9919 (seed 2028); c170 1.0211; c171 0.8807; c183 5.580 vs 5.625; c188 (0.9770, -2.0055); c189 +0.0031 (seed 2026); c190 -0.0235 (seed 2027); c239 0.9396; c240 1.1987; c241 0.00016257; all match the cards. T cards from exact outputs: c161 0.634510, c165 0.833333, c168 0.002128, c172 2.205308, c185 gaps -0.0080, +0.0066, +0.0022, -0.0056, -0.0074, c233-c236 0.847994, 0.843496, 0.835793, 0.833926 (checked by exact Fraction arithmetic in checks/card_numbers_d11.py)."),
    "d1-cards-math": (PASS, FRESH + f"{S}/checks/card_numbers_d11.py -> checks/card_numbers_d11.out re-derives: (2/pi) arctan(0.1) = 0.0634510, x10 = 0.6345103, gap to 2/pi 0.0021094; normal P(|Z|>10) = 1.52397e-23; t(3) tail formula equals numerical integration 0.0021284; x^3 P(|V|>x) at 1000 = 2.205308 vs 4 sqrt3/pi = 2.205316; Chebyshev 7/60; ten-dice threshold 40.4006; e^5.5 = 244.69193226; m2 = 163/16, m3 = 2157/32, m4 = 149461/256, kurtosis 149461/26569 = 5.6254, skewness 2.0729. Other card algebra (c028 35/3, c045 73/9 and 7/3, c048 64/9, c058 1/3 vs 1/9, c063, c064 -ab, c074 2/9, c110, c119 and c207-c208 matrices, c122, c125, c141, c142, c153) re-derived by hand."),
    "d1-cards-lesson-statements": (PASS, FRESH + f"All 227 cards read against the labelled-block index of their lessons ({S}/checks/L01.txt to L10.txt, built by {S}/checks/block_index_d11.py) and the lesson sections they cite. Every cited Definition, Proposition, Example, Remark, Lemma, Theorem, Assumption and problem resolves to the stated content ({S}/checks/card_refs_d11.out lists 18 unresolved strings: all are problem-set titles (e.g. 'P2 · ...', 'M3 · ...') or cross-lesson 'Lesson 6's Assumption 1', which resolve on reading the lesson; no card contradicts its lesson)."),
    "d1-cards-hypotheses": (PASS, FRESH + "each card stating a Proposition carries that proposition's hypotheses (checked against the block index): e.g. c038 and c225 (at least two values, positive weights), c039 and c215 (a not 0), c242 and c244 (finitely many values; positive weights), c093 and c096 (nu a positive integer, nu > 2 or nu <= 2), c105 (finitely many values or a density under Assumption 1(c)), c129 (every law finitely valued)."),
    "d1-cards-duplicates": (PASS, FRESH + "no two cards share a front; difflib scan over all 227 fronts and backs: near-duplicates (for example c234/c235/c236, c170/c239/c240, c162/c237) differ in n, nu, law or lab part and each states a different fact; no card duplicates another."),
    "d1-cards-forward-reference": (PASS, FRESH + "no card cites 'Lesson N' with N greater than its own lesson (scan of all cards); every block reference resolves in its own lesson or the cited earlier lesson (" + f"{S}/checks/card_refs_d11.out" + ")."),
    "d1-freshness-registry": (PASS, FRESH + f"{S}/gates/verify_refs_offline_d11.out: 560 entries, 0 problems. references.json changed since 47a36d8c only in used_by lists and generated_at for other units (git diff); no M4 key changed. freshness_flags empty: M4 has no debate brief and its one reading key is a course text the page does not attribute to."),
    "d1-gates-repo": (PASS, FRESH + f"{S}/gates/ruff_check_d11.out: 'All checks passed!' (ruff check .); {S}/gates/mypy_full_d11.out: 'Success: no issues found in 385 source files' (mypy --no-incremental); {S}/gates/pytest_relevant_d11.out: exit 0 for tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_docs_figures.py, test_curriculum.py, test_memo_exemplars.py, test_refs.py."),
    "d2-2.6-constraints-exceptions": (PASS, FRESH + "project.html:203-206 and 212-223 read against reference.py and test_project.py: matched_scale rejects nu <= 2 and non-int (incl. 3.0, True, '3'), accepts nu = 3; simulate_losses rejects bad family, gaussian with nu, student_t without nu, n_draws <= 0 and non-int, empty or non-int positions, cov of wrong shape, asymmetric, non-PD; accepts n_draws = 1, nu None for gaussian, a short position; quantile_99 rejects empty and non-int, accepts one loss. Each condition has a test (test_project.py:110-696)."),
    "d1-2.6-constraints-exceptions": (PASS, FRESH + "same reading as d2-2.6-constraints-exceptions (project.html:203-206 Constraints and Grading mode; 212-220 Conventions and Conditions), checked against reference.py:19-100 and the parametrized tests."),
    "d3-2.6-mut-new-student-error": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: all listed round-5 and round-7 mutants (v9_01..v9_04, d5_01, r7d_01..r7d_04) KILLED on seeds 0-9 in the 159/159 run."),
    "d1-2.6-contract-notes-chi-claim": (PASS, FRESH + f"project.html:215 and 228 chi-square sharing claims re-run: {S}/gates/chi_probes_d11.out (lag-1 50/50; lag-2 50/50; lag-3 39/50; even-indexed 44/50; chain lag-4 38/50; disjoint lag-4 0/50), probes built by round 10 and copied into the harness unchanged."),
    "d1-2.6-mut-pairwise-survivor": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'KILLED d5_01_chi_square_shared_by_draws_two_apart.py'."),
    "d6-2.6-mut-integer-division-chi": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'KILLED r6d_02_integer_division_chi_shape.py'."),
    "d6-2.6-mut-pivot-tolerance": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'KILLED r6d_01_pivot_tolerance_1e15_rejects_tiny_variance.py'."),
    "d6-2.6-mut-lag3-sharing": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'KILLED r6d_03_chi_square_shared_by_draws_six_apart_lag_three.py'; the lag-3 probe fails 39/50 seeds ({S}/gates/chi_probes_d11.out)."),
    "d1-lab-project-1": (PASS, FRESH + f"tests/labs/M4/lab-M4-project-1.py changed this round (docstring only). Page code equals the twin byte for byte ({S}/checks/project_labs_expected_d11.py); the twin alone under python -I -W error: exit 0, empty stderr ({S}/gates/project_twins_python_I.out); expected block equals output ({S}/gates/project_labs_expected_d11.out). Hypothesis numbers re-derived: w'Sigma w = 8.4e9; matched factor 0.6; ceil(0.99 * 20000) = 19800; correlation 1/6."),
    "d1-lab-project-2": (PASS, FRESH + f"Completion lab: every page line equals the twin's line or contains '___' (34 lines each); twin output equals the expected block (project_labs_expected_d11.out); matched factor 0.600000 and 0.333333, index 19800 and 100 at n = 101."),
    "d1-lab-project-3": (PASS, FRESH + f"Closed-form lab: twin output equals the expected block (project_labs_expected_d11.out); sd 91651.514, z 2.326348, parametric loss 213213 (round(z * sd)), index rows n = 100, 101, 19987 (ceil 19788, floor 19787) re-derived by hand."),
    "d6-gate-mutate-m4": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'mutate_graders M4: PASS (159/159 killed)', exit 0."),
    "d6-gate-unit-checks": (PASS, FRESH + f"{S}/gates/check_pages_M4.out PASS (unit); {S}/gates/check_dag_M4.out PASS; {S}/gates/check_projects_M4.out PASS. Note: the page-level form 'check_pages --page project' treats project.html as a lesson (11 lesson-only failures in {S}/gates/check_pages_project.out); the project page is checked by the unit run through check_common, so this is a misapplied invocation, not a finding."),
    "d6-gate-labs": (PASS, FRESH + f"{S}/gates/run_labs_M4.out: 'run_labs M4: PASS (13/13)', exit 0 (ten lesson labs and three project labs)."),
    "d6-gate-grader-reference": (PASS, FRESH + f"{S}/gates/run_graders_M4_0-49.out: 'run_graders M4: PASS (reference 50/50 seeds, slowest 0.9 s)'."),
    "d6-gate-lint-types": (PASS, FRESH + f"{S}/gates/ruff_check_d11.out ('All checks passed!'), ruff format --check on grader and tests/labs/M4 ('17 files already formatted'), {S}/gates/mypy_full_d11.out ('Success: no issues found in 385 source files')."),
    "d6-gate-tests": (PASS, FRESH + f"{S}/gates/pytest_relevant_d11.out: exit 0."),
    "d6-gate-refs": (PASS, FRESH + f"{S}/gates/verify_refs_offline_d11.out: 'offline integrity: 560 entries, 0 problems', exit 0."),
    "d6-gate-page-smoke": (PASS, FRESH + f"{S}/gates/page_smoke_project_d11.out: 'page_smoke modules/M/M4/project.html: PASS', 'page_smoke M4: PASS', exit 0; labs 0.0-0.1 s; in-browser grader 2.4 s."),
    "d6-2.6-alt-root-set": (PASS, FRESH + f"{S}/gates/alts_d11_seeds0-9.out: the alternatives roots ledgers/M4/scripts/M4-d-r8/alts/ (alt1-alt6), M4-d-r9/alts/ (alt_r9_1..3) and M4-d-r10/alts/ (alt_d10_1, _2) all run, 10/10 each."),
    "d7-2.6-cross-term-threshold": (PASS, FRESH + f"Round-10 FAIL is fixed: project.html:228 states the measured counts. {S}/gates/cross_d11.out reproduces them (+3 %: 0/50; -3 %: 1/50 at seed 38; +5 %: 19/50; -5 %: 30/50). The reference's maximum is 0.0239 (cross_d11.out eps+0.00). test_project.py:43-47 comment: {S}/gates/cross_mutants_d11.out gives r8_03 0.0677-0.0860 and r9_02 0.1406-0.1605 over seeds 0-9, matching the comment."),
    "d7-2.6-negation-claim": (PASS, FRESH + "test_a_short_position_is_valid_and_reverses_its_loss (test_project.py:233-249) reads: negating every position negates every loss, for both families, at 300 draws, two positions. The reference passes it on seeds 0-9 (" + f"{S}/gates/reference_seeds_0-9.out" + "); a sign-flipped Student-t draw is not caught, as project.html:228 says (" + f"{S}/gates/starter_m17_signprobe_d11.out: the sign-flipped probe passes seeds 0-4" + ")."),
    "d7-2.6-tiny-variance-claims": (PASS, FRESH + "test_project.py:600-645 read: the 1e-14, 1e-16 and 1e-30 claims: (10^13)^2 x 1e-14 = 1e12 (sd 1e6, comment at 601-602); both pivots of the 1e-14 example are positive (1e-14 and about 9e-14, comment at 640); 0.89 x scale for the second pivot at 627. The test names carry a typo, recorded under d11-test-names-1e16."),
    "d7-L01-L04-prose": (PASS, FRESH + "L02.html (the only changed lesson since 47a36d8c): line 51 (why-it-matters: 'Lesson 3 uses both in the standardized variable of its Definition 2.1', checked against L03 Definition 2.1) and line 270 (variance infinite when E[X^2] = infinity and a finite mean: X^2 <= 2(X - mu)^2 + 2 mu^2 gives E[X^2] <= 2 Var + 2 mu^2, which is correct) re-checked. L01.html, L03.html, L04.html carried: byte-identical since 47a36d8c."),
    "d7-L03-numerics": (PASS, FRESH + "L03 numerics re-derived this round: m2 163/16, m3 2157/32, m4 149461/256, kurtosis 5.6254, skewness 2.0729, Bernoulli 1/10 skewness 8/3 and kurtosis 73/9, p = 1/4 kurtosis 7/3, 64/9 squared skewness (" + f"{S}/checks/card_numbers_d11.out" + ")."),
    "d7-cards-exact-lab-grade": (PASS, FRESH + "c165, c185, c233, c234, c235, c236 (exact Fraction arithmetic, no simulation, grade T with basis); c161, c168, c172 (closed forms at fixed x, grade T with basis). Simulated values are graded C with a basis naming the lab (c030, c033, c047, c082, c083, c098, c112 numerical quadrature, c113, c143, c162, c166, c167, c169-c171, c183, c188-c190, c237-c241)."),
    "d8-2.6-symmetry-tiny-scale": (PASS, FRESH + "test_covariance_must_be_symmetric_at_a_tiny_scale (test_project.py:463-472): entries of order 1e-14 with a 1e-15 asymmetry; the reference rejects it (" + f"{S}/gates/reference_seeds_0-9.out" + " and the mutate run: r8d_01 KILLED)."),
    "d8-2.6-mut-r8d-02": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'KILLED r8d_02_gaussian_stream_reseeded_per_draw.py'."),
    "d8-2.6-mut-r8d-03": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'KILLED r8d_03_positions_read_in_reverse_order.py'."),
    "d8-2.6-mut-r8d-04": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: 'KILLED r8d_04_gaussian_draws_via_normalvariate.py'."),
    "d8-2.6-alt6-chi-order": (PASS, FRESH + f"{S}/gates/alts_d11_seeds0-9.out: alt6_chi_before_normals.py 10/10 (Student-t draw order is open, Conventions item 5); alt_d11_1 (same idea) 10/10."),
    "d8-2.6-lab-counts": (PASS, FRESH + f"project.html:228 counts and the grader lines 207-228 checked against {S}/gates/chi_probes_d11.out and {S}/gates/cross_d11.out (see d1-prose-numbers)."),
    "d8-cards-changed-and-new": (PASS, FRESH + "every card that changed since the round-10 pin, read against the current lesson: c007 (quantile definition, Definition 3.1), c009 (Remark 3.3: Q(F_k) = x_k), c015 (Example 3.5, ceil(148.5) = 149), c105 (Proposition 2.3 hypotheses, Assumption 1(c)), c215 (Proposition 2.4 with sign(a)), c231 (Proposition 1.3 and Example 1.5, A^T A differs). Removed this round: c014, c046, c124 (their content is covered by c009, c215 and c231). New or reworded cards c023, c081, c140, c195, c198, c218, c241, c242 also read and correct."),
    "d8-2.6-variance-claims-lines-31-39": (PASS, FRESH + f"{S}/gates/variance_d11.out reproduces every number of test_project.py:31-39 (see d1-2.6-grader-comment-numbers)."),
    "d9-2.6-three-position-pivot": (PASS, FRESH + "test_three_position_covariance_must_be_positive_definite (test_project.py:535-553): the three matrices' last pivots are -1e-4, -1 (= 1 - (1 + 1)) and 0 (= 2 - (1 + 1)), as the comments say; the reference rejects each. " + f"{S}/gates/mutate_M4_0-9_final.out: r9_07 KILLED."),
    "d9-2.6-mut-new-r9_04_05_06": (PASS, FRESH + f"{S}/gates/mutate_M4_0-9_final.out: KILLED r9_04_gaussian_stream_skips_first_normal.py, r9_05_loss_floored_not_rounded.py, r9_06_matched_factor_squared_in_t_scale.py."),
    "d9-2.6-student-t-sign-untested": (PASS, FRESH + f"project.html:228 says the sign of the Student-t losses is not tested. {S}/gates/starter_m17_signprobe_d11.out: the sign-flipped Student-t probe (ledgers/M4/scripts/M4-d-r10/probes/student_t_sign_flipped) passes seeds 0-4 with 155-156 passed, so the statement is true; the Gaussian sign is tested by the frozen stream."),
    "d9-2.6-chain-term": (PASS, FRESH + "project.html:215 defines the chain inline in the same sentence ('A chain of sharings at lag four, in which draws 4j and 4j + 4 reuse one variable for every j >= 0'), before the term is used again at project.html:228."),
    "d9-2.6-hours-own-estimate": (PASS, FRESH + "own estimate 26 h (component list at d1-2.6-hours), 13% below the declared 30 h, inside the 30% band (21 to 39 h). Low-end reading (each component at its minimum) gives about 20 h, so the verdict rests on the central estimate; reported as a judgment, not a measurement."),
    "d9-cards-c066-c243": (PASS, FRESH + "cards.json: M4-c066 absent; M4-c243 ('In which units is the standard deviation of X measured?') read: correct against L02 Definition 2.1."),
    "d9-index-hub-lines": (PASS, CARRY + "course/modules/M/M4/index.html (unchanged since 47a36d8c; the M4 diff lists no index.html change); check_pages M4 PASS covers the hub hours split (" + f"{S}/gates/check_pages_M4.out" + ")."),
    "d9-labs-page-vs-twin-lab2": (PASS, FRESH + "lab-M4-project-2: page code and twin compared line by line this round (34 lines each; every differing line contains '___'); expected block equals output."),
}

MISSING = [i for i in prev if i not in E]
assert not MISSING, f"rows without round-11 evidence: {MISSING}"

rows = []
for rid, old in prev.items():
    status, evidence = E[rid]
    row = {"id": rid, "check": old["check"], "location": old["location"], "status": status, "evidence": evidence}
    rows.append(row)

NEW = [
    {"id": "d11-test-names-1e16", "check": "test names match the values they test (learner-visible failure output)",
     "location": "course/modules/M/M4/grader/test_project.py:612 and :624 (test function names)",
     "status": "FAIL",
     "evidence": "Two test function names say '1e16' but the values they test are 1e-16 and 1e-30 (the parametrize ids and the comments at lines 613-614 and 627 say 1e-16 and 1e-30 correctly). pytest prints the function name in every failure line, so a learner sees 'variance_of_1e16_or_1e30' for a 1e-16 case. Found by reading the whole test file (lines 600-645). Not a numerical defect: the reference passes both (" + f"{S}/gates/reference_seeds_0-9.out" + ").",
     "fix": "Rename both functions: test_one_position_with_a_variance_of_1e_minus16_or_1e_minus30_is_accepted (line 612) and test_two_positions_with_covariance_of_order_1e_minus16_or_1e_minus30_are_accepted (line 624). Behaviour is unchanged; re-run run_graders --unit M4 --seeds 0-49 and page_smoke for project.html after the rename."},
    {"id": "d11-gate-check-pages-unit", "check": "gate: check_pages --unit M4 (project page checked through the unit run)",
     "location": "tools/check_pages.py; course/modules/M/M4/project.html", "status": PASS,
     "evidence": f"{S}/gates/check_pages_M4.out: 'check_pages M4: PASS', exit 0. {S}/gates/check_pages_project.out is a misapplied invocation (--page project treats project.html as a lesson and reports 11 lesson-only problems); not a finding."},
    {"id": "d11-labs-twins-python-I", "check": "2.5 labs: every M4 twin alone under python -I -W error",
     "location": "tests/labs/M4/lab-M4-L01-1.py to lab-M4-L10-1.py; lab-M4-project-1..3.py",
     "status": PASS,
     "evidence": f"{S}/gates/lesson_twins_python_I.out: all ten lesson twins exit 0, stderr 0 bytes; {S}/gates/project_twins_python_I.out: the three project twins exit 0, stderr 0 bytes; run_labs M4 13/13 ({S}/gates/run_labs_M4.out). Runtime well under 10 s."},
    {"id": "d11-project-page-read", "check": "2.6 project.html read in full, line by line (structure, rubric, exemplars, self-assessment, stretch, reading)",
     "location": "course/modules/M/M4/project.html:1-501", "status": PASS,
     "evidence": "All 501 lines read this round. Every numbered claim re-derived: Lab 1 hypothesis (8.4e9, 0.6, 19800, correlation 1/6), Lab 1 expected block equal to the twin output, Lab 2 index 19800 and 100, Lab 3 sd 91651.514 and z 2.326348 and parametric loss 213213, index rows, the time budget (components sum to 30), the rubric, both exemplars (word counts, 2267 and 32058 cents, 15.2 %), and the cross-term and chi-square counts (project.html:228, 215)."},
    {"id": "d11-links-anchors", "check": "2.9 links: in-page anchors, local files and hub anchor in project.html",
     "location": "course/modules/M/M4/project.html (18 in-page anchors; grader/ and L10.html links; index.html#placement)",
     "status": PASS,
     "evidence": "ledgers/M4/scripts/M4-d-r11/checks/project_links_d11.out: 'in-page anchors: 18 missing targets: []'; every local file link exists; index.html#placement target id present."},
    {"id": "d11-curriculum-scope", "check": "2.6 project scope and grading mode against the curriculum entry",
     "location": "curriculum/01-foundations.yaml:186-200 (M4 entry, project brief and grading); course/modules/M/M4/project.html:194-206",
     "status": PASS,
     "evidence": "Curriculum brief: simulate portfolio losses under multivariate Gaussian vs Student-t returns with matched covariance, quantify the 99% loss change, prove the moment conditions; grading both. project.html: rung 3 specification (simulator plus proof appendix), grading mode both (line 206). The file is byte-identical since 47a36d8c for the M4 entry (git diff)."},
    {"id": "d11-cards-full-read", "check": "2.7 cards: every card read against its lesson's labelled blocks (227 cards)",
     "location": "course/modules/M/M4/cards.json (all objects); course/modules/M/M4/L01.html-L10.html (labelled blocks)",
     "status": PASS,
     "evidence": f"Block index of each lesson: {S}/checks/L01.txt to L10.txt (built by {S}/checks/block_index_d11.py); card-number and reference checks: checks/card_numbers_d11.out, checks/card_refs_d11.out, checks/card_numbers_in_lesson_d11.out. No card contradicts its lesson; each card's hypotheses match the proposition it cites; no card uses a later lesson."},
    {"id": "d11-mutants-cover-spec-claims", "check": "2.6 mutation: round-11 mutants target spec claims not covered by earlier mutants",
     "location": "ledgers/M4/mutants/d11_01..d11_04",
     "status": PASS,
     "evidence": f"d11_01 rejects negative positions (page: 'a negative position is valid input', project.html:223), killed by the cross-term test on seed 0; d11_02 draws Gaussian normals position-major (page: 'for each draw in turn ... in position order', project.html:215), killed by test_gaussian_stream_is_frozen on seed 0; d11_03 uses the inverse CDF of rng.random() for the Gaussian family (page: 'from random.Random(seed).gauss', project.html:215), killed by the same test; d11_04 uses ceil(0.99 (n-1)) (page: quantile index ceil(0.99 n), project.html:214), killed by test_quantile_99_is_the_exact_order_statistic on seed 0. All killed on all 10 seeds ({S}/gates/new_mutants_d11_fail_counts.out)."},
    {"id": "d11-alternatives-over-constraint", "check": "2.6 alternatives: correct implementations with other algorithms and cutoffs pass",
     "location": "ledgers/M4/scripts/M4-d-r11/alts/alt_d11_1..3.py and the older alternatives",
     "status": PASS,
     "evidence": f"{S}/gates/alts_d11_seeds0-9.out: 16 alternatives (including Student-t draws in a different order, a second generator for chi-square, heapq selection, exact Fraction index, 1 - 2/nu, isfinite pivot test) each 10/10 seeds exit 0."},
]

for row in NEW:
    rows.append(row)

mutants = []
for line in (ROOT / S / "gates/mutate_M4_0-9_final.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+?): (.*) -> (.*)$", line)
    if m:
        name, desc, killed = m.groups()
        mutants.append({"id": name, "description": desc.strip(), "killed_by": killed.strip()})
assert len(mutants) == 159, len(mutants)

fragment = {
    "unit": "M4",
    "slice": "d",
    "round": 11,
    "verifier": "independent verifier (Haiku), unit M4, slice d, round 11; not a builder of M4",
    "pin": "ccaeeaf4 (detached HEAD in the checkout)",
    "base": "47a36d8c (round-10 pin). Delta for slice d since 47a36d8c: course/modules/M/M4/project.html (lines 61, 212-215, 228), cards.json (c007, c009, c014/c046/c124 removed, c015, c105, c215, c231), tests/labs/M4/lab-M4-project-1.py (docstring), L02.html (lines 51 and 270, not slice d but cards cite L02), references.json (other units' used_by only)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD11-M4-d",
    "scratch": f"{S}/ (all scripts, outputs and probes; gates/ holds the gate outputs; checks/ the card and block checks)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-10 FAIL rows d1-prose-numbers and d7-2.6-cross-term-threshold are fixed at project.html:228 and re-verified (cross_d11.out).",
        "Verdict FAIL is from one new row, d11-test-names-1e16 (two test names say 1e16 for values of 1e-16 and 1e-30; learner-visible in pytest output). No numerical or spec defect was found.",
        "Carried rows (byte-identical since 47a36d8c): d1-atlas, d1-studio, d1-tools-structure, d1-2.6-mut-m17 (re-run this round too), d9-index-hub-lines.",
        "Not checked: lesson prose outside the labelled blocks and the sentences the cards restate (other slices own it). Sections were read for the claims the cards make (L01 sections 1 and 3, L03 sections 3 and 4, L04 section 3, L08 sections 3 and 4, L09 sections 1 to 4), not sentence by sentence. The 159 mutants were run on seeds 0-9 only; the killing test shown per mutant is the first failing test that mutate_graders reports, not a full kill matrix. The 16 alternatives were run on seeds 0-9 only. The repo file ledgers/M4/M4-d.json was overwritten as the round-11 fragment; its previous content was a different scheme (round 13, ids P-01..GATE-03, pin fca6bb1), which the orchestrator should reconcile.",
    ],
    "summary": "Slice d round 11: FAIL on one new row (d11-test-names-1e16, low severity, rename two tests). Everything else PASS, re-verified this round: project.html read in full; grader run 50/50; 159/159 mutants killed on seeds 0-9 (4 new); 16 alternatives 10/10; cross-term and chi-square counts re-run; variance sweep re-run; 227 cards read against the lesson blocks; labs, gates and page_smoke re-run.",
}

out = ROOT / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "->", out)
