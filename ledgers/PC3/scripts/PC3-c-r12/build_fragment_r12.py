"""Round 12 verifier (PC3 slice c): builds ledgers/PC3/PC3-c.json from the round 11 fragment and this round's outputs.

Carried rows keep their id and their round-11 evidence, with the carry prefix; rows whose subject changed in the
delta 11d7077a..5db69a9b, and every row re-run this round, carry new evidence. Run from the checkout root."""

import json
import re
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE12-PC3-c"
S = f"{ROOT}/ledgers/PC3/scripts/PC3-c-r12"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-PC3-c.round11.json", encoding="utf-8"))

# ---- mutants: parse this round's full run (seeds 0-49) -------------------------------------------------------
mut_lines = open(f"{S}/mutate_r12_0-49_all.out", encoding="utf-8").read().splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    killed_by = None if killer.strip() == "None" else killer.strip()
    mutants.append({"id": name, "description": desc, "killed_by": killed_by,
                    "status": "KILLED" if killed_by else "SURVIVED"})
assert len(mutants) == 58, len(mutants)
mut_by = {m["id"]: m for m in mutants}


def kill(prefix_list):
    """Evidence for a list of mutant prefixes, taken from this round's run."""
    out = []
    for p in prefix_list:
        hits = [m for m in mutants if m["id"].startswith(p)]
        for m in hits:
            out.append(f"{m['id']} {m['status']} by {m['killed_by']}")
    return "; ".join(out)


rows_prev = {r["id"]: r for r in prev["rows"]}
overrides = {}


