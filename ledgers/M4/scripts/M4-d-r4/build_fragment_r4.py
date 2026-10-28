"""Builds ledgers/M4/M4-d.json (round 4) from the verifier's row decisions and the mutation output file."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CHK = Path("/tmp/verifyB4-M4-d")
SCR = CHK / "ledgers/M4/scripts/M4-d-r4"
CARRY = "Carried from round 3 (course/modules/M/M4/grader/instance.py, reference.py and starter.py byte-identical since the previous pin): "
CARRY_R = "Carried from round 3 (course/modules/M/M4/grader/test_project.py lines 221-224 are outside every hunk of git diff aa3c26c 2657ab5; the rest of the file was re-run): "
CARRY_V = "Carried from round 3 (references/ and tools/ byte-identical since the previous pin, git diff --quiet aa3c26c 2657ab5 exit 0): "

R = []


def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix or "Re-verify this row or record the gap."
    R.append(d)


# ---- commands and gates
row("m4d-cmd-check-projects", "Project gate for M4", "course/modules/M/M4/project.html; tools/check_projects.py", "PASS",
    "`.venv/bin/python tools/check_projects.py --unit M4` on 2657ab5: 'check_projects M4: PASS'.")
row("m4d-cmd-check-pages-dag", "Page and DAG gates for M4", "course/modules/M/M4/*.html; tools/check_pages.py; tools/check_dag.py", "PASS",
    "`tools/check_pages.py --unit M4`: 'check_pages M4: PASS'; `tools/check_dag.py --unit M4`: 'check_dag M4: PASS'.")
row("m4d-cmd-run-labs", "Project twins and page labs", "tests/labs/M4/lab-M4-project-1.py, -2.py, -3.py; tools/run_labs.py", "PASS",
    "`tools/run_labs.py --unit M4 --page project`: 'run_labs M4: PASS (3/3)'. `python -I -W error` on each of the three twins exits 0; lab-M4-project-3 output saved at ledgers/M4/scripts/M4-d-r4/lab_project3_output.txt.")
row("m4d-lab-project-embedded-output", "Printed output in project.html matches a fresh run of the project labs", "course/modules/M/M4/project.html; tests/labs/M4/lab-M4-project-*.py", "PASS",
    "run_labs holds each page lab to its embedded expected block: 'run_labs M4: PASS (3/3)' on 2657ab5 (the twin changed only in its docstring; its code and output are unchanged).")
row("m4d-cmd-collect-count", "Test count on the page equals the real collect-only count", "course/modules/M/M4/project.html line 136; course/modules/M/M4/grader/test_project.py", "PASS",
    "Scratch copy with reference.py as tail_risk.py: `pytest --collect-only -q test_project.py` gives '84 tests collected'. The page says 'runs 84 checks'.")
row("m4d-cmd-run-graders-reference", "Reference solution passes the suite", "course/modules/M/M4/grader/reference.py; test_project.py", "PASS",
    "`QF_SEED=0 python -I -W error -m pytest -q -p no:cacheprovider --assert=plain test_project.py`: '83 passed, 1 skipped'; with QF_SEED=1093: '83 passed, 1 skipped'.")
row("m4d-cmd-starter-fails", "Starter is not a solution", "course/modules/M/M4/grader/starter.py", "PASS",
    "Starter as tail_risk.py, QF_SEED=0: '82 failed, 1 passed, 1 skipped'.")
row("m4d-cmd-lint-types", "ruff and mypy on the grader and twins", "course/modules/M/M4/grader/*.py; tests/labs/M4/lab-M4-project-*.py", "PASS",
    "`ruff check` on grader and the three project twins: 'All checks passed!'; `ruff format --check`: '7 files already formatted'; `mypy --no-incremental` (whole repo): 'Success: no issues found in 255 source files'. Outputs in ledgers/M4/scripts/M4-d-r4/.")
row("m4d-cmd-page-smoke", "page_smoke for project.html", "course/modules/M/M4/project.html", "PASS",
    "`tools/page_smoke.py --unit M4 --pages project.html --skip-sweep`: 'page_smoke M4: PASS', exit 0 (ledgers/M4/scripts/M4-d-r4/page_smoke_project_output.txt). Pyodide per-lab timing was not separately measured; see m4d-proj-platform-claims.")
row("m4d-cmd-verify-refs", "Registry gate", "references/references.json", "PASS",
    CARRY_V + "the registry gate result of round 3 stands.")

# ---- grader numbers and tolerance
row("m4d-grader-tolerance-sweep-numbers", "Tolerance-section numbers over seeds 0-1999 (instance nu)", "course/modules/M/M4/grader/test_project.py lines 33-38", "PASS",
    "ledgers/M4/scripts/M4-d-r4/sweep_r4.py run with the instance's own nu (make_instance(s)['nu'] for s = 0..1999): reference max relative error of the sample variance is 0.125934 at nu 5, 0.096731 at nu 6, 0.072813 at nu 7, 0.062417 at nu 8 (sweep_instance_nu_output.txt). These round to 0.126, 0.097, 0.073, 0.062; the page's unrounded maxima 0.1259, 0.0967, 0.0728, 0.0624 match; 0.30 / 0.1259 = 2.38, 'about 2.4'. The comment says the maxima are from make_instance, which fixes the basis. A sweep that forces nu to 5 for every seed gives 0.1409 (sweep_forced_nu_output.txt); that is a different population and the comment does not claim it.")
row("m4d-grader-missing-factor-claim", "Claim: a missing matched factor fails on every seed at nu 5 and 6, and on most at 7 and 8", "course/modules/M/M4/grader/test_project.py lines 36-38", "PASS",
    "Same instance-nu sweep, mutant m01_student_t_not_rescaled: fails 347/347 at nu 5, 317/317 at nu 6, 342/343 at nu 7 and 288/317 at nu 8 (the page's counts 347, 317, 342 of 343, 288 of 317 match the seed counts printed by the sweep). Inflations 5/3, 3/2, 7/5, 4/3 = 1.67, 1.50, 1.40, 1.33 (page: 1.67, 1.50, 1.40, 1.33).")
row("m4d-grader-seed-1093-nu3", "Claim: the reference fails the variance check at seed 1093 with nu = 3", "course/modules/M/M4/grader/test_project.py lines 31-33", "PASS",
    "make_instance(1093)['nu'] == 3 (scratch run). Reference relative error of the sample variance at seed 1093 is 1.0220, above 0.30 (ledgers/M4/scripts/M4-d-r4/nu34_and_seed_check.txt). The check itself is skipped at nu 3, as the comment says.")
row("m4d-grader-gaussian-tolerance", "Gaussian tolerance 0.10 accepts correct solutions", "course/modules/M/M4/grader/test_project.py TOL_GAUSSIAN_VARIANCE", "PASS",
    "Reference, Gaussian sample-variance relative error over seeds 0..1999: max 0.054770 at seed 1625 (ledgers/M4/scripts/M4-d-r4/gauss_2000_output.txt), below 0.10. The builder's alternatives pass the whole suite at seeds 0-49 (m4d-grader-alt-builder).")
row("m4d-grader-alt-verifier", "Three verifier alternative implementations pass the suite", "ledgers/M4/scripts/M4-d-r3/altA_chisq_sum_of_squares.py, altB_ceil_by_integer_division_float.py, altC_crout_cholesky_column_order.py", "PASS",
    "Re-run on 2657ab5 with ledgers/M4/scripts/M4-d-r4/run_alt_r4.sh over seeds 0-49, each as tail_risk.py in a fresh copy of test_project.py and instance.py: altA pass=50 fail=0; altB pass=50 fail=0; altC pass=50 fail=0.")
row("m4d-grader-alt-builder", "Builder's five alternative implementations pass the suite", "ledgers/M4/scripts/alt_1.py .. alt_5.py; ledgers/M4/scripts/run_alternatives.py", "PASS",
    "`python3 ledgers/M4/scripts/run_alternatives.py --seeds 0-49` on 2657ab5: reference.py PASS (50/50); alt_1..alt_5 each PASS (50/50 seeds). Output in run_alternatives_seeds0-49_output.txt.")
row("m4d-grader-overconstraint-nu3", "Suite does not over-constrain nu 3 and 4", "course/modules/M/M4/grader/test_project.py (Student-t variance test skip for nu < 5); project.html line 150", "PASS",
    "The variance test skips for NU < 5 (line 145, skip reason). Seeds 0-49 include nu 3 (seed 1) and nu 4 (seed 0) instances, and all six solutions (reference, alt_1..5) and altA..C pass on them.")
row("m4d-grader-mutants-existing", "Every existing mutant is killed", "ledgers/M4/mutants/*.py (60 files)", "FAIL",
    "`tools/mutate_graders.py --unit M4 --seeds 0-99`: 'mutate_graders M4: FAIL (56/60 killed)'. Survivors: m11_loss_sign_flipped (see m4d-grader-sign-mutant), m17_student_t_second_seed (disclosed, see m4d-grader-seed-sharing-mutant), v4_m01_loss_rounded_per_position (see m4d-r4-grader-v4-rounding-per-position), v4_m02_matched_factor_skipped_for_small_nu (see m4d-r4-grader-v4-matched-factor-nu34). All other 56 are killed.",
    "Fix the grader for the two FAIL survivors named in their rows; m17 is accepted under the disclosed stream-order gap.")
row("m4d-grader-new-mutants", "Verifier round-3 student-error mutants (v3_*) are killed", "ledgers/M4/mutants/v3_m02_round_half_up_by_truncation.py; v3_m03_loss_scaled_by_weights.py", "PASS",
    "mutate_graders M4 --seeds 0-99: v3_m02 KILLED by test_gaussian_losses_are_rounded_once_not_truncated (seed 0); v3_m03 KILLED by test_gaussian_loss_variance_matches_portfolio_covariance (seed 0).")
row("m4d-grader-equivalent-mutant", "Equivalence of ceil(0.99 n) in floats with the exact index", "ledgers/M4/scripts/M4-d-r3/make_variants.py", "UNVERIFIABLE",
    "Float math.ceil(0.99*n) equals (99n+99)//100 for every n from 1 to 200000 (0 differences, scratch run). No proof for all n. The mutant is not in the mutant list and the grader does not depend on it.",
    "Prove the equivalence for all n or drop the row.")
row("m4d-grader-sign-mutant", "Sign convention of the loss is tested or stated as untested", "course/modules/M/M4/project.html line 134 (binding list), line 139 (loss positive when the portfolio falls), line 150 (suite does not test the sign)", "FAIL",
    "m11_loss_sign_flipped SURVIVES seeds 0-99. Line 139 states the convention the mutant violates ('The loss is positive when the portfolio falls'), and line 134 lists it among conventions that are 'binding'. Line 134 excepts item 2 (the sign) and line 150 says the suite does not test it, so the disclosure is accurate, but the convention is still stated as a convention the grader should hold and it is not enforced. A sign flip is invisible to the loss distribution (R symmetric), so no distribution test can see it without a fixed stream order, which the page leaves open.",
    "Either fix the stream order on the page so the suite can compare a seeded sign, or state on line 134 that item 2 is not a graded convention, in the same sentence as the exception.")
row("m4d-grader-seed-sharing-mutant", "Families share a seed (stream order not fixed)", "course/modules/M/M4/grader/test_project.py; project.html lines 142 and 150", "PASS",
    "m17_student_t_second_seed SURVIVES seeds 0-99. The page says 'Which random stream order a family uses is not fixed here' (line 142) and 'The suite does not check the stream order' (line 150). No page sentence requires the two families to share a seed, so the survivor violates no stated behaviour.")
row("m4d-grader-one-chi-square-per-asset", "One chi-square per draw is disclosed as unchecked", "project.html line 150; mutant n02_one_chi_square_per_asset.py", "PASS",
    "n02 is KILLED at seeds 0-99 (by test_student_t_loss_variance_matches_matched_covariance, seed 84), so the variance test catches a per-asset variant as a side effect. The page's sentence says the suite does not check 'that the Student-t family uses one chi-square variable per draw', which is a direct check that the suite indeed lacks; the side effect is not claimed to be a check.")
row("m4d-grader-rounding-comment-number", "Comment numbers for truncation (about 2.7) and rounding (about 4.08)", "course/modules/M/M4/grader/test_project.py lines 220-224", "PASS",
    CARRY_R + "round 3 scratch computation (400000 seeded N(0,4) draws: int() truncation variance 2.709, round() 4.096 with SE about 0.009; 4 + 1/12 = 4.083) is not affected by the changes in the diff.")
row("m4d-grader-conditions-coverage", "Each named condition on the page has a test", "project.html lines 145-147 (conditions); test_project.py", "PASS",
    "Name-level mapping of each condition to a test: family rejected (test_unknown_family_is_rejected); gaussian with nu (test_gaussian_rejects_a_degrees_of_freedom); student_t without nu (test_student_t_requires_degrees_of_freedom); nu <= 2 (test_student_t_rejects_nu_at_or_below_two, test_matched_scale_rejects_nu_equal_to_two); n_draws <= 0 and non-int (test_draw_count_of_zero_or_less_is_rejected, test_draw_count_must_be_a_whole_number); positions (test_positions_must_be_whole_cents, test_positions_must_not_be_empty); cov shape, symmetry, PD (test_covariance_must_match_the_number_of_positions, test_covariance_must_be_symmetric, test_covariance_must_be_square_with_one_row_per_position, test_indefinite_covariance_is_rejected, test_negative_second_pivot_is_rejected); quantile empty and non-int (test_quantile_99_rejects_an_empty_list, test_quantile_99_rejects_non_whole_losses); accepted inputs (test_one_draw_is_accepted, test_gaussian_accepts_no_degrees_of_freedom, test_student_t_accepts_nu_just_above_two, test_one_position_with_positive_variance_is_accepted, test_quantile_99_of_one_loss_is_that_loss). Collect count 84 includes all of them.")
row("m4d-grader-messages-no-values", "Messages do not reveal instance values", "course/modules/M/M4/grader/test_project.py lines 45-61 and all check() calls", "PASS",
    "`grep -n 'f\"' test_project.py` returns no f-string. check() and expect_value_error() messages are literal strings; the module docstring states the rule (line 8).")
row("m4d-grader-instance-spec", "instance.py matches its spec", "course/modules/M/M4/grader/instance.py", "PASS",
    CARRY + "the round-2 spec check of instance.py stands (git diff --quiet aa3c26c 2657ab5 on instance.py, reference.py, starter.py exits 0).")

# ---- project page prose and appendix
row("m4d-proj-matrix-and-moments", "Matrix and moment statements on the page", "course/modules/M/M4/project.html Appendix A1 to A4 (the 'Moments and the matched scale' passage)", "PASS",
    "Re-derived: E[W^-1] = Gamma(nu/2-1)/(2 Gamma(nu/2)) = 1/(nu-2) (substitute w = 2u: 2^(nu/2-1) Gamma(nu/2-1) / (2^(nu/2) Gamma(nu/2))); E[W^-2] = 1/((nu-2)(nu-4)) for nu > 4; Var(t) = nu E[1/W] = nu/(nu-2); integrand exponents nu/2-2 and nu/2-3 give the divergence stated for nu <= 2 and nu <= 4; E[RR^T] = E[(nu-2)/W] L E[ZZ^T] L^T = Sigma. Verified line by line against project.html Appendix passage (ledgers/M4/scripts/M4-d-r4 notes).")
row("m4d-proj-sign-untested-claim", "Claim: a sign error leaves the loss distribution unchanged", "course/modules/M/M4/project.html line 150", "PASS",
    "R = LZ and R = sqrt((nu-2)/W) LZ with Z symmetric and W independent of Z, so -R has the same law as R; the claim follows.")
row("m4d-proj-only-when-1-6", "Claim that the Student-t check runs only for nu of 5 or more", "project.html line 150; grader test_project.py line 145", "PASS",
    "The skip in test_student_t_loss_variance_matches_matched_covariance (NU < MIN_NU_FOR_T_VARIANCE_CHECK = 5) matches the page statement; the page lists nu 3 and 4 as skipped.")
row("m4d-proj-hours", "Hours table sums to 30 and matches data-hours-project", "course/modules/M/M4/project.html Time budget table; hub index.html", "PASS",
    "Rows 2 + 2 + 12 + 8 + 4 + 2 = 30; data-hours-project=\"30\" in project.html and index.html; hub lessons 10 x 9 = 90 plus project 30 = 120 (plan total). Pace not judged (architect ruling).")
row("m4d-proj-platform-claims", "Browser run limit and runtime claims", "project.html line 134 (120 seconds)", "UNVERIFIABLE",
    "The 120-second browser run limit was not measured in a browser this round.", "Measure in the browser or record the gap.")
row("m4d-proj-conditions-named", "Contract notes name exactly the conditions the suite does not test", "project.html lines 134 and 150", "FAIL",
    "Line 150 names the nu 3/4 variance, the sign, the stream order and the one-chi-square-per-draw item. It does not name the loss rounding: v4_m01_loss_rounded_per_position (one cent per position rounding) SURVIVES seeds 0-99, and the page states the loss is 'rounded once' (line 139) and lists the rounding of each loss as graded (line 136).",
    "Add the per-position rounding to the contract notes, or add a test that catches it (see m4d-r4-grader-v4-rounding-per-position).")
row("m4d-proj-conventions-binding-claim", "The conventions are called binding except three items the suite does not test", "project.html line 134", "FAIL",
    "Line 134: 'The conventions ... are binding, except three items the suite does not test: the sign of the loss (item 2), the stream order and the one chi-square variable per draw (item 5).' The Student-t variance at nu 3 and 4, which line 150 says the suite does not check, is item 1 (the model) and is missing from the exception list. Witnesses: m01_student_t_not_rescaled passes the whole suite at QF_SEED=1093 (nu 3) and QF_SEED=0 (nu 4); v4_m02 (matched factor skipped for nu 3 and 4) survives seeds 0-99. The per-position rounding belongs to item 2 (the loss) and is also not excepted.",
    "Extend the exception list at line 134 with the nu 3 and 4 Student-t variance and the per-position rounding, or add the test.")
row("m4d-proj-test-comment-measure", "Grader comment about the variance check fails on every seed", "course/modules/M/M4/grader/test_project.py lines 36-38", "PASS",
    "Verified by the instance-nu sweep (m4d-grader-missing-factor-claim): 347/347, 317/317, 342/343, 288/317.")
row("m4d-proj-process-words", "No process words in learner text", "course/modules/M/M4/project.html", "PASS",
    "Scan of the extracted page text (ledgers/M4/scripts/M4-d-r4/ scratch) for build, builder, verifier, round, REQUESTS, unit report: no process word in prose; 'round' occurs only as the Python function round() and in 'rounded'.")
row("m4d-proj-scope-words", "Scope words are backed", "course/modules/M/M4/project.html (every, only, same, any, always)", "PASS",
    "Each scope word checked in context: 'Every input is SIMULATED' (instance.py docstring; labs have no data file); 'only' in 'defined for nu > 2 only' (matched_scale definition); 'same covariance matrix' (the Student-t and Gaussian models share COV in the instance); 'every seed tested' backed by the instance-nu sweep; 'every nonzero w' is the definition of positive definite; 'every element the report shows' is the scoring rule. No 'always' or 'all' appears on the project page outside the exemplars, where Exemplar A's 'always riskier' is flagged by its own annotation.")
row("m4d-exemplar-a-scores", "Exemplar A scores and annotations", "course/modules/M/M4/project.html rubric exemplars (Exemplar A)", "PASS",
    "Each annotation checked against the rubric cell text: C1 2 (formula and hypothesis, no integral; level 2 text), C2 2 (matched factor stated, independence and Gamma integral missing; level 2 text; not annotated), C3 2 (index stated without derivation; level 2 text), C4 2 ('about 2,100 dollars' is a number Lab 3 does not print; level 2 text), C5 2 (four headings, two limitations; level 2 text). Body length 100 words counting headings, as the annotation says.")
row("m4d-exemplar-b-scores", "Exemplar B scores and annotations", "course/modules/M/M4/project.html rubric exemplars (Exemplar B)", "PASS",
    "C1 4 and C2 4: every step re-derived (Gamma integrals, divergence orders, E[RR^T] = Sigma; 1.0447 ratio, 4.5 % of 1). C3 4: index derivation from F_n and the 213213 / 210946 / 243004 values check. C4 4: 2267 = 213213 - 210946; 32058 = 243004 - 210946; 32058/210946 = 15.2 % above the sampled Gaussian loss (basis stated). C5 3 with the miss at level 4 (smallest inflation not stated), as the page says.")
row("m4d-exemplar-intro-numbers", "Numbers in the exemplar introduction and passages", "course/modules/M/M4/project.html exemplar introduction", "PASS",
    "The introduction claims that the exemplars' numbers come from Lab 1 or Lab 3 or are formulas of the inputs, except where annotated. Exemplar B's numbers were each recomputed (see m4d-exemplar-b-scores); Exemplar A's approximate dollar figure is annotated as not printed by Lab 3.")
row("m4d-rubric-structure", "Rubric has five criteria with four levels", "course/modules/M/M4/project.html rubric table", "PASS",
    "Rubric rows C1 to C5 each have four level cells (Exemplary, Proficient, Developing, Beginning) in the page text (lines 222-226).")
row("m4d-lab1-step2-comment", "Worked example step comment", "tests/labs/M4/lab-M4-project-1.py lines 37-41; project.html", "PASS",
    "sqrt(NU/W) times sqrt((NU-2)/NU) equals sqrt((NU-2)/W), as the comment states; code scale = sqrt((NU-2)/chi_square) with chi_square = gammavariate(NU/2, 2.0) (shape NU/2, scale 2) matches the comment.")
row("m4d-lab1-hypothesis-numbers", "Worked example hypothesis numbers", "project.html 'Stated before running' (line 22); lab-M4-project-1.py", "PASS",
    "8.4e9 cents squared; matched factor 0.6; index ceil(0.99 * 20000) = 19800 (lab output 19800); both sample variances within 5 % of target (1.0017 and 1.0447 printed); 243004 / 210946 = 1.152 (scratch: 1.15197).")
row("m4d-lab3-closed-forms", "Lab 3 closed forms", "tests/labs/M4/lab-M4-project-3.py", "PASS",
    "Recomputed: target 8400000000.0; sd 91651.5139; z = 2.3263478740; round(z*sd) = 213213 (213213.30); factors (nu-2)/nu = 1/3, 1/2, 0.6, 0.75 and inflations 3, 2, 1.666667, 1.333333 for nu = 3, 4, 5, 8; index 99/100/99 at n = 100/101 and 19788 at n = 19987 (lab output saved).")
row("m4d-proj-numbers-prose", "Numbers in project prose recomputed", "project.html (Lab 1 comment, Lab 3 text, grader comments, exemplars)", "PASS",
    "Recomputed in scratch: 243004/210946 = 1.15197 ('1.152'); 1.0447 is 4.47 % from 1 ('about 4.5 %'); 0.30/0.1259 = 2.38; nu/(nu-2) = 1.6667, 1.5, 1.4, 1.3333; P(|Z| > 10) = 1.5240e-23 (card and L10 agree).")
row("m4d-proj-lab3-docstring", "Lab 3 docstring claim about rounding", "tests/labs/M4/lab-M4-project-3.py lines 1-8 and 25", "PASS",
    "The only round() call in the twin is round(z99 * sd) at line 25, the parametric loss; every other number is printed with a format specifier. The docstring says so.")

# ---- cards
row("m4d-cards-inventory", "cards.json inventory", "course/modules/M/M4/cards.json", "PASS",
    "json load: 180 cards (164 grade T, 16 grade C). Round 3 read 172; the file now has 180.")
row("m4d-cards-duplicate", "Duplicate scan", "course/modules/M/M4/cards.json", "PASS",
    "180 ids, 180 unique (python set).")
row("m4d-cards-locators", "Card locators name a lesson and a locator that exists", "course/modules/M/M4/cards.json", "UNVERIFIABLE",
    "Locators were checked only for the nine new cards (M4-c173..c180) and the changed cards c095 and c157 (see the card rows below). The other cards were not checked this round.",
    "Check each remaining locator against its lesson.")
row("m4d-cards-numbers", "Card numbers appear in their lesson", "course/modules/M/M4/cards.json", "UNVERIFIABLE",
    "Checked for M4-c098 (1.669114, 1.666667, 0.001469 in L06 and lab output), M4-c157 (0.063451, 1.5240e-23 in L10 line 197-198) and M4-c095 (5/3 in L06). The remaining cards were not checked.",
    "Check each card number against its lesson text.")
row("m4d-cards-c098-seed", "Card M4-c098 seed", "course/modules/M/M4/cards.json M4-c098; tests/labs/M4/lab-M4-L06-1.py lines 5 and 18", "PASS",
    "The card says seed '20260602 + nu'. The twin's Part A uses random.Random(SEED + nu) with SEED = 20260602 (line 18), and the doc says so (line 5); N_DRAWS = 100000 (line 19) matches the card's n = 100000.")
row("m4d-cards-c098-rounding", "Card M4-c098 relative error 0.001469 is computed from unrounded values", "course/modules/M/M4/cards.json M4-c098; tests/labs/M4/lab-M4-L06-1.py; course/modules/M/M4/L06.html", "PASS",
    "The twin computes (variance - exact) / exact from unrounded floats (run output: 'nu 5 relative_error 0.001469'); the card says so.")
row("m4d-cards-c097", "Card M4-c097 statement (Proposition 1.5 in L06)", "course/modules/M/M4/cards.json M4-c097; L06 Proposition 1.5", "PASS",
    "L06 Proposition 1.5 (assuming Assumption 1): if X ~ N(mu, sigma^2) then E[X] = mu and Var(X) = sigma^2. The card matches.")
row("m4d-cards-c073", "Card M4-c073 statement (Example 1.7 in L05)", "course/modules/M/M4/cards.json M4-c073; L05 Example 1.7", "PASS",
    "L05 Example 1.7 (sigma_X > 0, a > 0, Y = aX + b): Cov = a Var(X), sigma_Y = a sigma_X, rho = 1. The card matches.")
row("m4d-cards-grade-basis", "Every non-T card has a grade and every C card has a basis", "course/modules/M/M4/cards.json", "PASS",
    "All 180 cards have a grade key; the 16 C cards each have a basis; M4-c164 now has grade T (the round-3 gap is closed).")
row("m4d-cards-sentence-level", "Sentence-level read of every card against its lesson", "course/modules/M/M4/cards.json", "UNVERIFIABLE",
    "Not completed this round for all 180 cards. The changed and new cards were read against their lesson text (rows below).",
    "Complete the sentence-level read of the remaining cards against the current lesson text.")
row("m4d-card-c095-changed", "Changed card M4-c095 ('nu > 2') agrees with L06 Proposition 2.6", "course/modules/M/M4/cards.json M4-c095; L06 Proposition 2.6", "PASS",
    "L06 Proposition 2.6: assuming Assumption 1, for nu a positive integer, if nu > 2 then E[t] = 0 and Var(t) = nu/(nu-2). The card's hypothesis nu > 2 matches; 5/3 at nu = 5 is in L06.")
row("m4d-card-c157-changed", "Changed card M4-c157 agrees with L10", "course/modules/M/M4/cards.json M4-c157; L10 Definition 1.1, Lab 1 Part A", "PASS",
    "L10 Definition 1.1 is the decay definition; P(|C| > 10) = (2/pi) arctan(0.1) = 0.063451 (scratch) and 1.5240e-23 for the normal (scratch: 1.5239706e-23); 1/0.063451 = 15.76, 'about 1 draw in 16' (L10 line 230). The card's text matches the current lesson.")
row("m4d-card-c178-sample-mean", "Card M4-c178 defines the sample mean (cited to L09 Section 1)", "course/modules/M/M4/cards.json M4-c178; course/modules/M/M4/L09.html Section 1", "FAIL",
    "The card says 'The sum of the first n variables divided by n (Section 1)'. The L09 Section 1 text (lines 21-32 of the lesson) never defines the sample mean X-bar_n or the sum S_n: X-bar_n first appears in the Proposition 1.2 statement and S_n in its proof without a definition. The formula appears only implicitly in the proof ('E[X-bar_n] = (1/n) sum E[X_i]').",
    "Add the definition of X-bar_n and S_n to L09 Section 1 (lesson owner), or change the card's locator to the proof line that uses (1/n) sum.")
row("m4d-cards-new-others", "New cards M4-c173, c174, c175, c176, c177, c179, c180 agree with their lessons", "course/modules/M/M4/cards.json; L01 Section 3, L06 Remark 2.2, L08 Sections 1 and 3, L09 Sections 1 and 2, L10 Section 1", "PASS",
    "c173: L01 infimum sentence (§3) matches. c174: L06 Remark 2.2 states P(X in A, Y in B) = P(X in A) P(Y in B) for all A, B: matches. c175: L08 §1 after Proposition 1.6 defines positive definite as w^T M w > 0 for every nonzero w: matches. c176: L08 §3 sample covariance with divisor n-1: matches. c177: L09 §1 'identically distributed ... 0 < sigma^2 < infinity' (raw HTML): matches. c179: L09 §2 i.i.d. factorization and each X_i has the law of X: matches. c180: L10 §1 'light-tailed' is 'not heavy-tailed (Section 1, after Definition 1.1)': matches.")
row("m4d-dag-concepts", "Concepts used within the prerequisite closure", "course/modules/M/M4/*.html; check_dag", "UNVERIFIABLE",
    "check_dag M4 PASS (m4d-cmd-check-pages-dag). The per-concept closure check (no concept used outside AC1, S0, S2 and their closure) was not redone this round for the project page.",
    "Redo the per-concept closure check for project.html.")
row("m4d-dag-gamma-function", "Gamma function used before definition", "course/modules/M/M4/project.html Assumption 1", "PASS",
    "Assumption 1 (a) defines Gamma(x) = integral of t^(x-1) e^(-t) inline before the density in (b) and before the appendix uses it. Gamma is not a curriculum concept.")
row("m4d-reading-attribution", "Attributions and theorem numbers match what was read", "course/modules/M/M4/project.html (appendix, source note)", "PASS",
    "The page's source note says 'This page attributes no statement to it, and no passage locator from it has been read' (project.html source note). Internal references traced: Lesson 6 Definition 2.1 (L06 line 47), Lesson 6 Proposition 1.5, Lesson 6 Proposition 2.6, Appendix A3, Lesson 1 quantile. No external source was opened.")

# ---- new rows for round 4
row("m4d-r4-grader-v4-rounding-per-position", "Loss rounded once (not per position)", "course/modules/M/M4/grader/test_project.py lines 221-229; project.html line 139", "FAIL",
    "New mutant v4_m01_loss_rounded_per_position (rounds each position's contribution, then sums) SURVIVES seeds 0-99. Witness: two positions [1000, 1000], cov [[4e-4,1e-4],[1e-4,9e-4]], 20000 seeded Gaussian draws: 5083 differ from the round-once reference, by 1 cent at most; the suite passes (83 passed, 1 skipped at QF_SEED=0). The only rounding test uses one position, where both rules agree.",
    "Add a rounding-once test with two positions whose expected value the test can compute (for example, a seed-independent check of the rounding rule on a fixed unrounded sum), or state on the page that the per-position rounding is not tested.")
row("m4d-r4-grader-v4-matched-factor-nu34", "Matched factor applied at nu 3 and 4", "course/modules/M/M4/grader/test_project.py (variance test skipped for nu < 5); project.html line 150 and line 134", "FAIL",
    "v4_m02_matched_factor_skipped_for_small_nu SURVIVES seeds 0-99. The unscaled m01 also passes the whole suite at QF_SEED=1093 (nu 3) and QF_SEED=0 (nu 4). The gap is disclosed on line 150, but line 134 calls the conventions binding except three items that omit it (see m4d-proj-conventions-binding-claim).",
    "Add nu 3 and 4 to the exception list on line 134, or add a test that is not the variance test (the fourth moment is infinite at nu 3 and 4, so use a rank or tail test the page states).")
row("m4d-r4-grader-v4-sign-folded", "Absolute value of the return (gains recorded as positive losses)", "ledgers/M4/mutants/v4_m03_loss_sign_folded.py", "PASS",
    "KILLED at seed 0 by test_gaussian_loss_variance_matches_portfolio_covariance (mutate_graders M4 --seeds 0-99 output).")
row("m4d-r4-grader-no-print", "No function prints (project.html line 134 'No function prints or warns')", "course/modules/M/M4/project.html line 134; grader test_project.py (no capsys test)", "FAIL",
    "Reference plus appended print('debug: computing') passes the whole suite: '83 passed, 1 skipped' at QF_SEED=0 with -W error (ledgers/M4/scripts/M4-d-r4/print_mutant_check.txt). test_project.py contains no capsys and no output check. Warnings are caught by -W error, printing is not.",
    "Add a test that calls each function with capsys and asserts no output, which the page states; or remove 'prints' from the constraint.")
row("m4d-r4-scope-words-cards", "Scope words in new card text", "course/modules/M/M4/cards.json M4-c157, M4-c180", "PASS",
    "M4-c157 'Not by itself' and 'heavy tail describes the decay' are backed by L10 Definition 1.1 and the printed 0.063451 versus 1.5240e-23; M4-c180 'not heavy-tailed' is the definition.")
row("m4d-r4-lab-project-3-rounding-claim", "Lab 3 docstring: every number is unrounded except the parametric loss", "tests/labs/M4/lab-M4-project-3.py", "PASS",
    "The docstring (lines 4-5) says the one rounded value in the code is the parametric 99% loss, rounded once with round(). Line 25 is the only round() call. The printed target and sd use format specifiers, which the docstring calls display rounding.")

# ---- mutants from the mutation output
mut_lines = (SCR / "mutate_graders_M4_seeds0-99_output.txt").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"(KILLED|SURVIVED) (\S+?)\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    entry = {"id": name, "description": desc}
    if status == "KILLED":
        entry["killed_by"] = killer
    else:
        entry["survived"] = True
    mutants.append(entry)

fragment = {
    "unit": "M4",
    "slice": "M4-d",
    "round": 4,
    "round_note": "Round 4 of M4-d. Delta from the round-3 pin aa3c26c to 2657ab5: project.html (exemplar A/B annotations, conventions carve-out, rounding claims), grader/test_project.py (new tests, changed comments), cards.json (180 cards: c157, c095, c164 changed; c173-c180 added), tests/labs/M4/lab-M4-project-3.py (docstring), and mutants d3s01-d3s10 added. The lesson files L01-L10 changed and are not owned by this slice; cards citing them were re-read against the current text. New mutants v4_m01-v4_m03 are the verifier's round-4 student-error mutants. Carried rows are marked 'Carried from round 3'.",
    "verifier": "Claude Haiku 5.5, independent verifier, round 4 (did not build M4)",
    "pin": "2657ab5 (detached checkout /tmp/verifyB4-M4-d)",
    "base": "none",
    "checkout": "/tmp/verifyB4-M4-d",
    "scratch": "/tmp/M4-v/d/",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Mutants: all 60 files in ledgers/M4/mutants run at seeds 0-99 (56 killed). Survivors: m11 (FAIL row), m17 (accepted under the disclosed stream-order gap), v4_m01 (FAIL row), v4_m02 (FAIL row). Alternatives: builder alt_1..alt_5 and round-3 altA..altC pass seeds 0-49. Gates run: check_projects, check_pages, check_dag (M4), run_labs (project page), collect-only (84), reference/starter, ruff, mypy (repo), page_smoke (project.html). Not checked: sentence-level read of all 180 cards, per-concept DAG closure, the 120-second browser limit, the registry live run (references and tools unchanged since aa3c26c, so the offline result stands). Lesson-owner findings outside this slice: L09 Section 1 uses X-bar_n and S_n without defining them (basis of M4-c178). Mutant hygiene: n01-n04 docstrings are the reference's docstring, not a one-line description of the error.",
    "summary": {},
}
fragment["summary"] = {
    "rows": len(R),
    "pass": sum(1 for r in R if r["status"] == "PASS"),
    "fail": sum(1 for r in R if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in R if r["status"] == "UNVERIFIABLE"),
    "mutants": len(mutants),
    "mutants_killed": sum(1 for m in mutants if m.get("killed_by")),
}
out = CHK / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"])
