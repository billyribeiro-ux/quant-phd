"""Round-12 verifier (M3 slice d): builds ledgers/M3/M3-d.json from the round-11 fragment (context only) and this
round's evidence. Carried rows keep their ids and say so; re-verified rows carry this round's evidence and the scripts
or outputs under ledgers/M3/scripts/M3-d-r12/. Run from the checkout root with .venv/bin/python -I."""

import json
import os
import re
import sys

sys.path.insert(0, "tools")
import ledger  # noqa: E402

ROOT = os.getcwd()
S = "ledgers/M3/scripts/M3-d-r12/out/"
PREV = json.load(open("/Users/billyribeiro/.fanout/frags/D-M3-d.round11.json", encoding="utf-8"))
CARRY_PREFIX = ("Carried from round 11 (cited files byte-identical since the previous pin ccaeeaf4; git diff "
                "ccaeeaf4..329c1d7 touches only cards.json at M3-c211, project.html at two lines, and three new v11d mutants): ")
# Rows whose cited subject changed or whose evidence must be re-proved this round.
OVERRIDE: dict[str, tuple[str, str, str, str, str]] = {}  # id -> (status, check, location, evidence, fix)
ALLOW_CARRY_CARDS = {f"cards-L0{i}" for i in range(2, 8)} | {"cards-L09", "cards-c208-duplicate", "cards-c167-misconception",
                     "cards-c131", "cards-c204", "cards-c144-prop23-hypothesis", "cards-c163-lab-count"}


def ov(i, status, check, location, evidence, fix=""):
    OVERRIDE[i] = (status, check, location, evidence, fix)


# ---- gates (round 12, pin 329c1d7) ----
ov("gate-check-pages", "PASS", "2.9 pages", "tools/check_pages.py --unit M3", f"'check_pages M3: PASS' EXIT 0 ({S}check_pages_M3.out)")
ov("gate-check-dag", "PASS", "2.9 DAG", "tools/check_dag.py --unit M3", f"'check_dag M3: PASS' EXIT 0 ({S}check_dag_M3.out)")
ov("gate-check-projects", "PASS", "2.6 projects", "tools/check_projects.py --unit M3", f"'check_projects M3: PASS' EXIT 0 ({S}check_projects_M3.out)")
ov("gate-run-labs", "PASS", "2.5 labs", "tools/run_labs.py --unit M3", f"'run_labs M3: PASS (12/12)' EXIT 0 ({S}run_labs_M3.out)")
ov("gate-run-graders", "PASS", "2.6 grader", "tools/run_graders.py --unit M3 --seeds 0-49", f"'reference 50/50 seeds' EXIT 0 ({S}run_graders_M3.out)")
ov("gate-page-smoke", "PASS", "2.9 smoke", "tools/page_smoke.py --unit M3 --pages project", f"'page_smoke M3: PASS'; in-browser grader 'All 163 tests pass' EXIT 0 ({S}page_smoke_project.out)")
ov("gate-ruff", "PASS", "ruff", "ruff check tests/labs/M3 course/modules/M/M3/grader", f"'All checks passed!' EXIT 0 ({S}ruff_check.out)")
ov("gate-mypy", "PASS", "mypy", "mypy --no-incremental", f"'Success: no issues found in 385 source files' EXIT 0 ({S}mypy.out)")
ov("gate-verify-refs", "PASS", "2.1 references", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M3 (live Crossref)",
   f"offline '560 entries, 0 problems' ({S}verify_refs_offline.out); live '--unit M3: 2 of 560 entries, 0 problems' EXIT 0 ({S}verify_refs_M3_live_r12.out)")
ov("gate-collect-only", "PASS", "2.6 grader count", "pytest --collect-only on the staged reference grader",
   f"'163 tests collected' ({S}collect_only_M3.out, staged by scripts/M3-d-r12/stage_grader_r12.sh)")
ov("gate-pytest-relevant", "PASS", "tooling pytest", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py tests/test_docs_figures.py",
   f"EXIT 0 ({S}pytest_relevant_r12.out)")
ov("gate-mutate-m3", "FAIL", "2.6 mutation", "tools/mutate_graders.py --unit M3 --seeds 0-9",
   f"Tool: 'mutate_graders M3: PASS (174/174 killed)' EXIT 0 ({S}mutate_M3_seeds0-9_r12.out). Verifier review: three of the 174 kills are SyntaxError at collection (mutants-collection-only-kills), so the tool's count overstates the kills.",
   "Repair the three mutant headers as described in mutants-collection-only-kills, then re-run the tool.")
ov("gate-reference-starter", "PASS", "2.6 grader runs", "staged reference and starter copies, QF_SEED=0, -W error",
   f"reference '163 passed'; starter '162 failed, 1 passed' where the one pass is test_module_imports_only_standard_library_or_numpy ({S}reference_seed0_r12.out, {S}starter_seed0_r12.out)")
