"""Build ledgers/CS2/CS2-d.json (round 12, slice d) from the r12 evidence files. Run with python -I from the checkout."""
import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD12-CS2-d")
S = "ledgers/CS2/scripts/CS2-d-r12"
PIN = "329c1d7feac5479403c351e64587c867278452cc"
BASE = "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87"
P = "PASS"
F = "FAIL"
U = "UNVERIFIABLE"
CARRY = "Carried from round 11 ({files} byte-identical since the previous pin ccaeeaf4): "

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)


# ---- gates (run by this verifier at pin 329c1d7; outputs in scripts/CS2-d-r12) ----
mut_out = (ROOT / S / "mutate_graders_r12.txt").read_text(encoding="utf-8").splitlines()
row("gate-mutate-cs2", "2.6-mutation", "ledgers/CS2/mutants/ (163 files); course/modules/CS/CS2/grader/test_project.py", P,
    "Command: .venv/bin/python tools/mutate_graders.py --unit CS2 --seeds 0-9 -> 'mutate_graders CS2: PASS (163/163 killed)', rc=0 "
    f"({S}/mutate_graders_r12.txt; one KILLED line per mutant, with the killing test and seed). Includes the three new mutants "
    "r12v_01..03 (killed by test_welford_sample_variance_of_one_value_raises, test_rolling_ties_expire_with_their_index[2], "
    "test_welford_sample_variance_matches_exact_reference).")
row("gate-run-graders", "2.6-autograder", "course/modules/CS/CS2/grader/", P,
    f"Command: tools/run_graders.py --unit CS2 --seeds 0-49 -> 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.3 s)', rc=0 "
    f"({S}/run_graders.txt). Independent copy: suite.py on reference.py seeds 0-49 -> seeds_failed=0 of 50 ({S}/reference_0_49.txt).")
row("gate-check-projects", "2.6-gate", "tools/check_projects.py; course/modules/CS/CS2/project.html", P,
    f"Command: tools/check_projects.py --unit CS2 -> 'check_projects CS2: PASS', rc=0 ({S}/check_projects.txt).")
row("gate-check-dag", "2.9-gate", "tools/check_dag.py", P,
    f"Command: tools/check_dag.py --unit CS2 -> 'check_dag CS2: PASS', rc=0 ({S}/check_dag.txt).")
row("gate-check-pages", "2.9-gate", "course/modules/CS/CS2/", P,
    f"Command: tools/check_pages.py --unit CS2 -> 'check_pages CS2: PASS', rc=0 ({S}/check_pages.txt).")
row("gate-run-labs", "2.5-gate", "tests/labs/CS2/; project.html lab blocks", P,
    f"Command: tools/run_labs.py --unit CS2 -> 'run_labs CS2: PASS (14/14)', rc=0 ({S}/run_labs.txt).")
row("gate-page-smoke", "2.9-gate", "course/modules/CS/CS2/project.html", P,
    f"Command: tools/page_smoke.py --unit CS2 --pages project.html (alone) -> 'page_smoke CS2: PASS', rc=0 ({S}/page_smoke_project.txt).")
row("gate-ruff-mypy", "lint/type gate", "course/modules/CS/CS2/grader; tests/labs/CS2; ledgers/CS2", P,
    f"Scope: this slice only. ruff check on the three paths -> 'All checks passed!'; ruff format --check -> '18 files already formatted'; "
    f"mypy --no-incremental on grader/ and the three project twins -> 'Success: no issues found in 7 source files' ({S}/ruff_check.txt, ruff_format.txt, mypy.txt). The repo-wide ruff/mypy gates were not run.")
row("gate-verify-refs", "2.1-citation", "references/references.json", P,
    f"Command: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', rc=0; tools/verify_refs.py --unit CS2 -> "
    f"'live re-verification of CS2: 1 of 560 entries, 0 problems', rc=0 ({S}/verify_refs_offline.txt, verify_refs_unit_live.txt).")
row("gate-collect-count", "2.6-count", "grader/test_project.py; project.html Grading mode", P,
    f"suite.py --collect on reference.py for seeds 0-49: 50 of 50 rc=0 and '175 tests collected' each ({S}/collect_all_seeds.txt). Page quotes 175 (project.html:211).")
row("gate-pytest-relevant", "2.5-gate", "tests/test_memo_exemplars.py, tests/test_docs_figures.py, tests/test_page_checks.py, tests/test_labs.py", P,
    f"pytest -q on those four modules -> 100% dots, rc=0 ({S}/pytest_slice.txt); pytest -q -k 'CS2 or cards or project_lab or grader' rc=0 ({S}/pytest_k.txt).")
row("gate-local-pytest", "2.6-autograder", "grader/test_project.py; project.html:256 local command", P,
    f"suite.py reproduces the project.html:256 command (pytest -q -p no:cacheprovider --assert=plain -W error, QF_SEED per seed) on reference.py: 50/50 pass ({S}/reference_0_49.txt).")

# ---- labs (project twins) ----
lab_out = (ROOT / S / "lab_equal_r12.txt").read_text(encoding="utf-8")
row("labs-project-1", "2.5-lab", "course/modules/CS/CS2/project.html:53-146; tests/labs/CS2/lab-CS2-project-1.py", P,
    "lab_equal_r12.py: page code == twin (True); expected block == twin output (True); twin run with python -I -W error rc=0; "
    "blanks 0; 14 expected lines (" + f"{S}/lab_equal_r12.txt). Hand check: window of four, step 12 min 1 / max 61, 44 <= 48.")
