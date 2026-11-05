"""Round 10 verifier (slice c): builds ledgers/PC3/PC3-c.json from the round 9 fragment ids, the round 10 gate outputs
under ledgers/PC3/scripts/PC3-c-r10/ and the mutants run by tools/mutate_graders.py. Every round 9 row id is kept."""

import datetime
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE10-PC3-c")
S = ROOT / "ledgers/PC3/scripts/PC3-c-r10"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-PC3-c.round9.json").read_text())
prev_rows = {r["id"]: r for r in prev["rows"]}

G = "course/modules/PC/PC3/grader/test_project.py"
P = "course/modules/PC/PC3/project.html"
CARRY = "Carried from round 9 (cited subject byte-identical since the previous pin: "

# id -> (status, location, evidence). Rows not listed keep the round 9 check label; their evidence is re-stated here.
R10 = {
    "proj-zero-fill-replay": ("PASS", f"{G} lines 315-323 (test_a_log_with_no_fill_replays_to_zero, shifted by one line after the new import on line 22); {P} line 393 (replay returns four keys)",
        "Fresh r10: run_graders PC3 0-49 reference 50/50 (run_graders_PC3.out); test_a_log_with_no_fill_replays_to_zero compares replay with the oracle on a no-fill log; project.html line 393 names the four keys that test_replay_returns... checks (test line 235)."),
    "proj-rubric-observable": ("PASS", f"{P} line 627 (C5 level 3 'as a word (it holds or it fails), with no number' against level 4 'gives the number')",
        "Read in full (r10). Level 3 forbids a number and level 4 requires one, so the two are separable by a reader. No vague descriptor found in the C1-C5 table (lines 623-627)."),
    "proj-rubric-ladder-gap-c1": ("PASS", f"{P} line 623 (C1 level 2)",
        "C1 level 2 needs two or more of the three values, each equal to replay, and no value replay does not return; level 1 is its complement (fewer than two, or a value replay does not return). Checked r10 against the table text, no gap."),
    "proj-rubric-ladder-gap-c1-no-pnl": ("PASS", f"{P} line 623 (C1 levels 1-3)",
        "A passage with cash flow and mark but no P&L is level 2 (two or more correct values); with three correct values and no turn named it is level 2; level 3 needs the three values and the cash-flow turns. Checked r10, no gap."),
    "proj-rubric-ladder-gap-c2": ("PASS", f"{P} line 624 (C2 levels 1-2, rewritten in round 10: level 2 'cites one or more turns by number, with at least one value from the log, or with a cited value that does not match'; level 1 'cites turns and gives no value from the log for any of them')",
        "Round 9 FAIL closed. A passage that cites turn 5 by number and field with no value is level 1; a passage with one turn and its value is level 2; a passage with only a mismatching value is level 2 by the 'or' clause. No passage falls outside levels 1-4."),
    "proj-rubric-ladder-gap-c3": ("PASS", f"{P} line 625 (C3 level 2)",
        "One change with its amount in cents and no rerun is level 2 ('either gives no rerun ...'); level 1 requires a change without its amount or no counterfactual. Checked r10."),
    "proj-rubric-ladder-gap-c3-one-run": ("PASS", f"{P} line 625 (C3 levels 2-4)",
        "Same seed with the P&L of at most one run and no difference is level 2; both runs without the difference is level 3; the change reported in cents is level 4. Checked r10."),
    "proj-rubric-ladder-gap-c3-other-seed": ("PASS", f"{P} line 625 (C3 levels 1-2, round 10 text: level 2 'either gives no rerun, reruns another seed, or ...')",
        "Round 9 FAIL closed: a rerun on another seed with an amount in cents is level 2 by the 'reruns another seed' branch. The gap still open for both runs with the difference unstated in cents is a separate row (proj-rubric-ladder-gap-c3-difference-no-unit)."),
    "proj-grader-35-checks": ("PASS", f"{P} line 397; {G} (per-seed tests at lines 145, 229, 246, 327, 343, 350, 380, 391, 432; seed-only and fixed-seed tests)",
        "ledgers/PC3/scripts/PC3-c-r10/r10_collect.out: collect-only 484 for seeds 0, 1, 7, 49 and 493 for seeds 50, 848197495, 1712259056. Arithmetic: 9 x 51 + 24 + 1 = 484; 9 x 52 + 24 + 1 = 493. Seed-only count 24 = 493 - (9 x 52 + 1). Matches page line 397."),
    "proj-starter-docstring-raise-scope": ("PASS", "course/modules/PC/PC3/grader/starter.py lines 8-9; project.html lines 411-418 and 418",
        "starter docstring says named invalid inputs must raise ValueError and the engine refuses an illegal quote; project.html 418 says other invalid input may raise any exception or return a value. Consistent. starter run: ledgers/PC3/scripts/PC3-c-r10/starter_fails.out (418 failed, 66 passed), so the empty implementation fails the suite."),
    "proj-plan-file-names": ("FAIL", "plans/PC3-build-plan.md lines 67-70, 317, 337, 340, 348 (policy.py, pnl.py); course/modules/PC/PC3/project.html lines 46, 393, 429, 443 and course/modules/PC/PC3/index.html lines 160, 167 (market_maker.py)",
        "Still open (unchanged since round 9). The plan names policy.py (quote) and pnl.py (replay) and a separate pnl.py; the shipped contract (project.html 393, index.html 160 and 167, grader/test_project.py line 30) is one market_maker.py. Verified r10 with grep. Fix: update the plan's Required outputs and grading lines to market_maker.py (both functions in one module) or mark the plan superseded for PC3."),
    "proj-hub-filenames": ("PASS", "course/modules/PC/PC3/index.html lines 160 and 167",
        "Fresh r10 grep: line 160 names market_maker.py and analysis.md; line 167 names market_maker.py for quote and replay. Matches project.html 393 and 446-449."),
    "proj-hub-skill-check-premise": ("PASS", f"course/modules/PC/PC3/index.html line 129 against {P} line 406",
        "Index line 129: a purchase at a bid of 10005 cents, cash flow with a negative value for cash paid out (expected -10005). Project line 406: a maker purchase at the bid b changes cash by -b. Consistent."),
    "proj-exemplar-a-numbers": ("PASS", f"{P} lines 635-662 (exemplar A)",
        "ledgers/PC3/scripts/PC3-c-r10/numbers_r10.out: purchases at bid turns 2,3,4,8,19 total 49910; sales at ask turns 5,7,13,18 total 39960; cash flow -9950; inventory 1; mark 9980; P&L 30; largest |inventory| 3; counterfactual half-spread 15 gives P&L 55, change +25, 9 fills. Turn 2 bid 9990, turn 5 ask 9980 with inventory 2 after, turn 18 ask 10000 with inventory 0 after: all as the exemplar states."),
    "proj-lab1-replay-prints": ("PASS", f"{P} lab-PC3-project-1 (lines 55-240) against tests/labs/PC3/lab-PC3-project-1.py",
        "run_labs PC3 project 3/3 (run_labs_project.out): page code equals the twin and the expected block equals the output. Isolated twin run under python -I -W error exit 0, empty stderr (twin_project_1.exit/.stderr). Fresh r10."),
    "proj-lab1-run": ("PASS", f"{P} lab-PC3-project-1; tools/run_labs.py",
        "ledgers/PC3/scripts/PC3-c-r10/run_labs_project.out: run_labs PC3: PASS (3/3)."),
    "proj-lab1-hypothesis-numbers": ("PASS", f"{P} line 57 (Lab 1 hypothesis)",
        "Hypothesis numbers 9 fills, -9950, 1 unit, 9980 mark, 30 P&L, limit 10 not passed: all equal to numbers_r10.out and the lab's printed block (project.html 234-238). Fresh r10."),
    "proj-lab2-completion": ("PASS", f"{P} lab-PC3-project-2 (lines 242-380)",
        "run_labs PC3 project PASS (completion rule: page lines equal the twin except the two ___ blanks). Isolated twin run under python -I -W error exit 0 (twin_project_2.exit). Expected block (374-380) equals output."),
    "proj-lab2-interpretation-last-quote": ("PASS", f"{P} line 381 (Lab 2 interpretation)",
        "With inventory 1 unit, P&L = -9950 + mark, so a mark other than 9980 changes the P&L on seed 0 (arithmetic). Read in full r10."),
    "proj-lab3-counterfactual": ("PASS", f"{P} lines 457-612 (Lab 3)",
        "run_labs PC3 project PASS for lab 3; expected block 600-610 equals output; numbers_r10.out: half-spread 15 gives 9 fills, P&L 55, change 25. Isolated twin run exit 0 (twin_project_3.exit)."),
    "proj-lab3-interpretation": ("PASS", f"{P} line 611 (Lab 3 interpretation)",
        "Prose: the block is the reference output, the counterfactual changes one number (half-spread) and reruns one game; the 25-cent difference is stated as a one-seed difference. Consistent with the lab code (play(SEED, 15)) and the expected block."),
    "proj-rung1-instance-claim": ("PASS", f"{P} line 391; course/modules/PC/PC3/grader/instance.py lines 27-53",
        "make_instance returns 21 fair values (v0 = 10000, positive, moves of exactly 5) and 20 arrivals: checked for seeds 0-19 in ledgers/PC3/scripts/PC3-c-r10/instances_20_seeds.out (every assertion passed)."),
    "proj-conventions-constants": ("PASS", f"{P} lines 402-407 (Conventions) and 393",
        "N = 20, v0 = 10000, moves +-5 with probability 1/2 (instance.py line 37), arrivals 1/4, 1/4, 1/2 (instance.py lines 40-45), trade rules (engine.py lines 35-46 and 80-86), cash and inventory (engine.py lines 84-86), P&L identity (replay in test_project.py line 337). Each constant equals the code."),
    "proj-exemplar-a-calibration": ("PASS", f"{P} lines 635-662 against rubric lines 623-627",
        "Blind scoring r10 from the passage text and the rubric (annotations not consulted for this score): C1 4, C2 4, C3 4, C4 3, C5 4 against official 4,4,4,3,4. Disclosure: the annotation block (lines 651-660) appeared in a diff I printed before writing these scores; the scores were derived from the passage and the descriptors. Every criterion within one level."),
    "proj-exemplar-b-calibration": ("PASS", f"{P} lines 664-692 against rubric lines 623-627",
        "Blind scoring r10: C1 2 (states P&L and cash flow; no mark), C2 2 (one turn with its value), C3 1 (change with no amount), C4 2 (names probabilities without effect), C5 1 (checked, no check named). Official 2,2,1,2,1: exact match."),
    "proj-exemplar-b-numbers": ("PASS", f"{P} lines 664-690 (exemplar B)",
        "P&L 30 and cash flow -9950 are the replay outputs (numbers_r10.out); turn 5 sold at the ask of 9980 (turn 5 ask 9980, fill 9980)."),
    "proj-exemplar-b-arrival-sensitivity": ("PASS", f"{P} line 676 (exemplar B text) and line 687 (annotation C4 level 2)",
        "Exemplar B names the probabilities 1/4, 1/4, 1/2 without any result they move; the annotation at line 687 says so (level 2). Consistent."),
    "proj-rubric-c2-level3-admits-mismatch": ("PASS", f"{P} line 624 (C2 levels 2 and 3)",
        "Level 3 requires every cited value to match and level 2 has the mismatch clause, so a two-turn passage with a mismatched value is level 2. Non-FAIL note (r10): level 3 says 'cites two turns' while level 4 says 'at least three'; a three-turn passage with two valued citations reads as level 3 under the highest-level-met reading and level 2 under a literal exact-count reading. The ladder is read cumulatively, which the exemplar annotations do."),
    "proj-rubric-c4-real-form-undefined": ("PASS", f"{P} line 626 (C4 level 4) against course/modules/PC/PC3/L04.html line 481",
        "L04 line 481 (moved from 466 in round 8): the queue of resting orders is not modelled and the model does not learn from the fills. The page's 'both set aside in Lesson 4' matches. Latency and more than one asset are named by the page as omissions without a claim about Lesson 4."),
    "proj-spec-log-schema": ("PASS", f"{P} line 393 against course/modules/PC/PC3/grader/engine.py lines 88-98",
        "The turn record keys on the page (turn, bid_cents, ask_cents, size, arrival, filled, fill_price_cents, inventory_after, cash_after_cents) equal the dict engine.py writes at lines 89-98; log keys seed, settlement_cents, turns (line 100)."),
    "proj-hours-arithmetic": ("PASS", f"course/modules/PC/PC3/index.html line 167; {P} lines 427-434",
        "Round 9 FAIL closed: index.html line 167 now says 'seven lines' and project.html has seven component rows: 1 + 1 + 3 + 2 + 2 + 4 + 1 = 14; 14/50 = 28 percent of the module (index line 167 and the hours-split bar aria-label '36 lesson hours and 14 project hours' agree). Estimate of the components: about 13 to 16 hours, within 30 percent of 14."),
    "proj-hub-placement-conflict": ("PASS", f"{P} lines 42-48 against course/modules/PC/PC3/index.html line 156",
        "index line 156: rungs 1 and 2 are skipped by reaching the placement bar and answering both skill checks; project line 42 says the same. Carried from round 9 (cited lines byte-identical since the previous pin: index.html line 156)."),
    "proj-hub-seed-scope": ("PASS", "course/modules/PC/PC3/index.html lines 55 and 160 against project.html line 397 and grader/test_project.py lines 36-38",
        "index line 55: seeds 0 to 49 and your own workspace seed; index line 160 adds seed plus 7919; project 397 and test lines 36-38 give the same set. Carried from round 9 (cited lines byte-identical since the previous pin)."),
    "proj-quote-rule-first-fill-survivor": ("PASS", f"{P} line 429 (quote row); ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py",
        "alt6 (mid from the first fill) passes all tests on seeds 0, 7, 49, 50, 848197495, 1712259056 (r10_alts_6seeds.out). The spec fixes no quoting rule, only legality (project line 395), so a different rule is legal."),
    "proj-builder-mutants": ("PASS", "ledgers/PC3/mutants/m01..m10",
        "tools/mutate_graders.py --unit PC3 --seeds 0-9 (mutate_r10_0-9.out): m01-m10 all KILLED."),
    "proj-verifier-mutants": ("PASS", "ledgers/PC3/mutants/v01..v26 (v17 absent from the set)",
        "mutate_r10_0-9.out: every v01-v16 and v18-v26 KILLED. Re-run on the round 10 grader (test_project.py changed)."),
    "proj-mutant-m08-description": ("PASS", "ledgers/PC3/mutants/m08_hard_coded_answer_for_any_log.py line 1",
        "Line 1: 'Student error: replay returns all zeros, a hard-coded answer, for every log.' Carried from round 9 (file byte-identical since the previous pin)."),
    "proj-verifier-mutants-r3-new": ("PASS", "ledgers/PC3/mutants/v13..v16",
        "mutate_r10_0-9.out: v13-v16 KILLED."),
    "proj-alternatives-1-2-4-5": ("PASS", "ledgers/PC3/alternatives/alt1, alt2, alt4, alt5",
        "r10_alts_6seeds.out: 0 of 6 seeds fail for each."),
    "proj-alt3-replay": ("PASS", "ledgers/PC3/alternatives/alt3_inventory_skew.py",
        "r10_alts_6seeds.out: 0 of 6 seeds fail."),
    "proj-alternative-6": ("PASS", "ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py",
        "r10_alts_6seeds.out: 0 of 6 seeds fail."),
    "proj-alternative-7-8-verifier": ("PASS", "ledgers/PC3/scripts/PC3-c-r2/alt7, alt8",
        "r10_alts_6seeds.out: 0 of 6 seeds fail each."),
    "proj-alternative-9-10-verifier-r3": ("PASS", "ledgers/PC3/scripts/PC3-c-r3/alt9, alt10",
        "r10_alts_6seeds.out: 0 of 6 seeds fail each."),
    "proj-alternatives-r4-new": ("PASS", "ledgers/PC3/scripts/PC3-c-r4/alts/alt11, alt12, alt13",
        "r10_alts_6seeds.out: 0 of 6 seeds fail each."),
    "proj-alternatives-r7-new": ("PASS", "ledgers/PC3/scripts/PC3-c-r7/alts/alt20..alt24",
        "r10_alts_6seeds.out: 0 of 6 seeds fail each."),
    "proj-r8-alternatives-new": ("PASS", "ledgers/PC3/scripts/PC3-c-r8/alts/alt_r8_a..e",
        "r10_alts_6seeds.out: 0 of 6 seeds fail each."),
    "proj-grader-seed-scope-claim": ("PASS", f"{P} line 397 against {G} lines 36-38",
        "SEED = QF_SEED (line 36), FIXED_SEEDS = range(50) (line 37), SEEDS adds SEED and SEED + 7919 (line 38). Matches the page."),
    "proj-grader-no-print": ("PASS", f"{G} lines 391-407 (test_no_function_prints_or_warns, all seeds) and 315-323 (no-fill replay); {P} line 395",
        "The test covers the game and a no-fill log on every seed; v08, v09, v24, v26, v27, v33, v34 KILLED (mutate_r10_0-9.out)."),
    "proj-grader-determinism-quote-state": ("PASS", f"{G} lines 411-426 (reload before each game); {P} lines 395 and 397",
        "Round 9 FAIL closed: the module is reloaded before the first game and before the other game, so a module-level cache from an earlier game cannot survive. v32 and v38 (module global and per-turn module dict) and v40 and v41 (unseeded generator and default-argument cache) are KILLED by this test (mutate_r10_0-9.out). The direct-call gap that remains is a separate FAIL row (proj-grader-state-between-turns)."),
    "proj-js-claims": ("PASS", f"{P} line 442 against course/assets/js/grader.js lines 56-61",
        "grader.js lines 56-61 store the draft after a 400 ms debounce (store.put) and line 53 writes 'derived from your workspace ID'. Carried from round 9 (grader.js and project.html line 442 byte-identical since the previous pin)."),
    "proj-local-commands": ("PASS", f"{P} lines 446-455 and 393",
        "Fresh r10: the page's game-log command run in a scratch copy with the reference as market_maker wrote a 20-turn log; QF_SEED=7 local pytest with the page's flags: 484 passed. No assert statement in test_project.py (grep), so --assert=plain changes nothing."),
    "proj-known-limitation": ("PASS", f"{P} line 395",
        "Text names the known limitation (the instance is readable, the autograder cannot check the fair path). Consistent with the file: the instance is in grader/instance.py and the suite cannot read the fair path of the learner's rule."),
    "proj-ladder-scope": ("PASS", f"{P} lines 40-50", "Four rungs as in the page; rung 3 names the module, the autograder section and the analysis. Carried from round 9 (lines 40-50 byte-identical since the previous pin)."),
    "proj-rubric-atlas-studios": ("PASS", f"{P} (whole page); plans/PC3-build-plan.md",
        "PC3 has no atlas milestone or studio in its plan; the page's rubric is the only rubric. Carried from round 9 (plan and page lines byte-identical except the rubric hunk, which does not touch atlas or studio text)."),
    "proj-stretch": ("PASS", f"{P} lines 702-710", "Three stretch items; seeds 0 to 199, informed share 0.6, inventory limit 5 are computable from the engine; nothing claimed about them. Read in full r10."),
    "proj-twin-rules": ("PASS", "tests/labs/PC3/lab-PC3-project-1..3.py",
        "run_labs PC3 project PASS; twins under python -I -W error exit 0 with empty stderr; page code equals the twin (modulo trailing newline)."),
    "proj-exception-types-labs": ("PASS", "tests/labs/PC3/lab-PC3-project-1..3.py",
        "The twins raise ValueError only for the two named replay conditions (20 turns, filled without a fill price), lines in the twin replay functions."),
    "proj-r4-new-mutants-v18-v20": ("PASS", "ledgers/PC3/mutants/v18..v20", "mutate_r10_0-9.out: KILLED."),
    "proj-grader-window-distinct-paths": ("PASS", f"{G} lines 450-454 (test_fixed_seeds_0_to_49_give_fifty_different_paths; was 425-429 before the import line)",
        "Fresh r10: the test passes on the reference; the 50 fixed seeds give 50 distinct paths (collect and reference run)."),
    "proj-grader-v21-replay-scales-by-size": ("PASS", "ledgers/PC3/mutants/v21", "mutate_r10_0-9.out: KILLED by test_a_fill_is_one_unit_whatever_its_quoted_size."),
    "proj-grader-v22-zero-fill-price-refused": ("PASS", "ledgers/PC3/mutants/v22", "mutate_r10_0-9.out: KILLED by test_a_fill_at_price_zero_is_a_legal_fill."),
    "proj-exemplar-levels-vs-plan": ("PASS", f"{P} lines 635 and 664; plans/PC3-build-plan.md line 380",
        "Plan line 380: exemplar-a data-level 4, exemplar-b data-level 2; page data-level 4 and 2 at lines 635 and 664. Carried from round 9 (plan and those lines byte-identical since the previous pin)."),
    "proj-instance-engine-names": ("PASS", "course/modules/PC/PC3/grader/instance.py line 27 (make_instance); engine.py line 49 (play(quote, seed))",
        "grep r10: instance.py:27 def make_instance(seed); engine.py:49 def play(quote, seed); page names match (project.html 391, 393, 448)."),
    "proj-r5-mutant-v23-first-fill-price": ("PASS", "ledgers/PC3/mutants/v23", "mutate_r10_0-9.out: KILLED."),
    "proj-r5-alternatives-14-16": ("PASS", "ledgers/PC3/scripts/PC3-c-r5/alts/alt14, alt15, alt16", "r10_alts_6seeds.out: 0 of 6 seeds fail each."),
    "proj-r5-labs-page-vs-twin": ("PASS", "project labs (page code vs twin)", "run_labs PC3 project PASS: page code equals twin."),
    "proj-grader-v24-stderr-print-survives": ("PASS", "ledgers/PC3/mutants/v24", "mutate_r10_0-9.out: KILLED by test_no_function_prints_or_warns (the row name is historical; the mutant is killed)."),
    "proj-grader-v25-last-filled-totals-survives": ("PASS", "ledgers/PC3/mutants/v25", "mutate_r10_0-9.out: KILLED by test_stale_totals_on_the_last_filled_turn_are_not_used."),
    "proj-grader-v26-logging-warning-survives": ("PASS", "ledgers/PC3/mutants/v26", "mutate_r10_0-9.out: KILLED by test_no_function_prints_or_warns."),
    "proj-plan-grader-seed-scope": ("PASS", "plans/PC3-build-plan.md lines 348 and 380",
        "Plan line 348 says the autograder runs on seeds 0-49; the page adds the learner's seed and seed plus 7919 (397), a superset that the plan does not contradict. Carried from round 9 (plan lines byte-identical since the previous pin). The plan's file names are a separate FAIL row."),
    "proj-verifier-mutants-r7-new": ("PASS", "ledgers/PC3/mutants/v27..v30", "mutate_r10_0-9.out: KILLED."),
    "proj-verifier-mutants-r8-new": ("PASS", "ledgers/PC3/mutants/v31..v34", "mutate_r10_0-9.out: KILLED."),
    "proj-r8-check-tools": ("PASS", "tools/check_pages.py --all; tools/check_dag.py --all; tools/check_projects.py --all",
        "ledgers/PC3/scripts/PC3-c-r10/check_pages.out, check_dag.out, check_projects.out: PC3 PASS (exit 0)."),
    "proj-r8-run-labs-page-smoke": ("PASS", "tools/run_labs.py --unit PC3 --page project; tools/run_graders.py --unit PC3 --seeds 0-49; tools/page_smoke.py --unit PC3 --pages project",
        "run_labs PC3 PASS (3/3); run_graders PC3 reference 50/50 (14.3 s); page_smoke PC3 project PASS, in-browser suite 493 tests pass on seed 1021546817."),
    "proj-lint-ruff": ("PASS", "ruff check and ruff format --check on course/modules/PC/PC3/grader and tests/labs/PC3",
        "ruff_check.out: All checks passed; ruff_format.out: 14 files already formatted (exit 0)."),
    "proj-mypy-labs": ("PASS", "mypy --no-incremental (repo config)",
        "mypy_repo.out: Success: no issues found in 385 source files (exit 0)."),
    "proj-grader-mypy-strict": ("PASS", "grader engine.py, instance.py, reference.py, starter.py, test_project.py and labs 1-3 under mypy --strict",
        "mypy_strict_grader_labs.out: Success, 9 source files, run in a scratch copy with reference.py copied as market_maker.py (the repo has no market_maker.py, so the in-place run reports import-not-found for the student module; that is the student's file, not a defect)."),
    "proj-grader-reference": ("PASS", "course/modules/PC/PC3/grader/reference.py", "run_graders PC3 0-49: reference 50/50 (run_graders_PC3.out)."),
    "proj-grader-starter-fails": ("PASS", "course/modules/PC/PC3/grader/starter.py", "starter_fails.out: starter as market_maker fails 418 tests (66 pass); the empty implementation does not pass."),
    "proj-grader-instances": ("PASS", "course/modules/PC/PC3/grader/instance.py; test_project.py lines 431-447",
        "instances_20_seeds.out: 20 seeds valid (21 positive values, moves of 5, 20 arrivals with the three names) and 8 distinct reference P&L values across them, 7 distinct settlements."),
    "proj-grader-messages": ("PASS", f"{G} lines 44-60 (expect and must_refuse) and every expect() message",
        "Read every message in r10; none contains a computed value (the refusal message names the condition phrase, which the page publishes)."),
    "proj-named-refusals": ("PASS", f"{P} lines 410-419; {G} must_refuse calls (lines 176-222)",
        "Four named conditions (bid below ask, size 0..5, 20 turns, a fill price) each tested with must_refuse; the page names the same four messages."),
    "proj-exception-types": ("PASS", f"{G} must_refuse calls and the page's named-invalid list (project.html 410-419)",
        "must_refuse is used only for the four named conditions; every other failure is expect()/pytest.fail (r10 read)."),
    "proj-run-labs-unit": ("PASS", "tools/run_labs.py --unit PC3 --page project", "run_labs_project.out: run_labs PC3: PASS (3/3)."),
    "proj-check-tools": ("PASS", "check_pages, check_dag, check_projects --all", "PC3 PASS in all three (check_*.out, exit 0)."),
    "proj-page-smoke": ("PASS", "tools/page_smoke.py --unit PC3 --pages project", "page_smoke_project.out: PASS; in-browser grader 493 tests pass on seed 1021546817."),
    "proj-banned-and-process-words": ("PASS", f"{P}; course/modules/PC/PC3/grader/*.py; tests/labs/PC3/lab-PC3-project-*.py",
        "grep r10 for BUILDER_RULES 1.3-1.4 strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, we will, as we saw) and for URLs and ellipses: no hit. Process words (verifier, builder, round, agent): none."),
    "proj-notation": ("PASS", f"notation/notation.json against {P} math",
        "notation.json registers 8 symbols (T, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, ...). The page uses N, t, v_t, v_0..v_20, I, I_20, b, a, b_t, a_t, q_t, pnl; none collides with a registered meaning (grep r10)."),
    "proj-dag-terms": ("PASS", f"{P} line 37 (concept link market-making-game) against course/modules/PC/PC3/L04.html line 60",
        "The concept is defined at L04 line 60 (def-market-making-game) and linked from project line 37 with href L04.html#def-market-making-game; check_dag PC3 PASS."),
    "proj-references": ("PASS", f"{P} reading list (data-cite) and references/references.json",
        "data-cite keys zhou2008practical and crack2015heard are present in references/references.json; verify_refs --offline: 560 entries, 0 problems (r8 and r10). The page attributes no page, edition or problem to either book. Carried from round 9 (references.json byte-identical since the previous pin)."),
    "proj-grader-replay-from-fills": ("PASS", f"{P} line 407 (Conventions); {G} lines 229-242",
        "Conventions: the cash flow is the sum of the fill cash flows; test_replay_returns_the_fills... compares replay with the fills (oracle)."),
    "proj-exemplar-levels-check-count": ("PASS", f"{P} lines 635 and 664", "data-scores 4,4,4,3,4 and 2,2,1,2,1: five criteria each, matching the five C-rows of the rubric."),
    "proj-r8-collect-counts": ("PASS", f"{G}; ledgers/PC3/scripts/PC3-c-r10/r10_collect.out", "Seeds 0,1,7,49: 484 collected; seeds 50, 848197495, 1712259056: 493 collected (r10)."),
    "proj-r8-pytest-pc3": ("PASS", "pytest -q -k PC3", "pytest_pc3.out: 9 passed (exit 0)."),
    "proj-r8-verify-refs": ("PASS", "tools/verify_refs.py --offline", "verify_refs_offline.out: offline integrity: 560 entries, 0 problems (exit 0)."),
    "proj-exemplar-a-c5-annotation": ("PASS", f"{P} line 658 (annotation C5 level 4) against line 649 (self-review text)",
        "Round 9 FAIL closed: the annotation now names the identity with its computed number (30 = -9950 + 1 x 9980) and says the agreement with the final cash is named without a number; line 649 does exactly that, and the level 4 descriptor needs one check with its number."),
    "proj-verifier-mutants-r9-new": ("PASS", "ledgers/PC3/mutants/v35, v36, v37, v38",
        "Round 9 FAIL closed: mutate_r10_0-9.out KILLS v35-v38 on the round 10 grader (v38 was the survivor in round 9, now killed by the reload test)."),
}

