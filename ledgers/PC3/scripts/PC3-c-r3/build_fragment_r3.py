"""Build ledgers/PC3/PC3-c.json (round 3) from the outputs under ledgers/PC3/scripts/PC3-c-r3/ and the mutant run."""
import json
import re
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE3-PC3-c"
S = f"{ROOT}/ledgers/PC3/scripts/PC3-c-r3"
sys.path.insert(0, f"{ROOT}/tools")
import ledger  # noqa: E402

P = "course/modules/PC/PC3/project.html"
G = "course/modules/PC/PC3/grader"
R = []


def row(rid, check, location, status, evidence, fix=None):
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    R.append(item)


# ---- rows that were FAIL in round 2 and are now PASS (re-verified from scratch)
row("proj-exemplar-a-numbers", "2.2-numbers", f"{P} line 643 (Exemplar A 'Evidence from the log')", "PASS",
    "Round-2 FAIL fixed. Sentence now reads 'Turn 5 sold at the ask of 9980 cents, and turn 18 sold at the ask of 10000 cents'. "
    "recompute_r3.out: turn 5 ask 9980 and fill 9980 (sell@ask, inv 2 after); turn 18 ask 10000 and fill 10000 (sell@ask, inv 0). Both values match the log; no count claim remains.")
row("proj-lab1-replay-prints", "2.5-labs", f"{P} Lab 1 code, replay() and main() (lines ~121-150 of the lab block)", "PASS",
    "Round-2 FAIL fixed. lab1_replay_print_check.out: the page's replay() contains 0 print calls (ast); replay output is 0 characters on seeds 0-5 and equals tp.oracle(log) on each. The per-fill print moved to main(), which reads record['inventory_after'] from the log. extract_labs.out: page code equals twin tests/labs/PC3/lab-PC3-project-1.py (0 differing lines of 161).")

# ---- lab rows
row("proj-lab1-run", "2.5-labs", f"{P} lab-PC3-project-1 (rung 1)", "PASS",
    "run_labs_project.out: 'run_labs PC3: PASS (3/3)', exit 0. python -I -W error on tests/labs/PC3/lab-PC3-project-1.py: exit 0, stderr 0 bytes. extract_labs.out: 161 page lines = 161 twin lines, 0 differing. Page output diffs empty against the expected block (lab1 output == expected, see lab1 run in this round).")
row("proj-lab1-hypothesis-numbers", "2.2-numbers", f"{P} line 57 (Lab 1 hypothesis)", "PASS",
    "recompute_r3.out (own game code from the page text): settlement 9980, 9 fills at turns 2,3,4,5,7,8,13,18,19, cash flow -9950, inventory 1, mark 9980, P&L 30, identity True, largest |inventory| 3 (limit 10). All hypothesis numbers match; expected block lines equal the printed output.")
row("proj-lab2-completion", "2.5-labs", f"{P} lab-PC3-project-2 (rung 2, completion)", "PASS",
    "extract_labs.out: the only differing lines between page code and twin are 105 'cash_flow = ___' and 106 'mark = ___'. Twin run under python -I -W error: exit 0, stderr 0; twin output diffs empty against the expected block (cash_flow -9950, inventory 1, mark 9980, P&L 30, identity True). Page code is not run (blanks), as designed.")
row("proj-lab2-interpretation-last-quote", "2.2-numbers", f"{P} line 372 (Lab 2 interpretation)", "PASS",
    "Sentence: 'With an inventory of 1 unit, a mark at any price other than the settlement value of 9980 cents changes the P&L on this seed'. P&L = -9950 + 1 x mark; recompute_r3.out: mark 9990 gives P&L 40, mark 9980 gives 30. True.")
row("proj-lab3-counterfactual", "2.2-numbers", f"{P} lines ~456-612 (Lab 3 hypothesis and expected block)", "PASS",
    "recompute_r3.out: half-spread 15 gives 9 fills, P&L 55, delta +25 cents, cash flow -9925 (same settlement, same arrivals). Hypothesis numbers and expected block lines match. run_labs PASS; twin output diffs empty against expected block.")
