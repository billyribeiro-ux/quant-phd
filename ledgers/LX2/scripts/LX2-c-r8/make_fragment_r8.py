"""Build ledgers/LX2/LX2-c.json (round 8) from the rows and mutant results recorded in this round."""
import json
import pathlib
from datetime import UTC, datetime

OUT = "ledgers/LX2/scripts/LX2-c-r8/out"
R7 = json.load(open("/Users/billyribeiro/.fanout/frags/E-LX2-c.round7.json", encoding="utf-8"))
P = "course/modules/LX/LX2/project.html"

ev = {
 "proj-gates-tooling": ("gate: check_projects, check_pages, check_dag, run_labs (7/7), page_smoke (project), ruff check and format, mypy --no-incremental, pytest (85 passed, LX2 subset), verify_refs --offline (560 entries, 0 problems) and --unit LX2 live (6 entries, 0 problems)", f"{OUT}/gates_project_labs_r8.txt; {OUT}/page_smoke_verify_refs_r8.txt; {OUT}/ruff_mypy_r8.txt; {OUT}/pytest_lx2_r8.txt; {OUT}/run_labs_LX2_r8.txt"),
 "proj-page-smoke": ("tools/page_smoke.py --unit LX2 --pages project: 'page_smoke modules/LX/LX2/project.html: PASS' and 'page_smoke LX2: PASS', exit 0 (run at the pin)", f"{OUT}/page_smoke_verify_refs_r8.txt"),
 "proj-labs-twins-alone": ("tools/run_labs.py --unit LX2: 'run_labs LX2: PASS (7/7)'; run_labs runs each twin under python -I -W error and compares stdout to the page's expected block under the labs.js token rule", f"{OUT}/run_labs_LX2_r8.txt"),
 "proj-page-code-equals-twin": ("lab 1 (lines 105-190) and lab 3 (lines 374-482) page code byte-identical to tests/labs/LX2/lab-LX2-project-{1,3}.py; lab 2 page code (lines 242-320) differs from its twin only at line 71 ('hit_rate = ___' vs 'hit_rate = Fraction(hits, horizon)') and line 73 ('bias = ___' vs 'bias = Fraction(sum(errors), horizon)'); every other line identical", f"{OUT}/page_vs_twin_r8.txt; ledgers/LX2/scripts/LX2-c-r8/page_vs_twin_r8.py"),
 "proj-rung1-hypothesis-and-steps": ("line 104 hypothesis (4 of 8, 0.5000, 0.2500, edge 15 and 19) equals the lab 1 expected block (lines 201-203); steps at 220-222 re-derived: e13 = +1, e14 = -3, errors sum to 2, 2/8 = 0.2500, strict band gives 2 of 8", f"{OUT}/rederive_r8.txt; {OUT}/run_labs_LX2_r8.txt"),
 "proj-rung2-numbers-and-claims": ("lines 241 and 331 (expected 4 of 6, 0.6667, 0.1667, edge [14, 17]) equal the twin output; interpretation line 332: hit/8 gives 0.5000 (token 70) and mean-absolute bias gives 2.8333 (token 74), both reproduced by the harness", f"{OUT}/rederive_r8.txt; {OUT}/harness_lab2_all_r8.txt"),
 "proj-rung2-instant-check-mutants": ("harness over the 34 existing lab 2 mutants: 29 killed, 5 survive (r6_lab2_float_format_ties_even, r6_lab2_hard_coded_printed_values, r6_lab2_round_half_even_ties, r6_lab2_round_half_toward_plus_infinity, r7_lab2_rounds_through_python_round); every survivor is one the page states (line 332: check grades printed output only, a literal blank passes, tie rules are not exercised; line 45 likewise)", f"{OUT}/harness_lab2_all_r8.txt"),
 "proj-rung2-student-error-mutants": ("4 new blank-fill student errors killed (bias_hit_errors_only, hit_rate_over_horizon_plus_one, hit_rate_counts_edge_months, bias_truncated_to_whole_units); the 5th (hit_rate_ceiling_four_places) prints the expected block and is disclosed by lines 45 and 332 (the check does not grade the expression)", f"{OUT}/harness_lab2_all_r8.txt; ledgers/LX2/mutants/r8_lab2_*.py"),
 "proj-rung2-alternatives": ("14 correct alternatives pass the lab 2 output rule: 12 earlier alternatives in ledgers/LX2/scripts/LX2-c-r4..r7/alts, alt-lab2-float-division.py, and alt_r8_a1_len_float_decimal.py (len(errors) denominator, float division, Decimal half-up)", f"{OUT}/harness_lab2_alts_r8.txt; {OUT}/harness_lab2_all_r8.txt"),
 "proj-rung2-alt-fixture": ("every r6, r7 and r8 mutant and the new alternative is a complete module whose first line is a one-line docstring describing the error or the method (checked by head -1 of each file)", "ledgers/LX2/mutants/r6_*.py; ledgers/LX2/mutants/r7_*.py; ledgers/LX2/mutants/r8_*.py"),
 "proj-lab3-numbers": ("rederive_r8.py (independent, seed 20261103, randint(-3, 3), shift -6 from month 28): 13 hits of 24, rate 0.5417, bias 2.1250 (sum 51), calibration sum 11 -> 0.9167, edge months [14, 15, 16, 19, 22, 24, 26], largest |e| 8 at months 34 and 35 (Part E earliest = 34); hypothesis line 373 and expected block lines 483-513 equal the run", f"{OUT}/rederive_r8.txt; {OUT}/run_labs_LX2_r8.txt"),
 "proj-lab-generator-description": ("lab 3 docstring (lines 376-403) matches the code (lines 412-479): seed 20261103, one randint(-3, 3) per month 1 to 36 in order, 100 + 2t + noise and -6 from month 28, H = 24, Part E earliest on a tie via key -t, Part F not an outcomes measure; the docstring's 'only the validation window enters the outcomes measures' matches the code", f"{OUT}/rederive_r8.txt; {OUT}/page_vs_twin_r8.txt"),
 "proj-exemplar-a-numbers": ("every number in exemplar A (lines 571-625) re-derived by rederive_r8.py: 13-27 errors sum -3, bias -0.2000, 13 hits, 0.8667; 28-36 sum 54, bias 6.0000, 0 hits; 51/24 = 2.125; strict band 6 hits, 0.2500; 7 edge months; 56/12 = 4.6667 at month 36; calibration 11/12 = 0.9167, the only integer sum that prints so; errors of months 28 to 36 are all positive, 3 to 8", f"{OUT}/rederive_r8.txt"),
 "proj-exemplar-b-numbers": ("exemplar B (lines 650-652): 13 of 24 -> 0.5417, bias 2.1250 both match rederive_r8.txt; 'every error in months 13 to 27 is between -3 and 3' (line 638) holds: errors -3..+3 in the Part A rows", f"{OUT}/rederive_r8.txt"),
 "proj-exemplar-calibration": ("blind scoring first, from the rubric and the annotation-stripped exemplar text (out/blind_rubric_exemplars_r8.txt): exemplar A 4,4,4,4,3 and exemplar B 2,2,2,1,1, against the official data-scores 4,4,4,4,3 and 2,2,2,1,1 (line 565, 632); all within one level", f"{OUT}/blind_rubric_exemplars_r8.txt; {P} lines 565, 632"),
 "proj-exemplar-b-c5-annotation": ("line 691 quotes the attachment section I, printed page 2 (PDF page 2 of SR2602a1.pdf); the page matches the attachment text (attach p2, 'This guidance does not set forth enforceable standards or prescriptive requirements'); the claim that the CFA sentence has no key holds (line 686)", "/tmp/lx2c-r8-src/a_p2.txt (SR2602a1.pdf page 2); " + P + " lines 686, 691"),
 "proj-exemplar-b-unread-requirement": ("line 686: 'SR 26-2 requires the outcomes analysis and the four sections' is a requirement the attachment does not set out (its section I says no enforceable standards or prescriptive requirements, SR2602a1.pdf p.2; no requirement in SR 26-2 letter text); annotation line 691 says so", "/tmp/lx2c-r8-src/a_p2.txt; " + P + " lines 686, 691"),
 "proj-source-supersession": ("FAIL: line 363 says 'Its locator is the cover letter's opening paragraph', but the same sentence's data-locator (line 363) reads \"cover letter, paragraph beginning 'The Board of Governors'\". In sr2602.htm and SR2602.pdf page 1 the first body paragraph is 'Applicability:'; the supersession sentence is the second paragraph. The supersession text (SR 11-7 and SR 21-8) and the 'Supersedes:' list after the signature (SR2602.pdf page 2) are verified", "/tmp/lx2c-r8-src/c_p1.txt; /tmp/lx2c-r8-src/c_p2.txt; " + P + " line 363"),
 "proj-source-applicability": ("line 364 span: 'expected to be most relevant to banking organizations with over $30 billion in total assets regulated by the Federal Reserve' matches SR2602.pdf page 1 ('Applicability:' paragraph); locator 'paragraph headed Applicability' correct", "/tmp/lx2c-r8-src/c_p1.txt; " + P + " line 364"),
 "proj-source-attachment": ("every attachment quote (lines 350-353, 364, 622, 691) located by pdftotext per page: conceptual soundness p.8, outcomes analysis p.9 ('established performance thresholds' also p.9), limitations p.7 (two quotes), ongoing monitoring p.9, enforceable-standards sentence p.2 (section I). Printed page = PDF page of SR2602a1.pdf (footers 1-12); section V 'Model Validation and Monitoring' starts p.7; headings 'Conceptual Soundness' p.8, 'Outcomes Analysis' p.9, 'Ongoing Model Monitoring' p.9; no 'Limitations' heading", "/tmp/lx2c-r8-src/a_p*.txt (pdftotext -f N -l N -layout SR2602a1.pdf)"),
 "proj-citations-registry": ("every data-cite key on the page (frb2026fed, cfandcode, gpondsecurities, gpondsecuritiesb, gpo1983dirks, gpo1997united) exists in references/references.json; verify_refs --unit LX2 live: 6 of 560 entries, 0 problems; verify_refs --offline: 560 entries, 0 problems", "references/references.json; " + f"{OUT}/page_smoke_verify_refs_r8.txt"),
 "proj-notation": ("the 65 inline math spans are the same set as at 06994db (no new spans, no removed spans); the symbols used (H, e_t, y_t, \\hat{y}_t, bias, t) are not in notation/notation.json (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); none of the registered symbols appears on the page", "notation/notation.json; " + P),
 "proj-dag-and-links": ("check_dag --unit LX2 PASS; 18 in-page anchors resolve; cross-page targets L04.html#s4 (section 4, outcomes analysis in exact arithmetic, band 2 inclusive, ties away from zero) and L04.html#def-model-risk-management exist", f"{OUT}/gates_project_labs_r8.txt; course/modules/LX/LX2/L04.html line 97 and line 113"),
 "proj-standard-error-term": ("term 'error' defined in the conventions dt 'Error and sign' (line 60) before use in lines 62-68 and in the labs; no 'standard error' term on the page", P + " lines 59-60, 62"),
 "proj-validation-window-term": ("'validation window' and 'calibration window' defined in the conventions dt 'Windows' (line 56) before first use in lines 58, 64", P + " lines 55-58, 64"),
 "proj-lab1-sections-claim": ("line 100 says the lab computes the outcomes analysis and not the other three sections: lab 1 (lines 105-190) prints Parts A-D only, the outcomes measures; line 204 says the printed measures 'say nothing about the model outside months 13 to 20' (true of the lab's eight values)", P + " lines 100, 204; lab 1 twin"),
 "proj-spec-complete": ("spec (lines 338-358): inputs (1)-(3) name the case section, the Lab 3 table (seed 20261103, 24 months), and the source note; required outputs name the four sections in order and the Part-letter rule; constraints state the rounding rule, the no-real-model rule, and the key-and-locator rule; grading mode states rubric only", P + " lines 338-357"),
 "proj-spec-ladder": ("ladder (lines 43-48) matches the page: rung 1 = lab 1 on eight months, rung 2 = lab 2 completion, rung 3 = specification and lab 3 case table, rung 4 = stretch (not graded, line 706)", P + " lines 43-48, 706"),
 "proj-hours": ("data-hours-project 14 (line 33) and eyebrow '14 hours' (line 35) agree with the table (lines 534-539: 2+2+2+3+3+2 = 14, line 540); 14/50 = 28 percent matches index.html line 176 ('36 lessons plus 14 project = 50 hours')", P + " lines 33, 35, 534-540; course/modules/LX/LX2/index.html lines 29, 176"),
 "proj-rubric-observable": ("FIXED: 'basis' is now a defined term (conventions dt 'Basis of a threshold', lines 73-74) and the C2 level-3 descriptor no longer uses it (line 554); C4 descriptors (line 556) use the defined term; every level names an element a reader can check", P + " lines 73-74, 554, 556"),
 "proj-rubric-criteria-count": ("five criterion rows C1-C5, each with four levels (lines 553-557), caption 'five criteria, four levels each' (line 550), exemplar scores use C1-C5 (lines 565, 632)", P + " lines 549-557"),
 "proj-autograder-na": ("tools/run_graders.py --unit LX2 printed 'run_graders LX2: no autograder (grading: rubric)'; page line 353 says rubric only; index.html line 36 'No autograder'", f"{OUT}/gates_project_labs_r8.txt; " + P + " line 357"),
 "proj-adversarial-na": ("page line 357: 'No adversarial review is used for this project'; plan decision (no question bank)", P + " line 357"),
 "proj-atlas-na": ("grep -i atlas over the page: 0 matches; no atlas link or entry", P),
 "proj-studio-na": ("grep -i studio over the page: 0 matches", P),
 "proj-data-and-figures-na": ("grep for img, svg, data-files and figures- over the page: 0 matches; labs read no data file (lab 3 generates its series from the seed, line 376-380)", P),
 "proj-banned-and-process-words": ("grep -i -E for verifier, builder, architect, planner, ruling, fragment, ledger, mutant, round N, agent, blind, checkout, todo, TBD, FIXME, lorem, 'as an ai', 'I think', 'we will', basically, obviously, clearly, simply, just, in order to, leverage, robust, sophisticated: no matches", P),
 "proj-case-realised-source": ("lines 92-93 (not documented (e)): case series = lab 3 values for months 1 to 36, part A prints 13-36; labs 1 and 2 agree with the case series only at month 18 (lab 1) and month 13 (lab 2), verified against rederive_r8.txt", f"{OUT}/rederive_r8.txt; " + P + " lines 92-93"),
 "proj-rung1-plan-scope": ("lines 203-233: rung 1 worked steps cover elements 1 to 4 on the same eight months; lab 1 computes element 2 only (line 100); the element-3 and element-4 arithmetic (lines 228, 234-236) re-derived", P + " lines 100, 207-236"),
 "proj-rung4-open-ended": ("lines 704-710: rung 4 'Not graded. Neither item has a fixed answer' (line 706); no score or answer is given", P + " lines 704-710"),
 "proj-exemplar-a-m1-window": ("line 572: M1 is tested on the validation window, months 13 to 36, which the assumption states (line 58: 'holds over the validation window'); line 58 and 87 use the same window", P + " lines 58, 87, 572"),
 "proj-exemplar-a-derivation-claim": ("lines 571-610: every derivation (window sums, rolling 12-month bias at month 36, strict-band count, 0.9167 integer sum) re-derived by rederive_r8.py; the statement 'the case documents no sampling model' matches the case section (lines 85-93)", f"{OUT}/rederive_r8.txt; " + P + " lines 571-610"),
 "proj-rung3-sr26-standard": ("line 46 rung-3 pointer; lines 350-353 quotes and locators verified against SR2602a1.pdf and SR2602.pdf (see proj-source-attachment); lines 363-365 source note (supersession locator prose defect recorded under proj-source-supersession)", "/tmp/lx2c-r8-src/; " + P + " lines 46, 346-365"),
 "proj-define-model-owner": ("the term 'model owner' is no longer used on the page (grep: 0 matches; the monitoring step at line 236 now says 'the person who signs the monthly planning figure'), so no undefined term remains", P + " lines 232-236, 605-613"),
 "proj-m2-statement-consistency": ("M2 wording at lines 58, 91, 112, 213, 249, 383, 567 is the same claim: the forecast for month t is issued before month t starts and uses no information from month t; the page never states M2 in a different form", P),
 "proj-reading-count": ("reading list lines 716-723 has six entries; line 715 says frb2026fed is cited for the three regulatory statements and 'the other five sources' are reading; the source note has three frb2026fed spans (lines 363-364)", P + " lines 715-723"),
 "proj-delta-lede-exemplars": ("line 37 lede unchanged in content; it names two annotated exemplars and says they are sample reports written to this specification; no figure or claim on the line is contradicted", P + " line 37"),
 "proj-delta-rung3-pointer": ("line 46: 'Lab 3 below prints the case table (defined under the conventions) that the report must quote'; the case table is defined at lines 71-72, and Lab 3 prints it in Part A", P + " lines 46, 71-72"),
 "proj-delta-limitations": ("exemplar A limitations (lines 597-598): 9 of 24 validation months (28 to 36) are the months from the shift; errors 3 to 8 units (Part A, verified); 'one window of 24 months' (H = 24) verified", f"{OUT}/rederive_r8.txt; " + P + " lines 597-598"),
 "proj-delta-rung2-disclosure": ("disclosure after the line shift: lines 45 (rung 2 'compares the printed output only'), 241 (hypothesis: a blank typed as the value it prints passes), and 332 (interpretation: literal blanks pass; tie rule not exercised); round 7 cited lines 237 and 328, which are now 241 and 332", P + " lines 45, 241, 332"),
 "proj-delta-case-series-line": ("line 93 (not documented, item (e)): the case series are lab 3's values for months 1 to 36 and part A prints 13 to 36; labs 1 and 2 each write their own values, agreeing with the case series only at month 18 (lab 1) and month 13 (lab 2), verified by rederive_r8.txt", f"{OUT}/rederive_r8.txt; " + P + " line 93"),
 "proj-delta-time-budget": ("line 537: outcomes-analysis row ('the split at month 28', 3 hours) and total 14 (line 540) add up with the other rows (2+2+2+3+3+2); the split is derived from Part A rows, as the page says", P + " lines 534-540"),
 "proj-scope-words": ("grep of scope words (only, all, every, always, never, exactly, same, drives, any) over the page: each occurrence in the r8 delta checked; 'every forecast misses' (line 597) holds for months 28 to 36 (hit=no in lab 3 Part A); 'only the validation window enters' (lab 3 docstring line 384) matches the code (outcomes use months 13 to 36 only)", f"{OUT}/rederive_r8.txt; " + P),
 "proj-hours-independent-estimate": ("plan decision; the page gives no independent-estimate claim; the hours table (lines 534-540) sums to 14 and matches the hub split", P + " lines 534-540"),
 "proj-terms-first-use": ("terms used before definition checked: window and error (conventions, lines 55-68) before the labs and the case section; 'case table' (line 71) before Lab 3; 'basis of a threshold' (line 73) before the monitoring step (line 235); 'registry key and locator' (line 75) before the source note", P + " lines 51-78, 235"),
 "proj-anchors-links": ("python script: 18 href='#...' anchors all resolve to an id on the page; every cross-page href resolves to an existing file and fragment", "ledgers/LX2/scripts/LX2-c-r8/ (anchor check run inline, 0 bad links)"),
 "proj-mutate-graders-na": ("tools/mutate_graders.py --unit LX2 produced no output and exit 0 (LX2 has no autograder); tools/run_graders.py --unit LX2 printed 'no autograder (grading: rubric)'", f"{OUT}/gates_project_labs_r8.txt; " + "ledgers/LX2/scripts/LX2-c-r8/"),
 "proj-pytest-lx2": ("pytest tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py tests/test_memo_exemplars.py -k 'LX2 or lx2 or project or Project': 85 passed, 335 deselected", f"{OUT}/pytest_lx2_r8.txt"),
 "proj-labjs-failure-messages": ("course/assets/js/labs.js compareOutput (lines 42-55) names the token and reports the mismatch; the expected value appears in the message, but the expected block is printed on the page (line 321-331, class expected) so the message adds nothing a learner cannot already read; the page says the rung is open-book (line 241 and round disclosure); the mismatch text is not a leak beyond the page", "course/assets/js/labs.js lines 42-55, 133-139; " + P + " lines 321-331"),
 "proj-lab2-docstring-completed-solution": ("FIXED: the learner-visible docstring (lines 242-246) now says the completed solution fills the two lines and the page shows them blanked (___); the twin docstring is the same text and the completed twin prints the expected block (run_labs PASS)", P + " lines 242-246; tests/labs/LX2/lab-LX2-project-2.py lines 1-6"),
 "proj-rung2-disclosure-verified": ("the disclosure claims at lines 45, 241 and 332 hold on the labs.js token rule: the whole-block compare kills hit/8 (0.5000) and mean-absolute bias (2.8333) as stated; the tie-rule and literal-blank survivors are the ones stated", f"{OUT}/harness_lab2_all_r8.txt; " + P + " lines 45, 241, 332"),
 "proj-r7-new-mutants": ("the three r7 student-error mutants (r7_lab2_one_sided_band, r7_lab2_edge_months_at_or_beyond_band, r7_lab2_window_one_month_early) re-run: killed (token 61, expected 91 tokens got 93, expected 91 tokens got 90); r7_lab2_rounds_through_python_round survives and is disclosed (tie rule, line 332)", f"{OUT}/harness_lab2_all_r8.txt"),
 "proj-rung2-alt-decimal": ("alt_r7_decimal_half_up.py: correct alternative, passes the lab 2 output rule (harness_lab2_alts_r8.txt)", f"{OUT}/harness_lab2_alts_r8.txt"),
 "proj-attachment-quote-locators": ("FIXED: every quote's printed page equals its PDF page in SR2602a1.pdf (footers 1-12): 8, 9, 7, 7, 9, 9 (quotes on p.9 incl. 'established performance thresholds'), and 2 (enforceable-standards sentence, section I); the combined file SR2602.pdf gives 10, 11, 9, 9, 11, 4 (offset of 2) and the text states 4, 9, 10, 11 correctly (line 365); the verifier's round-7 mismatch no longer exists", "/tmp/lx2c-r8-src/a_p*.txt; /tmp/lx2c-r8-src/c_p*.txt; " + P + " lines 350-353, 365, 622, 691"),
 "proj-claim-span-paraphrase": ("unquoted spans at lines 363-364 and 622 paraphrase the letter (e.g. 'are issuing' -> 'issue'); the paraphrase is not in quotation marks and each content matches SR2602.pdf page 1 and page 4 (attachment page 2)", "/tmp/lx2c-r8-src/c_p1.txt; /tmp/lx2c-r8-src/c_p4.txt; " + P + " lines 363-364, 622"),
 "proj-counter-evidence-c-grade": ("the C-graded claims (lines 344, 346-349, 350-353, 360, 364) carry their key and locator; the counter-evidence sentence (line 364, 'enforceable standards') is C-graded and quoted from the attachment", P + " lines 344-364"),
 "proj-prose-numbers-rederived": ("every numeric prose figure on the page (lines 56-66, 100-236, 241-332, 340-365, 511-514, 534-540, 567-625, 646-652, 682-691, 704-738) re-derived or checked against the labs and the attachment; no mismatch found beyond the locator prose at line 363", f"{OUT}/rederive_r8.txt; {OUT}/run_labs_LX2_r8.txt; " + P),
}

