"""Round-7 verifier (slice d): writes ledgers/M3/M3-d.json from the fresh r7 outputs. Carried rows name the round-6
fragment and the paths whose bytes are unchanged between the round-6 pin 142ecfc and the pin 9373ef3 (git diff empty)."""

import json
import re
from pathlib import Path

ROOT = Path.cwd()
S = "ledgers/M3/scripts/M3-d-r7"
OUT = f"{S}/out"
PIN = "9373ef398589097500ea849e30ff9da423b98943"
C6 = "Carried from round 6 (byte-identical since the previous pin 142ecfc; git diff 142ecfc 9373ef3 empty for {}): {}"
F_LESSONS = "course/modules/M/M3/L01-L07.html, L09.html, tests/labs/M3 (except lab-M3-project-3.py)"
F_GRADER_NOCHANGE = "course/modules/M/M3/grader/test_project.py (cited lines), grader/instance.py"


def carry(files: str, note: str) -> str:
    return C6.format(files, note)


rows: list[dict] = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates (fresh at 9373ef3)
row("gate-check-pages", "gate-check_pages", "course/modules/M/M3/*", "PASS",
    f"{OUT}/check_pages_M3.out: 'check_pages M3: PASS', exit 0 (tools/check_pages.py --unit M3, run fresh).")
row("gate-check-dag", "gate-check_dag", "course/modules/M/M3/*", "PASS",
    f"{OUT}/check_dag_M3.out: 'check_dag M3: PASS', exit 0.")
row("gate-check-projects", "gate-check_projects", "course/modules/M/M3/project.html", "PASS",
    f"{OUT}/check_projects_M3.out: 'check_projects M3: PASS', exit 0.")
row("gate-run-labs", "gate-run_labs", "tests/labs/M3/*.py; project.html", "PASS",
    f"{OUT}/run_labs_M3.out: 'run_labs M3: PASS (12/12)', exit 0 (includes lab-M3-project-1..3).")
row("gate-run-graders", "gate-run_graders", "course/modules/M/M3/grader/", "PASS",
    f"{OUT}/run_graders_M3_0-49.out: 'run_graders M3: PASS (reference 50/50 seeds, slowest 0.6 s)', exit 0.")
row("gate-page-smoke", "gate-page_smoke", "course/modules/M/M3/project.html:246", "FAIL",
    f"{OUT}/page_smoke_project.out (run as 'page_smoke.py --unit M3 --pages project'; the stem is 'project', an earlier "
    "run with 'project.html' matched no page and passed vacuously): FAIL 'horizontal scroll of 149 px at 360 px wide' in "
    "light mobile and dark mobile; zero other failures. Cause, measured: ledgers/M3/scripts/M3-d-r7/overflow_r7.py lists "
    "the widest element at 360 px, the inline <code>test_projection_repair_runs_exactly_max_iter_steps</code> (448 px wide, "
    "unbreakable) in the 'Alternating steps' bullet at project.html line 246; overflow_cause_r7.py shows scrollWidth 509 "
    "before and 360 after 'code{overflow-wrap:anywhere}' is injected. The sentence was added in commit 9373ef3 (142ecfc had "
    "no such identifier).",
    "project.html line 246: make the identifier breakable at a point that fits a 360 px column (for example insert <wbr> "
    "inside it, as exemplar B does at line 615 for test_projection_repair_is_no_farther<wbr>_than_clipping), or refer to the "
    "test in words; then re-run 'page_smoke.py --unit M3 --pages project' and require PASS in both themes at 360 px. "
    "(Breakpoint not tested by me; the CSS-injection test shows that breaking the identifier removes the overflow.)")
row("gate-ruff", "gate-ruff", "tests/labs/M3; course/modules/M/M3/grader", "PASS",
    f"{OUT}/ruff_check.out: 'All checks passed!' and '16 files already formatted', exit 0 for both.")
row("gate-mypy", "gate-mypy", "repository", "PASS",
    f"{OUT}/mypy.out: 'Success: no issues found in 385 source files', exit 0 (mypy --no-incremental).")
row("gate-verify-refs", "gate-verify_refs", "references/references.json", "PASS",
    f"{OUT}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'. Live Crossref run not performed.")
row("gate-collect-only", "gate-collect-only", "course/modules/M/M3/grader/test_project.py; project.html:237", "PASS",
    f"{OUT}/collect_only_M3.out: '163 tests collected'; project.html line 237 states '163 tests'.")
row("gate-pytest-relevant", "gate-pytest", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, "
    "test_memo_exemplars.py, test_docs_figures.py, test_refs.py", "PASS",
    f"{OUT}/pytest_relevant_r7.out: all tests pass, exit 0 (pytest -q, six modules).")
