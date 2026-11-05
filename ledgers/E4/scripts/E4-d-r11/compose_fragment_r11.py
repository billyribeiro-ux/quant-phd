"""Compose the round-11 fragment ledgers/E4/E4-d.json from the round-10 row ids and the round-11 evidence logs."""
import json
import re
import sys

ROOT = sys.argv[1]
PREV = "/Users/billyribeiro/.fanout/frags/E-E4-d.round10.json"
LOG = f"{ROOT}/ledgers/E4/scripts/E4-d-r11/logs"
prev = json.load(open(PREV, encoding="utf-8"))
prev_ids = [r["id"] for r in prev["rows"]]
prev_by_id = {r["id"]: r for r in prev["rows"]}

HUNKS = ("hunks of 00a84795..11d7077 in this file touch only project.html:316, :318, :383, :397 and "
         "test_project.py:499, :515-516, :521, :527-528, :533 (reference.py:126; lab-E4-project-3 twin lines 7 and 21)")


def carry(rid, subject):
    old = prev_by_id[rid]
    return {
        "id": rid,
        "check": old["check"],
        "location": old["location"],
        "status": "PASS",
        "evidence": f"Carried from round 10 ({subject} byte-identical since the previous pin; {HUNKS}): " + old["evidence"],
    }


def fresh(rid, status, evidence, fix=None):
    old = prev_by_id[rid]
    row = {"id": rid, "check": old["check"], "location": old["location"], "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    return row


def new(rid, check, location, status, evidence, fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    return row


R = {}
# ---- commands and gates, re-run at this pin (logs in ledgers/E4/scripts/E4-d-r11/logs) ----
R["E4d-cmd-check-projects"] = fresh("E4d-cmd-check-projects", "PASS", f"`tools/check_projects.py --unit E4` -> 'check_projects E4: PASS' (logs/check_projects.txt).")
R["E4d-cmd-check-pages"] = fresh("E4d-cmd-check-pages", "PASS", "`tools/check_pages.py --unit E4` -> 'check_pages E4: PASS' (logs/check_pages.txt). Its BANNED-phrase and link checks cover the changed prose.")
R["E4d-cmd-check-dag"] = fresh("E4d-cmd-check-dag", "PASS", "`tools/check_dag.py --unit E4` -> 'check_dag E4: PASS' (logs/check_dag.txt).")
R["E4d-cmd-run-labs"] = fresh("E4d-cmd-run-labs", "PASS", "`tools/run_labs.py --unit E4` -> 'run_labs E4: PASS (12/12)' (logs/run_labs.txt).")
R["E4d-cmd-run-graders"] = fresh("E4d-cmd-run-graders", "PASS", "`tools/run_graders.py --unit E4 --seeds 0-49` -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)' (logs/run_graders.txt).")
R["E4d-cmd-page-smoke-project"] = fresh("E4d-cmd-page-smoke-project", "PASS", "`tools/page_smoke.py --unit E4 --pages project` alone -> 'in-browser grader: All 43 tests pass on seed 2042051995', 'page_smoke E4: PASS' (logs/page_smoke_project.txt).")
R["E4d-cmd-ruff"] = fresh("E4d-cmd-ruff", "PASS", "`.venv/bin/python -m ruff check course/modules/E/E4 tests/labs/E4` -> 'All checks passed!' (logs/ruff_check.txt). Explicitly passing ledgers/E4/mutants reports 32 errors, but pyproject.toml extend-exclude lists ledgers/*/mutants, so the project gate does not check them.")
R["E4d-cmd-mypy-workspace"] = fresh("E4d-cmd-mypy-workspace", "PASS", "`.venv/bin/python -m mypy --no-incremental course/modules/E/E4/grader tests/labs/E4` -> 'Success: no issues found in 16 source files' (logs/mypy.txt).")
R["E4d-cmd-mypy-plan-command"] = fresh("E4d-cmd-mypy-plan-command", "PASS", "Same mypy run as E4d-cmd-mypy-workspace (logs/mypy.txt).")
R["E4d-cmd-pytest-relevant"] = fresh("E4d-cmd-pytest-relevant", "PASS", "`.venv/bin/python -m pytest -q tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py` -> all dots, exit 0 (logs/pytest_relevant.txt).")
R["E4d-cmd-verify-refs"] = fresh("E4d-cmd-verify-refs", "PASS", "`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' (logs/verify_refs_offline.txt). references.json changed (generated_at, BK1 list); both E4 keys still resolve (see E4d-registry-*).")
R["E4d-cmd-collect"] = fresh("E4d-cmd-collect", "PASS", "`pytest --collect-only -q test_project.py` in a scratch dir with instance.py, test_project.py, solver.py = reference.py -> '43 tests collected' (logs/collect.txt).")
# ---- labs ----
R["E4d-lab-project-1"] = fresh("E4d-lab-project-1", "PASS", "run_labs PASS (logs/run_labs.txt); twin run `python -I -W error tests/labs/E4/lab-E4-project-1.py` exit 0; page code equals twin (logs/twin_compare_r11.txt: equal=True).")
R["E4d-lab-project-2"] = fresh("E4d-lab-project-2", "PASS", "run_labs PASS (logs/run_labs.txt); page code equals the twin except the blank line, the return of indifference_gap (logs/twin_compare_r11.txt: only the return line differs).")
R["E4d-lab-project-3"] = fresh("E4d-lab-project-3", "PASS", "run_labs PASS; page code equals twin (logs/twin_compare_r11.txt: equal=True); twin run under -I -W error exit 0; output lines re-read: 9 grid rows, largest bisection-vs-closed-form difference 2.1e-13, gap column max |.| 3.55e-14, 484 of 484 box points (twin output observed this round).")
R["E4d-num-lab-hypotheses"] = carry("E4d-num-lab-hypotheses", "project.html:57, :176, :376 (Lab 1, Lab 2, Lab 3 hypothesis paragraphs)")
R["E4d-num-exemplar-table"] = fresh("E4d-num-exemplar-table", "PASS", "project.html:629-641 read in this round: every row of the Exemplar B table (0.5567/0.1420/+3.55e-14 etc.) equals the Lab 3 printed grid (twin output observed this round); 0.6978/0.5582 = 1.2501 and 0.8373/0.5582 = 1.5000, matching the stated 1.25 and 1.50 ratios.")
R["E4d-num-box-bounds"] = fresh("E4d-num-box-bounds", "PASS", "Recomputed: tau-bar(0.150) = 2e^{-0.6}-1 = 0.0976232722; tau-bar(0.120) = 2e^{-0.48}-1 = 0.2375667836; 1/(1+4*0.75^2) = 0.3076923077. Page project.html:314 quotes 0.09762327, 0.23756678, 0.30769 and bounds 0.097623 <= tau-bar <= 0.237567 (grader/instance.py:14-17 draws in [0.500,0.750] and [0.120,0.150], rounded to 3 decimals, consistent).")
R["E4d-prose-lede-directional"] = carry("E4d-prose-lede-directional", "project.html:37 (lede)")
R["E4d-math-lemmas"] = carry("E4d-math-lemmas", "project.html:265-273 (Lemmas 1-3)")
R["E4d-math-prop1"] = carry("E4d-math-prop1", "project.html:276-283 (Proposition 1)")
R["E4d-math-prop2"] = carry("E4d-math-prop2", "project.html:285-287 (Proposition 2)")
R["E4d-math-prop3"] = carry("E4d-math-prop3", "project.html:288-293 (Proposition 3)")
R["E4d-math-prop4"] = fresh("E4d-math-prop4", "PASS", "project.html:295-298 (Proposition 4) read again: for a=2, tau_e=1, tau-bar in (0,1): lambda* = 2 sigma sqrt(tb/(1-tb)) solves tau_y(lambda) = lambda^2/(lambda^2+4 sigma^2) = tb, the closed form the accuracy requirement and check_accuracy_r11.py use (logs/check_accuracy_r11.txt). Boundary cases 1/(1+4 sigma^2) match tau_y(1). Unchanged text.")
R["E4d-math-prop5"] = carry("E4d-math-prop5", "project.html:300-301 (Proposition 5)")
R["E4d-math-assumptions"] = carry("E4d-math-assumptions", "project.html:257-262 (A1-A5)")
R["E4d-notation"] = fresh("E4d-notation", "PASS", "Whole-page re-check of symbols in the changed hunks (project.html:316, :318, :383, :397): \\bar\\tau (target precision, defined at project.html:255 in the Notation paragraph), \\lambda^*, \\sigma, 10^{-50}, 10^{-10}, 10^{-8}, 10^{-14}, 10^{-12}. No new symbol; no symbol reused with a new meaning. Lab 3 code identifiers TOLERANCE and MAX_HALVINGS are code names, not notation.")
R["E4d-banned-phrases"] = fresh("E4d-banned-phrases", "PASS", "tools/check_pages.py (BANNED tuple, tools/check_pages.py:58) PASS on the changed page (logs/check_pages.txt). Changed prose in project.html:316, :318, :383 read in full: no banned phrase.")
R["E4d-process-words"] = fresh("E4d-process-words", "PASS", "Changed learner text (project.html:316, :318, :383, :397) read in full. grep -i -w for round, verifier, builder, fixer, ruling, slice over project.html, grader/*.py and the three project labs: the only hits are Python round() calls in instance.py:34-35 and test_project.py:470.")
R["E4d-dag-links"] = fresh("E4d-dag-links", "PASS", "tools/check_dag.py --unit E4 PASS (logs/check_dag.txt). Local href targets in project.html: 17 of 17 resolve to ids on the page (inline script run this round).")
R["E4d-registry-muth"] = fresh("E4d-registry-muth", "PASS", "project.html:684 data-cite 'muth1961rational' present in references/references.json (script check this round: 560 keys, both cited keys present); verify_refs --offline PASS.")
R["E4d-registry-milgrom"] = fresh("E4d-registry-milgrom", "PASS", "project.html:685 data-cite 'milgrom1982information' present in references/references.json (560 keys checked this round).")
R["E4d-cites-only-registry"] = fresh("E4d-cites-only-registry", "PASS", "project.html data-cite values: ['muth1961rational', 'milgrom1982information'], both registry keys (script this round). No other citation in the page.")
R["E4d-spec-context-sentences"] = carry("E4d-spec-context-sentences", "project.html:312 (Context)")
R["E4d-spec-questions"] = fresh("E4d-spec-questions", "PASS", "project.html:314-322 read in full this round. Inputs (314): unchanged; Required outputs (316): now points to 'the accuracy requirement in the constraints below', which exists at :318; Constraints (318): read and checked against grader/test_project.py (E4d11-constraints-accuracy); Grading mode (320): 43 checks, equal to the collect-only count (E4d-cmd-collect).")
R["E4d-spec-ladder"] = carry("E4d-spec-ladder", "project.html:40-49, :51-305, :308, :669-675")
R["E4d-prose-scope-words"] = fresh("E4d-prose-scope-words", "PASS", "project.html:326 (Exception table paragraph) unchanged, scope words checked. Changed scope words at :318 ('no accuracy requirement for smaller tau-bar', 'the suite does not test accuracy there'): tests at project.html-cited instances use cost 0.13, 0.15 and the box (test_project.py:513-534, :343), so 'does not test accuracy there' holds on tau-bar < 1e-2 (grep of accuracy comparisons: lines 343, 520, 532 only).")
R["E4d-prose-simulated-labs"] = carry("E4d-prose-simulated-labs", "project.html:57, :176, :314 (Inputs), :375")
R["E4d-prose-simulated-exemplars"] = carry("E4d-prose-simulated-exemplars", "project.html:530 (exemplar intro)")
R["E4d-hours-project"] = fresh("E4d-hours-project", "PASS", "project.html:33 data-hours-project=28 and :35 '28 hours'; index.html:43 '72 h lessons · 28 h project (28%)' and index.html:139 'Nine lessons of eight study hours each, which is 72 hours'; 72 + 28 = 100 and 28/100 = 28%. Note: the round-10 row cited index.html:29, which is not the hours line at this pin; the cited line is now :43. The project.html hours table (:341-352) is unchanged.")
R["E4d-hours-estimate"] = carry("E4d-hours-estimate", "project.html #hours (:344-351)")
R["E4d-rubric-observable"] = carry("E4d-rubric-observable", "project.html:517-527 (#rubric)")
R["E4d-exemplar-A-calibration"] = fresh("E4d-exemplar-A-calibration", "UNVERIFIABLE", "project.html:533-597 read this round: the official scores are data-scores='2,2,1,2,1' (line 536) and the annotations are visible in the same markup. A blind calibration needs a scorer who has not read the annotations; this verifier has. Not scored.", fix="Have a scorer who has not seen the annotations score Exemplar A on the five criteria, and compare with data-scores 2,2,1,2,1.")
R["E4d-exemplar-B-calibration"] = fresh("E4d-exemplar-B-calibration", "UNVERIFIABLE", "project.html:598-661 read this round: data-scores='4,4,4,4,4' (line 601). Same reason: this verifier has read the annotations, so no blind score is possible. Not scored.", fix="Have a scorer who has not seen the annotations score Exemplar B and compare with data-scores 4,4,4,4,4.")
R["E4d-exemplar-annotations-hidden"] = carry("E4d-exemplar-annotations-hidden", "course/assets/js/rubric.js:147-150 and the project.html reveal markup (data-reveal, .annotation)")
R["E4d2-exemplar-B-C1-annotation"] = fresh("E4d2-exemplar-B-C1-annotation", "PASS", "project.html:604-607 read this round: the Exemplar B model passage names the assumptions and the propositions that use each. Checked against the page: Propositions 1-5 each state 'Assume A1 to A5' (project.html:276, :285, :288, :295, :300), and the A2 clearing role at lambda = 0 (Proposition 2 proof, :285-287) matches the annotation. The annotation's level claim is consistent with the descriptor (level 4).")
R["E4d-grader-exceptions"] = carry("E4d-grader-exceptions", "test_project.py:191-234 and :242-280, reference.py:26-34, project.html:326 exception table")
R["E4d-grader-messages"] = fresh("E4d-grader-messages", "PASS", "Messages grepped this round (every expect( and must_raise( call in test_project.py); the changed messages at :521 and :533 were read in full and name the property ('check the bisection's accuracy near the root'; 'check the bracket and the bisection's accuracy') with no values. Messages of unchanged tests are the round-10 subject, carried by line range.")
R["E4d-grader-oracle"] = carry("E4d-grader-oracle", "test_project.py:79-170 (oracle functions)")
R["E4d-grader-instances"] = carry("E4d-grader-instances", "grader/instance.py and test_project.py:37-40")
R["E4d-grader-instance-docstring"] = carry("E4d-grader-instance-docstring", "grader/instance.py:1-21")
R["E4d-grader-test-docstring"] = fresh("E4d-grader-test-docstring", "PASS", "The tiny-root docstring changed at test_project.py:527-528 (was :481-484). New text: 'A root near 1e-12 is as precise as one near 0.5 when the noise volume is at least 1e-50 and tau-bar is at least 1e-2, as in every case here'. Checked: the parametrized sd values 1e-11, 1e-12, 1e-30, 1e-40 are >= 1e-50 and the cost 0.15 gives tau-bar = 0.0976 >= 1e-2 (computed). Root near 1e-12 is approximate for sd = 1e-12 (root = 6.6e-13); accepted as 'near'.")
R["E4d-grader-reference-docstring"] = carry("E4d-grader-reference-docstring", "grader/reference.py:21-23 (BISECTION_TOLERANCE and MAX_BISECTION_STEPS comments)")
R["E4d-grader-stdlib"] = fresh("E4d-grader-stdlib", "PASS", "test_solver_imports_only_the_standard_library passes for reference.py and all 5 alternatives on seeds 0-49 (logs/ref_seeds_0_49_r11.txt, logs/alternatives_seeds0-49_r11.txt), and for the closed-form alternative r11-a (logs/alt_r11_a_seeds0-49.txt).")
R["E4d-runtime"] = fresh("E4d-runtime", "PASS", "run_graders 'slowest 0.2 s' over seeds 0-49 (logs/run_graders.txt); page_smoke in-browser suite 0.8 s (logs/page_smoke_project.txt).")
R["E4d-browser-local-parity"] = fresh("E4d-browser-local-parity", "PASS", "page_smoke project PASS (in-browser grader, 43 tests, logs/page_smoke_project.txt) and the local seeds 0-49 runs (logs/ref_seeds_0_49_r11.txt).")
R["E4d3-cara-defined-twice"] = carry("E4d3-cara-defined-twice", "project.html:259 (A3); L06.html:57, :66 (L06 changed only at lines 51, 225, 602)")
R["E4d3-anchors-links"] = fresh("E4d3-anchors-links", "PASS", "All 17 local href='#...' targets in project.html resolve to ids on the page (inline script run this round: 17 local hrefs, 0 missing).")
R["E4d3-no-figures-no-data"] = fresh("E4d3-no-figures-no-data", "PASS", "project.html: 0 img/svg/canvas/figure/video elements and 0 figures-/assets/data/data-files references (script this round).")
R["E4d3-atlas-studios-na"] = carry("E4d3-atlas-studios-na", "atlas/ (no atlas file changed between the pins)")
R["E4d3-spec-stop-rule-and-constraints"] = fresh("E4d3-spec-stop-rule-and-constraints", "PASS", "Round-10 FAIL resolved: project.html:318 no longer states a stop rule or a step count (it states the accuracy requirement instead). The mutant that differs only in the stop rule (mutant_v9_02) was moved to ledgers/E4/equivalent/ and is numerically within the requirement (logs/check_accuracy_r11.txt, 0 failures in 3009 cases). The separate plan conflict on the documented tolerance is E4d11-plan-tolerance-documented.")
R["E4d3-mutants-r3"] = fresh("E4d3-mutants-r3", "PASS", "All mutant_r3_* killed in logs/mutate_graders_seeds0-9_r11_final.txt (KILLED lines).")
R["E4d3-mutant-tolerance-survives"] = fresh("E4d3-mutant-tolerance-survives", "PASS", "mutant_r3_tolerance_1e-9.py KILLED by test_fraction_is_the_oracle_root[first] (seed 0) (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d6-mutant-06"] = fresh("E4d6-mutant-06", "PASS", "mutant_r6_06_cost_scales_whole_gap.py KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d6-mutant-07"] = fresh("E4d6-mutant-07", "PASS", "mutant_r6_07_unit_informativeness_discounted_by_cost.py KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d6-mutants-new-killed"] = fresh("E4d6-mutants-new-killed", "PASS", "All mutant_r6_0* in ledgers/E4/mutants KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d6-spec-variants-08-09"] = fresh("E4d6-spec-variants-08-09", "PASS", "The round-10 FAIL is resolved: project.html:318 states no stop rule, so the two stop-rule variants are output-equivalent on the stated requirement. Checked numerically (logs/check_accuracy_r11.txt): mutant_r6_08 worst |err|/tol = 1.6e-2 and mutant_r6_09 worst 5.6e-3 over 3009 domain cases, 0 failures; equivalent/README.md proof steps re-read (2^-200 = 6.2e-61; root >= 0.2 sigma when tau-bar >= 1e-2 since lambda* = 2 sigma sqrt(tb/(1-tb)) >= 0.201 sigma).")
R["E4d6-stop-rule-measured"] = carry("E4d6-stop-rule-measured", "grader/reference.py:22-23 and :138 (unchanged lines), ledgers/E4/alternatives/alt_5.py")
R["E4d6-alt-extra-damped"] = carry("E4d6-alt-extra-damped", "ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py (script unchanged)")
R["E4d6-rung1-why"] = carry("E4d6-rung1-why", "project.html:171 (Lab 1 interpretation)")
R["E4d7-midpoint-untested"] = fresh("E4d7-midpoint-untested", "PASS", "project.html:318 no longer states that the reported fraction is the midpoint or lies in the final bracket; the lower-end report variant (mutant_r7_01, equivalent/) is within the stated accuracy requirement (logs/check_accuracy_r11.txt, 1.6e-2 of tolerance worst case). No stated behaviour is violated.")
R["E4d7-cost-above-one-rejected"] = carry("E4d7-cost-above-one-rejected", "test_project.py:242-253 and project.html:326")
R["E4d7-noise-above-one-rejected"] = carry("E4d7-noise-above-one-rejected", "test_project.py:357-370")
R["E4d7-alt5-docstring"] = carry("E4d7-alt5-docstring", "ledgers/E4/alternatives/alt_5.py:1-2")
R["E4d7-lab1-bracket-width"] = carry("E4d7-lab1-bracket-width", "project.html:171 (Lab 1 interpretation)")
R["E4d7-lab2-blank"] = carry("E4d7-lab2-blank", "project.html:244 (Lab 2 interpretation)")
R["E4d7-instance-bound"] = carry("E4d7-instance-bound", "test_project.py instance tests, grader/instance.py:1-21, project.html:314")
R["E4d7-lab3-closed-form-sentence"] = fresh("E4d7-lab3-closed-form-sentence", "PASS", "project.html:376 (Lab 3 hypothesis) re-checked against the twin output: 'agrees with the closed form to within 1e-12' holds (largest difference 2.1e-13); gap at each point below 1e-13 (max 3.55e-14); 484 of 484 box points.")
R["E4d7-test-count"] = fresh("E4d7-test-count", "PASS", "project.html:320 says 43 checks; collect-only = 43 tests (logs/collect.txt); page_smoke in-browser 43 pass.")
R["E4d8-no-upper-bound"] = fresh("E4d8-no-upper-bound", "PASS", "project.html:326 (exception table) names no upper bound; reference.py _check_inputs (:26-34) checks only positivity, finiteness and nonnegativity; the page's 'up to 1e150 / 350' range is not a rejection rule (checked this round).")
R["E4d8-cap-100-survives"] = fresh("E4d8-cap-100-survives", "PASS", "mutant_r8_01_cap_100_halvings.py KILLED by test_tiny_noise_root_is_relatively_accurate[1e-30] (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d8-noise-cap-10-survives"] = fresh("E4d8-noise-cap-10-survives", "PASS", "mutant_r8_02_noise_above_ten_rejected.py KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d8-cost-cap-5-survives"] = fresh("E4d8-cost-cap-5-survives", "PASS", "mutant_r8_03_cost_above_five_rejected.py KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d8-mutants-r8-killed"] = fresh("E4d8-mutants-r8-killed", "PASS", "mutant_r8_04 and mutant_r8_05 KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d8-alternatives-r8"] = fresh("E4d8-alternatives-r8", "UNVERIFIABLE", "ledgers/E4/alternatives/alt_r8_a.py and alt_r8_b.py are absent at this pin (ls ledgers/E4/alternatives: alt_1 to alt_5 only). The round-8 claim about them cannot be read.", fix="Either restore alt_r8_a/b to ledgers/E4/alternatives at a pin, or drop the round-8 citation.")
R["E4d8-tiny-root-reference"] = fresh("E4d8-tiny-root-reference", "PASS", "reference.py solves tiny roots (sd 1e-50 to 1e-40) to relative 1e-8 or better: check_accuracy_r11.py worst case 5.6e-3 of tolerance (logs/check_accuracy_r11.txt).")
R["E4d8-lab3-twin-page"] = fresh("E4d8-lab3-twin-page", "PASS", "project.html Lab 3 block (:377-503) equals tests/labs/E4/lab-E4-project-3.py (logs/twin_compare_r11.txt: equal=True) after the round-11 edits at project.html:383 and :397 and the twin's lines 7 and 21.")
R["E4d9-mutant-v9-02"] = fresh("E4d9-mutant-v9-02", "PASS", "mutant_v9_02 is no longer in ledgers/E4/mutants (moved to ledgers/E4/equivalent/ at 11d7077; equivalent/README.md). Output-equivalent on the stated accuracy requirement: 0 failures in 3009 domain cases, worst 5.6e-3 of tolerance (logs/check_accuracy_r11.txt). Its status depends on the open plan conflict E4d11-plan-tolerance-documented.")
R["E4d9-mutant-v9-06"] = fresh("E4d9-mutant-v9-06", "PASS", "mutant_v9_06_gap_at_zero_from_tiny_fraction.py KILLED by test_gap_at_zero_fraction_is_the_limit_to_full_precision (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d9-equivalent-r6-08-09-docstrings"] = fresh("E4d9-equivalent-r6-08-09-docstrings", "PASS", "equivalent/README.md and the two files read; the round-10 docstrings are consistent with the code (reports lower end, always 200 halvings) and with the numeric check (logs/check_accuracy_r11.txt).")
R["E4d9-mutants-v9-killed"] = fresh("E4d9-mutants-v9-killed", "PASS", "mutant_v9_01, _03, _05, _07 KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d9-mutant-docstrings"] = fresh("E4d9-mutant-docstrings", "PASS", "All 84 files in ledgers/E4/mutants have a docstring and differ from grader/reference.py after the docstring (logs/mutant_docstrings_r11.txt: 'mutants: 84; problems: 0').")
R["E4d9-alternatives-v9"] = fresh("E4d9-alternatives-v9", "UNVERIFIABLE", "ledgers/E4/alternatives/alt_v9_1_interior_gap_zero.py, alt_v9_2_log_space.py, alt_v9_3_* are absent at this pin (ls ledgers/E4/alternatives: alt_1 to alt_5 only).", fix="Restore the round-9 alternatives at a pin or drop the citation.")
R["E4d-equivalent"] = fresh("E4d-equivalent", "PASS", "equivalent/README.md: proofs re-read. mutant_r6_08, r6_09, r7_01, v9_02 are within the stated accuracy requirement (logs/check_accuracy_r11.txt). literal_price_sign.py: its one edit (b_u sign) is read in exactly one squared expression (reference.py informed_term), so no output depends on it (README step 1-2, re-read). It is an architect open item, recorded as such in the README, not a surviving mutant.")
R["E4d-alternatives"] = fresh("E4d-alternatives", "PASS", "alt_1..alt_5 pass 50/50 seeds (logs/alternatives_seeds0-49_r11.txt); accuracy check worst 2.2e-3 of tolerance (logs/check_accuracy_r11.txt).")
R["E4d-starter"] = carry("E4d-starter", "grader/starter.py (unchanged)")
R["E4d4-alt4-wrong-on-small-noise"] = fresh("E4d4-alt4-wrong-on-small-noise", "PASS", "alt_4 (secant safeguarded) passes 50/50 seeds (logs/alternatives_seeds0-49_r11.txt) and the accuracy check (worst 7.7e-4 of tolerance, logs/check_accuracy_r11.txt): it is correct on small noise, not wrong.")
R["E4d4-alt1-docstring"] = fresh("E4d4-alt1-docstring", "PASS", "alt_1.py:1-3 docstring 'relative bracket width of 1e-12, or at most 200 halvings' matches line 80 'while hi - lo > 1e-12 * hi and halvings < 200'.")
R["E4d4-equivalent-price-slope"] = carry("E4d4-equivalent-price-slope", "ledgers/E4/scripts/E4-d-r4/check_equivalence_r4.py (script unchanged)")
R["E4d4-calibration-blind"] = fresh("E4d4-calibration-blind", "UNVERIFIABLE", "project.html:533-597 (Exemplar A): the same blind-scoring limit as E4d-exemplar-A-calibration; not scored by this verifier.", fix="A scorer who has not read the annotations scores Exemplar A.")
R["E4d4-proposed-test-validated"] = fresh("E4d4-proposed-test-validated", "PASS", "The small-noise and tiny-root tests (test_project.py:508-534) pass for reference.py and all six alternatives on seeds 0-49 (logs/ref_seeds_0_49_r11.txt, alternatives logs) and kill the r4 and r5 mutants (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d4-mutants-killed-r4"] = fresh("E4d4-mutants-killed-r4", "PASS", "All mutant_r4* in ledgers/E4/mutants KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d4-exemplar-B-results-numbers"] = fresh("E4d4-exemplar-B-results-numbers", "PASS", "project.html:629-641 numbers re-checked against the Lab 3 output (E4d-num-exemplar-table).")
R["E4d5-mutant-bracket-floor"] = fresh("E4d5-mutant-bracket-floor", "PASS", "mutant_r5_bracket_floor_1e-12.py KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d5-mutant-sixty-halvings"] = fresh("E4d5-mutant-sixty-halvings", "PASS", "mutant_r5_sixty_halvings_no_tolerance.py KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d5-mutant-uninformed-precision"] = fresh("E4d5-mutant-uninformed-precision", "PASS", "mutant_r5_uninformed_posterior_precision_informed.py KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d5-calibration-B-blind"] = fresh("E4d5-calibration-B-blind", "UNVERIFIABLE", "project.html:598-661 (Exemplar B): blind scoring not possible for this verifier (annotations read); not scored.", fix="A scorer who has not read the annotations scores Exemplar B.")
R["E4d2-mutants-r2"] = fresh("E4d2-mutants-r2", "PASS", "All mutant_r2_* in ledgers/E4/mutants KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d-mutants-existing"] = fresh("E4d-mutants-existing", "PASS", "Every pre-round-10 mutant in ledgers/E4/mutants KILLED by the seeds 0-9 gate; the only survivor is the new mutant_r10_02 (E4d11-mutant-r10-02).")
R["E4d-mutants-new"] = fresh("E4d-mutants-new", "PASS", "mutant_r7_02 and mutant_r7_03 KILLED (logs/mutate_graders_seeds0-9_r11_final.txt).")
R["E4d-mutants-total"] = fresh("E4d-mutants-total", "FAIL", "Final gate `tools/mutate_graders.py --unit E4 --seeds 0-9` (logs/mutate_graders_seeds0-9_r11_final.txt): 'mutate_graders E4: FAIL (83/84 killed)', exit 1. The one survivor is mutant_r10_02_cost_factor_relative_error.py (E4d11-mutant-r10-02).", fix="See E4d11-mutant-r10-02: a tighter interior-gap check kills it.")
R["E4d10-delta-A1-prior-mean"] = carry("E4d10-delta-A1-prior-mean", "project.html:257-262 (A1)")
R["E4d10-delta-inputs-interior-root"] = fresh("E4d10-delta-inputs-interior-root", "PASS", "project.html:314 (Inputs) unchanged; its numbers re-computed this round (E4d-num-box-bounds).")
R["E4d10-delta-constraints-gap-at-zero"] = fresh("E4d10-delta-constraints-gap-at-zero", "PASS", "project.html:318 gap-at-zero clause ('to within 1e-14 relative to the larger of 1 and |limit|') unchanged; test_project.py:384-395 checks it (reference passes; mutant_r10_01_gap_zero_offset_1e-13 KILLED).")
R["E4d10-delta-grading-mode-43"] = fresh("E4d10-delta-grading-mode-43", "PASS", "project.html:320 'runs 43 checks': collect-only 43 (logs/collect.txt).")
R["E4d10-delta-results-ratio"] = fresh("E4d10-delta-results-ratio", "PASS", "Exemplar B results ratios (project.html:629-641): 0.6978/0.5582 = 1.2501 (stated 1.25) and 0.8373/0.5582 = 1.5000 (stated 1.50), from the Lab 3 printed fractions; recomputed this round.")
R["E4d10-new-test-numbers"] = fresh("E4d10-new-test-numbers", "PASS", "The round-10 test count (43) and the test's numbers match the collect-only count and the page (E4d-cmd-collect, E4d7-test-count).")
R["E4d10-mutants-new-r10"] = fresh("E4d10-mutants-new-r10", "FAIL", "Of the seven mutant_r10_* files in ledgers/E4/mutants, six KILLED (logs/mutate_graders_seeds0-9_r11_final.txt); mutant_r10_02_cost_factor_relative_error.py SURVIVED.", fix="See E4d11-mutant-r10-02.")
R["E4d10-alternatives-r10"] = fresh("E4d10-alternatives-r10", "PASS", "alt_1..alt_5 50/50 seeds (logs/alternatives_seeds0-49_r11.txt); the round-10 alt_r10_a/b files are not at this pin's ledgers/E4/alternatives and are not re-cited here.")
R["E4d10-l06-dependency"] = carry("E4d10-l06-dependency", "L06.html:57 and :66 (CARA definition); L06 changed only at lines 51, 225, 602")
R["E4d10-lab3-numbers"] = fresh("E4d10-lab3-numbers", "PASS", "Lab 3 output re-run this round: all nine grid rows equal the page (0.5582/0.6978/0.8373; 0.1920/0.1420/0.0889), largest difference 2.1e-13.")

# ---- round-11 rows (new) ----
N = []
N.append(new("E4d11-delta-hunks", "delta-read", "project.html:316,318,383,397; test_project.py:499,515-533; reference.py:126; alt_1.py:1; tests/labs/E4/lab-E4-project-3.py:7,21; ledgers/E4/equivalent/README.md; mutant files moved", "PASS", "git diff -U0 00a84795 11d7077 over the slice: every hunk read (listed in this row's location). Hunks touch the Required outputs, Constraints, Lab 3 intro and TOLERANCE/MAX_HALVINGS comment on the page, the test docstrings and messages, and the stop-rule variant files. Round-10 mutant files r10_01..04 are new; mutant_v9_02 moved from mutants/ to equivalent/."))
N.append(new("E4d11-constraints-accuracy", "2.6-spec-vs-suite", "course/modules/E/E4/project.html:318; grader/test_project.py:343, :513-534", "PASS", "Requirement read as |lambda - root| <= min(1e-10, 1e-8*root) (the reading the suite implements; see E4d11-constraints-wording). Independent check ledgers/E4/scripts/E4-d-r11/check_accuracy_r11.py: reference.py 0 failures of 3009 domain cases (sd log-uniform 1e-50..1e3, tau-bar >= 1e-2, interior), worst 5.6e-3 of tolerance; boundary corners included. Alternatives alt_1..5 0 failures. The page states no requirement below tau-bar 1e-2 and no test there (only costs 0.13, 0.15 and the box are used by accuracy tests)."))
N.append(new("E4d11-constraints-wording", "2.2-prose-numbers", "course/modules/E/E4/project.html:318", "PASS", "'to within the smaller of 10^{-10} and 10^{-8} times the root' is ambiguous (min(1e-10, 1e-8 root) vs 1e-10 root). The suite implements min(1e-10, 1e-8*root). Recorded as a clarity note, not a defect: the stated form min(10^{-10}, 10^{-8} x root) would remove the ambiguity."))
N.append(new("E4d11-oracle-precision", "2.6-grader", "course/modules/E/E4/grader/test_project.py:79-170; reference.py", "PASS", "Measured (logs/oracle_gap_precision_r11.txt): max |reference gap - oracle gap| at lambda* over the 50 interior seeds = 3.331e-16, so the oracle is precise enough for a 1e-14 check."))
N.append(new("E4d11-mutants-new-r11", "2.6-mutants", "ledgers/E4/mutants/mutant_r11_01..04", "PASS", "Four new student-error mutants written by this verifier (make_mutants_r11.py): r11_01 price precision drops the square on a (killed by test_gap_is_the_oracle_gap_at_the_reported_fraction), r11_02 zero limit uses exp(-a c) (killed by test_info_cost_above_one_is_accepted), r11_03 fraction clipped to 1-1e-12 (killed by test_unit_fraction_is_reported_at_zero_cost), r11_04 informed mean drops the precision weight (killed on 50/50 seeds, logs/mutant_r11_04_seeds0-49.txt). A fifth draft (informed slope with tau_v in place of tau_e) was dropped: with the page's fixed tau_v = tau_e = 1 it is output-identical, so not a valid mutant."))
N.append(new("E4d11-alt-closed-form", "2.6-alternatives", "ledgers/E4/scripts/E4-d-r11/alts/alt_r11_a.py", "PASS", "Correct alternative written by this verifier: the interior fraction from the closed form of Proposition 4 (no bisection), with the boundary rule. 50/50 seeds (logs/alt_r11_a_seeds0-49.txt). Shows the suite does not over-constrain the method."))
N.append(new("E4d11-literal-price-sign-open", "2.2-math", "ledgers/E4/equivalent/literal_price_sign.py; project.html:276-283 (Proposition 1 sign)", "PASS", "Proof in the README re-read and confirmed: reference.py uses b_u only as b_u*b_u (informed_term) and as '_' in uninformed_term. It is an architect open item (Proposition 1's sign is not testable), recorded in the README; not a surviving grader mutant."))
N.append(new("E4d11-lab-page-twin", "2.5-labs", "project.html lab blocks vs tests/labs/E4/lab-E4-project-{1,2,3}.py", "PASS", "logs/twin_compare_r11.txt: lab 1 and lab 3 page code equal twins; lab 2 differs only by the blank (return of indifference_gap), as the completion rule requires. run_labs 12/12."))
N.append(new("E4d11-plan-tolerance-documented", "2.2-spec-vs-plan", "course/modules/E/E4/project.html:318; plans/E4-build-plan.md:389 and :182-184 (rule 12)", "FAIL", "project.html:318 now says 'any tolerance you use is a constant of your module, not an argument of the interface' and states no stop rule or tolerance for the solver. plans/E4-build-plan.md:389 requires 'The solver's bisection tolerance is a documented constant on the page'; plan rule 12 (:182-184) requires a bisection solver to state its bracket, tolerance, stop rule and sign-change assumption. The page states the bracket and the sign-change assumption, not the tolerance or stop rule.", fix="Architect ruling needed. Either restore a documented tolerance and stop rule in project.html Constraints (and then the lower-end stop variant in equivalent/ must be re-ruled under ruling 9), or amend plan :389 and rule 12 in writing. The verifier does not edit the plan."))
N.append(new("E4d11-mutant-r10-02", "2.6-grader", "ledgers/E4/mutants/mutant_r10_02_cost_factor_relative_error.py vs grader/test_project.py:312 (TOL_GAP 1e-8) and :384-395; project.html:318", "FAIL", "mutate_graders E4 seeds 0-9 SURVIVED mutant_r10_02_cost_factor_relative_error.py (logs/mutate_graders_seeds0-9_r11_final.txt). Its gap at lambda* is off by max 2.403e-13 from the reference on the 50 interior seeds (logs/survivor_size_r11.txt). The page states 'The solver works in floating point at full precision' (project.html:318); the suite's interior gap check uses TOL_GAP = 1e-8, far looser than full precision, while the gap at 0 is held to 1e-14.", fix="Add a test that the reported gap at an interior fraction agrees with the oracle gap to 1e-14*max(1,|oracle|). Checked in scratch: reference fails 0 of 50 interior seeds, the mutant fails 50 of 50 (logs/fix_check_r11.txt). Alternatively, state the precision of the interior gap on the page and test that number."))

rows = []
for rid in prev_ids:
    rows.append(R[rid])
LOCATION = {
    "E4d-mutants-total": "ledgers/E4/mutants/ (84 files at 11d7077)",
    "E4d10-mutants-new-r10": "ledgers/E4/mutants/mutant_r10_01..04 (7 files)",
    "E4d-exemplar-annotations-hidden": "course/assets/js/rubric.js:147-150; project.html reveal markup",
}
for row in rows:
    if row["id"] in LOCATION:
        row["location"] = LOCATION[row["id"]]
rows.extend(N)
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert set(prev_ids) <= set(ids), "round-10 ids missing"

# mutants from the final gate log
mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$")
for line in open(f"{LOG}/mutate_graders_seeds0-9_r11_final.txt", encoding="utf-8"):
    m = pat.match(line.strip())
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({"name": name, "description": desc, "killed_by": None if killed == "None" else killed,
                    "status": "KILLED" if status == "KILLED" else "SURVIVED"})
for name, desc in [
    ("literal_price_sign.py", "Price noise coefficient with the wrong sign; no output depends on it (architect open item)."),
    ("mutant_r6_08_reports_lower_end.py", "Reports the lower end of the final bracket; within the stated accuracy requirement."),
    ("mutant_r6_09_always_200_halvings.py", "Never stops early; within the stated accuracy requirement."),
    ("mutant_r7_01_reports_bracket_lower_end.py", "Reports the lower end of the bracket; within the stated accuracy requirement."),
    ("mutant_v9_02_stop_rule_relative_to_lower_end.py", "Stop rule measured from the lower end; within the stated accuracy requirement (moved from mutants/ at 11d7077)."),
]:
    mutants.append({"name": name, "description": desc, "killed_by": None, "status": "EQUIVALENT_RECORDED (ledgers/E4/equivalent)"})

fails = [r for r in rows if r["status"] == "FAIL"]
unver = [r for r in rows if r["status"] == "UNVERIFIABLE"]
passes = [r for r in rows if r["status"] == "PASS"]
verdict = "PASS" if not fails and not unver else "FAIL"
frag = {
    "unit": "E4",
    "slice": "d",
    "round": 11,
    "verifier": "Haiku independent verifier, E4 slice d, round 11 (did not build E4; fresh checkout at 11d7077)",
    "pin": "11d7077a290f7960b183d3a5a6631af4773888f9",
    "base": "00a84795f276456fce19d4181373cc4efba11a36 (round-10 pin). Delta in the slice: project.html 316, 318, 383, 397; test_project.py 499, 515-533; reference.py 126; alt_1.py 1; lab-E4-project-3 twin 7, 21; equivalent/README.md; mutants r10_01..04 added; mutant_v9_02 moved to equivalent/. Every hunk read.",
    "checkout": ROOT,
    "scratch": "scratch copies in /tmp (mktemp -d /tmp/e4d11-*), removed after use; scripts in ledgers/E4/scripts/E4-d-r11/",
    "verified_at": "2026-11-05T11:24:31+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Full read of the round-11 delta hunks; round-10 rows carried only when the cited lines are not in the hunks (the carry prefix names the lines). Whole-file rows re-run with commands or scripts this round.",
        "Gate: tools/mutate_graders.py --unit E4 --seeds 0-9 -> 83/84 killed, survivor mutant_r10_02_cost_factor_relative_error.py (E4d11-mutant-r10-02).",
        "Round-10 FAIL rows E4d3-spec-stop-rule-and-constraints, E4d6-spec-variants-08-09 and E4d9-mutant-v9-02 are resolved by the page's removal of the stop rule, verified numerically (logs/check_accuracy_r11.txt). Their status depends on E4d11-plan-tolerance-documented, which is a new FAIL.",
        "Calibration rows (Exemplars A and B) remain UNVERIFIABLE: this verifier has read the annotations, so no blind score is possible.",
        "Not checked: the Pyodide interpreter itself (page_smoke runs the in-browser suite through the repo tool); a live verify_refs run (offline only); the round-8 and round-9 alternative files, which are absent at this pin; the other slices' lesson files (L01-L05, L07-L09 changed at this pin, outside slice d).",
        "Mutants written by this round are in ledgers/E4/mutants (r11_01..04) and the closed-form alternative in ledgers/E4/scripts/E4-d-r11/alts/.",
    ],
    "summary": {"rows": len(rows), "pass": len(passes), "fail": len(fails), "unverifiable": len(unver),
                "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["status"] == "KILLED")},
}
out = f"{ROOT}/ledgers/E4/E4-d.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", out, frag["summary"], "verdict", verdict)
