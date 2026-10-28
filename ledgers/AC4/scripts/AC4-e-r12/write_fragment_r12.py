"""Write the round-12 AC4-e fragment: carried, re-verified and new rows, and the mutant list with kills.

Inputs: the round-11 fragment (context), the mutant run output (seeds 0,1,25) and the mutant directory.
"""
import ast
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
R11 = json.loads(pathlib.Path("/tmp/fanout-frags/AC4-e.round11.json").read_text(encoding="utf-8"))
RUN = (ROOT / "ledgers/AC4/scripts/AC4-e-r12/out/mutants_all2.out").read_text(encoding="utf-8")
MUT = ROOT / "ledgers/AC4/mutants"
PREV = "91946cf"
r11 = {r["id"]: r for r in R11["rows"]}
r11_mut = {m["id"]: m for m in R11["mutants"]}

# ---- mutants: killed_by from seed 0 of the round 12 run
kills: dict[str, str] = {}
blocks = re.split(r"\n(?=KILLED|SURVIVED)", RUN)
for b in blocks:
    lines = b.strip().splitlines()
    if not lines or not lines[0].startswith(("KILLED", "SURVIVED")):
        continue
    name = lines[0].split()[-1]
    name = name[:-3] if name.endswith(".py") else name
    if lines[0].startswith("KILLED"):
        s0 = [l.strip() for l in lines if l.strip().startswith("seed 0")]
        failed = s0[0].split(" ", 4)[-1] if s0 else ""
        kills[name] = failed
mutants = []
for path in sorted(MUT.glob("*.py")):
    stem = path.stem
    doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
    desc = doc.strip().splitlines()[0] if doc.strip() else ""
    if stem in r11_mut:
        desc = r11_mut[stem]["description"]
    assert stem in kills, f"{stem} did not run as killed"
    killed_test = re.sub(r"^rc 1 ", "", kills[stem]).replace("FAILED ", "").split(" - ")[0]
    mutants.append({
        "id": stem,
        "file": f"ledgers/AC4/mutants/{path.name}",
        "description": desc,
        "killed_by": f"{killed_test} (seed 0; also killed on seeds 1 and 25)",
    })
assert len(mutants) == 79, len(mutants)

CARRY = "Carried from round 11 ({files} byte-identical since the previous pin {pin}): "

def carry(rid, files, location=None, note=""):
    r = dict(r11[rid])
    r["evidence"] = CARRY.format(files=files, pin=PREV) + r11[rid]["evidence"] + (" " + note if note else "")
    if location:
        r["location"] = location
    r["status"] = "PASS"
    return r

def row(rid, check, location, evidence):
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}

P = "course/modules/AC/AC4/"
T = P + "grader/test_project.py"
rows = []

