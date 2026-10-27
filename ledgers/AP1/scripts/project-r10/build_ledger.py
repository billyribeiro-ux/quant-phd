import json, re
from pathlib import Path

S = "/tmp/ap1-r5/project-r10"
CK = "/tmp/verify-ap1-r10-m"
R10 = "Round 10 (checkout ee0f984)"

# ---- mutants from the fresh mutate_graders run (seeds 0-9) ----
mut = []
for line in Path(f"{S}/mutate2.log").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    killed_by = None if killed.strip() == "None" else killed.strip()
    mut.append({"file": fname, "desc": desc, "killed_by": killed_by, "status": status})
assert len(mut) == 66, len(mut)

rows = []
def row(i, check, loc, status, ev, fix=None):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        assert fix, i
        r["fix"] = fix
    rows.append(r)

# ---------------- specification ----------------
row("proj-spec-completeness", "2.6-spec",
    "course/modules/AP/AP1/project.html #spec lines 127-140 (Constraints line 137); grader/starter.py; grader/test_project.py test_empty_payoff_sample_raises",
    "FAIL",
    f"{R10}: read project.html lines 127-140 and starter.py as a student. Signatures, dataclass, divide-by-T, error sign, strict x*<0, rank rule, finiteness and probability rules are stated. Questions a student would still have to ask: (1) the 'sum to one' tolerance is not a number (the suite accepts 1e-12, rejects 1e-6); (2) the tolerance for 'linearly dependent'/'singular' is not a number; (3) whether an empty payoff sample must raise is not stated anywhere, yet test_empty_payoff_sample_raises[sdf-values] requires ValueError for sdf_values on a (0, N) sample, where the spec's own definition (line 145: sdf_values returns Xb, one value per observation) gives an empty vector. Question (3) is decisive: the autograder enforces an answer the spec does not give.",
    "State in the Constraints paragraph (project.html line 137) whether an empty payoff sample raises ValueError. If it does, say so for every function that the sentence covers; if the spec should leave sdf_values on an empty sample to the student, delete the 'sdf-values' case from test_empty_payoff_sample_raises (see proj-new-tests-empty-sample).")

row("proj-spec-toolchain-claim", "2.6-spec", "course/modules/AP/AP1/project.html line 185",
    "PASS",
    f"{R10}: line 185 says 'Use Python 3.14 with NumPy 2.4 and pytest 9.0, the versions the in-browser grader runs.' Checkout venv: Python 3.14.8, numpy 2.4.6, pytest 9.0.2 (.venv/bin/python -c). course/assets/vendor/LOCK.json: numpy-2.4.6 (line 360) and pytest-9.0.2 (line 432) under pyodide v314.0.7.")

row("proj-spec-invalid-input-claim", "2.6-spec",
    "course/modules/AP/AP1/project.html line 137 (Constraints) and line 163 (time-budget row: 'every invalid input the specification names has a test'); grader/test_project.py test_invalid_input_raises (ids), test_square_redundant_payoffs_raise",
    "PASS",
    f"{R10}: re-derived from the ids of test_invalid_input_raises and the new tests. Each named input has a case: non-finite payoffs, prices, probabilities, SDF values, weights and means for every function that takes them (nan/inf ids); 1-d payoffs for every function (1d, 1d-moments, 1d-sdf, 1d-errors, 1d-population, 1d-minvar, 1d-minstd, 1d-train, 1d-test); fewer observations than assets (few); redundant payoffs at T>N (redundant, redundant-sum) and at T=N (test_square_redundant_payoffs_raise, m62 killed); singular covariance for min_variance_sdf and min_sdf_std (constant-var, constant-std, redundant-cov, redundant-cov-std, riskless seeds); probabilities negative, zero, summing to 2 or off by 1e-6/5e-4, wrong length, NaN/inf (neg-probs, zero-probs, sum, sum-1.0005, sum-1-plus-1e-6, probs-len, nan-probs, inf-probs); wrong SDF and weights lengths (m-len, short-prices). Observation, not a row failure: a T<=N singular-covariance sample for min_variance_sdf is not tested by itself; every realistic singular-covariance check (SVD, matrix_rank, cond) rejects it, and solve-only versions are killed by the riskless and redundant cases, so no plausible surviving mutant was found.")

row("proj-spec-print-warn-claim", "2.6-spec",
    "course/modules/AP/AP1/project.html line 137; grader/test_project.py test_every_public_function_is_silent_and_pure, test_ill_conditioned_payoffs_emit_no_warning, test_negative_sdf_values_are_legal_and_silent",
    "PASS",
    f"{R10}: the three named tests exist and pass on reference.py for seeds 0-49 (run_graders PASS 50/50). Killed in the mutate run (seeds 0-9, scratch/mutate2.log): m49 by test_every_public_function_is_silent_and_pure; m50 and m52 by test_ill_conditioned_payoffs_emit_no_warning; m53 by test_negative_sdf_values_are_legal_and_silent.")

