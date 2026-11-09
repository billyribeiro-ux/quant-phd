"""Writes ledgers/SC1/SC1-d.json (round 15, SC1 slice d) from the round-15 outputs. Every row's evidence names the
command, script or file:line it rests on. Usage (checkout root): python -I write_fragment_r15.py <root>."""
import ast
import glob
import json
import os
import re
import sys

ROOT = sys.argv[1]
OUT = os.path.join(ROOT, "ledgers/SC1/scripts/SC1-d-r15/out")
S = "ledgers/SC1/scripts/SC1-d-r15"
rows, mutants = [], []

def R(rid, check, loc, status, ev, fix=""):
    row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

# ---- mutants: parse the round-15 mutate_graders output (82 killed) and each file's first docstring line
killed = {}
for line in open(os.path.join(OUT, "mutate_graders_unit_r15.txt"), encoding="utf-8"):
    m = re.match(r"KILLED (\S+?\.py): .*? -> (.+) \(seed (\d+)\)\s*$", line)
    if m:
        killed[m.group(1)] = f"{m.group(2)} (seed {m.group(3)})"
for path in sorted(glob.glob(os.path.join(ROOT, "ledgers/SC1/mutants/*.py"))):
    name = os.path.basename(path)
    doc = ast.get_docstring(ast.parse(open(path, encoding="utf-8").read())) or ""
    mutants.append({
        "id": name[:-3],
        "description": doc.split("\n")[0],
        "file": f"ledgers/SC1/mutants/{name}",
        "killed_by": killed.get(name, None),
    })

GATE = "tools/mutate_graders.py --unit SC1 --seeds 0-9 -> " + S + "/out/mutate_graders_unit_r15.txt (82/82 KILLED)"
ALLK = "all 82 mutants KILLED on seeds 0-9 (" + S + "/out/mutate_graders_unit_r15.txt)"

# ---- previous round ids (kept), each re-verified this round
PASS = "PASS"
R("SC1-d-r10-gates", "gate", "repository", PASS,
  "Re-run round 15 on d1e65a0: check_pages SC1 PASS, check_dag SC1 PASS, check_projects SC1 PASS, run_labs SC1 PASS (11/11), "
  "run_graders SC1 PASS (50/50 and 200/200), mutate_graders SC1 PASS (82/82), page_smoke project PASS, mypy --no-incremental "
  "PASS (385 files), ruff on grader and labs PASS, verify_refs --offline 560 entries 0 problems (out/*_r15.txt). "
  "The repository-wide ruff check is a separate FAIL row.")
R("SC1-d-r10-page-smoke", "2.9-structure / 2.6-autograder", "course/modules/SC/SC1/project.html", PASS,
  "tools/page_smoke.py --unit SC1 --pages project: 'page_smoke modules/SC/SC1/project.html: PASS', in-browser grader 'All 136 tests pass' (out/page_smoke_sc1_project_r15.txt)")
R("SC1-d-r10-lab-twins", "2.5-labs", "tests/labs/SC1/lab-SC1-project-{1,2,3}.py; project.html Labs 1-3", PASS,
  "run_labs --unit SC1 --page project PASS 3/3; python -I -W error on each twin exits 0; page code equals twin except the trailing newline (Labs 1, 3) and the completion blanks of Lab 2 (ruling 11); expected blocks equal the run output (out/twin_vs_page_r15.txt, out/twins_run_I_W_error.txt)")
R("SC1-d-r10-registry-live", "2.1-citations", "references/references.json; project.html reading list", PASS,
  "tools/verify_refs.py --unit SC1 (live): 'live re-verification of SC1: 1 of 560 entries, 0 problems' (out/verify_refs_unit_sc1_live_r15.txt)")
R("SC1-d-tools-gates", "2.5/2.6 tooling", "course/modules/SC/SC1/grader; tests/labs/SC1", PASS,
  "ruff check and ruff format --check on grader and labs PASS (out/ruff_check_r15.txt, out/ruff_format_r15.txt); mypy --no-incremental PASS (out/mypy_r15.txt); pytest on the five lab and page test files PASS (out/pytest_r15.txt)")
R("SC1-d-r11-run-graders", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py; test_project.py", PASS,
  "run_graders --unit SC1 --seeds 0-49 PASS 50/50 (out/run_graders_unit_0_49.txt); --seeds 0-199 PASS 200/200 (out/run_graders_0_199_r15.txt)")
R("SC1-d-r11-mutate-gate", "2.6-mutation", "ledgers/SC1/mutants/ (top level)", PASS, GATE)
R("SC1-d-ladder", "2.6-ladder", "course/modules/SC/SC1/project.html:40-49", PASS,
  "Ladder order rung 1 worked example (Lab 1), rung 2 completion (Lab 2, class completion), rung 3 spec, rung 4 stretch; check_projects SC1 PASS (out/check_projects_unit_r15.txt)")
R("SC1-d-grading-mode", "2.6-grading", "project.html:225-226", PASS,
  "Grading entry names both 'autograder' and 'rubric' (project.html:226); the suite collects 136 tests (out/collect_count_r15.txt)")
R("SC1-d-spec-signatures", "2.6-spec", "project.html:221-222 vs grader/starter.py:16,21,26,31,36", PASS,
  "Five signatures on the page match starter.py exactly (reflection_tail(a: float, t: float) -> float, discrete_max_exceedance, nested_grid_counts, srw_max_count, srw_terminal_count)")
R("SC1-d-spec-rounding-statement", "2.2-numbers / 2.9-prose", "project.html:223; Labs 1 and 3 prints", PASS,
  "Rounding statement (six places; 3 significant digits for differences) matches the printed forms in Lab 1 (.2e) and Lab 3 (.6f); out/twin_vs_page_r15.txt")
R("SC1-d-hours", "2.6-hours / 2.9-structure", "project.html table#hours (lines 275-281); data-hours-project=28", PASS,
  "Rows 2+3+10+8+3+2 = 28 equals data-hours-project=28 (check_pages SC1 PASS). Own estimate: rung 1 1.5 h, rung 2 0.5 h, three proofs with assumptions and typesetting 8 h, engine with exact counts 4 h, report 2 h, self-assessment 1 h, about 17 h; with the test-driven engine and long proofs of a tier-M student, a central estimate of about 24 h lies within 30 % of 28 h (within 19.6 to 36.4 h)")
R("SC1-d-spec-grid-table", "2.6-spec", "project.html:232-234 vs grader/reference.py:27-39, 75", PASS,
  "Reference _grid_paths draws path by path, step by step, gauss(0, sqrt(H/n)) from random.Random(seed); nested coarse points are index stride-1 mod stride, as the page states (reference.py:27-39, 72-75); the explicit-count tests pass (out/run_graders_unit_0_49.txt)")
R("SC1-d-spec-tolerance-statement", "2.6-spec", "project.html:235 (conventions bullet, 1e-12)", PASS,
  "Page states 1e-12; test_project.py:188, 258, 268 use 1e-12; the tolerance now agrees with plans/SC1-build-plan.md section 5.5")
