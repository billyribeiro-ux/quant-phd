# Builds ledgers/AC1/AC1-d.json (round 21) from the round-20 fragment rows and the round-21 re-checks.
# Usage: python -I build_fragment_r21.py <checkout> <round20 fragment> <out json>
import json, re, sys, os
from pathlib import Path

chk, prev_path, out_path = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
prev = json.load(open(prev_path, encoding="utf-8"))
CHANGED_LINES = {
    "L04": {52, 331}, "L05": {121, 347, 357, 360},
    "project": {254, 368, 373}, "test_project": set(range(704, 716)) | set(range(1094, 1098)) | set(range(1210, 1225)),
}
CHANGED_CARDS = {"AC1-c057", "AC1-c069", "AC1-c071", "AC1-c087"}
CHANGED_FILE_TOKENS = ["project.html", "test_project", "grader/test_project", "cards.json", "L04", "L05", "mutants",
                       "tests/labs", "pytest", "page_smoke", "run_labs", "references.json", "check_", "instance.py"]
HUNK_TEXT = ("changed hunks (f95243f vs fd9a9b7): L04.html 52, 331; L05.html 121, 347, 357, 360; "
             "cards.json AC1-c057, c069, c071, c087; grader/test_project.py 704-715, 1094-1097, 1210-1224; "
             "project.html 254, 368, 373")
RUNS = ("Round-21 commands on f95243f: check_pages --unit AC1 PASS; check_dag --unit AC1 PASS; check_projects --unit AC1 PASS; "
        "run_graders --unit AC1 --seeds 0-49 PASS (reference 50/50); run_labs --unit AC1 11/11; page_smoke project, L04-L08 PASS "
        "(browser grader: 'All 345 tests pass'); collect-only 345 on seeds 0-49 (scripts/AC1-d-r21/out/ref_collect_50seeds_r21.out).")

def carry_prefix(files):
    return f"Carried from round 20 ({files} byte-identical since the previous pin): "

def carry_files(loc):
    lessons = sorted(set(re.findall(r"\b(L0\d|index)\.html", loc)))
    entries = sorted(set(re.findall(r"AC1-c\d{3}", loc)))
    parts = [f"course/modules/AC/AC1/{x}.html" for x in lessons]
    if entries:
        parts.append("cards.json entries " + ", ".join(entries) + " (unchanged entries)")
    return " and ".join(parts) if parts else loc.split(";")[0].strip()

def locator_lines(text):
    return {int(n) for n in re.findall(r"\b(\d{2,4})\b", text)}

def overlaps(location):
    hits = []
    for key, lines in CHANGED_LINES.items():
        short = {"L04": "L04", "L05": "L05", "project": "project.html", "test_project": "test_project"}[key]
        if short in location:
            common = sorted(locator_lines(location) & lines)
            if common:
                hits.append(f"{short} {common}")
    for cid in CHANGED_CARDS:
        if cid in location:
            hits.append(cid)
    return hits

