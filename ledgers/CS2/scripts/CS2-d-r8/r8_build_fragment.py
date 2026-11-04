"""Round 8, CS2 slice d: assemble the verifier fragment ledgers/CS2/CS2-d.json from the r8 script outputs.

Every row cites a script or output file under ledgers/CS2/scripts/CS2-d-r8/ (or a repo path). Mutant entries are
parsed from r8_mutate_all.txt (tools/mutate_graders.py --unit CS2 --seeds 0-9).
"""
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
S = "ledgers/CS2/scripts/CS2-d-r8"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---------------------------------------------------------------- gates (2.5/2.6 commands, run by this verifier)
row("gate-mutate-cs2", "gate", "ledgers/CS2/mutants/ (139 files); course/modules/CS/CS2/grader/test_project.py", "PASS",
    f"Command: .venv/bin/python tools/mutate_graders.py --unit CS2 --seeds 0-9 -> 'mutate_graders CS2: PASS (139/139 killed)', exit 0 ({S}/r8_mutate_all.txt). 136 existing mutants re-run plus three new r8v mutants.")
row("gate-run-graders", "gate", "course/modules/CS/CS2/grader/", "PASS",
    f"Command: .venv/bin/python tools/run_graders.py --unit CS2 --seeds 0-49 -> 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 ({S}/r8_run_graders.txt).")
row("gate-check-projects", "gate", "tools/check_projects.py; course/modules/CS/CS2/project.html", "PASS",
    f"Command: tools/check_projects.py --unit CS2 -> 'check_projects CS2: PASS', exit 0 ({S}/r8_check_projects.txt).")
row("gate-check-dag", "gate", "tools/check_dag.py", "PASS",
    f"Command: tools/check_dag.py --unit CS2 -> 'check_dag CS2: PASS', exit 0 ({S}/r8_check_dag.txt).")
row("gate-check-pages", "gate", "course/modules/CS/CS2/", "PASS",
    f"Command: tools/check_pages.py --unit CS2 -> 'check_pages CS2: PASS', exit 0 ({S}/r8_check_pages.txt).")
row("gate-run-labs", "gate", "tests/labs/CS2/; project.html lab blocks", "PASS",
    f"Command: tools/run_labs.py --unit CS2 -> 'run_labs CS2: PASS (14/14)', exit 0 ({S}/r8_run_labs.txt).")
row("gate-page-smoke", "gate", "course/modules/CS/CS2/project.html", "PASS",
    f"Command: tools/page_smoke.py --unit CS2 --pages project (run alone) -> 'page_smoke modules/CS/CS2/project.html: PASS', 'in-browser grader: All 175 tests pass', exit 0 ({S}/r8_page_smoke_project.txt).")
row("gate-ruff-mypy", "gate", "course/modules/CS/CS2, tests/labs/CS2, grader", "PASS",
    f"ruff check: 'All checks passed!' ({S}/r8_ruff_check.txt); ruff format --check: '18 files already formatted' ({S}/r8_ruff_format.txt); mypy --no-incremental on grader and labs: 'Success: no issues found in 18 source files' ({S}/r8_mypy.txt).")
row("gate-verify-refs", "gate", "references/references.json", "PASS",
    f"Command: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}/r8_verify_refs_offline.txt). The live run was not performed; the one record this slice uses was checked with plain curl (row proj-reading-citation).")
row("gate-collect-count", "gate", "course/modules/CS/CS2/grader/test_project.py; project.html Grading mode", "PASS",
    f"Script {S}/r8_collect_and_instances.py: pytest --collect-only on reference.py (as streamstats.py) for seeds 0-49 -> '175 tests collected' for all 50 seeds ({S}/r8_collect_and_instances.out.txt). Page says 175 (project.html:211).")
row("gate-pytest-relevant", "gate", "tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py tests/test_page_smoke.py", "PASS",
    f"Command: .venv/bin/pytest -q -p no:cacheprovider on those five files -> dots only, exit 0 ({S}/r8_pytest_relevant.txt).")
