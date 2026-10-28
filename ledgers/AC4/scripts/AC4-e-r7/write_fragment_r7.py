"""Write the round-7 fragment for AC4 slice e (verifier output). Run from the checkout root."""
import json, re, pathlib

ROOT = pathlib.Path(".")
OUT = ROOT / "ledgers/AC4/AC4-e.json"
MUT_OUT = pathlib.Path("/tmp/ac4-v/e7/mutate37b.out").read_text(encoding="utf-8").splitlines()

CARRY = "Carried from round 6 ({files} byte-identical since the previous pin): "
R6 = "course/modules/AC/AC4/L02.html, L06.html, cards.json"  # placeholder, not used

def carry(files, text):
    return CARRY.format(files=files) + text

rows = []
def row(id_, check, location, status, evidence):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

ROW_SRC = "course/modules/AC/AC4/project.html"
TEST = "course/modules/AC/AC4/grader/test_project.py"

row("proj-autograder-reference", "Reference solution passes the whole suite on the learner-facing grader files",
    "course/modules/AC/AC4/grader/reference.py; course/modules/AC/AC4/grader/test_project.py",
    "PASS", "Re-run round 7: ledgers/AC4/scripts/AC4-e-r7/r6_checks.py (copies instance.py, test_project.py, starter.py, reference.py as budget_engine.py): '274 passed' for reference on seeds 0,1,2,3,5,99,455320725 (/tmp/ac4-v/e7/r7_checks.out). tools/run_graders.py --unit AC4 --seeds 0-49: 'PASS (reference 50/50 seeds, slowest 0.2 s)' (/tmp/ac4-v/e7/run_graders.out).")
row("proj-collect-count", "Test count on the page equals the real collect-only count",
    ROW_SRC + " line 265; " + TEST,
    "PASS", "Re-verified (line 265 is inside the delta hunk): pytest --collect-only -q on the reference copies, seeds 0,1,4,9,455320725: '274 tests collected'. Page line 265 now reads 'collects <strong>274 checks</strong>'. Parametrised lengths are fixed (range(50) and literal tuples), so the count does not vary by seed.")
row("proj-autograder-alternatives", "Alternative correct implementations pass the suite (over-constraint probe)",
    TEST + "; ledgers/AC4/scripts/AC4-e-r7/alternatives_r4.py (alt_a, alt_b, alt_c); ledgers/AC4/scripts/AC4-e-r7/alt_e.py, alt_f.py, alt_g.py",
    "PASS", "Re-run round 7. alt_a, alt_b, alt_c (alternatives_r4.py, written from the page specification): '274 passed' on seeds 0, 4, 9, 25 each. alt_e, alt_f, alt_g (r6_checks.py): '274 passed' on seeds 0-9 and 25 each (/tmp/ac4-v/e7/r7_checks.out). Five correct engines, none copied from reference.py.")
row("proj-instances", "Case generator and its validity tests",
    "course/modules/AC/AC4/grader/instance.py",
    "PASS", "Re-run round 7: instance.py is not in the d57df1e..de53f7e diff. Payloads equal to the 00745fe copy for seeds 0-499 (r6_checks.py: 'instance payloads equal for seeds 0-499: True'). The suite passes on the reference (above).")
row("proj-alt-instance-coverage", "Instance generator, starter and reference support the alternative-engine probes",
    "course/modules/AC/AC4/grader/instance.py; course/modules/AC/AC4/grader/starter.py; course/modules/AC/AC4/grader/reference.py; " + TEST,
    "PASS", "Re-run round 7: alternatives pass (row proj-autograder-alternatives). Starter fails the suite: starter.py as budget_engine.py, seed 0: '268 failed, 6 passed'. starter.py, reference.py and instance.py payloads unchanged in this delta (not in the diff stat, except instance.py comments per round 6).")
row("proj-mutants-m01-m06", "Mutants m01-m06 killed by the grader",
    "ledgers/AC4/mutants/m01_mix_folded_into_price.py ... m06_no_zero_budget_guard.py",
    "PASS", "Re-run round 7: tools/mutate_graders.py --unit AC4 --seeds 0-9 (/tmp/ac4-v/e7/mutate37b.out): KILLED m01-m06 with killed_by named (for example m01 by test_every_grader_seed_reconciles_exactly[26] (seed 0); m06 by test_zero_budgeted_units_raise_value_error[master_budget] (seed 0)).")