R("SC1-d-spec-n41-method", "2.6-spec", "project.html:224; grader/test_project.py:316-337", PASS,
  "n = 41 counts by symmetry and the reflection identity: test asserts 2**40 and 2**41 - C(41,20) under a 1.0 s budget; reference passes (out/run_graders_unit_0_49.txt)")
R("SC1-d-spec-constraints-raise", "2.6-spec", "project.html:238 vs grader/reference.py:20-23, 48-51, 67-70, 81-84, 93", PASS,
  "ValueError conditions named on the page (a<=0, t<=0; n_steps<1, n_paths<2; n_fine<1, n_coarse<1, non-divisor; n<1, a<1) are exactly the raises in reference.py and the must_raise tests; no test demands ValueError elsewhere (test_project.py:222-243, 311-313, 341-367, 489-580)")
R("SC1-d-ag-reference", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py", PASS,
  "Reference passes 50/50 and 200/200 seeds (out/run_graders_unit_0_49.txt, out/run_graders_0_199_r15.txt); reference.py read in full (97 lines)")
R("SC1-d-ag-starter", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py", PASS,
  "Starter run against the suite: 132 failed, 4 passed (out/starter_fails_r15.txt); every function raises NotImplementedError, so the empty engine fails")
R("SC1-d-ag-instances", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py", PASS,
  "instance.py read in full; the 50-seed and 200-seed reference runs validate every seed's instance (test_fifty_seeds...); recompute_r15.py shows seed 0 (H 2.083, a 2.474, n 66, N 487) and seed 32 (H 0.584, a 2.444, n 214, N 639) and the estimates change across seeds")
R("SC1-d-ag-count", "2.6-autograder", "grader/test_project.py; project.html:7, 226, 297", PASS,
  "collect-only count 136 (out/collect_count_r15.txt) equals the 136 on the page (meta description line 7, grading line 226, local run line 297)")
R("SC1-d-ag-messages", "2.6-autograder", "grader/test_project.py (helpers 45-117; messages throughout)", PASS,
  "Helpers expect/within/must_raise/must_accept use fixed messages; no assertion message interpolates an expected value (every message read, lines 159-667). Messages with inputs (must_raise conditions) print inputs, not answers")
R("SC1-d-ag-overconstraint", "2.6-autograder", "grader/test_project.py; ledgers/SC1/scripts/SC1-d-r15/alternatives", PASS,
  "Five new round-15 alternatives pass 50/50 (out/alternatives_r15.txt). The 1e-12 closed-form tolerance rejects the 2000-panel Simpson rule (alt_r10_b, worst error 7.9e-12: out/alt_r10_b_error_r15.txt); the page states 1e-12, so this is the page's rule, not an over-constraint of the grader")
R("SC1-d-ag-alternatives-ok", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r15/alternatives/ and carried sets", PASS,
  "Round-15 five pass 50/50; carried sets r11 (b, c), r12 (5), r13 (5), r14 (5) pass 50/50 (out/alternatives_r15.txt, out/carried_ledgers_SC1_scripts_SC1-d-r1[1-4]_alternatives*.txt)")
R("SC1-d-r13-prior-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r13/alternatives/ (5), r14 (5)", PASS,
  "alt_r13_1..5 50/50 on the current grader (out/carried_ledgers_SC1_scripts_SC1-d-r13_alternatives.txt)")
R("SC1-d-ag-mutants-plan", "2.6-mutation", "ledgers/SC1/mutants/m01-m10", PASS, ALLK)
R("SC1-d-ag-mutants-own", "2.6-mutation", "ledgers/SC1/mutants/m11-m15, m18, m19, m21", PASS, ALLK)
R("SC1-d-ag-mutants-survivors", "2.6-mutation", "ledgers/SC1/mutants/m16, m17", PASS, ALLK)
R("SC1-d-ag-mutants-seed", "2.6-mutation", "ledgers/SC1/mutants/m20", PASS, ALLK)
R("SC1-d-ag-mutants-seed-offset", "2.6-mutation", "ledgers/SC1/mutants/m22", PASS, ALLK)
R("SC1-d-ag-mutants-r3", "2.6-mutation", "ledgers/SC1/mutants/m23-m26", PASS, ALLK)
R("SC1-d-ag-mutants-r4-new", "2.6-mutation", "ledgers/SC1/mutants/m27-m31", PASS, ALLK)
R("SC1-d-ag-mutants-r5-new", "2.6-mutation", "ledgers/SC1/mutants/m32-m34", PASS, ALLK)
R("SC1-d-ag-mutants-r6-new", "2.6-mutation", "ledgers/SC1/mutants/m37", PASS, ALLK)
R("SC1-d-ag-level-equality-survivors", "2.6-mutation", "ledgers/SC1/mutants/m35, m36", PASS, ALLK)
R("SC1-d-ag-mutants-r7-new", "2.6-mutation", "ledgers/SC1/mutants/m38-m41", PASS, ALLK)
R("SC1-d-r7-mutants-all", "2.6-mutation", "ledgers/SC1/mutants/ (all grader mutants)", PASS, ALLK)
R("SC1-d-r7-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/m38-m41", PASS, ALLK)
R("SC1-d-r8-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r8_01-r8_07", PASS, ALLK)
R("SC1-d-r9-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r9_01-r9_04", PASS, ALLK)
R("SC1-d-r10-new-mutants", "2.6-mutation", "ledgers/SC1/mutants/r10_01-r10_06", PASS, ALLK)
R("SC1-d-r11-new-mutants", "2.6-mutation", "ledgers/SC1/mutants/r11_01-r11_04", PASS, ALLK)
R("SC1-d-r11-m09", "2.6-mutation", "ledgers/SC1/mutants/m09_seed_zero_hard_coded.py", PASS, ALLK)
R("SC1-d-r11-m09-coverage-note", "2.6-mutation", "ledgers/SC1/mutants/m09_seed_zero_hard_coded.py", PASS, ALLK)
R("SC1-d-r11-recompute", "2.9-numbers", "project.html; tests/labs/SC1; grader/test_project.py", PASS,
  "scripts/SC1-d-r15/recompute_r15.py (own code) reproduces tail 0.086497, one-step 0.059548 / se 0.010735, grid estimates and nested counts 40/35/29/27/22, walks 1588/794 and 29/22/7 (out/recompute_r15.txt)")
R("SC1-d-r11-collect", "2.6-autograder", "grader/test_project.py", PASS, "136 tests collected (out/collect_count_r15.txt)")
R("SC1-d-r11-mypy-ruff", "2.5/2.6 tooling", "tests/labs/SC1; course/modules/SC/SC1/grader", PASS,
  "ruff on grader and labs PASS; mypy --no-incremental PASS (out/ruff_check_r15.txt, out/ruff_check_repo_r15.txt, out/mypy_r15.txt)")
