"""Build the round-2 ledger fragment for M3 slice M3-d from the verifier's recorded evidence.

Reads the mutate_graders output saved in this directory for the mutant list; the rows carry the evidence
recorded in the round-2 scripts (named by repository path in each row). Usage: build_fragment_r2.py <checkout-root>
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
here = root / "ledgers/M3/scripts/M3-d-r2"
S = "ledgers/M3/scripts/M3-d-r2"

mutants = []
for line in (here / "mutate_graders_M3_r2.out.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?)\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    entry = {"id": name, "description": desc}
    if status == "KILLED":
        entry["killed_by"] = killer
    else:
        entry["killed_by"] = ""
        entry["survived"] = "true"
    mutants.append(entry)

R = lambda **kw: kw  # noqa: E731
rows = [
    R(id="d-r1-01-suite-count", check="2.6-spec", location="course/modules/M/M3/project.html Grading mode; grader/test_project.py",
      status="PASS", evidence="pytest --collect-only on the reference copy: '105 tests collected'; the page says 105 (project.html line 237). In-browser: page_smoke --unit M3 --pages project printed 'All 105 tests pass on seed 1034933034'."),
    R(id="d-r1-02-spec-named-refusals", check="2.6-spec", location="project.html Constraints and Conventions (four named ValueError conditions); grader/test_project.py must_raise call sites",
      status="PASS", evidence="must_raise is used only in test_non_square_is_refused and test_asymmetry_beyond_tolerance_is_refused (MATRIX_FUNCS: min_eigenvalue, is_psd, clip_repair, projection_repair), test_weights_refuse_non_square_correlation, test_weights_refuse_asymmetric_correlation_beyond_tolerance, test_weights_refuse_volatility_at_or_below_zero, test_weights_refuse_length_mismatch (test_project.py lines 151-563). No other exception type is asserted. The page's 'in each function where that condition applies' matches these parametrisations."),
    R(id="d-r1-03-tests-only-unit-diagonal", check="2.6-spec", location="project.html Conventions 'Unit-diagonal matrix' item; grader/test_project.py test_min_eigenvalue_is_smallest_of_diagonal (line 206), test_min_eigenvalue_one_by_one, test_is_psd_one_by_one",
      status="PASS", evidence="The round-1 sentence is rewritten (project.html line 242): instances are unit-diagonal by construction (grader/instance.py _unit_symmetric line 'm[i][i] = 1.0' and _positive_definite normalised Gram), and the tests also use planted spectra and hand-made non-unit-diagonal matrices such as diag(3, -2, 5) (test line 208) and [[-0.25]] (line 213). Each claim is checked against the file text."),
    R(id="d-r1-04-over-constraint-differs-from-clipping", check="2.6-grader-alt", location="grader/test_project.py (round 1 test test_projection_repair_differs_from_clipping_on_this_instance removed)",
      status="PASS", evidence="The test is absent from the round-2 suite (grep -n differs_from_clipping test_project.py: no match). The replacement, test_lab3_reference_numbers_are_matched, is not the same property; the reference and alternatives alt1-alt6, alt_r2a, alt_r2c pass seeds 0-49 (sweep.py output in " + S + "). The round-1 witness seed 8574 cannot fail any remaining test."),
    R(id="d-r1-05-grader-reference-seeds", check="2.6-autograder", location="grader/reference.py; grader/instance.py",
      status="PASS", evidence="tools/run_graders.py --unit M3 --seeds 0-49: 'PASS (reference 50/50 seeds, slowest 0.2 s)'; " + S + "/sweep.py reference.py 0 49: 0 failing seeds of 50."),
    R(id="d-r1-06-instances-valid-and-varied", check="2.6-autograder", location="grader/instance.py make_instance",
      status="PASS", evidence="Carried from round 1 (grader/instance.py byte-identical since the previous pin c11ae01; git diff --name-only shows only test_project.py changed in grader/): round-1 evidence: k in {3,4,5} across seeds 0-19 and 20 distinct smallest eigenvalues of corr, each below -0.02 by the redraw rule (instance.py lines 'if _min_eigenvalue(corr) >= -_MARGIN: continue')."),
    R(id="d-r1-07-mutants-existing", check="2.6-mutation", location="ledgers/M3/mutants/fx01-fx10, m01-m10 (existing before this round's additions)",
      status="PASS", evidence="tools/mutate_graders.py --unit M3 --seeds 0-9 before adding round-2 mutants: all 24 existing mutants killed (fx01-fx10, m01-m10, v01-v04). Output recorded in " + S + "/mutate_graders_M3_r2.out.txt (the first 24 lines)."),
    R(id="d-r1-08-mutants-verifier", check="2.6-mutation", location="ledgers/M3/mutants/v01-v04",
      status="PASS", evidence="v01 killed by test_clip_repair_has_unit_diagonal_and_is_symmetric[seed]; v02 by test_weights_refuse_length_mismatch[longer]; v03 by test_projection_repair_is_a_valid_repair[seed]; v04 by test_asymmetry_beyond_tolerance_is_refused (mutate_graders output, seeds 0-9)."),
    R(id="d-r1-09-alternatives", check="2.6-autograder", location="ledgers/M3/alternatives/alt1-alt6 (builder-supplied); " + S + "/alternatives/alt_r2a, alt_r2b, alt_r2c",
      status="PASS", evidence="sweep.py over seeds 0-49: alt1..alt6 each 0 failing seeds of 50; alt_r2a_numpy_dykstra.py 0/50; alt_r2c_reference_other_cutoffs.py 0/50. Caveat from round 1 resolved: alt6 is NumPy-based. alt_r2b_pure_bisection_cholesky.py fails 50/50 (see d-r2-29); the other eight pass."),
    R(id="d-r1-10-lab1-output", check="2.5-labs", location="project.html Lab 1 (Rung 1); tests/labs/M3/lab-M3-project-1.py",
      status="PASS", evidence="tools/run_labs.py --unit M3: 'PASS (12/12)'; python -I -W error on the twin reproduces the page's expected block exactly (8 lines); " + S + "/lab_numbers.py recomputes eigenvalues -0.275297 1.463830 1.811467, rebuilt diagonal 1.096064 1.104409 1.074824 and repaired entries 0.636095, -0.382551, 0.469578 with numpy."),
    R(id="d-r1-11-lab2-output", check="2.5-labs", location="project.html Lab 2 (Rung 2); tests/labs/M3/lab-M3-project-2.py",
      status="PASS", evidence="Twin output equals the page's expected block (8 lines, diff empty). lab_numbers.py recomputes eigenvalues -0.203711 1.486490 1.717222, rebuilt diagonal 1.060165 1.075224 1.068322, repaired entries 0.498962, 0.409576, -0.586237."),
    R(id="d-r1-12-lab3-output-and-numbers", check="2.5-labs", location="project.html Lab 3 (Rung 3 reference numbers); tests/labs/M3/lab-M3-project-3.py",
      status="FAIL", evidence="The non-weight printed numbers reproduce (smallest eigenvalue -0.142113, distances 0.176573 and 0.175003, gap 0.001570, largest entry difference 0.011516, diagonal deviations 0.000000; " + S + "/lab_numbers.py). The printed weights do not come from the closed form: for the clipping repair the smallest eigenvalue of Sigma = DYD is 7.26e-18 (cond 1.7e16) and the printed weights are the normalised null vector of Sigma (residual 6.3e-18; " + S + "/null_check.py and sing_check.py). The projection's Sigma has eigenvalue -4.9e-13. See d-r2-28.",
      fix="Make the Lab 3 weights come from a positive definite correlation matrix (for example, a clipped matrix with a strictly positive smallest eigenvalue, or a different input), or state in the page that the clipping and projection matrices are singular and that their weights are a limit, then re-run the lab and regenerate the expected block."),
    R(id="d-r1-13-lab3-max-entry-gap", check="2.5-labs", location="project.html Lab 3 interpretation ('0.011516')",
      status="PASS", evidence="lab_numbers.py: max entry difference between projection and clipping = 0.011516416659581696 (unrounded), printed 0.011516 (project.html line 450)."),
    R(id="d-r1-14-lab3-smallest-eig", check="2.5-labs", location="project.html Lab 3 and Exemplar B summary (-0.142113)",
      status="PASS", evidence="lab_numbers.py: smallest eigenvalue of the Lab 3 input = -0.14211263700676982, printed -0.142113 (project.html line 446; Exemplar B summary line 562)."),
    R(id="d-r1-15-proofs-A1-A3", check="2.4-mathematics", location="project.html Appendix A (A1, A2, A3), lines 468 and 620-624",
      status="PASS", evidence="A1: X symmetric, z'Xz = sum max(lambda_i, f)(V'z)_i^2 >= 0 for f >= 0: re-derived by hand. A2: Y_ii = X_ii/(sqrt(d_i))^2 = 1 and z'Yz = w'Xw with w = D^{-1/2}z: re-derived. A3: det Sigma = a^2 b^2 (1 - rho^2), Sigma^{-1} 1 = (det)^{-1}(b(b - rho a), a(a - rho b)), sum a^2+b^2-2 rho ab = (a-b)^2 + 2ab(1-rho) > 0, scaling by c: " + S + "/a3_check.py over a 5x6x6 grid: max deviation 6.4e-14 between the closed form and the solve, and invariance under scaling by 3.7."),
    R(id="d-r1-16-weights-definition", check="2.4-mathematics", location="project.html Conventions 'Weights' item (line 246) and Required outputs (comparison_weights)",
      status="FAIL", evidence="The convention gives w = Sigma^{-1} 1 / (1' Sigma^{-1} 1) for every unit-diagonal correlation matrix C, with no invertibility hypothesis. Counterexample: C = [[1, 1], [1, 1]] (PSD with unit diagonal; the page's own Lesson 9 Example 3.6 yields this matrix), volumes (0.1, 0.2): Sigma = [[0.01, 0.02], [0.02, 0.04]] has determinant 0, so Sigma^{-1} does not exist. grader/reference.py comparison_weights raises ZeroDivisionError on this input (" + S + "/sing_check.py, last lines: 'reference weights on ... raises'). See d-r2-28.",
      fix="State the hypothesis: C positive definite (so Sigma is invertible), and say what comparison_weights returns for a singular C, or restrict the Lab 3 and report weights to a positive definite input."),
    R(id="d-r1-17-hours", check="2.9-hours", location="project.html Time budget table (#hours); index.html data-hours-lessons/data-hours-project; L01-L09 data-hours",
      status="PASS", evidence="Project rows 2+3+14+8+12+6 = 45 = data-hours-project. Lesson data-hours 12+11+12+12+12+11+11+12+12 = 105 = index data-hours-lessons; 105 + 45 = 150 = index 'Module M3 ... 150 hours'; 45/150 = 30% = index eyebrow. No pace claim checked (architect ruling)."),
    R(id="d-r1-18-rubric-calibration", check="2.6-rubric", location="project.html Exemplar B official scoring (line 558) and annotations (lines 566, 613-614); Exemplar A annotations (lines 501-552)",
      status="FAIL", evidence="Exemplar B's official scoring says it 'falls short of level 4 for C4 once: the report labels the inputs but does not say what a market claim would require'. Its own Limitations paragraph (line 609) says 'A market study would need real pairwise estimates, a source whose terms permit their use, and the same test of positive semidefiniteness on them', so the stated reason is contradicted by the exemplar text (what it omits is the statement that no market claim is made). Exemplar B's annotation at line 566 ('Meets C5 level 4: the Summary is under 80 words') attaches a summary length check to C5, which has no summary element in the rubric (line 483). Exemplar A's scores and annotations are consistent with the rubric rules I checked.",
      fix="Rewrite the Exemplar B C4 reason to name the missing element (no statement that no market claim is made), and move the summary-length annotation to a rubric element or drop it."),
    R(id="d-r1-19-rubric-observable", check="2.6-rubric", location="project.html rubric table (#rubric, lines 475-485) and Scoring paragraph (line 471)",
      status="PASS", evidence="Each level cell names an element a reader can find (for example 'the tolerance used', 'proves A3 for the two-asset case with |rho| < 1 and a, b > 0 named', 'names the test in the suite'); the scoring rule (line 471) defines levels by containment. Checked element by element against the exemplar annotations."),
    R(id="d-r1-20-atlas", check="2.7-structure", location="project.html (no Atlas section); plans/M3-build-plan.md line 3 and line 40",
      status="PASS", evidence="grep -c -i atlas course/modules/M/M3/project.html = 0; the plan states 'no Atlas milestone'."),
    R(id="d-r1-21-citations-axler-strang", check="2.1-citations", location="project.html Reading (lines 653-656); references/references.json keys axler2024linear (line 1208) and strang2023introduction (line 21415)",
      status="PASS", evidence="Registry editions: axler2024linear citation string 'Axler, Linear Algebra Done Right, 4th ed. (2024)'; strang2023introduction 'Strang, Introduction to Linear Algebra, 6th ed. (2023)' (references.json). tools/verify_refs.py --unit M3 (live): 2 of 560 entries re-verified, 0 problems; tools/verify_refs.py --offline: 560 entries, 0 problems. The page attributes no statement to either source (line 653)."),
    R(id="d-r1-22-cards-sample", check="2.7-cards", location="course/modules/M/M3/cards.json (170 cards; 21 changed or added since c11ae01)",
      status="PASS", evidence="Full scan: " + S + "/cards_check.py over all 170 cards: every Definition/Proposition/Theorem/Lemma/Corollary/Remark/Example label cited in a card exists in its lesson (no MISSING; two cross-lesson references M3-c054 and M3-c090 are named as such); every grade-T card cites only T claims; numbers in backs appear in the lesson text except '-1e-8' (M3-c167, written as a power of ten in the lesson). Changed or added cards (M3-c009, 054, 060, 076, 083-086, 090, 091, 096, 098, 100, 106, 112, 114, 145, 167, 168, 169, 170) read against the cited blocks: Definition 3.3, Proposition 3.12 (L01); Example 2.5, Proposition 1.4 (L03); Remark 1.6, Remark 2.7, Theorem 2.3 (L04); Proposition 1.5, 1.6, Example 1.7, Remark 1.8, Proposition 2.4, Remark 2.7, Example 2.6, Theorem 2.1, Remark 3.2, Definition 3.1 (L05); Theorem 2.3 and Remark 2.5 (L06); Theorem 2.2(c), Definition 2.1 (L07); Theorem 2.1 and the Lab 1 seed-8 claim (L08); Definition 2.1, Remark 2.2 and the Lab 1 counts (L09). Matrix claims were recomputed (C0 eigenvalues -0.8, 1.9, 1.9 and x'C0x = -2.4; [[1,2],[2,1]] form -2; the closed-form P^{-1}AP; AC vs CA). Lab numbers for cards M3-c016, c018, c074, c075, c094, c095, c096, c110, c111, c124-126, c139-141, c145, c162-164, c167 were matched to the printed lab output lines. Limit: I read all 170 card fronts and backs, and checked every mathematical and lab-number claim I could check; the lesson blocks of the 149 unchanged cards were checked by label and by mathematics, not each lesson paragraph."),
    R(id="d-r1-23-cards-duplicates", check="2.7-cards", location="course/modules/M/M3/cards.json (full scan)",
      status="PASS", evidence="Full scan of 170 cards: 170 unique ids; no duplicate fronts or backs (cards_check.out.txt lines 'DUPLICATE fronts: []', 'DUPLICATE backs: []'); difflib near-duplicate fronts above 0.8: only M3-c087/M3-c088 (positive semidefinite vs positive definite), which are distinct questions."),
    R(id="d-r1-24-lint", check="2.9-lint", location="grader/ and tests/labs/M3/",
      status="PASS", evidence=".venv/bin/ruff check tests/labs/M3 course/modules/M/M3/grader: All checks passed; ruff format --check: 16 files already formatted; .venv/bin/mypy --no-incremental (repository config, strict): Success, no issues found in 255 source files. Note: mypy run on the grader directory alone reports import-not-found for 'instance', because the grader is outside the repository mypy files; the repository gate passes."),
    R(id="d-r1-25-page-smoke", check="2.5-labs", location="course/modules/M/M3/project.html; tools/page_smoke.py --unit M3 --pages project --skip-sweep",
      status="PASS", evidence="page_smoke M3: PASS; lab-M3-project-1/2/3 ran in the browser runtime; in-browser grader: All 105 tests pass on seed 1034933034 (0.9 s)."),
    R(id="d-r2-26-floor-not-tested", check="2.6-mutation", location="grader/test_project.py (clip_repair floor tests, lines 322-333); project.html Required outputs ('clip_repair(matrix, floor=0.0), which sets every eigenvalue below floor to floor')",
      status="FAIL", evidence="Mutant m11_clip_ignores_floor (ledgers/M3/mutants/m11_clip_ignores_floor.py) always clips at 0 and SURVIVES all 105 tests on seeds 0-9. test_clip_repair_with_positive_floor_is_positive_semidefinite (floor 0.01) checks only PSD, which a zero-floor clip also satisfies; test_clip_repair_floor_below_every_eigenvalue_changes_nothing (floor -0.5) passes for a function that ignores the floor. The page states the floor behaviour (project.html Required outputs) and the suite never checks it.",
      fix="Add a test: for a unit-diagonal PSD input with a known eigenvalue below a positive floor f, clip_repair(A, floor=f) must differ from clip_repair(A) and must have every eigenvalue at least f before rescaling (or check the rebuilt matrix's smallest eigenvalue via the rescaling-invariant test)."),
    R(id="d-r2-27-symmetry-tolerance-absolute", check="2.6-mutation", location="grader/test_project.py test_asymmetry_within_tolerance_is_accepted (line 185) and test_asymmetry_beyond_tolerance_is_refused (line 175); project.html Conventions item (2) (line 247)",
      status="FAIL", evidence="Mutant m14_symmetry_relative_tolerance (ledgers/M3/mutants/m14_symmetry_relative_tolerance.py) refuses a pair that differs by 5e-10 when the entries are about 0.3 (threshold 1e-9 * max(|m_ij|, |m_ji|)), which the page's named condition does not cover ('beyond 1e-9'). It SURVIVES all tests on seeds 0-9: the accepted-asymmetry test uses 1e-10 (below the relative threshold 3e-10) and the refusal test uses 1e-8. Output: " + S + "/mutate_graders_M3_r2.out.txt.",
      fix="Add a test that a pair differing by 5e-10 at entries near 0.3 is accepted by every matrix function, and a pair differing by 2e-9 at entries near 0.3 is refused."),
    R(id="d-r2-28-weights-singular-sigma", check="2.4-mathematics", location="project.html Conventions 'Weights' (line 246) and Lab 3 (weights printed at lines 453-454); grader/test_project.py test_lab3_reference_numbers_are_matched (lines 390-415)",
      status="FAIL", evidence="Counterexample to the stated formula: C = [[1,1],[1,1]], volatilities (0.1, 0.2) gives a singular Sigma (det 0), so w = Sigma^{-1} 1 is undefined, yet C is a unit-diagonal PSD matrix (the page's own Lesson 9 Example 3.6 produces it). The Lab 3 clipping repair is singular in exact arithmetic (it zeroes the negative eigenvalue): eigvalsh(Sigma) = 7.26e-18, cond = 1.7e16; the printed clipping weights 1.218951, -0.546718, -0.012462, 0.340229 are the normalised null vector of Sigma (residual 6.3e-18; " + S + "/null_check.py). The projection repair's Sigma has eigenvalue -4.9e-13 and cond 2.0e11, so its printed weights are also set by a near-singular solve. numpy.linalg.lstsq (minimum-norm) gives 0.118840, 0.289713, 0.532186, 0.059261 for the clipping case (" + S + "/sing_check.py). The page presents these as the closed-form weights and its recommendation (line 609) rests on the projection weights.",
      fix="Add the hypothesis 'C positive definite' to the Weights convention, and remove the singular clipping and projection cases from Lab 3's weight lines and from the report's weight claims (or state that they are a limit or a minimum-norm answer and define that answer)."),
    R(id="d-r2-29-lab3-test-overconstrains-solver", check="2.6-autograder", location="grader/test_project.py test_lab3_reference_numbers_are_matched (weights part, lines 408-413)",
      status="FAIL", evidence="The test demands weights of the singular Lab 3 matrices to 1e-6 (clipping) and 1e-5 (projection). A correct Cholesky weight solve (" + S + "/alternatives/alt_r2b_pure_bisection_cholesky.py) raises ValueError 'expected a nonnegative input, got -2.39e-11' on the clipping matrix: test_lab3_reference_numbers_are_matched fails on seeds 0-49 (sweep.py: 50 failing seeds of 50; all other tests pass). A minimum-norm weight solve (lstsq_variant.py; " + S + "/lstsq_variant.py) fails the same test with an AssertionError on seeds 0-49. Neither method is wrong for a positive definite Sigma, where the spec's formula is defined, and the spec does not define the singular case (see d-r2-28).",
      fix="Restrict the printed-weight check to a positive definite input (keep the clipping and projection checks for the non-weight numbers), or define the singular-case answer in the page and test it."),
    R(id="d-r2-30-positive-diagonal-claim", check="2.4-mathematics", location="project.html Conventions 'Unit-diagonal matrix' item (line 242): 'The repairs are specified for any symmetric matrix with a positive diagonal.'",
      status="PASS", evidence="Proof checked: for clip_repair with floor f >= 0 and input A with A_ii > 0, X_ii = sum_k max(lambda_k, f) V_ik^2. If X_ii = 0 then V_ik = 0 for every k with lambda_k > 0 and f = 0, so A_ii = sum_{lambda_k<0} lambda_k V_ik^2 <= 0, a contradiction; for f > 0, X_ii >= f > 0. For a negative floor f < 0, max(lambda_k, f) >= lambda_k gives X_ii >= A_ii > 0. The projection repair is a Dykstra iteration on symmetric matrices and needs no sign condition."),
]

fragment = {
    "unit": "M3",
    "slice": "M3-d",
    "round": 2,
    "verifier": "independent verifier (Haiku), round 2, slice M3-d",
    "pin": "1817191",
    "base": "c11ae01",
    "previous_ledger": "/tmp/fanout-frags/B-M3-d.round1.json",
    "checkout": "/tmp/verifyB2-M3-d",
    "scratch": "/tmp/m3-v/d/r2",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since c11ae01: project.html, grader/test_project.py, cards.json, tests/labs/M3/lab-M3-project-3.py (L01, L06, L08 labs are other slices). grader/reference.py, grader/instance.py, grader/starter.py, lab-M3-project-1/2 twins and alt1-alt5 are byte-identical to c11ae01 (git diff --name-only).",
        "Hours: architect ruling applied; only arithmetic checked.",
        "Mutants: 28 in ledgers/M3/mutants (24 existing + m11-m14 written by this verifier); 26 killed, 2 survived (m11, m14). v01-v04 are present in the pinned tree (added after c11ae01).",
        "Not checked: a real NumPy-free browser run of alternatives (only Python sweeps); the report rubric was not scored on a learner report, only the exemplars were read; the 149 unchanged cards were checked by label, grade and mathematics, not paragraph by paragraph against each lesson block.",
        "The Lab 3 weights FAIL depends on singularity that is exact in the mathematics (Sigma has an exact zero eigenvalue for any clipped matrix with one negative eigenvalue and a unit diagonal after rescaling); the numerical value 7.26e-18 is the floating-point image of that zero.",
    ],
    "summary": "M3-d round 2: 30 rows, 23 PASS, 7 FAIL (d-r1-12, d-r1-16, d-r1-18, d-r2-26, d-r2-27, d-r2-28, d-r2-29); 28 mutants, 26 killed, 2 survived (m11, m14). FAIL.",
}

(root / "ledgers/M3/M3-d.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote ledgers/M3/M3-d.json", len(rows), "rows", len(mutants), "mutants")
