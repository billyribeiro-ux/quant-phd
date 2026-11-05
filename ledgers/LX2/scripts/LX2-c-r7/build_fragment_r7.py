"""Assemble the LX2-c round 7 ledger fragment from the outputs in ledgers/LX2/scripts/LX2-c-r7/out/ and the mutant files."""
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = "ledgers/LX2/scripts/LX2-c-r7/out/"
SRC = Path(open("/tmp/lx2c-r7-dir.txt").read().strip()).name

P = "PASS"
F = "FAIL"

rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)


PAGE = "course/modules/LX/LX2/project.html"
row("proj-gates-tooling", "gate: check_projects, check_pages, check_dag, run_labs, run_graders, ruff, mypy, pytest subset",
    PAGE + "; tests/labs/LX2/lab-LX2-project-{1,2,3}.py", P,
    f"Re-run at pin 06994db1: check_projects LX2: PASS ({OUT}check_projects_LX2_r7.txt); check_pages LX2: PASS "
    f"({OUT}check_pages_LX2_r7.txt); check_dag LX2: PASS ({OUT}check_dag_LX2_r7.txt); run_labs LX2: PASS (7/7) "
    f"({OUT}run_labs_LX2_r7.txt); ruff check and ruff format --check tests/labs/LX2 clean ({OUT}ruff_check_LX2_r7.txt, "
    f"{OUT}ruff_format_LX2_r7.txt); mypy --no-incremental: 'Success: no issues found in 385 source files' ({OUT}mypy_r7.txt); "
    f"pytest -k LX2 over test_labs, test_page_checks, test_run_labs, test_page_smoke, test_memo_exemplars: 7 passed ({OUT}pytest_LX2_r7.txt); "
    "run_graders --unit LX2 --seeds 0-49: 'no autograder (grading: rubric)' (observed in the shell run).")
row("proj-page-smoke", "2.9 page_smoke", PAGE, P,
    f"tools/page_smoke.py --unit LX2 --pages project: 'page_smoke modules/LX/LX2/project.html: PASS' and 'page_smoke LX2: PASS' ({OUT}page_smoke_project_r7.txt); the three labs were timed in the browser runtime in the same run.")
row("proj-labs-twins-alone", "2.5 labs: twins alone under python -I -W error", "tests/labs/LX2/lab-LX2-project-1.py, -2.py, -3.py", P,
    f"{OUT}twin_vs_page_r7.txt: each twin exits 0 with 0 stderr bytes under python -I -W error; stdout tokens equal the page's expected tokens (101, 91, 206 tokens; exact-token-equal=True for all three).")
row("proj-page-code-equals-twin", "2.5 labs: page code equals twin", PAGE + " lines 98-201 (lab 1), 235-329 (lab 2), 367-511 (lab 3)", P,
    f"{OUT}twin_vs_page_r7.txt: lab 1 and lab 3 page code differs from the twin in 0 lines; lab 2 differs in exactly 4 diff lines, the hit_rate and bias lines that the page blanks as ___ (lines 308, 310).")
row("proj-rung1-hypothesis-and-steps", "2.5 labs / 2.4 maths", PAGE + " lines 100, 199, 210-232", P,
    f"{OUT}rederive_r7.txt (L1 lines): errors [1,-3,2,0,-4,3,-2,5], sum 2; hits 4 of 8; hit rate 0.5000; bias 0.2500; edge months [15,19]; strict band 2 of 8 = 0.25 (line 217); 1/8 = 0.1250 (line 224); the eight months give both signs (line 210).")
row("proj-rung2-numbers-and-claims", "2.5 labs / 2.2 numbers", PAGE + " lines 237, 328", P,
    f"{OUT}rederive_r7.txt (L2 lines): errors [-1,2,6,1,-2,-5]; hits 4 of 6; hit rate 2/3 -> 0.6667; bias 1/6 -> 0.1667; edge months [14,17]; hit count over 8 -> 0.5000 (line 328); mean absolute error 17/6 -> 2.8333 (line 328). All match the expected block (twin_vs_page_r7.txt).")
row("proj-rung2-instant-check-mutants", "2.6 instant check: mutants killed by the whole-block compare", PAGE + " lines 45, 237, 328; ledgers/LX2/mutants/r6_lab2_hard_coded_printed_values.py", P,
    f"Round 6 FAIL: a hard-coded typed value passes. The page now states this behaviour: line 45 ('compares the printed output only, so it does not grade how a blank was filled'), line 237 ('a blank typed as the value it prints passes too'), line 328 ('a blank typed as 0.6667 or 0.1667 prints the same block and passes'). Re-run: {OUT}blank_literal_check_r7.txt shows the typed-literal blanks print stdout identical to the completed twin with exit 0 and no stderr; {OUT}lab2_candidates_r7.txt: r6_lab2_hard_coded_printed_values.py survives. Ruling applied: a surviving grader behaviour the page states is not a FAIL. The disclosure is the only control (labs.js compareOutput compares printed tokens, and the expected block is always shown), so the rung-2 check stays open-book and the verifier records it as a known limit.")
