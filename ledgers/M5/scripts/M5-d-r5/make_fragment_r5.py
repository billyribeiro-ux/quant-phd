import json, re, ast, pathlib, datetime, sys
REPO = pathlib.Path(sys.argv[1]); S = REPO / "ledgers/M5/scripts/M5-d-r5"; O = S / "out"
mut_out = (O / "mutate_M5_0-9.out").read_text(encoding="utf-8").splitlines()
killed = {}
for ln in mut_out:
    m = re.match(r"KILLED (\S+?\.py): .* -> (.+)$", ln)
    if m:
        killed[m.group(1)] = m.group(2).strip()
r5 = {
 "r5_01_resources_are_capital_below_one.py": "test_operator_matches_its_definition[0] (seed 0; 10/10 seeds killed)",
 "r5_02_value_is_the_bellman_image.py": "test_the_first_sweep_starts_from_zero_and_is_synchronous[0] (seed 0; 10/10 seeds killed)",
 "r5_03_utility_splits_the_root_of_the_difference.py": "test_operator_matches_its_definition[0] (seed 0; 10/10 seeds killed)",
}
killed.update(r5)
mutants = []
for f in sorted((REPO / "ledgers/M5/mutants").glob("*.py")):
    doc = ast.get_docstring(ast.parse(f.read_text(encoding="utf-8"))) or ""
    desc = " ".join(doc.split())
    mutants.append({"name": f.name, "description": desc, "killed_by": killed.get(f.name, "")})