row("proj-lab3-interpretation", "2.2-numbers", f"{P} line 611 (Lab 3 interpretation)", "PASS",
    "tests/labs/PC3/lab-PC3-project-3.py: SEED = 0 and one play per half-spread; the interpretation's 'does not test any other seed' matches. First printed block (settlement, fills, four numbers, identity, cash agreement) matches the print statements (extract_labs.out, page lab3 output == expected).")

# ---- instance, constants, rung claims
row("proj-rung1-instance-claim", "2.8-data / 2.6-spec", f"{P} line 53 and {G}/instance.py lines 5-13", "PASS",
    "rung1_instance_check.out: the page's Lab 1 draw_game(seed) equals grader instance.make_instance(seed) for seeds 0..49 (fair path and arrivals): 50 of 50 equal. instance.py docstring (lines 5-10) describes the same move-then-arrival order and thresholds 0.5 / 0.25 / 0.5 that the code uses (lines 37, 40, 42).")
row("proj-conventions-constants", "2.2-numbers", f"{P} 'Conventions' list (lines 400-408)", "PASS",
    "N = 20 turns; v_0 = 10000; moves +5/-5 with probability 1/2 (instance.py lines 22, 23, 37); arrivals 1/4, 1/4, 1/2 (instance.py lines 40-45); q in 0..5 (engine.py line 77, MAX_SIZE line 29); |I| <= 10 (engine.py line 81, LIMIT line 30). All match.")

# ---- rubric and exemplars
row("proj-exemplar-a-calibration", "2.6-rubric", f"{P} Exemplar A (lines 635-663, data-scores 2,2,1,2,1)", "PASS",
    "Blind re-scoring from the rubric table (lines ~ 624-629): C1 2 (P&L and cash flow stated, mark not stated, no turn named as the source); C2 2 (two turns with values); C3 1 (change named, no amount); C4 2 (arrival probabilities named, no effect stated); C5 1 ('I checked it', no check named). Equals the official 2,2,1,2,1.")
row("proj-exemplar-b-calibration", "2.6-rubric", f"{P} Exemplar B (lines 665-693, data-scores 4,4,4,3,4)", "PASS",
    "Blind re-scoring: C1 4 (cash flow, mark, P&L with fill turns); C2 4 (turns 2, 5, 18 with values matching the log); C3 4 (+5 cents, same seed rerun, change 25 cents in pnl); C4 3 (arrival probabilities and inventory limit named with results; settlement rule not named); C5 4 (identity and cash check with printed results). Equals the official 4,4,4,3,4.")
row("proj-exemplar-b-numbers", "2.2-numbers", f"{P} lines 669-678 (Exemplar B P&L decomposition, evidence, counterfactual)", "PASS",
    "recompute_r3.out: fills at turns 2,3,4,5,7,8,13,18,19; purchases at bid turns 2,3,4,8,19 sum 49910; sales at ask turns 5,7,13,18 sum 39960; 39960 - 49910 = -9950; inventory after turn 19 is 1, mark 9980; turn 5 inventory after 2; turn 18 inventory after 0; counterfactual fills 9, P&L 55 (+25). All match. The sentence 'the fills stay at 9' holds for half-spread 15 (recompute_r3.out).")
