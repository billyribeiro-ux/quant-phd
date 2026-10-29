"""Writes the round-7 fragment ledgers/E3/E3-d.json from the evidence in ledgers/E3/scripts/E3-d-r7/."""
import json, re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyC7-E3-d")
S = "ledgers/E3/scripts/E3-d-r7/"
R = []

def row(i, check, location, status, evidence, fix=None):
    d = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)

P = "PASS"; F = "FAIL"
row("proj-gate-check-projects", "tools/check_projects.py --all", "tools/check_projects.py", P,
    "check_projects.out line 'check_projects E3: PASS', rc=0 (S/check_projects.out).")
row("proj-gate-check-pages", "tools/check_pages.py --all", "tools/check_pages.py", P,
    "check_pages.out 'check_pages E3: PASS', rc=0 (S/check_pages.out); anchors such as def-prospect-theory resolve.")
row("proj-gate-check-dag", "tools/check_dag.py --all", "tools/check_dag.py", P,
    "check_dag.out 'check_dag E3: PASS', rc=0 (S/check_dag.out).")
row("proj-gate-run-labs", "tools/run_labs.py --unit E3 --page project", "tools/run_labs.py", P,
    "run_labs_project.out 'run_labs E3: PASS (3/3)', rc=0 (S/run_labs_project.out).")
row("proj-labs-twins-isolated", "python -I -W error on each project twin, run from /tmp",
    "tests/labs/E3/lab-E3-project-{1,2,3}.py", P,
    "twin_project_{1,2,3}.out end with rc=0 and the .err files are 0 bytes (S/twin_project_*.out, *.err).")
row("proj-page-smoke", "tools/page_smoke.py --unit E3 --pages project", "course/modules/E/E3/project.html", P,
    "page_smoke.out: 'in-browser grader: All 36 tests pass on seed 1773095357', 'page_smoke E3: PASS', rc=0.")
row("proj-ruff-mypy", "ruff check and format on grader/ and project twins; mypy --no-incremental",
    "course/modules/E/E3/grader/, tests/labs/E3/lab-E3-project-*.py", P,
    "ruff_check.out 'All checks passed!', ruff_format.out '7 files already formatted'; mypy.out 'Success: no issues found in 3 source files'; "
    "mypy on grader reference.py and instance.py: 'Success: no issues found in 2 source files'. Two round-7 mutants were reformatted and re-linted clean.")
row("proj-grader-reference-50", "tools/run_graders.py --unit E3 --seeds 0-49", "course/modules/E/E3/grader/reference.py", P,
    "run_graders_0_49.out 'run_graders E3: PASS (reference 50/50 seeds, slowest 1.1 s)', rc=0.")
row("proj-grader-collect", "collect-only count of test_project.py equals the page count ('runs 36 checks', project.html line 203)",
    "course/modules/E/E3/grader/test_project.py; project.html:203", P,
    "collect_only_workdir.out '36 tests collected'; grep -c 'def test_' = 36; page_smoke reports 36 tests.")
row("proj-grader-instances", "instance.py docstring claims against code", "course/modules/E/E3/grader/instance.py lines 1-30, 43-50, 146-259", P,
    "gamma round(uniform(0.10,0.80),3) l.212; lambda [1,3] l.213; kappa [0.5,5] l.214; wealth randrange(5_000_000,20_000_001,100) = $50,000 to $200,000 l.215; "
    "200 pairs l.218; denominators (4,5,10,20) l.44; magnitudes randrange(500,50001) = $5 to $500 l.60; mixed count >=100 l.232; "
    "half-cent margin 1e-6 l.43 and l.101; boundary margin 0.5 at gamma=0.001 l.146-147, l.237. Each docstring claim matches its code line.")
row("proj-grader-oracles", "oracle functions versus the spec formulas", "course/modules/E/E3/grader/test_project.py lines 87-135", P,
    "oracle_value, oracle_prospect, oracle_crra, oracle_loglik recomputed by S/se_step_sensitivity.py and S/recovery_count_r7.py; "
    "they equal the reference outputs to 3e-4 relative on the standard errors and to the cent on the certainty equivalents (run_graders 50/50).")
