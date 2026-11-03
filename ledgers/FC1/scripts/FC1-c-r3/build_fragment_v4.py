"""Build ledgers/FC1/FC1-c.json (round 3) from the verifier's own outputs under scripts/FC1-c-r3/out/fresh."""
import datetime
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD3-FC1-c")
OUT = "ledgers/FC1/scripts/FC1-c-r3/out/fresh/"

mutants = []
for line in (ROOT / OUT / "mutate_graders_0_9_final.out").read_text().splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*) -> (\S+)(?: \(seed \d+\))?$", line)
    if m:
        status, name, desc, killer = m.groups()
        mutants.append({
            "name": name,
            "description": desc,
            "killed_by": None if status == "SURVIVED" else killer,
        })

R = []


def row(id_, check, location, status, evidence, fix=""):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)


row("proj-check-projects", "2.6-structure", "course/modules/FC/FC1/project.html", "PASS",
    "tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS', exit 0 (" + OUT + "check_projects.out).")
row("proj-check-pages", "2.9-structure", "course/modules/FC/FC1/project.html", "PASS",
    "tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', exit 0 (" + OUT + "check_pages.out).")
row("proj-check-dag", "2.9-DAG", "project.html data-concept links present-value and discount-factor (M1, inside the closure)",
    "PASS", "tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS', exit 0 (" + OUT + "check_dag.out). grep of data-concept on "
    "project.html: only present-value and discount-factor; no FC2, FI1 or BK4 concept is named or linked.")
row("proj-run-labs", "2.5-labs", "project.html Labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py", "PASS",
    "tools/run_labs.py --unit FC1 --page project -> 'run_labs FC1: PASS (3/3)'; --unit FC1 -> 'PASS (8/8)' (" + OUT +
    "run_labs_project_stem.out, run_labs_fc1_all.out). The tool enforces byte-identity of page code and twin, the "
    "python -I -W error twin run, no stderr, and the expected-output rule.")
row("proj-page-smoke", "2.9-smoke", "course/modules/FC/FC1/project.html", "PASS",
    "tools/page_smoke.py --unit FC1 --pages project -> 'page_smoke modules/FC/FC1/project.html: PASS' and in-browser "
    "grader 'All 69 tests pass on seed 1316176078' (" + OUT + "page_smoke_project.out).")
row("proj-run-graders", "2.6-autograder-1", "grader/reference.py, test_project.py, instance.py, starter.py", "PASS",
    "tools/run_graders.py --unit FC1 --seeds 0-49 -> 'run_graders FC1: PASS (reference 50/50 seeds)' (" + OUT +
    "run_graders_0_49.out). Its checks include mypy --strict on reference, starter and instance, and the starter failing the suite.")
row("proj-lint-types", "gate", "course/modules/FC/FC1/grader/*.py, tests/labs/FC1/, ledgers/FC1/mutants/", "PASS",
    "ruff check . -> 'All checks passed!' (" + OUT + "ruff_check_repo.out); mypy --no-incremental -> 'Success: no issues found "
    "in 331 source files' (" + OUT + "mypy.out). ruff format --check . reports one file outside this slice "
    "(ledgers/M3/retired/...); recorded in notes, not a row of FC1-c (" + OUT + "ruff_format_repo.out).")
row("proj-lab1-numbers", "2.2-numbers / 2.5-labs", "project.html lines 58, 97-100 (Lab 1)", "PASS",
    "ledgers/FC1/scripts/FC1-c-r3/numbers_v4.py (" + OUT + "numbers_v4.out): events [(1,5000),(2,5000),(3,105000)]; exact "
    "present value 102775.091033 at 400 bps; price 102775; trade event (2,-98500). Page prose and expected block agree.")
row("proj-lab2-blanks", "2.5-labs", "project.html lines 133 and 140 (Lab 2); tests/labs/FC1/lab-FC1-project-2.py line 34",
    "PASS", "Two blanks: exponent `period` (line 133) and `-side * quantity * price_cents` (line 140), matching the interpretation "
    "text (line 149). The completion tolerance stated on line 149 (about 0.1 cent) is 1e-6 * (1 + 102775.09) = 0.103 under the "
    "run_labs.py rule tol*(1+|expected|). run_labs PASS (out/fresh/run_labs_project_stem.out).")