row("proj-exemplar-b-arrival-sensitivity", "2.2-numbers / 2.9-scope (rule 4, rule 7)",
    f"{P} line 677 (Exemplar B, 'Assumptions and limits': 'changing them changes the fills and the P&L on seed 0')", "FAIL",
    "arrival_sensitivity_r3.out (verifier's own code, seed 0, sizes 1, half-spread 10): base (p_buy 0.25, p_sell 0.25) gives 9 fills, P&L 30. The claim fails for small changes: p_buy 0.20 gives 9 fills, P&L 30 (unchanged); p_buy 0.24 and p_sell 0.24 and p_sell 0.20 also unchanged. Other changes do move both: p_buy 0.30 gives 11 fills, P&L 40; p_sell 0.26 gives 11, 40. 969 of 1326 grid points on a 0.01 grid change fills or P&L, so 'changing them changes' is an unqualified universal the computation contradicts.",
    fix="Replace the sentence with a qualified, computed one, e.g. 'changing them can change the fills and the P&L on seed 0: raising the uninformed-buy probability from 1/4 to 3/10 gives 11 fills and a P&L of 40 cents, while lowering it to 1/5 leaves both at 9 fills and 30 cents'. Keep it in Exemplar B only if the sentence is re-checked by the verifier.")
row("proj-rubric-observable", "2.6-rubric", f"{P} rubric table (id 'rubric', lines 619-633)", "PASS",
    "Each level names observable items (values, turns, numbers in the log or the replay). Level descriptors for C1-C5 read against the exemplars give the official scores (rows proj-exemplar-*-calibration). No descriptor relies on an unnamed standard.")

# ---- spec and schema
row("proj-spec-log-schema", "2.6-spec", f"{P} 'Rung 3 · Specification', Required outputs (line ~ 393)", "PASS",
    "Spec keys: seed, settlement_cents, turns (20 records with turn, bid_cents, ask_cents, size, arrival, filled, fill_price_cents, inventory_after, cash_after_cents). engine.py lines 52-54 (docstring) and 87-98 (record keys) match exactly; fill_price_cents None when unfilled (line 82, 95). learner_command_and_seeds.out: engine.play(market_maker.quote, 286907935) returns seed, settlement_cents, turns.")
row("proj-hours-arithmetic", "2.3-hours", f"{P} 'Time budget' table (lines ~ 426-436); index.html line 167 (hub split)", "PASS",
    "Project table: 1+1+3+2+2+4+1 = 14, stated total 14; data-hours-project=14 (project.html line 33); hub 36+14=50, 14/50 = 28.0 %, hub split 2+6+4+2 = 14. Arithmetic consistent. Composition differs: the hub's 6 h (policy.py + pnl.py) is not the table's 3+2 (quote+replay) plus 1 h self-assessment; totals agree, so noted, not failed (ruling: hours are design targets).")
row("proj-hub-placement-conflict", "2.9-scope / 2.8-cross-page", f"{P} line 47 vs course/modules/PC/PC3/index.html lines 72-74 and 156", "PASS",
    "project.html line 47: 'If you reached the placement bar and answered both skill checks on the module page, skip rungs 1 and 2'. index.html line 74: the bar is 80 percent (8 of 10) and 'To skip rungs 1 and 2, you must reach the bar and answer both skill checks'; line 156 repeats it. Consistent. (The file-name and seed conflicts are separate rows below.)")
row("proj-hub-filenames", "2.8-cross-page / 2.6-spec", "course/modules/PC/PC3/index.html lines 160 and 167 (outside slice c; cited because the project contract conflicts)", "FAIL",
    "index.html line 160: 'Write <code>policy.py</code>, the quoting rule, and <code>pnl.py</code>, the replay'; line 167: 'The autograded policy.py and pnl.py take 6 hours'. project.html line ~393 (spec) and grader/test_project.py line 26 (import market_maker as sol) require market_maker.py with quote and replay. A learner who follows the hub writes files the autograder does not import.",
    fix="In index.html lines 160 and 167, replace policy.py and pnl.py with market_maker.py (quote and replay are both in it), matching project.html 'Rung 3 · Specification'.")
row("proj-hub-seed-scope", "2.9-scope / 2.2-numbers (cross-page)", "course/modules/PC/PC3/index.html lines 55 and 160 (outside slice c)", "FAIL",
    "index.html line 55: 'a quoting policy and a P&L replay that pass the autograder on seeds 0 to 49'; line 160: 'The autograder runs them on seeds 0 to 49'. project.html line 397 (Grading mode): the autograder runs on your seed and on a second seed, seed plus 7919; grader.js line 53 gives each learner one seed from the workspace ID. run_graders --seeds 0-49 is the verifier's reference gate, not the learner's autograder.",
    fix="Change index.html lines 55 and 160 to 'pass the autograder on your workspace seed and a second seed' (project.html line 397 wording).")
