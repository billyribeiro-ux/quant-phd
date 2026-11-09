"""Build the round-16 fragment ledgers/PC3/PC3-c.json for PC3 slice c (project.html, grader, project labs, mutants).

Carry rule (verifier-rules: a PASS row is carried only when its cited subject is byte-identical): rows whose subject this
round changed (project.html line 397; the test definitions listed in out/func_delta_r16.txt; the mutant and alternative
sets; every gate) are re-verified and carry fresh evidence. Other PASS rows are carried with the prefix.
"""
import datetime
import json
import sys

PREV = "/Users/billyribeiro/.fanout/frags/E-PC3-c.round15.json"
OUT = "/Users/billyribeiro/.fanout/wt/verifyE16-PC3-c/ledgers/PC3/PC3-c.json"
S = "ledgers/PC3/scripts/PC3-c-r16/out/"
prev = json.load(open(PREV, encoding="utf-8"))
CARRY_PREFIX = ("Carried from round 15 (cited subject byte-identical since pin d1e65a0: project.html changed only at line 397 "
                "and the test definitions FILL_PRICES_CENTS, fill_record, _state, direct_states, "
                "test_no_function_prints_or_warns, test_a_direct_quote_is_legal_at_every_inventory_within_the_limit changed "
                "(out/func_delta_r16.txt); the cited lines or definitions of this row did not). Round-15 evidence: ")