row("proj-grader-no-network", "suite reads the imports of elicit.py; no network module", "course/modules/E/E3/grader/test_project.py lines 780-810", P,
    "NETWORK_MODULES check and capsys check present; test passes on reference seed 0 (36 passed, workdir run).")
row("proj-grader-second-participant", "second participant (seed + 7919) is also a maximum", "course/modules/E/E3/grader/test_project.py lines 35, 516-528", P,
    "test present; reference passes it on seeds 0-49 (run_graders 50/50).")
row("proj-grader-mutants-existing", "tools/mutate_graders.py --unit E3 --seeds 0-9 over all mutant files",
    "ledgers/E3/mutants/*.py (47 files: 43 earlier plus 4 round-7)", P,
    "mutate_E3_0_9_r7.out 'mutate_graders E3: PASS (47/47 killed)', rc=0.")
row("proj-grader-mutant-score-tolerance", "round-5 mutant r5_newton_stops_at_gradient_1e_2 against the stated score tolerance",
    "course/modules/E/E3/grader/test_project.py lines 460-485; project.html line 203", P,
    "mutate_E3_0_9_r7.out: KILLED r5_newton_stops_at_gradient_1e_2 by test_score_is_zero_at_the_estimate (seed 0); the test uses min over steps 1e-5 and 1e-6 against 2e-5, the page line 203 states the same.")
row("proj-grader-mutants-new", "round-5 survivors and round-7 student-error mutants",
    "ledgers/E3/mutants/r5_*.py, ledgers/E3/mutants/r7_*.py", P,
    "round-5 survivors now killed: r5_mixed_check_counts_only_the_first_lottery by test_estimate_accepts_a_mixed_lottery_on_the_b_side_alone (seed 0); "
    "r5_newton_stops_at_gradient_1e_2 by the score test; r5_se_gamma_applies_delta_factor_twice by the recovery test. "
    "Four new round-7 mutants, each re-run on seed 0 (killed): r7_wealth_check_tests_prize_alone (test_crra_gamma_zero...), "
    "r7_kappa_hat_reports_log_kappa (test_reported_log_likelihood...), r7_model_message_omits_allowed_names (test_model_name_must_be...), "
    "r7_prospect_value_rounded_before_inverse (test_prospect_matches_oracle...).")
row("proj-grader-alt-correct", "run_alternatives.py: five alternative correct engines, seeds 0-49", "ledgers/E3/scripts/run_alternatives.py", P,
    "alternatives_0_49.out: alt1 to alt5 each 'PASS (50/50 seeds)', rc=0.")
row("proj-grader-estimate-domain", "estimate domain 0 < gamma < 1, lambda > 0, kappa > 0",
    "course/modules/E/E3/grader/test_project.py lines 439-444", P,
    "test asserts strict domain; reference passes on seeds 0-49; the estimates are interior on all 50 seeds (recovery_count_r7.out).")
row("proj-grader-identification-margin", "recovery within the stated tolerance and the reference counts",
    "course/modules/E/E3/grader/test_project.py lines 502-513; recovery_count_r7.out", P,
    "recovery_count_r7.out: 50 of 50 seeds within 5 SE on every parameter; 49 of 50 within 4 SE. The per-seed 5 SE check passes on seed 0 and on the reference for every seed (50/50).")
row("proj-grader-recovery-threshold", "test threshold versus plans/E3-build-plan.md section 6.7 and section 10 Q12",
    "course/modules/E/E3/grader/test_project.py lines 502-513; plans/E3-build-plan.md lines 406 and 580-581", F,
    "The plan (section 6.7) requires 'within 4 standard errors on at least 47 of seeds 0-49', and section 10 Q12 recommends that threshold; the Architect decisions block says to follow a stated recommendation. "
    "The grader instead checks 5 standard errors on the single seed QF_SEED (l.511). Measured: 49 of 50 seeds meet 4 SE (recovery_count_r7.out), so the plan's count would pass today.",
    "Architect: either implement the plan's threshold (4 SE on at least 47 of seeds 0-49, a loop over seeds in test_project.py) and keep the page's sentence in line, or amend Q12 in the plan to the 5 SE single-seed rule, which the page already states.")
