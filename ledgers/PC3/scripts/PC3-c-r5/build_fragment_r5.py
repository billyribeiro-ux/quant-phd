"""Round-5 verifier fragment for PC3 slice c (project.html, grader, project labs, mutants, alternatives), pin 7376a5e.

Builds ledgers/PC3/PC3-c.json from the round-5 scripts' outputs. Mutant rows are read from mutate_all_r5.out.
Run from the checkout root: .venv/bin/python ledgers/PC3/scripts/PC3-c-r5/build_fragment_r5.py
"""
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE5-PC3-c")
S = ROOT / "ledgers/PC3/scripts/PC3-c-r5"
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

P = "course/modules/PC/PC3/project.html"
G = "course/modules/PC/PC3/grader"
R5 = "ledgers/PC3/scripts/PC3-c-r5"
REF_RUN = "run_gates_r5.sh outputs"

rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    rows.append(r)


PASS = "PASS"
FAIL = "FAIL"

# ---- carried from round 4 ids, re-verified this round (whole project.html read, lines 1-732) ----
row("proj-exemplar-a-numbers", "2.2-numbers", f"{P} line 643 (Exemplar A 'Evidence from the log')", PASS,
    f"Re-read line 643: 'Turn 5 sold at the ask of 9980 cents, and turn 18 sold at the ask of 10000 cents'. "
    f"Lab 1 output (lines 225, 229 of the page's expected block; twin run {R5}/labs_page_vs_twin_r5.out): turn 5 "
    "'sells at the ask 9980', turn 18 'sells at the ask 10000'.")
row("proj-lab1-replay-prints", "2.5-labs", f"{P} Lab 1 code (lines 85-185: draw_game, quote, maker_side, play, replay)", PASS,
    "Read lines 85-185 of the page block in full: no print or warn call in draw_game, quote, maker_side, play or replay; "
    "print calls only in main (lines 189-215). Page code equals twin tests/labs/PC3/lab-PC3-project-1.py line for line "
    f"(0 differing lines, {R5}/labs_page_vs_twin_r5.out).")
row("proj-lab1-run", "2.5-labs", f"{P} lab-PC3-project-1 (rung 1)", PASS,
    "run_labs.py --unit PC3 --page project: 'run_labs PC3: PASS (3/3)' (ledgers/PC3/scripts/PC3-c-r5/run_labs_project.out). "
    "Twin run with python -I -W error exit 0, stderr 0 bytes, output equals the expected block (labs_page_vs_twin_r5.out).")
row("proj-lab1-hypothesis-numbers", "2.2-numbers", f"{P} line 57 (Lab 1 hypothesis)", PASS,
    "Independent re-derivation from Conventions and Lesson 4 A1/A2 only (indep_numbers_r5.py, indep_numbers_r5.out): fills 9, "
    "cash -9950, inventory 1, settlement 9980, mark 9980, P&L 30, largest |inventory| 3, identity True. All match line 57.")
row("proj-lab2-completion", "2.5-labs", f"{P} lab-PC3-project-2 (rung 2 completion), lines 349-350", PASS,
    "labs_page_vs_twin_r5.out: page code differs from the twin on exactly two lines (105-106: 'cash_flow = ___', 'mark = ___') "
    "and the twin output equals the expected block (-9950, 1, 9980, 30, identity True).")
row("proj-lab2-interpretation-last-quote", "2.2-numbers", f"{P} line 381 (Lab 2 interpretation)", PASS,
    "Rung 1 result reproduced by the completed twin. The claim that a mark other than 9980 changes P&L with inventory 1 is the "
    "identity P&L = cash flow + 1 x mark (Conventions line 407), so it holds for every mark value.")
row("proj-lab3-counterfactual", "2.2-numbers", f"{P} lines 456-612 (Lab 3)", PASS,
    "Lab 3 twin output: settlement 9980, fills 9, cash -9950, inventory 1, mark 9980, P&L 30; half-spread 15: fills 9, P&L 55, "
    "change 25. Independent re-derivation (indep_numbers_r5.out): fills 9, P&L 55, change 25.")
row("proj-lab3-interpretation", "2.2-numbers", f"{P} line 611 (Lab 3 interpretation)", PASS,
    "The text says the 25-cent change is a difference on one seed and that the lab tests no other seed. Lab 3 runs seed 0 only "
    "(SEED = 0, play(SEED, ...) in the twin lines 577-596). Verified against indep_numbers_r5.out.")
row("proj-rung1-instance-claim", "2.8-data / 2.6-spec", f"{P} line 53; {G}/instance.py lines 5-10", PASS,
    "lab_draws_vs_instance_r5.py: draw_game(0) of lab-PC3-project-1 and of lab-PC3-project-3 equal make_instance(0) "
    "(fair path True, arrivals True, settlement 9980). Lesson 4 L04.html line 235-254 draws the same way (move, then arrival).")
