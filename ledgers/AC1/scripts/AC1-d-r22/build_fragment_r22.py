# Builds the round-22 AC1-d fragment from the round-21 row inventory plus this round's re-verification.
import json, sys
from pathlib import Path

CHK = Path("/tmp/verify22-AC1-d")
OUT = CHK / "ledgers/AC1/scripts/AC1-d-r22/out"
prev = json.load(open("/tmp/fanout-frags/AC1-d.round21.json"))
PREV_PIN = "f95243f"
PROJ_FILES = ("course/modules/AC/AC1/project.html, course/modules/AC/AC1/grader/* (reference.py, instance.py, "
              "starter.py, test_project.py), tests/labs/AC1/lab-AC1-project-1.py, lab-AC1-project-2.py, "
              "lab-AC1-project-3.py, references/references.json")
CARD_NOTE = ("cards.json changed at f95243f..d160ac3 only in AC1-c070; every other card object is byte-identical; "
             "AC1-c070 re-verified this round")
CMD = ("Round-22 commands on d160ac3: check_pages --unit AC1 PASS; check_dag --unit AC1 PASS; check_projects --unit AC1 "
       "PASS; run_graders --unit AC1 --seeds 0-49 PASS (reference 50/50; scripts/AC1-d-r22/out/run_graders.out); "
       "run_labs --unit AC1 11/11; page_smoke --unit AC1 --pages L04 L05 L06 project PASS; ruff check and format PASS; "
       "mypy PASS; verify_refs --unit AC1 live 2 of 560, 0 problems; verify_refs --offline 560 entries, 0 problems")

over = {}
def ov(ids: str, status: str, check: str, location: str, evidence: str) -> None:
    for i in ids.split():
        over[i] = dict(id=i, check=check, location=location, status=status, evidence=evidence)

ov("proj-run-graders proj-pyodide-smoke proj-check-pages proj-check-projects proj-check-dag proj-run-labs proj-labs-ruff "
   "proj-mypy-gate proj-verify-refs", "PASS", "gate", "AC1 grader, lab twins, project.html, references",
   "Re-run this round on d160ac3. " + CMD + ". Collect-only: 345 on each of seeds 0-49 "
   "(scripts/AC1-d-r22/out/ref_starter_50seeds_r22.out: 50 of 50 'ref collect 345'); reference 345 passed on 50 of 50 "
   "seeds; starter 343 failed, 2 passed on 50 of 50 seeds. Lab twins: L04, L05, L06 twins rerun under python -I -W error "
   "and each matches its embedded expected block exactly (scripts/AC1-d-r22/out/twin_L0[456]*.out).")
ov("proj-collect-count-176 proj-local-suite-reference proj-hours proj-prose-banned", "PASS", "2.6/2.9/hours",
   "course/modules/AC/AC1/project.html (lines 33, 368, 386-415); grader/test_project.py",
   "Re-verified on d160ac3: project.html and grader unchanged since f95243f (git diff --stat empty for both), so the cited "
   "locators are byte-identical. Collect 345 on 50 of 50 seeds (ref_starter_50seeds_r22.out). Added-line scan of the "
   "whole round-22 delta (scripts/AC1-d-r22/out/added_lines_r22.txt, 26 lines) finds no banned phrase or process word.")
ov("proj-pyodide-smoke", "PASS", "2.5-page-smoke", "project.html; L04, L05, L06 (changed); L07, L08 (unchanged this round)",
   CMD + ". page_smoke (scripts/AC1-d-r22/out/page_smoke_r22.out): L04, L05, L06, project PASS; in-browser grader 'All 345 "
   "tests pass'.")
ov("proj-run-labs proj-r21-twins-match-embedded-output proj-r22-lab-twins-changed", "PASS", "2.5-labs",
   "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py (changed), lab-AC1-L06-1.py, lab-AC1-project-1/2/3.py",
   "run_labs --unit AC1 11/11 PASS. Each twin run under python -I -W error (scripts/AC1-d-r22/out/twin_L04_again.out, "
   "twin_L05.out, twin_L06_again.out) equals its expected block in the lesson HTML exactly (checked with a script "
   "that strips the expected block and diffs it: L04 MATCH, L05 MATCH, L06 MATCH). The L05 twin added a print of "
   "contract_asset_months; the embedded block (L05.html line 333) prints '[2, 3, 4, 5, 6, 7, 8, 9]' for 0 percent upfront.")
ov("proj-r21-pytest-lab-subset proj-tests-labs-pytest", "PASS", "2.5-labs", "tests/test_run_labs.py, tests/test_labs.py, tests/test_page_checks.py",
   "Re-run on d160ac3: pytest tests/test_run_labs.py tests/test_labs.py tests/test_page_checks.py exit 0 "
   "(scripts/AC1-d-r22/out/pytest_labs_r22.out).")
