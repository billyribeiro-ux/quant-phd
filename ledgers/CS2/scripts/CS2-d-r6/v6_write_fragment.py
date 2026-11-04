"""Round-6 fragment writer for CS2 slice d. Builds ledgers/CS2/CS2-d.json from the recorded outputs in this folder.
Run from the checkout root: python3 ledgers/CS2/scripts/CS2-d-r6/v6_write_fragment.py"""

import json
import pathlib
import re
from datetime import UTC, datetime

root = pathlib.Path.cwd()
D = root / "ledgers/CS2/scripts/CS2-d-r6"
mut_lines = (D / "v6_mutate_final.txt").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    killed_by = None if killed.strip() == "None" else re.sub(r" \(seed \d+\)$", "", killed.strip())
    if status == "KILLED" and killed_by is None:
        raise SystemExit(f"parse error: {line}")
    mutants.append({"id": name, "description": desc, "killed_by": killed_by})
assert len(mutants) == 132, len(mutants)

P = "PASS"
F = "FAIL"
ROWS = [
    ("gate-mutate-cs2", "gate", "ledgers/CS2/mutants/ (132 files); tools/mutate_graders.py", F,
     "Command: .venv/bin/python tools/mutate_graders.py --unit CS2 --seeds 0-9 (output scripts/CS2-d-r6/v6_mutate_final.txt, exit 1). Last lines: 'SURVIVED v6_01_variance_default_ddof_is_population.py: ... -> None' and 'mutate_graders CS2: FAIL (131/132 killed)'. The gate must exit 0.",
     "Add a grader test that variance() equals variance(1): with values 1.0 and 3.0, acc.variance() must be 2.0 (close to variance(1)), which kills v6_01. Re-run the mutate gate; it must print PASS (132/132)."),
    ("gate-run-graders", "gate", "course/modules/CS/CS2/grader/", P,
     "Command: .venv/bin/python tools/run_graders.py --unit CS2 --seeds 0-49 -> 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.2 s)' (scripts/CS2-d-r6/v6_run_graders.txt). Also my own per-seed run of reference.py: exactly '174 passed' on 50/50 seeds (v6_alts_and_refs.out.txt)."),
    ("gate-check-projects", "gate", "tools/check_projects.py", P, "Command: .venv/bin/python tools/check_projects.py --unit CS2 -> 'check_projects CS2: PASS' (scripts/CS2-d-r6/v6_check_projects.txt, exit 0)."),
    ("gate-check-dag", "gate", "tools/check_dag.py", P, "Command: .venv/bin/python tools/check_dag.py --unit CS2 -> 'check_dag CS2: PASS' (v6_check_dag.txt, exit 0)."),
    ("gate-check-pages", "gate", "tools/check_pages.py; course/modules/CS/CS2/", P, "Command: .venv/bin/python tools/check_pages.py --unit CS2 -> 'check_pages CS2: PASS' (v6_check_pages.txt, exit 0)."),
    ("gate-run-labs", "gate", "tests/labs/CS2/; project.html labs", P, "Command: .venv/bin/python tools/run_labs.py --unit CS2 -> 'run_labs CS2: PASS (14/14)' (v6_run_labs.txt, exit 0)."),
    ("gate-page-smoke", "gate", "course/modules/CS/CS2/project.html", P,
     "Command: .venv/bin/python tools/page_smoke.py --unit CS2 --pages project (run alone) -> 'page_smoke modules/CS/CS2/project.html: PASS', 'in-browser grader: All 174 tests pass', all three Pyodide labs ran (scripts/CS2-d-r6/v6_page_smoke_project.txt, exit 0). NOTE: the round-5 row ran '--pages project.html', which matches no page (the tool compares the stem 'project') and reported a vacuous PASS; this round's run is the first real page_smoke evidence for project.html."),
    ("gate-ruff-mypy", "gate", "course/modules/CS/CS2, tests/labs/CS2, grader", P,
     "ruff check course/modules/CS/CS2 tests/labs/CS2 -> 'All checks passed!' (exit 0); ruff format --check on the same paths exit 0; repo 'ruff check .' exit 0; mypy --no-incremental -> 'Success: no issues found in 331 source files' (v6_mypy.txt). Outside slice d: repo 'ruff format --check .' exits 1 on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py (not a CS2 file; recorded in notes)."),
    ("gate-verify-refs", "gate", "references/references.json; tools/verify_refs.py", P,
     "Command: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (v6_verify_refs_offline.txt, exit 0). Command: tools/verify_refs.py --unit CS2 (live, network) -> 'live re-verification of CS2: 1 of 560 entries, 0 problems', exit 0 (v6_verify_refs_live.txt)."),
    ("gate-collect-count", "gate", "course/modules/CS/CS2/grader/test_project.py; project.html:211", P,
     "pytest --collect-only -q on reference.py as streamstats.py, for seeds 0-49: '174 tests collected' on every seed (each seed run gave exactly '174 passed'; v6_alts_and_refs.out.txt). project.html:211 states 'collects 174 checks ... for each of the seeds 0 to 49' and matches."),
    ("gate-pytest-relevant", "gate", "tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py tests/test_refs.py", P,
     "Command: .venv/bin/pytest -q <5 files> -> all dots, exit 0 (v6_pytest_relevant.txt)."),
    ("labs-project-1", "2.5/labs", "course/modules/CS/CS2/project.html:145; tests/labs/CS2/lab-CS2-project-1.py:70-71", F,
     "Ran the twin under python -I -W error (exit 0); page code equals the twin except a trailing newline; expected block equals the output (scripts/CS2-d-r6/v6_labs_compare.out.txt). But project.html:145 says 'the last line says the brute-force check agreed at every step'. The printed output's last line is 'deque operations: 44 ... bound 4n = 48'; the agreement line 'every step agrees with brute force: True' is the penultimate line (twin lines 70-71).",
     "In project.html line 145 change 'the last line says the brute-force check agreed at every step' to 'the line before the last says the brute-force check agreed at every step'."),
    ("labs-project-2", "2.5/labs", "course/modules/CS/CS2/project.html:146-188; tests/labs/CS2/lab-CS2-project-2.py", P,
     "Page code equals the twin except the two blanks (page 'mean = ___', 'm2 = ___'; twin 'mean = mean + delta / count', 'm2 = m2 + delta * (x - mean)'), which the docstring describes (checked by reading both). Twin run exit 0; output 'count 8 / mean 1000003.750000 / sample variance 8.500000' equals the expected block. Arithmetic recomputed: offsets sum 30, mean 3.75, sum of squares 59.5, /7 = 8.5."),
    ("labs-project-3", "2.5/labs", "course/modules/CS/CS2/project.html:260-337; tests/labs/CS2/lab-CS2-project-3.py", P,
     "Page code equals the twin except a trailing newline; twin exit 0; expected block equals output (8 lines incl. 'welford mean within 1e-9 of exact: True'). Recomputed with Fraction: sum 110046.0, exact mean 10004.181818, exact sample variance 8.313636, last four values min 10001.0 max 10006.3, median rank target 5 (5.5 - 1.1 = 4.4), 5th smallest 10003.2. Float rank target check: 0.1*20 - 0.05*20 = 1.0 in floats (ceil 1) but exact ceil is 2."),
    ("proj-prose-numbers", "2.9/2.2", "project.html lede 37; Lab 1 interpretation 145; Lab 2 hypothesis 150 and interpretation 188; Lab 3 interpretation 338; exemplars 376-390", P,
     "Every number in these passages recomputed or matched to a printed output: 44 deque operations and bound 48 (Lab 1 output); 8.5 and 1000003.75 and the eight offsets (Lab 2); 110046.0, 10004.181818, 8.313636, 4.4, 5, 10003.2 (Lab 3); 'eleven values', 'twelve values', 'eight values'. The wording defect in line 145 is recorded in labs-project-1."),
    ("proj-line145-amortized", "2.2/2.9", "project.html:145; course/modules/CS/CS2/L10.html Corollary 2.5(a), Theorem 2.4", P,
     "The claim 'constant amortized work per value in the average sense of Lesson 10, which bounds the average over a run and not the cost of any single value' is what L10 Corollary 2.5(a) states (average operations per insertion <= 2 over a run of n values, amortized O(1) in the average sense defined in Section 2). The 'last line' wording on the same line is recorded in labs-project-1."),
    ("proj-process-words", "2.9", "project.html; grader/*.py; tests/labs/CS2/lab-CS2-project-*.py; cards.json", P,
     "Scanned with grep -i for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it can be shown', 'it is important to note', 'studies show', 'experts agree', 'well known', 'obviously', 'clearly', verifier, builder, ledger, agent, 'round N', '...': no hits in any of those files."),
    ("proj-rubric-calibration", "2.6 rubric", "project.html:348-390 (rubric-memo; exemplar-a; exemplar-b)", P,
     "Calibration was NOT blind: I read the exemplar annotations before scoring. Scored each exemplar from the descriptor text. Exemplar A: C1 1 (no hypotheses listed), C2 1 (base case asserted, algebra not shown), C3 2 (S named, not tied to a sum after each count), C4 1, C5 1, C6 1. Exemplar B: 4 on each criterion (hypotheses H1-H3 listed and cited; base case and algebra justified; S invariant carried; real vs 64-bit float named; both inequalities, probes and three limits stated; counts and agreement cited, no timing). Official scores (data-scores) match my scores within one level."),
    ("proj-rubric-observable", "2.6 rubric", "project.html rubric-memo table C1-C6 (lines 348-355)", P,
     "Read each of the 24 level descriptors. Each names an element a reader can check (a numbered hypothesis list before the statement, a base case at one value, an S invariant after each count, a named arithmetic, two inequalities with the probe set, a printed count or agreement with the lab named). No descriptor relies on 'good', 'clear' or 'thorough'."),
    ("proj-ladder-scope", "2.6 spec", "project.html:40-52 (ladder), 53-188 (rungs 1-2), 260-337 (rung 3 lab), 400-411 (rung 4)", P,
     "Rung 1 worked example with a 'Why' note at each step (Lab 1). Rung 2 completion graded instantly (class 'lab completion'). Rung 3 specification. Rung 4 open-ended stretch. Tier F: the rung 1-2 minimum rule does not apply. The hub placement diagnostic (two data-skill items) matches the ladder sentence. check_projects PASS."),
    ("proj-notation", "2.9 notation", "project.html math spans; notation/notation.json; L09, L11 local symbols", P,
     "notation.json registers T, Phi, gamma3, gamma4, R*, R^e*, R_f, Q (blackboard). None appears in project.html or in the CS2 lessons' math spans (checked). Project symbols n, q, epsilon, x, v, delta (deviation), S (sum of squared deviations) follow L09 S_n and L11 Definition 1.2 (epsilon) and are local per notation.json's header. 'm' appears only in exemplar A, defined there as the mean."),
    ("proj-dag-concepts", "2.9 DAG", "project.html lede links; L09/L10/L11 dfn ids; concepts.html#mathematical-induction", P,
     "check_dag CS2 PASS. Lede links resolve: L09.html#def-welford-algorithm, L10.html#def-monotonic-deque, L11.html#def-quantile-sketch (each id present). The induction link resolves to concepts.html#mathematical-induction, an M1 concept in the CS2 prerequisite closure per the architect decision (Issue 1)."),
    ("proj-reading-citation", "2.1", "project.html:408-414 (reading); references/references.json key cormen2022introduction", P,
     "The reading list cites data-cite cormen2022introduction only, and states that no locator is given and no step is attributed to the textbook. Registry record read: title 'Introduction to Algorithms, Fourth Edition', four authors, Open Library source. verify_refs CS2 live: 1 of 560 entries, 0 problems."),
    ("proj-exemplar-b-claims", "2.4", "project.html:376-390 (exemplar-b)", P,
     "Re-derived the Welford induction in exemplar B line by line: mean update, a = -delta/(n+1), the cross term vanishes by the definition of the mean, S_{n+1} = S_n + n a^2 + n^2 delta^2/(n+1)^2 = S_n + n delta^2/(n+1) = S_n + delta(x_{n+1} - mean_{n+1}). Correct. Probe list (0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1 and one seeded value) matches instance.py PROBES_FIXED plus one seeded probe; streams of one to eight values with epsilons 0.05, 0.1, 0.2 match test_sketch_rank_guarantee_on_short_streams; Lab 1 44 <= 48 and Lab 3 8.313636 match the outputs."),
    ("proj-spec-completeness", "2.6 spec", "project.html Required outputs (lines 200-207), Constraints (209), Grading mode (211), Local (219-224)", P,
     "Questions a student would have asked, and where the page answers them: which 10 probes (grader/instance.py PROBES_FIXED plus one seeded value; the page names the file and the seed); which exceptions (the ten named conditions, Constraints); whether a None or string input must raise (Constraints says 'raises or denotes the number'); whether a float window 2.5 must raise (Constraints: raises an exception of any type). Not tested but stated: 'no method changes its arguments' (scalar arguments cannot change), and the '-> None' return annotations. Neither is a behaviour the suite must observe in this unit."),
    ("proj-hours", "2.6 hours", "project.html:227-246 (table id hours); course/modules/CS/CS2/index.html:29-43; L01-L11 data-hours", P,
     "Table rows 2+3+4+4+4+6+4+3 = 30 = data-hours-project. Hub 100 lesson hours and 30 project hours = 130 = curriculum; 30/130 = 23.1%, shown as 23%. Lesson data-hours sum to 100 (8+9+10+10+9+9+10+10+10+8+7). My own estimate of a competent tier-F student's effort (library with tests 10-14 h, Welford proof 4-6 h, sketch design and tests 6-9 h, rungs 1-2 and note 6-8 h) is 26-37 h, inside 30 +/- 30%."),
    ("proj-named-conditions", "2.6 grader", "grader/test_project.py must_raise call sites; project.html Constraints (209)", P,
     "Every must_raise call maps to one of the ten named conditions (Welford before-value, variance(1) with one value, NaN update, window < 1 incl. False, NaN push, minimum/maximum before push, epsilon outside (0,1) incl. NaN, infinities, booleans, NaN add, q outside [0,1], quantile on empty). The other invalid inputs use refuse_or_correct or 'an exception of any type', as Constraints states. Each named condition has a test (listed in the Named errors paragraph)."),
    ("grader-instance", "2.6 grader", "course/modules/CS/CS2/grader/instance.py", P,
     "make_instance is deterministic (test_instance_is_deterministic). Seeds 0-49: stream lengths 20-400, windows 2-30, epsilon in {0.05,0.1,0.2}, ten probes in [0,1], label 'SIMULATED stream N'. Distinctness: 50 seeds give 50 distinct (window, epsilon, n, exact sample variance) tuples (v6_alts_and_refs.out.txt)."),
    ("instance-docstring-counts", "2.2 numbers", "course/modules/CS/CS2/grader/instance.py:8-15", P,
     "Re-ran with python -I: seeds per offset {0: 16, 10000: 23, 1000000: 11} (docstring: 16, 23, 11). Naive variance (ss - n mean^2)/(n-1) with s += x, ss += x*x, mean = s/n, against the exact Fraction value at the grader's tolerance: failures {10000: 22, 1000000: 11}, and 0 at offset 0; the passing seeds at offset 10000 are seed 41 only (docstring: 'seed 41 passes'). Welford fails no seed of 0-49."),
    ("grader-reference", "2.6 grader", "course/modules/CS/CS2/grader/reference.py", P,
     "Run for seeds 0-49 as streamstats.py: exactly '174 passed' on 50/50 seeds (v6_alts_and_refs.out.txt, run via scripts/CS2-d-r6/v6_run_suite.sh). Read every line of reference.py (Welford update, rolling deques with index expiry, sketch with bisect insertion, compression cap floor(2 eps n)+1, exact Fraction target)."),
    ("grader-starter", "2.6 grader", "course/modules/CS/CS2/grader/starter.py", P,
     "Suite on starter.py, seed 0: '171 failed, 3 passed' (v6_alts_and_refs.out.txt). The suite fails on the starter as the page requires; the 3 passing checks are the instance and stdlib-only checks."),
    ("grader-tests-rank", "2.6 grader", "course/modules/CS/CS2/grader/test_project.py:850-885 (wide epsilon), 858 (witness), 876-906 (fixed witnesses)", P,
     "Recomputed the three witnesses with Fraction: (a) eps 0.3, stream [1.0, 2.0], q=1.0: target ceil(2 - 0.6)=2, only 2.0 satisfies both inequalities (1 < 1.4 for 1.0); (b) q=0.1, n=20, eps=0.05: exact target 2 (difference 1 + 5.6e-17 > 1), 64-bit float target 1 (0.1*20 - 0.05*20 == 1.0); (c) q=0.2500004, n=20, eps 0.05: qn = 5.000008, target 5; q rounded to 0.25 gives target 4. The tests match each docstring."),
    ("grader-docstring-delta", "2.6 grader", "course/modules/CS/CS2/grader/test_project.py (new test, module docstring); project.html:211", P,
     "The page's Grading-mode list was checked item by item against the suite: boundary values, empty-object checks, Welford against Fraction on prefixes 2-20 and the whole stream, scaling by 4, rolling checks for eight widths and repeated values, sketch probes, short/sorted/tied streams, eps 0.3/0.5/0.9, the fixed witnesses, 101-point monotonicity, int count, printing, stdlib imports, and value/window rules. Each named item has a test."),
    ("grader-messages-no-expected-value", "2.6 grader", "course/modules/CS/CS2/grader/test_project.py (every pytest.fail and must_raise message)", P,
     "Read every failure message. Messages name the property and print only the input under test, the learner's own return value, or the ddof/window the test chose; none prints the expected answer."),
    ("grader-new-mutants", "2.6 mutation", "ledgers/CS2/mutants/r4v_01..03", P,
     "Each of r4v_01, r4v_02, r4v_03 is listed in v6_mutate_final.txt as KILLED (rank target, rank-target rounding, two-value variance divisor)."),
    ("grader-alternatives", "2.6 alternatives", "ledgers/CS2/scripts/CS2-d-r6/alts_v6/ (alt_v6_a, b, c, d, e, f); ledgers/CS2/equivalent/ (d8_01, d8_02, d9_04, rank_target_without_clamp)", P,
     "Six new correct implementations, each run as streamstats.py for seeds 0-49, all exactly '174 passed' on 50/50 seeds: A two-pass exact-list accumulator with fsum and a sorted-list sketch; B delta-squared M2 form; C rolling deques that keep ties; D sketch with no compression (every value stored); E sketch with exact cap 2 eps n (no floor, no +1); F float() coercion of every argument (strings and booleans read as numbers; non-whole windows and non-0/1 ddof refused). Plus the four ledgers/CS2/equivalent variants, all 50/50. Round-5 FAIL (window 2.5) is resolved: Constraints now states that a window that denotes no whole number, such as 2.5, raises an exception of any type, so the test is spec-backed. Fuzz: 200 random streams (heavy ties, sorted runs, eps in {0.05..0.9}, probes k/40 plus random q, check after every add) gave 0 guarantee violations for reference, d8_01, d8_02, d9_04, alt D, alt E."),
    ("grader-mutant-r5v01", "2.6 mutation", "ledgers/CS2/mutants/r5v_01_sketch_compression_folds_maximum_into_predecessor.py", P,
     "v6_mutate_final.txt: 'KILLED r5v_01_... -> test_sketch_rank_guarantee_at_wide_epsilon[0.3] (seed 0)'. The round-5 survivor is now killed by the new test."),
    ("grader-mutant-v6-01", "2.6 mutation", "ledgers/CS2/mutants/v6_01_variance_default_ddof_is_population.py; course/modules/CS/CS2/project.html:202; grader/test_project.py", F,
     "Mutant: WelfordAccumulator.variance defaults to ddof 0. It survives every test: 174 passed on all 50 seeds (v6_alts_and_refs.out.txt), and the mutate gate reports SURVIVED. The page states the signature 'variance(ddof: int = 1) -> float' (project.html:202: 'ddof 0 gives the population variance and ddof 1 the sample variance'), so the default value is a stated behaviour and a mutant that violates it must be killed. No test calls variance() with no argument and checks its value (line 175 only checks the call before any value).",
     "Add to grader/test_project.py a test: acc.update(1.0); acc.update(3.0); if not close(acc.variance(), acc.variance(1)) or not close(acc.variance(), 2.0): pytest.fail('variance() with no argument must be the sample variance, as the Required outputs state.'). Re-run run_graders (50 seeds) and mutate_graders (expect 132/132)."),
    ("grader-new-mutants-v6-02-04", "2.6 mutation", "ledgers/CS2/mutants/v6_02_rolling_deques_shared_at_class_level.py; v6_03_quantile_target_uses_n_plus_one.py; v6_04_sketch_stores_arrival_order_unsorted.py", P,
     "KILLED in v6_mutate_final.txt: v6_02 by test_rolling_window_one_is_valid (seed 0; class-level deques shared between objects); v6_03 by test_sketch_rank_guarantee_on_short_streams[2-0.05] (seed 0; target from q(n+1)); v6_04 by test_sketch_rank_guarantee_at_each_probe[0] (seed 0; unsorted stored values). Each also violates Constraints or Conventions (each class holds its state in the object only; rank guarantee)."),
    ("cards-automated", "2.7", "course/modules/CS/CS2/cards.json (225 cards)", P,
     "Parsed with python -I: 225 cards, ids unique (CS2-c001..c226 with c067 absent, no duplicate ids), no exact duplicate fronts or backs, 149 grade T (no basis) and 76 grade C (each with basis); every lesson L01-L11 has cards (L01 14, L02 25, L03 21, L04 20, L05 23, L06 15, L07 21, L08 26, L09 19, L10 13, L11 28)."),
    ("cards-sample", "2.7", "cards.json: CS2-c003, c041, c057, c088, c112, c131, c150, c177, c196, c211 (10 unchanged cards)", P,
     "Each checked against its lesson statement: c003 Proposition 1.2 (witness c = a+b+1, n0 = 1); c041 Definition 1.1 (insertion sort); c057 Definition 2.1 (AVL variant); c088 Corollary 2.3 (strong induction); c112 Proposition 1.3 (book stays uncrossed; the 'remainder rests' step is Definition 2.1); c131 Theorem 2.3 (front index is the latest minimum); c150 Lab 1 k0,k1,k2 = 40,120,240 (printed); c177 Lab 4 Part B lower 13 and merge bound 21 (printed); c196 Lab 1 relative errors 8.852e-11 and 1.418e-02, ratio 1.60e8 (printed); c211 Proposition 1.4 (h(64j) = 0)."),
    ("cards-changed-delta", "2.7", "cards.json: changed c008, c015, c024, c135, c142, c143, c165; added c226", P,
     "Each of the eight cards was read against its lesson: c008 Proposition 2.3 and Remark 2.2 (L01); c015 Assumption 2.1 and Problem P2 (L02); c024 Proposition 2.2, Problem R3 ('costs more exactly when alpha >= 2' for integer n, verified algebraically) and Lab 2 printed 3.0156 / 4.0280 at n=256 (alpha 4.00); c135 Theorem 2.2 hypotheses and Corollary 2.5(c) (L10); c142 Definition 2.1 k_h formula and 'k_h >= (h+1)(h+2)/eps' (L11); c143 Definition 2.1 compaction; c165 Lab 1 printed line '1000 of 1000', Proposition 1.6 (count exactly n-1), Problem E3 (L01); c226 Definition 2.1 add. All numbers and references are present in the lesson (scan below)."),
    ("cards-c215", "2.7", "cards.json CS2-c215 (L05)", P,
     "AVL rule: L05 Definition/Section 3 (Insertion and rotations) states the heavy child's balance factor 0 or same sign gives one single rotation, opposite sign gives a double rotation; the card matches. 'Lab 1, Part A checks it after each of 500 seeded insertions' matches the lesson text."),
    ("cards-lab-numbers", "2.7", "cards.json: CS2-c024, c150, c165, c177, c196 (lab-printed numbers)", P,
     "Ran tests/labs/CS2/lab-CS2-L01-1.py, L02-1, L04-1, L09-1, L11-1 under python -I -W error (exit 0): each printed number on these cards appears in the output (listed under cards-sample and cards-changed-delta)."),
    ("cards-duplicates", "2.7", "cards.json (full scan)", P,
     "Full pairwise scan with difflib: 217 pairs above similarity thresholds (front > 0.6 or back > 0.7). Each high-similarity pair asks the same question with different parameters or quantities (for example c196 vs c197: offset 10^6 vs 10^9; c150 vs c166: epsilon 1/20 vs 1/10; c168, c169, c170, c171: Lab 2 at different alpha; c183/c184/c185: different rotations). No pair is a duplicate. No exact duplicate front or back."),
    ("cards-c033", "2.7", "cards.json CS2-c033 (L03); course/modules/CS/CS2/L03.html Proposition 1.5-1.6", P,
     "Proposition 1.6 states the sorted-list total in the hold run is at most 2N(N+1); the card matches. Lab 3 twin output: N=512 gives 65561 sorted-list moves <= 2*512*513 = 525312."),
    ("cards-full-number-scan", "2.7", "cards.json (all 225 cards against lesson text)", P,
     "For every card: every number in front and back appears in its lesson's text; every Proposition, Corollary, Theorem, Definition, Remark, Assumption, Problem, Research and Misconception reference appears in its lesson (problem labels such as 'R3 ·', 'E3 ·', 'M3 ·' are the lesson's labels for Problem R3, E3, M3). 'Section N' references resolve to the numbered lesson headings. Zero unresolved references."),
    ("mut-survivors", "2.6 mutation", "ledgers/CS2/equivalent/ (README.md and 4 files)", P,
     "The four files are alternative correct implementations (per the README's Lemmas 0-3), not equivalent mutants: each passes 50/50 seeds (exactly 174 passed). I re-derived Lemma 3's upper inequality (K-1 <= floor(x), band <= max(1, C_n) <= floor(2 eps n)+1, so the count is at most floor(qn+eps n)) and the fuzz gave 0 violations for reference, d8_01, d8_02, d9_04 over 200 random streams. None is a student error the specification forbids, so none belongs in mutants/. Recorded in notes."),
    ("equiv-m14_01", "2.6 mutation", "ledgers/CS2/equivalent/rank_target_without_clamp.py", P,
     "Proof re-derived: the first stored tuple has g >= 1, so its running rank is at least 1 >= any unclamped target <= 1; both versions return values[0]. Unclamped K >= 1 is identical. Passes 50/50 seeds."),
    ("instance-distinct-seeds", "2.8/2.6", "course/modules/CS/CS2/grader/instance.py", P,
     "Seeds 0-49: 50 distinct exact sample variances and 50 distinct (window, epsilon, n, variance) tuples (scripts v6_alts_and_refs.out.txt via v6_instance_claims). The instances differ materially in their answers, not only in labels."),
]

