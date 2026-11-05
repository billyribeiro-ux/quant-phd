"""Round 11 verifier: builds ledgers/PC3/PC3-c.json from the round 10 fragment (context only) and the round 11 evidence."""

import json
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE11-PC3-c"
DELTA = "git diff 00a84795..11d7077a"
S = "ledgers/PC3/scripts/PC3-c-r11/"
PREV = json.load(open("/Users/billyribeiro/.fanout/frags/E-PC3-c.round10.json", encoding="utf-8"))
PREV_ROWS = {r["id"]: r for r in PREV["rows"]}

MUT = {}
for line in open(ROOT + "/" + S + "mutate_r11_new_v43-v46_0-49.out", encoding="utf-8"):
    m = re.match(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line.rstrip())
    if m:
        MUT[m.group(2)] = {"status": m.group(1), "desc": m.group(3), "killer": m.group(4)}
assert len(MUT) == 55, len(MUT)


def mut_ids(prefix_list):
    out = []
    for p in prefix_list:
        hits = [k for k in MUT if k.startswith(p + "_")]
        assert len(hits) == 1, (p, hits)
        out.append(hits[0])
    return out


def mut_ev(names):
    parts = []
    for n in names:
        v = MUT[n]
        parts.append(f"{n[:3]} {v['status']} by {v['killer']}")
    return ("tools/mutate_graders.py --unit PC3 --seeds 0-49 (ledgers/PC3/scripts/PC3-c-r11/mutate_r11_new_v43-v46_0-49.out, 54 of 55 killed): "
            + "; ".join(parts) + ".")


ALT_EV = ("tools/run_graders-style scratch run of every alternative (r11_run_alts.py, seeds 0-49, r11_alts_0-49.out): "
          "all 38 files, including alt1-alt6, the PC3-c-r1..r10 alternatives and alt_r11_a..d, print 'fails on 0 of 50 seeds'.")

CARRY_GROUP = {
    "project": "project.html: the cited lines are byte-identical; the delta's project.html hunks touch only lines 53, 397, 625 and 627",
    "grader": "grader/test_project.py: the cited tests are byte-identical; the delta inserts lines only at 428-453, so later tests moved down",
    "index": "index.html: not in the delta",
    "starter": "grader/starter.py: not in the delta",
    "mutants": "the mutant file: byte-identical, not in the delta",
    "instance": "grader/instance.py and engine.py: not in the delta",
    "dag": "project.html line 37: not in the delta",
}

CARRY = {
    "proj-zero-fill-replay": "grader",
    "proj-rubric-ladder-gap-c1": "project",
    "proj-rubric-ladder-gap-c1-no-pnl": "project",
    "proj-rubric-ladder-gap-c2": "project",
    "proj-rubric-c2-level3-admits-mismatch": "project",
    "proj-starter-docstring-raise-scope": "starter",
    "proj-hub-filenames": "index",
    "proj-hub-skill-check-premise": "index",
    "proj-hub-placement-conflict": "index",
    "proj-hours-arithmetic": "index",
    "proj-lab1-hypothesis-numbers": "project",
    "proj-lab2-interpretation-last-quote": "project",
    "proj-lab3-interpretation": "project",
    "proj-rung1-instance-claim": "instance",
    "proj-conventions-constants": "project",
    "proj-exemplar-b-arrival-sensitivity": "project",
    "proj-spec-log-schema": "project",
    "proj-mutant-m08-description": "mutants",
    "proj-grader-no-print": "grader",
    "proj-grader-determinism-quote-state": "grader",
    "proj-js-claims": "project",
    "proj-local-commands": "project",
    "proj-known-limitation": "project",
    "proj-ladder-scope": "project",
    "proj-stretch": "project",
    "proj-grader-instances": "grader",
    "proj-grader-messages": "grader",
    "proj-named-refusals": "grader",
    "proj-exception-types": "grader",
    "proj-dag-terms": "dag",
    "proj-grader-replay-from-fills": "grader",
    "proj-instance-engine-names": "instance",
    "proj-r10-instances-20-seeds": "instance",
    "proj-r10-local-command": "project",
}

REV = {}

