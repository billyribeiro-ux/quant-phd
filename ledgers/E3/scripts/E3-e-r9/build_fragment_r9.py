"""Builds ledgers/E3/E3-e.json for round 9 (slice e, pin 1e272e5a) from the round-9 checks and the mutate output."""
import json
import pathlib
import re
from datetime import UTC, datetime

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD9-E3-e")
OUT_SCRIPTS = ROOT / "ledgers/E3/scripts/E3-e-r9"
MUT = ROOT / "ledgers/E3/mutants"
CARRY = "Carried from round 8 (%s byte-identical since the previous pin 2d755599): "
R9 = "Round 9 re-check: "

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- Non-PASS rows (verified FAIL) ----
row("E3e4-exemplar-B-level", "Exemplar levels match the binding plan (exemplar-a level 2, exemplar-b level 4)",
    "course/modules/E/E3/project.html:678 (data-level=\"3\"); plans/E3-build-plan.md:392 (exemplar-b data-level \"4\")",
    "FAIL",
    R9 + "project.html:678 still reads data-level=\"3\" (exemplar A data-level=\"2\" at :625, matching the plan). "
    "plans/E3-build-plan.md:392 still says exemplar-b data-level \"4\"; the plan file is unchanged since 2d755599. "
    "The page's own scores (data-scores 3,3,4,3,3; verdict at :680) give an overall level 3, so page and binding plan disagree.",
    "Architect ruling needed: either the plan's exemplar-b level becomes 3 (and the plan text changes), or exemplar B is "
    "rebuilt to meet level 4 and data-level=\"4\" is set. The builder must not change data-level alone.")
row("E3e-28", "Autograder claims stated on the page (tolerances, oracles, local-maximum check)",
    "course/modules/E/E3/project.html:213 ('moves each of gamma, lambda and kappa in turn'); "
    "course/modules/E/E3/grader/test_project.py:585-592",
    "FAIL",
    R9 + "project.html:213 says the local-maximum check moves each of gamma, lambda and kappa by 0.1 percent up and down. "
    "The suite's test_estimate_is_a_local_maximum (test_project.py:585-592) now moves only gamma and kappa "
    "(commit 1e272e5a); the lambda move was deleted. The page therefore states a check the suite does not run. "
    "All other tolerances stated at :213 match the suite: 46 tests (collect-only), 2e-5 score, 1e-9 likelihood slack, "
    "47 of 50 seeds, four standard errors, seed 30 fixed participant (LOW_KAPPA).",
    "Restore lambda in test_estimate_is_a_local_maximum, or change the page sentence to name the two coordinates AND give "
    "the evidence for dropping lambda (see E3e-r9-02: the reference shows no higher point in lambda on seeds 0-49).")
row("E3e5-03", "Lab-E3-project-3 calls the engine on the reference case (plan 6.1 item 3, binding)",
    "tests/labs/E3/lab-E3-project-3.py:1-188; course/modules/E/E3/project.html:391-399; plans/E3-build-plan.md:292",
    "FAIL",
    "Round 9 re-check: the plan says lab-E3-project-3 'calls the engine on the reference case and prints the estimates'. "
    "The twin imports no elicit module (grep of 'import|elicit' returns only the standard imports math and fractions) and "
    "main() calls its own second_order_search(grid_start()) and observed_information (lab-E3-project-3.py main). "
    "The page (project.html:395) tells the student to replace these with a call to their module, so the lab itself never "
    "calls the engine. Unchanged since 2d755599.",
    "Make the twin call a reference engine (for example by importing the reference estimate under a neutral name) and "
    "print the same lines, or amend plan 6.1 item 3 by architect ruling to say the lab is a standalone reference case.")
row("E3e-51", "Docstring numbers in the new grader test (whether-or-not-chosen fixture)",
    "course/modules/E/E3/grader/test_project.py:806-815 (docstring 'standard errors above 10^5')",
    "FAIL",
    "Round 9 run of the reference on the all-A fixture (scratch /tmp/e3e_r9/allA_check.py): choice precision kappa_hat = 924.73 "
    "(the 'near 925' is correct), se_lambda = 6.92e5 and se_kappa = 1.98e6 (both above 1e5), but se_gamma = 692.39, "
    "which is below 1e5. The docstring says 'standard errors above 10^5' without qualification, so it is false for se_gamma.",
    "Change the docstring to name the two standard errors that exceed 1e5 (se_lambda, se_kappa), or drop the number.")
row("E3e-31", "At least three NEW student-error mutants of the verifier, each killed (window 0-9)",
    "ledgers/E3/mutants/r9e_01_lambda_hat_clamped_at_ten.py; r9e_02_single_start_no_grid_search.py; r9e_03_prospect_ce_returned_in_dollars.py",
    "FAIL",
    "Three mutants written from reference.py (one edit each). r9e_02 is killed on seed 2 (test_score_is_zero_at_the_estimate); "
    "r9e_03 is killed on seed 0 (8 failures). r9e_01 (reported lambda_hat clamped at 10) passes seeds 0-9 and is SURVIVED in "
    "tools/mutate_graders.py --seeds 0-9 (ledgers/E3/scripts/E3-e-r9/mutate_E3_seeds0-9_r9.out: '122 killed, 1 survived'). "
    "On seed 49 it fails 4 tests, the only seed of 0-49 with lambda_hat above 10 (lambda_hat 20.69); no test uses a fixed "
    "participant with large lambda, so the suite kills the error only by chance.",
    "Add a fixed-seed participant with lambda_hat above 10 (as LOW_KAPPA = make_instance(30) does for kappa) to the suite, and "
    "assert the reported lambda equals the likelihood maximiser on it. Then re-run mutate_graders --seeds 0-9.")
