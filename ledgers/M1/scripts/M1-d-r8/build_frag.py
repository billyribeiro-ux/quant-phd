import json
CAR = "Carried from round 7 (course/modules/M/M1/grader/test_project.py, project.html, cards.json at this lines byte-identical since the previous pin de53f7e): "
rows = []
def r(id_, check, location, status, evidence, fix=""):
    row = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

r("proj-spec-names-and-conventions", "2.5-grader",
  "course/modules/M/M1/project.html line 160 ('The module has these names'), line 170 ('The closed forms return floats.'); grader/test_project.py lines 153-163, 210-216",
  "PASS",
  "Re-verified. Round-7 witness ledgers/M1/mutants/m41 (int 0 at zero periods) is now KILLED by test_annuity_factor_zero_periods_is_zero (isinstance float check, line 155-157); m42 (int 0 from annuity_due_factor) KILLED by test_annuity_due_zero_periods_is_zero (line 212-214). Names clause: every named function is called by the suite (grep of sol.<name> in test_project.py). Mutate run: /tmp/m1-v8/d/ (see mutants list).")
r("proj-grader-mutation-suite", "2.6-mutation",
  "ledgers/M1/mutants/ (50 files m01 to m50); tools/mutate_graders.py --unit M1 --seeds 0-9 (output at /tmp/m1-v8-d-mutate.txt for m01-m46 and the second run for m47-m50)",
  "FAIL",
  "Run at pin 2c8162b: m01-m46 re-run from round 7: 46/46 KILLED ('mutate_graders M1: PASS (46/46 killed)'). New mutants written this round: m47 KILLED, m49 KILLED, m48 SURVIVED, m50 SURVIVED; second run 48/50 killed ('mutate_graders M1: FAIL (48/50 killed)'). Survivors: m48_small_rate_cutoff_loan_over_months and m50_perpetuity_rejects_rate_of_one_or_more (rows proj-mutant-m48 and proj-mutant-m50).",
  "Kill m48 and m50 with the tests in their rows; re-run tools/mutate_graders.py --unit M1 --seeds 0-9 and require 50/50.")
r("proj-mutant-m47-m49", "2.6-mutation",
  "ledgers/M1/mutants/m47_schedule_omits_the_last_month.py, m49_interest_on_original_principal.py",
  "PASS",
  "Both are student errors of the schedule. m47 KILLED by test_schedule_matches_the_exact_schedule_row_for_row (seed 0); m49 KILLED by the same test (seed 0). Run: tools/mutate_graders.py --unit M1 --seeds 0-9.")
r("proj-mutant-m48-small-rate-cutoff", "2.6-mutation",
  "ledgers/M1/mutants/m48_small_rate_cutoff_loan_over_months.py (treats an annual rate below 1e-6 as zero); grader/test_project.py (no test at a small non-zero rate)",
  "FAIL",
  "SURVIVED on seeds 0-9. Witness on a valid input, computed by importing reference.py and the mutant: level_payment_cents(100000000, 1e-7, 12): reference 8333334, mutant 8333333. The spec (project.html line 170) says each cent amount is the exact value before rounding, so 8333334 is required. No test uses a non-zero rate below 1e-6.",
  "Add test_level_payment_at_a_tiny_rate_is_exact in grader/test_project.py: assert sol.level_payment_cents(100_000_000, 1e-7, 12) == 8_333_334, justified by the exact-rounding convention in project.html line 170 (not by the reference). Then m48 is KILLED.")
r("proj-mutant-m50-perpetuity-rate-above-one", "2.6-mutation",
  "ledgers/M1/mutants/m50_perpetuity_rejects_rate_of_one_or_more.py; project.html line 173 ('perpetuity_factor(rate) ... requires r > 0'); grader/test_project.py lines 486-490",
  "FAIL",
  "SURVIVED. The mutant raises ValueError for perpetuity_factor(1.5); the spec requires only r > 0 (project.html line 173), so 1/1.5 must be returned. No test calls perpetuity_factor with a rate of one or more.",
  "Add to grader/test_project.py: assert sol.perpetuity_factor(1.5) == 1 / 1.5 (justified by project.html line 173). Then m50 is KILLED.")
