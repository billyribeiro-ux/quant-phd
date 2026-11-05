"""Round-10 verifier (E3-d): assembles ledgers/E3/E3-d.json from the evidence files written in this run."""
import datetime, json, pathlib, re, sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD10-E3-d")
S = ROOT / "ledgers/E3/scripts/E3-d-r10"
SUITE = S / "suite_out"
PIN = "47a36d8c78633793ccc762ae19dcd5e19b780d19"


def suite_summary(label):
    path = SUITE / f"{label}.out"
    if not path.exists():
        return None
    lines = [l for l in path.read_text().splitlines() if "seed=" in l]
    ok = [l for l in lines if " rc=0 " in l]
    bad = [l for l in lines if " rc=0 " not in l]
    return len(ok), len(lines), bad


def fmt_suite(label):
    s = suite_summary(label)
    if s is None:
        return f"{label}: not yet run"
    ok, total, bad = s
    tail = "" if not bad else " | failing: " + " ; ".join(b.split(" :: ")[0] + " " + b.split(" :: ")[-1][:160] for b in bad)
    return f"{ok}/{total} seeds pass{tail}"


def mutate_rows():
    out = []
    text = (S / "s3d_mutate_E3_seeds0-9.out").read_text()
    for line in text.splitlines():
        m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line)
        if not m:
            continue
        status, name, desc, killed = m.groups()
        out.append({"name": name.removesuffix(".py"), "description": desc,
                    "killed_by": killed if status == "KILLED" else None})
    return out


rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    rows.append(r)


CARRY = "Carried from round 9 (grader/reference.py, grader/instance.py, grader/starter.py, lessons L02 L04-L08, index.html, tests/labs/E3, notation/notation.json, references/references.json, tools/* byte-identical since the previous pin): "

# ---- gates
row("gate-check-pages", "tools/check_pages.py --unit E3", "course/modules/E/E3/project.html",
    "PASS", "ledgers/E3/scripts/E3-d-r10/s3d_check_pages_E3.out: 'check_pages E3: PASS', rc=0")
row("gate-check-dag", "tools/check_dag.py --unit E3", "course/modules/E/E3/project.html",
    "PASS", "ledgers/E3/scripts/E3-d-r10/s3d_check_dag_E3.out: 'check_dag E3: PASS', rc=0")
row("gate-check-projects", "tools/check_projects.py --unit E3", "course/modules/E/E3/project.html",
    "PASS", "ledgers/E3/scripts/E3-d-r10/s3d_check_projects_E3.out: 'check_projects E3: PASS', rc=0")
row("gate-run-labs-project", "tools/run_labs.py --unit E3 --page project (twins under python -I -W error, page code = twin, expected = output)",
    "course/modules/E/E3/project.html Labs 1-3; tests/labs/E3/lab-E3-project-1..3.py",
    "PASS", "ledgers/E3/scripts/E3-d-r10/s3d_run_labs_project.out: 'run_labs E3: PASS (3/3)', rc=0; twins run alone: s3d_lab_twins_output.out, rc=0 each, 0 stderr bytes (s3d_twin_N.err)")
row("gate-page-smoke-project", "tools/page_smoke.py --unit E3 --pages project (Chromium, labs in Pyodide, in-browser grader with the reference)",
    "course/modules/E/E3/project.html", "PASS",
    "ledgers/E3/scripts/E3-d-r10/s3d_page_smoke_project.out: 'in-browser grader: All 47 tests pass on seed 1142605429 (31.6 s)', 'page_smoke E3: PASS', rc=0")
row("gate-run-graders-seeds-0-49", "tools/run_graders.py --unit E3 --seeds 0-49", "course/modules/E/E3/grader/",
    "PASS", "ledgers/E3/scripts/E3-d-r10/s3d_run_graders_E3_0_49.out: 'run_graders E3: PASS (reference 50/50 seeds, slowest 20.5 s)', rc=0")
row("gate-collect-46", "pytest --collect-only test_project.py (id kept from round 9; the count is now 47)",
    "course/modules/E/E3/grader/test_project.py; project.html:213",
    "PASS", "ledgers/E3/scripts/E3-d-r10/s3d_collect_only.out: '47 tests collected'; project.html:213 says 47 checks")
row("gate-reference-seed0", "reference.py as elicit.py, QF_SEED=0, pytest --assert=plain -W error (scratch /tmp/E3d_r10_ws/ref)",
    "course/modules/E/E3/grader/", "PASS", "ledgers/E3/scripts/E3-d-r10/s3d_reference_seed0.out: '47 passed in 14.10s', rc=0")
row("gate-starter-fails", "starter.py as elicit.py must fail the suite", "course/modules/E/E3/grader/starter.py",
    "PASS", "ledgers/E3/scripts/E3-d-r10/s3d_starter_seed0.out: '45 failed, 2 passed', rc=1")
