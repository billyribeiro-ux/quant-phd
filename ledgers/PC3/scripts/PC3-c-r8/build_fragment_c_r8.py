"""Round 8 verifier: build ledgers/PC3/PC3-c.json from the outputs of this round (no values typed in by hand
except the row text). Run with the checkout's .venv/bin/python from the checkout root."""

import json
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE8-PC3-c"
S = f"{ROOT}/ledgers/PC3/scripts/PC3-c-r8"
PIN = "0dee921a"
R7 = "round 7 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round7.json (pin 06994db)"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- rounds 7 FAIL rows, re-verified this round -------------------------------------------------------------
row("proj-zero-fill-replay", "2.6-grader (mutation survivor; stated behaviour of replay)",
    "course/modules/PC/PC3/grader/test_project.py lines 314-322 (new test_a_log_with_no_fill_replays_to_zero); "
    "project.html line 393 (replay returns the four keys)", "PASS",
    "Re-verified r8: the new test is present at the pin. Observed in ledgers/PC3/scripts/PC3-c-r8/r8v_mutate_default_0-9.out: "
    "'KILLED v27_replay_divides_by_the_number_of_fills.py ... -> test_a_log_with_no_fill_replays_to_zero (seed 0)'. "
    "Collect-only and reference runs (ledgers/PC3/scripts/PC3-c-r8/r8v_collect_r8.out) all pass.")
row("proj-rubric-observable", "2.6-rubric (every level descriptor observable)",
    "course/modules/PC/PC3/project.html line 627 (C5 level 3 'as a word (it holds or it fails), with no number' "
    "against level 4 'the number that the check computed or printed')", "PASS",
    "Re-read at the pin: level 3 now names a result as a word with no number; level 4 requires the number computed "
    "or printed (example 30 = -9950 + 1 x 9980). A check printing True falls to level 3, a check with a computed "
    "number to level 4. Ladder is observable for a boolean check.")
row("proj-rubric-ladder-gap-c1", "2.6-rubric (ladder covers every submission)",
    "course/modules/PC/PC3/project.html line 623 (C1 level 2)", "PASS",
    "Round-7 case re-checked: a submission that states cash_flow_cents, inventory_mark_cents and pnl_cents, each "
    "equal to replay, and names no turns now meets level 2 ('states the P&amp;L and at least one component, each "
    "equal to the output of replay'). The round-8 residual gap (components without a P&L total) is row "
    "proj-rubric-ladder-gap-c1-no-pnl.")
row("proj-rubric-ladder-gap-c1-no-pnl", "2.6-rubric (ladder covers every submission)",
    "course/modules/PC/PC3/project.html line 623 (C1 levels 1-3)", "FAIL",
    "A submission that states cash_flow_cents = -9950 and inventory_mark_cents = 9980 (each equal to replay on seed 0), "
    "states no P&L, and names no turns: level 3 needs 'the three values'; level 2 needs 'the P&amp;L and at least one "
    "component'; level 1 needs 'a result without its components' (no result is stated) or 'a value that replay does "
    "not return' (both values are returned by replay). No level matches.",
    "Level 2 (or level 1): 'states two or more of cash_flow_cents, inventory_mark_cents and pnl_cents, each equal to "
    "the output of replay'; keep level 2 as is for the P&amp;L with a component.")
row("proj-rubric-ladder-gap-c2", "2.6-rubric (ladder covers every submission)",
    "course/modules/PC/PC3/project.html line 624 (C2 levels 1-4)", "FAIL",
    "A submission that cites three turns by number only ('turns 2, 5 and 18 are fills') meets no level: level 4 and "
    "level 3 need 'by number and field' with values, level 2 needs 'one turn by number and field, with its value', or "
    "a value that does not match, and level 1 needs 'no turn cited'. The same holds for one turn cited with its field "
    "but no value ('turn 5, ask_cents').",
    "Level 2: 'cites one or more turns by number, each with at least one field and its value from the log, and every "
    "cited value matches the log' (level 1 stays 'no turn cited').")
row("proj-rubric-ladder-gap-c3", "2.6-rubric (ladder covers every submission)",
    "course/modules/PC/PC3/project.html line 625 (C3 level 2)", "PASS",
    "Round-7 case re-checked: a submission that states one change with its amount in cents and reruns the same seed, "
    "without the P&amp;L of either run, now meets level 2 ('either gives no rerun or reruns the same seed without the "
    "P&amp;L of either run'). The round-8 residual gap is row proj-rubric-ladder-gap-c3-one-run.")
row("proj-rubric-ladder-gap-c3-one-run", "2.6-rubric (ladder covers every submission)",
    "course/modules/PC/PC3/project.html line 625 (C3 levels 2-4)", "FAIL",
    "A submission that states the change (10 to 15 cents), reruns seed 0 and gives only the P&amp;L of the rerun (55 "
    "cents), with neither the baseline P&amp;L nor the difference: level 4 needs 'reports the change in pnl_cents'; "
    "level 3 needs 'the P&amp;L of both runs'; level 2 needs 'without the P&amp;L of either run', which this "
    "submission violates; level 1 needs no amount. No level matches.",
    "Level 2: 'states one change with its amount in cents, and either gives no rerun, or reruns the same seed and gives "
    "the P&amp;L of at most one run without the difference'.")