row("labs-project-2", "2.5-lab", "course/modules/CS/CS2/project.html:148-189; tests/labs/CS2/lab-CS2-project-2.py", P,
    "Page code equals the twin except the two ___ lines (twin has the completed mean and m2 expressions; the diff is in lab_equal_r12.txt); "
    "twin output == expected block (3 lines: count 8, mean 1000003.750000, sample variance 8.500000); twin rc=0 under -I -W error. "
    "Hand check: offsets 2,5,1,4,9,3,6,0 give mean 3.75 and S = 59.5, /7 = 8.5.")
row("labs-project-3", "2.5-lab", "course/modules/CS/CS2/project.html:262-339; tests/labs/CS2/lab-CS2-project-3.py", P,
    "page code == twin (True); expected == output (True, 8 lines); twin rc=0 under -I -W error. Independent recompute "
    f"({S}/project_numbers_r12.txt): sum 110046.0, mean 10004.181818, sample variance 8.313636, last-4 min 10001.0 max 10006.3, "
    "median target 5 (5.5 - 1.1 = 4.4 exact), 5th smallest 10003.2.")

# ---- project page: numbers, claims, structure ----
row("proj-prose-numbers", "2.2-numbers", "project.html lede, Inputs, Grading mode, time table, Labs 1-3 prose, exemplars", P,
    "Re-derived: 30 h (table rows 233-240 sum 2+3+4+4+4+6+4+3=30); 175 checks (collect, all seeds); instance ranges 20-400 values, offsets 0/10,000/1,000,000, "
    "windows 2-30, eps 0.05/0.1/0.2, ten probes (instance.py:27-41); Lab 1: 44 operations vs bound 4n=48 (expected block); Lab 3: 110046.0/11 = 10004.181818, "
    f"sample variance 8.313636, median rank 5 ({S}/project_numbers_r12.txt). Lab 2 mean 1000003.75, variance 8.5 (exact Fraction recompute in the same file). "
    "The 2^k and 4n figures match the lab expected blocks.")
row("proj-line145-amortized", "2.9-interpretation", "course/modules/CS/CS2/project.html:145", P,
    "Lab 1 interpretation: min 1 from step 9 is still in the window at step 12 ([1,47,61,35]) and leaves at step 13 (window of four). "
    "44 <= 48. Each value is appended once per deque and popped at most once per deque (code lines 89-106), so pushes = 2n and pops <= 2n, "
    "count <= 4n. The page says the bound is on the average over a run and no timing is claimed; no timing appears in Lab 1.")
row("proj-line386-design-note", "2.9-prose / 2.6-spec", "course/modules/CS/CS2/project.html:386 (Exemplar B design note)", P,
    "Each claimed check exists in test_project.py: ten probes (test_sketch_rank_guarantee_at_each_probe, lines 803-814); streams of one to eight values at eps 0.05, 0.1, 0.2 "
    "(852-867); sorted (839-849); repeated values (871-881); eps 0.3/0.5/0.9 at q 0, 0.25, 0.5, 0.75, 1 (884-897); fixed twenty-value stream at q = 0.1 and 0.2500004 (900-935); "
    "constant stream (825-830). Probe list matches instance.py:27,41.")
row("proj-process-words", "2.9-banned", "project.html; grader/*.py; tests/labs/CS2/lab-CS2-project-*.py; cards.json", P,
    f"grep -i -w for round, verifier, builder, ledger, reviewer, agent, fix, fixed, TODO, placeholder, draft, wip: only ordinary English and code round() ({S}/banned_and_context_r12.txt).")
row("proj-banned-phrases", "2.9-banned", "project.html; grader/*.py; tests/labs/CS2/lab-CS2-project-*.py; cards.json", P,
    f"Regex for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, "
    f"experts agree, it is well known, obviously, clearly, ellipsis, placeholder: no hit in prose or labs; test_project.py:268 is a type annotation tuple[..., ...] "
    f"({S}/banned_and_context_r12.txt).")
row("proj-rubric-observable", "2.6-rubric", "course/modules/CS/CS2/project.html:348-357 (rubric-memo, C1-C6, four levels)", P,
    "All 24 cells read (project.html:352-357). Six criteria, four levels each (4-7 required). Descriptors are checkable: C5 level 3 counts named limits, C6 level 2 "
    "requires a quoted number, C4 level 3 names floating point; no vague descriptor found.")
row("proj-rubric-calibration", "2.6-rubric", "course/modules/CS/CS2/project.html:362-391 (exemplar-a, exemplar-b; data-scores 1,1,2,1,1,1 and 4,4,4,4,4,4)", U,
    "Not blind. In this verifier's session the official score lines (project.html:367 and 378) and the annotation text (370-373, 382-384, 388-390) were displayed "
    "before any scoring, so a blind calibration against the rubric alone cannot be recorded. The two exemplars do sit at levels 1 and 4 (data-level attributes), "
    "and the annotations' cited passages exist (checked in this round).",
    "A verifier with no prior exposure to project.html:362-391 must score Exemplar A and Exemplar B from the rubric table (project.html:352-357) alone, with the "
    "data-scores and annotation paragraphs hidden, and record each criterion; the scores must be within one level of the official annotations.")