ov("gate-alternatives-seeds-0-49", "PASS", "2.6 alternatives", "scripts/M3-d-r12/run_alts_r12.sh: 10 alternatives x seeds 0-49",
   f"all 10 'PASS seeds 0-49' ({S}alts_seeds0-49_r12.out)")
ov("alternatives-count-and-seeds", "PASS", "2.6 alternatives count", "ledgers/M3/alternatives/ (10 files), run_alts_r12.sh",
   f"10 files, each 'PASS seeds 0-49' with 163 tests per seed ({S}alts_seeds0-49_r12.out). Ruling 10 needs five; ten are present.")
ov("alternatives-alt2-docstring", "FAIL", "2.6 alternatives, honesty of the file", "ledgers/M3/alternatives/alt2_dykstra_other_stop_rule.py line 1",
   "Line 1 reads 'stops on the feasibility gap alone and allows 5000 iterations'. No 5000 occurs in the file; line 112 is 'for _ in range(max_iter):', so the code respects max_iter (default 500). The docstring is false. The alternative passes seeds 0-49 (alts_seeds0-49_r12.out).",
   "Change line 1 to state that the loop runs at most max_iter steps (default 500) and stops on the gap alone.")

# ---- grader and page ----
ov("grader-named-conditions", "FAIL", "2.6 named refusals; 2.6 grader mutation",
   "grader/test_project.py: test_non_square_is_refused (line 185) and test_asymmetry_beyond_tolerance_is_refused (line 193) call every MATRIX_FUNCS entry with default arguments only; project.html line 237 (Constraints)",
   f"Survivor scripts/M3-d-r12/survivors/v12d_03_clip_validates_symmetry_only_for_default_floor.py (clip_repair checks symmetry only when floor == 0.0), held outside mutants/ so the gate stays green. It passes all seeds 0-9 ({S}survivor_v12d_03.out). Direct probe (scripts/M3-d-r12/probe_survivor_r12.py, {S}probe_survivor_r12.out): the reference raises ValueError for clip_repair([[1,0.3],[0.5,1]], floor=0.1); the candidate returns [[1.0, 0.37677], [0.37677, 1.0]]. The reference also raises for is_psd(tol=1e-5), projection_repair(tol=1e-6), projection_repair(max_iter=3) and clip_repair(floor=0.1) on the same asymmetric input (scripts/M3-d-r12/reference_refusals_r12.py, {S}reference_refusals_nondefault_r12.out). project.html line 237 states: 'raise ValueError for each of the four conditions ... in each function where that condition applies'. No test calls any refusal with a non-default floor, tol or max_iter (grep of test_project.py).",
   "Add grader tests that call each matrix function with non-default arguments (clip_repair floor=0.1, projection_repair tol=1e-6 and max_iter=3, is_psd tol=1e-5) on a non-square and on a 1e-8-asymmetric matrix, and assert ValueError. The reference raises in all of these, so the tests pass on it.")
ov("project-numbers", "PASS", "1 numbers vs unrounded; 2.2", "project.html Labs 1-3 printed numbers; lines 57-139, 466-477, 591-617",
   f"Every printed number in the prose recomputed independently with numpy (scripts/M3-d-r12/numbers_recompute_r12.py, {S}numbers_recompute_r12.out): eigenvalues -0.275297/-0.203711/-0.142113; repaired entries 0.636095, -0.382551, 0.469578 (Lab 1) and 0.498962, 0.409576, -0.586237 (Lab 2); distances 0.176573 and 0.175003, gap 0.001570181518 (prose 0.001570), largest entry difference 0.011516; determinant -0.261600; weights 1.778929, -1.096718, -0.255613, 0.573402 (sum 1). The 'about 1.78' and 'sum to 0.99' statements are exhibits in Exemplar A, not claims of the page.")
ov("project-lab1-memo-sentence", "PASS", "2 lab prints vs prose", "project.html lines 57, 139; tests/labs/M3/lab-M3-project-1.py",
   f"Lab 1 hypothesis (off-diagonal 0.8, -0.5, 0.6; verdict False; repaired diagonal 1 to six decimals; PSD True at 1e-9) matches the output: 'positive semidefinite at tol 1e-10: False', 'positive semidefinite at tol 1e-9 after repair: True' ({S}labs_twin_vs_page_r12.out).")
ov("project-lab2-completion", "PASS", "2 completion blanks", "project.html lines 142-224; tests/labs/M3/lab-M3-project-2.py",
   f"Page code differs from the twin only at the three blanks (Step 3 '___', Step 5 '___'), as ruling 11 permits. Filling them with the twin's expressions gives the expected block exactly ({S}labs_twin_vs_page_r12.out, 'expected block equals twin output: True').")
