"""Writes ledgers/E3/E3-d.json (round 4, slice d) from the outputs saved in ledgers/E3/scripts/E3-d-r4/.

Mutants are read from mutate_E3_r4.out (every KILLED / SURVIVED line). Run from the checkout:
python3 ledgers/E3/scripts/E3-d-r4/write_fragment_r4.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = "ledgers/E3/scripts/E3-d-r4"
SCRIPTS = {
    "gates": f"{D}/",
}

mut_rows = []
for line in (ROOT / D / "mutate_E3_r4.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+)\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    killed_by = None if killer.strip() == "None" else re.sub(r" \(seed \d+\)$", "", killer.strip())
    seed = re.search(r"\(seed (\d+)\)", killer)
    if killed_by is not None and seed:
        killed_by = f"{killed_by} (seed {seed.group(1)})"
    mut_rows.append({"id": name, "description": desc, "file": f"ledgers/E3/mutants/{name}.py", "killed_by": killed_by})

PASS = "PASS"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        r["fix"] = fix
    rows.append(r)


row("proj-gate-check-projects", "2.6 gate", "tools/check_projects.py --all", PASS,
    f"{D}/E3d_r4_tools_check_projects.py.out: 'check_projects E3: PASS', exit 0 (run this round on b276325).")
row("proj-gate-check-pages", "2.9 gate", "tools/check_pages.py --all", PASS,
    f"{D}/E3d_r4_tools_check_pages.py.out: 'check_pages E3: PASS', exit 0.")
row("proj-gate-check-dag", "2.9 gate", "tools/check_dag.py --all", PASS,
    f"{D}/E3d_r4_tools_check_dag.py.out: 'check_dag E3: PASS', exit 0. Anchors L02 #def-certainty-equivalent, L06 #def-prospect-theory, L03 #def-crra-utility each occur once (grep of course/modules/E/E3/L0{2,6,3}.html).")
row("proj-gate-run-labs", "2.5 labs", "tools/run_labs.py --unit E3 --page project", PASS,
    f"{D}/run_labs_E3_project.out: 'run_labs E3: PASS (3/3)', exit 0.")
row("proj-labs-twins-isolated", "2.5 labs", "tests/labs/E3/lab-E3-project-{1,2,3}.py", PASS,
    f"Run alone: .venv/bin/python -I -W error <twin> exit 0 for all three ({D}/E3d_r4_twin{{1,2,3}}.out). Page code equals twin for Labs 1 and 3; Lab 2 page code has the two '___' blanks and the twin holds the completed lines (the stated completion design; the completed expressions -math.log1p(math.exp(-z)) and -math.log1p(math.exp(z)) are the ones the page's interpretation names). Expected blocks equal twin output for all three ({D}/page_code_vs_twin.out).")
row("proj-page-smoke", "2.9 page_smoke", "tools/page_smoke.py --unit E3 --pages project", PASS,
    f"{D}/E3d_r4_smoke.out: 'page_smoke modules/E/E3/project.html: PASS', 'in-browser grader: All 35 tests pass on seed 1532773389', 'page_smoke E3: PASS'.")
row("proj-ruff-mypy", "gates", "grader and labs; repository mypy", PASS,
    "ruff check . -> 'All checks passed!'; ruff format --check . -> '335 files already formatted'; .venv/bin/mypy --no-incremental (repository configuration) -> 'Success: no issues found in 229 source files'. Scoped mypy on grader/ alone reports import-not-found for the staged modules elicit/instance, which is a scope artifact of the staging, not a finding.")
row("proj-grader-reference-50", "2.6 autograder 1", "tools/run_graders.py --unit E3 --seeds 0-49", PASS,
    f"{D}/run_graders_E3_0_49.out: 'run_graders E3: PASS (reference 50/50 seeds, slowest 1.0 s)', exit 0.")
row("proj-grader-collect", "2.6 autograder", "grader/test_project.py vs project.html line 203", PASS,
    f"{D}/collect_count.sh: '35 tests collected'. project.html line 203 says 'runs 35 checks'.")
row("proj-grader-instances", "2.6 autograder 2", "grader/instance.py", PASS,
    "Carried from round 3 (course/modules/E/E3/grader/instance.py byte-identical since the previous pin; git diff ccfdf4c b276325 lists no change to it): ledgers/E3/scripts/E3-d-r3/instances_sample.py over 20 seeds: every instance has gamma in [0.10,0.80], lambda in [1,3], kappa in [0.5,5]; answers differ across seeds. The reference run on seeds 0-49 this round re-exercised the instances.")
row("proj-grader-oracles", "2.6 autograder", "grader/test_project.py oracle_* functions", PASS,
    "Carried from round 3 (oracle block of test_project.py, lines 87-123, is outside the only changed hunk at lines 601-610): oracles are independent of reference.py. Re-exercised by the 50-seed reference run and the 36/36 mutant kills.")
row("proj-grader-no-network", "2.6 autograder 4", "grader/test_project.py lines 717-747", PASS,
    "Carried from round 3 (lines 717-747 unchanged; the only changed hunk is at 601-610): the test parses the imports of elicit.py and checks them against sys.stdlib_module_names; the suite passes on the reference this round.")
row("proj-grader-second-participant", "2.6 autograder", "grader/test_project.py line 35 and test_estimate_on_a_second_participant_is_also_a_maximum (line 500)", PASS,
    "INST2 = make_instance(SEED + 7_919) at line 35, used at line 500-503. Page line 203 describes it as a second participant: consistent.")
row("proj-grader-mutants-existing", "2.6 mutation", "ledgers/E3/mutants/{f,m,v,w,r3}_*.py (36 pre-existing files)", PASS,
    f"{D}/mutate_E3_r4.out (tools/mutate_graders.py --unit E3 --seeds 0-9): all 36 pre-existing mutants KILLED on seed 0 or 1 (see the mutants list).")
row("proj-grader-mutants-new", "2.6 mutation 3", "ledgers/E3/mutants/r4_*.py (4 new files)", "FAIL",
    "Four new student-error mutants written this round by make_r4_mutants.py: r4_probability_sum_tolerance_1e12 (SURVIVED), r4_prospect_uses_wealth (killed by test_prospect_matches_oracle_for_instance_lotteries seed 0), r4_zero_probability_rejected (killed by test_probabilities_must_be_nonnegative_and_sum_to_exactly_one seed 0), r4_newton_capped_at_five_steps (killed by test_estimate_returns_the_named_fields_as_finite_floats seed 1). The surviving mutant accepts a probability sum of 1 + 1e-13 where the reference refuses it (run this round: _check_probabilities((1/2, 1/2+1/10^13)) -> reference 'probabilities must sum to 1 (and be non-negative)', mutant accepts). project.html (exception table, row 2) says a lottery whose probabilities 'do not sum to exactly 1' raises ValueError 'probabilities must sum to 1'.",
    "Extend test_probabilities_must_be_nonnegative_and_sum_to_exactly_one (test_project.py line 300) with a must_raise on [Fraction(1, 2), Fraction(1, 2) + Fraction(1, 10**13)] with contains=('probabilities must sum to 1',); then re-run tools/mutate_graders.py --unit E3 --seeds 0-9, expecting 40/40 killed, and run_graders on 0-49.")
row("proj-grader-alt-correct", "2.6 alternatives", "ledgers/E3/scripts/run_alternatives.py (five alternatives)", PASS,
    f"{D}/alternatives_0_49.out: alt1 PASS 50/50, alt2 PASS 50/50, alt3 PASS 50/50, alt4 PASS 50/50, alt5 PASS 50/50 (exit 0). The round-3 alt4 failure (exact float equality on a zero-probability prize) is fixed by the tolerance at test_project.py line 607 (gap <= 1e-12).")
row("proj-grader-estimate-domain", "2.6 autograder", "project.html Conventions 'Estimation'; grader/test_project.py", PASS,
    "Carried from round 3 (Conventions paragraph and estimate tests unchanged this round): estimate uses gamma in (0,1), lambda > 0, kappa > 0, and test_estimates_lie_in_their_domains is the test for it.")
row("proj-grader-identification-margin", "2.6 autograder", "grader/test_project.py test_estimate_recovers_the_true_parameters_within_five_standard_errors", PASS,
    f"{D}/recovery_count.out: seed 2 has the largest z = 4.89 against the 5-SE threshold (passes, small margin); the four alternatives pass it.")
row("proj-grader-recovery-threshold", "2.6 autograder vs plan", "grader/test_project.py (recovery test) vs plans/E3-build-plan.md section 6.7 and section 10 Q12", "FAIL",
    f"{D}/recovery_count.out: 49 of 50 seeds within 4 standard errors on all three parameters; 50 of 50 within 5. plan 6.7 (line ~151) requires 'the estimate lies within 4 standard errors of the seed's true parameter on at least 47 of seeds 0-49'. The suite instead requires 5 SE on every seed (test_estimate_recovers_the_true_parameters_within_five_standard_errors). Q12 asks the architect to confirm or name another threshold; plans/E3-build-plan.md has no architect decision on Q12. project.html line 203 discloses the 5-SE tolerance, so the page and the suite agree; the plan does not.",
    "Architect resolves Q12 in plans/E3-build-plan.md: either record the per-seed 5-SE tolerance as the decision and amend plan 6.7, or change the test to the plan's count rule (within 4 SE on at least 47 of seeds 0-49). Then update project.html line 203 to match.")
row("proj-grader-plan-mutant-list", "plan 6.5 mutant list", "plans/E3-build-plan.md section 6.5 items 6, 7, 9", "FAIL",
    "Plan 6.5 items 6 (FOSD ranking reversed), 7 (SOSD on the CDFs) and 9 (Epstein-Zin EIS and risk aversion swapped) name behaviour that the project page does not contain: grep of course/modules/E/E3/project.html and grader/test_project.py for FOSD, SOSD and Epstein returns 0 hits in both. These three plan mutants therefore cannot be written against the project spec. The verifier's own 40 mutant files (ledgers/E3/mutants) cover the page's behaviours instead.",
    "Architect amends plan 6.5 items 6, 7 and 9 to project-scope mutants (the spec has no dominance or recursive-preference content), or adds the FOSD/SOSD and Epstein-Zin behaviour to the project spec and the suite.")
row("proj-grader-plan-fosd-tests", "plan 6.7 test list", "plans/E3-build-plan.md section 6.7 vs grader/test_project.py", "FAIL",
    "Plan 6.7 lists 'FOSD and SOSD verdicts on the instrument's pairs match the expected-utility ranking over a finite grid'. test_project.py contains no FOSD or SOSD test (grep returns 0). The project page does not ask for FOSD or SOSD, so the page is consistent; the plan and the suite are not.",
    "Architect removes the FOSD/SOSD bullet from plan 6.7 (the project spec has no dominance requirement), recorded as an architect decision; or adds the requirement to project.html and a grader test.")
row("proj-grader-estimate-domain-note", "plan 6.2 vs page", "plans/E3-build-plan.md 6.2 vs project.html Conventions", PASS,
    "Plan 6.2 wrote gamma in [0,1); the page and the suite use gamma in (0,1) for estimate, and the logit transform cannot represent gamma = 0 or 1. The page is the binding spec for the estimate domain.")
row("proj-spec-math", "2.4 mathematics", "project.html Conventions and Lab 1; grader/reference.py", PASS,
    f"{D}/recompute_numbers.out (own stdlib recomputation from the page formulas): CRRA CE 496/500 and prospect -30/500 for pair 1; P(A)=0.480149; log -0.733658; pair 2 prospect CE -762.141 (page -762); total -2.302315. Lab 2: z = -0.14, log P(A) = -0.765595182, log P(B) = -0.625595182 (page values). Prospect CE closed form c = -(-V/lambda)^(1/(1-gamma)) for V < 0 (page conventions) matches reference.py _prospect_ce.")
row("proj-spec-rounding", "2.6 spec", "project.html Conventions 'Whole cents'; reference.py _half_up (line 72-73)", PASS,
    "Page: floor(c + 1/2) with exact half toward plus infinity (2.5 -> 3, -0.5 -> 0). reference.py line 73 'return math.floor(y + 0.5)'. Lab 1 'nearest_cent' is the same rule.")
row("proj-spec-exception-table", "2.6 spec", "project.html Exception table; reference.py", PASS,
    "Four rows: model name (ValueError, two names), probability sum (ValueError, 'probabilities must sum to 1'), CRRA wealth plus prize (ValueError, 'wealth plus prize must stay positive'), responses empty or no mixed pair (ValueError, the condition). reference.py raises each with the quoted text (_check_model, _check_probabilities line 59, certainty_equivalent_cents lines 120-121, estimate lines 287-290 for the empty-or-unmixed case).")
row("proj-spec-params-keys", "2.6 spec", "project.html Required outputs (dd, after the three signatures)", PASS,
    "Round-3 FAIL is fixed: the page now names the keys 'gamma', 'lambda', 'kappa' and states which the models read (certainty_equivalent_cents reads gamma under crra, gamma and lambda under prospect; log_likelihood reads all three). Checked against reference.py and test_project.py calls.")
row("proj-spec-instrument-schema", "2.6 spec", "project.html Inputs (a)", PASS,
    "Round-3 FAIL is fixed: instrument.json is now specified as a JSON list with keys pair_id, prizes_a, probs_a, prizes_b, probs_b (no choice), whole-cent prizes, 'numerator/denominator' probabilities, at least 12 pairs with one mixed-sign lottery.")
row("proj-spec-questions", "2.6 spec", "project.html Specification", PASS,
    "Questions a student would ask were checked against the page: the estimate domain (gamma in (0,1)) is stated; the rounding rule is stated; the exception table; the key names; the instrument schema; the choice rule and its units (per $100). No clarifying question found that the page leaves unanswered.")
row("proj-spec-ladder", "2.6 ladder", "project.html section 'ladder' and rungs 1-4", PASS,
    "Rung 1 is fully solved with a 'why' note per step (Lab 1). Rung 2 is a completion lab graded by the twin's identical lines (run_labs). Rung 3 is the engine, autograded with a rubric for the instrument and report. Rung 4 is open-ended stretch. Tier U: rungs 1-2 at full length, as required.")
row("proj-spec-curriculum-scope", "2.6 scope", "curriculum/02-economics-finance-core.yaml lines 120-121 (E3 project block) vs project.html", PASS,
    "Curriculum project (yaml lines 120-121): estimate the risk-aversion and loss-aversion parameters by MLE and report the uncertainty. The page estimates three parameters (adds choice precision kappa) by MLE and reports standard errors; the extra parameter is the logit precision the model needs, stated in the spec.")
row("proj-hours", "2.6 hours", "project.html #hours table; index.html data-hours-*; curriculum E3 hours 70", PASS,
    "Table: 1+1+3+4+3+2 = 14 = data-hours-project=14 (project.html). Hub: data-hours-lessons=56 (8 lessons x 7 h) + 14 = 70 = curriculum/02-economics-finance-core.yaml line 91 'hours: 70'. Verifier's own estimate: rungs 1-2 about 2 h (as the table), engine 4-6 h (three functions, Newton search with standard errors), instrument 2-3 h, report 3-4 h, self-assessment 1-2 h, giving 12-17 h; the range 9.8-18.2 h is within 30 percent of 14.")
row("proj-rubric-observable", "2.6 rubric", "project.html rubric table (#rubric), all criteria", PASS,
    "Round-3 FAIL is fixed. C3 level 2 now reads 'Reports the three estimates with se_gamma, se_lambda and se_kappa' (observable); level 1 'No standard error reported, or a number is quoted that the run does not print'. C2 level 1 and 2 and C4 levels 1-2 were also reworded and remain observable. The 'some empirical claims' wording at C5 level 2 is vague but is distinguishable from level 1 by whether any claim carries a grade or key; not a FAIL.")
row("proj-rubric-calibration", "2.6 rubric 2", "project.html exemplar-a and exemplar-b (rubric blind scoring)", PASS,
    "Blind scores from the rubric only (annotations ignored). Exemplar A: C1 2, C2 2, C3 1, C4 2, C5 1 (official 2,2,1,2,2; C5 is within one level: the memo gives no grade or key on any claim, which is the level 1 descriptor 'No evidence grades or keys'). Exemplar B: C1 3 (two example pairs, not all twelve), C2 4 (per-response term both cases, simplification, which pairs identify each parameter), C3 4 (three SEs, convergence check, sample size, unreliability named), C4 3 (two limits, no direction of bias), C5 4 (official 3,4,4,3,4: exact match).")
row("proj-rubric-checks", "2.6 rubric", "tools/check_projects.py rubric_problems", PASS,
    f"{D}/E3d_r4_tools_check_projects.py.out: check_projects E3 PASS (five criteria, four levels, two exemplars, self-assessment form).")
row("proj-rubric-question-bank", "2.6 adversarial", "project.html", PASS,
    "No element with id 'question-bank' and the unit is not adversarial (plan Q9 and architect default: not adversarial, no question bank).")
row("proj-exemplar-numbers", "2.2 numbers", "project.html exemplar-b passages and Lab 3 data", PASS,
    f"{D}/recompute_numbers.out: 12 answers; 11 mixed-sign (non-mixed pair id 4 only); prize range -18700 to 19000 cents, as exemplar B says; pair 0 A is 6200 cents p=9/10 and -15100 p=1/10 against three prizes in B; pair 3 A 18800 p=3/4, -12500 p=1/4 and B 16500 p=2/5, -17700 p=3/5, both mixed. Estimates 0.6352, 6.1503, 2.0201, SEs 0.32, 9.59, 1.86, log-likelihood -7.1445: reference.estimate on the 12 answers (lab3_vs_reference.out) gives 0.63521, 6.15032, 2.02011, SE 0.31897, 9.59387, 1.86378, log-likelihood -7.144517 (rounded to the page's digits).")
row("proj-prose-lab1", "2.2 numbers, 2.5 labs", "project.html lab-E3-project-1 hypothesis and interpretation", PASS,
    f"{D}/recompute_numbers.out reproduces each printed value (CRRA cents 496 500 / 3000 -513 / 2166 1244; prospect -30 500 / 3000 -762 / 2144 140; P(A) 0.480149 / 0.637452 / 0.574613; total -2.302315). Interpretation: pair 2 sure $30 gain CE 3000 under both models and the -762 prospect CE (-762.141 unrounded) match.")
row("proj-prose-lab2", "2.5 labs", "project.html lab-E3-project-2 hypothesis and interpretation", PASS,
    f"{D}/recompute_numbers.out: z = 2*(1500-2200)/10000 = -0.14; log P(A) = -0.765595182; log P(B) = -0.625595182; P(A) = 0.465057055. Hypothesis values match. Interpretation's 'the sigmoid of z=-0.14' matches.")
row("proj-prose-lab3", "2.2 numbers, 2.5 labs", "project.html lab-E3-project-3 hypothesis and interpretation", PASS,
    f"{D}/lab3_vs_reference.out and {D}/page_code_vs_twin.out: the page's Lab 3 output equals the twin output; the 'largest score component' 3.55e-10 is printed by the lab; the interpretation's claims (score zero is a stationary point, not a maximum check) match the code (no Hessian sign check in main()).")
row("proj-prose-banned", "2.9 banned phrases", "project.html", PASS,
    "grep (case-insensitive) for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', obviously, clearly, roughly, historically: 0 hits each. 'about' appears only in prose, not as an approximation of a number.")
row("proj-prose-process-words", "2.9 process words", "project.html", PASS,
    "grep for builder, verifier, round, architect, plan (case-insensitive) on project.html: 0 hits.")
row("proj-notation", "2.4 notation", "project.html symbols vs notation/notation.json", PASS,
    "Symbols on the page: gamma, lambda, kappa, eta (local, not registered), A, B, c, v, V, z, x, e, Phi (stretch: probit, normal CDF). notation.json registers Phi, Phi^{-1} as the standard normal CDF and quantile (M4); the page uses it with that meaning. No registered symbol reused with another meaning.")
row("proj-reading-keys", "2.1 citations", "project.html section 'reading' and references/references.json", PASS,
    f"{D}/E3d_r4_verify_E3.out: 'live re-verification of E3: 5 of 560 entries, 0 problems', exit 0. {D}/E3d_r4_verify_offline.out: 'offline integrity: 560 entries, 0 problems'. The reading list cites the five curriculum keys; the page attributes no locator to any of them.")
row("proj-attribution", "2.1 attribution", "project.html", PASS,
    "The page's only claims are definitional and computed (the labs). No published locator is quoted; the reading section says so.")
row("proj-figures", "2.8 figures", "project.html", PASS,
    "grep: no svg, figure, img, iframe, or external URL in project.html: no chart or figure, so nothing to check under 2.8.")
row("proj-cards-sample", "2.7 cards sample", "course/modules/E/E3/cards.json ids E3-c010, c020, ..., c150 (every tenth) plus every changed card", PASS,
    "Sampled cards checked against lesson text: c010 (L01 Prop 3.1), c020 (L02 Def 1.2), c030 (r_A = 0.005, r_R = 0.5 at w=100 for u = sqrt(w)), c040 (L03 Prop 1.4), c050 (L03 Remark 2.8, bound (k+1)/2), c060 (L04 Thm 1.5), c070 (L04 Example 1.7: F_X=(1/2,1/2,1), F_Y=(0,1/2,1)), c080 (L05 Thm 1.3(a)), c090, c100 (L06 Def 1.3: note the page says p_i > 0, and the lesson does too), c110 (L06 Remark 3.1 and Props 1.4, 2.1, 2.2), c120 (L07 Remark 1.3), c130 (L07 section 4), c140 (L08 Def 2.1), c150 (L08 Model 2: -2.071068 CU, CE -1.072330 CU = -(2.071068/2)^2, wealth equivalent 99892.7670). Changed cards this round checked individually: c017 (L01 Part B six True comparisons; Prop 2.3), c045 (L03 Def 2.3), c053 (L03 Problem R3), c081 (L05 Cor 1.4 A1-A4), c082 (L05 Remark 1.5), c084 (L05 Prop 2.2 A1-A4), c090 (L05 Cor 3.3), c091 (L05 Remark 3.4), c113 (L06 Remark 3.2: lambda_R = (1/2)*sqrt(2) = sqrt(2)/2 for p=1/3, g=1000, l=300, alpha=delta=1/2 — recomputed), c123 and c131 (L07 Remark 1.6, Problem E2: 42.86863274-39.12507700 = 3.74355573 -> 3.7436), c127/c128 (L07 Lab 1 parts C/D: Gamma labels, 4.8788/3.9125, '10 of 10'), c137 (L08 tau), c148 (L08 prior set 30 to 60 of 90, 101951.2195 = 4180000/41), c154 (L08 Prop 2.4 A1-A3), c155 (L08 Problem R3 and Thm 2.2, A2).")
row("proj-cards-numbers", "2.7 cards numbers", "course/modules/E/E3/cards.json all cards", PASS,
    f"{D}/cards_scan.out: 'numbers (>5) not literal in own lesson: []'. Each multi-digit number on a card occurs in its own lesson text.")
row("proj-cards-duplicates", "2.7 duplicates", "course/modules/E/E3/cards.json full scan", PASS,
    f"{D}/cards_scan.out: 158 cards, unique contiguous ids E3-c001..c158, no exact duplicate fronts or backs. Near duplicates (difflib ratio >= 0.85): c004/c018 (assumption A1 vs A2, distinct facts) and c080/c082 (Theorem 1.3 'only through CE1' vs Remark 1.5 'mean vs distribution', distinct facts).")
row("proj-cards-xref", "2.7 cards cross-reference", "course/modules/E/E3/cards.json E3-c034, E3-c055, E3-c131, E3-c155", PASS,
    f"{D}/cards_scan.out lists 'Problem E2' and 'Problem R3' as not found by the literal pattern, because lesson problems are headed by titles such as 'E2 · ...' and ids such as emp-2. Checked by hand: L02 E2 (id E2, line 475), L03 E2 (title 'E2 · Checking the exact gamma 2 value', id emp-2), L07 E2 (id E2, line 406), L08 R3 (id R3, line 596) and L03 R3 (title 'R3 · What a grid check cannot establish'). Each card's reference resolves in its own lesson.")
row("proj-cards-grade-cite", "2.7 grades and keys", "course/modules/E/E3/cards.json grade, cite, basis fields", PASS,
    f"{D}/cards_grade_cite.out: grades T 100, C 23, D 1, none 34 (definitions). bad grade values: []; graded non-theorem cards without cite or basis: []; cite keys not in the registry: []. Basis values name Lab 1 parts of the lesson.")
row("proj-cards-hypotheses", "2.7 hypotheses", "course/modules/E/E3/cards.json E3-c074, E3-c081, E3-c090, E3-c092, E3-c104, E3-c105, E3-c154", "FAIL",
    "A card that states a result must carry its hypotheses. Fixed since round 3: E3-c081 now says 'Under A1 to A4' (L05 Corollary 1.4 begins 'Assume A1 to A4'); E3-c154 now says 'Under A1 to A3 of Proposition 2.4' (matches L08 Prop 2.4). Still missing: E3-c092 cites Corollary 1.4 with no A1 to A4 (the same corollary as c081); E3-c090 cites Corollary 3.3, whose hypotheses are those of Theorem 3.2 ('Assume A1 to A4, and psi = 1/gamma', L05 text), and the card carries only the psi = 1/gamma restriction; E3-c074 cites Proposition 1.8, which begins 'Under A1' (L04 text), with no A1; E3-c105 cites Proposition 2.2 (assume alpha, delta, lambda > 0, 0 < p < 1, g > 0, l > 0; L06 text) and its back uses p, g and l without defining them or stating those conditions. Accepted: E3-c104 (front fixes alpha = delta = 1; back defines p, g, l), E3-c138 (front 'one-element prior set'; back cites Prop 1.3), E3-c052 (Prop 1.4 holds for every w > 0, and the card concerns the family defined for positive wealth), E3-c009 (cites Prop 2.3 only for a descriptive claim), E3-c049 and E3-c037 (hypotheses in the back).",
    "Add the hypotheses to each card: c092 'Under A1 to A4, it is worth the sure plan at its certainty equivalent (Corollary 1.4)'; c090 'Under A1 to A4 and psi = 1/gamma, ... (Corollary 3.3)'; c074 'Under A1, a first-order ranking implies the integrated ordering (Proposition 1.8)'; c105 'For 0 < p < 1, g > 0, l > 0 and alpha, delta, lambda > 0, the sign threshold is lambda* = p g^alpha/((1-p) l^delta) (Proposition 2.2)'.")
row("proj-cards-coverage", "2.7 coverage (BUILDER_RULES 7)", "course/modules/E/E3/cards.json vs L01-L08 definitions, theorems, misconceptions, key formulas, key results", "UNVERIFIABLE",
    f"Checked: every Definition, Theorem, Proposition, Corollary and Lemma heading in L01-L08 has at least one card of its lesson naming it ({D}/card_coverage.out; the one unnamed item, L02 Remark 1.4, is a remark on hypotheses, not a required kind). All 24 quoted misconceptions in the eight lessons have a card addressing them, mapped by keyword (L08 one-element prior set: c138 and c142; L03 scale invariance: c048; L03 CRRA constant utility: c051). NOT checked: each key formula and each row of each lesson's key-results table against a card (BUILDER_RULES 7 names key formulas and key empirical results). That check was not performed this round.",
    "Verifier or builder maps every key-results table row and every displayed key formula in L01-L08 to a card of its lesson (or adds one), then re-runs card_coverage.py extended to those items.")
row("proj-structure", "2.9 structure", "project.html sections", PASS,
    "check_pages PASS. Section order: ladder, rungs, spec, budget, grader-section, local, report, stretch, reading, references, lesson-nav, matching the plan's section 6 and BUILDER_RULES 4 as read.")
row("proj-links", "2.9 links", "project.html internal links", PASS,
    "index.html#placement (id='placement' in index.html: 1 hit); L02 #def-certainty-equivalent, L06 #def-prospect-theory, L03 #def-crra-utility (1 hit each); page_smoke reports no external requests.")

fragment = {
    "unit": "E3",
    "slice": "E3-d",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 4 (did not build E3; scope: project.html rubric, grader, project labs, cards.json; project mutants)",
    "pin": "b276325f68b3032945c96810d651dcd39588b830",
    "base": "ccfdf4c (round-3 pin, fragment /Users/billyribeiro/.fanout/frags/C-E3-d.round3.json). Delta read in full for every slice hunk: project.html, grader/test_project.py (lines 601-610), cards.json (17 cards), and the hub index.html context. Re-verified from scratch: every round-3 non-PASS row. Carried PASS rows are marked 'Carried from round 3' and name the byte-identical subject.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC4-E3-d",
    "scratch": "/tmp (E3d_r4_* outputs; copies in ledgers/E3/scripts/E3-d-r4/)",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mut_rows,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Round 4, slice d, pin b276325. Commands run on the pin: check_projects, check_pages, check_dag, run_labs --page project, the three project twins under python -I -W error, page_code_vs_twin.py, run_graders 0-49, mutate_graders 0-9 (40 mutants), collect-only (35), page_smoke for the project page, ruff check and format, mypy (repository configuration), pytest tests/test_memo_exemplars.py and tests/test_page_checks.py, verify_refs --offline and --unit E3 (live), run_alternatives 0-49 (5/5 pass). Own scripts under ledgers/E3/scripts/E3-d-r4/. Not run: full pytest suite, render_curriculum, build_site --check, fetch_data --check (outside this slice). Not checked: lesson files other than as card sources (L01-L08 hub and lesson prose belong to other slices); the key-results table coverage of cards (UNVERIFIABLE row).",
    "summary": "E3-d round 4: verdict FAIL. Round-3 spec, rubric and hypothesis FAILs are fixed. Remaining FAILs: recovery threshold vs plan 6.7/Q12 (architect decision needed), plan 6.5 items 6/7/9 and plan 6.7 FOSD/SOSD tests not reflected in the project spec (architect decision needed), and one new surviving grader mutant (probability sum tolerance 1e-12) that the exception table makes a fault (test fix needed). One UNVERIFIABLE row (cards key-results and key-formula coverage).",
}

out = ROOT / "ledgers/E3/E3-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
statuses = [r["status"] for r in rows]
print("rows", len(rows), {s: statuses.count(s) for s in set(statuses)}, "mutants", len(mut_rows), "killed", sum(1 for m in mut_rows if m["killed_by"]))