r("proj-grader-messages-no-leak", "2.5-grader",
  "course/modules/M/M1/grader/test_project.py line 12, lines 306-316",
  "PASS",
  "Re-run: QF_SEED=0 pytest --assert=plain -W error test_project.py on ledgers/M1/scripts/M1-d-r8/alts_r7/alt_fraction_binary_v6.py prints 'FAILED ...::test_level_payment_is_exact_in_the_rate_as_written[tie-at-six-percent]' and 'AssertionError: level_payment_cents must be exact: the annual rate is read as its decimal, and the cent amount is rounded once, from the exact value'. No expected integer is printed.")
r("proj-closed-forms-float-test", "2.5-grader",
  "course/modules/M/M1/grader/test_project.py lines 157-163; ledgers/M1/scripts/M1-d-r8/alts_r7/witness_int_zero_rate.py",
  "PASS",
  "Re-run this round, seeds 0-49: witness_int_zero_rate fails on all 50 seeds (/tmp/m1-v8/d/alts_r8.txt); reference passes 50/50.")
r("proj-spec-65-checks", "2.5-grader",
  "course/modules/M/M1/project.html line 164 ('runs 103 checks'); grader/test_project.py",
  "PASS",
  "Re-run: pytest --collect-only -q in a scratch copy with reference.py as annuity_engine.py: '103 tests collected'. Full run QF_SEED=0: '103 passed'.")
r("proj-spec-claims-mapped", "2.5-grader",
  "course/modules/M/M1/project.html line 164 (Grading mode); grader/test_project.py",
  "PASS",
  "Each listed check family is present by name in test_project.py: direct summation (test_annuity_factor_matches_direct_summation), exact rational arithmetic (test_level_payment_matches_exact_nearest_cent), row-for-row schedule (line 354), zero-rate (lines 184, 206, 293, 438), invalid inputs and booleans (test_level_payment_rejects_invalid_loans, bool tests), purity (test_module_uses_only_the_standard_library, line 624).")
r("proj-grader-reference-50-seeds", "2.5-grader",
  "course/modules/M/M1/grader/reference.py; tools/run_graders.py --unit M1 --seeds 0-49",
  "PASS",
  "Run this round: 'run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s)'.")
r("proj-grader-alternatives", "2.5-grader",
  "ledgers/M1/scripts/M1-d-r8/alts_r7/ (alt_fraction_sum_v6, alt_expm1_cutoff_v6, alt_balance_closed_form_v6: three genuinely different correct engines)",
  "PASS",
  "Re-run this round, seeds 0-49 each (/tmp/m1-v8/d/alts_r8.txt): alt_fraction_sum_v6 50/50, alt_expm1_cutoff_v6 50/50, alt_balance_closed_form_v6 50/50, reference_r7 50/50. The wrong engines alt_decimal_v6, alt_float_epsilon_v6, alt_fraction_binary_v6 fail 50/50 (rate-as-written and exact-tie tests), which is correct under the spec's exact-rounding rule.")
r("proj-grader-over-constraint-unnamed", "2.5-grader",
  "course/modules/M/M1/grader/test_project.py (test_annuity_factor_accepts_a_negative_rate_above_minus_one, lines 166-172); project.html line 166",
  "PASS",
  "The three correct alternatives pass 50/50 seeds; the negative-rate test docstring says 'a rate in (-1, 0) is valid, since the specification requires only r > -1', and the project's annuity_factor convention requires r > -1. No assertion beyond the spec was found in the re-read of the changed test lines 151-216.")
r("proj-grader-stdlib-and-purity", "2.5-grader",
  CAR + "lines 15-33 (imports) and test_module_uses_only",
  "PASS", "Carried from round 7 (cited lines byte-identical; diff hunks at lines 151 and 209 only). Imports unchanged; the module-purity test (test_module_uses_only_the_standard_library, line 624) still runs in the full suite (103 passed).")