row("proj-conventions-constants", "2.2-numbers", f"{P} 'Conventions' list lines 402-407", PASS,
    "N = 20 (HORIZON 20); v0 = 10000; move +5/-5 with prob 1/2 (instance.py lines 36-38); arrivals 1/4, 1/4, 1/2 (instance.py "
    "lines 40-45); 0 <= q <= 5 (engine.py MAX_SIZE 5); |I| <= 10 (engine.py LIMIT 10, line 81); cash identity cash += -side*price "
    "(engine.py line 86); P&L = cash flow + I20 x v20 (replay).")
row("proj-exemplar-a-calibration", "2.6-rubric", f"{P} Exemplar A, lines 635-663 (data-scores 2,2,1,2,1)", PASS,
    "Blind scoring against descriptors (lines 623-627): C1 2 (P&L and cash flow stated, mark not), C2 2 (two turns, values match), "
    "C3 1 ('a wider spread would have helped', no amount), C4 2 (parameters named, no effect), C5 1 ('I checked it'). "
    "Matches data-scores and the annotations (lines 653-659) within one level.")
row("proj-exemplar-b-calibration", "2.6-rubric", f"{P} Exemplar B, lines 665-693 (data-scores 4,4,4,3,4)", PASS,
    "Blind scoring: C1 4 (three values, turns 2-19 named), C2 4 (turns 2, 5, 18, values match), C3 4 (change 10->15, same seed, "
    "P&L change +25), C4 3 (settlement rule not named), C5 4 (identity and final-cash agreement). Matches data-scores and the "
    "annotations (lines 683-688) within one level.")
row("proj-exemplar-b-numbers", "2.2-numbers", f"{P} lines 669-678 (Exemplar B)", PASS,
    "indep_numbers_r5.out: bids bought at turns 2,3,4,8,19 sum 49910; asks sold at turns 5,7,13,18 sum 39960; difference -9950. "
    "Inventory after turn 19 is 1, mark 9980, counterfactual 30 -> 55 (+25), largest inventory 3. All match the page.")
row("proj-exemplar-b-arrival-sensitivity", "2.2-numbers / 2.9-scope", f"{P} line 677 (Exemplar B 'Assumptions and limits')", PASS,
    "Re-verified with an independent simulator (indep_numbers_r5.out): p_buy 0.20 gives 9 fills and P&L 30 (unchanged); "
    "p_buy 0.30 gives 11 fills and P&L 40; p_sell 0.26 gives 11 fills and P&L 40. The sentence 'changing them can change the fills "
    "and the P&L on seed 0, while a small change may change neither' is true of both halves.")
row("proj-rubric-observable", "2.6-rubric", f"{P} rubric table lines 619-629", PASS,
    "Every descriptor names an observable: values equal to replay output (C1), turns cited by number and field (C2), a rerun "
    "with the amount in cents (C3), named parameters and what each moves (C4), a named check with its result (C5). "
    "Note (not a failure): C2 level 3 ('at least one cited value does not match the log') lets a mismatched value meet the bar "
    "('meets the bar at level 3 or above', line 620). It is observable, so it is noted, not failed.")
row("proj-spec-log-schema", "2.6-spec", f"{P} 'Required outputs' line 393", PASS,
    "quote state keys turn, inventory, cash_cents, max_size, limit, history match engine.py lines 66-73; replay keys match "
    "reference and test_project.py line 230; log keys seed, settlement_cents, turns and the nine record keys match engine.py "
    "lines 87-98. Command in line 393 run with the venv Python in a scratch copy: writes a log with keys seed, settlement_cents, turns and 20 records (scratch_checks_r5.out).")
row("proj-hours-arithmetic", "2.3-hours", f"{P} 'Time budget' lines 425-434; index.html lines 167-168", PASS,
    "Table: 1+1+3+2+2+4+1 = 14. Hub: 2+6+4+2 = 14 and 36 + 14 = 50; 14/50 = 28.0 percent. Own estimate of a competent learner: "
    "reading and Lab 1 about 1 h, Lab 2 about 1 h, quote and replay with 37-test debugging about 5-6 h, analysis and "
    "self-assessment about 4-5 h, total about 11-13 h, within 30 percent of 14. Hub split categories differ from the page "
    "split (6 h autograded vs 5 h quote+replay; 2 h final check vs 3 h), with the same total; noted, not an arithmetic error.")
row("proj-hub-placement-conflict", "2.9-scope / 2.8-cross-page", f"{P} lines 42-48 vs index.html lines 128-137", PASS,
    "project.html lines 40-48 and index.html lines 128-137 are unchanged since the round-4 pin (git diff 9a02b1af..7376a5e lists "
    "only index.html lines 34, 48, 71-74 and project.html lines 386-730). The ladder says rungs 1-2 are skipped only after both "
    "placement skill checks, and the hub places exactly those two checks. No conflict in the ladder wording. The premise defect "
    "of those checks is row proj-hub-skill-check-premise.")