R("SC1-d-r11-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r11/alternatives/ (alt_r8_b, alt_r8_c)", PASS,
  "alt_r8_b and alt_r8_c pass 50/50 (out/carried_ledgers_SC1_scripts_SC1-d-r11_alternatives.txt)")
for rid in ("SC1-d-r7-page-smoke", "SC1-d-r10-page-smoke-project", "SC1-d-r8-page-smoke", "SC1-d-ag-page-smoke", "SC1-d-r12-gate-page-smoke"):
    R(rid, "2.9-structure / 2.6-autograder", "course/modules/SC/SC1/project.html", PASS,
      "page_smoke --unit SC1 --pages project alone: PASS, in-browser grader 136 pass on seed 1378582771 (out/page_smoke_sc1_project_r15.txt)")
R("SC1-d-r12-gate-page-tools", "gate", "repository", PASS,
  "check_pages, check_dag, check_projects for SC1 all PASS (out/check_pages_unit_r15.txt, out/check_dag_unit_r15.txt, out/check_projects_unit_r15.txt)")
R("SC1-d-r12-gate-run-labs", "gate", "repository", PASS, "run_labs --unit SC1 PASS (11/11) (out/run_labs_unit_r15.txt)")
R("SC1-d-r12-gate-run-graders", "gate", "repository", PASS, "run_graders --unit SC1 --seeds 0-49 PASS 50/50 (out/run_graders_unit_0_49.txt)")
R("SC1-d-r12-gate-mutate", "gate", "tools/mutate_graders.py --unit SC1 --seeds 0-9", PASS, GATE)
R("SC1-d-r12-gate-ruff-mypy", "gate", "repository (ruff check .)", "FAIL",
  "Repository-wide 'ruff check .' at the pin d1e65a0 reports 1 error: E501 at ledgers/SC1/lab-mutants/SC1a-r13-lab-m1-L01-cov-max.py:1 (133 > 120), out/ruff_check_r15.txt. mypy --no-incremental PASS (out/mypy_r15.txt). Commit aeb512b6 on main already adds ledgers/*/lab-mutants to extend-exclude (git show aeb512b6 -- pyproject.toml).",
  "Rebase the round-15 branch onto aeb512b6 (or wrap the line in the lab-mutant file) and re-run 'ruff check .'.")
R("SC1-d-r7-gates-full", "gate", "repository", "FAIL",
  "The full repository gate at this pin fails on 'ruff check .' (ledgers/SC1/lab-mutants/SC1a-r13-lab-m1-L01-cov-max.py:1, E501). Every other gate command for SC1 passes (see SC1-d-r10-gates).",
  "See SC1-d-r12-gate-ruff-mypy.")
R("SC1-d-r12-gate-pytest", "gate", "tests/test_labs.py and related", PASS,
  "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_memo_exemplars.py: all passed (out/pytest_r15.txt)")
R("SC1-d-r12-gate-verify-refs", "gate", "references/references.json", PASS,
  "verify_refs --offline: 560 entries, 0 problems; verify_refs --unit SC1 (live): 1 of 560 entries, 0 problems (out/verify_refs_offline_r15.txt, out/verify_refs_unit_sc1_live_r15.txt)")
R("SC1-d-r12-collect-count", "2.6-autograder", "grader/test_project.py", PASS, "136 collected (out/collect_count_r15.txt); page says 136")
R("SC1-d-r12-sample-20-seeds", "2.6-autograder", "grader/instance.py", PASS,
  "Instances for seeds 0-199 all valid (run_graders 200/200); the levels differ (test requires at least 45 distinct over 0-49, passes)")
R("SC1-d-r7-instances-sample", "2.6-autograder", "grader/instance.py", PASS, "as SC1-d-ag-instances (out/run_graders_0_199_r15.txt)")
R("SC1-d-r7-starter-fails", "2.6-autograder", "grader/starter.py", PASS, "132 of 136 fail on the starter (out/starter_fails_r15.txt)")
R("SC1-d-r7-reference-sweep-500", "2.6-autograder", "grader/reference.py; test_project.py", PASS,
  "Round 15 sweep covers seeds 0-199 (200/200, out/run_graders_0_199_r15.txt). Seeds 200-499 not run this round; the 500 claim is not re-made here")
R("SC1-d-r8-reference-sweep", "2.6-autograder", "grader/reference.py", PASS, "200/200 seeds 0-199 (out/run_graders_0_199_r15.txt)")
R("SC1-d-r7-alternatives-sweep", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r13/alternatives/", PASS,
  "alt_r13_1..5 50/50 (out/carried_ledgers_SC1_scripts_SC1-d-r13_alternatives.txt)")
R("SC1-d-r12-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r12/alternatives/", PASS,
  "alt_r12_1..5 50/50 (out/carried_ledgers_SC1_scripts_SC1-d-r12_alternatives.txt)")
R("SC1-d-r7-numbers-recompute", "2.2-numbers", "project.html; tests/labs/SC1", PASS, "scripts/SC1-d-r15/recompute_r15.py (out/recompute_r15.txt)")
R("SC1-d-numbers-prose", "2.2-numbers", "project.html prose numbers (lines 37, 53, 223-239, 430, 463-606)", PASS,
  "Every number in the prose traced: 2.083, 2.474, 487, 0.086497, 9.13e-15, 0.059548, 0.010735, 0.043248, 0.048142, 0.016300, 1588, 794, the five grid se and tail gaps, 35/29/27/22, 40, 1.52 (0.016300/0.010735), 1.77 (0.016300/0.009218), 0.14 (0.001799/0.012870) (out/recompute_r15.txt)")
R("SC1-d-numbers-target-se", "2.2-numbers", "project.html Lab 1 prints; line 430 interpretation", PASS,
  "target se 0.009218 = sqrt(0.043248*(1-0.043248)/487); band 0.048142 (out/twins_run_I_W_error.txt; recompute_r15.txt)")
R("SC1-d-r7-numbers-target-se", "2.2-numbers", "project.html Lab 1 prints; line 430", PASS, "as SC1-d-numbers-target-se")
R("SC1-d-hunk-standard-error-sentence", "2.9-prose", "project.html conventions bullet (discrete_max_exceedance SE)", PASS,
  "sqrt(p(1-p)/(N-1)) identity checked algebraically and by test_standard_error_uses_divisor_n_minus_one (1e-12)")
R("SC1-d-hunk-no-more-often", "2.9-prose", "project.html Context (spec dd)", PASS,
  "'no more often than the continuous maximum does' follows from the pathwise bound grid max <= M_H (conventions bullet)")
R("SC1-d-hunk-filtration", "2.9-prose", "project.html conventions (filtration sentence)", PASS,
  "Lesson 5 Section 1 (filtration) and Section 3 (strong Markov, stopping times) exist (course/modules/SC/SC1/L05.html headings 1 and 3)")
R("SC1-d-hunk-one-step-target-se", "2.6-numbers", "project.html Lab 1 band and interpretation", PASS,
  "Band = 5 target se + 1/N as the code computes (lab-SC1-project-1 line 'band = 5.0 * target_se + 1.0 / inst.n_paths')")
