"""Builds ledgers/M1/M1-b.json for round 24 from the round-23 fragment (context) and fresh round-24 rows."""
import json, datetime

PREV = json.load(open("/tmp/fanout-frags/M1-b.round23.json"))
PREFIX = ("Carried from round 23 (course/modules/M/M1/L04.html and L05.html cited lines, cards.json and "
          "tests/labs/M1 byte-identical between pins 503d139 and 23cbd6a; the delta changes only L04.html "
          "lines 79, 378, 380 and L05.html lines 243, 266, 385-396): ")
FRESH_CHANGED = {"M1-b-2.2-L05-numbers-recomputed", "M1-b-2.3-grades", "M1-b-2.4-math-L04", "M1-b-2.5-lab-L05",
                 "M1-b-2.9-structure-prose", "M1-b-2.9-DAG", "M1-b-r4-term-before-def-L04",
                 "M1-b-r5-keyresults-basis-L04", "M1-b-r5-keyresults-basis-L05", "M1-b-r6-checked-in-lab-L05",
                 "M1-b-r7-L04-378-380-460-basis-text", "M1-b-r20-E-scope-remarks", "M1-b-r21-E-list-complete",
                 "M1-b-r22-E-lab1-dropped", "M1-b-r22-delta", "M1-b-r23-E-list-R3", "M1-b-r21-mutants",
                 "M1-b-2.7-cards", "M1-b-r18-cards-scan", "M1-b-r19-cards-scan"}
CMD = {"M1-b-cmd-pin", "M1-b-cmd-run_labs", "M1-b-cmd-twins", "M1-b-cmd-page_smoke", "M1-b-cmd-check_pages_dag",
       "M1-b-cmd-lint-types", "M1-b-cmd-refs", "M1-b-cmd-pytest"}

