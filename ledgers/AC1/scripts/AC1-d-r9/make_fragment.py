"""Writes ledgers/AC1/AC1-d.json (round 9, slice AC1-d). Run with python -I from the checkout root."""

import json
import pathlib

ROOT = pathlib.Path("/tmp/verify9-AC1-d")
OUT = ROOT / "ledgers/AC1/AC1-d.json"
PREV = "Carried from round 8 (byte-identical since the previous pin 2c8162b): "
DELTA_OK = "Re-verified round 9: "

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        r["fix"] = fix
    rows.append(r)


# ---- commands and gates (re-run on pin 96dd532 this round) ----
row("proj-run-graders", "2.6-autograder-reference", "course/modules/AC/AC1/grader/ (reference.py, instance.py, test_project.py)", "PASS",
    DELTA_OK + "tools/run_graders.py --unit AC1 --seeds 0-49 -> 'run_graders AC1: PASS (reference 50/50 seeds, slowest 0.3 s)' (/tmp/AC1-v9/AC1-d/run_graders.out). Direct run of ledgers/AC1/scripts/AC1-d-r9/run_suite.sh on reference.py, seed 0: '185 passed in 0.13s'.")
row("proj-collect-count-176", "2.6-spec-test-count", "project.html line 368 ('collects 185 checks'); grader/test_project.py", "PASS",
    DELTA_OK + "ledgers/AC1/scripts/AC1-d-r9/run_suite.sh reference.py seeds 0-49 in collect-only mode: 50 lines of '185 tests collected' (/tmp/AC1-v9/AC1-d/collect.out). Page line 368 says 185 and 'the count is 185 for each of the seeds 0 to 49': equal.")
row("proj-local-suite-reference", "2.6-autograder-local-run", "grader/test_project.py; project.html line 413 local command", "PASS",
    DELTA_OK + "run_suite.sh uses the page's flags (-q -p no:cacheprovider --assert=plain -W error) with QF_SEED=0: reference.py '185 passed in 0.13s'. The page's local command (line 413) is the same flag set.")
row("proj-pyodide-smoke", "2.6-autograder-pyodide", "course/modules/AC/AC1/project.html (labs 1-3, grader panel)", "PASS",
    DELTA_OK + "tools/page_smoke.py --unit AC1 --pages project -> 'in-browser grader: All 185 tests pass on seed 1565854548. (1.0 s)'; 'page_smoke modules/AC/AC1/project.html: PASS'; 'page_smoke AC1: PASS' (/tmp/AC1-v9/AC1-d/page_smoke.out).")
row("proj-check-pages", "2.9-structure", "course/modules/AC/AC1/*.html; cards.json", "PASS",
    DELTA_OK + "tools/check_pages.py --all -> 'check_pages AC1: PASS' (exit 0; /tmp/AC1-v9/AC1-d/check_pages.out).")
row("proj-check-projects", "2.6-hours-and-structure", "course/modules/AC/AC1/project.html (budget, rungs)", "PASS",
    DELTA_OK + "tools/check_projects.py --all -> 'check_projects AC1: PASS' (exit 0).")
row("proj-check-dag", "2.9-dag-concepts", "project.html 'Concepts used here'", "PASS",
    DELTA_OK + "tools/check_dag.py --all -> 'check_dag AC1: PASS' (exit 0). The Concepts item (project.html line 380) is unchanged since 2c8162b.")
row("proj-run-labs", "2.5-labs", "tests/labs/AC1/lab-AC1-project-1.py, -project-2.py, -project-3.py and the L01-L08 twins", "PASS",
    DELTA_OK + "tools/run_labs.py --unit AC1 -> 'run_labs AC1: PASS (11/11)'. Each of the 11 twins re-run as 'python -I -W error tests/labs/AC1/<twin>.py': exit 0 for all 11 (/tmp/AC1-v9/AC1-d/twin_*.out).")
row("proj-lab-twin-embed", "2.5-lab-embed-equals-twin", "project.html lab blocks 56-253 (Lab 1), 260-343 (Lab 2), 420-518 (Lab 3); tests/labs/AC1/lab-AC1-project-*.py", "PASS",
    DELTA_OK + "ledgers/AC1/scripts/AC1-d-r9/check_lab_embeds.py: lab-AC1-project-1 embedded==twin True and stdout==page expected True; lab-AC1-project-3 both True; lab-AC1-project-2 is the blanked template (four ___ blanks), so embedded!=twin by design, and its twin's stdout equals the page's expected block (True) (/tmp/AC1-v9/AC1-d/lab_embeds.out).")
row("proj-labs-ruff", "gate-ruff", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS",
    DELTA_OK + "ruff check course/modules/AC/AC1 tests/labs/AC1 -> 'All checks passed!'; ruff format --check -> '15 files already formatted' (/tmp/AC1-v9/AC1-d/ruff.out).")
row("proj-mypy-gate", "gate-mypy", "tests/labs/AC1; course/modules/AC/AC1/grader", "PASS",
    DELTA_OK + ".venv/bin/python -m mypy --no-incremental -> 'Success: no issues found in 153 source files', exit 0 (/tmp/AC1-v9/AC1-d/mypy.out).")
row("proj-verify-refs", "2.1-citations-tool", "references/references.json; project.html line 533 (data-cite penman2013financial)", "PASS",
    DELTA_OK + "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit AC1 (live) -> 'live re-verification of AC1: 2 of 560 entries, 0 problems' (exit 0). penman2013financial is at references/references.json line 18942 ('key': 'penman2013financial').")
row("proj-hours", "2.6-hours", "project.html line 35 (data-hours-project 30), time-budget rows (lines 390-398), total line 399; L01-L08 'study hours'; index.html data-hours-lessons=90", "PASS",
    DELTA_OK + "Time-budget rows 1+3+4+4+3+5+2+5+3 = 30 = the total on the page = data-hours-project 30. Lesson study hours 11+12+11+11+12+12+11+10 = 90 = index.html data-hours-lessons 90; 90+30 = 120, the figure on the hub. Arithmetic consistent; no pace judgement made (architect ruling on hours).")
