"""Build ledgers/AC1/AC1-b.json for round 21 from the round-20 rows (ids kept), the delta, and re-verified rows."""
import json
from pathlib import Path

ROOT = Path("/tmp/verify21-AC1-b")
prev = json.load(open("/tmp/fanout-frags/AC1-b.round20.json"))["rows"]
CARRY = ("Carried from round 20 (the cited subject is byte-identical since the previous pin fd9a9b7; the only changed "
         "subjects in slice b are L04.html lines 52 and 331, L05.html lines 121, 347, 357 and 360, and cards.json "
         "entries AC1-c057, c069, c071 and c087):")

NEW_EV = {
    "AC1b-card-c069": ("PASS", "cards.json AC1-c069 back now reads 'the paragraph after Remark 2.4 in Section 2, beginning "
        "Convention 1 and convention 2 agree at month 12'. L05.html line 124 is that paragraph; it says the difference at any "
        "m < 12 equals the convention-1 over-time revenue through m (convention 2 places no over-time revenue before month 12). "
        "The card's content matches. Problem P3 exists (L05.html line 423). Fixed since round 20.", None),
    "AC1b4-L04-why-scope": ("PASS", "L04.html line 52 (changed) now says 'The lesson states no requirement of US GAAP or IFRS "
        "Standards, and it cites neither primary text.' Remark 1.2 (line 63) says 'states no rule of either framework ... cites "
        "neither primary text'; References (L04.html line 560) says 'No source is cited on this page'. 'One SIMULATED set of 36 "
        "ledger entries over eight quarters' matches twin_L04 output (ledger_entries 36, quarters 8).", None),
    "AC1b-data-simulated": ("PASS", "L04.html line 52 (changed) still contains 'one SIMULATED set of 36 ledger entries'; "
        "L04 line 130 (lab hypothesis) and line 324 (honest pending); L05 lines 52, 128, 340; L06 lines 52, 125, 303 (grep -n). "
        "SIMULATED labelling present on every cited line.", None),
    "AC1b20-L04-why-same-quarter": ("PASS", "L04.html line 52 (changed): 'can report different net income in the same "
        "quarter, as Lab 1 shows'. twin_L04 output quarter q1: ni_rule_a -52,491 and ni_rule_b 3,612,039 (out/twin_L04.txt). "
        "The witness is printed.", None),
    "AC1b-scope-words": ("PASS", "Changed lines re-read for scope words (only, all, always, as much as, same, drives, offsets, "
        "raises; grep -o over L04.html 52, 331 and L05.html 121, 347, 357, 360). L04:52 'same' (transactions; quarter q1 witness "
        "above). L05:347 'only' ('a contract asset only under the 0 percent schedule'): witnessed by twin_L05 max_contract_asset "
        "0 at 40 percent (months_with_contract_asset 0) and 23,333,398 at 0 percent (months 8). L05:357 and 360 'same' ('the same "
        "contract's balance'; 'the same total of 80,495,111', printed totals_equal_under_both_conventions True). Carried lines "
        "unchanged.", None),
    "AC1b-L04-interp-lab-claims": ("PASS", "L04.html section 5 bullets 329 to 332; line 331 (changed) now 'Operating cash flow is "
        "not invariant to presentation. Proposition 3.1 shows that a classification choice changes operating cash flow by the "
        "amount moved.' Prop 3.1 (line 304) states CFO2 = CFO1 + I_t; the twin prints interest_moved_total_cents 3319293 and "
        "cfo_presentation_2 - cfo_presentation_1 = 27,832,482 - 24,513,189 = 3,319,293 (twin_L04). Bullet 2 (line 330) witness "
        "prepaid_balance_b zero at q0 and non-zero q1-q7 (twin_L04). Net income and cash unchanged: presentation_identity True.",
        None),
    "AC1b-L05-prose-as-much-as": ("PASS", "Section 4 bullet 1 (line 345): 'can move revenue between obligations' is a possibility "
        "claim supported by Remark 1.5 (line 87). Bullet 2 (line 346) unchanged. Line 357 (changed) has no scope word beyond "
        "'same' and 'every month' (Equal billing and revenue would need D_m = 0 in every month: D_m is not zero at month 1, "
        "32,792,272 cents, twin_L05). Line 365 unchanged. No 'as much as' claim.", None),
    "AC1b-L05-remark24-bullet": ("PASS", "L05.html section 4 bullet 3 (line 347, changed): 'Remark 2.4 shows that the balance can "
        "be large in between. Lab 1 shows a liability under both billing schedules, and a contract asset only under the 0 percent "
        "schedule.' twin_L05 prints max_contract_liability 32,792,272 (40 percent) and 6,163,184 (0 percent); max_contract_asset "
        "0 (40 percent) and 23,333,398 (0 percent). Remark 2.4 (line 121, changed) says 'can be large in between'. Each clause "
        "is witnessed. Recomputed in scratch: 40 percent balance has no month below zero; 0 percent has a month-2 to month-9 "
        "asset run (8 months).", None),
    "AC1b20-L05-remark24-condition": ("PASS", "L05.html line 121 (changed): 'When total billing and total revenue both equal the "
        "price (Proposition 2.3), it is zero at the end of the contract'. Proposition 2.3 (line 110): 'If total billing equals P "
        "and total revenue equals P, then D12 = 0.' The added condition is the proposition's hypothesis. Remark 2.4's 'can be "
        "large in between' is witnessed by the printed 32,792,272 peak.", None),
    "AC1b-cards-dup": ("PASS", "cards.json re-counted this round: 140 entries, 140 unique ids; lesson counts L04 20, L06 16, "
        "L05 14, matching the round-20 count. No card added or removed since fd9a9b7 (the diff changes only the grade and basis "
        "fields of AC1-c057, c071 and c087, and the back of c069).", None),
    "AC1b-slice-no-project": ("PASS", "Slice b has no project grader (check_projects.py --unit AC1 PASS, tools/check_projects output "
        "in ledgers/AC1/scripts/AC1-b-r21/out/check_projects.txt). Lab-twin mutants are out of scope by the architect ruling: "
        "a mutated twin that still exits 0 is not a finding unless a lesson sentence claims the property. No mutant needed.", None),
    "AC1b8-mutants-AC1-rerun": ("PASS", "Out of scope for slice b (no project grader in slice b). Project mutants "
        "(ledgers/AC1/mutants/, including the fix20d01-d10 and v20_m01-m06 files added since fd9a9b7) are the project slices' "
        "responsibility. Not re-run here.", None),
    "AC1b-cmd-pin": ("PASS", "git rev-parse --short HEAD = f95243f; git status shows no tracked modifications (out/pin.txt).", None),
    "AC1b-cmd-run_labs": ("PASS", "tools/run_labs.py --unit AC1 --page L04 / L05 / L06: each 'run_labs AC1: PASS (1/1)', exit 0 "
        "(out/run_labs_L04.txt, run_labs_L05.txt, run_labs_L06.txt).", None),
    "AC1b-cmd-twins": ("PASS", ".venv/bin/python -I -W error on tests/labs/AC1/lab-AC1-L04-1.py, L05-1.py, L06-1.py: exit 0 each "
        "(out/twin_L04.txt, twin_L05.txt, twin_L06.txt). Outputs match the pages' pre.expected blocks (AC1b-num rows).", None),
    "AC1b-cmd-check_pages": ("PASS", "tools/check_pages.py --unit AC1: 'check_pages AC1: PASS', exit 0 (out/check_pages.txt).", None),
    "AC1b-cmd-check_dag": ("PASS", "tools/check_dag.py --unit AC1: 'check_dag AC1: PASS', exit 0 (out/check_dag.txt).", None),
    "AC1b-cmd-check_projects": ("PASS", "tools/check_projects.py --unit AC1: 'check_projects AC1: PASS', exit 0 (out/check_projects.txt).", None),
    "AC1b-cmd-page_smoke": ("PASS", "tools/page_smoke.py --unit AC1 --pages L04 L05 L06: 'page_smoke AC1: PASS', exit 0 "
        "(out/page_smoke.txt).", None),
    "AC1b-cmd-lint-mypy": ("PASS", "ruff check tests/labs/AC1: 'All checks passed!'; ruff format --check: '11 files already "
        "formatted'; mypy --no-incremental tests/labs/AC1: 'Success: no issues found in 11 source files'; all exit 0 (out/ruff_check.txt, "
        "ruff_format.txt, mypy.txt).", None),
    "AC1b-cmd-verify_refs": ("PASS", "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0; "
        "tools/verify_refs.py --unit AC1 (live): '2 of 560 entries, 0 problems', exit 0 (out/verify_refs_offline.txt, "
        "verify_refs_live.txt). Slice b cites no registry key on its pages (AC1b-cit-none).", None),
    "AC1b-cmd-pytest": ("PASS", "pytest -q -k 'AC1 or lab': all dots, exit 0 (out/pytest.txt). pytest --collect-only -q -k 'AC1 or lab' "
        "exit 0; tests/test_page_smoke.py 2 and tests/test_run_labs.py 6 collected (out/collect.txt); no page in slice b states a "
        "test count.", None),
    "AC1b4-L05-misc1-peak": ("FAIL", "L05.html misconception 1 (line 357, changed): 'Under 0 percent upfront billing the same "
        "contract's balance became a contract asset in 8 months.' The lab prints months_with_contract_asset 8 (a count, twin_L05 "
        "line 'upfront_percent 0 ... months_with_contract_asset 8'). Recomputed in scratch (ledgers/AC1/scripts/AC1-b-r21/bal.py (output out/bal.txt)): the 0 percent "
        "balance is a contract asset first at month 2 and in months 2 to 9 (eight months). It did not become an asset at month 8. "
        "Also verified in the same sentence: 40 percent peak liability 32,792,272 at month 1, before month 12 (balance 0 at "
        "month 12); 'equal billing and revenue would need D_m = 0 in every month' correct. The sentence misstates the timing "
        "of the asset.",
        "Change to: 'Under 0 percent upfront billing the same contract's balance was a contract asset in 8 months, from month 2 "
        "to month 9.'"),
    "AC1b-num-L05-prose": ("FAIL", "L05.html interpretation (line 333): 'it is a contract asset in 8 months'; misconception 1 "
        "(line 357): 'became a contract asset in 8 months'. The lab prints the count 8 (months_with_contract_asset 8), but the "
        "phrasing states a time of onset, and the asset began at month 2 (balance -23,333,398 at month 2; scratch recompute). "
        "The other figures check: 0.6270 (50,471,362/80,495,111 = 0.62701), 0.2899 (23,333,398/80,495,111 = 0.28987), "
        "shares 0.0675 + 0.1173 + 0.3713 + 0.4439 = 1.0000, 20,583,168 = 6 x 452,837 + 6 x 2,977,691, and 2,717,022 + 17,866,146 "
        "= 20,583,168. Only the 8-months wording fails.",
        "Line 333 and line 357: replace 'a contract asset in 8 months' with 'a contract asset in 8 months, from month 2 to month 9' "
        "(or 'in eight of the twelve months, months 2 to 9')."),
    "AC1b-cards-L04-L06": ("FAIL", "cards.json entries re-read this round. AC1-c069 now matches L05.html line 124 (fixed); "
        "AC1-c057, c071 and c087 lost the grade C and basis fields and their backs still match Remark 1.2 / Section 4 (L04), Section 3 "
        "(L05 line 302-area text 'cites no primary text') and Section 3 (L06 line 301); grade is optional (check_pages.py 387-394). "
        "AC1-c070 (cards.json line 487) says 'At 0 percent it is a contract asset in 8 months', the same timing defect as "
        "AC1b21-L05-misc1 (row AC1b-num-L05-prose).",
        "AC1-c070 back: 'At 0 percent it is a contract asset in 8 months' to 'At 0 percent it is a contract asset in 8 months, "
        "months 2 to 9'."),
}