row("proj-hub-skill-check-premise", "2.2-numbers / 2.9-scope (cross-page)", "course/modules/PC/PC3/index.html lines 129-136 (placement skill checks; outside slice c)", "FAIL",
    "index.html line 129: 'a market maker buys one unit at an ask of 10 005 cents ... what is the cash flow'; line 134: 'after that fill the inventory is +1 unit'. In the project's model a maker purchase is at the bid and a maker sale at the ask (project.html line ~393: 'A fill at the bid is a purchase by the maker, and a fill at the ask is a sale by the maker'; Trades, line ~410). A buy at the ask is not a maker fill in this model.",
    fix="Rewrite both skill checks in the project's convention: a customer buys one unit from the maker at the ask 10005 (maker sells: cash flow +10005, inventory -1), or the maker buys at the bid, and recompute the answers and the mark from the same premise.")

# ---- quoting rule and mutants
row("proj-quote-rule-first-fill-survivor", "2.8-grader / 2.6-spec", f"{P} time-budget row 'Quoting rule: quote' (line ~429); grader test_project.py has no quote-mid check", "FAIL",
    "mutants v17_quote_mid_from_first_fill.py (quote takes the mid from the FIRST filled price in history, not the last) SURVIVED all 50 seeds' suite (mutate_all_r3.out, 26/27 killed). The suite checks only quote legality (bid < ask, size 0..5, int) on every turn; no test requires the mid to follow the last fill. project.html line 429 states the rung-3 rule as 'A rule that reads the history for the last filled price', which the mutant violates; the Grading-mode list (line 397) does not name the mid as graded, so this is a page/grader mismatch. Judgement call for the orchestrator: if the time-budget sentence is read as work description, not a graded property, this becomes PASS.",
    fix="Either (a) reword the time-budget row (line ~429) so it does not state a graded quote property, e.g. 'A quoting rule in market_maker.py that is legal on every turn for both instances', or (b) add a grader test that after a known fill price the quote's mid is that price, phrased as a property, and cite it in Grading mode.")
row("proj-builder-mutants", "2.8-grader", "ledgers/PC3/mutants/m01..m10", "PASS",
    "mutate_existing.out and mutate_all_r3.out: m01-m10 all KILLED (first kill at seed 0 for each). m08 (hard-coded zeros) body returns zeros before the dead code, matching its description.")
row("proj-verifier-mutants", "2.8-grader", "ledgers/PC3/mutants/v01..v12", "PASS",
    "mutate_all_r3.out: v01-v12 all KILLED on seed 0 (v04 killed by test_replay_sums_the_fills_not_the_running_totals; v08 by test_no_function_prints; v09 by test_quotes_are_legal_on_every_turn via warning; v10 by test_replay_refuses_a_log_that_is_not_twenty_turns[21]).")
row("proj-mutant-m08-description", "2.8-grader", "ledgers/PC3/mutants/m08_hard_coded_answer_for_any_log.py lines 1-2 and 34", "PASS",
    "Docstring: 'replay returns all zeros, a hard-coded answer, for every log'. Line 34 returns the zero dict before the replay code (the code after it is unreachable). Killed by test_filled_turn_without_a_price_is_refused (seed 0), so the mutant is killed; description matches the body.")
row("proj-verifier-mutants-r3-new", "2.8-grader", "ledgers/PC3/mutants/v13..v17 (new this round)", "PASS",
    "Four new student-error mutants killed on seed 0: v13 extra fifth key (test_replay_returns_the_fills...[0]); v14 inventory sums absolute sides (same test); v15 P&L = mark - cash (same test); v16 refuses unfilled turns without a price (same test). v17 (quote mid from first fill) SURVIVED; see proj-quote-rule-first-fill-survivor.")