row("proj-prose-banned", "2.9-banned-phrases", "project.html; cards.json; grader/test_project.py; L01-L08 changed passages", "PASS",
    DELTA_OK + "grep -i -E for 'roughly half|about 6%|historically|typically|usually|generally|ellipsis|…|builder|verifier|round [0-9]|unit report|REQUEST' over project.html, cards.json, test_project.py and L01-L08.html: no hit in project.html, cards.json or test_project.py. Out of slice, noted only: L07.html line 412 quiz distractor 'awards are typically forfeited at a stated rate' (a false option, not a claim). 'built' at project.html line 352 is 'cash flows built from net income'.")
row("proj-alt-implementations", "2.6-grader alternatives (ruling b)", "course/modules/AC/AC1/grader/test_project.py (whole suite)", "PASS",
    DELTA_OK + "Five correct alternatives, each run with run_suite.sh on seeds 0-49 (ledgers/AC1/scripts/AC1-d-r9/make_alternatives.py writes three; the two others are written by hand: /tmp/AC1-v9/AC1-d/alts2/alt_r9_d_bisect.py (bisect cutoffs, hand-written date parser, exact-type integer check) and alt_r9_e_snapshots.py (per-day snapshots, regex dates, calendar month ends)). Round-8 alternatives alt_r8_a/b/c: 50 of 50 seeds '185 passed'. alt_r9_d and alt_r9_e: 50 of 50 seeds '185 passed' (/tmp/AC1-v9/AC1-d/altsweep). No over-constraint found.")
row("proj-overconstraint-nonmapping", "2.6-over-constraint (ruling b)", "grader/test_project.py (post cases; the new round-8 cases at lines 452-464 and 469-479)", "PASS",
    DELTA_OK + "All five alternatives pass the new negative-credit and credits-above-debits cases (50 seeds). The three cases proposed in this round (rows proj-named-cond-*) are rejected by the reference and by alt_r9_d and alt_r9_e (/tmp/AC1-v9/AC1-d/alt_witness.out), so requiring them does not over-constrain the alternatives tested.")

# ---- mutants (ruling g) ----
for mid, text in [
    ("m01", "CFO receivables sign"), ("m02", "CFO omits the depreciation add-back"), ("m03", "dividends not deducted"),
    ("m04", "strict cutoff"), ("m05", "seed-0 cash hard-coded"), ("m06", "no month-end rule"), ("m07", "no negative-amount check"),
    ("m08", "leap-year February 28"), ("m09", "articulation all zero"), ("m10", "depreciation gap without the expense"),
    ("m11", "post changes its argument"), ("m12", "balance sheet cached"), ("m13", "statement prints"), ("m14", "dividends paid sign"),
    ("m15", "debit and credit on one line allowed"), ("m16", "line without a debit defaults to zero"), ("m17", "compact ISO dates accepted"),
    ("m18", "previous month end capped at 28"), ("m19", "articulation ignores dividends"), ("m20", "ending cash omits financing"),
    ("m21", "neither side accepted"), ("m22", "capex positive sign"), ("m23", "sales is balance not flow"), ("m24", "integral float accepted"),
    ("m25", "previous month minus 31 days"), ("m26", "payables increase sign reversed"), ("m27", "COGS from balance not flow"),
    ("m28", "timestamp truncated accepted"), ("m29", "boolean credit accepted"), ("m30", "whitespace date accepted"),
    ("m31", "account name case folded"), ("m32", "retained gap with dividends added"), ("m33", "total liabilities omits long-term debt"),
    ("m34", "net income omits depreciation"), ("m35", "working capital from balance not change"), ("m36", "beginning cash is period-end cash"),
    ("m37", "depreciation gap uses net equipment"), ("m38", "balance gap ignores equity"), ("m39", "account name whitespace stripped"),
    ("m40", "credit float accepted"), ("m41", "ISO week date accepted"), ("m42", "month end uses previous month length"),
    ("m43", "negative credit taken as absolute"), ("m44", "unbalanced only when debits exceed credits"),
]:
    pass

MUT_ROOT = "ledgers/AC1/mutants/"
mutants = []
import glob
for path in sorted(glob.glob(str(ROOT / "ledgers/AC1/mutants/m*.py"))):
    name = pathlib.Path(path).name
    mutants.append({"id": name[:3], "description": name[4:-3].replace("_", " "), "file": MUT_ROOT + name,
                    "killed_by": ""})
KILL = {
    "m43": "test_project.py::test_post_raises_a_value_error[a negative credit with no negative debit] (seed 0; also the boolean case); round-9 run",
    "m44": "test_project.py::test_post_raises_a_value_error[an unbalanced entry with credits above debits] (seed 0)",
}
for m in mutants:
    if m["id"] in KILL:
        m["killed_by"] = KILL[m["id"]]
    elif m["id"] in ("m45", "m46", "m47"):
        m["killed_by"] = ""
    else:
        m["killed_by"] = "killed on seed 0 (/tmp/AC1-v9/AC1-d/mutants_r9_run1.out)"
mutants = [m for m in mutants if m["id"] not in ("m45", "m46", "m47")] + [m for m in mutants if m["id"] in ("m45", "m46", "m47")]

import re as _re
_run = {}
for _line in open("/tmp/AC1-v9/AC1-d/mutants_r9_run1.out", encoding="utf-8"):
    _m = _re.match(r"(m\d\d)_\S+: KILLED seed (\d): (.*)", _line.strip())
    if _m:
        _run[_m.group(1)] = _m.group(3)[:150]
