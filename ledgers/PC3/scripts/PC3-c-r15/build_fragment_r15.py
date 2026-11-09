"""Round 15 fragment builder for PC3 slice c (verifier scratch). Reads the round-14 fragment for the row ids and the
decisions taken this round, reads the mutant run output, and writes ledgers/PC3/PC3-c.json."""
import ast, json, re, glob, datetime
from pathlib import Path

REPO = Path("/Users/billyribeiro/.fanout/wt/verifyE15-PC3-c")
S = REPO / "ledgers/PC3/scripts/PC3-c-r15"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-PC3-c.round14.json"))
CARRY_PREFIX = ("Carried from round 14 (cited lines byte-identical since the previous pin 8e5751c; the round-15 changed lines are "
                "project.html 397 and 633, plans/PC3-build-plan.md 406-408, 424, 430-433, test_project.py 119-123, 162, 336-357, "
                "439-440, 520-522; this row cites none of them): ")
TEST_NOTE = ("Test line numbers in this row are the round-14 numbers; the round-15 insertion at test_project.py 336-357 moves "
             "later tests by +22 lines, and the test bodies are unchanged. ")

# Fresh decisions made in this round: id -> (status, check, location, evidence, fix)
FRESH = {}
def fresh(i, status, loc, ev, fix=None, check=None):
    FRESH[i] = dict(status=status, location=loc, evidence=ev, fix=fix, check=check)

fresh("proj-grader-replay-from-fills", "PASS",
      "course/modules/PC/PC3/project.html line 407 (Conventions: 'the cash flow the sum of the fill cash flows ... carry no rounding'); course/modules/PC/PC3/grader/test_project.py lines 336-357 (new test)",
      "Round 15 (pin d1e65a0): test_a_fill_at_any_integer_cent_price_is_booked_exactly (lines 336-357) books fills at 10005 and 10003 and checks replay == oracle; the oracle gives cash flow 2 and inventory 0. Mutant r14_01 (rounds fill prices to the dime) is KILLED by it on seed 0 (out/mutate_pc3_0_49.out; out/mutate_pc3_73.out).")
fresh("proj-exemplar-scores-blind-disclosure", "FAIL",
      "course/modules/PC/PC3/project.html line 635 (data-scores=\"4,4,4,3,4\"), line 664 (data-scores=\"2,2,1,2,1\"), lines 651-690 (annotations); this verifier's read record",
      "Blind condition not met this round: the round-15 diff hunk output of project.html around line 635 printed data-scores=\"4,4,4,3,4\" for Exemplar A before any score was written, and the round-14 fragment (read at the start of this round) printed the Exemplar B levels 2,2,1,2,1. Those scores cannot be unseen, so this verifier cannot certify a blind scoring of either exemplar. The scores in this round were not produced blind and are not used as evidence. Ruling 15's text is not in verifier-rules.md, so the blind requirement applied is the page's own instruction to score before revealing.",
      fix="Re-run the exemplar scoring with a verifier that has not read project.html lines 633-692 or the round-14 fragment, and keep the official levels out of the served page (see proj-exemplar-scores-in-served-html).")
fresh("proj-direct-legal-sweep-turn20-no-history", "PASS",
      "course/modules/PC/PC3/grader/test_project.py test_a_direct_quote_is_legal_at_every_inventory_within_the_limit (lines 520-528) and direct_states (lines 118-135)",
      "direct_states now sweeps range(1, HORIZON + 1) (line 123), so every turn 1..20 at inventories -10..10 is quoted. Mutant r14_03 (locked quote at inventory -10 on turns 2-19) is KILLED by this test on seed 0 (out/mutate_pc3_0_49.out). Control: all 52 alternative correct implementations pass 50/50 (out/alts/SUMMARY.txt).")
fresh("proj-no-print-rare-branch-survivors", "PASS",
      "course/modules/PC/PC3/grader/test_project.py test_no_function_prints_or_warns (lines 434-466) and direct_states (lines 118-135); ledgers/PC3/mutants/s14_01_quote_prints_on_turn_thirteen_at_inventory_seven.py",
      "s14_01 (debug print on turn 13 at inventory +7) is KILLED by test_no_function_prints_or_warns[27] on seed 0 (out/mutate_pc3_0_49.out). The sweep reaches turn 13 at inventory 7 through direct_states. The class of branch not reached by the stated checks is recorded in proj-r15-quote-warns-turn-twenty-after-fill and proj-r15-replay-prints-at-plus-ten.")
