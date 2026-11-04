"""Round-6 fragment builder for PC3 slice c. Reads the mutation output and writes ledgers/PC3/PC3-c.json.
Run with: python3 -I <this file>. Row evidence is written here from the commands and reads recorded in the scratch outputs."""
import datetime
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE6-PC3-c")
S = "ledgers/PC3/scripts/PC3-c-r6"
CARRY = "Carried from round 5 (project.html byte-identical on the cited lines, and no other cited file changed, between pins 7376a5e and 4bd8cb9): "

R = []


def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix or ""
    R.append(d)


# ---- numbers and labs
row("proj-exemplar-a-numbers", "2.2-numbers", "course/modules/PC/PC3/project.html line 643 (Exemplar A 'Evidence from the log')", "PASS",
    "Line 643 reads 'Turn 5 sold at the ask of 9980 cents, and turn 18 sold at the ask of 10000 cents'. Independent replay (" + S + "/indep_numbers_r6.out): fill (5, -1, 9980) and fill (18, -1, 10000), both sales at the ask.")
row("proj-lab1-replay-prints", "2.5-labs", "project.html lab-PC3-project-1 code, lines 85-185 (draw_game, quote, maker_side, play, replay)", "PASS",
    "Read lines 85-185 in full: no print or warn call in those functions; print calls only in main (lines 188-215). " + S + "/labs_page_vs_twin_r6.out: lab-PC3-project-1 page code equals the twin on all 161 lines (0 differing).")
row("proj-lab1-run", "2.5-labs", "project.html lab-PC3-project-1 (rung 1)", "PASS",
    S + "/run_labs_project.out: 'run_labs PC3: PASS (3/3)'. " + S + "/labs_page_vs_twin_r6.out: twin exit 0, stderr 0 bytes, output equals expected block.")
row("proj-lab1-hypothesis-numbers", "2.2-numbers", "project.html line 57 (Lab 1 hypothesis)", "PASS",
    S + "/indep_numbers_r6.out: fills 9, cash -9950, inventory 1, settlement 9980, mark 9980, P&L 30, largest |inventory| 3, identity True. All match line 57.")
row("proj-lab2-completion", "2.5-labs", "project.html lab-PC3-project-2, lines 349-350 and 105-106 of the page block", "PASS",
    S + "/labs_page_vs_twin_r6.out: page differs from the twin on exactly two lines (cash_flow = ___, mark = ___); twin exit 0 and output equals the expected block (-9950, 1, 9980, 30, True).")
row("proj-lab2-interpretation-last-quote", "2.2-numbers", "project.html line 381 (Lab 2 interpretation)", "PASS",
    "Line 381 says a mark other than 9980 changes the P&L with inventory 1. P&L = cash flow + 1 x mark (Conventions line 407), so it changes for every other mark value. Line text read this round.")
row("proj-lab3-counterfactual", "2.2-numbers", "project.html lines 456-612 (Lab 3)", "PASS",
    S + "/labs_page_vs_twin_r6.out: lab-PC3-project-3 page equals twin on all 140 lines; twin output equals expected block (settlement 9980, 9 fills, P&L 55 and change 25 on the counterfactual). indep_numbers_r6.out: half-spread 15 gives 9 fills, P&L 55, change 25.")
row("proj-lab3-interpretation", "2.2-numbers", "project.html line 611 (Lab 3 interpretation)", "PASS",
    "Line 611 says the change is one seed and the lab tests no other seed. Lab 3 page code line 483 is SEED = 0 and the counterfactual is play(SEED, COUNTERFACTUAL_HALF_SPREAD) only.")
row("proj-rung1-instance-claim", "2.8-data / 2.6-spec", "project.html line 53; course/modules/PC/PC3/grader/instance.py lines 36-45", "PASS",
    S + "/indep_numbers_r6.out: instance(0) fair path and arrivals equal the independent draw (move then arrival, random.Random(0)): True, True. L04.html lines 235-254 are outside the L04 diff hunks (52, 175, 690).")
row("proj-conventions-constants", "2.2-numbers", "project.html Conventions lines 402-407", "PASS",
    "N = 20 (instance.py HORIZON 20), v0 = 10000 (START_CENTS), move +5/-5 at probability 1/2 (instance.py line 37), arrivals 1/4, 1/4, 1/2 (instance.py lines 40-45), 0 <= q <= 5 (engine.py MAX_SIZE line 29), |I| <= 10 (engine.py LIMIT line 30), cash identity cash += -side*price (engine.py line 86).")