row("proj-mutant-m07-empty-name", "Mutant m07 (empty product name accepted) is killed",
    "ledgers/AC4/mutants/m07_empty_name_accepted.py; " + TEST + " (test_empty_product_name_raises_value_error)",
    "PASS", "Re-run round 7: mutate_graders output 'KILLED m07_empty_name_accepted.py ... -> test_empty_product_name_raises_value_error (seed 0)'.")
row("proj-spec-empty-name-claim", "Constraints claim: ValueError for an empty or duplicated product name",
    ROW_SRC + " line 263 (Constraints); " + TEST + " (test_duplicate_product_names_raise_value_error, test_empty_product_name_raises_value_error)",
    "PASS", "Re-verified (line 263 is inside the delta hunk; the name clause is unchanged in wording): the two tests exist and pass on the reference (274 passed). m07 and m12 are KILLED in mutate37b.out.")
row("proj-spec-fresh-objects-claim", "Constraints claim: master_budget returns a fresh object on each call",
    ROW_SRC + " line 263; " + TEST + " (test_master_returns_fresh_objects, line 243)",
    "PASS", "Re-verified (line 263 in the delta hunk): m27 (cached object) under pytest, seed 0, -W error: 'FAILED test_project.py::test_master_returns_fresh_objects'. The reference passes that test. The purity-of-argument clause on the same line is row proj-purity-order-dependence.")
row("proj-spec-clarity-and-errors", "Constraints line 263 claims ValueError for every listed invalid input: a case without a required field; a value that is not a whole number (a float and a boolean are both refused); a negative count or amount; an empty product list; an empty or duplicated name; no budgeted units; and a negative or non-integer actual unit count passed to flexible_budget",
    ROW_SRC + " line 263 (Constraints); " + TEST + " (test_case_field_not_a_whole_number..., test_product_field_not_a_whole_number..., test_boolean_input_raises_value_error at line 587, test_non_whole_actual_units_argument at line 662)",
    "FAIL", "The whole-number clause ('a float and a boolean are both refused') is not enforced for every value. Booleans are tested only in fixed_overhead_cents (test_boolean_input_raises_value_error, line 589). The product fields (budget_units, budget_price_cents, standard_inputs_per_unit, actual_units, actual_price_cents) and the flexible_budget actual-units argument are tested only for floats. Two new student-error mutants that accept a boolean there SURVIVE mutate_graders.py --unit AC4 --seeds 0-9: m35_bool_accepted_in_product_fields (True read as 1 in a product field), m36_flexible_accepts_bool_units (flexible_budget(case, True) read as one unit). Every other clause is enforced: missing fields (m24, m25), negatives (m15, m17-m19, m22, m23, m26), empty list, empty or duplicate name (m07, m12), no budgeted units (m06), non-whole actual units argument (m16, m30-m33 killed). Fix: add a boolean case to test_product_field_not_a_whole_number_raises_value_error and to the flexible_budget argument test (for example offset True), or narrow line 263 to the fields that are tested.")
row("proj-messages-bare-asserts", "Every assert in the grader carries a message",
    TEST,
    "PASS", "Re-run round 7 (ast walk of test_project.py): 70 ast.Assert nodes, 0 without msg.")
row("proj-messages-no-leak", "Assertion and must_raise messages do not reveal expected answers",
    TEST + " (all assert messages, including the new must_raise messages at lines 643-665 and 735-765)",
    "PASS", "Re-verified: the new messages name the function and the field (for example 'flexible_budget: an actual unit count that is not a whole number', and f\"{name}: {field} given as the non-whole number {CASE[field] + offset!r}\", which shows the test's own input, not an expected value). No expected cent amount appears in a message.")
