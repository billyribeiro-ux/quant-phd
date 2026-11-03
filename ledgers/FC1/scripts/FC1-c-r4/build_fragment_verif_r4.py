"""Build the FC1-c round-4 fragment from the r4 command outputs (verifier r4). Writes ledgers/FC1/FC1-c.json only."""
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD4-FC1-c")
HERE = ROOT / "ledgers/FC1/scripts/FC1-c-r4"
OUT = HERE / "out"
MUT = ROOT / "ledgers/FC1/mutants"

PIN = "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b"
BASE = "a007712fdbfc8b4851123f4de76b5310ac5a9e64 (round 3 of this slice; delta a007712f..4eb6788 read in full)"
CARRY = "Carried from round 3 (course/modules/FC/FC1/cards.json entries and assets byte-identical since the previous pin):"
S = "ledgers/FC1/scripts/FC1-c-r4"
O = f"{S}/out"

# ---- mutants: parse the seeds 0-9 run (the window the verifier rules name) and cross-check seeds 0-19 ----
line_re = re.compile(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$")
def parse(path):
    res = {}
    for ln in (HERE / path).read_text(encoding="utf-8").splitlines():
        m = line_re.match(ln)
        if m:
            res[m.group(2)] = (m.group(1), m.group(3).strip(), m.group(4).strip())
    return res
m09 = parse("out/mutate_graders_0_9_r4.out")
m19 = parse("out/mutate_graders_0_19_r4.out")
files = sorted(p.name for p in MUT.glob("*.py"))
assert set(files) == set(m09) == set(m19), (len(files), len(m09), len(m19))
assert {k for k, v in m09.items() if v[0] == "SURVIVED"} == {k for k, v in m19.items() if v[0] == "SURVIVED"}
mutants = []
for name in files:
    status, desc, killed = m09[name]
    if status == "SURVIVED":
        mutants.append({"id": name, "description": desc, "killed_by": None,
                        "status": "SURVIVED on seeds 0-9 and 0-19"})
    else:
        mutants.append({"id": name, "description": desc, "killed_by": killed + " (seeds 0-9 run)"})
survivors = [m["id"] for m in mutants if m["killed_by"] is None]
assert len(mutants) == 99 and len(survivors) == 2, (len(mutants), survivors)

rows = [
 {"id": "proj-check-projects", "check": "2.6-structure", "location": "course/modules/FC/FC1/project.html",
  "status": "PASS", "evidence": f"tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS', exit 0 ({O}/check_projects.out)."},
 {"id": "proj-check-pages", "check": "2.9-structure", "location": "course/modules/FC/FC1/project.html",
  "status": "PASS", "evidence": f"tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', exit 0 ({O}/check_pages.out)."},
 {"id": "proj-check-dag", "check": "2.9-DAG", "location": "project.html data-concept links (lines 58, 178)",
  "status": "PASS", "evidence": f"tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS', exit 0 ({O}/check_dag.out). grep data-concept on project.html returns only present-value (lines 58, 178) and discount-factor (line 178); both are M1 concepts, inside the closure {{E1, M1, M2, P0.1}}. Futures, swaps, options, bond-price-yield, order-book and settlement-cycle appear only as plain prose (lines 157, 316; no link, no data-concept)."},
 {"id": "proj-run-labs", "check": "2.5-labs", "location": "project.html Labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py",
  "status": "PASS", "evidence": f"tools/run_labs.py --unit FC1 --page project -> 'run_labs FC1: PASS (3/3)'; --unit FC1 -> 'PASS (8/8)' ({O}/run_labs_project.out, {O}/run_labs_fc1.out). The tool enforces page-code/twin byte identity, the python -I -W error twin run, and the expected-output tolerance."},
 {"id": "proj-page-smoke", "check": "2.9-smoke", "location": "course/modules/FC/FC1/project.html",
  "status": "PASS", "evidence": f"tools/page_smoke.py --unit FC1 --pages project -> 'page_smoke modules/FC/FC1/project.html: PASS', 'in-browser grader: All 71 tests pass' ({O}/page_smoke_project.out)."},
 {"id": "proj-run-graders", "check": "2.6-autograder-1", "location": "grader/reference.py, test_project.py, instance.py, starter.py",
  "status": "PASS", "evidence": f"tools/run_graders.py --unit FC1 --seeds 0-49 -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.1 s)' ({O}/run_graders_0_49.out). Starter: scratch run of starter.py as instruments.py gives 69 failed, 2 passed (the two accept-any-exception tests); {S}/scratch_checks_r4.sh -> {O}/starter_seed0_r4.out."},
 {"id": "proj-lint-types", "check": "gate", "location": "course/modules/FC/FC1/grader/*.py, tests/labs/FC1/, ledgers/FC1/mutants/",
  "status": "PASS", "evidence": f"ruff check . -> 'All checks passed!' ({O}/ruff_check_repo.out); mypy --no-incremental -> 'Success: no issues found in 331 source files' ({O}/mypy_no_incremental.out). ruff format --check . reports one file, ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py, outside FC1 ({O}/ruff_format_repo.out); no FC1 file is flagged. Mutants and scripts are excluded by pyproject extend-exclude (explicit-path ruff runs over them are not the gate)."},
 {"id": "proj-lab1-numbers", "check": "2.2-numbers / 2.5-labs", "location": "project.html lines 58, 97-100 (Lab 1)",
  "status": "PASS", "evidence": f"{S}/numbers_r4_verif_r4.py (output {O}/numbers_r4.out): events [(1,5000),(2,5000),(3,105000)]; exact PV 102775.091033 (fraction .0910332 below one half) -> price 102775; trade (2,-98500). Lines 58 and 97-100 agree."},
 {"id": "proj-lab2-blanks", "check": "2.5-labs", "location": "project.html lines 133, 140, 149 (Lab 2); tests/labs/FC1/lab-FC1-project-2.py",
  "status": "PASS", "evidence": f"Blanks are the exponent period (line 133) and -side * quantity * price_cents (line 140), matching line 149. Tolerance on line 149 'about 0.1 cent': run_labs rule tol*(1+|expected|) = 1e-6*(1+102775.09) = 0.1028 cent. run_labs PASS ({O}/run_labs_project.out)."},
 {"id": "proj-lab3-fixture-values", "check": "2.2-numbers / 2.5-labs", "location": "project.html lines 198-276 (Lab 3); tests/labs/FC1/lab-FC1-project-3.py",
  "status": "PASS", "evidence": f"{O}/numbers_r4.out re-derives every printed Lab 3 value: A [(1,10500)] price 10000; B 11053, exact 11052.6316; C [(1,5001),(2,15002)]; D [(1,2)]; rounding events [(1,500),(2,500),(3,10500)], once 10278, term-by-term 10277; E (2,-98500); F [(1,1)] price 1 (exact 1/2); G [(1,10001)] price 5001 (exact 10001/2). All equal the expected block (lines 263-275). run_labs PASS."},
 {"id": "proj-rounding-fixture-terms", "check": "2.2-numbers", "location": "project.html line 193; grader/test_project.py lines 380-387",
  "status": "PASS", "evidence": f"{O}/numbers_r4.out: exact PV 10277.509103322713 -> 10278 rounded once; terms 480.7692308, 462.2781065, 9334.4617660 -> 481+462+9334 = 10277. Matches page line 193 and the test docstring lines 381-383."},
 {"id": "proj-lab3-claim-using-functions", "check": "2.5-labs / prose vs code", "location": "project.html line 198 vs twin lines 215-259",
  "status": "PASS", "evidence": "Hypothesis says functions for the bond and exact arithmetic (Fraction or int) for the trade and the exact values. The twin uses bond_events and bond_price (Fraction sums), and the trade is the exact int product (line 252). Lab twin unchanged since round 3 (tests/labs/FC1 not in the a007712f..4eb6788 diff)."},
 {"id": "proj-expected-equals-output", "check": "2.5-labs", "location": "project.html expected blocks lines 97-100, 145-148, 263-275",
  "status": "PASS", "evidence": f"run_labs (3/3 and 8/8, {O}/run_labs_project.out) compares each expected block with the twin's output under the page rule; numbers_r4.out re-derives each value independently."},
 {"id": "proj-hours-arithmetic", "check": "2.9-hours", "location": "project.html table#hours lines 286-293; data-hours-project line 34; index.html lines 29, 38-41",
  "status": "PASS", "evidence": "Rows 1+2+5+4+2+3+3 = 20 (project.html line 293 total 20). Hub: data-hours-lessons 50 + data-hours-project 20 = 70 (index.html line 29; line 41 '20 h project (28.6% of the 70 module hours)'; 20/70 = 28.6%)."},
 {"id": "proj-hours-rationale-rows", "check": "2.9-hours", "location": "project.html table#hours rows lines 286-293",
  "status": "PASS", "evidence": "Row 'named conditions' says eight conditions, side refused on 0, 2, -2, 3, -3 and accepted on +1 and -1: matches test_trade_side_* (lines 584-615) and the eight conditions of lines 165-167. Row 'bond events' (half-cent case, face in last period, one rounding) matches tests at lines 189-194, 304-315, 369-377."},
 {"id": "proj-hours-verifier-estimate", "check": "2.6-hours", "location": "project.html table#hours lines 286-293",
  "status": "PASS", "evidence": "Verifier's own estimate of the deliverable: rung 1 read 1 h, rung 2 completion 1.5-2 h, bond events and price 3-5 h, cash trade 2-3 h, named conditions 2-3 h, local suite and fixtures 2-3 h, self-check 1-2 h. Total 12.5-19 h, within 30% of 20 h. Declared hours are design targets (ruling)."},
 {"id": "proj-ladder", "check": "2.6-ladder", "location": "project.html lines 41-50 (ladder), 56-102 (rung 1), 104-150 (rung 2), 153-172 (rung 3), 312-319 (rung 4)",
  "status": "PASS", "evidence": "Rung 1 fully solved and annotated (Lab 1 steps 1-5); rung 2 completion graded by run_labs; rung 3 spec lines 153-172 within the cash-instrument scope (ruling 5); rung 4 open-ended and marked not graded (line 314). Tier U, so the minimal-rungs rule for tier M and up does not apply."},
 {"id": "proj-spec-interface", "check": "2.6-spec", "location": "project.html line 161; grader/starter.py lines 16-40; grader/reference.py",
  "status": "PASS", "evidence": "Names and signatures on the page match starter.py: Bond(face_cents, coupon_bps, periods) with events(); bond_price_cents(bond, yield_bps); CashTrade(quantity, price_cents, side, settlement_day) with events(). reference.py implements the same names. Scratch run of reference: 71 passed (" + O + "/reference_seed0_r4.out)."},
 {"id": "proj-named-conditions", "check": "2.6-spec", "location": "project.html lines 163-167; grader/test_project.py lines 215-260, 318-325, 471-487, 522-534, 571-644",
  "status": "PASS", "evidence": "Eight named conditions: Bond periods<1 (lines 217-223), face<=0 (232-240), coupon<0 (258-261); bond_price yield<=-10000 (471-479); CashTrade quantity<1 (522-530), price<0 (571-575), side not in {+1,-1} (584-607), settlement_day<1 (617-625). Boundary on the accepted side tested for each (lines 225, 242, 263, 481, 532, 576, 609, 627). Each refusal uses must_raise (ValueError only)."},
 {"id": "proj-test-count", "check": "2.6-count", "location": "project.html line 171 ('71 checks'); grader/test_project.py",
  "status": "PASS", "evidence": f"pytest --collect-only in a scratch copy with reference.py as instruments.py: '71 tests collected' ({O}/collect_only_r4.out). Page line 171 says 71. In-browser run 'All 71 tests pass' ({O}/page_smoke_project.out). 71 def test_ functions by ast (scan_asserts_r4.out)."},
 {"id": "proj-starter-fails", "check": "2.6-autograder", "location": "grader/starter.py",
  "status": "PASS", "evidence": f"starter.py as instruments.py: 69 failed, 2 passed (the two accept-any-exception tests, test_non_whole_face_is_refused_or_gives_ints and test_bool_periods_is_not_quietly_accepted_as_a_number) ({O}/starter_seed0_r4.out, from {S}/scratch_checks_r4.sh)."},
 {"id": "proj-instances", "check": "2.6-autograder-2", "location": "grader/instance.py seeds 0-19",
  "status": "PASS", "evidence": f"{S}/instances_r4.py over seeds 0-19 ({O}/instances_0_19_r4.out): every case satisfies the named conditions (face >= 1, periods >= 1, coupon >= 0, yield > -10000, quantity >= 1, price >= 0, side in {{+1,-1}}, settlement_day >= 1); 20 distinct (price, trade) answers of 20; 8 distinct period counts."},
 {"id": "proj-silence-purity", "check": "2.6-autograder", "location": "grader/test_project.py lines 656-710",
  "status": "PASS", "evidence": "test_the_module_prints_nothing covers 14 valid runs including the boundaries named in its docstring (yield -9999, -5000, 0; coupon 0; price 0; side -1; quantity 1; settlement 1; face 1 cent; periods 1, 12). test_refused_inputs_print_nothing_before_they_raise covers the 8 named refusals. test_repeated_events_calls_agree covers purity. Suite passes (reference, 71 passed)."},
 {"id": "proj-same-suite-pyodide-pytest", "check": "2.6-autograder-5", "location": "grader/test_project.py",
  "status": "PASS", "evidence": f"Local pytest of the same file with the reference: 71 passed ({S}/out/reference_seed0_r4.out). Pyodide: page_smoke in-browser run 'All 71 tests pass' ({O}/page_smoke_project.out)."},
 {"id": "proj-mutants-all", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/*.py (99 files)",
  "status": "FAIL", "evidence": f"tools/mutate_graders.py --unit FC1 --seeds 0-9 -> 'mutate_graders FC1: FAIL (97/99 killed)' ({O}/mutate_graders_0_9_r4.out); seeds 0-19 identical ({O}/mutate_graders_0_19_r4.out). The two survivors are r4c_schedule_stops_at_thirty_periods.py and r4c_discount_exponent_capped_at_thirty.py (rows proj-mutant-schedule-cap-thirty-survivor and proj-mutant-exponent-cap-thirty-survivor).",
  "fix": "Add one grader test with a bond of 40 periods: events() equals oracle_events(10_000, 500, 40) (one event per period 1..40, face in period 40), and bond_price_cents(bond, 400) equals oracle_price(...). Scratch-verified (out/fix40_*.out): the test passes the reference and fails both survivors. Then re-run mutate_graders --unit FC1 --seeds 0-9."},
 {"id": "proj-mutants-v1c-new", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/v1c_*.py (5 student-error mutants, round 1)",
  "status": "PASS", "evidence": f"Killed on seeds 0-9 ({O}/mutate_graders_0_9_r4.out): v1c_price_discounted_at_coupon_rate (test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period), v1c_seller_side_refused (test_seller_receives_cash_at_settlement), v1c_simple_discount_not_compound, v1c_trade_rounded_to_dollars, v1c_yield_guard_missing (test_yield_at_minus_one_is_refused)."},
 {"id": "proj-mutants-v2c-new", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r2c_*.py (4 student-error mutants, round 2)",
  "status": "PASS", "evidence": f"Killed on seeds 0-9 ({O}/mutate_graders_0_9_r4.out): r2c_bond_periods_capped_at_twelve, r2c_events_change_on_second_call (test_repeated_events_calls_agree), r2c_price_cached_on_first_yield (test_one_bond_priced_at_two_yields...), r2c_trade_settles_one_period_early."},
 {"id": "proj-mutants-r3c-killed", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r3c_*.py (round 3)",
  "status": "PASS", "evidence": f"All five r3c mutants killed on seeds 0-9 ({O}/mutate_graders_0_9_r4.out): r3c_discount_factor_float_times_amount, r3c_events_cached_by_face, r3c_price_ten_digits_integral_rounding (test_bond_price_exact_half_above_ten_significant_digits_is_exact), r3c_price_ten_significant_digits, r3c_schedule_stops_at_twenty_periods (test_bond_schedule_longer_than_twenty_periods_is_complete)."},
 {"id": "proj-mutants-v4c-new", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/v4c_*.py (5 student-error mutants, round 4 of the prior campaign)",
  "status": "PASS", "evidence": f"Killed on seeds 0-9: v4c_coupon_truncated_not_rounded, v4c_discount_exponent_one_short, v4c_float_discount_half_up, v4c_trade_sign_not_flipped, v4c_zero_amount_events_dropped ({O}/mutate_graders_0_9_r4.out)."},
 {"id": "proj-mutants-r4c-new", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r4c_*.py (5 student-error mutants written by this verifier, round 4)",
  "status": "PASS", "evidence": f"Written by this verifier with {S}/make_mutants_r4_verif_r4.py. Killed on seeds 0-9 ({O}/mutate_graders_0_9_r4.out): r4c_price_python_round_half_even (test_bond_price_exact_half_cent_rounds_away_from_zero), r4c_trade_amount_through_float (test_trade_cash_flow_is_exact_above_two_to_the_fifty_three), r4c_yield_bound_at_minus_nine_thousand (test_yield_just_above_minus_one_is_accepted). Two survive (see proj-mutants-all)."},
 {"id": "proj-mutant-schedule-cap-thirty-survivor", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r4c_schedule_stops_at_thirty_periods.py vs grader/test_project.py (tests at lines 182-186, 281-315) and project.html line 177",
  "status": "FAIL", "evidence": "Student error: Bond.events() stops at thirty periods, so a 31+ period bond loses its later coupons and its face. Survives every test on seeds 0-9 and 0-19 (mutate_graders output). project.html line 177 states: 'The bond's coupon is paid in each of periods 1 to periods, and its face in the last of them'; line 165 lists only periods < 1 as refused. The page names no upper bound, so the behaviour is stated and the survivor is a FAIL under ruling 9. Longest bond tested is 24 periods (line 304).",
  "fix": "Add the 40-period test described in proj-mutants-all. Its kill is verified in out/fix40_m30.out (1 failed, 71 passed)."},
 {"id": "proj-mutant-exponent-cap-thirty-survivor", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r4c_discount_exponent_capped_at_thirty.py vs grader/test_project.py and project.html line 178",
  "status": "FAIL", "evidence": "Student error: the discount exponent is capped at thirty, so the event in period 31+ is discounted by (1+y)^-30. Survives every test on seeds 0-9 and 0-19. project.html line 178: 'An event in period t is discounted by (1+y)^-t'. No test prices a bond with more than 24 periods, so the cap is not caught.",
  "fix": "Add the 40-period price check described in proj-mutants-all; it fails this mutant (out/fix40_m30x.out: 1 failed, 71 passed)."},
 {"id": "proj-mutant-schedule-cap-survivor", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r3c_schedule_stops_at_twenty_periods.py vs grader/test_project.py lines 304-315",
  "status": "PASS", "evidence": f"Round-3 survivor now killed: r3c_schedule_stops_at_twenty_periods.py killed by test_bond_schedule_longer_than_twenty_periods_is_complete on seed 0 ({O}/mutate_graders_0_9_r4.out). The same test does not catch a thirty-period cap; see proj-mutant-schedule-cap-thirty-survivor."},
 {"id": "proj-mutant-price-digits-survivor", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r3c_price_ten_digits_integral_rounding.py vs grader/test_project.py lines 417-428; project.html line 171",
  "status": "PASS", "evidence": f"Round-3 survivor now killed: r3c_price_ten_digits_integral_rounding.py killed by test_bond_price_exact_half_above_ten_significant_digits_is_exact on seed 0 ({O}/mutate_graders_0_9_r4.out)."},
 {"id": "proj-mutant-periods-13-15-survivor", "check": "2.6-mutation", "location": "grader/test_project.py lines 281-301; project.html line 171",
  "status": "PASS", "evidence": "Round-2 survivor now killed: r2c_bond_periods_capped_at_twelve killed by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period on seed 0 (mutate_graders_0_9_r4.out)."},
 {"id": "proj-mutant-price-cache-survivor", "check": "2.6-mutation", "location": "grader/test_project.py lines 455-468; project.html lines 161, 178",
  "status": "PASS", "evidence": "r2c_price_cached_on_first_yield killed by test_one_bond_priced_at_two_yields_gives_each_yield_its_own_price on seed 0 (mutate_graders_0_9_r4.out)."},
 {"id": "proj-docstring-float-claim", "check": "2.2-numbers / prose", "location": "grader/test_project.py lines 407-410, 431-434",
  "status": "PASS", "evidence": f"{S}/numbers_r4_verif_r4.py output: 1734792/1.0496 = 3305625/2 = 1652812.5 (exact, rounds to 1652813); binary-float discounting gives 1652812.4999999998 (rounds to 1652812). 13/1.04 = 25/2; (1+0.04)**-1 * 13 = 12.499999999999998 (rounds to 12). Both as printed in the docstrings ({O}/numbers_r4.out)."},
 {"id": "proj-named-error-message-values", "check": "2.6-failure-messages", "location": "grader/test_project.py (all assert and pytest.fail sites)",
  "status": "PASS", "evidence": f"{S}/scan_asserts_r4.py -> {O}/scan_asserts_r4.out: 0 asserts without a message; 7 pytest.fail calls; 14 messages contain digits and all name a period range, an input (2**53, 501, 1001, 100 periods, 24 periods) or a property, not an expected answer."},
 {"id": "proj-failure-messages", "check": "2.6-failure-messages", "location": "grader/test_project.py (all assert and pytest.fail sites)",
  "status": "PASS", "evidence": f"Same scan as proj-named-error-message-values ({O}/scan_asserts_r4.out). The new test messages (lines 311, 313) name the property (every period carries its coupon; discounted by its own period) and do not print values. Tests run with --assert=plain, so no comparison detail is shown."},
 {"id": "proj-alternatives", "check": "2.6-alternatives", "location": "ledgers/FC1/alternatives/a1..a5 (a3 docstring changed this round); ledgers/FC1/scripts/FC1-c-r4/alt/; FC1-c-r3/alt; FC1-c-r3/alt_v4",
  "status": "PASS", "evidence": f"{S}/run_alts_r4.py 50 -> {O}/alternatives_0_49_r4.out: a1-a5 pass seeds 0-49; alt/alt1-alt5 and alt_decimal, alt_integer, alt_memo_per_yield, alt_recurrence pass 0-49; alt_decimal_half_up passes 0-49. alt_float_half_up fails all 50 seeds (a float-based wrong answer on the exact rule; it is a mutant per ruling 10, not an alternative). a3 diff is docstring only (a007712f..4eb6788)."},
 {"id": "proj-alternatives-r4-new", "check": "2.6-alternatives", "location": "ledgers/FC1/scripts/FC1-c-r4/alt/alt6_r4_pow_fraction_floor.py",
  "status": "PASS", "evidence": f"New style written by this verifier: discount factor as Fraction(10000, 10000 + yield_bps) ** t, floor-based half-away rounding, validation by isinstance checks. Passes seeds 0-49 ({O}/alternatives_0_49_r4.out)."},
 {"id": "proj-cards-scan-duplicates", "check": "2.7-cards", "location": "course/modules/FC/FC1/cards.json (124 cards)",
  "status": "PASS", "evidence": f"{S}/cards_r4_verif_r4.py -> {O}/cards_scan_r4.out: 124 cards, no duplicate id, front or back; grades T 40, C 15, no grade field on 69 cards (same as round 3)."},
 {"id": "proj-cards-numbers-in-lessons", "check": "2.7-cards", "location": "course/modules/FC/FC1/cards.json; L01-L05.html",
  "status": "PASS", "evidence": f"{S}/cards_refs_r4.py -> {O}/cards_refs_r4.out: every card number and numbered reference (Proposition, Assumption, Remark, Definition, Example, Lab) appears in its lesson, case-insensitively; the 24 initial misses are block ranges ('Assumptions A1 to A3', 'Assumptions B1 to B4') and CSS-numbered misconceptions (course.css lines 938-960 print 'Misconception N.' for the N-th li.misconception) and a regex artefact ('Proposition s'). FC1-c014 and FC1-c122 rows below."},
 {"id": "proj-cards-sample", "check": "2.7-cards", "location": "cards.json FC1-c010, -020, -030, -040, -050, -060, -070, -080, -090, -100, -110, -120",
  "status": "PASS", "evidence": "Sampled 12 cards read against lesson text: c010 (6,861.89 = 1000 x (1-0.9^11)/0.1 = 6861.8940391, half up; Example 3.3 present in L01); c020 (Assumption 1.3 present in L02); c030 (hand reading of register entries, Example 3.1); c040 (Definition 2.1); c050 (Proposition 3.2 in L03); c060 (Remark 1.2 in L04); c070 (misconception 1, CSS-numbered); c080 (Proposition 2.2 in L05); c090 (Section 4); c100 (Proposition 2.3 in L04, share conservation G = R + 2X + C at c066 consistent); c110 (A2 is inside Assumption 2.0 in L01, lines 73 and 320); c120. No contradiction found."},
 {"id": "proj-cards-changed-subjects", "check": "2.7-cards", "location": "cards.json FC1-c013, -019, -058, -066, -078, -114, -120, -121, -122, -123, -124",
  "status": "PASS", "evidence": CARRY + " FC1-c013, -019, -058, -066, -078, -114, -120, -121, -123, -124 (cards.json diff a007712f..4eb6788 touches only c014 and c122). They were printed and read in full this round for form; lesson-text spot checks: c013 cites Proposition 4.1 (L01) and c066 cites Proposition 2.3 (L04, the identity G = R + 2X + C). FC1-c122 is re-verified in proj-cards-c122-equity-after-loss."},
 {"id": "proj-cards-c014-lab-true", "check": "2.7-cards", "location": "cards.json FC1-c014 (L01), changed this round",
  "status": "PASS", "evidence": "Changed this round (back text shortened, the 6.8619 clause removed). The lesson's expected output for Lab 1 Part A contains 'the partial sums equal the closed form exactly for n = 0 to 10: True' and Proposition 3.1 (data-grade T, L01) is cited; grade T is correct because the claim is proved on the page."},
 {"id": "proj-cards-c122-equity-after-loss", "check": "2.7-cards", "location": "cards.json FC1-c122 (L01), changed this round",
  "status": "PASS", "evidence": "Changed this round (the Remark 4.2 sentence removed). The card's hypothesis 'Under Assumption 4.0' matches L01 Assumption 4.0 (deposits keep their value). Its answer 'exactly when lambda <= E' matches Proposition 4.1 in L01 (data-grade T): 'the equity is nonnegative after the loss if and only if lambda <= E'. Remark 4.2 is still in L01 but no longer cited by the card."},
 {"id": "proj-cards-citation-R3", "check": "2.7-cards", "location": "cards.json FC1-c054 (L03)",
  "status": "PASS", "evidence": f"{O}/cards_refs_r4.out: no unmatched reference on FC1-c054; card unchanged since round 3 (cards.json diff a007712f..4eb6788 touches only c014 and c122)."},
 {"id": "proj-cards-citation-R2", "check": "2.7-cards", "location": "cards.json FC1-c089 (L05)",
  "status": "PASS", "evidence": f"{O}/cards_refs_r4.out: no unmatched reference on FC1-c089; card unchanged since round 3."},
 {"id": "proj-cards-citation-scan", "check": "2.7-cards", "location": "cards.json block references",
  "status": "PASS", "evidence": f"{O}/cards_refs_r4.out and {O}/cards_scan_r4.out: references resolve in their lesson (see proj-cards-numbers-in-lessons). No card cites a key that is not in references/references.json (cards carry no bibliographic keys)."},
 {"id": "proj-cards-grades", "check": "2.3-grades", "location": "cards.json grade fields vs lesson data-grade attributes",
  "status": "PASS", "evidence": f"{O}/cards_scan_r4.out: grade T 40, C 15 (unchanged counts; c014 and c122 are T and the lesson claims they cite are data-grade T). Cards without a grade field: 69 (as in round 3)."},
 {"id": "proj-spec-scope-vs-curriculum", "check": "2.6-scope", "location": "project.html lines 157, 161; curriculum/02-economics-finance-core.yaml lines 388-395; plans/FINAL-ARCHITECT-RULINGS.md item 5",
  "status": "PASS", "evidence": "The brief (yaml 393) reads 'Futures, swaps and options follow in FC2'; project.html line 157 says the project uses none of them and FC2 is 'Derivatives' (yaml line 397 'Derivatives Fundamentals'). Ruling 5 limits the project to cash instruments. Curriculum yaml is unchanged since round 3."},
 {"id": "proj-terminology-short-holder", "check": "2.2-terms", "location": "project.html lines 54, 179; grader/reference.py docstring line 10",
  "status": "PASS", "evidence": "'holder' is defined on first use (line 54, parenthesis: 'the party that owns the bond'); the sign convention on line 179 uses the holder's side consistently; reference.py line 10-11 states the same convention."},
 {"id": "proj-prose-banned-phrases", "check": "2.9-prose", "location": "course/modules/FC/FC1/project.html; cards.json; grader/*.py",
  "status": "PASS", "evidence": "Banned-phrase scan (BUILDER_RULES 1.3-1.4: TODO, TBD, lorem, for brevity, beyond the scope, left as an exercise, it is important to note, studies show, obviously, clearly, it can be shown, historically, roughly, and others) on project.html: 0 hits. Hits in cards.json ('as well' matches 'as we'; the math ellipsis in c-card 682 is not omitted content) and in test_project.py ('11052.63...' numeric truncation; Callable[..., None] type notation) are not banned uses."},
 {"id": "proj-scope-words", "check": "2.9-prose", "location": "project.html lines 163, 171, 176, 180, 184, 276; grader/test_project.py lines 9-13",
  "status": "PASS", "evidence": "'every output' (163): all outputs are checked as ints by checked_events/checked_int (lines 96-114). 'every named condition with its boundary on each side' (171): lines 217-625. 'No discounted term is rounded' (176): the price is one Fraction sum, rounded once (reference.py line 70). 'Events... every' (180) and 'the autograder checks them' (276): verified against the test names listed."},
 {"id": "proj-terms-before-definition", "check": "2.9-terms", "location": "project.html lines 38, 54, 58, 178",
  "status": "PASS", "evidence": "Face, coupon, settlement period (dfn, line 54), event (line 54), holder (line 54) are defined before use; present-value and discount-factor are linked concepts from M1 (line 58, 178). 'Reconciliation' (line 38) is plain English, not a term of the module."},
 {"id": "proj-notation", "check": "2.4-notation", "location": "project.html lines 58, 106, 178; notation/notation.json",
  "status": "PASS", "evidence": "Symbols on the page: y (per-period yield, line 58 'y = 400/10000') and t (period index, lines 106 and 178). notation/notation.json lists 8 symbols (T, R_f, gamma_3, ...); none is y or t, and none collides with the page's meanings. Macros used: none on this page."},
 {"id": "proj-footer-claim", "check": "2.9-prose", "location": "project.html line 341 footer",
  "status": "PASS", "evidence": f"'The autograder runs in your browser; nothing you write leaves it.' Page smoke reports no external requests ({O}/page_smoke_project.out); grader.js runs pytest in Pyodide (course/assets/js/grader.js, unchanged since round 3)."},
 {"id": "proj-saved-as-you-type", "check": "2.9-prose", "location": "project.html line 301",
  "status": "PASS", "evidence": "course/assets/js/grader.js lines 59-61: on each 'input' event the editor value is written with store.put('files', draftKey, editor.value) after a 400 ms debounce, and line 34-43 restores it on load (IndexedDB via store.js). project.html line 301 matches. Re-checked this round; grader.js unchanged since round 3."},
 {"id": "proj-references-reading-list", "check": "2.1-citations", "location": "project.html lines 321-333 (data-cite keys)",
  "status": "PASS", "evidence": "Keys mishkin2021economics and harris2002trading exist in references/references.json (560 entries, offline integrity 0 problems: " + O + "/verify_refs_offline.out). The page attributes no statement to either (line 323)."},
 {"id": "proj-cited-year-conflicts", "check": "2.1-citations", "location": "references/references.json (two keys); curriculum/02-economics-finance-core.yaml lines 384-385",
  "status": "PASS", "evidence": "Registry years: mishkin2021economics 2021; harris2002trading 2002 (years [2002, 2023]). Curriculum strings: 'Mishkin ... 13th ed. (2022)' and 'Harris, Trading and Exchanges (2003)'. The page cites by key with no year (architect decision). Conflicts recorded in registry_flags, not on the page."},
 {"id": "proj-data-simulated", "check": "2.8-data", "location": "project.html lines 45, 54, 72, 159; grader/instance.py docstring and label",
  "status": "PASS", "evidence": "No data file is read (line 54 'No file is read'). instance.py line 31 label 'SIMULATED bond and trade, seed N: not market data'; line 6 'Nothing here is market data'. Lab code comments say SIMULATED (lines 72, 120). No dataset is in data-files."},
 {"id": "proj-reference-deployment", "check": "2.6-deployment", "location": "course/modules/FC/FC1/grader/reference.py",
  "status": "PASS", "evidence": "Ruling 4 (plans/FINAL-ARCHITECT-RULINGS.md item 4): the repository has no deploy step yet, and the rule is recorded for the owner. reference.py docstring line 4 says so. Not a defect; does not fail the slice."},
]

# Rows of this slice that the verifier did not re-run and carries (none beyond those labelled CARRY above).
statuses = [r["status"] for r in rows]
counts = {s: statuses.count(s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"

fragment = {
  "unit": "FC1",
  "slice": "c",
  "round": 4,
  "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 4 (did not build FC1)",
  "pin": PIN,
  "base": BASE,
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyD4-FC1-c",
  "scratch": "/tmp/fc1c_r4_collect, /tmp/fc1c_r4_starter, /tmp/fc1c_r4_fix, /tmp/fc1c_r4_alts (copies of grader files; the scripts that made them are under ledgers/FC1/scripts/FC1-c-r4/)",
  "verified_at": "2026-11-03T16:41:58+00:00",
  "verdict": verdict,
  "rows": rows,
  "mutants": mutants,
  "registry_flags": [
    "mishkin2021economics: registry year 2021 (references/references.json); curriculum/02-economics-finance-core.yaml:384 says 'Mishkin ... 13th ed. (2022)'. Page cites the key only (architect decision). For the curriculum owner; not an FC1-c defect.",
    "harris2002trading: registry year 2002 (years [2002, 2023]); curriculum/02-economics-finance-core.yaml:385 says 'Harris, Trading and Exchanges (2003)'. Page cites the key only. For the curriculum owner.",
  ],
  "freshness_flags": [],
  "notes": (
    "Round 4 on 4eb6788 (delta a007712f..4eb6788 read hunk by hunk). Changed in the slice: project.html (lines 45, 163, 171, 176, 189), grader/test_project.py (new tests at lines 304-315 and 417-428; docstring at 281-287), cards.json (FC1-c014 and FC1-c122 backs shortened), ledgers/FC1/alternatives/a3 (docstring only), and new mutants r3c_* tracked, v4c_* tracked. Tests/labs/FC1, starter.py, reference.py, instance.py, lessons, references, notation, curriculum and tools are byte-identical to round 3. "
    "Round-3 non-PASS rows re-verified from scratch: proj-mutants-all (still FAIL, now 97/99 with two new survivors), proj-mutant-schedule-cap-survivor (now killed by test_bond_schedule_longer_than_twenty_periods_is_complete), proj-mutant-price-digits-survivor (now killed by test_bond_price_exact_half_above_ten_significant_digits_is_exact). "
    "The two new survivors are student errors that cap the schedule or the discount exponent at thirty periods; project.html line 177 and 178 state the behaviour for every period, and no test prices a bond longer than 24 periods. A scratch 40-period test kills both and passes the reference (out/fix40_*.out). "
    "Five new student-error mutants written this round (r4c_*): three are killed by existing tests, two are the survivors. One new alternative (alt6) passes seeds 0-49. Collect count 71 in a scratch copy. Hours: verifier estimate 12.5-19 h against 20 h declared (within 30%). "
    "Not checked: the full pytest suite (only -k FC1 in test_labs, test_run_labs, test_page_checks, test_page_smoke: 8 passed); build_site --check, render_curriculum and fetch_data --check (no input of those tools changed in the delta); a live verify_refs (offline only: 560 entries, 0 problems); Pyodide execution of the new mutants (the browser suite runs the reference only); a line-by-line re-read of all 124 cards (the full mechanical scan plus 12 sampled and 10 changed cards were read in full); the rung-4 stretch text against an external source (none is cited). "
    "Workspace note: ledgers/FC1/scripts/FC1-c-r4/ already contained tracked files from commit 04626e99 when this round started. Those tracked files were left untouched (the three names I first wrote over were restored with git checkout); this round's scripts carry the suffix _verif_r4 or are new names. The fragment ledgers/FC1/FC1-c.json was replaced by this round's fragment, as the round instructions specify."
  ),
  "summary": (
    f"Round 4 on 4eb6788. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
    f"Mutants: {len(mutants) - len(survivors)}/{len(mutants)} killed on seeds 0-9 (and 0-19); survivors: {', '.join(survivors)}. "
    f"Verdict {verdict}. FAIL rows: proj-mutants-all, proj-mutant-schedule-cap-thirty-survivor, proj-mutant-exponent-cap-thirty-survivor; the fix for all three is one 40-period grader test (verified in scratch)."
  ),
}

out_path = ROOT / "ledgers/FC1/FC1-c.json"
out_path.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out_path, "rows", len(rows), counts, "mutants", len(mutants), "survivors", survivors, "verdict", verdict)
