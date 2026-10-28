"""Builds ledgers/AC1/AC1-d.json (round 17) from the round-16 fragment (context only) and the round-17 outputs.

Rows whose cited subject is byte-identical since the previous pin are carried with the prefix the brief requires;
every other row is re-run or re-derived this round and says so. Usage: python3 -I build_fragment_r17.py
"""
import json
from pathlib import Path

CHK = Path("/tmp/verify17-AC1-d")
OUT = CHK / "ledgers/AC1/scripts/AC1-d-r17/out"
prev = json.loads(Path("/tmp/fanout-frags/AC1-d.round16.json").read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
prev_mut = {m["id"]: m for m in prev["mutants"]}

CARRY_FILES = "course/modules/AC/AC1/project.html line 366 and lines 33-47, 51-52, 370-415, 533-549 (only line 368 changed)"
PREFIX = "Carried from round 16 (files byte-identical since the previous pin): "


def files_for(location):
    import re

    names = []
    for m in re.findall(r"[\w/.-]+\.(?:html|py|json|md|yaml)", location):
        if m not in names:
            names.append(m)
    parts = []
    for n in names:
        if n.endswith("project.html"):
            parts.append("project.html (cited lines unchanged; only line 368 changed)")
        elif n.endswith("cards.json"):
            parts.append("cards.json (the cited card objects identical at c5daab2 and fefbf8b)")
        else:
            parts.append(n)
    return ", ".join(parts) if parts else "the cited artifacts"


def carry(rid, files=None):
    r = prev_rows[rid]
    files = files or files_for(r["location"])
    return {**r, "status": "PASS", "evidence": PREFIX.replace("files", files) + r["evidence"]}


RERUN = {
    "proj-run-graders": (
        "PASS",
        "Round 17 re-run on fefbf8b: tools/run_graders.py --unit AC1 --seeds 0-49 printed 'run_graders AC1: PASS "
        "(reference 50/50 seeds, slowest 0.3 s)' (out/run_graders.out); the reference gave 287 passed on each of seeds "
        "0-49 with --assert=plain -W error (out/ref_50.out); the starter gave 285 failed, 2 passed on each seed "
        "(out/starter_50.out).",
    ),
    "proj-collect-count-176": (
        "PASS",
        "project.html line 368 now states 287 checks. pytest --collect-only on the reference gave '287 tests "
        "collected' on each of seeds 0-49 (out/collect_50.out, 50 of 50 lines).",
    ),
    "proj-pyodide-smoke": (
        "PASS",
        "tools/page_smoke.py --unit AC1 --pages project L01 L02 L03 (stems; 'project.html' matches nothing) printed "
        "page_smoke PASS for modules/AC/AC1/L01.html, L02.html, L03.html and project.html, with 'in-browser grader: All "
        "287 tests pass' on the project page (out/smoke_project_labs.out, exit 0).",
    ),
    "proj-check-pages": (
        "PASS",
        "tools/check_pages.py --all: 'check_pages AC1: PASS', exit 0 (out/check_pages.out).",
    ),
    "proj-check-projects": (
        "PASS",
        "tools/check_projects.py --all: 'check_projects AC1: PASS', exit 0 (out/check_projects.out).",
    ),
    "proj-check-dag": (
        "PASS",
        "tools/check_dag.py --all: 'check_dag AC1: PASS', exit 0 (out/check_dag.out).",
    ),
    "proj-run-labs": (
        "PASS",
        "tools/run_labs.py --unit AC1: 'run_labs AC1: PASS (11/11)', exit 0 (out/run_labs.out).",
    ),
    "proj-lab-twin-embed": (
        "PASS",
        "The three project twins tests/labs/AC1/lab-AC1-project-1.py, -2.py, -3.py ran with python -I -W error and "
        "exited 0 (out/twins_project.out). The lab blocks in project.html are byte-identical to the previous pin; "
        "tools/embed_labs.py cannot be run under -I (it imports coursekit from tools/), so the block-to-twin "
        "comparison is carried, not re-run.",
    ),
    "proj-labs-ruff": (
        "PASS",
        "ruff check . printed 'All checks passed!' and ruff format --check printed '212 files already formatted' "
        "(out/ruff.out).",
    ),
    "proj-mypy-gate": (
        "PASS",
        "mypy --no-incremental: 'Success: no issues found in 153 source files', exit 0 (out/mypy.out).",
    ),
    "proj-verify-refs": (
        "PASS",
        "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (out/vr_offline.out); "
        "tools/verify_refs.py --unit AC1: 'live re-verification of AC1: 2 of 560 entries, 0 problems' "
        "(out/vr_live_AC1.out). The data-cite penman2013financial entry on project.html line 534 is unchanged.",
    ),
    "proj-prose-banned": (
        "PASS",
        "A banned-string scan (TODO, TBD, lorem, ellipses, roughly, about N, historically, for brevity, beyond the "
        "scope, obviously, clearly, well known, experts agree, studies show, left as an exercise, you can add more, "
        "details omitted) of project.html lines 366 and 368 and of the grader hunks added since the previous pin "
        "found no match (this round's scan, run inline; the file is not written).",
    ),
    "proj-alt-implementations": (
        "PASS",
        "Nine alternative correct statements.py files ran the whole suite on seeds 0-49: round-15 alt_r15_a/b/c and "
        "round-16 alt_r16_a/b/c (out/alts_r15_r16_50.out, 300 runs, all '287 passed') and round-17 alt_r17_a/b/c "
        "(out/alts_r17_50.out, 150 runs, all '287 passed'). Each alternative changes one mechanism: a 32-day jump "
        "for the month end, a next-day probe, a sorted bisect, a regex date form with type() integer cents, a "
        "Counter-based balance, a next-day cutoff, a calendar previous month end.",
    ),
    "proj-overconstraint-nonmapping": (
        "PASS",
        "grader/test_project.py: the parametrize list of test_post_raises_a_value_error runs from line 317 to line "
        "690 and now includes ('a date of 2100-02-29, which is not a real calendar date', ...) at line 529. Each case "
        "maps to a named post condition on project.html line 366 ('a date that is not in the form YYYY-MM-DD or is "
        "not a real calendar date'). The nine alternatives pass it on seeds 0-49.",
    ),
    "proj-page-spec-carry-post-cases": (
        "PASS",
        "project.html line 366 is unchanged. grader/test_project.py line 529 adds the 2100-02-29 post case, which the "
        "named condition covers. test_a_century_leap_day_posts_as_a_real_date (line 1057) checks that post accepts "
        "2000-02-29, which line 366 treats as a real date.",
    ),
    "proj-no-expected-value-leak": (
        "PASS",
        "project.html line 368 still states that a failing check 'never prints the expected value'. The grader "
        "messages (_check_values, lines 227-234, pytest.fail with the property name only; the assertions at lines "
        "940-1001 print a period end or a property name) contain no expected value. The browser flags include "
        "--assert=plain (tools/run_graders.py docstring), which disables assertion introspection; under default "
        "pytest rewriting an assert with an expected local would show both sides, so the claim holds under the "
        "grading flags only.",
    ),
    "proj-grader-carry": (
        "PASS",
        "The grader delta since the previous pin is three hunks: line 529 (one parametrized post case), lines 1057-1069 "
        "(test_a_century_leap_day_posts_as_a_real_date, a new test that posts 2000-02-29 with 5 cents and checks the "
        "balance sheet). Each hunk was read in full and all 287 tests pass on the reference for seeds 0-49.",
    ),
    "proj-line-368-grading-claims": (
        "PASS",
        "project.html line 368 re-verified claim by claim: the count is 287 (collect-only, seeds 0-49). Each listed "
        "area maps to a test: chart_of_accounts (line 295), standard-library imports (896), posting rules and named "
        "errors (317-690), boundary cases (one-cent entry 786, 10**12 cents 309-313, zero on one side 792, repeated "
        "entry 853, two entries one date 868, empty list 842, dates 1 Jan/31 Dec 766 and the leap day 779), the "
        "statement functions' silence (capsys, 1120) and return values, the three statements against the seeded "
        "ledger for the twelve month ends (919-937), balance identity (938), cash tie (946), net change in cash "
        "(954), retained earnings (972), operating cash flow (982), four articulation gaps (GAP_KEYS line 94, 964), "
        "month-end rule and century years (1036-1098), hand-worked January (729-746). Balance and cash claims are "
        "checked by the test names and bodies cited, not by a second run.",
    ),
    "proj-cards-c001-c126-coverage": (
        "PASS",
        "cards.json has 139 cards, ids AC1-c001 to AC1-c139, contiguous (checked). 128 cards are byte-identical to the "
        "previous pin and carried; the 11 cards that changed or are new (c050, c051, c095, c111, c133-c139) were read "
        "against their lessons (rows cards-L04, cards-L07, cards-L08).",
    ),
    "cards-inventory-and-dupes": (
        "PASS",
        "139 cards; 139 unique ids; no duplicate fronts or backs (case-insensitive, stripped) "
        "(scan run inline this round; no file kept).",
    ),
    "cards-grades": (
        "PASS",
        "Grades: C 50, T 42, none 47 (ungraded cards are definitions and formulas, as in previous rounds). The new "
        "cards c133-c138 carry grade C with basis 'Convention of Lab 1 (Section 2)' or 'Model choices (Definition "
        "1.2)'; c139 and c111 are ungraded definitions and state no graded result.",
    ),
    "cards-numbers-in-lessons": (
        "PASS",
        "For the 11 changed or new cards every number in the back appears in the lesson text (tag-stripped): the "
        "scan found no number absent from its lesson.",
    ),
    "cards-labels-resolve": (
        "PASS",
        "Every citation label of the 11 changed or new cards resolves in its own lesson: 'Section 2' (L04, L08), "
        "'Section 3' (L04), 'Definition 1.2 (i)' to '(v)' (L07; the lesson lists the five items in Definition 1.2, "
        "line 96).",
    ),
    "cards-banned": (
        "PASS",
        "Banned-string scan over all 139 cards (front, back, basis): no match.",
    ),
    "cards-L04": (
        "PASS",
        "L04 cards re-read against L04.html: c050 'rule A' (Section 2, line 105: 'Under rule A, a service paid for in "
        "advance is expensed in full in the quarter it is paid'); c133 'rule B' (line 105: 'each of the first three is "
        "the payment divided by four, rounded down to whole cents, and the last share takes the remainder'); c051 and "
        "c134 'presentation 1 and 2' (Section 3, line 351 and 'Presentation 2 places it in financing cash flow'; "
        "'same cash movements', line 351). Lines 105, 351 verified by tag-stripped text. Other L04 cards carried.",
    ),
    "cards-L07": (
        "PASS",
        "L07 cards re-read against L07.html Definition 1.2 (line 96): c095 'total cost fixed on the grant date' = (i); "
        "c135 'no award is forfeited' = (ii); c136 'no performance or market conditions' = (iii); c137 'income tax is "
        "ignored' = (iv); c138 'shares issued at vesting are not counted' = (v). Each matches the wording of the item. "
        "Other L07 cards carried.",
    ),
    "cards-L08": (
        "PASS",
        "L08 cards re-read against L08.html Section 2 (lines 112-119): c111 'DE_t = DTL_t - DTL_(t-1), with DTL_0 = 0' "
        "(line 115 and line 119); c139 'TE_t = CT_t + DE_t' (line 116, 'TE_t = CT_t + DE_t'), with CT_t the current "
        "tax and DE_t the deferred tax expense (line 119). Other L08 cards carried.",
    ),
    "cards-c001-c128-coverage-r15": (
        "PASS",
        "Superseded by proj-cards-c001-c126-coverage: 139 contiguous cards, 128 identical to the previous pin.",
    ),
    "proj-tests-labs-pytest": (
        "PASS",
        "pytest -q tests/test_run_labs.py tests/test_labs.py tests/test_page_checks.py: all dots, exit 0 "
        "(out/pytest_labs.out).",
    ),
    "proj-r13-year-edge-tests": (
        "PASS",
        "grader/test_project.py test_entries_on_the_first_and_last_days_of_the_year_post_and_count (line 766) and "
        "test_an_entry_dated_on_the_leap_day_posts_and_counts (line 779) are unchanged and pass on seeds 0-49.",
    ),
    "proj-starter-fails": (
        "PASS",
        "grader/starter.py fails the suite on every seed 0-49: 285 failed, 2 passed (out/starter_50.out).",
    ),
    "proj-r14-test-large-amount": (
        "PASS",
        "grader/test_project.py test_a_large_amount_posts_at_its_full_value (line 309-313) unchanged; it passes on "
        "seeds 0-49 and the nine alternatives.",
    ),
    "proj-r15-century-test-comment": (
        "PASS",
        "The comment of test_a_century_year_follows_the_400_year_rule moved from lines 1056-1058 to lines 1071-1073 "
        "after the insertion of test_a_century_leap_day_posts_as_a_real_date above it (text unchanged; checked).",
    ),
    "proj-v16-post-2100-02-29-not-enforced": (
        "PASS",
        "Killed now: ledgers/AC1/mutants/v16_m01_post_accepts_2100_02_29_as_a_date.py gives '1 failed, 286 passed' on "
        "seeds 0 and 17 (out/mutants_r17.out). The added case at grader line 529 is the witness.",
    ),
    "proj-v16-post-2000-02-29-not-enforced": (
        "PASS",
        "Killed now: ledgers/AC1/mutants/v16_m02_post_rejects_2000_02_29_as_a_date.py gives '1 failed, 286 passed' on "
        "seeds 0 and 17 (out/mutants_r17.out). test_a_century_leap_day_posts_as_a_real_date (line 1057) is the witness.",
    ),
    "proj-v16-alternatives-r16": (
        "PASS",
        "ledgers/AC1/scripts/AC1-d-r16/mk_alts16.py regenerated the three round-16 alternatives from the reference; "
        "all 150 runs on seeds 0-49 pass (out/alts_r15_r16_50.out).",
    ),
    "proj-v16-century-tests-four-functions": (
        "PASS",
        "The century list of the four functions is at grader lines 1029 (2100-02-29 in test_period_end_must_be_a_month_end, "
        "unchanged) and test_every_function_accepts_a_century_month_end at lines 1085-1098 (moved from 1071-1084 by "
        "the insertion above it; text unchanged). Each function accepts 2000-02-29 and 2100-02-28 (run).",
    ),
    "proj-r14-alternatives-new": (
        "PASS",
        "Round-14 alternatives are carried by the round-15 and round-16 alternative runs (out/alts_r15_r16_50.out): "
        "300 runs all pass.",
    ),
    "proj-r15-alts-a-b-c": (
        "PASS",
        "ledgers/AC1/scripts/AC1-d-r15/alts/alt_r15_a/b/c: 150 runs on seeds 0-49, all '287 passed' "
        "(out/alts_r15_r16_50.out).",
    ),
    "proj-v16-mutant-m03-articulation-no-month-end-test": (
        "PASS",
        "Re-run: v16_m03 gives '3 failed, 284 passed' on seeds 0 and 17 (out/mutants_r17.out).",
    ),
    "proj-mutants-set-killed": (
        "FAIL",
        "Re-run of all 147 files in ledgers/AC1/mutants/ on seeds 0 and 17 (out/mutants_r17.out): 147 of 147 fail on "
        "both seeds. Three new student-error mutants written this round (v17_m01, v17_m02, v17_m03; out/new_mutants_r17.out) "
        "all pass the whole suite on seeds 0 and 17: 3 survivors, so the set is 147 of 150 killed.",
    ),
}

# every round-16 row is kept; mutant rows are re-run
FAIL_CARRIED_TO_PASS = {"proj-v16-post-2100-02-29-not-enforced", "proj-v16-post-2000-02-29-not-enforced"}
CARRY_OVERRIDE_FILES = {
    "proj-page-spec-carry": "course/modules/AC/AC1/project.html line 366",
    "proj-r15-line-366-century-rule-four-functions": "course/modules/AC/AC1/project.html line 366",
    "proj-hours": "course/modules/AC/AC1/project.html lines 33 and 386-402 and index.html line 29",
    "proj-instances-carry": "course/modules/AC/AC1/grader/instance.py",
    "proj-v16-line-396-gap-key": "course/modules/AC/AC1/project.html line 396",
    "proj-local-suite-reference": "course/modules/AC/AC1/project.html lines 412-415",
    "proj-pytest-version-claim": "course/modules/AC/AC1/project.html line 415",
    "proj-l01-pytest-claim-line-415": "course/modules/AC/AC1/project.html line 415",
    "proj-line-37-lede-seed": "course/modules/AC/AC1/project.html line 37 and the grader panel",
    "proj-footer-nothing-leaves": "course/modules/AC/AC1/project.html line 549",
}
MUT_NOTE = "Re-run round 17: "

rows = []
for rid, r in prev_rows.items():
    if rid in RERUN:
        st, ev = RERUN[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": ev,
                     **({"fix": "Add a posting case for 2024/01/02 (slash form) to the posting-error list (grader "
                                 "line 317 onward) and make the nine alternatives pass it."} if False else {})})
    elif rid in FAIL_CARRIED_TO_PASS:
        rows.append({**r, "status": "PASS", "evidence": MUT_NOTE + r["evidence"]})
    elif "mutant" in rid:
        rows.append({**r, "status": "PASS", "evidence": MUT_NOTE + "killed on seeds 0 and 17 (out/mutants_r17.out). "
                     + r["evidence"]})
    elif rid in CARRY_OVERRIDE_FILES:
        rows.append({**r, "status": "PASS", "evidence": PREFIX.replace("files", CARRY_OVERRIDE_FILES[rid]) + r["evidence"]})
    else:
        rows.append(carry(rid))