# ---------- command and tool rows (re-run this round)
rows += [
    row("proj-autograder-reference", "Reference solution passes the whole suite on the learner-facing grader files",
        P + "grader/reference.py; " + P + "grader/test_project.py",
        "Re-run round 12: tools/run_graders.py --unit AC4 --seeds 0-49 -> 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.3 s)' "
        "(ledgers/AC4/scripts/AC4-e-r12/out/run_graders.out). Direct copy run in /tmp/ac4-v/e12/work: QF_SEED=0, pytest -q --assert=plain -W error -> '402 passed'."),
    row("proj-collect-count", "The page's grading-mode count equals the real collect-only count on every seed",
        P + "project.html line 265 (Grading mode); " + T,
        "Line 265 reads '402 checks'. pytest --collect-only -q over QF_SEED=0..49 with the reference copied in: every one of the 50 seeds prints '402 tests collected' (the uniq count split only on the timing suffix)."),
    row("proj-autograder-alternatives", "Correct alternative implementations pass; each one that fails violates a sentence of the page",
        T + "; ledgers/AC4/scripts/AC4-e-r12/alt_r12_a..e (5 new alternatives, 50 of 50 seeds PASS); earlier alternatives re-run (ledgers/AC4/scripts/AC4-e-r12/out/oldalts.out)",
        "Five new spec-correct alternatives (Decimal half-up; Fraction floor with strip-only emptiness; total from the actual-minus-budget identity; loop totals; comparison rounding) each PASS 50/50 seeds (out/alts.out). Earlier alternatives re-run on 50 seeds: r9 alt_e passes 50/50. The others fail only on tests whose rule is stated on the page (distinct failing functions on seed 0, re-run round 12): alt_a, alt_b, alt_i, alt_j fail test_case_that_is_a_read_only_mapping_is_accepted (they refuse a non-dict Mapping; page line 252 'a mapping', line 263 'a case that is not a mapping'); alt_c, alt_k and alt_l fail test_products_that_are_not_a_list_raise_value_error (they accept a tuple of products; page line 263 'products are not a list of mappings'); alt_f fails both of the first two; alt_h fails test_products_that_are_not_a_list_raise_value_error (tuple) and test_product_that_is_not_a_mapping_raises_value_error (it raises TypeError for a product that is 5 or None; page line 263 names ValueError). None of these is a spec-correct implementation, so none is an over-constraint."),
    row("proj-alt-l-extra-keys", "A case or product with extra keys is accepted",
        "ledgers/AC4/scripts/AC4-e-r12/out/oldalts.out (AC4-e-r10_alt_l); " + T,
        "Re-run round 12: alt_l's failures on seed 0 are only test_products_that_are_not_a_list_raise_value_error[tuple-*] (a tuple of products, which page line 263 says must raise). No failing test concerns extra keys; the extra-keys behaviour passes."),
    row("proj-autograder-alt-decimal", "A decimal-based alternative passes the suite",
        "ledgers/AC4/scripts/AC4-e-r12/alt_r12_a_decimal_half_up.py; " + T,
        "Re-run round 12: alt_r12_a_decimal_half_up (Decimal ROUND_HALF_UP for the flexed amounts) PASS 50/50 seeds (out/alts.out). The earlier decimal alternative alt_k fails only the tuple-products test, the same page-stated rule as above."),
    row("proj-autograder-rerun-mutants-m01-m37", "Every committed mutant is killed by the current grader",
        "ledgers/AC4/mutants (79 files: fx10_*, fx11_*, m01-m50, m52-m55, m56-m59, m61)",
        "Re-run round 12 with ledgers/AC4/scripts/AC4-e-r12/run_mutants.py on seeds 0, 1, 25 (out/mutants_all2.out): 79 KILLED, 0 SURVIVED. The one other mutant, m60, is moved out of the list (see proj-r12-mutant-m60-scope)."),
    row("proj-mutant-descriptions", "Every mutant in the list has a description that names the student error",
        "ledgers/AC4/mutants/ (first docstring line of each file)",
        "Each of the 79 files has a docstring; the descriptions in the fragment are taken from it (new round-12 mutants start 'Student error:'; the earlier mutants' descriptions are carried from round 11 and their docstrings are unchanged)."),
    row("proj-mutants-m01-m06", "Mutants m01-m06 are killed", "ledgers/AC4/mutants/ (m01-m06)",
        "Re-run round 12 (out/mutants_all2.out): all six KILLED on seeds 0, 1, 25."),
    row("proj-mutant-m07-empty-name", "Mutant m07 (empty product name accepted) is killed", "ledgers/AC4/mutants/m07_empty_name_accepted.py",
        "Re-run round 12: KILLED on seeds 0, 1, 25 (out/mutants_all2.out)."),
    row("proj-mutants-m08-m11", "Mutants m08-m11 are killed", "ledgers/AC4/mutants/ (m08-m11)",
        "Re-run round 12: all four KILLED on seeds 0, 1, 25."),
    row("proj-mutant-m12-duplicate-names", "Mutant m12 (duplicate names accepted) is killed", "ledgers/AC4/mutants/m12_duplicate_names_accepted_in_two_functions.py",
        "Re-run round 12: KILLED on seeds 0, 1, 25."),
    row("proj-mutants-m13-m20", "Mutants m13-m20 are killed", "ledgers/AC4/mutants/ (m13-m20)",
        "Re-run round 12: all eight KILLED on seeds 0, 1, 25."),
    row("proj-mutants-m15-m19", "Mutants m15-m19 are killed", "ledgers/AC4/mutants/ (m15-m19)",
        "Re-run round 12: all five KILLED on seeds 0, 1, 25."),
    row("proj-mutants-m21-m24", "Mutants m21-m24 are killed", "ledgers/AC4/mutants/ (m21-m24)",
        "Re-run round 12: all four KILLED on seeds 0, 1, 25."),
    row("proj-mutants-m21-m24-equivalence", "m21-m24 are not equivalent to the reference", "ledgers/AC4/mutants/ (m21-m24)",
        "Each of m21-m24 is KILLED on seeds 0, 1, 25 (out/mutants_all2.out), so none is equivalent to the reference on the suite."),
    row("proj-mutants-m25-m29", "Mutants m25-m29 are killed", "ledgers/AC4/mutants/ (m25-m29)",
        "Re-run round 12: all five KILLED on seeds 0, 1, 25."),
    row("proj-mutants-r6-new", "Mutants m30-m34 are killed", "ledgers/AC4/mutants/ (m30-m34)",
        "Re-run round 12: all five KILLED on seeds 0, 1, 25."),
    row("proj-mutants-r7-new", "Mutants m35-m37 are killed", "ledgers/AC4/mutants/m35..m37",
        "Re-run round 12: all three KILLED on seeds 0, 1, 25."),
    row("proj-mutants-r8-new", "Mutants m38-m40 are killed", "ledgers/AC4/mutants/m38..m40",
        "Re-run round 12: all three KILLED on seeds 0, 1, 25."),
    row("proj-mutants-r9-new", "Mutants m41-m46 are killed", "ledgers/AC4/mutants/m41..m46",
        "Re-run round 12: all six KILLED on seeds 0, 1, 25."),
    row("proj-mutants-r10-new", "Mutants m47-m50 are killed", "ledgers/AC4/mutants/m47..m50",
        "Re-run round 12: all four KILLED on seeds 0, 1, 25."),
    row("proj-mutants-r11-m53-m55", "Mutants m53-m55 are killed", "ledgers/AC4/mutants/m53..m55",
        "Re-run round 12: m53 killed by test_flexed_at_actual_total_matches_oracle, m54 by test_product_with_no_budgeted_units, m55 by test_exact_half_cent_rounds_up (seed 0); all KILLED on seeds 0, 1, 25."),
    row("proj-r12-mutants-new-student-errors", "Six new student-error mutants written this round are killed",
        "ledgers/AC4/mutants/m56_sales_price_on_budget_units.py, m57_master_variable_on_actual_units.py, m58_zero_actual_units_means_budget_total.py, m59_actual_mix_at_actual_price.py, m61_actual_profit_at_standard_inputs.py (five in the list); m60 moved out",
        "Generated by ledgers/AC4/scripts/AC4-e-r12/make_mutants_r12.py as one-site substitutions in the reference (each asserted to match once). Killed on seeds 0, 1, 25: m56 by test_four_variances_and_total_match_oracle; m57 by test_master_variable_cost_by_product[Alpha]; m58 by test_flexed_zero_units_leaves_only_fixed_overhead; m59 by test_four_variances_and_total_match_oracle; m61 by test_four_variances_and_total_match_oracle (out/mutants_all2.out). Each is a plausible student error: sales price on budgeted units, master variable cost on actual units, zero actual units replaced by the budget total, actual mix priced at actual selling prices, actual profit charged at standard inputs."),
    row("proj-r12-mutant-m60-scope", "A mutant that refuses product names differing only in letter case survives; the page does not state whether names are compared case-sensitively",
        "ledgers/AC4/scripts/AC4-e-r12/out_of_scope/m60_case_name_pairs_refused.py; " + P + "project.html line 263 (Constraints); " + T,
        "Mutant survives the suite on seed 0 (out/mutants_all2.out: 'SURVIVED m60'). Page line 263 says a product name 'is empty or appears twice' and says nothing about letter case, so the refused behaviour violates no stated sentence: out of scope, PASS, and it is kept out of the mutants list (the brief's rule: an out-of-scope survivor is recorded with its reason as a PASS row and kept out of the mutants list). Suggested page wording, for the builder to decide: state that names are compared exactly, character for character."),
    row("proj-mutant-m52-dict-only-case", "Mutant m52 (a case must be a dict) is killed by the new read-only-mapping test",
        "ledgers/AC4/mutants/m52_case_must_be_a_dict.py; " + T + " (test_case_that_is_a_read_only_mapping_is_accepted); " + P + "project.html line 252 ('a mapping') and line 263",
        "Round 11 FAIL resolved. Re-run round 12: m52 KILLED on seeds 0, 1, 25 by test_case_that_is_a_read_only_mapping_is_accepted[master_budget]. The test feeds types.MappingProxyType(copy of the case) and requires the dict's results; page line 252 says the case is 'a mapping' and line 263 refuses only 'a case that is not a mapping', so the test is stated by the page and the reference accepts it (50/50 seeds)."),
    row("proj-spec-products-list-tuple", "The page's 'a list of mappings' is enforced for tuples as well as dicts and text",
        P + "project.html line 263 (Constraints) and line 252 ('a list of mappings'); " + P + "grader/reference.py line 64 (isinstance(raw, list)); " + T + " (test_products_that_are_not_a_list_raise_value_error with a tuple)",
        "Round 11 FAIL resolved. The reference now refuses a tuple (reference.py line 64: 'if not isinstance(raw, list) or not raw'), and the test adds a tuple case to the not-a-list family. Both page lines require a list. Re-run round 12: reference 50/50 seeds; fx11_tuple_products_accepted KILLED on seeds 0, 1, 25; the alternatives that accept tuples fail only this test (see proj-autograder-alternatives)."),
    row("proj-messages-no-leak", "Assertion messages do not print the expected value (module docstring claim)",
        T + " lines 344, 613 (messages now 'a half cent must round up, not down.' and 'a third of a cent must round down, not up.'); module docstring line 11",
        "Round 11 FAIL resolved. grep of every assertion and pytest.fail message: no message contains a number (the only digits in messages are in the names of tests and in the f-string field names). The run uses --assert=plain (page line 'pytest -q -p no:cacheprovider --assert=plain -W error'), so pytest does not print compared values. The one message that echoes a value, test line 800 (f'{CASE[field] + offset!r}'), echoes the test's own input, not an expected output."),
    row("proj-messages-bare-asserts", "Every assertion in the grader carries a message", T,
        "ast scan of test_project.py: every ast.Assert node has a msg (no bare asserts)."),
    row("proj-grader-comments", "Grader comments match the code they describe after the line shifts",
        T + " lines 44-45, 476-478, 487, 515, 593, 741, 790, 798, 821",
        "Line numbers moved by the round-12 additions (+1 after line 21, +2 after line 786, +36 after line 891); each comment text is unchanged. Re-read: line 487 margins 5400 and 8000 (9000 - 5*200 and 6000 - 3*200 as built); line 515 each budgeted margin 1000 (1400-400, 1600-600, 1800-800); line 593 budget revenue 3 over 9 units; lines 476-478 the equal-margin argument (AT*m is an integer, so the whole-cent and exact flexed profits agree); line 741 and 821 bool is an int; line 798 'as the page states' matches page line 263 (floats refused)."),
    row("proj-grader-equal-margin-comment", "The equal-margin branch comment matches the code", T + " lines 473-478 (branch at line 475)",
        "Round 11 locator 472-474 moved to 473-475; the function test_two_product_shift_to_lower_margin_is_unfavourable (lines 464-483) is byte-identical (ast comparison, round 12). Its branch 'if margins[0] == margins[1]' is at line 475 and the equal-margin comment at lines 476-478 is re-read above."),
    row("proj-equal-margin-branch", "The equal-margin branch test runs and passes on the reference", T + " lines 464-483 (test_two_product_shift_to_lower_margin_is_unfavourable)",
        "Function byte-identical since 91946cf (ast comparison); reference 402/402 on seed 0; re-run round 12 seed scan over seeds 0-49: no seed has equal first-two budgeted margins (empty list), so the branch is exercised only by its explicit cents."),
    row("proj-spec-clarity-and-errors", "Each condition on the Constraints line has a test that asserts ValueError",
        P + "project.html line 263 (Constraints); " + T,
        "Re-check round 12, condition by condition: not a mapping (test_case_that_is_not_a_mapping_raises_value_error, test_non_mapping_case_raises_value_error); products not a list of mappings (test_products_that_are_not_a_list_raise_value_error with dict, text and tuple; test_product_that_is_not_a_mapping_raises_value_error with list, number and None); a case without a required field (test_missing_case_field_raises_value_error); text, float and boolean numbers (test_case_number_given_as_text..., test_float_money..., test_boolean_input...); negative counts and amounts (test_negative_units_raise_value_error and the negative_* family); empty product list (test_empty_product_list_raises_value_error); name not text, empty or duplicate (test_product_name_that_is_not_text_raises_value_error with number, None and True; test_empty_product_name_raises_value_error; test_duplicate_product_names_raise_value_error); no budgeted units (test_zero_budgeted_units_raise_value_error); negative or non-integer unit argument (test_negative_actual_units_argument..., test_float_actual_units_argument..., test_actual_units_argument_that_is_not_a_number...). Each must_raise check fails with the condition name when no ValueError is raised. The round-11 gap (tuple) is now covered."),
    row("proj-spec-coverage-claims", "The coverage list on line 265 is backed by tests",
        P + "project.html line 265 (Grading mode); " + T,
        "Each item has a test: master budget by product and in total (test_master_units_by_product, test_master_revenue_by_product, test_master_totals_and_profit); flexed budget at actual and budgeted units (test_flexed_at_actual_total_matches_oracle, test_flexed_at_budgeted_total_reproduces_the_master_budget); the four variances and total (test_four_variances_and_total_match_oracle); reconciliation seeds 0-49 (test_every_grader_seed_reconciles_exactly, parametrize range(50)); zero-variance cases (test_all_variances_are_zero_when_actuals_equal_budget); single product (test_single_product_has_no_mix_variance); zero-unit case (test_flexed_zero_units_leaves_only_fixed_overhead); purity and silence (test_functions_do_not_change_their_arguments, test_functions_are_silent). Count 402 re-collected on seeds 0-49."),
    row("proj-spec-sign-both-directions", "Each of price, volume, mix and efficiency is tested in both directions",
        T + " lines 394-401 (price), 404-412 (price unfavourable), 415-420 and 423-429 (efficiency), 486-511 and 464-483 (mix), 560-566 and 569-575 (volume)",
        "Function bodies byte-identical since 91946cf (ast comparison); line numbers moved (+1 or +2). Price: test_price_variance_is_favourable_when_price_rises and test_price_variance_is_unfavourable_when_every_price_falls (its message text changed, the assert is unchanged). Volume: ..._favourable_when_more_units_are_sold, ..._unfavourable_when_fewer_units_are_sold. Mix: test_two_product_shift_to_higher_margin_is_favourable (lines 486-511) and test_two_product_shift_to_lower_margin_is_unfavourable (464-483). Efficiency: the positive and negative tests."),
    row("proj-spec-reconcile-seeds", "Reconciliation is tested on seeds 0 to 49", T + " lines 695-700",
        "test_every_grader_seed_reconciles_exactly parametrized over range(50); body byte-identical since 91946cf; 402 collected on every seed (see proj-collect-count)."),
    row("proj-spec-empty-name-claim", "Empty product name raises ValueError (page claim)",
        P + "project.html line 263 (Constraints); " + T + " (test_empty_product_name_raises_value_error, lines 768-775)",
        "Function byte-identical since 91946cf (ast comparison); the reference raises for an empty name (reference.py, the 'non-empty string' check); fx10_name_type_unchecked and m07 are KILLED on seeds 0, 1, 25."),
    row("proj-spec-fresh-objects-claim", "master_budget returns a fresh object each call (page claim)",
        P + "project.html line 263 (Constraints); " + T + " (test_master_returns_fresh_objects, lines 244-251)",
        "Function byte-identical since 91946cf (ast comparison); m27_master_returns_cached_object is KILLED on seeds 0, 1, 25."),
    row("proj-hours", "Declared project hours match the hub split and lesson hours",
        P + "project.html lines 277-285 (line 282 text changed this round); " + P + "index.html line 29 (data-hours-lessons=50, data-hours-project=20); lesson data-hours L01-L08",
        "Re-run round 12: lesson data-hours 6,7,6,6,7,6,6,6 sum to 50 (= hub data-hours-lessons 50); project table lines 277-285 hours 1+2+2+6+4+2+2+1 = 20 (= data-hours-project 20); 50 + 20 = 70 (hub eyebrow '70 hours'). Line 282 now names 'rubric criterion C3 (below)' and C3 level 3 indeed requires the input price assumption (page line 316 row C3, level 3 'states which costs vary ... and states the input price assumption'). Per-component pace not judged (architect ruling)."),
    row("proj-cards-structure", "cards.json is well formed: 131 cards, unique ids, lesson and grade values valid",
        P + "cards.json (131 cards; c130 and c131 new this round)",
        "Re-run: json loads; 131 objects; ids unique and in sequence AC4-c001..AC4-c131; lessons L01-L08; grade values T (50) and C (48); 33 cards carry no grade field (ids AC4-c001, c002, c003, c004, c015, c016, c017, c031, c032, c045, c046, c047, c059, c060, c061, c069-c074, c082-c086, c097-c099, c110, c111, c120, c121; their fronts are definitions or 'what is' prompts). check_pages (out/check_pages.out) allows an absent grade, and BUILDER_RULES section 7 attaches a grade to a graded result; no grade-less card states a numerical result in its back that the lesson does not prove."),
    row("proj-cards-duplicates", "No duplicate card fronts or backs", P + "cards.json",
        "Re-run: no duplicate front (case-insensitive) and no duplicate back among the 131 cards."),
    row("proj-banned-phrases", "No banned phrase in the changed text or the cards", P + "project.html; " + P + "cards.json",
        "Re-scan of the changed text (lines 146, 263, 265, 282 of project.html; c130 and c131 of cards.json) and of the whole cards file for roughly, about N, historically, typically, usually, generally, ellipses, TODO, TBD, lorem and 'it is well known': no banned hit. The page word 'rounded' is the ordinary word, not a banned hedge."),
    row("proj-lab-1", "Lab 1 runs and its output matches the page", P + "project.html lines 53-147; ledgers/AC4/scripts/AC4-e-r12/out/run_labs.out",
        "run_labs --unit AC4 -> 'run_labs AC4: PASS (10/10)' (includes lab-AC4-project-1). The lab block and its expected output are inside lines 53-145, byte-identical since 91946cf."),
    row("proj-lab-1-interpretation", "Interpretation of Lab 1 is backed by the printed output and the case", P + "project.html line 146 (interpretation, changed this round)",
        "Re-derived in round 12: master 8,600,000 - 1,000,000 - 5,000,000 = 2,600,000 (budget revenue 1000*5000 + 400*9000; variable 1000*3*200 + 400*5*200). Budgeted margin 7,600,000 over 1,400 units = 5,428.571..., shown as 5,428.57; 100 x 5,428.57 = 542,857 = the printed volume variance (exact 542,857.14). Flexed profit at 1,500 units: revenue round(1500*8.6M/1400) = 9,214,286 and variable round(1500*1M/1400) = 1,071,429, profit 3,142,857; exact 3,142,857 1/7 (step 6 line). Standard share 1000/1400 = 71.4%, 1200/1500 = 80.0%; margins 5000-600 = 4,400 and 9000-1000 = 8,000. Mix = (1200*4400 + 300*8000 - 5,000,000) - 3,142,857 = 2,680,000 - 3,142,857 = -462,857. Price 240,000 - 60,000 = 180,000; efficiency 200*(5,100 - 5,300) = -40,000 with 5,100 = 3*1200 + 5*300; total 2,820,000 - 2,600,000 = 220,000; the four add to 220,000."),
    row("proj-r12-lab1-derived-figures", "Derived figures added to the Lab 1 interpretation are right to the printed digits", P + "project.html line 146",
        "'the 100 extra units earn the budgeted average margin of 5,428.57 cents each (7,600,000 cents of budgeted margin over 1,400 units)': 7,600,000 / 1,400 = 5,428.57 to the cent, 100 units = 542,857 (printed). The statement 'the budgeted average margin' is the budget's margin per budgeted unit, which is what the flexed budget values the volume change at (page line 'at the budgeted mix')."),
    row("proj-lab-1-interpretation-second-clause", "The second clause of the Lab 1 interpretation (no input price effect computed) is true of the lab",
        P + "project.html line 146 (last sentence)",
        "The Lab 1 code computes no input price variance (variance names: price, volume, mix, efficiency; no input price term); the sentence 'the stretch section asks you to add one' matches project.html line 399 (stretch 'Two inputs' and line 398 'A spending variance')."),
    row("proj-lab-1-run-line146-untouched", "Lab 1 code and its printed output are unchanged", P + "project.html lines 53-145",
        "Carried from round 11 (" + P + "project.html lines 53-145 byte-identical since the previous pin 91946cf; the only changed lines in the page are 146, 265 and 282): round-11 evidence: " + r11["proj-lab-1-run-line146-untouched"]["evidence"]),
    row("proj-lab-2", "Lab 2 runs and its output matches the page", P + "project.html lines 149-243; tests/labs/AC4/lab-AC4-project-2.py",
        "run_labs --unit AC4 -> PASS (10/10), includes lab-AC4-project-2. Three blanks (efficiency, actual-mix margin, sales mix) at project.html lines 210, 214 and 216 (grep: 'efficiency = ___', 'actual_mix_margin = ___', 'mix = ___')."),
    row("proj-check-pages", "check_pages passes for AC4", P + "*.html and cards.json",
        "tools/check_pages.py --unit AC4 -> 'check_pages AC4: PASS'; --all -> rc 0 (out/check_pages.out)."),
    row("proj-check-dag", "check_dag passes for AC4", P,
        "tools/check_dag.py --unit AC4 -> 'check_dag AC4: PASS'; --all -> rc 0 (out/check_dag.out)."),
    row("proj-check-projects", "check_projects passes for AC4", P + "project.html",
        "tools/check_projects.py --unit AC4 -> 'check_projects AC4: PASS'; --all -> rc 0 (out/check_projects.out)."),
    row("proj-page-smoke", "page_smoke passes for the project page in Chromium", P + "project.html",
        "tools/page_smoke.py --unit AC4 --pages project.html -> 'page_smoke AC4: PASS', rc 0 (out/page_smoke_project.out). Timing failure not seen; no re-run needed."),
    row("proj-ruff-mypy", "ruff and mypy pass on the AC4 grader and labs and on the repository",
        P + "grader; tests/labs/AC4; repository mypy configuration",
        "ruff check . -> 'All checks passed!'; ruff format --check . -> '212 files already formatted'; mypy --no-incremental (repository, strict) -> 'Success: no issues found in 153 source files' (out/mypy_repo.out). The grader files are outside the repository mypy 'files' setting and were type-checked with mypy --strict --python-version 3.14 on the grader copy: 'Success: no issues found in 4 source files'."),
    row("proj-run-labs-ac4", "run_labs passes for every AC4 lab including the two project labs", "tests/labs/AC4",
        "run_labs --unit AC4 -> 'run_labs AC4: PASS (10/10)' (out/run_labs.out)."),
    row("proj-run-graders-ac4", "run_graders passes for AC4 on seeds 0-49, including the starter-fails check", P + "grader",
        "tools/run_graders.py --unit AC4 --seeds 0-49 -> 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.3 s)'; the starter fails the suite (the run does not report it passing)."),
    row("proj-instances", "make_instance is deterministic, labelled SIMULATED, and differs across seeds", P + "grader/instance.py",
        "run_graders check_instances passes (determinism, distinct instances); the suite test test_instance_is_deterministic_and_labelled passes on seeds 0-49 (run_graders)."),
    row("proj-alt-instance-coverage", "The instance family covers the cases the page names", P + "grader/instance.py; " + P + "grader/starter.py",
        "Carried from round 11 (" + P + "grader/instance.py and starter.py byte-identical since the previous pin 91946cf): round-11 evidence: " + r11["proj-alt-instance-coverage"]["evidence"] + " Round 12 re-run: run_graders PASS, starter fails the suite."),
    row("proj-alt-g-student-error", "Student-error alternative alt_g is rejected by the suite", "ledgers/AC4/scripts/AC4-e-r8/alt_g.py (run in /tmp/ac4-v/e12/fs/altg)",
        "Re-run round 12: alt_g fails the suite on seed 0 (test_case_that_is_not_a_mapping_raises_value_error[none-*], test_products_that_are_not_a_list_raise_value_error[mapping-*] and others). Its rejection is correct: it does not meet the page's stated ValueError rules."),
    row("proj-citations-reading", "Reading-list keys resolve in the registry", P + "project.html reading list; references/references.json",
        "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit AC4 (live) -> 'live re-verification of AC4: 2 of 560 entries, 0 problems' (out/verify_refs_*.out). references/references.json is unchanged since 91946cf (git diff)."),
    row("proj-r12-read-only-mapping-test", "The read-only-mapping test is required by the page wording",
        T + " test_case_that_is_a_read_only_mapping_is_accepted (new, lines 909-925); " + P + "project.html lines 252 and 263",
        "The page says the case is 'a mapping' (line 252) and refuses 'a case that is not a mapping' (line 263); types.MappingProxyType is a Mapping, so it must give the dict's results. Reference passes 50/50 seeds; dict-only alternatives (r9 alt_a, alt_b, alt_f, alt_i, alt_j) fail this test on seed 0 and refuse a valid mapping, which the page does not allow. No over-constraint."),
    row("proj-r12-none-and-bool-tests", "The new None and boolean refusals are stated on the page",
        T + " test_case_field_that_is_none_raises_value_error, test_product_field_that_is_none_raises_value_error, test_product_name_that_is_not_text (True added); " + P + "project.html line 263",
        "Page line 263: 'a value that is not a whole number (text, a float and a boolean are all refused)' and 'a product name that is not text'. None is not a whole number. The reference refuses all three (50/50 seeds). No over-constraint: the page sets these refusals."),
    row("proj-r12-product-not-mapping-valueerror", "A product that is not a mapping raises ValueError, as the page names",
        T + " test_product_that_is_not_a_mapping_raises_value_error (list, number, None); " + P + "project.html line 263",
        "Page line 263 names ValueError for 'products are not a list of mappings'. The alternative alt_h raises TypeError for a product that is 5 or None (it indexes 'name' in the product), and fails this test on seed 0: a wrong exception type under the page, not an over-constraint. The reference raises ValueError for all three."),
    row("proj-r12-float-units-test", "The float unit-count test uses a value the page refuses",
        T + " test_float_actual_units_argument_raises_value_error (wrong_type: Any = 100.0)",
        "Page line 263: 'a negative or non-integer actual unit count passed to flexible_budget' and the float refusal sentence. The annotation change does not alter the test's assertion."),
    row("proj-r12-alternatives-new", "Five new correct alternative implementations pass on every seed",
        "ledgers/AC4/scripts/AC4-e-r12/alt_r12_a..e and make_alts_r12.py; out/alts.out",
        "Decimal half-up (a), Fraction floor with whitespace-only emptiness (b), total from the actual-minus-budget identity (c), loop totals (d), comparison rounding (e): each PASS 50/50 seeds under -W error with --assert=plain. None fails, so no over-constraint in the suite (architect ruling (b))."),
    row("proj-r12-cards-c130", "Card AC4-c130 is checked against the lesson text it comes from",
        P + "cards.json (AC4-c130, object at line 921 of the current file); " + P + "L01.html lines 70-76 (Proposition 1.3(c))",
        "Front: total cost per unit TC(Q)/Q of a linear cost. Back: TC(Q)/Q = F/Q + v for Q > 0, fixed per unit plus variable per unit, Proposition 1.3(c). L01 line 71 states 'TC(Q)/Q = F/Q + v' and line 76 proves it: '(c) TC(Q)/Q = (F + vQ)/Q = F/Q + v'. Grade T (proved on the page). Every card number is in the lesson."),
    row("proj-r12-cards-c131", "Card AC4-c131 is checked against the lesson text it comes from",
        P + "cards.json (AC4-c131, object at line 928); " + P + "L03.html lines 335 (Example 3.1) and 339-340 (Remark 3.2)",
        "Back: 'Minus the line's contribution less its avoidable fixed cost (Remark 3.2). In Example 3.1 that is -(6,000 - 4,000) = -2,000. The plant-level fixed cost allocated to the line is the same under both alternatives and has no place in the test.' Remark 3.2 says 'minus its contribution less its avoidable fixed cost ... -(6,000 - 4,000) = -2,000 ... The allocated plant-level cost is the same under both alternatives, so it has no place in the test.' Example 3.1 gives contribution 15,000 - 9,000 = 6,000 and avoidable fixed cost 4,000 (SIMULATED figures). The derivation is the identity change = -(contribution - avoidable fixed), read from Example 3.1's sentences; grade T is the proved-on-the-page grade."),
    row("proj-r12-count-matches-page", "The count on the page equals the collected count for every seed", P + "project.html line 265; " + T,
        "Re-verified in proj-collect-count: 402 on all 50 seeds."),
    row("proj-rubric-exhaustive", "Rubric rows cover every criterion with four levels", P + "project.html lines 314-318 (rubric rows)",
        "Carried from round 11 (" + P + "project.html lines 306-318 byte-identical since the previous pin 91946cf): " + r11["proj-rubric-exhaustive"]["evidence"]),
]