row("proj-lab3-fixture-values", "2.2-numbers / 2.5-labs", "project.html lines 198-276 (Lab 3); tests/labs/FC1/lab-FC1-project-3.py",
    "PASS", "numbers_v4.out re-derives every printed Lab 3 value: A [(1,10500)] price 10000; B 11053 exact 11052.6316; C "
    "[(1,5001),(2,15002)]; D [(1,2)]; rounding events [(1,500),(2,500),(3,10500)], once 10278, term-by-term 10277; E (2,-98500); "
    "F [(1,1)] price 1 (exact 1/2); G [(1,10001)] price 5001 (exact 10001/2). All equal the expected block; run_labs PASS.")
row("proj-rounding-fixture-terms", "2.2-numbers", "project.html line 193; grader/test_project.py lines 365-372", "PASS",
    "Exact present value 10277.509103 -> 10278 once; terms 480.7692307, 462.2781065, 9334.4617660 -> 481+462+9334 = 10277 "
    "(numbers_v4.out). Matches page line 193 and test docstring lines 366-368.")
row("proj-lab3-claim-using-functions", "2.5-labs / prose vs code", "project.html line 198 (Lab 3 hypothesis) vs twin lines 236-259",
    "PASS", "Hypothesis says functions for the bond and exact arithmetic for the trade and the exact values. The lab code uses "
    "bond_events and bond_price, an int trade event `(2, -10 * 9_850)`, and Fraction for exact values (page lines 236-259).")
row("proj-expected-equals-output", "2.5-labs", "project.html expected blocks lines 97-100, 145-148, 263-275", "PASS",
    "run_labs.py compares numbers within tol*(1+|expected|) and other tokens exactly; all three projects labs PASS (" + OUT +
    "run_labs_project_stem.out).")
row("proj-hours-arithmetic", "2.6-hours / 2.9-structure",
    "project.html table#hours lines 286-293, data-hours-project line 34; index.html line 29", "PASS",
    "Table components 1+2+5+4+2+3+3 = 20; equals data-hours-project=20 and the total row. Hub: data-hours-lessons=50 + "
    "data-hours-project=20 = 70 = module hours. Ruling (plans/FINAL-ARCHITECT-RULINGS.md, Rulings in verifier-rules): hours are "
    "design targets, only arithmetic inconsistency fails.")
row("proj-hours-rationale-rows", "2.6-hours", "project.html table#hours rows lines 286-293", "PASS",
    "All eight rows (including the total) carry a one-line rationale cell.")
row("proj-ladder", "2.6-spec ladder", "project.html lines 41-50 (ladder), 56-102 (rung 1), 104-150 (rung 2), 153-172 (rung 3), 312-319 (rung 4)",
    "PASS", "Rung 1: Lab 1 solved with a comment on each step. Rung 2: Lab 2 class completion, graded instantly, twin = completed "
    "solution. Rung 3: specification and autograder. Rung 4: stretch, marked not graded and open-ended.")
row("proj-spec-interface", "2.6-spec", "project.html line 161; grader/starter.py lines 16-40; grader/reference.py",
    "PASS", "Names and signatures on the page: Bond(face_cents, coupon_bps, periods).events(); bond_price_cents(bond, yield_bps); "
    "CashTrade(quantity, price_cents, side, settlement_day).events(). Identical in starter.py and reference.py.")
row("proj-named-conditions", "2.6-exception-table", "project.html lines 163-167; grader/test_project.py lines 215-301, 442-453, 493-596, 684-701",
    "PASS", "Eight named conditions (periods<1, face<=0, coupon<0, yield<=-10000, quantity<1, price<0, side not in {+1,-1}, "
    "settlement_day<1), each tested refused and at the boundary accepted (side tested at 0,2,-2,3,-3 refused, +1 and -1 accepted). "
    "must_raise is called only for those; non_whole_face and bool_periods accept any exception (lines 684-701).")
row("proj-test-count", "2.9-count", "project.html line 171 ('69 checks'); grader/test_project.py", "PASS",
    "pytest --collect-only -q test_project.py in scratch with reference.py as instruments.py -> '69 tests collected' ("
    + OUT + "collect_only.out).")