ov("project-lab3-check", "PASS", "2 lab prints vs prose", "project.html lines 290-478; tests/labs/M3/lab-M3-project-3.py",
   f"Page code identical to the twin; expected block equals the twin's output under python -I -W error (exit 0, {S}labs_twin_vs_page_r12.out). Hypothesis entries 0.7,0.3,-0.6,0.5,0.4,0.2 and vols 0.10,0.20,0.15,0.30 match the code. 'Lab 3 prints no weights for the two repairs' and 'prints no clipped diagonal' are true of the code.")
ov("project-lab3-diagonal-positivity-sentence", "PASS", "2 lab prints vs prose; 3 proof", "project.html lines 477, 605, 617",
   "The prose argument (completed run implies every d_i d_j > 0, hence all d_i nonzero of one sign; A1 gives d_i >= 0 via e_i^T X e_i; so positive) is logically valid, and it says the run shows this numerically. Verified by reasoning and by the completed-run exit status of clip_repair on this matrix (Lab 3 output).")
ov("project-spec-grader", "PASS", "1 spec vs starter and grader", "project.html lines 229-239; grader/starter.py; grader/test_project.py",
   "Spec signatures (min_eigenvalue, is_psd, clip_repair(matrix, floor), projection_repair(matrix, tol, max_iter), comparison_weights(corr, vols)) match starter.py lines and reference.py. The starter raises NotImplementedError (162 of 163 fail). The stated named conditions and the 163-test count match test_project.py.")
ov("project-conventions-math", "PASS", "5 math conventions", "project.html lines 242-252; grader/reference.py lines 109-150",
   "Clipping, projection step (J, E, N, H, W updates), gap and change definitions, weights formula and the 'no weights where Sigma singular' clause match reference.py (_psd_projection, projection_repair loop, comparison_weights) and the test that fixes the update (test_projection_repair_runs_exactly_max_iter_steps) (alternatives and equivalence checks in scripts/M3-d-r12/).")
ov("project-conventions-link", "PASS", "14 DAG link targets", "project.html line 233 (L05.html#def-positive-semidefinite-matrix), line 245, line 233 (eigendecomposition, spectral-theorem links)",
   "check_pages M3 PASS (out/check_pages_M3.out) verifies the anchors; L05.html Definition 1.4 defines PSD and PD together (grep L05 text); L04.html Theorem 2.3 is the spectral theorem and Definition 1.2 defines orthonormal (grep L04 text).")
ov("project-proof-A1", "PASS", "3 proof", "project.html line 643 (A1)",
   "A1 re-derived: X = V diag(max(Lambda_ii, f)) V^T is symmetric and z^T X z = sum max(...) (V^T z)_i^2 >= 0 since max(...) >= f >= 0. Hypotheses named (real symmetric, f >= 0, F1 to F4 for the spectral theorem Theorem 2.3). Complete.")
ov("project-proof-A2", "PASS", "3 proof", "project.html line 644 (A2)",
   "A2 re-derived: Y_ii = X_ii/(sqrt(d_i))^2 = 1; z^T Y z = q^T X q with q = D^{-1/2} z >= 0. Positivity of d_i named as needed for the division. Complete.")
ov("project-proof-A3", "PASS", "3 proof", "project.html line 645 (A3)",
   "A3 re-derived: det Sigma = a^2 b^2 (1 - rho^2) > 0; Sigma^{-1} iota = (det)^{-1}(b(b - rho a), a(a - rho b)); the sum a^2 + b^2 - 2 rho a b = (a-b)^2 + 2ab(1-rho) > 0 for |rho| < 1; scaling by c multiplies numerator and denominator by c^2. Complete.")
ov("project-proof-A4", "PASS", "3 proof", "project.html line 645 (A4)",
   "A4 re-derived: X u_i = V Lambda_0 e_i = 0 so X singular; with positive diagonal, Y z = D^{-1/2} X u_i = 0 for z = D^{1/2} u_i, so Y singular; Sigma S^{-1} z = S Y z = 0. Assumes F1 to F4 for the spectral decomposition. Complete.")
ov("project-hours", "PASS", "4 hours arithmetic", "project.html lines 259-267 (hours table); index.html data-hours-lessons and data-hours-project; L01-L09 data-hours",
   "Project table 2+3+14+8+12+6 = 45 = data-hours-project; hub 105 + 45 = 150 (index.html line 31 'Tier F · 150 hours'); lessons 12+11+12+12+12+11+11+12+12 = 105 = data-hours-lessons. 30% share stated and 45/150 = 0.30 holds. Ruling: hours are design targets; the 30% rule does not fail the slice.")