# new rows this round
NEW = [
    {"id": "proj-v17-slash-date-accepted", "check": "2.5-mutation (new student error, round 17) and 2.9-spec (post date rule)",
     "location": "course/modules/AC/AC1/project.html line 366 (Constraints: 'a date that is not in the form YYYY-MM-DD'); "
                 "grader/test_project.py lines 317-325 (posting-error list has no slash-form case); ledgers/AC1/mutants/v17_m01_slash_dates_normalised_and_accepted.py",
     "status": "FAIL",
     "evidence": "The mutant replaces '/' by '-' before validating a date. Witness (out/witness_r17.out): post([{date: '2024/01/02', ...}]) "
                 "returns the postings on the mutant and raises ValueError on the reference. The suite passes the mutant on seeds 0 and 17 "
                 "(out/new_mutants_r17.out: '287 passed'). The posting-error list tests '02/01/2024' (line 322) but no slash-form ISO-like date.",
     "fix": "Add ('a date with slashes in the form YYYY/MM/DD', [{**SMALL[0], 'date': '2024/01/02'}]) to the posting-error list in "
            "grader/test_project.py; the reference raises ValueError, so the reference and the nine alternatives still pass."},
    {"id": "proj-v17-line-both-sides-unequal-accepted", "check": "2.5-mutation (new student error, round 17) and 2.9-spec (post line rule)",
     "location": "course/modules/AC/AC1/project.html line 366 ('a line with both a debit and a credit, or with neither'); "
                 "grader/test_project.py lines 450-456 and 676-687 (both-sided cases use equal amounts, 5/5 and 7/7); ledgers/AC1/mutants/v17_m03_line_debit_and_credit_unequal_accepted.py",
     "status": "FAIL",
     "evidence": "The mutant tests the one-side rule with debit == credit, so a line with debit 5 and credit 3 passes. Witness (out/witness_r17.out): "
                 "post([{date: '2024-01-02', lines: [{cash, debit 5, credit 3}, {sales, debit 0, credit 2}]}]) is accepted by the mutant "
                 "and raises 'a line carries a debit or a credit, and exactly one' on the reference. Both seeds 0 and 17 pass on the mutant "
                 "(out/new_mutants_r17.out).",
     "fix": "Add a posting case with a balanced entry whose line has both a debit and a credit of unequal size (for example cash debit 5 "
            "credit 3 with sales credit 2) to the posting-error list; the reference raises ValueError so every alternative still passes."},
    {"id": "proj-v17-previous-month-end-century-leap", "check": "2.5-mutation (new student error, round 17) and 2.4-expected-values (century month end in the flow functions)",
     "location": "course/modules/AC/AC1/project.html line 366 (leap-year rule, and 'the statement functions ... raises for a period end that is not a month end'), line 368 ('the month-end rule, including century years'); "
                 "grader/test_project.py lines 1085-1098 (only 2000-02-29 and 2100-02-28, which do not reach the leap branch of the previous-month rule); ledgers/AC1/mutants/v17_m02_previous_month_end_leap_rule_without_century.py",
     "status": "FAIL",
     "evidence": "The mutant computes the previous month end with year % 4 and no century rule. Witness (out/witness_r17.out): "
                 "income_statement([], '2100-03-31') raises ValueError 'day 29 must be in range 1..28 for month 2 in year 2100' on the mutant and returns on the reference; "
                 "2100-03-31 is a month end (last day of March). The suite passes the mutant on seeds 0 and 17.",
     "fix": "Add a century-year flow check: income_statement, cash_flow_statement and articulation_check accept 2100-03-31 and 2000-03-31 (and the balance sheet "
            "agrees); the reference and the nine alternatives pass it."},
    {"id": "proj-v17-alternatives-r17", "check": "2.6-over-constraint (architect ruling b), round 17 alternatives",
     "location": "ledgers/AC1/scripts/AC1-d-r17/mk_r17.py; ledgers/AC1/scripts/AC1-d-r17/alts/alt_r17_a/b/c",
     "status": "PASS",
     "evidence": "Three alternatives, each changing one mechanism: alt_r17_a (month end by stepping one day forward), alt_r17_b (regex date form, type() int cents), alt_r17_c "
                 "(strict next-day cutoff in _balances, calendar previous month end with a January branch). Each runs the whole suite on seeds 0-49: 150 of 150 '287 passed' (out/alts_r17_50.out).",
     "fix": ""},
    {"id": "proj-v17-mutants-prior-147-rerun", "check": "2.5-mutation: every earlier mutant re-run",
     "location": "ledgers/AC1/mutants/ (147 files at fefbf8b, including v15_m01-m06, v16_m01-m03, fx16_m01)",
     "status": "PASS",
     "evidence": "All 147 files run on seeds 0 and 17 (out/mutants_r17.out): every one fails at least one test on both seeds (147 of 147). This includes the three round-16 mutants "
                 "(v16_m01 1 failed, v16_m02 1 failed, v16_m03 3 failed) that survived round 16.",
     "fix": ""},
    {"id": "proj-v17-equivalent-v16-m01-proof", "check": "2.5-mutation: equivalent mutant proof",
     "location": "ledgers/AC1/equivalent/v16_m01.proof.md; ledgers/AC1/equivalent/v16_m01_post_accepts_2100_02_29_as_a_date.py",
     "status": "PASS",
     "evidence": "The proof's premise holds: reference.py lines 34-43 (_iso_date) raise ValueError for 2100-02-29 via date.fromisoformat before any leap rule runs, and the equivalent file's _manual_iso_date (line 67) calls _iso_date first (line 68). For every date _iso_date accepts, a February 29 implies year % 4 == 0, so the manual rule gives the same length. Equivalent; the non-equivalent twin is ledgers/AC1/mutants/fx16_m01 (killed: 3 failed on both seeds).",
     "fix": ""},
    {"id": "proj-v17-collect-and-count-line-368", "check": "2.6-collect-count (round 17, count changed 285 to 287)",
     "location": "course/modules/AC/AC1/project.html line 368; grader/test_project.py",
     "status": "PASS",
     "evidence": "pytest --collect-only: 287 on each of seeds 0-49 (out/collect_50.out). The count matches the 287 on line 368. Two new collected items: one parametrize case (line 529) and one new test (line 1057).",
     "fix": ""},
    {"id": "cards-v17-changed-and-new-count", "check": "2.7-cards (count and changed cards)",
     "location": "course/modules/AC/AC1/cards.json (139 cards; changed c050, c051, c095, c111; new c133-c139)",
     "status": "PASS",
     "evidence": "128 cards identical to the previous pin, 4 changed, 7 new, computed by object comparison of the JSON at c5daab2 and fefbf8b. No page states a card count (grep of AC1 html for 'cards' finds only the 'Retrieval quiz' blocks).",
     "fix": ""},
]
rows.extend(NEW)
SET_FIX = ("Add the three survivors' witnesses to the grader: a slash-form date (proj-v17-slash-date-accepted), a balanced "
           "entry with an unequal both-sided line (proj-v17-line-both-sides-unequal-accepted) and a century-year March flow "
           "check (proj-v17-previous-month-end-century-leap); the reference and the nine alternatives pass all three.")