row("proj-starter-fails", "2.6-autograder-2", "grader/starter.py", "PASS",
    "run_graders.py --unit FC1 --seeds 0-49 PASS includes the starter-fails check (" + OUT + "run_graders_0_49.out); "
    "the two tests that pass on the starter are the two any-exception tests by design.")
row("proj-instances", "2.6-instance", "grader/instance.py seeds 0-19", "PASS",
    "ledgers/FC1/scripts/FC1-c-r3/instances_v4.py (" + OUT + "instances_0_19.out): all 20 instances valid by the page's ranges; "
    "20 distinct bond prices and 20 distinct trade cash flows; periods take 1..8.")
row("proj-silence-purity", "2.6-autograder-3", "grader/test_project.py lines 627-668", "PASS",
    "Silence checked on 14 valid and 8 refused inputs (lines 631-668); the reference passes all 69 on seeds 0-49 (" + OUT +
    "run_graders_0_49.out).")
row("proj-same-suite-pyodide-pytest", "2.6-dual-mode", "grader/test_project.py", "PASS",
    "Local pytest: run_graders PASS 50/50; in-browser (Pyodide) 'All 69 tests pass' on the reference (" + OUT +
    "page_smoke_project.out).")
row("proj-mutants-all", "2.6-mutation", "ledgers/FC1/mutants/*.py (94 files)", "FAIL",
    "tools/mutate_graders.py --unit FC1 --seeds 0-9 -> 'mutate_graders FC1: FAIL (92/94 killed)' (" + OUT +
    "mutate_graders_0_9_final.out). Survivors: r3c_schedule_stops_at_twenty_periods.py and "
    "r3c_price_ten_digits_integral_rounding.py (rows proj-mutant-schedule-cap-survivor, proj-mutant-price-digits-survivor).",
    "Kill both survivors with new grader tests (see those rows), then re-run `tools/mutate_graders.py --unit FC1 --seeds 0-9` "
    "until 94/94 are killed. Ruling 9 forbids a survivor in mutants/: a behaviour stated on the page must be killed, not moved.")
row("proj-mutants-v1c-new", "2.6-mutation", "ledgers/FC1/mutants/v1c_*.py (5 student-error mutants)", "PASS",
    "All five killed on seed 0 (" + OUT + "mutate_graders_0_9_final.out): v1c_seller_side_refused by test_seller_receives_cash_at_settlement; "
    "v1c_simple_discount_not_compound and v1c_price_discounted_at_coupon_rate by test_bond_price_with_thirteen_to_fifteen_periods_"
    "uses_every_period; v1c_trade_rounded_to_dollars by test_trade_has_one_settlement_event_on_its_settlement_day; "
    "v1c_yield_guard_missing by test_yield_at_minus_one_is_refused.")
row("proj-mutants-v2c-new", "2.6-mutation", "ledgers/FC1/mutants/r2c_*.py (4 student-error mutants)", "PASS",
    "All four killed on seed 0: r2c_bond_periods_capped_at_twelve by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period; "
    "r2c_events_change_on_second_call by test_repeated_events_calls_agree; r2c_price_cached_on_first_yield by "
    "test_one_bond_priced_at_two_yields_gives_each_yield_its_own_price; r2c_trade_settles_one_period_early by "
    "test_trade_has_one_settlement_event_on_its_settlement_day.")
row("proj-mutants-r3c-killed", "2.6-mutation", "ledgers/FC1/mutants/r3c_discount_factor_float_times_amount.py, r3c_events_cached_by_face.py, r3c_price_ten_significant_digits.py",
    "PASS", "Killed on seed 0 (" + OUT + "mutate_graders_0_9_final.out). The third is killed only by test_yield_just_above_minus_one_is_accepted, "
    "an incidental kill: the cent loss itself is not caught (see proj-mutant-price-digits-survivor).")
row("proj-mutants-v4c-new", "2.6-mutation", "ledgers/FC1/mutants/v4c_*.py (5 new student-error mutants by this verifier)", "PASS",
    "Written this round by ledgers/FC1/scripts/FC1-c-r3/make_mutants_v4.py from reference.py, all killed on seed 0: "
    "v4c_zero_amount_events_dropped by test_bond_zero_coupon_pays_only_the_face_in_the_last_period; v4c_trade_sign_not_flipped by "
    "test_trade_has_one_settlement_event_on_its_settlement_day; v4c_coupon_truncated_not_rounded by "
    "test_bond_events_match_the_oracle_on_both_cases; v4c_discount_exponent_one_short by "
    "test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period; v4c_float_discount_half_up by "
    "test_bond_coupon_is_exact_for_a_face_too_large_for_floats.")