ROW_OF = {
    "m09": ("proj-mutant-m09-articulation-zero", "2.6-mutation", "ledgers/AC1/mutants/m09_articulation_all_zero.py"),
    "m10": ("proj-mutant-m10-depreciation-gap", "2.6-mutation", "ledgers/AC1/mutants/m10_depreciation_gap_no_expense.py"),
    "m26": ("proj-mutant-m26-payables-sign", "2.6-mutation (round 5 student error, re-run)", "ledgers/AC1/mutants/m26_payables_increase_sign_reversed.py"),
    "m27": ("proj-mutant-m27-cogs-from-balance", "2.6-mutation (round 5 student error, re-run)", "ledgers/AC1/mutants/m27_cogs_from_balance_not_flow.py"),
    "m28": ("proj-mutant-m28-timestamp-date-accepted", "2.6-mutation (round 5 FAIL, now killed)", "ledgers/AC1/mutants/m28_timestamp_truncated_accepted.py"),
    "m29": ("proj-mutant-m29-boolean-credit-accepted", "2.6-mutation (round 6 FAIL, now killed)", "ledgers/AC1/mutants/m29_boolean_credit_accepted.py"),
    "m30": ("proj-mutant-m30-whitespace-date-accepted", "2.6-mutation (round 6 FAIL, now killed)", "ledgers/AC1/mutants/m30_whitespace_date_accepted.py"),
    "m31": ("proj-mutant-m31-account-name-case-folded", "2.6-mutation (round 6 FAIL, now killed)", "ledgers/AC1/mutants/m31_account_name_case_folded.py"),
    "m32": ("proj-mutant-m32-retained-gap-sign", "2.6-mutation (round 6 student error)", "ledgers/AC1/mutants/m32_retained_gap_dividends_added.py"),
    "m39": ("proj-mutant-m39-account-name-whitespace-stripped", "2.6-mutation (round 7 FAIL, now killed)", "ledgers/AC1/mutants/m39_account_name_whitespace_stripped.py"),
    "m40": ("proj-mutant-m40-credit-float-accepted", "2.6-mutation (round 7 FAIL, now killed)", "ledgers/AC1/mutants/m40_credit_float_accepted.py"),
    "m41": ("proj-mutant-m41-week-date-accepted", "2.6-mutation (round 7 FAIL, now killed)", "ledgers/AC1/mutants/m41_week_date_accepted.py"),
    "m42": ("proj-mutant-m42-month-end-previous-length", "2.6-mutation (round 8 NEW student error)", "ledgers/AC1/mutants/m42_month_end_uses_previous_month_length.py"),
}
for _mid, (_rid, _check, _file) in ROW_OF.items():
    row(_rid, _check, _file + "; grader/test_project.py", "PASS",
        DELTA_OK + "Killed on seed 0 by the suite (mutants_r9_run1.out): " + _run[_mid])
row("proj-mutants-m01-m08", "2.6-mutation (round 2-3 set)", "ledgers/AC1/mutants/m01 to m08", "PASS",
    DELTA_OK + "run_mutants.sh over the mutants (seeds 0-4): m01-m08 KILLED on seed 0: " + "; ".join(f"{k} {_run[k][:60]}" for k in ["m01","m02","m03","m04","m05","m06","m07","m08"]) + " (/tmp/AC1-v9/AC1-d/mutants_r9_run1.out).")
row("proj-mutants-m11-m20", "2.6-mutation (round 2-3 set)", "ledgers/AC1/mutants/m11 to m20", "PASS",
    DELTA_OK + "All ten KILLED on seed 0 (mutants_r9_run1.out): " + "; ".join(f"{k} {_run[k][:60]}" for k in ["m11","m12","m13","m14","m15","m16","m17","m18","m19","m20"]) + ".")
row("proj-mutants-m21-m25", "2.6-mutation (round 4 set)", "ledgers/AC1/mutants/m21 to m25", "PASS",
    DELTA_OK + "All five KILLED on seed 0 (mutants_r9_run1.out): " + "; ".join(f"{k} {_run[k][:60]}" for k in ["m21","m22","m23","m24","m25"]) + ".")
row("proj-mutants-m33-m38", "2.6-mutation (round 7 student errors, re-run)", "ledgers/AC1/mutants/m33 to m38", "PASS",
    DELTA_OK + "All six KILLED on seed 0 (mutants_r9_run1.out): " + "; ".join(f"{k} {_run[k][:60]}" for k in ["m33","m34","m35","m36","m37","m38"]) + ".")
row("proj-mutant-m43-negative-credit-absolute", "2.6-mutation (round 8 FAIL, now killed)", "ledgers/AC1/mutants/m43_negative_credit_taken_as_absolute.py; grader/test_project.py case 'a negative credit with no negative debit' (line ~480)", "PASS",
    DELTA_OK + "Round-8 FAIL cured: the suite now has the case. Run on seed 0: 'FAILED test_post_raises_a_value_error[a negative credit with no negative debit-transactions24]' plus the boolean case; 2 failed, 183 passed (mutants_r9 run). KILLED.")
row("proj-mutant-m44-unbalanced-one-direction", "2.6-mutation (round 8 FAIL, now killed)", "ledgers/AC1/mutants/m44_unbalanced_only_when_debits_exceed_credits.py; grader/test_project.py case 'an unbalanced entry with credits above debits' (lines ~452-464 area)", "PASS",
    DELTA_OK + "Run on seed 0: 'FAILED test_post_raises_a_value_error[an unbalanced entry with credits above debits-transactions25]'; 1 failed, 184 passed. KILLED.")
row("proj-mutants-set-killed", "2.6-mutation (set, 47 mutants)", "ledgers/AC1/mutants/ (47 files)", "FAIL",
    DELTA_OK + "tools/mutate_graders.py --unit AC1 --seeds 0-9 -> 'mutate_graders AC1: FAIL (44/47 killed)'; SURVIVED: m45_negative_debit_clamped_to_zero, m46_strptime_date_accepts_unpadded, m47_numeric_string_amount_accepted (/tmp/AC1-v9/AC1-d/mutate_gate.out).",
    fix="Add the three cases proposed in rows proj-named-cond-*: a negative debit balanced by a positive credit; a date with an unpadded month ('2024-1-02'); an amount that is the numeric string '5'. Verified in scratch (/tmp/AC1-v9/AC1-d/fixtest): with them, the reference and alt_r9_d, alt_r9_e and the three round-8 alternatives all pass (188 passed), and m45, m46 and m47 each fail one case.")
row("proj-mutants-new-r9-three-written", "2.6-mutation (ruling g: at least three new, round 9)", "ledgers/AC1/mutants/m45 to m47", "PASS",
    DELTA_OK + "Round 9 wrote three new student-error mutants of its own, each a plausible student error: m45 clamps a negative debit to zero (max(0, x) style); m46 parses post dates with strptime and drops the padding check; m47 converts a numeric string amount with int(), as the lab code does. Each is a real survivor (rows proj-mutant-m45/m46/m47 are FAIL).")
row("proj-mutants-new-m26-m28", "2.6-mutation (ruling g, at least three new)", "ledgers/AC1/mutants/ m26-m28 (round 5), m29-m32 (round 6), m33-m41 (round 7), m42-m44 (round 8), m45-m47 (round 9)", "PASS",
    DELTA_OK + "Every round since the first has added its own student-error mutants; the count requirement (at least three new this round) is met by m45-m47. Survivorship is recorded per mutant.")