REV["proj-rubric-observable"] = (
    "course/modules/PC/PC3/project.html line 627 (C5 level cells) with the C1-C5 rubric at lines 623-627",
    "Re-verified round 11: the C5 row (line 627) is now level 4 'names one check ... and gives the number', level 3 'names one check and its result as a word', level 2 'names one check, without its result', level 1 'names no self-review, ... or names a check and gives a number ... that replay does not produce'. Every C5 submission fits one of these by the highest-level rule (no check; a check without result; a word result; a number replay produces; a number replay does not produce).",
)
REV["proj-rubric-ladder-gap-c3"] = (
    "course/modules/PC/PC3/project.html line 625 (C3, all four cells)",
    "Re-verified round 11 (full C3 ladder, line 625): L4 one change with its amount in cents, same-seed rerun, change in pnl_cents reported in cents; L3 one change with its amount, same-seed rerun, both runs given, without the change reported in cents; L2 one change with its amount in cents and either no rerun, a rerun on another seed, or the same seed with at most one run and no difference; L1 no counterfactual, or a change without its amount in cents. Classes checked: both runs with unitless difference (L3), one run (L2), another seed (L2), no rerun (L2), a change with an amount not in cents and both runs (L3 by 'with its amount', also matching L1; the highest met is L3), no amount in cents (L1). Each class has one level.",
)
REV["proj-rubric-ladder-gap-c3-one-run"] = (
    "course/modules/PC/PC3/project.html line 625 (C3 levels 2-4)",
    "Re-verified round 11: a same-seed rerun giving one run's P&L and no change is L2 ('at most one run without the difference'); a one-run submission that also reports the change in cents is L4 by its text. Each case has one level.",
)
REV["proj-rubric-ladder-gap-c3-other-seed"] = (
    "course/modules/PC/PC3/project.html line 625 (C3 levels 1-2)",
    "Re-verified round 11: 'reruns another seed' is in L2 ('either gives no rerun, reruns another seed, or ...'), so a counterfactual with an amount in cents on another seed is L2.",
)
REV["proj-rubric-ladder-gap-c3-difference-no-unit"] = (
    "course/modules/PC/PC3/project.html line 625 (C3 level 3 cell: 'without the change reported in cents')",
    "Fixed in round 11 (FAIL in round 10): the C3 level 3 cell now reads 'gives the P&L of both runs, without the change reported in cents', so a same-seed rerun with both runs and a unitless difference such as '25' fits L3. Round 10 failed because the cell said 'without their difference'.",
)
REV["proj-rubric-ladder-gap-c5-wrong-number"] = (
    "course/modules/PC/PC3/project.html line 627 (C5 level 1 cell)",
    "Fixed in round 11 (FAIL in round 10): the C5 level 1 cell now includes 'names a check and gives a number for it that replay does not produce', so a check with a wrong number fits L1 and each C5 submission fits one level.",
)
REV["proj-rubric-c4-real-form-undefined"] = (
    "course/modules/PC/PC3/project.html line 626 (C4 level 4) against course/modules/PC/PC3/L04.html line 482",
    "Re-verified round 11: L04.html line 482 still sets aside 'the queue of resting orders' and 'a trader who learns from the fills, and this lesson does not model learning', so the C4 level 4 clause 'both set aside in Lesson 4' holds. The delta changed L04.html only at lines 181-190 and 528-531.",
)
REV["proj-grader-35-checks"] = (
    "course/modules/PC/PC3/project.html line 397; grader/test_project.py; ledgers/PC3/scripts/PC3-c-r11/r11_collect.out; r11_collect_list_seed7.txt",
    "Re-verified round 11 (count changed by the delta, 484 -> 485 and 493 -> 494): r11_collect.out gives 485 tests for seeds 0, 1, 7, 49 and 494 for seeds 50, 848197495, 1712259056, 34135437. Breakdown from r11_collect_list_seed7.txt: 9 functions run once per seed (9 x 51 = 459), four functions with 2, 2, 2 and 4 cases (10), 16 single functions; 459 + 10 + 16 = 485. Page arithmetic: 9 x 51 + 24 + 2 = 485 and 9 x 52 + 24 + 2 = 494, with 24 + 2 = 26 = 10 + 16. Pass.",
)
REV["proj-grader-seed-scope-claim"] = (
    "course/modules/PC/PC3/project.html line 397 against grader/test_project.py lines 37-38",
    "Re-verified round 11: FIXED_SEEDS = tuple(range(50)); SEEDS = dedup(FIXED_SEEDS, SEED, SEED + 7919) (test_project.py lines 37-38). Line 397 gives 51 seeds when the learner's seed is in 0-49 and 52 otherwise, which the set gives.",
)
REV["proj-hub-seed-scope"] = (
    "course/modules/PC/PC3/index.html lines 55 and 160 against project.html line 397 and grader/test_project.py lines 37-38",
    "Re-verified round 11: index.html line 55 (seeds 0 to 49 and your own workspace seed) and line 160 (seeds 0 to 49, your own seed and that seed plus 7919) match the set in project.html line 397 and test_project.py SEEDS. The hub states no test count (grep for 484, 485, 493, 494 in the PC3 pages finds only project.html line 397).",
)
REV["proj-plan-file-names"] = (
    "plans/PC3-build-plan.md lines 67-70, 317, 337, 340, 348 against project.html lines 46, 393, 429-430, 443 and index.html lines 160, 167 and grader/starter.py line 1",
    "Fixed in round 11 (FAIL in round 10): the delta changed plan lines 67-70, 317, 337, 340 and 348 from policy.py and pnl.py to market_maker.py. Re-verified: no file-name hit for policy.py or pnl.py remains in the plan; project.html, index.html, starter.py and test_project.py name market_maker.py. The remaining plan wording 'policy' is prose (lines 4, 372, 454, 599); the one stale call form on line 415 is listed as proj-plan-play-policy-signature.",
)
REV["proj-plan-grader-seed-scope"] = (
    "plans/PC3-build-plan.md lines 348 and 380",
    "Re-verified round 11: line 348 reads 'dual mode: market_maker.py on seeds 0-49'; line 380 gives exemplar levels 4 and 2. Consistent with the page and FIXED_SEEDS.",
)
REV["proj-exemplar-levels-vs-plan"] = (
    "course/modules/PC/PC3/project.html lines 635 and 664; plans/PC3-build-plan.md line 380",
    "Re-verified round 11: plan line 380 names exemplar-a data-level 4 and exemplar-b data-level 2; project.html line 635 has data-level=4 and line 664 has data-level=2.",
)
REV["proj-exemplar-levels-check-count"] = (
    "course/modules/PC/PC3/project.html lines 635 and 664 (data-scores)",
    "Re-verified round 11: exemplar-a data-scores 4,4,4,3,4 and exemplar-b data-scores 2,2,1,2,1 have five entries, one per criterion; the blind scores of the calibration rows match both.",
)
REV["proj-exemplar-a-numbers"] = (
    "course/modules/PC/PC3/project.html lines 635-662 (exemplar A) against ledgers/PC3/scripts/PC3-c-r11/numbers_r11.out",
    "Re-verified round 11 from a fresh seed-0 run of the reference: cash_flow -9950, inventory_end 1, inventory_mark 9980, pnl 30; nine fills at turns 2,3,4,5,7,8,13,18,19; buys at the bid (turns 2,3,4,8,19) total 49910 and sales at the ask (turns 5,7,13,18) total 39960, so 39960 - 49910 = -9950; turn 2 bid 9990 fill 9990; turn 5 ask 9980 fill 9980 inventory 2 after; turn 18 ask 10000 fill 10000 inventory 0 after; largest |inventory| 3; widened half-spread 15 gives P&L 55, change +25, fills 9. Every number in exemplar A matches.",
)
REV["proj-exemplar-b-numbers"] = (
    "course/modules/PC/PC3/project.html lines 664-690 (exemplar B) against numbers_r11.out",
    "Re-verified round 11: the replay gives P&L 30 and cash flow -9950; the turn-5 record is arrival informed, ask 9980, fill 9980, so 'turn 5 sold at the ask of 9980 cents' holds.",
)
REV["proj-exemplar-a-calibration"] = (
    "course/modules/PC/PC3/project.html lines 635-662 (passage text) against rubric lines 623-627",
    "Blind-scoring round 11 against the current descriptors, from the passage text: C1 4 (three values equal to replay output, cash-flow and inventory turns named); C2 4 (turns 2, 5, 18, each with a value that matches the log: 9990, 9980, 10000); C3 4 (one change, 10 to 15 cents, same seed, P&L 30 to 55, +25 cents); C4 3 (arrival probabilities and inventory limit with the result each moves; settlement rule not named; three of four items); C5 4 (identity with its computed number). Result 4,4,4,3,4 equals the official scoring (data-scores). Disclosure: an early grep printed lines 637 and 651-688 (official scoring and annotations) before this blind scoring; the scores above rest on the passage text and descriptors.",
)
REV["proj-exemplar-b-calibration"] = (
    "course/modules/PC/PC3/project.html lines 664-692 (passage text) against rubric lines 623-627",
    "Blind-scoring round 11 (same disclosure as proj-exemplar-a-calibration): C1 2 (cash flow and P&L stated, mark absent, no turn named); C2 2 (one turn, turn 5, value 9980 matches); C3 1 (a wider spread, no amount in cents); C4 2 (arrival probabilities named, no result each moves); C5 1 (checked, no check named). Result 2,2,1,2,1 equals the official scoring.",
)
REV["proj-exemplar-a-c5-annotation"] = (
    "course/modules/PC/PC3/project.html line 658 (annotation C5 level 4) against line 649 (self-review passage)",
    "Re-verified round 11: line 649 names the identity and gives 30 = -9950 + 1 x 9980, which numbers_r11.out confirms; the annotation's 'Meets C5 level 4' matches the level 4 cell.",
)
REV["proj-lab1-replay-prints"] = (
    "course/modules/PC/PC3/project.html lab-PC3-project-1 (lines 55-240) against tests/labs/PC3/lab-PC3-project-1.py; ledgers/PC3/scripts/PC3-c-r11/page_vs_twin.out, expected_vs_output.out, twin_project_1.stdout",
    "Re-verified round 11: page code identical to the twin (161 lines, page_vs_twin.out); the expected block equals the twin stdout (expected_vs_output.out); the printed fills, cash flow -9950, inventory 1, mark 9980, P&L 30 and the identity lines agree with numbers_r11.out.",
)
REV["proj-lab1-run"] = (
    "tools/run_labs.py --unit PC3 --page project; tests/labs/PC3/lab-PC3-project-1.py under python -I -W error",
    "Re-verified round 11: run_labs PC3: PASS (3/3) (run_labs_PC3_project.out); twin_project_1.exit 0, stderr empty.",
)
REV["proj-lab2-completion"] = (
    "course/modules/PC/PC3/project.html lab-PC3-project-2 (lines 242-380) against tests/labs/PC3/lab-PC3-project-2.py",
    "Re-verified round 11: the page's completion code has 129 lines equal to the twin's 129 lines except three lines containing ___ (page_vs_twin.out: blank-lines=3, non-blank mismatches=0); the expected block equals the twin's stdout; twin_project_2.exit 0.",
)
REV["proj-lab3-counterfactual"] = (
    "course/modules/PC/PC3/project.html lines 457-612 (Lab 3) against tests/labs/PC3/lab-PC3-project-3.py; twin_project_3.stdout",
    "Re-verified round 11: the twin prints 'counterfactual half-spread 15 cents: fills = 9 of 20', 'counterfactual pnl_cents = 55', 'change in pnl_cents from the wider half-spread = 25 cents'; my own run gives 55 and +25 (numbers_r11.out); page code identical to the twin (page_vs_twin.out).",
)
REV["proj-r5-labs-page-vs-twin"] = (
    "project labs 1-3: page code vs tests/labs/PC3/lab-PC3-project-1..3.py (page_vs_twin.out, expected_vs_output.out)",
    "Re-verified round 11: labs 1 and 3 page code identical to the twins (161 and 140 lines); lab 2 identical except three ___ blank lines; expected blocks equal the twins' stdout for all three labs.",
)
REV["proj-twin-rules"] = (
    "tests/labs/PC3/lab-PC3-project-1..3.py run with python -I -W error from a scratch directory",
    "Re-verified round 11: twin_project_1..3.exit are 0 and the .stderr files are empty.",
)
REV["proj-exception-types-labs"] = (
    "tests/labs/PC3/lab-PC3-project-1..3.py",
    "Re-verified round 11: the three twins run under python -I -W error with exit 0 and raise nothing; no lab names an exception type on the page beyond the replay's own checks.",
)
REV["proj-run-labs-unit"] = (
    "tools/run_labs.py --unit PC3 --page project (run_labs_PC3_project.out)",
    "Re-verified round 11: run_labs PC3: PASS (3/3), exit 0.",
)
REV["proj-check-tools"] = (
    "check_pages.py --all; check_dag.py --all; check_projects.py --all (gates_check.out)",
    "Re-verified round 11: all three exit 0; 'check_pages PC3: PASS', 'check_dag PC3: PASS', 'check_projects PC3: PASS'.",
)
REV["proj-r8-check-tools"] = (
    "tools/check_pages.py --all; tools/check_dag.py --all; tools/check_projects.py --all (gates_check.out)",
    "Re-verified round 11: as proj-check-tools; all PC3 lines PASS, exit 0.",
)
REV["proj-page-smoke"] = (
    "tools/page_smoke.py --unit PC3 --pages project (page_smoke_project.out)",
    "Re-verified round 11: exit 0; labs 1-3 run; 'in-browser grader: All 494 tests pass on seed 34135437'; 'page_smoke PC3: PASS'.",
)
REV["proj-r8-run-labs-page-smoke"] = (
    "tools/run_labs.py --unit PC3 --page project; tools/run_graders.py --unit PC3 --seeds 0-49; tools/page_smoke.py --unit PC3 --pages project",
    "Re-verified round 11: run_labs PC3 3/3; run_graders_PC3.out 'run_graders PC3: PASS (reference 50/50 seeds, slowest 0.3 s)'; page_smoke PC3 PASS.",
)
REV["proj-r8-collect-counts"] = (
    "course/modules/PC/PC3/grader/test_project.py; ledgers/PC3/scripts/PC3-c-r11/r11_collect.out",
    "Re-verified round 11 (round 10's 484/493 are superseded by the delta): seeds 0, 1, 7, 49 give 485; seeds 50, 848197495, 1712259056, 34135437 give 494 (r11_collect.out).",
)
REV["proj-r8-pytest-pc3"] = (
    "pytest -q -k PC3 (pytest_k_PC3.out)",
    "Re-verified round 11: nine tests pass (pytest_k_PC3.out), exit 0.",
)
REV["proj-r8-verify-refs"] = (
    "tools/verify_refs.py --offline (verify_refs_offline.out)",
    "Re-verified round 11: 'offline integrity: 560 entries, 0 problems', exit 0.",
)
REV["proj-references"] = (
    "course/modules/PC/PC3/project.html lines 713-715 (reading list data-cite) and references/references.json",
    "Re-verified round 11: data-cite keys zhou2008practical and crack2015heard are present in references/references.json; verify_refs offline 560 entries, 0 problems. The delta changed only used_by lists (BK4, LX1), not these entries.",
)
REV["proj-banned-and-process-words"] = (
    "course/modules/PC/PC3/project.html; course/modules/PC/PC3/grader/*.py; tests/labs/PC3/lab-PC3-project-1..3.py",
    "Re-verified round 11: no hit for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'important to note', obviously, clearly, 'well known', 'studies show', 'experts agree', 'about 6%', 'roughly half', historically, 'can be shown', an ellipsis, or the process words builder, verifier, fixer, architect, audit, round N, pass N.",
)
REV["proj-notation"] = (
    "notation/notation.json (macros, symbols); course/modules/PC/PC3/project.html math spans",
    "Re-verified round 11: the registered symbols are T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q; no \\(...\\) span on the PC3 project page uses any of them. Local symbols (N, t, v_t, a_t, b_t, q_t, I, pnl) are defined on the page (Conventions); the registry says locally conventional letters are defined per unit. Macros used (dots, ge, gt, le, lt, mathrm, times) are standard TeX commands; none is a registry macro, and the page does not use one. Math is unchanged by the delta.",
)
REV["proj-rubric-atlas-studios"] = (
    "course/modules/PC/PC3/project.html (whole page); plans/PC3-build-plan.md; gates_check.out",
    "Re-verified round 11: check_pages, check_dag and check_projects pass for PC3; no atlas or studio statement changed in the delta.",
)
REV["proj-grader-starter-fails"] = (
    "course/modules/PC/PC3/grader/starter.py in a scratch copy with test_project.py (starter_fails.out)",
    "Re-verified round 11: the starter's NotImplementedError stubs make 419 tests fail and 66 pass (starter_fails.out).",
)
REV["proj-grader-reference"] = (
    "course/modules/PC/PC3/grader/reference.py via tools/run_graders.py --unit PC3 --seeds 0-49 (run_graders_PC3.out)",
    "Re-verified round 11: reference 50/50 seeds PASS.",
)
REV["proj-grader-mypy-strict"] = (
    "scratch copy: engine.py, instance.py, test_project.py, market_maker.py (= reference.py), lab-PC3-project-1..3.py under mypy --strict (mypy_strict_scratch.out)",
    "Re-verified round 11: 'Success: no issues found in 7 source files', exit 0.",
)
REV["proj-mypy-labs"] = (
    "mypy --no-incremental (repo config) (mypy_repo.out)",
    "Re-verified round 11: 'Success: no issues found in 385 source files', exit 0.",
)
REV["proj-lint-ruff"] = (
    "ruff check and ruff format --check on course/modules/PC/PC3/grader and tests/labs/PC3; ruff check . (ruff_check.out, ruff_format.out, ruff_repo.out)",
    "Re-verified round 11: 'All checks passed!' (exit 0); '14 files already formatted' (exit 0); repo-wide ruff check exit 0.",
)
REV["proj-grader-window-distinct-paths"] = (
    "course/modules/PC/PC3/grader/test_project.py lines 482-485 (moved from 450-454; content byte-identical)",
    "Re-verified round 11: test_fixed_seeds_0_to_49_give_fifty_different_paths (line 482) builds 50 fair paths from make_instance on seeds 0..49 and expects 50 distinct paths; it uses no learner seed; the 50/50 reference run and the alternatives pass it.",
)
REV["proj-quote-rule-first-fill-survivor"] = (
    "course/modules/PC/PC3/project.html line 429 (quote row); ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py",
    "Re-verified round 11: alt6 (mid from the first fill) is among the alternatives that pass on 0 of 50 seeds (r11_alts_0-49.out); project.html line 429 still describes the quoting rule as free.",
)
REV["proj-grader-state-between-turns"] = (
    "course/modules/PC/PC3/grader/test_project.py lines 428-453 (test_a_direct_call_on_a_hand_built_state_ignores_an_earlier_game) against project.html line 395 ('keeps nothing between turns or games outside that state')",
    "Fixed in round 11 (FAIL in round 10): the new direct-call test reloads the module, quotes a hand-built turn-5 state, plays one other game with engine.play(sol.quote, 0), and quotes the same state again. v39 (keeps the mid in a module global) now fails it (mutate_r11_new_v43-v46_0-49.out: 'v39 KILLED by test_a_direct_call_on_a_hand_built_state_ignores_an_earlier_game (seed 0)'). Its docstring wording is a separate defect, proj-direct-call-test-docstring.",
)
REV["proj-verifier-mutants-r10-new"] = (
    "ledgers/PC3/mutants/v39..v42 (round 10 student-error mutants)",
    "Fixed in round 11 (FAIL in round 10): v39 is now killed by test_a_direct_call_on_a_hand_built_state_ignores_an_earlier_game (seed 0); v40 by test_the_quote_depends_only_on_the_state_it_is_given; v41 by the same test; v42 by test_replay_refuses_a_log_that_is_not_twenty_turns[19] (seed 0). Source: mutate_r11_new_v43-v46_0-49.out.",
)
REV["proj-verifier-mutants-r9-new"] = (
    "ledgers/PC3/mutants/v35..v38",
    "Re-verified round 11 (mutate_r11_new_v43-v46_0-49.out): " + "; ".join(f"{n[:3]} {MUT[n]['status']} by {MUT[n]['killer']}" for n in mut_ids(["v35", "v36", "v37", "v38"])) + ".",
)
REV["proj-builder-mutants"] = (
    "ledgers/PC3/mutants/m01..m10",
    mut_ev(mut_ids([f"m{i:02d}" for i in range(1, 11)])),
)
REV["proj-mutant-m08-description"] = None  # carried (mutant file byte-identical)
REV["proj-verifier-mutants"] = (
    "ledgers/PC3/mutants/v01..v16 and v18..v26 (v17 absent)",
    mut_ev(mut_ids([f"v{i:02d}" for i in list(range(1, 17)) + list(range(18, 27))])),
)
REV["proj-verifier-mutants-r3-new"] = (
    "ledgers/PC3/mutants/v13..v16",
    mut_ev(mut_ids(["v13", "v14", "v15", "v16"])),
)
REV["proj-r4-new-mutants-v18-v20"] = (
    "ledgers/PC3/mutants/v18..v20",
    mut_ev(mut_ids(["v18", "v19", "v20"])),
)
REV["proj-grader-v21-replay-scales-by-size"] = ("ledgers/PC3/mutants/v21", mut_ev(mut_ids(["v21"])))
REV["proj-grader-v22-zero-fill-price-refused"] = ("ledgers/PC3/mutants/v22", mut_ev(mut_ids(["v22"])))
REV["proj-r5-mutant-v23-first-fill-price"] = ("ledgers/PC3/mutants/v23", mut_ev(mut_ids(["v23"])))
REV["proj-grader-v24-stderr-print-survives"] = ("ledgers/PC3/mutants/v24", mut_ev(mut_ids(["v24"])))
REV["proj-grader-v25-last-filled-totals-survives"] = ("ledgers/PC3/mutants/v25", mut_ev(mut_ids(["v25"])))
REV["proj-grader-v26-logging-warning-survives"] = ("ledgers/PC3/mutants/v26", mut_ev(mut_ids(["v26"])))
REV["proj-verifier-mutants-r7-new"] = (
    "ledgers/PC3/mutants/v27..v30",
    mut_ev(mut_ids(["v27", "v28", "v29", "v30"])),
)
REV["proj-verifier-mutants-r8-new"] = (
    "ledgers/PC3/mutants/v31..v34",
    mut_ev(mut_ids(["v31", "v32", "v33", "v34"])),
)
REV["proj-alternatives-1-2-4-5"] = ("ledgers/PC3/alternatives/alt1, alt2, alt4, alt5", ALT_EV)
REV["proj-alt3-replay"] = ("ledgers/PC3/alternatives/alt3_inventory_skew.py", ALT_EV)
REV["proj-alternative-6"] = ("ledgers/PC3/alternatives/alt6_quote_mid_from_first_fill.py", ALT_EV)
REV["proj-alternative-7-8-verifier"] = ("ledgers/PC3/scripts/PC3-c-r2/alt7, alt8", ALT_EV)
REV["proj-alternative-9-10-verifier-r3"] = ("ledgers/PC3/scripts/PC3-c-r3/alt9, alt10", ALT_EV)
REV["proj-alternatives-r4-new"] = ("ledgers/PC3/scripts/PC3-c-r4/alts/alt11, alt12, alt13", ALT_EV)
REV["proj-alternatives-r7-new"] = ("ledgers/PC3/scripts/PC3-c-r7/alts/alt20..alt24", ALT_EV)
REV["proj-r8-alternatives-new"] = ("ledgers/PC3/scripts/PC3-c-r8/alts/alt_r8_a..e", ALT_EV)
REV["proj-r5-alternatives-14-16"] = ("ledgers/PC3/scripts/PC3-c-r5/alts/alt14, alt15, alt16", ALT_EV)
REV["proj-alternatives-r10-new"] = (
    "ledgers/PC3/scripts/PC3-c-r10/alts/alt_r10_a..d",
    ALT_EV,
)
REV["proj-r10-instances-20-seeds"] = None  # carried
REV["proj-grader-v21-replay-scales-by-size"] = REV["proj-grader-v21-replay-scales-by-size"]