row("E3e-r9-02", "Grader docstring claim: lambda 'has kinks where a certainty equivalent changes sign'",
    "course/modules/E/E3/grader/test_project.py:585-588 (docstring of test_estimate_is_a_local_maximum)",
    "FAIL",
    "Evidence against the claim (scratch /tmp/e3e_r9/): (1) with prizes (6200,-15100) at (0.9,0.1), the one-sided difference quotients "
    "of CE in lambda at the sign change of W are -2.0e-3 and -3.3e-2 at gamma 0.4 (step 1e-6, both tending to zero as the step shrinks, "
    "as h^(1/(1-gamma)-1)), so CE is C1 there, with no first-derivative kink. (2) On seeds 0-49, the reference estimate has no "
    "higher likelihood at lambda*(1 +- 1e-3) (lam_check.py: every max gain <= 0) or anywhere on a lambda or gamma scan of +-10 percent "
    "(lam_scan.py: no seed where a nearby point is higher). The docstring's stated reason for dropping lambda is therefore not evidenced.",
    "Remove the kink claim, and either restore the lambda move or justify its removal with a failing implementation and the "
    "tolerance it breaks (note: a score of 2e-5 times a 1e-3 step is 2e-8, above the 1e-9 slack, so the 1e-9 slack can reject a "
    "stationary point in any coordinate, not only lambda).")
row("E3e-r9-03", "Suite coverage of large lambda (lambda_hat above 10)",
    "course/modules/E/E3/grader/test_project.py (no fixed large-lambda participant); ledgers/E3/mutants/r9e_01_lambda_hat_clamped_at_ten.py",
    "FAIL",
    "Of seeds 0-49, lam_hat exceeds 10 only at seed 49 (20.69); every other seed has lam_hat <= 3.6 (lam_check.py output). Seeds 0-9 "
    "never reach that regime, so a student who clamps lambda_hat at 10 passes the 0-9 window and the first ten seeds of any local run.",
    "Add a fixed-seed participant with large lambda, as LOW_KAPPA does for kappa, to the suite (see E3e-31).")

# ---- Rows re-verified in round 9 (PASS) ----
row("E3e-01", "Banned strings in learner-visible prose; ellipsis outside code",
    "course/modules/E/E3/project.html; grader/*.py; tests/labs/E3/lab-E3-project-*.py; index.html",
    "PASS", R9 + "grep (case-insensitive) for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, "
    "you can add more, important to note, studies show, experts agree, well known, obviously, clearly, can be shown: no match on the page, the "
    "grader, the twins or the hub. The only 'final-' match (project.html:148) is 'final-wealth'. No ellipsis outside code (grep '...' and U+2026: none).")
row("E3e-02", "Process words in learner text",
    "course/modules/E/E3/project.html; grader/*.py; tests/labs/E3/lab-E3-project-*.py",
    "PASS", R9 + "grep for builder, verifier, architect, ruling, ledger, fragment, 'round N', reviewer, FINAL-, open item over the same files: no match. "
    "'pin' occurs only as 'pin down' (project.html:395, :708).")
row("E3e-03", "Process references in learner-visible code and docstrings",
    "course/modules/E/E3/grader/*.py; tests/labs/E3/lab-E3-project-*.py",
    "PASS", R9 + "the same grep over grader/*.py and the three project twins finds nothing. The changed docstring (test_project.py:585-592) "
    "refers to 'the page' and 'the score test', which are learner-facing references, not process words.")
row("E3e-04", "Links and anchors on project and hub pages; concept links resolve",
    "course/modules/E/E3/project.html (all href); index.html", "PASS",
    R9 + "scripted check of every href in project.html: local '#' anchors resolve to ids on the page; L02/L03/L04/L06 targets resolve "
    "(#def-certainty-equivalent, #def-crra-utility, #def-first-order-stochastic-dominance, #def-prospect-theory); grader and report "
    "links resolve; no external href. Output: no problems.")
row("E3e-05", "Project structure and ladder order",
    "course/modules/E/E3/project.html:40-48 (ladder), 201 (spec), 243 (questionnaire), 356 (budget), 374 (autograder), 387 (report), 747 (stretch), 755 (reading)",
    "PASS", R9 + "ladder read at :40-46 (rungs 1-4 in order; the changed sentence at :41 names both placement conditions, which match "
    "index.html:68 and :142). tools/check_projects.py --unit E3: PASS (gates_r9.out).")
row("E3e-06", "Hours arithmetic: hub split and project table",
    "project.html:33 (data-hours-project=14), :362-368 (table id=hours); index.html:29 (data-hours-lessons=56), :31 (70 hours)",
    "PASS", R9 + "table rows 1+1+3+4+3+2 = 14 (project.html:362-368); data-hours-project=14; eight lessons, each data-hours=7 (L01-L08.html line 2) "
    "= 56; 56+14 = 70 = index.html:31.")
row("E3e-07", "Rung 3 scope matches the curriculum brief",
    "project.html:205-215; curriculum/02-economics-finance-core.yaml:116-123", "PASS",
    R9 + "brief (yaml:116-123): 'estimate ... risk-aversion and loss-aversion parameters by MLE, and report the uncertainty'; deliverable "
    "'Instrument plus estimation report'; grading both. Spec (:205-215) asks for the instrument, the engine and the report, with both "
    "autograder and rubric. It adds kappa as a third estimated parameter, and the page says so.")
row("E3e-08", "Spec completeness: a competent student needs no clarifying question",
    "project.html:200-225 (spec and conventions), :230-238 (exception table)", "PASS",
    R9 + "questions checked: instrument.json keys and types; response keys; probability text forms; the three signatures; params keys per model; "
    "estimate's seven return keys; exception table conditions and message text; whole-cent rule; identification rule. No open question. "
    "The one inaccurate sentence (the local-maximum check) is recorded under E3e-28, not here.")
row("E3e-09", "Rubric C1 observable", "project.html:611 (C1 row)", "PASS",
    R9 + "level 4 names 'lists the pairs with prizes in cents and exact probabilities, and states how many pairs mix'; level 1 'no pair shown'. Observable.")
