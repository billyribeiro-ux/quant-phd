"""Build ledgers/FC2/FC2-d.json for verifier round 17 (FC2 slice d, pin aa659725). Run from the checkout root."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/FC2/scripts/FC2-d-r17/out/"
PREV = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-FC2-d.round16.json").read_text(encoding="utf-8"))
MUT_OUT = (ROOT / S / "mutate_graders_FC2_0-49_r17.out").read_text(encoding="utf-8").splitlines()

CARRY16 = "Carried from round 16 (grader/instance.py byte-identical since e896b7a4):"
CARRY16_LABS = "Carried from round 16 (tests/labs/FC2/lab-FC2-L04-1.py and lab-FC2-L06-1.py byte-identical since e896b7a4):"
CARRY16_EQ = "Carried from round 16 (ledgers/FC2/equivalent/README.md and r15_c, r15_d byte-identical since e896b7a4):"

# id -> (status, evidence, fix)  for every round-16 row id; fix only for non-PASS rows
R = {
    "fc2d-gate-check-projects": ("PASS", f"tools/check_projects.py --unit FC2 -> 'check_projects FC2: PASS', exit 0 ({S}check_projects.out).", ""),
    "fc2d-gate-check-pages": ("PASS", f"tools/check_pages.py --unit FC2 -> 'check_pages FC2: PASS', exit 0 ({S}check_pages.out).", ""),
    "fc2d-gate-check-dag": ("PASS", f"tools/check_dag.py --unit FC2 -> 'check_dag FC2: PASS', exit 0 ({S}check_dag.out).", ""),
    "fc2d-gate-run-labs": ("PASS", f"tools/run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)', exit 0 ({S}run_labs.out).", ""),
    "fc2d-gate-page-smoke": ("PASS", f"tools/page_smoke.py --unit FC2 --pages project -> 'in-browser grader: All 99 tests pass on seed 1982331660', 'page_smoke modules/FC/FC2/project.html: PASS', exit 0 ({S}page_smoke_project_alone.out). Other FC2 pages not re-run.", ""),
    "fc2d-gate-run-graders": ("PASS", f"tools/run_graders.py --unit FC2 -> 'run_graders FC2: PASS (reference 50/50 seeds)', exit 0 ({S}run_graders.out). Also harness_r17.py reference.py run 0-49 (50/50, {S}reference_run_0-49.out).", ""),
    "fc2d-gate-ruff": ("PASS", f"ruff check and ruff format --check on course/modules/FC/FC2/grader and tests/labs/FC2: 'All checks passed!' and 'already formatted', exit 0 ({S}ruff_check.out, {S}ruff_format.out).", ""),
    "fc2d-gate-mypy": ("PASS", f"Strict mypy (--config-file pyproject.toml, --no-incremental) on the staged grader (scanner.py = reference.py, instance.py, test_project.py, starter.py): 'Success: no issues found in 4 source files', exit 0 ({S}mypy_grader.out). Staging is needed because the suite imports scanner and instance.", ""),
    "fc2d-gate-pytest": ("PASS", f"Relevant suites: .venv/bin/python -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_refs.py tests/test_curriculum.py -> all dots, exit 0 ({S}pytest_relevant.out). This is a subset of tests/, not the full tree.", ""),
    "fc2d-gate-verify-refs": ("PASS", f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}verify_refs.out). The live run was not performed.", ""),
    "fc2d-collect-count": ("PASS", f"harness_r17.py grader collect on seeds 0-49 ({S}collect_per_seed.out: 99 tests on every seed) and seeds 50-83 (99 on all 34). project.html:320 states 99.", ""),
    "fc2d-seeds-84": ("PASS", f"harness_r17.py reference.py run 0-49 (50/50, {S}reference_run_0-49.out) and 50-83 (34/34, {S}reference_50-83.out): reference passes 99/99 on each of 84 seeds.", ""),
    "fc2d-starter-fails": ("PASS", f"harness_r17.py starter.py run 0-49: 0 of 50 seeds pass ({S}starter_0-49.r17.out).", ""),
    "fc2d-alternatives": ("PASS", f"41 alternative scanners (ledgers/FC2/scripts/FC2-d-r5, r6, r8, r10, r11, r14, r15 alts) each pass 50/50 seeds 0-49 with the new tie test present ({S}alts_summary.txt). Two r7 files named alt7_* are generator/checker scripts, not scanners, and are excluded (0/50).", ""),
    "fc2d-alt-r14-float-no-cutoff": ("PASS", f"alt3_float_epsilon_cutoff.py (FC2-d-r14/alts) 50/50 on seeds 0-49 ({S}alts_summary.txt); the float-cutoff alternative is not rejected by test_project.py:286-291 or 802-806, which are byte-identical in this delta.", ""),
    "fc2d-alt-r6-overconstraint": ("PASS", f"alt6_round6_alternative.py (FC2-d-r14) 50/50 on seeds 0-49 ({S}alts_summary.txt).", ""),
    "fc2d-mutate-builder": ("FAIL", f"tools/mutate_graders.py --unit FC2 --seeds 0-49 -> 'mutate_graders FC2: FAIL (108/111 killed)', exit 1 ({S}mutate_graders_FC2_0-49_r17.out). Survivors: r17_a_convexity_one_strike_returns_before_validation.py, r17_c_convexity_skips_length_check_for_one_strike.py, r17_d_convexity_chord_and_gross_in_plain_float.py. Probe: {S}probe_one_strike_r17.out; plain-float probe: {S}candidate_test_r17.py.", "Add the hand tests named under fc2d-spec-errors-scope and fc2d-r17-plain-float-convexity to course/modules/FC/FC2/grader/test_project.py; then re-run tools/mutate_graders.py --unit FC2 --seeds 0-49 and expect 111/111."),
    "fc2d-mut-new-r14": ("PASS", f"mutate_graders run ({S}mutate_graders_FC2_0-49_r17.out): KILLED r14_a..r14_e (seed 0).", ""),
    "fc2d-mut-v03": ("PASS", f"mutate_graders run: KILLED v03_parity_gross_bankers_round.py.", ""),
    "fc2d-mut-v04": ("PASS", f"mutate_graders run: KILLED v04_convexity_returns_one_based_index.py.", ""),
    "fc2d-mut-v05": ("PASS", f"mutate_graders run: KILLED v05_convexity_findings_before_parity.py.", ""),
    "fc2d-mut-v06": ("PASS", f"mutate_graders run: KILLED v06_gross_rounds_signed_gap_then_abs.py.", ""),
    "fc2d-mut-v01-boundary": ("PASS", f"mutate_graders run: KILLED v01_convexity_zero_net_kept.py.", ""),
    "fc2d-mut-v02-labels": ("PASS", f"mutate_graders run: KILLED v02_parity_explanation_names_P1_only.py.", ""),
    "fc2d-r5-mut-swap-weights": ("PASS", f"mutate_graders run: KILLED r5_b_swapped_chord_weights.py.", ""),
    "fc2d-r5-mut-skip-first": ("PASS", f"mutate_graders run: KILLED r5_c_parity_loop_skips_first_strike.py.", ""),
    "fc2d-r6-mut-new": ("PASS", f"mutate_graders run: KILLED r6_a, r6_b, r6_c.", ""),
    "fc2d-r7-mut-new": ("PASS", f"mutate_graders run: KILLED r7_a, r7_b, r7_c.", ""),
    "fc2d-r5-mut-direction": ("PASS", "ls ledgers/FC2/mutants shows r5_a, r5_b, r5_c and no r5_d (the direction mutant is absent as recorded).", ""),
    "fc2d-r5-grader-exact-ties": ("PASS", "course/modules/FC/FC2/grader/test_project.py:271-291 and 795-822 are unchanged in the delta (the only hunk is at 850); the exact-tie tests there pass on reference.py (harness_r17 run 0-49).", ""),
    "fc2d-r6-new-tie-tests": ("PASS", "test_project.py:809-849 unchanged; the delta inserts lines 850-859 (the non-dyadic tie test). The tie tests at 809-849 pass on reference.py 50/50 (harness run 0-49, out/reference_run_0-49.out).", ""),
    "fc2d-grader-stdlib": ("PASS", "test_module_imports_standard_library_only and test_module_does_not_import_grader_files pass on reference.py (harness_r17 run 0-49); grader/reference.py, instance.py and starter.py import only stdlib (read in full this round).", ""),
    "fc2d-grader-messages": ("PASS", "test_project.py:450-650 read in full this round; the message assertions pass on reference.py and kill z12_a..z12_g (mutate run). The one-strike validation gap is a coverage gap recorded under fc2d-spec-errors-scope, not a message defect.", ""),
    "fc2d-grader-instance-validity": ("PASS", CARRY16 + " grader/instance.py:41-60, 102-111, 118-131 re-read in full this round; reference passes on seeds 0-83.", ""),
    "fc2d-grader-instance-diversity": ("PASS", CARRY16 + " grader/instance.py:6-9, 134-142 re-read; make_instance(seed) runs on 84 seeds in harness_r17 with 99 passes each.", ""),
    "fc2d-lab1": ("PASS", "Lab 1 twin lab-FC2-project-1.py run alone with python -I -W error: stdout equals the expected block byte for byte, stderr 0 bytes ({S}twin_project_1.out). Every number re-derived in {S}rederive_r17.out (gaps 0, 120, 0, 0, -20, 0; chord 10500 = -75; net 30).", ""),
    "fc2d-lab2": ("PASS", "Lab 2 twin lab-FC2-project-2.py run alone: stdout equals the expected block. Page code differs from the twin only at the three blanks (gap line, two net lines), as a completion lab requires (run_labs PASS).", ""),
    "fc2d-lab3": ("PASS", f"Lab 3 twin lab-FC2-project-3.py run alone: stdout equals the expected block, stderr 0 bytes ({S}twin_project_3.out). Stated facts re-derived: gross 60 = cost at 4500 (net 0), chord at 6000 = -188/3, gross 63, net 3 ({S}rederive_r17.out).", ""),
    "fc2d-lab-twins-pure": ("PASS", f"tests/labs/FC2/lab-FC2-project-{{1,2,3}}.py run with python -I -W error from a scratch directory: exit 0, stderr empty ({S}twin_project_{{1,2,3}}.err). Page code equals the twins except the blanks of Lab 2.", ""),
    "fc2d-rederive-numbers": ("PASS", f"Independent exact-Fraction re-derivation of every printed number in Labs 1 and 3 and Exemplar B ({S}rederive_r17.py, {S}rederive_r17.out). All match project.html.", ""),
    "fc2d-rubric-observable": ("PASS", "project.html:504-516 (rubric table) read in full: each level names an observable (strikes, cents, legs, label names, check names). No level depends on an unstated quantity.", ""),
    "fc2d-rubric-calib-A": ("PASS", "Calibration against ~/.fanout/blind/FC2-d.json: blind A = [2,1,2,2,1]; project.html:584-641 data-scores 2,1,2,2,1. A matches on all five criteria.", ""),
    "fc2d-rubric-calib-B": ("PASS", "Blind B = [4,3,3,3,3]; project.html:520-583 data-scores 4,4,3,3,3. C1, C3, C4, C5 match; C2 differs by one level (4 vs 3), which is within the calibration tolerance named in the protocol.", ""),
    "fc2d-exemplar-numbers": ("PASS", f"Exemplar B: 6500 discounted 6175, gap 226; 7000 discounted 6650, gap 540; chord at 6000 = 802/3, call 330, chord less call -188/3, gross 63, net 3 ({S}rederive_r17.out). Exemplar A approximations (about 226, 540, 63) are consistent.", ""),
    "fc2d-exemplar-annotations": ("PASS", "Annotations read in full: the C3 annotation at project.html:543 (names P1-P4 and P6 for parity, P1, P2, P5 and P6 for convexity) is supported by the Model-free passage at :550, which now states P1, P2 and P3 for the parity findings; Limitations restates P1 to P3. The level 3/4 marks on C1-C5 agree with the rubric cells.", ""),
    "fc2d-exemplar-brief-structure": ("PASS", "project.html:489-499 (brief, six headings) and :518 (sentence on Exemplar B's five headings, without Chain and cost model; Exemplar A has Findings) match the passages in :520-641.", ""),
    "fc2d-spec-explanation-labels": ("PASS", "project.html:301 names the labels (parity P1, P2, P3, P4, P6; convexity P1, P2, P5, P6); test_project.py:680-686 asserts the exact label set and kills r15_b, r16_a and r16_b (mutate run).", ""),
    "fc2d-spec-errors-scope": ("FAIL", "project.html:309 says each condition is checked in every function that receives the input it names, and the grader checks it in each of those functions; :312 says df_ppm is checked in each of the three functions; :313 says the quote count is checked in convexity_violations. The suite has no one-strike chain test for these. Mutant r17_a (convexity returns [] for one strike before validating) returns [] for convexity_violations([100],[5],0) and convexity_violations([0],[5],PPM); mutant r17_c returns [] for convexity_violations([100],[5,5],PPM). Both survive all 99 tests on seeds 0-49 (mutate run; probe output in " + S + "probe_one_strike_r17.out). The reference raises ValueError for all three.", "Add hand tests in test_project.py: convexity_violations([100],[5],0) raises match='df_ppm'; convexity_violations([100],[5],PPM+1) raises match='df_ppm'; convexity_violations([0],[5],PPM) raises match='strictly increasing'; convexity_violations([100],[5,5],PPM) raises ValueError. Confirm the reference passes them."),
    "fc2d-hours": ("PASS", "project.html:339-357 table: 2+3+5+9+3+5+3 = 30; data-hours-project=30 at :29; index.html:29-41 gives 60 lesson + 30 project = 90 hours. Arithmetic consistent.", ""),
    "fc2d-reading-theorem-locator": ("PASS", "project.html:652-660: Theorem 1.2 (parity) at course/modules/FC/FC2/L05.html:63, Theorem 3.2 (convexity) at L05.html:115; Theorem 2.2 (bounds, used by instance.py) at L05.html:84 and its four bounds at :87-90, read this round.", ""),
    "fc2d-references-no-locator": ("PASS", "project.html:652-660 states no chapter, page or equation from the three listed references; the registry records are unchanged since e896b7a4 (references/references.json).", ""),
    "fc2d-notation": ("PASS", "project.html uses C, P, S, K, D (as df = df_ppm/1e6) and labels P1-P6; none of the registry symbols in notation/notation.json (T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q) occurs in project.html (grep). The page disambiguates P (put price) from P1-P6 at :Conventions.", ""),
    "fc2d-simulated-label": ("PASS", "grep -c SIMULATED course/modules/FC/FC2/project.html = 18; the chains in Labs 1-3, the instance (label 'SIMULATED', test_project.py:892-894) and the curriculum all carry the label.", ""),
    "fc2d-process-banned": ("PASS", f"check_pages.py --unit FC2 PASS ({S}check_pages.out) covers banned strings in visible prose; the new sentences in the delta (project.html:543, :550) contain no process words.", ""),
    "fc2d-ladder-claims": ("PASS", "project.html:40-50 ladder read in full: Rung 1 and 2 on the page, Rung 3 graded, Rung 4 stretch; the ladder matches check_projects PASS.", ""),
    "fc2d-curriculum-scope": ("PASS", "curriculum/02-economics-finance-core.yaml:427-429 now reads 'Given a SIMULATED option-chain snapshot' (line 428), so the round-16 registry flag about 'embedded' is resolved; the curriculum file is unchanged since e896b7a4.", ""),
    "fc2d-no-external": ("PASS", f"check_pages.py --unit FC2 PASS: no CDN or external script in project.html ({S}check_pages.out).", ""),
    "fc2d-new-tests": ("PASS", "test_project.py:682-686 (explanation label check) is unchanged; the delta's new test at 853-860 was checked for correctness by hand and by running it against the reference (candidate_test_r17.py-style chain, expected row present).", ""),
    "fc2d-lab1-hypothesis-terms": ("PASS", "project.html:55 (Lab 1 hypothesis: gross, net, three legs, 45 cents) matches the printed output and Lab 1's expected block.", ""),
    "fc2d-r6-project-line335": ("PASS", "project.html:37, :285, :335, :495, :511 read this round; the P-label and cost statements agree with the conventions at :335 and the brief at :495-511.", ""),
    "fc2d-r7-project-anchor-links": ("PASS", "project.html:37 and :282 anchor links (#conventions, #spec, #grader-section, #report, #stretch, #self-assessment, #rubric, #exemplars) resolve to ids present in the page (check_pages PASS).", ""),
    "fc2d-dag-closure": ("PASS", f"check_dag.py --unit FC2 PASS ({S}check_dag.out). The concepts linked from project.html (arbitrage-opportunity, put-call-parity, option-arbitrage-bounds) are defined in L01 and L05, which are in FC2's closure.", ""),
    "fc2d-r14-delta": ("PASS", "project.html:518 (brief structure sentence) and test_project.py:682-686 unchanged in the delta except line 320 (count) and the hunk at 543/550; the r14 delta claims still hold.", ""),
    "fc2d-r15-mut-a-parity-explanation-direction": ("PASS", "Fixed since round 16: ledgers/FC2/mutants/ no longer holds r15_a (git status: R100 ledgers/FC2/mutants/r15_a... -> ledgers/FC2/equivalent/r15_a...). ls ledgers/FC2/equivalent shows r15_a, r15_c, r15_d and README.md. Under ruling 34 the file is an equivalent; eq harness 50/50 on seeds 0-49 ({S}eq_r15_a_parity_explanation_reverses_the_positive_gap_trade.r17.out).", ""),
    "fc2d-r15-mut-b-convexity-names-P4": ("PASS", "mutate_graders run: KILLED r15_b_convexity_explanation_names_P4_as_an_input.py by test_scan_explanations_are_nonempty_and_name_the_rule.", ""),
    "fc2d-r15-mut-c-explanation-net-as-gross": ("PASS", f"Under ruling 34 this is an equivalent, not a mutant: equivalent/r15_c passes 50/50 on seeds 0-49 ({S}eq_r15_c_parity_explanation_prints_gross_where_net_belongs.r17.out). Caveat recorded: the mutant prints a wrong number inside the explanation text; the ruling accepts it because project.html:301 states labels, not numbers.", ""),
    "fc2d-r15-mut-d-convexity-explanation-side": ("PASS", f"Under ruling 34 this is an equivalent: equivalent/r15_d passes 50/50 on seeds 0-49 ({S}eq_r15_d_convexity_explanation_reverses_the_chord_side.r17.out).", ""),
    "fc2d-r15-alt-integer-decimal": ("PASS", f"alt7_integer_scaled.py and alt8_decimal_60.py (FC2-d-r15/alts) each 50/50 on seeds 0-49 ({S}alts_summary.txt).", ""),
    "fc2d-r16-mut-a-parity-explanation-names-P5": ("PASS", "mutate_graders run: KILLED r16_a_parity_explanation_names_P5_too.py by test_scan_explanations_are_nonempty_and_name_the_rule (seed 1). project.html:301 says a parity finding names P1, P2, P3, P4 and P6, so the extra P5 violates a stated behaviour.", ""),
    "fc2d-r16-mut-b-convexity-without-convex-word": ("PASS", "mutate_graders run: KILLED r16_b_convexity_explanation_states_chord_rule_without_the_word.py by test_scan_explanations_are_nonempty_and_name_the_rule (seed 0); project.html:301 requires the explanation to name the rule.", ""),
    "fc2d-r16-mut-c-float-chord-weights": ("PASS", "Fixed since round 16: mutate_graders run now KILLS r16_c_convexity_chord_weights_as_float_fractions.py by test_convexity_half_cent_tie_at_a_non_dyadic_chord_weight_rounds_once_up (seed 0). The new test is at test_project.py:853-860; the reference returns [('convexity',2,1,1)].", ""),
    "fc2d-r16-lab-docstrings-L04-L06": ("PASS", CARRY16_LABS + " tests/labs/FC2 has no diff between e896b7a4 and aa659725; run_labs 11/11 PASS in this round.", ""),
    "fc2d-r16-explanation-check-no-overconstraint": ("PASS", f"The label-set check (test_project.py:683-686) accepts the reference and all 41 alternatives (50/50 each) and all three equivalents (50/50 each): {S}alts_summary.txt, eq_*.r17.out.", ""),
    "fc2d-r16-equivalence-wording-scope": ("PASS", CARRY16_EQ + " README states (a) the label set and rule word are the reference's, (b) the three pass seeds 0-9. Re-run this round: all three pass seeds 0-49 (eq_*.r17.out). The README's three-member list is accurate now that r15_a is in equivalent/.", ""),
}

NEW = {
    "fc2d-r17-plain-float-convexity": ("FAIL",
        "Mutant r17_d_convexity_chord_and_gross_in_plain_float.py (weights (high-mid)/(high-low) in float, gross = int((-sd + 0.5)//1)) survives all 99 tests on seeds 0-49. project.html:308 states each money value is computed from exact fractions and rounded once. The existing exact-tie tests pass by luck under plain float: the chain strikes [1,2,7] calls [2,3,5] gives a float chord of exactly 2.5 (python -I check, " + S + "float_chord_tie_r17.out). The chain strikes [1,2,7] calls [7,7,4] puts [8,9,11] (spot 0, df 1, fee 0, spread 0) has an exact half-cent convexity gross of 1 at strike 2, but plain float gives chord 6.500000000000001 and gross 0, so the mutant returns [] where the reference returns [('convexity',2,1,1)]. candidate_test_r17.py: reference PASS; r17_d FAIL; r16_c FAIL; alt3_float_epsilon_cutoff, alt8_decimal_60, alt3_decimal, alt1_fraction_class, alt10_cross_multiplied_convexity_no_fraction all PASS.",
        "Add to course/modules/FC/FC2/grader/test_project.py a test with strikes [1,2,7], calls [7,7,4], puts [8,9,11], spot 0, df PPM, fee 0, spread 0, asserting rows_of(sol.scan(chain)) == [('convexity', 2, 1, 1)]. Re-run the mutate and the reference on seeds 0-49."),
    "fc2d-r17-test-comment-856": ("FAIL",
        "test_project.py:856 comment says 'The weights are not dyadic, so a float computation does not keep the tie' for the chain [1,2,7] [2,3,5] [3,5,12]. That is false for plain float arithmetic on this chain: w_low*2 + w_high*5 with float weights is exactly 2.5 (" + S + "float_chord_tie_r17.out). Only a float weight converted to a Fraction (r16_c) loses the tie. The comment states a fact about the code that the code does not show.",
        "Reword the comment at test_project.py:855-856 to say what is true: float weights 5/6 and 1/6 are not exact, and making them Fractions (Fraction(float)) loses the exact tie; or move the non-dyadic claim onto the [7,7,4] chain once the plain-float test is added (fc2d-r17-plain-float-convexity)."),
    "fc2d-r17-equivalent-probe-one-strike-scan-df": ("PASS",
        "Probe mutant (scan validates df_ppm only when len(strikes) > 1) is behaviourally equivalent: scan's convexity_violations call re-checks df_ppm, so scan(one strike, df=0) still raises 'df_ppm must lie in 1 to 1000000' (" + S + "probe_one_strike_r17.out, r17_b row: ValueError). It passes 99/99 on seeds 0-2. It was not kept in ledgers/FC2/mutants/ and sits in " + S + "equiv_candidates/.",
        ""),
    "fc2d-r17-plain-float-parity": ("PASS",
        "Mutant r17_e_parity_gap_in_plain_float.py (parity gap and gross in plain float) is KILLED by test_parity_exact_tie_at_a_non_dyadic_discount_factor (seed 0; 1 failed, 98 passed on seeds 0-9, " + S + "mutate_graders_FC2_0-49_r17.out). The parity float route is covered.",
        ""),
    "fc2d-r17-new-tie-test-no-overconstraint": ("PASS",
        f"The new test (test_project.py:853-860) passes on reference.py and on 41 alternatives 50/50 (alts_summary.txt); its expected value 1 follows from the stated exact-fraction rule (project.html:308) and from the gross rule (half up in magnitude, project.html:308), so it does not over-constrain an exact implementation. Hand-derived: chord = (5*2 + 1*5)/6 = 5/2; call 3; violation 1/2; gross 1 (rederive_r17.out row 'NEW TEST').",
        ""),
    "fc2d-r17-delta-hunks": ("PASS",
        "Delta aa659725 vs e896b7a4, read hunk by hunk: project.html:320 (98 -> 99); project.html:543 (Exemplar B C3 annotation) and :550 (Model-free passage, adds P1, P2 and P3 for parity); test_project.py:850-859 (new non-dyadic tie test); plans/FINAL-ARCHITECT-RULINGS.md rulings 31, 35, 36 (35 and 36 outside this slice; 31 and 34 read); ledgers/FC2/equivalent/r15_a (git mv, identical content R100); ledgers/FC2/mutants/ r16_a, r16_b, r16_c added. Lab twins, instance.py, reference.py, starter.py, lessons L04-L06 (other slices) not changed in the slice.",
        ""),
}

rows = []
prev_ids = [r["id"] for r in PREV["rows"]]
assert len(prev_ids) == len(set(prev_ids)) == 74, len(prev_ids)
for r in PREV["rows"]:
    status, evidence, fix = R[r["id"]]
    row = {"id": r["id"], "check": r["check"], "location": r["location"], "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)
assert set(R) == set(prev_ids), set(R) ^ set(prev_ids)
for rid, (status, evidence, fix) in NEW.items():
    loc = {
        "fc2d-r17-plain-float-convexity": "course/modules/FC/FC2/grader/test_project.py:853-860; project.html:308",
        "fc2d-r17-test-comment-856": "course/modules/FC/FC2/grader/test_project.py:855-856",
        "fc2d-r17-equivalent-probe-one-strike-scan-df": "ledgers/FC2/scripts/FC2-d-r17/equiv_candidates/r17_b_scan_skips_df_check_for_one_strike_chain.py",
        "fc2d-r17-plain-float-parity": "ledgers/FC2/mutants/r17_e_parity_gap_in_plain_float.py",
        "fc2d-r17-new-tie-test-no-overconstraint": "course/modules/FC/FC2/grader/test_project.py:853-860",
        "fc2d-r17-delta-hunks": "git diff e896b7a4 aa659725",
    }[rid]
    chk = {
        "fc2d-r17-plain-float-convexity": "plain-float convexity chord and gross (exact-fraction rule) are caught by the suite",
        "fc2d-r17-test-comment-856": "comments state what the code shows",
        "fc2d-r17-equivalent-probe-one-strike-scan-df": "one-strike scan df probe is equivalent to the reference (not a finding)",
        "fc2d-r17-plain-float-parity": "plain-float parity gap is caught by the suite",
        "fc2d-r17-new-tie-test-no-overconstraint": "new non-dyadic tie test does not reject exact or alternative implementations",
        "fc2d-r17-delta-hunks": "every hunk in the delta read and mapped to a row",
    }[rid]
    row = {"id": rid, "check": chk, "location": loc, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

mutants = []
for line in MUT_OUT:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    verdict, name, desc, killer = m.groups()
    mutants.append({
        "id": name,
        "description": desc,
        "killed_by": killer if verdict == "KILLED" else None,
        "status": verdict,
    })
assert len(mutants) == 111, len(mutants)

fragment = {
    "unit": "FC2",
    "slice": "d",
    "round": 17,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 17 (did not build FC2)",
    "pin": "aa6597255304919b9c4e5e5ca07763ae3e13d45c",
    "base": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a (round-16 pin; previous fragment ~/.fanout/frags/D-FC2-d.round16.json, read as context, its PASS rows re-verified or carried by byte-identity)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD17-FC2-d (detached at aa659725, .venv symlinked, vendor copied)",
    "scratch": "ledgers/FC2/scripts/FC2-d-r17/ (harness_r17.py, make_mutants_r17.py, build_fragment_r17.py, rederive_r17.py, probe_one_strike_r17.py, candidate_test_r17.py, search_plain_float_tie_r17.py, equiv_candidates/) and out/",
    "verified_at": "2026-11-09T14:40:19+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "hull2021options, stoll1969relationship, cox1979option: registry records carry no edition, volume or issue; the page quotes none (carried from round 16; references/references.json unchanged since e896b7a4).",
    ],
    "freshness_flags": [
        "plans/FC2-open-items.md departure 4 says the test count is 75 for seeds 0-49; the suite collects 99 on every seed 0-83 (out/collect_per_seed.out). Stale; the file is unchanged since e896b7a4.",
        "plans/FC2-open-items.md DAG_DEFECTS says FC2's closure excludes FC1; check_dag PASS in this round. Stale; file unchanged.",
        "plans/FC2-open-items.md departure 7 says mutants are 10/10 killed; mutate_graders FC2 0-49 now reports 108/111 killed with three survivors (r17_a, r17_c, r17_d). Stale.",
        "Resolved since round 16: the curriculum flag (curriculum/02-economics-finance-core.yaml:428 now says 'Given a SIMULATED option-chain snapshot').",
        "ledgers/FC2/equivalent/README.md is accurate now that r15_a is in equivalent/ (the round-16 freshness note on this is resolved).",
    ],
    "notes": [
        "Delta since the round-16 pin e896b7a4 (aa659725 = two commits, 0626d3b0 and aa659725): read hunk by hunk. In slice d: project.html:320 (count 98 to 99), :543 and :550 (Exemplar B C3 annotation and Model-free passage); grader/test_project.py:850-859 (new non-dyadic tie test); ledgers/FC2/mutants/ r16_a, r16_b, r16_c added; ledgers/FC2/equivalent/ r15_a moved in by git mv (content identical). Not in slice d but noted: L04, L05, L06 lesson prose, cards.json and FC1/M5/M7 files changed; FINAL-ARCHITECT-RULINGS.md rulings 35 and 36 added (outside this slice).",
        "Full read this round: project.html (674 lines, every section), grader/test_project.py (923 lines), grader/reference.py, instance.py, starter.py, the three project lab twins, the exemplars and the rubric. The round-16 note that the full-file read was not repeated does not apply this round.",
        "Ruling 34 (binding) treats r15_a, r15_c and r15_d as equivalents. r15_c changes a printed number inside the explanation (net printed as gross); the verifier accepts it under the ruling, and this caveat is recorded as before.",
        "Fail-closed decision: the one-strike gap (r17_a, r17_c) and the plain-float gap (r17_d) are FAIL rows because project.html:308-313 states the rules that they violate. The one-strike probe r17_b is behaviourally equivalent (scan re-checks df_ppm inside convexity_violations) and is not counted as a finding.",
        "The reference, all 84 seeds, collects 99 and passes 99. starter fails 50/50. The three lab twins run alone under python -I -W error with empty stderr. page_smoke for project.html passes in Chromium with 99 in-browser tests.",
        "Calibration: A matches the blind scorer exactly; B differs on C2 by one level, the tolerance the protocol names. No calibration fault.",
        "The full tests/ tree was not run; the relevant FC2-touching suites were run (test_labs, test_run_labs, test_page_checks, test_refs, test_curriculum). verify_refs was run offline only.",
        "Not checked: the claim that --assert=plain prints no expected values on failure (project.html local-run paragraph) was not executed; the three lab-FC2-L04/L06 lesson pages (other slices) were not re-verified here; the hub index.html lede and ladder are for the hub verifier; no published source was read (theorem numbers and bounds were checked against the lesson text only).",
    ],
    "summary": "",
}

fragment["summary"] = (
    f"FC2-d round 17 on aa659725: {sum(1 for r in rows if r['status']=='PASS')} PASS, "
    f"{sum(1 for r in rows if r['status']=='FAIL')} FAIL of {len(rows)} rows. "
    "Non-PASS: fc2d-mutate-builder (108/111 killed; r17_a, r17_c, r17_d survive); fc2d-spec-errors-scope (one-strike validation not tested for convexity_violations; project.html:309-313); "
    "fc2d-r17-plain-float-convexity (plain-float chord survives; chain [1,2,7] [7,7,4] [8,9,11] kills it, and 5 alternatives pass it); "
    "fc2d-r17-test-comment-856 (comment says a float computation loses the tie; plain float keeps it on that chain). "
    "Fixed since round 16: fc2d-r15-mut-a (r15_a in equivalent/), fc2d-r16-mut-c (killed by the new tie test). "
    "All gates PASS: check_pages, check_dag, check_projects, run_labs 11/11, page_smoke (project), run_graders 50/50 (84 seeds), starter 0/50, collect 99 on every seed, ruff, strict mypy (staged), relevant pytest, verify_refs offline, 41 alternatives 50/50, 3 equivalents 50/50."
)

out = ROOT / "ledgers/FC2/FC2-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, len(rows), "rows", len(mutants), "mutants")