NEW_ROWS = [
    {"id": "proj-grader-state-between-turns", "check": "2.6-spec (quote depends only on the state it is given; keeps nothing between turns or games outside that state)",
     "location": f"{G} lines 411-426 (only engine-driven games are compared); {P} line 395 ('A quote depends only on the state it is given: it keeps nothing between turns or games outside that state.')",
     "status": "FAIL",
     "evidence": "Mutant ledgers/PC3/mutants/v39_quote_keeps_the_mid_between_turns_reset_on_turn_one.py keeps the mid in a module global, reads only history[-1:], resets on turn 1. It SURVIVES every test on seeds 0-9 (mutate_r10_0-9.out) because the suite only calls quote through engine.play, which always passes a consecutive history. It is not equivalent: a direct call on a hand-built state separates it from the reference (ledgers/PC3/scripts/PC3-c-r10/probe_direct_state_v39.out): state at turn 5, history with a fill at 10020 on turn 2 and no fill on turns 1, 3, 4; reference (10010, 10030, 1), v39 on a fresh module (9990, 10010, 1).",
     "fix": "Add a test that calls sol.quote directly on hand-built states, not through engine.play: reload the module; call quote on a turn-5 state whose history has a fill at a price other than 10000 on turn 2 and no fill on turn 4, after a quote call on a different state (for example turn 1 with empty history); the answer must equal the answer of a freshly reloaded module on the same state. Name the property in the message; no value."},
    {"id": "proj-rubric-ladder-gap-c3-difference-no-unit", "check": "2.6-rubric (ladder covers every submission; descriptors exhaustive)",
     "location": f"{P} line 625 (C3 level 3 'gives the P&L of both runs without their difference' and level 4 'reports the change in pnl_cents in cents')",
     "status": "FAIL",
     "evidence": "Passage: 'Counterfactual: a half-spread of 15 cents (amount in cents); rerun of seed 0; P&L 30 and 55; the change is 25.' The change is not in cents, so level 4 is not met; level 3 is not met because the difference is given; level 2 is not met (both runs given, so 'at most one run' fails, and the rerun is on the same seed); level 1 is not met (the amount is in cents). No descriptor applies. Confirmed by reading lines 625 against the passage (r10).",
     "fix": "Reword level 3 to 'states one change with its amount, reruns the same seed, and gives the P&L of both runs, without the change reported in cents'. Then this passage is level 3 and the level 4 wording stays as is."},
    {"id": "proj-rubric-ladder-gap-c5-wrong-number", "check": "2.6-rubric (ladder covers every submission)",
     "location": f"{P} line 627 (C5 levels 1-4)",
     "status": "FAIL",
     "evidence": "Passage: 'Self-review: the identity holds, 31 = -9950 + 1 x 9980.' The check is named with a number that replay does not produce. Level 4 needs the number the check computed (not met: 31 is not computed by the check); level 3 needs the result as a word with no number (not met); level 2 needs the check without its result (not met: a result is given); level 1 covers no self-review or no named check (not met). No descriptor applies (r10 reading of line 627).",
     "fix": "Add to level 1: 'or names a check whose number is not the number replay produces'. This mirrors the C1 level 1 clause for a value that replay does not return."},
    {"id": "proj-verifier-mutants-r10-new", "check": "2.6-mutants (new student-error mutants v39-v42, round 10)",
     "location": "ledgers/PC3/mutants/v39_quote_keeps_the_mid_between_turns_reset_on_turn_one.py, v40_quote_draws_on_an_unseeded_generator.py, v41_quote_caches_the_mid_in_a_default_argument.py, v42_replay_reads_turn_twenty_before_the_length_check.py",
     "status": "FAIL",
     "evidence": "mutate_graders --unit PC3 --seeds 0-9 (mutate_r10_0-9.out): v40 KILLED by test_the_quote_depends_only_on_the_state_it_is_given; v41 KILLED by the same test; v42 KILLED by test_replay_refuses_a_log_that_is_not_twenty_turns[19]; v39 SURVIVED (see proj-grader-state-between-turns). 50 of 51 mutants killed; the one survivor is a stated-behaviour violation.",
     "fix": "Kill v39 with the direct-call test named in proj-grader-state-between-turns. Keep the other three as regression mutants."},
    {"id": "proj-alternatives-r10-new", "check": "2.7-alternatives (five-plus correct alternatives must pass; over-constraint check)",
     "location": "ledgers/PC3/scripts/PC3-c-r10/alts/alt_r10_a_reversed_scan_size_two.py, alt_r10_b_class_inventory_skew_size_zero.py, alt_r10_c_cache_rewritten_each_call.py, alt_r10_d_zero_size_on_last_turn.py",
     "status": "PASS",
     "evidence": "r10_run_alts.py (r10_alts_6seeds.out): all four pass on seeds 0, 7, 49, 50, 848197495, 1712259056 with the page's flags; they cover a reversed scan with size 2, a class with inventory skew and size 0 at the limit, a module cache rewritten each call (which the reload test must not reject), and a size 0 on turn 20 with a 25-cent half-spread on odd turns. Every alternative in slice c (34 files) passes on the same six seeds."},
    {"id": "proj-r10-instances-20-seeds", "check": "2.6-grader (instances valid and differ materially, sampled 20 seeds)",
     "location": f"{G}; course/modules/PC/PC3/grader/instance.py lines 27-53",
     "status": "PASS",
     "evidence": "ledgers/PC3/scripts/PC3-c-r10/instances_20_seeds.py (output instances_20_seeds.out): seeds 0-19: 21 positive fair values starting at 10000, moves of exactly 5, 20 arrivals with the three names; reference P&L takes 8 distinct values across the 20 seeds (-110 to 80 cents), settlements take 7 distinct values; the answers change, not only the labels."},
    {"id": "proj-r10-local-command", "check": "2.6-grader (page's local command and local flags work)",
     "location": f"{P} lines 393 and 448-449; course/modules/PC/PC3/grader/starter.py lines 6",
     "status": "PASS",
     "evidence": "In a scratch copy with reference.py as market_maker.py, the page's command 'python3 -c \"import json, engine, market_maker; print(json.dumps(engine.play(market_maker.quote, <seed>)))\" > game_log.json' wrote a 20-turn log with keys seed, settlement_cents, turns (seed 7). The page's pytest command with QF_SEED=7 gave 484 passed."},
]