rows = []
for r in R7["rows"]:
    rid = r["id"]
    if rid not in ev:
        raise SystemExit(f"no evidence for {rid}")
    text, loc = ev[rid]
    status = "PASS"
    if rid == "proj-source-supersession":
        status = "FAIL"
    row = {"id": rid, "check": r["check"], "location": r["location"], "status": status,
           "evidence": text + ". Evidence: " + loc}
    if status != "PASS":
        row["fix"] = ("Line 363: change 'Its locator is the cover letter's opening paragraph' to "
                      "'Its locator is the cover letter's paragraph beginning \"The Board of Governors\"', "
                      "so the prose matches the data-locator on the same span. Then re-run check_projects and page_smoke.")
    rows.append(row)

new_rows = [
 {"id": "proj-r8-delta-read", "check": "2.9 delta: every hunk of project.html read (06994db..0dee921)",
  "location": P + " (delta hunks at lines 43-47, 68-74, 90, 211-214, 233-236, 242-246, 350-365, 511-514, 551-557, 606-619, 688-691)",
  "status": "PASS", "evidence": "git diff 06994db 0dee921 -- " + P + " (135 lines) read in full, saved as " + f"{OUT}/project_html_delta_r7_to_r8.diff"
  + "; each hunk re-verified against the attachment, the labs, or the derivation (rows above). tests/labs/LX2/lab-LX2-project-2.py delta (docstring only) read."},
 {"id": "proj-r8-new-mutants", "check": "2.6 new student-error mutants written this round (at least three)",
  "location": "ledgers/LX2/mutants/r8_lab2_*.py (4 killed) and r8_lab2_hit_rate_ceiling_four_places.py (survives, disclosed)",
  "status": "PASS", "evidence": "harness_lab2_r8.py on each: r8_lab2_bias_hit_errors_only KILLED (token 74: 0.0000 vs 0.1667), r8_lab2_hit_rate_over_horizon_plus_one KILLED (token 70: 0.5714 vs 0.6667), r8_lab2_hit_rate_counts_edge_months KILLED (token 70: 0.3333 vs 0.6667), r8_lab2_bias_truncated_to_whole_units KILLED (token 74: 0.0000 vs 0.1667); the ceiling mutant prints the expected block and is a disclosed survivor (line 45, 332). Evidence file: " + f"{OUT}/harness_lab2_all_r8.txt"},
 {"id": "proj-r8-alternative-lab2-len-float-decimal", "check": "2.5 / 2.6 new correct alternative (over-constraint check)",
  "location": "ledgers/LX2/scripts/LX2-c-r8/alt_r8_a1_len_float_decimal.py",
  "status": "PASS", "evidence": "denominator len(REALISED), float division for the bias, Decimal ROUND_HALF_UP printing: passes the lab 2 output rule (" + f"{OUT}/harness_lab2_all_r8.txt" + ")"},
]
rows += new_rows