row("proj-mutant-m45-negative-debit-clamped", "2.6-mutation (NEW round 9, student error; spec-named condition 'a negative amount' not enforced for a debit)", "ledgers/AC1/mutants/m45_negative_debit_clamped_to_zero.py; grader/test_project.py post cases (lines ~307-480)", "FAIL",
    DELTA_OK + "Witness (/tmp/AC1-v9/AC1-d/witness_r9.out, python -I): post([{date 2024-01-02, lines [cash debit -5 credit 5], [common_stock debit 5 credit 0]}]): reference ValueError 'an amount must not be negative'; mutant accepted. run_suite.sh seeds 0-4: '185 passed' (SURVIVED).",
    fix="Add the case 'a negative debit balanced by a positive credit': lines [{account cash, debit -5, credit 5}, {account common_stock, debit 5, credit 0}] with SMALL[0] as the base; must_raise ValueError. Verified in scratch: reference and all alternatives raise it; the mutant fails it.")
row("proj-mutant-m46-unpadded-date-accepted", "2.6-mutation (NEW round 9, student error; spec-named condition 'a date that is not in the form YYYY-MM-DD' not enforced for post)", "ledgers/AC1/mutants/m46_strptime_date_accepts_unpadded.py; grader/test_project.py post date cases (lines ~315-322)", "FAIL",
    DELTA_OK + "Witness: post([{date '2024-1-5', ...}]): reference ValueError 'a date must be an ISO date, YYYY-MM-DD'; mutant accepted. Suite seeds 0-4: '185 passed' (SURVIVED). The unpadded form is tested only for period ends (test_period_end_must_be_a_month_end, '2024-1-31'), not for post dates.",
    fix="Add the case 'a date with an unpadded month': [{**SMALL[0], 'date': '2024-1-02'}] to the post parametrize list. Verified in scratch: reference and alt_r9_d, alt_r9_e, alt_r8_a/b/c all raise; m46 fails it.")
row("proj-mutant-m47-numeric-string-amount", "2.6-mutation (NEW round 9, student error; spec-named condition 'an amount that is not an integer' not enforced for strings)", "ledgers/AC1/mutants/m47_numeric_string_amount_accepted.py; grader/test_project.py amount cases (lines ~355-380)", "FAIL",
    DELTA_OK + "Witness: post([{... debit '5' ...}]): reference ValueError 'an amount must be an integer number of cents'; mutant accepted. Suite seeds 0-4: '185 passed' (SURVIVED). No test passes a string amount.",
    fix="Add the case 'an amount that is a numeric string': a line with debit '5' (a str) and the balancing credit as in the float case. Verified in scratch: reference and all alternatives raise; m47 fails it.")

# ---- page claims and spec ----
row("proj-page-spec-carry", "2.6-spec-named-errors and spec-enforced (ruling a)", "project.html line 366 (Constraints: 'Every named error condition raises ValueError ... The named conditions are these') and line 368; grader/test_project.py post cases", "FAIL",
    DELTA_OK + "The round-8 FAIL cases are cured: negative credit and unbalanced-with-credits-above-debits are now cases (m43, m44 killed). Three named conditions are still not enforced by the suite: (1) 'a negative amount' is only tested with debits that are also 'neither' or with negative credits, so a negative debit balanced by a positive credit is accepted (m45); (2) 'a date that is not in the form YYYY-MM-DD' is not tested for post dates in the unpadded form (m46); (3) 'an amount that is not an integer' is not tested for a string (m47). The page's claim that the suite covers 'each named error' (line 368) therefore overstates the suite.",
    fix="Add the three cases listed under proj-mutants-set-killed. Then either keep line 366 as it is (it then matches the suite) or, if the three are not added, weaken the claim. Do not weaken the spec itself.")
row("proj-page-spec-carry-post-cases", "2.6-spec-named-errors (post cases list)", "grader/test_project.py test_post_raises_a_value_error parametrize list (lines ~307-480)", "PASS",
    DELTA_OK + "The list has 26 cases (ids transactions0..transactions25). Read in full: every named condition except the three above has a case, and both directions of 'debit or credit, and exactly one' and of 'debits equal credits' are covered (cases 'a line with a debit and a credit', 'a line with neither', 'an unbalanced entry', 'an unbalanced entry with credits above debits').")
row("proj-balance-gap-sign-unenforced", "2.6-spec-claim (ruling a)", "project.html line 378 (Conventions, Articulation gaps)", "PASS",
    "Carried from round 8 (project.html line 378 is not in the 2c8162b..96dd532 hunks; diff hunks at lines 352 and 368 only): the sentence states that the suite does not test the sign of the always-zero balance_gap. test_articulation_gaps_are_zero and test_the_balance_sheet_balances check == 0 only; no test checks a reversed sign, so the claim is accurate.")
row("proj-scope-sentence-line-352", "2.9-prose (claim about the ledgers)", "course/modules/AC/AC1/project.html line 352 (Context)", "PASS",
    DELTA_OK + "Changed this round (the sentence 'The ledgers in the labs and the autograder's instance are labelled SIMULATED'). Checked: lab headers 'SIMULATED ledger' in Lab 1 (line 'SIMULATED ledger: ten transactions'), Lab 2 ('SIMULATED ledger: the ten transactions of Lab 1'), Lab 3 ('SIMULATED ledger for reference numbers'); instance.py make_instance returns 'label': 'SIMULATED' (verified for seeds 0-49). 'The labs' ledgers are written out by hand in the lab code': literal TRANSACTIONS (Lab 1), ENTRIES (Lab 2 and Lab 3) read in full.")
row("proj-conventions-debit-balance-sentence", "2.9-prose (line 373)", "course/modules/AC/AC1/project.html line 373 (Conventions, Balance through a date)", "PASS",
    "Carried from round 8 (project.html line 373 is not in the 2c8162b..96dd532 hunks): the sentence 'Assets other than accumulated depreciation have a normal debit balance, and so do dividends and expenses' agrees with the ACCOUNTS classes in starter.py and the reference (normal side = debit for asset, distribution, expense).")
