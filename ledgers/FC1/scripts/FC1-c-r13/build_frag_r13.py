"""Round-13 builder for the FC1-c fragment: rows and mutant list from this round's outputs (run from the checkout root)."""
import json
import re
from pathlib import Path

S = "ledgers/FC1/scripts/FC1-c-r13"
CARRY12 = "Carried from round 12 (files byte-identical since the previous pin 460b696): "

mutants = []
for line in Path(f"{S}/mutate_FC1_s0-9_r13.out").read_text().splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, where = m.groups()
    killed_by = None
    if status == "KILLED":
        killed_by = re.sub(r" \(seed \d+\)$", "", where).strip()
    mutants.append({"id": fname.removesuffix(".py"), "description": desc.strip(), "killed_by": killed_by})
assert len(mutants) == 75, len(mutants)

rows = [
 # --- run and gate results re-run this round ---
 dict(id="proj-run-graders", check="2.6-autograde-reference", location="course/modules/FC/FC1/grader/reference.py; tools/run_graders.py",
      status="PASS", evidence=f"Re-run: .venv/bin/python tools/run_graders.py --unit FC1 --seeds 0-49 -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.2 s)' ({S}/run_graders_FC1_0-49.out)."),
 dict(id="proj-collect-count-65", check="2.6-page-count", location="project.html line 171; grader/test_project.py",
      status="PASS", evidence=f"project.html line 171 says 'runs 65 checks'. Collect-only on the reference: '65 tests collected' ({S}/alts_and_collect.out line 2). Grep: 65 'def test_' lines in test_project.py. Browser: 'All 65 tests pass on seed 923639711' ({S}/page_smoke_project.out)."),
 dict(id="proj-browser-suite", check="2.6-autograder-both", location="project.html section#grader; course/assets/js/grader.js lines 95-110",
      status="PASS", evidence=f"page_smoke --unit FC1 --pages project: 'in-browser grader: All 65 tests pass' and 'page_smoke FC1: PASS' ({S}/page_smoke_project.out). grader.js renders r.test and r.message per result, so a failing test shows its name."),
 dict(id="proj-alternatives-five", check="2.6-autograde-alternatives", location="ledgers/FC1/alternatives/a1..a5 (a5 replaced this round)",
      status="PASS", evidence=f"{S}/alts_and_collect.sh run: a1_list_comprehension_events, a2_generator_methods, a3_fraction_throughout, a4_integer_division_half_up, a5_frozen_dataclass_reduce and reference.py each have 0 failing seeds of 20 (seeds 0-19, -W error). The round-12 float a5 is gone from the tree (git diff 460b696 762f636 shows it deleted; the replacement is exact Fraction arithmetic with one half-away rounding)."),
 dict(id="proj-instances-20", check="2.6-autograde-instances", location="grader/instance.py (byte-identical since 460b696)",
      status="PASS", evidence=f"{S}/instances_20_r13.py over seeds 0,2,...,38: the reference accepts all 20 instances (no exception); 20 distinct bond prices and 20 distinct trade events ({S}/instances_20_r13.out). Answers change, not only labels. Seeds 0-49 pass run_graders 50/50."),
 dict(id="proj-starter-vs-spec", check="2.6-spec", location="grader/starter.py; project.html line 161 (Required outputs)",
      status="PASS", evidence=CARRY12 + "grader/starter.py and project.html Required outputs (the names and signatures). starter.py is byte-identical at 762f636 (git diff --quiet 460b696 762f636). project.html changed only at line 171 in the delta, outside this sentence."),
 dict(id="proj-spec-questions", check="2.6-spec", location="project.html section#spec lines 153-172",
      status="PASS", evidence="Re-read this round, lines 153-172 (Context, Inputs, Required outputs, Constraints, Grading mode). The rules a student needs are stated: period indexing from 1 (line 177 Conventions), the rate rule (line 178), the sign rule (line 179), the rounding rule (line 176), the events list shape and the refused conditions (lines 163-167). No question left unanswered that the autograder checks. Grading mode line 171 now says 65 checks, which matches the collect-only count."),
 dict(id="proj-ladder", check="2.6-spec-ladder", location="project.html section#ladder lines 41-50",
      status="PASS", evidence="Re-read lines 41-50: rung 1 annotated Lab 1, rung 2 graded completion Lab 2 (class lab completion), rung 3 specification and grader, rung 4 stretch, not graded. check_projects --unit FC1: PASS ({S}/check_projects_FC1.out)."),
 dict(id="proj-stretch-scope", check="2.6-spec", location="project.html section#stretch lines 312-318",
      status="PASS", evidence=CARRY12 + "project.html section#stretch (the only project.html hunk in the delta is line 171)."),
 dict(id="proj-local-command", check="2.6-spec", location="project.html section#local lines 305-310; grader/starter.py",
      status="PASS", evidence=CARRY12 + "project.html section#local (no hunk in the delta) and grader/starter.py. The local command QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py was run here on the reference with the alternatives harness (" + S + "/alts_and_collect.out)."),
 # --- labs ---
 dict(id="proj-lab1-twin", check="2.5-labs", location="project.html lab-FC1-project-1 (lines 56-102); tests/labs/FC1/lab-FC1-project-1.py",
      status="PASS", evidence=f"run_labs --unit FC1: PASS (8/8) ({S}/run_labs_FC1.out). {S}/page_vs_twin_r13.py: page code equals the twin (only the trailing newline differs); twin exit 0 under python -I -W error; expected block equals the twin output ({S}/page_vs_twin_r13.out). Printed: 102775.091033, 102775, (2, -98500) (recomputed in {S}/numbers_r13.out)."),
 dict(id="proj-lab2-completion", check="2.5-labs-completion", location="project.html lab-FC1-project-2 (lines 104-150); tests/labs/FC1/lab-FC1-project-2.py",
      status="PASS", evidence=f"{S}/page_vs_twin_r13.out: the page code differs from the twin only at the two blanks (line 'exact_price = sum(... ** ___ ...)' and 'trade_event = (settlement_day, ___)'); every other page line equals the twin line. The expected block equals the twin output. run_labs FC1: PASS (8/8)."),
 dict(id="proj-lab2-docstring", check="2.9-prose", location="project.html line 107; tests/labs/FC1/lab-FC1-project-2.py docstring",
      status="PASS", evidence="Docstring line 1 'Rung 2 completion: the worked example, with two blanks for you to fill in.' matches the lab code, which has exactly the two blanks."),
 dict(id="proj-lab3-fixtures", check="2.5-labs", location="project.html lab-FC1-project-3 (lines 196-276); tests/labs/FC1/lab-FC1-project-3.py",
      status="PASS", evidence=f"Twin exit 0 under python -I -W error; expected block equals its output ({S}/page_vs_twin_r13.out). Every printed value recomputed with Fraction and float in {S}/numbers_r13.out: fixture B 11052.631578947368 -> 11053; rounding case exact 10277.509103322713 -> 10278, term-by-term 481+462+9334 = 10277; fixture F 1/2 -> 1; fixture G 5000.5 -> 5001; fixture C coupon 5001, D coupon 1."),
 dict(id="proj-prose-numbers", check="2.2-numbers", location="project.html lines 58, 176, 186-193, 198 and 275",
      status="PASS", evidence=f"Recomputed with Fraction this round ({S}/numbers_r13.out): line 58 PV 102775.091033 -> 102775 (the .091033 is below one half); fixture A 10000; fixture B 210000/19 = 11052.6316 -> 11053; fixture C 5000.5 -> 5001 and 15002; fixture D 0.5 -> 1; fixture F 1/2 -> 1; fixture G 5001; rounding case 10277.509103 -> 10278, terms 480.77, 462.28, 9334.46; trade (2, -98500). The 496 bps figure in the test docstring: coupon 30506.7015 -> 30507, PV 1652812.5, float gives 1652812.4999999998."),
 dict(id="proj-fixture-claims", check="2.9-prose", location="project.html lines 186-193 and 275 vs grader/test_project.py",
      status="PASS", evidence="Mapped each claim to a test: fixture A events (test_bond_one_period_fixture_is_par_coupon_plus_face) and price (test_bond_price_one_period_at_its_coupon_rate_is_par); fixture B price (test_bond_price_negative_yield_is_above_the_undiscounted_value); fixtures C and D events (test_bond_half_cent_coupon_rounds_away_from_zero, test_bond_half_cent_on_a_one_cent_face_rounds_up_not_to_zero); fixture E (test_buyer_pays_cash_at_settlement, test_seller_receives_cash_at_settlement); fixtures F and G prices (test_bond_price_exact_half_cent_rounds_away_from_zero, test_bond_price_exact_half_at_five_thousand_point_five_rounds_up); rounding price (test_bond_price_hand_fixture_rounds_the_sum_once). The page says fixture G's and the rounding case's events are not checked as lists: true, no test asserts those lists literally."),
 dict(id="proj-hours-arithmetic", check="2.6-hours", location="project.html section#budget lines 283-292; data-hours-project line 34; index.html line 29",
      status="PASS", evidence="Re-derived: 1+2+5+4+2+3+3 = 20, equal to data-hours-project=20 (project.html line 34) and to the hub's data-hours-project=20 (index.html line 29). Hours are design targets (ruling); only the arithmetic is checked."),
 dict(id="proj-check-pages-dag", check="2.9-structure", location="course/modules/FC/FC1/*.html",
      status="PASS", evidence=f"check_pages --unit FC1: PASS ({S}/check_pages_FC1.out). check_dag --unit FC1: PASS ({S}/check_dag_FC1.out)."),
 dict(id="proj-dag-closure", check="2.9-dag", location="project.html lines 58 and 178",
      status="PASS", evidence="Concept links present-value (line 58) and discount-factor (line 178) are M1 concepts in the closure of FC1 (plan section 0.1). No link to FC2, FI1 or other out-of-closure concepts in project.html (grep for data-concept: two hits only)."),
 dict(id="proj-notation", check="2.4-notation", location="project.html math; grader/*.py; tests/labs/FC1/lab-FC1-project-*.py; cards.json",
      status="PASS", evidence="Math on project.html uses t, y, (1+y)^-t, \\(t\\), \\(n\\) only, none registered in notation/notation.json (registered: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). Code identifiers yield_bps, coupon_bps, face_cents are not math symbols."),
 dict(id="proj-banned-phrases", check="2.9-prose", location="project.html; grader/*.py; lab twins; cards.json",
      status="PASS", evidence="check_pages --unit FC1: PASS (BANNED list, tools/check_pages.py lines 58-72). Grep this round, case-insensitive whole word, over the slice: build, builder, verifier, verified, requests, TODO, TBD, lorem, obviously, clearly and the other banned strings: 0 hits; 'round' only as the math verb ('rounds', 'rounded') and as 'Round-half-to-even' (lines 191 and the note on rounding) as a math term only; no ellipsis outside code."),
 dict(id="proj-reading-list", check="2.1-citations", location="project.html section#reading lines 321-327; references/references.json",
      status="PASS", evidence=f"verify_refs.py --offline: '560 entries, 0 problems' ({S}/verify_refs_offline.out). project.html line 323 says the page attributes no statement to either book; the list cites keys only."),
 dict(id="proj-named-conditions", check="2.6-autograde-exceptions", location="project.html lines 163-167; grader/test_project.py (refused and accepted tests)",
      status="PASS", evidence="Eight named conditions, each tested on both sides of its limit: periods 0 and -1 refused, 1 accepted; face 0 and -1 refused, 1 accepted; coupon -1 refused, 0 accepted; yield -10000 and -20000 refused, -9999 accepted; quantity 0 and -1 refused, 1 accepted; price -1 refused, 0 accepted; side 0, 2, -2, 3, -3 refused, +1 and -1 accepted; settlement_day 0 and -1 refused, 1 accepted. Unnamed inputs (quantity 501, 1001; coupon 15000; face 10**9; settlement_day 100) are accepted by must_accept, as the page's silence on upper limits requires."),
 dict(id="proj-failure-messages", check="2.6-autograde-messages", location="grader/test_project.py lines 75-93, 534-557; lines 300, 305, 323, 329, 334, 341 (bare asserts)",
      status="PASS", evidence="must_raise and must_accept messages name the condition; checked_events and checked_int name the property; _named_when_unimplemented turns NotImplementedError into a named failure. Six exact-value asserts carry no message string (lines 300, 305, 323, 329, 334, 341). In the browser (grader.js line 105) the failure shows the test name, which names the property (for example test_bond_price_exact_half_cent_at_496_bps_is_exact_not_float); with --assert=plain no expected value is printed, so none leaks. Hardening suggestion, not scored: add a short message to those six asserts."),
 dict(id="proj-test-docstring", check="2.6-autograde-docstrings", location="grader/test_project.py lines 252-265, 337-342, 423-432",
      status="PASS", evidence="Read the three tests added or changed in the delta. test_bond_coupon_above_one_hundred_percent_is_accepted: Bond(10000, 15000, 1) -> (1, 25000) (true). test_bond_price_exact_half_cent_at_496_bps: coupon 30506.7015 -> 30507, event (1, 1734792), PV 1652812.5, float 1652812.4999999998 (numbers_r13.out, true). test_trade_quantity_of_1001_is_accepted: (2, -1001*9850) (true)."),
 dict(id="proj-silence-coverage", check="2.6-autograde-silence", location="project.html line 163; grader/test_project.py lines 464-505",
      status="PASS", evidence="Read lines 464-505: 14 runs each checked with capsys (valid inputs and refused inputs); project.html line 163 says no function prints or warns on a valid input or a named refused input. Consistent."),
 dict(id="proj-privacy-claim", check="2.9-page-smoke", location="project.html footer line 340",
      status="PASS", evidence="Footer: 'nothing you write leaves it'. page_smoke --unit FC1 --pages project: PASS, zero console errors and no external requests (" + S + "/page_smoke_project.out)."),
 dict(id="proj-lint-types", check="2.6-lint", location="course/modules/FC/FC1; tests/labs/FC1",
      status="PASS", evidence=f"ruff check course/modules/FC/FC1 tests/labs/FC1: 'All checks passed!'. ruff format --check: '12 files already formatted'. Repo mypy --no-incremental (strict, pyproject): 'Success: no issues found in 229 source files' ({S}/mypy_repo.out, {S}/ruff_check.out). A path-only mypy call on the grader folder fails on the unresolved imports 'instruments' and 'instance', which is expected outside the repo config; the repo gate is the valid run."),
 dict(id="proj-reference-deployment", check="2.6-repo-wide", location="course/modules/FC/FC1/grader/reference.py (git-tracked)",
      status="PASS", evidence="Repo-wide matter, not failed in this slice per the workflow instruction. git ls-files shows reference.py tracked. Recorded in registry_flags."),
 # --- earlier mutants ---
 dict(id="proj-mutant-set-earlier", check="2.6-mutation", location="ledgers/FC1/mutants/ (72 earlier files)",
      status="PASS", evidence=f"tools/mutate_graders.py --unit FC1 --seeds 0-9 ({S}/mutate_FC1_s0-9_r13.out): every earlier mutant KILLED (c*, d*, f*, m*, r7-r12, v*). The three round-11 mutants (r11n01 killed by test_trade_quantity_of_1001_is_accepted, r11n02 by test_bond_coupon_above_one_hundred_percent_is_accepted, r11n03 by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period) and the three round-12 mutants (r12n01 by test_bond_has_one_event_per_period_numbered_one_to_n, r12n02 by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period, r12n03 by test_bond_price_exact_half_cent_at_496_bps_is_exact_not_float) are KILLED."),
 dict(id="proj-mutants-killed", check="2.6-mutation", location="ledgers/FC1/mutants/ (75 files); grader/test_project.py",
      status="FAIL", evidence=f"tools/mutate_graders.py --unit FC1 --seeds 0-9 -> 'mutate_graders FC1: FAIL (72/75 killed)' ({S}/mutate_FC1_s0-9_r13.out). Survivors: r13n01_coupon_computed_in_float, r13n02_trade_cash_flow_in_float, r13n03_yield_rate_through_float (this round's new student-error mutants; see the three rows below).",
      fix="Add the three tests named in the rows proj-mutant-r13n01, proj-mutant-r13n02 and proj-mutant-r13n03 to grader/test_project.py. Then re-run tools/mutate_graders.py --unit FC1 --seeds 0-9 and require 75/75."),
 dict(id="proj-mutant-r13n01", check="2.6-mutation", location="ledgers/FC1/mutants/r13n01_coupon_computed_in_float.py; grader/test_project.py (Bond.events tests)",
      status="FAIL", evidence=f"Mutant: the coupon is computed in binary floats, floor(face*coupon_bps/10000 + 0.5). SURVIVED on seeds 0-9. Distinguishing valid input (no upper limit on face is named; project.html line 163 says money is computed from exact fractions): Bond(10**17 + 4999, 1, 1).events(). Reference (1, 100010000000004999); mutant (1, 100010000000005000) ({S}/kill_inputs_r13.out, {S}/probe_new_mutants_r13.out). Standard: project.html line 163 'Money is an int in cents at every output, computed from exact fractions and rounded once.' and line 176 'The exact value of an output is computed from fractions'.",
      fix="Add to grader/test_project.py: def test_bond_coupon_is_exact_for_a_face_too_large_for_floats(): assert checked_events(sol.Bond(10**17 + 4999, 1, 1).events(), 'Bond.events') == [(1, 10**17 + 4999 + 10**13)] with a docstring saying the coupon 10**13 + 0.4999 rounds down to 10**13 exactly."),
 dict(id="proj-mutant-r13n02", check="2.6-mutation", location="ledgers/FC1/mutants/r13n02_trade_cash_flow_in_float.py; grader/test_project.py (CashTrade tests)",
      status="FAIL", evidence=f"Mutant: the trade cash flow is multiplied in a binary float. SURVIVED on seeds 0-9. Distinguishing valid input: CashTrade(2**40 + 1, 9851, 1, 2).events(). Reference (2, -10831289045231227); mutant (2, -10831289045231228) ({S}/kill_inputs_r13.out). The product is odd and above 2**53, so the float rounds it. Standard: project.html line 163 (exact fractions) and line 176 (every amount is an int number of cents, exact).",
      fix="Add to grader/test_project.py: def test_trade_cash_flow_is_exact_above_two_to_the_fifty_three(): assert checked_events(sol.CashTrade(2**40 + 1, 9851, 1, 2).events(), 'CashTrade.events') == [(2, -((2**40 + 1) * 9851))] with a docstring stating the product is above 2**53."),
 dict(id="proj-mutant-r13n03", check="2.6-mutation", location="ledgers/FC1/mutants/r13n03_yield_rate_through_float.py; grader/test_project.py (bond_price_cents tests)",
      status="FAIL", evidence=f"Mutant: the per-period yield is Fraction(rate / 10000) through a float. SURVIVED on seeds 0-9. Distinguishing valid input: Bond(13, 0, 1) at yield_bps 400. Exact present value 13/1.04 = 25/2 cents, an exact half that rounds away from zero to 13; mutant gives 12 ({S}/kill_inputs_r13.out; search in {S}/search_float_yield_r13.out). The suite's exact-half tests (496 bps, 1/2 cent at 10000 bps) do not use a yield whose float value lies above the exact rate.",
      fix="Add to grader/test_project.py: def test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield(): assert sol.bond_price_cents(sol.Bond(13, 0, 1), 400) == 13 with a docstring: 13 / 1.04 = 25/2 exactly, so the half cent rounds away from zero."),
 dict(id="cards-scan", check="2.7-cards-duplicates", location="course/modules/FC/FC1/cards.json (118 cards)",
      status="PASS", evidence=f"{S}/cards_scan.py: 118 cards; ids FC1-c001..c118 unique; no duplicate fronts or backs; 54 graded cards (39 T, 15 C), every C card has a basis; no bare \\bQ\\b, no V_b, no 'card' in text. Cosmetic: ids are not in sequence (c099/c108 and c101/c109 area, noted in round 12), not a failure."),
 dict(id="cards-c030", check="2.7-cards-changed", location="course/modules/FC/FC1/cards.json FC1-c030 (back); L02.html line 254 (Example 3.1), line 407 (table row, grade C)",
      status="PASS", evidence="The only changed card in the delta: its back adds '(Example 3.1)'. L02.html line 254 is the block-title 'Example 3.1 (the four combinations of form and venue)' and line 407 is the table row 'The four combinations of form and venue all occur in the register (Example 3.1)', graded C with basis 'a hand reading of register entries 1, 3, 4 and 6'. Line 255 says the four combinations are read off by hand, not printed by the lab, which matches the card's basis and grade C."),
 dict(id="cards-numbers", check="2.7-cards-lesson-agreement", location="cards.json (sampled cards, unchanged except FC1-c030); L01-L05 twins",
      status="PASS", evidence=CARRY12.replace("files byte-identical since the previous pin 460b696", "cards.json differs from the round-12 pin only at FC1-c030 (git diff 460b696 762f636 shows one changed line); lessons L01-L05.html and the lab twins are byte-identical since 460b696") + "the sampled card numbers were checked against the lab outputs in round 12 (scripts/FC1-c-r12/lab_L0*.out); the lab twins still print those values (" + S + "/run_labs_FC1.out PASS 8/8)."),
 dict(id="cards-hypothesis-and-grades", check="2.7-cards-grades", location="cards.json backs and grades; L03.html lines 61-62; L04.html lines 372, 376",
      status="PASS", evidence=CARRY12.replace("files byte-identical since the previous pin 460b696", "cards.json differs only at FC1-c030; L03.html, L04.html byte-identical since 460b696") + "the grade-C cards have a basis (cards-scan), the card-to-definition mapping (c036, c070, c071) and the c092 grade T were re-read in round 12."),
]


