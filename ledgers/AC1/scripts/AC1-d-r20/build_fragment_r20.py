"""Build the round-20 AC1-d ledger fragment: carry round-19 PASS rows whose cited subject is unchanged, re-verify the rest."""

import json
import re
import sys
from pathlib import Path

CHK = Path("/tmp/verify20-AC1-d")
OUT = CHK / "ledgers/AC1/scripts/AC1-d-r20/out"
prev = json.loads(Path("/tmp/fanout-frags/AC1-d.round19.json").read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

# Re-verified this round: id -> (check, location, status, evidence[, fix]).
NEW: dict[str, tuple] = {}


def new(rid, check, location, evidence, status="PASS", fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        row["fix"] = fix
    NEW[rid] = row


R = "ledgers/AC1/scripts/AC1-d-r20/out"
new("proj-run-graders", "2.6-autograder-reference", "course/modules/AC/AC1/grader/ (reference.py, test_project.py, instance.py)",
    f"Re-run r20: tools/run_graders.py --unit AC1 --seeds 0-49 printed 'run_graders AC1: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0 ({R}/run_graders.out). Also reference.py run through scripts/AC1-d-r20/run_suite.sh on seeds 0-49: 316 passed on every seed; starter.py: 314 failed, 2 passed (seed 0).")
new("proj-collect-count-176", "2.6-collect-count", "course/modules/AC/AC1/project.html line 368 ('collects 316 checks'); grader/test_project.py",
    "Re-run r20: pytest --collect-only on reference.py for seeds 0 to 49 gave 316 tests on all 50 seeds (tally: 'count 316 seeds 50'). Previous pin 51fa336 collected 310 (prev_grader/test_project_51fa336.py); the +6 are the new parametrize case, the new overdrawn-cash test and four 2000-02-28 cases (diff of collected IDs, scripts/AC1-d-r20/out/ids_diff_r20.out).")
new("proj-local-suite-reference", "2.6-local-suite", "course/modules/AC/AC1/project.html lines 412-415 ('Running the suite locally')",
    "Re-run r20: the command shape (pytest -q -p no:cacheprovider --assert=plain -W error test_project.py with QF_SEED) is what scripts/AC1-d-r20/run_suite.sh runs (-I -W error --assert=plain); reference passes 316 on seeds 0-49. Line 415 'pinned to (Pyodide 314.0.7)' is backed by tools/vendor_spec.yaml line 54 (version '314.0.7' under pyodide).")
new("proj-pyodide-smoke", "2.5-page-smoke", "course/modules/AC/AC1/project.html; L04, L05, L06, L07, L08",
    f"Re-run r20: tools/page_smoke.py --unit AC1 --pages project printed 'page_smoke modules/AC/AC1/project.html: PASS', in-browser grader 'All 316 tests pass on seed 1653240555. (1.2 s)' ({R}/page_smoke_project.out); --pages L04 L05 L06 L07 L08 PASS for each page with its lab ({R}/page_smoke_lessons.out).")
new("proj-check-pages", "2.9-structure", "course/modules/AC/AC1/*.html; cards.json", f"Re-run r20: tools/check_pages.py --unit AC1 and --all: PASS, exit 0 ({R}/check_pages.out, check_pages_all.out).")
new("proj-check-projects", "2.9-structure", "course/modules/AC/AC1/project.html (budget, rungs)", f"Re-run r20: tools/check_projects.py --unit AC1 and --all: PASS, exit 0 ({R}/check_projects.out, check_projects_all.out).")
new("proj-check-dag", "DAG", "project.html 'Concepts used here'; L01-L03 concept definitions", f"Re-run r20: tools/check_dag.py --unit AC1 and --all: PASS, exit 0 ({R}/check_dag.out, check_dag_all.out).")
new("proj-run-labs", "2.5-labs", "tests/labs/AC1/lab-AC1-project-1.py, -project-2.py, -project-3.py and L01-L08 lab twins",
    f"Re-run r20: tools/run_labs.py --unit AC1: 'run_labs AC1: PASS (11/11)', exit 0 ({R}/run_labs.out). The three project twins run alone under python -I -W error exit 0 and print the page's expected lines (scripts/AC1-d-r20/out/project_lab_1.out, _2.out, _3.out); the L04, L05 and L06 twins exit 0 under -I -W error (twin_L04.out, twin_L05.out, twin_L06.out).")
new("proj-lab-twin-embed", "2.5-labs", "project.html lab blocks (Lab 1 lines 56-253, Lab 2 lines 260-343, Lab 3 lines 420-518)",
    "Re-run r20: run_labs.py --unit AC1 PASS (11/11), which holds each embedded lab to its twin's output; the Lab 2 block text changed at lines 259 and 344 (hypothesis and interpretation only, code unchanged) and its printed output is unchanged (lines 341-343 vs project_lab_2.out).")
new("proj-labs-ruff", "gate", "tests/labs/AC1; course/modules/AC/AC1/grader", f"Re-run r20: ruff check course/modules/AC/AC1 tests/labs/AC1 and ruff check . 'All checks passed!', exit 0; ruff format --check on the same paths '15 files already formatted', exit 0 ({R}/ruff_check.out, ruff_check_all.out, ruff_format.out).")
new("proj-mypy-gate", "gate", "tests/labs/AC1; course/modules/AC/AC1/grader", f"Re-run r20: mypy --no-incremental 'Success: no issues found in 153 source files', exit 0 ({R}/mypy.out).")
new("proj-verify-refs", "2.1-citations", "references/references.json; project.html line 534 (data-cite penman2013financial)",
    f"Re-run r20: tools/verify_refs.py --offline 'offline integrity: 560 entries, 0 problems' exit 0; tools/verify_refs.py --unit AC1 'live re-verification of AC1: 2 of 560 entries, 0 problems' exit 0 ({R}/vr_offline.out, vr_live_AC1.out). The cited key is among the 2 live entries of AC1 only by the unit's scope; no registry file changed since the previous pin.")
new("proj-hours", "hours", "project.html line 33 (data-hours-project 30); time-budget table lines 386-401; index.html line 29 (data-hours-lessons 90)",
    "Re-check r20: table rows sum 1+3+4+4+3+5+2+5+3 = 30 (row 399 'Total' 30); the table text is unchanged (lines 390-399 not in the round-20 delta). Hub index.html data-hours-lessons=90; lesson data-hours values L01..L08 = 11,12,11,11,12,12,11,10, sum 90 (the arithmetic matches). Declared hours are design targets (architect ruling) and were not re-estimated.")
new("proj-prose-banned", "1.2/1.3-banned-phrases", "project.html and grader/test_project.py added lines (scripts/AC1-d-r20/out/added_lines_51fa336_to_fd9a9b7.txt, 37 lines)",
    f"Re-run r20: scripts/AC1-d-r20/delta_scans.py over the 37 added lines of the slice's pages and grader: 'banned hits: 0', 'process-word hits: 0' ({R}/delta_scans.out).")
new("proj-alt-implementations", "2.6-over-constraint (architect ruling b)", "course/modules/AC/AC1/grader/test_project.py (whole suite) against 38 alternative implementations",
    f"Re-run r20: scripts/AC1-d-r20/run_alt_one.sh over all 38 alternative files (35 earlier, scripts/AC1-d-r7..r19, plus 3 new: alt_r20_a_bisect_sorted_postings.py, alt_r20_b_single_pass_flows.py, alt_r20_c_next_day_month_end.py, generated by scripts/AC1-d-r20/mk_alts20.py): every alternative 'seeds with failures: 0 of 50' ({R}/alts_all_r20.out).")
new("proj-r20-new-tests-spec-supported", "2.6-spec and over-constraint (architect ruling b)", "grader/test_project.py: new test_an_overdrawn_cash_balance_is_reported_as_a_negative_amount (new test, after line 806); new parametrize case 'a line with a debit smaller than its credit, in an entry that balances'; new '2000-02-28' in the period-end list",
    "Each new check is stated by project.html line 366: 'Money is never converted and never adjusted: the engine reports the cents it is given' (overdrawn cash -100 reported as -100); 'a line with both a debit and a credit, of any sizes' (the debit-3/credit-5 line must raise ValueError); 'Each of the three statement functions and the articulation check raises for a period end that is not a month end' with 2000 a leap year (2000-02-28 is not a month end; 2000-02-29 is). All 316 tests pass on the reference for seeds 0-49. Alternatives pass; mutants fx/fix19d01/fix19d09 and v20_m02 are killed.")
new("proj-r20-collect-delta", "2.6-collect-count", "grader/test_project.py; project.html line 368",
    "Collected IDs seed 0: 310 at 51fa336, 316 at fd9a9b7. The diff of IDs (scripts/AC1-d-r20/out/ids_diff_r20.out) is the 'debit smaller than its credit' parametrize case (+1), 'test_an_overdrawn_cash_balance_is_reported_as_a_negative_amount' (+1) and test_period_end_must_be_a_month_end[2000-02-28-...] for four lambdas (+4).")
new("proj-r20-lab2-hypothesis-and-interpretation", "2.9-prose", "project.html line 259 (Lab 2 hypothesis) and line 344 (Lab 2 interpretation)",
    "The cash gap and earnings gap are defined under Conventions (lines 379: cash_gap = balance sheet cash less ending cash; retained_earnings_gap = change in retained earnings less net income and dividends_paid); the balance gap and depreciation gap are defined on lines 378 and 379. The Lab 2 code block (project.html lines 260-340, def retained at line 296) computes only cash_gap and earnings gap; its printed lines are 'ending cash 4800000 cash gap 0' and 'retained change 700000 earnings gap 0' (project_lab_2.out). The retained helper is in the code (line 'def retained').")
new("proj-r20-pytest-pin-claim", "2.9-prose", "project.html line 415",
    "'the versions the in-browser grader is pinned to (Pyodide 314.0.7)': tools/vendor_spec.yaml line 54 has pyodide version \"314.0.7\". Pytest 9.0.2 is the local pin in requirements-dev.txt (carried claim of round 19; the sentence says the versions are pinned, which the vendor spec and requirements support).")
new("proj-r20-line-366-and-368-carry", "2.9-spec", "project.html lines 366 and 368 (Constraints and Grading mode)",
    "Line 366 'Money is never converted and never adjusted' and the 'Every named error condition raises ValueError' list are unchanged; line 368 changed only its count (310 to 316), verified above; the 'covers' list is not exhaustive and the new cases fall within its boundary-case families.")
new("proj-r20-lab1-interpretation-carry", "2.2-numbers-in-prose", "project.html line 254 (Lab 1 interpretation)",
    "Recomputed from the printed Lab 1 output (project_lab_1.out): February sales 1,600,000 less cost 900,000 gives net income 700,000; receivables 2,400,000 to 2,200,000 (fall 200,000, cash +200,000), inventory 1,300,000 to 400,000 (fall 900,000, cash +900,000), payables 2,500,000 to 0 (cash -2,500,000); the three sum to -1,400,000 and operating cash flow is 700,000 - 1,400,000 = -700,000. Matches the printed line.")
new("proj-r20-l04-why-it-matters", "2.9-prose", "course/modules/AC/AC1/L04.html line 52 (why-it-matters, changed sentence 'Two recognition rules applied to the same transactions can report different net income in the same quarter, as Lab 1 shows')",
    f"Lab 1 output (twin_L04.out, quarter 1): ni_rule_a -52491 and ni_rule_b 3612039, so the two rules report different net income in the same quarter (quarter 0: both 3287820). The claim is supported by the printed numbers in scripts/AC1-d-r20/out/twin_L04.out.")
new("proj-r20-l04-units-no-ratio", "2.9-prose", "course/modules/AC/AC1/L04.html line 132-135 and tests/labs/AC1/lab-AC1-L04-1.py line 4 ('The lab prints no ratio.')",
    "The twin's full printed output (scripts/AC1-d-r20/out/twin_L04.out) contains integer cents and True/False flags only, no ratio, share or percentage. The docstring sentence matches the output, and the embedded copy is identical to the twin (run_labs PASS).")
new("proj-r20-l05-why-it-matters-def13", "2.9-prose", "course/modules/AC/AC1/L05.html line 52 ('a transaction price (Definition 1.3)')",
    "Definition 1.3 (L05.html lines 66-68) states 'let the transaction price be the integer P in cents', so the cross-reference is correct; Definition 1.2 is the performance obligation, cited as 'Definition 1.2 below' and correctly located.")
new("proj-r20-l05-remark-1-5-solution", "2.4-expected-values (solution text)", "course/modules/AC/AC1/L05.html line 401 (solution to the M1 scaling exercise, 'as Remark 1.5 states')",
    "Remark 1.5 (L05.html line 87) states 'Scaling every stand-alone price by the same factor leaves it unchanged'; the solution's floors (16,666, 33,333, 50,000), remainders (40, 20, 0) and the extra cent to obligation 1 (largest remainder 40) give 16,667, 33,333, 50,000, which equals M1. The attribution is to the scaling invariance that Remark 1.5 states, which is the claim the solution uses.")
new("proj-r20-l05-line-333-identities", "2.9-prose", "course/modules/AC/AC1/L05.html line 333 (interpretation, 'The balance identity and the month-6 identity are true by the construction of the lab')",
    "tests/labs/AC1/lab-AC1-L05-1 computes balance = billed_cum - recognized_cum and then prints the identity 'balance_identity True' against the same expression (lines 139-146), and month_6_difference_equals_over_time_revenue compares the difference with the over-time sum it is built from (lines 154-167). Both True prints therefore test the code, as the sentence says. The sentence is correct.")
new("proj-r20-l05-line-333-numbers", "2.2-numbers-in-prose", "course/modules/AC/AC1/L05.html line 333 (interpretation numbers)",
    f"Recomputed in the twin output (scripts/AC1-d-r20/out/twin_L05.out): shares 0.0675, 0.1173, 0.3713, 0.4439 (sum 1.0000); month-6 share 50,471,362 / 80,495,111 = 0.627011; 0 percent contract asset 23,333,398 / 80,495,111 = 0.28987 (0.2899 to four decimals); 2,717,022 = 6 x 452,837 and 17,866,146 = 6 x 2,977,691, total 20,583,168. All match the printed text.")
new("proj-r20-l05-line-387-solution", "2.4-expected-values", "course/modules/AC/AC1/L05.html line 387 (solution, 'Revenue in month 6 is 2,000, from obligation B alone')",
    "Obligation A is 60,000 in month 3 only; obligation B gives 24,000/12 = 2,000 in each month 1 to 12. Month 6 revenue is 2,000 from B alone, and cumulative through month 6 is 60,000 + 6 x 2,000 = 72,000. Correct.")
new("proj-r20-l06-line-296-articulation", "2.9-prose", "course/modules/AC/AC1/L06.html line 296 (interpretation, 'That check follows from how the schedule is built, so it tests the code and not the economics.')",
    "tests/labs/AC1/lab-AC1-L06-1.py lines 133-139: articulation = (ROU - liability change) equals payment minus expense_f, where expense_f = interest + amortization (the lab's docstring defines pattern F so) and interest and amortization are the schedule's own terms; the identity is algebraic in the construction, so the True print tests the code. Printed values in twin_L06.out (articulation_every_year True, year-1 expense 14,820,224 = 4,535,544 + 10,284,680) match the page.")
new("proj-r20-l07-section1-scu-dollar", "2.9-prose", "course/modules/AC/AC1/L07.html line 55 ('Amounts are in integer cents of SCU ... a dollar sign, which here means SCU'; 'Three terms are used in this section and the next')",
    "Worked examples with '$' in the lesson: line 86 ('1,200 cents ... or $12,000') and line 119 ('\\(\\mathrm{OI}_1 = \\$50{,}000\\)'). The three terms: vesting and grant-date fair value are defined in Section 1 (lines 55 and 59), additional paid-in capital is used in Section 2 (line 96, Delta APIC_t = S_t). The scope sentence is true of the three terms as a set.")
new("proj-r20-l07-why-it-matters", "2.9-prose", "course/modules/AC/AC1/L07.html line 51 (why-it-matters, 'no forfeitures (an award the employee loses before the required service is complete)')",
    "Assumption (ii) in Section 2 (line 73) reads 'No award is forfeited, that is, lost by the employee before it vests', and vesting is 'the period in which the employee must remain in service before the award is theirs' (line 55). The why-it-matters paraphrase matches both.")
new("proj-r20-l08-why-and-section1", "2.9-prose", "course/modules/AC/AC1/L08.html lines 51 and 55 (why-it-matters; Section 1 amounts paragraph)",
    "Definition 1.1 (line 58): C a multiple of 10,000 cents, b = C/L with C/L a multiple of 100 cents, tau_t = C p_t / 100, one flat rate r; so b and tau are multiples of 100 cents and K_t (Definition 1.2, line 63) is a sum of tau_s - b_s, a multiple of 100. Current tax CT_t = r(P_t - (tau_t - b_t))/100 and TE_t = r P_t / 100 are integers when P_t is a multiple of 100 (cards c110, c121). Example 1.4 writes $ amounts (the dollar sign means SCU, as line 55 says). All consistent.")
new("cards-L05", "2.7-cards", "cards.json c061-c074; L05.html lines 52, 121, 124, 333, 387, 401",
    "Group re-checked in round 20 (cards.json unchanged since the previous pin; L05 lines 52, 121, 333, 387 and 401 changed). Cards c061-c065, c068, c070, c072-c074 match the lesson and Lab 1 output (twin_L05.out; c070 numbers 32,792,272 and 23,333,398; c073 80,495,111 and 20,583,168). c069 fails (row cards-c069). Group FAIL because of c069 and the Remark 2.4 finding.",
    status="FAIL", fix="Fix cards-c069 and the Remark 2.4 hypothesis (row lesson-change-audit-r20-l05-remark-2-4).")
new("cards-c069", "2.7-cards", "cards.json AC1-c069 (L05); L05 Section 2 and problem P3",
    "Re-verified r20: cards.json AC1-c069 back text still reads '(Remark 2.4 in Section 2; problem P3)'. Remark 2.4 (L05.html line 121) is about the balance as a timing wedge and contains no convention difference; the statement is the unlabelled paragraph at line 124 ('the difference at any month m < 12 equals the convention-1 revenue ... from the over-time obligations') and is proved in P3 (lines 422-426). The card's substance is correct, its locator is wrong.",
    status="FAIL", fix="In cards.json AC1-c069 replace '(Remark 2.4 in Section 2; problem P3)' with '(the paragraph after Remark 2.4 in Section 2, beginning \"Convention 1 and convention 2 agree at month 12\"; problem P3)'.")
new("lesson-change-audit-r20-l05-remark-2-4", "2.2-scope-and-hypotheses (rewritten sentence)", "course/modules/AC/AC1/L05.html line 121 (Remark 2.4, 'When total billing equals the price, it is zero at the end of the contract under Proposition 2.3')",
    "Proposition 2.3 (L05.html line 111) states: 'If total billing equals P and total revenue equals P, then D_12 = 0'; its proof (line 116) uses V_12 = P from Proposition 2.1. The Remark cites Proposition 2.3 with only the billing hypothesis. Within the lesson the revenue hypothesis holds under convention 1 (Proposition 2.1), but Definition 2.2 defines V_m for any revenue schedule, so the Remark states a sufficient condition that is not sufficient alone (witness: billing = P, revenue total 0, balance at month 12 = P, not 0). cards-c068 states both hypotheses correctly.",
    status="FAIL", fix="In Remark 2.4 replace 'When total billing equals the price, it is zero' with 'When total billing and total revenue both equal the price (Proposition 2.3, with revenue equal to the price under convention 1 by Proposition 2.1), it is zero'.")
new("lesson-change-audit-r20-l06-l07-l08", "2.2-numbers-and-scope (rewritten sentences)", "course/modules/AC/AC1/L06.html line 296; L07.html lines 51, 55; L08.html lines 51, 55",
    "Each rewritten sentence is checked above (proj-r20-l06-line-296-articulation, proj-r20-l07-section1-scu-dollar, proj-r20-l07-why-it-matters, proj-r20-l08-why-and-section1). The L08 why-it-matters sentence 'the cumulative difference of Definition 1.2 is a sum of them' and the L07 'Three terms are used in this section and the next' are true as written (evidence in those rows).")
new("cards-L04", "2.7-cards", "cards.json c046-c060, c122, c132 (L04)", "Group re-checked in round 20: cards.json unchanged; the L04 changed lines (52 why-it-matters, 132-135 Units) are not cited by any L04 card (vocabulary scan: scripts/AC1-d-r20/delta_scans.py; out/delta_scans.out). Lab 1 numbers on c056, c060, c132 (3,319,293; -4,974,286; 6,632,381) match twin_L04.out.")
new("cards-L06", "2.7-cards", "cards.json c075-c090 (L06); L06.html line 296", "Group re-checked in round 20: c086, c088, c089, c090 numbers match twin_L06.out (1,785,952; -1,977,098; 14,820,224 vs 13,034,272; 61,708,083 and 63,494,035; 13,034,273 vs 13,034,272). The changed line 296 sentence is not cited by a card. Carried cards c075-c085, c087 are unchanged lesson text.")
new("cards-L07", "2.7-cards", "cards.json c091-c104 (L07); L07.html lines 49 and 55",
    "Group re-checked in round 20: c091 (vesting: 'the period in which the employee must remain in service'), c092 ('in integer cents'; line 59 'in integer cents'), c093 match L07 lines 55 and 59; c099 and c100 numbers (57,822.92 SCU, 6 of 6 years, 4 of 4 schedules) match the Lab 1 output in L07 (unchanged). c135-c138 cite Definition 1.2 (ii)-(v) (line 73), unchanged.")
new("cards-L08", "2.7-cards", "cards.json c105-c121, c125, c129-c131, c139 (L08); L08.html lines 51, 55",
    "Group re-checked in round 20: c105 to c107 (carrying amount, tax base, temporary difference) match the unchanged definitional content of L08 line 55 ('cost less book depreciation to date', 'cost less the tax depreciation to date'); c108 matches Definition 1.1 (line 59); c109 matches Definition 1.2 (line 63). Other L08 cards cite unchanged passages.")

new("lesson-change-audit-r19-l04-l05-l06-l08", "2.2-numbers-and-scope (round-19 rewritten sentences, re-checked)", "course/modules/AC/AC1/L04.html line 330 (Section 5 bullet, round 19); L05.html Remark 1.5, Remark 2.4, Proposition 1.4 key-results; L06.html Section 4; L08.html Section 2 integer paragraph",
    "Re-checked in round 20 against the current text. L05 Remark 2.4 (line 121) was changed again in round 20 and now states the billing hypothesis without the revenue hypothesis of Proposition 2.3: FAIL, see lesson-change-audit-r20-l05-remark-2-4. The other round-19 sentences are not changed by the round-20 delta (L04.html line 330, L05 Remark 1.5 at line 87, L06 Section 4, L08 Section 2) and their round-19 evidence stands only by the byte-identity of those lines (checked by git diff 51fa336..fd9a9b7 which lists changes only at L04 lines 52 and 132, L05 lines 52, 121, 333, 387, 401, L06 line 296, L07 lines 51, 55, L08 lines 51, 55).",
    status="FAIL", fix="Fix Remark 2.4 as in lesson-change-audit-r20-l05-remark-2-4; the other sentences need no change.")

ALT_EVIDENCE = (
    "Re-run in round 20: scripts/AC1-d-r20/run_alt_one.sh on all 38 alternative implementation files, seeds 0 to 49: "
    "every alternative has 'seeds with failures: 0 of 50' (scripts/AC1-d-r20/out/alts_all_r20.out); the grader it runs against is the round-20 grader."
)
OVERRIDE_CARRY = {
    "proj-overconstraint-nonmapping": "Re-verified round 20: the test_post_raises_a_value_error parametrize list changed (one case added: 'a line with a debit smaller than its credit, in an entry that balances', which the page's line 366 supports: 'a line with both a debit and a credit, of any sizes'). The other cases are unchanged and each raises ValueError on the reference (316 passed, seeds 0-49). Not mapped to a non-spec error.",
    "proj-page-spec-carry-post-cases": "Re-verified round 20: the post-raises list (now 35 cases) still maps each case to a named condition on project.html line 366; the added case is the 'both a debit and a credit' condition. Alternatives pass (ALT).",
    "proj-grader-carry": "Re-verified round 20: the round-19 hunks are unchanged except the new cases documented under proj-r20-new-tests-spec-supported; the suite passes the reference on seeds 0-49 and the 38 alternatives on seeds 0-49.",
    "proj-r14-test-large-amount": "Re-verified round 20: test_a_large_amount_posts_at_its_full_value still exists and passes on the reference and alternatives; line 368 changed only in its count.",
    "proj-page-lab-carry": "Re-verified round 20: Lab 1 block (lines 56-253) code and output unchanged; Lab 2 block (lines 257-344) hypothesis and interpretation changed (proj-r20-lab2-hypothesis-and-interpretation), code and printed output unchanged; Lab 3 block (lines 418-518) unchanged. run_labs 11/11 and the three twins print the expected lines.",
    "proj-pytest-version-claim": "Re-verified round 20: line 415 now reads 'the versions the in-browser grader is pinned to (Pyodide 314.0.7)'; see proj-r20-pytest-pin-claim (tools/vendor_spec.yaml line 54 pins 314.0.7).",
    "proj-l01-pytest-claim-line-415": "Re-verified round 20: project.html line 415 changed in the round-19 fix (see proj-r20-pytest-pin-claim); the pytest 9.0.2 and Python 3.14 versions are the local pins in requirements-dev.txt as before.",
    "proj-line-368-grading-claims": "Re-verified round 20: line 368 now says 'collects 316 checks' and 'the count is 316 for each of the seeds 0 to 49'; the collect-only run gives 316 on all 50 seeds (proj-collect-count-176); the coverage list is unchanged.",
    "proj-r19-collect-all-seeds": "Re-verified round 20: collect-only on the reference gives 316 on each of seeds 0 to 49 (scripts/AC1-d-r20/out is the tally); the round-19 figure of 310 is superseded by the round-19 fix that added 6 collected checks (proj-r20-collect-delta).",
    "proj-v17-collect-and-count-line-368": "Re-verified round 20: line 368 count is 316 and the collect-only count is 316 on all 50 seeds (proj-collect-count-176); the earlier count change is superseded.",
}
ALT_IDS = {
    "proj-r14-alternatives-new", "proj-r15-alts-a-b-c", "proj-r18-alternatives-d-b-c", "proj-r19-alternatives-new-a-b-c",
    "proj-r19-alternatives-existing-35", "proj-v16-alternatives-r16", "proj-v17-alternatives-r17",
}

# Carry: round-19 PASS rows not re-verified above (cited subject unchanged since the previous pin).
# Rows re-verified above keep their new evidence. Mutant rows are re-run this round (see mutants list).
MUTANT_IDS = {
    r["id"] for r in prev["rows"]
    if r["id"].startswith(("proj-mutant", "proj-mutants", "proj-r14-mutant", "proj-r15-mutant", "proj-v16-mutant",
                           "proj-v17-mutants", "proj-r18-student", "proj-r19-student", "proj-v16-m", "proj-r15-mutant",
                           "proj-mutants-m", "proj-mutant-m"))
}
REVERIFIED_MUTANT_ROW = (
    "Re-run in round 20: all 179 earlier mutant files and the 6 new round-20 mutants were run against seeds 0 and 17 "
    f"({R}/mutants_r20.out, {R}/mutants_v20_new.out); every one is killed (failing tests on both seeds)."
)
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in NEW:
        rows.append(NEW[rid])
    elif rid in OVERRIDE_CARRY:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": OVERRIDE_CARRY[rid]})
    elif rid in ALT_IDS:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ALT_EVIDENCE})
    elif rid in MUTANT_IDS:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": REVERIFIED_MUTANT_ROW})
    elif r["status"] == "PASS":
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": "Carried from round 19 (" + r["location"].split(" (")[0].split(";")[0].strip()
                     + " byte-identical since the previous pin, cited subject unchanged): " + r["evidence"]})
    else:
        # previous non-PASS rows: re-verified above (cards-L05, cards-c069); any other would need a fresh verdict
        if rid not in NEW:
            raise SystemExit(f"previous non-PASS row {rid} not re-verified")
