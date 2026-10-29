import json, sys
from datetime import datetime, timezone

ROOT = "/Users/billyribeiro/.fanout/wt/verifyC10-FC1-c"
C9 = "Carried from round 9 (course/modules/FC/FC1/grader/test_project.py lines cited, project.html lines cited, cards.json objects cited byte-identical since pin 33744e5; the round-10 delta hunks are project.html line 289, test_project.py lines 506-514, cards.json c013, c054, c070, c071, c082, c091, c092, c115-c118):"

def row(i, check, loc, status, ev, fix=None):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
 row("proj-run-graders", "2.6-grader", "course/modules/FC/FC1/grader/ (reference.py, starter.py, test_project.py, instance.py)", "PASS",
     "Re-run this round: `.venv/bin/python tools/run_graders.py --unit FC1 --seeds 0-49` -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.1 s)'. test_project.py changed (lines 506-514), so re-run."),
 row("proj-collect-count-55", "2.6-autograder", "project.html line 171 ('runs 59 checks'); grader/test_project.py", "PASS",
     "Re-run this round from scratch copy (test_project.py, instance.py, reference.py as instruments.py), `pytest --collect-only -q` -> '59 tests collected in 0.02s'. project.html line 171 says 59: equal."),
 row("proj-browser-suite", "2.6-autograder", "project.html line 301; course/assets/js/grader.js", "PASS",
     "Re-run this round: `tools/page_smoke.py --unit FC1 --pages project` -> 'in-browser grader: All 59 tests pass on seed 672730544' and 'page_smoke FC1: PASS'. Repo harness, not a real browser session."),
 row("proj-local-command", "2.6-autograder", "project.html section#local line 307; starter.py docstring", "PASS", C9 + " command text unchanged; project.html line 307 not in delta."),
 row("proj-alternatives-five", "2.6-autograder", "ledgers/FC1/alternatives/a1..a5", "PASS",
     "Re-run this round against the current test_project.py: ledgers/FC1/scripts/FC1-c-r10/alts_r10.out -> failing_seeds=0 for a1..a5 over seeds 0-49."),
 row("proj-instances-50", "2.6-autograder", "course/modules/FC/FC1/grader/instance.py", "PASS",
     C9 + " instance.py byte-identical; run_graders 50/50 PASS this round."),
 row("proj-starter-vs-spec", "2.6-spec", "grader/starter.py; project.html line 161", "PASS", C9 + " neither file in delta."),
 row("proj-spec-questions", "2.6-spec", "project.html section#spec lines 153-172", "PASS", C9 + " lines 153-172 not in delta (delta is line 289)."),
 row("proj-ladder", "2.6-spec", "project.html section#ladder lines 41-50", "PASS", C9 + " lines not in delta."),
 row("proj-stretch-scope", "2.6-spec", "project.html section#stretch lines 311-318", "PASS", C9 + " lines not in delta."),
 row("proj-lab1-twin", "2.6-lab", "project.html lab-FC1-project-1 (56-102); tests/labs/FC1/lab-FC1-project-1.py", "PASS",
     C9 + " twin byte-identical; run_labs FC1 this round: 'run_labs FC1: PASS (8/8)'."),
 row("proj-lab2-completion", "2.6-lab", "project.html lab-FC1-project-2 (104-150); tests/labs/FC1/lab-FC1-project-2.py", "PASS", C9 + " run_labs 8/8 this round."),
 row("proj-lab2-docstring", "2.6-lab", "project.html line 107; tests/labs/FC1/lab-FC1-project-2.py docstring", "PASS", C9 + " not in delta."),
 row("proj-lab3-fixtures", "2.6-lab", "project.html lab-FC1-project-3 (196-276); tests/labs/FC1/lab-FC1-project-3.py", "PASS", C9 + " run_labs 8/8 this round."),
 row("proj-prose-numbers", "2.6-prose", "project.html lines 54, 58, 101, 176, 186-193, 198, 275", "PASS", C9 + " none of these lines is in the round-10 delta."),
 row("proj-fixture-claims", "2.6-prose", "project.html line 275 vs grader/test_project.py lines 171-301", "PASS", C9 + " no delta in either range."),
 row("proj-hours-arithmetic", "2.6-hours", "project.html section#budget lines 285-292; data-hours-project=20 (line 34)", "PASS",
     "Re-read this round: hours column 1+2+5+4+2+3+3 = 20 = data-hours-project=\"20\" (line 34). Line 289 changed text only, hours still 2."),
 row("proj-check-pages-dag", "2.6-structure", "course/modules/FC/FC1/*.html", "PASS", "Re-run this round: check_pages --all and check_dag --all print PASS for every unit including FC1."),
 row("proj-dag-closure", "2.6-dag", "project.html lines 58 and 178", "PASS", C9 + " not in delta."),
 row("proj-notation", "2.6-notation", "project.html; grader/*.py; tests/labs/FC1/lab-FC1-project-*.py; cards.json", "PASS",
     C9 + " plus the round-10 text (line 289, test_project.py 506-514, cards c013/c054/c070/c071/c082/c091/c092/c115-c118) read: no new symbol. Note: lambda (λ) is used in the L01 lesson and in c013/c091 but has no entry in notation/notation.json; this is an L01 lesson-slice matter, recorded in notes."),
 row("proj-banned-phrases", "2.6-prose", "project.html; grader/*.py; lab twins", "PASS", C9 + " re-scanned: no process words in the round-10 text."),
 row("proj-reading-list", "2.6-refs", "project.html section#reading lines 320-327; references/references.json", "PASS", C9 + " neither file changed in the delta."),
 row("proj-named-conditions", "2.6-autograder", "project.html Constraints lines 163-167; grader/test_project.py lines 407-419 (side tests), 192-232, 329-337, 373", "FAIL",
     "Page line 163 says side not in {+1,-1} raises ValueError, and line 289 says side is refused for every value other than +1 and -1. The grader's side tests (test_project.py lines 407-419) cover only side 0, 2 and -2. Mutant ledgers/FC1/mutants/r10n01_side_three_accepted.py (refuses side 0 and +-2, accepts +-3) SURVIVES mutate_graders --unit FC1 --seeds 0-9 (ledgers/FC1/scripts/FC1-c-r10/mutate_FC1_s0-9.out: 'SURVIVED r10n01_side_three_accepted.py ... -> None').",
     "Add a test in grader/test_project.py that refuses side values such as 3, -3 and 100 (each with ValueError via must_raise), or narrow line 289 to the values the grader tests. Re-run run_graders, the alternatives and mutate_graders."),
 row("proj-failure-messages", "2.6-autograder", "grader/test_project.py lines 75-93, 534-557", "PASS", C9 + " not in delta."),
 row("proj-test-docstring", "2.6-autograder", "grader/test_project.py lines 464-487 and 506-514", "PASS",
     "Re-read this round: test_repeated_events_calls_agree (506-514) docstring says the bond and the trade are pure; the body asserts checked_events equality for both bond.events() and trade.events(). Docstring matches body. Test passes on reference (run_graders 50/50)."),
 row("proj-mutants-killed", "2.6-mutants", "ledgers/FC1/mutants/ (66 files); tools/mutate_graders.py --unit FC1 --seeds 0-9", "FAIL",
     "Re-run this round: 'mutate_graders FC1: FAIL (65/66 killed)' (ledgers/FC1/scripts/FC1-c-r10/mutate_FC1_s0-9.out). The one survivor is r10n01_side_three_accepted.py.",
     "Kill r10n01 with a grader test for side values outside {+1,-1} beyond 0, 2, -2 (see proj-named-conditions)."),
 row("proj-new-mutants-r10", "2.6-mutants", "ledgers/FC1/mutants/r10n01..r10n04", "FAIL",
     "Four new student-error mutants written this round: r10n01 side accepts 3 and -3 (SURVIVED); r10n02 coupon -1 accepted (KILLED by test_bond_negative_coupon_is_refused, seed 0); r10n03 yield -9999 refused early (KILLED by test_yield_just_above_minus_one_is_accepted, seed 0); r10n04 price 0 refused (KILLED by test_trade_price_zero_is_accepted_and_kept, seed 0).",
     "Kill r10n01 (see proj-named-conditions)."),
 row("proj-mutant-set-d-and-c", "2.6-mutants", "ledgers/FC1/mutants/ c*, r*, v*, d*, f*, m*", "PASS",
     "All 62 earlier mutants re-run with mutate_graders --unit FC1 --seeds 0-9 this round: 61 killed, the sole survivor is the new r10n01. Output in FC1-c-r10/mutate_FC1_s0-9.out."),
 row("proj-silence-coverage", "2.6-autograder", "project.html line 163; grader/test_project.py lines 464-505", "PASS", C9 + " lines 464-505 are unchanged; the delta starts at 506."),
 row("proj-lint-types", "2.6-lint", "course/modules/FC/FC1; repo mypy --no-incremental", "PASS",
     "Re-run this round: ruff check and ruff format --check on course/modules/FC/FC1 and tests/labs/FC1 pass; `mypy --no-incremental` -> 'Success: no issues found in 229 source files'."),
 row("proj-privacy-claim", "2.6-prose", "project.html footer line 340", "PASS", C9 + " line 340 not in delta."),
 row("proj-reference-deployment", "2.6-deployment", "course/modules/FC/FC1/grader/reference.py (git-tracked, git ls-files); BLUEPRINT.md lines 400-401", "FAIL",
     "BLUEPRINT.md lines 400-401 require deployment to exclude every grader/reference.py. The file is tracked (git ls-files). Grep of .github/workflows/ci.yml, tools/ and config for an exclusion finds none; the only references are the grader tools themselves. The reference docstring (reference.py lines 1-4) states that no file enforces the exclusion.",
     "Add the exclusion to the publish step (or a .gitignore-style deploy filter) that removes course/**/grader/reference.py, and cite it here."),
 row("cards-scan-98", "2.6-cards", "course/modules/FC/FC1/cards.json (118 cards)", "PASS",
     "Delta read in full: 7 modified objects (c013, c054, c070, c071, c082, c091, c092) and 4 added (c115-c118); the other 107 objects are JSON-identical to pin 33744e5 (checked by a per-object diff on sorted keys). Count 118 is the file's current length."),
 row("cards-numbers", "2.6-cards", "cards.json vs L01-L05 text; c013, c054, c070, c071, c082, c092, c115-c118", "PASS",
     "c082: 216 x 10060 = 2172960 (verified by python); L05 lab output prints 2172960 cents (L05.html line 377). c092: 181790 and 686189 printed by Lab 1 Part C (L01.html lines 301-302); 1000*(1-0.45^11)/0.55 = 181790 recomputed. c054: 11 x 11 = 121 pairs (L03.html line 330, 169)."),
 row("cards-labels-and-hypotheses", "2.6-cards", "cards.json backs (all); c013 vs L01.html lines 155-156", "PASS",
     "c013 now says For a loss lambda >= 0; Proposition 4.1 (L01.html line 155-156) states the equity claim with no lambda >= 0 condition, and the card adds the stated hypothesis as the lesson's Assumption 4.0 context. Other card backs byte-identical to pin 33744e5."),
 row("cards-hypothesis-c036", "2.6-cards", "cards.json FC1-c036 back; L03.html Definition 1.2 (lines 61-62)", "PASS", C9 + " object not in delta."),
 row("cards-misconception-refs", "2.6-cards", "cards.json c070, c071 backs; L04.html lines 372, 376", "PASS",
     "c070 'Only the shares that meet the best ask fill at its price' matches L04.html line 372 'Only the first 60 shares fill at the screen price'. c071 'a sell stop ... can be below the stop price' matches L04.html line 376 and fixture B (lab output line 338: 985 below 990)."),
 row("cards-grades-and-basis", "2.6-cards", "cards.json FC1-c092 (grade T, basis 'Lab 1, Part C (typed-in parameters)'); c054 (C); c014, c029, c091, c093, c095, c096", "FAIL",
     "c092 is graded T, but its answer 181790 cents appears only in the Lab 1 Part C printout (L01.html line 302). The page proves only the limit 181818 cents (L01.html line 142, Proposition 3.5), not total deposits after stage 10 under phi = 1/2; L01 line 460 grades only the lab's True checks T. Under the grade rule (rule 9) a value read off a lab is C naming the lab. c054 is C and matches (L03.html line 480). c091 has no grade field now (a question card, consistent with c114).",
     "Grade FC1-c092 C with basis 'Lab 1, Part C (printed; typed-in parameters)', or prove 181790 in L01 by a closed form for phi = 1/2 and keep T. Re-run check_pages and check_projects after editing cards.json through the builder."),
 row("cards-lesson-agreement", "2.6-cards", "cards.json c070, c071, c082, c092, c115-c118 vs L02, L03, L04, L05", "PASS",
     "c115 (Example 2.4, L02.html line 113; Definition 2.1 values commodities, derivative, exchange at lines 91-96). c116 (Remark 1.2, L02.html lines 62-63; Definition 1.1 line 57). c117 (Remark 1.3, L03.html line 66-67). c118 (Definition 1.2 and L05 offsets_nondecreasing, L05.html line 66; lab code lines 215-240). Confirmed by running the L05 lab with CLEARING_OFFSET=3: 'offsets_nondecreasing False'. c082 agrees with L05.html lines 375-377."),
 row("cards-notation-Q", "2.6-notation", "cards.json (grep for bare Q and V_b)", "PASS", C9 + " new objects c115-c118 contain no Q or V_b."),
]

