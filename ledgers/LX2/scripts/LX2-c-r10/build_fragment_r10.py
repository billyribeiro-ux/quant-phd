"""Write ledgers/LX2/LX2-c.json (round 10, slice c) from the evidence gathered this round.

Every row id of round 9 is kept. Every row was re-verified in round 10 (the page is the subject of every row and
its delta touched two lines), so no row is carried. Run from the checkout root with python -I -W error.
"""

import json
import pathlib
import re

ROOT = pathlib.Path(".")
OUT = ROOT / "ledgers/LX2/scripts/LX2-c-r10/out"
R9 = pathlib.Path("/Users/billyribeiro/.fanout/frags/E-LX2-c.round9.json")
r9 = json.loads(R9.read_text(encoding="utf-8"))

GATES = (
    "round 10 at pin 00a84795: check_pages --unit LX2 PASS (out/r10_check_pages_LX2.txt); check_dag --all exit 0 with "
    "LX2 PASS (out/r10_check_dag.txt); check_projects --unit LX2 PASS (out/r10_check_projects_LX2.txt); run_labs --unit "
    "LX2 PASS (7/7) (out/r10_run_labs_LX2.txt); run_graders --unit LX2 'no autograder (grading: rubric)' "
    "(out/r10_run_graders_LX2.txt)"
)
PAGE_SMOKE = "page_smoke --unit LX2 --pages project run alone: 'page_smoke modules/LX/LX2/project.html: PASS' (out/r10_page_smoke_project.txt)"
LABS = "tests/labs/LX2/lab-LX2-project-{1,2,3}.py run alone with python -I -W error: exit 0, empty stderr, stdout equals the expected block (out/r10_page_vs_twin.txt)"
RED = "independent re-derivation with fractions and Decimal ROUND_HALF_UP (ledgers/LX2/scripts/LX2-c-r10/rederive_c_r10.py, out/rederive_c_r10.txt)"
SR = "SR 26-2 files re-fetched by plain curl on 2026-11-05 from https://www.federalreserve.gov/supervisionreg/srletters/ (SR2602a1.pdf and SR2602.pdf sha256 identical to round 9: 209ce4c1..., 956b3bc6...; sr2602.htm sha256 05af406d...; scratch /tmp/lx2c-r10-src)"