row("proj-constraints-coverage", "2.6-spec",
    "course/modules/AP/AP1/project.html line 137 (Constraints) and line 139; grader/test_project.py",
    "PASS",
    f"{R10}: each Constraints item traced to a test: NumPy and stdlib only (test_imports_only_numpy_and_the_standard_library); pure, no print/warn/mutate (test_functions_do_not_mutate_or_print, test_every_public_function_is_silent_and_pure, test_min_sdf_std_does_not_change_its_prices); finite arrays and mean (invalid-input nan/inf ids); T divisor (test_second_moment_matrix_definition); E[mx]-p (test_pricing_error_sign_and_value); redundancy at T>N and T=N (redundant ids, test_square_redundant_payoffs_raise); fewer observations than assets (few); singular covariance (constant-*, redundant-cov*); probabilities (probability ids and rounding tests). Grading-mode invariance to units is covered for x* (test_x_star_is_invariant_to_units, test_x_star_accepts_small_units, test_rank_check_is_scale_invariant) and now for min_variance_sdf and min_sdf_std (test_min_variance_sdf_is_scale_equivariant, test_min_sdf_std_is_scale_invariant; killed m64). The 60-second limit: in-browser run of all 119 checks took 0.7 s (page_smoke, below).")

row("proj-hours-estimate", "2.6-hours",
    "course/modules/AP/AP1/project.html #hours (lines 153-169) and data-hours-project=36 (line 33)",
    "PASS",
    f"{R10}: the table sums to 36 (1+3+1+4+4+1+2+12+6+2), matching line 33 and line 35. My own estimate, component by component: read and set up 1; moments, x* and pricing errors 2.5; population x* 1; min-variance and std 3.5; recover_sdf and edge cases 3.5; local and browser runs 1; run_report 2; proof appendix 10; report 5; self-assessment 2. Total 31.5, which is 12.5% below 36 (limit 30%). Code 14.5 against the table's 16, report 17 against 20: each within 30%.")

row("proj-ladder", "2.6-ladder", "course/modules/AP/AP1/project.html #ladder lines 40-49; check_projects output",
    "PASS",
    f"{R10}: read lines 40-49. Rung 1 'Worked example' (Lab 1, fully annotated); Rung 2 'Completion problem' (Lab 2, 'graded instantly'); Rung 3 'Independent project' (section 3, autograded and rubric-graded); Rung 4 'Stretch' (section 8). Tier M, so rungs 1-2 are minimal, as the line-40 text says. tools/check_projects.py --unit AP1: 'check_projects AP1: PASS', exit 0.")

row("proj-reference-docstring-claim", "2.6-spec",
    "course/modules/AP/AP1/grader/reference.py lines 1-16 (module docstring, changed at 33fd452..ee0f984: 'raises ValueError, and'); grader/starter.py lines 7-12",
    "PASS",
    f"{R10}: the docstring claims that every function validates its inputs, raises ValueError, and never prints, warns or mutates its arguments. Reading reference.py: no print, no warnings call, all array inputs copied via np.array or np.asarray with the copy taken before any change (_matrix, _vector). test_every_public_function_is_silent_and_pure and test_functions_do_not_mutate_or_print pass for reference.py (run_graders PASS 50/50). starter.py's message wording now says 'a message ... helps you debug', consistent with test_invalid_input_raises, which checks the exception type only.")

# ---------------- new tests (round 10) ----------------
row("proj-new-tests-probability", "2.6-spec",
    "grader/test_project.py test_probabilities_off_one_beyond_rounding_raise, test_probability_rounding_is_accepted",
    "PASS",
    f"{R10}: both pass on reference.py (run_graders PASS 50/50). Killed in the mutate run (seeds 0-9): m55 (sum tolerance 1e-3) by test_probabilities_off_one_beyond_rounding_raise[sum-1.0005]; m41 (zero probabilities allowed) by test_invalid_input_raises[zero-probs] (seed 0). The 1e-12 rounding case is accepted (passes).")

row("proj-new-tests-negative-sdf", "2.6-spec", "grader/test_project.py test_negative_sdf_values_are_legal_and_silent",
    "PASS",
    f"{R10}: passes on reference.py for seeds 0-49. Killed in the mutate run: m53 by this test (scratch/mutate2.log).")

row("proj-new-tests-scale-invariance", "2.6-spec",
    "grader/test_project.py test_rank_check_is_scale_invariant[tiny-units], [huge-units]",
    "PASS",
    f"{R10}: passes on reference.py for seeds 0-49. Killed: m54 (absolute singular-value tolerance in _full_rank) by test_rank_check_is_scale_invariant (scratch/mutate2.log).")

row("proj-new-tests-share-below-zero", "2.6-spec",
    "grader/test_project.py test_share_negative_counts_states_just_below_zero (lines 771-780)",
    "PASS",
    f"{R10}: passes on reference.py for seeds 0-49. Killed: m59 (test_share_negative counts only x* below -1e-9) by this test (mutate2.log).")

row("proj-new-tests-ill-conditioned", "2.6-spec",
    "grader/test_project.py test_ill_conditioned_full_rank_payoffs_are_accepted (lines 783-794)",
    "PASS",
    f"{R10}: passes on reference.py for seeds 0-49. Killed: m60 (x_star_weights rejects condition number above 1e12) by this test (mutate2.log).")