fresh("proj-exemplar-scores-in-served-html", "FAIL",
      "course/modules/PC/PC3/project.html line 635 (article data-scores=\"4,4,4,3,4\", data-level=\"4\") and line 664 (data-scores=\"2,2,1,2,1\"); annotation asides lines 651-660 and 680-690; course/assets/js/rubric.js line 149",
      "Re-checked this round: grep of project.html shows data-scores at lines 635 and 664 (unchanged since pin 8e5751c). The official levels and the annotations are in the served source, and rubric.js hides only the presentation. The self-assessment paragraph (line 696) now says both are in the page source, which is accurate, but the leak remains.",
      fix="Do not serve data-scores or annotation text in the page source; load them only after the reader has stored a self-score (the page would need a separate JSON that is fetched on reveal).")
fresh("proj-plan-5-6-tests-not-in-suite", "PASS",
      "plans/PC3-build-plan.md lines 420-423 (inventory bullet) and 430-433 (seed-consistency bullet); course/modules/PC/PC3/grader/test_project.py lines 563-574 (test_fills_stop_at_the_inventory_limit_in_each_direction) and 422-430 (test_a_log_carries_its_own_seed_and_settlement)",
      "Inventory bullet: test_fills_stop_at_the_inventory_limit_in_each_direction exists (line 563); no game-log test asserts |inventory_after| <= 10 (grep of inventory_after in test_project.py: line 108 is the record key, and the only asserts are lines 278, 574 and 606, none of them on a game log bound |inventory| <= 10). Seed bullet: the sentence 'No test refuses a log copied from another seed: the check plays each game itself' is accurate; test_a_log_carries_its_own_seed_and_settlement (lines 422-430) calls engine.play(sol.quote, seed) and compares log['seed'] and the settlement with make_instance(seed).")
fresh("proj-r14-grader-rounding-survivor", "PASS",
      "ledgers/PC3/mutants/r14_01_replay_rounds_fill_prices_to_the_dime.py; course/modules/PC/PC3/project.html line 406 and line 407",
      "KILLED on seed 0 by test_a_fill_at_any_integer_cent_price_is_booked_exactly (out/mutate_pc3_0_49.out, this round).")
fresh("proj-r14-grader-locked-market-survivor", "PASS",
      "ledgers/PC3/mutants/r14_03_quote_locks_the_market_at_the_limit_mid_game.py; course/modules/PC/PC3/project.html line 395",
      "KILLED on seed 0 by test_a_direct_quote_is_legal_at_every_inventory_within_the_limit (out/mutate_pc3_0_49.out, this round), after the sweep was extended to turns 1-20.")
fresh("proj-r14-grader-print-survivor", "PASS",
      "ledgers/PC3/mutants/s14_01_quote_prints_on_turn_thirteen_at_inventory_seven.py; course/modules/PC/PC3/project.html line 395",
      "KILLED on seed 0 by test_no_function_prints_or_warns[27] (out/mutate_pc3_0_49.out, this round).")
fresh("proj-r14-grader-offgrid-survivor", "PASS",
      "ledgers/PC3/mutants/s14_02_replay_refuses_a_fill_off_the_dime_grid.py; course/modules/PC/PC3/project.html line 395 and 407",
      "KILLED on seed 0 by test_a_fill_at_any_integer_cent_price_is_booked_exactly (out/mutate_pc3_0_49.out, this round).")
fresh("proj-r14-mutants-aggregate", "PASS",
      "ledgers/PC3/mutants/ (the 70 files that existed at pin d1e65a0: m01-m10, v01-v49 without v17, r13_01-05, r14_01-04, s14_01-03)",
      "tools/mutate_graders.py --unit PC3 --seeds 0-49 on the 70 files: 70/70 KILLED (out/mutate_pc3_0_49.out, 'mutate_graders PC3: PASS (70/70 killed)'). The three new mutants of this round are in their own rows (73-file run: out/mutate_pc3_73.out).")
fresh("proj-r14-plan-cash-identity-sign", "PASS",
      "plans/PC3-build-plan.md line 424 ('Cash identity: cash_after changes by exactly +ask on a maker sale at the ask and by -bid on a maker purchase at the bid')",
      "Now matches project.html line 406 (maker purchase at bid: cash -b; maker sale at ask: cash +a), engine.py maker_side and the grader test_cash_moves_by_the_fill_price_on_each_turn (lines 393-406), which checks the same signs.")