ov("proj-verify-refs", "PASS", "2.1-citations", "references/references.json; project.html line 534 (data-cite penman2013financial)",
   "verify_refs --unit AC1 live: 2 of 560 entries, 0 problems; --offline: 560 entries, 0 problems (vr_live.out, vr_offline.out). "
   "references.json unchanged since f95243f.")
ov("proj-alt-implementations proj-r21-alternatives-two-new proj-overconstraint-nonmapping proj-r15-alts-a-b-c",
   "PASS", "2.6-over-constraint (architect ruling b)", "course/modules/AC/AC1/grader/test_project.py (whole suite)",
   "Round 22: three NEW alternative correct implementations (scripts/AC1-d-r22/alts/): alt_r22_a_next_month_first_day "
   "(month end from the first day of the next month), alt_r22_b_balance_cutoff_as_not_after (day not after the end), "
   "alt_r22_c_equity_as_assets_less_liabilities (equity as assets less liabilities). Each passes seeds 0-49: '0 of 50 "
   "seeds with failures' (scripts/AC1-d-r22/out/alts_r22.out). The 37 earlier alternatives are carried from round 21 "
   "(" + PROJ_FILES + " and the alternative files under ledgers/AC1/scripts/ are byte-identical since f95243f).")
ov("proj-mutants-set-killed proj-mutants-new-r10-m58-m61 proj-mutants-m01-m08 proj-mutants-m11-m20 proj-mutants-m21-m25 "
   "proj-mutants-m33-m38 proj-mutants-new-r9-three-written proj-mutants-new-m26-m28 proj-mutants-m62-m71-fixer "
   "proj-mutants-new-r11-m72-m75 proj-mutants-new-r12-m86-m89 proj-mutants-fx01-fx10 proj-mutants-new-r13-m91-m93 "
   "proj-r21-mutants-v21-student-errors", "PASS", "2.5-mutation",
   "ledgers/AC1/mutants/ (201 files)",
   "Round-22 re-run of ALL 201 mutants in ledgers/AC1/mutants/ on seeds 0 and 17 with the round-22 grader "
   "(scripts/AC1-d-r22/run_one_mutant.sh, output scripts/AC1-d-r22/out/mutants_r22.out): every one of the 201 lines "
   "shows 'N failed' on both seeds, so every mutant is killed. Previous-round mutants are unchanged files.")
for mid in ["proj-mutant-m09-articulation-zero", "proj-mutant-m10-depreciation-gap", "proj-mutant-m26-payables-sign",
            "proj-mutant-m27-cogs-from-balance", "proj-mutant-m28-timestamp-date-accepted",
            "proj-mutant-m29-boolean-credit-accepted", "proj-mutant-m30-whitespace-date-accepted",
            "proj-mutant-m31-account-name-case-folded", "proj-mutant-m32-retained-gap-sign",
            "proj-mutant-m39-account-name-whitespace-stripped", "proj-mutant-m40-credit-float-accepted",
            "proj-mutant-m41-week-date-accepted", "proj-mutant-m42-month-end-previous-length",
            "proj-mutant-m43-negative-credit-absolute", "proj-mutant-m44-unbalanced-one-direction",
            "proj-mutant-m45-negative-debit-clamped", "proj-mutant-m46-unpadded-date-accepted",
            "proj-mutant-m47-numeric-string-amount", "proj-mutant-m89-first-day-entry-rejected",
            "proj-mutant-m90-amount-cap-survives", "proj-r14-mutant-m101", "proj-r14-mutant-m102", "proj-r14-mutant-m103",
            "proj-r14-mutant-m104", "proj-r15-mutant-m01-income-blind-leap", "proj-r15-mutant-m02-cash-flow-blind-leap",
            "proj-r15-mutant-m03-articulation-blind-leap", "proj-r15-mutant-m04-balance-control",
            "proj-r15-mutant-m05-depreciation-gap-sign", "proj-r15-mutant-m06-dividends-paid-sign",
            "proj-v16-mutant-m03-articulation-no-month-end-test", "proj-r18-student-mutants-m01-m06",
            "proj-r19-student-mutants-v19-m01-m04", "proj-mutants-new-r10-m58-m61", "proj-mutant-m89-first-day-entry-rejected",
            "proj-r13-year-edge-tests"]:
    if mid == "proj-r13-year-edge-tests":
        continue
    ov(mid, "PASS", "2.5-mutation", "ledgers/AC1/mutants/", "Round-22 re-run of all 201 mutants on seeds 0 and 17 "
       "(scripts/AC1-d-r22/out/mutants_r22.out): this mutant shows 'failed' on both seeds.")