row("proj-new-tests-square-redundant", "2.6-spec",
    "grader/test_project.py test_square_redundant_payoffs_raise (lines 797-803)",
    "PASS",
    f"{R10}: the test builds a T=N sample whose last payoff is the sum of two others, and requires ValueError from x_star_weights. Passes on reference.py for seeds 0-49. A rank check at T=N (matrix_rank, SVD, or cond of the second moment matrix) raises, so a correct student solution passes. Killed: m62 (redundancy check skipped when T equals N) by this test, seed 0 (mutate2.log). Witness of the mutant's fault: the mutant returns weights where the reference raises.")

row("proj-new-tests-empty-sample", "2.6-spec",
    "grader/test_project.py test_empty_payoff_sample_raises, id 'sdf-values' (lines 806-821)",
    "FAIL",
    f"{R10}: the nine cases raise ValueError on a (0, N) payoff sample. Eight are required by the spec: second_moment_matrix, pricing_errors and recover_sdf divide by T; min-variance and min-std need T > N (covariance); x_star_weights needs T >= N (fewer observations than assets); population_x_star fails the probability-sum rule. The 'sdf-values' case is not. Spec line 145 defines sdf_values as Xb with one value per observation, which for T = 0 is an empty vector, and nothing in the spec makes an empty sample invalid. Witness: a validating sdf_values that checks ndim, finiteness and the weight length, and otherwise returns x @ b (scratch e_finite_no_empty/sdf_recovery.py), runs 118 passed and 1 failed on seeds 0 and 49, the failure being test_empty_payoff_sample_raises[sdf-values]. Such a solution follows the spec's definition, so the test over-constrains it. The reference passes only because its _matrix() rejects empty input.",
    "Delete the pytest.param for 'sdf-values' (test_project.py line 811) so that the test requires ValueError only where the spec forces it, or first make the spec state that an empty payoff sample raises ValueError (project.html line 137) and keep the case.")

row("proj-new-tests-scale-equivariance", "2.6-spec",
    "grader/test_project.py test_min_variance_sdf_is_scale_equivariant (lines 824-836), test_min_sdf_std_is_scale_invariant (lines 839-845)",
    "PASS",
    f"{R10}: the 1e-7 tolerances are not over-constraining. I wrote three genuinely different correct implementations (scratch/make_variants.py): (a) centred matrix with matrix_rank and np.linalg.lstsq solves; (b) SVD of the centred matrix with a relative 1e-12 threshold and np.linalg.pinv; (c) np.cov(bias=True), cond guard 1e13 and np.linalg.solve. Each, with the reference, passed all 119 checks on seeds 0-49 (scratch/log_*.txt: 50 of 50 '119 passed' per variant, no FAILED lines). Margins (scratch/margins.py, seeds 0-49, fraction of the allowed tolerance used, worst over variants): intercept a up to 1.3e-5, weights b up to 3.7e-6, SDF values m up to 6.5e-6, min_sdf_std up to 2.0e-6. The minimum bound over seeds is 0.035 at unit scale, so the relative tolerance of min_sdf_std is not near zero. m64 (absolute singular tolerance) is killed at seed 0 by [tiny-units] (mutate2.log), so the tests do what they were added for.")

row("proj-tests-counted-119", "2.6-spec",
    "course/modules/AP/AP1/project.html line 139; grader/test_project.py (collect-only)",
    "PASS",
    f"{R10}: `QF_SEED={{0..9,49}} pytest --collect-only -q` on a staged copy (scratch/ref, reference.py as sdf_recovery.py): '119 tests collected' for seeds 0,1,2,3,4,5,6,7,8,9 and 49. Full run seed 49: '119 passed'. The in-browser run (page_smoke, below) reports 'All 119 tests pass'. project.html line 139 says 119.")

row("proj-line139-grading-claims", "2.6-spec", "course/modules/AP/AP1/project.html line 139 (Grading mode)",
    "PASS",
    f"{R10}: line 139 lists definitions, exact in-sample pricing, invariance to units and repackaging, projection and minimum second moment, minimum-variance SDF and variance bound, out-of-sample errors with training weights, invalid input, purity and imports. Each has named tests in test_project.py (checked by reading the file in full); all 119 checks pass on reference.py for seeds 0-49 and collect on 11 seeds.")

# ---------------- autograder ----------------
row("proj-graders-0-49", "2.6-autograder", "course/modules/AP/AP1/grader/ (reference.py, test_project.py, instance.py)",
    "PASS",
    f"{R10}: `.venv/bin/python tools/run_graders.py --unit AP1 --seeds 0-49`: 'run_graders AP1: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 (scratch/run_graders.log).")

row("proj-instances", "2.6-autograder", "course/modules/AP/AP1/grader/instance.py (make_instance); instance.py byte-identical since 33fd452",
    "PASS",
    f"{R10}: scratch/instances.py ran make_instance on seeds 0-19 and checked: probabilities positive and summing to one; SDF positive; N <= S-2; prices equal payoffs.T @ (probs*m_true) (no arbitrage by construction); prices >= 0.3; riskless payoff column identically 1 where flagged; train and test finite. All 20 valid. The first x* weight is distinct across all 20 seeds (20 of 20). Sizes vary: states 6-14, assets 3-6, train 120-360, test 60-240, riskless on 12 of 20 seeds.")