ROWS = {
    "proj-gates-tooling": (
        "course/modules/LX/LX2/project.html; tests/labs/LX2/lab-LX2-project-{1,2,3}.py",
        f"gates: {GATES}; ruff check . exit 0 and ruff format --check . exit 0 (out/r10_ruff_check_all.txt, out/r10_ruff_format_all.txt); mypy --no-incremental 'Success: no issues found in 385 source files' (out/r10_mypy_all.txt); pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py -k 'LX2 or project' exit 0 (out/r10_pytest_subset.txt); verify_refs --offline 'offline integrity: 560 entries, 0 problems' (out/r10_verify_refs_offline.txt). Live verify_refs not run: no reference record changed.",
    ),
    "proj-page-smoke": ("course/modules/LX/LX2/project.html", PAGE_SMOKE + "; the page loads in Chromium with no console errors."),
    "proj-labs-twins-alone": ("tests/labs/LX2/lab-LX2-project-1.py, -2.py, -3.py", LABS),
    "proj-page-code-equals-twin": (
        "course/modules/LX/LX2/project.html lines 102-205 (lab 1), 239-333 (lab 2), 371-515 (lab 3)",
        "page code compared with the twin (ledgers/LX2/scripts/LX2-c-r10/page_vs_twin_r10.py): lab 1 86 of 86 lines identical; lab 3 109 of 109 identical; lab 2 differs in exactly two lines, 'hit_rate = ___' (page line 312) and 'bias = ___' (page line 314), against the twin's 'Fraction(hits, horizon)' and 'Fraction(sum(errors), horizon)'.",
    ),
    "proj-rung1-hypothesis-and-steps": (
        "course/modules/LX/LX2/project.html lines 104, 191-204, 210-236",
        f"lab 1 hypothesis (line 104): 4 hits of 8, rate 0.5000, bias 0.2500, edge months 15 and 19 match the printed block (lines 191-203) and {RED}: L1 errors [1,-3,2,0,-4,3,-2,5], hits 4, bias 2/8, edge [15,19]. Worked steps: 'Month 13 gives e13 = 126 - 125 = +1' (line 220) and 'month 14 gives e14 = 128 - 131 = -3' verified; the errors list in line 214 matches.",
    ),
    "proj-rung2-numbers-and-claims": (
        "course/modules/LX/LX2/project.html lines 241, 321-331",
        f"lab 2 hypothesis (line 241): 4 hits of 6, 0.6667, 0.1667, edge months 14 and 17 match the expected block (lines 321-331) and {RED}: L2 errors [-1,2,6,1,-2,-5], hits 4, rate 4/6 = 0.6667, bias 1/6 = 0.1667, edge [14,17].",
    ),
    "proj-rung2-instant-check-mutants": (
        "course/modules/LX/LX2/project.html lines 45, 332; ledgers/LX2/mutants/*lab2*.py",
        "harness (ledgers/LX2/scripts/LX2-c-r10/harness_lab2_r10.py, a copy of the labs.js compareOutput rule: NUMBER regex, tolerance 1e-6, whole-token compare) run on all 49 lab-2 files (out/r10_harness_all_lab2_mutants.txt): 34 KILLED, 15 SURVIVE (named in the student-error rows), 2 alternatives survive. The page's own examples at line 332 reproduce: hit count over 8 prints 0.5000; mean absolute error prints 2.8333.",
    ),
    "proj-rung2-student-error-mutants": (
        "course/modules/LX/LX2/project.html lines 45, 332; ledgers/LX2/mutants/r6_lab2_*.py, r10_lab2_*.py",
        "student-error survivors are disclosed on the page: tie-only rules (round half to even, round half toward +infinity, Python round, float format ties-even) are named at line 332 ('does not exercise the tie rule'); a hard-coded printed value passes (line 332, 'a blank typed as the value it prints passes'); the four-place ceiling and the |sum| bias agree with the printed block on this window and the page states that the check grades printed output only (line 45). Judgment: as in rounds 8 and 9, these are disclosed limits, not undisclosed defects.",
    ),
    "proj-rung2-alternatives": (
        "ledgers/LX2/mutants/alt-lab2-float-division.py; ledgers/LX2/mutants/alt_r10_lab2_*.py",
        "correct alternatives survive the whole-block compare (out/r10_harness_all_lab2_mutants.txt): alt-lab2-float-division.py SURVIVES; alt_r9_lab2_fmean_bias_error_list_hits.py SURVIVES; alt_r10_lab2_squared_error_band.py SURVIVES (band test (e)**2 <= 4); alt_r10_lab2_decimal_half_up_quantize.py SURVIVES (Decimal ROUND_HALF_UP quantize on the exact value).",
    ),
    "proj-rung2-alt-fixture": (
        "ledgers/LX2/mutants/r9_*.py; ledgers/LX2/mutants/alt_r9_lab2_fmean_bias_error_list_hits.py; ledgers/LX2/mutants/alt_r10_lab2_*.py",
        "each mutant and alternative is a complete module (run by harness with python -I -W error: no crash, stdout compared). The new alternatives carry the one-line docstring the fixture requires (ledgers/LX2/scripts/LX2-c-r10/make_r10_mutants.py asserts each substitution matches exactly once).",
    ),
    "proj-lab3-numbers": (
        "course/modules/LX/LX2/project.html lines 373 (hypothesis), 483-513 (expected block), 514 (interpretation)",
        f"{RED}: L3 hits 13 of 24, rate 13/24 = 0.5417; bias 51/24 = 2.1250; calibration sum 11, bias 11/12 = 0.9167; edge months [14,15,16,19,22,24,26]; largest |e| 8 at months 34 and 35, earliest 34. Expected block equals the twin output (out/r10_page_vs_twin.txt).",
    ),
    "proj-lab-generator-description": (
        "tests/labs/LX2/lab-LX2-project-3.py lines 1-22 (docstring); lab-LX2-project-1.py lines 1-22",
        "docstring claims checked against code: 'uniform on -3 to 3 inclusive (random.Random.randint)' matches rng.randint(-3, 3); '100 + 2 * t + noise, and 6 units less from month 28 on' matches SHIFT_FROM=28, SHIFT_UNITS=-6; 'Only the validation window enters the outcomes measures' matches errors dict over t in 13..36; 'Part E ... earliest such month on a tie' matches max(key=(abs, -t)). Lab 1 'No random draws are used' matches the code.",
    ),
    "proj-exemplar-a-numbers": (
        "course/modules/LX/LX2/project.html lines 565-630 (exemplar A)",
        f"{RED}: 'errors of months 28 to 36 are all positive, from 3 to 8' (line 572) = min 3, max 8; 'Its errors sum to 11, the only integer sum that prints as 0.9167' (line 572) = only k=11 in [-60,60] prints 0.9167; 'sum of 24 months 51, 51/24 = 2.125' (584); months 13-27 sum -3, 13 hits, -3/15 = -0.2000, 13/15 = 0.8667 (585); months 28-36 sum 54, 54/9 = 6.0000, 0/9 = 0.0000 (585); 'strict band ... 6 of 24, or 0.2500' (586); 'rolling bias 56/12 = 4.6667, months 25 to 36' (610) = 56/12 = 4.6667.",
    ),
    "proj-exemplar-b-numbers": (
        "course/modules/LX/LX2/project.html lines 632-695 (exemplar B)",
        f"{RED}: 'every error ... in months 13 to 27 is between -3 and 3' (638) = min -3, max 3; '13 hits out of 24 months, 0.5417' (650) = 13/24; 'The bias is 2.1250' (650) = 51/24; 'window ... 24 months' (662) = H.",
    ),
    "proj-exemplar-calibration": (
        "course/modules/LX/LX2/project.html #exemplar-a (data-scores 4,4,4,4,3), #exemplar-b (data-scores 2,2,2,1,1)",
        "blind scoring (round 10, from the annotation-stripped exemplar prose written to /tmp/lx2c-r10-src/exemplars_stripped_r10.txt; honest caveat: the first read of the page had shown the annotations, so the blind scores are the rubric applied to the prose alone): exemplar A 4,4,4,4,3; exemplar B 2,2,2,1,1. Official 4,4,4,4,3 and 2,2,2,1,1. Each criterion within one level (0 differences). See proj-r10-blind-exemplars.",
    ),
    "proj-exemplar-b-c5-annotation": (
        "course/modules/LX/LX2/project.html lines 686 and 691 (exemplar B sources and C5 annotation)",
        "line 686 'SR 26-2 requires the outcomes analysis ...' carries data-cite frb2026fed and no data-locator; 'The CFA Code also applies' carries no data-cite. Line 691 annotation: 'Misses C5 level 2: no regulatory statement carries both a key and a locator' matches the data attributes (grep).",
    ),
    "proj-exemplar-b-unread-requirement": (
        "course/modules/LX/LX2/project.html line 691 (exemplar B C5 annotation)",
        f"{SR}: PDF text (pdftotext -layout) of SR2602a1.pdf page 2 contains 'This guidance does not set forth enforceable standards or prescriptive requirements' (section I, printed page 2), so the annotation's statement that the source does not make the requirement holds.",
    ),
    "proj-source-supersession": (
        "course/modules/LX/LX2/project.html line 363 (data-locator and prose)",
        f"{SR}: cover letter (combined PDF page 1; sr2602.htm paragraph beginning 'The Board of Governors') reads 'which supersedes and replaces SR letter 11-7, Guidance on Model Risk Management (issued April 4, 2011) and SR letter 21-8'. The page's claim is a paraphrase in a claim span (no quotation marks) with that locator; the two letters also appear under 'Supersedes:' after the signature (combined PDF page 2).",
    ),
    "proj-source-applicability": (
        "course/modules/LX/LX2/project.html line 364 (data-locator 'cover letter, paragraph headed Applicability')",
        f"{SR}: sr2602.htm has 'Applicability:' as its own <p> (inside the panel) and 'over $30&nbsp;billion in total assets' within it; the claim's locator matches the paragraph headed Applicability; the page's paraphrase 'over $30 billion' matches.",
    ),
    "proj-source-attachment": (
        "course/modules/LX/LX2/project.html lines 347-360 (attachment expectations) and 363-367",
        f"{SR}: each quote located in SR2602a1.pdf (pdftotext): 'Validating conceptual soundness...' printed page 8; 'Outcomes analysis compares...' page 9; 'established performance thresholds' page 9; 'Sound validation identifies...' page 7; 'Ongoing model monitoring involves...' page 9; 'includes an assessment of a model's reliability and its limitations' page 7 (the source uses a curly apostrophe; typographic only). Headings: Conceptual Soundness p.8, Outcomes Analysis p.9, Ongoing Model Monitoring p.9; no Limitations heading.",
    ),
    "proj-citations-registry": (
        "course/modules/LX/LX2/project.html data-cite values; references/references.json",
        "data-cite values on the page: frb2026fed, cfandcode, gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united; each is present in references/references.json (entries walked by key) with verified_by 'issuer'. verify_refs --offline: 560 entries, 0 problems.",
    ),
    "proj-notation": (
        "course/modules/LX/LX2/project.html inline math (65 spans)",
        "inline math symbols on the page: H, t, y_t, e_t, \\hat{y}_t, \\operatorname{bias}, \\sum_t; none is a registered symbol of notation/notation.json (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); same meanings as Lesson 4 (L04.html s4: y_t realised, e_t error, H window length). No display math.",
    ),
    "proj-dag-and-links": (
        "course/modules/LX/LX2/project.html lines 62 (Lesson 4 band link), 68, 82 (concept link), and all href values",
        "check_dag --unit LX2 (in check_dag --all) PASS. Concept 'model-risk-management' is defined in L04.html (dfn id def-model-risk-management, line 97) inside the unit; links L04.html#s4 and L04.html#def-model-risk-management resolve (s4 at L04.html line 113). Internal anchors resolve (check_pages PASS).",
    ),
    "proj-standard-error-term": (
        "course/modules/LX/LX2/project.html lines 55-75 (conventions)",
        "'error' is defined at line 60 (e_t = yhat_t - y_t) before use in lines 62-66; the sign convention is stated and matches Lab 1 code (error = predicted - realised).",
    ),
    "proj-validation-window-term": (
        "course/modules/LX/LX2/project.html lines 53-56, 82-95",
        "'validation window' (months 13 to 36, H = 24) is defined at line 56 before its use in the case section (line 91) and the labs; 'calibration window' defined at line 56.",
    ),
    "proj-lab1-sections-claim": (
        "course/modules/LX/LX2/project.html lines 104, 204; tests/labs/LX2/lab-LX2-project-1.py",
        "line 100 says the lab 'does not compute the other three sections'; the lab computes Parts A-D of the outcomes analysis only (code lines 137-187). Line 204 'nothing about why any month missed' is consistent with the printed block.",
    ),
    "proj-spec-complete": (
        "course/modules/LX/LX2/project.html lines 337-358",
        "spec contains context, inputs, required outputs (validation report sections in order, self_assessment.md), constraints and grading mode (rubric only). The inputs describe the case table generated by Lab 3 from seed 20261103; plan 5.2 named a CSV, but architect decision 16 (no data files, no figures) and the lab-generated table are consistent with the page's own statements (not a finding).",
    ),
    "proj-spec-ladder": ("course/modules/LX/LX2/project.html lines 42-48 (ol.ladder)", "four rungs in the order 1 worked example, 2 completion, 3 independent project, 4 stretch; check_projects PASS (out/r10_check_projects_LX2.txt)."),
    "proj-hours": (
        "course/modules/LX/LX2/project.html lines 531-545 (table#hours); course/modules/LX/LX2/index.html data-hours-lessons=36, data-hours-project=14",
        "hours 2+2+2+3+3+2 = 14 = data-hours-project; 36 + 14 = 50; 14/50 = 28 percent as stated at line 540. check_pages hub split PASS.",
    ),
    "proj-rubric-observable": ("course/modules/LX/LX2/project.html lines 549-562 (table#rubric)", "every descriptor names an observable element (a band rule, a named test, a Lab 3 Part, a registry key and locator); check_projects rubric_problems PASS."),
    "proj-rubric-criteria-count": ("course/modules/LX/LX2/project.html lines 553-557", "five criteria (C1-C5), each with a th and exactly four td cells; check_projects PASS."),
    "proj-autograder-na": ("course/modules/LX/LX2/project.html line 357 (dd Grading mode); curriculum/06-profession-capstone.yaml:86", "grading is 'rubric'; run_graders --unit LX2: 'no autograder (grading: rubric)' (out/r10_run_graders_LX2.txt)."),
    "proj-adversarial-na": ("course/modules/LX/LX2/project.html line 357", "'No adversarial review is used for this project'; plan Q14 recommended no question bank; not applicable."),
    "proj-atlas-na": ("course/modules/LX/LX2/project.html spec (Context, Constraints)", "no Atlas series or milestone; plan B4; check_projects PASS with no atlas key."),
    "proj-studio-na": ("course/modules/LX/LX2/project.html", "LX2 is a module project, not a studio (plan 2.2 / 5.x); not applicable."),
    "proj-data-and-figures-na": ("course/modules/LX/LX2/project.html (no img, svg, figure, data-files attribute)", "grep for <img, <svg, <figure and data-files in project.html: none (architect decision 16: no figures, no data files)."),
    "proj-banned-and-process-words": ("course/modules/LX/LX2/project.html (visible text)", "visible-text scan (script and style removed) for verif, builder, batch, ledger, fragment, round N, audit, TODO, placeholder, lorem, fabricat, scaffold, agent, mutant, we, I, just, simply, obviously, clearly, probably: no process word in learner text (the only hits are inside the lab code blocks)."),
    "proj-case-realised-source": ("course/modules/LX/LX2/project.html lines 92-94 (case, not documented item (e))", "item (e) says the case series values are those Lab 3 generates from its seed for months 1 to 36, and that Labs 1 and 2 write their own illustrative values; code confirms (lab 1 REALISED at months 13-20, lab 2 at months 13-18 differ from Lab 3 except at month 18 and month 13 respectively)."),
    "proj-rung1-plan-scope": ("course/modules/LX/LX2/project.html lines 102-232", "rung 1 is one solved outcomes analysis with four element checks; the plan's rung 1 scope (plan 5.1 item 1) is met."),
    "proj-rung4-open-ended": ("course/modules/LX/LX2/project.html lines 704-711", "stretch items are open-ended and 'not graded'; no fixed answer is implied."),
    "proj-exemplar-a-m1-window": ("course/modules/LX/LX2/project.html line 572 (exemplar A conceptual soundness)", "M1 is stated over the validation window (case line 58 and lab 1 docstring); exemplar A tests M1 over months 13 to 36, consistent with that stated window."),
    "proj-exemplar-a-derivation-claim": ("course/modules/LX/LX2/project.html lines 585-586, 610-611", "derivation claims checked against Part A rows: 15-month split (-3, 13 hits), 9-month split (54, 0 hits), 56 for months 25-36, strict-band 6 of 24: all reproduced by rederive_c_r10.py."),
    "proj-rung3-sr26-standard": ("course/modules/LX/LX2/project.html lines 347-360, 363-367", f"{SR}: the attachment is stated as sound practice ('This guidance does not set forth enforceable standards'); the page's claim that SR 26-2 does not require the four sections is consistent with that sentence."),
    "proj-define-model-owner": ("course/modules/LX/LX2/project.html (no dfn); line 82 concept link", "the page defines no concept itself; the concept 'model-risk management' is linked to its dfn in L04 (in-unit prerequisite)."),
    "proj-m2-statement-consistency": ("course/modules/LX/LX2/project.html lines 91 (case assumptions), 112 (lab 1 docstring), 58", "M2 is stated the same way at lines 58, 91 and in lab 1 docstring: the forecast for month t is issued before month t starts and uses no information from month t; line 91 says M2 cannot be checked from the case, consistent with item (b)."),
    "proj-reading-count": (
        "course/modules/LX/LX2/project.html line 715 (Reading paragraph; round 9 FAIL location)",
        "FIXED since round 9. Line 715 now reads 'frb2026fed for eight regulatory statements of its own text: the three of the source note and the five quotes in the attachment expectations'. Counted: own text data-cite frb2026fed = 9 (8 claim spans plus the reading-list li); source note spans lines 363 (1) and 364 (2) = 3; attachment expectations lines 350-353 = 1+1+2+1 = 5. Exemplars cite it 4 times (A 3 at line 622, B 1 at line 686), and line 715 says 'the exemplars also cite it'. 'no other key for any claim': the other data-cite values appear only in the reading list.",
    ),
    "proj-delta-lede-exemplars": ("course/modules/LX/LX2/project.html line 37 (lede)", "lede: 'two annotated exemplars, which are sample reports written to this specification' matches the exemplars (lines 565, 632)."),
    "proj-delta-rung3-pointer": ("course/modules/LX/LX2/project.html line 46 (ladder rung 3)", "rung 3 pointer to the attachment expectations and the source note matches lines 347 and 361 (ids attachment-expectations, source)."),
    "proj-delta-limitations": ("course/modules/LX/LX2/project.html lines 597-598", "limitation text: 'From month 28 every forecast misses' (Part A months 28-36 all hit=no); 'errors from 3 to 8' (min 3, max 8); 'the 9 months 28 to 36' (count 9)."),
    "proj-delta-rung2-disclosure": ("course/modules/LX/LX2/project.html lines 45, 241, 332", "disclosure that the rung-2 check compares printed output only and does not exercise the tie rule: checked by the harness (tie-only mutants survive; the printed values 0.6667 and 0.1667 are not ties, verified by rederive_c_r10.py output: no fraction part of 10^4 * v equals 1/2)."),
    "proj-delta-case-series-line": ("course/modules/LX/LX2/project.html line 93", "'Lab 1 agrees with the Lab 3 value at month 18 only, and Lab 2 at month 13 only': Lab 1 month 18 = 133 = Lab 3 month 18; Lab 2 month 13 = 127 = Lab 3 month 13; no other month agrees (rederive_c_r10.py output)."),
    "proj-delta-time-budget": ("course/modules/LX/LX2/project.html lines 531-545", "time-budget rows sum to 14 and each has a one-line rationale; the rung-2 row names the blank-explanation work."),
    "proj-scope-words": ("course/modules/LX/LX2/project.html (visible text)", "scope words in the visible text (only, all, always, every, any, same, exactly, never, none): each is either a stated property checked here (for example 'every run prints the same lines' with no random draws; 'the same band and rule as Lesson 4', confirmed at L04.html s4 line 113 onward) or a rubric term."),
    "proj-hours-independent-estimate": ("course/modules/LX/LX2/project.html table#hours", "design-target ruling: hours are design targets; the arithmetic is consistent (14 = 2+2+2+3+3+2); the independent-estimate row is a judgment under that ruling and is not a finding."),
    "proj-terms-first-use": ("course/modules/LX/LX2/project.html lines 53-75 and 82-100", "terms (window, hit, bias, rounding, registry key, locator, basis of a threshold, case table) are defined in the conventions list before the case section and labs use them."),
    "proj-anchors-links": ("course/modules/LX/LX2/project.html (all href)", "every internal href (#ladder, #conventions, #case, #rungs, #spec, #source, #rubric-section, #exemplars, #attachment-expectations, #self-assessment, #stretch, #lab references) resolves to an id on the page (grep); check_pages PASS."),
    "proj-mutate-graders-na": ("tools/mutate_graders.py --unit LX2", "ledgers/LX2/scripts/LX2-c-r10/out/r10_mutate_graders_LX2.txt: exit 0 with no output for the rubric unit (no autograder)."),
    "proj-pytest-lx2": ("tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, tests/test_page_smoke.py", "pytest -k 'LX2 or project' exit 0 (out/r10_pytest_subset.txt); mypy strict on the LX2 twins 'Success: no issues found in 7 source files' (out/r10_mypy_labs.txt)."),
    "proj-labjs-failure-messages": ("course/assets/js/labs.js lines 42-58 and 133-138; course/modules/LX/LX2/project.html", "compareOutput names the first differing token and its expected value (labs.js line 53-54), inside the status text 'output differs from the expected result (...)'. The expected block is already printed on the page at lines 321-331, so the message reveals nothing the page does not show. Tolerance and token messages name the property that differs. Code unchanged since round 9."),
    "proj-lab2-docstring-completed-solution": ("course/modules/LX/LX2/project.html lines 242-262 (lab 2 docstring) and tests/labs/LX2/lab-LX2-project-2.py lines 1-22", "the docstring says the completed solution fills the hit-rate and bias lines and the page shows those lines blanked; the twin contains the completed lines (Fraction(hits, horizon), Fraction(sum(errors), horizon)); docstring and code agree."),
    "proj-rung2-disclosure-verified": ("course/modules/LX/LX2/project.html lines 45, 332", "disclosure claims hold on the page's compare rule: 'a hit rate written as the hit count over 8 ... prints 0.5000' (4/8) and 'a bias written as the mean of the absolute errors prints 2.8333' (17/6) reproduced by the harness."),
    "proj-r7-new-mutants": ("ledgers/LX2/mutants/r7_*.py", "re-run in round 10 (out/r10_harness_all_lab2_mutants.txt): all r7 files are KILLED or are the disclosed tie-only survivor r7_lab2_rounds_through_python_round.py."),
    "proj-rung2-alt-decimal": (
        "ledgers/LX2/scripts/LX2-c-r8/alt_r8_a1_len_float_decimal.py",
        "re-run in round 10 (out/r10_harness_alt_r8.txt): 'SURVIVES alt_r8_a1_len_float_decimal.py' (correct alternative, unchanged file).",
    ),
    "proj-attachment-quote-locators": ("course/modules/LX/LX2/project.html lines 347-360, 363-364, 622, 686", "each quote's printed page and PDF page (page 8, 9, 7, 9; cover letter; section I printed page 2) checked against SR2602a1.pdf and SR2602.pdf (see proj-source-attachment)."),
    "proj-claim-span-paraphrase": ("course/modules/LX/LX2/project.html line 363 (claim span paraphrase)", "the unquoted claim span paraphrases the cover letter: 'The Board of Governors, the Office of the Comptroller of the Currency and the Federal Deposit Insurance Corporation issue the attached Revised Guidance ... which supersedes and replaces SR letter 11-7 and SR letter 21-8' against the letter's 'The Board of Governors of the Federal Reserve System, Office of the Comptroller of the Currency (OCC), and Federal Deposit Insurance Corporation (FDIC) ... are issuing the attached Revised Guidance ... which supersedes and replaces SR letter 11-7 ... and SR letter 21-8'. Same content; no quotation marks are used."),
    "proj-counter-evidence-c-grade": ("course/modules/LX/LX2/project.html claim spans data-grade=C (12)", "12 claim spans grade C, all with data-cite and locator; the grade C is consistent with the single-source regulatory claims; counted by grep (data-grade=\"C\" = 12)."),
    "proj-prose-numbers-rederived": ("course/modules/LX/LX2/project.html (all numeric prose)", f"{RED}: every numeric statement in rungs 1-3, the exemplars, the limitations and the time budget re-derived; no mismatch (see proj-lab3-numbers, proj-exemplar-a-numbers, proj-exemplar-b-numbers, proj-rung1-hypothesis-and-steps, proj-rung2-numbers-and-claims)."),
    "proj-r8-delta-read": ("course/modules/LX/LX2/project.html lines 55 and 363", "round 8 delta hunks reread: superseded by the round 9 and round 10 hunks."),
    "proj-r8-new-mutants": ("ledgers/LX2/mutants/r8_lab2_*.py", "round 8 mutants re-run in round 10: killed except the disclosed ceiling survivor (out/r10_harness_all_lab2_mutants.txt)."),
    "proj-r8-alternative-lab2-len-float-decimal": ("ledgers/LX2/scripts/LX2-c-r8/alt_r8_a1_len_float_decimal.py", "covered by the r10 alternative family (see proj-rung2-alt-decimal); the earlier file is unchanged."),
    "proj-r9-delta-read": (
        "course/modules/LX/LX2/project.html lines 66-69 (rounding) and 715-716 (reading)",
        "round 10 delta 00a84795 vs c93dd52 for this slice (git diff c93dd526 00a84795 -- course/modules/LX/LX2 tests/labs/LX2): project.html two hunks, @@ -66 line 69 (Rounding definition: 'a tie, a value whose fifth decimal place is 5 with nothing after it, goes away from zero') and @@ -713 line 716 (Reading paragraph, eight statements). tests/labs/LX2 unchanged. Both hunks read in full and re-verified (rows proj-rounding-definition-r10 and proj-reading-count).",
    ),
    "proj-r9-new-mutants": ("ledgers/LX2/mutants/r9_lab2_*.py", "round 9 mutants re-run in round 10: each KILLED (out/r10_harness_all_lab2_mutants.txt)."),
    "proj-r9-alternative": ("ledgers/LX2/mutants/alt_r9_lab2_fmean_bias_error_list_hits.py", "re-run in round 10: SURVIVES (correct alternative)."),
    "proj-r9-blind-exemplars": (
        "course/modules/LX/LX2/project.html #exemplar-a, #exemplar-b",
        "see proj-exemplar-calibration: round 10 blind scores A 4,4,4,4,3 and B 2,2,2,1,1 match the official data-scores exactly.",
    ),
}

