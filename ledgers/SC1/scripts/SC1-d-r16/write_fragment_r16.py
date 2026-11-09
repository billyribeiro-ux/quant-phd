"""Build ledgers/SC1/SC1-d.json (round 16) from the round-15 fragment and the round-16 evidence.
Every round-15 row id is kept. A row is carried only when its cited files or lines are byte-identical since the
previous pin (d1e65a02); a row whose subject changed or that is a gate, numeric, or proof check is re-verified and
carries round-16 evidence. Usage: write_fragment_r16.py <checkout root> <previous fragment json>."""
import datetime
import json
import re
import sys

root, prev_path = sys.argv[1], sys.argv[2]
prev = json.load(open(prev_path, encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
OUT = "ledgers/SC1/scripts/SC1-d-r16/out"
PIN_PREV = "d1e65a02"
CF = "Carried from round 15 ({files} byte-identical since the previous pin {pin}): "
CL = ("Carried from round 15 (project.html lines {lines} byte-identical since the previous pin {pin}; the round-15 "
      "hunks touched only lines 162, 436 and 593): ")
GRADER = "course/modules/SC/SC1/grader/"
MUT = "ledgers/SC1/mutants/"

R16 = {}  # id -> (status, evidence) fresh round-16 verification
CARRY = {}  # id -> prefix string (carry original evidence)

def fresh(i, text, status="PASS", fix=""):
    R16[i] = (status, text, fix)

def carry_files(i, files):
    CARRY[i] = CF.format(files=files, pin=PIN_PREV)

def carry_lines(i, lines):
    CARRY[i] = CL.format(lines=lines, pin=PIN_PREV)

GATE = ("Round 16 gate run (ledgers/SC1/scripts/SC1-d-r16/gates_r16.sh, outputs in " + OUT + "/): ")
fresh("SC1-d-r10-gates", GATE + "check_pages SC1 PASS; check_dag SC1 PASS; check_projects SC1 PASS; run_labs SC1 PASS (11/11); "
      "run_graders SC1 PASS (50/50 and 200/200); mutate_graders SC1 PASS (86/86); page_smoke project PASS; mypy "
      "--no-incremental PASS (385 files); ruff check . PASS; ruff format --check . PASS (553 files); verify_refs --offline "
      "PASS (560 entries, 0 problems). Live verify_refs and the full pytest suite were not run.")
fresh("SC1-d-r10-page-smoke", "tools/page_smoke.py --unit SC1 --pages project: 'page_smoke SC1: PASS'; in-browser grader "
      "'All 136 tests pass on seed 571142431' (out/page_smoke_project_r16.txt).")
fresh("SC1-d-r10-lab-twins", "run_labs --unit SC1 --page project: 3/3 PASS (out/run_labs_project_r16.txt). Twins run with "
      "python -I -W error, exit 0, no stderr. Page code equals the twin for Labs 1 and 3; Lab 2 differs only at the two "
      "intended ___ blanks; each expected block equals the twin output (out/twin_vs_page_r16.txt, twin_vs_page_r16.py).")
fresh("SC1-d-r10-registry-live", "verify_refs.py --offline: 560 entries, 0 problems (out/verify_refs_offline_r16.txt). "
      "references.json record shreve2004stochastic read: type book, year 2004, Shreve, 'Stochastic Calculus for Finance II', "
      "status verified; the reading-list line matches. The live (network) run was not repeated this round.")
fresh("SC1-d-tools-gates", "ruff check and ruff format --check on course/modules/SC/SC1/grader and tests/labs/SC1: PASS "
      "(out/ruff_check_grader_labs_r16.txt, out/ruff_format_grader_labs_r16.txt); mypy --no-incremental PASS; pytest "
      "tests/test_labs.py tests/test_page_smoke.py: PASS (out/pytest_labs_page_r16.txt). tests/labs holds no pytest files "
      "(out/pytest_labs_r16.txt exit 5).")
fresh("SC1-d-r11-run-graders", "run_graders --unit SC1 --seeds 0-49: PASS 50/50 (out/run_graders_0_49_r16.txt); --seeds 0-199: "
      "PASS 200/200 (out/run_graders_0_199_r16.txt).")
fresh("SC1-d-r11-mutate-gate", "mutate_graders --unit SC1 --seeds 0-9: 86/86 KILLED, PASS (out/mutate_graders_unit_r16.txt). "
      "ledgers/SC1/mutants/ holds 86 top-level .py files and no subdirectories (find -mindepth 1 -type d: empty).")
carry_lines("SC1-d-ladder", "40-49")
carry_lines("SC1-d-grading-mode", "225-226")
fresh("SC1-d-spec-signatures", "project.html:222 signatures compared with grader/starter.py:16,21,26,31,36 and with "
      "reference.py: all five function names, parameters and return annotations match.")
carry_lines("SC1-d-spec-rounding-statement", "223; Labs 1 and 3 expected blocks unchanged")
fresh("SC1-d-hours", "table#hours (project.html 275-281): 2 + 3 + 10 + 8 + 3 + 2 = 28, equal to data-hours-project=28 (line 33) "
      "and the module's 28 of 100 hours. Round-16 estimate of the components: 1.5 + 1 + 8 to 12 + 5 to 8 + 3 + 1.5 to 2, "
      "about 20 to 28 hours, within 30 percent of 28 (ruling: hours are design targets).")
carry_lines("SC1-d-spec-grid-table", "232-234")
carry_lines("SC1-d-spec-tolerance-statement", "235")
carry_files("SC1-d-spec-n41-method", "course/modules/SC/SC1/grader/test_project.py; project.html 224")
carry_files("SC1-d-spec-constraints-raise", "course/modules/SC/SC1/grader/reference.py; project.html 238")
carry_files("SC1-d-ag-reference", GRADER + "reference.py")
carry_files("SC1-d-ag-starter", GRADER + "starter.py")
carry_files("SC1-d-ag-instances", GRADER + "instance.py")
fresh("SC1-d-ag-count", "collect-only in a scratch copy with reference.py as bm_checks.py: '136 tests collected' "
      "(out/collect_count_r16_scratch.txt). project.html lines 7, 226 and 297 each state 136.")
carry_files("SC1-d-ag-messages", GRADER + "test_project.py")
carry_files("SC1-d-ag-overconstraint", GRADER + "test_project.py; the round-16 alternatives run (out/alternatives_current_unique_r16.txt)")
fresh("SC1-d-ag-alternatives-ok", "ledgers/SC1/scripts/SC1-d-r16/run_one_r16.py on all 47 alternatives in the verified "
      "folders (r8-r16 'alternatives' directories) over seeds 0-49: every candidate 50/50 (out/alternatives_current_unique_r16.txt).")
fresh("SC1-d-r13-prior-alternatives", "round-16 run of ledgers/SC1/scripts/SC1-d-r13/alternatives/ (5) and "
      "SC1-d-r14/alternatives/ (5): all 50/50 (out/alternatives_current_unique_r16.txt).")
MUT_ROWS = {
    "SC1-d-ag-mutants-plan": "ledgers/SC1/mutants/m01..m10",
    "SC1-d-ag-mutants-own": "ledgers/SC1/mutants/m11-m15, m18, m19, m21",
    "SC1-d-ag-mutants-survivors": "ledgers/SC1/mutants/m16, m17",
    "SC1-d-ag-mutants-seed": "ledgers/SC1/mutants/m20",
    "SC1-d-ag-mutants-seed-offset": "ledgers/SC1/mutants/m22",
    "SC1-d-ag-mutants-r3": "ledgers/SC1/mutants/m23-m26",
    "SC1-d-ag-mutants-r4-new": "ledgers/SC1/mutants/m27-m31",
    "SC1-d-ag-mutants-r5-new": "ledgers/SC1/mutants/m32-m34",
    "SC1-d-ag-mutants-r6-new": "ledgers/SC1/mutants/m37",
    "SC1-d-ag-level-equality-survivors": "ledgers/SC1/mutants/m35, m36",
    "SC1-d-ag-mutants-r7-new": "ledgers/SC1/mutants/m38-m41",
    "SC1-d-r7-mutants-new": "ledgers/SC1/mutants/m38-m41",
    "SC1-d-r8-mutants-new": "ledgers/SC1/mutants/r8_01..r8_07, r8_e",
    "SC1-d-r9-mutants-new": "ledgers/SC1/mutants/r9_01..r9_04",
    "SC1-d-r10-new-mutants": "ledgers/SC1/mutants/r10_01..r10_06, r10_d",
    "SC1-d-r11-new-mutants": "ledgers/SC1/mutants/r11_01..r11_04",
    "SC1-d-r11-m09": "ledgers/SC1/mutants/m09_seed_zero_hard_coded.py",
    "SC1-d-r11-m09-coverage-note": "ledgers/SC1/mutants/m09_seed_zero_hard_coded.py",
    "SC1-d-r12-mutants-new-r12-01-04": "ledgers/SC1/mutants/r12_01..r12_04",
    "SC1-d-r12-mutant-tiny-level": "ledgers/SC1/mutants/r12_05",
    "SC1-d-r12-mutant-tiny-time": "ledgers/SC1/mutants/r12_06",
    "SC1-d-r13-mutants-new": "ledgers/SC1/mutants/r13_01..r13_05",
    "SC1-d-r14-new-mutants": "ledgers/SC1/mutants/r14_01..r14_03",
}
for i, files in MUT_ROWS.items():
    if i in CARRY:
        continue
    CARRY[i] = CF.format(files=files, pin=PIN_PREV) + "(each file killed again in the round-16 run, out/mutate_graders_unit_r16.txt) "
fresh("SC1-d-r7-mutants-all", "round-16 mutate_graders --unit SC1 --seeds 0-9: 86/86 KILLED (out/mutate_graders_unit_r16.txt); "
      "every top-level grader mutant named in this row is among the 86.")
fresh("SC1-d-r10-mutant-seed-coverage", "mutate_graders --unit SC1 --seeds 0-9: 86/86 killed (out/mutate_graders_unit_r16.txt).")
fresh("SC1-d-r12-mutants-all-existing", "ledgers/SC1/mutants/*.py: 86 files (82 earlier plus r16_01..r16_04), all KILLED on "
      "seeds 0-9 (out/mutate_graders_unit_r16.txt).")
fresh("SC1-d-r14-mutant-killed-by-label", "out/mutate_graders_unit_r16.txt: every line names a killing test and seed "
      "(86 KILLED lines, none SURVIVED).")
fresh("SC1-d-r15-mutants-new", "round-16 kill of r15_01..r15_04 by mutate_graders (out/mutate_graders_unit_r16.txt): all KILLED.")
fresh("SC1-d-r11-recompute", "Recomputed the seed-0 numbers from the reference (scripts: twin_vs_page_r16.py, instances_r16.py, "
      "word_counts_r16.py). Lab 1 and Lab 3 twin output equals the printed blocks (out/twin_vs_page_r16.txt). Derived values in "
      "prose: 0.016300 / 0.010735 = 1.52; 0.016300 / 0.009218 = 1.77; 0.001799 / 0.012870 = 0.14; 1588 = 2 x 794; 9.13e-15 "
      "printed. All agree with the page.")
fresh("SC1-d-r11-collect", "collect-only 136 (out/collect_count_r16_scratch.txt).")
fresh("SC1-d-r11-mypy-ruff", "mypy --no-incremental PASS (out/mypy_r16.txt); ruff check and format PASS on the grader and labs (out/ruff_*_grader_labs_r16.txt).")
fresh("SC1-d-r11-alternatives", "round-16 run of ledgers/SC1/scripts/SC1-d-r11/alternatives/ (alt_r8_b, alt_r8_c): both 50/50 (out/alternatives_current_unique_r16.txt).")
for i in ["SC1-d-r7-page-smoke", "SC1-d-r10-page-smoke-project", "SC1-d-r8-page-smoke", "SC1-d-ag-page-smoke",
          "SC1-d-r12-gate-page-smoke"]:
    fresh(i, "page_smoke --unit SC1 --pages project (round 16): PASS; in-browser grader 'All 136 tests pass' (out/page_smoke_project_r16.txt). The project page changed since the previous pin (lines 162, 436, 593), so the check was re-run.")
fresh("SC1-d-r12-gate-page-tools", "round 16: check_pages SC1 PASS, check_dag SC1 PASS, check_projects SC1 PASS (out/check_*_unit_r16.txt).")
fresh("SC1-d-r12-gate-run-labs", "round 16: run_labs SC1 PASS (11/11) and --page project PASS (3/3) (out/run_labs_*_r16.txt).")
fresh("SC1-d-r12-gate-run-graders", "round 16: run_graders SC1 PASS 50/50 and 200/200 (out/run_graders_0_*_r16.txt).")
fresh("SC1-d-r12-gate-mutate", "round 16: mutate_graders --unit SC1 --seeds 0-9 PASS (86/86) (out/mutate_graders_unit_r16.txt).")
fresh("SC1-d-r12-gate-ruff-mypy", "Round 16: ruff check . PASS ('All checks passed!') and ruff format --check . PASS (553 files) "
      "at 56cc575 (out/ruff_check_repo_r16.txt, out/ruff_format_repo_r16.txt); mypy --no-incremental PASS (out/mypy_r16.txt). "
      "The round-15 E501 at ledgers/SC1/lab-mutants is gone: commit aeb512b6 excludes ledgers/*/lab-mutants.")
fresh("SC1-d-r7-gates-full", "Round 16 full-gate run for SC1 at 56cc575: every SC1 gate PASS and the repository ruff check and "
      "format check PASS (see SC1-d-r10-gates). Repository-wide pytest was not run in full; the relevant files were.")
fresh("SC1-d-r12-gate-pytest", "round 16: pytest tests/test_labs.py tests/test_page_smoke.py PASS; pytest tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_run_labs.py PASS (out/pytest_relevant_r16.txt, out/pytest_labs_page_r16.txt).")
fresh("SC1-d-r12-gate-verify-refs", "verify_refs.py --offline: 560 entries, 0 problems (out/verify_refs_offline_r16.txt).")
fresh("SC1-d-r12-collect-count", "collect-only 136 in a scratch copy (out/collect_count_r16_scratch.txt).")
fresh("SC1-d-r12-sample-20-seeds", "instances_r16.py: all 50 seeds valid; the 20-seed sample (0,3,5,7,9,11,13,17,19,23,29,31,37,41,43,44,46,47,48,49) listed with H, a, grid, paths, one-step estimate and tail (out/instances_r16.txt).")
fresh("SC1-d-r7-instances-sample", "instances_r16.py (out/instances_r16.txt): 50 seeds valid, 49 distinct levels, 50 distinct horizons, 50 distinct one-step estimates.")
carry_files("SC1-d-r7-starter-fails", GRADER + "starter.py")
carry_files("SC1-d-r7-reference-sweep-500", GRADER + "reference.py; " + GRADER + "test_project.py (round 16 also ran seeds 0-199)")
carry_files("SC1-d-r8-reference-sweep", GRADER + "reference.py")
fresh("SC1-d-r7-alternatives-sweep", "round-16 run of ledgers/SC1/scripts/SC1-d-r13/alternatives/ (5): all 50/50 (out/alternatives_current_unique_r16.txt).")
fresh("SC1-d-r12-alternatives", "round-16 run of ledgers/SC1/scripts/SC1-d-r12/alternatives/ (5): all 50/50 (out/alternatives_current_unique_r16.txt).")
fresh("SC1-d-r7-numbers-recompute", "Recomputed in round 16 from the reference and the twins (out/twin_vs_page_r16.txt; out/instances_r16.txt): tail 0.086497; one-step 0.059548, se 0.010735; target 0.043248, target se 0.009218, band 0.048142; grid rows as printed; nested 35, 29, 27, 22 of 40; walk 1588 and 794 of 4096.")
fresh("SC1-d-numbers-prose", "Every number in project.html prose re-derived in round 16 against the twin output (out/twin_vs_page_r16.txt) and the arithmetic in the prose: lines 37, 53, 223-239, 430, 463-606. Exemplar word counts: out/word_counts_r16.txt (668 and 422 under the rendered-text convention). Line 593 changed; its numbers are unchanged.")
fresh("SC1-d-numbers-target-se", "Lab 1 prints target se 0.009218 and band 0.048142 (out/twin_vs_page_r16.txt); line 430 interpretation: 1.52 and 1.77 recomputed.")
fresh("SC1-d-r7-numbers-target-se", "Lab 1 prints target se 0.009218 and band 0.048142; line 430 recomputed (round 16).")
carry_lines("SC1-d-hunk-standard-error-sentence", "233 (the 0/1 identity sqrt(p(1-p)/(N-1)) rederived: sample sd / sqrt(N) = sqrt(p(1-p)/(N-1)))")
carry_lines("SC1-d-hunk-no-more-often", "218")
carry_lines("SC1-d-hunk-filtration", "231")
fresh("SC1-d-hunk-one-step-target-se", "project.html Lab 1 band and interpretation (lines 155-162) re-read after the round-15 hunk at line 162: band 5 target se + 1/N = 0.048142 recomputed from the twin (out/twin_vs_page_r16.txt); 'inside the band: True' printed; the interpretation's sentences on the band and the sample se are accurate.")
carry_lines("SC1-d-index-rung2-text", "45")
carry_lines("SC1-d-exemplar-a-scope", "463-465")
carry_lines("SC1-d-exemplarB-onestep-claim", "574-583")
carry_lines("SC1-d-exemplarB-proof", "609-627")
carry_lines("SC1-d-exemplarB-p1-assumptions", "611-612")
carry_lines("SC1-d-exemplarB-p1-freezing", "613")
carry_lines("SC1-d-exemplarB-proof-structure", "609-627")
fresh("SC1-d-exemplarB-numbers", "Exemplar B numbers re-checked against the twin output (out/twin_vs_page_r16.txt): tail 0.0865 and 0.0595, se 0.0107, 0.0163 above target, 1.52 se, 0.037215, 0.020788, 0.004361, 0.026948; all match the printed values after rounding.")
carry_lines("SC1-d-r12-P1-proof", "531")
carry_lines("SC1-d-r12-P2-P3-proofs", "535-537")
carry_lines("SC1-d-statements", "244-263")
carry_lines("SC1-d-statements-recheck-P2", "251-256")
carry_lines("SC1-d-A1-label", "56; Lab 1 output unchanged")
carry_files("SC1-d-A3-A4-usage", "project.html 243-249 (lines unchanged); course/modules/SC/SC1/L05.html")
fresh("SC1-d-L05-A4-i", "project.html has no citation of A4(i) (grep 'A4(i)' empty) and L05 defines A4(a)-(h) only (L05 Assumption A4 list read in round 16).")
fresh("SC1-d-lab1-run", "tests/labs/SC1/lab-SC1-project-1.py run with python -I -W error: exit 0, output equals the expected block (rounded to six places; Simpson difference 9.13e-15); run_labs --page project: PASS; page Lab 1 code equals the twin (out/twin_vs_page_r16.txt).")
fresh("SC1-d-lab2-run", "tests/labs/SC1/lab-SC1-project-2.py run with python -I -W error: exit 0; output 29, 22, 7, True equals the expected block; page code equals the twin except the two intended blanks; run_labs --page project: PASS (out/twin_vs_page_r16.txt).")
fresh("SC1-d-lab3-run", "tests/labs/SC1/lab-SC1-project-3.py run with python -I -W error: exit 0; output equals the expected block line for line (grid rows, nested counts, walk counts); page code equals the twin; run_labs --page project: PASS (out/twin_vs_page_r16.txt).")
fresh("SC1-d-lab3-onestep-interp", "Lab 3 interpretation (project.html:430) re-derived in round 16: standard errors 0.009819 to 0.012870; 0.001799 / 0.012870 = 0.14; 0.016300 / 0.010735 = 1.52 and 0.016300 / 0.009218 = 1.77; sign of the one-step sampling error (estimate minus target = +0.016300, printed bias estimate minus true bias = -0.016300); nested counts <= 40. All agree with the output.")
carry_files("SC1-d-lab1-docstring", "tests/labs/SC1/lab-SC1-project-1.py")
carry_lines("SC1-d-lab2-attribution", "210; L06 Corollary 1.4 and Proposition 1.3 read in round 16 (L06.html)")
carry_files("SC1-d-lab3-docstring", "tests/labs/SC1/lab-SC1-project-3.py")
fresh("SC1-d-labs-pytest", "tests/labs holds no pytest test functions (pytest exit 5, out/pytest_labs_r16.txt); the lab twins were run directly under python -I -W error (out/twin_vs_page_r16.txt) and by run_labs (11/11, 3/3).")
carry_lines("SC1-d-discretization-bias", "236")
fresh("SC1-d-monte-carlo-term", "grep -i 'monte carlo' over project.html (learner text): no match; the simulation is called 'seeded simulation' and 'Monte Carlo' is not used.")
fresh("SC1-d-scope-words", "Round 16 read every scope word in project.html (every, all, only, any, same, never, always, exactly, drives) with its context: each is backed by a computation, a pathwise inequality, a proof, or an explicit hypothesis. The round-15 overclaim at line 162 is fixed (see SC1-d-r15-lab1-interp-overclaim). Exemplar B's 'holds for every grid' (line 558, 601) is a deliberately wrong annotated example, not an assertion of the page.")
fresh("SC1-d-process-words", "Learner text scanned for process words (round, verifier, fixer, builder, batch, self-check, we, our, I): the only hits are the student voice of Exemplar A ('I do not order them by bias', line 505) and the proof's 'we get' (line 531), neither a process word.")
fresh("SC1-d-banned-structure", "Structure: ladder, rungs, spec, budget, grader, local, report/proofs, brief, rubric, exemplars, self-assessment, stretch, reading, references in order (check_projects SC1 PASS, out/check_projects_unit_r16.txt).")
fresh("SC1-d-banned-and-process-words", "BUILDER_RULES 1.3-1.4 banned strings (TODO, TBD, lorem, ellipsis, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'well known', 'obviously', 'clearly', 'it can be shown') searched in the learner text: none. Only code's tuple[int, ...] matches the ellipsis pattern.")
fresh("SC1-d-r12-banned-and-process-words", "Round-16 scan repeated: no banned phrase and no process word in learner text (scan in this round's work log; same list as SC1-d-banned-and-process-words).")
fresh("SC1-d-dag", "check_dag --unit SC1 PASS (out/check_dag_unit_r16.txt); project.html has two concept links (stopping-time, normal-distribution), both to concepts.html anchors and inside the closure.")
fresh("SC1-d-notation", "notation/notation.json read: registered macros \\E, \\Prob, \\Normal, \\indic, \\R; Phi = standard normal CDF (M4 entry) used as such (project.html conventions line 231, 256, 534); T is not used as a symbol (line 231 says so); H, a, N, n, t, B, M, tau, rho, K, F have no conflicting registry entry.")
fresh("SC1-d-r12-notation", "Round 16 notation re-check: no collisions (see SC1-d-notation).")
fresh("SC1-d-define-before-use", "Round 16: running maximum and grid maximum defined in the lede (line 37); standard error defined at line 53; conventions (lines 229-240) define B, M, tau, Phi, erfc, grid, pathwise, discretization bias. Lab 1's hypothesis (line 57) links P2 to the statements section (#statements), and P1 is in the same section (line 244); the forward reference is linked at first use. PASS with this note.")
carry_lines("SC1-d-pathwise-define-before-use", "232")
carry_lines("SC1-d-r12-pathwise-only-l01", "231-232 (L01 changed only in its References paragraph, not the pathwise definition)")
carry_lines("SC1-d-rubric-observable", "449-459")
carry_lines("SC1-d-rubric-exclusive", "453-457")
carry_lines("SC1-d-rubric-levels-cumulative", "445")
fresh("SC1-d-calib-A", "Blind scoring (ruling 15), ledgers/SC1/scripts/SC1-d-r16/blind_extract_r16.py, out/blind_exemplars_r16.txt: scored Exemplar A memo prose with the rubric descriptors only: C1 4, C2 4, C3 4, C4 3, C5 4. Official 4,4,4,3,4: equal.")
fresh("SC1-d-calib-B", "Blind scoring (out/blind_exemplars_r16.txt): Exemplar B scored C1 2, C2 2, C3 2, C4 2, C5 2. Official 2,2,2,2,2: equal.")
fresh("SC1-d-r12-blind-exemplar-A", "Blind score of Exemplar A from its memo prose only: 4,4,4,3,4 (out/blind_exemplars_r16.txt); calibration within one level on every criterion.")
fresh("SC1-d-r12-blind-exemplar-B", "Blind score of Exemplar B from its memo prose only: 2,2,2,2,2 (out/blind_exemplars_r16.txt); within one level.")
fresh("SC1-d-exemplar-a-annotations", "Round 16, exemplar A annotations read against their passages (project.html 465-545). Line 497 (Meets C1 level 3 on the 'The checks' passage, lines 491-493) says the one-step target is tied to the reflection principle with the assumption that B_H is normal. The checks passage itself says the one-step row's maximum is B_H and its target is half the tail (0.043248); the tie is supplied by the report: the Summary cites P2 for the tail (line 471), and the Setup (line 482) states the increments are Normal(0, H/n), which for one step gives B_H ~ Normal(0, H) (P1 and P2 assumptions, lines 531 and 533). The claim is therefore supported at report level; the other annotations (475, 486, 498, 510, 521, 541-542) match their passages. Recommendation, not a failure: move the normality clause into the checks passage.")
fresh("SC1-d-exemplar-a-annotations-P1", "Round 16: the Appendix annotations (project.html 541-542) match the P1 text (A4(b), A4(c), A4(g), A4(h), A3, continuity) and the freezing step (lines 531).")
fresh("SC1-d-r12-exemplarA-annotation-C3", "Round 16: Summary annotation (475) and Setup annotation (486) match their passages: the Summary values are printed by Lab 1 or Lab 3 and the Setup states the rounding rule.")
carry_lines("SC1-d-exemplarA-claim", "467")
fresh("SC1-d-r12-exemplarB-numbers-values", "Exemplar B numbers re-checked against the twin output (see SC1-d-exemplarB-numbers).")
fresh("SC1-d-r12-annotations-B-accuracy", "Round 16: project.html:593 now reads 'Misses C5 level 3: omits the standard error at 1 step, the 64-step grid and the nested inequality on the same paths'. The passage (588) gives the 1-step gap 0.026948 without its standard error, has no 64-step grid, and no nested counts: the annotation is accurate.")
fresh("SC1-d-r12-exemplarB-brief", "Round 16: brief item 1 (project.html:436) now reads 'For this project, a result that no printed number checks is stated with its limit in place of a number. P3 is such a result...'. P3 has no printed number (Lab 3 simulates no first-passage time), so the amendment is accurate.")
fresh("SC1-d-r12-exemplarB-brief-length", "Round 16 word count, rendered-text convention (tags removed without inserting spaces; ledgers/SC1/scripts/SC1-d-r16/word_counts_r16.py): Exemplar A body 668 words, Exemplar B body 422 words, both within 400 to 900. The page's figures (668, 422) match this convention.")
fresh("SC1-d-r12-lab-numbers", "Lab 1, 2, 3 printed numbers equal the expected blocks and the twin output (out/twin_vs_page_r16.txt).")
fresh("SC1-d-r12-page-vs-twin", "Round 16: page code equals twin for Labs 1 and 3; Lab 2 differs only at its two blanks (out/twin_vs_page_r16.txt).")
fresh("SC1-d-r12-walk-identity", "Walk identity: enumeration gives 1588 walks with maximum >= 3 and 794 ending at >= 3 for n = 12 (lab output); 4096 = 2^12. Parity argument (even endpoint at n = 12) in Exemplar A holds.")
fresh("SC1-d-r12-hours", "table#hours: 28 hours, rationale per row present (round-16 estimate in SC1-d-hours).")
carry_lines("SC1-d-r12-spec-tolerance-and-errors", "235, 238")
carry_files("SC1-d-spec-tolerance-plan", "plans/SC1-build-plan.md section 5.5 ('to within 1e-12'); project.html 235")
carry_files("SC1-d-plan-tolerance", "plans/SC1-build-plan.md section 5.5; course/modules/SC/SC1/grader/test_project.py:188, 258")
fresh("SC1-d-r12-reading-and-registry", "Round 16: reading list shreve2004stochastic resolves to references.json (book, 2004, verified); the reading paragraph attributes no passage or theorem.")
fresh("SC1-d-registry", "references/references.json: shreve2004stochastic record read (book, Shreve, 2004, status verified, used_by SC1); byte-identical to the previous pin (git diff).")
carry_lines("SC1-d-reading-disclosure", "645-651")
fresh("SC1-d-privacy-claim", "project.html:289 ('Your code is saved in this browser shortly after you stop typing') and footer line 664 read; grader.js line 53 'derived from your workspace ID' confirms the seed text; store.js line 2 states that files are kept in IndexedDB in the learner's browser.")
carry_files("SC1-d-exemplar-naming", "plans/SC1-build-plan.md section 5.4; project.html data-level lines 465 and 547")
fresh("SC1-d-dfn-policy", "grep '<dfn' project.html: 0 matches (round 16). The project defines no term with dfn.")
fresh("SC1-d-exemplar-claims", "Exemplar verdicts and Summary read (project.html 467, 549, 471, 553): each verdict's claims match its passages and annotations; the line-497 annotation is supported at report level (see SC1-d-exemplar-a-annotations).")
fresh("SC1-d-r12-interpretation-claim-lab3-grid-direction", "Lab 3 interpretation (line 430) re-derived: estimate 64 steps above tail by 0.001799; sign of the one-step gap; the grid direction is not ordered from one seed (the text says so).")
carry_files("SC1-d-ag-docstring", GRADER + "test_project.py docstring lines 1-21")
carry_files("SC1-d-r10-docstring", GRADER + "test_project.py docstring")
carry_files("SC1-d-r13-docstring-level-on-max", GRADER + "test_project.py lines 14-17")
fresh("SC1-d-r13-comment-both-zero", "test_project.py:470-474 comment rechecked: the seed-32 claim (grids 16, 32, 64 estimate 0.0 at the instance's own level) reproduced by ledgers/SC1/scripts/SC1-d-r16/seed32_comment_r16.py (out/seed32_comment_r16.txt): grids 16, 32, 64, 128 all 0.0.")
carry_files("SC1-d-ag-draws-depend-overconstraint", GRADER + "test_project.py lines 470-478")
carry_files("SC1-d-ag-band-overconstraint", GRADER + "test_project.py lines 122-125 and uses")
carry_files("SC1-d-ag-walk-listing-stall", GRADER + "test_project.py lines 316-337")
carry_files("SC1-d-ag-print-coverage", GRADER + "test_project.py lines 586-616")
carry_files("SC1-d-r10-explicit-tests", GRADER + "test_project.py lines 626-667")
fresh("SC1-d-r10-mutant-folder-hygiene", "Round 16: the lab-twin folders SC1-a-r10, SC1-a-r11 and SC1-a-r12 (19 files) were moved from ledgers/SC1/mutants/ to ledgers/SC1/lab-mutants/ (git R100 renames, commit 56cc575a). ledgers/SC1/mutants/ has no subdirectories (find). PASS.")
carry_files("SC1-d-r12-mutants-new-r12-01-04", MUT + "r12_01..r12_04 (killed in round 16)")
carry_files("SC1-d-r12-mutant-tiny-level", GRADER + "test_project.py lines 230-259; " + MUT + "r12_05 (killed in round 16)")
carry_files("SC1-d-r12-mutant-tiny-time", GRADER + "test_project.py lines 243-270; " + MUT + "r12_06 (killed in round 16)")
carry_files("SC1-d-r7-alt4-ruling10", "plans/SC1-build-plan.md section 5.7(4) text; " + MUT + "r12_01; plans/FINAL-ARCHITECT-RULINGS.md ruling 10 (lines 21-22 byte-identical; ruling 17-18 added for E4 only)")
carry_files("SC1-d-r13-tests-added", GRADER + "test_project.py lines 251-270")
fresh("SC1-d-r7-page-vs-twin", "Round 16 twin comparison (out/twin_vs_page_r16.txt): page code equals twin (Labs 1 and 3), Lab 2 blanks only; expected blocks equal twin output.")
carry_files("SC1-d-r7-registry-live", "references/references.json (shreve2004stochastic; offline integrity only this round)")
fresh("SC1-d-r8-proofs-trace", "P1, P2 and P3 re-traced in round 16 (project.html 531-537 and exemplar B 613-616): each step's assumption exists in the lists (A0, A3, A4(b), A4(c), A4(g), A4(h) for P1); the freezing step, the stopping property, and the erfc substitution (w = z/sqrt 2) re-derived; no gap found beyond the one named in Exemplar B.")
fresh("SC1-d-delta-r5-read", "Round 16 delta read from d1e65a02 to 56cc575a for every SC1 slice file: project.html (hunks 162, 436, 593), L01.html and L03.html (not this slice), cards.json (not this slice), plans/FINAL-ARCHITECT-RULINGS.md (rulings 17-18 for E4), grader, labs and mutants (unchanged except moves and four new mutants in round 16).")
fresh("SC1-d-delta-r6-read", "Same delta read (see SC1-d-delta-r5-read): every hunk in the slice read.")
fresh("SC1-d-r10-alternatives", "Round 16: alt_r10_a, alt_r10_c, alt_r10_e pass 50/50 (out/alternatives_current_unique_r16.txt). alt_r10_b_quadrature_tail.py moved to ledgers/SC1/retired/SC1-d-r10/alternatives/ and no longer sits in the alternatives folder. PASS. Note (not a row failure): by ruling 10 its failure on the 1e-12 rule makes it a mutant; it is not recorded in ledgers/SC1/mutants/, and it is not a survivor.")
fresh("SC1-d-r10-prior-alternatives", "Round 16: alt_r8_a, alt_r8_b, alt_r8_c, alt_r8_d in ledgers/SC1/scripts/SC1-d-r10/alternatives_r8_repathed_r10/ all 50/50 (out/alternatives_current_unique_r16.txt; alt_r8_c rerun alone 50/50). alt_r8_e_step_major.py moved to ledgers/SC1/retired/SC1-d-r10/alternatives_r8_repathed_r10/. PASS.")
fresh("SC1-d-r8-alternatives", "Round 16: ledgers/SC1/scripts/SC1-d-r8/alternatives/ alt_r8_a, b, c, d: all 50/50 (out/alternatives_current_unique_r16.txt).")
fresh("SC1-d-r8-alternatives-b-c-repath", "Round 16: ledgers/SC1/scripts/SC1-d-r9/alternatives_r8_repathed/ alt_r8_b and alt_r8_c: 50/50 each (out/alternatives_current_unique_r16.txt).")
fresh("SC1-d-r14-separate-paths", "Round 16 re-read: Lab 3 hypothesis (line 306) and interpretation (line 430), rubric C5 (line 457), exemplar B C5 (line 593) use the same shared-draw wording; no 'separate paths' statement remains for grids that share draws.")
fresh("SC1-d-r14-exemplarB-wordcount", "Round 16 exemplar word counts: body A 668, body B 422 on the rendered-text convention (out/word_counts_r16.txt).")
carry_lines("SC1-d-r14-rung4-stretch", "637-640")
fresh("SC1-d-r14-alt-folder-hygiene", "Round 16: alt_r8_e_step_major.py (SC1-d-r9 and SC1-d-r10 repathed folders) and alt_r10_b_quadrature_tail.py moved to ledgers/SC1/retired/. Remaining alternatives folders hold only passing candidates (out/alternatives_current_unique_r16.txt). PASS.")
carry_files("SC1-d-r14-new-mutants", MUT + "r14_01..r14_03 (killed in round 16)")
fresh("SC1-d-r14-new-alternatives", "Round 16: ledgers/SC1/scripts/SC1-d-r14/alternatives/ alt_r14_1..5 all 50/50 (out/alternatives_current_unique_r16.txt).")
fresh("SC1-d-r14-hours-estimate", "Round-16 hours estimate in SC1-d-hours; the table's 28 is within 30 percent.")
fresh("SC1-d-r14-collect-136", "collect-only 136 (out/collect_count_r16_scratch.txt).")
carry_files("SC1-d-r14-starter-fails", GRADER + "starter.py (NotImplementedError in every function)")
fresh("SC1-d-r14-sample-instances", "instances_r16.py: 20-seed sample and all 50 seeds valid (out/instances_r16.txt).")
fresh("SC1-d-r15-lab1-interp-overclaim", "Round 16: project.html:162 now reads 'the engine's tests check that the estimates at 4 steps and at the instance's own grid size do not exceed the tail by more than the sampling band'. test_project.py:455-462 (test_grid_estimate_does_not_exceed_the_continuous_tail) checks exactly n_steps in (4, instance n_steps) on INST and INST2 against tail + simulation_band. Accurate.")
fresh("SC1-d-r15-plan-5-5-within-5se", "Round 16 re-run of ledgers/SC1/scripts/SC1-d-r15/plan_5_5_within_5se_check_r15.py (output reproduced): the literal plan statement 'the estimate lies within 5 se of reflection_tail(a, H)' fails the reference on 45 of 50 seeds (seed 1 grid 1: estimate 0.247407, tail 0.484528, se 0.016621). The grader tests the one-step estimate against tail/2 (test_project.py:401-416) and grids against tail plus band (455-462), which the reference passes. plans/SC1-open-items.md has no ruling for section 5.5 (only the L06 item). Section 5.7(2) (quadrature-only reflection_tail to 1e-8) contradicts section 5.5 and the page's 1e-12 rule (page line 235), and 5.7(4) (Box-Muller with a different draw order) contradicts the page's stated draw order (line 233). Ruling 10 classes both as mutants, but the plan text was not amended. Unrecorded deviation remains.", "FAIL",
      "Record an architect ruling in plans/SC1-open-items.md and amend plans/SC1-build-plan.md: section 5.5 to 'the one-step estimate lies within 5 se of reflection_tail(a, H)/2, and each grid estimate is at most the tail plus the band'; section 5.7(2) and (4) to the ruling-10 treatment (a float-based route that misses 1e-12 or the draw order is a mutant, not an alternative). Then re-run tools/check_projects.py --unit SC1.")
fresh("SC1-d-r15-mutants-new", "Round 16 kill of r15_01..r15_04 (out/mutate_graders_unit_r16.txt): all KILLED.")
fresh("SC1-d-r15-alternatives-new", "Round 16: ledgers/SC1/scripts/SC1-d-r15/alternatives/ alt_r15_1..5 all 50/50 (out/alternatives_current_unique_r16.txt).")
fresh("SC1-d-r15-carried-alternatives", "Round 16 re-run of every carried alternatives folder (r8 to r15 'alternatives' directories, 47 candidates) over seeds 0-49: all 50/50 (out/alternatives_current_unique_r16.txt). The r10 repathed alt_r8_c showed 49/50 once in a parallel run with colliding scratch names; rerun alone 50/50.")
fresh("SC1-d-r15-blind-scoring", "Round 16 blind scoring (ruling 15): A 4,4,4,3,4; B 2,2,2,2,2 (out/blind_exemplars_r16.txt).")
fresh("SC1-d-r15-reference-200-seeds", "run_graders --unit SC1 --seeds 0-199: PASS 200/200 (out/run_graders_0_199_r16.txt).")
fresh("SC1-d-r15-cross-references", "Round 16: L05 Assumption A3 (strong Markov, bounded stopping time), A4(b) freezing, A4(c) hitting time of a closed set, A4(g) joint measurability, A4(h) measurability at a stopping time: read in L05.html. L05 Sections 1 and 3 exist (stopping time in Section 3). L06 Proposition 1.3 (discrete reflection identity) and Corollary 1.4 (discrete tail identity) read in L06.html. L02 Theorem 2.5 and Remark 2.6 present. L01 Definition 1.1 present. L08 first-passage results present.")

# ---- new round-16 rows ----
NEW = [
    ("SC1-d-r16-alternatives-new", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r16/alternatives/ (5 files)", "PASS",
     "Five new correct alternatives of different styles: alt_r16_1 (NormalDist tail, DP walk counts over (position, running max), streaming maxima, algebraic se), alt_r16_2 (erfc tail, binomial sums, reflection identity, statistics.stdev), alt_r16_3 (erf-based cdf, enumeration to 12 steps and identity beyond, index subsampling, fsum), alt_r16_4 (NormalDist, DP for both counts, index subsampling, sum of squares), alt_r16_5 (erfc, two-pass fsum variance, two-pass nested, binomial counts). All 50/50 seeds (out/alternatives_current_unique_r16.txt). alt_r16_5 first failed 0/50 on a duplicate-stride bug in the verifier's own code (two nested tests); fixed and rerun 50/50."),
    ("SC1-d-r16-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r16_01..r16_04", "PASS",
     "Four new student-error mutants (single-change copies of reference.py): r16_01 srw_max_count adds the count at a - 1; r16_02 standard error is the sample sd without dividing by sqrt(N); r16_03 reflection_tail rounds the level to two places; r16_04 one path raises ZeroDivisionError instead of ValueError. Killed by test_srw_reflection_identity_holds_exactly[6], test_standard_error_uses_divisor_n_minus_one, test_reflection_tail_is_the_erfc_closed_form and test_one_path_raises_value_error (seed 0)."),
    ("SC1-d-r16-lab3-shared-draws-wording", "2.9-prose / 2.6-rubric", "project.html:306, 430, 505, 457 (C5)", "PASS",
     "The claim that the grids 'share draws' is read as: each grid consumes the same seeded stream of standard normals from random.Random(seed) in the same order (project.html 233, 430). Path-by-path the grids do not reuse the same numbers (a 1-step path uses one draw, a 4-step path four), so the correlation statement is a conservative reading. Recorded as a note, not a failure."),
    ("SC1-d-r16-instances-materiality", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py", "PASS",
     "All 50 seeds valid; 49 distinct levels, 50 distinct horizons, 47 grid sizes, 48 path counts; 50 distinct one-step estimates (out/instances_r16.txt)."),
    ("SC1-d-r16-retired-alternatives", "2.6-autograder", "ledgers/SC1/retired/", "PASS",
     "Retired files (alt_r10_b_quadrature_tail.py, alt_r10_d, alt_r8_e copies) are outside the verified folders and are not counted. Their failures are on stated rules (1e-12, draw order), so they are mutants by ruling 10. Recording them under ledgers/SC1/mutants/ would make the mutant count reflect them; noted, not a failure."),
]

def rebuild_status(i):
    prev = prev_rows[i]
    if i in R16:
        status, text, fix = R16[i]
        loc = {"SC1-d-exemplar-a-annotations": "course/modules/SC/SC1/project.html:497 (exemplar A, The checks passage, C1 annotation)"}.get(i, prev["location"])
        return {"id": i, "check": prev["check"], "location": loc, "status": status,
                "evidence": "Round 16 (verifier): " + text, **({"fix": fix} if status != "PASS" else {})}
    if i in CARRY:
        return {"id": i, "check": prev["check"], "location": prev["location"], "status": "PASS",
                "evidence": CARRY[i] + prev["evidence"]}
    raise SystemExit(f"row {i} has no round-16 decision")

NOTES = ("Round 16 on 56cc575 (pin d1e65a02 was round 15). Whole project.html read (1-666); grader/reference.py, starter.py, instance.py and test_project.py read in full; the three lab twins compared with the page; every gate re-run with output under ledgers/SC1/scripts/SC1-d-r16/out/. Blind exemplar scoring (ruling 15) from ledgers/SC1/scripts/SC1-d-r16/out/blind_exemplars_r16.txt: A 4,4,4,3,4 and B 2,2,2,2,2, equal to the official scores. Round-15 FAIL rows closed: repository ruff (aeb512b6 excludes lab-mutants), exemplar B line 593 annotation, Lab 1 line 162 sentence, lab-twin folders moved to lab-mutants, alternative-like folders moved to retired. Still FAIL: plan 5.5 within-5-se item and plan 5.7(2),(4) (no architect ruling recorded). Mutants: 86 files, all KILLED on seeds 0-9 (4 new: r16_01..04). Alternatives: 5 new (alt_r16_1..5) and all 47 alternatives in the verified folders run on seeds 0-49, all 50/50. Historical r1-r7 alternative folders were not re-run and are not counted (as in round 15). Not checked: the in-browser UI (self-assessment form, storage round trip, seed display) was not clicked; seeds 200-499 of the reference; the live verify_refs run; the full repository pytest suite; L01-L08 and index.html as pages (other slices; their cited labels and results only); cards.json (no cards in this slice); hours beyond an estimate (design targets).")
SUMMARY = ("SC1-d round 16 on 56cc575: verdict FAIL. One FAIL row: the plan 5.5 and 5.7 conformance (unrecorded deviations). Gates, labs, mutants (86/86) and the 47 verified alternatives pass; blind scores match the official scores within one level.")
rows = []
for r in prev["rows"]:
    rows.append(rebuild_status(r["id"]))
for (rid, check, loc, status, text) in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": text})
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))

