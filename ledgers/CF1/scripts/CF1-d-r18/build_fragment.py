"""Build ledgers/CF1/CF1-d.json (round 18, slice CF1-d) from the round-17 fragment and this round's evidence.

Rows whose cited subject is byte-identical since fefbf8b are carried with a 'Carried from round 17' prefix; rows whose
subject changed are re-verified (new evidence) or replaced by FAIL rows. Every round-17 row id is kept.
"""

import json
import re
import sys
from pathlib import Path

CHECKOUT = Path(sys.argv[1])
OUT_DIR = CHECKOUT / "ledgers/CF1/scripts/CF1-d-r18/out"
prev = json.loads(Path("/tmp/fanout-frags/CF1-d.round17.json").read_text(encoding="utf-8"))

CARRY = (
    "Carried from round 17 (cited subject byte-identical since the previous pin fefbf8b; the round-18 edits are "
    "project.html lines 186, 192 and 213, grader/test_project.py lines 403-420 and 610-665, cards.json CF1-c096 and "
    "CF1-c104, L01.html line 443, L05.html line 225 and L06.html line 106; the line numbers of grader tests after "
    "line 405 moved, the test bodies did not): "
)

# Round-18 evidence for rows whose subject changed. Status FAIL rows carry a fix.
REVERIFIED = {
    "proj-test-count-72": (
        "Re-verified round 18: course/modules/CF/CF1/project.html line 192 now reads 'collects 143 checks'; "
        "'pytest --collect-only -q' on the reference workspace printed '143 tests collected' (run_graders workspace "
        "for grader/reference.py, QF_SEED=0). Output: ledgers/CF1/scripts/CF1-d-r18/out/run_graders.out."
    ),
    "proj-collect-count-50-seeds": (
        "Re-verified round 18: collect-only on the reference workspace printed 143 for seeds 0, 1, 7, 23 and 49 "
        "(QF_SEED varied, PYTHONHASHSEED=0), so the count does not depend on the seed. Page line 192 says 143."
    ),
    "proj-spec-count-118-hub": (
        "Re-verified round 18: project.html line 192 says 143 (the round-17 wording 118 and 138 is gone), and the "
        "collect-only count on the reference is 143 (proj-test-count-72)."
    ),
    "proj-count-cause-wording": (
        "Re-verified round 18: line 192 says the count is 'counted with pytest --collect-only on the reference "
        "solution; the count does not depend on the seed, because no parametrize list's length depends on the seed'. "
        "Collect on seeds 0, 1, 7, 23, 49 gives 143 each time, consistent with the sentence."
    ),
    "r13-collect-count-126": (
        "Superseded and re-checked round 18: the round-13 count of 126 is no longer on the page. The current line 192 "
        "says 143 and collect-only gives 143 (proj-test-count-72)."
    ),
    "r15-page-count-138": (
        "Superseded and re-checked round 18: the round-15 page count 138 is no longer on the page (line 192 says 143, "
        "collect-only gives 143). Historical rows are kept for traceability."
    ),
    "r16-collect-count-138": (
        "Superseded and re-checked round 18: the round-16 collect count 138 was correct for its grader; the round-18 "
        "grader adds five tests (three zero/tax alone tests, the payback 1e-9 case, the inflation -1-1e-9 case; file "
        "grader/test_project.py) and collects 143 (proj-test-count-72)."
    ),
    "proj-named-errors-untested": (
        "Re-verified round 18 for the claims it names: the named-error paragraph (project.html line 213) lists the "
        "errors; each named error that the paragraph claims for NPV, payback, Fisher and Monte Carlo has a test, "
        "except the non-finite-rate clause, which is FAIL row proj-named-errors-nonfinite-rate-untested."
    ),
    "proj-npv-empty-overconstraint": (
        "Re-verified round 18: project.html line 213 'an NPV over an empty list of flows' and grader/test_project.py "
        "test_npv_rejects_empty_flows (must_raise on npv(0.1, [])) are unchanged; the reference raises (run_graders "
        "PASS 50/50 seeds)."
    ),
    "proj-named-errors-tax-share-one": (
        "Re-verified round 18: project.html line 213 'a tax rate below 0 or at or above 1, or a working-capital share "
        "below 0 or at or above 1 (1.0 is refused for each, and 0 is valid)'; grader parametrize ids tax-one and "
        "share-one still present in test_invalid_project_raises_a_named_error; the new zero-alone tests check 0 is valid."
    ),
    "proj-error-message-unenforced": (
        "Re-verified round 18: project.html lines 190 and 213; grader must_raise (lines 53-59) checks the exception "
        "type only, and the page says 'The autograder checks the exception type for each of them; the wording of a "
        "message is not graded'. The non-finite-rate clause is tracked in proj-named-errors-nonfinite-rate-untested."
    ),
    "proj-capex-float-overconstraint": (
        "Re-verified round 18: project.html line 188 (capex) and line 213 'a capex that is not a positive integer number "
        "of cents, so a float such as 1000.0, a boolean or a text is refused'; grader test_invalid_project_raises_a_"
        "named_error[capex-float] and capex-bool, capex-text unchanged (grader lines 616-630 region)."
    ),
    "r13-rate-minus-one-named-errors": (
        "Re-verified round 18: the rate ≤ -1 clauses (NPV, discounted payback, Monte Carlo, Fisher) are tested by "
        "test_npv_rejects_rates_at_or_below_minus_one, test_payback_rejects_a_discount_rate_at_or_below_minus_one, "
        "test_monte_carlo_refuses_a_rate_at_or_below_minus_one and test_fisher_rejects_rates_at_or_below_minus_one; "
        "the non-finite clause is not (proj-named-errors-nonfinite-rate-untested)."
    ),
    "r13-new-invalid-input-params": (
        "Re-verified round 18: test_invalid_project_raises_a_named_error parametrize ids unchanged (capex-negative and "
        "the others); the round-18 edit adds only the inflation-just-below-minus-one id, which is a valid named error."
    ),
    "cards-changed-c071-lesson-agreement": (
        "Re-verified round 18: cards.json CF1-c071 (Section 4 states no finding on firm use) still agrees with L05.html "
        "section 4, whose intro changed (line 225) only to 'Payback has four defects. The first three follow from its "
        "definitions...'; the card's claim is not about the count of defects. CF1-c084 agrees with the rewritten "
        "L06.html Remark 2.4 (line 106): not proved, cited or graded; a reading aid. CF1-c065 unchanged (L05 line 86)."
    ),
    "cards-changed-c071-c084": (
        "Re-verified round 18: cards.json CF1-c071 and CF1-c084 against L05.html section 4 (line 225 changed, section "
        "text unchanged) and L06.html Remark 2.4 (line 106 changed). CF1-c084 back 'it is used only as a reading aid' "
        "agrees with the new remark, whose two exercises E1 and E2 apply the normal reading (L06 lines 309-327)."
    ),
    "cards-grade-semantics": (
        "FAIL round 18: cards.json CF1-c096 changed from grade C to grade T with basis 'Definition 1.1'. BLUEPRINT.md "
        "line 156-157 defines T as 'Theorem: proved on the page', and L05.html line 111 calls the same rule 'The payback "
        "convention is linear interpolation inside the year...'. A definition is a convention, so the card is over-graded "
        "(FAIL row cards-c096-grade-t-on-convention). Other changed cards: CF1-c104 C with a convention basis is correct; "
        "T cards with proof bases are unchanged."
    ),
    "cards-changed-r17-c056-c096": (
        "FAIL round 18: CF1-c056 unchanged (lab-derived, grade C) and still agrees with L04.html line 300. CF1-c096 back "
        "matches L05.html Definition 1.1 formula (line 59: PB = (τS−1) + (−CUM_{τS−1})/C_{τS}), but its grade changed "
        "from C to T, which is the defect of row cards-c096-grade-t-on-convention."
    ),
    "cards-c104-duplicates-c029": (
        "Re-verified round 18: CF1-c104 is now 'Does interest on the loan that funds a project enter its incremental cash "
        "flows?' (financing), and CF1-c029 is depreciation (non-cash, tax shield). No restatement. c104 back matches "
        "L02.html line 83 (third rule: financing stays out of the flows; interest and dividends pay providers of capital; "
        "counting interest counts the cost of capital twice). Grade C, basis 'convention, Section 1 (third rule)'."
    ),
    "proj-mutants-killed": (
        "FAIL round 18: 'mutate_graders.py --unit CF1 --seeds 0-9' on the 157 mutants in ledgers/CF1/mutants/ printed "
        "'mutate_graders CF1: FAIL (155/157 killed)'. The two survivors are d18_m01 (payback accepts a nan rate) and "
        "d18_m02 (Fisher accepts a nan inflation); see proj-mutants-round18-new. Output: ledgers/CF1/scripts/CF1-d-r18/out/"
        "mutate_r18_final.out."
    ),
    "proj-banned-phrases": (
        "Re-verified round 18: scan of course/modules/CF/CF1/project.html and cards.json for 'roughly half', 'about 6%', "
        "'historically', an ellipsis, 'process', 'build', 'builder', 'round ', 'verifier', 'unit report' found no hits "
        "(the only case-insensitive matches were 'request' and 'list[float]'). Scan in the round-18 log."
    ),
    "proj-process-words-r10": (
        "Re-verified round 18: the process-word scan over project.html and cards.json (build, builder, round, verifier, "
        "REQUEST, unit report) found no hits in the changed sentences (lines 186, 192, 213; c096, c104)."
    ),
    "r16-banned-process-words-scan": (
        "Re-verified round 18: cards.json scan for process words and banned phrases after the c096 and c104 edits: no hits "
        "(the 'I ' hits were a case-insensitive match inside other words)."
    ),
    "cards-duplicate-scan": (
        "Re-verified round 18: 109 cards, 109 unique ids; a pairwise difflib scan of fronts and backs (threshold 0.6) "
        "listed the pairs CF1-c042/c103 (same question at 3 and 5 per cent inflation, different numbers), c049/c091, "
        "c053/c107, c028/c089, c017/c090, c081/c082, c056/c107, c053/c056, c051/c106, c068/c102. The pairs were printed and read: "
        "c042/c103 ask the same question at 3 and 5 per cent inflation with different stated numbers; c049/c091 are the two parts of one problem; "
        "c017/c090 and c053/c107 and c056/c107 and c051/c106 ask different facts; c028/c089 and c081/c082 and c068/c102 are different lab or convention questions. "
        "No card restates another; CF1-c104 is not in the list."
    ),
    "cards-missing-grade-or-basis": (
        "Re-verified round 18: every one of the 109 cards has a grade (C or T) and a basis."
    ),
    "cards-count-vs-plan": (
        "Re-verified round 18: cards.json has 109 entries (plans/CF1-build-plan.md line 240 unchanged since fefbf8b)."
    ),
    "cards-numbers-in-lesson": (
        CARRY + "the cards whose numbers are cited (no number is on c096 or c104)."
    ),
    "lesson-l06-rewrites": (
        "FAIL round 18 for the round-18 Remark 2.4 sentence (see lesson-l06-remark-2-4-each-result-conditional). The cited "
        "L06 lines 129, 138 and 147 are byte-identical since fefbf8b; the E2 solution arithmetic 0.0552 ± 1.96 × 0.0010 "
        "= 0.05324 to 0.05716 (printed as 0.0532 to 0.0572) was recomputed."
    ),
    "index-card-and-hub-wording": (
        CARRY + "index.html lines 135-138; line 142 (L05 card body) changed to 'what payback ignores after its payback "
        "year', which agrees with L05 Proposition 2.1 and the four-bullet section 4."
    ),
    "r13-hub-l05-card-title-stale": (
        CARRY + "index.html line 142 title 'Payback and Its Discounted Form' unchanged; body changed to 'after its payback "
        "year' and re-read against L05 section 4 bullets 1 and 3 (ignores flows after its year)."
    ),
    "proj-mutants-round17-new": (
        CARRY + "the round-17 mutants r17_01..r17_04 are unchanged; they are killed in the round-18 run (155/157 "
        "overall)."
    ),
    "cmd-mutate-graders-r17": (
        "Historical command row, carried from round 17 (its output file ledgers/CF1/scripts/CF1-d-r17/out/mutate_r17.out "
        "is unchanged): 139/139 killed at that time. The round-18 command is cmd-mutate-graders-r18."
    ),
    "lesson-l01-conventional-rewrites": (
        "Re-verified round 18 for the round-18 edit at L01.html line 443 (R3 solution): see lesson-l01-r3-solution-r18. "
        "The cited lines 7, 51, 111, 174-175, 338, 371, 407 are byte-identical since fefbf8b."
    ),
    "lesson-l05-rewrites": (
        CARRY + "L05.html lines 107 and 117 (cited lines); line 225 (section 4 intro) changed and is checked in "
        "cards-changed-c071-lesson-agreement."
    ),
    "proj-mutants-round12-new": (
        CARRY + "r12d_01..r12d_05 are unchanged."
    ),
}