row("proj-page-lab-carry", "2.5-labs (carry, re-run)", "project.html lines 56-253 (Lab 1), 260-343 (Lab 2), 420-518 (Lab 3); tests/labs/AC1/", "PASS",
    DELTA_OK + "run_labs AC1 11/11; check_lab_embeds.py as in proj-lab-twin-embed. Lab 1 and Lab 3 page expected output equals the twin's stdout (True). Lab 1 numbers rechecked by hand against the expected block: 22 postings from 10 entries; February sales 1,600,000, COGS 900,000, net income 700,000; operating -700,000 = 700,000 - 1,400,000 (receivables +200,000, inventory +900,000, payables -2,500,000); ending cash 4,800,000. Lab 3 by hand: net equipment 2,920,000, assets 7,870,000, liabilities 2,250,000, common stock 6,000,000, retained -380,000 (income 70,000 less dividends 450,000), investing -3,000,000, financing 850,000, ending cash 4,850,000.")
row("proj-page-ladder-browser-carry", "2.6/2.9 (carry)", "project.html lines 40-47, 51-52, 406, 414, 533, 548", "PASS",
    "Carried from round 8 (those project.html lines are not in the 2c8162b..96dd532 hunks). Checked again this round: pytest 9.0.2 is pinned in course/assets/vendor/LOCK.json (line 432, pyodide/pytest-9.0.2-py3-none-any.whl) and the local .venv has pytest 9.0.2 with Python 3.14.8, matching 'Use Python 3.14 and pytest 9.0'.")
row("proj-instances-carry", "2.6-instances", "course/modules/AC/AC1/grader/instance.py", "PASS",
    DELTA_OK + "instance.py byte-identical to 2c8162b (git diff). Invariants re-run this round with /tmp/AC1-v9/AC1-d/instance_check.py over seeds 0-49: 200 entries each, all dated 2024, every entry balances, every account in the chart, all amounts int, label 'SIMULATED', and no cash, receivable, inventory, net equipment, payable or debt balance below zero at any entry (0 violations).")
row("proj-grader-carry", "2.6-grader read", "grader/test_project.py (whole file, 710 lines)", "PASS",
    DELTA_OK + "Read in full this round (lines 1-710). Oracle (_through, _expected_*), SMALL hand-worked January values (balance sheet, cash flow) recomputed by hand, GAP_WITNESS values recomputed by hand (cash gap -100, depreciation gap -100). Messages name the property and never print expected values; _check_values and must_raise print no expected value. Import test allows only stdlib. Count 185 verified by collect.")
row("proj-line-368-grading-claims", "2.6-grading-claims", "project.html line 368; grader/test_project.py", "PASS",
    DELTA_OK + "'collects 185 checks' and 'the count is 185 for each of the seeds 0 to 49': verified (collect, seeds 0-49). The coverage list maps to test names: chart of accounts (test_chart_of_accounts_is_the_specified_table), stdlib (test_the_module_imports_only_the_standard_library), posting and each named error (test_post_raises_a_value_error), silence (test_the_functions_are_silent), statement values (test_*_matches_the_ledger), balance identity (test_the_balance_sheet_balances), cash tie (test_cash_flow_ends_at_the_balance_sheet_cash), net change in cash (test_net_change_in_cash_equals_the_cash_lines_of_the_month), retained earnings (test_retained_earnings_move_by_net_income_less_dividends), operating CF formula (test_operating_cash_flow_is_...), four gaps (test_articulation_gaps_are_zero), month-end rule (test_period_end_must_be_a_month_end), hand-worked January (test_small_ledger_january_*). The 'posting rules and each named error' item is the overstatement recorded in proj-page-spec-carry.")
row("proj-line-37-lede-seed", "2.6-lede", "course/modules/AC/AC1/project.html line 37 (lede) and the panel; local command at line 413", "PASS",
    "Carried from round 8 (project.html line 37 and line 413 are not in the 2c8162b..96dd532 hunks): the lede's 200-transaction ledger and the seed-generated instance match instance.py (COUNT = 200).")
row("proj-footer-nothing-leaves", "2.9-claim (footer)", "project.html footer ('nothing you write leaves it'); course/assets/js/grader.js, store.js, python.js, py-worker.js", "PASS",
    DELTA_OK + "grep -n for fetch(, XMLHttpRequest, sendBeacon, WebSocket, importScripts and https:// in course/assets/js/{grader,store,python,py-worker,lab}.js: one hit, grader.js line 18 'const response = await fetch(url)' inside text(url), which loads only the starter and suite files from the panel's relative grader path. Learner code is kept with indexedDB (store.js line 17); py-worker.js reports results with postMessage only. No outbound request of learner code found.")

row("proj-line-377-working-capital-terms", "2.9-prose (round-7 FAIL, now fixed in round 8)", "course/modules/AC/AC1/project.html line 377 (Cash flow statement, indirect method)", "PASS",
    "Carried from round 8 (project.html line 377 is not in the 2c8162b..96dd532 hunks, which are lines 352 and 368 only): the sentence 'those three terms, which are the cash effects of the changes in receivables, inventory and payables' agrees with the grader's cash_from_operations formula (test_operating_cash_flow_is_net_income_plus_add_backs_and_working_capital) and with reference.py.")
row("proj-line-378-missing-space", "2.9-html (round-7 FAIL, now fixed in round 8)", "course/modules/AC/AC1/project.html lines 378-379 (Articulation gaps item)", "PASS",
    "Carried from round 8 (project.html lines 378-379 not in the 2c8162b..96dd532 hunks): the balance_gap item ends at </li> and the cash_gap item starts a new <li>; nothing runs together.")

# ---- cards ----
row("cards-inventory-and-dupes", "2.7-cards", "course/modules/AC/AC1/cards.json (126 cards)", "PASS",
    DELTA_OK + "126 cards; ids AC1-c001..AC1-c126 contiguous, in order, unique; 0 duplicate fronts, 0 duplicate backs (python check).")
row("cards-grades", "2.3-grades", "cards.json grade and basis fields", "PASS",
    DELTA_OK + "Grades: 43 without a grade, 42 C, 41 T. Every C card has a basis and every basis belongs to a C card. Grades judged against the BLUEPRINT section 3 grade table (T = theorem proved on the page; C = single-sample or lab output, convention): T only where a proposition or theorem is proved on the page; C for lab outputs, conventions and 'not stated' answers.")