row("proj-exemplar-a-calibration", "2.6-rubric", "project.html Exemplar A, lines 635-663 (data-scores 2,2,1,2,1)", "PASS",
    "Read lines 635-663. Annotations at lines 653-659 match the scores: C1 2 (P&L and cash flow stated, mark not), C2 2 (two turns with values from the log), C3 1 (asserts a change helps, no amount), C4 2 (parameters named, no effect), C5 1 (checked, no check named).")
row("proj-exemplar-b-calibration", "2.6-rubric", "project.html Exemplar B, lines 665-693 (data-scores 4,4,4,3,4)", "PASS",
    "Read lines 665-693. Annotations at lines 683-688 match the scores: C1-C3 and C5 level 4, C4 level 3 with the level-4 miss at line 687 (settlement rule not named). Consistent with the official-scoring line 667.")
row("proj-exemplar-b-numbers", "2.2-numbers", "project.html lines 669-678 (Exemplar B)", "PASS",
    S + "/indep_numbers_r6.out: purchases at the bid on turns 2, 3, 4, 8, 19 sum to 49910; sales at the ask on turns 5, 7, 13, 18 sum to 39960; 39960 - 49910 = -9950; inventory 1; mark 1 x 9980 = 9980; P&L 30. Turn-level claims at line 673 (turn 2 at 9990, turn 5 inventory 2, turn 18 inventory 0) match the indep fills and inventory path.")
row("proj-exemplar-b-arrival-sensitivity", "2.2-numbers", "project.html line 677 (Exemplar B 'Assumptions and limits', changed this round)", "PASS",
    "Line 677 says the arrival probabilities set the thresholds and that Lab 1 varies none, so the printed run does not measure their effect. Lab 1 uses draw < 0.25 and < 0.5 with no parameter sweep (page code lines 96-101). Largest inventory 3 is printed by Lab 1 (line 238) and by indep_numbers_r6.out (max |I| 3, limit not binding).")
row("proj-rubric-observable", "2.6-rubric", "project.html rubric table lines 619-629 (C4 changed this round)", "PASS",
    "Read lines 619-629. C4 level 4 now names items an analysis can check: arrival probabilities, inventory limit, settlement rule, and what is left out (the queue of resting orders and a trader who learns from fills, both set aside in L04 lines 465; latency; more than one asset). Each level 1-4 names a descriptor an analysis either has or lacks.")
row("proj-spec-log-schema", "2.6-spec", "project.html 'Required outputs' line 393", "PASS",
    "Line 393 state keys (turn, inventory, cash_cents, max_size, limit, history) match engine.py lines 66-73. Log keys (seed, settlement_cents, turns) and the nine record keys match engine.py lines 89-97 and 51-54. Arrival names match instance.py lines 24 and 40-45.")
row("proj-hours-arithmetic", "2.9-hours", "project.html 'Time budget' lines 425-434; index.html lines 167-168", "PASS",
    "Page lines 427-433 sum to 1+1+3+2+2+4+1 = 14 (line 434 total 14). 14/50 = 28.0 percent (line 434). Hub line 167: 36 lessons + 14 project = 50 module hours; hub split 2+6+4+2 = 14.")
row("proj-hub-placement-conflict", "2.4-structure", "project.html lines 42-48 vs index.html lines 74 and 128-137", "PASS",
    "Page line 42 says skip rungs 1 and 2 only if the placement bar is reached and both skill checks are answered. Hub line 74 says the same bar and two skill checks (data-skill items at lines 128-137). Consistent.")
row("proj-hub-filenames", "2.4-structure", "course/modules/PC/PC3/index.html lines 160 and 167 vs project.html lines 393, 443, 448 and grader/test_project.py line 26", "FAIL",
    "Hub line 160 says 'Write policy.py, the quoting rule, and pnl.py'; hub line 167 says 'The autograded policy.py and pnl.py take 6 hours'. Project page line 393 requires market_maker.py, line 443 sets data-solution=\"market_maker.py\", line 448 says market_maker.py, and test_project.py line 26 imports market_maker.",
    "Make the hub name market_maker.py (or, if the plan's policy.py/pnl.py is confirmed, rename the page and the grader). The hub and the project must name the same files.")
row("proj-hub-seed-scope", "2.6-spec", "course/modules/PC/PC3/index.html lines 55 and 160 vs project.html line 397", "FAIL",
    "Hub line 55 says the learner writes code that 'pass[es] the autograder on seeds 0 to 49'; hub line 160 says 'The autograder runs them on seeds 0 to 49'. Project line 397 says the suite runs on the learner's seed and seed + 7919 (test_project.py line 33: SEEDS = (SEED, SEED + 7919)); 0 to 49 is used only by the fixed-seed distinctness test (lines 387-391).",
    "Change the hub to match the grader (or change the grader; see proj-plan-grader-seed-scope). The hub and the project must state the same seed scope.")