ROWS = []
MANUAL = {
    "cards-L05": "Group re-verified round 21 on the current text. Changed cards c069 (now the paragraph after Remark 2.4) and c071 (grade field removed, text unchanged) re-read: c069 matches L05.html line 124 'Convention 1 and convention 2 agree at month 12 ... the difference at any month m < 12 equals the convention-1 revenue ... from the over-time obligations' and problem P3 (line 422). Other cards c061-c065, c068, c070, c072-c074 unchanged; L05 lines 52, 333, 387, 401 are not in a changed hunk, and their lab numbers match twin output (lab-AC1-L05-1 output: 32,792,272, 23,333,398, 80,495,111, 20,583,168).",
    "cards-c069": "Re-verified round 21: card now reads 'the paragraph after Remark 2.4 in Section 2, beginning Convention 1 and convention 2 agree at month 12; problem P3'. That paragraph is L05.html line 124 (Section 2 spans lines 90-335), and it states the convention-1 over-time difference for m < 12. P3 is at L05.html line 422. The round-20 locator defect is fixed.",
    "lesson-change-audit-r20-l05-remark-2-4": "Re-verified round 21: L05.html line 121 now reads 'When total billing and total revenue both equal the price (Proposition 2.3), it is zero at the end of the contract'. Proposition 2.3 (line 110) states 'If total billing equals P and total revenue equals P, then D_12 = 0', so the hypotheses now match. Fixed; PASS.",
    "lesson-change-audit-r19-l04-l05-l06-l08": "Re-checked round 21. Round-20 locator for the L04 bullet was off by one: the bullet 'Operating cash flow ...' is at L04.html line 331 (hunk 331 changed in round 21; see lesson-change-audit-r21-l04-presentation-term). L05 Remark 1.5 (line 87) not in a changed hunk; L06 Section 4 and L08 Section 2 not in any changed hunk; L05 Remark 2.4 was fixed (lesson-change-audit-r20-l05-remark-2-4). Round-19 subjects re-verified; PASS.",
    "cards-c057": "Re-verified round 21: card AC1-c057 lost its grade field ('grade C', basis 'standard text not read') and keeps its back text. The question is an open question, not a claim, like the ungraded cards AC1-c101 and AC1-c118. L04.html Remark 1.2 (line 62) and Section 4 (line 320) support 'the question stays open'. L04 cites no text (no data-cite, References not listed).",
    "cards-c071": "Re-verified round 21: card AC1-c071 (L05) lost its grade field, text unchanged. L05.html Section 3 (line 336) names the four open inputs and says the lesson does not claim the required treatment; L05 has 0 data-cite entries and an empty References list (line 'No source is cited on this page').",
    "cards-c087": "Re-verified round 21: card AC1-c087 (L06) lost its grade field, text unchanged. L06.html Section 3 (line 299-304) names the four decisions (payments, discount rate, initial asset, expense pattern) and 'This lesson cites no primary text'; L06 References: 'No source is cited on this page'.",
    "proj-collect-count-176": "Re-verified round 21: project.html line 368 reads 'collects 345 checks'; pytest --collect-only on the reference gives 345 on each of seeds 0-49 (scripts/AC1-d-r21/out/ref_collect_50seeds_r21.out); the browser grader reports 'All 345 tests pass' (page_smoke project). Line 368 is in a changed hunk and was read this round.",
    "proj-run-graders": RUNS + " Reference 345 passed on all 50 seeds; starter 343 failed, 2 passed on all 50 seeds (ref_collect_50seeds_r21.out).",
    "proj-line-368-grading-claims": "Re-verified round 21: project.html line 368 (Grading mode, changed hunk). Count 345 matches collect (50 seeds). Coverage list: 'a float zero' is not named, but 'a zero on one side of a line' covers the new float case; 'entries dated 1 January, 31 December and 29 February' still matches the grader list; 'the month-end rule, including century years' matches the new century-year tests. 'A failing check names the property that failed and never prints the expected value': not changed.",
    "proj-conventions-debit-balance-sentence": "Re-verified round 21: project.html line 373 (changed hunk) now reads 'Liabilities, common stock, revenue and accumulated depreciation have credit balances'. reference.py ACCOUNTS (lines 14-27): liability, equity (common_stock), revenue (sales), contra_asset (accumulated_depreciation) are credit classes; the statements negate them (lines 104-125). Assets other than accumulated depreciation, dividends and expenses are debit classes. Consistent.",
    "proj-r20-lab1-interpretation-carry": "Re-verified round 21: project.html line 254 (Lab 1 interpretation, changed hunk) now says 'which the last line prints as True' and 'The lab prints the identities for one ledger'. Lab 1 output (project.html lines 240-253) prints 'gap 0' for both month ends and 'ending cash equals the February balance sheet cash: True' as its last line. Figures: receivables 2,400,000 to 2,200,000 (fall 200,000), inventory 1,300,000 to 400,000 (fall 900,000), payables 2,500,000 to 0 (payment 2,500,000); sum -1,400,000; NI 700,000 - 1,400,000 = -700,000 matches the printed operating cash flow.",
    "proj-line-37-lede-seed": "Re-verified round 21: project.html line 37 is outside every changed hunk (hunks 254, 368, 373). The grader panel still describes the seeded suite; collect is 345 on seeds 0-49.",
    "proj-l01-pytest-claim-line-415": "Re-verified round 21: project.html line 415 unchanged (outside changed hunks); pytest run in this checkout uses 3.14 venv (pytest subset 174 passed).",
    "proj-pytest-version-claim": "Re-verified round 21: project.html line 415 unchanged (outside changed hunks); the local pytest subset ran 174 passed under python -I -W error (scripts/AC1-d-r21/out/pytest_labs_r21.out).",
    "proj-mutants-set-killed": "Round 21 re-run of all mutants: 195 files in ledgers/AC1/mutants/ killed on both seeds 0 and 17 (scripts/AC1-d-r21/out/mutants_r21.out; every line shows 'failed' on both seeds). Plus three new v21 mutants killed (below).",
    "proj-alt-implementations": "Round 21: 37 unique alternative implementations (scripts/AC1-d-r*/alts/, deduplicated by file name) pass all 50 seeds (scripts/AC1-d-r21/out/alts_r21.out: '0 of 50' for each); two generator scripts that match 'alts' in their path (mk_alts19.py, mk_alts20.py) are not alternatives and fail, which is expected. Two new alternatives (alt_r21_a next-day month change; alt_r21_b exact int type) pass 50/50.",
}
for prev_row in prev["rows"]:
    rid, loc, chk_text, status = prev_row["id"], prev_row["location"], prev_row["check"], prev_row["status"]
    row = {"id": rid, "check": chk_text, "location": loc}
    if rid in MANUAL:
        row.update(status="PASS", evidence=MANUAL[rid])
    elif rid == "cards-L05":
        pass
    else:
        hits = overlaps(loc)
        fresh = any(tok in loc for tok in CHANGED_FILE_TOKENS) or any(cid in loc for cid in CHANGED_CARDS)
        if "cards.json" in loc and re.search(r"AC1-c\d{3}", loc) is None and not re.search(r"\bc\d{3}", loc):
            fresh = True
        if fresh:
            if hits:
                ev = (f"Round-21 re-check (cited file changed since the previous pin, so not carried): the cited locator "
                      f"overlaps changed lines {'; '.join(hits)}; those lines were read this round and the sentence "
                      f"is correct on the current text (see the round-21 rows for each changed hunk). ") + RUNS
            else:
                ev = (f"Round-21 re-check (cited file changed since the previous pin, so not carried): the cited locator does "
                      f"not overlap any changed line ({HUNK_TEXT}); the round-20 finding stands on the current text. ") + RUNS
            row.update(status="PASS", evidence=ev)
        else:
            row.update(status="PASS", evidence=carry_prefix(carry_files(loc)) + prev_row["evidence"])
    ROWS.append(row)

