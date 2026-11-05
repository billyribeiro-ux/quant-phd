"""Round-11 (E3-d): assemble the verifier fragment ledgers/E3/E3-d.json from the evidence in ledgers/E3/scripts/E3-d-r11/.
Every PASS/FAIL below cites the script or output file that backs it. Validation is done by tools/ledger.py's validate()."""
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/E3/scripts/E3-d-r11"
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

out = lambda name: (ROOT / S / name).read_text(encoding="utf-8")  # noqa: E731

# --- mutants: every existing mutant from the tool run, plus the round-11 mutants from kill_r11.py
mutants = []
for line in out("mutate_E3_seeds0-9.out").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line)
    if m:
        status, name, desc, killed = m.groups()
        mutants.append({"name": name, "description": desc, "killed_by": None if status == "SURVIVED" else killed.strip()})
r11 = {}
for line in out("kill_r11.out").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+) -> (.*)$", line)
    if m:
        status, name, rest = m.groups()
        r11[name] = (status, rest.strip())
descs = {
    "r11d_01_identification_reads_only_the_a_lotteries.py": "Student error: loss aversion is accepted only when a lottery of A mixes a gain and a loss, so a set whose only mixed lottery is on the B side is refused.",
    "r11d_02_newton_stops_when_the_likelihood_gain_is_below_1e9.py": "Student error: the maximiser stops once one Newton step raises the log-likelihood by less than 1e-9, a function-value rule.",
    "r11d_03_crra_final_wealth_is_wealth_minus_each_prize.py": "Student error: the CRRA model takes final wealth as wealth minus each prize, so a gain lowers final wealth.",
    "r11d_04_twelve_response_questionnaire_returns_the_lab3_table.py": "Student error: estimate returns the printed Lab 3 numbers for any questionnaire of twelve responses, without maximising.",
}
for name, (status, rest) in sorted(r11.items()):
    mutants.append({"name": name, "description": descs[name], "killed_by": None if status == "SURVIVED" else rest})

# --- alternatives
alt_lines = {}
for p in sorted((ROOT / S / "alts_out").glob("*.out")):
    alt_lines[p.stem] = p.read_text(encoding="utf-8").strip()

def alt_status(stem):
    return alt_lines.get(stem, "NOT RUN")


alt_done = {k: v for k, v in alt_lines.items()}
ALT7 = alt_status("alt7_armijo_newton")
ALT1C = alt_status("alt1c_zoom_then_reference_newton")
ALT6 = alt_status("alt6_fd_step_1e-4")
ALT2C = alt_status("alt2c_newton_fd1e-6_damped")
ALT3 = alt_status("alt3_nelder_mead_v2")
ALT4B = alt_status("alt4b_bisection_full_precision")
ALT5 = alt_status("alt5_exp_log_float")

NOW = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S+00:00")
C = "Carried from round 10 (%s byte-identical since the previous pin): "
R = []


def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)


# ----- gates re-run this round
row("gate-check-pages", "tools/check_pages.py --unit E3", "course/modules/E/E3/project.html", "PASS",
    f"{S}/check_pages_E3.out: 'check_pages E3: PASS', RC=0")
row("gate-check-dag", "tools/check_dag.py --unit E3", "course/modules/E/E3/project.html", "PASS",
    f"{S}/check_dag_E3.out: 'check_dag E3: PASS', RC=0")
row("gate-check-projects", "tools/check_projects.py --unit E3", "course/modules/E/E3/project.html", "PASS",
    f"{S}/check_projects_E3.out: 'check_projects E3: PASS', RC=0")
row("gate-run-labs-project", "tools/run_labs.py --unit E3 --page project (twins under python -I -W error; page code = twin; expected = output)",
    "course/modules/E/E3/project.html Labs 1-3; tests/labs/E3/lab-E3-project-1..3.py", "PASS",
    f"{S}/run_labs_project.out: 'run_labs E3: PASS (3/3)', RC=0")
row("gate-page-smoke-project", "tools/page_smoke.py --unit E3 --pages project (Chromium, Pyodide labs, in-browser grader)",
    "course/modules/E/E3/project.html", "PASS",
    f"{S}/page_smoke_project.out: 'in-browser grader: All 48 tests pass on seed 720646626 (31.4 s)', 'page_smoke E3: PASS' (lab timings 0.0-0.1 s)")
row("gate-run-graders-seeds-0-49", "tools/run_graders.py --unit E3 --seeds 0-49", "course/modules/E/E3/grader/", "PASS",
    f"{S}/run_graders_E3_0_49.out: 'run_graders E3: PASS (reference 50/50 seeds, slowest 23.3 s)', RC=0. The window 0-49 passes; seeds outside it fail for the reference, see ref-suite-fails-generator-seeds")
row("gate-collect-46", "pytest --collect-only test_project.py (id kept from rounds 9-10; the count is now 48)",
    "course/modules/E/E3/grader/test_project.py; project.html:213", "PASS",
    f"{S}/ref_ws.out: '48 tests collected'; project.html:213 says 'runs 48 checks'. The id is historic")
row("gate-reference-seed0", "reference.py as elicit.py, QF_SEED=0, pytest --assert=plain -W error", "course/modules/E/E3/grader/", "PASS",
    f"{S}/ref_ws.out: '48 passed', RC of the run 0 (scratch /Users/billyribeiro/.fanout/scratch-E3-d-r11/ref)")
row("gate-starter-fails", "starter.py as elicit.py must fail the suite", "course/modules/E/E3/grader/starter.py", "PASS",
    f"{S}/ref_ws.out: starter seed 0: '46 failed, 2 passed'")
