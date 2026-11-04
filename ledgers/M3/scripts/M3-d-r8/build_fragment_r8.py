"""Round-8 verifier (M3 slice d): writes ledgers/M3/M3-d.json from the outputs in ledgers/M3/scripts/M3-d-r8/out/.

The mutant list is parsed from out/mutate_M3_seeds0-9_r8.out (the gate output), so each mutant's description and the
test that killed it are the gate's own. Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r8/build_fragment_r8.py
"""

import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "ledgers/M3/scripts/M3-d-r8/out"
S = "ledgers/M3/scripts/M3-d-r8"

mutants = []
for line in (OUT / "mutate_M3_seeds0-9_r8.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    if status != "KILLED":
        raise SystemExit(f"survivor: {name}")
    mutants.append({"id": name, "description": desc.strip(), "killed_by": killed.strip()})
assert len(mutants) == 160, len(mutants)

R = []


def row(id_, check, location, status, evidence, fix=""):
    R.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


GATE = "ledgers/M3/scripts/M3-d-r8/out/"
row("gate-check-pages", "gate-check_pages", "course/modules/M/M3/*", "PASS",
    GATE + "check_pages_M3.out: 'check_pages M3: PASS', exit 0 (tools/check_pages.py --unit M3, run fresh at 2d75559).")
row("gate-check-dag", "gate-check_dag", "course/modules/M/M3/*", "PASS",
    GATE + "check_dag_M3.out: 'check_dag M3: PASS', exit 0.")
row("gate-check-projects", "gate-check_projects", "course/modules/M/M3/project.html", "PASS",
    GATE + "check_projects_M3.out: 'check_projects M3: PASS', exit 0.")
row("gate-run-labs", "gate-run_labs", "tests/labs/M3/*.py; project.html", "PASS",
    GATE + "run_labs_M3.out: 'run_labs M3: PASS (12/12)', exit 0 (includes lab-M3-project-1..3).")
row("gate-run-graders", "gate-run_graders", "course/modules/M/M3/grader/", "PASS",
    GATE + "run_graders_M3_0-49.out: 'run_graders M3: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0.")
row("gate-page-smoke", "gate-page_smoke", "course/modules/M/M3/project.html:246", "PASS",
    GATE + "page_smoke_project.out ('page_smoke.py --unit M3 --pages project'): 'page_smoke modules/M/M3/project.html: PASS', "
    "in-browser grader 'All 163 tests pass'; no horizontal scroll at 360 px. The round-7 scroll (149 px, identifier at line 246) "
    "is fixed: line 246 now breaks the identifier with <wbr>. Only the line-246 identifier changed since round 7.")
row("gate-ruff", "gate-ruff", "tests/labs/M3; course/modules/M/M3/grader", "PASS",
    GATE + "ruff_check.out: 'All checks passed!' and '16 files already formatted', exit 0 for both.")
row("gate-mypy", "gate-mypy", "repository", "PASS",
    GATE + "mypy.out: 'Success: no issues found in 385 source files' (mypy --no-incremental), exit 0.")
row("gate-verify-refs", "gate-verify_refs", "references/references.json", "PASS",
    GATE + "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'. Live Crossref run not performed (no network check requested).")
row("gate-collect-only", "gate-collect-only", "course/modules/M/M3/grader/test_project.py; project.html:237", "PASS",
    GATE + "collect_only_M3.out: '163 tests collected' (staged copy, reference.py as covariance_doctor.py); project.html line 237 states '163 tests'.")
row("gate-pytest-relevant", "gate-pytest", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_memo_exemplars.py, test_page_smoke.py", "PASS",
    GATE + "pytest_relevant_r8.out: all pass, exit 0 (pytest -q, five modules).")
row("gate-mutate-m3", "gate-mutate_graders", "ledgers/M3/mutants/ (160 files)", "PASS",
    GATE + "mutate_M3_seeds0-9_r8.out: 'mutate_graders M3: PASS (160/160 killed)', exit 0, seeds 0-9. Each killer and description is in the mutants array.")
row("gate-reference-starter", "gate-reference-starter", "grader/reference.py; grader/starter.py", "PASS",
    GATE + "reference_seed0_r8.out: '163 passed' (QF_SEED=0, --assert=plain -W error, staged); starter_seed0_r8.out: '162 failed, 1 passed' (an empty implementation fails the suite).")
row("gate-alternatives-seeds-0-49", "gate-alternatives", "ledgers/M3/alternatives/alt1..alt10", "PASS",
    GATE + "alts_seeds0-49_r8.out: all ten alternatives PASS, 'failing []' on seeds 0-49 (163 passed on the last seed of each). Covers the six-alternative seeds 0-9 request and ruling 10.")
row("grader-instance", "2.6-grader-instance", "course/modules/M/M3/grader/instance.py; project.html lines 231-233", "PASS",
    GATE + "instance_check_r8.out (instance_check_r8.py): seeds 0-49: k in {3,4,5}; vols in [0.05,0.40]; corr symmetric, unit diagonal, off-diagonal in [-0.95,0.95], smallest eigenvalue below -0.02; psd_corr positive definite unit diagonal; psd_spectrum[0]=0; eigenvectors orthonormal. No problems. 50 distinct min-eigenvalues and 50 distinct weight vectors across seeds 0-49, so the answers change, not only the labels. Matches project.html line 231 and the instance.py docstring.")
row("grader-test-count-and-purity", "2.6-grader", "grader/test_project.py (purity tests); project.html line 237", "PASS",
    GATE + "collect_only_M3.out = 163 = page count; test_functions_print_nothing, test_inputs_are_not_mutated and test_repeated_calls_agree pass on the reference (reference_seed0_r8.out).")
row("grader-standard-library-only", "2.6-grader", "grader/test_project.py lines 833-848; project.html line 235", "PASS",
    "test_module_imports_only_standard_library_or_numpy passes on reference.py (reference_seed0_r8.out). Reference imports only math, collections.abc; page line 235 says 'standard library and NumPy only'.")
row("grader-lab3-reference-numbers", "2.6-grader", "grader/test_project.py lines 502-542; project.html Lab 3 expected block", "PASS",
    "test_lab3_reference_numbers_are_matched passes on reference.py. Independent re-derivation with numpy (" + S + "/numpy_rederive_r8.py, out/numpy_rederive_r8.out): smallest eigenvalue -0.142113; clip distance 0.176573; projection distance 0.175003; gap 0.001570; max entry difference 0.011516; weights 1.778929, -1.096718, -0.255613, 0.573402.")
row("grader-failure-messages-leak-answers", "2.6-grader", "grader/test_project.py (every assert and pytest.fail message)", "PASS",
    "Read every message in test_project.py (lines 1-869, this round). Messages name the property or the rule and the shape or condition; none prints an expected numeric value or the expected verdict's value.")
row("grader-named-conditions", "2.6-grader", "grader/test_project.py lines 176-210, 694-783; project.html line 248", "PASS",
    "ValueError is asserted only for: non-square input (lines 176-179, 694-701), asymmetry beyond 1e-9 (184-189, 706-710, 743-746), volatility not strictly positive incl. NaN (751-757), length mismatch (778-783). Tests at exactly 1e-9 and within 1e-10 assert no exception. reference.py also raises ValueError for an empty matrix (line 22) and a non-positive diagonal in rescaling (line 82); no test asserts either, and the page does not name them (allowed by project.html line 235).")
row("grader-browser-timeout", "2.6-grader", "project.html line 235; course/assets/js/python.js", "PASS",
    "page_smoke in-browser grader run: 1.2 s (page_smoke_project.out), against the page's 120 s limit.")
row("grader-reference-docstring", "2.6-grader", "grader/reference.py lines 1-5, 109-110", "PASS",
    "Docstring 'alternating projections, with correction terms' matches the code: the update at lines 116-128 carries corr_s (live) and corr_u (inert, see equivalent-alt10 row).")
row("grader-spec-rubric-counts", "2.9-structure", "project.html lines 237, 494-503", "PASS",
    "Rubric table has rows data-criterion C1..C5, each with four level cells (project.html lines 498-502); collect-only 163 equals page count.")
row("spec-projection-tol-undefined", "2.6-spec", "project.html lines 233, 246; grader/starter.py lines 31-35", "PASS",
    "tol is defined in the Alternating-steps bullet (line 246) as the stopping tolerance; the stopping rule is stated as an implementation choice, and starter.py says the same.")
row("grader-projection-spec-vs-reference", "2.4-math", "grader/reference.py lines 109-128; project.html line 246", "PASS",
    "Numpy re-implementation of the page's update (numpy_rederive_r8.py, function projection) run 500 steps with tol 1e-10 agrees with a 5000-step no-stop run to 1.4e-11 on the Lab 3 matrix, and gives the printed projection distance 0.175003 (numpy_rederive_r8.out), matching the reference's expected block.")
row("grader-weights-spec-vs-reference", "2.4-math", "grader/reference.py lines 131-150; project.html line 247", "PASS",
    "comparison_weights solves Sigma x = 1 with Sigma = S C S and normalises (reference.py line 148-150), the closed form of project.html line 247; test_weights_two_asset_closed_form and test_weights_solve_sigma_times_weights_proportional_to_ones pass on the reference.")
row("mutants-existing-140", "2.6-mutation", "ledgers/M3/mutants/ (all 156 pre-existing and round-7 files)", "PASS",
    "mutate_M3_seeds0-9_r8.out: every listed mutant KILLED (160 with the four new ones). The id is historical; the count is 160 this round.")
row("mutants-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/v4d_02..v4d_04", "PASS",
    "Killed in mutate_M3_seeds0-9_r8.out (see mutants array).")
row("mutants-v2d-01-05", "2.6-mutation", "ledgers/M3/mutants/v2d_01..v2d_05", "PASS",
    "Killed in mutate_M3_seeds0-9_r8.out (see mutants array).")
row("mutants-v2d-06", "2.6-mutation", "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py", "PASS",
    "Retired (not in ledgers/M3/mutants/); outside the gate. git diff --name-only 9373ef3 2d755599 -- ledgers/M3/retired is empty (0 files).")
row("mutants-v3d-02-05", "2.6-mutation", "ledgers/M3/mutants/v3d_02..v3d_05", "PASS",
    "Killed in mutate_M3_seeds0-9_r8.out (see mutants array).")
row("mutants-v5d-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/v5d_02, v5d_03, v5d_05, v5d_06", "PASS",
    "Killed in mutate_M3_seeds0-9_r8.out (see mutants array).")
row("mutants-r6-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/r6d_m02..r6d_m04", "PASS",
    "Killed in mutate_M3_seeds0-9_r8.out (see mutants array).")
row("mutants-r7-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/r7d_m01..r7d_m03", "PASS",
    "Killed in mutate_M3_seeds0-9_r8.out (see mutants array).")
row("mutants-v8d-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/v8d_01..v8d_04; ledgers/M3/scripts/M3-d-r8/make_mutants_r8.py", "PASS",
    "Four new student-error mutants written this round, each reference.py with one edit (script asserts each edit matches once): v8d_01 is_psd tolerance scaled by the largest eigenvalue (killed by test_is_psd_tolerance_is_not_scaled_by_the_diagonal); v8d_02 weights ignore the correlation entries (killed by test_lab3_reference_numbers_are_matched); v8d_03 projection refuses a one-by-one matrix with an unnamed ValueError (killed by test_projection_repair_one_by_one_is_one); v8d_04 unit diagonal pinned only after the last step (killed by test_projection_repair_is_a_valid_repair). All killed on seed 0.")
row("mutants-v5d-01-equivalent-moved", "2.6-equivalent", "ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py", "PASS",
    "Moved into ledgers/M3/equivalent/ with its proof in README.md (round-7 FAIL resolved). Bitwise check: " + S + "/equiv_alt10_r8.py, out/equiv_alt10_r8.out: 20000 trials (sizes 2-6, max_iter in {1,2,3,5,500}, tol in {0, 1e-10}), outputs differing 0 by == and by repr. The proof (README steps 1-5) is checked: H off-diagonal stays exactly 0.0, the diagonal of H is overwritten, and the gap, change and output do not read H's diagonal.")
row("mutants-v5d-04-accepted-stop-rule", "2.6-alternative", "ledgers/M3/alternatives/alt10_stop_when_either_gap_or_change.py", "PASS",
    "Stops when either gap or change is at most tol; PASS seeds 0-49 (gate-alternatives row). Not equivalent (it can stop one step earlier), so it stays an alternative.")
row("equivalent-r6d-m04", "2.6-alternative", "ledgers/M3/alternatives/alt7_dykstra_gap_only_stop.py", "PASS",
    "PASS on seeds 0-49 (alts_seeds0-49_r8.out); the stopping rule is an implementation choice (project.html line 246).")
row("equivalent-r11d-m02", "2.6-alternative", "ledgers/M3/alternatives/alt8_dykstra_step_only_stop.py", "PASS",
    "PASS on seeds 0-49 (alts_seeds0-49_r8.out).")
row("equivalent-r15d-m03-label", "2.6-alternative", "ledgers/M3/alternatives/alt9_dykstra_runs_full_budget.py", "PASS",
    "PASS on seeds 0-49 (alts_seeds0-49_r8.out).")
row("equivalent-readme-citation", "2.6-equivalent", "ledgers/M3/equivalent/README.md", "PASS",
    "README.md exists and gives the proof for alt10_no_unit_diagonal_correction.py (steps 1-5), the check, and the consequence for the page. The bitwise check above confirms the claim on 20000 inputs; the proof covers every input.")
row("project-numbers", "2.2-numbers", "project.html lines 57, 138, 143, 221, 290, 460-475, 581, 603, 615, 619, 628", "PASS",
    "numpy_rederive_r8.out re-derives every printed Lab 1-3 number (eigenvalues, rebuilt and repaired entries for Labs 1 and 2; Lab 3 distances, gap 0.001570 (0.001570181549 unrounded), entry gap 0.011516, diagonal deviations, determinant -0.261600, weights, and the smallest eigenvalues). project_labs_r8.out: each twin's stdout equals the expected block. Interpretive numbers (page lines 138, 221, 475, 581, 603, 615) match these outputs.")
row("project-lab1-memo-sentence", "2.5-labs", "project.html lines 57, 138; tests/labs/M3/lab-M3-project-1.py", "PASS",
    "Hypothesis (line 57): smallest eigenvalue negative, verdict False, diagonal 1 to six decimals, repaired check True: output shows False, rebuilt diagonal 1.096064 1.104409 1.074824, repaired check True. Interpretation (line 138) numbers match. Page code equals twin (project_labs_r8.out).")
row("project-lab2-completion", "2.5-labs", "project.html lines 141-222; tests/labs/M3/lab-M3-project-2.py", "PASS",
    "project_labs_r8.out: the page code differs from the twin only in the two blanks (twin line 50 and line 58; ruling 11 lets the twin be the completed solution); the twin runs under python -I -W error with exit 0 and its stdout equals the expected block. Blank 1 is smallest >= -1e-10 and blank 2 is math.sqrt(d[i]*d[j]), as line 221 says.")
row("project-lab3-check", "2.5-labs", "project.html lines 287-476; tests/labs/M3/lab-M3-project-3.py", "PASS",
    "project_labs_r8.out: page code equals twin (0 differing lines), twin exit 0 under -I -W error, stdout equals the 11-line expected block. Hypothesis (line 290) claims all hold in the output: input not PSD (False), projection nearer by a positive distance, both repairs unit-diagonal to 5e-7, determinant nonzero, input weights sum 1, both smallest eigenvalues zero to six decimals.")
row("project-lab3-diagonal-positivity-sentence", "2.9-prose", "project.html line 475 (and exemplar B, line 603, 615)", "PASS",
    "Argument re-derived: the rescaling math.sqrt(d[i]*d[j]) raises ValueError for a negative product and ZeroDivisionError for zero, so a completed run gives every d[i]*d[j] > 0 (including i = j), hence each d[i] is nonzero with one sign; A1 gives d[i] >= 0; so d[i] > 0. Numerically (numpy_rederive_r8.out): clipped X diagonal 1.056280, 1.045743, 1.000014, 1.040076, all positive; X smallest eigenvalue -7.5e-17.")
row("project-spec-grader", "2.9-prose", "project.html lines 229-237", "PASS",
    "Context, inputs and grading statements match grader/instance.py and test_project.py: k 3-5, 0.02 margin, planted spectra, 163 tests, the listed test families (checked by the test names and collect-only).")
row("project-conventions-math", "2.4-math", "project.html lines 242-249; grader/reference.py", "PASS",
    "Conventions match reference.py and the numerics: unit-diagonal and PSD definitions; Frobenius distance; clipping formula; alternating update (numpy re-run, see grader-projection row); weights formula; the four ValueError conditions (line 248) match the tests.")
row("project-conventions-link", "2.9-structure", "project.html line 243; course/modules/M/M3/L05.html", "PASS",
    "L05 anchor def-positive-semidefinite-matrix exists (check_dag M3 PASS; lesson 5 defines PSD by the quadratic form, which line 243 says).")
row("project-proof-A1", "2.4-math", "project.html appendix A1 (line 641)", "PASS",
    "Re-derived: X = V Lambda_f V^T is symmetric and z^T X z = sum max(lambda_i, f) (V^T z)_i^2 >= 0 since f >= 0. The spectral theorem cited is Theorem 2.3 of Lesson 4 (L04.html line 130), which holds under F1-F4 (L04.html lines 59-62).")
row("project-proof-A2", "2.4-math", "project.html appendix A2 (line 642)", "PASS",
    "Re-derived: Y_ii = X_ii / d_i = 1; z^T Y z = q^T X q >= 0 with q = D^{-1/2} z. The positivity of d_i is named as needed for the division.")
row("project-proof-A3", "2.4-math", "project.html appendix A3 (line 643)", "PASS",
    "Re-derived: det Sigma = a^2 b^2 (1 - rho^2) > 0; Sigma^{-1} iota = (b(b - rho a), a(a - rho b)) / det; the normalising sum a^2 + b^2 - 2 rho a b = (a-b)^2 + 2ab(1-rho) > 0; scaling by c > 0 multiplies all components and the sum by c^2. test_weights_two_asset_closed_form agrees on the reference.")
row("project-proof-A4", "2.4-math", "project.html appendix A4 (line 643)", "PASS",
    "Re-derived: X u_i = V Lambda_0 e_i = 0 (singular). With D_X positive, z = D_X^{1/2} u_i gives Y z = 0; with S_v positive, S_v^{-1} z gives Sigma S_v^{-1} z = S_v Y z = 0. Numerically the clipped X has smallest eigenvalue -7.5e-17 (numpy_rederive_r8.out).")
row("project-hours", "2.9-hours", "project.html lines 259-265; course/modules/M/M3/index.html", "PASS",
    "Table rows 2+3+14+8+12+6 = 45 = data-hours-project (line 33). Independent central estimate: rung 1 about 1.5 h, rung 2 about 2 h, engine (four functions, input checks, Jacobi and projection, 163-test suite) 10-14 h, weights 3-5 h, report with four proofs 10-14 h, self-check 3-5 h; central total about 35 h, 22% below 45 h, inside the 30% band. Hub hours checked by check_pages PASS.")
row("project-exemplars", "2.3-rubric", "project.html lines 507-652", "PASS",
    "Blind scoring from the rubric alone: Exemplar A C1 2, C2 2, C3 2, C4 1, C5 2 (official 2,2,2,1,2); Exemplar B C1 4, C2 4, C3 4, C4 3, C5 3 (official 4,4,4,3,3). Every criterion within one level, and annotations match.")
row("project-rubric", "2.3-rubric", "project.html lines 486-503", "PASS",
    "C1..C5 each have four observable level cells. Scoring rule (line 490) is written as 'any attempt', which is a rule, not a level descriptor; no level descriptor is vague (checked each cell).")
row("rubric-C4-level2-vague", "2.3-rubric", "project.html line 501 (C4 row)", "PASS",
    "C4 level 2 'Labels some inputs, or states a conclusion about a portfolio or a market from a printed result' is checkable: a reader can see whether any input is unlabelled or any portfolio or market conclusion is drawn.")
row("project-references", "2.9-structure", "project.html lines 670-681; references/references.json", "PASS",
    "Keys axler2024linear (verified, crossref) and strang2023introduction (verified, openlibrary) exist and are used_by M3 (references.json). Page line 672 attributes no statement to either source; verify_refs offline PASS.")
row("project-no-process-words", "2.9-prose", "project.html; cards.json; grader/*.py; tests/labs/M3/lab-M3-project-*.py", "PASS",
    "Static scan this round (misc_checks_r8.py; out/misc_checks_r8.out: 'banned/process-word hits: none' over project.html, cards.json, the grader and the project labs). The '...' and the ellipsis in cards.json are list notation (v1, ..., vk), not omitted content.")
row("project-stretch", "2.9-prose", "project.html lines 661-668", "PASS",
    "Three open tasks, each with a stated method; none claims a result. Read this round.")
row("project-links", "2.9-structure", "project.html (23 href values)", "PASS",
    "Every relative file link resolves (grader/starter.py, grader/test_project.py, grader/instance.py, index.html, L09.html, ../../../review.html, ../../../index.html) and every #anchor exists in project.html or the target page (misc_checks_r8.py; out/misc_checks_r8.out: 'links: 23 href values; problems: none').")
row("scope-repair-weights-vs-brief", "2.6-scope", "curriculum/01-foundations.yaml:185-187 (brief); project.html lines 475, 499, 615",
    "FAIL",
    "Brief: 'Compare the effect of each repair on downstream portfolio weights.' The page prints weights only for the input (line 472 / 475), and says the clipped matrix and the projection get no weights (lines 475, 615; rubric C2 at line 499). Re-derived: clip repair at floor 0 has smallest eigenvalue -8.1e-17 before rescaling and a positive diagonal, so A4 makes its Sigma singular (numpy_rederive_r8.out: 'lab3 X (clip before rescale) min eig -7.500049254979e-17 ... all positive True'); the projection's smallest eigenvalue is -2.5e-11 (numpy_rederive_r8.out), so its Sigma is numerically singular. The closed form therefore cannot compare the effect of the clipped repair on the weights, and the page states that it does not compare them. Architect decision B3 (closed form, plan line 130 and architect decision) has not been changed since round 7.",
    "Architect decision required, not a builder edit: (a) record in writing that the closed-form weights cannot be compared for a floor-0 clipped repair, and amend the brief through a curriculum change request; or (b) change the device so each repair has invertible Sigma (for example clip at a floor f > 0, which makes the clipped matrix positive definite, so the formula applies), or define a stated pseudo-inverse rule for singular Sigma, and then print the weights for each repair and rewrite rubric C2. The page must not ship while the brief's comparison is unmet.")
row("notation-registry", "2.9-notation", "project.html math; notation/notation.json", "PASS",
    "Symbols used on project.html (Sigma, rho, Lambda, V, X, Y, D, S, C, J, E, N, H, P, Z, a, b, c, d, f, q, z, t, k, i, m, u, v, w, e, iota) are checked against the notation.json symbol list (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q): none reused with another meaning. Macros used: \\top, \\boldsymbol, \\iota, \\det, \\lVert, \\rVert, \\max, \\sum, \\sqrt, \\ge, \\ne, \\dots are standard KaTeX, not registry macros; \\diag is registered. NOTATION_REQUESTS for \\top and \\iota are already open (plans/M3-open-items.md).")
row("notation-R-macro", "2.9-notation", "project.html; L07.html; L08.html; L09.html; cards.json", "PASS",
    "No \\mathbb in these files (misc_checks_r8.out: '\\mathbb counts' 0 for project.html, cards.json, L07, L08, L09).")
row("dag-linked-concepts", "2.9-dag", "project.html concept links (eigendecomposition L03, spectral-theorem L04, positive-semidefinite-matrix L05)", "PASS",
    "check_dag M3 PASS; the three linked concepts are defined in M3 lessons L03-L05, inside the closure.")
row("dag-m4-concepts-by-name", "2.9-dag", "project.html; cards.json; L01-L09 (lesson text)", "PASS",
    "misc_checks_r8.out, 'other-module concept names' (cholesky, ieee, minimum variance, mean-variance, quadratic programming, shrinkage, equal weight, OLS, present value, discount factor, random variable, expectation) over project.html, cards.json, L01-L09, the grader and the project labs: the only hit is the grader's cholesky (4 occurrences, see its own row). correlation, covariance, variance, standard deviation and Gaussian appear as plain prose, as FINAL-ARCHITECT-RULINGS item 3 permits. The grader is scanned in its own row.")
row("dag-cholesky-named-in-grader", "2.9-dag", "course/modules/M/M3/grader/test_project.py lines 13, 56, 73, 270", "FAIL",
    "The M8 concept cholesky-decomposition is named by Cholesky in learner-visible grader docstrings (test_project.py lines 13, 56, 73, 270; the file is linked from project.html line 279 and is not secret per project.html line 237). The grader also uses Cholesky pivots as its independent positive-definiteness test (_is_pd, lines 55-69; min_eig, lines 72-84). plans/M3-build-plan.md B4 says M3's L05 and labs must not name Cholesky or use it as a PSD test, and the rule of DAG-by-name (VERIFIER_RULES 2.9 / rule 14) applies to other-unit concepts used by name. Scope caveat: B4 literally names L05 and the labs, not the grader, so this is a rule-14 reading; the round-7 static scan did not cover grader files, which is why it was missed.",
    "Remove the concept name from the grader: reword lines 13, 56, 73 and 270 (for example 'by Gaussian elimination with strictly positive pivots' or 'independent bisection check'), and keep the independent test unchanged in logic. If the architect rules that B4 does not reach the grader, record that ruling in plans/M3-open-items.md and close this row. Then re-run run_graders --unit M3 --seeds 0-49 and mutate_graders --unit M3 --seeds 0-9.")
row("cards-structure", "2.7-cards", "course/modules/M/M3/cards.json (202 cards)", "PASS",
    S + "/cards_static_r8.py -> out/cards_static_r8.out: 202 cards, 202 unique ids, every lesson exists, no cite field, grade-C cards have basis, grades 117 T / 39 C / 46 none; 0 problems.")
row("cards-id-sequence", "2.7-cards", "course/modules/M/M3/cards.json ids", "PASS",
    "Ids unique; gaps and out-of-order appended ids are not defects (FINAL-ARCHITECT-RULINGS item 2). No card or page refers to M3-c208 (misc_checks_r8.out: 'files mentioning M3-c208: none').")
row("cards-numbers-cited", "2.7-cards", "cards.json front and back numbers", "PASS",
    "cards_static_r8.py: every numeric token in every card appears in that card's own lesson text (0 problems).")
row("cards-labels-cited", "2.7-cards", "cards.json grade and basis fields", "PASS",
    "Every card whose text cites a Lab is grade C with a basis; every grade-C card cites a lab or SIMULATED basis (cards_static_r8.py and misc_checks_r8.py; out/misc_checks_r8.out: 'grade/lab consistency problems: none').")
row("cards-duplicate-scan", "2.7-cards", "cards.json (all 20301 pairs by token Jaccard)", "PASS",
    S + "/out/cards_static_r8.out: 112 pairs at Jaccard >= 0.40, every pair listed. Read in full (cards_sample_and_pairs_r8.py part 2; out/cards_sample_and_pairs_r8.out lists every pair with both fronts). No two cards ask the same fact; the highest pair (c025 kernel vs c187 image, 0.86) and the Lab 1 count pairs (c163 vs c175, c162 vs c163/c175) ask different questions. M3-c208 (orthogonal matrix restated) is removed, so the round-7 duplicate is resolved.")
row("cards-deleted-definition-1-2a", "2.7-cards", "cards.json; course/modules/M/M3/L0*.html; project.html; grader/", "PASS",
    "misc_checks_r8.out: '1.2a' in M3 pages/cards: none (every M3 html page and cards.json). The only card that cited it (M3-c208) was deleted in 2d75559, and L09 has no remaining reference.")
row("cards-sample-20", "2.7-cards", "cards.json (seeded sample of 20: random.Random(20261104))", "PASS",
    "Each sampled card read with its lesson anchor (cards_sample_and_pairs_r8.py; out/cards_sample_and_pairs_r8.out, part 1): M3-c193, c164, c054, c083, c095, c129, c154, c006, c059, c100, c002, c169, c140, c153, c161, c180, c019, c119, c097, c008. All agree with the cited lesson text or lab output (for example c164 distances 0.175527 and 0.163280 match L09 Lab 1 output; c140 cosines match L08 Lab 1; c153 matches L09 Definition 3.1).")
row("cards-lab-numbers", "2.7-cards", "cards.json grade-C cards; tests/labs/M3/lab-M3-L09-1.py, L08, L05 outputs", "PASS",
    "L09 Lab 1 cards checked this round against the L09 expected block: c161 (0.6400000000), c162 (23 of 40), c163 (23 of 23 closer), c164 (0.175527, 0.163280), c175 (23 of 23 passes). L08 cards c140, c141, c145, c174 agree with L08 text (scales 8, 4, 2 bp per day at L08.html line 146). L05 grade-C cards (c095, c096, c097, c173) are carried: L05.html and their cards are byte-identical since 9373ef3 (carry_identity_r8.out).")
row("cards-L01", "2.7-cards", "cards.json L01 cards; L01.html; lab-M3-L01-1.py",
    "PASS",
    "Carried from round 7 (byte-identical since the previous pin 9373ef3: carry_identity_r8.out shows L01.html and its lab unchanged; these card entries are not in the git diff): cards re-checked this round by the static checks (numbers, locators, duplicates) and by the seeded sample (c006, c008, c002, c019, c169).")
row("cards-L02", "2.7-cards", "cards.json L02 cards; L02.html", "PASS",
    "Carried from round 7 (L02.html byte-identical since 9373ef3; cards unchanged in the git diff). Static checks this round; the seeded sample has none from L02 but the high-similarity pair c025/c187 was read.")
row("cards-L03", "2.7-cards", "cards.json L03 cards; L03.html", "PASS",
    "Carried from round 7 (L03.html byte-identical since 9373ef3). Static checks and the seeded sample (c054, c059) this round.")
row("cards-L04", "2.7-cards", "cards.json L04 cards; L04.html", "PASS",
    "Carried from round 7 (L04.html byte-identical since 9373ef3). Static checks this round; c063 read against L04 Definition 1.1 (transpose, L04.html line 68).")
row("cards-L05", "2.7-cards", "cards.json L05 cards; L05.html", "PASS",
    "Carried from round 7 (L05.html byte-identical since 9373ef3). Static checks and seeded sample (c193, c100, c083) this round.")
row("cards-L06", "2.7-cards", "cards.json L06 cards; L06.html lines 56-59, 127", "PASS",
    "Carried from round 7 (L06.html byte-identical since 9373ef3). Re-read this round: c101 matches L06 Definition 1.1 (line 59); c205 cites Fact 1.2, which exists at L06.html line 64.")
row("cards-L07", "2.7-cards", "cards.json L07 cards (c115-c127, c168, c194-c196); L07.html (line 56 changed)", "PASS",
    "Re-checked this round against the current L07.html: the changed sentence (line 56, inner product and norm now cited from Lesson 6, subspace from Lesson 1) is consistent with L06.html line 56 and L01.html line 81; no L07 card quotes the removed wording. Cards c115-c129 (printed), c168, c194-c196 read; each locator (Theorem 1.2(a)-(c), Theorem 1.3, Remark 1.4, Theorem 2.2) exists in L07 by the static locator check.")
row("cards-L08", "2.7-cards", "cards.json L08 cards; L08.html (lines 36, 58, 137, 146)", "PASS",
    "Changed cards and their lesson re-read this round: c142 (Definition 3.1 now states the three-tenor assumption, matches L08.html line 137 and the Section 3 text), c207 (same), c145 (L08 Lab 1 scales 8, 4, 2 bp per day, L08.html line 146). Trace card c132 matches Proposition 1.2 (L08.html line 71: the trace is the total squared movement); the 'as in Lesson 6, Proposition 2.4' cross-reference is valid (L06.html line 127 defines the trace and the Frobenius norm). Card c144 back (Proposition 2.3 with c = 2) matches L08.html line 121.")
row("cards-L09", "2.7-cards", "cards.json L09 cards; L09.html (lines 56-70, 184, 189-205)", "PASS",
    "Changed or affected cards re-read this round against the current L09.html: c147 (Frobenius norm via Lesson 6, Proposition 2.4, matches the Definition 1.2 rewrite), c185 (Definition 1.2 Frobenius distance), c182 (Method 2 text, line 184: stop when the largest entrywise change is below 1e-12 or after 500 steps, unit diagonal by construction), c161 and c164 (lab output), c163 and c175 (lab output 23 of 23). The deleted Definition 1.2a is referenced by no card.")
row("cards-c131", "2.7-cards", "cards.json M3-c131; L08.html Proposition 1.1", "PASS",
    "M3-c131 (symmetric and PSD for X~^T X~/(T-1)) matches L08 Proposition 1.1; not a duplicate of c083 (general Gram matrix) because it is the specialisation the lesson proves.")
row("cards-c204", "2.7-cards", "cards.json", "PASS",
    "misc_checks_r8.out: 'M3-c204 present: False'; no card references it.")
row("cards-c144-prop23-hypothesis", "2.7-cards", "cards.json M3-c144; L08.html Proposition 2.3", "PASS",
    "M3-c144 unchanged in the 9373ef3..2d75559 diff (cards.json hunks are only c142, c147, c163, c207, c208); back read this round: 'doubling X multiplies M and each eigenvalue by 4 ... unchanged (Proposition 2.3 with c = 2)', which matches L08.html line 121 (c^2 scaling, shares unchanged when the eigenvalue sum is positive).")
row("cards-c163-lab-count", "2.7-cards", "cards.json M3-c163 (front changed); L09.html Lab 1 expected block", "PASS",
    "New front asks the count of the 23 non-PSD matrices whose alternating-projection output passes the check and is strictly closer than R; the Lab 1 output line reads '... passes is_correlation and is strictly closer to A than R: 23 of 23'. Back 'All 23' matches.")
row("cards-c208-duplicate", "2.7-cards", "cards.json (M3-c208 deleted in 2d75559); M3-c101 and M3-c205", "PASS",
    "M3-c208 is removed (misc_checks_r8.out: 'files mentioning M3-c208: none'). c101 (definition: Q^T Q = I) and c205 (consequence: Q Q^T = I) remain as distinct facts, so no duplicate of the orthogonal-matrix definition is left.")
row("cards-sample-lesson-text-current", "2.9-structure", "course/modules/M/M3/L08.html; L09.html; project.html; cards.json", "PASS",
    "Cards citing the changed lesson text (c142, c147, c163, c182, c207) and the page's cross-references match the current text this round (see cards-L08, cards-L09 rows).")
row("alternatives-count-and-seeds", "2.6-alternative", "ledgers/M3/alternatives/ (10 files)", "PASS",
    "All ten alternatives PASS seeds 0-49 (alts_seeds0-49_r8.out): alt1 numpy eigh, alt2 Dykstra with another stop rule, alt3 numpy solve and eigvalsh, alt4 Jacobi with other cutoffs, alt5 Cholesky bisection min, alt6 numpy linalg engine, alt7-alt10 other stopping rules. Ruling 10 requires five; ten are run. (alt5 names Cholesky in its own file; the alternative is a test artefact, not a learner page.)")
row("links-and-anchors", "2.9-structure", "course/modules/M/M3/project.html", "PASS",
    "Covered by project-links row.")
DATA = {
    "unit": "M3",
    "slice": "d",
    "round": 8,
    "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, round 8; shares no context with the builders",
    "pin": "2d755599d8d74df292e3e43025f0458c4053802e",
    "base": "round-7 pin 9373ef39 (fragment /Users/billyribeiro/.fanout/frags/D-M3-d.round7.json, read as context; its PASS rows were not trusted and every non-PASS row was re-verified). Delta 9373ef3..2d75559 for this slice: project.html line 246 (wbr and k->t), cards.json (c142, c147, c163, c207 changed; c208 removed), L07.html line 56, L08.html (lines 58, 137, 146), L09.html (Definition 1.2 rewritten, Definition 1.2a removed), ledgers/M3/equivalent/ (README and alt10), ledgers/M3/alternatives/alt10, ledgers/M3/mutants/r7d_m01..m03.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD8-M3-d",
    "scratch": S + "/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Ruling 9: the four v8d mutants are new student-error mutants; the 156 earlier mutants and the three r7d mutants are re-run unchanged. The 160 mutants are all KILLED on seeds 0-9.",
        "Ruling 10: ten alternatives run on seeds 0-49; the page's six-alternative request is met by any six of them.",
        "Round-7 FAIL rows status: gate-page-smoke (fixed, PASS now), cards-c208-duplicate (fixed, PASS), mutants-v5d-01-equivalent-moved and equivalent-readme-citation (fixed, PASS), scope-repair-weights-vs-brief (NOT fixed, still FAIL).",
        "New FAIL found this round: dag-cholesky-named-in-grader (grader docstrings name the M8 concept; scope caveat recorded in the row).",
        "Not checked live: verify_refs against Crossref (offline integrity only); the browser at 360 px in a screenshot (page_smoke geometry only); the grader runs in a real Pyodide session beyond page_smoke's in-browser run.",
        "Not re-read line by line this round: the lesson bodies L01-L07 and L09 outside the cited hunks (their cards and labs carried from round 7 by byte-identity, see the carried rows). The cards were all checked by script (structure, numbers, locators, duplicates) and by re-reading the changed, lab-linked and a seeded sample of 20.",
        "Pre-existing files in ledgers/M3/scripts/M3-d-r8/ (alts_run.py, make_fragment.py, cards_check.py, lab_p*.err and similar, from an earlier run) were not used or relied on; every script cited by a row this round is a *_r8 file written in this round.",
        "No commit or push made. No course, tool, test, reference, curriculum or atlas file edited; new files only under ledgers/M3/mutants/, ledgers/M3/scripts/M3-d-r8/ and this fragment.",
    ],
    "summary": "",
}
pass_n = sum(1 for r in R if r["status"] == "PASS")
fail_n = sum(1 for r in R if r["status"] == "FAIL")
DATA["summary"] = (
    f"M3 slice d round 8 on pin 2d75559: verdict FAIL. Rows {len(R)}: PASS {pass_n}, FAIL {fail_n}, UNVERIFIABLE 0. "
    "Non-PASS rows: scope-repair-weights-vs-brief (brief's weight comparison not met; architect decision needed) and "
    "dag-cholesky-named-in-grader (grader names an M8 concept; rule-14 reading). Gates fresh: check_pages, check_dag, check_projects, "
    "run_labs 12/12, run_graders 50/50, page_smoke project PASS (scroll fixed), ruff, mypy, verify_refs offline, collect-only 163, "
    "pytest relevant, mutate 160/160 (exit 0), ten alternatives PASS seeds 0-49, equivalent alt10 bitwise 20000 trials 0 differences."
)
Path(ROOT / "ledgers/M3/M3-d.json").write_text(json.dumps(DATA, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(R), "PASS", pass_n, "FAIL", fail_n, "mutants", len(mutants))
