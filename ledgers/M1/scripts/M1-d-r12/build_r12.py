import json, re
CK = "/tmp/verify12-M1-d"
prev = json.load(open("/tmp/fanout-frags/M1-d.round11.json", encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
MUT = open(CK + "/ledgers/M1/scripts/M1-d-r12/out/mutate_all_r12.out", encoding="utf-8").read().splitlines()
kill = {}
for line in MUT:
    m = re.match(r"(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if m:
        kill[m.group(2)] = (m.group(1), m.group(3), m.group(4))

def carry(rid, files, location=None):
    old = prev_rows[rid]
    assert old["status"] == "PASS", rid
    return {"id": rid, "check": old["check"], "location": location or old["location"], "status": "PASS",
            "evidence": f"Carried from round 11 ({files}): " + old["evidence"]}

def new(rid, check, location, evidence, status="PASS", fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    return row

def mut_ev(prefix):
    hits = sorted(k for k in kill if k.startswith(prefix))
    assert hits, prefix
    return "; ".join(f"{k} {kill[k][0]} by {kill[k][2]}" for k in hits)

CARD_FILES = "course/modules/M/M1/cards.json and the unit's lesson HTML byte-identical since 91946cf; git diff --name-only shows no M1 cards or lesson file"
rows = []
A = rows.append

# ---------- spec, page, links, prose
A(carry("proj-spec-names-and-conventions", "course/modules/M/M1/project.html lines 160 and 170 byte-identical; the only changed line since 91946cf is 164 (git diff -U0: one hunk, @@ -164 @@)"))
A(new("proj-spec-65-checks", "The page's check count equals the collected grader test count",
      "course/modules/M/M1/project.html line 164 ('which runs 192 checks'); grader/test_project.py",
      "Reference copy (test_project.py, instance.py, reference.py as annuity_engine.py): collect-only printed '192 tests collected'; the run with -q --assert=plain -W error printed '192 passed' (also in run_graders, out/gates1.out). Page says 192: matches."))
A(new("proj-spec-claims-mapped", "The sections named in the Grading mode line exist in the suite",
      "course/modules/M/M1/project.html line 164 (Grading mode); grader/test_project.py test_annuity_factor_matches_direct_summation (line 156), test_annuity_factor_matches_exact_closed_form (165), test_growing_partial_sum_identity (375), test_level_payment_zero_rate_is_the_loan_over_the_months (411), test_booleans_are_rejected_where_a_number_is_meant (726), test_functions_do_not_print_or_warn (976); EXACT and EXACT2 (lines 84-86)",
      "Each named category is present: closed forms against direct sums and exact rationals, finite identities, the schedule row for row against EXACT, invariants, zero-rate case, invalid inputs with booleans, and purity. The reference passes 192/192."))
A(carry("proj-grader-messages-no-leak", "course/modules/M/M1/grader/test_project.py line 12 docstring (diff hunks start at lines 24 and 86 at 91946cf)", "course/modules/M/M1/grader/test_project.py line 12 (docstring: never prints the expected value)"))
A(carry("proj-grader-browser-and-local", "course/modules/M/M1/project.html lines 202-210 byte-identical"))
A(carry("proj-lab-interpretations-no-overreach", "course/modules/M/M1/project.html lines 103, 148, 306 byte-identical"))
A(carry("proj-l04-cited-numbers", "course/modules/M/M1/project.html, no changed line in the L04 text"))
A(carry("proj-ladder-rungs", "course/modules/M/M1/project.html lines 40-49 byte-identical"))
A(carry("proj-atlas-studio-data", "course/modules/M/M1/project.html (only line 164 changed)"))
A(new("proj-links-anchors", "Every in-page link target exists",
      "course/modules/M/M1/project.html href='#...' targets",
      "Targets used: #brief, #conventions, #grader-section, #report, #rubric, #self-assessment, #spec, #stretch and the skip link #main. Each id= exists in the file (checked by a script over the file, out/ and the page). #ladder, #exemplars, #local, #reading and #references also exist."))
A(carry("proj-cite-velleman", "course/modules/M/M1/project.html lines 501-504 byte-identical"))
A(new("proj-cite-velleman-registry-r12", "Registry integrity and live re-verification of the M1 citations",
      "tools/verify_refs.py --offline (out/vr_offline.out); tools/verify_refs.py --unit M1 (out/vr_live_M1.out)",
      "Offline: '560 entries, 0 problems', exit 0. Live, --unit M1: '1 of 560 entries, 0 problems', exit 0. The page's reading block (lines 499-506) says no passage locator is confirmed and attributes no statement to the source; the appendix proofs (Exemplar B, lines 468-478) cite no page of it."))
A(carry("proj-banned-phrase-about", "course/modules/M/M1/project.html lines 332, 388, 457 byte-identical"))
A(carry("proj-section-references", "course/modules/M/M1/project.html sections 'The brief' (line 309) and 'The rubric' (line 323) byte-identical"))
A(carry("proj-factor-tolerance-claim", "course/modules/M/M1/project.html line 445 byte-identical; grader close() and test_annuity_factor_zero_rate_is_the_number_of_periods unchanged (close is not in the changed-function list)"))
A(new("proj-invalid-input-claim", "Line 178's claim that each named invalid input raises ValueError is enforced",
      "course/modules/M/M1/project.html line 178; grader/test_project.py test_annuity_factor_rejects_the_wrong_types (292), test_perpetuity_rejects_non_finite_and_wrong_type_rates (696), test_growing_perpetuity_rejects_wrong_types (770), test_level_payment_rejects_invalid_loans (830), test_schedule_rejects_invalid_loans (870)",
      "The named conditions (a principal that is not a whole number of cents of one or more, a rate that is negative or not finite, a term that is not a whole number of months of one or more) are tested with ValueError-only expectations, for example (0, 0.05, 12), (1000, -0.01, 12), (1000, 0.05, 0), (1000, 0.05, 12.5) and (1000, 0.05, 2.0) in the parametrized lists. Rates of a non-numeric type are not named on the page, and only those accept TypeError (proj-grader-wrong-type-rate-valueerror)."))
A(new("proj-invalid-input-any-other-value", "Booleans are rejected where a number is meant, with ValueError",
      "course/modules/M/M1/project.html line 162; grader/test_project.py test_booleans_are_rejected_where_a_number_is_meant (726) and its parametrized list above it",
      "Line 162 names 'a boolean where a number is meant' among the ValueError conditions. The boolean block is byte-identical and passes; booleans stay ValueError in the TypeError witness (witness_r12v_d), because it raises ValueError for bool before the TypeError branch."))
A(carry("proj-tie-interest-docstring", "grader/test_project.py test_schedule_interest_tie_goes_up docstring and body identical (now line 496)"))
A(carry("proj-tie-rule-enforced", "course/modules/M/M1/project.html line 170 byte-identical; tie tests test_level_payment_tie_goes_up (465) and test_schedule_interest_tie_goes_up (496) identical"))
A(carry("proj-grader-tie-comment-digits", "grader/test_project.py tie tests test_level_payment_tie_goes_up (465) and test_schedule_interest_tie_goes_up (496) identical"))
A(carry("proj-rubric-shape", "course/modules/M/M1/project.html lines 325-336 byte-identical"))
A(carry("proj-rubric-descriptor-observable", "course/modules/M/M1/project.html lines 329-333 byte-identical"))
A(carry("proj-calibration-blind", "course/modules/M/M1/project.html lines 338-487 byte-identical"))
A(carry("proj-exemplar-length-and-summary", "course/modules/M/M1/project.html Exemplar B summary (line 411) and body (lines 420-478) byte-identical"))
A(carry("proj-exemplar-intro-claim", "course/modules/M/M1/project.html line 339 byte-identical"))
A(carry("proj-exemplar-B-setup-claim", "course/modules/M/M1/project.html line 422 byte-identical"))
A(new("proj-exemplar-A-numbers", "Exemplar A's quoted figures are the rounded values of Lab 3's output",
      "course/modules/M/M1/project.html lines 341-404 (article exemplar-a); Lab 3 output lines 296 and the twin run in out/twins.out",
      "Level payment 166750 cents = $1,667.50, quoted as $1,668 (rounded to the dollar, half up): consistent. Total interest 20024880 cents = $200,248.80, quoted as $200,000 (rounded to the thousand): consistent. Annuity 179.910 quoted as 179.9 and perpetuity 20.000 as 20.00: consistent. The annotations at lines 352 and 376 say the dollar and thousand figures are not printed by Lab 3, which is correct."))
A(new("proj-exemplar-B-level4-claims", "Exemplar B's numbers and its C4 verdict",
      "course/modules/M/M1/project.html lines 407 (verdict), 411 (summary), 445-456 (schedule, limitations), 462 (C4 level-4 miss)",
      "Recomputed in exact rationals (ledgers/M1/scripts/M1-d-r12/recompute_lab3.py): level payment 166750, final payment 166630, gap -120 cents, final balance 0, bound n(1+i)^n + 1 = 923.12276, printed 923.1228, total interest 20024880. The summary's 'within the bound of 923.1228 cents' is correct. The C4 level-4 miss at line 462 says the direction of fees, taxes and prepayment is not stated; the limitations passage (lines 456-467) does not state it, so the annotation is accurate. The verdict is a rubric judgement and is not re-scored here."))
A(new("proj-exemplar-B-closed-forms-and-schedule", "Exemplar B's closed-form and schedule numbers",
      "course/modules/M/M1/project.html lines 431-456",
      "Recomputed (recompute_lab3.py): annuity 179.910321841 (quoted 179.9), due 180.584985548 (180.6), perpetuity 20.000000000 (20.00), growing 33.333333333 (33.33), 400-term sum 33.333026270 (33.33 to four significant digits), tail q^400/(r-g) = 3.0706e-4 (quoted 3.071e-4), least N = 345, error at 344 payments 1.02781e-6 (quoted 1.028e-6). Month 1: payment 166750, interest 112500, principal 54250. All match Lab 3's printed lines (out/twins.out)."))
A(new("proj-numbers-recomputed", "Every number in Labs 1 to 3 recomputed independently",
      "course/modules/M/M1/project.html lines 55-104 (Lab 1), 106-149 (Lab 2), 217-307 (Lab 3); ledgers/M1/scripts/M1-d-r12/recompute_lab3.py",
      "Exact-rational recomputation of Lab 3 agrees with the printed values (above). Lab 1 twin output (out/twins.out) gives 149888, final balance 0, total interest 28959337, and the month rows printed. Lab 2 gives recurrence and closed form 166.791614392 and balance 24692994 after 12 payments, as printed."))
A(new("proj-hours", "Time budget arithmetic and the declared total",
      "course/modules/M/M1/project.html lines 182-198 (Time budget); data-hours-project=30 at line 33",
      "Component hours recomputed: 2 + 3 + 8 + 7 + 6 + 4 = 30, equal to data-hours-project 30. The hub split (30 of 100) is the Total row. Hours not judged on pace (architect ruling)."))
A(new("proj-lab1-run", "Lab 1 twin runs under python -I -W error and matches the expected block",
      "course/modules/M/M1/project.html lines 55-104; tests/labs/M1/lab-M1-project-1.py (out/twins.out)",
      "Exit 0 in 0.01 s; output equals the expected block line for line (monthly rate 0.005000, annuity factor 166.791614, level payment 149888, months 1, 2, 360, final balance 0, total interest 28959337)."))
A(new("proj-lab2-completion", "Lab 2 completion: the two blanks give the printed values",
      "course/modules/M/M1/project.html lines 106-149; tests/labs/M1/lab-M1-project-2.py",
      "The twin's blanks are 'total = total + v**k' (line 16 of the twin) and 'balance = balance + interest - payment' (line 32), the expressions the page states. The twin prints recurrence 166.791614392, closed form 166.791614392, difference 4.2e-12 and balance 24692994, matching the expected block."))
A(new("proj-lab3-reference", "Lab 3 twin output equals the expected block",
      "course/modules/M/M1/project.html lines 217-307; tests/labs/M1/lab-M1-project-3.py (out/twins.out)",
      "Each printed line equals the expected block: level payment 166750, month 1 payment/interest/principal 166750/112500/54250, final 166630 minus level -120, final balance 0, bound 923.1228, within bound True, principal sum True, total interest 20024880, total paid 50024880, annuity 179.910321841, due 180.584985548, perpetuity 20.000000000, growing 33.333333333, direct sum 33.333026270, tail 3.071e-04, least N 345, error 1.0278e-06."))
A(new("proj-lab-twins-isolated-r12", "The three project lab twins run under python -I -W error",
      "tests/labs/M1/lab-M1-project-1.py, lab-M1-project-2.py, lab-M1-project-3.py (out/twins.out)",
      "Each exits 0 under -I -W error and prints the expected output (see the three rows above)."))
A(new("proj-page-smoke-r12", "The project page runs in the browser harness",
      "course/modules/M/M1/project.html; tools/page_smoke.py --unit M1 --pages project.html (out/page_smoke_project.out)",
      "'page_smoke M1: PASS', exit 0. The per-lab 10 s Pyodide timing was not read separately: not checked (see notes)."))
A(new("proj-commands-gate-r12", "Page, project, DAG, labs and grader gate commands",
      "tools/check_pages.py --unit M1; tools/check_projects.py --unit M1; tools/check_dag.py --all; tools/run_labs.py --unit M1; tools/run_graders.py --unit M1 --seeds 0-49 (out/gates1.out)",
      "check_pages M1: PASS. check_projects M1: PASS. check_dag: M1 PASS (AC1, AC2, AC4, CF1 and AP1 lines appear in the same output). run_labs M1: PASS (11/11). run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s)."))
A(new("proj-commands-gate-r11", "Round-11 gate commands re-run",
      "tools/check_pages.py --unit M1; tools/check_projects.py --unit M1; tools/check_dag.py --all; tools/run_labs.py --unit M1; tools/page_smoke.py --unit M1 --pages project.html",
      "All PASS in out/gates1.out and out/page_smoke_project.out (see proj-commands-gate-r12)."))
A(new("proj-commands-gate-r10", "Round-10 gate commands re-run",
      "tools/verify_refs.py --offline (out/vr_offline.out); the other round-10 commands as in proj-commands-gate-r12",
      "verify_refs offline: 560 entries, 0 problems, exit 0. The others PASS as above."))
A(new("proj-mypy-and-pytest-r12", "Type check and curriculum tests",
      ".venv/bin/mypy --no-incremental (out/mypy.out); .venv/bin/pytest -q tests/test_curriculum.py",
      "mypy: 'Success: no issues found in 153 source files', exit 0. pytest tests/test_curriculum.py: 15 passed. The full repo pytest was not run."))
A(new("proj-grader-lint-types", "Lint and type checks on the grader",
      "course/modules/M/M1/grader/ (test_project.py, reference.py, starter.py, instance.py); ruff check; ruff format --check; mypy (repo run)",
      "ruff check course/modules/M/M1/grader: All checks passed. ruff format --check on the grader: 4 files already formatted. ruff check . (repo): All checks passed. mypy --no-incremental: no issues in 153 files. I did not confirm the file list includes grader/, so the mypy evidence is the repo run."))
A(new("proj-grader-stdlib-and-purity", "Grader is standard library only, and the module is pure",
      "course/modules/M/M1/grader/test_project.py imports (lines 15-34; 'from decimal import Decimal, localcontext' is new at line 27); test_functions_do_not_print_or_warn (976, identical)",
      "decimal is standard library. The other imports are unchanged. The purity test is byte-identical and passes on the reference."))
A(carry("proj-grader-instances", "course/modules/M/M1/grader/instance.py byte-identical (absent from the 91946cf..aebdc15 diff)"))
A(carry("proj-grader-instance-docstring-growth", "course/modules/M/M1/grader/instance.py docstring byte-identical"))
A(new("proj-closed-forms-float-test", "Closed forms return floats",
      "course/modules/M/M1/grader/test_project.py test_closed_forms_return_floats (189, body identical)",
      "Passes on the reference and on every correct alternative below. The spec sentence 'The closed forms return floats' is in project.html conventions (line 170)."))

# ---------- over-constraint, alternatives, docstrings
A(new("proj-grader-alternatives", "Correct alternative implementations pass; wrong ones fail",
      "ledgers/M1/scripts/M1-d-r12/alts/; ledgers/M1/scripts/M1-d-r11/alts/; ledgers/M1/scripts/M1-d-r10/alt_r10_*.py; ledgers/M1/scripts/M1-d-r9/alts_r8/ (out/alts_r9_r10.out)",
      "Seeds 0-9 each. PASS (14): alt_r12v_a, alt_r12v_b, alt_r12v_c; alt_r11_a, alt_r11_b, alt_r11_c; alt_r10_direct_sum_closed_payment, alt_r10_expm1_log1p, alt_r10_fraction_sum, alt_r10_tie_explicit; alt_balance_closed_form_v6, alt_expm1_cutoff_v6, alt_fraction_sum_v6, alt_r9_cutoff_1e15. FAIL, as they should: alt_decimal_v6, alt_float_epsilon_v6, alt_fraction_binary_v6, alt_r9_decimal60 (each reads the rate or rounds in binary, failing test_level_payment_is_exact_in_the_rate_as_written[tie-at-six-percent] or [half-cent-at-tiny-rate]) and witness_int_zero."))
A(new("proj-alt-correct-implementations-r12", "Three new correct implementations pass the full suite",
      "ledgers/M1/scripts/M1-d-r12/alts/alt_r12v_a_expm1_closed_form.py, alt_r12v_b_decimal_half_up_money.py, alt_r12v_c_horner_annuity.py",
      "Each passes 192/192 on seeds 0-9. They differ from the reference in the closed form (expm1/log1p), in the cent rounding (Decimal quantize with ROUND_HALF_UP at 110 digits) and in the summation (backward Horner)."))
A(new("proj-alt-correct-implementations-r11", "Round-11 alternatives still pass",
      "ledgers/M1/scripts/M1-d-r11/alts/alt_r11_a_direct_sum_annuity.py, alt_r11_b_exact_form_without_inverse.py, alt_r11_c_integer_half_up.py",
      "Each passes 192/192 on seeds 0-9 (run_one.sh)."))
A(new("proj-alt-correct-implementations-r10", "Round-10 alternatives still pass",
      "ledgers/M1/scripts/M1-d-r10/alt_r10_direct_sum_closed_payment.py, alt_r10_expm1_log1p.py, alt_r10_fraction_sum.py, alt_r10_tie_explicit.py",
      "Each passes 192/192 on seeds 0-9 (out/alts_r9_r10.out)."))
A(new("proj-grader-over-constraint-unnamed", "No check demands behaviour the page does not state",
      "course/modules/M/M1/grader/test_project.py test_annuity_factor_at_a_tiny_rate_is_not_taken_as_zero (219), test_annuity_accepts_a_rate_just_above_minus_one (265), test_perpetuity_factor_accepts_a_rate_of_one_or_more (330), test_level_payment_below_the_old_cutoffs_is_exact (427)",
      "The fourteen correct alternatives pass each of these. The new tiny-rate test asks only that a rate of 5e-10 gives the closed form (every correct alternative is within 1e-6, the expm1 form within 1.5e-16 of the 80-digit value, the naive form within 8.3e-8). Page conventions: 'It requires r > -1' (annuity_factor, line 171). No alternative is refused by these tests."))
A(new("proj-grader-minus-one-docstring-arithmetic", "Arithmetic in the rate-just-above-minus-one test",
      "course/modules/M/M1/grader/test_project.py test_annuity_accepts_a_rate_just_above_minus_one (265)",
      "At r = -0.999: v = 1/(1+r) = 1000, so the sum of v^k for k = 1..3 is 1000 + 10^6 + 10^9 = 1001001000, the asserted value; the due factor is that times (1 + r) = 0.001, asserted as 1001001000 * (1 - 0.999). Recomputed by hand; the reference passes the test."))
A(new("proj-grader-tiny-rate-docstring-numbers-r12", "Numbers in the new tiny-rate test's docstring",
      "course/modules/M/M1/grader/test_project.py test_annuity_factor_at_a_tiny_rate_is_not_taken_as_zero (219-234)",
      "numcheck.py (run with -I): exact factor at 5e-10, n = 100000, is 99997.5000166674 (docstring 99,997.5); zero rule gives 100000, relative error 2.5000e-5 (docstring 2.5e-5); naive float closed form relative error 8.274e-8 (docstring 'about 8e-8'). All three match."))
A(new("proj-grader-tiny-rate-test-arithmetic", "The level-payment tiny-rate test's value recomputed",
      "course/modules/M/M1/grader/test_project.py test_level_payment_below_the_old_cutoffs_is_exact (427, body identical)",
      "Docstring: the loan over the months is 36,934.497 cents (13296419/360 = 36934.4972); the exact payment 13296419 x i / (1 - (1+i)^-360) with i = 5e-9/12 is 36934.50000000427 (numcheck-style Fraction computation, out/), above the half-cent line, so the nearest cent is 36935. Matches the assertion."))
A(carry("proj-grader-perpetuity-rate-test", "grader/test_project.py test_perpetuity_factor_accepts_a_rate_of_one_or_more (330) body identical"))
A(new("proj-grader-reference-50-seeds", "The reference passes the suite on seeds 0-49",
      "course/modules/M/M1/grader/reference.py; tools/run_graders.py --unit M1 --seeds 0-49 (out/gates1.out)",
      "'run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s)'."))
A(new("proj-grader-run-graders-r11", "run_graders at seeds 0-49 passes", "tools/run_graders.py --unit M1 --seeds 0-49", "run_graders M1: PASS (reference 50/50 seeds)."))
A(new("proj-grader-run-graders-r10", "run_graders at seeds 0-49 passes", "tools/run_graders.py --unit M1 --seeds 0-49", "run_graders M1: PASS (reference 50/50 seeds)."))
A(new("proj-grader-collect-count", "The collected count equals the page's count",
      "course/modules/M/M1/grader/test_project.py; course/modules/M/M1/project.html line 164",
      "collect-only: 192 tests; the run with -W error: 192 passed. The page says 192."))
A(new("proj-grader-1200-month-test-r11", "The 1200-month term test passes and kills the 480-month cap",
      "course/modules/M/M1/grader/test_project.py test_level_payment_and_schedule_accept_a_term_of_1200_months (451, body identical)",
      "The reference passes. Mutant m57 (480-month cap) is KILLED: " + mut_ev("m57_") + "."))
A(carry("proj-grader-new-boundary-tests-r11", "grader/test_project.py isolated boundary checks (the block from test_annuity_factor_refuses_rate_of_minus_one_even_with_zero_periods onward) byte-identical since 91946cf"))
A(new("proj-grader-wrong-type-rate-valueerror", "Wrong-type rates are not required to raise ValueError (the round-11 FAIL)",
      "course/modules/M/M1/grader/test_project.py must_refuse (99-124) and its callers test_annuity_factor_rejects_the_wrong_types (292), test_perpetuity_rejects_non_finite_and_wrong_type_rates (696), test_growing_perpetuity_rejects_wrong_types (770), test_level_payment_rejects_invalid_loans (830), test_schedule_rejects_invalid_loans (870); project.html line 178",
      "Round-11 FAIL: the tests demanded ValueError for string and None rates, which the page does not name. Fixed: must_refuse accepts TypeError only where the counts are numbers and a rate is not. Witness witness_r12v_d (TypeError for a non-numeric, non-bool rate; bools stay ValueError): 192/192 on seeds 0-9, so the wrong-type rate tests now accept a correct TypeError. The page's named conditions still need ValueError (proj-grader-count-type-enforced-r12)."))
A(new("proj-grader-count-type-enforced-r12", "Count types still need ValueError",
      "course/modules/M/M1/grader/test_project.py test_schedule_rejects_invalid_loans and test_level_payment_rejects_invalid_loans (cases with '12', None, 12.0, 12.5, 2.0); project.html line 178",
      "witness_r12v_e (TypeError for a month count that is not an int): fails 10/10 seeds, e.g. test_schedule_rejects_invalid_loans[1000-0.05-None], [1000-0.05-2.0], [1000-0.05-12.5]. The page: 'a term that is not a whole number of months of one or more ... raises ValueError' (line 178)."))
A(new("proj-must-raise-scope-r12", "must_raise is used only for named conditions, as its docstring says",
      "course/modules/M/M1/grader/test_project.py must_raise docstring (89-93) and its call sites (grep: 45 matches including the two definitions, lines 652-999)",
      "Each call passes a named condition (rates of -1 or below, NaN, infinite, zero or negative rates, ranges, floats where a whole number is meant, booleans, a principal of -1 cent, the purity invalid calls). None passes a string or None rate, so ValueError-only is correct for them. The witness passes all of them."))
A(new("proj-must-refuse-docstring-r12", "must_refuse's docstring states the rule the code applies",
      "course/modules/M/M1/grader/test_project.py must_refuse docstring (100-110) and the accepted tuple (111-115)",
      "The docstring says a string or None count must raise ValueError and a string or None rate may raise TypeError. The code accepts (ValueError, TypeError) only when the counts are numbers (bool counts as int) and no rate is numeric, otherwise (ValueError,). Read against the code the two agree. The one masking case, a boolean count with a string rate, is not in any parametrized list."))
A(new("proj-spec-65-prose-r12", "The Constraints line is still consistent with the grader after the wrong-type change",
      "course/modules/M/M1/project.html line 162 ('raises ValueError for the conditions the conventions below name')",
      "The conventions name a non-finite rate, a negative rate, a boolean, a float or string count and the ranges. A string or None rate is none of the named conditions, so a TypeError for it does not contradict line 162. Consistent."))

# ---------- mutants
A(new("proj-grader-mutation-suite", "The grader kills every committed student-error mutant",
      "ledgers/M1/mutants/ (96 files); tools/mutate_graders.py --unit M1 --seeds 0-9 (out/mutate_all_r12.out)",
      "'mutate_graders M1: FAIL (94/96 killed)'. Survivors: r12v_01_annuity_cutoff_1e-10_treated_as_zero.py and r12v_03_schedule_interest_rounded_in_float.py. The 92 earlier mutants (m01 to m58, r10_01 to r10_10, r11_01 to r11_10, r11d_01 to r11d_04, r12d_01 to r12d_10) and r12v_02 and r12v_04 are KILLED.",
      status="FAIL",
      fix="Close both survivors (rows proj-mutant-r12v01-annuity-cutoff-1e-10 and proj-mutant-r12v03-float-schedule-interest), then re-run tools/mutate_graders.py --unit M1 --seeds 0-9 and require 96 of 96."))
A(new("proj-mutant-m47-m49", "Mutants m47 to m49 are killed",
      "ledgers/M1/mutants/m47_schedule_omits_the_last_month.py, m48_small_rate_cutoff_loan_over_months.py, m49_interest_on_original_principal.py (out/mutate_all_r12.out)",
      mut_ev("m47_") + "; " + mut_ev("m48_") + "; " + mut_ev("m49_")))
A(new("proj-mutant-m48-small-rate-cutoff", "Mutant m48 is killed",
      "ledgers/M1/mutants/m48_small_rate_cutoff_loan_over_months.py", mut_ev("m48_")))
A(new("proj-mutant-m50-perpetuity-rate-above-one", "Mutant m50 is killed",
      "ledgers/M1/mutants/m50_perpetuity_rejects_rate_of_one_or_more.py", mut_ev("m50_")))
A(new("proj-mutant-m51-tiny-rate-cutoff-1e-8", "Mutant m51 is killed",
      "ledgers/M1/mutants/m51_tiny_rate_cutoff_1e-8_treated_as_zero.py", mut_ev("m51_")))
A(new("proj-mutant-m52-float-small-rate", "Mutant m52 is killed",
      "ledgers/M1/mutants/m52_float_closed_form_for_small_rates.py", mut_ev("m52_")))
A(new("proj-mutant-m53-term-cap-360", "Mutant m53 is killed",
      "ledgers/M1/mutants/m53_term_capped_at_360_months.py", mut_ev("m53_")))
A(new("proj-mutant-m57-term-cap-480", "Mutant m57 is killed",
      "ledgers/M1/mutants/m57_term_capped_at_480_months.py", mut_ev("m57_")))
A(new("proj-mutants-m54-m58-new", "Mutants m54 to m56 and m58 are killed",
      "ledgers/M1/mutants/m54_*, m55_*, m56_*, m58_* (out/mutate_all_r12.out)",
      mut_ev("m54_") + "; " + mut_ev("m55_") + "; " + mut_ev("m56_") + "; " + mut_ev("m58_")))
A(new("proj-mutants-r11d-new", "Mutants r11d_01, r11d_02 and r11d_04 are killed",
      "ledgers/M1/mutants/r11d_01_*, r11d_02_*, r11d_04_* (out/mutate_all_r12.out)",
      mut_ev("r11d_01") + "; " + mut_ev("r11d_02") + "; " + mut_ev("r11d_04")))
A(new("proj-mutant-r11d03-annuity-tiny-cutoff", "Round-11 survivor r11d_03 is now killed",
      "ledgers/M1/mutants/r11d_03_annuity_tiny_rate_treated_as_zero.py; grader/test_project.py test_annuity_factor_at_a_tiny_rate_is_not_taken_as_zero (219)",
      mut_ev("r11d_03") + ". The new test at rate 5e-10 separates the 1e-9 cutoff from the closed form."))
A(new("proj-mutant-r12v02-binary-rate", "New mutant r12v_02 (exact arithmetic on the binary value of the float rate) is killed",
      "ledgers/M1/mutants/r12v_02_annual_rate_read_as_binary_fraction.py; project.html line 170 ('computed in exact rational arithmetic on the annual rate as it is written as a decimal')",
      mut_ev("r12v_02")))
A(new("proj-mutant-r12v04-growing-no-upper-bound", "New mutant r12v_04 (growth at or above the rate not refused) is killed",
      "ledgers/M1/mutants/r12v_04_growing_perpetuity_missing_upper_bound.py", mut_ev("r12v_04")))
A(new("proj-mutant-r12v01-annuity-cutoff-1e-10", "New mutant r12v_01 (a rate below 1e-10 taken as zero in annuity_factor) survives",
      "ledgers/M1/mutants/r12v_01_annuity_cutoff_1e-10_treated_as_zero.py; project.html line 171 ('annuity_factor(rate, periods) is a = sum v^k ... a zero rate gives the number of periods'); grader/test_project.py test_annuity_factor_at_a_tiny_rate_is_not_taken_as_zero docstring (220)",
      "SURVIVED at seeds 0-9 (out/mutate_all_r12.out). Witness: annuity_factor(5e-11, 100000) returns 100000.0 in the mutant and 99999.75827 in the reference (80-digit value 99999.749998; the zero rule is 2.5e-6 relative, above the test's 1e-6). The suite's only tiny rate in annuity_factor is 5e-10 (above the mutant's cutoff). The page says 'a zero rate gives the number of periods' and the test docstring says 'A rate of 5e-10 is not zero, so the factor is the closed form at that rate, not the number of periods'. A rate of 5e-11 is not zero by either sentence, so the mutant violates a stated behaviour that no test covers (the round-11 r11d_03 class, one decade lower).",
      status="FAIL",
      fix="Add a test at rate 5e-11 with 100,000 periods, expected value from 80-digit decimal arithmetic, tolerance 1e-6 (the zero rule is 2.5e-6 off; the naive closed form 8.3e-8 off, numcheck.py). The reference passes it. Then re-run tools/mutate_graders.py --unit M1 --seeds 0-9."))
A(new("proj-mutant-r12v03-float-schedule-interest", "New mutant r12v_03 (schedule interest rounded in floating point) survives",
      "ledgers/M1/mutants/r12v_03_schedule_interest_rounded_in_float.py; project.html line 170 ('Each cent amount is the exact value of its formula, computed in exact rational arithmetic ... before it is rounded'); grader/test_project.py test_schedule_interest_tie_goes_up (496)",
      "SURVIVED at seeds 0-9. Witness (float_witness.py search): principal 462554000 cents, annual rate 0.027, 360 months. Exact first-month interest 462554000 x 0.00225 = 1040746.5, a tie that rounds up to 1040747 (reference: 1040747); the mutant prints 1040746. No test computes a schedule whose interest is an exact half cent in that way.",
      status="FAIL",
      fix="Add a schedule test with principal 462554000, annual rate 0.027, 360 months, first-row interest 1040747 expected from exact arithmetic (and a second case from float_witness.py, e.g. 804509400 at 0.23, interest 15419764). Then re-run tools/mutate_graders.py --unit M1 --seeds 0-9."))
A(new("proj-r12-mutant-count", "Mutant count and naming",
      "ledgers/M1/mutants/ (96 files: m01 to m58, r10_01 to r10_10, r11_01 to r11_10, r11d_01 to r11d_04, r12d_01 to r12d_10, r12v_01 to r12v_04)",
      "96 files. The r12d_* files were in commit aebdc15 before this round and are re-run; the four r12v_* files were written by this verifier (mk_r12v.py)."))

# ---------- cards
for lesson in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"]:
    A(carry(f"cards-{lesson}", CARD_FILES))
A(new("cards-numbers-recomputed", "Card counts per lesson and total",
      "course/modules/M/M1/cards.json (179 cards)",
      "Counts recomputed: L01 24, L02 26, L03 27, L04 16, L05 20, L06 12, L07 24, L08 30; total 179; 179 unique ids."))
A(new("cards-duplicate-scan", "Duplicate scan of card ids, fronts and answers",
      "course/modules/M/M1/cards.json",
      "No duplicate id; no duplicate front after normalisation. Two cards share the answer 'No (lemma 2.2).': M1-c030 ('Is there an integer t with 2t = 1?') and M1-c173 ('Can an integer be both even and odd?'). Different questions: not duplicates."))
A(new("cards-process-and-banned", "Process words and banned phrases in cards and the project page",
      "course/modules/M/M1/cards.json; course/modules/M/M1/project.html (line 164 changed)",
      "Regex scan for builder, build, round, verifier, REQUESTS, unit report: only the ordinary word 'rounded' matched (cards M1-c135, M1-c146; project.html lines 170, 339, 347, 352, 371, 376). Banned phrases ('roughly half', 'about 6%', 'historically', ellipsis) matched nothing in cards.json or project.html. Line 164 contains none."))

# ---------- completeness check against round 11
ids = [r["id"] for r in rows]
dups = sorted({i for i in ids if ids.count(i) > 1})
missing = sorted(set(prev_rows) - set(ids))
assert not dups, dups
assert not missing, missing
print("rows", len(rows), "non-pass", [r["id"] for r in rows if r["status"] != "PASS"], "new ids", sorted(set(ids) - set(prev_rows)))
json.dump(rows, open("/tmp/m1-v12/d/build/rows.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