row("E3e-10", "Rubric C5 observable; exemplar B annotations match descriptors",
    "project.html:616-617 (C5 row); :672, :735-736 (annotations)", "PASS",
    R9 + "C5 level 4 'no locator is stated that was not read' and level 1 'No empirical claim has a grade or a registry key' are checkable on the memo text. "
    "Annotations for B's C5 (:735-736) and A's C5 (:672) match those descriptors.")
row("E3e-11", "Rubric structure: five criteria, four levels; data-criterion and data-level present",
    "project.html:607-617 (table id=rubric); :623-738 (exemplars)", "PASS",
    R9 + "five rows with data-criterion C1-C5 (grep); four level columns; every annotation carries data-criterion and data-level (:635-736).")
row("E3e-12", "Calibration: exemplar scores within one level of annotations (blind scoring)",
    "project.html:609-615 (rubric text), :623-674 (exemplar A), :676-738 (exemplar B)", "PASS",
    R9 + "scored both memos from the rubric text and the memo wording (the annotation text was in the same read, so this is a weak blind). "
    "Exemplar A: C1 2, C2 2, C3 1, C4 2, C5 1 (page 2,2,1,2,1). Exemplar B: C1 3, C2 3, C3 4, C4 3, C5 3 (page 3,3,4,3,3). "
    "All ten within one level; nine exact.")
row("E3e-13", "Word counts quoted for exemplars (memo text, headings included, tags removed)",
    "course/modules/E/E3/project.html:621", "PASS",
    R9 + "scripted count of the memo-text divs (headings included; tags removed with '' or ' '): Exemplar A 117, Exemplar B 450 "
    "(the page now says 450; the previous 435 is corrected). Both match :621.")
row("E3e-14", "Numbers in prose, exemplars, lab expected blocks and grader docstrings re-derived",
    "project.html:53, :57, :138, :143, :147, :148, :383-386, :571-578, :610-721; grader/test_project.py seed-49 docstring", "PASS",
    R9 + "Lab 1 expected block (496, 500, -30, 500, 0.480149, -0.733658, -2.302315) and Lab 2 (-0.765595182, -0.625595182, 0.465057055) and "
    "Lab 3 (0.6352, 6.1503, 2.0201, SE 0.32, 9.59, 1.86, LL -7.1445, score 3.55e-10, 11 of 12 mixed) match the twin output. Lab 3 re-derived "
    "with grader/reference.py (a different optimiser) reproduces every number. Exemplar B facts (prize range -18700..19000, 2-3 prizes, "
    "probabilities sum to 1, pairs 0 and 3) match the lab data. Hours sum 14. 46 tests collected.")
row("E3e-15", "Reading list: registry keys and which lessons cite which key",
    "project.html:757-765 (reading); L02.html:616; L05.html:609; L06.html:531; L07.html:80, :463; L08.html:67, :133, :619-620", "PASS",
    R9 + "Three keys carry graded claims: kahneman1979prospect (L07:80, C, title only), ellsberg1961risk (L08:133, C), gilboa1989maxmin (L08:67, :620, C). "
    "L06:531 cites kahneman1979prospect for no result. pratt1964risk (L02:616) and epstein1989substitution (L05:609) are named without a claim. "
    "The paragraph's statements match.")
row("E3e-16", "Attribution: titles and keys match registry records",
    "project.html:755-765; L02.html:616; L07.html:80; L08.html:67, :133, :619-620; references/references.json", "PASS",
    R9 + "registry: pratt1964risk 'Risk Aversion in the Small and in the Large', Econometrica 1964; kahneman1979prospect 'Prospect Theory: An Analysis "
    "of Decision under Risk', Econometrica 1979; epstein1989substitution (Epstein, Zin 1989); ellsberg1961risk 'Risk, Ambiguity, and the Savage "
    "Axioms', QJE 1961; gilboa1989maxmin 'Maxmin expected utility with non-unique prior', J. Math. Econ. 1989. Lesson statements that name "
    "titles (L07:80, L08:133, L08:67) match these titles and years. No passage locator is claimed.")
row("E3e-17", "Definitions and results cited from the project page exist",
    "project.html:53, :210, :213, :220, :222; L02.html:99, :103; L03.html:173; L06.html:61, :68", "PASS",
    R9 + "L02 Def 1.2 (certainty equivalent, id def-certainty-equivalent, :99); L02 Prop 1.3 (:103); L03 Prop 2.7 affine invariance (:173); "
    "L06 Def 1.2 (:61) and Def 1.3 (:68, p_i > 0); L04 id def-first-order-stochastic-dominance. All present.")
row("E3e-18", "Lab 1 prose vs code and output", "project.html:55-149; tests/labs/E3/lab-E3-project-1.py", "PASS",
    R9 + "twin run under python -I -W error: exit 0, stderr empty, output equal to the expected block (labs_r9.py). Page code equals twin "
    "(after strip). Prose: CRRA changes from wealth of $1,000.00 (WEALTH=100000); pair 2 sure $30 gain and the $40/$-20 lottery "
    "(B=[4000,-2000], probs 1/4, 3/4) printing -762 match the output.")
row("E3e-19", "Lab 1 hypothesis numbers vs expected block", "project.html:57, :141-147", "PASS",
    R9 + "496, 500, -30, 500, P(A)=0.480149, log -0.733658, sum -2.302315 all equal the printed lines.")
row("E3e-20", "Lab 2 hypothesis numbers and completed formulas", "project.html:153-197; tests/labs/E3/lab-E3-project-2.py", "PASS",
    R9 + "z = 2(1500-2200)/10000 = -0.14; P(A) = 0.465057055; log contributions -0.765595182 (A) and -0.625595182 (B) printed by the twin; "
    "page code equals twin except the two ___ lines (completion rule).")
