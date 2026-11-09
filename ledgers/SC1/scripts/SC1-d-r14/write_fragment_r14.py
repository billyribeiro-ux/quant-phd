"""Write the round-14 SC1-d fragment (ledgers/SC1/SC1-d.json) from the round-13 row list and this round's evidence.

Every round-13 row id is kept. Rows are re-decided this round from fresh checks (see out/ and scripts/), or carried
only where the cited subject is byte-identical since the previous pin (prefix 'Carried from round 13').
Usage: write_fragment_r14.py <checkout root>
"""
import json
import re
import sys
from datetime import datetime, timezone

root = sys.argv[1]
S = f"{root}/ledgers/SC1/scripts/SC1-d-r14"
O = f"{S}/out"
r13 = json.load(open("/Users/billyribeiro/.fanout/frags/E-SC1-d.round13.json", encoding="utf-8"))
r13_by_id = {r["id"]: r for r in r13["rows"]}
ids13 = [r["id"] for r in r13["rows"]]

FRESH = "Re-verified round 14 on 8e5751c: "
CARRY = "Carried from round 13 (byte-identical since the previous pin: {files}): "

# id -> (status, evidence, fix). Fix is required when status != PASS.
D = {}

def p(i, ev):
    D[i] = ("PASS", FRESH + ev, "")

def c(i, files, ev):
    D[i] = ("PASS", CARRY.format(files=files) + ev, "")

def f(i, ev, fix):
    D[i] = ("FAIL", FRESH + ev, fix)

GATES = "gate outputs in " + S + "/out/"
p("SC1-d-r10-gates", "check_pages, check_dag, check_projects (unit SC1) PASS; run_labs 11/11; run_graders 0-49 50/50; mutate_graders 80/80 killed; page_smoke project PASS; ruff, mypy --no-incremental PASS (" + GATES + ").")
p("SC1-d-r10-page-smoke", "page_smoke.py --unit SC1 --pages project: 'PASS', in-browser grader 136 tests pass (out/page_smoke_sc1_project.txt).")
p("SC1-d-r10-lab-twins", "scripts/check_labs_r14.py: Lab 1 and Lab 3 page code == twin; Lab 2 page keeps the ___ blanks by convention (Ruling 11) and differs from its twin only on those two lines; expected block == twin stdout for all three (out/check_labs_r14.txt); twins run under python -I -W error, exit 0 (out/twin_project_{1,2,3}.txt).")
p("SC1-d-r10-registry-live", "verify_refs.py --unit SC1 (live): '1 of 560 entries, 0 problems' (out/verify_refs_unit_sc1.txt); reading list at project.html reading section cites shreve2004stochastic only.")
p("SC1-d-tools-gates", "ruff check and ruff format --check on grader and tests/labs/SC1: clean (out/ruff_check.txt, out/ruff_format.txt); mypy --no-incremental: 385 files, no issues (out/mypy_nocache.txt).")
p("SC1-d-r11-run-graders", "run_graders.py --unit SC1 --seeds 0-49: 50/50 (out/run_graders_unit.txt); 0-199: 200/200 (out/run_graders_0_199_r14.txt).")
p("SC1-d-r11-mutate-gate", "mutate_graders.py --unit SC1 --seeds 0-9: 80/80 killed (out/mutate_graders_unit_r14.txt). The 80 files include 4 slice-a lab mutants (SC1a-r13-*), see SC1-d-r10-mutant-folder-hygiene.")
p("SC1-d-ladder", "project.html ladder (lines 40-49): rung 1 worked example (Lab 1), rung 2 completion (Lab 2), rung 3 project (spec, autograder, report), rung 4 stretch; check_projects.py --unit SC1 PASS.")
p("SC1-d-grading-mode", "project.html grading mode paragraph names both the autograder (grader/test_project.py) and the rubric; the suite count '136 tests' equals collect-only on the reference (out/collect_count_r14.txt: 136 tests collected).")
p("SC1-d-spec-signatures", "project.html spec 'Required outputs' lists the five signatures; grader/starter.py lines 16, 21, 26, 31, 36 match them exactly (read both).")
p("SC1-d-spec-rounding-statement", "project.html Constraints (rounding rule: unrounded value, six places, three significant digits for differences, horizon and level three decimals) matches the Lab 1 and Lab 3 print formats (out/twin_project_1.txt, _3.txt).")
p("SC1-d-hours", "project.html table#hours: 2+3+10+8+3+2 = 28 = data-hours-project=28 (line 33) = hub split 72+28 (course/modules/SC/SC1/index.html:29). Own estimate of the deliverables: about 31 h (rung 1 about 2 h, rung 2 about 3 h, three proofs about 10 h, engine and 136-test suite about 10 h, report about 4 h, self-assessment about 2 h), within 30 percent of 28.")
p("SC1-d-spec-grid-table", "project.html Conventions bullet 2 (t_k = kH/n, k = 1..n) and bullet 3 (sd sqrt(H/n_steps), path by path, step by step) match grader/reference.py _grid_paths (lines 27-39) and discrete_max_exceedance (line 75).")
p("SC1-d-spec-tolerance-statement", "project.html Conventions bullet 5 states 1e-10 for reflection_tail; test_project.py reflection tests use 1e-10 (grep verified). Statement and grader agree; the plan's 1e-12 is a separate row (SC1-d-plan-tolerance).")
p("SC1-d-spec-n41-method", "project.html Constraints (n = 41 must not list walks) matches test_srw_integers_are_exact_for_a_long_odd_walk (test_project.py:315-336, 1 s budget); binomial and DP alternatives pass it (out/alternatives_r14.txt).")
p("SC1-d-spec-constraints-raise", "project.html Conventions bullet 8 lists the ValueError conditions; reference.py raises exactly those (lines 20-23, 48-51, 67-70, 81-84, 93-96) and must_raise is used only for named conditions (test_project.py grep).")
p("SC1-d-ag-reference", "run_graders 0-49 50/50 and 0-199 200/200 on grader/reference.py (out/run_graders_unit.txt, out/run_graders_0_199_r14.txt); 136 passed in a scratch copy with reference as bm_checks.py.")
p("SC1-d-ag-starter", "starter.py raises NotImplementedError; the suite on starter.py: '132 failed, 4 passed' (out/starter_fails_r14.txt); the 4 passing tests use only instance.py.")
p("SC1-d-ag-instances", "grader/instance.py read in full; make_instance matches project.html Inputs and Draw order (horizon, level, grid size, path count from the seeded generator); 19 sampled seeds all valid with distinct levels, tails and one-step estimates (out/sample_instances_r14.txt).")
p("SC1-d-ag-count", "collect-only on reference: 136 tests (out/collect_count_r14.txt); project.html:7 meta description, 226 and 297 all say 136.")
p("SC1-d-ag-messages", "read the helpers (test_project.py 45-117) and the messages at 187, 391, 555: each names the property and does not print an expected value.")
p("SC1-d-ag-overconstraint", "five new round-14 correct alternatives (ledgers/SC1/scripts/SC1-d-r14/alternatives/alt_r14_1..5) pass seeds 0-49 50/50 each (out/alternatives_r14.txt): erf tail and DP walk counts; streaming maxima and count-based SE; normal CDF with statistics.stdev and (position, max) DP; symmetry bounds with a different tail rounding; sqrt(H)/sqrt(n) sd with fsum.")
p("SC1-d-ag-alternatives-ok", "the 5 round-14 alternatives pass 0-49 (above); the 6 previously failing repathed copies (alt_r8_b, alt_r8_c in SC1-d-r8, SC1-d-r9 repathed, SC1-d-r11) pass 50/50 each (out/prior_changed_alternatives_r14.txt).")
c("SC1-d-r13-prior-alternatives", "ledgers/SC1/scripts/SC1-d-r4, -r8, -r9, -r10, -r12 alternatives (byte-identical folders)", "the 18 unchanged correct alternatives passed on the round-13 suite (ledgers/SC1/scripts/SC1-d-r13/out/prior_correct_alternatives_r13.txt); the grader's code is unchanged since the previous pin (the only test_project.py hunks are a docstring and a comment, git diff e919577..8e5751c). The two changed copies, alt_r8_b and alt_r8_c, now pass 50/50 this round (out/prior_changed_alternatives_r14.txt).")
for i in ("SC1-d-ag-mutants-plan", "SC1-d-ag-mutants-own", "SC1-d-ag-mutants-survivors", "SC1-d-ag-mutants-seed", "SC1-d-ag-mutants-seed-offset", "SC1-d-ag-mutants-r3", "SC1-d-ag-mutants-r4-new", "SC1-d-ag-mutants-r5-new", "SC1-d-ag-mutants-r6-new", "SC1-d-ag-level-equality-survivors", "SC1-d-ag-mutants-r7-new", "SC1-d-r7-mutants-all", "SC1-d-r7-mutants-new", "SC1-d-r8-mutants-new", "SC1-d-r9-mutants-new", "SC1-d-r10-new-mutants", "SC1-d-r11-new-mutants", "SC1-d-r11-m09", "SC1-d-r11-m09-coverage-note", "SC1-d-r10-mutant-seed-coverage", "SC1-d-r12-mutants-all-existing", "SC1-d-r12-mutants-new-r12-01-04", "SC1-d-r12-mutant-tiny-level", "SC1-d-r12-mutant-tiny-time", "SC1-d-r13-mutants-new"):
    p(i, "mutate_graders.py --unit SC1 --seeds 0-9 (out/mutate_graders_unit_r14.txt): the mutant file named in this row's location is KILLED; killer test in the mutants list of this fragment.")