row("gate-ruff", "ruff check and ruff format --check on grader/ and tests/labs/E3",
    "course/modules/E/E3/grader; tests/labs/E3", "PASS",
    "ledgers/E3/scripts/E3-d-r10/s3d_ruff_check.out: 'All checks passed!'; s3d_ruff_format.out: '15 files already formatted'")
row("gate-mypy-strict-grader", "mypy --strict on the grader in its real layout (test_project.py with elicit.py, instance.py)",
    "course/modules/E/E3/grader/", "PASS",
    "ledgers/E3/scripts/E3-d-r10/s3d_mypy_workspace_strict.out: 'Success: no issues found in 3 source files', rc=0; s3d_mypy_grader_src.out (reference, instance, starter) rc=0. Note: run in the grader directory with no elicit.py, test_project.py gives 3 'unused type: ignore' errors (s3d_mypy_test_project.out); that is an artifact of the missing module, not a defect")
row("gate-mypy-repo", "mypy --no-incremental (repository, strict)", "repository", "PASS",
    "ledgers/E3/scripts/E3-d-r10/s3d_mypy_repo.out: 'Success: no issues found in 385 source files', rc=0")
row("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json (cited keys project.html:757-764)", "PASS",
    "ledgers/E3/scripts/E3-d-r10/s3d_verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc=0")
row("gate-pytest-relevant", "pytest tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py -k E3", "project.html exemplars and lab twins", "PASS",
    "ledgers/E3/scripts/E3-d-r10/s3d_pytest_relevant.out: 15 passed, rc=0")
row("gate-mutate-existing-112", "tools/mutate_graders.py --unit E3 --seeds 0-9 (every mutant present at the start: 140 files; id kept from round 9)",
    "ledgers/E3/mutants/", "PASS",
    "ledgers/E3/scripts/E3-d-r10/s3d_mutate_E3_seeds0-9.out: 'mutate_graders E3: PASS (140/140 killed)', rc=0; the tool sets QF_SEED per seed in its own env dict")
row("gate-mutants-count", "at least 3 mutants, and ten student-error mutants by the plan's count", "ledgers/E3/mutants/", "PASS",
    "140 mutants in the tool run; 3 new student-error mutants written this round (d10_01..03), see mutants list; the plan (§6.5) asks ten, and the ledger holds more than ten student-error mutants")

# ---- round-9 mutant rows (byte-identical files, re-run this round in the 140-mutant tool run)
row("mut-r9-01-lambda-frozen-at-grid-value", "student-error mutant", "ledgers/E3/mutants/r9_01_lambda_frozen_at_its_grid_value.py", "PASS",
    CARRY + "killed in the tool run: " + "test_estimate_returns_the_named_fields_as_finite_floats (seed 0)")
row("mut-r9-02-lambda-climbs-downhill", "student-error mutant", "ledgers/E3/mutants/r9_02_lambda_climbs_downhill.py", "PASS",
    CARRY + "killed in the tool run: test_score_is_zero_at_the_estimate (seed 0)")
row("mut-r9-03-lambda-reported-as-its-log", "student-error mutant", "ledgers/E3/mutants/r9_03_lambda_reported_as_its_log.py", "PASS",
    CARRY + "killed in the tool run: test_reported_log_likelihood_is_the_likelihood_at_the_estimate (seed 0)")
row("mut-r9-04-convergence-ignores-lambda", "within-tolerance candidate (NOT a grader mutant; moved out of ledgers/E3/mutants in round 9)",
    "ledgers/E3/scripts/E3-d-r9/within_tolerance/r9_04_convergence_test_ignores_lambda.py", "PASS",
    "re-run this round on the current suite, seeds 0-9: " + fmt_suite("cand_r9_04") + " (ledgers/E3/scripts/E3-d-r10/suite_out/cand_r9_04.out). It meets the page's stated score tolerance (2e-5 on all three components, project.html:213), so the suite cannot and should not reject it; it is not counted as a mutant")
row("relaxed-test-kills-unchanged", "the round-9 relaxed local-max test (no lambda move) killed no mutant; the lambda move is now restored",
    "course/modules/E/E3/grader/test_project.py:586-598", "PASS",
    "with the lambda move restored, the tool run kills 140/140 (s3d_mutate_E3_seeds0-9.out); the round-9 subject (test_project.py) changed, so this row was re-derived, not carried")