# carried rows whose cited subject is byte-identical since 91946cf
CARRY_IDS = {
    "proj-rubric-scoring-rule": ("course/modules/AC/AC4/project.html", "project.html line 308 (Scoring rule)"),
    "proj-rubric-C4-observation": ("course/modules/AC/AC4/project.html", "project.html lines 306, 316, 373"),
    "proj-rubric-C2-terms": ("course/modules/AC/AC4/project.html", "project.html lines 308 and 315"),
    "proj-calib-A-scores": ("course/modules/AC/AC4/project.html", "project.html line 326; exemplar A memo lines 330-340"),
    "proj-calib-A-annotation": ("course/modules/AC/AC4/project.html", "project.html lines 343-351"),
    "proj-calib-B-scores": ("course/modules/AC/AC4/project.html", "project.html line 357; exemplar B Result line ~363"),
    "proj-calib-B-annotation": ("course/modules/AC/AC4/project.html", "project.html lines 377-382"),
    "proj-exemplar-B-consequences": ("course/modules/AC/AC4/project.html", "project.html line 370 (Assumptions)"),
    "proj-exemplar-B-threshold": ("course/modules/AC/AC4/project.html", "project.html line 373"),
    "proj-exemplar-B-verdict": ("course/modules/AC/AC4/project.html", "project.html line 359; exemplar B lines 362-375"),
    "proj-memo-structure-length": ("course/modules/AC/AC4/project.html", "project.html exemplar A memo-text (line 330 onward) and exemplar B memo-text (lines 361-373)"),
    "proj-exemplar-intro-universal-claim": ("course/modules/AC/AC4/project.html", "project.html line 324 (exemplars intro); line 370"),
    "proj-exemplar-overall-level": ("course/modules/AC/AC4/project.html", "project.html line 324 and article data-level at lines 327 and 357"),
    "proj-reading-list-sentence": ("course/modules/AC/AC4/project.html", "project.html line 267 (Reading list dd)"),
    "proj-ladder-lede": ("course/modules/AC/AC4/project.html", "project.html line 42; index.html lines 70 and 155"),
    "proj-simulated-and-data": ("course/modules/AC/AC4/project.html", "project.html lines 53-56 and 252 (Inputs); tests/labs/AC4/lab-AC4-project-1.py"),
    "proj-inputs-every-number-int": ("course/modules/AC/AC4/project.html", "project.html lines 252 and 260"),
    "proj-stretch-two-inputs-scope": ("course/modules/AC/AC4/project.html", "project.html line 399"),
    "proj-conventions-no-spending-claim": ("course/modules/AC/AC4/project.html", "project.html line 260 (Conventions) and line 398"),
    "proj-stretch-spending": ("course/modules/AC/AC4/project.html", "project.html line 398"),
    "proj-stretch-two-inputs": ("course/modules/AC/AC4/project.html", "project.html line 399"),
    "proj-stretch-list-intact": ("course/modules/AC/AC4/project.html", "project.html lines 396-401"),
    "proj-card-c020": ("course/modules/AC/AC4/cards.json", "cards.json lines 134-138 (AC4-c020); L02.html"),
    "proj-card-c078": ("course/modules/AC/AC4/cards.json", "cards.json lines 553-557 (AC4-c078); L06.html Proposition 2.1"),
    "proj-card-c091": ("course/modules/AC/AC4/cards.json", "cards.json line 641 (AC4-c091); L07.html"),
    "proj-card-c061": ("course/modules/AC/AC4/cards.json", "cards.json line 436 (AC4-c061); L05.html lines 58-59"),
    "proj-card-c126-basis": ("course/modules/AC/AC4/cards.json", "cards.json (AC4-c126 basis); L03.html lines 292-300"),
    "proj-card-c102": ("course/modules/AC/AC4/cards.json", "cards.json lines 718-721 (AC4-c102); L08.html line 306"),
    "proj-card-c129": ("course/modules/AC/AC4/cards.json", "cards.json line 914 (AC4-c129); L08.html line 128"),
    "proj-cards-sample": ("course/modules/AC/AC4/cards.json", "cards.json (c010, c020, c030, c040, c050, c060, c070, c080 ...)"),
    "proj-cards-r10-L01": ("course/modules/AC/AC4/cards.json", "cards.json AC4-c003, c012, c014, c120, c127, c128; L01.html lines 88, 119"),
    "proj-cards-r10-L02": ("course/modules/AC/AC4/cards.json", "cards.json AC4-c029, c125; L02.html lines 252-257, 264"),
    "proj-cards-r10-L03": ("course/modules/AC/AC4/cards.json", "cards.json AC4-c038, c040, c042, c043, c122, c123, c124; L03.html lines 90, 95, 334, 348-349, 389"),
    "proj-cards-r10-L04": ("course/modules/AC/AC4/cards.json", "cards.json AC4-c045, c121; L04.html line 55"),
    "proj-cards-changed-lessons-r10": ("course/modules/AC/AC4/cards.json", "cards.json AC4-c059..c068; L05/L06 ids unchanged"),
    "proj-cards-targeted": ("course/modules/AC/AC4/cards.json", "cards.json (c062, c063, c064, c066, c067, c075, c076)"),
    "proj-cards-number-format": ("course/modules/AC/AC4/cards.json", "cards.json (c101, c102, c109)"),
    "proj-cards-changed-lessons": ("course/modules/AC/AC4/cards.json", "cards.json cards from L05 and L06; L05.html; L06.html"),
    "proj-spec-coverage-claims-unused": None,
    "proj-purity-order-dependence": ("course/modules/AC/AC4/grader/test_project.py", "test_project.py lines 992-1032 (purity section)"),
    "proj-mutants-r9-carry": None,
    "proj-lab-1-run-line146-untouched-unused": None,
}
for rid, spec in CARRY_IDS.items():
    if spec is None or rid not in r11:
        continue
    files, loc = spec
    rows.append(carry(rid, files, location=loc))

# hub and lesson rows that are carried whole are listed above; every other round-11 row id must be carried or re-verified
rows_by_id = {r["id"]: r for r in rows}
missing = [rid for rid in r11 if rid not in rows_by_id]
print("round-11 ids not yet written:", missing, file=sys.stderr)

FRAG = {
    "unit": "AC4",
    "slice": "AC4-e",
    "round": 12,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 12, slice AC4-e; did not build AC4)",
    "pin": "aebdc15",
    "base": "91946cf (round-11 pin; previous fragment /tmp/fanout-frags/AC4-e.round11.json used as context only)",
    "checkout": str(ROOT),
    "scratch": "/tmp/ac4-v/e12",
    "verified_at": "2026-10-28T20:00:00+00:00",
    "rows": rows,
    "mutants": mutants,
}
json.dump(FRAG, sys.stdout, indent=1, ensure_ascii=False)