fresh("proj-r14-plan-instance-sample-count", "PASS",
      "plans/PC3-build-plan.md line 406 ('give materially different fair paths (the test counts distinct paths over the fifty fixed seeds 0 to 49)')",
      "test_fixed_seeds_0_to_49_give_fifty_different_paths (lines 553-557) counts over range(50) and expects 50. Run: tools/run_graders.py --unit PC3 --seeds 0-49 reference 50/50 (out/run_graders_0_49.out).")
fresh("proj-r14-plan-reference-description", "PASS",
      "plans/PC3-build-plan.md lines 407-408 ('quote posts a symmetric quote around the last filled price in the public history (or start_cents before any fill), with a half-spread of 10 cents and size 1'); course/modules/PC/PC3/grader/reference.py lines 15-23",
      "reference.py quote: mid = START_CENTS (10000), then the last record with filled True sets mid to its fill_price_cents; returns (mid-10, mid+10, 1). The plan sentence matches; the earlier 'last fair value the public history implies' wording is gone.")

# Round-15 specific rows (new ids)
fresh("proj-r15-replay-prints-at-plus-ten", "FAIL",
      "ledgers/PC3/mutants/r15_01_replay_prints_at_ending_inventory_plus_ten.py; course/modules/PC/PC3/project.html line 395 ('Neither quote nor replay prints or warns'); course/modules/PC/PC3/grader/test_project.py test_no_function_prints_or_warns (lines 434-466, replay logs at lines 442-455)",
      "New student-error mutant written this round: replay prints when the ending inventory is exactly +10. Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-c-r15/run_cand_r15.py ledgers/PC3/mutants/r15_01_*.py range -> exit=0 on all 50 seeds (SURVIVED). Probe (ledgers/PC3/scripts/PC3-c-r15/new_mutant_probe_r15.py) shows the branch fires ('debug: ending inventory 10') on a +10 log. The replay logs the no-print test passes are the game, no_fill, zero_fill and ends_at_minus_ten logs (ending -10); none ends at +10, and no fixed seed's game does.",
      fix="Add a hand-built log that ends at +10 units (ten fills at the bid, then flat turns) to the logs replayed in test_no_function_prints_or_warns, mirroring ends_at_minus_ten.")
fresh("proj-r15-quote-warns-turn-twenty-after-fill", "FAIL",
      "ledgers/PC3/mutants/r15_02_quote_warns_on_turn_twenty_at_inventory_minus_nine.py; course/modules/PC/PC3/project.html line 395 ('Neither quote nor replay prints or warns'); course/modules/PC/PC3/grader/test_project.py direct_states (lines 118-135: histories hold unfilled records only)",
      "New student-error mutant written this round: quote calls warnings.warn on turn 20 at inventory -9 when turn 19 was a fill. Run on seeds 0-49: exit=0 on all 50 seeds (SURVIVED). Probe: the warning fires for that state ('inventory -9 after a fill on turn 19'). direct_states builds histories with no fill records, so the sweep never reaches a state with a fill in its history; the game does not reach this state on seeds 0-49.",
      fix="Give the no-print sweep (direct_states or a second list) histories that contain fills at a few prices, and include turn 20 at inventory -9 after a fill on turn 19.")
fresh("proj-r15-quote-locked-after-fill-history", "FAIL",
      "ledgers/PC3/mutants/r15_03_quote_locks_the_market_on_turn_five_at_inventory_minus_one.py; course/modules/PC/PC3/project.html line 395 ('A quote must have its bid below its ask'); course/modules/PC/PC3/grader/test_project.py test_a_direct_quote_is_legal_at_every_inventory_within_the_limit (lines 520-528) and test_a_direct_call_on_a_hand_built_state_ignores_an_earlier_game (lines 487-516)",
      "New student-error mutant written this round: quote posts bid == ask on turn 5 at inventory -1 when the last filled price is 10020. Run on seeds 0-49: exit=0 on all 50 seeds (SURVIVED). Probe: quote returns (10020, 10020, 1) on the state. The legality sweep builds histories with no fills (mid 10000), so it never sees a locked quote after a fill; the direct-call test builds this exact state (turn 5, inventory -1, fill at 10020 on turn 2) but checks only that two calls agree.",
      fix="Extend the legality sweep with histories that hold fills at several prices (for example the last filled price in 9980..10020), so every quoted state after a fill is checked for bid below ask.")