row("proj-ladder-scope", "2.6-ladder", "course/modules/CS/CS2/project.html:40-190, 260-340; curriculum/01-foundations.yaml:441-449", P,
    "Curriculum brief (O(1) mean and variance cumulative over every value seen, rolling min and max with monotonic deque, quantile sketch with a stated rank guarantee, prove "
    "Welford's update; deliverable streamstats.py, proof.md, design.md; grading both) matches the spec's Rung 3. Rung 1 and Rung 2 are annotated (Why notes, lab.completion blanks, "
    "expected output); Rung 4 is open-ended (project.html:400-406).")
row("proj-notation", "2.4-notation", "notation/notation.json; project.html math spans; grader files", P,
    "notation.json registers T, Phi/Phi^-1, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. Math spans in project.html use n, q, x_i, x_n, S_n, S_1, delta, varepsilon, a, i and \\bar, "
    "none of them a registered symbol; grep of the grader files finds no registered symbol used as math.")
row("proj-dag-concepts", "2.9-DAG", "project.html lede and Rung 3 links; L09.html, L10.html, L11.html; course/concepts.html", P,
    "check_dag CS2 PASS. Anchors resolve: L09 id=def-welford-algorithm, L10 id=def-monotonic-deque, L11 id=def-quantile-sketch, course/concepts.html id=mathematical-induction "
    "(M1, now a CS2 prerequisite per curriculum). No <dfn> on the page (grep count 0). Variance and quantile appear as plain formulas (architect decision Q2).")
row("proj-reading-citation", "2.1-citation", "project.html:408-414; references/references.json (cormen2022introduction)", P,
    "Reading list cites cormen2022introduction with no locator; page line 413 says no step is attributed to the textbook. verify_refs --unit CS2 live: 1 entry, 0 problems "
    "(gate-verify-refs).")
row("proj-exemplar-b-claims", "2.4-math", "project.html:376-391 (Exemplar B proof and design note)", P,
    "Re-derived: a = -delta/(n+1); sum (x_i - xbar_{n+1})^2 = S_n + n a^2; x_{n+1} - xbar_{n+1} = n delta/(n+1); S_{n+1} = S_n + n delta^2/(n+1) = S_n + delta(x_{n+1} - xbar_{n+1}). "
    f"The identity holds on 2000 random rational cases ({S}/project_numbers_r12.txt). Lab 3 values 8.313636 and 'True' are printed by the lab. "
    "Base case n=1 (S_1 = 0) is correct. Induction framing is redundant (the identity is direct) but not wrong.")
row("proj-spec-completeness", "2.6-spec", "project.html:238 (hours row) vs project.html:344 (write-up)", F,
    "A student would have to ask: must I prove the sketch's rank guarantee? Line 238 says 'Design the sketch, prove the rank guarantee the tests check, then run the short-stream "
    "tests against it.' (6 h), but the write-up section (line 344) asks for a proof only of Welford's update, and design.md must 'state the rank guarantee' with its probe set and limits "
    "(line 344) and C5 (line 356) has no proof criterion. The spec contradicts itself on what must be proved.",
    "Change project.html:238 to: 'Design the sketch, state the rank guarantee the tests check, then run the short-stream tests against it.' (Or, if a proof is wanted, add it to "
    "the design.md requirement at line 344 and to criterion C5 at line 356.)")
row("proj-context-length", "2.9-structure (BUILDER_RULES 5.2)", "project.html:196 (Context)", F,
    "BUILDER_RULES 5.2 requires 'Context: the real-world situation, in 2-4 sentences.' The Context dd has six sentences (sentence split of the dd text, "
    f"{S}/banned_and_context_r12.txt): (1) 'A monitoring team receives...'; (2) 'For each stream it needs...'; (3) 'You implement a small library...'; "
    "(4) 'The streams in the labs and the autograder are SIMULATED.'; (5) 'The autograder's stream is generated...'; (6) 'The labs' streams are written out...'.",
    "Merge to at most four sentences, for example: 'A monitoring team receives a stream of real numbers one at a time and needs, for each stream, the mean and variance so far, "
    "the minimum and maximum of the last few values, and a quantile estimate, all without a second pass. You implement a small library for these three tasks. The streams in the labs "
    "and the autograder are SIMULATED, and the autograder's stream is generated from the workspace seed by grader/instance.py.'")
row("proj-hours", "2.6-hours / 2.9-structure", "project.html:33, 233-241; course/modules/CS/CS2/index.html:29; curriculum/curriculum.json (CS2 hours 130)", P,
    "Project table sums to 30 (project.html:233-241). Hub data-hours-lessons=100 (index.html:29); L01-L11 declared 8+9+10+10+9+9+10+10+10+8+7 = 100 (check_pages PASS). "
    "100 + 30 = 130 = curriculum hours (curriculum.json CS2 hours 130). Project 30/130 = 23.1%, inside 10-40%.")
