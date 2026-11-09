"""Build the round-2 fragment ledgers/M5/M5-d.json from the round-2 outputs (verifier, slice d, unit M5).

The mutant list is parsed from mutate_M5_seeds0-9_with_r2.out (the gate run after the three round-2 mutants were added).
Row ids are kept from round 1 (M5-d-r1-01 .. 32); rows 33-37 are new in round 2.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
S = "ledgers/M5/scripts/M5-d-r2"

mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$")
with open(os.path.join(REPO, S, "mutate_M5_seeds0-9_with_r2.out"), encoding="utf-8") as fh:
    for line in fh:
        m = pat.match(line.rstrip("\n"))
        if not m:
            continue
        status, name, description, killer = m.groups()
        killed_by = None if killer.strip() == "None" else killer.strip()
        mutants.append({"name": name, "description": description, "killed_by": killed_by})
assert len(mutants) == 128, len(mutants)

ALT_FAIL_FIX = (
    "Choose one and make the page, the tests and plans/M5-open-items.md agree. (a) Restore open-items decision 3: "
    "project.html:244 must allow an in-place sweep and project.html:245 must accept the residual bound "
    "max|BV-V|/(1-beta) as a certified error, and the formula test test_certified_error_is_beta_over_one_minus_beta_"
    "times_the_last_change must then apply only to the synchronous solver. (b) Or replace alt1 and alt2 by two "
    "alternatives of a different style that obey project.html:244-245, pass seeds 0-49, and record the change in "
    "plans/M5-open-items.md. Then re-run run_graders --unit M5 --seeds 0-49 and check the five alternatives on seeds 0-49."
)

rows = [
    {"id": "M5-d-r1-01", "check": "2.6-autograder-reference", "location": "course/modules/M/M5/grader/reference.py",
     "status": "PASS",
     "evidence": f"tools/run_graders.py --unit M5 --seeds 0-49 exit 0, printed 'run_graders M5: PASS (reference 50/50 seeds, slowest 0.3 s)' ({S}/run_graders_M5_0-49.out)."},
    {"id": "M5-d-r1-02", "check": "2.6-instances", "location": "course/modules/M/M5/grader/instance.py",
     "status": "PASS",
     "evidence": f"{S}/d2_instances.py over seeds 0-49 against the docstring ranges (beta 0.80-0.95 step 0.01, alpha 0.30-0.70, 8-24 points, first point in [0.20,0.90], steps in [0.05,0.40], last point > 1, tol in {{1e-6,1e-8,1e-10}}, no grid point within 1e-6 of a resource level): invalid seeds []; 15 distinct betas, 27 alphas, 17 sizes; 50 of 50 distinct solved value vectors (output {S}/d2_instances.out). The 20-seed sample requirement is met by the 50 seeds."},
    {"id": "M5-d-r1-03", "check": "2.6-mutation-existing", "location": "ledgers/M5/mutants/ (125 files before round 2)",
     "status": "PASS",
     "evidence": f"tools/mutate_graders.py --unit M5 --seeds 0-9 ({S}/mutate_M5_seeds0-9_with_r2.out): 126 of 128 killed. Every mutant that existed before round 2 (the 112 original files and the 13 round-1 files) is KILLED; the only two SURVIVED lines are d3_01 and d3_02, which are new in round 2 (rows M5-d-r2-33 and -34)."},
    {"id": "M5-d-r1-04", "check": "2.6-mutation-new-killed", "location": "ledgers/M5/mutants/d1_02_continuation_reads_the_current_state.py; ledgers/M5/mutants/d1_03_value_is_the_penultimate_iterate.py",
     "status": "PASS",
     "evidence": f"{S}/mutate_M5_seeds0-9_with_r2.out: d1_02 KILLED by test_operator_matches_its_definition[0] (seed 0); d1_03 KILLED by test_certified_error_bounds_the_distance_to_the_fixed_point[0] (seed 0)."},
    {"id": "M5-d-r1-05", "check": "2.6-mutation-survivor", "location": "course/modules/M/M5/grader/test_project.py:663-692; ledgers/M5/mutants/d1_01_top_grid_point_never_a_successor.py",
     "status": "PASS",
     "evidence": f"Round 1 survivor d1_01 is now KILLED: {S}/mutate_M5_seeds0-9_with_r2.out line 1 gives 'KILLED d1_01 ... -> test_operator_uses_the_top_point_on_a_grid_inside_zero_one (seed 0)'. The new tests test_operator_uses_the_top_point_on_a_grid_inside_zero_one (test_project.py:663) and test_solver_fixed_point_on_a_grid_inside_zero_one (test_project.py:679) were read in full; both use the test's own reference (ref_sweep, ref_fixed_point)."},
    {"id": "M5-d-r1-06", "check": "2.6-alternatives", "location": "ledgers/M5/alternatives/alt1..alt5; course/modules/M/M5/project.html:244-245; plans/M5-build-plan.md:304; plans/M5-open-items.md:18",
     "status": "FAIL",
     "evidence": f"{S}/d2_run_candidate.py on seeds 0-49 ({S}/d2_alternatives_seeds0-49_counts.out): alt3 50/50 PASS, alt4 50/50 PASS, alt5 50/50 PASS; alt1 (in-place Gauss-Seidel sweep) 0/50 PASS and alt2 (residual stop with residual/(1-beta) as the bound) 0/50 PASS (failing tests are the certified-error formula tests, e.g. test_certified_error_is_beta_over_one_minus_beta_times_the_last_change[1-0]). The plan requires both as must-pass alternatives (plans/M5-build-plan.md:304 names the in-place sweep and 'stopping on ... the residual with the bound reported'; plans/M5-open-items.md:18 records decision 3 that both are accepted and says 'the five alternatives ... pass seeds 0-49', which is false at this pin). The page now states 'Each sweep is synchronous' (project.html:244) and 'No other bound is accepted' (project.html:245). Nothing in the plan's architect decisions narrows the list. The in-place bound is valid (the in-place sweep is a beta-contraction with the same fixed point, so the same certificate holds), so the page is over-constrained relative to the plan. Round 1 PASSed this row; I do not carry that PASS because the plan's required list was not compared to the page.",
     "fix": ALT_FAIL_FIX},
    {"id": "M5-d-r1-07", "check": "2.6-failure-message-leak", "location": "course/modules/M/M5/grader/test_project.py:426-441",
     "status": "PASS",
     "evidence": f"Round-1 leak fixed: the message at test_project.py:437-441 no longer names 0.4 or the 0.5 resources. {S}/d2_message_scan.py scanned all 77 expect/must_raise/fail messages (output {S}/d2_message_scan.out); each digit-bearing message names a bound, a tolerance from the test's own setup or a formula, and none quotes a computed value of the solver."},
    {"id": "M5-d-r1-08", "check": "2.6-mutant-descriptions", "location": "ledgers/M5/mutants/v11_01..v12_03",
     "status": "PASS",
     "evidence": f"The first docstring line of every mutant is an error description; the six v11/v12 files that carried the reference docstring now read e.g. 'Student-error mutant (M5 slice d round 11): utility is sqrt(k - k') while feasibility still uses k**alpha' (listed in {S}/mutate_M5_seeds0-9_with_r2.out)."},
    {"id": "M5-d-r1-09", "check": "2.6-test-count", "location": "course/modules/M/M5/project.html:235; course/modules/M/M5/grader/test_project.py",
     "status": "PASS",
     "evidence": f"project.html:235 states 98 checks; pytest --collect-only -q on test_project.py prints '98 tests collected' ({S}/collect_only_test_project.out)."},
    {"id": "M5-d-r1-10", "check": "2.6-browser-suite", "location": "course/modules/M/M5/project.html:272-281; course/assets/js/grader.js; course/assets/js/python.js",
     "status": "PASS",
     "evidence": f"tools/page_smoke.py --unit M5 --pages project: PASS, in-browser grader line 'All 98 tests pass on seed 728790743' ({S}/page_smoke_M5_project.out). grader.js:53 prints the seed derived from the workspace ID and the local command."},
    {"id": "M5-d-r1-11", "check": "2.6-rubric-observable", "location": "course/modules/M/M5/project.html:404-412 (C6 level 4 cell)",
     "status": "PASS",
     "evidence": "The C6 level-4 descriptor now requires the inequality \\(\\lVert V_n - V^{\\ast}\\rVert_\\infty \\le \\frac{\\beta}{1-\\beta}\\lVert V_n - V_{n-1}\\rVert_\\infty\\) and the fixed point V* it refers to, both observable in the page text; the level-3 descriptor is distinguishable from it."},
    {"id": "M5-d-r1-12", "check": "2.6-rubric-caption", "location": "course/modules/M/M5/project.html:404",
     "status": "PASS",
     "evidence": "The caption now reads 'scored with the self-assessment form below'; a scan of project.html for the phrase 'rule above' returns no match (python re over project.html)."},
    {"id": "M5-d-r1-13", "check": "2.6-calibration-exemplar-A", "location": "course/modules/M/M5/project.html:420-450 (exemplar A, data-scores 2,2,1,2,2,2)",
     "status": "UNVERIFIABLE",
     "evidence": f"Blind scoring was not achieved in this round. My scores from the memo prose alone are C1 2, C2 2, C3 1, C4 2, C5 2, C6 2, which match the official scores within one level. But the verdict line (project.html:422) and the annotations (project.html:436-446) were displayed in my tool output before I scored, so the scores are not blind. The prose-only extract written by the script that drops verdict lines, annotations and data-score attributes is {S}/exemplar_memo_prose_only.txt (exemplar-a part).",
     "fix": "A fresh verifier that has not read project.html:417-483 scores the prose-only extract with the rubric (project.html:401-416) and only then compares with the official scores 2,2,1,2,2,2; all six must be within one level."},
    {"id": "M5-d-r1-14", "check": "2.6-calibration-exemplar-B", "location": "course/modules/M/M5/project.html:452-482 (exemplar B, data-scores 4,4,4,4,4,3)",
     "status": "UNVERIFIABLE",
     "evidence": f"Same blinding defect as M5-d-r2 row 13. My body-only scores are C1 4, C2 4, C3 4, C4 4, C5 4, C6 3, which match the official scores; the verdict line (project.html:454) and the annotations (project.html:470-478) were visible before I scored. The prose-only extract is {S}/exemplar_memo_prose_only.txt (exemplar-b part).",
     "fix": "A fresh blind re-score from the prose-only extract, as for exemplar A; all six criteria must be within one level of 4,4,4,4,4,3."},
    {"id": "M5-d-r1-15", "check": "2.6-hours-arithmetic", "location": "course/modules/M/M5/project.html:33,258-264; course/modules/M/M5/index.html:29",
     "status": "PASS",
     "evidence": "Hours table 1+2+8+7+3+5 = 26 equals data-hours-project=26; hub split 104 lessons + 26 project = 130 (index.html:29, 39-42). My own estimate of the components: rung 1 about 1-1.5 h, rung 2 about 1.5-2.5 h, proof write-up 6-10 h, solver and 98-check suite 5-9 h, self-check 2-4 h, report revision and self-assessment 3-5 h; total 18-31 h, inside the 30% band (18.2-33.8 h)."},
    {"id": "M5-d-r1-16", "check": "2.6-labs", "location": "course/modules/M/M5/project.html:55-220,287-390; tests/labs/M5/lab-M5-project-1..3.py",
     "status": "PASS",
     "evidence": f"tools/run_labs.py --unit M5 --page project: 'run_labs M5: PASS (3/3)' ({S}/run_labs_M5_project.out). Each twin run with python -I -W error exits 0 with empty stderr ({S}/lab_project1_twin.out, lab_project2_twin.out, lab_project3_twin.out, and the .err files)."},
    {"id": "M5-d-r1-17", "check": "2.6-rung1-annotated", "location": "course/modules/M/M5/project.html:57,148-155",
     "status": "PASS",
     "evidence": "Lab 1 is a complete solution with a 'Step n' comment on each stage (resources, feasible sets, one sweep, contraction check, iteration to 1e-6, actual error); the twin output matches the page expected block (see row 16)."},
    {"id": "M5-d-r1-18", "check": "2.6-rung2-completion", "location": "course/modules/M/M5/project.html:159-222",
     "status": "PASS",
     "evidence": "Two blanks (ratio = ___, certified = ___), graded by the completed twin; run_labs passes the completion lab (row 16); check_projects M5 requires section.lab.completion and passes."},
    {"id": "M5-d-r1-19", "check": "2.6-numbers-lab3", "location": "course/modules/M/M5/project.html:289,373-388; exemplar text 432,464,466",
     "status": "PASS",
     "evidence": f"Independent recomputation {S}/d2_numbers_project.py ({S}/d2_numbers_project.out): 236 sweeps, last change 1.0251e-11, certified 9.2262e-11, a priori count 242 (own loop), residual 9.2264e-12 <= (1+beta) x certified, 200-pair largest ratio 0.9000000000000001 (<= beta+1e-12), smallest gap 0.021829, V values match Lab 3 to 6 dp. Page quotes match. Lab 1 numbers match: V1, sweep-1 change 0.826569, certified 7.439119 (9 x the unrounded change 0.8265687851715 = 7.4391190665, as printed; 9 x the rounded printed change 0.826569 would give 7.439121, which is only a rounding artefact of the display), stopping sweep 146, certified 9.495187e-7. Lab 2 ratio 0.3000000000000001."},
    {"id": "M5-d-r1-20", "check": "2.6-proof-math", "location": "course/modules/M/M5/project.html:393-399; exemplar proofs 459-466",
     "status": "PASS",
     "evidence": "I re-derived A1 (max-difference bound), A2 (coordinatewise Cauchy argument on R^m), A3 (uniqueness and convergence via A1 and the geometric sum) and A4 (d_{n+j} <= beta^j d_n, sum beta/(1-beta)) from the brief's hypotheses. Each conclusion holds under the listed hypotheses. Also re-derived: the feasibility claim (k_1 feasible from every state, since k^alpha >= k >= k_1 for k <= 1 and k^alpha > 1 >= k_1 for k > 1), and that the a priori count is a valid stopping bound (cert_n <= beta^n sqrt(k_m^alpha)/(1-beta))."},
    {"id": "M5-d-r1-21", "check": "2.6-named-invalid-inputs", "location": "course/modules/M/M5/project.html:240-248; course/modules/M/M5/grader/test_project.py:557-705",
     "status": "FAIL",
     "evidence": f"project.html:248 names 'a grid ... whose first point exceeds 1' as invalid. The parametrized invalid-grid test (test_project.py:616-651) has no one-point case with a first point above 1, so the named condition is untested for one-point grids: the mutant d3_02 (first-point check only for len(points) > 1) is accepted by the suite on seeds 0-9 ({S}/d2_new_mutants_seeds0-9.out) and returns value [-inf] from solve on grid [1.5] where the reference raises ValueError ({S}/d2_probe_survivors.out). All other named conditions have a must_raise test in both directions.",
     "fix": "Add [1.5] (one point, first point above 1) to the parametrized list in test_grid_must_be_nonempty_positive_strictly_increasing_and_start_at_most_one (test_project.py:616-651) with the id 'one-point-first-above-one'. Re-run run_graders --unit M5 --seeds 0-49, mutate_graders --unit M5 --seeds 0-9 (d3_02 must then be KILLED), and the five alternatives."},
    {"id": "M5-d-r1-22", "check": "2.6-starter-signatures", "location": "course/modules/M/M5/grader/starter.py:18,23; grader/reference.py:94,101; project.html:231",
     "status": "PASS",
     "evidence": "Starter and reference signatures are identical: bellman_operator(params, grid, values) and solve(params, grid, tol, max_iter), matching project.html:231. The starter fails all 98 tests (QF_SEED=0 pytest on starter.py as contraction_solver.py: '98 failed')."},
    {"id": "M5-d-r1-23", "check": "2.6-time-limit", "location": "course/modules/M/M5/project.html:233; course/assets/js/python.js:4,36",
     "status": "PASS",
     "evidence": "python.js:4 sets TIMEOUT_MS = 120000 and python.js:36 stops the runtime after it, matching 'A run in your browser stops after 120 seconds'."},
    {"id": "M5-d-r1-24", "check": "2.6-notation", "location": "course/modules/M/M5/project.html (all math); notation/notation.json",
     "status": "PASS",
     "evidence": "Commands on the page: \\R (registered macro, real numbers), \\mathcal, \\lVert/\\rVert, \\sup, \\max, \\mathrm, \\ast, \\alpha, \\beta (standard or locally defined in the conventions, as notation.json's preamble allows). Registered symbols T, \\Phi, \\gamma_3, R^\\ast and R^{e\\ast} do not occur on the page. Letters used: B, V, W, k, k', m, n, c, u, a, b, d, i, j; none is a registered symbol. Non-blocking note: Lab 2's hypothesis writes the operator as plain B in '\\sup|BV-BW|' while the conventions define \\mathcal{B}; same meaning, different typography."},
    {"id": "M5-d-r1-25", "check": "2.8-simulated-label", "location": "course/modules/M/M5/project.html:37,227,495,502; grader/instance.py:3",
     "status": "PASS",
     "evidence": "instance.py:3 'All values are SIMULATED.'; project.html:229 'All of it is SIMULATED: generated parameters, not data.'; the page has no dataset (no data-files attribute, check_pages data-files rule passes)."},
    {"id": "M5-d-r1-26", "check": "2.8-data-manifest", "location": "course/modules/M/M5/project.html; course/assets/data/market/MANIFEST.json",
     "status": "PASS",
     "evidence": "The project reads no snapshot: no data-files attribute on any project lab; the page's Inputs entry says 'No data file.' (project.html:229). Nothing to rebuild."},
    {"id": "M5-d-r1-27", "check": "2.8-figures", "location": "course/modules/M/M5/project.html",
     "status": "PASS",
     "evidence": "grep for <svg and <img in project.html returns 0 matches; no figures to check."},
    {"id": "M5-d-r1-28", "check": "2.1-references", "location": "course/modules/M/M5/project.html:500-512; references/references.json",
     "status": "PASS",
     "evidence": f"tools/verify_refs.py --unit M5 (live): '2 of 560 entries, 0 problems' ({S}/verify_refs_M5_live.out). tools/verify_refs.py --offline: '560 entries, 0 problems' ({S}/verify_refs_offline_all.out). Reading-list keys abbott2015understanding and rudin1976principles exist in the registry (used_by M5). The page attributes no statement to either source."},
    {"id": "M5-d-r1-29", "check": "2.6-lint-and-types", "location": "course/modules/M/M5/grader; tests/labs/M5",
     "status": "PASS",
     "evidence": f"ruff check . exit 0 ('All checks passed!', {S}/ruff_check.out); ruff format --check . exit 0 (553 files, {S}/ruff_format.out); ruff check and format --check on the grader and lab twins exit 0 ({S}/ruff_scoped.out); mypy --no-incremental: 'Success: no issues found in 385 source files' ({S}/mypy.out); pytest on tests/test_labs.py, test_memo_exemplars.py, test_page_checks.py, test_run_labs.py (-k M5 or lab/page/exemplar): exit 0 ({S}/pytest_M5_relevant.out)."},
    {"id": "M5-d-r1-30", "check": "2.9-structure", "location": "course/modules/M/M5/project.html:40-49,223-250,270-281,283-288,491-498",
     "status": "PASS",
     "evidence": f"Ladder, rungs 1-2, specification with conventions, hours table, autograder panel, local run, report with three labs and brief, rubric with two exemplars and self-assessment, stretch, reading, references, all present in order. tools/check_projects.py --unit M5: PASS ({S}/check_projects_M5.out). tools/check_pages.py --unit M5: PASS ({S}/check_pages_M5.out)."},
    {"id": "M5-d-r1-31", "check": "2.6-instance-simulated", "location": "course/modules/M/M5/grader/instance.py:3; project.html:229",
     "status": "PASS",
     "evidence": "instance.py docstring: 'All values are SIMULATED.' and 'Nothing here is a real economy, a real parameter or market data.'; project.html:229 labels the grader instance SIMULATED."},
    {"id": "M5-d-r1-32", "check": "2.2-interpretive-claims", "location": "course/modules/M/M5/project.html:156,219,389",
     "status": "PASS",
     "evidence": "Scope words checked one by one (only, all, every, same, exactly, always): line 156 'one pair cannot prove it for every pair' (true, one pair is one pair); line 219 'the supremum ... over all pairs of distinct vectors' (the definition of the best Lipschitz constant); line 389 'the printed values ... say nothing about any other grid' (scoped). The 'at most beta' ratio claim is compared with beta up to 1e-12, as the page says."},
    {"id": "M5-d-r2-33", "check": "2.6-mutation-new-survivor", "location": "ledgers/M5/mutants/d3_01_feasibility_allows_a_tie_tolerance_of_1e-12.py; course/modules/M/M5/grader/test_project.py:409-423",
     "status": "FAIL",
     "evidence": f"Round-2 mutant d3_01 (feasibility accepts successors up to 1e-12 above k**alpha) SURVIVED all 98 tests on every seed 0-9 ({S}/mutate_M5_seeds0-9_with_r2.out line 14; {S}/d2_new_mutants_seeds0-9.out). It violates project.html:242 ('k' is feasible from k when c >= 0, that is, when k' <= k^alpha'), which is an exact test. The only near-tie test uses a successor 1e-10 above the resources, which the 1e-12 tolerance also refuses. Probe: bellman_operator({{beta 0.5, alpha 0.5}}, [0.25, 0.5+5e-13], [0, 1e6]) returns [0.5, 500000.4551] by the reference, while the mutant raises ValueError from sqrt of a negative number ({S}/d2_probe_survivors.out). A suite that catches it must include a successor within 1e-12 above the resources.",
     "fix": "Add a test to test_project.py next to test_successor_just_above_the_resources_is_infeasible: p = {'beta': 0.5, 'alpha': 0.5}, grid = [0.25, 0.5 + 5e-13] (or math.nextafter(0.5, 1.0)), values = [0.0, 1.0e6]; expect the first entry of bellman_operator to be 0.5 within 1e-12, with the message naming feasibility as exact (k' <= k**alpha, no tolerance). Then re-run mutate_graders --unit M5 --seeds 0-9 (d3_01 must be KILLED) and run_graders --unit M5 --seeds 0-49."},
    {"id": "M5-d-r2-34", "check": "2.6-mutation-new-survivor", "location": "ledgers/M5/mutants/d3_02_first_point_bound_checked_only_for_longer_grids.py; course/modules/M/M5/grader/test_project.py:616-651",
     "status": "FAIL",
     "evidence": f"Round-2 mutant d3_02 (first-point-at-most-one check runs only for grids with two or more points) SURVIVED all 98 tests on seeds 0-9 ({S}/mutate_M5_seeds0-9_with_r2.out line 15). It violates project.html:248 ('whose first point exceeds 1' is invalid). Probe: solve({{beta 0.9, alpha 0.5}}, [1.5], 1e-6, 5) returns {{'value': [-inf], 'certified_error': nan, 'converged': False}} by the mutant, while the reference raises ValueError ({S}/d2_probe_survivors.out).",
     "fix": "Add [1.5] (one-point grid, first point above 1) to the invalid-grid parametrization, as in M5-d-r1-21. Then mutate_graders --unit M5 --seeds 0-9 must report d3_02 KILLED."},
    {"id": "M5-d-r2-35", "check": "2.6-mutation-new-killed", "location": "ledgers/M5/mutants/d3_03_value_is_the_penultimate_iterate_when_the_budget_runs_out.py",
     "status": "PASS",
     "evidence": f"d3_03 (value is the penultimate iterate when the budget runs out) is KILLED by test_the_first_sweep_starts_from_zero_and_is_synchronous[0] (seed 0) ({S}/mutate_M5_seeds0-9_with_r2.out line 16). The kill is incidental (a one-sweep budget); no test checks the value's gap to V* on a budget-exhausted run, so the gap is recorded as a coverage note, not a failure: project.html:244-246 says value is the vector the certified error refers to."},
    {"id": "M5-d-r2-36", "check": "2.6-dag", "location": "course/modules/M/M5/project.html concept links and links; curriculum/curriculum.json M5 prereqs",
     "status": "PASS",
     "evidence": f"check_dag.py --unit M5: PASS ({S}/check_dag_M5.out). Closure of M5 computed from curriculum/curriculum.json: M1, M2, P0.1. Concept links on the page: contraction-mapping (L07.html#def-contraction-mapping, anchor exists) and value-function-iteration (L09.html#def-value-function-iteration, anchor exists); the page does not use the term or link 'bellman-equation'. M1 Lesson 6 (geometric sum, L06.html) is named in prose and M1 is in the closure. L08.html link in the stretch section exists."},
    {"id": "M5-d-r2-37", "check": "2.6-spec-completeness", "location": "course/modules/M/M5/project.html:223-250",
     "status": "PASS",
     "evidence": "Clarifying questions I would have needed: none that block. Inputs (instance from make_instance), outputs (module, dict keys, report files), error conditions (named list), budget (max_iter, a priori count), stopping and converged definitions and the Lab 3 print lines are all stated. Open point, not blocking: the in-place and residual conventions (row M5-d-r1-06)."},
    {"id": "M5-d-r2-38", "check": "2.6-atlas-studio", "location": "curriculum/curriculum.json; plans/M5-build-plan.md:30, 402",
     "status": "PASS",
     "evidence": "No atlas key on the project and no Atlas milestone names M5 (plans/M5-build-plan.md:30 and :402). Not a studio. The check_projects atlas branch does not apply."},
]

fragment = {
    "unit": "M5",
    "slice": "d",
    "round": 2,
    "verifier": "Haiku independent verifier (round 2), no build context; blinding caveat on rows 13-14",
    "pin": "9294b914a51647c66d2dee62c4a112c76ba04900",
    "base": "aeb512b65b7774b59b84f836a13984fcfe9d0d1f",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS2-M5-d",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyS2-M5-d/ledgers/M5/scripts/M5-d-r2",
    "verified_at": "2026-11-09T04:41:06+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round 2 of slice d (project.html, grader, project labs, mutants, alternatives) at pin 9294b914; delta from round-1 pin aeb512b6 read in full: project.html (lines 158-160, 232-242, 405-411, 492-498), grader/test_project.py (436-441 message, new tests 663-692), mutants d1/d2 (new in the delta), v11/v12 (descriptions changed), tests/labs/M5 L02/L09 (not in this slice).",
        "Round-1 rows 05, 07, 08, 11, 12 are resolved and re-verified. Round-1 row 06 is re-opened: its PASS assumed the page's conventions matched the plan's required alternatives; they do not (row M5-d-r1-06).",
        "Blinding defect (rows 13-14): the official scores and annotations were visible in tool output before my scoring. My body-only scores agree within one level, but the calibration is recorded UNVERIFIABLE, as the ruling requires a blind, script-extracted score. The prose-only extract is in the scratch directory.",
        "tools/mutate_graders.py --unit M5 --seeds 0-9 exits 1 with 126 of 128 killed; survivors d3_01 and d3_02 (rows 33-34). tools/run_graders.py --unit M5 --seeds 0-49 exits 0 (reference 50/50).",
        "tools/check_pages.py --unit M5 --page project is not a valid project-page check (it applies lesson rules and fails on every project); the unit-level run passes and is recorded.",
        "page_smoke.py --pages takes page stems: 'project', not 'project.html'. A first run with 'project.html' matched no page and printed a vacuous PASS, so it was discarded.",
        "Interpretation note on the in-place bound: the in-place sweep G satisfies |G(V)_i - V*_i| <= beta * max(||G(V)_{<i} - V*||, ||V_{>=i} - V*||), hence ||G(V) - V*|| <= beta ||V - V*||; with V = V_n this gives ||V_{n+1} - V*|| <= beta/(1-beta) ||V_{n+1} - V_n||, so the certificate of the page holds for the in-place sweep as well (my derivation, not a page claim).",
        "Stretch item 'prove that the in-place bound is valid' is therefore well posed.",
    ],
    "summary": "Round 2, slice d, verdict FAIL: 38 rows (PASS 32, FAIL 4, UNVERIFIABLE 2). Failing: alternatives (only 3 of 5 pass seeds 0-49), two surviving grader mutants (feasibility tie tolerance 1e-12; one-point grid with first point above 1) and the matching untested named invalid input, and the non-blind calibration of both exemplars (UNVERIFIABLE). Mutants: 128, killed 126.",
}

out_path = os.path.join(REPO, "ledgers/M5/M5-d.json")
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
print("rows", len(rows), counts, "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
