import json

PIN = "7376a5e216c1e6d99becc76b4cd64028f5b55d3f"
S = "ledgers/LX2/scripts/LX2-c-r5"
O = S + "/out"

def row(id_, check, location, status, evidence, fix=""):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

GATES = (f"{O}/check_pages.txt: 'check_pages LX2: PASS' exit 0; {O}/check_dag.txt: 'check_dag LX2: PASS' exit 0; "
         f"{O}/check_projects.txt: 'check_projects LX2: PASS' exit 0; {O}/run_labs.txt: 'run_labs LX2: PASS (7/7)' exit 0; "
         f"{O}/ruff_check.txt: 'All checks passed!' and '7 files already formatted'; {O}/mypy.txt: 'Success: no issues found in 3 source files'; "
         f"{O}/verify_refs_unit.txt: 'live re-verification of LX2: 6 of 560 entries, 0 problems' exit 0; "
         f"{O}/pytest_lx2.txt: 7 passed (tests/test_labs.py, test_page_checks.py, test_run_labs.py, -k LX2); "
         f"{O}/run_graders.txt: 'no autograder (grading: rubric)'; {O}/mutate_graders.txt: no output, exit 0 (rubric unit).")

rows = [
 row("proj-gates-tooling", "gate", "course/modules/LX/LX2/project.html; tests/labs/LX2/lab-LX2-project-{1,2,3}.py", "PASS", GATES),
 row("proj-page-smoke", "2.5-2.9 page_smoke", "course/modules/LX/LX2/project.html", "PASS",
     f"Run alone: tools/page_smoke.py --unit LX2 --pages project, output in {O}/page_smoke_project.txt: 'page_smoke modules/LX/LX2/project.html: PASS', exit 0."),
 row("proj-labs-twins-alone", "2.5 labs", "tests/labs/LX2/lab-LX2-project-1.py, -2.py, -3.py", "PASS",
     f"python -I -W error on each twin: exit 0 and empty stderr ({O}/twin-project-{{1,2,3}}.txt, .err files 0 bytes). git diff 9a02b1af 7376a5e -- tests/labs/LX2 changes only lab-LX2-project-1.py line 7 (docstring M1 wording, 'holds over the validation window')."),
 row("proj-page-code-equals-twin", "2.5 labs", "course/modules/LX/LX2/project.html lines 101-186, 238-316, 361-469", "PASS",
     f"{S}/page_vs_twin_r5.py -> {O}/page_vs_twin_r5.txt: lab 1 and lab 3 page code equal the twin; lab 2 differs only at page lines 308 and 310 (hit_rate = ___, bias = ___). Each twin's stdout equals its page expected block."),
 row("proj-rung1-hypothesis-and-steps", "2.5 labs / 2.4 maths", "course/modules/LX/LX2/project.html lines 100, 203-232", "PASS",
     f"{S}/recompute_r5.py -> {O}/recompute_r5.txt: errors [1,-3,2,0,-4,3,-2,5]; 4 of 8 = 0.5000; bias 2/8 = 0.2500; edge [15,19]; strict 2 of 8 = 0.2500; one hit 1/8 = 0.1250. Line 208 M2 wording now matches line 58; Element 2 step 5 (13/24 = 0.5417, not a tie) re-derived."),
 row("proj-rung2-numbers-and-claims", "2.5 labs / 2.2 numbers", "course/modules/LX/LX2/project.html lines 237, 328", "PASS",
     f"{O}/recompute_r5.txt: errors [-1,2,6,1,-2,-5]; 4 of 6 = 0.6667; bias 1/6 = 0.1667; mean absolute 17/6 = 2.8333; edge [14,17]; over 8 = 0.5000; strict 2 of 6 = 0.3333."),
 row("proj-rung2-instant-check-mutants", "2.6 instant check", "ledgers/LX2/mutants/mut-lab2-*.py (5 files)", "PASS",
     f"{S}/lab2_check_r5.py -> {O}/lab2_mutants_r5.txt: mut-lab2-strict-band, -bias-mean-abs, -bias-sign-flip, -hit-over-8, -truncated-hit-rate all KILLED (token diffs 'hit=no' vs 'hit=yes', 2.8333, -0.1667, 0.5000, 0.6666 vs 0.6667)."),
 row("proj-rung2-student-error-mutants", "2.6 instant check (student-error mutants)", "ledgers/LX2/mutants/r3_lab2_*.py (5), r4_lab2_*.py (4), r5_lab2_*.py (5, new this round)", "PASS",
     f"{S}/make_r5_variants.py wrote the five new r5 mutants from the twin (each replacement asserted to apply once); {O}/lab2_mutants_r5.txt: all 19 mutants KILLED (r5: bias divides by hits 0.2500; bias over H-1 0.2000; hit rate counts misses 0.3333; bias = sum of forecasts 131.0000; hit rate prints count 4.0000). {O}/lab2_check_r3_rerun.txt: round-2 candidates 'ALL CANDIDATES AS EXPECTED', each whole_block_match=False."),
 row("proj-rung2-alternatives", "2.5 / 2.6 alternatives (over-constraint)", "ledgers/LX2/scripts/LX2-c-r5/alts/*.py; ledgers/LX2/mutants/alt-lab2-float-division.py", "PASS",
     f"{O}/alts_and_twin_r5.txt: the twin and four new correct alternatives PASS (len(errors) horizon; generator count with len(REALISED); Fraction(hits) / horizon; float quotients printed by decimal_text); alt-lab2-float-division.py PASSES ({O}/lab2_mutants_r5.txt)."),
 row("proj-lab3-numbers", "2.2 numbers / 2.5 labs", "course/modules/LX/LX2/project.html lines 360, 470-501, 573, 597", "PASS",
     f"{S}/recompute_r5.py: seed 20261103 reproduces Part A; 13 of 24 = 0.5417; bias 51/24 = 2.1250; edge [14,15,16,19,22,24,26]; worst 8 at month 34 (ties 34 and 35, earliest 34); calibration sum 11, bias 0.9167, only integer sum printing 0.9167 over 12. Interpretation split: months 13-27 sum -3, bias -0.2000, 13 hits, 13/15 = 0.8667; months 28-36 sum 54, bias 6.0000, 0 hits. Lab 3 expected block equals twin stdout ({O}/twin-project-3.txt)."),
 row("proj-lab-generator-description", "2.2 / 2.5 labs (docstring vs code)", "course/modules/LX/LX2/project.html lines 361-391, 419-427; tests/labs/LX2/lab-LX2-project-3.py", "PASS",
     "Docstring: randint(-3,3) uniform inclusive (code line simulate_realised uses rng.randint(-3, 3)); 100+2t+noise, 6 less from month 28 (SHIFT_FROM=28, SHIFT_UNITS=-6); seed 20261103; calibration months 1-12, validation 13-36, H=24 (code CALIBRATION_END=12, LAST_MONTH=36). Month 28 check: 156 - 149 = 7 consistent with noise -1. Page prints Parts A-F (run_labs; twin-project-3 output)."),
 row("proj-exemplar-a-numbers", "2.2 numbers", "course/modules/LX/LX2/project.html lines 558-597", "PASS",
     f"{S}/recompute_r5.py: months 28-36 errors 7,6,4,3,7,6,8,8,5 (min 3, max 8, all positive); months 13-27 sum -3; rolling 12-month bias at month 36 = 56/12 = 4.6667 (months 25-36 sum 56); strict band 6 of 24 = 0.2500 (13 - 7 edge months); 51/24 = 2.125 prints 2.1250."),
 row("proj-exemplar-b-numbers", "2.2 numbers", "course/modules/LX/LX2/project.html lines 625, 637, 649", "PASS",
     "recompute_r5.txt: months 13-27 errors lie in [-3, 3] (min -3 at month 21, max +3 at month 18); 13/24 = 0.5417; bias 2.1250 positive (over-forecast). Exemplar B's 'one limit' and 'no metric' are the annotated defects."),
 row("proj-exemplar-calibration", "2.2 / rubric calibration", "course/modules/LX/LX2/project.html exemplar A lines 552-617 (data-scores 4,4,4,4,3); exemplar B lines 619-682 (data-scores 2,2,2,1,1)", "PASS",
     "Each official score equals the number of descriptors the annotations mark as met: A C1 4 (meets level 4), C2 4, C3 4, C4 4, C5 3 (misses level 4 once); B C1 2 (meets 2, misses 3), C2 2, C3 2, C4 1 (meets 1, misses 2), C5 1 (meets 1, misses 2). Level 3 bar is per criterion as stated in the rubric intro."),
 row("proj-exemplar-b-c5-annotation", "2.4 / rubric C5", "course/modules/LX/LX2/project.html lines 673, 677-678", "PASS",
     "Line 673: keyed statement with no data-locator, CFA Code sentence with no key. Line 677-678 annotation: the attachment's section I sentence (PDF page 4, printed page 2) says 'does not set forth enforceable standards or prescriptive requirements', confirmed by pdftotext of the plain-curl PDF (/tmp/lx2c-r5-src.11JiQe/sr.txt, PDF page 4)."),
 row("proj-exemplar-b-unread-requirement", "2.4 unread-standard rule", "course/modules/LX/LX2/project.html lines 673, 678", "PASS",
     "Line 673 states 'SR 26-2 requires the outcomes analysis and the four sections'. The attachment text (sr.txt PDF page 4) says the guidance sets forth no prescriptive requirements; the annotation at line 678 marks it as a miss, so the exemplar is a deliberate defect and the annotation is correct."),
 row("proj-source-supersession", "2.3 registry / locator", "course/modules/LX/LX2/project.html line 350 (source note P1 claim at line 359)", "PASS",
     "Plain curl of https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm (HTTP 200): 'supersedes and replaces SR letter 11-7 ... and SR letter 21-8' in the cover letter ('SR letter 11-7, Guidance on Model Risk Management (issued April 4, 2011) and SR letter 21-8'); the Supersedes list after the signature has the same two letters. The page's paraphrase ('The Board of Governors, the Office of the Comptroller...') is a paraphrase, not a quotation, and says the same thing."),
 row("proj-source-applicability", "2.3 registry / locator", "course/modules/LX/LX2/project.html line 351 (claim at line 360)", "PASS",
     "sr_html.txt line ~317: 'Applicability: This letter is expected to be most relevant to banking organizations with over $30 billion in total assets regulated by the Federal Reserve.' Matches the page's wording. Date April 17, 2026 matches the letter header."),
 row("proj-source-attachment", "2.3 registry / locator", "course/modules/LX/LX2/project.html lines 351-352, 360, 609", "PASS",
     f"Every attachment quote checked by exact match after normalising apostrophes against plain-curl SR2602.pdf (pdftotext -layout, {'/tmp/lx2c-r5-src.11JiQe/sr.txt'}): CS quote on PDF page 10 (printed 8); OA quote on PDF page 11 (printed 9) and 'established performance thresholds' on PDF page 11; limitation quotes on PDF page 9 (printed 7, inside 'V. MODEL VALIDATION AND MONITORING'); Ongoing Model Monitoring quote on PDF page 11 (printed 9); 'does not set forth enforceable standards or prescriptive requirements' on PDF page 4 (printed 2, inside 'I. INTRODUCTION' which starts on PDF page 3). Section headings checked by grep. The page's pdf-page/printed-page pairs match the printed footers. The PDF is the one linked from the admitted page (sr2602.htm href /supervisionreg/srletters/SR2602.pdf)."),
 row("proj-citations-registry", "2.3 / registry", "references/references.json (frb2026fed); course/modules/LX/LX2/project.html lines 350-352, 360, 609, 673, 703-709", "PASS",
     "references.json frb2026fed: url https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm, year 2026, title 'SR 26-2 ... April 17, 2026'; the page cites only frb2026fed for regulatory statements; reading list keys match the registry. Reading-paragraph count is a separate row (proj-reading-count)."),
 row("proj-notation", "2.4 notation (notation/notation.json)", "course/modules/LX/LX2/project.html math spans", "PASS",
     "Symbols used on the page: t, H, e_t, y_t, \\hat{y}_t, bias (\\operatorname), sums over t, |e_t| <= 2. None is a registered symbol with another meaning: T is not used (plan 2.4 forbids it for horizon), no \\E, \\Prob, \\R, \\SR, \\PBO, \\FDR. H is introduced at line 56 with a pointer to its definition at line 64 (explicit forward reference, not a violation)."),
 row("proj-dag-and-links", "2.8 DAG", "course/modules/LX/LX2/project.html lines 62, 68, 78; course/modules/LX/LX2/L04.html line 97 (dfn model-risk-management), line 113 (s4)", "PASS",
     f"{O}/check_dag.txt: PASS. The concept link at line 78 points to L04.html#def-model-risk-management, which is defined at L04.html line 97 (dfn data-concept model-risk-management). Links at 62, 68 point to L04.html#s4, which exists at line 113. The page is after L04 in the unit, so the link is to an earlier lesson."),
 row("proj-standard-error-term", "2.4 terms", "course/modules/LX/LX2/project.html", "PASS",
     "grep -c 'standard error' on the page = 0; the term is not used."),
 row("proj-validation-window-term", "2.4 / 2.5 terms", "course/modules/LX/LX2/project.html lines 56, 64, 66, 109, 223, 347-348", "PASS",
     "First use of 'validation window' is line 56 (defined there: months 13 to 36). Later uses are consistent with that window (14 occurrences in total)."),
 row("proj-lab1-sections-claim", "2.2 prose claims", "course/modules/LX/LX2/project.html line 96 vs lines 101-122, 187-199", "PASS",
     "Line 96 says Lab 1 computes the outcomes analysis, the second of the four sections; the lab prints only Parts A-D of outcomes measures (twin-project-1 output), and the worked steps after it (lines 203-232) work the other three sections."),
 row("proj-spec-complete", "2.5 structure (check_projects)", "course/modules/LX/LX2/project.html lines 336-345, 703-709", "PASS",
     f"{O}/check_projects.txt PASS. dl.spec carries Context, Inputs, Required outputs, Constraints, Grading mode; the attachment-expectations item is a dt with id; the Reading list keys match the references."),
 row("proj-spec-ladder", "2.5 ladder", "course/modules/LX/LX2/project.html lines 40-48, 94-96, 235, 308-310, 691-698", "PASS",
     "Ladder rungs 1-4 in order; rung 2 completion lab with two ___ blanks; rung 3 rubric; rung 4 optional. Plan 5.1 item 3 (lab-LX2-project-3 recomputes the default numbers and prints the table) matches the page."),
 row("proj-hours", "2.8 hours arithmetic", "course/modules/LX/LX2/project.html lines 33, 521-527; course/modules/LX/LX2/index.html lines 29, 75", "PASS",
     "Hours column 2+2+2+3+3+2 = 14 = data-hours-project 14 = index.html data-hours-project 14. 14/50 = 28 percent of the module's 50 hours (index.html 'Tier U · 50 hours')."),
 row("proj-rubric-observable", "2.7 rubric observable", "course/modules/LX/LX2/project.html lines 534-544", "PASS",
     "Each of the 5 criteria x 4 levels has an observable cell; the bar is level 3 or above on every criterion (line 534). Level 4 C5 cell requires every statement sourced or marked, which the exemplar annotations test."),
 row("proj-rubric-criteria-count", "2.7 rubric count", "course/modules/LX/LX2/project.html lines 536-546, 552, 619, 684", "PASS",
     "Five criteria (C1-C5), four levels; two exemplars A and B; data-scores attributes match the official scores in the verdict paragraphs (lines 552, 619, 684)."),
 row("proj-autograder-na", "2.5 grading mode", "course/modules/LX/LX2/project.html line 353", "PASS",
     f"Line 353 'Rubric only. There is no autograder.' Plan 5.2 grading = rubric. {O}/run_graders.txt: 'no autograder (grading: rubric)'."),
 row("proj-adversarial-na", "plan decision", "course/modules/LX/LX2/project.html line 353", "PASS",
     "Line 353 'No adversarial review is used for this project.' Architect decisions (plan line 619): not adversarial, no question bank. Consistent."),
 row("proj-atlas-na", "plan B4", "course/modules/LX/LX2/project.html", "PASS",
     "No Atlas series, milestone or model name appears on the page; the case is PF-SIM (SIMULATED). Rung 4 offers a student-chosen model only."),
 row("proj-studio-na", "plan 2.2 / 5.x", "course/modules/LX/LX2/project.html", "PASS",
     "No studio or interactive component other than the labs and the self-assessment form on the page."),
 row("proj-data-and-figures-na", "plan 2.4 / architect decision 16", "course/modules/LX/LX2/project.html", "PASS",
     "grep for svg, canvas, figure, chart on the page: none. No figures, no new JS kernel (architect decision 16). The case table is generated by Lab 3 (no data file)."),
 row("proj-banned-and-process-words", "2.2 banned and process words", "course/modules/LX/LX2/project.html", "PASS",
     f"{O}/check_pages.txt PASS (BANNED list). grep for build, builder, verifier, round, request, ledger, planner, architect on the page: none. grep for ellipsis, 'for brevity', 'studies show', 'clearly', 'obviously', 'well known': none."),
 row("proj-case-realised-source", "2.3 / 2.5 case documentation", "course/modules/LX/LX2/project.html lines 89-90; Lab 1 REALISED; Lab 2 REALISED; Lab 3 table", "PASS",
     "Lab 1 realised values agree with the Lab 3 value at month 18 only (133 = 133; the other seven months differ); Lab 2 agrees at month 13 only (127 = 127). Verified by recompute_r5.py."),
 row("proj-rung1-plan-scope", "2.5 plan 5.1", "course/modules/LX/LX2/project.html lines 203-232; plans/LX2-build-plan.md lines 335-336", "PASS",
     "Plan 5.1 item 1: rung 1 is one solved SIMULATED validation with the four element checks, each with a why annotation. The page has four Element sections, each with reason steps (lines 205-232)."),
 row("proj-rung4-open-ended", "2.5 plan 5.1 item 4", "course/modules/LX/LX2/project.html lines 691-698; plans/LX2-build-plan.md lines 343-344", "PASS",
     "Rung 4 is optional and not graded (line 692); both items are open-ended and the page does not score them. Consistent with plan 5.1 item 4."),
 row("proj-exemplar-a-m1-window", "2.4 M1 test", "course/modules/LX/LX2/project.html lines 58, 87, 559", "PASS",
     "M1 is stated over the validation window (lines 58, 87); exemplar A tests M1 on months 13-36 with Part C and the Part A rows (line 559) and says the calibration bias is a fit check, not a test. Consistent with the stated window."),
 row("proj-exemplar-a-derivation-claim", "2.2 derivation claims", "course/modules/LX/LX2/project.html lines 527, 559", "PASS",
     "Line 527: the split is the reader's to check. Line 559: 'Its errors sum to 11, the only integer sum that prints as 0.9167 over 12 months' verified (only 11 in -200..200). 'Part A does not print those months' is true of the lab output."),
 row("proj-rung3-sr26-standard", "2.3 regulatory scope (round-4 FAIL re-verified)", "course/modules/LX/LX2/project.html lines 46, 336-344, 350-352; curriculum/06-profession-capstone.yaml lines 82-84; plans/LX2-build-plan.md lines 294 and 349-350", "PASS",
     "Round-4 FAIL asked for the attachment's validation passages and the expectations per element. The spec now lists four attachment expectations (lines 336-345) with pdf-page and printed-page locators, each quote verified exactly against the plain-curl PDF (see proj-source-attachment). Limitations has no attachment heading (grep: no 'Limitations' heading in the PDF), and the page says so. The curriculum brief's 'to the standard of SR 26-2' is met for the four elements by quoting the attachment's sound-practice statements, and the page claims no requirement."),
 row("proj-define-model-owner", "2.1 item 5 define-before-use (round-4 FAIL re-verified)", "course/modules/LX/LX2/project.html line 232 (first use, plain dfn); line 605", "PASS",
     "grep 'model owner' on the page: first occurrence line 232, '<dfn>model owner</dfn>, the person who signs the monthly planning figure' (plain dfn, no data-concept, as the rule requires). Line 605 is later. Round-4 FAIL is resolved."),
 row("proj-m2-statement-consistency", "2.4 statement consistency (round-4 FAIL re-verified)", "course/modules/LX/LX2/project.html lines 58, 87, 108, 208, 567 (plus lab docstrings 260-270 and 380-390 without the timing clause)", "PASS",
     "All five full M2 statements (58, 87, 108 Lab 1 docstring, 208 element 1 step 1, 567 exemplar A) read 'issued before month t starts and uses no information from month t'. Lab 2 and Lab 3 docstrings state the no-information half only, a consistent subset. M1 in lab docstring 108 reads 'holds over the validation window' (same as line 58). Round-4 FAIL is resolved."),
 row("proj-reading-count", "2.4 numbers in prose (new this round)", "course/modules/LX/LX2/project.html line 711 vs lines 359-360", "FAIL",
     "Line 711: 'This project cites frb2026fed for the two regulatory statements of the source note'. The source note has three keyed claims: line 359 (cover letter opening paragraph), line 360 (cover letter Applicability) and line 360 (attachment section I). Exemplar A's Sources row correctly says 'three regulatory statements'.",
     "Change 'the two regulatory statements of the source note' (line 711) to 'the three regulatory statements of the source note', or drop the count."),
]

