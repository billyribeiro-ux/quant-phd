import json
P = "9fd6aed"
rows = []
def add(i, check, loc, status, ev):
    rows.append({"id": i, "check": check, "location": loc, "status": status, "evidence": ev})
add("FC1-b-r7-gate-check-pages", "tools/check_pages.py --unit FC1 --page L04 / L05", "course/modules/FC/FC1/L04.html, L05.html", "PASS",
    "Re-run at 0d2d0f3: 'check_pages FC1 L04: PASS', 'check_pages FC1 L05: PASS', rc=0 (ledgers/FC1/scripts/FC1-b-r7/check_pages_L04.out, check_pages_L05.out).")
add("FC1-b-r7-gate-check-dag", "tools/check_dag.py --all", "L04.html, L05.html and the unit", "PASS",
    "Re-run: 'check_dag FC1: PASS', rc=0 (ledgers/FC1/scripts/FC1-b-r7/check_dag.out).")
add("FC1-b-r7-gate-run-labs", "tools/run_labs.py --unit FC1 --page L04 and --page L05", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    "Re-run: 'run_labs FC1: PASS (1/1)' for each page, rc=0 (run_labs_L04.out, run_labs_L05.out); unit run 'run_labs FC1: PASS (8/8)' (run_labs.out).")
add("FC1-b-r7-gate-page-smoke", "tools/page_smoke.py --unit FC1", "L04.html, L05.html", "PASS",
    "Re-run: 'page_smoke modules/FC/FC1/L04.html: PASS', 'page_smoke modules/FC/FC1/L05.html: PASS', 'page_smoke FC1: PASS', rc=0 (page_smoke.out). The tool has no single-page form that reports per page; --pages was run too (page_smoke_L04_L05.out, 'page_smoke FC1: PASS').")
add("FC1-b-r7-gate-ruff-mypy-pytest", "ruff check, ruff format --check, mypy --no-incremental, pytest -k FC1", "tests/labs/FC1; course/modules/FC/FC1", "PASS",
    "ruff: 'All checks passed!', '8 files already formatted', rc=0 (ruff.out); mypy: 'Success: no issues found in 229 source files', rc=0 (mypy.out); pytest -k FC1: '.........  100%', rc=0 (pytest_fc1.out).")