# Rows re-verified this round: id -> (status, evidence, fix)
FRESH = {
 "proj-grader-35-checks": ("PASS", "Fresh: local pytest (scripts/PC3-c-r16/local_suite_r16.sh, out/local_suite_r16.txt) collects 487 tests for QF_SEED=0 and QF_SEED=7 and 496 for QF_SEED=100, all pass for the reference. Counted from test_project.py: 9 per-seed tests x 51 seeds + 25 seed-only + 3 seedless = 487; 9 x 52 + 28 = 496. project.html line 397 reads 487/496, 51/52 and 25/3 accordingly.", ""),
 "proj-grader-seed-scope-claim": ("PASS", "Fresh: SEEDS = dict.fromkeys(0..49, SEED, SEED+7919) in test_project.py line 38 gives 51 distinct seeds for QF_SEED in 0..49 and 52 otherwise (collect counts above). project.html line 397 says '51 seeds when your seed is one of 0 to 49, and 52 otherwise'.", ""),
 "proj-hub-seed-scope": ("PASS", "Fresh for project.html line 397 (seed counts as above). index.html lines 55 and 160 are byte-identical since pin d1e65a0 (not in this slice; carried from round 15).", ""),
 "proj-r15-grading-counts": ("PASS", "Fresh: collect counts 487 (seed 0, 7) and 496 (seed 100) from local_suite_r16.txt; the 9-per-seed, 25 and 3 split matches the test definitions (func_delta_r16.txt).", ""),
 "proj-r15-direct-states-log-wording": ("PASS", "Fresh: project.html line 397 now reads 'with hand-built unfilled records for the earlier turns' (grep of line 397), matching the test docstring at test_project.py lines 556-559 and direct_states (lines 133-138). The round-15 wording defect is fixed.", ""),
 "proj-grader-no-print": ("PASS", "Fresh: test_no_function_prints_or_warns (test_project.py lines 461-502) now also runs ends_at_plus_ten and the direct states with fills. Mutant run (out/mutate_pc3_76_0_49_r16.out): all 76 mutants killed on seeds 0-49, and the no-print test kills the print and warning mutants r15_01, r15_02, v47, v48, v49 and s14_01.", ""),
 "proj-banned-and-process-words": ("PASS", "Fresh: grep -n -i over project.html and grader/*.py for TODO, TBD, lorem, clearly, obviously, studies show, well known, important to note, ellipsis, and build/builder/round/verifier/requests (run this round): no hit; 'round' occurs only inside 'around' (project.html line 466, reference.py lines 5 and 21). check_pages.py --unit PC3 PASS (out/check_pages_unit.out).", ""),
 "proj-rubric-atlas-studios": ("PASS", "Fresh: grep -c -i 'atlas|studio' project.html = 0. The page names no Atlas milestone or studio, and the curriculum entry has no atlas key (plans/PC3-build-plan.md section 8).", ""),
 "proj-exemplar-a-numbers": ("PASS", "Fresh: scripts/PC3-c-r16/numbers_r16.py (out/numbers_r16.txt) recomputes cash flow -9950, inventory 1, mark 9980, P&L 30, nine fills at turns 2,3,4,5,7,8,13,18,19, purchases 49910, sales 39960, counterfactual 55 (+25), largest |inventory| 3, turn-5 inventory 2, turn-18 inventory 0. Every exemplar A number matches.", ""),
 "proj-exemplar-b-numbers": ("PASS", "Fresh: the exemplar B numbers (P&L 30, cash flow -9950, turn 5 sold at the ask 9980) match numbers_r16.txt.", ""),
 "proj-exemplar-b-arrival-sensitivity": ("PASS", "Fresh: exemplar B names the arrival probabilities 1/4, 1/4, 1/2 (project.html line 676) and its annotation (line 687, C4 level 2) says they are named without the result they move. The rubric C4 level-2 descriptor ('names one or more of the model's parameters... with or without the result') allows this.", ""),
 "proj-exemplar-a-c5-annotation": ("PASS", "Fresh: exemplar A self-review (line 649) gives 30 = -9950 + 1 x 9980 with the identity check printed by Lab 1 (out/twin_vs_page_r16.txt: expected block equals twin stdout). Annotation line 658 (C5 level 4) matches the rubric C5 level-4 cell.", ""),
 "proj-exemplar-levels-check-count": ("PASS", "Fresh: data-level 4 and 2 on exemplar-a and exemplar-b (project.html lines 635, 664); each has five data-scores entries; the rubric has five criteria.", ""),
 "proj-exemplar-levels-vs-plan": ("PASS", "Fresh: the two exemplars are at levels 4 and 2 (lines 635, 664); plans/PC3-build-plan.md section 5.4 requires exemplars at two levels, and the plan's two levels are met.", ""),
 "proj-lab1-replay-prints": ("PASS", "Fresh: project.html lab-PC3-project-1 page code equals tests/labs/PC3/lab-PC3-project-1.py (out/twin_vs_page_r16.txt: twin==page True); the twin exits 0 under python -I -W error and its stdout equals the expected block.", ""),
 "proj-lab1-run": ("PASS", "Fresh: tools/run_labs.py --unit PC3 --page project: PASS (3/3) (out/run_labs_project.out); twin run under python -I -W error (out/twin_vs_page_r16.txt).", ""),
 "proj-lab1-hypothesis-numbers": ("PASS", "Fresh: Lab 1 hypothesis (project.html line 57 area) states 9 fills, -9950, inventory 1, settlement 9980, mark 9980, P&L 30, limit 10: all equal the printed output and numbers_r16.txt.", ""),
 "proj-lab2-completion": ("PASS", "Fresh: page code of lab-PC3-project-2 differs from the twin only at the two blank lines (cash_flow = ___, mark = ___); the twin exits 0 and its stdout equals the expected block (out/twin_vs_page_r16.txt).", ""),
 "proj-lab2-interpretation-last-quote": ("PASS", "Fresh: Lab 2 interpretation says a mark at any price other than 9980 changes the P&L with an inventory of 1 unit. P&L = cash flow + 1 x mark, so the change equals the mark difference; the statement is an identity, checked by the line 'identity holds: True'.", ""),
 "proj-lab3-counterfactual": ("PASS", "Fresh: Lab 3 page code equals its twin (twin==page True); output 9 fills, P&L 30 -> 55, change 25 cents, matching numbers_r16.txt (out/numbers_r16.txt: counterfactual half 15 fills 9 pnl 55 change 25).", ""),
 "proj-lab3-interpretation": ("PASS", "Fresh: Lab 3 interpretation reads the printed block (first block the reference, last three lines the counterfactual) and states one seed only; both match the output.", ""),
 "proj-twin-rules": ("PASS", "Fresh: twins tests/labs/PC3/lab-PC3-project-1..3.py run under python -I -W error with exit 0 and no stderr (out/twin_vs_page_r16.txt); ruff check and format --check PASS on tests/labs/PC3 (out/ruff_check.out, ruff_format.out).", ""),
 "proj-exception-types-labs": ("PASS", "Fresh: the three project twins raise no exception and use no refusal path (out/twin_vs_page_r16.txt, exit 0 for all three).", ""),
 "proj-r5-labs-page-vs-twin": ("PASS", "Fresh: out/twin_vs_page_r16.txt shows page code equals twin for labs 1 and 3, and for lab 2 only at the two blanks.", ""),
 "proj-r14-lab-draw-equals-instance": ("PASS", "Fresh: draw_game(0) in each twin matches grader/instance.py make_instance(0) (the path and arrivals agree: numbers_r16.txt, sample_instances_r16.txt).", ""),
 "proj-r15-labs-twins-isolated": ("PASS", "Fresh: out/twin_vs_page_r16.txt (python -I -W error, exit 0 for lab-PC3-project-1..3).", ""),
 "proj-run-labs-unit": ("PASS", "Fresh: tools/run_labs.py --unit PC3 --page project: run_labs PC3: PASS (3/3) (out/run_labs_project.out).", ""),
 "proj-r8-run-labs-page-smoke": ("PASS", "Fresh: run_labs PASS (3/3); tools/run_graders.py --unit PC3 --seeds 0-49: PASS (reference 50/50) (out/run_graders_0_49.out); page_smoke --pages project PASS with 'All 496 tests pass' in Pyodide (out/page_smoke_project.out).", ""),
 "proj-page-smoke": ("PASS", "Fresh: tools/page_smoke.py --unit PC3 --pages project: PASS (out/page_smoke_project.out), Pyodide grader 496 tests pass on a non-fixed seed.", ""),
 "proj-r15-gates": ("PASS", "Fresh: check_pages PASS, check_dag PASS, check_projects PASS (out/check_*_unit.out); page_smoke project PASS; run_labs PASS; run_graders PASS.", ""),
 "proj-check-tools": ("PASS", "Fresh: check_pages --unit PC3 PASS, check_dag --unit PC3 PASS, check_projects --unit PC3 PASS (out/check_pages_unit.out, check_dag_unit.out, check_projects_unit.out).", ""),
 "proj-r8-check-tools": ("PASS", "Fresh: same three commands as proj-check-tools, all exit 0.", ""),
 "proj-r8-collect-counts": ("PASS", "Fresh: pytest collect counts 487 / 496 (out/local_suite_r16.txt).", ""),
 "proj-r8-pytest-pc3": ("PASS", "Fresh: pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py exit 0 (out/pytest_r16.out); the grader suite runs 487/496 passes locally (out/local_suite_r16.txt).", ""),
 "proj-r8-verify-refs": ("PASS", "Fresh: tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline_r16.out).", ""),
 "proj-references": ("PASS", "Fresh: verify_refs offline PASS (560 entries, 0 problems); both reading keys zhou2008practical and crack2015heard appear in references/references.json (grep). project.html reading list is data-cite only.", ""),
 "proj-r14-reading-keys": ("PASS", "Fresh: same as proj-references; data-cite keys match the registry entries.", ""),
 "proj-lint-ruff": ("PASS", "Fresh: ruff check tests/labs/PC3 course/modules/PC/PC3/grader: exit 0; ruff format --check: exit 0 (out/ruff_check.out, ruff_format.out).", ""),
 "proj-mypy-labs": ("PASS", "Fresh: .venv/bin/mypy --no-incremental (repo config, files tools and tests): 'Success: no issues found in 385 source files', exit 0 (out/mypy_repo_r16.out).", ""),
 "proj-grader-mypy-strict": ("PASS", "Fresh: mypy --strict on engine.py, instance.py, test_project.py and market_maker.py (= reference.py) in a scratch copy: 'Success: no issues found in 4 source files' (out/mypy_grader_strict_r16.out shows the import-only errors when market_maker is absent, which is not a defect).", ""),
 "proj-r15-mypy-strict-grader": ("PASS", "Fresh: same scratch strict-mypy run as proj-grader-mypy-strict: no issues.", ""),
 "proj-r14-lint-mypy-pytest": ("PASS", "Fresh: ruff check and format PASS, repo mypy PASS, pytest subset PASS (out/ruff_*.out, mypy_repo_r16.out, pytest_r16.out).", ""),
 "proj-grader-reference": ("PASS", "Fresh: tools/run_graders.py --unit PC3 --seeds 0-49: PASS (reference 50/50 seeds) (out/run_graders_0_49.out); local pytest of reference.py gives 487 passed for seeds 0 and 7 and 496 for seed 100 (out/local_suite_r16.txt).", ""),
 "proj-grader-starter-fails": ("PASS", "Fresh: local suite with starter.py as market_maker.py, QF_SEED=0: '421 failed, 66 passed' (out/local_suite_r16.txt), so the suite fails on the starter.", ""),
 "proj-r15-starter-fails": ("PASS", "Fresh: same run as proj-grader-starter-fails.", ""),
 "proj-grader-instances": ("PASS", "Fresh: 40 sampled instances (seeds 0-19, 100-119) all valid (21 values from 10000, steps of +-5, 20 named arrivals, positive); 36 distinct (path, arrivals) tuples; the reference P&L takes 11 distinct values across the 40 seeds (out/sample_instances_r16.txt).", ""),
 "proj-r10-instances-20-seeds": ("PASS", "Fresh: out/sample_instances_r16.txt (40 seeds, valid, differing paths and P&L).", ""),
 "proj-verifier-mutants": ("PASS", "Fresh: tools/mutate_graders.py --unit PC3 --seeds 0-49 with the 76 mutants: 76/76 KILLED (out/mutate_pc3_76_0_49_r16.out).", ""),
 "proj-builder-mutants": ("PASS", "Fresh: m01..m10 among the 76 KILLED (out/mutate_pc3_76_0_49_r16.out).", ""),
 "proj-mutant-m08-description": ("PASS", "Fresh: ledgers/PC3/mutants/m08_hard_coded_answer_for_any_log.py first docstring line names the student error; killed (out/mutate_pc3_76_0_49_r16.out).", ""),
 "proj-verifier-mutants-r3-new": ("PASS", "Fresh: v13..v16 KILLED in the 76-mutant run.", ""),
 "proj-verifier-mutants-r7-new": ("PASS", "Fresh: v27..v30 KILLED in the 76-mutant run.", ""),
 "proj-verifier-mutants-r8-new": ("PASS", "Fresh: v31..v34 KILLED in the 76-mutant run.", ""),
 "proj-verifier-mutants-r9-new": ("PASS", "Fresh: v35..v38 KILLED in the 76-mutant run.", ""),
 "proj-verifier-mutants-r10-new": ("PASS", "Fresh: v39..v42 KILLED in the 76-mutant run.", ""),
 "proj-verifier-mutants-r11-new": ("PASS", "Fresh: v43..v46 KILLED in the 76-mutant run.", ""),
 "proj-r4-new-mutants-v18-v20": ("PASS", "Fresh: v18..v20 KILLED in the 76-mutant run.", ""),
 "proj-grader-v21-replay-scales-by-size": ("PASS", "Fresh: v21 KILLED in the 76-mutant run.", ""),
 "proj-grader-v22-zero-fill-price-refused": ("PASS", "Fresh: v22 KILLED in the 76-mutant run.", ""),
 "proj-r5-mutant-v23-first-fill-price": ("PASS", "Fresh: v23 KILLED in the 76-mutant run.", ""),
 "proj-grader-v24-stderr-print-survives": ("PASS", "Fresh: v24 KILLED in the 76-mutant run.", ""),
 "proj-grader-v25-last-filled-totals-survives": ("PASS", "Fresh: v25 KILLED in the 76-mutant run.", ""),
 "proj-grader-v26-logging-warning-survives": ("PASS", "Fresh: v26 KILLED in the 76-mutant run.", ""),
 "proj-grader-v44-limit-lock-survives": ("PASS", "Fresh: v44 KILLED in the 76-mutant run.", ""),
 "proj-r13-mutants-r13_01-05": ("PASS", "Fresh: r13_01..r13_05 KILLED in the 76-mutant run.", ""),
 "proj-r14-grader-rounding-survivor": ("PASS", "Fresh: r14_01 KILLED in the 76-mutant run.", ""),
 "proj-r14-grader-locked-market-survivor": ("PASS", "Fresh: r14_03 KILLED in the 76-mutant run.", ""),
 "proj-r14-grader-print-survivor": ("PASS", "Fresh: s14_01 KILLED in the 76-mutant run.", ""),
 "proj-r14-grader-offgrid-survivor": ("PASS", "Fresh: s14_02 KILLED in the 76-mutant run.", ""),
 "proj-r14-mutant-control-s14_03": ("PASS", "Fresh: s14_03 KILLED in the 76-mutant run.", ""),
 "proj-r14-mutants-aggregate": ("PASS", "Fresh: all 76 files in ledgers/PC3/mutants are listed in out/mutate_pc3_76_0_49_r16.out and all are KILLED (76/76).", ""),
 "proj-r15-replay-prints-at-plus-ten": ("PASS", "Fresh: ledgers/PC3/mutants/r15_01_replay_prints_at_ending_inventory_plus_ten.py KILLED by test_no_function_prints_or_warns (out/mutate_pc3_76_0_49_r16.out). The round-15 survivor is fixed by the added ends_at_plus_ten log (test_project.py lines 484-491).", ""),
 "proj-r15-quote-warns-turn-twenty-after-fill": ("PASS", "Fresh: r15_02 KILLED (out/mutate_pc3_76_0_49_r16.out) by the no-print test, whose direct states now include fill histories (direct_states second family, test_project.py lines 144-150).", ""),
 "proj-r15-quote-locked-after-fill-history": ("PASS", "Fresh: r15_03 KILLED (out/mutate_pc3_76_0_49_r16.out) by test_a_direct_quote_is_legal_at_every_inventory_within_the_limit, whose direct states now include fills at 9980..10020 (test_project.py lines 555-566).", ""),
 "proj-r12-survivor-reachability": ("PASS", "Fresh: v47, v48, v49 KILLED in the 76-mutant run (out/mutate_pc3_76_0_49_r16.out) by test_no_function_prints_or_warns.", ""),
 "proj-no-print-rare-branch-survivors": ("PASS", "Fresh: all no-print mutants (v26, v33, v34, v47, v48, v49, s14_01, r15_01, r15_02) are KILLED in the 76-mutant run; test_no_function_prints_or_warns (test_project.py lines 461-502) reaches the branches.", ""),
 "proj-direct-legal-sweep-turn20-no-history": ("PASS", "Fresh: test_a_direct_quote_is_legal_at_every_inventory_within_the_limit now sweeps fill histories (test_project.py lines 555-566), and every prior legal alternative passes it (out/prior_alternatives_r16.txt: 52/52 pass 487).", ""),
 "proj-alt-turn-indexed-history-overconstrained": ("PASS", "Fresh: the r12 turn-indexed-history alternative is among the 52 prior candidates re-run against the changed suite: all 52 pass 487 (out/prior_alternatives_r16.txt).", ""),
 "proj-alternatives-r12-b-e": ("PASS", "Fresh: candidates alt_r12_b..e are among the 52 prior candidates, all pass 487 (out/prior_alternatives_r16.txt).", ""),
 "proj-r15-alternatives-all": ("PASS", "Fresh: 52 of 52 prior candidate modules pass 487 on the current suite (out/prior_alternatives_r16.txt).", ""),
 "proj-alternatives-1-2-4-5": ("PASS", "Fresh: alternatives alt1, alt2, alt4, alt5 are among the 52 prior candidates, all pass 487 (out/prior_alternatives_r16.txt).", ""),
 "proj-alt3-replay": ("PASS", "Fresh: alt3 inventory-skew is among the 52 prior candidates, all pass 487; the round-16 alternative 3 (inventory-skewed, replay from the cash identity) also passes 487 (out/alternatives_r16.txt).", ""),
 "proj-alternative-6": ("PASS", "Fresh: alt6 (quote mid from the first fill) is among the 52 prior candidates, all pass 487 (out/prior_alternatives_r16.txt).", ""),
 "proj-quote-rule-first-fill-survivor": ("PASS", "Fresh: alt6 passes 487 (out/prior_alternatives_r16.txt). A first-fill mid is a different legal policy; the page does not state which fill sets the mid for the learner's rule (project.html rule text only for the reference rule, Rungs 1 and 2), so no mutant is needed.", ""),
 "proj-alternative-7-8-verifier": ("PASS", "Fresh: alt7 and alt8 are among the 52 prior candidates, all pass 487.", ""),
 "proj-alternative-9-10-verifier-r3": ("PASS", "Fresh: alt9 and alt10 are among the 52 prior candidates, all pass 487.", ""),
 "proj-alternatives-r4-new": ("PASS", "Fresh: alt11..alt13 are among the 52 prior candidates, all pass 487.", ""),
 "proj-alternatives-r7-new": ("PASS", "Fresh: alt20..alt24 are among the 52 prior candidates, all pass 487.", ""),
 "proj-r8-alternatives-new": ("PASS", "Fresh: alt_r8_a..e are among the 52 prior candidates, all pass 487.", ""),
 "proj-r5-alternatives-14-16": ("PASS", "Fresh: alt14..alt16 are among the 52 prior candidates, all pass 487.", ""),
 "proj-alternatives-r10-new": ("PASS", "Fresh: alt_r10_a..d are among the 52 prior candidates, all pass 487.", ""),
 "proj-alternatives-r11-new": ("PASS", "Fresh: alt_r11_a..d are among the 52 prior candidates, all pass 487.", ""),
 "proj-r14-alternatives-15": ("PASS", "Fresh: the 52 prior candidates, which include alt1..alt6 and the r13 set, all pass 487 (out/prior_alternatives_r16.txt).", ""),
}

