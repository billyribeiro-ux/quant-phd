"""Builds ledgers/AC1/AC1-a.json for round 12 from the round 11 fragment and the round 12 decisions."""
import json
import sys

PREV = "/tmp/fanout-frags/AC1-a.round11.json"
OUT = sys.argv[1]
prev = json.load(open(PREV))
CP = ("Carried from round 11 (cited passage byte-identical since the previous pin; none of the changed hunks "
      "index.html 141, L01.html 51 and 559, L02.html 552, L03.html 57, 603-625 and 668, cards.json c007 and c127, "
      "twin lab-AC1-L03-1.py 447-468 lies in it; L03 lines after 603 are now +7): ")
R = "Re-verified at aebdc15 (/tmp/verify12-AC1-a, /tmp/ac1-v/a-r12/): "

PASS, FAIL = "PASS", "FAIL"
# Decisions: id -> (status, evidence) for re-verified rows; absent id -> carried from round 11 with CP prefix.
D = {
 "AC1a-cmd-check_pages": (PASS, "Run at aebdc15: 'check_pages AC1: PASS', exit 0 (/tmp/ac1-v/a-r12/check_pages.out)."),
 "AC1a-cmd-check_dag": (PASS, "Run at aebdc15: 'check_dag AC1: PASS', exit 0 (/tmp/ac1-v/a-r12/check_dag.out). check_dag does not test term order; see AC1a-dag-concepts."),
 "AC1a-cmd-run_labs": (PASS, "Run at aebdc15: 'run_labs AC1: PASS (11/11)', exit 0 (/tmp/ac1-v/a-r12/run_labs.out)."),
 "AC1a-cmd-page_smoke": (PASS, "Run at aebdc15: 'page_smoke AC1: PASS' for index, L01, L02, L03, exit 0 (/tmp/ac1-v/a-r12/page_smoke.out)."),
 "AC1a-cmd-verify_refs": (PASS, "Run at aebdc15: live 'verify_refs --unit AC1' '2 of 560 entries, 0 problems'; offline '560 entries, 0 problems' (/tmp/ac1-v/a-r12/verify_refs_live.out, verify_refs_offline.out). references/, tools/, curriculum/, notation/ and atlas/ have an empty git diff from 91946cf to aebdc15."),
 "AC1a-cmd-ruff-mypy": (PASS, "Run at aebdc15: ruff check 'All checks passed!'; ruff format --check '212 files already formatted'; mypy --no-incremental 'Success: no issues found in 153 source files'; all exit 0 (/tmp/ac1-v/a-r12/ruff.out, ruff_fmt.out, mypy.out)."),
 "AC1a-cmd-twin-run": (PASS, "Run at aebdc15: python -I -W error on lab-AC1-L01-1.py, L02-1 and L03-1, each exit 0 (/tmp/ac1-v/a-r12/twin_L01.out, twin_L02.out, twin_L03.out)."),
 "AC1a-cmd-pytest-AC1": (PASS, "Run at aebdc15: pytest -q tests -k 'AC1 or lab': all passed, exit 0 (/tmp/ac1-v/a-r12/pytest.out); pytest --co -k 'AC1 or lab' collects 143, the same count as round 11."),
 "AC1a-cmd-build-site": (PASS, "Run at aebdc15: tools/build_site.py --check 'site data current: 6 outputs', exit 0 (/tmp/ac1-v/a-r12/build_site.out)."),
 "AC1a-cmd-scope-witness": (PASS, "Run at aebdc15: ledgers/AC1/scripts/AC1-a-r11/witness_r11.py with python -I: ALL PASS (/tmp/ac1-v/a-r12/witness_r11.out). Hypothesis (i) of Proposition 3.2 (L01.html line 388) is witnessed by the hub rung-2 row AC1a-r10-hub-rung2-explain-scope."),
 "AC1a-twin-matches-page": (PASS, "Re-run at aebdc15: ledgers/AC1/scripts/AC1-a-r12/cmp_code.py: data-run block equals the twin for L01, L02 and L03 (all True); cmp_expected.py: the expected block equals the twin stdout for L01, L02 and L03 (all True). The changed L03 output line 'checks 1 to 4 hold in every year: True' (L03.html 668) equals the twin line."),
 "AC1a-cite-none": (PASS, "Re-checked at aebdc15: zero data-cite, class=\"cite\" or data-key markup in index.html, L01.html, L02.html, L03.html."),
 "AC1a-lab-seeded-offline": (PASS, "Re-checked at aebdc15: the three twins import only random and dataclasses (twin lines 12-13, 17-18, 14-15), SEED = 20261027, no network call; each ran under python -I -W error exit 0. The L03 twin change adds no import."),
 "AC1a-num-hub": (PASS, "Re-derived at aebdc15: hub 90 + 30 = 120; 30/120 = 25.0%; 80% of 9 = 7.2, so eight correct; 7/9 = 77.8%; lesson hours 11+12+11+11+12+12+11+10 = 90. Line 141 (the only changed hub line) recomputed: 2,500 - 1,900 = 600."),
 "AC1a-hours-hub": (PASS, "Re-checked at aebdc15: hub split L01 11 h, L02 12 h, L03 11 h; data-hours L01 11, L02 12, L03 11 (grep); lesson hours sum 90 equals the hub split. Hours are design targets, not judged on pace."),
 "AC1a-hours-L01": (PASS, "Re-checked at aebdc15: L01.html data-hours=\"11\"."),
 "AC1a-hours-L02": (PASS, "Re-checked at aebdc15: L02.html data-hours=\"12\"."),
 "AC1a-hours-L03": (PASS, "Re-checked at aebdc15: L03.html data-hours=\"11\"."),
 "AC1a-struct-lessons": (PASS, "Re-checked at aebdc15: check_pages PASS for L01-L03; the diff adds no heading or section and removes none (hunks listed in AC1a-r12-delta)."),
 "AC1a-struct-hub": (PASS, "Re-checked at aebdc15: check_pages PASS for the hub; index.html has one changed line (141), inside the explain of the rung-2 item."),
 "AC1a-notation": (PASS, "Re-checked at aebdc15: the TeX spans of the four pages use only \\Delta, \\blacksquare, \\dots, \\in, \\le, \\sum, \\text, \\times (scan.py); none of the registered macros of notation/notation.json is used. No changed hunk contains TeX."),
 "AC1a-banned-phrases": (PASS, "Re-scanned at aebdc15 with ledgers/AC1/scripts/AC1-a-r12/scan.py over index.html, L01-L03.html and cards.json for roughly, about <digit>, historically, typically, generally, usually, as much as, drives, offsets, builder, verifier, round <digit>, REQUEST, unit report, ellipses, clearly, obviously, simply, half of, most, often. Hits are reviewed: 'at most one side' (L01 Definition 1.1 and Remark 2.2 wording), 'half of' as fraction wording, Python '...' type hints, and 'offsets' (L03 misconception 2 and card AC1-c037; computed fact, unchanged). None is a banned phrase or an omitted-content ellipsis."),
 "AC1a-L01-timings-balances": (PASS, "Re-derived at aebdc15: Example 3.3 (L01.html line 400): 192,834.97 + 21,046.51 = 213,881.48; 154,267.97 + 21,046.51 = 175,314.48; 213,881.48 - 175,314.48 = 38,567.00. Example text unchanged in this delta."),
 "AC1a-L01-key-scope": (PASS, "Re-verified at aebdc15: the Key results table row at L01.html line 559 (changed) is the posting row, verified in AC1a-r12-L01-559-posting-row; rows at lines 560-561 are byte-identical to 91946cf and state the SIMULATED revenue difference 38,567.00 and the convention of Section 1."),
 "AC1a-r8-L03-theorem-para": (PASS, "Re-read at aebdc15 (L03.html line 135): 'The lab checks four of its five parts'; Check 1 prints gaps 0.00 at each year end (twin output lines 2-5); Checks 2, 3 and 4 print True (twin lines 15, 18-23, 26-28). Theorem 5.1 (line 127) has five claims; the lab omits the investing and financing equalities, so four of five is correct."),
 "AC1a-r11-cards-c127-c128": (PASS, "Re-verified at aebdc15: c127 changed in this delta and is verified in AC1a-r12-cards-c127; c128 (cards.json) says 'four of the five parts' and 'Checks 1 to 4', matching line 135 and the twin output."),
 "cards-L01-all": (PASS, "Re-verified at aebdc15: AC1-c007 (changed) verified in AC1a-r12-cards-c007 against L01.html line 87 and the lab output ('entries before 7, after 7'); the other L01 cards are carried (L01.html lines they cite are byte-identical since 91946cf)."),
 "cards-L03-all": (PASS, "Re-verified at aebdc15: AC1-c127 (changed) verified in AC1a-r12-cards-c127; AC1-c128 matches line 135 and the twin output; the other L03 cards are carried."),
 "cards-L03-theorem-5-1-print-claim": (PASS, "Re-read at aebdc15: L03.html line 135, the paragraph after Theorem 5.1, unchanged in this delta and matching the cards that cite it."),
 "cards-duplicate-scan": (PASS, "Re-run at aebdc15: cards.json holds 128 entries (AC1-c001 to AC1-c128), 128 unique ids and 128 unique fronts (python -I scan). Round 11's text said 126 unit cards; that count was wrong in the round 11 evidence (the file has 128 entries, of which 50 belong to L01-L03)."),
 "AC1a-r9-delta": (PASS, "Historical round 9 record. Superseded for this round by AC1a-r12-delta, which reads every hunk of 91946cf..aebdc15 for the slice; the rows it lists are carried or re-verified individually."),
 "AC1a-r3-delta": (PASS, "Historical round 3 record. Superseded for this round by AC1a-r12-delta; the cited passages are re-checked as individual rows."),
 "AC1a-r4-delta": (PASS, "Historical round 4 record. Superseded for this round by AC1a-r12-delta."),
 "AC1a-r5-delta": (PASS, "Historical round 5 record. Superseded for this round by AC1a-r12-delta."),
 "AC1a-r6-delta": (PASS, "Historical round 6 record. Superseded for this round by AC1a-r12-delta."),
 "AC1a-r8-delta": (PASS, "Historical round 8 record. Superseded for this round by AC1a-r12-delta."),
 "AC1a-r8-mutants-not-required": (PASS, "Re-checked at aebdc15: the slice is lessons plus the hub, not a project slice; ledgers/AC1/mutants/ mutates the AC1-d project grader and is out of scope here. No mutant is required or listed for AC1-a."),
 "AC1a-r10-hub-rung2-explain-scope": (PASS, "Previously FAIL (round 11). Fixed at aebdc15: index.html line 141 now states hypotheses (i) to (iii) of Proposition 3.2 (L01.html line 388: AR debits are credit sales, AR credits are collections, no write-offs; revenue = credit + cash sales; cash from customers = cash sales + collections), then 2,500 - 1,900 = 600, and says (iv) and (v) are not used. These match the Proposition text word for word in substance; the explanation's conclusion holds under (i) to (iii) because the proof uses only those. Arithmetic re-derived."),
 "AC1a-r10-witness-w1-w6": (PASS, "Re-run at aebdc15: ledgers/AC1/scripts/AC1-a-r10/witness_r10.py /tmp/verify12-AC1-a/ exit 0; W1-W6 print their results (W4 prints 'interest or tax account present: False', the expected value), W6 'data-run equals twin: True' for L01, L02, L03 (/tmp/ac1-v/a-r12/witness_r10.out)."),
 "AC1a-r11-delta": (PASS, "Round 11 delta record. Its hunks were changed again in aebdc15 (index 141, L01 51 and 559, L02 552, L03 57 and 603-668, cards c007 and c127, twin 447-468); every one is read in AC1a-r12-delta."),
 "AC1a-r11-L03-check6-wording": (PASS, "Re-run at aebdc15: cmp_expected.py reports the page expected block equal to the twin stdout for L03 (all True); the Check 6 line (twin line 444, unchanged) is identical in page and twin; the four gaps 1,000,000.00, 1,300,000.00, 1,300,000.00 and 200,000.00 are in the output (twin lines 37-42)."),
 "AC1a-r11-banned-process-words": (PASS, "Re-run at aebdc15 with ledgers/AC1/scripts/AC1-a-r12/scan.py over index.html, L01-L03.html and cards.json: no 'builder', 'verifier', 'round <digit>', 'REQUEST' or 'unit report' in learner text; 'offsets' (L03 misconception 2, card AC1-c037) is a computed statement, unchanged."),
 "AC1a-r11-notation": (PASS, "Re-run at aebdc15: TeX spans in the four pages use only operators and no registered macro (scan.py output 'macros' list)."),
 "AC1a-r11-mutants-na": (PASS, "Not applicable: lesson slice, no project grader in this slice. No mutant is listed for AC1-a in round 12."),
 "AC1a-r11-witness-arithmetic": (PASS, "Re-run at aebdc15: ledgers/AC1/scripts/AC1-a-r11/witness_r11.py with python -I: ALL PASS, including L02 2025 check 1,003,421.14 + 1,000,000 - 515,320.87 + 166,205.02 = 1,654,305.29, L03 Check 4 4,454,305.29 + 1,491,615.64 = 5,945,920.93, and the Check 6 gaps 891,615.64 and 200,000.00 (/tmp/ac1-v/a-r12/witness_r11.out)."),
 "AC1a-r8-concept-index": (PASS, "Re-run at aebdc15: tools/build_site.py --check 'site data current: 6 outputs' (/tmp/ac1-v/a-r12/build_site.out); concepts.html is generated and is current."),
 "AC1a-dag-concepts": (FAIL, "Re-verified at aebdc15: check_dag passes, but the rewritten L03.html Definition 1.1 (line 57, the statement-articulation definition) uses 'depreciation' before the lesson introduces it. L03.html line 38 lists 'Introduces: ... depreciation and amortization', and the dfn of depreciation is Definition 1.2 at line 62 (data-concept depreciation-and-amortization). BUILDER_RULES 10 ('No concept used before it is introduced') is broken; the convention used for this term elsewhere is a forward pointer (L02.html line 73: 'Depreciation ... is given in Lesson 3 (Definition 1.2 there)'), which line 57 lacks. Fix: change line 57 to 'adding back depreciation (Lesson 3, Definition 1.2)'. The 'indirect method' term carries its forward pointer '(Definition 2.1, the indirect method)' and is acceptable."),
 "AC1a-L03-as-much-as": (PASS, "Re-scanned at aebdc15: no 'as much as' in L03.html (scan.py over the four pages); the interpretation paragraph at L03.html line 669 is unchanged text."),
}
NEW = [
 {"id": "AC1a-r12-delta", "check": "Round 12 delta 91946cf..aebdc15 for the slice, every hunk read",
  "location": "index.html line 141; L01.html lines 51 and 559; L02.html line 552; L03.html lines 57, 603-625 (code, comment, flag), 668 (printed line); tests/labs/AC1/lab-AC1-L03-1.py lines 447-468; cards.json c007 and c127",
  "status": PASS, "evidence": "git diff --stat 91946cf aebdc15 for the slice lists these files; each hunk was read in full (git diff 91946cf aebdc15 -- course/modules/AC/AC1 tests/labs/AC1). The AC1 grader/test_project.py and project.html hunks belong to the project slice and were not judged in this slice. No other AC1-a file changed. The hunks are listed here so that every changed sentence has a row."},
 {"id": "AC1a-r12-index-141-rung2", "check": "Hub rung-2 explanation after the round 11 fix",
  "location": "course/modules/AC/AC1/index.html line 141; L01.html line 388 (Proposition 3.2)",
  "status": PASS, "evidence": "The explanation names hypotheses (i) (AR debits only credit sales, AR credits only collections, no write-offs), (ii) (revenue = credit sales + cash sales) and (iii) (cash from customers = cash sales + collections); these match Proposition 3.2 (L01.html line 388) word for word in substance. It states (iv) and (v) are not used; the proof of the AR identity (L01.html line 393) uses only (i) to (iii). 2,500 - 1,900 = 600 (computed). Witness ledgers/AC1/scripts/AC1-a-r10/witness_r10.py and the hub witness in witness_r11.py confirm the earlier omission."},
 {"id": "AC1a-r12-L01-559-posting-row", "check": "Key results row: a balanced entry posted to the wrong account passes the check (Remark 2.2)",
  "location": "course/modules/AC/AC1/L01.html line 559; Remark 2.2 (line 103); Definition 1.1 (line 72); lab check_entry (tests/labs/AC1/lab-AC1-L01-1.py lines 46-58)",
  "status": PASS, "evidence": "Remark 2.2 lists four tests: each entry balances, its accounts exist, each amount is a non-negative integer number of cents, and no line carries both a debit and a credit; it says a line with neither side is not refused. The row's list matches these four. Definition 1.1 states balance, non-negative integer cents and 'either a debit or a credit' per line (one side per line). The lab's check_entry tests the account (line 52), the amount type and sign (line 55), both sides on one line (line 57, 'if line.debit and line.credit') and the balance (line 61); a line with neither side passes, as stated. Lab output 'ValueError' lines for the unbalanced, unknown-account and fractional tests (/tmp/ac1-v/a-r12/twin_L01.out) agree."},
 {"id": "AC1a-r12-L01-51-why-it-matters", "check": "Why-it-matters paragraph: 'each entry's two sides carry equal totals'",
  "location": "course/modules/AC/AC1/L01.html line 51",
  "status": PASS, "evidence": "Restates the balance rule of Definition 1.1 and Proposition 2.1 (L01.html line 91: total debits equal total credits). No new term."},
 {"id": "AC1a-r12-L03-def11-articulation-rewrite", "check": "Definition 1.1 (articulation): indirect operating cash flow by adding back depreciation and adjusting for receivables and payables",
  "location": "course/modules/AC/AC1/L03.html line 57; Definition 2.1 (line 71); Proposition 2.2 (line 76)",
  "status": PASS, "evidence": "The identity stated is the one of Definition 2.1 (net income + depreciation - increase in receivables + increase in payables) and the equality with the direct method is the conclusion of Proposition 2.2 under its hypotheses (line 76). The pointers '(Propositions 2.2, 3.1, 4.1 and 4.2)' and '(Definition 2.1, the indirect method)' are forward pointers to this lesson's results, the same convention as earlier rounds accepted. The term-order defect of the word 'depreciation' on this line is recorded in AC1a-dag-concepts (FAIL)."},
 {"id": "AC1a-r12-L03-code-and-output-checks", "check": "Lab 3 articulation flag and comment after the round 12 change",
  "location": "tests/labs/AC1/lab-AC1-L03-1.py lines 450-465; course/modules/AC/AC1/L03.html lines 606-621 and 668; twin output /tmp/ac1-v/a-r12/twin_L03.out",
  "status": PASS, "evidence": "The comment 'Checks 1 to 4 as printed above' is accurate: Check 1 prints the balance gap 0.00 for 2024-2027 (output lines 2-5); Check 2 prints 'indirect equals direct: True' (line 15); Check 3 prints True for retained earnings and net equipment (lines 18-23, including the equipment roll-forward the flag adds); Check 4 prints True (lines 26-28). The flag adds the balance identity for the year ends in YEARS, which Check 1 prints as gaps, and the equipment identity, which Check 3 prints. The investing and financing equalities are not in the flag and the comment says so. The printed line 'checks 1 to 4 hold in every year: True' (output line 44) matches the page (cmp_expected.py)."},
 {"id": "AC1a-r12-cards-c007", "check": "Card AC1-c007: double-entry rule enforced at posting",
  "location": "course/modules/AC/AC1/cards.json AC1-c007; L01.html line 87",
  "status": PASS, "evidence": "The card's new back ('In this lab the rule is enforced at posting: an entry that is not balanced is refused, and the ledger is left unchanged (Section 2)') matches L01.html line 87 word for word in substance. The lab's post refuses an unbalanced entry (check_entry line 61; post at line 70) and the output reads 'entries before 7, after 7' after the malformed entries (twin_L01.out)."},
 {"id": "AC1a-r12-cards-c127", "check": "Card AC1-c127: Check 2 is evidence, not an independent test of the theorem",
  "location": "course/modules/AC/AC1/cards.json AC1-c127; L03.html line 135 (the paragraph after Theorem 5.1)",
  "status": PASS, "evidence": "The new back text ('It is not an independent test of the theorem, which the proof already gives (Section 5)') matches the sentence in L03.html line 135. Check 2 prints 'indirect equals direct: True' (twin line 15). The grade C and basis (Lab 3 SIMULATED; the paragraph after Theorem 5.1) are correct."},
 {"id": "AC1a-r12-L02-552-prop32-scope", "check": "L02 bullet on what Proposition 3.2 does and does not cover (inventory, intangibles, taxes, interest)",
  "location": "course/modules/AC/AC1/L02.html line 552; Proposition 3.2 (line 97); Remark 3.3 (line 107); Definition 2.1 (line 72-76)",
  "status": PASS, "evidence": "'Inventory and intangible assets are balance-sheet accounts that Proposition 3.2 does not name': Proposition 3.2's hypotheses name only balanced entries, the equity accounts and the revenue and expense accounts (line 97), and Remark 3.3 (line 107) says no inventory or other balance-sheet account is needed. 'Covered if it meets the hypotheses' is a conditional and is true. 'An intangible asset that is amortized brings in an expense account outside the four of Definition 2.1' is true: the four accounts are S, K, O and D (line 76). Taxes and interest unchanged. The term 'amortized' is the subject of AC1a-r12-L02-552-amortized-term."},
 {"id": "AC1a-r12-L02-552-amortized-term", "check": "Term 'amortized' used in Lesson 2 before the lesson that introduces it",
  "location": "course/modules/AC/AC1/L02.html line 552; course/modules/AC/AC1/L03.html line 38 (Introduces) and line 62 (Definition 1.2)",
  "status": FAIL, "evidence": "The rewritten bullet at L02.html line 552 uses 'An intangible asset that is amortized' in Lesson 2. Amortization is introduced in Lesson 3: L03.html line 38 ('Introduces: ... depreciation and amortization') and the dfn at line 62. The only earlier mention of depreciation in Lesson 2 carries a forward pointer (L02.html line 73: 'Depreciation ... is given in Lesson 3 (Definition 1.2 there)'); the amortized clause has none. BUILDER_RULES 10 ('No concept used before it is introduced') is broken. Fix: 'An intangible asset that is amortized (Lesson 3, Definition 1.2) brings in an expense account outside the four of Definition 2.1'."},
]

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in D:
        st, ev = D[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": R + ev})
    else:
        ev = CP + r["evidence"]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})
