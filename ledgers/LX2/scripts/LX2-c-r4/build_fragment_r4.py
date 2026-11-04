"""LX2-c round 4: writes the verifier fragment ledgers/LX2/LX2-c.json (rows, mutants, flags) from the evidence above.

Every row names the script or command whose output backs it (paths under ledgers/LX2/scripts/LX2-c-r4/out/).
Run from the checkout root: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r4/build_fragment_r4.py
"""

import json
from datetime import UTC, datetime
from pathlib import Path

R = "ledgers/LX2/scripts/LX2-c-r4/out/"
PAGE = "course/modules/LX/LX2/project.html"


def row(rid, check, location, status, evidence, fix=""):
    return {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix}


rows = [
    row("proj-gates-tooling", "gate", f"{PAGE}; tests/labs/LX2/lab-LX2-project-{{1,2,3}}.py", "PASS",
        f"ledgers/LX2/scripts/LX2-c-r4/run_checks.sh, outputs in {R}: check_pages LX2: PASS (check_pages.txt); "
        "check_dag LX2: PASS; check_projects LX2: PASS; run_labs LX2: PASS (7/7); run_graders LX2: 'no autograder "
        "(grading: rubric)'; ruff check tests/labs/LX2: 'All checks passed!'; ruff format --check: '7 files already "
        "formatted'; mypy --no-incremental on the three project twins: 'Success: no issues found in 3 source files'. "
        "verify_refs.py --unit LX2 (verify_refs_unit.txt): 'live re-verification of LX2: 6 of 560 entries, 0 problems', "
        "exit 0. pytest -k LX2 over tests/test_labs.py, tests/test_page_checks.py, tests/test_run_labs.py: 7 passed "
        "(pytest_lx2.txt). tools/mutate_graders.py --unit LX2: no output, exit 0 (rubric unit)."),
    row("proj-page-smoke", "2.5-2.9 page_smoke", PAGE, "PASS",
        f"Run alone: tools/page_smoke.py --unit LX2 --pages project (page_smoke_project.txt): 'page_smoke "
        "modules/LX/LX2/project.html: PASS', 'page_smoke LX2: PASS', exit 0; lab timings 0.0 s each; boot 1.1 s."),
    row("proj-labs-twins-alone", "2.5 labs", "tests/labs/LX2/lab-LX2-project-1.py, -2.py, -3.py", "PASS",
        f"Each twin run alone as python -I -W error <twin> (twin-project-{{1,2,3}}.txt, exit 0; .err files empty). "
        "git diff 67a2d13e HEAD -- tests/labs/LX2 shows no change to the project twins since the round-3 pin."),
    row("proj-page-code-equals-twin", "2.5 labs", f"{PAGE} lines 101-186, 238-316, 361-469", "PASS",
        f"ledgers/LX2/scripts/LX2-c-r4/page_vs_twin_r4.py ({R}page_vs_twin_r4.txt): lab 1 and lab 3 page code equal "
        "the twin (modulo final newline); lab 2 differs from its twin only at page lines 308 and 310 (hit_rate = ___, "
        "bias = ___). Page code with the blanks filled runs with exit 0, empty stderr, and stdout equal to the page "
        "expected block; each twin's stdout equals its page expected block."),
    row("proj-rung1-hypothesis-and-steps", "2.5 labs / 2.4 maths", f"{PAGE} lines 100, 203-232", "PASS",
        f"recompute_r4.py ({R}recompute_r4.txt): Lab 1 errors [1,-3,2,0,-4,3,-2,5], 4 of 8 hits, 0.5000, bias 2/8 = "
        "0.2500, edge [15,19], strict 2 of 8 = 0.2500, one hit = 1/8 = 0.1250. Line 100 matches. Line 210 lists the "
        "same errors; line 216 e13 = +1, e14 = -3; line 217 strict rate 0.2500; line 218 2/8; line 219 13/24 is "
        "0.5416 repeating 6 and rounds to 0.5417 under either tie rule, and no printed value in the three labs is an "
        "exact tie ('ties [False, False]' for Labs 1 and 2; Lab 3 13/24 and 51/24 not ties). Line 231-232 threshold "
        "2 against Part C 0.2500 is consistent."),
    row("proj-rung2-numbers-and-claims", "2.5 labs / 2.2 numbers", f"{PAGE} lines 237, 328", "PASS",
        "recompute_r4.txt: Lab 2 errors [-1,2,6,1,-2,-5]; 4 of 6 = 0.6667; bias 1/6 = 0.1667; edge [14,17]; mean of "
        "absolute errors 17/6 = 2.8333; hits over 8 = 0.5000; strict band 2 of 6 = 0.3333. Lines 237 and 328 match."),
    row("proj-rung2-instant-check-mutants", "2.6 instant check", "ledgers/LX2/mutants/mut-lab2-*.py (5 files)", "PASS",
        f"lab2_r4_check.py ({R}lab2_r4_check.txt) and lab2_check_r3_rerun.txt: all five mut-lab2-*.py fixtures carry "
        "the page's header and their whole block differs from the expected block: strict-band (line 3), bias-mean-abs "
        "(2.8333), bias-sign-flip (-0.1667), hit-over-8 (0.5000), truncated-hit-rate (0.6666). All killed."),
    row("proj-rung2-student-error-mutants", "2.6 instant check (student-error mutants)",
        "ledgers/LX2/mutants/r3_lab2_*.py (5) and r4_lab2_*.py (4, new this round)", "PASS",
        f"lab2_r4_check.py ({R}lab2_r4_check.txt): r3 mutants (percent, sign reversed, rung-1-length hit rate, rung-1-length "
        "bias, hit count added) and four new r4 mutants (make_r4_mutants.py, written from the twin with each "
        "replacement asserted to apply once): hit rate over H-1 (prints 0.8000), bias dropping month 13 (0.3333), "
        "forecast of month t-1 (line 2 of output differs), hit rate to three decimals (0.667). All killed. Round-2 "
        "candidates (bias over H-1, bias over hit count, bias from hit errors only, one-sided band, strict band) "
        "re-run from lab2_check_r3.py: all kill (lab2_check_r3_rerun.txt)."),
    row("proj-rung2-alternatives", "2.6 instant check (over-constraint)",
        "ledgers/LX2/scripts/LX2-c-r4/alts/*.py; ledgers/LX2/mutants/alt-lab2-float-division.py", "PASS",
        f"lab2_r4_check.py ({R}lab2_r4_check.txt): three new correct alternatives (integer half-up on numerator and "
        "denominator; decimal ROUND_HALF_UP on the exact quotient; a class-based Window) and the existing float-division "
        "alternative all print the whole expected block ('alternatives failing: 0'). lab2_check_r3_rerun.txt: five "
        "round-3 alternatives also pass."),
    row("proj-lab3-numbers", "2.2 numbers / 2.5 labs", f"{PAGE} lines 360, 470-501, 573, 597", "PASS",
        "recompute_r4.txt (own seeded generator, random.Random(20261103), exact Fraction, decimal half-up): Part B 13 of 24, "
        "0.5417; Part C 51/24 = 2.1250; Part D [14,15,16,19,22,24,26]; Part E 8 at months 34 and 35, earliest 34; Part F "
        "11/12 = 0.9167 (the only integer sum in -200..200 printing 0.9167). Printed Part A rows equal the recomputed "
        "errors. Prose: 13/15 = 0.8667, -3/15 = -0.2000 (months 13-27 sum -3, 13 hits), 54/9 = 6.0000 and 0/9 = 0.0000 "
        "(months 28-36 sum 54, errors 3 to 8), sum check 51 (line 501); strict band 6 of 24 = 0.2500 (line 573); "
        "rolling 56/12 = 4.6667 at month 36 (months 25-36, line 597)."),
    row("proj-lab-generator-description", "2.5 labs / docstring", f"{PAGE} lines 361-391, 419-427; lab-LX2-project-3.py", "PASS",
        "Docstring lines 363-366: one randint(-3, 3) draw per month t = 1..36 in order, realised 100 + 2t + noise, 6 "
        "units less from month 28. simulate_realised() (lines 419-427) does this; recompute_r4.py reproduces the Part A "
        "values from the same seed. Line 371 'Only the validation window enters the outcomes measures' matches Parts B-E "
        "(months 13-36 only); Part F is labelled as not part of the outcomes measures (line 386-387)."),
    row("proj-exemplar-a-numbers", "2.2 numbers", f"{PAGE} lines 558-597", "PASS",
        "Every number in exemplar A rechecked in recompute_r4.txt: 2.1250 (51/24 = 2.125, line 571); 13/24 = 0.5417; "
        "-3/15, 13/15, 54/9, 0/9 (line 572); strict band 6 of 24 = 0.2500 (line 573); errors of months 28-36 from 3 to 8 "
        "(line 559); 9 post-change months (line 585); rolling 56/12 = 4.6667 (line 597). Calibration 11/12 = 0.9167 (line "
        "559)."),
    row("proj-exemplar-b-numbers", "2.2 numbers", f"{PAGE} lines 625, 637, 649", "PASS",
        "Months 13-27 errors lie in [-3, 3] (recompute_r4.txt 'errors 13-27'); 13 hits of 24 = 0.5417 and bias 2.1250 "
        "(line 637); window 24 months (line 649, Lab 3 Part A)."),
    row("proj-exemplar-calibration", "2.5 rubric scores (calibration)",
        f"{PAGE} exemplar A lines 552-617 (data-scores 4,4,4,4,3); exemplar B lines 619-682 (data-scores 2,2,2,1,1)", "PASS",
        "Scored from the rubric descriptors (lines 538-544) and the passage text: exemplar A C1 4, C2 4, C3 4, C4 4, C5 3 "
        "(the unmarked rolling-window sentence, line 596); exemplar B C1 2, C2 2, C3 2, C4 1, C5 1 (no key with a locator, "
        "line 673). Both match the official scores exactly and are within one level. Caveat: the annotations were read "
        "before these scores were written, so this is not a blind run."),
    row("proj-exemplar-b-c5-annotation", "2.3 grades / rubric annotation", f"{PAGE} lines 673, 677-678", "PASS",
        "Line 673: the keyed sentence carries data-cite=\"frb2026fed\" and no data-locator; the CFA sentence carries no "
        "data-cite; annotation lines 677-678 names both defects and the unread requirement."),
    row("proj-exemplar-b-unread-requirement", "2.3 grades / attribution", f"{PAGE} lines 673, 678", "PASS",
        "Line 673 states what SR 26-2 requires, without a locator; the annotation (line 678) says it should read not stated "
        "here, consistent with the page's source note. The statement is not graded on the exemplar."),
    row("proj-source-supersession", "2.1 attribution / locator", f"{PAGE} line 350", "PASS",
        f"Plain curl of the SR 26-2 letter PDF (fetch_sr2602_r4.sh; HTTP 200, 237,044 bytes). sr2602_checks_r4.txt: the cover "
        "letter text 'the attached Revised Guidance on Model Risk Management, which supersedes and replaces SR letter 11-7 "
        "... and SR letter 21-8' is on PDF page 1; the 'Supersedes:' list is on PDF page 2 after the signature. The page's "
        "sentence is a grade-C paraphrase without quotation marks (the Board, OCC and FDIC 'issue' the attachment), which "
        "the grade allows; the dates (April 17, 2026) match PDF page 1."),
    row("proj-source-applicability", "2.1 attribution / locator", f"{PAGE} line 351", "PASS",
        "sr2602_checks_r4.txt: 'Applicability: This letter is expected to be most relevant to banking organizations with "
        "over $30 billion in total assets regulated by the Federal Reserve.' on PDF page 1; the page's sentence (line 351) "
        "matches it, with locator 'cover letter, paragraph headed Applicability'."),
    row("proj-source-attachment", "2.1 attribution / scope", f"{PAGE} lines 351-352, 609", "PASS",
        "Disclosure only. Lines 351-352 say the attachment was not read and that no statement about it is made. The same "
        "PDF contains the attachment (PDF pages 2-15; headings 'Components of Model Validation' and 'Conceptual "
        "Soundness' on page 10, 'Outcomes Analysis' and 'Ongoing Model Monitoring' on page 11; sr2602_checks_r4.txt). The "
        "disclosure is accurate; the scope consequence is recorded as the FAIL row proj-rung3-sr26-standard."),
    row("proj-citations-registry", "2.1 registry", "references/references.json; "+PAGE+" lines 350-351, 609, 673, 703-709", "PASS",
        "python -I check of references/references.json: frb2026fed (year 2026, verified_by issuer, URL sr2602.htm), "
        "cfandcode, gpondsecurities, gpondsecuritiesb, gpo1983dirks (year 1983), gpo1997united (year 1997) all present. "
        "verify_refs --unit LX2: 0 problems. Claims cite frb2026fed only (lines 350, 351, 609, 673); the five other keys "
        "appear only in the reading list, which the page says is not cited for any claim."),
    row("proj-notation", "2.4 notation", PAGE, "PASS",
        f"macros_r4.py ({R}macros_r4.txt): \\frac 2, \\hat 4, \\le 3, \\sum 2, \\operatorname 1 only; no registered macro "
        "(\\E, \\Prob, \\R, \\indic, \\SR, \\PBO, \\FDR) and no registered symbol (T, \\Phi, \\gamma_3, R^\\ast) appears. "
        "Symbols: H (window length, plan section 2.4), t, e_t, y_t, \\hat{y}_t, bias, M1, M2. No collision."),
    row("proj-dag-and-links", "2.9 DAG and links", f"{PAGE} lines 62, 68, 78; course/modules/LX/LX2/L04.html lines 97, 113", "PASS",
        "check_dag LX2: PASS. Only concept link: line 78 model-risk-management -> L04.html#def-model-risk-management (dfn at "
        "L04.html line 97). Anchors L04.html#s4 resolve (L04.html line 113, h2 id=s4). grep for out-of-closure names "
        "(grep_checks_r4.txt): zero hits for reconcil, integrity, spreadsheet, value-at-risk, stress test, backtest, "
        "overfit, efficient market, agency cost, adverse selection, moral hazard, Kyle, statistical power, hypothesis test, "
        "standard error, inference, confidence interval, significance, central clearing, voluntary disclosure."),
    row("proj-standard-error-term", "2.2 undefined terms", PAGE, "PASS",
        "grep_checks_r4.txt: 'standard error' 0 hits; 'inference|confidence interval|p-value|significan' 0 hits."),
    row("proj-validation-window-term", "2.4 defined terms / notation", f"{PAGE} lines 56, 64, 66, 109, 223, 347-348", "PASS",
        "Line 56: calibration months 1-12, validation months 13-36, H = 24 defined with H defined under Hit rate (line 64). "
        "Line 64: H per measure; Lab 1 H = 8, Lab 2 H = 6. Line 66: bias summed over the same window with the same H. "
        "Lab 1 docstring (line 109) H = 8, Lab 2 (line 246) H = 6, Lab 3 (line 371) H = 24: consistent."),
    row("proj-lab1-sections-claim", "2.5 labs / claims about the lab", f"{PAGE} line 96 vs lines 101-122, 187-199", "PASS",
        "Line 96: 'The lab does not test conceptual soundness, limitations or monitoring.' Lab 1 code (lines 101-186) "
        "prints Parts A-D only; expected block lines 187-199. The claim is accurate."),
    row("proj-spec-complete", "2.1 spec completeness (questions a student would ask)", f"{PAGE} lines 336-345, 703-709", "PASS",
        "Context: 4 sentences (line 336). Inputs (line 338): case documentation, Lab 3 table (seed 20261103, 24 months), "
        "source note. Required outputs (line 340): validation.md with four named sections in order, and self_assessment.md. "
        "Constraints (line 342), grading mode (line 344), reading list (lines 703-709). Questions a competent student would "
        "still ask, none blocking: (1) where validation.md and self_assessment.md are handed in (no submission entry; the "
        "FC1 and E3 project pages have none either); (2) the expected length of the report. The question which SR 26-2 "
        "standard applies is the FAIL row proj-rung3-sr26-standard."),
    row("proj-spec-ladder", "2.6 ladder structure", f"{PAGE} lines 40-48, 94-96, 235, 308-310, 691-698", "PASS",
        "Order: rung 1 worked example (Lab 1, line 98), rung 2 completion (Lab 2, line 235, class 'lab completion', blanks at "
        "lines 308 and 310), rung 3 independent project (spec, rubric, Lab 3 at line 358), rung 4 stretch (line 691, "
        "'Not graded'). check_projects LX2: PASS. Rung 1 content and rung 4 content were FAILs in round 3 and are PASS now "
        "(rows proj-rung1-plan-scope, proj-rung4-open-ended). Rung 3 scope against the curriculum brief is the FAIL row "
        "proj-rung3-sr26-standard."),
    row("proj-hours", "2.6 hours arithmetic", f"{PAGE} lines 33, 521-527; course/modules/LX/LX2/index.html line 29", "PASS",
        "Component hours 2+2+2+3+3+2 = 14 (lines 521-527); data-hours-project 14 (line 33); hub data-hours-lessons 36 + "
        "project 14 = 50 (index.html line 29); 14/50 = 28 percent (line 527). My own estimates: rung 1 read and annotate "
        "2-2.5 h; rung 2 about 1 h; intake 1.5-2 h; outcomes analysis 2-3 h; report 3-4 h; self-assessment about 2 h; "
        "total 12-15 h, within 30 percent of 14 h."),
    row("proj-rubric-observable", "2.6 rubric observability", f"{PAGE} lines 534-544", "PASS",
        "Every level descriptor names an observable element (an assumption and its test, a band rule, a threshold and its "
        "basis, a key and a locator, a Part letter, a metric and a frequency). No vague descriptor remains; none of 'looks sound', 'checks accuracy', 'notes some caveats', "
        "'monitors regularly', 'cites sources' appears (grep)."),
    row("proj-rubric-criteria-count", "2.6 rubric structure", f"{PAGE} lines 536-546, 552, 619, 684", "PASS",
        "Five criteria C1-C5, each a row with one th and exactly four td cells (lines 540-544); exemplar A data-level 4 (line "
        "552) and exemplar B data-level 2 (line 619); self-assessment data-rubric=\"rubric\" data-exemplars=\"exemplar-a "
        "exemplar-b\" (line 684). check_projects LX2: PASS."),
    row("proj-autograder-na", "2.6 grading mode", f"{PAGE} line 344", "PASS",
        "Line 344: 'Rubric only. There is no autograder.' run_graders.py --unit LX2: 'no autograder (grading: rubric)'."),
    row("proj-adversarial-na", "2.6 grading mode", f"{PAGE} line 344", "PASS",
        "Line 344: 'No adversarial review is used for this project.' Plan section 12 Q14 (not adversarial, no question bank)."),
    row("proj-atlas-na", "2.6 Atlas milestones (not applicable)", PAGE, "PASS",
        "grep -i atlas: 0 hits on the page. The curriculum's 'your own Atlas models' is replaced by the SIMULATED case under "
        "plan B4 (recommended resolution Q6, binding under the architect decisions). See the separate SR 26-2 scope row."),
    row("proj-studio-na", "2.6 studios (not applicable)", PAGE, "PASS",
        "No studio on the project page (grep -i studio: 0 hits)."),
    row("proj-data-and-figures-na", "2.8 data and figures (not applicable)", PAGE, "PASS",
        "grep_checks_r4.txt: svg, img, figure, data-files, data-chart, canvas: 0 hits. No dataset is read (plan section 6)."),
    row("proj-banned-and-process-words", "2.9 banned phrases and process words", PAGE, "PASS",
        "grep_checks_r4.txt: banned strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an "
        "exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, "
        "clearly), process words (builder, verifier, architect, fragment, ledger, agent, placeholder, round N, studio, "
        "atlas, debate, autograder, grader, mutant) and ellipsis: 0 hits. 'drafting' (line 525) is a learner activity, and "
        "'no autograder' (line 344) is negated."),
    row("proj-case-realised-source", "2.5 case documentation vs labs", f"{PAGE} lines 89-90; Lab 1 REALISED; Lab 2 REALISED; Lab 3 table",
        "PASS",
        "recompute_r4.txt: Lab 1 values agree with the Lab 3 case series at month 18 only ('LAB1 vs case series agree at "
        "months [18]'); Lab 2 values agree at month 13 only ('LAB2 ... [13]'). Line 89 item (e) and line 90 say this."),
    row("proj-rung2-alt-fixture", "fixture consistency", "ledgers/LX2/mutants/alt-lab2-float-division.py; mut-lab2-*.py", "PASS",
        "lab2_r4_check.py / lab2_check_r3_rerun.txt: every fixture's header line equals the page's Lab 2 header "
        "(header_match=True for all 15 fixtures); alt-lab2-float-division.py matches the whole block (body_differing_lines=[])."),
    row("proj-rung1-plan-scope", "2.6 ladder: rung 1 scope against plan section 5.1 item 1",
        f"{PAGE} lines 203-232; plans/LX2-build-plan.md lines 335-336", "PASS",
        "Round-3 FAIL re-verified and fixed. Lines 203-232 now work the four element checks in the order of section 5.2 "
        "(Element 1 conceptual soundness, line 206; Element 2 outcomes analysis, line 213; Element 3 limitations, line 222; "
        "Element 4 ongoing monitoring, line 228), each step with a 'The reason' annotation; the element 2 arithmetic is "
        "checked in recompute_r4.txt."),
    row("proj-rung4-open-ended", "2.6 ladder: rung 4 genuinely open-ended", f"{PAGE} lines 691-698; plans/LX2-build-plan.md lines 343-344",
        "PASS",
        "Round-3 FAIL re-verified and fixed. Lines 693-696: 'Not graded. Neither item has a fixed answer.' Item 1 validates a "
        "second SIMULATED model case (scope set by the student); item 2 compares two limitations sections. Matches plan "
        "section 5.1 item 4. No fixed yes-or-no or single comparison is required."),
    row("proj-exemplar-a-m1-window", "2.4 mathematics / 2.3 grades", f"{PAGE} lines 58, 87, 559", "PASS",
        "Round-3 FAIL re-verified and fixed. Line 559 tests M1 on the validation window (months 13-36, the window line 58 "
        "states), with Part C (2.1250) and the Part A rows for months 28-36; the calibration bias (Part F, 0.9167) is "
        "described as a check of the fit, not a test of M1, which matches line 56."),
    row("proj-exemplar-a-derivation-claim", "2.2 numbers: derivation statement", f"{PAGE} lines 527, 559",
        "PASS",
        "Round-3 FAIL re-verified and fixed. Line 559 gives 11 as the sum of the calibration errors and states that 11 is the "
        "only integer sum that prints as 0.9167 over 12 months, citing Part F. recompute_r4.txt: 'integer sums ... [11]' "
        "(only 11 in -200..200). Line 527's claim now agrees with the exemplar."),
    row("proj-rung3-sr26-standard", "2.6 rung 3 scope vs curriculum; 2.1 attribution",
        f"{PAGE} lines 46, 336-344, 350-352; curriculum/06-profession-capstone.yaml lines 82-84; plans/LX2-build-plan.md lines 294 (section 3, L04) and 349-350 (section 5.2)",
        "FAIL",
        "Curriculum brief (06-profession-capstone.yaml:82-83): 'Write a validation report to the standard of SR 26-2 (which "
        "superseded SR 11-7 in 2026) ... conceptual soundness, outcomes analysis, limitations, ongoing monitoring.' The "
        "page's rung 3 and spec (lines 46, 336-344) require the four elements but not the SR 26-2 standard. The source note "
        "(lines 351-352) says the attachment was not read. The attachment is in the same PDF that the registry key points to "
        "(fetch_sr2602_r4.sh, HTTP 200; sr2602_checks_r4.txt): 'Components of Model Validation' and 'Conceptual Soundness' "
        "(PDF page 10), 'Outcomes Analysis' and 'Ongoing Model Monitoring' (PDF page 11). This verifier read those headings "
        "only, not the attachment text. Plan section 3 (L04) and section 5.2 require the SR 26-2 element names to come from "
        "the page the builder reads. The gap is therefore avoidable and the rung-3 scope is narrower than the curriculum brief.",
        "Read the attachment's validation passages (PDF pages 10-11 and 'Components of Model Validation'), state in the spec "
        "which of its expectations the report must meet for each element, each with data-cite=\"frb2026fed\" and a "
        "data-locator (PDF page); mark the limitations element as the curriculum's list if the attachment does not head it. "
        "Alternatively the architect amends the brief at curriculum/06-profession-capstone.yaml:82-83 to drop 'to the standard "
        "of SR 26-2' (a curriculum change; builders do not edit curriculum files), and the page then says so."),
    row("proj-define-model-owner", "2.9 define before use (plan section 2.1 item 5)", f"{PAGE} line 232 (first use); line 596",
        "FAIL",
        "'model owner' first appears at line 232 ('the example names a monthly frequency and the model owner as reviewer') with "
        "no definition. The only definition is in exemplar A at line 596 ('Role: the model owner, who signs the monthly "
        "planning figure and receives the rolling bias'), which comes later. grep -n owner (grep_checks_r4.txt) gives lines "
        "232 and 596 only. Plan section 2.1 item 5 names 'model owner' among the terms to define in prose at first use.",
        "At line 232, define the term at first use with a plain <dfn> (no data-concept), for example 'the model owner, the "
        "person who signs the monthly planning figure', or replace it with 'the reviewer named in the rubric's role'."),
    row("proj-m2-statement-consistency", "2.4 assumptions complete; internal consistency",
        f"{PAGE} lines 58, 87, 107-108 (Lab 1 docstring), 208", "FAIL",
        "Line 58 (conventions) states M2 as 'the forecast for month t is issued before month t starts and uses no information "
        "from month t'. Line 87 (case documentation, which line 78 calls 'the whole documentation of the case') states M2 as "
        "'the forecast for month t uses no information from month t' with no issue-timing clause. Element 1 (line 208) and "
        "the Lab 1 docstring (lines 107-108) follow line 58. The timing clause is therefore an assumption that the case "
        "documentation does not list, and item (b) on line 89 says issue dates are not documented. Lab 1 docstring line 107 "
        "also states M1 as 'the model's stated assumption' while line 58 and line 87 state it as holding over the validation "
        "window.",
        "Make the case-documentation M2 at line 87 match line 58 (state the timing clause as an assumption without dates), or "
        "remove the clause from lines 58, 208 and 108; and make the Lab 1 docstring M1 (line 107) match lines 58 and 87."),
]

