"""Round 17: writes ledgers/E4/E4-d.json (E4 slice d, round 17) from the outputs under out/.

Every round-16 row id is kept (the rule is to keep all row ids). A row is FRESH when this round re-ran the command or
re-read the subject; it is CARRY when the subject is byte-identical since the round-16 pin 56cc575a (the carry prefix
names the subject). The project.html hunks of 56cc575a..700bf33f have pre-image lines 37, 42, 53, 57, 60-62, 171, 176,
179-181, 244, 522, 529 and 595-596; a carried row cites only lines outside them.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/E4/scripts/E4-d-r17"
OUT = f"{S}/out"
PREV = json.load(open("/Users/billyribeiro/.fanout/frags/E-E4-d.round16.json", encoding="utf-8"))
PREV_IDS = [r["id"] for r in PREV["rows"]]

PREFIX = "Carried from round 16 ({subject}; the grader/, references/references.json E4 records, notation/, course/assets/ and curriculum/ are byte-identical since 56cc575a): "
SUBJECT = {
    "model": "project.html model section lines 246-305, outside the hunks",
    "spec": "project.html spec section lines 307-335, outside the hunks",
    "hours": "project.html time-budget lines 337-354, outside the hunks",
    "reading": "project.html reading lines 679-686, outside the hunks",
    "exB": "project.html Exemplar B lines 598-661, outside the hunks",
    "lab3": "project.html Lab 3 block lines 373-503 and tests/labs/E4/lab-E4-project-3.py, outside the hunks",
    "grader": "course/modules/E/E4/grader/ (no delta)",
    "mut": "pre-existing files in ledgers/E4/mutants/ (no delta; four v17 files added)",
    "alt": "ledgers/E4/alternatives/ (no delta)",
    "equiv": "ledgers/E4/equivalent/ (no delta)",
    "reg": "references/references.json E4 records (no change to the muth1961rational or milgrom1982information entries)",
    "l06": "course/modules/E/E4/L06.html and L07.html (no delta)",
    "site": "course/assets/ (no delta)",
}

# Fresh rows: id -> (status, evidence)
FRESH = {
    "E4d-cmd-check-projects": ("PASS", f"{OUT}/check_projects.txt: 'check_projects E4: PASS', exit 0 (tools/check_projects.py --unit E4)."),
    "E4d-cmd-check-pages": ("PASS", f"{OUT}/check_pages.txt: 'check_pages E4: PASS', exit 0 (includes the banned-string scan)."),
    "E4d-cmd-check-dag": ("PASS", f"{OUT}/check_dag.txt: 'check_dag E4: PASS', exit 0."),
    "E4d-cmd-run-labs": ("PASS", f"{OUT}/run_labs.txt: 'run_labs E4: PASS (12/12)', exit 0."),
    "E4d-cmd-run-graders": ("PASS", f"{OUT}/run_graders_0_49.txt: 'run_graders E4: PASS (reference 50/50 seeds)', exit 0."),
    "E4d-cmd-page-smoke-project": ("PASS", f"{OUT}/page_smoke_project.txt: 'page_smoke E4: PASS', exit 0 (project page only)."),
    "E4d-cmd-ruff": ("PASS", f"{OUT}/ruff_check.txt 'All checks passed!' and {OUT}/ruff_format.txt '16 files already formatted', exit 0."),
    "E4d-cmd-mypy-workspace": ("PASS", f"{OUT}/mypy_workspace.txt: full .venv/bin/mypy 'Success: no issues found in 385 source files', exit 0."),
    "E4d-cmd-mypy-plan-command": ("PASS", f"{OUT}/mypy_e4.txt: mypy --no-incremental tests/labs/E4 course/modules/E/E4/grader 'Success: no issues found in 16 source files', exit 0."),
    "E4d-cmd-pytest-relevant": ("PASS", f"{OUT}/pytest_relevant_r17.txt: pytest on test_memo_exemplars.py, test_page_checks.py, test_labs.py, test_page_smoke.py, test_run_labs.py, exit 0."),
    "E4d-cmd-verify-refs": ("PASS", f"{OUT}/verify_refs_offline.txt '560 entries, 0 problems' (exit 0); {OUT}/verify_refs_E4_live.txt 'live re-verification of E4: 3 of 560 entries, 0 problems' (exit 0)."),
    "E4d-cmd-collect": ("PASS", f"{OUT}/collect_only_reference.txt: '48 tests collected' with reference.py installed as solver.py (ledgers/E4/scripts/E4-d-r17/collect_reference.sh). The bare collect (out/collect_only.txt) fails with ModuleNotFoundError: solver, because the suite imports solver by design."),
    "E4d-lab-project-1": ("PASS", f"{S}/twins_and_page_code.py (out/twins_and_page_code.txt): twin lab-E4-project-1 alone under python -I -W error: exit 0, stderr 0 bytes; page data-run block equals the twin; page expected block equals twin stdout (15 lines). Values checked by {S}/rederive_fixed_point.py (out/rederive_fixed_point.txt)."),
    "E4d-lab-project-2": ("PASS", f"{S}/twins_and_page_code.py (out/twins_and_page_code.txt): twin exit 0, stderr 0; page block differs from the twin only in the blanked return line (by design); expected block equals twin stdout (4 lines). Endpoints by {S}/endpoint_checks_r17.py (out/endpoint_checks_r17.txt)."),
    "E4d-lab-project-3": ("PASS", f"{S}/twins_and_page_code.py (out/twins_and_page_code.txt): twin exit 0, stderr 0; page code equals twin; expected block equals stdout (12 lines). The nine grid rows and the 484-of-484 box count re-derived by {S}/rederive_fixed_point.py and {S}/endpoint_checks_r17.py."),
    "E4d-num-lab-hypotheses": ("PASS", f"project.html:57 (Lab 1), :175 (Lab 2) and :375 (Lab 3) hypothesis values equal the twin outputs (out/twins_and_page_code.txt) and the independent fixed-point re-derivation (out/rederive_fixed_point.txt) and the endpoint script (out/endpoint_checks_r17.txt)."),
    "E4d-num-exemplar-table": ("PASS", f"project.html:629-641 (Exemplar B table): all nine rows equal out/rederive_fixed_point.txt; lambda* = 2 sigma sqrt(tau_bar/(1-tau_bar)) at (0.500, 0.120) gives 0.558180, shown as 0.5582; ratios 0.6978/0.5582 = 1.2501 and 0.8373/0.5582 = 1.5000; largest |gap| 3.55e-14 (< 4e-14)."),
    "E4d-num-box-bounds": ("PASS", f"project.html:313 (Inputs): tau_bar(0.150) = 0.09762327, tau_bar(0.120) = 0.23756678 and 1/(1+4*0.75^2) = 0.307692 (out/endpoint_checks_r17.txt); instance.py:7-8 draws; the 484-of-484 count is out/endpoint_checks_r17.txt."),
    "E4d-prose-lede-directional": ("PASS", "project.html:37 (lede, changed this round): the fraction rises with the noise at a fixed cost (Lab 3 rows 0.5582, 0.6978, 0.8373 at cost 0.120); the informativeness does not depend on the noise volume on the interior (0.1920 at three volumes); at a fixed fraction more noise lowers tau_y = lam^2 tau_e^2/(lam^2 tau_e + a^2 sd^2) and so Corr(v,p)^2 (Propositions 1 and 2)."),
    "E4d-spec-ladder": ("PASS", "project.html:42 (changed this round): 'Rungs 1 and 2 are short.' E4 is tier M (course/modules/E/E4/index.html:31 'Tier M'; curriculum/02-economics-finance-core.yaml). BUILDER_RULES.md:188-189 says rungs 1-2 are kept to the minimum from tier M upward; M6 and SC1 project.html:42 use the same 'short' wording. Rung 1 (one instance, six printed steps, annotated at :170) and rung 2 (one blank, :242) are minimal. The round-16 FAIL (at full length) is resolved."),
    "E4d16-tier-M-ladder-sister": ("PASS", "course/modules/M/M6/project.html:42 and course/modules/SC/SC1/project.html:42 read this round: 'Rungs 1 and 2 are short.'; E4 project.html:42 uses the same wording."),
    "E4d-prose-scope-words": ("PASS", f"{S}/static_checks_r17.py (out/static_checks_r17.txt) gives the counts per scope word (only 15, all 4, every 18, any 7, same 12, exactly 2, always 0, drives 0). The changed hits (lines 37, 53, 175, 242, 520-527, 593-606) are stated hypotheses, grid computations (out/rederive_fixed_point.txt) or exemplar text; 'the same in both labs' (:53) matches the constants in both twins and reference.py."),
    "E4d-prose-simulated-labs": ("PASS", "project.html:57, :175, :314, :375 and the lab docstrings (twins and page blocks) carry SIMULATED for the Lab 1, Lab 2 and Lab 3 instances."),
    "E4d-prose-simulated-exemplars": ("PASS", "project.html:533 (exemplar intro, outside the hunks): 'Two report excerpts on a SIMULATED instance'."),
    "E4d-banned-phrases": ("PASS", f"check_pages PASS (banned-string scan, out/check_pages.txt) and {S}/static_checks_r17.py (out/static_checks_r17.txt): banned-hits [] for for brevity, beyond the scope, details omitted, TODO, TBD, lorem, left as an exercise, you can add more, it is important to note, obviously, clearly, well known, experts agree, studies show, it can be shown, roughly, historically, and an ellipsis."),
    "E4d-process-words": ("PASS", f"{S}/static_checks_r17.py (out/static_checks_r17.txt): process-word hits [] for builder, verifier, ruling, architect, ledger, fragment, batch, slice, the agent in project.html; grader and lab files have no such text (grep this round)."),
    "E4d-dag-links": ("PASS", f"{OUT}/check_dag.txt 'check_dag E4: PASS'; concept targets L06 noisy-rational-expectations-equilibrium and L07 price-informativeness exist (grep this round); L06.html:66 is the CARA Definition 6.2 that project.html:257 and :53 cite."),
    "E4d-notation": ("PASS", f"notation/notation.json: symbols list (8 entries, incl. gamma_3, gamma_4, R^ast, R^{{e ast}}, mathbb{{Q}}) has 0 hits on the page; the custom macros the page uses (Corr, Cov, E, Normal, Var) are all in the macros registry (out/static_checks_r17.txt). F_U, F_I, tau_bar and lambda^* are defined on the page (:251, :265-297)."),
    "E4d13-notation": ("PASS", f"{S}/static_checks_r17.py (out/static_checks_r17.txt), as E4d-notation."),
    "E4d-rubric-observable": ("PASS", "project.html:520-527 (changed this round): C5 level 1 'Names no limit of the model; hedges only with general remarks such as results may vary.' and level 2 'Names one or two specific assumptions of the model, for example the exponential utility or the exogenous noise supply, as limits.' Both have observable tests (a named limit or not; a named example). The round-16 'caveats' descriptor is gone; the blind C5 score of Exemplar A under these descriptors is 1 (out/blind_scores_r17.txt)."),
    "E4d-exemplar-B-calibration": ("PASS", f"Blind text-only scores of Exemplar B (stripped copy by {S}/strip_exemplars.py; record {OUT}/blind_scores_r17.txt): C1 4, C2 4, C3 4, C4 4, C5 4. Official at project.html:602 and annotations :610, :621, :646-647, :658: 4,4,4,4,4. Exact on every criterion. Exemplar B's annotations were not displayed to the verifier before the blind scores were recorded (disclosure in the record file)."),
    "E4d5-calibration-B-blind": ("PASS", f"Same as E4d-exemplar-B-calibration: blind 4,4,4,4,4 against official 4,4,4,4,4 ({OUT}/blind_scores_r17.txt)."),
    "E4d15-exemplar-verdicts": ("PASS", "project.html:535 data-scores 2,2,1,2,1 and :600 data-scores 4,4,4,4,4 agree with the annotation levels (A: :545 2, :546 3, :557 2, :558 3, :569 2, :570 3, :581 1, :582 2, :593 1, :594 2; B: :610 4, :621 4, :646 4, :647 4, :658 4) and with the verdict paragraphs :537 and :602."),
    "E4d-exemplar-A-calibration": ("UNVERIFIABLE", f"Blind text-only scores of Exemplar A: C1 2, C2 2, C3 1, C4 2, C5 1 (record {OUT}/blind_scores_r17.txt), equal to the official 2,2,1,2,1 (project.html:535, :537). NOT CLEAN: the first version of the stripper let one read print Exemplar A's annotation lines before blind scoring (disclosed in the record). Fix: a fresh verifier re-scores Exemplar A blind with strip_exemplars.py run first and no annotation read."),
    "E4d4-calibration-blind": ("UNVERIFIABLE", "Same as E4d-exemplar-A-calibration: Exemplar A blind scoring is contaminated this round by the disclosed read. Fix: clean blind re-score of Exemplar A."),
    "E4d-mutants-existing": ("PASS", f"tools/mutate_graders.py --unit E4 --seeds 0-9 ({OUT}/mutate_graders_E4_0_9_r17.txt): all 130 pre-existing mutants KILLED; the one survivor is the new mutant_v17_02 (row E4d17-mutant-v17-02)."),
    "E4d-mutants-new": ("PASS", f"mutant_r7_02_rejects_noise_above_one.py and mutant_r7_03_rejects_cost_above_one.py: KILLED in {OUT}/mutate_graders_E4_0_9_r17.txt."),
    "E4d-mutants-total": ("FAIL", f"{OUT}/mutate_graders_E4_0_9_r17.txt: 'mutate_graders E4: FAIL (133/134 killed)', exit 1. Survivor: mutant_v17_02_price_slope_drops_uninformed_term.py (row E4d17-mutant-v17-02)."),
    "E4d15-cmd-mutate": ("FAIL", f"tools/mutate_graders.py --unit E4 --seeds 0-9 exits 1 this round (133/134 killed, {OUT}/mutate_graders_E4_0_9_r17.txt). Fix: see E4d17-mutant-v17-02."),
    "E4d9-mutant-docstrings": ("PASS", f"Every ledgers/E4/mutants/*.py (134 files) has a first docstring line that describes the error; tools/mutate_graders.py prints it for each mutant ({OUT}/mutate_graders_E4_0_9_r17.txt)."),
    "E4d-equivalent": ("PASS", f"ledgers/E4/equivalent/: literal_price_sign.py, mutant_r6_08_reports_lower_end.py, mutant_r7_01_reports_bracket_lower_end.py, mutant_v9_02_stop_rule_relative_to_lower_end.py: each 50/50 on seeds 0-49 via {S}/run_candidate_r17.py ({OUT}/cand/eq_*.txt). Not counted in mutants/."),
    "E4d-alternatives": ("PASS", f"ledgers/E4/alternatives/alt_1.py..alt_8.py: each 50/50 on seeds 0-49 ({OUT}/cand/alt_*.txt, {S}/run_candidate_r17.py with the suite from course/modules/E/E4/grader); reference.py 50/50 ({OUT}/cand/reference.txt)."),
    "E4d16-alt-sweep": ("PASS", f"{OUT}/cand/alt_1.txt..alt_8.txt: 50/50 each this round."),
    "E4d15-alternatives-sweep": ("PASS", f"alt_1..alt_8 50/50 and the four equivalents 50/50 ({OUT}/cand/)."),
    "E4d13-candidates-accepted": ("PASS", f"{OUT}/cand/alt_*.txt and eq_*.txt: all accepted 50/50 this round."),
    "E4d-runtime": ("PASS", f"{OUT}/page_smoke_project.txt 'page_smoke E4: PASS' (tools/page_smoke.py: zero console errors, math rendered, no external requests for the project page); {OUT}/run_graders_0_49.txt."),
    "E4d-browser-local-parity": ("PASS", f"{OUT}/page_smoke_project.txt (browser side) and {OUT}/run_graders_0_49.txt (local pytest side, same suite and flags, tools/run_graders.py); {OUT}/pytest_relevant_r17.txt."),
    "E4d3-anchors-links": ("PASS", f"{S}/static_checks_r17.py (out/static_checks_r17.txt): 12 in-page hrefs, missing []; index.html:66 id=placement exists (grep this round)."),
    "E4d13-links": ("PASS", f"{S}/static_checks_r17.py (out/static_checks_r17.txt): no missing in-page anchor in course/modules/E/E4/project.html."),
    "E4d13-hours-arithmetic": ("PASS", "project.html:343-349 component hours 1+1+5+8+5+5+3 = 28 = data-hours-project (:33) = eyebrow (:35) = hub split (index.html:29)."),
    "E4d3-spec-stop-rule-and-constraints": ("FAIL", "project.html:317 (Constraints) states the gap-at-0 and interior-gap accuracy of 1e-14 relative to max(1,|value|); the stop rule (1e-12 times the upper end, at most 240 halvings) is implemented as stated (reference.py:138-139, the stop test and its halving cap; constants at :21-22). The gap clause is not tested at its stated precision: test_project.py:251, :312, :377 use TOL_GAP = 1e-8. Fix: see E4d17-gap-tolerance-constraint."),
    "E4d16-constraints-any-sentence": ("FAIL", "Every sentence of project.html:317 checked: the stop rule, bracket, tolerance, accuracy for noise >= 1e-50 and tau_bar >= 1e-2 (E4d11-constraints-accuracy), boundary rule, exception names, and display rule hold; the two gap-precision clauses are tested at 1e-8, not 1e-14 (test_project.py:251, :312, :377). Fix: see E4d17-gap-tolerance-constraint."),
    "E4d10-delta-constraints-gap-at-zero": ("FAIL", "project.html:317 gap-at-zero clause (to within 1e-14 relative to max(1,|limit|)) is tested by test_project.py:251 and :377 at TOL_GAP = 1e-8. Fix: see E4d17-gap-tolerance-constraint."),
    "E4d17-placeholder": ("PASS", "unused"),
}
FRESH.pop("E4d17-placeholder")

# Carry rows: id -> (subject key, note about what is relied on)
CARRY = {
    "E4d-hours-estimate": None,
    "E4d16-hours-band": ("hours", "the hours band and the component table are unchanged"),
    "E4d-spec-questions": None,
    "E4d10-delta-inputs-interior-root": ("spec", "project.html:313 Inputs paragraph (interior root on the box)"),
    "E4d10-delta-grading-mode-43": ("spec", "project.html:319 grading mode: 48 checks and the rubric bar (collect count 48 is FRESH above)"),
    "E4d11-constraints-accuracy": ("spec", "project.html:317 accuracy clauses for lambda* (1e-10 for noise >= 1e-50 and tau_bar >= 1e-2) and the corner test in grader/test_project.py"),
    "E4d11-constraints-wording": ("spec", "project.html:317 wording (no function prints or warns; the report displays every number at the brief's precision)"),
    "E4d11-plan-tolerance-documented": ("spec", "project.html:317 documents the 1e-12 stop tolerance and 240 halvings (matches reference.py:23-24)"),
    "E4d12-bisection-assumption": ("spec", "project.html:317 'the sign-change assumption' clause"),
    "E4d13-extreme-inputs": ("spec", "project.html:325-327 exception table and range paragraph"),
    "E4d15-range-extremes": ("spec", "project.html:325-327 exception range paragraph"),
    "E4d12-tiny-noise-informativeness": ("spec", "project.html:325-326 range text on tiny noise and grader/reference.py"),
    "E4d8-no-upper-bound": ("spec", "project.html:325 (no upper bound named) and grader/reference.py:122-151"),
    "E4d7-instance-bound": ("spec", "project.html:313-314 and grader/instance.py:1-37"),
    "E4d7-midpoint-untested": ("spec", "project.html:317 (midpoint clause) and ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py"),
    "E4d6-stop-rule-measured": ("grader", "grader/reference.py:22-23 and the stop-rule measurements in ledgers/E4/equivalent/README.md"),
    "E4d8-tiny-root-reference": ("grader", "grader/reference.py (solve_model) and the corner suite"),
    "E4d7-cost-above-one-rejected": ("grader", "grader/test_project.py test_info_cost_above_one_is_accepted (passes on the reference, 50/50)"),
    "E4d7-noise-above-one-rejected": ("grader", "grader/test_project.py test_noise_volume_far_above_one_is_accepted"),
    "E4d7-test-count": ("spec", "project.html:319 '48 checks' with the fresh collect count 48 (E4d-cmd-collect)"),
    "E4d10-new-test-numbers": ("grader", "grader/test_project.py docstrings that carry numbers"),
    "E4d11-oracle-precision": ("grader", "grader/test_project.py:79-170 oracle functions"),
    "E4d11-mutant-r10-02": ("mut", "ledgers/E4/mutants/mutant_r10_02_cost_factor_relative_error.py vs grader/test_project.py; killed this round (out/mutate_graders_E4_0_9_r17.txt)"),
    "E4d-grader-exceptions": ("grader", "grader/test_project.py exception tests and reference.py:26-34"),
    "E4d-grader-messages": ("grader", "grader/test_project.py every expect() message"),
    "E4d-grader-oracle": ("grader", "grader/test_project.py:79-170 oracle (agreement with the reference at interior fractions 3.3e-16, out/oracle_gap_precision.txt)"),
    "E4d-grader-instances": ("grader", "grader/instance.py and test_project.py:37-40"),
    "E4d-grader-instance-docstring": ("grader", "grader/instance.py:1-21 docstring"),
    "E4d-grader-test-docstring": ("grader", "grader/test_project.py docstrings"),
    "E4d-grader-reference-docstring": ("grader", "grader/reference.py:1-13 module docstring and :21-23 constant comments"),
    "E4d-grader-stdlib": ("grader", "grader/test_project.py standard-library test (suite passes 50/50)"),
    "E4d4-proposed-test-validated": ("grader", "grader/test_project.py small-noise and corner tests"),
    "E4d16-instances-20": ("grader", "grader/instance.py draws (seeds 0-49 run 50/50, out/run_graders_0_49.txt)"),
    "E4d13-instances-seeds-0-49": ("grader", "grader/instance.py and test_project.py:37 (seeds 0-49 run 50/50)"),
    "E4d-starter": ("grader", "grader/starter.py"),
    "E4d12-corner-test-docstring": ("grader", "grader/test_project.py:555-558 docstring"),
    "E4d13-endpoint-gap-precision": ("grader", "grader/test_project.py:419-450 endpoint tests (pass 50/50)"),
    "E4d15-grader-docstring-scale": ("grader", "grader/test_project.py:402-405 docstring vs code"),
    "E4d14-corner-scan": ("grader", "grader/reference.py and the corner scan record of round 14 (no change to the code under test)"),
    "E4d14-accuracy-sweep": ("grader", "grader/reference.py and the accuracy record of round 14 (no change to the code under test)"),
    "E4d12-prose-2pow240": ("grader", "grader/reference.py:23 and ledgers/E4/equivalent/literal_price_sign.py"),
    "E4d13-accuracy-sweep": ("grader", "grader/reference.py and project.html:317 (no change)"),
    "E4d10-delta-results-ratio": ("lab3", "project.html:628 exemplar B results ratios (lines outside the hunks; numbers re-derived this round)"),
    "E4d10-lab3-numbers": ("lab3", "Lab 3 printed numbers and twin tests/labs/E4/lab-E4-project-3.py (run this round)"),
    "E4d8-lab3-twin-page": ("lab3", "Lab 3 page block and twin (run this round, FRESH in E4d-lab-project-3)"),
    "E4d4-exemplar-B-results-numbers": ("exB", "project.html:628-641 Exemplar B results and table"),
    "E4d12-exemplar-B-sigma": ("exB", "project.html:607 Exemplar B Model passage (sigma)"),
    "E4d13-exemplar-numbers-arith": ("exB", "project.html:628-641 Exemplar B table and ratios (numbers re-derived this round)"),
    "E4d16-exemplar-B-claims": ("exB", "project.html:627-661 Exemplar B claims (numbers re-derived this round)"),
    "E4d2-exemplar-B-C1-annotation": ("exB", "project.html:610 annotation for B C1 (lines outside the hunks)"),
    "E4d-exemplar-annotations-hidden": ("site", "project.html reveal markup (data-reveal, :537, :602) and course/assets JS/CSS (no delta)"),
    "E4d-registry-muth": ("reg", "project.html:685 and references/references.json muth1961rational record (verify_refs offline and live E4 PASS this round)"),
    "E4d-registry-milgrom": ("reg", "project.html:686 and references/references.json milgrom1982information record (verify_refs PASS this round)"),
    "E4d-cites-only-registry": ("reading", "project.html:681-686 reading list (data-cite muth1961rational, milgrom1982information)"),
    "E4d15-reading-and-citations": ("reading", "project.html:681-686 reading list and references/references.json E4 records"),
    "E4d15-plan-and-rulings": ("reading", "plans/E4-build-plan.md and plans/FINAL-ARCHITECT-RULINGS.md (rulings 15-18 unchanged; the delta adds rulings 19-20 for M7 only)"),
    "E4d3-atlas-studios-na": ("spec", "project.html (no atlas or studio requirement) and curriculum/02-economics-finance-core.yaml E4 entry (no delta)"),
    "E4d3-no-figures-no-data": ("spec", "project.html has no figure or dataset element (grep this round showed no svg, img or data-files attribute)"),
    "E4d3-cara-defined-twice": ("model", "project.html:257 (A3) is the only definition on the page; the rungs paragraph (:53, changed) gives a forward reference to Definition 6.2 of L06, which is confirmed at course/modules/E/E4/L06.html:66"),
    "E4d10-l06-dependency": ("l06", "course/modules/E/E4/L06.html:57, :66, :169 and L07.html:62 (no delta)"),
    "E4d11-literal-price-sign-open": ("model", "project.html model section (A1-A6, Lemmas 1-3, Propositions 1-5) and ledgers/E4/equivalent/literal_price_sign.py"),
    "E4d-math-lemmas": ("model", "project.html:265-272 (Lemmas 1-3); independently re-derived in out/rederive_fixed_point.txt (Propositions 1, 3, 4 numbers)"),
    "E4d-math-prop1": ("model", "project.html:275-285 (Proposition 1 and its proof); b_u/b_s and tau_y verified by out/rederive_fixed_point.txt (bu/bs -3.45199422 at lam 0.57937525)"),
    "E4d-math-prop2": ("model", "project.html:284-285 (Proposition 2); informativeness 0.15898618 verified by out/rederive_fixed_point.txt"),
    "E4d-math-prop3": ("model", "project.html:287-292 (Proposition 3); the sign rule and G(0+) verified by out/rederive_fixed_point.txt and endpoint_checks_r17.py"),
    "E4d-math-prop4": ("model", "project.html:294-297 (Proposition 4); closed form 0.5582 at (0.500, 0.120) verified by out/rederive_fixed_point.txt"),
    "E4d-math-prop5": ("model", "project.html:299-300 (Proposition 5); proportionality of lambda* in sigma verified by the Lab 3 grid (out/rederive_fixed_point.txt)"),
    "E4d-math-assumptions": ("model", "project.html:253-261 (A1-A6)"),
    "E4d13-independent-rederivation": ("model", "independent fixed-point re-derivation this round (FRESH evidence in E4d17-independent-rederivation)"),
    "E4d11-lab-page-twin": ("lab3", "Lab 1 and Lab 2 page blocks equal the twins (FRESH this round in E4d-lab-project-1 and -2); Lab 3 block unchanged"),
    "E4d13-lab-twins-direct": ("lab3", "twin runs this round (out/twins_and_page_code.txt)"),
    "E4d6-rung1-why": ("model", "project.html:170 Lab 1 interpretation (changed this round) re-read: each step's reason matches the printed step"),
    "E4d7-lab1-bracket-width": ("model", "project.html:170 sentence about the bracket width 2^-53 at the 53rd halving: out/bracket_width_check.txt (width 1.1102e-16 from halving 53, ends adjacent) confirms it"),
    "E4d7-lab2-blank": ("model", "project.html:242 'Only the blank changes' (changed this round); the page code differs from the twin only in the blank line (out/twins_and_page_code.txt)"),
    "E4d10-delta-A1-prior-mean": ("model", "project.html:255 (A1) outside the hunks"),
    "E4d11-delta-hunks": ("spec", "project.html:313-320 and grader/test_project.py:401-418, :534-553 (no change since round 16 beyond the hunks listed)"),
    "E4d12-equivalent-readme-numbers": ("equiv", "ledgers/E4/equivalent/README.md stop-rule numbers"),
    "E4d13-readme-corner-domain": ("equiv", "ledgers/E4/equivalent/README.md 'Stop-rule variants' paragraph 2"),
    "E4d15-stop-rule-variants-architect": ("equiv", "ledgers/E4/equivalent/README.md 'Stop-rule variants' open item"),
    "E4d15-literal-price-sign": ("equiv", "ledgers/E4/equivalent/literal_price_sign.py (50/50 this round)"),
    "E4d14-equivalent-literal-3000": ("equiv", "ledgers/E4/equivalent/literal_price_sign.py"),
    "E4d4-equivalent-price-slope": ("equiv", "ledgers/E4/equivalent/literal_price_sign.py and its check script"),
    "E4d16-equiv-bitwise": ("equiv", "ledgers/E4/equivalent/literal_price_sign.py bitwise record"),
    "E4d16-equiv-ruling17-numeric": ("equiv", "ledgers/E4/equivalent/README.md ruling-17 numeric record"),
    "E4d6-spec-variants-08-09": ("equiv", "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py and the moved mutant_r6_09 record"),
    "E4d9-equivalent-r6-08-09-docstrings": ("equiv", "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py docstring"),
    "E4d4-alt1-docstring": ("alt", "ledgers/E4/alternatives/alt_1.py docstring (alt_1 50/50 this round)"),
    "E4d4-alt4-wrong-on-small-noise": ("alt", "ledgers/E4/alternatives/alt_4.py (50/50 this round)"),
    "E4d7-alt5-docstring": ("alt", "ledgers/E4/alternatives/alt_5.py docstring (50/50 this round)"),
    "E4d13-alternatives-plan-list": ("alt", "ledgers/E4/alternatives/alt_4.py and alt_5.py docstrings (50/50 this round)"),
    "E4d10-alternatives-r10": ("alt", "ledgers/E4/alternatives/alt_1..alt_5 (50/50 this round)"),
    "E4d12-alt-variants-new": ("alt", "ledgers/E4/alternatives/alt_6..alt_8 (50/50 this round)"),
    "E4d11-alt-closed-form": ("alt", "ledgers/E4/scripts/E4-d-r11/alts/alt_r11_a.py (exists in the checkout) and alt_1..8"),
    "E4d6-alt-extra-damped": ("alt", "ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py (exists in the checkout)"),
    "E4d8-alternatives-r8": ("alt", "the round-8 alt_r8_a.py and alt_r8_b.py are RETIRED under ruling 18 and absent from the checkout (checked this round); the candidate set that stands now is alt_1..alt_8, which pass 50/50 this round"),
    "E4d9-alternatives-v9": ("alt", "the round-9 alt_v9_* files are RETIRED under ruling 18 and absent from the checkout (checked this round); the candidate set that stands now is alt_1..alt_8, which pass 50/50 this round"),
    "E4d4-mutants-killed-r4": ("mut", "ledgers/E4/mutants/mutant_r4*.py, killed this round"),
    "E4d5-mutant-bracket-floor": ("mut", "ledgers/E4/mutants/mutant_r5_bracket_floor_1e-12.py, killed this round"),
    "E4d5-mutant-sixty-halvings": ("mut", "ledgers/E4/mutants/mutant_r5_sixty_halvings_no_tolerance.py, killed this round"),
    "E4d5-mutant-uninformed-precision": ("mut", "ledgers/E4/mutants/mutant_r5_uninformed_posterior_precision_informed.py, killed this round"),
    "E4d6-mutant-06": ("mut", "ledgers/E4/mutants/mutant_r6_06_cost_scales_whole_gap.py, killed this round"),
    "E4d6-mutant-07": ("mut", "ledgers/E4/mutants/mutant_r6_07_unit_informativeness_discounted_by_cost.py, killed this round"),
    "E4d6-mutants-new-killed": ("mut", "ledgers/E4/mutants/mutant_r6_0*.py, killed this round"),
    "E4d6-spec-variants-08-09-placeholder": None,
    "E4d7-alt5-docstring-placeholder": None,
    "E4d8-cap-100-survives": ("mut", "ledgers/E4/mutants/mutant_r8_01_cap_100_halvings.py, killed this round; project.html:318 states the 240 halvings"),
    "E4d8-noise-cap-10-survives": ("mut", "ledgers/E4/mutants/mutant_r8_02_noise_above_ten_rejected.py, killed this round"),
    "E4d8-cost-cap-5-survives": ("mut", "ledgers/E4/mutants/mutant_r8_03_cost_above_five_rejected.py, killed this round"),
    "E4d8-mutants-r8-killed": ("mut", "ledgers/E4/mutants/mutant_r8_04_*.py and mutant_r8_05_*.py, killed this round"),
    "E4d9-mutant-v9-02": ("equiv", "ledgers/E4/equivalent/mutant_v9_02_stop_rule_relative_to_lower_end.py (50/50 this round)"),
    "E4d9-mutant-v9-06": ("mut", "ledgers/E4/mutants/mutant_v9_06_gap_at_zero_from_tiny_fraction.py, killed this round"),
    "E4d9-mutants-v9-killed": ("mut", "ledgers/E4/mutants/mutant_v9_01, _03, _05, _07 (killed this round)"),
    "E4d10-mutants-new-r10": ("mut", "ledgers/E4/mutants/mutant_r10_01..04, killed this round"),
    "E4d11-mutants-new-r11": ("mut", "ledgers/E4/mutants/mutant_r11_01..04, killed this round"),
    "E4d12-mutant-gap-stop": ("mut", "ledgers/E4/mutants/mutant_r12_04_stops_when_midpoint_gap_is_tiny.py, killed this round"),
    "E4d13-new-mutants": ("mut", "ledgers/E4/mutants/mutant_r13_01..05, killed this round"),
    "E4d13-mutant-gate-final": ("mut", "ledgers/E4/mutants/ pre-existing files (killed this round)"),
    "E4d14-mutants-r14-new": ("mut", "ledgers/E4/mutants/mutant_r14_01..05, killed this round"),
    "E4d15-mutants-single-change": ("mut", "ledgers/E4/mutants/*.py pre-existing files, each killed this round"),
    "E4d15-mutants-new-r15": ("mut", "ledgers/E4/mutants/mutant_r15_01..04, killed this round"),
    "E4d2-mutants-r2": ("mut", "ledgers/E4/mutants/mutant_r2_*.py, killed this round"),
    "E4d3-mutants-r3": ("mut", "ledgers/E4/mutants/mutant_r3_*.py, killed this round"),
    "E4d3-mutant-tolerance-survives": ("mut", "ledgers/E4/mutants/mutant_r3_tolerance_1e-9.py, killed this round"),
    "E4d4-mutants-killed-r4-placeholder": None,
    "E4d-mutants-placeholder": None,
    "E4d16-mutants-ast-profile": ("mut", "ledgers/E4/mutants/ pre-existing files: each differs from reference.py in one code unit (round-16 profile); the four v17 files were profiled by diff this round (one line each)"),
    "E4d16-mutants-v16-new": ("mut", "ledgers/E4/mutants/mutant_v16_01..04, killed this round (see mutants list)"),
    "E4d12-mutant-gap-stop-placeholder": None,
    "E4d14-mutants-placeholder": None,
    "E4d16-alt-sweep-placeholder": None,
}
for k in [k for k, v in CARRY.items() if v is None or k.endswith("placeholder")]:
    CARRY.pop(k)

CARRY["E4d7-lab3-closed-form-sentence"] = ("lab3", "project.html:502 interpretation (closed-form column is Proposition 4) and the Lab 3 hypothesis at :375, outside the hunks")
FRESH["E4d14-delta-read"] = ("PASS", "Delta since the round-16 pin 56cc575a read this round for slice d: git diff 56cc575a 700bf33f on project.html (hunks at pre-image lines 37, 42, 53, 57, 60-62, 171, 176, 179-181, 244, 522, 529, 595-596), tests/labs/E4/lab-E4-project-1.py and -2.py (docstrings only), ledgers/E4/mutants v16_01..04 (added), ledgers/E4/alternatives and equivalent (no delta), grader/ (no delta), references/references.json (E4 records unchanged), plans/FINAL-ARCHITECT-RULINGS.md (rulings 19-20 added, not E4). Full slice diff saved at ledgers/E4/scripts/E4-d-r17/out/delta_slice.diff.")

CARRY["E4d-hours-estimate"] = ("hours", "the round-16 estimate (23 h against 28 h, 18% below, inside the 30% bar) is not re-estimated this round; the component table and the grader are unchanged")
CARRY["E4d-spec-context-sentences"] = ("spec", "project.html:311 Context paragraph")
CARRY["E4d-spec-questions"] = ("spec", "project.html:313-321 (Inputs, Required outputs, Constraints, Grading mode, Reading list); the Constraints clause on the gap tolerance is a separate FAIL row E4d17-gap-tolerance-constraint")
CARRY["E4d-hours-project"] = ("hours", "project.html:33 and :35 (eyebrow and data-hours-project) and the time table lines 341-352")

LOC_OVERRIDE = {
    "E4d-spec-ladder": "course/modules/E/E4/project.html:42",
    "E4d-rubric-observable": "course/modules/E/E4/project.html:520-527 (#rubric)",
    "E4d-exemplar-A-calibration": "course/modules/E/E4/project.html:535-598 (Exemplar A)",
    "E4d4-calibration-blind": "course/modules/E/E4/project.html:535-598 (Exemplar A)",
    "E4d-exemplar-B-calibration": "course/modules/E/E4/project.html:600-662 (Exemplar B)",
    "E4d5-calibration-B-blind": "course/modules/E/E4/project.html:600-662 (Exemplar B)",
    "E4d-mutants-total": "ledgers/E4/mutants/ (134 files)",
    "E4d15-cmd-mutate": "tools/mutate_graders.py --unit E4 --seeds 0-9",
    "E4d3-spec-stop-rule-and-constraints": "course/modules/E/E4/project.html:317 (Constraints); grader/test_project.py:251, :312, :377",
    "E4d16-constraints-any-sentence": "course/modules/E/E4/project.html:317 (Constraints)",
    "E4d10-delta-constraints-gap-at-zero": "course/modules/E/E4/project.html:317; grader/test_project.py:251, :377",
    "E4d-prose-lede-directional": "course/modules/E/E4/project.html:37 (lede)",
    "E4d-num-lab-hypotheses": "course/modules/E/E4/project.html:57, :175, :375",
    "E4d-lab-project-2": "course/modules/E/E4/project.html:173-243 #lab-E4-project-2; tests/labs/E4/lab-E4-project-2.py",
}

# Round-17 new rows
NEW = {
    "E4d17-mutant-v17-02": ("mutant_v17_02_price_slope_drops_uninformed_term", "FAIL", "ledgers/E4/mutants/mutant_v17_02_price_slope_drops_uninformed_term.py:57 (b_s = lam tau_e / denominator); project.html:276 (Proposition 1 b_s formula)",
        "Surviving student-error mutant (price slope b_s omits the (1-lam) tau_y term). Survives seeds 0-9 (out/mutate_graders_E4_0_9_r17.txt: SURVIVED) and seeds 0-49 (run_candidate_r17.py: 50/50 pass). Interface effect measured: solve_model equals the reference except at 2 of 14400 grid points (out/search_v17_02_gap_diff.txt), where lambda* differs at 1e-12 relative and the largest reported-gap difference is 7.6e-14 at (sd 0.66975, cost 0.12437); at that point the mutant's reported gap is within 1.7e-15 of the Proposition 3 gap at its own fraction (ledgers/E4/scripts/E4-d-r17/mutant_v17_02_probe.py, out/mutant_v17_02_probe.txt). So the mutant meets the page's stated interface tolerances (lambda* to 1e-10 relative; gap to 1e-14 at the reported fraction, project.html:317) and no test can separate it at those tolerances.",
        "Architect decision (ruling-9 path, as for literal_price_sign.py): either accept mutant_v17_02 as equivalent within the page's stated precision and move it to ledgers/E4/equivalent/ with this proof, or make the page state an output that depends on b_s at finer than 1e-12 and add a test. Until one is done the mutants gate reads 133/134."),
    "E4d17-mutants-new-killed": (None, "PASS", "ledgers/E4/mutants/mutant_v17_01_zero_limit_drops_tau_e_over_tau_v.py, mutant_v17_03_informed_term_reads_price_at_one.py, mutant_v17_04_uninformed_slope_divides_by_prior.py",
        "Three of the four new round-17 student-error mutants are KILLED: v17_01 by test_info_cost_above_one_is_accepted (seed 0); v17_03 by test_indifference_holds_at_an_interior_fraction[first] (seed 0); v17_04 by test_gap_is_the_oracle_gap_at_the_reported_fraction[first] (seed 0) (out/mutate_graders_E4_0_9_r17.txt). Each is one changed line of reference.py (diff checked this round)."),
    "E4d17-gap-tolerance-constraint": (None, "FAIL", "course/modules/E/E4/grader/test_project.py:44 (TOL_GAP = 1e-8), :251, :312, :377; course/modules/E/E4/project.html:317 (Constraints)",
        "project.html:317 requires the reported gap at fraction 0 and at an interior fraction to agree with the Proposition 3 gap to within 1e-14 relative to the larger of 1 and |value|. The three tests at :251 (gap at 0, cost 2.0), :312 (gap at the reported fraction, both instances) and :377 (gap at 0, cost 0.30) compare with TOL_GAP = 1e-8, six orders looser than the stated precision. Measured: reference vs oracle at 151 interior inputs, largest difference 3.3e-16 (out/oracle_gap_precision.txt), so the reference meets 1e-14. The tests at :301 (gap should vanish at an interior root) cannot be tightened to 1e-14: in a scratch run with TOL_GAP = 1e-14 for all tests the reference failed it on the seed-3 instance (the reported gap at the root is of order 1e-14, and the bisection stops at 1e-12 relative); that test keeps TOL_GAP.",
        "In grader/test_project.py replace TOL_GAP by 1e-14 * max(1.0, abs(expected)) in the three comparisons at :251, :312 and :377, and keep TOL_GAP at :301, :325, :329. Verified in a scratch copy by ledgers/E4/scripts/E4-d-r17/tighten_check_r17.py (out/tighten_check_r17.txt): reference.py and alt_1..alt_8 at 50/50 each with the three checks at 1e-14. Note the change does not kill mutant_v17_02 (see E4d17-mutant-v17-02)."),
    "E4d17-oracle-agreement": (None, "PASS", f"{OUT}/oracle_gap_precision.txt; {OUT}/cand/alt_*.txt",
        "Interior agreement of the reference with the suite's own oracle: largest |reported - oracle| 3.3e-16 over 151 inputs (150 sampled from the box plus the mutant's point), count above 1e-14: 0 (ledgers/E4/scripts/E4-d-r17/oracle_gap_precision.py)."),
    "E4d17-independent-rederivation": (None, "PASS", f"{S}/rederive_fixed_point.py; {OUT}/rederive_fixed_point.txt; {OUT}/endpoint_checks_r17.txt; {S}/bracket_width_check.py",
        "Independent numerical route (fixed point on the clearing condition, variances from the moments, no closed forms of the page) reproduces: lambda* 0.57937525 and 0.57052263 (Labs 1, 2), b_u/b_s -3.45199422, tau_bar 0.18904110, informativeness 0.15898618 and 0.12466375, and all nine Lab 3 rows (fraction, informativeness; gap within 1.1e-16 of zero at each root). The Lab 1 bracket claim (width 2^-53 from the 53rd halving, ends adjacent, stays) is confirmed by out/bracket_width_check.txt."),
}

PREV_BY_ID = {r["id"]: r for r in PREV["rows"]}


def build_rows():
    rows = []
    seen = set()
    for pid in PREV_IDS:
        if pid in seen:
            continue
        seen.add(pid)
        prev_row = PREV_BY_ID[pid]
        check = prev_row["check"]
        loc = LOC_OVERRIDE.get(pid, prev_row["location"])
        if pid in FRESH:
            status, evidence = FRESH[pid]
        elif pid in CARRY:
            key, note = CARRY[pid]
            status = "PASS"
            evidence = PREFIX.format(subject=SUBJECT[key]) + note + "."
        else:
            raise SystemExit(f"row {pid} has no FRESH or CARRY entry")
        row = {"id": pid, "check": check, "location": loc, "status": status, "evidence": evidence}
        if status != "PASS":
            row["fix"] = fix_for(pid, status)
        rows.append(row)
    for nid, (_, status, loc, evidence, *rest) in NEW.items():
        row = {"id": nid, "check": "2.6-mutation" if "mutant" in nid else "2.6-autograder", "location": loc,
               "status": status, "evidence": evidence}
        if status != "PASS":
            row["fix"] = rest[0]
        rows.append(row)
    return rows


FIX = {
    "E4d-exemplar-A-calibration": "Blind re-score of Exemplar A by a verifier that has not read its annotations: run strip_exemplars.py first, then score C1-C5 from the rubric; compare with 2,2,1,2,1 (within one level).",
    "E4d4-calibration-blind": "As E4d-exemplar-A-calibration.",
    "E4d-mutants-total": "See E4d17-mutant-v17-02.",
    "E4d15-cmd-mutate": "See E4d17-mutant-v17-02.",
    "E4d3-spec-stop-rule-and-constraints": "See E4d17-gap-tolerance-constraint.",
    "E4d16-constraints-any-sentence": "See E4d17-gap-tolerance-constraint.",
    "E4d10-delta-constraints-gap-at-zero": "See E4d17-gap-tolerance-constraint.",
}


def fix_for(pid, status):
    return FIX[pid]


NOTES = [
    "Blind exemplar scoring (ruling 15) ran first with ledgers/E4/scripts/E4-d-r17/strip_exemplars.py (final version). DISCLOSURE: the first stripper version let one read print Exemplar A's annotation lines, so Exemplar A is UNVERIFIABLE this round (E4d-exemplar-A-calibration, E4d4-calibration-blind). Exemplar B was not exposed before scoring and scores 4,4,4,4,4 blind against official 4,4,4,4,4 (PASS). Record: out/blind_scores_r17.txt.",
    "Delta since the round-16 pin 56cc575a (only commit: 700bf33f): project.html (lede line 37, ladder line 42 'short', rungs paragraph 53, Lab 1 text 57 and 170, Lab 2 text 175 and 242, rubric caption 520 and C5 cells 527, Exemplar A C5 annotation 593-594), tests/labs/E4/lab-E4-project-1.py and -2.py (docstrings only), ledgers/E4/mutants v16_01..04 added. The grader, alternatives, equivalent, references E4 records and notation are unchanged. Hunk list and full slice diff: out/delta_slice.diff.",
    "Previous FAIL rows E4d-spec-ladder and E4d-rubric-observable are resolved by the delta and re-verified fresh (PASS). Previous UNVERIFIABLE rows for Exemplar B are re-verified fresh (PASS); Exemplar A remains UNVERIFIABLE (contamination disclosed above).",
    "Gates run this round on 700bf33f (out/): check_pages PASS; check_dag PASS; check_projects PASS; run_labs 12/12 PASS; run_graders 0-49 reference 50/50 PASS; page_smoke project PASS; ruff check and format clean; mypy --no-incremental (slice) and full mypy (385 files) clean; pytest on five relevant files passed; verify_refs offline 560 entries 0 problems and live E4 3 entries 0 problems. The bare collect of the grader fails with ModuleNotFoundError: solver (by design, the suite imports solver); the count 48 is taken with reference.py as solver.py in a scratch copy (out/collect_only_reference.txt).",
    "Mutation run (tools/mutate_graders.py --unit E4 --seeds 0-9): 134 mutants, 133 killed, exit 1 (out/mutate_graders_E4_0_9_r17.txt). Four new student-error mutants written from reference.py (one changed line each): three killed, one survived (mutant_v17_02). Alternatives alt_1..alt_8 and the four equivalents pass 50/50 on seeds 0-49 (out/cand/).",
    "Rulings applied: 15 (blind scoring, see above); 17 (stop-rule variants: the equivalent README numbers were carried, not re-argued); 18 (alt_r8_* and alt_v9_* are absent from the checkout; rows E4d8-alternatives-r8 and E4d9-alternatives-v9 now rest on alt_1..alt_8, which pass). Ruling 9 applies to mutant_v17_02 (see its row).",
    "Hours: the time table (28 h, components 1+1+5+8+5+5+3) and the 23 h round-16 estimate are carried; neither the table nor the grader changed. Not re-estimated this round.",
    "Notation: references/references.json, plans/FINAL-ARCHITECT-RULINGS.md (rulings 19-20 added for M7) and curriculum/ changed elsewhere in the repo, none in the E4 slice-d subjects.",
    "Not checked by this verifier: lessons L01-L09 and cards.json (other slices; cards excluded); tools/render_curriculum.py, build_site.py --check and fetch_data.py --check (no curriculum, site-data or market input changed in slice d); the full pytest suite (five relevant files only); live verify_refs for all 560 entries (only the three E4 entries live); the Pyodide run beyond page_smoke; a 20-seed instance sample this round (carried from round 16; instance.py unchanged); the 2025-2026 freshness of muth1961rational and milgrom1982information (no freshness claim made).",
    "Scripts and outputs: ledgers/E4/scripts/E4-d-r17/ (run_gates_r17.sh, collect_reference.sh, run_candidate_r17.py, run_alts_r17.sh, twins_and_page_code.py, rederive_fixed_point.py, endpoint_checks_r17.py, bracket_width_check.py, oracle_gap_precision.py, search_v17_02_gap_diff.py, strip_exemplars.py, write_fragment_r17.py) and out/.",
]
SUMMARY = (
    "E4 slice d round 17 (pin 700bf33f): verdict FAIL. Resolved from round 16: the ladder now says 'short' (matches tier-M sisters M6 and SC1) and the C5 rubric descriptors are observable. "
    "New FAIL 1: the suite compares the gap at fraction 0 (test_project.py:251, :377) and at the reported interior fraction (:312) against TOL_GAP = 1e-8, while project.html:317 states 1e-14; the reference meets 1e-14 (largest 3.3e-16 over 151 interior inputs) and alt_1..alt_8 pass with the three tests at 1e-14 in a scratch copy. "
    "New FAIL 2: mutant_v17_02 (b_s without the (1-lam) tau_y term, against project.html:276) survives seeds 0-49; its solver outputs differ from the reference only within the page's stated tolerances, so this needs an architect ruling (ruling-9 equivalence or a finer stated requirement). "
    "Exemplar A blind calibration is UNVERIFIABLE because the verifier's first stripper version exposed its annotations (disclosed); Exemplar B is clean and matches 4,4,4,4,4."
)

rows = build_rows()
mutants = []
for line in open(f"{OUT}/mutate_graders_E4_0_9_r17.txt", encoding="utf-8"):
    m = re.match(r"(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line.strip())
    if not m:
        continue
    state, name, desc, killed = m.groups()
    killed_by = None if killed.strip() == "None" else killed.strip()
    mutants.append({"id": name[:-3], "file": f"ledgers/E4/mutants/{name}", "description": desc.strip(),
                    "killed_by": killed_by})
fails = [r["id"] for r in rows if r["status"] != "PASS"]
fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 17,
    "verifier": "Haiku independent verifier, E4 slice d, round 17 (did not build E4; checkout pinned at 700bf33f, detached)",
    "pin": "700bf33f334486d7b5b4f22d4f82f3e25d4b39b6",
    "base": "56cc575a774a66e9580d3182969eb7d6aa413731 (round-16 pin); delta in slice d listed in notes",
    "checkout": str(ROOT),
    "scratch": "/Users/billyribeiro/.fanout/scratch-E4-d-r17 (probes only; all evidence files are under ledgers/E4/scripts/E4-d-r17/out/)",
    "verified_at": "2026-11-09T06:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": SUMMARY,
}
json.dump(fragment, open(f"{ROOT}/ledgers/E4/E4-d.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(rows), "non-pass", fails)
print("mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