row("gate-local-pytest", "gate", "course/modules/CS/CS2/grader/test_project.py; project.html Running the suite locally", "PASS",
    f"reference.py copied as streamstats.py; QF_SEED=0, 17, 41; pytest -q -p no:cacheprovider --assert=plain -W error test_project.py -> '175 passed' each (Python 3.14.8, pytest 9.0.2, which project.html:257 names) ({S}/r8_local_pytest_reference.txt). Covers 3 of 50 seeds locally; the 50-seed run is the Pyodide-equivalent gate above.")

# ---------------------------------------------------------------- labs (2.5)
row("labs-project-1", "2.5-lab", "course/modules/CS/CS2/project.html:53-146; tests/labs/CS2/lab-CS2-project-1.py", "PASS",
    f"Script {S}/r8_labcheck.py (output {S}/r8_labcheck.out.txt): twin run as 'python -I -W error', exit 0, empty stderr. Page code equals twin except a trailing newline. Expected block equals output (trailing whitespace only). Hypothesis and interpretation checked: 'every step agrees with brute force: True'; step 9 minimum 1 is still in the window at step 12 ([1, 47, 61, 35]); 44 deque operations <= 4n = 48; 'does not measure time'. Rung-1 'Why' notes sit on the deque rules (project.html lines 80, 82, 88, 94, 100); the page (project.html:44) claims a note on each deque rule, which matches.")
row("labs-project-2", "2.5-lab", "course/modules/CS/CS2/project.html:148-189; tests/labs/CS2/lab-CS2-project-2.py", "PASS",
    f"Script {S}/r8_labcheck.py: twin under -I -W error exit 0. Page code equals twin line for line except the two blanks 'mean = ___' and 'm2 = ___' (class lab completion). Expected 'count 8 / mean 1000003.750000 / sample variance 8.500000' equals output. Interpretation re-derived: offsets 2,5,1,4,9,3,6,0 have mean 3.75 and sum of squares about the mean 59.5, so the sample variance is 59.5/7 = 8.5.")
row("labs-project-3", "2.5-lab", "course/modules/CS/CS2/project.html:262-339; tests/labs/CS2/lab-CS2-project-3.py", "PASS",
    f"Script {S}/r8_labcheck.py and {S}/r8_numbers.py (outputs r8_labcheck.out.txt, r8_numbers.out.txt): twin exit 0 under -I -W error; expected equals output. Numbers recomputed from unrounded Fractions: sum 110046.0, exact mean 10004.181818..., exact sample variance 8.313636..., Welford agrees to 1e-9 (True), last-four min 10001.0 and max 10006.3, 5.5 - 1.1 = 4.4 so rank 5, 5th smallest 10003.2.")

# ---------------------------------------------------------------- project prose and structure (2.2, 2.4, 2.6, 2.9)
row("proj-prose-numbers", "2.2-numbers", "project.html lede, Inputs, Grading mode, time table, Labs 1-3 interpretations, exemplars", "PASS",
    f"Every number in the page re-derived: 175 checks ({S}/r8_collect_and_instances.out.txt); 20-400 values, window 2-30, epsilon {{0.05,0.1,0.2}}, ten probes (instance.py PROBES_FIXED line 27 plus one seeded value); time table 2+3+4+4+4+6+4+3 = 30; lesson hours 8+9+10+10+9+9+10+10+10+8+7 = 100 (data-hours on L01-L11) and 100 + 30 = 130 = curriculum hours; Lab 1 44 <= 48; Lab 3 8.313636 and 10003.2; Conventions example 2 - 0.3*2 = 1.4 ({S}/r8_witness.py); rank witnesses 2 vs 1 and 5 vs 4 ({S}/r8_witness.py).")
row("proj-line145-amortized", "2.9-interpretation", "course/modules/CS/CS2/project.html:145 (Lab 1 interpretation, changed since round 7)", "PASS",
    "Changed sentence: 'it would leave the window at step 13, which this lab does not run'. Value 1 is pushed at step 9 (index 8); at step 13 the window holds indices 9-12, so index 8 leaves there (window arithmetic on the printed series, project.html:139-142). The lab runs twelve steps only. Re-verified from scratch this round.")