add("FC1-b-r7-gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    "'offline integrity: 560 entries, 0 problems', rc=0 (verify_refs.out). No live run.")
add("FC1-b-r7-twin-page-equality", "page data-run code vs tests/labs/FC1 twin", "L04.html pre code[data-run]; L05.html pre code[data-run]", "PASS",
    "twins_r7.py: 'L04 page_code==twin: True', 'L05 page_code==twin: True' (twins_r7.out).")
add("FC1-b-r7-twin-isolated-run", "python -I -W error on each twin", "tests/labs/FC1/lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    "twins_r7.out: 'L04 twin rc 0 stderr bytes 0', 'L05 twin rc 0 stderr bytes 0'.")
add("FC1-b-r7-expected-equals-output", "pre.expected vs twin stdout", "L04.html line 331 (pre.expected); L05.html line 366", "PASS",
    "twins_r7.out: 'L04 expected==stdout: True', 'L05 expected==stdout: True' (whitespace-stripped equality).")
add("FC1-b-r7-M3-separate-arrivals", "Round-6 FAIL re-verified: M3 prompt and solution vs Remark 1.2", "course/modules/FC/FC1/L04.html lines 407-409 (M3); Remark 1.2 lines 66-67", "PASS",
    "Line 407 prompt now has two arriving buy orders; line 408 says the second arrives 'after the first has finished matching'; line 409 solution checks activation after each order finished matching (last fill 1001 then 1000). Remark 1.2 (line 67) states stops are checked only after the arriving order has finished matching, not after each fill. Hand check: last fill 1001 > 1000 no activation; last fill 1000 = stop, activates. Matches. The round-6 FAIL is fixed.")
add("FC1-b-r7-M3-stale-stop-rule", "M3 solution wording vs Definition 1.1 and Remark 1.2", "course/modules/FC/FC1/L04.html line 409; lines 61, 66-67", "PASS",
    "Line 409 uses 'at or below its stop' for a sell stop, matching line 61 (Definition 1.1 sell stop: at or below) and Remark 1.2 (line 67).")
add("FC1-b-r7-M3-examples-problems", "Re-verify of M3 prompt and solution after the edit, plus the carried examples", "L04.html lines 391-487", "PASS",
    "Only lines 407-409 changed in this range since 9fd6aed (git diff hunks: 407-409). The rest is byte-identical since the previous pin; carried from round 6 (FC1-b-r6-L04-M3-examples-problems) for those lines. The edited M3 re-derived above.")
add("FC1-b-r7-market-order-definition", "Definition 1.1 market-order sentence (new text) vs Definition 2.1 and the lab", "course/modules/FC/FC1/L04.html line 59", "PASS",
    "Line 59 now: 'A market order never rests in the limit order book (Definition 2.1).' Definition 2.1 (line 84) defines the book as the set of resting limit orders, so a market order, which never rests, is consistent. Lab market orders are not appended to the book: lab-FC1-L04-1.py line 90 appends only when kind == 'limit' with qty > 0. Within-lesson forward pointer to Definition 2.1; the term 'limit order book' is already named on line 51 and defined on line 84. Concept not linked from another lesson, so no DAG effect.")
add("FC1-b-r7-cards-L04-L05-unchanged", "cards.json entries with lesson L04/L05 vs 9fd6aed", "course/modules/FC/FC1/cards.json", "PASS",
    "Compared the 111 entries per id: 9 changed ids (c010, c014, c017, c029, c091, c092, c093, c095, c096), all lesson L01 or L02; 40 L04/L05 entries byte-identical.")
add("FC1-b-r7-process-words", "grep -i -w for process words", "L04.html, L05.html, lab-FC1-L04-1.py, lab-FC1-L05-1.py", "PASS",
    "Re-run (process_words.out, 6 hits): lab docstring and page text 'checked once the arriving order has finished matching' and 'checked for an uncrossed book' describe the lab's own checks; no learner-facing process words. Unchanged hunks.")
carried = [
 ("FC1-b-r5-L04-stop-trigger-fix", "L04.html lines 61, 67, 93-111; lab-FC1-L04-1.py activate()"),
 ("FC1-b-r5-L04-numbers-independent", "L04.html lines 331-352; lab-FC1-L04-1.py main()"),
 ("FC1-b-r5-L04-trace-claims", "L04.html lines 339-346, 353, 452"),
 ("FC1-b-r5-L04-proofs-2.2-2.3", "L04.html lines 93-111"),
 ("FC1-b-r5-L04-notation", "L04.html lines 104, 432"),
 ("FC1-b-r5-L04-key-results-quiz", "L04.html lines 496-498, 519-527, 546-578"),
 ("FC1-b-r6-L04-why-it-matters", "L04.html line 48"),
 ("FC1-b-r6-L04-notation", "L04.html lines 48, 61, 104, 432; L05.html lines 66, 100, 390, 468, 488"),
 ("FC1-b-r5-L05-numbers-independent", "L05.html lines 109, 366-389, 488, 495, 544, 575-636"),
 ("FC1-b-r6-L05-numbers", "L05.html lines 390, 485-488, 493-496; twin output"),
 ("FC1-b-r6-E1-basis-wording", "L05.html line 488"),
 ("FC1-b-r5-L05-E2-net-payers", "L05.html lines 493-496"),
 ("FC1-b-r5-L05-dates", "L05.html lines 378-379, 445, 502, 582"),
 ("FC1-b-r5-L05-E3-lag-variant", "L05.html line 502; lab-FC1-L05-1.py SETTLEMENT_LAG line 29"),
 ("FC1-b-r5-L05-prop-2.1-2.2-proofs", "L05.html lines 77-96, 459-479"),
 ("FC1-b-r5-L05-R2-negative-consideration", "L05.html lines 518-520"),
 ("FC1-b-r5-L05-harris-claim", "L05.html line 403; references/references.json (harris2002trading)"),
 ("FC1-b-r5-L05-no-settlement-source", "L05.html line 397, 543, 625-632"),
 ("FC1-b-r5-L05-parameter-claim", "L05.html line 390"),
 ("FC1-b-r5-L05-offsets-never-decrease", "L05.html line 66"),
 ("FC1-b-r5-L05-remark-2.3-identities", "L05.html lines 100, 398"),
 ("FC1-b-r5-hours", "L04.html line 2; L05.html line 2"),
 ("FC1-b-r5-twin-page-equality-prev", "L04.html, L05.html pre code (prior round)"),
]
for i, loc in carried:
    add(i, "carried", loc, "PASS", "Carried from round 6 (" + loc + " byte-identical since the previous pin 9fd6aed; the 9fd6aed..0d2d0f3 hunks in L04.html are lines 59 and 407-409 only, and L05.html, lab-FC1-L04-1.py and lab-FC1-L05-1.py are unchanged): round-6 evidence stands (see the round-6 fragment, /Users/billyribeiro/.fanout/frags/C-FC1-b.round6.json).")
frag = {
 "unit": "FC1", "slice": "FC1-b", "round": 7,
 "verifier": "Claude Haiku 5.5, independent verifier for FC1-b round 7 (did not build FC1)",
 "pin": "0d2d0f3f8ffb68fc54bb854cb1d7bf28e6483e78",
 "base": "9fd6aed (round-6 pin; round-6 fragment /Users/billyribeiro/.fanout/frags/C-FC1-b.round6.json)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC7-FC1-b",
 "scratch": "ledgers/FC1/scripts/FC1-b-r7/",
 "verified_at": "2026-10-29",
 "verdict": "PASS",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Delta 9fd6aed..0d2d0f3 for the slice: L04.html line 59 (Definition 1.1 market-order sentence) and lines 407-409 (M3 prompt and solution). L05.html, both lab twins and cards for L04/L05 are byte-identical. The delta also touches cards L01/L02, grader/test_project.py and project.html, which are outside this slice.",
  "Round-6 FAIL FC1-b-r6-M3-separate-arrivals is fixed and re-verified (now PASS). Its old wording is gone.",
  "No grader in this slice: no student-error mutants required; none written. Lab twins are demonstrations (ruling).",
  "Twin code equals page code and expected blocks equal stdout under python -I -W error with zero stderr.",
  "Both L04 and L05 page smoke and lab runs were executed. The 'page_smoke alone per page' form does not exist; the unit run was used and reported per page."
 ],
 "summary": "FC1-b round 7: 37 PASS, 0 FAIL. The round-6 M3 FAIL is fixed. All gates pass at 0d2d0f3 (check_pages L04/L05, check_dag, run_labs, page_smoke, ruff, mypy, pytest -k FC1, verify_refs --offline). Twins equal page code and expected blocks. Rows whose cited lines are unchanged are carried from round 6, with the carry prefix."
}
json.dump(frag, open("ledgers/FC1/FC1-b.json", "w"), indent=1, ensure_ascii=False)
print(len(rows), sum(r["status"]=="PASS" for r in rows))
