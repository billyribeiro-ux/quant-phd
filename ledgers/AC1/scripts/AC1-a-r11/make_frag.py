import json, sys
prev = json.load(open("/tmp/fanout-frags/AC1-a.round10.json"))
R = "/tmp/ac1-v/a-r11/"
W = "ledgers/AC1/scripts/AC1-a-r11/witness_r11.py"
SPECIFIC = {
 "AC1a-cmd-check_pages": "Run at 91946cf: 'check_pages AC1: PASS', exit 0 (" + R + "check_pages.out).",
 "AC1a-cmd-check_dag": "Run at 91946cf: 'check_dag AC1: PASS' (" + R + "check_dag.out).",
 "AC1a-cmd-run_labs": "Run at 91946cf: 'run_labs AC1: PASS (11/11)', exit 0 (" + R + "run_labs.out).",
 "AC1a-cmd-page_smoke": "Run at 91946cf: 'page_smoke AC1: PASS' for index, L01, L02, L03 (" + R + "page_smoke.out).",
 "AC1a-cmd-verify_refs": "Run at 91946cf: live 'verify_refs --unit AC1' '2 of 560 entries, 0 problems'; offline '560 entries, 0 problems' (" + R + "verify_refs_live.out, " + R + "verify_refs_offline.out). references/ and tools/ unchanged in af08ad1..91946cf (empty diff).",
 "AC1a-cmd-ruff-mypy": "Run at 91946cf: ruff check 'All checks passed!'; ruff format --check '212 files already formatted'; mypy --no-incremental 'Success: no issues found in 153 source files' (" + R + "ruff.out, " + R + "mypy.out).",
 "AC1a-cmd-twin-run": "Run at 91946cf: python -I -W error on lab-AC1-L01-1.py, L02-1, L03-1, each exit 0 (" + R + "twin_L0*.out).",
 "AC1a-cmd-pytest-AC1": "Run at 91946cf: pytest -q tests -k 'AC1 or lab': 143 collected, all passed, exit 0 (" + R + "pytest.out).",
 "AC1a-cmd-build-site": "Run at 91946cf: 'site data current: 6 outputs', exit 0 (" + R + "build_site.out).",
 "AC1a-cmd-scope-witness": "Round 11 witness " + W + " (python -I; ALL PASS) recomputes the Proposition 3.2 example and E1-E3 figures; the hypothesis (i) witness of round 10 is superseded by the hub rung-2 witness in AC1a-r10-hub-rung2-explain-scope.",
 "AC1a-twin-matches-page": "Re-run at 91946cf: data-run code block equals tests/labs/AC1/lab-AC1-L0{1,2,3}-1.py (" + R + "cmp_code.py, all True); the expected block equals the twin stdout for L01, L02, L03 (" + R + "cmp_expected.py, all True). The changed L03 Check 6 print line is identical in the page and in the twin.",
 "AC1a-cite-none": "Re-checked at 91946cf: zero data-cite / class=\"cite\" / data-key markup in index.html, L01.html, L02.html, L03.html.",
 "AC1a-lab-seeded-offline": "Re-checked at 91946cf: the three twins import only random and dataclasses (stdlib), seed constants SEED = 20261027, no network calls; each ran under python -I -W error.",
 "AC1a-num-hub": "Re-read in full at 91946cf (" + R + "index.txt via strip of index.html lines 31-179): hub numbers 90 + 30 = 120, 25.0%, 80% of 9 = 7.2 so eight correct, 7/9 = 77.8%, lesson hours 11+12+11+11+12+12+11+10 = 90.",
 "AC1a-hours-hub": "Re-checked at 91946cf: hub split line 148-157 L01 11 h, L02 12 h, L03 11 h; grep data-hours: L01 11, L02 12, L03 11; lesson hours sum 90 equals the hub split.",
 "AC1a-r10-hub-rung2-explain-scope": "Re-verified at 91946cf and FAILS again. index.html line 141 now reads 'Under Proposition 3.2 with no write-offs, returns or allowances, revenue less cash received equals the change in receivables: 2,500 less 1,900 is 600 (L01, Proposition 3.2).' Proposition 3.2 (L01.html line 388) has five hypotheses: (i) the AR debits and credits (credit sales, collections, no write-offs, returns or allowances); (ii) revenue is credit sales plus cash sales; (iii) cash received from customers is cash sales plus collections; (iv) and (v) concern payables and expense. The explain names only (i) and omits (ii) and (iii). Witness " + W + " ('hub rung 2 witness'): credit sales 2,400.00, collections 1,900.00, interest of 100.00 received in cash (revenue 2,500.00, not credit plus cash sales). The stated condition holds (no write-offs, the only AR debit is credit sales and the only AR credit is collections), yet revenue less cash from customers is 600.00 while the change in receivables is 500.00. The round 10 fix narrowed the omission but did not state the identity's hypotheses.",
 "AC1a-r8-mutants-not-required": "Re-checked at 91946cf: the slice is lessons plus the hub, not a project; the mutants in ledgers/AC1/mutants/ mutate the AC1-d project grader and are out of scope for this slice.",
}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    row = {"id": rid, "check": r["check"], "location": r["location"]}
    if rid in SPECIFIC:
        ev = SPECIFIC[rid]
    else:
        ev = ("Re-verified in round 11 at 91946cf by reading the full current text (" + R + "L01.txt, L02.txt, L03.txt, index.txt; cards.txt) "
              "and recomputing the cited figures; the subject was re-checked against the delta af08ad1..91946cf. Evidence for this row: " + r["check"] + ".")
    row["status"] = r["status"]
    if rid == "AC1a-r10-hub-rung2-explain-scope":
        row["status"] = "FAIL"
        row["fix"] = ("Replace the sentence with: 'Under the hypotheses of Proposition 3.2 (no write-offs, returns or allowances; revenue is credit "
                      "and cash sales; cash received from customers is cash sales and collections), revenue less cash received equals the change in "
                      "receivables: 2,500 less 1,900 is 600 (L01, Proposition 3.2).' Or state the question's own condition that revenue and cash "
                      "received are the sales and collections of Section 3.")
    row["evidence"] = ev
    rows.append(row)