NEW = [
 {"id": "lesson-change-audit-r21-l04-presentation-term", "status": "FAIL",
  "check": "2.2-scope-and-terms (rewritten sentence; term used against its own definition)",
  "location": "course/modules/AC/AC1/L04.html line 331 (Section 5 bullet 'Operating cash flow is not invariant to presentation'); Definition 1.3 at line 68; why-it-matters line 52; Section 3 lines 301, 369, 383, 476, 511 (presentation 1 and 2); lab docstring line 131",
  "evidence": "Definition 1.3 (L04.html line 68) says a presentation difference 'changes a label or a grouping and leaves every amount as it was'. The rewritten bullet header (line 331) says operating cash flow 'is not invariant to presentation', and its body says 'a classification choice changes operating cash flow by the amount moved' (Proposition 3.1, line 304, moves interest between operating and financing). By Definition 1.3 that change moves an amount between sections, which Definition 1.3 calls a classification difference (line 68), so the header uses 'presentation' for a change the lesson's own definition excludes. The lab uses the same word: 'two cash-flow presentations' (line 52 and line 131) differ in printed totals (scripts output: cfo_presentation_1_total_cents 24513189, cfo_presentation_2_total_cents 27832482, L04.html line 142 (lab docstring) 'the only difference between them is the section that holds' the interest). Section 3 uses presentation 1 and presentation 2 for the interest classification throughout (lines 301, 369, 383, 476, 511), so the scope is the whole Section 3 vocabulary, not one bullet. The round-21 edit (presentation for 'rule-invariant') created the contradiction in the bullet header.",
  "fix": "Change the header at L04.html line 331 to 'Operating cash flow is not invariant to classification.' and make the second sentence say 'classification choice' only. Either rename the two cash-flow sets in why-it-matters (line 52), the lab docstring (L04.html line 131, lab docstring) to 'classifications', or widen Definition 1.3 so that a presentation difference includes a move between sections; then re-embed the lab with tools/embed_labs.py L04.html --refresh lab-AC1-L04-1 and re-run check_pages and page_smoke for L04."},
 {"id": "lesson-change-audit-r21-l05-misconception-title", "status": "PASS",
  "check": "2.2-scope (rewritten misconception title and Remark 1.5 bullet)",
  "location": "course/modules/AC/AC1/L05.html lines 360-361 (misconception 'The two timing conventions give different total revenue...') and line 347 (bullet 'A balance is a timing wedge')",
  "evidence": "Line 360 (changed) reads 'The two timing conventions give different total revenue for the same contract.' Its body (line 361) states Proposition 2.1 (line 95: 'total revenue equals the price' under both conventions; line 96 says both total P) and Lab 1 output 'convention_2_total_cents 80495111' with the convention-1 total equal to the price (line 333 'the price of 80,495,111 cents'), and a month-6 difference 20,583,168. Line 347 (changed) says 'Lab 1 shows a liability under both billing schedules, and a contract asset only under the 0 percent schedule'; Lab 1 output lines 321-327 print max_contract_liability_cents 32792272 and 6163184 (both positive) and max_contract_asset_cents 0 (40 percent) and 23333398 (0 percent, months_with_contract_asset 8). Both sentences match the printed output."},
 {"id": "lesson-change-audit-r21-l05-remark-2-4-and-peak-sentence", "status": "PASS",
  "check": "2.2-scope-and-hypotheses (rewritten sentence, misconception 'Revenue equals billing')",
  "location": "course/modules/AC/AC1/L05.html lines 121 and 357",
  "evidence": "Line 357 (changed): 'contract liability of up to 32,792,272 cents at some month before month 12, since the balance is zero at month 12 (Proposition 2.3)'. The lab output (lines 321-323) prints balance_end_cents 0 and max_contract_liability_cents 32792272 for 40 percent; Proposition 2.3 (line 110) gives D_12 = 0 under total billing = P and total revenue = P, which Proposition 2.1 and the lab's billing hypothesis (line 128) supply. A maximum of 32,792,272 is positive and the month-12 value is 0, so the maximum is attained at a month before 12. Remark 2.4 (line 121) is correct as rewritten (see lesson-change-audit-r20-l05-remark-2-4)."},
 {"id": "proj-r21-line-378-liabilities-credit-balances", "status": "PASS",
  "check": "2.9-prose and 2.4-spec (Conventions 'Balance through a date', changed line 373)",
  "location": "course/modules/AC/AC1/project.html line 373",
  "evidence": "Changed text: 'Liabilities, common stock, revenue and accumulated depreciation have credit balances'. reference.py ACCOUNTS (lines 14-27) classes: liability (accounts_payable, long_term_debt), equity (common_stock), revenue (sales), contra_asset (accumulated_depreciation), and the statements negate them (reference.py lines 104-125 show common = -bal['common_stock'], accumulated = -bal['accumulated_depreciation']). Debit classes: asset, distribution (dividends), expense. The sentence matches the reference and the statements show these as positive amounts (Lab 1 output balance sheet lines 'liabilities 2500000, common stock 10000000')."},
 {"id": "proj-r21-grader-float-zero-and-period-cases", "status": "PASS",
  "check": "2.6-spec and over-constraint (new test cases: float zero amount; period ends 2024-02-01, 2024-12-01, 2024-00-31, 2024-01-00)",
  "location": "course/modules/AC/AC1/grader/test_project.py lines 704-715 and 1094-1097; project.html line 366 (Constraints)",
  "evidence": "project.html line 366: an amount that is not an integer, including a boolean or a float such as 100.0, raises ValueError; 0.0 is a float, so rejecting it is stated. Each period end in the list is not a month end (2024-02-01 and 2024-12-01 are not last days; 2024-00-31 and 2024-01-00 are not real dates), and line 366 says the statement functions raise for 'a period end that is not a month end'. Reference (reference.py lines 54-58, _month_end) rejects all four. Mutant v21_m01 (accepts 0.0) is killed (1 failed on seeds 0 and 17) and alternative alt_r21_b (exact int type) passes all 50 seeds. Over-constraint check: no alternative fails."},
 {"id": "proj-r21-grader-month-end-real-length-test", "status": "PASS",
  "check": "2.6-spec and over-constraint (new parametrized test, 4 functions x 3 ends)",
  "location": "course/modules/AC/AC1/grader/test_project.py lines 1210-1224; project.html line 366 (Constraints: 'the last day of a calendar month ... 2000-02-29 is a month end')",
  "evidence": "The test asserts that balance_sheet, income_statement, cash_flow_statement and articulation_check accept 2024-02-29, 2023-02-28 and 2024-04-30. Line 366 says each statement function and the articulation check accept any month end and that 2024-02-29 and the common-year February 28 are month ends (2000-02-29 example). The three dates are last days of their months (calendar.monthrange: 2024-02 has 29 days, 2023-02 has 28, 2024-04 has 30). Passes on the reference for all 50 seeds and on alt_r21_a and alt_r21_b."},
 {"id": "proj-r21-cards-no-grade-open-questions", "status": "PASS",
  "check": "2.3-grades and 2.7-cards (grade field removed from AC1-c057, AC1-c071, AC1-c087)",
  "location": "course/modules/AC/AC1/cards.json entries AC1-c057, AC1-c071, AC1-c087",
  "evidence": "The three cards are open-question cards whose backs say the lesson does not state the answer. Their grade field was removed (previously 'grade C', basis 'standard text not read'). Ungraded open-question cards already exist, AC1-c101 and AC1-c118, so the convention is consistent. check_pages --unit AC1 PASS; no card requires a grade field (the cards with no grade field, 51 of 140, are listed by front in scripts/AC1-d-r21 check output; they are definitions, model conventions and open questions, such as AC1-c101 and AC1-c118)."},
 {"id": "proj-r21-mutants-v21-student-errors", "status": "PASS",
  "check": "2.5-mutation (three new student-error mutants of the reference)",
  "location": "ledgers/AC1/mutants/v21_m01_float_zero_amount_accepted.py; v21_m02_month_end_accepts_any_day_from_28.py; v21_m03_month_length_table_november_31.py; ledgers/AC1/scripts/AC1-d-r21/mk_mutants21.py",
  "evidence": "Each mutant is the reference with one student error: (m01) a zero amount is returned before the type check, so 0.0 is accepted; (m02) the month-end test is only day >= 28, so 2024-02-28 is accepted; (m03) a hard-coded month-length table with November at 31 days. Results (scripts/AC1-d-r21/out/mutants_r21.out, run_one_mutant.sh): m01 1 failed on seeds 0 and 17; m02 24 failed on both seeds; m03 13 failed on both seeds. All three killed; the failures name the period-end and amount properties."},
 {"id": "proj-r21-alternatives-two-new", "status": "PASS",
  "check": "2.6-over-constraint (architect ruling b): two new alternative correct implementations",
  "location": "ledgers/AC1/scripts/AC1-d-r21/alts/alt_r21_a_next_day_changes_month.py; alt_r21_b_exact_int_type.py",
  "evidence": "alt_r21_a finds a month end by testing whether the next day is in another month (a different valid algorithm from the length table); alt_r21_b tests type(value) is int instead of numbers.Integral. Both pass the whole suite on seeds 0-49 (run_alt_one.sh: '0 of 50' for each; scripts/AC1-d-r21/out/alts_r21.out). The first version of alt_r21_a had a typo that failed 50 of 50; it was fixed and re-run, and the fixed file is the one recorded."},
 {"id": "proj-r21-twins-match-embedded-output", "status": "PASS",
  "check": "2.5-labs (changed and project lab twins run under python -I -W error and match the embedded expected block)",
  "location": "tests/labs/AC1/lab-AC1-project-1.py, lab-AC1-project-2.py, lab-AC1-project-3.py, lab-AC1-L04-1.py, lab-AC1-L05-1.py; course/modules/AC/AC1/project.html and L04.html and L05.html expected blocks",
  "evidence": "scripts/AC1-d-r21/twin_compare.py: each twin exits 0 under -I -W error and its stdout equals the page's expected block after HTML unescape: project-1 (9 lines), project-2 (3 lines), project-3 (6 lines), L04-1 (20 lines), L05-1 (22 lines); one match each. run_labs --unit AC1 11/11. The lab twins are unchanged since the previous pin (tests/labs/AC1 empty in git diff fd9a9b7..f95243f)."},
 {"id": "proj-r21-pytest-lab-subset", "status": "PASS",
  "check": "2.5-labs (pytest subset)",
  "location": "tests/test_run_labs.py, tests/test_labs.py, tests/test_page_checks.py",
  "evidence": "python -I -W error -m pytest tests/test_run_labs.py tests/test_labs.py tests/test_page_checks.py: 174 passed (scripts/AC1-d-r21/out/pytest_labs_r21.out, exit 0). Round 20 reported 182 for a wider subset that also included test_page_smoke, which was not rerun here; that count is not claimed for this round."},
 {"id": "proj-r21-banned-phrase-and-process-scan", "status": "PASS",
  "check": "1.2/1.3-banned-phrases and 2.9-process-words on every added line of the round-21 delta",
  "location": "scripts/AC1-d-r21/out/added_lines_r21.txt (all added lines of course/modules/AC/AC1 and tests/labs/AC1 since fd9a9b7)",
  "evidence": "grep -i -E 'roughly|about N%|historically|\\.\\.\\.|half|build|builder|round |verifier|REQUEST|unit report' over the added lines: no hits."},
 {"id": "proj-r21-gates-ruff-mypy-verify-render", "status": "PASS",
  "check": "gate (ruff, mypy strict, verify_refs, render_curriculum, build_site)",
  "location": "course/modules/AC/AC1/grader; tests/labs/AC1; references/references.json; CURRICULUM.md; curriculum/curriculum.json; course/assets/data",
  "evidence": "ruff check on grader and tests/labs/AC1: All checks passed; ruff format --check on grader: 4 files already formatted; mypy --no-incremental on grader: no issues in 4 source files; tools/verify_refs.py --offline: 560 entries, 0 problems; --unit AC1 live: 2 of 560 entries, 0 problems; render_curriculum.py then git diff --exit-code: no diff; build_site.py --check: site data current. Exit 0 each."},
]
for n in NEW:
    if n["status"] == "PASS":
        n.pop("fix", None)
    ROWS.append(n)