row("proj-alternatives", "2.6-autograder-alternatives", "ledgers/FC1/alternatives/a1..a5 and ledgers/FC1/scripts/FC1-c-r3/alt_v4/alt_decimal_half_up.py",
    "PASS", "ledgers/FC1/scripts/FC1-c-r3/run_alts_v4.py ... 50 (" + OUT + "alternatives_0_49.out): all six correct alternatives "
    "(list comprehensions, generator methods, Fraction throughout, integer division, frozen dataclass reduce, 60-digit Decimal) "
    "pass 50/50 seeds. The float implementation is a mutant under ruling 10 (v4c_float_discount_half_up.py) and fails 50/50.")
row("proj-failure-messages", "2.6-autograder-4", "grader/test_project.py (all assert and pytest.fail sites)", "PASS",
    "scan_messages_v4.py (" + OUT + "scan_messages.out): bare asserts: none (the two round-2 bare asserts at former lines 647-652 now "
    "carry messages at lines 675-681). One short message, line 162 'events differ', names the property (events) and is accepted; "
    "the numbers in messages are input descriptors (2**53, 501 units, 12 periods), never a computed answer.")
row("proj-cards-scan-duplicates", "2.7-cards", "course/modules/FC/FC1/cards.json (124 cards)", "PASS",
    "ledgers/FC1/scripts/FC1-c-r3/cards_scan_v4.py (" + OUT + "cards_scan.out): 124 entries, 124 unique ids FC1-c001..c124, "
    "no duplicate fronts, no duplicate backs. Non-sequential order is not a defect (ruling 2).")
row("proj-cards-numbers-in-lessons", "2.7-cards", "course/modules/FC/FC1/cards.json; L01-L05.html", "PASS",
    "cards_scan_v4.py: every Definition, Proposition, Remark, Section and Example number in a card occurs in the card's own "
    "lesson. The regex flags 'Assumption A1..B4' of L01 and L03 (lines in " + OUT + "cards_scan.out): read by hand, these are "
    "the items A1-A3 of Assumption 2.0 (L01) and A1-A3, B1-B4 of the Assumptions blocks (L03), so they are present.")
row("proj-cards-sample", "2.7-cards (sampled, re-derived)", "cards.json FC1-c010, -020, -030, -040, -050, -060, -070, -080, -090, -100, -110, -120",
    "PASS", "Each re-derived against its lesson: c010 Example 3.3 (6861.8940391 -> 6,861.89) L01; c020 Assumption 1.3 L02; c030 "
    "Example 3.1 and Lab 2 Part C L02; c040 Definition 2.1 P=C+I*m_n L03; c050 Proposition 3.2 (T) L03; c060 Remark 1.2 L04; c070 "
    "Misconceptions 1 L04; c080 Proposition 2.2 (T) L05; c090 Section 4 and SETTLEMENT_LAG = 2 L05; c100 Proposition 2.3 (T) L04; "
    "c110 Assumption 2.0 A2 L01; c120 Definition 1.1 L02. Sample of 12 of 124, per 10-card rule.")
row("proj-cards-changed-subjects", "2.7-cards", "cards.json FC1-c013, -019, -058, -066, -078, -114, -120, -121, -122, -123, -124",
    "PASS", "Re-read against the current lesson text: c013 and c122 vs Proposition 4.1 and Remark 4.2 (L01); c019 and c120 vs "
    "Definition 1.1 (L02); c058 and c121 vs Definition 1.1 buy and sell stop (L04); c066 vs Proposition 2.3 (L04): the 'no withdrawal "
    "or modification' sentence follows from Proposition 2.2 (an event is an arrival or stop activation) and C counts only "
    "market-order cancellations; c078, c114, c123, c124 vs L05 Section 2 (c_i = q_i p_i; G = sum c_i; Rec_j, Pay_j, x_j; NP).")
row("proj-cards-citation-R3", "2.7-cards", "cards.json FC1-c054 (L03)", "PASS",
    "Carried from round 2 (FC1-c054 entry JSON-identical and L03.html byte-identical since c737272f, git diff --quiet): the cited "
    "Proposition 3.2 (T) and Lab 1 Part C claims are unchanged.")
