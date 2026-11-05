"""Build the round-7 slice-c fragment from the outputs of this round's runs (no repo file other than the fragment is written)."""
import json
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE7-PC3-c"
S = f"{ROOT}/ledgers/PC3/scripts/PC3-c-r7"

mutants = []
for line in open(f"{S}/mutate_default_0-9_with_new.out", encoding="utf-8"):
    m = re.match(r"(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line.strip())
    if not m:
        continue
    status, name, desc, killed = m.groups()
    desc = desc.replace("Student error: ", "").rstrip(".")
    entry = {
        "id": name[:-3],
        "file": f"ledgers/PC3/mutants/{name}",
        "description": desc,
        "killed_by": None if killed.strip() == "None" else killed.strip(),
        "status": status,
    }
    mutants.append(entry)

R = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)

# ---- FAIL rows (project unit defects, with evidence) ----
row("proj-zero-fill-replay", "2.6-grader (mutation survivor; stated behaviour of replay)",
    "course/modules/PC/PC3/project.html line 393 (Required outputs: replay returns exactly the four keys with pnl = cash flow + mark); "
    "course/modules/PC/PC3/grader/test_project.py (no test replays a log without a fill); ledgers/PC3/mutants/v27_replay_divides_by_the_number_of_fills.py",
    "FAIL",
    "Command (pytest collect/run, scratch copy): a 20-turn log with every turn unfilled (size 0) passed to v27's replay raises ZeroDivisionError "
    "('division by zero'). QF_SEED=0 and QF_SEED=7 with v27 as market_maker.py: '432 passed'. mutate_graders output "
    "(ledgers/PC3/scripts/PC3-c-r7/mutate_default_0-9_with_new.out): SURVIVED v27. A 20-turn log with no fills is not one of the four invalid "
    "inputs the page names (project.html lines 410-419: 'Any other invalid input may raise ... or return'), so replay must return the zero record for it.",
    "Add a test in test_project.py: a hand-built 20-turn log with every turn filled false and fill_price_cents None (or an engine log from a size-0 quote on seed 0) "
    "must give cash_flow_cents 0, inventory_end 0, inventory_mark_cents 0, pnl_cents 0 with no exception; then re-run mutate_graders --unit PC3 and confirm v27 is killed.")
row("proj-rubric-observable", "2.6-rubric (every level descriptor observable)",
    "course/modules/PC/PC3/project.html line 627 (C5 level 3 'Names one check and its result, without a value') against line 627 level 4 ('gives its printed or computed result')",
    "FAIL",
    "Blind reading of the rubric: for a boolean check such as the identity (result 'holds' or 'True'), the phrase 'without a value' and the phrase 'printed or computed result' "
    "cannot be separated; a scorer cannot tell whether naming the identity result is level 3 or level 4. The round-6 scope note called this ambiguous and it is unchanged.",
    "Replace the level 3 and level 4 wording with observable criteria, for example level 3: 'names one check and its result as a word (holds or fails), with no number'; level 4: 'names one check and gives the number it computed or printed (for example 30 = -9950 + 9980)'.")
row("proj-rubric-ladder-gap-c1", "2.6-rubric (ladder covers every submission)",
    "course/modules/PC/PC3/project.html line 623 (C1 levels 1-4)",
    "FAIL",
    "A submission that states cash_flow_cents, inventory_mark_cents and pnl_cents, each equal to replay, and names no turns: level 4 needs the turns for both parts; level 3 needs the turns that produced the cash flow; "
    "level 2 is 'states the P&L and one component' (this submission states two components); level 1 is 'states a result without its components' (this one states them). No level matches.",
    "Level 2: 'states the P&L and at least one component, each equal to the output of replay' (then level 3 needs the three values with the cash-flow turns named).")
row("proj-rubric-ladder-gap-c3", "2.6-rubric (ladder covers every submission)",
    "course/modules/PC/PC3/project.html line 625 (C3 levels 1-4)",
    "FAIL",
    "A submission that states one change with its amount in cents and reruns seed 0 but reports neither run's P&L nor the difference: level 3 needs 'the P&L of both runs'; level 2 is 'gives no rerun' (this submission reran); "
    "level 1 is 'without its amount in cents' (this one gives it). No level matches.",
    "Level 2: 'states one change with its amount in cents and reruns the same seed, without the P&L of either run' or give level 2 the rerun-without-numbers case explicitly.")