# Previous non-PASS and changed-subject rows that this round settles.
OVERRIDE = {
 "proj-exemplar-scores-in-served-html": ("PASS", "Ruling 15 (plans/FINAL-ARCHITECT-RULINGS.md, item 15, read this round): 'The page keeps its annotations for learners; they are not moved out of the HTML.' The data-scores and annotation asides at project.html lines 635-690 are the designed reveal content; rubric.js line 149 hides them with the hidden attribute until the learner reveals, and project.html line 696 discloses that they are in the source. Not a defect under ruling 15.", ""),
 "proj-exemplar-scores-blind-disclosure": ("UNVERIFIABLE", "The blind condition is not certified for this verifier. This round the verifier printed project.html lines 632-694 by tag skeleton before scoring, and the first grep and the skeleton print both showed data-scores and the annotation data-level values (project.html lines 635, 664, 653-658, 682-688). Ruling 15's extraction (scripts/PC3-c-r16/extract_memo_r16.py, out/memo_prose_r16.txt) was run, but the scores were formed after the attributes had been seen.", "A fresh verifier that has not printed project.html lines 632-694 runs extract_memo_r16.py, scores out/memo_prose_r16.txt against the rubric (lines 620-627), and only then compares with data-scores. Record that the prior view was absent."),
 "proj-exemplar-a-calibration": ("UNVERIFIABLE", "Prose-only scoring (out/memo_prose_r16.txt, the rubric) gives C1 4, C2 4, C3 4, C4 3, C5 4, which equals the official 4,4,4,3,4 and every annotation (lines 653-658). Not certified blind, for the reason given in proj-exemplar-scores-blind-disclosure, so the row cannot be PASS.", "Re-score exemplar A in a fresh blind run as in proj-exemplar-scores-blind-disclosure."),
 "proj-exemplar-b-calibration": ("UNVERIFIABLE", "Prose-only scoring gives C1 2, C2 2, C3 1, C4 2, C5 1, equal to the official 2,2,1,2,1 and to the annotations (lines 682-688; the annotation for C2 level 2 'cites one turn' matches the rubric C2 level-2 cell). Not certified blind, so UNVERIFIABLE.", "Re-score exemplar B in a fresh blind run as in proj-exemplar-scores-blind-disclosure."),
}