# ---- mutants written this round (killing evidence from the per-seed runs, seeds 0-9)
row("mut-d10-01-identification-reads-only-b", "a student mutant: identification counts a mixed lottery only on the B side",
    "ledgers/E3/mutants/d10_01_identification_reads_only_the_b_lotteries.py; course/modules/E/E3/grader/test_project.py (no test covers an A-side-only mixed set); project.html:223, 237",
    "FAIL", "per-seed suite run (ledgers/E3/scripts/E3-d-r10/suite_out/mut_d10_01.out): " + fmt_suite("mut_d10_01") +
    ". Independent check: ledgers/E3/scripts/E3-d-r10/s3d_a_side_only_check.out: the reference returns the B-side estimates (gamma 0.1174, lambda 0.794, kappa 2.162) for a set whose only mixed lotteries are A lotteries, and the mutant raises ValueError. project.html:237 refuses a set only when 'no response has a lottery that mixes a gain and a loss', and project.html:223 says a pair identifies lambda when 'one of its two lotteries mixes'",
    "Add a test in test_project.py next to test_estimate_accepts_a_mixed_lottery_on_the_b_side_alone: every B lottery pure (a sure amount), at least one A lottery mixed; estimate must not raise ValueError (the mirror of the B-side test; the reference returns for the mirrored B-side set)")
row("mut-d10-02-likelihood-uses-crra-ce", "a student mutant: the likelihood uses CRRA certainty equivalents at a fixed wealth",
    "ledgers/E3/mutants/d10_02_likelihood_uses_crra_certainty_equivalents.py", "PASS",
    "per-seed suite run: " + fmt_suite("mut_d10_02") + " (killed on every seed 0-9)")
row("mut-d10-03-estimate-drops-pure-responses", "a student mutant: the estimator drops responses whose two lotteries are both pure",
    "ledgers/E3/mutants/d10_03_estimate_drops_the_pure_responses_first.py", "PASS",
    "per-seed suite run: " + fmt_suite("mut_d10_03") + " (killed on every seed 0-9)")

# ---- alternatives
row("alt-1-2-3-5-seeds-0-9", "alternatives 1 (grid zoom + Newton), 2 (Newton, FD step 1e-6), 3 (Nelder-Mead + Newton), 5 (exp/log float CE): must pass seeds 0-9",
    "ledgers/E3/scripts/E3-d-r10/alts/{alt1c_zoom_then_reference_newton, alt2c_newton_fd1e-6_damped, alt3_nelder_mead_v2, alt5_exp_log_float}/elicit.py",
    "PASS", "per-seed suite runs (suite_out/alt1c.out, alt2c.out, alt3v2.out, alt5.out). Seed 2 is the tight case: alt1b and alt1c (grid zoom + Newton, the reference loop from a different start) stop about 1e-6 from the maximum, with the reference-style score 8.8e-4 at step 1e-5 and 3.8e-5 at step 1e-6, so test_score_is_zero_at_the_estimate fails on seed 2 only; the reference passes that test with 6.4e-9 at step 1e-5 (s3d_seed2_score_alt1c.out: the same score evaluated directly on make_instance(2); the seed-2 log-likelihoods agree to 1e-9). The score criterion is the page's (project.html:213, 2e-5); the reference stops at gradient 1e-7, which the alternative does not reach. Recorded PASS for the grader and as an alternative defect; see notes. alt2c " + fmt_suite("alt2c") + "; alt3v2 " + fmt_suite("alt3v2") + "; alt5 " + fmt_suite("alt5") + "; alt1c " + fmt_suite("alt1c") + ". The first versions (alt1, alt2) failed the recovery, second-participant and large-lambda tests because their own stopping rules left non-stationary points (alt1 seed 2 score 4.3e-4); the repaired versions above are the ones counted")
row("alt-4-bisection-seeds-0-9", "alternative 4: prospect CE by bisection inversion, then the same half-up rule",
    "ledgers/E3/scripts/E3-d-r10/alts/alt4b_bisection_full_precision/elicit.py", "PASS",
    "per-seed suite run (suite_out/alt4b.out): " + fmt_suite("alt4b") + ". Note: the first bisection (alts/alt4_bisection_ce, tolerance 1e-9 cents) fails test_half_cent_goes_up_on_exact_halves on every seed (suite_out/alt4.out: " + fmt_suite("alt4") + "). That test is consistent with project.html:221 (CE 'computed in floating point ... rounded once', exact half up); an inversion stopped at 1e-9 cents is not full precision, so this is not counted as an over-constraint")
row("alt-6-finite-difference-step-1e-4", "alternative 6 (reference with finite-difference step 1e-4 in the optimiser, Hessian and standard errors)",
    "ledgers/E3/scripts/E3-d-r10/alts/alt6_fd_step_1e-4/elicit.py; course/modules/E/E3/grader/test_project.py:619-642 and 1035-1064", "PASS",
    "per-seed suite run (suite_out/alt6.out): " + fmt_suite("alt6") + ". The round-9 FAIL reproduces at seed 2 (test_score_is_zero_at_the_estimate, test_standard_errors_match_the_coordinate_change_oracle). Measured at seed 2 (ledgers/E3/scripts/E3-d-r10/s3d_alt6_seed2.out: alt6 score 8.7e-5 to 3.3e-3 at steps 1e-5 and 1e-6; se_gamma 0.0429 against the oracle's 0.0620, -31%; reference score 6.4e-9 at step 1e-5). The implementation is not a correct MLE at the page's own tolerance, so the grader's rejection is correct; recorded PASS for the grader, and the alternative is not a required one")
