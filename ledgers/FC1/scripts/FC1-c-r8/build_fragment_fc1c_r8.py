"""Round-8 verifier (FC1-c): build the fragment from the recorded outputs in out/ (no edits to course files)."""
import ast, json, pathlib, re

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-FC1-c")
S = ROOT / "ledgers/FC1/scripts/FC1-c-r8"
OUT = S / "out"
MUT = ROOT / "ledgers/FC1/mutants"

# ---- mutants: parse the final tool run -------------------------------------------------------
mutants = []
killed_count = survived = 0
for line in (OUT / "mutate_graders_0_19_r8_final.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+)\.py: (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    description = ast.get_docstring(ast.parse((MUT / f"{name}.py").read_text(encoding="utf-8"))) or desc
    first = description.splitlines()[0]
    if status == "SURVIVED":
        survived += 1
        killed = "SURVIVED on seeds 0-19 (no test fails)"
    else:
        killed_count += 1
    mutants.append({"id": name, "description": first, "killed_by": killed})
assert len(mutants) == 120, len(mutants)

def fix_row(_id, check, location, status, evidence, fix=None):
    row = {"id": _id, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        row["fix"] = fix
    return row

P = "PASS"
F = "FAIL"
FIX_MUT = ("Add the three accepted-input tests in ledgers/FC1/scripts/FC1-c-r8/proposed_fix_test_project_r8.py "
           "(yield 200000 bps; 5001 periods; settlement in period 5001) to grader/test_project.py before the "
           "wrapper loop, and change project.html line 171 from '79 checks' to '82 checks' with the three new "
           "cases named. Verified in a scratch copy only (not applied): 82 collected, reference 82/82, all 15 "
           "alternatives pass seeds 0-19 (out/alternatives_fixed_suite_r8.out), each survivor killed.")

rows = [
 fix_row("proj-check-projects","2.6-structure","course/modules/FC/FC1/project.html",P,
   "tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS', exit 0 (out/check_projects.out)."),
 fix_row("proj-check-pages","2.9-structure","course/modules/FC/FC1/project.html",P,
   "tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', exit 0 (out/check_pages.out)."),
 fix_row("proj-check-dag","2.9-dag","project.html; curriculum/curriculum.json concepts",P,
   "tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS', exit 0 (out/check_dag.out)."),
 fix_row("proj-run-labs","2.5-labs","project.html Labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py",P,
   "tools/run_labs.py --unit FC1 --page project -> 'run_labs FC1: PASS (3/3)'; --unit FC1 -> 'PASS (8/8)' (out/run_labs_project.out, out/run_labs_fc1.out)."),
 fix_row("proj-page-smoke","2.9-smoke","course/modules/FC/FC1/project.html",P,
   "tools/page_smoke.py --unit FC1 --pages project -> 'page_smoke modules/FC/FC1/project.html: PASS', exit 0; in-browser grader 'All 79 tests pass on seed 273923516' (out/page_smoke_project.out)."),
 fix_row("proj-run-graders","2.6-autograde-reference","grader/reference.py, test_project.py, instance.py, starter.py",P,
   "tools/run_graders.py --unit FC1 --seeds 0-49 -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.2 s)' (out/run_graders_0_49.out)."),
 fix_row("proj-lint-types","2.6-lint","course/modules/FC/FC1/grader/*.py; tests/labs/FC1/",P,
   "ruff check . -> 'All checks passed!' (out/ruff_check.out); ruff format --check on FC1 pages, labs and ledgers -> '12 files already formatted' (out/ruff_format_fc1.out); mypy --no-incremental -> 'Success: no issues found in 385 source files' (out/mypy.out)."),
 fix_row("proj-lab1-numbers","2.2-numbers","project.html lines 58, 97-100 (Lab 1)",P,
   "Exact Fractions (out/numbers_r8.out): present value 102775.09103322713 cents -> price 102775; page line 58 prints 102775.091033; labs_r8.out: Lab 1 expected block equals twin output."),
 fix_row("proj-lab2-blanks","2.5-labs","project.html lines 133, 140 (Lab 2)",P,
   "out/labs_r8.out: page code differs from tests/labs/FC1/lab-FC1-project-2.py at exactly two lines, the exponent '___' (vs period) and the trade '___' (vs -side * quantity * price_cents); twin exit 0 under -I -W error; expected equals output."),
 fix_row("proj-lab3-fixture-values","2.2-numbers","project.html lines 198-275 (Lab 3)",P,
   "out/numbers_r8.out recomputes each printed value: A 10000; B 11053 (210000/19 = 11052.6316); C [(1,5001),(2,15002)]; D [(1,2)]; rounding case events [(1,500),(2,500),(3,10500)], price 10278 once and 10277 term by term; E (2,-98500); F [(1,1)] price 1; G [(1,10001)] price 5001. out/labs_r8.out: page code equals twin (0 differing lines) and expected equals output."),
 fix_row("proj-rounding-fixture-terms","2.2-numbers","project.html line 193; grader/test_project.py lines 396-403",P,
   "out/numbers_r8.out: exact 10277.509103322713 rounds once to 10278; terms 480.769231, 462.278107, 9334.461766 round one by one to 481+462+9334 = 10277."),
 fix_row("proj-lab3-claim-using-functions","2.5-labs","project.html line 198 vs tests/labs/FC1/lab-FC1-project-3.py",P,
   "out/labs_r8.out: Lab 3 page code equals its twin (0 differing lines); the twin defines bond_events, bond_price, term_by_term_price with Fraction and the trade as an int product, as the hypothesis states."),
 fix_row("proj-expected-equals-output","2.5-labs","project.html expected blocks lines 97-100, 145-148, 263-275",P,
   "out/labs_r8.out: 'expected block == twin output: True' for all three labs; out/run_labs_project.out PASS (3/3)."),
 fix_row("proj-hours-arithmetic","2.9-hours","project.html table#hours lines 286-293; data-hours-project line 34",P,
   "1+2+5+4+2+3+3 = 20 = data-hours-project=20 (line 34); index.html data-hours-lessons=50 (five lessons of ten hours, index lines 137-143), so 70 = curriculum/02-economics-finance-core.yaml line 366 hours: 70."),
 fix_row("proj-hours-rationale-rows","2.9-hours","project.html table#hours lines 286-293",P,
   "All seven component rows and the total carry a rationale cell (read in full)."),
 fix_row("proj-hours-verifier-estimate","2.6-hours","project.html table#hours lines 286-293",P,
   "Architect ruling: hours are design targets; only arithmetic inconsistencies fail, and none is found (proj-hours-arithmetic). Not re-estimated."),
 fix_row("proj-ladder","2.6-ladder","project.html lines 41-50, 52-151 (rungs 1-2), 153-172 (rung 3), 312-319 (rung 4)",P,
   "Rung 1 is the annotated worked example (Lab 1); rung 2 is a completion problem with two blanks (Lab 2); rung 3 is the specification with the autograder; rung 4 is not graded (line 314)."),
 fix_row("proj-spec-interface","2.6-spec","project.html line 161; grader/starter.py",P,
   "starter.py lines 16-40 match line 161: Bond(face_cents, coupon_bps, periods).events(); bond_price_cents(bond, yield_bps); CashTrade(quantity, price_cents, side, settlement_day).events()."),
 fix_row("proj-named-conditions","2.6-spec","project.html lines 163-167; grader/test_project.py",P,
   "All eight named conditions are tested on both sides: periods 0 and -1 refused (215-222) / 1 accepted (225); face 0, -1 refused (232-239) / 1 accepted (242); coupon -1 refused (258) / 0 accepted (263); yield -10000, -20000 refused (499-506) / -9999 accepted (509); quantity 0, -1 refused (559-566) / 1 accepted (569); price -1 refused (608) / 0 accepted (613); side 0, 2, -2, 3, -3 refused (621-643) / +1, -1 accepted (646); settlement 0, -1 refused (654-661) / 1 accepted (664)."),
 fix_row("proj-test-count","2.6-spec","project.html line 171; grader/test_project.py",P,
   "Page says '79 checks'; pytest --collect-only -q on grader/test_project.py with instruments.py present: '79 tests collected' (out/collect_only_r8.out); page_smoke: 'All 79 tests pass'."),
 fix_row("proj-starter-fails","2.6-autograde","grader/starter.py",P,
   "out/starter_run_r8.out: '77 failed, 2 passed'. The two passing tests accept any exception by design (test_non_whole_face_is_refused_or_gives_ints, test_bool_periods_is_not_quietly_accepted_as_a_number, test_project.py lines 750-767); both are named in out/starter_failed_messages_r8.out."),
 fix_row("proj-instances","2.6-autograde","grader/instance.py, seeds 0-19",P,
   "out/instance_seeds_r8.out: 20 of 20 distinct (price, trade) pairs; every case valid (ranges checked); labelled SIMULATED (instance.py line 3 and line 31)."),
 fix_row("proj-silence-purity","2.6-autograde","grader/test_project.py test_the_module_prints_nothing, test_refused_inputs_print_nothing_before_they_raise (lines 693-734)",P,
   "out/pytest_ref_seed_r8.out: '79 passed' with the documented flags on the reference; both tests pass; the page states the rule (line 163)."),
 fix_row("proj-same-suite-pyodide-pytest","2.6-autograde","grader/test_project.py",P,
   "Local pytest with the documented flags, QF_SEED=273923516: '79 passed' on the reference (out/pytest_ref_seed_r8.out); page_smoke in-browser grader 'All 79 tests pass' (out/page_smoke_project.out)."),
 fix_row("proj-mutants-all","2.6-mutation","ledgers/FC1/mutants/*.py (120 files)",F,
   "tools/mutate_graders.py --unit FC1 --seeds 0-19 -> 'mutate_graders FC1: FAIL (117/120 killed)' (out/mutate_graders_0_19_r8_final.out). Survivors: r8c_yield_refused_above_one_thousand_percent, r8c_settlement_day_refused_above_five_thousand, r8c_periods_refused_above_five_thousand (rows proj-mutant-yield-1000-survivor, proj-mutant-settlement-5000-survivor, proj-mutant-periods-5000-survivor).",
   FIX_MUT),
 fix_row("proj-mutants-v1c-new","2.6-mutation","ledgers/FC1/mutants/v1c_*.py",P,
   "Killed in out/mutate_graders_0_19_r8_final.out: v1c_price_discounted_at_coupon_rate, v1c_seller_side_refused, v1c_simple_discount_not_compound, v1c_trade_rounded_to_dollars, v1c_yield_guard_missing (each KILLED)."),
 fix_row("proj-mutants-v2c-new","2.6-mutation","ledgers/FC1/mutants/r2c_*.py",P,
   "Killed in out/mutate_graders_0_19_r8_final.out: r2c_bond_periods_capped_at_twelve, r2c_events_change_on_second_call, r2c_price_cached_on_first_yield, r2c_trade_settles_one_period_early."),
 fix_row("proj-mutants-r3c-killed","2.6-mutation","ledgers/FC1/mutants/r3c_*.py",P,
   "Killed in out/mutate_graders_0_19_r8_final.out: all five r3c_* mutants (discount_factor_float_times_amount, events_cached_by_face, price_ten_digits_integral_rounding, price_ten_significant_digits, schedule_stops_at_twenty_periods)."),
 fix_row("proj-mutants-v4c-new","2.6-mutation","ledgers/FC1/mutants/v4c_*.py",P,
   "Killed in out/mutate_graders_0_19_r8_final.out: all five v4c_* mutants."),
 fix_row("proj-mutants-r4c-new","2.6-mutation","ledgers/FC1/mutants/r4c_*.py",P,
   "Killed in out/mutate_graders_0_19_r8_final.out: all five r4c_* mutants."),
 fix_row("proj-mutants-r5c-new","2.6-mutation","ledgers/FC1/mutants/r5c_*.py",P,
   "Killed in out/mutate_graders_0_19_r8_final.out: all four r5c_* mutants."),
 fix_row("proj-mutants-r6c-killed","2.6-mutation","ledgers/FC1/mutants/r6c_*.py",P,
   "Killed in out/mutate_graders_0_19_r8_final.out: all eight r6c_* mutants."),
 fix_row("proj-mutants-r7c-new","2.6-mutation","ledgers/FC1/mutants/r7c_*.py",P,
   "Re-run in out/mutate_graders_0_19_r8_final.out: all five r7c_* mutants KILLED, including r7c_periods_refused_above_one_thousand (killed by test_bond_schedule_of_one_thousand_and_one_periods_is_accepted, seed 0)."),
 fix_row("proj-mutant-schedule-cap-thirty-survivor","2.6-mutation","grader/test_project.py line 318 (40-period test)",P,
   "r4c_schedule_stops_at_thirty_periods KILLED by test_bond_schedule_of_forty_periods_is_complete_and_discounted_by_its_own_period (seed 0) (out/mutate_graders_0_19_r8_final.out)."),
 fix_row("proj-mutant-exponent-cap-thirty-survivor","2.6-mutation","grader/test_project.py line 318",P,
   "r4c_discount_exponent_capped_at_thirty KILLED by the 40-period test (seed 0)."),
 fix_row("proj-mutant-schedule-cap-survivor","2.6-mutation","grader/test_project.py line 304 (24-period test)",P,
   "r3c_schedule_stops_at_twenty_periods KILLED by test_bond_schedule_longer_than_twenty_periods_is_complete (seed 0)."),
 fix_row("proj-mutant-price-digits-survivor","2.6-mutation","grader/test_project.py line 434",P,
   "r3c_price_ten_significant_digits and r3c_price_ten_digits_integral_rounding KILLED by test_bond_price_exact_half_above_ten_significant_digits_is_exact (seed 0)."),
 fix_row("proj-mutant-price-cache-survivor","2.6-mutation","grader/test_project.py line 483",P,
   "r2c_price_cached_on_first_yield KILLED by test_one_bond_priced_at_two_yields_gives_each_yield_its_own_price (seed 0)."),
 fix_row("proj-mutant-price-epsilon-survivor","2.6-mutation","grader/test_project.py line 459",P,
   "r5c_price_rounded_with_epsilon KILLED by test_bond_price_just_under_a_half_cent_rounds_down (seed 0)."),
 fix_row("proj-mutant-yield-100-survivor","2.6-mutation","grader/test_project.py line 515",P,
   "r5c_yield_above_one_hundred_percent_refused KILLED by test_yield_above_one_hundred_percent_is_accepted (seed 0)."),
 fix_row("proj-mutant-schedule-cap-forty-survivor","2.6-mutation","grader/test_project.py line 791",P,
   "r6c_schedule_stops_at_forty_periods KILLED by the 100-period test (seed 0)."),
 fix_row("proj-mutant-exponent-cap-forty-survivor","2.6-mutation","grader/test_project.py line 791",P,
   "r6c_discount_exponent_capped_at_forty KILLED by the 100-period test (seed 0)."),
 fix_row("proj-mutant-yield-200-survivor","2.6-mutation","grader/test_project.py line 822",P,
   "r6c_yield_above_two_hundred_percent_refused KILLED by test_yield_of_three_hundred_percent_per_period_is_accepted (seed 0)."),
 fix_row("proj-mutant-settlement-cap-100-survivor","2.6-mutation","grader/test_project.py line 831",P,
   "r6c_settlement_day_above_one_hundred_refused KILLED by test_trade_settling_after_period_one_hundred_is_accepted (seed 0)."),
 fix_row("proj-mutant-decimal-40-digits-survivor","2.6-mutation","grader/test_project.py line 839",P,
   "r6c_price_decimal_forty_significant_digits KILLED by test_bond_price_exact_half_above_forty_significant_digits_is_exact (seed 0)."),
 fix_row("proj-mutant-decimal-28-digits-kill","2.6-mutation","grader/test_project.py line 839",P,
   "r6c_price_default_decimal_28_digits KILLED by test_bond_price_exact_half_above_forty_significant_digits_is_exact (seed 0)."),
 fix_row("proj-mutant-periods-cap-1000-survivor","2.6-mutation","grader/test_project.py line 806",P,
   "r7c_periods_refused_above_one_thousand KILLED by test_bond_schedule_of_one_thousand_and_one_periods_is_accepted (seed 0) (out/mutate_graders_0_19_r8_final.out). Round-7 FAIL re-verified from scratch."),
 fix_row("proj-mutant-r7c-coupon-half-even","2.6-mutation","grader/test_project.py line 189",P,
   "r7c_coupon_rounded_half_even KILLED by test_bond_half_cent_coupon_rounds_away_from_zero (seed 0)."),
 fix_row("proj-mutant-r7c-discount-float","2.6-mutation","grader/test_project.py line 423",P,
   "r7c_discount_factor_float_then_exact KILLED by test_bond_price_exact_half_cent_at_496_bps_is_exact_not_float (seed 0)."),
 fix_row("proj-mutant-r7c-price-cap-1m","2.6-mutation","grader/test_project.py line 347",P,
   "r7c_price_refused_above_one_million_cents KILLED by test_bond_price_is_an_int_in_cents (seed 0)."),
 fix_row("proj-mutant-r7c-hard-coded-answer","2.6-mutation","grader/test_project.py line 318",P,
   "r7c_price_is_seed_zero_answer_constant KILLED by the 40-period test (seed 0); the seed-zero price is 4281937 (out/instance_seeds_r8.out)."),
 fix_row("proj-alternatives","2.6-alternatives","ledgers/FC1/alternatives/a1..a5 (grader suite seeds 0-19)",P,
   "out/alternatives_0_19_r8.out: a1_list_comprehension_events, a2_generator_methods, a3_fraction_throughout, a4_integer_division_half_up, a5_frozen_dataclass_reduce: pass=20 fail=0 each."),
 fix_row("proj-alternatives-r4-new","2.6-alternatives","ledgers/FC1/scripts/FC1-c-r4/alt/alt6_r4_pow_fraction_floor.py",P,
   "out/alternatives_0_19_r8.out: pass=20 fail=0."),
 fix_row("proj-alternatives-r6-new","2.6-alternatives","ledgers/FC1/scripts/FC1-c-r6/alt/alt7..alt9",P,
   "out/alternatives_0_19_r8.out: alt7_r6_decimal_prec60_half_up, alt8_r6_integer_common_denominator, alt9_r6_running_discount_factor: pass=20 fail=0 each."),
 fix_row("proj-alternatives-r7-new","2.6-alternatives","ledgers/FC1/scripts/FC1-c-r7/alt/alt10..alt12",P,
   "out/alternatives_0_19_r8.out: alt10, alt11, alt12: pass=20 fail=0 each."),
 fix_row("proj-docstring-float-claim","2.2-numbers","grader/test_project.py lines 423-427, 451-452, 459-462",P,
   "out/numbers_r8.out: (1+0.04)**-1*13 = 12.499999999999998 (rounds to 12); Bond(1704285,179,1) at 496 bps exact 3305625/2 = 1652812.5 (rounds to 1652813); float 1652812.4999999998; 13/1.04 = 25/2 exact."),
 fix_row("proj-test-docstring-hand-numbers","2.2-numbers","grader/test_project.py docstrings",P,
   "out/numbers_r8.out re-derives every hand number in the docstrings: 10277.509103, 480.77/462.28/9334.46, 11052.6316, 30506.7015 (rounds 30507), 1734792, 10**13+0.4999, 2**40+1 times 9851 = 10831289045231227 > 2**53, 10**10+1 and 10**12+1 halves, 300075005 price just under half (= 1/2 - 1/(2*1000300030001)), 4200 and 2625. Decimal prec 10 drops the half of 5000000000.5 (out/numbers_r8.out)."),
 fix_row("proj-named-error-message-values","2.6-messages","grader/test_project.py lines 75-93",P,
   "must_raise and must_accept messages name the condition and carry no values; out/starter_failed_messages_r8.out."),
 fix_row("proj-failure-messages","2.6-messages","grader/test_project.py lines 693-734, 770-788",P,
   "out/starter_failed_messages_r8.out: each failure is the first docstring line plus 'The student module has no implementation for X'; no expected value is printed; assertions run under --assert=plain."),
 fix_row("proj-starter-message-leaks-answer","2.6-messages","grader/test_project.py line 822-828 (docstring of the 300% test)",P,
   "Round-7 leak (the printed value 2625 in the docstring first line) is removed: the first line now reads 'a yield of 30000 bps ... is not named as refused; the price is the discounted event' (no value). No failure message in out/starter_failed_messages_r8.out contains an expected value of the learner's seeded case."),
 fix_row("proj-starter-unwrapped-new-tests","2.6-messages","grader/test_project.py lines 849-852 (wrapper loop at file end)",P,
   "The wrapper loop now runs after the last test (lines 849-852). out/starter_failed_messages_r8.out lists all 79 tests, including test_bond_schedule_of_one_thousand_and_one_periods_is_accepted, with the 'no implementation' message; no traceback."),
 fix_row("proj-cards-scan-duplicates","2.6-cards","course/modules/FC/FC1/cards.json",P,
   "141 cards, ids and fronts and backs all unique (ledgers/FC1/scripts/FC1-c-r8/out/cards_mech_r8.out); only gap FC1-c134 (removed); 55 near-duplicate pairs by difflib (front ratio > 0.7 or back > 0.85) are distinct assumptions or questions (e.g. B1 vs B4, buy stop vs sell stop)."),
 fix_row("proj-cards-numbers-in-lessons","2.2-numbers","cards.json vs lessons_text/L01-L05 (checkout)",P,
   "out/cards_mech_r8.out: no card number missing from its lesson; hand check of the card numbers in out/cards_numbers_r8.out (0.20881062 -> 0.209; 181790 and 181818 cents; 686189; 1817.90; 216*10060 = 2172960; 2026-10-28 Wednesday, 2026-10-30 Friday)."),
 fix_row("proj-cards-numbered-references","2.6-cards","cards.json citations",P,
   "Every cited Definition, Proposition, Remark, Example, Corollary, Assumption and Problem label exists in its lesson (L01 P2, R2; L02 P3; L03 R1; L04 R2, R3; Assumptions A1-A3, B1-B4 in L03 'Assumptions B1 to B4'). out/cards_mech_r8.out flags only the wording 'misconception N' and 'Assumption A1' forms, which the lessons write as numbered misconception entries and 'A1 (...)'."),
 fix_row("proj-cards-sample","2.6-cards","cards.json (all 141 cards read in full)",P,
   "Every card read in full and checked against the current lesson text (lessons_text/L01-L05, regenerated this round) for its cited locator; no card contradicts its lesson. Cards checked in detail: L01 c001-c018, c091-c094, c103-c104, c110-c111, c122, c125-c126, c136; L02 c019-c034, c095-c096, c115-c116, c120, c127; L03 c035-c055, c097-c098, c105-c108, c112-c113, c117, c128-c131, c137-c140; L04 c056-c072, c099-c100, c119, c121, c132-c133, c135, c141; L05 c073-c090, c101-c102, c109, c114, c118, c123-c124, c142."),
 fix_row("proj-cards-changed-subjects","2.6-cards","cards.json diff 9373ef3..2d755599",P,
   "git diff 9373ef3 HEAD -- cards.json changed c008 (back), c039 (back), c043 (front and back), c060 (front and back), c066 (back), c069 (back), c083 (back), c118 (front and back); c139, c140, c141, c142 added; c134 removed. Each changed card re-verified against the current lesson text: L01 line 37 and Remark 3.2 (c008); L03 Definition 2.1 and Example 2.5 (c039, c043, c139, c140); L04 Remark 1.2 (c060, c141), Proposition 2.3 (c066), Lab 1 printed lines 251-252 (c069); L05 Lab 1 output line 275-276 and Definition 1.2 (c083, c118, c142; c142 confirmed by setting CLEARING_OFFSET to 3 -> offsets_nondecreasing False, to 2 -> True)."),
 fix_row("proj-cards-c014-lab-true","2.5-labs","cards.json FC1-c014",P,
   "L01 lab output line 177: 'the partial sums equal the closed form exactly for n = 0 to 10: True'."),
 fix_row("proj-cards-c122-equity-after-loss","2.6-cards","cards.json FC1-c122",P,
   "Proposition 4.1 (L01 line 68): equity after a loss is E - lambda, nonnegative iff lambda <= E; card carries Assumption 4.0 (lesson line 66)."),
 fix_row("proj-cards-citation-R3","2.6-cards","cards.json FC1-c067",P,
   "L04 'R3 · Why the traded term has a factor of two' exists (lesson line 318); card cites Remark 2.4 and Problem R3 accordingly."),
 fix_row("proj-cards-citation-R2","2.6-cards","cards.json FC1-c068",P,
   "L04 'R2 · What fails from a crossed start' (lesson lines 314-317): bid 1005, ask 1000, 5-share buy at 999 rests and leaves the book crossed; card matches."),
 fix_row("proj-cards-citation-scan","2.6-cards","cards.json citations (all cards)",P,
   "out/cards_mech_r8.out: no missing cited label beyond the wording forms explained under proj-cards-numbered-references."),
 fix_row("proj-cards-grades","2.6-cards","cards.json grade fields vs the lesson result tables (L01 264-269, L02 224-227, L03 269-274, L04 323-328, L05 357-363)",P,
   "Grades agree with the lesson tables: T for Propositions 2.2, 3.1, 3.5, 4.1 (L01), 1.4, 2.5 (L02), 2.3, Corollary 2.4, 3.2 (L03), 2.2, 2.3 (L04), 2.1(i), 2.1(ii), 2.2 (L05); C for the Lab 1 SIMULATED readouts (c052, c053, c054, c069, c082-c086, c088, c097-c098). T cards read off typed-in labs (c092, c093, c095, c096, c125) are accepted: each value is an exact computation on the page-shown lab code and follows from Propositions 2.2, 3.5 (D_t = d*kappa^t) or 4.1 (c092 checked: 181790 = round(1000*(1-0.45^11)/0.55*100))."),
 fix_row("proj-spec-scope-vs-curriculum","2.6-scope","project.html line 157; curriculum/02-economics-finance-core.yaml line 396-397",P,
   "project.html names FC2 as the 'Derivatives' unit; curriculum FC2 title 'Derivatives Fundamentals' (line 397)."),
 fix_row("proj-terminology-short-holder","2.6-terms","project.html line 54",P,
   "'holder' is defined at line 54 before its use in the Rung 2 and Rung 3 text."),
 fix_row("proj-prose-banned-phrases","2.9-prose","project.html, cards.json, L01-L05, grader/*.py",P,
   "grep for the BUILDER_RULES 1.3-1.4 banned strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, it is important to note, studies show, experts agree, obviously, clearly, roughly half, historically, ellipsis): no prose hit (only Python 'tuple[str, ...]' in L02 line 153 and L05 line 139)."),
 fix_row("proj-process-words","2.6-prose","project.html, cards.json, labs",P,
   "No process words in learner text (no verifier, round, builder, fragment). 'a reviewer reads it' (project.html lines 161, 163) is specification text, not process."),
 fix_row("proj-scope-words","2.6-prose","project.html lines 163, 171, 176-186",P,
   "Scope words checked: 'every' and 'all' in Money, Periods and Sides bullets are the spec rules, tested by the suite; 'exactly' in fixture A and B are computed (10500/1.05 = 10000; 210000/19); 'Each events() call returns the same list' is tested (test_repeated_events_calls_agree)."),
 fix_row("proj-terms-before-definition","2.6-prose","project.html lines 54-56, 161",P,
   "face, coupon, event, settlement period and per-period yield are defined in the rungs text (line 54) before the spec (line 161) uses instruments.py names; fixture terms match the grader's terms."),
 fix_row("proj-notation","2.6-notation","notation/notation.json; FC1 pages and cards",P,
   "notation.json holds 8 protected symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); none occurs in course/modules/FC/FC1 (grep this round). In-unit letters (C, R, E, P, X as cash, resting shares, equity, profit, shares traded) are defined per lesson and are not registry symbols."),
 fix_row("proj-footer-claim","2.6-prose","project.html line 341; course/assets/js/grader.js",P,
   "grader.js fetches only the grader files (line 18); drafts are kept by store.put in the browser (lines 33-79); page_smoke requires zero requests to other hosts. 'Nothing you write leaves it' holds for this page."),
 fix_row("proj-saved-as-you-type","2.6-prose","project.html line 301; course/assets/js/grader.js lines 33-79",P,
   "grader.js stores the editor text under the unit's draft key on every input (debounced 400 ms, line 61) and on reset (line 72, 79)."),
 fix_row("proj-references-reading-list","2.6-refs","project.html lines 321-328; references/references.json",P,
   "mishkin2021economics and harris2002trading are registry keys (references.json; checked this round); tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (out/verify_refs_offline.out). The page states no attribution to either source."),
 fix_row("proj-cited-year-conflicts","2.6-refs","project.html reading list (rendered from the registry)",P,
   "The page cites keys only and attributes no statement; registry year conflicts (harris2002trading 2002 vs curriculum '2003'; mishkin2021economics 2021 vs curriculum '13th ed. (2022)') are a registry and curriculum flag, recorded below, not a page FAIL. Live checks not run (offline)."),
 fix_row("proj-data-simulated","2.6-data","project.html lines 45, 55, 159; grader/instance.py; tests/labs/FC1",P,
   "No data file is read (project.html line 55); instance.py line 31 labels the case SIMULATED; the labs are SIMULATED or typed-in and say so; no market data is embedded."),
 fix_row("proj-lab3-autograder-coverage-note","2.5-labs","project.html line 276 (note after Lab 3)",P,
   "The note says which fixtures the autograder checks. Checked each named test: fixture A events (one-period tests) and price (one-period par test); fixture B price (negative-yield test); fixture C and D events (half-cent tests); fixture E events (buyer and seller tests); fixture F events (one-cent-face test) and price (exact-half test); fixture G price (exact-half test); rounding-fixture price (rounding test); fixture G events and rounding-case events are not checked as lists (confirmed: no test asserts those lists)."),
 fix_row("proj-page-grading-description","2.6-spec","project.html line 171; grader/test_project.py",P,
   "Line 171 names the 79 checks' coverage: 13-15, 24, 40, 100 and 1001-period bonds; both 2-case price tests; fixtures; rounding cases including Bond(10**40+1,0,1) and forty-one-digit price; yield at 150% and 300%; settlement 100 and 1000; silence and purity. Every named item is present in test_project.py (collect-only count 79)."),
 fix_row("proj-reference-deployment","2.9-deploy","BLUEPRINT.md line 401; grader/reference.py line 4; .github/workflows/ci.yml",F,
   "BLUEPRINT.md line 401: deployment 'excludes every grader/reference.py'. reference.py line 4: 'no file in this repository enforces that'. The repository has no deploy step: ci.yml has no publish step (only artifact upload of screenshots), and check_projects.py line 132 requires reference.py to exist next to the suite. The exclusion is unimplemented.",
   "Add the exclusion to the deployment step that publishes course/ (for example, exclude */grader/reference.py), or record the gap in the deployment docs. Repo-wide; outside the FC1 slice but unmet at this pin, unchanged from round 7."),
 fix_row("proj-ruff-repo-gate-note","2.6-lint","repository gate (ruff check .)",P,
   "ruff check . -> 'All checks passed!' (out/ruff_check.out)."),
 fix_row("proj-mutants-r8c-new","2.6-mutation","ledgers/FC1/mutants/r8c_*.py (four new student-error mutants written this round)",F,
   "Four new student-error mutants: r8c_yield_refused_above_one_thousand_percent, r8c_settlement_day_refused_above_five_thousand, r8c_periods_refused_above_five_thousand, r8c_face_refused_above_int64. The first three SURVIVE seeds 0-19 (out/mutate_graders_0_19_r8_final.out); r8c_face_refused_above_int64 is KILLED by test_bond_price_exact_half_above_forty_significant_digits_is_exact (seed 0).",
   FIX_MUT),
 fix_row("proj-mutant-yield-1000-survivor","2.6-mutation","grader/test_project.py lines 515-521 (yield test); project.html line 171",F,
   "r8c_yield_refused_above_one_thousand_percent (refuses yield_bps > 100000) survives seeds 0-19. project.html line 171 states: 'a yield above 100 % per period, which the page does not refuse (checked at 150 % and at 300 %)'. The suite checks 150% and 300% only.",
   FIX_MUT),
 fix_row("proj-mutant-settlement-5000-survivor","2.6-mutation","grader/test_project.py lines 831-836; project.html line 171",F,
   "r8c_settlement_day_refused_above_five_thousand (refuses settlement_day > 5000) survives seeds 0-19. project.html line 171 states: 'trades settling in periods 100 and 1000, which the page does not bound'.",
   FIX_MUT),
 fix_row("proj-mutant-periods-5000-survivor","2.6-mutation","grader/test_project.py lines 791-819; project.html lines 163-165",F,
   "r8c_periods_refused_above_five_thousand (refuses periods > 5000) survives seeds 0-19. project.html line 165 lists the only Bond refusal as 'periods less than 1', and line 163 says each named condition raises ValueError and any other refusal is not described; the same class of survivor as round 7's periods cap at 1000 (FAIL there).",
   FIX_MUT),
 fix_row("proj-mutant-face-int64-kill","2.6-mutation","grader/test_project.py line 839",P,
   "r8c_face_refused_above_int64 KILLED by test_bond_price_exact_half_above_forty_significant_digits_is_exact (seed 0)."),
 fix_row("proj-alternatives-r8-new","2.6-alternatives","ledgers/FC1/scripts/FC1-c-r8/alt/alt13..alt15",P,
   "Written this round: alt13_r8_floor_half_fraction (floor(|x|+1/2) with a reciprocal-ratio discount), alt14_r8_common_scale_integers (one integer fraction over (10000+yield)**last), alt15_r8_decimal_prec60_quantize (Decimal at 60 digits, ROUND_HALF_UP quantize). Each passes seeds 0-19 (out/alternatives_0_19_r8.out, alt15 line appended after the runner-name fix). No over-constraint found."),
 fix_row("proj-cards-c139-c142-new","2.6-cards","cards.json FC1-c139..c142",P,
   "c139 (-1000 = -1 * 100 * (10000 - 9990)), c140 (-600 = 400 - 1000 = C), c141 (Remark 1.2 check repetition), c142 (offsets_nondecreasing False iff clearing offset > settlement lag; verified by running the Lab 1 twin with CLEARING_OFFSET 3 and 2)."),
]

for row in rows:
    assert row["id"] and row["status"] in ("PASS", "FAIL")

# ---- assemble --------------------------------------------------------------------------------
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fail_n = sum(1 for r in rows if r["status"] == "FAIL")
fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 8 (did not build FC1)",
    "pin": "2d755599d8d74df292e3e43025f0458c4053802e",
    "base": "9373ef398589097500ea849e30ff9da423b98943 (round-7 pin of this slice)",
    "checkout": str(ROOT),
    "scratch": "/tmp/fc1c_r8/ (ref and starter copies of the grader), /tmp/fc1c_r8_fix/ (proposed-fix suite, not applied); ledgers/FC1/scripts/FC1-c-r8/proposed_fix_test_project_r8.py",
    "verified_at": "2026-11-04T20:30:55+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "harris2002trading: registry year 2002 (references/references.json); curriculum/02-economics-finance-core.yaml line 385 says 'Harris, Trading and Exchanges (2003)'. The project page cites the key only. For the curriculum owner.",
        "mishkin2021economics: registry year 2021; curriculum line 384 says '13th ed. (2022)'. Not checked online (offline only). The project page cites the key only. For the curriculum owner.",
    ],
    "freshness_flags": [],
    "notes": [
        "Round 8 on 2d75559 (round-7 pin 9373ef3). Delta read in full: project.html (4 lines: rung 2 link, line 171 count 79, the 1001-period list); grader/test_project.py (+1001-period test at 806, 300%-test docstring at 822, wrapper moved to the end at 849-852, docstrings reworded); cards.json (c008, c039, c043, c060, c066, c069, c083, c118 changed; c139-c142 added; c134 removed). Labs, reference.py, instance.py, starter.py and the alternatives a1-a5 are byte-identical to round 7 (git diff stat); all were re-run this round.",
        "Every previous non-PASS row was re-verified from scratch: proj-mutants-all, proj-mutants-r7c-new, proj-mutant-periods-cap-1000-survivor (now PASS), proj-starter-message-leaks-answer (now PASS), proj-starter-unwrapped-new-tests (now PASS), proj-reference-deployment (still FAIL). No row was carried; every row was re-run or re-read this round.",
        "Mutants: 120 files in ledgers/FC1/mutants (116 earlier plus four written this round). Run with tools/mutate_graders.py --unit FC1 --seeds 0-19: 117 killed, 3 survived (the three new r8c yield/settlement/periods caps). Four new student-error mutants were written this round, all with one-line docstrings; the face-cap mutant is killed.",
        "Alternatives: a1-a5 (ledgers/FC1/alternatives), alt6-alt12 (earlier rounds' scripts) and alt13-alt15 (written this round) each pass the suite on seeds 0-19 (out/alternatives_0_19_r8.out). Under the proposed fix (scratch only), all 15 still pass (out/alternatives_fixed_suite_r8.out).",
        "Proposed fix, not applied (verifier rule: report, do not fix): three accepted-input tests (yield 200000 bps; a 5001-period bond; settlement in period 5001) raise the suite to 82 tests. Reference 82/82; the three survivors are killed; the page count and the grading list would need updating from 79 to 82. The fix file is ledgers/FC1/scripts/FC1-c-r8/proposed_fix_test_project_r8.py.",
        "Labs: the twins run under python -I -W error; the page code equals each twin except Lab 2's two blanks; the expected blocks equal the twin outputs (out/labs_r8.out).",
        "Numbers: every number in project.html prose, the Lab 1-3 expected blocks, the grader docstrings and the cards was re-derived with exact Fractions (out/numbers_r8.out, out/cards_numbers_r8.out).",
        "Lessons L01-L05 were read as needed for the cards (text regenerated from the checkout in ledgers/FC1/scripts/FC1-c-r8/lessons_text/); the lessons are not in this slice and their prose was not audited beyond the statements the cards and project page cite.",
        "Could not check: the deployed site (no deploy config in this repository; BLUEPRINT's exclusion rule is unimplemented, proj-reference-deployment); live Crossref and publisher checks (offline only, no network); the full repository pytest suite (only -k FC1: 9 passed, out/pytest_fc1_r8.out; the grader directory is not collectible without instruments.py, expected); a Pyodide run of the proposed-fix tests (local pytest only); hours (architect ruling: design targets); a browser run of the four r8c mutants.",
        "The round-7 fragment at /Users/billyribeiro/.fanout/frags/D-FC1-c.round7.json was used as context only; none of its PASS rows was carried.",
        "The previous content of ledgers/FC1/FC1-c.json (tracked; a round-13 fragment from pin 762f636d) is replaced by this round-8 fragment, as the orchestration requested.",
    ],
    "summary": (f"Round 8 on 2d75559: {len(rows)} rows: {pass_n} PASS, {fail_n} FAIL, 0 UNVERIFIABLE. Verdict FAIL. "
                f"Mutants: 117/120 killed on seeds 0-19; survivors r8c_yield_refused_above_one_thousand_percent, "
                f"r8c_settlement_day_refused_above_five_thousand, r8c_periods_refused_above_five_thousand (the three "
                f"FAIL mutant rows, with the proposed fix in scratch). FAIL row proj-reference-deployment (repo-wide, "
                f"BLUEPRINT exclusion unimplemented). Alternatives: 15/15 pass seeds 0-19. Labs, page checks, DAG, "
                f"projects, page smoke, ruff, mypy, verify_refs and the reference run (50/50 seeds) all PASS."),
}

problems = None
import sys
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402
problems = ledger.validate(fragment, "FC1-c")
print("validate:", problems)
target = ROOT / "ledgers/FC1/FC1-c.json"
target.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", target, "rows", len(rows), "pass", pass_n, "fail", fail_n, "mutants", len(mutants))
