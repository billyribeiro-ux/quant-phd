import ast, json, pathlib, re, datetime

CK = pathlib.Path("/tmp/verify-ap1-r6-d")
MUT = CK / "ledgers/AP1/mutants"
LOGPATH = "/tmp/ap1-r5/project/logs/mutate_r6.log"
LOG = pathlib.Path(LOGPATH).read_text(encoding="utf-8").splitlines()

killed = {}
for line in LOG:
    m = re.match(r"(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line)
    if m:
        killed[m.group(2)] = (m.group(1), m.group(3), m.group(4).strip())
files = sorted(MUT.glob("m*.py"))
assert len(files) == 55, len(files)
assert set(killed) == {f.name for f in files}

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

def doc_of(path):
    return ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""

FIX = {
    "proj-spec-invalid-input-claim": (
        "Either (a) make must_raise check each case's message for a short phrase that names its condition (for example "
        "'redundant', 'finite', 'one per asset', 'strictly positive', 'sum to one') without printing the expected value, "
        "so m48 fails and the LinAlgError route fails too; or (b) delete 'with a message that says what was wrong' and its "
        "parenthetical from line 137 and from the starter docstrings, and reword must_raise's failure text, which currently "
        "says the specification requires 'a ValueError naming the violated condition'."),
    "proj-spec-print-warn-claim": (
        "Add a call pricing_errors(TEST, PRICES, sdf) with a finite negative sdf value to the silence test (or a new test "
        "that records warnings as the ill-conditioned test does). The reference passes it; m53 then fails."),
    "proj-mutant-m48": (
        "Make the grader enforce the message (per-case phrase check, see proj-spec-invalid-input-claim) or delete the "
        "message requirement from the spec. The file stays in `mutants`; it is not equivalent and is not removed."),
    "proj-mutant-m53": (
        "Same test as proj-spec-print-warn-claim: a negative finite SDF value in a pricing_errors call under the warnings "
        "recorder. Then m53 fails on seed 0."),
    "proj-mutant-m54": (
        "Add a test that x_star_weights(c*TRAIN, c*PRICES) and recover_sdf accept payoffs scaled by c = 1e-11 (the reference "
        "accepts; m54 raises 'linearly independent columns'). The grader's own comment says the redundancy check must not "
        "depend on absolute size."),
    "proj-mutant-m55": (
        "Add a population_x_star call with state probabilities summing to 1.0005 (reference raises 'probs must sum to one'; "
        "m55 accepts). Keep the reference's 1e-9 rounding tolerance."),
    "proj-data-fx-retrieved-date": (
        "Change the three 'retrieved 2026-10-19' statements (project.html lines 133, 194 and 340) to the date the MANIFEST "
        "records for fx_monthly (2026-10-26), or, if the file was not re-fetched on 2026-10-26, correct the MANIFEST retrieved "
        "and raw_sha256 fields to the values that were fetched and rerun fetch_data --check."),
}

rows = []
rows.append(row("proj-spec-completeness", "2.6-spec",
    "course/modules/AP/AP1/project.html #spec (lines 127-139), #conventions; grader/starter.py; grader/reference.py", "PASS",
    "Re-read as a student. The eight functions in 'Required outputs' are exactly the eight defs of grader/reference.py and "
    "the eight calls in call_every_public_function (test_project.py lines 641-660). The rules a student needs are stated "
    "and tested: divide by T (test_second_moment_matrix_definition), pricing error E[mx]-p (test_pricing_error_sign_and_value), "
    "train-only weights (test_recover_sdf_reports_in_and_out_of_sample_errors), strict x*<0 (test_share_negative_counts_test_rows), "
    "finite inputs and the 63 invalid-input cases (pytest --collect-only, test_invalid_input_raises). Questions I would have "
    "had to ask: none that the graded behaviour depends on. The spec gives no numerical tolerance for 'singular' or "
    "'redundant'; the graded cases are exact dependence (duplicate column; sum of two columns) and an independent sample with "
    "condition number 1.22e8 (test_ill_conditioned_payoffs_emit_no_warning), which 'linearly dependent' accepts."))
rows.append(row("proj-spec-toolchain-claim", "2.6-spec", "course/modules/AP/AP1/project.html line 185", "PASS",
    "Line 185: 'Use Python 3.14 with NumPy 2.4 and pytest 9.0, the versions the in-browser grader runs'. requirements-dev.txt "
    "pins numpy==2.4.6 and pytest==9.0.2; pyproject.toml line 5 requires-python >=3.14; "
    "course/assets/vendor/pyodide/pyodide-lock.json info.python = 3.14.2 and its packages numpy 2.4.6 and pytest 9.0.2; the "
    "vendored wheels numpy-2.4.6-cp314 and pytest-9.0.2-py3-none-any.whl are present; tools/vendor_spec.yaml pins Pyodide "
    "314.0.7 to the same numpy, scipy and pytest. The sentence matches all of them."))
rows.append(row("proj-spec-invalid-input-claim", "2.6-spec",
    "course/modules/AP/AP1/project.html line 137; grader/test_project.py must_raise (lines 64-70)", "FAIL",
    "The parenthetical is accurate: must_raise catches ValueError and returns; it never reads str(error). But line 137 still "
    "states an obligation, 'a message that says what was wrong', and the suite does not enforce it. Mutant m48 (every "
    "validator raises ValueError('invalid input')) is not equivalent (its text differs from the reference's on the same "
    "input) and passes all 97 checks on seeds 0-9 and on seeds 0-49 (own run: 0 failing seeds). The LinAlgError case is the "
    "same gap: LinAlgError subclasses ValueError (checked now: MRO LinAlgError, ValueError, Exception on numpy 2.4.6), so a solution that lets "
    "np.linalg.solve raise passes the type check with a message that does not name the condition. A disclosure does not "
    "make an unchecked requirement checked.", FIX["proj-spec-invalid-input-claim"]))
rows.append(row("proj-spec-print-warn-claim", "2.6-spec",
    "course/modules/AP/AP1/project.html line 137; grader/test_project.py test_every_public_function_is_silent_and_pure, "
    "test_ill_conditioned_payoffs_emit_no_warning", "FAIL",
    "Closed since round 5: m49 (print in min_variance_sdf), m50 (RuntimeWarning in x_star_weights) and m51 (in-place "
    "price change) are killed. The silence test calls all eight public functions on valid inputs and records stdout, stderr, "
    "warnings and argument changes. The ill-conditioned sample has cond(E_T[xx']) = 1.222e8 > 1e6 (asserted in the test; "
    "recomputed here), is valid for every function (reference passes), and is the same on every seed. The claim is universal "
    "('never warn'), though: m53 (pricing_errors warns on a finite negative SDF value) is a warning on a legal input "
    "(demonstrated: reference returns, m53 emits RuntimeWarning) and survives seeds 0-9 and 0-49, because no test calls "
    "pricing_errors with a negative value. The claim is not backed by the suite.", FIX["proj-spec-print-warn-claim"]))
rows.append(row("proj-ladder", "2.6-ladder", "course/modules/AP/AP1/project.html #ladder (lines 40-49), #rungs, #stretch",
    "PASS",
    "Rung 1 = Lab 1, annotated worked example (run_labs PASS). Rung 2 = Lab 2, completion problem graded instantly (run_labs "
    "PASS). Rung 3 = the specification, autograder and report (#spec, #grader-section, #report). Rung 4 = #stretch, open-ended. "
    "Tier M (curriculum/curriculum.json AP1 tier 'M'): 'at the master's tier rungs 1 and 2 are short' is consistent with the "
    "lab lengths. Line 42 changed only by removing 'independent' from the cited claim (see proj-cite-tetzlaff2025cornerstone)."))
rows.append(row("proj-hours-estimate", "2.6-hours", "course/modules/AP/AP1/project.html #hours (Time budget table)", "PASS",
    "My estimate: code 16.5 h (read and setup 1; eight functions with 63 invalid-input cases 8; recover_sdf and composition 3; "
    "run_report 2; local and browser runs 1.5); proof appendix 11 h (A1 2, A2 3, A3 4, A4 2); report body 5 h; self-assessment "
    "and calibration 1.5 h. Total 34 h against the declared 36: 5.6% away, inside the 30% bound. Declared rows sum to 36 "
    "(1+3+1+4+4+1+2+12+6+2); code 16, report 20."))
rows.append(row("proj-line139-grading-claims", "2.6-spec", "course/modules/AP/AP1/project.html line 139 (Grading mode)", "PASS",
    "'97 checks run with warnings as errors': pytest --collect-only gives 97 on every seed 0-49 (proj-test-count). "
    "pytestmark filterwarnings('error') (test_project.py line 31) and -W error in the local command (line 5) are present. "
    "Every category listed exists in the file. Browser: 'All 97 tests pass' (proj-dual-mode)."))
rows.append(row("proj-test-count", "2.6-autograder", "course/modules/AP/AP1/grader/test_project.py; project.html line 139",
    "PASS",
    "Command per seed: QF_SEED=s .venv/bin/python -m pytest --collect-only -q -p no:cacheprovider test_project.py, s = 0..49, in a "
    "scratch copy of reference.py, instance.py, test_project.py. All 50 seeds print '97 tests collected'."))
rows.append(row("proj-graders-0-49", "2.6-autograder", "course/modules/AP/AP1/grader/ (reference.py, test_project.py, instance.py)",
    "PASS",
    "Command: .venv/bin/python tools/run_graders.py --unit AP1 --seeds 0-49 -> 'run_graders AP1: PASS (reference 50/50 seeds, "
    "slowest 0.2 s)', exit 0 (logs/run_graders_r6.log)."))
rows.append(row("proj-instances", "2.6-autograder", "course/modules/AP/AP1/grader/instance.py", "PASS",
    "Sampled 20 of seeds 0-49 with numpy default_rng(2026): [0, 2, 4, 5, 8, 12, 14, 16, 21, 25, 26, 30, 31, 32, 33, 34, 39, 40, 43, "
    "49]. Each: probs sum to one and are positive; m_true > 0; payoffs finite; every price >= 0.3 and prices == payoffs.T @ (probs "
    "* m_true); 6 <= S <= 14 and 3 <= N <= min(S-2, 6); train/test shapes in range; training payoffs with a constant (risky block "
    "when riskless) have full column rank. No invalid instance. Answers differ: 20 distinct x* weight vectors and 20 distinct "
    "(S, N, riskless, T) tuples (seed 0 weights 1.1562, -0.3273, 0.3409; seed 2 weights -0.5948, -0.4038, 1.998)."))
rows.append(row("proj-share-probe-test", "2.6-autograder",
    "course/modules/AP/AP1/grader/test_project.py test_share_negative_uses_the_training_weights", "PASS",
    "Run: run_graders 50/50 PASS. Its share-negative mutants m24, m25, m26 and m34 are killed in the mutate_graders run (log)."))
rows.append(row("proj-messages-no-leak", "2.6-autograder",
    "course/modules/AP/AP1/grader/test_project.py must_raise (line 70), assertion messages, pytest.fail", "PASS",
    "Failure text names the violated property and never prints an expected value (for example 'x* must price every training "
    "payoff exactly in sample'; must_raise prints the case's condition, not the answer). Note for the builder, not a leak: line "
    "70 says the spec requires 'a ValueError naming the violated condition', which the revised page no longer requires; that is "
    "part of proj-spec-invalid-input-claim's fix."))
rows.append(row("proj-dual-mode", "2.6-autograder", "course/modules/AP/AP1/project.html section#grader; tools/page_smoke.py",
    "PASS",
    "Command: .venv/bin/python tools/page_smoke.py --unit AP1 -> 'page_smoke AP1: PASS', with 'in-browser grader: All 97 tests pass on "
    "seed 2010782402 (0.8 s)' on project.html (page_smoke pastes reference.py into the in-browser grader). Local: run_graders 50/50."))

for f in files:
    status, desc, by = killed[f.name]
    doc = doc_of(f)
    rid = "proj-mutant-" + f.name[:3]
    loc = f"ledgers/AP1/mutants/{f.name}; grader/test_project.py"
    if status == "KILLED":
        rows.append(row(rid, "2.6-mutation", loc, "PASS",
            f"Mutant: {doc.splitlines()[0]} mutate_graders --unit AP1 --seeds 0-9 at 653fcee (log {LOGPATH}): KILLED by {by}."))
    else:
        note = {
            "m48": "Not equivalent: its ValueError text differs from the reference's on the same invalid input (for example "
                   "'payoffs must be finite' vs 'invalid input'), and line 137 requires a message that says what was wrong; the "
                   "grader checks only the exception type. SURVIVED seeds 0-9 (log) and seeds 0-49 (own pytest per seed, 0 failing).",
            "m53": "Not equivalent: pricing_errors(TRAIN, PRICES, sdf) with one sdf value -0.5 returns the reference result, while the "
                   "mutant also emits RuntimeWarning (demonstrated by a warnings recorder; the suite runs with -W error, so the "
                   "warning would fail a test that calls it). SURVIVED seeds 0-9 (log) and seeds 0-49 (own run, 0 failing).",
            "m54": "Not equivalent: payoffs and prices scaled by 1e-11 (independent columns, accepted by the reference) make the mutant "
                   "raise ValueError 'linearly independent columns'. SURVIVED seeds 0-9 (log) and seeds 0-49 (own run, 0 failing). "
                   "No test uses a scale below 1e-5 (test_x_star_accepts_small_units).",
            "m55": "Not equivalent: state probabilities summing to 1.0005 raise in the reference ('probs must sum to one') and are "
                   "accepted by the mutant. SURVIVED seeds 0-9 (log) and seeds 0-49 (own run, 0 failing). No test probes a sum "
                   "between 1+1e-9 and 2.",
        }[f.name[:3]]
        rid_fail = {"m48": "proj-mutant-m48", "m53": "proj-mutant-m53", "m54": "proj-mutant-m54", "m55": "proj-mutant-m55"}[f.name[:3]]
        rows.append(row(rid, "2.6-mutation", loc, "FAIL",
            f"Mutant: {doc.splitlines()[0]} {note}", FIX[rid_fail]))

rows.append(row("proj-mutation-run", "2.6-mutation", "ledgers/AP1/mutants/ (55 files); grader/test_project.py", "FAIL",
    "Command: .venv/bin/python tools/mutate_graders.py --unit AP1 --seeds 0-9 -> 'mutate_graders AP1: FAIL (51/55 killed)', exit 1 "
    "(log " + LOGPATH + "). Survivors: m48, m53, m54, m55 (rows above). Killed: 51, including the new m52 (sdf_values warns on a "
    "negative value, killed by test_ill_conditioned_payoffs_emit_no_warning).",
    "Fix the four survivors (see their rows). Then rerun mutate_graders --unit AP1 --seeds 0-9 and require 55/55."))
rows.append(row("proj-mutant-equivalence", "2.6-mutation", "ledgers/AP1/mutants/", "PASS",
    "No listed mutant is equivalent. For each survivor an input distinguishes it from the reference: m48 by the message text of "
    "the same invalid input; m53 by pricing_errors with a finite negative SDF value (warning); m54 by payoffs scaled 1e-11 "
    "(raise); m55 by probabilities summing to 1.0005 (accepted). Demonstration script run in scratch: "
    "/tmp/ap1-r5/project/surv/demo.py, outputs recorded in this round's notes."))
rows.append(row("proj-lab-project-1", "2.5-labs", "course/modules/AP/AP1/project.html #lab-AP1-project-1; tests/labs/AP1/lab-AP1-project-1.py",
    "PASS",
    "run_labs --unit AP1 -> PASS 22/22, includes lab-AP1-project-1. Output matches the page's expected block (E[x x'] = [[1.0, 1.05], "
    "[1.05, 1.185]]; determinant 0.0825; b = (1.367273, -0.387879); x* = (0.824242, 0.940606, 1.134545)) and the interpretation's "
    "0.22303 / 0.775758 sample weights and out-of-sample errors about 5 and 10 cents (0.0485, 0.0964)."))
rows.append(row("proj-lab-project-2", "2.5-labs", "course/modules/AP/AP1/project.html #lab-AP1-project-2; tests/labs/AP1/lab-AP1-project-2.py",
    "PASS",
    "run_labs PASS (22/22). Recomputed by running the twin with an appended print: weights [1.9386 0.0537 -0.0123 -1.0058], "
    "max in-sample error 3.3e-16, out-of-sample [-0.00619 0.00056 0.01017 -0.00345]; mean of x* = 0.98695, so the riskless weight "
    "1.93856 is 1.96 times the sample x* mean ('nearly twice', derived on the page as shown). The interpretation's 'twice the SDF's "
    "mean' is supported to that precision."))
rows.append(row("proj-lab-project-3", "2.5-labs",
    "course/modules/AP/AP1/project.html #lab-AP1-project-3; tests/labs/AP1/lab-AP1-project-3.py; course/assets/data/market/fx_monthly.csv",
    "PASS",
    "run_labs PASS (22/22). Independent recomputation from the CSV (scratch recompute.py, numpy only, no lab code): payoffs AUD, CAD, CHF, "
    "EUR, GBP, JPY, NOK, NZD, SEK; train 1999-02..2012-11 (166), test 2012-12..2026-09 (166); checksums sum 2989.0264134608 and sum of "
    "squares 2992.6599604987 (matches); out-of-sample bp AUD 249.4, CAD 266.3, CHF 289.2, EUR 295.1, GBP 301.4, JPY 243.7, NOK 248.1, "
    "NZD 259.0, SEK 271.2 (all match); rms 270.0 bp; benchmark 20.1 bp; x* train mean 0.9981, sd 0.1824; test share negative 0.0000, "
    "min 0.0401; mean(x*)^2 + sd^2 = 1.02955 = E_T[x*^2]. The in-sample maximum is 2.0e-15 in my operation order against the lab's "
    "1.1e-14: both are rounding and the page calls it rounding; not a mismatch of substance."))
rows.append(row("proj-data-fx-licence", "2.8-data", "course/modules/AP/AP1/project.html Inputs and Lab 3; tools/data_sources.yaml fx_monthly; course/assets/data/market/MANIFEST.json",
    "PASS",
    "licence_url https://www.federalreserve.gov/disclaimer.htm fetched (HTTP 200, 2026-10-26). Quoted text found at character offset 9390 of the "
    "tag-stripped text: 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed "
    "without permission. Please cite to the Board as the source of the information.' That grants redistribution. MANIFEST licence string "
    "matches. fetch_data --check: 3 datasets, 0 problems."))
rows.append(row("proj-data-fx-retrieved-date", "2.8-data",
    "course/modules/AP/AP1/project.html lines 133, 194 and 340; MANIFEST.json fx_monthly.retrieved", "FAIL",
    "MANIFEST fx_monthly now records retrieved 2026-10-26 and raw_sha256 17d087d0... (changed from 8f370f9c... in this delta; processed "
    "sha256 60572240... unchanged). The page still says 'retrieved 2026-10-19' in the Inputs paragraph (line 133), the Lab 3 hypothesis "
    "(line 194) and Exemplar B's data section (line 340). The dataset's stated date and the page disagree.",
    FIX["proj-data-fx-retrieved-date"]))
rows.append(row("proj-fetch-data-check", "2.8-data", "course/assets/data/market/MANIFEST.json; tools/fetch_data.py", "PASS",
    "Command: .venv/bin/python tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems', exit 0 (logs/fetch_data_r6.log)."))
rows.append(row("proj-rubric-observable", "2.6-rubric", "course/modules/AP/AP1/project.html table#rubric (C1-C6 x 4 levels), row C3",
    "PASS",
    "Read every cell. C3 level 4 now names observable elements: the direction of the bias ('the sample second moment is at least E[x*^2] "
    "on average') and the riskless case ('the mean is pinned, so the whole bias sits in the variance'). Both are statements a reader can "
    "check in the report; the expression is mathematically right (E[f(S_hat)] >= f(S) by Jensen, with E[S_hat] = S; with a riskless "
    "payoff the sample mean of x* is fixed at p_0). Other cells name elements a reader can find (assumptions, a named inequality, a unit, "
    "a named section). C4 level 4 'says what its size implies for the variance bound' is a link the report either makes or does not."))
rows.append(row("proj-rubric-calibration", "2.6-rubric", "course/modules/AP/AP1/project.html #exemplar-a, #exemplar-b, #self-assessment", "PASS",
    "Blind re-score from the rubric and the memo passages (not the annotations): Exemplar A 2,2,1,2,2,2 (C3 1: no A3); Exemplar B 4,4,4,4,3,4 "
    "(C3 4: A3 states the upward bias, the strict and zero cases, the convexity sup argument with Jensen, and the riskless pinned mean; C5 3: "
    "the in-sample and out-of-sample errors are read, but no separating check is proposed). Official data-scores: A 2,2,1,2,2,2; B 4,4,4,4,3,4. "
    "Every criterion within one level (in fact exact). Caveat: the same file holds the official scores, so this is a re-derivation with that "
    "knowledge, not a fully blind pass."))
rows.append(row("proj-exemplar-word-counts", "2.6-rubric", "course/modules/AP/AP1/project.html #exemplar-a, #exemplar-b (memo text)", "PASS",
    "Counted tokens (whitespace-separated) inside the memo-text blocks, headings excluded. Exemplar A body = 51 (Summary) + 52 (Data and "
    "method, Out-of-sample) = 103, matching its annotation. Exemplar B body = 59 (Summary) + 224 (Data and method, In-sample) + 313 "
    "(Out-of-sample, Limitations) = 596, matching its annotation; Summary 59 <= 100."))
rows.append(row("proj-exemplar-b-math", "2.6-math", "course/modules/AP/AP1/project.html #exemplar-b, Appendix A1-A4; course/modules/AP/AP1/L04.html Example 5.1",
    "PASS",
    "Re-derived: A1 (E[xx']b = p; positive definite; uniqueness by invertibility); A2 (E[(m-x*)x_n] = 0; E[x* eps] = 0; E[m^2] = E[x*^2] + E[eps^2]); "
    "A3 (E_T[x_hat x] = p; f(A) = sup_c (2c'p - c'Ac) hence convex; E[g_S_hat(c)] = g_S(c); f(S) <= E[f(S_hat)]; strict for N=1 since p^2/s is strictly "
    "convex; riskless mean pinned); A4 (E[m_v] = v; E[m_v x] = v mu + Sigma beta = p; minimality via Cov(eps, m_v) = 0 and Var(m) = Var(m_v) + Var(eps)). "
    "Lesson 4 Example 5.1 recomputed: E[mz] = 0.9 + 0.45 - 0.2 = 1.15; E[z^2] = 3; c = 0.383333; E[x* e3] = -0.095833. Numbers 0.9981^2 + 0.1824^2 = 1.0295 agree with "
    "the computed E_T[x*^2] = 1.029547."))
rows.append(row("proj-exemplar-b-cross-refs", "2.6-rubric", "course/modules/AP/AP1/project.html (all 'Lesson N, <kind> x.y' references)", "PASS",
    "Every referenced result exists as a block-title in its lesson: L04 Theorem 3.2, Theorem 4.1, Example 5.1, Lab 3; L05 Proposition 1.2, "
    "Theorem 2.1, Proposition 2.2, Proposition 2.3, Theorem 2.4, Problem R3 (id R3); L07 Definition 1.1, Definition 4.1, Proposition 2.1, "
    "Theorem 3.3, Lemma 3.2, Lab 2; L01 Lab 2 (R^2 0.99891, line 308 in lab-AP1-L01-2); L07 Lab 2 (ridge 80.2 bp, line 274 in lab-AP1-L07-2)."))
rows.append(row("proj-self-assessment-form", "2.6-rubric", "course/modules/AP/AP1/project.html #self-assessment; course/assets/js/rubric.js (byte-identical since 33fd452)",
    "PASS",
    "Chromium drive (scratch form_drive.py, playwright, static server on 127.0.0.1): 72 radios in three targets (self, exemplar-a, exemplar-b); "
    "scored the exemplars with A 2,2,1,2,2,2 and B 4,4,4,4,3,4 and self 3s, clicked 'Reveal the official scoring': the comparison table shows "
    "the official scores 2,2,1,2,2,2 and 4,4,4,4,3,4, the summaries and the generosity advice render, page errors: none. rubric.js is "
    "byte-identical (git diff --quiet 33fd452 653fcee)."))
rows.append(row("proj-project-numbers", "2.2-numbers", "course/modules/AP/AP1/project.html (all quoted numbers)", "PASS",
    "Checked each quoted number: 36 h and 16/20 split (proj-hours-estimate); 97 checks (proj-test-count); 63 invalid-input cases (collect); "
    "Lab 1/2/3 outputs (run_labs; Lab 3 recomputed); 270.0 bp, 20.1 bp, per-currency bp, 0.9981, 0.1824, 0.0401, 166 months, 2012-11/12 split "
    "(recomputed); 1.1e-14 (lab output; my 2.0e-15 is rounding); 0.99891 (L01 Lab 2); 80.2 bp (L07 Lab 2, line 274); 1.15, 0.383333, "
    "-0.383333 (L04 Example 5.1, recomputed); 176 effect sizes and 60 studies (OpenAlex abstract)."))
rows.append(row("proj-banned-phrases", "2.9-prose", "course/modules/AP/AP1/project.html", "PASS",
    "Scanned for every banned string in BUILDER_RULES §1 items 2-4 (TODO, TBD, lorem, an ellipsis or '...', 'for brevity', 'details omitted', "
    "'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', "
    "'obviously', 'clearly', 'roughly half', 'historically', 'About 6'): zero hits."))
rows.append(row("proj-verify-refs-live", "2.1-citations", "references/references.json (AP1 entries); tools/verify_refs.py --unit AP1", "PASS",
    "Command: .venv/bin/python tools/verify_refs.py --unit AP1 -> 'live re-verification of AP1: 9 of 560 entries, 0 problems', exit 0 "
    "(network available; no proxy error)."))
rows.append(row("proj-verify-refs-offline", "2.1-citations", "references/references.json (integrity, all 560 entries)", "PASS",
    "Command: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0. (The --unit flag is "
    "live-only; the tool refuses it offline, logged as logs/verify_refs_offline_r6.log.)"))
rows.append(row("proj-registry-used-by", "2.1-citations", "references/references.json used_by; project.html inline claim and Reading list", "PASS",
    "The project page cites eight keys: kalyuga2003expertise and tetzlaff2025cornerstone (inline claim) and cochrane2005asset, hansen1991implications, "
    "harrison1979martingales, harrison1981martingales, delbaen1994general, duffie2001dynamic (Reading list). All eight list AP1 in used_by "
    "(shleifer1997limits also lists AP1; it is not cited on the project page)."))
rows.append(row("proj-cite-kalyuga2003expertise", "2.1-attribution", "course/modules/AP/AP1/project.html #ladder claim (data-cite kalyuga2003expertise tetzlaff2025cornerstone, locator Abstract)",
    "PASS",
    "Kalyuga, Ayres, Chandler & Sweller (2003), 'The Expertise Reversal Effect', DOI 10.1207/s15326985ep3801_4 (registry entry). OpenAlex abstract "
    "(HTTP 200, api.openalex.org/works/doi:...): 'Instructional techniques that are highly effective with inexperienced learners can lose their "
    "effectiveness and even have negative consequences when used with more experienced learners.' The first clause of the claim is that sentence."))
rows.append(row("proj-cite-tetzlaff2025cornerstone", "2.1-attribution",
    "course/modules/AP/AP1/project.html #ladder claim (data-locator 'Abstract'); references/references.json tetzlaff2025cornerstone", "PASS",
    "The word 'independent' is gone from line 42. The claim now reads: 'a meta-analysis of 60 experimental studies (176 effect sizes) finds the "
    "effect, though asymmetric (assisting novices helps more than withholding assistance from experts) and less clear for younger students and "
    "for the humanities and language learning'. OpenAlex abstract (HTTP 200; a secondary copy of the publisher's abstract, which Crossref does not "
    "carry; ScienceDirect not retried): '176 effect sizes from 60 experimental studies'; 'the expertise reversal effect is robust across a wide "
    "variety of contexts'; 'for younger students and some fields of study (i.e., humanities and language learning), the evidence for effectiveness "
    "is less clear'; 'the expertise reversal effect is not symmetrical: providing novices with assistance has a stronger effect than withholding "
    "assistance from experts'. The word 'independent' does not occur in the abstract (checked). Registry entry matches OpenAlex: Tetzlaff, Simonsmeier, "
    "Peters, Brod (2025), Learning and Instruction, DOI 10.1016/j.learninstruc.2025.102142, title identical."))
rows.append(row("proj-atlas-studios", "2.6-atlas-studio", "curriculum/curriculum.json AP1 entry", "PASS",
    "Not applicable: AP1 is a module with a project (curriculum 'project': title SDF recovery, grading 'both'); it has no atlas milestone and no studio "
    "entry, so the atlas and studio checks do not apply. curriculum/curriculum.json is byte-identical since 33fd452 (not in git diff stat)."))
rows.append(row("proj-question-bank", "2.6-rubric", "course/modules/AP/AP1/project.html", "PASS",
    "Not applicable: BUILDER_RULES §5.4 item 4 requires a question bank only for adversarial-review projects (IC defence, debate, referee report). "
    "AP1's project is a code-plus-proof report (curriculum 'deliverable': 'Code plus proof appendix')."))
rows.append(row("proj-check-projects", "2.6-command", "tools/check_projects.py --unit AP1", "PASS",
    "Command: .venv/bin/python tools/check_projects.py --unit AP1 -> 'check_projects AP1: PASS', exit 0."))
rows.append(row("proj-check-pages", "2.9-structure", "course/modules/AP/AP1/*.html (tools/check_pages.py --unit AP1)", "PASS",
    "Command: .venv/bin/python tools/check_pages.py --unit AP1 -> 'check_pages AP1: PASS', exit 0."))
rows.append(row("proj-run-labs", "2.5-labs", "tests/labs/AP1/*.py, course/modules/AP/AP1/*.html", "PASS",
    "Command: .venv/bin/python tools/run_labs.py --unit AP1 -> 'run_labs AP1: PASS (22/22)', exit 0 (logs/run_labs_r6.log)."))
rows.append(row("proj-page-smoke", "2.9-structure", "tools/page_smoke.py --unit AP1 (course pages incl. project.html)", "PASS",
    "Command: .venv/bin/python tools/page_smoke.py --unit AP1 -> 'page_smoke AP1: PASS'; project.html PASS (zero console errors, all math "
    "rendered, no external requests); in-browser grader on reference: 'All 97 tests pass' in 0.8 s; the labs run in the browser."))
rows.append(row("proj-run-graders-command", "2.6-autograder", "tools/run_graders.py --unit AP1 --seeds 0-49", "PASS",
    "Same command as proj-graders-0-49: PASS 50/50, exit 0."))

m = [r for r in rows]
summary_rows = len(rows)
passes = sum(r["status"] == "PASS" for r in rows)
fails = [r["id"] for r in rows if r["status"] != "PASS"]
mutants = []
for f in files:
    status, desc, by = killed[f.name]
    mutants.append({"description": doc_of(f).splitlines()[0],
                    "killed_by": None if status == "SURVIVED" else by.strip()})
frag = {
    "unit": "AP1",
    "slice": "proj-: AP1 project page, grader/ (reference, starter, instance, test_project), project labs 1-3, rubric/exemplars/self-assessment, the project-referenced citations, and ledgers/AP1/mutants/",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent project-slice verifier, round 6 (did not build AP1; no shared context)",
    "pin": "653fcee",
    "base": "33fd452",
    "previous_ledger": "ledgers/AP1/project.json at 33fd452 (round 5, pin 33fd452)",
    "checkout": "/tmp/verify-ap1-r6-d (detached at 653fcee)",
    "scratch": "/tmp/ap1-r5/project/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
    "verdict": "PASS" if not fails else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Round 6 (project slice), pin 653fcee, base 33fd452. No row carried from round 5: project.html changed (lines 42, 137, 139, 185, 262), so every project row was re-derived. Commands on the new pin: run_graders --unit AP1 --seeds 0-49 (PASS 50/50); mutate_graders --unit AP1 --seeds 0-9 (FAIL 51/55; survivors m48, m53, m54, m55); collect-only per seed 0-49 (97 on every seed); page_smoke --unit AP1 (PASS, in-browser 97 on the reference); run_labs --unit AP1 (PASS 22/22); check_projects and check_pages --unit AP1 (PASS); verify_refs --unit AP1 live (9 of 560, 0 problems) and --offline (560 entries, 0 problems); fetch_data --check (3 datasets, 0 problems). Tooling: .venv Python 3.14.8, numpy 2.4.6, pytest 9.0.2 (requirements-dev.txt). New mutants m52-m55 written by this verifier: m52 killed; m53, m54, m55 survive and are FAIL rows. Logs in /tmp/ap1-r5/project/logs/. Decision on m48: not equivalent (message text differs for the same input) and not removed from `mutants`; the claim it tests is still on page line 137. Decision on the invalid-input and print/warn claims: FAIL, because each states a requirement the suite does not enforce (m48; m53). Not verified: the ScienceDirect abstract (not retried; the OpenAlex copy was used, as in round 5). Blind calibration was a re-derivation from the rubric and memo text in a file that also holds the official scores.",
    "summary": {
        "rows": len(rows),
        "pass": passes,
        "fail": len(rows) - passes,
        "unverifiable": 0,
        "mutants": len(mutants),
        "mutants_killed": sum(1 for x in mutants if x["killed_by"]),
        "fail_ids": fails,
    },
}
out = CK / "ledgers/AP1/project.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", passes, "fail", len(rows) - passes, "mutants", len(mutants), "killed", frag["summary"]["mutants_killed"])
print("fail ids", fails)