row("gate-mutate-m3", "gate-mutate_graders", "ledgers/M3/mutants/ (156 files)", "PASS",
    f"{OUT}/mutate_M3_seeds0-9_r7.out: 'mutate_graders M3: PASS (156/156 killed)', exit 0, seeds 0-9. Includes the three "
    "round-7 mutants r7d_m01..m03 (killed by test_projection_repair_is_no_farther_than_clipping, "
    "test_clip_repair_is_positive_semidefinite, test_min_eigenvalue_matches_planted_spectrum).")
row("gate-reference-starter", "gate-reference-starter", "grader/reference.py; grader/starter.py", "PASS",
    f"{S}/stage_grader_r7.sh -> {OUT}/collect_only_M3.out ('163 tests collected'), {OUT}/reference_seed0_r7.out ('163 passed'), "
    f"{OUT}/starter_seed0_r7.out ('162 failed, 1 passed'; the failures are NotImplementedError from the starter's stubs).")
row("gate-alternatives-seeds-0-49", "gate-alternatives", "ledgers/M3/alternatives/alt1..alt9; "
    "ledgers/M3/scripts/M3-d-r5/equivalent/alt10, alt11", "PASS",
    f"{OUT}/alts_seeds0-49_r7.out: all 11 candidates PASS on seeds 0-49 (163 passed each), exit 0; "
    f"{OUT}/alts_seeds0-9_r7.out also PASS. Runner: {S}/run_alts_r7.py.")

# ---- grader
row("grader-instance", "2.6-grader-instance", "course/modules/M/M3/grader/instance.py; project.html lines 231-233", "PASS",
    f"{S}/instance_sample_r7.py -> {OUT}/instance_sample_r7.out: seeds 0-19 satisfy k in {{3,4,5}}, vols in [0.05,0.40], "
    "unit-diagonal symmetric corr with smallest eigenvalue below -0.02, positive definite psd_corr, orthonormal "
    "eigenvectors (error below 3e-12), and 20 distinct answer triples of 20.")
row("grader-test-count-and-purity", "2.6-grader", "grader/test_project.py lines 793-830; project.html line 237",
    "PASS", carry("grader/test_project.py lines 793-830", "163 tests; purity and printing tests; the cited lines are unchanged") +
    f"; fresh: collect {OUT}/collect_only_M3.out = 163.")
row("grader-standard-library-only", "2.6-grader", "grader/test_project.py lines 833-848; project.html line 235",
    "PASS", carry("grader/test_project.py lines 833-848", "imports restricted to standard library and NumPy"))
row("grader-lab3-reference-numbers", "2.6-grader", "grader/test_project.py lines 502-542; project.html Lab 3 expected block",
    "PASS", carry("grader/test_project.py lines 502-542", "Lab 3 numbers at tolerances 1e-6/1e-5") +
    f"; fresh: numpy re-derivation {S}/out/numpy_rederive_r7.out reproduces 0.176573, 0.175003, 0.001570, 0.011516, "
    "-0.2616 and weights 1.778929, -1.096718, -0.255613, 0.573402.")
row("grader-failure-messages-leak-answers", "2.6-grader", "grader/test_project.py lines 247-265, 328-329, 396-398, "
    "409-410, 547-552, 582-584", "PASS", carry("grader/test_project.py (cited lines)",
    "failure messages name the property and print no expected value; the cited lines are unchanged"))
row("grader-named-conditions", "2.6-grader", "grader/test_project.py lines 158-229, 751-783; project.html line 248",
    "PASS", carry("grader/test_project.py (cited lines)",
    "ValueError asserted only for the four named conditions; the cited lines are unchanged"))
row("grader-browser-timeout", "2.6-grader", "project.html line 235; course/assets/js/python.js line 4", "PASS",
    carry("project.html line 235; python.js", "the browser limit statement; fresh: in-browser grader ran in 1.1 s "
    f"({OUT}/page_smoke_project.out)"))
row("grader-reference-docstring", "2.6-grader", "grader/reference.py lines 1-5, 74", "PASS",
    "Changed in 9373ef3 and re-read: the module docstring ('the projection repair is computed by alternating projections, "
    "with correction terms') and _psd_projection's docstring ('Negative eigenvalues set to zero, then the matrix rebuilt "
    "from its eigenvectors; no rescaling') match the code at lines 74-77.")
row("grader-spec-rubric-counts", "2.9-structure", "project.html lines 237, 489-499", "PASS",
    f"Fresh: collect {OUT}/collect_only_M3.out = 163; rubric table rows data-criterion C1..C5 each with four level cells.")
row("spec-projection-tol-undefined", "2.6-spec", "project.html lines 233-246; grader/starter.py lines 31-35", "PASS",
    "Re-read at 9373ef3 (line 246 changed): tol is the stopping tolerance defined in the Alternating-steps bullet; the "
    "stopping rule is stated as an implementation choice; test_projection_repair_runs_exactly_max_iter_steps exists in "
    "grader/test_project.py (parametrized steps 1-3, tol=0) and matches the sentence; starter.py docstring agrees.")