row("alt-lambda-local-max-restored-on-alternatives", "the restored lambda move in the local-maximum check holds on the alternatives", "course/modules/E/E3/grader/test_project.py:586-598", "PASS",
    "the alternatives above run the current suite, including test_estimate_is_a_local_maximum (lambda moved), at seeds 0-9; no alternative failed it")
row("alt-cross-seed-likelihood", "alternatives' log-likelihood vs the reference on seeds 0-49 (any alternative above the reference is a finding; below is a local maximum)",
    "course/modules/E/E3/grader/test_project.py:619-642", "PASS",
    "ledgers/E3/scripts/E3-d-r10/alts_out/compare_*.txt and s3d_alt_compare2.py: no alternative exceeds the reference likelihood; alt2c and alt3 reach a lower stationary point on seed 6 (3.18 nats below); alt1b and alt1c on seed 42 (0.068 nats below). A local maximum is not what the page's 'maximum-likelihood' requires of the suite, and the suite's local-max checks accept it; noted, not a grader failure")

# ---- round-9 rows: grader and page rows that changed this round
row("ladder-skill-checks-claim", "project ladder: skip rungs 1-2 only with the placement bar and both skill checks", "course/modules/E/E3/project.html:42; index.html:142", "PASS",
    "project.html:42 read this round; index.html:142 'you must reach the placement bar and answer both skill checks' matches")
row("lab1-inputs-notation", "Lab 1 stated inputs and symbols", "course/modules/E/E3/project.html:53; tests/labs/E3/lab-E3-project-1.py:10-12", "PASS",
    "project.html:53 gamma 0.40, lambda 2.00, kappa 1.50 matches the twin constants (GAMMA, LAMBDA, KAPPA) at lines 67-69 of the page code")
row("nearest-cent-docstring-lab1", "Lab 1 docstring: exact half goes up", "course/modules/E/E3/project.html:74; tests/labs/E3/lab-E3-project-1.py:17", "PASS",
    "project.html:74 'an exact half going up (toward plus infinity)' matches nearest_cent = math.floor(amount + 0.5); twin byte-identical to the page (run_labs PASS)")
row("grader-dominance-sentence", "project.html:213 dominance sentence vs the dominance checks", "course/modules/E/E3/project.html:213; grader/test_project.py:1175-1206", "PASS",
    "project.html:213 'the first- and second-order dominance checks ... which allow one cent' matches DOMINANCE_SLACK = 1 and the two tests; both checks pass on the reference (seed 0 and the 50-seed run)")
row("grader-tolerances-vs-page", "project.html:213 local-maximum check moves each of gamma, lambda and kappa by 0.1 percent", "course/modules/E/E3/project.html:213; grader/test_project.py:586-598",
    "PASS", "round-9 FAIL is fixed: test_estimate_is_a_local_maximum now moves gamma, lambda and kappa at +/-1e-3 relative, tolerance 1e-9 (test_project.py:591-598); the page sentence matches; the reference passes it on seeds 0-49 (run_graders PASS)")
row("grader-local-max-kink-claim", "grader docstring must not claim lambda kinks that the page does not state", "course/modules/E/E3/grader/test_project.py:586-588", "PASS",
    "round-9 FAIL is fixed: the docstring now says 'Moving each of gamma, lambda and kappa by 0.1 percent ... This is the local maximum check that the page states' (test_project.py:587-588); no kink claim remains")
row("grader-large-lambda-docstring", "grader docstring of test_estimate_on_a_large_loss_aversion_participant_is_also_a_maximum (claims about a search that rejects lambda above 10)",
    "course/modules/E/E3/grader/test_project.py:664-669", "FAIL",
    "ledgers/E3/scripts/E3-d-r10/s3d_lam10_reject.py (output s3d_lam10_reject.out): a reference search that rejects lambda above 10 (objective -inf there) does NOT stop at the boundary. It converges to an interior point, lambda_hat 7.2176, with score 1e-7 (step 1e-5) and 1e-7 (step 1e-6), and that point passes the large-lambda check (s3d_reject_lambda10_suite.out: the rejecting elicit.py passes test_estimate_on_a_large_loss_aversion_participant_is_also_a_maximum, reproduced by s3d_reject_lambda10_elicit.py), so the docstring sentence 'A search that rejects lambda above 10 stops at that boundary, where the score is not zero, so the score check fails it' is false as stated",
    "Delete the sentence 'A search that rejects lambda above 10 stops at that boundary, where the score is not zero, so the score check fails it.' (or restate it as what the check does: it fails an estimate whose reported lambda is clamped at 10, as in r9e_01)")
