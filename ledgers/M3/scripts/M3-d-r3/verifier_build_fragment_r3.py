"""Build ledgers/M3/M3-d.json, the round-3 fragment for M3 slice d (verifier round 3, pin a007712).

Rows are the verifier's own findings from the commands and scripts under ledgers/M3/scripts/M3-d-r3/ and out3/.
The mutant list is parsed from out3/mutate_M3_seeds0-9_final.out (tools/mutate_graders.py output), and each
description is the mutant file's own first docstring line. Run from the checkout root with the checkout's venv.
"""

import ast
import datetime
import json
import re
from pathlib import Path

ROOT = Path.cwd()
OUT3 = "ledgers/M3/scripts/M3-d-r3/out3"
SCRIPTS = "ledgers/M3/scripts/M3-d-r3"


def mutants() -> list[dict]:
    result = []
    for line in (ROOT / OUT3 / "mutate_M3_seeds0-9_final.out").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
        if not m:
            continue
        status, name, desc, killed = m.groups()
        killed_by = None if killed.strip() == "None" else killed.strip()
        doc = ast.get_docstring(ast.parse((ROOT / "ledgers/M3/mutants" / name).read_text(encoding="utf-8")))
        first = (doc or desc).splitlines()[0].strip()
        result.append({"name": name, "description": first, "killed_by": killed_by})
    return result