row("proj-hub-skill-check-premise", "2.2-numbers", "course/modules/PC/PC3/index.html lines 128-137 (rung 1 skill check, data-answer -10005)", "FAIL",
    "Hub line 129: 'a market maker buys one unit at an ask of 10 005 cents'. Project line 393 says 'A fill at the bid is a purchase by the maker, and a fill at the ask is a sale by the maker'; line 406 says 'A maker purchase at the bid b changes cash by -b'. A purchase at an ask is not a fill in this game.",
    "Reword the premise to a purchase at the bid (for example 'a market maker buys one unit at its bid of 10 005 cents'), keeping data-answer -10005, or change the answer to match a sale at the ask.")
row("proj-quote-rule-first-fill-survivor", "2.7-alternatives", "project.html line 429 (rung 3 time row); ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py", "PASS",
    S + "/alts_all_r6.out: alt6_quote_mid_from_first_fill passes 50/50 seeds (0-49).")
row("proj-builder-mutants", "2.6-mutants", "ledgers/PC3/mutants/m01..m10", "PASS",
    S + "/mutate_r6_full.out: m01-m10 all KILLED on seeds 0-49 (first kill named per mutant).")
row("proj-verifier-mutants", "2.6-mutants", "ledgers/PC3/mutants/v01..v16", "PASS",
    S + "/mutate_r6_full.out: v01-v16 all KILLED.")
row("proj-mutant-m08-description", "2.6-mutants", "ledgers/PC3/mutants/m08_hard_coded_answer_for_any_log.py lines 1-2 and 34", "PASS",
    CARRY + "m08 file byte-identical since 7376a5e. Line 1 reads 'Student error: replay returns all zeros, a hard-coded answer, for every log.' and mutate_r6_full.out reports m08 KILLED.")
row("proj-verifier-mutants-r3-new", "2.6-mutants", "ledgers/PC3/mutants/v13..v16", "PASS",
    S + "/mutate_r6_full.out: v13, v14, v15, v16 KILLED.")
row("proj-alternatives-1-2-4-5", "2.7-alternatives", "ledgers/PC3/alternatives/alt1, alt2, alt4, alt5", "PASS",
    S + "/alts_all_r6.out: alt1, alt2, alt4, alt5 each pass 50/50 seeds.")
row("proj-alt3-replay", "2.7-alternatives", "ledgers/PC3/alternatives/alt3_inventory_skew.py", "PASS",
    S + "/alts_all_r6.out: alt3 passes 50/50 seeds.")
row("proj-alternative-6", "2.7-alternatives", "ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py", "PASS",
    S + "/alts_all_r6.out: alt6 passes 50/50 seeds.")
row("proj-alternative-7-8-verifier", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r2/alt7_*.py, alt8_*.py", "PASS",
    S + "/alts_all_r6.out: alt7 and alt8 each pass 50/50 seeds.")
row("proj-alternative-9-10-verifier-r3", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r3/alt9_*.py, alt10_*.py", "PASS",
    S + "/alts_all_r6.out: alt9 and alt10 each pass 50/50 seeds.")
row("proj-alternatives-r4-new", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r4/alts/alt11, alt12, alt13", "PASS",
    S + "/alts_all_r6.out: alt11, alt12, alt13 each pass 50/50 seeds.")
row("proj-grader-35-checks", "2.6-spec", "project.html line 397 ('39 checks'); grader/test_project.py", "PASS",
    "Collect-only in a scratch workspace holding engine.py, instance.py, test_project.py and reference.py as market_maker.py (/tmp/pc3c-r6-ws/ref): '39 tests collected'. Page line 397 says 39. Browser smoke (" + S + "/page_smoke_project.out): 'All 39 tests pass on seed 1419791452'.")
row("proj-grader-seed-scope-claim", "2.6-spec", "project.html line 395 (Integrity) and line 397 (Grading mode); grader/test_project.py lines 33, 139-140 and parametrize markers", "PASS",
    "Seed-parametrised functions: test_quotes_are_legal, replay_returns, replay_agrees, pnl_identity, money_integers, cash_moves, log_carries_seed, instance_deterministic = 8 x 2 seeds = 16. Seed-only: 7 refusal/boundary items, 3 replay refusals, 7 fill-rule items, the settlement mark, stale totals, one-unit fill, price-0 fill, no-print = 22. Fixed seeds 0-49 = 1. Total 39. Matches line 397.")