FAILS = [
    {
        "id": "proj-named-errors-nonfinite-rate-untested",
        "check": "1.4 / 2.9: every named error the page states is enforced by a test (BLUEPRINT grader rule; architect ruling a)",
        "location": "course/modules/CF/CF1/project.html line 213 (Named errors: 'a rate that is not finite (nan or infinity), or at or below −1, in an NPV, a discounted payback, a Fisher conversion or a Monte Carlo request'); course/modules/CF/CF1/grader/test_project.py lines 112 (nan/inf only for npv) and absence of nan/inf cases for payback_period, fisher_nominal and npv_monte_carlo",
        "status": "FAIL",
        "evidence": (
            "The round-18 page claims ValueError for a non-finite rate in a discounted payback, a Fisher conversion and a Monte Carlo request. "
            "grep for float('nan') and float('inf') in test_project.py finds rate cases only at line 112, which parametrises npv_rejects_rates_at_or_below_minus_one. "
            "The reference raises for these (reference.py lines 26-28 _check_rate, called by payback_period line 148, fisher_nominal lines 164-165, npv_monte_carlo line 177), so the reference passes. "
            "But the suite does not enforce the claim: mutant d18_m01 (payback_period accepts nan: guard is rate <= -1 only) SURVIVED all 10 seeds, and mutant d18_m02 (fisher_nominal accepts inflation nan: guard is inflation <= -1 only) SURVIVED all 10 seeds. "
            "Run: ledgers/CF1/scripts/CF1-d-r18/out/mutate_r18_final.out (SURVIVED lines). "
            "Mutant d18_m03 (Monte Carlo with an inline NPV and no guard on the rate) was judged equivalent and archived: npv() inside npv_monte_carlo still raises, see proj-equivalent-d18-m03."
        ),
        "fix": (
            "Either add tests to grader/test_project.py that must_raise on payback_period(flows, nan), payback_period(flows, inf), fisher_nominal(nan, 0.02), fisher_nominal(0.02, nan), fisher_nominal(0.02, inf) and npv_monte_carlo(PROJECT, nan, 3, SEED, 0.1), "
            "or narrow the page sentence to the rates the suite tests (NPV, and the -1 and below rates in discounted payback, Fisher and Monte Carlo). The reference passes any such test, so the fix is in the suite or the page, not in reference.py."
        ),
    },
    {
        "id": "proj-inputs-missing-space-inflation",
        "check": "2.9 prose: the rewritten Inputs sentence renders correctly",
        "location": "course/modules/CF/CF1/project.html line 186 (Inputs): '...nwc_share: the working-capital share (defined in the conventions below), at least 0 and below 1.<code>inflation</code>: above −1.'",
        "status": "FAIL",
        "evidence": (
            "grep of line 186 shows '1.<code>inflation</code>' with no space after the full stop, so the rendered page reads 'below 1.inflation: above −1.' The sentence was rewritten in round 18 (its 'nwc_share' part is new). "
            "Other sentences of the Inputs paragraph are unchanged since fefbf8b."
        ),
        "fix": "Insert a space after the full stop: '...at least 0 and below 1. <code>inflation</code>: above −1.' in course/modules/CF/CF1/project.html line 186.",
    },
    {
        "id": "cards-c096-grade-t-on-convention",
        "check": "cards: grade semantics (BLUEPRINT section 3 table: T = theorem proved on the page; BUILDER_RULES; cards agree with current lesson text)",
        "location": "course/modules/CF/CF1/cards.json CF1-c096 (grade 'T', basis 'Definition 1.1'); course/modules/CF/CF1/L05.html line 111 ('The payback convention is linear interpolation inside the year...') and lines 57-59 (Definition 1.1)",
        "status": "FAIL",
        "evidence": (
            "The round-17 card CF1-c096 had grade C and basis 'convention, Section 1 (interpolation)'. In round 18 it was changed to grade T with basis 'Definition 1.1' (git diff fefbf8b..7143726, cards.json lines 770-776). "
            "BLUEPRINT.md lines 156-157: T means 'Theorem: proved on the page, or with a precisely cited proof'. Definition 1.1 is a definition, not a proved theorem, and L05.html line 111 calls the same rule 'the payback convention'. "
            "The card's back text matches Definition 1.1 (L05 line 59: PB = (τS−1) + (−CUM_{τS−1})/C_{τS}), so the content is right and only the grade is over-stated."
        ),
        "fix": "Set CF1-c096 back to grade 'C' with basis 'convention, Definition 1.1 (linear interpolation, L05 section 1)', as the lesson labels it, or label the card's answer as a definition rather than a theorem.",
    },
    {
        "id": "lesson-l06-remark-2-4-each-result-conditional",
        "check": "2.9 / 2.4: scope of a rewritten sentence (scope words 'each', 'only') against the exercises it describes",
        "location": "course/modules/CF/CF1/L06.html line 106 (Remark 2.4: 'the two exercises that apply it (E1 and E2) label each result as conditional on that reading'); E1 solution (L06 lines 313-315)",
        "status": "FAIL",
        "evidence": (
            "E1's solution gives three results: the error 84543.40 − 79078.68 = 5464.72 cents (recomputed: 5464.72), the number of standard errors 5464.72/4400.22 = 1.2419 (recomputed: 1.24192), and 'well inside three standard errors'. Only the last, the two-sided probability 2(1 − Φ(1.2419)) = 0.2143 (recomputed: 0.21427), is labelled 'under that reading'. "
            "So the claim that E1 labels each result as conditional on the normal reading is over-stated: the cents error and the standard-error count do not depend on normality. E2 is correct: its band 0.0532 to 0.0572 uses the 1.96 normal multiplier and the solution says so."
        ),
        "fix": "Change Remark 2.4 to say the exercises E1 and E2 label the normal-based probability and band as conditional on that reading (the cents error and the standard-error count need no normal reading).",
    },
    {
        "id": "proj-mutants-round18-new",
        "check": "2.5 / mutation (BLUEPRINT grader rule; VERIFIER_RULES 2.6): every student-error mutant of the grader is killed",
        "location": "ledgers/CF1/mutants/d18_m01_payback_nan_rate_accepted.py, d18_m02_fisher_nan_inflation_accepted.py, d18_m04_fisher_inflation_never_checked.py (round-18 mutants written by this verifier); d18_m03 archived in ledgers/CF1/scripts/CF1-d-r18/ (equivalent)",
        "status": "FAIL",
        "evidence": (
            "Three new student-error mutants written from grader/reference.py (make_mutants.py). d18_m04 (Fisher never checks inflation) KILLED by test_fisher_rejects_rates_at_or_below_minus_one[inflation-minus-one] (seed 0). "
            "d18_m01 (payback with rate guard rate <= -1 only, nan accepted) SURVIVED seeds 0-9. d18_m02 (Fisher with inflation guard inflation <= -1 only, nan accepted) SURVIVED seeds 0-9. "
            "The page states the behaviour these mutants violate (project.html line 213), so both survivors are FAIL. Output: ledgers/CF1/scripts/CF1-d-r18/out/mutate_d18_new.out."
        ),
        "fix": "Add the nan/inf cases named in proj-named-errors-nonfinite-rate-untested (for payback_period and fisher_nominal) to grader/test_project.py; then the two survivors are killed. Keep the mutants.",
    },
    {
        "id": "cmd-mutate-graders-r18",
        "check": "2.5 command: tools/mutate_graders.py --unit CF1 --seeds 0-9 (all mutants in ledgers/CF1/mutants/)",
        "location": "ledgers/CF1/mutants/*.py (157 files); ledgers/CF1/scripts/CF1-d-r18/out/mutate_r18_final.out",
        "status": "FAIL",
        "evidence": "Observed last line: 'mutate_graders CF1: FAIL (155/157 killed)'. SURVIVED: d18_m01_payback_nan_rate_accepted.py and d18_m02_fisher_nan_inflation_accepted.py. The 154 earlier mutants (r18_01..r18_11 included) and d18_m04 are KILLED.",
        "fix": "See proj-named-errors-nonfinite-rate-untested: add the nan/inf tests so both survivors are killed.",
    },
]

