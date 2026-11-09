"""Build ledgers/M5/M5-d.json for round 4 (slice d) from the round-4 outputs. Rows are written by hand below;
the mutant list is parsed from out/mutate_M5_0-9_with_r4.out, which prints every mutant's first docstring line."""
import datetime
import json
import re
import sys
from pathlib import Path

CHECKOUT = Path(sys.argv[1])
OUT = CHECKOUT / "ledgers/M5/scripts/M5-d-r4/out"
now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()

mutants = []
for line in (OUT / "mutate_M5_0-9_with_r4.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    mutants.append({
        "name": name,
        "description": desc,
        "killed_by": killer if status == "KILLED" else None,
    })
assert len(mutants) == 135, len(mutants)

ROWS = [
 ("M5-d-r1-01", "2.6-autograder-reference", "course/modules/M/M5/grader/reference.py", "PASS",
  "tools/run_graders.py --unit M5 --seeds 0-49 (rc 0): 'run_graders M5: PASS (reference 50/50 seeds, slowest 0.3 s)' (ledgers/M5/scripts/M5-d-r4/out/run_graders_M5_0-49.out). In a scratch workspace the reference as contraction_solver.py passes all 101 tests with QF_SEED=0, --assert=plain -W error (pytest output in this round). reference.py is byte-identical to the round-3 pin (git diff 8196077d..edbb7aa8 lists no change)."),
 ("M5-d-r1-02", "2.6-instances", "course/modules/M/M5/grader/instance.py", "PASS",
  "Re-run this round: ledgers/M5/scripts/M5-d-r2/d2_instances.py under python -I (out/instances_r4.out): invalid seeds [], 15 betas, 27 alphas, 17 sizes, 50 distinct solved vectors. Docstring ranges (lines 5-12) match the code (lines 44-53): beta 80-95 /100, alpha 30-70 /100, size 8-24, first point 0.20-0.90, steps 0.05-0.40, last point above 1 (line 51), tol set (line 27)."),
 ("M5-d-r1-03", "2.6-mutation-existing", "ledgers/M5/mutants/ (all 131 files at this pin)", "PASS",
  "tools/mutate_graders.py --unit M5 --seeds 0-9 on the pin (ledgers/M5/scripts/M5-d-r4/out/mutate_M5_0-9_with_r4.out): 'mutate_graders M5: PASS (135/135 killed)', rc 0. The 128 pre-round-3 mutants and the three round-3 mutants are all killed by the round-4 suite."),
 ("M5-d-r1-04", "2.6-mutation-new-killed", "ledgers/M5/mutants/d1_02_continuation_reads_the_current_state.py; d1_03_value_is_the_penultimate_iterate.py", "PASS",
  "out/mutate_M5_0-9_with_r4.out: d1_02 KILLED by test_operator_matches_its_definition[0] (seed 0); d1_03 KILLED by test_certified_error_bounds_the_distance_to_the_fixed_point[0] (seed 0)."),
 ("M5-d-r1-05", "2.6-mutation-survivor", "course/modules/M/M5/grader/test_project.py:739-753; ledgers/M5/mutants/d1_01_top_grid_point_never_a_successor.py", "PASS",
  "out/mutate_M5_0-9_with_r4.out: d1_01 KILLED by test_operator_uses_the_top_point_on_a_grid_inside_zero_one (seed 0)."),
 ("M5-d-r1-06", "2.6-alternatives", "ledgers/M5/alternatives/ (alt1..alt5 pass); plans/M5-build-plan.md:304; plans/M5-open-items.md:18 and 113-130; course/modules/M/M5/project.html:244-245", "FAIL",
  "Alternatives pass: out/alt_seeds_0-49.out: alt1..alt5 50/50 each on seeds 0-49. The two rejected files fail 0/50 (not_accepted/). The contract conflict is unchanged: plans/M5-build-plan.md:304 still names the in-place (Gauss-Seidel) sweep and the residual-bound stop as must-pass alternatives, and project.html:244-245 now states that each sweep is synchronous, so the in-place sweep cannot pass. plans/M5-open-items.md decision 3 (line 18) still says the in-place sweep and the residual bound are accepted, which contradicts the page. No architect ruling in plans/FINAL-ARCHITECT-RULINGS.md resolves this (rulings 10 and 21 do not mention M5). Non-blocking under ruling 26 (not a blocking kind), but it stays open until the architect decides.",
  ),
 ("M5-d-r1-07", "2.6-failure-message-leak", "course/modules/M/M5/grader/test_project.py (every expect/must_raise/pytest.fail message)", "PASS",
  "ledgers/M5/scripts/M5-d-r2/d2_message_scan.py re-run (out/message_scan_r4.out): 81 messages scanned. My own grep of every message literal (this round) finds only literal test constants (1e-10, 1e-12, 5e-13, 1e-6, the spec's own values), never a computed solver value. Observed with --assert=plain on the round-4 mutant r4_02: 'E   Failed: <message>' and 'All traceback entries are hidden'; no expected value printed."),
 ("M5-d-r1-08", "2.6-mutant-descriptions", "ledgers/M5/mutants/ (135 files)", "PASS",
  "AST scan (this round): every mutant has a first docstring line of at least 20 characters naming a student error; out/mutate_M5_0-9_with_r4.out prints each. I read all 135 printed lines. The four round-4 mutants name errors a learner writes (Euclidean norm of the change, (1-beta)/beta factor, continuation at the next grid point, sqrt(k**alpha) - k' parenthesis error)."),
 ("M5-d-r1-09", "2.6-test-count", "course/modules/M/M5/project.html:235 ('Grading mode', 101 checks); grader/test_project.py", "PASS",
  "Page says 101 checks (project.html:235). pytest --collect-only -q (out/collect_r4.out): '101 tests collected'. Full run on the reference: '101 passed'."),
 ("M5-d-r1-10", "2.6-browser-suite", "course/modules/M/M5/project.html:272-281; course/assets/js/grader.js:53; course/assets/js/py-worker.js:111", "PASS",
  "page_smoke.py --unit M5 --pages project --skip-sweep (out/page_smoke_project.out): 'in-browser grader: All 101 tests pass on seed 748553322', 'page_smoke modules/M/M5/project.html: PASS', rc 0. course/assets/js/python.js:4 TIMEOUT_MS = 120000 matches the page's 120 seconds."),
 ("M5-d-r1-11", "2.6-rubric-observable", "course/modules/M/M5/project.html:404-412 (rubric cells C1-C6)", "PASS",
  "Each criterion has four level cells that name observable features (proof steps named, numbers printed by run_report.py, named limitation with direction). The only gap found is the C5 exclusivity gap recorded in row M5-d-r3-42."),
 ("M5-d-r1-12", "2.6-rubric-caption", "course/modules/M/M5/project.html:404", "PASS",
  "Caption now states 'Where a passage fits two cells, score the lower level.' That rule resolves the overlaps between adjacent levels in C1, C2 and C4."),
 ("M5-d-r1-13", "2.6-calibration-exemplar-A", "course/modules/M/M5/project.html:420-450 (exemplar A, data-scores 2,2,1,2,2,2)", "UNVERIFIABLE",
  "Not scored by this verifier (task instruction and ruling 23): a dedicated blind scorer must strip the annotations, the verdict line and data-scores, score the memo prose, then compare with the official scores. This verifier read the annotations while checking the page, so it cannot be blind.",
  ),
 ("M5-d-r1-14", "2.6-calibration-exemplar-B", "course/modules/M/M5/project.html:452-482 (exemplar B, data-scores 4,4,4,4,4,3)", "UNVERIFIABLE",
  "Not scored by this verifier (ruling 23). Delegated to the dedicated blind scorer; same reason as M5-d-r1-13.",
  ),
 ("M5-d-r1-15", "2.6-hours-arithmetic", "course/modules/M/M5/project.html:33, 258-264; course/modules/M/M5/index.html:29, 39-42; curriculum/curriculum.json (M5 hours 130)", "PASS",
  "Table rows 1+2+8+7+3+5 = 26 (project.html lines 258-264, total 26). data-hours-project 26 (line 33). Hub: data-hours-lessons 104 + data-hours-project 26 = 130 (index.html:29), and 26/130 = 20.0 % (line 42 says 20%). Lesson hours 6x10 + 4x11 = 104 is outside this slice (index.html:131)."),
 ("M5-d-r1-16", "2.6-labs", "course/modules/M/M5/project.html:55-220, 287-390; tests/labs/M5/lab-M5-project-1..3.py", "PASS",
  "tools/run_labs.py --unit M5 --page project (out/run_labs_M5_project.out): 'run_labs M5: PASS (3/3)'. tools/run_labs.py --unit M5 (out/run_labs_M5_all.out): 'PASS (13/13)'. run_labs checks page code byte-identical to twin, twin under python -I -W error, and expected block equal to output under the labs.js rule."),
 ("M5-d-r1-17", "2.6-rung1-annotated", "course/modules/M/M5/project.html:57, 58-155 (Lab 1 prose 'Stated before running' and code)", "PASS",
  "Independent recomputation (ledgers/M5/scripts/M5-d-r4/numbers_r4.py, out/numbers_r4.out): resources 0.707107/0.948683/1.183216; feasible {0.5} from 0.5 and {0.5,0.9} from 0.9 and 1.4; V1 = (0.455090, 0.669838, 0.826569); contraction 0.409581 <= 0.743912; sweep-1 change 0.826569, certified 7.439119; stop at sweep 146 (sweep 145 certified 1.055e-6 > 1e-6); change 1.055e-7; certified 9.495187e-7 printed as 0.000000950; actual 9.495178e-7, agree to nine decimals as printed."),
 ("M5-d-r1-18", "2.6-rung2-completion", "course/modules/M/M5/project.html:159-222", "PASS",
  "Recomputed: ratio for V=0, W=(0.1,0.2,0.3) is 0.300000000 (<= beta); 146 sweeps; certified 9.495e-07; last change 1.055e-07; values 4.550898, 4.765646, 4.922377. Instant check (out/lab2_instant_check_r4.out): the correct bound line is accepted; the wrong variants (certified = change, 2*change, change/(1-beta)) are rejected because the sweep-count token is exact (146 is the only count a correct bound gives). Note the 1e-6 absolute tolerance is reported separately in M5-d-r4-47."),
 ("M5-d-r1-19", "2.6-numbers-lab3", "course/modules/M/M5/project.html:289, 373-388; exemplar text not scored", "PASS",
  "Recomputed (out/numbers_r4.out): smallest gap 0.021829 (> 1e-6); 236 sweeps; last change 1.025e-11; certified 9.226e-11; a priori count 242, so the budget is 242 + 1 = 243 and 236 <= 243; residual 9.226e-12 <= (1+beta) x 9.226e-11 = 1.753e-10; worst ratio over 200 pairs (random.Random(7)) 0.9000000000000001 printed 0.900000 <= beta + 1e-12; the ten V(k) values match the expected block to 6 decimals."),
 ("M5-d-r1-20", "2.6-proof-math", "course/modules/M/M5/project.html:393-399 (brief A1-A4 hypotheses and conclusions); Conventions 'Certified error' and 'Iteration budget' (lines 244-248)", "PASS",
  "A1: |max_f - max_g| <= max|f - g| over one feasible set; the feasible set depends only on k (k_1 feasible from every state, k^alpha >= k_1 for k<=1 because alpha<1, k^alpha > 1 >= k_1 for k>1), so A1 holds for all V, W. A4: d_{n+j} <= beta^j d_n gives ||V_n - V*|| <= d_n beta/(1-beta). A priori budget: V_1 is in [0, sqrt(k_m^alpha)], so cert_n <= beta^n sqrt(k_m^alpha)/(1-beta), which justifies 'within the a priori count plus one' (the stated count is valid). No hypothesis is missing from A1-A4 as listed."),
 ("M5-d-r1-21", "2.6-named-invalid-inputs", "course/modules/M/M5/project.html:240-248; course/modules/M/M5/grader/test_project.py:618-785", "PASS",
  "Each condition on the page's list has a must_raise test: beta/alpha (lines 621-636: 0, 1, -0.1, 1.2, nan, inf, bool, string), tol (647-653), max_iter (671-678, including float and bool), grid (688-726: empty, equal, decreasing, zero, negative, first above one, nan, bool, inf, string), values length (780-785). No test demands ValueError for a condition the page does not name (checked each must_raise)."),
 ("M5-d-r1-22", "2.6-starter-signatures", "course/modules/M/M5/grader/starter.py:18,23; grader/reference.py:94,101; project.html:231", "PASS",
  "starter.py signatures bellman_operator(params, grid, values) and solve(params, grid, tol, max_iter) (lines 18, 23) equal reference.py:94, 101 and the page text (line 231). starter.py is byte-identical since 8196077d (git diff empty). The suite run on a scratch copy of starter.py (QF_SEED=0, --assert=plain -W error) gives '101 failed', so the starter is not accepted."),
 ("M5-d-r1-23", "2.6-time-limit", "course/modules/M/M5/project.html:233; course/assets/js/python.js:4", "PASS",
  "Page: 'A run in your browser stops after 120 seconds.' python.js TIMEOUT_MS = 120000 (line 4)."),
 ("M5-d-r1-24", "2.6-notation", "course/modules/M/M5/project.html (all math); notation/notation.json", "PASS",
  "The page writes reals as \\R (registered macro, notation.json macros) and has no \\mathbb{R}. Macros used: beta, alpha, le, ge, lVert, rVert, mathcal, sup, max, sum, sqrt, ast, times, cdots, mathrm, frac, text, in, infty. The registered symbols (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q) do not appear with another meaning. The operator's \\mathcal{B} and the iterate symbols are defined on the page (Conventions, Rung 1), and notation.json says alpha and beta are local."),
 ("M5-d-r1-25", "2.8-simulated-label", "course/modules/M/M5/project.html:229; course/modules/M/M5/grader/instance.py:3, 56", "PASS",
  "project.html:229 'No data file. ... All of it is SIMULATED: generated parameters, not data.' instance.py:3 'All values are SIMULATED.' and :56 'label': 'SIMULATED'."),
 ("M5-d-r1-26", "2.8-data-manifest", "course/modules/M/M5/project.html (no data-files attribute)", "PASS",
  "grep -c 'data-files' course/modules/M/M5/project.html = 0. No embedded data is read by any lab (labs read no file; Lab 1 and Lab 3 are self-contained)."),
 ("M5-d-r1-27", "2.8-figures", "course/modules/M/M5/project.html", "PASS",
  "grep for figure, svg and chart in project.html: 0 hits (no figures on this page)."),
 ("M5-d-r1-28", "2.1-references", "course/modules/M/M5/project.html:500-512; references/references.json", "PASS",
  "tools/verify_refs.py --offline (out/verify_refs_offline.out): '560 entries, 0 problems'. Both keys (abbott2015understanding, rudin1976principles) are present in references/references.json. The reading section states that no passage locator is checked and attributes nothing to them (line 500-512)."),
 ("M5-d-r1-29", "2.6-lint-and-types", "course/modules/M/M5/grader; tests/labs/M5; ledgers/M5; repository", "PASS",
  "Repository gate, as CLAUDE.md states it: ruff check . -> 'All checks passed!' (out/ruff_check_repo_r4.out, rc 0); ruff format --check . -> '553 files already formatted' (out/ruff_format_repo_r4.out, rc 0). The extend-exclude list (mutants, scripts, alternatives) is respected by the repo gate; passing those paths explicitly lints them and is not the gate. mypy --no-incremental (repo): 'Success: no issues found in 385 source files' (out/mypy_no_incremental.out). pytest -q -k M5: pass (out/pytest_M5_k.out)."),
 ("M5-d-r1-30", "2.9-structure", "course/modules/M/M5/project.html:40-49, 223-250, 270-281, 283-288, 491-498", "PASS",
  "All sections of the brief (Setting-to-Limitations, Appendix A with A1-A4) are present; every href anchor used on the page exists (#brief, #conventions, #grader-section, #report, #rubric, #self-assessment, #spec, #stretch, index.html#placement, L07/L08/L09 anchors, review.html). Checked with a grep of id attributes."),
 ("M5-d-r1-31", "2.6-instance-simulated", "course/modules/M/M5/grader/instance.py:3; project.html:229", "PASS",
  "Same evidence as M5-d-r1-25: the instance is generated from the seed and labelled SIMULATED."),
 ("M5-d-r1-32", "2.2-interpretive-claims", "course/modules/M/M5/project.html:156, 219, 389", "PASS",
  "Line 156 (Lab 1 interpretation): 'It holds here, and one pair cannot prove it for every pair' matches the single-pair contraction line in the Lab 1 expected block (line 142-155, 'holds: True'). Line 219 (Lab 2): 'the lab shows one pair at or below the bound and proves nothing else' matches the ratio line. Line 389 (Lab 3): 'The printed values ... say nothing about any other grid' matches the lab's scope. Lab 1's 'agree to nine decimals in this run' matches the printed 0.000000950 and 0.000000950."),
 ("M5-d-r2-33", "2.6-mutation-new-survivor", "ledgers/M5/mutants/d3_01_feasibility_allows_a_tie_tolerance_of_1e-12.py; course/modules/M/M5/grader/test_project.py:444-460", "PASS",
  "out/mutate_M5_0-9_with_r4.out: KILLED by test_successor_within_a_tie_tolerance_above_the_resources_is_infeasible (seed 0)."),
 ("M5-d-r2-34", "2.6-mutation-new-survivor", "ledgers/M5/mutants/d3_02_first_point_bound_checked_only_for_longer_grids.py; course/modules/M/M5/grader/test_project.py:721-726", "PASS",
  "out/mutate_M5_0-9_with_r4.out: KILLED by test_grid_must_be_nonempty_positive_strictly_increasing_and_start_at_most_one[one-point-first-above-one] (seed 0)."),
 ("M5-d-r2-35", "2.6-mutation-new-killed", "ledgers/M5/mutants/d3_03_value_is_the_penultimate_iterate_when_the_budget_runs_out.py", "PASS",
  "out/mutate_M5_0-9_with_r4.out: KILLED by test_the_first_sweep_starts_from_zero_and_is_synchronous[0] (seed 0)."),
 ("M5-d-r2-36", "2.6-dag", "course/modules/M/M5/project.html concept links (contraction-mapping, value-function-iteration) and prose references; curriculum/curriculum.json M5 prereqs", "PASS",
  "tools/check_dag.py --unit M5: PASS (out/check_dag_M5.out). Link targets exist: L07.html#def-contraction-mapping and L09.html#def-value-function-iteration (dfn ids found in those lessons). Reading claims: M5 L01, L02, L04, L07 are completeness, sequences/Cauchy, metric spaces, contraction; M1 Lesson 6 (geometric-series, finite geometric sum) exists. The Bellman operator is introduced in M5 L08 (the page refers to it by name in the conventions)."),
 ("M5-d-r2-37", "2.6-spec-completeness", "course/modules/M/M5/project.html:223-250", "PASS",
  "Conventions and Constraints name the inputs, returns (value, iterations, certified_error, converged), stopping rule, budget and invalid inputs; each named condition has a grader test (see M5-d-r1-21)."),
 ("M5-d-r2-38", "2.6-atlas-studio", "curriculum/curriculum.json (M5 entry); plans/M5-build-plan.md:402", "PASS",
  "curriculum.json M5: hours 130, project title 'Contraction-mapping solver' with grading 'both'. tools/check_projects.py --unit M5: PASS (out/check_projects_M5.out). The studio entry is unchanged since the round-3 pin."),
 ("M5-d-r3-39", "2.6-mutation-new-survivor", "ledgers/M5/mutants/r3_01_operator_clamps_each_image_at_zero.py; course/modules/M/M5/grader/test_project.py:121-141", "PASS",
  "Fixed in round 3 (fixer added negative vectors to test_operator_matches_its_definition, uniform(-3, 3)). Re-run: out/mutate_M5_0-9_with_r4.out: KILLED by test_operator_matches_its_definition[0] (seed 0)."),
 ("M5-d-r3-40", "2.6-mutation-new-survivor", "ledgers/M5/mutants/r3_02_continuation_uses_absolute_value.py; course/modules/M/M5/grader/test_project.py:121-141", "PASS",
  "Same test change as row 39. Re-run: KILLED by test_operator_matches_its_definition[0] (seed 0)."),
 ("M5-d-r3-41", "2.6-mutation-new-survivor", "ledgers/M5/mutants/r3_03_feasibility_tie_tolerance_of_1e-14.py; course/modules/M/M5/grader/test_project.py:463-479", "PASS",
  "Fixed in round 3 (new test test_feasibility_is_exact_with_no_tie_tolerance_at_the_last_bit, successor math.nextafter(0.5, 1.0)). Re-run: KILLED by test_feasibility_is_exact_with_no_tie_tolerance_at_the_last_bit (seed 0)."),
 ("M5-d-r3-42", "2.6-rubric-observable-exclusive", "course/modules/M/M5/project.html:404-412 (rubric cells; C5 row)", "FAIL",
  "The round-3 level boundaries (C1, C2, C4, C5, C6) are fixed: each now has an explicit level-3 or level-2 boundary. One gap remains in C5: level 4 requires every number printed with its unit, the instance and the tolerance, and the line named; level 3 requires every number printed and the tolerance stated, with at least one line reference missing. A report whose numbers are all printed with tolerance and line references, but one number has no unit, matches no C5 level. LOW (presentation of the rubric, not a blocking kind).",
  ),
 ("M5-d-r3-43", "2.6-exemplar-descriptor-exclusivity", "course/modules/M/M5/project.html:420-482 (annotations)", "UNVERIFIABLE",
  "Not verified by this verifier: the annotation reasons are exemplar scoring material. Checking them against the descriptors would be scoring, which the task and ruling 23 assign to the dedicated blind scorer. The round-3 complaint text was changed in this slice's delta, but this verifier does not assert the annotations are correct.",
  ),
 ("M5-d-r4-44", "2.6-alternatives-five-pass", "ledgers/M5/alternatives/alt1..alt5 (synchronous, different styles); ledgers/M5/alternatives/not_accepted/", "PASS",
  "ledgers/M5/scripts/M5-d-r4/alt_seeds_r4.py (out/alt_seeds_0-49.out): alt1_functional_reduce_and_tuples 50/50; alt2_class_with_precomputed_feasible_tables 50/50; alt3_comprehension_with_feasible_index_lists 50/50; alt4_bisect_for_feasible_successors 50/50 (bisect_right on the sorted grid); alt5_reverse_order_synchronous_sweep 50/50. Five styles pass seeds 0-49 (ruling 10). The two not_accepted files fail 0/50 (first failure: test_certified_error_is_beta_over_one_minus_beta_times_the_last_change[1-0], the certified-error formula test; their README gives the synchronous and stop-rule reasons)."),
 ("M5-d-r4-45", "2.6-grader-docstring-claim", "course/modules/M/M5/grader/test_project.py:559-562 (test_stop_uses_the_largest_absolute_change_over_the_grid)", "PASS",
  "The docstring says the change at the last grid point alone certifies tol one sweep before the sup-norm change. Recomputed (out/stop_claim_r4.out): sup-norm stop at sweep 170, last-point-only stop at sweep 169. The tolerance is 0.10 % below the sweep-169 certificate (1.01297e-11) and 14.5 % above the sweep-170 certificate (8.649e-12): all four float orderings of the certificate stop at 170 (out/tie_margin_r4.out), so the test is not sensitive to the evaluation order."),
 ("M5-d-r4-46", "2.6-new-student-error-mutants", "ledgers/M5/mutants/r4_01..r4_04 (four new student-error mutants written this round)", "PASS",
  "r4_01 Euclidean norm for the change (killed by test_certified_error_is_beta_over_one_minus_beta_times_the_last_change); r4_02 (1-beta)/beta factor (killed by test_certified_error_bounds_the_distance_to_the_fixed_point[0]); r4_03 continuation at the next grid point (killed by test_operator_matches_its_definition[0]); r4_04 sqrt(k**alpha) - k' (killed by test_operator_matches_its_definition[0]). None sits at a tolerance boundary (ruling 25): each changes a behaviour the page states (the sup norm at Conventions 'Certified error', the factor, the continuation term, the utility). Note for the architect: d3_01, r3_03 and the one-ulp test are feasibility tie-tolerance mutants; the page states exact feasibility (k' <= k**alpha), so they are not sub-accuracy equivalents, but ruling 25 can be read to exclude them."),
 ("M5-d-r4-47", "2.6-lab-comparator-absolute-tolerance", "course/modules/M/M5/project.html:373 (Lab 3 expected block, data-tolerance 1e-6); :215 (Lab 2); :142 (Lab 1); course/assets/js/labs.js:50", "FAIL",
  "labs.js compares numeric tokens by |actual - expected| <= tol*(1+|expected|) with tol 1e-6, which is an absolute check for values this small. Lab 3 prints 9.226e-11, 1.025e-11, 9.226e-12 and Lab 2 prints 9.495e-07 and 1.055e-07: any value in [-1e-6, 1e-6] passes those tokens, so the browser and run_labs cannot tell a correct certified error from 0. The sweep-count tokens are still exact, so no wrong stop is accepted. Lab statements are not false (the labs are demonstrations, ruling 11), but a 'graded instantly' claim on the completion line rests on this check. LOW. Fix: use a relative check for scientific-notation tokens (or a smaller data-tolerance for those blocks, after confirming Pyodide and CPython print identical digits).",
  ),
 ("M5-d-r4-48", "2.6-mutation-full-rerun", "ledgers/M5/mutants/ (135 files); tools/mutate_graders.py --unit M5 --seeds 0-9", "PASS",
  "out/mutate_M5_0-9_with_r4.out: 135 of 135 KILLED, rc 0, 'mutate_graders M5: PASS (135/135 killed)'. No survivor, so no equivalent proof is needed. ledgers/M5/equivalent/ does not exist and no equivalent is claimed."),
 ("M5-d-r4-49", "2.9-process-words", "course/modules/M/M5/project.html (learner text)", "PASS",
  "grep -i for round, fixer, verifier, builder, ruling, slice, mutant, rubric-round, architect, ledger in project.html: 0 hits."),
]

