"""Round 16, FC1-c: assemble ledgers/FC1/FC1-c.json from the round-15 rows, the round-16 evidence and the mutate output.

Run from the checkout root with: .venv/bin/python -I ledgers/FC1/scripts/FC1-c-r16/build_fragment_r16.py
"""
import datetime
import json
import re
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "ledgers/FC1/scripts/FC1-c-r16/out"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-FC1-c.round15.json").read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

CARRY = "Carried from round 15 ({files} byte-identical since the previous pin dde0486b): "
P = "PASS"
F = "FAIL"

def carry(rid: str, files: str, evidence: str) -> dict:
    return {"id": rid, "check": prev_rows[rid]["check"], "location": prev_rows[rid]["location"], "status": P,
            "evidence": CARRY.format(files=files) + evidence}

def fresh(rid: str, location: str, evidence: str, status: str = P, fix: str | None = None) -> dict:
    row = {"id": rid, "check": prev_rows[rid]["check"] if rid in prev_rows else rid, "location": location,
           "status": status, "evidence": evidence}
    if status != P:
        row["fix"] = fix
    return row

MUT = "ledgers/FC1/mutants/"
SC = "ledgers/FC1/scripts/FC1-c-r16/out/"
rows = [
    fresh("proj-run-graders", "course/modules/FC/FC1/grader/reference.py; tools/run_graders.py",
          f"`.venv/bin/python tools/run_graders.py --unit FC1 --seeds 0-49` -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0 ({SC}run_graders_s0-49.out). Re-run because test_project.py changed."),
    fresh("proj-collect-count-65", "course/modules/FC/FC1/project.html line 171; grader/test_project.py",
          f"collect-only on a scratch copy (scripts/collect_count.py, reference as instruments.py): '99 tests collected' ({SC}collect_count_r16.out). `grep -c '^def test_'` = 99. project.html line 171 says 'runs 99 checks'. The id keeps the historical text '65' for tracking only."),
    fresh("proj-browser-suite", "course/modules/FC/FC1/project.html line 302 (section#grader); course/assets/js/grader.js",
          f"page_smoke --unit FC1 --pages project: 'in-browser grader: All 99 tests pass on seed 702045824' and 'page_smoke modules/FC/FC1/project.html: PASS' ({SC}page_smoke_project.out). The panel attributes (line 302) are unchanged in the delta."),
    fresh("proj-alternatives-five", f"ledgers/FC1/alternatives/a1..a5 (run against grader/test_project.py)",
          f"alt_run_r16.py (copy of the round-15 runner) on a1..a5 at seeds 0-49: 'PASS ... failing seeds 0/50' for each ({SC}alternatives_r16_s0-49.out). Re-run because the suite gained two accepted-input tests."),
    fresh("proj-alternatives-integer-only", "ledgers/FC1/scripts/FC1-c-r14/alt_integer_only_r14.py",
          f"alt_run_r16.py: 'PASS alt_integer_only_r14.py: failing seeds 0/50' ({SC}alternatives_r16_s0-49.out)."),
    fresh("proj-alternatives-new-r15", "ledgers/FC1/scripts/FC1-c-r15/alternatives/alt_decimal_100_digits_r15.py; alt_cached_lists_r15.py",
          f"alt_run_r16.py: 'PASS alt_decimal_100_digits_r15.py: failing seeds 0/50' and 'PASS alt_cached_lists_r15.py: failing seeds 0/50' ({SC}alternatives_r16_s0-49.out)."),
    fresh("proj-instances-20", "course/modules/FC/FC1/grader/instance.py",
          f"check_instances_r15.py re-run on the round-16 checkout: range violations []; distinct full answer tuples over seeds 0-49: 50; sample seeds 0-19 prices listed; label contains SIMULATED: True ({SC}instances_r16.out). instance.py byte-identical since dde0486b; run_graders determinism check PASS."),
    fresh("proj-instances-50", "course/modules/FC/FC1/grader/instance.py; grader/reference.py",
          f"Same run as proj-instances-20: 'distinct bond prices over seeds 0-49: 50', 'distinct bond event lists: 50', 'distinct trade events: 50' ({SC}instances_r16.out)."),
    fresh("proj-starter-vs-spec", "course/modules/FC/FC1/grader/starter.py; project.html line 161",
          f"Signatures of starter.py and reference.py compared (instances_r16.out lines 'Bond __init__ ref ... starter ...'; all five identical). run_graders PASS includes the starter-fails-suite check. project.html line 161 names Bond(face_cents, coupon_bps, periods), bond_price_cents(bond, yield_bps), CashTrade(quantity, price_cents, side, settlement_day): same names as the starter."),
    fresh("proj-spec-questions", "course/modules/FC/FC1/project.html lines 153-172",
          "Re-read lines 153-172 in full. Required outputs match starter.py names and signatures. Constraints (line 163) and the named-condition list (lines 165-167) are the only refusals listed; the eight named conditions are counted as 3 (Bond) + 1 (bond_price_cents) + 4 (CashTrade). Grading mode (line 171) reads '99 checks', matching the collect count. Context (line 157) scope sentence matches ruling 5."),
    carry("proj-ladder", "project.html lines 41-50 and course/modules/FC/FC1/index.html lines 122-128",
          "git diff -U0 dde0486b..HEAD hunks in project.html are at lines 38, 54, 101, 171, 188 and 323 only; index.html is unchanged. Previous evidence stands."),
    carry("proj-stretch-scope", "project.html lines 312-318 (section#stretch)",
          "No hunk in project.html lines 312-318 (hunk list 38, 54, 101, 171, 188, 323). Previous evidence stands."),
    carry("proj-local-command", "project.html lines 305-310 and grader/starter.py docstring",
          "No hunk in project.html lines 305-310; starter.py unchanged in the delta (`git diff --quiet dde0486b..HEAD -- course/modules/FC/FC1/grader/starter.py`). Previous evidence stands."),
    fresh("proj-lab1-twin", "course/modules/FC/FC1/project.html lab-FC1-project-1 (lines 56-102); tests/labs/FC1/lab-FC1-project-1.py",
          f"scripts/page_vs_twin_r16.py output: 'lab-FC1-project-1.py: rc=0 output==expected: True; page block vs twin differing lines: 0' ({SC}page_vs_twin_r16.out). The changed interpretation sentence (line 101) is checked against the printed lines: exact present value 102775.09103322713 (numbers_r16.out, 'L1 ... exact 6dp 102775.091033'), fraction .091033 < 1/2 so the price is 102775; the first printed line carries the coupon 5000; the trade line is -98500 (negative: buyer pays)."),
    carry("proj-lab2-completion", "project.html lines 104-150 and tests/labs/FC1/lab-FC1-project-2.py",
          f"No hunk in lines 104-150; lab-FC1-project-2.py unchanged. Fresh page_vs_twin_r16 output also shows output==expected True and only the two blanks differing ({SC}page_vs_twin_r16.out)."),
    carry("proj-lab2-docstring", "project.html line 107 and tests/labs/FC1/lab-FC1-project-2.py line 1",
          "No hunk at project.html line 107 (hunk list 38, 54, 101, 171, 188, 323); lab-FC1-project-2.py unchanged in the delta. Previous round's FAIL was fixed in round 15 and this row stays PASS."),
    carry("proj-lab3-fixtures", "project.html lines 196-276 and tests/labs/FC1/lab-FC1-project-3.py",
          f"No hunk in lines 196-276; lab-FC1-project-3.py unchanged. Fresh page_vs_twin_r16: 'lab-FC1-project-3.py: rc=0 output==expected: True; ... differing lines: 0'. Fixture C text (line 188) is re-derived in proj-fixture-claims."),
    fresh("proj-prose-numbers", "course/modules/FC/FC1/project.html lines 54, 58, 101, 171, 176, 186-193, 198, 275, 290, 293",
          f"Every number re-derived with exact Fractions in scripts/numbers_r16.py ({SC}numbers_r16.out): 100000 face, 500 bps coupon = 5000 cents, 3 periods, events (1,5000),(2,5000),(3,105000); 400 bps; exact PV 102775.091033 cents; price 102775; trade (2,-98500); 99 checks (collect); fixtures A-G and rounding fixture (see proj-fixture-claims); rounding fixture term-by-term 481+462+9334 = 10277 vs once-rounded 10278; hours 1+2+5+4+2+3+3 = 20 (line 293 Total 20)."),
    fresh("proj-fixture-claims", "course/modules/FC/FC1/project.html lines 183-194 and 276; grader/test_project.py lines 174-200, 245, 396-480",
          f"numbers_r16.out: A events [(1,10500)], price 10000; B exact 210000/19 = 11052.6316, rounds 11053; C events [(1,5001),(2,15002)], coupon 10001/2 = 5000.5 -> 5001 (line 188 now says 'the coupon of 10001 cents times 50 % of face is 5000.5 cents, which rounds up to 5001': correct); D [(1,2)]; E (2,-98500) and seller (2,98500); F exact 1/2, half-away 1, half-even 0; G [(1,10001)] price 5001; rounding fixture events [(1,500),(2,500),(3,10500)], exact 10277.509103, price 10278, term-wise 10277. Test names covering them exist at grader lines 174, 182, 189, 197, 418, 428, 437, 445, 456, 481 (test_project.py); ast_scan_r16.out: no assert lacks a message."),
    carry("proj-hours-arithmetic", "project.html section#budget lines 283-293 and course/modules/FC/FC1/index.html lines 29-41",
          "No hunk in project.html lines 283-293 and index.html is unchanged. Recomputed in this round: 1+2+5+4+2+3+3 = 20, matching Total 20 and the hub's 20 of 70."),
    fresh("proj-check-pages-dag", "course/modules/FC/FC1/ (project.html)",
          f"check_pages.py --unit FC1: 'check_pages FC1: PASS'; check_dag.py --unit FC1: 'check_dag FC1: PASS'; check_projects.py --unit FC1: 'check_projects FC1: PASS' (exit 0 each; {SC}check_pages_unit.out, check_dag_unit.out, check_projects_unit.out)."),
    fresh("proj-dag-closure", "course/modules/FC/FC1/project.html lines 58, 178, 316; curriculum/curriculum.json (prerequisite closure)",
          f"check_dag FC1 PASS ({SC}check_dag_unit.out). The Lesson 5 reference at project.html line 177 ('business-day offset ... in Lesson 5') matches course/modules/FC/FC1/L05.html line 63 ('Each state carries a business-day offset'). L05.html is changed in the delta by another slice; this cited sentence is still present."),
    fresh("proj-notation", "course/modules/FC/FC1/project.html math (\\(y\\), \\(t\\), \\(1+y\\), \\(y = 400/10000\\)); notation/notation.json",
          f"notation_r16.sh: page math tokens are \\(1+y\\) (1), \\(t\\) (3), \\(y = 400/10000\\) (1); the delta adds no math token ({SC}notation_r16.out is the script output in out/). notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}}; y and t are local letters (notation.json 'about' allows conventionally local letters) and no registered symbol is reused."),
    fresh("proj-banned-phrases", "course/modules/FC/FC1/project.html; grader/*.py; tests/labs/FC1/lab-FC1-project-*.py",
          f"check_pages FC1 PASS (its BANNED list covers the project page; {SC}check_pages_unit.out). grep -i over the grader files and the three lab twins for the BANNED strings of tools/check_pages.py: only a code identifier '_named_when_unimplemented' and Callable[..., None] match the pattern '...'; no prose match."),
    fresh("proj-reading-list", "course/modules/FC/FC1/project.html lines 323-327; references/references.json; curriculum/02-economics-finance-core.yaml lines 383-386",
          "Line 323 now says 'The two sources of this unit that are in the reference registry. The curriculum also names a third source, which is not in the registry'. references.json has keys mishkin2021economics and harris2002trading (entries 'Economics of Money, Banking, and Financial Markets' and 'Trading and Exchanges'); no entry matches McLeay or Radia (grep empty). curriculum lines 383-386 list three sources. The page states no years, so the year differences (curriculum: Harris 2003, Mishkin 2022; registry keys: 2002, 2021) are not asserted on the page and are noted, not failed."),
    carry("proj-scope-ruling5", "project.html line 157; curriculum/02-economics-finance-core.yaml lines 388-395; plans/FINAL-ARCHITECT-RULINGS.md lines 11-12",
          "No hunk at project.html line 157; the curriculum yaml is unchanged (git diff --quiet); the ruling file changed only by appended rulings 30-34 at line 94 onward, so lines 11-12 (ruling 5) are unchanged."),
    fresh("proj-named-conditions", "course/modules/FC/FC1/project.html lines 165-167; grader/test_project.py must_raise call sites",
          "must_raise call sites present: Bond periods (test_bond_periods_zero_is_refused, periods=-1 test, boundary periods=1 accepted), face (face 0 and -1 refused, one cent accepted), coupon negative (refused; zero accepted), bond_price yield (-10000 refused, -20000 refused, the boundary -9999 accepted), CashTrade quantity (0, -1 refused; 1 accepted), price negative (-1 refused; 0 accepted), side (0, 2, -2, 3, -3 refused; +1, -1 accepted), settlement_day (0, -1 refused; 1 accepted). Grep of must_raise(...) lines in test_project.py."),
    fresh("proj-named-conditions-context", "course/modules/FC/FC1/project.html lines 163 and 167; grader/test_project.py lines 63-70 and 268-278",
          "Page line 163 says each named condition raises ValueError and any other invalid input may raise any exception or return; line 167 lists the CashTrade refusals. test_project.py 268-278 (zero-coupon periods and face refusals, each 'the page names ... for every bond, with or without a coupon') and the helpers at lines 63-70 are present and consistent with the page."),
    fresh("proj-failure-messages", "course/modules/FC/FC1/grader/test_project.py (all assertions, must_raise, must_accept, checked_events, checked_int)",
          f"ast_scan_r16.py on the round-16 test file: 99 test functions; asserts without a message: []; must_raise/must_accept calls without a condition string: [] ({SC}ast_scan_r16.out)."),
    fresh("proj-test-docstring", "course/modules/FC/FC1/grader/test_project.py docstrings (the two new tests at lines 354-360 and 643-651)",
          f"ast_scan_r16.py: tests without a docstring: [] ({SC}ast_scan_r16.out). The two new docstrings name the page's basis ('the page names only coupon_bps negative as refused...'; 'the page names only price_cents negative as refused') and the expected value, which the reference reproduces (numbers_r16.out)."),
    fresh("proj-simulated-labels", "course/modules/FC/FC1/project.html lines 54, 72, 120, 159; grader/instance.py label",
          f"Line 54 says both labs use SIMULATED values; the twins lab-FC1-project-1.py line 1 and lab-FC1-project-2.py line 14 carry the SIMULATED label; grep for open(, read_text, urllib, requests, socket, random in the three twins: no match (rc=1). instances_r16.out: 'label contains SIMULATED: True'. Wording note (not a failure): line 54 glosses SIMULATED as 'generated numbers', but the lab values are typed-in constants, not generated; the label stays accurate."),
    fresh("proj-silence-coverage", "course/modules/FC/FC1/project.html line 163; grader/test_project.py lines 740-766",
          "test_the_module_prints_nothing (lines 740-764) lists 14 valid inputs, all with the capsys check; test_refused_inputs_print_nothing_before_they_raise (766) checks refused inputs; reference passes all 99 tests under -W error (run_graders and in-browser run). Page line 163 limits the silence claim to the inputs the suite checks, and the test docstring says the same."),
    carry("proj-privacy-claim", "project.html line 341; course/assets/js/grader.js; course/assets/js/py-worker.js",
          "No hunk at project.html line 341; course/assets/js is unchanged in the delta (`git diff --quiet dde0486b..HEAD -- course/assets/js`)."),
    fresh("proj-lint-types", "course/modules/FC/FC1/grader/*.py; tests/labs/FC1/*.py",
          f"ruff check course/modules/FC/FC1/grader tests/labs/FC1: 'All checks passed!' ({SC}ruff_check_grader_labs.out). ruff format --check (same scope): '12 files already formatted' ({SC}ruff_format_scope.out). mypy --no-incremental (repo): 'Success: no issues found in 385 source files' ({SC}mypy_repo.out). mypy --strict on reference.py, starter.py, instance.py: 'Success: no issues found in 3 source files' ({SC}mypy_grader_strict.out). The ruff run over the whole scratch directory failed only on my own scratch runner (ledgers/FC1/scripts/FC1-c-r16/alt_run_r16.py, PTH118), which is not a repository file."),
    carry("proj-reference-deployment", "course/modules/FC/FC1/grader/reference.py lines 3-4; BLUEPRINT.md lines 400-401",
          "reference.py and BLUEPRINT.md are unchanged in the delta (`git diff --quiet dde0486b..HEAD` for both paths)."),
    fresh("proj-exemplar-blind", "course/modules/FC/FC1/project.html; curriculum grading for FC1 project",
          "grep -i exemplar on project.html: no match. The only 'solution' is the lab-2 docstring at line 107 ('Rung 2 completed solution: the worked example with its two blanks filled in'), which is a learner-facing worked example, not a graded exemplar. The calibration note says the project has no rubric exemplars to score."),
    fresh("proj-mutant-set-earlier", "ledgers/FC1/mutants/ (136 files that existed at the round-14 pin)",
          "`git diff --name-status 1431aa1d..HEAD -- ledgers/FC1/mutants` = 16 A, no M or D: the 136 files that existed at 1431aa1d are byte-identical. Total mutants now 155."),
    fresh("proj-mutant-first-line", "ledgers/FC1/mutants/*.py (every file's first docstring line)",
          "Scanned the first docstring line of all 155 files (ast.get_docstring). 150 name a student error (for example 'CashTrade refuses a price above...' or 'Bond.events() adds the face...'). Five files do not: ledgers/FC1/mutants/fc1a_r5_lab_L01_closed_form_exponent_short.py, fc1a_r5_lab_L01_half_limit_comparison_flipped.py, fc1a_r5_lab_L02_well_formed_accepts_two_values.py, fc1a_r5_lab_L03_spread_capture_doubled.py, fc1a_r5_lab_L03_tie_pays_full_profit.py. They are lab mutants (their first lines start 'FC1 lab L0x:'), not project student-error mutants. See the note on them under proj-mutants-killed."),
    fresh("proj-new-mutants-r10", "ledgers/FC1/mutants/r10n01..r10n04; r10c_*",
          f"mutate_graders.py --unit FC1 --seeds 0-9 (round-16 run, {SC}mutate_FC1_s0-9_r16.out): every r10n* and r10c_* file KILLED (killed_by lines recorded there)."),
    fresh("proj-new-mutants-r11", "ledgers/FC1/mutants/r11n01..r11n03; r11c_*",
          f"Same run: every r11n* and r11c_* file KILLED ({SC}mutate_FC1_s0-9_r16.out)."),
    fresh("proj-new-mutants-r12", "ledgers/FC1/mutants/r12n01..r12n03; r12c_*",
          f"Same run: every r12n* and r12c_* file KILLED ({SC}mutate_FC1_s0-9_r16.out)."),
    fresh("proj-mutant-r13n01", "ledgers/FC1/mutants/r13n01_coupon_computed_in_float.py; grader/test_project.py test_bond_coupon_is_exact_for_a_face_too_large_for_floats",
          f"KILLED in the round-16 mutate run ({SC}mutate_FC1_s0-9_r16.out): killed_by test_bond_coupon_is_exact_for_a_face_too_large_for_floats (seed 0)."),
    fresh("proj-mutant-r13n02", "ledgers/FC1/mutants/r13n02_trade_cash_flow_in_float.py; grader/test_project.py test_trade_cash_flow_is_exact_above_two_to_the_fifty_three",
          f"KILLED in the round-16 mutate run ({SC}mutate_FC1_s0-9_r16.out): killed_by test_trade_cash_flow_is_exact_above_two_to_the_fifty_three (seed 0)."),
    fresh("proj-mutant-r13n03", "ledgers/FC1/mutants/r13n03_yield_rate_through_float.py; grader/test_project.py test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield",
          f"KILLED in the round-16 mutate run ({SC}mutate_FC1_s0-9_r16.out): killed_by test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield (seed 0)."),
    fresh("proj-new-mutants-r14-killed", "ledgers/FC1/mutants/r14n02, r14n03, r14n04",
          f"Same run: r14n02, r14n03 and r14n04 KILLED ({SC}mutate_FC1_s0-9_r16.out)."),
    fresh("proj-mutant-r14n01", "ledgers/FC1/mutants/r14n01_sale_skips_quantity_and_settlement_checks.py; grader/test_project.py test_sale_quantity_zero_is_refused",
          f"KILLED in the round-16 mutate run ({SC}mutate_FC1_s0-9_r16.out): killed_by test_sale_quantity_zero_is_refused (seed 0)."),
    fresh("proj-mutant-r14n05", "ledgers/FC1/mutants/r14n05_bond_periods_and_face_checked_only_with_a_coupon.py; grader/test_project.py test_bond_zero_coupon_periods_zero_is_refused",
          f"KILLED in the round-16 mutate run ({SC}mutate_FC1_s0-9_r16.out): killed_by test_bond_zero_coupon_periods_zero_is_refused (seed 0)."),
    fresh("proj-new-mutants-r15-killed", "ledgers/FC1/mutants/r15n01..r15n04",
          f"Same run: r15n01 through r15n04 KILLED ({SC}mutate_FC1_s0-9_r16.out)."),
    fresh("proj-mutant-r15n05", "ledgers/FC1/mutants/r15n05_price_refused_above_one_million_cents.py; grader/test_project.py test_trade_price_of_ten_to_the_ninth_cents_is_accepted (line 643)",
          f"Was FAIL in round 15 (no test accepted a price above 1000000 cents). Now KILLED by the new test test_trade_price_of_ten_to_the_ninth_cents_is_accepted (seed 0, {SC}mutate_FC1_s0-9_r16.out). Over seeds 0-49 the mutant fails 50/50 (alt_run_r16.py output in {SC}survivor_check_seeds0-49_r16.out)."),
    fresh("proj-mutant-r15n06", "ledgers/FC1/mutants/r15n06_coupon_refused_above_twenty_thousand_bps.py; grader/test_project.py test_bond_coupon_of_twenty_thousand_one_bps_is_accepted (line 354)",
          f"Was FAIL in round 15. Now KILLED by test_bond_coupon_of_twenty_thousand_one_bps_is_accepted (seed 0, {SC}mutate_FC1_s0-9_r16.out)."),
    fresh("proj-accepted-input-tests-r16", "grader/test_project.py lines 354-360 and 643-651; project.html lines 165-171",
          f"Both new tests pass on the reference (run_graders 50/50, {SC}run_graders_s0-49.out). Their expected values were re-derived independently: Bond(10000, 20001, 1).events() = [(1, 30001)] and CashTrade(10, 10**9, 1, 2).events() = [(2, -10000000000)] (numbers_r16.out). The page names only coupon_bps negative (line 165) and price_cents negative (line 167) as refused, and line 171 says the page names no upper limit on a price or a coupon, so the tests are accepted-input checks the page supports. All eight alternatives pass both tests (alternatives_r16_s0-49.out)."),
    fresh("proj-mutant-r16n02", "ledgers/FC1/mutants/r16n02_coupon_refused_above_one_hundred_percent.py",
          f"KILLED by test_bond_coupon_above_one_hundred_percent_is_accepted (seed 0; {SC}mutate_FC1_s0-9_r16.out). The page names no upper limit on a coupon, so this student error is a violation the suite catches."),
    fresh("proj-mutant-r16n01", "ledgers/FC1/mutants/r16n01_price_refused_above_two_to_the_thirty_one.py; grader/test_project.py (no test accepts a price above 2**31 - 1)",
          f"SURVIVED: no test kills it on seeds 0-9 ({SC}mutate_FC1_s0-9_r16.out: 'SURVIVED r16n01 ... -> None') or on seeds 0-49 ({SC}survivor_check_seeds0-49_r16.out: 'PASS ... failing seeds 0/50'). The page says the module refuses only the named conditions and that it names no upper limit on a price (project.html line 171 and lines 165-167). A price of 2**31 is valid, so refusing it is a non-equivalent behaviour the page states is accepted. Ruling 9 requires a grader test for it.",
          status=F,
          fix="Add an accepted-input test to grader/test_project.py, for example: must_accept(lambda: sol.CashTrade(10, 2**31, 1, 2).events(), 'price_cents = 2**31') and assert it equals [(2, -(10 * 2**31))]. Checked: this value passes on the reference (ledgers/FC1/scripts/FC1-c-r16/out/fix_check_r16.out). Then re-run mutate_graders --unit FC1."),
    fresh("proj-mutant-r16n03", "ledgers/FC1/mutants/r16n03_coupon_refused_above_two_to_the_thirty_one_bps.py; grader/test_project.py (no test accepts a coupon above 20001 bps)",
          f"SURVIVED on seeds 0-9 ({SC}mutate_FC1_s0-9_r16.out) and on seeds 0-49 ({SC}survivor_check_seeds0-49_r16.out: 'PASS ... failing seeds 0/50'). The page names no upper limit on a coupon (project.html line 171) and refuses only coupon_bps negative (line 165), so refusing a coupon of 2**31 bps is a stated-behaviour violation the suite does not catch.",
          status=F,
          fix="Add an accepted-input test: must_accept(lambda: sol.Bond(10_000, 2**31, 1).events(), 'coupon_bps = 2**31') with the expected [(1, 2**31 + 10_000)]. Checked: passes on the reference (fix_check_r16.out). Then re-run mutate_graders --unit FC1."),
    fresh("proj-mutants-killed", "ledgers/FC1/mutants/ (155 files); grader/test_project.py",
          f"mutate_graders.py --unit FC1 --seeds 0-9 (round 16, {SC}mutate_FC1_s0-9_r16.out): 'mutate_graders FC1: FAIL (153/155 killed)'. The two survivors are r16n01 and r16n03 (the rows above). Note (not a ruling-26 defect): five of the 153 kills are the fc1a_r5_lab_* lab files, which lack the Bond/CashTrade API; they fail the suite trivially (e.g. fc1a_r5_lab_L01_closed_form_exponent_short.py: 97 failed, 2 passed under QF_SEED=0), so they are not evidence about the grader and should be moved out of ledgers/FC1/mutants/.",
          status=F,
          fix="Kill r16n01 and r16n03 with the accepted-input tests in proj-mutant-r16n01 and proj-mutant-r16n03, then re-run `.venv/bin/python tools/mutate_graders.py --unit FC1 --seeds 0-9`."),
    fresh("proj-run-labs", "tests/labs/FC1 (all eight twins)",
          f"run_labs.py --unit FC1: 'run_labs FC1: PASS (8/8)' ({SC}run_labs_fc1.out)."),
    fresh("proj-page-smoke", "course/modules/FC/FC1/project.html",
          f"page_smoke.py --unit FC1 --pages project: 'page_smoke modules/FC/FC1/project.html: PASS' and 'page_smoke FC1: PASS' ({SC}page_smoke_project.out)."),
    fresh("proj-check-projects", "course/modules/FC/FC1/project.html; grader panel attributes",
          f"check_projects.py --unit FC1: 'check_projects FC1: PASS' ({SC}check_projects_unit.out)."),
    fresh("proj-pytest-targeted", "tests/test_curriculum.py; tests/test_labs.py; tests/test_page_checks.py; tests/test_run_labs.py (selected by -k 'FC1 or project or page')",
          f"pytest -q on those four files with -k 'FC1 or project or page': exit 0, no F or E in the output ({SC}pytest_targeted.out). verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' ({SC}verify_refs_offline.out)."),
]