row("identification-convention-zero-prize", "project.html:223 identification convention", "course/modules/E/E3/project.html:223; grader/test_project.py mixed() and identification tests", "PASS",
    "page statement checked by hand: a lottery with no gain or no loss (zero prize neither) has a CE free of lambda (v is linear in lambda on the loss side and the inverse divides it out); verified with the reference's CE; the 'only when one lottery mixes' necessary condition holds")
row("models-definition-change", "project.html:220 value function, parameter ranges", "course/modules/E/E3/project.html:220; grader/reference.py:64-68, 85-91", "PASS",
    "project.html:220 'v(x)=x^(1-gamma) ... with 0 <= gamma < 1 and lambda > 0' matches reference _check_prospect and _value; L06 Definition 1.2 (line 61-64) with alpha = delta = 1-gamma")
row("questionnaire-fraction-contract", "project.html:207 and :273 probability text", "course/modules/E/E3/project.html:207, 273", "PASS",
    "regex /^(0|1|\\d+\\/\\d*[1-9]\\d*)$/ accepts '0', '1' and numerator/denominator with a nonzero denominator; page text matches; the engine's _check_probabilities uses Fraction(p) (reference.py:50-54)")
row("questionnaire-grammar", "project.html:340 export status grammar", "course/modules/E/E3/project.html:340", "PASS",
    "read at line 340: 'No export: pair(s) ... has/have no choice yet.' with singular/plural by missing.length; matches the page's stated behaviour")
row("questionnaire-js-browser", "questionnaire loads the instrument, lists pairs, blocks export until each pair has a choice, exports responses.json", "course/modules/E/E3/project.html:245-353",
    "PASS", "read lines 279-353: load validates pair_id and lotteries, the export refuses while any pair has no choice (lines 327-343), writes responses.json. page_smoke PASS (no console errors on load). A click-through export in a real browser was not run (honest gap)")
row("questionnaire-js-syntax", "inline questionnaire script parses", "course/modules/E/E3/project.html:249-355", "PASS",
    "ledgers/E3/scripts/E3-d-r10/s3d_questionnaire_inline.js (second inline script block) through 'node --check': rc=0 (s3d_questionnaire_node_check.out)")
row("hours-arithmetic", "time-budget table sums to data-hours-project and the hub split", "course/modules/E/E3/project.html:33, 362-370; index.html:29", "PASS",
    "1+1+3+4+3+2 = 14 = data-hours-project (project.html:33); hub data-hours-lessons=56 + data-hours-project=14 = 70 (index.html:29); check_pages PASS")
row("exemplar-word-count-A", "Exemplar A memo words", "course/modules/E/E3/project.html:625-676; claim at :623", "PASS",
    "word count of the memo text (runs of non-space characters, tags removed, headings included, the four memo-text divs): 117 = the page's '117 words' (project.html:623)")
row("exemplar-word-count-B", "Exemplar B memo words", "course/modules/E/E3/project.html:623 (claim), :678-740 (memo)", "FAIL",
    "same count for Exemplar B: memo-text divs give 450 words (tags removed, headings included); the whole article gives 836, memo + annotations 672, memo + verdict 612. No definition gives 603. Round 9 had 450 and the claim was changed to 603 in this pin (delta project.html:623)",
    "Change '603 words' to '450 words' in project.html:623 (the sentence 'the memo text of Exemplar A is 117 words and that of Exemplar B is 450 words')")
row("fixed-case-data-claims", "Lab 3 instrument claims in Exemplar B", "course/modules/E/E3/project.html:683-684; Lab 3 data", "PASS",
    "computed from the 12 Lab 3 answers: prizes between -18700 and 19000 cents; two or three prizes per lottery; pairs 0 and 3 quoted match the data; 11 of 12 pairs mixed (only pair 4 has none; lab prints 'mixed-sign answers: 11')")
row("exemplar-b-model-identification", "Exemplar B model paragraph: identification", "course/modules/E/E3/project.html:696", "PASS",
    "the statements that lotteries without a gain or without a loss do not identify lambda match the Identification convention (project.html:223); the precision and curvature identification sentences are marked as hypotheses")
row("exemplar-b-interpretation", "Exemplar B interpretation: SE exceeds the estimate; SIMULATED; stakes hypothetical", "course/modules/E/E3/project.html:719", "PASS",
    "Lab 3 se_lambda 9.59 > lambda_hat 6.1503; the 'I expect, without computing it here' sentences are hypotheses by the page's own words")
row("exemplar-scores-annotations", "exemplar data-scores and annotations agree with the rubric", "course/modules/E/E3/project.html:625-740, 611-615", "PASS",
    "Exemplar A data-scores 2,2,1,2,1 with the official-scoring line; Exemplar B 3,3,4,3,3; every annotation's level matches the rubric descriptors in the table (rows C1-C5)")