now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
rows = []
for rid, prow in prev_rows.items():
    if rid in R10:
        status, location, evidence = R10[rid]
        row = {"id": rid, "check": prow["check"], "location": location, "status": status, "evidence": evidence}
    else:
        raise SystemExit(f"round 9 row {rid} has no round 10 decision")
    if status != "PASS":
        row["fix"] = {
            "proj-plan-file-names": "Update plans/PC3-build-plan.md Required outputs and grading lines (policy.py, pnl.py) to market_maker.py (quote and replay in one module) or mark the plan superseded for PC3.",
        }[rid]
    rows.append(row)
for row in NEW_ROWS:
    if row["status"] != "PASS":
        row["fix"] = {
            "proj-grader-state-between-turns": "Add the direct-call test described in the evidence (reload, then compare a call on a hand-built state with a fresh module).",
            "proj-rubric-ladder-gap-c3-difference-no-unit": "Reword C3 level 3 to 'gives the P&L of both runs, without the change reported in cents'.",
            "proj-rubric-ladder-gap-c5-wrong-number": "Add to C5 level 1: 'or names a check whose number is not the number replay produces'.",
            "proj-verifier-mutants-r10-new": "Kill v39 with the direct-call test (see proj-grader-state-between-turns).",
        }[row["id"]]
    rows.append(row)