row("gate-ruff", "ruff check and ruff format --check on grader/ and tests/labs/E3", "course/modules/E/E3/grader; tests/labs/E3", "PASS",
    f"{S}/ruff_check.out: 'All checks passed!' RC=0; {S}/ruff_format.out: '15 files already formatted' RC=0")
row("gate-mypy-strict-grader", "mypy --strict on the grader in its layout (elicit.py=reference, instance.py, test_project.py)",
    "course/modules/E/E3/grader/", "PASS", f"{S}/mypy_grader_strict.out: 'Success: no issues found in 3 source files', RC=0")
row("gate-mypy-repo", "mypy --no-incremental (repository, strict)", "repository", "PASS",
    f"{S}/mypy_repo.out: 'Success: no issues found in 385 source files', RC=0")
row("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json (keys cited at project.html:782-789)", "PASS",
    f"{S}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', RC=0. references.json changed only in generated_at and used_by of two entries (BK1/BK4, E9/LX1); no key cited on the E3 project page changed; the live run was not repeated")
row("gate-pytest-relevant", "pytest tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py -k E3", "project.html exemplars and lab twins", "PASS",
    f"{S}/pytest_relevant.out: 15 test marks, no failure, RC=0")
row("gate-mutate-existing-112", "tools/mutate_graders.py --unit E3 --seeds 0-9 (every mutant file present at the start of the run: 150; the id is kept from round 9)",
    "ledgers/E3/mutants/", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: 'mutate_graders E3: PASS (150/150 killed)', RC=0. The run started before the round-11 mutants existed; those are in kill_r11.out")
row("gate-mutants-count", "at least 3 mutants, and student-error mutants in the ledger", "ledgers/E3/mutants/", "PASS",
    "150 existing + 4 round-11 student-error mutants (r11d_01..04); the ledger holds far more than the three the protocol asks")

# ----- round-11 mutants
row("mut-r11d-01-identification-reads-only-the-a-lotteries", "student-error mutant (loss aversion accepted only from A-side mixed lotteries)",
    "ledgers/E3/mutants/r11d_01_identification_reads_only_the_a_lotteries.py; grader/test_project.py:844-870", "PASS",
    f"{S}/kill_r11.out: '{r11['r11d_01_identification_reads_only_the_a_lotteries.py'][1][:200]}'")
row("mut-r11d-03-crra-final-wealth-minus-prize", "student-error mutant (CRRA final wealth = wealth minus prize)",
    "ledgers/E3/mutants/r11d_03_crra_final_wealth_is_wealth_minus_each_prize.py", "PASS",
    f"{S}/kill_r11.out: killed by '{r11['r11d_03_crra_final_wealth_is_wealth_minus_each_prize.py'][1][:120]}'")
row("mut-r11d-02-newton-stops-on-likelihood-gain", "student-error mutant (maximiser stops when one Newton step gains < 1e-9 in log-likelihood)",
    "ledgers/E3/mutants/r11d_02_newton_stops_when_the_likelihood_gain_is_below_1e9.py; grader/test_project.py (no test)", "FAIL",
    f"SURVIVES the suite on seeds 0-9 ({S}/kill_r11.out). It is distinguishable from the reference only off the generator: "
    f"on 26-response random participants (search_tell.py rng 11, trials 31 and 47) it raises 'observed information is not positive definite' "
    f"while the reference returns stationary points with score 4.8e-8 and 9.8e-8 ({S}/search_tell_r11d_02.out, {S}/search_tell_ref.out, {S}/trial_detail.out). "
    f"On the generator family (seeds 0-399) its output and failures equal the reference's ({S}/seed_scan_r11d_02_0_399.out vs {S}/seed_scan_ref_0_399.out), "
    f"so no generator seed in 0-399 separates them.",
    "Add a fixed participant (JSON responses from search_tell.py rng 11, trial 31, 26 pairs; the reference passes its score and local-max checks with score 4.8e-8) "
    "to test_project.py beside LOW_KAPPA/LARGE_LAMBDA, with a check that estimate returns and passes the score and local-maximum checks; re-run kill_r11.py on it.")
row("mut-r11d-04-twelve-response-lab3-table", "student-error mutant (estimate returns the Lab 3 table for any 12-response questionnaire)",
    "ledgers/E3/mutants/r11d_04_twelve_response_questionnaire_returns_the_lab3_table.py; grader/test_project.py (no 12-response MLE check)", "FAIL",
    f"SURVIVES the suite on seeds 0-9 ({S}/kill_r11.out). It violates the stated maximum-likelihood estimate (project.html:7 and index.html:33 say 'maximum likelihood') "
    f"on every 12-response questionnaire other than Lab 3, and no test of the suite covers a 12-response set. The reference passes the score and local-maximum checks on the suite's two 12-response sets (B-side and its A-side mirror: score 1.9e-8, local-max excess -7.7e-9, {S}/fixed_sets_check.out).",
    "Add a test on the B-side 12-response set (test_project.py B_SIDE_* constants): the estimate's score is below 2e-5 at step 1e-5 or 1e-6 and no 0.1 percent move raises the likelihood by more than 1e-9 (the reference passes, see fixed_sets_check.out). Re-run kill_r11.py.")

# ----- the reference fails the unchanged suite on generator seeds outside 0-49
row("ref-suite-fails-generator-seeds", "2.6 autograder: the reference passes the suite on every seed the page can give (project.html:211 'graded on the participant that your seed generates')",
    "course/modules/E/E3/grader/reference.py:261-278 (maximiser; silent return at 272-273); grader/test_project.py:558-583 (score), 586-598 (local maximum)", "FAIL",
    f"{S}/seed_scan_ref_0_399.out (make_instance seeds 0-399, reference): RuntimeError 'observed information is not positive definite' on seed 157; "
    "score 8.98e-2 (seed 108), 1.39e-1 (seed 165), 2.53e-2 (seed 269), against the page's 2e-5. "
    f"{S}/ref_bad_seeds_suite.out (the unchanged suite with the reference): seed 108 1 failed (test_score_is_zero_at_the_estimate); seed 157 the estimate raises RuntimeError inside the suite; "
    "seed 165 2 failed (test_score_is_zero_at_the_estimate and test_estimate_is_a_local_maximum: a nearby parameter has a higher likelihood); seed 269 1 failed. "
    f"{S}/probe108.out (seed 108): the engine's and the oracle's gradients agree (log-lambda component -0.224386); the central derivative in log-lambda is -0.224 at step 1e-5 but +0.0898 at 1e-6 and +0.0942 at 1e-7 and 1e-8, so the 1e-5 finite difference has the wrong sign and the damped Newton loop exits at reference.py:272-273 with max|grad| 0.224 (instrumented run, scratch dbg108). "
    f"Alternative Armijo-Newton ({S}/alts/alt7_armijo_newton, {S}/alt7_seed108.out) also fails seed 108 (score 2.49e-1 at 1e-5, 6.0e-2 at 1e-6). "
    f"A scratch copy with _H = 1e-7 (not a fix: {S}/seed_scan_h1e-7_0_399.out) raises on six seeds (75, 77, 139, 152, 157, 352) and still fails 108, 165, 269 (8.2e-3, 6.8e-3, 1.7e-3).",
    "Make the maximiser converge on seeds 108, 157, 165 and 269, not return silently: replace the finite-difference gradient at step 1e-5 (reference.py:21) with an exact score or a step that is validated per seed, and make the loop raise when the damped step cannot raise the likelihood (reference.py:272-273) instead of returning. Then re-run run_graders and seed_scan.py over 0-399; the suite's seed list must not contain a seed the reference fails, or the page must say which seeds are not gradable.")

# ----- round-10 FAILs now resolved
row("mut-d10-01-identification-reads-only-b", "student mutant: identification counts a mixed lottery only on the B side",
    "ledgers/E3/mutants/d10_01_identification_reads_only_the_b_lotteries.py; grader/test_project.py:873-900 (new test)", "PASS",
    f"Round-10 FAIL resolved. The new test test_estimate_accepts_a_mixed_lottery_on_the_a_side_alone (test_project.py:873-900) kills it ({S}/mutate_E3_seeds0-9.out: 'KILLED d10_01 ... -> test_estimate_accepts_a_mixed_lottery_on_the_a_side_alone')")
row("grader-large-lambda-docstring", "grader docstring for the seed-49 test is true", "course/modules/E/E3/grader/test_project.py:664-668", "PASS",
    "Round-10 FAIL resolved: the sentence 'A search that rejects lambda above 10 stops at that boundary ...' is deleted (diff 47a36d8c..ccaeeaf). The remaining docstring states what the test checks; the reference passes it on seeds 0-49 (run_graders PASS)")
row("exemplar-word-count-B", "project.html claim of the memo-text word counts", "course/modules/E/E3/project.html:646 (claim), memo divs of Exemplar A and B", "PASS",
    f"Round-10 FAIL resolved. {S}/wordcount_r11.out: memo-text divs Exemplar A = 117 words, Exemplar B = 450 words (tags removed, headings included); the claim reads '117 words' and '450 words'")
row("exemplar-word-count-A", "word count of Exemplar A memo text", "course/modules/E/E3/project.html:646", "PASS",
    f"{S}/wordcount_r11.out: 117 (= the claim)")
row("grading-mode-48-checks", "the count of checks on the page equals the collect-only count", "course/modules/E/E3/project.html:213; grader/test_project.py", "PASS",
    f"{S}/ref_ws.out: 48 tests collected; project.html:213 says 'runs 48 checks with warnings as errors'")
row("grading-mode-tolerance-phrases", "the tolerance sentences of project.html:213 match the tests (the gamma = 1 phrase and the prospect units phrase changed in this pin)",
    "course/modules/E/E3/project.html:213; grader/test_project.py:164-199 (CRRA log case, homogeneity, CRRA risky lottery), 214-238 (prospect)", "PASS",
    "Re-derived: 'except the case gamma = 1, where the utility is ln w' matches test_crra_log_case (ONE_CENT + TOL, line 177); 'tested in units of the prospect value ... slack 1e-9 times one plus the absolute value' matches test_prospect_sure_amount (line 234-236); exact integer equality for prospect and CRRA at gamma 0 (lines 149, 159, 220)")
row("lab3-hypothesis-and-twin", "Lab 3 hypothesis and the instruction 'replace the body of the function estimate ... keep main' match the page code and twin",
    "course/modules/E/E3/project.html:395-402, 417-606; tests/labs/E3/lab-E3-project-3.py", "PASS",
    f"{S}/labs_check.out: lab-E3-project-3 twin rc=0, 0 stderr bytes; page code equals twin; expected block equals output. The instruction names estimate and main, which the page code defines (project.html:567-606)")

# ----- re-derived this round (subject changed in this pin)
row("ladder-skill-checks-claim", "ladder text matches index.html", "course/modules/E/E3/project.html:42; index.html:142", "PASS",
    C % "course/modules/E/E3/project.html lines 1-209 and index.html" + "project.html:42 and index.html:142 read: 'answered both skill checks ... skip rungs 1 and 2' matches")
row("lab1-inputs-notation", "Lab 1 inputs named on the page equal the twin constants", "course/modules/E/E3/project.html:53; tests/labs/E3/lab-E3-project-1.py:10-12", "PASS",
    C % "project.html lines 1-209 and lab-E3-project-1.py" + "gamma 0.40, lambda 2.00, kappa 1.50 match GAMMA, LAMBDA, KAPPA of the twin")
row("nearest-cent-docstring-lab1", "nearest-cent statement of Lab 1", "course/modules/E/E3/project.html:74; tests/labs/E3/lab-E3-project-1.py:17", "PASS",
    C % "project.html lines 1-209 and lab-E3-project-1.py" + "'an exact half going up (toward plus infinity)' matches nearest_cent = floor(amount + 0.5); run_labs PASS")
row("grader-dominance-sentence", "project.html:213 dominance sentence (one cent) matches the tests", "course/modules/E/E3/project.html:213; grader/test_project.py:1147-1150, 1204-1235", "PASS",
    "Re-derived: DOMINANCE_SLACK = 1 (test_project.py:1147-1150); first- and second-order tests at lines 1204-1235; both pass on the reference seeds 0-49 (run_graders PASS)")
row("grader-tolerances-vs-page", "project.html:213 tolerances match the suite's constants and checks", "course/modules/E/E3/project.html:213; grader/test_project.py:586-598", "PASS",
    "Re-derived: the local-maximum move of 0.1 percent of each of gamma, lambda, kappa with 1e-9 slack (test_project.py:586-598) matches the page; the score tolerance 2e-5 at step 1e-5 or 1e-6 matches test_score_is_zero_at_the_estimate (lines 580-583)")
row("grader-local-max-kink-claim", "docstring of the local-maximum test", "course/modules/E/E3/grader/test_project.py:586-588", "PASS",
    "Re-derived: 'This is the local maximum check that the page states' (lines 587-588); no kink claim remains")
row("identification-convention-zero-prize", "identification convention statement (lambda-free CE without a gain or without a loss)",
    "course/modules/E/E3/project.html:223; grader/test_project.py mixed() and identification tests", "PASS",
    C % "project.html lines 1-391 (line 223 unchanged)" + "checked by hand: a lottery with no gain or no loss has a lambda-free CE; 'only when one of its two lotteries mixes' is a necessary condition")
row("models-definition-change", "Models convention matches L06 Definitions 1.2-1.3 and reference.py",
    "course/modules/E/E3/project.html:220; grader/reference.py:64-68, 85-91; L06.html:61, 68", "PASS",
    C % "project.html lines 1-391, reference.py" + "L06.html Definition 1.2 (value function, line 61) and 1.3 (prospect value of a lottery, line 68) match; reference _check_prospect and _value match 0 <= gamma < 1 and lambda > 0")
row("questionnaire-fraction-contract", "questionnaire probability contract and the engine's Fraction reading", "course/modules/E/E3/project.html:207, 273",
    "PASS", C % "project.html lines 1-391" + "regex /^(0|1|\\d+\\/\\d*[1-9]\\d*)$/ accepts '0', '1' and numerator/denominator with a nonzero denominator; the engine reads Fraction(p) (reference.py:50-54)")
row("questionnaire-grammar", "export refusal grammar", "course/modules/E/E3/project.html:340", "PASS",
    C % "project.html lines 1-391" + "'No export: pair(s) ... has/have no choice yet.' matches missing.length singular/plural")
row("questionnaire-js-browser", "questionnaire JS behaviour as described", "course/modules/E/E3/project.html:245-353", "PASS",
    C % "project.html lines 1-391" + "load validates pair_id and lotteries; export refuses while a pair has no choice (lines 327-343); page_smoke PASS. A real-browser click-through was not run (honest gap)")
row("questionnaire-js-syntax", "inline questionnaire script parses", "course/modules/E/E3/project.html:249-355", "PASS",
    C % "project.html lines 1-391" + "the same inline block was checked with node --check in round 10 (s3d_questionnaire_node_check.out, rc=0); page_smoke loaded the page without console errors in this round")
row("hours-arithmetic", "hours split sums to the declared project hours and the hub", "course/modules/E/E3/project.html:33, 362-370; index.html:29", "PASS",
    f"1+1+3+4+3+2 = 14 = data-hours-project (project.html:33 and the table); index.html:29 data-hours-lessons 56 + data-hours-project 14 = 70; curriculum E3 hours 70; check_pages PASS ({S}/check_pages_E3.out)")
row("hours-estimate-30pct", "2.6 hours: the verifier's own estimate is within 30 percent of the declared 14 hours",
    "course/modules/E/E3/project.html:362-370", "PASS",
    "Verifier estimate: rungs 1-2 about 2 h; instrument 3 h; elicit.py and its local runs 6-8 h for a competent student (the MLE with standard errors, the exception table and the seed windows); report and uncertainty 3 h; self-assessment 2 h; total 16-18 h, i.e. +14 to +29 percent of 14 h. Within the 30 percent limit, but near it at the upper end")
row("exemplar-b-model-identification", "Exemplar B identification statements", "course/modules/E/E3/project.html:707, 719", "PASS",
    "Re-derived: the statements that lotteries without a gain or without a loss do not identify lambda match the Identification convention (project.html:223); the precision and curvature identification sentences are marked as hypotheses ('I expect, without computing it here')")
row("exemplar-b-interpretation", "Exemplar B interpretation statements", "course/modules/E/E3/project.html:731, 742", "PASS",
    f"Re-derived: se_lambda 9.59 > lambda_hat 6.1503 (lab 3 prints); the 'I expect, without computing it here' sentences are hypotheses; {S}/wordcount_r11.out")
row("exemplar-scores-annotations", "exemplar official scores and annotations match the rubric", "course/modules/E/E3/project.html:648-763", "PASS",
    "Blind scoring from the rubric text (before reading the annotations' levels): Exemplar A 2,2,1,2,1 and Exemplar B 3,3,4,3,3; both equal the official data-scores within one level on every criterion")
row("notation", "every symbol vs notation/notation.json", "course/modules/E/E3/project.html (math)", "PASS",
    "notation.json registers T, \\Phi (standard normal CDF; used with that meaning in the stretch section), gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}. Greek letters gamma, lambda, kappa, zeta, alpha, delta, xi, the lottery value W and c are local (notation.json 'about'); no registered symbol is reused")
row("scope-words", "scope words (only, all, every, exactly) carry their computation", "course/modules/E/E3/project.html:213, 221-223, 683, 695, 719", "PASS",
    "'only when one of its two lotteries mixes' (223) is a necessary condition, checked by the lambda-free CE argument; 'every' at 213 refers to the suite's checks, read at test_project.py (every check listed)")
row("process-words", "no process words in learner text", "course/modules/E/E3/project.html", "PASS",
    "text scan: no 'builder', 'verifier', 'fragment', 'ledger'; 'reference' occurs only as 'reference point' and 'Rung 3 reference case'; 'round' only as rounding; banned phrases of BUILDER_RULES 1.3-1.4 (TODO, TBD, lorem, ..., clearly, obviously, it is important to note) absent")
row("concept-links-definitions", "concept links resolve to their definitions", "course/modules/E/E3/project.html:53, 213, 220, 222", "PASS",
    "prospect-theory -> L06.html#def-prospect-theory (id present, L06.html:69); certainty-equivalent -> L02.html#def-certainty-equivalent (L02.html:99); crra-utility -> L03.html#def-crra-utility (L03.html:88); first-order-stochastic-dominance -> L04.html#def-first-order-stochastic-dominance (L04.html:80); check_dag PASS")
row("fixed-case-data-claims", "Exemplar B data claims: prize range, prizes per lottery, quoted pairs, and the mixed count, against the Lab 3 answers",
    "course/modules/E/E3/project.html:707 (Exemplar B instrument memo); tests/labs/E3/lab-E3-project-3.py ANSWERS", "PASS",
    f"{S}/fixed_case_data.out: prizes between -18700 and 19000 (the claim '-18 700 and 19 000'); two or three prizes per lottery; pair 0 = 6200 at 9/10 and -15100 at 1/10 against three prizes in B; pair 3 = 18800 at 3/4, -12500 at 1/4 against 16500 at 2/5, -17700 at 3/5; 11 of 12 pairs mixed (the lab prints 'mixed-sign answers: 11')")
row("grader-instances-sample-20", "2.6 autograder item 2: 20 sampled seeds give valid instances that differ materially",
    "course/modules/E/E3/grader/instance.py (make_instance)", "PASS",
    f"{S}/instances_sample20.out: seeds 0,1,2,3,7,11,13,17,19,23,29,30,31,37,41,43,47,49,53,57: every instance has 200 responses, exact probabilities summing to 1, choices A or B, whole-cent prizes, 129-134 or more mixed questions; invalid seeds: none; 20 of 20 distinct choice vectors and 20 of 20 distinct prize sums")
row("dag-unlinked-names", "MLE, Hessian and Fisher-type terms are prose (Architect decision)", "course/modules/E/E3/project.html", "PASS",
    "MLE, Hessian, observed information are plain prose; check_dag PASS")
row("citations-reading", "reading section and cited keys match the lessons", "course/modules/E/E3/project.html:782-789; L02.html:616; L05.html:609; L06.html:531; L07.html:80; L08.html:67, 133", "PASS",
    f"grep this round: data-cite kahneman1979prospect at L07.html:80 (data-grade C); ellsberg1961risk at L08.html:133 (C); gilboa1989maxmin at L08.html:67 (C); pratt1964risk only named at L02.html:616 and epstein1989substitution only at L05.html:609; no other lesson attaches either key. Anchors checked this round after the lesson edits")
row("rubric-levels-vs-annotations", "every annotation names a descriptor of its stated level", "course/modules/E/E3/project.html:611-617, 648-763", "PASS",
    "re-read this round: each annotation names the descriptor of the stated level (e.g. C3 level 2 requires the three se_* estimates; Exemplar A reports none)")
row("lab1-prose-numbers", "Lab 1 prose numbers", "course/modules/E/E3/project.html:57, 148", "PASS",
    "printed twin output (run_labs PASS): CRRA 496/500, prospect -30/500; P(A) 0.480149, log -0.733658; sum -2.302315; pair 2 sure 3000 both models and prospect -762; all match the prose")
row("lab2-prose-numbers", "Lab 2 prose numbers", "course/modules/E/E3/project.html:153, 197", "PASS",
    "printed: -0.765595182, -0.625595182, P(A)=0.465057055; z = 2*(1500-2200)/10000 = -0.14; all match")
row("lab3-prose-numbers", "Lab 3 prose numbers", "course/modules/E/E3/project.html:395, 607-614, 708, 719, 731", "PASS",
    "printed (labs_check and run_labs PASS): gamma_hat 0.6352, lambda_hat 6.1503, kappa_hat 2.0201, se 0.32/9.59/1.86, log-lik -7.1445, score 3.55e-10, 11 of 12 mixed; all match the page")
row("lab-twins-isolated", "each project twin runs alone under python -I -W error", "tests/labs/E3/lab-E3-project-1..3.py", "PASS",
    f"{S}/labs_check.out: lab-E3-project-1, -2, -3: twin rc=0, stderr_bytes=0")
row("lab-page-code-equals-twin", "page code equals its twin (Lab 2 is a completion lab)", "course/modules/E/E3/project.html Labs 1-3", "PASS",
    f"{S}/labs_check.out: Labs 1 and 3 page code equals the twin exactly; Lab 2 differs from its twin only on the two '___' blank lines (run_labs completion rule, tools/run_labs.py:77-86 passes)")
row("lab-expected-equals-output", "expected block equals the twin's output", "course/modules/E/E3/project.html Labs 1-3", "PASS",
    f"{S}/labs_check.out: expected_equals_output=True for all three labs")
row("instance-docstring-claims", "instance.py docstring claims", "course/modules/E/E3/grader/instance.py:1-33, 45-52, 148-261", "PASS",
    C % "grader/instance.py" + "read in round 10; the seed facts it implies are re-derived in fixed_participants.out (seeds 0, 7919, 30, 49, n=200)")
row("grader-messages-never-print-answer", "failure messages name the property and never print an answer",
    "course/modules/E/E3/grader/test_project.py:45-64, 251-285 and every expect()", "PASS",
    "read every expect/pytest.fail call in the file (including the new test at 873-900): fixed strings; the only formatted messages print the model name tested (line 311) or the condition label")
row("grader-gamma0-exact-convention", "gamma = 0 exact half-cent convention", "project.html:221; grader/test_project.py:144-149; grader/reference.py:122-124", "PASS",
    C % "project.html lines 1-391 and reference.py" + "reference sums Fraction products and rounds once with floor(x + 1/2); test compares with the test's own nearest() (line 67-69)")
row("grader-seed49-se-docstring-numbers", "seed-49 standard-error numbers in the docstring", "grader/test_project.py:1064-1075", "PASS",
    f"Re-derived with the reference on seed 49 ({S}/docstring_numbers_r11.out): se_lambda 135.054074 (1e-5) and 97.674709 (1e-6); se_gamma 0.09474 and 0.07983; reverse order 136.779 (+1.28%) and 98.086 (+0.42%); -27.7 percent and -15.7 percent; all match the docstring (its 97.67 is 97.6747 rounded)")
row("grader-allA-docstring", "all-A degenerate-set numbers in the docstring", "grader/test_project.py:903-910", "PASS",
    f"{S}/docstring_numbers_r11.out: all-A kappa_hat 924.73 (~925), se_lambda 692051.98 (>1e5), se_kappa 1981269 (>1e5), se_gamma 692.39 (about 692); match the docstring")
row("grader-seed30-kappa-below-one", "fixed participant seed 30 has kappa below 1", "grader/instance.py; grader/test_project.py:36", "PASS",
    f"{S}/fixed_participants.out: seed 30 true kappa 0.635; reference kappa_hat 0.8973 < 1")
row("grader-seed49-lambda-above-ten", "fixed participant seed 49 has lambda_hat above 10", "grader/test_project.py:37, 664-694", "PASS",
    f"{S}/fixed_participants.out: seed 49 reference lambda_hat 20.6864 > 10")
row("grader-recovery-47-of-50", "recovery threshold", "grader/test_project.py:601-616", "PASS",
    f"run_graders 0-49 PASS (the recovery test runs in every seed's suite run, the reference passes all 50); the threshold 47 is the page's (project.html:213)")
row("grader-second-participant-and-clamp", "second participant and the clamp checks", "grader/test_project.py:619-642; instance.py", "PASS",
    f"reference passes (run_graders PASS); mutants e3d4_05 and r9e_04 and r9e_01 are killed (mutate_E3_seeds0-9.out); {S}/tell_apart_ref.out: 53 participants (seeds 0-49, 7919, 30, 49) with worst score 2.3e-7")
row("convention-whole-cents", "whole-cent convention", "project.html:221; grader/reference.py:71-73, 118-128", "PASS",
    C % "project.html lines 1-391 and reference.py" + "floor(c + 1/2) in _half_up; gamma = 0 CRRA exact path; no other money rounding")
row("concept-links-definitions-carried", "concept links at project.html:205, 207", "course/modules/E/E3/project.html:205, 207", "PASS",
    C % "project.html lines 1-391" + "link targets unchanged; check_dag PASS; page_smoke PASS")
row("rung1-lab-answers-claim", "Lab 1 prints what project.html:44 says", "course/modules/E/E3/project.html:44; tests/labs/E3/lab-E3-project-1.py", "PASS",
    C % "project.html lines 1-391 and lab-E3-project-1.py" + "Lab 1 prints per pair the CRRA and prospect CEs, P(A), the chosen log-probability; the total for pairs 1-3 (run_labs PASS)")
row("relaxed-test-kills-unchanged", "local-maximum test (lambda move restored) kills the lambda-frozen mutants", "course/modules/E/E3/grader/test_project.py:586-598", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: r9_01, r9_02, r9_03 KILLED; the local-maximum lines unchanged")
row("mut-r9-01-lambda-frozen-at-grid-value", "student-error mutant", "ledgers/E3/mutants/r9_01_lambda_frozen_at_its_grid_value.py", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: KILLED r9_01 -> test_estimate_returns_the_named_fields_as_finite_floats (seed 0). Carried from round 10 (the file is byte-identical since the previous pin)")
row("mut-r9-02-lambda-climbs-downhill", "student-error mutant", "ledgers/E3/mutants/r9_02_lambda_climbs_downhill.py", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: KILLED r9_02 -> test_score_is_zero_at_the_estimate (seed 0). Re-run this round")
row("mut-r9-03-lambda-reported-as-its-log", "student-error mutant", "ledgers/E3/mutants/r9_03_lambda_reported_as_its_log.py", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: KILLED r9_03 -> test_reported_log_likelihood_is_the_likelihood_at_the_estimate (seed 0). Re-run this round")
row("mut-r9-04-convergence-ignores-lambda", "within-tolerance candidate (not a grader mutant; kept out of ledgers/E3/mutants)",
    "ledgers/E3/scripts/E3-d-r9/within_tolerance/r9_04_convergence_test_ignores_lambda.py", "PASS",
    "Carried from round 10 (candidate byte-identical): meets the page's 2e-5 score tolerance on seeds 0-9 in round 10 (suite_out/cand_r9_04.out); not counted as a mutant")
row("mut-d10-02-likelihood-uses-crra-ce", "student mutant: the likelihood uses CRRA certainty equivalents",
    "ledgers/E3/mutants/d10_02_likelihood_uses_crra_certainty_equivalents.py", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: KILLED d10_02 -> test_log_likelihood_matches_oracle_at_the_true_parameters")
row("mut-d10-03-estimate-drops-pure-responses", "student mutant: the estimator drops responses with two pure lotteries",
    "ledgers/E3/mutants/d10_03_estimate_drops_the_pure_responses_first.py", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: KILLED d10_03 -> test_reported_log_likelihood_is_the_likelihood_at_the_estimate (seed 0)")
row("mut-e8-01-se-diagonal-only", "student-error mutant", "ledgers/E3/mutants/e8_01_se_from_inverse_of_the_diagonal_only.py", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: KILLED -> test_standard_errors_match_the_coordinate_change_oracle")
row("mut-e8-02-crra-zero-wealth-allowed", "student-error mutant", "ledgers/E3/mutants/e8_02_crra_allows_final_wealth_of_exactly_zero.py", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: KILLED -> test_crra_requires_wealth_plus_every_prize_to_stay_positive")
row("mut-e8-03-prospect-loss-weight-on-gains", "student-error mutant", "ledgers/E3/mutants/e8_03_prospect_loss_weight_also_scales_the_gain_branch.py", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: KILLED -> test_prospect_matches_oracle_for_instance_lotteries")
row("mut-e8-04-prospect-adds-wealth", "student-error mutant", "ledgers/E3/mutants/e8_04_prospect_model_adds_wealth_to_each_prize.py", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: KILLED -> test_prospect_matches_oracle_for_instance_lotteries")
row("mut-e8-05-model-name-type-error", "student-error mutant", "ledgers/E3/mutants/e8_05_model_name_error_raises_type_error.py", "PASS",
    f"{S}/mutate_E3_seeds0-9.out: KILLED -> test_model_name_must_be_crra_or_prospect (seed 0)")
row("alt-1-2-3-5-seeds-0-9", "alternatives 1c (grid zoom + Newton), 2c (Newton FD 1e-6 damped), 3 (Nelder-Mead + Newton), 5 (exp/log float CE): seeds 0-9 under the current suite",
    "ledgers/E3/scripts/E3-d-r10/alts/{alt1c_zoom_then_reference_newton, alt2c_newton_fd1e-6_damped, alt3_nelder_mead_v2, alt5_exp_log_float}/elicit.py", "PASS",
    f"{S}/alts_out: alt2c 10/10; alt3 10/10; alt5 10/10; alt1c {ALT1C}. alt1c fails seed 2 on test_score_is_zero_at_the_estimate ({S}/alt_seed2_names.out, score 8.8e-4 at step 1e-5 per round 10). Its own stopping rule leaves a non-stationary point at the page's tolerance, so the grader's rejection is correct (not an over-constraint)")
row("alt-4-bisection-seeds-0-9", "alternative 4b: prospect CE by bisection to full precision, then the half-up rule", "ledgers/E3/scripts/E3-d-r10/alts/alt4b_bisection_full_precision/elicit.py", "PASS",
    f"{S}/alts_out/alt4b_bisection_full_precision.out: {ALT4B}")
row("alt-6-finite-difference-step-1e-4", "alternative 6 (FD step 1e-4 in the optimiser, Hessian and standard errors)", "ledgers/E3/scripts/E3-d-r10/alts/alt6_fd_step_1e-4/elicit.py; grader/test_project.py:619-642, 1064-1091",
    "PASS", f"{S}/alts_out/alt6_fd_step_1e-4.out: {ALT6}; {S}/alt_seed2_names.out: seed 2 fails test_score_is_zero_at_the_estimate and test_standard_errors_match_the_coordinate_change_oracle (the alternative's finite-difference step is too coarse for the page's tolerance); not a required implementation")
row("alt-7-armijo-newton-seeds-0-9", "alternative 7 (round 11): finer grid, damped Newton with Armijo backtracking, stdlib only; seeds 0-9 under the current suite",
    f"{S}/alts/alt7_armijo_newton/elicit.py", "PASS",
    f"{S}/alts_out/alt7_armijo_newton.out: {ALT7}. The one failure is seed 9 on test_score_is_zero_at_the_estimate ({S}/alt7_seed9_names.out): the estimate has score 2.8e-4 at step 1e-6 (7.3e-4 at 1e-5), so the alternative returns a non-stationary point (the likely exit is its Armijo loop returning at a step below 1e-14; not instrumented). The page's tolerance (2e-5, project.html:213) rejects it correctly; it is not an over-constraint. Seeds 0-8 pass. The same silent-return defect is in the reference (see ref-suite-fails-generator-seeds).")
row("alt-lambda-local-max-restored-on-alternatives", "the lambda move in the local-max test holds on the alternatives",
    "course/modules/E/E3/grader/test_project.py:586-598", "PASS",
    f"{S}/alt_seed2_names.out and alts_out/*.out: the failing tests of the alternatives at seeds 0-9 and 2 are the score and standard-error tests, never test_estimate_is_a_local_maximum")
row("alt-cross-seed-likelihood", "alternatives' likelihood vs the reference on seeds 0-49", "course/modules/E/E3/grader/test_project.py:619-642",
    "PASS", C % "reference.py, instance.py and the alternatives' elicit.py files" + "ledgers/E3/scripts/E3-d-r10/alts_out/compare_*.txt: no alternative exceeds the reference likelihood")

# ----- every round-10 row id must still be present (rule: keep all row ids)
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-E3-d.round10.json").read_text(encoding="utf-8"))
ids = {r["id"] for r in R}
missing = [r["id"] for r in prev["rows"] if r["id"] not in ids]

NOTES = (
    "Round 11 (E3-d) at ccaeeaf. Delta from 47a36d8c read hunk by hunk: project.html (line 213 grading mode now 48 checks and the "
    "gamma = 1 / prospect-unit phrasing; lines 392-606 Lab 3 hypothesis and code (the lab twin changed the same way); line 646 Exemplar B word count 450), "
    "grader/test_project.py (line 665-668 docstring sentence deleted; new test test_estimate_accepts_a_mixed_lottery_on_the_a_side_alone at 873-900; "
    "lines after 870 shift by +29), tests/labs/E3/lab-E3-project-3.py (twin of Lab 3), 14 new mutant files, references.json (used_by and generated_at only). "
    "Lines of project.html 1-209 and 214-391 and the reference, starter and instance files are byte-identical to the round-10 pin; rows citing only those are carried with the round-10 prefix or re-derived. "
    "The mutation run (tools/mutate_graders.py --unit E3 --seeds 0-9) was started first in the background; it covers the 150 mutant files present at its start. "
    "The four round-11 mutants were run with kill_r11.py (same procedure, seeds 0-9). "
    "Round-10 FAIL rows mut-d10-01, grader-large-lambda-docstring and exemplar-word-count-B are resolved by the pin. "
    "New FAILs: (1) ref-suite-fails-generator-seeds: the reference fails the unchanged suite on generator seeds 108, 157, 165, 269 (0-399 scan); "
    "(2) mut-r11d-02 survives seeds 0-9 and is distinguishable only off the generator; (3) mut-r11d-04 survives seeds 0-9 and no test covers a 12-response MLE. "
    "Observations, not counted as FAIL rows: on seed 49 the reference's point (lambda_hat 20.6864, log-likelihood -126.0315) is a local maximum, and a stationary point at lambda 7.2176 has log-likelihood -125.9315 (round-10 evidence s3d_lam10_reject.out); the page calls the estimate maximum-likelihood, and its suite checks are local by its own wording (project.html:213). "
    "On random 26-31-response participants with extreme parameters the reference raises RuntimeError (trial 8) or returns gamma_hat of about 5e-8 (trials 31, 47), which the page does not name (search_tell.py, trial_detail.out); "
    "the boundary gamma is not an error by the page's open domain but is worth a note for the architect. "
    "Could not check: a real-browser click-through of the questionnaire export; the learner's own elicit.py in Pyodide; the self-assessment form in site.js (outside the slice); cards.json and the lesson texts beyond their anchors and citations (other slices); live verify_refs; the alternatives on seeds 10-49 under the full suite; the reference on the seeds 400+ (the scan stops at 399)."
)
SUMMARY = ""  # filled below

fails = [r for r in R if r["status"] != "PASS"]
fragment = {
    "unit": "E3",
    "slice": "d",
    "round": 11,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 11 (did not build E3)",
    "pin": "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87",
    "base": "47a36d8c (round-10 pin); delta 47a36d8c..ccaeeaf (see notes)",
    "checkout": str(ROOT),
    "scratch": "/Users/billyribeiro/.fanout/scratch-E3-d-r11",
    "verified_at": NOW,
    "verdict": "FAIL" if fails else "PASS",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": "",
}
n_pass = sum(1 for r in R if r["status"] == "PASS")
n_fail = sum(1 for r in R if r["status"] == "FAIL")
n_unv = sum(1 for r in R if r["status"] == "UNVERIFIABLE")
killed = sum(1 for m in mutants if m.get("killed_by"))
fragment["summary"] = (
    f"E3-d round 11 at ccaeeaf: {len(R)} rows: {n_pass} PASS, {n_fail} FAIL, {n_unv} UNVERIFIABLE. "
    f"Mutants: {killed}/{len(mutants)} killed (150 existing: 150/150; round-11 student-error mutants: 2/4). "
    f"Round-10 ids missing from this fragment: {missing or 'none'}."
)
dest = ROOT / "ledgers/E3/E3-d.json"
dest.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
problems = ledger.validate(fragment, "E3-d")
print("wrote", dest, "rows", len(R), "pass", n_pass, "fail", n_fail, "mutants", killed, "/", len(mutants))
print("missing round-10 ids:", missing)
print("validate:", problems)