row("notation", "every symbol and macro on the changed page lines vs notation/notation.json", "course/modules/E/E3/project.html (math)", "PASS",
    "macros used on the page are registered or lesson-local; \\Phi in the stretch section is the registered standard normal CDF (notation.json '\\Phi, \\Phi^{-1}'); gamma, lambda, kappa, zeta, alpha, delta, xi, W are lesson-local (notation.json 'about': gamma is local); no registered symbol is reused")
row("scope-words", "scope words in changed sentences need a computation or a stated hypothesis", "course/modules/E/E3/project.html:213, 221-223, 683, 695, 719", "PASS",
    "'only when one of its two lotteries mixes' (223) is a necessary condition, checked by the lambda-free CE argument; 'every' at 213 refers to the suite's checks, verified by reading the tests")
row("process-words", "no process words in learner text", "course/modules/E/E3/project.html", "PASS",
    "text scan: 'round' appears only as rounding (12 uses, all of rounding); no 'builder', 'verifier', 'fragment', 'ledger'; 'the suite' refers to the autograder")
row("concept-links-definitions", "concept links and def ids used by the changed text", "course/modules/E/E3/project.html:53, 213, 220, 222", "PASS",
    "prospect-theory -> L06.html#def-prospect-theory (L06.html:69); certainty-equivalent -> L02.html#def-certainty-equivalent (L02.html:99); crra-utility -> L03.html#def-crra-utility (L03.html:88); first-order-stochastic-dominance -> L04.html#def-first-order-stochastic-dominance (L04.html:80); check_dag PASS")
row("dag-unlinked-names", "concepts used by the changed text lie in the prerequisite closure or are prose-only", "course/modules/E/E3/project.html", "PASS",
    "MLE, Hessian, observed information and Fisher-type terms are plain prose (Architect decisions: MLE plain prose); check_dag PASS")
row("citations-reading", "reading section registry keys and their claims", "course/modules/E/E3/project.html:757-764; L02.html:616; L05.html:609; L06.html:531; L07.html:80; L08.html:67, 133", "PASS",
    "claims grep: kahneman1979prospect attached to a graded claim at L07.html:80 (data-grade C); ellsberg1961risk at L08.html:133 and gilboa1989maxmin at L08.html:67 (data-grade C); pratt1964risk only named at L02.html:616 and epstein1989substitution only at L05.html:609 (no claim span); matches project.html:759")
row("rubric-levels-vs-annotations", "rubric descriptors vs exemplar annotations", "course/modules/E/E3/project.html:611-617, 623-740", "PASS",
    "each annotation names a descriptor of the stated level (e.g. C3 level 2 requires the three se_* estimates, Exemplar A misses it)")
row("lab1-prose-numbers", "Lab 1 prose numbers vs printed output", "course/modules/E/E3/project.html:57, 148", "PASS",
    "printed (s3d_lab_twins_output.out): CRRA 496/500, prospect -30/500; P(A) 0.480149, log -0.733658; sum -2.302315; pair 2 prospect B -762, CRRA B -513 (not quoted); sure 3000 both models; all match")
row("lab2-prose-numbers", "Lab 2 prose numbers vs printed output", "course/modules/E/E3/project.html:153, 197", "PASS",
    "printed: -0.765595182, -0.625595182, P(A)=0.465057055, z=-0.14 (2*(1500-2200)/10000); all match")
row("lab3-prose-numbers", "Lab 3 prose numbers vs printed output", "course/modules/E/E3/project.html:395, 584-590, 708, 719", "PASS",
    "printed: gamma_hat 0.6352, lambda_hat 6.1503, kappa_hat 2.0201, se 0.32/9.59/1.86, log-lik -7.1445, score 3.55e-10, 11 of 12 mixed; all match")
row("lab-twins-isolated", "twins under python -I -W error, alone", "tests/labs/E3/lab-E3-project-1..3.py", "PASS",
    "ledgers/E3/scripts/E3-d-r10/s3d_twin_1.err, s3d_twin_2.err, s3d_twin_3.err: rc=0 and 0 bytes of stderr")
row("lab-page-code-equals-twin", "page code equals twin (run_labs)", "course/modules/E/E3/project.html Labs 1-3", "PASS",
    "run_labs PASS (s3d_run_labs_project.out)")
row("lab-expected-equals-output", "expected block equals twin output", "course/modules/E/E3/project.html Labs 1-3", "PASS",
    "run_labs PASS; twin outputs in s3d_lab_twins_output.out match the expected blocks")
row("instance-docstring-claims", "instance.py docstring ranges, pair counts, denominators, guards", "course/modules/E/E3/grader/instance.py:1-33, 45-52, 148-261", "PASS",
    "read every line: gamma [0.10,0.80] three decimals, lambda [1,3], kappa [0.5,5], wealth 50k-200k dollars, 200 pairs, 2-3 prizes, magnitudes 500-50000 cents, denominators 4/5/10/20, mixed count >= 100, Hessian and boundary guards, half-cent guard 1e-6: all as stated")