def set_row(rid, status, location, evidence, fix=None, check=None):
    base = rows_prev.get(rid, {})
    row = {"id": rid, "check": check or base.get("check", "2.6"), "location": location, "status": status,
           "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    overrides[rid] = row


CMD = "Round 12 (pin 5db69a9b): "

# --- re-verified this round (subjects changed in the delta, or re-run) ---
set_row("proj-grader-35-checks", "PASS",
        "course/modules/PC/PC3/project.html line 397; grader/test_project.py; ledgers/PC3/scripts/PC3-c-r12/r12_collect.out; r12_collect_list_seed7.txt",
        CMD + "the delta changed the count (485 -> 486; 494 -> 495). r12_collect.out (r12_collect.sh): 486 tests for seeds 0, 1, 7, 49 and 495 for seeds 50, 848197495, 1712259056, 34135437. r12_collect_list_seed7.txt: 9 functions run once per seed x 51 = 459; four parametrised functions with 2, 2, 2 and 4 cases = 10; 17 single functions; 459 + 10 + 17 = 486. Of the 17 singles, 3 use no seed (the fixed-seed path count, the direct legal sweep and the direct call), so seed-only = 10 + 14 = 24 and no-seed = 3. Page arithmetic: 9 x 51 + 24 + 3 = 486 and 9 x 52 + 24 + 3 = 495. Pass.")
set_row("proj-grader-seed-scope-claim", "PASS", "course/modules/PC/PC3/project.html line 397 against grader/test_project.py lines 37-38",
        CMD + "FIXED_SEEDS = tuple(range(50)); SEEDS dedups (0..49, SEED, SEED + 7919) (test_project.py lines 37-38). Line 397's seed clause (51 seeds when your seed is 0-49, 52 otherwise) is unchanged by the delta; its count clause is re-verified in proj-grader-35-checks.")
set_row("proj-lab1-hypothesis-numbers", "PASS", "course/modules/PC/PC3/project.html line 57 (Lab 1 hypothesis, changed by the delta)",
        CMD + "the delta changed the hypothesis wording to 'no inventory passes the inventory limit of 10 units (defined under Conventions)'. The numbers are unchanged: 9 fills, cash flow -9950, inventory 1 unit, settlement 9980, mark 9980, P&L 30 (ledgers/PC3/scripts/PC3-c-r12/twin_project_1.stdout). The limit is defined in the Conventions 'Trades' bullet (project.html line 405: a fill needs |I| <= 10). Pass.")
set_row("proj-exemplar-a-numbers", "PASS", "course/modules/PC/PC3/project.html lines 635-662 (exemplar A) against ledgers/PC3/scripts/PC3-c-r12/twin_project_1.stdout",
        CMD + "purchases at the bid on turns 2, 3, 4, 8, 19 = 9990 + 9980 + 9970 + 9980 + 9990 = 49910; sales at the ask on turns 5, 7, 13, 18 = 9980 + 9990 + 9990 + 10000 = 39960; 39960 - 49910 = -9950; turn 2 bid 9990 fill 9990; turn 5 ask 9980 fill 9980 inventory +2 after; turn 18 ask 10000 fill 10000 inventory +0 after; largest |inventory| 3 (twin line 'largest |inventory| over the run = 3 (limit 10): True'); counterfactual fills 9, P&L 55, change +25 (twin_project_3.stdout). Every number in exemplar A matches.")
set_row("proj-exemplar-b-numbers", "PASS", "course/modules/PC/PC3/project.html lines 664-690 (exemplar B) against ledgers/PC3/scripts/PC3-c-r12/twin_project_1.stdout",
        CMD + "P&L 30 and cash flow -9950 agree with the twin; the turn-5 record is 'maker sells at the ask 9980 cents', so 'Turn 5 sold at the ask of 9980 cents' holds.")
set_row("proj-lab1-replay-prints", "PASS", "course/modules/PC/PC3/project.html lab-PC3-project-1 (lines 55-240) against tests/labs/PC3/lab-PC3-project-1.py; ledgers/PC3/scripts/PC3-c-r12/page_vs_twin.out, expected_vs_output.out, twin_project_1.stdout",
        CMD + "page_vs_twin.out: lab 1 page code 161 lines, identical=True to the twin; expected_vs_output.out: the expected block equals the twin stdout (True). The printed fill lines (9 fills, turns 2, 3, 4, 5, 7, 8, 13, 18, 19), cash flow -9950, inventory 1, mark 9980, P&L 30 and the identity line agree with the page prose at line 239.")
set_row("proj-lab1-run", "PASS", "tools/run_labs.py --unit PC3 --page project; tests/labs/PC3/lab-PC3-project-1.py under python -I -W error",
        CMD + "ledgers/PC3/scripts/PC3-c-r12/run_labs_PC3_project.out: 'run_labs PC3: PASS (3/3)', exit 0; twin_project_1.exit 0; twin_project_1.stderr 0 bytes.")
set_row("proj-lab2-completion", "PASS", "course/modules/PC/PC3/project.html lab-PC3-project-2 (lines 242-380) against tests/labs/PC3/lab-PC3-project-2.py",
        CMD + "page_vs_twin.out: lab 2 page code 129 lines, blank-lines=3 (the three ___ lines), non-blank mismatches=0; expected_vs_output.out equal; twin_project_2.exit 0, stderr 0 bytes.")
set_row("proj-lab3-counterfactual", "PASS", "course/modules/PC/PC3/project.html lines 457-612 (Lab 3) against tests/labs/PC3/lab-PC3-project-3.py; ledgers/PC3/scripts/PC3-c-r12/twin_project_3.stdout",
        CMD + "page_vs_twin.out: lab 3 page code 140 lines identical to the twin; the twin prints 'counterfactual half-spread 15 cents: fills = 9 of 20', 'counterfactual pnl_cents = 55', 'change in pnl_cents from the wider half-spread = 25 cents'; expected_vs_output.out equal.")
set_row("proj-rubric-c4-real-form-undefined", "PASS", "course/modules/PC/PC3/project.html line 626 (C4 level 4) against course/modules/PC/PC3/L04.html line 482 (L04.html changed in the delta at lines 178 and 573; line 482 re-read)",
        CMD + "grep of L04.html line 482: 'the queue of resting orders' is set aside ('this game does not model that queue') and 'a trader who learns from the fills ... this lesson does not model learning'. The C4 level 4 clause 'both set aside in Lesson 4' holds.")
set_row("proj-grader-v44-limit-lock-survives", "PASS", "ledgers/PC3/mutants/v44_quote_crosses_at_the_limit.py; grader/test_project.py test_a_direct_quote_is_legal_at_every_inventory_within_the_limit (new in the delta, lines 461-478)",
        CMD + "mutate_r12_0-49_all.out: " + kill(["v44"]) + ". The round 11 survivor is killed by the new direct-call sweep. (The sweep itself has a defect: see proj-direct-legal-sweep-turn20-no-history.)")
set_row("proj-direct-call-test-docstring", "PASS", "course/modules/PC/PC3/grader/test_project.py lines 429-435 (docstring) against line 452 (engine.play(sol.quote, 0))",
        CMD + "the docstring now reads 'A direct call on a hand-built state; the engine plays one other game in between.' and the body calls engine.play(sol.quote, 0) at line 452. Consistent.")
set_row("proj-plan-play-policy-signature", "PASS", "plans/PC3-build-plan.md line 415 against line 357 and grader/engine.py line 49",
        CMD + "plans/PC3-build-plan.md line 415 now reads 'play(quote, seed) returns exactly 20 turn records', matching line 357 and engine.py line 49 'def play(quote: QuoteFn, seed: int)'. Closed.")
set_row("proj-builder-mutants", "PASS", "ledgers/PC3/mutants/m01..m10 (mutate_r12_0-49_all.out)",
        CMD + kill([f"m0{i}" for i in range(1, 10)] + ["m10"]))
set_row("proj-verifier-mutants", "PASS", "ledgers/PC3/mutants/v01..v16 and v18..v26 (v17 absent)",
        CMD + kill([f"v{i:02d}" for i in list(range(1, 17)) + list(range(18, 27))]))
set_row("proj-verifier-mutants-r3-new", "PASS", "ledgers/PC3/mutants/v13..v16", CMD + kill([f"v{i:02d}" for i in range(13, 17)]))
set_row("proj-r4-new-mutants-v18-v20", "PASS", "ledgers/PC3/mutants/v18..v20", CMD + kill([f"v{i:02d}" for i in range(18, 21)]))
set_row("proj-verifier-mutants-r7-new", "PASS", "ledgers/PC3/mutants/v27..v30", CMD + kill([f"v{i:02d}" for i in range(27, 31)]))
set_row("proj-verifier-mutants-r8-new", "PASS", "ledgers/PC3/mutants/v31..v34", CMD + kill([f"v{i:02d}" for i in range(31, 35)]))
set_row("proj-verifier-mutants-r9-new", "PASS", "ledgers/PC3/mutants/v35..v38", CMD + kill([f"v{i:02d}" for i in range(35, 39)]))
set_row("proj-verifier-mutants-r10-new", "PASS", "ledgers/PC3/mutants/v39..v42", CMD + kill([f"v{i:02d}" for i in range(39, 43)]))
set_row("proj-verifier-mutants-r11-new", "PASS", "ledgers/PC3/mutants/v43..v46", CMD + kill([f"v{i:02d}" for i in range(43, 47)]))
set_row("proj-grader-v21-replay-scales-by-size", "PASS", "ledgers/PC3/mutants/v21", CMD + kill(["v21"]))
set_row("proj-grader-v22-zero-fill-price-refused", "PASS", "ledgers/PC3/mutants/v22", CMD + kill(["v22"]))
set_row("proj-r5-mutant-v23-first-fill-price", "PASS", "ledgers/PC3/mutants/v23", CMD + kill(["v23"]))
set_row("proj-grader-v24-stderr-print-survives", "PASS", "ledgers/PC3/mutants/v24", CMD + kill(["v24"]))
set_row("proj-grader-v25-last-filled-totals-survives", "PASS", "ledgers/PC3/mutants/v25", CMD + kill(["v25"]))
set_row("proj-grader-v26-logging-warning-survives", "PASS", "ledgers/PC3/mutants/v26", CMD + kill(["v26"]))
set_row("proj-grader-state-between-turns", "PASS", "course/modules/PC/PC3/grader/test_project.py lines 428-453 (test_a_direct_call_on_a_hand_built_state_ignores_an_earlier_game; docstring changed in the delta)",
        CMD + "the body is unchanged; the docstring was rewritten. v39..v42 are killed by it on seed 0 (" + kill(["v39", "v40", "v41", "v42"]) + ").")
set_row("proj-grader-instances", "PASS", "course/modules/PC/PC3/grader/instance.py; test_project.py instance tests", CMD + "instance.py byte-identical to 11d7077a; the instance tests are unchanged (test_instance_is_deterministic_and_well_formed); the instance checks ran in the 486-test collection on every seed (r12_collect.out).")
set_row("proj-quote-rule-first-fill-survivor", "PASS", "course/modules/PC/PC3/project.html line 429 (quote row); ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py",
        CMD + "r12_alts_0-49.out: alt6_quote_mid_from_first_fill.py fails on 0 of 50 seeds (see proj-alternatives-r12-b-e and the alternative rows).")
set_row("proj-twin-rules", "PASS", "tests/labs/PC3/lab-PC3-project-1..3.py run with python -I -W error from a scratch directory",
        CMD + "twin_project_1..3.exit are 0 and twin_project_1..3.stderr are 0 bytes.")
set_row("proj-exception-types-labs", "PASS", "tests/labs/PC3/lab-PC3-project-1..3.py", CMD + "the three twins exit 0 under python -I -W error with empty stderr (twin_project_*.exit, .stderr).")
set_row("proj-run-labs-unit", "PASS", "tools/run_labs.py --unit PC3 --page project (run_labs_PC3_project.out)", CMD + "'run_labs PC3: PASS (3/3)', exit 0.")
set_row("proj-check-tools", "PASS", "tools/check_pages.py --unit PC3; tools/check_dag.py --unit PC3; tools/check_projects.py --unit PC3 (gates_check.out)",
        CMD + "'check_pages PC3: PASS', 'check_dag PC3: PASS', 'check_projects PC3: PASS', each exit 0 (gates_check.out).")
set_row("proj-r8-check-tools", "PASS", "tools/check_pages.py, check_dag.py, check_projects.py for PC3 (gates_check.out)", CMD + "as proj-check-tools: all three PASS, exit 0.")
set_row("proj-page-smoke", "PASS", "tools/page_smoke.py --unit PC3 --pages project.html (page_smoke_project.out)",
        CMD + "'page_smoke PC3: PASS', exit 0; the in-browser grader line reports the suite on the learner seed (see page_smoke_project.out).")
set_row("proj-r8-run-labs-page-smoke", "PASS", "tools/run_labs.py --unit PC3 --page project; tools/run_graders.py --unit PC3 --seeds 0-49; tools/page_smoke.py (project)",
        CMD + "run_labs 3/3; run_graders_PC3.out 'run_graders PC3: PASS (reference 50/50 seeds, slowest 0.3 s)'; page_smoke PASS.")
set_row("proj-grader-reference", "PASS", "course/modules/PC/PC3/grader/reference.py via tools/run_graders.py --unit PC3 --seeds 0-49 (run_graders_PC3.out)",
        CMD + "reference 50/50 seeds PASS, exit 0.")
set_row("proj-grader-starter-fails", "PASS", "course/modules/PC/PC3/grader/starter.py in a scratch copy with test_project.py (starter_fails.out)",
        CMD + "the starter fails 420 tests and passes 66 (486 collected); the new direct test fails on the starter, as the other tests do. Pass.")
set_row("proj-grader-mypy-strict", "PASS", "scratch copy: engine.py, instance.py, test_project.py, market_maker.py (= reference.py) (mypy_strict_scratch.out)",
        CMD + "'Success: no issues found in 4 source files', exit 0 (mypy --strict on the changed test file).")
set_row("proj-mypy-labs", "PASS", "mypy --no-incremental (repo config) (mypy_repo.out)", CMD + "'Success: no issues found in 385 source files', exit 0.")
set_row("proj-lint-ruff", "PASS", "ruff check and ruff format --check on course/modules/PC/PC3/grader, tests/labs/PC3 and tests (ruff_check.out, ruff_format.out)",
        CMD + "'All checks passed!' exit 0; '14 files already formatted' exit 0.")
set_row("proj-r8-pytest-pc3", "PASS", "pytest -k PC3 (pytest_k_PC3_summary.txt)", CMD + "'9 passed, 712 deselected', exit 0.")
set_row("proj-r8-verify-refs", "PASS", "tools/verify_refs.py --offline (verify_refs_offline.out)", CMD + "'offline integrity: 560 entries, 0 problems', exit 0.")
set_row("proj-references", "PASS", "course/modules/PC/PC3/project.html lines 713-715 (reading data-cite) and references/references.json",
        CMD + "verify_refs_offline.out 560 entries, 0 problems; keys zhou2008practical and crack2015heard are data-cite keys of the registry.")
set_row("proj-r8-collect-counts", "PASS", "course/modules/PC/PC3/grader/test_project.py; ledgers/PC3/scripts/PC3-c-r12/r12_collect.out",
        CMD + "486 for seeds 0, 1, 7, 49 and 495 for seeds 50, 848197495, 1712259056, 34135437 (r12_collect.out). Pass.")
set_row("proj-banned-and-process-words", "PASS", "course/modules/PC/PC3/project.html; grader/*.py; tests/labs/PC3/lab-PC3-project-*.py (check_pages.py PC3 PASS, gates_check.out)",
        CMD + "check_pages (banned strings in visible prose, BUILDER_RULES 1.3-1.4) PASS for PC3 after the delta; the new prose ('Three further checks', 'defined under Conventions') contains no banned or process phrase.")
set_row("proj-rubric-atlas-studios", "PASS", "course/modules/PC/PC3/project.html (whole page); plans/PC3-build-plan.md; gates_check.out",
        CMD + "check_pages, check_dag and check_projects pass for PC3; the delta changed no atlas or studio statement.")
set_row("proj-r12-survivor-reachability", "PASS", "ledgers/PC3/scripts/PC3-c-r12/r12_probe_reach.py (uses the checkout's engine and the reference)",
        CMD + "r12_probe_reach.out: across seeds 0-49 under the reference quote, inventory after each turn takes values -8..8 only (max |inventory| 8), so inventory -10 is never reached; fill prices lie in 9920..10080, so 0 is never reached; settlement equals 10000 on 8 seeds. The three new survivors depend on these facts.")

# --- exemplar calibration: blind requirement not met this round ---
set_row("proj-exemplar-a-calibration", "UNVERIFIABLE",
        "course/modules/PC/PC3/project.html lines 635-662 (passage text) against rubric lines 623-627",
        CMD + "my scores from the passage text and the descriptors are C1 4, C2 4, C3 4, C4 3, C5 4 (4,4,4,3,4). They equal the official data-scores, but this verifier was not blind: the header line 635 (which carries data-scores=\"4,4,4,3,4\") was printed before scoring. The scores are not valid blind evidence.",
        fix="A fresh verifier scores exemplar A from the passage text only, with data-scores and the annotation list hidden, and records the result against the official scoring.")
set_row("proj-exemplar-b-calibration", "UNVERIFIABLE",
        "course/modules/PC/PC3/project.html lines 664-692 (passage text) against rubric lines 623-627",
        CMD + "my scores from the passage text are C1 2, C2 2, C3 1, C4 2, C5 1 (2,2,1,2,1), equal to the official data-scores. Not blind: this verifier printed exemplar B's annotation list (lines 680-690) before scoring it.",
        fix="A fresh verifier scores exemplar B from the passage text only, with the annotation list hidden, and records the result.")
set_row("proj-exemplar-scores-blind-disclosure", "FAIL",
        "course/modules/PC/PC3/project.html lines 635, 653, 655, 664, 680-690 (data-scores and annotations) read by this verifier before blind scoring",
        CMD + "disclosure: this round's first read of exemplar A printed its header with data-scores (line 635), a grep printed annotation lines 653 and 655 (exemplar A) and lines 682-686 (exemplar B), and the passage of exemplar B was printed together with its annotation aside before scoring. The blind requirement (VERIFIER_RULES 2.6 rubric 2) was therefore not met for either exemplar in round 12. The calibration rows proj-exemplar-a-calibration and proj-exemplar-b-calibration are UNVERIFIABLE for that reason.",
        fix="Re-score both exemplars with a fresh verifier who has not seen data-scores or annotations; if the scores differ from the official ones by more than one level, change the annotations or the descriptors.")

# --- FAIL rows found this round ---
set_row("proj-direct-legal-sweep-turn20-no-history", "FAIL",
        "course/modules/PC/PC3/grader/test_project.py test_a_direct_quote_is_legal_at_every_inventory_within_the_limit (lines 461-478; the state uses \"history\": [] at turn 20); course/modules/PC/PC3/project.html line 395 (history = the earlier turn records) and line 397 (the third check, 'with no history')",
        CMD + "the new test feeds turn 20 an empty history. Project line 395 defines history as 'the earlier turn records of the log', so turn 20 has 19 earlier records; the state the test builds is outside that definition. A correct rule that uses the definition (quote reads state['history'][k] for k < turn - 1; file ledgers/PC3/scripts/PC3-c-r12/alts/alt_r12_a_turn_indexed_history.py) passes 485 tests on seed 0 and fails the new test with IndexError (ledgers/PC3/scripts/PC3-c-r12/r12_alt_a_failure.txt; the same on seeds 1, 7 and 49, and on all 50 seeds in r12_alts_0-49.out). The rule is over-constrained by an input the page's own definition excludes.",
        fix="Give turn 20 a history of 19 records (for example turn_record(t, size=1, filled=False) for t in 1..19, as test_no_function_prints_or_warns already builds) and keep the empty history for turn 1 only; change line 397 and the docstring to say so; then re-run alt_r12_a (must pass) and v44 (must still be killed).",
        check="2.6-grader (over-constraint: a correct implementation under the page's state definition must pass)")
set_row("proj-no-print-rare-branch-survivors", "FAIL",
        "course/modules/PC/PC3/grader/test_project.py test_no_function_prints_or_warns (lines 391-407) and the direct sweep; ledgers/PC3/mutants/v47_quote_prints_at_inventory_minus_ten.py, v48_replay_prints_at_ending_inventory_minus_ten.py, v49_replay_prints_on_a_fill_at_price_zero.py; project.html line 395 ('Neither quote nor replay prints or warns') and line 397 (checked 'on the game and on a log with no fill')",
        CMD + "mutate_r12_0-49_all.out: " + kill(["v47", "v48", "v49"]) + ". Each is a student-error print on a branch that no game of seeds 0-49 reaches (r12_probe_reach.out: inventory in -8..8, fill prices 9920..10080). The no-print test calls quote and replay only on games and the no-fill log, and checks stdout and stderr there; the direct sweep (inventory -10..10) and the hand-built replay logs check no output. Line 395 states the rule unqualified, so these survivors violate a stated behaviour: 55 of 58 killed, 3 survived.",
        fix="In test_no_function_prints_or_warns, also call quote on the direct sweep states (turns 1 and 20, inventory -10..10) and replay on the hand-built logs (a fill at price 0, and a log whose ending inventory is -10 built from its turns), under capsys, caplog and the warnings filter; then re-run mutate_graders --unit PC3 --seeds 0-49 and expect 58 of 58 killed.",
        check="2.6-mutation (surviving grader mutants that violate a stated rule)")
set_row("proj-alt-turn-indexed-history-overconstrained", "FAIL",
        "ledgers/PC3/scripts/PC3-c-r12/alts/alt_r12_a_turn_indexed_history.py run against grader/test_project.py (the same finding as proj-direct-legal-sweep-turn20-no-history, recorded as the alternative's row)",
        CMD + "alt_r12_a fails 1 test on every seed 0-49 (r12_alts_0-49.out: 'fails on 50 of 50 seeds'); the failing test is test_a_direct_quote_is_legal_at_every_inventory_within_the_limit (IndexError). The other 485 tests pass on seeds 0, 1, 7 and 49.",
        fix="See proj-direct-legal-sweep-turn20-no-history: fix the test's state, then alt_r12_a must show 'fails on 0 of 50 seeds'.")
set_row("proj-alternatives-r12-b-e", "PASS", "ledgers/PC3/scripts/PC3-c-r12/alts/alt_r12_b_scan_fills_with_guard.py, alt_r12_c_size_by_inventory_limit_check.py, alt_r12_d_class_quoter_fixed_spread.py, alt_r12_e_quote_from_turn_and_fill_count.py (each with a replay)",
        CMD + "r12_alts_0-49.out: each of b, c, d, e 'fails on 0 of 50 seeds' (replay copied from the reference, with the same ValueError messages). Each is a different correct quoting rule (a list comprehension, a size-0-at-limit rule, a class with the spread as an attribute, and a turn-1 start that never reads an empty history).")
set_row("proj-rubric-ladder-exclusive-highest-level", "FAIL",
        "course/modules/PC/PC3/project.html rubric caption (line 620) and cells C1-C5 (lines 623-627); C3 level 3 cell ('States one change with its amount') against C1 level 1 cell ('states a change without its amount in cents')",
        CMD + "the descriptors are cumulative, not exclusive: C1 level 2 ('two or more ... each equal') contains C1 level 3's three-value case; C2 level 2 contains levels 3 and 4; C4 level 2 contains 3 and 4. The page does not say which cell wins (the verifier's 'highest met' reading of round 11 is not on the page). C3 is also overlapping: a change whose amount is not in cents, with both runs, meets level 3 ('with its amount') and level 1 ('without its amount in cents'). The exclusive-and-exhaustive check of the brief therefore fails on the page text.",
        fix="Add one sentence under the rubric caption: 'A submission takes the highest level whose descriptor it meets.' and write C3 level 3 as 'States one change with its amount in cents ...', so that an amount in other units meets only level 1.")
set_row("proj-plan-line-319-lab3-play", "FAIL",
        "plans/PC3-build-plan.md line 319 ('it runs the reference play(seed=0)') against project.html line 517 (the lab's own def play(seed: int, half_spread: int)) and grader/engine.py line 49 (play(quote, seed))",
        CMD + "the plan names a play(seed=0) call for lab 3 that the lab does not make. The lab defines its own play(seed, half_spread) (project.html line 517) and calls it with the reference rule and half-spread 10, then 15. The plan's engine signature (line 357) is play(quote, seed).",
        fix="In plans/PC3-build-plan.md line 319 replace 'runs the reference play(seed=0)' with 'runs the reference game on seed 0 through its own play(seed, half_spread), at half-spread 10 and then 15'.")


# --- alternative rows: the test file changed, so every alternative row is re-run this round ---
ALT_ROWS = ["proj-alternatives-1-2-4-5", "proj-alt3-replay", "proj-alternative-6", "proj-alternative-7-8-verifier",
            "proj-alternative-9-10-verifier-r3", "proj-alternatives-r4-new", "proj-alternatives-r7-new",
            "proj-r8-alternatives-new", "proj-r5-alternatives-14-16", "proj-alternatives-r10-new",
            "proj-alternatives-r11-new"]
for rid in ALT_ROWS:
    set_row(rid, "PASS", rows_prev[rid]["location"],
            CMD + "re-run on seeds 0-49 against the round 12 test_project.py (r12_alts_0-49.out, 43 files): the files this row names fail on 0 of 50 seeds. The only failing file in the run is alt_r12_a (proj-alt-turn-indexed-history-overconstrained).")
set_row("proj-hub-seed-scope", "PASS", "course/modules/PC/PC3/index.html lines 55 and 160 against project.html line 397 (seeds clause)",
        CMD + "the seeds clause of project.html line 397 (0 to 49, your seed and your seed plus 7919; 51 or 52 seeds) is unchanged by the delta; the count clause is re-verified in proj-grader-35-checks. index.html is byte-identical (not in the delta).")
set_row("proj-starter-docstring-raise-scope", "PASS", "course/modules/PC/PC3/grader/starter.py lines 8-9; project.html lines 411-418",
        CMD + "starter.py and project.html 411-418 unchanged; starter run: ledgers/PC3/scripts/PC3-c-r12/starter_fails.out '420 failed, 66 passed' (the empty implementation fails the suite).")
set_row("proj-notation", "PASS", "notation/notation.json; course/modules/PC/PC3/project.html math spans (changed spans: line 57 only)",
        CMD + "the only math span changed by the delta is line 57 (\\(-9950\\), \\(30\\), \\(\\times\\)); it introduces no symbol outside notation/notation.json (the r11 registered list T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q is not touched). The line 397 change adds no math.")

# --- carried rows: keep id, keep round-11 PASS evidence with the carry prefix ---
def carry_scope(row):
    loc = row["location"]
    if "test_project" in loc:
        return "grader/test_project.py cited functions, whose bodies are unchanged by the delta (it changed only the docstrings at 118-119 and 429-435, and inserted the test at 461-478)"
    if "project.html" in loc:
        return "project.html cited lines, which the delta did not change (it changed only lines 57 and 397)"
    if "plans/" in loc:
        return "plan cited lines, which the delta did not change (it changed only line 415)"
    if "L04.html" in loc or "L06.html" in loc:
        return "cited lines of the lesson, which the delta did not change"
    return "cited files, which the delta did not change"


final_rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in overrides:
        final_rows.append(overrides.pop(rid))
        continue
    if r["status"] == "PASS":
        new = dict(r)
        new["evidence"] = f"Carried from round 11 ({carry_scope(r)}, byte-identical since the previous pin 11d7077a): " + r["evidence"]
        final_rows.append(new)
    else:
        raise SystemExit(f"row {rid} was FAIL in round 11 and has no round-12 override")

# new rows (not in round 11)
for rid, row in overrides.items():
    if rid not in {x["id"] for x in final_rows}:
        final_rows.append(row)

assert all(r["status"] in ("PASS", "FAIL", "UNVERIFIABLE") for r in final_rows)
ids = [r["id"] for r in final_rows]
assert len(ids) == len(set(ids)), "duplicate ids"

fragment = {
    "unit": "PC3",
    "slice": "c",
    "round": 12,
    "verifier": "independent verifier (Haiku 5.5), round 12, slice c (did not build PC3)",
    "pin": "5db69a9b",
    "base": "round 11 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round11.json (pin 11d7077a). Delta 11d7077a..5db69a9b for slice c: course/modules/PC/PC3/project.html (lines 57 and 397 only), grader/test_project.py (docstrings at 118-119 and 429-435; new test at 461-478), mutants v43-v46 unchanged and new v47-v49 (this round), plans/PC3-build-plan.md (line 415 only), L04.html (lines 178, 573; 482 re-read), tests/labs/PC3/lab-PC3-L04-1.py and L06-1.py (not slice c's labs). Byte-identical: engine.py, instance.py, reference.py, starter.py, labs project-1..3, index.html, grader.js.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-PC3-c",
    "scratch": "ledgers/PC3/scripts/PC3-c-r12/ (every script and output used by a row); /tmp/pc3c-r12-* scratch copies only for mutation and strict-mypy runs",
    "verified_at": "2026-11-05T14:50:57+00:00",
    "verdict": "FAIL",
    "rows": final_rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "",
    "summary": "",
}
fragment["summary"] = (
    f"PC3-c round 12: verdict FAIL. Rows {len(final_rows)}: "
    f"PASS {sum(r['status']=='PASS' for r in final_rows)}, FAIL {sum(r['status']=='FAIL' for r in final_rows)}, "
    f"UNVERIFIABLE {sum(r['status']=='UNVERIFIABLE' for r in final_rows)}. Mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed."
)

fragment["notes"] = (
    "Round 12 pin 5db69a9b (delta from 11d7077a: project.html lines 57 and 397; grader/test_project.py docstrings and the new "
    "direct legal sweep; mutants v43-v46 kept and v47-v49 added by this verifier; plan line 415; L04.html and L06.html "
    "outside the slice's labs). Gates run by this verifier, outputs in ledgers/PC3/scripts/PC3-c-r12/: check_pages, check_dag, "
    "check_projects (gates_check.out, PASS); run_labs PC3 project 3/3 (run_labs_PC3_project.out); run_graders PC3 0-49 reference "
    "50/50 (run_graders_PC3.out); page_smoke PC3 project (page_smoke_project.out, PASS); mutate_graders PC3 0-49 on 58 mutants: "
    "55 killed, 3 survived (mutate_r12_0-49_all.out); alternatives on 0-49, 43 files (r12_alts_0-49.out): 42 fail on 0 of 50, "
    "alt_r12_a fails on 50 of 50 (r12_alt_a_failure.txt); collect-only 486 / 495 (r12_collect.out); ruff check and format PASS "
    "(ruff_check.out, ruff_format.out); mypy --no-incremental 385 files PASS (mypy_repo.out); mypy --strict on the four grader "
    "modules PASS (mypy_strict_scratch.out); starter 420 failed / 66 passed (starter_fails.out); pytest -k PC3 9 passed; "
    "verify_refs --offline 560 entries, 0 problems (verify_refs_offline.out); twins alone under python -I -W error exit 0, empty "
    "stderr (twin_project_1..3.*); page_vs_twin.out and expected_vs_output.out. Reachability: r12_probe_reach.out. "
    "Blind scoring: NOT achieved this round (see proj-exemplar-scores-blind-disclosure); both calibration rows are UNVERIFIABLE. "
    "Not checked: the in-browser self-assessment form (JavaScript, not in slice c's gates); cards.json (slices a and b); L04 and "
    "L06 labs (other slices); plan sections outside the delta (carried by r11 with the byte-identical note); the Pyodide "
    "in-browser run of the new test was not run separately (page_smoke ran the project page as a whole)."
)

json.dump(fragment, open(f"{ROOT}/ledgers/PC3/PC3-c.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(fragment["summary"])