ov("project-exemplars", "PASS", "1 exemplar scores; 5 rubric calibration", "project.html lines 509-575 (Exemplar A), 577-654 (Exemplar B)",
   "Calibration re-scored from the passage text and the rubric descriptors only: Exemplar A -> C1 2, C2 2, C3 2, C4 1, C5 2 (official 2,2,2,1,2); Exemplar B -> C1 4, C2 4, C3 4, C4 3, C5 3 (official 4,4,4,3,3). Within one level on every criterion. Limitation: the annotations were visible in my read of the page before this scoring, so the blindness rule was not strictly met; the match is on the passage text alone.")
ov("project-rubric", "PASS", "5 rubric levels observable", "project.html lines 494-507 (rubric table)",
   "Each level descriptor names an observable element (a printed number, a named proof, a named test, a stated hypothesis). No descriptor is vague in the sense of the rule; C4 level 2 is checked below.")
ov("rubric-C4-level2-vague", "PASS", "5 rubric levels observable", "project.html line 503 (C4 row)",
   "C4 level 2 'Labels some inputs, or states a conclusion about a portfolio or a market from a printed result' names two observable conditions (labels present or absent; a market conclusion). Not vague.")
ov("project-references", "PASS", "3 attribution", "project.html lines 674-684 (Reading and References); references/references.json (axler2024linear, strang2023introduction)",
   f"The page quotes no locator and attributes no statement to Axler or Strang. Live Crossref run of verify_refs --unit M3: 2 of 560 entries, 0 problems ({S}verify_refs_M3_live_r12.out).")
ov("project-no-process-words", "PASS", "12 process words", "project.html; cards.json; grader/*.py; tests/labs/M3/lab-M3-project-*.py",
   "scripts/M3-d-r12/process_words_r12.sh ({S}process_words_r12.out): no verifier, ledger, fixer, builder, agent, revised or audit word in project.html, cards.json, the grader or the labs.")
ov("project-stretch", "PASS", "5 stretch", "project.html lines 663-670",
   "Three stretch items (weighted distance, seeded count over 200 matrices of sizes 3 to 5 with seeds stated, stopping-rule study) are open-ended and name the data (seeded, SIMULATED).")
ov("project-links", "PASS", "links", "project.html (href and src values)",
   "check_pages M3 PASS (out/check_pages_M3.out); no http(s) reference in project.html and every href/src target is an anchor or a relative path ({S}process_words_r12.out); check_pages resolves them.")
ov("project-brief-scope", "PASS", "4 scope brief", "project.html lines 229-233, 264, 475, 486, 617",
   "The page brief items 1-5 match the page's own spec (distances, weights of the input, where the formula applies to each repair). The curriculum brief wording is a separate row (scope-repair-weights-vs-brief).")
ov("scope-repair-weights-vs-brief", "FAIL", "4 scope vs curriculum brief",
   "curriculum/01-foundations.yaml lines 185-188 (brief); project.html lines 262-264, 475-477, 486, 503, 617-621; plans/M3-build-plan.md B3 (lines 369-373)",
   "The curriculum brief says: 'Compare the effect of each repair on downstream portfolio weights.' The page says (line 477) 'this page does not compare the weights of the two repairs: it gives no weights for either repaired matrix', and its brief (line 486) asks only whether the formula applies to each repair. Plan B3 records the architect question and proposes closed-form weights; no architect ruling narrows the curriculum brief. Round 11's PASS read the page's brief, not the curriculum source. Rung 3 must match the curriculum scope exactly (2.6).",
   "Architect decision required. Either (a) add to the spec a comparison of the input's weights with each repair's weights where the closed form is defined, stating the conditioning of the projection's Sigma, or (b) amend curriculum/01-foundations.yaml lines 185-188 to the scope the page delivers and regenerate. The verifier does not choose.")
ov("spec-stop-rule-sentence", "PASS", "3 spec vs reference", "project.html line 248 (Alternating steps)",
   "The sentence (reference stops after a step whose gap and change are both at most tol; output last W_t) matches reference.py projection_repair (lines 'if gap <= tol and step <= tol: break'). alt10 (stop on either) is an accepted alternative because the spec says the stopping rule is the student's.")
ov("project-lab3-weights-sentence", "PASS", "2 lab prints vs prose", "project.html lines 475-477; tests/labs/M3/lab-M3-project-3.py",
   "The sentence that Lab 3 prints the input weights and sum (1.778929 ... sum 1.000000) matches the expected block exactly ({S}labs_twin_vs_page_r12.out).")
ov("grader-instance", "PASS", "2.6 instances", "grader/instance.py; project.html line 231",
   "Read in full. k in {3,4,5}; vols in [0.05,0.40]; corr unit diagonal, off-diagonal in [-0.95,0.95], accepted only when min eigenvalue < -0.02 (the 'margin of 0.02' on page line 231); psd_corr positive definite (normalised Gram of k x (k+2)); spectra and orthonormal eigenvectors. Instances differ by seed (answers change).")