row("proj-hub-filenames", "2.8-cross-page / 2.6-spec", "course/modules/PC/PC3/index.html lines 160 and 167 (outside slice c; re-verified)",
    FAIL,
    "index.html line 160: 'Write <code>policy.py</code>, the quoting rule, and <code>pnl.py</code>, the replay'; line 167: 'The "
    "autograded policy.py and pnl.py take 6 hours'. project.html line 393 names market_maker.py; grader/test_project.py line 26 "
    "imports market_maker. Plan section 5.2 (plans/PC3-build-plan.md line 337 and 340) also names policy.py and pnl.py. "
    "index.html has no change on these lines since the round-4 pin.",
    "Align the names. Either rename the page and grader to the plan's policy.py (quote) and pnl.py (replay), or record an "
    "architect ruling for market_maker.py, and then make index.html lines 160 and 167 use the same names as project.html.")
row("proj-hub-seed-scope", "2.9-scope / 2.2-numbers (cross-page)", "course/modules/PC/PC3/index.html lines 55 and 160 (outside slice c)",
    FAIL,
    "index.html line 55: 'pass the autograder on seeds 0 to 49'; line 160: 'The autograder runs them on seeds 0 to 49'. "
    "project.html line 397 (Grading mode): sixteen checks run on your seed and seed + 7919, and twenty on your seed; "
    "course/assets/js/grader.js line 53 derives one seed from the workspace ID. Plan section 5.2 line 348 says 'seeds 0-49' for the grading mode, so "
    "the hub follows the plan and the page does not. The run with --seeds 0-49 is the verifier's gate, not the learner's autograder.",
    "Decide the grading rule once and make both pages say it. If the page stands (own seed plus seed + 7919), rewrite index.html "
    "lines 55 and 160 to say so; if the plan's 0-49 stands, change project.html lines 395-397 and grader.js. Record the ruling.")
row("proj-hub-skill-check-premise", "2.2-numbers / 2.9-scope (cross-page)", "course/modules/PC/PC3/index.html lines 128-137 (outside slice c)",
    FAIL,
    "index.html line 129: 'a market maker buys one unit at an ask of 10 005 cents ... cash flow' (answer -10005, explanation: 'A buy fill "
    "pays the ask'); line 134: 'after that fill the inventory is +1 unit'. project.html line 393 ('a fill at the ask is a sale by the "
    "maker') and Conventions line 406 (maker sale at the ask: cash +a, inventory -1) contradict this. index.html is unchanged here.",
    "Restate the two skill checks in the project's convention: a maker purchase at the bid (cash flow -bid, inventory +1), or a "
    "maker sale at the ask (cash flow +ask, inventory -1), with the answer computed from Conventions line 406.")
row("proj-quote-rule-first-fill-survivor", "2.8-grader / 2.6-spec", f"{P} Rung 3 time-budget row line 429; alternatives/alt6", PASS,
    "Line 429 reads 'a quoting rule in market_maker.py that is legal on every turn for both instances' (no last-fill requirement). "
    "Spec and Constraints (lines 393-395) only require legality. alt6 (quote mid from the first fill) passes 50/50 seeds "
    "(scripts/PC3-c-r5/run_alts_r5.py output alts_all_r5.out).")
row("proj-builder-mutants", "2.6-mutation", "ledgers/PC3/mutants/m01..m10", PASS,
    "mutate_graders.py --unit PC3 --seeds 0-49 (mutate_all_r5.out): m01..m10 each KILLED (listed in the mutants array).")
row("proj-verifier-mutants", "2.6-mutation", "ledgers/PC3/mutants/v01..v16", PASS,
    "mutate_all_r5.out: v01..v16 each KILLED.")
row("proj-mutant-m08-description", "2.6-mutation", "ledgers/PC3/mutants/m08_hard_coded_answer_for_any_log.py lines 1-2 and 34",
    PASS, "Docstring line 1: 'Student error: replay returns all zeros, a hard-coded answer, for every log.' Line 34 returns all-zero "
    "fields for every 20-turn log. KILLED by test_filled_turn_without_a_price_is_refused (seed 0) in mutate_all_r5.out.")
row("proj-verifier-mutants-r3-new", "2.6-mutation", "ledgers/PC3/mutants/v13..v16", PASS,
    "v13..v16 KILLED in mutate_all_r5.out. v17 (round-4 survivor) is no longer a mutant: it is ledgers/PC3/alternatives/alt6, "
    "a legal rule that passes 50/50 seeds.")
row("proj-alternatives-1-2-4-5", "2.6-alternatives", "ledgers/PC3/alternatives/alt1, alt2, alt4, alt5", PASS,
    "run_alts_r5.py (alts_all_r5.out): each passes 50/50 seeds on the checkout's grader files with the page flags.")
row("proj-alt3-replay", "2.6-alternatives", "ledgers/PC3/alternatives/alt3_inventory_skew.py", PASS,
    "alts_all_r5.out: passes 50/50 seeds.")