fresh("proj-r15-direct-states-log-wording", "FAIL",
      "course/modules/PC/PC3/project.html line 397 ('each later turn with the unfilled records of the earlier turns of the log'); course/modules/PC/PC3/grader/test_project.py direct_states (lines 118-135) and test_a_direct_quote_is_legal_at_every_inventory_within_the_limit docstring (lines 520-522)",
      "The sentence says the third check's states hold 'the unfilled records of the earlier turns of the log'. The code builds them by hand: history = [turn_record(t, size=1, filled=False) for t in range(1, turn)] (line 132). No log is read or used, and the records are synthetic (bid 9990, ask 10010, arrival uninformed-sell). The test docstring (520-522) says 'the unfilled records of turns 1 to t-1', which is accurate.",
      fix="In project.html line 397 replace 'the unfilled records of the earlier turns of the log' with 'hand-built unfilled records for the earlier turns', matching the docstring.")
fresh("proj-r15-grading-counts", "PASS",
      "course/modules/PC/PC3/project.html line 397 (487 checks for seeds 0-49, 496 otherwise; 25 seed-only; 3 no-seed; 9 x 51 and 9 x 52)",
      "pytest --collect-only -q via run_cand_r15.py --collect: seed 0 -> 487 tests collected, seed 7 -> 487, seed 100 -> 496 (ledgers/PC3/scripts/PC3-c-r15/out/*). Split: 9 per-seed tests x 51 seeds = 459 for seed 0; the remaining 28 = 25 seed-only + 3 no-seed, matching the page. 51 seeds for a learner seed in 0-49 and 52 otherwise (test_project.py lines 36-38).")
fresh("proj-r15-exemplar-intro-fill-numbers", "PASS",
      "course/modules/PC/PC3/project.html line 633 (intro: 'numbers that follow from a fill price') and the exemplar numbers at lines 635-690",
      "Recomputed independently (ledgers/PC3/scripts/PC3-c-r15/numbers_r15.py) on seed 0 with the reference: 9 fills at turns 2,3,4,5,7,8,13,18,19; replay cash flow -9950, inventory 1, mark 9980, P&L 30; bid-fill sum 49910 (turns 2,3,4,8,19), ask-fill sum 39960 (turns 5,7,13,18); max |inventory| 3; turn 5 fill at 9980 (ask); turn 2 fill at 9990 (bid); turn 18 fill at 10000 (ask) leaving inventory 0; wider half-spread 15 gives 9 fills and P&L 55 (change +25). Every number in Exemplar A and Exemplar B matches; the new permission for numbers 'that follow from a fill price' is not used beyond sums and fill prices.")
fresh("proj-r15-integer-cent-test", "PASS",
      "course/modules/PC/PC3/grader/test_project.py lines 336-357 (test_a_fill_at_any_integer_cent_price_is_booked_exactly); plans/PC3-build-plan.md lines 430-432 (Fill prices bullet)",
      "Hand-built log: turn 1 sale at the ask 10005 (maker cash +10005, inventory -1), turn 2 purchase at the bid 10003 (cash -10003, inventory 0), settlement 10003. oracle gives cash 2, inventory 0, mark 0, P&L 2; the docstring's '10005 - 10003 = 2 cents' is correct. Killed mutant r14_01 and s14_02 (out/mutate_pc3_0_49.out).")
fresh("proj-r15-alternatives-all", "PASS",
      "ledgers/PC3/alternatives/alt1..alt6; ledgers/PC3/scripts/PC3-c-r1..r14 alt modules (52 candidate modules; list in ledgers/PC3/scripts/PC3-c-r15/alt_candidates.txt)",
      "Each of the 52 correct candidate modules (every alt*.py that defines quote and replay) run on seeds 0-49 against the pinned suite: 52 of 52 pass 50/50 (out/alts/SUMMARY.txt, out/alts/*.txt). Six run_*.py scripts that the file scan also matched are runners, not candidates, and were excluded (pass=0 by construction).")