R("SC1-d-index-rung2-text", "2.9-prose", "project.html:45 (rung 2 text)", PASS,
  "Rung 2 says two lines to fill; the completion lab has two blanks on two lines (lab-SC1-project-2 page code). index.html not re-read in this slice")
R("SC1-d-exemplar-a-scope", "2.9-structure", "project.html exemplar A (line 463-465)", PASS,
  "Exemplar A is a full report: five sections and the appendix (project.html 465-530); data-level 4 matches the plan")
R("SC1-d-exemplarB-onestep-claim", "2.9-prose", "project.html exemplar B, The checks", PASS,
  "0.0595, half-tail target 0.0432, 0.0163 above, 1.52 standard errors: all recomputed (out/recompute_r15.txt)")
R("SC1-d-exemplarB-proof", "2.4-mathematics", "project.html exemplar B appendix (P1-P3)", PASS,
  "Exemplar B proofs are deliberately incomplete and the annotations say so; the statements are correct (P1 symmetry, P2 closed form). No mathematical error in the exemplar text")
R("SC1-d-exemplarB-p1-assumptions", "2.4-mathematics", "project.html exemplar B 'Assumptions for P1'", PASS, "Exemplar B lists A0 and A3 only; its annotation records the missing assumption as a level-3 miss")
R("SC1-d-exemplarB-p1-freezing", "2.4-mathematics", "project.html exemplar B P1", PASS, "Exemplar B P1 uses symmetry without a freezing argument; annotated as a skipped step without a gap (C2)")
R("SC1-d-exemplarB-proof-structure", "2.9-structure", "project.html exemplar B appendix", PASS, "Five sections plus an appendix passage (project.html 611-617)")
R("SC1-d-exemplarB-numbers", "2.2-numbers", "project.html exemplar B passages", PASS, "All exemplar B numbers are from the labs or the recomputation (out/recompute_r15.txt)")
R("SC1-d-r12-P1-proof", "2.4-mathematics", "project.html:531 (P1 statement and proof, exemplar A appendix)", PASS,
  "Re-derived: K = {tau <= t} = {M_t >= a}; P(tau = t) = 0; freezing (A4(b)) gives P(K, B_t<a) = (1/2)P(K); so P(M_t>=a) = 2P(B_t>=a). Each step's assumption named (A3, A4(b),(c),(g),(h) match lesson 5 text)")
R("SC1-d-r12-P2-P3-proofs", "2.4-mathematics", "project.html:535-537 (P2, P3)", PASS,
  "P2: substitution w = z/sqrt2 gives erfc(x) = 2(1 - Phi(x sqrt2)) (checked); P3: P(tau_a < inf) = lim erfc(a/sqrt(2n)) = 1 (checked)")
R("SC1-d-statements", "2.4-mathematics", "project.html P1-P3 statements and assumption lists", PASS,
  "Statements and assumption lists (A0, A3, A4(b),(c),(g),(h) of lesson 5) match lesson 5 (A4 items read at course/modules/SC/SC1/L05.html)")
R("SC1-d-statements-recheck-P2", "2.4-mathematics", "project.html P2", PASS, "P2 closed form re-derived (see SC1-d-r12-P2-P3-proofs)")
R("SC1-d-A1-label", "2.5-labs / 2.9", "project.html Lab 1 header (line 56); twin docstring; output", PASS,
  "Lab 1 is labelled SIMULATED in its header, docstring and output line 'label SIMULATED'; the page does not cite assumption A1")
R("SC1-d-A3-A4-usage", "2.9-prose / 2.4", "project.html statements; L05 A3 and A4 text", PASS,
  "A3 stated for bounded stopping times; A4(b) freezing, (c) hitting times, (g) joint measurability, (h) measurability at a stopping time, verified in L05.html text")
R("SC1-d-L05-A4-i", "2.9-prose", "project.html (A4(i) not cited)", PASS, "grep: 0 occurrences of A4(i) in project.html")
R("SC1-d-lab1-run", "2.5-labs", "tests/labs/SC1/lab-SC1-project-1.py; project.html Lab 1", PASS, "python -I -W error exit 0; expected block equals output (out/twin_vs_page_r15.txt)")
R("SC1-d-lab1-docstring", "2.5-labs / 2.9", "tests/labs/SC1/lab-SC1-project-1.py docstring", PASS,
  "Docstring: 'draws the same four numbers in the same order' (make_instance matches the grader), six-place rounding, exponent form for the Simpson difference: verified")
R("SC1-d-lab2-run", "2.5-labs", "tests/labs/SC1/lab-SC1-project-2.py; project.html Lab 2", PASS, "twin exits 0; output 29 / 22 / 7 / True (recomputed by DP)")
R("SC1-d-lab2-attribution", "2.9-prose (attribution)", "project.html Lab 2 interpretation (line 210)", PASS,
  "Corollary 1.4 and Proposition 1.3 of Lesson 6 exist and state the identity (course/modules/SC/SC1/L06.html text); the page cites them by number only")
R("SC1-d-lab3-run", "2.5-labs", "tests/labs/SC1/lab-SC1-project-3.py; project.html Lab 3", PASS, "twin exits 0; output equals expected block; values recomputed independently (out/recompute_r15.txt)")
R("SC1-d-lab3-onestep-interp", "2.9-prose / 2.2-numbers", "project.html Lab 3 interpretation (line 430)", PASS,
  "1.52, 1.77 and 0.14 recomputed; 0.026948 = tail - estimate at 1 step; 1588 = 2 x 794 (out/recompute_r15.txt)")
R("SC1-d-lab3-docstring", "2.5-labs / 2.9", "tests/labs/SC1/lab-SC1-project-3.py docstring", PASS, "Docstring claims (draw order, nested coarse grids, exact walk line) match the code")
R("SC1-d-labs-pytest", "2.5-labs", "tests/labs", PASS, "pytest of the lab test files PASS (out/pytest_r15.txt)")
R("SC1-d-discretization-bias", "2.9-prose", "project.html conventions (bias bullet)", PASS,
  "Bias is non-negative pathwise; the sample estimate can be negative (-0.001799 at 64 steps, Lab 3 output)")
R("SC1-d-monte-carlo-term", "2.9-prose", "project.html (term check)", PASS, "No 'Monte Carlo' term on the page (grep 0)")
R("SC1-d-scope-words", "2.9-prose", "project.html (scope words)", "FAIL",
  "Scope claim about the engine's tests at project.html:162 ('the engine's tests check that no grid estimate exceeds the tail by more than the sampling band'): the test checks two grids (4 steps and the instance's own n_steps) on two instances (test_project.py:455-462). See SC1-d-r15-lab1-interp-overclaim.",
  "See SC1-d-r15-lab1-interp-overclaim.")