ov("proj-r21-mutants-v21-student-errors", "PASS", "2.5-mutation", "ledgers/AC1/mutants/v21_m01..v21_m03",
   "Round-22 re-run (scripts/AC1-d-r22/out/mutants_r22.out): v21_m01_float_zero_amount_accepted, "
   "v21_m02_month_end_accepts_any_day_from_28 and v21_m03_month_length_table_november_31 each show 'failed' on seeds 0 and 17.")
ov("proj-r22-student-mutants-v22", "PASS", "2.5-mutation (new round-22 student errors)",
   "ledgers/AC1/mutants/v22_m01_missing_transaction_date_defaults.py, v22_m02_missing_line_account_defaults_to_cash.py, "
   "v22_m03_empty_account_name_accepted.py",
   "Three NEW student-error mutants of the reference (scripts/AC1-d-r22/mk_mutants22.py). Each is killed on seeds 0 and 17 "
   "by the named test: v22_m01 -> test_post_raises_a_value_error[a transaction without a date-transactions1] (spec: "
   "project.html line 366, 'post raises for a transaction without a date'); v22_m02 -> "
   "[a line without an account-transactions27] (spec: 'a line without an account'); v22_m03 -> [an empty account name-"
   "transactions50] (spec: 'an account outside the chart'). Each mutant's failing test is printed by pytest -rf.")
ov("cards-numbers-in-lessons", "PASS", "2.9-numbers-in-cards",
   "course/modules/AC/AC1/cards.json (140 cards) against L01-L08",
   "Re-run this round (scripts/AC1-d-r22/cards_numbers.py, out cards_numbers_r22.out): 140 cards, 140 unique ids, 0 duplicate "
   "fronts; every number in every front and back appears in its own lesson's tag-stripped text except AC1-c077 '5,000', "
   "which the lesson writes as KaTeX source '5{,}000' (L06.html line 68); the rendered value is 5,000. Result: PASS.")
ov("cards-inventory-and-dupes", "PASS", "2.7-cards", "course/modules/AC/AC1/cards.json",
   "Re-run: 140 cards, ids AC1-c001..AC1-c140, 140 unique ids, 0 duplicate fronts (cards_numbers_r22.out). Lesson counts: "
   "L01 16, L02 16, L03 18, L04 20, L05 14, L06 16, L07 18, L08 22 (sum 140).")
ov("cards-banned cards-labels-resolve", "PASS", "2.7-cards / 1.2-banned",
   "course/modules/AC/AC1/cards.json (140 cards) against each card's own lesson",
   "Re-run (scripts/AC1-d-r22/cards_labels_banned.py, out cards_labels_banned_r22.out): no card contains a banned phrase or "
   "process word; every cited Definition/Proposition/Corollary/Remark/Theorem/Problem/Section/Lab label occurs in its own "
   "lesson, except 'Section 1/2/5' in AC1-c004, c007, c091, c092, c093, c127, which are heading numbers rendered as "
   "<span class=\"section-number\">N</span> (checked: L01 Section 2, L07 Section 1, L03 Section 5 headings exist).")
ov("cards-grades cards-registry-cites cards-no-open-r10-fail cards-v17-changed-and-new-count", "PASS", "2.7-cards",
   "course/modules/AC/AC1/cards.json", "Carried from round 21 (" + CARD_NOTE + "; the grade and basis fields of all "
   "other cards are unchanged; references.json unchanged): see round-21 locators.")
ov("cards-c070", "PASS", "2.7-card vs lesson", "cards.json AC1-c070 (L05) against L05.html Lab 1 and misconception paragraph",
   "AC1-c070 back now reads 'At 0 percent it is a contract asset in 8 months, months 2 to 9, with a largest value of "
   "23,333,398 cents'. The lab (tests/labs/AC1/lab-AC1-L05-1.py, rerun) prints months_with_contract_asset 8 and "
   "contract_asset_months [2, 3, 4, 5, 6, 7, 8, 9] for 0 percent and [] for 40 percent; the 40 percent liability peak "
   "32,792,272 and the contract-asset peak 23,333,398 match. Grade C, basis 'Lab 1 (SIMULATED), seed 2605' is correct for a "
   "single-seed lab result. PASS.")
ov("cards-c059-c060-c070-c090", "PASS", "2.7-card vs lesson", "cards.json AC1-c059, c060, c070, c090",
   "c070 re-verified above; c059 (L04), c060 (L04, Proposition 3.1; 3,319,293 cents) and c090 (L06) carried: " + CARD_NOTE + ".")