row("proj-named-conditions", "2.6-spec", "project.html:209 (Constraints, ten named conditions); grader/test_project.py must_raise calls", P,
    "Each of (1)-(10) has a must_raise test: (1) 171-180; (2) 183-186; (3) 215-218 and 221-222; (4) 450-459; (5) 478-481 and 484-485; (6) 470-475; (7) 673-680; "
    "(8) 791-797; (9) 692-710 (NaN 702-704); (10) 727-733. Each test asserts ValueError only for named conditions (must_raise / must_accept).")
row("proj-line195-inputs", "2.2-prose / 2.9", "project.html:195-198 (Inputs)", P,
    "20-400 finite values, one or six decimals (instance.py:37-38), offsets 0/10,000/1,000,000 (instance.py:29), window 2-30 (instance.py:39), eps 0.05/0.1/0.2 (instance.py:28,40), "
    "ten probes in [0,1] (instance.py:41), SIMULATED label (instance.py:47). Matches the page.")
row("proj-exemplar-namely-sentence", "2.2-prose / 2.9", "project.html:363", P,
    "Fixed in this delta: the namely-clause now names the probe set and epsilons of grader/instance.py (PROBES_FIXED, EPSILONS) and the wide epsilons (0.3, 0.5, 0.9), witness "
    "quantiles (0.1, 0.2500004, the q values in the wide-eps test) and stream lengths (1-8, twenty) that test_project.py sets. Exemplar B's constants are all among these.")
row("proj-inventory-test-claims", "2.6-spec / 2.9", "project.html:211 (test inventory paragraph) vs grader/test_project.py", P,
    "Every item of the inventory has a test: named-condition boundaries (window 0/1, eps 0/1e-6/0.999999/-1e-6, q 1.1/1.0, nextafter) 450-475, 673-724; empty object and NaN first value and infinite eps/q 166-222, 484, 673, 708, 796; "
    "Welford against Fraction on every prefix 2-20 (334-341) and on the whole stream (307-331); doubling x4 (352-359); rolling vs brute force on every position (499-506), eight widths (508-515), repeated values (489-497); "
    "sketch guarantee at ten probes (803-814), short streams (854-867), sorted (839-849), repeated (871-881), eps 0.3/0.5/0.9 (884-897), fixed 20-value witnesses (900-935); "
    "constant and single-value (825-835); default ddof 1 (204-212); monotone in q on 101 grid plus probes (817-822); count int and read-only (233-241); no printing (244-281); stdlib (130-141); "
    "bool/padded/string/None/whole-float/2.5 values and windows (284-294, 372-381, 534-655, 745-788); ddof strings, floats and None (384-422).")

# ---- grader ----
row("grader-instance", "2.6-instance", "course/modules/CS/CS2/grader/instance.py", P,
    "Read in full (50 lines). make_instance is deterministic (test_instance_is_deterministic 109-112); 500 distinct payloads for seeds 0-499 "
    f"({S}/instance_distinct_r12.txt). Every instance valid: suite seeds 0-49 pass (gate-run-graders).")
row("instance-docstring-counts", "2.2-numbers", "course/modules/CS/CS2/grader/instance.py:8-16", P,
    f"Re-run (naive_offsets_r12.py, exact Fraction reference, seeds 0-49): naive failures by offset {{0: '0 of 16', 10000: '22 of 23', 1000000: '11 of 11'}}; seed 41 is the only pass at 10,000 "
    f"({S}/naive_offsets_r12.txt). Docstring text matches. instance.py unchanged since pin ccaeeaf4.")
row("grader-reference", "2.6-autograder / 2.2 docstring", "course/modules/CS/CS2/grader/reference.py:95-100 (QuantileSketch docstring) vs :108-110", P,
    "Fixed in this delta: the docstring now says three parallel lists (the code keeps _values, _g, _delta). Invariants of the docstring checked on 400 random and tie-heavy streams after every add: "
    f"sum(g) = n, sorted values, g + delta <= floor(2 eps n) + 1, and every stored value has a copy whose 1-based rank lies in [S_i, S_i + delta_i]: 0 violations ({S}/sketch_docstring_r12.txt). "
    "Reference passes 50/50 (gate-run-graders).")
row("grader-starter", "2.6-autograder", "course/modules/CS/CS2/grader/starter.py", P,
    "Read in full. Suite on starter.py (seed 0): 172 failed, 3 passed (the three that do not call a method: instance determinism, validity, stdlib). Suite fails on the starter as project.html:206 says.")
row("grader-tests-rank", "2.6-autograder", "course/modules/CS/CS2/grader/test_project.py:800-935", P,
    "Read in full. Rank-guarantee tests use Fraction inequalities (guarantee_holds 736-742; 803-814; 900-935). Witness docstrings: q = 0.1, n = 20, eps 0.05 exact target 2 (float target 1, recomputed: "
    f"math.ceil(0.1*20 - 0.05*20) = 1, exact 2); q = 0.2500004 target 5, six-place 0.25 target 4 (recomputed, {S}/project_numbers_r12.txt).")
row("grader-docstring-delta", "2.6-autograder", "course/modules/CS/CS2/grader/test_project.py:884-889 (changed hunk); 244-281 (unchanged, re-read)", P,
    "Only hunk in test_project.py since pin ccaeeaf4 is the wide-eps docstring (884-889). Read in full. The test_classes_never_print and refused-call logic (244-281) re-read this round.")