mutants = []
for m in R7["mutants"]:
    name = m.get("name") or m.get("id")
    mutants.append({"name": name, "description": m["description"], "killed_by": m.get("killed_by")})
for name, desc, killed in [
  ("r8_lab2_bias_hit_errors_only.py", "Student error: the bias sums only the errors of the months that are hits (|e| <= 2), then divides by H = 6.", "rung-2 whole-block compare under labs.js rule (token 74: 0.0000 vs 0.1667)"),
  ("r8_lab2_hit_rate_over_horizon_plus_one.py", "Student error: the hit rate divides by H + 1 = 7, an off-by-one in the window length.", "rung-2 whole-block compare under labs.js rule (token 70: 0.5714 vs 0.6667)"),
  ("r8_lab2_hit_rate_counts_edge_months.py", "Student error: the hit rate counts only the months at the edge of the band (|e| = 2) instead of all hits.", "rung-2 whole-block compare under labs.js rule (token 70: 0.3333 vs 0.6667)"),
  ("r8_lab2_bias_truncated_to_whole_units.py", "Student error: the bias is truncated to a whole number of units with int() before it is printed.", "rung-2 whole-block compare under labs.js rule (token 74: 0.0000 vs 0.1667)"),
  ("r8_lab2_hit_rate_ceiling_four_places.py", "Student error (rounding rule): the hit rate is rounded up to four places with math.ceil, not half up; it prints the same block on this window. Disclosed survivor: the check grades printed output only (page lines 45, 332).", None),
]:
    mutants.append({"name": name, "description": desc, "killed_by": killed})