row("E3e-21", "Lab 3 estimates, standard errors, score, log-likelihood, interpretation", "project.html:391-589; tests/labs/E3/lab-E3-project-3.py", "PASS",
    R9 + "twin output: answers 12, mixed 11, gamma 0.6352 (SE 0.32), lambda 6.1503 (SE 9.59), kappa 2.0201 (SE 1.86), LL -7.1445, score 3.55e-10, "
    "domain True. Interpretation (score is in coordinates; not a maximum check; SE is one standard deviation of an approximation) matches the code.")
row("E3e-22", "Lab and code gates for project labs and grader",
    "tests/labs/E3/lab-E3-project-1..3.py; course/modules/E/E3/grader/", "PASS",
    R9 + "gates_r9.out: run_labs E3 PASS (11/11); ruff check PASS; ruff format --check PASS (15 files); mypy --no-incremental: 385 files, no issues; "
    "pytest tests/test_labs.py -k E3: exit 0. run_graders E3 seeds 0-49 (run_graders_E3_seeds0-49_r9.out): PASS 50/50.")
row("E3e-23", "Mathematics on the page: conventions, identification, delta-method SE convention", "project.html:213-225", "PASS",
    R9 + "conventions read against grader/reference.py: _half_up = floor(y+1/2); gamma=0 exact-sum path (:122-124); logit _logit_sum; SE = "
    "sqrt of diagonal of inverse observed information with the delta factor (estimate). Identification convention re-derived: if the "
    "positive-probability prizes have no gain, W = -lambda*S with S = sum p(-x)^(1-gamma), and c = -(S)^(1/(1-gamma)), lambda-free; "
    "if no loss, W = sum p x^(1-gamma) >= 0 is lambda-free; a zero prize is in the gain branch with v(0)=0. So the lottery's CE depends on "
    "lambda only if it has a positive-probability gain and a positive-probability loss; a pair identifies lambda only if one lottery mixes.")
row("E3e-24", "Notation: symbols and macros vs notation/notation.json", "project.html (math spans); L01-L08 and index (macros); notation/notation.json", "PASS",
    R9 + "notation.json: 8 symbols (Phi, gamma_3, gamma_4 and program-wide ones), 24 macros. Page symbols: gamma, lambda, kappa, zeta, xi, alpha, delta, "
    "W, z, v, P, CE (\\mathrm{CE}), Phi. Phi is registered (M4, standard normal CDF) and used with that meaning (:750). The registry 'about' says "
    "gamma/alpha/lambda-type letters are local and defined where used; each is defined on the page (alpha and delta by Lesson 6 Def 1.2, cited at :49-53 and :220). "
    "gamma_3, gamma_4, \\Prob, \\E and \\Var do not appear on the page. No collision.")
row("E3e-25", "DAG in prose: concepts outside the prerequisite closure", "project.html (visible text, meta description); L02-L08", "PASS",
    R9 + "concept links on the page: prospect-theory (L06), certainty-equivalent (L02), crra-utility (L03), first-order-stochastic-dominance (L04). "
    "Other lessons' names used (Epstein–Zin, maxmin, Pratt) appear only in the reading paragraph and are stated as not implemented. "
    "Prerequisites E1, M4 (plan line 3) cover Phi and the logit/probit context.")
row("E3e-26", "Terms used before definition on the project page", "project.html:53, :205, :213, :220, :223-224", "PASS",
    R9 + "'logit' appears at :50 before its definition, with an explicit forward reference ('which the Choice probability convention of Rung 3 "
    "defines'); certainty equivalent is defined in Lesson 2 and cited; observed information is defined inline at :224; zeta and xi are defined "
    "at :224 before the delta-method sentence.")
row("E3e-27", "Scope words carry a computation or hypothesis (changed prose)",
    "project.html:44, :213, :221, :224, :602-605, :617, :680, :684, :689, :696, :735", "PASS",
    R9 + "each scope word read in context: 'every certainty equivalent ... printed' (:44) is true of Lab 1's output; 'every prize' (:213) names the "
    "homogeneity test; 'Every money output is an int' (:221) is the suite's type check; 'curvature by the all-gain or all-loss pairs' (:696) is "
    "explicitly 'a hypothesis for you to test'; exemplar B's 'every estimate ... is a computed result of Lab 3' (:680) matches the printed lines.")
row("E3e-29", "Reference passes the suite on seeds 0-49", "course/modules/E/E3/grader/reference.py; tools/run_graders.py --unit E3 --seeds 0-49", "PASS",
    R9 + "run_graders E3 --seeds 0-49: 'PASS (reference 50/50 seeds, slowest 20.7 s)', exit 0 (run_graders_E3_seeds0-49_r9.out).")
row("E3e-30", "Re-run all existing mutants (seeds 0-9)",
    "ledgers/E3/mutants/ (123 files: 120 at the pin plus 3 written this round); tools/mutate_graders.py --unit E3 --seeds 0-9", "PASS",
    R9 + "mutate_graders E3 --seeds 0-9 (mutate_E3_seeds0-9_r9.out): 122 of 123 killed. All 120 mutants listed at the pin are killed "
    "(including the round-7 r7_01..03, round-8 e8*/r8_* and the e8e_02/e8e_03 series), plus r9e_02 and r9e_03. The one survivor, "
    "r9e_01, is a new mutant counted under E3e-31.")
row("E3e-32", "Five alternative correct implementations pass (over-constraint check)",
    "ledgers/E3/scripts/run_alternatives.py (alt1..alt5); ledgers/E3/scripts/E3-e-r9/run_alternatives_seeds0-9_r9.out", "PASS",
    R9 + "run_alternatives --seeds 0-9: alt1 PASS 10/10, alt2 PASS 10/10, alt3 PASS 10/10, alt4 PASS 10/10, alt5 PASS 10/10 (exit 0). "
    "Note: this run used the test file as it now stands (without the lambda move); the five alternatives were not run against the restored lambda move.")
