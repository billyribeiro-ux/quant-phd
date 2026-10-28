# Writes the round-23 row inputs (re-verified rows, carried rows, new rows, new mutants, notes) for build_fragment_r23.py.
import json, re, sys
from pathlib import Path

S = Path("/tmp/verify23-AC1-d/ledgers/AC1/scripts/AC1-d-r23")
OUT = S / "out"
prev = json.loads(Path("/tmp/fanout-frags/AC1-d.round22.json").read_text(encoding="utf-8"))
ids = [r["id"] for r in prev["rows"]]
alts_status = (OUT / "alts_carried_r23.out").read_text(encoding="utf-8")
RUN_CMD = "scripts/AC1-d-r23/out/"
UNCHANGED = "course/modules/AC/AC1/project.html, grader/, tests/labs/AC1/, L01-L04 and L07-L08 pages, index.html"
MUT = "Re-run this round on the round-23 grader (unchanged since d160ac3): all 204 mutants in ledgers/AC1/mutants/ killed on seeds 0 and 17 (scripts/AC1-d-r23/out/mutants_r23.out)."
ALT = ("Re-run this round on the round-23 grader (unchanged since d160ac3): 6 alternatives of this round (alt_r23_a/b/c, "
       "alt_r22_a/b/c) pass seeds 0 to 49 (out/alts_r23.out); 46 earlier alternative files from the rounds 10 to 21 "
       "directories pass seeds 0 to 49 (out/alts_carried_r23.out). Two generator scripts (mk_alts19.py, mk_alts20.py) are "
       "not implementations and fail 50 of 50 as expected; they are excluded from the count.")

RE = {}
def re_(rid, status, ev):
    RE[rid] = [status, ev]