NEW = [
 ("proj-r16-mutant-control-true-division", "2.6-mutation (control: new student-error mutant)", "ledgers/PC3/mutants/r16_01_quote_half_spread_from_previous_quote_true_division.py; course/modules/PC/PC3/grader/test_project.py test_quotes_are_legal_on_every_turn", "PASS", "New mutant written this round: quote reads the half-spread from the previous record with true division (float 10.0). Run: scripts/PC3-c-r16/run_mutants_r16.sh (out/new_mutants_r16.txt): 102 failed, KILLED by test_quotes_are_legal_on_every_turn on seeds 0-49 (type check)."),
 ("proj-r16-mutant-stop-loss-locked", "2.6-mutation (new student-error mutant)", "ledgers/PC3/mutants/r16_02_quote_stop_loss_posts_a_locked_market.py; test_project.py test_quotes_are_legal_on_every_turn", "PASS", "New mutant: a stop-loss at cash <= -40000 posts a locked market (bid equal to ask). Killed: 32 failures in out/new_mutants_r16.txt (ValueError from the engine on seeds 29, 33, 37, 7919 and others). The games reach cash <= -40000."),
 ("proj-r16-mutant-reversed-quote-marked-loss", "2.6-mutation (new student-error mutant, reachability)", "ledgers/PC3/mutants/r16_03_quote_reverses_on_a_marked_loss.py; test_project.py test_a_direct_quote_is_legal_at_every_inventory_within_the_limit", "PASS", "New mutant: quote reverses (bid above ask) when cash plus inventory x last fill <= -30000. Killed only by the direct legality sweep (1 failure), not by any game of seeds 0-49 (out/new_mutants_r16.txt). The direct sweep therefore is the only check of this branch, which is what the changed test adds."),
 ("proj-r16-mutants-76", "2.6-mutants (full set)", "ledgers/PC3/mutants/ (76 files); out/mutate_pc3_76_0_49_r16.out", "PASS", "tools/mutate_graders.py --unit PC3 --seeds 0-49 after this round's test change: 'mutate_graders PC3: PASS (76/76 killed)', exit 0."),
 ("proj-r16-alternatives-five-new", "2.6-alternatives (five correct implementations, new)", "ledgers/PC3/scripts/PC3-c-r16/alternatives/alt_r16_1..5*.py", "PASS", "Five new correct implementations of different styles run against the current suite (QF_SEED=0 covers seeds 0-49): class-based policy with an Accounts class (alt 1), closure factory with a reduce fold (alt 2), inventory-skewed quotes with a replay from the cash identity (alt 3), size 5 - |inventory|//2 with a list accumulator (alt 4), size 2 outside 9950..10050 with a dataclass record per fill (alt 5). Each: 487 passed (out/alternatives_r16.txt)."),
 ("proj-r16-alternatives-prior-52", "2.6-alternatives (prior candidates against the changed suite)", "ledgers/PC3/scripts/PC3-c-r15/alt_candidates.txt (58 entries: 52 modules and 6 runner scripts)", "PASS", "The test definitions changed this round, so every prior candidate module was re-run: 52 of 52 pass 487 (out/prior_alternatives_r16.txt). The 6 runner scripts are not alternatives and were excluded."),
 ("proj-r16-reference-collect-and-starter", "2.6-grader (suite on reference and starter)", "course/modules/PC/PC3/grader/test_project.py; grader/reference.py; grader/starter.py", "PASS", "Local suite (out/local_suite_r16.txt): reference 487 passed (seeds 0 and 7), 496 passed (seed 100); starter 421 failed, 66 passed."),
 ("proj-r16-numbers-independent", "2.2-numbers", "course/modules/PC/PC3/project.html lines 57, 393-407, 455-612, 635-690; scripts/PC3-c-r16/numbers_r16.py", "PASS", "numbers_r16.py recomputes from grader/engine.py and reference.py: settlement 9980, 9 fills at turns 2,3,4,5,7,8,13,18,19, cash flow -9950, inventory 1, mark 9980, P&L 30, counterfactual 55 (+25 on seed 0 at half-spread 15), largest |inventory| 3, arrivals 2/5/13 (uninformed-buy/uninformed-sell/informed) for seed 0 (out/numbers_r16.txt). Every prose number on the page matches."),
 ("proj-r16-exemplar-annotation-vs-rubric", "2.6-rubric (annotation descriptor matches the rubric text)", "course/modules/PC/PC3/project.html lines 620-627 (rubric), 651-660 and 680-690 (annotations)", "PASS", "Read the rubric text and the annotations this round. Exemplar B's C2 level-2 annotation ('cites one turn by number and field') matches the rubric C2 level-2 cell ('cites one or more turns ... with at least one value'); its level-3 miss matches the level-3 cell (two turns). Exemplar A's C4 level-3 annotation matches the C4 level-3 cell (three of four items)."),
 ("proj-r16-rung-length-tier", "2.6-spec (ladder: rungs 1-2 length)", "course/modules/PC/PC3/project.html ladder section ('Rungs 1 and 2 are at full length'); BUILDER_RULES 5.1; BLUEPRINT line 222", "PASS", "BUILDER_RULES 5.1 and BLUEPRINT line 222 make rungs 1-2 minimal from the master's tier (M) upward. PC3 is tier U (curriculum/06-profession-capstone.yaml line 159), so full length is the rule. FC2 and E5 plans record the same reading (plans/FC2-build-plan.md line 149; plans/E5-build-plan.md line 311). No defect."),
 ("proj-r16-links-anchors", "2.4-structure (links and anchors)", "course/modules/PC/PC3/project.html (31 href values); scripts/PC3-c-r16/anchors_r16.py", "PASS", "anchors_r16.py: 31 links checked, no missing file, no missing anchor (out/anchors_r16.txt)."),
 ("proj-r16-notation-and-terms", "2.4-notation / 2.14-DAG", "course/modules/PC/PC3/project.html math spans; notation/notation.json", "PASS", "Macros on the page: \\times, \\le, \\ge, \\lt, \\gt, \\dots, \\mathrm (standard KaTeX, no registered symbol). No T, Phi, gamma, R*, Q (blackboard) or pi appears. Concept terms (adverse selection, Bayes, martingale, Kelly, CAPM, duration, Poisson, MDP) appear nowhere on the page (grep, out/ transcript)."),
 ("proj-r16-hours-estimate", "2.9-hours (own estimate)", "course/modules/PC/PC3/project.html lines 421-438", "PASS", "Own estimate: rung 1 read 1 h, rung 2 1 h, quote 1.5-3 h, replay 1-2 h, grader runs and debugging 2-3 h, analysis 3-5 h, self-assessment 1 h: 10-16 h against 14 h, inside 30 %."),
 ("proj-r16-instance-sample", "2.8-data (instances)", "course/modules/PC/PC3/grader/instance.py; scripts/PC3-c-r16/sample_instances_r16.py", "PASS", "40 seeds (0-19, 100-119): all valid; 36 distinct paths/arrivals; reference P&L takes 11 distinct values (out/sample_instances_r16.txt)."),
 ("proj-r16-grader-mypy-note", "2.6-lint (grader typing)", "course/modules/PC/PC3/grader/*.py", "PASS", "mypy --strict on the grader with market_maker.py present: no issues (scratch). Without market_maker.py the grader does not type-check, which is expected because the module is supplied by the learner or by reference.py."),
]