row("proj-grader-35-checks", "2.6-spec (count claim equals real collect-only count)",
    "course/modules/PC/PC3/project.html line 397; grader/test_project.py", "PASS",
    "Re-verified r8 (ledgers/PC3/scripts/PC3-c-r8/r8v_collect_r8.out): QF_SEED 0, 1, 7, 49 -> '433 tests collected' and 433 passed; QF_SEED 50, "
    "848197495, 1712259056 -> '441 tests collected' and 441 passed. Arithmetic: 8 x 51 + 24 + 1 = 433; "
    "8 x 52 + 24 + 1 = 441. The 24 on-seed tests were counted by reading test_project.py (lines 143-422). The page "
    "sentences (line 397) match.")
row("proj-starter-docstring-raise-scope", "2.6-spec (wording matches the named-invalid-input contract)",
    "course/modules/PC/PC3/grader/starter.py lines 8-9; project.html lines 411-418", "PASS",
    "starter.py lines 8-9 now read: 'Every input to replay that the specification names as invalid must raise "
    "ValueError; the engine refuses an illegal quote.' This matches project.html lines 411-418 (two engine refusals, "
    "two replay refusals) and line 418 (other invalid inputs unconstrained).")
row("proj-plan-file-names", "2.6-spec (file contract matches the plan)",
    "plans/PC3-build-plan.md lines 67-69, 317-318, 337, 340, 348; course/modules/PC/PC3/project.html lines 46 and 393; "
    "grader/test_project.py line 29", "FAIL",
    "The binding plan names policy.py (quote) and pnl.py (replay) and dual-mode grading on policy.py and pnl.py (plan "
    "lines 317, 337, 340, 348). The page (project.html lines 46, 393) and the grader (test_project.py line 29: "
    "'import market_maker as sol') use one file, market_maker.py. grep 'market_maker' over plans/ finds nothing, so no "
    "architect decision records the rename.",
    "Architect decision: either amend the plan (sections 1, 5.3, 6) to market_maker.py and record the decision, or "
    "rename the module on the page, in the grader, starter, reference and twins to policy.py and pnl.py.")
row("proj-hub-filenames", "2.4-structure (hub and project name the same files)",
    "course/modules/PC/PC3/index.html lines 160 and 167", "PASS",
    "index.html line 160 and 167 name market_maker.py. grep for 'policy.py' and 'pnl.py' under course/modules/PC/PC3/ "
    "returns nothing at the pin. (Cross-slice: index.html is not in slice c; the check is recorded for the hub owner.)")
row("proj-hub-skill-check-premise", "2.2-numbers (hub skill-check premise is consistent with the game)",
    "course/modules/PC/PC3/index.html line 129 against project.html line 406 (a purchase at the bid changes cash by "
    "-b)", "PASS",
    "index.html line 129 now reads 'a market maker buys one unit at a bid of 10 005 cents', and the cash flow asked "
    "for is -10005 under the conventions (project.html line 406). Consistent. (Cross-slice, recorded for the hub owner.)")
row("proj-exemplar-a-numbers", "2.2-numbers",
    "course/modules/PC/PC3/project.html lines 635-662 (exemplar A)", "PASS",
    "Independent re-derivation (ledgers/PC3/scripts/PC3-c-r8/r8v_indep_numbers.out): purchases at the bid on turns 2, 3, 4, 8, 19 total 49910; "
    "sales at the ask on turns 5, 7, 13, 18 total 39960; 39960 - 49910 = -9950; inventory after turn 19 = 1; mark "
    "1 x 9980 = 9980; P&amp;L 30; turn 5 inventory after = 2; turn 18 inventory after = 0. All match exemplar A.")
row("proj-lab1-replay-prints", "2.5-labs",
    "course/modules/PC/PC3/project.html lab-PC3-project-1 (lines 55-240) against tests/labs/PC3/lab-PC3-project-1.py",
    "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_twin_vs_page.py: page code equals twin except one trailing newline (the page block has none). Twin run "
    "alone with python -I -W error: exit 0, empty stderr; output equals the expected block (diff: final newline only). "
    "The interpretation line (239) describes the printed per-fill line and the identity line correctly.")
row("proj-lab1-run", "2.5-labs", "course/modules/PC/PC3/project.html lab-PC3-project-1; tools/run_labs.py",
    "PASS", "ledgers/PC3/scripts/PC3-c-r8/r8v_run_labs_project.out: 'run_labs PC3: PASS (3/3)', exit 0.")