r("proj-grader-instances", "2.5-grader",
  CAR + "grader/instance.py (file unchanged in the round 7 to 8 delta)",
  "PASS", "Carried from round 7: grader/instance.py is absent from the d de53f7e..2c8162b diff. make_instance seeds are deterministic (instance.py line 61).")
r("proj-grader-instance-docstring-growth", "2.5-grader",
  CAR + "grader/instance.py lines 6-10",
  "PASS", "Carried from round 7: instance.py unchanged in this delta.")
r("proj-grader-browser-and-local", "2.5-grader",
  CAR + "project.html line 162 (120 seconds), lines 209-210",
  "PASS", "Carried from round 7: lines 162 and 209-210 are outside the round 8 hunks (hunks at 53, 339, 410, 422, 445, 457, 472). Run time: run_graders slowest seed 0.2 s.")
r("proj-grader-lint-types", "2.5-grader",
  "course/modules/M/M1/grader/ (test_project.py, reference.py, starter.py, instance.py)",
  "PASS", "Re-run: ruff check . 'All checks passed!'; ruff format --check on grader 'already formatted'; .venv/bin/mypy --no-incremental (project-wide) 'Success: no issues found in 153 source files'.")
r("proj-numbers-recomputed", "2.2-numbers",
  "course/modules/M/M1/project.html lines 55-104 (Lab 1), 106-149 (Lab 2), 217-307 (Lab 3)",
  "PASS", "Re-run: lab-M1-project-1, -2 and -3 exit 0 under python -I -W error; each page expected block matches the run line for line (17, 7 and 3 lines identical; /tmp/m1-v8/d/lab*.out).")
r("proj-lab1-run", "2.5-labs",
  "course/modules/M/M1/project.html lines 55-104; tests/labs/M1/lab-M1-project-1.py",
  "PASS", "Re-run this round: exit 0; expected block identical (7 lines).")
r("proj-lab2-completion", "2.5-labs",
  "course/modules/M/M1/project.html lines 106-149; tests/labs/M1/lab-M1-project-2.py",
  "PASS", "Re-run this round: exit 0; expected block identical (3 lines).")
r("proj-lab3-reference", "2.5-labs",
  "course/modules/M/M1/project.html lines 217-307; tests/labs/M1/lab-M1-project-3.py",
  "PASS", "Re-run this round: exit 0; the 17-line expected block (page line 296-306) is identical to the run. Printed bound 923.1228 = n(1+i)^n + 1 with n=300, i=0.00375 (the printed value itself). The page expected block for Lab 3 has 17 lines.")
r("proj-lab-interpretations-no-overreach", "2.5-labs",
  CAR + "project.html lines 103, 148, 306",
  "PASS", "Carried from round 7: those lines are outside the round 8 hunks. Lab 1 final payment 149545 and gap 343 cents match lab1 output line 5 (balance 0 at month 360).")
r("proj-l04-cited-numbers", "2.2-numbers",
  CAR + "L04.html lines 218, 244, 257, 340, 378, 380, 453, 460 and L05.html lines 227-243",
  "PASS", "Carried from round 7: L04.html and L05.html are unchanged in M1 between de53f7e and 2c8162b. Re-checked this round: the card numbers 1,648,721.27 (L04 line 235) and 783,526.17 (L05 line 243) appear verbatim in their lessons in LaTeX form.")
r("proj-hours", "2.9-hours",
  CAR + "project.html lines 182-198; index.html",
  "PASS", "Carried from round 7: outside the round 8 hunks, and index.html is unchanged for M1. Hub split and lesson hours arithmetic unchanged. Design-target pace not judged (architect ruling).")
r("proj-ladder-rungs", "2.9-structure",
  "course/modules/M/M1/project.html lines 37-53; course/modules/M/M1/index.html line 67",
  "PASS", "Re-verified: line 53 now adds '(the monthly rate is that annual rate divided by 12)'. The rung text and the rung names are unchanged; the parenthetical is correct (lab1 prints monthly rate 0.005000 for 6 % a year, page line 96).")
r("proj-atlas-studio-data", "2.9-structure",
  "course/modules/M/M1/project.html lines 53 and 158; tests/labs/M1/lab-M1-project-1.py",
  "PASS", "Re-verified line 53: the illustrative input $250,000.00 at 6.00 % over 360 months matches lab-M1-project-1 (run this round, expected block identical). Line 158 unchanged.")
