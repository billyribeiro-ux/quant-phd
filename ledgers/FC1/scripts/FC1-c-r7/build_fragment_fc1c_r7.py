"""Round-7 verifier (FC1-c): writes ledgers/FC1/FC1-c.json from the outputs under ledgers/FC1/scripts/FC1-c-r7/out/.

Mutant rows are parsed from out/mutate_graders_0_19_r7.out (tools/mutate_graders.py output), so every mutant row is the
tool's own verdict. Row verdicts are the verifier's, written below with the command or script that produced each one.
Usage: python3 -I build_fragment_fc1c_r7.py <checkout>   (run from the checkout root with the repository's tools on sys.path)
"""
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
OUT = ROOT / "ledgers/FC1/scripts/FC1-c-r7/out"
MUT = (ROOT / "ledgers/FC1/mutants").glob("*.py")
mutate_text = (OUT / "mutate_graders_0_19_r7.out").read_text(encoding="utf-8")
mut_lines = [l for l in mutate_text.splitlines() if l.startswith(("KILLED ", "SURVIVED "))]
mutants = []
mutant_survivors = []
for line in mut_lines:
    status, rest = line.split(" ", 1)
    name, rest = rest.split(": ", 1)
    description, killer = rest.rsplit(" -> ", 1)
    if killer == "None":
        killed_by = None
    else:
        test, seed = re.match(r"(\S+) \(seed (\d+)\)", killer).groups()
        killed_by = f"{test} (seed {seed})"
    mutants.append({"id": name[:-3], "description": description, "killed_by": killed_by})
mutant_survivors = [m for m in mutants if not m['killed_by']]
assert len(mutants) == len(list(ROOT.joinpath("ledgers/FC1/mutants").glob("*.py"))), "a mutant has no tool line"

def ids_killed(prefix):
    found = [m for m in mutants if m["id"].startswith(prefix)]
    return found, all(m["killed_by"] for m in found)

def killed_row(row_id, prefix, location, text):
    found, ok = ids_killed(prefix)
    names = ", ".join(m["id"] for m in found)
    killers = "; ".join(f"{m['id']} -> {m['killed_by']}" for m in found)
    return {"id": row_id, "check": "2.6-mutation", "location": location,
            "status": "PASS" if ok and found else "FAIL",
            "evidence": f"{text} Tool verdict in out/mutate_graders_0_19_r7.out: {killers}. Mutants: {names}.",
            **({} if ok and found else {"fix": "Kill the surviving mutant (see the row that names it)."})}