# ---- mutants
mut_out = (ROOT / OUT / "mutate_M3_seeds0-9_r7.out").read_text(encoding="utf-8").splitlines()
killed_lines = [l for l in mut_out if l.startswith("KILLED ")]
row("mutants-v3d-01-max-iter-plus-one", "2.6-mutation", "ledgers/M3/mutants/v3d_01_projection_repair_runs_one_extra_step.py",
    "PASS", f"{OUT}/mutate_M3_seeds0-9_r7.out: KILLED (fresh run).")
row("mutants-v4d-01-clip-skips-rescale", "2.6-mutation", "ledgers/M3/mutants/v4d_01_clip_repair_skips_rescale_when_nearly_unit_diagonal.py",
    "PASS", f"{OUT}/mutate_M3_seeds0-9_r7.out: KILLED (fresh run).")
row("mutants-existing-140", "2.6-mutation", "ledgers/M3/mutants/ (all files)", "PASS",
    f"Fresh: {OUT}/mutate_M3_seeds0-9_r7.out lists {len(killed_lines)} KILLED and 0 SURVIVED over 156 files.")
row("mutants-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/v4d_02..v4d_04", "PASS",
    f"Fresh: KILLED in {OUT}/mutate_M3_seeds0-9_r7.out.")
row("mutants-v2d-01-05", "2.6-mutation", "ledgers/M3/mutants/v2d_01..v2d_05", "PASS",
    f"Fresh: KILLED in {OUT}/mutate_M3_seeds0-9_r7.out.")
row("mutants-v2d-06", "2.6-mutation", "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py", "PASS",
    carry("ledgers/M3/retired/", "retired mutant, not in the mutant set; it is a numpy-import mutant killed by "
          "test_module_imports_only_standard_library_or_numpy"))
row("mutants-v3d-02-05", "2.6-mutation", "ledgers/M3/mutants/v3d_02..v3d_05", "PASS",
    f"Fresh: KILLED in {OUT}/mutate_M3_seeds0-9_r7.out.")
row("mutants-v5d-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/v5d_02, v5d_03, v5d_05, v5d_06", "PASS",
    f"Fresh: KILLED in {OUT}/mutate_M3_seeds0-9_r7.out.")
row("mutants-r6-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/r6d_m02..r6d_m04", "PASS",
    f"Fresh: KILLED in {OUT}/mutate_M3_seeds0-9_r7.out.")
row("mutants-r7-new-student-errors", "2.6-mutation", "ledgers/M3/mutants/r7d_m01_projection_correction_uses_new_iterate.py; "
    "r7d_m02_clip_floors_the_diagonal_not_the_eigenvalues.py; r7d_m03_min_eigenvalue_bisection_ten_steps.py", "PASS",
    f"Written by {S}/make_mutants_r7.py (each replacement asserted once). Killed fresh: r7d_m01 by "
    "test_projection_repair_is_no_farther_than_clipping (seed 0); r7d_m02 by test_clip_repair_is_positive_semidefinite (seed 0); "
    f"r7d_m03 by test_min_eigenvalue_matches_planted_spectrum (seed 0); see {OUT}/mutate_M3_seeds0-9_r7.out.")
row("mutants-v5d-01-equivalent-moved", "2.6-equivalent", "ledgers/M3/scripts/M3-d-r5/equivalent/alt10_equivalent_no_unit_diagonal_correction.py "
    "(was v5d_01)", "FAIL",
    "Architect ruling 9 requires equivalent mutants in ledgers/M3/equivalent/ with a README proof. The file sits in a scripts "
    "folder, has no README, and is not in ledgers/M3/equivalent/. It passes seeds 0-49 (gate-alternatives-seeds-0-49).",
    "Move it to ledgers/M3/equivalent/ together with its proof (see equivalent-readme-citation), or classify it as an "
    "alternative in ledgers/M3/alternatives/ and drop it from the equivalent list.")
row("mutants-v5d-04-accepted-stop-rule", "2.6-alternative", "ledgers/M3/scripts/M3-d-r5/equivalent/alt11_stop_when_either_gap_or_change.py "
    "(was v5d_04)", "PASS",
    f"Correct alternative: PASS seeds 0-49 in {OUT}/alts_seeds0-49_r7.out; project.html line 246 says the stopping rule is an "
    "implementation choice. Its location is covered by equivalent-readme-citation.")
row("equivalent-r6d-m04", "2.6-alternative", "ledgers/M3/alternatives/alt7_dykstra_gap_only_stop.py", "PASS",
    f"PASS seeds 0-49 in {OUT}/alts_seeds0-49_r7.out. The stopping rule is an implementation choice (project.html line 246).")
row("equivalent-r11d-m02", "2.6-alternative", "ledgers/M3/alternatives/alt8_dykstra_step_only_stop.py", "PASS",
    f"PASS seeds 0-49 in {OUT}/alts_seeds0-49_r7.out.")
row("equivalent-r15d-m03-label", "2.6-alternative", "ledgers/M3/alternatives/alt9_dykstra_runs_full_budget.py", "PASS",
    f"PASS seeds 0-49 in {OUT}/alts_seeds0-49_r7.out.")