row("proj-cards-citation-R2", "2.7-cards", "cards.json FC1-c089 (L05)", "PASS",
    "Carried from round 2 (FC1-c089 entry JSON-identical and L05.html byte-identical since c737272f, git diff --quiet).")
row("proj-cards-citation-scan", "2.7-cards", "cards.json block references", "PASS",
    "cards_scan_v4.py over all 124 cards (see proj-cards-numbers-in-lessons); no citation to a missing label.")
row("proj-cards-grades", "2.7-cards / 2.3-grades", "cards.json grade fields T (40), C (15) vs lesson data-grade attributes",
    "PASS", "T grades checked on the six changed or sampled T cards: c013 and c122 (Proposition 4.1, L01 data-grade=T), c050 "
    "(Proposition 3.2, L03 data-grade=T), c066 and c100 (Proposition 2.3, L04 T), c080 (Proposition 2.2, L05 T). C grades checked on "
    "the sampled c030 (the Example 3.1 block carries the C marker, L02) and c054 (the Lab 1 Part C marker, L03). The other 13 C-graded "
    "cards were not each checked against a lesson marker (honest gap).")
row("proj-spec-scope-vs-curriculum", "2.6-spec (rung 3 matches curriculum scope)", "project.html lines 157, 161; curriculum/02-economics-finance-core.yaml lines 388-395; plans/FINAL-ARCHITECT-RULINGS.md item 5", "PASS",
    "Binding ruling 5 limits FC1's project to cash instruments (bond and a trade that settles later), and the curriculum brief "
    "(yaml 388-391) matches: 'Represent a fixed-rate bond and a trade that settles later ... Futures, swaps and options follow in "
    "FC2.' Page line 157 states the same. The older plan wording ('trade-lifecycle and order-book simulator') is superseded.")
row("proj-terminology-short-holder", "2.12-prose", "project.html line 54 (holder), line 179 (Sides and signs); grader/reference.py docstring line 10",
    "PASS", "holder is defined on line 54 before first use; sign rule (side +1 buyer pays, -1 seller receives) identical on line 179, "
    "reference.py line 10 and starter.py.")
row("proj-prose-banned-phrases", "1.3-1.4 banned phrases", "course/modules/FC/FC1/project.html and cards.json", "PASS",
    "check_pages.py PASS (banned-phrase check, " + OUT + "check_pages.out); grep of project.html for verifier, builder, round N, draft, "
    "TODO, placeholder, we, our, agent: no hits.")
row("proj-scope-words", "2.2-prose scope words", "project.html lines 163, 176, 180, 184, 276; grader/test_project.py lines 9-13",
    "PASS", "Universal words checked: 'every named condition' and 'no function prints or warns' (line 163) are learner requirements "
    "tested on listed inputs; the page does not claim exhaustive checking. 'Each events() call returns the same list' (line 180) is "
    "tested (test_repeated_events_calls_agree). Line 276 mapping of fixtures to tests matches test names. Fixture G and rounding-case "
    "event lists are not asserted as lists (grep of test_project.py: only prices at lines 370, 387).")
row("proj-terms-before-definition", "2.9-terms", "project.html lines 38, 54, 58, 178", "PASS",
    "event, holder, face, coupon, basis point, settlement period are defined on line 54 before Lab 1 (line 58); present value and "
    "discount factor are linked to M1; cash instrument is defined in L02 Example 3.1 (the form axis) before this project.")
row("proj-notation", "2.9-notation", "project.html symbols y and t (lines 58, 106, 178); notation/notation.json", "PASS",
    "notation.json registers 8 program-wide symbols (T, Phi, and others), none used here. y (per-period yield, line 54 'per-period "
    "yield of 400 basis points') and t (period, line 54 and 178) are defined on this page. No \\mathbb{R} on the page (grep count 0).")
row("proj-footer-claim", "2.9-claim", "project.html line 341 footer", "PASS",
    "Footer: 'nothing you write leaves it'. grader.js fetches only the grader's own files (grader.js line 18 fetch(url)); "
    "saving uses IndexedDB (store.js line 2); page_smoke PASS includes zero requests to other hosts.")