REV["proj-grader-v39-killed-note"] = None
del REV["proj-grader-v39-killed-note"]

NEW_ROWS = [
    {
        "id": "proj-grader-v44-limit-lock-survives",
        "check": "2.6-mutants (a student-error mutant that violates a stated rule must be killed by the suite)",
        "location": "ledgers/PC3/mutants/v44_quote_crosses_at_the_limit.py (round 11, mine); course/modules/PC/PC3/project.html line 395 ('A quote must have its bid below its ask, and its size must lie in 0 to 5'); course/modules/PC/PC3/grader/test_project.py test_quotes_are_legal_on_every_turn (games only)",
        "status": "FAIL",
        "evidence": "mutate_graders.py --unit PC3 --seeds 0-49 (mutate_r11_new_v43-v46_0-49.out): 'SURVIVED v44_quote_crosses_at_the_limit.py'. v44 posts a locked quote (bid equal to ask) whenever the inventory it sees has |inventory| >= 10. maxinv.out: the reference's largest |inventory| over seeds 0-49 is 8 and no fixed seed reaches 10, so no game reaches the locked state and the suite's per-game legality test never sees it. project.html line 395 states the bid-below-ask rule with no seed qualifier, and the engine refuses such a quote with ValueError. The other 54 mutants, including the three new ones v43, v45 and v46, are killed.",
        "fix": "Add a direct-call legality test to grader/test_project.py that sweeps quote over inventory -10..10 at turns 1 and 20 with an empty history and asserts bid < ask and 0 <= size <= 5 (message naming the turn and inventory). probe_legal_sweep.out: the probe kills v44 and passes the reference, alt4_size_scaled_by_inventory, alt_r11_b and alt_r11_c. Then update project.html line 397 (9 x 51 + 24 + 3 = 486 and 9 x 52 + 24 + 3 = 495; 'Two further checks' becomes 'Three further checks'), re-run collect-only, mutate_graders.py --seeds 0-49 and the 38 alternatives.",
    },
    {
        "id": "proj-direct-call-test-docstring",
        "check": "2.6-spec (a docstring states what the test does)",
        "location": "course/modules/PC/PC3/grader/test_project.py lines 429-433 (docstring 'A direct call, with no engine.') against line 452 (engine.play(sol.quote, 0))",
        "status": "FAIL",
        "evidence": f"Read of the delta ({DELTA}, hunk @@ -425,6 +425,38 @@): the docstring of test_a_direct_call_on_a_hand_built_state_ignores_an_earlier_game opens 'A direct call, with no engine.' and then says 'one other game is played'; line 452 calls engine.play(sol.quote, 0). The docstring contradicts the body.",
        "fix": "Replace the first sentence of the docstring with 'A direct call on a hand-built state; the engine plays one other game in between.' Docstring text only; the body and the count are unchanged.",
    },
    {
        "id": "proj-plan-play-policy-signature",
        "check": "2.6-spec (the plan's engine and test contract names the engine's signature)",
        "location": "plans/PC3-build-plan.md line 415 ('Log shape. play(policy, seed) returns exactly 20 turn records') against plans/PC3-build-plan.md line 357 (play(quote, seed)) and course/modules/PC/PC3/grader/engine.py line 49 (def play(quote: QuoteFn, seed: int))",
        "status": "FAIL",
        "evidence": "grep of the plan after the delta: line 357 and the engine both say play(quote, seed); line 415 still says play(policy, seed). The file names were fixed in the delta (proj-plan-file-names), but this stale call form in the plan's log-shape contract was not.",
        "fix": "In plans/PC3-build-plan.md line 415 change 'play(policy, seed)' to 'play(quote, seed)' (text only; plan is architect-owned).",
    },
    {
        "id": "proj-verifier-mutants-r11-new",
        "check": "2.6-mutants (round 11 student-error mutants of the verifier's own design)",
        "location": "ledgers/PC3/mutants/v43_replay_marks_one_turn_early.py, v45_replay_skips_informed_fills.py, v46_quote_reads_a_global_only_on_turn_one.py",
        "status": "PASS",
        "evidence": "mutate_r11_new_v43-v46_0-49.out: " + "; ".join(f"{n[:3]} {MUT[n]['status']} by {MUT[n]['killer']}" for n in ["v43_replay_marks_one_turn_early.py", "v45_replay_skips_informed_fills.py", "v46_quote_reads_a_global_only_on_turn_one.py"]) + ". Each is a complete module with a one-line student-error docstring; v44 is listed as its own failing row.",
    },
    {
        "id": "proj-alternatives-r11-new",
        "check": "2.7-alternatives (correct alternatives must pass; over-constraint check)",
        "location": "ledgers/PC3/scripts/PC3-c-r11/alts/alt_r11_a..d (four new correct implementations: reverse scan with size 0 at the limit; cash-shifted mid with a 2-cent spread; dataclass record with size 0 from |inventory| 6; parity size with a while loop replay)",
        "status": "PASS",
        "evidence": ALT_EV + " The four new alternatives are in r11_alts_0-49.out as alt_r11_a..d, each 'fails on 0 of 50 seeds'. The new direct-call tests pass on them, so the round-11 test additions do not over-constrain correct quotes.",
    },
    {
        "id": "proj-rubric-ladder-exclusive-highest-level",
        "check": "2.6-rubric (descriptors exclusive and exhaustive)",
        "location": "course/modules/PC/PC3/project.html lines 623-627",
        "status": "PASS",
        "evidence": "Read of project.html lines 623-627 (all five ladders, four cells each). Convention: a submission takes the highest level whose cell it meets. C1 and C2 cells are nested ('two or more' contains 'the three values'; 'at least three turns' contains 'two turns'), so the overlaps resolve upward; C3 and C5 were checked class by class (C3: both runs with a unitless difference -> L3, one run -> L2, another seed or no rerun -> L2, amount not in cents with both runs -> L3 or L1 resolved to L3, no amount in cents -> L1; C5: word result -> L3, no result -> L2, no check or wrong-number -> L1, number replay produces -> L4). C4: four items named with results -> L4, three -> L3, one or more -> L2, none -> L1. No submission class gets two different levels under the convention.",
    },
    {
        "id": "proj-exemplar-scores-blind-disclosure",
        "check": "2.6-rubric (blind calibration; disclosure of any unblinded read)",
        "location": "course/modules/PC/PC3/project.html lines 637, 651-660, 666, 680-688 (official scores and annotations)",
        "status": "PASS",
        "evidence": "Disclosed in notes: an early grep printed the official-scoring lines and the annotation lines before the blind scoring. The calibration rows (proj-exemplar-a-calibration, proj-exemplar-b-calibration) record scores from the passage text against the descriptors, and the scores match the official ones; the disclosure is carried on those rows.",
    },
]