row("equivalent-readme-citation", "2.6-equivalent", "ledgers/M3/equivalent/ (absent); ledgers/M3/scripts/M3-d-r5/equivalent/",
    "FAIL",
    "ls ledgers/M3 at 9373ef3: alternatives, mutants, retired, scripts and the M3-*.json fragments only. No ledgers/M3/equivalent/ "
    "folder and no README exists. The round-6 PASS on this row recorded that absence as a pass, which the ruling does not allow. "
    "The two candidates (alt10, alt11) live under scripts/M3-d-r5/equivalent/ without proofs in a README.",
    "Create ledgers/M3/equivalent/README.md with each equivalence proof (the argument, plus an exhaustive or randomized check) "
    "and move the equivalent candidates there; or record them as accepted alternatives in ledgers/M3/alternatives/ and state "
    "that no equivalent mutant exists for M3.")

# ---- project page
row("project-numbers", "2.2-numbers", "project.html lines 57, 138, 143, 221, 460-472, 575-619", "PASS",
    f"Fresh: twin stdout equals the expected blocks (run_labs gate); {S}/out/numpy_rederive_r7.out re-derives every Lab 3 "
    "number and the exemplar B numbers (0.176573 - 0.175003 = 0.001570; weights sum; A3 closed form max difference 1.1e-16).")
row("project-lab1-memo-sentence", "2.5-labs", "project.html lines 53-57, 138; tests/labs/M3/lab-M3-project-1.py", "PASS",
    carry("project.html lines 53-57, 138; lab-M3-project-1.py",
          "Lab 1 twin exit 0 under -I -W error, stdout equals expected block, page code equals twin") +
    f"; fresh: {S}/out/project_labs_check_r7.out (page code == twin True, 8 lines match).")
row("project-lab2-completion", "2.5-labs", "project.html lines 141-222; tests/labs/M3/lab-M3-project-2.py", "PASS",
    f"Fresh: {S}/out/project_labs_check_r7.out and a diff of the page code against the twin: the only differences are the "
    "two blanks, which are filled with 'smallest >= -1e-10' and 'math.sqrt(d[i] * d[j])'; the twin's stdout equals the expected block.")
row("project-lab3-check", "2.5-labs", "project.html lines 287-470; tests/labs/M3/lab-M3-project-3.py", "PASS",
    f"Fresh: {S}/out/project_labs_check_r7.out: page code == twin, twin exit 0 under -I -W error, 11 lines match the expected block.")
row("project-lab3-diagonal-positivity-sentence", "2.9-prose", "project.html Lab 3 interpretation (line 473)", "PASS",
    "Re-derived from the twin: clip_repair divides by math.sqrt(d[i] * d[j]) for every (i, j), including i = j; a negative "
    "product raises ValueError and a zero product raises ZeroDivisionError, so a completed run shows every product is positive, "
    "and A1 gives nonnegative d[i]. The sentence matches.")
row("project-spec-grader", "2.9-prose", "project.html lines 229-237", "PASS",
    carry("project.html lines 229-237", "context and grading-mode sentences; 163 tests, the four named ValueError conditions"))
row("project-conventions-math", "2.4-math", "project.html lines 242-249; grader/reference.py _psd_projection and projection_repair",
    "PASS", "Re-read at 9373ef3 (lines 244, 246 changed). reference.py projection_repair: y = P(x + corr_s); corr_s = x + corr_s - y; "
    "new_x = y + corr_u with diagonal 1; corr_u = y + corr_u - new_x; gap = ||new_x - y||_F; change = ||new_x - x||_F. This is the "
    "page's update. The Frobenius and clipping bullets match reference.py and the test suite; the stopping-rule sentence matches "
    "test_projection_repair_runs_exactly_max_iter_steps (tol=0, steps 1-3).")
row("project-conventions-link", "2.9-structure", "project.html line 243; L05.html#def-positive-semidefinite-matrix", "PASS",
    f"check_dag and check_pages for M3 PASS at 9373ef3 ({OUT}/check_dag_M3.out, {OUT}/check_pages_M3.out); the anchor is in L05, "
    "unchanged since 142ecfc.")
for a, text in (("A1", "X = V Lambda_f V^T is symmetric and z^T X z = sum max(lambda_i, f) (V^T z)_i^2 >= 0 for f >= 0; the "
                 "spectral theorem (Theorem 2.3 of Lesson 4, cited as holding under F1 to F4, which Lesson 4 defines in section 1) "
                 "is the only external step"),
                ("A2", "Y_ii = X_ii / (sqrt(d_i))^2 = 1 and z^T Y z = q^T X q with q = D^{-1/2} z >= 0; positive d_i is named"),
                ("A3", "det Sigma = a^2 b^2 (1 - rho^2) > 0; Sigma^{-1} iota = (b(b - rho a), a(a - rho b)) / det; the sum of "
                 "components is a^2 + b^2 - 2 rho a b = (a - b)^2 + 2ab(1 - rho) > 0; scaling by c^2 cancels"),
                ("A4", "X u_i = V Lambda_0 e_i = 0 for lambda_i < 0; z = D_X^{1/2} u_i gives Y z = 0; S_v^{-1} z gives Sigma S_v^{-1} z = 0")):
    row(f"project-proof-{a}", "2.4-math", f"project.html appendix {a}", "PASS",
        carry(f"project.html appendix {a} (line ~636-638)", "proof read and re-derived: " + text))