FRESH = {
 "M1-b-cmd-pin": ("PASS", "course/modules/M/M1/L04.html; L05.html; tests/labs/M1/; cards.json",
   "git rev-parse HEAD = 23cbd6ac0f337571c7de710bc584e55a0bcca39c (checkout pin 23cbd6a, detached). git status --short shows only the .venv symlink (untracked, not a source change)."),
 "M1-b-cmd-run_labs": ("PASS", "tools/run_labs.py --unit M1; course/modules/M/M1/L04.html; L05.html",
   "Re-run: .venv/bin/python tools/run_labs.py --unit M1 exit 0, last line 'run_labs M1: PASS (11/11)' (out/run_labs.txt)."),
 "M1-b-cmd-twins": ("PASS", "tests/labs/M1/lab-M1-L04-1.py; lab-M1-L05-1.py; course/modules/M/M1/L04.html and L05.html <pre class=expected>",
   "Each twin run as python -I -W error from the checkout: exit 0, stderr 0 bytes (out/twin_L04.err, twin_L05.err). Stdout compared to the embedded expected block by a script: L04 27 lines equal, L05 13 lines equal (True, True). Output in out/twin_L04.out, twin_L05.out."),
 "M1-b-cmd-page_smoke": ("PASS", "tools/page_smoke.py --unit M1 --pages L04 L05",
   "Exit 0: 'page_smoke modules/M/M1/L05.html: PASS' and 'page_smoke M1: PASS' (out/page_smoke.txt); lab timings 0.0 s."),
 "M1-b-cmd-check_pages_dag": ("PASS", "tools/check_pages.py --unit M1; tools/check_dag.py --unit M1; tools/check_projects.py --unit M1",
   "'check_pages M1: PASS', 'check_dag M1: PASS', 'check_projects M1: PASS', each exit 0 (out/check_pages.txt, check_dag.txt, check_projects.txt)."),
 "M1-b-cmd-lint-types": ("PASS", "tests/labs/M1/ (ruff); lab-M1-L04-1.py, lab-M1-L05-1.py (mypy)",
   "ruff check tests/labs/M1 exit 0; ruff format --check tests/labs/M1 exit 0 (out/ruff.txt); mypy --no-incremental on both twins exit 0 (out/mypy.txt)."),
 "M1-b-cmd-refs": ("PASS", "references/references.json; tools/verify_refs.py; L04.html:459-462; L05.html:472-475",
   "verify_refs.py --offline exit 0: 'offline integrity: 560 entries, 0 problems'. verify_refs.py --unit M1 exit 0: 'live re-verification of M1: 1 of 560 entries, 0 problems' (out/refs_offline.txt, refs_live_m1.txt). The M1 references paragraphs cite no new key (diff unchanged there)."),
 "M1-b-cmd-pytest": ("PASS", "tests/test_run_labs.py; tests/test_page_checks.py; tests/test_labs.py",
   "pytest -q on the three files: exit 0, all dots, no F or E (out/pytest.txt)."),
 "M1-b-2.2-L05-numbers-recomputed": ("PASS", "course/modules/M/M1/L05.html:243 (Example 3.1), 266 (misconception 1), 223-235 (Lab 1 printed output), 390-393 (key results)",
   "Changed line 243 ('Lab 1 prints all three whole-cent values') re-derived in ledgers/M1/scripts/M1-b-r24/recompute_r24.py (out/recompute.txt): 1,000,000 x 1.05^-5 = 783526.1665 -> 783,526 cents; 1,000,000 x (1.025)^-10 = 781198.4017 -> 781,198; 1,000,000 x e^-0.25 = 778800.7831 -> 778,801. Factor digits 0.7835261665, 0.7811984017, 0.7788007831 match the printed lab output (twin_L05.out). Spread 783,526 - 778,801 = 4,725 cents. Changed misconception numbers 0.9759000729 (t=0.5) and 0.6139132535 (t=10) match the printed annual column; recomputed factors 0.97590007295 and 0.61391325354."),
 "M1-b-2.3-grades": ("PASS", "course/modules/M/M1/L04.html: Props 2.1, 2.2, 3.1 (83, 101, 224), key-results rows (377-384); L05.html: Props 1.4, 2.1, 2.2, 2.4 (87, 106, 116, 131), key results (388-395)",
   "Changed key-results rows re-read in full. L04 rows 378 and 380 are T with Proposition 2.2 under Assumption E (its proof at 107 uses E, so the scope is backed) and R3 under E for r_m > r only (R3 derives r_m = m(e^{r/m}-1) from A1, A2 and the monotone power, then uses E at 367 for e^x - 1 > x). L05 rows 390, 392, 393: Prop 1.4 (87, 'Assume E', line 88), Prop 2.2 (116, 'Assume E'), Prop 2.4 (131, 'Assume E'); each row's 'Under Assumption E' prefix matches the statement. All grades T with a derivation on the page; no grade changed in the delta."),
 "M1-b-2.4-math-L04": ("PASS", "course/modules/M/M1/L04.html: Prop 2.1 block (83-90), Prop 2.2 (101-109), R2 (358), R3 (361-367), key results (378-380), references (460)",
   "Changed rows 378 and 380 re-derived. Prop 2.2 proof (107): 0 < 1 + r/m < e^{r/m} from E, raised to the m-th power, and (e^{r/m})^m = e^r from A2. R3: (1 + r_m/m)^m = e^r with 1 + r_m/m > 0 has the unique positive root e^{r/m}; the claim r_m > r follows from e^x - 1 > x (E) with x = r/m. Numeric check: r_12 = 12(e^{0.05/12} - 1) = 0.05010431149 (out/recompute.txt), matching the printed 0.0501043115. For even m, -e^{r/m} also satisfies the power equation, so the hypothesis 1 + r_m/m > 0 is needed as the page says."),
 "M1-b-2.5-lab-L05": ("PASS", "course/modules/M/M1/L05.html: Lab 1 hypothesis (142), Remark 2.3 (127), interpretation (236), misconceptions 1-3 (266-274); tests/labs/M1/lab-M1-L05-1.py",
   "Changed misconception 1 (266): 'Its check that the annual factor decreases in t (annual_decreasing_in_t True) means that the five printed annual factors fall from one row to the next, so each lies between the first and the last.' Twin lines 53-63 (the same code as the embedded copy at L05.html:195-206): decreasing = annual < previous, with previous starting at 1 and updated each row, so the check is a row-to-row strict decrease starting from 1 (twin line 62); output 'annual_decreasing_in_t True' (twin_L05.out). The second sentence: 'The check annual_between_zero_and_one True shows that both are below one.' The check is Decimal(0) < annual < Decimal(1) over all five rows (twin line 63), so it shows every printed factor is between zero and one; the page says only 'both are below one' for the first and last rows, a narrower statement that is true. No lab claim overreaches."),
 "M1-b-2.9-structure-prose": ("PASS", "course/modules/M/M1/L04.html and L05.html (changed lines re-read in full; full-page grep)",
   "Full-page case-insensitive grep (out/scan_words.txt): roughly half, about 6%, historically, ellipsis, builder, verifier, REQUESTS, unit report, typically, usually: 0 hits in both pages. 'round' hits are code (ROUND_HALF_EVEN, lines 133/154 and 161/187) and 'unrounded' (L04 218, 340; L05 254, 270, 339, 346); no process word."),
 "M1-b-2.9-DAG": ("PASS", "tools/check_dag.py --unit M1 (re-run); L04.html:79 (changed line)",
   "check_dag M1: PASS (exit 0, out/check_dag.txt). sed -n 79p L04.html | grep -c data-concept = 0; check_dag passes for M1 with the changed line; no concept attribute is added or removed by the delta."),
 "M1-b-r4-term-before-def-L04": ("PASS", "course/modules/M/M1/L04.html:75 (first mention), 78-80 (Assumption E block), 52, 54-56, 59, 101 (Prop 2.2 statement)",
   "Assumption E is first named at line 75 ('stated as Assumption E in the next block'), a signpost to the block at 78-80. The changed line 79 lists places that use Proposition 2.2, which is first named at 75 and stated at 101; its list also names 'Remark 2.3' (first labelled at 112) and 'Problem R2' (358) before they appear. These are forward cross-references to labelled items, not undefined terms, and the page introduces each before use in its own section; no term is used before definition in the sense of a concept. Recorded as PASS on that reading (the earlier rounds took the same reading)."),
 "M1-b-r5-keyresults-basis-L04": ("PASS", "course/modules/M/M1/L04.html:372-384 (key results), 459-462 (references paragraph)",
   "Changed rows 378 and 380 read in full. Source column of 380: 'Derived in R3 from A1 and A2 of L03, Assumption E, and the strict monotonicity ... stated in the proof of Proposition 2.2'. The proof of Prop 2.2 (line 107) states 0 < a < b gives a^m < b^m, and R3 (365) relies on Assumption E at 367. Both bases are named; the 'under Assumption E' qualifier now scopes r_m > r only, which is the only step using E in R3."),
 "M1-b-r5-keyresults-basis-L05": ("PASS", "course/modules/M/M1/L05.html:385-396 (key results), 472-475 (references)",
   "Changed rows 390, 392, 393 read in full. The sources name Assumption E, A1, A2 of L03, L03 Propositions 1.3, 1.4 and 1.6(a) (confirmed present in course/modules/M/M1/L03.html at lines 82, 92, 112 and 118), Proposition 2.1 and the Lab 1 check. Each row's 'Under Assumption E' prefix matches its statement (Prop 1.4 at 87-88 'Assume E'; Prop 2.2 at 116 'Assume E'; Prop 2.4 at 131 'Assume E')."),
 "M1-b-r6-checked-in-lab-L05": ("PASS", "course/modules/M/M1/L05.html:388-396 (key results); tests/labs/M1/lab-M1-L05-1.py",
   "Row for Prop 2.1 ('checked in Lab 1') is unchanged; the lab prints equivalent_continuous equal to annual in every row and max_gap_equivalent_vs_annual 0.0000000000 (twin_L05.out). Changed rows 390-393 cite 'illustrated by the printed columns of Lab 1' for Props 2.2 and 2.4: the lab prints continuous_at_5pct (below annual, row by row) and semiannual (below annual) columns, so the illustration is accurate."),
 "M1-b-r7-L04-378-380-460-basis-text": ("PASS", "course/modules/M/M1/L04.html:378, 380 (rows for Prop 2.2 and R3), 460 (references paragraph)",
   "Row 378: 'Under Assumption E, for r > 0 and every m >= 1, F_m(r) < e^r (Proposition 2.2)' with source 'Proved in §2 from Assumption E, A2 of L03, and the power fact stated in its proof'. Row 380: 'under Assumption E, r_m > r (Problem R3)' with source 'Derived in R3 from A1 and A2 of L03, Assumption E, and the strict monotonicity ... stated in the proof of Proposition 2.2'. Line 460 (references paragraph) states the results in §2 are derived from E and A2 and the power fact; it does not claim that R3 uses no E. Basis text matches the solutions at 358 and 365-367."),
 "M1-b-2.7-cards": ("PASS", "course/modules/M/M1/cards.json (full scan, out/cards_scan.txt); M1-c075, M1-c163 re-read",
   "Full scan of cards.json (out/cards_scan.txt): 180 entries, no duplicate id, no duplicate front. cards.json is unchanged in the delta 503d139..23cbd6a (git diff --stat empty). M1-c075 back: 'No. Under Assumption E, every F_m(r) is below e^r (Proposition 2.2)...' and M1-c163 back: 'Yes, r_m > r under Assumption E (Problem R3)...' both match L04.html lines 101-102, 365-367 and 380."),
 "M1-b-r18-cards-scan": ("PASS", "course/modules/M/M1/cards.json", "Superseded by the full scan this round (out/cards_scan.txt): 180 entries, no duplicate id, no duplicate front."),
 "M1-b-r19-cards-scan": ("PASS", "course/modules/M/M1/cards.json", "Superseded by the full scan this round (out/cards_scan.txt): 180 entries, no duplicate id, no duplicate front."),
 "M1-b-r20-E-scope-remarks": ("PASS", "course/modules/M/M1/L04.html:79 (list, Remark 2.3 entry), 112 (Remark 2.3); L05.html:127",
   "Changed line 79 still lists Remark 2.3; line 112 'Under Assumption E, Proposition 2.2 says that they stay below e^r' names Proposition 2.2 and E. Consistent. L05.html:127 unchanged in the delta."),
 "M1-b-r21-E-list-complete": ("FAIL", "course/modules/M/M1/L04.html:79 (list); 365 (R3 solution); 380 (key results)",
   "Round-21 row. The list at line 79 is no longer complete: the R3 solution at line 365 names Proposition 2.2 ('as in the proof of Proposition 2.2') and is absent from the list after the round-23 edit removed 'the solution to Problem R3'. See M1-b-r24-E-list-R3-named."),
 "M1-b-r22-E-lab1-dropped": ("PASS", "course/modules/M/M1/L04.html:79 (list); line 117 (Lab 1 hypothesis)",
   "'the Lab 1 hypothesis' is still in the list at line 79, and line 117 names Propositions 2.1 and 2.2. This row is only about the Lab 1 entry, and it is PASS. The list-completeness defect is recorded in M1-b-r24-E-list-R3-named."),
 "M1-b-r22-delta": ("PASS", "course/modules/M/M1/L04.html:79, 375-380; L05.html:243, 266, 385-396; cards.json; tests/labs/M1; tools; references",
   "git diff --stat 503d139 23cbd6a -- course/modules/M/M1 tests/labs/M1 tools references cards.json: L04.html 6 lines (79, 378, 380), L05.html 10 lines (243, 266, 390, 392, 393 with the 'Under Assumption E' prefix) plus three ledgers/M1/mutants/r23v_*.py files (project-grader mutants, out of slice b). No change to tests/labs/M1, tools, references, cards.json or the hours markup."),
 "M1-b-r21-mutants": ("PASS", "ledgers/M1/mutants/ (project slices a and c)",
   "Slice b is a lesson slice and has no project mutants (architect ruling, unchanged). The delta adds ledgers/M1/mutants/r23v_01_growing_perpetuity_adds_growth.py, r23v_02_annuity_one_period_short.py and r23v_03_last_payment_clipped_not_paid.py; their headers name the M1 project (annuity_engine.py), so they belong to slices a and c and are not run here."),
 "M1-b-r23-E-list-R3": ("FAIL", "course/modules/M/M1/L04.html:79 (list) ; 365 (R3 solution)",
   "The round-23 premise was wrong: the R3 solution does name Proposition 2.2 (line 365, 'as in the proof of Proposition 2.2'), and the round-23 grep omitted line 365. The round-23 remedy removed the R3 entry, which leaves the list incomplete. Corrected in M1-b-r24-E-list-R3-named."),
}