row("proj-grader-35-checks", "2.6-spec (count claim equals real collect-only count)",
    "course/modules/PC/PC3/project.html line 397 ('The autograder runs 440 checks ... 440 for any seed outside 0 to 49, and 432 for seed 0'; 'Eight checks run on each of 52 seeds')",
    "FAIL",
    "ledgers/PC3/scripts/PC3-c-r7/collect_counts_c_r7.out: collect-only QF_SEED=0, 1, 7, 49 give '432 tests collected'; QF_SEED=50 and 848197495 give '440 tests collected'; "
    "the reference run gives 432 passed (seed 0) and 440 passed (seed 848197495); page_smoke_project.out also reports 440. The sentence covers seed 0 and seeds outside 0 to 49 but not seeds 1 to 49, which give 432. "
    "'52 seeds' is wrong for seeds 0 to 49: those seeds form a set of 51 distinct seeds (0..49 plus seed + 7919), and outside it 52. 8 x 51 + 24 = 432; 8 x 52 + 24 = 440.",
    "Write: '432 checks for any seed from 0 to 49, 440 for any other seed. Eight checks run on each distinct seed of the set: 51 seeds for a seed from 0 to 49, 52 otherwise.'")
row("proj-starter-docstring-raise-scope", "2.6-spec (wording matches the named-invalid-input contract)",
    "course/modules/PC/PC3/grader/starter.py lines 8-9 ('Every input the specification names as invalid must raise ValueError.') against project.html lines 410-419 ('The engine raises ValueError for the first two conditions, and your replay for the last two.')",
    "FAIL",
    "Reading both texts: the starter tells a learner that quote must raise for a crossed or oversized quote; the page assigns those two refusals to the engine, and the suite does not require quote to raise (test_project.py lines 173-196 use the engine). "
    "Low severity: the suite behaviour is correct; the starter sentence is inaccurate.",
    "Reword starter.py line 8: 'Every input to replay that the specification names as invalid must raise ValueError; the engine refuses an illegal quote.'")
row("proj-plan-file-names", "2.6-spec (file contract matches the plan)",
    "course/modules/PC/PC3/project.html line 393 (market_maker.py), line 429-430 and 442; grader/test_project.py line 29 (import market_maker) and grader/starter.py line 1; against plans/PC3-build-plan.md lines 337-340 (policy.py quote, pnl.py replay) and 348, and the Q1 default at line 577",
    "FAIL",
    "Plan 5.2 names policy.py and pnl.py as the required outputs; plan 5.6 names the same files for the reference; the architect decisions (plan line 627) say a stated recommendation is followed, and Q1's recommendation (line 577) is policy.py / pnl.py. "
    "grep of plans/FINAL-ARCHITECT-RULINGS.md shows no ruling that changes the file names. The page and suite use market_maker.py throughout, so the built contract differs from the plan's binding one.",
    "Rename the learner module contract to policy.py (quote) and pnl.py (replay) across project.html, grader/test_project.py, grader/starter.py, grader/reference.py and the hub, or record a written architect ruling that approves market_maker.py.")
row("proj-hub-filenames", "2.4-structure (hub and project name the same files)",
    "course/modules/PC/PC3/index.html lines 160 and 167 (policy.py, pnl.py) against project.html line 393 (market_maker.py); cross-slice (index.html belongs to the hub slice)",
    "FAIL",
    "index.html line 160 'Write policy.py, the quoting rule, and pnl.py'; line 167 'The autograded policy.py and pnl.py take 6 hours'. project.html line 393 and 442 require market_maker.py. Unchanged since round 6 (index.html changed only lines 159 and 167 in 4bd8cb9..06994db).",
    "Make the hub and the project name the same files (see proj-plan-file-names).")
row("proj-hub-skill-check-premise", "2.2-numbers (hub skill-check premise is consistent with the game)",
    "course/modules/PC/PC3/index.html line 129 ('a market maker buys one unit at an ask of 10 005 cents'; answer -10005) against project.html Trades and Cash bullets (lines 405-406: a maker purchase is at the bid b, changes cash by -b)",
    "FAIL",
    "In the game, a maker purchase is a fill at the bid (project.html line 406; engine.py maker_side and play, lines 83-86); a fill at the ask is a sale by the maker. The hub's premise (buy at an ask) has no fill in the game, so the stated answer is not a game cash flow. Cross-slice: owned by the hub slice.",
    "Change the hub skill-check premise to a purchase at a bid (for example 'a market maker buys one unit at a bid of 10 005 cents', answer -10005) and re-run check_pages.")