NEW_ROWS = {
    "proj-rounding-definition-r10": (
        "course/modules/LX/LX2/project.html line 69 (Rounding, round 10 delta)",
        f"{RED}: the sentence 'half up to four decimal places, so a tie, a value whose fifth decimal place is 5 with nothing after it, goes away from zero' matches the labs' decimal_text (floor(|v| * 10^4 + 1/2), away from zero for negatives too) and the L04 section 4 rule (line 'A tie is rounded away from zero'); the rederive output shows no printed value of this window is an exact tie (no fraction part equal to 1/2).",
    ),
    "proj-r10-sources-refetch": (
        "references/references.json frb2026fed (url sr2602.htm); course/modules/LX/LX2/project.html lines 347-367",
        f"{SR}. Quotes in the page checked by pdftotext: 6 attachment quotes located on printed pages 7, 8, 9 (2 on 7, 1 on 8, 2 on 9); the enforceability sentence on printed page 2; cover-letter and Supersedes text on pages 1 and 2; Section V heading on printed page 7. Combined-file page mapping: printed 2, 7, 8, 9 are combined PDF pages 4, 9, 10, 11 (verified: 'does not set forth' on 4, quotes on 9, 10, 11).",
    ),
    "proj-r10-rederive": (
        "course/modules/LX/LX2/project.html (all numeric prose and printed blocks)",
        f"{RED}: lab 1 4/8 and 0.2500, lab 2 4/6 and 0.1667, lab 3 13/24, 51/24, 11/12, 56/12, 54/9, -3/15 all reproduced; strict-band counts 2 (lab 1) and 6 (lab 3) reproduced; the page's 'eight months' and 'six months' windows and 'H = 24' match.",
    ),
    "proj-r10-new-mutants": (
        "ledgers/LX2/mutants/r10_lab2_hit_rate_integer_division.py, r10_lab2_edge_list_prints_all_hits.py, r10_lab2_bias_subtracts_hit_count.py, r10_lab2_bias_absolute_value_of_sum_per_H.py",
        "four new student-error mutants written by round 10 (ledgers/LX2/scripts/LX2-c-r10/make_r10_mutants.py): integer division of the hit count (prints 0.0000, KILLED); Part D lists every hit month (KILLED); bias subtracts the hit count (prints -0.5000, KILLED); bias takes |sum| (prints 0.1667 on this window, SURVIVES: equivalent here, the sum is +1; disclosed as printed-output-only grading at line 45). Earlier round-10 files r10_lab2_bias_absolute_error_sum.py (equivalent: sum +1) and r10_lab2_hit_band_three.py (equivalent: no |e| = 3 in the window, banner prints the literal 'band 2 units') were re-run and survive for the same reason.",
    ),
    "proj-r10-alternative": (
        "ledgers/LX2/mutants/alt_r10_lab2_squared_error_band.py; ledgers/LX2/mutants/alt_r10_lab2_decimal_half_up_quantize.py",
        "two new correct alternatives both SURVIVE the whole-block compare (out/r10_harness_new_mutants.txt): the band tested as (predicted - realised)**2 <= 4 and the printed values produced by Decimal quantize with ROUND_HALF_UP.",
    ),
}