assert all(m["killed_by"] for m in mutants), [m["name"] for m in mutants if not m["killed_by"]]
CARRY4 = "Carried from round 4 (%s byte-identical since the previous pin edbb7aa8): "
rows = [
 ("M5-d-r1-01","2.6-autograder-reference","course/modules/M/M5/grader/reference.py","PASS",
  "Fresh: tools/run_graders.py --unit M5 --seeds 0-49 -> 'run_graders M5: PASS (reference 50/50 seeds, slowest 0.3 s)' (out/run_graders_M5_0-49.out, rc 0). Scratch workspace with reference.py as contraction_solver.py: QF_SEED=0 pytest --assert=plain -W error test_project.py -> 101 passed; --collect-only -> 101 tests. reference.py has no diff since edbb7aa8."),
 ("M5-d-r1-02","2.6-instances","course/modules/M/M5/grader/instance.py","PASS",
  CARRY4 % "grader/instance.py" + "round 4 ran ledgers/M5/scripts/M5-d-r2/d2_instances.py under python -I: invalid seeds [], 15 betas, 27 alphas, 17 sizes, 50 distinct solved vectors; docstring ranges (lines 5-12) match code (lines 44-53). Not re-run this round; the file is unchanged."),
 ("M5-d-r1-03","2.6-mutation-existing","ledgers/M5/mutants/ (138 files at this pin: 135 existing incl. r4_01..r4_04, plus r5_01..r5_03)","PASS",
  "Fresh: tools/mutate_graders.py --unit M5 --seeds 0-9 -> 'mutate_graders M5: PASS (135/135 killed)', rc 0 (out/mutate_M5_0-9.out, 135 KILLED lines). The three new r5 mutants killed on 10/10 seeds each (out/new_r5_mutants_seeds0-9.out; scripts/M5-d-r5/kill.py)."),
 ("M5-d-r1-04","2.6-mutation-new-killed","ledgers/M5/mutants/d1_02_continuation_reads_the_current_state.py; d1_03_value_is_the_penultimate_iterate.py","PASS",
  CARRY4 % "mutants d1_02 and d1_03 and grader/test_project.py" + "both still KILLED in the fresh run (out/mutate_M5_0-9.out)."),
 ("M5-d-r1-05","2.6-mutation-survivor","course/modules/M/M5/grader/test_project.py:739-753; ledgers/M5/mutants/d1_01_top_grid_point_never_a_successor.py","PASS",
  CARRY4 % "grader/test_project.py and mutant d1_01" + "d1_01 KILLED in the fresh run (out/mutate_M5_0-9.out)."),
 ("M5-d-r1-06","2.6-alternatives","ledgers/M5/alternatives/ (alt1..alt5 pass); plans/M5-build-plan.md:304-306; plans/M5-open-items.md:18-20; course/modules/M/M5/project.html:244","FAIL",
  "Fresh: scripts/M5-d-r5/alt_seeds_r5.py -> alt1..alt5 50/50 seeds each; not_accepted/alt1_gauss_seidel_in_place.py 0/50 and not_accepted/alt2_residual_stop.py 0/50 (out/alt_seeds_0-49.out). The conflict is unchanged at this pin: plans/M5-build-plan.md:304-306 lists the in-place (Gauss-Seidel) sweep and the residual stop as must-pass alternatives; plans/M5-open-items.md:18-20 (decision 3) accepts them; project.html:244 states 'Each sweep is synchronous' and defers the in-place sweep to Rung 4. grep M5 in plans/FINAL-ARCHITECT-RULINGS.md returns nothing, so no ruling resolves it.",
  "Architect decision needed. Either amend the page contract (project.html:244) to admit the in-place sweep and the residual-bound stop, restate the formula test per solver, and move the two not_accepted files back; or amend plans/M5-build-plan.md:304-306 and plans/M5-open-items.md decision 3 so that they are not must-pass. Non-blocking under ruling 26; the row stays FAIL until ruled."),
 ("M5-d-r1-07","2.6-failure-message-leak","course/modules/M/M5/grader/test_project.py (every expect/must_raise/pytest.fail message)","PASS",
  CARRY4 % "grader/test_project.py" + "the file is unchanged; the --assert=plain sentence at project.html:280 is unchanged; a failing run in scratch printed only the test's own message (e.g. 'Failed: bel...')."),
 ("M5-d-r1-08","2.6-mutant-descriptions","ledgers/M5/mutants/ (138 files)","PASS",
  "Fresh: ast.get_docstring on all 138 mutant files: every file has a non-empty description (script run in this checkout). Every description is copied into the fragment mutants list."),
 ("M5-d-r1-09","2.6-test-count","course/modules/M/M5/project.html:235 ('Grading mode', 101 checks); grader/test_project.py","PASS",
  "Fresh: pytest --collect-only -q test_project.py -> '101 tests collected'; the reference passes 101 (see M5-d-r1-01). project.html:235 says 'runs 101 checks'."),
 ("M5-d-r1-10","2.6-browser-suite","course/modules/M/M5/project.html:272-281; course/assets/js/grader.js:34-61,53; course/assets/js/store.js; course/assets/js/py-worker.js:111","PASS",
  "project.html:272 says the code 'is saved in this browser as you type': grader.js:34 loads and :61 saves the draft through store.js (IndexedDB) on a 400 ms timer. grader.js:53 prints the local command with QF_SEED, which matches project.html:279. py-worker.js:111 runs pytest.main with -p no:cacheprovider --assert=plain -W error. page_smoke (out/page_smoke_M5_project.out): 'in-browser grader: All 101 tests pass'."),
 ("M5-d-r1-11","2.6-rubric-observable","course/modules/M/M5/project.html:404-412 (rubric cells C1-C6)","PASS",
  "Fresh: all six rows re-read after the delta. The only changed cell is C5 (line 410): level 4 no longer requires the unit and the instance, so the level-4 descriptor is 'every number printed, tolerance stated, every line named', level 3 is 'every number printed, tolerance stated, one line reference missing', level 2 is '1-3 numbers not printed, or a number without its tolerance', level 1 is '4 or more not printed'. The bands are disjoint and cover every case; the round-3 gap (M5-d-r3-42) is closed. The other rows are unchanged."),
 ("M5-d-r1-12","2.6-rubric-caption","course/modules/M/M5/project.html:403-404","PASS",
  "Fresh: caption at line 403 reads 'six criteria, four levels each, scored with the self-assessment form below. Where a passage fits two cells, score the lower level. The report meets the bar at level 3 or above on every criterion.' The table has six criteria and four levels, and the form is at project.html:483 (id self-assessment, data-rubric=rubric)."),
 ("M5-d-r1-13","2.6-calibration-exemplar-A","course/modules/M/M5/project.html:419-449 (data-scores 2,2,1,2,2,2); ~/.fanout/blind/M5-d.json (blind scores A 2,1,1,2,2,1)","PASS",
  "Calibration by the dedicated blind scorer (ruling 23): ~/.fanout/blind/M5-d.json gives A = [2,1,1,2,2,1] for C1..C6. Official data-scores at project.html:419 are 2,2,1,2,2,2. Differences are 0,1,0,0,0,1, each within one level. Not scored by this verifier. See notes on the KNOWN-ISSUES record."),
 ("M5-d-r1-14","2.6-calibration-exemplar-B","course/modules/M/M5/project.html:451-481 (data-scores 4,4,4,4,4,3); ~/.fanout/blind/M5-d.json (blind scores B 4,3,4,3,3,3)","PASS",
  "Calibration by the dedicated blind scorer (ruling 23): ~/.fanout/blind/M5-d.json gives B = [4,3,4,3,3,3]. Official data-scores at project.html:451 are 4,4,4,4,4,3. Differences are 0,1,0,1,1,0, each within one level."),
 ("M5-d-r1-15","2.6-hours-arithmetic","course/modules/M/M5/project.html:33, 258-264; course/modules/M/M5/index.html:29, 39-42, 131; curriculum/curriculum.json (M5 hours 130)","PASS",
  "Fresh: project table rows 1+2+8+7+3+5 = 26 (line 264 total 26; 26/130 = 20.0 %); data-hours-project=26 at project.html:33. Hub index.html:29 data-hours-lessons=104, data-hours-project=26, so 104+26=130 = curriculum M5 hours 130. Lesson data-hours (L01..L10): 10,10,10,10,10,10 for L01-L06 and 11,11,11,11 for L07-L10, summing to 104 (hub line 131 says six at 10 and four at 11)."),
 ("M5-d-r1-16","2.6-labs","course/modules/M/M5/project.html:55-220, 287-390; tests/labs/M5/lab-M5-project-1..3.py","PASS",
  "Fresh: tools/run_labs.py --unit M5 --page project -> 'run_labs M5: PASS (3/3)'. Each twin run under python -I -W error exits 0. Lab 1 and Lab 3: page code equals twin (scripts/M5-d-r5/extract.py; only a trailing newline differs), and output equals the expected block exactly (out/lab1_twin_output.txt vs lab1_expected.txt; lab3 likewise). Lab 2: page differs from the completed twin only at the two '___' blanks (by design); the filled page code gives output equal to its expected block (out/lab2_filled_output.txt)."),
 ("M5-d-r1-17","2.6-rung1-annotated","course/modules/M/M5/project.html:57, 58-155","PASS",
  "Fresh (scripts/M5-d-r5/numbers.py -> out/numbers_lab1_lab2.out): resources 0.707107, 0.948683, 1.183216; V1 = (0.455090, 0.669838, 0.826569); 0.409581 <= 0.743912; first change 0.8265688 -> 0.826569 and certified 7.4391191 -> 7.439119; stop at sweep 146 with certified 9.4951874e-7 < 1e-6; actual error 9.4951777e-7 <= certified 9.4951874e-7, both printed 0.000000950 at nine decimals. All match the hypothesis text. Tolerance changed to 1e-15 at project.html:142; output still exact."),
 ("M5-d-r1-18","2.6-rung2-completion","course/modules/M/M5/project.html:159-222","PASS",
  "Fresh: filled Lab 2 (scripts/M5-d-r5/lab2_fill.py) -> ratio = 0.300000 (0.3 exactly, out/numbers_lab1_lab2.out), sweeps 146, certified 9.4951874e-7 -> '9.495e-07', last change 1.0550208e-7 -> '1.055e-07'. Filled output equals the expected block (out/lab2_filled_output.txt vs lab2_expected.txt)."),
 ("M5-d-r1-19","2.6-numbers-lab3","course/modules/M/M5/project.html:289, 293-298, 365, 373-388","PASS",
  "Fresh (scripts/M5-d-r5/numbers3.py -> out/numbers_lab3.out): gap 0.021828872 (> 1e-6, 'clear of a tie: True'); 236 sweeps; last change 1.0251355e-11; certified 9.2262198e-11; a priori count 242 (U = sqrt(2.7^0.3) = 1.160659); 236 <= 243; residual 9.2263974e-12 <= (1+beta) x certified = 1.753e-10; worst ratio over 200 pairs with random.Random(7) = 0.900000000000000, worst - beta = 1.1e-16, so 'at most beta up to a rounding margin of 1e-12' is true and the code (twin line 'worst <= BETA + 1e-12') matches the new wording; V(k) values match the expected block to 6 dp. Tolerance 1e-15 at project.html:372 accepts the exact output."),
 ("M5-d-r1-20","2.6-proof-math","course/modules/M/M5/project.html:393-399 (brief A1-A4); Conventions 244-248","PASS",
  "Re-derived: A1 from |max f - max g| <= max|f - g| over one feasible set, which depends only on k; k_1 is feasible from every state (k <= 1: k^alpha >= k >= k_1 uses alpha < 1; k > 1: k^alpha > 1 >= k_1). A2 finite grid, coordinatewise limit. A3 from A1, A2 and V_0 = 0. A4 from d_{n+j} <= beta^j d_n with d_n = ||V_n - V_{n-1}||. Budget claim (line 247): d_n <= beta^{n-1}||V_1|| <= beta^{n-1} U with U = sqrt(k_m^alpha), so certified_n <= beta^n U/(1-beta), which is <= tol at n = a priori count; the page's 'count plus one' is a valid weaker statement."),
 ("M5-d-r1-21","2.6-named-invalid-inputs","course/modules/M/M5/project.html:240-248; grader/reference.py:34-78; grader/test_project.py:618-785 (carried)","PASS",
  "Fresh: each named condition on project.html:248 has a branch in reference.py: beta/alpha not a finite real or boolean, or outside (0,1) (_real, _params, lines 24-42); tol not finite or not > 0 (_tolerance, 73-78); max_iter not a whole number >= 1, bool or float refused (_budget, 66-70); grid empty, non-positive, not strictly increasing, first point > 1 (_grid, 45-56); values length (_values, 59-63). The test file part is carried from round 4 (byte-identical since edbb7aa8)."),
 ("M5-d-r1-22","2.6-starter-signatures","course/modules/M/M5/grader/starter.py:18,23; grader/reference.py:94,101; project.html:231","PASS",
  "Fresh: starter.py:18 'def bellman_operator(params, grid, values)'; starter.py:23 'def solve(params, grid, tol, max_iter)'; reference.py:94 and 101 match. reference.py:123-128 returns value, iterations, certified_error, converged, as project.html:231 states."),
 ("M5-d-r1-23","2.6-time-limit","course/modules/M/M5/project.html:233; course/assets/js/python.js:4","PASS",
  "Fresh: python.js:4 'const TIMEOUT_MS = 120000' = 120 seconds, the figure at project.html:233."),
 ("M5-d-r1-24","2.6-notation","course/modules/M/M5/project.html (all math, 187 spans); notation/notation.json","PASS",
  "Fresh: registry symbols are T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}; macros include \\R = \\mathbb{R} (real numbers). Math in project.html uses \\R (registered meaning), \\mathcal{B}, \\ast, \\lVert, \\rVert, \\sup, \\max, \\sqrt, \\sum, \\mathrm and module-local letters (B, V, W, k, a, b, c, d, i, j, m, n, u, alpha, beta). No registered symbol is used with another meaning; the registry 'about' text says alpha, beta, m and similar letters are local to each lesson."),
 ("M5-d-r1-25","2.8-simulated-label","course/modules/M/M5/project.html:229; course/modules/M/M5/grader/instance.py:3, 41, 56","PASS",
  "project.html:229: 'All of it is SIMULATED: generated parameters, not data.' instance.py:3 'All values are SIMULATED.', :56 label 'SIMULATED' (instance.py byte-identical since edbb7aa8)."),
 ("M5-d-r1-26","2.8-data-manifest","course/modules/M/M5/project.html (no data-files attribute)","PASS",
  "Fresh: grep for data-files in project.html returns nothing; the three project labs open no data file and have no data-files attribute."),
 ("M5-d-r1-27","2.8-figures","course/modules/M/M5/project.html","PASS",
  "Fresh: grep for figure, svg and figures- in project.html returns nothing; the page has no live figure."),
 ("M5-d-r1-28","2.1-references","course/modules/M/M5/project.html:500-512; references/references.json","PASS",
  "Fresh: data-cite abbott2015understanding and rudin1976principles at project.html:503-504 resolve to keys at references/references.json:51 and :20391; the M5 curriculum sources list the same two works. check_pages M5 PASS (out/check_pages_M5.out)."),
 ("M5-d-r1-29","2.6-lint-and-types","course/modules/M/M5/grader; tests/labs/M5; ledgers/M5; repository","PASS",
  "Fresh: ruff check . -> 'All checks passed!' rc 0; ruff format --check . -> '554 files already formatted' rc 0 (ledgers/*/mutants, alternatives and scripts are excluded in pyproject.toml extend-exclude); mypy --no-incremental -> 'Success: no issues found in 385 source files' rc 0; pytest -q tests -k M5 -> 13 passed rc 0 (tests/test_labs.py: 13)."),
 ("M5-d-r1-30","2.9-structure","course/modules/M/M5/project.html:40-49, 223-250, 270-281, 283-288, 491-498","PASS",
  "Fresh: sections present in order: ladder (#ladder, 40-49), rungs (#rungs, 51-221 with labs 1 and 2), spec (#spec, 223-250: Context, Inputs, Required outputs, Constraints, Grading mode, Conventions), hours (#hours), grader (#grader-section, 270-281), local (#local, 276-281), report (#report, 283-488: Lab 3, brief, rubric, exemplars, self-assessment), stretch (#stretch, 490-497), reading (#reading), references."),
 ("M5-d-r1-31","2.6-instance-simulated","course/modules/M/M5/grader/instance.py:3; project.html:229","PASS",
  "Fresh: project.html:229 and the instance.py lines in M5-d-r1-25. The three project labs read no data file (see M5-d-r1-26)."),
 ("M5-d-r1-32","2.2-interpretive-claims","course/modules/M/M5/project.html:156, 219, 389","PASS",
  "Fresh: line 156 'The stopping sweep is 146, and the certified error at that sweep is about 9.5e-07 ... agree to nine decimals in this run' matches out/numbers_lab1_lab2.out. Line 219 '9.495e-07 is the same unrounded value, 9.495187e-7, that Lab 1 prints as 0.000000950' matches 9.4951874e-7. Line 389 'the printed values ... say nothing about any other grid' is a scope limit and is not contradicted."),
 ("M5-d-r2-33","2.6-mutation-new-survivor","ledgers/M5/mutants/d3_01_feasibility_allows_a_tie_tolerance_of_1e-12.py; course/modules/M/M5/grader/test_project.py:444-460","PASS",
  CARRY4 % "mutant d3_01 and grader/test_project.py" + "KILLED in the fresh run (out/mutate_M5_0-9.out)."),
 ("M5-d-r2-34","2.6-mutation-new-survivor","ledgers/M5/mutants/d3_02_first_point_bound_checked_only_for_longer_grids.py; course/modules/M/M5/grader/test_project.py:721-726","PASS",
  CARRY4 % "mutant d3_02 and grader/test_project.py" + "KILLED in the fresh run (out/mutate_M5_0-9.out)."),
 ("M5-d-r2-35","2.6-mutation-new-killed","ledgers/M5/mutants/d3_03_value_is_the_penultimate_iterate_when_the_budget_runs_out.py","PASS",
  CARRY4 % "mutant d3_03" + "KILLED in the fresh run (out/mutate_M5_0-9.out)."),
 ("M5-d-r2-36","2.6-dag","course/modules/M/M5/project.html:37, 227, 494, 501 (concept links and prose); curriculum/curriculum.json (M5 prereqs ['M2']; M2 prereqs ['M1'])","PASS",
  "Fresh: check_dag M5 PASS (out/check_dag_M5.out). Concept links resolve: L07.html#def-contraction-mapping (1 match) and L09.html#def-value-function-iteration (1 match). Prose: Lessons 1, 2, 4, 7 of M5 (completeness, Cauchy sequences, metric spaces, contraction) are in the unit; the M1 Lesson 6 finite geometric sum (M1/L06.html:36, 90) is in the prerequisite closure M5 -> M2 -> M1; the L08 link is in the unit."),
 ("M5-d-r2-37","2.6-spec-completeness","course/modules/M/M5/project.html:223-250","PASS",
  "Fresh: the spec states inputs (no data file, the seeded instance, SIMULATED), outputs (contraction_solver.py with bellman_operator and solve; report/run_report.py, report.md, self_assessment.md), constraints, grading mode, and conventions (state space, feasibility, utility, operator, iteration, certified error, stopping, budget, invalid inputs). Each named symbol and signature is defined in the spec or the conventions."),
 ("M5-d-r2-38","2.6-atlas-studio","curriculum/curriculum.json (M5 entry); plans/M5-build-plan.md:402","PASS",
  "Fresh: the M5 curriculum entry has no atlas key, project title 'Contraction-mapping solver', grading 'both'. plans/M5-build-plan.md:402 says no Atlas entry names M5 and no atlas contract is needed. Both files are unchanged since the previous pin."),
 ("M5-d-r3-39","2.6-mutation-new-survivor","ledgers/M5/mutants/r3_01_operator_clamps_each_image_at_zero.py; course/modules/M/M5/grader/test_project.py:121-141","PASS",
  CARRY4 % "mutant r3_01 and grader/test_project.py" + "KILLED in the fresh run (out/mutate_M5_0-9.out)."),
 ("M5-d-r3-40","2.6-mutation-new-survivor","ledgers/M5/mutants/r3_02_continuation_uses_absolute_value.py; course/modules/M/M5/grader/test_project.py:121-141","PASS",
  CARRY4 % "mutant r3_02 and grader/test_project.py" + "KILLED in the fresh run (out/mutate_M5_0-9.out)."),
 ("M5-d-r3-41","2.6-mutation-new-survivor","ledgers/M5/mutants/r3_03_feasibility_tie_tolerance_of_1e-14.py; course/modules/M/M5/grader/test_project.py:463-479","PASS",
  CARRY4 % "mutant r3_03 and grader/test_project.py" + "KILLED in the fresh run (out/mutate_M5_0-9.out)."),
 ("M5-d-r3-42","2.6-rubric-observable-exclusive","course/modules/M/M5/project.html:404-412 (rubric C5 row, line 410)","PASS",
  "Previous FAIL (M5-d-r3-42: a report with every number printed and tolerance and line references, but one number without a unit, matched no C5 level). Fixed at line 410: level 4 now needs every number printed, the tolerance stated, and every line named; level 3 needs every number printed and the tolerance stated, with at least one line reference missing. The unit and instance requirement is gone, so the C5 bands are exclusive and exhaustive. Integer counts such as '236 sweeps' carry the tolerance through the instance sentence, which is how exemplar B (official C5 = 4, project.html:465) reads the descriptor."),
 ("M5-d-r3-43","2.6-exemplar-descriptor-exclusivity","course/modules/M/M5/project.html:419-482 (annotations); ~/.fanout/blind/M5-d.json","PASS",
  "Calibration row (ruling 23). Blind scores in ~/.fanout/blind/M5-d.json are A [2,1,1,2,2,1] and B [4,3,4,3,3,3]; official scores are A 2,2,1,2,2,2 and B 4,4,4,4,4,3 (project.html:419, 451). Each criterion is within one level. The Meets/Misses labels in the annotations (lines 436-478) match the level text of the rubric as it now reads (lines 406-411); the C5 note at line 475 names the instance as well, which the level-4 descriptor no longer requires, a surplus that does not contradict it."),
 ("M5-d-r4-44","2.6-alternatives-five-pass","ledgers/M5/alternatives/alt1..alt5 (synchronous, different styles); ledgers/M5/alternatives/not_accepted/","PASS",
  "Fresh: scripts/M5-d-r5/alt_seeds_r5.py -> alt1..alt5 50/50 seeds each, first failure None; not_accepted alt1 and alt2 0/50 (out/alt_seeds_0-49.out). The alternatives directory is unchanged since the previous pin."),
 ("M5-d-r4-45","2.6-grader-docstring-claim","course/modules/M/M5/grader/test_project.py:559-562 (test_stop_uses_the_largest_absolute_change_over_the_grid)","PASS",
  CARRY4 % "grader/test_project.py" + "the docstring claim is unchanged; the reference's change at reference.py:118 is the largest absolute entry, as the docstring says."),
 ("M5-d-r4-46","2.6-new-student-error-mutants","ledgers/M5/mutants/r4_01..r4_04 (round 4); r5_01..r5_03 (this round)","PASS",
  "The four round-4 mutants are KILLED in the fresh run (out/mutate_M5_0-9.out). Three new student-error mutants this round (r5_01 resources read as capital below one; r5_02 value returned as the operator image; r5_03 utility sqrt(k^alpha) - sqrt(k')) are each killed on 10/10 seeds (out/new_r5_mutants_seeds0-9.out)."),
 ("M5-d-r4-47","2.6-lab-comparator-absolute-tolerance","course/modules/M/M5/project.html:142, 215, 372 (data-tolerance 1e-15); course/assets/js/labs.js:50","PASS",
  "Previous FAIL (data-tolerance 1e-6 accepted 9.226e-11 for 0). Fixed: data-tolerance is 1e-15 on all three expected blocks. labs.js:50 accepts a token when |a-e| <= tol*(1+|e|), so a certified error of 0 against 9.226e-11 is now rejected (difference 9.2e-11 > 1e-15). The reference outputs are exact string matches (M5-d-r1-16), so the tighter check accepts the correct output. Printed 6-dp values are at least 2.5e-8 from a rounding boundary (scripts/M5-d-r5/boundary.py), so CPython/Pyodide ulp differences cannot change printed digits. The in-browser lab run was not executed (see what_not_checked)."),
 ("M5-d-r4-48","2.6-mutation-full-rerun","ledgers/M5/mutants/ (138 files); tools/mutate_graders.py --unit M5 --seeds 0-9","PASS",
  "Fresh: mutate_graders M5 0-9 -> 135/135 killed (existing set) and the three new r5 mutants 10/10 seeds each. Seeds 10-49 were not run for mutants (the gate is seeds 0-9)."),
 ("M5-d-r4-49","2.9-process-words","course/modules/M/M5/project.html (learner text)","PASS",
  "Fresh: learner-text scan for round, fixer, verifier, builder, ruling, slice, architect, ledger, audit, delta, fragment, blind, scorer, previous: no hit in learner text. The only matches are the L09 'Previous' navigation link (line 514) and the hours row 'Report revision' (a task name)."),
]
out_rows = []
for r in rows:
    if len(r) == 6:
        rid, check, loc, status, ev, fix = r
    else:
        rid, check, loc, status, ev = r; fix = None
    row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = fix
    out_rows.append(row)