row("proj-alternatives-1-2-4-5", "2.8-grader / 2.7-alternatives", "ledgers/PC3/alternatives/alt1, alt2, alt4, alt5", "PASS",
    "alternatives_r3.out (run_alts_r3.py, each alternative as market_maker.py, test_project.py, seeds 0-49): alt1 50/50, alt2 50/50, alt4 50/50, alt5 50/50.")
row("proj-alt3-replay", "2.8-grader / 2.7-alternatives", "ledgers/PC3/alternatives/alt3_inventory_skew.py (replay lines 26-46)", "PASS",
    "alternatives_r3.out: alt3 (inventory skew, sums fills) passes 50/50 seeds under the unchanged suite.")
row("proj-alternative-6", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r1/alt6_size_zero_on_multiples_of_three.py", "PASS",
    "alternatives_r3.out: alt6 (size 0 on every third turn, zip replay) passes 50/50 seeds.")
row("proj-alternative-7-8-verifier", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r2/alt7_*.py and alt8_*.py", "PASS",
    "alternatives_r3.out: alt7 (one-cent half-spread, reversed scan) 50/50; alt8 (quarter spread, size 0 at the limit) 50/50.")
row("proj-alternative-9-10-verifier-r3", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r3/alt9_reverse_scan_size_five_dataclass.py and alt10_inventory_zero_size_at_limit_reduce_fold.py", "PASS",
    "Written this round to test over-constraint: alt9 scans history backwards, quotes size 5, uses a dataclass accumulator; alt10 skews the mid by -1 cent per unit of inventory, quotes size 0 at |I| = limit, folds with functools.reduce. alternatives_r3.out: both pass 50/50 seeds.")
row("proj-grader-35-checks", "2.8-grader", f"{P} 'Grading mode' (line 397) and {G}/test_project.py", "PASS",
    "Collect count: 37 tests in the reference workspace (collect_in_workspace.out, and pytest --collect-only run in /tmp/pc3c-r3-ws). In-browser page_smoke: 'All 37 tests pass'. The page's '37 checks' equals the real count. collect_only.out in the checkout errors only because market_maker.py is absent there (expected).")
row("proj-grader-seed-scope-claim", "2.8-grader", f"{P} 'Constraints' Integrity sentence (line 395) and 'Grading mode' (line 397)", "PASS",
    "Parametrized over SEEDS (seed, seed+7919): test_quotes_are_legal, test_replay_returns, test_replay_agrees, test_pnl_identity, test_money_and_units, test_cash_moves, test_a_log_carries, test_instance_is_deterministic = 8 names x 2 = 16 cross-seed. Remaining 21 seed-only (collect count 37 - 16). The 8 named checks in the page match these names.")
row("proj-grader-no-print", "2.8-grader", f"{P} 'Constraints' ('No function prints or warns', line 395)", "PASS",
    "grep: no print( or warn in engine.py, instance.py, reference.py, starter.py; test_no_function_prints exists; replay() in the Lab 1 page has 0 print calls (lab1_replay_print_check.out). pytestmark filterwarnings('error') enforces warnings.")
row("proj-grader-replay-from-fills", "2.8-grader", f"{P} Conventions 'The P&L' bullet; {G}/test_project.py oracle (lines 68-79)", "PASS",
    "oracle() derives cash, inventory and mark from fills and settlement only; test_replay_returns... compares replay output with oracle for the fixed quote and the student's quote. Reference replay matches oracle (run_graders PASS 50/50).")
row("proj-grader-mypy-strict", "2.8-grader / 2.9-gate", f"{G}/test_project.py (lines 139-165 changed earlier) and engine.py, instance.py", "PASS",
    "mypy_strict_workspace.out: 'mypy --strict --ignore-missing-imports test_project.py engine.py instance.py' -> Success; 'mypy --strict test_project.py' (reference as market_maker) -> Success. mypy_grader.out (run on the grader folder in the checkout) has import-not-found errors only because the module names are absent there, plus 'Returning Any' in test_project.py lines 65, 133, 147 that appear only without the module resolved; the workspace run is clean. Repo gate mypy (repo_mypy) also PASS.")
