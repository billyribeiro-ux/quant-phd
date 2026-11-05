"""Writes the round-10 CS2 slice-d fragment (ledgers/CS2/CS2-d.json) from the verification results."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/CS2/scripts/CS2-d-r10"
PASS, FAIL, UNV = "PASS", "FAIL", "UNVERIFIABLE"
FIX_PRINT = (
    "In course/modules/CS/CS2/grader/test_project.py test_classes_never_print (lines 243-258), also call "
    "variance(0), read count, call quantile(0.0) and quantile(1.0), and make the refused calls on fresh objects "
    "(mean, variance(0), minimum, quantile(0.5)) under the same capsys check. Checked in scratch: "
    f"{S}/fixcheck/test_project_fixed.py passes the reference and the five round-10 alternatives on seeds 0-9 "
    "(run_fixed.sh) and kills r10_01 and r10_02 on seeds 0-2. Then re-run tools/mutate_graders.py --unit CS2 "
    "--seeds 0-9; expect 156/156 killed and exit 0."
)

rows = [
    ("gate-mutate-cs2", "gate", FAIL,
     "ledgers/CS2/mutants/ (156 files); grader/test_project.py",
     "Command: .venv/bin/python tools/mutate_graders.py --unit CS2 --seeds 0-9 -> 'mutate_graders CS2: FAIL (154/156 killed)', rc=1 "
     f"({S}/mutate_graders_r10_final.txt). Survivors: r10_01_variance_ddof0_leaves_a_debug_print.py and "
     "r10_02_quantile_at_zero_leaves_a_debug_print.py. The 152 mutants at the pin all die ('PASS (152/152 killed)' "
     f"in {S}/mutate_graders.txt before the new mutants were added). Both survivors violate project.html:209 'The three classes never print or warn.'",
     FIX_PRINT),
    ("gate-run-graders", "gate", PASS, "course/modules/CS/CS2/grader/",
     "Command: tools/run_graders.py --unit CS2 --seeds 0-49 -> 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.2 s)', rc=0 "
     f"({S}/run_graders.txt). Also {S}/reference_0_49.txt: seeds_failed=0 of 50 via suite.py.", None),
    ("gate-check-projects", "gate", PASS, "tools/check_projects.py; course/modules/CS/CS2/project.html",
     "Command: tools/check_projects.py --unit CS2 -> 'check_projects CS2: PASS', rc=0 (check_projects.txt).", None),
    ("gate-check-dag", "gate", PASS, "tools/check_dag.py",
     "Command: tools/check_dag.py --unit CS2 -> 'check_dag CS2: PASS', rc=0 (check_dag.txt).", None),
    ("gate-check-pages", "gate", PASS, "course/modules/CS/CS2/",
     "Command: tools/check_pages.py --unit CS2 -> 'check_pages CS2: PASS', rc=0 (check_pages.txt).", None),
    ("gate-run-labs", "gate", PASS, "tests/labs/CS2/; project.html lab blocks",
     "Command: tools/run_labs.py --unit CS2 -> 'run_labs CS2: PASS (14/14)', rc=0 (run_labs.txt).", None),
    ("gate-page-smoke", "gate", PASS, "course/modules/CS/CS2/project.html",
     "Command: tools/page_smoke.py --unit CS2 --pages project.html -> 'page_smoke CS2: PASS', rc=0 (page_smoke_project.txt). "
     "tools/page_smoke.py:34-36 pastes the reference into the in-browser grader and requires every test to pass, so this covers the Pyodide run.", None),
    ("gate-ruff-mypy", "gate", PASS, "course/modules/CS/CS2, tests/labs/CS2, ledgers/CS2 (edited paths)",
     "ruff check and ruff format --check on the three paths: rc=0, '18 files already formatted' (ruff_final.txt). mypy --no-incremental: 'Success: no issues found in 385 source files', rc=0 (mypy_final.txt).", None),
    ("gate-verify-refs", "gate", PASS, "references/references.json",
     "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', rc=0. tools/verify_refs.py --unit CS2 (live, plain HTTP) -> 'live re-verification of CS2: 1 of 560 entries, 0 problems', rc=0 (verify_refs_unit_live.txt).", None),
    ("gate-collect-count", "gate", PASS, "course/modules/CS/CS2/grader/test_project.py; project.html Grading mode",
     f"suite.py reference 0-49 --collect: '175 tests collected' for all 50 seeds (collect_all_seeds.txt: 50 x 175). project.html:211 states 175 for seeds 0 to 49.", None),
    ("gate-pytest-relevant", "gate", PASS, "tests/test_memo_exemplars.py tests/test_docs_figures.py tests/test_page_checks.py tests/test_labs.py",
     "Command: .venv/bin/python -m pytest -q on those four modules -> rc=0 (pytest_slice.txt); pytest -q -k 'CS2 or cards or project_lab or grader' -> rc=0 (pytest_k.txt).", None),
    ("gate-local-pytest", "gate", PASS, "course/modules/CS/CS2/grader/test_project.py; project.html Running the suite locally",
     "suite.py reproduces project.html:256 (QF_SEED, pytest -q -p no:cacheprovider --assert=plain -W error test_project.py) in a temp workspace: reference 50/50 pass; Python 3.14.8, pytest 9.0.2 (project.html:257 matches).", None),
    ("labs-project-1", "2.5-lab", PASS, "course/modules/CS/CS2/project.html:53-146; tests/labs/CS2/lab-CS2-project-1.py",
     "lab_equal.py: code==twin True, expected==output True (15 expected lines). python -I -W error twin rc=0. Printed 'deque operations: 44 ... bound 4n = 48' equals project.html:144 and prose at 145 and 389. Step 12 window [1, 47, 61, 35] min 1 max 61 matches the printed rows.", None),
    ("labs-project-2", "2.5-lab", PASS, "course/modules/CS/CS2/project.html:148-189; tests/labs/CS2/lab-CS2-project-2.py",
     "lab_equal.py: page code equals twin except the two ___ blanks (the twin holds mean = mean + delta / count and m2 = m2 + delta * (x - mean)); expected==output True. Hand check: offsets sum 30, mean 3.75, S = 59.5, 59.5/7 = 8.5.", None),
    ("labs-project-3", "2.5-lab", PASS, "course/modules/CS/CS2/project.html:262-339; tests/labs/CS2/lab-CS2-project-3.py",
     "lab_equal.py: code==twin True; expected==output True (9 lines). Sum of the eleven values 110046.0 /11 = 10004.181818; 5.5 - 1.1 = 4.4, ceil 5; 5th smallest 10003.2 (sorted list hand check).", None),
    ("proj-prose-numbers", "2.2-numbers", PASS, "project.html lede, Inputs, Grading mode, time table, Labs 1-3 prose, exemplars",
     "Every number re-derived: 30 h (table 2+3+4+4+4+6+4+3=30); 175 checks (collect); 20-400 values, offsets 0/10,000/1,000,000, windows 2-30, eps 0.05/0.1/0.2 (instance.py:4-5, make_instance); ten probes (instance.py PROBES_FIXED + one); 0.2500004 and q=0.1 witnesses (test_project.py:879-914); Lab outputs 44/48, 8.5, 10004.181818, 8.313636, 10003.2, True.", None),
    ("proj-line145-amortized", "2.9-interpretation", PASS, "course/modules/CS/CS2/project.html:145",
     "Line 145: step 9 min 1 still in window at step 12 (window [1,47,61,35]); step 13 is not run; 44 <= 48; each value appended once per deque, at most one pop per element per deque, so count <= 4n holds. Matches lab output.", None),
    ("proj-line386-design-note", "2.6-spec / 2.9", PASS, "course/modules/CS/CS2/project.html:386 (design.md probe list, Exemplar B)",
     "Ten probes = instance.py PROBES_FIXED (0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1) plus round(rng.random(),3); eps 0.05/0.1/0.2 on streams of 1-8 values (test_sketch_rank_guarantee_on_short_streams); 0.3/0.5/0.9 at q 0, 0.25, 0.5, 0.75, 1 (test_sketch_rank_guarantee_at_wide_epsilon); 0.1 and 0.2500004 on 1..20 (test_sketch_rank_target_*); constant stream (test_sketch_constant_stream_returns_the_constant). All present.", None),
    ("proj-process-words", "2.9-banned", PASS, "project.html; grader/*.py; tests/labs/CS2/lab-CS2-project-*.py; cards.json",
     "grep -i for round, verifier, builder, ledger, reviewer, agent, fix, TODO, placeholder: only 'fixed' (ordinary English, 'a fixed twenty-value stream') matched in project.html; none in cards.json.", None),
    ("proj-rubric-observable", "2.6-rubric", PASS, "course/modules/CS/CS2/project.html:348-357 (rubric-memo, C1-C6, four levels)",
     "Read all 24 cells. Each descriptor is checkable (for example C4 level 4 names the arithmetic, 64-bit floats and the lab; C6 level 3 'names a lab output' is separated from level 2 'quotes no number' by whether a printed number is quoted). No vague descriptor found.", None),
    ("proj-rubric-calibration", "2.6-rubric", UNV, "course/modules/CS/CS2/project.html:362-390 (exemplar-a, exemplar-b; data-scores 1,1,2,1,1,1 and 4,4,4,4,4,4)",
     "Not blind. This round I read the exemplar annotation paragraphs (project.html:370-373, 382, 384, 388, 390) before scoring, so the blind calibration of VERIFIER_RULES 2.6 rubric item 2 cannot be claimed. Official scores are internally consistent with the annotations (A: 1,1,2,1,1,1; B: 4 x6), but that is not calibration.",
     "Run the calibration with a fresh verifier that has not read the exemplar annotations: score Exemplar A (project.html:365-374) and Exemplar B (project.html:376-391) from the rubric table (project.html:352-357) alone, record six scores each, and pass the row only if every criterion is within one level of the official scores."),
    ("proj-ladder-scope", "2.6-ladder", PASS, "course/modules/CS/CS2/project.html:40-190, 260-340, 400-406; curriculum/curriculum.json (CS2 project brief)",
     "Rung 1 is Lab 1 with annotated why-notes; Rung 2 is Lab 2 with an expected block; Rung 3 is the spec, matching the curriculum brief (Welford mean/variance, rolling min/max with monotonic deque, quantile sketch with rank guarantee, prove Welford, streamstats.py/proof.md/design.md, grading both). Rung 4 has two open extensions. Tier F, so the M-tier minimal-rung rule does not apply.", None),
    ("proj-notation", "2.4-notation", PASS, "notation/notation.json; project.html math spans",
     "notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q and macros (\\E, \\Var, ...). project.html uses only n, q, eps, delta, x-bar, S, m, M2, v, N (conventionally local per notation.json 'about') and raw \\bar, \\delta, \\sum, \\varepsilon, \\le, \\dots, \\frac, \\cdot. No registered symbol or macro is used with a different meaning. grep -c mathbb|\\R = 0.", None),
    ("proj-dag-concepts", "2.9-DAG", PASS, "project.html lede and rung-3 links; L09.html, L10.html, L11.html; concepts.html#mathematical-induction",
     "check_dag CS2 PASS. Links welford-algorithm (L09), monotonic-deque (L10), quantile-sketch (L11) and mathematical-induction resolve to definitions in those lessons and in course/concepts.html; all lie in the unit's closure.", None),
    ("proj-reading-citation", "2.1-citation", PASS, "project.html:408-414; references/references.json (cormen2022introduction)",
     "verify_refs --unit CS2 (live): 1 entry, 0 problems. The record (Introduction to Algorithms, 4th ed., MIT Press, 2022, ISBN 9780262046305) is re-resolved. The page gives no locator and attributes no step to it (project.html:413 'names no page or section'), so no attribution is read off the book.", None),
    ("proj-exemplar-b-claims", "2.4-math", PASS, "course/modules/CS/CS2/project.html:376-391 (exemplar B proof and design note)",
     "Re-derived: a = -delta/(n+1); sum (x_i - xbar_{n+1})^2 = S_n + n a^2 = S_n + n delta^2/(n+1)^2; new term (n delta/(n+1))^2; total S_n + n delta^2/(n+1) = S_n + delta (x_{n+1} - xbar_{n+1}). Hypotheses H1-H3 are cited where used. Base case S_1 = 0 correct. Exemplar B's 'S_n/(n-1)' is sample variance with denominator n-1.", None),
    ("proj-spec-completeness", "2.6-spec", PASS, "course/modules/CS/CS2/project.html Inputs, Required outputs, Constraints, Conventions, Named errors",
     "Read in full. Questions I would have had to ask: (1) must quantile(q) return one of the stored values? The spec defines correctness by the two rank inequalities only, and the grader accepts any v, so this is answered by the spec's own definition. (2) Are bools valid values? Constraints covers 'not a real number' with 'either an exception or the number it denotes', and the grader accepts both. No question remains that the page leaves unanswered.", None),
    ("proj-hours", "2.6-hours", PASS, "course/modules/CS/CS2/project.html:33, 233-241; course/modules/CS/CS2/index.html:data-hours-lessons; L01-L11 data-hours",
     "Table 2+3+4+4+4+6+4+3 = 30 (page 30). My own estimate: rung 1 1.5 h, rung 2 2 h, Welford 3.5 h, proof 3 h, deque 3 h, sketch 7 h, validation and property tests 4 h, note and self-assessment 4 h: 28 h, within 30% of 30. index.html data-hours-lessons=100 and the eleven L01-L11 declared hours sum to 100 (grep). 100 + 30 = 130, matching curriculum.json CS2 hours 130.", None),
    ("proj-named-conditions", "2.6-spec", PASS, "project.html:209 (Constraints, ten named conditions); grader/test_project.py must_raise calls",
     "Each of conditions (1)-(10) has a must_raise test: (1) 170-179, (2) 182, (3) 214-221, (4) 430-439, (5) 458-465, (6) 450-455, (7) 653-660, (8) 771-777, (9) 672-690, (10) 707-713. must_raise is used only for named conditions (grep).", None),
    ("proj-line195-inputs", "2.2-prose / 2.9", PASS, "course/modules/CS/CS2/project.html:195-198 (Inputs)",
     "Read: 20-400 finite values, one or six decimals, offsets 0/10,000/1,000,000, window 2-30, eps 0.05/0.1/0.2, ten probes, SIMULATED. Matches instance.py:4-5, 27-41.", None),
    ("grader-instance", "2.6-instance", PASS, "course/modules/CS/CS2/grader/instance.py",
     "Read in full (50 lines). make_instance is deterministic (test_instance_is_deterministic), every stream is 20-400 finite floats, labelled SIMULATED, ten probes. The invalid key names one of six kinds.", None),
    ("instance-docstring-counts", "2.2-numbers", PASS, "course/modules/CS/CS2/grader/instance.py:8-16",
     "naive_offsets.py (exact Fraction reference, close() rel 1e-9 abs 1e-9): naive variance fails 0 of 16 at offset 0, 22 of 23 at 10,000 (seed 41 passes), 11 of 11 at 1,000,000. Matches the docstring exactly. Reference Welford passes 50/50.", None),
    ("grader-reference", "2.6-autograder", PASS, "course/modules/CS/CS2/grader/reference.py",
     "Read in full (143 lines). Welford update and variance (ddof 0/1, TypeError otherwise), rolling deques, GK-style sketch with exact Fraction target max(1, ceil(q n - eps n)). guarantee_battery.py: 1500 random streams, 69,000 exact quantile checks plus monotonicity, 0 violations.", None),
    ("grader-starter", "2.6-autograder", PASS, "course/modules/CS/CS2/grader/starter.py",
     "Read in full. Every method raises NotImplementedError; suite.py on starter.py: 172 failed, 3 passed (the three passing checks do not call a method). Matches project.html:206.", None),
    ("grader-tests-rank", "2.6-autograder", PASS, "course/modules/CS/CS2/grader/test_project.py:783-915",
     "Read in full. Rank guarantee tests use Fraction inequalities; the two witness tests (879-914) have the exact targets stated in their docstrings (2 for q=0.1, 5 and the floor-based 4 for q=0.2500004), re-derived by hand.", None),
    ("grader-docstring-delta", "2.6-autograder", PASS, "course/modules/CS/CS2/grader/test_project.py:203-212, 241-261, 411-424",
     "Read the round-9-to-pin hunks. test_classes_never_print now runs 150 extra values (correct) but still misses variance(0) and quantile(0.0) (FAIL row gate-mutate-cs2). The infinite-input test (420) now requires both mean and variance non-finite, which matches project.html:209.", None),
    ("grader-messages-no-expected-value", "2.6-autograder", PASS, "course/modules/CS/CS2/grader/test_project.py (all pytest.fail and must_raise messages)",
     "Read every message. Each names the property and none prints the expected value (must_raise, refuse_or_correct, close-based fails).", None),
    ("grader-new-mutants", "2.6-mutation", PASS, "ledgers/CS2/mutants/r4v_01..03",
     "Covered by the gate run: all listed files are in the 154/156 kills (mutate_graders_r10_final.txt).", None),
    ("grader-mutant-r5v01", "2.6-mutation", PASS, "ledgers/CS2/mutants/r5v_01_sketch_compression_folds_maximum_into_predecessor.py",
     "Killed in the gate run (mutate_graders_r10_final.txt).", None),
    ("grader-mutant-v6-01", "2.6-mutation", PASS, "ledgers/CS2/mutants/v6_01_variance_default_ddof_is_population.py; test_project.py:203-212",
     "Killed in the gate run by test_welford_variance_default_ddof_is_sample.", None),
    ("grader-new-mutants-v6-02-04", "2.6-mutation", PASS, "ledgers/CS2/mutants/v6_02..v6_04",
     "All killed in the gate run (mutate_graders_r10_final.txt).", None),
    ("grader-new-mutants-r7v", "2.6-mutation", PASS, "ledgers/CS2/mutants/r7v_01..04", "All killed in the gate run.", None),
    ("grader-new-mutants-r8v", "2.6-mutation", PASS, "ledgers/CS2/mutants/r8v_01..03", "All killed in the gate run.", None),
    ("grader-alternatives", "2.6-autograder", PASS,
     f"{S}/alts/alt_r10_E, F, G, I, J (five new correct alternatives)",
     "suite.py on seeds 0-49: alt_r10_E_fsum_two_pass_welford 50/50; alt_r10_F_rolling_brute_window_list 50/50; alt_r10_G_sorted_list_sketch_linear_rank 50/50; alt_r10_I_sketch_cap_floor_without_plus_one 50/50 (exact cap without +1); alt_r10_J_welford_exact_fraction_state 50/50. Also the guarantee battery: 0 violations for each sketch alternative. (A candidate with target ceil(q n), no slack, FAILS 50/50; it is a student error and is recorded as r10_03, not an alternative.)", None),
    ("mut-survivors", "2.6-mutation", PASS, "ledgers/CS2/equivalent/ (d8_01, d8_02, d9_04)",
     "Not counted as faults: each passes seeds 0-9 and has 0 violations in 69,000 randomized exact guarantee checks (guarantee_battery.py, 1500 trials). project.html states the rank guarantee and no internal cap (project.html:218; Conventions 'the autograder does not test memory'), so a sketch that satisfies the guarantee violates no stated behaviour. The README's lemmas were read for the cap and bisect_left variants; the randomized check supports them.", None),
    ("equiv-m14_01", "2.4-math / 2.6-mutation", PASS, "ledgers/CS2/equivalent/rank_target_without_clamp.py",
     "Proof of exact equivalence: for target <= 1 the answer is the first stored value, because rank = g_1 >= 1 >= target. Removing max(1, .) therefore changes only targets <= 0, which return values[0] in both versions. Suite passes seeds 0-9.", None),
    ("instance-distinct-seeds", "2.6-instance", PASS, "course/modules/CS/CS2/grader/instance.py; ledgers/CS2/scripts/CS2-d-r10/instance_variety.py",
     "20 seeds (0,2,...,38): all valid; 20 distinct (mean, variance) pairs and 20 distinct sketch medians (instance_variety.py output).", None),
    ("gate-mutate-r7-new", "2.6-mutation", PASS, "ledgers/CS2/mutants/r7v_01..04", "Killed in the gate run.", None),
    ("grader-infinite-input", "2.6-autograder / 2.9-spec", PASS,
     "course/modules/CS/CS2/grader/test_project.py:411-424 (test_welford_infinite_input_gives_no_finite_answer)",
     "Round-9 FAIL is fixed: line 423 is now 'if math.isfinite(mean) or math.isfinite(var)', so the test requires both non-finite (project.html:209). Mutant r9v_01 is killed (gate run, test_welford_infinite_input_gives_no_finite_answer[inf], seed 0).", None),
    ("grader-classes-never-print", "2.6-autograder / 2.9-spec", FAIL,
     "course/modules/CS/CS2/grader/test_project.py:243-261 (test_classes_never_print); project.html:209 'The three classes never print or warn.'",
     "Round-9 hole fixed: r9v_02 (print on the 100th update) is killed by the 150-value tail. The check is still incomplete: it calls variance(1) and quantile(0.5) only. r10_01 (print inside variance(0)) and r10_02 (print inside quantile(0.0)) both survive seeds 0-9 (mutate_graders_r10_final.txt), and the page's sentence forbids both.",
     FIX_PRINT),
    ("grader-new-mutant-r9v03", "2.6-mutation", PASS, "ledgers/CS2/mutants/r9v_03_sketch_new_tuple_delta_drops_successor_delta.py",
     "Killed in the gate run by test_sketch_rank_guarantee_at_each_probe[4] (seed 5).", None),
    ("grader-alt-round9", "2.6-autograder", PASS, "ledgers/CS2/scripts/CS2-d-r9/alts/alt_r9_a_exact.py .. alt_r9_e_exact_block.py",
     "Re-run this round with suite.py on seeds 0-49: all five pass 50/50. (Other round-9 files in that folder, alt_r7_01..06 and alt_r8_01..04, were also run: all pass except alt_r7_06_r9path.py, which fails at import because it hard-codes /Users/billyribeiro/.fanout/wt/verifyB9-CS2-d/..., a removed checkout. It is not runnable and is not counted as an alternative.)", None),
    ("grader-fuzz-round9", "2.6-autograder", PASS, f"{S}/guarantee_battery.py (replaces the round-9 r9_fuzz_guarantee.py rerun)",
     "guarantee_battery.py reference.py 1500 7: trials 1500, quantile checks 69000, violations 0 (round-9 fuzz not rerun; this battery supersedes it for this round).", None),
    ("cards-automated", "2.7-cards", PASS, "course/modules/CS/CS2/cards.json",
     f"{S}/cards_check.py: 220 entries, 220 unique ids, 0 duplicate fronts, 0 duplicate backs, every entry has the keys id, lesson, front, back, grade (+ basis for C), 153 T / 67 C, every C card has a basis, no T card has one, every lesson file exists.", None),
    ("cards-sample", "2.7-cards", PASS, "course/modules/CS/CS2/cards.json: every 10th card (ids at indices 0, 10, ..., 210; 22 cards)",
     "Checked against the current lesson text (plain-text extraction, ledgers/CS2/scripts/CS2-d-r10/text_*.txt): c001 (L01 Def 1.1), c011 (Example 2.1: 3n+7 <= 10n for n>=1), c021 (Cor 2.3), c031 (Prop 1.3b), c041 (Def 1.1), c051 (Prop 3.2), c061 (Prop 2.4), c072 (Def 1.1 BFS), c082 (Prop 2.3), c092 (Cor 3.4 induction on i+j), c102 (Lab 1 Part A float refusal printed line 394), c112 (Prop 1.3 hypotheses), c122 (Cor 2.3 six operations), c132 (Thm 2.4), c142 (Def 2.1 k_h formula at L11.html:75-76), c152 (Def 1.2; 500/550/450 arithmetic), c173 (Prop 1.6 proof), c183 (Lab 1 Part A '53 single right-right'), c205 (M3 solution: k_0=20, 20 items, weight 40), c215 (L05 line 42 heavy-child rule), c220 (Section 1), c223 (Def 1.1 L08), c224-level sampling complete. Each consistent. c024 is the exception (row cards-c024).", None),
    ("cards-changed-delta", "2.7-cards", PASS,
     "cards.json CS2-c038, c095, c136, c158, c228, c229, c230, c231 (changed or new since the round-9 pin, except c024)",
     "c038: 205 = 107+98 and 602 = 241+361 at N=16 (lab output, text_L03 line 272); misconception 3 named. c095: Example 2.4 and P3 (first failure at amount 6), correct. c136: Lab 1 windows 1,2,5,13,30 all 200 positions, totals 396-399 < 400 (text_L10). c158: lab-CS2-L02 prints 'successful total probes=1275, average=25.5000' (lab_L02_twin.out). c228: difference (n-2m+1)/(2m), positive exactly when n >= 2m (L02 R3). c229: heap 8517+10623=19140, sorted 3742+17663=21405 at N=256. c230: R2 proves {1,c} optimal for every a >= 0; the argument uses two denominations. c231: totals 396-399 for both deques, Theorem 2.4 bound 2n.", None),
    ("cards-c024", "2.7-cards", FAIL, "course/modules/CS/CS2/cards.json: CS2-c024 (L02, grade T), front 'Does an absent key cost less, because there is nothing to find?'",
     "The back answers 'No.' and gives only the absent cost alpha = n/m. The lesson (L02 Proposition 2.2 and R3, text_L02 lines 214 and 158) says the absent key costs less than a successful search when n < 2m - 1. Numerically: n=16, m=64 gives absent 0.2500 against successful 1.1172, so an absent key does cost less. The 'No.' is false in general and contradicts the page's own R3 result.",
     "Replace the back of CS2-c024 with: 'Not always. Under Assumption 2.1 an unsuccessful search costs alpha = n/m (Proposition 2.2(a)). That is below the successful average 1 + (n - 1)/(2m) when n < 2m - 1, equal at n = 2m - 1, and above it when n >= 2m (Problem R3).' Grade T stays."),
    ("cards-c155", "2.7-cards", PASS, "cards.json CS2-c155; lab-CS2-L02 output",
     "lab_L02_twin.out: successful average 2.0078 at n=128 and 3.0156 at n=256; model 1 + (n-1)/128 = 1.9922 and 2.9922 (Proposition 2.2(c)). Card matches.", None),
    ("cards-c035", "2.7-cards", PASS, "cards.json CS2-c035; lab-CS2-L03 rows (text_L03 lines 181-206)",
     "Sorted-list move ratios per doubling: 2.8980, 3.5282, 4.5050, 3.9129, 3.7118, 4.1119, 4.0287, 4.0316. Largest is 4.5050 at N=128 (4514/1002 = 4.5050), as the card says.", None),
    ("cards-c174", "2.7-cards", PASS, "cards.json CS2-c174; lab-CS2-L03 rows",
     "Heap move ratios per doubling: 2.5734, 2.3778, 2.2331, 2.1535, 1.9858, 2.0100, 2.0722, 2.0687. Smallest is 1.9858 at N=512 (21095/10623 = 1.9859 at N=512 vs N=256 as the card says), matching the card.", None),
    ("cards-c227", "2.7-cards", PASS, "cards.json CS2-c227 (L05, T); L05 Section 1 text",
     "L05 line 22: 'Every key in the left subtree of a node is smaller than the node's key, and every key in the right subtree is larger.' Card matches.", None),
    ("cards-lab-numbers", "2.7-cards", PASS, "cards.json grade C (67 cards); lab outputs of the lessons",
     "Every C-card number is a verbatim substring of its lesson (cards_check.py: 0 missing). C cards re-checked against twin output this round: c035, c038, c136, c155, c158, c174, c229 (and c183 53, c215 Lab 1 Part A rule, c102 printed line). The rest are covered by the mechanical check, not by reading the lab output one by one.", None),
    ("cards-duplicates", "2.7-cards", PASS, "course/modules/CS/CS2/cards.json (full pairwise scan)",
     "cards_check.py: 26 front pairs at difflib ratio >= 0.8, each asking a different fact (for example c115 price level created vs c187 removed; c182 vs c183 vs c185 rotation kinds; c201 vs c202 excess vs deficit). No duplicate fronts or backs.", None),
    ("cards-full-number-scan", "2.7-cards", PASS, "course/modules/CS/CS2/cards.json (all 220 cards)",
     "cards_check.py: every number on every card (after stripping trailing commas) appears verbatim in its lesson text: 0 misses.", None),
    ("cards-count-observation", "2.7-cards", PASS, "course/modules/CS/CS2/cards.json (220 cards: L01 14, L02 22, L03 22, L04 20, L05 24, L06 15, L07 22, L08 26, L09 17, L10 14, L11 24)",
     "Observation only: 153 T and 67 C. The round-9 count (216) is superseded.", None),
    ("cards-changed-c025-c087-c095", "2.7-cards", PASS, "cards.json CS2-c025, CS2-c087, CS2-c095",
     "c025: at fixed m, 1 + (n-1)/(2m) to 1 + (2n-1)/(2m) differ by n/(2m); at n=128 to 256 with m=64 the increase is exactly 1 (checked). c087: L07 Theorem 2.2 hypotheses (D finite nonempty set of positive integers; a nonnegative integer) match the card's basis (text_L07 lines 29-31). c095: correct (see cards-changed-delta).", None),
    ("cards-c033", "2.7-cards", PASS, "cards.json CS2-c033; text_L03 Prop 1.6 and Prop 1.5 hold run",
     "Hold run of N initial pushes, N holds, N drain pops (text_L03 line 37); Prop 1.6: at most 2N(N+1) sorted-list moves. Card matches.", None),
    ("cards-c215", "2.7-cards", PASS, "cards.json CS2-c215 (L05, C); L05.html line 42 and Part A",
     "Heavy-child rule text (L05 line 42): heavy child is left child for +2, right for -2; same sign or zero factor gives a single rotation, opposite sign gives a double rotation. Lab 1 Part A check 'every check True after each of the 500 insertions'. Card matches.", None),
]

fragment = {
    "unit": "CS2",
    "slice": "d",
    "round": 10,
    "verifier": "independent verifier (Haiku), round 10; did not build CS2",
    "pin": "47a36d8c78633793ccc762ae19dcd5e19b780d19",
    "base": "1e272e5a641f18412703b37778a44db6f7391a69",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD10-CS2-d",
    "scratch": S,
    "verified_at": "2026-11-05T09:50:00+00:00",
    "verdict": "FAIL",
    "rows": [
        {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev,
         **({"fix": fix} if status != PASS else {})}
        for rid, check, status, loc, ev, fix in [
            (r[0], r[1], r[2], r[3], r[4], r[5] if len(r) > 5 else None) for r in rows
        ]
    ],
    "mutants": [
        {"id": "r10_01_variance_ddof0_leaves_a_debug_print.py",
         "description": "Debug print left in variance(0): prints on every population-variance call, which the no-print check never makes.",
         "killed_by": None},
        {"id": "r10_02_quantile_at_zero_leaves_a_debug_print.py",
         "description": "Debug print left in quantile(0.0): prints when the minimum is asked for, a call the no-print check never makes.",
         "killed_by": None},
        {"id": "r10_03_rank_target_drops_the_epsilon_slack.py",
         "description": "Rank target uses ceil(q n) and drops the epsilon slack, so the answer is one-sided on the rank guarantee.",
         "killed_by": "test_sketch_rank_guarantee_at_each_probe[3] (seed 0)"},
        {"id": "r10_04_compress_cap_computed_in_floats.py",
         "description": "Compress cap computed in 64-bit floats, so 2 eps n rounds up across an integer and the cap is one too large.",
         "killed_by": "test_sketch_rank_guarantee_at_wide_epsilon[0.3] (seed 0)"},
    ],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-9 fragment (/Users/billyribeiro/.fanout/frags/D-CS2-d.round9.json) used as context only; none of its PASS rows were carried. Every row was re-run or re-derived this round; the ids are kept.",
        "Delta since the round-9 pin 1e272e5a: project.html:387 (sketch note domain sentence, checked against spec line 209), test_project.py (print test extended, infinite-input test changed: both checked), cards.json (c024, c038, c095, c136, c158 changed; c228-c231 new; read in full as hunks).",
        "Not blind rubric calibration: see proj-rubric-calibration (UNVERIFIABLE). The orchestrator must run a fresh calibration verifier.",
        "The surviving prints (r10_01, r10_02) mean the grader does not test 'never print' on every method. Fix in grader-classes-never-print. The patched copy is in the scratch folder and passes reference and five alternatives on seeds 0-9.",
        "Script hygiene: ledgers/CS2/scripts/CS2-d-r9/alts/alt_r7_06_r9path.py hard-codes a removed checkout path (/Users/billyribeiro/.fanout/wt/verifyB9-CS2-d/...). It cannot be re-run; repair it or remove it.",
        "The equivalent/ files are not in mutants/, so the gate does not count them. Their guarantee-preservation is evidenced by guarantee_battery.py (0 violations in 69,000 checks each); the three sketch variants are not formal proofs of equivalence, only correct alternatives. The exact-equivalence proof is given only for rank_target_without_clamp.py.",
        "The constant-stream check uses exact variance == 0.0 on 5.0 (test_welford_constant_stream_has_zero_variance). The spec states a 1e-9 tolerance. No correct alternative tested fails it on that input, so it is recorded as an observation, not a row.",
        "Question the spec leaves to a student: none that blocks the build (see proj-spec-completeness).",
        "Not checked: the in-browser saving of the learner's code (project.html:249, 'saved in this browser as you type'); the 500-800-word length of design.md (not graded); the rubric calibration (not blind, see above); the Exemplar A/B scores beyond their annotations; cards outside the 22-card sample and the changed set were checked only by mechanical checks.",
    ],
    "summary": ("CS2 slice d, round 10: FAIL. Gates PASS: check_pages, check_dag, check_projects, run_graders (50/50), run_labs (14/14), "
                "page_smoke (project), ruff, mypy, verify_refs (offline and live CS2), collect 175 on seeds 0-49, relevant pytest, local suite 50/50. "
                "FAILs: (1) mutate_graders 154/156 (exit 1): debug prints in variance(0) and quantile(0.0) survive, violating project.html:209; "
                "(2) card CS2-c024 says 'No' to 'does an absent key cost less', false for n < 2m-1. UNVERIFIABLE: the rubric calibration is not blind. "
                "Five new correct alternatives pass 50/50; the round-9 two-hole fixes (infinite input, 100th-update print) are confirmed."),
}

problems = None
import sys
sys.path.insert(0, "tools")
import ledger  # noqa: E402

problems = ledger.validate(fragment, "CS2-d")
print("validate:", problems)
counts = {s: sum(1 for r in fragment["rows"] if r["status"] == s) for s in (PASS, FAIL, UNV)}
killed = sum(1 for m in fragment["mutants"] if m["killed_by"])
print("rows", len(fragment["rows"]), counts, "mutants killed", killed, "of", len(fragment["mutants"]))
Path("ledgers/CS2/CS2-d.json").write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("written ledgers/CS2/CS2-d.json")