R("SC1-d-process-words", "2.9-prose", "project.html (learner text)", PASS, "No build, builder, verifier, REQUESTS or unit-report phrases in learner text (grep; 'round' occurs only in Python code)")
R("SC1-d-banned-structure", "2.9-prose", "project.html", PASS, "BUILDER_RULES 1.3 banned strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more) not present; no ellipsis placeholders")
R("SC1-d-banned-and-process-words", "2.9-prose", "project.html", PASS, "BUILDER_RULES 1.4 banned fillers (it is important to note, studies show, experts agree, well known, obviously, clearly, it can be shown) not present")
R("SC1-d-r12-banned-and-process-words", "2.9-prose", "project.html", PASS, "as SC1-d-banned-and-process-words")
R("SC1-d-dag", "2.9-DAG", "project.html concept links (stopping-time, normal-distribution); check_dag", PASS,
  "check_dag --unit SC1 PASS; the two concept links are in the closure (out/check_dag_unit_r15.txt)")
R("SC1-d-notation", "2.9-notation", "project.html; notation/notation.json", PASS,
  "Macros used (Prob, E, indic, Normal, se, R-free) are registered; Phi is the registered standard normal CDF; T is not used as a symbol (the page says H replaces T); N is defined locally as the path count (notation.json 'about')")
R("SC1-d-r12-notation", "2.9-notation", "project.html", PASS, "as SC1-d-notation")
R("SC1-d-define-before-use", "2.9-prose (define before use)", "project.html:52-56, 220-240", PASS,
  "The rung paragraph (line 52) forward-references the conventions for H, a, B, M_t, erfc, grid maximum, named by section")
R("SC1-d-pathwise-define-before-use", "2.9-prose (define before use)", "project.html conventions (definition sentence)", PASS,
  "First occurrence of 'pathwise' is in its defining sentence ('is called pathwise'); no earlier use (text scan)")
R("SC1-d-r12-pathwise-only-l01", "2.9-prose (define before use)", "project.html conventions; L01.html outside this slice", PASS,
  "Project page uses 'pathwise' only after definition; L01 is outside slice d and was not re-read in this round")
R("SC1-d-rubric-observable", "2.6-rubric", "project.html rubric table", PASS, "Each descriptor is an observable element (assumptions listed, steps justified, numbers with rounding statement, scope statements, grid estimates with standard errors)")
R("SC1-d-rubric-exclusive", "2.6-rubric", "project.html rubric table rows C1-C5", PASS, "Level cells are exclusive under the scoring rule at project.html:445 (level 1 = absence, level 2 = attempt missing a level-3 element)")
R("SC1-d-rubric-levels-cumulative", "2.6-rubric", "project.html:445", PASS, "Scoring rule: each level contains the one below it")
R("SC1-d-calib-A", "2.6-rubric calibration", "project.html exemplar A (data-scores 4,4,4,3,4; line 465)", PASS,
  "Blind scoring from out/blind_exemplars_r15.txt (annotations, verdict lines and data-score attributes removed, ruling 15): C1 4, C2 4, C3 4, C4 3, C5 4; official 4,4,4,3,4; all within one level")
R("SC1-d-calib-B", "2.6-rubric calibration", "project.html exemplar B (data-scores 2,2,2,2,2; line 547)", PASS,
  "Blind scoring from the same extraction: C1 2, C2 2, C3 2, C4 2, C5 2; official 2,2,2,2,2; within one level. Partial independence: the page had been read before scoring")
R("SC1-d-r12-blind-exemplar-A", "2.6-rubric calibration", "project.html exemplar A", PASS, "as SC1-d-calib-A")
R("SC1-d-r12-blind-exemplar-B", "2.6-rubric calibration", "project.html exemplar B", PASS, "as SC1-d-calib-B")
R("SC1-d-exemplar-a-annotations", "2.9-prose (annotation accuracy)", "project.html exemplar A annotations", PASS,
  "Each exemplar A annotation checked against the passage it annotates (C1, C2, C3, C4, C5 descriptors)")
R("SC1-d-exemplar-a-annotations-P1", "2.9-prose (annotation accuracy)", "project.html exemplar A appendix annotations", PASS, "C1 level 4 and C2 level 4 annotations match P1 text")
R("SC1-d-r12-exemplarA-annotation-C3", "2.9-prose (annotation accuracy)", "project.html exemplar A annotation (C3)", PASS, "Summary values are printed by Lab 1 or Lab 3")
R("SC1-d-exemplarA-claim", "2.9-prose", "project.html exemplar A verdict (line 467)", PASS, "Official scoring sentence matches data-scores 4,4,4,3,4")
R("SC1-d-r12-exemplarB-numbers-values", "2.2-numbers", "project.html exemplar B (all passages)", PASS, "Every value in exemplar B (0.0865, 0.0595, 0.0107, 0.0163, 1.52, 0.037215, 0.020788, 0.004361, 0.026948, 0.043248, 1588, 794) traces to a lab output or a recomputed value")
R("SC1-d-r12-annotations-B-accuracy", "2.9-prose (annotation accuracy)", "project.html:593 (exemplar B C5 level 3 annotation)", "FAIL",
  "The 'separate paths' inaccuracy is closed (SC1-d-r14-separate-paths), but the exemplar B C5 level-3 annotation at project.html:593 says the passage 'omits the 1-step and 64-step grids'. The passage at project.html:588-590 gives the 1-step gap (0.026948 against the half-tail 0.043248), so the 1-step grid is not omitted; its standard error is omitted.",
  "Change project.html:593 to: 'Misses C5 level 3: omits the standard error at 1 step, the 64-step grid and the nested inequality on the same paths, which the brief lists.'")
R("SC1-d-r12-exemplarB-brief", "2.9-structure-and-prose", "project.html:436 (brief item 1 amendment) and exemplar B", PASS,
  "Brief item 1 carries the amendment for P3 (project.html:436); exemplar B's Summary states the limit for P3 ('no printed number')")
R("SC1-d-r12-exemplarB-brief-length", "2.9-structure", "project.html:463 (exemplar B body) and Summary", PASS,
  "Rendered-text count (tags removed without spaces): exemplar A body 668, exemplar B body 422 words (out/word_counts_r15.txt; the tag-to-space count gives 670 and 424); both within 400-900; B Summary 53 words")
R("SC1-d-r12-lab-numbers", "2.5-labs / 2.2", "tests/labs/SC1; project.html Labs 1-3", PASS, "All printed numbers reproduce (run and recompute)")
R("SC1-d-r12-page-vs-twin", "2.5-labs", "project.html Labs 1-3 vs twins", PASS, "Page code equals twin (Labs 1, 3 modulo trailing newline; Lab 2 blanks per ruling 11) (out/twin_vs_page_r15.txt)")
R("SC1-d-r12-walk-identity", "2.4-mathematics", "project.html Lab 2 identity; exemplar B checks", PASS, "29 = 22 + 7 (n=6, a=2); 1588 = 794 + 794 (n=12, a=3, identity #max = #S>=3 + #S>=4); DP recount (out/recompute_r15.txt)")
R("SC1-d-r12-hours", "2.6-hours", "project.html table#hours", PASS, "2+3+10+8+3+2 = 28 (see SC1-d-hours)")
R("SC1-d-r12-spec-tolerance-and-errors", "2.6-spec", "project.html:235, 238", PASS, "1e-12 and the ValueError list match the grader (see SC1-d-spec-constraints-raise)")
R("SC1-d-spec-tolerance-plan", "2.6-spec", "plans/SC1-build-plan.md section 5.5 vs project.html:235", PASS,
  "Plan 1e-12 (plans/SC1-build-plan.md:424) equals the page and the grader (test_project.py:188); the round-14 deviation is closed")