row("proj-lab1-hypothesis-numbers", "2.2-numbers",
    "course/modules/PC/PC3/project.html line 57 (Lab 1 hypothesis)", "PASS",
    "9 fills in 20 turns, cash flow -9950, inventory 1, settlement 9980, mark 9980, P&amp;L 30, identity holds, largest "
    "|inventory| 3 under limit 10: all equal the independent re-derivation (ledgers/PC3/scripts/PC3-c-r8/r8v_indep_numbers.out).")
row("proj-lab2-completion", "2.5-labs", "course/modules/PC/PC3/project.html lab-PC3-project-2 (lines 242-380)",
    "PASS", "Page code equals twin except the two blanks at lines 349-350 (cash_flow = ___, mark = ___) (twin_vs_page "
    "diff). Twin under python -I -W error prints the expected block (exit 0). Run_labs 3/3.")
row("proj-lab2-interpretation-last-quote", "2.2-numbers",
    "course/modules/PC/PC3/project.html line 381 (Lab 2 interpretation)", "PASS",
    "'With an inventory of 1 unit, a mark at any price other than 9980 changes the P&amp;L': P&amp;L = cash flow + 1 x "
    "mark, so a different mark changes the P&amp;L by the same amount. Direction and size are correct.")
row("proj-lab3-counterfactual", "2.2-numbers", "course/modules/PC/PC3/project.html lines 457-612 (Lab 3)",
    "PASS", "Independent re-derivation: half-spread 15 gives 9 fills, P&amp;L 55, change +25 (ledgers/PC3/scripts/PC3-c-r8/r8v_indep_numbers.out). "
    "Twin under python -I -W error matches the expected block (lines 600-610).")
row("proj-lab3-interpretation", "2.2-numbers",
    "course/modules/PC/PC3/project.html line 611 (Lab 3 interpretation)", "PASS",
    "'The last three lines are the counterfactual' (lines 608-610 of the expected block) and 'the first block' (lines "
    "601-607, seven lines including the settlement line). Both descriptions match the printed output.")
row("proj-rung1-instance-claim", "2.8-data / 2.6-spec",
    "course/modules/PC/PC3/project.html line 391; grader/instance.py lines 27-53", "PASS",
    "make_instance returns a 21-value path from 10000 and 20 arrivals (instance.py lines 27-53); the draw order (move "
    "then arrival, thresholds 0.5, 0.25, 0.5) matches Lab 1 and the seed-0 game in the independent script.")
row("proj-conventions-constants", "2.2-numbers",
    "course/modules/PC/PC3/project.html lines 402-407 (Conventions) and line 393", "PASS",
    "Constants 10000, +/-5, 1/4, 1/4, 1/2, size 0..5, limit 10 match instance.py and engine.py (MAX_SIZE 5, LIMIT 10). "
    "Cash moves: purchase at the bid -b, sale at the ask +a (engine.py lines 84-86).")
row("proj-exemplar-a-calibration", "2.6-rubric (blind calibration)",
    "course/modules/PC/PC3/project.html lines 635-662 against rubric lines 623-627", "PASS",
    "Scored from the passage and the rubric: C1 4, C2 4, C3 4, C4 3, C5 4 (equal to data-scores 4,4,4,3,4). Caveat: "
    "the official-scoring line (line 637) and the annotations were in the same Read output, so this is not a strictly "
    "blind pass; the agreement is recorded as observed.")
row("proj-exemplar-b-calibration", "2.6-rubric (blind calibration)",
    "course/modules/PC/PC3/project.html lines 664-692 against rubric lines 623-627", "PASS",
    "Scored from the passage and the rubric: C1 2, C2 2, C3 1, C4 2, C5 1 (equal to data-scores 2,2,1,2,1). Same caveat "
    "on blindness as exemplar A.")
row("proj-exemplar-b-numbers", "2.2-numbers", "course/modules/PC/PC3/project.html lines 664-690 (exemplar B)",
    "PASS", "P&amp;L 30 and cash flow -9950 (Lab 1 output); turn 5 sold at the ask 9980 (Lab 1 line 225). Correct.")
row("proj-exemplar-b-arrival-sensitivity", "2.2-numbers",
    "course/modules/PC/PC3/project.html line 687 (annotation) and line 676", "PASS",
    "The annotation 'names the arrival probabilities without saying which result depends on them' is accurate; "
    "exemplar B states the probabilities as the model's choices and names no effect.")
row("proj-rubric-c2-level3-admits-mismatch", "2.6-rubric",
    "course/modules/PC/PC3/project.html line 624 (C2 levels 2 and 3)", "PASS",
    "Level 2 admits a turn whose cited value does not match the log, and level 3 requires every cited value to match. "
    "Consistent. (The turn-citation gap at levels 1-2 is row proj-rubric-ladder-gap-c2.)")
row("proj-rubric-c4-real-form-undefined", "2.6-rubric / 2.14-DAG",
    "course/modules/PC/PC3/project.html line 626 (C4 level 4) against course/modules/PC/PC3/L04.html line 466", "PASS",
    "L04 line 466 sets aside the queue of resting orders and a learning trader ('this lesson does not model learning'). "
    "C4 level 4 names exactly those two items. Consistent.")