EXTRA = [
 dict(id="proj-collect-count-55", check="2.6-page-count", location="project.html line 171; grader/test_project.py",
      status="PASS", evidence="Round-12 row, superseded by proj-collect-count-65: the count the page states is now 65, and the collect-only count is 65 (" + S + "/alts_and_collect.out line 2). The round-12 count of 62 is no longer on the page."),
 dict(id="proj-instances-50", check="2.6-autograde-instances", location="grader/instance.py",
      status="PASS", evidence="Round-12 row, superseded by proj-instances-20: run_graders 0-49 is 50/50 (" + S + "/run_graders_FC1_0-49.out); the 20-seed sample is " + S + "/instances_20_r13.out. instance.py is byte-identical since 460b696."),
 dict(id="proj-new-mutants-r10", check="2.6-mutation", location="ledgers/FC1/mutants/r10n01..r10n04",
      status="PASS", evidence="mutate_graders FC1 0-9 (" + S + "/mutate_FC1_s0-9_r13.out): r10n01_side_three_accepted, r10n02_coupon_minus_one_accepted, r10n03_yield_minus_9999_refused and r10n04_price_zero_refused are each KILLED (the mutant list in this fragment carries each killed_by test)."),
 dict(id="proj-mutant-set-d-and-c", check="2.6-mutation", location="ledgers/FC1/mutants/ c*, d*, f*, m*, v*, r7-r9 files",
      status="PASS", evidence="All earlier mutants other than the three r13 survivors are KILLED on seeds 0-9 in " + S + "/mutate_FC1_s0-9_r13.out (count 72 of 75 killed; the 72 killed include all c, d, f, m, r7, r8, r9 and v files)."),
 dict(id="proj-new-mutants-r11", check="2.6-mutation", location="ledgers/FC1/mutants/r11n01..r11n03",
      status="PASS", evidence="KILLED on seeds 0-9 (" + S + "/mutate_FC1_s0-9_r13.out): r11n01 by test_trade_quantity_of_1001_is_accepted, r11n02 by test_bond_coupon_above_one_hundred_percent_is_accepted, r11n03 by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period."),
 dict(id="proj-new-mutants-r12", check="2.6-mutation", location="ledgers/FC1/mutants/r12n01..r12n03",
      status="PASS", evidence="KILLED on seeds 0-9 (" + S + "/mutate_FC1_s0-9_r13.out): r12n01 by test_bond_has_one_event_per_period_numbered_one_to_n, r12n02 by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period, r12n03 by test_bond_price_exact_half_cent_at_496_bps_is_exact_not_float. The round-12 FAIL on r12n03 is cleared."),
 dict(id="cards-scan-98", check="2.7-cards-duplicates", location="course/modules/FC/FC1/cards.json",
      status="PASS", evidence="Round-12 row, superseded by cards-scan (118 cards): " + S + "/cards_scan.out shows unique ids, no duplicate fronts or backs, every graded C card has a basis."),
 dict(id="cards-labels-and-hypotheses", check="2.7-cards-labels", location="cards.json backs (all); c013 vs L01.html lines 155-156",
      status="PASS", evidence=CARRY12.replace("files byte-identical since the previous pin 460b696", "cards.json differs from the round-12 pin only at FC1-c030; L01.html is byte-identical since 460b696") + "every grade-C card has a basis and no card carries a grade outside T/C (cards_scan.out)."),
 dict(id="cards-hypothesis-c036", check="2.7-cards-hypothesis", location="cards.json FC1-c036; L03.html Definition 1.2 (lines 61-62)",
      status="PASS", evidence=CARRY12.replace("files byte-identical since the previous pin 460b696", "cards.json differs only at FC1-c030; L03.html byte-identical since 460b696") + "FC1-c036 back states the convention of Definition 1.2 at L03.html lines 61-62."),
 dict(id="cards-misconception-refs", check="2.7-cards-misconceptions", location="cards.json FC1-c070, FC1-c071; L04.html lines 372, 376",
      status="PASS", evidence=CARRY12.replace("files byte-identical since the previous pin 460b696", "cards.json differs only at FC1-c030; L04.html byte-identical since 460b696") + "the two misconception cards match the misconception items at L04.html lines 372 and 376."),
 dict(id="cards-grades-and-basis", check="2.7-cards-grades", location="cards.json FC1-c014, c029, c054, c091-c096",
      status="PASS", evidence=f"cards_scan.py (" + S + "/cards_scan.out): 54 graded cards (39 T, 15 C), each C card has a basis; no grade outside T/C. FC1-c092 is grade T with basis 'Lab 1, Part C (typed-in parameters)', unchanged since the round-12 pin."),
 dict(id="cards-lesson-agreement", check="2.7-cards-lesson-agreement", location="cards.json c070, c071, c082, c092, c115-c118 vs L02-L05",
      status="PASS", evidence=CARRY12.replace("files byte-identical since the previous pin 460b696", "cards.json differs only at FC1-c030; L02-L05.html and the lab twins are byte-identical since 460b696") + "the lesson-agreement cards are unchanged, and the lab twins still print the values they cite (run_labs 8/8 this round)."),
 dict(id="cards-notation-Q", check="2.4-notation", location="cards.json (bare Q, V_b, card)",
      status="PASS", evidence=f"cards_scan.py pattern scan (" + S + "/cards_scan.out): \\bQ\\b 0 hits; V_b 0 hits; \\bcard\\b 0 hits."),
]
rows.extend(EXTRA)