row("grader-messages-no-expected-value", "2.6-autograder", "course/modules/CS/CS2/grader/test_project.py (all pytest.fail and must_raise messages)", P,
    "Every message read. Each names the property; none prints the expected value (must_raise prints the named condition; refuse_or_correct prints the property; messages that print "
    "repr(ddof) or the learner's answer print the input or the learner's own answer, never the reference answer).")
row("grader-wide-eps-docstring", "2.2 docstring / 2.6-autograder", "course/modules/CS/CS2/grader/test_project.py:884-889", P,
    "Fixed in this delta. Docstring now says quantile(1.0) 'passes the guarantee exactly when its answer is 2.0 or more'. Recheck for [1.0, 2.0], eps 0.3, q 1: "
    "answer v >= 2 gives below = 2 <= 2.6 and at-or-below 2 >= 1.4; answer v < 2 gives at-or-below <= 1 < 1.4 (fails). Claim exact.")
row("grader-new-mutants", "2.6-mutation", "ledgers/CS2/mutants/r4v_01..03", P, "All killed in the gate run (gate-mutate-cs2).")
row("grader-mutant-r5v01", "2.6-mutation", "ledgers/CS2/mutants/r5v_01_sketch_compression_folds_maximum_into_predecessor.py", P, "Killed in the gate run (gate-mutate-cs2).")
row("grader-mutant-v6-01", "2.6-mutation", "ledgers/CS2/mutants/v6_01_variance_default_ddof_is_population.py; test_project.py:204-212", P, "Killed in the gate run (gate-mutate-cs2).")
row("grader-new-mutants-v6-02-04", "2.6-mutation", "ledgers/CS2/mutants/v6_02..v6_04", P, "All killed in the gate run (gate-mutate-cs2).")
row("grader-new-mutants-r7v", "2.6-mutation", "ledgers/CS2/mutants/r7v_01..04", P, "All killed in the gate run (gate-mutate-cs2).")
row("grader-new-mutants-r8v", "2.6-mutation", "ledgers/CS2/mutants/r8v_01..03", P, "All killed in the gate run (gate-mutate-cs2).")
row("gate-mutate-r7-new", "2.6-mutation", "ledgers/CS2/mutants/r7v_01..04", P, "In the 163/163 gate run (gate-mutate-cs2).")
row("grader-new-mutant-r9v03", "2.6-mutation", "ledgers/CS2/mutants/r9v_03_sketch_new_tuple_delta_drops_successor_delta.py", P, "Killed in the gate run (gate-mutate-cs2).")
row("grader-new-mutants-r12v", "2.6-mutation", "ledgers/CS2/mutants/r12v_01_variance_one_value_returns_nan.py; r12v_02_rolling_deques_cleared_when_window_fills.py; r12v_03_welford_first_value_leaves_mean_at_zero.py", P,
    "Three new student-error mutants written this round (variance(1) with one value returns NaN; rolling deques cleared when the window fills; Welford mean left at 0 after the first value). "
    "Each is a complete module with a one-line docstring. Killed: r12v_01 by test_welford_sample_variance_of_one_value_raises; r12v_02 by test_rolling_ties_expire_with_their_index[2]; "
    "r12v_03 by test_welford_sample_variance_matches_exact_reference (seed 0). Each is listed in the fragment's mutants.")
row("grader-infinite-input", "2.6-autograder", "course/modules/CS/CS2/grader/test_project.py:431-444", P,
    "Read. Asserts a non-finite mean or variance, or a raise, after an infinite Welford value (project.html:209 states this outcome). Re-read this round, unchanged.")
row("grader-classes-never-print", "2.6-autograder", "course/modules/CS/CS2/grader/test_project.py:244-281; project.html:209", P,
    "Re-read this round. Covers variance(0), count, quantile(0.0), quantile(1.0), refused calls on fresh objects; fails on any output or warning. Matches the spec's never-print rule.")
row("grader-alternatives", "2.6-autograder (over-constraint)", "course/modules/CS/CS2/grader/test_project.py:825-835; ledgers/CS2/scripts/CS2-d-r12/alts/", F,
    "Five-plus alternative correct implementations (A-F below) pass 50/50, but alternative G is a correct implementation that fails two tests. G = reference with quantile(0.0) returning "
    "one unit below the smallest stored value. Its rank guarantee holds on all 30300 battery checks (alt_G_guarantee_r12.txt): at q = 0 the lower inequality is trivially true and the upper "
    "inequality needs #{x < v} = 0 <= eps n, which holds for v = min - 1. Yet test_sketch_constant_stream_returns_the_constant and test_sketch_single_value_returns_that_value demand "
    "quantile(q) == the constant at every probe (alt_G_suite_r12.txt: 50/50 seeds fail on the constant test; seed 0 pytest run also fails the single-value test). The spec's only "
    "tested property is the rank guarantee (plan 6.3, and project.html:211-212 describes these as 'constant-stream and single-value checks', not as a stated behaviour).",
    "Replace the equality checks at test_project.py:825-835 with guarantee checks: for each probe q, assert guarantee_holds(stream, sketch.quantile(q), q, EPS) on the constant stream "
    "[c]*40 and the one-value stream (keep the 'returns a float' check). Keep the page sentence (project.html:211) as is.")