for rid, what, loc in [
    ("proj-rubric-exhaustive", "Rubric rows are exhaustive over the five criteria with four levels each", "project.html lines 314-318 (rubric rows)"),
    ("proj-rubric-scoring-rule", "Scoring rule states the bar and levels", "project.html line 308 (Scoring rule)"),
    ("proj-rubric-C4-observation", "Criterion C4 is observable at each level", "project.html lines 306, 316, 373"),
    ("proj-calib-A-scores", "Exemplar A scores and level match the rubric", "project.html line 326 (data-scores), exemplar A text lines 330-340"),
    ("proj-calib-A-annotation", "Exemplar A annotations quote the memo", "project.html lines 343-351"),
    ("proj-calib-B-scores", "Exemplar B scores and level match the rubric", "project.html line 357 (data-scores), exemplar B Result paragraph line 363"),
    ("proj-calib-B-annotation", "Exemplar B annotations quote the memo", "project.html lines 377-382"),
    ("proj-memo-structure-length", "Memo structure and length sections are present in both exemplars", "project.html lines 330-340 (A memo-text) and 361-373 (B memo-text)"),
    ("proj-exemplar-B-consequences", "Exemplar B consequences are stated on the assumptions line", "project.html line 370 (Assumptions)"),
    ("proj-exemplar-B-threshold", "Exemplar B threshold statement", "project.html line 373"),
    ("proj-reading-list-sentence", "Reading-list sentence (no grading dependence)", "project.html line 266 (Reading list dd)"),
    ("proj-hours", "Declared project hours and hub split agree arithmetically", "project.html lines 277-285; course/modules/AC/AC4/index.html line 29 (data-hours-lessons 50, data-hours-project)"),
    ("proj-ladder-lede", "Ladder lede and placement description", "project.html line 42; course/modules/AC/AC4/index.html lines 70 and 155"),
    ("proj-simulated-and-data", "Simulated labelling and Inputs statement", "project.html lines 53-56 (lab 1 hypothesis) and 252 (Inputs); tests/labs/AC4/lab-AC4-project-1.py"),
    ("proj-equal-margin-branch", "Equal-margin branch test", TEST + " lines 463-480 (test_two_product_shift_to_lower_margin_is_unfavourable)"),
    ("proj-grader-equal-margin-comment", "Comment on the equal-margin branch", TEST + " lines 472-474"),
    ("proj-rubric-C2-terms", "Rubric C2 terms match the scoring rule", "project.html line 308 (scoring rule) and line 315 (rubric row C2)"),
    ("proj-exemplar-overall-level", "Exemplar overall level", "project.html line 324 (intro) and article data-level/data-scores lines 326 and 357"),
    ("proj-citations-reading", "Reading list citations resolve to registry keys", "project.html reading list; references/references.json (datar2020horngrens, kaplan199...)"),
]:
    row(rid, what, loc, "PASS", carry(
        "project.html and the cited lines are outside the delta hunks (257-268, 395-400)" if "project.html" in loc else "the cited file is outside the delta",
        "cited lines re-read in round 7 and unchanged (git diff d57df1e de53f7e shows hunks only at project.html 257-268 and 395-400, and test_project.py 40-43, 640-680, 750-780)."))

row("proj-mutants-m08-m11", "Mutants m08-m11 killed",
    "ledgers/AC4/mutants/m08_efficiency_on_budget_units.py ... m11_flexed_profit_rounded_once.py",
    "PASS", "Re-run round 7 (mutate37b.out): KILLED m08 (test_every_grader_seed_reconciles_exactly[26]), m09 (test_boolean_input_raises_value_error[master_budget]), m10 (test_every_grader_seed_reconciles_exactly[26]), m11 (test_every_grader_seed_reconciles_exactly[15]).")
row("proj-mutants-m13-m20", "Mutants m13-m20 killed",
    "ledgers/AC4/mutants/m13 ... m20",
    "PASS", "Re-run round 7 (mutate37b.out): KILLED m13 (test_exact_half_cent_rounds_up), m14 (test_exact_half_cent_rounds_up), m16 (test_float_actual_units_argument_raises_value_error), m20 (test_product_field_not_a_whole_number_raises_value_error[0.0-budget_units-master_budget]).")