row("proj-grader-plan-mutant-list", "plan section 6.5 student-error mutant list (binding: ten mutants per grader)",
    "plans/E3-build-plan.md section 6.5 items 1-10; ledgers/E3/mutants/", F,
    "Items 1-5, 8 and 10 have E3 counterparts (ledgers/E3/mutants f/m/r series). Items 6 (FOSD ranking with reversed inequality), 7 (SOSD on CDFs) and 9 (Epstein-Zin exponent swap) name functions that exist in neither project.html nor test_project.py (grep -c 'FOSD|SOSD|Epstein' = 0 in both files).",
    "Architect: amend plan section 6.5 items 6, 7 and 9 to errors that the E3 engine contains (for example, a misreported standard error, a missing wealth check), or add the FOSD/SOSD and Epstein-Zin requirements to the spec. Until then, the plan's list is not satisfiable as written.")
row("proj-grader-plan-fosd-tests", "plan section 6.7 test list versus grader/test_project.py",
    "plans/E3-build-plan.md section 6.7 bullet 'FOSD and SOSD verdicts'; course/modules/E/E3/grader/test_project.py", F,
    "Plan 6.7 requires 'FOSD and SOSD verdicts on the instrument's pairs match the expected-utility ranking'. test_project.py contains no FOSD or SOSD test (grep 0), and project.html specifies no such verdict.",
    "Architect: drop the bullet from plan 6.7 (the page does not spec FOSD/SOSD, consistent with the E3 scope), or add the spec sentence and the tests.")
row("proj-grader-seed49-docstring", "numeric claim in a grader docstring: 'for seed 49 ... about 1% ... and about 12% between steps 1e-5 and 1e-6'",
    "course/modules/E/E3/grader/test_project.py lines 760-764 (docstring of test_standard_errors_match_the_delta_method_oracle)", F,
    "se_step_sensitivity.out (seed 49, oracle observed information, delta method): se_lambda is 135.054 at step 1e-5 and 97.675 at step 1e-6 (-27.7%); se_gamma 0.09474 vs 0.07983 (-15.7%); se_kappa 0.5729 vs 0.5605 (-2.2%). "
    "The '12%' is not reproduced. The '1%' for evaluation order reproduces (se_lambda 135.054 normal vs 136.780 with the answers reversed: 1.28%).",
    "Replace '12%' with the measured figures (about 28% for se_lambda and 16% for se_gamma between steps 1e-5 and 1e-6), and fix the tolerance in the next row.")
row("proj-grader-se-step-overconstraint", "a correct engine that differs only in the finite-difference step of the observed information (1e-6 instead of 1e-5) must pass",
    "course/modules/E/E3/grader/test_project.py lines 732-777 (_observed_information step 1e-5, tolerance 10%)", F,
    "Variant = reference.py with the Hessian in estimate() taken at step 1e-6 (ledgers/E3/scripts/E3-d-r7/variant_se_step_1e6_elicit.py). "
    "variant_h1e6_seed49.out: seed 49 -> 'FAILED test_standard_errors_match_the_delta_method_oracle, 1 failed, 35 passed'; seed 0 -> 36 passed. "
    "The page does not fix a finite-difference step, and the spec's standard error is the observed-information formula, so this engine is a correct implementation that the suite rejects.",
    "Make the oracle's standard errors step-robust (for example Richardson extrapolation over steps 1e-3, 1e-4, 1e-5, or an analytic Hessian in the oracle), or widen the tolerance for weakly identified seeds with a stated reason; then re-run the variant on seeds 0-49.")
row("proj-grader-estimate-domain-note", "plan 6.2 versus project.html Conventions 'Estimation'", "plans/E3-build-plan.md section 6.2; project.html Conventions", P,
    "Plan 6.2 gives gamma in [0,1) as the model domain; the page's Estimation convention states gamma in (0,1) for estimate; the grader asserts the open interval (test l.439-441). The estimate is interior on all 50 seeds, so the page and grader are consistent.")