# the one previous row that changed subject is replaced above; ids of the round-12 rows are kept
round12_ids = [r["id"] for r in json.loads(Path("/Users/billyribeiro/.fanout/frags/C-FC1-c.round12.json").read_text())["rows"]]
have = {r["id"] for r in rows}
missing = [i for i in round12_ids if i not in have]
print("round-12 row ids not yet covered:", missing)

fragment = {
 "unit": "FC1", "slice": "c", "round": 13,
 "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 13 (did not build FC1)",
 "pin": "762f636d", "base": "460b696 (round-12 pin); delta in slice: project.html line 171, grader/test_project.py (three new tests), cards.json FC1-c030, ledgers/FC1/alternatives/a5, mutants r11n01-03 and r12n01-03",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC13-FC1-c", "scratch": "/tmp/fc1c13_*",
 "verified_at": "2026-10-29T00:00:00+00:00", "verdict": "FAIL",
 "rows": rows, "mutants": mutants,
 "registry_flags": [
   "Repo-wide, not failed (per workflow instruction): course/modules/FC/FC1/grader/reference.py is git-tracked and BLUEPRINT.md lines 400-401 require deployment to exclude it; nothing enforces the exclusion.",
   "Curriculum scope conflict for the user or architect: curriculum/02-economics-finance-core.yaml lines 388-395 (project brief) names bonds, futures, swaps and options; the binding architect decision and project.html cover cash instruments only. Not edited here (generated source)."],
 "freshness_flags": [],
 "notes": ("Round 13 on 762f636 (delta 460b696..762f636 in slice: project.html line 171 'runs 65 checks'; grader/test_project.py three new tests at lines 265, 337-342, 426-432; cards.json FC1-c030; ledgers/FC1/alternatives/a5 replaced by an exact frozen-dataclass implementation; mutants r11n01-03 and r12n01-03 added). "
   "Round-12 FAIL rows: proj-alternatives-five and proj-new-mutants-r12 are now PASS (the float a5 is gone; r12n03 is killed by the exact-half 496 bps test). proj-mutants-killed is FAIL again because this round's three new mutants survive. "
   "New FAILs (3 survivors, each a student-error money-as-float mutant the page's exact-fraction rule forbids): r13n01 coupon in floats (Bond(10**17+4999,1,1)), r13n02 trade cash flow in floats (CashTrade(2**40+1,9851,1,2)), r13n03 yield through floats (Bond(13,0,1) at 400 bps, exact 25/2 -> 13). "
   "Commands run this round: run_graders 0-49 (50/50); run_labs (8/8); page_vs_twin_r13.py (page code and expected blocks vs twins, twins under python -I -W error); check_pages; check_dag; check_projects; page_smoke --pages project; ruff check and format; mypy repo strict; verify_refs --offline (560, 0 problems); pytest test_page_checks.py and test_page_smoke.py; mutate_graders 0-9 (72/75); alts_and_collect (a1-a5 and reference, 0 failing of 20; collect 65); cards_scan; instances_20; numbers_r13.py; search_float_yield_r13.py. "
   "Not checked: the full pytest suite and render_curriculum, build_site --check and fetch_data --check (no curriculum, data or site input changed in this slice); a live verify_refs run (offline only); line-by-line re-read of all 118 cards (cards.json changed in one entry; the scan and the sampled rows cover the rest); Pyodide execution of the three new mutants (local only); hours not re-estimated (architect ruling); the r13 mutants were not run in the browser."),
 "summary": None,
}
fragment["summary"] = {
 "rows_total": len(rows),
 "pass": sum(1 for r in rows if r["status"] == "PASS"),
 "fail": sum(1 for r in rows if r["status"] == "FAIL"),
 "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
 "mutants": {"killed": sum(1 for m in mutants if m["killed_by"]), "total": len(mutants)},
}
Path("ledgers/FC1/FC1-c.json").write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(fragment["summary"]))