def row(row_id, check, location, status, evidence, fix=None):
    r = {"id": row_id, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

EX = "ledgers/FC1/scripts/FC1-c-r7/out"
rows = []
rows.append(row("proj-check-projects", "2.6-structure", "course/modules/FC/FC1/project.html", "PASS",
    f"tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS', exit 0 ({EX}/check_projects.out)."))
rows.append(row("proj-check-pages", "2.9-structure", "course/modules/FC/FC1/project.html", "PASS",
    f"tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', exit 0 ({EX}/check_pages.out)."))
rows.append(row("proj-check-dag", "2.9-dag", "project.html; curriculum/curriculum.json concepts", "PASS",
    f"tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS' ({EX}/check_dag.out). The two linked concepts, present-value and discount-factor, map to module M1 in curriculum.json (inside the FC1 closure, plan section 0.1)."))
rows.append(row("proj-run-labs", "2.5-labs", "project.html Labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py", "PASS",
    f"tools/run_labs.py --unit FC1 --page project -> 'run_labs FC1: PASS (3/3)'; --unit FC1 -> 'PASS (8/8)' ({EX}/run_labs_project.out, {EX}/run_labs_fc1.out)."))
rows.append(row("proj-page-smoke", "2.9-smoke", "course/modules/FC/FC1/project.html", "PASS",
    f"tools/page_smoke.py --unit FC1 --pages project -> 'page_smoke modules/FC/FC1/project.html: PASS', exit 0; in-browser grader 'All 78 tests pass' ({EX}/page_smoke_project.out)."))
rows.append(row("proj-run-graders", "2.6-autograde-reference", "grader/reference.py, test_project.py, instance.py, starter.py", "PASS",
    f"tools/run_graders.py --unit FC1 --seeds 0-49 -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.2 s)' ({EX}/run_graders_0_49.out)."))
rows.append(row("proj-lint-types", "2.6-lint", "course/modules/FC/FC1/grader/*.py; tests/labs/FC1/", "PASS",
    f"ruff check . -> 'All checks passed!' ({EX}/ruff_check.out); ruff format --check on FC1 pages, labs and ledgers -> '12 files already formatted' ({EX}/ruff_format_fc1.out); mypy --no-incremental -> 'Success: no issues found in 385 source files' ({EX}/mypy.out)."))
rows.append(row("proj-lab1-numbers", "2.2-numbers", "project.html lines 58, 97-100 (Lab 1)", "PASS",
    f"Recomputed in exact Fractions by ledgers/FC1/scripts/FC1-c-r7/numbers_fc1c_r7.py ({EX}/numbers_fc1c_r7.out): events [(1, 5000), (2, 5000), (3, 105000)]; exact present value 102775.091033 (to 6 dp); price 102775. Matches the page's hypothesis and expected block."))
rows.append(row("proj-lab2-blanks", "2.5-labs", "project.html lines 133, 140, 149 (Lab 2)", "PASS",
    "Diff of the page code against tests/labs/FC1/lab-FC1-project-2.py: exactly two lines differ, the price line with the exponent blank ('___' vs 'period') and the trade-event line with the cash-flow blank ('___' vs '-side * quantity * price_cents'), which are the two blanks; the printed lines match Lab 1 (run_labs completion check PASS, run_labs_project.out)."))
rows.append(row("proj-lab3-fixture-values", "2.2-numbers", "project.html lines 198-276 (Lab 3)", "PASS",
    f"Every printed fixture value recomputed exactly ({EX}/numbers_fc1c_r7.out, {EX}/docstring_numbers_r7.out): A 10000 (10500/1.05); B 11053 with exact 210000/19 = 11052.6316; C [(1, 5001), (2, 15002)]; D [(1, 2)]; rounding case events [(1, 500), (2, 500), (3, 10500)], price 10278 rounded once, 10277 term by term; E (2, -98500); F [(1, 1)] price 1; G [(1, 10001)] price 5001 (exact 5000.5). Page code equals twin (exact string comparison, this round)."))
rows.append(row("proj-rounding-fixture-terms", "2.2-numbers", "project.html line 193; grader/test_project.py lines 394-401", "PASS",
    f"Exact present value 10277.509103 rounds once to 10278; the terms 480.769231, 462.278107, 9334.461766 round one by one to 481 + 462 + 9334 = 10277 ({EX}/docstring_numbers_r7.out)."))
rows.append(row("proj-lab3-claim-using-functions", "2.5-labs", "project.html line 198 vs tests/labs/FC1/lab-FC1-project-3.py", "PASS",
    "The Lab 3 hypothesis says the bond uses the functions of this lab and exact arithmetic for trade and exact values; the twin defines bond_events, bond_price and term_by_term_price with Fraction, and the trade is an int product (twin lines 215-259). Page code equals twin."))
rows.append(row("proj-expected-equals-output", "2.5-labs", "project.html expected blocks lines 97-100, 145-148, 263-275", "PASS",
    f"run_labs compares each expected block with the twin's output under the page's tolerance rule (coursekit.compare_output: 1e-6 * (1 + |expected|), about 0.1 cent on 102775). ({EX}/run_labs_project.out: PASS (3/3))."))
rows.append(row("proj-hours-arithmetic", "2.9-hours", "project.html table#hours lines 286-293; data-hours-project line 34", "PASS",
    "1 + 2 + 5 + 4 + 2 + 3 + 3 = 20 = data-hours-project = the hub's 20 h project; with 50 h of lessons (index.html) the module is 70 h (curriculum/02-economics-finance-core.yaml line 366)."))
rows.append(row("proj-hours-rationale-rows", "2.9-hours", "project.html table#hours lines 286-293", "PASS",
    "All seven component rows and the total carry a rationale cell (read in full)."))
rows.append(row("proj-hours-verifier-estimate", "2.6-hours", "project.html table#hours lines 286-293", "PASS",
    "Ruling applies: hours are design targets; only arithmetic inconsistencies fail, and none is found (row proj-hours-arithmetic). Not re-estimated."))
rows.append(row("proj-ladder", "2.6-ladder", "project.html lines 41-50, 52-151, 153-172, 312-319", "PASS",
    "Rung 1 is a fully solved annotated worked example (Lab 1); rung 2 is a completion problem with two blanks and an instant check; rung 3 is the specification with autograder; rung 4 is open-ended and not graded (lines 312-319)."))
rows.append(row("proj-spec-interface", "2.6-spec", "project.html line 161; grader/starter.py", "PASS",
    "Names and signatures in starter.py (lines 16-40) match line 161: Bond(face_cents, coupon_bps, periods).events(); bond_price_cents(bond, yield_bps); CashTrade(quantity, price_cents, side, settlement_day).events()."))
rows.append(row("proj-named-conditions", "2.6-spec", "project.html lines 163-167; grader/test_project.py", "PASS",
    "All eight named conditions are tested on both sides of the boundary: periods 0 refused / 1 accepted (lines 215-229); face 0 and -1 refused / 1 accepted (232-247); coupon -1 refused / 0 accepted (258-265); yield -10000 and -20000 refused / -9999 accepted (494-508); quantity 0 and -1 refused / 1 accepted (554-569); price -1 refused / 0 accepted (603-613); side 0, 2, -2, 3, -3 refused / +1 and -1 accepted (616-646); settlement 0 and -1 refused / 1 accepted (649-664)."))
rows.append(row("proj-test-count", "2.6-spec", "project.html line 171; grader/test_project.py", "PASS",
    f"Page says '78 checks'; pytest --collect-only on the checkout's grader files gives '78 tests collected' ({EX}/collect_only_r7.out)."))
rows.append(row("proj-starter-fails", "2.6-autograde", "grader/starter.py", "PASS",
    f"Suite on starter.py: '76 failed, 2 passed' ({EX}/starter_run_r7.out). The two passing tests accept any exception by design (test_non_whole_face_is_refused_or_gives_ints, test_bool_periods_is_not_quietly_accepted_as_a_number). The naming of the failures is row proj-starter-unwrapped-new-tests and proj-starter-message-leaks-answer."))
rows.append(row("proj-instances", "2.6-autograde", "grader/instance.py, seeds 0-19", "PASS",
    "Scripted for seeds 0-19: the bond price and the trade event differ for all 20 seeds (price and trade pair: 20 of 20 distinct); every case is valid (the reference passes seeds 0-49). Labelled SIMULATED in its docstring and label field (numbers_fc1c_r7 / docstring_numbers_r7 outputs)."))
rows.append(row("proj-silence-purity", "2.6-autograde", "grader/test_project.py test_the_module_prints_nothing, test_refused_inputs_print_nothing_before_they_raise", "PASS",
    "Both tests pass on the reference (run_graders and pytest 78 passed) and the page states the rule (project.html line 163)."))
rows.append(row("proj-same-suite-pyodide-pytest", "2.6-autograde", "grader/test_project.py", "PASS",
    f"Local pytest with the documented flags: '78 passed' on the reference; the in-browser grader in page_smoke reports 'All 78 tests pass' ({EX}/pytest_fc1_r7.out, {EX}/page_smoke_project.out)."))
rows.append(row("proj-mutants-all", "2.6-mutation", "ledgers/FC1/mutants/*.py (116 files)", "FAIL" if mutant_survivors else "PASS", f"tools/mutate_graders.py --unit FC1 --seeds 0-19 -> 'mutate_graders FC1: {'FAIL' if mutant_survivors else 'PASS'} ({len(mutants) - len(mutant_survivors)}/{len(mutants)} killed)' (out/mutate_graders_0_19_r7.out). Survivors: {', '.join(m['id'] for m in mutant_survivors) or 'none'}.", None if not mutant_survivors else "Kill the survivor listed: see proj-mutant-periods-cap-1000-survivor."))
rows.append(killed_row("proj-mutants-v1c-new", "v1c_", "ledgers/FC1/mutants/v1c_*.py", "Student-error mutants, earlier verifier rounds."))
rows.append(killed_row("proj-mutants-v2c-new", "r2c_", "ledgers/FC1/mutants/r2c_*.py", "Student-error mutants, earlier verifier rounds."))
rows.append(killed_row("proj-mutants-r3c-killed", "r3c_", "ledgers/FC1/mutants/r3c_*.py", "Student-error mutants, earlier verifier rounds."))
rows.append(killed_row("proj-mutants-v4c-new", "v4c_", "ledgers/FC1/mutants/v4c_*.py", "Student-error mutants, earlier verifier rounds."))
rows.append(killed_row("proj-mutants-r4c-new", "r4c_", "ledgers/FC1/mutants/r4c_*.py", "Student-error mutants, earlier verifier rounds."))
rows.append(killed_row("proj-mutants-r5c-new", "r5c_", "ledgers/FC1/mutants/r5c_*.py", "Student-error mutants, round 5."))
rows.append(killed_row("proj-mutants-r6c-killed", "r6c_", "ledgers/FC1/mutants/r6c_*.py", "Round-6 verifier mutants, all now killed."))
rows.append(killed_row("proj-mutants-r7c-new", "r7c_", "ledgers/FC1/mutants/r7c_*.py", "Round-7 verifier mutants (five written this round; one survives, see proj-mutant-periods-cap-1000-survivor)."))

def one(mutant_id):
    m = [x for x in mutants if x["id"] == mutant_id]
    assert len(m) == 1, mutant_id
    return m[0]

prev_survivors = [
    ("proj-mutant-schedule-cap-thirty-survivor", "r4c_schedule_stops_at_thirty_periods", "grader/test_project.py line 318 (40-period test)"),
    ("proj-mutant-exponent-cap-thirty-survivor", "r4c_discount_exponent_capped_at_thirty", "grader/test_project.py line 318"),
    ("proj-mutant-schedule-cap-survivor", "r3c_schedule_stops_at_twenty_periods", "grader/test_project.py lines 304-315"),
    ("proj-mutant-price-digits-survivor", "r3c_price_ten_digits_integral_rounding", "grader/test_project.py lines 431-442"),
    ("proj-mutant-price-cache-survivor", "r2c_price_cached_on_first_yield", "grader/test_project.py lines 469-482"),
    ("proj-mutant-price-epsilon-survivor", "r5c_price_rounded_with_epsilon", "grader/test_project.py line 455"),
    ("proj-mutant-yield-100-survivor", "r5c_yield_above_one_hundred_percent_refused", "grader/test_project.py line 510"),
    ("proj-mutant-schedule-cap-forty-survivor", "r6c_schedule_stops_at_forty_periods", "grader/test_project.py line 318"),
    ("proj-mutant-exponent-cap-forty-survivor", "r6c_discount_exponent_capped_at_forty", "grader/test_project.py line 318"),
    ("proj-mutant-yield-200-survivor", "r6c_yield_above_two_hundred_percent_refused", "grader/test_project.py line 510"),
    ("proj-mutant-settlement-cap-100-survivor", "r6c_settlement_day_above_one_hundred_refused", "grader/test_project.py line 814"),
    ("proj-mutant-decimal-40-digits-survivor", "r6c_price_decimal_forty_significant_digits", "grader/test_project.py line 822"),
    ("proj-mutant-decimal-28-digits-kill", "r6c_price_default_decimal_28_digits", "grader/test_project.py line 822"),
]
for row_id, mid, loc in prev_survivors:
    m = one(mid)
    rows.append(row(row_id, "2.6-mutation", loc, "PASS" if m["killed_by"] else "FAIL",
        f"Round-6 survivor, now killed on seeds 0-19: {m['id']} -> {m['killed_by']} (out/mutate_graders_0_19_r7.out). "
        "Round-6 FAIL re-verified from scratch this round." if m["killed_by"] else "Still alive.",
        None if m["killed_by"] else "Add a test that kills this mutant."))

rows.append(row("proj-mutant-periods-cap-1000-survivor", "2.6-mutation",
    "ledgers/FC1/mutants/r7c_periods_refused_above_one_thousand.py vs grader/test_project.py (no test has more than 100 periods)",
    "FAIL",
    "Student error: Bond refuses more than 1000 periods. SURVIVED on seeds 0-19 (out/mutate_graders_0_19_r7.out). "
    "The page states the behaviour this mutant violates: project.html line 177, 'The bond's coupon is paid in each of periods 1 to periods, "
    "and its face in the last of them'; line 165 names only 'periods less than 1' as refused. The suite's largest bond has 100 periods (line 791). "
    "Refusing a 1001-period bond is therefore not caught.",
    "Add a test for a 1001-period bond: Bond(10_000, 500, 1_001).events() equals oracle_events(10_000, 500, 1_001), and bond_price_cents at 400 bps equals "
    "oracle_price of those events. A validated version of this and the three fixes of rows proj-starter-* is in "
    "ledgers/FC1/scripts/FC1-c-r7/proposed_fix_r7.py: applied to a scratch copy it gives 79 tests, 116/116 mutants killed on seeds 0-19 "
    "(out/kill_check_proposed_fix_r7.out), the reference passing, and all eight alternatives passing. project.html line 171 would then read '79 checks' and name the 1001-period bond."))

rows.append(row("proj-mutant-r7c-coupon-half-even", "2.6-mutation", "ledgers/FC1/mutants/r7c_coupon_rounded_half_even.py", "PASS",
    f"Student error: coupon rounded half to even. KILLED: {one('r7c_coupon_rounded_half_even')['killed_by']} (out/mutate_graders_0_19_r7.out)."))
rows.append(row("proj-mutant-r7c-discount-float", "2.6-mutation", "ledgers/FC1/mutants/r7c_discount_factor_float_then_exact.py", "PASS",
    f"Student error: float discount factors. KILLED: {one('r7c_discount_factor_float_then_exact')['killed_by']}."))
rows.append(row("proj-mutant-r7c-price-cap-1m", "2.6-mutation", "ledgers/FC1/mutants/r7c_price_refused_above_one_million_cents.py", "PASS",
    f"Student error: a valid large price refused. KILLED: {one('r7c_price_refused_above_one_million_cents')['killed_by']}. The kill comes from the learner's seeded case (a face up to 50,000.00 is valid, line 159 and page line 161); no dedicated large-price test exists, which the page does not require."))
rows.append(row("proj-mutant-r7c-hard-coded-answer", "2.6-mutation", "ledgers/FC1/mutants/r7c_price_is_seed_zero_answer_constant.py", "PASS",
    f"Hard-coded seed-0 answer returned for every bond. KILLED: {one('r7c_price_is_seed_zero_answer_constant')['killed_by']}."))
rows.append(row("proj-alternatives", "2.6-alternatives", "ledgers/FC1/alternatives/a1..a5", "PASS",
    f"Each alternative run against the current suite on seeds 0-19 (scripts/run_alts_r7.sh -> {EX}/alternatives_0_19_r7.out): a1 20/20, a2 20/20, a3 20/20, a4 20/20, a5 20/20 pass."))
rows.append(row("proj-alternatives-r4-new", "2.6-alternatives", "ledgers/FC1/scripts/FC1-c-r4/alt/alt6_r4_pow_fraction_floor.py", "PASS",
    f"alt6 20/20 on seeds 0-19 ({EX}/alternatives_extra_r7.out)."))
rows.append(row("proj-alternatives-r6-new", "2.6-alternatives", "ledgers/FC1/scripts/FC1-c-r6/alt/alt7..alt9", "PASS",
    f"alt7 (Decimal at 60 digits, half up), alt8 (one integer ratio over (10000+yield)**T), alt9 (running discount factor): 20/20 each on seeds 0-19 ({EX}/alternatives_extra_r7.out)."))
rows.append(row("proj-alternatives-r7-new", "2.6-alternatives", "ledgers/FC1/scripts/FC1-c-r7/alt/alt10..alt12", "PASS",
    f"Written this round: alt10 (Fraction powers of 10000/(10000+yield), integer half-up coupon), alt11 (Decimal at 200 digits, ROUND_HALF_UP), alt12 (repeated exact division by 1+y, floor(|x|+1/2) rounding). 20/20 each on seeds 0-19 ({EX}/alternatives_0_19_r7.out)."))
rows.append(row("proj-docstring-float-claim", "2.2-numbers", "grader/test_project.py lines 421-452 (docstrings)", "PASS",
    f"Scripted: 13 * (1 + 0.04) ** -1 = 12.499999999999998 (rounds to 12) and 1734792 * (1 + 0.0496) ** -1 = 1652812.4999999998 ({EX}/docstring_numbers_r7.out)."))
rows.append(row("proj-test-docstring-hand-numbers", "2.2-numbers", "grader/test_project.py lines 205-212, 421-461, 504-516, 592-600, 791-829 (docstrings and asserts)", "PASS",
    f"Recomputed in exact Fractions ({EX}/docstring_numbers_r7.out): 1734792/1.0496 = 3305625/2 = 1652812.5 (rounds to 1652813); 13/1.04 = 25/2; (10**17+4999)/10000 = 10**13 + 0.4999 (rounds to 10**13); 299985000.5 - 1/(2*1000300030001) exact equality with the claimed form; (2**40+1)*9851 = 10831289045231227 (odd, above 2**53); 10500/4 = 2625; 10500/2.5 = 4200; every docstring number checked here matches its recomputation; no docstring states a number the test does not check."))
rows.append(row("proj-named-error-message-values", "2.6-messages", "grader/test_project.py (every assert and pytest.fail site)", "PASS",
    f"Under the documented flags (QF_SEED=0 pytest -q -p no:cacheprovider --assert=plain -W error) a failing run prints only the message: the failure of r7c_price_is_seed_zero_answer_constant shows 'E   AssertionError: <message>' lines and no expected value (grep for 4281937 finds 0 lines; {EX}/flags_probe_mutant_failure_output_r7.out)."))
rows.append(row("proj-failure-messages", "2.6-messages", "grader/test_project.py assert messages", "PASS",
    "Each assert and pytest.fail message names the violated property (for example 'the price is the sum of each event discounted by (1 + y) ** -t, rounded once'), and no assert message carries a hidden expected value (grep of every message). Starter failures are covered by the two FAIL rows below."))
rows.append(row("proj-starter-message-leaks-answer", "2.6-messages", "grader/test_project.py lines 456-457, 593 (first docstring lines, shown as the failure summary on the starter)", "FAIL",
    f"The starter's failure summary is the first line of each test docstring. Two hidden tests print their answers there: test_bond_price_just_under_a_half_cent_rounds_down ('...the exact price is 299985000 plus 1/2 minus', so 299985000 is shown; {EX}/starter_run_r7.out line 81) and test_trade_cash_flow_is_exact_above_two_to_the_fifty_three ('...is (2**40 + 1) * 9851 = 10831289045231227 cents', line 115). test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield (line 446) also shows its exact value 25/2 (line 79). The rule is 'never leak the answer'.",
    "Reword those first docstring lines so they state the property without the expected value, moving the arithmetic to line 2 or later. Checked on a scratch copy: with the rewording the starter output contains none of 299985000, 10831289045231227, 25/2, 2625 (ledgers/FC1/scripts/FC1-c-r7/out/starter_run_proposed_fix_r7.out)."))
rows.append(row("proj-starter-unwrapped-new-tests", "2.6-messages", "grader/test_project.py lines 786-788 (wrapper loop) and 791-829 (four tests added after it)", "FAIL",
    f"_named_when_unimplemented (lines 765-788) is applied by a loop at line 786, which runs before the four tests added this round (lines 791, 806, 814, 822). Those four are not wrapped: on the starter they fail with a raw 'NotImplementedError: Bond' traceback and print no property name ({EX}/starter_run_r7.out lines 148-185), instead of the required failure that names the property.",
    "Move the wrapper loop (lines 786-788) to the end of the module, after the last test. Checked on a scratch copy: all 79 tests then fail on the starter with a named message (starter_run_proposed_fix_r7.out: 77 failed and 2 passed, 0 NotImplementedError lines)."))
rows.append(row("proj-cards-scan-duplicates", "2.7-cards", "course/modules/FC/FC1/cards.json (137 cards)", "PASS",
    f"137 ids, all unique; no duplicate front and no duplicate back ({EX}/cards_numbers_r7.out). Near-duplicate fronts (e.g. c110/c111, c107/c113) are distinct questions about different assumptions; near-duplicate backs c058/c121 (buy vs sell stop), c132/c133 (best bid vs best ask), c036/c137, c013/c122 are distinct claims. The id gap FC1-c134 is the card removed in this delta."))
rows.append(row("proj-cards-numbers-in-lessons", "2.7-cards", "course/modules/FC/FC1/cards.json; lessons L01-L05", "PASS",
    f"Every number in every card's front and back appears in its own lesson text: 0 issues ({EX}/cards_numbers_r7.out, lessons stripped by strip_html_r7.py from the unchanged L01-L05 HTML)."))
rows.append(row("proj-cards-numbered-references", "2.7-cards", "cards.json block references vs lessons", "PASS",
    f"163 numbered references (Proposition, Remark, Example, Assumption, Definition, Corollary, Problem, Section) scanned ({EX}/cards_refs_r7.out). Ten lines are flagged, all 'Assumption A1/A2/A3/B1/B2/B3/B4'; each is a numbered item in its lesson ('A2 (full redeposit)' under 'Assumption 2.0', L01 line 33; 'B1 (two dealers)' under 'Assumptions B1 to B4', L03 line 57; 'A1 (trades at the quote)' etc. under 'Assumptions A1 to A3', L03 line 33). The scan's flag is a formatting artefact; no citation is missing."))
rows.append(row("proj-cards-sample", "2.7-cards", "cards.json, 137 cards; sampled against L01-L05 (stripped text)", "PASS",
    "All 137 cards read this round against the stripped lesson text. Content checked against the lesson statements for c010 (1000 x (1 - 0.9^11)/0.1 = 6861.8940391, computed), c011 (1000/0.55 = 1818.18; base 10,000 dollars stated in Example 3.6, L01 lines 63-64), c012 (Remark 3.4, L01 line 57-58), c015 (S_1 = 1900, computed), c016 (stage-10 multiplier 6.8619), c020/c021 (Assumption 1.3 and Proposition 1.4, L02 lines 27-30), c030/c033/c034/c095/c096 (Lab 2 register read from tests/labs/FC1/lab-FC1-L02-1.py and its output: exposure 3,3,2,2,2; form 6/6; venue 4/8; derivative entries 3, 5, 6, 8, 10, 11), c043/c044 (Example 2.5, L03 line 51), c050 (Proposition 3.2 statement, L03 line 65), c053/c097/c098 (Lab 1 Part B: 4000, -545, 3455; L03 line 202), c054 (121 pairs, L03 line 202), c061/c062 (Examples 1.3, 1.4, L04 lines 30-33 and Fixture A/B output at L04 line 255), c066/c100 (Proposition 2.3 with stops counted at activation, L04 lines 43-46), c069 (L04 line 229: 0 crossed events), c080/c089 (Proposition 2.1 and 2.2 hypotheses, L05 lines 33-38), c082-c086 (216 x 10060 = 2172960; 14282414/68398886 = 0.20881 -> 0.209; Friday 2026-10-30 from Wednesday 2026-10-28 by date arithmetic; L05 lines 47, 263-302), c092/c093 (Lab 1 Parts C and D; L01 lines 179-189, 306-308), c110/c111 (Assumption 2.0 items A2 and A3, L01 lines 32-34), c122 (Proposition 4.1, L01 line 70)."))
rows.append(row("proj-cards-changed-subjects", "2.7-cards", "cards.json FC1-c044, FC1-c125; FC1-c134 removed", "PASS",
    "Re-checked against the current lesson text. c044 (back changed): Example 2.5 is a closed sequence with spread term 400 and profit -600 (L03 line 51, 213), so 'a closed sequence can earn the spread and still lose money when the mid moves against the dealer' is correct. c125 (front and back changed): L01 Lab 1 Part B prints 'each stage balances: True' and 'cumulative reserves plus loans equal total deposits: True' (L01 lines 296-297), so 'Both print True' is correct. c134 was removed; no reference to FC1-c134 remains in the course tree (grep)."))
rows.append(row("proj-cards-c014-lab-true", "2.7-cards", "cards.json FC1-c014 (L01)", "PASS",
    "Lab 1 Part A prints 'the partial sums equal the closed form exactly for n = 0 to 10: True' (L01 line 291, run output)."))
rows.append(row("proj-cards-c122-equity-after-loss", "2.7-cards", "cards.json FC1-c122 (L01)", "PASS",
    "Assumption 4.0 and Proposition 4.1: equity after a loss is nonnegative iff lambda <= E (L01 line 70)."))
rows.append(row("proj-cards-citation-R3", "2.7-cards", "cards.json FC1-c054 (L03)", "PASS",
    "Lab 1 Part C checks 121 pairs and prints the three symmetric pairs (L03 line 202); the lesson says the grid is a finite check and the proof covers every whole-cent ask at or above cost (L03 line 202)."))
rows.append(row("proj-cards-citation-R2", "2.7-cards", "cards.json FC1-c089 (L05)", "PASS",
    "Proposition 2.1(ii) proof uses Pay_j >= 0 and A1 makes every consideration non-negative (L05 lines 35, 357); the card's counterexample with one trade of -100 cents is the L05 problem set's own point (line 357)."))
rows.append(row("proj-cards-citation-scan", "2.7-cards", "cards.json block references", "PASS",
    "Same scan as proj-cards-numbered-references (163 references; artefact flags explained there)."))
rows.append(row("proj-cards-grades", "2.7-cards", "cards.json grade and basis fields", "PASS",
    "41 T and 15 C cards and 81 ungraded cards (ungraded cards are definitions and remarks). Sampled T cards (c010, c014, c092, c093, c122) rest on lesson proofs or exact typed-in lab checks; sampled C cards (c030, c033, c052, c053, c069, c082-c086) cite SIMULATED labs or a hand reading, with the basis named."))
rows.append(row("proj-spec-scope-vs-curriculum", "2.6-spec", "project.html lines 157, 161; curriculum/02-economics-finance-core.yaml lines 388-395", "PASS",
    "Curriculum brief: 'Futures, swaps and options follow in FC2' (yaml line 393); FC2 is 'Derivatives Fundamentals' (yaml line 397). The page says cash instruments only and names FC2 as the Derivatives unit: consistent."))
rows.append(row("proj-terminology-short-holder", "2.9-prose", "project.html lines 54, 159, 179", "PASS",
    "'holder' is defined at its first use (line 54) and used consistently."))
rows.append(row("proj-prose-banned-phrases", "2.9-prose", "project.html; cards.json; L01-L05; grader/*.py", "PASS",
    "check_pages.py (banned strings) passes; case-insensitive grep for TODO, TBD, lorem, for brevity, omitted, beyond the scope, exercise, you can add more, important to note, studies show, experts agree, it is well known, obviously, clearly and ellipses finds none in the project's learner text."))
rows.append(row("proj-process-words", "2.9-prose", "project.html; cards.json; grader/*.py; tests/labs/FC1/lab-FC1-project-*.py", "PASS",
    "Case-insensitive grep for verifier, builder, planner, build, ledger, REQUEST, unit report, audit, campaign, Architect, plan section and round N: no match in learner-visible text."))
rows.append(row("proj-scope-words", "2.9-prose", "project.html lines 163, 171, 176, 180, 276", "PASS",
    "Scope words (every, each, any, never, always, only) are tied to a test or a stated rule: 'every named condition' (171) is tested on both sides; 'each events() call' (180) is tested by test_repeated_events_calls_agree; 'every period 1..periods' (177) is tested for 13-15, 24, 40 and 100 periods; 'the page does not refuse' (171) is tested at 150 % and 300 %; 'the page does not bound' (171) is tested at settlement 100 and 1000."))
rows.append(row("proj-terms-before-definition", "2.9-prose", "project.html lines 38, 54, 58, 178", "PASS",
    "face, coupon, settlement period, event and holder are defined in line 54 before use; basis point (line 54); present value and discount factor are linked to the curriculum concepts (line 58, 178)."))
rows.append(row("proj-notation", "2.4-notation", "project.html lines 58, 106, 178; notation/notation.json", "PASS",
    "notation.json registers T, Phi, gamma_3, gamma_4, R*, R^e*, R_f and blackboard Q. None occurs on the FC1 project page; the lowercase y, t, n and period symbols used here are not registered, so none collides."))
rows.append(row("proj-footer-claim", "2.9-smoke", "project.html line 341 footer", "PASS",
    f"page_smoke: no external requests ({EX}/page_smoke_project.out). The footer's claim 'nothing you write leaves it' is consistent with grader.js, which fetches only same-origin files."))
rows.append(row("proj-saved-as-you-type", "2.9-prose", "project.html line 301; course/assets/js/grader.js lines 59-61", "PASS",
    "Carried from round 6 (course/assets/js/grader.js and labs.js byte-identical since the previous pin: git diff --quiet 142ecfc HEAD). Round 6 read grader.js line 59-61 (an input listener saving the editor text after a 400 ms debounce); the lines are unchanged."))
rows.append(row("proj-references-reading-list", "2.1-citations", "project.html lines 321-333 (data-cite keys); references/references.json", "PASS",
    "Both keys exist in references/references.json with status 'verified' (harris2002trading, mishkin2021economics); the page cites by key only and attributes no statement to either source (line 323). verify_refs --offline: '560 entries, 0 problems' (out/verify_refs_offline.out). Live Crossref not run (offline)."))
rows.append(row("proj-cited-year-conflicts", "2.1-citations", "references/references.json; curriculum/02-economics-finance-core.yaml lines 384-385", "PASS",
    "Registry years disagree with the curriculum's quoted years: harris2002trading 2002 (curriculum says 2003; Crossref 2002); mishkin2021economics 2021 (curriculum says 13th ed. 2022). The project page prints no year, so no page claim is wrong; the conflict is a registry flag below."))
rows.append(row("proj-data-simulated", "2.8-data", "project.html lines 45, 54, 72, 159; grader/instance.py label", "PASS",
    "No dataset is read; every value is labelled SIMULATED (instance.py docstring and label field; project.html line 54)."))
rows.append(row("proj-lab3-autograder-coverage-note", "2.9-prose", "project.html line 276 (note after Lab 3)", "PASS",
    "The note says which fixture events the autograder does not check ('Fixture G's events and the rounding case's events are not checked as lists; their prices are'). Verified: no test asserts Bond(10001,0,1).events() or Bond(10000,500,3).events() as a list (grep of test_project.py), and the prices are asserted at test_bond_price_exact_half_at_five_thousand_point_five_rounds_up and test_bond_price_hand_fixture_rounds_the_sum_once. The other fixture claims in line 276 match the tests named there."))
rows.append(row("proj-page-grading-description", "2.6-spec", "project.html line 171", "PASS",
    "Every item in the line-171 list is a test in grader/test_project.py: events of the bond and trade (122-200, 524-528); the discounted-sum price on two cases (352) and on 13-15, 24, 40 and 100 periods (281, 304, 318, 791); the fixtures (174-275, 394-431); the exact-half cases including ten, forty and forty-one digits and the hair under a half cent (431, 822, 455); every named condition on both sides (215-664); yield above 100 % at 150 % and 300 % (510, 806); trades settling in periods 100 and 1000 (667, 814); silence and purity (688-745)."))
rows.append(row("proj-reference-deployment", "2.6-autograder", "course/modules/FC/FC1/grader/reference.py; BLUEPRINT.md lines 400-401", "FAIL",
    "BLUEPRINT.md line 400-401: 'Deployment publishes course/ ... and excludes every grader/reference.py: the suites are public, the reference solutions are not.' No exclusion exists in the repository: .github/workflows/ci.yml has no deploy step and no artifact of course/; no vercel, netlify or wrangler config is tracked; .gitignore does not exclude reference.py. reference.py's own docstring says 'no file in this repository enforces that'. Unchanged since round 6 (9373ef3 touches no deploy file). This is repo-wide, not FC1-only.",
    "Make the publish step exclude every course/**/grader/reference.py, either as a committed deploy-config exclusion or by moving reference solutions outside course/ and updating tools/run_graders.py, tools/check_projects.py and tools/page_smoke.py, which read grader/reference.py. Applies to every autograded unit."))
rows.append(row("proj-ruff-repo-gate-note", "2.9-lint", "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py", "PASS",
    f"ruff check . -> 'All checks passed!' ({EX}/ruff_check.out); the round-6 note on a ruff format issue in a retired M3 file is not reproduced at this pin."))

registry_flags = [
    "harris2002trading: registry year 2002 (Crossref); curriculum/02-economics-finance-core.yaml line 385 says 'Harris, Trading and Exchanges (2003)'. The project page cites the key only. For the curriculum owner.",
    "mishkin2021economics: registry year 2021 (record); curriculum line 384 says '13th ed. (2022)'. Not checked online (offline only). The project page cites the key only. For the curriculum owner.",
]
mutant_survivors = [m for m in mutants if not m["killed_by"]]
passing = sum(r["status"] == "PASS" for r in rows)
failing = [r for r in rows if r["status"] != "PASS"]
notes = [
    "Round 7 on 9373ef3 (round-6 pin 142ecfc). Slice delta 142ecfc..9373ef3 read in full: project.html (line 54: 'a per-period yield ... the rate at which each event is discounted back to period 0'; line 171: '78 checks' with the new tests named); grader/test_project.py (+40 lines at 791-829, after the wrapper loop at 786); cards.json (c044 back changed, c125 front and back changed, c134 removed). Lessons L01-L05, labs, reference, instance, starter, alternatives a1-a5 and notation are byte-identical to round 6 (git diff stat).",
    "All 116 mutants (111 earlier plus five written this round) were run by tools/mutate_graders.py --unit FC1 --seeds 0-19: 115 killed, 1 survived (r7c_periods_refused_above_one_thousand.py, FAIL row).",
    "Round-6 FAIL rows proj-mutant-*-survivor are re-verified as PASS (killed by the four tests added this round at lines 318/510/667/791/822 and the decimal and yield cases).",
    "Round-6 FAIL row proj-reference-deployment is still FAIL (no repo-wide exclusion; see that row).",
    "A scratch copy with the three proposed fixes (wrapper moved to the end; two first docstring lines reworded and the 2625 line; a 1001-period test) gives 79 tests; 116/116 mutants killed on seeds 0-19; reference passes; alternatives a1-a5, alt6-alt12 all pass; starter output contains no leaked answer (out/kill_check_proposed_fix_r7.out, out/starter_run_proposed_fix_r7.out). The fix is NOT applied to the repository (verifier rule: report, do not fix).",
    "Cards: 137 cards in the file at this pin (138 at round 6, c134 removed). Full read of all 137 cards this round; content checked against the current lesson text for about 40 of them, plus every changed card and the scans. The lessons' own prose, problem sets and labs were not audited in this slice beyond the statements the cards cite.",
    "Could not check: the deployed site (no deploy config in the repository); live Crossref and publisher checks (offline only, no network); the full repository pytest suite (only -k FC1: 9 passed, and tests/ run for FC1); a browser run of the three proposed-fix tests in Pyodide (local pytest only); hours (architect ruling: design targets); the lessons' prose beyond the cited statements; byte-level rebuild of anything outside this slice.",
    "Round-7 fragment replaces ledgers/FC1/FC1-c.json, which at this pin held a round-13 fragment written by an earlier verifier. The orchestrator decides whether the round-13 content must be kept elsewhere.",
]
frag = {
    "unit": "FC1",
    "slice": "c",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 7 (did not build FC1)",
    "pin": "9373ef398589097500ea849e30ff9da423b98943",
    "base": "142ecfc2bd27061de18bd67e83df81e69f5c249d (round-6 pin of this slice)",
    "checkout": str(ROOT),
    "scratch": "/tmp/fc1c_r7/ (starter_out.txt, fixed/ with the proposed fix); /tmp/fc1c_r7_kill.*, /tmp/fc1c_r7_*alt* (removed after use)",
    "verified_at": datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds"),
    "verdict": "FAIL" if failing else "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": registry_flags,
    "freshness_flags": [],
    "notes": notes,
    "summary": (f"Round 7 on 9373ef3: {len(rows)} rows: {passing} PASS, {len(failing)} FAIL, 0 UNVERIFIABLE. "
                f"Verdict FAIL. Mutants: {len(mutants) - len(mutant_survivors)}/{len(mutants)} killed on seeds 0-19. "
                "FAIL rows: proj-mutant-periods-cap-1000-survivor (and aggregate proj-mutants-r7c-new, proj-mutants-all), "
                "proj-starter-message-leaks-answer, proj-starter-unwrapped-new-tests, proj-reference-deployment (repo-wide)."),
}
out_path = ROOT / "ledgers/FC1/FC1-c.json"
out_path.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out_path, "rows", len(rows), "FAIL", len(failing), "mutants", len(mutants))
