import json
import sys

OLD = "/Users/billyribeiro/.fanout/frags/S-FC2-b.round5.json"
old = {r["id"]: r for r in json.load(open(OLD, encoding="utf-8"))["rows"]} if False else None
prev = json.load(open(OLD, encoding="utf-8"))
old = {r["id"]: r for r in prev["rows"]}
assert len(old) == 70, len(old)

def carry(rid, files):
    ev = old[rid]["evidence"]
    assert old[rid]["status"] == "PASS", rid
    return {
        "id": rid,
        "check": old[rid]["check"],
        "location": old[rid]["location"],
        "status": "PASS",
        "evidence": f"Carried from round 5 ({files} byte-identical since the previous pin dde0486b): " + ev,
    }

def fresh(rid, check, location, evidence):
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}

RE = "ledgers/FC2/scripts/FC2-b-r6/"
rows = []
# commands, re-run this round
rows += [
    fresh("FC2b-cmd-check_pages", "gate", "index, L01-L08, cards.json (unit gate)",
          f"Re-run this round: .venv/bin/python tools/check_pages.py --unit FC2 -> 'check_pages FC2: PASS', exit 0 ({RE}gates1.txt)."),
    fresh("FC2b-cmd-check_dag", "gate", "L04-L06 links and dfn",
          f"Re-run: tools/check_dag.py --unit FC2 -> 'check_dag FC2: PASS', exit 0 ({RE}gates1.txt)."),
    fresh("FC2b-cmd-check_projects", "gate", "project.html (unit gate, outside slice)",
          f"Re-run: tools/check_projects.py --unit FC2 -> 'check_projects FC2: PASS', exit 0 ({RE}gates1.txt)."),
    fresh("FC2b-cmd-run_graders", "gate", "grader/ (unit gate, outside slice; grader/test_project.py changed in this delta)",
          f"Re-run: tools/run_graders.py --unit FC2 --seeds 0-49 -> 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0 ({RE}run_graders.txt)."),
    fresh("FC2b-cmd-run_labs", "gate", "tests/labs/FC2 (unit, and L04, L05, L06 separately)",
          f"Re-run: tools/run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)'; --page L04, L05, L06 each 'PASS (1/1)' ({RE}run_labs.txt)."),
    fresh("FC2b-cmd-page_smoke", "gate", "L04.html, L05.html, L06.html (each run alone)",
          f"Re-run: tools/page_smoke.py --unit FC2 --pages L04 (then L05, then L06, each alone) -> 'page_smoke modules/FC/FC2/L0n.html: PASS' and 'page_smoke FC2: PASS', exit 0 each ({RE}page_smoke_L04.txt, _L05.txt, _L06.txt)."),
    fresh("FC2b-cmd-twins-isolated", "gate", "tests/labs/FC2/lab-FC2-L04-1.py, lab-FC2-L05-1.py, lab-FC2-L06-1.py",
          f"Re-run: .venv/bin/python -I -W error on each twin from the repo: exit 0 and 0 bytes stderr; stdout equals the page's expected block exactly (23, 21, 23 lines; checked by script). Outputs in {RE}L04.out, L05.out, L06.out."),
    fresh("FC2b-cmd-ruff", "gate", "tests/labs/FC2 twins",
          f"Re-run: ruff check tests/labs/FC2/ -> 'All checks passed!'; ruff format --check -> '11 files already formatted' ({RE}lint_refs.txt)."),
    fresh("FC2b-cmd-mypy", "gate", "repository mypy configuration",
          f"Re-run: mypy --no-incremental -> 'Success: no issues found in 385 source files', exit 0 ({RE}lint_refs.txt)."),
    fresh("FC2b-cmd-pytest", "gate", "tests/test_labs.py -k FC2; tests/test_page_checks.py; tests/test_run_labs.py",
          f"Re-run: pytest -k FC2 on test_labs.py -> 11 passed, exit 0; test_page_checks.py + test_run_labs.py -> 47 passed, exit 0 ({RE}pytest.txt)."),
    fresh("FC2b-cmd-verify_refs", "gate", "references/references.json; L04-L06 carry no data-cite",
          f"Re-run: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({RE}lint_refs.txt). Live run not performed (network; no L04-L06 page cites a key)."),
]
# labs
rows += [
    fresh("FC2b-lab-L04-twin", "lab", "L04.html:123-244; tests/labs/FC2/lab-FC2-L04-1.py",
          f"Changed this delta (twin docstring lines 8-10; page lines 136 and 243). Page code equals twin exactly (script: code==twin); expected block L04.html:220-242 equals twin stdout exactly ({RE}L04_twin_stdout.txt, L04.out). Lab output lines 222-242 re-derived: payoffs 25.00 at 125, break-evens 108/93, path hold values 6.56/7.29/8.10/9.00/10.00, best dates 1 and 3 (18.00, 14.58)."),
    fresh("FC2b-lab-L06-twin", "lab", "L06.html:165-318; tests/labs/FC2/lab-FC2-L06-1.py",
          f"Changed this delta (page line 171-175 and twin docstring lines 4-9, same text). Page code equals twin exactly; expected block L06.html:294-316 equals twin stdout exactly ({RE}L06_twin_stdout.txt). Interpretation L06.html:317 consistent with output (shares as fractions 1/2, 3/4, 5/6; bond -20, -30, -50)."),
    fresh("FC2b-lab-L04-hypothesis", "lab", "L04.html:125 vs expected block L04.html:220-242",
          "Hypothesis text re-read: call payoff zero up to 100 USD and spot-100 above (grid 0..200 step 25 USD); break-even profits 108 and 93; best exercise dates 1 and 3; hold value 6.56 USD. Each matches the expected block (exact match). Line 125 unchanged this delta."),
    fresh("FC2b-lab-L06-hypothesis", "lab", "L06.html:167 vs expected block L06.html:294-316",
          "Hypothesis: one-period price 30 (3000 cents), two-period 45 (4500 cents), one-period, four path and self-financing checks print True. Output lines 299, 301, 306, 312-316 confirm each. Line 167 unchanged this delta."),
    fresh("FC2b-lab-L06-docstring", "lab", "tests/labs/FC2/lab-FC2-L06-1.py:1-12 (shown on L06.html:170-178); printed lines L06.html:297-309",
          f"Re-verified against this delta's docstring change (adds 'and in closed form'). Cents are printed on exactly the time-0 lines 228 (V0 one period, 3000 cents), 230 (discounted expectation, 3000 cents), 246 (backward-induction V0, 4500 cents), 253 (closed form, 4500 cents); after-move, expiry and stock values (226, 239-245, 303-304) are in currency units only; shares print as Fractions (227, 298, 308, 310, 311). Matches the docstring and code (cents() is half-up). Output in {RE}L06.out."),
]
# maths L04 changed hunks
rows += [
    fresh("FC2b-math-L04-s1-s2", "math", "L04.html:57-112 (A1-A5, Def 1.1, Lemma 1.2, Def 2.1, Prop 2.2, Prop 2.3, Remark 2.4)",
          "Re-read in full. Prop 2.2 proof (L04.html:99) and Prop 2.3 proof (L04.html:107) re-derived: each uses A2, A3 (and A5 for 2.3); Remark 2.4 (L04.html:111) now reads 'Lesson 5 treats the date-0 comparison of an American and a European call', a pointer with no equality claim; hypotheses of Prop 2.2 (A2, A3) and 2.3 (A2, A3, A5) stated and used. Lemma 1.2 identity re-checked by cases (L04.html:80)."),
    fresh("FC2b-math-L04-example-2.5", "math", "L04.html:115-121 (Example 2.5, Remark 2.6)",
          "Re-derived: r = ln(10/9) = 0.10536 (L04.html:116); call intrinsic 0,20,0,0,10; hold 10(9/10)^4 = 6.561 -> 6.56; exercise at 1 gives 20*9/10 = 18; put best date 3, 20(9/10)^3 = 14.58; hold put 0. Remark 2.6 (L04.html:120) changed sentence has no numbers and no result claim."),
]
# plan / cards changed
rows += [
    fresh("FC2b-plan-L06-A2", "plan", "L06.html:55 (A2) vs plans/FC2-build-plan.md section 5.2 A2 (plan lines 287-288)",
          "Carried from round 5 (course/modules/FC/FC2/L06.html:55 and plans/FC2-build-plan.md byte-identical since dde0486b; L06.html delta hunk is lines 171-175 only): " + old["FC2b-plan-L06-A2"]["evidence"]),
    fresh("FC2b-plan-L04-no-L05-result", "structure / architect decision",
          "L04.html:51, 111, 120, 243, 248, 258, 262 vs plan lines 105 and 431-432",
          "Round-5 FAIL re-verified and now PASS. Plan line 105 (L04 lab: 'the theorem waits for L05') and plan lines 431-432 ('not stated in L04') are met: the seven L04 locations now carry only pointers ('Lesson 5 treats the date-0 comparison of an American and a European call'), with no Theorem 4.1 equality, no (N) and no r >= 0 claim (checked L04.html:51, 111, 120, 243, 248, 258, 262). grep of L04.html for 'Theorem 4.1', 'Remark 4.2', 'no income' returns no result claim. Judgement (not a FAIL): L04.html:262 says 'exercising at once is never better than selling', a consequence of Prop 2.2 proved in L04 that expressly leaves holding-vs-selling open; it is not the plan's 'early exercise never optimal' result, which L05 Theorem 4.1 proves."),
    fresh("FC2b-cards-hypotheses", "cards", "cards.json FC2-c059 (L04 hypotheses) and the other slice cards",
          "Round-5 FAIL re-verified and now PASS. FC2-c059 is rewritten (cards.json, this delta): it no longer cites Theorem 4.1. Its Prop 2.3 claim carries A2, A3, A5 (Proposition 2.3, L04.html:103-104) and Remark 2.4. All other slice cards that state a proposition were re-checked against their hypotheses: c066-c067, c069-c071 (now with (N) and r >= 0 in L05.html:301), c078, c084-c085, c089, c093, c132, c160-c162, c163."),
    fresh("FC2b-cards-delta-round1", "cards",
          "cards.json delta dde0486b..e896b7a4 for L04-L06: FC2-c059, c060, c081, c082 changed; c184, c185 added; c176 removed",
          f"Delta hunks read in full (cards_delta: {RE}cards_delta.txt; git diff dde0486b e896b7a4 -- course/modules/FC/FC2/cards.json). Changed or new slice cards re-verified from scratch: c059 PASS (above); c060 PASS (Prop 2.2 under A2, A3 at L04.html:99; 'Section 4' is the L04 misconceptions, L04.html:253-273); c081 PASS (R_f = 1 + r_1, Definition 1.1 at L06.html:59); c082 PASS (A6: 0 < d < R_f < u, Definition 1.2 at L06.html:64); c184 PASS (u S_0 or d S_0, Definition 1.2); c185 PASS (1/R_f, Definition 1.1). Unchanged slice cards carried (see FC2b-cards-L05-c064 and the rest). Removed c176 has no remaining reference (grep)."),
    fresh("FC2b-cards-coverage", "cards", "cards.json: slice cards with lesson L04, L05, L06",
          f"Re-counted this round ({RE}cards_delta.txt): 72 slice cards: L04 18 (19 - c176), L05 25 (unchanged), L06 29 (27 + c184, c185). Key-results mirror counts unchanged."),
    fresh("FC2b-cards-duplicates", "cards", "cards.json whole deck, pairwise scan",
          f"Re-run this round: pairwise difflib scan of all 172 cards ({RE}cards_dup_r6.py, cards_dup_r6.txt). No duplicate ids; no pair with identical front and back; the high-similarity pairs (65 over 0.6) were read; the new c184/c185 differ in question (possible values; value of a sure payoff) from c081, c082 and c166."),
    fresh("FC2b-cards-near-duplicate", "cards", "near-duplicate pairs in the slice",
          f"Re-read from {RE}cards_dup_r6.txt: L05 c160/c162 (lower bounds on call vs put, different claims), c066/c161/c162, c069/c070, c057/c135 (put best date vs call exercise value), c084/c163, c089/c084, c136/c137, c166/c184 and c184/c185 are distinct questions; accepted as in round 5 and not failed."),
    fresh("FC2b-cards-grade-ruling9", "cards", "cards.json grades for L04-L06",
          "C-graded slice cards (c058, c061, c072, c073, c074, c079, c095, c148, c155, c171) each name Lab 1 or a lab output; T-graded cards cite a Theorem, Lemma, Proposition, Example, Remark, Definition or Problem on the page. c075 (T, Problem E1 exact) accepted as in round 5."),
    fresh("FC2b-cards-L04-grades", "cards", "cards.json FC2-c051..c062, c135, c142, c143, c158, c159, c179 (c176 removed)",
          "Re-read this round: grades match content (T for Lemma/Prop/Example/Remark facts: c052, c054-c057, c059, c060, c062, c135, c179; C for lab output: c058, c061). Hub and key-results mirror unchanged."),
    fresh("FC2b-cards-L04-rest", "cards", "L04 cards without grade (c051, c053, c142, c143, c158, c159)",
          "Re-read: c051 (payoffs, Definition 1.1), c053 (Definition 2.1), c142 (A3, L04.html:62), c143 (A4, L04.html:63), c158 (Props 2.2/2.3 need A2, A3, A5; Section 3 L04.html:249), c159 (A2, L04.html:61). All agree with the current L04 text."),
]
rows += [
    fresh("FC2b-cards-L05-C-grades", "cards", "cards.json L05 C-graded cards c072, c073, c074, c079, c155, c171",
          f"Carried from round 5 (cards.json objects c072, c073, c074, c079, c155, c171 byte-identical since dde0486b; lab output unchanged, lab-FC2-L05-1.py byte-identical): " + old["FC2b-cards-L05-C-grades"]["evidence"]),
    fresh("FC2b-cards-L05-c064", "cards", "cards.json FC2-c064 (Theorem 1.2 card)",
          "Carried from round 5 (cards.json object FC2-c064 byte-identical since dde0486b; L05.html:62-72 byte-identical): " + old["FC2b-cards-L05-c064"]["evidence"]),
    fresh("FC2b-cards-L05-rest", "cards", "cards.json L05 cards c063-c071, c075, c076, c078, c080, c132, c153, c160-c162, c180",
          "Re-verified this round for the cards whose cited Theorem 4.1 text changed (L05.html:301, 310): c071 states A1-A5, (N), r >= 0 and Remark 4.2 (PASS); c080 (r < 0; Remark 4.2 and Problem R2) and c132 (r >= 0 hypotheses; Remark 4.2) PASS. Others are byte-identical objects, carried from round 5, and their cited L05 subjects (Definition 1.1, Theorem 1.2, Theorem 2.2, Definition 3.1, Remark 3.3, Theorem 3.2, Corollary 3.4, Problems E1, Section 5) are byte-identical since dde0486b."),
    fresh("FC2b-cards-L06-grades", "cards", "cards.json FC2-c081..c098, c136, c137, c148-c150, c163, c166, c174, c181",
          "Changed c081 and c082 re-verified (above). Unchanged objects carried from round 5: T cards cite Theorem 1.4 (a)-(c), Theorem 2.2, Theorem 3.3, Example 1.5/1.6/3.4, Section 4 and Remark 1.7, all byte-identical; C cards (c095, c148) cite Lab 1 output unchanged."),
    fresh("FC2b-cards-L06-rest", "cards", "L06 cards without grade",
          "Re-read: c083 (Definition 1.3), c088 (Definition 2.1), c090 (Definition 3.1), c092 (Definitions 3.1, 3.2), c166 (Definition 1.2), c174 (Definition 3.5), c184 (Definition 1.2), c185 (Definition 1.1); each agrees with the current L06 text. Others carried (byte-identical objects)."),
    fresh("FC2b-cards-key-mirror", "cards", "key-results tables L04.html:383-393, L05.html:450-460, L06.html:401-410 vs cards",
          "Tables byte-identical in this delta (changes at L04 51/111/120/243/248/258/262, L05 51/301/310/483/517, L06 171-175 only). Each key-result row still maps to a card: L04 c052, c054, c055, c056, c057; L05 c064, c066-c070, c071, c155/c072; L06 c163, c084, c085, c093, c094. No row cites c176."),
    fresh("FC2b-cards-c176-added", "cards", "cards.json FC2-c176 (removed in this delta); FC2-c184, c185 (added)",
          f"c176 (an L04 card on A1) is removed in this delta and no reference to FC2-c176 remains (grep over course, tests, tools, references, plans: no match; {RE}cards_delta.txt). A1 is still stated at L04.html:60 and is not a key result. c184 and c185 added and verified (see FC2b-cards-delta-round1). PASS: no claim is left without its card."),
]
rows += [
    fresh("FC2b-quiz-L04-L06", "quiz", "L04.html:396-466 (9 items), L05.html:464-534 (9 items), L06.html:412-481 (10 items)",
          "L04 and L06 quiz unchanged. L05 items re-checked where changed: Q3 (L05.html:483, 'Under A3 and (N)'; explain 489 consistent with Theorem 2.2(a)) and Q7 (L05.html:517; explain now matches Remark 4.2). Numeric answers re-derived: 17, 20, 77, 6.56, 9.85, 12, 1, 40.48, 0.5, 30, 0.75, 45, 75 (no change)."),
    fresh("FC2b-misconception-L04-L06-other", "misconception", "L04.html:256-271 (re-verified), L05.html:327-337, L06.html:327-335 (carried)",
          "L04 misconceptions 1-4 re-read; misconceptions 1 and 2 changed in this delta and re-derived (see FC2b-plan-L04-no-L05-result). Carried from round 5 for L05.html:327-337 and L06.html:327-335 (byte-identical since dde0486b): " + old["FC2b-misconception-L04-L06-other"]["evidence"][-400:]),
    fresh("FC2b-hours", "hours", "L04-L06 data-hours; index.html:29 and the hub hour cards",
          "Carried from round 5 (course/modules/FC/FC2/index.html and data-hours lines byte-identical since dde0486b): hours L04 7, L05 8, L06 8 match eyebrows; the eight lesson hours 6+8+9+7+8+8+8+6 = 60 equal the hub split (index.html data-hours-lessons=60)."),
    fresh("FC2b-banned-process", "prose", "L04-L06 visible prose and twin docstrings",
          f"Re-read this delta's hunks and grep of L04-L06 and the twins for builder/verifier/round/revised/previous/updated/fixed/draft/TODO/delta: only 'fixed' (a fixed list, a fixed rational), 'Previous' (nav) and a 'rounded' display rule matched; none is process language ({RE}lint_refs.txt not used; grep output recorded in this run)."),
    fresh("FC2b-notation", "notation", "L04-L06 math vs notation/notation.json",
          "notation/, references/, tools/ and plans/FC2-build-plan.md byte-identical to dde0486b (git diff --quiet), so the registered symbols are unchanged. No new symbol appears in the delta: the new text uses (N), r, A1-A5, D, V_A, V_E, Lesson labels already registered or defined on the page."),
    fresh("FC2b-dag-links", "dag", "L04-L06 concept links and definitions",
          "check_dag FC2 PASS (re-run, gates1.txt). The delta removes no link and adds no concept use outside the unit's closure (no new data-concept)."),
    fresh("FC2b-define-before-use-self-financing", "define-before-use", "L06.html:161-162 (Definition 3.5), first use L06.html:167",
          "Carried from round 5 (L06.html:161-162 and 167 unchanged in this delta): " + old["FC2b-define-before-use-self-financing"]["evidence"][-250:]),
    fresh("FC2b-scope-words", "scope", "L04-L06 'every', 'all', 'never', 'any', 'always', 'only', 'exactly', 'same' in the changed hunks and full reads",
          "Changed hunks re-read: L04.html:111 and L04.html:262 ('never better than selling' is backed by Prop 2.2, L04.html:99); L04 lab docstring 'The lab makes no claim about that choice at any date' is a negative claim about the lab, which prints only path dates 0-4 (no scope claim is computed); L05.html:483 ('Under A3 and (N)'); L05.html:517 ('does not say how the buyer ... should behave on each path', matching Remark 4.2). No unsupported universal claim found in the hunks."),
    fresh("FC2b-simulated-labels", "simulated", "L04 Example 2.5 (L04.html:115), L04 lab (L04.html:124-128), L05 lab (L05.html:132-136), L06 lab (L06.html:167-178)",
          "SIMULATED labels re-read; each lab docstring states the price data are written in the code or are model inputs (L04 twin line 3; L05 twin line 3; L06 twin lines 4-9). No market-data claim introduced in the delta."),
    fresh("FC2b-figures", "figures", "L04-L06 (no figures, data-files or data-cite)",
          "grep of L04, L05, L06 for data-files, data-cite, <figure>, figures-L and <svg>: no match (run this round). Carried from round 5 for the absence of figures."),
    fresh("FC2b-lab-rng-network", "lab", "tests/labs/FC2 L04/L05/L06 twins (read in full)",
          "Re-read this round. Imports: L04 twin fractions only (line 17); L05 twin fractions and itertools (lines 17-18); L06 twin math and fractions (lines 16-17). No random, no network, no file read. Output stderr 0 bytes under -W error."),
    fresh("FC2b-num-L04", "prose numbers", "L04.html prose numbers (lines 51, 73, 116, 120, 125, 243, 258-266, 335-377, 389-390)",
          "Re-derived each number again: 0.10536 (ln(10/9)), 6.56, 18.00, 14.58, 108, 93, 17.00, 25.00, 127.43484 (R3 family, L04.html:360: 20000/729 = 27.434842 + 100), 32.805 (R3, L04.html:374), 10.00/8.10/9.00 (E1, L04.html:335). Line 243 changed sentence adds no number. All agree with the printed expected block."),
    fresh("FC2b-num-L04-why-locator", "prose numbers", "L04.html:51, 116, 360, 374 (locators for derived numbers)",
          "L04.html:51 changed sentence contains no number; 116, 360, 374 re-derived (above) and agree."),
    fresh("FC2b-struct-L04", "structure", "L04.html (BUILDER_RULES 4.2 order and counts)",
          "Section order 1-8 and the lesson structure unchanged (same heading ids s1-s8, same blocks; the delta is same-line-count replacement). Quiz 9 items, problem set 3+3+3+3 (M1-M3, P1-P3, E1-E3, R1-R3)."),
    fresh("FC2b-lab-L05-twin", "lab", "L05.html:131-287; tests/labs/FC2/lab-FC2-L05-1.py",
          "Carried from round 5 (lab-FC2-L05-1.py and L05.html:131-287 byte-identical since dde0486b; L05 delta hunks at 51, 301, 310, 483, 517 only). Re-run this round: twin under -I -W error exit 0, stdout equals L05.html:265-285 exactly (script). Carried evidence: " + old["FC2b-lab-L05-twin"]["evidence"][:300]),
    fresh("FC2b-lab-L05-hypothesis", "lab", "L05.html:133 vs expected block L05.html:265-285",
          "Carried from round 5 (L05.html:133 and 265-285 byte-identical): the hypothesis's claims (40 pairs, zero parity cost, -300 cents planted put, three triples with 90 USD middle) are re-confirmed by the run this round (output lines 268-285)."),
    fresh("FC2b-lab-L05-D-claim", "lab", "tests/labs/FC2/lab-FC2-L05-1.py lines 5-9 (docstring) and L05.html:138-142",
          f"Carried from round 5 (twin docstring and L05.html:138-142 byte-identical) and re-checked this round by a D sweep (script {RE}l05_d_sweep_r6.py, output {RE}l05_d_sweep_r6.txt): D = 1/100 breaks bounds (call at 80 USD 10120 > spot, put at 80 USD 200 > DK = 80), D = 0, 1/2, 9/10, 1, 3/2 give convexity violations 0; D = 9/10 gives 0 bound violations, matching the docstring claims."),
    fresh("FC2b-lab-L05-named-errors", "lab", "L05.html:286; L05.html:281-284 printed triples",
          "Carried from round 5 (L05.html:281-286 byte-identical): the three violated triples 8000/9000/10000, 8000/9000/11000, 8000/9000/12000 re-derived by hand (lambda = 1/2, 2/3, 3/4; chords 2000, 2033.3, 2250 < 2500)."),
]
rows += [
    fresh("FC2b-math-L05-thm1.2", "math", "L05.html:62-68 (Theorem 1.2, proof)",
          "Carried from round 5 (L05.html:62-68 byte-identical): proof re-derived this round (payoff X at tau is zero; A3 applied to V0 < 0 and V0 > 0 via -X)."),
    fresh("FC2b-math-L05-remark1.3-hypotheses", "math", "L05.html:70-72 (Remark 1.3)",
          "Carried from round 5 (L05.html:70-72 byte-identical): Remark 1.3 lists A1, A2, A3, A5 and the rate of A4, as used in the Theorem 1.2 proof (L05.html:67)."),
    fresh("FC2b-math-L05-thm2.2", "math", "L05.html:83-103 (Theorem 2.2 (a)-(d), proof, Remark 2.3)",
          "Carried from round 5 (L05.html:83-103 byte-identical): all four parts re-derived this round; the uses of (N) in (a) and (c) and not in (b) and (d) match Remark 2.3."),
    fresh("FC2b-math-L05-thm3.2-cor3.4", "math", "L05.html:109-129 (Def 3.1, Theorem 3.2 cases (i)-(iv), Remark 3.3); L05.html:289-295 (Corollary 3.4)",
          "Carried from round 5 (L05.html:109-129 and 289-295 byte-identical): lambda identity re-derived (P1), four cases re-derived this round, Corollary 3.4 proof checked (payoff non-negative; A3 gives C(K1) >= C(K2))."),
    fresh("FC2b-math-L05-thm4.1-remark4.2", "math", "L05.html:299-311 (Theorem 4.1 and proof, Remark 4.2)",
          "Changed this delta (L05.html:301 adds 'with r >= 0' to the hypotheses list; L05.html:310 Remark 4.2 now opens 'Under A1 to A5 and (N), with r >= 0'). Re-derived this round: V_A(0) >= V_E(0) from Prop 2.3 (A2, A3, A5); date-t portfolio (buy European call, short share, lend e^{-r(tau-t)}K) has payoff (K - S_tau)^+ >= 0 by A1, A2, A4; A3 gives V_E(t) >= S_t - e^{-r(tau-t)}K >= S_t - K when r >= 0; the cash flows net non-negative; A3 excludes the reverse position. Hypotheses match the statement. Note (not a failure): (N) is listed but the proof never invokes it (L05.html:303-306)."),
    fresh("FC2b-math-L05-problems", "math", "L05.html:348-436 (M1-M3, P1-P3, E1-E3, R1-R3)",
          "Carried from round 5 (L05.html:348-436 byte-identical): re-derived this round. M1 9.85; M2 bound 12, initial value -9; M3 chord 9.5; P1 identity; P3 parity carries convexity (S terms cancel); E1 0, 100, 800 cents; E3 bound 8 = put; R1 payoff independent of put price; R2 bound 9.48 < 20; R3 corollary."),
    fresh("FC2b-math-L05-why-it-matters-rate", "2.9 prose / 2.4 math", "L05.html:51 (why-it-matters)",
          "Re-verified (changed line). The non-negative-rate qualifier of round 2 is still present: 'under A1 to A5, (N) and a non-negative rate' (L05.html:51) and 'Theorem 4.1' (L05.html:301). The added '(N)' is used before it is defined: see FC2b-define-before-use-N."),
    fresh("FC2b-num-L05", "prose numbers", "L05.html prose numbers (lines 51, 286, 315, 352, 359, 366, 402-416, 434, 480-531)",
          "Re-derived: 40.48 (L05.html:315 and Q at 528-531: 100 e^{-0.1} - 50 = 40.484); 9.85; 12; 9.48 (R2 at 434: 120 - 1.10517*100 = 9.483); 8.00; 0.9*120-100 = 8; 1.00 USD second difference; the changed lines 483 and 517 contain no number. All agree with the printed output."),
    fresh("FC2b-struct-L05", "structure", "L05.html (BUILDER_RULES 4.2 order and counts)",
          "Section order and counts unchanged (same heading ids s1-s10; the delta replaces text on lines already present; quiz 9 items; problem set 9 items). Re-read in full this round."),
    carry("FC2b-misconception-L05-1", "L05.html:323-326"),
]
# The remaining carried rows whose evidence is not yet included
rows += [
    carry("FC2b-math-L04-problems", "L04.html:281-377"),
    carry("FC2b-math-L06-thm1.4", "L06.html:76-100"),
    carry("FC2b-math-L06-thm2.2-thm3.3", "L06.html:116-158"),
    carry("FC2b-math-L06-examples", "L06.html:93-99 and 155-158"),
    carry("FC2b-math-L06-remarks-misconceptions", "L06.html:101-105, 114 and 327-336"),
]
# Mixed carry prefix for the remaining L05 rows already present above (L05.html:62-72 etc.)
row_ids = [r["id"] for r in rows]
missing = [rid for rid in old if rid not in row_ids]
print("missing from new rows:", missing)
extra = [rid for rid in row_ids if rid not in old]
print("new ids:", extra)
json.dump(rows, open(RE + "rows_r6_partial.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