mutant_names = [
    ("mut-lab2-strict-band", "Band test is strict (|e| < 2), so months at the edge of the band are counted as misses."),
    ("mut-lab2-bias-mean-abs", "Bias is the mean of the absolute errors instead of the signed mean error."),
    ("mut-lab2-bias-sign-flip", "Bias sign is reversed: realised minus forecast is used instead of forecast minus realised."),
    ("mut-lab2-hit-over-8", "Hit rate divides the hit count by 8, the length of rung 1, instead of H = 6."),
    ("mut-lab2-truncated-hit-rate", "Hit rate is truncated to four places before printing, so the half-up rule is never applied."),
    ("r3_lab2_hit_rate_as_percent", "Hit rate printed as a percentage (hits / H times 100) where the page defines a share between 0 and 1."),
    ("r3_lab2_bias_sign_reversed", "Bias sign reversed (realised minus forecast) against the page's forecast-minus-realised convention."),
    ("r3_lab2_hit_rate_rung1_length", "Hit rate divided by 8, the length of rung 1's window, instead of H = 6 of this window."),
    ("r3_lab2_bias_rung1_length", "Bias divided by 8, the length of rung 1's window, instead of H = 6 of this window."),
    ("r3_lab2_bias_adds_hit_count", "Hit count added to the error sum before dividing by H (sum over two different quantities)."),
    ("r4_lab2_hit_rate_horizon_minus_one", "Hit rate divides the hit count by H - 1 = 5, an off-by-one horizon, instead of H = 6."),
    ("r4_lab2_bias_drops_first_month", "Bias sums the errors of months 14 to 18 only, dropping month 13, then divides by H = 6."),
    ("r4_lab2_forecast_lagged_one_month", "Forecast uses the previous month index, forecast(t - 1), so each error is one month stale."),
    ("r4_lab2_hit_rate_three_decimals", "Hit rate is printed to three decimals (0.667), while the page prints four decimals."),
]
mutants = [
    {"name": n, "description": d,
     "killed_by": "rung-2 instant check (whole-block compare): ledgers/LX2/scripts/LX2-c-r4/out/lab2_r4_check.txt"}
    for n, d in mutant_names
]
round2_candidates = [
    ("r2-bias-denominator-horizon-minus-1", "Bias divides the error sum by H - 1 = 5 (off-by-one horizon)."),
    ("r2-bias-over-hit-count", "Bias divides the error sum by the hit count (4) instead of H."),
    ("r2-bias-sum-of-hit-errors-only", "Bias is the mean of only the errors of hit months."),
    ("r2-one-sided-band-hit-rate", "Hit test is one-sided (e <= 2), so large negative errors count as hits."),
    ("r2-strict-band-hit-rate", "Hit test counts |e| < 2, so edge months 14 and 17 are misses."),
]
for n, d in round2_candidates:
    mutants.append({"name": n, "description": d,
                    "killed_by": "rung-2 instant check, candidate in ledgers/LX2/scripts/LX2-c-r3/lab2_check_r3.py "
                                 "(re-run: ledgers/LX2/scripts/LX2-c-r4/out/lab2_check_r3_rerun.txt)"})