row("proj-share-probe-test", "2.6-autograder",
    "grader/test_project.py test_share_negative_uses_the_training_weights, test_share_negative_counts_test_rows",
    "PASS",
    f"{R10}: both pass on reference.py for seeds 0-49. Killed (scratch/mutate2.log): m26 and m25 and m35 by test_share_negative_uses_the_training_weights; m34 and m40 by test_share_negative_counts_test_rows; m38 by test_recover_sdf_summary_statistics.")

row("proj-messages-no-leak", "2.6-autograder", "grader/test_project.py must_raise (lines 64-70) and assertion messages",
    "PASS",
    f"{R10}: must_raise fails with '<condition>: the specification requires a ValueError.' The condition names the input, not an expected value. Assertion messages name the property ('x* must price every training payoff exactly in sample...'). m48 (generic ValueError text) is equivalent under this grader (mutant row below), so the messages are not compared.")

row("proj-dual-mode", "2.6-autograder", "course/modules/AP/AP1/project.html section#grader; tools/page_smoke.py",
    "PASS",
    f"{R10}: local run_graders seeds 0-49 PASS (pytest with -W error); in-browser: `tools/page_smoke.py --unit AP1` reports 'in-browser grader: All 119 tests pass on seed 166446775. (0.7 s)' and 'page_smoke modules/AP/AP1/project.html: PASS'.")

row("proj-mutation-run", "2.6-mutation", "ledgers/AP1/mutants/ (66 files); grader/test_project.py",
    "FAIL",
    f"{R10}: `.venv/bin/python tools/mutate_graders.py --unit AP1 --seeds 0-9` -> 'mutate_graders AP1: FAIL (63/66 killed)', exit 1 (scratch/mutate2.log). The 63 earlier mutants are all killed, including m62, m63 and m64 (round-9 survivors). Survivors: m65_x_star_casts_prices_to_the_payoff_dtype, m66_train_std_one_pass_variance, m67_min_sdf_std_uses_the_magnitude_of_its_mean. Each also survives the full 50-seed suite (scratch loop), so each is a FAIL row below. Earlier round-9 failures m62/m63/m64 are now KILLED.",
    "Kill m65, m66 and m67 (see their rows), then re-run `tools/mutate_graders.py --unit AP1 --seeds 0-9`.")

row("proj-mutant-m48-equivalent", "2.6-mutation",
    "ledgers/AP1/equivalent/m48_generic_value_error_messages.py; grader/reference.py",
    "PASS",
    f"{R10}: AST comparison (scratch/equiv.py, the ast module, dropping docstrings and the arguments of every raise): reference.py and m48 'AST EQUAL (25871 nodes)'. Because the spec no longer requires a message that names the condition (line 137 changed in 33fd452..ee0f984), the generic message is spec-conformant and m48 is not a fault. Not in the mutants list.")

row("proj-mutant-equivalence", "2.6-mutation", "ledgers/AP1/equivalent/ (m48)",
    "PASS",
    f"{R10}: the only file in ledgers/AP1/equivalent/ is m48_generic_value_error_messages.py, the AST proof above. Not counted in summary mutants.")

# ---------------- labs ----------------
row("proj-lab-project-1", "2.5-lab", "course/modules/AP/AP1/project.html #lab-AP1-project-1; tests/labs/AP1/lab-AP1-project-1.py",
    "PASS",
    f"{R10}: tools/run_labs.py --unit AP1: 'run_labs AP1: PASS (22/22)', exit 0; each run compares stdout with the page's expected output (labs.js rule); the twin is byte-identical since 33fd452 (git diff --quiet on tests/labs/AP1).")

row("proj-lab-project-2", "2.5-lab", "course/modules/AP/AP1/project.html #lab-AP1-project-2; tests/labs/AP1/lab-AP1-project-2.py",
    "PASS",
    f"{R10}: run_labs PASS 22/22 (as above). Twin byte-identical since 33fd452. page_smoke in-browser lab run: 'lab lab-AP1-project-2: 0.0 s' with no error.")

row("proj-lab-project-3", "2.5-lab", "course/modules/AP/AP1/project.html #lab-AP1-project-3 (expected block from line 228); tests/labs/AP1/lab-AP1-project-3.py",
    "PASS",
    f"{R10}: `python -I -W error lab-AP1-project-3.py` in a scratch dir with data/fx_monthly.csv copied from the checkout: exit 0, empty stderr; output matches the expected block line for line (payoffs, train/test dates, checksums 2989.0264134608 / 2992.6599604987, max |in-sample error| 2.0e-15, bp per currency, rms 270.0 bp, x* mean 0.9981 and s.d. 0.1824, share negative 0.0000 and min 0.0401, benchmark 20.1 bp). In Pyodide (headless Chromium, scratch/lab3_pyodide.py): the same lines, max |in-sample error| 9.5e-15, no page errors.")

row("proj-lab3-insample-quote", "2.2-numbers",
    "course/modules/AP/AP1/project.html line 231 (expected block) and line 342 (In-sample verification)",
    "PASS",
    f"{R10}: line 231 reads 'max |in-sample error|: 2.0e-15' = the CPython run above. Line 342 reads 'below 10^{{-13}}, which is rounding error'. Measured: CPython 2.0e-15 and Pyodide 9.5e-15 (both below 1e-13). Both measured this round.")