row("proj-alternative-6", "2.6-alternatives", "ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py", PASS,
    "alts_all_r5.out: passes 50/50 seeds. Docstring line 1 says it is a legal rule under the spec.")
row("proj-alternative-7-8-verifier", "2.6-alternatives", "ledgers/PC3/scripts/PC3-c-r2/alt7_*.py, alt8_*.py", PASS,
    "alts_all_r5.out: both pass 50/50 seeds.")
row("proj-alternative-9-10-verifier-r3", "2.6-alternatives", "ledgers/PC3/scripts/PC3-c-r3/alt9_*.py, alt10_*.py", PASS,
    "alts_all_r5.out: both pass 50/50 seeds.")
row("proj-alternatives-r4-new", "2.6-alternatives", "ledgers/PC3/scripts/PC3-c-r4/alts/alt11, alt12, alt13", PASS,
    "alts_all_r5.out: alt11, alt12 and alt13 each pass 50/50 seeds.")
row("proj-grader-35-checks", "2.6-spec / 2.5-tests", f"{P} line 397 and {G}/test_project.py", PASS,
    "Collect-only in a scratch workspace (reference as market_maker.py): '37 tests collected' (scratch_checks_r5.out, collect-only in the reference workspace). "
    "Count: 8 tests x 2 seeds = 16 on both seeds; 20 on the learner seed plus 1 fixed-range test = 21. Matches the page's 37 / 16 / 21. "
    "The round-4 wording '35' is no longer on the page.")
row("proj-grader-seed-scope-claim", "2.6-spec", f"{P} line 395 (Integrity) and line 397 (Grading mode)", PASS,
    "Sixteen parametrised checks run on SEEDS = (SEED, SEED + 7919) (test_project.py line 33); the rest use SEED only; the last "
    "(test_fixed_seeds_0_to_49_give_fifty_different_paths, line 363) uses no learner seed. Matches line 397.")
row("proj-grader-no-print", "2.6-grader", f"{P} 'Constraints' line 395; {G}/test_project.py lines 334-338", PASS,
    "test_no_function_prints captures stdout over quote and replay. Grep for print( in grader/*.py returns 0 matches. "
    "Warnings are errors (pytestmark, line 30; -W error).")
row("proj-grader-replay-from-fills", "2.6-grader", f"{P} Conventions 'The P&L' line 407; {G}/test_project.py oracle lines 68-79", PASS,
    "oracle sums fill cash flows, takes the side from price == bid, and marks at settlement; it is written apart from reference.py. "
    "Matches line 407.")
row("proj-grader-mypy-strict", "2.6-grader", f"{G}/engine.py, instance.py, test_project.py, reference.py (run with market_maker = reference)", PASS,
    "mypy --strict --python-version 3.14 on the four files in a scratch workspace: 'Success: no issues found in 4 source files' "
    "(scratch_checks_r5.out; not in the repo gate). Note: the repo mypy config (pyproject.toml lines 27-31) checks tools and tests only, so "
    "the course grader is not in the repo gate.")
row("proj-grader-reference", "2.6-grader", f"{G}/reference.py", PASS,
    "run_graders.py --unit PC3 --seeds 0-49: 'run_graders PC3: PASS (reference 50/50 seeds, slowest 0.4 s)'. Also the page "
    "command with QF_SEED 0, 39893, 39901, 7919: 37 passed each (scratch_checks_r5.out).")
row("proj-grader-starter-fails", "2.6-grader", f"{G}/starter.py", PASS,
    "Starter run under the suite (scratch_checks_r5.out, QF_SEED=0): '20 failed, 17 passed'; the failures include test_no_function_prints "
    "(NotImplementedError). The suite fails on the starter.")
row("proj-grader-instances", "2.8-data", f"{G}/instance.py", PASS,
    "sample20_and_starter_r5.py: 20 seeds drawn by random.Random(20260311): all valid (21 positive ints from 10000, moves of 5, 20 "
    "arrivals from the three names); 20 distinct paths, 20 distinct arrival strings, 9 distinct settlements. "
    "Seeds 0-49: 50 distinct paths (collect_and_paths.py).")
row("proj-grader-messages", "2.6-grader", f"{G}/test_project.py lines 40-55 and throughout", PASS,
    "Messages name the property and carry no computed learner value (checked each expect/must_refuse string). The only values "
    "named are spec values (10000, 0..5, 20 turns) and the refusal phrases the page quotes.")
row("proj-named-refusals", "2.6-grader", f"{G}/test_project.py lines 166-217; {P} 'Named invalid inputs' lines 410-418", PASS,
    "Four named conditions each have a test (crossed/locked quote, size 6 and -1, log of 19 and 21 turns, filled with None price). "
    "Each message phrase matches engine.py lines 76 and 78 and the replay messages.")
