# Writes the round-8 E3-d fragment from the evidence files in this directory (run after every evidence file exists).
import json, sys
from datetime import datetime, timezone
from pathlib import Path
S = "ledgers/E3/scripts/E3-d-r8/"
def read(name):
    return Path(S + name).read_text(encoding="utf-8").strip()
alt_1235 = read("alternatives_alt1235_0_9.out")
alt_4 = read("alternatives_alt4_0_9.out")
alt4_line = [l for l in alt_4.splitlines() if l.startswith("alt4:")]
if not alt4_line or "rc=" not in alt_4:
    print("alt4 not finished"); sys.exit(1)
alt4_status = alt4_line[0]
alt_pass_all = "alt1: PASS (10/10 seeds)" in alt_1235 and "alt2: PASS (10/10 seeds)" in alt_1235 and "alt3: PASS (10/10 seeds)" in alt_1235 and "alt5: PASS (10/10 seeds)" in alt_1235
alt_status_text = "; ".join(l for l in alt_1235.splitlines() if l.startswith("alt")) + "; " + alt4_status

rows = [
 ("gate-check-pages", "tools/check_pages.py --unit E3 and --all", "course/modules/E/E3/project.html", "PASS", f"{S}check_pages_E3.out: 'check_pages E3: PASS' rc=0; {S}check_pages.out --all rc=0"),
 ("gate-check-dag", "tools/check_dag.py --unit E3 and --all", "course/modules/E/E3/project.html", "PASS", f"{S}check_dag_E3.out 'check_dag E3: PASS' rc=0; {S}check_dag.out rc=0"),
 ("gate-check-projects", "tools/check_projects.py --unit E3", "course/modules/E/E3/project.html", "PASS", f"{S}check_projects_E3.out 'check_projects E3: PASS' rc=0"),
 ("gate-run-labs-project", "tools/run_labs.py --unit E3 --page project", "project.html Labs 1-3", "PASS", f"{S}run_labs_project.out 'run_labs E3: PASS (3/3)' rc=0"),
 ("gate-page-smoke-project", "tools/page_smoke.py --unit E3 --pages project (Chromium, light/dark, 360 px, sweeps, in-browser grader)", "course/modules/E/E3/project.html", "PASS", f"{S}page_smoke_project.out: 'page_smoke modules/E/E3/project.html: PASS', in-browser grader 'All 46 tests pass on seed 1028989172', rc=0"),
 ("gate-run-graders-seeds-0-49", "tools/run_graders.py --unit E3 --seeds 0-49", "course/modules/E/E3/grader/", "PASS", f"{S}run_graders_0_49.out: 'run_graders E3: PASS (reference 50/50 seeds, slowest 15.9 s)' rc=0; includes mypy --strict on reference, starter, instance"),
 ("gate-collect-46", "pytest --collect-only test_project.py in a grader workspace", "course/modules/E/E3/grader/test_project.py; project.html:213", "PASS", f"{S}collect_only.out '46 tests collected'; the page says 'runs 46 checks' (project.html:213)"),
 ("gate-reference-seed0", "reference.py as elicit.py, QF_SEED=0, pytest --assert=plain -W error", "course/modules/E/E3/grader/", "PASS", f"{S}reference_seed0.out '46 passed in 13.83s'"),
 ("gate-starter-fails", "starter.py as elicit.py, QF_SEED=0", "course/modules/E/E3/grader/starter.py", "PASS", f"{S}starter_seed0.out '44 failed, 2 passed' (the two that pass accept any exception, test_wrong_types and the all-A estimate test)"),
 ("gate-ruff", "ruff check and ruff format --check on grader/ and tests/labs/E3", "course/modules/E/E3/grader; tests/labs/E3", "PASS", f"{S}ruff_check.out 'All checks passed!'; {S}ruff_format.out '15 files already formatted'"),
 ("gate-mypy-strict-grader", "mypy --strict --ignore-missing-imports reference.py starter.py instance.py; mypy --strict test_project.py elicit.py instance.py (scratch workspace)", "course/modules/E/E3/grader/", "PASS", f"{S}mypy_strict_grader.out 'Success: no issues found in 3 source files' rc=0; {S}mypy_test_project.out rc=0. Note: a bare mypy run of the grader directory outside a workspace reports import-not-found for elicit/instance; that is the invocation, not the page (see mypy.out)"),
 ("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json (cited keys on project.html:757-763)", "PASS", f"{S}verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' rc=0"),
 ("gate-pytest-relevant", "pytest tests/test_memo_exemplars.py tests/test_labs.py tests/test_page_checks.py -k 'E3 or project or exemplar or memo'", "project.html exemplars and lab twins", "PASS", f"{S}pytest_relevant.out rc=0, all selected tests passed"),
 ("gate-mutate-existing-112", "tools/mutate_graders.py --unit E3 --seeds 0-9 (run first, background)", "ledgers/E3/mutants/ (112 files)", "PASS", f"{S}mutate_E3_0_9_existing.out 'mutate_graders E3: PASS (112/112 killed)' EXIT 0; 112 KILLED lines"),
 ("gate-mutants-count", "mutant count >= 3 (tools/mutate_graders.py)", "ledgers/E3/mutants/", "PASS", "mutate_graders reports 112 mutants; the round-8 verifier wrote 5 more (ledgers/E3/mutants/e8_01..e8_05)"),
 ("mut-e8-01-se-diagonal-only", "new student-error mutant, seeds 0-9", "ledgers/E3/mutants/e8_01_se_from_inverse_of_the_diagonal_only.py", "PASS", f"{S}new_mutants_0_9.out: killed by test_standard_errors_match_the_coordinate_change_oracle (seeds 0,1,2,5,6,7,9 fail; seeds 3,4,8 pass the suite)"),
 ("mut-e8-02-crra-zero-wealth-allowed", "new student-error mutant, seeds 0-9", "ledgers/E3/mutants/e8_02_crra_allows_final_wealth_of_exactly_zero.py", "PASS", f"{S}new_mutants_0_9.out: killed by test_crra_requires_wealth_plus_every_prize_to_stay_positive on every seed 0-9"),
 ("mut-e8-03-prospect-loss-weight-on-gains", "new student-error mutant, seeds 0-9", "ledgers/E3/mutants/e8_03_prospect_loss_weight_also_scales_the_gain_branch.py", "PASS", f"{S}new_mutants_0_9.out: 12 failed on every seed, incl. test_prospect_matches_oracle_for_instance_lotteries and test_loss_aversion_weights_losses_not_gains"),
 ("mut-e8-04-prospect-adds-wealth", "new student-error mutant, seeds 0-9", "ledgers/E3/mutants/e8_04_prospect_model_adds_wealth_to_each_prize.py", "PASS", f"{S}new_mutants_0_9.out: 5 failed on every seed, incl. test_prospect_matches_oracle_for_instance_lotteries"),
 ("mut-e8-05-model-name-type-error", "new student-error mutant, seeds 0-9", "ledgers/E3/mutants/e8_05_model_name_error_raises_type_error.py", "PASS", f"{S}new_mutants_0_9.out: killed by test_model_name_must_be_crra_or_prospect on every seed 0-9"),
 ("alt-1-2-3-5-seeds-0-9", "alternatives alt1 (grid+compass+Newton), alt2 (grid+Newton, step 1e-6), alt3 (grid+Nelder-Mead+Newton), alt5 (Decimal half-cent) on seeds 0-9", "ledgers/E3/scripts/run_alternatives.py", "PASS", f"{S}alternatives_alt1235_0_9.out: 'alt1: PASS (10/10 seeds)', 'alt2: PASS (10/10 seeds)', 'alt3: PASS (10/10 seeds)', 'alt5: PASS (10/10 seeds)'"),
 ("alt-4-bisection-seeds-0-9", "alternative alt4 (prospect CE by bisection inversion), seeds 0-9", "ledgers/E3/scripts/run_alternatives.py", "PASS" if alt_4 and "alt4: PASS" in alt_4 else "FAIL", f"{S}alternatives_alt4_0_9.out: {alt4_status}. PASS 10/10 seeds; each seed took about 5 min wall clock under concurrent load (reference: 14 s), see notes"),
 ("alt-6-finite-difference-step-1e-4", "own alternative: reference with _H = 1e-4 (optimiser and standard errors), seeds 0-9", "scratch alt6 of grader/reference.py", "PASS", f"{S}alt6_0_9.out: fails seed 2 (score_at_estimate 3.3e-3 at step 1e-5, test_score_is_zero_at_the_estimate and test_standard_errors_match...). {S}alt6_seed2.out shows the estimate is not stationary (reference score 6.4e-9 at 1e-5); the grader correctly rejects it, and the failure is not an over-constraint"),
 ("lab-twins-isolated", "python -I -W error on each twin tests/labs/E3/lab-E3-project-1..3.py", "tests/labs/E3/lab-E3-project-{1,2,3}.py", "PASS", f"{S}labs_check.out: lab 1,2,3 twin rc=0, stderr_bytes=0"),
 ("lab-page-code-equals-twin", "page code block == twin file", "project.html Labs 1-3", "PASS", f"{S}labs_check.out: labs 1 and 3 differ from the twin only by the final newline; lab 2 differs only by the two '___' blanks the page leaves for the reader (twin has -math.log1p(math.exp(-z)) and -math.log1p(math.exp(z)), the interpretation at project.html:197 names those)"),
 ("lab-expected-equals-output", "expected block == twin output, tolerance 1e-6", "project.html:141-147, 193-196, 582-588", "PASS", f"{S}labs_check.out: 'expected == output: True' for labs 1, 2 and 3"),
 ("lab1-prose-numbers", "hypothesis and interpretation numbers vs printed output", "project.html:57, 148", "PASS", f"{S}labs_check.out: 496/500, -30/500, 0.480149, -0.733658, -2.302315, pair 2 -762 and 3000; all equal the printed lines; '$30.00 gain' = 3000 cents"),
 ("lab2-prose-numbers", "hypothesis, completion values and interpretation vs output", "project.html:153, 197", "PASS", f"{S}labs_check.out lab 2 output: -0.765595182, -0.625595182, 0.465057055 (sigmoid at z = -0.14 = 2*(1500-2200)/10000); z recomputed by hand"),
 ("lab3-prose-numbers", "hypothesis, interpretation and memo numbers vs output", "project.html:393, 589, 706", "PASS", f"{S}labs_check.out lab 3 output: 0.6352, 6.1503, 2.0201; 0.32, 9.59, 1.86; 3.55e-10; -7.1445; 11 of 12 mixed; lambda SE 9.59 > 6.15"),
 ("grader-seed49-se-docstring-numbers", "docstring numbers test_project.py:980-991 for seed 49", "grader/test_project.py:980-991", "PASS", f"{S}rederive.out and {S}reverse_order.out: SE_lambda 135.054 (1e-5), 97.675 (1e-6), -27.68%; SE_gamma 0.09474, 0.07983, -15.73%; reverse order 136.78 (+1.28%) and 98.09 (+0.42%)"),
 ("grader-allA-docstring", "docstring numbers test_project.py:820-826 (all-A set: precision near 925, SE above 1e5)", "grader/test_project.py:820-843", "PASS", f"{S}instance_and_allA.out: kappa_hat 924.73, se_lambda 692051.98, se_kappa 1981269.33"),
 ("grader-seed30-kappa-below-one", "LOW_KAPPA = make_instance(30) has kappa < 1 (project.html:213, test_project.py:36)", "grader/instance.py; test_project.py:36", "PASS", f"{S}rederive.out: seed30 kappa 0.635 (<1), gamma 0.477, lambda 1.578"),
 ("grader-recovery-47-of-50", "recovery count on seeds 0-49 (project.html:213; test_project.py:599-614)", "grader/test_project.py:599", "PASS", f"{S}run_graders_0_49.out: reference passes the whole suite (including the recovery test) on 50/50 seeds"),
 ("grader-tolerances-vs-page", "every tolerance stated at project.html:213 vs the test code", "project.html:213; grader/test_project.py:151-198, 213-237, 549-596, 617-641, 980-1009, 1120-1151", "PASS", "exact cent comparisons at 151-160, 213-221, 143-148; half-cent slack ONE_CENT+TOL (0.5+1e-6) at 176, 196, 208; 1e-9 relative at 441, 463; 1e-7 at 553, 630; 2e-5 at 580; 1e-9 local maximum at 596; 10% at 1004; one cent dominance at DOMINANCE_SLACK=1, lines 1106-1110. Nothing in the test is tighter than the page states"),
 ("grader-messages-never-print-answer", "failure messages never print the expected value (round 7 FAIL)", "grader/test_project.py:251-285 and every expect() message", "PASS", "round-7 FAIL (lines 254,258 printed -25) is fixed: the messages at 254-285 now give the rule, not the value; grep of all messages shows no expected numeric answer"),
 ("grader-gamma0-exact-convention", "CRRA gamma=0 exact expected prize (round-7 FAIL grader-gamma0-exact-over-constraint)", "project.html:221; grader/test_project.py:143-148; grader/reference.py:122-124", "PASS", "round-7 FAIL is resolved: the page now states the gamma = 0 exact-fraction exception (project.html:221), the reference sums Fraction (reference.py:123-124), and mutant e3d7_01 is killed at seed 1 (mutate_E3_0_9_existing.out)"),
 ("grader-second-participant-and-clamp", "second participant and clamp detection", "grader/test_project.py:617-641; instance.py", "PASS", f"{S}rederive.out: seed 30 kappa 0.635; mutants e3d4_05 and r7_kappa_hat_reports_log_kappa killed (mutate_E3_0_9_existing.out)"),
 ("instance-docstring-claims", "instance.py docstring ranges, pair counts, prize magnitudes, denominators, the 100-mixed rule", "grader/instance.py:1-33, 45-52", "PASS", f"{S}instance_and_allA.out: 0 problems over seeds 0-49 and 30 (gamma in [0.10,0.80], lambda in [1,3], kappa in [0.5,5], wealth in [$50k,$200k] in whole cents, 200 pairs, 2-3 prizes, |prize| in [500,50000], probs positive and sum 1, denominators in {1,2,4,5,10,20}, >= 100 mixed pairs)"),
 ("identification-convention-zero-prize", "page statement 'the certainty equivalent of a lottery whose positive-probability prizes are all gains, or all losses does not depend on lambda ... So a pair identifies lambda only when one of its two lotteries mixes' (zero prizes)", "project.html:223; project.html:682 and :694 (exemplar B)", "FAIL", f"{S}zero_prize_identification.out: {{0 w.p. 1/2, -100 w.p. 1/2}} and {{0, 100}} have CE free of lambda (-31.498026247 at lambda 0.5,1,2,3), so the conclusion holds; but neither lottery is 'all gains' or 'all losses' under the page's gain/loss convention (a prize above or below zero), so the stated hypothesis omits zero prizes and the 'So' step needs them"),
 ("questionnaire-js-browser", "questionnaire in Chromium: load instrument, pair list, export blocked until every pair has a choice, export file, bad file, no network", "project.html:245-353", "PASS", f"{S}questionnaire_browser.out: export disabled before load; legends '2000 cents with probability 1/2; -1000 ...'; export blocked; download 'responses.json' equals the lotteries and choices; bad '1/0' rejected with the page's message; page_errors []; non_local_requests []"),
 ("questionnaire-grammar", "questionnaire status message for several missing choices", "project.html:339 (JS)", "FAIL", f"{S}questionnaire_browser.out: status_missing_choice = 'No export: pair 1, 2 has no choice yet.' (plural subject with singular verb)"),
 ("questionnaire-fraction-contract", "probability text accepted by the questionnaire vs spec (project.html:207, 273)", "project.html:273", "PASS", f"{S}probcheck.out: '0','1','1/2','499/1000' accepted; '1/0','2/0','1/' and '-1/4' rejected; '00','01','1/05' accepted, which Fraction reads exactly; '5/4' accepted and refused later by the engine"),
 ("questionnaire-js-syntax", "inline questionnaire script parses", "project.html:249-353", "PASS", "node --check on the extracted script: SYNTAX_OK (Node 24.22.0)"),
 ("exemplar-word-count-A", "exemplar A memo words (117)", "project.html:623-674", "PASS", f"{S}exemplar_words.out: memo blocks 4, words 117 (headings included)"),
 ("exemplar-word-count-B", "exemplar B memo words (435)", "project.html:676-738", "PASS", f"{S}exemplar_words.out: memo blocks 5, words 435 (headings included)"),
 ("exemplar-scores-annotations", "data-scores and official scoring agree with annotations and rubric", "project.html:623-738", "PASS", "A: 2,2,1,2,1 and B: 3,3,4,3,3 agree with the annotated levels; test_memo_exemplars passes"),
 ("fixed-case-data-claims", "Lab 3 data: prize range, 2-3 prizes, probability sums, 11 of 12 mixed, pair 0 and 3 descriptions (Exemplar B)", "project.html:682, 393", "PASS", f"{S}fixed_case_claims.out: prizes [-18700, 19000]; 2 or 3 prizes per lottery; 11 mixed pairs; pair 4 not mixed; pair 0 and pair 3 descriptions match the data"),
 ("rung1-lab-answers-claim", "round-8 page change: 'answers written into the lab, not generated from the parameters'", "project.html:44; Lab 1 code lines 112-115", "PASS", "Lab 1 choices are literal strings \"A\"/\"B\" in the code; the page's new wording matches"),
 ("convention-whole-cents", "whole-cents convention (project.html:221) vs the engine", "project.html:221; grader/reference.py:71-73, 118-128", "PASS", "_half_up is floor(y + 0.5) used once; gamma=0 CRRA uses floor(expected_change + 1/2) on the Fraction; no other money rounding in reference.py"),
 ("citations-reading", "reading section (project.html:757-764): registry keys and their claims (round-7 FAIL at 757-763)", "project.html:757-764; L02.html:616; L05.html:609; L06.html:531; L07.html:80; L08.html:67, 133", "PASS", "round-7 FAIL resolved: kahneman1979prospect (L07:80), ellsberg1961risk (L08:133) and gilboa1989maxmin (L08:67) carry data-cite claims with grade C; pratt1964risk appears in L02:616 with no claim; epstein1989substitution is named in L05:609 with no claim; the L06:531 kahneman mention is 'no result'"),
 ("concept-links-definitions", "concept links and def ids used by the page", "project.html:53, 205, 207, 213, 220", "PASS", "def-prospect-theory (L06), def-certainty-equivalent (L02), def-crra-utility (L03), def-first-order-stochastic-dominance (L04) exist; L03 Proposition 2.7 exists at L03.html:173; L06 Definition 1.1 reference point at L06.html:56"),
 ("hours-arithmetic", "hours table total vs data-hours-project and hub split", "project.html:33, 362-368; index.html:29-40", "PASS", "1+1+3+4+3+2 = 14 = data-hours-project = 14; hub 56 lesson + 14 project = 70 (index.html:29, 31, 40)"),
 ("notation", "symbols vs notation/notation.json (T, Phi, gamma_3, gamma_4, R*, R_f, Q registered)", "project.html math (130 spans)", "PASS", "Phi used only as the standard normal distribution function (registered meaning); T, gamma_3, gamma_4, R*, R^{e*}, R_f, Q not used; gamma, lambda, kappa, zeta, xi, alpha, delta are lesson-local (notation.json 'about')"),
 ("scope-words", "scope words (only, all, every, any, exactly) in claims", "project.html lines 44, 53, 57, 148, 197, 213, 221, 223, 225, 393, 589, 602, 603, 682, 694, 716, 729", "PASS", "checked each claim-bearing use against code or output (see the rows above); not every one of the 59 matching lines was re-derived, so this row covers the claim-bearing uses only"),
 ("process-words", "no process words in learner text", "project.html", "PASS", "grep for verifier, round, builder, batch, slice, agent, todo, placeholder, draft, pending, reviewer returned no matches"),
 ("dag-unlinked-names", "concepts used outside the prerequisite closure", "project.html", "PASS", f"{S}check_dag_E3.out PASS; project.html names Lessons 1-8 of this unit only"),
 ("rubric-levels-vs-annotations", "rubric descriptors vs exemplar annotations", "project.html:611-615, 623-738", "PASS", "level descriptors used for A's C1..C5 and B's C1..C5 match the annotations; B's C4 level 4 'states the direction of bias' is not met (annotated as missed)"),
]
rows_out = []
for rid, check, loc, status, ev in rows:
    r = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = {
            "identification-convention-zero-prize": "project.html:223 replace 'whose positive-probability prizes are all gains, or all losses' with 'whose positive-probability prizes include no gain' or 'include no loss' (zero prizes count in neither); make the same change in the exemplar sentence at project.html:682 ('all gains or all losses') and the sentence at :694 ('the pairs that can identify loss aversion are the mixed ones').",
            "questionnaire-grammar": "project.html:339 pluralise: use 'pair ' for one missing id and 'pairs ' with 'have' for several (e.g. 'No export: pairs 1, 2 have no choice yet.').",
        }[rid]
    rows_out.append(r)