# Assemble the rows, in the round 10 order, and check that every round 10 id is accounted for.
rows = []
missing = []
for prev in PREV["rows"]:
    rid = prev["id"]
    if rid in REV and REV[rid] is not None:
        loc, ev = REV[rid]
        rows.append({"id": rid, "check": prev["check"], "location": loc, "status": "PASS", "evidence": ev})
    elif rid in CARRY:
        grp = CARRY[rid]
        rows.append({
            "id": rid,
            "check": prev["check"],
            "location": prev["location"],
            "status": "PASS",
            "evidence": f"Carried from round 10 ({CARRY_GROUP[grp]}): " + prev["evidence"],
        })
    else:
        missing.append(rid)
assert not missing, missing
known = {r["id"] for r in PREV["rows"]}
assert set(REV) - known == set(), set(REV) - known
for r in NEW_ROWS:
    rows.append(r)

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"

mutants = []
for name, v in MUT.items():
    mutants.append({
        "id": name,
        "description": v["desc"],
        "killed_by": v["killer"] if v["status"] == "KILLED" else None,
        "status": v["status"],
    })

fails = [r["id"] for r in rows if r["status"] != "PASS"]
verdict = "FAIL" if fails else "PASS"
passes = sum(1 for r in rows if r["status"] == "PASS")
counts = {"rows": len(rows), "PASS": passes, "FAIL": len(fails), "UNVERIFIABLE": 0}