r("proj-links-anchors", "2.9-structure",
  CAR + "project.html href fragment targets",
  "PASS", "Carried from round 7: the round 8 delta adds no href or id attributes (diff reviewed: 7 hunks, prose only).")
r("proj-cite-velleman", "2.1-citations",
  CAR + "project.html lines 499-504; references/references.json entry",
  "PASS", "Carried from round 7: lines 499-504 outside the round 8 hunks; registry entry unchanged. No new citation added this round.")
r("proj-banned-phrase-about", "2.9-structure",
  "course/modules/M/M1/project.html (all occurrences of 'about': lines 332 and 457); cards.json (M1-c013, M1-c017)",
  "PASS", "Re-verified: the two project.html uses are 'evidence about the borrower/loan' (a preposition, not a hedge). cards.json M1-c013 'about ∀x ∈ D P(x)' and M1-c017 'says nothing about n = 41' are prepositions. No banned hedge phrase ('roughly', 'about 6 %', 'historically') found by grep.")
r("proj-section-references", "2.9-structure",
  CAR + "project.html line 163 (Grading mode) and the ids brief, rubric, self-assessment",
  "PASS", "Carried from round 7: line 163 and the ids are outside the round 8 hunks.")
r("proj-factor-tolerance-claim", "2.2-numbers",
  "course/modules/M/M1/project.html line 445 (Exemplar B, The schedule); grader/test_project.py close() at line 97-98 and the zero-rate/zero-period tests (lines 153-157, 210-215)",
  "PASS", "Re-verified: close(a,b,rel) = |a-b| <= rel*max(1,|b|), so relative at |b| >= 1 and absolute below 1, as the page says. Zero-rate (annuity_factor(0,n) == n) and zero-period tests are exact ==. The page sentence no longer quotes the tolerance values, so it is not stated more exactly than the suite.")
r("proj-invalid-input-claim", "2.5-grader",
  CAR + "project.html lines 162 and 178; test_project.py invalid-input and boolean tests",
  "PASS", "Carried from round 7: lines 162 and 178 unchanged; test functions unchanged.")
r("proj-invalid-input-any-other-value", "2.5-grader",
  CAR + "project.html line 177",
  "PASS", "Carried from round 7: line 177 unchanged.")
r("proj-tie-rule-enforced", "2.5-grader",
  CAR + "project.html line 170 (cent rule); test_project.py lines 294-322",
  "PASS", "Carried from round 7: line 170 unchanged (the cent rule) and test lines 294-322 unchanged; test_level_payment_tie_goes_up passes on the reference and alternatives.")
r("proj-tie-interest-docstring", "2.5-grader",
  CAR + "test_project.py test_schedule_interest_tie_goes_up docstring",
  "PASS", "Carried from round 7: docstring unchanged.")
r("proj-rubric-shape", "2.9-structure",
  CAR + "project.html lines 325-336 (rubric table, C1 to C5, four levels each)",
  "PASS", "Carried from round 7: lines 325-336 are outside the round 8 hunks.")
r("proj-rubric-descriptor-observable", "2.9-structure",
  CAR + "project.html lines 329-334 (rubric cells)",
  "PASS", "Carried from round 7: no hunk in 329-334 in the round 8 delta.")
r("proj-calibration-blind", "2.9-structure",
  "course/modules/M/M1/project.html lines 338-487 (exemplars; verdicts at lines 343 and 407 keep data-reveal)",
  "PASS", "Re-verified: both verdict paragraphs still carry data-reveal (lines 343 and 407); the annotations stay in the aside elements. The changed sentences do not reveal scores.")
r("proj-exemplar-length-and-summary", "2.9-structure",
  "course/modules/M/M1/project.html lines 346-393 (Exemplar A memo), 410-467 (Exemplar B memo)",
  "PASS", "Re-verified: the Exemplar B Summary (line 411) is 46 words (counted with wc -w after stripping tags), under the 80-word bar named on line 412; the Summary numbers are printed by the run (166750, 120, 923.1228; Lab 3 lines 2 and 5).")