# ---- PASS rows ----
row("proj-exemplar-a-numbers", "2.2-numbers",
    "course/modules/PC/PC3/project.html lines 635-662 (exemplar A, P&L decomposition and evidence)",
    "PASS",
    "ledgers/PC3/scripts/PC3-c-r7/indep_numbers_c_r7.out: bids 9990+9980+9970+9980+9990 = 49910, asks 9980+9990+9990+10000 = 39960, cash -9950; identity 30 = -9950 + 1*9980 True; fill turns [2,3,4,5,7,8,13,18,19] equal Lab 1 output (run by the twin, labs_page_vs_twin_c_r7.out).")
row("proj-lab1-replay-prints", "2.5-labs",
    "course/modules/PC/PC3/project.html Lab 1 section (line 55 onward) and tests/labs/PC3/lab-PC3-project-1.py",
    "PASS",
    "ledgers/PC3/scripts/PC3-c-r7/labs_page_vs_twin_c_r7.out: page code IDENTICAL to twin (0 diff lines); twin run with python -I -W error exits 0 with 0 stderr bytes; expected block == twin output.")
row("proj-lab1-run", "2.5-labs", "project.html lab-PC3-project-1 (rung 1)", "PASS",
    "tools/run_labs.py --unit PC3 --page project: 'run_labs PC3: PASS (3/3)' (ledgers/PC3/scripts/PC3-c-r7/run_labs_project.out).")
row("proj-lab1-hypothesis-numbers", "2.2-numbers", "project.html line 57 (Lab 1 hypothesis)", "PASS",
    "Hypothesis states 9 fills, cash flow -9950, inventory 1, settlement 9980, mark 9980, P&L 30, limit 10 not passed. Twin output shows 'fills = 9 of 20 turns', -9950, 1, 9980, 9980, 30, 'largest |inventory| ... = 3 (limit 10): True'. indep_numbers_c_r7.out agrees.")
row("proj-lab2-completion", "2.5-labs",
    "project.html lab-PC3-project-2 (lines 242-290 region: page code blanks at cash_flow and mark)", "PASS",
    "labs_page_vs_twin_c_r7.out: the only differences from the twin are the two lines 'cash_flow = ___' and 'mark = ___' (completion rule); expected block equals twin output (cash -9950, inventory 1, mark 9980, P&L 30, identity True).")
row("proj-lab2-interpretation-last-quote", "2.2-numbers", "project.html Lab 2 interpretation paragraph", "PASS",
    "With inventory 1 the P&L is cash flow + 1 * settlement, so a mark at another price changes the P&L one for one; the interpretation's claim holds by the identity (project.html Conventions, The P&L).")
row("proj-lab3-counterfactual", "2.2-numbers", "project.html lines 457-612 (Lab 3)", "PASS",
    "Twin output: fills 9 of 20, counterfactual pnl 55, change 25 cents. indep_numbers_c_r7.out: half-spread 15 gives fills 9, cash -9925, P&L 55; change 25. Hypothesis (line 459) agrees.")
row("proj-lab3-interpretation", "2.2-numbers", "project.html Lab 3 interpretation paragraph", "PASS",
    "Interpretation names the first block (settlement, fills, four numbers, identity, cash agreement) and the three counterfactual lines; the expected block has exactly these lines (labs_page_vs_twin_c_r7.out).")
row("proj-rung1-instance-claim", "2.8-data / 2.6-spec", "project.html line 391 (Inputs) and grader/instance.py lines 27-53", "PASS",
    "ledgers/PC3/scripts/PC3-c-r7/instance_match_c_r7.out: 0 mismatches for seeds 0-49 between make_instance and an independent generator written from the stated draw order (move, then arrival). engine.play matches the independent run on fills and cash for seeds 0-49 (0 mismatches).")
row("proj-conventions-constants", "2.2-numbers", "project.html Conventions lines 402-407 and Required outputs line 393", "PASS",
    "N = 20, v0 = 10000, +/-5 cents, size max 5, limit 10 match engine.py (MAX_SIZE=5, LIMIT=10) and instance.py (START_CENTS=10000, MOVE_CENTS=5); arrival probabilities 1/4, 1/4, 1/2 match L04.html A1 (line 64).")