row("proj-rung2-student-error-mutants", "2.6 instant check: student-error mutants, rounding rule", PAGE + " lines 68, 124, 256, 283, 328; ledgers/LX2/mutants/r6_lab2_round_half_even_ties.py, r6_lab2_round_half_toward_plus_infinity.py, r6_lab2_float_format_ties_even.py, r7_lab2_rounds_through_python_round.py", P,
    f"Round 6 FAIL: tie-rule mutants pass. Re-derived: no printed value of rung 2 is an exact tie (2/3 and 1/6 are not ties; rederive_r7.txt 'L2 tie check'). The page now says (line 328) 'It also does not exercise the tie rule ... a rounding rule that differs from half up only at a tie, such as round half to even, prints the same block.' The four tie-rule survivors are exactly that class ({OUT}lab2_candidates_r7.txt). Every other student-error mutant is killed: the 29 killed faults include the off-by-one, sign, band, edge-list, window, bias and hit-rate errors; the five survivors are the four tie-rule mutants and the one literal-blank mutant. Ruling applied, as above: stated behaviour, not a FAIL.")
row("proj-rung2-alternatives", "2.5 / 2.6 alternative correct implementations pass (over-constraint check)",
    "ledgers/LX2/scripts/LX2-c-r5/alts/*.py; ledgers/LX2/scripts/LX2-c-r6/alts/*.py; ledgers/LX2/scripts/LX2-c-r7/alts/alt_r7_decimal_half_up.py; ledgers/LX2/mutants/alt-lab2-float-division.py", P,
    f"{OUT}lab2_candidates_r7.txt: all 10 correct alternatives print the expected block under the page's compare rule (alt-lab2-float-division, alt-r5-a1..a4, alt_r6_a1,a3,a4,a5, alt_r7_decimal_half_up: Decimal ROUND_HALF_UP quantize on the exact Fraction). None is killed.")
row("proj-rung2-alt-fixture", "2.6 fixture: each mutant and alternative is a complete module with a one-line docstring describing the error",
    "ledgers/LX2/mutants/r6_*.py; ledgers/LX2/mutants/r7_*.py", P,
    "Every r6 and r7 mutant is a complete module (runs under python -I -W error, exit 0 unless killed by an exception) whose docstring's first line reads 'Student error: ...' (checked by first-line print of each file).")
row("proj-lab3-numbers", "2.2 numbers / 2.5 labs (lab 3 rung-3 check)", PAGE + " lines 369, 479-511", P,
    f"{OUT}rederive_r7.txt (L3 lines) and {OUT}twin_vs_page_r7.txt: hits 13 of 24; 13/24 -> 0.5417; bias 51/24 = 17/8 -> 2.1250; edge months [14,15,16,19,22,24,26]; largest absolute error 8 at months 34 and 35, the earlier is 34; calibration sum 11, 11/12 -> 0.9167; the expected block of lab 3 equals its twin's output (206 tokens).")
row("proj-lab-generator-description", "2.2 / 2.5 labs: docstring vs code", PAGE + " lab 3 docstring lines 370-400 and code lines 402-476; tests/labs/LX2/lab-LX2-project-3.py", P,
    "Docstring vs code checked line by line: randint(-3,3) once per month 1 to 36 in order; shift -6 from month 28 (SHIFT_FROM=28); Part E picks max by (abs(error), -t), so the earliest month wins ties; only months 13 to 36 enter Parts B to E; no file is read (lab reads no file, line 366 holds).")
row("proj-exemplar-a-numbers", "2.2 numbers", PAGE + " lines 567-625 (exemplar A)", P,
    f"{OUT}rederive_r7.txt: 2.1250; 0.9167 from sum 11 over 12 months (only integer that prints 0.9167); months 28-36 errors 3 to 8, all positive; 13/24 -> 0.5417; sum 51 -> 2.125 -> 2.1250; months 13-27 sum -3, -3/15 = -0.2000, 13/15 = 0.8667; months 28-36 sum 54, 54/9 = 6.0000, 0/9 = 0.0000; strict band 6 of 24 = 0.2500; rolling 12-month bias at month 36 = 56/12 = 4.6667 (errors of months 25-36).")
row("proj-exemplar-b-numbers", "2.2 numbers", PAGE + " lines 646, 634 (exemplar B)", P,
    f"{OUT}rederive_r7.txt: 13 hits of 24 -> 0.5417; bias 2.1250; months 13 to 27 errors all within [-3, 3] (True).")