mutants = []
import glob, os
for f in sorted(glob.glob("ledgers/LX2/mutants/r5_lab2_*.py")):
    mutants.append({"name": os.path.basename(f), "description": "new this round, student-error rung-2 mutant (see file docstring); killed by the rung-2 whole-block compare", "killed_by": "rung-2 instant check (lab2_check_r5.py); output in " + O + "/lab2_mutants_r5.txt"})
for f in ["mut-lab2-strict-band.py","mut-lab2-bias-mean-abs.py","mut-lab2-bias-sign-flip.py","mut-lab2-hit-over-8.py","mut-lab2-truncated-hit-rate.py",
          "r3_lab2_hit_rate_as_percent.py","r3_lab2_bias_sign_reversed.py","r3_lab2_hit_rate_rung1_length.py","r3_lab2_bias_rung1_length.py","r3_lab2_bias_adds_hit_count.py",
          "r4_lab2_hit_rate_horizon_minus_one.py","r4_lab2_bias_drops_first_month.py","r4_lab2_forecast_lagged_one_month.py","r4_lab2_hit_rate_three_decimals.py"]:
    mutants.append({"name": f, "description": "existing lab-2 student-error mutant (re-run this round)", "killed_by": "rung-2 instant check (lab2_check_r5.py); " + O + "/lab2_mutants_r5.txt"})