fresh("proj-r15-labs-twins-isolated", "PASS",
      "tests/labs/PC3/lab-PC3-project-1.py, -2.py, -3.py; course/modules/PC/PC3/project.html lab-PC3-project-1..3",
      "Each twin run from a scratch directory with python -I -W error: exit 0 for all three (run 1 prints 'largest |inventory| over the run = 3 (limit 10): True'). run_labs --unit PC3 --page project: PASS (3/3). Labs and their page blocks are byte-identical to pin 8e5751c (not in the delta).")
fresh("proj-r15-gates", "PASS",
      "tools/check_pages.py, check_dag.py, check_projects.py (--unit PC3); page_smoke.py --pages project.html; run_labs.py --page project; run_graders.py --seeds 0-49; ruff check and ruff format --check; mypy --no-incremental; pytest -k PC3; verify_refs.py --offline; fetch_data.py --check; build_site.py --check",
      "All exit 0: check_pages PASS, check_dag PASS, check_projects PASS, page_smoke PASS, run_labs PASS (3/3), run_graders PASS (reference 50/50), ruff check 'All checks passed!', ruff format '14 files already formatted', mypy 'no issues found in 385 source files', pytest -k PC3 (exit 0), verify_refs '560 entries, 0 problems', fetch_data '3 datasets, 0 problems', build_site 'site data current: 6 outputs' (out/ALL_EXIT.txt).")
fresh("proj-r15-mypy-strict-grader", "PASS",
      "scratch copy of course/modules/PC/PC3/grader/engine.py, instance.py, test_project.py and market_maker.py (= reference.py)",
      "mypy --strict on the four files: 'Success: no issues found in 4 source files'.")
fresh("proj-r15-starter-fails", "PASS",
      "course/modules/PC/PC3/grader/starter.py with test_project.py (seeds 0 and 7)",
      "Starter fails the suite: 'failed, 66 passed' on seed 0 and seed 7 (out/starter_r15.out, via run_cand_r15.py).")


fresh("proj-grader-35-checks", "PASS",
      "course/modules/PC/PC3/project.html line 397 (487 / 496 checks; 9 x 51 + 25 + 3 and 9 x 52 + 25 + 3); course/modules/PC/PC3/grader/test_project.py",
      "Collect-only this round: 487 tests for seeds 0 and 7, 496 for seed 100 (out/*; run_cand_r15.py --collect). The page's split (nine per-seed checks, 25 seed-only, three no-seed) matches the test list: nine tests parametrized over SEEDS, 25 seed-only tests, and test_fixed_seeds_0_to_49_give_fifty_different_paths, test_a_direct_call_on_a_hand_built_state_ignores_an_earlier_game and test_a_direct_quote_is_legal_at_every_inventory_within_the_limit as the no-seed checks.")
fresh("proj-grader-seed-scope-claim", "PASS",
      "course/modules/PC/PC3/project.html line 397 ('51 seeds when your seed is one of 0 to 49, and 52 otherwise') against grader/test_project.py lines 36-38",
      "SEEDS = tuple(dict.fromkeys((*FIXED_SEEDS, SEED, SEED + 7_919))) with FIXED_SEEDS = range(50): 51 distinct seeds for SEED in 0-49 and 52 otherwise (checked by collect counts 487 for seed 0 and 496 for seed 100).")
fresh("proj-hub-seed-scope", "PASS",
      "course/modules/PC/PC3/index.html lines 55 and 160 against course/modules/PC/PC3/project.html line 397 (seeds clause)",
      "index.html 160: 'runs them on seeds 0 to 49, on your own workspace seed, and on that seed plus 7919'; project.html 397 gives the same seed set (51 or 52 seeds). index.html is byte-identical to pin 8e5751c (not in the delta).")
fresh("proj-grader-no-print", "PASS",
      "course/modules/PC/PC3/grader/test_project.py test_no_function_prints_or_warns (lines 434-466) and its docstring (lines 437-440)",
      "The test runs quote and replay on the game of each seed, on the no_fill, zero_fill and ends_at_minus_ten logs, and on direct_states() (every turn 1..20, inventory -10..10), with capsys, caplog and warnings recording. The docstring's list of reached branches matches the code.")
fresh("proj-r14-reach-and-instances", "PASS",
      "course/modules/PC/PC3/grader/test_project.py test_no_function_prints_or_warns docstring (lines 437-440) and instance tests (lines 534-557)",
      "Docstring: 'The checks reach branches that a game of the fixed seeds never takes: a log with no fill, a fill at price 0, a log that ends at inventory -10, and the quotes of the direct states at every turn from 1 to 20 and every inventory from -10 to 10.' Matches the code and the sweep.")