rows = []
for r in r9["rows"]:
    rid = r["id"]
    loc, ev = ROWS[rid]
    rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS", "evidence": ev})
for rid, (loc, ev) in NEW_ROWS.items():
    rows.append({"id": rid, "check": "round 10 new row: " + rid.replace("proj-", "").replace("-", " "), "location": loc, "status": "PASS", "evidence": ev})
missing = [r["id"] for r in r9["rows"] if r["id"] not in ROWS]
assert not missing, missing

# mutants: harness output, one line per file (the alternatives are printed twice by the glob run; dedupe)
harness = {}
for line in (OUT / "r10_harness_all_lab2_mutants.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(SURVIVES|KILLED\s*)\s+(\S+\.py)(.*)$", line)
    if m:
        harness.setdefault(m.group(2), (m.group(1).strip(), m.group(3).strip(" -")))
for line in (OUT / "r10_harness_alt_r8.txt").read_text(encoding="utf-8").splitlines() + (OUT / "r10_harness_new_mutants.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(SURVIVES|KILLED\s*)\s+(\S+\.py)(.*)$", line)
    if m:
        harness.setdefault(m.group(2), (m.group(1).strip(), m.group(3).strip(" -")))

DISCLOSED_TIE = {"r6_lab2_float_format_ties_even.py", "r6_lab2_round_half_even_ties.py",
                 "r6_lab2_round_half_toward_plus_infinity.py", "r7_lab2_rounds_through_python_round.py"}