row("proj-grader-no-print", "2.6-spec", "project.html line 395 ('No function prints or warns'); grader/test_project.py lines 358-362 (test_no_function_prints) and line 30 (filterwarnings)", "FAIL",
    "test_no_function_prints checks only capsys.readouterr().out (line 362). A quote or replay that writes to sys.stderr passes (" + S + "/mutate_r6_full.out: v24_replay_prints_a_debug_line_to_stderr SURVIVED). A logging.warning call also passes (v26 SURVIVED). The page sentence 'No function prints or warns' is not fully enforced.",
    "Assert both streams are empty (capsys.readouterr().err as well as .out) and assert no log records (caplog) in test_no_function_prints; see proj-grader-v24 and proj-grader-v26.")
row("proj-grader-replay-from-fills", "2.6-spec", "project.html Conventions 'The P&L' line 407; grader/test_project.py oracle lines 68-79", "PASS",
    "Oracle (lines 68-79) computes cash flow from the fills, the inventory from the fills, the mark as inventory x settlement, and the P&L as their sum, from the log alone. Matches Conventions line 407.")
row("proj-grader-mypy-strict", "2.6-lint", "course/modules/PC/PC3/grader/engine.py, instance.py, test_project.py, reference.py", "PASS",
    "In the scratch workspace: .venv/bin/mypy --strict engine.py instance.py test_project.py market_maker.py -> 'Success: no issues found in 4 source files'.")
row("proj-grader-reference", "2.6-grader", "course/modules/PC/PC3/grader/reference.py", "PASS",
    S + "/run_graders.out: 'run_graders PC3: PASS (reference 50/50 seeds)'. Scratch pytest with reference as market_maker: 39 passed for QF_SEED 0, 1, 2, 7, 49.")
row("proj-grader-starter-fails", "2.6-grader", "course/modules/PC/PC3/grader/starter.py", "PASS",
    "Scratch run with starter.py as market_maker.py: 22 failed, 17 passed (the NotImplementedError stubs are caught by the suite, which must fail on the starter).")
row("proj-grader-instances", "2.8-data", "course/modules/PC/PC3/grader/instance.py lines 1-53", "PASS",
    "Read instance.py in full. Deterministic from random.Random(seed); keys seed, label, start_cents, fair_path_cents (21 values), arrivals (20 names), settlement_cents. Matches plan 5.6 and the page's Inputs line 391. Fixed-seed distinctness: 50 distinct paths for seeds 0-49 (indep_numbers_r6.out).")
row("proj-grader-messages", "2.6-grader", "course/modules/PC/PC3/grader/test_project.py lines 40-55 and every expect() message", "PASS",
    "Read every message in the file. Messages name the property or the condition named in the spec; none interpolates a computed expected value (expect() takes a fixed string; must_refuse() prints only the phrase). __tracebackhide__ is set in expect and must_refuse.")
row("proj-named-refusals", "2.6-grader", "course/modules/PC/PC3/grader/test_project.py lines 169-217; project.html lines 410-418", "PASS",
    "Four named conditions (bid must be below ask; size must lie in 0..5; a log has exactly 20 turns; a filled turn needs a fill price) each have must_refuse tests (lines 169-217). Page lines 413-416 quote the same phrases; engine.py lines 76 and 78 raise the first two.")
row("proj-exception-types", "2.6-grader", "course/modules/PC/PC3/grader/test_project.py lines 47-55 and 168-218; project.html line 418", "PASS",
    "No pytest.raises in the file. must_refuse is used only for the four named conditions. Page line 418 says any other invalid input may raise any exception or return; the suite requires no type for those.")
row("proj-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3 --page project", "PASS",
    S + "/run_labs_project.out: 'run_labs PC3: PASS (3/3)'.")
row("proj-check-tools", "2.9-tools", "tools/check_pages.py, check_dag.py, check_projects.py --unit PC3", "PASS",
    S + "/check_pages.out: 'check_pages PC3: PASS'; check_dag.out: 'check_dag PC3: PASS'; check_projects.out: 'check_projects PC3: PASS'.")
row("proj-page-smoke", "2.5-labs", "tools/page_smoke.py --unit PC3 --pages project", "PASS",
    S + "/page_smoke_project.out: 'page_smoke modules/PC/PC3/project.html: PASS', 'page_smoke PC3: PASS'; in-browser grader 'All 39 tests pass'.")