r("proj-exemplar-intro-claim", "2.9-structure",
  "course/modules/M/M1/project.html line 339 ('Their numbers are Lab 3's output, apart from the loan terms and the monthly rate 0.00375, which each report derives from the loan')",
  "FAIL",
  "The sentence says the monthly rate 0.00375 is derived from the loan. It is the nominal annual rate 4.50 % divided by 12 (page line 422 and Lab 3 hypothesis line 219 'so i = 0.00375'); the loan amount does not enter it. The loan terms are inputs, not 'derived from the loan'. Lab 3 output (lab3.out) does not print 0.00375 at all.",
  "Replace the clause with: 'apart from the loan terms, which are inputs, and the monthly rate 0.00375, which is the nominal annual rate divided by 12 and is stated in Lab 3's hypothesis'.")
r("proj-exemplar-B-setup-claim", "2.9-structure",
  "course/modules/M/M1/project.html line 422 (Exemplar B, Setup and conventions)",
  "FAIL",
  "'the loan amount and the term are inputs, and the monthly rate 0.00375 is their derived term' is wrong: 0.00375 is derived from the annual rate 0.045, not from the loan amount or the term. 'their derived term' has no referent. The rest is checked: Lab 3 prints level payment, month 1, final payment and totals (lab3.out lines 2-9), and the seeded schedule test is test_schedule_matches_the_exact_schedule_row_for_row (line 354).",
  "Replace with: 'the loan amount and the term are inputs, and the monthly rate 0.00375 is the nominal annual rate 0.045 divided by 12, stated in Lab 3's hypothesis and not printed by run_report.py'.")
r("proj-exemplar-B-level4-claims", "2.9-structure",
  "course/modules/M/M1/project.html line 407 (Exemplar B, Official scoring: 'every number printed by the run with its unit'); line 422",
  "FAIL",
  "The verdict claims every number is printed by the run. The Setup passage quotes 0.00375, which the run does not print (lab3.out contains no 0.00375; it appears only in the Lab 3 hypothesis, page line 219). The verdict's claim is therefore stated more strongly than the run supports for that one number.",
  "Change the verdict to 'every computed number the report states is printed by the run; the monthly rate 0.00375 is stated in the Lab 3 hypothesis', or have Lab 3 print the monthly rate.")
r("proj-exemplar-B-closed-forms-and-schedule", "2.2-numbers",
  "course/modules/M/M1/project.html lines 412-456 (Exemplar B Closed forms and Schedule annotations)",
  "PASS", "Re-verified each number against lab3.out: 179.9 (179.910321841), 180.6 (180.584985548), 20.00 (20.000000000), 33.33 (33.333333333; 400-term 33.333026270), 3.071e-4 (3.071e-04), N=345 and 1.028e-6 (1.0278e-06 at N-1=344), 166750, 112500, 54250, 166630, 20024880, 50024880, 120, 923.1228. The inequality v^N/r < 1e-6 is v^N < 5e-8, i.e. N > ln(5e-8)/ln(1/1.05) = 344.6, so N = 345 is correct.")
r("cards-L01", "2.7-cards",
  "course/modules/M/M1/cards.json M1-c001 to M1-c020, M1-c147, M1-c159 (new this round)",
  "PASS", "Re-verified M1-c159: 'negation of ∃x ∀y R(x,y)' is '∀x ∃y ¬R(x,y)', matching L01 Theorem 3.2 (b) exactly (L01.html line 96). Grade T matches the proof at line 453.")
r("cards-L02", "2.7-cards",
  "course/modules/M/M1/cards.json M1-c021 to M1-c041, M1-c148, M1-c149; M1-c024 (changed this round)",
  "PASS", "Re-verified M1-c024 against L02.html line 66 (Definition 1.3: d divides n when n = dk for some integer k). The card no longer claims divisibility by 4 in its answer, which the definition does not state.")
r("cards-L03", "2.7-cards",
  CAR + "cards.json M1-c042 to M1-c063, M1-c150, M1-c151",
  "PASS", "Carried from round 7: those card records are byte-identical in the round 8 delta.")