NEW_ROWS = [
    ("AC1b21-L05-misc2-title", "PASS",
     "L05.html misconception 2 title (line 360, changed): 'The two timing conventions give different total revenue for the same contract.'",
     "Body: Proposition 2.1 (line 96) says both conventions total P (the body's claim); convention 2 changes only timing (L05 line 92 "
     "convention definition); twin_L05 totals_equal_under_both_conventions True and revenue total 80,495,111 equals_price True; "
     "month_6_difference_cents 20583168. Title is the negation of the misconception and the body refutes it."),
    ("AC1b21-L05-misc1-since-clause", "PASS",
     "L05.html misconception 1 (line 357, changed): 'a contract liability of up to 32,792,272 cents at some month before month 12, since the balance is zero at month 12 (Proposition 2.3)'",
     "Recomputed: D_12 = 0 (Prop 2.3); the 40 percent balance is positive (liability) at months 0 to 11 with maximum 32,792,272 at month 1 (scratch). "
     "The reason given is valid: a positive maximum cannot sit at month 12 where the balance is zero."),
    ("AC1b21-L05-bullet-asset-only", "PASS",
     "L05.html section 4 bullet 3 (line 347, changed): 'a contract asset only under the 0 percent schedule'",
     "The 'only' is scoped to the lab's two billing schedules (40 and 0 percent). twin_L05 max_contract_asset_cents 0 at 40 percent, 23,333,398 at 0 percent. Restricting the word to 'the lab's two schedules' keeps it true."),
    ("AC1b21-L04-line331-cfo-bullet", "PASS",
     "L04.html section 5 bullet 2 (line 331, changed): 'Operating cash flow is not invariant to presentation.'",
     "Proposition 3.1 (line 304) with interest moved: twin_L04 cfo_presentation_1 24,513,189, cfo_presentation_2 27,832,482, difference 3,319,293 = interest_moved_total_cents; the general wording is witnessed by this non-zero case."),
    ("AC1b21-L04-line52-why", "PASS",
     "L04.html line 52 why-it-matters (changed): 'The lesson states no requirement of US GAAP or IFRS Standards, and it cites neither primary text.'",
     "Same content as Remark 1.2 (line 63) and the References block (line 560). The sentence no longer says the lesson 'does not state what' standards require; it says the lesson states no requirement, which Remark 1.2 supports."),
    ("AC1b21-card-c057", "PASS",
     "cards.json AC1-c057 (grade and basis fields removed; back unchanged)",
     "Back: 'This lesson does not say. It cites no primary text for the question, so the question stays open (Remark 1.2, Section 4).' Remark 1.2 (L04 line 63) and Section 4 (line 322) support it; key-results row (L04 line 477) says the same. A card with no result carries no grade (cards without grade are common in this file, e.g. c001 to c008)."),
    ("AC1b21-card-c071", "PASS",
     "cards.json AC1-c071 (grade and basis removed; back unchanged)",
     "Back matches L05 Section 3 paragraph (line 338): 'cites no primary text for them, so the four inputs stay open (Section 3)'. The four inputs in the front (obligations, timing, progress, stand-alone prices) are the four Section 3 names."),
    ("AC1b21-card-c087", "PASS",
     "cards.json AC1-c087 (grade and basis removed; back unchanged)",
     "Back: 'The lesson states none of them. It cites no primary text for them, so these decisions stay open (Section 3).' L06 Section 3 (line 301) lists the discount rate, initial asset, expense pattern, variable payments and options as open and states 'This lesson cites no primary text'."),
    ("AC1b21-card-c070", "FAIL",
     "cards.json AC1-c070 back (line 487), grade C",
     "'At 0 percent it is a contract asset in 8 months' (see AC1b-num-L05-prose). Recomputed: asset first at month 2, months 2 to 9. The count of 8 is right; 'in 8 months' states the timing wrongly."),
    ("AC1b21-L05-keyresult-row-line492", "FAIL",
     "L05.html key-results table row (line 492), grade C: 'under 0 percent it is a contract asset in 8 months'",
     "Same wording defect as AC1-c070 and the interpretation (line 333). The lab's printed count (8) and largest asset (23,333,398) are right; the timing phrase is not (asset first at month 2)."),
]

