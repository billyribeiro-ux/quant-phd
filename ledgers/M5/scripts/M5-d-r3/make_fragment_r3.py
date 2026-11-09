"""Round 3, slice d: build ledgers/M5/M5-d.json from the verifier's rows and the mutation output (run from the checkout).

Usage: python3 -I make_fragment_r3.py <checkout-root>. Mutant descriptions and kill records are parsed from
ledgers/M5/scripts/M5-d-r3/out/mutate_M5_0-9_with_r3.out, the output of tools/mutate_graders.py --unit M5 --seeds 0-9.
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
S = "ledgers/M5/scripts/M5-d-r3/out/"

mutants = []
for line in (root / S / "mutate_M5_0-9_with_r3.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    verdict, name, description, killed = m.groups()
    killed_by = None if verdict == "SURVIVED" else killed.strip()
    mutants.append({"name": name, "description": description.strip(), "killed_by": killed_by})

R = []


def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)


row("M5-d-r1-01", "2.6-autograder-reference", "course/modules/M/M5/grader/reference.py", "PASS",
    f"tools/run_graders.py --unit M5 --seeds 0-49 (rc 0): 'run_graders M5: PASS (reference 50/50 seeds, slowest 0.3 s)' ({S}run_graders_M5_0-49.out). "
    "Reference also passes all 100 checks on seed 0 in a scratch workspace (reference copied to contraction_solver.py).")

row("M5-d-r1-02", "2.6-instances", "course/modules/M/M5/grader/instance.py", "PASS",
    f"Re-run this round: ledgers/M5/scripts/M5-d-r2/d2_instances.py (unchanged, run with python3 -I): invalid seeds [], 15 betas, 27 alphas, 17 sizes, "
    f"50 of 50 distinct solved vectors (output {S}instances_recheck_r3.out). instance.py is byte-identical to the round-2 pin "
    "(git diff 9294b914..8196077d lists no change to it). Docstring ranges (beta 0.80-0.95, alpha 0.30-0.70, 8-24 points, tol set) match the code at lines 44-53.")

row("M5-d-r1-03", "2.6-mutation-existing", "ledgers/M5/mutants/ (all 128 files present before round 3)", "PASS",
    f"tools/mutate_graders.py --unit M5 --seeds 0-9 re-run on the pin: every one of the 128 pre-round-3 mutants is KILLED ({S}mutate_M5_0-9.out: 128/128). "
    f"The later run with the three new mutants ({S}mutate_M5_0-9_with_r3.out) kills the same 128; the only survivors are the three new rows M5-d-r3-39..41.")

row("M5-d-r1-04", "2.6-mutation-new-killed", "ledgers/M5/mutants/d1_02_continuation_reads_the_current_state.py; ledgers/M5/mutants/d1_03_value_is_the_penultimate_iterate.py", "PASS",
    f"{S}mutate_M5_0-9_with_r3.out: d1_02 KILLED by test_operator_matches_its_definition[0] (seed 0); d1_03 KILLED by test_certified_error_bounds_the_distance_to_the_fixed_point[0] (seed 0).")

row("M5-d-r1-05", "2.6-mutation-survivor", "course/modules/M/M5/grader/test_project.py:663-692; ledgers/M5/mutants/d1_01_top_grid_point_never_a_successor.py", "PASS",
    f"{S}mutate_M5_0-9_with_r3.out: d1_01 KILLED by test_operator_uses_the_top_point_on_a_grid_inside_zero_one (seed 0); test_project.py:719-733 read in full.")

row("M5-d-r1-06", "2.6-alternatives", "ledgers/M5/alternatives/alt1..alt5; course/modules/M/M5/project.html:244-245; plans/M5-build-plan.md:304; plans/M5-open-items.md:18 and 113-130", "FAIL",
    f"Alternatives now pass: ledgers/M5/scripts/M5-d-r3/alt_seeds_r3.py on seeds 0-49 ({S}alt_seeds_0-49.out): alt1_functional 50/50, alt2_class 50/50, alt3_comprehension 50/50, "
    "alt4_bisect 50/50, alt5_reverse_order 50/50, reference 50/50. The round-1 in-place and residual alternatives are in ledgers/M5/alternatives/not_accepted/ and fail 0/50. "
    "But the plan still requires them: plans/M5-build-plan.md:304 lists 'in-place (Gauss-Seidel) sweep' and 'stopping on the certified bound and on the residual with the bound reported' "
    "among the five alternatives that must pass, and that line is unchanged at this pin. The page now binds the solver to synchronous sweeps (project.html:244, 'Each sweep is synchronous'), "
    "so the in-place alternative is excluded by the page. The fixer's note (plans/M5-open-items.md:113-130) records the change and says 'the architect may still choose to amend the page contract', "
    "so the plan deviation is not ratified by anyone with architect authority.",
    "Architect ratifies the synchronous-only contract (project.html:244-245 as written) and amends plans/M5-build-plan.md:304 so that the in-place sweep and the residual-bound stop are stretch "
    "items, recorded in plans/M5-open-items.md; or, if the in-place sweep is to be a must-pass alternative, restore it by changing project.html:244 and the formula test scope. "
    "No grader change is needed for either option: the five alternatives in ledgers/M5/alternatives/ pass seeds 0-49.")

row("M5-d-r1-07", "2.6-failure-message-leak", "course/modules/M/M5/grader/test_project.py:40-54 and every expect/must_raise message", "PASS",
    f"Re-run: ledgers/M5/scripts/M5-d-r2/d2_message_scan.py on the current file ({S}message_scan_recheck_r3.out): 79 messages scanned. "
    "Digits that appear are bounds, tolerances or the test's own inputs (for example 1e-12, 5e-13, 1e-10), never a computed solver value. "
    f"Observed with --assert=plain on a wrong solution (ledgers/M5/mutants/m68): 'E   Failed: <message>' only, with 'All traceback entries are hidden'; no expected value printed.")

row("M5-d-r1-08", "2.6-mutant-descriptions", "ledgers/M5/mutants/ (131 files)", "PASS",
    f"{S}mutate_M5_0-9_with_r3.out prints each mutant's first docstring line. I read all 131: each names a student error (for example m14 'returns a stored answer whenever beta, alpha and the grid size match seed 0'). "
    "The three new mutants' first lines name their error (r3_01, r3_02, r3_03).")

row("M5-d-r1-09", "2.6-test-count", "course/modules/M/M5/project.html:235; course/modules/M/M5/grader/test_project.py", "PASS",
    f"project.html:235 quotes 100 checks. pytest --collect-only in a scratch workspace with reference.py as contraction_solver.py: '100 tests collected' ({S}collect_only_workspace_reference_r3.out). "
    f"The collect-only run inside the grader directory fails with 'Interrupted: 1 error during collection' because contraction_solver.py is absent there ({S}collect_only_suite.out); that is a missing-module artefact of the command, not a page defect.")

row("M5-d-r1-10", "2.6-browser-suite", "course/modules/M/M5/project.html:272-281; course/assets/js/grader.js:53; course/assets/js/py-worker.js:111", "PASS",
    "py-worker.js:111 runs pytest with '-q -p no:cacheprovider --assert=plain -W error'; grader.js:53 prints the same local command; page_smoke M5 project: 'in-browser grader: All 100 tests pass on seed 2089745084' "
    f"({S}page_smoke_project.out). python.js:4 TIMEOUT_MS = 120000 matches the 120 s statement at project.html:233.")

row("M5-d-r1-11", "2.6-rubric-observable", "course/modules/M/M5/project.html:404-412 (rubric cells)", "PASS",
    "Each level cell names an observable element (for example C6 level 4 'with the direction each moves the error'; C5 level 4 'names the printed line that each number comes from'). "
    "No cell relies on an unquantified adjective. Level-boundary coverage is a separate finding (row M5-d-r3-42).")

row("M5-d-r1-12", "2.6-rubric-caption", "course/modules/M/M5/project.html:404", "PASS",
    "Caption: 'six criteria, four levels each ... meets the bar at level 3 or above'. The table has six criteria C1-C6 with four levels each (lines 407-412).")

row("M5-d-r1-13", "2.6-calibration-exemplar-A", "course/modules/M/M5/project.html:420-450 (exemplar A, data-scores 2,2,1,2,2,2)", "UNVERIFIABLE",
    "Not scored by this verifier, by design: ruling 23 assigns blind scoring of rubric exemplars to a dedicated scorer that never opens project.html, and this verifier has read the annotations and the official scores "
    "(project.html:420-482) in this round, so it cannot score blind. Only descriptor exclusivity is reported (row M5-d-r3-43).",
    "A dedicated blind scorer (ruling 23) extracts the memo prose of exemplar A with a stripping script, scores C1-C6 from the rubric alone, and compares with 2,2,1,2,2,2 (each within one level).")

row("M5-d-r1-14", "2.6-calibration-exemplar-B", "course/modules/M/M5/project.html:452-482 (exemplar B, data-scores 4,4,4,4,4,3)", "UNVERIFIABLE",
    "Same as M5-d-r1-13: not scored here, by ruling 23; this verifier had read the annotations before this check.",
    "A dedicated blind scorer (ruling 23) scores exemplar B's stripped prose from the rubric alone and compares with 4,4,4,4,4,3 (each within one level).")

row("M5-d-r1-15", "2.6-hours-arithmetic", "course/modules/M/M5/project.html:33,258-264; course/modules/M/M5/index.html:29,39-42", "PASS",
    "Components 1+2+8+7+3+5 = 26 (project.html:258-263); total 26 at line 264 and 33. Hub: data-hours-lessons=104 + data-hours-project=26 = 130 (index.html:29), matching the curriculum M5 hours 130. "
    "Verifier's own estimate: rung 1 about 1 h, rung 2 about 1.5 h, proofs A1-A4 with the report 6-8 h, solver and tests 4-6 h, self-check 2-3 h, revision and self-assessment 3-5 h, total about 18-24 h; "
    "26 h is within 30% of that range (26 is 24% above the 21 h midpoint).")

row("M5-d-r1-16", "2.6-labs", "course/modules/M/M5/project.html:55-220,287-390; tests/labs/M5/lab-M5-project-1..3.py", "PASS",
    f"run_labs.py --unit M5 --page project: 3/3 ({S}run_labs_M5_project.out); run_labs --unit M5: 13/13 ({S}run_labs_M5_all.out). "
    f"Own comparison ({S}labs_vs_twins_r3.out): Lab 1 and Lab 3 page code equals the twin byte-for-byte; Lab 2 differs only at the two '___' blanks (diff at lines 37 and 47), "
    "the completed twin runs with rc 0 and empty stderr under python -I -W error, and each stdout equals the page's expected block (ruling 11 applies).")

row("M5-d-r1-17", "2.6-rung1-annotated", "course/modules/M/M5/project.html:57,58-155", "PASS",
    "Lab 1 code (lines 58-141) has six numbered steps, each with a comment; its expected block (142-155) equals the twin's output.")

row("M5-d-r1-18", "2.6-rung2-completion", "course/modules/M/M5/project.html:159-222", "PASS",
    "Lab 2 page code has exactly two blanks (lines 198 and 208); the completed twin fills them with the ratio and the bound lines; expected block (215-218) equals the twin's output.")

row("M5-d-r1-19", "2.6-numbers-lab3", "course/modules/M/M5/project.html:289,373-388; exemplar text 432,464,466", "PASS",
    f"Independent recomputation by the verifier from the definitions ({S}indep_numbers_r3.out): gap 0.021829, 236 sweeps, last change 1.025e-11, certified 9.226e-11, a priori 242, residual 9.226e-12, "
    "worst ratio 0.900000, V values 5.804999 ... 6.171668 all match the printed block. Rung 1 and 2 numbers match too: V1, 0.409581 <= 0.743912, sweep-1 certified 7.439119, stop sweep 146, "
    "certified 9.495187e-7 (the 'unrounded value' cited at project.html:219), last change 1.055e-7, ratio 0.300000.")

row("M5-d-r1-20", "2.6-proof-math", "course/modules/M/M5/project.html:393-399; exemplar proofs 459-466", "PASS",
    "Verifier's own proof check of A1-A4: A1 uses that both maxima range over the same feasible set (feasibility depends on k only) and |max f - max g| <= max|f - g|; "
    "A1 needs the first-point hypothesis for nonempty feasible sets (k1 <= k^alpha for every state, using alpha < 1 for k <= 1 and k1 <= 1 for k > 1, project.html:241); "
    "A4 uses d_{k+1} <= beta d_k and the limit from A3. No gap found. Exemplar proofs are not scored here (ruling 23).")

row("M5-d-r1-21", "2.6-named-invalid-inputs", "course/modules/M/M5/project.html:240-248; course/modules/M/M5/grader/test_project.py:601-765", "PASS",
    "Each named condition (beta/alpha in (0,1) incl. bool and non-finite; tol finite and > 0; max_iter whole number >= 1 incl. bool and float; grid empty / non-positive / not strictly increasing / first point > 1; values length) "
    "has a must_raise test (lines 601-765) and a valid-side test: one-point grid [1.5] at test_project.py:679 (id one-point-first-above-one) is now present, closing the round-2 gap; "
    f"tie-tolerance refusal at 443-459 added. Mutants that exploit these gaps are killed ({S}mutate_M5_0-9_with_r3.out: d3_01, d3_02 KILLED). The three new survivors (rows 39-41) concern the operator and the tolerance, not a named invalid input.")

row("M5-d-r1-22", "2.6-starter-signatures", "course/modules/M/M5/grader/starter.py:18,23; grader/reference.py:94,101; project.html:231", "PASS",
    "starter.py defines bellman_operator(params, grid, values) and solve(params, grid, tol, max_iter), the same as reference.py:94,101 and as project.html:231 states.")

row("M5-d-r1-23", "2.6-time-limit", "course/modules/M/M5/project.html:233; course/assets/js/python.js:4,36", "PASS",
    "python.js:4 TIMEOUT_MS = 120000 and the 120 s statement agree; the suite runs in under 1 s on the reference (run_graders slowest 0.3 s).")

row("M5-d-r1-24", "2.6-notation", "course/modules/M/M5/project.html (all math); notation/notation.json", "PASS",
    "Macros used: \\R (registered), \\beta, \\alpha, \\mathcal{B} (defined locally at project.html:227 and 243 per the architect's Q1 notation ruling), \\ast, \\lVert/\\rVert, \\sqrt, \\max, \\sup, \\mathrm, \\frac, \\cdots (standard LaTeX; BUILDER_RULES 3.1 is read as project macros). "
    "No use of T for the operator (grep for T in math: none). No registered symbol is given another meaning: the symbols k, k', c, u, V, W, V_n, V^\\ast, m, n, j, d_n are local to the page.")

row("M5-d-r1-25", "2.8-simulated-label", "course/modules/M/M5/project.html:229; course/modules/M/M5/grader/instance.py:3,56", "PASS",
    "project.html:229 'All of it is SIMULATED: generated parameters, not data'; instance.py returns 'label': 'SIMULATED' (line 56) and its docstring says 'All values are SIMULATED.' (line 3).")

row("M5-d-r1-26", "2.8-data-manifest", "course/modules/M/M5/project.html (no data-files attribute)", "PASS",
    "The project reads no dataset: grep for data-files in project.html returns 0 matches, and project.html:229 says 'No data file'. Nothing to check against MANIFEST.json for this page.")

row("M5-d-r1-27", "2.8-figures", "course/modules/M/M5/project.html", "PASS",
    "grep -c '<svg' project.html = 0; the page has no chart or interactive figure. Nothing to render.")

row("M5-d-r1-28", "2.1-references", "course/modules/M/M5/project.html:500-512; references/references.json", "PASS",
    "data-cite keys abbott2015understanding and rudin1976principles exist in references/references.json (entries list, lines 51 and 20391). "
    f"The page attributes no statement to either source (project.html:502 says so). verify_refs --offline: 'offline integrity: 560 entries, 0 problems' ({S}verify_refs_offline.out).")

row("M5-d-r1-29", "2.6-lint-and-types", "course/modules/M/M5/grader; tests/labs/M5; repository", "PASS",
    f"ruff check . : 'All checks passed!' ({S}ruff_check_repo.out). ruff format --check . : '553 files already formatted' ({S}ruff_format_repo.out). "
    f"mypy --no-incremental: 'Success: no issues found in 385 source files' ({S}mypy_no_incremental.out). "
    f"A scoped ruff run that included ledgers/M5/mutants and alternatives reports E501 and format issues there ({S}ruff_check_scope.out); pyproject.toml:18 excludes those paths, so the repo-wide run is the gate.")

row("M5-d-r1-30", "2.9-structure", "course/modules/M/M5/project.html:40-49,223-250,270-281,283-288,491-498", "PASS",
    f"check_pages M5: PASS ({S}check_pages_M5.out); check_projects M5: PASS ({S}check_projects_M5.out); page_smoke M5 project: PASS, zero console errors ({S}page_smoke_project.out). "
    "Section order ladder, rungs, spec, hours, autograder, local, report, stretch, reading, references matches the project template.")

row("M5-d-r1-31", "2.6-instance-simulated", "course/modules/M/M5/grader/instance.py:3; project.html:229", "PASS",
    "The instance is seeded from the workspace seed and its label is SIMULATED; the page calls it an input, not data (project.html:229).")

row("M5-d-r1-32", "2.2-interpretive-claims", "course/modules/M/M5/project.html:156,219,389", "PASS",
    "Line 156 (Step 4 holds for one pair; A1 proves it for all pairs), line 219 (the lab shows one pair and proves nothing else), line 389 (the 200-pair check is not a proof; margin 1e-12) all match the code at project.html:84-89, 109-112 and 365-366.")

row("M5-d-r2-33", "2.6-mutation-new-survivor", "ledgers/M5/mutants/d3_01_feasibility_allows_a_tie_tolerance_of_1e-12.py; course/modules/M/M5/grader/test_project.py:443-459", "PASS",
    f"{S}mutate_M5_0-9_with_r3.out: d3_01 KILLED by test_successor_within_a_tie_tolerance_above_the_resources_is_infeasible (seed 0).")

row("M5-d-r2-34", "2.6-mutation-new-survivor", "ledgers/M5/mutants/d3_02_first_point_bound_checked_only_for_longer_grids.py; course/modules/M/M5/grader/test_project.py:679", "PASS",
    f"{S}mutate_M5_0-9_with_r3.out: d3_02 KILLED by test_grid_must_be_nonempty_positive_strictly_increasing_and_start_at_most_one[one-point-first-above-one] (seed 0).")

row("M5-d-r2-35", "2.6-mutation-new-killed", "ledgers/M5/mutants/d3_03_value_is_the_penultimate_iterate_when_the_budget_runs_out.py", "PASS",
    f"{S}mutate_M5_0-9_with_r3.out: d3_03 KILLED by test_the_first_sweep_starts_from_zero_and_is_synchronous[0] (seed 0).")

row("M5-d-r2-36", "2.6-dag", "course/modules/M/M5/project.html concept links and links; curriculum/curriculum.json M5 prereqs", "PASS",
    f"check_dag M5: PASS ({S}check_dag_M5.out). contraction-mapping links L07.html#def-contraction-mapping and value-function-iteration links L09.html#def-value-function-iteration; "
    "both definitions exist (L07.html, L09.html). 'Lessons 1, 2, 4 and 7' (project.html:502) are L01 completeness, L02 sequences, L04 metric spaces and L07 Banach, matching the page.")

row("M5-d-r2-37", "2.6-spec-completeness", "course/modules/M/M5/project.html:223-250", "PASS",
    "Questions a competent student would still ask, checked against the page: none material. Domain of V (every vector, project.html:243), the value at non-grid points (no such points; the operator is on the grid), the return type (list of floats, 244 and 231), the budget and convergence semantics (246-248) are all stated.")

row("M5-d-r2-38", "2.6-atlas-studio", "curriculum/curriculum.json (M5 entry); plans/M5-build-plan.md:402", "PASS",
    "The M5 curriculum entry has no atlas key and no atlas milestone names M5 (plans/M5-build-plan.md:402-403); the atlas-contract check does not apply to this unit.")

row("M5-d-r3-39", "2.6-mutation-new-survivor", "ledgers/M5/mutants/r3_01_operator_clamps_each_image_at_zero.py; course/modules/M/M5/grader/test_project.py:121-141 (and 144-163, 166-182)", "FAIL",
    f"{S}mutate_M5_0-9_with_r3.out: SURVIVED on all seeds 0-9 (no killing test). {S}probe_survivors_r3.out: bellman_operator(p, [0.5,0.9,1.4], [-1.0, 0.0, 0.5]) = reference [-0.4449, 0.2206, 0.5322] but mutant [0.0, 0.2206, 0.5322]. "
    "project.html:243 defines BV 'for a vector V on the grid' with no sign restriction, so the mutant violates a stated behaviour. Every bellman_operator test draws nonnegative vectors: test_project.py:130 uniform(0,3), 153-154 and 175 uniform(0,4), 210 0.5*i. "
    "Fix tested in a scratch copy only ({S}fix_check_r3.out): drawing signed values uniform(-3,3) at test_project.py:130 keeps the reference passing 10/10 seeds and kills r3_01 on 8 of 10 seeds; the five alternatives also pass 10/10 on that copy ({S}fix_check_alts_r3.out).",
    "In test_operator_matches_its_definition (test_project.py:130) draw the values from uniform(-3.0, 3.0) so that negative vectors are checked against the definition; optionally the same in test_operator_is_a_contraction_in_the_sup_norm. Then re-run mutate_graders --unit M5 --seeds 0-9 (r3_01 must be KILLED) and run_graders --unit M5 --seeds 0-49.")

row("M5-d-r3-40", "2.6-mutation-new-survivor", "ledgers/M5/mutants/r3_02_continuation_uses_absolute_value.py; course/modules/M/M5/grader/test_project.py:121-141", "FAIL",
    f"{S}mutate_M5_0-9_with_r3.out: SURVIVED on seeds 0-9. {S}probe_survivors_r3.out: with V = [-1.0, 0.0, 0.5] the reference gives [-0.4449, 0.2206, 0.5322] and the mutant (continuation beta*|V(k')|) gives [1.3551, 1.5698, 1.7266]. "
    "project.html:243 states the operator for any vector V; the suite's vectors are nonnegative (see M5-d-r3-39). Fix tested in scratch ({S}fix_check_r3.out): the same signed-vector change kills r3_02 on 9 of 10 seeds; the reference passes 10/10.",
    "The same change as M5-d-r3-39 (signed vectors in test_operator_matches_its_definition, test_project.py:130). Re-run mutate_graders --unit M5 --seeds 0-9 and require r3_02 KILLED.")

row("M5-d-r3-41", "2.6-mutation-new-survivor", "ledgers/M5/mutants/r3_03_feasibility_tie_tolerance_of_1e-14.py; course/modules/M/M5/grader/test_project.py:443-459", "FAIL",
    f"{S}mutate_M5_0-9_with_r3.out: SURVIVED on seeds 0-9. {S}probe_survivors_r3.out: from k = 0.25 with alpha 0.5 (resources exactly 0.5), a successor 0.5+5e-15 or math.nextafter(0.5, 1.0) makes the reference return [0.5, ...] (refused) while the mutant raises ValueError (a math domain error from sqrt of a negative number), "
    "and the page says feasibility is exact: 'k is feasible from k when c >= 0, that is, when k' <= k^alpha' (project.html:241). The suite's tie test uses 0.5+5e-13 (test_project.py:449), which lies outside the 1e-14 window, so the mutant is accepted. "
    f"Fix tested in scratch ({S}fix_check_r3.out): adding a test with successor math.nextafter(0.5, 1.0) expecting 0.5 kills r3_03 on 10 of 10 seeds, and the reference passes 10/10.",
    "Add to test_project.py a test with grid [0.25, math.nextafter(0.5, 1.0)] from beta 0.5, alpha 0.5, values [0.0, 1.0e6], expecting the first entry to be 0.5 within 1e-12 with the message 'feasibility is exact: no tie tolerance'. Re-run mutate_graders --unit M5 --seeds 0-9 (r3_03 must be KILLED).")

row("M5-d-r3-42", "2.6-rubric-observable-exclusive", "course/modules/M/M5/project.html:407-412 (rubric cells C1, C2, C4, C5, C6)", "FAIL",
    "Descriptor exclusivity and exhaustiveness: some passages match no level cell. C1 (line 407): a passage naming exactly one of the five elements matches no cell (level 4 needs all five, level 3 four with the fixed point identified as the grid's, level 2 two or three, level 1 none); "
    "a passage naming four without identifying the fixed point also matches none. C2 (408): a proof where every step names its property but the constant does not appear in the last line matches neither level 4 (needs the constant) nor level 3 (needs one step without its property). "
    "C4 (410): a complete derivation that shows the geometric series but does not state the sweep the solver uses matches neither level 4 nor level 3 (level 3 needs the series not shown). "
    "C5 (411): a report with three unprinted numbers out of ten matches neither level 2 ('one or two') nor level 1 ('most'; not defined for three). "
    "C6 (412): a passage naming the grid limitation with the direction of the error but no statement of the scope of the bound matches no level cell (level 4 needs the scope; level 3 needs no direction; level 2 needs one limitation and is read as the only one).",
    "Make the cells exhaustive. C1 level 1: 'Names one or none of the five, or states the operator without its domain.' C1 level 2: 'Names two or three of the five, or four without the fixed point identified as the grid's.' "
    "C2 level 3: 'Proves A1 with every step justified, but one step stated without its property or without the constant in the last line.' "
    "C4 level 3: 'Derives the bound and its constant with the geometric series shown or stated, but does not state the sweep the solver uses.' "
    "C5 level 2: 'One to three numbers quoted that run_report.py does not print, or a number given without its tolerance.' C5 level 1: 'Four or more numbers not printed by the run, or numbers quoted without a source.' "
    "C6 level 2: 'Names one limitation, or the grid limitation with its direction but no scope of the bound.'")

row("M5-d-r3-43", "2.6-exemplar-descriptor-exclusivity", "course/modules/M/M5/project.html:420-482 (annotations)", "FAIL",
    "Reported, not scored (ruling 23). Exemplar A C4 'Misses C4 level 3' (line 443) gives as its reason that the bound is 'asserted with its constant' with no derivation: that is the level-2 situation, and the level-3 cell requires a derivation, so the level-3 miss is cited with a level-2 reason. "
    "Exemplar A C5 'Misses C5 level 3' (line 445) has one valid element (the count has no printed line) and a second clause, 'the instance is not stated where the count first appears', which is not an element of the level-3 cell (level 3 turns on printed numbers and the tolerance). "
    "Exemplar B C4 'Meets level 4' (line 475) cites 'states the bound for the sweep the solver uses'; the passage (line 464) ties the bound to 'the stop' but does not state it in those words, a borderline match. "
    "All other annotations cite elements of their own cell: A C1-L2, A C2-L2 and L3-miss, A C3-L1, A C4-L2, A C5-L2, A C6-L2, B C1-C5 at level 4, B C6-L3 and B C6-L4-miss.",
    "Re-word the two misses so each cites an element of the level it names (A C4 L3: 'no derivation, so the sum is not shown' under level 2 instead, or move the reason; A C5 L3: cite 'the count of about 240 has no printed line'). Re-word B line 475 to quote the passage's own phrase ('At the stop, the bound'). Exemplar scores are not changed by this row.")


ledger = {
    "unit": "M5",
    "slice": "d",
    "round": 3,
    "verifier": "Haiku independent verifier (round 3), no build context; exemplar scoring not performed (ruling 23)",
    "pin": "8196077d5f56c3919d33e69888176d197d378ad4",
    "base": "9294b914a51647c66d2dee62c4a112c76ba04900",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS3-M5-d",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyS3-M5-d/ledgers/M5/scripts/M5-d-r3",
    "verified_at": "2026-11-09T06:40:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta from the round-2 pin 9294b914 to 8196077d read in full for slice d: project.html (lines 33-35 lede, 232-235 grading mode, 277-280 local run), grader/test_project.py (+60 lines: the one-point case at 679, tie test 443-459, __tracebackhide__ on all test functions), alternatives alt1 and alt2 (replaced) and not_accepted/, mutants d3_01..d3_03 (new in round 2), plans/M5-open-items.md (round-2 fixer section). tests/labs/M5/lab-M5-L06-1.py changed in the delta; it is outside slice d and was not verified here.",
        "Gates run this round (outputs under ledgers/M5/scripts/M5-d-r3/out/): run_graders M5 0-49 PASS; mutate_graders M5 0-9 FAIL 128/131 (the three new survivors are rows 39-41); check_pages, check_dag, check_projects, page_smoke project, run_labs project 3/3 and all 13/13, ruff repo-wide, ruff format repo-wide, mypy --no-incremental, verify_refs --offline, pytest -k M5 (13 passed). The page's collect count was taken in a scratch workspace (100).",
        "tools/check_pages.py was run unit-wide (it has no project-only mode that applies project rules); the project page passes page_smoke alone.",
        "Blind exemplar scoring was not performed by this verifier (ruling 23). This verifier read the annotations and official scores while checking descriptor exclusivity, so rows 13-14 stay UNVERIFIABLE by design.",
        "The alternatives in ledgers/M5/alternatives/ (alt1-alt5) pass seeds 0-49 at 50/50 each; the two not_accepted files fail 0/50. Row 06 is FAIL only on the plan-versus-page question (plans/M5-build-plan.md:304 still names the in-place and residual alternatives as must-pass).",
        "Scratch scripts that write to /tmp (fix_check_r3.py, fix_check_alts_r3.sh) do not touch the repository; the patched test copy is /tmp/m5d_r3_fix/patched/test_project.py and is not committed.",
        "run_gates_r3.sh has a collect-only step that runs in the grader directory and therefore fails (no contraction_solver.py there); the valid count is in out/collect_only_workspace_reference_r3.out.",
    ],
    "summary": "Round 3, slice d, verdict FAIL. 43 rows: PASS 35, FAIL 6, UNVERIFIABLE 2. Mutants: 131, killed 128. Failing: row 06 (plan-versus-page alternatives, needs architect ratification), rows 39-41 (three new surviving grader mutants: operator on negative vectors, absolute-value continuation, 1e-14 tie tolerance), row 42 (rubric level boundaries leave passages unscored), row 43 (two exemplar annotation reasons cite elements of other levels). Rows 13-14 (blind calibration) UNVERIFIABLE by design. Alternatives 1-5 pass seeds 0-49; the reference passes seeds 0-49; all numbers on the page recompute.",
}

out = root / "ledgers/M5/M5-d.json"
out.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(R), "mutants", len(mutants), "survivors", sum(1 for m in mutants if m["killed_by"] is None))