row("E3e-33", "Test count on the page equals the collect-only count", "project.html:213 ('runs 46 checks'); grader/test_project.py", "PASS",
    R9 + "pytest --collect-only -q test_project.py: '46 tests collected'.")
row("E3e-34", "Exception table: conditions, types and message text", "project.html:230-238; grader/reference.py:28-60, :116-121; test_project.py:287-386, :630-638", "PASS",
    R9 + "reference messages: 'model must be \"crra\" or \"prospect\"' (ValueError), 'probabilities must sum to 1 (and be non-negative)' (ValueError), "
    "'wealth plus prize must stay positive' (ValueError), and the estimate ValueErrors. Each quoted message contains the table's text. Types match.")
row("E3e-35", "Figures on the page", "course/modules/E/E3/project.html; L02-L08", "PASS",
    R9 + "grep for <svg and <figure in project.html: 0 matches (no figure to verify).")
row("E3e-36", "Registry integrity for the five E3 keys", "references/references.json; tools/verify_refs.py --offline", "PASS",
    R9 + "verify_refs --offline: 'offline integrity: 560 entries, 0 problems' (gates_r9.out). Five keys present (see E3e-16).")
row("E3e-37", "Questionnaire and privacy claims", "project.html:245, :247, :273-353, :376, :778; course/assets/js/grader.js", "PASS",
    R9 + "project.html contains no fetch, XMLHttpRequest or sendBeacon; the questionnaire exports via a Blob download; the only fetch in "
    "the page's scripts is grader.js:18, a same-origin load of the suite files. 'nothing you write leaves it' (footer) holds for the page code.")
row("E3e-38", "Rung 4 is open-ended and not graded", "project.html:747-753", "PASS",
    R9 + "Rung 4 is titled stretch, lists open extensions, and is not in the grading paragraph (:213) or the hours table.")
row("E3e-42", "Rename consistency (zeta, kappa, lambda, gamma, xi)",
    "project.html:203, :213-214, :224; grader/*.py; tests/labs/E3/lab-E3-project-3.py", "PASS",
    R9 + "the page and the grader use gamma, lambda, kappa for the parameters and zeta, xi for the transformed coordinates in the same sense "
    "(grader/reference.py: c, a, b are the transformed coordinates of gamma, lambda, kappa; lab 3: zeta, log lambda, log kappa).")
row("E3e-46", "Same suite passes in Pyodide and locally", "tools/page_smoke.py --unit E3 --pages project", "PASS",
    R9 + "page_smoke --pages project: PASS; 'in-browser grader: All 46 tests pass on seed 683201862'; lab-E3-project-1..3 timings < 0.2 s.")
row("E3e-47", "Hours: verifier estimate of each deliverable vs declared 14 h (30 percent band)", "project.html:362-368", "PASS",
    R9 + "verifier estimates: rung 1 about 1 h; rung 2 about 1 h; instrument and questionnaire file about 3 h; elicit.py with the exception table "
    "and local pass about 5 h; uncertainty and report about 3 h; self-assessment about 2 h. Total 15 h against 14 declared (7 percent).")
row("E3e-48", "SIMULATED labels where generated data is used; no real data", "project.html:44, :53, :57, :376, :393, :396, :549-589; grader/instance.py:1", "PASS",
    R9 + "SIMULATED appears at :44, :53, :57, :376, :393, :396 and the lab 3 hypothesis; instance.py is generated from the seed; the stakes are "
    "described as hypothetical (:716).")
row("E3e-49", "Page smoke: console errors, unrendered math, external requests, 360 px", "course/modules/E/E3/project.html (L02-L08 carried)", "PASS",
    R9 + "page_smoke --pages project: PASS (console, math, requests). L02-L08 pages are unchanged since 2d755599 and were smoked in round 8.")
row("E3e-50", "Over-constraint: a correct implementation that the SE or suite wrongly rejects",
    "grader/test_project.py:918-950 (SE oracle); ledgers/E3/scripts/E3-e-r9/run_alternatives_seeds0-9_r9.out", "PASS",
    R9 + "five different correct implementations (alt1..alt5) pass 10/10 seeds with the SE tests in place (run_alternatives output). "
    "Whether a correct implementation fails the restored lambda move is not checked; see E3e-28.")
row("E3e4-gates", "Repository gates for the E3 project slice (pin 1e272e5a)", "tools/check_pages.py; check_dag.py; check_projects.py; run_labs.py; verify_refs.py --offline; run_graders.py; page_smoke.py; ruff; mypy; pytest tests/test_labs.py -k E3", "PASS",
    R9 + "gates_r9.out: every command exit 0 (check_pages, check_dag, check_projects PASS; run_labs 11/11; verify_refs 0 problems; page_smoke project PASS; "
    "ruff check and format PASS; mypy 385 files clean; pytest test_labs -k E3 exit 0). run_graders seeds 0-49 PASS 50/50. The L02-L08 page_smoke "
    "was not re-run (those pages are unchanged).")
row("E3e4-C2-observability", "Rubric level descriptors observable (C2)", "project.html:612, :630-634, :695-699", "PASS",
    R9 + "C2 level 3 names the value function, logit rule and per-response likelihood term; level 4 names the simplification and which pairs "
    "identify loss aversion and precision: all observable on the memo text.")
row("E3e4-lab3-rederive", "Lab 3 numbers re-derived independently", "project.html:391-589; tests/labs/E3/lab-E3-project-3.py", "PASS",
    R9 + "the 12 lab answers converted to responses and passed to grader/reference.py estimate(): gamma 0.6352, lambda 6.1503, kappa 2.0201, "
    "se 0.32, 9.59, 1.86, log-likelihood -7.1445. Matches the lab's printed values.")
