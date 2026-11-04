"""Round-6 verifier: writes the FC1-c round-6 ledger fragment from the outputs in out/ (mutants parsed from mutate_graders)."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
S = ROOT / "ledgers/FC1/scripts/FC1-c-r6"
OUT = S / "out"
MUT_LINE = re.compile(r"^(KILLED|SURVIVED) (\S+\.py): (.*?) -> (.*)$")
mutants = []
for line in (OUT / "mutate_graders_0_19_r6.out").read_text(encoding="utf-8").splitlines():
    m = MUT_LINE.match(line)
    if not m:
        continue
    status, name, description, tail = m.groups()
    killed_by = None
    if status == "KILLED":
        killed_by = re.match(r"(test_\w+)", tail).group(1) + " " + re.search(r"\(seed \d+\)", tail).group(0)
    mutants.append({"name": name, "description": description, "killed_by": killed_by})
assert len(mutants) == 111, len(mutants)
assert sum(1 for m in mutants if m["killed_by"]) == 106

E = "ledgers/FC1/scripts/FC1-c-r6/out/"
PRO = "ledgers/FC1/scripts/FC1-c-r6/proposed_grader_fix_r6.py"
FIX_SUITE = ("Add the four probe tests of " + PRO + " to course/modules/FC/FC1/grader/test_project.py (100-period bond at 400 bps; "
             "yield 30000 bps gives 2625; settlement_day 1000 accepted; Bond(10**40 + 1, 0, 1) at 10000 bps gives 5*10**39 + 1). "
             "With them the suite kills 111/111 mutants on seeds 0-19 (" + E + "proposed_fix_mutants_r6.out), passes the reference on seeds 0-49 "
             "and all nine alternatives (" + E + "proposed_fix_reference_r6.out), and collects 78 tests (" + E + "proposed_fix_collect_r6.out). "
             "Then change project.html line 171 from '74 checks' to '78 checks', and name the new probes in that sentence.")
rows = [
 dict(id="proj-check-projects", check="2.6-structure", location="course/modules/FC/FC1/project.html", status="PASS",
      evidence="tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS', exit 0 (" + E + "check_projects.out)."),
 dict(id="proj-check-pages", check="2.9-structure", location="course/modules/FC/FC1/project.html", status="PASS",
      evidence="tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', exit 0 (" + E + "check_pages.out)."),
 dict(id="proj-check-dag", check="2.9-DAG", location="project.html lines 58, 157, 178, 316", status="PASS",
      evidence="tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS' (" + E + "check_dag.out). Links: present-value (58, 178) and discount-factor (178), both M1 concepts in the closure. Futures, swaps, options (157) and the limit order book (316) are plain prose with no link, as the architect decision requires."),
 dict(id="proj-run-labs", check="2.5-labs", location="project.html Labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py; lesson twins", status="PASS",
      evidence="tools/run_labs.py --unit FC1 --page project -> 'run_labs FC1: PASS (3/3)'; --unit FC1 -> 'PASS (8/8)' (" + E + "run_labs_project.out, " + E + "run_labs_fc1.out). run_labs runs each twin as python -I -W error, page code equal to twin, expected block equal to output."),
 dict(id="proj-page-smoke", check="2.9-smoke", location="course/modules/FC/FC1/project.html", status="PASS",
      evidence="tools/page_smoke.py --unit FC1 --pages project -> 'page_smoke modules/FC/FC1/project.html: PASS', exit 0; in-browser 'All 74 tests pass on seed 705602400' (" + E + "page_smoke_project.out)."),
 dict(id="proj-run-graders", check="2.6-autograder-1", location="grader/reference.py, test_project.py, instance.py, starter.py", status="PASS",
      evidence="tools/run_graders.py --unit FC1 --seeds 0-49 -> 'run_graders FC1: PASS (reference 50/50 seeds)', exit 0 (" + E + "run_graders_0_49.out)."),
 dict(id="proj-lint-types", check="2.9-lint", location="course/modules/FC/FC1/grader/*.py, tests/labs/FC1/", status="PASS",
      evidence=".venv/bin/ruff check . -> 'All checks passed!' (" + E + "ruff_check.out); ruff format --check on course/modules/FC/FC1 and tests/labs/FC1 -> 12 files already formatted; mypy --no-incremental -> 'Success: no issues found in 331 source files' (" + E + "mypy.out). Out of slice, recorded in notes: the repo-wide 'ruff format --check .' reports ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py."),
 dict(id="proj-lab1-numbers", check="2.2-numbers", location="project.html lines 58, 97-100 (Lab 1)", status="PASS",
      evidence="Recomputed in exact Fractions by " + E + "nums_r6.py (" + E + "numbers_r6.out): coupon 5000; events [(1,5000),(2,5000),(3,105000)]; exact present value 102775.091033; price 102775; trade (2,-98500)."),
 dict(id="proj-lab2-blanks", check="2.5-labs", location="project.html lines 133, 140, 149 (Lab 2)", status="PASS",
      evidence="Blanks are the period exponent and -side*quantity*price (line 149); run_labs completion check PASS (" + E + "run_labs_project.out). Tolerance 1e-6*(1+|expected|) = 0.10 cent at 102775.09, matching the page's 'about 0.1 cent'."),
 dict(id="proj-lab3-fixture-values", check="2.2-numbers", location="project.html lines 198-276 (Lab 3)", status="PASS",
      evidence="Every printed fixture value recomputed (" + E + "numbers_r6.out): A 10000; B 11053 with exact 11052.6316; C [(1,5001),(2,15002)]; D [(1,2)]; rounding case 10278 once, 10277 term by term; E (2,-98500); F [(1,1)] price 1; G [(1,10001)] price 5001. run_labs matches each expected line."),
 dict(id="proj-rounding-fixture-terms", check="2.2-numbers", location="project.html line 193; grader/test_project.py lines 394-401", status="PASS",
      evidence="Exact present value 10277.509103 rounds once to 10278; terms 480.769231, 462.278107, 9334.461766 round to 481+462+9334=10277 (" + E + "numbers_r6.out). Test docstring (lines 395-397) states 10277.5091, 480.77, 462.28, 9334.46, which agree."),
 dict(id="proj-lab3-claim-using-functions", check="2.5-labs", location="project.html line 198 vs tests/labs/FC1/lab-FC1-project-3.py", status="PASS",
      evidence="The twin uses bond_events and bond_price (exact Fractions) and an int for the trade, as the hypothesis says; run_labs page-equals-twin PASS (" + E + "run_labs_project.out)."),
 dict(id="proj-expected-equals-output", check="2.5-labs", location="project.html expected blocks lines 97-100, 145-148, 263-275", status="PASS",
      evidence="run_labs compares each expected block with the twin's output under the page's rule (" + E + "run_labs_project.out: PASS (3/3))."),
 dict(id="proj-hours-arithmetic", check="2.9-hours", location="project.html table#hours lines 286-293; data-hours-project line 34; index.html lines 31, 39, 41", status="PASS",
      evidence="1+2+5+4+2+3+3 = 20 = data-hours-project = the hub's '20 h project' (index.html line 41); 50 h lessons + 20 h project = 70 h (index.html lines 31, 41); 20/70 = 28.57%, printed as 28.6% (index.html lines 39, 41)."),
 dict(id="proj-hours-rationale-rows", check="2.9-hours", location="project.html table#hours lines 286-293", status="PASS",
      evidence="All seven component rows and the total carry a rationale cell (read in full, project.html lines 286-293)."),
 dict(id="proj-hours-verifier-estimate", check="2.6-hours", location="project.html table#hours lines 286-293", status="PASS",
      evidence="Ruling: hours are design targets; only arithmetic inconsistencies fail. The arithmetic is checked in proj-hours-arithmetic. No failing estimate is asserted."),
 dict(id="proj-ladder", check="2.6-ladder", location="project.html lines 41-50 (ladder), 56-102, 104-150, 153-172, 312-319", status="PASS",
      evidence="Rung 1 is a fully solved annotated worked example (Lab 1); rung 2 is a completion problem with two blanks and an instant check; rung 3 is the specification (id spec, line 153) with the autograder (id grader-section, line 299); rung 4 is open-ended and ungraded (id stretch, line 312). Anchors resolve."),
 dict(id="proj-spec-interface", check="2.6-spec", location="project.html line 161; grader/starter.py lines 16-40", status="PASS",
      evidence="Names and signatures in starter.py match line 161: Bond(face_cents, coupon_bps, periods).events(); bond_price_cents(bond, yield_bps); CashTrade(quantity, price_cents, side, settlement_day).events()."),
 dict(id="proj-named-conditions", check="2.6-autograder-3", location="project.html lines 163-167; grader/test_project.py (8 conditions, both sides)", status="PASS",
      evidence="Each named condition is tested on both sides in test_project.py: periods<1 (0 refused, 1 accepted); face<=0 (0 and -1 refused, 1 accepted); coupon<0 (-1 refused, 0 accepted); yield<=-10000 (-10000 and -20000 refused, -9999 accepted); quantity<1 (0 and -1 refused, 1 accepted); price<0 (-1 refused, 0 accepted); side (0,2,-2,3,-3 refused; +1,-1 accepted); settlement<1 (0 and -1 refused, 1 accepted). must_raise is used only for these."),
 dict(id="proj-test-count", check="2.9-structure", location="project.html line 171 ('74 checks')", status="PASS",
      evidence="pytest --collect-only on the checkout's grader files with reference.py as instruments.py: 74 tests (" + E + "collect_only_r6.out), equal to the page."),
 dict(id="proj-starter-fails", check="2.6-autograder", location="grader/starter.py", status="PASS",
      evidence="Suite on starter.py: 72 failed, 2 passed (" + E + "starter_probe_r6.out). The two passing tests accept any exception by design (non-whole face; bool periods). Every failure is a named property message, no traceback (ran with -W error --assert=plain)."),
 dict(id="proj-instances", check="2.6-autograder-2", location="grader/instance.py, seeds 0-19", status="PASS",
      evidence="Scripted (" + E + "instance_and_float_r6.py, output " + E + "instance_and_float_r6.out): all 20 instances valid by their ranges; 20 distinct bond prices and 20 distinct trade amounts, so the answers change with the seed."),
 dict(id="proj-silence-purity", check="2.6-autograder", location="grader/test_project.py lines 688-729", status="PASS",
      evidence="test_the_module_prints_nothing (14 valid inputs) and test_refused_inputs_print_nothing_before_they_raise (8 refusals) pass on the reference (" + E + "run_graders_0_49.out) and on the proposed fix."),
 dict(id="proj-same-suite-pyodide-pytest", check="2.6-autograder-5", location="grader/test_project.py", status="PASS",
      evidence="Local pytest: 74 passed (" + E + "pytest_fc1_r6.out with -k FC1 gives 9 passed; the full file runs as 74 on the reference in " + E + "run_graders_0_49.out). In-browser 74 pass (" + E + "page_smoke_project.out)."),
 dict(id="proj-mutants-all", check="2.6-mutation", location="ledgers/FC1/mutants/*.py (111 files)", status="FAIL",
      evidence="tools/mutate_graders.py --unit FC1 --seeds 0-19 -> 'mutate_graders FC1: FAIL (106/111 killed)' (" + E + "mutate_graders_0_19_r6.out). Survivors: r6c_schedule_stops_at_forty_periods.py, r6c_discount_exponent_capped_at_forty.py, r6c_yield_above_two_hundred_percent_refused.py, r6c_settlement_day_above_one_hundred_refused.py, r6c_price_decimal_forty_significant_digits.py (rows below).",
      fix="Aggregate of the five rows below. " + FIX_SUITE),
 dict(id="proj-mutants-v1c-new", check="2.6-mutation", location="ledgers/FC1/mutants/v1c_*.py", status="PASS",
      evidence="Five v1c_ mutants, each KILLED in " + E + "mutate_graders_0_19_r6.out."),
 dict(id="proj-mutants-v2c-new", check="2.6-mutation", location="ledgers/FC1/mutants/r2c_*.py", status="PASS",
      evidence="Four r2c_ mutants, each KILLED in " + E + "mutate_graders_0_19_r6.out."),
 dict(id="proj-mutants-r3c-killed", check="2.6-mutation", location="ledgers/FC1/mutants/r3c_*.py", status="PASS",
      evidence="Five r3c_ mutants, each KILLED in " + E + "mutate_graders_0_19_r6.out."),
 dict(id="proj-mutants-v4c-new", check="2.6-mutation", location="ledgers/FC1/mutants/v4c_*.py", status="PASS",
      evidence="Five v4c_ mutants, each KILLED in " + E + "mutate_graders_0_19_r6.out."),
 dict(id="proj-mutants-r4c-new", check="2.6-mutation", location="ledgers/FC1/mutants/r4c_*.py", status="PASS",
      evidence="Five r4c_ mutants, each KILLED in " + E + "mutate_graders_0_19_r6.out."),
 dict(id="proj-mutants-r5c-new", check="2.6-mutation", location="ledgers/FC1/mutants/r5c_*.py", status="PASS",
      evidence="Four r5c_ mutants (round 5), each KILLED in " + E + "mutate_graders_0_19_r6.out, including r5c_price_rounded_with_epsilon.py and r5c_yield_above_one_hundred_percent_refused.py."),
 dict(id="proj-mutants-r6c-killed", check="2.6-mutation", location="ledgers/FC1/mutants/r6c_*.py (killed ones)", status="PASS",
      evidence="Written by this verifier (scripts/FC1-c-r6/make_r6c_mutants_verifier_r6.py and make_decimal_mutants_r6.py). KILLED in " + E + "mutate_graders_0_19_r6.out: r6c_coupon_cumulative_rounding.py (test_bond_coupon_is_face_times_coupon_rate_rounded_half_away, seed 0); r6c_quantity_above_two_thousand_refused.py (test_trade_cash_flow_is_exact_above_two_to_the_fifty_three); r6c_price_default_decimal_28_digits.py (see proj-mutant-decimal-28-digits-kill)."),
 dict(id="proj-mutant-schedule-cap-thirty-survivor", check="2.6-mutation", location="ledgers/FC1/mutants/r4c_schedule_stops_at_thirty_periods.py vs grader/test_project.py line 318", status="PASS",
      evidence="KILLED (" + E + "mutate_graders_0_19_r6.out) by the 40-period test."),
 dict(id="proj-mutant-exponent-cap-thirty-survivor", check="2.6-mutation", location="ledgers/FC1/mutants/r4c_discount_exponent_capped_at_thirty.py vs test_project.py line 318", status="PASS",
      evidence="KILLED (" + E + "mutate_graders_0_19_r6.out) by the 40-period test."),
 dict(id="proj-mutant-schedule-cap-survivor", check="2.6-mutation", location="ledgers/FC1/mutants/r3c_schedule_stops_at_twenty_periods.py vs test_project.py lines 304-315", status="PASS",
      evidence="KILLED (" + E + "mutate_graders_0_19_r6.out) by the 24-period test."),
 dict(id="proj-mutant-price-digits-survivor", check="2.6-mutation", location="ledgers/FC1/mutants/r3c_price_ten_digits_integral_rounding.py vs test_project.py lines 431-442", status="PASS",
      evidence="KILLED (" + E + "mutate_graders_0_19_r6.out) by the exact-half test above ten significant digits."),
 dict(id="proj-mutant-periods-13-15-survivor", check="2.6-mutation", location="grader/test_project.py lines 281-301", status="PASS",
      evidence="The 13-15 period test asserts events and price for 13, 14 and 15 periods; the mutants of that class listed in mutate_graders_0_19_r6.out are KILLED."),
 dict(id="proj-mutant-price-cache-survivor", check="2.6-mutation", location="grader/test_project.py lines 469-482; project.html lines 161, 178", status="PASS",
      evidence="ledgers/FC1/mutants/r2c_price_cached_on_first_yield.py is KILLED (" + E + "mutate_graders_0_19_r6.out)."),
 dict(id="proj-mutant-price-epsilon-survivor", check="2.6-mutation", location="ledgers/FC1/mutants/r5c_price_rounded_with_epsilon.py; test_project.py line 455", status="PASS",
      evidence="Round-5 FAIL re-verified: KILLED by test_bond_price_just_under_a_half_cent_rounds_down (seed 0) in " + E + "mutate_graders_0_19_r6.out. The round-5 fix is present in the checkout."),
 dict(id="proj-mutant-yield-100-survivor", check="2.6-mutation", location="ledgers/FC1/mutants/r5c_yield_above_one_hundred_percent_refused.py; test_project.py line 510", status="PASS",
      evidence="Round-5 FAIL re-verified: KILLED by test_yield_above_one_hundred_percent_is_accepted (seed 0). The page line 171 states that the page does not refuse a yield above 100 % per period, so the test is grounded in the page."),
 dict(id="proj-mutant-schedule-cap-forty-survivor", check="2.6-mutation", location="ledgers/FC1/mutants/r6c_schedule_stops_at_forty_periods.py vs grader/test_project.py lines 318-329", status="FAIL",
      evidence="Student error: Bond.events() stops at period 40. SURVIVED on seeds 0-19 (" + E + "mutate_graders_0_19_r6.out). The page states the behaviour for every bond: project.html line 177 'The bond's coupon is paid in each of periods 1 to periods, and its face in the last of them'; the test at test_project.py line 319 says 'names no upper limit on periods'. No test has more than 40 periods.",
      fix="Add a 100-period bond test: Bond(10_000, 500, 100).events() equals the oracle and bond_price_cents at 400 bps equals the oracle sum (proposed_grader_fix_r6.py, test_bond_schedule_of_one_hundred_periods_...). It kills this mutant on seeds 0-19. " + FIX_SUITE),
 dict(id="proj-mutant-exponent-cap-forty-survivor", check="2.6-mutation", location="ledgers/FC1/mutants/r6c_discount_exponent_capped_at_forty.py vs test_project.py lines 318-329", status="FAIL",
      evidence="Student error: the discount exponent is min(period, 40). SURVIVED on seeds 0-19 (" + E + "mutate_graders_0_19_r6.out). project.html line 178: 'An event in period t is discounted by (1+y)^-t'. No test discounts an event after period 40.",
      fix="The 100-period price test in proposed_grader_fix_r6.py kills it (events 41-100 discounted by their own period). " + FIX_SUITE),
 dict(id="proj-mutant-yield-200-survivor", check="2.6-mutation", location="ledgers/FC1/mutants/r6c_yield_above_two_hundred_percent_refused.py; test_project.py lines 510-516; project.html lines 166, 171", status="FAIL",
      evidence="Student error: bond_price_cents refuses yield_bps above 20000. SURVIVED on seeds 0-19 (" + E + "mutate_graders_0_19_r6.out). project.html line 166 names only yield_bps at or below -10000 as refused; line 171 says 'a yield above 100 % per period, which the page does not refuse'. The same reasoning holds for 200 %, which no test covers.",
      fix="Add: bond_price_cents(Bond(10_000, 500, 1), 30_000) == 2_625 (10500 / 4 exactly), per proposed_grader_fix_r6.py. " + FIX_SUITE),
 dict(id="proj-mutant-settlement-cap-100-survivor", check="2.6-mutation", location="ledgers/FC1/mutants/r6c_settlement_day_above_one_hundred_refused.py; test_project.py lines 667-674; project.html line 167", status="FAIL",
      evidence="Student error: CashTrade refuses settlement_day above 100. SURVIVED on seeds 0-19 (" + E + "mutate_graders_0_19_r6.out). project.html line 167 names only settlement_day less than 1 as refused. test_project.py line 668 says the page names no upper limit, yet the largest period tested is 100.",
      fix="Add: CashTrade(10, 9_850, 1, 1_000).events() == [(1_000, -98_500)], per proposed_grader_fix_r6.py. " + FIX_SUITE),
 dict(id="proj-mutant-decimal-40-digits-survivor", check="2.6-mutation", location="ledgers/FC1/mutants/r6c_price_decimal_forty_significant_digits.py; test_project.py lines 431-442; project.html lines 163, 176", status="FAIL",
      evidence="Student error: bond_price_cents sums in a Decimal context of 40 significant digits. SURVIVED on seeds 0-19 (" + E + "mutate_graders_0_19_r6.out). project.html line 163 says a coupon or price 'is computed from exact fractions and rounded once', and line 176 says 'the exact value ... is rounded once'. The largest exact-half test has 13 significant digits. A face of 10**40 + 1 cents is valid (no upper limit is named), and a finite-precision sum fails it.",
      fix="Add: bond_price_cents(Bond(10**40 + 1, 0, 1), 10_000) == 5 * 10**39 + 1, per proposed_grader_fix_r6.py. It kills the 40-digit mutant and the 28-digit mutant. Reference and alt7 (Decimal prec 60) still pass. " + FIX_SUITE),
 dict(id="proj-mutant-decimal-28-digits-kill", check="2.6-mutation", location="ledgers/FC1/mutants/r6c_price_default_decimal_28_digits.py", status="PASS",
      evidence="Student error: default Decimal context (28 digits). KILLED, but only accidentally: the first failure is test_yield_just_above_minus_one_is_accepted at seed 3 (" + E + "mutate_graders_0_19_r6.out), where the 28-digit quantize overflows. No exact-half test above 13 digits kills it on the current suite. The proposed fix kills it on a precision test (proposed_fix_mutants_r6.out)."),
 dict(id="proj-alternatives", check="2.6-alternatives", location="ledgers/FC1/alternatives/a1..a5 (scripts ledgers/FC1/scripts/FC1-c-r6/run_alts_r6.sh)", status="PASS",
      evidence="run_alts_r6.sh: a1 list comprehension, a2 generators, a3 Fraction throughout, a4 integer division half up, a5 frozen dataclass reduce each pass seeds 0-19 (" + E + "alternatives_0_19_r6.out). Plan item (5), a float implementation, is not a correct implementation under the page's exact-fraction rule (project.html line 163) and is not used; a5 stands in for the slot."),
 dict(id="proj-alternatives-r4-new", check="2.6-alternatives", location="ledgers/FC1/scripts/FC1-c-r4/alt/alt6_r4_pow_fraction_floor.py", status="PASS",
      evidence="alt6 passes seeds 0-19 (" + E + "alternatives_0_19_r6.out)."),
 dict(id="proj-alternatives-r6-new", check="2.6-alternatives", location="ledgers/FC1/scripts/FC1-c-r6/alt/alt7..alt9", status="PASS",
      evidence="Written by this verifier: alt7 Decimal at 60 digits with ROUND_HALF_UP, alt8 one integer ratio over (10000+yield)**T, alt9 running discount factor with floor(x+1/2). All pass seeds 0-19 (" + E + "alternatives_0_19_r6.out) and pass the proposed fix (" + E + "proposed_fix_reference_r6.out)."),
 dict(id="proj-docstring-float-claim", check="2.6-docstrings", location="grader/test_project.py lines 421-452", status="PASS",
      evidence="Scripted (" + E + "instance_and_float_r6.out): 13*(1+0.04)**-1 = 12.499999999999998 and 1734792*(1+0.0496)**-1 = 1652812.4999999998, as the docstrings say."),
 dict(id="proj-named-error-message-values", check="2.6-failure-messages", location="grader/test_project.py (every assert and pytest.fail site)", status="PASS",
      evidence="Under the documented flags (--assert=plain -W error) a failing run prints only the property message, no expected values (" + E + "leak_probe_r6.out, mutant r6c_coupon_cumulative_rounding.py, 8 failed)."),
 dict(id="proj-failure-messages", check="2.6-failure-messages", location="grader/test_project.py (every assert and pytest.fail site)", status="PASS",
      evidence="Each assert message names the property (for example 'the price is the sum of each event discounted by (1 + y) ** -t, rounded once'); starter run names every property (" + E + "starter_probe_r6.out)."),
 dict(id="proj-cards-scan-duplicates", check="2.7-cards", location="course/modules/FC/FC1/cards.json (138 cards)", status="PASS",
      evidence="138 ids, all unique; no repeated front or back text (cards_numbers_r6.out: duplicate fronts [], duplicate backs []). Near pairs read: c002/c136, c013/c122, c036/c138, c066/c100, c044/c045 state different facts."),
 dict(id="proj-cards-numbers-in-lessons", check="2.7-cards", location="course/modules/FC/FC1/cards.json; lessons L01-L05", status="PASS",
      evidence="cards_numbers_r6.py: 138 cards, 0 numbers in a card absent from its lesson (" + E + "cards_numbers_r6.out)."),
 dict(id="proj-cards-sample", check="2.7-cards", location="cards.json, all 138 cards against L01-L05", status="PASS",
      evidence="All 138 cards read against the stripped text of L01-L05 (scripts/FC1-c-r6/lessons_text/). Each card's lesson field matches the section that holds its result."),
 dict(id="proj-cards-changed-subjects", check="2.7-cards", location="cards.json c002, c013, c036, c055, c061, c066, c093, c094, c136, c137, c138", status="PASS",
      evidence="The changed and new cards of the 440ed3c..142ecfc delta were re-checked against the current lesson text: c002 (L01 Remark 1.2), c013 (Prop 4.1), c036 (Def 1.2), c055 (Prop 3.2, misconception 3), c061 (Example 1.3), c066 (Prop 2.3), c093 (Lab 1 Part D), c094 (Assumption 4.0), c136 (Remark 1.2), c137 and c138 (Def 1.2)."),
 dict(id="proj-cards-c014-lab-true", check="2.7-cards", location="cards.json FC1-c014 (L01)", status="PASS",
      evidence="Lab 1 Part A prints True (L01 lab output; run_labs PASS)."),
 dict(id="proj-cards-c122-equity-after-loss", check="2.7-cards", location="cards.json FC1-c122 (L01)", status="PASS",
      evidence="Proposition 4.1: equity after loss is nonnegative iff lambda <= E (L01 text)."),
 dict(id="proj-cards-citation-R3", check="2.7-cards", location="cards.json FC1-c054 (L03)", status="PASS",
      evidence="L03 Lab 1 Part C lists 121 pairs asks 100-110; the grid is stated as finite and not a proof of all asks (L03 Remark 3.3 and R3 text)."),
 dict(id="proj-cards-citation-R2", check="2.7-cards", location="cards.json FC1-c089 (L05)", status="PASS",
      evidence="L05 Proposition 2.1(ii) proof uses Pay_j >= 0; the counterexample with consideration c = -100 is worked in the L05 problem set (Let one trade have buyer A, seller B and consideration c = -100 cents)."),
 dict(id="proj-cards-citation-scan", check="2.7-cards", location="cards.json block references", status="PASS",
      evidence="Scripted scan of 154 'Proposition/Remark/Example/Definition/Assumption/Problem/Corollary' references in the card text: each appears in its lesson (only 'Assumption B1..B4, A3' written as ranges, which L03 states)."),
 dict(id="proj-cards-grades", check="2.7-cards", location="cards.json grade and basis fields", status="PASS",
      evidence="T cards are lesson-proved results or typed-in lab outputs graded T in the lesson's key-results table; C cards cite SIMULATED labs or hand readings with their basis (BLUEPRINT §3; BUILDER_RULES §7). No T card rests on a SIMULATED lab."),
 dict(id="proj-spec-scope-vs-curriculum", check="2.6-scope", location="project.html lines 157, 161; curriculum/02-economics-finance-core.yaml lines 388-395", status="PASS",
      evidence="Curriculum project brief: 'Futures, swaps and options follow in FC2.' Page lines 157 and 161 match: cash instruments only; FC2 named as the Derivatives unit (curriculum line 396-397)."),
 dict(id="proj-terminology-short-holder", check="2.9-prose", location="project.html lines 54, 179", status="PASS",
      evidence="'holder' is defined at its first use in line 54 and used consistently (lines 54, 159, 179)."),
 dict(id="proj-prose-banned-phrases", check="2.9-prose", location="course/modules/FC/FC1/project.html; cards.json; L01-L05; grader/*.py", status="PASS",
      evidence="grep (case-insensitive) for TODO, TBD, lorem, for brevity, omitted, beyond the scope, exercise, you can add more, important to note, studies show, experts agree, well known, obviously, clearly, can be shown, roughly, historically, and an ellipsis: 0 hits in prose. The one '...' in test_project.py line 376 is the repeating decimal 11052.63..., not an omission."),
 dict(id="proj-scope-words", check="2.9-prose", location="project.html lines 163, 171, 176, 180, 276; cards.json scope words", status="PASS",
      evidence="Every scope word read: 'every named condition', 'each events() call', 'no function prints or warns' are requirements that test_project.py checks on the listed inputs; the rest are computations shown on the page."),
 dict(id="proj-terms-before-definition", check="2.9-prose", location="project.html lines 38, 54, 58, 178", status="PASS",
      evidence="face, coupon, settlement period, event and holder are defined in line 54 before use; basis point in line 54; present value and discount factor are linked and defined in the M1 closure."),
 dict(id="proj-notation", check="2.4-notation", location="project.html lines 58, 106, 178; notation/notation.json; cards.json", status="PASS",
      evidence="notation.json registers T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f and blackboard Q. None occurs in the FC1 pages. The page's y and t (lines 58, 178) are local and unregistered. Plain Q, the volume in L03 card FC1-c131, is not the registered blackboard Q; no collision in this unit."),
 dict(id="proj-footer-claim", check="2.9-smoke", location="project.html line 341 footer", status="PASS",
      evidence="page_smoke: no external requests (" + E + "page_smoke_project.out). grader.js fetches only the same-origin grader files and the store is IndexedDB; nothing leaves the browser."),
 dict(id="proj-saved-as-you-type", check="2.9-prose", location="project.html line 301", status="PASS",
      evidence="course/assets/js/grader.js line 59-61: an input listener saves the editor text to the store after a 400 ms debounce."),
 dict(id="proj-references-reading-list", check="2.1-citations", location="project.html lines 321-333 (data-cite keys)", status="PASS",
      evidence="Both keys (mishkin2021economics, harris2002trading) exist in references/references.json with status verified; the page cites by key only (architect decision)."),
 dict(id="proj-cited-year-conflicts", check="2.1-citations", location="references/references.json; curriculum/02-economics-finance-core.yaml lines 384-385; L05.html", status="PASS",
      evidence="Registry years: harris2002trading 2002 (notes.year: curriculum 2003, crossref 2002); mishkin2021economics 2021 (notes.year: curriculum 2022). The page shows the registry year only (architect decision). Offline check only: verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (" + E + "verify_refs_offline.out). Flags below."),
 dict(id="proj-data-simulated", check="2.8-data", location="project.html lines 45, 54, 72, 159; grader/instance.py docstring and label", status="PASS",
      evidence="No dataset is read; every value is labelled SIMULATED (instance.py label; project.html line 54)."),
 dict(id="proj-reference-deployment", check="2.6-autograder (BLUEPRINT §7)", location="course/modules/FC/FC1/grader/reference.py", status="FAIL",
      evidence="BLUEPRINT.md line 400-401: 'Deployment publishes course/ ... and excludes every grader/reference.py: the suites are public, the reference solutions are not.' The repo has no exclusion: no .vercelignore, vercel.json or deploy config is tracked (git ls-files), tools/ and .github/workflows/ci.yml never exclude reference.py, and reference.py sits under course/ (" + E + "deploy_exclusion_check_r6.out). reference.py's own docstring says 'no file in this repository enforces that'. The round-5 PASS is not supported by any artifact.",
      fix="Make the publish step exclude every course/**/grader/reference.py (a deploy-config exclusion committed to the repo, or moving reference solutions outside course/ and updating tools/run_graders.py, check_projects.py and page_smoke.py, which read grader/reference.py). This is repo-wide: it applies to every autograded unit, not only FC1."),
]
# keep round-5 ids, in order: the round-5 rows above are all present except the three new ones added below
new_ids = {"proj-mutants-r6c-killed"}
assert len(rows) == len({r["id"] for r in rows})
fragment = {
 "unit": "FC1",
 "slice": "c",
 "round": 6,
 "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 6 (did not build FC1)",
 "pin": "142ecfc2bd27061de18bd67e83df81e69f5c249d",
 "base": "440ed3c8216725d498d9c6d7c746907d4d418198 (round-5 pin of this slice; delta 440ed3c..142ecfc read for project.html, grader/test_project.py, cards.json and the r5c_/r6c_ mutants)",
 "checkout": str(ROOT),
 "scratch": "/tmp/fc1c_r6_* (nums, lessons, collect, dec28, dec40, fix, fixall, starter, leak, alt, probe); durable copies in ledgers/FC1/scripts/FC1-c-r6/",
 "verified_at": "2026-11-04T05:20:00+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [
   "harris2002trading: registry year 2002 (Crossref); curriculum/02-economics-finance-core.yaml line 385 says 'Harris, Trading and Exchanges (2003)'. The project page cites the key only. For the curriculum owner.",
   "mishkin2021economics: registry year 2021 (OpenLibrary, origin manual); curriculum line 384 says '13th ed. (2022)'. Not checked online (offline only). The project page cites the key only. For the curriculum owner."
 ],
 "freshness_flags": [],
 "notes": [
   "Round 6 on 142ecfc. Delta 440ed3c..142ecfc read in full for FC1 slice files: project.html (lines 43, 163, 171), grader/test_project.py (two tests added at 455 and 510), cards.json (15 changed cards, c136-c138 added), and the r5c_ mutants. Lessons, labs, reference/instance/starter, alternatives and notation are byte-identical to round 5.",
   "Round-5 FAIL rows proj-mutant-price-epsilon-survivor and proj-mutant-yield-100-survivor are re-verified as PASS (killed now). Round-5 PASS rows were all re-run or re-read in this round, not carried.",
   "New survivors found this round (five) are FAIL rows, each with a fix whose probe tests were validated in scripts/FC1-c-r6/proposed_grader_fix_r6.py; the probes make all 111 mutants die and keep reference and all alternatives passing. The project page's count must change from 74 to 78 with the fix.",
   "Plan item (5) of the five alternatives (a float implementation) is not a correct implementation under the page's exact-fraction rule and is not used. a5 stands in for it.",
   "Lessons L01-L05 were read in full (stripped text) only to check cards. Their prose, labs and problem sets are not in this slice and were not audited here.",
   "Could not check: the deployed site (no deploy config in repo); live Crossref / publisher checks (offline only, no network); the full pytest suite (only -k FC1: 9 passed); in-browser runs for seeds other than one; hours (ruling: design targets).",
   "Repo-wide gate notes outside this slice: 'ruff format --check .' fails on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py. Pre-existing tracked files in ledgers/FC1/scripts/FC1-c-r6/ (from commit 0d2d0f3f) were left as they were; my make_mutants script was restored from git after I overwrote it by name, and my generator is make_r6c_mutants_verifier_r6.py."
 ],
 "summary": "Round 6 on 142ecfc: 74 rows: 67 PASS, 7 FAIL, 0 UNVERIFIABLE. Verdict FAIL. Mutants: 106/111 killed on seeds 0-19 (five survivors: schedule cap at 40, exponent cap at 40, yield cap at 200 %, settlement cap at 100, 40-digit Decimal). FAIL rows: proj-mutants-all (aggregate), the five survivor rows, and proj-reference-deployment (no exclusion of grader/reference.py from the published course/ tree in the repo). Fix validated in scripts/FC1-c-r6/proposed_grader_fix_r6.py: 111/111 killed, reference and all nine alternatives pass."
}
pathlib.Path(ROOT / "ledgers/FC1/FC1-c.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "fail", sum(r["status"] == "FAIL" for r in rows), "pass", sum(r["status"] == "PASS" for r in rows))