row("project-hours", "2.9-hours", "project.html lines 252-268; course/modules/M/M3/index.html line 29; lesson data-hours", "PASS",
    "Project rows 2+3+14+8+12+6 = 45 = data-hours-project. Lesson data-hours L01..L09 = 12+11+12+12+12+11+11+12+12 = 105 = "
    "data-hours-lessons (index.html line 29). 105 + 45 = 150 = curriculum hours (curriculum/01-foundations.yaml, M3 hours: 150). "
    "My own estimate of the components (ladder 5 h, engine 10-14 h, weights 6-10 h, report and four proofs 10-15 h, "
    "self-check 4-6 h) totals 35-50 h, inside the 30 % band.")
row("project-exemplars", "2.3-rubric", "project.html lines 502-647", "PASS",
    "Blind scoring by me from the rubric alone, then compared: exemplar A 2,2,2,1,2 (official 2,2,2,1,2); exemplar B 4,4,4,3,3 "
    "(official 4,4,4,3,3). Exemplar A's numbers (1.78, -1.10, -0.26, 0.57 sum 0.99) and exemplar B's printed values (0.176573, "
    "0.175003, 0.001570, 0.011516, 0.000000, -0.142113) match Lab 3's output. The official B annotation that B lacks an explicit "
    "'no market claim is made' statement is correct (B says what a market claim would require).")
row("project-rubric", "2.3-rubric", "project.html lines 486-500", "PASS",
    carry("project.html lines 486-500", "C1..C5 each with four observable level cells; the C2 level 3 cell (line 499) unchanged"))
row("rubric-C4-level2-vague", "2.3-rubric", "project.html line 501 (C4 row)", "PASS",
    carry("project.html line 501", "C4 level 2 is observable ('Labels some inputs, or states a conclusion about a portfolio or a market')"))
row("project-references", "2.9-structure", "project.html lines 665-677; references/references.json", "PASS",
    carry("project.html lines 665-677", "Axler 2024 and Strang 2023 are verified, used_by M3") +
    "; fresh: references/references.json has axler2024linear (2024, Springer, DOI 10.1007/978-3-031-41026-0) and "
    "strang2023introduction (2023, Wellesley-Cambridge), both status verified; verify_refs offline PASS.")
row("project-no-process-words", "2.9-prose", "project.html; cards.json; grader/*.py; tests/labs/M3/lab-M3-project-*.py", "PASS",
    f"{S}/static_checks_r7.py -> {OUT}/static_checks_r7.out: no process word in project.html, cards.json or the labs; the only hits "
    "are the Python built-in round( in grader/instance.py code.")
row("project-stretch", "2.9-prose", "project.html lines 656-663", "PASS",
    carry("project.html lines 656-663", "three stretch items; none claims a result"))
row("scope-repair-weights-vs-brief", "2.6-scope", "curriculum/01-foundations.yaml:185-186 (brief); project.html lines 244, 473, 499, 615",
    "FAIL",
    "Brief (curriculum/01-foundations.yaml 185-186): 'Compare the effect of each repair on downstream portfolio weights.' Plan 4 "
    "(M3-build-plan.md line 220) requires weights for each repair. The page (line 473 and exemplar B) gives weights only for the "
    "input; the clipped matrix has no weights by A4, and the projection has none because its printed smallest eigenvalue is zero "
    "to six decimals. Re-derived: min eigenvalue of the clipped matrix X before rescaling is -7.5e-17 and its diagonal is positive "
    "(1.056, 1.046, 1.000014, 1.040), so A4 applies to every non-PSD input with positive diagonal, not only to Lab 3's matrix. "
    f"Evidence: {S}/out/numpy_rederive_r7.out. The architect decision B3 (closed form with no concept name) therefore cannot "
    "satisfy the brief for the clipped repair at floor 0.",
    "Architect decision required, not a builder edit: either (a) accept in writing that the closed-form weights cannot be "
    "compared for repairs at floor 0 (and keep the page's disclosure), or (b) change the device, for example clip at a floor "
    "f > 0 (which makes the clipped matrix positive definite, so the formula applies) or a stated pseudo-inverse rule, and then "
    "the builder prints weights for each repair and the rubric C2 is rewritten. The page cannot be made to meet the brief "
    "under the current B3 ruling.")