row("E3e4-prizes-mixed", "Exemplar B instrument facts (prize range, prizes per lottery, probabilities sum to 1, pair facts)", "project.html:680-698", "PASS",
    R9 + "scripted from the lab 3 data: prizes -18700..19000; 2 or 3 prizes per lottery; every probability list sums to exactly 1; pair 0 "
    "(6200 w.p. 9/10, -15100 w.p. 1/10 vs three prizes in B) and pair 3 (18800 3/4, -12500 1/4 vs 16500 2/5, -17700 3/5; both mixed) match the memo.")
row("E3e4-identification", "Identification claims (lambda identified only by mixed lotteries; precision claim labelled)",
    "project.html:213, :223, :694, :717", "PASS",
    R9 + "the convention at :223 (new wording) re-derived (see E3e-23). The memo's precision identification at :696 is labelled 'a hypothesis for you to test'.")
row("E3e4-cross-refs", "Cross-references to lessons (Lesson 3 Proposition 2.7; Lesson 6 Definitions 1.2 and 1.3; Lesson 2 Proposition 1.3)",
    "project.html:53, :210, :220; L03.html:173; L06.html:61, :68; L02.html:99, :103", "PASS",
    R9 + "L03 Prop 2.7 is the affine-invariance proposition the page cites (:53), and the page's identity w^(1-gamma) = (1-gamma)u_gamma(w)+1 "
    "follows from L03 :90; L06 Def 1.2 and 1.3 match :220; L02 Prop 1.3 exists (:103).")
row("E3e4-attribution-titles", "Attribution of lesson statements about reading-list papers (title-only claims)",
    "course/modules/E/E3/L07.html:80; L08.html:67, :133, :619-620", "PASS",
    R9 + "titles and years match the registry (see E3e-16); each claim is graded C with 'title only; paper not read'.")
row("E3e4-stretch-phi", "Stretch probit link: Phi against the registry", "project.html:750; notation/notation.json (Phi, module M4)", "PASS",
    R9 + "Phi is registered (M4) as the standard normal CDF; the stretch says 'Phi is the standard normal distribution function'.")
row("E3e4-ruling-392", "Plan's exemplar wording agrees with the architect ruling on excerpts",
    "plans/E3-build-plan.md:392; plans/E3-open-items.md:145-149; plans/FINAL-ARCHITECT-RULINGS.md item 7", "PASS",
    R9 + "plan line 392 and FINAL-ARCHITECT-RULINGS item 7 both say the exemplars are excerpts. Note (not a row FAIL): E3-open-items.md:147 quotes "
    "'103 and 375 words', which are stale; the page now says 117 and 450 (E3e-13). The level disagreement is E3e4-exemplar-B-level.")
row("E3e5-01", "Rung 1 worked example: each step carries a why note (plan 6.1 item 1)", "tests/labs/E3/lab-E3-project-1.py:58-137; project.html:55-57, :138", "PASS",
    R9 + "the twin's comment lines precede each step (pair list, CRRA values, prospect values, logit, log-likelihood).")
row("E3e5-02", "Grader test file type-clean under mypy --strict", "course/modules/E/E3/grader/test_project.py", "PASS",
    R9 + "mypy --no-incremental (repo config): Success, 385 files, no issues (gates_r9.out).")
row("E3e5-03", "Lab-E3-project-3 calls the engine on the reference case (plan 6.1 item 3, binding)",
    "tests/labs/E3/lab-E3-project-3.py; course/modules/E/E3/project.html:391-399; plans/E3-build-plan.md:292", "FAIL",
    "See the FAIL row E3e5-03 above: the twin never calls an engine (no import of elicit); main() uses its own solver.",
    "See E3e5-03 fix (above).")
row("E3e5-04", "Prospect model extends Lesson 6 Definition 1.3 (p_i > 0) to zero-probability prizes", "project.html:220, :225; L06.html:68-69", "PASS",
    R9 + "L06 Def 1.3 requires p_i > 0; the page allows zero probability (:225) and W = sum p_i v(x_i) is unchanged, so a zero-probability prize adds 0. "
    "The extension is stated.")
row("E3e5-05", "Hub ladder text agrees with the spec", "course/modules/E/E3/index.html:146; project.html:207, :213", "PASS",
    R9 + "index.html:146: 'at least 12 pairs with at least one mixed-sign lottery', graded by autograder and rubric, matches the spec (:207, :213).")
row("E3e6-01", "Lab-E3-project-3 docstring describes code that exists", "tests/labs/E3/lab-E3-project-3.py:4-6 (embedded at project.html:398-399)", "PASS",
    R9 + "the docstring names grid_start and second_order_search; both exist in the twin (lines 61-75).")
row("E3e-51", "Docstring number in the new grader test (whether-or-not-chosen fixture)",
    "course/modules/E/E3/grader/test_project.py:806-815", "FAIL",
    "See the FAIL row E3e-51 above: se_gamma = 692.39 is not above 1e5.",
    "See E3e-51 fix (above).")
row("E3e-52", "New grader fixture facts: the B-side lotteries are mixed", "course/modules/E/E3/grader/test_project.py:780-806 (B_SIDE_SURE_A, B_SIDE_LOTTERIES)", "PASS",
    R9 + "imported the module: 12 B lotteries, each mixed (a gain and a loss, positive probability); 12 sure A amounts (single prizes, so pure).")
row("E3e-53", "New zero-prize test: a gain and a zero prize is not mixed", "course/modules/E/E3/grader/test_project.py:696-714", "PASS",
    R9 + "the test is in the 46-test run that passes on every seed 0-49 of the reference (run_graders PASS 50/50).")
row("E3e-54", "Round-7 verifier mutants: three new student-error mutants, each killed",
    "ledgers/E3/mutants/r7_01_*.py, r7_02_*.py, r7_03_*.py", "PASS",
    R9 + "mutate_E3_seeds0-9_r9.out: KILLED r7_01 (test_crra_requires_wealth_plus_every_prize_to_stay_positive, seed 0), r7_02 "
    "(test_log_likelihood_matches_oracle_at_the_true_parameters, seed 0), r7_03 (test_estimate_returns_the_named_fields_as_finite_floats).")