rows = []
for r in prev:
    rid = r["id"]
    if rid in NEW_EV:
        status, ev, fix = NEW_EV[rid]
    elif r["status"] == "PASS":
        status, ev, fix = "PASS", CARRY + " " + r["evidence"], None
    else:
        raise SystemExit(f"unhandled non-PASS prior row {rid}")
    out = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev}
    if fix:
        out["fix"] = fix
    rows.append(out)

seen = {r["id"] for r in rows}
for rid, status, loc, ev in NEW_ROWS:
    assert rid not in seen
    row = {"id": rid, "check": "AC1-b round 21 re-verification of a changed or new subject", "location": loc,
           "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = "Replace the 8-months timing wording with the months the lab counts (months 2 to 9)."
    rows.append(row)

frag = {
    "unit": "AC1",
    "slice": "AC1-b",
    "round": 21,
    "round_note": ("round 21: delta since the round-20 pin fd9a9b7 is L04.html line 52 (why-it-matters) and 331 (section 5 "
                   "bullet 2), L05.html lines 121 (Remark 2.4), 347 (section 4 bullet 3), 357 (misconception 1) and 360 "
                   "(misconception 2 title), and cards.json AC1-c057, c069, c071, c087. L06.html and the three twins are "
                   "byte-identical since fd9a9b7."),
    "verifier": "Haiku independent verifier for slice AC1-b, round 21; did not build AC1 and shares no context with its builders",
    "pin": "f95243f",
    "base": "fd9a9b7 (round-20 pin; /tmp/fanout-frags/AC1-b.round20.json is context only; carried PASS rows state the byte-identical condition)",
    "checkout": "/tmp/verify21-AC1-b (detached at f95243f; .venv symlink)",
    "scratch": "/tmp/AC1-v/AC1-b-r21",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b is pages and twins, not a project slice: no project grader, no student-error mutant and no alternative implementation is in scope. Lab twins are demonstrations (architect ruling), so a mutated twin that still exits 0 is not a finding.",
        "Lab output is SIMULATED (seeds 2604, 2605, 2606). Results read off a lab are grade C naming the lab; results proved on the page are T.",
        "The 8-months defect (AC1b21-L05-misc1 wording family) is the only FAIL cause beyond the round-20 card locator, which is fixed (AC1b-card-c069 PASS).",
        "Not checked: live reachability of any publisher or SEC source (no slice-b row cites one); hours on pace (architect ruling, not failed); carried rows were not re-read line by line where their cited lines are byte-identical since fd9a9b7.",
    ],
    "summary": "",
}
n = len(rows)
npass = sum(1 for r in rows if r["status"] == "PASS")
nfail = sum(1 for r in rows if r["status"] == "FAIL")
frag["summary"] = (f"AC1-b round 21 (L04, L05, L06 and twins; pin f95243f): {n} rows, {npass} PASS, {nfail} FAIL, 0 UNVERIFIABLE. "
                   "Verdict FAIL: the 8-months timing wording (L05 line 357, line 333, card AC1-c070, key-results row 492).")
out = ROOT / "ledgers/AC1/AC1-b.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", n, "pass", npass, "fail", nfail, "->", out)