mutants = []
for line in open(f"{root}/{OUT}/mutate_graders_unit_r16.txt", encoding="utf-8"):
    m = re.match(r"(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line.strip())
    if m:
        name, desc, killed = m.group(2), m.group(3), m.group(4)
        mutants.append({"id": name, "description": desc,
                        "killed_by": None if killed.strip() == "None" or m.group(1) == "SURVIVED" else killed.strip()})
fails = [r for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "SC1",
    "slice": "d",
    "round": 16,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 16 (did not build SC1-d; read the whole project.html, grader and labs; re-ran every gate; blind exemplar scoring; five new alternatives; four new mutants; re-ran every carried alternative folder)",
    "pin": "56cc575a",
    "base": "d1e65a02 (round-15 pin); delta read: project.html hunks 162, 436, 593; L01/L03/cards.json outside the slice; plans/FINAL-ARCHITECT-RULINGS.md rulings 17-18 (E4); ledgers/SC1 moves (lab-mutants, retired) and round-16 scripts",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE16-SC1-d",
    "scratch": "/tmp/sc1d-r16/",
    "scripts_dir": "ledgers/SC1/scripts/SC1-d-r16/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": SUMMARY,
}
json.dump(frag, open(f"{root}/ledgers/SC1/SC1-d.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
from collections import Counter
c = Counter(r["status"] for r in rows)
print("rows", len(rows), dict(c), "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
for r in fails:
    print("NON-PASS", r["id"], r["location"])