row("proj-lint-ruff", "2.9-tools", "ruff check and ruff format --check on course/modules/PC/PC3/grader and tests/labs/PC3", "PASS",
    S + "/ruff_check.out: 'All checks passed!'; ruff_format.out: '14 files already formatted'.")
row("proj-mypy-labs", "2.9-tools", "mypy --no-incremental (repo)", "PASS",
    S + "/mypy_repo.out: 'Success: no issues found in 385 source files'.")
row("proj-banned-and-process-words", "2.12-process", "project.html all visible text and code; tests/labs/PC3/lab-PC3-project-1..3.py", "PASS",
    "Scanned project.html text (tags stripped) for verifier, builder, architect, round, fixer, ledger, plan, TODO, draft, placeholder, pending, ruling, mutant, twin: only 'around' (contains 'round') in lines 466 and 53 matched. No process words.")
row("proj-notation", "2.13-notation", "project.html inline and display math (49 spans) vs notation/notation.json", "PASS",
    "Re-extracted all 49 \\(...\\) and \\[...\\] spans. Symbols used: N, v_t, v_0, v_20, b_t, a_t, q_t, I, I_20, |I|, t, pnl, plus digits and operators. notation/notation.json (unchanged since 7376a5e) registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. No overlap, no reuse.")
row("proj-dag-terms", "2.14-dag", "project.html whole text; course/modules/PC/PC3/L04.html line 60 (def-market-making-game)", "PASS",
    "The only concept link on the page is line 37 to L04.html#def-market-making-game, and L04 line 60 carries <dfn id=\"def-market-making-game\">. Other terms (latency, quantiles, expected, spread, inventory) are plain words with no link, and adverse selection is no longer named on the page.")
row("proj-references", "2.11-refs", "project.html 'Reading' lines 710-717 and 'References' line 721; references/references.json", "PASS",
    "references.json contains zhou2008practical and crack2015heard (grep count 2). " + S + "/verify_refs.out: 'offline integrity: 560 entries, 0 problems'. Page lines 712-716 cite keys only and attribute no problem, answer, page or edition.")
row("proj-js-claims", "2.10-js", "project.html lines 442 (autosave), 395 and 449 and footer line 730; course/assets/js/store.js lines 122-136; grader.js lines 53, 59-61", "PASS",
    "store.js: unitSeed derives a 31-bit FNV-1a seed from the workspace ID (lines 134-136). grader.js lines 59-61: textarea input saved through a debounced store.put (400 ms), so the code is saved as typed. grader.js line 53 and py-worker.js line 111 use the same pytest flags as page line 449.")
row("proj-local-commands", "2.10-js", "project.html line 393 (log command) and line 449 (local suite command)", "PASS",
    "Run in a scratch folder with engine.py, instance.py, reference.py as market_maker.py: the line-393 command writes a valid 20-turn log (seed 7, settlement 10010); 'QF_SEED=7 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py' gives 39 passed.")
row("proj-known-limitation", "2.6-spec", "project.html line 395 'Known limitation'; course/modules/PC/PC3/grader/engine.py docstring lines 1-20", "PASS",
    "engine.py docstring lines 1-20 and the log keys (seed, settlement_cents, turns) confirm the log does not carry the fair path. instance.py is readable, as the page says.")
row("proj-ladder-scope", "2.9-scope", "project.html lines 40-48 (changed this round at lines 44-45); curriculum/06-profession-capstone.yaml lines 175-181", "PASS",
    "Curriculum brief (lines 175-181) says 'in-page market-making game' and 'inventory risk'. The page plays by code (plan section 12 Q1 default), which the plan confirms. Rung claims (full length for rungs 1-2, skip rule) match plan 5.1 and index.html line 74.")
row("proj-rubric-atlas-studios", "2.9-scope", "plans/PC3-build-plan.md section 12 Q16; project.html grep 'atlas'", "PASS",
    "grep -i atlas course/modules/PC/PC3/project.html: no matches. The rubric does not reference atlas studios.")
row("proj-stretch", "2.5-labs", "project.html lines 701-708 (Rung 4 stretch)", "PASS",
    "Read lines 701-708: three specified tasks (distribution over seeds 0-199, informed share 0.6, inventory limit 5) with the method to be stated. Plan 5.1 item 4 specifies the first two; the third is a stated extension.")
row("proj-twin-rules", "2.5-labs", "tests/labs/PC3/lab-PC3-project-1..3.py", "PASS",
    S + "/labs_page_vs_twin_r6.out: each twin run with python -I -W error exits 0 with 0 stderr bytes.")