row("proj-exception-types", "2.6-grader", f"{G}/test_project.py lines 47-55 and 168-218; {P} line 418", PASS,
    "must_refuse is used only for the four named conditions; line 418 says other invalid inputs may raise anything, and no test "
    "requires a type for other inputs.")
row("proj-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3 --page project", PASS,
    "ledgers/PC3/scripts/PC3-c-r5/run_labs_project.out: 'run_labs PC3: PASS (3/3)'.")
row("proj-check-tools", "2.9-structure", "tools/check_pages.py, check_dag.py, check_projects.py --unit PC3", PASS,
    "check_pages PC3: PASS; check_dag PC3: PASS; check_projects PC3: PASS (run_gates_r5.sh outputs).")
row("proj-page-smoke", "2.9-structure / 2.5-labs", "tools/page_smoke.py --unit PC3 --pages project", PASS,
    "page_smoke_project.out: 'in-browser grader: All 37 tests pass on seed 1104260787'; 'page_smoke modules/PC/PC3/project.html: PASS'.")
row("proj-lint-ruff", "2.9-structure", f"ruff check and ruff format --check on {G} and tests/labs/PC3", PASS,
    "ruff_check.out: 'All checks passed!'; ruff_format.out: '14 files already formatted'.")
row("proj-mypy-labs", "2.5-labs", "mypy --no-incremental (repo: tools, tests incl. tests/labs/PC3)", PASS,
    "mypy_repo.out: 'Success: no issues found in 385 source files'.")
row("proj-banned-and-process-words", "2.9-prose", f"{P} all text and code; tests/labs/PC3/lab-PC3-project-1..3.py", PASS,
    "Scanned for the BUILDER_RULES 1.3-1.4 phrases (TODO, TBD, lorem, for brevity, beyond the scope, it is important to note, "
    "obviously, clearly, studies show, experts agree, it is well known) and for ellipses: 0 hits. Process words (verifier, builder, "
    "ledger, round, fragment, audit, revised): 0 hits in learner text ('names no reviewer' is a statement about the page).")
row("proj-notation", "2.4-notation", f"{P} inline and display math (49 spans) vs notation/notation.json", PASS,
    "Symbols on the page: N (local to the module, defined at line 402), t, v_t, v_0, v_20, a_t, b_t, q_t, I, I_20, pnl. "
    "notation.json symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. No collision. Macros used "
    "(\\times, \\le, \\ge, \\gt, \\lt, \\dots, \\mathrm, \\cdot) are standard TeX, not registered macros.")
row("proj-dag-terms", "2.9-DAG / 2.9-terms", f"{P} whole text; L04.html def id def-market-making-game",
    PASS, "Only concept link: market-making-game (line 37, L04.html#def-market-making-game); L04.html defines it with "
    "id='def-market-making-game' data-concept='market-making-game'. 'Adverse selection' appears at lines 626 and 677 as plain prose "
    "(no link, no dfn), matching plan D3. The defect in the 'as defined in Lesson 4' pointer is row proj-rubric-c4-real-form-undefined.")
row("proj-references", "2.1-citations", f"{P} 'Reading' lines 710-717 and 'References' line 721", PASS,
    "data-cite keys zhou2008practical and crack2015heard exist in references/references.json (entries present). The page attributes "
    "no page, problem or edition. verify_refs --offline: 'offline integrity: 560 entries, 0 problems' (verify_refs.out).")
row("proj-js-claims", "2.9-prose", f"{P} line 442 (autograder saves code as you type), line 395 and footer line 730", PASS,
    "course/assets/js/grader.js: editor 'input' listener saves the draft (store.put, 400 ms debounce, lines 59-61); "
    "seed = store.unitSeed(unit), a hash of the workspace ID (store.js lines 135-143, grader.js line 53). No learner text is sent "
    "(only the suite and starter files are fetched).")
row("proj-local-commands", "2.6-grader", f"{P} line 393 (log command) and line 449 (local suite command)", PASS,
    "Log command run exactly as printed (venv python, no -I) in a scratch folder with the reference as market_maker.py: "
    "game_log.json written with keys seed, settlement_cents, turns (20 records). The pytest command with the page flags runs "
    "37 tests (scratch_checks_r5.out).")
row("proj-known-limitation", "2.6-prose", f"{P} line 395 'Known limitation'; {G}/engine.py docstring lines 1-20", PASS,
    "Line 395 says a student who reads instance.py can see the fair path, and the log shows only the settlement. "
    "instance.py is readable and engine.play never shows the fair value to the policy (engine.py lines 6-19). Consistent.")
row("proj-ladder-scope", "2.6-spec / curriculum scope", f"{P} lines 40-48; curriculum/06-profession-capstone.yaml lines 175-181", PASS,
    "Rung 1 worked example (Lab 1), Rung 2 completion (Lab 2, graded instantly), Rung 3 spec with grader and analysis, "
    "Rung 4 stretch. Curriculum brief says 'play the in-page game ... and analyse edge and inventory risk'. The page plays by "
    "code (Architect Q1 default, plan section 12, confirmed: no JavaScript game). Analysis covers edge (P&L) and inventory (mark, "
    "limit). Noted: 'inventory risk' is not named as such. Not failed.")