row("proj-saved-as-you-type", "2.9-claim", "project.html line 301", "PASS",
    "'Your code is saved in this browser as you type': grader.js lines 59-61, an input listener that calls store.put after a 400 ms timer.")
row("proj-references-reading-list", "2.9-references", "project.html lines 321-333 (data-cite keys)", "PASS",
    "data-cite mishkin2021economics and harris2002trading both exist in references/references.json (status verified). The page "
    "prints no year and states that it attributes no statement to either.")
row("proj-cited-year-conflicts", "2.9-registry", "references/references.json entries; curriculum/02-economics-finance-core.yaml lines 384-385",
    "PASS", "Registry: mishkin2021economics year 2021 (curriculum '13th ed., 2022'); harris2002trading year 2002 (curriculum '(2003)'). "
    "The project page prints no year, so there is no prose conflict (architect Q3 b). Recorded in registry_flags; not corrected here.")
row("proj-data-simulated", "1.4 honest data / 2.8", "project.html Inputs (line 159), Lab 1 (line 54, 72); grader/instance.py docstring and label",
    "PASS", "No data file: the project labs read nothing. Every value is labelled SIMULATED (page line 54 and line 159; instance.py label).")
row("proj-reference-deployment", "repo-wide (not failed)", "course/modules/FC/FC1/grader/reference.py", "PASS",
    "Ruling 4 (FINAL-ARCHITECT-RULINGS): deployment exclusion is not a defect of this slice; not failed.")
row("proj-mutant-periods-13-15-survivor", "2.6-mutation / 2.2-numbers", "grader/test_project.py lines 281-300; project.html line 171",
    "PASS", "Round-2 survivor r2c_bond_periods_capped_at_twelve is now killed by test_bond_price_with_thirteen_to_fifteen_periods_uses_"
    "every_period on seed 0 (" + OUT + "mutate_graders_0_9_final.out). Re-verified from scratch; the round-2 FAIL does not reproduce.")
row("proj-mutant-price-cache-survivor", "2.6-mutation / 2.2-numbers", "grader/test_project.py lines 426-439; project.html line 161, 178",
    "PASS", "Round-2 survivor r2c_price_cached_on_first_yield is now killed by test_one_bond_priced_at_two_yields_gives_each_yield_its_own_price "
    "(seed 0; " + OUT + "mutate_graders_0_9_final.out).")
row("proj-docstring-float-claim", "2.2 / prose (docstring vs computation)", "grader/test_project.py lines 402-409",
    "PASS", "Docstring now says a float discount factor (1 + 0.04) ** -1 times 13 gives 12.499999999999998 and rounds to 12. "
    "numbers_v4.out: 13 * (1 + 0.04) ** -1 = 12.499999999999998 and round() = 12; exact 25/2 rounds to 13. Claim holds.")
row("proj-named-error-message-values", "2.6-autograder-4", "grader/test_project.py (all messages)", "PASS",
    "scan_messages_v4.py: messages with 2+ digit numbers (lines 212, 277, 310, 518, 528, 539) describe inputs, not answers.")
row("proj-mutant-schedule-cap-survivor", "2.6-mutation", "ledgers/FC1/mutants/r3c_schedule_stops_at_twenty_periods.py vs grader/test_project.py lines 281-300 and project.html line 177",
    "FAIL", "Mutant: Bond.events() builds at most twenty periods (face moved to period 20). It survives all 69 tests on seeds 0-9 "
    "(" + OUT + "mutate_graders_0_9_final.out). It is not equivalent: probe_survivors_v4.py (" + OUT + "probe_survivors_v4.out) gives "
    "Bond(10000,500,21).events() 20 events vs 21, and Bond(10000,500,24) at 400 bps 11359 vs 11525. Page line 177 states the coupon "
    "is paid in each of periods 1 to periods, and no grader test exceeds 15 periods.",
    "Add a test to test_project.py: for periods 24, events() equals oracle_events(10_000, 500, 24) and bond_price_cents(Bond(10_000, 500, 24), 400) "
    "equals oracle_price(...) (= 11525). Then re-run tools/mutate_graders.py --unit FC1 --seeds 0-9 and require this mutant killed.")