mutants = [
 {"name": "e8_01_se_from_inverse_of_the_diagonal_only.py", "description": "Standard errors take 1/sqrt of each diagonal entry of the information, ignoring the off-diagonal terms.", "killed_by": "test_standard_errors_match_the_coordinate_change_oracle (seeds 0,1,2,5,6,7,9)"},
 {"name": "e8_02_crra_allows_final_wealth_of_exactly_zero.py", "description": "CRRA refuses final wealth below zero but accepts exactly zero.", "killed_by": "test_crra_requires_wealth_plus_every_prize_to_stay_positive (seeds 0-9)"},
 {"name": "e8_03_prospect_loss_weight_also_scales_the_gain_branch.py", "description": "The loss weight lambda multiplies the gain branch of the value function as well as the loss branch.", "killed_by": "test_prospect_matches_oracle_for_instance_lotteries (seeds 0-9)"},
 {"name": "e8_04_prospect_model_adds_wealth_to_each_prize.py", "description": "The prospect model values the lottery on final wealth instead of on the change from 0.", "killed_by": "test_prospect_matches_oracle_for_instance_lotteries (seeds 0-9)"},
 {"name": "e8_05_model_name_error_raises_type_error.py", "description": "An unknown model name raises TypeError, where the specification names ValueError.", "killed_by": "test_model_name_must_be_crra_or_prospect (seeds 0-9)"},
]
for m in mutants:
    m["id"] = m.pop("name")