for n in ["r2-bias-denominator-horizon-minus-1","r2-bias-over-hit-count","r2-bias-sum-of-hit-errors-only","r2-one-sided-band-hit-rate","r2-strict-band-hit-rate"]:
    mutants.append({"name": n, "description": "round-2 candidate in ledgers/LX2/scripts/LX2-c-r3/lab2_check_r3.py (re-run this round)", "killed_by": O + "/lab2_check_r3_rerun.txt: ALL CANDIDATES AS EXPECTED"})

alts = [
 {"name": "alt-r5-a1-len-of-errors.py", "description": "ALTERNATIVE (must pass): horizon = len(errors) in both measures", "killed_by": "PASSES (" + O + "/alts_and_twin_r5.txt)"},
 {"name": "alt-r5-a2-count-by-generator.py", "description": "ALTERNATIVE (must pass): hit count by generator, len(REALISED) horizon", "killed_by": "PASSES (" + O + "/alts_and_twin_r5.txt)"},
 {"name": "alt-r5-a3-fraction-arithmetic.py", "description": "ALTERNATIVE (must pass): Fraction(hits) / horizon and Fraction(sum, 1) / horizon", "killed_by": "PASSES (" + O + "/alts_and_twin_r5.txt)"},
 {"name": "alt-r5-a4-float-with-fraction-decimal.py", "description": "ALTERNATIVE (must pass): float quotients printed by decimal_text", "killed_by": "PASSES (" + O + "/alts_and_twin_r5.txt)"},
 {"name": "alt-lab2-float-division.py", "description": "ALTERNATIVE (must pass, existing): float division for both measures", "killed_by": "PASSES (" + O + "/lab2_mutants_r5.txt)"},
]
mutants_all = mutants + alts