PASSES = [
    {
        "id": "proj-new-grader-tests-r18",
        "check": "2.5 / 2.9: the round-18 grader additions match the page's named-error and valid-input rules (architect ruling b: no over-constraint)",
        "location": "course/modules/CF/CF1/grader/test_project.py lines 406-410 ([1e-9, 10.0] payback case, id positive-first-just-above-zero), 616-621 (inflation -1-1e-9), and the three zero-alone tests (test_zero_revenue_alone_is_valid, test_zero_cash_costs_alone_are_valid, test_tax_rate_of_zero_alone_is_valid); project.html lines 186, 213",
        "status": "PASS",
        "evidence": (
            "The page says a first flow that is not negative is refused (line 213), so +1e-9 is refused; it says inflation is above -1 (line 186), so -1-1e-9 is refused; it says zero is valid in both lists and tax rate 0 is valid (lines 186, 213), so the zero-alone tests are right. "
            "run_graders PASS 50/50 seeds on the reference; the three alternative engines alt_d18_1..3 PASS 50/50 seeds (alts_all_r18.out). Mutants r18_03 (tax 0 refused) and r18_10/r18_11 KILLED by the new tests (mutate_r18_final.out)."
        ),
    },
    {
        "id": "proj-equivalent-d18-m03",
        "check": "2.5 mutation: equivalent-mutant proof for a Monte Carlo mutant with no rate guard of its own",
        "location": "ledgers/CF1/scripts/CF1-d-r18/make_mutants.py (m03 text); /tmp/CF1-v/d18/equiv/m03_check.py (run); reference.py lines 88-93 (npv guard)",
        "status": "PASS",
        "evidence": (
            "The mutant replaces the npv_monte_carlo guard with rate <= -1 only. Calling it with rate nan (python -I) raised 'ValueError: rate must be a finite number above -1: a rate of -1 or less makes discount factors undefined', because npv() called once per draw runs _check_rate(rate) (reference.py line 90). "
            "So every observable behaviour equals the reference and the mutant is equivalent. It is archived in the scratch directory and is not in the mutants list."
        ),
    },
    {
        "id": "proj-alternatives-round18-new",
        "check": "2.5 alternatives (architect ruling b; brief procedure: at least three genuinely different correct implementations)",
        "location": "ledgers/CF1/scripts/CF1-d-r18/alts/alt_d18_1_running_discount_factor_fsum.py, alt_d18_2_tighter_bisection_and_multiplied_discount.py, alt_d18_3_inverted_rate_guard.py (made by make_alts.py from grader/reference.py)",
        "status": "PASS",
        "evidence": (
            "alt_d18_1: npv by a running discount factor and math.fsum; alt_d18_2: payback with (1+rate)**(-t) and bisection stopping at 1e-13 relative; alt_d18_3: rate guard written as 'not (rate > -1) or not isfinite'. "
            "Each runs the whole suite on seeds 0-49 with PASS (alts_all_r18.out: PASSED_ALL_SEEDS). The contract numbers (4001 grid points, window 1e-4..1e4, 1e-7 root precision) are kept."
        ),
    },
    {
        "id": "proj-alternatives-rerun-all-prior-r18",
        "check": "2.5 alternatives re-run: every earlier grader alternative in ledgers/CF1/scripts/*/alts against the round-18 suite",
        "location": "ledgers/CF1/scripts/CF1-d-r7..r16 alts directories (alt_r7..alt_r16, 49 files) and ledgers/CF1/scripts/CF1-d-r15/alts/ref_reference.py; outputs ledgers/CF1/scripts/CF1-d-r18/out/alts_all_r18.out and alts_r9_r18.out",
        "status": "PASS",
        "evidence": (
            "49 earlier alternative engine files PASSED_ALL_SEEDS on seeds 0-49 with the round-18 test_project.py, and ref_reference.py too (the new tests are satisfied by all of them; alts_all_r18.out and alts_r9_r18.out). "
            "Excluded: alt_r17_a_tolerance_1e9.py, alt_r17_b_horner_npv.py, alt_r17_c_shield_from_difference_tolerance_1e4.py under ledgers/CF1/scripts/CF1-a-r17/alts/: these are slice-a lab-level alternatives (their output is the Lab 2 sunk-study line), not capbudget engines, so collection fails with 'ERROR test_project.py'. They do not count as grader alternatives and are the CF1-a slice's concern."
        ),
    },
    {
        "id": "proj-lab-twins-isolated-r18",
        "check": "2.5 labs: the project-page twins run alone under python -I -W error",
        "location": "tests/labs/CF1/lab-CF1-project-1.py, lab-CF1-project-2.py, lab-CF1-project-3.py; ledgers/CF1/scripts/CF1-d-r18/out/project_labs_isolated.out",
        "status": "PASS",
        "evidence": "Each twin exits 0 under 'python -I -W error' (project_labs_isolated.out). tests/labs/CF1 is byte-identical to fefbf8b.",
    },
    {
        "id": "cmd-gates-r18",
        "check": "2.5 command gates: check_projects, check_pages, check_dag, run_labs, run_graders (seeds 0-49), page_smoke (project), verify_refs (offline and live), ruff, mypy",
        "location": "ledgers/CF1/scripts/CF1-d-r18/out/*.out",
        "status": "PASS",
        "evidence": (
            "check_projects --all: 'check_projects CF1: PASS' (and AP1). check_pages --unit CF1: 'check_pages CF1: PASS'. check_dag --all: PASS (CF1 and AP1). run_labs --unit CF1: 'PASS (9/9)'. "
            "run_graders --unit CF1 --seeds 0-49: 'PASS (reference 50/50 seeds, slowest 0.3 s)'. page_smoke --unit CF1 --pages project.html: 'page_smoke CF1: PASS'. "
            "verify_refs --offline: 'offline integrity: 560 entries, 0 problems'. verify_refs --unit CF1 (live): '2 of 560 entries, 0 problems'. "
            "ruff check and ruff format --check on grader and tests/labs/CF1: 'All checks passed!' and '13 files already formatted'. mypy --no-incremental on the grader and labs: 'Success: no issues found in 13 source files'."
        ),
    },
    {
        "id": "cards-c104-financing-convention",
        "check": "cards: CF1-c104 back agrees with L02 Section 1 (third rule); grade C is a convention",
        "location": "course/modules/CF/CF1/cards.json CF1-c104; course/modules/CF/CF1/L02.html line 83 (Section 1, third rule)",
        "status": "PASS",
        "evidence": "L02.html line 83: 'The third rule is also a convention: financing stays out of the flows. Interest and dividends are payments to the providers of capital, and the rate in Lesson 1 already charges for that capital, so counting interest as a project flow counts the cost of capital twice.' The card back restates it; basis 'convention, Section 1 (third rule)' and grade C match the lesson's own word 'convention'.",
    },
    {
        "id": "lesson-l01-r3-solution-r18",
        "check": "2.4 arithmetic and scope of the rewritten R3 solution (L01.html line 443)",
        "location": "course/modules/CF/CF1/L01.html line 443 (R3 solution)",
        "status": "PASS",
        "evidence": "Recomputed: 1.05/1.06 - 1 = -0.009434 (page -0.0094, -0.009434...), 1.05/1.03 - 1 = +0.019417 (page +0.0194, +0.019417...). The new sentence 'The problem does not say which of the two rates the owner faces, so each is computed' is accurate for R3 as stated.",
    },
    {
        "id": "lesson-l05-section4-intro-r18",
        "check": "2.9 prose: rewritten section-4 intro of L05 ('Payback has four defects...') against its four bullets",
        "location": "course/modules/CF/CF1/L05.html line 225",
        "status": "PASS",
        "evidence": "Bullets: (1) ignores flows after its year (Proposition 2.1, a definitional result); (2) simple rule ignores time value (from the definition); (3) discounted rule still ignores later flows (Proposition 2.2); (4) the cut-off is a choice (from the decision rule). The sentence 'The first three follow from its definitions. The fourth follows from the cut-off that a decision rule attaches to it' is accurate: (3) uses the definitions with Proposition 2.2 proved in Section 2.",
    },
    {
        "id": "proj-page-round18-count-sentence",
        "check": "2.9 prose: the round-18 count and the Required outputs / Grading mode claims (project.html lines 186, 192)",
        "location": "course/modules/CF/CF1/project.html lines 186, 192",
        "status": "PASS",
        "evidence": "'collects 143 checks' matches collect-only 143 (seeds 0, 1, 7, 23, 49). the phrase '(defined in the conventions below)' for nwc_share matches the Working capital convention bullet (nwc_t = nwc_share × revenue_t). Only the 1.inflation typo (proj-inputs-missing-space-inflation) fails.",
    },
    {
        "id": "index-ladder-rung1-worked-example-r18",
        "check": "index: the ladder rung-1 line is unchanged; the edited paragraph above it is re-read",
        "location": "course/modules/CF/CF1/index.html line 151 (rung 1)",
        "status": "PASS",
        "evidence": "Line 151 (rung 1 'Worked example') is byte-identical to fefbf8b; the edited paragraph above it ('You may skip them when you reach the placement bar and answer both skill checks') agrees with the placement rule on line 68.",
    },
]