import re as _re
MUTANTS = []
for _line in open('/Users/billyribeiro/.fanout/wt/verifyE16-PC3-c/ledgers/PC3/scripts/PC3-c-r16/out/mutate_pc3_76_0_49_r16.out', encoding='utf-8'):
    _m = _re.match(r'^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$', _line.rstrip())
    if _m:
        MUTANTS.append({'name': _m.group(2), 'description': _m.group(3), 'killed_by': _m.group(4) if _m.group(1) == 'KILLED' else None})
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in OVERRIDE:
        status, ev, fix = OVERRIDE[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev, "fix": fix})
        continue
    if rid in FRESH and FRESH[rid][1]:
        status, ev, fix = FRESH[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev, "fix": fix})
        continue
    if r["status"] == "PASS":
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY_PREFIX + r["evidence"], "fix": ""})
    else:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "FAIL",
                     "evidence": "Round-15 FAIL row re-checked this round (see the fresh evidence in the rows listed in notes).",
                     "fix": r.get("fix", "")})
# Rows that were FAIL last round and are now fresh-PASS via FRESH (ids not in OVERRIDE).
for rid, (status, ev, fix) in FRESH.items():
    if rid not in {x["id"] for x in rows} and ev:
        base = next(r for r in prev["rows"] if r["id"] == rid) if any(r["id"] == rid for r in prev["rows"]) else None
        rows.append({"id": rid, "check": base["check"] if base else "2.6", "location": base["location"] if base else "", "status": status, "evidence": ev, "fix": fix})