mutants = []
for name, (status, detail) in sorted(harness.items()):
    if name.startswith("alt"):
        desc = "ALTERNATIVE correct implementation (must survive)"
        kb = "SURVIVES (correct; over-constraint check passes)" if status == "SURVIVES" else "KILLED (over-constraint FAIL)"
    elif status == "KILLED":
        desc = "student-error mutant (lab 2 twin edit)"
        kb = f"KILLED by the labs.js whole-block compare, harness r10: {detail}"
    elif name in DISCLOSED_TIE:
        desc = "student-error mutant (rounding rule)"
        kb = "SURVIVES: tie-only rounding rule, disclosed at page line 332 ('does not exercise the tie rule')"
    elif name == "r6_lab2_hard_coded_printed_values.py":
        desc = "student-error mutant (prints the expected block without computing)"
        kb = "SURVIVES: disclosed at page lines 45 and 332 (a blank or code typed as the printed value passes; the check grades printed output only)"
    elif name == "r8_lab2_hit_rate_ceiling_four_places.py":
        desc = "student-error mutant (rounding up at four places)"
        kb = "SURVIVES: ceiling and half-up agree on both printed values; disclosed as printed-output-only grading (page lines 45, 332)"
    elif name in {"r10_lab2_bias_absolute_error_sum.py", "r10_lab2_bias_absolute_value_of_sum_per_H.py"}:
        desc = "student-error mutant (bias sign convention: |sum|)"
        kb = "SURVIVES: equivalent on this window (error sum is +1, so |sum| = sum); disclosed as printed-output-only grading (page line 45)"
    elif name == "r10_lab2_hit_band_three.py":
        desc = "student-error mutant (band width 3)"
        kb = "SURVIVES: equivalent on this window (no month has |error| = 3; the banner text is literal)"
    else:
        desc = "student-error mutant (lab 2 twin edit)"
        kb = f"SURVIVES ({detail})"
    mutants.append({"name": name, "description": desc, "killed_by": kb})