row("proj-exemplar-calibration", "rubric calibration (score exemplars blind, within one level)", PAGE + " lines 541-557 rubric; exemplar A 561-626; exemplar B 628-691", P,
    f"Blind scoring: the exemplar passages were extracted with annotations removed ({OUT}page_checks_r7.txt). Scored from the rubric descriptors only: exemplar A C1 4, C2 4, C3 4, C4 3, C5 3 against annotated 4,4,4,4,3 (every criterion within one level); exemplar B C1 2, C2 2, C3 2, C4 1, C5 1 against annotated 2,2,2,1,1 (exact). Caveat: I read the annotated page earlier in this round, so the blind step is by descriptor, not by a fresh reader. The C4 divergence turns on the undefined term 'basis' (row proj-rubric-observable).")
row("proj-exemplar-b-c5-annotation", "2.4 / rubric C5 annotation", PAGE + " lines 682, 686-687", P,
    "Annotation at 686-687 matches the passage: the claim at line 682 carries data-cite frb2026fed with no data-locator (no locator), the CFA Code sentence carries no key; the attachment section I statement (printed page 2, PDF page 4) contradicts 'requires' (quote_check_r7.txt).")
row("proj-exemplar-b-unread-requirement", "2.4 unread-standard rule", PAGE + " lines 682, 687", P,
    f"{OUT}quote_check_r7.txt and the fetched SR2602.pdf: 'This guidance does not set forth enforceable standards or prescriptive requirements' is an exact substring on combined PDF page 4 (printed page 2).")
row("proj-source-supersession", "2.3 registry / locator (supersession)", PAGE + " line 359 (source note)", P,
    f"Cover letter (sr2602.htm text line 1756; letter text line 30): 'which supersedes and replaces SR letter 11-7 ... and SR letter 21-8'; 'Supersedes:' list after the signature names both letters (letter text lines 57-62). The page's span is a condensed paraphrase with the locator 'cover letter, opening paragraph'; accurate.")
row("proj-source-applicability", "2.3 registry / locator (applicability)", PAGE + " line 360 (source note)", P,
    f"Exact sentence in the letter ('This letter is expected to be most relevant to banking organizations with over $30 billion in total assets regulated by the Federal Reserve.', letter text line 24; sr2602.htm line 1750); {OUT}quote_check_r7.txt: exact substring on PDF page 1.")
row("proj-source-attachment", "2.3 registry / locator (attachment quotes and printed pages)", PAGE + " lines 346-349, 360, 618", P,
    f"{OUT}quote_check_r7.txt: each attachment quote at lines 346-349 and 360 is an exact substring of the fetched SR2602.pdf text; printed pages match their locators (8, 9, 9, 7, 7, 9 and 2). The PDF-page part of the locators is a separate row (proj-attachment-quote-locators).")
row("proj-citations-registry", "2.1 citations: registry keys and verify_refs", "references/references.json (frb2026fed, cfandcode, gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united); " + PAGE + " data-cite values", P,
    f"verify_refs.py --unit LX2 (live): 'live re-verification of LX2: 6 of 560 entries, 0 problems' ({OUT}verify_refs_LX2_live_r7.txt); verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' ({OUT}verify_refs_offline_r7.txt). Keys cited on the page (page_checks_r7.txt): frb2026fed, cfandcode, gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united; claim spans cite only frb2026fed.")
row("proj-notation", "2.4 notation (notation/notation.json)", PAGE + " 65 inline math spans", P,
    "The page's symbols are t, H, e_t, \\hat{y}_t, y_t and \\operatorname{bias}. notation/notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} and the macros \\E, \\Prob, ...; none is used with another meaning; T is not used on this page (H is the planned horizon symbol, plan 2.4).")
row("proj-dag-and-links", "2.9 DAG: links and definitions", PAGE + " lines 62, 68, 78, 232", P,
    f"check_dag LX2: PASS ({OUT}check_dag_LX2_r7.txt). L04.html#s4 exists and states the band 2 inclusive and the half-away-from-zero rounding to four places (L04.html section 4); L04.html#def-model-risk-management exists (L04.html line 97, dfn data-concept). Every href resolves ({OUT}page_checks_r7.txt).")
row("proj-standard-error-term", "2.4 terms before definition", PAGE + " lines 60, 62, 64", P,
    "e_t is defined at line 60 ('Error and sign') before its first use in the Hit definition at line 62; the hit rate (line 64) uses H and hits defined earlier.")
row("proj-validation-window-term", "2.4 / 2.5 terms before definition", PAGE + " lines 37, 55-56, 58, 64", P,
    "Windows and H are defined at lines 55-56 before uses at 58-108, 200-228 and 346-348. Note (non-blocking): the lede at line 37 says 'the outcomes measures' before the conventions define hit rate and bias (lines 61-66); the term 'outcomes analysis' is forward-referenced explicitly at line 44.")
row("proj-lab1-sections-claim", "2.2 prose claims about what the lab computes", PAGE + " lines 96, 204 vs lab 1 code (lines 101-201)", P,
    "Line 96 says the lab computes the outcomes analysis (the second section) and not the other three; lab 1 code computes hits, hit rate, bias and edge months only (lines 143-183) and prints Parts A to D only.")