row("proj-grader-reference", "2.8-grader", f"{G}/reference.py", "PASS",
    "run_graders.out: 'run_graders PC3: PASS (reference 50/50 seeds, slowest 0.1 s)'; typecheck of reference.py, instance.py, starter.py under mypy --strict clean (gate).")
row("proj-grader-starter-fails", "2.8-grader", f"{G}/starter.py", "PASS",
    "run_graders.out: the gate runs the starter on seed 0 and reports FAIL if it passes; no such message, so the starter fails the suite (NotImplementedError). Overall PASS.")
row("proj-grader-instances", "2.8-grader", f"{G}/instance.py", "PASS",
    "run_graders.out: check_instances deterministic and distinct over the first 20 seeds (no FAIL lines). rung1_instance_check.out: 50 of 50 seeds equal to the page's draw.")
row("proj-grader-messages", "2.8-grader", f"{G}/test_project.py (messages at lines 40-55, 150-163, 229-235, 268, 288-292)", "PASS",
    "Read every expect() / pytest.fail() message: none interpolates a computed value; the two f-strings name only the expected phrase (line 53, 55). Matches 'a failing check names the property ... never prints the value'.")
row("proj-named-refusals", "2.8-grader / 2.6-spec", f"{G}/test_project.py lines 166-217 and {P} 'Named invalid inputs' (lines 410-417)", "PASS",
    "Four named conditions in the page (bid must be below ask; size must lie in 0..5; a log has exactly 20 turns; a filled turn needs a fill price) match the phrases in must_refuse() calls and the engine/reference messages. Other invalid inputs are not required to raise (no test demands an exception outside the named list).")
row("proj-exception-types", "2.8-grader", f"{G}/test_project.py lines 47-55 and 168-218", "PASS",
    "must_refuse() (ValueError) is used only for the four named conditions; test_bid_one_cent_below_ask_is_accepted and test_sizes_at_the_edges_* demand no exception. Matches the page sentence 'The autograder requires no exception type for those'.")

# ---- gates and content checks
row("proj-run-labs-unit", "2.5-labs / 2.9-gate", "tools/run_labs.py --unit PC3 --page project", "PASS",
    "run_labs_project.out: 'run_labs PC3: PASS (3/3)', exit 0.")
row("proj-check-tools", "2.9-gate", "tools/check_pages.py, check_dag.py, check_projects.py --unit PC3", "PASS",
    "check_pages.out 'check_pages PC3: PASS'; check_dag.out 'check_dag PC3: PASS'; check_projects.out 'check_projects PC3: PASS'; each exit 0.")
row("proj-page-smoke", "2.9-gate", f"tools/page_smoke.py --unit PC3 (project.html)", "PASS",
    "page_smoke.out: 'page_smoke modules/PC/PC3/project.html: PASS' (labs and in-browser grader 'All 37 tests pass'), page_smoke PC3: PASS, exit 0.")
row("proj-lint-ruff", "2.9-gate", f"ruff check and format check on {G} and tests/labs/PC3/lab-PC3-project-*.py", "PASS",
    "ruff_check.out 'All checks passed!' (exit 0); ruff_format.out '8 files already formatted' (exit 0). Repo ruff on tests/labs/PC3 and grader: exit 0.")
row("proj-mypy-labs", "2.9-gate", "tests/labs/PC3/lab-PC3-project-1..3.py", "PASS",
    "mypy_labs.out: 'Success: no issues found in 3 source files'; repo mypy (mypy_repo.out) 'Success: no issues found in 385 source files'.")
