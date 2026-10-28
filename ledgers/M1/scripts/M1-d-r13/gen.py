import json, re, pathlib, subprocess
CK = pathlib.Path("/tmp/verify13-M1-d")
prev = json.load(open("/tmp/fanout-frags/M1-d.round12.json"))
prev_rows = {r["id"]: r for r in prev["rows"]}
OUT = "ledgers/M1/scripts/M1-d-r13/out/mutate_r13_final.out"
CARRY = "Carried from round 12 ({files} byte-identical since the previous pin): "
# lines of the mutate output
mut = []
for line in (CK / OUT).read_text().splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if m:
        status, fname, desc, killer = m.groups()
        mut.append({"id": fname.split("_")[0] if False else fname[:-3],
                    "file": f"ledgers/M1/mutants/{fname}", "description": desc,
                    "killed_by": killer, "run": f"tools/mutate_graders.py --unit M1 --seeds 0-9 (round 13, checkout eaf6d87): {status}"})
assert len(mut) == 109, len(mut)
assert all(m["killed_by"] for m in mut)
ALL_KILLED = all(m["run"].endswith("KILLED") for m in mut)

def carry(rid, files):
    r = dict(prev_rows[rid])
    r["evidence"] = CARRY.format(files=files) + r["evidence"]
    return r

def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    return d

PAGE = "course/modules/M/M1/project.html"
TEST = "course/modules/M/M1/grader/test_project.py"
rows = []
R = rows.append

# ---- rows re-run or re-derived this round
R(row("proj-spec-65-checks", "The page's check count equals the collected grader test count",
      f"{PAGE} line 164 ('which runs 196 checks'); {TEST}", "PASS",
      "Re-run on eaf6d87: `pytest --collect-only -q` in a workspace of test_project.py, instance.py and reference.py (as annuity_engine.py) printed '196 tests collected'; the same workspace with -q --assert=plain -W error printed '196 passed' (QF_SEED=0). Page says 196: matches."))
R(row("proj-spec-claims-mapped", "Every grading category named on line 164 is enforced by a test",
      f"{PAGE} line 164; {TEST} (test_annuity_factor_matches_direct_summation l.156, test_annuity_factor_matches_exact_closed_form l.165, test_schedule_matches_the_exact_schedule_row_for_row l.574, test_booleans_are_rejected_where_a_number_is_meant l.761, test_functions_do_not_print_or_warn l.1012, the zero-rate tests l.213/424/658, the invariants by name)", "PASS",
      "Re-read line 164 (changed: 196 checks; 'a second instance, which a fixed answer for the first would also have to match'). Each category maps to a named test (listed in location; 100 test functions, 196 collected cases). Re-run 196 passed under -W error. The second-instance claim holds: INST2 is used at test_project.py l.86, l.588 and l.1054-1055, so a fixed answer for seed 0 is checked against the second loan as well."))
R(row("proj-tie-rule-enforced", "The page's cent rule (a tie goes up) is enforced by the grader",
      f"{PAGE} line 170 (the cent rule); {TEST} test_schedule_interest_tie_goes_up (l.496), test_level_payment_tie_at_a_non_zero_rate_goes_up (l.484), parametrized exact tie tests (l.516-540)", "PASS",
      "Re-run 196 passed. Recomputed the two new tie cases with Fraction: 462554000 x 0.027/12 = 1040746.5 (exact, goes up to 1040747) and 804509400 x 0.23/12 = 15419763.5 (exact, goes up to 15419764): both expected values are the rounded-up exact values. Rule enforced by the exact-arithmetic tests; the float-separation claims are the defect in proj-grader-tie-comment-digits."))
R(row("proj-grader-tie-comment-digits", "The grader comments and docstring on the two new exact-tie cases state the arithmetic they test",
      f"{TEST} l.516-528: comment 'the float product is 15419763.49' (l.522) and the docstring sentence 'Floating point multiplication lands just below the tie and would round down' (test_schedule_interest_tie_is_exact_not_floating_point, l.531-535)", "FAIL",
      "Recomputed in Python 3.14 float: case 1 (462554000, 0.027): opening*(0.027/12) = 1040746.4999999999 (below the tie, so the comment's claim holds for this order); case 2 (804509400, 0.23): opening*(0.23/12) = 15419763.500000002 and opening*0.23/12 = 15419763.5, so the float product is NOT 15419763.49 and does not land below the tie. The float mutant (floor(opening*i+0.5), as in ledgers/M1/mutants/r12v_03) returns 15419764 for case 2, equal to the expected value: case 2 does not separate float from exact arithmetic. The docstring's claim that float 'would round down' is therefore false for the second case. Grader is untouched by this verifier.",
      fix="Correct the comment at l.522 to the computed float value (15419763.500000002 for opening*(i), 15419763.5 for opening*rate/12), and either drop the 'would round down' sentence for case 2 or replace case 2 with a principal and rate for which opening*(rate/12) falls below the tie (search with ledgers/M1/scripts/M1-d-r12/float_witness.py style loop), then re-run tools/mutate_graders.py --unit M1 --seeds 0-9."))
