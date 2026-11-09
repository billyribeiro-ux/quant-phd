"""Round 17, PC3 slice c: build ledgers/PC3/PC3-c.json from the round-16 rows, the round-17 re-verification and the mutate output."""
import json
import re
from datetime import UTC, datetime

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE17-PC3-c"
OUT = f"{ROOT}/ledgers/PC3/PC3-c.json"
S = "ledgers/PC3/scripts/PC3-c-r17/out"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-PC3-c.round16.json", encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

CARRY_NOTE = ("Carried from round 16 (the cited subject is byte-identical between pins 56cc575a and 700bf33f; the only "
              "changed lines in this slice are project.html line 450 and test_project.py lines 9-13, out/delta_r17.txt): ")

# Rows re-verified in round 17 (new evidence). value = (status, location, evidence)
RE = {
 "proj-zero-fill-replay": ("PASS", "course/modules/PC/PC3/grader/test_project.py test_a_log_with_no_fill_replays_to_zero lines 386-394 (round-16 cited 315-323, stale); project.html line 393 and 407",
   "Read in full this round. The test builds a no-fill log (turn_record filled=False on turns 1-20) and requires replay to return zero for all four keys, which the stated definitions (project.html 393, 407) give. reference.py passes on seed 0 (487 passed; out/alternatives_seed0_r17.txt)."),
 "proj-grader-35-checks": ("PASS", "course/modules/PC/PC3/project.html line 397 (487 / 496); course/modules/PC/PC3/grader/test_project.py",
   "collect-only (out/collect_counts_r17.txt): seeds 0, 25, 49 -> 487; seeds 50, 7919, 77314143 -> 496. Count by decomposition: 9 seed-parametrised functions x 51 seeds (seed 0) or 52 (other) + 25 seed-only items + 3 seed-free checks (test_fixed_seeds_0_to_49_give_fifty_different_paths, test_a_direct_call_on_a_hand_built_state_ignores_an_earlier_game, test_a_direct_quote_is_legal_at_every_inventory_within_the_limit). Page's 9 x 51 + 25 + 3 = 487 and 9 x 52 + 25 + 3 = 496 match."),
 "proj-grader-seed-scope-claim": ("PASS", "course/modules/PC/PC3/project.html line 397 against grader/test_project.py lines 36-38 (SEED, FIXED_SEEDS, SEEDS)",
   "test_project.py line 38 builds SEEDS = dict.fromkeys(FIXED_SEEDS, SEED, SEED+7919): 50 fixed seeds, plus the learner's seed and seed+7919; collect-only gives 51 seeds of nine checks for seed 0 (487) and 52 otherwise (496), out/collect_counts_r17.txt."),
 "proj-r15-grading-counts": ("PASS", "course/modules/PC/PC3/project.html line 397; grader/test_project.py (collect-only)",
   "Re-run this round: out/collect_counts_r17.txt (487 for seeds 0-49 samples; 496 for 50, 7919, 77314143). Seed-only items: 25 (19 seed-only functions with 4 parametrised into 10 items); seed-free: 3."),
 "proj-r8-collect-counts": ("PASS", "course/modules/PC/PC3/grader/test_project.py; collect-only counts",
   "pytest --collect-only with QF_SEED in {0, 25, 49, 50, 7919, 77314143}: 487, 487, 487, 496, 496, 496 (out/collect_counts_r17.txt)."),
 "proj-grader-no-print": ("PASS", "course/modules/PC/PC3/grader/test_project.py test_no_function_prints_or_warns lines 462-502 and its docstring lines 465-468 (round-16 cited 434-466, stale)",
   "Read this round. The test captures stdout/stderr (capsys), logging (caplog at DEBUG) and warnings (catch_warnings, simplefilter always) across the game, the no-fill, zero-fill, -10 and +10 logs and all direct states, and the docstring names exactly those channels. Mutants m03, s14_01, v08, v09, v24, v26, v47, v48, v49 are killed by it (out/mutate_pc3_79_0_49_r17.out)."),
 "proj-grader-determinism-quote-state": ("PASS", "course/modules/PC/PC3/grader/test_project.py test_the_quote_depends_only_on_the_state_it_is_given lines 505-520 (round-16 cited 411-426, stale)",
   "Read this round: importlib.reload(sol) before each of the two games; the assertion compares the two logs with ==. Mutant v46 and r13_05 are killed by it (out/mutate_pc3_79_0_49_r17.out)."),
 "proj-direct-call-test-docstring": ("PASS", "course/modules/PC/PC3/grader/test_project.py test_a_direct_call_on_a_hand_built_state_ignores_an_earlier_game lines 523-552 (docstring 524-528; engine.play(sol.quote, 0) at line 547)",
   "Docstring says: state at turn 5, history has a fill at 10020 on turn 2, no fill on turns 3-4, reload then quote, then one other game, then quote again. Code (lines 529-552) matches each clause."),
 "proj-grader-state-between-turns": ("PASS", "course/modules/PC/PC3/grader/test_project.py lines 523-552 (same function as proj-direct-call-test-docstring)",
   "Same read as above; the test checks fresh == after on a hand-built turn-5 state."),
 "proj-grader-window-distinct-paths": ("PASS", "course/modules/PC/PC3/grader/test_project.py test_fixed_seeds_0_to_49_give_fifty_different_paths lines 590-594 (round-16 cited 482-485, stale)",
   "Read this round: set of 50 tuples from make_instance(s)['fair_path_cents'] for s in range(50); expect len == 50. Passes on reference and on all 58 candidates (out/prior_candidates_seed0_r17.txt)."),
 "proj-direct-legal-sweep-turn20-no-history": ("PASS", "course/modules/PC/PC3/grader/test_project.py test_a_direct_quote_is_legal_at_every_inventory_within_the_limit lines 555-565; direct_states lines 133-151",
   "Read this round: family 1 covers turns 1-20 with turn t holding t-1 unfilled records (turn 20 included), inventories -10..10; family 2 covers turns 2-20 after a fill at each of five prices, bid and ask. Passes on the reference; the turn-indexed-history alternative is not over-constrained (out/prior_candidates_seed0_r17.txt, alt_r12_a)."),
 "proj-no-print-rare-branch-survivors": ("PASS", "course/modules/PC/PC3/grader/test_project.py test_no_function_prints_or_warns lines 462-502, direct_states lines 133-151; mutant s14_01 and v47-v49",
   "The rare-branch prints (turn 13 at inventory +7, inventory -10, price-zero fill) are reached by the direct states or the hand-built logs and are killed (out/mutate_pc3_79_0_49_r17.out)."),
 "proj-r14-reach-and-instances": ("PASS", "course/modules/PC/PC3/grader/test_project.py no-print docstring lines 465-468 and instance tests lines 571-587",
   "Read this round. The docstring's branch list is reached by the code that follows it (log with no fill, fill at 0, ends at -10 and +10, direct states)."),
 "proj-r15-integer-cent-test": ("PASS", "course/modules/PC/PC3/grader/test_project.py test_a_fill_at_any_integer_cent_price_is_booked_exactly lines 364-383 (round-16 cited 336-357, stale)",
   "Read this round: fills at 10005 (ask) and 10003 (bid); the oracle gives 2 cents; the test compares replay with the oracle exactly. Mutants r14_01 and s14_02 are killed by it."),
 "proj-r15-direct-states-log-wording": ("PASS", "course/modules/PC/PC3/project.html line 397; course/modules/PC/PC3/grader/test_project.py direct_states docstring lines 134-138 and code lines 139-151",
   "Docstring: first family turns 1-20 with unfilled records for turns 1 to t-1; second family turns 2-20 with unfilled records for turns 1 to t-2 and a fill on turn t-1, at each of the five prices, bid and ask. The code (lines 140-150) does exactly this."),
 "proj-r16-reference-collect-and-starter": ("PASS", "course/modules/PC/PC3/grader/test_project.py; grader/reference.py; grader/starter.py",
   "reference.py through the suite: 487 passed on seed 0 and 496 on seed 77314143 (out/alternatives_seed0_r17.txt, out/alternatives_seed77314143_r17.txt); starter.py: 421 failed, 66 passed on seed 0 (the suite fails on the starter)."),
 "proj-grader-reference": ("PASS", "course/modules/PC/PC3/grader/reference.py via tools/run_graders.py --unit PC3 --seeds 0-49",
   "out/run_graders_0_49.out: 'run_graders PC3: PASS (reference 50/50 seeds, slowest 0.5 s)'; in-browser grader line 'All 496 tests pass on seed 77314143'."),
 "proj-grader-starter-fails": ("PASS", "course/modules/PC/PC3/grader/starter.py with test_project.py in a scratch copy",
   "Seed 0: 421 failed, 66 passed (out/alternatives_seed0_r17.txt, the starter line). The failures are NotImplementedError from quote and replay."),
 "proj-r15-starter-fails": ("PASS", "course/modules/PC/PC3/grader/starter.py with test_project.py (seeds 0 and 77314143)",
   "Seed 0: 421 failed, 66 passed (out/alternatives_seed0_r17.txt); seed 77314143: 429 failed, 67 passed (out/starter_seed77314143_r17.txt). The suite fails on the starter on both seeds."),
 "proj-r16-numbers-independent": ("PASS", "course/modules/PC/PC3/project.html lines 57, 393-407, 455-612, 635-690 (numbers); scripts/PC3-c-r17/numbers_r17.py",
   "numbers_r17.py re-derives the game from the stated rules without the page or twin code: seed 0 at half-spread 10: 9 fills, cash -9950, inventory 1, mark 9980, pnl 30; half-spread 15: 9 fills, pnl 55; change 25 (out/numbers_r17.txt). Exemplar A sums 49910 (turns 2,3,4,8,19) and 39960 (turns 5,7,13,18) recomputed: -9950."),
 "proj-r16-exemplar-annotation-vs-rubric": ("PASS", "course/modules/PC/PC3/project.html rubric lines 620-627 and annotations (lines 651-660, 680-690)",
   "Read this round after the prose-only scoring. Every annotation's level claim matches the rubric cell it names (A: C1-C3, C5 level 4; C4 level 3 with the settlement rule missed; B: C1 2, C2 2, C3 1, C4 2, C5 1). This check compares annotations with the rubric text, not the blind scores."),
 "proj-r16-links-anchors": ("PASS", "course/modules/PC/PC3/project.html (31 href values, 21 unique); out/links_anchors_r17.txt",
   "Every href resolves: 21 unique targets exist, all 5 fragment anchors (#brief, #conventions, #grader-section, #report, #self-assessment, #spec, #stretch, #main) and L04.html#def-market-making-game exist in their target files. No external request."),
 "proj-notation": ("PASS", "notation/notation.json (8 symbols); course/modules/PC/PC3/project.html math spans (out/notation_banned_r17.txt)",
   "Math tokens used: I, I_20, N, a_t, b_t, q_t, t, v_0, v_t, v_20 and macros; none is a registered symbol (T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q). N is a local letter per notation.json 'about'."),
 "proj-r16-notation-and-terms": ("PASS", "course/modules/PC/PC3/project.html math spans; notation/notation.json (out/notation_banned_r17.txt)",
   "Same scan as proj-notation. No D-term (martingale, Kelly, Bayes, Poisson, Markov, CAPM, duration, DCF, adverse selection) appears in learner prose of project.html."),
 "proj-banned-and-process-words": ("PASS", "course/modules/PC/PC3/project.html (whole page, read in full this round); grader/*.py; tests/labs/PC3/lab-PC3-project-*.py",
   "Banned-phrase scan (out/notation_banned_r17.txt): zero hits for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, three-dot ellipsis. Process words: 'round' hits only as 'rounding'; zero for build, builder, verifier, REQUESTS, unit report."),
 "proj-rubric-atlas-studios": ("PASS", "course/modules/PC/PC3/project.html (whole page, read this round); tools/check_projects.py --unit PC3 (out/check_projects_unit.out)",
   "project.html has 0 mentions of atlas, contract or studio (out/links_anchors_r17.txt). check_projects PASS. The plan's no-Atlas and no-studio statements are unchanged."),
 "proj-hours-arithmetic": ("PASS", "course/modules/PC/PC3/project.html lines 421-438 (time budget); course/modules/PC/PC3/index.html data-hours-lessons=36 and data-hours-project=14",
   "Re-summed: 1+1+3+2+2+4+1 = 14 (the table's total). 14/50 = 28.0 %. Hub data attributes 36 and 14 sum to 50."),
 "proj-r16-hours-estimate": ("PASS", "course/modules/PC/PC3/project.html lines 421-438",
   "My own estimate per component: Rung 1 about 1 h; Rung 2 about 1 h; quote rule 2-4 h (declared 3); replay 1.5-3 h (declared 2); autograder runs 1-2 h (declared 2); analysis 3-5 h (declared 4); self-assessment 0.5-1.5 h (declared 1). Mid-point total 14 h; the declared 14 h is within 30 % (9.8-18.2)."),
 "proj-check-tools": ("PASS", "tools/check_pages.py --unit PC3; tools/check_dag.py --unit PC3; tools/check_projects.py --unit PC3 (out/check_pages_unit.out, out/check_dag_unit.out, out/check_projects_unit.out)",
   "All three exit 0 this round (out/ALL_EXIT_r17.txt): 'check_projects PC3: PASS', 'check_pages PC3: PASS', 'check_dag PC3: PASS'."),
 "proj-r8-check-tools": ("PASS", "tools/check_pages.py, check_dag.py, check_projects.py --unit PC3 (out/*_unit.out)",
   "Same as proj-check-tools; re-run this round."),
 "proj-run-labs-unit": ("PASS", "tools/run_labs.py --unit PC3 --page project (out/run_labs_project.out)",
   "'run_labs PC3: PASS (3/3)' this round."),
 "proj-r8-run-labs-page-smoke": ("PASS", "tools/run_labs.py --unit PC3 --page project; tools/run_graders.py --unit PC3 --seeds 0-49; tools/page_smoke.py --unit PC3 --pages project (out/*.out)",
   "run_labs PASS (3/3); run_graders PASS (reference 50/50); page_smoke PASS for project.html (out/page_smoke_project.out)."),
 "proj-page-smoke": ("PASS", "tools/page_smoke.py --unit PC3 --pages project (out/page_smoke_project.out)",
   "'page_smoke modules/PC/PC3/project.html: PASS' and 'page_smoke PC3: PASS' this round."),
 "proj-r15-gates": ("PASS", "tools/check_pages.py, check_dag.py, check_projects.py (--unit PC3); page_smoke.py --pages project.html; run_labs (out/ALL_EXIT_r17.txt)",
   "All exit 0 except mypy_grader_labs, which checks the grader without market_maker.py and fails on sibling imports; that is a property of the command, not of the module (the strict run with reference.py as market_maker.py PASSES, out/mypy_grader_strict_r17.out)."),
 "proj-lint-ruff": ("PASS", "ruff check and ruff format --check on course/modules/PC/PC3/grader and tests/labs/PC3; ruff check . (repo) (out/ruff_check.out, out/ruff_format.out, out/ruff_repo_r17.out)",
   "'All checks passed!' (repo ruff check .) and '14 files already formatted' (grader and labs)."),
 "proj-mypy-labs": ("PASS", "mypy --no-incremental with the repo config (files tools and tests) (out/mypy_repo_r17.out)",
   "'Success: no issues found in 385 source files', exit 0."),
 "proj-grader-mypy-strict": ("PASS", "scratch copy: engine.py, instance.py, test_project.py, market_maker.py (= reference.py) (out/mypy_grader_strict_r17.out)",
   "'Success: no issues found in 4 source files', exit 0."),
 "proj-r14-lint-mypy-pytest": ("PASS", "ruff check and format; repo mypy; pytest on PC3-selected tests (out/ruff_*.out, out/mypy_repo_r17.out, out/pytest_pc3_r17.txt)",
   "ruff and repo mypy PASS; pytest test_labs.py, test_run_labs.py, test_page_smoke.py -k PC3: 9 passed (out/pytest_pc3_r17.txt)."),
 "proj-r15-mypy-strict-grader": ("PASS", "scratch copy of engine.py, instance.py, test_project.py and market_maker.py (= reference.py) (out/mypy_grader_strict_r17.out)",
   "Same run as proj-grader-mypy-strict: no issues."),
 "proj-r16-grader-mypy-note": ("PASS", "course/modules/PC/PC3/grader/*.py (out/mypy_grader_strict_r17.out)",
   "With market_maker.py present, strict mypy passes. Without it the grader cannot type-check; expected, the module is supplied by the learner or by reference.py."),
 "proj-r8-pytest-pc3": ("PASS", "pytest -k PC3 on tests/test_labs.py, test_run_labs.py, test_page_smoke.py (out/pytest_pc3_r17.txt)",
   "9 passed, 364 deselected."),
 "proj-r8-verify-refs": ("PASS", "tools/verify_refs.py --offline (out/verify_refs_offline_r17.out); tools/verify_refs.py --unit PC3 (out/verify_refs_PC3_live_r17.out)",
   "offline integrity: 560 entries, 0 problems; live re-verification of PC3: 2 of 560 entries, 0 problems (the live run was a plain-HTTP tool run)."),
 "proj-references": ("PASS", "course/modules/PC/PC3/project.html data-cite reading list (zhou2008practical, crack2015heard); references/references.json (changed in this pin, out/delta_r17.txt)",
   "The two keys are re-verified by the live PC3 run (2 entries, 0 problems), and the offline registry check passes (560 entries). The page attributes no problem, edition or page to either book."),
 "proj-r14-reading-keys": ("PASS", "course/modules/PC/PC3/project.html lines 714-715 (data-cite) against references/references.json (changed in this pin)",
   "Same live and offline runs as proj-references."),
 "proj-twin-rules": ("PASS", "tests/labs/PC3/lab-PC3-project-1..3.py run with python -I -W error from the checkout (out/twin_vs_page_r17.txt)",
   "Exit 0 and empty stderr for all three twins; no network and no warnings."),
 "proj-lab1-run": ("PASS", "tools/run_labs.py --unit PC3 --page project; tests/labs/PC3/lab-PC3-project-1.py under python -I -W error (out/twin_vs_page_r17.txt)",
   "Twin exit 0, stderr 0 bytes, output equal to the expected block."),
 "proj-r5-labs-page-vs-twin": ("PASS", "project labs 1-3: page code vs tests/labs/PC3/lab-PC3-project-1..3.py (out/twin_vs_page_r17.txt)",
   "Lab 1 and lab 3: page code equals twin. Lab 2: the only differences are the two blanks, 'cash_flow = ___' and 'mark = ___' (the completion rule); every other line equals the twin."),
 "proj-r15-labs-twins-isolated": ("PASS", "tests/labs/PC3/lab-PC3-project-1.py, -2.py, -3.py; project.html lab sections (out/twin_vs_page_r17.txt)",
   "Each twin runs alone under python -I -W error, exit 0, empty stderr, and its output equals the page's expected block."),
 "proj-lab1-replay-prints": ("PASS", "course/modules/PC/PC3/project.html lab-PC3-project-1 (lines 55-240) against tests/labs/PC3/lab-PC3-project-1.py (out/twin_vs_page_r17.txt)",
   "Page code equals twin; the expected block equals the twin's output; the interpretation (line 239) describes the printed lines correctly."),
 "proj-lab1-hypothesis-numbers": ("PASS", "course/modules/PC/PC3/project.html line 57 (Lab 1 hypothesis); out/numbers_r17.txt",
   "9 fills, -9950, inventory 1, settlement 9980, mark 9980, pnl 30, identity holds, largest inventory 3 <= 10: all recomputed independently."),
 "proj-lab2-completion": ("PASS", "course/modules/PC/PC3/project.html lab-PC3-project-2 (lines 242-382) against tests/labs/PC3/lab-PC3-project-2.py (out/twin_vs_page_r17.txt)",
   "Page code equals the twin except the two blanks (cash_flow = ___, mark = ___); expected block equals the completed twin's output."),
 "proj-lab2-interpretation-last-quote": ("PASS", "course/modules/PC/PC3/project.html line 381 (Lab 2 interpretation)",
   "With inventory 1 unit, the mark is the settlement value, so a different price changes the P&L by the same number of cents: a true statement on this seed (numbers_r17.py)."),
 "proj-lab3-counterfactual": ("PASS", "course/modules/PC/PC3/project.html lab-PC3-project-3 (lines 457-612) against tests/labs/PC3/lab-PC3-project-3.py (out/twin_vs_page_r17.txt, out/numbers_r17.txt)",
   "Counterfactual at half-spread 15: 9 fills, pnl 55, change 25 cents, recomputed independently."),
 "proj-lab3-interpretation": ("PASS", "course/modules/PC/PC3/project.html line 611 (Lab 3 interpretation)",
   "The first block is the reference output (settlement, fills, four numbers, identity, cash agreement); the last three lines are the counterfactual. Matches the printed lines."),
 "proj-exemplar-a-numbers": ("PASS", "course/modules/PC/PC3/project.html lines 635-662 (exemplar A, prose) against out/numbers_r17.txt and the Lab 1 output",
   "Recomputed: purchases 9990+9980+9970+9980+9990 = 49910; sales 9980+9990+9990+10000 = 39960; cash flow -9950; mark 9980; P&L 30; turn 2 bid 9990, turn 5 ask 9980 with inventory 2 after, turn 18 ask 10000 with inventory 0 after: all match the log. Largest inventory 3 (Lab 1 prints it)."),
 "proj-exemplar-b-numbers": ("PASS", "course/modules/PC/PC3/project.html lines 664-692 (exemplar B, prose) against out/numbers_r17.txt",
   "30 cents, -9950 cents, turn 5 sold at the ask 9980: all match the log."),
 "proj-exemplar-b-arrival-sensitivity": ("PASS", "course/modules/PC/PC3/project.html line 676 (exemplar B text) and line 687 (annotation C4 level 2)",
   "Exemplar B names the arrival probabilities (1/4, 1/4, 1/2 from the conventions) without a result they move; the level-2 annotation matches."),
 "proj-conventions-constants": ("PASS", "course/modules/PC/PC3/project.html lines 402-407 (Conventions) and 393; grader/instance.py; grader/engine.py",
   "N = 20, v0 = 10000, moves +-5 with probability 1/2, arrivals 1/4, 1/4, 1/2, Q = 5, L = 10: all match engine.py (MAX_SIZE 5, LIMIT 10, HORIZON 20) and instance.py (START_CENTS 10000, MOVE_CENTS 5, arrival thresholds 0.25 and 0.5)."),
 "proj-rung1-instance-claim": ("PASS", "course/modules/PC/PC3/project.html line 391; course/modules/PC/PC3/grader/instance.py lines 27-53",
   "Instance: 21 integers from 10000, 20 arrivals, SIMULATED label, deterministic from random.Random(seed). Matches the page."),
 "proj-r15-exemplar-intro-fill-numbers": ("PASS", "course/modules/PC/PC3/project.html line 633 (intro) and the exemplar text (lines 635-692)",
   "Every number in the exemplars is a Lab 1 or Lab 3 output, a sum of fill prices (49910, 39960) or a fill-price-derived quote (9980, 9990, 10000), or the arrival probabilities: all recomputed in numbers_r17.py or read from the printed output."),
 "proj-r14-lab-draw-equals-instance": ("PASS", "tests/labs/PC3/lab-PC3-project-1..3.py draw_game(0) against course/modules/PC/PC3/grader/instance.py make_instance(0)",
   "Each lab's draw_game uses the same draw order and thresholds as make_instance; numbers_r17.py's independent game gives the same arrivals and settlement 9980 for seed 0."),
 "proj-named-refusals": ("PASS", "course/modules/PC/PC3/project.html lines 410-419; grader/test_project.py must_refuse calls at lines 225, 230, 241, 246, 264, 271",
   "Each named condition (bid not below ask, size outside 0..5, log not 20 turns, filled turn without price) has its own test and the phrase the page gives. The refusal checks catch ValueError (see proj-local-commands for the claim about it)."),
 "proj-exception-types": ("PASS", "course/modules/PC/PC3/grader/test_project.py must_refuse calls (lines 225-271) and the page's named-invalid list (project.html 410-419)",
   "Exception types are demanded only for the four named conditions: no must_refuse call covers a non-named input."),
 "proj-grader-replay-from-fills": ("PASS", "course/modules/PC/PC3/project.html line 407 (Conventions); grader/test_project.py test_replay_agrees_with_the_engine_final_cash_and_inventory (lines 295-308) and test_replay_returns_the_fills_cash_flow_inventory_and_pnl (lines 277-291)",
   "The two tests assert replay equals the fill-sum oracle (oracle() lines 73-84) and the engine's final cash and inventory: the fill-sum wording of line 407 is what they check."),
 "proj-r14-plan-inventory-bullet": ("PASS", "plans/PC3-build-plan.md lines 420-423 against grader/test_project.py test_fills_stop_at_the_inventory_limit_in_each_direction lines 601-611 (round-16 cited 563-574, stale)",
   "The plan's inventory bullet is implemented by that test: fills at -10 and +10 limit, and the refused eleventh fill."),
 "proj-plan-5-6-tests-not-in-suite": ("PASS", "plans/PC3-build-plan.md lines 420-423 and 430-433 against grader/test_project.py test_fills_stop_at_the_inventory_limit_in_each_direction (lines 601-611), test_a_log_carries_its_own_seed_and_settlement (lines 451-458) and test_inventory_is_marked_at_the_settlement_value_not_the_quote_mid (lines 437-447)",
   "Every test the plan's section 5.6 names exists in the suite under the plan's name or a close variant, and the page's grading list matches."),
 "proj-r14-alternatives-15": ("PASS", "ledgers/PC3/alternatives/alt1..alt6 and the 52 candidate modules listed in ledgers/PC3/scripts/PC3-c-r15/alt_candidates.txt",
   "Re-run this round: the six alternatives pass on seeds 0 and 77314143 (out/alternatives_*_r17.txt); the 52 candidate modules pass on seed 0 (52 of 52) and on seed 77314143 (out/prior_candidates_*_r17.txt). The six non-module entries of that list are runner scripts, not candidates, and are excluded."),
 "proj-r15-alternatives-all": ("PASS", "ledgers/PC3/alternatives/alt1..alt6 and the 52 candidate modules (out/prior_candidates_*_r17.txt)",
   "Same re-run as proj-r14-alternatives-15: all correct candidates pass the current suite."),
 "proj-r16-alternatives-prior-52": ("PASS", "ledgers/PC3/scripts/PC3-c-r15/alt_candidates.txt (52 modules)",
   "run_candidates_r17.sh over the 52 modules, seeds 0 and 77314143: 52 exit 0 each time (out/prior_candidates_seed0_r17.txt, out/prior_candidates_seed77314143_r17.txt)."),
 "proj-r16-mutants-76": ("FAIL", "ledgers/PC3/mutants/ (79 files, round 17); course/modules/PC/PC3/grader/test_project.py; out/mutate_pc3_79_0_49_r17.out",
   "mutate_graders --unit PC3 --seeds 0-49 over the 79 listed mutants: 78 killed, 1 SURVIVED: r17_02_replay_side_from_arrival_for_uninformed_fills.py. The 76 earlier mutants are all killed (the round-16 set plus r17_01 and r17_03 killed)."),
 "proj-local-commands": ("FAIL", "course/modules/PC/PC3/project.html line 450 (the --assert=plain paragraph) and lines 448-449; grader/test_project.py must_refuse lines 52-60 and calls at lines 264 and 271",
   "Line 450 says: 'An exception that your code raises is not caught by the suite, so that check fails with its own traceback instead.' False for ValueError raised by the learner's replay in the two refusal checks: must_refuse has 'except ValueError as error' (test_project.py line 57). Probe (out/probe_wrong_wording_r17.txt, module with replay raising ValueError('oops, wrong length')): 2 failed with 'Failed: the refusal must name the condition ...' at test_project.py:264. The --assert=plain claim (no assert statements; grep finds none) and the -W error claim are correct; lines 448-449 are correct."),
}