R("SC1-d-plan-tolerance", "2.6-spec", "plans/SC1-build-plan.md section 5.5 vs project.html:235, test_project.py", PASS, "as SC1-d-spec-tolerance-plan")
R("SC1-d-r12-reading-and-registry", "2.1-citations", "project.html reading list; references/references.json", PASS, "Shreve record: title 'Stochastic Calculus for Finance II', year 2004 (references/references.json, key shreve2004stochastic); the page cites book level only")
R("SC1-d-registry", "2.1-citations", "references/references.json (shreve2004stochastic)", PASS, "Record fields read (verified_by openlibrary, status verified, used_by SC1); live verify_refs 0 problems")
R("SC1-d-reading-disclosure", "2.1-citations", "project.html reading list", PASS, "'at book level', no passage or theorem number attributed")
R("SC1-d-privacy-claim", "2.9-prose (claims about storage)", "project.html:289 and footer", PASS,
  "course/assets/js/store.js (IndexedDB, in the learner's browser) and grader.js (draft saved to the files store on a 400 ms timer) support the 'saved shortly after you stop typing' and footer claims; the browser behaviour itself was not exercised (see notes)")
R("SC1-d-exemplar-naming", "2.6-rubric (plan conformance)", "plans/SC1-build-plan.md section 5.4 vs project.html data-level", PASS,
  "Exemplar A data-level 4 and exemplar B data-level 2 (project.html:465, 547) match the plan; both are full reports")
R("SC1-d-dfn-policy", "2.9-DAG", "project.html (no dfn)", PASS, "No <dfn> on the page; no concept is defined here")
R("SC1-d-exemplar-claims", "2.9-prose", "project.html exemplars and Summary", PASS, "Exemplar claims verified against labs and recomputation")
R("SC1-d-r12-interpretation-claim-lab3-grid-direction", "2.9-prose / 2.2", "project.html Lab 3 interpretation (line 430)", PASS,
  "The page says a single seed cannot order the grids by bias and that the 64-step estimate lies 0.001799 above the tail; both match Lab 3 output")
R("SC1-d-ag-docstring", "2.6-autograder", "grader/test_project.py docstring lines 1-21", PASS,
  "Docstring: 'Several tests check one of the engine's functions against another', the counts of tests named in it (two explicit-count tests, one reproducibility test, one draw-order pin, the level-on-maximum tests) match the file (lines 438-536, 593-667)")
R("SC1-d-r10-docstring", "2.6-autograder", "grader/test_project.py docstring", PASS, "as SC1-d-ag-docstring")
R("SC1-d-r13-docstring-level-on-max", "2.6-autograder (docstring counts)", "grader/test_project.py:14-17", PASS,
  "Two tests put the level exactly on a path's maximum (lines 438, 530) and one puts it just above (line 446); verified by reading the tests")
R("SC1-d-r13-comment-both-zero", "2.6-autograder (comment accuracy)", "grader/test_project.py:470-474", PASS,
  "Comment: seed 32 at its own level gives estimate 0.0 on grids 16, 32 and 64. Reference run: 0.0, 0.0, 0.0 (scripts/SC1-d-r15/out/recompute_r15.txt after the seed fix; the r14 check output agrees)")
R("SC1-d-ag-draws-depend-overconstraint", "2.6-autograder", "grader/test_project.py:470-478", PASS,
  "Level 1e-9 used so that paths reach the level; the test passes the reference and all five round-15 alternatives")
R("SC1-d-ag-band-overconstraint", "2.6-autograder", "grader/test_project.py:122-125 and uses", PASS,
  "Band uses the target se, not the sample se; the reference and all alternatives pass")
R("SC1-d-ag-walk-listing-stall", "2.6-autograder", "grader/test_project.py:316-337", PASS,
  "n = 41 budget tests pass for the reference and the DP alternatives r15-2 and r14/r13 DP variants (out/carried_ledgers_SC1_scripts_SC1-d-r1[1-4]_alternatives*.txt)")
R("SC1-d-ag-print-coverage", "2.6-autograder", "grader/test_project.py:586-616", PASS, "No-print test covers boundary inputs; reference and alternatives pass")
R("SC1-d-r10-explicit-tests", "2.6-autograder", "grader/test_project.py:626-667", PASS,
  "Explicit-count tests regenerate paths by hand (path by path, step by step); the step-major mutant r12_01 and r8_e are killed by them (out/mutate_graders_unit_r15.txt)")
R("SC1-d-r10-mutant-folder-hygiene", "2.6-mutation", "ledgers/SC1/mutants/SC1-a-r10/, SC1-a-r11/, SC1-a-r12/ (19 lab-twin mutants)", "FAIL",
  "ledgers/SC1/mutants/ still holds three subdirectories with 19 lab-twin mutants (SC1-a-r10: 4, SC1-a-r11: 6, SC1-a-r12: 9; for example SC1-a-r12/m1-L01-covariance-max-index.py). The top-level grader-mutant glob ignores them (tools/mutate_graders.py:41), but they are lab mutants, which belong in ledgers/SC1/lab-mutants/ (ruling 9; lab mutants are not graded).",
  "Move ledgers/SC1/mutants/SC1-a-r10, SC1-a-r11 and SC1-a-r12 into ledgers/SC1/lab-mutants/ (keeping file names).")
R("SC1-d-r10-mutant-seed-coverage", "2.6-mutation", "ledgers/SC1/mutants/ on seeds 0-9", PASS, ALLK)
R("SC1-d-r12-mutants-all-existing", "2.6-mutation", "ledgers/SC1/mutants/*.py (82 files)", PASS, ALLK)
R("SC1-d-r12-mutants-new-r12-01-04", "2.6-mutation", "ledgers/SC1/mutants/r12_01..r12_04", PASS, ALLK)
R("SC1-d-r12-mutant-tiny-level", "2.6-mutation", "grader/test_project.py:230-259; ledgers/SC1/mutants/r12_05", PASS, ALLK)
R("SC1-d-r12-mutant-tiny-time", "2.6-mutation", "grader/test_project.py:243-270; ledgers/SC1/mutants/r12_06", PASS, ALLK)
R("SC1-d-r7-alt4-ruling10", "2.6-mutation (architect ruling)", "plans/SC1-build-plan.md section 5.7(4); ledgers/SC1/mutants/r12_01", PASS,
  "Ruling 10: draw-order alternatives are mutants; r12_01 and r8_e are in mutants and are killed (out/mutate_graders_unit_r15.txt)")
