"""Round-11 verifier (M3 slice d): assemble the fragment ledgers/M3/M3-d.json from the round-11 outputs.

Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r11/build_fragment_r11.py
"""

import json
import re
from pathlib import Path

ROOT = Path.cwd()
S = "ledgers/M3/scripts/M3-d-r11"
OUT = ROOT / "ledgers/M3/M3-d.json"

mutants = []
for line in (ROOT / S / "out/mutate_M3_seeds0-9_r11.out").read_text(encoding="utf-8").splitlines():
    if not line.startswith("KILLED "):
        continue
    body = line[len("KILLED ") :]
    name, rest = body.split(": ", 1)
    desc, killed = rest.rsplit(" -> ", 1)
    mutants.append({"id": name.removesuffix(".py"), "description": desc, "killed_by": killed})

rows = []


def row(rid, check, location, status, evidence, fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


GATES = "ledgers/M3/scripts/M3-d-r11/out/"
row("gate-check-pages", "gate-check_pages", "course/modules/M/M3/*", "PASS",
    GATES + "check_pages_M3.out: 'check_pages M3: PASS', EXIT 0 (tools/check_pages.py --unit M3 at ccaeeaf).")
row("gate-check-dag", "gate-check_dag", "course/modules/M/M3/*", "PASS",
    GATES + "check_dag_M3.out: 'check_dag M3: PASS', EXIT 0.")
row("gate-check-projects", "gate-check_projects", "course/modules/M/M3/project.html", "PASS",
    GATES + "check_projects_M3.out: 'check_projects M3: PASS', EXIT 0.")
row("gate-run-labs", "gate-run_labs", "tests/labs/M3/*.py; project.html", "PASS",
    GATES + "run_labs_M3.out: 'run_labs M3: PASS (12/12)', EXIT 0. " + GATES +
    "labs_twin_vs_page_r11.out: the three project twins run under python -I -W error with exit 0; each expected block "
    "equals its twin's output; project-1 and project-3 page code is identical to the twin; project-2 page code differs "
    "from its twin only at the two ___ blanks (Step 3 and Step 5), as the completion problem requires.")
row("gate-run-graders", "gate-run_graders", "course/modules/M/M3/grader/", "PASS",
    GATES + "run_graders_M3.out: 'run_graders M3: PASS (reference 50/50 seeds)', EXIT 0.")
row("gate-page-smoke", "gate-page_smoke", "course/modules/M/M3/project.html", "PASS",
    GATES + "page_smoke_project.out: 'page_smoke M3: PASS', EXIT 0 (project page alone).")
row("gate-ruff", "gate-ruff", "tests/labs/M3; course/modules/M/M3/grader; ledgers/M3/mutants/v11d_*.py", "PASS",
    GATES + "ruff_check.out 'All checks passed!' and ruff_format.out '16 files already formatted' (labs and grader); "
    "the three new mutants pass ruff check --force-exclude and ruff format --check (3 files already formatted).")
row("gate-mypy", "gate-mypy", "repository", "PASS",
    GATES + "mypy.out: 'Success: no issues found in 385 source files' (mypy --no-incremental).")
row("gate-verify-refs", "gate-verify_refs", "references/references.json", "PASS",
    GATES + "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'; " + GATES +
    "verify_refs_M3_live_r11.out: 'live re-verification of M3: 2 of 560 entries, 0 problems' (plain run, EXIT 0).")
row("gate-collect-only", "gate-collect-only", "course/modules/M/M3/grader/test_project.py; project.html", "PASS",
    GATES + "collect_only_M3.out: '163 tests collected' on the staged copy (stage_grader_r11.sh); project.html line 237 "
    "states 163 at line 239.")
row("gate-pytest-relevant", "gate-pytest", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, "
    "test_memo_exemplars.py, test_page_smoke.py", "PASS",
    GATES + "pytest_relevant_r11.out: five modules, EXIT 0 (.venv/bin/python -m pytest -q at ccaeeaf).")
row("gate-mutate-m3", "gate-mutate_graders", "ledgers/M3/mutants/ (171 files)", "PASS",
    GATES + "mutate_M3_seeds0-9_r11.out: 'mutate_graders M3: PASS (171/171 killed)', EXIT 0 (tools/mutate_graders.py "
    "--unit M3 --seeds 0-9).")
row("gate-reference-starter", "gate-reference-starter", "grader/reference.py; grader/starter.py", "PASS",
    GATES + "reference_seed0_r11.out: '163 passed' (QF_SEED=0, --assert=plain -W error); starter_seed0_r11.out: "
    "'162 failed, 1 passed'.")
row("gate-alternatives-seeds-0-49", "gate-alternatives", "ledgers/M3/alternatives/ (10 files)", "PASS",
    GATES + "alts_seeds0-9_r11.out (run_alts_r11.sh): all ten alternatives PASS 163/163 on each of seeds 0-9. alt10 was "
    "also run on seeds 0-49 with 0 failures (/private/tmp/verifyD11-alt10-50). Alternatives 1-9 were not run beyond "
    "seeds 0-9.")
row("alternatives-svd-probe", "2.6-alternative-svd", "ledgers/M3/scripts/M3-d-r10/probes/alt11_svd_signed_eigenvalues.py",
    "PASS", "SVD-based correct alternative (probe from round 10, re-run on the r11 grader in /private/tmp/verifyD11-alt11): "
    "163 passed on each of seeds 0-9.")
row("alternatives-numpy-return-types", "2.6-alternative-numpy", "ledgers/M3/scripts/M3-d-r11/probes/"
    "make_numpy_return_probe_r11.py; out/numpy_return_probe_r11.out", "PASS", "A reference variant returning np.bool_ from is_psd and ndarray matrices "
    "and vectors (/private/tmp/verifyD11-probe-numpy): 163 passed on each of seeds 0-9. The round-10 failure of "
    "numpy-bool verdicts is fixed by as_verdict (test_project.py lines 134-139).")
row("alternatives-count-and-seeds", "2.6-alternatives", "ledgers/M3/alternatives/ (10 files)", "PASS",
    GATES + "alts_seeds0-9_r11.out: ten alternatives, all PASS on seeds 0-9. The brief says six; the directory holds ten and "
    "all ten were run, which is a superset.")
row("grader-instance", "2.6-grader-instance", "course/modules/M/M3/grader/instance.py; project.html line 231", "PASS",
    "instance.py read in full (110 lines). ledgers/M3/scripts/M3-d-r11/instances_check_r11.py: seeds 0-19 each valid "
    "(k in {3,4,5}; unit diagonal; psd_corr positive definite; min eigenvalue below -0.02). Eigenvectors are orthonormal to "
    "1.8e-11 over seeds 0-49 (rounded to 12 decimals), within every grader tolerance.")
row("grader-test-count-and-purity", "2.6-grader-test-count", "grader/test_project.py lines 812-849; project.html line 237",
    "PASS", "collect-only 163 equals the page's 163. test_functions_print_nothing (812-820) and test_inputs_are_not_mutated "
    "(823-849) read in full.")
row("grader-standard-library-only", "2.6-grader-imports", "grader/test_project.py lines 852-867; project.html line 237",
    "PASS", "test_module_imports_only_standard_library_or_numpy walks the AST and allows numpy and sys.stdlib_module_names; "
    "project line 236 states the standard library and NumPy only.")
row("grader-lab3-reference-numbers", "2.6-grader-lab3-numbers", "grader/test_project.py lines 538-561; project.html Lab 3",
    "PASS", "Test values -0.142113 (1e-6), 0.176573 (1e-6), 0.175003 (1e-5), 0.011516 (1e-5), weights 1.778929/-1.096718/"
    "-0.255613/0.573402 (1e-6). out/numbers_numpy_r11.out (independent NumPy eigh and solve): identical at the printed six decimals.")
row("grader-failure-messages-leak-answers", "2.6-grader-messages", "grader/test_project.py (every assert, pytest.fail, "
    "must_raise and must_not_raise message)", "PASS", "All 890 lines read. No message interpolates an expected or computed "
    "value; f-strings carry only condition names, shapes, positions and modes.")
row("grader-named-conditions", "2.6-grader-named-conditions", "grader/test_project.py lines 134-200, 680-784, 713-802; "
    "project.html line 250", "PASS", "must_raise is used only for the four named conditions: non-square (185-188, 713-720), "
    "asymmetry beyond 1e-9 (193-198, 725-729, 763-765), volatility not strictly positive (770-776, zero, negative, NaN), and "
    "length mismatch (796-802). grep: no pytest.raises in the grader. must_not_raise cases are inputs the page calls valid.")
row("grader-browser-timeout", "2.6-grader-browser", "project.html line 237; course/assets/js/python.js line 4", "PASS",
    "python.js line 4: TIMEOUT_MS = 120000, matching 120 seconds on project.html line 237.")
row("grader-reference-docstring", "2.6-reference-docstring", "grader/reference.py lines 1-5, 109-110", "PASS",
    "Docstring names Jacobi eigenvalues and alternating projections with correction terms; matches lines 33-63 and 109-128.")
row("grader-spec-rubric-counts", "2.6-spec-counts", "project.html lines 237, 490, 495, 498-502", "PASS",
    "Five criteria C1-C5 with four levels each (rows 500-504); 163 tests (line 239); 'meets the bar at level 3 or above' "
    "(lines 239, 492, 497).")
row("spec-projection-tol-undefined", "spec-tol-defined", "project.html lines 233, 246; grader/starter.py lines 30-36", "PASS",
    "tol is the stopping tolerance of the projection (line 233 and conventions line 248: gap and change both at most tol); "
    "starter.py docstring says the stopping rule is the learner's choice.")
row("grader-projection-spec-vs-reference", "2.6-spec-vs-reference", "grader/reference.py lines 109-128; project.html line 248",
    "PASS", "Compared line by line: J=P(W+E); E=W+E-J; N=J+H with diagonal set to 1; H=J+H-N; W=N; gap=||N-J||_F; change="
    "||N-W_prev||_F; stop when both <= tol; at most max_iter steps. Matches; test_projection_repair_runs_exactly_max_iter_steps "
    "passes on the reference for steps 1-3.")
row("grader-weights-spec-vs-reference", "2.6-spec-vs-reference", "grader/reference.py lines 131-150; project.html line 249",
    "PASS", "Sigma = SCS, Gauss-Jordan solve with partial pivoting, normalise to sum 1; ValueError for length mismatch and "
    "non-positive volatility (136-138). Matches the spec and the closed form (A3) to 1e-16 (out/numbers_numpy_r11.out).")
row("grader-numpy-bool-return", "2.6-grader-return-types", "grader/test_project.py lines 134-139 and the is_psd asserts",
    "PASS", "Round-10 observation fixed: as_verdict accepts bool or np.bool_. The np.bool_/ndarray probe passes 163 on each "
    "of seeds 0-9.")
row("grader-failure-messages-r10", "2.6-grader-no-leak", "grader/test_project.py", "PASS",
    "No test embeds the expected value in its message (the check in grader-failure-messages-leak-answers covers the new "
    "as_verdict and np.ndarray lines).")
row("mutants-existing-140", "mutants-all-existing", "ledgers/M3/mutants/ (171 files)", "PASS",
    GATES + "mutate_M3_seeds0-9_r11.out: every mutant KILLED on seeds 0-9 (171/171).")
row("mutants-new-student-errors", "mutants-v4d", "ledgers/M3/mutants/v4d_02..v4d_04", "PASS",
    GATES + "mutate_M3_seeds0-9_r11.out: each KILLED.")
row("mutants-v2d-01-05", "mutants-v2d", "ledgers/M3/mutants/v2d_01..v2d_05", "PASS", GATES + "mutate output: each KILLED.")
row("mutants-v2d-06", "mutants-retired-v2d06", "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py", "PASS",
    "Retired (correct alternative: the page allows NumPy). Re-run this round: 163 passed on each of seeds 0-9.")
row("mutants-v3d-02-05", "mutants-v3d", "ledgers/M3/mutants/v3d_02..v3d_05", "PASS", GATES + "mutate output: each KILLED.")
row("mutants-v5d-new-student-errors", "mutants-v5d", "ledgers/M3/mutants/v5d_02, v5d_03, v5d_05, v5d_06", "PASS",
    GATES + "mutate output: each KILLED.")
row("mutants-r6-new-student-errors", "mutants-r6d", "ledgers/M3/mutants/r6d_m02..r6d_m04", "PASS", GATES + "mutate output: each KILLED.")
row("mutants-r7-new-student-errors", "mutants-r7d", "ledgers/M3/mutants/r7d_m01..r7d_m03", "PASS", GATES + "mutate output: each KILLED.")
row("mutants-v8d-new-student-errors", "mutants-v8d", "ledgers/M3/mutants/v8d_01..v8d_04", "PASS", GATES + "mutate output: each KILLED.")
row("mutants-v9d-new-student-errors", "mutants-v9d", "ledgers/M3/mutants/v9d_01..v9d_04", "PASS", GATES + "mutate output: each KILLED.")
row("mutants-v10d-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/v10d_01..v10d_04", "PASS",
    GATES + "mutate output: each KILLED (v10d_01 test_lab3_reference_numbers_are_matched; v10d_02 test_non_square_is_refused "
    "and the asymmetry tests; v10d_03 test_projection_repair_runs_exactly_max_iter_steps[1]; v10d_04 test_lab3_reference_numbers_are_matched).")
row("mutants-v11d-new-student-errors", "2.6-mutation (new this round, 3 >= 3)",
    "ledgers/M3/mutants/v11d_01..v11d_03; ledgers/M3/scripts/M3-d-r11/make_mutants_v11d_r11.py", "PASS",
    GATES + "mutate_M3_seeds0-9_r11.out: v11d_01 projection pins the PSD iterate's diagonal before the correction term is "
    "formed (KILLED by test_projection_repair_is_a_valid_repair[seed]); v11d_02 symmetry tolerance scaled by dimension "
    "(KILLED by test_asymmetry_of_twice_the_tolerance_is_refused_at_large_entries[1.0-min_eigenvalue]); v11d_03 _rescale "
    "divides by sqrt(d_0 d_j) (KILLED by test_clip_repair_has_unit_diagonal_and_is_symmetric[seed]).")
row("mutants-r15d-description", "2.6-mutation-description", "ledgers/M3/mutants/r15d_m01_is_psd_strict_boundary.py:1; "
    "r15d_m02_rescale_missing_sqrt_on_column.py:1", "PASS", "Round-10 FAIL fixed at ccaeeaf: the first docstring lines now "
    "name the error ('is_psd uses a strict inequality, ...'; 'clip_repair divides entry (i, j) by sqrt(d_i) * d_j, ...'), "
    "and the mutate output prints them. No mutant's first line is the reference header any more (grep over all 171 files).")
row("mutants-description-all", "2.6-mutation-description", "ledgers/M3/mutants/ (171 files, first line)", "PASS",
    "All 171 first docstring lines were read; each describes a specific error.")
row("mutants-v5d-01-equivalent-moved", "equivalent-alt10-bitwise", "ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py",
    "PASS", "ledgers/M3/scripts/M3-d-r11/probes/equiv_alt10_bitwise_r11.py: outputs differing bitwise (float.hex) 0 of 10000 "
    "(1000 random symmetric matrices, sizes 2-6, tol in {0, 1e-10}, max_iter in {1, 2, 3, 5, 20}).")
row("mutants-v5d-04-accepted-stop-rule", "alternative-stop-either", "ledgers/M3/alternatives/alt10_stop_when_either_gap_or_change.py",
    "PASS", "PASS 163/163 on seeds 0-9 (alts_seeds0-9_r11.out) and 0 failures on seeds 0-49 (/private/tmp/verifyD11-alt10-50).")
row("equivalent-r6d-m04", "alternative-gap-only-stop", "ledgers/M3/alternatives/alt7_dykstra_gap_only_stop.py", "PASS",
    "alts_seeds0-9_r11.out: PASS on seeds 0-9.")
row("equivalent-r11d-m02", "alternative-step-only-stop", "ledgers/M3/alternatives/alt8_dykstra_step_only_stop.py", "PASS",
    "alts_seeds0-9_r11.out: PASS on seeds 0-9.")
row("equivalent-r15d-m03-label", "alternative-full-budget", "ledgers/M3/alternatives/alt9_dykstra_runs_full_budget.py", "PASS",
    "alts_seeds0-9_r11.out: PASS on seeds 0-9.")
row("equivalent-readme-citation", "equivalent-readme", "ledgers/M3/equivalent/README.md", "PASS",
    "The cited check script ledgers/M3/scripts/M3-d-r7-fixer/equiv_alt10_check.py exists. Claim 'bitwise identical': 0 of "
    "10000 differ (probe above). Claim 'alt10 stop-either passes seeds 0-49': confirmed (0 failures). Claim 'not equivalent "
    "(can stop one step earlier)': ledgers/M3/scripts/M3-d-r11/probes/alt10_vs_reference_tol_r11.py gives 22 of 150 outputs "
    "differing (seeds 0-49, tol in {1e-3, 1e-6, 1e-10}).")
row("project-numbers", "1-numbers-vs-unrounded", "course/modules/M/M3/project.html lines 57-139, 466-476, 477, 579-583, 591-617",
    "PASS", "Every printed and prose number recomputed with NumPy (" + GATES + "numbers_numpy_r11.out, script "
    "numbers_numpy_r11.py): eigenvalues, rebuilt diagonals, repaired rows, distances 0.176573 / 0.175003 "
    "(gap 0.001570), max entry difference 0.011516, det -0.261600, weights 1.778929 -1.096718 -0.255613 0.573402 (sum 1), "
    "smallest eigenvalues 0 and -0 at six decimals, cond(Sigma_proj) about 1.9e15. Exemplar rounding (1.78, -1.10, -0.26, "
    "0.57 summing to 0.99) checked.")
row("project-lab1-memo-sentence", "2-lab-prints-vs-prose", "project.html lines 57, 139; tests/labs/M3/lab-M3-project-1.py",
    "PASS", "Hypothesis: smallest eigenvalue negative and verdict False; repaired diagonal 1 to six decimals; passes at 1e-9. "
    "Interpretation: repaired off-diagonals 0.636095, -0.382551, 0.469578 and rebuilt diagonal 1.096064, 1.104409, 1.074824 "
    "all match the expected block.")
row("project-lab2-completion", "2-completion-blanks", "project.html lines 142-224; tests/labs/M3/lab-M3-project-2.py", "PASS",
    "The two blanks are the expressions the hypothesis names (smallest >= -1e-10; math.sqrt(d[i] * d[j])); the expected block "
    "equals the twin's output (-0.203711 ... 0.409576 ...).")
row("project-lab3-check", "2-lab-prints-vs-prose", "project.html lines 290-478; tests/labs/M3/lab-M3-project-3.py", "PASS",
    "Hypothesis items (not PSD; projection nearer by a positive distance; diagonals 0.000000 at 5e-7; determinant nonzero; "
    "weights sum 1; both repairs' smallest eigenvalue zero to six decimals) match the expected block and the independent "
    "NumPy values.")
row("project-lab3-diagonal-positivity-sentence", "2-lab-prints-vs-prose", "project.html lines 477, 605, 617", "PASS",
    "Clipped rebuilt diagonal (NumPy) 1.05628, 1.045743, 1.000014, 1.040076: all positive, so A4's hypothesis holds on Lab 3's "
    "matrix. The sentence 'a completed run shows every d[i]*d[j] is positive, A1 makes d[i] nonnegative' is a valid inference "
    "(math.sqrt and division raise on a negative or zero product). Line 477 says the run shows it numerically and does not prove it.")
row("project-spec-grader", "1-spec-vs-starter-and-grader", "project.html lines 229-239; grader/starter.py; grader/test_project.py",
    "PASS", "Function names and signatures in project.html line 235 match starter.py; the constraint line matches the test "
    "file's docstring and 'named conditions'.")
row("project-conventions-math", "5-math-conventions", "project.html lines 242-252; grader/reference.py", "PASS",
    "Clipping (A1 and A2 route), Frobenius distance, projection steps, weights and the four named ValueError conditions match "
    "reference.py and the test file line by line.")
row("project-conventions-link", "dag-link-target", "project.html line 245 (L05.html#def-positive-semidefinite-matrix); "
    "line 233 (L05.html Definition 1.4)", "PASS", "course/modules/M/M3/L05.html line 72 defines positive-semidefinite-matrix "
    "(dfn id def-positive-semidefinite-matrix); L05 Definition 1.4 is '(positive semidefinite and positive definite)'.")
row("project-proof-A1", "3-proof", "project.html line 643 (A1, Repairs in the report exemplar B)", "PASS",
    "Proof checked: X symmetric; z'Xz = sum max(Lambda_ii, f)(V'z)_i^2 >= 0 since max >= f >= 0. Hypotheses named (F1 to F4, "
    "real symmetric A, f >= 0). Spectral theorem reference Lesson 4 Theorem 2.3 (L04.html line 130) holds under F1 to F4.")
row("project-proof-A2", "3-proof", "project.html line 644 (A2)", "PASS",
    "Y_ii = X_ii/(sqrt d_i)^2 = 1; z'Yz = q'Xq with q = D^{-1/2}z >= 0; positivity of d_i named as the hypothesis.")
row("project-proof-A3", "3-proof", "project.html line 645 (A3)", "PASS",
    "Checked algebraically: Sigma = [[a^2, rho ab],[rho ab, b^2]], det = a^2 b^2 (1 - rho^2) > 0; Sigma^{-1} iota proportional to "
    "(b(b - rho a), a(a - rho b)); sum a^2 + b^2 - 2 rho ab = (a-b)^2 + 2ab(1-rho) > 0; scaling by c > 0 multiplies all by c^2 "
    "and cancels. Hypotheses |rho| < 1 and a, b > 0 named.")
row("project-proof-A4", "3-proof", "project.html line 645 (A4)", "PASS",
    "Checked: X u_i = V Lambda_0 e_i = 0 so X singular; with d_i > 0 assumed, z = D^{1/2} u_i gives Yz = 0 with z nonzero; "
    "Sigma S_v^{-1} z = S_v Y z = 0. Hypotheses named (F1 to F4, symmetric C with a negative eigenvalue, positive diagonal).")
row("project-hours", "4-hours-arithmetic", "project.html lines 259-267 (hours table); index.html line 29 "
    "(data-hours-lessons 105, data-hours-project 45); L01-L09 data-hours", "PASS",
    "Table: 2 + 3 + 14 + 8 + 12 + 6 = 45 (data-hours-project 45). Lessons 12+11+12+12+12+11+11+12+12 = 105; 105 + 45 = 150, the "
    "module total in index.html line 7.")
row("project-exemplars", "1-exemplar-scores", "project.html lines 509-575 (Exemplar A), 577-654 (Exemplar B)", "PASS",
    "Scores agree with annotations. Exemplar A: C1 2, C2 2, C3 2, C4 1, C5 2 (each 'Meets level k' and 'Misses level k+1' pair). "
    "Exemplar B: C1 4, C2 4, C3 4, C4 3, C5 3. Exemplar B's stated numbers equal Lab 3's printed values.")
row("project-rubric", "5-rubric-levels", "project.html lines 494-507", "PASS", "Five criteria, four levels each; each level "
    "cell names observable elements consistent with the scoring rule in line 492.")
row("rubric-C4-level2-vague", "5-rubric-levels", "project.html line 503 (C4 row)", "PASS",
    "Level 2 names the error as labelling some inputs, or a conclusion from a printed result; consistent with Exemplar A's C4 1.")
row("project-references", "3-attribution", "project.html lines 674-684 (Reading), references list; references/references.json",
    "PASS", "Reading section states that no passage locator is confirmed and no statement is attributed. verify_refs offline 560/0 "
    "and live M3 2/560 with 0 problems.")
row("project-no-process-words", "12-process-words", "project.html; cards.json; grader/*.py; tests/labs/M3/lab-M3-project-*.py",
    "PASS", "grep for builder, verifier, verified, audit, round, agent, reviewer, fixer, batch, checkout, ledger, TODO, FIXME, "
    "placeholder, lorem: no matches in these files.")
row("project-stretch", "5-stretch", "project.html lines 663-670", "PASS", "Three stretch items; the second asks for a count 'over 200 "
    "seeded matrices' and says not to extend it, which is a labelled scope.")
row("project-links", "links", "project.html (href and src values)", "PASS",
    "check_pages PASS; the placement anchor exists (index.html line 68, id=placement); the grader and report anchors resolve.")
row("project-brief-scope", "4-scope-brief", "project.html lines 229-233, 264, 475, 486, 617", "PASS",
    "Brief item 4 asks for each repair whether the weight formula applies and why; the page answers it (see scope row).")
row("scope-repair-weights-vs-brief", "4-scope-brief", "project.html lines 262-264, 475-477, 486, 503, 617-621", "PASS",
    "Round-10 FAIL resolved. The brief (line 486) asks only whether the weight formula applies to each repaired matrix, with "
    "the reason. The page answers both: clipped matrix gets no weights (A4, positive diagonal shown by the run and A1); the "
    "projection gets none because its Sigma is numerically singular (printed smallest eigenvalue 0 to six decimals; NumPy "
    "cond about 1.9e15), flagged as numerical evidence and not a proof (rubric C2 level 3). No weight comparison is demanded.")
row("spec-stop-rule-sentence", "3-spec-vs-reference", "project.html line 248 (Alternating steps)", "PASS",
    "The sentence on stopping (stop when gap and change are both at most tol; output last W_t; tests check the output and the "
    "iterates at tol = 0, not the stopping rule) matches reference.py lines 116-128 and the test at 631-637.")
row("project-lab3-weights-sentence", "2-lab-prints-vs-prose", "project.html line 475-477; tests/labs/M3/lab-M3-project-3.py",
    "PASS", "Lab 3 prints weights for the input only (line 460 of the expected block); the page says so.")
row("notation-registry", "notation", "notation/notation.json; project.html; L08.html; cards.json", "PASS",
    "Registered symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) are not reused with another "
    "meaning on these pages (T is the observation count in M3 as the registry says). \\iota is not registered; it is a local "
    "symbol defined at first use in project.html line 249 and in L08 Section 3. See registry_flags.")
row("notation-R-macro", "notation", "project.html; L07.html; L08.html; L09.html; cards.json", "PASS",
    "Macros used (\\R, \\tr, \\diag) are registered in notation.json macros with those meanings. No unregistered program-wide "
    "macro found.")
row("dag-linked-concepts", "14-dag-links", "project.html concept links (eigendecomposition, spectral-theorem, "
    "positive-semidefinite-matrix)", "PASS", "check_dag M3 PASS; targets exist (L03 def-eigendecomposition, L04 "
    "def-spectral-theorem, L05 def-positive-semidefinite-matrix).")
row("dag-m4-concepts-by-name", "14-dag-names", "project.html; cards.json; L01-L09", "PASS",
    "Jacobi rotations and Gaussian elimination with partial pivoting appear only inside code docstrings (project.html lines 69, "
    "152, 308, 404), not as prose concepts. No Cholesky, Dykstra or SVD concept is named in project prose outside the M3 "
    "closure; the SVD appears in L06, which is in the unit.")
row("dag-cholesky-named-in-grader", "14-dag-names", "course/modules/M/M3/grader/*", "PASS",
    "grep -i cholesky over grader/: no match. Nothing to flag.")
row("cards-structure", "10-cards-structure", "course/modules/M/M3/cards.json", "PASS",
    "208 cards; unique ids; lessons L01-L09 only; every card has front, back, lesson; grade T, C or none.")
row("cards-id-sequence", "10-cards-ids", "course/modules/M/M3/cards.json", "PASS",
    "Gaps at M3-c102, c148, c191, c204, c206 are historic removals (ledgers/M3/M3-d.json history and cards_r9.json); no "
    "reference to these ids exists anywhere in the tree (grep).")
row("cards-numbers-cited", "10-cards-numbers", "cards.json front and back; L08.html; L09.html", "PASS",
    "Numbers in changed or new cards appear in their lesson: c141 0.7587 and 0.9791 (L08 expected block); c167 1e-12 and 1e-8 "
    "(L09 is_correlation); c213 0.01 (L08 Section 1).")
row("cards-labels-cited", "10-cards-labels", "cards.json grade and basis fields", "PASS",
    "C cards carry basis; the new cards c208 to c213 carry no grade and no basis (T for c208 only).")
row("cards-duplicate-scan", "10-cards-duplicates", "course/modules/M/M3/cards.json (21528 pairs)", "PASS",
    "Full token-Jaccard scan of fronts and backs over all 208 cards: highest front similarity c017/c019 0.88 and c087/c088 0.875, "
    "highest back similarity c025/c187 0.92 (kernel vs image: different claims). No duplicates.")
row("cards-sample-20", "10-cards-read", "cards.json (all 208 cards read)", "PASS",
    "Every card read this round (dump in three slices, c001-c213). Mathematical claims spot-checked by hand: c020, c027, c033, "
    "c037, c041, c048, c056, c060, c073, c085, c093, c095, c108, c112, c117, c120, c128, c152, c160, c181, c183, c201, c203.")
row("cards-lab-numbers", "10-cards-lab-numbers", "cards.json grade-C cards; tests/labs/M3 expected blocks", "PASS",
    "C cards on changed lessons (c139, c140, c141, c145, c163, c167, c174, c175) checked against the L08 and L09 expected "
    "blocks; L01-L07 lab cards carried from round 10 (lab code and expected blocks byte-identical since 47a36d8).")
row("cards-L01", "10-cards-lesson", "cards c001-c022, c169-c170 vs L01.html", "PASS", "Re-read this round; L01.html "
    "byte-identical since the previous pin; carried from round 10 (cards c001-c022 and c169-c170 byte-identical since "
    "47a36d8c). Spot checks: c020, c027, c033, c037.")
row("cards-L02", "10-cards-lesson", "cards c023-c042, c184, c187 vs L02.html", "PASS", "Carried from round 10 (L02.html and "
    "cards byte-identical since 47a36d8c); re-read this round; c033, c037, c041 verified by hand.")
row("cards-L03", "10-cards-lesson", "cards c043-c062, c171-c172, c188 vs L03.html", "PASS", "Carried from round 10 (L03.html and "
    "cards byte-identical since 47a36d8c); re-read; c048, c056, c060 verified by hand.")
row("cards-L04", "10-cards-lesson", "cards c063-c078, c192 vs L04.html", "PASS", "Carried from round 10 (L04.html and cards "
    "byte-identical since 47a36d8c); re-read; c073 verified by hand.")
row("cards-L05", "10-cards-lesson", "cards c079-c100, c173, c176, c179, c180, c193, c203 vs L05.html", "PASS", "Carried from "
    "round 10 (L05.html and cards byte-identical since 47a36d8c); re-read; c085, c093, c098, c203 verified by hand; "
    "Definition 1.4 link target confirmed.")
row("cards-L06", "10-cards-lesson", "cards c101-c114, c178, c205 vs L06.html", "PASS", "Carried from round 10 (L06.html and cards "
    "byte-identical since 47a36d8c); re-read; c112 verified by hand.")
row("cards-L07", "10-cards-lesson", "cards c115-c129, c168, c177, c194-c196 vs L07.html", "PASS", "Carried from round 10 (L07.html "
    "unchanged since 47a36d8c; cards byte-identical); re-read; c117, c120, c128, c168, c196 checked against Theorem 1.2, Theorem "
    "1.3, Theorem 2.2(c) and Remark 1.4 labels.")
row("cards-L08", "10-cards-lesson", "cards c130-c145, c174, c186, c197-c201, c207, c209-c213 vs L08.html (Section 3 changed)",
    "FAIL", "M3-c211 (cards.json, lesson L08): the back cites Lesson 7, Theorem 1.2 for the orthogonal projection onto the span "
    "of the earlier shapes, but Theorem 1.2 requires linearly independent columns (L07.html line 65), and the earlier shapes are "
    "independent only under the at-least-three-distinct-tenor-values assumption (L08.html line 137). The card carries only "
    "'Assuming F1 to F4 of Lesson 4'. Cards c142 and c207 carry the three-value assumption; c211 does not. All other L08 cards "
    "checked (c139, c140, c141, c142, c145, c174, c186, c201, c207, c210, c212, c213) agree with the current L08 text.",
    "Rewrite M3-c211 back as: 'Assuming F1 to F4 of Lesson 4 and at least three distinct tenor values (which make the earlier "
    "shapes linearly independent, the hypothesis of Lesson 7, Theorem 1.2), it means subtracting from the shape its orthogonal "
    "projection onto the span of the earlier shapes (Lesson 7, Theorem 1.2).'")
row("cards-L09", "10-cards-lesson", "cards c146-c167, c181-c183, c185, c202, c208 vs L09.html (line 119 changed)", "PASS",
    "c167 new text matches the L09 lab's is_correlation (symmetric, unit diagonal to 1e-12, smallest eigenvalue >= -1e-8) and the "
    "expected block (23 of 23, 23 of 23); c208 matches Method 1 (L09.html line 182) and Propositions 3.2(a) and 3.4; c155 matches "
    "Proposition 3.2(b), whose new cross-reference (Lesson 5, Definition 1.4) exists.")
row("cards-c208-duplicate", "10-cards-duplicates", "cards.json M3-c208 (new)", "PASS",
    "M3-c208 is new and not a duplicate: nearest fronts are c153 and c158 with distinct questions (token Jaccard < 0.5).")
row("cards-c167-misconception", "10-cards-lesson", "cards.json M3-c167 (changed)", "PASS",
    "Text checked against L09 lab code (is_correlation, lines 261-265) and expected block (lines 343-344); Remark 2.2 exists "
    "(L09.html line 94).")
row("cards-c209-c213-new", "10-cards-lesson", "cards.json M3-c209 to c213 (new)", "PASS",
    "c209 column space = {A gamma} (L07.html line 56, Section 1); c210 cosine (L08.html line 137, Section 3); c212 tenor and "
    "c213 yield change in bp with 1 bp = 0.01 percentage point (L08.html line 56, Section 1). c211 is the FAIL row above.")
row("cards-c131", "10-cards-lesson", "cards.json M3-c131; L08.html Proposition 1.1", "PASS", "Carried from round 10: "
    "L08 Proposition 1.1 unchanged; re-checked: M symmetric and x'Mx = ||X~x||^2/(T-1).")
row("cards-c204", "10-cards-ids", "cards.json (no M3-c204)", "PASS", "No M3-c204 in cards.json (gap, see cards-id-sequence).")
row("cards-c144-prop23-hypothesis", "10-cards-hypotheses", "cards.json M3-c144; L08.html Proposition 2.3", "PASS",
    "Doubling X multiplies M and eigenvalues by 4; shares unchanged by Proposition 2.3 with c = 2; hypothesis F1 to F4 carried.")
row("cards-c163-lab-count", "10-cards-lab-numbers", "cards.json M3-c163; L09.html Lab 1 expected block", "PASS",
    "All 23 counts match the expected block (23 of 23 for both counts).")
row("cards-sample-lesson-text-current", "10-cards-current-text", "L07.html, L08.html, L09.html, project.html, cards.json", "PASS",
    "Cards cite the current text: the L08 Section 3 rewrite (c207, c210) and the L08 title used by the hub card (index.html "
    "L08 card and L08.html line 36 agree; no stale 'Yield-Curve Factors' string anywhere outside ledgers).")
row("lesson-l08-section3-text", "1-lesson-math", "course/modules/M/M3/L08.html lines 137-141 (changed)", "PASS",
    "Checked: with exactly two distinct tenor values, tau^2 = -ab iota + (a+b) tau (so the curvature shape is zero); with three "
    "distinct values the shapes are nonzero (Vandermonde independence) and mutually orthogonal after orthogonalization. "
    "Definition 3.1 'exactly one principal direction attains the largest |cos|' matches the labels in c207.")
row("lesson-l09-prop32b-reference", "3-cross-reference", "course/modules/M/M3/L09.html line 119 (Proposition 3.2(b))", "PASS",
    "The new reference (Lesson 5, Definition 1.4) exists: L05.html Definition 1.4 '(positive semidefinite and positive definite)'.")
row("links-and-anchors", "links", "course/modules/M/M3/project.html; index.html; L08.html", "PASS",
    "check_pages M3 PASS; anchors used by project.html (placement, grader-section, report, stretch, conventions) resolve.")

registry_flags = [
    "\\iota (boldsymbol iota, the all-ones vector) is not in notation/notation.json. The project page (line 249) and L08 Section 3 "
    "define it locally at first use. Only program-wide symbols are registered (notation.json 'about'). Builder may request "
    "registration if it is meant to be program-wide."
]
freshness_flags = [
    "Not checked: literature on nearest correlation matrices and alternating projections (no search run; the slice cites no "
    "new sources)."
]
notes = [
    "Scope: the brief says six alternatives. ledgers/M3/alternatives/ holds ten; all ten were run on seeds 0-9, and alt10 on "
    "seeds 0-49. All pass.",
    "Round-10 FAIL rows re-verified. mutants-r15d-description is fixed at ccaeeaf. scope-repair-weights-vs-brief is PASS: the "
    "brief asks only whether the weight formula applies to each repair, and the page answers it with reasons.",
    "Grader change at ccaeeaf (as_verdict, ndarray acceptance): the NumPy-return probe passes on seeds 0-9, so the round-10 "
    "observation is resolved.",
    "Grader observation (not a row): test_is_psd_accepts_eigenvalue_exactly_at_minus_tol requires equality at the boundary, "
    "which the spec states ('at least -tol'). An implementation that rounds its eigenvalue one ulp below -0.5 would be refused "
    "by its own is_psd. The reference and all alternatives pass.",
    "Instance observation: eigenvectors are rounded to 12 decimals, so orthonormality holds to 1.8e-11, not exactly. All "
    "grader tolerances are far above this.",
    "Cards: the only defect is M3-c211 (missing Theorem 1.2 hypothesis). M3-c208 to c213 are new and checked; M3-c167 changed "
    "and is checked against the L09 lab.",
    "Hours: 45 in the table and the data attribute; 105 + 45 = 150 module total.",
    "Live reference check: tools/verify_refs.py --unit M3 (plain run): 2 of 560 entries, 0 problems.",
    "Not checked: a Pyodide browser run of the autograder (beyond page_smoke); a rendered screenshot of project.html; the "
    "self-assessment form's JavaScript; L01-L07 lesson bodies except where cards cite them (carried from round 10); alternatives "
    "1-9 beyond seeds 0-9; the live references beyond M3's two keys; the SVD probe beyond seeds 0-9.",
]

fails = [r for r in rows if r["status"] != "PASS"]
ledger = {
    "unit": "M3",
    "slice": "d",
    "round": 11,
    "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, round 11; shares no context with the builders",
    "pin": "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87",
    "base": "round-10 pin 47a36d8c (fragment /Users/billyribeiro/.fanout/frags/D-M3-d.round10.json, read as context; its PASS rows were not trusted). Delta 47a36d8..ccaeeaf for this slice: project.html (lines 117-118, 201, 237, 245-247, 475-477 area and Exemplar B line 615), grader/test_project.py (as_verdict, ndarray acceptance), cards.json (M3-c167 changed; M3-c208 to c213 new), L08.html line 137 (Section 3), L09.html line 119 (Proposition 3.2(b)), index.html L08 card, references.json used_by, tests/labs/M3/lab-M3-project-1.py and -2.py (comments), and four mutant files (r15d_m01, r15d_m02 docstrings) plus three new v11d mutants written this round.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD11-M3-d",
    "scratch": "ledgers/M3/scripts/M3-d-r11/",
    "verified_at": "2026-11-05T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": registry_flags,
    "freshness_flags": freshness_flags,
    "notes": notes,
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": len(fails),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
    },
}
OUT.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "fail", len(fails), "mutants", len(mutants), "killed", ledger["summary"]["mutants_killed"])
