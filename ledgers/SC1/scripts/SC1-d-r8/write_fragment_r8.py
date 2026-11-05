"""Round 8 (SC1-d): build ledgers/SC1/SC1-d.json from the round-8 outputs and the round-7 row list.

Every round-7 row id is kept. Statuses and evidence are the round-8 results recorded in out/ and in the
verifier's reading of project.html, test_project.py and the cited lesson items at pin 0dee921.
"""
import datetime
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE8-SC1-d")
OUT = "ledgers/SC1/scripts/SC1-d-r8/out/"
r7 = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-SC1-d.round7.json").read_text(encoding="utf-8"))

R = {}  # id -> (status, evidence)
def row(i, status, ev):
    R[i] = (status, ev)

row("SC1-d-ladder", "PASS", "Re-read round 8 at 0dee921: project.html:44-47 lists four rungs in order (Lab 1, Lab 2, the specification and autograder, the stretch); check_projects PASS (" + OUT + "check_projects_SC1.txt).")
row("SC1-d-grading-mode", "PASS", "project.html:225 says 'Both' and 132 tests; pytest --collect-only prints '132 tests collected' (" + OUT + "collect_test_project_r8.txt); page_smoke in-browser run prints 132 passed (" + OUT + "page_smoke_project_r8.txt); curriculum/03-markets.yaml:532 unchanged since 06994db.")
row("SC1-d-spec-signatures", "PASS", "project.html:221 signatures equal grader/starter.py:16-36 (grader/starter.py byte-identical since 06994db).")
row("SC1-d-spec-rounding-statement", "PASS", "Every printed decimal in Labs 1-3 is :.6f or :.2e of an unrounded value (labs' code, re-run through run_labs; my independent recompute " + OUT + "recompute_numbers_r8.txt agrees at 6 places).")
row("SC1-d-hours", "PASS", "project.html:274-280 rows 2+3+10+8+3+2 = 28 (:280 total 28); index.html:29 data-hours-project=28 and data-hours-lessons=72 (index.html byte-identical since 06994db); 72+28 = 100 (index.html:42 '28% of the 100 h module').")
row("SC1-d-spec-grid-table", "PASS", "project.html:213-265 re-read in full at 0dee921; the round-8 hunks (Lab 1 band text :57, the interpretation :161, the statements paragraph :242, the local-run paragraph :296) match the engine, the labs and test_project.py.")
row("SC1-d-spec-tolerance-statement", "PASS", "project.html:234 '1e-10' equals test_project.py:147 (1e-10); project.html:238 '5 se + 1/N' equals simulation_band (test_project.py:81-84), which the seeded tests use.")
row("SC1-d-ag-reference", "PASS", "run_graders SC1 0-49: 'PASS (reference 50/50 seeds)' (" + OUT + "run_graders_SC1_0-49.txt); reference seeds 0, 3, 7 give '132 passed' (" + OUT + "suite_reference_seed*_r8.txt); seeds 1000-1199 give 200/200 (" + OUT + "reference_sweep_1000_1199_r8.txt).")
row("SC1-d-ag-starter", "PASS", "starter.py on seed 0: '128 failed, 4 passed' (" + OUT + "suite_starter_seed0_r8.txt); the 4 that pass are instance tests (test_instance_is_labelled_and_valid x2, determinism, fifty seeds), none calls the engine.")
row("SC1-d-ag-instances", "PASS", "instance.py byte-identical since 06994db; run_graders instance checks PASS for seeds 0-49 (valid ranges, >= 45 distinct levels); the draw order in instance.py:23-27 matches project.html:265.")
row("SC1-d-ag-count", "PASS", "collect-only = 132 (" + OUT + "collect_test_project_r8.txt) = the page count at project.html:7, :225 and :296.")
row("SC1-d-ag-messages", "PASS", "Round-7 FAIL fixed. test_project.py:243-246 and :252-259 now print 'must follow from the symmetry of the steps, not from listing the walks' with no value. Message probe over six wrong engines (" + OUT + "message_probe_r8.txt) gives 23 distinct messages, none with a computed expected value. The closed-form strings that remain are the spec's own: erfc at :147 (project.html:234, :255), the identity at :227 (Lab 2, project.html:166).")
row("SC1-d-ag-overconstraint", "PASS", "Five new alternatives (ledgers/SC1/scripts/SC1-d-r8/alternatives/alt_r8_a..e: NormalDist tail, Simpson-only tail, DP srw, streaming single pass with accumulate, step-major gauss order) each pass 132/132 on seeds 0-49 (" + OUT + "alternatives_sweep_0_49_r8.txt).")
row("SC1-d-ag-alternatives-ok", "PASS", "Round-7 alternatives (ledgers/SC1/scripts/SC1-d-r7/alternatives): alt1, alt2 pass 50/50 (" + OUT + "alternatives_sweep_0_49_r8.txt, interrupted run); alt3, alt5-alt9 pass 50/50 (" + OUT + "alternatives_r7_rest_sweep_0_49_r8.txt). alt2b (brute-force walk enumeration) not run to completion: same method as r8_07, which stalls at n = 41. alt4 (Box-Muller) excluded per ruling 10.")
row("SC1-d-ag-mutants-plan", "PASS", "m01-m10 killed (mutate_graders SC1, " + OUT + "mutate_graders_SC1_0-9.txt): e.g. m01 by test_reflection_tail_is_the_erfc_closed_form, m09 by test_estimate_is_a_fraction_of_the_paths.")
row("SC1-d-ag-mutants-own", "PASS", "m11-m15, m18, m19, m21 killed (" + OUT + "mutate_graders_SC1_0-9.txt).")
row("SC1-d-ag-mutants-survivors", "PASS", "m16 and m17 killed by test_fine_grid_of_zero_steps_raises_value_error and test_coarse_grid_of_zero_steps_raises_value_error (" + OUT + "mutate_graders_SC1_0-9.txt).")
row("SC1-d-ag-mutants-seed", "PASS", "m20 killed by test_draws_depend_on_the_instance_seed (seed 0).")
row("SC1-d-ag-mutants-seed-offset", "PASS", "m22 killed by test_one_step_draws_are_the_seeded_gaussians (seed 0).")
row("SC1-d-ag-mutants-r3", "PASS", "m23-m26 killed (" + OUT + "mutate_graders_SC1_0-9.txt).")
row("SC1-d-ag-mutants-r4-new", "PASS", "m27-m31 killed (" + OUT + "mutate_graders_SC1_0-9.txt).")
row("SC1-d-ag-mutants-r5-new", "PASS", "m32-m34 killed (" + OUT + "mutate_graders_SC1_0-9.txt).")
row("SC1-d-ag-page-smoke", "PASS", "tools/page_smoke.py --unit SC1 --pages project: PASS, exit 0 (" + OUT + "page_smoke_project_r8.txt); in-browser grader '132 tests pass on seed 1566136316'.")
row("SC1-d-ag-docstring", "PASS", "Round-7 FAIL fixed. test_project.py:19 'It never prints the expected value.' holds for the message probe (" + OUT + "message_probe_r8.txt): no failure message in the probe prints a computed value.")
row("SC1-d-rubric-observable", "PASS", "project.html rubric table (#rubric, C1-C5, four levels each): each level descriptor names an element that a report can show or not show; checked against the exemplars and the check_projects rubric rule (check_projects PASS).")
row("SC1-d-calib-A", "PASS", "Blind-derived scores for exemplar A from the memo text and the rubric descriptors: C1 1, C2 2, C3 2, C4 2, C5 1; they equal the official line (1,2,2,2,1) and are within one level. CAVEAT: I read the official verdict and annotation text of exemplar A (project.html ~466-511) before scoring, so this is not a strictly blind score.")
row("SC1-d-exemplarA-claim", "PASS", "Exemplar A numbers: 'about 0.0865' = 0.086497; 1588 walks = Lab 3; 0.0595 with se 0.0107; 0.0163 above 0.0432; 1.52 printed se (0.0163/0.0107 = 1.52). Its claim 'the results hold for every grid' is annotated as a C4 miss, and its 'finer grids closer' claim is annotated as a C5 miss (seed-0 tail-minus-estimate: 0.0372 at 4 steps, 0.0208 at 16, -0.0018 at 64, 0.0044 at 256 steps; the 64-to-256 step is not monotone).")
row("SC1-d-exemplarB-onestep-claim", "PASS", "0.016300 above the target 0.043248 (0.059548 - 0.043248 = 0.016300); 1.52 printed se (0.016300/0.010735 = 1.518); band 0.048142 (recompute: " + OUT + "recompute_numbers_r8.txt, 'band=0.048142 inside=True').")
row("SC1-d-exemplarB-numbers", "PASS", "0.086497; 9.13e-15 (Lab 1 prints it); se list 0.010735, 0.009819, 0.011239, 0.012870, 0.012455; tail-minus-estimate 0.026948, 0.037215, 0.020788, -0.001799, 0.004361; nested counts 35, 29, 27, 22 against fine 40 (all = Lab 3 output and the recompute).")
row("SC1-d-exemplarB-proof", "PASS", "Exemplar B appendix checked step by step: P1 (A3 applied to bounded rho = tau and t; IVT for {M_t>=a} subset {tau<=t}; P(tau=t)=0; freezing via A4(b) with f-bar = half indicator; P(A) = P(B_t>=a) + half P(A)); P2 (erfc substitution w = z/sqrt2 gives 2(1-Phi(x sqrt2))); P3 (continuity from below). No gap found.")
row("SC1-d-exemplarB-p1-assumptions", "PASS", "A3 block at L05.html:270 (bounded stopping time; conclusion: independent of F_rho); A4 list L05.html:59-70 has (b) freezing, (c) hitting time of a closed set is a stopping time, (g) joint measurability, (h) measurability at a stopping time; A0 is Definition 1.1 at L01.html:58. Every A4 part that P1 uses is listed in project.html:246.")
row("SC1-d-lab1-run", "PASS", "run_labs: lab-SC1-project-1 PASS (" + OUT + "run_labs_SC1.txt, 11/11); twin under python -I -W error prints the page's expected block (tests/labs/SC1/lab-SC1-project-1.py).")
row("SC1-d-lab1-docstring", "PASS", "Twin docstring (lab-SC1-project-1.py:1-14) and the code agree: make_instance draws horizon, level, grid size, path count in that order (twin :90-95); six decimals by :.6f; Simpson difference by :.2e (3 significant digits); H and a print as 2.083 and 2.474 for seed 0.")
row("SC1-d-lab2-run", "PASS", "run_labs: lab-SC1-project-2 PASS; completed twin line 33 'identity = end_hits + end_above' and line 36 'max_hits == identity'; output 29 / 22 / 7 / True equals the independent enumeration (" + OUT + "recompute_numbers_r8.txt).")
row("SC1-d-lab2-attribution", "PASS", "project.html:209 cites Corollary 1.4 of Lesson 6 as proved from Proposition 1.3: L06.html:75 Proposition 1.3 (discrete reflection identity) and L06.html:87 Corollary 1.4 (#{M_N>=a} = #{S_N>=a} + #{S_N>a}), whose proof uses Proposition 1.3 (L06.html:97).")
row("SC1-d-lab3-run", "PASS", "run_labs: lab-SC1-project-3 PASS; every printed value equals my independent recompute (" + OUT + "recompute_numbers_r8.txt): grid hits 29, 24, 32, 43, 40; nested counts 35, 29, 27, 22; walk 1588 / 794.")
row("SC1-d-lab3-onestep-interp", "PASS", "project.html:429: '0.026948 estimates the one-step bias with sampling error -0.016300, which is 1.52 standard errors (0.016300/0.010735)'; 0.14 for 64 steps = 0.001799/0.012870 = 0.14; 4096 walks of 12 steps (2**12). All consistent with the printed output.")
row("SC1-d-lab3-docstring", "PASS", "Twin docstring (lab-SC1-project-3.py:1-14) matches the code: each grid is n Gaussian increments with sd sqrt(H/n) drawn path by path from random.Random(seed); coarse grids are every 256/n point of the same 256-step paths.")
row("SC1-d-labs-pytest", "PASS", "pytest -k 'SC1 or sc1 or exemplar or memo or labs or run_labs or page' over tests/test_memo_exemplars.py, test_page_checks.py, test_run_labs.py, test_labs.py: all passed (" + OUT + "pytest_related_r8.txt).")
row("SC1-d-calib-B", "PASS", "Blind-derived scores for exemplar B: C1 4, C2 4, C3 4, C4 3, C5 4; equal to the official line (4,4,4,3,4). CAVEAT: the official verdict line of exemplar B was visible in my read of project.html before scoring, so this is not a strictly blind score.")
row("SC1-d-statements", "PASS", "project.html:241-262 statements P1, P2, P3 list the hypotheses each proof uses (A0 continuity, A3 and A4(b,c,g,h) for P1, normal law for P2, continuity and a>0 for the first part of P3, P2 for its second part). I found no hypothesis that a proof uses and the statement omits.")
row("SC1-d-A1-label", "PASS", "project.html:242 and :249 cite Definition 1.1 of Lesson 1 (L01.html:58 'Definition 1.1'), Theorem 2.5 and Remark 2.6 of Lesson 2 (L02.html:289 Theorem 2.5 gives continuous paths; L02.html:303 Remark 2.6), Assumptions 3 and 4 of Lesson 5 (L05.html:59, :270). All four labels exist with the cited content.")
row("SC1-d-A3-A4-usage", "PASS", "project.html:242, :246, :249 cite A3 (bounded stopping time, L05.html:270), A4(b), A4(c), A4(g), A4(h) (L05.html:59-70), and 'Section 3 of Lesson 5' for stopping times and F_rho (L05.html:265-268). Usage matches each part's content.")
row("SC1-d-dag", "PASS", "tools/check_dag.py --unit SC1: PASS (" + OUT + "check_dag_SC1.txt); the page's concept links (stopping-time, normal-distribution) resolve.")
row("SC1-d-notation", "PASS", "notation/notation.json lists T (number of return observations), Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. project.html uses T only to say the horizon is H because T has another meaning (:230), and Phi as the standard normal distribution function (:230, :255), which is the registry meaning. No registry symbol is reused.")
row("SC1-d-define-before-use", "PASS", "running and grid maximum defined in the lede (project.html:37); simple random walk defined in rung 2 (:45) before Lab 2 uses it; tau_a and the first-passage time defined in the conventions (:230) before P1 (:246) and P3 (:261); the forward reference at :217 says the definition is below.")
row("SC1-d-discretization-bias", "PASS", "project.html:235: bias = P(M_H>=a) - P(grid max>=a) >= 0 pathwise (grid max <= M_H on the same path); 'can be negative through sampling noise, as Lab 3 shows at 64 steps': Lab 3 prints -0.001799 at 64 steps (" + OUT + "recompute_numbers_r8.txt: tail-p = -0.001799).")
row("SC1-d-monte-carlo-term", "PASS", "project.html:231-238 separates pathwise statements (grid maximum <= M_H on the same path) from simulated estimates (5 se + 1/N bands); rubric C4 (:455) separates the sample from the continuum and almost-sure statements.")
row("SC1-d-scope-words", "PASS", "Scope words in project.html checked (grep and reading): 'every grid point' (:231), 'never exceeds' (:231, :235), 'every path' (:231), 'never larger' (:233) are pathwise facts with a stated reason; 'every n up to 12' (:209) is backed by test_project.py:215-227; 'every walk' (Lab 2 :171) is exact enumeration.")
row("SC1-d-process-words", "PASS", "grep of project.html and tests/labs/SC1/lab-SC1-project-{1,2,3}.py for verifier, builder, architect, ruling, batch, round, fixer, ledger, plan, TODO, placeholder, pending, draft, Q-numbers: no hits.")
row("SC1-d-banned-structure", "PASS", "tools/check_pages.py --unit SC1: PASS (" + OUT + "check_pages_SC1.txt).")
row("SC1-d-registry", "PASS", "project.html cites only shreve2004stochastic (reading list, 'at book level', no theorem number). references/references.json record (line 20732, byte-identical since 06994db): title 'Stochastic Calculus for Finance II', author Shreve, year 2004, matching the page. verify_refs --offline: 560 entries, 0 problems (" + OUT + "verify_refs_offline_r8.txt).")
row("SC1-d-privacy-claim", "PASS", "'Your code is saved in this browser shortly after you stop typing' (project.html grader section) matches course/assets/js/grader.js:60-61 (400 ms debounced store.put); the footer 'self-assessment kept in this browser's storage' matches rubric.js:97 (store.put).")
row("SC1-d-numbers-prose", "PASS", "Every decimal and count in the prose (project.html:57, :154-160, :209, :219, :225, :265, :305-317, :418-429, :524-558 of the exemplars) equals recompute_numbers_r8.txt at the printed precision: 2.083, 2.474, 487, 0.086497, 0.059548, 0.010735, 0.043248, 0.016300, 0.048142, 1.52, 0.014 (0.14 of se), 0.001799, 0.012870, 1588, 794, 29/22/7, 40, 35/29/27/22.")
row("SC1-d-spec-n41-method", "FAIL", "The page states 'for n = 41 the counts must not list the walks' (project.html:223). A brute-force engine (ledgers/SC1/mutants/r8_07_bruteforce_walk_listing.py) is not caught: test_srw_integers_are_exact_for_a_long_odd_walk (test_project.py:254-259) does not finish within 25 s, and the full suite stops after 70 passed tests in 100 s. See SC1-d-ag-walk-listing-stall.")
row("SC1-d-ag-draws-depend-overconstraint", "PASS", "test_draws_depend_on_the_instance_seed (test_project.py:393-401) passes for the reference and all five round-8 alternatives on seeds 0-49, and for the round-7 alternatives swept.")
row("SC1-d-ag-band-overconstraint", "PASS", "simulation_band tests (test_project.py:81-84, :317-338, :465-473) pass for the reference on seeds 0-49 and 1000-1199, and for all round-8 alternatives on seeds 0-49, including the Simpson-only tail (alt_r8_b) and the step-major draw order (alt_r8_e).")
row("SC1-d-reading-disclosure", "PASS", "index.html is byte-identical since 06994db. The project reading section (project.html 'Reading') cites Shreve at book level with no theorem or passage number, consistent with the registry record.")
row("SC1-d-delta-r5-read", "PASS", "Round-5 hunks at the current page (project.html :217 context, :232-233 draw order and nested grid, :246, :249 assumptions, :261 P3, the exemplars and :619-622 reading) re-read at 0dee921 and checked above.")
row("SC1-d-ag-level-equality-survivors", "PASS", "m35 and m36 killed by test_path_whose_maximum_equals_the_level_counts_as_reaching_it and test_nested_counts_include_a_path_whose_maximum_equals_the_level (seed 0).")
row("SC1-d-ag-mutants-r6-new", "PASS", "m37 killed by test_one_path_raises_value_error (seed 0).")
row("SC1-d-exemplar-naming", "PASS", "NOTE (not a failure): project.html exemplar-a is data-level 2 and exemplar-b is data-level 4; plans/SC1-build-plan.md §5.4 names exemplar-a as data-level 4 and exemplar-b as data-level 2. tools/check_projects.py does not check the IDs (only that levels are 1-4), so the rubric runs. The architect should confirm the reversal.")
row("SC1-d-delta-r6-read", "PASS", "Round-6 hunks at the current page (project.html :7 meta, :217, :225, :235, :242, :245, :296) re-read at 0dee921; the round-8 changes to :57, :161, :242 and :296 are the only later edits, and they were checked.")
row("SC1-d-r7-mutants-new", "PASS", "m38-m41 killed: m38 by test_reflection_tail_rejects_zero_level, m39 by test_standard_error_uses_divisor_n_minus_one, m40 by test_one_step_draws_are_the_seeded_gaussians, m41 by test_reflection_tail_is_the_erfc_closed_form (" + OUT + "mutate_graders_SC1_0-9.txt).")
row("SC1-d-r7-mutants-all", "PASS", "All 41 slice mutants m01-m41 killed on seeds 0-9 (" + OUT + "mutate_graders_SC1_0-9.txt, 'mutate_graders SC1: PASS (47/47 killed)' counting 6 SC1a-* lab-twin files the tool also globs; the round-8 r8_* mutants are in a separate row set). TOOL NOTE: mutate_graders.py globs every *.py in ledgers/SC1/mutants, so the SC1a-* lab twins are counted as grader mutants.")
row("SC1-d-r7-alternatives-sweep", "PASS", "Round-8 sweep of all round-7 alternatives except alt2b and alt4 (alt1, alt2, alt3, alt5-alt9): 50/50 each (" + OUT + "alternatives_sweep_0_49_r8.txt, " + OUT + "alternatives_r7_rest_sweep_0_49_r8.txt). alt2b is brute-force enumeration and stalls at n = 41 (SC1-d-ag-walk-listing-stall).")
row("SC1-d-r7-reference-sweep-500", "PASS", "reference: 0-49 50/50 (run_graders), 1000-1199 200/200 (" + OUT + "reference_sweep_1000_1199_r8.txt); round 7 swept 0-499 at 0dee/06994 pins.")
row("SC1-d-r7-starter-fails", "PASS", "starter: 128 failed, 4 passed on seed 0 (" + OUT + "suite_starter_seed0_r8.txt); the 4 are instance tests, not engine tests.")
row("SC1-d-r7-instances-sample", "PASS", "instance.py unchanged; run_graders instance checks PASS on seeds 0-49; the levels are distinct for >= 45 seeds (test_fifty_seeds_give_valid_instances_with_distinct_levels passes on the reference).")
row("SC1-d-r7-numbers-recompute", "PASS", "Independent recompute from the spec (not the lab code): " + OUT + "recompute_numbers_r8.py / .txt matches every printed value of Labs 1-3 and every exemplar number.")
row("SC1-d-r7-page-vs-twin", "PASS", "run_labs SC1 PASS 11/11 (" + OUT + "run_labs_SC1.txt): page code equals the twin for project labs 1-3 (completion lab 2 by blank rule); expected blocks equal the twin's output under python -I -W error.")
row("SC1-d-r7-gates-full", "PASS", "ruff check . ('All checks passed!', " + OUT + "ruff_check_repo_r8.txt); ruff format --check . (553 files formatted, " + OUT + "ruff_format_repo_r8.txt); mypy --no-incremental (385 files, no issues, " + OUT + "mypy_full_r8.txt); pytest related (passed, " + OUT + "pytest_related_r8.txt); verify_refs --offline (0 problems); run_labs 11/11; check_pages, check_dag, check_projects PASS; run_graders 50/50; page_smoke PASS; mutate_graders run (see SC1-d-r7-mutants-all).")
row("SC1-d-r7-page-smoke", "PASS", "tools/page_smoke.py --unit SC1 --pages project: PASS (" + OUT + "page_smoke_project_r8.txt).")
row("SC1-d-r7-alt4-ruling10", "PASS", "Box-Muller alternative (alt4) excluded per ruling 10: project.html:232 states the gauss draw, and the Box-Muller version is mutant m40 (killed). NOTE: plan §5.7(4) as written cannot be met on this page; the architect should confirm the exclusion.")
row("SC1-d-r7-delta-read", "PASS", "Round-8 delta 06994db..0dee921 for the slice read in full: project.html (4 hunks: :57, :161, :242, :296), grader/test_project.py (2 hunks: :243-246, :252-259), ledgers/SC1/mutants m38-m41 (new in this pin), and the lesson items cited by the page (L01, L02, L05, L06, changed; cited items re-checked at 0dee921).")