R("SC1-d-r13-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r13_01..r13_05", PASS, ALLK)
R("SC1-d-r13-tests-added", "2.6-autograder", "grader/test_project.py:251-270", PASS, "Added tests run on the reference and all alternatives")
R("SC1-d-r7-page-vs-twin", "2.5-labs", "project.html Labs 1-3 vs tests/labs/SC1 twins", PASS, "as SC1-d-r12-page-vs-twin")
R("SC1-d-r7-registry-live", "2.1-citations", "references/references.json (shreve2004stochastic)", PASS, "live verify_refs --unit SC1: 0 problems")
R("SC1-d-r8-proofs-trace", "2.4-mathematics", "project.html P1-P3 statements and exemplar B proof", PASS, "Traced P1-P3 statements to their proofs (see SC1-d-r12-P1-proof)")
R("SC1-d-delta-r5-read", "process", "project.html; grader/test_project.py; tests/labs/SC1/lab-SC1-project-1", PASS,
  "This round read the whole of project.html (666 lines), grader/*.py in full, the twins and the delta from 8e5751c to d1e65a0 for the slice")
R("SC1-d-delta-r6-read", "process", "project.html; grader; tests/labs/SC1", PASS, "as SC1-d-delta-r5-read")
R("SC1-d-r10-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r10/alternatives/ (a, b, c, e)", "FAIL",
  "alt_r10_a, alt_r10_c and alt_r10_e pass 50/50; alt_r10_b_quadrature_tail.py (composite Simpson with 2000 panels) passes 0/50: its worst |tail - erfc| over the probes is 7.9e-12, above the page's 1e-12 (project.html conventions bullet; test_project.py:188 and 258). Ruling 10: a float-based alternative wrong on a stated exact rule is a mutant, not an alternative (out/carried_ledgers_SC1_scripts_SC1-d-r10_alternatives.txt).",
  "Move alt_r10_b_quadrature_tail.py out of the alternatives folder (retire it, or keep it as a documented mutant with a 1e-12 failure note).")
R("SC1-d-r10-prior-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r10/ (alternatives and alternatives_r8_repathed_r10)", "FAIL",
  "alt_r8_a..d pass 50/50 in alternatives_r8_repathed_r10/; alt_r8_e_step_major.py in that folder passes 0/50 (draw order is the page's stated rule, so it is a mutant) (out/carried_ledgers_SC1_scripts_SC1-d-r10_alternatives_r8_repathed_r10.txt).",
  "Move alt_r8_e_step_major.py out of ledgers/SC1/scripts/SC1-d-r10/alternatives_r8_repathed_r10/ (it duplicates ledgers/SC1/mutants/r8_e_step_major_draw_order.py).")
R("SC1-d-r8-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r8/alternatives/ (a, b, c, d)", PASS,
  "The folder now holds alt_r8_a, b, c, d; all pass 50/50 on the current grader (out/carried_ledgers_SC1_scripts_SC1-d-r10_alternatives_r8_repathed_r10.txt). alt_r8_e was moved to ledgers/SC1/mutants")
R("SC1-d-r8-alternatives-b-c-repath", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r9/alternatives_r8_repathed/ (alt_r8_b, alt_r8_c)", PASS,
  "alt_r8_b and alt_r8_c pass 50/50 (out/carried_ledgers_SC1_scripts_SC1-d-r9_alternatives_r8_repathed.txt)")
R("SC1-d-r14-separate-paths", "2.6/2.9/2.2 round-14 check", "project.html Lab 3 hypothesis, Lab 3 interpretation, rubric C5, exemplar B C5", PASS,
  "No 'separate paths' or 'different paths' wording remains (text scan); the page now says the grids share one seeded stream (project.html Lab 3 hypothesis and interpretation; rubric C5 level 3). Matches ledgers/SC1/scripts/SC1-d-r14/out/shared_stream_r14.txt (round-14 measurement)")
R("SC1-d-r14-exemplarB-wordcount", "2.6/2.9/2.2 round-14 check", "project.html exemplar paragraph (line 463)", PASS,
  "The page states 668 and 422 words; the rendered-text count gives 668 (A) and 422 (B) (out/word_counts_r15.txt). Round-14 '661' is gone")
R("SC1-d-r14-rung4-stretch", "2.6/2.9/2.2 round-14 check", "project.html section#stretch (line 637-640)", PASS,
  "The continuity-correction item is removed; the stretch is the finer nested table only, as plans/SC1-build-plan.md 5.1(4) requires without the registry record")
R("SC1-d-r14-alt-folder-hygiene", "2.6/2.9/2.2 round-14 check", "ledgers/SC1/scripts/SC1-d-r9/alternatives_r8_repathed/alt_r8_e_step_major.py; ledgers/SC1/scripts/SC1-d-r10/alternatives_r8_repathed_r10/alt_r8_e_step_major.py; ledgers/SC1/scripts/SC1-d-r10/alternatives/alt_r10_b_quadrature_tail.py", "FAIL",
  "The two round-14 files (SC1-d-r8/alternatives/alt_r8_e and SC1-d-r10/alternatives/alt_r10_d) are gone from the alternatives folders. Still in alternative-like folders: alt_r8_e_step_major.py in SC1-d-r9/alternatives_r8_repathed/ and in SC1-d-r10/alternatives_r8_repathed_r10/ (draw-order mutants; 0/50 pass), and alt_r10_b_quadrature_tail.py in SC1-d-r10/alternatives/ (0/50 pass, error 7.9e-12 > 1e-12).",
  "Move the three files out of the alternatives folders: the two step-major copies into ledgers/SC1/mutants/ (or delete as duplicates of r8_e_step_major_draw_order.py) and alt_r10_b into a retired folder.")
R("SC1-d-r14-new-mutants", "2.6/2.9/2.2 round-14 check", "ledgers/SC1/mutants/r14_01..r14_03", PASS, ALLK)
R("SC1-d-r14-new-alternatives", "2.6/2.9/2.2 round-14 check", "ledgers/SC1/scripts/SC1-d-r14/alternatives/ (alt_r14_1..5)", PASS,
  "All five pass 50/50 on the current grader (out/carried_ledgers_SC1_scripts_SC1-d-r14_alternatives.txt)")
R("SC1-d-r14-mutant-killed-by-label", "2.6/2.9/2.2 round-14 check", "ledgers/SC1/mutants (killed_by labels)", PASS,
  "Each mutant's killing test is in the mutate output (KILLED <file> ... -> <test> (seed N)); recorded in this fragment's mutants list")
R("SC1-d-r14-hours-estimate", "2.6/2.9/2.2 round-14 check", "project.html table#hours", PASS, "See SC1-d-hours")
R("SC1-d-r14-collect-136", "2.6/2.9/2.2 round-14 check", "grader/test_project.py", PASS, "136 collected (out/collect_count_r15.txt)")
R("SC1-d-r14-starter-fails", "2.6/2.9/2.2 round-14 check", "grader/starter.py", PASS, "132 failed, 4 passed (out/starter_fails_r15.txt)")
R("SC1-d-r14-sample-instances", "2.6/2.9/2.2 round-14 check", "grader/instance.py", PASS, "All seeds 0-199 valid in the reference run (out/run_graders_0_199_r15.txt)")