row("proj-spec-math", "Conventions and Lab 1 formulas versus reference and an independent recomputation", "course/modules/E/E3/project.html Conventions; grader/reference.py", P,
    "Conventions (l.210-213) match reference.py _check_model, _value, _prospect_ce, _logit_sum, estimate (l.281-317). Lab 1 numbers recomputed: pair 2 CE values, z = -0.14 in Lab 2 (-0.765595182 and -0.625595182 match the twin).")
row("proj-spec-rounding", "'Whole cents' convention: exact half toward plus infinity, floor(c+1/2)", "course/modules/E/E3/project.html Conventions; grader/reference.py _half_up and the CRRA gamma = 0 branch",  P,
    "reference.py l.71-73 (floor(y+0.5)) and l.122-124 (Fraction floor(expected+1/2)); tests l.260-270 pass with 2.5 -> 3, 0.5 -> 1, -0.5 -> 0.")
row("proj-spec-exception-table", "exception table rows versus reference messages", "course/modules/E/E3/project.html Exception table; grader/reference.py", P,
    "Messages: 'model must be \"crra\" or \"prospect\"' (ref l.30), 'probabilities must sum to 1 (and be non-negative)' (l.60), 'wealth plus prize must stay positive' (l.121), 'need at least one response, and mixed-sign lotteries, to identify loss aversion' (l.288) each contain the quoted text.")
row("proj-spec-params-keys", "Required outputs: signatures and dict keys", "course/modules/E/E3/project.html Required outputs; grader/reference.py; grader/starter.py", P,
    "Signatures in project.html l.199 equal starter.py l.17-35 and reference.py; estimate returns gamma_hat, lambda_hat, kappa_hat, se_gamma, se_lambda, se_kappa, log_likelihood (reference l.309-316).")
row("proj-spec-instrument-schema", "Inputs (a): instrument.json keys", "course/modules/E/E3/project.html Inputs (a); grader/instance.py _serialise", P,
    "Inputs (a) lists pair_id, prizes_a, probs_a, prizes_b, probs_b without choice; instance.py serialises the same keys plus choice for the responses (l.195-205), matching Inputs (b).")
row("proj-spec-questions", "Specification: required outputs, constraints and grading mode", "course/modules/E/E3/project.html Specification (l.193-206)", P,
    "Context, Inputs, Required outputs, Constraints and Grading present; grading names the autograder (36 checks) and the rubric; the reading list cites five keys.")
row("proj-spec-ladder", "ladder and rung order", "course/modules/E/E3/project.html section 'ladder' (l.40-49)", P,
    "Four rungs in the order that check_projects requires; check_projects E3 PASS.")
row("proj-spec-curriculum-scope", "curriculum brief for the E3 project versus the page", "curriculum/02-economics-finance-core.yaml lines 116-121 (brief: 'Design and run an in-page lottery questionnaire, estimate ... by MLE ... report the uncertainty'; deliverable 'Instrument plus estimation report'; grading both)", P,
    "Round-5 FAIL is resolved: project.html section #questionnaire (l.232-343) is an in-page questionnaire that exports responses.json in the (b) form; the estimate and standard errors are in the engine spec; #report carries the instrument and report rubric.")
row("proj-hours", "#hours table sums to the project hours; hub split; curriculum hours", "project.html #hours (l.348-358); course/modules/E/E3/index.html data-hours-*", P,
    "1 + 1 + 3 + 4 + 3 + 2 = 14 = data-hours-project (project.html l.33; index.html); data-hours-lessons 56; 56 + 14 = 70 = the hub's stated module hours.")
row("proj-rubric-observable", "rubric descriptors are observable", "course/modules/E/E3/project.html #rubric (l.595-604)", P,
    "Each level names a countable or visible element (count of pairs, cents, the three se_ keys, a limit with a direction, a grade and key).")
row("proj-rubric-calibration", "exemplar scores match the annotations", "course/modules/E/E3/project.html #exemplar-a (data-scores 2,2,1,2,2) and #exemplar-b (3,4,4,3,4)", P,
    "Exemplar A annotations: C1 meets 2/misses 3, C2 meets 2/misses 3, C3 meets 1/misses 2, C4 meets 2, C5 meets 2 -> 2,2,1,2,2. Exemplar B: C1 meets 3/misses 4, C2 meets 4, C3 meets 4, C4 meets 3/misses 4, C5 meets 4 -> 3,4,4,3,4. Both match data-scores and the verdict text.")