row("proj-exemplar-a-calibration", "2.6-rubric (blind calibration)", "project.html lines 635-662 (exemplar A) against rubric lines 623-627", "PASS",
    "Blind scoring from the rubric alone: C1 4 (three values, turns named for both parts), C2 4 (turns 2, 5, 18 with fields, values match), C3 4 (change with amount, rerun, change in cents), C4 3 (three of four items), C5 4 (identity and cash agreement, computed). Annotations data-scores 4,4,4,3,4 (line 635). Within one level on every criterion.")
row("proj-exemplar-b-calibration", "2.6-rubric (blind calibration)", "project.html lines 664-690 (exemplar B) against rubric", "PASS",
    "Blind scoring: C1 2, C2 2, C3 1, C4 2, C5 1 against data-scores 2,2,1,2,1 (line 664). Within one level on every criterion.")
row("proj-exemplar-b-numbers", "2.2-numbers", "project.html exemplar B passages (lines 664-690)", "PASS",
    "P&L 30 and cash flow -9950 equal the replay output (Lab 1); turn 5 sold at the ask of 9980 cents matches Lab 1 output line 'turn  5: maker sells at the ask 9980 cents'.")
row("proj-exemplar-b-arrival-sensitivity", "2.2-numbers", "project.html exemplar B assumptions passage and annotation (line 687)", "PASS",
    "Arrival probabilities 1/4, 1/4, 1/2 are stated as model choices (L04.html A1, line 64); annotation 'names the arrival probabilities without saying which result depends on them' is consistent with the passage.")
row("proj-rubric-c2-level3-admits-mismatch", "2.6-rubric", "project.html line 624 (C2 levels 2 and 3)", "PASS",
    "Level 3 now reads 'cites two turns by number and field, and every cited value matches the log'; a cited mismatch falls to level 2 ('or cites one or more turns with at least one cited value that does not match the log'). The round-6 inversion is gone.")
row("proj-rubric-c4-real-form-undefined", "2.6-rubric / 2.14-DAG", "project.html line 626 (C4 level 4) against L04.html line 465", "PASS",
    "C4 level 4 names the queue of resting orders and a trader who learns from the fills. L04.html line 465 sets both aside ('this game does not model that queue'; 'this lesson does not model learning'). The plan's example list differs only in its examples.")
row("proj-spec-log-schema", "2.6-spec", "project.html line 393 (log keys) against grader/engine.py lines 87-100", "PASS",
    "Log keys seed, settlement_cents, turns; turn keys turn, bid_cents, ask_cents, size, arrival, filled, fill_price_cents, inventory_after, cash_after_cents. engine.play returns exactly these (verified by the replay and oracle tests).")
row("proj-hours-arithmetic", "2.9-hours", "project.html lines 422-434 (Time budget); index.html line 167", "PASS",
    "Components 1+1+3+2+2+4+1 = 14; 14/50 = 28 percent, matching the hub. Own estimate: rungs 1-2 about 2 h, quote 3-5 h, replay 1-2 h, autograder fixes 1-2 h, analysis 3-4 h, self-assessment 1 h: 11-16 h, within 30 percent of 14.")
row("proj-hub-placement-conflict", "2.4-structure", "project.html lines 42-48 against index.html line 156", "PASS",
    "Both say a student who reaches the placement bar and answers both skill checks skips rungs 1 and 2.")
row("proj-hub-seed-scope", "2.6-spec", "index.html lines 55 and 160 against project.html line 397 and grader/test_project.py lines 36-37", "PASS",
    "The suite now runs its eight seed checks on the fixed seeds 0 to 49, the learner seed and seed + 7919 (FIXED_SEEDS = range(50)); the hub's 'seeds 0 to 49' is consistent with it.")
row("proj-quote-rule-first-fill-survivor", "2.7-alternatives", "project.html line 429 (time row for quote); ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py", "PASS",
    "alt6 (mid from the first fill) passes 50/50 seeds (alts_all_r7.out). The quote rule is a legal choice; none is required to earn a particular P&L.")
row("proj-builder-mutants", "2.6-mutants", "ledgers/PC3/mutants/m01..m10 (builder mutants)", "PASS",
    "mutate_graders --unit PC3 (default seeds 0-9, ledgers/PC3/scripts/PC3-c-r7/mutate_default_0-9.out): m01-m10 KILLED.")
row("proj-verifier-mutants", "2.6-mutants", "ledgers/PC3/mutants/v01..v26", "PASS",
    "Same run: all v01-v26 present in the run are KILLED, including v24, v25 and v26 that survived in round 6 (stderr, stale totals, logging warning).")