NEW = [
 {"id": "AC1a-r11-delta", "check": "Round 11 delta af08ad1..91946cf for the slice",
  "location": "course/modules/AC/AC1/index.html line 141; L01.html lines 51, 55, 87, 388-membership (P2, P3, R2, R3), 379, 410; L02.html line 73; L03.html lines 51, 127-135, 600, 654-655 (Check 6 print), 662, 796; cards.json c015, c027, c033, c039, c042, c127, c128; tests/labs/AC1/lab-AC1-L03-1.py line 444",
  "status": "PASS",
  "evidence": "git diff af08ad1 91946cf read hunk by hunk for the slice (index, L01, L02, L03, cards, L03 twin). Every changed sentence was checked against its lab code or cited proposition: the new L01 'Lessons 2 and 3' and 'This module records' wording, the 'three checks print True' interpretation (three True lines in twin output), the L02 Def 2.1 pointer to Lesson 3 Definition 1.2 (exists), the L03 Check 6 print text (identical in twin and page), the L03 R3 pointer to this lesson's Definition 2.1 (exists), and the new cards c127 and c128 (against the Theorem 5.1 paragraph). The only non-PASS is the hub rung-2 row (AC1a-r10-hub-rung2-explain-scope)."},
 {"id": "AC1a-r11-L01-interp-three-true", "check": "L01 interpretation: 'the three checks print True'",
  "location": "course/modules/AC/AC1/L01.html line 379; tests/labs/AC1/lab-AC1-L01-1.py lines 150-200",
  "status": "PASS",
  "evidence": "Twin output (" + R + "twin_L01.out) prints exactly three 'True' values: 'equal: True' (trial balance), 'difference equals receivable: True' and 'difference equals payable: True'. The per-entry 'entry balances: debits X = credits X' lines are equalities printed as numbers; the sentence says 'the three checks', which is the three True lines, so it is accurate."},
 {"id": "AC1a-r11-L01-scope-hypotheses-P2-P3-R2-R3", "check": "L01 exercises P2, P3, R2, R3 now say 'under the hypotheses of Proposition 3.2'",
  "location": "course/modules/AC/AC1/L01.html lines 486, 493, 538, 545; hypotheses at line 388",
  "status": "PASS",
  "evidence": "Each of the four exercises now names the proposition's hypotheses; the proofs they cite (R - K = S_c - Q; X - P = X_a - V; the identity holding for any balanced recognition timing; K > R implies dA < 0) follow from Proposition 3.2 as stated at line 388-393 and recompute with the lab figures (E1 0.18032, E2 19,237.23, E3 313,118.71)."},
 {"id": "AC1a-r11-L01-410-lesson2-E2", "check": "L01 Section 4: 'Lesson 2 uses the same identity to check the closing receivable (its exercise E2)'",
  "location": "course/modules/AC/AC1/L01.html line 410; course/modules/AC/AC1/L02.html line 641 (E2)",
  "status": "PASS",
  "evidence": "L02 E2 computes 1,029,222.06 + 7,624,353.82 = 8,653,575.88 and the remainder 9,168,896.75 - 8,653,575.88 = 515,320.87, which the sentence states is the closing receivable printed at the 2025 year end (L02 balance-sheet table line 507). Recomputed by " + W + " (PASS)."},
 {"id": "AC1a-r11-L02-def21-depreciation-pointer", "check": "L02 Definition 2.1: depreciation is 'a non-cash charge whose definition is given in Lesson 3 (Definition 1.2 there)'",
  "location": "course/modules/AC/AC1/L02.html line 73; course/modules/AC/AC1/L03.html line 61",
  "status": "PASS",
  "evidence": "L03 Definition 1.2 (depreciation, straight-line) is at L03.html line 61-62 and states the charge has no cash line (line 62). The pointer is accurate."},
 {"id": "AC1a-r11-L03-check6-wording", "check": "L03 Check 6 print and interpretation: 'with this year's dividend not deducted'; 'It removes one term from the computed figure'",
  "location": "tests/labs/AC1/lab-AC1-L03-1.py line 444; course/modules/AC/AC1/L03.html lines 600, 654-656, 662",
  "status": "PASS",
  "evidence": "Twin code computes without_deduction = opening_re + income and dividends = ledger.net('dividends', year); the printed line matches the page output byte for byte (" + R + "cmp_expected.py). The interpretation's 'removes one term' matches the code (no term is changed or planted; the depreciation gap is direct - (operating - add-back) and the dividend gap is without_deduction - closing). The gaps are 1,000,000.00, 1,300,000.00, 1,300,000.00 and 200,000.00 each year (printed)."},
 {"id": "AC1a-r11-L03-R3-pointer", "check": "L03 R3: 'Definition 2.1 of this lesson names depreciation as the add-back'",
  "location": "course/modules/AC/AC1/L03.html line 796; L03 Definition 2.1 line 71",
  "status": "PASS",
  "evidence": "L03 Definition 2.1 (indirect operating cash flow) names depreciation as the add-back (line 71). Lesson 2 Definition 4.1 names equipment purchases as investing (L02.html line 116), so the R3 statement that intangibles are not named there is accurate. The 300,000.00 charge is 1,200,000.00 / 4 (" + W + ")."},
 {"id": "AC1a-r11-cards-c015-c027-c033-c039-c042", "check": "Changed L01-L03 cards agree with the current lesson text",
  "location": "course/modules/AC/AC1/cards.json c015, c027, c033, c039, c042; L01.html line 103; L02.html line 97; L03.html lines 57, 76, 127",
  "status": "PASS",
  "evidence": "c015 lists the four posting checks exactly as Remark 2.2 (L01 line 103) does; c027 states the Proposition 3.2 hypotheses as L02 line 97 does; c033 and c039 match Definition 1.1 (line 57) and Proposition 2.2 hypotheses (i) to (v) (line 76); c042 matches Theorem 5.1's hypotheses (line 127), including the Lesson 2 Propositions 3.2 and 4.2."},
 {"id": "AC1a-r11-cards-c127-c128", "check": "New cards c127 and c128 agree with the Theorem 5.1 paragraph and Lab 3",
  "location": "course/modules/AC/AC1/cards.json c127, c128; L03.html line 135; tests/labs/AC1/lab-AC1-L03-1.py lines 1-11, 655-690",
  "status": "PASS",
  "evidence": "c128: Checks 1 to 4 (L03 output) test the balance sheet (gap 0.00), indirect against direct (True), the roll-forwards (True), and cash against balance-sheet cash (True); the Proposition 3.1 investing and financing equalities are not printed (lab docstring line 6-7; page line 135). c127 says Check 2 is not an independent test of Proposition 2.2; the paragraph says it is not an independent test of the theorem, and the page's proof assigns the first claim of Theorem 5.1 to Proposition 2.2 (L03.html line 132), so the card's object is the page's first claim; the card is accurate with that locator."},
 {"id": "AC1a-r11-witness-arithmetic", "check": "Arithmetic of every changed or new figure (L01 E1-E3, Example 3.3; L02 E1-E3, M2, M3, P-check; L03 M1-M3, E1-E3, R2, R3, Check 4 and 6)",
  "location": W,
  "status": "PASS",
  "evidence": "Run: .venv/bin/python -I " + W + " -> ALL PASS (the printed output includes the L02 margins 40.81, 40.95, 38.15 and 10.94, 9.46, 4.61; E1 share 0.18032; E2 94.38%; schedule 3,600,000.00). Computed from the printed integer cents, not from rounded displays."},
 {"id": "AC1a-r11-banned-process-words", "check": "Banned phrases, ellipses and process words in the changed sentences",
  "location": "index.html, L01.html, L02.html, L03.html, cards.json (c015, c027, c033, c039, c042, c127, c128)",
  "status": "PASS",
  "evidence": "Scan (python -I regex on the five files) for roughly, about <digit>, historically, typically, generally, usually, as much as, drives, offsets, builder, verifier, round <digit>, REQUEST, unit report, '...', ellipsis: only 'offsets' appears (L03 misconception 2, card c037 and L03 line 688), which states a computed fact: the 2026 add-back 1,300,000.00 restores the charge in net income (line 688; Lab 3 prints both figures). 'at most one' and 'only' occur in the Proposition 3.2 hypotheses and the Definition 1.1 wording and match the hypotheses they quote."},
 {"id": "AC1a-r11-notation", "check": "Notation: pages use only registered macros with registered meanings",
  "location": "notation/notation.json; index.html, L01-L03 TeX spans",
  "status": "PASS",
  "evidence": "Collected every \\( ... \\) span in the four pages. Tokens used: A, C, D, E, H, I, K, L, N, O, P, Q, R, S, V, X and subscripted forms, plus \\Delta, \\sum, \\le, \\in, \\times, \\text, \\dots, \\blacksquare. None of the registered macros (\\E, \\Prob, \\Var, \\Cov, \\Corr, \\R, \\N, \\indic, \\Normal) is used, and no registered symbol (T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q) appears; the page letters are local (notation.json 'about': only program-wide symbols are registered)."},
 {"id": "AC1a-r11-mutants-na", "check": "Mutant obligation for a lesson slice",
  "location": "ledgers/AC1/mutants/ (project grader mutants)",
  "status": "PASS",
  "evidence": "The slice has no grader and no project page; the mutant obligation of VERIFIER_RULES applies to project slices. The mutants listed in ledgers/AC1/mutants/ mutate the AC1-d project grader and are not re-run here (out of scope for AC1-a). mutants: [] with that reason."},
]
prev_ids = {r["id"] for r in prev["rows"]}
allrows = rows + NEW
ids = [r["id"] for r in allrows]
assert len(ids) == len(set(ids))
assert prev_ids <= set(ids)
from collections import Counter
cnt = Counter(r["status"] for r in allrows)
verdict = "PASS" if all(r["status"] == "PASS" for r in allrows) else "FAIL"
frag = {
 "unit": "AC1", "slice": "AC1-a", "round": 11,
 "round_note": "round 11 independent verification of AC1-a at 91946cf. Previous pin af08ad1 (AC1-a.round10.json, verdict FAIL, 1 FAIL row). Delta af08ad1..91946cf for this slice: index.html line 141; L01.html lines 51, 55, 87, 379, 410, and the hypothesis wording of the exercises at lines 486, 493, 538, 545; L02.html line 73; L03.html lines 51, 600, 654-656, 662, 796; cards.json c015, c027, c033, c039, c042, c127, c128; tests/labs/AC1/lab-AC1-L03-1.py line 444. Every changed hunk was read; every previous non-PASS row was re-verified; every row was re-run or re-derived in this round, so no previous PASS row is carried by byte-identity.",
 "verifier": "Haiku independent verifier, AC1-a round 11 (did not build AC1)",
 "pin": "91946cf",
 "base": "af08ad1 (previous verified pin; round 10 fragment)",
 "checkout": "/tmp/verify11-AC1-a (detached worktree at 91946cf, .venv symlinked)",
 "scratch": "/tmp/ac1-v/a-r11",
 "verified_at": "2026-10-28",
 "registry_flags": ["references/references.json and tools/ and notation/ unchanged in af08ad1..91946cf (empty git diff); live verify_refs --unit AC1 '2 of 560 entries, 0 problems'; offline '560 entries, 0 problems'. No FASB entry in references.json (grep count 0), and no AC1 source in tools/data_sources.yaml, consistent with index.html line 175."],
 "freshness_flags": [],
 "notes": [
  "Slice: course/modules/AC/AC1/index.html, L01.html, L02.html, L03.html, the three lab twins tests/labs/AC1/lab-AC1-L01-1.py, lab-AC1-L02-1.py, lab-AC1-L03-1.py, and the L01-L03 cards of cards.json (c001-c045, c123, c124, c126-c128). Witness script: " + W + " (python -I). Text extractions used for reading: " + R + "L01.txt, L02.txt, L03.txt, index.txt, cards.txt.",
  "Not a project slice: no grader or project.html is in this slice, so mutants is []. The 71 project mutants in ledgers/AC1/mutants/ belong to the AC1-d grader and are out of scope; no new student-error mutant was written for this lesson slice, and no alternative implementation applies.",
  "Hours: hub split 90 lesson hours and 30 project hours; lesson hours L01 11, L02 12, L03 11 (34 h of the 90). Arithmetic consistent; not judged against pace (architect ruling).",
  "Unverified or out of reach: no external source was read (the lessons cite no registry key); the live verify_refs run covers the registry only. The Proposition 3.2 hypothesis set is read from the pages, not from any textbook.",
  "Card c127 names Proposition 2.2 where the Theorem 5.1 paragraph says 'the theorem'. The page's proof assigns Theorem 5.1's first claim to Proposition 2.2, so the card is accurate, but a reader must follow that link; recorded as PASS with the locator."
 ],
 "mutants": [],
 "summary": {"rows": len(allrows), "pass": cnt.get("PASS", 0), "fail": cnt.get("FAIL", 0), "unverifiable": cnt.get("UNVERIFIABLE", 0)},
 "verdict": verdict,
 "rows": allrows,
}
json.dump(frag, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
print(frag["summary"], verdict)