row("proj-banned-and-process-words", "2.12-process / 2.13-banned", f"{P} (all text, code and expected blocks); {G}", "PASS",
    "Scan of stripped text for round/verif/builder/agent/AI/draft/placeholder/TODO/we/our/I and similar: no process words in learner text. 'I checked it.' appears only as the scripted Exemplar A self-review (a learner sample). 'Step' appears only in lab comments.")
row("proj-notation", "2.13-notation", f"{P} inline math (49 spans) vs notation/notation.json (8 registered symbols, 'Binding notation registry')", "PASS",
    "Symbols used: I, I_20, N (=20, local), a_t, b_t, q_t, v_t, v_0, v_20, pnl (\\mathrm). None of the 8 registered symbols (T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q) appears, so no collision. Macros used are the registered ones only (none of the registry macros needed).")
row("proj-dag-terms", "2.14-dag", f"{P} (all text); course/modules/PC/PC3/L04.html", "PASS",
    "The only concept link on project.html is market-making-game (href L04.html#def-market-making-game; L04.html contains id='def-market-making-game'), in-unit. 'Adverse selection' appears as a named omission (rubric C4, Exemplar B) and is defined in L04.html ('adverse selection, the loss a maker takes ...'). check_dag PASS.")
row("proj-references", "2.2-sources", f"{P} 'Reading' (lines 710-720) and references section", "PASS",
    "data-cite keys zhou2008practical and crack2015heard exist in references/references.json (verified_by openlibrary); verify_refs.out 'offline integrity: 560 entries, 0 problems'. The page attributes no passage, problem or page number; the sentence 'This page attributes no problem, answer, page or edition' holds.")
row("proj-js-claims", "2.4-claims", f"{P} 'Autograder' section paragraph and footer; course/assets/js/grader.js lines 1-4, 33-34, 61, 79", "PASS",
    "grader.js: seed from workspace ID via store.unitSeed (line 33); code saved in IndexedDB as typed (store.put debounce, lines 61, 79); fetch calls are static assets only (lines 18, plus data/notation/refs loaders). Claims 'saved in this browser', 'the seed comes from your workspace ID' and 'nothing you write leaves it' match the code.")
row("proj-local-commands", "2.4-claims", f"{P} Spec 'Required outputs' (python3 -c command) and 'Running the suite locally'", "PASS",
    "learner_command_and_seeds.out: the spec command (import json, engine, market_maker; json.dumps(engine.play(...))) runs in a folder with engine.py, instance.py, market_maker.py and prints the log; QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py passes for seeds 286907935, 2147483647, 0, 49 (37 passed each).")
row("proj-known-limitation", "2.4-claims", f"{P} 'Constraints' (line 395); engine.py docstring lines 19 and 52-54", "PASS",
    "The log has seed, settlement_cents and turns only (engine.py lines 52-54, 96-100): no fair path. instance.py is readable. No test checks avoidance of the fair path (grep of test_project.py): the stated limitation is accurate.")
row("proj-ladder-scope", "2.8-cross-page / 2.9-scope", f"{P} lines 40-48 (ladder); curriculum/06-profession-capstone.yaml lines 175-182", "PASS",
    "Ladder: rungs 1-2 full length, skip rule as in the hub. The curriculum brief ('in-page market-making game against scripted counterparties ... post-game analysis') is looser than project.html ('Play is by code'), not contradictory in a way a learner would act on; deliverable 'Game log plus analysis' is consistent with analysis.md plus the written log. No failure; noted.")
row("proj-rubric-atlas-studios", "2.8-cross-page", "plans/PC3-build-plan.md section 8; project.html (no 'Atlas' text: grep count 0)", "PASS",
    "Plan section 8: 'None' (no Atlas milestone). project.html contains no Atlas milestone claim and no atlas contract reference.")
row("proj-stretch", "2.2-numbers / 2.6-spec", f"{P} lines 701-708 (Rung 4 · Stretch)", "PASS",
    "Stretch items are open tasks; the informed-share task (informed 1/2 to 0.6, uninformed evenly split) is expressible with the page's arrival rules (engine.py maker_side, instance.py thresholds). No numeric claim in the stretch text to check.")