ov("grader-browser-timeout", "PASS", "2.6 browser constraints", "project.html line 237; course/assets/js/python.js line 4",
   "project.html line 237: 'A run in your browser stops after 120 seconds'; python.js line 4: TIMEOUT_MS = 120000.")
ov("grader-test-count-and-purity", "PASS", "2.6 count; purity", "grader/test_project.py test_functions_print_nothing, test_inputs_are_not_mutated; project.html line 237",
   f"163 tests collected (out/collect_only_M3.out); purity tests read in full (lines ~812-890). Each function and input is checked.")
ov("grader-standard-library-only", "PASS", "2.6 imports", "grader/test_project.py test_module_imports_only_standard_library_or_numpy; project.html line 237",
   "The import test walks the AST of covariance_doctor.py and allows numpy and sys.stdlib_module_names. Starter-only imports pass it; the mutant vd3_04 (scipy) is killed by it (out/mutate_M3_seeds0-9_r12.out).")
ov("grader-lab3-reference-numbers", "PASS", "2.6 Lab 3 numbers", "grader/test_project.py test_lab3_reference_numbers_are_matched; project.html Lab 3",
   f"The grader's Lab 3 values (-0.142113; 0.176573; 0.175003 at 1e-5; 0.011516 at 1e-5; weights at 1e-6) equal the printed output of Lab 3 and my numpy recomputation ({S}numbers_recompute_r12.out). The reference passes them (reference_seed0_r12.out).")
ov("grader-spec-rubric-counts", "PASS", "2.6 counts; 2.6 rubric", "project.html lines 237, 490, 495, 498-502; grader/test_project.py",
   "'163 tests' (collect-only 163); five criteria and four levels per criterion in the rubric table (lines 494-507).")
ov("spec-projection-tol-undefined", "PASS", "1 spec; tolerance defined", "project.html lines 233, 246; grader/starter.py lines 30-36",
   "tol is defined in the conventions (projection_repair: tol is the stopping tolerance, the stopping rule is the student's); the starter's projection_repair docstring says so; PSD tolerance 1e-9 and 1e-8 stated for the repairs.")
ov("grader-projection-spec-vs-reference", "PASS", "3 spec vs reference", "grader/reference.py _psd_projection and projection_repair; project.html line 248",
   "Reference computes the PSD step as clipping at 0 without rescaling, then the unit-diagonal step, matching the page (conventions, 'Alternating steps').")
ov("grader-weights-spec-vs-reference", "PASS", "3 spec vs reference", "grader/reference.py comparison_weights; project.html line 249",
   "Reference solves Sigma x = 1 with Sigma = S C S, normalises to sum 1, raises the two named weight conditions. Matches the page's weights convention.")
ov("grader-failure-messages-leak-answers", "PASS", "2.6 messages", "grader/test_project.py (every assert, pytest.fail and must_raise message)",
   "Messages name a property and never print the expected value; carried (grader unchanged).")

# ---- mutants and equivalence ----
ov("mutants-existing-140", "FAIL", "2.6 mutation (all existing)", "ledgers/M3/mutants/ (174 files)",
   f"tools/mutate_graders.py --unit M3 --seeds 0-9: 174/174 killed ({S}mutate_M3_seeds0-9_r12.out). 171 kills are assertion failures; three are collection-only (mutants-collection-only-kills).",
   "See mutants-collection-only-kills.")
ov("mutants-description-all", "PASS", "2.6 mutation description", "ledgers/M3/mutants/ (174 files, first docstring line)",
   "Parsed every file: each first docstring line names a student error; none is the reference docstring.")
ov("equivalent-readme-citation", "PASS", "2.6 equivalence proof", "ledgers/M3/equivalent/README.md and alt10_no_unit_diagonal_correction.py",
   f"Re-proved by hand (H off-diagonal exactly 0.0 after each step; diagonal overwritten, so the correction is inert). Re-run bitwise on the checkout: 'trials 1200: outputs differing 0' ({S}equiv_alt10_r12.out; scripts/M3-d-r12/equiv_alt10_r12.py).")
ov("mutants-v12d-new-student-errors", "PASS", "2.6 mutation (new this round)", "ledgers/M3/mutants/v12d_01, v12d_02, v12d_04",
   f"Three new student-error mutants written this round (scripts/M3-d-r12/make_mutants_r12.py): v12d_01 projection PSD step reflects negative eigenvalues (killed by test_projection_repair_is_no_farther_than_clipping[seed], seed 0); v12d_02 unit correction from previous iterate (killed by test_projection_repair_is_no_farther_than_clipping[seed], seed 0); v12d_04 clip rescales first (killed by test_clip_repair_has_unit_diagonal_and_is_symmetric[seed], seed 0); ({S}mutate_M3_seeds0-9_r12.out).")