ROWS = [
    # ---- gates (run by this verifier on pin a007712)
    dict(id="gate-check-pages", check="gate", location="course/modules/M/M3/ (all pages)", status="PASS",
         evidence=f"tools/check_pages.py --all: 'check_pages M3: PASS', exit 0 ({OUT3}/check_pages.out)."),
    dict(id="gate-check-dag", check="gate", location="course/modules/M/M3/ (all pages)", status="PASS",
         evidence=f"tools/check_dag.py --all: 'check_dag M3: PASS', exit 0 ({OUT3}/check_dag.out)."),
    dict(id="gate-check-projects", check="gate", location="course/modules/M/M3/project.html", status="PASS",
         evidence=f"tools/check_projects.py --all: 'check_projects M3: PASS', exit 0 ({OUT3}/check_projects.out)."),
    dict(id="gate-run-graders", check="gate", location="course/modules/M/M3/grader/", status="PASS",
         evidence=f"tools/run_graders.py --unit M3 --seeds 0-49: 'run_graders M3: PASS (reference 50/50 seeds)', exit 0 ({OUT3}/run_graders.out)."),
    dict(id="gate-run-labs", check="gate", location="tests/labs/M3/ and project.html labs", status="PASS",
         evidence=f"tools/run_labs.py --unit M3: 'run_labs M3: PASS (12/12)', exit 0; includes lab-M3-project-1..3 (run_labs checks code = twin, twin under python -I -W error, expected = output) ({OUT3}/run_labs.out)."),
    dict(id="gate-page-smoke", check="gate", location="course/modules/M/M3/project.html", status="PASS",
         evidence=f"tools/page_smoke.py --unit M3 --pages project (stem form; the form --pages project.html selects no page and passes vacuously, so it was not used): 'page_smoke modules/M/M3/project.html: PASS'; in-browser grader 'All 155 tests pass' ({OUT3}/page_smoke_project.out). Lesson pages and index are outside slice d and were not run."),
    dict(id="gate-ruff", check="gate", location="course/modules/M/M3/grader/, tests/labs/M3/", status="PASS",
         evidence=f"ruff check course/modules/M/M3/grader tests/labs/M3: 'All checks passed!'; ruff format --check: '16 files already formatted' ({OUT3}/ruff.out)."),
    dict(id="gate-mypy", check="gate", location="course/modules/M/M3/grader/reference.py, instance.py, starter.py", status="PASS",
         evidence=f"mypy --no-incremental on the three files: 'Success: no issues found in 3 source files' ({OUT3}/mypy.out)."),
    dict(id="gate-verify-refs", check="gate", location="references/references.json", status="PASS",
         evidence=f"tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' ({OUT3}/verify_refs_offline.out). Live run not executed; the Axler DOI was read with plain curl to api.crossref.org ({OUT3}/axler_crossref.txt)."),
    dict(id="gate-collect-only", check="gate", location="course/modules/M/M3/grader/test_project.py vs project.html line 237", status="PASS",
         evidence=f"pytest --collect-only -q in a scratch copy (reference as covariance_doctor.py, instance.py, test_project.py): '155 tests collected'; project.html line 237 states 155 ({OUT3}/collect_only.out)."),
    dict(id="gate-pytest-relevant", check="gate", location="tests/test_labs.py, tests/test_page_checks.py, tests/test_run_labs.py", status="PASS",
         evidence=f"pytest -q tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py -k 'M3 or project or grader': exit 0 ({OUT3}/pytest_relevant.out)."),
    dict(id="gate-mutate-m3", check="2.6-mutation", location="ledgers/M3/mutants/ (142 files)", status="FAIL",
         evidence=f"tools/mutate_graders.py --unit M3 --seeds 0-9: 'mutate_graders M3: FAIL (137/142 killed)', exit 1. Survivors: v3d_01_projection_repair_runs_one_extra_step.py, vd3_01_comparison_weights_symmetrises_caller_corr_in_place.py, vd3_02_min_eigenvalue_symmetrises_caller_matrix_in_place.py, vd3_03_is_psd_symmetrises_caller_matrix_in_place.py, vd3_04_min_eigenvalue_uses_scipy_not_allowed_by_page.py ({OUT3}/mutate_M3_seeds0-9_final.out).",
         fix="Every survivor must be killed by a new grader test (ruling 9): see grader-test-count-and-purity (vd3_01..03), grader-standard-library-only (vd3_04) and mutants-v3d-01-max-iter-plus-one (v3d_01). Re-run tools/mutate_graders.py --unit M3 --seeds 0-9 until exit 0."),
    dict(id="gate-reference-starter", check="3.3-mutation", location="course/modules/M/M3/grader/reference.py, starter.py", status="PASS",
         evidence=f"tools/run_graders.py asserts the starter fails the suite; the M3 run passed ({OUT3}/run_graders.out); starter.py signatures equal project.html line 233 and the test calls."),
    dict(id="gate-alternatives-seeds-0-49", check="2.6-alternatives", location="ledgers/M3/alternatives/alt1..alt6", status="PASS",
         evidence=f"{SCRIPTS}/run_alts_r3.py over alt1..alt6 and the reference, seeds 0-49: each 'PASS ... 155 passed' ({OUT3}/alts_seeds_0-49.out)."),
    dict(id="gate-named-conditions", check="2.6-autograder-refusals", location="course/modules/M/M3/grader/test_project.py must_raise call sites", status="PASS",
         evidence="grep must_raise: call sites at lines 175, 185, 225, 649, 661, 697, 708, 733 assert ValueError only for the four named conditions (non-square; asymmetry beyond 1e-9; volatility not strictly positive; length mismatch). Tests at 210-215 and 674-681 assert no exception for in-tolerance input."),
    # ---- grader
    dict(id="grader-instance", check="2.6-instances", location="course/modules/M/M3/grader/instance.py", status="PASS",
         evidence=f"{SCRIPTS}/instances_sample_r3.py, seeds 0-19: every instance valid (k in {{3,4,5}}, symmetric, unit diagonal, min eigenvalue of corr below -0.02, psd_corr positive definite with unit diagonal, vols positive, psd_spectrum[0] = 0); the 20 clip distances are pairwise distinct ({OUT3}/instances_sample_r3.out). Second instance (INST2, seed + 7919) is used in test_project.py."),
    dict(id="grader-test-count-and-purity", check="2.6-autograder-purity", location="course/modules/M/M3/grader/test_project.py lines 755-772 (test_inputs_are_not_mutated)", status="FAIL",
         evidence=f"mutants vd3_01_comparison_weights_symmetrises_caller_corr_in_place.py, vd3_02_min_eigenvalue_symmetrises_caller_matrix_in_place.py and vd3_03_is_psd_symmetrises_caller_matrix_in_place.py all survive seeds 0-9 ({OUT3}/mutate_M3_seeds0-9_final.out). test_inputs_are_not_mutated passes the asymmetric-within-tolerance matrix 'near' only to clip_repair and projection_repair (lines 766-767); min_eigenvalue, is_psd and comparison_weights are called only on symmetric inputs. project.html line 235 states 'No function changes its arguments'.",
         fix="In test_inputs_are_not_mutated also call sol.min_eigenvalue(near), sol.is_psd(near) and sol.comparison_weights(near_corr, vols), where near_corr is an in-tolerance asymmetric correlation matrix (asymmetry 1e-10), and assert each argument equals its pre-call copy. Then update the test count on project.html line 237 to the new collect-only count."),
    dict(id="grader-lab3-reference-numbers", check="2.6-numbers", location="course/modules/M/M3/grader/test_project.py LAB3_CORR, LAB3_VOLS, test_lab3_reference_numbers_are_matched", status="PASS",
         evidence=f"{SCRIPTS}/project_numbers_r3.py (numpy oracle, out3/project_numbers_r3.out): smallest eigenvalue -0.1421126; clip distance 0.1765732; projection distance 0.1750030; gap 0.0015702; largest entry difference 0.0115164; weights 1.778929, -1.096718, -0.255613, 0.573402. All equal the test constants within the test tolerances."),
    dict(id="grader-browser-timeout", check="2.6-project", location="course/assets/js/python.js:4 and :36-37", status="PASS",
         evidence="python.js line 4: TIMEOUT_MS = 120000; lines 36-37 stop the run after TIMEOUT_MS / 1000 = 120 s. project.html line 235 says 'A run in your browser stops after 120 seconds'."),
    dict(id="grader-standard-library-only", check="2.6-autograder-constraints", location="course/modules/M/M3/grader/test_project.py (no import test); course/modules/M/M3/project.html line 235; grader/starter.py line 8", status="FAIL",
         evidence=f"project.html line 235 now states 'The standard library and NumPy only' (the round-2 'standard library only' wording was changed, and NumPy is allowed by plans/M3-build-plan.md Q3 'NumPy yes'). No test inspects imports. vd3_04_min_eigenvalue_uses_scipy_not_allowed_by_page.py (min_eigenvalue calls scipy.linalg.eigvalsh) survives seeds 0-9 ({OUT3}/mutate_M3_seeds0-9_final.out).",
         fix="Add a test (ast parse of covariance_doctor.py) that fails when any import is neither in sys.stdlib_module_names nor 'numpy', with a message naming the rule and not the answer; re-check that all six alternatives and the reference pass it; then update the test count on project.html line 237. Alternatively delete the constraint sentence from project.html line 235 and the starter line 8."),
    dict(id="grader-reference-docstring", check="prose-non-learner", location="course/modules/M/M3/grader/reference.py lines 3-4", status="PASS",
         evidence="The reference's module docstring reads 'the Frobenius-nearest repair is Alternating projections, with correction terms, between ...': a grammatical defect in a file that is not shipped to learners. It asserts nothing false. Recorded as a note, not a finding; a one-word fix ('is alternating projections') would remove it."),
    dict(id="alternatives-five-standard-library", check="2.6-alternatives", location="ledgers/M3/alternatives/alt1..alt6", status="PASS",
         evidence="Imports read by grep: alt1, alt2, alt4, alt5 standard library (math, collections.abc); alt3 standard library plus numpy inside functions; alt6 numpy. None imports scipy. All six obey the page's 'standard library and NumPy only' (project.html line 235). Styles: alt5 bisection with Cholesky pivots; alt2 Dykstra with a feasibility-gap stop; alt4 Jacobi with other cutoffs; alt1/alt3/alt6 NumPy routines."),
    dict(id="alternatives-seeds-0-49", check="2.6-alternatives", location="ledgers/M3/alternatives/", status="PASS",
         evidence=f"Six alternatives run under the grader on seeds 0-49 with the browser flags: 155 passed on every seed for each ({OUT3}/alts_seeds_0-49.out)."),
    # ---- mutants (existing and new)
    dict(id="mutants-existing-128", check="2.6-mutation", location="ledgers/M3/mutants/ (133 committed files)", status="PASS",
         evidence=f"git ls-files ledgers/M3/mutants: 133 committed files; every one is KILLED on seeds 0-9 in {OUT3}/mutate_M3_seeds0-9_final.out. The count changed from the round-2 '128' because the round-2 fixer added v2d_01..05 in the round-2 commit."),
    dict(id="mutants-new-student-errors", check="2.6-mutation", location="ledgers/M3/mutants/vd1_01..vd1_05", status="PASS",
         evidence=f"vd1_01..05 are KILLED on seed 0 ({OUT3}/mutate_M3_seeds0-9_final.out)."),
    dict(id="mutants-v2d-01-05", check="2.6-mutation", location="ledgers/M3/mutants/v2d_01..v2d_05", status="PASS",
         evidence=f"v2d_01..v2d_05 are KILLED on seed 0 ({OUT3}/mutate_M3_seeds0-9_final.out)."),
    dict(id="mutants-v2d-06", check="2.6-mutation", location="ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py", status="PASS",
         evidence="v2d_06 (NumPy eigh inside the engine) was the round-2 surviving mutant. The page now allows NumPy (project.html line 235), so the behaviour is not a fault; the file is out of mutants/ (ledgers/M3/retired/) and is the same kind of engine as alt1 and alt6."),
    dict(id="mutants-v3d-01-max-iter-plus-one", check="2.6-mutation", location="ledgers/M3/mutants/v3d_01_projection_repair_runs_one_extra_step.py; project.html line 233; grader/test_project.py lines 561-569", status="FAIL",
         evidence=f"v3d_01 runs range(max_iter + 1) steps. It SURVIVES seeds 0-9 ({OUT3}/mutate_M3_seeds0-9_final.out). project.html line 233 states the function 'stops after at most max_iter alternating steps'. The only max_iter test (test_projection_repair_honours_max_iter) checks that one iteration differs from the default run, which an off-by-one still satisfies.",
         fix="The page does not pin the iteration, so no implementation-neutral test can count steps. Either (a) pin the update rule on project.html (the reference's Dykstra step) and add a test that compares projection_repair(corr, max_iter=m) for m = 1, 2, 3 with an m-step oracle written in the test file, or (b) remove 'stops after at most max_iter alternating steps' from project.html line 233 and state max_iter only as a cap. Architect decision between (a) and (b); (a) kills the mutant."),
    dict(id="mutants-v3d-02-05", check="2.6-mutation", location="ledgers/M3/mutants/v3d_02..v3d_05", status="PASS",
         evidence=f"v3d_02 (floor scaled by largest eigenvalue), v3d_03 (projection warm-starts from the previous call), v3d_04 (clip output rounded to six decimals), v3d_05 (min_eigenvalue of the repaired matrix) are all KILLED on seed 0 ({OUT3}/mutate_M3_seeds0-9_final.out)."),
    # ---- equivalent/
    dict(id="equivalent-r6d-m04", check="2.6-equivalence", location="ledgers/M3/equivalent/r6d_m04_projection_stops_on_gap_only.py", status="FAIL",
         evidence=f"Not exactly equivalent. {OUT3}/equiv_output_diff_r3.out: exact-equal to the reference on 46 of 50 seeds, largest entry difference 1.988e-11. The file differs from the reference only in the stop test (diff). The README gives no proof, only 'ruled ... by independent verifiers'.",
         fix="Under ruling 9 this file belongs in equivalent/ only with a README proof: (i) cite project.html line 233 as the only stop statement ('stops after at most max_iter alternating steps'), so a tolerance-based stop is not fixed; (ii) state the numerical bound from out3/equiv_output_diff_r3.out and that all 155 tests pass on seeds 0-49. Alternatively move it to alternatives/ and let the grader pass it."),
    dict(id="equivalent-r11d-m02", check="2.6-equivalence", location="ledgers/M3/equivalent/r11d_m02_projection_stops_on_step_only.py", status="FAIL",
         evidence=f"Not exactly equivalent: exact-equal on 49 of 50 seeds, largest entry difference 1.818e-11 ({OUT3}/equiv_output_diff_r3.out). Same missing proof as equivalent-r6d-m04.",
         fix="Same as equivalent-r6d-m04: write the README proof (page line 233 states no tolerance-based stop; measured bound; 155 tests pass) or move the file to alternatives/."),
    dict(id="equivalent-r15d-m03-label", check="2.6-equivalence", location="ledgers/M3/equivalent/r15d_m03_projection_repair_never_stops_early.py and README.md", status="FAIL",
         evidence=f"Exact-equal on 0 of 50 seeds; largest entry difference 3.686e-11 ({OUT3}/equiv_output_diff_r3.out). The file's only change is the stop test 'and False' (diff). The README calls it equivalent without an argument.",
         fix="Give the README proof: the page states no tolerance-based stopping rule (line 233), every output differs from the reference by less than 4e-11 on seeds 0-49, and all 155 tests pass. Or move it to alternatives/, since it is a valid implementation that the grader accepts."),
    dict(id="equivalent-readme-citation", check="1.4-attribution", location="ledgers/M3/equivalent/README.md lines 3-5", status="FAIL",
         evidence="README line 4-5 says 'project.html states no stop criterion for the projection loop (line 660)'. project.html line 660 is the stretch item 'The stopping rule' (report how the distance changes with tol and max_iter); it does not say that no stop criterion is stated. The only stop statement is project.html line 233 ('stops after at most max_iter alternating steps').",
         fix="Replace the locator: cite project.html line 233 and quote its words; drop the reference to line 660 or quote it accurately."),
    # ---- project (rubric, spec, labs, proofs)
    dict(id="project-numbers", check="2.2-numbers", location="course/modules/M/M3/project.html lines 57-60, 130-137, 213-220, 460-468, 469, 575, 597, 609, 622", status="PASS",
         evidence=f"{SCRIPTS}/project_numbers_r3.py (numpy.linalg.eigh oracle, not the page code) reproduces every printed number: Lab 1 eigenvalues -0.275297 1.463830 1.811467, rebuilt diagonal 1.096064 1.104409 1.074824, repaired entries 0.636095 -0.382551 0.469578; Lab 2 eigenvalues -0.203711 1.486490 1.717222, rebuilt diagonal 1.060165 1.075224 1.068322; Lab 3 numbers as in grader-lab3-reference-numbers, determinant -0.261600. Diagonal deviations are 0.0 and 2.2e-16 (unrounded), below 5e-7 as the page says. Prose numbers 0.176573, 0.175003, 0.001570, 0.011516, 1.78, 0.99 (exemplar A) re-derived."),
    dict(id="project-lab1-memo-sentence", check="2.9-prose", location="course/modules/M/M3/project.html Repairs and their checks paragraph (line 597)", status="PASS",
         evidence="'a zero or negative diagonal entry would have printed no value or a deviation of 2': a zero entry gives sqrt(0) in the rescaling and a ZeroDivisionError (no value); a negative entry gives sqrt of a negative product (no value) or, when both diagonal entries are negative, a diagonal of -1 and deviation 2. Checked by reasoning against the Lab 3 rescaling formula."),
    dict(id="project-conventions-link", check="2.9-links", location="course/modules/M/M3/project.html line 53 and line 240 (id='conventions')", status="PASS",
         evidence="The anchor #conventions exists (project.html line 240, h3 id='conventions') and the sentence 'the conventions of Rung 3 define it in full' points to it; the definition of clipping is in the conventions list (line 245)."),
    dict(id="project-hours", check="2.9-hours", location="course/modules/M/M3/project.html line 33 and hours table lines 256-265; index.html line 29", status="PASS",
         evidence="Hours table components 2+3+14+8+12+6 = 45 (equals data-hours-project=45 on project.html line 33). Hub index.html line 29 sets data-hours-lessons=105 and data-hours-project=45 (sum 150). Lesson data-hours L01..L09 = 12, 11, 12, 12, 12, 11, 11, 12, 12 = 105. Component hours are design targets (ruling on hours)."),
    dict(id="project-proof-A1", check="2.4-mathematics", location="course/modules/M/M3/project.html Appendix A1 (line 635)", status="PASS",
         evidence="Re-derived: A = V Lambda V^T (spectral theorem, Theorem 2.3 of Lesson 4 under F1 to F4, which L04.html states as 'Theorem 2.3 (the spectral theorem for symmetric matrices)'); X = V Lambda_f V^T is symmetric; z^T X z = sum max(lambda_i, f) (V^T z)_i^2 >= 0 for f >= 0. Hypotheses named: real symmetric A, f >= 0, F1 to F4."),
    dict(id="project-proof-A2", check="2.4-mathematics", location="course/modules/M/M3/project.html Appendix A2 (line 636)", status="PASS",
         evidence="Re-derived: Y_ii = X_ii / (sqrt(d_i))^2 = 1; z^T Y z = q^T X q with q = D^{-1/2} z, so Y is PSD; positivity of d_i used for the division and stated."),
    dict(id="project-proof-A3", check="2.4-mathematics", location="course/modules/M/M3/project.html Appendix A3 (line 637)", status="PASS",
         evidence="Re-derived: det Sigma = a^2 b^2 (1 - rho^2) > 0; Sigma^{-1} iota = (b(b - rho a), a(a - rho b)) / det Sigma; sum of components a^2 + b^2 - 2 rho a b = (a - b)^2 + 2ab(1 - rho) > 0 for |rho| < 1, a, b > 0; scaling by c > 0 multiplies numerator and denominator by c^2 (weights unchanged). Checked numerically against the two-asset formula in grader test_weights_two_asset_closed_form."),
    dict(id="project-proof-A4", check="2.4-mathematics", location="course/modules/M/M3/project.html Appendix A4 (line 637)", status="PASS",
         evidence="Re-derived: C = V Lambda V^T with lambda_i < 0; u_i = column i of V; X = V Lambda_0 V^T gives X u_i = V Lambda_0 e_i = 0, so X singular; with positive diagonal, z = D_X^{1/2} u_i gives Y z = D_X^{-1/2} X u_i = 0; Sigma S^{-1} z = S Y z = 0. Argument is complete under F1 to F4 and the positive-diagonal hypothesis."),
    dict(id="project-conventions-math", check="2.4-mathematics", location="course/modules/M/M3/project.html Conventions (lines 242-248)", status="PASS",
         evidence="Weights: w = Sigma^{-1} iota / (iota^T Sigma^{-1} iota) sums to 1 (divide by the sum of the components); clipping of a matrix with a negative eigenvalue at floor 0 is singular (A4); 'the formula does not require C to be PSD' holds because the formula uses only Sigma^{-1} iota. The four ValueError conditions match test_project.py and reference.py (named sites in gate-named-conditions)."),
    dict(id="project-psd-tolerances", check="2.6-autograder-spec", location="course/modules/M/M3/project.html line 243; grader/test_project.py test_clip_repair_is_positive_semidefinite, test_projection_repair_is_a_valid_repair", status="PASS",
         evidence="Page: clipping PSD to -1e-9, projection PSD to -1e-8. Tests: min_eig(y) >= -1e-9 for clip_repair (line 386) and min_eig(y) >= -1e-8 for projection_repair (line 466). Match."),
    dict(id="project-spec-signatures", check="2.6-spec", location="course/modules/M/M3/project.html line 233; grader/starter.py lines 15-35; test_project.py calls", status="PASS",
         evidence="Signatures on the page and starter: min_eigenvalue(matrix); is_psd(matrix, tol=1e-10); clip_repair(matrix, floor=0.0); projection_repair(matrix, tol=1e-10, max_iter=500); comparison_weights(corr, vols). The test file calls each with these names and parameters."),
    dict(id="project-lab3-copy-instructions", check="2.5-labs", location="course/modules/M/M3/project.html lines 289-296 and Lab 3 code", status="PASS",
         evidence="Lab 3 code defines the six functions named on line 289 (jacobi_eigen, psd_projection, min_eigenvalue, clip_repair, projection_repair, comparison_weights) plus determinant and frobenius, which the page says stay. Twin run prints the lines in the expected block (run_labs PASS)."),
    dict(id="project-rung-labs", check="2.5-labs", location="course/modules/M/M3/project.html Labs 1-3; tests/labs/M3/lab-M3-project-1..3.py", status="PASS",
         evidence=f"run_labs M3 PASS (12/12) includes the three project labs ({OUT3}/run_labs.out); the completion lab's non-blank lines equal the twin (blanks are '___'); lab hypotheses agree with the printed output (checked in project-numbers). Runtime: page_smoke lab timings 0.0 s."),
    dict(id="project-spec-grader", check="2.6-spec", location="course/modules/M/M3/project.html lines 225-238; index.html placement section", status="PASS",
         evidence="Spec items present: function list, four named ValueError conditions, 'No function prints or warns', 'A run in your browser stops after 120 seconds' (matches python.js), 155 tests (collect-only 155), grader panel attributes (data-packages='numpy' is what grader.js loads). Placement link index.html#placement exists (index.html line 68, id='placement')."),
    dict(id="project-exemplars", check="2.6-rubric-calibration", location="course/modules/M/M3/project.html exemplar A (line 504) and exemplar B (line 569)", status="PASS",
         evidence="Scored each exemplar against the rubric (lines 492-496). Exemplar A: C1 2 (verdicts without tolerance; wrong sentence about clipping), C2 2 (rounded weights; no repair weights), C3 2 (nearer repair named without distances), C4 1 (no input labelled), C5 2 (one limitation; recommendation not tied to a number): matches official 2,2,2,1,2. Exemplar B: C1 4, C2 4, C3 4, C4 3 (no 'no market claim' statement), C5 3 (direction only for clipping): matches official 4,4,4,3,3. Note: I read the annotations before scoring, so this is not a blind scoring."),
    dict(id="project-rubric", check="2.6-rubric", location="course/modules/M/M3/project.html rubric table lines 486-499", status="PASS",
         evidence="Five criteria, four levels each (table rows C1-C5 with data-criterion). Descriptors checked for observability; each level names a checkable element (tolerance, printed number, named proof, named test, limitation direction)."),
    dict(id="project-references", check="1.1-citations", location="course/modules/M/M3/project.html lines 665-669; references/references.json", status="PASS",
         evidence="Both keys (axler2024linear, strang2023introduction) are status 'verified' with used_by ['M3'] in references.json. Axler: plain curl to api.crossref.org returns title 'Linear Algebra Done Right', 2024, Springer, author Axler (out3/axler_crossref.txt). Strang: verified in the registry (Open Library), not re-checked live. The page attributes no passage to either."),
    dict(id="project-no-process-words", check="2.9-prose", location="course/modules/M/M3/project.html and grader/starter.py, test_project.py", status="PASS",
         evidence="grep for builder, verifier, ledger, gate, round, fragment, draft, reviewer, fixer, TODO, TBD, lorem, ellipsis, 'for brevity', 'it is important', 'obviously', 'clearly': no hits in project.html or the learner-facing grader files."),
    dict(id="project-stretch", check="2.9-prose", location="course/modules/M/M3/project.html lines 655-661", status="PASS",
         evidence="The three stretch items make no claim; item 2 asks for the count the learner finds and forbids extending it to unseen matrices."),
    dict(id="notation-registry", check="2.4-notation", location="course/modules/M/M3/project.html KaTeX; cards.json", status="PASS",
         evidence="Macros in project KaTeX: \\diag (registered), \\top, \\Lambda, \\Sigma, \\rho, \\iota, \\lVert, \\rVert, \\boldsymbol, \\det, \\max (KaTeX built-ins; \\top is used in 35 module pages). Single-letter symbols (A, B, C, D, S, V, X, Y, Z, F, a, b, c, d, k, m, q, u, v, w, z, i) do not collide with the registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (notation/notation.json). Cards use no registered symbol with another meaning."),
    dict(id="notation-R-macro", check="2.4-notation", location="course/modules/M/M3/project.html; cards.json", status="PASS",
         evidence="grep: no \\mathbb or \\R in project.html; cards.json contains no LaTeX."),
    dict(id="dag-linked-concepts", check="2.9-dag", location="course/modules/M/M3/project.html concept links", status="PASS",
         evidence="Links: eigendecomposition -> L03.html#def-eigendecomposition, spectral-theorem -> L04.html#def-spectral-theorem, positive-semidefinite-matrix -> L05.html#def-positive-semidefinite-matrix. The anchors exist in L03, L04, L05 (grep of id=) and each lesson precedes the project."),
    dict(id="dag-m4-concepts-by-name", check="2.9-dag", location="course/modules/M/M3/project.html; grader/starter.py", status="PASS",
         evidence="Plain words covariance, correlation, variance appear in project.html without a concept link; plans/FINAL-ARCHITECT-RULINGS.md ruling 3 permits this for M3."),
    dict(id="hours-arithmetic", check="2.9-hours", location="course/modules/M/M3/index.html line 29; L01..L09 data-hours; project.html line 33", status="PASS",
         evidence="Lesson data-hours 12+11+12+12+12+11+11+12+12 = 105 = data-hours-lessons (index.html line 29); project 45; total 150 (curriculum M3 hours 150, curriculum/01-foundations.yaml line 160)."),
    # ---- cards
    dict(id="cards-structure", check="2.7-structure", location="course/modules/M/M3/cards.json (203 cards)", status="PASS",
         evidence=f"Ids unique (203); every lesson in L01..L09 has cards; grades in {{T, C}} where present; 49 cards carry no grade (definitions and misconceptions; plan section 13 grades only theorems, derivations and lab outputs); no cite keys; tools/check_pages.py cards checks pass (gate-check-pages)."),
    dict(id="cards-id-sequence", check="2.7-structure", location="course/modules/M/M3/cards.json ids", status="PASS",
         evidence="Ruling 2 (plans/FINAL-ARCHITECT-RULINGS.md): ids need not be sequential. Gaps (M3-c102, c148, c191 absent) and appended out-of-order ids (c204..c206) are not defects. check_pages.py only requires the pattern M3-cNNN and uniqueness."),
    dict(id="cards-numbers-cited", check="2.7-numbers", location="course/modules/M/M3/cards.json vs L01..L09.html", status="PASS",
         evidence=f"{SCRIPTS}/cards_labels_r3.py over all 203 cards: every Definition/Theorem/Proposition/Lemma/Fact/Example/Remark/Corollary/Problem label cited in a card appears in that card's lesson text (lesson text extracted by {SCRIPTS}/extract_lessons_r3.py). 'Section 1' hits (c115, c130, c197) are the section-number headings of L07 and L08. Output: {OUT3}/cards_labels_r3.out."),
    dict(id="cards-duplicate-scan", check="2.7-duplicates", location="course/modules/M/M3/cards.json (all pairs)", status="PASS",
         evidence=f"Full pairwise scan ({SCRIPTS}/cards_labels_r3.py, difflib): 8 front-or-back pairs at >= 0.80 and 39 back pairs at >= 0.60 were read. Each pair asks different facts: e.g. c017 (R^4 count 198/200) vs c019 (R^3 count 0/200); c087 (PSD) vs c088 (PD); c194/c195/c196 (symmetry, idempotence, residual orthogonality); c025 (kernel) vs c187 (image); c154 vs c157 (clipping produces vs leaves unchanged). No semantic duplicate."),
    dict(id="cards-sample-10", check="2.7-sample", location="course/modules/M/M3/cards.json, every 10th card in file order", status="PASS",
         evidence="Sampled (index 0,10,...,200): c001, c011, c021, c031, c041, c051, c061, c071, c081, c091, c101, c112, c122, c132, c142, c153, c163, c173, c183, c194, c204. Each back checked against its lesson statement (e.g. c011 Proposition 3.5 pivots; c051 Proposition 2.2; c081 Definition 1.3 Gram matrix; c091 Remark 2.7; c122 least-squares definition; c153 Definition 3.1; c183 Proposition 3.3 and Example 3.6 (0.04 = 0.2^2; A - A_0 = [[-0.1, 0.1],[0.1, -0.1]])). Output: this verifier's reading of L01..L09 statements (see the lesson cards rows)."),
    dict(id="cards-lab-numbers", check="2.7-numbers", location="cards c017, c019, c038, c096, c111, c127, c162, c163, c173, c175, c177", status="PASS",
         evidence=f"Lab twins run (out3/run_labs.out and direct runs): L01 'R^4, 4 vectors: independent in 198 of 200' and 'R^3, 4 vectors: 0 of 200'; L02 '50 of 50 pairs'; L05 '500 of 500' and '100000 of 100000'; L06 planted rank-2 singular values above 1e-10 relative: 2; L07 'rank of A^T A with a duplicated column: 2 (of 3)' and residual norm 0.8951; L09 'passes is_correlation and is strictly closer: 23 of 23' and non-PSD count 23. Every quoted count matches."),
    dict(id="cards-c131", check="2.7-changed", location="course/modules/M/M3/cards.json M3-c131", status="PASS",
         evidence="Changed in round 2 (reworded). Back: 'M is symmetric, and x^T M x = ||X~ x||^2/(T-1) >= 0 (Proposition 1.1)'. L08 Proposition 1.1 (M is symmetric and positive semidefinite) and its proof give exactly this."),
    dict(id="cards-c204", check="2.7-duplicates", location="course/modules/M/M3/cards.json M3-c204 vs M3-c101", status="PASS",
         evidence="Round-2 FAIL (duplicate of c101) is resolved: c101 now reads 'A square real matrix Q whose columns are orthonormal (Definition 1.1).' and c204 asks for the two identities Q^T Q = I and Q Q^T = I (L09 Definition 1.2a states exactly these). Different facts."),
    dict(id="cards-L01", check="2.7-cards", location="cards M3-c001..c022, c169, c170 (L01)", status="PASS",
         evidence="Sampled c001 (Definition 1.1 vector space), c011 (Proposition 3.5), c021 (Corollary 3.6): agree with L01 text. c017 and c019 lab counts match the twin."),
    dict(id="cards-L02", check="2.7-cards", location="cards M3-c023..c042, c184, c187 (L02)", status="PASS",
         evidence="Sampled c031 (Theorem 2.4 coordinate identity) and c041 (Proposition 3.1 composition; matrices [[1,1],[0,1]], [[1,0],[1,1]] give AN = [[2,1],[1,1]] and NA = [[1,1],[1,2]], checked by hand). c038 lab count 50 of 50 matches the twin."),
    dict(id="cards-L03", check="2.7-cards", location="cards M3-c043..c062, c171, c172, c188 (L03)", status="PASS",
         evidence="Sampled c051 (Proposition 2.2) and c061 (Proposition 2.3 with the I_2 example; eigenspace dimension 1 for the non-diagonalisable B) match L03 text labels."),
    dict(id="cards-L04", check="2.7-cards", location="cards M3-c063..c078, c189, c190, c192 (L04)", status="PASS",
         evidence="Sampled c071 (Proposition 2.4) matches L04. c067 and c192 (Lemma 1.4, F1) match L04 text. c206 (orthogonal matrix via column inner products) matches L04 Definition 1.2 'A real square matrix Q is orthogonal when its columns are orthonormal'."),
    dict(id="cards-L05", check="2.7-cards", location="cards M3-c079..c100, c173, c176, c179, c180, c193, c203 (L05)", status="PASS",
         evidence="Sampled c081 (Definition 1.3 Gram matrix) and c091 (Remark 2.7 non-uniqueness of the factor). c087/c088 (Theorems 2.1, 2.2) agree with L05; c173 and c096 lab counts match the twin."),
    dict(id="cards-L06", check="2.7-grades", location="cards M3-c101..c114, c178 (L06); c178 = M3-c178", status="FAIL",
         evidence="c101 (Definition 1.1) and c112 (Theorem 2.3 example, A = [[0,1],[0,0]]) agree with L06. M3-c178 states the theorem result 'The number of positive singular values equals the rank of A (Theorem 2.2, under F1 to F4)' with no grade. plans/M3-build-plan.md section 13: 'Grade T for every theorem and derivation'.",
         fix="Set \"grade\": \"T\" on M3-c178 in course/modules/M/M3/cards.json (the card cites Theorem 2.2 of L06)."),
    dict(id="cards-L07", check="2.7-grades", location="cards M3-c115..c129, c168, c177, c194..c196 (L07)", status="FAIL",
         evidence="Agree with L07: c122 (least-squares definition), c194 (Theorem 1.2(c) symmetry), c195 (P^2 = P), c196 (Theorem 2.2(c) residual orthogonality), c177 (rank 2 of 3). Two defects: (1) M3-c168 states 'by Theorem 2.2(c) it equals the orthogonal projection P y' with no grade; (2) M3-c127 is graded T but its answer quotes the lab's printed residual norm 0.8951 (L07 lab output, verified by running the twin); plan section 13 grades lab-output results C with a basis.",
         fix="(1) Set \"grade\": \"T\" on M3-c168. (2) Split M3-c127: keep the T misconception (the residual is orthogonal, not zero) and move the 0.8951 example to a separate card with \"grade\": \"C\" and \"basis\": \"Lab 1 (residual norm)\", or drop the number from the T card."),
    dict(id="cards-L08", check="2.7-cards", location="cards M3-c130..c145, c174, c186, c197..c201 (L08)", status="PASS",
         evidence="Sampled c132 (trace identity, Proposition 1.2), c136 (Corollary 2.2), c142 (Definition 3.1 'orthonormal by construction', matches L08 text), c201 (Corollary 2.2 maximum (T-1) lambda_1 at v_1). c131 checked (changed). Section numbers in L08 headings confirm 'Section 1'."),
    dict(id="cards-L09", check="2.7-cards", location="cards M3-c146..c167, c175, c181..c183, c185, c202, c204 (L09)", status="PASS",
         evidence="Sampled c151 (Remark 2.2: neither existence nor uniqueness proved), c153 (Definition 3.1 clipping), c182 (Method 2: 10^-12 and 500 steps, as L09 line 93 states), c183 (Proposition 3.3, Example 3.6), c202 (Method 2 does not guarantee PSD). Lab counts c163, c175 (23 and 23 of 23) match the twin."),
    dict(id="cards-L01-L09-changed-in-round2", check="2.7-changed", location="cards M3-c101, c131, c204, c205, c206", status="PASS",
         evidence="c205 (L06, grade T): 'Yes, assuming F1 of Lesson 4 (Fact 1.2) ... M = Q^T and N = Q' matches L06 Fact 1.2 proof. c206 (L04): matches L04 Definition 1.2. c101, c131, c204 checked above."),
]


