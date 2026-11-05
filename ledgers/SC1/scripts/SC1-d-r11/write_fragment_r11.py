#!/usr/bin/env python3
"""Write the round-11 SC1 slice-d fragment ledgers/SC1/SC1-d.json from the outputs in scripts/SC1-d-r11/out/.

Every row cites the command or script whose output backs it. Run from the checkout root:
    .venv/bin/python ledgers/SC1/scripts/SC1-d-r11/write_fragment_r11.py
"""

from __future__ import annotations

import ast
import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers/SC1/scripts/SC1-d-r11/out"
MUT = ROOT / "ledgers/SC1/mutants"
S = "ledgers/SC1/scripts/SC1-d-r11"

PIN = "11d7077a290f7960b183d3a5a6631af4773888f9"
BASE = "00a84795f276456fce19d4181373cc4efba11a36"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> dict[str, str]:
    out = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        out["fix"] = fix
    return out


ROWS: list[dict[str, str]] = [
    # ---- gates and commands (run this round on pin 11d7077) ----
    row("SC1-d-r10-gates", "gate", "repository", "PASS",
        f"check_pages --unit SC1 PASS, check_dag --unit SC1 PASS, check_projects --unit SC1 PASS ({S}/out/check_*_SC1.txt); "
        f"run_labs --unit SC1 'PASS (11/11)' ({S}/out/run_labs_SC1.txt); mypy --no-incremental 'Success: no issues found in 385 "
        f"source files' ({S}/out/mypy.txt); verify_refs --offline '560 entries, 0 problems' ({S}/out/verify_refs_offline.txt); "
        "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py "
        f"tests/test_docs_figures.py (selected) exit 0 ({S}/out/pytest_sc1_related.txt)."),
    row("SC1-d-r10-page-smoke", "2.9-structure / 2.6-autograder", "course/modules/SC/SC1/project.html", "PASS",
        "page_smoke.py --unit SC1 --pages project: 'page_smoke modules/SC/SC1/project.html: PASS', in-browser grader "
        f"'All 134 tests pass on seed 884571770' ({S}/out/page_smoke_SC1_project.txt)."),
    row("SC1-d-r10-lab-twins", "2.5-labs", "tests/labs/SC1/lab-SC1-project-{1,2,3}.py; project.html Labs 1-3", "PASS",
        "run_labs --unit SC1 checks each page lab is byte-identical to its twin, runs the twin under python -I -W error, "
        "and matches the expected block: 11/11 PASS. Twins unchanged in the delta 00a84795..11d7077 (git diff --stat empty "
        "for tests/labs/SC1)."),
    row("SC1-d-r10-registry-live", "2.1-citations", "references/references.json; project.html reading list", "PASS",
        "shreve2004stochastic record: title 'Stochastic Calculus for Finance II', year 2004, status verified, used_by SC1. "
        "Plain curl to https://openlibrary.org/search.json?title=stochastic+calculus+for+finance+ii&author=shreve returned HTTP 200 "
        "with 'Stochastic Calculus for Finance Ii' by Steven E. Shreve, first_publish_year 2004 (entry OL1518086A). The "
        "reading line cites book level only, with no passage or theorem number. The record is byte-identical across "
        "00a84795..11d7077 (delta touches only generated_at and other entries' used_by)."),
    row("SC1-d-tools-gates", "2.5/2.6 tooling", "repository", "PASS",
        f"ruff check and ruff format --check on course/modules/SC/SC1/grader and tests/labs/SC1: 'All checks passed!' and "
        f"'15 files already formatted' ({S}/out/ruff_check_sc1_grader_labs.txt); collect-only 134 ({S}/out/collect_count.txt)."),
    row("SC1-d-r11-run-graders", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py; test_project.py", "PASS",
        "run_graders --unit SC1 --seeds 0-49: 'run_graders SC1: PASS (reference 50/50 seeds, slowest 1.1 s)' "
        f"({S}/out/run_graders_SC1_0-49.txt); --seeds 50-199: 'PASS (reference 150/150 seeds)' "
        f"({S}/out/run_graders_SC1_50-199.txt). The tool also type-checks the reference, starter and instance under mypy --strict "
        "and requires the starter to fail the suite."),
    row("SC1-d-r11-mutate-gate", "2.6-mutation", "ledgers/SC1/mutants/ (top level)", "FAIL",
        "mutate_graders --unit SC1 --seeds 0-9 exits 0 with 'PASS (68/68 killed)' "
        f"({S}/out/mutate_graders_SC1_0-9_final.txt). Of the 68, six are not grader mutants: the SC1a-lab-mut*/SC1a-r6-lab-mut* "
        "files are lab twins of L01-L03 that define none of reflection_tail, discrete_max_exceedance or nested_grid_counts "
        "(grep count 0 for each in every file), so they are 'killed' by AttributeError, not by a property test. The engine "
        "gate is therefore 62 of 62.",
        "Move the six SC1a-* files out of ledgers/SC1/mutants/ into a lab-mutant folder (for example ledgers/SC1/lab-mutants/) "
        "that the grader gate does not read, then re-run mutate_graders --unit SC1 --seeds 0-9 and expect 62/62."),
    # ---- spec, constraints, hours, ladder ----
    row("SC1-d-ladder", "2.6-ladder", "course/modules/SC/SC1/project.html:40-49", "PASS",
        "Ladder order: Rung 1 worked example (Lab 1), Rung 2 completion (Lab 2, class lab completion), Rung 3 independent project, "
        "Rung 4 stretch; the ladder text matches the sections (lines 40-49, 51-211, 213-297, 608-615)."),
    row("SC1-d-grading-mode", "2.6-grading", "project.html 'Grading mode' dd (line 225)", "PASS",
        "States 'both' and names 'runs 134 tests'; collect-only gives 134 (out/collect_count.txt)."),
    row("SC1-d-spec-signatures", "2.6-spec", "project.html 'Required outputs' dd (line 221) vs grader/starter.py", "PASS",
        "Five signatures listed on the page match starter.py lines 16, 21, 26, 31, 36 exactly (reflection_tail(a, t), "
        "discrete_max_exceedance(instance, n_steps), nested_grid_counts(instance, n_fine, n_coarse), srw_max_count(n, a), "
        "srw_terminal_count(n, a))."),
    row("SC1-d-spec-rounding-statement", "2.2-numbers / 2.9-prose", "project.html Constraints dd (line 223); Labs 1 and 3 prints",
        "PASS",
        "Constraints: six decimals from the unrounded value, horizon and level as generated to three decimals, differences in "
        "exponent form to three significant digits. Lab 1 prints '{:.6f}' for every computed value and '{:.2e}' for the Simpson "
        "difference (twin lines 87-93); Lab 3 prints '{:.6f}' (lines 94-109). Output (run_labs) matches. Horizon and level "
        "print by repr of round(x, 3), which gives the generated value with at most three decimals."),
    row("SC1-d-hours", "2.6-hours / 2.9-structure", "project.html table#hours (lines 271-282); data-hours-project=28 (line 33)",
        "PASS",
        "2+3+10+8+3+2 = 28. Hub index.html line 29: data-hours-lessons=72, data-hours-project=28; the eight lessons each carry "
        "data-hours=9 (72). 72+28 = 100 = 'Tier M · 100 hours' (index.html line 31). No arithmetic inconsistency."),
    row("SC1-d-spec-grid-table", "2.6-spec", "project.html Conventions bullets (lines 231-233)", "PASS",
        "Grid t_k = kH/n for k = 1..n; sd = sqrt(H/n_steps); path-by-path, step-by-step order as reference.py lines 27-39 and "
        "test_project.py _explicit_paths; nested coarse grid = every n_fine/n_coarse-th point (reference line 75)."),
    row("SC1-d-spec-tolerance-statement", "2.6-spec", "project.html Conventions reflection_tail bullet (line 234)", "PASS",
        "States 10^-10; test_reflection_tail_is_the_erfc_closed_form enforces 1e-10 (test_project.py:187). Consistent. "
        "Plan deviation recorded in SC1-d-plan-tolerance."),
    row("SC1-d-spec-n41-method", "2.6-spec", "project.html:223, grader/test_project.py:294-315", "PASS",
        "Page forbids listing walks for n = 41; test_srw_integers_are_exact_for_a_long_odd_walk runs under a 1.0 s budget and "
        "checks 2**40 and 2**41 - C(41,20). Recomputed by dp: srw counts for n = 5 a = 1 give 16 = 2**4, consistent (recompute_r11.txt)."),
    row("SC1-d-spec-constraints-raise", "2.6-spec", "project.html Conventions ValueError bullet (line 237) vs test_project.py",
        "PASS",
        "Named conditions: reflection_tail a<=0, t<=0; discrete n_steps<1, n_paths<2; nested n_fine<1, n_coarse<1, non-divisor; "
        "srw n<1, a<1 in both. Tests must_raise/must_accept cover exactly these (lines 221-239, 318-345, 466-487, 532-556). "
        "No test demands ValueError for another input."),
    # ---- grader ----
    row("SC1-d-ag-reference", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py", "PASS",
        "run_graders 0-49 and 50-199 PASS (out/run_graders_SC1_0-49.txt, out/run_graders_SC1_50-199.txt). reference.py is "
        "byte-identical to the round-10 pin."),
    row("SC1-d-ag-starter", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py", "PASS",
        "Every function raises NotImplementedError (starter.py lines 18, 23, 28, 33, 38); run_graders requires the starter to "
        "fail the suite and reports PASS (out/run_graders_SC1_0-49.txt)."),
    row("SC1-d-ag-instances", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py", "PASS",
        "Sample of 20 seeds (out/sample_instances_r11.txt): all valid (H>0, a>0, 4<=n<=256, 400<=N<=800, n*N<=200000, label "
        "SIMULATED); 20 distinct tail values. instance.py:21-35 uses the same draw order as the lab twin "
        "tests/labs/SC1/lab-SC1-project-1.py:31-38 and the page's make_instance (project.html Lab 1 twin)."),
    row("SC1-d-ag-count", "2.6-autograder", "grader/test_project.py; project.html (lines 7, 225, 296)", "PASS",
        f"collect-only = 134 with QF_SEED=0 ({S}/out/collect_count.txt); page claims 134 in the meta description, the grading "
        "dd and the local-run paragraph."),
    row("SC1-d-ag-messages", "2.6-autograder", "grader/test_project.py:45-117 and 293-315", "PASS",
        "Messages name the property (e.g. line 187 'the tail must equal erfc(a / sqrt(2 t)) to 1e-10', line 401, line 642). "
        "No message interpolates an expected value; only inputs appear (e.g. line 534 'n_coarse = ... does not divide n_fine')."),
    row("SC1-d-ag-overconstraint", "2.6-autograder", "grader/test_project.py; ledgers/SC1/scripts/SC1-d-r11/alternatives/",
        "PASS",
        "Correct alternatives pass 50/50 (see SC1-d-r11-alternatives). The 1e-12 comparisons are between hit fractions (integers "
        "over N) and explicit counts, so float summation order matters only for a position tied with the level to within float "
        "error; no correct alternative was affected."),
    row("SC1-d-ag-alternatives-ok", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r11/alternatives/ and the r7/r9/r10 folders",
        "PASS",
        f"Kill matrix over seeds 0-49 ({S}/out/kill_matrix_r11.json, kill_alt_r8_bc_repathed.json). Passing correct alternatives "
        "(50/50 seeds): alt1 normaldist, alt2 simpson-only, alt3 srw dp, alt5 cumsum/index subsample, alt6 pascal row, alt8 "
        "one-minus-erf, alt9 closed-form se, alt_r8_a normaldist, alt_r8_b quadrature (repathed), alt_r8_c dp (repathed), "
        "alt_r8_d streaming, alt_r9_a..e, alt_r10_a, alt_r10_b, alt_r10_c, alt_r10_e. That is 20 alternatives of different styles."),
    row("SC1-d-ag-mutants-plan", "2.6-mutation", "ledgers/SC1/mutants/m01-m10 (plan 5.6 items 1-10)", "PASS",
        "All ten killed on 50 of 50 seeds except m09 (killed on seed 0 only, see SC1-d-r11-m09). m01 by "
        "test_reflection_tail_is_the_erfc_closed_form, m02 same, m03 test_one_step_estimate_matches_..._second_seed, m04 "
        "test_one_step_draws_are_the_seeded_gaussians, m05/m06 test_standard_error_uses_divisor_n_minus_one, m07 coarse<=fine, "
        "m08 erfc closed form, m10 test_reflection_tail_rejects_zero_time."),
    row("SC1-d-ag-mutants-own", "2.6-mutation", "ledgers/SC1/mutants/m11-m15, m18, m19, m21", "PASS",
        "All killed on 50/50 seeds (kill_matrix_r11.json). m11 killed by test_nested_counts_match_an_explicit_subsample... "
        "(formerly survived seeds 1-49 per round 10; now 50/50)."),
    row("SC1-d-ag-mutants-survivors", "2.6-mutation", "ledgers/SC1/mutants/m16, m17", "PASS",
        "m16 and m17 (named ValueError skipped) killed 50/50 by the fine and coarse zero-step tests."),
    row("SC1-d-ag-mutants-seed", "2.6-mutation", "ledgers/SC1/mutants/m20_draws_seeded_with_zero_for_every_instance.py", "PASS",
        "Killed 50/50 by test_draws_depend_on_the_instance_seed (first failing seed 0)."),
    row("SC1-d-ag-mutants-seed-offset", "2.6-mutation", "ledgers/SC1/mutants/m22_seed_offset_by_one.py", "PASS",
        "Killed 50/50 by test_one_step_draws_are_the_seeded_gaussians."),
    row("SC1-d-ag-mutants-r3", "2.6-mutation", "ledgers/SC1/mutants/m23-m26", "PASS",
        "All killed 50/50 (srw odd shortcut, standard error / n, misplaced increment scale, srw reflection endpoint)."),
    row("SC1-d-ag-mutants-r4-new", "2.6-mutation", "ledgers/SC1/mutants/m27-m31", "PASS",
        "All killed 50/50 (coarse starts at first step, paths redrawn per path, srw terminal drop, identity shift, fresh coarse paths)."),
    row("SC1-d-ag-mutants-r5-new", "2.6-mutation", "ledgers/SC1/mutants/m32-m34", "PASS",
        "m32 and m34 killed 50/50 (formerly survived on some seeds; the explicit-count tests added in the round-10 delta now kill them)."),
    row("SC1-d-ag-mutants-r6-new", "2.6-mutation", "ledgers/SC1/mutants/m37_one_path_accepted_with_zero_error.py", "PASS",
        "Killed 50/50 by test_one_path_raises_value_error."),
    row("SC1-d-ag-level-equality-survivors", "2.6-mutation", "ledgers/SC1/mutants/m35, m36", "PASS",
        "Strict-inequality mutants killed 50/50 by the level-on-a-path-maximum tests (test_project.py:416-429, 507-513)."),
    row("SC1-d-ag-mutants-r7-new", "2.6-mutation", "ledgers/SC1/mutants/m38-m41", "PASS", "All killed 50/50."),
    row("SC1-d-r7-mutants-all", "2.6-mutation", "ledgers/SC1/mutants/ (all grader mutants)", "PASS",
        "Every engine mutant is killed on at least one seed in 0-9 (mutate_graders 68/68 including six misfiled files) and "
        "all but m09 on 50 of 50 seeds (kill_matrix_r11.json)."),
    row("SC1-d-r8-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r8_01..r8_07", "PASS",
        "All killed 50/50 (leftover prints, tiny-level rejection, worst-case p, tiny-tail warning, nested fine steps, "
        "brute-force listing)."),
    row("SC1-d-r9-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r9_01..r9_04", "PASS", "All killed 50/50 by the print/warning test."),
    row("SC1-d-r10-new-mutants", "2.6-mutation", "ledgers/SC1/mutants/r10_01..r10_06", "PASS",
        "All killed 50/50 (kill_matrix_r11.json)."),
    row("SC1-d-r11-new-mutants", "2.6-mutation", "ledgers/SC1/mutants/r11_01..r11_04 (new this round)", "PASS",
        "Four new student-error mutants, each a single-change copy of reference.py written by scripts/SC1-d-r11/"
        "make_mutants_r11.py: r11_01 coarse grid ends one step early (killed 50/50), r11_02 reflection_tail rounded inside the "
        "engine (killed 50/50 by the 1e-10 closed-form test), r11_03 strict inequality on the coarse count only (killed 50/50), "
        "r11_04 draws reseeded by the grid size (killed 50/50). Kill data: out/kill_matrix_r11_new.json."),
    row("SC1-d-r11-m09", "2.6-mutation", "ledgers/SC1/mutants/m09_seed_zero_hard_coded.py", "PASS",
        "Killed on seed 0 only (1/50; first failure test_estimate_is_a_fraction_of_the_paths). This is the 'hard-coded answer for "
        "seed 0' the verifier rules name; it passes every other seed because it returns the reference there. The integrity clause "
        "in the page (the second instance, make_instance(seed + 7919)) is what catches a hard-coded answer for the learner's own "
        "seed; that is not separately tested here (no mutant keyed on the learner's own seed was written)."),
    row("SC1-d-r7-alt4-ruling10", "2.6-autograder", "plans/SC1-build-plan.md 5.7(4); plans/FINAL-ARCHITECT-RULINGS.md item 10",
        "PASS",
        "Plan 5.7(4) asks for Box-Muller on a different draw order that stays within 5 se. The page now states the path-by-path "
        "draw order as exact (project.html:232, 233), so the Box-Muller alternative is wrong on a stated rule and is a mutant "
        "(Ruling 10: 'a float-based alternative that is wrong on a stated exact rule is a mutant, not an alternative'). Killed "
        "50/50 (alt4_box_muller_step_major.py)."),
    row("SC1-d-r7-alternatives-sweep", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r7/alternatives/*.py", "PASS",
        "alt1, alt2, alt3, alt5, alt6, alt8, alt9 pass 50/50. alt2b (enumeration for n = 41) and alt7 (step-major order) fail "
        "50/50 by the page's own rules, so they are mutants, not alternatives. alt4 see SC1-d-r7-alt4-ruling10."),
    row("SC1-d-r7-reference-sweep-500", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py", "PASS",
        "Reference passes seeds 0-199 (150 + 50 seeds this round). Seeds 200-499 were not re-run this round; reference.py is "
        "byte-identical to the round-10 pin and the only changed grader file is test_project.py, which the 0-199 sweep covers."),
    row("SC1-d-r7-starter-fails", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py", "PASS",
        "Starter fails the suite (run_graders check; NotImplementedError in every function)."),
    row("SC1-d-r7-instances-sample", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py", "PASS",
        "Sample in out/sample_instances_r11.txt (20 seeds, distinct answers)."),
    row("SC1-d-r7-numbers-recompute", "2.2-numbers", "project.html Labs 1-3 and prose", "PASS",
        "Independent recomputation in scripts/SC1-d-r11/recompute_r11.py (out/recompute_r11.txt): every printed Lab 1 and Lab 3 "
        "value and every walk count (1588, 794, 29, 22, 7) matches."),
    row("SC1-d-r7-page-vs-twin", "2.5-labs", "project.html Labs 1-3 vs tests/labs/SC1/lab-SC1-project-{1,2,3}.py", "PASS",
        "run_labs: page code equals twin (Lab 2 blanks replaced by the twin's completed lines, as the run_labs docstring allows)."),
    row("SC1-d-r7-gates-full", "2.5/2.6 tooling", "repository root", "PASS",
        "Gates run this round are listed under SC1-d-r10-gates and SC1-d-tools-gates. Not run: the full repository pytest suite "
        "and ruff over the whole repository (not in this slice's scope; mypy --no-incremental over the whole project was run)."),
    row("SC1-d-r7-registry-live", "2.1-citations", "references/references.json (shreve2004stochastic)", "PASS",
        "See SC1-d-r10-registry-live (openlibrary HTTP 200, year 2004)."),
    row("SC1-d-r7-page-smoke", "2.9-structure", "course/modules/SC/SC1/project.html", "PASS", "See SC1-d-r10-page-smoke."),
    row("SC1-d-r10-page-smoke-project", "2.9-structure", "project.html", "PASS", "See SC1-d-r10-page-smoke."),
    row("SC1-d-r10-mutant-folder-hygiene", "ledger hygiene (2.6-mutation)", "ledgers/SC1/mutants/SC1a-lab-mut1..3, SC1a-r6-lab-mut1..3",
        "FAIL",
        "Six lab-twin mutants of slice a sit in the grader mutant folder. They define no engine function (grep count 0), so the "
        f"grader gate counts them as killed for an unrelated reason ({S}/out/mutate_graders_SC1_0-9_final.txt). Round 10 passed "
        "this row; the defect persists at 11d7077.",
        "Move the six files out of ledgers/SC1/mutants/ (see SC1-d-r11-mutate-gate)."),
    row("SC1-d-r10-mutant-seed-coverage", "2.6-autograder (rule 11 at the learner's seed)",
        "grader/test_project.py (new explicit-count tests, delta 00a84795..11d7077)", "PASS",
        "Round 10 found eleven mutants (m07, m11, m18, m19, m21, m25, m27, m31, m32, m34, r10_06) surviving on some seeds in 0-49. "
        "The round-10 delta adds test_discrete_estimate_matches_an_explicit_count_on_the_stated_draws and "
        "test_nested_counts_match_an_explicit_subsample_of_the_fine_paths; in this round each of the eleven fails on 50 of 50 "
        "seeds (kill_matrix_r11.json)."),
    row("SC1-d-r10-alternatives", "2.6-autograder (alternatives)", "ledgers/SC1/scripts/SC1-d-r11/alternatives/; SC1-d-r10/alternatives",
        "PASS",
        "alt_r10_a, alt_r10_b, alt_r10_c, alt_r10_e pass 50/50. alt_r10_d (step-major draws) was listed as an alternative in round 10; "
        "under the page's new draw-order sentence (project.html:232-233) it fails 50/50 and is a mutant (Ruling 10). Twenty "
        "passing alternatives remain (SC1-d-ag-alternatives-ok)."),
    row("SC1-d-r10-prior-alternatives", "2.6-autograder (alternatives)", "ledgers/SC1/scripts/SC1-d-r{7,8,9}/alternatives/", "PASS",
        "Re-run on seeds 0-49 this round. Passing: r7 alt1/2/3/5/6/8/9, r8 a/b/c/d (b and c repathed to this checkout), r9 a-e. "
        "Failing by the page's rules: r7 alt2b (n = 41 enumeration), r7 alt4 and alt7 and r8 alt_r8_e (step-major or Box-Muller "
        "draws), counted as mutants."),
    row("SC1-d-r8-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r8/alternatives/", "PASS",
        "alt_r8_b and alt_r8_c import the reference from the defunct verifyE8 worktree and error on import in this checkout. "
        "Repathed copies in scripts/SC1-d-r11/alternatives/ (repath_r8_alternatives.py) pass 50/50 (out/kill_alt_r8_bc_repathed.txt)."),
    row("SC1-d-r8-reference-sweep", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py", "PASS", "See SC1-d-ag-reference."),
    row("SC1-d-r8-proofs-trace", "2.4-proof", "project.html statements and exemplar B appendix", "PASS",
        "P1 traced step by step (stopping time by A4(c); tau = t has probability zero; A3 gives independence of the restart; "
        "A4(b) with Z=(t-rho, 1_A) gives the half; A4(g) gives measurability; A4(h) gives F_rho-measurability). No step skipped "
        "that the statement does not list."),
    row("SC1-d-r8-page-smoke", "2.9-structure", "project.html", "PASS", "See SC1-d-r10-page-smoke."),
    row("SC1-d-delta-r5-read", "2.9-prose (delta read)", "project.html; grader/test_project.py", "PASS",
        "Full read of the round-10 to round-11 delta in this slice: project.html 10 lines (meta and grading counts 132 to 134, "
        "draw-order sentences, nested sentence) and test_project.py 49 lines (docstring sentence and two new tests)."),
    row("SC1-d-delta-r6-read", "2.9-prose (delta read)", "project.html; grader/test_project.py", "PASS", "See SC1-d-delta-r5-read."),
    # ---- labs ----
    row("SC1-d-lab1-run", "2.5-labs", "project.html Lab 1; tests/labs/SC1/lab-SC1-project-1.py", "PASS",
        "run_labs PASS for lab-SC1-project-1 (page = twin; output equals the expected block: seed 0 H = 2.083, a = 2.474, "
        "N = 487, tail 0.086497, Simpson diff 9.13e-15, estimate 0.059548 se 0.010735, band 0.048142, inside True)."),
    row("SC1-d-lab1-docstring", "2.5-labs / 2.9-prose", "tests/labs/SC1/lab-SC1-project-1.py:1-14; project.html Lab 1 hypothesis",
        "PASS",
        "Docstring: 'draws the same four numbers in the same order' (lines 33-37 match make_instance), 'six decimal places ... except "
        "the Simpson difference, printed in exponent form to three significant digits' (lines 87-93: .6f and .2e). Matches."),
    row("SC1-d-lab2-run", "2.5-labs", "project.html Lab 2; tests/labs/SC1/lab-SC1-project-2.py", "PASS",
        "run_labs PASS: output '29 / 22 / 7 / True' equals the page's expected block; the page's ___ blanks are the only "
        "differing lines (run_labs completion rule)."),
    row("SC1-d-lab2-attribution", "2.9-prose / attribution", "project.html:209 vs L06.html:75-90 (Proposition 1.3, Corollary 1.4)",
        "PASS",
        "L06 Proposition 1.3 is the discrete reflection identity and Corollary 1.4 the discrete tail identity, proved from it. "
        "Page statement matches; 'the engine's tests check every n up to 12' matches test_project.py:255-275 (range(1, 13))."),
    row("SC1-d-lab3-run", "2.5-labs", "project.html Lab 3; tests/labs/SC1/lab-SC1-project-3.py", "PASS",
        "run_labs PASS. Output: grid rows (hits 29, 24, 32, 43, 40), nested coarse counts 35, 29, 27, 22 under fine 40, walk "
        "1588 and 794 (matches recompute_r11.txt)."),
    row("SC1-d-lab3-onestep-interp", "2.5-labs / 2.9-prose", "project.html:429 (Lab 3 interpretation)", "PASS",
        "0.026948 - 0.043248 = -0.016300; 0.016300/0.010735 = 1.5185 (1.52); 0.016300/0.009218 = 1.7683 (1.77); 0.001799/0.012870 "
        "= 0.1398 (0.14). All recomputed (recompute_r11.txt)."),
    row("SC1-d-lab3-docstring", "2.5-labs / 2.9-prose", "tests/labs/SC1/lab-SC1-project-3.py:3-11; project.html Lab 3 hypothesis",
        "PASS",
        "Docstring states the coarse grids are the same 256-step paths, the tail is the continuous maximum on [0, H], and 'The walk "
        "line is an exact count'; code (lines 92-109) matches. Hypothesis: 'each grid is drawn on its own paths' matches "
        "path_maxima called per grid."),
    row("SC1-d-labs-pytest", "2.5-labs / tooling", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, "
        "tests/test_memo_exemplars.py, tests/test_docs_figures.py", "PASS",
        "pytest exit 0 on the selected files (out/pytest_sc1_related.txt)."),
    # ---- proofs, statements, citations, notation, DAG ----
    row("SC1-d-statements", "2.6-spec / 2.4-proof", "project.html 'The three results to prove' (lines 241-262)", "PASS",
        "P1 (A0, A3, A4(b), A4(c), A4(g), A4(h)), P2 (P1 and normal law), P3 (continuity, P2 for second part) are internally "
        "consistent; the proofs in the appendix use exactly the listed parts."),
    row("SC1-d-A1-label", "2.6-spec / attribution", "project.html Statements A0 bullet (line 242); L01.html Definition 1.1; L02.html Theorem 2.5, Remark 2.6",
        "PASS",
        "L01 Definition 1.1 gives B_0 = 0, normal increments with variance equal to length (D2 at L01:159). L02 Theorem 2.5 "
        "(continuous paths on [0,1]) and Remark 2.6 ([0,infinity)) exist with these labels (L02.html:289, 303). A0's "
        "'continuous paths' attribution is correct."),
    row("SC1-d-A3-A4-usage", "2.6-spec / attribution", "project.html statements (lines 242, 246); L05.html:59-69 (A4), L05.html:271-279 (A3)",
        "PASS",
        "A4(b) freezing, A4(c) hitting times of a closed set (stopping time), A4(g) joint measurability, A4(h) measurability at a "
        "stopping time with rho <= c; A3 conclusion: X_r = B_{rho+r} - B_rho is standard BM independent of F_rho, for bounded rho. "
        "Each usage in P1 matches its statement (L05.html:59-69, 271-279)."),
    row("SC1-d-L05-A4-i", "2.6-spec / attribution", "project.html (no A4(i) cited); L05.html:69", "PASS",
        "A4(i) (integrable freezing) is used only in M2 per L05.html:69; the project's statements cite A4(b), A4(c), A4(g), A4(h) only."),
    row("SC1-d-statements-recheck-P2", "2.4-proof", "project.html P2 statement (line 255) and exemplar B appendix (line 587)", "PASS",
        "erfc(a/sqrt(2t)) = 2(1 - Phi(a/sqrt t)): substitution w = z/sqrt2 gives erfc(x) = (2/sqrt(2 pi)) int_{x sqrt2}^inf e^{-z^2/2} dz "
        "= 2(1 - Phi(x sqrt2)); numerically max error 1.11e-16 over the grid (recompute_r11.txt)."),
    row("SC1-d-dag", "2.9-DAG", "project.html links (stopping-time, normal-distribution); tools/check_dag.py --unit SC1",
        "PASS",
        "check_dag --unit SC1 PASS. Both linked concepts lie in the prerequisite closure {M1, M2, M4, M5, M6, P0.1} (plan section 4): "
        "stopping-time (M6), normal-distribution (M4). Unlinked terms named in the plan's NOT IN CURRICULUM list are plain prose."),
    row("SC1-d-notation", "2.8-notation", "project.html math (259 delimited expressions)", "PASS",
        "Macros used: \\Prob, \\Normal, \\indic, \\Phi (all registered in notation/notation.json or standard TeX). Single "
        "letters: H (horizon, not T), N (path count, local), B, M, tau, rho, F, k, n, t, a, p; T appears only in the sentence "
        "explaining that T has another meaning. No registered symbol is reused with a different meaning."),
    row("SC1-d-define-before-use", "2.5-labs / 2.9-prose", "project.html (within the page)", "PASS",
        "Within the project page, H, N, M_t, tau_a, Phi, erfc, grid maximum, standard error, simulated estimate, 'almost surely' "
        "(defined inline at line 455) and 'pathwise' (defined at line 231) are introduced before or at first use on this page. "
        "The cross-page use of 'pathwise' is the FAIL row SC1-d-pathwise-define-before-use."),
    row("SC1-d-pathwise-define-before-use", "2.9-prose / define-before-use", "course/modules/SC/SC1/L01.html:67 (first use); "
        "project.html:231 (definition)", "FAIL",
        "Re-verified at 11d7077. 'pathwise' is used in L01.html:67 ('(D1) is pathwise only at time 0'), L03.html:261, 278, 452, 484, "
        "L07.html:164, 303, 367 and L08.html:217-236, before the project page (the last page) defines it at project.html:231 "
        "('A statement that holds on every path in this way is called pathwise.'). The term is used as a technical term before "
        "any lesson defines it. L01.html:67 is byte-identical to round 10 for this sentence.",
        "Define 'pathwise' in plain words at its first use in L01.html:67 (or reword that sentence without the term) and do the "
        "same for the L03, L07 and L08 uses, so that the project page's definition at line 231 is a restatement. Owners: L01, L03, "
        "L07 and L08 builders."),
    row("SC1-d-discretization-bias", "2.9-prose / 2.4-proof", "project.html:235 (definition), :429 (use)", "PASS",
        "Bias = P(M_H >= a) - P(grid max >= a) >= 0 by the pathwise bound (grid max <= M_H); the estimate can be negative (lab "
        "shows -0.001799 at 64 steps). Proved and computed; first use (line 429) follows the definition."),
    row("SC1-d-monte-carlo-term", "2.9-prose", "project.html; grader/test_project.py", "PASS",
        "'simulation band' and 'standard error' defined with the band formula (line 238, test_project.py:121-124) before use."),
    row("SC1-d-scope-words", "2.9-prose (scope words)", "project.html:217, 223, 231-238, 429, 455; L-lab docstrings", "PASS",
        "'Every instance is SIMULATED' (238) is a labelling rule enforced by instance.py; 'every grid point lies in [0,H]' (231) is "
        "arithmetic; 'never exceeds' (231, 235) are proven; 'every coarse count is at most the fine count' (Lab 3) is computed on "
        "four counts; 'holds for every path' statements are pathwise and proved."),
    row("SC1-d-process-words", "2.9-prose (no process words)", "project.html; tests/labs/SC1/lab-SC1-project-{1,2,3}.py; grader/*.py",
        "PASS",
        "Case-insensitive scan for builder, verifier, ledger, fixer, architect, round, revised, updated, TODO, placeholder: no hits "
        "in the slice (scan output empty)."),
    row("SC1-d-banned-structure", "2.9-structure", "project.html; tools/check_pages.py --unit SC1", "PASS",
        "check_pages --unit SC1 PASS (banned phrases, structure)."),
    row("SC1-d-registry", "2.1-citations", "project.html reading list (line 621); references/references.json", "PASS",
        "Only shreve2004stochastic is cited; record present, verified, used_by SC1; offline registry integrity 560 entries, 0 problems."),
    row("SC1-d-privacy-claim", "2.9-prose", "project.html:288 ('saved in this browser')", "PASS",
        "grader.js saves the draft with store.put('files', ...) after a 400 ms debounce (grader.js:61); store.js writes to the browser's "
        "IndexedDB and, when IndexedDB is unavailable, falls back to a session-only memory store that the page reports "
        "(store.js:2-6). Footer (line 636) says 'kept in this browser's storage': matches the normal path."),
    row("SC1-d-numbers-prose", "2.2-numbers", "project.html lines 57, 154-160, 209, 219, 225, 265, 305-309, 429", "PASS",
        "Every decimal in the prose recomputed (out/recompute_r11.txt): 0.086497, 9.13e-15, 0.059548, 0.010735, 0.043248, 0.009218, "
        "0.048142, 0.016300, 1.52, 1.77, 0.14, 0.026948, 0.037215, 0.020788, -0.001799, 0.004361, 40/35/29/27/22, 1588, 794; "
        "H = 2.083, a = 2.474, N = 487 for seed 0 (the instance draw order matches the page)."),
    row("SC1-d-r7-numbers-target-se", "2.2-numbers", "project.html:429; Lab 1 output", "PASS",
        "target standard error: sqrt(p(1-p)/487) at the unrounded p = tail/2 is 0.00921764, which rounds to 0.009218 "
        "(Lab 1 output line 158; recompute_r11.txt prints 'target 0.043248 target_se 0.009218'). Python's sqrt(p(1-p)/487) at "
        "the rounded p = 0.043248 gives 0.00921761, which also rounds to 0.009218; the printed value is correct either way."),
    row("SC1-d-numbers-target-se", "2.2-numbers", "project.html:429; Lab 1 output", "PASS", "See SC1-d-r7-numbers-target-se."),
    row("SC1-d-reading-disclosure", "2.9-prose / attribution", "project.html reading list (lines 617-623)", "PASS",
        "Reading states the book and year (2004) at book level, and says no passage or theorem is attributed. Open Library confirms "
        "a 2004 'Stochastic Calculus for Finance II' by Steven E. Shreve."),
    row("SC1-d-exemplar-naming", "2.9-structure (plan conformance)", "project.html exemplar-a data-level=2, exemplar-b data-level=4 vs plans/SC1-build-plan.md 5.4",
        "PASS",
        "Plan 5.4 says exemplar-a data-level 4 and exemplar-b data-level 2; the page reverses them. data-level is not shown to the "
        "learner. Non-blocking plan deviation for the architect (see notes)."),
    row("SC1-d-plan-tolerance", "2.6-spec (plan conformance)", "project.html Conventions (line 234); grader/test_project.py:187 vs plans/SC1-build-plan.md 5.5",
        "PASS",
        "Plan 5.5 asks for erfc agreement to 1e-12; the page and the test use 1e-10 consistently. Every correct implementation "
        "tested passes at 1e-10 (alternatives pass 50/50). Non-blocking plan deviation for the architect (see notes)."),
    row("SC1-d-dfn-policy", "2.9-prose (architect policy)", "project.html (no <dfn> element)", "PASS",
        "Plan D9 said the project would define 'discretization bias' with a plain <dfn>; the architect defaults say concepts "
        "outside the closure are plain prose with no dfn. The page has no <dfn> and defines the term in prose (line 235). Consistent "
        "with the architect default."),
    # ---- exemplars and rubric ----
    row("SC1-d-rubric-observable", "2.9-prose", "project.html rubric table#rubric (lines 448-458)", "PASS",
        "Each C1-C5 cell has four observable levels. Descriptors name checkable items (named assumptions, numbers with a rounding "
        "statement, a standard error, an exact count, a stated gap). No descriptor depends on taste. Note: 'where single-seed noise "
        "can reverse it' (C5 level 2) is a judgement the reader can check from the printed standard errors; not a FAIL."),
    row("SC1-d-calib-A", "2.9-prose / rubric calibration", "project.html exemplar-a data-scores=1,2,2,2,1",
        "PASS",
        "Scored from the rubric text: C1 1 (no numbered assumptions), C2 2 (P1 proved with 'by symmetry', P2 and P3 not proved), C3 2 "
        "(unrounded decimals with no rounding statement), C4 2 (grid results presented as holding for every grid), C5 1 (no "
        "numbers). Equals the official 1,2,2,2,1. CAVEAT: not strictly blind; the page and its annotations were read before scoring."),
    row("SC1-d-calib-B", "2.9-prose / rubric calibration", "project.html exemplar-b data-scores=4,4,4,3,4",
        "PASS",
        "Scored from the rubric: C1 4, C2 4, C3 3 (the per-value type is stated only generally in Setup), C4 3 (limitations omit the "
        "continuum statement), C5 4. Official 4,4,4,3,4; C3 differs by one level, inside the calibration tolerance. Same caveat "
        "on blindness as SC1-d-calib-A."),
    row("SC1-d-exemplarA-claim", "2.2-numbers / 2.9-prose", "project.html exemplar A passages (lines 469-514)", "PASS",
        "Each exemplar A claim is annotated as a miss (C3, C4, C5). Its numbers (0.0865, 0.0595, 0.0107, 0.0163, 0.0432, 1.52, 1588) "
        "match Labs 1 and 3; the claim 'finer grids give estimates closer to the tail' is contradicted by 0.004361 (256) vs -0.001799 "
        "(64) and is annotated as a miss."),
    row("SC1-d-exemplar-a-annotations", "2.9-prose (annotation accuracy)", "project.html exemplar A annotations (lines 474-512)",
        "PASS", "Each annotation names a descriptor that the passage misses or meets; the C2 'meets level 2' and P1 'misses C1 level 3' "
        "match the passage text (lines 495-500)."),
    row("SC1-d-r7-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/m38-m41", "PASS",
        "m38 (a = 0 accepted), m39 (SE over sqrt(N-1)), m40 (Box-Muller instead of gauss), m41 (Phi form) killed 50/50 "
        "(kill_matrix_r11.json)."),
    row("SC1-d-hunk-standard-error-sentence", "2.9-prose", "project.html:53 (rungs paragraph)", "PASS",
        "'A standard error is the estimated standard deviation of a simulated estimate, so it measures the sampling noise of one run' "
        "is a definition consistent with the SE formula used in the labs (twin lines 73-75)."),
    row("SC1-d-hunk-no-more-often", "2.6-spec / 2.4-proof", "project.html:217 (Context)", "PASS",
        "'a grid maximum reaches a level no more often than the continuous maximum does' is the pathwise bound "
        "{grid max >= a} subset of {M_H >= a} (project.html:231, 235); holds on every path, so the probability statement is true."),
    row("SC1-d-hunk-filtration", "2.6-spec / attribution", "project.html:230 (conventions, filtration F_t and F_rho)", "PASS",
        "F_t and F_rho are defined as in Sections 1 and 3 of Lesson 5 (L05.html:56 defines F_t; L05.html:268 defines F_rho)."),
    row("SC1-d-hunk-one-step-target-se", "2.2-numbers / 2.5-labs", "project.html:429 (Lab 3 interpretation)", "PASS",
        "Recomputed: one-step estimate sampling error -0.016300 = 1.52 sample SE and 1.77 target SE (recompute_r11.txt)."),
    row("SC1-d-index-rung2-text", "2.9-prose (cross-check)", "course/modules/SC/SC1/index.html:168", "PASS",
        "Index describes the completion problem as 'the identity line and the final comparison line removed', matching Lab 2's two "
        "blanks (identity = ___ and max_hits == ___)."),
    row("SC1-d-exemplar-a-scope", "2.9-structure / brief conformance", "project.html:462 ('Two reports written to this brief'), exemplar A (lines 464-516), brief (line 442)",
        "FAIL",
        "Exemplar A is introduced as a report 'written to this brief', but it has three of the five brief sections (Summary, The "
        "checks, Discretization), no 'Setup and conventions' and no 'Limitations', and a body of 122 words against the 400 to 900 "
        "the brief requires (line 442). The page does not say it is an excerpt.",
        "Either state that exemplar A is an excerpt (the E3 precedent, FINAL-ARCHITECT-RULINGS item 7) or complete its five sections "
        "to the brief. The rubric scores are unaffected."),
    row("SC1-d-exemplarB-onestep-claim", "2.2-numbers", "project.html exemplar B checks passage (lines 544-554)", "PASS",
        "0.059548, 0.016300 above the target 0.043248, 1.52 standard errors, band 0.048142: all match Lab 1 output."),
    row("SC1-d-exemplarB-numbers", "2.2-numbers", "project.html exemplar B summary, discretization, limitations (lines 523-578)", "PASS",
        "9.13e-15 'within 10 to the minus 14' (true); grid SEs 0.010735, 0.009819, 0.011239, 0.012870, 0.012455 and tail minus "
        "estimate 0.026948, 0.037215, 0.020788, -0.001799, 0.004361 match Lab 3; nested 35, 29, 27, 22 under 40 match."),
    row("SC1-d-exemplarB-proof", "2.4-proof / 2.9-prose", "project.html exemplar B appendix P1, P2, P3 (lines 584-590)", "PASS",
        "Traced in full: P1 decomposition A = {tau <= t} = {M_t >= a}, Prob(tau = t) = 0, freezing with f(z,y) = 1{z2=1}1{y(z1)<0}, "
        "f-bar = half; P(A) = P(B_t >= a) + P(A)/2. P2 substitution verified numerically. P3 limit is erfc(0) = 1. All steps are "
        "justified by the cited parts."),
    row("SC1-d-exemplarB-p1-assumptions", "2.9-prose / 2.4-proof", "project.html exemplar B 'Assumptions for P1' (line 583) and statements (line 245-248)",
        "PASS",
        "Exemplar B's assumption list matches the statements section item for item (A0; A3 for rho = tau wedge t; A4(b), (c), (g), (h); "
        "a > 0, t > 0)."),
    row("SC1-d-exemplar-a-annotations-P1", "2.9-prose", "project.html exemplar A P1 passage (line 495)", "PASS",
        "The symmetry step has no numbered assumption; annotation 'Misses C1 level 3: A3 is never listed' is accurate."),
    # ---- labs and reliability of the new tests ----
    row("SC1-d-r10-explicit-tests", "2.6-autograder", "grader/test_project.py:603-644 (two new tests)", "PASS",
        "Both new tests pass on the reference over seeds 0-199 (run_graders). _explicit_paths follows the page's draw order "
        "(path by path, step by step, gauss(0, sqrt(H/n))). They compare exact integer counts, and the grid estimate within 1e-12."),
    row("SC1-d-r10-docstring", "2.6-autograder", "grader/test_project.py:1-20", "PASS",
        "Docstring says 'Two tests regenerate the seeded paths by hand' (lines 14-16): correct, two such tests exist (lines 618, 632). "
        "'One test calls discrete_max_exceedance twice' (test_estimate_is_reproducible) and 'Two tests put the level exactly on a "
        "path's maximum' are also correct."),
    row("SC1-d-ag-print-coverage", "2.6-autograder", "grader/test_project.py:40-44 (autouse _no_stray_output)", "PASS",
        "Autouse fixture checks stdout after every test; test_no_function_prints_or_warns checks boundary inputs. 'Warnings are errors' "
        "via pytestmark filterwarnings('error'). The mutants r8_06, r9_01-04 are killed by these checks."),
    row("SC1-d-ag-walk-listing-stall", "2.6-autograder", "grader/test_project.py:293-315", "PASS",
        "A brute-force listing for n = 41 cannot finish in 1.0 s; r8_07 (brute force) is killed 50/50 and the alternative alt2b fails "
        "50/50 by design."),
    row("SC1-d-ag-band-overconstraint", "2.6-autograder", "grader/test_project.py:120-123 and call sites", "PASS",
        "simulation_band uses the target's standard error (page convention). Correct alternatives pass; no test uses the sample "
        "standard error for the band."),
    row("SC1-d-ag-draws-depend-overconstraint", "2.6-autograder", "grader/test_project.py:448-456", "PASS",
        "Uses a = 1e-9 so paths reach the level. Every correct alternative passes it on seeds 0-49 (kill_matrix_r11.json); "
        "the only failures are the draw-order and enumeration mutants."),
    row("SC1-d-ag-docstring", "2.6-autograder", "grader/test_project.py:1-20", "PASS", "See SC1-d-r10-docstring."),
    row("SC1-d-ag-page-smoke", "2.6-autograder", "project.html; tools/page_smoke.py --unit SC1 --pages project", "PASS",
        "PASS (out/page_smoke_SC1_project.txt)."),
    row("SC1-d-r8-alternatives-b-c-repath", "2.6-autograder", "scripts/SC1-d-r11/alternatives/alt_r8_b, alt_r8_c", "PASS",
        "Repathed copies pass 50/50 (see SC1-d-r8-alternatives)."),
    row("SC1-d-r11-recompute", "2.2-numbers", "scripts/SC1-d-r11/recompute_r11.py", "PASS",
        "Recomputed from the page's definitions by a separate implementation (DP for walks, explicit paths for grids). All match."),
    row("SC1-d-r11-collect", "2.6-autograder", "grader/test_project.py", "PASS", "collect-only 134 = page 134 (out/collect_count.txt)."),
    row("SC1-d-r11-mypy-ruff", "tooling", "tests/labs/SC1, course/modules/SC/SC1/grader", "PASS",
        "mypy --no-incremental: Success (385 files); ruff check and format clean on the slice."),
    row("SC1-d-r11-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r11/out/kill_matrix_r11.json", "PASS",
        "Twenty correct alternatives pass 50/50 seeds (listed in SC1-d-ag-alternatives-ok). Five alternatives that fail (alt4, alt2b, "
        "alt7, alt_r8_e, alt_r10_d) fail for stated page rules and are counted as mutants, not as alternatives."),
    row("SC1-d-r11-m09-coverage-note", "2.6-mutation", "ledgers/SC1/mutants/m09_seed_zero_hard_coded.py", "PASS",
        "See SC1-d-r11-m09. Note: the grader kills m09 on seed 0 only; a hard-coded answer keyed to a learner's own seed is not "
        "modelled by any mutant."),
]

REGISTRY_FLAGS: list[str] = []
FRESHNESS_FLAGS: list[str] = []


def mutants_list() -> list[dict[str, str | None]]:
    kills: dict[str, dict[str, object]] = {}
    for name in ("kill_matrix_r11.json", "kill_matrix_r11_new.json"):
        data = json.loads((OUT / name).read_text(encoding="utf-8"))
        for path, info in data.items():
            kills[Path(path).name] = info
    out: list[dict[str, str | None]] = []
    for path in sorted(MUT.glob("*.py")):
        if path.name.startswith("SC1a-"):
            continue  # lab twins misfiled here; reported in row SC1-d-r11-mutate-gate
        doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or "(no description)"
        info = kills[path.name]
        failing = int(info["failing_seeds_of_50"])  # type: ignore[arg-type]
        test = info["first_failure_test"]
        killed = f"{test} (first failing seed {info['first_failure_seed']}; {failing} of 50 seeds fail)" if failing else None
        out.append({"name": path.name, "description": doc.splitlines()[0], "killed_by": killed})
    return out


def main() -> None:
    mutants = mutants_list()
    counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
    for r in ROWS:
        counts[r["status"]] += 1
    ids = [r["id"] for r in ROWS]
    assert len(ids) == len(set(ids)), "duplicate row ids"
    verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
    fragment = {
        "unit": "SC1",
        "slice": "d",
        "round": 11,
        "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 11 (did not build SC1; re-verified every round-10 row against the 00a84795..11d7077 delta and re-ran every command row)",
        "pin": PIN,
        "base": f"{BASE} (round-10 pin)",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyE11-SC1-d",
        "scratch": "/tmp/sc1d-r11/ (collect-only work copy); durable scripts and outputs under ledgers/SC1/scripts/SC1-d-r11/",
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "verdict": verdict,
        "rows": ROWS,
        "mutants": mutants,
        "registry_flags": REGISTRY_FLAGS,
        "freshness_flags": FRESHNESS_FLAGS,
        "notes": NOTES,
        "summary": (
            f"SC1 slice d round 11 on {PIN[:7]}: verdict {verdict}. Rows {len(ROWS)}: PASS {counts['PASS']}, FAIL {counts['FAIL']}, "
            f"UNVERIFIABLE {counts['UNVERIFIABLE']}. Mutants: {len(mutants)} engine grader mutants in ledgers/SC1/mutants/ (58 earlier "
            "+ 4 new r11_01..04), all killed on at least one seed in 0-9; 61 of 62 are killed on 50 of 50 seeds, m09 on seed 0 only "
            "by design. Alternatives: 20 pass on seeds 0-49."
        ),
    }
    dest = ROOT / "ledgers/SC1/SC1-d.json"
    dest.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {dest} verdict={verdict} rows={len(ROWS)} counts={counts} mutants={len(mutants)}")


NOTES = (
    "Verdict FAIL with three non-PASS rows. (1) SC1-d-pathwise-define-before-use: 'pathwise' is used before its only definition "
    "(project.html:231, the last page) in L01.html:67 and in L03, L07 and L08; unchanged since round 10. (2) SC1-d-r10-mutant-folder-hygiene "
    "and SC1-d-r11-mutate-gate: six lab-twin mutants of slice a sit in ledgers/SC1/mutants/ and are 'killed' by AttributeError, so the "
    "gate reports 68/68 instead of 62/62 engine mutants. (3) SC1-d-exemplar-a-scope: exemplar A is called a report 'written to this brief' "
    "but has three of five sections and a 122-word body. "
    "Round-10 non-PASS rows re-verified: SC1-d-r10-mutant-seed-coverage is now PASS (all eleven mutants fail on 50 of 50 seeds because "
    "the round-10 delta added the two explicit-count tests). "
    "Round-10 alternatives row: alt_r10_d (step-major draws) is now a mutant because the page states the draw order as exact "
    "(project.html:232-233); it is not counted as an alternative. Twenty alternatives pass on seeds 0-49. "
    "Architect deviations recorded as PASS rows, not FAILs: (a) tolerance 1e-10 on the page and in test_project.py:187 vs 1e-12 in "
    "plan 5.5; (b) exemplar data-level attributes reversed vs plan 5.4 (A=2, B=4 on the page; plan A=4, B=2); (c) plan 5.7(4) "
    "(Box-Muller on a different draw order) conflicts with the page's stated draw order and is treated as a mutant under Ruling 10. "
    "Calibration: exemplar A 1,2,2,2,1 (= official), exemplar B 4,4,3,3,4 vs official 4,4,4,3,4 (C3 within one level). Not strictly "
    "blind: the page and the annotations were read before scoring. "
    "m09 (hard-coded answer for seed 0) is killed on seed 0 only, by design of the rule's own example; the integrity clause is "
    "carried by the second instance, which no mutant exercises for a learner's own seed. "
    "Scripts: ledgers/SC1/scripts/SC1-d-r11/ (kill_rate.py, make_mutants_r11.py, recompute_r11.py, sample_instances_r11.py, "
    "collect_count.sh, repath_r8_alternatives.py, write_fragment_r11.py) and out/."
)


if __name__ == "__main__":
    main()