row("cards-numbers-in-lessons", "2.7-card-numbers", "cards.json; L01-L08 (tag-stripped text, /tmp/AC1-v9/AC1-d/txt/)", "PASS",
    DELTA_OK + "ledgers/AC1/scripts/AC1-d-r9/cards_numbers.py over all cards: every number on each card appears in its own lesson text, except AC1-c077's 5,000 whose lesson writes it as 5{,}000 in Definition 1.3 (L06 formula I_t = floor((L_{t-1} rho + 5{,}000) / 10{,}000)): not a missing number.")
row("cards-labels-resolve", "2.7-card-citations", "cards.json citations against each card's own lesson", "PASS",
    DELTA_OK + "Labels in the current lessons: Definition 1.3 (L01), Remark 2.2 (L01), Proposition 3.2 (L01, L02), Definition 1.2 (L03, L08), Theorem 5.1 (L03), Theorem 2.1 and Corollary 2.2 (L07), Definition 1.1 and 1.2 (L08), Proposition 4.2 (L02, L03), Definition 4.1 (L02), Remark 6.3 (L03), Proposition 6.2 (L03), Example 2.2 (L08). Each label exists in the card's own lesson text.")
row("cards-banned", "2.9-banned-phrases", "cards.json", "PASS",
    DELTA_OK + "grep on cards.json for the banned list and process words: no hits; no ellipsis.")
row("cards-registry-cites", "2.1-citations", "cards.json", "PASS",
    DELTA_OK + "grep -c data-cite cards.json -> 0; citations are lesson labels only.")
row("cards-c015", "2.7-card (L01 Remark 2.2 and Definition 1.1 changed this round)", "cards.json AC1-c015; L01.html Remark 2.2 (line 103) and Definition 1.1", "PASS",
    DELTA_OK + "L01 line 103 (Remark 2.2) now lists 'a non-negative integer number of cents with one side per line'; the card says 'The check tests that each entry balances and that its accounts exist (Remark 2.2). Definition 1.1 also requires non-negative integer cents and one side per line.' Agrees with both passages.")
row("cards-L01", "2.7-cards (c001-c007, c009-c016)", "cards.json c001-c007, c009-c016; L01.html", "PASS",
    DELTA_OK + "Read against the current L01 (Definitions 1.1-1.3, Proposition 2.1, Remark 2.2, Proposition 3.2, Example 3.3, Section 1 table). c008 (round-8 FAIL) now reads 'Recording a sale as revenue in the period in which it is made...' = Definition 1.3 (L01 line 'Accrual accounting records a sale as revenue in the period in which it is made'): PASS. c009, c011, c014: Lab 1 printed figures checked against the run (cash debits 255,314.48, credits 30,594.17, balance 224,720.31; sales 213,881.48; expense 49,831.40 less cash paid 30,594.17 = 19,237.23; closing receivable 38,567.00). c013 states the hypotheses (i)-(v) of Proposition 3.2 as the lesson does.")
row("cards-L01-claims-table-scope", "2.7-claims (L01 Key results, section 8)", "course/modules/AC/AC1/L01.html Key results (section 8)", "PASS",
    "Carried from round 8 (L01 Key results table is not in the 2c8162b..96dd532 hunks, which end at line 384-410 of L01 in Sections 3-4 and at line 103 in Remark 2.2): the table row 'A balanced entry posted to the wrong account passes the check (Remark 2.2)' is consistent with the changed Remark 2.2.")
row("cards-L02", "2.7-cards (c017-c032)", "cards.json c017-c032; L02.html", "PASS",
    DELTA_OK + "L02 changes read: Definition 2.1 (D = depreciation expense; c022 says 'D for depreciation': consistent), Proposition 2.2 with its hypothesis (c028 states the identity for the lab's four income accounts: consistent), Proposition 3.2 proof wording (c029 'for any ledger... and for any year end': consistent), Section 6 'at every year end' (c027 consistent). c025, c026, c031 figures match Lab 2 run (NI 1,003,421.14; operating 1,654,305.29; cash 3,000,000.00 -> 4,454,305.29; RE 803,421.14 = NI less dividends 200,000.00). c032 (changed this round) agrees with Definition 4.1 and the Key results row 'what any reporting framework requires for this split is not stated here'.")
row("cards-L03", "2.7-cards (c033-c039, c041-c045, c124 excluded)", "cards.json c033-c039, c041-c045; L03.html", "PASS",
    DELTA_OK + "Read against the current L03: Definitions 1.1, 1.2, 2.1; Proposition 2.2 (c039 'proves it for the lab's operating activity'; hypotheses (i)-(v) hold for the lab's ledger, scope given); Proposition 4.1; Theorem 5.1 (c038, c042: lab scope and 'Theorem 5.1 proves...'); Proposition 6.2 (c036, c037, c043). c036/c037 figures (1,500,000.00 investing; add-back 1,300,000.00; CFO 2,191,615.64) match Lab 3 output. c044 (1,000,000.00, 2,300,000.00, 3,600,000.00) matches Lab 3 Check 5. c045 matches Remark 6.3 ('changes the charge in every quarter, including the first').")
row("cards-c040-investing-scope", "2.7-card-scope (Proposition 3.1 hypotheses added this round)", "cards.json AC1-c040 (grade T, L03); L03.html Proposition 3.1 (line 92)", "FAIL",
    DELTA_OK + "Proposition 3.1 now states hypotheses (i) to (iv) and 'in the lab's ledger'. The card asserts without scope or hypotheses that 'Investing cash flow equals minus the change in equipment at cost (Proposition 3.1)'. The claim is false outside the hypotheses (for example, a credit to equipment or a non-equipment investing line), so the card drops a condition its cited proposition states (the same class as the round-8 FAIL on AC1-c102).",
    fix="Rewrite AC1-c040 back as: 'In the lab's ledger, under the hypotheses of Proposition 3.1, investing cash flow equals minus the change in equipment at cost (Proposition 3.1).' Keep grade T.")
row("cards-c124-financing-scope", "2.7-card-scope (Proposition 3.1 hypotheses added this round)", "cards.json AC1-c124 (grade T, L03); L03.html Proposition 3.1", "FAIL",
    DELTA_OK + "AC1-c124 asserts 'Financing cash flow equals the change in long-term debt plus the change in common stock, minus dividends paid (Proposition 3.1)' with no scope. Proposition 3.1 (iii) requires that common stock and long-term debt have no debits and are credited only by owner investments and borrowings, and (ii) names the only financing lines. The card omits both, so it states more than the proposition proves.",
    fix="Rewrite AC1-c124 as: 'In the lab's ledger, under the hypotheses of Proposition 3.1, financing cash flow equals the change in long-term debt plus the change in common stock, minus dividends paid (Proposition 3.1).' Keep grade T.")