row("proj-spec-complete", "2.6 spec completeness (questions a student would ask)", PAGE + " lines 333-353 (dl.spec), 337-340 inputs and outputs, 701-707", P,
    "The spec names context, inputs (1)-(3), required outputs (four sections in order plus self_assessment.md), constraints, grading and the reading list. Two questions remain unanswered and do not block a start: (a) the expected length or layout of validation.md; (b) whether self_assessment.md is graded (line 340 calls it a summary; grading is not stated).")
row("proj-spec-ladder", "2.6 ladder", PAGE + " lines 40-47 (ladder), 98-201 (rung 1), 235-329 (rung 2), 333-353 and 367-511 (rung 3), 701-707 (rung 4)", P,
    "Four rungs in order; rung 1 fully solved and annotated (lab 1 output and worked steps 206-233); rung 2 completion lab with a shown expected block (class 'lab completion'); rung 3 spec and lab 3; rung 4 open-ended and not graded (line 702). check_projects LX2: PASS.")
row("proj-hours", "2.8 hours arithmetic", PAGE + " line 33 (data-hours-project 14), 530-536 (time budget); index.html lines 29, 44, 176", P,
    "Time budget rows 2 + 2 + 2 + 3 + 3 + 2 = 14 (lines 530-535); data-hours-project=14; hub data-hours-lessons=36 and data-hours-project=14, 36 + 14 = 50; 14/50 = 28 percent (line 536).")
row("proj-rubric-observable", "2.6 rubric: every level descriptor is observable", PAGE + " lines 549-553 (C1-C5 descriptors), 605-610 (exemplar A C4)", F,
    "Each descriptor was read. The term 'basis' is used in three descriptors and is never defined on the page (grep for 'basis': C2 level 3 at line 550 'one figure lacks its Part citation or its basis'; C4 level 4 at line 552 'a threshold with the basis for the threshold'; C4 level 3 at line 552 'the basis of the threshold or the reviewing role is missing'). Under the plan's own rule a descriptor that cannot be observed without that term is vague. The exemplar A 'Meets C4 level 4' (line 610) rests on a basis that compares two observed biases (line 605), which a reader could score as level 3, so the descriptor does not fix the score. Other descriptors (C1 level 4, C3 level 4, C5 levels 1-4) are observable.",
    "Define the term once on the page, for example 'the basis of a threshold is the number, from the case, the conventions or a Part row, that the threshold is set against, with its source named'. Replace 'its basis' in C2 level 3 with 'one figure lacks its Part citation'. Re-score exemplar A's C4 line against the defined term and keep the annotation consistent.")
row("proj-rubric-criteria-count", "2.6 rubric: five criteria, four cells each", PAGE + " lines 549-553, 561, 628", P,
    f"{OUT}page_checks_r7.txt: rows C1 to C5 each have one th and four td; data-scores has five entries for each exemplar (lines 561 and 628).")
row("proj-autograder-na", "2.5 grading mode", PAGE + " line 353", P,
    "Line 353: 'Rubric only. There is no autograder.' run_graders --unit LX2: 'no autograder (grading: rubric)'.")
row("proj-adversarial-na", "plan decision (no question bank)", PAGE + " line 353", P,
    "Line 353: 'No adversarial review is used for this project.' Plan Q14 and architect default: not adversarial.")
row("proj-atlas-na", "plan B4", PAGE, P,
    "grep -ci atlas course/modules/LX/LX2/project.html = 0 (no Atlas milestone or series referenced).")
row("proj-studio-na", "plan 2.2 / 5.x", PAGE, P,
    "The page is the LX2 project, not a studio; no studio requirement is stated or needed (check_projects LX2: PASS).")
row("proj-data-and-figures-na", "plan 2.4 / architect decision 16 (no figures, no data)", PAGE, P,
    "grep: 0 img, 0 svg, 0 figure, 0 data-files on the page; the spec's case table is generated by lab 3 from its seed (line 338).")
row("proj-banned-and-process-words", "2.9 banned phrases; process words in learner text", PAGE + " (whole page)", P,
    f"check_pages LX2: PASS ({OUT}check_pages_LX2_r7.txt). grep over the page: TODO, TBD, lorem, '...' and 'beyond the scope' absent; 'builder', 'verifier', 'REQUEST', 'round 6' absent ({OUT}page_checks_r7.txt). The phrase 'round half to even' (line 328) is learner content about a rounding rule.")
row("proj-case-realised-source", "2.3 / 2.5 case documentation", PAGE + " lines 80-92, 89, 225 vs labs 1-3", P,
    "Line 89: 'Lab 1 agrees with the Lab 3 value at month 18 only, and Lab 2 at month 13 only.' Re-derived: lab 1 realised months 13-20 equal lab 3 realised only at month 18 (133); lab 2 realised months 13-18 equal lab 3 only at month 13 (127); rederive_r7.txt lines 'L1 vs L3 agreement' and 'L2 vs L3 agreement'.")