row("proj-line386-design-note", "2.6-spec / 2.9", "course/modules/CS/CS2/project.html:386 (design.md probe list, changed since round 7)", "PASS",
    "Each claim re-checked against the suite: ten probes = nine fixed plus one seeded (instance.py:27,41); streams of one to eight values at eps 0.05, 0.1, 0.2 (test_project.py:829-845); sorted streams (816-826); repeated values (848-858); eps 0.3, 0.5, 0.9 at q 0, 0.25, 0.5, 0.75, 1 (861-873); fixed twenty-value stream at q = 0.1 and q = 0.2500004 (876-911); constant stream (802-806). The rank target is the ceiling of qn - eps n and at least 1 (Conventions). Re-verified from scratch this round.")
row("proj-process-words", "2.9-banned", "project.html; grader/*.py; tests/labs/CS2/lab-CS2-project-*.py; cards.json", "PASS",
    "grep -n -i over the slice for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, in this section, in this lesson, let us, we will: no hit. Two hits on 'this page': the nav label 'On this page' (not learner prose) and project.html:413 'so this page gives no locator', a factual description of the citation, not a process instruction.")
row("proj-rubric-observable", "2.6-rubric", "course/modules/CS/CS2/project.html:348-357 (rubric-memo, C1-C6, four levels each)", "PASS",
    "All 24 level descriptors read. Each names a checkable element: a numbered hypothesis list before the statement, base case at one value, both inequalities with the slack, named probes and streams, a printed lab count or measured error. None is vague.")
row("proj-rubric-calibration", "2.6-rubric", "course/modules/CS/CS2/project.html:362-390 (exemplar-a, exemplar-b; data-scores)", "UNVERIFIABLE",
    "Not blind. The exemplar annotation paragraphs were read in this session before any scoring, so the calibration cannot be called blind. Rubric-only re-score of the exemplar bodies (annotations not used): A gives C1 1, C2 1, C3 2, C4 1, C5 1, C6 1 (official 1,1,2,1,1,1). B gives C1 3 or 4 (H1 is cited in the closing sentence, not at the division step), C2 4, C3 4, C4 4, C5 4, C6 4 (official 4s). Both are within one level of the official scores, but that is not the blind test the rule requires.",
    fix="Run the exemplar calibration with a fresh verifier that has not read the exemplar annotations (project.html:362-390). Score A and B from the rubric table alone and record the scores here; the row passes if every criterion is within one level.")
row("proj-ladder-scope", "2.6-ladder", "course/modules/CS/CS2/project.html:40-190, 260-340, 400-406", "PASS",
    "Rung 1 is Lab 1, fully solved with why notes. Rung 2 is Lab 2, class lab completion, with an expected block that grades the blanks. Rung 3 is the spec, grader and write-up, matching the curriculum project 'Streaming statistics library' (curriculum/01-foundations.yaml:442-449). Rung 4 is open-ended stretch. Tier F keeps rungs 1-2 at full length, as BUILDER_RULES 5.1 requires.")
row("proj-notation", "2.4-notation", "notation/notation.json; project.html math spans; cards.json", "PASS",
    "Script {S}/r8_notation_check.py (output r8_notation_check.out.txt): registry has eight entries (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); 34 math spans on project.html use only S, S_n, n, q, x, x_i, a, i, delta, epsilon, bar-x, sum; collisions: none. cards.json: the only matches for registry-like patterns are the strict rank R^-(v) (cards c140, c141, c147, c148, c152, c217), which the registry does not register, so there is no collision. Requesting R^- under NOTATION_REQUESTS is the lesson builder's obligation, noted here, not a finding.")
row("proj-dag-concepts", "2.9-DAG", "project.html lede and rung-3 links; L09-L11; ../../../concepts.html#mathematical-induction", "PASS",
    f"{S}/r8_check_dag.txt PASS. Links to welford-algorithm (L09), monotonic-deque (L10) and quantile-sketch (L11) are in-unit and earlier. mathematical-induction is defined in M1 (course/modules/M/M1/L06.html:id def-mathematical-induction), and M1 is a CS2 prerequisite in curriculum/curriculum.json (prereqs [CS1, M1]). The project page has no dfn (grep count 0).")
row("proj-reading-citation", "2.1-citation", "project.html:408-414; references/references.json:5962 (cormen2022introduction)", "PASS",
    "Registry key present (status verified, Open Library OL34192801M). Plain curl: 'curl -s https://openlibrary.org/books/OL34192801M.json' returned HTTP 200 with title 'Introduction to Algorithms, Fourth Edition', publish year 2022, publisher MIT Press, ISBN-13 9780262046305, matching the registry. The page gives no locator and attributes no step to the book (project.html:413).")