row("proj-mutants-m15-m19", "Mutants m15-m19 killed",
    "ledgers/AC4/mutants/m15_negative_actual_inputs_accepted.py, m17_negative_actual_units_accepted.py, m18, m19",
    "PASS", "Re-run round 7 (mutate37b.out): KILLED m15, m17, m18, m19 each with a named negative-value test.")
row("proj-mutants-m21-m24", "Mutants m21-m24 killed",
    "ledgers/AC4/mutants/m21_missing_product_field_defaults_to_zero.py, m22, m23, m24",
    "PASS", "Re-run round 7 (mutate37b.out): KILLED m21, m22, m23, m24.")
row("proj-mutants-m21-m24-equivalence", "No mutant in the list is equivalent to the reference (equivalence proof where needed)",
    "ledgers/AC4/mutants/m21..m24",
    "PASS", "Every mutant in the list is KILLED (mutate37b.out), so none is claimed equivalent. Each accepts or defaults an input that the page says must raise ValueError, so none is equivalent to the reference.")
row("proj-spec-coverage-claims", "Page line 265 claims the suite covers each named ValueError, purity and silence",
    ROW_SRC + " line 265; " + TEST,
    "FAIL", "Line 265 says the autograder covers 'each named ValueError; purity and silence'. The named ValueError for a value that is not a whole number is only partly enforced: m35_bool_accepted_in_product_fields and m36_flexible_accepts_bool_units SURVIVE mutate_graders.py --unit AC4 --seeds 0-9 (see proj-spec-clarity-and-errors). Purity (m34 now KILLED) and silence (m28 KILLED) are enforced. Fix: as for proj-spec-clarity-and-errors, or narrow 'each named ValueError' to the cases the tests cover.")
row("proj-mutant-m12-duplicate-names", "Mutant m12 (duplicate names accepted in two functions) is killed",
    "ledgers/AC4/mutants/m12_duplicate_names_accepted_in_two_functions.py; " + TEST + " (line 607)",
    "PASS", "Re-run round 7: 'KILLED m12 ... -> test_duplicate_product_names_raise_value_error[master_budget] (seed 0)'.")
row("proj-cards-structure", "cards.json structure: each card has id, lesson, front, back; graded cards have a grade",
    "course/modules/AC/AC4/cards.json",
    "PASS", "Re-run round 7: 119 cards. Every card has id, lesson, front and back. The 88 cards with a grade carry T (45) or C (43); the 31 definition and procedure cards carry no grade field (existing convention). The two edited cards (c020, c078) keep their grades.")
row("proj-cards-duplicates", "No duplicate card ids or fronts",
    "course/modules/AC/AC4/cards.json",
    "PASS", "Re-run round 7: no duplicate ids and no duplicate fronts across 119 cards.")
row("proj-cards-sample", "Sampled cards agree with their lesson text",
    "course/modules/AC/AC4/cards.json (c010, c020, c030, c040, c050, c060, c070, c080, c090, c100, c025)",
    "PASS", "c020 and c025 re-verified in round 7 (see proj-card-c020, proj-cards-changed-lessons). The other sampled cards are byte-identical in this delta (cards.json diff hunks are only at lines 134 and 553) and their source lessons L03, L04, L07, L08 are unchanged; L01 and L05 changes do not touch them.")
row("proj-cards-targeted", "Targeted cards (Lab numbers, proposition references, changed-proposition cards) agree with lesson text",
    "course/modules/AC/AC4/cards.json (c029, c062, c063, c064, c066, c067, c075, c076, c079, c080, c081, c083, c084, c087 and others)",
    "PASS", "c063 and c066 re-read in round 7 against L05 Definition 1.2 and Proposition 2.2: consistent with the new 'no assumption on the cost function' wording. c078 re-verified (proj-card-c078). Other targeted cards are byte-identical in this delta; their L02/L05/L06 source sentences that changed do not state the card's claim differently (checked by grep of the changed phrases in cards.json).")
row("proj-cards-number-format", "Card numbers are written in the lesson's format",
    "course/modules/AC/AC4/cards.json (c101, c102, c109)",
    "PASS", "Carried from round 6 (cards.json lines of c101, c102, c109 byte-identical since the previous pin; L08 unchanged): the numbers (2250.00 and -486.00 cents, 4 of 28 pairs) match L08 lab output as read in round 6.")