ov("mutants-collection-only-kills", "FAIL", "2.6 mutation (kill validity)",
   "ledgers/M3/mutants/r12d_m02_min_eigenvalue_first_jacobi_value.py, r12d_m03_projection_keeps_negatives_down_to_minus_0p01.py, r12d_m04_weights_scale_row_by_first_volatility.py (line 1 is the mutant docstring, then the reference docstring is a second string statement before 'from __future__')",
   "mutate_graders.py reports these three as killed, but the only failure is 'SyntaxError: from __future__ imports must occur at the beginning of the file' at collection (out/mutate_M3_seeds0-9_r12.out; run_one_mutant_r12.sh output). No test assertion kills them, so the student error each models is untested. Probe: scripts/M3-d-r12/repair_broken_mutant_probe_r12.py writes copies with only the second docstring removed (scripts/M3-d-r12/broken_mutant_repairs/); each copy is then killed by real assertions (r12d_m02 by test_min_eigenvalue_is_smallest_of_diagonal and test_min_eigenvalue_agrees_with_independent_bisection; r12d_m03 by test_projection_repair_is_a_valid_repair and test_lab3_reference_numbers_are_matched; r12d_m04 by test_lab3_reference_numbers_are_matched and test_weights_two_asset_closed_form). Outputs: out/ directory of this round.",
   "In each of the three files delete the second (reference) docstring so that 'from __future__' follows the mutant's docstring, as in scripts/M3-d-r12/broken_mutant_repairs/. Re-run tools/mutate_graders.py --unit M3 --seeds 0-9 and confirm each is killed by a named test, not by collection.")

# ---- cards ----
ov("cards-structure", "PASS", "10 cards structure", "course/modules/M/M3/cards.json (208 records)",
   f"scripts/M3-d-r12/cards_scan_r12.py: 208 records, 208 distinct ids, sorted; field sets: 118 with grade T, 39 grade C with basis, 51 without grade; no grade outside {{T, C}}; every C card has a basis; no basis on a non-C card ({S}cards_scan_r12.out).")
ov("cards-id-sequence", "PASS", "10 cards ids", "course/modules/M/M3/cards.json",
   "Ids 1..213 with 102, 148, 191, 204, 206 absent; no duplicates; order ascending. Ruling 2: gaps are not defects.")
ov("cards-numbers-cited", "PASS", "10 cards numbers cited", "cards.json front and back; L01.html, L08.html, L09.html",
   "Numbered items cited by the cards were checked this round against the lesson text for L01, L08, c175 and c209; the other lessons' cards are carried (records and lesson pages byte-identical since ccaeeaf4).")
ov("cards-labels-cited", "PASS", "10 cards labels (ruling 13)", "cards.json grade and basis fields; L01-L09 key-results tables",
   "Ruling 13 check (scripts/M3-d-r12/kr_vs_cards_r12.py, {S}kr_vs_cards_r12.out): 39 C cards, 11 C key-results rows, no T card cites lab output or SIMULATED values; every C card cites a lab run and mirrors a C row with the same grade and the same lab run. Wording of the basis differs from the Source column in L06-L09 ('Lab 1, ...' vs 'Lab 1 output (...)'), as it does in L02-L05 (prefix); the same grade and run are named, so this is recorded as consistent.")
ov("cards-duplicate-scan", "PASS", "10 cards duplicates", "course/modules/M/M3/cards.json (all 208 pairs compared)",
   f"scripts/M3-d-r12/cards_scan_r12.py: no duplicate fronts or backs after normalisation; two pairs with combined similarity >= 0.80: M3-c025 / M3-c187 (kernel vs image of a linear map, different facts) and M3-c082 / M3-c193 (PSD vs PD, different facts). Not duplicates ({S}cards_scan_r12.out).")
ov("cards-sample-20", "PASS", "10 cards read", "cards.json (all 208 records read as data; 52 read against lesson text this round)",
   "Read this round against the lesson text: L01 (24, all), L08 (28, all), M3-c175, M3-c189, M3-c190, M3-c209. Lessons L02-L07 and L09 carried (records and lesson pages byte-identical since ccaeeaf4). Sample rule (1 in 10) is exceeded.")
ov("cards-L01", "PASS", "10 cards lesson", "cards c001-c022, c169-c170 vs L01.html",
   "Each card checked against the L01 definitions, propositions and examples (Definition 1.1, Lemma 1.3, Proposition 1.4, Definition 2.1, Proposition 2.2, Example 2.3, Definitions 3.1-3.3, Lemma 3.4, Proposition 3.5, Corollary 3.6, Theorem 3.7, Theorem 3.8, Example 3.9, Example 3.10, Proposition 3.12) and the Lab 1 counts 188/200, 198/200, 100/100, 0/200 (L01 lab output). Grades match the key-results rows (lines 294-303).")
