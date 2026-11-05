"""Round-9 builder for ledgers/CS2/CS2-d.json (slice d). Rows carry their evidence strings; no verdict is asserted
by hand: the verdict is PASS only when every row is PASS (checked below and by tools/ledger.py)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/CS2/scripts/CS2-d-r9"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates
row("gate-mutate-cs2", "gate", "ledgers/CS2/mutants/ (142 files); course/modules/CS/CS2/grader/test_project.py", "FAIL",
    f"Command: .venv/bin/python tools/mutate_graders.py --unit CS2 --seeds 0-9 -> 'mutate_graders CS2: FAIL (140/142 killed)', exit 1 ({S}/r9_mutate_all.txt). The 139 files that existed at the pin were run first with the same command and gave 'PASS (139/139 killed)', exit 0. The two survivors are r9v_01 and r9v_02 (rows grader-infinite-input and grader-classes-never-print).",
    "Apply the two grader test fixes in rows grader-infinite-input and grader-classes-never-print, then re-run tools/mutate_graders.py --unit CS2 --seeds 0-9; expect 142/142 killed and exit 0.")
row("gate-run-graders", "gate", "course/modules/CS/CS2/grader/", "PASS",
    f"Command: .venv/bin/python tools/run_graders.py --unit CS2 --seeds 0-49 -> 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 ({S}/r9_run_graders.txt).")
row("gate-check-projects", "gate", "tools/check_projects.py; course/modules/CS/CS2/project.html", "PASS",
    f"Command: .venv/bin/python tools/check_projects.py --unit CS2 -> 'check_projects CS2: PASS', exit 0 ({S}/r9_check_projects.txt).")
row("gate-check-dag", "gate", "tools/check_dag.py", "PASS",
    f"Command: .venv/bin/python tools/check_dag.py --unit CS2 -> 'check_dag CS2: PASS', exit 0 ({S}/r9_check_dag.txt).")
row("gate-check-pages", "gate", "course/modules/CS/CS2/", "PASS",
    f"Command: .venv/bin/python tools/check_pages.py --unit CS2 -> 'check_pages CS2: PASS', exit 0 ({S}/r9_check_pages.txt).")
row("gate-run-labs", "gate", "tests/labs/CS2/; project.html lab blocks", "PASS",
    f"Command: .venv/bin/python tools/run_labs.py --unit CS2 -> 'run_labs CS2: PASS (14/14)', exit 0 ({S}/r9_run_labs.txt).")
row("gate-page-smoke", "gate", "course/modules/CS/CS2/project.html", "PASS",
    f"Command: .venv/bin/python tools/page_smoke.py --unit CS2 --pages project (run alone) -> 'page_smoke CS2: PASS', 'in-browser grader: All 175 tests pass' on seed 53492232, exit 0 ({S}/r9_page_smoke_project.txt). Pyodide pin 314.0.7 (tools/vendor_spec.yaml:53-54) is Python 3.14; pytest 9.0.2 (LOCK.json) matches project.html:257.")
row("gate-ruff-mypy", "gate", "course/modules/CS/CS2, tests/labs/CS2, grader", "PASS",
    f"ruff check: 'All checks passed!' ({S}/r9_ruff_check.txt); ruff format --check: '18 files already formatted' ({S}/r9_ruff_format.txt); mypy --no-incremental on grader and labs: 'Success: no issues found in 18 source files', exit 0 ({S}/r9_mypy.txt).")
row("gate-verify-refs", "gate", "references/references.json", "PASS",
    f"Command: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}/r9_verify_refs_offline.txt). The live run was not performed. The one record this slice uses was checked with plain curl (row proj-reading-citation).")
row("gate-collect-count", "gate", "course/modules/CS/CS2/grader/test_project.py; project.html Grading mode", "PASS",
    f"Script {S}/r9_suite_runner.py with --collect (pytest --collect-only, -W error, --assert=plain) on reference.py as streamstats.py, seeds 0-49: 'collected counts: [175]' ({S}/r9_collect_reference_0_49.txt). project.html:211 states 175.")
row("gate-pytest-relevant", "gate", "tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py tests/test_page_smoke.py", "PASS",
    f"Command: .venv/bin/pytest -q -p no:cacheprovider on those five files -> 'EXIT 0', dots only ({S}/r9_pytest_relevant.txt).")
row("gate-local-pytest", "gate", "course/modules/CS/CS2/grader/test_project.py; project.html Running the suite locally", "PASS",
    f"{S}/r9_suite_runner.py reference.py 0-49 with the project.html:256 flags (pytest -q -p no:cacheprovider --assert=plain -W error; Python 3.14.8, pytest 9.0.2): 50/50 seeds all-pass ({S}/r9_reference_pass_0_49_local.txt).")

# ---- labs
row("labs-project-1", "2.5-lab", "course/modules/CS/CS2/project.html:53-146; tests/labs/CS2/lab-CS2-project-1.py", "PASS",
    f"{S}/r9_labcheck.py: twin under python -I -W error exit 0, empty stderr; page code equals twin (0 differing lines); expected block equals output ({S}/r9_labcheck.out.txt). Interpretation re-derived: step 9's minimum 1 (index 8) is still in the window at step 12 and leaves at step 13; 44 <= 48; every-step agreement True.")
row("labs-project-2", "2.5-lab", "course/modules/CS/CS2/project.html:148-189; tests/labs/CS2/lab-CS2-project-2.py", "PASS",
    f"{S}/r9_labcheck.py: twin exit 0 under -I -W error; page code equals twin except the two blanks 'mean = ___' and 'm2 = ___' (class completion convention, architect ruling 11); expected 'count 8 / mean 1000003.750000 / sample variance 8.500000' equals output. Recomputed: offsets 2,5,1,4,9,3,6,0 have mean 3.75 and S = 172 - 8*3.75^2 = 59.5, so the sample variance is 59.5/7 = 8.5.")
row("labs-project-3", "2.5-lab", "course/modules/CS/CS2/project.html:262-339; tests/labs/CS2/lab-CS2-project-3.py", "PASS",
    f"{S}/r9_labcheck.py: twin exit 0 under -I -W error; page code equals twin; expected equals output. Interpretation: 5.5 - 1.1 = 4.4, ceil 5; 5th smallest 10003.2 (sorted list recomputed by hand); exact mean 110046.0/11 = 10004.181818 (sum recomputed).")

# ---- project prose, math, structure
row("proj-prose-numbers", "2.2-numbers", "project.html lede, Inputs, Grading mode, time table, Labs 1-3 interpretations, exemplars", "PASS",
    f"Every number re-derived: 20-400 values, window 2-30, epsilon {{0.05,0.1,0.2}}, ten probes (instance.py PROBES_FIXED nine plus one seeded), 175 checks ({S}/r9_collect_reference_0_49.txt), hours 2+3+4+4+4+6+4+3 = 30, lesson hours 100 (8+9+10+10+9+9+10+10+10+8+7) so 100+30 = 130; Lab 1 44 <= 48; Lab 3 mean 10004.181818 and variance 8.313636; ceil(q n - eps n) witnesses; the Inputs sentence changed this round is covered by row proj-line195-inputs.")
row("proj-line145-amortized", "2.9-interpretation", "course/modules/CS/CS2/project.html:145", "PASS",
    "Value 1 is pushed at step 9 (index 8). At step 13 the window holds indices 9-12, so index 8 leaves there (printed series, project.html:139-142). The lab runs twelve steps only, so the sentence 'which this lab does not run' is accurate. Line 145 is byte-identical to the round-8 pin; re-read this round.")
row("proj-line386-design-note", "2.6-spec / 2.9", "course/modules/CS/CS2/project.html:386 (design.md probe list)", "PASS",
    "Each claim checked against test_project.py: ten probes = nine fixed plus one seeded (instance.py:27,41); streams of one to eight values at eps 0.05, 0.1, 0.2 (test_project.py:829-845); sorted streams (815-826); repeated values (847-858); eps 0.3, 0.5, 0.9 at q 0, 0.25, 0.5, 0.75, 1 (861-873); fixed twenty-value stream at q = 0.1 and q = 0.2500004 (876-911); constant stream (802-806). Rank target at least 1 is in Conventions (project.html:219).")
row("proj-process-words", "2.9-banned", "project.html; grader/*.py; tests/labs/CS2/lab-CS2-project-*.py; cards.json", "PASS",
    "Scan (python, round 9) for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, roughly half, about 6%, historically, in this section, in this lesson, let us, we will, ellipsis: no hit. Learner-text scan for verifier, builder, architect, ruling, round N, mutant, draft, placeholder: no hit.")
row("proj-rubric-observable", "2.6-rubric", "course/modules/CS/CS2/project.html:348-357 (rubric-memo, C1-C6, four levels each)", "PASS",
    "All 24 level descriptors read this round. Each names a checkable element (numbered hypotheses before the statement, base case at one value, each algebra line justified, named arithmetic, probe set and streams, a printed lab count or measured error). None is vague.")
row("proj-rubric-calibration", "2.6-rubric", "course/modules/CS/CS2/project.html:362-390 (exemplar-a, exemplar-b; data-scores 1,1,2,1,1,1 and 4,4,4,4,4,4)", "UNVERIFIABLE",
    "Not blind. This session read the exemplar annotation paragraphs (project.html:370-373, 382, 384, 388, 390) before scoring, so the calibration required by VERIFIER_RULES 2.6 rubric item 2 cannot be claimed. Round 8 was also not blind. Rubric-only scores recorded in round 8 for reference, not as this round's calibration: A within one level, B within one level.",
    "Run the calibration with a fresh verifier that has not read the exemplar annotations: score Exemplar A (project.html:365-374) and Exemplar B (project.html:376-391) from the rubric table (project.html:352-357) alone, record six scores each, and pass the row only if every criterion is within one level of data-scores (A 1,1,2,1,1,1; B 4,4,4,4,4,4). Do not edit the page to make the scores match.")
row("proj-ladder-scope", "2.6-ladder", "course/modules/CS/CS2/project.html:40-190, 260-340, 400-406", "PASS",
    "Rung 1 is Lab 1, fully solved with why notes at lines 80, 82, 88, 94, 100. Rung 2 is Lab 2, class lab completion with an expected block. Rung 3 is the spec, grader and write-up, matching curriculum/01-foundations.yaml:442-449 (streamstats.py, proof.md, design.md; grading both; 'cumulative over every value seen'). Rung 4 is open-ended stretch.")
row("proj-notation", "2.4-notation", "notation/notation.json; project.html math spans (34)", "PASS",
    f"{S}/r9_notation.py ({S}/r9_notation.out.txt): 34 math spans; macros used are plain TeX only (no registered macro misused); single-letter symbols S, a, i, n, q, x are program-local; registry symbols T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, Q do not occur on the page. cards.json: no registered symbol occurs; R^-(v) (cards c140, c141, c147, c148, c152, c217) is not registered, so it does not collide.")
row("proj-dag-concepts", "2.9-DAG", "project.html lede and rung-3 links; L09-L11; ../../../concepts.html#mathematical-induction", "PASS",
    f"{S}/r9_check_dag.txt PASS. welford-algorithm (L09), monotonic-deque (L10), quantile-sketch (L11) are in-unit and earlier. mathematical-induction is defined in course/modules/M/M1/L06.html (dfn id def-mathematical-induction, line 60) and CS2 prereqs are ['CS1','M1'] (curriculum/curriculum.json).")
row("proj-reading-citation", "2.1-citation", "project.html:408-414; references/references.json:5962 (cormen2022introduction)", "PASS",
    f"Plain curl: 'curl -s https://openlibrary.org/books/OL34192801M.json' returned HTTP 200 with title 'Introduction to Algorithms, Fourth Edition', publish year 2022, publisher MIT Press, ISBN-13 9780262046305 ({S}/r9_curl_openlibrary.txt, {S}/r9_openlibrary_OL34192801M.json), matching the registry. The page gives no locator and attributes no step to the book (project.html:413).")
row("proj-exemplar-b-claims", "2.4-math", "project.html:376-391 (exemplar B proof and design note)", "PASS",
    "Re-derived by hand: a = -delta/(n+1); sum over i<=n of (x_i - xbar_{n+1})^2 = S_n + n a^2 (middle term zero by the definition of xbar_n); x_{n+1} - xbar_{n+1} = n delta/(n+1); S_{n+1} = S_n + n delta^2/(n+1) = S_n + delta (x_{n+1} - xbar_{n+1}); base S_1 = 0; sample variance S_n/(n-1). Lab 1 44 <= 48 and Lab 3 agreement are the printed evidence the page cites (r9_labcheck.out.txt).")
row("proj-spec-completeness", "2.6-spec", "course/modules/CS/CS2/project.html Inputs, Required outputs, Constraints, Conventions, Named errors", "PASS",
    "Questions a competent student would ask, each answered on the page: default ddof (signature variance(ddof: int = 1)); None and strings (Constraints); which conditions raise ValueError (the ten named conditions); rank target (Conventions, Exact counts); probe count and stream sizes (Inputs); monotonicity (Conventions); memory not tested (Conventions). No unanswered question found. Estimated effort, my own: 22 h (see proj-hours).")
row("proj-hours", "2.6-hours", "project.html:227-246 (table id hours); course/modules/CS/CS2/index.html:29 and L01-L11 data-hours", "PASS",
    "Table sums to 30 (2+3+4+4+4+6+4+3). My independent central estimate: rung 1 1.5 h; rung 2 1 h; Welford accumulator and tests 3 h; Welford proof 3 h; deque min/max and tests 3 h; quantile sketch and guarantee tests 6 h; named-condition validation 2 h; design note and self-assessment 2.5 h; total 22 h, which is 27% below 30 h and inside the 30% bound. Hub data-hours-lessons=100, data-hours-project=30 (index.html:29); lesson data-hours 8,9,10,10,9,9,10,10,10,8,7 sum to 100.")
row("proj-named-conditions", "2.6-spec", "project.html:209 (Constraints, ten named conditions); grader/test_project.py must_raise call sites", "PASS",
    "Ten conditions, each with a test: (1) test_project.py:170-179; (2) :182-185; (3) :214-217; (4) :427-436 incl. False at :435; (5) :455-458; (6) :447-452 and :924; (7) :650-666 incl. booleans :655-657 and infinities/NaN; (8) :768-770; (9) :669-687; (10) :704-710. Every must_raise call maps to one of the ten.")
row("proj-line195-inputs", "2.2-prose / 2.9", "course/modules/CS/CS2/project.html:195-198 (Inputs, changed since the round-8 pin)", "PASS",
    "Changed sentence: 'The window, the parameter of RollingMinMax defined under Conventions below, is an integer from 2 to 30. The quantile sketch's epsilon, which the rank guarantee under Conventions below uses, is 0.05, 0.1 or 0.2.' Both values match instance.py:30-41 (window randint(2,30), EPSILONS) and Conventions (project.html:217-218). No new number or banned phrase.")

# ---- grader
row("grader-instance", "2.6-instance", "course/modules/CS/CS2/grader/instance.py", "PASS",
    "Read in full. Deterministic (test_instance_is_deterministic). Lengths 20-400, offsets {0, 1e4, 1e6}, decimals {1, 6}, windows 2-30, epsilons {0.05, 0.1, 0.2}, ten probes, one invalid kind per seed among six named conditions. Label 'SIMULATED stream {seed}'.")
row("instance-docstring-counts", "2.2-numbers", "course/modules/CS/CS2/grader/instance.py:8-16", "PASS",
    f"{S}/r9_instances.py ({S}/r9_instances.out.txt): naive formula (s += x, ss += x*x, mean = s/n, (ss - n mean^2)/(n-1)) against the exact Fraction value over seeds 0-49: offset 0: 16 seeds, 0 fail; offset 10,000: 23 seeds, 22 fail, seed 41 passes; offset 1,000,000: 11 seeds, 11 fail. The docstring's counts and exception match exactly.")
row("grader-reference", "2.6-autograder", "course/modules/CS/CS2/grader/reference.py", "PASS",
    "Read in full (143 lines). run_graders 50/50 (r9_run_graders.txt); local pytest flags 50/50 (r9_reference_pass_0_49_local.txt). Docstring claims checked by r9_fuzz_guarantee.py: g + delta <= floor(2 eps n) + 1 after every add (0 violations in 47,247 steps) and the rank copy invariant (0 violations).")
row("grader-starter", "2.6-autograder", "course/modules/CS/CS2/grader/starter.py", "PASS",
    f"Every method raises NotImplementedError (read in full). Suite on the starter, seeds 0-4: 0/5 pass, failing tests include test_invalid_case_is_refused and test_welford_count_starts_at_zero ({S}/r9_starter_0_4.txt).")
row("grader-tests-rank", "2.6-autograder", "course/modules/CS/CS2/grader/test_project.py:876-911", "PASS",
    "Witness 1 (q 0.1, n 20, eps 0.05): exact target ceil(1.0000000000000000555) = 2; float target 1 (recomputed: python gives math.ceil(0.1*20 - 0.05*20) = 1, Fraction gives 2). Witness 2 (q 0.2500004): qn = 5.000008, target 5; q rounded to 0.25 gives 4 and needs at_or_below >= 4.000008. Both docstrings match.")
row("grader-docstring-delta", "2.6-autograder", "course/modules/CS/CS2/grader/test_project.py:203-212; project.html:211", "PASS",
    "test_welford_variance_default_ddof_is_sample matches the grading-mode text on project.html:211 ('the default of variance(), which is ddof 1 ... on two values').")
row("grader-messages-no-expected-value", "2.6-autograder", "course/modules/CS/CS2/grader/test_project.py (all pytest.fail and must_raise messages)", "PASS",
    "Every message read. Each prints a property name, the input under test, or the learner's own return value. None prints an expected answer.")
row("grader-new-mutants", "2.6-mutation", "ledgers/CS2/mutants/r4v_01..03", "PASS",
    f"Killed in the round-9 run ({S}/r9_mutate_all.txt): r4v_01, r4v_02, r4v_03 each KILLED.")
row("grader-mutant-r5v01", "2.6-mutation", "ledgers/CS2/mutants/r5v_01_sketch_compression_folds_maximum_into_predecessor.py", "PASS",
    f"KILLED in {S}/r9_mutate_all.txt.")
row("grader-mutant-v6-01", "2.6-mutation", "ledgers/CS2/mutants/v6_01_variance_default_ddof_is_population.py; test_project.py:203-212", "PASS",
    f"KILLED by test_welford_variance_default_ddof_is_sample ({S}/r9_mutate_all.txt).")
row("grader-new-mutants-v6-02-04", "2.6-mutation", "ledgers/CS2/mutants/v6_02..v6_04", "PASS",
    f"All KILLED in {S}/r9_mutate_all.txt.")
row("grader-new-mutants-r7v", "2.6-mutation", "ledgers/CS2/mutants/r7v_01..04", "PASS",
    f"All KILLED in {S}/r9_mutate_all.txt.")
row("grader-new-mutants-r8v", "2.6-mutation", "ledgers/CS2/mutants/r8v_01..03", "PASS",
    f"All KILLED in {S}/r9_mutate_all.txt (r8v_01 mean floor division; r8v_02 mean rounded to six places; r8v_03 expiry by count).")
row("grader-alternatives", "2.6-autograder", "ledgers/CS2/scripts/CS2-d-r8/cands/alt_r8_a..f.py (round 8, six); ledgers/CS2/scripts/CS2-d-r9/alts/alt_r9_a..e.py (round 9, five)", "PASS",
    f"Round 9: five new full implementations of different style (exact Fraction state; store-all two-pass fsum with lazy-sorted sketch; (n-1)/n delta-squared Welford with list-based monotonic deque and binary-search sketch; standard Welford with sorted-window rolling and Greenwald-Khanna style left-to-right compression; exact sorted blocks). Each passes the suite on seeds 0-49: 50/50 ({S}/r9_alternatives_seeds0_49.txt). Round-8 six remain as recorded in the round-8 fragment.")
row("mut-survivors", "2.6-mutation", "ledgers/CS2/equivalent/ (d8_01, d8_02, d9_04)", "PASS",
    f"Re-run this round: each is a correct implementation, so it is not a fault. Randomized guarantee check: 27,300 probes each (5 stream kinds, 300 streams, eps {{0.05,0.1,0.2,0.3,0.5,0.9,0.01}}, 13 probe q values), 0 violations ({S}/r9_fuzz_guarantee.out.txt). Argument: ledgers/CS2/equivalent/README.md Lemmas 0 and 1 (copy invariant), re-read this round.")
row("equiv-m14_01", "2.4-math / 2.6-mutation", "ledgers/CS2/equivalent/rank_target_without_clamp.py", "PASS",
    "Argument re-derived: stored tuples have g >= 1, so the first running rank is >= 1; if the unclamped target is below 1 both versions return values[0]; otherwise the two targets are equal. Randomized check: 27,300 probes, 0 violations ({S}/r9_fuzz_guarantee.out.txt).")
row("instance-distinct-seeds", "2.6-instance", "course/modules/CS/CS2/grader/instance.py", "PASS",
    f"Seeds 0-19 (sample of 20): all 20 instances valid; 20 distinct (n, window, eps, exact sample variance) tuples; 20 distinct exact means ({S}/r9_instances.out.txt). The answers change, not only the labels.")
row("gate-mutate-r7-new", "2.6-mutation", "ledgers/CS2/mutants/r7v_01..04", "PASS",
    f"All four KILLED in the round-9 run ({S}/r9_mutate_all.txt).")

# ---- grader holes found this round
row("grader-infinite-input", "2.6-autograder / 2.9-spec", "course/modules/CS/CS2/grader/test_project.py:408-421 (test_welford_infinite_input_gives_no_finite_answer); project.html:209", "FAIL",
    "project.html:209: 'For an infinite value passed to WelfordAccumulator.update, the call raises, or the mean and the sample variance that follow are not finite numbers.' The test fails only when the mean and the variance are both finite (test_project.py:420, 'if math.isfinite(mean) and math.isfinite(var)'). Mutant ledgers/CS2/mutants/r9v_01_welford_infinite_value_leaves_variance_nan.py (on an infinite value the mean stays finite and M2 becomes NaN) SURVIVES seeds 0-9 ({S}/r9_mutate_all.txt). The reading used is 'both not finite', the plain reading of 'the mean and the sample variance ... are not finite numbers'.",
    "Change test_project.py:420 to `if math.isfinite(mean) or math.isfinite(var):` with the same message family. Checked in a scratch copy ({S}/fixcheck/test_fix_inf.py, {S}/r9_fixcheck.py): reference passes seeds 0-9; r9v_01 fails on all ten seeds; the five round-9 alternatives pass. If the owner reads the sentence as 'either', move r9v_01 to ledgers/CS2/equivalent/ with a README and say so on the page.")
row("grader-classes-never-print", "2.6-autograder / 2.9-spec", "course/modules/CS/CS2/grader/test_project.py:243-258 (test_classes_never_print); project.html:209 'The three classes never print or warn.'", "FAIL",
    f"test_classes_never_print feeds at most five values to each class under capsys (test_project.py:244-255). Mutant ledgers/CS2/mutants/r9v_02_welford_prints_every_hundredth_update.py prints at the 100th update and SURVIVES seeds 0-9 ({S}/r9_mutate_all.txt). Instances run up to 400 values, so the print is reachable and the page's sentence is violated.",
    "Drive each class through at least 120 operations under capsys, for example the whole stream plus a deterministic 150-value tail, as in {S}/fixcheck/test_fix_print.py. Checked in a scratch copy: reference passes seeds 0-9; r9v_02 fails on all ten seeds; the five round-9 alternatives pass ({S}/r9_fixcheck_alts_with_both_fixes.txt, which combines both fixes).")
row("grader-new-mutant-r9v03", "2.6-mutation", "ledgers/CS2/mutants/r9v_03_sketch_new_tuple_delta_drops_successor_delta.py", "PASS",
    f"Student error: the new tuple's delta takes only the successor g (drops its delta). KILLED by test_sketch_rank_guarantee_at_each_probe[4] (seed 5) ({S}/r9_mutate_all.txt). The guarantee fuzz also finds violations ({S}/r9_fuzz_guarantee.out.txt, mutant_r9v_03: 294 violations).")
row("grader-alt-round9", "2.6-autograder", f"{S}/alts/alt_r9_a_exact.py .. alt_r9_e_exact_block.py", "PASS",
    f"Five correct alternatives, each a complete streamstats module, pass the suite on seeds 0-49 (50/50 each, {S}/r9_alternatives_seeds0_49.txt). Their sketch answers also satisfy the rank guarantee on 27,300 fuzz probes each ({S}/r9_fuzz_guarantee.out.txt).")
row("grader-fuzz-round9", "2.6-autograder", f"{S}/r9_fuzz_guarantee.py", "PASS",
    f"Rank guarantee of Conventions, exact Fraction counts, 300 random streams (uniform, ties, sorted, descending, offset 1e6) x 7 eps x 13 probes = 27,300 probes per candidate: reference, alt_a..alt_e, equiv_d8_01, equiv_d8_02, equiv_d9_04, equiv_rank_clamp: 0 violations each ({S}/r9_fuzz_guarantee.out.txt).")

# ---- cards
row("cards-automated", "2.7-cards", "course/modules/CS/CS2/cards.json (216 cards)", "PASS",
    f"{S}/r9_cards_checks.py ({S}/r9_cards_checks.out.txt): 216 cards; ids unique and CS2-cNNN; keys only id, lesson, front, back, grade, basis, cite; basis present exactly when grade is not T; grades T (150) and C (66); every lesson L01-L11 has at least one card; no exact duplicate fronts; numbers other than 0, 1, 2 on any card missing from its own lesson text: none.")
row("cards-sample", "2.7-cards", "cards.json: sample of 22 cards (one per ~10), checked against lesson text and twin output", "PASS",
    f"Sampled and re-read this round: c003 (witness c = a+b+1, n0 = 1, Proposition 1.2); c009 (2^k - 1 and 4^k, twin L01 output); c024 (4.0280 and 3.0156 at n = 256, twin L02); c048 (Corollary 2.2, twin L04 Part C inequality for 2 <= n <= 1000); c063 (500 seeded insertions, twin L05); c065 (height 64, 7, log_phi 65 = 8.6747, twin L05); c069 (1.440420 printed, twin L05); c075 (40 graphs, 200 sources, 0 mismatches, twin L06); c097 (47 calls, 28 stored, 183, twin L07); c123 (two-pass smallest error at 0, 1e6, 1e9, twin L09); c127 (S_3 = 2: sample 1, population 2/3, computed); c151 (198430 and 18213 recomputed); c155 (2.0078, 3.0156, model 1.9922, 2.9922); c157 (0.2680 ... 4.0280, twin L02); c159 (166912, twin L03); c205 (Problem M3 solution in L11); c209 (Section 3 'fourth limit' in L02 is 'The table stores keys'). All match ({S}/twins/*.out).")
row("cards-changed-delta", "2.7-cards", "cards.json entries changed since the round-8 pin (c025, c087, c095) and the round-8 changed set (c035, c155, c174, c227)", "PASS",
    "Changed entries re-verified this round (row cards-changed-c025-c087-c095). c035, c155, c174 re-verified from twin output (rows cards-c035, cards-c155, cards-c174). c227 re-verified against L05 Section 1 text (row cards-c227). Round-8 changed set c008, c024, c143, c165 re-read this round.")
row("cards-c155", "2.7-cards", "course/modules/CS/CS2/cards.json CS2-c155; ledgers/CS2/scripts/CS2-d-r9/twins/lab-CS2-L02-1.out", "PASS",
    "Front 'What successful-search averages does Lab 2 print at n = 128 and n = 256?' Lab 2 output: 'alpha= 2.00 n=128 successful average probes=2.0078 (model 1.9922)' and 'alpha= 4.00 n=256 successful average probes=3.0156 (model 2.9922)'. Matches the back.")
row("cards-c035", "2.7-cards", "cards.json CS2-c035; lab-CS2-L03-1 output rows N=64..4096", "PASS",
    "Printed sorted-list move ratios: 3.5282 (N=64), 4.5050 (N=128), 3.9129, 3.7118, 4.1119, 4.0287, 4.0316. Maximum 4.5050 at N=128, where the sorted list makes 4514 moves against 1002 at N=64 (twin output). Matches.")
row("cards-c174", "2.7-cards", "cards.json CS2-c174; lab-CS2-L03-1 output rows N=64..4096", "PASS",
    "Printed heap move ratios: 2.3778, 2.2331, 2.1535, 1.9858 (N=512), 2.0100, 2.0722, 2.0687. Minimum 1.9858 at N=512, where the heap makes 21095 moves against 10623 at N=256 (twin output). Matches.")
row("cards-c227", "2.7-cards", "cards.json CS2-c227 (L05, grade T); course/modules/CS/CS2/L05.html Section 1", "PASS",
    "L05 text: 'Every key in the left subtree of a node is smaller than the node's key, and every key in the right subtree is larger.' The card's back states the same. Matches.")
row("cards-lab-numbers", "2.7-cards", "cards.json grade C (66 cards); tests/labs/CS2/lab-CS2-L01-1..L11-1", "PASS",
    f"{S}/r9_cards_refs.py ({S}/r9_cards_refs.out.txt): every number (other than 0, 1, 2) on a grade-C card occurs in its lesson's twin output, except derived sums and reference numbers, each checked by hand: 21405, 205, 602, 19140 (sums of printed values, L03 twin); 60 (30 + 30, L07); 100.00 (10000 cents example, c102); 7.87 (7.286e-15 / 9.258e-16 = 7.8700, c193). Every card's cross-reference label (Definition, Proposition, Theorem, Lemma, Corollary, Remark, Problem, Example, Assumption) resolves in its own lesson, and the 'Section N' references resolve to numbered headings (checked by hand).")
row("cards-duplicates", "2.7-cards", "course/modules/CS/CS2/cards.json (full pairwise scan)", "PASS",
    f"{S}/r9_cards_checks.py: no exact duplicate fronts. 67 pairs have a front or back difflib ratio above 0.8 (round 8 reported 57 on the same rule; the count differs and is recorded here). The highest-similarity pairs were read, and each asks a different fact: e.g. c030/c031 push vs pop bound; c035/c174 max vs min ratio; c115/c187 levels created vs removed; c184/c185 left-right vs right-left rotations; c191/c192 trades vs executions; c124/c195 naive vs Welford at offset 1e9; c201/c202 excess vs deficit. No pair is a duplicate.")
row("cards-c033", "2.7-cards", "cards.json CS2-c033; lab-CS2-L03-1 output", "PASS",
    "Sorted-list moves 98 at N = 16 <= 2*16*17 = 544 and 4378444 at N = 4096 <= 2*4096*4097 = 33562624 (twin output; Proposition 1.6 in L03).")
row("cards-full-number-scan", "2.7-cards", "cards.json (all 216 cards)", "PASS",
    f"{S}/r9_cards_checks.py and r9_cards_refs.py: numbers (other than 0, 1, 2) on any card missing from its own lesson text: 0.")
row("cards-c215", "2.7-cards", "cards.json CS2-c215 (AVL double/single rotation rule)", "PASS",
    "L05 text: 'If the heavy child's balance factor is 0 or has the same sign as the unbalanced node's, one single rotation ... If it has the opposite sign, a double rotation is made'. The card states the same rule. Lab 1 Part A invariant True after every insertion (twin L05 output).")
row("cards-count-observation", "2.7-cards", "cards.json (216 cards)", "PASS",
    "Observation, not a finding. BUILDER_RULES section 7 asks for one card per definition, theorem statement, key formula, key empirical result and misconception, with no count cap; the 50-80 figure is an estimate in plan section 9. check_pages passes. Notes for the owner are in the notes field.")
row("cards-changed-c025-c087-c095", "2.7-cards", "cards.json CS2-c025, CS2-c087, CS2-c095 (backs reworded since the round-8 pin)", "PASS",
    "c025: 'Under Assumption 2.1 and at fixed m, the average successful cost is 1 + (n - 1)/(2m)'. L02 Assumption 2.1 (simple uniform hashing) and Proposition 2.2(c) state exactly this. The increase from n = 128 to 256 at m = 64: (1 + 255/128) - (1 + 127/128) = 1 exactly. c087: 'with the minimum over an empty set taken as infinity and infinity plus 1 equal to infinity (Theorem 2.2)'. L07 Theorem 2.2 hypotheses state both conventions. c095: 'optimal for denominations {1, c} with an integer c >= 2 (Problem R2)'. L07 Problem R2 states 'Let D = {1, c} with an integer c >= 2'. Example 2.4 and Problem P3 (fails first at amount 6: greedy 4+1+1 vs 3+3) re-checked by brute force; {1,c} optimality re-checked for c = 2..12, amounts <= 200.")
row("proj-line195-inputs-check", "2.2-prose", "course/modules/CS/CS2/project.html:195-198", "PASS",
    "See row proj-line195-inputs.")

# drop the placeholder duplicate row added above for clarity
rows = [r for r in rows if r["id"] != "proj-line195-inputs-check"]

mutants = [
    {"id": "r9v_01_welford_infinite_value_leaves_variance_nan.py",
     "description": "Welford update given an infinite value leaves the mean finite and sets M2 to NaN, so variance(1) is NaN while mean() still returns a finite number.",
     "killed_by": None},
    {"id": "r9v_02_welford_prints_every_hundredth_update.py",
     "description": "Welford update left a debugging print that fires on every hundredth value, so the accumulator prints output during a long stream.",
     "killed_by": None},
    {"id": "r9v_03_sketch_new_tuple_delta_drops_successor_delta.py",
     "description": "Sketch insertion sets the new tuple delta from the successor g alone, dropping the successor delta from the bookkeeping.",
     "killed_by": "test_sketch_rank_guarantee_at_each_probe[4] (seed 5)"},
]

statuses = [r["status"] for r in rows]
verdict = "PASS" if all(s == "PASS" for s in statuses) and all(m["killed_by"] for m in mutants) else "FAIL"
fragment = {
    "unit": "CS2",
    "slice": "d",
    "round": 9,
    "verifier": "independent verifier (Haiku), round 9; did not build CS2; slice d",
    "pin": "1e272e5a641f18412703b37778a44db6f7391a69",
    "base": "2d755599d8d74df292e3e43025f0458c4053802e (round-8 pin). Delta in slice d: course/modules/CS/CS2/project.html:195 (Inputs sentence); cards.json CS2-c025, CS2-c087, CS2-c095 (backs); new mutants r9v_01..03 and round-9 scripts. Byte-identical since the round-8 pin: grader/ (all four files), tests/labs/CS2, L01-L11, index.html, ledgers/CS2/equivalent/, ledgers/CS2/mutants/ except the three r8v files added before 1e272e5 (tools/ unchanged).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD9-CS2-d",
    "scratch": "ledgers/CS2/scripts/CS2-d-r9",
    "verified_at": "2026-11-05T01:30:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-9 result: three FAIL rows (gate-mutate-cs2, grader-infinite-input, grader-classes-never-print) and one UNVERIFIABLE row (proj-rubric-calibration). The two grader holes are real survivors of student errors that project.html:209 forbids; the proposed test fixes were checked in scratch copies and do not change the reference or the five alternatives.",
        "proj-rubric-calibration cannot be blind in this session: the exemplar annotations were read before any scoring. It needs a fresh verifier (see its fix).",
        "All 67 rows were re-verified this round from scratch or by script; no round-8 PASS row was carried, because every subject either changed or was re-run here. Round-8 rows keep their ids.",
        "Cards: the cards-duplicates scan found 67 pairs above the 0.8 difflib threshold (round 8 recorded 57 on the same rule). All high-similarity pairs ask different facts, so no duplicate was found. Observation for the owner (not a row FAIL): many grade-C cards restate a single printed count of one seeded lab run (e.g. c052, c066, c079, c162, c182-c185, c187-c192). Plan section 9 lists lab results as card material, but BUILDER_RULES section 7 says 'Do not make cards of trivia'. Three cards bundle two claims (c024, c038, c136). The owner may want to split or drop them.",
        "Rank target 'and at least 1' (project.html:219) is not checked by the suite: guarantee_holds in test_project.py checks only the two inequalities. The reference clamps to 1, and an unclamped variant is equivalent (ledgers/CS2/equivalent/rank_target_without_clamp.py), so this is a documentation-level gap, not a fault.",
        "The tracked ledgers/CS2/CS2-d.json at the checkout was a round-15 fragment (pin 448548f). Per the orchestrator's instruction this round's fragment replaces it in this checkout. The directory ledgers/CS2/scripts/CS2-d-r9/ already held tracked files from an earlier attempt (alts_run_r9.py, write_fragment_r9.py, etc.); they were not modified, and round-9 files carry distinct names.",
        "Outside slice d, noted only: index.html:164 (hub, rung 2) says the completion problem removes 'the mean and sum-of-squares lines'; project.html:149-150 says 'the mean and M2 lines'. The wording differs; the lab itself is consistent.",
        "Hours: my central estimate is 22 h against 30 h (27% below), inside the 30% bound; the margin is small.",
        "Not checked: the live verify_refs run (offline only); a blind rubric calibration; in-browser behaviour beyond page_smoke; the proofs of lesson theorems themselves (other slices), only the card wording against the lesson text and the printed numbers.",
    ],
    "summary": "CS2 slice d, round 9: FAIL. Gates: check_pages, check_dag, check_projects, run_graders (50/50), run_labs (14/14), page_smoke (project), ruff, ruff format, mypy, verify_refs --offline, collect 175 on seeds 0-49, relevant pytest, local pytest 50/50 all PASS. mutate_graders: 140/142 killed (exit 1); the two survivors are real student errors that project.html:209 forbids (infinite Welford input leaving a finite mean with NaN variance; a print at the hundredth update). Rubric calibration UNVERIFIABLE (not blind). Five new alternatives pass 50/50. Cards: all 216 re-checked by script and reading; the three changed cards are correct.",
}
out = Path(ROOT) / "ledgers/CS2/CS2-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "statuses", {s: statuses.count(s) for s in set(statuses)}, "verdict", verdict)