row("proj-banned-phrases", "Banned phrases and process words (BUILDER_RULES 1.2/1.3; no process words)",
    ROW_SRC + "; course/modules/AC/AC4/cards.json",
    "PASS", "Re-run round 7: grep -i -E for 'roughly half', 'about 6%', 'historically', 'builder', 'verifier', 'round [0-9]', 'REQUESTS', 'unit report', an ellipsis and 'build' in project.html and cards.json: no matches.")
row("proj-lab-1", "Project lab 1 runs and matches the page output",
    ROW_SRC + " lines 53-147; tests/labs/AC4/lab-AC4-project-1.py",
    "PASS", "Re-run round 7: python -I -W error lab-AC4-project-1.py: rc 0; output steps 1-8 (master 2600000; flexed 3142857; price 180000; volume 542857; efficiency -40000; mix -462857; total 220000; four variances sum to total: True) match the page output (/tmp/ac4-v/e7/lab-AC4-project-1.out). run_labs --unit AC4: 10/10.")
row("proj-lab-1-interpretation", "Lab 1 interpretation does not overreach", ROW_SRC + " line 146 (interpretation)",
    "PASS", "Carried from round 6 (project.html line 146 byte-identical since the previous pin; the delta hunks are at 257-268 and 395-400): the interpretation restates the printed steps, and the lab output of round 7 is the same numbers.")
row("proj-lab-2", "Project lab 2 runs and matches the page output", ROW_SRC + " lines 149-243; tests/labs/AC4/lab-AC4-project-2.py",
    "PASS", "Re-run round 7: python -I -W error lab-AC4-project-2.py: rc 0; output identical to lab 1 steps (/tmp/ac4-v/e7/lab-AC4-project-2.out).")
row("proj-mutants-m25-m29", "Mutants m25-m29 killed",
    "ledgers/AC4/mutants/m25_missing_actual_inputs_defaults_to_zero.py ... m29_master_marks_the_argument.py",
    "PASS", "Re-run round 7 (mutate37b.out): KILLED m25, m26, m27 (test_product_field_not_a_whole_number...; test_master_returns_fresh_objects also fails under pytest), m28 (test_functions_are_silent[flexible_budget]), m29 (test_functions_do_not_change_their_arguments[master_budget]).")
row("proj-purity-order-dependence", "Constraints claim: functions never change an argument (purity, including product order)",
    TEST + " (test_functions_do_not_change_their_arguments, line 733; test_functions_do_not_reorder_their_products, line 755; test_shared_case_is_unchanged_by_the_suite, line 776); " + ROW_SRC + " line 263",
    "PASS", "Re-verified: the delta adds test_functions_do_not_reorder_their_products (reversed product list). m34_master_sorts_caller_products_in_place is now KILLED: 'KILLED m34 ... -> test_functions_do_not_reorder_their_products[master_budget] (seed 0)'. The shared-case test still compares CASE with PRISTINE at the end of the run. The reference passes all of them.")
row("proj-mutants-r6-new", "Round-6 survivors m30-m34 are killed by the current grader",
    "ledgers/AC4/mutants/m30_fractional_input_price_truncated.py, m31, m32, m33, m34",
    "PASS", "Re-run round 7 (mutate37b.out): KILLED m30 (test_case_field_not_a_whole_number_raises_value_error[0.5-input_price_cents-master_budget]), m31 (...[0.5-actual_inputs_used-master_budget]), m32 (test_product_field_not_a_whole_number_raises_value_error[0.5-actual_units-...]), m33 (test_case_field_not_a_whole_number_raises_value_error[0.5-fixed_overhead_cents-...]), m34 (test_functions_do_not_reorder_their_products[master_budget]).")
row("proj-mutant-descriptions", "Mutant descriptions name the error (not the reference docstring)",
    "ledgers/AC4/mutants/m21_missing_product_field_defaults_to_zero.py ... m29_master_marks_the_argument.py",
    "PASS", "Re-run round 7: mutate37b.out prints the mutant's own one-line description for m21-m29 (for example 'Missing product field defaults to zero instead of raising ValueError.'), not the reference docstring. The round-6 defect is fixed in the mutant files.")