row("proj-run-labs", "2.5-labs", "tests/labs/AP1/*.py; course/modules/AP/AP1/*.html",
    "PASS",
    f"{R10}: tools/run_labs.py --unit AP1: 'run_labs AP1: PASS (22/22)', exit 0 (scratch/run_labs.log).")

# ---------------- data ----------------
row("proj-data-fx-licence", "2.8-data",
    "course/modules/AP/AP1/project.html Inputs (line 133) and Lab 3 (line 194); tools/data_sources.yaml fx_monthly licence; course/assets/data/market/MANIFEST.json licence_url",
    "PASS",
    f"{R10}: fetched https://www.federalreserve.gov/disclaimer.htm (HTTP 200, 85130 bytes, scratch/net/): the sentence 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' is present and matches the quote in data_sources.yaml and MANIFEST licence. about.htm (HTTP 200): 'Last Update: February 06, 2023', no terms of its own. The data_sources.yaml diff since 33fd452 changes only the check date to 2026-10-26.")

row("proj-data-fx-retrieved-date", "2.8-data",
    "course/modules/AP/AP1/project.html (retrieved 2026-10-19 on lines 133, 194, 340); MANIFEST.json fx_monthly retrieved",
    "PASS",
    f"{R10}: grep 'retrieved' in project.html: three occurrences, all '2026-10-19'; MANIFEST.json fx_monthly 'retrieved': '2026-10-19'. Not refreshed (BUILDER_RULES 6.6).")

row("proj-data-fx-rebuild", "2.8-data",
    "course/assets/data/market/fx_monthly.csv; MANIFEST.json fx_monthly; tools/fetch_data.py --fetch",
    "PASS",
    f"{R10}: `tools/fetch_data.py --fetch --only fx_monthly` in a scratch copy (git archive ee0f984, scratch/rebuild): 'built fx_monthly: 669 rows, 67392 bytes, 1971-01 to 2026-09', exit 0. The rebuilt file is byte-identical to the checkout's (cmp). sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e equals MANIFEST line 42. raw_sha256 is a provenance field of the download and is not compared.")

row("proj-fetch-data-check", "2.8-data", "course/assets/data/market/MANIFEST.json; tools/fetch_data.py --check",
    "PASS",
    f"{R10}: `tools/fetch_data.py --check`: 'fetch_data: 3 datasets, 0 problems', exit 0.")

# ---------------- rubric ----------------
row("proj-rubric-observable", "2.6-rubric",
    "course/modules/AP/AP1/project.html table#rubric (lines 256-267), C6 level 2 cell",
    "FAIL",
    f"{R10}: every level descriptor read against BUILDER_RULES 5.4 item 1. Observable throughout except one. C6 level 2 reads 'Has at least three of the five sections and some of the appendix, but misses an element of level 3.' 'Some of the appendix' has no threshold: one proof, two proofs and a sketch all read as 'some'. Under VERIFIER_RULES 2.6 a vague descriptor is a failure. The other descriptors name counts, sections, numbers or units (for example C4 level 3, 'every currency's test error'; C5 level 3, 'names at least three of'), or refer to level 3 by its own cells.",
    "Replace 'some of the appendix' in the C6 level 2 cell with a count, for example 'at least one of A1-A4'.")

row("proj-rubric-calibration", "2.6-rubric",
    "course/modules/AP/AP1/project.html #exemplar-a (lines 273-321), #exemplar-b (lines 323-385), table#rubric (lines 256-267)",
    "PASS",
    f"{R10}: scored each exemplar from the rubric text and the passages. Caveat: I printed the full articles, annotations included, in the same pass, so this is not a strictly blind score. Exemplar A: C1 2 (formula and existence, no assumptions), C2 2 (Pythagorean identity without orthogonality), C3 1 (A3 missing), C4 2 (A4 by analogy, one out-of-sample number), C5 2 (zero in-sample errors read as fit), C6 2 (three of five sections, no benchmark). Official 2,2,1,2,2,2: exact. Exemplar B: C1 4 (assumptions, positive definiteness, redundancy case), C2 4 (both directions, equality, the 1.15/0.383333 example), C3 4 (identity, convexity, Jensen, strictness, upward bias, riskless pinning), C4 4 (per-currency errors, RMS, benchmark, dates, x* shape), C5 3 (no check proposed), C6 4 (five sections, A1-A4, 597 words, 59-word Summary). Official 4,4,4,4,3,4: exact. Within one level on every criterion.")

row("proj-exemplar-word-counts", "2.6-rubric",
    "course/modules/AP/AP1/project.html #exemplar-b memo-text paragraphs (lines 327-357) and annotation line 381; #exemplar-a",
    "PASS",
    f"{R10}: scratch/words.py parses project.html (html.parser; annotations and the appendix excluded; verdict paragraphs excluded; entities decoded; split on whitespace). Exemplar B: Summary 59 + Data and method 170 + In-sample verification 55 + Out-of-sample pricing 172 + Limitations 141 = 597 (line 381 says 597). Exemplar A: Summary 51 + Data and method 32 + Out-of-sample pricing 20 = 103 (its annotation says 103). Both within 500-1200 (B) and the Summary at most 100 words (B: 59).")

