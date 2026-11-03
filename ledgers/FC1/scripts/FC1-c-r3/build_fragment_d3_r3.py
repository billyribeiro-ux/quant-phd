"""Builds ledgers/FC1/FC1-c.json (round 3, verifier D3) from the round-3 outputs. Evidence lives in the cited files."""
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = ROOT / "ledgers/FC1/scripts/FC1-c-r3/out"
mutate_lines = (OUT / "mutate_graders_all_r3.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mutate_lines:
    m = re.match(r"(KILLED|SURVIVED) (\S+?): (.*) -> (\S.*|None)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    killed_by = None if killed == "None" else killed
    mutants.append({"id": name[:-3], "description": desc, "killed_by": killed_by})
assert len(mutants) == 89, len(mutants)

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


CARRY = "Carried from round 2 (the cited files byte-identical since the round-2 pin c737272): "

row("proj-check-projects", "2.6-structure", "course/modules/FC/FC1/project.html", "PASS",
    "Re-run on a007712: .venv/bin/python tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS' "
    "(ledgers/FC1/scripts/FC1-c-r3/out/check_projects.out, exit 0).")
row("proj-check-pages", "2.9-structure", "course/modules/FC/FC1/project.html", "PASS",
    "Re-run: tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS' (out/check_pages.out, exit 0).")
row("proj-check-dag", "2.9-DAG", "course/modules/FC/FC1/project.html concept links (present-value, discount-factor) and the L05 lesson link",
    "PASS", "Re-run: tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS' (out/check_dag.out, exit 0). Concept links are "
    "present-value and discount-factor only (project.html lines 58, 178).")
row("proj-run-labs", "2.5-labs", "project.html labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py", "PASS",
    "Re-run: tools/run_labs.py --unit FC1 --page project -> 'run_labs FC1: PASS (3/3)' (out/run_labs_project.out); "
    "all FC1 pages -> 'run_labs FC1: PASS (8/8)' (out/run_labs_all_pages.out).")
row("proj-page-smoke", "2.9-smoke", "course/modules/FC/FC1/project.html", "PASS",
    "Re-run: tools/page_smoke.py --unit FC1 --pages project -> 'page_smoke FC1: PASS'; in-browser grader 'All 69 tests "
    "pass on seed 303922455' (out/page_smoke_project.out, exit 0).")
row("proj-run-graders", "2.6-autograder-1", "course/modules/FC/FC1/grader/reference.py, test_project.py, instance.py, starter.py",
    "PASS", "Re-run: tools/run_graders.py --unit FC1 --seeds 0-19 -> 'run_graders FC1: PASS (reference 20/20 seeds, slowest "
    "0.2 s)' (out/run_graders_0_19.out); the architect's full range --seeds 0-49 is out/run_graders_0_49.out (exit 0 means PASS there too). "
    "reference.py is tracked; recorded as a repo-wide note, not failed (see notes).")
row("proj-lint-types", "gate", "course/modules/FC/FC1/grader/*.py and tests/labs/FC1/", "PASS",
    "ruff check on grader and labs: 'All checks passed!' (out/ruff_check_grader_labs.out); ruff format --check on the same: "
    "'12 files already formatted' (out/ruff_format_grader_labs.out); ruff check . passes (out/ruff_repo.out); mypy "
    "--no-incremental: 'Success: no issues found in 331 source files' (out/mypy_no_incremental.out). Repo-wide "
    "'ruff format --check .' exits 1 on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py, outside FC1 "
    "(out/ruff_format_repo.out); recorded in notes, not an FC1 row.")
row("proj-lab1-numbers", "2.2-numbers / 2.5-labs", "project.html lines 58 and 97-100 (Lab 1)", "PASS",
    "Recomputed in Fraction (ledgers/FC1/scripts/FC1-c-r3/numbers_instances_r3.py, out/numbers_instances_r3.out): coupon "
    "5000; events (1,5000),(2,5000),(3,105000); exact PV 102775.09103322713 -> 102775; trade (2,-98500). Prose "
    "'102775.091033' and 'below one half' are correct. Twin run alone under python -I -W error: out/twin_p1.out, exit 0.")
row("proj-lab2-blanks", "2.5-labs", "project.html lines 133 and 140 (Lab 2); tests/labs/FC1/lab-FC1-project-2.py", "PASS",
    "Two blanks; the page-to-twin difference is exactly the two blanks (claims_checks_r3.py, out/claims_checks_r3.out, section 1). run_labs PASS (out/run_labs_project.out). "
    "Tolerance: tools/coursekit.py compare_output uses tol*(1+|expected|) = 1e-6*(1+102775.09) = 0.103 cent, matching "
    "'about 0.1 cent' (project.html line 149).")
row("proj-lab3-fixture-values", "2.2-numbers / 2.5-labs", "project.html lines 198-276 (Lab 3); tests/labs/FC1/lab-FC1-project-3.py",
    "PASS", "Twin run alone under python -I -W error (exit 0), output in out/twin_p3.out; the 13 printed lines equal the page's "
    "expected block line by line (checked by script in this round). Hand values recomputed in out/numbers_instances_r3.out: "
    "A 10000 (10500/1.05); B 11053, exact 210000/19 = 11052.6316; C (1,5001),(2,15002); D (1,2); rounding events, 10278 "
    "once and 10277 per term; E (2,-98500); F (1,1) price 1 (exact 1/2); G (1,10001) price 5001 (exact 10001/2).")
row("proj-rounding-fixture-terms", "2.2-numbers", "project.html line 193; grader/test_project.py lines 366-368", "PASS",
    "out/numbers_instances_r3.out: exact PV 10277.509103322713 -> 10278; per-term 480.77, 462.28, 9334.46 -> 481 + 462 + 9334 = "
    "10277. Docstring figures correct.")
row("proj-lab3-claim-using-functions", "2.5-labs / prose vs code", "project.html line 198 (Lab 3 hypothesis) vs tests/labs/FC1/lab-FC1-project-3.py",
    "PASS", "Re-checked against the twin this round: fixtures A, B, C, D, F, G and the rounding case go through bond_events, "
    "bond_price and term_by_term_price; fixture E is int arithmetic (line 52: buy = (2, -10 * 9_850)); fixture B's exact value "
    "is a Fraction. The hypothesis sentence matches the code.")
row("proj-expected-equals-output", "2.5-labs", "project.html expected blocks (lines 97, 145, 263-275)", "PASS",
    "run_labs compares every expected block with its output (out/run_labs_all_pages.out, PASS 8/8). Labs 1 and 3 also compared "
    "equal with the twin's run output (claims_checks_r3.py section 2, out/claims_checks_r3.out; out/twin_p1.out, out/twin_p3.out).")
row("proj-hours-arithmetic", "2.6-hours / 2.9-structure", "project.html table#hours (lines 286-293); index.html data-hours-lessons and data-hours-project; curriculum.json FC1 hours",
    "PASS", "Components 1+2+5+4+2+3+3 = 20 (Total row 20). index.html data-hours-lessons=50 (5 lessons x data-hours 10 in "
    "L01-L05, out/hours_attributes_r3.out) and data-hours-project=20 sum to 70, the curriculum.json FC1 hours figure (70). "
    "20/70 = 28.6 % as the hub states. claims_checks_r3.py section 6 (out/claims_checks_r3.out) repeats the sums.")
row("proj-hours-rationale-rows", "2.6-hours", "project.html table#hours rows (lines 286-293)", "PASS",
    "Each of the seven component rows has a one-line rationale; the Total row names the hub figure (20 of the module's 70). "
    "Read this round.")
row("proj-ladder", "2.6-spec ladder", "project.html lines 41-50 and 153-278", "PASS",
    "Rung 1 worked example (Lab 1), Rung 2 completion (Lab 2, graded instantly), Rung 3 specification, Rung 4 stretch marked "
    "'Not graded' (line 314). index.html#placement anchor exists (index.html line 67).")
row("proj-spec-interface", "2.6-spec", "project.html line 161; grader/starter.py lines 16-40", "PASS",
    "Bond(face_cents, coupon_bps, periods).events, bond_price_cents(bond, yield_bps), CashTrade(quantity, price_cents, side, "
    "settlement_day).events match starter.py exactly.")
row("proj-named-conditions", "2.6-autograder-exception-table", "grader/test_project.py must_raise call sites and refused-input list (lines 217-260, 442-449, 493-595, 656-664)",
    "PASS", "must_raise is used for exactly the eight named conditions: periods 0 and -1; face 0 and -1; coupon -1; yield -10000 "
    "and -20000; quantity 0 and -1; price -1; side 0, 2, -2, 3, -3; settlement_day 0 and -1. Accepted boundaries: periods 1, "
    "face 1, coupon 0, yield -9999, quantity 1, price 0, side +1 and -1, settlement_day 1 (tests at lines 225, 242, 263, 454, "
    "503, 547, 580, 598). The page's boundary list (line 290) matches.")
row("proj-test-count", "2.9-count", "project.html line 171 ('69 checks'); grader/test_project.py", "PASS",
    "pytest --collect-only -q on the reference copy: '69 tests collected' (out/collect_only_r3.out). Page count equals the real count.")
row("proj-starter-fails", "2.6-autograder-2", "grader/starter.py", "PASS",
    "Starter under the browser flags: '67 failed, 2 passed' (out/starter_local_r3.out). The two that pass accept any exception "
    "by design (test_non_whole_face and test_bool_periods, page lines 163-165). The 67 failures each name the property and "
    "say 'The student module has no implementation for ...' (out/starter_local_r3.out).")
row("proj-instances", "2.6-instance", "grader/instance.py, seeds 0-19", "PASS",
    "ledgers/FC1/scripts/FC1-c-r3/numbers_instances_r3.py: all 20 seeds satisfy the page's valid-input rules (asserted) and "
    "give 20 distinct bond prices and 20 distinct trade flows (out/numbers_instances_r3.out).")
row("proj-silence-purity", "2.6-autograder-3", "grader/test_project.py lines 627-668 (silence), 671-680 (purity)", "PASS",
    "Silence test covers the valid boundary list on page lines 163 and 629-630; the refused-input silence test covers each named "
    "refusal. Reference and all 14 alternatives pass on seeds 0-19 (out/alternatives_0_19_r3.out; out/run_graders_0_19.out). "
    "Print and warning mutants are killed by these tests (rows of out/mutate_graders_all_r3.out, e.g. r7n01, r8n02, c3n04).")
row("proj-same-suite-pyodide-pytest", "2.6-dual-mode", "grader/test_project.py in Pyodide (page_smoke) and local pytest", "PASS",
    "Pyodide: 'All 69 tests pass' (out/page_smoke_project.out). Local pytest with the page flags on the starter and on the "
    "reference: 69 collected (out/collect_only_r3.out); sampled alternatives: 69 passed (out/sample_counts_r3.out).")
row("proj-mutants-all", "2.6-mutation", "ledgers/FC1/mutants/*.py (89 files: 84 earlier, 5 new r3c_*)", "FAIL",
    "tools/mutate_graders.py --unit FC1 --seeds 0-9 -> 'mutate_graders FC1: FAIL (87/89 killed)' (out/mutate_graders_all_r3.out). "
    "The two survivors are the new r3c_schedule_stops_at_twenty_periods.py and r3c_price_ten_digits_integral_rounding.py "
    "(rows proj-mutant-periods-over-twenty-survivor and proj-mutant-decimal-precision-survivor). The two round-2 survivors "
    "r2c_bond_periods_capped_at_twelve.py and r2c_price_cached_on_first_yield.py are now killed "
    "(by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period and test_one_bond_priced_at_two_yields_gives_each_yield_its_own_price).",
    "Make the two survivors die: see the fix in proj-mutant-periods-over-twenty-survivor and proj-mutant-decimal-precision-survivor. "
    "Re-run tools/mutate_graders.py --unit FC1 --seeds 0-9 until 89/89 are killed.")
row("proj-mutants-v1c-new", "2.6-mutation", "ledgers/FC1/mutants/v1c_*.py (5 round-1 student-error mutants)", "PASS",
    "All five KILLED in out/mutate_graders_all_r3.out: v1c_simple_discount_not_compound, v1c_trade_rounded_to_dollars, "
    "v1c_yield_guard_missing, v1c_price_discounted_at_coupon_rate, v1c_seller_side_refused.")
row("proj-mutants-v2c-new", "2.6-mutation", "ledgers/FC1/mutants/r2c_*.py (4 round-2 student-error mutants)", "PASS",
    "All four KILLED in out/mutate_graders_all_r3.out: r2c_events_change_on_second_call (test_repeated_events_calls_agree), "
    "r2c_trade_settles_one_period_early, r2c_bond_periods_capped_at_twelve (13-15 period test), r2c_price_cached_on_first_yield "
    "(test_one_bond_priced_at_two_yields_gives_each_yield_its_own_price).")
row("proj-mutants-r3c-new", "2.6-mutation", "ledgers/FC1/mutants/r3c_*.py (5 new student-error mutants written this round)", "PASS",
    "Five new complete solution modules, each with a one-line docstring naming a student error: r3c_events_cached_by_face "
    "(KILLED by test_bond_face_one_cent_is_accepted), r3c_discount_factor_float_times_amount (KILLED by the 496-bps test; the "
    "400-bps test alone also fails, out/float_mutant_single_tests_r3.out), r3c_schedule_stops_at_twenty_periods (SURVIVED, row "
    "proj-mutant-periods-over-twenty-survivor), r3c_price_ten_digits_integral_rounding (SURVIVED, row "
    "proj-mutant-decimal-precision-survivor), r3c_price_ten_significant_digits (KILLED by "
    "test_yield_just_above_minus_one_is_accepted, but only because quantize raises InvalidOperation at yield -9999 on the "
    "seed-0 bond, not by a cent error; out/decimal_exception_r3.out: 'seed-0 bond at -9999 raises InvalidOperation').")
row("proj-alternatives", "2.6-autograder-alternatives", "ledgers/FC1/alternatives/a1-a5 (5), ledgers/FC1/scripts/FC1-c-r2/alt (3), ledgers/FC1/scripts/FC1-c-r3/alt (1 new + 5 from r2)",
    "PASS", "Fourteen correct alternatives run under the browser flags on seeds 0-19 (ledgers/FC1/scripts/FC1-c-r3/run_alts_r3.py, "
    "out/alternatives_0_19_r3.out): none fails on any seed. Each run's return code was 0; the runner's success text is a fixed "
    "string that still says 68 (see notes); the real counts are in out/sample_counts_r3.out (69 passed on seeds 0, 3, 7, 19 for "
    "a3, alt_decimal and the new alt_memo_per_yield.py). The new alternative keeps a per-object memo keyed by yield, so the "
    "one-bond-two-yields test does not over-constrain caching.")
row("proj-failure-messages", "2.6-autograder-4", "grader/test_project.py (asserts): 0 bare asserts; scans out/scan_asserts.out, out/scan_leak.out", "PASS",
    "Round-2 FAIL resolved. scan_asserts.py: 52 asserts with a message, 0 bare (out/scan_asserts.out). scan_leak.py: no visible "
    "traceback frame with a literal (out/scan_leak.out, 'scan done'). A failing run shows only the messages (out/leak_*.out, "
    "e.g. 'AssertionError: the final period must carry its coupon and the face together').")
row("proj-failure-message-events-differ", "2.6-autograder-4", "grader/test_project.py line 162 (test_bond_events_match_the_oracle_on_both_cases)", "FAIL",
    "The message 'events differ' names no property: the learner sees only that the event list differs. "
    "ledgers/FC1/scripts/FC1-c-r3/short_messages_r3.py (out/short_messages_r3.out) finds 52 asserts with a message, of which "
    "exactly one has five words or fewer: line 162, 'events differ'.",
    "Replace 'events differ' with the property: 'each event must be the coupon of its period, with the face in the last "
    "period, on both cases'. No expected value in the message.")
row("proj-mutant-periods-over-twenty-survivor", "2.6-mutation / 2.2-numbers", "grader/test_project.py lines 281-300 (13-15 periods) and no test with more than 15 periods; project.html line 177",
    "FAIL",
    "ledgers/FC1/mutants/r3c_schedule_stops_at_twenty_periods.py (Bond.events builds at most twenty periods) SURVIVES all 69 "
    "tests on seeds 0-9 (out/mutate_graders_all_r3.out). Cause: no test prices or lists a bond with more than 15 periods. "
    "project.html line 177 states that the coupon is paid 'in each of periods 1 to periods' and line 165 names no upper limit. "
    "The mutant is wrong on that sentence: Bond(10000,500,24).events() differs from the oracle, and the reference matches it "
    "(out/mutant_probes_r3.out; out/numbers_instances_r3.out, Bond(10000,500,24) at 400 bps = 11525 = oracle).",
    "Add to test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period (or a new test) a 24-period bond: the event list "
    "must equal oracle_events(10000, 500, 24) and bond_price_cents at 400 bps must equal oracle_price (11525 cents). "
    "Re-run mutate_graders --unit FC1 --seeds 0-9 and require r3c_schedule_stops_at_twenty_periods.py to die.")
row("proj-mutant-decimal-precision-survivor", "2.6-mutation / 2.2-numbers", "grader/test_project.py price tests (no price test where a cent is lost at ten significant digits); project.html line 176",
    "FAIL",
    "ledgers/FC1/mutants/r3c_price_ten_digits_integral_rounding.py (bond_price_cents sums in a Decimal context of ten significant "
    "digits) SURVIVES all 69 tests on seeds 0-9 (out/mutate_graders_all_r3.out). Cause: no price test has a value whose cent is "
    "lost at ten significant digits. project.html line 176 states 'The exact value of an output is computed from fractions, and "
    "it is rounded once, to the nearest cent': the mutant does not compute from fractions. Evidence: Bond(10**12+1, 0, 1) at "
    "10000 bps has the exact value 500000000000.5, expected 500000000001; the mutant returns 500000000000 "
    "(out/mutant_probes_r3.out); the reference returns 500000000001.",
    "Add to the exact-half price tests a fixture with a price of about 5 * 10**11 cents: Bond(10**12 + 1, 0, 1) at 10000 bps "
    "must price 500000000001 (the exact half rounds away from zero). Re-run mutate_graders --unit FC1 --seeds 0-9 and require "
    "r3c_price_ten_digits_integral_rounding.py to die.")
row("proj-docstring-dropped-coupons-claim", "2.12-prose / 2.2 (docstring vs computation)",
    "grader/test_project.py lines 281-286 (test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period docstring)", "FAIL",
    "The docstring says: 'at 500 bps a bond is at par for every n, so a schedule that dropped its later coupons would still price "
    "at 10000 cents'. Computed (ledgers/FC1/scripts/FC1-c-r3/numbers_instances_r3.py, out/numbers_instances_r3.out, section "
    "'docstring claim'): a 13-period schedule at 500 bps whose events are (1, 500) and (13, 10500), that is, coupons 2 to 12 "
    "dropped, prices 6044.56 cents, not 10000. A schedule that stops at 12 periods with the face moved to period 12 is a par "
    "bond (10000.0). The sentence is false for a dropped-coupon schedule as written and is learner-visible in the grader source.",
    "Reword to: 'at 500 bps a bond is at par for every n, so a schedule that stopped early, with the face moved to its last "
    "period, would also price at 10000 cents; only the 400 bps price and the event list catch a dropped coupon.'")
row("proj-cards-changed-r3", "2.7-cards", "cards.json FC1-c013, c019, c058, c066, c078, c114 (changed) and c120-c124 (added)", "PASS",
    "Each changed or added card checked against its lesson text this round: c013 (Proposition 4.1 states equity = E - lambda, "
    "L01 lines near 'Proposition 4.1 (equity absorbs the loss)'); c019 and c120 (Definition 1.1 in L02); c058 and c121 (Definition "
    "1.1 in L04, stop activation text); c066 (Proposition 2.3 and the 'no cancellations or modifications' sentence in L04); c078, "
    "c114, c123, c124 (L05 Section 2: c_i = q_i p_i cents, G = sum c_i, Rec_j, Pay_j, NP = sum max(-x_j, 0)); c122 (Proposition 4.1 "
    "and Remark 4.2 in L01, 'a test, not a legal rule'); lesson sentences printed by claims_checks_r3.py section 4 (out/claims_checks_r3.out). All numbers appear in their lessons (out/cards_check.out: 124 cards, 0 "
    "numbers missing). cards_delta_r3.py (out/cards_delta_r3.out): changed = c013, c019, c058, c066, c078, c114; added = c120-c124; no removal.")
row("proj-cards-scan-duplicates", "2.7-cards", "course/modules/FC/FC1/cards.json (124 cards)", "PASS",
    "ledgers/FC1/scripts/FC1-c-r3/cards_check.py over all 124 cards (out/cards_check.out): ids unique; no duplicate normalised front "
    "or back; the only 'problems' are six 'Assumption A1/B1/...' references that L03 states as 'Assumptions A1 to A3' and "
    "'Assumptions B1 to B4' (L03 lines 78-80, 133-135), so they resolve.")
row("proj-cards-numbers-in-lessons", "2.7-cards", "cards.json, every digit run of length >= 2 in back vs the lesson text", "PASS",
    "cards_check.py: for all 124 cards every number in the back (commas removed) appears in its own lesson HTML text; zero misses "
    "(out/cards_check.out: 0 'numbers-not-in-lesson' lines).")
row("proj-cards-sample", "2.7-cards (sampled, then re-derived)", "cards.json: the round-2 sample (c001, c011, c021, ..., c111) and the numeric cards (c010, c012, c016, c037, c043, c082-c084, c092, c093, c097, c098)", "PASS",
    CARRY + "cards.json entries byte-identical (out/cards_delta_r3.out: 'round-2 sample and numeric cards unchanged: True') and "
    "L01-L05.html byte-identical (out/cards_delta_r3.out). Round-2 re-derivations stand: c010 686189 cents, c011 181818 cents, c012, "
    "c016, c037 spread 30 and 0.6 %, c043 profit -600, c082 2172960, c083 Friday 2026-10-30, c084 0.209, c092 181790 and 686189, "
    "c093 -50, c097/c098 3455 (ledgers/FC1/scripts/FC1-c-r2/numbers_r2.py, out/numbers_r2.out of round 2).")
row("proj-cards-citation-R3", "2.7-cards", "cards.json FC1-c054 (lesson L03)", "PASS",
    "Cited 'Lab 1, Part C' with no 'Problem R3'; L03 has the 'Lab 1, Part C' output and the 121-pair grid; resolved by cards_check.py "
    "(out/cards_check.out, no unresolved reference for FC1-c054).")
row("proj-cards-citation-R2", "2.7-cards", "cards.json FC1-c089 (lesson L05)", "PASS",
    "Back cites 'the proof of Proposition 2.1(ii)'. L05 proof of (ii) contains 'By A1 every c_i is non-negative, so Rec_j >= 0 and "
    "Pay_j >= 0' (round-2 read; L05 unchanged since the round-2 pin). Resolved by cards_check.py.")
row("proj-cards-citation-scan", "2.7-cards", "cards.json block references (back and basis)", "PASS",
    "cards_check.py resolves every reference against its own lesson; the only unresolved hits are the six Assumption-letter "
    "false positives above (L03 headings list them).")
row("proj-cards-grades", "2.7-cards / 2.3-grades", "cards.json grade T fields vs lesson data-grade attributes", "PASS",
    "All 24 T-graded cards that cite a Proposition or Corollary cite a claim element with data-grade=\"T\" in their own lesson "
    "(claims_checks_r3.py section 3, out/claims_checks_r3.out: 'T cards citing a Proposition or Corollary: 24 without a T claim: []'; the claim span is '<span class=\"block-title claim\" data-grade=\"T\">Proposition N.M'). The other 16 "
    "T cards cite Examples, Remarks, Problems or Definitions; read, not re-graded (the same treatment as round 2).")
row("proj-spec-scope-vs-curriculum", "2.6-spec (rung 3 matches curriculum scope)", "project.html lines 157, 161; curriculum/02-economics-finance-core.yaml lines 388-395; curriculum/curriculum.json; course/assets/data/program.json", "PASS",
    "Re-checked this round: curriculum.json FC1 project brief reads 'Represent a fixed-rate bond and a trade that settles later "
    "as dated cash-flow objects with a common interface ... Futures, swaps and options follow in FC2.', the same scope as the page "
    "(line 157: 'Futures, swaps and options are not part of this project'). The yaml and program.json are byte-identical since "
    "the round-2 pin, and the grader defines only Bond and CashTrade. claims_checks_r3.py section 5 (out/claims_checks_r3.out): "
    "brief equals the expected sentence: True; scope sentence present: True.")
row("proj-terminology-short-holder", "2.12-prose", "project.html line 179 (Sides and signs); grader/reference.py docstring line 10", "PASS",
    "grep for 'long' and 'short' in project.html and grader/*.py: no hits (out/banned_and_process_words_r3.out). Side +1 is 'the buyer, who pays cash'; -1 is 'the seller, who receives cash'.")
row("proj-prose-banned-phrases", "1.3-1.4 banned phrases", "course/modules/FC/FC1/project.html, cards.json, grader/*.py", "PASS",
    "grep -i for TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'left as an exercise', 'it is important to note', 'studies "
    "show', 'experts agree', 'well known', 'obviously', 'clearly', and process words (builder, verifier, ledger, checkout, mutant, plan, "
    "architect, long, short): no hits (out/banned_and_process_words_r3.out). 'round' hits are the arithmetic word for rounding.")
row("proj-scope-words", "2.2 / prose scope words", "project.html lines 168-171, 176-180, 191, 227-230, 273-276 (changed this round)", "PASS",
    "Changed sentences read in context. The 69-check count matches collect-only. The Lab 3 note's list of checked fixtures now "
    "includes fixture F's events; grep confirms that fixture G's events and the rounding case's events are not tested as lists "
    "(no test calls Bond(10_001, 0, 1).events() or Bond(10000, 500, 3).events(); out/fixture_uses_r3.out).")
row("proj-terms-before-definition", "2.9 terms", "project.html lines 54, 177, 179", "PASS",
    CARRY + "project.html lines 54 and 177-179 are outside every changed hunk (the hunks are at 168-171, 227-230 and 273-276). "
    "event, holder, settlement period and face are defined on line 54 before their use in Lab 1 and the conventions.")
row("proj-notation", "2.9 notation", "project.html symbols y and t (lines 58, 106, 133, 166, 178) vs notation/notation.json", "PASS",
    CARRY + "notation/notation.json byte-identical; the page uses y (per-period yield) and t (period index), neither a registered "
    "macro with another meaning.")
row("proj-footer-claim", "2.9 footer", "project.html line 341 footer", "PASS",
    CARRY + "footer unchanged; page_smoke this round reports no external requests (out/page_smoke_project.out), and course/assets is "
    "byte-identical since the round-2 pin.")
row("proj-saved-as-you-type", "2.9 claim", "project.html line 301; course/assets/js/grader.js", "PASS",
    CARRY + "grader.js byte-identical since the round-2 pin (git diff of course/assets: no change).")
row("proj-references-reading-list", "2.9 references", "project.html Reading section (data-cite mishkin2021economics, harris2002trading)", "PASS",
    CARRY + "references/ byte-identical since the round-2 pin. Both keys exist; the page attributes no statement to either.")
row("proj-cited-year-conflicts", "2.9 registry", "references/references.json; plans/FC1-build-plan.md line 29", "PASS",
    CARRY + "the registry gives harris2002trading year 2002 and mishkin2021economics year 2021; the curriculum string differs. The "
    "page cites the key only, so no year is printed (architect Q3). Recorded in registry_flags, not failed.")
row("proj-data-simulated", "1.4 honest data", "project.html Inputs (line 159), Lab 1 text; grader/instance.py", "PASS",
    CARRY + "the page states 'The values are SIMULATED; none is market data' (line 159); instance.py docstring says the same; no data file is read.")
row("proj-reference-deployment", "repo-wide (not failed)", "course/modules/FC/FC1/grader/reference.py", "PASS",
    CARRY + "reference.py is tracked. Repo-wide note, not an FC1 failure (FINAL-ARCHITECT-RULINGS ruling 4): BLUEPRINT's exclusion "
    "is not enforced by any deploy step. Recorded for the owner.")
row("proj-named-error-message-values", "2.6-autograder-4 (values in messages)", "grader/test_project.py assert messages and pytest.fail texts", "PASS",
    "scan_asserts.py (out/scan_asserts.out) and scan_leak.py (out/scan_leak.out): no assert message or pytest.fail text contains an "
    "expected value; literal values appear only in source lines of hidden frames (__tracebackhide__). A failing run with "
    "--assert=plain prints the messages and no literal values (out/leak_m03_principal_omitted_at_maturity.out).")
row("proj-mutant-periods-13-15-survivor", "2.6-mutation / 2.2-numbers", "grader/test_project.py lines 281-300 vs project.html line 171", "PASS",
    "Round-2 FAIL resolved: r2c_bond_periods_capped_at_twelve.py is KILLED by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period "
    "(out/mutate_graders_all_r3.out). The test now compares the event list and the 400-bps price with the oracle.")
row("proj-mutant-price-cache-survivor", "2.6-mutation / 2.2-numbers", "grader/test_project.py lines 426-439; project.html lines 161, 178", "PASS",
    "Round-2 FAIL resolved: r2c_price_cached_on_first_yield.py is KILLED by test_one_bond_priced_at_two_yields_gives_each_yield_its_own_price "
    "(out/mutate_graders_all_r3.out). The test prices one bond object at two yields and compares each with its own oracle.")
row("proj-docstring-float-claim", "2.12-prose / 2.2 (docstring vs computation)", "grader/test_project.py lines 402-409", "PASS",
    "Round-2 FAIL resolved. The docstring now names the failing form: '(1 + 0.04) ** -1 times 13 gives 12.499999999999998 and rounds "
    "to 12'. Verified (out/numbers_instances_r3.out): 13*(1+0.04)**-1 = 12.499999999999998; 13/(1+0.04) = 12.5. The mutant "
    "r3c_discount_factor_float_times_amount fails test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield "
    "(out/float_mutant_single_tests_r3.out: '1 failed').")

fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 3 (did not build FC1)",
    "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
    "base": "c737272f5bdef4a027417989cd52254555e8a0bb (round 2 of this slice, verifyD2-FC1-c)",
    "checkout": str(ROOT),
    "scratch": "/tmp/fc1c_r3_* (copies of grader files used for collect-only, starter, float mutant, alternatives, probes; "
                "the evidence is archived under ledgers/FC1/scripts/FC1-c-r3/out)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "harris2002trading: registry year 2002 (crossref), curriculum string 2003 (plans/FC1-build-plan.md line 29); page cites the key only (architect Q3). Carried from round 1.",
        "mishkin2021economics: registry year 2021 (record), curriculum string 2022; page cites the key only (architect Q3). Carried from round 1.",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 3 of FC1-c on pin a007712. Delta from c737272 read: project.html (69-check count, term_by_term docstring, "
        "fixture-F interpretation), grader/test_project.py (13-15 test, float docstring, new two-yields test, messages), "
        "lab-FC1-project-3 twin (one docstring line, equal to the page), cards.json (changed c013, c019, c058, c066, c078, c114; "
        "added c120-c124), new r2c mutants already in the tree and the round-3 mutants. Lessons L01-L05, references, notation, "
        "curriculum yaml, program.json, course/assets and reference.py are byte-identical to the round-2 pin. "
        "Every command row was re-run on the pin (out/_exit_codes.txt): check_pages, check_dag, check_projects, run_labs "
        "(project and all pages), run_graders 0-19, mutate_graders 0-9, page_smoke, ruff (grader, labs, repo check), ruff format "
        "(grader and labs), mypy --no-incremental, verify_refs --offline, render_curriculum (output diff clean), build_site --check. "
        "Repo-wide 'ruff format --check .' exits 1 on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py, which is "
        "not in FC1 (outside this slice; not failed here). render_curriculum.py without --check rewrote curriculum/curriculum.json "
        "and CURRICULUM.md with identical content (git diff clean afterwards). "
        "The alternatives runner's success text is a fixed string saying '68 passed'; the real count is 69 (checked by pytest "
        "-q on sampled alternatives: 69 passed). "
        "The Decimal ten-digit mutant r3c_price_ten_significant_digits is killed only by an InvalidOperation at yield -9999 on the "
        "seed-0 bond (decimal quantize overflow), not by a cent error; its integral-rounding sibling survives. "
        "Not checked: the full pytest suite (only the grader and labs are run here); the live verify_refs (network, only --offline); "
        "the Pyodide run of the five new mutants (the browser suite runs the reference only); a line-by-line re-derivation of "
        "the 16 T cards that cite Examples, Remarks, Problems or Definitions (read, not re-graded, as in round 2). Cards: all 124 "
        "cards were run through cards_check.py this round; the cards not changed since the round-2 pin are the same bytes "
        "(cards_delta_r3.py), and their round-2 re-derivations are carried. The alternatives runner (scratch copy of run_alts_r2.py) "
        "prints a fixed '68 passed' string; the real counts are in out/sample_counts_r3.out. Ad hoc checks: checks_r3.sh."
    ),
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
killed = sum(1 for m in mutants if m["killed_by"])
fragment["summary"] = (
    f"{len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
    f"Mutants: {killed}/{len(mutants)} killed on seeds 0-9 (survivors: r3c_schedule_stops_at_twenty_periods, "
    f"r3c_price_ten_digits_integral_rounding). Alternatives: 14/14 pass seeds 0-19. Verdict FAIL."
)
dest = ROOT / "ledgers/FC1/FC1-c.json"
dest.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", dest, counts, "mutants", killed, "/", len(mutants))