R(row("proj-grader-collect-count", "Collected grader test count and the page's stated count agree",
      f"{TEST}; {PAGE} line 164", "PASS", "Re-run: '196 tests collected' (see proj-spec-65-checks). The count rose by 4 from 192 on aebdc15: test_annuity_factor_at_a_rate_of_5e_11 (+1), test_schedule_interest_tie_is_exact (+2 parametrized cases), test_level_payment_rejects_invalid_loans with math.nan (+1)."))
R(row("proj-invalid-input-claim", "Non-finite rates are refused, as the page says",
      f"{PAGE} line 162 and line 178; {TEST} test_level_payment_rejects_invalid_loans (the list now includes (1000, math.nan, 12), l.884)", "PASS",
      "Re-run 196 passed: the nan case raises ValueError under -W error. Page line 162 ('including a non-finite number') is enforced for nan as well as inf (the inf case was already in the list)."))
R(row("proj-invalid-input-any-other-value", "Booleans and floats where whole numbers are meant are refused",
      f"{PAGE} line 162; {TEST} test_booleans_are_rejected_where_a_number_is_meant (l.761) and the invalid-loan list (l.880-890)", "PASS",
      "Re-run 196 passed with -W error on seeds 0-49 through tools/run_graders.py --unit M1 --seeds 0-49 (reference 50/50). Mutants r13f_06 (bool months accepted) and m16/m17/m18/m20/m21 are killed (out/mutate_r13_final.out)."))
R(row("proj-grader-new-boundary-tests-r11", "Boundary tests added in round 11 still hold",
      f"{TEST} lines 810-898 (includes the nan line at l.884)", "PASS", "Re-run 196 passed; the block contains the new nan case, which passes (raises ValueError)."))
R(row("proj-grader-count-type-enforced-r12", "Invalid loan inputs for schedules are refused with the named exception type",
      f"{TEST} test_schedule_rejects_invalid_loans and test_level_payment_rejects_invalid_loans", "PASS", "Re-run 196 passed (reference) and every committed mutant of the type family (r12v_02 binary rate, r13f_06 bool months, r12d_05/06 integer zero rates) killed. Witness witness_r12v_e (TypeError for month counts) still fails 10/10 seeds: the grader requires ValueError, as the page's conventions (line 178) say."))
R(row("proj-grader-mutation-suite", "The grader kills every committed student-error mutant",
      "ledgers/M1/mutants/ (109 files); tools/mutate_graders.py --unit M1 --seeds 0-9 (ledgers/M1/scripts/M1-d-r13/out/mutate_r13_final.out)", "PASS",
      f"Observed: 'mutate_graders M1: PASS (109/109 killed)', exit 0. Survivor from the previous round (r12v_01) and r12v_03 are now KILLED. The equivalent mutant I wrote this round (r13v_04, annuity cutoff 1e-12) survives the suite; it is moved out of the mutants directory to ledgers/M1/scripts/M1-d-r13/equiv/ with a proof row (proj-r13-equiv-r13v04-cutoff-1e-12). All 109 files are listed in this fragment's mutants field."))
R(row("proj-mutant-r12v01-annuity-cutoff-1e-10", "Round-12 mutant r12v_01 (annuity cutoff 1e-10) is killed",
      "ledgers/M1/mutants/r12v_01_annuity_cutoff_1e-10_treated_as_zero.py; " + TEST + " test_annuity_factor_at_a_rate_of_5e_11_is_not_taken_as_zero (l.236)", "PASS",
      "KILLED by test_annuity_factor_at_a_rate_of_5e_11_is_not_taken_as_zero (seed 0 and all seeds 0-9). Recomputed: at rate 5e-11, 100000 periods, zero rate gives 100000 vs exact 99999.7499979, relative error 2.50003e-6 > 1e-6."))