row("proj-spec-log-schema", "2.6-spec",
    "course/modules/PC/PC3/project.html line 393 against grader/engine.py lines 89-98", "PASS",
    "The ten record keys and the three log keys named on the page are exactly those engine.play writes (engine.py "
    "lines 89-98 and 100). Confirmed by the documented game_log command (run in a scratch dir: log has keys seed, "
    "settlement_cents, turns; 20 records with the nine record keys plus turn).")
row("proj-hours-arithmetic", "2.9-hours",
    "course/modules/PC/PC3/project.html lines 422-434 (time budget); index.html line 167", "PASS",
    "1 + 1 + 3 + 2 + 2 + 4 + 1 = 14 (project.html data-hours-project=14, line 33). 14 / 50 = 28.0 %; index.html line "
    "167 states the same split and the 36 + 14 = 50 total.")
row("proj-hub-placement-conflict", "2.4-structure",
    "course/modules/PC/PC3/project.html lines 42-48 against course/modules/PC/PC3/index.html line 156", "PASS",
    "Both describe the same skip rule: rungs 1 and 2 are skipped only by a placement bar plus both skill checks.")
row("proj-hub-seed-scope", "2.6-spec",
    "course/modules/PC/PC3/index.html lines 55 and 160 against project.html line 397 and grader/test_project.py lines "
    "36-37", "PASS", "index.html line 160 lists seeds 0 to 49, the workspace seed and seed plus 7919, matching "
    "test_project.py lines 36-37 (FIXED_SEEDS = range(50), SEEDS adds SEED and SEED + 7919).")
row("proj-quote-rule-first-fill-survivor", "2.7-alternatives",
    "course/modules/PC/PC3/project.html line 429; ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py", "PASS",
    "alt6 is a legal quote (mid from the first fill), passes 52 of 52 seeds in r8 (ledgers/PC3/scripts/PC3-c-r8/r8v_older_alts.out).")