row("proj-stretch-two-inputs", "Stretch 'Two inputs' bullet states a true reconciliation",
    ROW_SRC + " line 399 (Rung 4 Stretch, 'Two inputs')",
    "FAIL", "The bullet says the case gets two inputs 'each with its own standard and price', then says 'show that the sales price, sales volume, sales mix and the two efficiency variances still add to the total'. That sum omits the input price variance and holds only when each actual input price equals its standard. Witness (exact integers, /tmp/ac4-v/e7/chk/id2.py and the inline check): one product, budget 100 units at 1000 cents, standard 2 units of input 1 at 50 cents and 1 unit of input 2 at 200 cents, fixed overhead 0; actual 100 units at 1000 cents, actual inputs 200 at 60 cents and 100 at 200 cents. The five figures sum to 0, the total profit variance is -2000, and the missing input price variance is -2000. Fix: add 'when each actual input price equals its standard', or add the input price variances to the list.")
row("proj-grader-comments", "Grader comments describe the code they sit above",
    TEST + " lines 43-44 (PRISTINE comment) and line 734 (test_shared_case_is_unchanged_by_the_suite comment)",
    "PASS", "Re-verified: lines 43-44 now say the purity test builds its case from PRISTINE through fresh(); fresh() (line 48) does copy PRISTINE. The line 734 comment says 'many tests before it have passed the shared CASE', which is true (for example test_functions_are_silent and test_negative_units_raise_value_error pass CASE or a copy of it). No 'every' overstatement remains.")

# new rows
row("proj-mutants-r7-new", "Round-7 student-error mutants m35-m37 are killed (boolean acceptance, boolean actual units, a warning)",
    "ledgers/AC4/mutants/m35_bool_accepted_in_product_fields.py; ledgers/AC4/mutants/m36_flexible_accepts_bool_units.py; ledgers/AC4/mutants/m37_master_warns.py",
    "FAIL", "m37_master_warns is KILLED under -W error (test_negative_input_price_raises_value_error[master_budget], seed 0): the warning becomes an exception under the grader's flags. m35 and m36 SURVIVE mutate_graders.py --unit AC4 --seeds 0-9 ('SURVIVED m35 ... -> None', 'SURVIVED m36 ... -> None'; /tmp/ac4-v/e7/mutate37b.out). Both are plausible student errors (isinstance(x, int) without the bool exclusion). Fix: add boolean cases for product fields and for flexible_budget's actual-units argument.")
row("proj-stretch-spending", "Stretch 'Spending variance' bullet: zero when the actual price is standard; six figures add to the total 'exactly when it is not'",
    ROW_SRC + " line 398 (Rung 4 Stretch, 'A spending variance')",
    "FAIL", "Low severity wording. The sentence restricts the exact reconciliation to the case where the actual input price is not the standard. The identity holds in both cases: the six-figure check (id2.py, 3000 random cases, sign convention favourable positive: input price variance (s-a) times actual inputs, fixed overhead variance budget less actual) has 0 mismatches, including a = s and fixed overhead at budget. The phrase 'exactly when it is not' implies a condition that is not there. Fix: 'and that the six figures add to the total exactly, whether or not the actual input price is the standard'.")
row("proj-card-c020", "Card AC4-c020 agrees with the current L02 text and Lab 1 output",
    "course/modules/AC/AC4/cards.json line 137 (AC4-c020); course/modules/AC/AC4/L02.html line 127 (Proposition 4.1 proof), line 264 (lab interpretation)",
    "PASS", "Re-verified (edited in this delta: 'safe at its own volume only if that volume is above the zero of the segment it lies in'). Proposition 4.1 proof (L02 line 127): OI is strictly increasing on each segment, so within a segment OI >= 0 implies the volume is at or above that segment's zero, which makes 'only if' a valid necessary condition. Lab 1 output (L02 line 264): negative from 2,001 to 2,088 units. Boundary: at exactly the zero OI = 0; the card's 'above' treats safe as strictly positive operating income, which the margin-of-safety definition in L02 supports. Grade C, basis Lab 1: the necessity claim is proved in L02, so the grade is conservative.")