fragment = {
    "unit": "LX2",
    "slice": "LX2-c",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for LX2-c, round 4 (did not build LX2; no shared context with the builders)",
    "pin": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba",
    "base": ("round 3 fragment /Users/billyribeiro/.fanout/frags/E-LX2-c.round3.json at pin 67a2d13e7575608e95b2e34a9c7c2a82c61b117b. "
             "Delta read with git diff -U0 67a2d13e HEAD over course/modules/LX/LX2/project.html (every hunk read; the page was also read in full, "
             "725 lines), course/modules/LX/LX2/index.html (4 lines, outside the slice, read for the placement wording), "
             "tests/labs/LX2 (project twins: no change), ledgers/LX2/mutants (r3_lab2 fixtures; r3_l03/r3_l04 are other slices)."),
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE4-LX2-c",
    "scratch": "/tmp/lx2c-r4-src.IRKp30 and /tmp/lx2c-r4-sr.roTi4T (SR 26-2 letter by plain curl, converted with pdftotext -layout)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "gpo1983dirks: references/references.json title reads 'Dirks v. SEC, 463 U.S. 646 (1982)' while its year field is 1983. "
        "project.html prints no year for it, so no row here depends on it; the registry owner should reconcile the two fields.",
    ],
    "freshness_flags": [],
    "notes": [
        "Full read: project.html (725 lines) read in full; the twins are identical to the page code (page_vs_twin_r4.txt).",
        "Round-3 FAIL rows proj-rung1-plan-scope, proj-rung4-open-ended, proj-exemplar-a-m1-window and proj-exemplar-a-derivation-claim "
        "are re-verified from scratch and now PASS. Every round-3 PASS row was re-run or re-read this round (its subject, project.html, "
        "changed in the delta), so no row is carried forward. Row ids are kept.",
        "New FAIL rows this round: proj-rung3-sr26-standard (scope narrower than the curriculum brief; the SR 26-2 attachment is in the same PDF "
        "and was not read beyond its headings), proj-define-model-owner (define-before-use), proj-m2-statement-consistency (M2 differs between "
        "lines 58 and 87).",
        "SR 26-2: one plain curl of https://www.federalreserve.gov/supervisionreg/srletters/SR2602.pdf (HTTP 200, no bot check or login). "
        "No other network access except tools/verify_refs.py --unit LX2 (its own live check).",
        "Calibration: the exemplar annotations were read before scoring, so the calibration is not blind (stated in proj-exemplar-calibration).",
        "Not checked: the rendered page in a browser (no browser session; labs.js compareOutput read at lines 42-60 and 133-141; the rubric "
        "self-assessment form (rubric.js) was not exercised); horizontal scroll at 360 px; the full repository gate (targeted run only, per "
        "the project's targeted-test rule); build_site.py --check; the L01-L04 lessons and cards (outside slice c).",
        "The SR 26-2 attachment was not read beyond the headings located by sr2602_checks_r4.py. Statements about its content are not made here.",
        "mutate_graders.py --unit LX2 is a no-op for a rubric unit; the lab-2 student-error mutants were run as the instant-check candidates.",
        "19 mutants are listed: 5 mut-lab2-*.py files, 5 r3_lab2_*.py files, 4 new round-4 files (ledgers/LX2/mutants/r4_lab2_*.py), and 5 "
        "round-2 candidates that exist only in the round-3 script. All 19 are killed by the rung-2 whole-block compare.",
        "Correct alternatives: 3 new (scripts/LX2-c-r4/alts) and 1 existing (alt-lab2-float-division.py); all pass.",
    ],
    "summary": ("LX2-c round 4: FAIL. 45 rows: 42 PASS (the 42 round-3 row ids kept; the four round-3 FAILs now PASS) and 3 new FAIL "
                "(proj-rung3-sr26-standard, proj-define-model-owner, proj-m2-statement-consistency). Every number on project.html, "
                "the three project lab twins, their expected blocks and the exemplar figures was recomputed independently. "
                "19 lab-2 mutants all killed; 4 correct alternatives pass."),
}

out = Path("ledgers/LX2/LX2-c.json")
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants))
