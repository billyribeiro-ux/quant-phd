"""Writes the CS2 slice d round 14 ledger fragment from the evidence in this scratch directory (run from checkout root)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path.cwd()
S = "ledgers/CS2/scripts/CS2-d-r14"
PIN = "1431aa1d842a5d2d05fd5953c098500bf78a4307"
BASE = "329c1d7feac5479403c351e64587c867278452cc"

mutants = []
for line in (ROOT / S / "mutate_graders_0-9_r14.txt").read_text(encoding="utf-8").splitlines():
    if not line.startswith("KILLED "):
        continue
    name, rest = line[len("KILLED "):].split(": ", 1)
    desc, killed = rest.rsplit(" -> ", 1)
    mutants.append({"id": name, "description": desc, "killed_by": killed})
assert len(mutants) == 176, len(mutants)

R = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)


row("gate-mutate-cs2", "2.6-mutation (tools/mutate_graders.py --unit CS2 --seeds 0-9, all existing mutants)",
    "ledgers/CS2/mutants/ (176 files)", "PASS",
    f"{S}/mutate_graders_0-9_r14.txt: 'mutate_graders CS2: PASS (176/176 killed)', rc=0. The first run on seeds 0-1 "
    "left four survivors (r12f_10, r7_02, r8v_02, r9v_03), all killed in the 0-9 window at seeds 2, 3, 2, 5. "
    "Per-mutant kill lines are in the mutants list of this fragment.")
row("gate-run-graders", "2.6-autograder run_graders --seeds 0-49", "course/modules/CS/CS2/grader/", "PASS",
    f"{S}/run_graders.txt: 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.3 s)', rc=0.")
row("gate-check-projects", "2.6 check_projects --unit CS2", "course/modules/CS/CS2/project.html", "PASS",
    f"{S}/check_projects.txt: 'check_projects CS2: PASS', rc=0.")
row("gate-check-dag", "2.9 check_dag --unit CS2", "curriculum/01-foundations.yaml CS2 prereqs [CS1, M1]", "PASS",
    f"{S}/check_dag.txt: 'check_dag CS2: PASS', rc=0.")
row("gate-check-pages", "2.9 check_pages --unit CS2", "course/modules/CS/CS2/", "PASS",
    f"{S}/check_pages.txt: 'check_pages CS2: PASS', rc=0.")
row("gate-run-labs", "2.5 run_labs --unit CS2 --page project", "tests/labs/CS2/lab-CS2-project-{1,2,3}.py", "PASS",
    f"{S}/run_labs_project.txt: 'run_labs CS2: PASS (3/3)', rc=0.")
row("gate-page-smoke", "2.9 page_smoke --unit CS2 --pages project", "course/modules/CS/CS2/project.html", "PASS",
    f"{S}/page_smoke_project.txt: labs 0.0 s each; 'in-browser grader: All 175 tests pass on seed 1960780701'; "
    "'page_smoke modules/CS/CS2/project.html: PASS', rc=0.")
row("gate-ruff-mypy", "2.9 ruff check, ruff format --check, mypy --no-incremental",
    "grader/, tests/labs/CS2/, ledgers/CS2/mutants/r14_*", "PASS",
    f"{S}/ruff_check.txt 'All checks passed!' rc=0; {S}/ruff_format.txt '18 files already formatted' rc=0; "
    f"{S}/mypy.txt 'Success: no issues found in 385 source files' rc=0.")
row("gate-verify-refs", "2.1 verify_refs --offline and --unit CS2 (live)", "references/references.json", "PASS",
    f"{S}/verify_refs_offline.txt 'offline integrity: 560 entries, 0 problems' rc=0; "
    f"{S}/verify_refs_unit_CS2_live.txt 'live re-verification of CS2: 1 of 560 entries, 0 problems' rc=0.")
row("gate-collect-count", "2.6 collect-only count, seeds 0-49", "course/modules/CS/CS2/grader/test_project.py", "PASS",
    f"{S}/collect_reference.txt: 50 lines, each 'rc=0 175 tests collected', 'seeds_failed=0 of 50'.")
row("gate-pytest-relevant", "relevant pytest (-k CS2)",
    "tests/test_labs.py, tests/test_page_smoke.py, tests/test_page_checks.py", "PASS",
    f"{S}/pytest_k_CS2.txt: quiet run ends with rc=0 (command: pytest -q -k CS2 on the three files).")
row("gate-local-pytest", "2.6-autograder local pytest (-p no:cacheprovider --assert=plain -W error)",
    "course/modules/CS/CS2/grader/test_project.py", "PASS",
    f"{S}/collect_reference.txt and {S}/suite.py runs use the local pytest (9.0.2, Python 3.14.8, see "
    "'.venv/bin/python --version'): reference 50/50 seeds with 175 passed (alts_A.txt..alts_E.txt show 175 passed per seed).")

row("labs-project-1", "2.5 lab, rung 1 (lab-CS2-project-1)", "course/modules/CS/CS2/project.html:53-146", "PASS",
    f"{S}/labs_twin_r14.txt: page code == twin (74 lines each); twin run alone with python -I -W error rc=0; "
    "twin stdout == expected block. Lab prints 44 deque ops and bound 4n = 48; docstring/hypothesis claims checked "
    f"against the output and {S}/docstring_naive_r14.txt ('lab1 ... deque ops 44 bound 4n 48').")
row("labs-project-2", "2.5 lab, rung 2 completion (lab-CS2-project-2)", "course/modules/CS/CS2/project.html:148-189",
    "PASS",
    f"{S}/labs_twin_r14.txt: the page block differs from the twin in exactly two lines, the blanks "
    "'mean = ___' and 'm2 = ___' (the twin holds the completed expressions 'mean + delta / count' and "
    "'m2 + delta * (x - mean)'). This is the designed completion layout. The twin run alone (python -I -W error) "
    "matches the expected block (count 8, mean 1000003.750000, sample variance 8.500000). Recomputed by hand: "
    "offsets 2,5,1,4,9,3,6,0 give mean 3.75 and sum of squared deviations 59.5, /7 = 8.5.")
row("labs-project-3", "2.5 lab, rung 3 reference numbers (lab-CS2-project-3)", "course/modules/CS/CS2/project.html:260-340",
    "PASS",
    f"{S}/labs_twin_r14.txt: page code == twin (64 lines); twin rc=0; stdout == expected. "
    f"{S}/numbers_r14.txt B: exact mean 10004.181818, exact sample variance 8.313636, sum 110046.0, "
    "last-4 min 10001.0 max 10006.3, median target 5, 5th smallest 10003.2, qn-eps*n = 22/5 = 4.4 (all recomputed with Fraction).")

row("proj-prose-numbers", "2.2 numbers in prose (classes a, b, c)", "course/modules/CS/CS2/project.html", "PASS",
    f"Every number recomputed: {S}/numbers_r14.txt (A, B, C), {S}/docstring_naive_r14.txt. Lab numbers are "
    "(a) printed by Lab 1/2/3 (run_labs passes). 4n=48 and 44 (Lab 1); 8.313636, 10004.181818, 110046.0/11 "
    "(Lab 3, derived sum shown); 5.5-1.1=4.4 (c). Witnesses: q=0.1 n=20 eps=0.05 exact target 2 vs float 1; "
    "q=0.2500004 target 5 vs q=0.25 target 4 (numbers_r14.txt C). Counts 175 (gate-collect-count), 30/100/130 hours "
    "(index.html data-hours-lessons=100, data-hours-project=30; curriculum CS2 hours 130). Nothing rounded differently "
    "from the unrounded value.")
row("proj-line145-amortized", "2.2 / 2.3 speed claim (line 145) and grade", "project.html:145", "PASS",
    "Line 145 says the count 44 is at most 4n = 48 and gives amortized constant work 'in the average sense', "
    "which the lab's single seeded series does not prove. The 4n bound follows from each value being pushed "
    "once per deque and popped at most once (re-derived in docstring_naive_r14.py, count 44 agrees). The sentence "
    "disclaims timing (line 145: 'it does not measure time').")
row("proj-line386-design-note", "2.3 / 2.6 Exemplar B design claims (line 386-387)", "project.html:386-387", "PASS",
    "Probe set (0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1, one seeded value) = PROBES_FIXED + round(rng.random(),3) "
    "(grader/instance.py:27,41); epsilons 0.05, 0.1, 0.2 (instance.py:28); wide epsilons 0.3, 0.5, 0.9 at q "
    "0,0.25,0.5,0.75,1 (test_project.py:891-904); short streams 1-8 and 20-value q=0.1 and q=0.2500004 witnesses "
    "(test_project.py:859-943); constant and single-value streams at each probe (test_project.py:825-843). "
    "The memory and domain limits match the suite (no memory test: grep found none).")
row("proj-exemplar-b-claims", "2.4 / 2.3 Exemplar B proof and numbers", "project.html:376-391", "PASS",
    "Re-derived the Welford step: S_{n+1} = S_n + n*delta^2/(n+1) with a = delta/(n+1) and new deviation n*delta/(n+1) "
    "(exact algebra, checked by hand in the proof steps). Lab 3 numbers 8.313636 and the 1e-9 agreement are "
    f"Lab 3 output ({S}/numbers_r14.txt B). Exemplar B's C2 algebra line '(n+n^2)/(n+1)^2 = n/(n+1)' is "
    "justified by an implicit cancellation, not by name; this is within one level of the official 4 and is noted "
    "in notes, not a failure.")
row("proj-process-words", "2.9 no process words in learner text", "course/modules/CS/CS2/project.html", "PASS",
    "grep -n -i for verifier, builder, ledger, round N, agent, TODO, TBD, lorem: no hits in project.html.")
row("proj-banned-phrases", "2.9 BUILDER_RULES 1.3-1.4 banned phrases", "course/modules/CS/CS2/project.html", "PASS",
    "grep -i for todo, tbd, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, "
    "it is important to note, studies show, experts agree, it is well known, obviously, clearly: no hits. "
    "The word 'we' (lines 380-381) is proof prose, not a banned filler phrase.")
row("proj-rubric-observable", "2.6 rubric descriptors are observable", "course/modules/CS/CS2/project.html:350-357", "PASS",
    "Read all 6 criteria x 4 levels. Each level is decided by a visible element (a listed hypothesis, a shown base case, "
    "a named lab output, a stated guarantee with probe set and limits). No descriptor depends on an unstated judgement. "
    "Observation: C6 level 2 ('names a lab for each claim, quotes no number') and level 3 ('names a lab output') differ "
    "only by whether a number is quoted, which is observable.")
row("proj-rubric-calibration", "2.6 rubric calibration (exemplars scored blind)",
    "course/modules/CS/CS2/project.html:362-391 (exemplar-a, exemplar-b)", "UNVERIFIABLE",
    "Not blind. The official scores and the annotations (data-reveal paragraphs, project.html:367, 370-373, 378, 382-384, "
    "388-390) were displayed to this verifier in this session before any scoring. For the record, reading the bodies "
    "against the rubric alone gives Exemplar A 1,1,2,1,1,1 and Exemplar B 4,4,4,4,4,4, which match the official "
    "scores; this is not evidence of a blind calibration.",
    "A verifier with no prior exposure to project.html:362-391 must score Exemplar A and Exemplar B from the rubric table "
    "(project.html:350-357) alone, with the data-scores and annotation paragraphs hidden, record each criterion, and "
    "confirm each score is within one level of the official annotation.")
row("proj-ladder-scope", "2.6 ladder present and correct", "course/modules/CS/CS2/project.html:40-190", "PASS",
    "Rung 1 (Lab 1) is fully solved with a why note on each deque rule (lines 80, 82, 88, 94, 100). Rung 2 (Lab 2) is "
    "graded instantly by its expected block. Rung 3 matches the curriculum project (streaming statistics library, "
    "grading both). Rung 4 (stretch, lines 400-406) is open-ended (weighted/time-decayed accumulator; merge of two sketches).")
row("proj-notation", "2.4 / BUILDER 3 notation against notation/notation.json", "course/modules/CS/CS2/project.html", "PASS",
    "Registered symbols and macros (notation/notation.json: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, "
    "\\mathbb{Q}; macros \\E, \\Prob, \\Var, \\R, ...). project.html uses only \\bar, \\delta, \\sum, \\varepsilon, "
    "\\le, \\dots, \\frac, \\cdot (grep count). None collides; n, q, S, m, x_i are conventionally local letters "
    "(notation.json 'about').")
row("proj-dag-concepts", "2.9 / BUILDER 1.10 DAG and concept links", "curriculum/01-foundations.yaml:417-421; project.html", "PASS",
    "CS2 prereqs are [CS1, M1] (curriculum/01-foundations.yaml:421), which applies architect option (a) of "
    "plans/CS2-build-plan.md section 2, so mathematical-induction (M1) is in the closure. welford-algorithm, "
    "monotonic-deque and quantile-sketch are defined once in L09, L10, L11 (def- ids present) and linked from the page. "
    "The page writes no variance or quantile-function concept link (plan section 2 item 2). check_dag PASS.")
row("proj-reading-citation", "2.1 reading list and attribution", "course/modules/CS/CS2/project.html:408-414", "PASS",
    "The reading item cites cormen2022introduction, which is in references/references.json (status verified, pages null, "
    "container null). The page says it names no page or section and attributes no step to it, which matches the record. "
    "verify_refs --unit CS2 (live) PASS.")
row("proj-spec-completeness", "2.6 spec complete for a competent student (no clarifying question needed)",
    "course/modules/CS/CS2/project.html:194-224; 238", "PASS",
    "Round 12 FAIL: the hours row (line 238) asked for a proof of the rank guarantee the write-up does not require. "
    "Line 238 now reads 'state the rank guarantee the tests check', consistent with line 344 and criterion C5. Re-read: "
    "inputs, outputs, constraints, grading mode, probe set, witnesses and exception rules are stated; no question found "
    "that the page leaves open for the named conditions.")
row("proj-context-length", "2.9 / BUILDER 5.2 Context in 2-4 sentences", "course/modules/CS/CS2/project.html:196", "PASS",
    "Round 12 FAIL (six sentences). The Context dd now has three sentences: 'A monitoring team receives ...'; 'You implement "
    "a small library ...'; 'The streams in the labs and the autograder are SIMULATED, ...'. Within 2-4.")
row("proj-hours", "2.6 hours estimate within 30% (and hub split sums to 30)", "course/modules/CS/CS2/project.html:227-245",
    "PASS",
    "My own estimate: rung 1 1.5 h, rung 2 1 h, Welford 3 h, Welford proof 3 h, deque 3 h, sketch with rank tests 8 h, "
    "package and validation 3 h, design note 2.5 h, Lab 3 1 h; total 26 h, 13% below 30 (within 30%). Declared rows sum "
    "to 30 (2+3+4+4+4+6+4+3). Hub data-hours-project=30 and lessons 100 (index.html).")
row("proj-named-conditions", "2.6 named conditions (Constraints) and their tests",
    "course/modules/CS/CS2/project.html:209, 224; grader/test_project.py", "PASS",
    "The ten conditions map to tests: (1) test_welford_mean_before_any_value_raises, _variance_before_, "
    "_population_variance_before_; (2) test_welford_sample_variance_of_one_value_raises; (3) test_welford_nan_update_raises; "
    "(4) test_rolling_window_zero_raises, _negative_, _boolean_false_; (5) test_rolling_nan_push_raises; (6) "
    "test_rolling_minimum/maximum_before_push_raises; (7) test_sketch_epsilon_outside_open_interval_raises and "
    "test_sketch_boolean_epsilon_raises; (8) test_sketch_nan_add_raises; (9) test_sketch_quantile_below_zero / above_one / "
    "nan / outside_closed_interval; (10) test_sketch_quantile_on_empty_sketch_raises. must_raise is used only for these.")
row("proj-line195-inputs", "2.1 Inputs paragraph agrees with instance.py", "project.html:198; grader/instance.py:27-41",
    "PASS",
    f"{S}/instances_r14.txt: all 50 seeds have 20-400 finite values, decimals 1 or 6, offsets 0/10000/1000000, window "
    "2-30, epsilon in {0.05,0.1,0.2}, 10 probes in [0,1], SIMULATED label; 'validity problems: none'.")
row("proj-exemplar-namely-sentence", "2.6 exemplar sourcing sentence (line 363)", "project.html:363", "PASS",
    "The fixed constants the sentence names (probe set, epsilons, wide epsilons, witness quantiles, stream lengths) are "
    "in instance.py:27-28 and test_project.py:859-943 (see proj-line386-design-note).")
row("proj-inventory-test-claims", "2.6 test-count and test-content claims in the spec (line 211)",
    "project.html:211; grader/test_project.py", "PASS",
    "175 = collect-only count (gate-collect-count). Each named coverage item was matched to a test: boundary cases "
    "(window 0/1, epsilon 0/1e-6/0.999999/-1e-6, q 1.1/1.0, q just outside/inside each end), prefixes 2-20, scaling by 4, "
    "eight widths, repeated values, wide epsilons, the fixed witnesses, monotonicity over 101 q plus probes, count type, "
    "no print/warn, stdlib only, boolean/string/None/whole-float/2.5 inputs and ddof string/float/None. "
    "The statement 'the autograder does not test memory' holds (no memory test in test_project.py).")

row("grader-instance", "2.6-autograder instance.py: deterministic, valid, materially different", "grader/instance.py",
    "PASS",
    f"{S}/instances_r14.txt: validity over seeds 0-49 'none'; test_instance_is_deterministic; 20-seed sample shows 20 of 20 "
    "distinct (mean, variance) pairs; 50 of 50 distinct streams (numbers_r14.txt A).")
row("instance-docstring-counts", "2.2 numbers in instance.py docstring (lines 11-13)", "grader/instance.py:8-14", "PASS",
    f"{S}/docstring_naive_r14.txt re-derives the counts with the docstring's own order (s += x, ss += x*x, mean = s/n, "
    "variance (ss - n*mean*mean)/(n-1)): offset 0 has 16 seeds, 0 naive failures; offset 10000 has 23 seeds, 22 naive "
    "failures (seed 41 passes); offset 1000000 has 11 seeds, 11 failures. The reference Welford passes 50 of 50 "
    f"({S}/numbers_r14.txt A). Failure = variance off by more than 1e-9 relative (mean-only failures: 0).")
row("instance-distinct-seeds", "2.6 instances differ materially (answers, not labels)", "grader/instance.py", "PASS",
    f"{S}/instances_r14.txt: 20 of 20 sampled seeds give distinct (mean, sample variance); 48 of 50 distinct sketch medians "
    "over seeds 0-49 (the two repeats are a tie of stream answers, not a label change).")
row("grader-reference", "2.6-autograder reference passes 0-49 and the sketch docstring claims hold",
    "grader/reference.py", "PASS",
    f"run_graders 50/50; {S}/numbers_r14.txt D: 400 random sketches, sum(g)=n, g+delta <= floor(2 eps n)+1 and the "
    "rank-interval invariant all hold (0 violations); E: 132600 rank-guarantee checks, 0 violations.")
row("grader-starter", "2.6 starter raises NotImplementedError in every method", "grader/starter.py", "PASS",
    "starter.py lines 13-53: every method (update, count, mean, variance, __init__, push, minimum, maximum, add, quantile) "
    "raises NotImplementedError; the suite therefore fails on the starter.")
row("grader-tests-rank", "2.6 rank tests: exact target witnesses and short-stream docstrings",
    "grader/test_project.py:859-943", "PASS",
    f"Witness q=0.1, n=20, eps=0.05: exact target 2, float target 1 ({S}/numbers_r14.txt C). Witness q=0.2500004: "
    "target 5 vs 4 for q=0.25. Short-stream docstring: slack below one rank for eps 0.05 and 0.1 at all lengths and for "
    "0.2 up to length 4 (0.2*5 = 1.0), recomputed.")
row("grader-docstring-delta", "2.6 docstrings changed since round 12 (test_project.py 825-828, 836-837, 862-864, 892-896)",
    "grader/test_project.py", "PASS",
    "The constant-stream and single-value tests now check the guarantee at each probe (guarantee_holds), and their "
    "docstrings match the code. The wide-epsilon docstring arithmetic (2 - 0.6 = 1.4; answer below 2.0 has one value at or "
    "below it) re-derived. The denoted-value docstring (slack 0.5 rank, one value below 10.0) re-derived.")
row("grader-messages-no-expected-value", "2.6 failure messages name the property and never leak the expected answer",
    "grader/test_project.py (pytest.fail and must_raise messages)", "PASS",
    "Read every pytest.fail, must_raise and refuse_or_correct message. Messages name the property; where a learner's "
    "returned value is printed (for example None-ddof and None-window tests) it is the learner's own value, not the expected "
    "answer. No message prints an expected reference value.")
row("grader-wide-eps-docstring", "2.6 wide-epsilon docstring arithmetic", "grader/test_project.py:892-904", "PASS",
    "Two values 1.0 and 2.0, epsilon 0.3: qn - eps*n = 2 - 0.6 = 1.4; an answer below 2.0 has at most one value at or below it "
    "(1 < 1.4), so the docstring is correct (recomputed).")
row("grader-new-mutants", "2.6-mutation: at least three new student-error mutants of my own",
    "ledgers/CS2/mutants/r14_01..03 (written by ledgers/CS2/scripts/CS2-d-r14/make_mutants_r14.py)", "PASS",
    "r14_01 Welford M2 sign flipped (killed by test_welford_variance_default_ddof_is_sample, seed 0); r14_02 quantile "
    "tests the upper rank bound g+delta (killed by test_sketch_rank_guarantee_on_short_streams[5-0.2], seed 0; the "
    f"battery {S}/mutant_guarantee_r14_new.txt shows 3213 guarantee breaks); r14_03 Welford mean divisor max(count-1,1) "
    "(killed by test_welford_sample_variance_matches_exact_reference, seed 0). All three are in the 176/176 gate run.")
row("grader-alternatives", "2.6-autograder: correct alternatives pass (over-constraint check)",
    f"{S}/alts/alt_r14_A..E.py; ledgers/CS2/scripts/CS2-d-r12/alts/alt_r12_G_q0_below_minimum.py", "PASS",
    "Five new correct implementations pass 50/50 each: A exact sorted list with Fraction target; B exact list with "
    "floor(qn-eps n)+1 cutoff and fsum Welford; C reference with cap floor(2 eps n); D Welford with exact Fraction sums; "
    "E brute-force rolling window (alts_A.txt..alts_E.txt, 175 passed per seed). Round-12 alternative G (quantile(0) below "
    f"the minimum, the round-12 over-constraint FAIL) re-run now: 0 of 50 failures ({S}/alts_r12_rerun.txt). "
    "Round-12 alternatives A, B, F, G re-run: 0 failures each.")
row("grader-alt-r12-A-F", "2.6 round-12 alternatives A-F re-run on the current suite",
    f"ledgers/CS2/scripts/CS2-d-r12/alts/; {S}/alts_repointed_r14/", "PASS",
    f"{S}/alts_r12_rerun.txt: A, B, F 0 of 50. C, D, E failed to import because the round-12 scratch files read the reference "
    "from the deleted checkout verifyD12-CS2-d (a stale absolute path, not a grader fault). The same files repointed to "
    f"this checkout ({S}/alts_repointed_r14/) pass 0 of 50 each. The round-7 alternative alt_r7_06_r9path.py had the same "
    "stale path (verifyB12-CS2-d) and passes 0 of 50 repointed.")
row("grader-guarantee-battery", "2.6 rank guarantee holds for the reference (battery)", "grader/reference.py", "PASS",
    f"{S}/numbers_r14.txt E: 132600 (stream, eps, q) checks with exact counts, 0 violations. "
    f"{S}/mutant_guarantee_r14.txt: reference 0 of 90900 checks break.")
row("grader-classes-never-print", "2.6 classes never print or warn; state held per object", "grader/test_project.py:244-281; 945-959",
    "PASS",
    "test_classes_never_print drives 150+ operations per class with capsys and warnings capture; "
    "test_instances_hold_their_own_state checks independence. The r9f print/warn mutants are in the 176/176 run.")
row("grader-infinite-input", "2.6 infinite input outcome (Constraints line 209)", "grader/test_project.py:431-444", "PASS",
    "The test accepts a raise or non-finite mean/variance for +inf and -inf (Constraints). Re-derived: the reference's update "
    "gives mean inf and variance nan, so the reference passes by the non-finite branch.")
row("mut-survivors", "2.6-mutation: survivors at seeds 0-1 are killed in the window",
    "ledgers/CS2/mutants/r12f_10, r7_02, r8v_02, r9v_03", "PASS",
    "Behaviour checked by battery: r7_02 (drops repeated values) breaks the guarantee on 939 of 90900 checks; r9v_03 "
    "(successor delta dropped) on 620; both are killed (seeds 3 and 5). r8v_02 (mean rounded to six places) and r12f_10 "
    "(refuses negative values, a value the page says is a real number, line 198) are killed only on offset-0 seeds (2, 6, 7 "
    "in the window), which is why the window matters; both are killed at seed 2. No survivor needed a spec citation change.")
row("equiv-m14_01", "2.6 equivalent mutant proof (ledgers/CS2/equivalent/rank_target_without_clamp.py)",
    "ledgers/CS2/equivalent/rank_target_without_clamp.py", "PASS",
    f"Argument: every stored tuple has g >= 1, so after the first tuple the running rank is >= 1; a target <= 1 therefore "
    f"returns the first value in both versions, and a target > 1 is unchanged. Differential check {S}/equiv_diff_r14.txt: "
    "28500 (stream, eps, q) checks, 0 differences.")

freshness = []
registry = []
notes = [
    "Scope: slice d of CS2 (project.html, grader/ reference, instance, starter, test_project.py, the three project labs, "
    "and ledgers/CS2/mutants). Cards were out of scope this round (no cards rows). Cards rows of round 12 are not carried.",
    "Round 13 fragment is missing: /Users/billyribeiro/.fanout/frags/D-CS2-d.round13.json does not exist (the frags directory "
    "holds rounds 1-12 for D-CS2-d). The requested context path was therefore unavailable; round 12 was used as context. "
    "The committed ledgers/CS2/CS2-d.json at the pin (round 15, pin 448548f9) is from another lineage and is overwritten here "
    "as the task requires.",
    "Delta since the round-12 pin 329c1d7f in the slice: project.html (3 hunks: lines 196, 238 and 386, the Exemplar B design paragraph), grader/test_project.py (25 lines: constant and single-value guarantee tests, docstrings), and new mutants "
    "r12f_01..10 and r12v_01..03 (already in the round-12-fix). reference.py, instance.py, starter.py and the three project "
    "twins are byte-identical since 329c1d7f. Every slice file was read in full this round; every row was re-verified, so no "
    "PASS row is carried from round 12.",
    "Blindness: the rubric calibration could not be done blind (annotations displayed earlier in this session), so "
    "proj-rubric-calibration is UNVERIFIABLE and the verdict is FAIL.",
    "Observation, not a failure: Exemplar B's C2 algebra step '(n+n^2)/(n+1)^2 = n/(n+1)' is justified by an implicit cancellation "
    "rather than named; C2 level 4 says 'justified by name'. The official 4 is within one level, so calibration tolerance holds.",
    "Observation, not a failure: project.html:220 says an infinite value is outside the domain, while Constraints (line 209) "
    "gives an outcome for WelfordAccumulator.update. Both are consistent (the Welford case is stated explicitly).",
    "Lab 2 page block is not runnable as printed (blanks by design); the twin is runnable and matches the expected block.",
    "Not run: the full repository gate (scope limited to this slice, per the assignment); cards; the other slices' pages. "
    "No git commit or push, and no course, tool, test, reference, curriculum or atlas file was edited. Scratch scripts and "
    "outputs are under ledgers/CS2/scripts/CS2-d-r14/ (untracked). Pre-existing tracked files in that directory "
    "(mkws.sh, run_one.sh, mut/) belong to another verifier and were not modified or used.",
    "Stray files: alt_r14_C/D/E were first written to the checkout root by mistake and were deleted before the final run.",
]
non_pass = [r for r in R if r["status"] != "PASS"]
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
summary = (
    f"CS2 slice d round 14: FAIL. Rows {len(R)} (pass={counts['PASS']} fail={counts['FAIL']} "
    f"unverifiable={counts['UNVERIFIABLE']}). Non-PASS: proj-rubric-calibration (UNVERIFIABLE, not blind). "
    "Gates PASS: mutate_graders 176/176 (rc 0), run_graders 50/50, collect 175 x 50, run_labs 3/3, page_smoke, check_pages, "
    "check_dag, check_projects, ruff, mypy, pytest -k CS2, verify_refs offline and live. Round-12 FAILs (proj-spec-completeness, "
    "proj-context-length, grader-alternatives) are fixed and re-verified. Mutants: 176 listed, 176 killed; 3 new student-error mutants "
    "(r14_01..03) killed."
)
fragment = {
    "unit": "CS2",
    "slice": "d",
    "round": 14,
    "verifier": "independent verifier (Haiku), round 14; did not build CS2",
    "pin": PIN,
    "base": BASE,
    "checkout": str(ROOT),
    "scratch": S,
    "verified_at": "2026-11-09T06:40:00+00:00",
    "verdict": "PASS" if not non_pass else "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": registry,
    "freshness_flags": freshness,
    "notes": notes,
    "summary": summary,
}
out = ROOT / "ledgers/CS2/CS2-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(R), counts, "mutants", len(mutants), "verdict", fragment["verdict"])