row("cards-c126-straight-line", "2.7-card (L03 Definition 1.2 wording)", "cards.json AC1-c126 (grade C, L03); L03.html Definition 1.2 and Remark 6.3", "PASS",
    DELTA_OK + "Card: an equal amount for each quarter of the life, so cost less any residual value is spread evenly; the lab's assets have no residual value (Definition 1.2). Definition 1.2 (L03 line 62) says the same, with the residual value parenthetical added this round. Consistent.")
row("cards-L03-c123", "2.3-theorem-proof", "cards.json AC1-c123 (grade T); L03.html Proposition 4.2 and its proof", "PASS",
    DELTA_OK + "Card hypotheses (no entry credits equipment at cost; no entry debits accumulated depreciation; every credit to accumulated depreciation is a depreciation entry) are exactly Proposition 4.2 (i)-(iii); the card's conclusion (net equipment rolls forward by additions less depreciation) matches the statement and proof. Lab 3 Check 3 prints True for every year.")
row("cards-L03-theorem-5-1-print-claim", "2.5-lab-print-claim", "course/modules/AC/AC1/L03.html Theorem 5.1 paragraph; tests/labs/AC1/lab-AC1-L03-1.py", "PASS",
    DELTA_OK + "lab-AC1-L03-1.py under python -I -W error: exit 0, output read in full. Check 1 prints the gap 0.00 at each year end; Checks 2, 3 and 4 print True (indirect equals direct: True; roll-forwards True; cash to balance sheet True); Check 5 and Check 6 are not named in the paragraph. The paragraph's statement matches.")
row("cards-L03-theorem-5-1-print-claim-hypotheses", "2.4-theorem-hypotheses", "L03.html Theorem 5.1 hypotheses (new this round)", "PASS",
    DELTA_OK + "Theorem 5.1's hypotheses name Propositions 2.2, 3.1, 4.2 and Proposition 3.2 of Lesson 2 with the only-equity-accounts hypothesis; the lab's ledger satisfies them (lab output: all checks True). The card AC1-c042 uses the lab scope 'in every fiscal year of the lab's ledger', which covers them.")
row("cards-L04", "2.7-cards (c046-c060, c122)", "cards.json c046-c060, c122; L04.html", "PASS",
    "Carried from round 8 (L04.html and cards c046-c060, c122 byte-identical since 2c8162b; not in the diff): same text. lab-AC1-L04-1.py re-run under python -I -W error: exit 0.")
row("cards-L05", "2.7-cards (c061-c074)", "cards.json c061-c074; L05.html", "PASS",
    "Carried from round 8 (L05.html and cards c061-c074 byte-identical since 2c8162b): same text. lab-AC1-L05-1.py re-run under python -I -W error: exit 0.")
row("cards-L06", "2.7-cards (c075-c090)", "cards.json c075-c090; L06.html", "PASS",
    "Carried from round 8 (L06.html and cards c075-c090 byte-identical since 2c8162b): same text. lab-AC1-L06-1.py re-run under python -I -W error: exit 0. c077's 5,000 is 5{,}000 in the lesson (see cards-numbers-in-lessons).")
row("cards-L07", "2.7-cards (c091-c101, c103-c104)", "cards.json c091-c101, c103, c104; L07.html", "PASS",
    DELTA_OK + "L07 changed this round at Definition 1.1 ('a whole number of shares'), Definition 1.2 (assumptions wording), the Corollary 2.2 display and the Section 2 exercises. Cards read against the current text: c091-c093 (Section 1), c094 (Definition 1.1 formula), c095 (Definition 1.2 (i)-(v)), c096 (Theorem 1.3), c097 (Theorem 2.1 (a)), c099/c100 (Lab 1 figures 4/4, 6/6, year 3 57,822.92 with all four grants vesting: checked against the grant lines G1-G4 and the table), c101 and c103/c104 (Definition 1.1 and Theorem 1.3 nonnegativity).")
row("cards-c098-citation", "2.7-card-scope", "cards.json AC1-c098 (L07); Theorem 2.1 (c) and (d); Corollary 2.2", "PASS",
    DELTA_OK + "Card: 'Holding operating income fixed, a change in the expense moves net income and APIC in opposite directions by the same amount, and leaves equity and cash unchanged (Corollary 2.2). The change in total equity equals operating income (Theorem 2.1 (c))'. Corollary 2.2 text: 'Under the model, holding OI_t fixed, a change in S_t moves RE and APIC in opposite directions by the same amount, and leaves Equity and Cash unchanged'. Theorem 2.1 (c): APIC + RE change = OI_t. Agrees.")
row("cards-c102-equity-wording", "2.7-card-scope (round-8 FAIL, now fixed)", "cards.json AC1-c102 (grade T); L07.html Corollary 2.2", "PASS",
    DELTA_OK + "Round-8 FAIL cured: the card now reads 'No. Holding operating income fixed, cash is unchanged, but net income falls by the expense, retained earnings fall and APIC rises by the same amount, so total equity is unchanged (Corollary 2.2).' This is the Corollary's scope; the Misconceptions item uses the same scope.")
row("cards-L08", "2.7-cards (c105-c108, c110-c121, c125)", "cards.json c105-c108, c110-c121, c125; L08.html", "PASS",
    DELTA_OK + "Read against the current L08 (Definitions 1.1, 1.2; Theorems 1.3, 2.1; Example 1.4, Example 2.2; Lab 1; Misconceptions; M2, M3). Numbers: DTL 2,942.10 in years 2 and 3 with K 14,010.00 (Lab 1 table, seed 20260702), zero at year 5; Example 2.2 CT_1 6,300, TE_1 10,500, DE_1 4,200. c121 says faster tax depreciation lowers current tax and raises the deferred balance by the same amount: the Misconceptions item states exactly that, citing Theorem 2.1 (a) and (b); the card cites only (b), an incomplete citation but a true claim (PASS). c115/c125 match Theorem 2.1 (c) and (d).")