rows = [{"id": i, "check": c, "location": loc, "status": s, "evidence": ev,
         **({"fix": fx} if s != P else {})} for (i, c, loc, s, ev, fx) in [(*r[:4], r[4], r[5] if len(r) > 5 else "") for r in ROWS]]
# re-create fix field for FAIL rows
fixes = {
    "gate-mutate-cs2": "Add the default-ddof test described in grader-mutant-v6-01, then re-run tools/mutate_graders.py --unit CS2 --seeds 0-9 (expect 132/132 killed, exit 0).",
    "labs-project-1": "In course/modules/CS/CS2/project.html line 145 change 'the last line says the brute-force check agreed at every step' to 'the line before the last says the brute-force check agreed at every step'.",
    "grader-mutant-v6-01": "Add to grader/test_project.py: acc.update(1.0); acc.update(3.0); assert close(acc.variance(), 2.0) and close(acc.variance(), acc.variance(1)), with a failure message naming the default ddof from Required outputs. Re-run run_graders (50 seeds) and mutate_graders (132/132).",
}
for r in rows:
    if r["status"] == F:
        r["fix"] = fixes[r["id"]]
for r in rows:
    r.pop("fix", None) if r["status"] == P else None

counts = {s: sum(1 for r in rows if r["status"] == s) for s in (P, F)}
verdict = "PASS" if counts[F] == 0 else "FAIL"
fragment = {
    "unit": "CS2",
    "slice": "d",
    "round": 6,
    "verifier": "independent verifier (Haiku), round 6; did not build CS2; slice d",
    "pin": "142ecfc2bd27061de18bd67e83df81e69f5c249d",
    "base": "440ed3c8216725d498d9c6d7c746907d4d418198 (round-5 pin); delta: project.html lines 208, 404; grader/test_project.py (new wide-epsilon test); cards.json (c008, c015, c024, c135, c142, c143, c165 changed; c226 added); ledgers/CS2/mutants/r5v_01..03 added",
    "checkout": str(root),
    "scratch": "ledgers/CS2/scripts/CS2-d-r6/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-6 new student-error mutants (4 written, 1 survives): v6_01 default ddof 0 SURVIVES all 50 seeds (FAIL); v6_02 class-level deques, v6_03 target from q(n+1), v6_04 unsorted sketch are killed.",
        "Six new alternative correct implementations (alts_v6/ A-F) plus the four ledgers/CS2/equivalent variants pass 50/50 seeds. None is over-constrained; the round-5 alternatives FAIL (window 2.5) is resolved by the Constraints sentence 'raises an exception of any type'.",
        "The round-5 gate 'page_smoke --pages project.html' was vacuous (the tool compares page stems, so it checked zero pages). Round 6 reran it as '--pages project': real Pyodide and browser checks passed.",
        "Calibration is not blind: the exemplar annotations were read before scoring. Scores were derived from the descriptor text and match the official scores.",
        "Notation: no registered symbol is used by the slice. S, delta, epsilon and m follow the lesson-local meanings.",
        "Hours: the page's 30 h budget and the hub's 100+30 split are arithmetically consistent. My effort estimate (26-37 h) is inside 30 +/- 30%.",
        "Outside slice d (not a CS2 row): repo-wide 'ruff format --check .' exits 1 on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py. Repo 'ruff check .' passes; the CS2 files pass both.",
        "ledgers/CS2/scripts/CS2-d-r6/ already held round-6 artifacts committed earlier (commit 7aa909e9, 'Batch 2: fixes for independent verification round 6'). I did not rely on them; my scripts use the v6_ prefix and sit beside them. ledgers/CS2/CS2-d.json was overwritten by this round's fragment.",
        "mutate_graders attributes a kill to the first failing test in file order, so a few kills name a test that is not the one aimed at the mutant (for example s3_10 is attributed to test_rolling_non_integral_float_window_is_refused). Each such mutant is still killed by a test; the attribution is imprecise.",
    ],
    "summary": (f"CS2 slice d, round 6: {verdict}. {len(rows)} rows ({counts[P]} PASS, {counts[F]} FAIL). Mutants 131/132 killed; v6_01 (default ddof 0) survives all 50 seeds. "
                "FAILs: the mutate gate (v6_01), the ddof default test gap (grader-mutant-v6-01), and a Lab 1 interpretation sentence that names the wrong output line (labs-project-1, project.html:145). "
                "All other gates pass: check_pages, check_dag, check_projects, run_labs (14/14), run_graders (50/50), page_smoke (project, real run), mypy, ruff on the slice, verify_refs offline and live, collect count 174 on every seed, and relevant pytest."),
}
out = root / "ledgers/CS2/CS2-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants), "verdict", verdict)