R(row("proj-mutant-r12v03-float-schedule-interest", "Round-12 mutant r12v_03 (schedule interest in floating point) is killed",
      "ledgers/M1/mutants/r12v_03_schedule_interest_rounded_in_float.py; " + TEST + " test_schedule_interest_tie_is_exact_not_floating_point[tie-at-2.7-percent] (l.516-540)", "PASS",
      "KILLED by test_schedule_interest_tie_is_exact_not_floating_point[tie-at-2.7-percent] (seed 0). Recomputed: 462554000 x (0.027/12) = 1040746.4999999999 in float, floor(+0.5) = 1040746; exact = 1040747. The second case does not kill it (see proj-grader-tie-comment-digits)."))
R(row("proj-r12-mutant-count", "The committed mutant directory holds the files this fragment lists",
      "ledgers/M1/mutants/ (109 files: m01 to m58, r10_01 to r10_10, r11_01 to r11_10, r11d_01 to r11d_04, r12d_01 to r12d_10, r12v_01 to r12v_04, r13f_01 to r13f_10, r13v_01 to r13v_03)", "PASS",
      "ls ledgers/M1/mutants | wc -l = 109 (this round). Previous fragment: 96 files. Added since: r13f_01 to r13f_10 (committed in the delta aebdc15..eaf6d87, not in the round-12 run) and r13v_01 to r13v_03 (this round). r13v_04 moved out as an equivalent mutant."))
R(row("proj-r13-mutants-new-student-errors", "Three new student-error mutants written by this verifier are killed",
      "ledgers/M1/mutants/r13v_01_monthly_rate_rounded_to_six_places.py, r13v_02_last_month_interest_truncated.py, r13v_03_level_payment_tiny_rate_cutoff_1e-9.py; generator ledgers/M1/scripts/M1-d-r13/mk_r13v.py", "PASS",
      "r13v_01 (level payment uses i rounded to 6 dp): KILLED by test_level_payment_matches_exact_nearest_cent (seed 0). r13v_02 (final month interest floored): KILLED by test_level_payment_and_schedule_accept_a_term_of_1200_months (seed 0). r13v_03 (monthly rate below 1e-9 taken as zero in level payment): KILLED by test_level_payment_below_the_old_cutoffs_is_exact (seed 0). Each mutant is a complete module derived from grader/reference.py with one line changed (assert count == 1 in mk_r13v.py)."))
R(row("proj-r13-equiv-r13v04-cutoff-1e-12", "Equivalent mutant: annuity factor treats a rate below 1e-12 as zero (not a mutant of the suite)",
      "ledgers/M1/scripts/M1-d-r13/equiv/r13v_04_annuity_tiny_rate_cutoff_1e-12.py; " + TEST + " close() l.126-127 and the tolerance sentence in test_annuity_factor_at_a_tiny_rate_is_not_taken_as_zero (l.219-224)", "PASS",
      "Survives the suite. Computed in 80-digit decimal: rate 1e-12, 100000 periods, exact 99999.99499995017, zero-rate value 100000, relative error 5.00005e-8, below the grader's stated tolerance of 1e-6 (close(), l.127). The mutant is therefore within the stated tolerance for the periods the suite uses; it is not a violation of any sentence on the page. Honest gap: the cutoff would exceed 1e-6 only from about 2,000,000 periods (relative error 1.00000e-6 at n = 2000000), a range the suite and the page do not state; recorded, not failed."))
R(row("proj-r13-final-payment-bound-docstring", "Docstring of the final-payment bound test states a derivable bound",
      f"{TEST} test_final_payment_is_within_the_stated_bound (docstring l.639-641)", "PASS",
      "Derived: with exact balance B and schedule opening O, D_k = O_k - B_k obeys D_1 = 0, D_{k+1} = (1+i) D_k + e_k with |e_k| <= 1/2. So |D_n| <= (1/2)((1+i)^n - 1)/i <= (n/2)(1+i)^n, and the final payment differs from the exact payment by at most |(1+i)D_n| + 1/2 + 1/2 (the last term is the rounding of the level payment) <= (n/2)(1+i)^n + 1 <= n(1+i)^n + 1. The stated bound holds, and 'not a tighter one' is accurate. Re-run: the test passes on the reference (196 passed)."))
R(row("proj-r13-inst2-comment", "Second-instance comment matches its use",
      f"{TEST} l.40 and uses at l.86, l.588, l.1054-1055", "PASS", "INST2 feeds exact_rows (l.86), the schedule row-for-row check (l.588) and the level payment check (l.1054). The comment 'a fixed answer for one seed must also match a second loan' describes that use. Re-run 196 passed."))
