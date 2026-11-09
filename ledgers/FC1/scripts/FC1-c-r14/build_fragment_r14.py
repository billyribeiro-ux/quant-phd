"""Round 14, FC1-c: write the verifier fragment ledgers/FC1/FC1-c.json from the rows below and the mutate output.

The mutant list is parsed from ledgers/FC1/scripts/FC1-c-r14/out/mutate_FC1_s0-9_final.out (tools/mutate_graders.py).
Usage: python -I ledgers/FC1/scripts/FC1-c-r14/build_fragment_r14.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

S = "ledgers/FC1/scripts/FC1-c-r14"
O = f"{S}/out"

ROWS: list[dict[str, str]] = [
    {"id": "proj-run-graders", "check": "2.6-autograde-reference", "location": "course/modules/FC/FC1/grader/reference.py; tools/run_graders.py",
     "status": "PASS", "evidence": f"`.venv/bin/python tools/run_graders.py --unit FC1 --seeds 0-49` -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.3 s)' ({O}/run_graders_s0-49.out)."},
    {"id": "proj-collect-count-65", "check": "2.6-page-count", "location": "course/modules/FC/FC1/project.html line 171; grader/test_project.py",
     "status": "PASS", "evidence": f"pytest --collect-only on a scratch copy: '92 tests collected' ({O}/collect_count_r14.out); page line 171 says 'runs 92 checks'. The id keeps the round-13 text '65' for tracking only; the count is now 92."},
    {"id": "proj-browser-suite", "check": "2.6-autograder-both", "location": "course/modules/FC/FC1/project.html line 302 (section#grader); course/assets/js/grader.js",
     "status": "PASS", "evidence": f"`tools/page_smoke.py --unit FC1 --pages project` -> 'in-browser grader: All 92 tests pass on seed 552738088', 'page_smoke modules/FC/FC1/project.html: PASS' ({O}/page_smoke_FC1_project.out). Panel attributes data-suite, data-support, data-solution, data-starter present (project.html line 302)."},
    {"id": "proj-alternatives-five", "check": "2.6-autograde-alternatives", "location": "ledgers/FC1/alternatives/a1..a5 (run against grader/test_project.py)",
     "status": "PASS", "evidence": f"run_candidates_r14.py seeds 0-49: a1_list_comprehension_events, a2_generator_methods, a3_fraction_throughout, a4_integer_division_half_up, a5_frozen_dataclass_reduce each 'ALL PASS 50/50 seeds' ({O}/alternatives_and_reference_s0-49.out). a4 uses integer division for the coupon and the trade and Fractions for the price; the extra pure-integer alternative below covers the integer-only style."},
    {"id": "proj-alternatives-integer-only", "check": "2.6-autograde-alternatives", "location": f"{S}/alt_integer_only_r14.py",
     "status": "PASS", "evidence": f"Extra alternative written this round: integer-only arithmetic (common denominator (10000+yield_bps)**periods, integer half-away division). run_candidates_r14.py seeds 0-49: 'ALL PASS 50/50 seeds' ({O}/alt_integer_only_r14.out)."},
    {"id": "proj-instances-20", "check": "2.6-autograde-instances", "location": "course/modules/FC/FC1/grader/instance.py",
     "status": "PASS", "evidence": f"{S}/check_instances_r14.py prints seeds 0-19 (face, periods, yield, price, trade event); every value in range; independent Fraction oracle agrees with the bond price and trade event ({O}/instances_r14.out)."},
    {"id": "proj-instances-50", "check": "2.6-autograde-instances", "location": "course/modules/FC/FC1/grader/instance.py",
     "status": "PASS", "evidence": f"{S}/check_instances_r14.py over seeds 0-49: 'range problems=none'; 50 distinct (bond price, trade event) pairs; 50 distinct bond prices; periods take all of 1..8; 49 distinct yields ({O}/instances_r14.out). Answers change with the seed, not only labels."},
    {"id": "proj-starter-vs-spec", "check": "2.6-spec", "location": "course/modules/FC/FC1/grader/starter.py; project.html line 161",
     "status": "PASS", "evidence": f"starter.py names and signatures equal reference.py (Bond, Bond.events, bond_price_cents, CashTrade, CashTrade.events). Starter at seed 0: 90 failed, 2 passed (the two passing tests accept any exception by design), zero Tracebacks ({O}/starter_seed0_r14.out)."},
    {"id": "proj-spec-questions", "check": "2.6-spec", "location": "course/modules/FC/FC1/project.html lines 153-172",
     "status": "PASS", "evidence": "Questions I would have had to ask: none blocking. settlement_day being a period index is stated by 'Inputs' (line 159, 'a settlement period') and fixed by Fixture E (line 190, CashTrade(10, 9850, 1, 2).events() is [(2, -98500)]). Sign, period indexing and rounding are stated in Conventions (lines 176-180)."},
    {"id": "proj-ladder", "check": "2.6-spec-ladder", "location": "course/modules/FC/FC1/project.html lines 41-50",
     "status": "PASS", "evidence": "Rung 1 is Lab 1, fully solved with a step comment per line (lines 56-102); Rung 2 is Lab 2, class 'lab completion', graded instantly (lines 104-150); Rung 3 is the autograded module with scope matching the curriculum brief (curriculum/02-economics-finance-core.yaml 388-395); Rung 4 is not graded (lines 312-318)."},
    {"id": "proj-stretch-scope", "check": "2.6-spec", "location": "course/modules/FC/FC1/project.html section#stretch lines 312-318",
     "status": "PASS", "evidence": "Stretch items are stated as not graded and open-ended (a limit order book; a bond with an odd first period); each asks for a stated convention and a check."},
    {"id": "proj-local-command", "check": "2.6-spec", "location": "course/modules/FC/FC1/project.html section#local lines 305-310; grader/starter.py docstring",
     "status": "PASS", "evidence": "The command on line 308 uses QF_SEED with the same flags used by the runner (--assert=plain -W error); equivalent runs in scratch copies gave the results recorded in " + f"{O}/collect_count_r14.out and {O}/reference_seed0_r14.out."},
    {"id": "proj-lab1-twin", "check": "2.5-labs", "location": "course/modules/FC/FC1/project.html lab-FC1-project-1 (lines 56-102); tests/labs/FC1/lab-FC1-project-1.py",
     "status": "PASS", "evidence": f"{S}/compare_labs_r14.py: page code equals twin line for line; expected block equals twin stdout; `python -I -W error tests/labs/FC1/lab-FC1-project-1.py` exit 0 ({O}/twins_project_labs_r14.out). Printed values recomputed in {S}/numbers_r14.py."},
    {"id": "proj-lab2-completion", "check": "2.5-labs-completion", "location": "course/modules/FC/FC1/project.html lab-FC1-project-2 (lines 104-150); tests/labs/FC1/lab-FC1-project-2.py",
     "status": "PASS", "evidence": f"compare_labs_r14.py: two '___' blanks on the page (lines 133 and 140); every other line equals the twin; the twin's completed run equals the expected block ({O}/twins_project_labs_r14.out). Tolerance claim (line 149, about 0.1 cent) matches course/assets/js/labs.js tolerance*(1+|expected|) with tolerance 1e-6: 1e-6*102776 = 0.103."},
    {"id": "proj-lab2-docstring", "check": "2.9-prose", "location": "course/modules/FC/FC1/project.html line 107; tests/labs/FC1/lab-FC1-project-2.py line 1",
     "status": "FAIL", "evidence": "The docstring of the completed twin says 'Rung 2 completion: the worked example, with two blanks for you to fill in.' The twin is the completed program and contains no '___' (compare_labs_r14.py: blanks on the twin = 0). The established convention is 'Rung 2 completed solution: ...' (tests/labs/M1/lab-M1-project-2.py line 1; ruling 11). The sentence is accurate only for the page, and it is a sentence about what the twin contains.",
     "fix": "Change line 1 of tests/labs/FC1/lab-FC1-project-2.py and the identical docstring line 107 of project.html to 'Rung 2 completed solution: the worked example with its two blanks filled in.' (keep the page line and the twin line identical, as run_labs requires)."},
    {"id": "proj-lab3-fixtures", "check": "2.5-labs", "location": "course/modules/FC/FC1/project.html lab-FC1-project-3 (lines 196-276); tests/labs/FC1/lab-FC1-project-3.py",
     "status": "PASS", "evidence": f"Twin runs exit 0 under -I -W error; page code equals twin; expected block equals output for all 13 printed lines, each value recomputed by {S}/numbers_r14.py (10278 vs 10277, 11053 with exact 11052.6316, 1 for fixture F, 5001 for fixture G)."},
    {"id": "proj-prose-numbers", "check": "2.2-numbers", "location": "course/modules/FC/FC1/project.html lines 58, 101, 176, 186-193, 198, 275",
     "status": "PASS", "evidence": f"{S}/numbers_r14.py output ({O}/numbers_r14.out): exact PV 102775.091033 (line 58); 10277.509103 rounds to 10278 and term rounding gives 10277 (lines 193, 198); 10500/0.95 = 210000/19 = 11052.6316 rounds to 11053 (line 187); 1/2 cent rounds away to 1 (fixture F); 5000.5 rounds to 5001 (fixture G); 'exact' value 1/2 cent claims verified."},
    {"id": "proj-fixture-claims", "check": "2.9-prose", "location": "course/modules/FC/FC1/project.html lines 183-194 and 276; grader/test_project.py lines 174-212, 396-420",
     "status": "PASS", "evidence": "Each fixture A-G and the rounding fixture is matched to its named test (read in full): A events line 174 and price line 367; B price line 376; C events line 189; D events line 197; E lines 536 and 544; F events line 242 and price line 406; G price line 415; rounding price line 396. Fixture G events and the rounding case's events are not asserted as lists (grep 'Bond(10_001, 0, 1)' and 'Bond(10_000, 500, 3)' give price assertions only), as page line 276 says."},
    {"id": "proj-hours-arithmetic", "check": "2.6-hours", "location": "course/modules/FC/FC1/project.html section#budget lines 283-293; index.html line 29",
     "status": "PASS", "evidence": "Component hours 1+2+5+4+2+3+3 = 20 (lines 286-292); data-hours-project=\"20\" (index.html line 29, hub lessons 50, total 70). My own component estimate: about 14 to 22 hours, inside 30 percent of 20."},
    {"id": "proj-check-pages-dag", "check": "2.9-structure", "location": "course/modules/FC/FC1/ (project.html)",
     "status": "PASS", "evidence": f"`tools/check_pages.py --unit FC1` -> 'check_pages FC1: PASS' ({O}/check_pages.out); `tools/check_dag.py --unit FC1` -> 'check_dag FC1: PASS' ({O}/check_dag.out)."},
    {"id": "proj-dag-closure", "check": "2.9-dag", "location": "course/modules/FC/FC1/project.html lines 58, 178",
     "status": "PASS", "evidence": "The only concept links are present-value and discount-factor (M1 closure, course/concepts.html anchors exist). Out-of-closure names (futures, swaps, options, yield-to-maturity, duration, clearing house) do not occur as terms on the page except in the scope sentence on line 157, which names FC2 and uses no FC2 concept. 'settlement period' is a plain dfn without data-concept (line 54)."},
    {"id": "proj-notation", "check": "2.4-notation", "location": "course/modules/FC/FC1/project.html math; grader/*.py; tests/labs/FC1/lab-FC1-project-*.py",
     "status": "PASS", "evidence": "Math on the page uses only y (defined line 178 as yield_bps over 10000), t (period, line 178) and the expressions (1+y), (1+y)^-t. No T, Q, R_f, Phi, gamma, R^*, R^{e*} and no \\mathbb in the page (grep)."},
    {"id": "proj-banned-phrases", "check": "2.9-prose", "location": "course/modules/FC/FC1/project.html; grader/*.py; lab twins",
     "status": "PASS", "evidence": "grep of the check_pages BANNED patterns (TODO, TBD, lorem, obviously, clearly, ellipsis) and of the process words (build, builder, verifier, round N, ledger, mutant, planner) over project.html, the grader and the three twins: zero hits."},
    {"id": "proj-reading-list", "check": "2.1-citations", "location": "course/modules/FC/FC1/project.html lines 321-327; references/references.json (mishkin2021economics, harris2002trading)",
     "status": "PASS", "evidence": f"`tools/verify_refs.py --unit FC1` (live): 'live re-verification of FC1: 2 of 560 entries, 0 problems'; `tools/verify_refs.py --offline` (whole registry): '560 entries, 0 problems' ({O}/verify_refs_FC1_live.out, {O}/verify_refs_offline_all.out). The page states no year and no statement from either book (line 323), so the registry-year conflicts do not reach the page."},
    {"id": "proj-scope-ruling5", "check": "2.6-scope", "location": "course/modules/FC/FC1/project.html line 157; curriculum/02-economics-finance-core.yaml 388-395; plans/FINAL-ARCHITECT-RULINGS.md item 5",
     "status": "PASS", "evidence": "The project covers a fixed-rate bond and a cash trade only (line 157 and the brief at yaml 388-395). Futures, swaps and options are absent from the grader and labs (grep). Matches ruling 5 (cash instruments only)."},
    {"id": "proj-named-conditions", "check": "2.6-autograde-exceptions", "location": "course/modules/FC/FC1/project.html lines 163-167; grader/test_project.py must_raise call sites (lines 215-260, 499-512, 559-662, 719-734)",
     "status": "PASS", "evidence": "Eight named conditions (periods, face, coupon, yield, quantity, price, side, settlement_day) are each refused and accepted at their boundary in the default context. must_raise is used only for the named conditions (every call site checked by reading). Context gaps are recorded in proj-named-conditions-context."},
    {"id": "proj-named-conditions-context", "check": "2.6-autograde-mutation", "location": "course/modules/FC/FC1/project.html lines 163 and 167; grader/test_project.py lines 559-662 (CashTrade refusals) and 215-260, 719-734 (Bond refusals)",
     "status": "FAIL", "evidence": f"Every CashTrade refusal for quantity, price_cents and settlement_day uses side=+1 (lines 559-561, 608-610, 654-661, 726-727 of the suite); every Bond face and periods refusal uses coupon_bps=500 (lines 215-246, 719-724). Two surviving mutants violate the unconditional statements: project.html line 163 'Each named condition below raises ValueError' and line 167 (CashTrade: quantity less than 1; price_cents negative; settlement_day less than 1). See proj-mutant-r14n01 and proj-mutant-r14n05 ({O}/mutate_FC1_s0-9_final.out).",
     "fix": "Add to grader/test_project.py: must_raise(lambda: sol.CashTrade(0, 9_850, -1, 2).events(), 'quantity < 1, sell'); must_raise(lambda: sol.CashTrade(10, -1, -1, 2).events(), 'price_cents < 0, sell'); must_raise(lambda: sol.CashTrade(10, 9_850, -1, 0).events(), 'settlement_day < 1, sell'); must_raise(lambda: sol.Bond(10_000, 0, 0).events(), 'periods < 1, zero coupon'); must_raise(lambda: sol.Bond(0, 0, 3).events(), 'face_cents <= 0, zero coupon'). Probe: {S}/probe_fix_r14.py kills both survivors and the reference passes ({O}/probe_fix_r14.out)."},
    {"id": "proj-failure-messages", "check": "2.6-autograde-messages", "location": "grader/test_project.py (all assertions and pytest.fail calls)",
     "status": "PASS", "evidence": "ast scan of test_project.py: 0 assert statements without a message. Messages name the property ('periods must run 1..periods', 'the coupon ... rounded once') and never print an expected value (--assert=plain shows only the message)."},
    {"id": "proj-test-docstring", "check": "2.6-autograde-docstrings", "location": "grader/test_project.py docstrings at lines 206-208, 398-399, 423-427, 434-438, 449-452, 459-462, 840-842, 970-972, 983-985",
     "status": "PASS", "evidence": f"Every number in those docstrings recomputed by {S}/numbers_r14.py and the probe in this round: 1652812.4999999998 and 1652812 (line 427), 12.499999999999998 and 12 (line 452), 299985000.5 - 1/(2*1000300030001) (line 462), 9334.46 and 10277.5091 (line 398), 10500/101 = 103.96 rounds to 104 and 10500/1001 = 10.49 rounds to 10 (lines 883, 931), 9999999999999900 + 100/(10**14+1) (line 971). All match."},
    {"id": "proj-simulated-labels", "check": "2.8-data", "location": "course/modules/FC/FC1/project.html lines 54, 72, 120, 159; grader/instance.py line 31",
     "status": "PASS", "evidence": "project.html has no data-files attribute (grep count 0) and the twins read no file; the inputs are labelled SIMULATED (5 lines on the page mention it; instance.py label 'SIMULATED bond and trade, seed N: not market data')."},
    {"id": "proj-silence-coverage", "check": "2.6-autograde-silence", "location": "project.html line 163; grader/test_project.py lines 693-734",
     "status": "PASS", "evidence": "capsys tests cover 14 valid inputs and 8 named refusals; the page's silence claim (line 163) is qualified to those inputs, and the suite passes the reference with -W error."},
    {"id": "proj-privacy-claim", "check": "2.9-page-smoke", "location": "course/modules/FC/FC1/project.html line 341; course/assets/js/grader.js",
     "status": "PASS", "evidence": "page_smoke reports no external requests for the project page (out/page_smoke_FC1_project.out). grader.js writes only to the local store (store.put, IndexedDB per store.js line 2) and its one fetch (text(url), grader.js line 18) loads the grader files; no network write of learner code."},
    {"id": "proj-lint-types", "check": "2.6-lint", "location": "course/modules/FC/FC1 (grader); tests/labs/FC1",
     "status": "PASS", "evidence": f"`ruff check` and `ruff format --check` on tests/labs/FC1 and the grader: 'All checks passed!', '12 files already formatted' ({O}/ruff_r14.out). Repository mypy gate `.venv/bin/mypy --no-incremental`: 'Success: no issues found in 385 source files' ({O}/mypy_repo_default_r14.out). Strict mypy on test_project.py + instance.py + reference.py as instruments.py: pass ({O}/mypy_strict_grader_scratch_r14.out). Note: the planner's literal command `mypy tests/labs/FC1 course/modules/FC/FC1/grader` reports 3 errors because the learner module 'instruments' is absent ({O}/mypy_plan_cmd_r14.out); not a defect of the code."},
    {"id": "proj-reference-deployment", "check": "2.6-repo-wide", "location": "course/modules/FC/FC1/grader/reference.py lines 3-4",
     "status": "PASS", "evidence": "reference.py is git-tracked and its docstring names the BLUEPRINT deployment rule. Architect ruling 4: the repository has no deploy step and the rule is not a defect of any module that must fail a slice. Recorded as a registry flag only."},
    {"id": "proj-exemplar-blind", "check": "2.6-rubric", "location": "course/modules/FC/FC1/project.html (0 matches for rubric or exemplar); curriculum/02-economics-finance-core.yaml line 395 (grading: autograder)",
     "status": "PASS", "evidence": "The project is graded by autograder only, with no rubric and no exemplars, so there is nothing to score. Blind exemplar scoring (ruling 23) is not applicable and was not performed."},
    {"id": "proj-mutant-set-earlier", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/ (136 files that existed before round 14)",
     "status": "PASS", "evidence": f"`tools/mutate_graders.py --unit FC1 --seeds 0-9` ({O}/mutate_FC1_s0-9_final.out): all 136 pre-existing mutants KILLED (killer and seed per mutant in the mutants list below)."},
    {"id": "proj-mutant-first-line", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/*.py (141 files)",
     "status": "PASS", "evidence": "ast.get_docstring first line of every mutant names a specific student error (checked by an ast scan this round; the mutants list below carries each description)."},
    {"id": "proj-new-mutants-r10", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r10n01..r10n04",
     "status": "PASS", "evidence": f"Killed: r10n01 by test_trade_side_three_is_refused, r10n02 by test_bond_negative_coupon_is_refused, r10n03 by test_yield_just_above_minus_one_is_accepted, r10n04 by test_trade_price_zero_is_accepted_and_kept ({O}/mutate_FC1_s0-9_final.out)."},
    {"id": "proj-new-mutants-r11", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r11n01..r11n03",
     "status": "PASS", "evidence": f"Killed: r11n01 by test_trade_quantity_of_1001_is_accepted, r11n02 by test_bond_coupon_above_one_hundred_percent_is_accepted, r11n03 by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period ({O}/mutate_FC1_s0-9_final.out)."},
    {"id": "proj-new-mutants-r12", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r12n01..r12n03",
     "status": "PASS", "evidence": f"Killed: r12n01 by test_bond_has_one_event_per_period_numbered_one_to_n, r12n02 by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period, r12n03 by test_bond_price_exact_half_cent_at_496_bps_is_exact_not_float ({O}/mutate_FC1_s0-9_final.out)."},
    {"id": "proj-mutant-r13n01", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r13n01_coupon_computed_in_float.py; grader/test_project.py lines 205-212",
     "status": "PASS", "evidence": f"Round-13 survivor, now KILLED by test_bond_coupon_is_exact_for_a_face_too_large_for_floats (seed 0) ({O}/mutate_FC1_s0-9_final.out)."},
    {"id": "proj-mutant-r13n02", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r13n02_trade_cash_flow_in_float.py; grader/test_project.py lines 597-605",
     "status": "PASS", "evidence": f"Round-13 survivor, now KILLED by test_trade_cash_flow_is_exact_above_two_to_the_fifty_three (seed 0) ({O}/mutate_FC1_s0-9_final.out)."},
    {"id": "proj-mutant-r13n03", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r13n03_yield_rate_through_float.py; grader/test_project.py lines 448-456",
     "status": "PASS", "evidence": f"Round-13 survivor, now KILLED by test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield (seed 0) ({O}/mutate_FC1_s0-9_final.out)."},
    {"id": "proj-new-mutants-r14-killed", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r14n02, r14n03, r14n04",
     "status": "PASS", "evidence": f"Written this round from grader/reference.py by {S}/make_mutants_r14.py. r14n02 (price memo keyed by yield alone) KILLED by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period; r14n03 (negative yield as magnitude) KILLED by test_bond_price_negative_yield_is_above_the_undiscounted_value; r14n04 (face paid with the first coupon) KILLED by test_bond_coupon_is_face_times_coupon_rate_rounded_half_away ({O}/mutate_FC1_s0-9_final.out)."},
    {"id": "proj-mutant-r14n01", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r14n01_sale_skips_quantity_and_settlement_checks.py; grader/test_project.py CashTrade refusal tests (lines 559-662, 654-661)",
     "status": "FAIL", "evidence": f"Student error: CashTrade checks quantity, price and settlement_day only for a buy, so a sale of zero units is accepted. SURVIVED all 10 seeds 0-9 (mutate_graders: 'SURVIVED r14n01... -> None'; {O}/mutate_FC1_s0-9_final.out; {O}/new_mutants_r14_s0-9.out). Every CashTrade refusal test uses side=+1, so no test distinguishes it. The page states the refusal without a side qualifier: project.html line 167 ('CashTrade: quantity less than 1; price_cents negative; ... settlement_day less than 1') and line 163 ('Each named condition below raises ValueError').",
     "fix": "Add the three sell-side refusal tests listed in proj-named-conditions-context. Re-run tools/mutate_graders.py --unit FC1 --seeds 0-9: r14n01 must be KILLED."},
    {"id": "proj-mutant-r14n05", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/r14n05_bond_periods_and_face_checked_only_with_a_coupon.py; grader/test_project.py Bond refusal tests (lines 215-246, 719-724)",
     "status": "FAIL", "evidence": f"Student error: Bond refuses periods below 1 and a non-positive face only when the coupon is non-zero, so a zero-coupon bond with no face is accepted. SURVIVED all seeds 0-9 ({O}/mutate_FC1_s0-9_final.out; {O}/probe_r14n05_s0-9.out). All Bond refusal tests use coupon_bps=500. project.html line 165 states the Bond conditions without a coupon qualifier and line 163 says each named condition raises.",
     "fix": "Add must_raise(lambda: sol.Bond(10_000, 0, 0).events(), 'periods < 1, zero coupon') and must_raise(lambda: sol.Bond(0, 0, 3).events(), 'face_cents <= 0, zero coupon') (see proj-named-conditions-context). The probe ({S}/probe_fix_r14.py) shows the new test kills this mutant."},
    {"id": "proj-mutants-killed", "check": "2.6-mutation", "location": "ledgers/FC1/mutants/ (141 files); grader/test_project.py",
     "status": "FAIL", "evidence": f"`tools/mutate_graders.py --unit FC1 --seeds 0-9` -> 'mutate_graders FC1: FAIL (139/141 killed)' ({O}/mutate_FC1_s0-9_final.out). Survivors: r14n01_sale_skips_quantity_and_settlement_checks and r14n05_bond_periods_and_face_checked_only_with_a_coupon.",
     "fix": "Add the five refusal tests in proj-named-conditions-context to grader/test_project.py, then re-run tools/mutate_graders.py --unit FC1 --seeds 0-9 and require 141/141."},
    {"id": "proj-run-labs", "check": "2.5-labs", "location": "tests/labs/FC1 (all eight twins)",
     "status": "PASS", "evidence": f"`tools/run_labs.py --unit FC1` -> 'run_labs FC1: PASS (8/8)' ({O}/run_labs_FC1.out)."},
    {"id": "proj-page-smoke", "check": "2.9-page-smoke", "location": "course/modules/FC/FC1/project.html",
     "status": "PASS", "evidence": f"`tools/page_smoke.py --unit FC1 --pages project` -> 'page_smoke FC1: PASS', labs in Pyodide 0.0 s each, in-browser grader 0.9 s ({O}/page_smoke_FC1_project.out)."},
    {"id": "proj-check-projects", "check": "2.6-spec", "location": "course/modules/FC/FC1/project.html; grader panel",
     "status": "PASS", "evidence": f"`tools/check_projects.py --unit FC1` -> 'check_projects FC1: PASS' ({O}/check_projects.out)."},
    {"id": "proj-pytest-targeted", "check": "2.9-tooling", "location": "tests/test_curriculum.py; tests/test_labs.py (selected by -k 'FC1 or project or grader')",
     "status": "PASS", "evidence": f"`.venv/bin/pytest -q tests/test_curriculum.py tests/test_labs.py -k 'FC1 or project or grader'` exit 0 ({O}/pytest_targeted_r14.out)."},
]

MUT_FILES = sorted(p.name for p in (ROOT / "ledgers/FC1/mutants").glob("*.py"))
KILL_RE = re.compile(r"^(KILLED|SURVIVED) (\S+?\.py): (.*) -> (.*)$")
mutants: list[dict[str, object]] = []
text = (ROOT / O / "mutate_FC1_s0-9_final.out").read_text(encoding="utf-8").splitlines()
for line in text:
    m = KILL_RE.match(line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    killed_by = None if killer == "None" else killer.split(" (seed")[0]
    mutants.append({"id": name, "description": desc, "killed_by": killed_by, "status": status})
assert len(mutants) == len(MUT_FILES) == 141, (len(mutants), len(MUT_FILES))

counts = {s: sum(1 for r in ROWS if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
killed = sum(1 for m in mutants if m["status"] == "KILLED")

fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 14,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 14 (did not build FC1)",
    "pin": "1431aa1d842a5d2d05fd5953c098500bf78a4307",
    "base": "762f636d (round-13 pin). The fragment named D-FC1-c.round13.json does not exist; the round-13 fragment tracked at ledgers/FC1/FC1-c.json (pin 762f636) was used as context and is overwritten by this round's fragment.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD14-FC1-c",
    "scratch": f"{S}/ (scripts and out/); temporary directories under /tmp/fc1c14-*",
    "verified_at": "2026-11-09T06:23:00+00:00",
    "verdict": verdict,
    "rows": ROWS,
    "mutants": [{"id": m["id"], "name": m["id"], "description": m["description"], "killed_by": m["killed_by"], "status": m["status"]} for m in mutants],
    "registry_flags": [
        "mishkin2021economics: registry year 2021 (Open Library record; notes.year curriculum '13th ed. (2022)' vs record 2021). The project page states no year; a published-version check beyond verify_refs --unit FC1 was not done.",
        "harris2002trading: registry year 2002 (Crossref print_year 2002; notes.year curriculum 2003). The project page states no year.",
        "course/modules/FC/FC1/grader/reference.py is git-tracked; BLUEPRINT deployment exclusion is not enforced (architect ruling 4: not a slice defect).",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 14, FC1-c, pin 1431aa1d (HEAD). Delta from round-13 pin 762f636d in the slice: project.html (32 lines: prose, the Lab 1 interpretation, the Constraints and Grading mode text (92 checks), Money and Sides conventions, fixtures D/F and the Lab 3 note); grader/test_project.py (about 470 lines: the 92-test suite); grader/reference.py and starter.py (docstrings only); tests/labs/FC1/lab-FC1-project-3.py (2 lines, docstring); ledgers/FC1/alternatives/a3 (docstring); ledgers/FC1/mutants (75 files at round 13, 136 at this pin, plus 5 written this round = 141; r13n01-03 now killed). "
        "Byte-identical since 762f636d: grader/instance.py, lab-FC1-project-1.py, lab-FC1-project-2.py, alternatives a1, a2, a4, a5. Every row was re-verified in this round from the pin; no round-13 PASS row was carried forward. Round-13 cards rows (cards-*) were not re-verified because the task scope for this round is 'No cards'; they are not carried. "
        "Exemplar blind scoring: not applicable (autograder only, no rubric). "
        "Learner-visible text: no process words. The mutants array lists every file in ledgers/FC1/mutants/ with the killing test from the final run; two survivors (r14n01, r14n05) are FAILs. "
        "Open FAIL rows and fixes are in the rows (proj-lab2-docstring, proj-named-conditions-context, proj-mutant-r14n01, proj-mutant-r14n05, proj-mutants-killed). Nothing was edited in the repository except the ledger fragment, the new mutant files r14n01-r14n05 under ledgers/FC1/mutants, and the scripts and outputs under ledgers/FC1/scripts/FC1-c-r14/."
    ),
    "summary": (
        f"FC1-c round 14 at 1431aa1d: {verdict}. Rows {len(ROWS)}: PASS {counts['PASS']}, FAIL {counts['FAIL']}, UNVERIFIABLE {counts['UNVERIFIABLE']}. "
        f"Mutants {killed}/{len(mutants)} killed; survivors r14n01 (buy-only CashTrade validation) and r14n05 (Bond checks only with a coupon). "
        "Lab 2 twin docstring says the twin has blanks. Reference 50/50 seeds; all five alternatives and one extra integer-only alternative pass seeds 0-49; the 20 sampled instances are valid and the 50 seeds give 50 distinct answers; 92 tests collected; page_smoke, run_labs, check_pages, check_dag, check_projects, ruff and mypy pass."
    ),
}

problems = ledger.validate(fragment, "FC1-c")
if problems:
    print("\n".join(problems))
    raise SystemExit(1)
out_path = ROOT / "ledgers/FC1/FC1-c.json"
out_path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out_path, "verdict", verdict, counts, f"mutants {killed}/{len(mutants)}")