# Mutants: parse the round-16 mutate output (KILLED/SURVIVED lines).
mut_rows = []
for line in (OUT / "mutate_FC1_s0-9_r16.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?)\.py: (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mut_rows.append({
        "id": name,
        "description": desc,
        "killed_by": killed if killed != "None" else f"none: {status} on seeds 0-9 and 0-49",
    })

notes = (
    "Round 16, FC1-c, delta verification (ruling 30) from the round-15 pin dde0486b to the checkout pin e896b7a4. "
    "Delta in the slice: course/modules/FC/FC1/project.html (hunks at lines 38 lede, 54 rungs, 101 lab-1 interpretation, "
    "171 grading mode '99 checks' and the two new accepted-input claims, 188 fixture C wording, 323 reading wording); "
    "grader/test_project.py (two new accepted-input tests at lines 354 and 643); ledgers/FC1/mutants (11 added: fc1a_r5_lab_* x5, "
    "r15n01-n06); no change to the labs, starter, reference, instance, alternatives or the page's grader panel. "
    "Other changed files in the same range belong to other slices (L04.html, L05.html, cards.json, FC2 and other units) and are not verified here. "
    "Rows re-verified from scratch: every row whose subject changed (page lines, test file, mutant set) and the round-15 FAIL rows. "
    "Carried from round 15 only where the cited lines and files are byte-identical (no hunk, or quiet git diff): proj-ladder, proj-stretch-scope, "
    "proj-local-command, proj-lab2-completion, proj-lab2-docstring, proj-lab3-fixtures, proj-hours-arithmetic, proj-privacy-claim, "
    "proj-reference-deployment, proj-scope-ruling5. "
    "Round-16 result: two new student-error mutants survive (r16n01 price refused above 2**31 - 1; r16n03 coupon refused above 2**31 - 1 bps), "
    "each a stated-behaviour violation (the page names no upper limit on a price or a coupon). These are FAIL rows under ruling 26 (surviving non-equivalent mutant). "
    "Verifier-level observations (not FAIL rows, ruling 26 kinds only): (a) five fc1a_r5_lab_* files sit in ledgers/FC1/mutants/ as lab mutants, "
    "not project student errors; they are killed only because they lack the project API; move them out. "
    "(b) project.html line 54 says the event is 'defined at the end of this paragraph', but the definition sentence is the third-from-last sentence of the paragraph; "
    "a wording pointer, LOW. (c) line 54 glosses SIMULATED as 'generated numbers' while the lab values are typed-in constants; LOW wording. "
    "(d) reading list years: curriculum says Harris (2003) and Mishkin 13th ed. (2022); registry keys harris2002trading (year 2002) and mishkin2021economics (year 2021); "
    "the page states no years, so no row fails. "
    "Not checked: the live verify_refs run (network); render_curriculum, build_site --check and fetch_data --check (no curriculum, site or data input of this slice changed; "
    "they belong to the slices that changed those inputs); the full pytest suite; the L04/L05 lessons; Pyodide execution of the new mutants (local only)."
)

fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 16,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 16 (did not build FC1)",
    "pin": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a",
    "base": "dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-15 pin; round-15 fragment /Users/billyribeiro/.fanout/frags/D-FC1-c.round15.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD16-FC1-c",
    "scratch": "ledgers/FC1/scripts/FC1-c-r16/ (scripts and out/)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mut_rows,
    "registry_flags": [
        "references/references.json: mishkin2021economics (year 2021) and harris2002trading (year 2002) vs curriculum/02-economics-finance-core.yaml FC1 sources (Mishkin 13th ed. 2022; Harris 2003). Page states no years; not a row failure.",
        "The third source named by the curriculum (McLeay, Radia & Thomas 2014) is absent from references/references.json, as the page's Reading section states.",
    ],
    "freshness_flags": [
        "verify_refs live run not executed (network); offline run only (560 entries, 0 problems).",
    ],
    "notes": notes,
    "summary": {
        "rows": len(rows),
        "PASS": sum(r["status"] == "PASS" for r in rows),
        "FAIL": sum(r["status"] == "FAIL" for r in rows),
        "UNVERIFIABLE": sum(r["status"] == "UNVERIFIABLE" for r in rows),
        "mutants": len(mut_rows),
        "mutants_killed": sum(not m["killed_by"].startswith("none") for m in mut_rows),
        "failing_rows": [r["id"] for r in rows if r["status"] != "PASS"],
        "prior_round_rows_not_in_this_fragment": sorted(set(prev_rows) - {r["id"] for r in rows}),
    },
}
out_path = ROOT / "ledgers/FC1/FC1-c.json"
out_path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out_path, "rows", len(rows), "mutants", len(mut_rows))