row("notation-registry", "2.9-notation", "project.html math; notation/notation.json", "PASS",
    "Fresh: math symbols on project.html (Sigma, rho, Lambda, iota, V, X, Y, D, S, C, J, E, N, H, P(M), Z, a, b, c, f, d_i, q, z, "
    f"{S}/static_checks_r7.py -> {OUT}/static_checks_r7.out: the single letters are ABCDEFHJMNPSVXYZ and abcdefikmquvwz; "
    "no registered symbol (T, Q, R_f, Phi, gamma_3) is used on the page. Local letters (N, S, m) are defined on the page "
    "(notation.json 'about': conventionally local letters are defined where used).")
row("notation-R-macro", "2.9-notation", "project.html; L07.html; L08.html; L09.html; cards.json", "PASS",
    f"{OUT}/static_checks_r7.out: \\mathbb count 0 in project.html, L07, L08, L09 and cards.json. (L04.html has 3 and L06.html 1, "
    "all \\mathbb{C}; outside this slice; \\mathbb{C} is not a registered macro, reported for the L04/L06 slice.)")
row("dag-linked-concepts", "2.9-dag", "project.html concept links: eigendecomposition (L03), spectral-theorem (L04), "
    "positive-semidefinite-matrix (L05)", "PASS",
    f"check_dag M3 PASS ({OUT}/check_dag_M3.out); all three linked concepts are defined in M3 lessons L03-L05 (inside the closure).")
row("dag-m4-concepts-by-name", "2.9-dag", "project.html; cards.json; L01-L09", "PASS",
    f"{S}/static_checks_r7.py -> {OUT}/static_checks_r7.out: 0 matches for cholesky, ieee, minimum variance, mean variance, "
    "quadratic programming, equal weight in project.html, cards.json and all nine lesson pages.")

# ---- cards
row("cards-structure", "2.7-cards", "course/modules/M/M3/cards.json (203 cards)", "PASS",
    f"Fresh: {S}/static_checks_r7.py -> {OUT}/static_checks_r7.out: 203 cards, 203 unique ids, no duplicate fronts or backs. "
    "Compared with 142ecfc (202 cards): c144 and c163 edited, c208 added; no card removed.")
row("cards-id-sequence", "2.7-cards", "course/modules/M/M3/cards.json ids", "PASS",
    "Ids unique. Gaps c102, c148, c191, c204 and the out-of-order appended c207 and c208 are not defects (architect ruling 2). "
    "No page or card refers to a card id.")
row("cards-numbers-cited", "2.7-cards", "cards.json (back and front numbers, references)", "PASS",
    f"Fresh: {S}/card_refs_r7.py -> {OUT}/card_refs_r7.out: 201 'Kind N.M' references and 267 numbers checked against the named "
    "lesson text (extracted from L0n.html): 0 misses. Cross-lesson references (c054: Lesson 1 Proposition 3.12; c076, c077, "
    "c090: Lesson 4 Theorem 2.3) were checked by hand against L01 and L04 text.")
row("cards-labels-cited", "2.7-cards", "cards.json grade and basis fields", "PASS",
    f"Fresh: {S}/static_checks_r7.py -> {OUT}/static_checks_r7.out: 117 T, 39 C, 47 with no grade; no C card without a Lab "
    "in its basis; no non-C card carries a basis.")
row("cards-duplicate-scan", "2.7-cards", "cards.json (all pairs)", "PASS",
    f"Fresh: {S}/cards_overlap_r7.py -> {OUT}/cards_overlap_r7.out: 81 pairs at Jaccard >= 0.40 read; each high pair asks a "
    "different fact (for example c135 k=1 against c186 k>=2; c136 against c201; c194 symmetry against c195 idempotence). The one "
    "semantic duplicate, c208 against c101 and c205, is a FAIL row (cards-c208-duplicate).")
row("cards-sample-10", "2.7-cards", "cards.json (all 203 cards)", "PASS",
    "Every card was read in full at 9373ef3. Per-id comparison with 142ecfc: only c144, c163 and c208 differ (c163 front and c144 "
    "back changed, c208 added); all other 199 cards are byte-identical and carried by the lesson rows.")
row("cards-lab-numbers", "2.7-cards", "cards.json grade-C cards; tests/labs/M3/lab-M3-L05-1.py, lab-M3-L09-1.py", "PASS",
    carry("cards.json grade-C cards except c163; lab twins", "lab outputs named in the basis fields match the lesson's printed "
          "output") + "; c163 re-checked fresh (see cards-c163-lab-count).")
row("cards-L01", "2.7-cards", "cards.json L01 cards (24); L01.html; lab-M3-L01-1.py", "PASS",
    carry("L01.html, its lab and cards", "24 cards: definitions, propositions, misconceptions and lab counts re-read"))
row("cards-L02", "2.7-cards", "cards.json L02 cards (22); L02.html", "PASS",
    carry("L02.html, its lab and cards", "22 cards re-read"))
row("cards-L03", "2.7-cards", "cards.json L03 cards (23); L03.html", "PASS",
    carry("L03.html, its lab and cards", "23 cards re-read"))