CARRY_EXCLUDE_PATTERNS = [r"project\.html[^;]*44[6-9]", r"project\.html[^;]*45[0-5]", r"test_project\.py lines? [1-2]?[0-9]\b"]

rows = []
carried = 0
for rid, r in prev_rows.items():
    if rid in RE:
        status, loc, ev = RE[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": status, "evidence": ev,
                     **({"fix": "Fix the sentence in project.html line 450 as stated in proj-local-commands."} if status == "FAIL" and rid == "proj-local-commands" else {}),
                     **({"fix": "Make the row's mutant set equal the suite's kill set: add a test for the r17_02 behaviour (see proj-r17-mutant-r17_02)."} if status == "FAIL" and rid == "proj-r16-mutants-76" else {})})
        continue
    if rid in ("proj-exemplar-a-calibration", "proj-exemplar-b-calibration", "proj-exemplar-scores-blind-disclosure"):
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "UNVERIFIABLE",
                     "evidence": ("Round 17 (this verifier): the blind condition is NOT certified. The start-of-round tag map "
                                  "(grep -n on section/article tags) printed project.html line 635 and line 664 including "
                                  "data-scores and data-level before any scoring, so the scores were formed with the official "
                                  "values visible. Prose-only extraction (ledgers/PC3/scripts/PC3-c-r17/extract_memo_r17.py, "
                                  "out/memo_prose_r17.txt) with the rubric (lines 623-627) gives A 4,4,4,3,4 and B 2,2,1,2,1, which "
                                  "equals the official scores, but that is not evidence of blind calibration."),
                     "fix": ("A fresh verifier that has not printed project.html lines 632-694 runs extract_memo_r17.py, "
                             "scores out/memo_prose_r17.txt against the rubric lines 623-627, and only then reads data-scores. "
                             "Record that the earlier view was absent.")})
        continue
    if rid in ("proj-hub-seed-scope", "proj-plan-grader-seed-scope"):
        pass
    # carry: subject byte-identical (see CARRY_NOTE); verify no carried row cites the changed lines
    loc = r.get("location", "")
    assert "450" not in loc and "446-455" not in loc, rid
    rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS",
                 "evidence": CARRY_NOTE + r["evidence"]})
    carried += 1