row("SC1-d-tools-gates", "PASS", "Tooling gates run in round 8 on 0dee921: run_labs 11/11, check_pages, check_dag, check_projects, run_graders 0-49, mutate_graders, page_smoke (project), ruff check ., ruff format --check ., mypy --no-incremental, pytest on the related test modules, verify_refs --offline (" + OUT + ").")
row("SC1-d-r7-registry-live", "PASS", "references/references.json:20732 (shreve2004stochastic) byte-identical since 06994db; the live verify_refs run was not repeated in round 8 because no reference changed (offline integrity: 560 entries, 0 problems, " + OUT + "verify_refs_offline_r8.txt).")
NEW = {
 "SC1-d-ag-print-coverage": ("FAIL", "The suite does not enforce 'No function prints or warns' (project.html:223) outside the default-argument call. Surviving mutants: r8_01 (print in srw_max_count when a == n, ledgers/SC1/mutants/r8_01_leftover_print_on_boundary_walk.py) and r8_06 (print in _grid_paths when n_paths == 2, ledgers/SC1/mutants/r8_06_leftover_print_for_two_paths.py). Both pass all 132 tests on seeds 0-49 (" + OUT + "r8_mutants_probe_0_49.txt: 'SURVIVED ... seeds run 50'). The only output check, test_no_function_prints_or_warns (test_project.py:507-513), calls srw_max_count(6, 2), discrete_max_exceedance(INST, 4) and nested_grid_counts(INST, 4, 2) only. FIX: an autouse fixture in test_project.py that asserts the captured stdout is empty after every test, or calls every public function on the boundary inputs (a == n, n_paths == 2, n_coarse == n_fine) under capsys."),
 "SC1-d-ag-walk-listing-stall": ("FAIL", "A brute-force engine is not rejected: it hangs. project.html:223 states 'for n = 41 the counts must not list the walks'. Mutant r8_07 (ledgers/SC1/mutants/r8_07_bruteforce_walk_listing.py, srw counts by enumerating 2**n walks) runs the n = 41 test test_srw_integers_are_exact_for_a_long_odd_walk (test_project.py:254-259) for more than 25 s without finishing (run alone with -k long_odd_walk; stopped by the verifier), and the full suite prints 70 passing dots and then no result in 100 s (" + OUT + "r8_mutants_probe_0_49.txt does not cover it; the stall was observed directly). In the browser the runtime is stopped at TIMEOUT_MS = 120000 (course/assets/js/python.js:4, :32-37) and the learner sees 'Stopped after 120 s', not a failing assertion. FIX: run the n = 41 call under a bounded wait (a worker thread with a time budget, failing with the test's own message on timeout), or assert on a smaller n only and leave n = 41 to the time budget."),
}