row("proj-builder-mutants", "2.6-mutants", "ledgers/PC3/mutants/m01..m10", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_mutate_default_0-9.out: all ten builder mutants KILLED (m01-m10).")
row("proj-verifier-mutants", "2.6-mutants", "ledgers/PC3/mutants/v01..v26", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_mutate_default_0-9.out: v01-v26 all KILLED.")
row("proj-mutant-m08-description", "2.6-mutants", "ledgers/PC3/mutants/m08_hard_coded_answer_for_any_log.py line 1",
    "PASS", "Mutate output: 'KILLED m08_hard_coded_answer_for_any_log.py: Student error: replay returns all zeros, a "
    "hard-coded answer, for every log. -> test_replay_agrees_with_the_engine_final_cash_and_inventory[34] (seed 0)'. "
    "The description matches the file's first docstring line.")
row("proj-verifier-mutants-r3-new", "2.6-mutants", "ledgers/PC3/mutants/v13..v16", "PASS",
    "All four KILLED in ledgers/PC3/scripts/PC3-c-r8/r8v_mutate_default_0-9.out.")
row("proj-alternatives-1-2-4-5", "2.7-alternatives", "ledgers/PC3/alternatives/alt1, alt2, alt4, alt5", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_older_alts.out: 0 of 52 seeds fail for each.")
row("proj-alt3-replay", "2.7-alternatives", "ledgers/PC3/alternatives/alt3_inventory_skew.py", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_older_alts.out: 0 of 52 seeds fail.")
row("proj-alternative-6", "2.7-alternatives", "ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_older_alts.out: 0 of 52 seeds fail.")
row("proj-alternative-7-8-verifier", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r2/alt7, alt8", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_older_alts.out: 0 of 52 seeds fail for alt7 and alt8.")
row("proj-alternative-9-10-verifier-r3", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r3/alt9, alt10", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_older_alts.out: 0 of 52 seeds fail for alt9 and alt10.")
row("proj-alternatives-r4-new", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r4/alts/alt11, alt12, alt13", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_older_alts.out: 0 of 52 seeds fail for alt11-13.")
row("proj-alternatives-r7-new", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r7/alts/alt20..alt24", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_older_alts.out: 0 of 52 seeds fail for alt20-24.")
row("proj-r8-alternatives-new", "2.7-alternatives",
    "ledgers/PC3/scripts/PC3-c-r8/alts/alt_r8_a..e (written this round)", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_alts_alt_r8.out: five new correct implementations (asymmetric 3/7 quote; size-0 never trades; bid 1 / ask "
    "20000 size 5 with fold replay; half-spread 1 with parity size; mid from last turn midpoint) each pass 53 of 53 "
    "seeds (0-49, 50, 848197495, 1712259056).")
row("proj-grader-seed-scope-claim", "2.6-spec",
    "project.html line 397 against grader/test_project.py lines 36-37", "PASS",
    "Membership of the seed sets is as stated (51 or 52 distinct seeds), confirmed by the collect counts.")
row("proj-grader-no-print", "2.6-spec (no print or warning on quote or replay)",
    "course/modules/PC/PC3/grader/test_project.py lines 389-400 (plays SEED only) and 314-322 (no-fill replay, no "
    "capture); project.html line 395 ('Neither quote nor replay prints or warns') and line 397 (check runs on your "
    "seed); ledgers/PC3/mutants/v33_replay_prints_only_for_a_log_with_no_fill.py and "
    "v34_quote_prints_only_when_inventory_reaches_five.py", "FAIL",
    "v33 SURVIVED: mutate_graders --unit PC3 --seeds 0-9 prints 'SURVIVED v33_... -> None'; QF_SEED=0 gives 433 "
    "passed; the mutant prints 'debug: no fill in this log' on a no-fill replay, which no test captures. v34 "
    "SURVIVES at QF_SEED 0-7 and 9 (433 passed) and is killed only at QF_SEED=8 (1 failed) (ledgers/PC3/scripts/PC3-c-r8/r8v_print_mutants_per_seed.out). "
    "The page states the no-print rule without a seed qualifier (line 395).",
    "Run the capsys/caplog/warnings check on every seed in SEEDS, and wrap the replay of the hand-built logs (the "
    "no-fill log at least) in capsys; then re-run mutate_graders --unit PC3 --seeds 0-9 and confirm v33 and v34 are "
    "killed on seed 0.")
row("proj-grader-determinism-quote-state", "2.6-spec (quote sees the state listed under Required outputs)",
    "project.html line 403 ('The quote sees the state listed under Required outputs') and line 393; "
    "grader/test_project.py (no determinism test); ledgers/PC3/mutants/v32_quote_keeps_last_fill_in_a_module_global.py",
    "FAIL",
    "v32 SURVIVED mutate_graders 0-9. Demonstration (ledgers/PC3/scripts/PC3-c-r8/r8v_demo_v32.sh output): in one process, after a game on seed 7, "
    "the seed-0 turn-1 quote is (10010, 10030, 1); in a fresh process it is (9990, 10010, 1). The full suite passes "
    "for the mutant: QF_SEED=0 433 passed, QF_SEED=7 433 passed, QF_SEED=1712259056 441 passed. The suite never plays "
    "the same seed twice, so a log that depends on earlier games is not detected.",
    "Add a test that plays the student's quote on SEED twice (and once after another seed) and requires identical logs; "
    "or state in project.html that the quote is a function of its state alone and test it. Then confirm v32 is KILLED "
    "by mutate_graders --unit PC3 --seeds 0-9.")
row("proj-js-claims", "2.6-grader / 2.4-prose",
    "course/modules/PC/PC3/project.html line 442 against course/assets/js/grader.js lines 56-61", "PASS",
    "grader.js editor 'input' listener debounces store.put('files', draftKey, ...) (400 ms), matching 'saved in this "
    "browser as you type'. The seed text 'derived from your workspace ID' matches grader.js line 53 and store.js line 134.")
row("proj-local-commands", "2.6-grader",
    "course/modules/PC/PC3/project.html lines 446-455 and line 393", "PASS",
    "The documented game_log command, run in a scratch directory with reference.py as market_maker.py without -I, "
    "writes valid JSON with keys seed, settlement_cents, turns. The pytest line with --assert=plain -W error is the "
    "one the grader runs; the suite uses no assert statement (grep: none outside docstrings).")
row("proj-known-limitation", "2.6-spec", "course/modules/PC/PC3/project.html line 395", "PASS",
    "The instance file is readable (grader/instance.py) and the log holds only the settlement value, as stated.")
row("proj-ladder-scope", "2.6-spec", "course/modules/PC/PC3/project.html lines 40-50", "PASS",
    "Ladder rungs 1-4 match the sections below them (labs 1-3, spec, analysis, stretch).")
row("proj-rubric-atlas-studios", "2.6-atlas/studio",
    "course/modules/PC/PC3/project.html (whole page) and plans/PC3-build-plan.md", "PASS",
    "grep of project.html for Atlas or studio terms: none.")
row("proj-stretch", "2.6-spec", "course/modules/PC/PC3/project.html lines 702-710", "PASS",
    "Stretch items are open-ended and name no result, so no claim to check.")
row("proj-twin-rules", "2.5-labs", "tests/labs/PC3/lab-PC3-project-1..3.py", "PASS",
    "Each twin runs alone under python -I -W error with exit 0 and empty stderr (ledgers/PC3/scripts/PC3-c-r8/r8v_* and tmp run).")
row("proj-exception-types-labs", "2.5-labs", "tests/labs/PC3/lab-PC3-project-1..3.py", "PASS",
    "The twins raise no exception and use no refusal path.")
row("proj-r4-new-mutants-v18-v20", "2.6-mutants", "ledgers/PC3/mutants/v18..v20", "PASS",
    "All three KILLED in ledgers/PC3/scripts/PC3-c-r8/r8v_mutate_default_0-9.out.")
row("proj-grader-window-distinct-paths", "2.6-grader",
    "course/modules/PC/PC3/grader/test_project.py lines 425-429", "PASS",
    "test_fixed_seeds_0_to_49_give_fifty_different_paths passes at every QF_SEED checked (433/441 passed).")
row("proj-grader-v21-replay-scales-by-size", "2.6-mutants", "ledgers/PC3/mutants/v21", "PASS",
    "KILLED by test_a_fill_is_one_unit_whatever_its_quoted_size (ledgers/PC3/scripts/PC3-c-r8/r8v_mutate_default_0-9.out).")
row("proj-grader-v22-zero-fill-price-refused", "2.6-mutants", "ledgers/PC3/mutants/v22", "PASS",
    "KILLED by test_a_fill_at_price_zero_is_a_legal_fill (ledgers/PC3/scripts/PC3-c-r8/r8v_mutate_default_0-9.out).")
row("proj-exemplar-levels-vs-plan", "2.6-rubric / plan",
    "course/modules/PC/PC3/project.html lines 635 and 664; plans/PC3-build-plan.md line 380", "PASS",
    "data-level 4 for exemplar A and 2 for exemplar B, as the plan requires.")
row("proj-instance-engine-names", "2.6-spec",
    "grader/instance.py make_instance (line 27); grader/engine.py play(quote, seed) (line 49)", "PASS",
    "Names used on the page match the signatures.")
row("proj-r5-mutant-v23-first-fill-price", "2.6-mutants", "ledgers/PC3/mutants/v23", "PASS",
    "KILLED by test_pnl_is_cash_flow_plus_inventory_times_settlement[26] (ledgers/PC3/scripts/PC3-c-r8/r8v_mutate_default_0-9.out).")
row("proj-r5-alternatives-14-16", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r5/alts/alt14, alt15, alt16",
    "PASS", "ledgers/PC3/scripts/PC3-c-r8/r8v_older_alts.out: 0 of 52 seeds fail for each.")
row("proj-r5-labs-page-vs-twin", "2.5-labs", "project labs page code vs twin", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_twin_vs_page.py: identical apart from the trailing newline and the two blanks in Lab 2.")
row("proj-grader-v24-stderr-print-survives", "2.6-mutants", "ledgers/PC3/mutants/v24", "PASS",
    "KILLED by test_no_function_prints_or_warns (seed 0) in r8.")
row("proj-grader-v25-last-filled-totals-survives", "2.6-mutants", "ledgers/PC3/mutants/v25", "PASS",
    "KILLED by test_stale_totals_on_the_last_filled_turn_are_not_used (seed 0) in r8.")
row("proj-grader-v26-logging-warning-survives", "2.6-mutants", "ledgers/PC3/mutants/v26", "PASS",
    "KILLED by test_no_function_prints_or_warns (seed 0) in r8.")
row("proj-plan-grader-seed-scope", "2.6-spec", "plans/PC3-build-plan.md lines 348 and 380",
    "PASS", "Plan lines 348 and 380 describe dual-mode grading on seeds 0 to 49 (with the file-name point recorded in "
    "proj-plan-file-names); test_project.py lines 36-37 match the seed scope.")
row("proj-verifier-mutants-r7-new", "2.6-mutants", "ledgers/PC3/mutants/v27..v30", "PASS",
    "Round-7 survivor v27 is now KILLED by test_a_log_with_no_fill_replays_to_zero (seed 0); v28, v29, v30 KILLED "
    "(ledgers/PC3/scripts/PC3-c-r8/r8v_mutate_default_0-9.out).")
row("proj-verifier-mutants-r8-new", "2.6-mutants", "ledgers/PC3/mutants/v31..v34 (written this round)", "FAIL",
    "v31 KILLED by test_replay_agrees_with_the_engine_final_cash_and_inventory[33] (seed 0). v32 SURVIVED (row "
    "proj-grader-determinism-quote-state). v33 SURVIVED and v34 killed only at seed 8 (row proj-grader-no-print).",
    "See proj-grader-no-print and proj-grader-determinism-quote-state.")

# ---- round 8 gate and command rows ----------------------------------------------------------------------------
row("proj-r8-check-tools", "2.6-gates",
    "tools/check_pages.py --all; tools/check_dag.py --all; tools/check_projects.py --all", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_check_pages.out, ledgers/PC3/scripts/PC3-c-r8/r8v_check_dag.out, ledgers/PC3/scripts/PC3-c-r8/r8v_check_projects.out: every unit PASS including PC3, exit 0.")
row("proj-r8-run-labs-page-smoke", "2.5-labs / 2.6-grader",
    "tools/run_labs.py --unit PC3 --page project; tools/run_graders.py --unit PC3 --seeds 0-49; "
    "tools/page_smoke.py --unit PC3 --pages project", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_run_labs_project.out 'run_labs PC3: PASS (3/3)'; ledgers/PC3/scripts/PC3-c-r8/r8v_run_graders.out 'reference 50/50 seeds'; "
    "ledgers/PC3/scripts/PC3-c-r8/r8v_page_smoke_project.out 'page_smoke PC3: PASS' (in-browser suite 441 tests pass on seed 1712259056).")
row("proj-lint-ruff", "2.6-lint", "ruff on course/modules/PC/PC3/grader and tests/labs/PC3", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_ruff_check.out 'All checks passed!'; ledgers/PC3/scripts/PC3-c-r8/r8v_ruff_format.out '14 files already formatted'.")
row("proj-mypy-labs", "2.5-labs", "mypy --no-incremental (repo config: tools, tests)", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_mypy_repo.out 'Success: no issues found in 385 source files'.")
row("proj-grader-mypy-strict", "2.6-lint",
    "grader engine.py, instance.py, reference.py, test_project.py, market_maker (reference copy), labs 1-3",
    "PASS", "Scratch copy: mypy --strict --no-incremental on the eight files: 'Success: no issues found in 8 source "
    "files'. (The repo mypy config covers tools and tests only, so this was run explicitly.)")
row("proj-grader-reference", "2.6-grader", "course/modules/PC/PC3/grader/reference.py", "PASS",
    "run_graders 50/50 seeds (ledgers/PC3/scripts/PC3-c-r8/r8v_run_graders.out); reference is excluded from the panel (data-support lists engine "
    "and instance only).")
row("proj-grader-starter-fails", "2.6-grader", "course/modules/PC/PC3/grader/starter.py", "PASS",
    "Starter stubs with the suite: 367 failed, 66 passed (the 66 do not call the student's module); quote and replay "
    "stubs raise NotImplementedError as the page says.")
row("proj-grader-instances", "2.8-data", "grader/instance.py; test_project.py lines 406-422", "PASS",
    "Determinism, 21 positive values, 5-cent moves and arrival names pass for every seed (433/441).")
row("proj-grader-messages", "2.6-grader", "grader/test_project.py lines 44-59 and every expect() message", "PASS",
    "Each message names the property and contains no computed value (read all messages).")
row("proj-named-refusals", "2.6-spec", "project.html lines 410-419; test_project.py lines 173-221", "PASS",
    "Six must_refuse calls in six test functions cover the two engine messages and two replay messages with the named phrases.")
row("proj-exception-types", "2.6-spec", "test_project.py must_refuse calls (lines 173-221)", "PASS",
    "Every exception-type expectation is for a named condition (crossed quote, size 6 and -1, log length 19 and 21, "
    "filled turn without a price); no other test demands an exception.")
row("proj-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3 --page project", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_run_labs_project.out: 'run_labs PC3: PASS (3/3)'.")
row("proj-check-tools", "2.6-gates", "check_pages, check_dag, check_projects --all", "PASS",
    "Same as proj-r8-check-tools.")
row("proj-page-smoke", "2.5-labs / 2.6-grader", "tools/page_smoke.py --unit PC3 --pages project", "PASS",
    "ledgers/PC3/scripts/PC3-c-r8/r8v_page_smoke_project.out 'page_smoke PC3: PASS'.")
row("proj-banned-and-process-words", "2.6-prose", "project.html text and grader/*.py", "PASS",
    "grep for verifier, builder, architect, batch, agent, TODO, placeholder: no learner-facing match ('around' only).")
row("proj-notation", "2.4-notation", "notation/notation.json against project.html math", "PASS",
    "Registered symbols are T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q. project.html uses none of them. Local symbols "
    "N, I, v_t, b_t, a_t, q_t, pnl are not registered and the registry says N and similar letters are local.")
row("proj-dag-terms", "2.14-DAG", "project.html concept links (one: market-making-game) against L04.html", "PASS",
    "Only data-concept=market-making-game appears (grep); the lesson defines it.")
row("proj-references", "2.1-citations", "project.html reading list (data-cite) and references", "PASS",
    "zhou2008practical and crack2015heard are in references/references.json; ledgers/PC3/scripts/PC3-c-r8/r8v_verify_refs.out 'offline integrity: "
    "560 entries, 0 problems'.")
row("proj-grader-replay-from-fills", "2.6-spec", "project.html Conventions (line 407); test_project.py lines 228-241",
    "PASS", "replay is compared to the fill-sum oracle (oracle, lines 72-83).")
row("proj-exemplar-levels-check-count", "2.6-rubric", "project.html lines 635 and 664", "PASS",
    "Exemplar data-levels and data-scores match the official scoring lines (637, 666).")
row("proj-r8-collect-counts", "2.6-spec",
    "course/modules/PC/PC3/grader/test_project.py; ledgers/PC3/scripts/PC3-c-r8/r8v_collect_r8.out", "PASS",
    "Collect-only and reference pass counts: 433 for seeds 0, 1, 7, 49; 441 for 50, 848197495, 1712259056.")
row("proj-r8-pytest-pc3", "2.6-gates", "pytest -q -k PC3 (ledgers/PC3/scripts/PC3-c-r8/r8v_pytest_pc3.out)", "PASS",
    "Nine tests passed (the lab twins); the grader is not in that collection and is covered by the rows above.")
row("proj-r8-verify-refs", "2.1-citations", "tools/verify_refs.py --offline (ledgers/PC3/scripts/PC3-c-r8/r8v_verify_refs.out)", "PASS",
    "'offline integrity: 560 entries, 0 problems', exit 0.")

# ---- mutants: parsed from this round's mutate_graders output --------------------------------------------------
mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$")
with open(f"{S}/r8v_mutate_default_0-9.out", encoding="utf-8") as fh:
    for line in fh:
        m = pat.match(line.rstrip("\n"))
        if not m:
            continue
        status, name, description, killed = m.groups()
        mutants.append({
            "name": name,
            "description": description,
            "file": f"ledgers/PC3/mutants/{name}",
            "killed_by": None if killed == "None" or status == "SURVIVED" else killed,
        })

counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
verdict = "FAIL" if counts.get("FAIL") or any(m["killed_by"] is None for m in mutants) else "PASS"

fragment = {
    "unit": "PC3",
    "slice": "c",
    "round": 8,
    "verifier": "independent verifier (Haiku 5.5), round 8, slice c (did not build PC3)",
    "pin": PIN,
    "base": f"{R7}; delta 06994db..0dee921a for slice c: project.html (14 lines), grader/starter.py, grader/test_project.py "
            "(new test_a_log_with_no_fill_replays_to_zero), mutants v27-v30 (committed), tests/labs/PC3/lab-PC3-L04-1.py "
            "(not slice c). Every row re-verified this round; no PASS row carried.",
    "checkout": ROOT,
    "scratch": "/tmp/pc3c-r8/ (collect, mypy, mutant, demo and alternative scratch copies)",
    "verified_at": "2026-11-05T01:59:01+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Gates on pin 0dee921a (ledgers/PC3/scripts/PC3-c-r8/r8v_*.out): check_pages, check_dag, check_projects PASS; run_labs PC3 project 3/3; "
        "run_graders 0-49 reference 50/50; page_smoke PASS; ruff check and format PASS; mypy --no-incremental PASS; "
        "mypy --strict on grader and labs PASS (scratch); verify_refs offline PASS; pytest -k PC3 9 passed. Mutants: "
        "mutate_graders --unit PC3 --seeds 0-9 on 43 mutants (39 existing + v31-v34 written this round): 41 killed, "
        "2 survived (v32, v33); v34 killed at seed 8 only. Alternatives: 25 earlier correct implementations (all 52 seeds pass) and 5 new "
        "ones (alt_r8_a..e) pass all seeds checked (52 or 53 each). Exemplar scoring: A 4,4,4,3,4 and B 2,2,1,2,1, equal "
        "to the official scoring; caveat: the official scoring and annotations were in the same Read output, so the "
        "blind step was not a separate pass. Not checked: a real browser render of the grader panel and self-assessment "
        "form (page_smoke only); the L04 twin and index.html beyond the cross-slice lines cited; cards (not in scope); "
        "render_curriculum, build_site --check and fetch_data --check (outside slice c); learner seeds outside the "
        "reported set; the S/r8v collect of the whole repo (only -k PC3). Note: ledgers/PC3/scripts/PC3-c-r8/"
        "run_alts_c_r8.py and collect_counts.sh (committed at the pin by another agent) point at the main checkout "
        "/Users/billyribeiro/dev/quant-phd, not this pin; their outputs were not relied on."
    ),
    "summary": (
        f"PC3-c round 8: verdict {verdict}. Rows: {len(rows)} total, "
        f"{counts.get('PASS', 0)} PASS, {counts.get('FAIL', 0)} FAIL, {counts.get('UNVERIFIABLE', 0)} UNVERIFIABLE. "
        f"Mutants: {len(mutants)} (39 existing + 4 new), {sum(1 for m in mutants if m['killed_by'])} killed, "
        f"{sum(1 for m in mutants if not m['killed_by'])} survived (v32 global quote state; v33 print on no-fill replay). "
        "Round-7 FAILs fixed: count sentence (433/441), C5 wording, starter docstring, hub file names and premise, "
        "v27 no-fill replay. Still open: plan file names (policy.py/pnl.py vs market_maker.py), three rubric ladder gaps "
        "(C1 components without P&L, C2 turns cited without value, C3 rerun with one run's P&L), no-print check on one "
        "game only, and no determinism test for the quote."
    ),
}

problems = []
for r in rows:
    if r["status"] not in ("PASS", "FAIL", "UNVERIFIABLE"):
        problems.append(r["id"])
    if r["status"] != "PASS" and not r.get("fix"):
        problems.append(r["id"] + " no fix")
ids = [r["id"] for r in rows]
dups = sorted({i for i in ids if ids.count(i) > 1})
print("rows", len(rows), counts, "mutants", len(mutants), "dups", dups, "problems", problems)
with open(f"{ROOT}/ledgers/PC3/PC3-c.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