ids = [r["id"] for r in out_rows]
assert len(ids) == len(set(ids)) == 49, len(ids)
prev = json.load(open("/Users/billyribeiro/.fanout/frags/S-M5-d.round4.json"))
assert [r["id"] for r in prev["rows"]] == ids, "row ids differ from round 4"
counts = {s: sum(1 for r in out_rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
  "unit": "M5", "slice": "d", "round": 5,
  "verifier": "Haiku independent verifier (round 5), no build context; exemplar scores from the dedicated blind scorer (ruling 23), not from this verifier",
  "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
  "base": "8196077d5f56c3919d33e69888176d197d378ad4",
  "delta_from": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
  "checkout": str(REPO), "scratch": str(S),
  "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
  "verdict": "FAIL" if counts["FAIL"] or counts["UNVERIFIABLE"] else "PASS",
  "rows": out_rows,
  "mutants": mutants,
  "registry_flags": [], "freshness_flags": [],
  "notes": [
    "Delta edbb7aa8..dde0486b for slice d: course/modules/M/M5/project.html (15 lines: data-tolerance 1e-6 -> 1e-15 at lines 142, 215, 372; Lab 3 hypothesis wording 'up to a rounding margin of 10^-12' at line 289; Lab 3 docstring reflow at 293-294 with the same code; rubric C5 cell line 410 without the unit and instance requirement); tests/labs/M5/lab-M5-project-3.py (docstring reflow only, code unchanged); ledgers/M5/mutants/r4_01..r4_04 (four mutant files now at the pin). grader/, alternatives/, lab-M5-project-1/2 twins, labs.js, tools/ and notation/ are unchanged since edbb7aa8. Lab twins tests/labs/M5/lab-M5-L05-1.py and lab-M5-L08-1.py changed in the delta but are outside slice d.",
    "KNOWN-ISSUES record: the task text says the M5 calibration is 'accepted by the architect and recorded in plans/KNOWN-ISSUES.md'. At the pin, plans/KNOWN-ISSUES.md has no M5 entry (grep M5 empty; the file lists only E3 rows), and plans/FINAL-ARCHITECT-RULINGS.md has no M5 ruling. The calibration rows are PASS on the blind file alone; the architect acceptance and the KNOWN-ISSUES record are not verifiable in this checkout.",
    "ledgers/M5/M5-d.json already existed at the pin (round 12 content from another run); it is overwritten here with round 5 as instructed.",
    "Rubric C5 reading: 'a number is given without its tolerance' is read as applying to floating-point results under the stated instance tolerance (1e-10), the reading exemplar B's official C5 = 4 uses. If the architect reads it per-number, integer counts would force level 2; recorded as an interpretation, not a row.",
    "Non-blocking classification (ruling 26): M5-d-r1-06 is a plan-versus-page contract conflict awaiting the architect; no blocking kind found this round.",
  ],
  "summary": "Round 5, slice d, verdict FAIL. 49 rows: PASS %d, FAIL %d (M5-d-r1-06 only: plan/page contract conflict on the in-place sweep, architect decision needed), UNVERIFIABLE %d. Previous FAILs now PASS: M5-d-r3-42 (rubric C5 fixed), M5-d-r4-47 (tolerance 1e-15). Calibration rows M5-d-r1-13, -14, r3-43 PASS on ~/.fanout/blind/M5-d.json. Mutants: 138 total, 138 killed (135 existing 0-9 seeds; 3 new r5 on 10/10 seeds). Alternatives alt1..alt5 50/50; not_accepted 0/50. Repo ruff check and format, mypy strict-no-incremental, pytest -k M5, verify_refs --offline, check_pages/dag/projects, run_labs, run_graders, page_smoke all PASS." % (counts["PASS"], counts["FAIL"], counts["UNVERIFIABLE"]),
  "what_not_checked": [
    "In-browser (Pyodide) execution of the three project labs; the tolerance argument relies on the printed-digit margin analysis, not a browser run.",
    "Mutants on seeds 10-49 (gate is 0-9); alternatives were run on 0-49.",
    "Exemplar annotations were not scored by this verifier (ruling 23); calibration is the blind file.",
    "Architect acceptance of calibration and the KNOWN-ISSUES record (absent at the pin).",
    "verify_refs live run (offline only, per the M5 gate).",
  ],
}
path = REPO / "ledgers/M5/M5-d.json"
path.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", path, counts, "mutants", len(mutants))