row("grader-alt-r12-A-F", "2.6-autograder (alternatives)", "ledgers/CS2/scripts/CS2-d-r12/alts/alt_r12_A..F (A exact sorted list, floor+1 target; B Welford delta-squared (n-1)/n form, list-head deques, float target + 1e-9; C shifted sums, brute window; D weighted exact list; E reference with cap floor(2 eps n); F lazy compression every 50 adds)", P,
    f"suite.py seeds 0-49 on each: 0 of 50 failing for A, B, C, D, E, F ({S}/alts_r12_results.txt). Each was checked by the grader on all 50 seeds.")
row("grader-guarantee-battery", "2.6-autograder (battery)", "ledgers/CS2/scripts/CS2-d-r12/guarantee_battery_r12.py; guarantee_battery_long_r12.py", P,
    "Rank-guarantee battery, all 101 q values, 300 random and tie-heavy streams (n up to 150; seed 7): reference 30300 checks, 0 violations; alternative E 30300, 0; alternative G 30300, 0. "
    "Long battery (n up to 400, seed 23, 240 streams): reference 24240, 0 violations; lazy-compression F 24240, 0 (guarantee_long_r12v04.txt).")
row("grader-fuzz-round9", "2.6-autograder (battery)", "ledgers/CS2/scripts/CS2-d-r12/guarantee_battery_r12.py", P,
    "Re-run this round as the battery above (round 11's battery file is not reused). Reference: 0 violations in 30300 checks.")
row("grader-alt-round9", "2.6-autograder (alternatives)", "ledgers/CS2/scripts/CS2-d-r9/alts/alt_r9_a_exact.py .. alt_r9_e_exact_block.py", P,
    "Carried from round 11 (scripts/CS2-d-r9/alts/* byte-identical since the previous pin ccaeeaf4): each of the five alternatives passed 0 of 50 seeds in round 11. Alternatives A-F of this round also pass.")
row("mut-survivors", "2.6-mutation (equivalents)", "ledgers/CS2/equivalent/d8_01, d8_02, d9_04", P,
    "Carried from round 11 (ledgers/CS2/equivalent/* byte-identical since the previous pin ccaeeaf4): not counted as faults. Re-run this round: suite seeds 0-49, 0 of 50 failing each "
    f"({S}/equivalents_r12.txt). The equivalence arguments are in ledgers/CS2/equivalent/README.md (unchanged).")
row("equiv-m14_01", "2.6-mutation (equivalents)", "ledgers/CS2/equivalent/rank_target_without_clamp.py", P,
    f"Carried from round 11 (byte-identical). Re-run this round: suite seeds 0-49, 0 of 50 failing ({S}/equivalents_r12.txt); the clamp is not reached on any tested stream.")
row("instance-distinct-seeds", "2.6-instance", "course/modules/CS/CS2/grader/instance.py", P,
    f"500 distinct payloads for seeds 0-499; 20 sampled seeds give 20 distinct (mean, variance) pairs and 20 distinct sketch medians, all valid ({S}/instance_distinct_r12.txt; instance_variety_r12.txt).")

# ---- cards ----
row("cards-automated", "2.2 / cards structure", "course/modules/CS/CS2/cards.json (224 entries)", P,
    f"cards_check_r12.py: 224 entries; ids unique and CS2-cNNN; keys consistent (155 T, 69 C); every lesson L01-L11 has at least one card; every non-T grade has basis; every lesson exists; "
    f"per lesson L01 14, L02 22, L03 22, L04 20, L05 24, L06 15, L07 24, L08 26, L09 17, L10 15, L11 25 ({S}/cards_check_r12.txt).")
row("cards-sample", "2.7 cards sample", "course/modules/CS/CS2/cards.json (every 10th card, 23 cards read)", P,
    f"Read every 10th card by position (CS2-c001, c011, c021, c031, c041, c051, c061, c072, c082, c092, c102, c112, c122, c132, c142, c152, c173, c183, c205, c215, c220, c223, c232). "
    f"Each front/back checked against the cited lesson text; the numeric claims check out ({S}/cards_sample_and_dups_r12.txt).")
row("cards-changed-delta", "2.7 cards (changed since pin ccaeeaf4)", "cards.json: c097, c099, c138, c151, c205 changed; c232, c233, c234, c235 added", F,
    "Each changed or added card was checked against the current lesson text and the lab expected blocks (rows below). Eight are PASS; CS2-c097 is FAIL (unsupported lab attribution).",
    "See cards-c097.")
row("cards-c097", "2.7 cards (lab numbers)", "course/modules/CS/CS2/cards.json CS2-c097 (L07, grade C, basis 'Lab 1, Part C (one pair, one run)')", F,
    "Back: 'the memoized recursion stores 28 subproblems and makes 47 calls, the rest being 11 lookups of stored values and 8 base calls (Lab 1, Part C).' The split 11 and 8 is correct "
    f"(independent count, {S}/l07_split_r12.py: calls 47 = stored 28 + base 8 + lookups 11), but Lab 1 Part C does not print it (L07.html expected block line 503 prints table cells 49, stored 28, memo calls 47 only) and L07.html does not state it. "
    "A card attributes a number to a lab that does not print it.",
    "Either remove the split: 'No. On the LCS pair ACGTACG and TGCATGC the memoized recursion stores 28 subproblems and makes 47 calls (Lab 1, Part C), so the calls outnumber the subproblems.', "
    "or change the lab (owner: L07 builder) to print the lookup and base-call counts and cite that output.")