ov("lesson-change-audit-r21-l04-presentation-term", "PASS", "2.7-card/lesson 2.9-prose",
   "course/modules/AC/AC1/L04.html line 331 (Section 5 bullet 'Operating cash flow is not invariant to classification.'); "
   "L04.html lines 52, 129-131, 299-301 (round-22 rename)",
   "The round-21 FAIL is fixed in d160ac3: the bullet now says 'classification', which matches Proposition 3.1 (CFO "
   "moves by the amount moved; Lab 1: 3,319,293 cents). The rename 'two cash-flow arrangements' (line 52, lab heading "
   "line 129) and the Section 3 sentence (line 301) define presentation 1 and 2 as arrangements and state that Definition "
   "1.3 (line 68, 'a presentation difference ... leaves every amount as it was') does not cover them: correct, because "
   "those two arrangements change operating and financing amounts by I_t. The lab docstring (tests/labs/AC1/lab-AC1-L04-1.py "
   "line 1) matches the new heading. Re-verified.")
ov("lesson-change-audit-r21-l05-misconception-title lesson-change-audit-r21-l05-remark-2-4-and-peak-sentence", "PASS",
   "2.7 lesson prose", "L05.html misconception paragraph (line 363), Remark 2.4 (line 121), Key results row (line 495)",
   "Re-verified this round: the misconception paragraph now reads 'was a contract asset in 8 months, months 2 to 9' (lab output "
   "contract_asset_months [2..9], 8 months); Remark 2.4 (line 121) unchanged; key-results row cites 'months 2 to 9'. "
   "Under 0 percent upfront billing the balance is negative exactly in months 2 to 9 (printed list), so the wording is "
   "exact. E3 solution (line 454) says the lab prints the months and count: true.")
ov("lesson-change-audit-r20-l05-remark-2-4 lesson-change-audit-r20-l06-l07-l08 lesson-change-audit-r19-l04-l05-l06-l08", "PASS",
   "2.7 lesson prose", "L04.html line 331; L05.html lines 52, 121, 333; L06.html lines 296, 320, 411; L07 lines 51, 55; L08 lines 51, 55",
   "Re-verified on the round-22 text. L04 bullet (line 331, formerly cited as 330) now reads 'classification' and is verified "
   "(see lesson-change-audit-r21-l04-presentation-term). L05 line 52 'Definition 1.3' for allocation and transaction price "
   "verified against L05 Definitions 1.1 and 1.3 (line 67). L06 line 320 'Pattern S equals the payment in every year of "
   "Lab 1': verified by the L06 twin output (expense_straight_line equals payment in years 1-7: 13,034,272 and 13,034,273). "
   "L06 line 411 solution: 'The lab prints one lease' true (one lease, no crossing-year sweep in the lab). L07 and L08 lines unchanged.")
ov("proj-r20-l05-line-333-identities proj-r20-l05-line-333-numbers proj-r20-l05-why-it-matters-def13 proj-r20-l04-why-it-matters proj-r20-l04-units-no-ratio", "PASS",
   "2.2/2.9 numbers and prose", "L05.html lines 52, 333; L04.html lines 52, 129-135; tests/labs/AC1/lab-AC1-L04-1.py line 4",
   "Re-verified on round-22 text. L05 line 333 numbers recomputed from the rerun twin output: 80,495,111 total; "
   "month-6 cumulative 50,471,362 (share 0.62701 = 50,471,362/80,495,111); 40 percent peak 32,792,272; 0 percent contract "
   "asset peak 23,333,398 = 0.2899 of price; contract_asset_months [2..9] (8 months); month-6 difference 20,583,168. "
   "Rounding: 0.6270 from unrounded 0.62701 is consistent. L04 line 52 'two cash-flow arrangements' and 36 entries (lab prints "
   "ledger_entries 36) verified; lab docstring line 4 'The lab prints no ratio' unchanged and true (no ratio printed).")
ov("proj-r21-banned-phrase-and-process-scan", "PASS", "1.2/1.3 banned and process words",
   "round-22 delta added lines (scripts/AC1-d-r22/out/added_lines_r22.txt, 26 lines)",
   "Scan for roughly, about, historically, typically, usually, generally, often, most, half, ellipsis, round, build, verifier: "
   "no banned hit (the one match is 'unrounded', a mathematical term in L05 line 333).")