row("proj-rubric-checks", "tools/check_projects.py rubric_problems", "tools/check_projects.py lines 58-72", P,
    "check_projects.out E3 PASS.")
row("proj-rubric-question-bank", "no adversarial question bank required", "course/modules/E/E3/project.html (no id=question-bank); plans/E3-build-plan.md section 6.6", P,
    "grep for question-bank returns nothing; the architect decision says no question bank.")
row("proj-exemplar-numbers", "numbers in exemplar memos are Lab 3 numbers or read from its data", "course/modules/E/E3/project.html exemplar-a and exemplar-b", P,
    "Exemplar B: gamma 0.6352, lambda 6.1503, kappa 2.0201, se 0.32/9.59/1.86, score 3.55e-10, log-likelihood -7.1445 match the Lab 3 expected block; prize range -18700 to 19000 and pairs 0 and 3 match ANSWERS (l.401-414); 11 mixed pairs match Lab 3 output.")
row("proj-prose-lab1", "Lab 1 hypothesis and interpretation prose vs printed output", "course/modules/E/E3/project.html Lab 1 (l.57, l.138)", P,
    "Hypothesis numbers (496/500, -30/500, P(A)=0.480149, -0.733658, sum -2.302315) equal the expected block l.131-137; pair 2 'sure $30.00 (3000 cents both models)' and '-762' match l.133.")
row("proj-prose-lab2", "Lab 2 hypothesis and interpretation vs output and twin", "course/modules/E/E3/project.html Lab 2 (l.143, l.187)", P,
    "z = 2(1500-2200)/10000 = -0.14 (computed); -0.765595182 and -0.625595182 equal the expected block; the page code equals the twin except the two blanks (diff: 4 lines, all blanks).")
row("proj-prose-lab3", "Lab 3 hypothesis and interpretation vs output", "course/modules/E/E3/project.html Lab 3 (l.382, l.577)", P,
    "Expected values gamma_hat 0.6352, lambda_hat 6.1503, kappa_hat 2.0201, SEs two decimals, score below 1e-6 (3.55e-10), 12 answers and 11 mixed (l.570-576) match the twin run (twin_project_3.out).")
row("proj-prose-banned", "BUILDER_RULES banned phrases and placeholders", "course/modules/E/E3/project.html; cards.json", P,
    "grep for TODO, placeholder, lorem, tbd, coming soon: no hits in project.html or cards.json.")
row("proj-prose-process-words", "no process words in learner text", "course/modules/E/E3/project.html; cards.json", P,
    "grep for verifier, builder, round, we will, let us, in this section: no hits.")
row("proj-notation", "every symbol versus notation/notation.json", "course/modules/E/E3/project.html math; notation/notation.json", P,
    "Macros used on the page (\\Phi, \\alpha, \\delta, \\eta, \\gamma, \\kappa, \\lambda, \\theta, \\tfrac) are Greek letters declared local or \\Phi, whose registry meaning is 'standard normal CDF' (notation.json, M4), used the same way on the stretch line. No registered symbol is reused with another meaning.")
row("proj-reading-keys", "Reading section keys exist in the registry", "course/modules/E/E3/project.html #reading (l.741-751); references/references.json", P,
    "pratt1964risk, kahneman1979prospect, epstein1989substitution, ellsberg1961risk, gilboa1989maxmin are all 'verified' entries in references/references.json (entries list, used_by E3).")
row("proj-attribution", "no statement attributed to a source the page has not read", "course/modules/E/E3/project.html; cards.json cards with cite (c097, c134, c157, c158)", P,
    "Registry titles: 'Prospect Theory: An Analysis of Decision under Risk' (kahneman1979prospect), 'Risk, Ambiguity, and the Savage Axioms' (ellsberg1961risk, contains 'Ambiguity'), 'Maxmin expected utility with non-unique prior' (gilboa1989maxmin); card claims about those titles match. The page states no locator from them.")