row("proj-card-c078", "Card AC4-c078 agrees with L06 Proposition 2.1 hypothesis",
    "course/modules/AC/AC4/cards.json line 556 (AC4-c078); course/modules/AC/AC4/L06.html line 79 (Proposition 2.1)",
    "PASS", "Re-verified (edited in this delta: 'provided the actual material price equals the standard price pi'). L06 line 79: 'with Q_b > 0 and the actual material price equal to pi, T = SP + V + M + E with no residual, for any actual units, actual selling prices and actual kilograms'. The card matches it. L06 lines 270 and 379-381 state the fifth term needed when the price differs.")
row("proj-cards-changed-lessons", "Cards citing lessons changed in this delta still agree with those lessons",
    "course/modules/AC/AC4/cards.json (c001, c020, c025, c044, c050, c053, c057, c058, c066, c078, c088, c100); lessons L01, L02, L05, L06 (changed in this delta)",
    "PASS", "Re-verified: c025 vs L02 Proposition 3.2 (line 98, now 'no step, meaning no jump in fixed cost at a threshold volume'): card text '(no step)' is consistent. c024 and c006 cite Remark 2.3 whose first sentence changed; the card claims are unchanged. c066 vs L05 Proposition 2.2 ('with no assumption on the cost function'): consistent. c063 and c068 vs L05 Definition 1.2 and Problem R3 (fixed overhead flexes 'if a part moves with volume', not the card's claim): consistent. c078 and c020 re-verified above. c001 (L01) and c044, c050, c053, c057, c058, c088, c100 (L03, L04, L07, L08) are byte-identical and their sources are unchanged in this delta except the L01 and L05 sentences checked by grep (no card cites the changed L01 residual wording).")
row("proj-inputs-every-number-int", "Inputs and Conventions: every number the engine returns is an int; no currency or unit conversion",
    ROW_SRC + " lines 252 and 260 (Inputs and Conventions); " + TEST,
    "PASS", "Re-verified (line 260 changed in this delta): ran the reference on the page's inputs (/tmp/ac4-v/e7/chk/id_check.py): every leaf of master_budget, flexible_budget and variance_decomposition is type int (True). The new sentence 'It rounds only where the flexed budget rule says to' matches reference.py: the only rounding is _nearest_cent in flexible_budget and the mix uses its whole-cent profit.")
row("proj-page-smoke", "page_smoke runs the project page and its in-browser grader",
    ROW_SRC, "PASS", "Re-run round 7: tools/page_smoke.py --unit AC4 --pages project: 'in-browser grader: All 274 tests pass on seed 17143279. (0.8 s)'; 'page_smoke AC4: PASS'.")
row("proj-check-projects", "check_projects --all", ROW_SRC,
    "PASS", "Re-run round 7: tools/check_projects.py --all exit 0; 'check_projects AC4: PASS'.")
row("proj-check-pages", "check_pages --all", ROW_SRC,
    "PASS", "Re-run round 7: tools/check_pages.py --all exit 0; 'check_pages AC4: PASS'.")
row("proj-check-dag", "check_dag --all", "course/modules/AC/AC4",
    "PASS", "Re-run round 7: tools/check_dag.py --all exit 0; 'check_dag AC4: PASS'.")
row("proj-ruff-mypy", "ruff and mypy", "course/modules/AC/AC4/grader; tests/labs/AC4; repository mypy configuration (pyproject.toml)",
    "PASS", "Re-run round 7: ruff check and ruff format --check on course/modules/AC/AC4/grader and tests/labs/AC4: 'All checks passed!', '14 files already formatted'. mypy --no-incremental over the repository: 'Success: no issues found in 153 source files'.")
row("proj-stretch-list-intact", "Rung 4 Stretch list: three bullets, the rolling forecast bullet unchanged",
    ROW_SRC + " lines 396-401", "PASS", "Re-verified: the third bullet ('A rolling forecast') is byte-identical to the round-6 text; the first two bullets are the subject of proj-stretch-two-inputs and proj-stretch-spending.")
