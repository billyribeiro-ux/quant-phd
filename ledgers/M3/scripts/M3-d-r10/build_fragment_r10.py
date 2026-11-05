"""Round-10 verifier (M3 slice d): assemble ledgers/M3/M3-d.json from the r10 evidence in out/ and the mutation output.
Run from the checkout root: .venv/bin/python ledgers/M3/scripts/M3-d-r10/build_fragment_r10.py"""

import json
import re
from datetime import UTC, datetime

from pathlib import Path

ROOT = Path.cwd()
OUT = "ledgers/M3/scripts/M3-d-r10/out/"
SC = "ledgers/M3/scripts/M3-d-r10/"

rows = []


def row(rid, check, location, status, evidence, fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# ---- gates (re-run on pin 47a36d8c) ----
row("gate-check-pages", "gate-check_pages", "course/modules/M/M3/*", "PASS",
    f"{OUT}check_pages_M3.out: 'check_pages M3: PASS', exit 0 (tools/check_pages.py --unit M3 at 47a36d8c).")
row("gate-check-dag", "gate-check_dag", "course/modules/M/M3/*", "PASS",
    f"{OUT}check_dag_M3.out: 'check_dag M3: PASS', exit 0.")
row("gate-check-projects", "gate-check_projects", "course/modules/M/M3/project.html", "PASS",
    f"{OUT}check_projects_M3.out: 'check_projects M3: PASS', exit 0.")
row("gate-run-labs", "gate-run_labs", "tests/labs/M3/*.py; project.html", "PASS",
    f"{OUT}run_labs_M3.out: 'run_labs M3: PASS (12/12)', exit 0; {SC}out/labs_twin_vs_page_r10.out: the three project "
    "twins run under python -I -W error with exit 0, and each expected block equals its twin's output.")
row("gate-run-graders", "gate-run_graders", "course/modules/M/M3/grader/", "PASS",
    f"{OUT}run_graders_M3.out: 'run_graders M3: PASS (reference 50/50 seeds)', exit 0 (seeds 0-49).")
row("gate-page-smoke", "gate-page_smoke", "course/modules/M/M3/project.html", "PASS",
    f"{OUT}page_smoke_project.out: 'page_smoke M3: PASS', exit 0 (project page alone).")
row("gate-ruff", "gate-ruff", "tests/labs/M3; course/modules/M/M3/grader", "PASS",
    f"{OUT}ruff_check.out 'All checks passed!' and ruff_format.out '16 files already formatted' (run on the M3 labs and grader); "
    "the four new mutants pass ruff check --force-exclude and ruff format --check.")
row("gate-mypy", "gate-mypy", "repository", "PASS",
    f"{OUT}mypy.out: 'Success: no issues found in 385 source files' (mypy --no-incremental).")
row("gate-verify-refs", "gate-verify_refs", "references/references.json", "PASS",
    f"{OUT}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'; {OUT}verify_refs_M3_live_r10.out: "
    "'live re-verification of M3: 2 of 560 entries, 0 problems' (tools/verify_refs.py --unit M3, plain run).")
row("gate-collect-only", "gate-collect-only", "course/modules/M/M3/grader/test_project.py; project.html", "PASS",
    f"{OUT}collect_only_M3.out: '163 tests collected' on the staged copy ({SC}stage_grader_r10.sh); project.html line 237 "
    "states 163 tests.")
row("gate-pytest-relevant", "gate-pytest", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, "
    "test_memo_exemplars.py, test_page_smoke.py", "PASS",
    f"{OUT}pytest_relevant_r10.out: five modules, exit 0 (pytest -q, tests/ at 47a36d8c).")
row("gate-mutate-m3", "gate-mutate_graders", "ledgers/M3/mutants/ (168 files)", "PASS",
    f"{OUT}mutate_M3_seeds0-9_r10.out: 'mutate_graders M3: PASS (168/168 killed)', exit 0 (tools/mutate_graders.py "
    "--unit M3 --seeds 0-9), including the four new v10d mutants.")
row("gate-reference-starter", "gate-reference-starter", "grader/reference.py; grader/starter.py", "PASS",
    f"{OUT}reference_seed0_r10.out: '163 passed' (QF_SEED=0, --assert=plain -W error); starter_seed0_r10.out: "
    "'162 failed, 1 passed'.")
row("gate-alternatives-seeds-0-49", "gate-alternatives", "ledgers/M3/alternatives/alt1..alt10", "PASS",
    f"{SC}out/alts_seeds0-9_r10.out (run_alts_r10.sh): all ten alternatives PASS 163/163 on each of seeds 0-9. "
    "Seeds 0-49 were not re-run this round; the alternatives are byte-identical since the round-9 pin.")
row("alternatives-svd-probe", "2.6-alternative-svd", "ledgers/M3/scripts/M3-d-r10/probes/alt11_svd_signed_eigenvalues.py",
    "PASS", "SVD-based correct alternative (signed eigenvalues from the SVD, lstsq weights, SVD projection step): "
    "163 passed on each of seeds 0-9 (run in /private/tmp/verifyD10-alt11 with the grader's suite, -W error).")
row("alternatives-count-and-seeds", "2.6-alternatives", "ledgers/M3/alternatives/ (10 files)", "PASS",
    f"{SC}out/alts_seeds0-9_r10.out: ten alternatives, all PASS on seeds 0-9 (count is 10, above the required five).")

# ---- grader (byte-identical to the round-9 pin; re-read in full this round) ----
row("grader-instance", "2.6-grader-instance", "course/modules/M/M3/grader/instance.py; project.html line 231", "PASS",
    f"instance.py read in full (110 lines). {SC}instances_check_r10.py + out/instances_check_r10.out: seeds 0-19 each "
    "valid (k in {3,4,5}; corr unit-diagonal, symmetric, entries within 0.95; min eigenvalue below -0.02; psd_corr "
    "positive definite with unit diagonal; vols in range; psd_spectrum[0] = 0; eigenvectors orthonormal). The 20 min "
    "eigenvalues and 20 weight vectors are all distinct.")
row("grader-test-count-and-purity", "2.6-grader-test-count", "grader/test_project.py lines 794-831; project.html line 237",
    "PASS", "collect-only 163 equals the page's 163. test_functions_print_nothing (794-802) and "
    "test_inputs_are_not_mutated (805-831) exist; test_repeated_calls_agree (852-870).")
row("grader-standard-library-only", "2.6-grader-imports", "grader/test_project.py lines 834-849; project.html line 235",
    "PASS", "test_module_imports_only_standard_library_or_numpy walks the AST and allows numpy and sys.stdlib_module_names; "
    "project line 235 states the standard library and NumPy only.")
row("grader-lab3-reference-numbers", "2.6-grader-lab3-numbers", "grader/test_project.py lines 503-543; project.html Lab 3",
    "PASS", f"Test values -0.142113, 0.176573 (1e-6), 0.175003 (1e-5), 0.011516 (1e-5), weights 1.778929/-1.096718/"
    f"-0.255613/0.573402 (1e-6). {OUT}numbers_numpy_r10.out (independent NumPy eigh and solve, not the page's Jacobi): "
    "-0.142113, 0.176573, 0.175003, 0.011516, weights identical to the printed 6 decimals.")
row("grader-failure-messages-leak-answers", "2.6-grader-messages", "grader/test_project.py (every assert, pytest.fail, "
    "must_raise message)", "PASS", "Every assert and pytest.fail message was read (lines 115-130, 141, 149, 241-273, 286-297, "
    "303-311, 330-357, 382-454, 486-500, 543, 556-583, 619, 650-870). None interpolates an expected or computed value; "
    "only property names and the Lab 3 quantity name are printed.")
row("grader-named-conditions", "2.6-grader-named-conditions", "grader/test_project.py lines 134-200, 680-784; project.html line 248",
    "PASS", "must_raise is used only for the four named conditions: non-square (177-180, 695-702), asymmetry beyond 1e-9 "
    "(185-190, 223-230, 707-711, 744-747), volatility not strictly positive (752-758), length mismatch (778-784). "
    "must_not_raise cases use inputs the page calls valid (exact and sub-tolerance asymmetry). grep: no pytest.raises.")
row("grader-browser-timeout", "2.6-grader-browser", "project.html line 235; course/assets/js/python.js line 4",
    "PASS", "python.js line 4: TIMEOUT_MS = 120000, matching the 120 seconds on project.html line 235.")
row("grader-reference-docstring", "2.6-reference-docstring", "grader/reference.py lines 1-5, 109-110", "PASS",
    "Docstring names Jacobi eigenvalues and alternating projections with correction terms; matches lines 33-63 and 109-128.")
row("grader-spec-rubric-counts", "2.6-spec-counts", "project.html lines 237, 490, 495, 498-502", "PASS",
    "Five criteria C1-C5 with four levels each (rows 498-502); 163 tests (line 237); 'meets the bar at level 3 or above' (lines 237, 490, 495, 503).")
row("spec-projection-tol-undefined", "spec-tol-defined", "project.html lines 233, 246; grader/starter.py lines 30-36", "PASS",
    "tol is the stopping tolerance of the projection (line 233 and conventions line 246: gap and change both at most tol); "
    "starter.py docstring says the stopping rule is the learner's choice.")
row("grader-projection-spec-vs-reference", "2.6-spec-vs-reference", "grader/reference.py lines 109-128; project.html line 246",
    "PASS", "Compared line by line: J=P(W+E); E=W+E-J; N=J+H with diagonal set to 1; H=J+H-N; W=N; gap=||N-J||_F; "
    "change=||N-W_prev||_F; stop when both <= tol; at most max_iter steps. Matches (reference 116-127; "
    "test_projection_repair_runs_exactly_max_iter_steps at tol 0, steps 1-3 passes for all reference runs).")
row("grader-weights-spec-vs-reference", "2.6-spec-vs-reference", "grader/reference.py lines 131-150; project.html line 247",
    "PASS", "Sigma = SCS, solve Sigma x = iota by Gauss-Jordan with partial pivoting, normalise to sum 1; ValueError for "
    "length mismatch and non-positive volatility (136-138). Closed form (A3) matches a NumPy linear solve to 1e-16 "
    f"({OUT}numbers_numpy_r10.out).")
row("grader-numpy-bool-return", "2.6-grader-return-types", "grader/test_project.py lines 286-289, 297-368, 373",
    "PASS", "Observation, not a finding: the is_psd asserts compare with 'is True'/'is False'. A correct NumPy is_psd whose "
    f"result is numpy.bool_ (probe {SC}probes/probe_numpy_bool_is_psd.py) fails 14 is_psd tests. The starter annotates "
    "-> bool, so this is a return-type deviation, not a numerical alternative; recorded in notes for the builder to decide.")
row("grader-failure-messages-r10", "2.6-grader-no-leak", "grader/test_project.py", "PASS",
    "No test embeds the expected value in its message (checked with the list in grader-failure-messages-leak-answers).")

# ---- mutants ----
row("mutants-existing-140", "mutants-all-existing", "ledgers/M3/mutants/ (all 164 files before this round)", "PASS",
    f"{OUT}mutate_M3_seeds0-9_r10.out: every existing mutant KILLED on seeds 0-9 (168/168 with the four new ones).")
row("mutants-new-student-errors", "mutants-v4d", "ledgers/M3/mutants/v4d_02..v4d_04", "PASS",
    f"{OUT}mutate_M3_seeds0-9_r10.out: each KILLED.")
row("mutants-v2d-01-05", "mutants-v2d", "ledgers/M3/mutants/v2d_01..v2d_05", "PASS", f"{OUT}mutate_M3_seeds0-9_r10.out: each KILLED.")
row("mutants-v2d-06", "mutants-retired-v2d06", "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py", "PASS",
    f"Retired (correct alternative, the page allows NumPy). {OUT}retired_v2d06_seeds0-9_r10.out: '163 passed' on each of seeds "
    "0-9; the file is byte-identical to the round-9 pin.")
row("mutants-v3d-02-05", "mutants-v3d", "ledgers/M3/mutants/v3d_02..v3d_05", "PASS", f"{OUT}mutate_M3_seeds0-9_r10.out: each KILLED.")
row("mutants-v5d-new-student-errors", "mutants-v5d", "ledgers/M3/mutants/v5d_02, v5d_03, v5d_05, v5d_06", "PASS",
    f"{OUT}mutate_M3_seeds0-9_r10.out: each KILLED.")
row("mutants-r6-new-student-errors", "mutants-r6d", "ledgers/M3/mutants/r6d_m02..r6d_m04", "PASS", f"{OUT}mutate_M3_seeds0-9_r10.out: each KILLED.")
row("mutants-r7-new-student-errors", "mutants-r7d", "ledgers/M3/mutants/r7d_m01..r7d_m03", "PASS", f"{OUT}mutate_M3_seeds0-9_r10.out: each KILLED.")
row("mutants-v8d-new-student-errors", "mutants-v8d", "ledgers/M3/mutants/v8d_01..v8d_04", "PASS", f"{OUT}mutate_M3_seeds0-9_r10.out: each KILLED.")
row("mutants-v9d-new-student-errors", "mutants-v9d", "ledgers/M3/mutants/v9d_01..v9d_04", "PASS", f"{OUT}mutate_M3_seeds0-9_r10.out: each KILLED.")
row("mutants-v10d-new-student-errors", "2.6-mutation (new this round, 4 >= 3)", "ledgers/M3/mutants/v10d_01..v10d_04; "
    f"{SC}make_mutants_v10d_r10.py", "PASS",
    "v10d_01 projection PSD step uses clipping with rescaling (killed by test_lab3_reference_numbers_are_matched); "
    "v10d_02 min_eigenvalue reads only the lower triangle with no symmetry check (killed by test_non_square_is_refused, "
    "and by the asymmetry tests in the same run); v10d_03 projection returns the iterate before the last step (killed by "
    "test_projection_repair_runs_exactly_max_iter_steps[1]); v10d_04 Sigma_ij = C_ij v_j^2 (killed by "
    f"test_lab3_reference_numbers_are_matched). All in {OUT}mutate_M3_seeds0-9_r10.out.")
row("mutants-r15d-description", "2.6-mutation-description", "ledgers/M3/mutants/r15d_m01_is_psd_strict_boundary.py:1; "
    "ledgers/M3/mutants/r15d_m02_rescale_missing_sqrt_on_column.py:1", "FAIL",
    f"{OUT}mutate_M3_seeds0-9_r10.out lines 'KILLED r15d_m01...' and 'KILLED r15d_m02...': the description printed for both is "
    "the module docstring's first line, 'Reference solution for the M3 project, covariance_doctor.py. Not shipped to "
    "learners.' VERIFIER_RULES 2.6-3 requires the first docstring line to describe the error. Both files are otherwise "
    "killed (test_is_psd_accepts_eigenvalue_exactly_at_minus_tol; test_clip_repair_has_unit_diagonal_and_is_symmetric).",
    "Rewrite the first docstring line of each file to name its error, e.g. r15d_m01: 'is_psd uses a strict inequality, so "
    "a smallest eigenvalue exactly at -tol is refused.' (this duplicates r3d_m01 and r7d_m02; retire it or keep it with the "
    "new line). r15d_m02: 'clip_repair divides entry (i, j) by sqrt(d_i) * d_j, so the rescaled matrix is not symmetric.'")
row("mutants-v5d-01-equivalent-moved", "equivalent-alt10-bitwise", "ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py",
    "PASS", f"{SC}out/equiv_alt10_r10.out: 'trials 10000 outputs differing 0' (1000 random symmetric matrices, sizes 2-6, "
    "max_iter in {1,2,3,5,20}, tol in {0, 1e-10}, exact list equality).")
row("mutants-v5d-04-accepted-stop-rule", "alternative-stop-either", "ledgers/M3/alternatives/alt10_stop_when_either_gap_or_change.py",
    "PASS", f"{SC}out/alts_seeds0-9_r10.out: PASS on seeds 0-9.")
row("equivalent-r6d-m04", "alternative-gap-only-stop", "ledgers/M3/alternatives/alt7_dykstra_gap_only_stop.py", "PASS",
    f"{SC}out/alts_seeds0-9_r10.out: PASS on seeds 0-9.")
row("equivalent-r11d-m02", "alternative-step-only-stop", "ledgers/M3/alternatives/alt8_dykstra_step_only_stop.py", "PASS",
    f"{SC}out/alts_seeds0-9_r10.out: PASS on seeds 0-9.")
row("equivalent-r15d-m03-label", "alternative-full-budget", "ledgers/M3/alternatives/alt9_dykstra_runs_full_budget.py", "PASS",
    f"{SC}out/alts_seeds0-9_r10.out: PASS on seeds 0-9.")
row("equivalent-readme-citation", "equivalent-readme", "ledgers/M3/equivalent/README.md", "PASS",
    "The cited ledgers/M3/scripts/M3-d-r7-fixer/equiv_alt10_check.py exists. Its claim (10000 trials, 0 differing) "
    f"was re-run as {SC}equiv_alt10_r10.py: 10000 trials, 0 differing. The README proof steps 1-5 were read against "
    "reference lines 116-127: H_0 = 0, off-diagonal H is exactly 0.0 (J + 0.0 - J), so the correction term is inert.")

# ---- project page (changed this round: lines 117, 199, 231, 245, 246, 475, 615) ----
row("project-numbers", "project-printed-numbers", "project.html lines 57, 138, 143, 221, 290, 460-475, 581, 603, 615, 619, 628",
    "PASS", f"{OUT}numbers_numpy_r10.out (independent NumPy): Lab 1 eigenvalues -0.275297/1.463830/1.811467, rebuilt diagonal "
    "1.096064/1.104409/1.074824, repaired off-diagonal 0.636095/-0.382551/0.469578; Lab 2 eigenvalues -0.203711/1.486490/"
    "1.717222, rebuilt diagonal 1.060165/1.075224/1.068322; Lab 3 min eigenvalue -0.142113, distances 0.176573 and 0.175003 "
    "(gap 0.001570), max entry difference 0.011516, det -0.2616, weights 1.778929/-1.096718/-0.255613/0.573402, the 4dp "
    "weights sum to 1.0. The exemplar sentence 'rounded values sum to 0.99' (line 552): 1.78-1.10-0.26+0.57 = 0.99 checked.")
row("project-lab1-memo-sentence", "project-lab1", "project.html lines 57, 138; tests/labs/M3/lab-M3-project-1.py", "PASS",
    f"{SC}out/labs_twin_vs_page_r10.out: 'page code identical to twin'; expected block equals twin output. Hypothesis "
    "(smallest eigenvalue negative, verdict False, diagonal 1 to six decimals, passes at 1e-9) matches the output.")
row("project-lab2-completion", "project-lab2", "project.html lines 141-222; tests/labs/M3/lab-M3-project-2.py", "PASS",
    f"{SC}out/labs_twin_vs_page_r10.out: the page code differs from the twin only at the two intended blanks (line 193 "
    "'___' for 'smallest >= -1e-10'; line 201 '___' for 'math.sqrt(d[i] * d[j])'); the twin's output equals the expected "
    "block. Interpretation (line 221) checked against the output.")
row("project-lab3-check", "project-lab3", "project.html lines 287-476; tests/labs/M3/lab-M3-project-3.py", "PASS",
    f"{SC}out/labs_twin_vs_page_r10.out: page code identical to twin; expected equals output. Hypothesis (line 290) entries "
    "0.7,0.3,-0.6,0.5,0.4,0.2 and volatilities 0.10,0.20,0.15,0.30 match the code; the six named functions match lines 306-424.")
row("project-lab3-diagonal-positivity-sentence", "project-lab3-proof-chain", "project.html line 475 (and exemplar B, lines 603, 615)",
    "PASS", "Chain: completed rescaling (math.sqrt(d[i]*d[j]) never fails and never divides by zero) => every d[i]*d[j] > 0 "
    "=> every d[i] nonzero with one sign; A1 => d[i] >= 0 (take z = i-th unit vector) => positive diagonal. Valid. Numerically "
    f"the clipped diagonal is 1.05628, 1.045743, 1.000014, 1.040076 ({OUT}numbers_numpy_r10.out).")
row("project-spec-grader", "project-spec", "project.html lines 229-237", "PASS",
    "Inputs (SIMULATED, grader/instance.py), required functions and signatures (line 233) match starter.py lines 15-41 and "
    "reference.py; constraints (235) and grading mode (237) match test_project.py and the 120 s timeout.")
row("project-conventions-math", "project-conventions", "project.html lines 242-249; grader/reference.py", "PASS",
    "Frobenius, PSD, clipping, weights and the four ValueError conditions match reference.py (_as_matrix 17-30, _rescale 78-83, "
    "comparison_weights 131-150). Clipping and weights formulas re-derived with NumPy (numbers_numpy_r10.out).")
row("project-conventions-link", "project-conventions-link", "project.html line 243; course/modules/M/M3/L05.html", "PASS",
    "L05.html#def-positive-semidefinite-matrix exists (L05.html line 72, Definition 1.4); 'Lesson 5 gives the definition by the "
    "quadratic form' is consistent with Definition 1.4.")
row("project-proof-A1", "2.4-proof", "project.html appendix A1 (line 641)", "PASS",
    "Read in full. z^T X z = sum max(lambda_i, f)(V^T z)_i^2 >= 0 since max(lambda_i, f) >= f >= 0. Hypotheses named: real "
    "symmetric input, f >= 0, F1-F4 for the spectral theorem (L04 Theorem 2.3, L04.html line 130).")
row("project-proof-A2", "2.4-proof", "project.html appendix A2 (line 642)", "PASS",
    "Read in full. Y_ii = X_ii/(sqrt d_i)^2 = 1; z^T Y z = q^T X q with q = D^(-1/2) z >= 0. Positivity of d_i is named as needed.")
row("project-proof-A3", "2.4-proof", "project.html appendix A3 (line 643)", "PASS",
    "Read in full. det Sigma = a^2 b^2 (1-rho^2); Sigma^{-1} iota = (b(b-rho a), a(a-rho b))/det; sum = a^2+b^2-2 rho ab = "
    "(a-b)^2 + 2ab(1-rho) > 0; scaling by c leaves weights unchanged. Hypotheses |rho| < 1, a, b > 0 named. NumPy: closed form "
    "vs linear solve max difference 1.4e-17 to 2.2e-16 on three (a, b, rho) sets, and under scaling by 7 (numbers_numpy_r10.out).")
row("project-proof-A4", "2.4-proof", "project.html appendix A4 (line 643)", "PASS",
    "Read in full. X u_i = V Lambda_0 e_i = 0 for lambda_i < 0, so X singular; with positive diagonal z = D^(1/2) u_i gives Yz = 0; "
    "Sigma S^{-1} z = S Y z = 0 for every v > 0. Each step checked; hypotheses (F1-F4, negative eigenvalue, positive diagonal) named. "
    "NumPy: min eigenvalue of clipped X -7.5e-17, of Sigma(clip) -3.4e-18 (numbers_numpy_r10.out).")
row("project-hours", "2.6-hours", "project.html lines 259-265; course/modules/M/M3/index.html; L01-L09 data-hours", "PASS",
    "Project table 2+3+14+8+12+6 = 45 (line 265 total 45; hub data-hours-project 45). Lesson hours 12+11+12+12+12+11+11+12+12 = 105 "
    "(hub data-hours-lessons 105). Hub 105 + project 45 = 150. Own estimate of the components: rung 1 about 1-2 h, rung 2 about 2-3 h, "
    "engine about 10-16 h, weights about 6-10 h, report and four proofs about 10-16 h, self-check about 4-6 h: total within 30% of 45.")
row("project-exemplars", "2.3-rubric-calibration", "project.html lines 507-652", "PASS",
    "Both exemplars read in full. Blind scoring against the rubric alone: Exemplar A 2,2,2,1,2 (C4 has no SIMULATED label, so level 1; "
    "C5 names one limitation, level 2); Exemplar B 4,4,4,3,3 (C4 lacks an explicit no-market-claim statement; C5 gives a direction only "
    "for clipping). Official scores data-scores 2,2,2,1,2 and 4,4,4,3,3: match within one level on every criterion.")
row("project-rubric", "2.3-rubric", "project.html lines 486-503", "PASS",
    "Five criteria, four levels each; levels nest ('Everything in level 3, and ...'); scoring rule (line 490) matches the cell text.")
row("rubric-C4-level2-vague", "rubric-observable", "project.html line 501 (C4 row)", "PASS",
    "Level 2 names 'Labels some inputs, or states a conclusion ... from a printed result'; level 1 'No input is labelled'. Each level is observable.")
row("project-references", "2.9-references", "project.html lines 670-681; references/references.json", "PASS",
    "data-cite axler2024linear and strang2023introduction are both registry keys (references.json entries, verified_by crossref / "
    "openlibrary). The page cites them only in the reading list and attributes no statement to them (line 672).")
row("project-no-process-words", "2.9-process-words", "project.html; cards.json; grader/*.py; tests/labs/M3/lab-M3-project-*.py",
    "PASS", "grep -i over these files for builder, verifier, verification, round N, fixer, ruling, architect, slice, checkout, "
    "TODO, TBD, lorem, placeholder, 'for brevity', 'beyond the scope', 'it is important to note', 'clearly', 'obviously', "
    "'simply', 'just ': no match.")
row("project-stretch", "2.6-stretch", "project.html lines 661-668", "PASS",
    "Three stretch items; the count item states its seeds, generator and count rule (line 665). No claim is made.")
row("project-links", "2.9-links", "project.html (26 distinct href/src values)", "PASS",
    f"{SC}links_r10.py, out/links_r10.out: 26 distinct references, none missing, no external URLs, every #anchor exists in its "
    "target page.")
row("project-brief-scope", "2.6-scope", "project.html line 229-233, 262, 475, 615", "PASS",
    "Rung 3 covers diagnose and both repairs (curriculum brief items 1 and 2). The brief's third clause is the FAIL row "
    "scope-repair-weights-vs-brief.")
row("scope-repair-weights-vs-brief", "2.6-scope", "curriculum/01-foundations.yaml:185-188 (brief); project.html lines 262, "
    "475, 615; plans/M3-build-plan.md section 4 and B3", "FAIL",
    "The brief says: 'Compare the effect of each repair on downstream portfolio weights.' project.html line 475 and exemplar B "
    "line 615 say the page gives no weights for either repaired matrix ('So this page does not compare the weights of the two "
    "repairs'). The plan's rung 3a second part is 'Compute weights for each repair and check the properties in the grader' "
    "(section 4 table). Architect decision B3 (plans/M3-build-plan.md lines 369-373; 'Architect decisions' 2026-10-28) fixed the "
    "closed-form weights and their naming, but did not waive the comparison. Numerically the comparison is blocked on Lab 3's "
    f"matrix: Sigma of the clipped repair has smallest eigenvalue -3.4e-18 and of the projection -4.9e-13 "
    f"({OUT}numbers_numpy_r10.out), so neither repair has a computable weight vector. The brief's comparison is therefore not "
    "delivered, and the page says so.",
    "Architect decides one of: (a) a curriculum change request replacing the brief's 'compare the effect on weights' with "
    "'state where the weight formula applies to each repair', then the plan and page follow; or (b) the builder chooses a "
    "matrix and volatilities for which both repaired Sigma are invertible, prints both weight vectors in Lab 3, adds the "
    "grader tests for them, and updates lines 475 and 615 and the exemplars to match.")
row("spec-stop-rule-sentence", "spec-stop-rule", "project.html line 246 (conventions, 'Alternating steps')", "PASS",
    "Round-9 FAIL is fixed at 47a36d8c: line 246 now reads 'An implementation may stop early by any rule of its own choosing; "
    "the reference stops after a step whose gap and change are both at most tol'. Consistent with starter.py lines 30-36 and "
    "with the test that fixes the update (tol = 0, steps 1-3).")
row("project-lab3-weights-sentence", "project-lab3-weights", "project.html line 475; tests/labs/M3/lab-M3-project-3.py", "PASS",
    "The sentence that the projection's Sigma is singular exactly when its matrix is (S invertible, same rank) is correct. The "
    "page does not claim a proof for the projection, and labels the printed -0.000000 as numerical evidence only.")

# ---- notation and DAG ----
row("notation-registry", "3-notation", "project.html math (123 spans); notation/notation.json", "PASS",
    "Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q are not used on project.html; registered macro \\diag is "
    "used as 'diagonal matrix'; \\tr, \\R, \\E, \\Var, \\Cov, \\Corr, \\N, \\Prob are not used. Local symbols (V, Lambda, Sigma, "
    "C, S, D, X, Y, W, E, H, J, N, P, f, k, v, a, b, rho) are defined at first use, as notation.json's 'about' allows.")
row("notation-R-macro", "3-notation", "project.html; L07.html; L08.html; L09.html; cards.json", "PASS",
    "grep: project.html contains no \\R macro; cards.json writes R^n as plain text.")
row("dag-linked-concepts", "14-dag-links", "project.html concept links", "PASS",
    "Three concept links: eigendecomposition (L03.html#def-eigendecomposition), spectral-theorem (L04.html#def-spectral-theorem), "
    "positive-semidefinite-matrix (L05.html#def-positive-semidefinite-matrix). All in M3's prerequisite closure.")
row("dag-m4-concepts-by-name", "14-dag-names", "project.html; cards.json; L01-L09", "PASS",
    "Out-of-closure names scanned: 'covariance' (8) and 'correlation' (3) are prose-only under the architect's B1/Q2 decision "
    "(plans/M3-build-plan.md 'Architect decisions': covariance is the formula with no concept link); 'variance' (2) is prose; "
    "'portfolio' (3) is a plain word; 'Gaussian' occurs only in 'Gaussian elimination'; no Cholesky, IEEE 754, minimum-variance, "
    "mean-variance or quadratic-programming concept appears.")
row("dag-cholesky-named-in-grader", "14-dag-cholesky", "course/modules/M/M3/grader/*; M3 slice files", "PASS",
    "grep -ril cholesky over course/modules/M/M3 and tests/labs/M3/lab-M3-project-*.py: no match.")

# ---- cards ----
row("cards-structure", "7-cards-structure", "course/modules/M/M3/cards.json (202 cards)", "PASS",
    f"{SC}out/cards_r10.out: 202 cards, unique ids; keys id, lesson, front, back (+ grade and basis on 156); grades T 117, C 39, "
    "none 46; every C card has a basis; no T card mentions a lab, SIMULATED or a seed.")
row("cards-id-sequence", "7-cards-ids", "course/modules/M/M3/cards.json ids", "PASS",
    f"{SC}out/cards_r10.out: gaps in M3-c001..c207 at c102, c148, c191, c204, c206; no card or page refers to a missing id.")
row("cards-numbers-cited", "2.7-cards-numbers", "cards.json front and back", "PASS",
    f"{SC}out/cards_r10.out: every decimal number on every card occurs in its lesson text or in a twin output (0 misses).")
row("cards-labels-cited", "2.7-cards-labels", "cards.json grade and basis fields", "PASS",
    f"{SC}out/cards_r10.out: every C card has a basis; no T card cites a lab or SIMULATED output; every 'Definition/Proposition/"
    "Remark/Example/Theorem/Lemma/Corollary/Fact n.m' on a card occurs in that card's own lesson (0 missing).")
row("cards-duplicate-scan", "2.7-cards-duplicates", "cards.json (all 20301 pairs)", "PASS",
    f"{SC}out/cards_r10.out: 20301 pairs by token Jaccard; no exact duplicate front or back. Top pairs read: c025/c187 (kernel vs "
    "image), c135/c186 (k=1 vs k>=2 maximizers), c136/c201 (sum of squared scores vs its maximum), c194/c195 (P symmetric vs "
    "P^2 = P), c119/c195, c118/c119 (distinct claims about P), c082/c193 (PSD vs PD). Each pair asks different content.")
row("cards-sample-20", "2.7-cards-sample", "cards.json: indices 0, 10, ..., 200 (21 cards) and every card changed this round",
    "PASS", "Read in full: c001, c011, c021, c031, c041, c051, c061, c071, c081, c091, c101, c112, c121, c122, c127 (changed), "
    "c132, c142, c153, c163 (changed), c173, c183, c194, c205 and the L08 cards c131, c140, c144, c145, c207. Each statement "
    "checked against its lesson and the arithmetic (e.g. c041 AN and NA; c112 A^T A; c183 squared distance 0.04 = 0.01+0.01+0.01+0.01).")
row("cards-lab-numbers", "2.7-cards-lab-numbers", "cards.json grade-C cards; tests/labs/M3/lab-M3-L0*-1.py outputs", "PASS",
    f"{SC}out/cards_r10.out; L09 twin output lines 10-12: '40 ... 23', 'is_correlation ... 23 of 23', 'strictly closer ... 23 of 23' "
    "(c163 'All 23', c167 'strictly closer'); L05 twin line 9: '100000 of 100000' (c173); L08 twin lines 8-10: cosines 0.9994, 0.9985, "
    "0.9990 (c140).")
row("cards-L01", "2.7-cards-lesson", "cards c001-c022, c169-c170; L01.html", "PASS",
    "Unchanged this round (L01.html and its cards byte-identical to the round-9 pin). Round-9 read of every cited label and "
    "statement is carried; the card-level script checks (numbers, citations) pass this round.")
row("cards-L02", "2.7-cards-lesson", "cards c023-c042, c184, c187; L02.html", "PASS",
    "Unchanged this round (byte-identical). Script checks (numbers, citations) pass; sampled cards c031 and c041 re-checked by hand.")
row("cards-L03", "2.7-cards-lesson", "cards c043-c062, c171-c172, c188; L03.html", "PASS",
    "Unchanged this round (byte-identical). Script checks pass; sampled c051 and c061 re-checked.")
row("cards-L04", "2.7-cards-lesson", "cards c063-c078, c192; L04.html", "PASS",
    "Unchanged this round (byte-identical). Script checks pass; sampled c071 re-checked.")
row("cards-L05", "2.7-cards-lesson", "cards c079-c100, c173, c176, c179, c180, c193, c203; L05.html", "PASS",
    "Unchanged this round (byte-identical). Script checks pass; sampled c081, c091 re-checked; c173 twin output checked.")
row("cards-L06", "2.7-cards-lesson", "cards c101-c114, c178, c205; L06.html", "PASS",
    "Unchanged this round (byte-identical). Script checks pass; sampled c101, c112, c205 re-checked by hand.")
row("cards-L07", "2.7-cards-lesson", "cards c115-c129, c168, c177, c194-c196; L07.html (line 437 nav only, changed)", "PASS",
    "c127 (changed this round) read and checked: the residual is orthogonal, not zero, under F1-F4 and independent columns. "
    "c121, c194, c195 re-checked; the L07 hunk is a navigation link only.")
row("cards-L08", "2.7-cards-lesson", "cards c130-c145, c174, c186, c197-c201, c207; L08.html lines 6, 36, 137, 141, 414-416", "PASS",
    "L08 changed hunks read (line 137 explicit centred squared tenors; line 141 wording; 414-416 renamed). c142 and c207 "
    "re-checked against the current text; c131 (Prop 1.1) and c144 (Prop 2.3 hypothesis: sum > 0) re-checked; c140 cosines "
    "checked against the twin.")
row("cards-L09", "2.7-cards-lesson", "cards c146-c167, c181-c183, c185, c202; L09.html lines 52, 597 (changed)", "PASS",
    "c163 (changed) and c167 (changed) read and checked: 'All 23' and 'strictly closer' match twin output lines 10-12. c183 "
    "squared distance 0.04 re-derived (Example 3.6 entries -0.1, 0.1). L09 hunk at line 52 read.")
row("cards-c131", "2.7-cards-id", "cards.json M3-c131; L08.html Proposition 1.1", "PASS",
    "Card states T >= 2 and symmetric PSD with x^T M x = ||X~ x||^2/(T-1); Proposition 1.1 has the same hypotheses.")
row("cards-c204", "2.7-cards-id", "cards.json (no M3-c204)", "PASS",
    "Id c204 is absent (gap listed in cards-id-sequence); no card to verify.")
row("cards-c144-prop23-hypothesis", "2.7-cards-id", "cards.json M3-c144; L08.html Proposition 2.3 (line 121)", "PASS",
    "Card says doubling X multiplies M by 4 and shares unchanged 'whenever the shares are defined (the eigenvalue sum is positive)'. "
    "Proposition 2.3 has that hypothesis (sum > 0) and a nonzero c.")
row("cards-c163-lab-count", "2.7-cards-id", "cards.json M3-c163; L09.html Lab 1 expected block", "PASS",
    "Card answer 'All 23' matches twin output line 'alternating-projection output passes is_correlation and is strictly closer to "
    "A than R: 23 of 23'; the 40 matrices match 'seeded 5x5 matrices: 40'.")
row("cards-c208-duplicate", "2.7-cards-duplicate", "cards.json (M3-c208 absent); M3-c101, M3-c205", "PASS",
    "M3-c208 is absent (ids end at c207). c101 (orthogonal matrix definition) and c205 (Q^T Q = I implies Q Q^T = I) are different claims.")
row("cards-sample-lesson-text-current", "2.7-cards-current-text", "L07.html, L08.html, L09.html, project.html, cards.json",
    "PASS", "Changed hunks read this round: L07.html line 437; L08.html lines 6, 36, 137, 141, 414-416; L09.html lines 52, 597; "
    "project.html lines 117, 199, 231, 245, 246, 475, 615; cards.json M3-c127 and M3-c167 (and M3-c163 unchanged). Cards citing these "
    "agree with the current text.")

# ---- structure and links ----
row("links-and-anchors", "2.9-links", "course/modules/M/M3/project.html", "PASS", f"{SC}out/links_r10.out (same script as project-links).")

# ---- assemble ----
mutants = []
for line in (ROOT / OUT / "mutate_M3_seeds0-9_r10.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^KILLED (\S+?): (.*) -> (.*)$", line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2).strip(), "killed_by": m.group(3).strip()})
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
fragment = {
    "unit": "M3",
    "slice": "d",
    "round": 10,
    "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, round 10; shares no context with the builders",
    "pin": "47a36d8c78633793ccc762ae19dcd5e19b780d19",
    "base": "round-9 pin 1e272e5a (fragment /Users/billyribeiro/.fanout/frags/D-M3-d.round9.json, read as context; its PASS rows "
            "were not trusted). Delta 1e272e5..47a36d8 for this slice: project.html (lines 117, 199, 231, 245, 246, 475, 615), "
            "cards.json (M3-c127, M3-c167), L07.html line 437, L08.html lines 6, 36, 137, 141, 414-416, L09.html lines 52, 597, "
            "tests/labs/M3/lab-M3-project-1.py and -2.py (comment lines), curriculum/01-foundations.yaml line 175 (concept name), "
            "four new mutants in ledgers/M3/mutants/. grader/ (all four files), alternatives/, equivalent/README.md, retired/ and "
            "the L01-L06 pages are byte-identical to the round-9 pin.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD10-M3-d",
    "scratch": SC,
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "\\iota (boldsymbol iota, all-ones vector) is not registered in notation/notation.json; project.html defines it at its first use "
        "(weights bullet, line 247). Request registration or confirm the local definition (plans/M3-open-items.md).",
    ],
    "freshness_flags": [
        "Not checked this round: 2025-2026 work on nearest correlation matrices and alternating projections (no literature search "
        "was run; the only live check was verify_refs on the two M3 keys).",
    ],
    "notes": [
        "Round 10 FAILs: (1) scope-repair-weights-vs-brief (carried from round 9; the brief's weights comparison is not delivered and "
        "Lab 3's matrix has no computable repaired weights); (2) mutants-r15d-description (new: two mutant files' first docstring "
        "line is the reference header, not an error description).",
        "Round-9 FAIL spec-stop-rule-sentence is fixed at 47a36d8c (line 246) and re-verified PASS.",
        "Observation, not a row: the grader's is_psd asserts compare with 'is True' and 'is False'. A NumPy is_psd returning numpy.bool_ "
        "fails 14 tests (probe in scripts/M3-d-r10/probes). The starter annotates -> bool, so this is a return-type deviation; the builder "
        "may wish to test truthiness instead.",
        "Four new student-error mutants (v10d_01..v10d_04) written from reference.py with asserted single-match edits; all killed on "
        "seeds 0-9. Full mutation run: 168/168 killed.",
        "Ten alternatives plus one SVD-based alternative (probe) pass seeds 0-9 (163 passed each). Seeds 0-49 for the alternatives were not "
        "re-run this round.",
        "Equivalent mutant alt10 re-checked bit for bit (10000 trials, 0 differing) under the README's stated conditions.",
        "Grader instances: seeds 0-19 checked against the contract with NumPy; all valid and all answers distinct.",
        "Not checked: a browser run of the autograder (Pyodide) beyond page_smoke; a screenshot at 360 px (the project page has no figure); "
        "a live browser run of Rung 2's instant check; the Lesson 1-6 bodies beyond the cards that cite them (not in this slice's scope).",
        "The repository's ledgers/M3/M3-d.json in this checkout held an older round-18 fragment (pin 8f80909); it has been overwritten by "
        "this round-10 fragment as the task requires.",
    ],
    "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"],
                "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"])},
}
(ROOT / "ledgers/M3/M3-d.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants), "verdict", verdict)