row("proj-exemplar-b-claims", "2.4-math", "project.html:376-390 (exemplar B proof and design note)", "PASS",
    "Re-derived by hand: a = -delta/(n+1); sum over i<=n of (x_i - xbar_{n+1})^2 = S_n + n a^2 (middle term zero by definition of xbar_n); x_{n+1} - xbar_{n+1} = n delta/(n+1); total S_{n+1} = S_n + n delta^2/(n+1) = S_n + delta (x_{n+1} - xbar_{n+1}). Base case S_1 = 0. Sample variance S_n/(n-1). Lab 1 44 <= 48 and Lab 3 1e-9 agreement are the printed evidence the page cites.")
row("proj-spec-completeness", "2.6-spec", "project.html Inputs, Required outputs, Constraints, Conventions, Named errors", "PASS",
    "Questions a competent student would ask, each answered on the page: default ddof (signature variance(ddof: int = 1), Required outputs); None and strings (Constraints); which conditions raise ValueError (the ten named conditions); how the rank target is computed (Conventions, Exact counts); probe count and stream sizes (Inputs); monotonicity (Conventions); memory not tested (Conventions). No unanswered question found.")
row("proj-hours", "2.6-hours", "project.html:227-246 (table id hours); course/modules/CS/CS2/index.html:29-43", "PASS",
    "Independent estimate, central case: rung 1 2 h; rung 2 1 h; Welford accumulator with its suite run 3 h; Welford proof 3.5 h; deque min and max 3 h; quantile sketch 4 h; named-condition validation 2 h; design note and self-assessment 3 h. Total 21.5 h, which is 28% below the declared 30 h, inside the 30% bound. The low end of my range (about 17 h) would be outside it; the margin is small.")
row("proj-named-conditions", "2.6-spec", "project.html:209 (Constraints, ten named conditions); grader/test_project.py must_raise call sites", "PASS",
    "The ten conditions: (1) mean/variance before a value, test_project.py:170-179; (2) variance(1) with one value, :182-185; (3) NaN update, :214-221; (4) window below 1 incl. False, :427-436; (5) NaN push, :455-462; (6) min/max before push, :447-452 and :924; (7) epsilon outside (0,1) incl. booleans, infinities, NaN, :650-666; (8) NaN add, :768-774; (9) q outside [0,1], NaN, infinities, :669-687; (10) quantile on empty, :704-710. Every must_raise call maps to one of these ten.")

# ---------------------------------------------------------------- grader (2.6)
row("grader-instance", "2.6-instance", "course/modules/CS/CS2/grader/instance.py", "PASS",
    f"Read in full. Deterministic (test_instance_is_deterministic). Lengths 20-400, offsets {{0, 1e4, 1e6}}, decimals {{1, 6}}, windows 2-30, epsilons {{0.05, 0.1, 0.2}}, ten probes, one invalid kind per seed among six named conditions (window_zero=(4), epsilon_one=(7), q_above_one=(9), welford_nan=(3), rolling_nan=(5), sketch_nan=(8)). Label 'SIMULATED stream {{seed}}'. Sampled seeds 0-19 differ in every (n, window, eps, variance) tuple ({S}/r8_collect_and_instances.out.txt).")
row("instance-docstring-counts", "2.2-numbers", "course/modules/CS/CS2/grader/instance.py:8-13", "PASS",
    f"Script {S}/r8_numbers.py (output r8_numbers.out.txt): seeds per offset {{0: 16, 1e4: 23, 1e6: 11}}; naive-formula failures {{1e4: 22, 1e6: 11, 0: 0}}; the only passing 1e4 seed is 41. The docstring's counts and exception match exactly.")
row("grader-reference", "2.6-autograder", "course/modules/CS/CS2/grader/reference.py", "PASS",
    f"Read in full (143 lines). run_graders 50/50 ({S}/r8_run_graders.txt). Local pytest passes 175 on seeds 0, 17, 41 ({S}/r8_local_pytest_reference.txt).")
row("grader-starter", "2.6-autograder", "course/modules/CS/CS2/grader/starter.py", "PASS",
    f"Every method raises NotImplementedError (read in full). Suite run on the starter for seeds 0-4: 0/5 pass, failing seeds [0, 1, 2, 3, 4] ({S}/r8_starter_seeds0_4.txt).")