for n in NEW:
    rows.append({"id": n["id"], "check": n["check"], "location": n["location"], "status": n["status"], "evidence": n["evidence"]})

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
for rid in prev_ids if False else []:
    pass
missing = [r["id"] for r in prev["rows"] if r["id"] not in ids]
assert not missing, missing
unused = [k for k in D if k not in {r["id"] for r in prev["rows"]}]
frag = {
 "unit": "AC1", "slice": "AC1-a", "round": 12,
 "round_note": "round 12 independent verification of AC1-a at aebdc15. Previous pin 91946cf (round 11 fragment, verdict FAIL, 1 FAIL row). Delta 91946cf..aebdc15 for this slice: index.html line 141; L01.html lines 51 and 559; L02.html line 552; L03.html lines 57, 603-625 and 668; cards.json c007 and c127; tests/labs/AC1/lab-AC1-L03-1.py lines 447-468. Every hunk was read (row AC1a-r12-delta). Previous PASS rows whose cited passage is outside every hunk are carried with the prefix 'Carried from round 11'; rows whose subject touches a hunk, or that are command runs, were re-verified in this round.",
 "verifier": "Haiku independent verifier, AC1-a round 12 (did not build AC1)",
 "pin": "aebdc15",
 "base": "91946cf (previous verified pin; round 11 fragment)",
 "checkout": "/tmp/verify12-AC1-a (detached worktree at aebdc15, .venv symlinked)",
 "scratch": "/tmp/ac1-v/a-r12",
 "verified_at": "2026-10-28",
 "registry_flags": ["references/references.json and tools/, notation/, curriculum/ unchanged in 91946cf..aebdc15 (empty git diff); live verify_refs --unit AC1 '2 of 560 entries, 0 problems'; offline '560 entries, 0 problems'. No citation markup in the four pages."],
 "freshness_flags": [],
 "notes": [
  "Slice: course/modules/AC/AC1/index.html, L01.html, L02.html, L03.html, the three lab twins tests/labs/AC1/lab-AC1-L01-1.py, lab-AC1-L02-1.py, lab-AC1-L03-1.py, and the L01-L03 cards of cards.json (AC1-c001 to c045, c123, c124, c126 to c128). The AC1 grader/test_project.py and project.html hunks in the same delta belong to the project slice and are not judged here.",
  "Line numbers: in aebdc15 the L03.html lines after 603 are shifted by +7 relative to 91946cf (hunk @@ -603,15 +603,22 @@). Carried rows keep their round 11 locators; the text they cite is unchanged.",
  "Carry rule: a previous PASS row is carried only when the passage it cites lies outside every changed hunk listed in round_note (the CP prefix states this). Rows that cite a command, a witness, a card or a passage that touches a hunk were re-run or re-verified.",
  "Mutants: none for this slice. The slice is lessons and the hub, not a project; ledgers/AC1/mutants/ belongs to the AC1-d project grader. No new mutant and no alternative implementation applies to this slice.",
  "Round 11 evidence said '126 unit cards'; cards.json holds 128 entries with unique ids and fronts (row cards-duplicate-scan). The count of 126 in round 11 was not reproduced.",
  "Witness scripts: ledgers/AC1/scripts/AC1-a-r12/scan.py (banned-phrase, process-word and macro scan), cmp_code.py and cmp_expected.py (twin-to-page equality, paths set to the checkout). ledgers/AC1/scripts/AC1-a-r12/build_fragment_r12.py builds this fragment.",
  "Could not check: no external source is cited by the four pages (no registry key), so no reading of any paper or standard was possible or needed; the Proposition 3.2 hypothesis set is read from the pages only.",
  "Hours: hub split 90 lesson hours and 30 project hours; lesson hours L01 11, L02 12, L03 11 (34 of the 90 shown in the hub split by lesson). Arithmetic consistent; not judged against pace (architect ruling).",
 ],
 "mutants": [],
 "summary": {},
 "verdict": None,
 "rows": rows,
}
frag["summary"] = {"rows": len(rows), "pass": sum(r["status"] == PASS for r in rows), "fail": sum(r["status"] == FAIL for r in rows), "unverifiable": 0}
frag["verdict"] = "PASS" if all(r["status"] == PASS for r in rows) else "FAIL"
json.dump(frag, open(OUT, "w"), indent=1, ensure_ascii=False)
print("rows", len(rows), frag["summary"], frag["verdict"], "unused decisions:", unused)