ov("proj-r22-delta-scope", "PASS", "scope", "git diff --stat f95243f d160ac3 for course/modules/AC/AC1 and tests/labs/AC1",
   "Slice delta: L04.html, L05.html, L06.html, cards.json (AC1-c070 only), tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py. "
   "project.html and grader/* are NOT in the delta, so the project rows are carried by byte-identity.")

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in over:
        rows.append(over[rid])
        continue
    if rid.startswith("cards"):
        rows.append(dict(id=rid, check=r["check"], location=r["location"], status="PASS",
                         evidence="Carried from round 21 (" + CARD_NOTE + "): " + r["evidence"][:300]))
    else:
        rows.append(dict(id=rid, check=r["check"], location=r["location"], status="PASS",
                         evidence="Carried from round 21 (" + PROJ_FILES + " byte-identical since the previous pin): "
                         + r["evidence"][:300]))
ids = {r["id"] for r in rows}
extra = [
    dict(id="proj-r22-ref-starter-collect-50-seeds", check="2.6-autograder-reference", location="grader/reference.py, starter.py, test_project.py",
         status="PASS", evidence="scripts/AC1-d-r22/out/ref_starter_50seeds_r22.out: reference 345 passed (50/50), collect 345 (50/50), starter 343 failed, 2 passed (50/50). Seeds 0-49."),
]
for e in extra:
    if e["id"] not in ids:
        rows.append(e)
        ids.add(e["id"])
for oid, orow in over.items():
    if oid not in ids:
        rows.append(orow)
        ids.add(oid)
for r in prev["rows"]:
    assert r["id"] in ids, r["id"]
mutants = [
    dict(id="v22_m01_missing_transaction_date_defaults", description="student posts a transaction with no date under a default date",
         file="ledgers/AC1/mutants/v22_m01_missing_transaction_date_defaults.py", killed_by="seeds 0 and 17: 1 failed each (test_post_raises_a_value_error[a transaction without a date-transactions1])"),
    dict(id="v22_m02_missing_line_account_defaults_to_cash", description="student posts a line with no account to cash",
         file="ledgers/AC1/mutants/v22_m02_missing_line_account_defaults_to_cash.py", killed_by="seeds 0 and 17: 1 failed each (test_post_raises_a_value_error[a line without an account-transactions27])"),
    dict(id="v22_m03_empty_account_name_accepted", description="student accepts the empty string as an account name",
         file="ledgers/AC1/mutants/v22_m03_empty_account_name_accepted.py", killed_by="seeds 0 and 17: 1 failed each (test_post_raises_a_value_error[an empty account name-transactions50])"),
]
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag = dict(
    unit="AC1", slice="AC1-d", round=22,
    verifier="Claude Haiku 5.5, independent verifier for AC1-d, round 22 (did not build AC1; computed the delta f95243f..d160ac3 on the slice and re-verified every previous non-PASS row and every row whose subject changed)",
    pin="d160ac3", base="f95243f (round-21 pin); slice delta: L04.html (52, 129-131, 299-301, 331, 418), L05.html (52, 293-298, 333, 363, 418-454 area, 495), L06.html (320, 411), cards.json (AC1-c070), tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py",
    checkout="/tmp/verify22-AC1-d", scratch="/tmp/ac1-v/d22", verified_at="2026-10-28T00:00:00+00:00",
    verdict=verdict, rows=rows, mutants=mutants, registry_flags=[], freshness_flags=[],
    notes=("Round 22 on d160ac3. Mutants: 201 files in ledgers/AC1/mutants/ (198 earlier + 3 new v22), all killed on seeds 0 and 17 (scripts/AC1-d-r22/out/mutants_r22.out). "
           "Alternatives: 3 new (alt_r22_a/b/c) pass seeds 0-49; the 37 round-21 alternatives are carried (grader and alternative files unchanged). "
           "Reference 345 on 50 seeds; starter 343 failed, 2 passed on 50 seeds. The round-21 FAIL (lesson-change-audit-r21-l04-presentation-term) is fixed and re-verified PASS. "
           "Not checked by this verifier: a full line-by-line re-read of every lesson page (only the changed hunks and the lab numbers they cite); the 37 round-21 alternatives were not re-run; "
           "the three new cards-related scripts check numbers and labels by text match, not by reading each card against its paragraph again; hours were not re-estimated (architect ruling)."),
    summary=(f"AC1-d round 22: verdict {verdict}. {sum(1 for r in rows if r['status']=='PASS')} PASS rows, "
             f"{sum(1 for r in rows if r['status']!='PASS')} non-PASS. Mutants 201 (198 + 3 new), all killed; alternatives 3 new + 37 carried pass 50/50; reference 345 on 50 seeds; starter 343 failed on 50 seeds."),
)
Path(CHK / "ledgers/AC1/AC1-d.json").write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "verdict", verdict)