row("proj-exception-types-labs", "2.5-labs", "project.html Lab 1 replay lines 165-166, 172-173; Lab 3 replay lines 555-556, 560-561", "PASS",
    "Lab 1 and Lab 3 replays raise ValueError with the named messages 'a log has exactly 20 turns' and 'a filled turn needs a fill price' (read this round). Labs never raise in the run.")
row("proj-r4-new-mutants-v18-v20", "2.6-mutants", "ledgers/PC3/mutants/v18, v19, v20", "PASS",
    S + "/mutate_r6_full.out: v18, v19, v20 KILLED.")
row("proj-grader-window-distinct-paths", "2.6-grader", "course/modules/PC/PC3/grader/test_project.py lines 387-391; project.html line 397", "PASS",
    "test_fixed_seeds_0_to_49_give_fifty_different_paths (lines 387-391) asserts 50 distinct paths; the page's 'fifty different fair paths' matches. Independent count: 50 (indep_numbers_r6.out). Uses fixed seeds, so it is the same for every learner.")
row("proj-grader-v21-replay-scales-by-size", "2.6-grader", "course/modules/PC/PC3/grader/test_project.py lines 270-279; ledgers/PC3/mutants/v21_replay_scales_each_fill_by_quoted_size.py", "PASS",
    "Round-5 FAIL resolved. test_a_fill_is_one_unit_whatever_its_quoted_size kills v21 (mutate_r6_full.out: 'KILLED v21 ... -> test_a_fill_is_one_unit_whatever_its_quoted_size (seed 0)'). Page line 395 'A fill is one unit' is now tested.")
row("proj-grader-v22-zero-fill-price-refused", "2.6-grader", "course/modules/PC/PC3/grader/test_project.py lines 282-291; ledgers/PC3/mutants/v22_replay_refuses_a_zero_fill_price.py", "PASS",
    "Round-5 FAIL resolved. test_a_fill_at_price_zero_is_a_legal_fill kills v22 (mutate_r6_full.out). The named refusal is only the None price (page line 416).")
row("proj-rubric-c4-real-form-undefined", "2.6-rubric", "project.html line 626 (C4 level 4) and line 677; course/modules/PC/PC3/L04.html lines 158 and 465", "PASS",
    "Round-5 FAIL resolved. C4 level 4 now names 'the queue of resting orders and a trader who learns from the fills, both set aside in Lesson 4'. L04.html line 465 says the queue is not modelled and that Proposition 3.1 does not cover a learning trader; line 158 describes adverse selection in its simplest form. The phrase 'adverse selection in its real form' is gone from the page.")
row("proj-plan-file-names", "2.6-spec", "project.html lines 393, 443, 448; grader/test_project.py line 26 vs plans/PC3-build-plan.md lines 317, 337-341, 575-579 (Q1 default) and 380 (Q1 wording)", "FAIL",
    "Plan 5.2 and 5.1 item 3 name policy.py (quote) and pnl.py (replay); the Q1 default (plan line 577) is the play interface 'policy.py, pnl.py, game_log.json, analysis.md', and the architect decisions confirm the default play interface (no JavaScript game). The page and grader use market_maker.py throughout. Also plan 5.3 gives play(policy_module, seed); engine.play takes a quote function (engine.py line 49).",
    "Rename the solution file and its references to policy.py and pnl.py (or obtain an architect ruling that changes the plan's file names) and align play's signature with plan 5.3.")
row("proj-exemplar-levels-vs-plan", "2.6-rubric", "project.html line 635 (exemplar-a data-level=2) and line 665 (exemplar-b data-level=4) vs plans/PC3-build-plan.md line 380", "FAIL",
    "Round 5 recorded this row as PASS while quoting the inverted plan. Plan line 380: exemplar-a is data-level 4 and exemplar-b is data-level 2. Page: exemplar-a data-level=2 (scores 2,2,1,2,1) and exemplar-b data-level=4 (scores 4,4,4,3,4). The plan's binding exemplar assignment is inverted.",
    "Swap the exemplar levels so exemplar-a is the level-4 analysis and exemplar-b the level-2 analysis (or obtain an architect ruling and amend plan line 380).")
row("proj-instance-engine-names", "2.6-spec", "grader/engine.py lines 49-58 and grader/instance.py lines 27-53 vs plans/PC3-build-plan.md lines 357-359 and 405-406", "PASS",
    "make_instance(seed) returns seed, start_cents=10000, fair_path_cents (21), arrivals (20 names), settlement_cents, as plan lines 357-359 require. Engine play returns seed, settlement_cents, turns. The play signature difference (quote function vs policy module) is recorded under proj-plan-file-names.")
