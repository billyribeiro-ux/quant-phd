import json

P = "course/modules/PC/PC3/project.html"
G = "course/modules/PC/PC3/grader"
LABS = "tests/labs/PC3/lab-PC3-project"

def row(rid, check, loc, status, ev):
    return {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}

RUN_CHECKS = "run_labs --page project (PASS 3/3); labs_r2.py (page code vs twin, expected block vs twin stdout, python -I -W error exit 0, stderr empty): all three labs True"

rows = [
 row("proj-lab1-run", "2.5-labs", f"{P} lab-PC3-project-1 (rung 1)", "PASS",
     "Round 2: `tools/run_labs.py --unit PC3 --page project` printed `run_labs PC3: PASS (3/3)`. ledgers/PC3/scripts/PC3-c-r2/labs_r2.py: page code equals tests/labs/PC3/lab-PC3-project-1.py line for line (0 differing lines); twin exit 0, stderr length 0; expected block equals twin stdout."),
 row("proj-lab1-hypothesis-numbers", "2.2-numbers", f"{P} line 57 (Lab 1 hypothesis)", "PASS",
     "ledgers/PC3/scripts/PC3-c-r2/recompute_r2.py (own game code, Lesson 4 draw order): seed 0 settlement 9980, 9 fills, cash flow -9950, inventory 1, mark 9980, P&L 30, max |inventory| 3. Every value in the hypothesis matches; expected block lines 224-231 match."),
 row("proj-lab2-completion", "2.5-labs", f"{P} lab-PC3-project-2 (rung 2, completion)", "PASS",
     "labs_r2.py: the only differing lines between page code and twin are the blanks `cash_flow = ___` (line 340) and `mark = ___` (line 341); the other lines are identical. Twin output equals the expected block (cash_flow -9950, inventory 1, mark 9980, P&L 30, identity True)."),
 row("proj-lab2-interpretation-last-quote", "2.2-numbers", f"{P} line 372 (Lab 2 interpretation, changed this round)", "PASS",
     "Sentence now reads: 'With an inventory of 1 unit, a mark at any price other than 9980 changes the P&L on this seed'. Arithmetic: P&L = -9950 + 1 x p, which equals 30 only at p = 9980. recompute_r2.py: mark at 9990 gives P&L 40. True."),
 row("proj-lab3-counterfactual", "2.2-numbers", f"{P} lines 448-600 (Lab 3 hypothesis and expected block)", "PASS",
     "recompute_r2.py check3: half-spread 15 gives 9 fills and P&L 55; delta +25. Hypothesis (line 450) and expected block (lines 597-599) match. run_labs PASS."),
 row("proj-lab3-interpretation", "2.2-numbers", f"{P} line 600 (Lab 3 interpretation)", "PASS",
     "Lab 3 code (tests/labs/PC3/lab-PC3-project-3.py) plays one seed, SEED = 0, and prints one counterfactual; the interpretation's 'not an estimate ... on other seeds' and 'the lab does not test any other seed' match the code. The first block of printed lines (settlement, fills, four numbers, identity, cash agreement) matches the code's print statements."),
 row("proj-rung1-instance-claim", "2.8-data / 2.6-spec", f"{P} line 53 and {G}/instance.py docstring lines 5-10", "PASS",
     "Round 2 check: make_instance(s) from the grader equals the independent draw (move draw then arrival draw, thresholds 0.5 / 0.25 / 0.5) for seeds 0..49 with 0 mismatches (label-mapped comparison). The Lesson 4 twin (tests/labs/PC3/lab-PC3-L04-1.py lines 56-70) uses the same draw order."),
 row("proj-conventions-constants", "2.2-numbers", f"{P} 'Conventions' list lines 391-399", "PASS",
     "N = 20, v_0 = 10000, moves +/-5 with probability 1/2, arrivals 1/4, 1/4, 1/2, q in 0..5, |I| <= 10 all match engine.py (MAX_SIZE 5, LIMIT 10, lines 29-30, 81, 77-78) and instance.py (START_CENTS, MOVE_CENTS, thresholds). Lesson 4 text (L04.html) states the same constants (Remark 1.2 and A2, A4, A5)."),
 row("proj-exemplar-a-calibration", "2.6-rubric", f"{P} Exemplar A, lines 624-652, data-scores 2,2,1,2,1", "PASS",
     "Blind re-scoring from the rubric table (lines 612-616) by the verifier: C1 2 (P&L and cash flow stated, no mark, no turn named), C2 2 (two turns with values), C3 1 ('a wider spread would help', no amount), C4 2 (parameters named, no effect stated), C5 1 ('I checked it'). Equals the official 2,2,1,2,1."),
 row("proj-exemplar-b-calibration", "2.6-rubric", f"{P} Exemplar B, lines 654-681, data-scores 4,4,4,3,4", "PASS",
     "Blind re-scoring: C1 4 (cash flow, mark, P&L with turns), C2 4 (turns 2, 5, 18 with values matching the expected block), C3 4 (5 cents, rerun of seed 0, +25), C4 3 (arrival probabilities and inventory limit with results; settlement rule not named), C5 4 (identity and cash check with values). Equals the official 4,4,4,3,4."),
 row("proj-exemplar-b-numbers", "2.2-numbers", f"{P} line 660 (Exemplar B P&L decomposition) and lines 662-668", "PASS",
     "recompute_r2.py: fills at turns 2,3,4,5,7,8,13,18,19 (match expected block lines 215-223); purchases at bid 9990+9980+9970+9980+9990 = 49910 (turns 2,3,4,8,19); sales at ask 9980+9990+9990+10000 = 39960 (turns 5,7,13,18); cash flow 39960-49910 = -9950; turn-5 inventory after = 2; turn-18 inventory after = 0; largest |inventory| = 3 (Lab 1 prints it); counterfactual fills 9, P&L 30 -> 55 (+25). All correct."),
 row("proj-exemplar-a-numbers", "2.2-numbers", f"{P} line 632 (Exemplar A 'Evidence from the log')", "FAIL",
     "Line 632 reads 'Turn 5 sold at the ask of 9980 cents, and turn 18 sold at 10000 cents, so the maker sold at the ask twice.' The expected block (lines 218-222) and recompute_r2.py show four sales at the ask: turns 5 (9980), 7 (9990), 13 (9990) and 18 (10000). The count 'twice' is false for the log the page prints. (Round 1 marked this PASS; that was wrong.) Fix: replace 'so the maker sold at the ask twice' with 'the maker sold at the ask four times, on turns 5, 7, 13 and 18' (or 'at least twice' if the passage is meant to cite two of them)."),
 row("proj-rubric-observable", "2.6-rubric", f"{P} rubric table lines 606-619", "PASS",
     "Each descriptor names a value the student can read in the analysis or the replay (fields, turn numbers, a stated change in cents, a named check and its result). The rubric region is byte-identical to the round-1 pin (no hunk in the diff covers lines 606-619)."),
 row("proj-spec-log-schema", "2.6-spec", f"{P} 'Rung 3 · Specification', Required outputs (line 384) and Inputs (line 382)", "PASS",
     "Round-1 gap closed: Required outputs now lists the log keys (seed, settlement_cents, turns), the 9 turn-record keys, the arrival names and the None rule. Checked against engine.py lines 88-98 and 100: identical key sets. quote state keys (turn, inventory, cash_cents, max_size, limit, history) match engine.py lines 66-73. The page's game_log command run in a scratch folder with reference market_maker and engine.py (seed 7919) wrote 20 turns with keys seed, settlement_cents, turns; replay returned {cash_flow_cents -49800, inventory_end 5, inventory_mark_cents 49650, pnl_cents -150}. Grading-mode paragraph now says the analysis is scored by the student (self-assessment), so the round-1 'who grades' gap is closed."),
 row("proj-hours-arithmetic", "2.6-hours", f"{P} 'Time budget' table lines 414-428; {G[:-7]}index.html line 31 and data-hours attributes", "PASS",
     "Table rows 1+1+3+2+2+4+1 = 14 (line 425). data-hours-project=14 (line 33) and eyebrow '14 hours' (line 35). Hub: 'Tier U · 50 hours' (index.html line 31), data-hours-lessons=36 + 14 = 50. 14/50 = 28.0 %, within 10-40 % (check_pages PASS)."),
 row("proj-hub-placement-conflict", "2.6-placement", f"{P} line 42 vs course/modules/PC/PC3/index.html placement section", "PASS",
     "Round-1 conflict closed. project.html line 42 now reads 'If you reached the placement bar and answered both skill checks on the module page, skip rungs 1 and 2'. index.html states 'To skip rungs 1 and 2, you must reach the bar and answer both skill checks.' Same rule."),
 row("proj-grader-35-checks", "2.6-autograder", f"{P} 'Grading mode' (line 388)", "PASS",
     "Round-1 figure 35 was stale. `pytest --collect-only -q` in a scratch copy with the reference module prints '37 tests collected'. Page says 37 (line 388). Parametrized SEEDS tests: 16 (8 tests x 2 seeds); the other 21 run on SEED only. Page counts 16 and 21: correct."),
 row("proj-grader-seed-scope-claim", "2.6-autograder", f"{P} 'Constraints' Integrity sentence (line 386) and 'Grading mode' (line 388)", "PASS",
     "Round-1 claim 'the second instance of every test' is gone. Page now says 'on the 16 checks that run on a second seed' (line 386) and lists the 16 (line 388). Verified count: 16 SEEDS-parametrized tests (test_project.py lines 139, 223, 240, 256, 271, 286, 294, 323, 344 with SEEDS=2) and 21 single-seed tests, total 37."),
 row("proj-grader-no-print", "2.6-autograder", f"{P} 'Constraints' ('No function prints or warns', line 386); {G}/test_project.py lines 334-338", "PASS",
     "test_no_function_prints added (lines 334-338, capsys). mutate_graders now kills v08 (print in replay) by test_no_function_prints on seed 0. Warnings: pytestmark filterwarnings('error') (line 30); v09 (warnings.warn in quote) killed. Note: the worked example's Lab 1 replay itself prints (see proj-lab1-replay-prints)."),
 row("proj-grader-replay-from-fills", "2.6-autograder", f"{P} Conventions 'The P&L' bullet (line 398); {G}/test_project.py lines 257-267", "PASS",
     "test_replay_sums_the_fills_not_the_running_totals (lines 257-267) added. Mutant v04 (replay copies last running totals) killed by it on seed 0. Mutant v11 (every fill booked at the bid) killed by test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0]. Cash flow = sum of fill cash flows is now tested."),
 row("proj-grader-mypy-strict", "2.6-typing", f"{G}/test_project.py (lines 139-165 changed)", "PASS",
     "Scratch dir with engine.py, instance.py, test_project.py and market_maker.py = reference.py: `mypy --strict --no-incremental --python-version 3.14 test_project.py engine.py instance.py market_maker.py` -> 'Success: no issues found in 4 source files'. (With round-1 test file: 5 errors at lines 157-162.) The repo gate `.venv/bin/mypy` covers tools and tests only, so this grader is checked here by hand."),
 row("proj-grader-reference", "2.6-autograder", f"{G}/reference.py", "PASS",
     "`tools/run_graders.py --unit PC3 --seeds 0-49` -> 'run_graders PC3: PASS (reference 50/50 seeds, slowest 0.1 s)'. Scratch run: reference market_maker, seeds 0 and 7919: '37 passed' both."),
 row("proj-grader-starter-fails", "2.6-autograder", f"{G}/starter.py", "PASS",
     "Scratch run with starter.py as market_maker.py, QF_SEED=0: '20 failed, 17 passed' (the 17 do not call the student's functions). Suite fails on starter, as required."),
 row("proj-grader-instances", "2.6-autograder", f"{G}/instance.py", "PASS",
     "make_instance(s) equals the independent draw for seeds 0..49 (0 mismatches). Returns seed, label 'SIMULATED', start_cents, fair_path_cents (21 ints), arrivals (20 names), settlement_cents, as the docstring (lines 27-53) states."),
 row("proj-grader-messages", "2.6-autograder", f"{G}/test_project.py lines 40-55, 150-163, 229-235, 268, 288-292", "PASS",
     "Failure messages name the property and never interpolate a computed value; the only f-string is must_refuse's phrase (a named condition, not a computed value). Checked by reading every expect/pytest.fail message in the 417-line file."),
 row("proj-named-refusals", "2.6-autograder", f"{G}/test_project.py lines 166-218", "PASS",
     "must_refuse used for exactly the four named conditions: bid == ask (line 171), bid > ask (line 176), size 6 (187), size -1 (192), log of 19 and 21 turns (210), filled with no price (217). Each names the page's message phrase ('bid must be below ask', 'size must lie in 0..5', 'a log has exactly 20 turns', 'a filled turn needs a fill price'). mutate_graders kills v10 (21-turn log accepted) and v12 (filled turn without price skipped)."),
 row("proj-builder-mutants", "2.6-autograder", "ledgers/PC3/mutants/m01..m10", "PASS",
     "tools/mutate_graders.py --unit PC3 (seeds 0-9): all ten builder mutants KILLED (see mutants list). m08 now returns zeros, and its description matches (see proj-mutant-m08-description)."),
 row("proj-verifier-mutants", "2.6-autograder", "ledgers/PC3/mutants/v01..v08 (round-1 verifier mutants)", "PASS",
     "Round-1 survivors v04 and v08 are now killed (v04 by test_replay_sums_the_fills_not_the_running_totals, v08 by test_no_function_prints). All of v01..v08 KILLED in the round-2 mutate_graders run (22/22)."),
 row("proj-mutant-m08-description", "2.6-autograder", "ledgers/PC3/mutants/m08_hard_coded_answer_for_any_log.py lines 1-2 and 34", "PASS",
     "Docstring now reads 'replay returns all zeros, a hard-coded answer, for every log'. Line 34 returns all four zeros before any other statement, so the description matches the code (for every log that passes the 20-turn length check, which is the only input the replay checks first). Round-1 FAIL (description said seed-0 answer) is closed."),
 row("proj-alternatives-1-2-4-5", "2.6-autograder", "ledgers/PC3/alternatives/alt1, alt2, alt4, alt5", "PASS",
     "ledgers/PC3/scripts/PC3-c-r2/run_candidates.py --seeds 0-49: alt1 PASS 50/50, alt2 PASS 50/50, alt4 PASS 50/50, alt5 PASS 50/50."),
 row("proj-alt3-replay", "2.6-autograder", "ledgers/PC3/alternatives/alt3_inventory_skew.py (replay lines 26-46)", "PASS",
     "Round-1 FAIL closed: the replay now books each fill from its own price (price == bid_cents -> purchase, else sale) and sums units and cash; it is not a running-totals copy. run_candidates.py: PASS 50/50 seeds; by reading, cash = sum of fill cash flows, units = sum of fill sides."),
 row("proj-alternative-6", "2.6-autograder", "ledgers/PC3/scripts/PC3-c-r1/alt6_size_zero_on_multiples_of_three.py", "PASS",
     "run_candidates.py --seeds 0-49: PASS 50/50 (round-1 verifier alternative, re-run on this pin)."),
 row("proj-alternative-7-8-verifier", "2.6-autograder", "ledgers/PC3/scripts/PC3-c-r2/alt7_*.py and alt8_*.py", "PASS",
     "Two new verifier alternatives (1-cent half-spread at size 5 with a reversed-scan mid and a fold replay; a 25-cent half-spread with size falling to 0 at the limit and a comprehension replay). run_candidates.py --seeds 0-49: PASS 50/50 each."),
 row("proj-lint-ruff", "2.9-lint", f"{G} and {LABS}-*.py", "PASS",
     "`.venv/bin/python -m ruff check course/modules/PC/PC3/grader tests/labs/PC3` -> 'All checks passed!'; `ruff format --check` -> '14 files already formatted'. ruff check ledgers/PC3 -> All checks passed!"),
 row("proj-mypy-labs", "2.9-typing", f"{LABS}-1..3.py", "PASS",
     "`.venv/bin/mypy --no-incremental` (repo strict config, files = tools, tests) -> 'Success: no issues found in 385 source files'. `mypy --strict tests/labs/PC3/*.py` -> 'Success: no issues found in 9 source files'."),
 row("proj-page-smoke", "2.9-page", f"{P}", "PASS",
     "`tools/page_smoke.py --unit PC3 --pages project` -> 'page_smoke modules/PC/PC3/project.html: PASS', 'page_smoke PC3: PASS'; in-browser grader 'All 37 tests pass on seed 1165722733'. Note: check_pages with --page project fails because --page is a lesson-only flag; the unit-level `check_pages.py --unit PC3` (no --page) PASSes, and project pages are checked by check_projects. Not a page defect."),
 row("proj-check-tools", "2.9-tools", "tools/check_pages.py, check_dag.py, check_projects.py --unit PC3", "PASS",
     "`check_pages.py --unit PC3` -> 'check_pages PC3: PASS'; `check_dag.py --unit PC3` -> 'check_dag PC3: PASS'; `check_projects.py --unit PC3` -> 'check_projects PC3: PASS'. verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'."),
 row("proj-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3 --page project", "PASS",
     "Round-2 command: 'run_labs PC3: PASS (3/3)' for the project page. The unit-wide run of other labs is outside this slice."),
 row("proj-banned-and-process-words", "2.9-prose", f"{P} (all text, code and expected blocks); {G}/*.py; {LABS}-*.py", "PASS",
     "grep (case-insensitive) for build, builder, round, verifier, REQUESTS, fixer, architect, planner, scratch in project.html and the grader and project-lab files: no hits."),
 row("proj-notation", "2.7-notation", "notation/notation.json and course/modules/PC/PC3/project.html math", "PASS",
     "Registry (8 symbols): T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. Page math (36 distinct snippets: N, t, v_t, v_0, v_20, b_t, a_t, q_t, I, I_20, pnl, p-free probabilities) uses none of the registered symbols with another meaning. Macro set unused."),
 row("proj-dag-terms", "2.8-dag", f"{P} (all text)", "PASS",
     "check_dag PC3 PASS. Terms used: market-making game (linked, L04, in closure); adverse selection, inventory, the spread, mark-to-market P&L are plain prose (architect D3/D4, no link, no dfn) and appear only in plain words."),
 row("proj-references", "2.8-refs", f"{P} 'Reading' (lines 699-706) and references section", "PASS",
     "data-cite keys zhou2008practical and crack2015heard exist in references/references.json (lines 23402 and 6222). verify_refs --offline: 560 entries, 0 problems. The page cites both by key with no edition, page or problem (line 701)."),
 row("proj-js-claims", "2.8-claims", f"{P} lines 433, 685, 719 (browser storage claims)", "PASS",
     "course/assets/js/grader.js lines 33-79 store the draft with store.put on each edit (debounced 400 ms); rubric.js lines 8 and 85-97 keep scores in the store via store.js, which is the learner's browser backend; store.js line 7 says nothing leaves the browser. The claims 'saved in this browser as you type', 'your scores stay in this browser' and 'nothing you write leaves it' match."),
 row("proj-local-commands", "2.6-spec", f"{P} lines 383-384 (game_log command) and 439-440 (local pytest)", "PASS",
     "Game-log command run verbatim in a scratch folder: writes a valid 20-turn JSON log. Local pytest command with the same flags run: 37 collected, reference passes both seeds."),
 row("proj-known-limitation", "2.6-autograder (stated limitation)", f"{P} line 386; {G}/engine.py docstring line 19", "PASS",
     "engine.py line 19: 'The engine does not show the fair value to the policy. The log does show the settlement value, after the last turn.' The turn records have no fair-value key (engine.py lines 88-98). The stated limitation is accurate, and the 'second seed' clause now refers to the 16 counted checks."),
 row("proj-ladder-scope", "2.6-projects (ladder and scope)", f"{P} lines 40-48; curriculum/06-profession-capstone.yaml:175-182", "PASS",
     "Rung 1 worked example (Lab 1), rung 2 completion (Lab 2), rung 3 independent project graded by autograder and rubric, rung 4 stretch. Check_projects PASS. Rung 3 is a single module market_maker.py (see notes on plan file names)."),
 row("proj-rubric-atlas-studios", "2.6-atlas / 2.6-studios", "plans/PC3-build-plan.md section 8", "PASS",
     "No Atlas milestone and no studio is named for PC3; check_projects PASS. plans/PC3-build-plan.md is byte-identical to the round-1 pin (not in the diff)."),
 row("proj-stretch", "2.6-projects (rung 4)", f"{P} lines 690-697", "PASS",
     "Stretch items state no numbers, so no computation is claimed: distribution over seeds 0-199, informed share 0.6 with uninformed split evenly, inventory limit 5 units. Each is a change the engine's rules can express."),
 row("proj-twin-rules", "2.5-labs (twin rules)", f"{LABS}-1..3.py", "PASS",
     "Each twin imports only __future__, random and typing; uses random.Random(seed); ends with an unconditional `main()` call (lines 154, 127, 138), no __name__ guard. Each ran under python -I -W error with exit 0 and empty stderr."),
 row("proj-exception-types", "2.6-autograder (exception rule)", f"{G}/test_project.py lines 47-55, 168-218", "PASS",
     "must_refuse is used only for the four named invalid inputs (see proj-named-refusals). Other tests expect no exception; the 'Any other invalid input' sentence (line 409) is matched by the test design."),
 row("proj-lab1-replay-prints", "2.2-labs vs 2.6-autograder", f"{P} Lab 1 code lines 176-179 (replay prints per fill) and line 232 (interpretation); spec 'No function prints or warns' line 386; twin {LABS}-1.py lines 168-171, 176-179", "FAIL",
     "The worked example's replay prints a line for each fill (page lines 176-179), and the page says 'The labs show the replay that your replay function must reproduce'. Probe: the Lab 1 replay function copied verbatim into a scratch market_maker.py (reference quote) and run against test_project.py: 2 failed, 35 passed. FAILED test_no_function_prints ('no function may print'), and FAILED test_filled_turn_without_a_price_is_refused (TypeError, because int(None) runs before any refusal, page's named ValueError is never raised). The same missing named refusal exists in the Lab 2 (line 337) and Lab 3 (line 551) replays. Fix: move the per-fill print from Lab 1's replay into main() (iterating log['turns']) and update the interpretation (line 232) to say so; add the 'a filled turn needs a fill price' ValueError check to the three lab replays, or state on the page that the labs omit the named refusals. Lab twins are edited only by the builder."),
]