row("proj-rung1-plan-scope", "2.6 ladder scope (plan 5.1 item 1)", PAGE + " lines 203-233", P,
    "Element 1 (lines 206-211), element 2 (213-220), element 3 (222-226), element 4 (228-233): each annotated with the reason for each step.")
row("proj-rung4-open-ended", "2.6 rung 4 is genuinely open-ended", PAGE + " lines 701-706", P,
    "Line 702: 'Not graded. Neither item has a fixed answer'; the two items (lines 704-705) are open-ended and unscored.")
row("proj-exemplar-a-m1-window", "2.4 M1 test on the stated window", PAGE + " lines 58, 87, 567-568", P,
    "M1 is stated over the validation window (line 58); exemplar A tests it over months 13 to 36 (line 568); the test is named and limited (it does not show the trend holds).")
row("proj-exemplar-a-derivation-claim", "2.2 derivation claims", PAGE + " lines 567-605 (exemplar A)", P,
    f"Derivations re-computed in {OUT}rederive_r7.txt (sums, split, strict count, rolling bias); each stated value matches.")
row("proj-rung3-sr26-standard", "2.3 regulatory scope; attachment quotes and locators", PAGE + " lines 46, 336-361", P,
    f"Quotes exact (quote_check_r7.txt); 'This guidance does not set forth enforceable standards or prescriptive requirements' (line 360) is exact; the statement that the page does not say SR 26-2 requires any section (line 360) is consistent with it. PDF-page part of the locators: see proj-attachment-quote-locators.")
row("proj-define-model-owner", "2.1 item 5: plain dfn at first use", PAGE + " line 232 (first use), line 605 (later)", P,
    f"{OUT}page_checks_r7.txt: first occurrence of 'model owner' is line 232, which is the plain <dfn> (no data-concept); line 605 is a later use.")
row("proj-m2-statement-consistency", "2.4 statement consistency of assumption M2", PAGE + " lines 58, 87, 108, 209, 245, 379, 567", P,
    "M2 is stated the same way in the conventions (58), the case (87: cannot be checked from the case), lab 1 docstring (108), the worked steps (209: untested), lab 2 docstring (245), lab 3 docstring (379) and exemplar A (567: not tested).")
row("proj-reading-count", "2.4 numbers in prose (reading-list count)", PAGE + " lines 711-719 vs claim spans", P,
    "Reading list has six keys (lines 713-718). Line 711 says the project cites frb2026fed for 'the three regulatory statements of the source note, and no other key for any claim'. The claim spans cite no other key (page_checks_r7.txt), so the statement is true. It is incomplete: frb2026fed is also cited for the four expectations at 346-349 and in exemplar A at 618. Non-blocking.")
row("proj-delta-lede-exemplars", "2.9 delta: lede sentence (changed in round 6, unchanged in round 7)", PAGE + " line 37", P,
    "Line 37 says the report is graded against 'two annotated exemplars'; exemplar A (line 561) and exemplar B (line 628) are the two.")
row("proj-delta-rung3-pointer", "2.9 delta: rung 3 text", PAGE + " line 46", P,
    "Line 46 anchors #rubric-section, #attachment-expectations and #source resolve (page_checks_r7.txt); the attachment-expectation list is at lines 343-351.")
row("proj-delta-limitations", "2.2 numbers in prose (exemplar A limitations)", PAGE + " lines 593-594", P,
    "'errors from 3 to 8 units' and 'the validation window is one window of 24 months, and 9 of its months, 28 to 36' match the Part A rows (rederive_r7.txt).")
row("proj-delta-rung2-disclosure", "2.9 delta: rung 2 lede (line 45), hypothesis (237), interpretation (328)", PAGE + " lines 45, 237, 328", P,
    f"Every hunk of the round 7 delta was read (git diff 4bd8cb9 06994db -- course/modules/LX/LX2/project.html: 5 hunks, lines 45, 89, 237, 328, 532). The three rung-2 hunks state the disclosure; verified by {OUT}blank_literal_check_r7.txt and {OUT}lab2_candidates_r7.txt; the 'compares the printed output only' sentence matches labs.js compareOutput (lines 42-55).")
row("proj-delta-case-series-line", "2.3 delta: case documentation item (e), line 89", PAGE + " line 89", P,
    "The changed sentence ('the Lab 3 table is the case's realised series') matches lab 3 being the only generator of the case series (lab 3 docstring lines 370-376) and the agreement claims re-derived in rederive_r7.txt.")
row("proj-delta-time-budget", "2.8 delta: time-budget rationale, line 532", PAGE + " line 532", P,
    "Changed rationale ('Read the case section ...') keeps the 2-hour row; the total stays 14 (lines 530-536). The case is described as a section of this page, which matches lines 76-92.")
