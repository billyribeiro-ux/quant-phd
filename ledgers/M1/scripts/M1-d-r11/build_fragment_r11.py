"""Builds ledgers/M1/M1-d.json, the round-11 fragment of slice M1-d (run with python -I from the checkout).

Mutant rows are read from the run output of tools/mutate_graders.py (ledgers/M1/scripts/M1-d-r11/mutate_all.out),
the four new mutants from run_engine.sh runs recorded in this script's evidence strings.
usage: build_fragment_r11.py <checkout> <mutate_all.out>
"""

import json
import pathlib
import re
import sys

CHECKOUT = pathlib.Path(sys.argv[1])
MUT_OUT = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8").splitlines()

pat = re.compile(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$")
mutants = []
for line in MUT_OUT:
    m = pat.match(line)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    mutants.append(
        {
            "id": fname.split("_")[0] if not fname.startswith("r1") else "_".join(fname.split("_")[:2]),
            "file": f"ledgers/M1/mutants/{fname}",
            "description": desc,
            "killed_by": killed if status == "KILLED" else None,
            "run": "tools/mutate_graders.py --unit M1 --seeds 0-49 (round 11, checkout 91946cf): " + status,
        }
    )

NEW_MUT = [
    ("r11d_01_closing_balance_ignores_interest", "Closing balance is the opening balance less the whole payment, so the interest is never repaid and the schedule does not clear.", "KILLED", "test_level_payment_accepts_a_term_above_360_months (seed 0)"),
    ("r11d_02_growing_perpetuity_first_payment_at_time_zero", "Growing perpetuity values the stream one period early, as (1 + growth) / (rate - growth), a timing error on the first payment.", "KILLED", "test_growing_perpetuity_factor_matches_one_over_rate_minus_growth (seed 0)"),
    ("r11d_03_annuity_tiny_rate_treated_as_zero", "Annuity factor treats any rate below 1e-9 in size as zero and returns the number of periods, a cutoff the specification does not state.", "SURVIVED", None),
    ("r11d_04_final_payment_level_principal_opening", "The final month pays the level amount, while its principal is the whole opening balance, so the last row does not add up: payment is not interest plus principal.", "KILLED", "test_level_payment_and_schedule_accept_a_term_of_1200_months (seed 0)"),
]
for name, desc, status, killed in NEW_MUT:
    mutants.append(
        {
            "id": "_".join(name.split("_")[:2]),
            "file": f"ledgers/M1/mutants/{name}.py",
            "description": desc,
            "killed_by": killed,
            "run": "ledgers/M1/scripts/M1-d-r11/run_engine.sh over seeds 0-49: " + ("50 of 50 seeds fail" if status == "KILLED" else "50 of 50 seeds pass (survived)"),
        }
    )

CARRY9 = "Carried from round 10 (cited lines byte-identical since the previous pin af08ad1): "
rows = [
    {
        "id": "proj-spec-names-and-conventions", "check": "2.5-grader",
        "location": "course/modules/M/M1/project.html line 160 ('The module has these names'), line 170 ('The closed forms return floats.')",
        "status": "PASS",
        "evidence": CARRY9 + "cited lines unchanged in the af08ad1..91946cf delta (its hunks are at lines 164 and 407 only).",
    },
    {
        "id": "proj-grader-mutation-suite", "check": "2.6-mutants",
        "location": "ledgers/M1/mutants/ (82 files: m01 to m58, r10_01 to r10_10, r11_01 to r11_10, r11d_01 to r11d_04); tools/mutate_graders.py",
        "status": "FAIL",
        "evidence": "Re-run this round: tools/mutate_graders.py --unit M1 --seeds 0-49 on the 78 mutants committed at 91946cf: 'mutate_graders M1: PASS (78/78 killed)' (output in ledgers/M1/scripts/M1-d-r11/mutate_all.out). The four new student-error mutants r11d_01 to r11d_04 (ledgers/M1/scripts/M1-d-r11/mk_mut_r11d.py): r11d_01, r11d_02 and r11d_04 killed on every seed; r11d_03 (annuity factor treated as zero below 1e-9) survives 50 of 50 seeds. Row proj-mutant-r11d03-annuity-tiny-cutoff gives the witness and the sentence it violates.",
        "fix": "Add to test_project.py a closed-form check at a tiny nonzero rate (for example annuity_factor(5e-10, 360) against the exact sum, relative tolerance 1e-9). A cutoff of 1e-12 or below passes it; r11d_03 fails it.",
    },
    {
        "id": "proj-mutant-m47-m49", "check": "2.6-mutants", "location": "ledgers/M1/mutants/m47_schedule_omits_the_last_month.py, m48_small_rate_cutoff_loan_over_months.py, m49_interest_on_original_principal.py",
        "status": "PASS",
        "evidence": "Re-run this round (mutate_all.out): m47, m48 and m49 each KILLED at seed 0 (see the mutant list of this fragment).",
    },
    {
        "id": "proj-mutant-m48-small-rate-cutoff", "check": "2.6-mutants", "location": "ledgers/M1/mutants/m48_small_rate_cutoff_loan_over_months.py; grader/test_project.py (level-payment tests)",
        "status": "PASS",
        "evidence": "Re-run this round: m48 KILLED (mutate_all.out).",
    },
    {
        "id": "proj-mutant-m50-perpetuity-rate-above-one", "check": "2.6-mutants", "location": "ledgers/M1/mutants/m50_perpetuity_rejects_rate_of_one_or_more.py; grader/test_project.py lines 226-230",
        "status": "PASS",
        "evidence": "Re-run this round: m50 KILLED (mutate_all.out); the test asserts perpetuity_factor(1.5) = 1/1.5 and project.html line 173 says only r > 0 is required.",
    },
    {
        "id": "proj-mutant-m51-tiny-rate-cutoff-1e-8", "check": "2.6-mutants", "location": "ledgers/M1/mutants/m51_tiny_rate_cutoff_1e-8_treated_as_zero.py; grader/test_project.py lines 369-381",
        "status": "PASS",
        "evidence": "Re-run this round: m51 KILLED by test_level_payment_below_the_old_cutoffs_is_exact (mutate_all.out).",
    },
    {
        "id": "proj-mutant-m52-float-small-rate", "check": "2.6-mutants", "location": "ledgers/M1/mutants/m52_float_closed_form_for_small_rates.py",
        "status": "PASS",
        "evidence": "Re-run this round: m52 KILLED (mutate_all.out).",
    },
    {
        "id": "proj-mutant-m53-term-cap-360", "check": "2.6-mutants", "location": "ledgers/M1/mutants/m53_term_capped_at_360_months.py; grader/test_project.py lines 382-391",
        "status": "PASS",
        "evidence": "Re-run this round: m53 KILLED by test_level_payment_accepts_a_term_above_360_months (mutate_all.out).",
    },
    {
        "id": "proj-grader-tiny-rate-test-arithmetic", "check": "2.4-math", "location": "grader/test_project.py test_level_payment_below_the_old_cutoffs_is_exact (body lines 369-381; moved from 307-313)",
        "status": "PASS",
        "evidence": "Carried from round 10 (test body byte-identical since af08ad1; only its line numbers moved). Recomputed this round: Fraction(13296419) * (5e-9/12) / (1 - (1+5e-9/12)^-360) rounds to 36935 (python -I, scratch recompute).",
    },
    {
        "id": "proj-grader-perpetuity-rate-test", "check": "2.4-math", "location": "grader/test_project.py test_perpetuity_factor_accepts_a_rate_of_one_or_more (lines 226-230 at af08ad1, now shifted)",
        "status": "PASS",
        "evidence": "Carried from round 10 (test body byte-identical since af08ad1): 1/1.5 is the value of a perpetuity at a rate of 150 %; project.html line 173 requires r > 0 only.",
    },
    {
        "id": "proj-grader-tie-comment-digits", "check": "2.4-math", "location": "grader/test_project.py tie tests (comment block; body unchanged)",
        "status": "PASS",
        "evidence": "Carried from round 10: the tie-test comment is byte-identical since af08ad1; the digits re-derived this round (6 % one month on 100 cents = 100.5 cents, tie up to 101; scratch recompute gave 101).",
    },
    {
        "id": "proj-grader-alternatives", "check": "2.5-grader",
        "location": "ledgers/M1/scripts/M1-d-r11/alts/ (alt_r11_a, alt_r11_b, alt_r11_c); ledgers/M1/scripts/M1-d-r10/ and M1-d-r9/alts_r8/ alternatives; ledgers/M1/scripts/M1-d-r11/run_engine.sh",
        "status": "PASS",
        "evidence": "Re-run this round against the 91946cf grader, seeds 0-49, each 50/50 pass: alt_r11_a_direct_sum_annuity, alt_r11_b_exact_form_without_inverse, alt_r11_c_integer_half_up, reference, reference_r9 (rerun after a path fix), alt_expm1_cutoff_v6, alt_fraction_sum_v6, alt_balance_closed_form_v6, alt_r9_cutoff_1e15, alt_r10_fraction_sum, alt_r10_expm1_log1p, alt_r10_direct_sum_closed_payment, alt_r10_tie_explicit, and reference.py of r8 (all passed). No assertion rejects any of these. The type-error witness is a separate row (proj-grader-wrong-type-rate-valueerror).",
    },
    {
        "id": "proj-grader-reference-50-seeds", "check": "2.5-grader", "location": "course/modules/M/M1/grader/reference.py; tools/run_graders.py --unit M1 --seeds 0-49",
        "status": "PASS",
        "evidence": "Re-run this round: 'run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s)' (ledgers/M1/scripts/M1-d-r11/ and graders.out); own harness run_engine.sh reference.py: pass=50 fail=0; starter.py: pass=0 fail=50 (empty implementation must fail).",
    },
    {
        "id": "proj-grader-over-constraint-unnamed", "check": "2.5-grader",
        "location": "course/modules/M/M1/grader/test_project.py test_annuity_accepts_a_rate_just_above_minus_one (line 219), test_perpetuity_factor_accepts_a_rate_of_one_or_more (226-230), test_level_payment_below_the_old_cutoffs_is_exact (369-381)",
        "status": "PASS",
        "evidence": "Re-run this round: each assertion's value is re-derived (-0.999 gives 1001001000 = 1000 + 10^6 + 10^9; 1/1.5; 36935). The three correct alternative families pass 50/50 (proj-grader-alternatives). The over-constraint found this round is on non-numeric TYPES of rates, not on these values; it is recorded in proj-grader-wrong-type-rate-valueerror.",
    },
    {
        "id": "proj-spec-65-checks", "check": "2.5-grader", "location": "course/modules/M/M1/project.html line 164 ('which runs 188 checks')",
        "status": "PASS",
        "evidence": "Re-verified this round: the page now says 188 checks (it said 138 at af08ad1). Collect-only on the reference engine: '188 tests collected in 0.05s' (grader copy with reference.py as annuity_engine.py, python -I).",
    },
    {
        "id": "proj-spec-claims-mapped", "check": "2.5-grader", "location": "course/modules/M/M1/project.html line 164 (Grading mode); grader/test_project.py (sections 'closed forms', 'level payment and the amortization schedule', 'invalid inputs', 'purity')",
        "status": "PASS",
        "evidence": "Re-verified: the list on line 164 (closed forms, finite identities, schedule row for row, invariants, zero-rate case, invalid inputs, booleans, purity) maps to test names in the file: test_annuity_factor_matches_direct_summation, test_perpetuity_partial_sum_identity, test_schedule_matches_the_exact_schedule_row_for_row, test_schedule_closing_balance_is_never_negative, test_level_payment_zero_rate_is_the_loan_over_the_months, test_annuity_due_rejects_invalid_inputs, test_booleans_are_rejected_where_a_number_is_meant, test_functions_do_not_print_or_warn (purity block, line 899 onward).",
    },
    {
        "id": "proj-grader-messages-no-leak", "check": "2.5-grader",
        "location": "course/modules/M/M1/grader/test_project.py line 12 (docstring: never prints the expected value); new assertion messages at lines 393-399, 809-846",
        "status": "PASS",
        "evidence": "Read every new assertion message of the af08ad1..91946cf delta: none states an expected numeric value (for example 'the term has no upper limit: a 1200-month loan is valid and its payment is the exact value'). The 1200-month messages state the rule, not the number.",
    },
    {
        "id": "proj-closed-forms-float-test", "check": "2.5-grader", "location": "course/modules/M/M1/grader/test_project.py test_closed_forms_return_floats (lines 160-165)",
        "status": "PASS",
        "evidence": "Carried from round 10: the body is byte-identical since af08ad1; project.html line 170 ('The closed forms return floats'). Reference engine passes (50/50).",
    },
    {
        "id": "proj-grader-stdlib-and-purity", "check": "2.5-grader", "location": "course/modules/M/M1/grader/test_project.py purity block (line 899 onward)",
        "status": "PASS",
        "evidence": "Carried from round 8 (course/modules/M/M1/grader/test_project.py purity block byte-identical since 2c8162b; the diff since af08ad1 touches lines 218 to 807 only).",
    },
    {
        "id": "proj-grader-instances", "check": "2.5-grader", "location": "course/modules/M/M1/grader/instance.py (absent from the diff)",
        "status": "PASS",
        "evidence": "Carried from round 8: instance.py is byte-identical since 2c8162b; run_graders check_instances PASS this round (run_graders output).",
    },
    {
        "id": "proj-grader-instance-docstring-growth", "check": "2.5-grader", "location": "course/modules/M/M1/grader/instance.py docstring",
        "status": "PASS",
        "evidence": "Carried from round 8 (instance.py byte-identical since 2c8162b).",
    },
    {
        "id": "proj-grader-browser-and-local", "check": "2.5-grader", "location": "course/modules/M/M1/project.html lines 202-210 (autograder and local run)",
        "status": "PASS",
        "evidence": "Carried from round 8 for the lines cited (unchanged since 2c8162b). The command at line 209 was run this round with the same flags through run_engine.sh (-q -p no:cacheprovider --assert=plain -W error, QF_SEED).",
    },
    {
        "id": "proj-grader-lint-types", "check": "2.9-gates", "location": "course/modules/M/M1/grader/ (test_project.py, reference.py, starter.py, instance.py)",
        "status": "PASS",
        "evidence": "Re-run this round: .venv/bin/ruff check course/modules/M/M1 'All checks passed!'; .venv/bin/ruff format --check course/modules/M/M1 '4 files already formatted'; .venv/bin/mypy --no-incremental 'Success: no issues found in 153 source files' (mypy.out).",
    },
    {
        "id": "proj-numbers-recomputed", "check": "2.2-numbers", "location": "course/modules/M/M1/project.html lines 55-104 (Lab 1), 106-149 (Lab 2), 217-307 (Lab 3 and its interpretation at 306)",
        "status": "PASS",
        "evidence": "Recomputed this round with Fraction and 60-digit Decimal (ledgers/M1/scripts/M1-d-r11/ and /tmp/m1-v11/d/scratch/recompute.py): level payment 166750 cents (exact 166749.7434), month 1 interest 112500 and principal 54250, final payment 166630 (−120 from level), bound n(1+i)^n+1 = 923.1228, annuity 179.910321841, due 180.584985548, growing perpetuity 33.333333333, 400-term sum 33.333026270, tail 3.07063e-4, least N = 345, error at 344 = 1.02781e-6, total interest 20024880, total paid 50024880; Lab 1 factor 166.791614, payment 149888. All match the page.",
    },
    {
        "id": "proj-lab1-run", "check": "2.5-labs", "location": "course/modules/M/M1/project.html lines 55-104; tests/labs/M1/lab-M1-project-1.py",
        "status": "PASS",
        "evidence": "Re-run this round: python -I -W error tests/labs/M1/lab-M1-project-1.py output equals the page's expected block (7 lines, compared programmatically); tools/run_labs.py --unit M1 --page project: 'run_labs M1: PASS (3/3)'.",
    },
    {
        "id": "proj-lab2-completion", "check": "2.5-labs", "location": "course/modules/M/M1/project.html lines 106-149; tests/labs/M1/lab-M1-project-2.py",
        "status": "PASS",
        "evidence": "Re-run this round: twin output equals the expected block (3 lines); the blanks are 'total + v**k' and 'balance + interest - payment' (page line 148).",
    },
    {
        "id": "proj-lab3-reference", "check": "2.5-labs", "location": "course/modules/M/M1/project.html lines 217-307; tests/labs/M1/lab-M1-project-3.py",
        "status": "PASS",
        "evidence": "Re-run this round: twin output equals the expected block (17 lines, programmatic comparison); every printed value re-derived independently (proj-numbers-recomputed).",
    },
    {
        "id": "proj-lab-interpretations-no-overreach", "check": "2.5-labs", "location": "course/modules/M/M1/project.html lines 103, 148, 306",
        "status": "PASS",
        "evidence": "Carried from round 8 for the interpretation paragraphs (byte-identical since 2c8162b). Re-checked this round against the printed output: 343 cents = 149888 - 149545 (line 103); recurrence difference 4.2e-12 (line 148); 'the lab does not test the module; the suite does' (line 306) is consistent with the twin.",
    },
    {
        "id": "proj-l04-cited-numbers", "check": "2.2-numbers", "location": "course/modules/M/M1/project.html (no L04 figure is quoted; page cites L04 only by name in the ladder/conventions)",
        "status": "PASS",
        "evidence": "Carried from round 8 (lines unchanged since 2c8162b); the page quotes no number from L04 in the delta range.",
    },
    {
        "id": "proj-hours", "check": "2.9-structure", "location": "course/modules/M/M1/project.html lines 182-198 (Time budget); data-hours-project=30 at line 33",
        "status": "PASS",
        "evidence": "Re-verified this round: 2 + 3 + 8 + 7 + 6 + 4 = 30 equals data-hours-project 30 (line 33) and the Total row (line 194). Hub split not re-judged on pace (architect ruling: hours are design targets).",
    },
    {
        "id": "proj-ladder-rungs", "check": "2.9-structure", "location": "course/modules/M/M1/project.html lines 40-49", "status": "PASS",
        "evidence": "Carried from round 8 (byte-identical since 2c8162b).",
    },
    {
        "id": "proj-atlas-studio-data", "check": "2.9-structure", "location": "course/modules/M/M1/project.html (no atlas or studio data in the delta)", "status": "PASS",
        "evidence": "Carried from round 8 (byte-identical since 2c8162b).",
    },
    {
        "id": "proj-links-anchors", "check": "2.9-structure", "location": "course/modules/M/M1/project.html anchors #ladder, #spec, #conventions (167), #hours (182), #grader-section (200), #local (206), #report (213), #brief (309), #rubric (325), #exemplars (338), #self-assessment (483), #stretch (490), #reading (499), #references (507)",
        "status": "PASS",
        "evidence": "Re-verified this round by grep of id attributes on the page; python tools/check_pages.py --unit M1 PASS; check_projects PASS; page_smoke --unit M1 --pages project.html 'page_smoke M1: PASS'.",
    },
    {
        "id": "proj-cite-velleman", "check": "2.1-citations", "location": "course/modules/M/M1/project.html lines 501-504 (reading list, data-cite velleman2019prove)", "status": "PASS",
        "evidence": "Re-run this round: tools/verify_refs.py --offline 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit M1 (live) 're-verification of M1: 1 of 560 entries, 0 problems'. The page states no passage locator (line 501) and attributes no statement to the source.",
    },
    {
        "id": "proj-banned-phrase-about", "check": "2.9-structure", "location": "course/modules/M/M1/project.html lines 332, 388, 457 (the word 'about' in the rubric and exemplar text)", "status": "PASS",
        "evidence": "Re-read: 'about' appears in its ordinary sense ('evidence about the borrower', 'about the loan', 'about whether the borrower can pay'); the banned uses in BUILDER_RULES (approximate figures such as 'About 6%') do not occur on the page.",
    },
    {
        "id": "proj-section-references", "check": "2.9-structure", "location": "course/modules/M/M1/project.html sections 'The brief' (309) and 'The rubric' (323)", "status": "PASS",
        "evidence": "Carried from round 8 (byte-identical since 2c8162b).",
    },
    {
        "id": "proj-factor-tolerance-claim", "check": "2.4-math", "location": "course/modules/M/M1/project.html line 445 ('relative where the value is at least one and absolute below one; the zero-rate and zero-period factors are compared exactly')",
        "status": "PASS",
        "evidence": "Re-read against grader/test_project.py close() (line 124: rel*max(1, |b|)) and the exact comparisons test_annuity_factor_zero_rate_is_the_number_of_periods and test_annuity_factor_one_period_is_one_discounted_payment (== 1.0). The sentence holds for these tests.",
    },
    {
        "id": "proj-invalid-input-claim", "check": "2.5-grader", "location": "course/modules/M/M1/project.html line 178 ('Each invalid input named in this section raises ValueError.'); grader/test_project.py lines 482-528 region (invalid-input tests)",
        "status": "PASS",
        "evidence": "Carried from round 8 for the named conditions (boolean, float where a whole number is meant, non-finite, negative or zero counts): these tests are byte-identical since 2c8162b and pass on the reference. The conditions that the page does NOT name (string and None values of a rate) are a separate FAIL row, proj-grader-wrong-type-rate-valueerror.",
    },
    {
        "id": "proj-invalid-input-any-other-value", "check": "2.5-grader", "location": "course/modules/M/M1/grader/test_project.py boolean block (lines 645-670 at 91946cf) and project.html line 162",
        "status": "PASS",
        "evidence": "Re-run this round: the boolean cases and the new boolean-False cases (test_booleans_are_rejected_where_a_number_is_meant) are named by project.html line 162 ('a boolean where a number is meant') and pass on the reference; no alternative that raises ValueError for booleans fails. The string/None cases are in the FAIL row.",
    },
    {
        "id": "proj-tie-rule-enforced", "check": "2.4-math", "location": "course/modules/M/M1/project.html line 170 (the cent rule); grader/test_project.py tie tests (test_level_payment_tie_goes_up, test_schedule_interest_tie_goes_up)",
        "status": "PASS",
        "evidence": "Carried from round 8 (tie tests byte-identical since 2c8162b); re-run this round with the reference and the alternatives (proj-grader-alternatives).",
    },
    {
        "id": "proj-tie-interest-docstring", "check": "2.4-math", "location": "grader/test_project.py test_schedule_interest_tie_goes_up docstring",
        "status": "PASS",
        "evidence": "Carried from round 8: '1 cent accrues exactly 0.5 cents in month 1' at a 600 % annual rate: 1 * 6.0/12 = 0.5 is exact.",
    },
    {
        "id": "proj-rubric-shape", "check": "2.9-structure", "location": "course/modules/M/M1/project.html lines 325-336 (rubric table, five criteria, four levels)", "status": "PASS",
        "evidence": "Carried from round 8 (byte-identical since 2c8162b).",
    },
    {
        "id": "proj-rubric-descriptor-observable", "check": "2.9-structure", "location": "course/modules/M/M1/project.html lines 329-333 (descriptors)", "status": "PASS",
        "evidence": "Carried from round 8 (byte-identical since 2c8162b).",
    },
    {
        "id": "proj-calibration-blind", "check": "2.9-structure", "location": "course/modules/M/M1/project.html lines 338-487 (exemplars; verdict paragraphs at 343 and 407 are the data-reveal blocks)", "status": "PASS",
        "evidence": "Carried from round 8 for the exemplar structure (the only delta inside 338-487 is the verdict text at line 407, verified below); the reveal stays behind data-reveal.",
    },
    {
        "id": "proj-exemplar-length-and-summary", "check": "2.9-structure", "location": "course/modules/M/M1/project.html Exemplar B summary (line 411) and body (lines 420-478)",
        "status": "PASS",
        "evidence": "Counted this round (HTML stripped, math counted as one token): Exemplar B Summary 46 words (under 80); body sections Summary, Setup, Closed forms, The schedule, Limitations total 642 words (400 to 900 bar; the approximate count is 642 with math as one token each). Exemplar A is not changed this round.",
    },
    {
        "id": "proj-exemplar-intro-claim", "check": "2.2-numbers", "location": "course/modules/M/M1/project.html line 339 ('Exemplar B's derivations are symbolic or use only the loan inputs and printed values')",
        "status": "PASS",
        "evidence": "Re-checked this round: Exemplar B's derivations (lines 469-476) use the loan inputs (n, i, L, P) and symbols; the only printed values quoted are from Lab 3 (proj-numbers-recomputed).",
    },
    {
        "id": "proj-exemplar-B-setup-claim", "check": "2.2-numbers", "location": "course/modules/M/M1/project.html line 422 (Exemplar B, Setup and conventions)",
        "status": "PASS",
        "evidence": "Carried from round 10 (line 422 byte-identical since af08ad1): 0.045/12 is written as a symbol; the loan inputs are named; the run prints the level payment, the first month, the final payment and the totals (Lab 3 output lines 260-270).",
    },
    {
        "id": "proj-exemplar-B-level4-claims", "check": "2.3-grades", "location": "course/modules/M/M1/project.html line 407 (Exemplar B official-scoring verdict), lines 411 and 445 (the bound)",
        "status": "PASS",
        "evidence": "Re-verified this round. Line 407 now reads 'the cent bound is derived in A4 from the rule and the loan inputs, its value 923.1228 printed by the run'. A4 (lines 472) derives |F-P| <= (n-1)(1+i)^(n-1) + 1 <= n(1+i)^n + 1 from the recursion and n, i (checked step by step: the induction on |D_k| <= k(1+i)^(k-1), the step using 1 <= (1+i)^k, and the triangle inequality). Lab 3 prints 'bound on final minus level payment (cents): 923.1228' and that equals 300*(1.00375)^300 + 1 (recomputed). The round-10 defect (the bound described as derived from the printed run) is fixed.",
    },
    {
        "id": "proj-exemplar-B-closed-forms-and-schedule", "check": "2.4-math", "location": "course/modules/M/M1/project.html lines 431-456 (Exemplar B closed forms and schedule)",
        "status": "PASS",
        "evidence": "Re-checked this round: 179.9, 180.6, 20.00, 33.33, 3.071e-4 (q^400/(r-g), q=(1+g)/(1+r)), N=345 and the error 1.028e-6 at 344 all match the Lab 3 output; the schedule figures 166750, 112500, 54250, 166630, 30000000, 50024880 and 20024880 match the run.",
    },
    {
        "id": "cards-L01", "check": "2.7-cards", "location": "course/modules/M/M1/cards.json, the 24 cards of lesson L01 (M1-c001 to M1-c170): changed M1-c008, new M1-c170",
        "status": "PASS",
        "evidence": "Changed/new cards checked against L01.html (Theorem 3.1, the two negation identities, lines 31-43 and 218-221 of the lesson text): M1-c008 'negation of forall x in D P(x)' is 'exists x in D not P(x) (Theorem 3.1)'; M1-c170 'negation of exists x in D P(x)' is 'forall x in D not P(x) (Theorem 3.1)'. Unchanged cards carried from round 10 (byte-identical).",
    },
    {
        "id": "cards-L02", "check": "2.7-cards", "location": "course/modules/M/M1/cards.json, the 26 cards of lesson L02: changed M1-c025, M1-c029, M1-c030; new M1-c171, M1-c172, M1-c173",
        "status": "PASS",
        "evidence": "Checked against L02.html lines 28-29 (Fact 1.4 'the unit takes it as given. It is not proved here'), 33 (Theorem 1.5: a+b = 2(m+n), ab = 4mn), 40 (Lemma 2.2: no integer is both even and odd). M1-c171 'Does the unit prove that every integer is even or odd? No. ... (Fact 1.4)' matches line 29. Carried for the rest.",
    },
    {
        "id": "cards-L03", "check": "2.7-cards", "location": "course/modules/M/M1/cards.json, the 27 cards of lesson L03: changed M1-c049, M1-c052; new M1-c174, M1-c175",
        "status": "PASS",
        "evidence": "Checked against L03.html: Proposition 1.4 (ln(e^x) = x; e^(ln y) = y, y > 0; line 39), Proposition 1.6(a) (ln 1 = 0), 1.6(c) (ln(1/y) = -ln y). M1-c174 and M1-c175 match. Carried for the rest.",
    },
    {
        "id": "cards-L04", "check": "2.7-cards", "location": "course/modules/M/M1/cards.json, the 16 cards of lesson L04: changed M1-c067; new M1-c176",
        "status": "PASS",
        "evidence": "L04.html Definition 1.2 (line 26): factor e^(rt) over t years and effective annual rate e^r - 1. M1-c067 and M1-c176 match.",
    },
    {
        "id": "cards-L05", "check": "2.7-cards", "location": "course/modules/M/M1/cards.json, the 20 cards of lesson L05: changed M1-c083; new M1-c177",
        "status": "PASS",
        "evidence": "L05.html Proposition 1.4 (raw HTML): 'Assume E. Let r > 0. For every t > 0, 0 < (1 + r)^(-t) < 1. Moreover t -> (1 + r)^(-t) is strictly decreasing for t >= 0.' M1-c083 ('strictly between 0 and 1 ... (Proposition 1.4)') and M1-c177 ('strictly decreases for t >= 0 ... (Proposition 1.4)') match.",
    },
    {
        "id": "cards-L06", "check": "2.7-cards", "location": "course/modules/M/M1/cards.json, the 12 cards of lesson L06: changed M1-c098",
        "status": "PASS",
        "evidence": "L06.html Corollary 2.3 (line 53): S_n(1) = n for every n >= 1; the closed form is not defined at q = 1. M1-c098 'S_n(1)' back 'S_n(1) = n (Corollary 2.3)' matches.",
    },
    {
        "id": "cards-L07", "check": "2.7-cards", "location": "course/modules/M/M1/cards.json, the 24 cards of lesson L07: changed M1-c108; new M1-c178",
        "status": "PASS",
        "evidence": "L07.html Definition 3.1 (line 65-67): payment C(1+g)^(t-1) at each time t >= 1, g > -1; 'Write q = (1 + g)/(1 + r). Because g > -1, 1 + g > 0, so q > 0.' M1-c108 and M1-c178 match.",
    },
    {
        "id": "cards-L08", "check": "2.7-cards", "location": "course/modules/M/M1/cards.json, the 30 cards of lesson L08: changed M1-c123, M1-c146; new M1-c179",
        "status": "PASS",
        "evidence": "L08.html Section 1 (line 70): interest for one month on balance B at monthly rate i is iB; Section 3 (lines 174-176): interest I_k taken to the nearest cent with exact halves going up; the regular payment A taken to the nearest cent, paid in months 1 to n-1. M1-c123, M1-c146 and M1-c179 match (c179 cites Section 3, which is 'The schedule in integer cents', heading 3).",
    },
    {
        "id": "cards-numbers-recomputed", "check": "2.7-cards", "location": "course/modules/M/M1/cards.json (179 cards)",
        "status": "PASS",
        "evidence": "Counted this round: 179 cards, 179 unique ids. Every number on a changed or new card appears in its lesson or is a formula the lesson states: 1 (Fact 1.4), 2k or 2k+1, 2(m+n), 4mn, 0 and ln 1, x, y, e^(rt), e^r - 1, 0 and 1, n, C(1+g)^(t-1), iB, nearest cent.",
    },
    {
        "id": "cards-duplicate-scan", "check": "2.7-cards", "location": "course/modules/M/M1/cards.json",
        "status": "PASS",
        "evidence": "Pairwise scan this round (difflib over all 179 fronts and backs): the highest-similarity pairs are distinct questions (for example M1-c008 'negation of forall' and M1-c170 'negation of exists', fronts 0.97 similar but different claims; M1-c118/M1-c154 differ in N). No duplicate pair involves a changed card.",
    },
    {
        "id": "cards-process-and-banned", "check": "2.9-structure", "location": "course/modules/M/M1/cards.json; course/modules/M/M1/project.html",
        "status": "PASS",
        "evidence": "Scanned the changed and new cards and the project page for banned phrases (roughly, historically, About 6 %, ellipses) and process words (build, builder, round, verifier, unit report, REQUEST): none found.",
    },
    {
        "id": "proj-grader-minus-one-docstring-arithmetic", "check": "2.4-math", "location": "course/modules/M/M1/grader/test_project.py test_annuity_accepts_a_rate_just_above_minus_one docstring (lines 219-222)",
        "status": "PASS",
        "evidence": "Round-10 defect fixed: the docstring now reads the closed form as (1 - (1+r)^-3) / r = (1 - 10^9) / (-0.999). Recomputed: (1 - 10^9)/(-0.999) = 1001001000.0 exactly (python, Fraction), equal to 1000 + 10^6 + 10^9.",
    },
    {
        "id": "proj-mutant-m57-term-cap-480", "check": "2.6-mutants", "location": "ledgers/M1/mutants/m57_term_capped_at_480_months.py; grader/test_project.py test_level_payment_and_schedule_accept_a_term_of_1200_months (lines 393-409)",
        "status": "PASS",
        "evidence": "Round-10 survivor now killed: m57 KILLED by test_level_payment_and_schedule_accept_a_term_of_1200_months (mutate_all.out). The new test checks level_payment_cents(100000, 0.0384, 1200) == 327 (recomputed exactly: 327) and a 1200-row schedule equal to the exact one.",
    },
    {
        "id": "proj-mutants-m54-m58-new", "check": "2.6-mutants", "location": "ledgers/M1/mutants/m54_growing_perpetuity_refuses_negative_growth.py, m55_perpetuity_refuses_rates_below_a_small_floor.py, m56_schedule_interest_tie_rounds_down.py, m58_annuity_refuses_rates_below_minus_half.py",
        "status": "PASS",
        "evidence": "Re-run this round: m54, m55, m56 and m58 KILLED (mutate_all.out).",
    },
    {
        "id": "proj-alt-correct-implementations-r11", "check": "2.5-grader",
        "location": "ledgers/M1/scripts/M1-d-r11/alts/alt_r11_a_direct_sum_annuity.py, alt_r11_b_exact_form_without_inverse.py, alt_r11_c_integer_half_up.py",
        "status": "PASS",
        "evidence": "Three new correct engines (direct summation of the annuity; the exact form L i (1+i)^n / ((1+i)^n - 1) with no inverse; integer half-up rounding of the exact rational): each passes 50/50 seeds (run_engine.sh). They pass the new boundary tests and the 1200-month test.",
    },
    {
        "id": "proj-grader-wrong-type-rate-valueerror", "check": "2.5-grader",
        "location": "course/modules/M/M1/grader/test_project.py line 89 (must_raise docstring: 'The specification names ValueError for every invalid input.'), lines 633-645 (rates given as strings or None), 707-715 (growth rates as strings or None), 246-265 (periods and rates of the wrong type); project.html lines 162 and 178",
        "status": "FAIL",
        "evidence": "Witness: ledgers/M1/scripts/M1-d-r11/alts/witness_r11_type_error_for_wrong_types.py is the reference with values of a non-numeric type (string, None, list) raising TypeError (booleans and floats keep ValueError, as project.html line 162 names them). With seed 0 the suite gives '37 failed, 151 passed'; the failures include rates given as strings or None (test_perpetuity_rejects_non_finite_and_wrong_type_rates, test_growing_perpetuity_rejects_wrong_types, test_annuity_due_rejects_invalid_inputs, test_level_payment_rejects_invalid_loans[1000-None-12]). project.html line 162 says ValueError is raised 'for the conditions the conventions below name'; line 178 says 'Each invalid input named in this section raises ValueError'. A rate given as a string or None is not among the named conditions, so the page does not state the requirement the tests enforce, and the docstring overstates it. The sentence on line 89 is the claim that is not supported.",
        "fix": "Either name the requirement on the page (in the conventions of project.html, after line 178, say that a value of another type, such as a string or None where a number is meant, raises ValueError) or relax the tests and the must_raise docstring to accept TypeError for non-numeric types. Keep ValueError for booleans, floats where a whole number is meant, and non-finite numbers, which the page names.",
    },
    {
        "id": "proj-mutant-r11d03-annuity-tiny-cutoff", "check": "2.6-mutants",
        "location": "ledgers/M1/mutants/r11d_03_annuity_tiny_rate_treated_as_zero.py; course/modules/M/M1/grader/test_project.py lines 127-129 (docstring: 'a(n) = sum of v^k ... relative tolerance 1e-9'); project.html line 171 ('annuity_factor(rate, periods) is a = sum v^k')",
        "status": "FAIL",
        "evidence": "The mutant returns float(n) when |rate| < 1e-9. Survives all 50 seeds (run_engine.sh: pass=50 fail=0; seed 0 under pytest: '188 passed'). Its error is measurable: at rate 5e-10 and 360 periods the mutant returns 360.0 against the exact sum 359.99996751 (relative error 9.0e-8, above the 1e-9 tolerance that the test docstring at line 128 states for the closed form); at 1e-10 the relative error is 1.8e-8. The explicit rates the grader passes to annuity_factor are 0.05, 0.01, -0.01, -0.5, -0.999 and the instance rate ANN_RATE = annuity_bps/10000 with annuity_bps in 10 to 2000 (grader/instance.py line 67), so the smallest nonzero rate any test uses is 0.001 (grep of annuity_factor calls in test_project.py).",
        "fix": "Add a test that annuity_factor(5e-10, 360) and annuity_factor(1e-10, 360) equal the exact sum (or the exact closed form in Fractions) at relative tolerance 1e-9. A cutoff of 1e-12 or below passes this test (its error is about (n-1)*r/2, under 1e-9 for r below 1e-12), so the fix does not over-constrain the alternatives.",
    },
    {
        "id": "proj-mutants-r11d-new", "check": "2.6-mutants",
        "location": "ledgers/M1/mutants/r11d_01_closing_balance_ignores_interest.py, r11d_02_growing_perpetuity_first_payment_at_time_zero.py, r11d_04_final_payment_level_principal_opening.py",
        "status": "PASS",
        "evidence": "Three new plausible student errors, killed on every seed 0-49 (run_engine.sh: pass=0 fail=50). r11d_01 closing = opening - payment (first failing test in file order: test_level_payment_accepts_a_term_above_360_months); r11d_02 growing value (1+g)/(r-g) (first failure: test_growing_perpetuity_factor_matches_one_over_rate_minus_growth); r11d_04 the final month pays the level amount while its principal is the whole balance (first failure: test_level_payment_and_schedule_accept_a_term_of_1200_months; also test_schedule_matches_the_exact_schedule_row_for_row and test_schedule_payment_is_interest_plus_principal). An earlier candidate, a final principal forced to the opening balance while the payment is unchanged, was EQUIVALENT (the reference's final payment is opening + interest, so the substitution is the identity) and was discarded.",
    },
    {
        "id": "proj-grader-1200-month-test-r11", "check": "2.4-math", "location": "course/modules/M/M1/grader/test_project.py lines 393-409",
        "status": "PASS",
        "evidence": "Re-derived: 0.0384/12 = 0.0032 = 2/625 (denominator odd, so no interest amount is a half cent, since 4 * balance would have to equal 625 times an odd number); level payment at 100000 cents, 1200 months: 327 (python Fraction); exact_rows(100000, 384, 1200) equals the reference schedule (run_engine reference pass). The term has no upper limit by project.html line 177 ('a term that is not a whole number of months of one or more').",
    },
    {
        "id": "proj-grader-new-boundary-tests-r11", "check": "2.4-math", "location": "course/modules/M/M1/grader/test_project.py lines 810-898 (isolated boundary checks) and the parametrized additions at lines 246-262, 633-645, 707-715, 748-770, 781-800",
        "status": "PASS",
        "evidence": "Each new expected value re-derived: annuity at -0.999 with 3 periods = 1001001000; annuity at 0 periods = float 0; one period = 1/(1+r); level payment of 1 cent over 1 month at 5 % = 1; 499 cents over 1000 months at zero rate = 0; 1000 cents at 5 % over 1 month = 1004 (schedule); 10000 cents at 12 % over 1 month = 10100 with interest 100. Each new invalid-input case is a condition that project.html names (negative or zero principal, a term that is zero, negative, fractional or boolean, a non-finite or negative annual rate, growth at or above the rate, a rate of zero or less for the perpetuity) except the string and None values covered by proj-grader-wrong-type-rate-valueerror.",
    },
    {
        "id": "proj-commands-gate-r11", "check": "2.9-gates", "location": "tools/check_pages.py --unit M1; tools/check_projects.py --unit M1; tools/check_dag.py --all; tools/run_labs.py --unit M1; tools/page_smoke.py --unit M1 --pages project.html",
        "status": "PASS",
        "evidence": "Re-run this round: check_pages M1 PASS; check_projects M1 PASS; check_dag --all PASS (M1, S7, AC1, AC2, AC4, CF1, AP1); run_labs M1 'PASS (11/11)' and project 'PASS (3/3)'; page_smoke M1 (project.html) 'PASS'.",
    },
    {
        "id": "proj-grader-run-graders-r11", "check": "2.5-grader", "location": "tools/run_graders.py --unit M1 --seeds 0-49",
        "status": "PASS",
        "evidence": "Re-run this round: 'run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s)' (ledgers/M1/scripts/M1-d-r11/graders.out).",
    },
]

# keep each previous round-10 row id present
PREVIOUS_IDS = [
    "proj-spec-names-and-conventions", "proj-grader-mutation-suite", "proj-mutant-m47-m49", "proj-mutant-m48-small-rate-cutoff",
    "proj-mutant-m50-perpetuity-rate-above-one", "proj-mutant-m51-tiny-rate-cutoff-1e-8", "proj-mutant-m52-float-small-rate",
    "proj-mutant-m53-term-cap-360", "proj-grader-tiny-rate-test-arithmetic", "proj-grader-perpetuity-rate-test",
    "proj-grader-tie-comment-digits", "proj-grader-alternatives", "proj-grader-reference-50-seeds",
    "proj-grader-over-constraint-unnamed", "proj-spec-65-checks", "proj-spec-claims-mapped", "proj-grader-messages-no-leak",
    "proj-closed-forms-float-test", "proj-grader-stdlib-and-purity", "proj-grader-instances", "proj-grader-instance-docstring-growth",
    "proj-grader-browser-and-local", "proj-grader-lint-types", "proj-numbers-recomputed", "proj-lab1-run", "proj-lab2-completion",
    "proj-lab3-reference", "proj-lab-interpretations-no-overreach", "proj-l04-cited-numbers", "proj-hours", "proj-ladder-rungs",
    "proj-atlas-studio-data", "proj-links-anchors", "proj-cite-velleman", "proj-banned-phrase-about", "proj-section-references",
    "proj-factor-tolerance-claim", "proj-invalid-input-claim", "proj-invalid-input-any-other-value", "proj-tie-rule-enforced",
    "proj-tie-interest-docstring", "proj-rubric-shape", "proj-rubric-descriptor-observable", "proj-calibration-blind",
    "proj-exemplar-length-and-summary", "proj-exemplar-intro-claim", "proj-exemplar-B-setup-claim", "proj-exemplar-B-level4-claims",
    "proj-exemplar-B-closed-forms-and-schedule", "cards-L01", "cards-L02", "cards-L03", "cards-L04", "cards-L05", "cards-L06",
    "cards-L07", "cards-L08", "cards-numbers-recomputed", "cards-duplicate-scan", "cards-process-and-banned",
    "proj-grader-minus-one-docstring-arithmetic", "proj-mutant-m57-term-cap-480", "proj-mutants-m54-m58-new",
    "proj-alt-correct-implementations-r10", "proj-grader-collect-count", "proj-commands-gate-r10", "proj-grader-run-graders-r10",
]
have = {r["id"] for r in rows}
# proj-alt-correct-implementations-r10, proj-grader-collect-count, proj-commands-gate-r10 and proj-grader-run-graders-r10 are added below
rows.append({
    "id": "proj-alt-correct-implementations-r10", "check": "2.5-grader",
    "location": "ledgers/M1/scripts/M1-d-r10/alt_r10_*.py and ledgers/M1/scripts/M1-d-r9/alts_r8/alt_expm1_cutoff_v6.py, alt_fraction_sum_v6.py, alt_balance_closed_form_v6.py, alt_r9_cutoff_1e15.py",
    "status": "PASS",
    "evidence": "Re-run this round against the 91946cf grader, seeds 0-49: alt_r10_fraction_sum, alt_r10_expm1_log1p, alt_r10_direct_sum_closed_payment, alt_r10_tie_explicit, alt_expm1_cutoff_v6, alt_fraction_sum_v6, alt_balance_closed_form_v6, alt_r9_cutoff_1e15 each pass 50/50 (prev*.out).",
})
rows.append({
    "id": "proj-grader-collect-count", "check": "2.5-grader", "location": "course/modules/M/M1/grader/test_project.py; course/modules/M/M1/project.html line 164",
    "status": "PASS",
    "evidence": "Re-run this round: collect-only with the reference engine: '188 tests collected in 0.05s', equal to the page's 188 (line 164).",
})
rows.append({
    "id": "proj-commands-gate-r10", "check": "2.9-gates", "location": "tools/check_pages.py --unit M1; tools/check_projects.py --unit M1; tools/check_dag.py --all; tools/run_labs.py --unit M1; tools/verify_refs.py --offline",
    "status": "PASS",
    "evidence": "Re-run this round (see proj-commands-gate-r11): all PASS; verify_refs --offline 560 entries, 0 problems.",
})
rows.append({
    "id": "proj-grader-run-graders-r10", "check": "2.5-grader", "location": "tools/run_graders.py --unit M1 --seeds 0-49",
    "status": "PASS",
    "evidence": "Re-run this round: run_graders M1 PASS 50/50 (see proj-grader-run-graders-r11).",
})

missing = [i for i in PREVIOUS_IDS if i not in {r["id"] for r in rows}]
assert not missing, missing

fragment = {
    "unit": "M1",
    "slice": "M1-d",
    "round": 11,
    "round_note": "round 11 (independent re-verification of slice M1-d at 91946cf). Delta af08ad1..91946cf read for project.html (lines 164 and 407), grader/test_project.py (new tests 218-230 and 246-262, 393-409, 625-715, 748-770, 781-800, 810-898), cards.json (c008, c025, c029, c030, c049, c052, c067, c083, c098, c108, c123, c146 changed; c170 to c179 new). Previous non-PASS rows re-verified; carried PASS rows only where the cited lines or bodies are byte-identical. Every command row re-run. Mutants: 78 committed plus four new student-error mutants r11d_01 to r11d_04 (one replaced after it proved equivalent).",
    "verifier": "Claude Haiku 5.5 (independent verifier, slice M1-d, round 11; did not build M1; no shared context with builders)",
    "pin": "91946cf (detached HEAD of /tmp/verify11-M1-d)",
    "base": "af08ad1 (round-10 pin, used for the delta)",
    "previous_ledger": "/tmp/fanout-frags/M1-d.round10.json (context only)",
    "checkout": "/tmp/verify11-M1-d",
    "scratch": "/tmp/m1-v11/d/",
    "verified_at": "2026-10-28T13:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Hours not judged on pace (architect ruling); the arithmetic 2+3+8+7+6+4 = 30 equals data-hours-project 30.",
        "Card count is 179 (cards.json); round 10 recorded 168. No page states a card count.",
        "Not checked: the Pyodide browser run of the grader and the 10-second Pyodide budget per lab (page_smoke reported PASS but its per-lab timing was not read); the live Crossref/registry run beyond tools/verify_refs.py --unit M1 (1 of 560 entries re-verified live: 0 problems).",
        "The committed scripts in ledgers/M1/scripts/M1-d-r10/ and M1-d-r9/ are not authored by this verifier; this verifier added the M1-d-r11 directory.",
        "Reference-match rules do not apply to this slice (no reference capture).",
    ],
    "summary": "",
}
n = len(fragment["rows"])
pass_n = sum(r["status"] == "PASS" for r in fragment["rows"])
fail_n = sum(r["status"] == "FAIL" for r in fragment["rows"])
fragment["summary"] = (
    f"M1-d round 11 at 91946cf: {n} rows, {pass_n} PASS, {fail_n} FAIL. FAIL rows: proj-grader-mutation-suite and "
    "proj-mutant-r11d03-annuity-tiny-cutoff (the tiny-rate annuity cutoff survives; the suite lacks the closed-form check at a rate near 1e-10), "
    "proj-grader-wrong-type-rate-valueerror (the tests demand ValueError for string and None rates, which project.html does not name; a TypeError witness fails 37 tests). "
    f"Mutants: {len(fragment['mutants'])} (81 killed, 1 survived: r11d_03; the 78 earlier mutants all killed, and of the four new mutants three are killed and r11d_03 survives)."
)
out = CHECKOUT / "ledgers" / "M1" / "M1-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, n, pass_n, fail_n, len(fragment["mutants"]))