row("proj-exemplar-b-math", "2.4-math",
    "course/modules/AP/AP1/project.html #exemplar-b Appendix A1-A4 (lines 367-374); the appendix is outside every 33fd452..ee0f984 hunk",
    "PASS",
    f"{R10}: A1 (positive definiteness from independence and pi>0; existence and uniqueness by invertibility), A2 (orthogonality both ways, equality iff eps = 0 using pi>0, the Example 5.1 x* = (1.15, 0.383333, -0.383333) is a lesson figure, L04 has it), A3 (identity; the supremum-of-affine convexity argument; Jensen with E[S^]=S; strict for N=1; the riskless pinning), A4 (feasibility and minimality with the variance decomposition). Numerical spot checks (scratch/proofs.py, 200 random samples, T=60, N=4): A3 identity worst |E_T[x* x]-p| = 8.9e-16; A4 feasibility worst error 1.4e-15 and the variance formula matches mv.var() to 1e-10. The argument of A3's bias step is standard and checked by hand.")

row("proj-exemplar-b-cross-refs", "2.9-structure",
    "course/modules/AP/AP1/project.html (every 'Lesson N, <kind> x.y' reference); course/modules/AP/AP1/L01-L07.html",
    "PASS",
    f"{R10}: each cited statement found by grep in the lesson pages: Proposition 2.1 (L04, L07), Definition 1.1 (L01-L07), Theorem 3.2 (L04, L05, L06), Theorem 3.3 (L07), Example 5.1 (L01, L04), Theorem 4.1 (L01, L03, L04, L05, L07), Definition 4.1 (L07), Proposition 2.2 (L01, L02, L03, L05), Proposition 2.3 (L05), Theorem 2.1 and 2.4 (L05), Proposition 1.2 (L02, L05). Figures: 0.99891 in L01, 80.2 in L07, 1.15 and 0.383333 in L04, 0.9996 in L05. Lesson 7 Lab 2 reports 80.2 basis points for ridge (80.2 appears in L07.html, as cited).")

row("proj-self-assessment-form", "2.6-rubric",
    "course/modules/AP/AP1/project.html #self-assessment (lines 387-391); course/assets/js/rubric.js (byte-identical since 33fd452)",
    "PASS",
    f"{R10}: scratch/form_drive.py (headless Chromium via Playwright, served from course/): 18 radio groups (3 targets x 6 criteria, 72 radios); chose a level in each group; clicked 'Reveal the official scoring'; 3 summaries rendered and the comparison table has 7 rows (header plus six criteria); exemplar A annotations visible; no console or page errors.")

row("proj-question-bank", "2.6-rubric", "course/modules/AP/AP1/project.html; BUILDER_RULES.md 5.4 item 4",
    "PASS",
    f"{R10}: BUILDER_RULES 5.4 item 4 applies to adversarial-review projects (IC defence, debate, referee report) only. AP1's project is an autograded module plus a rubric-graded report, so the question-bank rule is not triggered. No question bank is claimed on the page (grep for 'attack', 'angle', 'question bank', 'adversarial' finds none).")

# ---------------- citations ----------------
row("proj-cite-kalyuga2003expertise", "2.1-citation",
    "course/modules/AP/AP1/project.html #ladder claim (line 42; data-cite kalyuga2003expertise, data-locator Abstract); references/references.json",
    "PASS",
    f"{R10}: registry DOI 10.1207/s15326985ep3801_4. OpenAlex record fetched this round (HTTP 200, scratch/net/): abstract 'Instructional techniques that are highly effective with inexperienced learners can lose their effectiveness and even have negative consequences when used with more experienced learners.' Page text 'instructional techniques that are highly effective with inexperienced learners can lose their effectiveness, and even have negative consequences, with more experienced learners' matches. Scope: the claim is about instructional techniques, which the abstract states.")

row("proj-cite-tetzlaff2025cornerstone", "2.1-citation",
    "course/modules/AP/AP1/project.html #ladder claim (line 42; data-cite tetzlaff2025cornerstone, data-locator Abstract)",
    "PASS",
    f"{R10}: registry DOI 10.1016/j.learninstruc.2025.102142. Crossref (HTTP 200, scratch/net/): title 'A cornerstone of adaptivity – A meta-analysis of the expertise reversal effect', DOI matches, no abstract field. OpenAlex (HTTP 200): 'Of 1590 identified studies, 176 effect sizes from 60 experimental studies and a total of 5924 participants were finally included'; 'the expertise reversal effect is not symmetrical: providing novices with assistance has a stronger effect than withholding assistance from experts'; 'for younger students and some fields of study (i.e., humanities and language learning), the evidence for effectiveness is less clear'. Line 42 says 'a meta-analysis of 60 experimental studies (176 effect sizes) finds the effect, though asymmetric ... and less clear for younger students and for the humanities and language learning' = the abstract. The word 'independent' is absent from line 42 and the abstract does not support it. Scope: the meta-analysis is of 60 experimental studies in the expertise-reversal literature; the page's claim does not extend beyond it.")