# Gates and commands re-run on 503d139
re_("proj-run-graders", "PASS", "Re-run: .venv/bin/python tools/run_graders.py --unit AC1 -> 'run_graders AC1: PASS (reference 50/50 seeds, slowest 0.4 s)', exit 0 (out/run_graders.out).")
re_("proj-collect-count-176", "PASS", "Re-run: .venv pytest --collect-only on the grader (scripts/AC1-d-r23/run_suite.sh ... collect) -> '345 tests collected'; project.html line 368 says 'collects 345 checks ... for each of the seeds 0 to 49' (matches).")
re_("proj-local-suite-reference", "PASS", "Re-run: reference.py through run_suite.sh seed 0 -> '345 passed in 0.22s'; run_graders 50/50 seeds (out/run_graders.out).")
re_("proj-pyodide-smoke", "PASS", "Re-run full unit page smoke: tools/page_smoke.py --unit AC1 -> 'page_smoke AC1: PASS', 10 pages each PASS incl. L05, L06, project (out/page_smoke_r23.out).")
re_("proj-check-pages", "PASS", "Re-run: tools/check_pages.py --unit AC1 -> 'check_pages AC1: PASS', exit 0 (out/check_pages.out).")
re_("proj-check-projects", "PASS", "Re-run: tools/check_projects.py --unit AC1 -> 'check_projects AC1: PASS', exit 0 (out/check_projects.out).")
re_("proj-check-dag", "PASS", "Re-run: tools/check_dag.py --unit AC1 -> 'check_dag AC1: PASS', exit 0 (out/check_dag.out).")
re_("proj-run-labs", "PASS", "Re-run: tools/run_labs.py --unit AC1 -> 'run_labs AC1: PASS (11/11)', exit 0 (out/run_labs.out); the twins run under python -I -W error with exit 0 and empty stderr (L01 to L08, project-1 to 3).")
re_("proj-lab-twin-embed", "PASS", "Re-run: each AC1 twin's stdout compared with the embedded expected block of its page (L06.html line 277 expected block); the diff is leading indentation only (out/twin_L05.stdout, out/twin_L06.stdout); run_labs embed check PASS.")
re_("proj-labs-ruff", "PASS", "Re-run: .venv/bin/ruff check . -> 'All checks passed!' (out/ruff_check.out); .venv/bin/ruff format --check . -> '220 files already formatted' (out/ruff_format.out).")
re_("proj-mypy-gate", "PASS", "Re-run: .venv/bin/mypy --no-incremental -> 'Success: no issues found in 153 source files' (out/mypy.out).")
re_("proj-verify-refs", "PASS", "Re-run: tools/verify_refs.py --unit AC1 -> 'live re-verification of AC1: 2 of 560 entries, 0 problems'; tools/verify_refs.py --offline -> '560 entries, 0 problems' (out/vr_live.out, out/vr_offline.out). references/references.json unchanged in the delta.")
re_("proj-tests-labs-pytest", "PASS", "Re-run: .venv/bin/pytest tests/test_run_labs.py tests/test_labs.py tests/test_page_checks.py -> exit 0 (out/pytest_labs.out).")
re_("proj-r21-pytest-lab-subset", "PASS", "Re-run: the same three test files, exit 0 (out/pytest_labs.out).")
re_("proj-r21-gates-ruff-mypy-verify-render", "PASS", "Re-run ruff check, ruff format --check, mypy --no-incremental, verify_refs live and offline (out/*.out). tools/render_curriculum.py not re-run: the delta touches no curriculum/*.yaml, CURRICULUM.md or curriculum.json (git diff --stat d160ac3 503d139 shows only course/modules/AC/AC1 L05, L06, cards.json and other units).")
re_("proj-r21-twins-match-embedded-output", "PASS", "Re-run: twins run under python -I -W error, exit 0 (out/*.err empty); L05 and L06 stdout compared with the embedded blocks (out/twin_L06.stdout; L05 values quoted in the page match the printed block: balance_end_cents 0, max_contract_liability_cents 32792272, contract_asset_months [2..9], month_6_difference_cents 20583168).")
re_("proj-r22-lab-twins-changed", "PASS", "Re-run: lab-AC1-L05-1.py and lab-AC1-L06-1.py exit 0 under -I -W error (out/run_labs.out PASS 11/11). Neither twin changed in the delta (git diff shows no tests/labs/AC1 change).")
re_("proj-r22-ref-starter-collect-50-seeds", "PASS", "Reference: run_graders.py --unit AC1 re-run, 50/50 seeds (out/run_graders.out). Starter: run_suite.sh starter.py seed 0 -> '343 failed, 2 passed in 3.74s' (the starter is unchanged; the 50-seed starter run was not repeated this round).")
re_("proj-prose-banned", "PASS", "Re-run banned/scope scan on the round-23 delta's added lines (out/added_lines_r23.txt, 14 lines): no roughly/about N/historically/typically/usually/generally/ellipsis/process words (scan output empty except the scope words 'only' in cards c088 and 'same' in c141, both checked row cards-c088-scope and cards-c141-new-card).")
re_("proj-r21-banned-phrase-and-process-scan", "PASS", "Same scan as proj-prose-banned: added lines of L05.html, L06.html and cards.json (14 lines) contain no banned phrase and no process word (out/added_lines_r23.txt).")
re_("proj-r22-delta-scope", "PASS", "git diff --stat d160ac3 503d139 -- course/modules/AC/AC1 tests/labs/AC1 -> L05.html (1 line), L06.html (2 lines), cards.json (14 lines), 3 files; grader/, tests/labs/AC1/, project.html, L01-L04, L07-L08, index.html unchanged (git diff --stat run this round). Round 23 delta is therefore L05 line 351, L06 lines 52 and 320, cards AC1-c069, AC1-c088 and new AC1-c141.")

for rid in ids:
    if "mutant" in rid:
        re_(rid, "PASS", MUT)