summary = ("LX2-c round 5: FAIL. 46 rows: 45 PASS (the 45 round-4 row ids kept; the three round-4 FAILs proj-rung3-sr26-standard, "
           "proj-define-model-owner and proj-m2-statement-consistency now PASS after re-verification) and 1 FAIL (new row proj-reading-count: "
           "line 711 says 'two' regulatory statements in the source note, which has three keyed claims at lines 359-360). "
           "Every number on project.html, the three twins, the expected blocks, and the exemplar figures was recomputed independently. "
           "All 24 lab-2 mutants killed (19 files plus the 5 round-2 candidates); 5 correct alternatives pass.")

frag = {
 "unit": "LX2",
 "slice": "LX2-c",
 "round": 5,
 "verifier": "Claude Haiku 5.5, independent verifier for LX2-c, round 5 (did not build LX2; no shared context with the builders)",
 "pin": PIN,
 "base": "round 4 fragment /Users/billyribeiro/.fanout/frags/E-LX2-c.round4.json at pin 9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba. Delta read with git diff 9a02b1af 7376a5e over course/modules/LX/LX2/project.html (23 insertions, 14 deletions; every hunk read), tests/labs/LX2/lab-LX2-project-1.py (one docstring line), plans/LX2-build-plan.md (unchanged in this delta). The whole page (734 lines) was also read in full.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE5-LX2-c",
 "scratch": "/tmp/lx2c-r5-src.11JiQe (SR 26-2 letter sr2602.htm and attachment SR2602.pdf by plain curl, HTTP 200; pdftotext -layout -> sr.txt; sr_html.txt)",
 "verified_at": "2026-11-04T17:12:09+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutants_all,
 "registry_flags": ["gpo1983dirks: references/references.json title reads 'Dirks v. SEC, 463 U.S. 646 (1982)' while its year field is 1983 (carried from round 4; no row in this slice prints a year for it, so no row depends on it; out of this slice to fix)."],
 "freshness_flags": ["The attachment passages were checked against the PDF fetched 2026-11-04 by plain curl; the registry url is the HTML letter, and the PDF is the one the admitted page links (SR2602.pdf)."],
 "notes": [
   "Full read: project.html (734 lines) read in full; the three twins were run and compared with the page (page_vs_twin_r5.txt).",
   "Round-4 FAIL rows re-verified from scratch: proj-rung3-sr26-standard (the spec now quotes the attachment with verified locators), proj-define-model-owner (plain dfn at first use, line 232), proj-m2-statement-consistency (all five full M2 statements match). All now PASS.",
   "Every other row was re-run or re-read this round because project.html changed in the delta; no row is carried forward.",
   "Design observation, not a row: plan 5.2 names a CSV input; the page instead has Lab 3 generate the case table from the stated seed and generator (plan 5.1 item 3 describes exactly that). The page states this openly, so it is not a FAIL here.",
   "Not checked: a rendered browser run of labs.js and rubric.js (no browser session used); 360 px horizontal scroll beyond page_smoke; build_site.py --check; full repository gate (targeted per the project rule); L01-L04 lessons and cards (outside slice c); the attachment PDF beyond the cited passages and headings.",
   "The verify_refs live run was limited to LX2 (6 of 560 entries, 0 problems) as the rules require; no other network access was used except the two plain-curl fetches of the SR 26-2 page and PDF.",
 ],
 "summary": summary,
}
out = "ledgers/LX2/LX2-c.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", out, len(rows), "rows", len(mutants_all), "mutants")