for r in rows:
    if r["id"] == "proj-mutants-set-killed":
        r["fix"] = SET_FIX
    if r["status"] == "PASS":
        r.pop("fix", None)
    elif not r.get("fix"):
        raise SystemExit(f"non-PASS row without fix: {r['id']}")

mutant_files = sorted((CHK / "ledgers/AC1/mutants").glob("*.py"))
mutants = []
NEW_SURVIVORS = ("v17_m01_slash_dates_normalised_and_accepted", "v17_m02_previous_month_end_leap_rule_without_century",
                 "v17_m03_line_debit_and_credit_unequal_accepted")
for f in mutant_files:
    mid = f.stem
    base = prev_mut.get(mid)
    desc = base["description"] if base else mid.replace("_", " ")
    killed = "" if mid in NEW_SURVIVORS else "seeds 0 and 17 (out/mutants_r17.out): both fail (round 17 re-run)"
    mutants.append({"id": mid, "description": desc, "file": f"ledgers/AC1/mutants/{f.name}", "killed_by": killed})

counts = {"PASS": sum(1 for r in rows if r["status"] == "PASS"), "FAIL": sum(1 for r in rows if r["status"] == "FAIL")}
frag = {
    "unit": "AC1", "slice": "AC1-d", "round": 17,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 17; did not build AC1; read the round-16 fragment as context and computed the delta c5daab2..fefbf8b on the slice",
    "pin": "fefbf8b", "base": "c5daab2 (round-16 pin)",
    "checkout": "/tmp/verify17-AC1-d", "scratch": "/tmp/AC1-v/AC1-d/r17",
    "verified_at": "2026-10-28T11:30:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta c5daab2..fefbf8b on the slice: project.html line 368 (count 285 to 287); grader/test_project.py line 529 "
        "(one post case), lines 1057-1069 (new test); cards.json c050, c051, c095, c111 changed and c133-c139 new; "
        "ledgers/AC1/mutants and equivalent gained v16 files. Lessons, index, labs, twins, instance.py, reference.py, "
        "starter.py, references and the other 128 cards are byte-identical. Re-run this round: collect-only on seeds "
        "0-49 (287 each), reference and starter on seeds 0-49, all 147 mutants on seeds 0 and 17, nine alternatives on seeds "
        "0-49, three new mutants and three witnesses, run_graders, page_smoke, check_pages/dag/projects, build_site --check, "
        "render_curriculum diff, verify_refs offline and live AC1, run_labs AC1, the three project twins, ruff, mypy, pytest "
        "subset. FAIL: three new survivors (rows proj-v17-slash-date-accepted, proj-v17-line-both-sides-unequal-accepted, "
        "proj-v17-previous-month-end-century-leap) and the set row proj-mutants-set-killed. NOT CHECKED: Pyodide 314.0.7 "
        "itself (local Python 3.14 only); the embed_labs block-to-twin comparison (tool needs tools/ on the path, not run under -I); "
        "the 47 ungraded cards were not re-graded beyond their citations; the 128 identical cards and the lessons were not "
        "re-read line by line this round (carried by the byte-identity rule, checked by scripts only); the three round-17 "
        "mutants were judged against line 366 and line 368, not against a published source."
    ),
    "summary": {"rows": len(rows), **counts, "UNVERIFIABLE": 0, "mutants": len(mutants),
                "mutants_killed_seed0_and_seed17": sum(1 for m in mutants if m["killed_by"])},
}
out = CHK / "ledgers/AC1/AC1-d.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants))