row("grader-tests-rank", "2.6-autograder", "course/modules/CS/CS2/grader/test_project.py:861-912", "PASS",
    f"Witness 1 (q 0.1, n 20, eps 0.05): exact Fraction target 2 (difference 1 + 1.1e-15 > 1), float target 1 ({S}/r8_witness.py). Witness 2 (q 0.2500004): qn = 5.000008, exact target 5, q rounded to 0.25 gives 4, needs at_or_below >= 4.000008 ({S}/r8_witness.py). Both docstrings match.")
row("grader-docstring-delta", "2.6-autograder", "course/modules/CS/CS2/grader/test_project.py:203-212; project.html:211", "PASS",
    "Test test_welford_variance_default_ddof_is_sample (added since round 7) matches the grading-mode text on project.html:211 ('the default of variance(), which is ddof 1 ... on two values'). Re-verified from scratch this round.")
row("grader-messages-no-expected-value", "2.6-autograder", "course/modules/CS/CS2/grader/test_project.py (all pytest.fail and must_raise messages)", "PASS",
    "Every message read. Each prints the property name, the input under test, or the learner's own return value. None prints an expected answer. The changed message at test_project.py:872 ('wide epsilon (0.3, 0.5 or 0.9)') names the property and reveals no answer.")
row("grader-new-mutants", "2.6-mutation", "ledgers/CS2/mutants/r4v_01..03", "PASS",
    f"Killed in {S}/r8_mutate_all.txt: r4v_01 (test_sketch_rank_guarantee_on_short_streams[3-0.2] seed 0), r4v_02 (...[2-0.05] seed 0), r4v_03 (test_welford_sample_variance_of_two_values_is_defined seed 0).")
row("grader-mutant-r5v01", "2.6-mutation", "ledgers/CS2/mutants/r5v_01_sketch_compression_folds_maximum_into_predecessor.py", "PASS",
    f"Killed by test_sketch_rank_guarantee_at_wide_epsilon[0.3] (seed 0) ({S}/r8_mutate_all.txt).")
row("grader-mutant-v6-01", "2.6-mutation", "ledgers/CS2/mutants/v6_01_variance_default_ddof_is_population.py; course/modules/CS/CS2/grader/test_project.py:203-212", "PASS",
    f"Killed by test_welford_variance_default_ddof_is_sample (seed 0) ({S}/r8_mutate_all.txt).")
row("grader-new-mutants-v6-02-04", "2.6-mutation", "ledgers/CS2/mutants/v6_02..v6_04", "PASS",
    f"Killed: v6_02 by test_rolling_window_one_is_valid (seed 0); v6_03 by test_sketch_rank_guarantee_on_short_streams[2-0.05] (seed 0); v6_04 by test_sketch_rank_guarantee_at_each_probe[5] (seed 0) ({S}/r8_mutate_all.txt).")
row("grader-new-mutants-r7v", "2.6-mutation", "ledgers/CS2/mutants/r7v_01..04", "PASS",
    f"Killed: r7v_01 by test_sketch_rank_guarantee_at_each_probe[3]; r7v_02 by the same probe test; r7v_03 by the same probe test; r7v_04 by test_welford_sample_variance_matches_exact_reference (all seed 0) ({S}/r8_mutate_all.txt).")
row("grader-new-mutants-r8v", "2.6-mutation", "ledgers/CS2/mutants/r8v_01_welford_mean_uses_floor_division.py; r8v_02_welford_mean_rounded_to_six_places.py; r8v_03_rolling_expires_candidate_by_count.py", "PASS",
    f"Three new student-error mutants, each a complete module with a one-line docstring error: r8v_01 mean += delta // count (killed by test_welford_population_variance_matches_exact_reference, seed 0); r8v_02 mean() rounded to six places (killed by test_welford_every_short_prefix_matches_exact[3], seed 2; passes seeds 0,1,3,4,5,8,9, so the mutant is not killed on every seed); r8v_03 rolling min/max expiring the front by count (killed by test_rolling_ties_expire_with_their_index[2], seed 0). ({S}/r8_mutate_all.txt; candidates in {S}/cands/r8c_*.py.)")