non_pass = [r for r in ROWS if r[3] != "PASS"]
rows = []
for rid, check, loc, status, evidence, *rest in ROWS:
    row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": evidence}
    if status != "PASS":
        fix_map = {
            "M5-d-r1-06": "Architect amends plans/M5-build-plan.md:304 and plans/M5-open-items.md decision 3 to the synchronous-only contract (the five passing alternatives satisfy ruling 10), or restores an in-place sweep by changing project.html:244-245 and the first-sweep test. No grader change is needed for the alternatives.",
            "M5-d-r1-13": "Blind scorer (ruling 23) scores exemplar A from the stripped memo prose and compares with the official scores; this verifier does not score.",
            "M5-d-r1-14": "Blind scorer (ruling 23) scores exemplar B from the stripped memo prose; this verifier does not score.",
            "M5-d-r3-42": "In project.html rubric C5, make level 4 require only the printed line and tolerance (drop 'with its unit, the instance'), or add to level 3 'or a number has no unit'. Keep the rest of the cells.",
            "M5-d-r3-43": "Blind scorer (ruling 23) checks the annotations against the rubric, as part of scoring the exemplars; this verifier does not.",
            "M5-d-r4-47": "In labs.js or the page, compare scientific-notation tokens with a relative tolerance (|x-y| <= tol*|y|), or set a smaller data-tolerance on the Lab 2 and Lab 3 blocks after confirming identical output across runtimes.",
        }
        row["fix"] = fix_map[rid]
    rows.append(row)