p("SC1-d-r7-alt4-ruling10", "FINAL-ARCHITECT-RULINGS.md item 10: a float-based alternative wrong on a stated exact rule is a mutant; plan 5.7(4) Box-Muller with another draw order is therefore r12_01_step_major_draw_order.py, killed by test_two_paths/draw tests (out/mutate_graders_unit_r14.txt).")
p("SC1-d-r11-recompute", "scripts/recompute_r14.py recomputes every seed-0 number from grader/reference.py and the instance: tail 0.086497, quadrature diff 8.73e-15, one-step 0.059548 (se 0.010735), target 0.043248 (target se 0.009218), band 0.048142, grid rows and nested counts (out/recompute_r14.txt).")
p("SC1-d-r11-collect", "collect-only on reference in a scratch workspace: 136 tests (out/collect_count_r14.txt).")
p("SC1-d-r11-mypy-ruff", "ruff check and format on course/modules/SC/SC1/grader and tests/labs/SC1; mypy --no-incremental: PASS (out/ruff_check.txt, out/mypy_nocache.txt).")
D["SC1-d-r11-alternatives"] = ("PASS", FRESH + "the SC1-d-r11 copies of alt_r8_b and alt_r8_c load no external file and pass 50/50 on the suite (out/prior_changed_alternatives_r14.txt); the old absolute reference path is gone (grep for /Users/ and verifyE in the scripts folders: no hits).", "")
for i in ("SC1-d-r7-page-smoke", "SC1-d-r10-page-smoke-project", "SC1-d-r8-page-smoke", "SC1-d-r12-gate-page-smoke"):
    p(i, "page_smoke.py --unit SC1 --pages project: PASS, in-browser grader 136/136 (out/page_smoke_sc1_project.txt).")