row("proj-rubric-atlas-studios", "2.6-atlas/studios", f"plans/PC3-build-plan.md section 12 Q16; {P} grep 'atlas'", PASS,
    "grep -c atlas project.html = 0; plan section 12 Q16: no Atlas contract for PC3 (section 8). Not a studio.")
row("proj-stretch", "2.6-spec", f"{P} lines 701-708 (Rung 4 stretch)", PASS,
    "Three extensions with explicit inputs (seeds 0 to 199, informed probability 0.6, limit 5). Each is runnable with the engine "
    "as written (engine.py takes the limit as a constant). Not graded (plan section 5.1).")
row("proj-twin-rules", "2.5-labs", "tests/labs/PC3/lab-PC3-project-1..3.py", PASS,
    "Each twin runs under python -I -W error with no stderr (labs_page_vs_twin_r5.out), seeded random.Random(0), standard library only, "
    "no network.")
row("proj-exception-types-labs", "2.5-labs", f"{P} Lab 1 and Lab 3 replay (raise ValueError lines)", PASS,
    "Lab 1 replay raises ValueError at page lines 166 and 173; Lab 3 at page lines 556 and 561. "
    "The page text does not claim these checks beyond their text.")
row("proj-r4-new-mutants-v18-v20", "2.6-mutation", "ledgers/PC3/mutants/v18, v19, v20", PASS,
    "mutate_all_r5.out: v18 KILLED by test_filled_turn_without_a_price_is_refused (seed 0); v19 and v20 KILLED by "
    "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0].")
row("proj-grader-window-distinct-paths", "2.8-grader / 2.2-numbers",
    f"{G}/test_project.py lines 363-367 and {P} line 397", PASS,
    "Round-4 FAIL resolved. The window test is now test_fixed_seeds_0_to_49_give_fifty_different_paths over fixed seeds 0..49, "
    "not the learner's seeds. collect_and_paths.py: 50 distinct paths, no identical pair. Reference passes with QF_SEED 39893 and 39901 "
    "(37 passed each, scratch_checks_r5.out). Page line 397 describes the same fixed-range check.")

# ---- new this round ----
row("proj-grader-v21-replay-scales-by-size", "2.6-mutation / 2.8-grader",
    f"{G}/test_project.py (no test replays a fill of size other than 1); {P} line 395 'A fill is one unit.'",
    FAIL,
    "NEW SURVIVOR. ledgers/PC3/mutants/v21_replay_scales_each_fill_by_quoted_size.py (quote sizes 1; replay multiplies each fill's "
    "cash and inventory by record['size']) passes all 37 tests on seed 0 (scratch_checks_r5.out, QF_SEED 0; mutate_all_r5.out: SURVIVED). "
    "Page line 395 states 'A fill is one unit.' and line 393 defines the replay in fills. survivor_demo_r5.out: a legal size-5 log "
    "(quote (9990,10010,5), seed 0) gives replay cash flow -449350 against the oracle -89870 No test "
    "replays a log whose records have size other than 1, so the stated one-unit rule is untested.",
    "Add a test that replays an engine log played with a size-5 quote (for example engine.play(lambda s: (9990, 10010, 5), SEED)) "
    "and compares replay to oracle(log), and add a hand-built filled record with size 3 to the replay tests. Both must name the "
    "one-unit rule in their docstring. Then re-run mutate_graders: v21 must be killed.")
row("proj-grader-v22-zero-fill-price-refused", "2.6-mutation / 2.8-grader",
    f"{G}/test_project.py (no test replays a filled turn with price 0); {P} line 416 (named refusal: price None)",
    FAIL,
    "NEW SURVIVOR. ledgers/PC3/mutants/v22_replay_refuses_a_zero_fill_price.py tests 'not price' and so refuses a fill at price 0. "
    "Page line 416 names the refusal for a price of None only, and line 395 allows bid of any value below ask. The engine produces "
    "such fills: engine.play(lambda s: (0, 9990, 1), 0) has fills at turns 2, 3, 4, 8, 19 with price 0 (survivor_demo_r5.out, "
    "reference oracle cash 59940, inventory -1). The mutant raises 'a filled turn needs a fill price' on that legal log. It "
    "passes all 37 tests (mutate_all_r5.out: SURVIVED; scratch_checks_r5.out: 37 passed under the page flags).",
    "Add a test with a hand-built or engine-played log that has a filled turn at price 0 (bid 0), and expect replay to equal "
    "oracle(log) with no exception. Keep the named refusal for None only, as line 416 states.")
