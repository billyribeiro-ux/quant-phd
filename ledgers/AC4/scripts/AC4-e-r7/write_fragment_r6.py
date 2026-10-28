"""Writes ledgers/AC4/AC4-e.json (round 6) from the round-6 check results. Run from the checkout root."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
MUT_LOG = pathlib.Path(sys.argv[2])
VERIFIED_AT = sys.argv[3]

CARRY = "Carried from round 5 (course/modules/AC/AC4/project.html byte-identical in the cited lines since the previous pin 00745fe; the diff hunks are at project.html lines 252, 265 and 399 only): "
CARRY_TESTS = "Carried from round 5 (course/modules/AC/AC4/grader/test_project.py byte-identical in the cited lines since the previous pin 00745fe; the diff hunks are at test_project.py lines 43-46, 552-557, 637-641, 677-683 and 733-739 only): "

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


row("proj-autograder-reference", "Reference solution passes the whole suite on the learner-facing grader files",
    "course/modules/AC/AC4/grader/reference.py; course/modules/AC/AC4/grader/test_project.py", "PASS",
    "Copied instance.py, test_project.py, starter.py and reference.py (as budget_engine.py) to /tmp/ac4-v/e6/ref. "
    "QF_SEED=0,1,2,3,5,99,455320725 pytest -q --assert=plain -W error test_project.py: '221 passed' on every seed. "
    "tools/run_graders.py --unit AC4 --seeds 0-49: 'PASS (reference 50/50 seeds)'.")
row("proj-collect-count", "Test count on the page equals the real collect-only count",
    "course/modules/AC/AC4/project.html line 265; course/modules/AC/AC4/grader/test_project.py", "PASS",
    "pytest --collect-only -q on seeds 0,1,2,4,9,17,123,999,1999,455320725: '221 tests collected' every time. "
    "Page line 265 reads 'collects <strong>221 checks</strong>'. grep for 212 in course/modules/AC/AC4 finds no stale count.")
row("proj-autograder-alternatives", "Alternative correct implementations pass the suite (over-constraint probe)",
    "course/modules/AC/AC4/grader/test_project.py; ledgers/AC4/scripts/AC4-e-r6/alternatives_r4.py; ledgers/AC4/scripts/AC4-e-r6/alt_e.py, alt_f.py, alt_g.py", "PASS",
    "Five correct engines written from the page specification, none from reference.py: alt_a-c (alternatives_r4.py, rerun this round on seeds 0, 4, 9, 25: '221 passed' each); "
    "alt_e (Fraction half-up, one generic whole-number validator, class-free), alt_f (integer-only half-up (2n+d)//(2d), KeyError translated to ValueError, per-product loops), "
    "alt_g (class-based engine, schema table, mix as actual-mix margin less flexed profit): '221 passed' on seeds 0-9 and 25 for each (r6_checks.py).")
row("proj-instances", "Case generator and its validity tests",
    "course/modules/AC/AC4/grader/instance.py", "PASS",
    "instance.py changed in this delta (comments and the module docstring only: 'three products'); n_products is fixed at 3 in code. "
    "Payloads compared with the 00745fe copy (git show) for seeds 0-499: identical (r6_checks.py). The suite passes on the reference on seeds 0, 1, 2, 3, 5, 99, 455320725 (pytest) and 0-49 (run_graders.py).")
row("proj-alt-instance-coverage", "Instance generator, starter and reference support the alternative-engine probes",
    "course/modules/AC/AC4/grader/instance.py; course/modules/AC/AC4/grader/starter.py; course/modules/AC/AC4/grader/reference.py; course/modules/AC/AC4/grader/test_project.py", "PASS",
    "starter.py and reference.py are byte-identical to 00745fe (not in the git diff). instance.py: payloads identical to 00745fe for seeds 0-499 (r6_checks.py). test_project.py (740 lines) was read in full this round, including every changed hunk and the new tests; "
    "the starter fails the suite (run_graders.py starter check: PASS). Seeds 0-9 and 25 are used by the alternatives.")
row("proj-mutants-m01-m06", "Mutants m01-m06 killed by the grader",
    "ledgers/AC4/mutants/m01_mix_folded_into_price.py ... m06_no_zero_budget_guard.py", "PASS",
    "tools/mutate_graders.py --unit AC4 --seeds 0-9 (output /tmp/ac4-v/e6/mutate4.out): KILLED m01-m06 with killed_by named. "
    "ledgers/AC4/scripts/AC4-e-r6/run_mutants.py seeds 0-3: KILLED on every seed.")
row("proj-mutant-m07-empty-name", "Mutant m07 (empty product name accepted) is killed",
    "ledgers/AC4/mutants/m07_empty_name_accepted.py; course/modules/AC/AC4/grader/test_project.py (test_empty_product_name_raises_value_error, line 615)", "PASS",
    "mutate_graders.py seed 0: KILLED by test_empty_product_name_raises_value_error; run_mutants.py seeds 0-3: KILLED.")
row("proj-spec-empty-name-claim", "Constraints claim: ValueError for an empty or duplicated product name",
    "course/modules/AC/AC4/project.html line 263 (Constraints); course/modules/AC/AC4/grader/test_project.py (lines 607 and 615)", "PASS",
    "test_duplicate_product_names_raise_value_error (line 607, parametrised over FUNCTIONS) and test_empty_product_name_raises_value_error (line 615) pass on the reference; m07 and m12 are KILLED.")
row("proj-spec-fresh-objects-claim", "Constraints claim: master_budget returns a fresh object on each call",
    "course/modules/AC/AC4/project.html line 263; course/modules/AC/AC4/grader/test_project.py (test_master_returns_fresh_objects, line 243)", "PASS",
    "test_master_returns_fresh_objects passes on the reference; mutant m27 (cached object returned) fails it: run_mutants.py seed 0-3 'FAILED test_project.py::test_master_returns_fresh_objects'. "
    "The purity-of-argument claim on the same line is a separate row (proj-purity-order-dependence).")
row("proj-spec-clarity-and-errors", "Constraints line 263 claims ValueError for every listed invalid input: a case without a required field; a value that is not a whole number (a float and a boolean are both refused); a negative count or amount; an empty product list; an empty or duplicated name; no budgeted units; a negative or non-integer actual unit count",
    "course/modules/AC/AC4/project.html line 263 (Constraints); course/modules/AC/AC4/grader/test_project.py", "FAIL",
    "Round-5 survivors are now KILLED: m25 by test_missing_case_field_raises_value_error[actual_inputs_used-master_budget], m26 by test_negative_input_price_raises_value_error[master_budget]. "
    "The missing-field, negative-field, empty-list, name and budgeted-units items are enforced. The whole-number item is not: the only float tests are budget_price_cents (test_float_money_raises_value_error), "
    "the actual-units argument (test_float_actual_units_argument_raises_value_error) and a boolean in fixed_overhead_cents. Four new student-error mutants accept a fraction in one of the other integer fields and truncate it: "
    "m30_fractional_input_price_truncated (200.5 read as 200), m31_fractional_actual_inputs_truncated (5300.5 read as 5300), m32_fractional_actual_units_truncated (1199.6 read as 1199), m33_fractional_fixed_overhead_truncated (2000000.75 read as 2000000). "
    "All four SURVIVED mutate_graders.py seeds 0-9 and run_mutants.py seeds 0-3 (every seed rc 0, 221 passed).",
    fix="Add a parametrised test over every integer field (case: input_price_cents, fixed_overhead_cents, actual_inputs_used; product: budget_units, budget_price_cents, standard_inputs_per_unit, actual_units, actual_price_cents) that passes a fraction such as x.5 or a float such as x.0 and expects ValueError from each FUNCTION, then m30-m33 are KILLED. Or narrow line 263 to the whole-number checks the suite makes.")
row("proj-messages-bare-asserts", "Every assertion in the grader carries a message",
    "course/modules/AC/AC4/grader/test_project.py", "PASS",
    "ast walk over test_project.py: 69 assert statements, 0 without a message (the count rose from 68 with the new shared-case assertion).")
row("proj-messages-no-leak", "Assertion messages do not reveal expected values or wording the tests do not check",
    "course/modules/AC/AC4/grader/test_project.py (all assert messages, including the new missing-field, negative-field and shared-case messages)", "PASS",
    "Read every assert message, must_raise condition string and the new messages (lines 552-557, 637-641, 677-683, 733-739). None prints an expected value. "
    "The new test_shared_case_is_unchanged_by_the_suite message names the property only.")
row("proj-rubric-exhaustive", "Rubric table: every criterion has four observable levels",
    "course/modules/AC/AC4/project.html lines 314-318 (rubric rows)", "PASS",
    CARRY + "lines 314-318 unchanged (rubric C1-C5 each have four levels; re-read this round).")
row("proj-rubric-scoring-rule", "Scoring rule paragraph is complete and each term is defined before it is used",
    "course/modules/AC/AC4/project.html line 308 (Scoring rule)", "PASS",
    CARRY + "line 308 unchanged; the terms 'tied to a case figure', 'tied to a named product', 'input count' and 'action' are defined there before the rubric rows.")
row("proj-rubric-C4-observation", "C4 observation and threshold definition matches the C4 descriptors and the Exemplar B threshold",
    "course/modules/AC/AC4/project.html lines 306, 316, 373", "PASS",
    CARRY + "the definition (line 306), the C4 level-4 descriptor (line 316) and the Exemplar B threshold (line 373) are unchanged; the threshold re-derived: mix = (1200 - 1500*1000/1400)(4400 - m_D) with m_D = P - 1000 changes sign at P = 5,400.")
row("proj-calib-A-scores", "Exemplar A data-scores (2,2,2,1,2) match the rubric",
    "course/modules/AC/AC4/project.html line 326 (data-scores), exemplar A text lines 330-340", "PASS",
    CARRY + "Exemplar A text and data-scores unchanged; 318 body words; overall level min(2,2,2,1,2) = 1 matches data-level 1.")
row("proj-calib-A-annotation", "Exemplar A annotation matches the descriptors and the memo text",
    "course/modules/AC/AC4/project.html lines 343-351", "PASS",
    CARRY + "annotation lines unchanged and each cites an unchanged passage.")
row("proj-calib-B-scores", "Exemplar B data-scores (4,4,3,4,4) match the rubric as the memo now reads",
    "course/modules/AC/AC4/project.html line 357 (data-scores), exemplar B Result paragraph line 363", "PASS",
    CARRY + "Exemplar B memo text and data-scores unchanged since 00745fe; the Result paragraph's five cent figures (+220,000; +542,857; +180,000; -40,000; -462,857) re-derived and sum to 220,000 exactly.")
row("proj-calib-B-annotation", "Exemplar B annotation matches the text and the descriptors",
    "course/modules/AC/AC4/project.html lines 377-382", "PASS",
    CARRY + "annotation lines unchanged.")
row("proj-memo-structure-length", "Memo exemplars: headings and body length as the rubric states",
    "course/modules/AC/AC4/project.html lines 330-340 (A memo-text) and 361-373 (B memo-text)", "PASS",
    CARRY + "both memo-texts unchanged; script over <p> bodies: Exemplar A 318 words (three headings), Exemplar B 393 words (four headings). Both inside 300-600.")
row("proj-lab-1", "Lab 1 runs, and its output matches the expected block",
    "course/modules/AC/AC4/project.html lines 53-147; tests/labs/AC4/lab-AC4-project-1.py", "PASS",
    "python -I -W error tests/labs/AC4/lab-AC4-project-1.py -> exit 0. Compared with the page's expected block (<pre class=\"expected\">) by script: identical. "
    "run_labs.py --unit AC4: 'PASS (10/10)'.")
row("proj-lab-1-interpretation", "Lab 1 interpretation agrees with the lab output and with the step 6 explanation",
    "course/modules/AC/AC4/project.html line 146 (interpretation)", "PASS",
    CARRY + "line 146 unchanged and the lab twin unchanged. Re-derived this round: 5,300 input units against a standard of 5,100 (3x1200 + 5x300); 71.4% to 80.0%; 4,400 vs 8,000 margin; exact flexed profit minus whole-cent = 1/7.")
row("proj-lab-2", "Lab 2 (completion) reproduces Lab 1 output",
    "course/modules/AC/AC4/project.html lines 149-243; tests/labs/AC4/lab-AC4-project-2.py", "PASS",
    "python -I -W error tests/labs/AC4/lab-AC4-project-2.py -> exit 0; output diff against Lab 1: IDENTICAL.")
row("proj-exemplar-B-consequences", "Exemplar B input-price consequence (210 cents) is arithmetically right",
    "course/modules/AC/AC4/project.html line 370 (Assumptions)", "PASS",
    CARRY + "line 370 unchanged; 5,300 x (210 - 200) = 53,000; 220,000 - 53,000 = 167,000.")
row("proj-exemplar-B-threshold", "Exemplar B reversing threshold of 5,400 cents is right",
    "course/modules/AC/AC4/project.html line 373", "PASS",
    CARRY + "line 373 unchanged; the sign change is at P = 5,400 (re-derived).")
row("proj-mutants-m08-m11", "Mutants m08-m11 killed",
    "ledgers/AC4/mutants/m08_efficiency_on_budget_units.py ... m11_flexed_profit_rounded_once.py", "PASS",
    "mutate4.out: KILLED m08, m09, m10, m11 (killed_by named); run_mutants.py seeds 0-3: KILLED.")
row("proj-mutants-m13-m20", "Mutants m13-m20 killed",
    "ledgers/AC4/mutants/m13_mix_rounded_from_exact_fraction.py ... m20_integral_float_accepted.py", "PASS",
    "mutate4.out: KILLED m13-m20 (killed_by named); run_mutants.py seeds 0-3: KILLED on every seed.")
row("proj-mutants-m15-m19", "Round-3 survivors m15, m17, m18, m19 are killed",
    "ledgers/AC4/mutants/m15_negative_actual_inputs_accepted.py, m17, m18, m19", "PASS",
    "mutate4.out: m15 by test_negative_actual_inputs_raises_value_error[master_budget]; m17 by test_negative_actual_product_field_raises_value_error[actual_units-master_budget]; "
    "m18 by test_negative_fixed_overhead_raises_value_error[master_budget]; m19 by test_negative_actual_product_field_raises_value_error[actual_price_cents-master_budget].")
row("proj-mutants-m21-m24", "Student-error mutants m21-m24 (round 4) are killed",
    "ledgers/AC4/mutants/m21_missing_product_field_defaults_to_zero.py, m22_negative_budget_price_accepted.py, m23_negative_standard_inputs_accepted.py, m24_missing_input_price_defaults_to_zero.py", "PASS",
    "mutate4.out: m21 by test_missing_product_field_raises_value_error[budget_units-master_budget]; m22 by test_negative_budget_price_raises_value_error[master_budget]; "
    "m23 by test_negative_standard_inputs_raises_value_error[master_budget]; m24 by test_missing_case_field_raises_value_error[input_price_cents-master_budget] (the round-4 test name was replaced by the case-field test).")
row("proj-mutants-m21-m24-equivalence", "Equivalent-mutant check for the mutants that were not killed",
    "ledgers/AC4/mutants/m21..m24", "PASS",
    "All four are killed, so no equivalence proof is needed. Each accepts an input that the page's Constraints line says must raise ValueError.")
row("proj-spec-coverage-claims", "Coverage claim on the page (line 265) maps to tests: 'each named ValueError; purity and silence'",
    "course/modules/AC/AC4/project.html line 265; course/modules/AC/AC4/grader/test_project.py", "FAIL",
    "Line 265 says the suite covers 'each named ValueError; purity and silence'. Two named items are not fully enforced: the whole-number ValueError (m30-m33 SURVIVED, see proj-spec-clarity-and-errors) and purity (m34 SURVIVED, see proj-purity-order-dependence). "
    "Budgets, variances, reconciliation, sign, zero-variance, single-product, zero-unit and silence are backed by named tests that pass on the reference and kill their mutants.",
    fix="Make the suite kill m30-m34 (see those rows) or narrow line 265 to the checks the suite enforces.")
row("proj-mutant-m12-duplicate-names", "Mutant m12 (duplicate names accepted by two functions) is killed",
    "ledgers/AC4/mutants/m12_duplicate_names_accepted_in_two_functions.py; course/modules/AC/AC4/grader/test_project.py (line 607)", "PASS",
    "mutate4.out: KILLED by test_duplicate_product_names_raise_value_error[master_budget]; run_mutants.py seeds 0-3: KILLED.")
row("proj-hours", "Hours: hub split and lesson hours agree; project table sums to the declared 20 hours",
    "course/modules/AC/AC4/project.html lines 277-285; course/modules/AC/AC4/index.html line 29 (data-hours-lessons 50, data-hours-project 20); lesson pages L01-L08 data-hours", "PASS",
    "data-hours: L01 6, L02 7, L03 6, L04 6, L05 7, L06 6, L07 6, L08 6 = 50 = data-hours-lessons. Project table rows 1+2+2+6+4+2+2+1 = 20 = data-hours-project. 50 + 20 = 70 = the eyebrow. Hours are design targets; not paced.")
row("proj-cards-structure", "cards.json structure: every card has id, lesson, front, back; grade in T/C/U when present",
    "course/modules/AC/AC4/cards.json", "PASS",
    "ledgers/AC4/scripts/AC4-e-r6/cards_check.py: 119 cards, 0 structure problems. 32 cards carry no grade (definitions and misconceptions); check_pages.py validates grade only when present, and BUILDER_RULES 7 grades only graded results.")
row("proj-cards-duplicates", "Full duplicate scan of cards (ids, fronts, backs)",
    "course/modules/AC/AC4/cards.json", "PASS",
    "cards_check.py: 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs (case-insensitive, stripped), after the c053 front change.")
row("proj-cards-sample", "Sample cards AC4-c010 ... c100 agree with their current lessons",
    "course/modules/AC/AC4/cards.json (c010, c020, c030, c040, c050, c060, c070, c080, c090, c100, c025)", "PASS",
    "c025 (changed) re-verified against L02 Proposition 3.2 (line 98): 'for any change in volume h with Q and Q+h in a range where the price, the variable cost and the fixed cost do not change (no step)... exactly'. "
    "c100 re-verified against L08 line 302 (Lemma 8.3 wording) and L08 line 119 (30 to 102.8). c050 re-verified against L04 Example 4.1 (line 358). Other sampled cards byte-identical since 00745fe and their numbers appear in their lessons (cards_check.py).")
row("proj-cards-targeted", "Targeted cards agree with the lesson text where the lesson changed in this delta",
    "course/modules/AC/AC4/cards.json (c029, c062, c063, c064, c066, c067, c075, c076, c079, c080, c081, c083, c084, c087, c088, c089, c094, c112, c118, c119)", "PASS",
    "Re-read this round against the current lessons (the lesson hunks in L01-L08 touched some of these): c029 and c118 against lab-AC4-L02-1 output (first whole volume 89; loss runs 0-88 and 2001-2088; margin of safety 411.11 / 16.44%); "
    "c062-c067 and c080-c081 against lab-AC4-L05-1 and lab-AC4-L06-1 output (static +140,000; volume-and-mix +265,000; flexible -125,000; L06 -40,000 / +249,000 / +16,000 / -75,000, total +150,000; fixed -10,000, operating +140,000); "
    "c063 against the lab's fixed overhead 500,000 per period; c075 and c076 against L06 lines 287 and 283 (2,400 and 2,950 kg, 400 kg for the extra units, 150 kg excess, 2,800 standard); "
    "c079 and c112 against L06 line 408 ('no converse is claimed'); c083 and c084 against L07 lines 72-100; c087, c089, c094 against L07 lines 315, 313-318 and Section 4 (46 SCU, -30,000; range [52, 80]; surplus 140,000); "
    "c088 against L07 line 315 (changed this round: 'the price of the supplier's outside sale'; 2,000 x (55-60) = -10,000; Sigma = 30,000); c118 and c119 against L02 line 267; c081 against L06 lab output.")
row("proj-cards-number-format", "Numeric card backs use the lesson's printed format",
    "course/modules/AC/AC4/cards.json (c101, c102, c109)", "PASS",
    "c101 '2250.00 cents' and '-486.00 cents' and c109 '4 of the 28 pairs' match the L08 lab output (SIM-G RI 2250.00, EVA -486.00; pairs ranked differently 4 of 28). c102 Section 5 example: RI_X 15, RI_Y 20, OI/C 0.12 and 0.10 (L08 line 128).")
row("proj-banned-phrases", "No banned phrase in the project page or the cards",
    "course/modules/AC/AC4/project.html; course/modules/AC/AC4/cards.json", "PASS",
    "grep for 'roughly half', 'about 6%', 'historically', 'typically', 'usually', '...' and the ellipsis character, and for process words (builder, verifier, round, REQUEST, unit report): 0 hits.")
row("proj-simulated-and-data", "Labs and grader use SIMULATED data; no real-data claim is unsupported",
    "course/modules/AC/AC4/project.html lines 53-56 (lab 1 hypothesis) and 252 (Inputs); tests/labs/AC4/lab-AC4-project-1.py", "PASS",
    "Lab 1 inputs are the twin's own typed values (no data file read). Line 252 (changed this round) says 'the course's data manifest holds no plant-level dataset': course/assets/data/market/MANIFEST.json lists three datasets (fx_daily, fx_monthly, ust_daily), none plant-level; tools/data_sources.yaml's rejected list has no plant data.")
row("proj-page-smoke", "Project page loads in Chromium and the in-browser grader passes",
    "course/modules/AC/AC4/project.html; tools/page_smoke.py --unit AC4 --pages project", "PASS",
    "page_smoke AC4: PASS. lab-AC4-project-1 0.0 s; lab-AC4-project-2 0.0 s; in-browser grader: 'All 221 tests pass on seed 1482591378. (0.8 s)'.")
row("proj-check-projects", "check_projects passes for AC4",
    "course/modules/AC/AC4/project.html", "PASS",
    "tools/check_projects.py --all: check_projects AC4: PASS.")
row("proj-check-pages", "check_pages passes for AC4 (cards and page structure)",
    "course/modules/AC/AC4/project.html", "PASS",
    "tools/check_pages.py --all: check_pages AC4: PASS (exit 0).")
row("proj-check-dag", "check_dag passes for AC4",
    "course/modules/AC/AC4", "PASS",
    "tools/check_dag.py --all: check_dag AC4: PASS (exit 0).")
row("proj-ruff-mypy", "ruff and mypy pass on the grader and project labs",
    "course/modules/AC/AC4/grader/; tests/labs/AC4; repository mypy configuration (pyproject.toml)", "PASS",
    "ruff check and ruff format --check on course/modules/AC/AC4/grader and tests/labs/AC4: 'All checks passed!' and '14 files already formatted'. Repository mypy --no-incremental: 'Success: no issues found in 153 source files'. The grader directory is outside the repository mypy file list.")
row("proj-citations-reading", "Reading list keys are in the registry and resolve offline and live",
    "course/modules/AC/AC4/project.html (reading list, references); references/references.json (datar2020horngrens, kaplan1998cost)", "PASS",
    "tools/verify_refs.py --offline: integrity 560 entries, 0 problems. tools/verify_refs.py --unit AC4 (live): 2 of 560 entries, 0 problems. The reading list text is unchanged and makes no claim that depends on the sources.")
row("proj-equal-margin-branch", "Equal-margin branch of the two-product mix test is correct and passes",
    "course/modules/AC/AC4/grader/test_project.py (test_two_product_shift_to_lower_margin_is_unfavourable, lines 463-480)", "PASS",
    CARRY_TESTS + "lines 463-480 unchanged; the branch asserts sales_mix == 0 when margins are equal, which holds for the reference and for alt_a-c and alt_e-g on seeds 0-9 and 25.")
row("proj-grader-equal-margin-comment", "Equal-margin comment states what the algebra proves",
    "course/modules/AC/AC4/grader/test_project.py lines 472-474", "PASS",
    CARRY_TESTS + "comment unchanged; the AT*m integer difference and the whole-cent equality re-derived (flexed profit equals exact profit when margins are equal).")
row("proj-rubric-C2-terms", "C2 rubric terms are defined before use",
    "course/modules/AC/AC4/project.html line 308 (scoring rule) and line 315 (rubric row C2)", "PASS",
    CARRY + "lines 308 and 315 unchanged.")
row("proj-exemplar-overall-level", "Exemplar overall levels follow the scoring rule",
    "course/modules/AC/AC4/project.html line 324 (intro) and article data-level/data-scores lines 326 and 357", "PASS",
    CARRY + "lines 324-326 and 357 unchanged; overall level is the lowest criterion score: A 1, B 3.")
row("proj-ladder-lede", "Ladder lede matches the placement description on the module hub",
    "course/modules/AC/AC4/project.html line 42; course/modules/AC/AC4/index.html line 70 (placement description), line 155 (project ladder section)", "PASS",
    "index.html line 70 changed this round: 'rungs 1 and 2 of the project ladder, described below'. The project ladder is described at index.html line 155 (below line 70). 7/9 = 77.8% and 8/9 = 88.9%, so the 80% bar needs eight correct, as stated. project.html line 42 unchanged and consistent (both skill checks, then rung 3).")
row("proj-inputs-every-number-int", "Every case number is a whole number (int) and the test suite checks types",
    "course/modules/AC/AC4/project.html lines 252 and 260 (Inputs and Conventions); course/modules/AC/AC4/grader/test_project.py (test_flexed_budget_returns_integer_cents, test_variances_are_whole_cents, test_master_budget_values_are_integers)", "PASS",
    "The Inputs text (line 252, changed this round) states whole cents and whole units. The three type tests named check int types for flexed amounts, variances and master-budget values; the reference returns ints throughout. The tests do not check case-input types for every field (see proj-spec-clarity-and-errors).")
row("proj-reading-list-sentence", "Reading list sentence: the autograder needs none of the readings",
    "course/modules/AC/AC4/project.html line 266 (Reading list dd)", "PASS",
    CARRY + "line 266-267 unchanged; the autograder's quantities are defined in the Conventions and Constraints text, not in the readings.")
row("proj-cards-changed-lessons", "Cards whose cited lesson text changed agree with the current lessons",
    "course/modules/AC/AC4/cards.json: AC4-c001, c025, c044, c050, c053, c057, c058, c088, c100", "PASS",
    "Re-verified this round against the current lessons: c025 vs L02 line 98 (Prop 3.2 range wording, now 'no step'); c053 (front and back changed) vs L04 line 110-112 (Prop 3.2 hypothesis; sufficient, no converse stated); "
    "c058 (basis changed to Definition 1.1 stage one) vs L04 lines 58-59 and 481; c088 vs L07 line 315; c050 and c057 vs L04 Example 4.1 (lines 324-330, 358) and lab-AC4-L04-1 output (Y 55,000 allocated, 45,000 avoidable, 30,000 contribution, 15,000 net); "
    "c100 vs L08 line 302 and 119; c001 vs L01 Definition 1.1 (line 59); c044 vs L03 line 516 ('the assumptions in §5'; convention with no registry source).")
row("proj-mutants-m25-m29", "Round-5 survivors m25-m29 are killed",
    "ledgers/AC4/mutants/m25_missing_actual_inputs_defaults_to_zero.py, m26_master_accepts_negative_input_price.py, m27_master_returns_cached_object.py, m28_debug_print_left_in_flexible_budget.py, m29_master_marks_the_argument.py", "PASS",
    "mutate4.out: m25 by test_missing_case_field_raises_value_error[actual_inputs_used-master_budget]; m26 by test_negative_input_price_raises_value_error[master_budget]; m27 by test_negative_units_raise_value_error[master_budget] in mutate_graders (and by test_master_returns_fresh_objects in run_mutants.py); m28 by test_functions_are_silent[flexible_budget]; m29 by test_functions_do_not_change_their_arguments[master_budget].")
row("proj-purity-order-dependence", "Purity: no function changes its argument, including with product rows in other orders",
    "course/modules/AC/AC4/grader/test_project.py (test_functions_do_not_change_their_arguments, line 703; test_shared_case_is_unchanged_by_the_suite, line 733); ledgers/AC4/mutants/m34_master_sorts_caller_products_in_place.py", "FAIL",
    "m29 (round-5 survivor) is now KILLED, because fresh() now copies the pristine case. But m34 (validate, then sort the caller's products list by name in place) SURVIVED mutate_graders.py seeds 0-9 and run_mutants.py seeds 0-3 (rc 0 on every seed). "
    "The suite's case always lists Alpha, Beta, Gamma, which is already sorted, so no purity test sees the reordering. The purity claim on line 265 and line 263 ('never change an argument') is therefore not enforced for unsorted product rows.",
    fix="Add a purity test over a case whose products are in reverse name order (for each FUNCTION, deep-copy it, call the function, compare with a deep copy taken before), so m34 is KILLED. Alternatively narrow the claim to the case the suite generates.")
row("proj-mutants-r6-new", "Round-6 student-error mutants m30-m34 are killed",
    "ledgers/AC4/mutants/m30_fractional_input_price_truncated.py, m31_fractional_actual_inputs_truncated.py, m32_fractional_actual_units_truncated.py, m33_fractional_fixed_overhead_truncated.py, m34_master_sorts_caller_products_in_place.py", "FAIL",
    "Five new mutants written by this verifier (each a complete module from reference.py with one plausible error): m30-m33 accept a fraction and truncate it, m34 sorts the caller's list in place. "
    "mutate_graders.py --unit AC4 --seeds 0-9: SURVIVED m30, m31, m32, m33, m34 (killed_by None). run_mutants.py seeds 0-3: SURVIVED on every seed. None is equivalent: each accepts an input the page says must raise ValueError (m30-m33) or changes an argument the page says must not be changed (m34).",
    fix="See proj-spec-clarity-and-errors (whole-number tests) and proj-purity-order-dependence (reversed-order purity test); rerun mutate_graders.py until these five are KILLED.")
row("proj-mutant-descriptions", "Each mutant's opening docstring describes its error (VERIFIER_RULES 2.6)",
    "ledgers/AC4/mutants/m21_missing_product_field_defaults_to_zero.py ... m29_master_marks_the_argument.py", "FAIL",
    "On the checkout's copy (round-5 files), m21-m29 opened with the reference solution's docstring ('Reference solution for the AC4 budget and variance engine'), so mutate_graders.py printed that text as each mutant's description. "
    "This verifier replaced each module docstring in ledgers/AC4/mutants (in this checkout only) with a one-line description of its error; mutant bodies unchanged. The rerun output in mutate4.out shows the corrected descriptions.",
    fix="Keep the corrected first lines in ledgers/AC4/mutants (done in the checkout); the next fragment must cite the corrected files.")
row("proj-stretch-two-inputs", "Stretch item 'Two inputs' describes a count consistent with the variances defined in the spec",
    "course/modules/AC/AC4/project.html line 399 (Rung 4 Stretch, 'Two inputs')", "FAIL",
    "The rewritten sentence says: 'Give an efficiency variance for each input, and show that the four variances still add to the total.' With two inputs the specification's four variances become five terms (sales price, sales volume, sales mix, and one efficiency variance per input), so 'the four variances' is a count the sentence does not support. "
    "The round-5 text said 'four product variances', which had the same defect.",
    fix="Change to 'show that the sales price, sales volume, sales mix and the two efficiency variances still add to the total', or 'show that the variances still add to the total'.")
row("proj-grader-comments", "Grader comments state what the code does",
    "course/modules/AC/AC4/grader/test_project.py lines 43-44 (PRISTINE comment) and line 734 (test_shared_case_is_unchanged_by_the_suite comment)", "FAIL",
    "Line 43-44: 'a learner's function that changes CASE in place would otherwise be hidden from the purity test, which builds its own case from CASE'. The purity test (test_functions_do_not_change_their_arguments) now builds its case from PRISTINE via fresh(), so the comment describes code that no longer exists. "
    "Line 735: 'every test before it has passed the shared CASE to the learner's functions'. Several earlier tests (test_module_defines_the_three_functions, test_signatures_match_the_contract, test_instance_* and test_only_standard_library_imports) never pass CASE to a learner function, so 'every' is an overstatement.",
    fix="Line 43-44: 'the purity test builds its own case from PRISTINE'. Line 734: 'many tests before it have passed the shared CASE to the learner's functions'.")

# mutants from the official run
mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$")
for line in MUT_LOG.read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    entry = {"id": fname[:-3], "file": f"ledgers/AC4/mutants/{fname}", "description": desc}
    entry["killed_by"] = None if killed.strip() == "None" else killed.strip()
    mutants.append(entry)
assert len(mutants) == 34, len(mutants)

fragment = {
    "unit": "AC4",
    "slice": "AC4-e",
    "round": 6,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 6, slice AC4-e; did not build AC4)",
    "pin": "d57df1e",
    "base": "00745fe (round-5 pin; /tmp/fanout-frags/AC4-e.round5.json used as context only; carried rows name their cited subject and the round-5 source)",
    "previous_ledger": "/tmp/fanout-frags/AC4-e.round5.json",
    "checkout": "/tmp/verify6-AC4-e",
    "scratch": "/tmp/ac4-v/e6",
    "verified_at": VERIFIED_AT,
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 00745fe..d57df1e for this slice: project.html (lines 252, 265, 399), grader/instance.py (comments and docstring only; payloads identical for seeds 0-499), grader/test_project.py (missing-field, negative-input, purity and shared-case tests), cards.json (c025, c053, c058, c088). reference.py, starter.py, the project labs and the memo exemplars are unchanged.",
        "Lesson pages L01-L08 and index.html changed in this delta but are outside this slice; the cards cite them, so the cards' cited passages were re-read (see proj-cards-changed-lessons and proj-cards-targeted). index.html line 70 and the ladder text were re-read for proj-ladder-lede.",
        "Mutants: 34 in ledgers/AC4/mutants (29 from rounds 4-5, now with corrected docstrings for m21-m29; 5 new this round: m30-m34). mutate_graders.py --unit AC4 --seeds 0-9: 29/34 killed; the five survivors are m30-m34.",
        "Alternatives: alt_a-c (round 4) rerun, and alt_e, alt_f, alt_g written this round from the page spec; all 221 pass on seeds 0-9 and 25.",
        "Not checked: lesson pages L01-L08 line by line (outside this slice); index.html Data status section (changed this round, outside this slice); the full text of the memo rubric beyond the lines cited; any external source (the reading list is registry-backed and the page says it makes no claim that depends on it); the Pyodide runtime beyond page_smoke's Chromium run.",
        "Scratch scripts: ledgers/AC4/scripts/AC4-e-r6/ (r6_checks.py, write_fragment_r6.py, alt_e.py, alt_f.py, alt_g.py, alternatives_r4.py, cards_check.py, run_mutants.py, plus round-5 helpers). Logs: /tmp/ac4-v/e6/ (mutate4.out, run_mutants2.out, run_labs.out, page_smoke.out, verify_offline.out, verify_live.out, check_pages.out, check_dag.out, check_projects.out, run_graders.out).",
    ],
    "summary": {},
}
nf = sum(1 for r in rows if r["status"] != "PASS")
fragment["summary"] = {
    "rows": len(rows),
    "pass": len(rows) - nf,
    "fail": nf,
    "non_pass_ids": [r["id"] for r in rows if r["status"] != "PASS"],
    "mutants": len(mutants),
    "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
}
out = ROOT / "ledgers/AC4/AC4-e.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"])