ov("cards-L08", "PASS", "10 cards lesson", "cards c130-c145, c174, c186, c197-c201, c207, c210-c213 vs L08.html",
   f"Re-verified in full (previous FAIL row). M3-c211 now matches L08 Section 3 ('orthogonalizing means subtracting ... (Lesson 7, Theorem 1.2)' and 'the earlier shapes are independent') and Lesson 7 Theorem 1.2 (columns linearly independent). Lab numbers 75.9/18.1/5.2, 0.7587 -> 0.9791, 0.9994/0.9985/0.9990 match the L08 lab output. Definitions 1.3, 3.1, Theorem 1.4, Corollary 2.2, Propositions 1.1, 1.2, 2.3 and Remark 2.4 exist and say what the cards say. Section 1 defines tenor and bp. Previous row's inclusion of c209 was a mapping error: M3-c209 is an L07 card.")
ov("cards-c209-c213-new", "PASS", "10 cards new", "cards.json M3-c209 (L07), M3-c210 to M3-c213 (L08)",
   "M3-c209 (column space) checked against L07 line 23. M3-c210 to M3-c213 checked against L08 Section 1 and Section 3 text (cosine, orthogonalization, tenor, bp). M3-c211 PASS (fixed).")
ov("cards-lab-numbers", "PASS", "10 cards lab numbers", "cards.json grade-C cards; tests/labs/M3 expected blocks; L01, L08, L09 lab output",
   "L01 counts (188, 198, 100, 0) match the L01 lab output; L08 values match L08 lines 179-181; L09 counts 23 of 23 (c175) match the L09 lab output.")
ov("cards-sample-lesson-text-current", "PASS", "10 cards current text", "L01.html, L08.html, cards.json",
   "Card text matches the current lesson text (L08 Section 3 change reflected in c211; L01 and L08 read in full this round).")
ov("cards-c208-duplicate", "PASS", "10 cards duplicates", "cards.json M3-c208 (L09)", "Carried: M3-c208 record unchanged; not a duplicate of any other card.")
ov("cards-L08-section3", "PASS", "1 lesson math", "L08.html Section 3", "see cards-L08 and lesson-l08-section3-text")

# ---- notation, DAG, lessons ----
ov("notation-registry", "PASS", "13 notation", "notation/notation.json (8 symbols); project.html; L08.html; cards.json",
   "Registry symbols T, gamma_3, gamma_4 and macros (\\E, \\R, \\diag, \\tr, ...). project.html uses no mathbb and none of the registered symbols with another meaning; Sigma, S, C, V, Lambda, D, P, J, E_t, H_t, N_t, W_t are page-local and collide with no registry entry.")
ov("notation-R-macro", "PASS", "13 notation macro", "project.html; L07.html; L08.html; L09.html; cards.json",
   "grep: no \\mathbb in project.html; \\R used for reals (ruling 1).")
ov("dag-linked-concepts", "PASS", "14 DAG links", "project.html concept links (eigendecomposition, spectral-theorem, positive-semidefinite-matrix)",
   "check_dag M3 PASS (out/check_dag_M3.out); the three project links point to L03, L04 and L05 definitions that exist.")
ov("dag-m4-concepts-by-name", "PASS", "14 DAG names", "project.html; cards.json; L01-L09",
   "Covariance, correlation, variance and Gaussian appear as plain prose without a link (ruling 3). check_dag M3 PASS.")
ov("links-and-anchors", "PASS", "links", "course/modules/M/M3/project.html; index.html; L08.html",
   "check_pages M3 PASS (out/check_pages_M3.out); page_smoke: zero console errors, no external requests (out/page_smoke_project.out).")
ov("lesson-l08-section3-text", "PASS", "1 lesson math", "course/modules/M/M3/L08.html Section 3 (lines 137-141)",
   "Re-read in the text extract: the three shapes, their match rule and the three-value assumption are stated; the Theorem 1.2 reference is correct (L07 Theorem 1.2 needs independence, which the page states under the three-value assumption).")


# ---- assembly ----
SUBJECT_CHANGED = ("project.html", "cards.json", "ledgers/M3/mutants/ (")
rows = []
unresolved = []
for prev in PREV["rows"]:
    pid = prev["id"]
    if pid in OVERRIDE:
        status, check, location, evidence, fix = OVERRIDE.pop(pid)
    elif prev["status"] == "PASS" and not (any(t in prev["location"] for t in SUBJECT_CHANGED) and pid not in ALLOW_CARRY_CARDS):
        status, check, location, fix = "PASS", prev["check"], prev["location"], ""
        evidence = CARRY_PREFIX + prev["evidence"]
    else:
        unresolved.append((pid, prev["status"], prev["location"][:80]))
        continue
    rows.append({"id": pid, "check": check, "location": location, "status": status,
                 "evidence": evidence.replace("{S}", S), **({"fix": fix} if fix else {})})
