"""Round 18, PC3 slice c. Builds ledgers/PC3/PC3-c.json from the round-17 fragment, the round-18 evidence and the mutate output.

Rows re-verified in round 18 get fresh evidence. Other PASS rows are carried when the subject they cite is byte-identical
since the previous pin 700bf33f (see the notes). Exemplar rows are not carried: exemplar scoring belongs to the blind scorer.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE18-PC3-c")
PREV = Path("/Users/billyribeiro/.fanout/frags/E-PC3-c.round17.json")
OUT_DIR = ROOT / "ledgers/PC3/scripts/PC3-c-r18/out"
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

prev = json.loads(PREV.read_text(encoding="utf-8"))

DELEGATED = {
    "proj-exemplar-a-calibration",
    "proj-exemplar-b-calibration",
    "proj-exemplar-b-numbers",
    "proj-exemplar-b-arrival-sensitivity",
    "proj-exemplar-a-numbers",
    "proj-exemplar-scores-blind-disclosure",
    "proj-r17-blind-status",
    "proj-exemplar-levels-vs-plan",
    "proj-exemplar-levels-check-count",
    "proj-exemplar-a-c5-annotation",
    "proj-r15-exemplar-intro-fill-numbers",
    "proj-r16-exemplar-annotation-vs-rubric",
    "proj-exemplar-scores-in-served-html",
    "proj-r14-self-assessment-disclosure",
}

MUT_OUT = (OUT_DIR / "mutate_pc3_0_49_final.out").read_text(encoding="utf-8").splitlines()
killed = []
for line in MUT_OUT:
    m = re.match(r"KILLED (\S+?): (.*) -> (.*)$", line)
    if m:
        killed.append({"name": m.group(1), "description": m.group(2).strip(), "killed_by": m.group(3).strip()})
assert len(killed) == 92, len(killed)
assert all(k["killed_by"] for k in killed)

GATE = "out/mutate_pc3_0_49_final.out (mutate_graders --unit PC3 --seeds 0-49: 92 of 92 KILLED)"

FRESH: dict[str, tuple[str, str, str]] = {}


def fresh(rid: str, location: str, evidence: str, status: str = "PASS") -> None:
    FRESH[rid] = (status, location, evidence)


fresh("proj-grader-35-checks", "course/modules/PC/PC3/project.html line 397; course/modules/PC/PC3/grader/test_project.py (collect-only)",
      "Round 18 collect-only (ledgers/PC3/scripts/PC3-c-r18/collect_counts_r18.sh, out/collect_counts.out): 489 tests for seed 0 and 498 for seed 77314143. "
      "Decomposition: 9 seed-parametrized functions over 51 seeds (seed 0) or 52 (seed 77314143) = 459 or 468; 27 seed-only items and 3 seed-free items "
      "(test_fixed_seeds_0_to_49_give_fifty_different_paths, test_a_direct_call_on_a_hand_built_state_ignores_an_earlier_game, "
      "test_a_direct_quote_is_legal_at_every_inventory_within_the_limit) = 30. 459 + 30 = 489; 468 + 30 = 498. Line 397 states 489/498 and 9 x 51 + 27 + 3 = 489, 9 x 52 + 27 + 3 = 498: matches.")
fresh("proj-r15-grading-counts", "course/modules/PC/PC3/project.html line 397; course/modules/PC/PC3/grader/test_project.py (collect-only)",
      "Same collect-only run as proj-grader-35-checks (out/collect_counts.out): line 397 counts (489 for seeds 0-49, 498 otherwise; 27 seed-only and 3 seed-free checks; 9 seed-parametrized checks) match the collection.")
fresh("proj-grader-seed-scope-claim", "course/modules/PC/PC3/project.html line 397; course/modules/PC/PC3/grader/test_project.py lines 36-38 (SEED, FIXED_SEEDS, SEEDS)",
      "SEEDS = fixed seeds 0-49 plus SEED and SEED + 7919 (lines 36-38, unchanged). Line 397: 51 seeds when the learner's seed is in 0-49, 52 otherwise. Collected counts agree (out/collect_counts.out: 51 x 9 and 52 x 9).")
fresh("proj-hub-seed-scope", "course/modules/PC/PC3/index.html lines 55 and 160; course/modules/PC/PC3/project.html line 397",
      "Hub line 55 and line 160 name seeds 0 to 49, the learner's workspace seed and (line 160) that seed plus 7919, which is the seed set of project.html line 397 and of test_project.py SEEDS. Consistent.")
fresh("proj-local-commands", "course/modules/PC/PC3/project.html lines 448-450 (--assert=plain paragraph); course/modules/PC/PC3/grader/test_project.py must_refuse lines 52-60 and calls at lines 264 and 271",
      "Round 17 FAIL (wrong sentence). Line 450 now says a ValueError raised by the learner's replay is caught in the two refusal checks and the check passes only if its message names the condition. Code: must_refuse catches ValueError only around call(), which is the learner's replay at lines 264 and 271 (other must_refuse calls wrap engine.play with suite lambdas). Probe ledgers/PC3/scripts/PC3-c-r18/probe_wrong_wording_r18.py (ValueError 'oops, wrong length'): 2 failed, test_replay_refuses_a_log_that_is_not_twenty_turns[19] and [21] (out/probe_wording_and_type_r18.out). Probe probe_type_error_r18.py (TypeError): 1 failed, test_filled_turn_without_a_price_is_refused, as a traceback. The sentence matches the code. test_project.py contains no assert statement (grep '^\\s*assert ' returned nothing), so --assert=plain changes nothing.",
      "PASS")
fresh("proj-rubric-observable", "course/modules/PC/PC3/project.html lines 620-627 (rubric rows C1-C5)",
      "Read in full in round 18. Every level cell names an observable: turn numbers and fields, equality with replay output, values matching the log, a rerun with its P&L in cents, named items, a named check with its number. No vague descriptor found.")
fresh("proj-rubric-ladder-gap-c1", "course/modules/PC/PC3/project.html line 623 (C1 level 2 cell)",
      "C1 level 2: 'two or more of the three values, each equal to replay, and no value that replay does not return'. Re-read after the round-18 change to the level-4 and level-3 cells: a submission with two or three correct values and no unreturned value meets level 2 unless it meets level 3 or 4, which require the three values and turns named. Every submission is covered once.")
fresh("proj-rubric-ladder-gap-c1-no-pnl", "course/modules/PC/PC3/project.html line 623 (C1 levels 1-3)",
      "C1 levels 1-3 as now written: level 3 needs the three values and cash-flow turns, level 2 two or more correct values, level 1 fewer than two correct values or any unreturned value. A submission with fewer than two correct values or with no pnl_cents is at level 1; the descriptors are exhaustive over the counts.")
fresh("proj-rubric-ladder-exclusive-highest-level", "course/modules/PC/PC3/project.html caption line 620 and cells lines 623-627",
      "Caption: highest level whose descriptor is met. C1 after round 18: L4 = three correct values + both turn sets + no unreturned value; L3 = three correct + cash-flow turns only + no unreturned value; L2 = two or more correct + no unreturned value; L1 = fewer than two correct or any unreturned value. Levels are exclusive by the count and the turn clauses, and exhaustive. C2-C5 unchanged in this round.")
fresh("proj-r17-rubric-c1-levels", "course/modules/PC/PC3/project.html line 623 (C1 cells, levels 4 to 1)",
      "Round 17 FAIL: levels 4 and 3 did not forbid a value replay does not return. Line 623 now ends the level-4 and level-3 cells with 'and states no value that replay does not return'. Level 2 and 1 clauses unchanged. A submission stating the three correct values, naming the turns and also an unreturned value fails levels 4 and 3, and level 2 ('no value that replay does not return'), and lands at level 1. Verified by reading line 623.",
      "PASS")
fresh("proj-r17-mutant-r17_02", "ledgers/PC3/mutants/r17_02_replay_side_from_arrival_for_uninformed_fills.py; course/modules/PC/PC3/grader/test_project.py test_a_fill_takes_its_side_from_its_price_not_its_arrival (lines 386-400)",
      "Round 17 survivor. The new test (lines 386-400, two parametrizations) kills it: " + GATE + " lists KILLED r17_02 -> test_a_fill_takes_its_side_from_its_price_not_its_arrival. The reference passes the new test (out/candidates_seed0.out, out/candidates_seed77314143.out).",
      "PASS")
fresh("proj-r16-mutants-76", "ledgers/PC3/mutants/ (92 files at 50559266); course/modules/PC/PC3/grader/test_project.py; " + "out/mutate_pc3_0_49_final.out",
      "Round 17 FAIL (78 of 79 killed). Round 18: mutate_graders --unit PC3 --seeds 0-49 over all 92 listed mutants: 92 killed, 0 survived (" + GATE + "). Each file defines exactly one quote and one replay (grep count 92 of 92).")
fresh("proj-r17-scope-words", "course/modules/PC/PC3/project.html lines 1-631 and 695-732 (every line outside the exemplar passages)",
      "Scope words (every, only, same, any, exactly, all, always, never) listed by grep on the non-exemplar lines and checked: 'Every instance is SIMULATED' (instance.py label 'SIMULATED'); 'every accounting value is an int' (lab 3 twin, types checked); 'Twenty-seven checks run on your seed only' (collect-only: 27 seed-only items); 'a quote depends only on the state it is given' (two state tests plus the direct-sweep test); 'exactly 20 turns' (engine and replay); 'the same game' (labs 1 and 2 both seed 0 and rule); 'the lab does not test any other seed' (lab 3 twin uses SEED = 0 only). No unsupported scope word.")
fresh("proj-banned-and-process-words", "course/modules/PC/PC3/project.html lines 1-631 and 695-732; course/modules/PC/PC3/grader/*.py; tests/labs/PC3/lab-PC3-project-*.py",
      "grep -i for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, important to note, studies show, experts agree, well known, obviously, clearly, verifier, fixer, builder, architect, ruling, round N, carried, audit and ellipses: no hit (the 'round' hits are inside 'around'). check_pages --unit PC3 PASS (out/check_pages_unit.out), which applies the banned-string rule of BUILDER_RULES 1.3-1.4.")
fresh("proj-notation", "course/modules/PC/PC3/project.html math spans outside lines 632-694; notation/notation.json (8 symbols)",
      "Math spans used: N, t, v_t, v_0, v_20, a_t, b_t, a, b, q_t, I, I_20, |I|, pnl and integers. None of the registered symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) appears, so no collision. N is the page-local turn count; L04 declares N, t, p and L local to that lesson.")
fresh("proj-r16-notation-and-terms", "course/modules/PC/PC3/project.html math spans; notation/notation.json",
      "Same check as proj-notation: no registered symbol is used with another meaning; inventory I and the quote symbols are not registered and are defined on the page (Conventions).")
fresh("proj-r17-delta-hunks", "course/modules/PC/PC3/project.html lines 397, 450, 623; course/modules/PC/PC3/grader/test_project.py lines 386-400; ledgers/PC3/mutants (13 files added)",
      "Delta 700bf33f..50559266 read hunk by hunk (git diff -U0): project.html changes exactly lines 397, 450 and 623 (same line count); test_project.py one hunk @@ -383,6 +383,22 @@ adding test_a_fill_takes_its_side_from_its_price_not_its_arrival at lines 386-400; ledgers/PC3/mutants gains fx17_01..fx17_10 and r17_01..r17_03 (insertions only); alternatives, labs twins, engine.py, instance.py, reference.py, starter.py unchanged. Each hunk is re-verified by its own row in this fragment.")
fresh("proj-r17-gates", "ledgers/PC3/scripts/PC3-c-r18/gates_r18.sh; gates_extra_r18.sh; out/",
      "Round-18 gate set run on 50559266: check_dag, check_projects, run_labs (3/3), run_graders 0-49 (50/50), page_smoke --pages project (PASS, 498 in-browser tests), check_pages --unit PC3, verify_refs --offline (560 entries, 0 problems), verify_refs --unit PC3 (2 of 560, 0 problems), mutate 0-49 (92/92), ruff (repo), ruff format (repo), mypy (repo, 385 files), pytest on tests/test_labs.py and test_page_checks.py -k PC3 (9 passed), pytest on tests/test_run_labs.py and tests/test_page_smoke.py (full: 2 and 8 passed). check_pages --page project is a tool misuse (applies lesson rules to the project page) and is not used as evidence; the whole-unit run is.")
fresh("proj-r17-spec-command", "course/modules/PC/PC3/project.html line 393 (python3 -c command for game_log.json)",
      "Ran the documented command in a scratch copy with engine.py, instance.py and reference.py as market_maker.py, seed 0: valid JSON with keys seed, settlement_cents, turns (20 records, keys as line 393 lists). replay gives cash_flow_cents -9950, inventory_end 1, inventory_mark_cents 9980, pnl_cents 30, equal to Lab 1. Scratch removed.")
fresh("proj-r17-twin-vs-page", "course/modules/PC/PC3/project.html lab sections lab-PC3-project-1..3 (lines 55-612); tests/labs/PC3/lab-PC3-project-1..3.py",
      "run_labs.py --unit PC3 --page project: PASS 3/3 (out/run_labs_project.out). The tool requires each page code line to equal its twin line (or contain a blank for the completion lab) and each expected block to equal the twin's printed output under python -I -W error. Lab 2 blanks: lines 349-350 only.")
fresh("proj-r17-alternatives-six", "ledgers/PC3/alternatives/alt1..alt6",
      "Re-run on the round-18 suite (which contains the new test): alt1 to alt6 exit 0 on seed 0 (489 passed) and on seed 77314143 (498 passed). out/candidates_seed0.out, out/candidates_seed77314143.out.")
fresh("proj-r16-alternatives-five-new", "ledgers/PC3/scripts/PC3-c-r16/alternatives/alt_r16_1..5*.py",
      "Re-run round 18: all five exit 0 on seed 0 (489) and on seed 77314143 (498). out/alt_r16_seed0_r18.out, out/alt_r16_seed77314143_r18.out.")
fresh("proj-r16-alternatives-prior-52", "52 prior candidate modules listed in ledgers/PC3/scripts/PC3-c-r18/out/candidate_modules_r18.txt (from ledgers/PC3/scripts/PC3-c-r17/out/prior_candidates_list_r17.txt, helpers removed)",
      "Round 18 re-run on the current suite: 52 of 52 exit 0 on seed 0 and 52 of 52 on seed 77314143 (out/prior_candidates_seed0_r18.out, out/prior_candidates_seed77314143_r18.out). The new test does not over-constrain any of them.")
for rid in ["proj-r15-alternatives-all", "proj-r14-alternatives-15"]:
    fresh(rid, "the 52 prior candidate modules and ledgers/PC3/alternatives/alt1..alt6",
          "Covered by the round-18 re-run of the 52 prior candidates and alt1..alt6 on seeds 0 and 77314143 (out/prior_candidates_seed0_r18.out, out/prior_candidates_seed77314143_r18.out, out/candidates_seed0.out, out/candidates_seed77314143.out): all exit 0.")
for rid in ["proj-quote-rule-first-fill-survivor", "proj-alternatives-1-2-4-5", "proj-alt3-replay", "proj-alternative-6",
            "proj-alternative-7-8-verifier", "proj-alternative-9-10-verifier-r3", "proj-alternatives-r4-new", "proj-alternatives-r7-new",
            "proj-r8-alternatives-new", "proj-alternatives-r10-new", "proj-alternatives-r11-new", "proj-alt-turn-indexed-history-overconstrained",
            "proj-alternatives-r12-b-e", "proj-r5-alternatives-14-16"]:
    fresh(rid, "the alternative modules named in the round-17 row, re-run on the round-18 suite",
          "Re-run in round 18 on the current suite (including the new test): each module is one of the 52 prior candidates or alt1..alt6, all exit 0 on seeds 0 and 77314143 (out/prior_candidates_seed0_r18.out, out/prior_candidates_seed77314143_r18.out, out/candidates_seed0.out, out/candidates_seed77314143.out).")
fresh("proj-r8-collect-counts", "course/modules/PC/PC3/grader/test_project.py (collect-only, seeds 0 and 77314143)",
      "collect_counts_r18.sh (out/collect_counts.out): 489 tests for seed 0; 498 for seed 77314143; per-function counts listed in proj-grader-35-checks.")
fresh("proj-r8-pytest-pc3", "tests/test_labs.py -k PC3; tests/test_page_checks.py -k PC3; tests/test_run_labs.py; tests/test_page_smoke.py",
      "pytest tests/test_labs.py tests/test_page_checks.py -k PC3: 9 passed (out/pytest_labs_pc3.out). tests/test_run_labs.py and tests/test_page_smoke.py are generic (no PC3 test id, so -k PC3 collects nothing and exits 5); run in full: 2 + 8 passed (out/pytest_run_labs_page_smoke.out).")
fresh("proj-r8-verify-refs", "tools/verify_refs.py --offline; tools/verify_refs.py --unit PC3",
      "Offline over the whole registry: 560 entries, 0 problems (out/verify_refs_offline_all.out). Live --unit PC3: 2 of 560 entries re-verified, 0 problems (out/verify_refs_live_pc3.out). The two keys are zhou2008practical and crack2015heard.")
fresh("proj-references", "course/modules/PC/PC3/project.html reading list (data-cite zhou2008practical, crack2015heard); references/references.json",
      "Live re-verification of the two keys: 0 problems (out/verify_refs_live_pc3.out); the Reading section names no problem, answer, page or edition (read in full).")
fresh("proj-r14-reading-keys", "course/modules/PC/PC3/project.html reading list (data-cite lines); references/references.json",
      "Keys re-verified live (out/verify_refs_live_pc3.out): both present and both match the registry record. The reading list lines are unchanged since the previous pin.")
fresh("proj-page-smoke", "tools/page_smoke.py --unit PC3 --pages project (course/modules/PC/PC3/project.html)",
      "page_smoke --unit PC3 --pages project: PASS (out/page_smoke_project.out): zero console errors, zero external requests, labs 0.0 s each in Pyodide, in-browser grader 'All 498 tests pass on seed 2061445586 (1.4 s)'.")
fresh("proj-run-labs-unit", "tools/run_labs.py --unit PC3 --page project", "run_labs PC3 project: PASS (3/3) (out/run_labs_project.out).")
for rid in ["proj-check-tools", "proj-r8-check-tools", "proj-r15-gates", "proj-r8-run-labs-page-smoke"]:
    fresh(rid, "tools/check_pages.py --unit PC3; tools/check_dag.py --unit PC3; tools/check_projects.py --unit PC3; tools/run_labs.py; run_graders; page_smoke",
          "Round 18: check_pages --unit PC3 PASS (out/check_pages_unit.out); check_dag PASS (out/check_dag_unit.out); check_projects PASS (out/check_projects_unit.out); run_labs PASS 3/3; run_graders 0-49 PASS 50/50 (out/run_graders_0_49.out); page_smoke project PASS.")
fresh("proj-lint-ruff", "ruff check and ruff format --check on course/modules/PC/PC3, tests/labs/PC3, ledgers/PC3; repo ruff check . and ruff format --check .",
      "Round 18: ruff check on the slice exit 0 (out/ruff_check_slice.out); ruff format --check on the slice exit 0 (out/ruff_format_slice.out); repo ruff check . exit 0 (out/ruff_repo.out); repo ruff format --check . exit 0, 553 files (out/ruff_format_repo.out).")
fresh("proj-r14-lint-mypy-pytest", "ruff; repo mypy; pytest on PC3 selections",
      "Round 18: ruff repo and slice clean; repo mypy --no-incremental: 'Success: no issues found in 385 source files' (out/mypy_repo.out); pytest PC3 selections pass (out/pytest_labs_pc3.out, out/pytest_run_labs_page_smoke.out).")
fresh("proj-mypy-labs", "tests/labs/PC3 twins; repo mypy (files = tools, tests)", "Repo mypy --no-incremental: 385 source files, no issues (out/mypy_repo.out); tests/labs/PC3 twins are in the scope.")
for rid in ["proj-grader-mypy-strict", "proj-r15-mypy-strict-grader", "proj-r16-grader-mypy-note"]:
    fresh(rid, "course/modules/PC/PC3/grader/engine.py, instance.py, test_project.py, market_maker.py (= reference.py)",
          "Round 18 mypy --strict on the four files in a scratch copy: 'Success: no issues found in 4 source files' (ledgers/PC3/scripts/PC3-c-r18/mypy_grader_r18.sh, out/mypy_grader_strict_r18.out).")
fresh("proj-grader-reference", "course/modules/PC/PC3/grader/reference.py via tools/run_graders.py --unit PC3 --seeds 0-49",
      "run_graders PC3: PASS (reference 50/50 seeds, slowest 0.6 s) (out/run_graders_0_49.out). Also the suite passes reference.py at seeds 0 and 77314143 (out/candidates_seed0.out, out/candidates_seed77314143.out).")
fresh("proj-r16-reference-collect-and-starter", "course/modules/PC/PC3/grader/test_project.py; grader/reference.py; grader/starter.py",
      "reference.py: 489 passed (seed 0), 498 passed (seed 77314143); starter.py: fails (423 and 431 failed on seeds 0 and 77314143). out/candidates_seed0.out, out/candidates_seed77314143.out, out/starter_seed77314143_r18.out.")
for rid in ["proj-grader-starter-fails", "proj-r15-starter-fails"]:
    fresh(rid, "course/modules/PC/PC3/grader/starter.py with test_project.py in a scratch copy (seeds 0 and 77314143)",
          "starter.py exits 1 on seed 0 (423 failed, 66 passed) and seed 77314143 (431 failed, 67 passed); every failure is NotImplementedError from the stub. out/candidates_seed0.out, out/starter_seed77314143_r18.out.")
for rid in ["proj-grader-instances", "proj-r10-instances-20-seeds", "proj-r16-instance-sample"]:
    fresh(rid, "course/modules/PC/PC3/grader/instance.py; sample of 20 seeds",
          "ledgers/PC3/scripts/PC3-c-r18/sample_instances_r18.py (run with python -I; out/sample_instances.out): 20 of 20 sampled seeds (0, 1, 2, 3, 5, 8, 13, 21, 34, 49, 50, 77, 100, 255, 1000, 4096, 7919, 77314143, 2061445586, 123456789) give 21 positive integer fair values from 10000, each move exactly 5 cents, 20 arrivals from the three names, settlement = last value, and the same instance on a second call. 20 distinct fair paths; 20 distinct arrival sequences.")
fresh("proj-grader-messages", "course/modules/PC/PC3/grader/test_project.py expect() and must_refuse() (lines 44-60) and every expect message",
      "Read every expect and must_refuse message in the suite. Each names the property (for example 'a fill must be refused exactly when it would take |inventory| above 10'). None prints a computed value. must_refuse names the condition.")
for rid in ["proj-lab1-run", "proj-lab1-replay-prints", "proj-lab1-hypothesis-numbers", "proj-lab2-completion", "proj-lab3-counterfactual",
            "proj-twin-rules", "proj-exception-types-labs", "proj-r5-labs-page-vs-twin", "proj-r15-labs-twins-isolated"]:
    fresh(rid, "course/modules/PC/PC3/project.html Lab 1-3 sections (lines 55-612); tests/labs/PC3/lab-PC3-project-1..3.py",
          "run_labs PASS 3/3 (out/run_labs_project.out): page code equals twin, expected block equals output. Lab 1 hypothesis numbers (9 fills, -9950, 1, 9980, 30, max |inventory| 3 within 10) read from the output. Lab 3 counterfactual 15-cent half-spread: 9 fills, pnl 55, change 25 (lab output and interpretation line 611).")
fresh("proj-lab2-interpretation-last-quote", "course/modules/PC/PC3/project.html line 381 (Lab 2 interpretation)",
      "Line 381 says a mark other than the settlement value of 9980 cents changes the P&L on this seed. With inventory 1, P&L = cash flow + 1 x mark, so any other mark changes it by the difference: true. The lab output gives cash flow -9950 and mark 9980, P&L 30 (out/run_labs_project.out).")
fresh("proj-lab3-interpretation", "course/modules/PC/PC3/project.html line 611 (Lab 3 interpretation)",
      "Line 611: the 25-cent change is one seed; the lab runs only seed 0 (twin SEED = 0). Lab output: counterfactual pnl 55, change 25 (out/run_labs_project.out).")
fresh("proj-zero-fill-replay", "course/modules/PC/PC3/grader/test_project.py test_a_log_with_no_fill_replays_to_zero (lines 402-410 at 50559266; body unchanged)",
      "The test builds a 20-turn log with every turn unfilled (size 1, filled false) and compares replay with the oracle (zero cash, zero inventory, zero mark, zero P&L). Reference passes it on seeds 0 and 77314143 (out/candidates_seed0.out: 489 passed; out/candidates_seed77314143.out: 498 passed). The no-fill branch is exercised by test_no_function_prints_or_warns too (out/mutate_pc3_0_49_final.out, 92 of 92 killed).")
fresh("proj-r15-direct-states-log-wording", "course/modules/PC/PC3/project.html line 397 (third check wording); course/modules/PC/PC3/grader/test_project.py direct_states docstring (lines 134-138) and code (lines 139-151)",
      "Line 397 describes the third check: quote on hand-built states at every inventory -10..10, every turn 1..20 with unfilled history, and turns 2..20 after a fill at 9980, 9990, 10000, 10010, 10020 cents as a purchase at the bid and a sale at the ask, each quote legal. direct_states() builds exactly those two families (lines 139-151) with the history shapes its docstring states (lines 134-138). Matches.")
fresh("proj-r16-numbers-independent", "course/modules/PC/PC3/project.html lines 57, 393-407, 455-612 (non-exemplar numbers)",
      "Independent recomputation in round 18 (ledgers/PC3/scripts/PC3-c-r18/counterfactual_check_r18.py, out/counterfactual_check_r18.out): seed 0 at half-spread 10 gives 9 fills, cash flow -9950, inventory 1, settlement 9980, mark 9980, P&L 30; at half-spread 15 gives 9 fills and P&L 55, change 25. Conventions constants (N 20, v0 10000, moves 5, arrivals 1/4 1/4 1/2, limit 10, size 0..5) match engine.py and instance.py. Exemplar numbers (lines 632-694) are not checked here.")
fresh("proj-rubric-atlas-studios", "course/modules/PC/PC3/project.html (non-exemplar lines); tools/check_projects.py --unit PC3",
      "check_projects --unit PC3 PASS (out/check_projects_unit.out). PC3 is a module; the curriculum entry has no atlas key (curriculum/curriculum.json PC3 entry) and no studio requirement. Page read in full outside the exemplar passages.")
fresh("proj-plan-grader-seed-scope", "plans/PC3-build-plan.md lines 348 and 380; course/modules/PC/PC3/project.html line 397",
      "Plan requires the autograder on seeds 0-49 (lines 348, 380). The page adds the learner's seed and seed + 7919; the plan names no 7919 and does not forbid it, and the page's counts (489/498) match the collection. Superset, consistent with BUILDER_RULES 5.3 item 1.")
fresh("proj-r16-hours-estimate", "course/modules/PC/PC3/project.html lines 421-438 (time budget)",
      "Own estimate (round 18): read and annotate Lab 1 about 1 h; completion 1 h; quote 2-3 h; replay 1-2 h; autograder and local run 2 h; analysis 3-4 h; self-assessment 1 h: total about 11-14 h against 14 h, within 30 percent. Table sums to 14 (1+1+3+2+2+4+1).")
fresh("proj-hours-arithmetic", "course/modules/PC/PC3/project.html lines 421-438; course/modules/PC/PC3/index.html data-hours-lessons=36, data-hours-project=14; curriculum PC3 hours 50",
      "Table rows sum to 14 = data-hours-project (14) = hub figure. 36 + 14 = 50 = curriculum PC3 hours; 14 / 50 = 28.0 percent, as stated. Lessons: six lessons at data-hours 6 each = 36.")
fresh("proj-r17-blind-note-not-applicable", "(not used)", "(not used)", "PASS")  # placeholder removed below

# New rows of round 18.
fresh("proj-r18-mutant-r18_01", "ledgers/PC3/mutants/r18_01_replay_resimulates_the_game_from_the_seed.py; test_project.py test_replay_returns_the_fills_cash_flow_inventory_and_pnl",
      "New student-error mutant (round 18): replay re-plays the game from log['seed'] with its own quote and ignores the logged fills. Killed on seed 0 by test_replay_returns_the_fills_cash_flow_inventory_and_pnl[38] (out/mutate_pc3_0_49_final.out) and on seeds 0 and 77314143 by the same test (out/candidates_mutants_seed0_r18.out, out/candidates_seed77314143_r18.out).")
fresh("proj-r18-mutant-r18_02", "ledgers/PC3/mutants/r18_02_replay_books_informed_fills_as_purchases.py; test_project.py test_replay_agrees_with_the_engine_final_cash_and_inventory",
      "New student-error mutant: every informed fill booked as a purchase. Killed by test_replay_agrees_with_the_engine_final_cash_and_inventory[19] (seed 0) (out/mutate_pc3_0_49_final.out) and by test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0..2] on seeds 0 and 77314143 (out/candidates_mutants_seed0_r18.out, out/candidates_seed77314143_r18.out).")
fresh("proj-r18-mutant-r18_03", "ledgers/PC3/mutants/r18_03_replay_marks_the_change_from_the_start_value.py; test_project.py test_pnl_is_cash_flow_plus_inventory_times_settlement",
      "New student-error mutant: the mark is the inventory times (settlement - 10000). Killed by test_pnl_is_cash_flow_plus_inventory_times_settlement[29] (seed 0) (out/mutate_pc3_0_49_final.out) and by test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0..2] on seeds 0 and 77314143 (out/candidates_mutants_seed0_r18.out, out/candidates_seed77314143_r18.out).")
fresh("proj-r18-alternatives-new", "ledgers/PC3/scripts/PC3-c-r18/alt_r18_1_skew_and_size.py, alt_r18_2_mean_of_last_three_fills.py, alt_r18_3_never_quotes.py",
      "Three new correct implementations written in round 18: a skewed quote with size falling as |inventory| grows and a side-from-price replay (r18-1); a quote on the mean of the last three fills and a dataclass fold (r18-2); a policy that never quotes a size and an explicit-loop replay (r18-3). All exit 0 on seeds 0 and 77314143 (out/candidates_seed0.out, out/candidates_seed77314143.out).")
fresh("proj-r18-fill-side-by-price-equivalence", "course/modules/PC/PC3/grader/reference.py replay side rule; course/modules/PC/PC3/project.html line 397 and Conventions",
      "A replay that takes the side from price compared with the turn's mid (fill price above the mid is a sale) agrees with the ask/bid rule on every log whose fills are at the quoted bid or ask (r18-1 candidate passes). A replay that infers the side from the arrival name fails the new test (r17_02). The suite therefore separates the rules that the page states from the ones it does not.")

# ---- build rows ----
rows: list[dict[str, str]] = []
carried = 0
for old in prev["rows"]:
    rid = old["id"]
    if rid in DELEGATED:
        continue
    if rid in FRESH:
        status, location, evidence = FRESH[rid]
        if rid == "proj-r17-blind-note-not-applicable":
            continue
        rows.append({"id": rid, "check": old["check"], "location": location, "status": status, "evidence": evidence})
        continue
    if old["status"] != "PASS":
        raise SystemExit(f"row {rid} is {old['status']} and has no round-18 re-verification")
    carried += 1
    rows.append({
        "id": rid,
        "check": old["check"],
        "location": old["location"],
        "status": "PASS",
        "evidence": ("Carried from round 17 (" + old["location"][:220] + " byte-identical since the previous pin 700bf33f; "
                     "changed lines of that file are excluded from the cited subject): " + old["evidence"]
                     + " [round-17 line numbers; test_project.py lines from 389 on are +16 at 50559266; "
                       "L04.html lines from 128 on are +2]"),
    })

known_ids = {r["id"] for r in rows}
for rid, (status, location, evidence) in FRESH.items():
    if rid == "proj-r17-blind-note-not-applicable":
        continue
    if rid not in known_ids:
        rows.append({"id": rid, "check": "2.6-round18", "location": location, "status": status, "evidence": evidence})
        known_ids.add(rid)

for r in rows:
    if r["status"] != "PASS" and not r.get("fix"):
        r["fix"] = "see evidence"
assert len({r["id"] for r in rows}) == len(rows), "duplicate ids"

notes = [
    "Scope and blindness: slice c = project.html (excluding the exemplar passages, lines 632-694, which were neither read nor scored, per ruling 23), grader/ (engine, instance, reference, starter, test_project), the three project labs and their twins, the 92 mutants and the alternatives. The exemplar rows of the round-17 fragment (proj-exemplar-a-calibration, proj-exemplar-b-calibration, proj-exemplar-b-numbers, proj-exemplar-b-arrival-sensitivity, proj-exemplar-a-numbers, proj-exemplar-scores-blind-disclosure, proj-r17-blind-status, proj-exemplar-levels-vs-plan, proj-exemplar-levels-check-count, proj-exemplar-a-c5-annotation, proj-r15-exemplar-intro-fill-numbers, proj-r16-exemplar-annotation-vs-rubric, proj-exemplar-scores-in-served-html) are not in this fragment and are not carried: they are delegated to the dedicated blind scorer.",
    "Delta since round 17 (700bf33f..50559266, slice only): project.html lines 397 (counts and seed text), 450 (--assert paragraph) and 623 (C1 cells) changed; test_project.py gained one test at lines 386-400 (all other functions byte-identical); 13 mutant files added (fx17_01..10, r17_01..03); L04.html gained two lines at 127 (not in the round-17 subject except L04 line 482 -> 484); cards.json changed (not in this slice).",
    "Round-17 FAIL rows now PASS with fresh evidence: proj-local-commands, proj-r17-rubric-c1-levels, proj-r17-mutant-r17_02, proj-r16-mutants-76.",
    "Rows citing a test function were carried where the function is byte-identical; their line numbers in the carried evidence are round-17 numbers (+16 for test_project.py lines from 389 on).",
    "Observation, not a row: the page (line 393) says the browser does not save game_log.json and gives a local command; plans/PC3-build-plan.md section 5.2 (line 317) lists game_log.json as written by the page's runner. The deviation is documented on the page and the command works (proj-r17-spec-command), so it is noted for the architect rather than failed.",
    "Observation, not a row: a quote that writes module state it never reads changes no output, so no input distinguishes it (an equivalent mutant under VERIFIER_RULES 2.6). page line 397 states 'it keeps nothing between turns or games'; the suite checks outputs only. A test that snapshots the module dictionary before and after a game would check the stated property directly.",
    "check_pages --page project applies the lesson rules to the project page (11 false problems, out/check_pages_project.out). The whole-unit run is used as evidence (out/check_pages_unit.out, PASS). This is a tool limitation, not a page defect.",
    "Not checked here: the browser UI claims (workspace seed derivation, saving the code in the browser, 'graded instantly'); Pyodide timings beyond page_smoke; the rubric exemplars (blind scorer); the analysis rubric's scoring of a real submission.",
    "Mutation coverage: 92 of 92 listed mutants killed on seeds 0-49 (out/mutate_pc3_0_49_final.out). Each of my three new mutants is a complete module (quote and replay) and was checked for killing on seeds 0 and 77314143.",
    "Alternatives: 6 in ledgers/PC3/alternatives, 52 prior candidates, 3 new (alt_r18_1..3) and 5 round-16 modules: all 66 pass seeds 0 and 77314143.",
]

fragment = {
    "unit": "PC3",
    "slice": "c",
    "round": 18,
    "verifier": "independent verifier (Haiku 5.5), round 18, slice c; did not build PC3; exemplar scoring not performed (ruling 23)",
    "pin": "50559266",
    "base": "round 17 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round17.json (pin 700bf33f); delta 700bf33f..50559266 for this slice as in the notes",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE18-PC3-c (detached at 50559266; .venv symlinked; course/assets/vendor present)",
    "scratch": "ledgers/PC3/scripts/PC3-c-r18/ (gates_r18.sh, gates_extra_r18.sh, run_candidates_r18.sh, collect_counts_r18.sh, mypy_grader_r18.sh, sample_instances_r18.py, probe_*_r18.py, alt_r18_*.py, build_fragment_r18.py, out/)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "",
    "rows": rows,
    "mutants": killed,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": "",
}

problems = ledger.validate(fragment, "PC3-c")
passes = sum(1 for r in rows if r["status"] == "PASS")
fails = [r["id"] for r in rows if r["status"] != "PASS"]
fragment["verdict"] = "PASS" if not fails and not problems else "FAIL"
fragment["summary"] = (f"PC3-c round 18: verdict {fragment['verdict']}. Rows {len(rows)}: PASS {passes}, "
                       f"non-PASS {len(fails)}. Mutants {len(killed)}/{len(killed)} killed on seeds 0-49. "
                       f"Carried rows: {carried}. Delegated exemplar rows: {len([o for o in prev['rows'] if o['id'] in DELEGATED])}.")
out = ROOT / "ledgers/PC3/PC3-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", passes, "nonpass", fails, "carried", carried, "problems", problems)
print("verdict", fragment["verdict"])