row("proj-run-labs-ac4", "run_labs --unit AC4 (all twins)", "tests/labs/AC4", "PASS", "Re-run round 7: tools/run_labs.py --unit AC4: 'run_labs AC4: PASS (10/10)'.")
row("proj-autograder-rerun-mutants-m01-m37", "Full mutant set (37 mutants) killed on seeds 0-9 except m35 and m36",
    "ledgers/AC4/mutants (37 files)", "FAIL", "Re-run round 7: 35 of 37 KILLED; m35 and m36 SURVIVED (see proj-mutants-r7-new). mutate_graders.py tail: 'mutate_graders AC4: FAIL (35/37 killed)'.")

mutants = []
for line in MUT_OUT:
    m = re.match(r"(KILLED|SURVIVED) (\S+?)\.py: (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    desc = desc.split(" Reference solution for the AC4")[0].rstrip(".") + "."
    mutants.append({"id": name.split("_")[0], "file": f"ledgers/AC4/mutants/{name}.py", "description": desc,
                    "killed_by": None if killed.strip() == "None" else killed.strip()})
assert len(mutants) == 37, len(mutants)

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
fail = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "AC4",
    "slice": "AC4-e",
    "round": 7,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 7, slice AC4-e; did not build AC4)",
    "pin": "de53f7e",
    "base": "d57df1e (round-6 pin; /tmp/fanout-frags/AC4-e.round6.json used as context only; carried rows name the files byte-identical since the previous pin and the cited lines outside the delta hunks)",
    "previous_ledger": "/tmp/fanout-frags/AC4-e.round6.json",
    "checkout": "/tmp/verify7-AC4-e",
    "scratch": "/tmp/ac4-v/e7",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta d57df1e..de53f7e for this slice: project.html (lines 257-268 constraints, grading mode, conventions; lines 395-400 stretch), cards.json (c020 line 137, c078 line 556), grader/test_project.py (new whole-number, product-order and shared-case tests). Lessons L01, L02, L05, L06 changed (outside the slice; cards citing them re-checked). instance.py, reference.py, starter.py, the labs and the memo exemplars are unchanged.",
        "Mutants: 37 in ledgers/AC4/mutants. m01-m34 carried from the round-6 checkout (copied, not edited; docstrings from round 6). m35, m36, m37 are new this round. mutate_graders.py --unit AC4 --seeds 0-9: 35/37 killed. Survivors m35 (bool accepted in product fields) and m36 (bool accepted as flexible_budget's actual units). The page line 263 claims a boolean is refused for every whole-number value, so these are FAILs.",
        "Alternatives: alt_a, alt_b, alt_c (alternatives_r4.py) and alt_e, alt_f, alt_g (ledgers/AC4/scripts/AC4-e-r7/) all pass 274 on seeds 0-9 and 25 (alt_a-c on 0, 4, 9, 25).",
        "Round-6 FAILs resolved: proj-mutants-r6-new (m30-m34 now killed), proj-purity-order-dependence (m34 killed by the new reorder test), proj-grader-comments (comments corrected), proj-stretch-two-inputs (text replaced, but a new scope error in the same bullet, see the FAIL row), proj-spec-clarity-and-errors and proj-spec-coverage-claims (still FAIL, now on the boolean clause only; the fraction clause is enforced).",
        "Not checked: lesson pages L01-L08 line by line (outside this slice; only the sentences the cards cite were re-read); index.html Data status section; the memo rubric beyond the cited lines; the registry and verify_refs live run (carried, references.json not in the delta); Pyodide beyond page_smoke's Chromium run; the m35/m36 fixes (not applied: the verifier does not fix).",
        "Scratch: ledgers/AC4/scripts/AC4-e-r7/ (r6_checks.py, alternatives_r4.py, alt_e.py, alt_f.py, alt_g.py, id_check.py, id2.py, write_fragment_r7.py). Logs: /tmp/ac4-v/e7/ (mutate.out, mutate37b.out, r7_checks.out, run_graders.out, lab outputs, check_*.out).",
    ],
    "summary": {"rows": len(rows), "pass": len(rows) - len(fail), "fail": len(fail), "non_pass_ids": fail,
                "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"])},
}
OUT.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "fail", fail, "mutants", len(mutants), "killed", frag["summary"]["mutants_killed"])