ids_prev = {r["id"] for r in prev["rows"]}
for rid, row in NEW.items():
    if rid not in ids_prev:
        rows.append(row)
seen = set()
for row in rows:
    assert row["id"] not in seen, row["id"]
    seen.add(row["id"])
missing = ids_prev - seen
print("previous ids missing from this round:", sorted(missing))

mutant_files = sorted(p for p in (CHK / "ledgers/AC1/mutants").glob("*.py"))
mutants = []
for p in mutant_files:
    name = p.stem
    mutants.append({"id": name, "description": name.replace("_", " "), "file": f"ledgers/AC1/mutants/{p.name}",
                    "killed_by": "seeds 0 and 17: both fail (scripts/AC1-d-r20/out/mutants_r20.out and mutants_v20_new.out)"})
fragment = {
    "unit": "AC1",
    "slice": "AC1-d",
    "round": 20,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 20 (did not build AC1; read the round-19 fragment as context, computed the delta 51fa336..fd9a9b7 on the slice)",
    "pin": "fd9a9b7",
    "base": "51fa336 (round-19 pin). Slice delta: course/modules/AC/AC1/project.html (lines 257, 259, 342, 344, 368, 415), grader/test_project.py (+21 lines: one parametrize case, one overdrawn-cash test, one '2000-02-28' period end), L04.html (52, 132), L05.html (52, 121, 333, 387, 401), L06.html (296), L07.html (51, 55), L08.html (51, 55), tests/labs/AC1/lab-AC1-L04-1.py (line 4). cards.json, the starter, instance.py and the other lessons are unchanged.",
    "checkout": str(CHK),
    "scratch": "/tmp/ac1-v/d20",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Verified this round: run_graders AC1 PASS (50/50); reference 316 passed on seeds 0-49; starter 314 failed; collect 316 on all 50 seeds; page_smoke project and L04, L05, L06, L07, L08 PASS; run_labs 11/11; check_pages, check_dag, check_projects PASS (AC1 and all units); build_site --check; render_curriculum (no diff to CURRICULUM.md or curriculum.json); verify_refs offline 560/0 and live AC1 2/0; ruff check (AC1 and whole repo) and format; mypy strict 153 files; pytest subset (labs, run_labs, page_checks, page_smoke) 182 passed; 185 mutants (179 earlier plus 6 new round-20 student errors) all killed on seeds 0 and 17; 41 alternative implementation files on seeds 0 to 49 (38 unique by name, including 3 new), all pass. Not checked: Pyodide 314.0.7 itself (local Python 3.14.8 and pytest only); the L07 and L08 lab twins were not run as twins (run_labs covers them and page_smoke passed); the L01 to L03 pages and their cards (carried by byte identity). Out-of-slice observation for the L04 owner: L04.html key-results row (line 473) reads 'cash plus receivables, plus the unexpired prepaid balance under rule B, equals cumulative net income under each rule', which is ambiguous for rule A (carried observation from round 19; the row is not in this slice).",
    "summary": "AC1-d round 20: verdict FAIL. Three FAIL rows: cards-c069 (locator 'Remark 2.4' does not contain the convention-difference statement; the paragraph after Remark 2.4 at L05.html line 124 does), cards-L05 (group, from c069), and lesson-change-audit-r20-l05-remark-2-4 (Remark 2.4 cites Proposition 2.3 with only the billing hypothesis; Proposition 2.3 also needs total revenue equal to the price). Every other row PASS, re-verified this round or carried with its cited subject byte-identical. Mutants: 185, all killed on seeds 0 and 17. Alternatives: 41 files (38 unique names), all pass on seeds 0 to 49.",
}
out = CHK / "ledgers/AC1/AC1-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
counts = {}
for row in rows:
    counts[row["status"]] = counts.get(row["status"], 0) + 1
print("rows", len(rows), counts, "mutants", len(mutants))