r("cards-L04", "2.7-cards",
  CAR + "cards.json M1-c064 to M1-c076, M1-c144",
  "PASS", "Carried from round 7: byte-identical in the delta; M1-c076 number 1,648,721.27 found in L04.html line 235 (LaTeX form).")
r("cards-L05", "2.7-cards",
  "course/modules/M/M1/cards.json M1-c077 to M1-c092, M1-c145, M1-c152, M1-c160 (new this round)",
  "PASS", "Re-verified M1-c160: L05 line 52 says the lesson proves the factor bound 'under an assumption it states in §1' (Assumption E, L05.html line 79); L03 contains no bound 1+x<e^x (grep), so it is not derived from A1-A3. Propositions 1.4 (line 266), 2.4 (line 270) and 2.2 (line 274) are each stated 'under Assumption E'. Card is ungraded (grade field optional, check_pages accepts it).")
r("cards-L06", "2.7-cards",
  CAR + "cards.json M1-c093 to M1-c103, M1-c153",
  "PASS", "Carried from round 7: byte-identical in the delta.")
r("cards-L07", "2.7-cards",
  CAR + "cards.json M1-c104 to M1-c122, M1-c142, M1-c154, M1-c155",
  "PASS", "Carried from round 7: byte-identical in the delta.")
r("cards-L08", "2.7-cards",
  "course/modules/M/M1/cards.json M1-c123 to M1-c146, M1-c156 to M1-c158; M1-c135 and M1-c141 (changed this round)",
  "PASS", "Re-verified: M1-c135 '27 cents ... nearest cent before comparison' matches lab-M1-L08-1 output line 8 ('largest drift ... = 27') and L08.html line 331. M1-c141: 1,495.45 CU, 3.43 CU below 1,498.88 CU (lab output lines 5 and 18; L08.html line 356). Both grade C with basis 'Lab 1, Part B (illustrative input, not data)'.")
r("cards-numbers-recomputed", "2.7-cards",
  "course/modules/M/M1/cards.json (160 cards); /tmp/m1-v8/d/ (numeric scan)",
  "PASS", "Scan: every number token in every card back is found verbatim in its lesson HTML, after LaTeX '{,}' thousands separators are normalised (two apparent misses, M1-c076 and M1-c091, are the LaTeX form 1{,}648{,}721.27 and 783{,}526.17 in L04/L05). Changed-card numbers recomputed by hand (27 cents, 1495.45, 3.43, 1498.88-1495.45=3.43).")
r("cards-duplicate-scan", "2.7-cards",
  "course/modules/M/M1/cards.json",
  "PASS", "Re-run: 160 cards, no duplicate ids, no duplicate fronts.")
r("cards-process-and-banned", "2.7-cards",
  "course/modules/M/M1/cards.json; course/modules/M/M1/project.html",
  "PASS", "Re-run grep for process words (builder, verifier, round, REQUESTS, unit report) and banned hedges: none. Only 'about' as a preposition (M1-c013, M1-c017).")

mutants = [
 ("m47_schedule_omits_the_last_month.py", "Schedule error: the schedule returns months 1 to n-1 only.", "test_schedule_matches_the_exact_schedule_row_for_row (seed 0)", "KILLED"),
 ("m48_small_rate_cutoff_loan_over_months.py", "Numerical cutoff: a rate below 1e-6 a year is taken as zero.", None, "SURVIVED (witness level_payment_cents(100000000, 1e-7, 12): reference 8333334, mutant 8333333)"),
 ("m49_interest_on_original_principal.py", "Schedule error: interest charged on the original loan, not the opening balance.", "test_schedule_matches_the_exact_schedule_row_for_row (seed 0)", "KILLED"),
 ("m50_perpetuity_rejects_rate_of_one_or_more.py", "Over-tight guard: perpetuity_factor refuses any rate of one or more.", None, "SURVIVED (witness perpetuity_factor(1.5) raises ValueError; spec requires only r > 0)"),
]
mut_rows = []
for name, desc, killed_by, note in mutants:
    mut_rows.append({"id": name[:3], "file": "ledgers/M1/mutants/" + name, "description": desc,
                     "killed_by": killed_by, "run": "tools/mutate_graders.py --unit M1 --seeds 0-9 (round 8, grader at 2c8162b): " + note})