NEW = [
 {"id": "M1-b-r24-E-list-R3-named", "check": "Line 79 list of places that name Proposition 2.2 is complete",
  "location": "course/modules/M/M1/L04.html:79 (list); 365 (R3 solution names Prop 2.2)", "status": "FAIL",
  "evidence": "grep -n 'Proposition 2.2' L04.html (out in this round's transcript, reproduced: lines 75, 79 (E sentence), 101, 107, 112, 117, 261, 358, 365, 378, 380, 425, 460). Line 365 is the R3 solution: 'as in the proof of Proposition 2.2'. Line 79 says E 'is used in Proposition 2.2 and in each other place on this page that names Proposition 2.2: the section 2 introduction, Remark 2.3, the Lab 1 hypothesis, the misconception in §5, Problem R2, the key-results table in §7, quiz item 5 and the references paragraph in §9'. The R3 solution is not in that list, so the 'each other place' claim is false by one place. The closing sentence 'It is used directly in Problem R3' states the use of E in R3 separately, but it does not repair the completeness claim. Fix: restore 'the solution to Problem R3' in the colon list at line 79 (between 'Problem R2,' and 'the key-results table in §7'); the closing sentence may stay."},
 {"id": "M1-b-r24-L04-R3-E-scope", "check": "R3 solution uses E only where the text says so",
  "location": "course/modules/M/M1/L04.html:361-367; 380", "status": "PASS",
  "evidence": "R3 derivation of r_m = m(e^{r/m}-1) uses A1, A2 and monotone power only (365); E is used at 367 for e^{r/m}-1 > r/m. Row 380 puts 'under Assumption E' on r_m > r only. Matches the solution."},
 {"id": "M1-b-r24-L05-243-whole-cents", "check": "Example 3.1 whole-cent claim matches the lab output",
  "location": "course/modules/M/M1/L05.html:243; tests/labs/M1/lab-M1-L05-1.py:43-45, 75-77; L05.html:223-235", "status": "PASS",
  "evidence": "Lab prints 'annual cents 783526', 'semiannual cents 781198', 'continuous cents 778801' (twin_L05.out, to_cents with ROUND_HALF_EVEN). Recomputed independently: 783526.1665, 781198.4017, 778800.7831 (out/recompute.txt). Page text 'Lab 1 prints all three whole-cent values' is accurate."},
 {"id": "M1-b-r24-L05-266-monotone-check", "check": "Misconception 1 description of the two lab checks matches lab code and output",
  "location": "course/modules/M/M1/L05.html:266; tests/labs/M1/lab-M1-L05-1.py:53-54, 62-63, 70-71", "status": "PASS",
  "evidence": "Code: decreasing = annual < previous, previous starts at 1; inside = 0 < annual < 1 over all five rows; output 'annual_decreasing_in_t True' and 'annual_between_zero_and_one True'. The page's sentence 'so each lies between the first and the last' follows from the row-to-row decrease; 'both are below one' is narrower than the check (which covers all rows and also the lower bound 0) and is true. Printed first 0.9759000729 and last 0.6139132535 match twin_L05.out."},
 {"id": "M1-b-r24-L05-key-results-E-scope", "check": "Each 'Under Assumption E' prefix added to L05 key-results rows matches the statement's own assumption",
  "location": "course/modules/M/M1/L05.html:87-88 (Prop 1.4 'Assume E'), 116 (Prop 2.2), 131 (Prop 2.4), 390, 392, 393", "status": "PASS",
  "evidence": "Statements at lines 87-88, 116 and 131 begin 'Assume E' (read in full at this round). Key-results rows 390, 392, 393 carry 'Under Assumption E' matching those statements. Prop 2.1 (row 391, no E) is stated without E at line 106 and is unchanged."},
 {"id": "M1-b-r24-embed-twins", "check": "Embedded expected blocks equal the twins' real output", "location": "course/modules/M/M1/L04.html expected block (191-217); L05.html (223-235)", "status": "PASS",
  "evidence": "Script compare of <pre class=expected> against the stdout of each twin run with python -I -W error: L04 27 lines equal, L05 13 lines equal (True). Re-run in this round."},
]