rows = []
seen = set()
for r in prev["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in REVERIFIED:
        new = dict(r)
        new["evidence"] = REVERIFIED[rid]
        if rid in ("cards-grade-semantics", "cards-changed-r17-c056-c096", "proj-mutants-killed", "lesson-l06-rewrites"):
            new["status"] = "FAIL"
            new["fix"] = (
                "See the FAIL row of the same defect in this fragment (cards-c096-grade-t-on-convention, "
                "lesson-l06-remark-2-4-each-result-conditional, proj-named-errors-nonfinite-rate-untested)."
                if rid != "proj-mutants-killed"
                else "See proj-mutants-round18-new and cmd-mutate-graders-r18."
            )
        elif rid in ("cards-changed-r17-c056-c096",):
            pass
        else:
            new["status"] = "PASS"
            new.pop("fix", None)
        rows.append(new)
        continue
    new = dict(r)
    if r["status"] == "FAIL" and rid == "cards-c104-duplicates-c029":
        new["status"] = "PASS"
        new["evidence"] = REVERIFIED[rid]
        new.pop("fix", None)
    elif r["status"] == "PASS":
        new["evidence"] = CARRY + (r["evidence"] if r["evidence"] else "")
    else:
        new["evidence"] = CARRY + r["evidence"]
    rows.append(new)

for f in FAILS + PASSES:
    if f["id"] in seen:
        raise SystemExit(f"id collision {f['id']}")
    rows.append(f)

# Mutants: parse the final mutate_graders run (every mutant file of ledgers/CF1/mutants/*.py).
mut = []
for line in (OUT_DIR / "mutate_r18_final.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    entry = {"file": f"ledgers/CF1/mutants/{name}", "description": desc}
    entry["killed_by"] = None if killed == "None" else killed
    mut.append(entry)

frag = {
    "unit": "CF1",
    "slice": "CF1-d",
    "round": 18,
    "verifier": "independent verifier (Haiku), round 18 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json; project slice needs mutants)",
    "pin": "7143726 (detached, /tmp/verify18-CF1-d)",
    "base": "fefbf8b (round-17 pin); delta computed with git diff fefbf8b 7143726 and every hunk in this slice read",
    "checkout": "/tmp/verify18-CF1-d",
    "scratch": "/tmp/CF1-v/d18",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mut,
    "registry_flags": prev["registry_flags"],
    "freshness_flags": [],
    "notes": (
        "Round-18 delta for this slice (fefbf8b..7143726): course/modules/CF/CF1/project.html (lines 186, 192, 213), "
        "grader/test_project.py (payback first flow 1e-9 case; inflation -1-1e-9 case; three zero-alone tests), "
        "cards.json (CF1-c096 grade C to T; CF1-c104 replaced: depreciation restatement removed, financing card added), "
        "L01.html line 443, L05.html line 225, L06.html line 106, index.html lines 142 and 150-152, and ledgers/CF1/mutants/r18_01..r18_11 "
        "(already present; killed). tests/labs/CF1/* and the grader reference are unchanged. Scripts: ledgers/CF1/scripts/CF1-d-r18/ "
        "(make_alts.py, make_mutants.py, run_new.py, build_fragment.py); outputs in ledgers/CF1/scripts/CF1-d-r18/out/. "
        "New mutants written by this verifier: ledgers/CF1/mutants/d18_m01, d18_m02, d18_m04 (d18_m03 archived as equivalent). "
        "Not checked: svelte/browser page_smoke only for the project page; the BLUEPRINT grade table was read but not every card was re-graded against the full lesson text; "
        "hours were not re-estimated (architect ruling: hours are design targets)."
    ),
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
frag["summary"] = (
    f"CF1-d round 18 (pin 7143726): {len(rows)} rows, {n_pass} PASS, {n_fail} FAIL. "
    f"FAIL: proj-named-errors-nonfinite-rate-untested (nan/inf rate claim untested for payback, Fisher, Monte Carlo; mutants d18_m01/m02 survive), "
    f"proj-inputs-missing-space-inflation (typo), cards-c096-grade-t-on-convention (definition graded T), "
    f"lesson-l06-remark-2-4-each-result-conditional (scope overstated). "
    f"Mutants: {len(mut)} run, {sum(1 for m in mut if m['killed_by'])} killed, 2 survivors. Alternatives: 3 new and 49 earlier engines pass 50/50 seeds."
)

target = CHECKOUT / "ledgers/CF1/CF1-d.json"
target.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", n_pass, "fail", n_fail, "mutants", len(mut))