NEW = [
 {"id": "proj-r17-delta-hunks", "check": "2.6-delta (round 17 hunks in this slice)",
  "location": "course/modules/PC/PC3/project.html line 450; course/modules/PC/PC3/grader/test_project.py lines 9-13; ledgers/PC3/mutants/r16_01..03; out/delta_r17.txt",
  "status": "PASS",
  "evidence": "git diff 56cc575a..700bf33f for this slice (out/delta_r17.txt): project.html changed at line 450 only (the --assert paragraph, now 'each failed property check ... An exception ... not caught'); test_project.py changed in the module docstring only (hunk -9,8 +9,8, line numbers unchanged); mutants r16_01..03 added (already in the round-16 count). Not in this slice: L05.html, L06.html, cards.json, tests/labs/PC3/lab-PC3-L06-1.py, references/references.json (PC3 keys re-verified), plans/FINAL-ARCHITECT-RULINGS.md (ruling 15 read). Every hunk was read."},
 {"id": "proj-r17-gates", "check": "2.6-gates (round 17, all commands run on 700bf33f)",
  "location": "ledgers/PC3/scripts/PC3-c-r17/gates_r17.sh; out/ALL_EXIT_r17.txt",
  "status": "PASS",
  "evidence": "check_projects, check_pages, check_dag, run_labs (project), run_graders 0-49, ruff check and format (labs and grader), page_smoke (project), mutate_graders 0-49: all exit 0. The grader mypy line of the same script exits 1 only because it runs mypy on the grader directory without market_maker.py (sibling imports unresolved); with reference.py as market_maker.py the strict run passes (out/mypy_grader_strict_r17.out). The repo mypy (out/mypy_repo_r17.out) and ruff check . pass. Mutant run: out/mutate_pc3_79_0_49_r17.out (see proj-r16-mutants-76)."},
 {"id": "proj-r17-mutant-r17_01", "check": "2.6-mutation (new student-error mutant, round 17)",
  "location": "ledgers/PC3/mutants/r17_01_replay_memoizes_the_result_by_seed.py; test_project.py test_replay_agrees_with_the_engine_final_cash_and_inventory",
  "status": "PASS",
  "evidence": "Student error: replay caches its result by the log's seed and returns it for any later log with that seed. Killed on seed 0 by test_replay_agrees_with_the_engine_final_cash_and_inventory[36] (out/mutate_pc3_79_0_49_r17.out; run_candidates_r17.sh, 109 failures)."},
 {"id": "proj-r17-mutant-r17_02", "check": "2.6-mutation (new student-error mutant, round 17; surviving mutant that violates a stated rule)",
  "location": "ledgers/PC3/mutants/r17_02_replay_side_from_arrival_for_uninformed_fills.py; course/modules/PC/PC3/project.html line 393 (sentence 'A fill at the bid is a purchase by the maker, and a fill at the ask is a sale by the maker.'); course/modules/PC/PC3/grader/test_project.py (no test for a fill whose arrival name and price disagree)",
  "status": "FAIL",
  "evidence": "The mutant takes the side of an uninformed fill from the arrival name (uninformed-buy -> maker sells, uninformed-sell -> maker buys) and of an informed fill from its price. It passes all 487 tests on seed 0 and all 496 on seed 77314143 (run_candidates_r17.sh, out/mutate_pc3_79_0_49_r17.out: SURVIVED). It agrees with the engine on every engine-produced log, so no test distinguishes it, but a hand-built log with arrival uninformed-buy and a fill at the bid is booked as a sale, against the sentence at project.html line 393 (a fill at the bid is a purchase). Per the round rulings (a surviving grader mutant that violates a stated sentence is a FAIL).",
  "fix": "Add a hand-built test: turn 1, bid 9990, ask 10010, arrival 'uninformed-buy', filled, fill_price 9990, inventory 1, cash -9990, rest of the turns unfilled; expect replay == oracle (side from price). Candidate written and run in a scratch copy: passes on grader/reference.py and fails on r17_02 (ledgers/PC3/scripts/PC3-c-r17/out/candidate_fix_r17.txt). Not written into the repo (verifier writes no grader files)."},
 {"id": "proj-r17-mutant-r17_03", "check": "2.6-mutation (new student-error mutant, round 17)",
  "location": "ledgers/PC3/mutants/r17_03_replay_reads_the_ending_inventory_from_the_last_turn.py; test_project.py test_replay_sums_the_fills_not_the_running_totals",
  "status": "PASS",
  "evidence": "Student error: the ending inventory is the last turn's inventory_after, not the sum of the fills. Killed on seed 0 by test_replay_sums_the_fills_not_the_running_totals (out/mutate_pc3_79_0_49_r17.out)."},
 {"id": "proj-r17-alternatives-six", "check": "2.6-alternatives (six correct implementations, round 17)",
  "location": "ledgers/PC3/alternatives/alt1..alt6 (class-based integer accounts; closures and fold; inventory skew; size by inventory; threshold quoting with dataclass; quote mid from first fill)",
  "status": "PASS",
  "evidence": "run_candidates_r17.sh on the current suite: all six exit 0 with 487 passed on seed 0 and 496 passed on seed 77314143 (out/alternatives_seed0_r17.txt, out/alternatives_seed77314143_r17.txt). The reference also passes on both."},
 {"id": "proj-r17-twin-vs-page", "check": "2.5-labs (page code vs twin, round 17)",
  "location": "course/modules/PC/PC3/project.html lab-PC3-project-1..3; tests/labs/PC3/lab-PC3-project-1..3.py",
  "status": "PASS",
  "evidence": "scripts/PC3-c-r17/twin_vs_page_r17.py (out/twin_vs_page_r17.txt): lab 1 and lab 3 page code equal the twin; lab 2 differs only at the two completion blanks; the expected block equals each twin's output; each twin exits 0 with empty stderr under python -I -W error."},
 {"id": "proj-r17-spec-command", "check": "2.6-spec (documented command, round 17)",
  "location": "course/modules/PC/PC3/project.html line 393 (python3 -c command for game_log.json)",
  "status": "PASS",
  "evidence": "In a folder with engine.py, instance.py and reference.py copied as market_maker.py: python3 -c 'import json, engine, market_maker; print(json.dumps(engine.play(market_maker.quote, 0)))' exits 0 and prints the log as JSON beginning {\"seed\": 0, \"settlement_cents\": 9980, \"turns\": [...]} (out/spec_command_r17.txt)."},
 {"id": "proj-r17-scope-words", "check": "2.9-prose (scope words, round 17)",
  "location": "course/modules/PC/PC3/project.html (every, only, same, any, exactly, all, always, never; whole page read this round)",
  "status": "PASS",
  "evidence": "Scan (out/notation_banned_r17.txt and the round-17 read): 'every turn' and 'every value' claims are checked by the suite (test_quotes_are_legal_on_every_turn, direct states); 'a quote depends only on the state' is checked by test_the_quote_depends_only_on_the_state_it_is_given; 'a log shows only the settlement value' is true of engine.py's log keys; 'every instance is SIMULATED' is the label set in instance.py; 'the lab does not test any other seed' is true of lab 3's twin (seed 0 only); the zero counts for all, always, never, drives. 'any other invalid input may raise any exception' matches the suite's refusals."},
 {"id": "proj-r17-rubric-c1-levels", "check": "2.6-rubric (C1 descriptors exclusive: a fabricated value must cap the level)",
  "location": "course/modules/PC/PC3/project.html rubric row C1, cells level 4 and level 3 (line 623); level 1 cell (line 623)",
  "status": "FAIL",
  "evidence": "The level-1 cell says a C1 submission that states 'a value that replay does not return' is level 1. The level-2 cell forbids such a value ('no value that replay does not return'), but the level-3 and level-4 cells do not. The caption's rule ('takes the highest level whose descriptor it meets') then scores a submission that states all three correct values, names the turns, and also states an unreturned value (for example 'fills: 9') at level 4, although the level-1 descriptor it also meets says level 1. The descriptors are therefore not exclusive for this case.",
  "fix": "Add 'and no value that replay does not return' to the level-4 and level-3 cells of C1 (project.html line 623), so that the level-1 clause is never overridden by a higher cell."},
 {"id": "proj-r17-blind-status", "check": "2.6-rubric (blind calibration status, round 17)",
  "location": "course/modules/PC/PC3/project.html lines 635-692 (data-scores, annotations); ledgers/PC3/scripts/PC3-c-r17/extract_memo_r17.py; out/memo_prose_r17.txt",
  "status": "UNVERIFIABLE",
  "evidence": "Recorded in full in proj-exemplar-scores-blind-disclosure (the start-of-round grep printed data-scores). No blind scores can be certified for this verifier.",
  "fix": "A fresh verifier re-scores from out/memo_prose_r17.txt before reading the attributes (see proj-exemplar-scores-blind-disclosure)."},
]