fragment = {
 "unit": "LX2", "slice": "LX2-c", "round": 8,
 "round_note": "Round 8 (fresh full read of project.html and the labs; round 7 fragment used as context only; carried-PASS prefix not used because every row's subject was re-verified this round).",
 "verifier": "Claude Haiku 5.5, independent verifier for LX2-c, round 8 (did not build LX2; no shared context with the builders)",
 "pin": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3",
 "base": "round 7 pin 06994db16d1ab449bcf29898a7f56cfa999dce57 (fragment /Users/billyribeiro/.fanout/frags/E-LX2-c.round7.json). Delta 06994db..0dee921 for this slice: course/modules/LX/LX2/project.html (135-line diff, saved in out/) and tests/labs/LX2/lab-LX2-project-2.py (docstring, 4 lines). lab-LX2-project-1.py and -3.py unchanged.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE8-LX2-c (detached at 0dee921; .venv symlinked)",
 "scratch": "/tmp/lx2c-r8-src (SR 26-2 letter sr2602.htm, SR2602.pdf (14 pages), SR2602a1.pdf (attachment, 12 pages), fetched by plain curl HTTP 200 on 2026-11-04; pdftotext -layout per page); /tmp/lx2c-r8-blind (annotation-stripped rubric and exemplars, blind step); outputs copied to ledgers/LX2/scripts/LX2-c-r8/out/",
 "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [
   "gpo1983dirks: references/references.json title field reads '(1982)' while its year field is 1983 (planner N1). This page cites the key in the reading list only and prints no year. Out of this slice; the architect corrects the record.",
   "frb2026fed: the record URL (sr2602.htm) links the attachment as SR2602a1.pdf. Round 8 page locators name SR2602a1.pdf page numbers, which match the attachment file (printed = PDF page), and give the combined-file numbers in the text (line 365). The record is correct; the round 7 mismatch is resolved on the page."],
 "freshness_flags": ["SR 26-2 (dated April 17, 2026) is the letter fetched on 2026-11-04. No newer superseding letter was searched for. The page cites SR 11-7 and SR 21-8 only through the supersession statement (line 363)."],
 "notes": [
   "Blind calibration done first: exemplar A 4,4,4,4,3 and exemplar B 2,2,2,1,1 scored from the rubric and the annotation-stripped text (out/blind_rubric_exemplars_r8.txt) before reading any annotation; both match the official data-scores within the one-level rule.",
   "Full read: project.html (738 lines) read in full, line by line, including every annotation and the rubric; the round 8 delta hunks were read in full and each re-verified.",
   "Round 7 FAILs: proj-rubric-observable is PASS (the term 'basis' is now defined at lines 73-74); proj-attachment-quote-locators is PASS (every printed page verified against SR2602a1.pdf); proj-lab2-docstring-completed-solution is PASS (learner docstring now matches the page's blanked code). proj-rung2-instant-check-mutants and proj-rung2-student-error-mutants stay PASS under the ruling that a surviving grader behaviour the page states is not a FAIL (lines 45, 241, 332).",
   "New FAIL this round: proj-source-supersession. The round 8 locator change in the data attribute (line 363) was not carried into the prose sentence on the same line; the prose still says 'opening paragraph'. One-line fix in the summary.",
   "Mutants: 39 lab 2 rung-2 candidates re-run under the labs.js token rule: 33 killed, 6 survive (5 round 6/7 tie and literal-blank survivors, plus the round 8 ceiling mutant), each survivor disclosed on the page. 14 correct alternatives pass.",
   "LX2 has no autograder: tools/run_graders.py and tools/mutate_graders.py report 'no autograder (grading: rubric)' and produce no mutant run; the rung-2 check is the only machine grader, and it is covered above.",
   "Not checked: the browser UI at 360 px and in dark theme beyond what page_smoke asserts (I did not view screenshots); the self-assessment form (JavaScript) was not run; the lessons, cards and hub (other slices) were not checked beyond the DAG, hours and link checks named here; SR 26-2 superseded-by search (none run)."
 ],
 "summary": {},
}
fragment["summary"] = {
  "text": "LX2-c round 8: FAIL. " + str(len(rows)) + " rows: " + str(sum(1 for r in rows if r['status']=='PASS')) + " PASS, 1 FAIL, 0 UNVERIFIABLE. Every round 7 row id is kept (67) and three round 7 FAILs are now PASS (proj-rubric-observable, proj-attachment-quote-locators, proj-lab2-docstring-completed-solution). One new FAIL: proj-source-supersession (line 363 prose 'opening paragraph' contradicts its own data-locator 'paragraph beginning The Board of Governors'). Plus 3 new rows. Gates re-run at the pin: check_projects, check_pages, check_dag, run_labs (7/7), page_smoke (project), ruff check and format, mypy --no-incremental, pytest (85 passed), verify_refs offline and live: all PASS. Mutants: 33 of 39 killed; 6 survivors all disclosed on the page. 14 correct alternatives pass. Blind exemplar scores match the official scores."
}
pathlib.Path("ledgers/LX2/LX2-c.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "statuses", {s: sum(1 for r in rows if r['status']==s) for s in ('PASS','FAIL','UNVERIFIABLE')}, "mutants", len(mutants))