row("proj-rubric-c4-real-form-undefined", "2.6-rubric / 2.9-terms",
    f"{P} line 626 (C4 level 4 descriptor) and line 677 (Exemplar B), against course/modules/PC/PC3/L04.html lines 158 and 465",
    FAIL,
    "Line 626 requires the level-4 passage to name 'adverse selection in its real form, as defined in Lesson 4'. Lesson 4 never "
    "defines a real form: L04.html line 158 says 'adverse selection ... in its simplest form here', and line 465 says 'Adverse "
    "selection is modelled in its simplest form'. The descriptor therefore cites a definition that is absent, so a learner "
    "cannot meet it by reading the pointer. Line 677 repeats 'adverse selection in its real form' without a definition.",
    "Replace 'adverse selection in its real form, as defined in Lesson 4' with the wording the page can support, for example "
    "'adverse selection beyond the simplest form in Lesson 4 (the informed-trader cost; the order-book queue and the price impact "
    "are left out)', in both line 626 and line 677. Lesson 4 line 465 supports the queue point.")
row("proj-plan-file-names", "2.6-spec / plan conformance",
    f"{P} lines 393, 443, 448 and {G}/test_project.py line 26 against plans/PC3-build-plan.md lines 337-341 and 575-579 (Q1)",
    FAIL,
    "Plan section 5.2 (binding, Architect decisions block) requires two modules: policy.py with quote and pnl.py with replay "
    "(plan lines 337 and 340), and Q1 (lines 577-579) recommends a Pyodide engine played by code with policy.py, pnl.py, "
    "game_log.json and analysis.md. The project page, starter, reference and test_project.py use one module, market_maker.py "
    "(project.html line 393; test_project.py line 26 'import market_maker as sol'). No architect ruling in plans/FINAL-ARCHITECT-"
    "RULINGS.md or the PC3 plan changes the names (grep: no PC3 or market_maker entry). The hub also uses the plan's names, so "
    "the unit disagrees with itself (see proj-hub-filenames).",
    "Either rename to policy.py (quote) and pnl.py (replay) in project.html, starter.py, reference.py, test_project.py and the "
    "engine.py docstring, or obtain and record an architect ruling in plans/PC3-build-plan.md that market_maker.py replaces the two "
    "modules. Then align index.html lines 160 and 167 to whichever name is chosen.")
row("proj-exemplar-levels-vs-plan", "2.6-rubric / plan conformance",
    f"{P} lines 635 and 665 (data-level 2 and 4) vs plans/PC3-build-plan.md line 380 (exemplar-a data-level 4, exemplar-b data-level 2)",
    PASS,
    "The page's data-level values match each exemplar's own official scoring (A: 2,2,1,2,1; B: 4,4,4,3,4) and both calibrate by "
    "blind scoring (rows proj-exemplar-a/b-calibration). The plan text at line 380 labels them the other way round. This is "
    "the plan's labelling, not a page defect; the architect should confirm the labels. Not failed.")
row("proj-instance-engine-names", "2.6-spec / plan conformance",
    f"{G}/engine.py lines 49-58 and {G}/instance.py lines 30-31 vs plans/PC3-build-plan.md lines 357-359 and 405-406",
    PASS,
    "The plan lists four arrival names (including 'none', plan lines 359 and 405-406) and play(policy_module, seed) (line 357). The page and code use three arrival names "
    "(one arrival per turn, Lesson 4 A1) and play(quote, seed) with a quote function. Both are consistent with Lesson 4 and with "
    "every test; the 'none' name is not needed under A1. Noted for the architect, not failed.")
row("proj-r5-mutant-v23-first-fill-price", "2.6-mutation", "ledgers/PC3/mutants/v23_replay_marks_at_the_first_fill_price.py", PASS,
    "mutate_all_r5.out: KILLED by test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0).")
row("proj-r5-alternatives-14-16", "2.6-alternatives", "ledgers/PC3/scripts/PC3-c-r5/alts/alt14, alt15, alt16", PASS,
    "run_alts_r5.py (alts_all_r5.out): each of the three new correct pairs passes 50/50 seeds (reduce replay; asymmetric inventory "
    "skew with size 2 or 1; size 0 then 5 with a 9-below, 11-above quote).")
row("proj-r5-labs-page-vs-twin", "2.5-labs", f"{P} lab-PC3-project-1..3 code and expected blocks",
    PASS, "labs_page_vs_twin_r5.out: page code equals twin on lab 1 and 3 (0 differing lines); lab 2 differs in the two blank lines "
    "only; every twin output equals its expected block.")