R(row("proj-r13-5e11-test-numbers", "Numbers in the 5e-11 test docstring",
      f"{TEST} test_annuity_factor_at_a_rate_of_5e_11_is_not_taken_as_zero (l.236-245)", "PASS",
      "Recomputed in 80-digit decimal: exact factor 99999.74999791668 (docstring: 99,999.7499979), zero-rate value 100000, relative error 2.5000271e-6 (docstring: 2.5e-6), float closed form 99999.75827179596 with relative error 8.27e-8 from the exact value (docstring: 8.3e-8). All match."))
R(row("proj-r13-tie-test-1-numbers", "Numbers in the 2.7% tie case",
      f"{TEST} parametrized case tie-at-2.7-percent (l.518-520)", "PASS",
      "Recomputed with Fraction: 462554000 x 0.027 / 12 = 2081493/2 = 1040746.5 exactly; the tie goes up to 1040747 (expected value). Float with the monthly rate first gives 1040746.4999999999 as the comment says."))
R(row("proj-r13-nan-invalid", "NaN rate refused with ValueError", f"{TEST} l.884", "PASS",
      "Included in the 196-case run; passes under -W error on seeds 0-9 (run_graders reference and the seed loop)."))
R(row("proj-r13-alternatives-new", "Three new correct implementations pass the suite",
      "ledgers/M1/scripts/M1-d-r13/alts/alt_r13_a_direct_sum_annuity.py (direct summation up to 200000 periods), alt_r13_b_expm1_cutoff_1e-14.py (expm1/log1p closed form, zero cutoff 1e-14), alt_r13_c_reciprocal_power_annuity.py (v = 1/(1+r), (1 - v^n)/r)", "PASS",
      "run_alts13.sh on seeds 0-9 (QF_SEED 0..9, -W error, 196 cases): alt a 10/10 pass, alt b 10/10 pass, alt c 10/10 pass. Each is a complete annuity_engine.py derived from reference.py with only annuity_factor replaced. These differ in numerical cutoff, algorithm, and summation order; none is over-constrained by the suite."))
R(row("proj-r13-alternatives-r12-rerun", "Round-12 alternatives still pass the grown suite",
      "ledgers/M1/scripts/M1-d-r12/alts/alt_r12v_a_expm1_closed_form.py, alt_r12v_b_decimal_half_up_money.py, alt_r12v_c_horner_annuity.py", "PASS",
      "run_alts13.sh on seeds 0-9: all three 10/10 pass with 196 cases each. Negative witnesses: witness_r12v_d_type_error_for_rate_types passes 10/10 (correct: a TypeError for rate types is not a required behaviour beyond ValueError examples); witness_r12v_e_type_error_for_month_type fails 10/10 (correct: counts must be ValueError)."))
R(row("proj-grader-alternatives", "Alternative correct implementations pass the grader across rounds",
      "ledgers/M1/scripts/M1-d-r13/alts/; ledgers/M1/scripts/M1-d-r12/alts/; ledgers/M1/scripts/M1-d-r11/alts/; ledgers/M1/scripts/M1-d-r10/", "PASS",
      "Re-run this round: 6 correct alternatives (3 new, 3 from r12) pass 10/10 seeds each; reference passes 10/10. Earlier rounds' correct alternatives were not re-run here beyond the cited rows."))
R(row("proj-r13-run-graders-0-49", "Reference passes the grader on seeds 0-49", "course/modules/M/M1/grader/reference.py; tools/run_graders.py --unit M1 --seeds 0-49", "PASS",
      "Observed: 'run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s)'."))
R(row("proj-r13-labs-run", "Lab run and project lab twins", "tools/run_labs.py --unit M1; tests/labs/M1/lab-M1-project-1.py, lab-M1-project-2.py, lab-M1-project-3.py", "PASS",
      "run_labs M1: PASS (11/11). Each twin run as `python -I -W error <twin>` exits 0 (outputs 7, 3 and 17 lines). The lab files are unchanged since aebdc15 (no diff under tests/labs/M1)."))
R(row("proj-r13-gates", "Repo gates for the M1 slice", "tools/check_pages.py --unit M1; tools/check_projects.py --unit M1; tools/check_dag.py --unit M1; tools/page_smoke.py --unit M1 --pages project.html", "PASS",
      "check_pages M1: PASS; check_projects M1: PASS; check_dag M1: PASS; page_smoke M1 (project.html): PASS (ledgers/M1/scripts/M1-d-r13/out/page_smoke.out). The Pyodide timing was not read beyond page_smoke's PASS."))