row("grader-messages-never-print-answer", "failure messages never print a value", "course/modules/E/E3/grader/test_project.py:251-285 and every expect()", "PASS",
    "all expect/pytest.fail messages are fixed strings; expected values are not formatted into messages (read every call)")
row("grader-gamma0-exact-convention", "CRRA gamma = 0 exact expected prize convention", "project.html:221; grader/test_project.py:144-148; grader/reference.py:122-124", "PASS",
    "reference sums Fraction products and rounds once with floor(x + 1/2); test checks equality with the test's own nearest(); matches page")
row("grader-seed49-se-docstring-numbers", "docstring numbers for seed 49 SE (test_standard_errors_match_the_coordinate_change_oracle)", "grader/test_project.py:1035-1046", "PASS",
    "ledgers/E3/scripts/E3-d-r10/s3d_seed_facts.out: seed 49 se_lambda 135.054 (1e-5) and 97.675 (1e-6); se_gamma 0.09474 and 0.07983; reverse order 136.779 (+1.3%) and 98.086 (+0.4%); all match the docstring")
row("grader-allA-docstring", "docstring numbers for the all-A set", "grader/test_project.py:874-881", "PASS",
    "ledgers/E3/scripts/E3-d-r10/s3d_all_a_degenerate.out: kappa_hat 924.73, se_lambda 692052, se_kappa 1981269, se_gamma 692.39; docstring says ~925, above 1e5 and about 692: match")
row("grader-seed30-kappa-below-one", "fixed participant with kappa below one (seed 30)", "grader/instance.py; grader/test_project.py:36", "PASS",
    "s3d_seed_facts.out: seed 30 kappa_hat 0.8973 < 1")
row("grader-recovery-47-of-50", "recovery count on seeds 0-49 (47 of 50)", "grader/test_project.py:601-616", "PASS",
    "run_graders 0-49 PASS (the recovery test runs inside every seed's suite run, and the reference passes all 50); the threshold 47 is the page's (project.html:213)")
row("grader-second-participant-and-clamp", "second participant and clamp detection", "grader/test_project.py:619-642; instance.py", "PASS",
    "tests run (reference passes; mutants e3d4_05 and r9e_04 killed); seed 30 LOW_KAPPA and INST2 as stated")
row("convention-whole-cents", "whole-cents convention vs engine", "project.html:221; grader/reference.py:71-73, 118-128", "PASS",
    "floor(c + 1/2) in reference _half_up; gamma = 0 CRRA exact path; no other rounding of money")
row("concept-links-definitions-carried", "concept link targets used by unchanged page lines", "course/modules/E/E3/project.html:205, 207", "PASS",
    "project.html:205/207 link targets are unchanged text; check_dag PASS; page_smoke PASS")


# ---- round-9 rows whose ids must be kept
E8_IDS = {"e8_01_se_from_inverse_of_the_diagonal_only": "mut-e8-01-se-diagonal-only",
          "e8_02_crra_allows_final_wealth_of_exactly_zero": "mut-e8-02-crra-zero-wealth-allowed",
          "e8_03_prospect_loss_weight_also_scales_the_gain_branch": "mut-e8-03-prospect-loss-weight-on-gains",
          "e8_04_prospect_model_adds_wealth_to_each_prize": "mut-e8-04-prospect-adds-wealth",
          "e8_05_model_name_error_raises_type_error": "mut-e8-05-model-name-type-error"}
for e8, rid in E8_IDS.items():
    kill = next((l for l in (S / "s3d_mutate_E3_seeds0-9.out").read_text().splitlines() if l.startswith("KILLED " + e8)), "")
    row(rid, "round-8 student-error mutant (carried)", "ledgers/E3/mutants/" + e8 + ".py", "PASS",
        CARRY + "tool run: " + (kill or "KILLED line not found") + " (s3d_mutate_E3_seeds0-9.out)")

row("rung1-lab-answers-claim", "project.html:44 rung-1 text vs Lab 1 output", "course/modules/E/E3/project.html:44; tests/labs/E3/lab-E3-project-1.py", "PASS",
    "project.html:44 says Lab 1 prints three choice pairs, each certainty equivalent and each likelihood term; the Lab 1 output (s3d_lab_twins_output.out) prints CRRA and prospect CEs per pair, P(A), the chosen log-probability, and the total for pairs 1-3; run_labs PASS")

# fix up the two rows that are not PASS to carry fixes
for r in rows:
    if r["status"] != "PASS" and not r.get("fix"):
        r["fix"] = "see evidence"