# ---- mutants ----
mutants = []
for line in (S / "mutate_all_r5.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+)\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    killed_by = None if killed.strip() == "None" else killed.strip()
    mutants.append({"id": name, "description": desc, "killed_by": killed_by, "file": f"ledgers/PC3/mutants/{name}.py"})

fragment = {
    "unit": "PC3",
    "slice": "c",
    "round": 5,
    "verifier": "independent verifier (Haiku 5.5), round 5, slice c (did not build PC3)",
    "pin": "7376a5e",
    "base": "round 4 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round4.json (pin 9a02b1af). Delta 9a02b1af..7376a5e for slice c: project.html (lines 386-730: spec, grading mode, rubric C4, exemplar B assumptions, footer), grader/test_project.py (window test replaced by fixed seeds 0-49), mutants v18-v20 and alt6 (moved from mutants/v17), index.html (hub lines 34, 48, 71-74, not slice c, re-verified only for the cited lines), L01-L06 and cards.json (slices a, b, d; not read here).",
    "checkout": str(ROOT),
    "scratch": "/tmp/pc3c-r5-ws (ref/, starter/, v21/, v22/ grader workspaces; indep numbers and survivor demos written into ledgers/PC3/scripts/PC3-c-r5)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Full reads this round: project.html (732 lines), grader engine.py, instance.py, reference.py, starter.py, test_project.py (418 lines), the three project lab twins, the diff of every PC3 file changed since 9a02b1af, all 32 mutant files (run through mutate_graders), all 16 alternative files (run through run_alts_r5.py on seeds 0-49).",
        "Gate commands run once on the pin (scripts/PC3-c-r5/run_gates_r5.sh): check_pages, check_dag, check_projects, run_labs (project), run_graders 0-49 (PASS 50/50), mutate_graders 0-49 (30/32 killed, the two survivors are the FAIL rows), page_smoke (project), ruff check and format, mypy --no-incremental, verify_refs --offline, pytest -k PC3. collect_only failed in the grader directory because market_maker is absent there; the count was taken in a scratch workspace (37).",
        "Round-4 FAIL row proj-grader-window-distinct-paths is resolved (PASS). Round-4 hub rows proj-hub-filenames, proj-hub-seed-scope and proj-hub-skill-check-premise still hold (index.html lines 55, 129, 134, 160, 167 unchanged) and stay FAIL. They are outside slice c and are listed so that the unit ledger carries them.",
        "Architect decisions (binding) checked: ten student-error mutants (32 files, 30 killed, 2 new survivors listed) and five alternative correct implementations (16 files, all pass) are met; no question bank required (page has none; plan Q15 and Q6); tier U, so rungs 1-2 are full length and not minimal.",
        "Rubric note (not failed): C2 level 3 accepts a cited value that does not match the log, while level 3 is the bar. The rubric is observable as written, so it is a design comment for the builder.",
        "Scope notes (not failed): Rung 4 stretch items are specified tasks (plan 5.1 item 4 specifies them). The curriculum brief says 'in-page game' and 'inventory risk'; the plan's Q1 default (play by code) was confirmed, and the analysis covers edge and inventory through C1 and C4.",
        "Not checked: the full repo gate (render_curriculum, build_site --check, fetch_data --check, check_pages --all, run_graders over all units, full pytest suite); index.html beyond the cited lines; L01-L06 and cards.json (slices a, b, d); the in-browser Pyodide run beyond page_smoke's own in-browser step; learner seeds outside the sampled 20 (exhaustive window check not needed now that the window test uses fixed seeds 0-49); the grader.js rendering in a real browser (only the source was read); the rubric's C5 wording 'without a value' was read as 'result named without its number', which the page can support.",
    ],
    "summary": "",
}
n_fail = sum(1 for r in rows if r["status"] != "PASS")
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
killed = sum(1 for m in mutants if m["killed_by"])
fragment["summary"] = (
    f"Slice c round 5 at pin 7376a5e: verdict FAIL. Rows {len(rows)}: PASS {counts['PASS']}, FAIL {counts['FAIL']}, "
    f"UNVERIFIABLE {counts['UNVERIFIABLE']}. FAIL: proj-grader-v21-replay-scales-by-size and proj-grader-v22-zero-fill-price-refused "
    "(two new surviving grader mutants; the suite never replays a size other than 1 or a price of 0), "
    "proj-rubric-c4-real-form-undefined (rubric cites 'adverse selection in its real form, as defined in Lesson 4', which Lesson 4 does not define), "
    "proj-plan-file-names (page and grader use market_maker.py; binding plan names policy.py and pnl.py), and the three round-4 hub rows "
    "(proj-hub-filenames, proj-hub-seed-scope, proj-hub-skill-check-premise; outside slice c, still true). Round-4 FAIL "
    f"proj-grader-window-distinct-paths is PASS now. Mutants {killed}/{len(mutants)} killed (v21 and v22 survive). Alternatives: 16 of 16 pass seeds 0-49. "
    "Gates PASS: check_pages, check_dag, check_projects, run_labs 3/3, run_graders 50/50, page_smoke, ruff, mypy, verify_refs, pytest -k PC3; collect 37."
)
out = ROOT / "ledgers/PC3/PC3-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
problems = ledger.validate(fragment, "PC3-c")
print("written", out, "rows", len(rows), "mutants", len(mutants), "validate:", problems)