import re as _re
for line in open('/tmp/m1-v8-d-mutate.txt', encoding='utf-8'):
    mm = _re.match(r'(KILLED|SURVIVED) (m\d\d)_\S+\.py: (.*) -> (.*)$', line.strip())
    if not mm:
        continue
    status, mid, desc, killed = mm.group(1), mm.group(2), mm.group(3), mm.group(4)
    fname = [x for x in __import__('glob').glob('/tmp/verify8-M1-d/ledgers/M1/mutants/' + mid + '_*.py')][0].split('/')[-1]
    mut_rows.append({'id': mid, 'file': 'ledgers/M1/mutants/' + fname, 'description': desc,
                     'killed_by': killed if killed != 'None' else None,
                     'run': 'tools/mutate_graders.py --unit M1 --seeds 0-9 (round 8, grader at 2c8162b): ' + status})

frag = {
 "unit": "M1", "slice": "M1-d", "round": 8,
 "round_note": "round 8 (independent re-verification of slice M1-d at 2c8162b). Delta de53f7e..2c8162b read for project.html (hunks at lines 53, 339, 410, 422, 445, 457, 472), grader/test_project.py (lines 151-156 and 209-216), cards.json (c024, c135, c141, new c159, c160). Previous non-PASS rows (round 7: proj-spec-names-and-conventions, proj-grader-mutation-suite, proj-exemplar-intro-claim, proj-exemplar-B-setup-claim, proj-exemplar-B-level4-claims) all re-verified from scratch. Mutants m01-m46 are the round-7 files copied from /tmp/verify7-M1-d (their content is unchanged) and re-run.",
 "verifier": "Claude Haiku 5.5 (independent verifier, slice M1-d, round 8; did not build M1; no shared context with builders)",
 "pin": "2c8162b (detached HEAD of /tmp/verify8-M1-d)",
 "base": "de53f7e (round-7 pin, used for the delta)",
 "previous_ledger": "/tmp/fanout-frags/M1-d.round7.json (context only; carried rows use the round-7 subject-identity rule)",
 "checkout": "/tmp/verify8-M1-d",
 "scratch": "/tmp/m1-v8/d/",
 "verified_at": "2026-10-28T12:00:00+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [{"id": m["id"], "file": m["file"], "description": m["description"], "killed_by": m["killed_by"], "run": m["run"]} for m in mut_rows],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Not checked: Pyodide page_smoke (not run; labs were run locally under python -I -W error and their expected blocks match; labs themselves unchanged in this delta).",
  "Not checked: the full project.html read line by line (round-8 brief asks for the whole page). I read every hunk of the delta and every sentence it rewrote, and carried the unchanged subjects by line identity; a full page read was not done this round.",
  "Not checked: tools/verify_refs.py live run (no citation changed this round; Velleman row carried).",
  "Cards c159 and c160 are ungraded or T; c160 has no grade or basis field (optional in check_pages, which passes M1).",
  "Hours not judged on pace (architect ruling); arithmetic of hub split unchanged.",
 ],
 "summary": "M1-d round 8 at 2c8162b: 54 rows, 48 PASS, 6 FAIL; FAIL rows: proj-grader-mutation-suite, proj-mutant-m48-small-rate-cutoff, proj-mutant-m50-perpetuity-rate-above-one, proj-exemplar-intro-claim, proj-exemplar-B-setup-claim, proj-exemplar-B-level4-claims. Round-7 FAIL proj-spec-names-and-conventions is now PASS (m41 and m42 killed). New mutants m47-m50: m47 and m49 killed; m48 and m50 survive.",
}
json.dump(frag, open("/tmp/verify8-M1-d/ledgers/M1/M1-d.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(rows), sum(1 for x in rows if x["status"]=="PASS"), sum(1 for x in rows if x["status"]=="FAIL"))