fragment = {
    "unit": "PC3",
    "slice": "c",
    "round": 11,
    "verifier": "independent verifier (Haiku 5.5), round 11, slice c (did not build PC3)",
    "pin": "11d7077a",
    "base": "round 10 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round10.json (pin 00a84795). Delta 00a84795..11d7077a for slice c: course/modules/PC/PC3/project.html (lines 53, 397, 625, 627), course/modules/PC/PC3/grader/test_project.py (new test lines 428-453, inserted before the instance tests), plans/PC3-build-plan.md (lines 67-70, 317, 337, 340, 348, 357, 363-380, 399, 410-456 and others, all naming market_maker.py), course/modules/PC/PC3/L04.html (not in slice c's gates; read for the C4 clause), ledgers/PC3/mutants/v39..v42 (round 10 mutants). Not changed in slice c: engine.py, instance.py, reference.py, starter.py, tests/labs/PC3/lab-PC3-project-1..3.py, grader.js, alternatives, notation, index.html.",
    "checkout": ROOT,
    "scratch": "/tmp/pc3c-r11-* (maxinv, strict, collect, list, probe, alts, twin, num) and ledgers/PC3/scripts/PC3-c-r11/ for every kept script and output",
    "verified_at": "2026-11-05T11:58:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Gates on pin 11d7077a (scripts and outputs under ledgers/PC3/scripts/PC3-c-r11/): check_pages, check_dag, check_projects PASS for PC3 (gates_check.out, exit 0); run_labs PC3 project 3/3 (run_labs_PC3_project.out); twins alone under python -I -W error exit 0, empty stderr (twin_project_1..3.exit); page code vs twin and expected blocks vs twin stdout (page_vs_twin.out, expected_vs_output.out); page_smoke PC3 project PASS, in-browser 494 on seed 34135437 (page_smoke_project.out); run_graders PC3 0-49 reference 50/50 (run_graders_PC3.out); mutate_graders --unit PC3 --seeds 0-9 on the 51 existing mutants: 51/51 killed (mutate_r11_0-9.out); mutate_graders --seeds 0-49 on 55 mutants (51 existing + v43, v44, v45, v46 of mine): 54 killed, v44 survived (mutate_r11_new_v43-v46_0-49.out); 38 alternatives on seeds 0-49: all 0 of 50 fail (r11_alts_0-49.out); collect-only 485 for seeds 0, 1, 7, 49 and 494 for 50, 848197495, 1712259056, 34135437 (r11_collect.out); ruff check and format PASS (ruff_check.out, ruff_format.out, ruff_repo.out); mypy --no-incremental: 385 files, no issues (mypy_repo.out); mypy --strict on grader and labs in a scratch copy (reference as market_maker.py): 7 files, no issues (mypy_strict_scratch.out); starter fails 419 tests (starter_fails.out); pytest -k PC3: 9 passed (pytest_k_PC3.out); verify_refs --offline: 560 entries, 0 problems (verify_refs_offline.out); maxinv.out (reference max |inventory| 8 on seeds 0-49); numbers_r11.out (exemplar and Lab 3 numbers recomputed); probe_legal_sweep.out (the v44 probe). "
        "Blind scoring disclosure: my first grep of project.html printed the official-scoring lines (637, 666) and annotation lines (651-688) before scoring. The exemplar scores in the calibration rows were then derived from the passage text and the descriptors, and they match the official scores; treat the calibration as disclosed, not fully blind. "
        "Exclusivity convention: the ladders are read by the highest level whose cell the submission meets; this makes every submission map to one level and is stated in proj-rubric-ladder-exclusive-highest-level. "
        "Round 10 FAIL rows now PASS: proj-plan-file-names (plan renamed to market_maker.py), proj-grader-state-between-turns and proj-verifier-mutants-r10-new (v39-v42 killed by the new direct-call test), proj-rubric-ladder-gap-c3-difference-no-unit and proj-rubric-ladder-gap-c5-wrong-number (ladder cells changed). "
        "Non-FAIL observations: the C2 and C3 ladders accept a wrong cited value only as a mismatch in C2 (explicit) and not in C3 (level 4 reads 'reports the change in cents' without requiring it to equal the difference); the C3 rule is literal and classifies the submission, so it is recorded as a clarity suggestion, not a FAIL. The plan's 5.4 criterion wording is shorter than the page's (for example 'the policy works' versus 'the rule works'); the page is the binding text. "
        "Not checked: the in-browser self-assessment form (JavaScript; not in slice c's gates); cards.json (slices a and b); L04.html and L06.html beyond the cited sentence; plan sections outside the delta hunks (carried); Pyodide timing per test (only the pytest path and page_smoke's in-browser run were used)."
    ),
    "summary": (
        f"PC3-c round 11: verdict {verdict}. Rows {counts['rows']}: PASS {counts['PASS']}, FAIL {counts['FAIL']}, UNVERIFIABLE 0. "
        "FAIL rows: proj-grader-v44-limit-lock-survives (a student quote that locks at the inventory limit survives: no fixed seed reaches |inventory| 10, and the suite tests legality on games only; project.html line 395 states the rule unqualified; probe sweep kills it); "
        "proj-direct-call-test-docstring (test_project.py line 429 says 'with no engine' while line 452 calls engine.play); "
        "proj-plan-play-policy-signature (plan line 415 still says play(policy, seed)). "
        "Closed since round 10: proj-plan-file-names, proj-grader-state-between-turns, proj-verifier-mutants-r10-new, proj-rubric-ladder-gap-c3-difference-no-unit, proj-rubric-ladder-gap-c5-wrong-number. "
        "Counts: collect 485 (seeds 0-49) and 494 (other), matching page line 397."
    ),
}

out = ROOT + "/ledgers/PC3/PC3-c.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", counts, "verdict", verdict, "mutants", len(mutants), "fails", fails)