row("proj-r5-mutant-v23-first-fill-price", "2.6-mutants", "ledgers/PC3/mutants/v23_replay_marks_at_the_first_fill_price.py", "PASS",
    S + "/mutate_r6_full.out: v23 KILLED by test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0).")
row("proj-r5-alternatives-14-16", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r5/alts/alt14, alt15, alt16", "PASS",
    S + "/alts_all_r6.out: alt14, alt15, alt16 each pass 50/50 seeds.")
row("proj-r5-labs-page-vs-twin", "2.5-labs", "project.html lab-PC3-project-1..3 code and expected blocks vs tests/labs/PC3", "PASS",
    S + "/labs_page_vs_twin_r6.out: project-1 0 differing lines, project-2 2 differing (the blanks), project-3 0 differing; each twin output equals its expected block.")
# ---- round-6 rows: new survivors and new findings
row("proj-rubric-c2-level3-admits-mismatch", "2.6-rubric", "project.html line 624 (C2 level 3) against level 2 (line 624) and level 4 (line 624); bar sentence at lines 397 and 620", "FAIL",
    "C2 level 3 reads 'Cites three turns by number and field, and at least one cited value does not match the log'. Level 2 requires values from the log, and level 4 requires every value to match. The ladder is not monotone in accuracy: an analysis with a wrong cited value meets the stated bar (level 3 or above), while a correct but thinner one does not reach it at level 3. The annotations (lines 655-656) do not address the mismatch.",
    "Make level 3 require every cited value to match the log (for example 'Cites three turns by number and field, every cited value matches the log, with one turn or field omitted'), and move a mismatched value to level 2 or 1.")
row("proj-grader-v24-stderr-print-survives", "2.6-mutants", "ledgers/PC3/mutants/v24_replay_prints_a_debug_line_to_stderr.py (new this round); course/modules/PC/PC3/grader/test_project.py lines 358-362", "FAIL",
    "Student error: replay writes a debug line to sys.stderr. " + S + "/mutate_r6_full.out: SURVIVED. Page line 395 says 'No function prints or warns', and test_no_function_prints (lines 358-362) reads only stdout.",
    "In test_no_function_prints, also assert capsys.readouterr().err == '' (both streams) and rerun; the mutant must then be KILLED.")
row("proj-grader-v25-last-filled-totals-survives", "2.6-mutants", "ledgers/PC3/mutants/v25_replay_takes_totals_from_last_filled_turn.py (new this round); course/modules/PC/PC3/grader/test_project.py lines 257-267", "FAIL",
    "Student error: replay copies cash_after_cents and inventory_after from the last filled turn. " + S + "/mutate_r6_full.out: SURVIVED. The hand-built stale-totals test (lines 257-267) has one fill, so the last filled turn's totals equal the sum of the fills. Page Conventions line 407 says the cash flow is 'the sum of the fill cash flows'.",
    "Add a hand-built log with at least two fills and stale running totals on the last filled turn (for example fills on turns 1 and 3 with a wrong cash_after_cents and inventory_after on turn 3), and check replay against the oracle.")
row("proj-grader-v26-logging-warning-survives", "2.6-mutants", "ledgers/PC3/mutants/v26_quote_logs_a_warning_through_logging.py (new this round); course/modules/PC/PC3/grader/test_project.py lines 30, 358-362", "FAIL",
    "Student error: quote calls logging.warning on every turn. " + S + "/mutate_r6_full.out: SURVIVED. Page line 395 says 'No function prints or warns'; the suite's warnings filter (line 30) covers only the warnings module, and no test reads log records.",
    "Add a caplog check in test_no_function_prints that asserts no log record is emitted by quote or replay; the mutant must then be KILLED.")
row("proj-plan-grader-seed-scope", "2.6-spec", "plans/PC3-build-plan.md section 5.2 'Grading' (line 348) and section 5.6 legality, replay, cash and P&L bullets ('For seeds 0-49'); FINAL-ARCHITECT-RULINGS item 10 ('pass seeds 0-49') vs project.html line 397 and grader/test_project.py line 33", "FAIL",
    "The plan's grader runs the legality, replay, cash and P&L checks on seeds 0-49 ('dual mode: policy.py and pnl.py on seeds 0-49'). The suite runs the 16 seed-dependent checks on two seeds only (the learner's and seed + 7919, test_project.py line 33). Seeds 0-49 appear only in the distinctness test (lines 387-391). The page is internally consistent, but it does not implement the plan's grading scope and the hub repeats the plan's wording (index.html lines 55, 160).",
    "Run the 16 seed-dependent checks over seeds 0-49 as well as the learner's seed (the browser run is 0.8 s for 39 tests, so the cost fits), or obtain an architect ruling that changes plan 5.2 and 5.6 and the hub wording.")