row("cards-c109-scope", "2.7-card-scope (round-8 FAIL, now fixed)", "cards.json AC1-c109 (L08); L08.html Definition 1.2", "PASS",
    DELTA_OK + "Round-8 FAIL cured: Definition 1.2 reads 'In this model, a positive balance is a liability, and a negative balance is an asset.' The card now says 'In this model, a positive balance is a liability and a negative balance is an asset (Definition 1.2).' Agrees.")
row("cards-c008-wording", "2.7-card-lesson agreement (L01 Definition 1.3)", "cards.json AC1-c008 (L01); L01.html Definition 1.3", "PASS",
    DELTA_OK + "Round-8 FAIL cured: the card now reads 'Recording a sale as revenue in the period in which it is made, and a cost as an expense in the period in which it is incurred, whether or not cash has moved...' which is Definition 1.3's wording.")
row("cards-c057", "2.7-card", "cards.json AC1-c057 (L04); L04 Remark 1.2 and Section 4", "PASS",
    "Carried from round 8 (L04.html and c057 byte-identical since 2c8162b): same text.")
row("cards-c069", "2.7-card", "cards.json AC1-c069 (L05); L05 Section 2 and problem P3", "PASS",
    "Carried from round 8 (L05.html and c069 byte-identical since 2c8162b): same text.")
row("cards-c071", "2.7-card", "cards.json AC1-c071 (L05); L05 Section 3", "PASS",
    "Carried from round 8 (L05.html and c071 byte-identical since 2c8162b): same text.")
row("cards-c079", "2.7-card", "cards.json AC1-c079 (L06); L06 Definition 1.4", "PASS",
    "Carried from round 8 (L06.html and c079 byte-identical since 2c8162b): same text.")
row("cards-c087", "2.7-card", "cards.json AC1-c087 (L06); L06 Section 3", "PASS",
    "Carried from round 8 (L06.html and c087 byte-identical since 2c8162b): same text.")
row("cards-c104", "2.7-card", "cards.json AC1-c104 (L07); L07 Definition 1.1 and Theorem 1.3", "PASS",
    DELTA_OK + "Read against the new Definition 1.1 (n_g >= 0, f_g >= 0, v_g >= 1): each yearly amount is floor(C/v) >= 0 or C - (v-1)floor(C/v) >= floor(C/v) >= 0, and the amounts sum to C (Theorem 1.3), so no year exceeds the total.")
row("cards-c052", "2.7-card", "cards.json AC1-c052 (L04); L04 Proposition 2.1", "PASS",
    "Carried from round 8 (L04.html and c052 byte-identical since 2c8162b): same text.")
row("cards-c013-scope", "2.7-card-scope", "cards.json AC1-c013 (L01); L01 Proposition 3.2", "PASS",
    DELTA_OK + "Card states the hypotheses (i)-(v) and the lab-free statement 'holds for any opening balances', which Proposition 3.2 and its paragraph state. L01 changed at the Section 3 introduction, which now says 'Under the hypotheses of Proposition 3.2' (consistent with the card).")
row("cards-c088-scope", "2.7-card-scope", "cards.json AC1-c088 (L06); L06 Lab 1 figures and Proposition 2.3", "PASS",
    "Carried from round 8 (L06.html and c088 byte-identical since 2c8162b): same text.")
row("cards-c018-wording", "2.7-card", "cards.json AC1-c018 (L02); L02 Definition 1.1", "PASS",
    DELTA_OK + "Definition 1.1 (flow and stock) unchanged; card matches it.")
row("cards-c059-c060-c070-c090", "2.7-card numbers", "cards.json AC1-c059, c060, c070, c090 (L04, L05, L06)", "PASS",
    "Carried from round 8 (L04-L06 and these cards byte-identical since 2c8162b): lab-AC1-L04-1, L05-1, L06-1 re-run exit 0.")
row("proj-cards-c001-c126-coverage", "2.7-coverage", "cards.json (all 126 cards)", "PASS",
    DELTA_OK + "Every card is accounted for in the rows: L01 cards by cards-L01/cards-c008-wording/cards-c015; L02 by cards-L02; L03 by cards-L03, cards-c040-investing-scope, cards-c124-financing-scope, cards-L03-c123, cards-c126-straight-line; L04 and L05 and L06 by carried rows; L07 by cards-L07, cards-c098-citation, cards-c102-equity-wording, cards-c104; L08 by cards-L08, cards-c109-scope; c122 by cards-L04 and c125 by cards-L08.")

# ---- structure ----
fragment = {
    "unit": "AC1",
    "slice": "AC1-d",
    "round": 9,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 9; did not build AC1; the round-8 fragment was read as context; every round-8 non-PASS row was re-verified; every row whose subject changed was re-read; PASS rows carried only where the cited subject is byte-identical to 2c8162b",
    "pin": "96dd532 (detached worktree /tmp/verify9-AC1-d); previous pin 2c8162b (round 8)",
    "base": "2c8162b (round 8 pin); delta is 96dd532 hunks in project.html (lines 352, 368), grader/test_project.py (two post cases), cards.json (c008, c032, c102, c109), L01, L02, L03, L07, L08 lessons",
    "previous_ledger": "/tmp/fanout-frags/AC1-d.round8.json",
    "checkout": "/tmp/verify9-AC1-d",
    "scratch": "/tmp/AC1-v9/AC1-d/",
    "verified_at": "2026-10-28T05:20:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Mutants are in ledgers/AC1/mutants/ (m01-m44 copied unchanged from the round-8 checkout; m45-m47 written this round). "
        "Scripts: ledgers/AC1/scripts/AC1-d-r9/ (run_suite.sh, run_mutants.sh, make_alternatives.py, cards_numbers.py, check_lab_embeds.py, make_fragment.py). "
        "Hand-written alternatives: /tmp/AC1-v9/AC1-d/alts2/alt_r9_d_bisect.py and alt_r9_e_snapshots.py. "
        "Proposed fix tested in scratch only (/tmp/AC1-v9/AC1-d/fixtest): not applied to the course (verifiers do not fix)."
    ),
    "summary": {},
}
statuses = [r["status"] for r in rows]
fragment["summary"] = {
    "rows": len(rows),
    "PASS": statuses.count("PASS"),
    "FAIL": statuses.count("FAIL"),
    "UNVERIFIABLE": statuses.count("UNVERIFIABLE"),
    "mutants": len(mutants),
    "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
    "mutants_survived": [m["id"] for m in mutants if not m["killed_by"]],
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT, fragment["summary"])