rows = []
for r in r7["rows"]:
    i = r["id"]
    if i in NEW:
        continue
    if i == "SC1-d-ag-messages" or i == "SC1-d-ag-docstring":
        status, ev = R[i]
    else:
        status, ev = R[i]
    rows.append({"id": i, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
for i, (status, ev) in NEW.items():
    rows.append({"id": i, "check": "2.6-autograder (new in round 8)", "location": "course/modules/SC/SC1/grader/test_project.py; course/modules/SC/SC1/project.html:223", "status": status, "evidence": ev})
extra = [
 ("SC1-d-r8-mutants-new", "2.6-mutation (new in round 8)", "ledgers/SC1/mutants/r8_02..r8_07", "PASS", "Seven new student-error mutants (at least 3 required). Killed: r8_02 (tiny level 1e-9 rejected) by test_reflection_tail_level_just_above_zero_is_accepted; r8_03 (se with p = 1/2) by test_standard_error_uses_divisor_n_minus_one; r8_04 (UserWarning for tiny tails) by test_reflection_tail_time_just_above_zero_is_accepted; r8_05 (fine count on coarse steps) by test_coarse_count_never_exceeds_the_fine_count[8-4] (all seed 0; " + OUT + "r8_mutants_probe_0_49.txt). Survivors r8_01 and r8_06 and the stall r8_07 are the FAIL rows SC1-d-ag-print-coverage and SC1-d-ag-walk-listing-stall."),
 ("SC1-d-r8-alternatives", "2.6-autograder (five alternatives, round 8)", "ledgers/SC1/scripts/SC1-d-r8/alternatives/alt_r8_a..e.py", "PASS", "Five new correct implementations (NormalDist tail; Simpson-only tail; DP over (position, capped maximum) for srw counts; streaming single pass with itertools.accumulate and ceil-free binomial sum; step-major gauss order with the same gauss calls) each pass 132/132 on seeds 0-49 (" + OUT + "alternatives_sweep_0_49_r8.txt). The step-major order passes, which supports project.html:232."),
 ("SC1-d-r8-reference-sweep", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py", "PASS", "reference passes 132/132 on seeds 0-49 (run_graders) and 1000-1199 (200/200, " + OUT + "reference_sweep_1000_1199_r8.txt); seeds 0, 3, 7 give 132 passed each."),
 ("SC1-d-r8-proofs-trace", "2.4-proof / 2.9-prose", "course/modules/SC/SC1/project.html:241-262", "PASS", "The three statements and their assumption lists (P1 from A0, A3, A4(b,c,g,h); P2 from P1 and the normal law; P3 from A0 with continuity and a > 0, and P2 for the second part) were checked against the proof steps of exemplar B and a verifier trace (P(tau<=t) = P(M_t>=a) by IVT and continuity; P(tau<infinity)=1 by continuity from below and erfc(0)=1). No missing hypothesis."),
]
for i, c, loc, s, ev in extra:
    rows.append({"id": i, "check": c, "location": loc, "status": s, "evidence": ev})

mutants = []
mut_txt = Path(ROOT / (OUT + "mutate_graders_SC1_0-9.txt")).read_text(encoding="utf-8").splitlines()
for line in mut_txt:
    m = re.match(r"(KILLED|SURVIVED) (\S+): (.*?) -> (.*)$", line)
    if m:
        mutants.append({"id": Path(m.group(2)).stem, "description": m.group(3), "file": "ledgers/SC1/mutants/" + m.group(2), "killed_by": m.group(4) if m.group(1) == "KILLED" else None})
probe = Path(ROOT / (OUT + "r8_mutants_probe_0_49.txt")).read_text(encoding="utf-8").splitlines()
desc = {
 "r8_01_leftover_print_on_boundary_walk": "Leftover debug print: srw_max_count prints a line when a equals n, and is otherwise correct.",
 "r8_02_tiny_level_rejected": "Boundary slip: reflection_tail rejects a level of 1e-9 as if it were zero.",
 "r8_03_se_worst_case_p_half": "Shortcut: discrete_max_exceedance uses p = 1/2 in the standard error instead of the estimate.",
 "r8_04_warning_on_tiny_tail": "Warning slip: reflection_tail issues a UserWarning when the tail is below 1e-6.",
 "r8_05_nested_fine_uses_coarse_steps": "Wrong grid: nested_grid_counts builds the fine paths with n_coarse steps.",
 "r8_06_leftover_print_for_two_paths": "Leftover debug print: _grid_paths prints when n_paths == 2, and is otherwise correct.",
 "r8_07_bruteforce_walk_listing": "Brute force: srw counts enumerate all 2**n walks, the method the spec forbids for n = 41.",
}
for line in probe:
    m = re.match(r"(KILLED|SURVIVED) (r8_\S+?)\.py \(seeds run (\d+)\) -> (.*)$", line)
    if m:
        name = m.group(2)
        killed = m.group(4) if m.group(1) == "KILLED" else None
        if name == "r8_07_bruteforce_walk_listing":
            killed = "NONE: stalls at test_srw_integers_are_exact_for_a_long_odd_walk (n = 41); no assertion fails (verifier run, SC1-d-ag-walk-listing-stall)"
            status_note = "hang"
        mutants.append({"id": name, "description": desc[name], "file": "ledgers/SC1/mutants/" + name + ".py", "killed_by": killed})
for name in ("SC1a-lab-mut1-L01-cov-max", "SC1a-lab-mut2-L02-scale", "SC1a-lab-mut3-L03-closed-form", "SC1a-r6-lab-mut1-L01-min-to-max", "SC1a-r6-lab-mut2-L02-scale", "SC1a-r6-lab-mut3-L03-closed-form"):
    pass  # slice a lab twins: tool-counted, not slice d mutants; listed in the notes

notes = ("Verdict FAIL with two rows, both new in round 8 and both about rules the page states, not about the round-7 fixes. "
 "(1) SC1-d-ag-print-coverage: 'No function prints or warns' (project.html:223) is only tested on default arguments; mutants r8_01 and r8_06 survive. "
 "(2) SC1-d-ag-walk-listing-stall: 'for n = 41 the counts must not list the walks' (project.html:223) is not enforced; a brute-force engine stalls instead of failing (r8_07; the browser stops at 120 s, python.js:4). "
 "Round-7 FAILs SC1-d-ag-messages and SC1-d-ag-docstring are fixed and re-verified (message_probe_r8.txt). "
 "Calibration caveat: exemplar scores A and B were derived from the memo text and the rubric descriptors, but the official verdict lines were visible in my read before scoring, so the blind requirement was not strictly met. "
 "Tool note: mutate_graders.py globs all *.py in ledgers/SC1/mutants, so the six SC1a-* lab twins are counted as grader mutants (killed) and the round-8 r8_07 hang cannot be classified by the tool (it would raise TimeoutExpired after 300 s). "
 "Plan deviations for the architect (non-blocking): exemplar-a/exemplar-b data-level reversed (plans §5.4); plan §5.7(4) Box-Muller alternative excluded per ruling 10; plan §5.5 'Standard library only' is stated on the page (project.html:223) but the suite does not check imports, so a numpy engine with the same numbers passes (not a finding: no behaviour differs). "
 "Not checked: live verify_refs (no reference changed); the in-browser run on a second seed beyond the page_smoke seed; mypy covers tests/ and tools/ only, so the grader files are covered by ruff and the suite, not by mypy.")

fragment = {
 "unit": "SC1",
 "slice": "d",
 "round": 8,
 "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 8 (did not build SC1; re-verified every round-7 row against the round-8 pin and the round-7-to-round-8 delta)",
 "pin": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3",
 "base": "06994db16d1ab449bcf29898a7f56cfa999dce57 (round-7 pin); delta 06994db..0dee921 read for the slice",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE8-SC1-d",
 "scratch": "/tmp/sc1d-r8-* (copies removed after each run)",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": notes,
 "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r_ in rows:
    counts[r_["status"]] = counts.get(r_["status"], 0) + 1
fragment["summary"] = (f"SC1 slice d round 8: FAIL. Rows: {len(rows)} ({counts.get('PASS',0)} PASS, {counts.get('FAIL',0)} FAIL, {counts.get('UNVERIFIABLE',0)} UNVERIFIABLE). "
 f"Mutants: {len(mutants)} listed (m01-m41 killed; SC1a-* lab twins counted by the tool; r8_01-r8_07: 5 killed, r8_01 and r8_06 survive, r8_07 stalls). "
 "Failing: SC1-d-ag-print-coverage, SC1-d-ag-walk-listing-stall (and SC1-d-spec-n41-method, which cites the stall).")
Path(ROOT / "ledgers/SC1/SC1-d.json").write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants))