row("cards-L04", "2.7-cards", "cards.json L04 cards (19); L04.html", "PASS",
    carry("L04.html and its cards", "19 cards re-read; the F1-F4 assumptions are defined in L04 section 1"))
row("cards-L05", "2.7-cards", "cards.json L05 cards; L05.html", "PASS",
    carry("L05.html, lab-M3-L05-1.py and cards", "cards re-read"))
row("cards-L06", "2.7-cards", "cards.json L06 cards (15); L06.html lines 24-25 (Definition 1.1)", "PASS",
    carry("L06.html and its cards", "M3-c101 matches L06 Definition 1.1 (orthogonal matrix)"))
row("cards-L07", "2.7-cards", "cards.json L07 cards (20); L07.html", "PASS",
    carry("L07.html and its cards", "20 cards re-read"))
row("cards-L08", "2.7-cards", "cards.json L08 cards (c130-c145, c174, c186, c197-c201, c207); L08.html (changed in 9373ef3)",
    "PASS",
    f"Fresh at 9373ef3 against the current L08 text ({OUT}/text/L08.txt from extract_lesson_text_r7.py): Proposition 1.1, 1.2; Definition 1.3 "
    "(shares defined when the eigenvalue sum is positive); Theorem 1.4 (table row now states 'whenever the eigenvalue sum is "
    "positive', matching c200); Theorem 2.1(a),(b) (c135, c186); Corollary 2.2 (c136, c201); Proposition 2.3 (table row states "
    "'positive eigenvalue sum', matching c137 and c144); Remark 2.4 (c138); Definition 3.1 (c142, c207); Lab 1 outputs (c140 "
    "cosines 0.9994/0.9985/0.9990 by level/slope/curvature; c141 0.7587 to 0.9791; c174 75.9/18.1/5.2). All consistent.")
row("cards-L09", "2.7-cards", "cards.json L09 cards (c146-c185, c202); L09.html (unchanged since 142ecfc)", "PASS",
    carry("L09.html and cards M3-c146..c162, c164..c185, c202 (c163 and c208 handled separately)", "the L09 cards re-read; the "
          "lesson's lab counts 23, 23 of 23, 0.175527 and 0.163280 match the L09 lab output"))
row("cards-L01-L09-changed-in-round3", "2.7-cards", "cards.json M3-c101, c127, c142, c168, c178, c202, c205", "PASS",
    carry("cards.json entries c101, c127, c142, c168, c178, c202, c205", "byte-identical per id; c101 re-read against L06 Definition 1.1"))
row("cards-c131", "2.7-cards", "cards.json M3-c131; L08.html Proposition 1.1", "PASS",
    carry("cards.json M3-c131; L08 Proposition 1.1 text", "re-checked against the L08 text: M symmetric and x^T M x = ||X~x||^2/(T-1) >= 0"))
row("cards-c204", "2.7-cards", "cards.json (M3-c204 removed at 142ecfc)", "PASS",
    "M3-c204 is absent (per-id comparison: removed earlier, not in 9373ef3); no card restates M3-c101 except the c208 case "
    "recorded in cards-c208-duplicate.")
row("cards-c144-prop23-hypothesis", "2.7-cards", "cards.json M3-c144 back; course/modules/M/M3/L08.html Proposition 2.3",
    "PASS",
    "Re-read at 9373ef3 (the back changed): 'False. Under F1 to F4 of Lesson 4, M is quadratic in X, so doubling X multiplies M and "
    "each eigenvalue by 4. Whenever the shares are defined (the eigenvalue sum is positive), they are unchanged (Proposition 2.3 "
    "with c = 2).' L08 Proposition 2.3 states the positive-sum hypothesis; the round-6 defect is fixed.")
row("cards-c163-lab-count", "2.7-cards", "cards.json M3-c163 front (changed in 9373ef3); L09.html; lab-M3-L09-1.py output",
    "PASS",
    "New front: 'in how many of the 23 seeded 5 x 5 matrices with a smallest eigenvalue below -1e-9 does the alternating-projection "
    "output pass the correlation check and come out strictly closer to A than the clip-and-rescale matrix?' Answer 23 of 23: the "
    "L09 lab prints 'alternating-projection output passes is_correlation and is strictly closer to A than R: 23 of 23' (L09 "
    "expected output, line 223). The back's caveat (no nearest matrix is shown) matches L09 line 109.")
row("cards-c208-duplicate", "2.7-cards", "cards.json M3-c208 (new in 9373ef3, lesson L09); cards M3-c101 and M3-c205",
    "FAIL",
    "M3-c208 asks 'which two matrix equations make Q orthogonal, in the sense of Definition 1.2a' and answers Q^T Q = I and "
    "Q Q^T = I. The same definition is M3-c101 (L06 Definition 1.1: orthogonal matrix as Q^T Q = I, the columns orthonormal), and "
    "the fact that Q^T Q = I implies Q Q^T = I is M3-c205. Token Jaccard against c101 is 0.38 (below the 0.40 scan threshold), "
    f"but the fact asked is the same ({OUT}/static_checks_r7.out: Jaccard 0.38 against c101, 0.21 against c205). The concept is also defined twice in the course: L06 Definition 1.1 and L09 "
    "Definition 1.2a 'orthogonal matrix' (L09 text, Definition 1.2a).",
    "Delete M3-c208 (its content is covered by c101 and c205). Separately, the L09 builder should remove the second definition "
    "of orthogonal matrix (Definition 1.2a) or cite L06 Definition 1.1 instead; I did not edit it.")