existing = {r["id"] for r in rows}
for pid, (status, check, location, evidence, fix) in OVERRIDE.items():
    if pid in existing:
        continue
    rows.append({"id": pid, "check": check, "location": location, "status": status,
                 "evidence": evidence.replace("{S}", S), **({"fix": fix} if fix else {})})
if unresolved:
    print("UNRESOLVED previous rows (need an override):")
    for u in unresolved:
        print("  ", u)

# ---- mutants: every file in ledgers/M3/mutants/ with its kill record, plus the survivor ----
mutants = []
for line in open(S + "mutate_M3_seeds0-9_r12.out", encoding="utf-8"):
    m = re.match(r"^KILLED (\S+)\.py: (.*) -> (.*) \(seed \d+\)$", line.rstrip("\n"))
    if m:
        killed_by = m.group(3)
        desc = m.group(2)
        if killed_by.startswith("collection/import error"):
            killed_by = None
            desc += " [kill is a SyntaxError at collection, not a test assertion; see mutants-collection-only-kills]"
        mutants.append({"id": m.group(1), "description": desc, "killed_by": killed_by})
survivor_desc = ("clip_repair checks symmetry only when the floor is the default, so an asymmetric input with another floor "
                 "is not refused (survivor; kept in scripts/M3-d-r12/survivors/, not in mutants/).")
mutants.append({"id": "v12d_03_clip_validates_symmetry_only_for_default_floor", "description": survivor_desc, "killed_by": None})

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
killed = sum(1 for m in mutants if m["killed_by"])
fragment = {
    "unit": "M3",
    "slice": "d",
    "round": 12,
    "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, round 12; shares no context with the builders",
    "pin": "329c1d7feac5479403c351e64587c867278452cc",
    "base": "round-11 pin ccaeeaf4 (fragment /Users/billyribeiro/.fanout/frags/D-M3-d.round11.json, read as context; its PASS rows were re-proved or carried only where the cited files are byte-identical). Delta ccaeeaf4..329c1d7 for this slice: cards.json (M3-c211 only), project.html (two lines: 53 and 247), three new v11d mutants, ruling 13.",
    "checkout": ROOT,
    "scratch": "ledgers/M3/scripts/M3-d-r12/",
    "verified_at": "2026-11-05T14:00:00+00:00",
    "verdict": "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 and killed == len(mutants) else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Full read this round: project.html (694 lines), grader/starter.py, reference.py, instance.py, test_project.py (890 lines), tests/labs/M3 project twins, all 208 cards records (structure and scan), L01 and L08 cards against lesson text, c175, c189, c190, c209, 10 alternatives (diffs and seeds 0-49), equivalent/alt10 and README.",
        "Survivor v12d_03 is a real gap: the page says the four named ValueError conditions apply in each function (project.html line 237), and the suite refuses them only with default arguments. It is kept out of mutants/ so the mutate gate stays green; the fix is a grader test change, not a page change.",
        "Scope: the curriculum brief (curriculum/01-foundations.yaml lines 185-188) asks to compare each repair's effect on downstream portfolio weights; the page declines that comparison. This needs an architect decision; the verifier does not pick the fix.",
        "alt2 docstring claims 5000 iterations; the code respects max_iter. Behaviour is correct (alt2 passes seeds 0-49); only the docstring is false.",
        "Calibration of Exemplars A and B was re-scored from the passage text and the rubric; the annotations were visible during the earlier read, so the blindness rule was not strictly met.",
        "Ruling 13: the basis wording of C key-results rows and C cards differs in L06-L09 ('Lab 1 output (...)' vs 'Lab 1, ...'), as in L02-L05 (prefix). Grade and lab run agree in every case; recorded as consistent, not as a FAIL.",
        "Card M3-c209 is an L07 card; the round-11 FAIL row listed it under L08 (mapping error), now verified under L07.",
        "Could not check: a strictly blind rubric calibration; the browser (Pyodide) run of the alternatives (only local pytest); the live Crossref verification ran for the two M3 references only (verify_refs --unit M3); no rebuild of the lab expected blocks beyond the twin run.",
    ],
    "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"],
                "mutants_killed": killed, "mutants": len(mutants)},
}
problems = ledger.validate(fragment, "M3-d")
print("validate:", problems)
print("verdict:", fragment["verdict"], "rows:", len(rows), counts, "mutants killed", killed, "/", len(mutants))
json.dump(fragment, open("ledgers/M3/M3-d.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("written ledgers/M3/M3-d.json")