mutants = []
for line in (S / "mutate_r10_0-9.out").read_text().splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    desc = re.sub(r"^Student error: ", "", desc).strip()
    desc = desc.rstrip(".") + "."
    mutants.append({"id": name, "description": desc, "killed_by": None if killed.strip() == "None" else killed.strip(), "status": status})

fragment = {
    "unit": "PC3",
    "slice": "c",
    "round": 10,
    "verifier": "independent verifier (Haiku 5.5), round 10, slice c (did not build PC3)",
    "pin": "00a84795",
    "base": "round 9 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round9.json (pin c93dd526). Delta c93dd526..00a84795 for slice c: course/modules/PC/PC3/project.html (lines 53, 623-625, 654, 658, 685), grader/test_project.py (line 22 import; reload test lines 411-426), course/modules/PC/PC3/index.html (lines 37, 167), ledgers/PC3/mutants v35-v38 (committed in r9 pin fixes). Not changed: engine.py, instance.py, reference.py, starter.py, tests/labs/PC3, alternatives, grader.js, plans/PC3-build-plan.md, notation, references.json, L04.html.",
    "checkout": str(ROOT),
    "scratch": "/tmp/pc3c-r10-* (collect, strict, starter, twin, cmd) and ledgers/PC3/scripts/PC3-c-r10/ for every kept script",
    "verified_at": now,
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Gates on pin 00a84795 (scripts under ledgers/PC3/scripts/PC3-c-r10/): check_pages, check_dag, check_projects PASS (PC3); "
        "run_labs PC3 project 3/3; run_graders PC3 0-49 reference 50/50; page_smoke PC3 project PASS (in-browser 493 on seed 1021546817); "
        "run_labs twins alone under python -I -W error exit 0 (twin_project_1..3.exit); ruff check and format PASS; mypy --no-incremental PASS (385 files); "
        "mypy --strict on grader and labs PASS in a scratch copy with reference.py as market_maker.py (the in-repo run reports import-not-found for the student module, expected); "
        "pytest -k PC3 9 passed; verify_refs --offline 560 entries 0 problems; collect 484 for seeds 0,1,7,49 and 493 for 50, 848197495, 1712259056. "
        "Mutants: mutate_graders --unit PC3 --seeds 0-9 on 51 mutants (m01-m10, v01-v26, v27-v38, v39-v42): 50 killed, 1 survived (v39). "
        "Alternatives: 34 alternative correct implementations in slice c pass on seeds 0,7,49,50,848197495,1712259056 (r10_alts_6seeds.out); the reload test is seed-independent. "
        "Exemplars scored blind from the passage text and the descriptors: A 4,4,4,3,4 (official 4,4,4,3,4), B 2,2,1,2,1 (official 2,2,1,2,1). Disclosure: the annotation block of exemplar A (lines 651-660) appeared in a diff printed before the scores were written. "
        "Non-FAIL observation: C2 level 3 reads 'two turns' while level 4 reads 'at least three'; read cumulatively, the ladder is consistent (proj-rubric-c2-level3-admits-mismatch). "
        "Not checked: the browser UI of the self-assessment form (JavaScript, not in slice c's gates); the cards (not in slice c); the hub's lesson hours beyond the 14-hour arithmetic."
    ),
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = (
    f"PC3-c round 10: verdict FAIL. Rows {len(rows)}: PASS {counts['PASS']}, FAIL {counts['FAIL']}, UNVERIFIABLE {counts['UNVERIFIABLE']}. "
    "FAIL rows: proj-plan-file-names (plan still names policy.py and pnl.py), proj-grader-state-between-turns (v39 survives: stated 'keeps nothing between turns' is not tested by a direct call), "
    "proj-rubric-ladder-gap-c3-difference-no-unit (C3 passage with both runs and an unitless difference fits no level), proj-rubric-ladder-gap-c5-wrong-number (C5 check with a wrong number fits no level), "
    "proj-verifier-mutants-r10-new (v39 survivor). Closed since round 9: proj-rubric-ladder-gap-c2, proj-rubric-ladder-gap-c3-other-seed, proj-hours-arithmetic, proj-grader-determinism-quote-state, proj-exemplar-a-c5-annotation, proj-verifier-mutants-r9-new. "
    f"Mutants: {sum(1 for m in mutants if m['killed_by'])} of {len(mutants)} killed."
)
out = ROOT / "ledgers/PC3/PC3-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n")
print("wrote", out, "rows", len(rows), counts, "mutants", len(mutants))
