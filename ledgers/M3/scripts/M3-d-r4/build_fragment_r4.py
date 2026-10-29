"""Build ledgers/M3/M3-d.json (round 4, slice M3-d) from the round-4 verifier run.

Mutant rows are parsed from the output of tools/mutate_graders.py --unit M3 --seeds 0-9 (saved as
ledgers/M3/scripts/M3-d-r4/mutate_final_r4.out). Row statuses are the verifier's findings, written here by hand.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
out_lines = (ROOT / "ledgers/M3/scripts/M3-d-r4/mutate_final_r4.out").read_text(encoding="utf-8").splitlines()
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?\.py): (.*) -> (.*)$")
mutants = []
for line in out_lines:
    m = pat.match(line)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    mutants.append({
        "id": fname[:-3],
        "description": desc,
        "killed_by": "" if killed.strip() == "None" else killed.strip(),
    })
mutants = sorted(mutants, key=lambda x: x["id"])

SURV_FIX = "Add the boundary test or the default-tolerance test named in the fix column of the row, then re-run."
R = []  # rows
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)

CARRY = "Carried from round 3 (course/modules/M/M3/grader/reference.py, grader/instance.py byte-identical since aa3c26c): "
row("d-r1-01-suite-count", "page test count equals collect-only count", "project.html line 237 (Grading mode); grader/test_project.py", "PASS",
    "Round 4: collect-only in the grader workspace built by tools/run_graders.py (reference copy) gives '142 tests collected'; page says 142. page_smoke --unit M3 --pages project: 'All 142 tests pass on seed 697963252'.")
row("d-r1-02-spec-named-refusals", "ValueError is asserted only for the four named conditions", "project.html Constraints (line 235), Conventions item 4 (line 247); grader/test_project.py must_raise call sites lines 124, 170, 180, 220, 572, 584, 620, 631, 647",
    "PASS", "Round 4: grep -n must_raise lists 9 hits (definition and 8 call sites): non-square (170, 572), asymmetry beyond 1e-9 (180, 220, 584, 620), volatility at or below zero (631), length mismatch (647). The new negative-floor and exact-tolerance tests (lines 369-398, 597-606) assert no exception.")
row("d-r1-03-tests-only-unit-diagonal", "unit-diagonal scope stated and the non-unit-diagonal tests exist as stated", "project.html Conventions 'Unit-diagonal matrix' (line 242); grader/test_project.py lines 238-239, 255",
    "PASS", "Round 4: line 242 names diag(3, -2, 5) for min_eigenvalue; test_project.py line 238 uses diag(3, -2, 5) and asserts -2 (line 239). The new clip tests (lines 369-398) use the unit-diagonal input [[1, 1.3], [1.3, 1]].")
row("d-r1-04-over-constraint-differs-from-clipping", "no test demands a result that differs from clipping by a rule the page does not state", "grader/test_project.py",
    "PASS", "Round 4: grep -c differs_from_clipping test_project.py = 0. Nine correct implementations (ledgers/M3/scripts/M3-d-r4/sweep_alts_r4.out.txt) pass 50 of 50 seeds each.")
row("d-r1-05-grader-reference-seeds", "reference passes seeds 0-49", "course/modules/M/M3/grader/reference.py; tools/run_graders.py --unit M3 --seeds 0-49",
    "PASS", "Round 4: 'run_graders M3: PASS (reference 50/50 seeds, slowest 0.2 s)'.")
row("d-r1-06-instances-valid-and-varied", "instances are valid and varied", "course/modules/M/M3/grader/instance.py",
    "PASS", CARRY + "git diff aa3c26c 2657ab5 -- grader/instance.py is empty. Round-3 evidence: k in {3,4,5} and 20 distinct smallest eigenvalues for seeds 0-19.")
row("d-r1-07-mutants-existing", "every pre-existing mutant is killed", "ledgers/M3/mutants (38 pre-existing and the round-3 additions)",
    "PASS", "Round 4: tools/mutate_graders.py --unit M3 --seeds 0-9 (ledgers/M3/scripts/M3-d-r4/mutate_final_r4.out): all pre-existing mutants KILLED. Survivors are only rows d-r3-32, d-r4-40, d-r4-39.")
row("d-r1-08-mutants-verifier", "verifier mutants v01-v04 are killed", "ledgers/M3/mutants/v01-v04",
    "PASS", "Round 4 output: v01 KILLED by test_clip_repair_has_unit_diagonal_and_is_symmetric[seed]; v02 by test_weights_refuse_length_mismatch[longer]; v03 by test_projection_repair_is_a_valid_repair[seed]; v04 by test_asymmetry_beyond_tolerance_is_refused[1-2--1.0-is_psd].")
row("d-r1-09-alternatives", "correct alternative implementations pass", "ledgers/M3/alternatives/alt1-alt6; ledgers/M3/scripts/M3-d-r4/alternatives/*.py",
    "PASS", "Round 4 sweep against the current grader, seeds 0-49, 142 tests each: alt1..alt6 and alt_r3a/b/c all 0 failing seeds of 50 (sweep_alts_r4.out.txt).")
row("d-r1-10-lab1-output", "Lab 1 runs and matches the page block", "project.html Lab 1 (lines 55-139); tests/labs/M3/lab-M3-project-1.py",
    "PASS", "Round 4: python -I -W error lab-M3-project-1.py exit 0; output identical to the page block (8 lines; twin1.out vs page pre block 1).")
row("d-r1-11-lab2-output", "Lab 2 runs and matches the page block", "project.html Lab 2 (lines 141-222); tests/labs/M3/lab-M3-project-2.py",
    "PASS", "Round 4: exit 0; output identical to the page block (8 lines; twin2.out vs page pre block 3).")
row("d-r1-12-lab3-output-and-numbers", "Lab 3 output, interpretation sentences and printed numbers", "project.html Lab 3 (lines 287-469, interpretation line 469); tests/labs/M3/lab-M3-project-3.py",
    "PASS", "Round 4: exit 0; output identical to the page block (9 lines; twin3.out vs page pre block 6). Recomputed with NumPy (ledgers/M3/scripts/M3-d-r3/lab3_recompute.py): distances 0.17657323 and 0.17500304, gap 0.00157018 (printed 0.001570), max entry difference 0.01151642 (0.011516), det -0.2616, weights 1.77892919 -1.09671848 -0.25561313 0.57340242 (sum 1). Every sentence of the revised interpretation checked: no projection weights are printed; the clipped matrix min eigenvalue is -7.5e-17 and its diagonal (1.05628, 1.04574, 1.00001, 1.04008) is positive, so A4 applies.")
row("d-r1-13-lab3-max-entry-gap", "max entry gap value", "project.html Lab 3 output line 'largest entry difference'",
    "PASS", "Round 4 recomputation: 0.011516416659581585; printed 0.011516 (twin3.out).")
row("d-r1-14-lab3-smallest-eig", "smallest eigenvalue of the Lab 3 matrix", "project.html Lab 3 output and Exemplar B summary",
    "PASS", "Round 4: eigvalsh minimum -0.14211264; printed -0.142113 (twin3.out line 1; Exemplar B summary).")
row("d-r1-15-proofs-A1-A3", "appendix proofs A1-A4 are complete with their hypotheses", "project.html Appendix A (lines 635-637)",
    "PASS", "Round 4 re-derivation: A1 (z'Xz = sum max(lambda_i,f)(V'z)_i^2 >= 0); A2 (Y_ii = 1, z'Yz = w'Xw >= 0; the removed 'only when' clause no longer appears); A3 (det = a^2b^2(1-rho^2) > 0; numerator b(b-rho a), a(a-rho b); sum a^2+b^2-2rho ab = (a-b)^2+2ab(1-rho) > 0 under |rho|<1; c-scaling); A4 (Xv_i = 0, Y and Sigma singular). No gap found.")
row("d-r1-16-weights-definition", "weights convention states its domain", "project.html Conventions 'Weights' (line 246)",
    "PASS", "Round 4: line 246 unchanged since aa3c26c; it states the formula only where Sigma is invertible and 1'Sigma^-1 1 != 0, and that the singular case is unspecified and untested (grader lines 569-590 assert no weights value for singular cases).")
row("d-r1-17-hours", "hub split equals lesson hours; project table equals 45", "course/modules/M/M3/index.html data-hours-lessons/project; L01-L09 data-hours; project.html time budget (lines 256-263)",
    "PASS", "Round 4: lesson data-hours 12,11,12,12,12,11,11,12,12 sum to 105 = data-hours-lessons; project table 2+3+14+8+12+6 = 45 = data-hours-project; 105+45 = 150. Pace not judged (architect ruling).")
row("d-r1-18-rubric-calibration", "official exemplar scores agree with the rubric cells and annotations", "project.html Exemplar B (lines 566-630), rubric C4/C5 cells (lines 495-496)",
    "PASS", "Round 4: data-scores=\"4,4,4,3,3\" and the official line 'C1 4 C2 4 C3 4 C4 3 C5 3' match the annotations: C4 level 4 needs a statement that no market claim is made, which Exemplar B lacks (it has 'Meets C4 level 3' only); C5 level 4 needs a direction for each limitation, which Exemplar B gives for the clipping error only (annotation 'Misses C5 level 4'). Round-3 FAIL resolved. Wording error in the same exemplar: row d-r4-38.")
row("d-r1-19-rubric-observable", "each rubric cell names an observable element", "project.html rubric table (lines 488-498) and scoring rule (line 484)",
    "PASS", "Round 4: cells read; each level names an element a reader can check; scoring rule at line 484 states containment. Cells unchanged since aa3c26c.")
row("d-r1-20-atlas", "no Atlas contract claim on the page", "course/modules/M/M3/project.html",
    "PASS", "Round 4: grep -c -i atlas project.html = 0.")
row("d-r1-21-citations-axler-strang", "cited registry keys are verified and attached claims match the registry", "project.html Reading (lines 664-671); references/references.json keys axler2024linear, strang2023introduction",
    "PASS", "Round 4: tools/verify_refs.py --offline: '560 entries, 0 problems'; tools/verify_refs.py --unit M3 (live): '2 of 560 entries, 0 problems'. references/ unchanged since aa3c26c (git diff empty), so the round-3 reading of the two registry entries still applies.")
row("d-r1-22-cards-sample", "every card whose subject changed is checked against the current lesson text", "course/modules/M/M3/cards.json (15 changed, 1 added since aa3c26c)",
    "PASS", "Round 4: changed M3-c076, c077, c092, c098, c099, c101, c102, c103, c106, c108, c112, c113, c114, c117, c167 and added c179 were read against the current lesson statements (L04 Thm 2.3 'Assuming F1 to F4'; L05 Thm 2.1, 2.2 'Assuming F1 to F4'; L06 Def 1.1, Fact 1.2 'Assuming F1', Lemma 1.3 'Assuming F3 (Gram-Schmidt)', Thm 2.2 'Assuming F1 to F4', Thm 2.3 'Assuming F1'; L07 Thm 2.2) and the Lab 1 outputs (L09 counts 23 of 40, 23 of 23 for both checks; L05 Part A output). Unchanged cards cite lesson statements whose text changed only by 'Assuming F1' prefixes; the four cited statements whose hypotheses were flagged by a scan (M3-c074, c082, c086, c109) were read: c082 and c086 cite Definition 1.4 (no hypothesis), c074 and c109 name no statement and are finite lab checks. The other 163 unchanged cards were checked by the structure, label and number scan only, not paragraph by paragraph (see notes).")
row("d-r1-23-cards-duplicates", "no duplicate card fronts or backs", "course/modules/M/M3/cards.json (full scan)",
    "PASS", "Round 4: ledgers/M3/scripts/M3-d-r2/cards_check.py . : 'DUPLICATE fronts: []', 'DUPLICATE backs: []', 'cards: 179 unique ids: 179'. Grade tally: T 104, C 37, no grade 38 (grade key absent); every C card has a basis.")
row("d-r1-24-lint", "ruff and the project mypy gate pass", "course/modules/M/M3/grader; tests/labs/M3; pyproject.toml [tool.mypy]",
    "PASS", "Round 4: ruff check grader and labs: 'All checks passed!'; ruff format --check: '16 files already formatted'; .venv/bin/mypy --no-incremental (project scope tools and tests): 'Success: no issues found in 255 source files'. Note: running mypy on the grader directory alone reports two import-not-found errors (covariance_doctor, instance); the grader is outside the configured mypy scope.")
row("d-r1-25-page-smoke", "page smoke passes within the browser budget", "course/modules/M/M3/project.html; tools/page_smoke.py --unit M3 --pages project --skip-sweep",
    "PASS", "Round 4: 'page_smoke M3: PASS'; in-browser grader 'All 142 tests pass on seed 697963252 (0.9 s)'; lab timings 0.0 s each.")
row("d-r2-26-floor-not-tested", "floor behaviour is tested", "grader/test_project.py lines 357-398",
    "PASS", "Round 4: m11_clip_ignores_floor KILLED by test_clip_repair_floor_raises_eigenvalues_below_it; f2_clip_ignores_floor KILLED; b2d_m02 KILLED by test_clip_repair_negative_floor_keeps_eigenvalue_above_it.")
row("d-r2-27-symmetry-tolerance-absolute", "symmetry tolerance is absolute, not relative", "grader/test_project.py lines 205-225",
    "PASS", "Round 4: m14_symmetry_relative_tolerance KILLED by test_asymmetry_exactly_the_tolerance_is_accepted[1.0-projection_repair]; f2_symmetry_tolerance_relative KILLED.")
row("d-r2-28-weights-singular-sigma", "weights stated only where Sigma is invertible, Lab 3 weights are the input's", "project.html Conventions 'Weights' (line 246) and Lab 3 interpretation (line 469)",
    "PASS", "Round 4: line 246 and the revised line 469 (Lab 3 prints weights for the input only; the clipped matrix is singular by A4, the projection's invertibility is not established) re-checked against twin3.out and the recomputation (det -0.2616).")
row("d-r2-29-lab3-test-overconstrains-solver", "the Lab 3 test checks the input only", "grader/test_project.py test_lab3_reference_numbers_are_matched (lines 451-475)",
    "PASS", "Round 4: unchanged; the nine alternatives pass seeds 0-49, including the Dykstra and clipping variants.")
row("d-r2-30-positive-diagonal-claim", "positive-diagonal claim in the conventions", "project.html Conventions 'Unit-diagonal matrix' (line 242)",
    "PASS", "Round 4: X_ii = sum_k max(lambda_k,0) V_ik^2 >= sum_k lambda_k V_ik^2 = A_ii > 0 when A_ii > 0 and the floor is 0 (re-derived); the rescaling is defined.")
row("d-r3-31-a2-unproven-only-when", "A2 makes no unproven 'only when' claim", "project.html Appendix A2 (line 636)",
    "PASS", "Round 4: the sentence now reads 'The positivity of d_i is needed for the division.' No 'only when' remains (grep). Re-derived A2 (see d-r1-15).")
row("d-r3-32-is-psd-boundary-survivor", "is_psd accepts an eigenvalue exactly at -tol (page line 233: 'every eigenvalue is at least -tol')",
    "grader/test_project.py test_is_psd_* (lines 271-311); project.html Required outputs (line 233)",
    "FAIL", "Survivor r3d_m01_is_psd_strict_at_minus_tol (is_psd returns min_eigenvalue > -tol) is KILLED by no test on seeds 0-9 (mutate_final_r4.out). Witness (ledgers/M3/scripts/M3-d-r4/witness_check.py output): is_psd(diag(-0.5, 1, 1), tol=0.5) is True for reference_solution, False for the mutant. The suite's boundary test (line 297) uses tol 0.5 +/- 1e-6, not the boundary.",
    "Add to test_project.py: assert is_psd([[-0.5,0,0],[0,1,0],[0,0,1]], tol=0.5) is True, citing 'every eigenvalue is at least -tol' (line 233). Check that the mutant is killed.")
row("d-r3-33-purity-not-stated", "the purity requirement is stated on the page and tested", "project.html Constraints (line 235), Grading mode (line 237); grader/test_project.py test_inputs_are_not_mutated (line 670), test_repeated_calls_agree (line 681)",
    "PASS", "Round 4: the requirement is stated (line 235: 'No function changes its arguments, and repeated calls with the same arguments return the same values'). The enforcement gap found this round is row d-r4-39, not this row.")
row("d-r3-34-cards-drop-hypotheses", "cards that cite hypothesis-laden statements carry the hypothesis", "course/modules/M/M3/cards.json M3-c076, c077, c092, c098, c099, c113",
    "PASS", "Round 4: all six cards now carry 'Under F1 to F4 of Lesson 4' (or 'under F1'); the cited statements read 'Assuming F1 to F4' (L04 Thm 2.3, L05 Thm 2.1 and 2.2, L06 Thm 2.2). Verified against the page text. Unchanged for c077 whose claim is Theorem 2.3 with symmetry.")
row("d-r3-35-mutant-m05-equivalent", "the returned iterate is within tolerance of the unit-diagonal iterate", "projection_repair returns the last PSD iterate (round-3 mutant r3d_m05, not kept in the list)",
    "PASS", CARRY + "grader/reference.py and instance.py. Round-3 witness: largest |y_ii - 1| = 8.596e-11 over seeds 0-49 (ledgers/M3/scripts/M3-d-r3/survivor_witness.py).")
row("d-r3-36-new-mutants-killed", "round-3 verifier mutants are killed", "ledgers/M3/mutants/r3d_m02, r3d_m03, r3d_m04, r3d_m06",
    "PASS", "Round 4 output: r3d_m02 KILLED by test_lab3_reference_numbers_are_matched; r3d_m03 by test_lab3_reference_numbers_are_matched; r3d_m04 by test_clip_repair_has_unit_diagonal_and_is_symmetric[seed]; r3d_m06 by test_weights_refuse_non_square_correlation[two_rows_three_columns].")
row("d-r3-37-dag-and-links", "DAG, page and project checks and concept links", "project.html concept links (lines 53, 243); tools/check_dag.py, check_pages.py, check_projects.py --all",
    "PASS", "Round 4: 'check_dag M3: PASS'; 'check_pages M3: PASS'; 'check_projects M3: PASS'.")
row("d-r4-38-exemplar-b-lab-prints", "the exemplar's claim about what Lab 3 prints", "project.html Exemplar B 'Distances and weights' / 'Repairs and their checks' paragraph (line ~590)",
    "FAIL", "The exemplar says 'Lab 3 prints ... True for the projection's smallest eigenvalue at tolerance 1e-8'. Lab 3 prints 'projection positive semidefinite at tol 1e-8: True' (twin3.out line 8); it prints no projection eigenvalue. Lab 3 prints the smallest eigenvalue of the input only (-0.142113).",
    "Reword to 'Lab 3 prints True for the projection's positive-semidefiniteness verdict at tolerance 1e-8'.")
row("d-r4-39-purity-test-order-dependent", "a comparison_weights that changes its volatility argument fails the purity test in the full suite", "grader/test_project.py test_inputs_are_not_mutated (lines 670-678) and the module-level INST (line 34); project.html Constraints line 235",
    "FAIL", "Mutant r4d_m03_weights_rescale_argument_in_place (divides the caller's vols list in place) SURVIVES the full suite on seeds 0-9 ('142 passed'). Pytest -k not_mutated on the same mutant fails at line 678 (assert vols == INST['vols']). The cause: INST['vols'] is passed directly to comparison_weights by earlier tests (lines 508, 530, 542, 555, 653, 666), so the shared list is already changed when line 678 compares it. Spec line 235 says no function changes its arguments.",
    "Snapshot the inputs at import (e.g. VOLS0 = copy.deepcopy(INST['vols']) and CORR0 = copy.deepcopy(INST['corr']) at module load) and assert against the snapshots, or pass only copies in the earlier tests. Re-run the mutant and check KILLED in the full suite.")
row("d-r4-40-is-psd-default-tolerance", "is_psd's default tolerance is 1e-10 (page signature)", "grader/test_project.py test_is_psd_* (lines 271-311); project.html Required outputs (line 233: 'is_psd(matrix, tol=1e-10)')",
    "FAIL", "Mutant r4d_m01_is_psd_default_tol_eight (default tol=1e-8) SURVIVES the full suite on seeds 0-9. Witness: is_psd(diag(-5e-9, 1, 1)) with the default tolerance is False for the reference and True for the mutant (verified in this round). Line 233 states the signature with tol=1e-10 and 'True when every eigenvalue is at least -tol'.",
    "Add a call without tol: assert is_psd(diag(-5e-9, 1, 1)) is False, citing line 233. Re-run and check the mutant is killed.")
row("d-r4-41-verifier-mutant-descriptions", "each mutant opens with a docstring that describes its error (VERIFIER_RULES 2.6)", "ledgers/M3/mutants/r3d_m01, m02, m03, m04, m06",
    "PASS", "Round 3 mutants opened with 'Reference solution ... Not shipped to learners.' instead of the error. Rewritten this round to describe the error (first docstring line); the code is unchanged, and the killed and survived outcomes are unchanged in mutate_final_r4.out.")
row("d-r4-42-projection-mutants-equivalent-on-domain", "two survivors of the projection cap and stopping rule are not a stated-behaviour violation", "ledgers/M3/scripts/M3-d-r4/equivalent_on_domain/ (r4d_m04_projection_default_iterations_fifty, r4d_m05_projection_stops_on_gap_only); ledgers/M3/scripts/M3-d-r4/proj_mut_check.py",
    "PASS", "Both mutants were removed from the mutants list. Over seeds 0-49 the outputs equal the reference's within 0 (m04) and 1.99e-11 (m05), with min eigenvalue -5.2e-11 and unit diagonal. Neither the page nor the contract states an iteration count beyond the signature default, and Exemplar B says the suite checks the result, not the stopping rule (line ~623). This is a domain-limited observation, not a proof of equivalence in general.")
row("d-r4-43-new-mutants-written", "at least three new student-error mutants for this round", "ledgers/M3/mutants/r4d_m01, r4d_m02, r4d_m03",
    "PASS", "Five new mutants were written (r4d_m01..m05). Two (m04, m05) are domain-equivalent and moved out (row d-r4-42). Three remain: m01 (SURVIVED, row d-r4-40), m02 (KILLED), m03 (SURVIVED, row d-r4-39).")

killed = sum(1 for m in mutants if m["killed_by"])
verdict_ok = all(r["status"] == "PASS" for r in R)
fragment = {
    "unit": "M3",
    "slice": "M3-d",
    "round": 4,
    "verifier": "independent verifier (Haiku), round 4, slice M3-d",
    "pin": "2657ab5",
    "base": "aa3c26c",
    "previous_ledger": "/tmp/fanout-frags/B-M3-d.round3.json",
    "checkout": "/tmp/verifyB4-M3-d",
    "scratch": "/tmp/m3-v/d/r4",
    "verified_at": "2026-10-28",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since aa3c26c (round-3 pin): project.html, grader/test_project.py, cards.json, L02-L09 and index.html (lesson changes add 'Assuming F1' hypotheses), tests/labs/M3/lab-M3-L03-1.py and lab-M3-L07-1.py (not in slice d). Byte-identical: grader/reference.py, grader/instance.py, grader/starter.py, lab-M3-project-1/2/3 twins, ledgers/M3/alternatives. Verified this round: the three project twins match the page output blocks exactly.",
        "Mutants: 56 in ledgers/M3/mutants (53 killed, 3 survived: r3d_m01 -> d-r3-32, r4d_m01 -> d-r4-40, r4d_m03 -> d-r4-39). r4d_m04 and r4d_m05 are kept out of the list (row d-r4-42). Mutate output: ledgers/M3/scripts/M3-d-r4/mutate_final_r4.out.",
        "Alternatives: nine correct implementations (builder alt1-alt6, verifier alt_r3a-c) each 0 failing seeds of 50 against the current grader (sweep_alts_r4.out.txt).",
        "Cards: 179 (c179 added). Hypothesis scan: ledgers/M3/scripts/M3-d-r4/card_scan_r4.py output in scratch; the heuristic scan has name collisions across lessons, so each flagged card was read against its own lesson.",
        "Not checked: a learner-written report (only the two exemplars are scored); the self-assessment form in a browser (UI); lesson pages L01-L09 paragraph by paragraph (outside slice d except as the source of the cards); 163 unchanged cards paragraph by paragraph; the 131 unchanged-card text beyond structure, label and number checks.",
        "Process note: the grader's full-suite run uses one shared INST object, which is why the purity mutant survives (row d-r4-39); the test file itself was not edited.",
    ],
    "summary": f"M3-d round 4: {len(R)} rows, {sum(1 for r in R if r['status']=='PASS')} PASS, {sum(1 for r in R if r['status']=='FAIL')} FAIL; {len(mutants)} mutants, {killed} killed, 3 survived.",
}
path = ROOT / "ledgers/M3/M3-d.json"
path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", path, "rows", len(R), "mutants", len(mutants), "killed", killed)