row("proj-mutant-m08-description", "2.6-mutants", "ledgers/PC3/mutants/m08_hard_coded_answer_for_any_log.py line 1", "PASS",
    "Docstring first line: 'Student error: replay returns all zeros, a hard-coded answer, for every log.' KILLED by test_replay_agrees_with_the_engine_final_cash_and_inventory[34] (seed 0).")
row("proj-verifier-mutants-r3-new", "2.6-mutants", "ledgers/PC3/mutants/v13..v16", "PASS",
    "All four KILLED in mutate_default_0-9.out.")
row("proj-alternatives-1-2-4-5", "2.7-alternatives", "ledgers/PC3/alternatives/alt1, alt2, alt4, alt5", "PASS",
    "alts_all_r7.out: each passes 50/50 seeds with the page's flags (-W error, --assert=plain).")
row("proj-alt3-replay", "2.7-alternatives", "ledgers/PC3/alternatives/alt3_inventory_skew.py", "PASS", "alts_all_r7.out: 50/50.")
row("proj-alternative-6", "2.7-alternatives", "ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py", "PASS", "alts_all_r7.out: 50/50.")
row("proj-alternative-7-8-verifier", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r2/alt7, alt8", "PASS", "alts_all_r7.out: 50/50 each.")
row("proj-alternative-9-10-verifier-r3", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r3/alt9, alt10", "PASS", "alts_all_r7.out: 50/50 each.")
row("proj-alternatives-r4-new", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r4/alts/alt11, alt12, alt13", "PASS", "alts_all_r7.out: 50/50 each.")
row("proj-alternatives-r7-new", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r7/alts/alt20..alt24 (written this round)", "PASS",
    "alts_all_r7.out: alt20 (class maker, constant quote), alt21 (reverse scan, throttle at |inventory| 8), alt22 (inventory shift, size 5, dict accumulator), alt23 (closure quoter, while-loop replay), alt24 (parity half-spread, size growth): each 50/50. No over-constraint found.")
row("proj-grader-seed-scope-claim", "2.6-spec", "project.html line 397 (membership of the seed sets) against grader/test_project.py lines 36-37 and collect-only", "PASS",
    "The eight seed checks run on 0..49, the learner seed and seed + 7919; the 24 other checks run on the learner seed or on none; collect-only counts 24 non-seed tests and 8 seed-parametrised tests (432 for seed 0). Only the numeric wording is wrong (proj-grader-35-checks).")
row("proj-grader-no-print", "2.6-spec", "project.html line 395 ('Neither quote nor replay prints or warns'); grader/test_project.py lines 378-389", "PASS",
    "test_no_function_prints_or_warns checks stdout and stderr, caplog records, and warnings. v24 (stderr print), v26 (logging.warning) are now KILLED by it (mutate_default_0-9.out).")
row("proj-grader-replay-from-fills", "2.6-spec", "project.html Conventions 'The P&L' (line 407); test_project.py lines 228-241 and 261-271", "PASS",
    "The replay tests use an oracle built from the fills alone (lines 72-83) and check exact equality with the replay on fixed and student logs.")
row("proj-grader-mypy-strict", "2.6-lint", "course/modules/PC/PC3/grader/engine.py, instance.py, reference.py, test_project.py; tests/labs/PC3 project twins", "PASS",
    "ledgers/PC3/scripts/PC3-c-r7/mypy_strict_grader_labs_c_r7.out: mypy --strict on the grader set with a solution module present: 'Success: no issues found in 4 source files'; repo mypy --no-incremental: 385 source files, success (run_gates gate output). Without a solution module the suite reports import-not-found, which is expected.")
row("proj-grader-reference", "2.6-grader", "course/modules/PC/PC3/grader/reference.py", "PASS",
    "run_graders PC3 --seeds 0-49: 'reference 50/50 seeds, slowest 0.3 s'; pytest with reference as market_maker.py: 432 passed (seed 0), 440 passed (seed 848197495).")
row("proj-grader-starter-fails", "2.6-grader", "course/modules/PC/PC3/grader/starter.py", "PASS",
    "starter as market_maker.py with QF_SEED=0: 366 failed, 66 passed; failures are NotImplementedError from quote/replay (suite must fail on it).")
row("proj-grader-instances", "2.8-data", "grader/instance.py; test_project.py lines 414-418", "PASS",
    "All 50 fixed-seed instances are valid (21 positive values starting at 10000, 20 arrivals with the three names) and 50 distinct fair paths (indep_numbers_c_r7.out, instance_match_c_r7.out). Sampled 50, not 20.")
row("proj-grader-messages", "2.6-grader", "grader/test_project.py lines 44-59 and every expect() message", "PASS",
    "All 469 lines read. Failure messages name the property; none print a computed expected value (must_refuse prints only the named phrase; engine messages print the turn number).")
row("proj-named-refusals", "2.6-spec", "project.html lines 410-419; test_project.py lines 173-221", "PASS",
    "Four named conditions: crossed quote, size outside 0..5, log not 20 turns, filled turn without price. Engine message 'turn N: bid must be below ask' contains the named phrase; replay messages are exact.")
row("proj-exception-types", "2.6-spec", "test_project.py must_refuse calls (lines 173-221)", "PASS",
    "must_refuse is used only for the four named conditions; no other test requires an exception type.")
row("proj-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3 --page project", "PASS", "'run_labs PC3: PASS (3/3)'.")
row("proj-check-tools", "2.6-gates", "tools/check_pages.py --all; check_dag.py --all; check_projects.py --all", "PASS",
    "ledgers/PC3/scripts/PC3-c-r7/check_pages.out, check_dag.out, check_projects.out: 'PC3: PASS' and exit 0.")
row("proj-page-smoke", "2.5-labs / 2.6-grader", "tools/page_smoke.py --unit PC3 --pages project", "PASS",
    "page_smoke_project.out: PASS; in-browser grader 'All 440 tests pass on seed 848197495'.")
row("proj-lint-ruff", "2.6-lint", "ruff check and format on course/modules/PC/PC3/grader and tests/labs/PC3", "PASS",
    "ruff_check.out 'All checks passed!'; ruff_format.out '14 files already formatted'. ledgers/*/mutants are excluded by pyproject (extend-exclude).")
row("proj-mypy-labs", "2.5-labs", "mypy --no-incremental (repo config includes tests)", "PASS", "mypy_repo.out: 'Success: no issues found in 385 source files'.")
row("proj-banned-and-process-words", "2.6-prose", "project.html text and grader/*.py", "PASS",
    "grep for verifier, builder, architect, planner, fixer, draft, TODO, ledger, blueprint, DATA_REQUEST: no match in learner text.")
row("proj-notation", "2.4-notation", "notation/notation.json (symbols T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q) against project.html math", "PASS",
    "No registered symbol is used on the page with another meaning; page-local symbols (N, v_t, b_t, a_t, q_t, I, pnl) are defined in Conventions and the Rungs section.")
row("proj-dag-terms", "2.14-DAG", "project.html concept links (one: market-making-game) against L04.html line 60 dfn", "PASS",
    "The only concept link resolves to the in-unit definition (L04.html line 60, dfn id def-market-making-game). Adverse selection, martingale and Bayes are not used on the page.")
row("proj-references", "2.1-citations", "project.html reading list (data-cite) and references; verify_refs --offline", "PASS",
    "verify_refs_offline: '560 entries, 0 problems'. Reading list uses data-cite only; no bibliographic data typed; no claim attributed to either book.")
row("proj-js-claims", "2.6-grader / 2.4-prose", "project.html grader section (line 440 onward) and self-assessment section (id self-assessment, line ~690); course/assets/js/grader.js lines 61, 72, 79; rubric.js line 8; store.js", "PASS",
    "Draft code is saved with store.put on a 400 ms debounce (grader.js lines 61, 72, 79); rubric scores go through store.js (rubric.js line 8 and saveRecord). The statements 'saved in this browser' and 'scores stay in this browser' are supported by source. Not run in a real browser (see notes).")
row("proj-local-commands", "2.6-grader", "project.html lines 446-455 (local pytest) and lines 392-393 (game_log command)", "PASS",
    "QF_SEED=0 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py: '432 passed'. The game_log command as written (python3 -c with engine and market_maker) writes a 20-turn log for seed 3.")
row("proj-known-limitation", "2.6-spec", "project.html line 395 (Known limitation)", "PASS",
    "Limitation matches the plan's B3 and the suite: no test can tell a rule that reads instance.py; the page says so.")
row("proj-ladder-scope", "2.6-spec", "project.html ladder lines 40-50; rung 3 spec line 388 onward", "PASS",
    "Rung 1 fully solved and annotated; rung 2 completion graded by the completion rule; rung 3 terms in plan order (Context, Inputs, Required outputs, Constraints, Grading mode); rung 4 not graded.")
row("proj-rubric-atlas-studios", "2.6-atlas/studio", "project.html (no Atlas or studio text) and plan 'no Atlas milestone'", "PASS",
    "grep: no atlas or studio reference on the page; the plan declares no Atlas milestone for PC3.")
row("proj-stretch", "2.6-spec", "project.html lines 702-710 (Rung 4)", "PASS", "Rung 4 is not graded and no test depends on it; it names no seeds beyond the plan's 0 to 199.")
row("proj-twin-rules", "2.5-labs", "tests/labs/PC3/lab-PC3-project-1..3.py", "PASS",
    "Each twin: standard library only (random, typing), seeded random.Random(0), no network; python -I -W error exit 0, stderr 0 bytes; run time 0.0 s (page_smoke).")
row("proj-exception-types-labs", "2.5-labs", "project labs", "PASS", "No lab raises or catches an exception; all three exit 0 under python -I -W error.")
row("proj-r4-new-mutants-v18-v20", "2.6-mutants", "ledgers/PC3/mutants/v18..v20", "PASS", "All three KILLED (mutate_default_0-9.out).")
row("proj-grader-window-distinct-paths", "2.6-grader", "test_project.py lines 414-418", "PASS", "50 distinct fixed-seed paths; test passes on the reference (432 passed).")
row("proj-grader-v21-replay-scales-by-size", "2.6-mutants", "ledgers/PC3/mutants/v21_replay_scales_each_fill_by_quoted_size.py", "PASS", "KILLED by test_a_fill_is_one_unit_whatever_its_quoted_size (seed 0).")
row("proj-grader-v22-zero-fill-price-refused", "2.6-mutants", "ledgers/PC3/mutants/v22_replay_refuses_a_zero_fill_price.py", "PASS", "KILLED by test_a_fill_at_price_zero_is_a_legal_fill (seed 0).")
row("proj-exemplar-levels-vs-plan", "2.6-rubric / plan", "project.html line 635 (exemplar-a data-level=4) and line 664 (exemplar-b data-level=2) against plans/PC3-build-plan.md line 380", "PASS",
    "Round 6 FAIL is fixed: exemplar-a is data-level 4 and exemplar-b is data-level 2, as plan line 380 states.")
row("proj-instance-engine-names", "2.6-spec", "grader/instance.py make_instance (line 27); grader/engine.py play(quote, seed) (line 49)", "PASS",
    "make_instance(seed) matches plan 5.6 and the page. engine.play takes the quote function rather than plan 5.3's policy module; the page's command uses engine.play(market_maker.quote, seed), consistent with the engine. Naming is covered under proj-plan-file-names.")
row("proj-r5-mutant-v23-first-fill-price", "2.6-mutants", "ledgers/PC3/mutants/v23_replay_marks_at_the_first_fill_price.py", "PASS", "KILLED by test_pnl_is_cash_flow_plus_inventory_times_settlement[26] (seed 0).")
row("proj-r5-alternatives-14-16", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r5/alts/alt14, alt15, alt16", "PASS", "alts_all_r7.out: 50/50 each.")
row("proj-r5-labs-page-vs-twin", "2.5-labs", "project labs page code vs twin", "PASS", "labs_page_vs_twin_c_r7.out: identical except the two completion blanks (Lab 2).")
row("proj-grader-v24-stderr-print-survives", "2.6-mutants", "ledgers/PC3/mutants/v24_replay_prints_a_debug_line_to_stderr.py", "PASS", "Round 6 survivor now KILLED by test_no_function_prints_or_warns (seed 0), mutate_default_0-9.out.")
row("proj-grader-v25-last-filled-totals-survives", "2.6-mutants", "ledgers/PC3/mutants/v25_replay_takes_totals_from_last_filled_turn.py", "PASS", "Round 6 survivor now KILLED by test_stale_totals_on_the_last_filled_turn_are_not_used (seed 0): the new two-fill hand-built log exposes the stale totals.")
row("proj-grader-v26-logging-warning-survives", "2.6-mutants", "ledgers/PC3/mutants/v26_quote_logs_a_warning_through_logging.py", "PASS", "Round 6 survivor now KILLED by test_no_function_prints_or_warns (caplog check).")
row("proj-plan-grader-seed-scope", "2.6-spec", "plans/PC3-build-plan.md lines 348 and 380-ff (dual mode on seeds 0-49) against test_project.py lines 36-37", "PASS",
    "The legality, replay, cash and P&L checks now run on fixed seeds 0 to 49 (SEEDS includes range(50)); the round-6 FAIL is fixed. The file-name deviation is recorded under proj-plan-file-names.")
row("proj-verifier-mutants-r7-new", "2.6-mutants", "ledgers/PC3/mutants/v27..v30 (written by this verifier)", "FAIL",
    "v28, v29, v30 KILLED; v27 SURVIVED (zero-fill log raises ZeroDivisionError). See proj-zero-fill-replay for the defect and the fix.",
    "Add the zero-fill test named in proj-zero-fill-replay, then re-run mutate_graders --unit PC3.")

notes = (
    "Round 7 slice c. Pin 06994db (checkout /Users/billyribeiro/.fanout/wt/verifyE7-PC3-c, detached). "
    "Delta from round 6 (4bd8cb9): project.html (exemplar levels, C2 level 3, rubric wording, count sentence, seed-set sentence), grader/test_project.py (FIXED_SEEDS range(50); new tests for stale totals and no-print), starter.py (docstring), mutants v24-v26 (round-6 survivors now killed), no change to alternatives or to index.html beyond two hub lines. "
    "All project.html lines read (732), grader engine.py, instance.py, reference.py, starter.py and all 469 lines of test_project.py read. Three project twins read and run. "
    "Gates run once on the pin (ledgers/PC3/scripts/PC3-c-r7/run_gates_c_r7.sh): check_pages, check_dag, check_projects PASS; run_labs project 3/3; run_graders 0-49 reference 50/50; page_smoke PASS (440 in browser on seed 848197495); ruff check and format PASS; mypy --no-incremental PASS; verify_refs --offline 560 entries, 0 problems; pytest -k PC3 passed. "
    "Mutants: mutate_graders --unit PC3 default seeds 0-9 on the 35 existing mutants: 35/35 KILLED (ledgers/PC3/scripts/PC3-c-r7/mutate_default_0-9.out); also 0-49: 35/35 KILLED. With 4 new verifier mutants (v27-v30): 38/39 KILLED; v27 survives. "
    
    "Cross-slice (not my rows, reported for the hub owner): index.html line 160 and 167 name policy.py and pnl.py (the project uses market_maker.py); index.html line 129 skill-check premise (buy at an ask) conflicts with the game (a maker purchase is at the bid). "
    "Tool note (not a page defect): mutate_graders attributes m09 to test_a_log_carries_its_own_seed_and_settlement[28]; a direct pytest run of the same mutant fails first in test_quotes_are_legal_on_every_turn[0]. The kill stands either way. "
    "Not checked: a real browser render of the grader panel and rubric form (source read only; page_smoke ran the suite in its runner); the full repo pytest suite (only -k PC3); the Pyodide runtime beyond page_smoke; learner seeds outside 0-49 beyond seeds 848197495 and 50; render_curriculum, build_site --check and fetch_data --check (outside slice c); the L04 lab twin and cards (other slices)."
)

summary = (
    "PC3-c round 7: verdict FAIL. Rows: 82 total, 72 PASS, 10 FAIL. Mutants: 39 listed (35 builder and round-5/6 verifier mutants plus v27-v30 this round), 38 killed, 1 survived (v27: replay crashes on a valid no-fill log; the suite has no such test). "
    "Alternatives: 24 correct implementations, all 24 pass on 50/50 seeds. Count claim, rubric ladder gaps (C1, C3), C5 wording, starter docstring scope, plan file-name contract (market_maker.py vs policy.py/pnl.py), and the no-fill replay gap are the FAIL rows; hub rows proj-hub-filenames and proj-hub-skill-check-premise are cross-slice FAILs."
)

frag = {
    "unit": "PC3",
    "slice": "c",
    "round": 7,
    "verifier": "independent verifier (Haiku 5.5), round 7, slice c (did not build PC3)",
    "pin": "06994db",
    "base": "round 6 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round6.json (pin 4bd8cb9). Delta 4bd8cb9..06994db for slice c: project.html, grader/test_project.py, grader/starter.py, mutants v24-v26 (round 6 survivors), tests/labs/PC3 L04 twin (not slice c, read only for the L04 hunk check: no effect on slice c).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-PC3-c",
    "scratch": "/tmp/pc3c-r7-* (collect, mypy, mutant scratch copies); scripts and outputs in ledgers/PC3/scripts/PC3-c-r7",
    "verified_at": "2026-11-04T18:30:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}
with open(f"{ROOT}/ledgers/PC3/PC3-c.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(R), "PASS", sum(r["status"] == "PASS" for r in R), "FAIL", sum(r["status"] == "FAIL" for r in R), "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
