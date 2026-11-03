"""Build ledgers/M3/M3-d.json for M3 slice d, round 3 (verifier scratch; run from the checkout)."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD3-M3-d")
OUT = ROOT / "ledgers/M3/scripts/M3-d-r3/out"
MUT = ROOT / "ledgers/M3/mutants"
CARRY = "Carried from round 2 (files byte-identical since the previous pin c737272): "
R = []


def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        d["fix"] = fix
    R.append(d)


# ---- gates (run this round at pin a007712)
row("gate-check-pages", "gate: tools/check_pages.py --all (M3 line)", "course/modules/M/M3/*", "PASS",
    "out/check_pages.out: 'check_pages M3: PASS', exit 0.")
row("gate-check-dag", "gate: tools/check_dag.py --all (M3 line)", "course/modules/M/M3/*", "PASS",
    "out/check_dag.out: 'check_dag M3: PASS', exit 0.")
row("gate-check-projects", "gate: tools/check_projects.py --all (M3 line)", "course/modules/M/M3/project.html", "PASS",
    "out/check_projects.out: 'check_projects M3: PASS', exit 0.")
row("gate-run-graders", "gate: tools/run_graders.py --unit M3 --seeds 0-49", "course/modules/M/M3/grader/", "PASS",
    "out/run_graders.out: 'run_graders M3: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0.")
row("gate-run-labs", "gate: tools/run_labs.py --unit M3 (12 twins; page code = twin; expected = output)",
    "course/modules/M/M3/L0*.html, project.html", "PASS",
    "out/run_labs.out: 'run_labs M3: PASS (12/12)', exit 0. Each twin also run alone with python -I -W error: out/twins_alone.out, 12 x exit 0.")
row("gate-page-smoke", "gate: tools/page_smoke.py --unit M3 --pages <one page> (project, L01..L09, index)",
    "course/modules/M/M3/*.html", "PASS",
    "out/page_smoke_{project,L01..L09,index}.out: each 'page_smoke M3: PASS' and exit 0.")
row("gate-ruff", "gate: ruff check and ruff format --check on grader and tests/labs/M3",
    "course/modules/M/M3/grader/, tests/labs/M3/", "PASS",
    "out/ruff.out: 'All checks passed!' exit 0; '16 files already formatted' exit 0.")
row("gate-mypy", "gate: mypy --no-incremental on reference.py, instance.py, starter.py",
    "course/modules/M/M3/grader/", "PASS", "out/mypy.out: 'Success: no issues found in 3 source files', exit 0.")
row("gate-verify-refs", "gate: tools/verify_refs.py --offline", "references/references.json", "PASS",
    "out/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. No reference changed in M3 this round.")
row("gate-collect-only", "project.html test count (155) equals real collect-only count",
    "course/modules/M/M3/project.html line 237 vs grader/test_project.py", "PASS",
    "QF_SEED=0 .venv/bin/python -I -m pytest --collect-only -q -p no:cacheprovider test_project.py in /tmp/m3d_r3_coll (test_project.py, instance.py, reference.py as covariance_doctor.py): '155 tests collected'. The same run against the reference: '155 passed'. project.html line 237 says 155 tests.")
row("gate-pytest-relevant", "gate: pytest tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py",
    "tests/", "PASS", "out/pytest_relevant.out: all dots, exit 0.")
row("gate-mutate-m3", "gate: tools/mutate_graders.py --unit M3 --seeds 0-9 (exit 0 required)",
    "ledgers/M3/mutants/*.py (137 files)", "FAIL",
    "out/mutate_M3_seeds0-9_with_vd3.out: 'mutate_graders M3: FAIL (133/137 killed)', exit 1. SURVIVED: vd3_01_comparison_weights_symmetrises_caller_corr_in_place.py, vd3_02_min_eigenvalue_symmetrises_caller_matrix_in_place.py, vd3_03_is_psd_symmetrises_caller_matrix_in_place.py, vd3_04_min_eigenvalue_uses_scipy_not_allowed_by_page.py. All 133 others killed on seed 0 or on the seed named in the output. v2d_06 is no longer in mutants/ (moved to retired/).",
    fix="Add to grader/test_project.py the two checks in ledgers/M3/scripts/M3-d-r3/proposed_fix_tests.py: (a) min_eigenvalue, is_psd and comparison_weights must not change an asymmetric-within-tolerance matrix they are given (kills vd3_01..03); (b) an AST import check that only the standard library and NumPy are imported (kills vd3_04). Verified in a scratch copy: reference and all six alternatives pass both checks on seeds 0-9. Then rerun the gate; it must exit 0.")
row("gate-reference-starter", "starter.py signatures match project.html 'Required outputs'; reference passes",
    "course/modules/M/M3/grader/starter.py lines 15-37; project.html line 233", "PASS",
    "starter.py defines min_eigenvalue(matrix), is_psd(matrix, tol=1e-10), clip_repair(matrix, floor=0.0), projection_repair(matrix, tol=1e-10, max_iter=500), comparison_weights(corr, vols), as the page lists them. reference.py passes all 155 tests (QF_SEED=0) and 50/50 seeds (run_graders).")
row("gate-alternatives-seeds-0-49", "six alternatives pass the suite on seeds 0-49",
    "ledgers/M3/alternatives/", "PASS", "out/alternatives_seeds_0-49.out: alt1..alt6 each 50/50 pass (ledgers/M3/scripts/M3-d-r3/run_alts.py).")
row("gate-named-conditions", "ValueError asserted only for the four named conditions",
    "course/modules/M/M3/grader/test_project.py (must_raise sites)", "PASS",
    "grep: 9 must_raise( call sites in test_project.py, one helper. They cover: non-square (4 matrix functions x 3 shapes, plus comparison_weights), asymmetry beyond 1e-9 (4 matrix functions, comparison_weights), volatility not strictly positive (zero, negative, NaN, first/middle/last), length mismatch (empty, shorter, longer). Every other test asserts a value or a property. Matches project.html Conventions 'The four named ValueError conditions'.")

# ---- grader
row("grader-instance", "grader/instance.py matches the project.html Inputs paragraph",
    "course/modules/M/M3/grader/instance.py lines 1-15, 24-109; project.html Rung 3 Inputs", "PASS",
    "k drawn from {3,4,5} (line 90); vols in [0.05,0.40] (line 91); corr unit diagonal (line 59 and 54-62); redrawn until smallest eigenvalue < -_MARGIN = -0.02 (lines 24, 93), matching 'not positive semidefinite by a margin of 0.02'; psd_corr positive definite (lines 65-69); spectrum and psd_spectrum with first entry exactly 0 (lines 96-97); orthonormal eigenvectors (lines 72-83); label 'SIMULATED' (line 101).")
row("grader-test-count-and-purity", "test count and purity tests",
    "course/modules/M/M3/grader/test_project.py", "PASS",
    "155 collected (gate-collect-only). Purity: test_functions_print_nothing (line 744) and test_repeated_calls_agree (line 775). Argument-mutation coverage is incomplete; see grader-no-argument-mutation.")
row("grader-lab3-reference-numbers", "Lab 3 printed numbers are matched by the suite",
    "grader/test_project.py test_lab3_reference_numbers_are_matched (line 508); project.html Lab 3 expected block", "PASS",
    "The test passes on reference.py (155 passed). Lab 3 run this round prints smallest eigenvalue -0.142113, distances 0.176573 (clip) and 0.175003 (projection), gap 0.001570, largest entry difference 0.011516, weights 1.778929 -1.096718 -0.255613 0.573402; the test's checks use the same numbers.")
row("grader-browser-timeout", "120-second browser run limit",
    "course/assets/js/python.js line 4 (TIMEOUT_MS = 120000); project.html Constraints", "PASS",
    "python.js line 4 TIMEOUT_MS = 120000 matches 'A run in your browser stops after 120 seconds'. course/assets is byte-identical to the round-2 pin.")
row("grader-standard-library-only", "'The standard library and NumPy only' is enforced or does not survive as a mutant",
    "course/modules/M/M3/project.html line 235 (Constraints); grader/starter.py line 8; grader/test_project.py (no import test)", "FAIL",
    "project.html Constraints: 'The standard library and NumPy only.' starter.py line 8: 'Use the standard library and NumPy only.' No test in test_project.py inspects imports. vd3_04_min_eigenvalue_uses_scipy_not_allowed_by_page.py (min_eigenvalue calls scipy.linalg.eigvalsh) survives seeds 0-9 (out/mutate_M3_seeds0-9_with_vd3.out). Round 2 raised the same gap; this round relaxed the wording to NumPy (consistent with plan Q3) but added no check.",
    fix="Add an AST import test to grader/test_project.py: every import in covariance_doctor.py must be in sys.stdlib_module_names or be numpy (proposed_fix_tests.py::test_fix_std_lib_and_numpy_imports_only). It kills vd3_04 and passes the reference and all six alternatives on seeds 0-9.")
row("grader-no-argument-mutation", "'No function changes its arguments' is tested for every function",
    "course/modules/M/M3/project.html Constraints (line 235); grader/test_project.py test_inputs_are_not_mutated (line 755)", "FAIL",
    "The constraint is stated on the page. test_inputs_are_not_mutated passes exact-symmetric corr to min_eigenvalue and is_psd, and passes an asymmetric-within-tolerance matrix only to clip_repair and projection_repair; comparison_weights never receives an asymmetric-within-tolerance matrix in any purity test. vd3_01_comparison_weights_symmetrises_caller_corr_in_place.py, vd3_02_min_eigenvalue_symmetrises_caller_matrix_in_place.py and vd3_03_is_psd_symmetrises_caller_matrix_in_place.py (each writes the symmetrised average back into the caller's matrix after validating it) all survive seeds 0-9.",
    fix="Extend test_inputs_are_not_mutated (or add a sibling test) to call min_eigenvalue, is_psd and comparison_weights on an asymmetric-within-tolerance copy (symmetric_pair(..., 1e-10)) and assert the copy is unchanged. proposed_fix_tests.py::test_fix_inputs_not_mutated_by_scalar_functions does this: it kills vd3_01..03 and passes the reference and all six alternatives (seeds 0-9).")
row("grader-reference-docstring", "reference.py docstring and the stdlib-only claim",
    "course/modules/M/M3/grader/reference.py lines 1-5", "PASS",
    "Docstring: 'Pure Python, standard library only.' reference.py imports only math and collections.abc, so the claim is true for the reference. The reference is not shipped to learners.")

# ---- alternatives
row("alternatives-five-standard-library", "five correct alternatives obey the stated constraint",
    "ledgers/M3/alternatives/*.py; project.html line 235", "PASS",
    "Round 2 FAIL cleared: the page now permits NumPy (project.html line 235; starter.py line 8; plans/M3-build-plan.md Q3 'NumPy yes'). alt1, alt3, alt6 import numpy; alt2, alt4, alt5 import only math and collections.abc (grep of import lines). All six conform.")
row("alternatives-seeds-0-49", "alternatives pass seeds 0-49 with the suite",
    "ledgers/M3/alternatives/", "PASS",
    "out/alternatives_seeds_0-49.out: alt1..alt6 each 50/50 seeds pass (-W error, --assert=plain). The new fix tests also pass on all six for seeds 0-9 (proposed_fix_tests.py run).")

# ---- mutants
row("mutants-existing-128", "pre-existing student-error mutants are killed",
    "ledgers/M3/mutants/ (128 files not named v2d_* or vd3_*)", "PASS",
    "out/mutate_M3_seeds0-9_with_vd3.out: all 128 are KILLED (killed_by named in the output).")
row("mutants-new-student-errors", "vd1_01..05 (round 2) killed", "ledgers/M3/mutants/vd1_0[1-5]*.py", "PASS",
    "out/mutate_M3_seeds0-9_with_vd3.out: all five KILLED.")
row("mutants-v2d-01-05", "v2d_01..05 (round 2) killed", "ledgers/M3/mutants/v2d_0[1-5]*.py", "PASS",
    "out/mutate_M3_seeds0-9_with_vd3.out: all five KILLED.")
row("mutants-v2d-06", "round-2 survivor v2d_06 (eigh uses numpy) disposition",
    "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py; ledgers/M3/equivalent/README.md", "FAIL",
    "v2d_06 was removed from mutants/ and placed in retired/. The page now permits NumPy, so the mutant does not violate the page. Ruling 9 requires such a mutant to go to equivalent/ with a README proof; retired/ is not documented, and equivalent/README.md does not list it.",
    fix="Move the file to ledgers/M3/equivalent/ and add a README entry citing project.html line 235 and plans/M3-build-plan.md Q3 as the proof that the numpy import is permitted.")
row("mutants-docstring-first-line", "every mutant's first docstring line names the student error (ruling 9)",
    "ledgers/M3/mutants/r15d_m01_is_psd_strict_boundary.py; ledgers/M3/mutants/r15d_m02_rescale_missing_sqrt_on_column.py", "FAIL",
    "Both files open with the reference header 'Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.' The mutate output therefore reports the mutants under that text (out/mutate_M3_seeds0-9_with_vd3.out lines for r15d_m01 and r15d_m02). The errors are: is_psd uses 'min_eigenvalue(matrix) > -tol' (strict), and _rescale divides by 'math.sqrt(d[i]) * d[j]' instead of 'math.sqrt(d[i] * d[j])'. Both are killed.",
    fix="Replace the first docstring line of each file with the error, for example 'is_psd uses a strict inequality, so a smallest eigenvalue exactly -tol is refused.' and 'rescaling divides by sqrt(d_i) * d_j instead of sqrt(d_i * d_j).'")
row("mutants-new-round3-written", "round-3 student-error mutants (vd3_01..04) are complete modules with the error on the first docstring line",
    "ledgers/M3/mutants/vd3_01..04", "PASS",
    "Written by ledgers/M3/scripts/M3-d-r3/verifier_make_mutants_round3.py from reference.py, one exact replacement each (asserted unique). Each module parses; ast.get_docstring first lines name the error. Three are in-place argument writes after validation, one is a scipy call. Their survival is recorded in the gate and grader rows above.")
row("equivalent-r6d-m04", "equivalent: stop on gap alone",
    "ledgers/M3/equivalent/r6d_m04_projection_stops_on_gap_only.py; README.md line 8", "PASS",
    "out/equivalent_seeds_0-49.out: 50/50 pass. The only change from reference.py is the stop test (gap alone) and docstrings. The page states no stop criterion (project.html line 660 asks the learner to vary tol and max_iter; line 233 says 'stops after at most max_iter alternating steps'). PSD follows within 1e-10 because the gap is at most tol.")
row("equivalent-r11d-m02", "equivalent: stop on step alone",
    "ledgers/M3/equivalent/r11d_m02_projection_stops_on_step_only.py; README.md line 9", "PASS",
    "out/equivalent_seeds_0-49.out: 50/50 pass. Only the stop test and docstrings differ from reference.py. Same page basis as r6d_m04 (no stop criterion stated).")
row("equivalent-r15d-m03-label", "equivalent: never stops early; README label matches the file",
    "ledgers/M3/equivalent/r15d_m03_projection_repair_never_stops_early.py; README.md lines 10-12", "PASS",
    "diff against reference.py: the stop test line becomes 'if gap <= tol and step <= tol and False:' and the docstring changes; nothing else. out/equivalent_seeds_0-49.out: 50/50 pass. 'At most max_iter' (line 233) is satisfied by running max_iter steps.")
row("equivalent-readme-citation", "README proof cites the page sentences it relies on",
    "ledgers/M3/equivalent/README.md lines 3-6; project.html lines 233 and 660", "PASS",
    "README cites project.html line 660 for the absence of a stop criterion (verified: line 660 is the 'stopping rule' stretch item and states no criterion). Non-blocking: the README does not cite line 233's 'at most max_iter' sentence, which r15d_m03 satisfies.")

# ---- project page
row("project-numbers", "every number on project.html equals a printed value or an arithmetic result",
    "course/modules/M/M3/project.html lines 57-60, 130-137, 213-220, 460-468, 469, 575, 609, 622, 657",
    "PASS",
    "Re-ran Lab 1, Lab 2 and Lab 3 (tests/labs/M3/lab-M3-project-1..3.py under python -I -W error); outputs equal the expected blocks and every number quoted in the prose: eigenvalues -0.275297 1.463830 1.811467, rebuilt diagonal 1.096064 1.104409 1.074824, repaired off-diagonals 0.636095 -0.382551 0.469578, Lab 2 expected 1.060165 1.075224 1.068322, Lab 3 smallest -0.142113, distances 0.176573 / 0.175003 / 0.001570, entry difference 0.011516, determinant -0.261600, weights 1.778929 -1.096718 -0.255613 0.573402 summing to 1. Exemplar A rounded weights 1.78 -1.10 -0.26 0.57 sum to 0.99 as stated. Hours and tests checked as separate rows.")
row("project-lab1-memo-sentence", "Exemplar B 'Repairs and their checks' passage (lab-printed values and the A2 hypothesis)",
    "course/modules/M/M3/project.html Exemplar B, 'Repairs and their checks' (around line 597)", "PASS",
    "Prints True at tolerance 1e-8 for the projection, the deviation 0.000000 for each repair, the smallest eigenvalue -0.142113 and the False verdict at 1e-10, all as printed. The counterfactual 'a zero or negative diagonal entry would have printed no value or a deviation of 2' matches the code path (zero: division by zero; mixed-sign negative: sqrt of a negative; both negative: deviation 2). It cannot arise for the clipped matrix, which A1 makes PSD. Non-blocking.")
row("project-conventions-link", "'Rungs 1 and 2' paragraph: eigenvector sentence and #conventions link",
    "course/modules/M/M3/project.html Rungs 1 and 2 paragraph (line 53); id=conventions (line ~96)", "PASS",
    "'An eigenvalue is a number λ for which Ax = λx has a nonzero solution x, called an eigenvector' is a correct definition; the anchor href='#conventions' resolves to id=conventions in the Rung 3 section.")
row("project-hours", "time budget and hub hours arithmetic",
    "course/modules/M/M3/project.html lines 33 and the hours table; index.html lines 29 and 39; L01..L09 data-hours",
    "PASS",
    "Table: 2 + 3 + 14 + 8 + 12 + 6 = 45 = data-hours-project (project.html line 33). Hub: data-hours-lessons 105 + data-hours-project 45 = 150. Lesson data-hours 12,11,12,12,12,11,11,12,12 sum to 105.")
row("project-proof-A1", "Appendix A1 (clipping gives a PSD matrix) is a complete proof",
    "course/modules/M/M3/project.html Appendix A (A1)", "PASS",
    "Re-derived: X = V diag(max(Λ_ii, f)) V^T; z^T X z = Σ max(Λ_ii,f)(V^T z)_i^2 ≥ 0 since max(Λ_ii,f) ≥ f ≥ 0. Hypotheses named (real symmetric, f ≥ 0, F1 to F4 of Lesson 4).")
row("project-proof-A2", "Appendix A2 (rescaling a PSD matrix with positive diagonal) is a complete proof",
    "course/modules/M/M3/project.html Appendix A (A2)", "PASS",
    "Re-derived: Y_ii = X_ii/(sqrt d_i)^2 = 1; z^T Y z = q^T X q ≥ 0 with q = D^{-1/2} z. The positive diagonal is named as the hypothesis.")
row("project-proof-A3", "Appendix A3 (two-asset weights and scaling) is a complete proof",
    "course/modules/M/M3/project.html Appendix A (A3)", "PASS",
    "Re-derived: det Σ = a²b²(1-ρ²) > 0; Σ^{-1} ι = (det Σ)^{-1}(b(b-ρa), a(a-ρb)); normalised weights (b(b-ρa), a(a-ρb))/(a²+b²-2ρab); denominator = (a-b)² + 2ab(1-ρ) > 0. Scaling by c>0 multiplies numerator and denominator by c², so weights are unchanged. The test test_weights_two_asset_closed_form checks the same formula.")
row("project-proof-A4", "Appendix A4 (singular clipped matrix, rescaled and Σ singular) is a complete proof",
    "course/modules/M/M3/project.html Appendix A (A4)", "PASS",
    "Re-derived: Xu_i = VΛ_0 e_i = 0 when Λ_ii < 0; z = D_X^{1/2} u_i gives Yz = D_X^{-1/2} X u_i = 0; S_v^{-1} z gives Σ S_v^{-1} z = S_v Y z = 0. All steps check.")
row("project-rung-labs", "project labs 1-3 exist, run, and match their pages",
    "course/modules/M/M3/project.html; tests/labs/M3/lab-M3-project-1..3.py", "PASS",
    "run_labs (12/12) includes the three project labs; completion twin (lab-M3-project-2) is the completed solution; the page has exactly two blanks (Step 3 and Step 5), matching the hypothesis.")
row("project-spec-grader", "specification and grader-section wiring",
    "course/modules/M/M3/project.html lines 233-237 and the grader panel (line ~272); grader/starter.py; index.html line 68", "PASS",
    "Signatures, file names, the report/ files, the 155-test count and data-packages='numpy' agree with starter.py, test_project.py and the NumPy decision (plans/M3-build-plan.md Q3). The enforcement gap is recorded in grader-standard-library-only.")
row("project-exemplars", "exemplar official scores equal their annotations",
    "course/modules/M/M3/project.html Exemplar A (data-scores 2,2,2,1,2) and B (4,4,4,3,3)", "PASS",
    "Exemplar A annotations: C1 level 2 met, 3 missed; C2 level 2 met, 3 missed; C3 level 2 met, 3 missed; C4 level 1; C5 level 2 met, 3 missed. Exemplar B: C1 4, C2 4, C3 4, C4 3 (level 4 missed), C5 3 (level 4 missed). Consistent with the official scoring line of each exemplar.")
row("project-rubric", "rubric has five criteria with four levels", "course/modules/M/M3/project.html table#rubric", "PASS",
    "Five rows (C1..C5), four level cells each, plus the 'meets the bar at level 3 or above' sentence. check_projects M3 PASS.")
row("project-references", "references and reading list", "course/modules/M/M3/project.html lines 665-669; references/references.json", "PASS",
    "data-cite axler2024linear and strang2023introduction: both status 'verified', used_by ['M3'] in references/references.json. The page attributes no statement to them, as its Reading paragraph says.")
row("project-no-process-words", "no process words in learner text", "course/modules/M/M3/*.html, grader/*.py, cards.json", "PASS",
    "grep (case-insensitive) for builder, verifier, ledger, architect, planner, TODO, FIXME, placeholder, orchestrat, haiku, agent, 'lab twin', 'this build': 0 hits. 'round' occurs only as numeric rounding.")
row("project-stretch", "stretch items", "course/modules/M/M3/project.html lines 656-661", "PASS",
    "Three open items (weighted distance; count over 200 seeded matrices per size with seeds stated; stopping rule). No numbers quoted, so nothing to check beyond wording.")

# ---- prose (slice a/b/c content; carried or re-read)
for n, why in [("L01", ""), ("L02", ""), ("L03", ""), ("L04", ""), ("L05", ""), ("L06", "")]:
    row(f"prose-{n}", f"{n} prose (carried; outside slice d)", f"course/modules/M/M3/{n}.html", "PASS",
        CARRY + f"{n}.html is not in the round-2..round-3 delta (git diff c737272..a007712 lists only L07, L08, L09 among the lesson pages).")
row("prose-L07", "L07 changed hunks (outside slice d; hunks re-read)", "course/modules/M/M3/L07.html", "PASS",
    "Changed: why-it-matters sentence now says 'a subspace (defined in Lesson 1)' (L01.html line 53 heading 'Vector spaces and subspaces'); the proof of (a) and the misconception use \\diag, a registered macro. Cited theorems exist: Theorem 1.2 (a)-(c), Theorem 1.3, Remark 1.4, Theorem 2.2 (a)-(c), Definition 1.1, Definition 2.1. Lab 1 expected output still matches the run.")
row("prose-L08", "L08 changed hunks (outside slice d; hunks re-read)", "course/modules/M/M3/L08.html", "PASS",
    "Changed: tenor is defined before the variables that use it; \\tr and \\diag are registered macros; Problems M1, M2 and the quiz item use \\tr and \\diag. Proposition 1.2 and Definition 1.3 keep their statements. Lab 1 outputs (75.9 18.1 5.2; 0.7587 to 0.9791; cosines 0.9994 0.9985 0.9990) match the run.")
row("prose-L09", "L09 changed hunks (outside slice d; hunks re-read)", "course/modules/M/M3/L09.html", "PASS",
    "Changed: the lab hypothesis, docstring and expected block now say 'passes is_correlation and is strictly closer to A than R: 23 of 23', which the twin prints (run). The interpretation (23 of 40 not PSD; 17 PSD; index-0 distances 0.175527 and 0.163280) matches the run. 'Where the canon breaks' and explain for Q7 use \\diag, registered. The sentence 'the repair is not always the nearest correlation matrix, to the lab's tolerance' is supported by the 23 counted cases.")

# ---- notation
row("notation-registry", "every symbol vs notation/notation.json",
    "course/modules/M/M3/*.html, cards.json; notation/notation.json", "PASS",
    "Registered program symbols: T (number of observations), \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. M3 uses T as the number of observations, the same meaning. M3 does not use \\Phi, \\gamma_3, \\gamma_4, R_f or \\mathbb{Q}. \\gamma in L07 is a local coefficient vector (the registry says gamma is local to each lesson). C^\\ast in L09 is not the registered R^\\ast. Registered macros used: \\R, \\diag, \\tr.")
row("notation-R-macro", "real numbers written \\R (architect ruling 1)", "course/modules/M/M3/*.html", "PASS",
    "grep: no \\mathbb{R} in any M3 page (0 hits). \\mathbb{C} appears in L04 (3) and L06 (1); it is not a registry macro, but it is not a real-number symbol and conflicts with nothing. Non-blocking.")

# ---- DAG and concepts
row("dag-linked-concepts", "concept links point to earlier lessons and to defined concepts",
    "course/modules/M/M3/*.html data-concept links", "PASS", "out/check_dag.out: 'check_dag M3: PASS', exit 0.")
row("dag-m4-concepts-by-name", "concepts outside the closure used by name or link",
    "course/modules/M/M3/*.html, project.html, grader/starter.py, grader/test_project.py", "PASS",
    "Architect ruling 3 (plans/FINAL-ARCHITECT-RULINGS.md item 3) accepts correlation, covariance, variance, standard deviation and Gaussian as plain prose, and the title 'Covariance-matrix doctor'. grep finds no link to an M4, M7, AP2, PR1, S2 or M8 concept and no 'OLS', 'mean-variance', 'minimum-variance' or 'shrinkage' in learner text. 'Cholesky' appears only in test_project.py as an independent checker (not the module's PSD test, not learner text): a note, not a defect.")
row("hours-arithmetic", "hub split and lesson hours", "course/modules/M/M3/index.html lines 29 and 39; L01..L09; project.html", "PASS",
    "105 + 45 = 150; lesson hours sum to 105; project 45 (see project-hours). Design targets are not failed (ruling in verifier-rules).")

# ---- cards
row("cards-structure", "cards.json structure", "course/modules/M/M3/cards.json", "PASS",
    "203 cards; ids unique; grade T (115), C (39) or absent (49); every lesson L01..L09 has cards; each C card has a basis naming a lab; check_pages M3 PASS. Full dump: out/cards_dump.txt.")
row("cards-id-sequence", "ids sequential", "course/modules/M/M3/cards.json", "PASS",
    "Architect ruling 2 (plans/FINAL-ARCHITECT-RULINGS.md item 2): ids need not be sequential. Gaps 102, 148, 191 are not defects.")
row("cards-numbers-cited", "every cited label appears in its lesson", "course/modules/M/M3/cards.json vs L01..L09.html",
    "PASS", "out/cards_numbers.out: 193 citations checked, 0 missing (script ledgers/M3/scripts/M3-d-r3/cards_numbers.py).")
row("cards-c131", "M3-c131 (symmetric and PSD of centred data matrix)", "course/modules/M/M3/cards.json M3-c131", "PASS",
    CARRY + "entry byte-identical. Re-read: x^T M x = ||X~x||^2/(T-1) >= 0 matches Proposition 1.1, grade T.")
row("cards-c101", "M3-c101 (orthogonal matrix, L06)", "course/modules/M/M3/cards.json M3-c101", "PASS",
    "Changed this round: 'A square real matrix Q whose columns are orthonormal (Definition 1.1).' Matches L06 Definition 1.1 (line 59-60). The old answer restated Q^T Q = I, which made it a duplicate of c204; the wording is now correct, but the definition is still asked by c204 and c206 (rows below).")
row("cards-c205", "M3-c205 (Q^T Q = I implies Q Q^T = I), new", "course/modules/M/M3/cards.json M3-c205", "PASS",
    "New, grade T. Matches L06 Fact 1.2's proof: F1 applied to M = Q^T and N = Q gives Q^T invertible with inverse Q, hence Q Q^T = I. Hypothesis F1 of Lesson 4 is named.")
row("cards-c206", "M3-c206 (orthogonal matrix by column inner products, L04), new", "course/modules/M/M3/cards.json M3-c206", "FAIL",
    "The answer is correct (L04 Definition 1.2, lines 73-80, says 'A real square matrix Q is orthogonal when its columns are orthonormal ... Q is orthogonal exactly when Q^T Q = I'). But it asks the same question as M3-c101 ('What is an orthogonal matrix?', L06 Definition 1.1), so the card set has a duplicate (rule 10).",
    fix="Delete M3-c206 (c101 already asks the definition). If L04 is meant to teach the inner-product form, ask a different fact, for example the (i,j) entry of Q^T Q.")
row("cards-c204", "M3-c204 (L09, the two identities making Q orthogonal)", "course/modules/M/M3/cards.json M3-c204", "FAIL",
    "The answer matches L09 Definition 1.2a (line 69-70). It asks the definition of an orthogonal matrix again, as c101 does (L06 Definition 1.1), so it duplicates content already carded (rule 10). The round-2 finding (duplicate of c101) still applies in substance; the wording of c101 changed, the duplicate did not go away.",
    fix="Delete M3-c204. Its content (Q^T Q = I and Q Q^T = I) is covered by c101 and by the derivation card c205.")
row("cards-L01", "L01 cards", "course/modules/M/M3/cards.json (L01 entries)", "PASS",
    CARRY + "all 24 L01 entries byte-identical; round-2 verification stands. Lab 1 counts re-run this round: 188 of 200, 198 of 200, 100 of 100, 0 of 200 (match c016-c019).")
row("cards-L02", "L02 cards", "course/modules/M/M3/cards.json (L02 entries)", "PASS",
    CARRY + "all 22 L02 entries byte-identical. Lab 1 counts re-run: 50 of 50 (c038, c039, c184).")
row("cards-L03", "L03 cards", "course/modules/M/M3/cards.json (L03 entries)", "PASS",
    CARRY + "all 23 L03 entries byte-identical. Lab 1 values re-run: 3 of 3, det P = 6, rank(B - I) = 1 (c057, c058, c171, c172).")
row("cards-L04", "L04 cards", "course/modules/M/M3/cards.json (L04 entries)", "FAIL",
    "The 19 carried L04 entries are byte-identical and verified (c074, c075 re-run: 200 of 200 per check; 1200 pairs). M3-c206 (new this round, L04) duplicates the orthogonal-matrix definition asked by M3-c101 (see cards-c206).",
    fix="Remove M3-c206 (see cards-c206).")
row("cards-L05", "L05 cards", "course/modules/M/M3/cards.json (L05 entries)", "PASS",
    CARRY + "all 28 L05 entries byte-identical. Lab 1 values re-run: 118 of 360 grid angles, 500 of 500, 100000 of 100000, 0.0000 1.0000 3.0000, eigenvalues -1 and 3 (c095-c097, c173, c176).")
row("cards-L06", "L06 cards", "course/modules/M/M3/cards.json (L06 entries)", "PASS",
    "Changed: c101 (verified above) and new c205 (verified). Other entries byte-identical. Lab 1 values re-run: 2.2335 0.9250 0.3348; 2 singular values above 1e-10; all identity checks True (c109-c111).")
row("cards-L07", "L07 cards (20)", "course/modules/M/M3/cards.json (L07 entries)", "PASS",
    "Read every entry against L07: Theorem 1.2 (a)-(c), Theorem 1.3, Remark 1.4, Theorem 2.2 (a)-(c), Definition 1.1 and 2.1; Lab 1 values re-run: 1.3325, 0.8488, -0.4120, residual 0.8951, rank 2 of 3 (c124-c126, c177).")
row("cards-L08", "L08 cards (23)", "course/modules/M/M3/cards.json (L08 entries)", "PASS",
    "Read every entry against L08: Propositions 1.1-1.2, Definition 1.3, Theorem 1.4, Theorem 2.1, Corollary 2.2, Proposition 2.3, Remark 2.4, Definition 3.1 (shapes orthogonalised, so 'orthonormal by construction' holds). Lab 1 values re-run: 75.9 18.1 5.2; 0.7587 to 0.9791; cosines 0.9994 0.9985 0.9990; planted scale 8.0 on the level factor (twin line 46).")
row("cards-L09", "L09 cards (28)", "course/modules/M/M3/cards.json (L09 entries)", "FAIL",
    "Verified: c146-c167, c181-c185, c202 against L09 text; c161-c164, c175 against the run (0.6400000000; eigenvalues -0.800000 1.900000 1.900000; 23 of 40; 0.175527 and 0.163280); c182 against the lab's alternating_projections (clip, set diagonal, stop when the change is below TOL = 1e-12, at most MAX_ITER = 500). Failure: M3-c204 duplicates the orthogonal-matrix definition (see cards-c204). Non-blocking note: c163 asks for 'strictly closer' only, while the lab now counts 'passes is_correlation and strictly closer'; the answer 23 of 23 is correct for the printed run.",
    fix="Delete M3-c204 (see cards-c204). Optionally make c163's question name the feasibility condition the lab counts.")
row("cards-c-numbers-lab", "C-grade card numbers match the lab outputs", "course/modules/M/M3/cards.json (39 C cards) vs L01..L09 expected blocks",
    "PASS", "Script check: every number in every C card's back appears in its own lesson text (0 missing). Lab values for L01-L09 were re-run and compared by hand for the cards cited in the rows above.")

# ---- notes and mutants
mut_lines = (OUT / "mutate_M3_seeds0-9_with_vd3.out").read_text(encoding="utf-8").splitlines()
mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$")
for line in mut_lines:
    m = pat.match(line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    doc = (MUT / name).read_text(encoding="utf-8")
    first = doc.split("\n", 1)[0].strip('"')
    entry = {"name": name, "description": first, "killed_by": None if killed.strip() == "None" else killed.strip()}
    mutants.append(entry)
    if status == "SURVIVED":
        assert entry["killed_by"] is None

assert len(mutants) == 137, len(mutants)
notes = (
    "Round 3 on pin a007712 (round-2 pin c737272). Delta read in full: course/modules/M/M3/L07.html, L08.html, L09.html; "
    "cards.json (c101 reworded; c205 and c206 added); project.html (rungs paragraph, spec Constraints and grader panel "
    "now NumPy-permitting, unit-diagonal convention, Exemplar B memo); grader/starter.py (docstring); tests/labs/M3/lab-M3-L09-1.py; "
    "ledgers/M3/alternatives unchanged; ledgers/M3/equivalent/README.md and r15d file re-read; ledgers/M3/mutants: v2d_06 moved to retired/. "
    "Not changed: grader/reference.py, instance.py, test_project.py, alternatives, twins other than L09. "
    "Round-2 FAIL rows re-verified: grader-standard-library-only (still FAIL, now on the NumPy wording), alternatives-five-standard-library (PASS now), "
    "mutants-v2d-06 (now a placement FAIL), cards-c204 and cards-L09 (still FAIL: duplicate of the orthogonal-matrix definition), "
    "dag-m4-concepts-by-name (PASS under ruling 3), equivalent-r15d-m03-label (PASS). "
    "Commands run by this verifier: check_pages, check_dag, check_projects, run_graders 0-49, run_labs, page_smoke for project, L01..L09, index (one page at a time), "
    "ruff check and format, mypy --no-incremental, verify_refs --offline, mutate_graders --unit M3 --seeds 0-9, pytest on test_page_checks, test_labs, test_run_labs, "
    "collect-only, the six alternatives and the three equivalents on seeds 0-49 (run_alts.py, run_files.py), the twins alone under python -I -W error, the new fix checks (proposed_fix_tests.py) on the reference, the alternatives and the survivors."
)
registry_flags = [
    "Repository-wide observation (not an M3 defect): orthogonal matrix is defined three times in M3 (L04 Definition 1.2, L06 Definition 1.1, L09 Definition 1.2a). This is the source of the duplicate cards c204 and c206; the lesson owners (slices a-c) should keep one defining statement and cross-reference the others."
]
freshness_flags = []
summary = (
    "M3 slice d round 3: FAIL. All 74 round-2 row ids kept; 7 new ids added (grader-no-argument-mutation, mutants-docstring-first-line, mutants-new-round3-written, cards-c101, cards-c205, cards-c206, cards-c-numbers-lab). "
    "Non-PASS rows: gate-mutate-m3 (4 survivors: 3 in-place argument writes, 1 scipy call), grader-standard-library-only, grader-no-argument-mutation, mutants-v2d-06 (placement), mutants-docstring-first-line (2 mutants with the reference header), cards-c204 and cards-c206 (duplicate orthogonal-matrix definition), cards-L04 and cards-L09 (follow from c206 and c204). "
    "Fixes verified in a scratch copy (proposed_fix_tests.py): the two grader checks kill all four survivors and pass the reference and all six alternatives on seeds 0-9."
)

now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
frag = {
    "unit": "M3",
    "slice": "d",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for M3-d, round 3 (did not build M3; round-2 fragment used as context only)",
    "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
    "base": "c737272f5bdef4a027417989cd52254555e8a0bb (round-2 pin); delta read in full (out/m3_course_delta_c737272_to_a007712.diff)",
    "checkout": str(ROOT),
    "scratch": "ledgers/M3/scripts/M3-d-r3/",
    "verified_at": now,
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": registry_flags,
    "freshness_flags": freshness_flags,
    "notes": notes,
    "summary": summary,
}
(ROOT / "ledgers/M3/M3-d.json").write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(R), "non-PASS", sum(1 for r in R if r["status"] != "PASS"), "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
