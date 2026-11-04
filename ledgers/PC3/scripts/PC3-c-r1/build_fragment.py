"""Write the PC3 slice-c verifier fragment for round 1 (ledgers/PC3/PC3-c.json).

The fragment is generated from this file so that every row's evidence is plain text with no escaping errors. The
rows record only what the scripts in this directory and the commands listed in each evidence string produced.
Run from the checkout root: .venv/bin/python ledgers/PC3/scripts/PC3-c-r1/build_fragment.py
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers/PC3/PC3-c.json"
S = "ledgers/PC3/scripts/PC3-c-r1"
PROJ = "course/modules/PC/PC3/project.html"
GRADER = "course/modules/PC/PC3/grader/test_project.py"

PASS = "PASS"
FAIL = "FAIL"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> dict[str, str]:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        item["fix"] = fix
    return item


ROWS = [
    row(
        "proj-lab1-run", "2.5-labs", f"{PROJ} lab-PC3-project-1 (rung 1)", PASS,
        "run_labs: `.venv/bin/python tools/run_labs.py --unit PC3 --page project` printed PASS (3/3). Twin run as "
        "`python -I -W error tests/labs/PC3/lab-PC3-project-1.py` exited 0 with empty stderr, and its stdout equals the "
        "page's expected block line for line (run_labs compare).",
    ),
    row(
        "proj-lab1-hypothesis-numbers", "2.2-numbers", f"{PROJ} Lab 1 hypothesis", PASS,
        f"{S}/recompute_project_numbers.py check1 (independent game code): seed 0 has 9 fills, cash flow -9950, "
        "inventory 1, settlement 9980, mark 9980, P&L 30, largest |inventory| 3 (limit 10). Every value in the hypothesis "
        "matches.",
    ),
    row(
        "proj-lab2-completion", "2.5-labs", f"{PROJ} lab-PC3-project-2 (rung 2, completion)", PASS,
        "run_labs --page project: the completion rule passes (every page line equals the twin line except the two "
        "`___` lines, which are `cash_flow = ___` and `mark = ___`). The twin prints cash_flow_cents -9950, "
        "inventory_end 1, inventory_mark_cents 9980, pnl_cents 30, identity True, equal to the page's expected block.",
    ),
    row(
        "proj-lab2-interpretation-last-quote", "2.2-numbers", f"{PROJ} Lab 2 interpretation", PASS,
        f"{S}/recompute_project_numbers.py check2: the turn-20 quote is (9980, 10000), mid 9990. Marking the ending "
        "inventory (1 unit) at that mid gives P&L 40, against 30 at the settlement value, so the sentence 'a mark at the "
        "last quote would give a different P&L on this seed' is true.",
    ),
    row(
        "proj-lab3-counterfactual", "2.2-numbers", f"{PROJ} lab-PC3-project-3 hypothesis and expected block", PASS,
        f"run_labs --page project PASS; recompute check1: half-spread 15 gives 9 fills and P&L 55, change +25 cents. "
        "The hypothesis, the expected block and the independent recomputation agree.",
    ),
    row(
        "proj-lab3-interpretation", "2.2-numbers", f"{PROJ} Lab 3 interpretation", PASS,
        "The lab plays one seed (SEED = 0 in tests/labs/PC3/lab-PC3-project-3.py, lines 'SEED = 0') and prints one "
        "counterfactual. The interpretation's statement that it is 'not an estimate ... on other seeds' matches the "
        "code, which tests no other seed.",
    ),
    row(
        "proj-rung1-instance-claim", "2.8-data / 2.6-spec", f"{PROJ} line 53 and grader/instance.py docstring", PASS,
        f"{S}/recompute_project_numbers.py check3: make_instance(seed) equals the lab's draw order (move draw, then arrival "
        "draw, thresholds 0.5 / 0.25 / 0.5) for seeds 0..49, with 0 mismatches. tests/labs/PC3/lab-PC3-L04-1.py lines "
        "58-70 use the same draw order, so the instance.py claim that the seed-0 instance is the Lesson 4 game on seed 0 "
        "holds.",
    ),
    row(
        "proj-conventions-constants", "2.2-numbers", f"{PROJ} 'Conventions' list", PASS,
        "N = 20, v_0 = 10000 cents, moves of +5 or -5 with probability 1/2, arrival probabilities 1/4, 1/4, 1/2, "
        "|I| <= 10 and 0 <= q <= 5 all match engine.py (MAX_SIZE = 5, LIMIT = 10, lines 29-30, 77-81) and instance.py "
        "(START_CENTS, MOVE_CENTS, thresholds, lines 21-45).",
    ),
    row(
        "proj-exemplar-a-calibration", "2.6-rubric", f"{PROJ} Exemplar A (#exemplar-a, data-scores 2,2,1,2,1)", PASS,
        "Blind scoring by the verifier from the rubric table only: C1 2 (P&L and cash flow stated, no mark), C2 2 (two "
        "turns with values), C3 1 (no amount in cents), C4 2 (parameters named, no effect stated), C5 1 ('I checked it'). "
        "The verifier's scores equal the official 2,2,1,2,1 exactly.",
    ),
    row(
        "proj-exemplar-b-calibration", "2.6-rubric", f"{PROJ} Exemplar B (#exemplar-b, data-scores 4,4,4,3,4)", PASS,
        "Blind scoring: C1 4 (cash flow, mark and P&L with turns), C2 4 (turns 2, 5, 18 with values that match the log; "
        "field names are paraphrased, e.g. 'the bid', 'inventory 2 after it', which the verifier accepts), C3 4 (5 cents, "
        "rerun of seed 0, +25), C4 3 (settlement rule not named), C5 4 (identity and cash check with values). The verifier's "
        "scores equal the official 4,4,4,3,4 exactly.",
    ),
    row(
        "proj-exemplar-b-numbers", "2.2-numbers", f"{PROJ} Exemplar B 'P&L decomposition' and 'Counterfactual'", PASS,
        f"{S}/recompute_project_numbers.py check4 and check5: maker purchases at the bid 9990, 9980, 9970, 9980, 9990 sum "
        "to 49910; sales at the ask 9980, 9990, 9990, 10000 sum to 39960; cash flow -9950; fill turns 2, 3, 4, 5, 7, 8, 13, "
        "18, 19; the turn-5 ask is 9980 and the turn-2 bid is 9990. Counterfactual +25 (check1).",
    ),
    row(
        "proj-exemplar-a-numbers", "2.2-numbers", f"{PROJ} Exemplar A 'Evidence from the log'", PASS,
        f"{S}/recompute_project_numbers.py check5: turn 5 is a sale at the ask 9980 and turn 18 a sale at 10000 (fill "
        "turns list and quotes). The two cited values match the log.",
    ),
    row(
        "proj-rubric-observable", "2.6-rubric", f"{PROJ} rubric table (#rubric)", PASS,
        "Each of the 20 descriptors was read against the others. Levels are separated by counts (three values, three "
        "turns, one or two turns), by the presence of a printed or computed value, and by the presence of an amount in "
        "cents. No descriptor depends on an unobservable judgement. The C5 level 3 phrase 'without a value' is "
        "distinguished from level 4 'gives its printed or computed result' by whether a value appears.",
    ),
    row(
        "proj-spec-log-schema", "2.6-spec (completeness)", f"{PROJ} 'Rung 3 · Specification', Required outputs and Inputs",
        FAIL,
        "A competent student would have to ask: what keys does a log have, and what keys does a turn record have? The "
        "page's Required outputs names only the state key 'history' ('the earlier turn records of the log'). The log keys "
        "(seed, settlement_cents, turns) and the turn-record keys (turn, bid_cents, ask_cents, size, arrival, filled, "
        "fill_price_cents, inventory_after, cash_after_cents) appear only in the Lab 1 code and in grader/engine.py's "
        "docstring. Also, the 'Grading mode' paragraph says the analysis 'is graded by rubric', while the same paragraph "
        "says the student scores it; the page does not say who issues the rubric grade or where analysis.md is submitted.",
        "Add a Log paragraph to Required outputs listing the log keys and the turn-record keys, saying that fill_price_cents "
        "is None when filled is false, and that a fill at the bid is a maker purchase and a fill at the ask a maker sale. "
        "Say who issues the rubric grade for analysis.md and where it is submitted.",
    ),
    row(
        "proj-hours-arithmetic", "2.6-hours", f"{PROJ} 'Time budget' table (#hours); course/modules/PC/PC3/index.html "
        "data-hours-lessons=36, data-hours-project=14", PASS,
        "The table sums to 1+1+3+2+2+4+1 = 14. 14 of 50 is 28.0 percent, which matches the hub's total of 36 + 14 = 50 and "
        "the page's 'Equals the project hours in the hub'. Verifier estimate of the deliverable: rung 1-2 about 2 h, quote "
        "and replay 4-6 h, autograder runs 1-2 h, analysis 3-5 h, self-assessment about 1 h, total 11-16 h, inside 30 percent "
        "of 14.",
    ),
    row(
        "proj-hub-placement-conflict", "2.9-prose (cross-page)", f"{PROJ} line 42 vs course/modules/PC/PC3/index.html lines 74 and 156",
        FAIL,
        "project.html line 42: 'If you met the placement bar on the module page, skip rungs 1 and 2 and start at rung 3.' "
        "index.html line 74: 'To skip rungs 1 and 2, you must reach the bar and answer both skill checks.' index.html line "
        "156: 'To skip them, a student must reach the placement bar and answer both skill checks.' The two pages give "
        "different rules for skipping rungs 1 and 2.",
        "Change project.html line 42 to 'If you reached the placement bar and answered both skill checks on the module page, "
        "skip rungs 1 and 2 and start at rung 3.' (the hub's rule, which the curriculum plan adopts).",
    ),
    row(
        "proj-grader-35-checks", "2.6-autograder", f"{PROJ} 'Grading mode' ('runs 35 checks')", PASS,
        f"`pytest --collect-only -q test_project.py` in a scratch copy of the grader reports '35 tests collected'. "
        "QF_SEED=0 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py gives 35 passed.",
    ),
    row(
        "proj-grader-seed-scope-claim", "2.6-autograder / 2.9-prose", f"{PROJ} 'Grading mode' and 'Constraints' "
        f"(Integrity sentence); {GRADER} lines 9-10", FAIL,
        "The page says the checks that use a game run on the student's seed and on seed+7919, and that 'integrity rests on "
        "... the second instance of every test'. Only 8 tests are parametrized over SEEDS (decorators at test_project.py "
        "lines 139, 222, 239, 256, 272, 279, 309, 323), so 16 of 35 tests run on two seeds. The named-refusal tests run on "
        "SEED only (lines 168, 173, 178, 184, 189, 194, 204, 212), and the hand-built-log and custom-instance tests (lines "
        "296, 351, 365, 380) run on SEED only. 'The second instance of every test' is false, and 'the named refusals' are "
        "not checked on the second instance.",
        "Replace 'the second instance of every test' with the list of the 16 two-seed tests, and move 'the named refusals' "
        "out of the two-seed list, or parametrize the refusal tests over SEEDS and correct the Grading mode sentence.",
    ),
    row(
        "proj-grader-no-print", "2.6-autograder (stated constraint)", f"{PROJ} 'Constraints' ('No function prints or "
        "warns.'); course/modules/PC/PC3/grader/starter.py line 8-9", FAIL,
        "Mutant v08 (a print() left in replay) passes all 35 tests on seed 0 and is reported SURVIVED by "
        "tools/mutate_graders.py --unit PC3 --seeds 0-49. The page states the constraint, and no test checks stdout. "
        "Probe (ledgers/PC3/scripts/PC3-c-r1/probe_stale_totals.py pattern, plus a capsys test): a test that calls "
        "replay(fixed_log(SEED)) and asserts that stdout is empty FAILS v08 and PASSES the reference (the reference has no "
        "print, see grep of reference.py and engine.py).",
        "Add to test_project.py: def test_replay_and_quote_print_nothing(capsys: pytest.CaptureFixture[str]) -> None: "
        "sol.replay(fixed_log(SEED)); expect(capsys.readouterr().out == '', 'no function may print'). (Warnings are already "
        "failures through -W error.)",
    ),
    row(
        "proj-grader-replay-from-fills", "2.6-autograder (stated behaviour)", f"{PROJ} Conventions 'The P&L' bullet ('the cash "
        f"flow the sum of the fill cash flows'); Lab 1 step 4; {GRADER} lines 240-253", FAIL,
        "Mutant v04 (replay copies the last turn's cash_after_cents and inventory_after instead of summing the fills) passes "
        "all 50 seeds (mutate_graders SURVIVED). The stated rule is that the cash flow is the sum of the fill cash flows, and "
        "that the replay computes from the fills. On engine logs the running totals equal the fill sums, so no current test "
        "tells them apart. Probe: scripts/PC3-c-r1/probe_stale_totals.py appends a test with one sale at 10010 and stale "
        "running totals (cash 0, inventory 0) to a copy of the suite: the reference PASSES and v04 FAILS. The builder's "
        "alternative 3 uses the same replay (see proj-alt3-replay).",
        "Add to test_project.py: a hand-built log with one fill at 10_010 (uninformed-buy, so the maker sells) and turns 2 to "
        "20 with cash_after_cents 0 and inventory_after 0; expect(sol.replay(log) == oracle(log), 'the cash flow must be the "
        "sum of the fill cash flows, and the inventory the sum of the fills'). The probe in scripts/PC3-c-r1 is the test.",
    ),
    row(
        "proj-grader-mypy-strict", "2.6-typing (BUILDER_RULES 'type-checked by mypy strict like all other code')",
        f"{GRADER} lines 65, 133, 147, 157, 160, 161, 162", FAIL,
        "mypy --no-incremental --strict --ignore-missing-imports --explicit-package-bases run in the grader directory: "
        "reference.py, instance.py, starter.py and engine.py pass ('Success: no issues found in 4 source files'). "
        "test_project.py has 6 errors: line 65 and 133 (no-any-return from engine.play), line 147 (no-any-return from sol.quote), "
        "lines 157, 160, 161 and 162 (quotes is list[object], so tuple unpacking and the bid, ask and size types are not known).",
        "Wrap engine.play results in cast(dict[str, Any], ...), type sol.quote results with cast(tuple[int, int, int], ...), "
        "and type the quotes list as list[tuple[int, int, int]] after the isinstance check.",
    ),
    row(
        "proj-grader-reference", "2.6-autograder item 1", "course/modules/PC/PC3/grader/reference.py", PASS,
        "tools/run_graders.py --unit PC3 --seeds 0-49: 'run_graders PC3: PASS (reference 50/50 seeds, slowest 0.1 s)'. "
        "page_smoke in-browser run (Pyodide) of the reference: 'All 35 tests pass on seed 1136679017'.",
    ),
    row(
        "proj-grader-starter-fails", "2.6-autograder", "course/modules/PC/PC3/grader/starter.py", PASS,
        "run_graders PC3 checked that the starter fails the suite (no 'the starter passes the suite' problem was printed).",
    ),
    row(
        "proj-grader-instances", "2.6-autograder item 2", "course/modules/PC/PC3/grader/instance.py", PASS,
        "run_graders check_instances: make_instance is deterministic and the seeds 0..49 are not identical. Instances are "
        "valid (test_instance_is_deterministic_and_well_formed passes on seeds 0 and 7919). Materiality: "
        f"{S}/recompute_project_numbers.py check6: the reference P&L over seeds 0..19 takes 8 distinct values, so the answers "
        "change, not only the labels.",
    ),
    row(
        "proj-grader-messages", "2.6-autograder item 4", f"{GRADER} lines 40-55, 150-162, 229-235, 268, 288-292", PASS,
        "The failure messages name the property ('a quoted size must lie in 0..5', 'the cash flow must be the sum of the "
        "fill cash flows') and contain no computed value. expect() and must_refuse() set __tracebackhide__ = True. "
        "pytest runs with --assert=plain, so no comparison values are printed.",
    ),
    row(
        "proj-named-refusals", "2.6-autograder (exception types)", f"{GRADER} lines 168-216", PASS,
        "Each named condition has an isolated test: crossed quote (168, 'bid must be below ask'), bid above ask (173), "
        "size 6 (184), size -1 (189), log of 19 and 21 turns (204, 'a log has exactly 20 turns'), filled turn without a "
        "price (212, 'a filled turn needs a fill price'). must_refuse() is used only for these four named conditions. "
        "The seed-scope gap in proj-grader-seed-scope-claim is separate.",
    ),
    row(
        "proj-builder-mutants", "2.6-autograder item 3 (builder mutants m01-m10)", "ledgers/PC3/mutants/m01..m10", PASS,
        "tools/mutate_graders.py --unit PC3 --seeds 0-49: 10 of 10 builder mutants KILLED. Killing tests are listed in the "
        "mutants array.",
    ),
    row(
        "proj-verifier-mutants", "2.6-autograder item 3 (verifier mutants v01-v08)", "ledgers/PC3/mutants/v01..v08", FAIL,
        "Eight mutants written by the verifier (scripts/PC3-c-r1/make_verifier_mutants.py). v01, v02, v03, v05, v06 and v07 "
        "are KILLED. v04 (running totals) and v08 (print in replay) SURVIVE all 50 seeds. Each survivor violates a stated "
        "rule (see proj-grader-replay-from-fills and proj-grader-no-print).",
        "Add the two tests in proj-grader-replay-from-fills and proj-grader-no-print. Re-run mutate_graders: v04 and v08 "
        "must then be KILLED.",
    ),
    row(
        "proj-mutant-m08-description", "2.6-autograder item 3 (mutant description)",
        "ledgers/PC3/mutants/m08_hard_coded_answer_for_any_log.py", FAIL,
        "The first docstring line says 'a hard-coded answer, the one for seed 0, is returned for every log'. The mutant "
        "(diff against reference.py, line 34) returns all zeros, {cash_flow_cents: 0, inventory_end: 0, "
        "inventory_mark_cents: 0, pnl_cents: 0}, which is not the seed-0 answer. The kill is valid; the description is not.",
        "Change the docstring's first line to 'Student error: replay returns all zeros, a hard-coded answer, for every log.'",
    ),
    row(
        "proj-alternatives-1-2-4-5", "2.6-autograder item 1 (alternatives)",
        "ledgers/PC3/alternatives/alt1, alt2, alt4, alt5", PASS,
        f"{S}/run_candidates.py --seeds 0-49: alt1 (class Maker), alt2 (closures and fold), alt4 (size scaled by inventory) "
        "and alt5 (threshold quoting with a dataclass) each PASS 50/50 seeds. Note: alt5's threshold never fires, because "
        "its half-spread is 5 cents, so ask - bid = 10 on every turn and size is always 1. It does not exercise size 0.",
    ),
    row(
        "proj-alt3-replay", "2.6-autograder item 1 (alternative 3)", "ledgers/PC3/alternatives/alt3_inventory_skew.py "
        "(replay)", FAIL,
        "alt3 passes 50/50 seeds, but its replay returns the last turn's cash_after_cents and inventory_after, not the sum of "
        "the fills. That is not a correct implementation under the stated rule (see proj-grader-replay-from-fills). The "
        "suite accepts it because nothing tests the fill sum on a log whose running totals are stale.",
        "Fixed by the test in proj-grader-replay-from-fills. After it is added, alt3 must FAIL (its replay will return the "
        "stale totals), or its replay must be changed to sum the fills.",
    ),
    row(
        "proj-alternative-6", "2.6-autograder item 1 (verifier alternative)",
        f"{S}/alt6_size_zero_on_multiples_of_three.py", PASS,
        f"{S}/run_candidates.py --seeds 0-49: PASS 50/50. This legal policy quotes size 0 on every third turn and replays "
        "with zip over the fills, so the size-0 branch and a different replay both pass.",
    ),
    row(
        "proj-lint-ruff", "2.5 / 2.9 gates", "tests/labs/PC3, course/modules/PC/PC3/grader", PASS,
        "ruff check tests/labs/PC3 course/modules/PC/PC3/grader: 'All checks passed!'. ruff format --check on the same paths: "
        "'14 files already formatted'.",
    ),
    row(
        "proj-mypy-labs", "2.5-labs (typing)", "tests/labs/PC3/lab-PC3-project-1..3.py", PASS,
        "mypy --no-incremental --strict tests/labs/PC3: 'Success: no issues found in 4 source files' (the three project "
        "labs and the other PC3 twins in that directory).",
    ),
    row(
        "proj-page-smoke", "2.9-structure / 2.5-labs", f"{PROJ} (page_smoke)", PASS,
        "tools/page_smoke.py --unit PC3 --pages project (run alone): 'page_smoke modules/PC/PC3/project.html: PASS'. Lab "
        "times 0.0 s each; in-browser grader 'All 35 tests pass on seed 1136679017 (0.7 s)'. Zero console errors and "
        "no external requests were reported.",
    ),
    row(
        "proj-check-tools", "2.6 / 2.9 gates", "tools/check_projects.py, check_pages.py, check_dag.py --unit PC3", PASS,
        "check_projects PC3: PASS. check_pages PC3: PASS. check_dag PC3: PASS. (These are unit-wide runs; the project page's "
        "concept links resolve to defined concepts.)",
    ),
    row(
        "proj-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3", PASS,
        "run_labs PC3: PASS (9/9). This includes the three project labs and the six lesson labs, which are outside this "
        "slice but run with the same command.",
    ),
    row(
        "proj-banned-and-process-words", "2.9-prose", f"{PROJ} (all text)", PASS,
        "grep -i of every BANNED string in tools/check_pages.py (TODO, TBD, lorem, 'for brevity', 'details omitted', "
        "'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', "
        "'experts agree', 'it is well known', 'obviously', 'clearly', and three-dot ellipses) found no hit. grep -w for "
        "build, builder, round, verifier, REQUESTS and 'unit report' found no learner-text hit. The 'around' matches are "
        "not the word 'round'.",
    ),
    row(
        "proj-notation", "2.4-notation", "notation/notation.json and "
        f"{PROJ}", PASS,
        "The registered symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) do not occur in "
        "project.html. N is a local symbol (Conventions: 'There are N = 20 turns'), which notation.json's about text "
        "allows. t, v, b, a, q, I are local and defined in the Conventions list before use.",
    ),
    row(
        "proj-dag-terms", "2.9-DAG / plan section 4", f"{PROJ} (all text)", PASS,
        "grep -i for martingale, Bayes, Kelly, Poisson, Markov, duration, beta, CAPM, DCF, binomial, permutation and "
        "combination finds no hit. 'adverse selection' appears in the rubric (C4) and in the exemplars as plain prose, "
        "with no link and no definition, which is the plan's D3 resolution.",
    ),
    row(
        "proj-references", "2.1-citations", f"{PROJ} 'Reading' (reading-list, data-cite zhou2008practical, crack2015heard)",
        PASS,
        "The page cites only the two registry keys, at book level, with no page, problem, answer or edition. "
        "tools/verify_refs.py --offline: '560 entries, 0 problems'. NOT CHECKED: the live Crossref run for these two keys "
        "(the --unit form of verify_refs needs the network and was not run). This row covers the attribution scope only.",
    ),
    row(
        "proj-js-claims", "2.6-autograder (browser behaviour)", f"{PROJ} Inputs and the grader section",
        PASS,
        "The seed is derived from the workspace: course/assets/js/grader.js line 33 (store.unitSeed) and line 53 ('derived "
        "from your workspace ID'); store.js line 134 (FNV-1a). Code is saved as you type: grader.js lines 59-61 "
        "(debounced store.put, 400 ms). The grader runs the suite with env QF_SEED (grader.js line 95). Scores stay in the "
        "browser: rubric.js store.put (kv). These were read, not exercised by hand.",
    ),
    row(
        "proj-local-commands", "2.6-autograder (student workflow)", f"{PROJ} 'Required outputs' game-log command and "
        "'Running the suite locally'", PASS,
        "Ran the page's game-log command in a scratch directory with engine.py, instance.py and the reference as "
        "market_maker.py: exit 0, 20 turns, settlement 9980, seed 0. Ran the page's local pytest command with QF_SEED=0: "
        "35 passed.",
    ),
    row(
        "proj-known-limitation", "2.6-autograder (stated limitation)", f"{PROJ} 'Constraints' ('Known limitation')",
        PASS,
        "course/modules/PC/PC3/grader/engine.py docstring line 19: 'The engine does not show the fair value to the policy. "
        "The log does show the settlement value, after the last turn.' The turn records carry no fair path (see the "
        "turn-record keys in engine.py lines 89-98). The limitation sentence is accurate. Its 'second instance of every "
        "test' clause is the subject of proj-grader-seed-scope-claim.",
    ),
    row(
        "proj-ladder-scope", "2.6-projects (ladder and scope)", f"{PROJ} 'The ladder'; curriculum/06-profession-capstone.yaml:175-182",
        PASS,
        "Rung 1 is a full-length worked example (Lab 1), rung 2 a graded completion (Lab 2), rung 3 an independent project "
        "graded by both modes, rung 4 open-ended (stretch). The brief (in-page market-making game against scripted "
        "counterparties with hidden information, post-game analysis of edge and inventory risk) matches rung 3. Playing by "
        "code instead of by clicking is the architect's ruling (plan B1).",
    ),
    row(
        "proj-rubric-atlas-studios", "2.6-atlas / 2.6-studios", "plans/PC3-build-plan.md section 8", PASS,
        "No Atlas milestone and no studio is named for PC3 (plan section 8; check_projects PASS). No contract is required.",
    ),
    row(
        "proj-stretch", "2.6-projects (rung 4)", f"{PROJ} 'Rung 4 · Stretch'", PASS,
        "The informed-share stretch (0.6, uninformed split evenly) and the limit stretch (5 units) state no numbers, so no "
        "computation is claimed. The stretch is consistent with the engine's rules.",
    ),
    row(
        "proj-twin-rules", "2.5-labs (twin rules)", "tests/labs/PC3/lab-PC3-project-1..3.py", PASS,
        "Standard library only (__future__, random, typing). random.Random(seed) for every draw. Each twin ends with an "
        "unconditional main() call (line 154 of project-1, 127 of project-2, 138 of project-3), no __name__ guard. Each runs under -I -W error "
        "with empty stderr.",
    ),
    row(
        "proj-exception-types", "2.6-autograder (exception rule)", f"{GRADER} lines 47-55, 168-216",
        PASS,
        "must_refuse() appears only for the four named invalid inputs. The other tests expect no exception, and the "
        "engine's bid-must-be-below-ask message contains the named phrase ('turn N: bid must be below ask').",
    ),
]


MUTANTS = [
    {"id": "m01_pnl_omits_inventory_mark", "description": "Student error: the P&L is cash only, with the inventory mark omitted.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
    {"id": "m02_sell_cash_sign_flipped", "description": "Student error: the cash flow of a fill has the wrong sign on every side.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
    {"id": "m03_unfilled_orders_counted", "description": "Student error: the filled flag is ignored, so unfilled turns are replayed as fills.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
    {"id": "m04_mark_uses_last_quote_mid", "description": "Student error: the inventory is marked at the last quoted mid, not at the settlement value.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
    {"id": "m05_settlement_rounded_to_dime", "description": "Student error: the settlement is rounded to the nearest dime before it marks the inventory.", "killed_by": "test_inventory_is_marked_at_the_settlement_value_not_the_quote_mid (seed 0)"},
    {"id": "m06_last_turn_omitted", "description": "Student error: the replay loop stops one turn early and omits the last turn.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
    {"id": "m07_sell_adds_to_inventory", "description": "Student error: a sale adds to inventory instead of reducing it (sign of the inventory update flipped).", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
    {"id": "m08_hard_coded_answer_for_any_log", "description": "Student error: returns all zeros (a hard-coded answer) for every log; the first docstring line wrongly says it is the seed-0 answer.", "killed_by": "test_filled_turn_without_a_price_is_refused (seed 0)"},
    {"id": "m09_quoted_size_above_maximum", "description": "Student error: the quote posts size 6, above the largest quoted size of 5.", "killed_by": "test_quotes_are_legal_on_every_turn[0] (seed 0)"},
    {"id": "m10_crossed_quote_on_turn_one", "description": "Student error: on turn 1 the quote is locked (bid equal to ask), so the engine refuses it.", "killed_by": "test_quotes_are_legal_on_every_turn[0] (seed 0)"},
    {"id": "v01_quote_swaps_bid_and_ask_after_a_fill", "description": "Student error: after the first fill the bid and the ask are swapped, so every later quote is crossed.", "killed_by": "test_quotes_are_legal_on_every_turn[0] (seed 0)"},
    {"id": "v02_quote_size_by_true_division", "description": "Student error: the quoted size uses true division, so it is the float 1.0 and not the integer 1.", "killed_by": "test_quotes_are_legal_on_every_turn[0] (seed 0)"},
    {"id": "v03_replay_marks_at_last_fill_price", "description": "Student error: the inventory is marked at the price of the last fill, not at the settlement value.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
    {"id": "v04_replay_copies_last_running_totals", "description": "Student error: replay copies the last turn's running cash and inventory instead of summing the fills.", "killed_by": None},
    {"id": "v05_replay_side_from_arrival_name", "description": "Student error: replay takes the side of each fill from the arrival name, so an informed sale is booked as a buy.", "killed_by": "test_replay_returns_the_fills_cash_flow_inventory_and_pnl[0] (seed 0)"},
    {"id": "v06_replay_mark_by_true_division", "description": "Student error: the inventory mark uses true division, so it is a float and not an integer number of cents.", "killed_by": "test_money_and_units_are_integers[0] (seed 0)"},
    {"id": "v07_replay_int_of_none_not_refused", "description": "Student error: a filled turn with no fill price crashes with a TypeError instead of the named ValueError.", "killed_by": "test_filled_turn_without_a_price_is_refused (seed 0)"},
    {"id": "v08_replay_leaves_a_debug_print", "description": "Student error: a debugging print is left in replay, so the function prints while it runs.", "killed_by": None},
]

NOTES = (
    "Scope: project.html, grader/ (engine, instance, reference, starter, test_project), the three project labs, the "
    "builder mutants m01-m10, the builder alternatives alt1-alt5, and the verifier's own alternative alt6 and mutants "
    "v01-v08. Every number was recomputed by scripts in ledgers/PC3/scripts/PC3-c-r1/. Commands run and their output are "
    "in the rows. Mutation totals: 16 of 18 killed on seeds 0-49 (v04 and v08 survive). Alternatives: 5 of 5 builder "
    "alternatives and alt6 pass on seeds 0-49, but alt3's replay is not a correct implementation under the stated rule. "
    "NOT CHECKED: (1) the live Crossref resolution for the two reading-list keys (verify_refs --unit needs the network); "
    "(2) full-repository gates (whole-repo ruff, whole-repo mypy, full pytest, build_site, render_curriculum), which are "
    "outside this slice; (3) the rubric and self-assessment UI by hand in a browser (page_smoke covers the page's "
    "structure and the in-browser grader only); (4) the hub, lessons and cards, which are other slices, except for the "
    "placement-rule cross-check in proj-hub-placement-conflict; (5) ledger.py was not run, so no merged "
    "ledgers/PC3.verification.json was written (that is the orchestrator's merge). The verifier wrote no edits under "
    "course/, tests/, tools/ or references/."
)

SUMMARY = ""  # filled in main() from the row counts and the mutant kills


def main() -> None:
    fragment = {
        "unit": "PC3",
        "slice": "c",
        "round": 1,
        "verifier": "independent verifier (Haiku 5.5), round 1, slice c",
        "pin": "1c1645f3b00eada2fb54d39c86d5d949e15b4fbc",
        "base": "none (first independent verification of this slice)",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyE1-PC3-c",
        "scratch": "/tmp/pc3c-* (scratch copies only; nothing in them is cited as evidence without its script)",
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "verdict": "FAIL" if any(r["status"] != PASS for r in ROWS) else "PASS",
        "rows": ROWS,
        "mutants": MUTANTS,
        "registry_flags": [],
        "freshness_flags": [],
        "notes": NOTES,
        "summary": "",
    }
    killed = sum(1 for m in MUTANTS if m["killed_by"])
    fragment["summary"] = (
        f"Slice c (round 1): verdict {fragment['verdict']}. Rows {len(ROWS)}: PASS "
        f"{sum(r['status'] == PASS for r in ROWS)}, FAIL {sum(r['status'] != PASS for r in ROWS)}, UNVERIFIABLE 0. "
        f"Mutants killed {killed} of {len(MUTANTS)} (survivors: v04, v08)."
    )
    OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = {s: sum(1 for r in ROWS if r["status"] == s) for s in (PASS, FAIL)}
    print(f"wrote {OUT.relative_to(ROOT)}: rows={len(ROWS)} {counts}")


if __name__ == "__main__":
    main()