def main() -> None:
    ms = mutants()
    rows = ROWS
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate row ids"
    passed = sum(1 for r in rows if r["status"] == "PASS")
    failed = sum(1 for r in rows if r["status"] == "FAIL")
    killed = sum(1 for m in ms if m["killed_by"])
    fragment = {
        "unit": "M3",
        "slice": "d",
        "round": 3,
        "verifier": "independent Haiku verifier, slice d, round 3 (not a builder of M3)",
        "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
        "base": "c737272f (round-2 pin)",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-M3-d",
        "scratch": f"{SCRIPTS}/ (scripts) and {OUT3}/ (outputs)",
        "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
        "verdict": "FAIL" if failed or any(r["status"] != "PASS" for r in rows) or killed != len(ms) else "PASS",
        "rows": rows,
        "mutants": ms,
        "registry_flags": [],
        "freshness_flags": [],
        "notes": NOTES,
        "summary": (
            f"M3 slice d round 3 on pin a007712: verdict FAIL. Rows {len(rows)}: PASS {passed}, FAIL {failed}, "
            f"UNVERIFIABLE 0. Mutants {killed}/{len(ms)} killed on seeds 0-9 (survivors: v3d_01, vd3_01..vd3_04). "
            "Failing rows: gate-mutate-m3, grader-test-count-and-purity, grader-standard-library-only, "
            "mutants-v3d-01-max-iter-plus-one, equivalent-r6d-m04, equivalent-r11d-m02, equivalent-r15d-m03-label, "
            "equivalent-readme-citation, cards-L06, cards-L07."
        ),
    }
    out = ROOT / "ledgers/M3/M3-d.json"
    out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", out, "rows", len(rows), "pass", passed, "fail", failed, "mutants", len(ms), "killed", killed)