row("E3e-55", "Round-7 Lesson 2 prose (A4 wording, Lab 1 Part A premium, Problem P2, references)",
    "course/modules/E/E3/L02.html:84, :136, :381, :399, :616", "PASS",
    CARRY % "course/modules/E/E3/L02.html and tests/labs/E3/lab-E3-L02-1.py" + "L02 unchanged in the delta 2d755599..1e272e5a.")
row("E3e-56", "Round-7 Lesson 3 references (Module M1 results cited)", "course/modules/E/E3/L03.html:564; course/modules/M/M1/L03.html", "PASS",
    CARRY % "course/modules/E/E3/L03.html" + "L03 unchanged in the delta; M1 is outside the slice and was not changed by the delta either.")
row("E3e-57", "Round-7 Lesson 4 prose", "course/modules/E/E3/L04.html:52, :165-172, :176, :485, :493, :573-579, :591", "PASS",
    CARRY % "course/modules/E/E3/L04.html" + "L04 unchanged in the delta.")
row("E3e-58", "Round-7 Lesson 7 numbers", "course/modules/E/E3/L07.html:86, :88, :92, :98, :127, :334, :336-338, :505", "PASS",
    CARRY % "course/modules/E/E3/L07.html" + "L07 unchanged in the delta.")
row("E3e-59", "Round-7 Lesson 8 prose", "course/modules/E/E3/L08.html:142-160, :412-419, :425, :477, :496, :683, :697", "PASS",
    CARRY % "course/modules/E/E3/L08.html" + "L08 unchanged in the delta.")
row("E3e-60", "Round-7 hub reading paragraph and the Lesson 2 and 3 'name only' statements",
    "course/modules/E/E3/index.html:166; L01.html; L02.html:616; L03.html:564", "PASS",
    CARRY % "course/modules/E/E3/index.html, L01-L03 html" + "none of these files changed in the delta.")
row("E3e-r8-01", "Rung 1 text: 'answers written into the lab ... not generated from the parameters'",
    "course/modules/E/E3/project.html:44; tests/labs/E3/lab-E3-project-1.py:58-64", "PASS",
    R9 + "the twin's pairs are literal lists of prizes, probabilities and the answer (lines 58-64), not generated from GAMMA/LAMBDA/KAPPA.")
row("E3e-r8-02", "Whole-cents exception at gamma = 0 (CRRA): exact Fraction sum before the single rounding",
    "course/modules/E/E3/project.html:221; grader/reference.py:122-124; grader/test_project.py:146, :264, :281", "PASS",
    R9 + "reference.py:122-124 sums Fraction(p*x) exactly and returns floor(sum + 1/2); the page bullet at :221 states this.")
row("E3e-r8-03", "Exemplar B C4 misses text (round-8 change at :720)", "course/modules/E/E3/project.html:720-724", "PASS",
    R9 + "C4 level 4 miss reads: 'states no direction of bias for either limit; ...' (:724), matching the level 4 descriptor (direction of bias).")
row("E3e-r8-04", "Grader test messages changed at :251-288", "course/modules/E/E3/grader/test_project.py:251-288", "PASS",
    CARRY % "course/modules/E/E3/grader/test_project.py:251-288 (not in the delta hunk)" + "the delta changed only test_project.py:585-592.")
row("E3e-r8-05", "Lesson 2 hypothesis (:209): \\Var macro, numbers and predictions", "course/modules/E/E3/L02.html:209; tests/labs/E3/lab-E3-L02-1.py", "PASS",
    CARRY % "course/modules/E/E3/L02.html and lab-E3-L02-1.py" + "neither file changed in the delta.")
row("E3e-r8-06", "Lesson 4 hypothesis and :493 bullet", "course/modules/E/E3/L04.html:98, :150, :176, :493; tests/labs/E3/lab-E3-L04-1.py:8-14, :108-120", "PASS",
    CARRY % "course/modules/E/E3/L04.html and lab-E3-L04-1.py" + "neither file changed in the delta.")
row("E3e-r8-07", "FINAL-ARCHITECT-RULINGS item 11 (rung 2 completion blanks) and the lab twin",
    "plans/FINAL-ARCHITECT-RULINGS.md:24-25; tests/labs/E3/lab-E3-project-2.py; course/modules/E/E3/project.html:151-198", "PASS",
    CARRY % "plans/FINAL-ARCHITECT-RULINGS.md lines 24-25 and lab-E3-project-2.py" + "the file gained a new item 12 at its end (M3 concept); item 11 is unchanged; the lab twin is unchanged.")
row("E3e-39", "Suite gap: named probability condition for log_likelihood",
    "course/modules/E/E3/grader/test_project.py:458-507", "PASS",
    CARRY % "test_project.py:458-507" + "the delta touches only :585-592.")
row("E3e-40", "Numbers in grader docstrings (seed-49 standard errors and reverse-order shifts)",
    "course/modules/E/E3/grader/test_project.py (test_standard_errors_match_the_coordinate_change_oracle, :981-1018)", "PASS",
    CARRY % "test_project.py:981-1018" + "the delta touches only :585-592.")
row("E3e-41", "Equivalent-mutant README for a survivor", "ledgers/E3/equivalent/", "PASS",
    R9 + "ledgers/E3/equivalent does not exist (ls: No such file). No survivor is claimed as equivalent; the one survivor (r9e_01) is a fault, not an equivalent mutant.")
row("E3e-43", "Instance docstring vs code", "course/modules/E/E3/grader/instance.py:11-14, :17-19", "PASS",
    CARRY % "grader/instance.py" + "instance.py is not in the delta. Round 9 also validated all 50 seeds' instances (sum to 1, whole cents, distinct answers).")