for rid, check, loc, status, ev in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev, "fix": ""})

# Fix the one 'FAIL' row that is re-verified PASS this round by name.
for r in rows:
    if r["id"] in ("proj-r15-replay-prints-at-plus-ten", "proj-r15-quote-warns-turn-twenty-after-fill",
                   "proj-r15-quote-locked-after-fill-history", "proj-r15-direct-states-log-wording"):
        r["status"] = "PASS"
        r["fix"] = ""

# Unique ids
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]

nonpass = [r for r in rows if r["status"] != "PASS"]
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if not nonpass else "FAIL"
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
frag = {
 "unit": "PC3",
 "slice": "c",
 "round": 16,
 "verifier": "independent verifier (Haiku 5.5), round 16, slice c; did not build PC3; blind calibration not certified (see rows)",
 "pin": "56cc575a",
 "base": "round 15 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round15.json (pin d1e65a0). Delta d1e65a0..56cc575a for slice c: project.html line 397 (Grading mode); grader/test_project.py: definitions FILL_PRICES_CENTS, fill_record, _state, direct_states, test_no_function_prints_or_warns, test_a_direct_quote_is_legal_at_every_inventory_within_the_limit (out/func_delta_r16.txt); mutants r15_01..03 (already in the round-15 pin). Plan, reference, engine, instance, starter, labs unchanged.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE16-PC3-c (detached at 56cc575a, the pin; .venv symlinked; course/assets/vendor present)",
 "scratch": "ledgers/PC3/scripts/PC3-c-r16/ (gates_r16.sh, out/, local_suite_r16.sh, run_mutants_r16.sh, twin_vs_page_r16.py, extract_memo_r16.py, numbers_r16.py, sample_instances_r16.py, anchors_r16.py, func_delta_r16.py, build_fragment_r16.py, alternatives/alt_r16_1..5); scratch in /tmp/pc3c_r16_* (removed)",
 "verified_at": now,
 "verdict": verdict,
 "rows": rows,
 "mutants": MUTANTS,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
   "Blindness: this verifier printed the data-scores and the annotation data-level values (project.html lines 635-690) with a tag skeleton before scoring, so the blind calibration is UNVERIFIABLE. Prose-only scores (out/memo_prose_r16.txt, rubric) are A 4,4,4,3,4 and B 2,2,1,2,1, equal to the official scores.",
   "Ruling 15 is in plans/FINAL-ARCHITECT-RULINGS.md (not in verifier-rules.md). Under ruling 15 the page keeps its annotations in the HTML, so the round-15 served-html FAIL is not a defect.",
   "Carried rows keep their round-15 evidence; their test-function line numbers shifted by about +28 after test_project.py line 134 in this round (cited definitions are byte-identical, out/func_delta_r16.txt).",
   "Full read this round: project.html (732 lines, including the exemplar text and annotations after the blind scoring), grader/engine.py, instance.py, reference.py, starter.py and test_project.py (645 lines), and the three project twins (via twin_vs_page_r16.py).",
   "Gate outputs (exit codes) are in out/ALL_EXIT_r16.txt; the repo-level mypy and the pytest subset were run after it (out/mypy_repo_r16.out, out/pytest_r16.out).",
   "Mutants: 76 listed (73 prior, 3 new r16_01..03); mutate_graders reports 76/76 KILLED on seeds 0-49 (out/mutate_pc3_76_0_49_r16.out)."
 ],
 "summary": ""
}
frag["summary"] = (f"PC3-c round 16: verdict {verdict}. Rows {len(rows)}: PASS {counts['PASS']}, FAIL {counts['FAIL']}, UNVERIFIABLE {counts['UNVERIFIABLE']}. "
                   f"Mutants 76/76 killed on seeds 0-49 (3 new: r16_01 control, r16_02, r16_03). Alternatives: 5 new and 52 prior candidates, all 487 pass on the current suite.")
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(verdict, counts, len(rows))
for r in nonpass:
    print(r["id"], r["status"])