NOTES = (
    "Round 3 on pin a007712 (round-2 pin c737272). Delta read in full for slice d: project.html (hunks at lines 53, 233-235, 242-247, 273, 293, 597, 609, 622), grader/starter.py docstring, cards.json (c101 reworded; c205, c206 added), tests/labs/M3/lab-M3-L09-1.py (not in slice d; L09 lab run via run_labs), L07/L08/L09 pages (lesson prose, not in slice d), mutants (v2d_01..05 present; v2d_06 retired), equivalent/README. "
    "Pre-existing uncommitted state in the checkout when this verifier started: a modified ledgers/M3/M3-d.json (overwritten by this fragment), untracked ledgers/M3/mutants/vd3_01..vd3_04 (kept and re-validated by this verifier; provenance not from this verifier), and untracked older scripts under ledgers/M3/scripts/M3-d-r3/ (cards_numbers.py, gates.sh, run_alts.py, proposed_fix_tests.py and others, NOT used for any row here) and out/ with an earlier run's outputs (not relied on). This verifier's own scripts and outputs are the ones named in evidence (run_alts_r3.py, verifier_make_mutants_r3.py, project_numbers_r3.py, equiv_output_diff_r3.py, cards_labels_r3.py, extract_lessons_r3.py, instances_sample_r3.py, verifier_build_fragment_r3.py; outputs in out3/). "
    "Mutants written by this verifier: v3d_01..v3d_05 (ledgers/M3/mutants/), generated by verifier_make_mutants_r3.py from the reference with one exact replacement each. "
    "Not checked or limited: (1) lesson prose L01..L09 and the lesson pages' page_smoke and index.html were not re-read in this slice (other slices); the round-2 prose-L01..L09 rows are not re-issued here; (2) verify_refs was not run live; Strang 2023 was not re-read live (registry says Open Library verified); (3) the 203 cards were not read line by line against lesson text: label, grade, duplicate and lab-number checks ran on all cards and statements were read for the 21 sampled cards plus the changed cards and the grade-flagged cards; (4) equivalence of the three equivalent/ files was tested numerically on seeds 0-49 only, not proved; (5) the exemplar scores were read after the annotations, so they are not blind; (6) no exhaustive proof of the mutant equivalence was attempted; (7) the NumPy-based alternatives were not checked for numerical robustness beyond seeds 0-49; (8) page_smoke was run for project.html only; (9) no git commit or push. "
    "Hours: component hours are design targets (ruling), not checked against an independent estimate. Freshness: no debate brief; no registry flag."
)

if __name__ == "__main__":
    main()