row("proj-scope-words", "2.2 / 2.4 scope words (only, all, every, always, never, exactly, same, drives)", PAGE + " lines 37-711 (grep)", P,
    "Scope words were grepped with context (every, all, only, exactly, same, each, never, any). Universal statements are computed: 'From month 28 every forecast misses' (line 593; errors 28-36 all |e| >= 3); 'every error ... between -3 and 3' (line 634; months 13-27, True); 'the only integer sum that prints as 0.9167' (line 568; only 11 in [10.9998, 11.001)); 'the Lab 1 agrees ... at month 18 only' (line 89); 'differ only at an exact tie' (line 219) is the definition of the two rules; 'every run prints the same lines' (line 104) holds because lab 1 uses no random draws.")
row("proj-hours-independent-estimate", "2.6 hours: independent estimate within 30%", PAGE + " lines 526-537", P,
    "Independent estimate: rung 1 1.5-2 h; rung 2 0.5-1 h; intake 1.5-2 h; outcomes 2-3 h; report 3-4 h; self-assessment 1.5-2 h; total 10-14 h, inside 14 +/- 30 percent (9.8-18.2 h). Note: the rung-2 rationale (line 531) budgets 2 h for explaining wrong blanks, which the page does not ask a student to write.")
row("proj-terms-first-use", "2.9 terms used before definition", PAGE + " lines 37, 44, 46, 56, 60-68, 81, 232, 605", P,
    "Round 7 scan: PF-SIM first at line 81 (defined there); model owner at 232 (plain dfn); outcomes analysis forward-referenced at 44 and defined at 70; the lede's 'outcomes measures' is noted under proj-validation-window-term.")
row("proj-anchors-links", "2.9 structure: internal links resolve", PAGE + " (all href)", P,
    f"{OUT}page_checks_r7.txt: unresolved hrefs: [] (all # fragments and the L04.html, index.html, review.html and asset links resolve).")
row("proj-mutate-graders-na", "2.6 autograder mutation tool (no autograder for rubric grading)", "tools/mutate_graders.py --unit LX2; tools/run_graders.py --unit LX2 --seeds 0-49", P,
    f"{OUT}mutate_graders_LX2_r7.txt: the tool skips rubric units (tools/mutate_graders.py line 35) and exits 0 with no output. The mutation run for the rung-2 completion check is in {OUT}lab2_candidates_r7.txt.")
row("proj-pytest-lx2", "2.5 labs: same suite in local pytest", "tests/test_labs.py, test_page_checks.py, test_run_labs.py, test_page_smoke.py, test_memo_exemplars.py (-k LX2)", P,
    f"{OUT}pytest_LX2_r7.txt: 7 passed.")
row("proj-labjs-failure-messages", "2.6 failure messages name the property and do not leak the answer", "course/assets/js/labs.js lines 42-55, 133-139; course/assets/css/course.css:1065", P,
    "compareOutput names the first differing token and the expected token. The expected block is always rendered on the page under the 'Expected output' label (course.css line 1065), so the message reveals nothing the page does not already show; the answer is public in this design, which the rung-2 disclosure states.")
row("proj-lab2-docstring-completed-solution", "2.2 / 2.5 labs: learner-visible docstring vs code (what the file contains)",
    PAGE + " line 241 (lab 2 docstring); tests/labs/LX2/lab-LX2-project-2.py docstring", F,
    "The docstring inside the code block the learner edits says 'This file is the completed solution: the page shows the same program with the hit-rate line and the bias line blanked'. The file shown on the page has ___ in those two lines (lines 308, 310), so the first clause is false for the file the learner runs. The page's own sentence after the colon is correct, which is why this is a wording defect and not a wrong number.",
    "Reword the docstring in the twin and in the page code, keeping them identical except the two blanks: for example 'The completed solution fills in the hit-rate and bias lines. This page shows it with those two lines blanked (___). The printed output of the completed solution is the expected output of the instant check.' Then re-run run_labs --unit LX2 and check_pages --unit LX2.")
row("proj-rung2-disclosure-verified", "2.6 disclosure claims in rung 2 hold on the page's compare rule", PAGE + " lines 45, 237, 328", P,
    f"{OUT}blank_literal_check_r7.txt: blanks typed as 0.6667 and 0.1667 give stdout identical to the completed twin, exit 0. {OUT}lab2_candidates_r7.txt: 4 tie-rule and 1 literal-blank mutant survive, all named in the page's disclosure. No other class survives.")
row("proj-r7-new-mutants", "2.6 new student-error mutants (at least 3, written this round)", "ledgers/LX2/mutants/r7_lab2_one_sided_band.py, r7_lab2_edge_months_at_or_beyond_band.py, r7_lab2_window_one_month_early.py, r7_lab2_rounds_through_python_round.py", P,
    f"Written by ledgers/LX2/scripts/LX2-c-r7/make_r7_mutants.py from the twin with one error each. Killed: one_sided_band (token 61 'hit=yes' vs 'hit=no'), edge_months_at_or_beyond_band (token count 93 vs 91), window_one_month_early (token count 90 vs 91). Survived: rounds_through_python_round (tie-rule class, disclosed at line 328). {OUT}lab2_candidates_r7.txt.")