row("proj-mutant-price-digits-survivor", "2.6-mutation / 2.2-numbers", "ledgers/FC1/mutants/r3c_price_ten_digits_integral_rounding.py vs grader/test_project.py lines 318-416; project.html lines 163, 176",
    "FAIL", "Mutant: bond_price_cents sums in a Decimal context of ten significant digits. It survives all 69 tests on seeds 0-9 "
    "(" + OUT + "mutate_graders_0_9_final.out). Not equivalent: probe_survivors_v4.out gives Bond(10**10+1,0,1) at 10000 bps 5000000000 "
    "vs reference 5000000001, and Bond(10**12+1,0,1) 500000000000 vs 500000000001. Page line 176 states the exact value is "
    "computed from fractions and rounded once. The mutant's own docstring says 'more than seven digits'; the first failing case has "
    "eleven digits, so that description needs correcting when the file is rewritten.",
    "Add a grader test: bond_price_cents(Bond(10**10 + 1, 0, 1), 10_000) == 5_000_000_001 and bond_price_cents(Bond(10**12 + 1, 0, 1), 10_000) "
    "== 500_000_000_001 (exact halves above ten significant digits). Re-run tools/mutate_graders.py --unit FC1 --seeds 0-9 and require the mutant killed.")

NOTES = (
    "Round 3 of FC1-c on pin a007712f (base c737272f). Delta read hunk by hunk: project.html (line 171 '69 checks'; line 227 "
    "docstring; lines 273-276 Lab 3 interpretation), grader/test_project.py (13-15-period test; new one-bond-two-yields test; "
    "__tracebackhide__ and messages at the two former bare asserts; repeated-calls messages), cards.json (FC1-c013, -019, -058, -066, "
    "-078, -114 revised; FC1-c120..c124 added), tests/labs/FC1/lab-FC1-project-3.py (docstring line only), mutants r2c_* (4 added). "
    "Every round-2 non-PASS row re-verified from scratch: proj-failure-messages now PASS; proj-mutants-all still FAIL (new survivors); "
    "proj-mutant-periods-13-15-survivor and proj-mutant-price-cache-survivor now PASS (killed); proj-docstring-float-claim now PASS. "
    "Mutants: 92/94 killed on seeds 0-9. Two survivors are the untracked r3c_* files already in mutants/ from an earlier run in this "
    "checkout; they are counted and cited (ruling 9). Alternatives: 6 correct implementations pass seeds 0-49. "
    "Plan item (5), a float alternative, fails 50/50 on the page's exact rule and is a mutant (ruling 10). "
    "Scope ruling 5 is binding: the project is cash instruments only. Out of slice: ruff format --check . reports one file in "
    "ledgers/M3/retired (outside FC1). Stale files in ledgers/FC1/scripts/FC1-c-r3/out/ (top level) pre-date this run and are not cited; "
    "the cited outputs are in out/fresh/. Not checked: full repo pytest (only tests -k FC1 in test_labs, test_run_labs, test_page_checks: "
    "8 passed); live verify_refs (only --offline: 560 entries, 0 problems); Pyodide run of the new mutants (browser suite ran the reference "
    "only); individual regrade of 15 C-graded cards (sampled); cards.json not compared line by line beyond the sample and changed cards."
)

fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 3 (did not build FC1)",
    "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
    "base": "c737272f5bdef4a027417989cd52254555e8a0bb (round 2 of this slice)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-FC1-c",
    "scratch": "/tmp/fc1c_v4_alts, /tmp/fc1c_v4_collect, /tmp/fc1c_v4_leak (copies of grader files; archived evidence under ledgers/FC1/scripts/FC1-c-r3/)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [
        "harris2002trading: registry year 2002 (crossref), curriculum string 2003 (curriculum/02-economics-finance-core.yaml line 385); page cites the key only (architect Q3 b). Carried from round 2.",
        "mishkin2021economics: registry year 2021 (record), curriculum string 2022 (yaml line 384); page cites the key only (architect Q3 b). Carried from round 2.",
    ],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": f"{len(R)} rows: {sum(r['status'] == 'PASS' for r in R)} PASS, {sum(r['status'] == 'FAIL' for r in R)} FAIL, 0 UNVERIFIABLE. Mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed on seeds 0-9. Verdict FAIL.",
}
out = ROOT / "ledgers/FC1/FC1-c.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n")
print("rows", len(R), "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]), "verdict", fragment["verdict"])