row("grader-alternatives", "2.6-over-constraint", f"{S}/cands/alt_r8_a..f.py", "PASS",
    f"Six alternative correct implementations, each passes 50/50 seeds: a exact sorted-list sketch; b store-all two-pass (math.fsum); c exact Fraction Welford state; d running-sum mean with the Welford identity for M2; e sketch cap from stored tuple count; f brute-force rolling min/max. Output {S}/r8_alternatives_seeds0_49.txt. Rank guarantee fuzzed for all six: 37,500 probes each, 0 violations ({S}/r8_fuzz_guarantee.py; the first version used Fraction(q) of the exact q and was corrected to the float the grader passes).")
row("mut-survivors", "2.6-equivalence", "ledgers/CS2/equivalent/ (d8_01, d8_02, d9_04)", "PASS",
    f"Re-run this round: 50/50 seeds each ({S}/r8_equivalent_survivors_seeds0_49.txt) and 37,500 guarantee probes each with 0 violations. They are correct alternatives, not spec violations, so they are not counted as faults (Conventions: 'the autograder does not test memory'; the guarantee is the only sketch behaviour the spec states).")
row("equiv-m14_01", "2.6-equivalence", "ledgers/CS2/equivalent/rank_target_without_clamp.py", "PASS",
    f"Suite 50/50 and 37,500 guarantee probes with 0 violations ({S}/r8_equivalent_survivors_seeds0_49.txt). Argument re-derived: stored tuples have g >= 1, so the first running rank is >= 1; if the unclamped target is below 1 both versions return values[0]; otherwise the two targets are equal.")
row("instance-distinct-seeds", "2.6-instance", "course/modules/CS/CS2/grader/instance.py", "PASS",
    f"Seeds 0-19: 20 distinct (n, window, epsilon, exact sample variance) tuples and 20 distinct exact means ({S}/r8_collect_and_instances.out.txt). Answers change, not only labels.")
row("gate-mutate-r7-new", "2.6-mutation", "ledgers/CS2/mutants/r7v_01..04", "PASS",
    f"All four r7v mutants killed in the 139/139 run ({S}/r8_mutate_all.txt).")

# ---------------------------------------------------------------- cards (2.7)
row("cards-automated", "2.7-cards", "course/modules/CS/CS2/cards.json (216 cards)", "PASS",
    f"Script {S}/r8_cards_checks.py (output {S}/r8_cards_checks.out.txt): 216 cards; ids unique and CS2-cNNN; keys exact (basis present exactly when grade is not T); grades C and T; every lesson L01-L11 has a card; numbers other than 0, 1, 2 on each card missing from its own lesson text: 0; numbers on grade-C cards missing from the lesson text and the twin output: 0; twins L01-L11 each exit 0 under -I -W error.")
row("cards-sample", "2.7-cards", "cards.json: sample of 22 cards checked against lesson text and twin output", "PASS",
    f"Sample (one row per ~10 cards): c003 (witness c = a+b+1, n0 = 1, correct); c009 (2^k - 1 comparisons, 4^k pair steps, counts printed by L01 twin); c024 (Lab 2 prints 4.0280 and 3.0156 at n = 256; output {S}/r8_twin_L02.out); c035 (see its own row); c048 (Corollary 2.2 proof: n! >= (n/2)^(floor(n/2)+1), L04.html); c063 (Lab 1 Part A 500 insertions); c065 (L05 twin: plain BST 64, AVL 7, log_phi 65 = 8.6747); c069 (1.440420 in L05 twin); c075 (L06 twin: 40 graphs, 200 sources = every source, 0 mismatches); c097 (47 calls, 28 subproblems, 183 without memo); c123 (two-pass smallest error at 0, 1e6, 1e9); c127 (S_3 = 2 gives 1 and 2/3); c151 (198430 and 18213 match L11 text); c155 (see its own row); c157 (0.2680, 0.5400, 1.0960, 2.0320, 4.0280 match L02 twin); c159 (166912); c174 (see its own row); c205 (L11 Problem M3 solution: 20th and 40th adds compact); c209 (L02 'four limits', Section 3 is 'Where the canon breaks'); c210 (50 probes by Proposition 1.4); c215 (AVL rotation rule; checked invariant output in L05 twin); c227 (see its own row); c165 (L01 'E3' exists, Lab 1 line quoted); c154 (window 1, 2, 5 largest removal counts 1, 2, 5 in L10 twin).")