mutants = [
 {"id": "m01_pnl_omits_inventory_mark", "description": "Student error: the P&L is cash only, with the inventory mark omitted.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
 {"id": "m02_sell_cash_sign_flipped", "description": "Student error: the cash flow of a fill has the wrong sign on every side.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
 {"id": "m03_unfilled_orders_counted", "description": "Student error: the filled flag is ignored, so unfilled turns are replayed as fills.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
 {"id": "m04_mark_uses_last_quote_mid", "description": "Student error: the inventory is marked at the last quoted mid, not at the settlement value.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
 {"id": "m05_settlement_rounded_to_dime", "description": "Student error: the settlement is rounded to the nearest dime before it marks the inventory.", "killed_by": "test_inventory_is_marked_at_the_settlement_value_not_the_quote_mid (seed 0)"},
 {"id": "m06_last_turn_omitted", "description": "Student error: the replay loop stops one turn early and omits the last turn.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
 {"id": "m07_sell_adds_to_inventory", "description": "Student error: a sale adds to inventory instead of reducing it.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
 {"id": "m08_hard_coded_answer_for_any_log", "description": "Student error: replay returns all zeros for every log.", "killed_by": "test_filled_turn_without_a_price_is_refused (seed 0)"},
 {"id": "m09_quoted_size_above_maximum", "description": "Student error: the quote posts size 6, above the largest quoted size of 5.", "killed_by": "test_quotes_are_legal_on_every_turn[0] (seed 0)"},
 {"id": "m10_crossed_quote_on_turn_one", "description": "Student error: on turn 1 the quote is locked (bid equal to ask).", "killed_by": "test_quotes_are_legal_on_every_turn[0] (seed 0)"},
 {"id": "v01_quote_swaps_bid_and_ask_after_a_fill", "description": "Student error: after the first fill the bid and the ask are swapped.", "killed_by": "test_quotes_are_legal_on_every_turn[0] (seed 0)"},
 {"id": "v02_quote_size_by_true_division", "description": "Student error: the quoted size uses true division (float 1.0).", "killed_by": "test_quotes_are_legal_on_every_turn[0] (seed 0)"},
 {"id": "v03_replay_marks_at_last_fill_price", "description": "Student error: the inventory is marked at the price of the last fill.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
 {"id": "v04_replay_copies_last_running_totals", "description": "Student error: replay copies the last turn's running cash and inventory instead of summing the fills.", "killed_by": "test_replay_sums_the_fills_not_the_running_totals (seed 0)"},
 {"id": "v05_replay_side_from_arrival_name", "description": "Student error: replay takes the side of each fill from the arrival name.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
 {"id": "v06_replay_mark_by_true_division", "description": "Student error: the inventory mark uses true division (a float).", "killed_by": "test_money_and_units_are_integers[0] (seed 0)"},
 {"id": "v07_replay_int_of_none_not_refused", "description": "Student error: a filled turn with no fill price crashes with TypeError instead of ValueError.", "killed_by": "test_filled_turn_without_a_price_is_refused (seed 0)"},
 {"id": "v08_replay_leaves_a_debug_print", "description": "Student error: a debugging print is left in replay (the spec says no function prints).", "killed_by": "test_no_function_prints (seed 0)"},
 {"id": "v09_quote_warns_on_turn_one", "description": "Student error: quote calls warnings.warn on turn one (the spec says no function prints or warns). NEW in round 2.", "killed_by": "test_quotes_are_legal_on_every_turn[0] (seed 0)"},
 {"id": "v10_replay_accepts_more_than_twenty_turns", "description": "Student error: replay refuses fewer than 20 turns but accepts 21. NEW in round 2.", "killed_by": "test_replay_refuses_a_log_that_is_not_twenty_turns[21] (seed 0)"},
 {"id": "v11_replay_books_every_fill_at_the_bid", "description": "Student error: every fill's cash is booked at the bid, so sales are short by the spread. NEW in round 2.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
 {"id": "v12_replay_skips_filled_turn_without_price", "description": "Student error: a filled turn with no fill price is skipped instead of refused with ValueError. NEW in round 2.", "killed_by": "test_filled_turn_without_a_price_is_refused (seed 0)"},
]

notes = (
 "Scope: project.html, grader/ (engine.py, instance.py, reference.py, starter.py, test_project.py), tests/labs/PC3/lab-PC3-project-1..3.py, "
 "builder mutants m01-m10, round-1 verifier mutants v01-v08, four new round-2 mutants v09-v12, builder alternatives alt1-alt5, round-1 alt6, new round-2 alt7 and alt8. "
 "Pin 67c47689 (round-1 pin 1c1645f3). Delta read in full: project.html hunks at lines 4, 34-56, 369, 381-412, 415, 438, 619-622; test_project.py (quotes-legal cast, new replay-sums test, new no-print test); alt3; m08; v01-v08; scripts. "
 "Plan deviation (not a row): plans/PC3-build-plan.md section 5.2 names policy.py and pnl.py, and section 5.1 says so too; the built page uses one module market_maker.py with quote and replay. The page and grader are consistent with each other (market_maker imported by test_project.py), so this is a plan-to-build naming change, not a page defect. Architect decisions do not rule on file names. "
 "Round-1 PASS rows were re-derived, not carried. Round-1 row proj-exemplar-a-numbers was wrong (PASS); it is now FAIL. "
 "Gate note: the repo mypy gate (pyproject files = tools, tests) does not include course grader files; strict mypy on the grader was run by hand (proj-grader-mypy-strict). "
 "Commands run and outputs are cited in the rows. "
 "NOT CHECKED: (1) live Crossref or network verify_refs (only --offline run); (2) whole-repo gates (full pytest, build_site, render_curriculum, fetch_data --check, check_pages --all for other units, run_graders --all); (3) hub, lessons and cards (other slices; placement and hours cross-checked only); (4) browser visual check by hand of the rubric and self-assessment UI (page_smoke run only); (5) ledger.py was not run, so no merged ledgers/PC3.verification.json; (6) the mutation run used seeds 0-9 (mutate_graders default), and the four new mutants and alt7/alt8 used seeds 0-49. "
 "No edits under course/, tests/, tools/, references/ or plans/. Scratch dirs only under /tmp."
)

frag = {
 "unit": "PC3",
 "slice": "c",
 "round": 2,
 "verifier": "independent verifier (Haiku 5.5), round 2, slice c",
 "pin": "67c47689c49435bc0e6639e3de4feded5eefdd64",
 "base": "round 1 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round1.json (pin 1c1645f3), context only; no round-1 PASS row carried, all re-derived",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE2-PC3-c",
 "scratch": "/tmp/pc3c-r2-* (scratch workspaces only; every cited result comes from a script under ledgers/PC3/scripts/PC3-c-r2/ or a command listed in the row)",
 "verified_at": "2026-11-04T08:15:02+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": notes,
 "summary": "Slice c (round 2): verdict FAIL. Rows 50: PASS 48, FAIL 2, UNVERIFIABLE 0. Mutants: 22 of 22 killed (builder m01-m10, round-1 v01-v08 including former survivors v04 and v08, new v09-v12). Alternatives: alt1-alt8 pass 50/50 seeds. FAIL rows: proj-exemplar-a-numbers (line 632: 'sold at the ask twice', log has four), proj-lab1-replay-prints (Lab 1 replay prints and omits the named refusal, so copying it fails test_no_function_prints).",
}

with open("ledgers/PC3/PC3-c.json", "w", encoding="utf-8") as f:
    json.dump(frag, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("rows", len(rows), "mutants", len(mutants))