for rid in ["proj-alt-implementations", "proj-overconstraint-nonmapping", "proj-r14-alternatives-new", "proj-r15-alts-a-b-c",
            "proj-v16-alternatives-r16", "proj-v17-alternatives-r17", "proj-r18-alternatives-d-b-c",
            "proj-r19-alternatives-new-a-b-c", "proj-r19-alternatives-existing-35", "proj-r21-alternatives-two-new"]:
    re_(rid, "PASS", ALT)

re_("cards-inventory-and-dupes", "PASS", "Re-run cards_numbers.py on the 141-card file: 'cards 141 unique ids 141 duplicate fronts 0' (out/cards_numbers.out). cards.json changed in the delta (AC1-c069, AC1-c088 rewritten, AC1-c141 added).")
re_("cards-grades", "PASS", "Re-run inline check: 42 T, 48 C, 51 cards with no grade field (grade field removed from some open-question cards in round 21); every C card has a basis; no C card lacks a basis (python check over cards.json, 141 entries).")
re_("cards-registry-cites", "PASS", "cards.json has no citation keys (fields: back, basis, front, grade, id, lesson); the only numeric tokens with four digits are years or seeds. Re-checked on 141 entries.")
re_("cards-no-open-r10-fail", "PASS", "Re-check on cards.json (141 entries): no field marked open or failed; the three round-21 open-question cards carry no grade (AC1-c057, c071, c087 unchanged).")
re_("cards-numbers-in-lessons", "PASS", "Re-run cards_numbers.py (out/cards_numbers.out): 'number misses 1' for AC1-c077 back '5,000' whose lesson text is KaTeX '5{,}000' in L06 Definition 1.3 (grep count 5 for '5{,}000' in L06.html); a scanner artifact of the tag-stripped text, not a missing number. Every other number on all 141 cards appears in its own lesson, including AC1-c069 and AC1-c088 numbers and the AC1-c141 numbers 13,034,272, 13,034,273 (L06 lines 320 and Lab 1 output).")
re_("cards-labels-resolve", "PASS", "Re-run cards_labels_banned.py (out/cards_labels_banned.out): 141 cards checked, 7 label misses, all scanner artifacts (the scanner matches text after tag stripping and does not see the section-number spans): 'Section 1' (L07 section-number span 1, 'A grant as a schedule'), 'Section 2' (L01 c004, c007), 'Section 5' (L03 c127), and 'Section 1' (L07 c091-c093): each is a section-number span followed by the heading text (for example L07 section-number 1, 'A grant as a schedule'). 'Problem P3' (L05 c069) is the problem titled 'P3' in the 'Problem set' section 6 (line 377).")
re_("cards-banned", "PASS", "Re-run cards_labels_banned.py: no banned phrase (roughly, about N, historically, typically, usually, generally, ellipsis) and no process word (builder, verifier, round N, REQUEST) in any of 141 cards (out/cards_labels_banned.out prints BANNED for none).")
re_("proj-cards-c001-c126-coverage", "PASS", "Re-run over cards.json (141 cards) against L01-L08: every card's lesson is present; coverage recounted from the file: 141 ids, unique, no duplicate fronts (out/cards_numbers.out).")
re_("cards-c001-c128-coverage-r15", "PASS", "Re-run over cards.json (141 cards): ids AC1-c001 to AC1-c141 with c129-c131, c132 and c139, c140, c141 in their lessons; no id missing or duplicated (out/cards_numbers.out).")
re_("cards-v17-changed-and-new-count", "PASS", "cards.json 141 entries (was 140); new entry AC1-c141 (L06) appended; AC1-c069 and AC1-c088 rewritten; count 141 confirmed by re-run (out/cards_numbers.out).")
re_("cards-c069", "PASS", "cards.json AC1-c069 (L05, grade T): front 'For a month m below 12, what is the difference between the two conventions' cumulative revenue?'; back 'The convention-1 revenue from the over-time obligations through month m: the first m monthly shares of each over-time obligation (Problem P3).' Checked against L05.html P3 (lines 428-435): the problem states the difference equals the convention-1 over-time revenue through m for m < 12, and its solution sums the first m monthly shares floor(a/12) of each over-time obligation (6 x 452,837 and 6 x 2,977,691 at m = 6). Matches; 'first m monthly shares' is what the solution uses.")
re_("cards-c088-scope", "PASS", "cards.json AC1-c088 (L06, grade C, basis 'Lab 1 (SIMULATED)'): new front 'Under pattern F, is the lease expense in each year equal to the payment made in that year?'; back 'No. Pattern F's year-1 expense is 14,820,224 cents against a payment of 13,034,272 cents (Lab 1). Only the sums over the term are equal (Proposition 2.3).' Lab 1 output (L06.html line 277 expected block): expense_front_loaded 14820224 vs payment 13034272 in year 1, and pattern F differs from the payment in each of the 7 years; sum_payments_cents 91239905 = sum_expense_front_loaded_cents. The 'Only' is bounded to Lab 1 by the grade basis; Proposition 2.3 proves the sums, and the card does not claim anything about other leases. PASS.")
re_("cards-L05", "PASS", "cards.json c061-c074 on L05 re-read against the lesson (L05.html lines 52, 121, 124, 333, 387, 401 unchanged); c069 re-verified this round (row cards-c069). PASS.")
re_("cards-L06", "PASS", "cards.json c075-c090 on L06 re-read against the lesson: c088 rewritten and re-verified (row cards-c088-scope); c087 and c079 unchanged; L06.html line 296 unchanged. PASS.")
re_("lesson-change-audit-r19-l04-l05-l06-l08", "PASS", "L06.html line 320 (misconception 1) changed this round: re-read; 'the contractual payment is level at 13,034,272 cents; ... the one-cent final adjustment falls in year 7, where the payment and the pattern S expense are both 13,034,273 cents' matches lab output (payment 13034272 years 1-6, 13034273 year 7; expense_straight_line the same). L05 lines 52, 121, 333 unchanged. L04 line 331, L06 lines 296, 411, L07 lines 51, 55, L08 lines 51, 55 unchanged. PASS.")
re_("lesson-change-audit-r20-l05-remark-2-4", "PASS", "Same as lesson-change-audit-r19-l04-l05-l06-l08: L06 line 320 re-read and matched to Lab 1 output; L05 line 121 (Remark 2.4) unchanged; L05 line 351 (new text, row r23-l05-line-351-open-inputs) re-verified separately. PASS.")
re_("lesson-change-audit-r20-l06-l07-l08", "PASS", "Same: L06 lines 296, 320 (re-read, matches lab output), 411 unchanged text; L07 lines 51, 55 and L08 lines 51, 55 unchanged. PASS.")