R(row("proj-r13-ruff-mypy", "Lint and type checks on the changed grader file",
      "course/modules/M/M1/grader/test_project.py; mypy files list in pyproject.toml (tools, tests)", "PASS",
      "ruff check course/modules/M/M1/grader: All checks passed; ruff format --check on the grader and tests/labs/M1: 15 files already formatted. Repo mypy --no-incremental: 'Success: no issues found in 153 source files' (mypy files = tools, tests; the grader is not in the configured list, so its strict typing is not gated; running mypy on the grader alone reports import-not-found for annuity_engine and instance, a path artifact)."))
R(row("proj-r13-registry", "Citation registry for the M1 page",
      "tools/verify_refs.py --unit M1 (live); tools/verify_refs.py --offline", "PASS",
      "Live: 'live re-verification of M1: 1 of 560 entries, 0 problems'. Offline: 'offline integrity: 560 entries, 0 problems'. The page's cites are unchanged since aebdc15 (the delta touches only line 164 of project.html)."))
R(row("proj-r13-mutant-run-observed", "Mutation run exit status and count", "tools/mutate_graders.py --unit M1 --seeds 0-9", "PASS",
      "Observed exit 0 and 'mutate_graders M1: PASS (109/109 killed)' (out/mutate_r13_final.out). Earlier run before moving r13v_04 out gave 109/110 with r13v_04 surviving (kept as ledgers/M1/scripts/M1-d-r13/out/mutate_r13c.out)."))
R(row("proj-r13-links-anchors", "Links in the changed line resolve", f"{PAGE} line 164 href targets #rubric, #self-assessment, #conventions", "PASS",
      "Each target id occurs once in project.html (id=\"rubric\", id=\"self-assessment\", id=\"conventions\")."))
R(row("proj-r13-banned-words-line-164", "The changed line has no banned phrase or process word", f"{PAGE} line 164", "PASS",
      "grep for roughly, about, historically, process, builder, verifier, round, unit report on line 164: no match."))
R(row("proj-r13-spec-second-instance-prose", "The page's grading sentence is accurate about the second instance", f"{PAGE} line 164", "PASS",
      "Line 164 says the grader's integrity comes 'from a second instance, which a fixed answer for the first would also have to match' (verified by INST2 use, proj-r13-inst2-comment)."))
R(row("proj-r13-ladder-and-numbers-carried-check", "Lab numbers on the page still match the unchanged labs", f"{PAGE} lines 55-149, 217-307", "PASS",
      "Carried from round 12 (course/modules/M/M1/project.html lines 55-149 and 217-307, and tests/labs/M1 byte-identical since the previous pin): the lab twins run this round (proj-r13-labs-run) and the outputs are unchanged."))