now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
notes = (
 "Round 8 (E3-d) at pin 2d755599 (checkout /Users/billyribeiro/.fanout/wt/verifyD8-E3-d). Delta since the round-7 pin 9373ef39: project.html (lines 44, 221, 719, 757), grader/test_project.py (lines 251-285), new mutants r7_01..03 and e3d7_01..04 (already committed at 2d755599, counted in the 112 mutants). Every row was re-verified from scratch this round; none was carried. "
 "Decisions the verifier made: (1) the identification sentence and its exemplar echo are FAIL (minor, wording) because the stated class omits zero prizes; the claim itself holds (zero_prize_identification.out). "
 "(2) the questionnaire status message grammar is FAIL (minor). "
 "(3) grader SE step rule: project.html:213 says 'either step passes' and test_standard_errors_match... requires one step for all three standard errors. Read as the whole check passing with either step, the grader matches the page; not a row. "
 "(4) seed-49 finite-difference standard errors are unstable with the step: SE_lambda 135.05 at 1e-5, 97.67 at 1e-6, 136.46 at 1e-4, 149.90 at 3e-6 (step_scan.out). An accurate method (1e-3..1e-5, or the converged value 136.5) passes the page's tolerance because the page's 1e-5 value is within 1%; a 3e-6 step does not, and that is a numerical choice the page does not ask for. Not an over-constraint of a correct implementation. "
 "(5) alt4 (bisection inversion of the value function) passes 10/10 seeds but took about 5 minutes per seed wall clock under concurrent load (reference: 14 s); the page states no run-time limit (grep of project.html), so this is an observation, not a row. "
 "(6) browser checks: page_smoke ran the full project page in Chromium; the questionnaire was driven by Playwright (questionnaire_browser.py); the self-assessment form in site.js is outside this slice and was not exercised beyond page_smoke's load and console checks. "
 "Could not check: the Pyodide in-browser grader on a learner's own elicit.py (only the page_smoke run with its reference), and the self-assessment form interaction. "
 "Round-7 non-PASS rows re-verified: grader-message-never-prints-answer (FIXED, PASS), grader-gamma0-exact-over-constraint (FIXED by page convention, PASS), citations-reading (FIXED, PASS), not-checked-browser-questionnaire (now PASS via Playwright). "
 "Mutation run: 112/112 KILLED on seeds 0-9 (mutate_E3_0_9_existing.out); 5 new mutants e8_01..05 all killed (new_mutants_0_9.out)."
)
frag = {
 "unit": "E3",
 "slice": "d",
 "round": 8,
 "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 8 (did not build E3)",
 "pin": "2d755599d8d74df292e3e43025f0458c4053802e",
 "base": "9373ef398589097500ea849e30ff9da423b98943 (round-7 pin); delta 9373ef39..2d75559: project.html lines 44, 221, 719, 757 and grader/test_project.py lines 251-285 (slice d); plus 7 new mutants (e3d7_01..04, r7_01..03) at 2d755599; cards.json and lesson pages are outside slice d",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyD8-E3-d",
 "scratch": "/Users/billyribeiro/.fanout/scratch-E3-d-r8",
 "verified_at": now,
 "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows_out) else "PASS",
 "rows": rows_out,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": notes,
 "summary": f"E3-d round 8 at 2d75559: {len(rows_out)} rows: {sum(r['status']=='PASS' for r in rows_out)} PASS, {sum(r['status']=='FAIL' for r in rows_out)} FAIL, {sum(r['status']=='UNVERIFIABLE' for r in rows_out)} UNVERIFIABLE. Mutants: 5 new, 5/5 killed. Alternatives: alt1/2/3/5 10/10 seeds; {alt4_status}.",
}
out = Path("ledgers/E3/E3-d.json")
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows_out), "verdict", frag["verdict"])