row("cards-sample-lesson-text-current", "2.9-structure", "course/modules/M/M3/L08.html; L09.html; project.html", "PASS",
    f"Current lesson text matches the cards that cite it (see cards-L08, cards-c144, cards-c163-lab-count); "
    f"{OUT}/card_refs_r7.out: 0 misses.")

# ---- structure and carried others

fragment = {
    "unit": "M3",
    "slice": "d",
    "round": 7,
    "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, round 7; shares no context with the builders",
    "pin": PIN,
    "base": "round-6 pin 142ecfc (fragment /Users/billyribeiro/.fanout/frags/D-M3-d.round6.json, read as context). Delta "
            "142ecfc..9373ef3 for this slice: project.html (lines 244, 246, 338, 473), grader/reference.py, grader/starter.py, "
            "grader/test_project.py (docstrings at 480-497, 638-667), L08.html (lines 95, 428, 432), lab-M3-project-3.py (line 51), "
            "cards.json (c144 back, c163 front, c208 added). L01-L07, L09 and the other labs byte-identical.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD7-M3-d",
    "scratch": f"{S}/ (scripts, out/); ws /private/tmp/verifyD7-M3-d-ws-r7",
    "verified_at": "2026-11-04T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Pre-existing files in ledgers/M3/scripts/M3-d-r7/ (committed in ce7b3821, earlier batch work) were not used or relied on; my scripts and outputs are named distinctly.",
        "The 360 px horizontal scroll (gate-page-smoke) is a regression introduced by 9373ef3 at project.html line 246. Round 6 did not measure it (its page_smoke PASS was at 142ecfc).",
        "Mutants: 156 files; each KILLED on seeds 0-9 in the fresh run; r7d_m01..m03 are new student-error mutants written by me.",
        "Alternatives: alt1-alt9 plus alt10, alt11 pass seeds 0-49 (fresh). Ruling 10 asks for five; the page's seed window for M3 is 0-49.",
        "Not checked: live Crossref (verify_refs online); the 120 s browser limit beyond the in-browser run of 1.1 s; each of the 153 pre-existing mutants read line by line (checked by the gate and killers); lesson text of L01-L07 and L09 re-read only where a card cites it (carried, byte-identical); the L04/L06 use of \\mathbb{C} (other slice).",
        "No commit or push made.",
    ],
    "summary": "",
}

mut_entries = []
for line in killed_lines:
    body = line[len("KILLED "):]
    name, rest = body.split(": ", 1)
    desc, test = rest.rsplit(" -> ", 1)
    killed_by = test.strip()
    mut_entries.append({"id": name, "description": desc, "killed_by": killed_by})
fragment["mutants"] = mut_entries

n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
n_unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
fragment["summary"] = (f"M3 slice d round 7 on pin 9373ef3: verdict FAIL. Rows: {len(rows)}; PASS {n_pass}; FAIL {n_fail}; "
                       f"UNVERIFIABLE {n_unv}. Non-PASS rows: gate-page-smoke (360 px horizontal scroll, project.html line 246, "
                       "regression from 9373ef3); scope-repair-weights-vs-brief (architect decision B3 cannot meet the brief); "
                       "cards-c208-duplicate (restates the orthogonal-matrix definition of c101/c205); equivalent-readme-citation "
                       "(no ledgers/M3/equivalent/ README); mutants-v5d-01-equivalent-moved (same location). Mutants: "
                       f"{len(mut_entries)} of {len(mut_entries)} killed on seeds 0-9, including three new round-7 mutants. "
                       "Gates re-run fresh at 9373ef3: check_pages, check_dag, check_projects, run_labs 12/12, run_graders 50/50, "
                       "page_smoke project FAIL (scroll), ruff, mypy, verify_refs offline, collect-only 163, pytest relevant, "
                       "mutate 156/156, alternatives seeds 0-49 all PASS.")

problems = []
for r in rows:
    if r["status"] not in ("PASS", "FAIL", "UNVERIFIABLE"):
        problems.append(r["id"])
    if r["status"] != "PASS" and not r.get("fix"):
        problems.append("nofix " + r["id"])
ids = [r["id"] for r in rows]
dups = sorted({i for i in ids if ids.count(i) > 1})
print("rows", len(rows), "PASS", n_pass, "FAIL", n_fail, "dups", dups, "problems", problems)
(ROOT / "ledgers/M3/M3-d.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote ledgers/M3/M3-d.json")