# ---- carried rows
carry_map = {
 "proj-spec-names-and-conventions": f"{PAGE} lines 160-162",
 "proj-grader-messages-no-leak": f"{TEST} lines 1-12 (module docstring)",
 "proj-grader-browser-and-local": f"{PAGE} lines 202-210",
 "proj-lab-interpretations-no-overreach": f"{PAGE} lines 103, 148, 306",
 "proj-l04-cited-numbers": f"{PAGE} (no L04 figure)",
 "proj-ladder-rungs": f"{PAGE} lines 40-49",
 "proj-atlas-studio-data": f"{PAGE} (no atlas or studio data)",
 "proj-links-anchors": f"{PAGE} href targets other than line 164",
 "proj-cite-velleman": f"{PAGE} lines 501-504",
 "proj-cite-velleman-registry-r12": "tools/verify_refs.py (references unchanged; re-run as proj-r13-registry)",
 "proj-banned-phrase-about": f"{PAGE} lines 332, 388, 457",
 "proj-section-references": f"{PAGE} sections 'The brief' and 'The rubric'",
 "proj-factor-tolerance-claim": f"{PAGE} line 445",
 "proj-tie-interest-docstring": f"{TEST} test_schedule_interest_tie_goes_up docstring (l.496-500)",
 "proj-grader-tiny-rate-docstring-numbers-r12": f"{TEST} test_annuity_factor_at_a_tiny_rate_is_not_taken_as_zero docstring (l.219-224)",
 "proj-grader-tiny-rate-test-arithmetic": f"{TEST} test_level_payment_below_the_old_cutoffs_is_exact",
 "proj-grader-minus-one-docstring-arithmetic": f"{TEST} test_annuity_accepts_a_rate_just_above_minus_one",
 "proj-grader-perpetuity-rate-test": f"{TEST} test_perpetuity_factor_accepts_a_rate_of_one_or_more",
 "proj-grader-over-constraint-unnamed": f"{TEST} test_annuity_factor_at_a_tiny_rate_is_not_taken_as_zero",
 "proj-grader-instance-docstring-growth": "course/modules/M/M1/grader/instance.py docstring",
 "proj-grader-instances": "course/modules/M/M1/grader/instance.py",
 "proj-grader-stdlib-and-purity": f"{TEST} imports (l.15-34)",
 "proj-closed-forms-float-test": f"{TEST} test_closed_forms_return_floats (l.189)",
 "proj-grader-wrong-type-rate-valueerror": f"{TEST} must_refuse (l.99-124)",
 "proj-must-raise-scope-r12": f"{TEST} must_raise docstring (l.89-93)",
 "proj-must-refuse-docstring-r12": f"{TEST} must_refuse docstring (l.100-110)",
 "proj-spec-65-prose-r12": f"{PAGE} line 162",
 "proj-grader-1200-month-test-r11": f"{TEST} test_level_payment_and_schedule_accepts_a_term_of_1200_months",
 "proj-grader-run-graders-r11": "tools/run_graders.py --unit M1 --seeds 0-49 (historical, r11)",
 "proj-grader-run-graders-r10": "tools/run_graders.py --unit M1 --seeds 0-49 (historical, r10)",
 "proj-grader-reference-50-seeds": "course/modules/M/M1/grader/reference.py",
 "proj-alt-correct-implementations-r10": "ledgers/M1/scripts/M1-d-r10/",
 "proj-alt-correct-implementations-r11": "ledgers/M1/scripts/M1-d-r11/alts/",
 "proj-rubric-shape": f"{PAGE} lines 325-336",
 "proj-rubric-descriptor-observable": f"{PAGE} lines 329-333",
 "proj-calibration-blind": f"{PAGE} lines 338-487",
 "proj-exemplar-length-and-summary": f"{PAGE} lines 411 and body 412-487",
 "proj-exemplar-intro-claim": f"{PAGE} line 339",
 "proj-exemplar-B-setup-claim": f"{PAGE} line 422",
 "proj-exemplar-A-numbers": f"{PAGE} lines 341-404",
 "proj-exemplar-B-level4-claims": f"{PAGE} lines 407, 411, 445-456",
 "proj-exemplar-B-closed-forms-and-schedule": f"{PAGE} lines 431-456",
 "proj-numbers-recomputed": f"{PAGE} lines 55-104, 106-149, 217-307",
 "proj-hours": f"{PAGE} lines 182-198",
 "proj-lab1-run": f"{PAGE} lines 55-104; tests/labs/M1/lab-M1-project-1.py",
 "proj-lab2-completion": f"{PAGE} lines 106-149; tests/labs/M1/lab-M1-project-2.py",
 "proj-lab3-reference": f"{PAGE} lines 217-307; tests/labs/M1/lab-M1-project-3.py",
 "cards-L01": "course/modules/M/M1/cards.json (sha 5c3311f8 identical at both pins) and lesson L01",
 "cards-L02": "course/modules/M/M1/cards.json and lesson L02",
 "cards-L03": "course/modules/M/M1/cards.json and lesson L03",
 "cards-L04": "course/modules/M/M1/cards.json and lesson L04",
 "cards-L05": "course/modules/M/M1/cards.json and lesson L05",
 "cards-L06": "course/modules/M/M1/cards.json and lesson L06",
 "cards-L07": "course/modules/M/M1/cards.json and lesson L07",
 "cards-L08": "course/modules/M/M1/cards.json and lesson L08",
 "cards-numbers-recomputed": "course/modules/M/M1/cards.json",
 "cards-duplicate-scan": "course/modules/M/M1/cards.json",
}
done_ids = {r["id"] for r in rows}
for rid, files in carry_map.items():
    assert rid in prev_rows, rid
    if rid in done_ids:
        continue
    r = dict(prev_rows[rid]); r["evidence"] = CARRY.format(files=files) + r["evidence"]
    rows.append(r)
    done_ids.add(rid)
missing = [i for i in prev_rows if i not in done_ids]
print("previous ids not yet placed:", missing)