carried = []
for r in PREV["rows"]:
    rid = r["id"]
    if rid in FRESH:
        st, loc, ev = FRESH[rid]
        carried.append({"id": rid, "check": r["check"], "location": loc, "status": st, "evidence": ev})
        continue
    if rid in FRESH_CHANGED:
        raise SystemExit("row needs fresh evidence: " + rid)
    if r["status"] != "PASS":
        raise SystemExit("unexpected non-PASS carry: " + rid)
    carried.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                    "evidence": PREFIX + r["evidence"]})

FIX = "Restore 'the solution to Problem R3,' in the colon list at course/modules/M/M1/L04.html:79 (between 'Problem R2,' and 'the key-results table in §7'); the closing sentence may stay."
for r in carried + NEW:
    if r["status"] != "PASS":
        r["fix"] = FIX
rows = carried + NEW
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
for r in PREV["rows"]:
    assert r["id"] in ids, "dropped id " + r["id"]
frag = {
 "unit": "M1", "slice": "M1-b", "round": 24,
 "verifier": "independent verifier (Haiku), round 24",
 "pin": "23cbd6ac0f337571c7de710bc584e55a0bcca39c",
 "base": "none",
 "previous_fragment": "/tmp/fanout-frags/M1-b.round23.json",
 "checkout": "/tmp/verify24-M1-b",
 "scratch": "/tmp/M1-v/M1-b-r24",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Slice b is lessons L04 and L05 with their lab twins, not a project slice: no student-error mutants or alternative implementations apply (architect ruling, as in rounds 16-23). ledgers/M1/mutants/ is slice a and c material; the delta adds three r23v_* project mutants that are not run here.",
  "Delta 503d139..23cbd6a for slice b (git diff --stat, M1 scope): L04.html lines 79, 378, 380; L05.html lines 243, 266, 390, 392, 393. cards.json, tests/labs/M1, tools/, references/ and the hours markup are unchanged.",
  "Round-23 row M1-b-r23-E-list-R3 rested on a grep that omitted L04.html line 365. The R3 solution does name Proposition 2.2, so its remedy (deleting the R3 entry from the list at line 79) made the list incomplete. This round's FAIL row M1-b-r24-E-list-R3-named carries the corrected fix.",
  "Rows carried from round 23 cite only lines byte-identical between the pins (checked by a line-range scan of their locations against the delta); every row citing a changed line was re-verified fresh.",
  "Not checked: the cited Lab 1 printed values were compared to the twin run, not to a second independent implementation; the references (Beneish, SEC) are not cited on these pages and no external source was fetched in this round."
 ],
 "summary": {}
}
n = len(rows)
fails = sum(1 for r in rows if r["status"] == "FAIL")
frag["summary"] = {"rows": n, "pass": n - fails, "fail": fails, "unverifiable": 0}
json.dump(frag, open("ledgers/M1/M1-b.json", "w"), indent=1, ensure_ascii=False)
print("rows", n, "fail", fails)