fresh("proj-exemplar-a-numbers", "PASS",
      "course/modules/PC/PC3/project.html lines 635-662 (exemplar A) against ledgers/PC3/scripts/PC3-c-r15/numbers_r15.py output",
      "Every exemplar A number recomputed this round (see proj-r15-exemplar-intro-fill-numbers): cash flow -9950, inventory 1, mark 9980, P&L 30, nine fills at turns 2,3,4,5,7,8,13,18,19, bid sum 49910, ask sum 39960, wide-spread P&L 55 (+25), max inventory 3.")
fresh("proj-exemplar-b-numbers", "PASS",
      "course/modules/PC/PC3/project.html lines 664-690 (exemplar B) against ledgers/PC3/scripts/PC3-c-r15/numbers_r15.py output",
      "Exemplar B states P&L 30 and cash flow -9950 (both match replay on seed 0) and turn 5 sold at the ask of 9980 (turn 5 fill: ask, 9980). No other number is stated.")
fresh("proj-banned-and-process-words", "PASS",
      "course/modules/PC/PC3/project.html (lines 397 and 633 read in full this round); grader/*.py; tests/labs/PC3/lab-PC3-project-*.py",
      "Grep for process words (round, verifier, fixer, builder, batch, mutant, survivor) on project.html, test_project.py and reference.py: no hit in learner text; the only 'reference' hits are the rule name (project.html 466) and docstrings of reference.py.")
fresh("proj-r14-plan-inventory-bullet", "PASS",
      "plans/PC3-build-plan.md lines 420-423 (inventory bullet) against course/modules/PC/PC3/grader/test_project.py test_fills_stop_at_the_inventory_limit_in_each_direction (lines 563-574)",
      "The bullet's claim (both directions: an order reaching 10 fills, one reaching 11 does not; no assertion of |inventory_after| <= 10 on game logs) matches the test at lines 563-574 and the grep in proj-plan-5-6-tests-not-in-suite.")

# Carry-or-fresh for the pass rows that this round re-ran (mutants, alternatives, tools) are fresh above.
RERUN_BY_PREFIX = {
    "proj-builder-mutants": "All ten m-series mutants KILLED on seeds 0-49 this round (out/mutate_pc3_0_49.out).",
    "proj-verifier-mutants": "v-series mutants KILLED this round (out/mutate_pc3_0_49.out).",
}

def evidence_for(row):
    rid = row["id"]
    if rid in FRESH:
        d = FRESH[rid]
        return d["status"], d["location"], d["evidence"], d.get("fix")
    return None

rows = []
prev_rows = prev["rows"]
for r in prev_rows:
    rid = r["id"]
    if rid in FRESH:
        d = FRESH[rid]
        out = {"id": rid, "check": r["check"], "location": d["location"], "status": d["status"], "evidence": d["evidence"]}
        if d["status"] != "PASS":
            out["fix"] = d["fix"]
        rows.append(out)
        continue
    # carried: subject lines unchanged this round (see CARRY_PREFIX); status PASS as in round 14
    assert r["status"] == "PASS", f"round-14 non-PASS row not decided: {rid}"
    ev = CARRY_PREFIX + r["evidence"]
    if "test" in r["location"]:
        ev = ev + " " + TEST_NOTE
    if r["location"].startswith("ledgers/PC3/mutants") or "mutants/" in r["location"]:
        ev = ev + " Re-run this round on all 73 mutants: the killer named in the mutants array is the killer in out/mutate_pc3_73.out where the mutant is listed."
    if "alternatives" in r["location"] or "alts" in r["location"]:
        ev = ev + " Re-run this round: the candidate passes 50/50 on the pinned suite (out/alts/SUMMARY.txt)."
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})

for rid, d in FRESH.items():
    if not any(r["id"] == rid for r in prev_rows):
        out = {"id": rid, "check": rid.replace("proj-", "2.6-") , "location": d["location"], "status": d["status"], "evidence": d["evidence"]}
        if d["status"] != "PASS":
            out["fix"] = d["fix"]
        rows.append(out)

# Mutants: all files at the pin, description from the docstring, killer from the 73-file run output.
mut_text = (S / "out/mutate_pc3_73.out").read_text(encoding="utf-8") if (S / "out/mutate_pc3_73.out").exists() else ""
killers = {}
for m in re.finditer(r"^(KILLED|SURVIVED) (\S+?): (.*?) -> (.*)$", mut_text, re.M):
    killers[m.group(2)] = (m.group(1), m.group(4).strip())