fragment = {
    "unit": "LX2",
    "slice": "LX2-c",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for LX2-c, round 10 (did not build LX2)",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36",
    "base": "round 9 pin c93dd526025c6dffd34c54cd2c89eb62a890f885 (fragment /Users/billyribeiro/.fanout/frags/E-LX2-c.round9.json). Delta c93dd52..00a8479 for this slice: course/modules/LX/LX2/project.html (2 hunks: line 69 rounding definition; line 716 reading paragraph). tests/labs/LX2/*.py unchanged.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-LX2-c (detached at 00a84795; .venv symlinked; vendor copied)",
    "scratch": "/tmp/lx2c-r10-src (SR2602a1.pdf, SR2602.pdf, sr2602.htm fetched by plain curl 2026-11-05; text extracts a1.txt and combined.txt; exemplars_stripped_r10.txt)",
    "verified_at": "2026-11-05T03:30:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "SR 26-2 htm sha256 05af406d... differs from round 9's eb2f03c3... (the PDFs are byte-identical). The htm text was used only to confirm the cover-letter sentences (Applicability paragraph, Supersedes list); every quote on the page was checked against the PDFs."
    ],
    "notes": [
        "Round 10 FAIL (proj-reading-count) is fixed: line 715 now counts eight statements, which matches the page's own 8 claim spans (3 source note, 5 attachment expectations). Every round 9 row id is kept (74) and the new rows are added (5). Verdict PASS.",
        "No row is carried from round 9: the page is the subject of every row, and the two-hunk delta does not change the other content. Every row was re-verified in this round (the whole page was read line by line, labs were run alone, and the numbers were re-derived).",
        "Blind exemplar scoring: the first read of project.html had shown the annotations and official scores, so the blind scores were made from the annotation-stripped prose (/tmp/lx2c-r10-src/exemplars_stripped_r10.txt) under the rubric alone. A 4,4,4,4,3 and B 2,2,2,1,1 match the official scores. This is a calibration pass but not a fully clean blind pass; the caveat is recorded.",
        "Mutants: 49 lab-2 files run through the labs.js compare copy (harness_lab2_r10.py): 34 KILLED; 15 survivors are either tie-only or printed-output-only disclosed (see rows proj-rung2-student-error-mutants), or equivalent on this window (r10_lab2_bias_absolute_error_sum, r10_lab2_bias_absolute_value_of_sum_per_H, r10_lab2_hit_band_three); 3 correct alternatives (alt-lab2-float-division, alt_r9_..., alt_r10_lab2_squared_error_band, alt_r10_lab2_decimal_half_up_quantize) all survive. Four new student-error mutants written this round: 3 killed, 1 equivalent on this window. The earlier round-10 files in ledgers/LX2/mutants/ (created before this round's run) were re-run and are reported with their status.",
        "Judgment, not a finding: the instant rung-2 check does not grade the expression (page line 45 discloses this). The |sum| bias mutant is an expression error that prints the expected value on this window; that is the disclosed limit, as in rounds 8 and 9.",
        "Plan deviation noticed and judged not a finding: plan section 5.2 named a SIMULATED CSV input; the page instead has Lab 3 generate the case table from seed 20261103 (page lines 342, 370). Architect decision 16 (no data files, no figures) and the page's own statements are consistent, and the table is printed by a lab run, so the student can obtain every value.",
        "Verified outside this slice only as cross-references: the module hub split (36 + 14 = 50), the placement quiz wording (bar of 80 percent, two skill checks), and the L04 section 4 band and rounding rules.",
        "Not checked: the self-assessment form was not executed in a browser (rubric.js hides .annotation and [data-reveal] at line 149 and stores in IndexedDB via store.js; no fetch in rubric.js). Dark-theme and 360 px screenshots were not taken beyond page_smoke's own checks. verify_refs --live was not run (no reference record changed; the offline integrity check passes). The full CLAUDE.md gate chain (build_site --check, fetch_data --check, render_curriculum) was not run: those outputs are not in this slice. page_smoke ran in Chromium as part of its tool; no screenshots were taken by me.",
    ],
    "summary": f"LX2-c round 10: PASS. {len(rows)} rows: {len(rows)} PASS, 0 FAIL, 0 UNVERIFIABLE (74 round 9 ids kept; proj-reading-count FAIL from round 9 is now PASS; {len(NEW_ROWS)} new rows). Full re-read of project.html (738 lines) and the three lab twins; every number re-derived; SR 26-2 quotes re-checked against the PDFs fetched by plain curl; labs, page_smoke, check_pages, check_dag, check_projects, run_labs, run_graders, ruff, mypy, pytest subset and verify_refs offline all pass at 00a84795.",
}

out = ROOT / "ledgers/LX2/LX2-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants))