row("cards-changed-delta", "2.7-cards", "cards.json entries changed or added since the round-7 pin (c035, c155, c174, c227) and the round-7 changed set (c008, c015, c024, c135, c142, c143, c165)", "PASS",
    "Changed/added entries re-verified (rows cards-c035, cards-c155, cards-c174, cards-c227). Round-7 changed set: c008, c024, c143, c165 re-read this round against the lesson text and the twin (see cards-sample). Carried from round 7 (cards.json entries c015, c135, c142 byte-identical since the previous pin, git diff 9373ef39..2d755599 touches only c035, c155, c174 and adds c227): their round-7 evidence stands for those three entries only.")
row("cards-c155", "2.7-cards", "course/modules/CS/CS2/cards.json CS2-c155 (front, back, basis); tests/labs/CS2/lab-CS2-L02-1.py output", "PASS",
    f"Round-7 FAIL re-verified from scratch. Card now prints averages only: 'Lab 2 prints 2.0078 at n = 128 and 3.0156 at n = 256 ... model values 1.9922 and 2.9922'. Lab 2 output ({S}/r8_twin_L02.out): alpha 2.00 n=128 successful average 2.0078 (model 1.9922); alpha 4.00 n=256 successful average 3.0156 (model 2.9922). Model check 1 + (n-1)/(2m) with m = 64: 1 + 127/128 = 1.9922, 1 + 255/128 = 2.9922. No totals claimed. PASS.")
row("cards-c035", "2.7-cards", "course/modules/CS/CS2/cards.json CS2-c035; lab-CS2-L03-1 output rows N=64..4096", "PASS",
    f"Round-7 FAIL re-verified. Front: largest per-doubling growth factor of the sorted list's moves for a row from N=64 to N=4096. Printed ratios in rows 64..4096: 3.5282, 4.5050, 3.9129, 3.7118, 4.1119, 4.0287, 4.0316 ({S}/r8_twin_L03.out). Maximum 4.5050 at N=128, where the sorted list makes 4514 moves against 1002 at N=64; 4514/1002 = 4.50499 rounds to 4.5050. PASS.")
row("cards-c174", "2.7-cards", "course/modules/CS/CS2/cards.json CS2-c174; lab-CS2-L03-1 output rows N=64..4096", "PASS",
    f"Round-7 FAIL re-verified. Front: smallest per-doubling growth factor of the heap's moves for a row from N=64 to N=4096. Printed heap move ratios in rows 64..4096: 2.3778, 2.2331, 2.1535, 1.9858, 2.0100, 2.0722, 2.0687 ({S}/r8_twin_L03.out). Minimum 1.9858 at N=512, where the heap makes 21095 moves against 10623 at N=256; 21095/10623 = 1.98587. PASS.")
row("cards-c227", "2.7-cards", "course/modules/CS/CS2/cards.json CS2-c227 (new card, L05, grade T)", "PASS",
    "Back: every key in the left subtree is smaller than the node's key and every key in the right subtree is larger (Section 1). L05.html text: 'left subtree of a node is smaller than the node's key, and every key in the right subtree is larger'. Matches.")
row("cards-lab-numbers", "2.7-cards", "cards.json grade C (66 cards); tests/labs/CS2/lab-CS2-L01-1..L11-1", "PASS",
    f"Each C-card number checked against its twin output ({S}/r8_twin_L0*.out): e.g. c022 (1.0000), c038 (205 vs 602 at N=16; 19140 vs 21405 at N=256), c039 (4933, 4514, 10623, 17663), c052 (21), c053 (1023, 5120), c097, c098 (30+30), c099 (length 3, 49 cells), c113 (185 created, 177 removed, 8 remain), c123, c124, c150 (40/120/240; 20/60/120), c157, c162 (298), c163 (7 steps), c164 (340), c176 (14), c177 (13, 21), c180 (11), c181 (12.9186), c182-c185 (63, 53, 55, 57), c186 (1238), c193-c195, c198-c202, c154, c158, c160.")