frag = {
 "unit": "FC1",
 "slice": "c",
 "round": 10,
 "verifier": "Claude Haiku 5.5, independent verifier for FC1 slice c (project.html, grader, project labs, cards.json), round 10; did not build FC1",
 "pin": "fa61d6e",
 "base": "round 9 fragment /Users/billyribeiro/.fanout/frags/C-FC1-c.round9.json (pin 33744e5, context only). Delta 33744e5..fa61d6e in this slice: project.html line 289 (budget row text), grader/test_project.py lines 506-514 (test_repeated_events_calls_agree adds trade purity), cards.json (c013, c054, c070, c071, c082, c091, c092 modified; c115-c118 added). reference.py, instance.py, starter.py and tests/labs/FC1 byte-identical.",
 "checkout": ROOT,
 "scratch": "/tmp/fc1c10-collect, /tmp/fc1c10_alts, /tmp/fc1c10_l05.py",
 "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
 "verdict": None,
 "rows": rows,
 "mutants": [
  {"id": "r10n01_side_three_accepted", "description": "Student error: CashTrade refuses side 0 and +-2 but accepts +-3 (side rule not 'not in {+1,-1}').", "killed_by": None},
  {"id": "r10n02_coupon_minus_one_accepted", "description": "Student error: Bond accepts coupon_bps of -1.", "killed_by": "test_bond_negative_coupon_is_refused (seed 0)"},
  {"id": "r10n03_yield_minus_9999_refused", "description": "Student error: bond_price_cents refuses yield_bps at -9999 (one step early).", "killed_by": "test_yield_just_above_minus_one_is_accepted (seed 0)"},
  {"id": "r10n04_price_zero_refused", "description": "Student error: CashTrade refuses price_cents of 0.", "killed_by": "test_trade_price_zero_is_accepted_and_kept (seed 0)"},
  {"id": "existing-62-mutants", "description": "All 62 earlier mutants in ledgers/FC1/mutants/ re-run with mutate_graders --unit FC1 --seeds 0-9.", "killed_by": "61/62 killed; the survivor is r10n01"},
 ],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Out of slice (L01 lesson): the symbol lambda (λ) is used in L01.html (Proposition 4.1, Remark 4.2) and by c013 and c091, and has no entry in notation/notation.json (grep for 'lambda' returns nothing). The L01 verifier should decide whether it is a notation FAIL.",
  "Grade-rule judgement: c092 is FAIL on the rule that a value read off a lab printout is C naming the lab; the lab uses typed-in parameters, not SIMULATED data. If the rule is read as limited to SIMULATED labs, the row would be a PASS with a recorded ruling.",
  "Not re-run this round: run_labs for lab-FC1-L0x (lesson slices), pytest tests for labs (pytest_labs; the twin content did not change), verify_refs was not re-run (references unchanged in this slice), fetch_data and render_curriculum not run (no curriculum change in the slice), the full pytest suite not run.",
  "Browser: page_smoke ran the in-browser suite on one seed through the repo harness, not a real browser session.",
  "Non-slice items in the round 9 notes (L03 Q as volume, grade-table wording in L01/L02) were not re-checked by this slice verifier."
 ],
 "summary": "",
}
bad = [r['id'] for r in rows if r['status'] not in ('PASS','FAIL')]
assert not bad, bad
frag['verdict'] = 'PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL'
n = len(rows); f = sum(1 for r in rows if r['status']=='FAIL')
frag['summary'] = (f"FC1-c round 10: verdict {frag['verdict']}. Rows {n}: PASS {n-f}, FAIL {f}. "
  "FAILs: proj-named-conditions and proj-mutants-killed/proj-new-mutants-r10 (grader gap: side values beyond 0, 2, -2 accepted, surviving mutant r10n01, cited sentence project.html line 163 and 289); "
  "cards-grades-and-basis (c092 graded T on a lab-printed value); proj-reference-deployment (no exclusion of grader/reference.py, BLUEPRINT.md 400-401; carried from round 9).")
out = "/Users/billyribeiro/.fanout/wt/verifyC10-FC1-c/ledgers/FC1/FC1-c.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(out, frag['verdict'], n, f)