# Rows whose subject is unchanged are carried; these name the files or lines byte-identical since the pin.
CARRY = {}
for rid in ids:
    if rid not in RE:
        CARRY[rid] = UNCHANGED
EXPLICIT = {
    "proj-r20-l04-why-it-matters": "L05.html lines 52 and 333, L04.html lines 52 and 129-135, tests/labs/AC1/lab-AC1-L04-1.py line 4",
    "proj-r20-l04-units-no-ratio": "L05.html lines 52 and 333, L04.html lines 52 and 129-135, tests/labs/AC1/lab-AC1-L04-1.py line 4",
    "proj-r20-l05-why-it-matters-def13": "L05.html lines 52 and 333, L04.html lines 52 and 129-135, tests/labs/AC1/lab-AC1-L04-1.py line 4",
    "proj-r20-l05-line-333-identities": "L05.html lines 52 and 333, L04.html lines 52 and 129-135, tests/labs/AC1/lab-AC1-L04-1.py line 4",
    "proj-r20-l05-line-333-numbers": "L05.html lines 52 and 333, L04.html lines 52 and 129-135, tests/labs/AC1/lab-AC1-L04-1.py line 4",
    "proj-r20-l05-remark-1-5-solution": "L05.html line 401 (the delta changed L05 line 351 only)",
    "proj-r20-l05-line-387-solution": "L05.html line 387 (the delta changed L05 line 351 only)",
    "proj-r20-l06-line-296-articulation": "L06.html line 296 (the delta changed L06 lines 52 and 320 only)",
    "proj-hours": "project.html lines 33, 368, 386-415 and the lesson hours in index.html (the delta changed neither)",
    "proj-r21-cards-no-grade-open-questions": "cards.json entries AC1-c057, AC1-c071, AC1-c087 (the delta changed AC1-c069, AC1-c088 and appended AC1-c141)",
    "cards-c079": "cards.json AC1-c079 entry and L06.html Definition 1.4 (line 72, unchanged)",
    "cards-c087": "cards.json AC1-c087 entry and L06.html Section 3 (unchanged)",
    "cards-c059-c060-c070-c090": "cards.json AC1-c059, c060, c070, c090 entries and their lessons (the delta changed AC1-c069 and AC1-c088 only)",
    "cards-c070": "cards.json AC1-c070 entry and L05.html Lab 1 and misconception paragraph (line 363 unchanged)",
    "cards-c066-c067-definition-1-3-setting": "cards.json AC1-c066, AC1-c067 entries and L05.html Definition 1.3 (lines 67-70), Proposition 1.4 (line 73), Proposition 2.1 (line 95), all unchanged",
    "cards-c071": "cards.json AC1-c071 entry and L05.html Section 3 (unchanged)",
    "cards-c104": "cards.json AC1-c104 entry and L07.html Definition 1.1 and Theorem 1.3 (unchanged)",
}
CARRY.update({k: v for k, v in EXPLICIT.items() if k in CARRY})
for k, v in EXPLICIT.items():
    if k in RE:
        pass