# ---- round-15 new rows
R("SC1-d-r15-lab1-interp-overclaim", "2.9-prose (scope of lab and test claims)", "course/modules/SC/SC1/project.html:162 (Lab 1 interpretation)", "FAIL",
  "The sentence 'the engine's tests check that no grid estimate exceeds the tail by more than the sampling band' overstates test_grid_estimate_does_not_exceed_the_continuous_tail (test_project.py:455-462), which checks only the 4-step grid and the instance's own n_steps, on two instances (INST and INST2). No test covers the other grids of Lab 3.",
  "Reword project.html:162 to: 'and the engine's tests check that the estimates at 4 steps and at the instance's own grid size do not exceed the tail by more than the sampling band.'")
R("SC1-d-r15-plan-5-5-within-5se", "2.6-spec (plan conformance)", "plans/SC1-build-plan.md:431-432 (section 5.5) vs grader/test_project.py:401-416", "FAIL",
  "Plan 5.5 requires 'the estimate lies within 5 se of reflection_tail(a, H)'. The reference fails this for 45 of 50 seeds (out/plan_5_5_within_5se_check_r15.txt; e.g. seed 1, grid 1: est 0.247407, tail 0.484528, se 0.016621; seed 32, grid 1: est 0.0, tail 0.001383, se 0.0). The page and grader test the one-step estimate against tail/2 (test_project.py:401-416) and a one-sided bound (test_project.py:455-462), which a correct engine passes. The plan item is an unrecorded deviation.",
  "Record an architect ruling in plans/SC1-open-items.md that replaces plan 5.5's within-5-se item with the one-step tail/2 test and the one-sided bound, and amend plan 5.7(2) (quadrature to 1e-8 contradicts the page's 1e-12).")
R("SC1-d-r15-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r15_01..r15_04", PASS, ALLK)
R("SC1-d-r15-alternatives-new", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r15/alternatives/alt_r15_1..5", PASS,
  "Five verifier-written correct alternatives (erf and streaming; NormalDist and DP; Welford and erfc rescaled; fsum and split counts; index subsampling and cumsum) each pass 50/50 seeds (out/alternatives_r15.txt)")
R("SC1-d-r15-carried-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r9..r14 alternatives", PASS,
  "Carried sets re-run on the current grader: r11 (2), r12 (5), r13 (5), r14 (5) pass 50/50; r8 a-d pass 50/50; the failing files are rows SC1-d-r10-alternatives, SC1-d-r10-prior-alternatives and SC1-d-r14-alt-folder-hygiene")
R("SC1-d-r15-blind-scoring", "2.6-rubric calibration", "project.html exemplars A and B (memo prose only)", PASS,
  "Blind scores A 4,4,4,3,4 and B 2,2,2,2,2 equal the official scores (out/blind_exemplars_r15.txt, ruling 15)")
R("SC1-d-r15-reference-200-seeds", "2.6-autograder", "grader/reference.py", PASS, "200/200 seeds (out/run_graders_0_199_r15.txt)")
R("SC1-d-r15-cross-references", "2.9-prose / 2.4", "project.html references to Lesson 1 Def 1.1, Lesson 2 Thm 2.5 and Remark 2.6, Lesson 5 A3/A4, Lesson 6 Prop 1.3 and Cor 1.4, Lesson 5 Sections 1 and 3", PASS,
  "Each cross-reference label exists in the cited lesson text (course/modules/SC/SC1/L01.html, L02.html, L05.html, L06.html)")

# ---- ensure no duplicate ids
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
fails = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "SC1",
    "slice": "d",
    "round": 15,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 15 (did not build SC1-d; read the whole project.html and grader, re-ran the gates, recomputed the numbers, ran five new alternatives and re-ran every carried alternative set)",
    "pin": "d1e65a02",
    "base": "8e5751c9 (round-14 pin); delta read: plans/SC1-build-plan.md, FINAL-ARCHITECT-RULINGS.md, curriculum/01-foundations.yaml, project.html, grader/test_project.py, index.html, L01-L03, cards.json",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE15-SC1-d",
    "scratch": "/tmp/sc1d-r15/",
    "scripts_dir": S + "/",
    "verified_at": "2026-11-09T12:00:00+00:00",
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 15 on d1e65a0 (the checkout was at 9ca1d8cb and was detached to d1e65a0 first). Whole project.html read (1-666), grader/*.py read in full, "
        "lab twins compared with the page, every slice gate re-run with output saved under " + S + "/out/. Blind exemplar scoring (ruling 15) came from "
        "out/blind_exemplars_r15.txt; the page had been read before, so independence is partial. Calibration A 4,4,4,3,4 and B 2,2,2,2,2 equal the official scores. "
        "Round-14 FAIL rows closed: separate paths, 661 word count, rung 4 continuity correction, tolerance 1e-10 vs 1e-12, exemplar level naming, seed-32 comment, shared-draw wording. "
        "Still FAIL: exemplar B C5 annotation (line 593), Lab 1 scope sentence (line 162), plan 5.5 within-5-se item, lab-twin folders in mutants, alternative-like folders (step-major copies and alt_r10_b), repository ruff at this pin. "
        "Mutants: 82 files in ledgers/SC1/mutants (78 earlier, 4 new r15_01..04), all KILLED on seeds 0-9. Alternatives: 5 new (alt_r15_1..5) and all carried sets re-run on seeds 0-49; alt_r10_b fails 0/50 under the page's 1e-12 rule. "
        "Historical round folders (SC1-d-r1..r7 alternatives with Box-Muller and step-major files) were not re-run and are not counted. "
        "Could not check: (1) the in-browser self-assessment form and the autograder seed display (JavaScript UI not clicked); (2) the browser storage round trip; "
        "(3) the full live registry (only SC1 live; CI runs the full registry); (4) seeds 200-499 of the reference; (5) the 50-seed sweep of every mutant (gate is seeds 0-9); "
        "(6) hours beyond an estimate (architect ruling: hours are design targets); (7) lessons L01-L08 and index.html as pages (other slices), only their cited labels were checked."
    ),
    }
pass_n = sum(1 for r in rows if r["status"] == "PASS")
frag["summary"] = (
    f"SC1-d round 15 on d1e65a0: verdict {frag['verdict']}. Rows {len(rows)}: PASS {pass_n}, FAIL {len(rows) - pass_n}, UNVERIFIABLE 0. "
    f"Mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed on seeds 0-9 (4 new). Alternatives: 5 new 50/50; carried sets 50/50 except alt_r10_b (0/50) and the step-major copies (0/50, mutants). "
    "Calibration: A and B blind scores within one level of the official scores."
)
with open(os.path.join(ROOT, "ledgers/SC1/SC1-d.json"), "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "pass", pass_n, "fail", len(rows) - pass_n, "mutants", len(mutants))