row("proj-registry-used-by", "2.1-citation",
    "references/references.json (entries cochrane2005asset, delbaen1994general, duffie2001dynamic, hansen1991implications, harrison1979martingales, harrison1981martingales, kalyuga2003expertise, tetzlaff2025cornerstone); project.html data-cite keys",
    "PASS",
    f"{R10}: read references/references.json 'entries' with a script: used_by for each key that the AP1 project cites contains 'AP1' (cochrane2005asset ['AP1'], delbaen1994general ['AP1'], duffie2001dynamic ['AP1'], hansen1991implications ['AP1','AP3'], harrison1979martingales ['AP1'], harrison1981martingales ['AP1'], kalyuga2003expertise ['AP1','P0.2','S7'], tetzlaff2025cornerstone ['AP1','S7']).")

row("proj-verify-refs-live", "2.1-citation", "references/references.json (AP1 entries); tools/verify_refs.py --unit AP1",
    "PASS",
    f"{R10}: `.venv/bin/python tools/verify_refs.py --unit AP1`, final line 'live re-verification of AP1: 9 of 560 entries, 0 problems', exit 0 (scratch/verify_live.log). No network or proxy error this round.")

row("proj-verify-refs-offline", "2.1-citation", "references/references.json (integrity, all 560 entries)",
    "PASS",
    f"{R10}: `.venv/bin/python tools/verify_refs.py --offline` (no --unit: --unit is rejected with --offline by the tool): 'offline integrity: 560 entries, 0 problems', exit 0.")

row("proj-atlas-studios", "2.6-atlas-studios",
    "curriculum/curriculum.json AP1 entry (project: title 'SDF recovery', grading 'both'); curriculum/curriculum.json byte-identical since 33fd452",
    "PASS",
    f"{R10}: the AP1 entry reads project.title 'SDF recovery', grading 'both', tier 'M', hours 120 (module); the project table hours sum to 36 (proj-hours-estimate). Carried from the previous round (9) (curriculum/curriculum.json byte-identical since 33fd452): git diff --quiet 33fd452 ee0f984 -- curriculum/curriculum.json succeeded this round. The Atlas and studio rules do not apply to a module project.")

# ---------------- structure and commands ----------------
row("proj-check-projects", "2.6-structure", "tools/check_projects.py --unit AP1",
    "PASS", f"{R10}: 'check_projects AP1: PASS', exit 0 (scratch/check_projects.log).")

row("proj-check-pages", "2.9-structure", "course/modules/AP/AP1/*.html (tools/check_pages.py --unit AP1)",
    "PASS", f"{R10}: 'check_pages AP1: PASS', exit 0 (scratch/check_pages.log). The check covers the page contract, unique ids, alt text, SVG title/desc, banned strings (BUILDER_RULES 1.3-1.4) and local-only resources.")

row("proj-page-smoke", "2.9-structure", "tools/page_smoke.py --unit AP1 (project.html and index.html; labs; in-browser grader)",
    "PASS",
    f"{R10}: `.venv/bin/python tools/page_smoke.py --unit AP1`: 'in-browser grader: All 119 tests pass on seed 166446775. (0.7 s)', 'page_smoke modules/AP/AP1/project.html: PASS', 'page_smoke AP1: PASS', exit 0 (scratch/page_smoke.log). Labs 1-3 in Pyodide: 0.0 s each after preload.")

row("proj-banned-phrases", "2.9-structure", "course/modules/AP/AP1/project.html (BUILDER_RULES 1.3-1.4 and 2 rule 2)",
    "PASS", f"{R10}: tools/check_pages.py --unit AP1 (scratch/check_pages.log): 'check_pages AP1: PASS', which includes the banned-string check on visible prose of every AP1 page.")

row("proj-project-numbers", "2.2-numbers", "course/modules/AP/AP1/project.html (every quoted number in the spec, labs and exemplars)",
    "PASS",
    f"{R10}: Lab 3's printed values (CPython and Pyodide) match the expected block and exemplar B: checksums, 166 months each, per-currency bp, rms 270.0, mean 0.9981 and s.d. 0.1824, test min 0.0401, share 0.0000, benchmark 20.1. Lab 1 and Lab 2 pass run_labs. Spec numbers 119 (line 139) and 36 hours (line 33, hours table) match the tests and the table. Words 597 and 103 recounted (proj-exemplar-word-counts). The 2.0e-15 and 'below 10^-13' line are verified (proj-lab3-insample-quote). Numbers not re-derived this round: 0.99891 (a lesson figure, present in L01), 80.2 (L07 lesson figure).")

# ---------------- mutants ----------------
WITNESS = {
 "m65": "x_star_weights(X, p) with X an integer matrix (rng.integers(1, 9, (40, 3))) and p = (0.97, 0.99, 1.01): reference b = (0.00320, 0.02994, 0.01090); mutant b = (-0.04506, -0.08519, 0.13757); the mutant's b prices its own sample at (-0.97, -0.99, -0.01) (scratch/wit/witness.py).",
 "m66": "payoffs X = 1 + 1e-7 * N(0,1) (200 x 3), prices p = 1e8 * mean(X): reference train_std 5.65428, mutant 5.47723, relative difference 3.1e-2 (scratch/wit/witness66.py). The payoffs are finite and full rank under the reference's relative rule.",
 "m67": "min_sdf_std(Z, p, -0.97) with Z = normal(1, 0.2) 150 x 3: reference 15.79594, mutant 0.24055 (scratch/wit/witness.py). The mean argument is finite and the covariance is nonsingular.",
}
FIX = {
 "m65": "Add a test that calls x_star_weights and sdf_values on an integer-valued payoff sample (for example a 40 x 3 integer matrix) with fractional prices (0.97, 0.99, 1.01), and requires the weights to equal those of the same sample cast to float64 (computed in the test) to 1e-9.",
 "m66": "Add a recover_sdf test on a sample whose training x* has mean about 1e8 and standard deviation about 5 (payoffs 1 + 1e-7 * noise, prices 1e8 * mean payoff): require train_std to match a two-pass np.std of the training x* at rel_tol 1e-8.",
 "m67": "Add a test that min_sdf_std and min_variance_sdf with a negative finite mean (for example -0.97) match an independent computation of sqrt((p - v*mu)' Sigma^-1 (p - v*mu)) at the same v, in the same tolerances as the positive-mean tests.",
}