row("cards-c099", "2.7 cards (lab numbers)", "cards.json CS2-c099 (L07, C, basis Lab 1, Part C)", P,
    "LCS length 3 for ACGTACG/TGCATGC: L07.html expected block line 502 ('part C: LCS x = ACGTACG, y = TGCATGC, LCS length = 3'). Card is the lab's printed value.")
row("cards-c138", "2.7 cards (T, changed)", "cards.json CS2-c138 (L10, T)", P,
    "Theorem 2.2 (the deque invariant), L10.html:73, says the deque holds exactly the candidate indices (line 352 key-results row 'the deque holds exactly the candidate indices described in Theorem 2.2', grade T). The card's 'No' is correct: the window holds more values than the deque. Grade T with Theorem 2.2 is consistent.")
row("cards-c151", "2.7 cards (T, changed)", "cards.json CS2-c151 (L11, T)", P,
    "Corollary 2.6 (L11.html, 'Growth of the bound'): bound (L+1)(L+2)(L+3)/(3 eps) + (L+1). Recomputed (memory_bound_r12.py, memory_bound_r12.txt): L = 29, eps = 1/20: 30*31*32/0.15 + 30 = 198430 (below n = 10^9); exact sum at n = 10^9 is 198370. Card wording matches the lesson.")
row("cards-c205", "2.7 cards (T, changed)", "cards.json CS2-c205 (L11, T); L11.html Problem M3", P,
    "Problem M3 (L11.html): k_0 = 20 at eps = 1/10; 20th add compacts level 0 (10 items to level 1), 40th add compacts again, level 1 holds 20 items, below k_1 = 60, total weight 40. "
    "Recomputed: k_h = 2*ceil((h+1)(h+2)/(2 eps)) gives k_0 = 20, k_1 = 60. Card matches.")
row("cards-c232", "2.7 cards (C, added)", "cards.json CS2-c232 (L07, C)", P,
    "183 calls without a memo table: L07.html expected block line 504 'recursion with no memo table makes 183 calls' and the independent recount (twin code). Basis names the lab.")
row("cards-c233", "2.7 cards (C, added)", "cards.json CS2-c233 (L07, C; Proposition 3.5)", P,
    "49 table cells: expected block line 503 'table cells filled = 49'. 49 = 7*7 pairs with 1 <= i, j <= 7 (both strings have length 7). Proposition 3.5 ('cost of the LCS table', L07.html) states the fill computes exactly mn entries.")
row("cards-c234", "2.7 cards (C, added)", "cards.json CS2-c234 (L10, C)", P,
    "L10.html expected block line 210: 'window 30: ... largest deque size 10'. Card's '10, below the window size of 30' matches the printed value.")
row("cards-c235", "2.7 cards (T, added)", "cards.json CS2-c235 (L11, T); L11.html Problem R3", P,
    "Problem R3 (L11.html): sum_{h=0}^{12} (20(h+1)(h+2) - 1) = 20*910 - 13 = 18187. Recomputed from the Definition 2.1 capacities by memory_bound_r12.py (" + S + "/memory_bound_r12.txt): exact sum 18187 > n = 5000. Card matches the lesson.")
row("cards-lab-numbers", "2.2 / 2.7 cards (C-grade numbers vs lab output)", "cards.json grade C (69 cards)", F,
    "Every number on each card is present in its own lesson text (cards_check_r12.py: 0 absent). Lab attribution re-checked this round for the changed/added C cards (c097 FAIL, c099, c232, c233, c234 PASS) "
    "and carried from round 11 for the unchanged C cards (byte-identical).",
    "Fix CS2-c097 as in cards-c097.")
row("cards-duplicates", "2.7 cards (duplicates)", "cards.json full scan", P,
    f"No duplicate ids, fronts or backs (cards_check_r12.txt). Pairwise front similarity >= 0.8: 27 pairs ({S}/cards_sample_and_dups_r12.txt), each a distinct question (e.g. c030 push vs c031 pop; c184 vs c185 double rotations). None involves a changed or added card.")
row("cards-full-number-scan", "2.2 / cards numbers", "cards.json (all 224 entries)", P,
    f"Every number on every card's front and back appears verbatim in its own lesson text: 0 absent ({S}/cards_check_r12.txt).")
row("cards-count-observation", "2.2 cards counts", "cards.json per-lesson counts", P,
    "Per lesson: L01 14, L02 22, L03 22, L04 20, L05 24, L06 15, L07 24, L08 26, L09 17, L10 15, L11 25 (sum 224). Changed from round 11 by the four added cards (c232, c233 to L07; c234 to L10; c235 to L11).")
row("cards-c024", "2.7 cards", "cards.json CS2-c024 (L02, T)", P,
    "Carried from round 11 (cards.json entry byte-identical since the previous pin ccaeeaf4; not in this delta): the back's alpha = n/m comparison with the successful average holds.")
row("cards-c155", "2.7 cards", "cards.json CS2-c155; lab-CS2-L02 expected block", P,
    "Carried from round 11 (entry byte-identical since ccaeeaf4): Lab 2 printed 2.0078 at n = 128 and 3.0156 at n = 256; model 1 + 127/128 = 1.9922, 1 + 255/128 = 2.9922.")