CARDS_STR = ("cards.json entries cited in the location and their lesson pages (the round-23 delta changed cards.json "
             "only at AC1-c069, AC1-c088 and appended AC1-c141)")
for rid in list(CARRY):
    loc = next(r["location"] for r in prev["rows"] if r["id"] == rid)
    if rid not in EXPLICIT and "cards.json" in loc:
        CARRY[rid] = CARDS_STR
for rid in ["lesson-change-audit-r21-l05-misconception-title", "lesson-change-audit-r21-l05-remark-2-4-and-peak-sentence"]:
    CARRY[rid] = "L05.html lines 121, 363 and 495 (the round-23 delta changed L05 line 351 only)"
# carried rows citing L05/L06/cards without an explicit entry are a build error
for rid in list(CARRY):
    loc = next(r["location"] for r in prev["rows"] if r["id"] == rid)
    if rid not in EXPLICIT and re.search(r"L05|L06|cards\.json", loc) and CARRY[rid] == UNCHANGED:
        print("CHECK CARRY", rid, "|", loc[:120])

NEW = [
 {"id": "r23-l05-line-351-open-inputs-sentence", "check": "2.9-prose and 2.7 lesson prose (changed sentence)",
  "location": "course/modules/AC/AC1/L05.html line 351 (Section 4 bullet 'The four open inputs are the standard-specific questions.')",
  "status": "PASS",
  "evidence": "Rewritten sentence: 'The identities in this lesson are proved for the conventions this lesson fixes. They do not decide any of the four answers.' Checked: the lesson has proof blocks for Proposition 1.4 (line 76), Proposition 2.1 (line 99) and Proposition 2.3 (line 114), and Section 3 (line 342) says the lesson fixes all four inputs by construction and cites no primary text. 'Identities' is bounded to those three propositions and the balance identity of Definition 2.2. No overreach found."},
 {"id": "r23-l06-line-52-why-it-matters", "check": "2.4-prose and 2.9-prose (changed why-it-matters sentence)",
  "location": "course/modules/AC/AC1/L06.html line 52 (why-it-matters)",
  "status": "PASS",
  "evidence": "Rewritten clause: 'proves that the asset less the liability moves with cash paid less the front-loaded expense that Definition 1.4 defines, in every year.' Checked: Definition 1.4 (line 72) states 'Pattern F, front-loaded, is expense E^F_t = I_t + a_t'; Proposition 2.4 (line 109) states the identity for every year t; its proof (line 113) uses Definitions 1.3 and 1.4 for each t including t = n; Lab 1 prints articulation_every_year True (L06 output). The term is introduced in Definition 1.4, which the sentence points to. PASS."},
 {"id": "r23-l06-line-320-pattern-s-misconception", "check": "2.2-numbers-in-prose and 2.9-prose (changed misconception paragraph)",
  "location": "course/modules/AC/AC1/L06.html line 320 (Section 5 misconception 1)",
  "status": "PASS",
  "evidence": "Numbers re-derived from Lab 1 printed output (L06.html line 277 expected block): pattern F year 1 expense 14820224, payment 13034272; payments 13034272 in years 1-6, final payment 13034273 (final_payment_cents 13034273, contractual_payment_cents 13034272); expense_straight_line 13034272 in years 1-6 and 13034273 in year 7; sum_payments_cents 91239905 = 6 x 13034272 + 13034273. Floor check: floor(91239905/7) = 13034272 (Definition 1.4). 'The contractual payment is level at 13,034,272' matches Definition 1.3 (Y_t = P for t < n). PASS."},
 {"id": "cards-c141-new-card", "check": "2.7-cards (new card) and 2.2-numbers",
  "location": "course/modules/AC/AC1/cards.json AC1-c141 (L06, grade C, basis 'Lab 1 (SIMULATED)')",
  "status": "PASS",
  "evidence": "Front 'In Lab 1, does pattern S expense equal the payment in every year?' Back 'Yes. Pattern S spreads the total payments in equal shares over the term. It is 13,034,272 cents in years 1 to 6 and 13,034,273 cents in year 7, the same as the payments in those years (Lab 1).' Checked against Lab 1 output: expense_straight_line 13034272 (years 1-6) and 13034273 (year 7); payment 13034272 and 13034273 in the same years; Definition 1.4 (line 72-74) 'spreads the total payments in equal shares'. The 'yes' is bounded to Lab 1 by the basis. PASS."},
 {"id": "r23-delta-scope", "check": "scope (round-23 delta against round-22 pin)",
  "location": "git diff --stat d160ac3 503d139 -- course/modules/AC/AC1 tests/labs/AC1 references",
  "status": "PASS",
  "evidence": "3 files changed in the slice: course/modules/AC/AC1/L05.html (1 line, 351), L06.html (2 lines, 52 and 320), cards.json (14 lines: AC1-c069, AC1-c088 rewritten, AC1-c141 added). No change in grader/, tests/labs/AC1/, project.html, L01-L04, L07-L08, index.html, references/. The other changed paths in the repository (AC4, CF1, M1 pages and ledgers) are outside the slice."},
 {"id": "r23-mutants-v23-student-errors", "check": "2.5-mutation (three new student-error mutants, round 23)",
  "location": "ledgers/AC1/mutants/v23_m01_one_cent_imbalance_accepted.py, v23_m02_december_thirtieth_is_month_end.py, v23_m03_posting_dated_one_day_late.py; grader/test_project.py",
  "status": "PASS",
  "evidence": "Each mutant is a copy of grader/reference.py with one change, written by scripts/AC1-d-r23/mk_mutants23.py. v23_m01 accepts an entry out by one cent (spec: project.html line 366 'an entry whose debits do not equal its credits' raises); killed on seeds 0 and 17 by test_post_raises_a_value_error[an unbalanced entry-transactions26] etc. v23_m02 accepts 30 December as a period end (spec: line 366 'a period end ... the last day of a calendar month'); killed by test_period_end_must_be_a_month_end[2024-12-30-...] x4. v23_m03 dates every posting one day late; killed by 54/57 failing tests including test_an_entry_dated_on_the_period_end_is_in_that_balance. All three exit with failures on both seeds (out/mutants_r23.out)."},
 {"id": "r23-alternatives-six-correct", "check": "2.6-over-constraint: six correct alternatives (architect ruling b)",
  "location": "scripts/AC1-d-r23/alts/ (alt_r23_a_date_regex_then_parse, alt_r23_b_sorted_ledger_early_stop, alt_r23_c_month_end_day28_trick) and scripts/AC1-d-r22/alts/ (alt_r22_a, b, c)",
  "status": "PASS",
  "evidence": "Each alternative differs from reference.py (diff run) and passes 50 of 50 seeds: alt_r23_a regex date check; alt_r23_b balances from the date-sorted ledger with an early break; alt_r23_c month end from the day-28 trick. Output 0 of 50 seeds with failures for all six (out/alts_r23.out). Over-constraint witness: none."},
 {"id": "r23-page-smoke-full-unit", "check": "2.5-page-smoke (all AC1 pages)",
  "location": "tools/page_smoke.py --unit AC1",
  "status": "PASS",
  "evidence": "Full unit run: index, L01-L08, project each 'PASS'; 'page_smoke AC1: PASS' (out/page_smoke_r23.out). Only a timing line is printed per lab; no timing failure."},
 {"id": "r23-collect-and-reference-seed0", "check": "2.6-autograder count and reference (changed-neighbour rerun)",
  "location": "course/modules/AC/AC1/grader/test_project.py; grader/reference.py; project.html line 368",
  "status": "PASS",
  "evidence": "pytest --collect-only on the grader: '345 tests collected' (out/ run_suite collect); reference seed 0: '345 passed in 0.22s'; project.html line 368 says the grader 'collects 345 checks' and the count is 345 for each seed 0 to 49 (run_graders 50/50). Starter seed 0: '343 failed, 2 passed in 3.74s'."},
 {"id": "r23-banned-scan-cards-and-pages", "check": "1.2/1.3 banned phrases and process words in the delta",
  "location": "course/modules/AC/AC1/L05.html line 351; L06.html lines 52, 320; cards.json AC1-c069, AC1-c088, AC1-c141",
  "status": "PASS",
  "evidence": "Scan of the 14 added lines (out/added_lines_r23.txt) for roughly, about N, historically, typically, usually, generally, '...', builder, verifier, round N, REQUEST, all, always, as much as, drives, offsets, raises: only 'only' (c088, bounded to Lab 1 by its basis), 'same' (c141, verified against lab output) and 'raises' inside line 52's quoted spec terms match; no banned phrase or process word."},
 {"id": "cards-c069-scanner-note", "check": "2.9-numbers-in-cards (scanner artifact note)",
  "location": "scripts/AC1-d-r23/out/cards_numbers.out and cards_labels_banned.out",
  "status": "PASS",
  "evidence": "The two non-matching items the scanners print are artifacts of tag stripping: AC1-c077 '5,000' is '5{,}000' in KaTeX (L06 Definition 1.3); labels 'Section 1' (L07), 'Section 2' (L01), 'Section 5' (L03) are section-number spans followed by the heading text, and 'Problem P3' is the problem titled P3 under section 6, 'Problem set'. Each was read in the lesson and matches."},
]
(S / "reverified.json").write_text(json.dumps({k: v for k, v in RE.items()}, indent=1, ensure_ascii=False), encoding="utf-8")
(S / "carried.json").write_text(json.dumps(CARRY, indent=1, ensure_ascii=False), encoding="utf-8")
(S / "new_rows.json").write_text(json.dumps(NEW, indent=1, ensure_ascii=False), encoding="utf-8")
print("RE", len(RE), "CARRY", len(CARRY), "NEW", len(NEW), "total", len(RE) + len(CARRY) + len(NEW), "prev", len(ids))