for m in mut:
    num = m["file"][:3]  # mNN
    i = f"proj-mutant-{num}"
    loc = f"ledgers/AP1/mutants/{m['file']}; grader/test_project.py"
    if m["killed_by"]:
        ev = (f"{R10}: tools/mutate_graders.py --unit AP1 --seeds 0-9 (scratch/mutate2.log): KILLED {m['file']} -> {m['killed_by']}. "
              f"Description: {m['desc']}")
        row(i, "2.6-mutation", loc, "PASS", ev)
    else:
        ev = (f"{R10}: tools/mutate_graders.py --unit AP1 --seeds 0-9 (scratch/mutate2.log): SURVIVED {m['file']} (no test fails on seeds 0-9). "
              f"Re-run on seeds 0-49 with the mutant as sdf_recovery.py (scratch/mut_*): 50 of 50 seeds pass, so it survives the full window. "
              f"Witness that it is not equivalent: {WITNESS[num]} Description: {m['desc']}")
        row(i, "2.6-mutation", loc, "FAIL", ev, FIX[num])

# ---------------- write the fragment ----------------
mutants_out = [{"description": m["desc"], "killed_by": (m["killed_by"] if m["killed_by"] else None)} for m in mut]
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
killed = sum(1 for m in mutants_out if m["killed_by"])
fail_ids = [r["id"] for r in rows if r["status"] != "PASS"]
verdict = "PASS" if counts["PASS"] == len(rows) and killed == len(mutants_out) else "FAIL"
ledger = {
    "unit": "AP1",
    "slice": "project",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent project-slice verifier, round 10 (did not build AP1; no shared context with its builders or earlier verifiers)",
    "pin": "ee0f984",
    "base": "33fd452 (carry-forward diff base, per the round-10 preamble); previous round (9) at 7216a6c",
    "previous_ledger": "ledgers/AP1/project.json as it stood in the round-10 checkout before this run: round 9, 113 rows, 107 PASS, 6 FAIL, 60/63 mutants.",
    "checkout": "/tmp/verify-ap1-r10-m (detached at ee0f984)",
    "scratch": "/tmp/ap1-r5/project-r10/ (logs, staged variants, witnesses, network captures, scripts)",
    "verified_at": "2026-10-27T01:20:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants_out,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 10. Commands re-run on Python 3.14.8 / numpy 2.4.6 / pytest 9.0.2: mutate_graders --unit AP1 --seeds 0-9 (63 of the 63 earlier mutants killed; "
        "the three new mutants m65-m67 survive, 63/66); run_graders --unit AP1 --seeds 0-49 (PASS 50/50, 119 checks); collect-only on seeds 0-9 and 49 (119 each); "
        "page_smoke --unit AP1 (in-browser grader: 119 pass on seed 166446775, 0.7 s; project.html PASS); run_labs --unit AP1 (22/22); check_projects, check_pages (PASS); "
        "verify_refs --unit AP1 (live: 9 of 560 entries, 0 problems) and --offline (560 entries, 0 problems; --unit is rejected with --offline by the tool); fetch_data --check (0 problems) and --fetch of fx_monthly in a scratch copy (byte-identical). "
        "Network: federalreserve.gov disclaimer and about pages, OpenAlex and Crossref records for both cited DOIs, fetched this round (HTTP 200). "
        "The three-implementation check of the scale tests (lstsq, pinv, np.cov+solve) passed on all 50 seeds; no over-constraint found there. "
        "The one over-constraint is test_empty_payoff_sample_raises[sdf-values] (FAIL). "
        "Carry-forward: only curriculum/curriculum.json (AP1 entry) and references/references.json are byte-identical since 33fd452, and rows citing them were re-read this round; project.html changed in 33fd452..ee0f984 (hunks at lines 42, 137, 139, 185, 231, 262, 342, 378-381), so every row whose subject is project.html was re-derived, not carried. "
        "Blind scoring caveat: the exemplar and annotation text were printed in the same pass as the scoring. "
        "Not checked: the self-assessment form was driven in Chromium but not for every criterion pair; the Pyodide value of Lab 3 was read from a headless run, not from a real browser session."
    ),
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": len(mutants_out),
        "mutants_killed": killed,
        "fail_ids": fail_ids,
    },
}
out = Path(f"{CK}/ledgers/AP1/project.json")
out.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants_out), "killed", killed, "verdict", verdict)
print("fail_ids", fail_ids)