rows.extend(NEW)
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
missing = [i for i in prev_rows if i not in ids]
assert not missing, missing

mut = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$")
for line in open(f"{ROOT}/{S}/mutate_pc3_79_0_49_r17.out", encoding="utf-8"):
    m = pat.match(line.rstrip("\n"))
    if m:
        verdict, name, desc, killed = m.groups()
        mut.append({"name": name, "description": desc, "killed_by": None if killed.strip() == "None" else killed.strip()})
assert len(mut) == 79, len(mut)

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 and all(m["killed_by"] for m in mut) else "FAIL"

frag = {
    "unit": "PC3",
    "slice": "c",
    "round": 17,
    "verifier": "independent verifier (Haiku 5.5), round 17, slice c; did not build PC3; blind exemplar calibration NOT certified (see proj-exemplar-scores-blind-disclosure)",
    "pin": "700bf33f",
    "base": "round 16 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round16.json (pin 56cc575a). Delta 56cc575a..700bf33f for this slice: project.html line 450 and test_project.py module docstring lines 9-13 only; mutants r16_01..03 added; out/delta_r17.txt.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE17-PC3-c (detached at 700bf33f; .venv symlinked; course/assets/vendor present)",
    "scratch": "ledgers/PC3/scripts/PC3-c-r17/ (gates_r17.sh, out/, run_candidates_r17.sh, twin_vs_page_r17.py, numbers_r17.py, extract_memo_r17.py, build_fragment_r17.py, probe_wrong_wording_market_maker.py, alternatives via ledgers/PC3/alternatives); temp copies in /tmp/pc3c_r17_* (removed)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mut,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Blindness: this verifier's start-of-round grep (tag map) printed project.html lines 635 and 664 including data-scores before the prose-only scoring. The blind calibration is therefore UNVERIFIABLE again, as in round 16. Prose-only scores (out/memo_prose_r17.txt, rubric lines 623-627) are A 4,4,4,3,4 and B 2,2,1,2,1, equal to the official values; not evidence of a blind run.",
        "Carried rows (status PASS, prefix 'Carried from round 16'): the cited subject is byte-identical between the pins. Rows whose cited test_project.py lines were stale in round 16 (the function had moved) were re-verified this round by reading the whole suite and carry the round-17 locations.",
        "Full read this round: project.html (732 lines, including the exemplars after the prose scoring), grader/engine.py, instance.py, reference.py, starter.py and test_project.py (645 lines), and the three project twins (out/twin_vs_page_r17.txt).",
        "The repo mypy gate covers tools and tests only; the grader is type-checked in a scratch copy with reference.py as market_maker.py (out/mypy_grader_strict_r17.out).",
        "Mutants: 79 listed (76 from earlier rounds, r17_01..03). 78 killed on seeds 0-49; r17_02 survives and is a FAIL (proj-r17-mutant-r17_02).",
        "Alternatives: 6 in ledgers/PC3/alternatives and 52 candidate modules: all pass on seeds 0 and 77314143.",
    ],
    "summary": (f"PC3-c round 17: verdict {verdict}. Rows {len(rows)}: PASS {counts['PASS']}, FAIL {counts['FAIL']}, "
                f"UNVERIFIABLE {counts['UNVERIFIABLE']}. Mutants {sum(1 for m in mut if m['killed_by'])}/{len(mut)} killed on seeds 0-49. "
                f"Carried rows: {carried}."),
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(frag["summary"])