row("cards-c035", "2.7 cards", "cards.json CS2-c035; lab-CS2-L03 rows", P,
    "Carried from round 11 (entry byte-identical since ccaeeaf4): 4514/1002 = 4.5050 is the largest sorted-list per-doubling ratio printed by Lab 3.")
row("cards-c174", "2.7 cards", "cards.json CS2-c174; lab-CS2-L03 rows", P,
    "Carried from round 11 (entry byte-identical since ccaeeaf4): 21095/10623 = 1.985785 is the smallest heap per-doubling ratio, at N = 512.")
row("cards-c227", "2.7 cards", "cards.json CS2-c227 (L05, T); L05.html Section 1", P,
    "Carried from round 11 (entry byte-identical since ccaeeaf4): the BST order property as stated in L05 line 23.")
row("cards-changed-c025-c087-c095", "2.7 cards", "cards.json CS2-c025, CS2-c087, CS2-c095", P,
    "Carried from round 11 (cards.json entries byte-identical since ccaeeaf4; not in this delta).")
row("cards-c033", "2.7 cards", "cards.json CS2-c033; text_L03 Proposition 1.5/1.6", P,
    "Carried from round 11 (cards.json entry byte-identical since ccaeeaf4; L03.html unchanged since ccaeeaf4).")
row("cards-c215", "2.7 cards", "cards.json CS2-c215 (L05, C); L05.html line 43 and Section 3", P,
    "Carried from round 11 (cards.json entry byte-identical since ccaeeaf4; L05.html unchanged since ccaeeaf4).")

# ---- mutants list: every mutant in ledgers/CS2/mutants with its killing test (from the gate run) ----
mutants = []
for line in mut_out:
    m = re.match(r"^KILLED (\S+\.py): (.*) -> (.*)$", line)
    if m:
        name, desc, killed = m.group(1), m.group(2), m.group(3)
        mutants.append({"id": name[:-3], "description": desc, "killed_by": killed})

fragment = {
    "unit": "CS2",
    "slice": "d",
    "round": 12,
    "verifier": "independent verifier (Haiku), round 12; did not build CS2",
    "pin": PIN,
    "base": BASE,
    "checkout": str(ROOT),
    "scratch": S,
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if any(r["status"] != P for r in rows) else "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since round-11 pin ccaeeaf4 (slice d files): project.html lines 218 and 363; grader/reference.py lines 95-100 (docstring only); grader/test_project.py lines 884-889 (docstring only); "
        "cards.json (c097, c099, c138, c151, c205 changed; c232-c235 added); ledgers/CS2/mutants r12v_01..03 (new, written by this verifier); scripts under CS2-d-r12 (this verifier's scratch). "
        "Every file of the slice was read in full this round (project.html 428 lines, grader/*.py, three project twins, all cards by sampling plus scripted full checks).",
        "Rubric calibration is not blind: the official scores and annotations were displayed to this verifier before scoring, so proj-rubric-calibration is UNVERIFIABLE and must be done by a fresh verifier.",
        "Lazy-compression sketch (compacts only every 50th add) is a correct implementation of the spec (the uncompressed structure satisfies the same invariants, and the guarantee held in 125,240 battery checks (101,000 short + 24,240 long) with 0 violations. It was first written as a mutant, found to be correct, and is kept as alternative F, not as a fault.",
        "ledgers/CS2/scripts/CS2-d-r12 already contained tracked scratch files from another verifier (commit fca6bb10). They were not modified; this verifier's files there are untracked and named *_r12*. ledgers/CS2/CS2-d.json at the pin held another round's fragment (round 15, pin 448548f); it is overwritten here as the task requires.",
        "Not run: the repo-wide ruff/mypy gates (scope limited to this slice); page_smoke on the whole unit (only project.html, as the rule for this slice); live network re-verification beyond verify_refs --unit CS2.",
        "No git commit or push was made. No course, tool, test, reference, curriculum or atlas file was edited.",
    ],
    "summary": "",
}
n_fail = sum(1 for r in rows if r["status"] == F)
n_unv = sum(1 for r in rows if r["status"] == U)
n_pass = sum(1 for r in rows if r["status"] == P)
fragment["summary"] = (
    f"CS2 slice d, round 12: FAIL. Rows {len(rows)} (pass={n_pass} fail={n_fail} unverifiable={n_unv}). "
    f"Gates all PASS (mutate_graders 163/163 rc 0; run_graders 50/50; collect 175 x 50; labs 14/14; page_smoke project; check_pages/dag/projects; ruff; mypy; verify_refs; relevant pytest). "
    "Non-PASS: proj-spec-completeness (sketch proof required by hours row but not by write-up), proj-context-length (Context has 6 sentences, BUILDER_RULES 5.2 says 2-4), "
    "grader-alternatives (constant-stream and single-value tests over-constrain a correct sketch: alternative G), cards-c097 (lab attribution of 11 lookups and 8 base calls not printed by Lab 1), "
    "cards-changed-delta and cards-lab-numbers (follow from c097), proj-rubric-calibration (UNVERIFIABLE, not blind). Mutants: 163 of 163 killed, including 3 new this round."
)
out = ROOT / "ledgers/CS2/CS2-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants), "verdict", fragment["verdict"])