row("cards-duplicates", "2.7-cards", "course/modules/CS/CS2/cards.json (full pairwise scan)", "PASS",
    f"Script {S}/r8_cards_checks.py: exact duplicate fronts: none. 57 near-duplicate pairs (front or back difflib ratio > 0.8). Each pair asks different facts: e.g. c030/c031 push vs pop comparisons; c035/c174 max vs min moves ratio; c115/c187 levels created vs removed; c184/c185 double left-right vs right-left rotations; c191/c192 trades vs executions; c124/c195 naive vs Welford at offset 1e9. No pair is a duplicate.")
row("cards-c033", "2.4-cards", "cards.json CS2-c033; L03 twin output", "PASS",
    f"Sorted-list moves 98 at N=16 <= 2*16*17 = 544 and 4378444 at N=4096 <= 2*4096*4097 = 33562624 ({S}/r8_twin_L03.out). Bound statement is Proposition 1.6 (lesson text).")
row("cards-full-number-scan", "2.7-cards", "cards.json (all 216 cards)", "PASS",
    f"{S}/r8_cards_checks.py: numbers (other than 0, 1, 2) on any card missing from its own lesson text: 0.")
row("cards-c215", "2.4-cards", "cards.json CS2-c215 (AVL double/single rotation rule)", "PASS",
    f"Rule restated matches the standard AVL case split. Lab 1 Part A invariant after every insertion True ({S}/r8_twin_L05.out). Lesson Section 3 text not re-read this round; carried from round 7 by byte identity of the cards.json entry c215 (not in the delta).")
row("cards-count-observation", "2.7-cards", "cards.json", "PASS",
    "Observation only (not a row finding): 216 cards against the planner's expected 50-80 (plan section 9). check_pages passes, so the count is recorded, not failed.")

# ---------------------------------------------------------------- mutants list
mutants = []
for line in (ROOT / S / "r8_mutate_all.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^KILLED (\S+): (.*) -> (.*)$", line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})

# ---------------------------------------------------------------- fragment
frag = {
    "unit": "CS2",
    "slice": "d",
    "round": 8,
    "verifier": "independent verifier (Haiku), round 8; did not build CS2; slice d",
    "pin": "2d755599d8d74df292e3e43025f0458c4053802e",
    "base": "9373ef398589097500ea849e30ff9da423b98943 (round-7 pin); delta: project.html lines 145 and 386; grader/test_project.py line 872 (failure message); cards.json c035, c155, c174 changed, c227 added; mutants r7v_01..04 (re-run); new mutants r8v_01..03; new candidates under ledgers/CS2/scripts/CS2-d-r8/cands/",
    "checkout": str(ROOT),
    "scratch": S,
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-7 FAIL rows cards-c035, cards-c155 and cards-c174 are re-verified from scratch and now PASS.",
        "Round-7 proj-rubric-calibration was not blind; this round it is UNVERIFIABLE for the same reason. This is the only non-PASS row.",
        "Mutation gate: 139 of 139 killed on seeds 0-9 (136 existing, 3 new). Every mutant file is a complete module with a one-line docstring.",
        "Alternatives: six correct implementations pass 50/50 seeds; the rank guarantee is fuzzed for six sketch-bearing candidates and for the reference, 37,500 probes each, 0 violations.",
        "The 'Carried from round 7' prefix is used only in cards-changed-delta for entries byte-identical since the previous pin (c015, c135, c142) and cards-c215.",
        "Rung 1 annotation covers the deque rules (twin lines 80-100), not each append; project.html:44 claims exactly that, so the row passes on the page's wording.",
        "The checkout's ledgers/CS2/CS2-d.json was overwritten by this round's fragment; it previously held a round-15 fragment with pin 448548f9 that is not from this pin's lineage.",
    ],
    "summary": "CS2 slice d, round 8: FAIL. All gates pass (mutate 139/139, run_graders 50/50, check_pages/dag/projects, run_labs 14/14, page_smoke project, ruff, ruff format, mypy, verify_refs offline, collect 175 on seeds 0-49, relevant pytest, local pytest 3 seeds). The three round-7 card FAILs are re-verified and pass. One row is non-PASS: proj-rubric-calibration is UNVERIFIABLE because the exemplar calibration was not blind (annotations read before scoring).",
}
out = ROOT / "ledgers/CS2/CS2-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "non-PASS", [r["id"] for r in rows if r["status"] != "PASS"])