p("SC1-d-ag-page-smoke", "project.html grader panel (section#grader data-unit=SC1, data-suite=test_project.py, data-solution=bm_checks.py): page_smoke runs the panel suite: 136 pass.")
p("SC1-d-r7-gates-full", "ruff, mypy, check_pages, check_dag, check_projects, run_labs, run_graders, mutate_graders and pytest on the labs and page tools all run this round (out/*.txt).")
p("SC1-d-r12-gate-page-tools", "check_pages.py --unit SC1 PASS, check_dag.py --unit SC1 PASS, check_projects.py --unit SC1 PASS (out/check_pages_unit.txt, out/check_dag_unit.txt, out/check_projects_unit.txt).")
p("SC1-d-r12-gate-run-labs", "run_labs.py --unit SC1: PASS (11/11) (out/run_labs_unit.txt).")
p("SC1-d-r12-gate-run-graders", "run_graders.py --unit SC1 --seeds 0-49: PASS (out/run_graders_unit.txt).")
p("SC1-d-r12-gate-mutate", "mutate_graders.py --unit SC1 --seeds 0-9: 80/80 killed (out/mutate_graders_unit_r14.txt).")
p("SC1-d-r12-gate-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental (385 files): PASS (out/ruff_check.txt, out/ruff_format.txt, out/mypy_nocache.txt).")
p("SC1-d-r12-gate-pytest", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_memo_exemplars.py: all pass (out/pytest_labs.txt).")
p("SC1-d-r12-gate-verify-refs", "verify_refs.py --unit SC1 (live): 1 of 560, 0 problems (out/verify_refs_unit_sc1.txt).")
p("SC1-d-r12-collect-count", "collect-only on reference in a scratch copy: 136 tests (out/collect_count_r14.txt). The checkout's own collect fails without bm_checks.py, as the suite requires a solution module (out/collect_only_grader.txt).")
p("SC1-d-r12-sample-20-seeds", "scripts/sample_instances_r14.py: 19 seeds (0, 3, ..., 48, 1234, 987654) all valid; levels, tails and one-step estimates all distinct (out/sample_instances_r14.txt).")
p("SC1-d-r7-instances-sample", "instance.py read in full; sample of 19 seeds valid and distinct (out/sample_instances_r14.txt).")
p("SC1-d-r7-starter-fails", "starter.py on the suite: 132 failed, 4 passed (out/starter_fails_r14.txt).")
p("SC1-d-r7-reference-sweep-500", "run_graders.py 0-199: 200/200 (out/run_graders_0_199_r14.txt). Seeds 200-499 not re-run this round; the 0-199 sweep is the evidence.")
p("SC1-d-r8-reference-sweep", "run_graders.py 0-199: 200/200 (out/run_graders_0_199_r14.txt).")
c("SC1-d-r7-alternatives-sweep", "ledgers/SC1/scripts/SC1-d-r13/alternatives/ (byte-identical folder)", "the round-13 folder's five alternatives passed 0-49 on the round-13 suite; the suite's code is unchanged since then (git diff e919577..8e5751c shows only comment and docstring lines in test_project.py). Round-14 alternatives: see SC1-d-ag-overconstraint.")
c("SC1-d-r12-alternatives", "ledgers/SC1/scripts/SC1-d-r12/alternatives/ (byte-identical folder)", "the five round-12 alternatives passed 0-49 on the round-13 suite (round-13 fragment); the suite's code is unchanged since then (comment and docstring hunks only).")
p("SC1-d-r7-numbers-recompute", "scripts/recompute_r14.py: every number on the page for seed 0 recomputed from reference.py and instance.py (out/recompute_r14.txt).")
p("SC1-d-numbers-prose", "project.html prose numbers recomputed (lines 37, 53, 223-239, 430, 463-606): tail 0.086497, 1.52 = 0.016300/0.010735, 1.77 = 0.016300/0.009218, 0.14 = 0.001799/0.012870, 0.026948, 0.037215, 0.020788, -0.001799, 0.004361, 1588 = 2*794 (out/recompute_r14.txt). The one wrong prose number, 661 words, is SC1-d-r14-exemplarB-wordcount.")
p("SC1-d-numbers-target-se", "Lab 1 prints target standard error 0.009218 (out/twin_project_1.txt); the page's 1.77 target standard errors at line 430 recomputed (out/recompute_r14.txt).")
p("SC1-d-r7-numbers-target-se", "same as SC1-d-numbers-target-se: 0.016300/0.009218 = 1.7683 (out/recompute_r14.txt).")
p("SC1-d-hunk-standard-error-sentence", "project.html Conventions bullet 3: sample sd with divisor N-1 over sqrt(N) equals sqrt(p(1-p)/(N-1)); algebra checked and the reference uses that formula (reference.py lines 68-72).")
p("SC1-d-hunk-no-more-often", "project.html Context: a grid maximum reaches a level no more often than the continuous maximum, because the grid is a subset of [0,H] on each path (Conventions bullet 2); true by the pathwise argument and by the shared-path counts (out/recompute_r14.txt: nested coarse <= fine).")
p("SC1-d-hunk-filtration", "project.html:231 defines the filtration and stopping-time sigma-algebra by reference to Lesson 5 Sections 1 and 3; L05 defines both (grep verified, L05.html).")
p("SC1-d-hunk-one-step-target-se", "project.html Lab 1 band and interpretation (lines 57, 162): target se 0.009218, band 0.048142, difference 0.016300 (out/twin_project_1.txt).")
p("SC1-d-index-rung2-text", "project.html:45 rung 2 text and index.html placement (lines 72-74): nine items, 80 percent bar, 8 of 9 = 88.9 percent, 7 of 9 = 77.8 percent (arithmetic checked); index.html changed one line (Assumption 2.1(a)-(c)) which the rung 2 text does not cite.")
p("SC1-d-exemplar-a-scope", "project.html exemplar A (lines 465-517, byte-identical since the previous pin): Summary states 'The results hold for every grid, as the run shows' from one seed; annotation C4 level 3 miss is correct.")
p("SC1-d-exemplarB-onestep-claim", "project.html exemplar B The checks (line 547, revised): 0.086497, 9.13e-15, 0.043248, 0.059548, 0.016300, 0.048142, 1588, 794 all match out/recompute_r14.txt and out/twin_project_*.txt.")
p("SC1-d-exemplarB-proof", "project.html exemplar B appendix P1-P3 (lines 583-591) read line by line: P1 steps (freezing by A4(b), stopping time by A4(c), joint measurability A4(g), F_rho measurability A4(h), A3 for rho bounded) and the 1/2 symmetry are correct; P2 erfc substitution checked; P3 limit checked.")
p("SC1-d-exemplarB-p1-assumptions", "exemplar B 'Assumptions for P1' (line 584): A0, A3, A4(b), A4(c), A4(g), A4(h) match L05 items (b), (c), (g), (h) and A3 (grep L05.html verified).")
p("SC1-d-r12-P1-proof", "project.html:244-250 P1 statement and assumption list: A0, A3, A4(b), (c), (g), (h) of Lesson 5 (L05.html items verified); statement 2 P(M_t>=a) = 2P(B_t>=a) (correct, proof of exemplar B re-derived).")
p("SC1-d-r12-P2-P3-proofs", "project.html:256, 262 statements; exemplar B P2 (erfc(x) = 2(1 - Phi(x sqrt 2)) with x = a/sqrt(2t)) and P3 (P(tau_a < inf) = lim erfc(a/sqrt(2n)) = 1) re-derived and correct.")
p("SC1-d-statements", "project.html:243-263 statements and assumption lists read in full; each cited Lesson 5 item and Lesson 1 Definition 1.1 exists (grep verified).")
p("SC1-d-statements-recheck-P2", "project.html:256 P2 statement and its two assumptions re-read; correct.")
p("SC1-d-A1-label", "project.html Lab 1 header and expected output carry SIMULATED (line 'label SIMULATED' in the printed instance line, out/twin_project_1.txt).")
p("SC1-d-A3-A4-usage", "project.html:243, 247 cite A3 and A4(b), (c), (g), (h) of Lesson 5; L05.html lists A3 (strong Markov, bounded stopping times) and A4 items (b) freezing, (c) hitting times, (g) joint measurability, (h) measurability at a stopping time (grep verified).")
p("SC1-d-L05-A4-i", "project.html has no A4(i) reference (grep count 0 this round); L05 uses A4(i) only in its own text.")
p("SC1-d-lab1-run", "tests/labs/SC1/lab-SC1-project-1.py under python -I -W error: exit 0; output equals the page's expected block (out/twin_project_1.txt; out/check_labs_r14.txt).")
p("SC1-d-lab1-docstring", "twin docstring lines 1-14 read: six-decimal rounding from the unrounded value, Simpson difference in three significant digits, H and a printed to three decimals, N an integer (matches the printed lines).")
p("SC1-d-lab2-run", "tests/labs/SC1/lab-SC1-project-2.py under -I -W error: exit 0; output equals the page's expected block (out/twin_project_2.txt).")
p("SC1-d-lab2-attribution", "project.html Lab 2 interpretation: 'Corollary 1.4 of Lesson 6, proved from Proposition 1.3'; L06.html has Proposition 1.3 (discrete reflection identity) and Corollary 1.4 (discrete tail identity) with that content (grep verified).")
p("SC1-d-lab3-run", "tests/labs/SC1/lab-SC1-project-3.py under -I -W error: exit 0; output equals the page's expected block (out/twin_project_3.txt).")
p("SC1-d-lab3-onestep-interp", "project.html Lab 3 interpretation (line 430): 0.001799 = 0.14 of 0.012870; 0.016300/0.010735 = 1.52; 0.016300/0.009218 = 1.77; 1588 = 4096 walks reaching 3 (out/recompute_r14.txt). The 'drawn on different paths' wording is SC1-d-r14-separate-paths.")
p("SC1-d-lab3-docstring", "twin docstring lines 1-17 read: the draw order, the nested grids and the rounding rule match the code (out/twin_project_3.txt).")
p("SC1-d-labs-pytest", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_memo_exemplars.py: all pass (out/pytest_labs.txt).")
p("SC1-d-discretization-bias", "project.html:236 bias definition: P(M_H>=a) - P(max B_tk >= a) is never negative (grid maximum is at most M_H on each path); Lab 3 shows -0.001799 at 64 steps from sampling noise, as the sentence says (out/twin_project_3.txt).")
p("SC1-d-monte-carlo-term", "no 'Monte Carlo' on project.html (grep count 0); the page says 'simulation' and 'seeded paths' throughout.")
p("SC1-d-scope-words", "project.html scope words (every, all, only, always, never, exactly, any, same) read in context; each universal claim is either a pathwise identity on the same paths or a stated limit (rounding, grid, seed). No unsupported universal claim beyond SC1-d-r14-separate-paths.")
p("SC1-d-process-words", "project.html learner text searched for TODO, TBD, placeholder, verifier, builder, round, agent, Claude, batch: no hits (grep this round).")
p("SC1-d-banned-structure", "project.html section order matches the brief and check_pages.py (PASS); no banned headings found on read-through.")
p("SC1-d-banned-and-process-words", "as SC1-d-process-words: no banned or process words in learner text (grep this round).")
p("SC1-d-r12-banned-and-process-words", "as SC1-d-process-words (grep this round).")
p("SC1-d-dag", "check_dag.py --unit SC1: PASS; concept links stopping-time and normal-distribution resolve to concepts.html ids (grep verified); 'Simpson's rule' is defined inline at its first use (Lab 1 hypothesis).")
p("SC1-d-notation", "notation/notation.json: T is registered for another meaning, and the page uses H (project.html Conventions bullet 1); Phi = standard normal CDF (module M4) as on the page; macros used \\Prob, \\Normal, \\indic are registered; other commands are standard LaTeX.")
p("SC1-d-r12-notation", "as SC1-d-notation (LaTeX commands listed and checked against notation.json macros this round).")
p("SC1-d-define-before-use", "project.html: running maximum (lede), simple random walk (Rung 2, line 45), grid maximum and standard error (Rungs paragraph), stopping time and filtration (Conventions 231), pathwise and discretization bias (232, 236) all defined before use; first-passage at line 7 and 37 refers to Lesson 8 and is defined at 231.")
p("SC1-d-pathwise-define-before-use", "course/modules/SC/SC1/L01.html (changed hunks): the word 'pathwise' does not occur in L01.html (grep count 0); project.html first uses 'pathwise' at 232, where it is defined.")
p("SC1-d-r12-pathwise-only-l01", "L01.html grep for 'pathwise': 0 hits this round (the pathwise use that round 13 flagged is gone).")
p("SC1-d-rubric-observable", "project.html rubric table (lines 449-459) read cell by cell; every level names an observable element (quoted sentences, counts, assumptions listed, numbers printed or not). No vague descriptor found.")
p("SC1-d-rubric-levels-cumulative", "project.html scoring rule (line 445): level 2 is any attempt that misses a level-3 element, level 1 is the absence its cell names; each level contains the one below.")
p("SC1-d-calib-A", "blind scoring (scripts/blind_exemplars_r14.py output ledgers/SC1/scripts/SC1-d-r14/out/blind_exemplars_r14.txt, annotations and verdicts stripped; scored before the annotated passages were read): C1 1, C2 2, C3 2, C4 2, C5 1; official data-scores 1,2,2,2,1: all within one level.")
p("SC1-d-calib-B", "blind scoring of exemplar B (annotations stripped, scored before the annotated text was read): C1 4, C2 4, C3 4, C4 3, C5 4; official data-scores 4,4,4,3,4 (line 519). The round-13 C3 gap (the unprinted 794 count) is gone: the checks passage no longer quotes a count at 4 or above. Within one level on every criterion.")
p("SC1-d-r12-blind-exemplar-A", "as SC1-d-calib-A: blind 1,2,2,2,1 against official 1,2,2,2,1.")
p("SC1-d-r12-blind-exemplar-B", "as SC1-d-calib-B: blind 4,4,4,3,4 against official 4,4,4,3,4.")
p("SC1-d-exemplar-a-annotations", "exemplar A annotations (lines 474-512) checked against the blind text: C4 level 3 miss (every grid claim), C3 level 3 miss (no rounding statement), C1 level 3 miss (no A3 for P1), C5 level 1 (no numbers). Accurate.")
p("SC1-d-exemplar-a-annotations-P1", "exemplar A appendix annotations (lines 500-501): P1 lists no assumptions and the symmetry step names none; accurate.")
p("SC1-d-r12-exemplarA-annotation-C3", "exemplar A annotation at line 487 (C3 level 2): 1.52 is derived (printed in Lab 3's interpretation prose, not by the lab program), so 'printed by neither lab' is accurate as to lab output; accurate.")
p("SC1-d-exemplarA-claim", "exemplar A verdict (line 467): C1 1, C2 2, C3 2, C4 2, C5 1 with reasons that match the blind text and annotations.")
p("SC1-d-exemplarB-numbers", "project.html exemplar B passages: every number is printed by Lab 1 or Lab 3, or is a difference or identity of printed values (out/twin_project_1.txt, _3.txt; out/recompute_r14.txt). The ≥4 walk count is no longer quoted.")
p("SC1-d-r12-exemplarB-numbers-values", "all exemplar B number values recomputed (out/recompute_r14.txt): correct. The body word count '661' is wrong, see SC1-d-r14-exemplarB-wordcount.")
f("SC1-d-r12-annotations-B-accuracy", "exemplar B annotations (lines 529-598): the C5 level 3 annotation ('says that the grids the brief lists are drawn on separate paths') is inaccurate, because the grids share one seeded normal stream (out/shared_stream_r14.txt); the other annotations are accurate, and the verdict's 'printed by Lab 1 and Lab 3' is now true.", "Rewrite the C5 level 3 annotation and the rubric's C5 level 3 cell to state the shared stream, as in SC1-d-r14-separate-paths.")
f("SC1-d-r12-exemplarB-brief", "exemplar B says it is 'written to this brief'. Brief item 1 (Summary: 'the one number that shows each holds') is not met for P3: the Summary says 'no printed number checks P3' (project.html Summary passage). Items 2 (grids and draw order in Setup) and 3 (no unprinted count) are now met.", "Either print a number that checks P3 (a Lab with a first-passage check) and quote it in the Summary, or amend brief item 1 to allow a stated limit for a result with no printed number, and cite that amendment in the brief.")
p("SC1-d-r12-exemplarB-brief-length", "exemplar B body (five sections): 659 words by the brief's rule (out/word_counts_r14.txt), inside 400-900; Summary 80 words, inside 'at most 80'. The page's '661' is wrong (see SC1-d-r14-exemplarB-wordcount).")
p("SC1-d-exemplarB-proof-structure", "exemplar B appendix (lines 583-591): assumptions listed before each of P1, P2, P3; statements follow; order matches the brief (appendix after body).")
p("SC1-d-exemplarB-p1-freezing", "exemplar B P1 (line 585): A4(b) applied to Z = (t - rho, 1_K) and Y = restarted path, with f bounded and jointly measurable (by A4(g)); the expectation f-bar is 1/2 1{z2=1} 1{z1>0}; correct.")
p("SC1-d-r12-lab-numbers", "tests/labs/SC1 and project.html Labs 1-3 numbers match (out/check_labs_r14.txt; out/recompute_r14.txt).")
p("SC1-d-r12-page-vs-twin", "scripts/check_labs_r14.py: Lab 1 and Lab 3 page code == twin; Lab 2 differs only on its two blank lines (Ruling 11) (out/check_labs_r14.txt).")
p("SC1-d-r12-walk-identity", "project.html Lab 2 identity and exemplar B checks: walks reaching 3 = 1588 = 794 + 794 = 2 * 794; for n = 12 walks ending at 3 or above equal walks ending at 4 or above (even endpoint); enumeration confirms 1588 (out/recompute_r14.txt).")
p("SC1-d-r12-hours", "project.html table#hours sums to 28 (recomputed); estimate in SC1-d-hours.")
p("SC1-d-r12-spec-tolerance-and-errors", "project.html:235 (1e-10 tolerance) and :238 (ValueError conditions) agree with test_project.py and reference.py; the plan's 1e-12 is recorded as SC1-d-plan-tolerance.")
f("SC1-d-spec-tolerance-plan", "plans/SC1-build-plan.md §5.5 says the erfc check is to within 1e-12; project.html:235 and the grader's reflection tests use 1e-10. No ruling in plans/FINAL-ARCHITECT-RULINGS.md or plans/SC1-open-items.md records the change.", "Either tighten the page and the grader to 1e-12 (a 1e-12 bound still passes the reference and all five alternatives), or record the architect ruling in plans/SC1-open-items.md.")
f("SC1-d-plan-tolerance", "same as SC1-d-spec-tolerance-plan: plan §5.5 (1e-12) vs project.html:235 and test_project.py (1e-10); unrecorded deviation.", "Same as SC1-d-spec-tolerance-plan.")
p("SC1-d-r12-reading-and-registry", "project.html reading list cites shreve2004stochastic at book level; references.json record: Shreve, Stochastic Calculus for Finance II, 2004, status verified, openlibrary (read this round).")
p("SC1-d-registry", "references/references.json record shreve2004stochastic: title, author Steven E. Shreve, year 2004, status verified (read this round; verify_refs live: 0 problems).")
p("SC1-d-reading-disclosure", "project.html reading section: 'at book level, with no passage or theorem number attributed to it' (no locator on page).")
p("SC1-d-privacy-claim", "project.html:289 and footer: code and self-assessment kept in this browser; course/assets/js/store.js uses IndexedDB in the learner's browser with a fallback (read this round).")
f("SC1-d-exemplar-naming", "plans/SC1-build-plan.md §5.4: exemplar-a is data-level 4 and exemplar-b data-level 2, and both are 'fully written proofs and reports'. project.html:465 gives exemplar-a data-level 2 and exemplar-b data-level 4 (line 519), and calls exemplar A 'an excerpt, not a full report' (line 463). No ruling records the change.", "Either swap the data-level attributes and make exemplar A a full report, or record the architect ruling for the excerpt and the level swap in plans/SC1-open-items.md.")
p("SC1-d-dfn-policy", "project.html has no <dfn> (grep count 0); concept links only (check_dag PASS).")
p("SC1-d-exemplar-claims", "project.html exemplar claims: A is 'an excerpt' with 122 words (out/word_counts_r14.txt: 122); B has five sections (659 words, not 661: SC1-d-r14-exemplarB-wordcount); both use seed-0 Lab 3 numbers (checked).")
p("SC1-d-r12-interpretation-claim-lab3-grid-direction", "Lab 3 interpretation (line 430) and exemplar A Discretization annotation: the one-step tail-minus-estimate 0.026948 estimates bias 0.043248 with error -0.016300; 256-step gap 0.004361 larger in absolute value than 64-step -0.001799; direction claims accurate (out/recompute_r14.txt). The 'different paths' wording is SC1-d-r14-separate-paths.")
p("SC1-d-ag-docstring", "test_project.py docstring lines 1-21 read this round: the 'level exactly on a path's maximum' sentence now names one discrete, one nested and one just-above test, matching the code (test_path_whose_maximum_equals_the_level..., test_nested_counts_include..., test_path_just_below...).")
p("SC1-d-r10-docstring", "test_project.py module docstring read in full (lines 1-21): each claim matches a test (checked against the test names).")
p("SC1-d-r13-docstring-level-on-max", "test_project.py:14-16 now reads 'Two tests put the level exactly on a path's maximum, one for the discrete estimate and one for the nested counts, and one puts it just above a path's maximum': matches test_path_whose_maximum_equals_the_level_counts_as_reaching_it (discrete), test_nested_counts_include_a_path_whose_maximum_equals_the_level (nested) and test_path_just_below_the_level_is_not_counted (just above). Fixed.")
f("SC1-d-r13-comment-both-zero", "test_project.py:470-472 now says: 'At the instance's own level the tail can be so small that no path reaches it (seed 32 at grids 16, 32 and 64), and then the estimates are 0 and cannot differ.' Checked (out/comment_claim_seed32_r14.txt): seed 32 at its own level has estimate 0.0 on grids 16, 32 and 64, but the other seed 32+7919 at the same level gives 0.607, 0.691, 0.684, so the two estimates DO differ; the clause 'cannot differ' is false for the pair the test compares. Only seed 32 is zero among seeds 0-49.", "Replace the last clause: 'At the instance's own level the tail can be so small that no path reaches a grid's level (seed 32, grids 16, 32 and 64, estimate 0.0), so the test uses a level near zero.'")
p("SC1-d-ag-draws-depend-overconstraint", "test_project.py:470-478: a level of 1e-9 and a second seed; the five alternatives pass it (50/50 each).")
p("SC1-d-ag-band-overconstraint", "test_project.py:121-124 simulation_band uses the target's standard error; all five new alternatives and the prior correct set pass the band tests.")
p("SC1-d-ag-walk-listing-stall", "test_project.py:315-336 (n = 41 budget): the binomial alternative and the DP alternative (alt_r14_1, alt_r14_3) pass on seeds 0-49.")
p("SC1-d-ag-print-coverage", "test_project.py:584-614 no-print test read: calls every public function on boundary inputs; passes on the reference and all alternatives.")
p("SC1-d-r10-explicit-tests", "test_project.py:624-665 (explicit path regeneration) read: the paths follow the page's draw order; two alternatives with different internal code pass.")
f("SC1-d-r10-mutant-folder-hygiene", "ledgers/SC1/mutants/ holds 4 slice-a lab mutants (SC1a-r13-lab-m1-L01-cov-max.py, SC1a-r13-lab-m2-L02-hat-peak-half.py, SC1a-r13-lab-m3-L03-var-divisor-n.py, SC1a-r13-lab-m4-L03-closed-form-H3.py; their docstrings name 'SC1 lab L01..L03'). They were added in 8e5751c (git log). The mutate gate counts them as grader mutants (80 files, 80 killed), and they are killed by grader tests only because they are not grader solutions. The folder is for grader mutants.", "Move the four SC1a-r13-lab-m*.py files to ledgers/SC1/lab-mutants/ (lab mutants belong there; lab-mutants already holds the SC1a-lab and SC1a-r6 ones).")
p("SC1-d-r10-mutant-seed-coverage", "mutate_graders.py --unit SC1 --seeds 0-9: every grader mutant KILLED (out/mutate_graders_unit_r14.txt).")
p("SC1-d-r12-mutants-all-existing", "all 73 grader mutants from earlier rounds are KILLED on seeds 0-9 (out/mutate_graders_unit_r14.txt).")
p("SC1-d-r12-mutants-new-r12-01-04", "r12_01..r12_04 KILLED (out/mutate_graders_unit_r14.txt).")
p("SC1-d-r12-mutant-tiny-level", "r12_05_tiny_level_guard_returns_one.py KILLED (out/mutate_graders_unit_r14.txt); the closed-form tests at test_project.py:251-259 kill it.")
p("SC1-d-r12-mutant-tiny-time", "r12_06_tiny_time_guard_returns_zero.py KILLED (out/mutate_graders_unit_r14.txt); test_project.py:262-269 kill it.")
p("SC1-d-r7-alt4-ruling10", "FINAL-ARCHITECT-RULINGS.md item 10 (a float-based alternative wrong on a stated exact rule is a mutant): plan 5.7(4) draw-order variant is r12_01_step_major_draw_order.py, KILLED (out/mutate_graders_unit_r14.txt).")
p("SC1-d-r13-mutants-new", "r13_01..r13_05 KILLED on seeds 0-9 (out/mutate_graders_unit_r14.txt).")
p("SC1-d-r13-tests-added", "test_project.py:251-269 (the two closed-form tests) read; they kill r12_05 and r12_06.")
p("SC1-d-r7-page-vs-twin", "scripts/check_labs_r14.py: Lab 1 and 3 page code == twin; expected == twin stdout (out/check_labs_r14.txt).")
p("SC1-d-r7-registry-live", "verify_refs.py --unit SC1 live: 0 problems (out/verify_refs_unit_sc1.txt).")
p("SC1-d-r8-proofs-trace", "project.html P1-P3 statements and exemplar B proof traced line by line (see SC1-d-exemplarB-proof).")
p("SC1-d-delta-r5-read", "process: this round read the whole slice (project.html 1-667, grader/*.py, tests/labs/SC1 twins, mutants, alternatives) and the delta e919577..8e5751c for every slice file.")
p("SC1-d-delta-r6-read", "process: the delta e919577..8e5751c for slice d read in full: project.html hunks at 450-550 and test_project.py hunks at 16 and 472; L01, L02, L05, L06, index.html hunks read as text diffs; mutant and alternative additions listed.")
c("SC1-d-r10-alternatives", "ledgers/SC1/scripts/SC1-d-r10/alternatives/ (byte-identical folder)", "alt_r10_a, b, c, e pass seeds 0-49 on the round-13 suite; alt_r10_d is the draw-order mutant (fails 2 tests this round, out/step_major_check_r14.txt): it is in the alternatives folder, see SC1-d-r14-alt-folder-hygiene.")
c("SC1-d-r10-prior-alternatives", "ledgers/SC1/scripts/SC1-d-r10/ (byte-identical folder)", "the round-10 correct alternatives are unchanged and passed on the round-13 suite; the suite's code is unchanged since then.")
f("SC1-d-r8-alternatives", "alt_r8_a and alt_r8_d pass 50/50 (carried, byte-identical). alt_r8_b and alt_r8_c FAILED in round 13 (absolute reference path) and now pass 50/50 (out/prior_changed_alternatives_r14.txt). alt_r8_e_step_major.py is a draw-order mutant (fails 2 tests on seed 0: out/step_major_check_r14.txt) kept in the alternatives folder.", "Move alt_r8_e_step_major.py out of ledgers/SC1/scripts/SC1-d-r8/alternatives/ (Ruling 10: it is a mutant; r12_01_step_major_draw_order.py already covers it).")
p("SC1-d-r8-alternatives-b-c-repath", "the repathed copies in SC1-d-r9/alternatives_r8_repathed/ (alt_r8_b, alt_r8_c) now load nothing external and pass 50/50 (out/prior_changed_alternatives_r14.txt). The round-13 failure is gone.")

p("SC1-d-rubric-exclusive", "project.html rubric (lines 449-459 as revised, read cell by cell). Under the scoring rule at line 445 (level 1 = the absence its cell names; level 2 = any attempt that misses a level-3 element or makes a named error; each level contains the one below), the cells are exclusive and exhaustive: C1 level 1 'No numbered assumptions for any result' is an absence, and 'assumptions stated after the proof' is now an attempt (level 2); C3 level 1 'No numbers are quoted' is an absence, and quoting a number that run_report does not print is level 2; C4 level 1 has no claim beyond the sample and no caveat (an absence), and an overclaim is level 2. Round-13 overlaps are removed. The separate-paths element of C5 level 3 is a different defect (SC1-d-r14-separate-paths).")
# ---- new rows for round 14 ----
D["SC1-d-r14-separate-paths"] = ("FAIL", "The page says the grids are drawn on 'separate' or 'different' paths (project.html:306 Lab 3 hypothesis 'Each grid is drawn on its own paths'; :430 'The rows are drawn on different paths'; :457 rubric C5 level 3 'drawn on separate paths'; :559 exemplar B 'These rows use separate paths'; the C5 level 3 annotation). Measured this round (scripts/shared_stream_r14.py, out/shared_stream_r14.txt): every grid is built from the same seeded stream random.Random(seed), so normal number m is one-step path m (scaled by sqrt(H)) and four-step increment m (scaled by sqrt(H/4)); the one-step draw equals 2 x the four-step increment for all m < N, exactly (max difference 0.0). The grids therefore share normal draws and their estimates are correlated, not independent samples. grader/reference.py _grid_paths restarts random.Random(seed) for each n_steps, which is the cause.", "Replace 'separate', 'different' and 'its own' paths with: each grid is generated from the same seeded stream, so the grids share their normal draws and their estimates are correlated. Change rubric C5 level 3 (line 457), the Lab 3 hypothesis (306) and interpretation (430), exemplar B (559) and its C5 level 3 annotation to match. Rubric exclusivity is unaffected.")
D["SC1-d-r14-exemplarB-wordcount"] = ("FAIL", "project.html:463 says exemplar B's five sections 'run to 661 words without headings'. Counted this round by the brief's rule (a word is a run of characters between spaces; out/word_counts_r14.txt and an independent raw-HTML count): 80 + 140 + 153 + 140 + 146 = 659 words.", "Change '661' to '659' at project.html:463.")
D["SC1-d-r14-rung4-stretch"] = ("FAIL", "project.html stretch section lists a second level and 'A continuity correction' (propose a level shift for the grid maximum; 'This section cites no source'). plans/SC1-build-plan.md §5.1 item 4 says the stretch is the second level and a Brownian-bridge continuity correction only after its registry record is admitted, and 'Without the record, the stretch is limited to a finer grid and an additional nested-grid table'. §12 item 14 says 'No continuity correction is graded'. The page offers the uncited continuity correction without the record.", "Remove the continuity-correction item (and the second-level item, unless the architect reads §5.1(4) as allowing it), keeping the finer nested table; or admit the continuity-correction record first and cite it.")
D["SC1-d-r14-alt-folder-hygiene"] = ("FAIL", "Ruling 10 (plans/FINAL-ARCHITECT-RULINGS.md item 10): a float-based alternative wrong on a stated exact rule is a mutant, not an alternative. Two draw-order mutants sit in alternatives folders: ledgers/SC1/scripts/SC1-d-r8/alternatives/alt_r8_e_step_major.py and ledgers/SC1/scripts/SC1-d-r10/alternatives/alt_r10_d_step_major_order.py. Each fails 2 tests on seed 0 (checked this round). The same error is already r12_01_step_major_draw_order.py in mutants.", "Move both files out of the alternatives folders (into ledgers/SC1/mutants/ with a first docstring line naming the error, or delete as duplicates of r12_01).")
D["SC1-d-r14-new-mutants"] = ("PASS", FRESH + "three new student-error mutants written as single-change copies of reference.py (scripts/make_mutants_r14.py): r14_01_path_seeded_by_path_index.py (KILLED by test_one_step_draws_are_the_seeded_gaussians), r14_02_nested_fine_drops_the_horizon_point.py (KILLED by test_coarse_count_never_exceeds_the_fine_count[8-8]), r14_03_terminal_count_compares_the_up_count.py (KILLED by test_srw_counts_match_enumeration_for_n_up_to_12[11]). Output in out/mutate_graders_unit_r14.txt.", "")
D["SC1-d-r14-new-alternatives"] = ("PASS", FRESH + "five new correct alternatives (scripts/alternatives/alt_r14_1..5) pass seeds 0-49, 50/50 each (out/alternatives_r14.txt).", "")
D["SC1-d-r14-mutant-killed-by-label"] = ("PASS", FRESH + "mutant r8_01_leftover_print_on_boundary_walk.py is KILLED, but mutate_graders.py labels the kill 'collection/import error'. Run directly (scratch), its failures are the autouse no-output fixture in every test (ERROR at teardown: 'no function may print'). The kill is genuine; the tool label is wrong (the regex matches FAILED lines only). Recorded in the mutants list as killed by test_no_function_prints_or_warns (autouse _no_stray_output).", "")
D["SC1-d-r14-hours-estimate"] = ("PASS", FRESH + "own estimate of the deliverables about 31 h against the declared 28 h (within 30 percent: 28 x 1.3 = 36.4). Components as in SC1-d-hours.", "")
D["SC1-d-r14-collect-136"] = ("PASS", FRESH + "collect-only on reference in scratch: 136 tests (out/collect_count_r14.txt); pages say 136.", "")
D["SC1-d-r14-starter-fails"] = ("PASS", FRESH + "suite on starter.py: 132 failed, 4 passed (instance-only tests) (out/starter_fails_r14.txt).", "")
D["SC1-d-r14-sample-instances"] = ("PASS", FRESH + "19 seeds valid and distinct in level, tail and one-step estimate (out/sample_instances_r14.txt).", "")

# ---- assemble ----
def _full(text):
    text = re.sub(r"(?<![\w/.-])scripts/", "ledgers/SC1/scripts/SC1-d-r14/", text)
    text = re.sub(r"(?<![\w/.-])out/", "ledgers/SC1/scripts/SC1-d-r14/out/", text)
    return text
for _k, _v in list(D.items()):
    D[_k] = (_v[0], _full(_v[1]), _full(_v[2]))
rows = []
for rid in ids13:
    if rid not in D:
        raise SystemExit(f"no round-14 decision for {rid}")
    status, ev, fix = D[rid]
    base = r13_by_id[rid]
    row = {"id": rid, "check": base["check"], "location": base["location"], "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)
LOC = {
    "SC1-d-r14-separate-paths": "course/modules/SC/SC1/project.html:306 (Lab 3 hypothesis), :430 (Lab 3 interpretation), :457 (rubric C5 level 3), :559 (exemplar B Discretization), and the exemplar B C5 level 3 annotation",
    "SC1-d-r14-exemplarB-wordcount": "course/modules/SC/SC1/project.html:463 (Two exemplars paragraph)",
    "SC1-d-r14-rung4-stretch": "course/modules/SC/SC1/project.html:609-615 (section#stretch; the continuity-correction item at line 614)",
    "SC1-d-r14-alt-folder-hygiene": "ledgers/SC1/scripts/SC1-d-r8/alternatives/alt_r8_e_step_major.py; ledgers/SC1/scripts/SC1-d-r10/alternatives/alt_r10_d_step_major_order.py",
}
extra = [k for k in D if k not in ids13]
for rid in extra:
    status, ev, fix = D[rid]
    row = {"id": rid, "check": "2.6/2.9/2.2 round-14 check", "location": LOC.get(rid, "see evidence"), "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

# mutants from the gate output
mut = []
for line in open(f"{O}/mutate_graders_unit_r14.txt", encoding="utf-8"):
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line.strip())
    if not m:
        continue
    status, name, desc, killer = m.groups()
    killer = re.sub(r" \(seed \d+\)$", "", killer)
    if name == "r8_01_leftover_print_on_boundary_walk.py":
        killer = "test_no_function_prints_or_warns (autouse _no_stray_output teardown; tool label 'collection/import error' is wrong)"
    mut.append({"id": name, "description": desc, "killed_by": killer if status == "KILLED" else None})

fails = [r for r in rows if r["status"] != "PASS"]
passes = [r for r in rows if r["status"] == "PASS"]
frag = {
    "unit": "SC1",
    "slice": "d",
    "round": 14,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 14 (did not build SC1-d; read the whole project page, the grader, the twins, the round-13 fragment and the delta e919577..8e5751c)",
    "pin": "8e5751c9",
    "base": "e919577b (round-13 pin)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE14-SC1-d",
    "scratch": "/tmp/sc1d-r14/ (ws: reference suite; alt: new alternatives; prior: changed repathed alternatives; starter; r8_01; step_*; blind text ledgers/SC1/scripts/SC1-d-r14/out/blind_exemplars_r14.txt)",
    "scripts_dir": "ledgers/SC1/scripts/SC1-d-r14/",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if not fails else "FAIL",
    "rows": rows,
    "mutants": mut,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Round 14 on 8e5751c. Whole project.html read (1-667), grader/*.py read in full, lab twins and page code compared, every gate re-run in this checkout (out/*.txt). Calibration: blind scoring of both exemplars before the annotated passages were read: A 1,2,2,2,1 and B 4,4,4,3,4, both equal to the official scores. Rubric exclusivity: the scoring rule (project.html line 445) makes level 1 an absence and level 2 an attempt, so every criterion's cells are exclusive and exhaustive under it; PASS. Round-13 FAILs closed: rubric overlaps, exemplar B 794 count, calib-B, docstring on level-max, alternatives alt_r8_b/c (now run), mutate gate. Still FAIL: the 'separate paths' claim (shared normal stream, measured), the C5 annotation that repeats it, the brief item 1 gap for P3, the comment that says 'cannot differ' (false for seed 32), the 661 word count, the mutant folder holding slice-a lab mutants, two draw-order mutants in alternatives folders, the rung 4 continuity correction against plan 5.1(4), and three unrecorded plan deviations (1e-10 vs 1e-12; exemplar data-level swap and excerpt). Mutants: 80 files in ledgers/SC1/mutants, all KILLED on seeds 0-9; 3 new round-14 mutants (r14_01..03) and 5 new alternatives (alt_r14_1..5, 50/50 seeds 0-49). Could not check: (1) the in-browser self-assessment form (JavaScript UI not clicked; page_smoke runs only the grader panel); (2) the full-registry verify_refs run (only SC1 live; CI runs the full registry); (3) the 500-seed reference sweep (0-199 run, 200/200); (4) the 50-seed sweep of all 80 mutants (gate is seeds 0-9, as the plan says); (5) the hub's placement quiz items beyond the rung-2 wording (other slices); (6) the self-assessment's stored-state behaviour in a browser; (7) timing of n = 41 under Pyodide (the budget test runs in CPython only, 0.3 s).",
    "summary": f"SC1 slice d round 14 on 8e5751c: verdict {'PASS' if not fails else 'FAIL'}. Rows {len(rows)}: PASS {len(passes)}, FAIL {len(fails)}, UNVERIFIABLE 0. Mutants {len(mut)}/{len(mut)} killed on seeds 0-9 (3 new). Alternatives: 5 new correct alternatives 50/50; 6 previously failing repathed alternatives now 50/50.",
}
out = f"{root}/ledgers/SC1/SC1-d.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out, "rows", len(rows), "pass", len(passes), "fail", len(fails), "mutants", len(mut))
