"""Writes ledgers/E3/E3-d.json (round 3, slice d) from the round-3 evidence files in this directory.
The rows state what was checked; every number in them comes from the output files named in its evidence.
Usage (from the checkout): .venv/bin/python -I ledgers/E3/scripts/E3-d-r3/write_fragment_r3.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/E3/scripts/E3-d-r3"
P = "course/modules/E/E3/project.html"
G = "course/modules/E/E3/grader"
C = "course/modules/E/E3/cards.json"
OUT = ROOT / "ledgers/E3/E3-d.json"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates and runs -------------------------------------------------------------------------------------------
row("proj-gate-check-projects", "2.6 structure gate", "tools/check_projects.py --all", "PASS",
    "Observed: 'check_projects E3: PASS' (exit 0), run on the pin ccfdf4c.")
row("proj-gate-check-pages", "2.9 structure gate", "tools/check_pages.py --all", "PASS",
    "Observed: 'check_pages E3: PASS' (exit 0).")
row("proj-gate-check-dag", "2.9 DAG gate", "tools/check_dag.py --all", "PASS",
    "Observed: 'check_dag E3: PASS' (exit 0); concept anchors L06 #def-loss-aversion, L06 #def-prospect-theory and "
    "L02 #def-certainty-equivalent exist (grep of id attributes).")
row("proj-gate-run-labs", "2.5 labs", "tools/run_labs.py --unit E3 --page project", "PASS",
    "Observed: 'run_labs E3: PASS (3/3)' (exit 0). Lab 1, Lab 2 and Lab 3 expected blocks equal the output.")
row("proj-labs-twins-isolated", "2.5 labs", "tests/labs/E3/lab-E3-project-{1,2,3}.py", "PASS",
    f"Run alone: .venv/bin/python -I -W error <twin> exit 0 for all three; outputs in the run (Lab 1: 'log-likelihood "
    f"of the three choices: -2.302315'; Lab 2: '-0.765595182' and '-0.625595182'; Lab 3: 'gamma_hat: 0.6352'). "
    f"Page code equals the twin (run_labs).")
row("proj-page-smoke", "2.5/2.6 Pyodide", "tools/page_smoke.py --unit E3 --pages project", "PASS",
    "Observed: 'page_smoke modules/E/E3/project.html: PASS', 'in-browser grader: All 35 tests pass on seed 117508852 "
    "(2.3 s)', 'page_smoke E3: PASS' (exit 0). Needed the project-pinned chromium (.venv playwright install chromium).")
row("proj-ruff-mypy", "gate", "course/modules/E/E3/grader, tests/labs/E3; mypy strict", "PASS",
    "ruff check: 'All checks passed!'; ruff format --check: '15 files already formatted'; mypy --no-incremental: "
    "'Success: no issues found in 229 source files'.")
row("proj-grader-reference-50", "2.6 autograder 1", "grader/reference.py via tools/run_graders.py", "PASS",
    "Observed: 'run_graders E3: PASS (reference 50/50 seeds, slowest 1.3 s)'. The same tool's starter step "
    "(tools/run_graders.py lines 162-166) requires the starter to fail.")
row("proj-grader-collect", "2.6 test count", "grader/test_project.py vs project.html line 203", "PASS",
    f"{S}/collect_count.sh: '35 tests collected'; project.html line 203 says 'runs 35 checks'.")
row("proj-grader-instances", "2.6 autograder 2", "grader/instance.py", "PASS",
    f"{S}/instances_sample.py over 20 seeds (incl. 7919, 7926): every instance has gamma in [0.10,0.80], lambda in "
    f"[1,3], kappa in [0.5,5], 200 pairs, probabilities summing to 1, magnitudes in [500,50000] cents, wealth in "
    f"[5000000,20000000] cents; problems: []; 20 of 20 distinct gamma values.")
row("proj-grader-oracles", "2.6 autograder", "grader/test_project.py oracle_* functions", "PASS",
    "Test oracles are written separately from reference.py (test_project.py lines 87-123 vs reference.py lines 85-100) "
    "and are used for every expected value; expected values are never printed (expect/must_raise, lines 43-63).")
row("proj-grader-no-network", "2.6 autograder", "grader/test_project.py lines 717-747", "PASS",
    "Test parses elicit.py with ast and checks each top-level import against sys.stdlib_module_names and the network "
    "list; capsys check that functions print nothing; module-level pytest.mark.filterwarnings('error').")
row("proj-grader-second-participant", "2.6 autograder", "grader/test_project.py test_estimate_on_a_second_participant",
    "PASS", "INST2 = make_instance(SEED + 7919) is used in that test; the page's description of the second participant "
    "(line 203) matches.")
row("proj-grader-mutants-existing", "2.6 mutation", "ledgers/E3/mutants/{f,m,v,w}*.py (32 files)", "PASS",
    f"{S}/mutate_E3_r3.out: all 32 pre-existing mutants KILLED (seeds 0-9, see mutants list).")
row("proj-grader-mutants-new", "2.6 mutation", "ledgers/E3/mutants/r3_*.py (4 new files)", "PASS",
    f"Four new student-error mutants written by this verifier (make_r3_mutants.py): r3_half_cent_truncated_toward_zero "
    f"(plan 6.5 item 8, not previously present), r3_kappa_se_is_observed_information_not_inverted, "
    f"r3_mixed_check_counts_zero_probability_losses, r3_estimate_stops_at_grid_start. All four KILLED on seed 0 "
    f"(mutate_E3_r3.out); 'mutate_graders E3: PASS (36/36 killed)'.")
row("proj-grader-alt-correct", "2.6 over-constraint", "ledgers/E3/scripts/run_alternatives.py, 5 alternatives", "FAIL",
    "run_alternatives.py --seeds 0-49 (E3-d-r3/alternatives_0_49.out): alt1 PASS 50/50, alt2 PASS 50/50, alt3 PASS "
    "50/50, alt5 PASS 50/50, alt4 FAIL 46/50 (seeds 26, 29, 44, 45). alt4_failures.py: each failing seed fails "
    "test_zero_probability_prize_contributes_nothing_to_the_likelihood. alt4_zero_prob_gap.py: alt4 gives a "
    "likelihood gap of -1.1102230246251565e-16 between a response with and without a zero-probability prize; the "
    "test compares with == and no tolerance (test_project.py, the 'assert sol.log_likelihood(with_zero, TRUE) == "
    "sol.log_likelihood(without, TRUE)' expression in that test).",
    f"In {G}/test_project.py, replace the exact equality in test_zero_probability_prize_contributes_nothing_to_the_"
    f"likelihood with abs(a - b) <= 1e-12. The page's log-likelihood is a float, and a zero-probability prize must add "
    f"nothing up to floating-point error. Then rerun run_alternatives.py --seeds 0-49 and run_graders.py --seeds 0-49.")
row("proj-grader-estimate-domain", "2.6 spec vs plan", f"{P} Conventions 'Estimation'; plans/E3-build-plan.md 6.2",
    "PASS", "Page and suite use gamma in (0,1) for estimate (project.html Lab 3 text; test_estimates_lie_in_their_domains). "
    "Plan 6.2 wrote [0,1). The logit transform cannot return gamma = 0, so (0,1) is the consistent reading. Noted, "
    "not a defect.")
row("proj-grader-identification-margin", "2.6 autograder note", f"{G}/test_project.py test_estimate_recovers_the_true_"
    "parameters_within_five_standard_errors", "PASS",
    f"{S}/recovery_count.py: seed 2 has the largest z = 4.89 (threshold 5). Passes, but with little margin; the four "
    f"alternatives pass it. Noted only.")
row("proj-grader-recovery-threshold", "2.6 autograder / plan 6.7 and Q12", "grader/test_project.py vs "
    "plans/E3-build-plan.md 6.7 and 10 Q12", "FAIL",
    f"Plan 6.7 requires 'within 4 standard errors on at least 47 of seeds 0-49' (Q12: planner proposal, 'confirm, or "
    f"name another threshold'). recovery_count.py: 49 of 50 seeds are within 4 SE on all three parameters, 50 of 50 "
    f"within 5 SE. The suite tests 5 SE per seed, a choice project.html line 203 states but the plan does not "
    f"confirm. No architect confirmation of Q12 is recorded in plans/E3-build-plan.md.",
    "Either (a) the architect records the 5-SE per-seed threshold as the confirmed answer to Q12 in "
    "plans/E3-open-items.md or the plan, or (b) the suite implements the 47-of-50 count within the 60 s Pyodide budget "
    "(a per-seed loop is too slow in-browser; measure before choosing).")
row("proj-grader-plan-mutant-list", "plan 6.5 mutant list", "plans/E3-build-plan.md 6.5 items 6, 7, 9", "FAIL",
    "Plan 6.5 items 6 (FOSD ranking reversed), 7 (SOSD on the CDFs) and 9 (Epstein-Zin EIS and risk aversion swapped) "
    "name behaviour that E3's project spec (project.html Rung 3, Specification) does not contain; no FOSD, SOSD or "
    "Epstein-Zin function exists in elicit.py. Item 8 (truncation) is now covered by r3_half_cent_truncated_toward_zero.",
    "Architect to replace plan 6.5 items 6, 7 and 9 with mutants of the E3 spec (for example a log-likelihood that uses "
    "the chosen alternative's probability for both choices, or a CRRA gamma=0 that uses the log form). Then the verifier "
    "writes them into ledgers/E3/mutants/.")
row("proj-grader-plan-fosd-tests", "plan 6.7 test list", "plans/E3-build-plan.md 6.7 vs grader/test_project.py", "FAIL",
    "Plan 6.7 lists 'FOSD and SOSD verdicts on the instrument's pairs match the expected-utility ranking over a finite "
    "grid'. test_project.py has no FOSD or SOSD test, and project.html never asks for FOSD (the instrument is graded by "
    "rubric). The plan and the page disagree, and the suite follows the page.",
    "Architect to delete the FOSD/SOSD item from plan 6.7 (the E3 spec does not require it), or add the requirement to "
    "project.html Rung 3 and a test for it.")

# ---- spec ---------------------------------------------------------------------------------------------------------
row("proj-spec-math", "2.4 mathematics", f"{P} Specification and Conventions; grader/reference.py", "PASS",
    "CRRA CE, prospect CE (closed form, both signs), logit choice probability and log-likelihood, and the delta-method "
    "SE were compared with reference.py (lines 85-100, 156-176, 242-317) and with test oracles; the formulas and "
    "reference agree. Lab 3 reference estimates (lab3_vs_reference.py) match the printed numbers.")
row("proj-spec-rounding", "2.4 mathematics", f"{P} Conventions 'Whole cents'; reference.py _half_up", "PASS",
    "Page: floor(c + 1/2), 2.5 -> 3, -0.5 -> 0. reference.py line 73 'return math.floor(y + 0.5)'; "
    "test_half_cent_goes_up_on_exact_halves (2.5 -> 3, 0.5 -> 1, -0.5 -> 0) passes on the reference.")
row("proj-spec-exception-table", "2.6 spec", f"{P} Exception table; reference.py", "PASS",
    "Each of the four rows maps to a ValueError with the quoted text ('probabilities must sum to 1', 'wealth plus prize "
    "must stay positive', model names, mixed-sign condition); tests must_raise cover each row.")
row("proj-spec-params-keys", "2.6 spec completeness", f"{P} line 199 (Required outputs)", "FAIL",
    "The page gives the signatures of certainty_equivalent_cents(..., params: dict[str, float], ...), log_likelihood(..., "
    "params) but never names the keys of params. The suite and reference read params['gamma'], params['lambda'], "
    "params['kappa'] (reference.py lines 118, 126 and 169-171). A competent student would have to ask which keys to use.",
    "Add to Required outputs: 'params is a dict with the keys \"gamma\", \"lambda\" and \"kappa\"; the crra model reads "
    "only gamma'.")
row("proj-spec-instrument-schema", "2.6 spec completeness", f"{P} line 197 (Inputs a)", "FAIL",
    "The page requires 'instrument.json' with at least 12 pairs but gives no key names or format. Only the responses "
    "format is specified (keys pair_id, choice, prizes_a, probs_a, prizes_b, probs_b). A student would have to ask "
    "what instrument.json must contain.",
    "State the instrument.json format, for example a JSON list of objects with the same keys as the responses, with "
    "prizes in cents and probabilities as 'numerator/denominator' strings.")
row("proj-spec-questions", "2.6 spec completeness", f"{P} Specification", "PASS",
    "Other questions a student would ask were checked against the page: the estimate domain (gamma in (0,1)) is stated; "
    "the rounding rule is stated; the exception table is complete for named conditions; the response format is stated. "
    "Only the two gaps above remain.")
row("proj-spec-ladder", "2.6 ladder", f"{P} section 'ladder' and rungs 1-4", "PASS",
    "Rung 1 is fully solved with a 'why' note per step (Lab 1). Rung 2 is a completion lab graded by the twin's "
    "identical lines (run_labs). Rung 3 is the engine and the report. Rung 4 is open-ended. Tier U (curriculum "
    "02-economics-finance-core.yaml, E3 tier: U) so rungs 1-2 are full length, as the page says.")
row("proj-spec-curriculum-scope", "2.6 scope", "curriculum/02-economics-finance-core.yaml E3 project block",
    "PASS", "Curriculum project: 'estimate the participant's risk-aversion and loss-aversion parameters by MLE, and "
    "report the uncertainty'; deliverable 'Instrument plus estimation report'; grading both. The page also estimates "
    "the choice precision kappa, which plan 6.2 specifies. A superset, documented; noted only.")
row("proj-hours", "2.6 hours", f"{P} #hours table; index.html data-hours-*; curriculum E3 hours: 70",
    "PASS", "Table: 1+1+3+4+3+2 = 14 = data-hours-project=14. Hub: data-hours-lessons=56 + 14 = 70 = curriculum E3 hours: "
    "70 (curriculum/02-economics-finance-core.yaml line 91). Hours are design targets; only the arithmetic is checked.")
row("proj-rubric-observable", "2.6 rubric 1", f"{P} rubric table, criterion C3 (level 2 cell)", "FAIL",
    "The C3 level-2 cell reads 'Reports the estimates without standard errors, or without the sample size, or quotes a "
    "number that the run does not print'. The level-2 text is a disjunction, so a report that gives the estimates but no "
    "standard error meets it. Exemplar A (C3, data-level annotation 'Misses C3 level 2: no standard error and no sample "
    "size are reported') reads it as a conjunction. The same report scores 2 by the cell and 1 by the annotation, and "
    "the scoring rule ('the highest level whose every element the report shows') does not settle it.",
    "Rewrite the C3 level-2 cell as one condition, for example 'Reports the estimates and the sample size, but no standard "
    "errors' and make level 1 'No estimate and no uncertainty reported'. Then re-annotate exemplar A to match.")
row("proj-rubric-calibration", "2.6 rubric 2", f"{P} exemplar-a and exemplar-b annotations", "PASS",
    "Blind scores from the rubric only: exemplar A C1 2, C2 2, C3 2, C4 2, C5 2 (official 2,2,1,2,2; C3 within one "
    "level). Exemplar B C1 3, C2 4, C3 4, C4 3, C5 4 (official 3,4,4,3,4), exact match. Within one level on every "
    "criterion, so the calibration rule passes. The C3 wording is a separate row.")
row("proj-rubric-checks", "2.6 rubric", "tools/check_projects.py rubric_problems", "PASS",
    "Five criteria, four levels each, both exemplars, self-assessment form (section#self-assessment), check_projects PASS.")
row("proj-rubric-question-bank", "2.6 rubric 3", f"{P}", "PASS",
    "No element id='question-bank' on the page; the question bank is not required (plan 6.6, check_projects).")
row("proj-exemplar-numbers", "2.2 numbers (rubric prose)", f"{P} exemplar-b passages",
    "PASS", f"{S}/exemplar_and_instrument_check.py on the lab twin data: 12 answers; prize range -18700 to 19000 cents "
    f"(exemplar B says -18 700 to 19 000); each lottery has 2 or 3 prizes and probabilities summing to 1 exactly; 11 of "
    f"12 pairs mixed (Lab 3 prints 11). Exemplar B's 0.32, 9.59, 1.86, 3.55e-10, -7.1445 match Lab 3's printed output.")
row("proj-prose-lab1", "2.2 numbers (prose)", f"{P} lab-E3-project-1 hypothesis and interpretation", "PASS",
    f"{S}/lab1_independent.py recomputes, from the page's formulas: CRRA 496/500, prospect -30/500, P(A)=0.480149, "
    f"log -0.733658; pair 2 CRRA 3000/-513, prospect 3000/-762; pair 3 2166/1244 and 2144/140; total -2.302315. All match "
    f"the page text and the expected block.")
row("proj-prose-lab2", "2.2 numbers (prose)", f"{P} lab-E3-project-2 hypothesis", "PASS",
    f"{S}/lab1_independent.py: z = -0.14; log P(A) = -0.765595182, log P(B) = -0.625595182, as the page states.")
row("proj-prose-lab3", "2.2 numbers (prose)", f"{P} lab-E3-project-3 hypothesis and interpretation", "PASS",
    f"{S}/lab3_vs_reference.py: reference.estimate on the twelve page answers gives gamma 0.6352101, lambda 6.150316, kappa "
    f"2.020107, se 0.31897/9.59387/1.86378, log-likelihood -7.144517. Printed values agree at the stated precision. The "
    f"interpretation's claim that the lab checks the score and not a maximum is consistent with the code.")
row("proj-prose-banned", "1.3-1.4 banned phrases", f"{P}", "PASS",
    "grep for TODO, TBD, lorem, ellipsis, 'for brevity', 'details omitted', 'beyond the scope', 'it is important to "
    "note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly', 'of course': no hits.")
row("proj-prose-process-words", "2.9 process words", f"{P}", "PASS",
    "No builder, verifier, round, architect or plan wording in learner text (grep).")
row("proj-notation", "2.4 notation", f"{P} symbols; notation/notation.json", "PASS",
    "Symbols on the page: gamma, lambda, kappa, eta (local, not registered); Phi (stretch: probit) is the registered "
    "normal CDF (notation.json, module M4) and is used with that meaning; gamma_3 and gamma_4 are registered but not "
    "used on this page. No registered symbol takes another meaning. Macros used: \\gamma, \\lambda, \\kappa, \\eta, "
    "\\Phi, \\hat, \\mathrm, \\log, \\ln, \\texttt; none unregistered (page_smoke strict math passed).")
row("proj-reading-keys", "2.1 citations", f"{P} section 'reading' and references/references.json", "PASS",
    "Five keys verified in references.json (status 'verified'): pratt1964risk, kahneman1979prospect, "
    "epstein1989substitution, ellsberg1961risk, gilboa1989maxmin. verify_refs --offline: '560 entries, 0 problems'. "
    f"{S}/verify_refs_E3_live.out (verify_refs.py --unit E3, live): '5 of 560 entries, 0 problems'. The page attributes no "
    "statement to any key.")
row("proj-attribution", "2.1 attribution", f"{P}", "PASS",
    "The page's only claims are definitional and computed (the labs). No published locator is quoted. Consistent with "
    "its statement 'No passage locator from these sources has been confirmed'.")
row("proj-figures", "2.8 figures", f"{P}", "PASS",
    "The project page contains no chart or figure element (grep); nothing to check under 2.8.")
row("proj-cards-sample", "2.7 cards (sample)", f"{C} ids E3-c010, c020, ..., c150 (every tenth card, 15 cards)", "PASS",
    "Each sampled card was checked against its lesson statement: c010 (L01 Proposition 3.1, affine utility); c020 (L02 "
    "Definition 1.2); c030 (L02 Definition 2.1, Example 2.3: r_A = 0.005, r_R = 0.5 at w = 100); c040 (L03 Proposition 1.4); "
    "c050 (L03 Remark 2.8, bound (k+1)/2); c060 (L04 Theorem 1.5, under A1); c070 (L04 Example 1.7); c080 (L05 Theorem 1.3, "
    "A1-A4); c090 (L05 Corollary 3.3; Lab 1 uses psi=2); c100 (L06 Definition 1.3, p_i > 0); c110 (L06 Remark 3.1); c120 "
    "(L07 Remark 1.3); c130 (L07 Example 1.4 / Remark 1.6: 2*omega(3/10) = 0.5715817698, omega(3/5) = 0.3912507700, "
    "recomputed in Python); c140 (L08 Definition 2.1); c150 (L08 Model 2: V = 5 - sqrt(50) = -2.0710678, c = -1.0723305 "
    "CU = -107.23 cents, wealth 99892.7670 cents, 1 CU = 100 cents as the lesson states). Only card-level issues are in "
    "the hypotheses row.")
row("proj-cards-numbers", "2.7 cards", f"{C} all cards", "PASS",
    f"{S}/cards_scan.py (HTML parser text, so 'x < 0' does not swallow text): every number with more than one digit "
    f"in a card occurs in its own lesson; the one apparent miss (E3-c150 '1.072330') was a scanner bug (regex tag strip) "
    f"and is resolved by the parser. Output: 'numbers (>5) not literal in own lesson: []'.")
row("proj-cards-duplicates", "2.7 cards duplicates", f"{C} full scan", "PASS",
    "cards_scan.py: 158 cards, no duplicate ids, exact duplicate fronts or backs. Near duplicates (difflib ratio >= 0.85): "
    "c004/c018 (assumption A1 vs A2, distinct) and c080/c082 (formula vs mean, distinct claims). No duplicate card.")
row("proj-cards-xref", "2.7 cards cross-refs", f"{C} E3-c034, E3-c055", "PASS",
    "'Problem E2' resolves to the problem with id E2 in the card's own lesson: L02 line 463 (id=\"E2\", 'E2 · The "
    "approximation error...') and L03 line 411 ('E2 · Checking the exact gamma 2 value'). c034 numbers recomputed: "
    "0.565835/5.065835 = 11.17%, 0.565835/4.5 = 12.57%; c055: M = 9/80000, CE = 80000/9 = 8888.89 (lesson's Problem E2 "
    "solution).")
row("proj-cards-grade-cite", "2.7 cards / BUILDER 7", f"{C} grade, cite, basis fields", "PASS",
    f"{S}/cards_grade_cite.py: grades T 100, C 23, D 1, no grade 34 (definitions); every graded non-T card has cite or "
    f"basis; all cite keys ('epstein1989substitution', 'kahneman1979prospect', 'ellsberg1961risk', 'gilboa1989maxmin') "
    f"exist in references.json.")
row("proj-cards-hypotheses", "2.7 cards (hypotheses)", f"{C} E3-c081, E3-c090, E3-c154", "FAIL",
    "A card must carry a stated result's hypotheses. E3-c081 ('What is the value of a risky date-1 plan?') states Corollary "
    "1.4, which begins 'Assume A1 to A4' (L05 Corollary 1.4). E3-c090 states Corollary 3.3, which holds 'under the "
    "assumptions of Theorem 3.2' (A1 to A4 and psi = 1/gamma, L05 Theorem 3.2). E3-c154 states Proposition 2.4, which "
    "assumes A1 to A3 (L08 Proposition 2.4). None of the three backs names its assumptions.",
    "Add the assumption names to each back: E3-c081 'Under A1 to A4, ...'; E3-c090 'Under A1 to A4 and psi = 1/gamma, ...'; "
    "E3-c154 'Under A1 to A3, ...'.")
row("proj-cards-coverage", "2.7 cards completeness (BUILDER 7)", f"{C} vs L01-L08 definitions, theorems, misconceptions",
    "UNVERIFIABLE",
    "Not checked in full: BUILDER_RULES 7 requires one card per definition, theorem, key formula, key result and misconception. "
    "This verifier checked 15 sampled cards in depth and the whole file by script, but did not enumerate every definition "
    "and misconception in the eight lessons against the card list.",
    "Run a per-lesson audit (list each Definition/Theorem/Proposition/Corollary/Lemma and each 'misconception' item, and map "
    "each to a card id), and add the missing cards.")

# ---- page and lab evidence --------------------------------------------------------------------------------------
row("proj-structure", "2.9 structure", f"{P} sections ladder, rungs, spec, budget, grader, local, report, brief, rubric, "
    "exemplars, self-assessment, stretch, reading", "PASS",
    "check_pages PASS; section order matches the plan's section 6 and BUILDER_RULES 4 as read; minimum counts (five rubric "
    "criteria, two exemplars, twelve pairs in Lab 3) met.")
row("proj-links", "2.9 links", f"{P} internal links", "PASS",
    "index.html#placement exists (section id='placement'); L02.html and L06.html anchors exist; page_smoke reports no "
    "external requests.")

fragment = {
    "unit": "E3",
    "slice": "E3-d",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 3 (did not build E3; scope: project.html rubric, grader, project labs, cards.json; project mutants)",
    "pin": "ccfdf4c",
    "base": "ccfdf4c (no round-2 pin recorded in the ledger; the round-2 fragment is not in /Users/billyribeiro/.fanout/frags; full re-verification of the slice, no carried PASS rows)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC3-E3-d",
    "scratch": "/tmp (E3d_* files: rg, mg, labs, smoke outputs, a staged grader copy in a mktemp directory)",
    "verified_at": "2026-10-28T00:00:00+00:00",
}

# mutants from the mutate_graders output
mutants = []
for line in (ROOT / S / "mutate_E3_r3.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^KILLED (\S+): (.*) -> (\S+) \(seed (\d+)\)$", line)
    if m:
        fname, desc, test, seed = m.groups()
        mutants.append({
            "id": Path(fname).stem,
            "description": desc,
            "file": f"ledgers/E3/mutants/{fname}",
            "killed_by": f"{test} (seed {seed})",
        })

fragment["verdict"] = "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS"
fragment["rows"] = rows
fragment["mutants"] = mutants
fragment["registry_flags"] = []
fragment["freshness_flags"] = []
fragment["notes"] = (
    "Round 3, slice d, pin ccfdf4c. Ran on the pin: check_projects, check_pages, check_dag, run_labs (project page), the "
    "three project twins under python -I -W error, run_graders 0-49, mutate_graders (36 mutants, 0-9), page_smoke for the "
    "project page (after installing the project's pinned chromium with the project venv's playwright), ruff check and "
    "format, mypy --no-incremental, collect-only (35), verify_refs --offline and --unit E3 (live), pytest "
    "tests/test_memo_exemplars.py and tests/test_page_checks.py, and run_alternatives.py 0-49 (alt4 FAIL). Own scripts are in "
    f"{S}/. Not run: the full pytest suite, render_curriculum, build_site --check, fetch_data --check (no slice input "
    "changed those files; they are outside this slice). Scanner note: the round-2 card scripts (ledgers/E3/scripts/E3-d-r2) "
    "strip tags with a regex that swallows text after a bare '<' ('x < 0'); this verifier's cards_scan.py uses an HTML "
    "parser instead. The earlier round-2 scanner results on numbers are therefore not relied on."
)
fragment["summary"] = (
    f"E3-d round 3: verdict {fragment['verdict']}. {sum(r['status'] == 'PASS' for r in rows)} PASS, "
    f"{sum(r['status'] == 'FAIL' for r in rows)} FAIL, {sum(r['status'] == 'UNVERIFIABLE' for r in rows)} UNVERIFIABLE. "
    f"Mutants: {len(mutants)} listed, all killed on seed 0 (32 pre-existing + 4 new r3_*). Alternatives: 4 of 5 pass on "
    f"seeds 0-49 (alt4 fails 4 seeds on an exact float equality in the grader)."
)

problems = []
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

problems = ledger.validate(fragment, "E3-d")
OUT.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", OUT, "rows", len(rows), "mutants", len(mutants), "verdict", fragment["verdict"])
print("validate:", problems)