row("E3e-44", "Dominance witnesses and verdict oracle (FOSD and SOSD)",
    "course/modules/E/E3/grader/test_project.py:1106-1165", "PASS",
    CARRY % "test_project.py:1106-1165" + "the delta touches only :585-592. The page's dominance sentence (:213) was re-read against :1049-1120 (DOMINANCE_SLACK = 1 cent, distribution-function and integral verdicts).")
row("E3e-45", "Failure messages name the property and do not leak the answer",
    "course/modules/E/E3/grader/test_project.py:44-63 and every expect()/must_raise call; :251-288", "PASS",
    R9 + "the changed local-maximum message (:591) names the property and carries no value; the expect() helper (:44-49) prints no value; carried for the remaining messages.")
row("E3e-r9-01", "Dominance and identification sentences on the page match the suite (new wording at :213 and :223)",
    "course/modules/E/E3/project.html:213, :223; grader/test_project.py:1049-1120", "PASS",
    R9 + "the new dominance sentence (first order on distribution functions, second order on integrals, one cent) matches _first_order_verdict, _second_order_verdict and DOMINANCE_SLACK = 1. The identification convention (:223) was re-derived (E3e-23).")
row("E3e-r9-04", "Questionnaire regex (new) accepts and rejects the stated probability forms",
    "course/modules/E/E3/project.html:270-281 (isProbability)", "PASS",
    R9 + "node v24 test: accepts '0', '1', '1/2', '9/10', '0/5', '1/1', '1/05'; rejects '2', '00', '01', '1/0', '1.0', '-1/2', '', '1/'. "
    "It also accepts '2/1' (a probability above 1, which the engine's sum check refuses); the page does not claim the browser checks sums.")
row("E3e-r9-05", "Ladder placement sentence matches the hub's placement rule", "project.html:41; index.html:68, :142", "PASS",
    R9 + "index.html:68 'To skip rungs 1 and 2, you must reach the bar and answer both skill checks'; index.html:142 says the same; project.html:41 matches.")
row("E3e-r9-06", "Lab 1 nearest_cent docstring matches the twin", "project.html:74; tests/labs/E3/lab-E3-project-1.py:17", "PASS",
    R9 + "page code equals the twin after strip (labs_r9.py), so the changed docstring is identical in both places.")

# ---- Mutants ----
mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+): (.*?) -> (.*)$")
for line in (OUT_SCRIPTS / "mutate_E3_seeds0-9_r9.out").read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    killed_by = "" if status == "SURVIVED" or killed.strip() == "None" else killed.strip()
    mutants.append({
        "id": fname[:-3],
        "description": desc.strip(),
        "file": f"ledgers/E3/mutants/{fname}",
        "killed_by": killed_by,
    })
assert len(mutants) == 123, len(mutants)

fragment = {
    "unit": "E3",
    "slice": "e",
    "round": 9,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-e, round 9 (did not build E3; read verifier-rules.md, VERIFIER_RULES.md, "
                 "BUILDER_RULES.md, plans/E3-build-plan.md, plans/E3-open-items.md, plans/FINAL-ARCHITECT-RULINGS.md, and the round-8 fragment as context)",
    "pin": "1e272e5a",
    "base": "2d755599 (round-8 pin; round-8 fragment /Users/billyribeiro/.fanout/frags/D-E3-e.round8.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD9-E3-e",
    "scratch": "/tmp/e3e_r9/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 2d755599..1e272e5a inside the slice, read in full: project.html (ladder :41; rungs :53; lab 1 docstring :74; spec and conventions "
        ":213-225 incl. dominance, identification and the JS regex and no-choice message at :270-340; exemplar A text unchanged; exemplar B word count "
        "and the 'stakes hypothetical' and 'identify' hunks at :680-716; hours wording :365); grader/test_project.py:585-592 (local-maximum test: lambda "
        "removed); tests/labs/E3/lab-E3-project-1.py:17 (docstring only); plans/FINAL-ARCHITECT-RULINGS.md (item 12 appended, M3 concept, out of slice). "
        "cards.json and curriculum/01-foundations.yaml changed in the delta and are outside slice e (no cards).",
        "Changed-subject rows re-verified this round: E3e-01..E3e-27 (project page), E3e-28 (FAIL), E3e-30..E3e-38, E3e-42, E3e-45, E3e-46..E3e-50, "
        "the E3e4 and E3e5 rows, and the three E3e-r9 rows. Carried rows name their cited files as byte-identical since 2d755599.",
        "Stale figures: plans/E3-open-items.md:147 quotes exemplar word counts 103 and 375; the page now counts 117 and 450 (verified). "
        "Not a FAIL row (the ruling is historical wording), but the ruling should be refreshed with the next architect ruling.",
        "Mutate window: 122 of 123 killed on seeds 0-9. The survivor r9e_01 is killed on seed 49 only (4 tests); see E3e-31 and E3e-r9-03.",
        "Alternatives: five correct implementations pass seeds 0-9. None of them was run against a restored lambda move, so whether a correct "
        "implementation would be over-constrained by that move is not measured (E3e-28 fix).",
        "Blind scoring of exemplars (E3e-12) was weakened: the annotation text was in the same read as the memo text.",
    ],
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = (
    f"{len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
    f"Mutants: {len(mutants)} listed; {sum(1 for m in mutants if m['killed_by'])} killed; 1 survivor (r9e_01 at seeds 0-9, killed on seed 49). "
    "Alternatives alt1..alt5: PASS 10/10 seeds each. Gates: ledgers/E3/scripts/E3-e-r9/gates_r9.out. Lab run: labs_r9.py output in the same folder."
)
out_path = ROOT / "ledgers/E3/E3-e.json"
out_path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out_path, len(rows), "rows", counts, "mutants", len(mutants))