row("proj-twin-rules", "2.5-labs", "tests/labs/PC3/lab-PC3-project-1..3.py", "PASS",
    "Twins run under python -I -W error: exit 0, stderr 0 (extract_labs and lab runs). Lab 1 and Lab 3 page code equals twin line for line (0 differing lines); Lab 2 differs only in the two blanked lines. Twin 2 gained the None check (line ~100) matching the page.")
row("proj-exception-types-labs", "2.8-grader", f"{P} Lab 1 and Lab 3 replay (raise ValueError lines)", "PASS",
    "Lab replays raise ValueError only for 'a log has exactly 20 turns' and 'a filled turn needs a fill price', the same two named conditions as the page.")

# ---- mutant list
mutants = []
kill_re = re.compile(r"^(KILLED|SURVIVED) (\S+?\.py): (.*?) -> (.*)$")
for line in open(f"{S}/mutate_all_r3.out", encoding="utf-8"):
    m = kill_re.match(line.strip())
    if not m:
        continue
    status, name, desc, where = m.groups()
    killed_by = where.strip() if status == "KILLED" else ""
    mutants.append({"id": name[:-3], "description": desc, "file": f"ledgers/PC3/mutants/{name}", "killed_by": killed_by})

fragment = {
    "unit": "PC3",
    "slice": "c",
    "round": 3,
    "verifier": "independent verifier (Haiku 5.5), round 3, slice c",
    "pin": "67a2d13e",
    "base": "round 2 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round2.json (pin 67c47689) and round 1; all rows re-derived this round, no round-2 PASS row carried",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE3-PC3-c",
    "scratch": "/tmp/pc3c-r3-ws (grader workspace), /tmp/pc3c-r3-*.py (extracted lab pages); every cited result comes from a file under ledgers/PC3/scripts/PC3-c-r3/",
    "verified_at": "2026-11-04T10:00:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta since 67c47689 (round 2): project.html (Lab 1 replay print moved to main, Lab 2 None check, Lab 3 wording, Exemplar A and B sentences, spec and grading wording); tests/labs/PC3 project twins 1-3; grader/ unchanged; no mutant or alternative changed. "
        "Read in full: project.html (all 732 lines), grader engine.py, instance.py, reference.py, starter.py, test_project.py (417 lines). "
        "Not checked: full-repo gates (render_curriculum, build_site --check, fetch_data --check, check_pages --all, run_graders --all, pytest whole suite); the hub index.html beyond the lines cited; L04.html beyond the definition id and adverse-selection sentence; live Crossref or any network verify_refs (offline only); the in-browser grader run in a real browser (page_smoke only). "
        "Mutant count: 27 (m01-m10, v01-v17); 26 killed, v17 survived. The survivor is a judgement call (see proj-quote-rule-first-fill-survivor)."
    ),
    "summary": "Slice c round 3: verdict FAIL. Five FAIL rows: proj-exemplar-b-arrival-sensitivity (computed counterexample to an unqualified sentence), proj-quote-rule-first-fill-survivor (surviving mutant against a stated rule sentence), and three cross-page hub rows in index.html (policy.py/pnl.py names, 'seeds 0 to 49' scope, skill-check premise that a maker buys at the ask). Round-2 FAILs proj-exemplar-a-numbers and proj-lab1-replay-prints are fixed and re-verified PASS. Gates: check_pages, check_dag, check_projects, run_labs (3/3), page_smoke, run_graders (50/50), ruff, mypy, verify_refs --offline, pytest -k subset all PASS.",
}

problems = ledger.validate(fragment, "PC3-c")
print("validate:", problems)
counts = {}
for r in R:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
print("rows", len(R), counts, "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
ids = [r["id"] for r in R]
print("duplicate ids:", sorted({i for i in ids if ids.count(i) > 1}))
if not problems:
    open(f"{ROOT}/ledgers/PC3/PC3-c.json", "w", encoding="utf-8").write(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n")
    print("written")
