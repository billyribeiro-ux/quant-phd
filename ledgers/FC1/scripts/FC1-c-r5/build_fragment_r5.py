"""Round 5 verifier (FC1-c): build the fragment ledgers/FC1/FC1-c.json from the rows and the mutate_graders output."""
import json
import pathlib
import re

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-FC1-c")
OUT_DIR = ROOT / "ledgers/FC1/scripts/FC1-c-r5/out"
mutate_lines = (OUT_DIR / "mutate_graders_0_19_r5.out").read_text(encoding="utf-8").splitlines()

mutants = []
for line in mutate_lines:
    m = re.match(r"^(KILLED|SURVIVED) (\S+\.py): (.*)$", line)
    if not m:
        continue
    status, name, rest = m.groups()
    desc, _, killed = rest.rpartition(" -> ")
    if status == "KILLED":
        killed_by = killed
    else:
        killed_by = "none: survives every test on seeds 0-19"
    mutants.append({"name": name, "description": desc, "killed_by": killed_by, "outcome": status})
assert len(mutants) == 103, len(mutants)

P = "PASS"
F = "FAIL"
rows = [
    {"id": "proj-check-projects", "check": "2.6-structure", "location": "course/modules/FC/FC1/project.html", "status": P,
     "evidence": "tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS', exit 0 (ledgers/FC1/scripts/FC1-c-r5/out/check_projects.out)."},
    {"id": "proj-check-pages", "check": "2.9-structure", "location": "course/modules/FC/FC1/project.html", "status": P,
     "evidence": "tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', exit 0 (out/check_pages.out)."},
    {"id": "proj-check-dag", "check": "2.9-DAG", "location": "project.html data-concept links (lines 58, 178)", "status": P,
     "evidence": "tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS', exit 0 (out/check_dag.out). Links are present-value (lines 58, 178) and discount-factor (line 178), both M1 concepts inside the closure. Futures, swaps, options, bond-price-yield, order-book and settlement-cycle appear as plain prose only (lines 157, 316)."},
    {"id": "proj-run-labs", "check": "2.5-labs", "location": "project.html Labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py; lesson twins L01-L05",
     "status": P,
     "evidence": "tools/run_labs.py --unit FC1 --page project -> 'run_labs FC1: PASS (3/3)'; --unit FC1 -> 'PASS (8/8)' (out/run_labs_project.out, out/run_labs_fc1.out). Project twins run alone as python -I -W error: exit 0 each (out/project_labs_I_W_error_r5.out). Lesson twins run alone as python -I -W error: exit 0, outputs in out/lesson_labs_output_r5.out."},
    {"id": "proj-page-smoke", "check": "2.9-smoke", "location": "course/modules/FC/FC1/project.html", "status": P,
     "evidence": "tools/page_smoke.py --unit FC1 --pages project -> 'page_smoke modules/FC/FC1/project.html: PASS'; in-browser 'All 72 tests pass on seed 717609726' (out/page_smoke_project.out)."},
    {"id": "proj-run-graders", "check": "2.6-autograder-1", "location": "grader/reference.py, test_project.py, instance.py, starter.py", "status": P,
     "evidence": "tools/run_graders.py --unit FC1 --seeds 0-49 -> 'run_graders FC1: PASS (reference 50/50 seeds)' (out/run_graders_0_49.out). Scratch /tmp/fc1c_r5_collect (test_project.py + instance.py + reference as instruments.py): 72 passed with QF_SEED=0. starter.py as instruments.py: '70 failed, 2 passed' (out/project_labs_I_W_error_r5.out); the two passing tests accept any exception on an input the page does not name."},
    {"id": "proj-lint-types", "check": "gate", "location": "course/modules/FC/FC1/grader/*.py, tests/labs/FC1/, ledgers/FC1/mutants/", "status": P,
     "evidence": "ruff check . -> 'All checks passed!' (out/ruff_check.out); ruff format --check on course/modules/FC/FC1 and tests/labs/FC1 -> '12 files already formatted' (out/ruff_format_fc1.out); mypy --no-incremental -> 'Success: no issues found in 331 source files' (out/mypy.out). Whole-repo ruff format was not rerun this round (round 4 flagged only ledgers/M3/retired, outside this slice)."},
    {"id": "proj-lab1-numbers", "check": "2.2-numbers / 2.5-labs", "location": "project.html lines 58, 97-100 (Lab 1)", "status": P,
     "evidence": "ledgers/FC1/scripts/FC1-c-r5/numbers_r5.py (out/numbers_r5.out): exact PV 225796875/2197 = 102775.0910332..., fraction .0910 below one half, price 102775; trade -98500. Lines 58 and 97-100 agree."},
    {"id": "proj-lab2-blanks", "check": "2.5-labs", "location": "project.html lines 133, 140, 149 (Lab 2)", "status": P,
     "evidence": "Blanks are the exponent period (line 133) and -side * quantity * price_cents (line 140), matching the Lab 1 expressions. run_labs PASS (out/run_labs_project.out). Tolerance 1e-6 * (1 + 102775.09) = 0.1028 cent, matching 'about 0.1 cent' on line 149."},
    {"id": "proj-lab3-fixture-values", "check": "2.2-numbers / 2.5-labs", "location": "project.html lines 198-276 (Lab 3)", "status": P,
     "evidence": "out/numbers_r5.out re-derives every Lab 3 printed value: A [(1,10500)] price 10000; B 11053 (exact 11052.6316); C [(1,5001),(2,15002)]; D [(1,2)]; rounding events [(1,500),(2,500),(3,10500)], once 10278, termwise 10277; E (2,-98500); F [(1,1)] price 1 (exact 1/2, round() gives 0); G [(1,10001)] price 5001. All equal the expected block (lines 263-275). run_labs PASS; twin run python -I -W error exit 0."},
    {"id": "proj-rounding-fixture-terms", "check": "2.2-numbers", "location": "project.html line 193; grader/test_project.py lines 383-401 (lines moved by the inserted 40-period test)", "status": P,
     "evidence": "out/numbers_r5.out: exact PV 10277.509103322713 -> 10278 rounded once; terms 480.7692, 462.2781, 9334.4618 -> 481+462+9334 = 10277. Page line 193 and the test docstrings agree."},
    {"id": "proj-lab3-claim-using-functions", "check": "2.5-labs / prose vs code", "location": "project.html line 198 vs twin tests/labs/FC1/lab-FC1-project-3.py", "status": P,
     "evidence": "Hypothesis: functions for the bond, exact arithmetic (Fraction or int) for the trade and the exact values. Twin: bond_events and bond_price (Fraction sums), trade is the int product 10 * 9850 (line 252). tests/labs/FC1 is byte-identical to the round-4 pin."},
    {"id": "proj-expected-equals-output", "check": "2.5-labs", "location": "project.html expected blocks lines 97-100, 145-148, 263-275", "status": P,
     "evidence": "run_labs 3/3 and 8/8 (out/run_labs_project.out, out/run_labs_fc1.out) compare each expected block with the twin output under the page rule; numbers_r5.out re-derives each value."},
    {"id": "proj-hours-arithmetic", "check": "2.9-hours", "location": "project.html table#hours lines 286-293; data-hours-project line 34; index.html lines 29, 38-41", "status": P,
     "evidence": "Rows 1+2+5+4+2+3+3 = 20 (project.html line 293). index.html line 29: data-hours-lessons 50 + data-hours-project 20 = 70; line 41 '20 h project (28.6% of the 70 module hours)'; 20/70 = 28.57 %. Each lesson header says 10 study hours (5 x 10 = 50)."},
    {"id": "proj-hours-rationale-rows", "check": "2.9-hours", "location": "project.html table#hours rows lines 286-293", "status": P,
     "evidence": "Row 'named conditions' (line 290): eight conditions, side refused on 0, 2, -2, 3, -3 and accepted on +1, -1: matches test_trade_side_* at lines 598-628. Row 'bond events' (half-cent case, face in last period, one rounding) matches tests at lines 189-202, 304-329, 383-401."},
    {"id": "proj-hours-verifier-estimate", "check": "2.6-hours", "location": "project.html table#hours lines 286-293", "status": P,
     "evidence": "Carried from round 4 (project.html table#hours lines 286-293 byte-identical since the previous pin, 4eb6788): verifier estimate 12.5-19 h against 20 h declared; hours are design targets (ruling)."},
    {"id": "proj-ladder", "check": "2.6-ladder", "location": "project.html lines 41-50 (ladder), 56-102 (rung 1), 104-150 (rung 2), 153-172 (rung 3), 312-319 (rung 4)", "status": P,
     "evidence": "Rung 1 fully worked (Lab 1 steps 1-5); rung 2 completion graded by run_labs; rung 3 spec within the cash-instrument scope (ruling 5); rung 4 open-ended and marked not graded (line 314). Tier U: minimal-rungs rule does not apply."},
    {"id": "proj-spec-interface", "check": "2.6-spec", "location": "project.html line 161; grader/starter.py lines 16-40; grader/reference.py", "status": P,
     "evidence": "Names and signatures on the page match starter.py: Bond(face_cents, coupon_bps, periods) with events(); bond_price_cents(bond, yield_bps); CashTrade(quantity, price_cents, side, settlement_day) with events(). Scratch reference run: 74 passed with the two fix tests appended (/tmp/fc1c_r5_fix)."},
    {"id": "proj-named-conditions", "check": "2.6-spec", "location": "project.html lines 163-167; grader/test_project.py lines 215-223, 232-240, 258-261, 485-492, 536-543, 585-587, 598-628, 631-638",
     "status": P,
     "evidence": "Eight named conditions: periods<1 (215-223), face<=0 (232-240), coupon<0 (258-261), yield<=-10000 (485-492), quantity<1 (536-543), price<0 (585-587), side not in {+1,-1} (598-620), settlement_day<1 (631-638). Accepted boundary tested for each (225-229, 242-247, 263-266, 495-498, 546-551, 590-595, 623-628, 641-646). Each refusal uses must_raise, which requires ValueError only for these conditions."},
    {"id": "proj-test-count", "check": "2.6-count", "location": "project.html line 171 ('72 checks'); grader/test_project.py", "status": P,
     "evidence": "pytest --collect-only in scratch: '72 tests collected' (out/collect_only_r5.out); 72 'def test_' functions by grep; in-browser 'All 72 tests pass' (out/page_smoke_project.out). Page says 72."},
    {"id": "proj-starter-fails", "check": "2.6-autograder", "location": "grader/starter.py", "status": P,
     "evidence": "starter.py as instruments.py: 70 failed, 2 passed (out/project_labs_I_W_error_r5.out tail). The 2 passing are the accept-any-exception tests test_non_whole_face_is_refused_or_gives_ints and test_bool_periods_is_not_quietly_accepted_as_a_number."},
    {"id": "proj-instances", "check": "2.6-autograder-2", "location": "grader/instance.py seeds 0-19", "status": P,
     "evidence": "Carried from round 4 (grader/instance.py byte-identical since the previous pin, 4eb6788): every case satisfies the named conditions over seeds 0-19 (ledgers/FC1/scripts/FC1-c-r4/out/instances_0_19_r4.out). The five alternatives and the new fixes pass seeds 0-19 in this round (proj-alternatives)."},
    {"id": "proj-silence-purity", "check": "2.6-autograder", "location": "grader/test_project.py lines 670-724", "status": P,
     "evidence": "test_the_module_prints_nothing (670-693) covers 14 valid runs incl. boundaries named in its docstring; test_refused_inputs_print_nothing_before_they_raise (696-711) covers the 8 named refusals; test_repeated_events_calls_agree (714-724). Reference: 74 passed (scratch)."},
    {"id": "proj-same-suite-pyodide-pytest", "check": "2.6-autograder-5", "location": "grader/test_project.py", "status": P,
     "evidence": "Local pytest of the same file with the reference: 72 passed (out/collect_only_r5.out scratch run). Pyodide: page_smoke in-browser 'All 72 tests pass' (out/page_smoke_project.out)."},
    {"id": "proj-mutants-all", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/*.py (103 files)", "status": F,
     "evidence": "tools/mutate_graders.py --unit FC1 --seeds 0-19 -> 'mutate_graders FC1: FAIL (101/103 killed)' (out/mutate_graders_0_19_r5.out). Survivors: r5c_price_rounded_with_epsilon.py (row proj-mutant-price-epsilon-survivor) and r5c_yield_above_one_hundred_percent_refused.py (row proj-mutant-yield-100-survivor). All 99 earlier mutants are killed.",
     "fix": "Append the two tests below to grader/test_project.py (verified in a scratch copy, /tmp/fc1c_r5_fix, built by ledgers/FC1/scripts/FC1-c-r5/fix_tests_r5.py): test_bond_price_just_under_a_half_cent_rounds_down (Bond(300_075_005, 0, 3) at 1 bps == 299_985_000) and test_yield_above_one_hundred_percent_is_accepted (Bond(10_000, 500, 1) at 15_000 bps == 4_200). Reference passes 74; both survivors and the other new mutant fail; all five alternatives pass. Then re-run tools/mutate_graders.py --unit FC1 --seeds 0-19 and update the test count on project.html line 171 (74) and its list of checks."},
    {"id": "proj-mutants-v1c-new", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/v1c_*.py (5 student-error mutants, round 1)", "status": P,
     "evidence": "All five killed on seeds 0-19 (out/mutate_graders_0_19_r5.out)."},
    {"id": "proj-mutants-v2c-new", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r2c_*.py (4 student-error mutants, round 2)", "status": P,
     "evidence": "All four killed on seeds 0-19 (out/mutate_graders_0_19_r5.out)."},
    {"id": "proj-mutants-r3c-killed", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r3c_*.py (round 3)", "status": P,
     "evidence": "All five killed on seeds 0-19 (out/mutate_graders_0_19_r5.out)."},
    {"id": "proj-mutants-v4c-new", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/v4c_*.py (5 student-error mutants)", "status": P,
     "evidence": "All five killed on seeds 0-19 (out/mutate_graders_0_19_r5.out)."},
    {"id": "proj-mutants-r4c-new", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r4c_*.py (5 student-error mutants, round 4)", "status": P,
     "evidence": "All five killed on seeds 0-19 (out/mutate_graders_0_19_r5.out), including the two round-4 survivors r4c_schedule_stops_at_thirty_periods.py and r4c_discount_exponent_capped_at_thirty.py, now killed by test_bond_schedule_of_forty_periods_is_complete_and_discounted_by_its_own_period."},
    {"id": "proj-mutants-r5c-new", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r5c_*.py (4 student-error mutants written by this verifier, round 5)", "status": P,
     "evidence": "Written by ledgers/FC1/scripts/FC1-c-r5/make_mutants_r5.py. Killed on seeds 0-19: r5c_discount_exponent_capped_at_twenty_four (by the 40-period test), r5c_settlement_event_one_period_late (by test_trade_has_one_settlement_event_on_its_settlement_day). The two survivors are rows proj-mutant-price-epsilon-survivor and proj-mutant-yield-100-survivor."},
    {"id": "proj-mutant-schedule-cap-thirty-survivor", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r4c_schedule_stops_at_thirty_periods.py vs grader/test_project.py line 318", "status": P,
     "evidence": "Round-4 survivor now KILLED on seed 0 by test_bond_schedule_of_forty_periods_is_complete_and_discounted_by_its_own_period (out/mutate_graders_0_19_r5.out)."},
    {"id": "proj-mutant-exponent-cap-thirty-survivor", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r4c_discount_exponent_capped_at_thirty.py vs grader/test_project.py line 318", "status": P,
     "evidence": "Round-4 survivor now KILLED on seed 0 by test_bond_schedule_of_forty_periods_is_complete_and_discounted_by_its_own_period (out/mutate_graders_0_19_r5.out)."},
    {"id": "proj-mutant-schedule-cap-survivor", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r3c_schedule_stops_at_twenty_periods.py vs grader/test_project.py lines 304-315", "status": P,
     "evidence": "KILLED on seeds 0-19 by test_bond_schedule_longer_than_twenty_periods_is_complete (out/mutate_graders_0_19_r5.out)."},
    {"id": "proj-mutant-price-digits-survivor", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r3c_price_ten_digits_integral_rounding.py vs grader/test_project.py lines 431-442", "status": P,
     "evidence": "KILLED on seeds 0-19 by test_bond_price_exact_half_above_ten_significant_digits_is_exact (out/mutate_graders_0_19_r5.out)."},
    {"id": "proj-mutant-periods-13-15-survivor", "check": "2.6-mutation", "location": "grader/test_project.py lines 281-301", "status": P,
     "evidence": "KILLED on seeds 0-19: r2c_bond_periods_capped_at_twelve by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period (out/mutate_graders_0_19_r5.out)."},
    {"id": "proj-mutant-price-cache-survivor", "check": "2.6-mutation", "location": "grader/test_project.py lines 469-482; project.html lines 161, 178", "status": P,
     "evidence": "KILLED on seeds 0-19: r2c_price_cached_on_first_yield by test_one_bond_priced_at_two_yields_gives_each_yield_its_own_price (out/mutate_graders_0_19_r5.out)."},
    {"id": "proj-mutant-price-epsilon-survivor", "check": "2.6-mutation (rule: exact half-cent rounding)", "location": "ledgers/FC1/mutants/r5c_price_rounded_with_epsilon.py; project.html line 176; grader/test_project.py (no test near a half cent that is not exact)", "status": F,
     "evidence": "Student error: bond_price_cents adds 1e-9 cent before rounding. SURVIVES seeds 0-19 (out/mutate_graders_0_19_r5.out). The page states the rule: 'a coupon or a price is computed from exact fractions, and it is rounded once, to the nearest cent, with a half going away from zero' (project.html line 176; also line 163 'computed from exact fractions'). A price a hair under a half cent must round down; the mutant rounds it up. No test has an exact price just under a half cent. Ruling 9 applies (stated behaviour).",
     "fix": "Append test_bond_price_just_under_a_half_cent_rounds_down: sol.Bond(300_075_005, 0, 3) at yield 1 bps must equal 299_985_000 (exact price 299985000 + 1/2 - 1/(2*1000300030001); verified with out/numbers_r5.out logic in ledgers/FC1/scripts/FC1-c-r5/near_half_r5.py). Scratch-verified: reference passes; the mutant fails (1 failed, 73 passed); all five alternatives pass."},
    {"id": "proj-mutant-yield-100-survivor", "check": "2.6-mutation (rule: named refusals only)", "location": "ledgers/FC1/mutants/r5c_yield_above_one_hundred_percent_refused.py; project.html lines 163, 166, 178; grader/test_project.py lines 332-339 (the coupon-above-100% test)", "status": F,
     "evidence": "Student error: bond_price_cents raises ValueError for yield_bps > 10000. SURVIVES seeds 0-19 (out/mutate_graders_0_19_r5.out). The page names one yield refusal only: 'yield_bps at or below -10000, because 1+y must be positive' (line 166); it says only named conditions raise and that other invalid inputs may do anything (line 163); it states 10000 is 100 % (line 178). A 150 % per-period yield is therefore not a named invalid input, and no test prices any yield above 900 bps. The grader already treats an unnamed upper limit as valid for the coupon (lines 332-339). Judgement: the cited sentences make the refusal of a valid rate a violation; the verifier reports it as FAIL.",
     "fix": "Append test_yield_above_one_hundred_percent_is_accepted: sol.bond_price_cents(sol.Bond(10_000, 500, 1), 15_000) must equal 4_200 (10500 / 2.5). Scratch-verified: reference passes; the mutant fails (1 failed, 73 passed); all five alternatives pass."},
    {"id": "proj-alternatives", "check": "2.6-autograder-3", "location": "ledgers/FC1/alternatives/a1..a5 (scripts ledgers/FC1/scripts/FC1-c-r5/run_alts_r5.sh)", "status": P,
     "evidence": "Each of the five alternatives passes the test file, the same instance and seeds 0-19: a1 20/20, a2 20/20, a3 20/20, a4 20/20, a5 20/20 (out/alternatives_0_19_r5.out). Covers list comprehensions, generator methods, Fraction throughout, integer division half-up and a frozen-dataclass reduce."},
    {"id": "proj-alternatives-r4-new", "check": "2.6-autograder-3", "location": "ledgers/FC1/scripts/FC1-c-r4/alt/alt6_r4_pow_fraction_floor.py", "status": P,
     "evidence": "Passes the test file on seeds 0-19 (20/20, out/alternatives_0_19_r5.out)."},
    {"id": "proj-docstring-float-claim", "check": "2.2-numbers / prose", "location": "grader/test_project.py lines 421-452 (float claims in docstrings), lines 574-577", "status": P,
     "evidence": "numbers_r5.out: 1734792 / 1.0496 = 3305625/2 = 1652812.5, rounds to 1652813; float discounting gives 1652812.4999999998 (python). 13 / 1.04 = 25/2; (1+0.04)**-1 * 13 = 12.499999999999998 (python). (2**40+1)*9851 = 10831289045231227, odd, above 2**53. Coupon of face 10**17+4999 at 1 bps = 10**13 + 0.4999 cents rounds to 10**13. All confirmed."},
    {"id": "proj-named-error-message-values", "check": "2.6-messages", "location": "grader/test_project.py (every assert and pytest.fail site)", "status": P,
     "evidence": "Read in full (lines 1-770). must_raise messages name the condition and never an expected value; the assert messages name the property (for example 'a half-cent coupon must round away from zero'). No message prints an expected answer."},
    {"id": "proj-failure-messages", "check": "2.6-messages", "location": "grader/test_project.py (every assert and pytest.fail site)", "status": P,
     "evidence": "Read in full. Each message names the violated property and the idea to revisit; the NotImplementedError wrapper (lines 747-770) names the property with no traceback."},
    {"id": "proj-cards-scan-duplicates", "check": "2.6-cards", "location": "course/modules/FC/FC1/cards.json (135 cards)", "status": P,
     "evidence": "python scan: 135 cards, ids unique, fronts unique; the 11 new cards FC1-c125..c135 ask questions not asked by any other card (checked against all fronts). Round 4 counted 124 cards."},
    {"id": "proj-cards-numbers-in-lessons", "check": "2.6-cards", "location": "course/modules/FC/FC1/cards.json; L01-L05 text and lesson_labs_output_r5.out", "status": P,
     "evidence": "ledgers/FC1/scripts/FC1-c-r5/card_refs_r5.py: every three-digit-or-more number in a card (front, back, basis) and every citation label (Definition, Proposition, Remark, Example, Problem, Section, misconception, Assumption) occurs in its own lesson text or in the lesson lab output. The seven 'Assumption A1/B1/B2/B3/B4/A3' citations occur as 'A1 (...)' or 'B1 (...)' items in L01 and L03."},
    {"id": "proj-cards-sample", "check": "2.6-cards", "location": "cards.json all 135 cards against L01-L05 labelled blocks and lab outputs", "status": P,
     "evidence": "Every card read (not a sample). L01 read in full; L02-L05 read in their labelled blocks (definitions, propositions, remarks, examples, misconceptions, problems) and the lines each card cites; each card's number checked against lab outputs (out/lesson_labs_output_r5.out): e.g. c010 686189, c011 181818, c092 181790, c093 -50, c097 -545, c098 3455, c084 0.209, c082 2172960, c083 Friday 2026-10-30, c061 159000, c062 985 fill, c029/c095/c096 counts."},
    {"id": "proj-cards-changed-subjects", "check": "2.6-cards", "location": "cards.json FC1-c013, -018, -020, -026, -036, -056, -066, -069, -074, -076, -077, -090, -091, -106, -116", "status": P,
     "evidence": "Each changed back re-read against the current lesson text: c013 = Prop 4.1 (L01); c018 = Section 5 (L01); c020 = Assumption 1.3 (L02); c026 = Remark 2.3 (L02); c036 = Def 1.2 (L03, m and h whole numbers); c056 = Def 1.1 (L04, 'now'); c066 = Prop 2.3 (L04); c069 = Lab 1 output (0 and 0); c074 = Def 1.1 (L05); c076 = Def 1.2 (L05); c077 = Remark 1.3 (L05); c090 = Section 4 and registry (no settlement-cycle title among 560 references); c091 = Remark 4.2 (L01); c106 = A3 (L03); c116 = Remark 1.2 (L02). All agree."},
    {"id": "proj-cards-c014-lab-true", "check": "2.6-cards", "location": "cards.json FC1-c014 (L01)", "status": P,
     "evidence": "Lab 1, Part A prints 'the partial sums equal the closed form exactly for n = 0 to 10: True' (out/lesson_labs_output_r5.out). Card grade T with basis is consistent with Proposition 3.1."},
    {"id": "proj-cards-c122-equity-after-loss", "check": "2.6-cards", "location": "cards.json FC1-c122 (L01)", "status": P,
     "evidence": "Proposition 4.1 (L01): equity after loss is E - lambda; nonnegative iff lambda <= E. Card matches. Grade T is proof-backed."},
    {"id": "proj-cards-citation-R3", "check": "2.6-cards", "location": "cards.json FC1-c054 (L03)", "status": P,
     "evidence": "Lab output 'pairs with no strictly profitable deviation in the grid: (100,100), (101,101), (102,102)'; '121 pairs' (out/lesson_labs_output_r5.out). Card grade C names Lab 1, Part C."},
    {"id": "proj-cards-citation-R2", "check": "2.6-cards", "location": "cards.json FC1-c089 (L05)", "status": P,
     "evidence": "Proof of Proposition 2.1(ii) (L05) uses A1 (non-negative considerations) for Pay_j >= 0. Counterexample arithmetic: one trade with consideration -100 gives NP = 100 and G = -100, so 100 <= -100 fails."},
    {"id": "proj-cards-citation-scan", "check": "2.6-cards", "location": "cards.json block references", "status": P,
     "evidence": "card_refs_r5.py: all citation labels resolve in the card's lesson (see proj-cards-numbers-in-lessons)."},
    {"id": "proj-cards-grades", "check": "2.6-cards", "location": "cards.json grade and basis fields vs lesson grading", "status": P,
     "evidence": "C cards cite SIMULATED labs or hand readings (c030, c033, c034, c052, c053, c054, c069, c082-c088, c097, c098) with basis fields; T cards are proof-backed (for example c009 Prop 3.5, c125 Prop 2.2 with typed-in Lab 1 Part B check). New definition cards c126-c135 carry no grade (None), like the other definitions."},
    {"id": "proj-spec-scope-vs-curriculum", "check": "2.6-scope", "location": "project.html lines 157, 161; curriculum/02-economics-finance-core.yaml lines 388-395", "status": P,
     "evidence": "Carried from round 4 (project.html lines 157 and 161 and curriculum/02-economics-finance-core.yaml byte-identical since the previous pin 4eb6788): FC2 is 'Derivatives Fundamentals' (FC2/index.html h1), matching the page's statement."},
    {"id": "proj-terminology-short-holder", "check": "2.6-terms", "location": "project.html lines 54, 179; grader/reference.py docstring line 10", "status": P,
     "evidence": "Carried from round 4 (project.html lines 54 and 179 and grader/reference.py byte-identical since the previous pin 4eb6788): 'holder' is defined on line 54 before use on line 179."},
    {"id": "proj-prose-banned-phrases", "check": "2.12-process-words", "location": "course/modules/FC/FC1/project.html; cards.json; L01-L05.html; grader/*.py", "status": P,
     "evidence": "grep for round, verifier, builder, architect, ruling, blueprint, planned, placeholder, todo over the slice: no learner-text hit (the grep matches are code-variable names and 'Round' does not appear in learner text)."},
    {"id": "proj-scope-words", "check": "2.4-scope", "location": "project.html lines 163, 171, 176, 180, 184, 276; cards.json scope words; grader/test_project.py lines 9-13", "status": P,
     "evidence": "Scope words in cards: every/only/exactly/always/never checked against their lesson statements (for example c050 'exactly the three', c054 'only equilibria' verified by Lab 1 Part C, c066 'after every event' holds for the proof's general state). No unsupported universal claim found."},
    {"id": "proj-terms-before-definition", "check": "2.5-terms", "location": "project.html lines 38, 54, 58, 178", "status": P,
     "evidence": "face, coupon, settlement period defined on line 54 before use in Lab 1 (line 58); present value and discount factor linked to their concept pages on lines 58 and 178."},
    {"id": "proj-notation", "check": "2.7-notation", "location": "project.html lines 58, 106, 178; notation/notation.json; cards.json", "status": P,
     "evidence": "project.html uses y, t and (1+y) only; notation.json registers no y or t. Plain Q (volume, card c131, L03) is not the registered \\mathbb{Q}; plain R (L04 resting shares) is not the registered \\R; T in cards is a grade field, not the registered T. No registered symbol takes another meaning."},
    {"id": "proj-footer-claim", "check": "2.5-prose", "location": "project.html line 341 footer", "status": P,
     "evidence": "Carried from round 4 (project.html line 341 byte-identical since the previous pin 4eb6788): the autograder runs in the browser; the page's grader panel (line 302) is the same suite."},
    {"id": "proj-saved-as-you-type", "check": "2.5-prose", "location": "project.html line 301", "status": P,
     "evidence": "Carried from round 4 (project.html line 301 byte-identical since the previous pin 4eb6788)."},
    {"id": "proj-references-reading-list", "check": "2.8-references", "location": "project.html lines 321-333 (data-cite keys)", "status": P,
     "evidence": "Carried from round 4 (project.html lines 321-333 byte-identical since the previous pin 4eb6788): cited keys mishkin2021economics and harris2002trading exist in references/references.json (unchanged)."},
    {"id": "proj-cited-year-conflicts", "check": "2.8-references", "location": "references/references.json; curriculum/02-economics-finance-core.yaml lines 384-385; L05.html Remark 'registry holds that book under the year 2002'", "status": P,
     "evidence": "Carried from round 4 (references/references.json and the curriculum yaml byte-identical since the previous pin 4eb6788). Registry flag (year mismatch for the curriculum owner) carried in registry_flags; it is not an FC1-c defect."},
    {"id": "proj-data-simulated", "check": "2.5-data", "location": "project.html lines 45, 54, 72, 159; grader/instance.py docstring and label", "status": P,
     "evidence": "Carried from round 4 (those project.html lines and grader/instance.py byte-identical since the previous pin 4eb6788): every bond and trade is labelled SIMULATED; no file is read."},
    {"id": "proj-reference-deployment", "check": "2.6-deploy", "location": "course/modules/FC/FC1/grader/reference.py", "status": P,
     "evidence": "Carried from round 4 (reference.py byte-identical since the previous pin 4eb6788): the docstring states that the file is not an answer shown to learners and that deployment must exclude it (BLUEPRINT 7); the repo enforces no exclusion (registry note, not a page defect)."},
]

for r in rows:
    if r["status"] != "PASS":
        assert r.get("fix"), r["id"]

fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 5 (did not build FC1)",
    "pin": "440ed3c8216725d498d9c6d7c746907d4d418198",
    "base": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b (round 4 pin of this slice; delta 4eb6788..440ed3c read in full for project.html, grader/test_project.py, cards.json and the r4c mutants)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-FC1-c",
    "scratch": "/tmp/fc1c_r5_collect (suite, instance and reference), /tmp/fc1c_r5_fix (suite with two proposed tests), /tmp/fc1c_r5_text (lesson text), /tmp/fc1c_r5_alt.* (alternatives)",
    "verified_at": "2026-11-03T22:46:06+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [
        {"id": m["name"], "description": m["description"], "killed_by": m["killed_by"], "outcome": m["outcome"]}
        for m in mutants
    ],
    "registry_flags": [
        "mishkin2021economics: registry year 2021 (references/references.json); curriculum/02-economics-finance-core.yaml:384 says 'Mishkin ... 13th ed. (2022)'. Page cites the key only. For the curriculum owner; not an FC1-c defect.",
        "harris2002trading: registry year 2002; curriculum/02-economics-finance-core.yaml:385 says 'Harris, Trading and Exchanges (2003)'. Page cites the key only. For the curriculum owner.",
    ],
    "freshness_flags": [],
    "notes": "Round 5 on 440ed3c. Delta 4eb6788..440ed3c read hunk by hunk: project.html lines 171 (72 checks), 188 and 191 (fixture wording); grader/test_project.py new 40-period test at lines 318-329 (inserted, so later line numbers moved by +14) and docstring changes at 431-435; cards.json wording changes on 15 cards and 11 new cards (FC1-c125..c135); r4c_* mutants tracked. Lesson HTML, index, labs, reference/instance/starter, alternatives, curriculum, references, notation, plan and tools are byte-identical to the round-4 pin. Cards: all 135 read; L01 read in full, L02-L05 read in their labelled blocks and the lines each card cites, with lab outputs captured (out/lesson_labs_output_r5.out). Not checked: L02-L05 running prose outside labelled blocks was not read sentence by sentence; the registry claim 'no settlement-cycle source' was checked by title only (CPMI and BIS pages not opened; no network use); whole-repo ruff format and the full pytest suite were not run (only -k FC1 in tests: 9 passed).",
    "summary": "Round 5 on 440ed3c. 72 rows: 69 PASS, 3 FAIL, 0 UNVERIFIABLE. Verdict FAIL. Mutants: 101/103 killed on seeds 0-19 (the 99 earlier mutants all killed; new survivors r5c_price_rounded_with_epsilon.py and r5c_yield_above_one_hundred_percent_refused.py). FAIL rows: proj-mutants-all (aggregate), proj-mutant-price-epsilon-survivor, proj-mutant-yield-100-survivor. Both fixes are single grader tests verified in scratch (reference 74 pass; all five alternatives pass; both survivors killed). The yield row is a judgement under ruling 9 and is flagged as such.",
}

out = ROOT / "ledgers/FC1/FC1-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, len(rows), "rows", len(mutants), "mutants")