row("proj-figures", "figure and chart rules", "course/modules/E/E3/project.html", P,
    "No svg, canvas, chart or figure element on the page; the questionnaire is a form, not a figure.")
row("proj-cards-sample", "cards sample against lessons", "course/modules/E/E3/cards.json (162 cards read in full)", F,
    "All 162 cards were read and checked against L01-L08 text and the lab twin outputs. Defects found in cards E3-c034, c035, c055, c108/c114, c131 and c155 (rows proj-cards-numbers, proj-cards-duplicates, proj-cards-xref).",
    "Apply the fixes in the three card rows below.")
row("proj-cards-numbers", "every card number appears in its lesson; card numbers and output keys match lab outputs",
    "course/modules/E/E3/cards.json vs L01-L08.html and tests/labs/E3/lab-E3-L0x-1.py", F,
    "cards_r7.py: every number in every card occurs in its own lesson text (0 misses). Output-key check: E3-c035 says 'linear_premium_zero_at_all_scales True'; the L02 twin prints 'linear_premium_zero_at_three_scales True' (twin_L02.out). Other card numbers match twin outputs (c016, c017, c032-c034, c054, c093-c096, c127, c144, c150-c153).",
    "Change E3-c035 to say linear_premium_zero_at_three_scales True (the printed key).")
row("proj-cards-duplicates", "no duplicate cards", "course/modules/E/E3/cards.json E3-c108 and E3-c114", F,
    "No exact duplicate fronts or backs (cards_r7.out). E3-c108 and E3-c114 test the same Remark 2.5 fact about the two copies of the gamble (integrated value 100 against narrow-framed -200 at lambda = 2, so bundling flips the sign). Round 6 changed the wording, not the fact.",
    "Merge E3-c114 into E3-c108, or replace c114 with a different fact from Remark 2.5 or Example 2.3.")
row("proj-cards-xref", "cross-references in cards resolve to lesson items", "course/modules/E/E3/cards.json E3-c034 (L02), E3-c055 (L03), E3-c131 (L07), E3-c155 (L08)", F,
    "cards_r7.out: '(Problem E2)' occurs only in L06.html; cards c034, c055, c131 cite it from L02, L03 and L07. '(Problem R3)' (c155, L08) is not in L08.html; it occurs in L03 and L04. The round-5 PASS for this row was wrong.",
    "Re-point each citation to an item of its own lesson: c034 to 'Lab 1, part A' (the 11.17 and 12.57 percent figures come from the Lab 1 numbers), c055 and c131 to their Lab 1 part or Example, and c155 to Theorem 2.2 with its own hypothesis A2 and no problem number.")
row("proj-cards-grade-cite", "grade, cite and basis fields", "course/modules/E/E3/cards.json", P,
    "162 cards: 99 grade T, 25 C with basis, 1 D (c097, cite), 4 with cite (c134, c157, c158, c097) and 37 definition cards with no grade (BUILDER_RULES 7 requires a grade only for graded results).")
row("proj-cards-hypotheses", "result cards carry the hypotheses of the result they cite", "course/modules/E/E3/cards.json E3-c104, E3-c089, E3-c091, E3-c144, E3-c159",  P,
    "Round-5 FAILs are resolved: c104 now states alpha = delta = 1, 0 < p < 1, g > 0, l > 0 (L06 Proposition 2.1); c089 and c091 state A1 to A4 (L05 defines A1 0<beta<1, A2 psi>0 and psi not 1, A3 gamma not 1, A4 positive consumption); c144 states u(W) = -1/W with gamma = 2 (L08 Example 2.5). c159 matches L02 Remark 1.4.")
row("proj-cards-coverage", "BUILDER_RULES 7 coverage: every key-results row, key formula, definition, theorem, misconception has a card", "course/modules/E/E3/cards.json vs L01-L08.html key-results tables and named statements", P,
    "coverage_r7.out: every named Definition/Proposition/Theorem/Lemma/Corollary heading of L01-L08 is cited by a card of its lesson (the two 'not cited' hits, Proposition 1.3 and 1.6 of L03, are cross-lesson references in the text, not L03 statements). The 65 key-results rows each map to a card; the round-5 gap (L03 gamma = 1 and k checks) is covered by E3-c160.")