frag = {
    "unit": "M5",
    "slice": "d",
    "round": 4,
    "verifier": "Haiku independent verifier (round 4), no build context; exemplar scoring not performed (ruling 23)",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "8196077d5f56c3919d33e69888176d197d378ad4",
    "checkout": str(CHECKOUT),
    "scratch": str(CHECKOUT / "ledgers/M5/scripts/M5-d-r4"),
    "verified_at": now,
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta from the round-3 pin 8196077d to edbb7aa8 read in full for slice d: project.html (lines 50-53 Rung 1 prose, 232 grading mode 100 to 101 checks, 244-248 conventions unchanged, 401-412 rubric caption and cells, 436-476 annotations), grader/test_project.py (+24 lines: negative vectors at line 131, nextafter test at 463-479), mutants r3_01..r3_03, alternatives unchanged, plans/M5-open-items.md (round-2 fixer section).",
        "Gates run this round (outputs under ledgers/M5/scripts/M5-d-r4/out/): run_graders M5 0-49 PASS; mutate_graders M5 0-9 135/135 killed; alt_seeds 0-49 (5 pass 50/50, 2 rejected 0/50); check_pages, check_dag, check_projects M5 PASS; run_labs M5 project 3/3 and all 13/13; page_smoke project PASS (includes the in-browser grader on 101 tests); ruff check and ruff format on the M5 scope PASS; mypy --no-incremental PASS (385 files); pytest -k M5 PASS; verify_refs --offline 0 problems; collect-only 101.",
        "Ruling 26 classification: blocking kinds (false math, missing hypothesis, wrong number, over-graded claim, failing gate, surviving non-equivalent mutant, lab statement the code does not support) found none. Non-blocking: M5-d-r1-06 (plan text versus page contract, architect decision), M5-d-r3-42 (rubric C5 gap, LOW), M5-d-r4-47 (absolute tolerance on scientific-notation tokens, LOW). The slice verdict is FAIL only because verifier rules make any non-PASS row fail the verdict; the three UNVERIFIABLE rows are delegated to the blind scorer.",
        "Row M5-d-r4-46: the three tie-tolerance feasibility mutants (d3_01, r3_03, the one-ulp test) are not sub-accuracy equivalents because the page states exact feasibility; they stay in mutants/ and are killed.",
        "tools/run_labs.py takes --page with the page stem (project), not a path; the first attempt with a path ran zero labs and was discarded.",
        "Background mutation run: an earlier duplicate process was killed by PID (my own, started by mistake) so that the output file is from one run only.",
    ],
    "what_not_checked": [
        "Blind exemplar scoring (rows 13, 14, 43): by ruling 23 this verifier must not score or read the annotations for scoring.",
        "Lab 3 and Lab 2 in-browser comparator behaviour beyond run_labs and page_smoke (run in Chromium on the project page only, not in the other pages).",
        "Cards: none in this slice (task says No cards).",
        "Lesson pages (L01 to L10) and the M5 hub beyond the hours arithmetic: outside slice d.",
        "Pyodide-vs-CPython floating-point digits for the printed 6-decimal values: only CPython was run here.",
        "The equivalence of the synchronous-only page to plans/M5-build-plan.md:304 is an architect decision, not checked.",
    ],
    "summary": None,
}

n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
n_unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
frag["summary"] = (
    f"Round 4, slice d, verdict FAIL. {len(rows)} rows: PASS {n_pass}, FAIL {n_fail} "
    f"(M5-d-r1-06 non-blocking architect decision; M5-d-r3-42 LOW rubric C5 gap; M5-d-r4-47 LOW absolute tolerance on scientific tokens), "
    f"UNVERIFIABLE {n_unv} (rows 13, 14, 43: exemplar scoring delegated to the blind scorer, ruling 23). "
    f"Mutants: {len(mutants)} total, {sum(1 for m in mutants if m['killed_by'])} killed, 0 survivors; 4 new student-error mutants written this round (r4_01..r4_04). "
    f"Alternatives: alt1..alt5 pass seeds 0-49 at 50/50 each. Reference passes 50/50 seeds. Blocking-kind defects: none found."
)
frag["notes"] = [n for n in frag["notes"]]

out_path = CHECKOUT / "ledgers/M5/M5-d.json"
out_path.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out_path, len(rows), "rows", len(mutants), "mutants")