row("proj-rung2-alt-decimal", "2.5 / 2.6 new correct alternative (over-constraint check)", "ledgers/LX2/scripts/LX2-c-r7/alts/alt_r7_decimal_half_up.py", P,
    f"Decimal quantize with ROUND_HALF_UP on the exact Fraction; stdout tokens equal the expected block; exit 0 ({OUT}lab2_candidates_r7.txt, and the survived list of correct alternatives).")

row("proj-attachment-quote-locators", "2.3 quote-by-quote check against the attachment (locator file and page)", PAGE + " lines 346-349, 360, 618", F,
    f"{OUT}quote_check_r7.txt: every quote is exact, and the printed pages match. The PDF page numbers in the locators (10, 11, 11, 9, 9, 11, 4) are the pages of SR2602.pdf, the 14-page letter plus attachment. The record's URL (sr2602.htm, line 9187 of references.json) links the attachment as SR2602a1.pdf, where the same quotes are on PDF pages 8, 9, 9, 7, 7, 9 and 2. The locator names no file, so a reader who opens the linked attachment finds different PDF page numbers. Printed page numbers are correct in both files.",
    "Name the file in each locator, for example 'SR2602.pdf, PDF page 10', or give the attachment file's own PDF page numbers (8, 9, 9, 7, 9, 2 as listed above). Change the source note (line 361) to say which file the page numbers follow.")
row("proj-claim-span-paraphrase", "2.3 paraphrase checked against source", PAGE + " lines 359-360, 618", P,
    f"{OUT}quote_check_r7.txt: the applicability sentence and the section I sentence are exact; the supersession sentence (line 359) is a condensed, unquoted paraphrase ('issue the attached Revised Guidance ..., which supersedes and replaces SR letter 11-7 and SR letter 21-8'), and the letter's own text (letter text lines 26-31) says the same thing with intervening words; accurate.")
row("proj-counter-evidence-c-grade", "2.3 grades: C-graded claim counter-evidence (BUILDER_RULES 2.5)", PAGE + " lines 344, 346-349, 360", P,
    "The C-graded regulatory claims carry the published counter-evidence the source gives: the attachment states it sets forth no enforceable standards or prescriptive requirements (line 360, quoted exactly) and that its expectations are sound practice (line 344). The rung-3 expectations (346-349) are quotes, and the limit they do not reach (no threshold in the case, line 347) is stated.")
row("proj-prose-numbers-rederived", "2.2 numbers: one row for the full set of numeric prose (rungs 1-3, exemplars, limitations, monitoring)", PAGE + " (all numeric prose)", P,
    f"{OUT}rederive_r7.txt recomputes every number in the rung 1, rung 2, rung 3 and exemplar prose: lab 1 (0.5000, 0.2500, edge [15,19], 1/8, 0.25 strict); lab 2 (0.6667, 0.1667, 2.8333, 0.5000, edge [14,17]); lab 3 (13/24, 0.5417, 2.1250, 0.9167, 11, edge list, 8 at 34, split 13/15 and -3, 9 months and 54, 51, 56/12 = 4.6667, strict 6 of 24). Every stated figure matches, and every displayed rounding is half up at four places.")

mutant_names = {}
cand = open(ROOT / OUT / "lab2_candidates_r7.txt", encoding="utf-8").read().splitlines()
mutants = []
for line in cand:
    m = re.match(r"^(KILLED|SURVIVED)\s+(\S+)(?:\s+\|\s+(.*))?$", line)
    if not m:
        continue
    kind, name, why = m.group(1), m.group(2), m.group(3)
    if name.startswith("alt"):
        continue
    path = ROOT / "ledgers/LX2/mutants" / name
    doc = open(path, encoding="utf-8").read().split("\n")[0].replace('"""', "").strip()
    if kind == "KILLED":
        mutants.append({"name": name, "description": doc,
                        "killed_by": f"rung-2 whole-block compare under labs.js rule ({why})"})
    else:
        mutants.append({"name": name, "description": doc, "killed_by": None})