row("proj-structure", "section structure and order", "course/modules/E/E3/project.html", P,
    "Sections in order: ladder, rungs, spec, questionnaire, budget, autograder, local, report (Lab 3, brief, rubric, exemplars, self-assessment), stretch, reading, references, nav.")
row("proj-links", "internal and concept links", "course/modules/E/E3/project.html", P,
    "check_pages E3 PASS; the concept links (prospect-theory, certainty-equivalent, crra-utility) point to existing L02, L03, L06 anchors; in-page anchors #conventions, #questionnaire, #self-assessment, #rubric, #exemplars exist.")

mutants = []
for line in (ROOT / S / "mutate_E3_0_9_r7.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+)\.py: (.*) -> (.*)$", line)
    if m:
        mutants.append({"id": m.group(1), "file": f"ledgers/E3/mutants/{m.group(1)}.py",
                        "description": m.group(2), "killed_by": m.group(3)})
survivors = [l for l in (ROOT / S / "mutate_E3_0_9_r7.out").read_text(encoding="utf-8").splitlines() if l.startswith("SURVIVED")]
assert not survivors and len(mutants) == 47, (len(mutants), len(survivors))

non_pass = [r for r in R if r["status"] != "PASS"]
fragment = {
    "unit": "E3",
    "slice": "d",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier, unit E3 slice d, round 7 (did not build E3; read the verifier rules and the round-5 fragment)",
    "pin": "0d2d0f3",
    "base": "04626e9 (round-5 pin, last fragment on disk: frags/C-E3-d.round5.json). The round-6 fragment C-E3-d.round6.json is not on disk; the delta 04626e9..0d2d0f3 was read in full for the slice files.",
    "checkout": str(ROOT),
    "scratch": "/tmp/E3d_r7 (work, variant, m_* mutant workspaces); evidence copied to ledgers/E3/scripts/E3-d-r7/",
    "verified_at": "2026-10-29T06:40:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta since 04626e9 read in full for project.html (123 lines), grader/test_project.py (94 lines), cards.json (60 lines), "
        "the L02 lab twin, and the r5 mutant files. Everything in the slice was re-read this round (project.html 766 lines, grader reference.py, instance.py, test_project.py, starter.py, cards.json 162 cards); "
        "no round-5 PASS row was carried. Four new student-error mutants written (r7_*.py, all killed on seeds 0-9). "
        "Two mutant docstrings were reworded after the 0-9 run (r7_model_message_omits_allowed_names, r7_wealth_check_tests_prize_alone); code unchanged and each re-killed on seed 0. "
        "Not checked: the browser UI of the questionnaire and of the autograder (no browser run; JS read in source only); full pytest suite; render_curriculum, build_site --check, fetch_data --check (outside this slice); "
        "the lesson prose beyond the statements cited by cards (lesson slices belong to other verifiers); collect-only from the repo root fails because elicit.py is not on the path, so the count was taken in the workdir with the same files. "
        "coverage_r7.py reports two cross-lesson hits (L03 Proposition 1.3 and 1.6 are references to L02 and M1, not L03 statements); not counted as gaps."
    ),
    "summary": (
        f"E3-d round 7: verdict FAIL, {len(non_pass)} non-PASS rows of {len(R)}. Fixed since round 5: questionnaire added (curriculum scope), "
        "the three new round-5 mutants killed, the L03 gamma = 1 card (c160) added, hypotheses added to c089/c091/c104/c144. "
        "Still failing: recovery threshold versus plan Q12, plan 6.5 items 6/7/9 and 6.7 FOSD/SOSD (architect), the seed-49 docstring figure (12% vs 28%), "
        "a new over-constraint (a correct engine with a 1e-6 standard-error step fails seed 49), card c035 output key, card cross-references c034/c055/c131/c155 (round-5 PASS was wrong), "
        "card near-duplicate c108/c114. Alternatives 5/5 pass seeds 0-49; mutants 47/47 killed; reference 50/50."
    ),
}
out = ROOT / "ledgers/E3/E3-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(R), "non-pass", len(non_pass), "mutants", len(mutants))