mutants = []
for f in sorted(glob.glob(str(REPO / "ledgers/PC3/mutants/*.py"))):
    name = Path(f).name
    desc = ast.get_docstring(ast.parse(Path(f).read_text(encoding="utf-8"))) or "(no description)"
    desc = desc.splitlines()[0]
    status, killed = killers.get(name, (None, None))
    mutants.append({"id": name, "description": desc, "killed_by": killed if status == "KILLED" else None})

counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
killed_n = sum(1 for m in mutants if m["killed_by"])
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) and killed_n == len(mutants) else "FAIL"
fragment = {
    "unit": "PC3",
    "slice": "c",
    "round": 15,
    "verifier": "independent verifier (Haiku 5.5), round 15, slice c; did not build PC3",
    "pin": "d1e65a0",
    "base": ("round 14 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round14.json (pin 8e5751c). Delta 8e5751c..d1e65a0 for slice c: "
             "project.html 397 (grading-mode counts) and 633 (exemplar intro); grader/test_project.py 119-123, 162, 336-357 (new test), 439-440, 520-522; "
             "plans/PC3-build-plan.md 406-408, 424, 430-433; ledgers/PC3/mutants r14_01-04 and s14_01-03 (added, all killed). L04.html 64, 83, 483 changed (outside this slice; cited L04 lines 60 and 482 are byte-identical)."),
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE15-PC3-c (detached at d1e65a02, the pin; the checkout was 9ca1d8cb before this round and was moved to the pin)",
    "scratch": "ledgers/PC3/scripts/PC3-c-r15/ (gates_r15.sh, out/, run_cand_r15.py, alts_batch_r15.sh, numbers_r15.py, new_mutant_probe_r15.py, build_fragment_r15.py); /tmp/pc3c_r15_probe (scratch)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "Round-14 blind exemplar scoring is not repeated: the scores were visible in this round's tool output before scoring (proj-exemplar-scores-blind-disclosure FAIL).",
        "Three new surviving grader mutants (r15_01..03) are FAIL rows against project.html line 395."
    ],
    "notes": [
        "Pin: the task named d1e65a0; the checkout was at 9ca1d8cb (an ancestor) and was detached at d1e65a02 before any check. All commands ran at d1e65a02.",
        "Full slice read: grader/test_project.py (609 lines) read in full; project.html changed hunks (397, 633) and the Conventions, rubric, exemplar and hours regions read; plans/PC3-build-plan.md 400-436 read in full. Not re-read this round: project.html lines 1-390, 441-630 and 700-720 except the regions named in rows (they are byte-identical to pin 8e5751c, which the round-14 fragment read in full).",
        "Carried rows: " + str(sum(1 for r in rows if str(r["evidence"]).startswith("Carried from round 14"))) + " round-14 PASS rows whose cited lines are unchanged are carried with the carry prefix; test-line numbers after line 336 are the round-14 numbers (+22 shift).",
        "The alternatives scan matched six runner scripts (r10_run_alts.py, r11_run_alts.py, r12_run_alts.py, r8v_run_older_alts.py, r9v_run_all_alts.py, r9v_run_alts.py) in addition to 52 candidate modules; they were not run as candidates.",
        "Ruling 15 text is not in /Users/billyribeiro/.fanout/verifier-rules.md; the blind requirement was applied as the page states it.",
        "L04.html changed at lines 64, 83 and 483 in this delta; these are outside slice c and no row in this slice cites them.",
    ],
    "summary": "",
}
fragment["summary"] = (f"PC3-c round 15: verdict {verdict}. Rows {len(rows)}: PASS {counts.get('PASS',0)}, FAIL {counts.get('FAIL',0)}, "
                       f"UNVERIFIABLE {counts.get('UNVERIFIABLE',0)}. Mutants {killed_n}/{len(mutants)} killed on seeds 0-49 "
                       f"(survivors: {', '.join(m['id'] for m in mutants if not m['killed_by']) or 'none'}). "
                       "Alternatives: 52 of 52 correct implementations pass 50/50.")
out = REPO / "ledgers/PC3/PC3-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, verdict, counts, f"mutants {killed_n}/{len(mutants)}")