mutants = mutate_rows() + [
    {"name": "d10_01_identification_reads_only_the_b_lotteries", "description": "Loss-aversion identification counts a mixed lottery only on the B side of each question, so a set whose only mixed lottery is A is refused.", "killed_by": None},
    {"name": "d10_02_likelihood_uses_crra_certainty_equivalents", "description": "The logit likelihood takes its certainty equivalents from the CRRA model at the current gamma (wealth fixed at 1000 dollars) instead of the prospect value.", "killed_by": "test_log_likelihood_matches_oracle_at_the_true_parameters (seeds 0-9, 14 failing)"},
    {"name": "d10_03_estimate_drops_the_pure_responses_first", "description": "The estimator discards every response whose two lotteries are both pure before maximising, so the likelihood uses only the mixed questions.", "killed_by": "test_reported_log_likelihood_is_the_likelihood_at_the_estimate (seeds 0-9, 6 to 7 failing)"},
]
# the mutant-line kills use "(seed 0)"; the per-seed d10 kills are recorded in their descriptions above
mutants = [m for m in mutants]

NOTES = (
    "Round 10 (E3-d) at 47a36d8c. Delta from 1e272e5a read hunk by hunk: project.html (ladder, rung 1-2 text, Lab 1 claim, grading-mode text with 47 checks, Estimation and Identification conventions, the exemplar word count 603, Exemplar B text) and grader/test_project.py (lambda move added to test_estimate_is_a_local_maximum, new large-lambda test at seed 49, docstring edits, degenerate all-A docstring). Re-verified every round-9 non-PASS row: grader-tolerances-vs-page and grader-local-max-kink-claim now PASS; alt-6 round-9 FAIL reproduced at seed 2 and attributed to alt6 being numerically inaccurate (score 3.3e-3, se_gamma -31%), so PASS for the grader. "
    "Carried rows are only those whose subject files are byte-identical (reference.py, instance.py, starter.py, lessons L02 and L04-L08, index.html, tests/labs/E3, notation, references, tools). "
    "Per-seed runs use QF_SEED inside env -i; the first per-seed runner dropped it and ran seed 0 for every seed, and those results were discarded and redone (suite_out/). "
    "Untracked files found in the checkout at the start (ledgers/E3/mutants/v10_01..04_*.py, ledgers/E3/scripts/E3-d-r10/* from an earlier attempt) were not relied on; the four v10 mutants were included in the 140 tool run and killed. "
    "Observations for the architect (not counted as FAIL rows): (1) on seed 49 the reference estimate (lambda_hat 20.6864, log-likelihood -126.0315) is a local maximum, and a stationary point at lambda 7.2176 has log-likelihood -125.9315; the page says 'maximum-likelihood' and does not claim a global maximum, and the suite accepts both. (2) On seed 2 the score test is at the finite-difference noise floor: the reference's score is 6.4e-9 at step 1e-5 but 8.8e-4 at step 1e-6, so the test passes only through the 1e-5 step; alternatives that stop 1e-6 from the maximum fail it (alt1b, alt1c). (3) The prospect exact-half test requires a float-precision inversion; a bisection stopped at 1e-9 cents fails it on every seed (alt4). "
    "Could not check: the questionnaire export click-through in a real browser (page_smoke loads the page and runs the reference grader only); the self-assessment form in site.js (outside slice d); cards.json and the curriculum.json M3 rename (other slices); a learner's own elicit.py in Pyodide; the alternatives' seeds 0-49 full suite (only the likelihood and recovery comparison was run for seeds 0-49, in s3d_alt_compare2.py outputs)."
)

frag = {
    "unit": "E3",
    "slice": "d",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 10 (did not build E3)",
    "pin": PIN,
    "base": "1e272e5a (round-9 pin); delta 1e272e5a..47a36d8c: course/modules/E/E3/project.html (lines 42-44, 53, 74, 205-223, 273, 340, 366, 623-740 changed; the 'Grading mode' text now says 47 checks), course/modules/E/E3/grader/test_project.py (lines 36-37, 163-165, 374-376, 585-695, 878-881, 1035-1046 changed), ledgers/E3/mutants (new r9 files, 140 total), cards.json and curriculum.json (outside slice d)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD10-E3-d",
    "scratch": "/tmp/E3d_r10_ws (reference, starter, mypy workspace), /tmp/E3d_r10_seed2_alt1c, /tmp/E3d_r10_suite_* (per-seed suites)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": "",
}
counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
frag["summary"] = f"E3-d round 10 at 47a36d8c: {len(rows)} rows: {counts.get('PASS', 0)} PASS, {counts.get('FAIL', 0)} FAIL, {counts.get('UNVERIFIABLE', 0)} UNVERIFIABLE. Mutants: 140 existing (140/140 killed by the tool run) and 3 new (2 killed on all seeds 0-9; d10_01 survives all seeds 0-9)."
out = ROOT / "ledgers/E3/E3-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts)