# ---- mutants
mutants = []
for line in (ROOT / S / "mutate_r6_full.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+\.py): (.*?) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, killer = m.groups()
    killer = killer.strip()
    killed_by = None if status == "SURVIVED" else killer.rsplit(" ->", 1)[0] if False else killer
    mutants.append({
        "id": fname[:-3],
        "file": f"ledgers/PC3/mutants/{fname}",
        "description": desc.strip(),
        "killed_by": None if status == "SURVIVED" else killer,
        "status": status,
    })
mutants.sort(key=lambda d: d["id"])

verdict = "FAIL"
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
ledger = {
    "unit": "PC3",
    "slice": "c",
    "round": 6,
    "verifier": "independent verifier (Haiku 5.5), round 6, slice c (did not build PC3)",
    "pin": "4bd8cb9",
    "base": "round 5 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round5.json (pin 7376a5e). Delta 7376a5e..4bd8cb9 for slice c: project.html (lines 44-45, 397, 626, 677 changed), grader/test_project.py (two tests added at lines 270-291, later lines shift by 24), mutants v21-v23 (already in round 5 pin ledger) and no change to alternatives, index.html, references, notation, tools or plans. L01-L06 and cards.json changed (slices a, b, d; not read here, L04.html hunks at lines 52, 175, 690 checked for the cited lines only).",
    "checkout": str(ROOT),
    "scratch": "/tmp/pc3c-r6-ws (ref/, st/, cmd/); scripts and outputs in " + S,
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Full reads this round: project.html (732 lines, every line), grader engine.py, instance.py, reference.py, starter.py, test_project.py (442 lines, every line), the three project lab twins (via the page-vs-twin comparison and the page code reads), mutants v21-v26 and every new alternative. The round-5 PASS row proj-exemplar-levels-vs-plan was wrong and is now FAIL.",
        "Gates run once on the pin (" + S + "/run_gates_r6.sh): check_pages, check_dag, check_projects, run_labs (project 3/3), run_graders 0-49 (50/50 reference), mutate_graders 0-49 (32/35 killed; the three survivors are FAIL rows), page_smoke (project), ruff check and format, mypy --no-incremental, verify_refs --offline (560 entries, 0 problems), pytest -k PC3 (passed). The mutate run was also written to " + S + "/mutate_r6_full.out.",
        "Alternatives: 19 files (alt1-6, alt7-10, alt11-13, alt14-16, and alt17-19 written this round) run through run_alts_r6.py on seeds 0-49: every one passes 50/50. No over-constraint found.",
        "Independent numbers: indep_numbers_r6.py re-derives the Lab 1 numbers, the Exemplar B sums, the Lab 3 counterfactual (15 cents: 9 fills, P&L 55, change 25), the largest inventory (3) and the 50 distinct fixed-seed paths from the page's stated rules, without the page's code. All match.",
        "Scope notes (not failed): the rubric's C5 level 3 'names one check and its result, without a value' is ambiguous; read as 'result named without its number', which the page can support. The starter's docstring says every input the spec names as invalid must raise ValueError, while the spec puts the quote refusals on the engine; the suite does not require it of the quote, so no finding.",
        "Not checked: render_curriculum, build_site --check, fetch_data --check and the full repo gate (outside slice c); L01-L06 and cards.json (slices a, b, d); index.html beyond the cited lines; the grader.js rendering in a real browser (source read and in-browser pytest output read only); learner seeds outside 0-49 and the seed-derivation value of a real workspace; run_graders over all units; the full pytest suite (only -k PC3 run).",
    ],
    "summary": {
        "rows": len(R),
        "PASS": counts["PASS"],
        "FAIL": counts["FAIL"],
        "UNVERIFIABLE": counts["UNVERIFIABLE"],
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
        "mutants_survived": sum(1 for m in mutants if not m["killed_by"]),
        "alternatives_passing": "19 of 19 (50/50 seeds each)",
        "gates": "check_pages, check_dag, check_projects, run_labs, run_graders, page_smoke, ruff, mypy, verify_refs PASS; mutate_graders FAIL (32/35); pytest -k PC3 PASS; collect 39",
    },
}
out = ROOT / "ledgers/PC3/PC3-c.json"
out.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(R), counts, "mutants", len(mutants), "survived", [m["id"] for m in mutants if not m["killed_by"]])