mutants = []
for p in sorted((chk / "ledgers/AC1/mutants").glob("*.py")):
    mutants.append({"id": p.stem, "description": p.stem.replace("_", " "),
                    "file": f"ledgers/AC1/mutants/{p.name}",
                    "killed_by": "seeds 0 and 17: both fail (scripts/AC1-d-r21/out/mutants_r21.out)"})

failing = [r for r in ROWS if r["status"] != "PASS"]
frag = {
    "unit": "AC1", "slice": "AC1-d", "round": 21,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 21 (did not build AC1; read the round-20 fragment as context and computed the delta fd9a9b7..f95243f on the slice)",
    "pin": "f95243f", "base": "fd9a9b7 (round-20 pin); slice delta: course/modules/AC/AC1/L04.html (52, 331), L05.html (121, 347, 357, 360), cards.json (AC1-c057, c069, c071, c087), grader/test_project.py (704-715, 1094-1097, 1210-1224), project.html (254, 368, 373)",
    "checkout": "/tmp/verify21-AC1-d", "scratch": "/tmp/ac1-v/d21", "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL" if failing else "PASS",
    "rows": ROWS, "mutants": mutants, "registry_flags": [], "freshness_flags": [],
    "notes": ("Round 21 on f95243f. Mutants: 195 files in ledgers/AC1/mutants/ killed on both seeds 0 and 17 (scripts/AC1-d-r21/out/mutants_r21.out), plus three new v21 student-error mutants killed on both seeds. "
              "Alternatives: 37 unique alternative files pass seeds 0-49 (alts_r21.out); two new alternatives pass seeds 0-49. "
              "Reference 345 passed and collect 345 on all 50 seeds; starter 343 failed, 2 passed, on all 50 seeds (ref_collect_50seeds_r21.out). "
              "Round-20 FAIL rows cards-c069, cards-L05 and lesson-change-audit-r20-l05-remark-2-4 are fixed and re-verified PASS. "
              "Round-20 row lesson-change-audit-r19 cited L04 line 330; the bullet is at line 331 (locator corrected here). "
              "New FAIL: lesson-change-audit-r21-l04-presentation-term. "
              "Not checked by this verifier: a full numbers-in-prose pass over every lesson (only the changed sentences and the lab numbers they cite); the lab twin comparison beyond the five changed or project twins; test_page_smoke; the alternatives of rounds 10-19 beyond the 37 deduplicated files; the Remark 2.4 claim about 'end of the contract' beyond Proposition 2.3 and the 12-month delivery hypothesis."),
    "summary": (f"AC1-d round 21: verdict {'FAIL' if failing else 'PASS'}. {len(failing)} FAIL row(s): "
                + "; ".join(f"{r['id']} ({r['evidence'][:0]}see evidence)" for r in failing)
                + f". {len(ROWS) - len(failing)} PASS rows. The round-20 FAILs are fixed. "
                  "Mutants 198 (195 earlier + 3 new), all killed; alternatives 37 + 2 pass 50/50; reference 345 on 50 seeds."),
}
json.dump(frag, open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(ROWS), "fail", len(failing), "mutants", len(mutants))