killed = sum(1 for x in mutants if x["killed_by"])
assert len(mutants) == 34 and killed == 29, (len(mutants), killed)
assert len(rows) == len({r["id"] for r in rows})
frag = {
    "unit": "LX2",
    "slice": "LX2-c",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for LX2-c, round 7 (did not build LX2; no shared context with the builders)",
    "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "base": "round 6 pin 4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (fragment /Users/billyribeiro/.fanout/frags/E-LX2-c.round6.json). Delta 4bd8cb9..06994db for this slice: course/modules/LX/LX2/project.html only, five hunks (lines 45, 89, 237, 328, 532), each read. tests/labs/LX2/lab-LX2-project-{1,2,3}.py byte-identical to the round 6 pin (git diff --quiet). No tools/, tests/ (except other units' labs), references/, notation/ or course/assets/ changes in the delta.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-LX2-c (detached at 06994db; .venv symlinked)",
    "scratch": f"{SRC} (SR 26-2 letter sr2602.htm, SR2602.pdf (14 pages, letter plus attachment) and SR2602a1.pdf (attachment, 12 pages), fetched by plain curl HTTP 200 on 2026-11-04; pdftotext -layout; no other scratch is evidence)",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "gpo1983dirks: references/references.json title field reads '(1982)' while its year field is 1983 (planner N1). This page cites the key in the reading list only and prints no year. Out of this slice; the architect corrects the record.",
        "frb2026fed: the record URL (sr2602.htm) links the attachment as SR2602a1.pdf, but the page's attachment locators give PDF page numbers of SR2602.pdf (the combined file). See proj-attachment-quote-locators. The record itself is correct.",
    ],
    "freshness_flags": [
        "SR 26-2 (dated April 17, 2026) is the letter fetched on 2026-11-04. No newer superseding letter was searched for. The page cites SR 11-7 and SR 21-8 only through the supersession statement (line 359). No 2025-2026 secondary work is cited on the page.",
    ],
    "notes": [
        "Rows re-verified this round from the round 7 pin. Every row cites a command output in ledgers/LX2/scripts/LX2-c-r7/out/ or a script in ledgers/LX2/scripts/LX2-c-r7/.",
        "Full read: project.html (734 lines, 66,897 bytes) read in full line by line; each number, quote, cross-reference and claim span checked. The round 7 delta hunks were read in full.",
        "Ruling applied to the two round 6 FAIL rows (proj-rung2-instant-check-mutants, proj-rung2-student-error-mutants): every surviving grader mutant is a behaviour the page now states (lines 45, 237, 328), so the verifier records PASS under the ruling 'a surviving grader mutant is a FAIL only when the page states the behaviour it violates'. If the architect does not accept disclosure as meeting that ruling, these two rows return to FAIL and the rung-2 check needs a grader that reads the code or a tie in its printed values.",
        "The mutants list is the 34 fault mutants for the rung-2 completion check (5 mut-lab2, 5 r3, 4 r4, 5 r5, 11 r6, 4 r7). 29 are killed. The 5 survivors are tie-rule and literal-blank mutants, listed with killed_by null, and are stated on the page. 10 correct alternatives pass (not listed as mutants).",
        "Blind calibration: exemplar passages were extracted with annotations removed (page_checks_r7.txt) and scored from the rubric. I had read the annotated page earlier in this round, so the blind step is by descriptor, not by a fresh reader.",
        "Not checked: the browser UI (light and dark theme at 360 px) beyond what page_smoke asserts; I did not view screenshots. The rung-2 typed-literal result comes from running the twin with the blanks filled, not from clicking the page. page_smoke ran the three labs in the browser runtime.",
        "Not checked: lessons, cards, hub and FC1 gate (other slices). Dirks and O'Hagan are cited on the page only in the reading list, so their records are not checked against the opinions.",
        "Not checked: the SR 26-2 letter and attachment against any later version (none searched). verify_refs --unit LX2 was a live run (6 entries) and passed.",
        "Non-blocking observations: the rung-2 expected block is shown under 'Expected output' at all times, so the rung is open-book by design (disclosed). The rubric level-4 C4 descriptor and exemplar A's C4 annotation depend on the term 'basis' (proj-rubric-observable).",
    ],
    "summary": "LX2-c round 7: FAIL. 67 rows: 64 PASS, 3 FAIL, 0 UNVERIFIABLE. Every round 6 row id is kept (59), plus 8 new rows. The round 6 FAILs (proj-rung2-instant-check-mutants, proj-rung2-student-error-mutants) are PASS under the ruling that a surviving grader behaviour the page states is not a FAIL; the page now discloses both (lines 45, 237, 328). The three FAIL rows: proj-rubric-observable (undefined term 'basis' in three rubric descriptors), proj-attachment-quote-locators (PDF page numbers follow SR2602.pdf, not the linked SR2602a1.pdf; printed pages correct), proj-lab2-docstring-completed-solution (learner-visible docstring calls the blanked file the completed solution). Mutants: 29/34 killed (5 disclosed survivors); 10 correct alternatives pass. Gates re-run at the pin: check_projects, check_pages, check_dag, run_labs, page_smoke (project), ruff, mypy, pytest -k LX2, verify_refs (LX2 live and offline): all PASS. All numbers, quotes, cross-references and labs re-derived.",
}
problems = []
for r in rows:
    for f in ("id", "check", "location", "status", "evidence"):
        if not str(r.get(f, "")).strip():
            problems.append((r.get("id"), f))
    if r["status"] != "PASS" and not r.get("fix"):
        problems.append((r["id"], "fix"))
print("problems:", problems)
dst = ROOT / "ledgers/LX2/LX2-c.json"
dst.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
print("rows", len(rows), counts, "mutants", len(mutants), "killed", killed)
