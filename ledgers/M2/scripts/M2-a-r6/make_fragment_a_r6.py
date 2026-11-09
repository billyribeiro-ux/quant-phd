"""Build the round-6 delta fragment for unit M2, slice a (verifier checkout at e896b7a4).

Rows whose subject is byte-identical since the previous pin dde0486b are carried from the round-5
fragment with the carry prefix; rows whose subject changed in the delta are re-verified and given new evidence.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
R5 = json.load(open("/Users/billyribeiro/.fanout/frags/S-M2-a.round5.json", encoding="utf-8"))
old = {r["id"]: r for r in R5["rows"]}

PFX = {
    "idx": "Carried from round 5 (course/modules/M/M2/index.html cited lines byte-identical since the previous pin dde0486b; the only index.html hunk is line 130): ",
    "L01": "Carried from round 5 (course/modules/M/M2/L01.html cited lines byte-identical since the previous pin dde0486b; the L01 hunks are lines 154, 158 and 163): ",
    "L02": "Carried from round 5 (course/modules/M/M2/L02.html byte-identical since the previous pin dde0486b): ",
    "L03": "Carried from round 5 (course/modules/M/M2/L03.html byte-identical since the previous pin dde0486b): ",
    "L04": "Carried from round 5 (course/modules/M/M2/L04.html byte-identical since the previous pin dde0486b): ",
    "L05": "Carried from round 5 (course/modules/M/M2/L05.html cited lines byte-identical since the previous pin dde0486b; the L05 hunks are lines 94, 307 and 309): ",
    "L06": "Carried from round 5 (course/modules/M/M2/L06.html byte-identical since the previous pin dde0486b): ",
    "h07": "Carried from round 5 (course/modules/M/M2/L04.html:156 and course/modules/M/M2/L13.html:105-115 byte-identical since the previous pin dde0486b; L13.html is not in the delta): ",
    "twin": "Carried from round 5 (tests/labs/M2 twins byte-identical since the previous pin dde0486b): ",
    "card": "Carried from round 5 (cited course/modules/M/M2/cards.json entries byte-identical since the previous pin dde0486b; the changed entries are M2-c002, c008, c064, c113, c135, c233, c390 and the added c424, c425): ",
}

# id -> prefix key for carried rows (subject byte-identical since dde0486b)
CARRY = {
    "M2a-R1-H02": "idx", "M2a-R1-H03": "idx", "M2a-R1-H04": "idx", "M2a-R1-H05": "idx",
    "M2a-R1-H06": "idx", "M2a-R1-H07": "h07", "M2a-R3-H09": "idx", "M2a-R1-X-REF-01": "idx",
    "M2a-R1-X-HRS-01": "L01", "M2a-R1-X-GRADE-01": "L05",
    "M2a-R1-L01-MATH-02": "L01", "M2a-R1-L01-LAB-01": "L01", "M2a-R1-L01-GRADE-01": "L01",
    "M2a-R1-L01-PROSE-01": "L01", "M2a-R4-L01-PROSE-02": "L01", "M2a-R1-L01-QUIZ-01": "L01",
    "M2a-R1-L01-CARD-02": "card",
    "M2a-R1-L02-MATH-01": "L02", "M2a-R1-L02-MATH-02": "L02", "M2a-R1-L02-LAB-01": "L02",
    "M2a-R1-L02-PROSE-01": "L02", "M2a-R1-L02-PROSE-02": "L02", "M2a-R1-L02-E-01": "L02",
    "M2a-R1-L02-QUIZ-01": "L02", "M2a-R1-L02-CARD-01": "card",
    "M2a-R1-L03-MATH-01": "L03", "M2a-R1-L03-MATH-02": "L03", "M2a-R1-L03-MATH-03": "L03",
    "M2a-R1-L03-PROSE-01": "L03", "M2a-R1-L03-LAB-01": "L03", "M2a-R1-L03-QUIZ-01": "L03",
    "M2a-R1-L03-CARD-01": "card",
    "M2a-R1-L04-MATH-01": "L04", "M2a-R1-L04-MATH-02": "L04", "M2a-R1-L04-LAB-01": "L04",
    "M2a-R1-L04-CARD-01": "card", "M2a-R1-L04-QUIZ-01": "L04", "M2a-R1-L04-CARD-02": "card",
    "M2a-R1-L05-MATH-01": "L05", "M2a-R1-L05-LAB-01": "L05", "M2a-R1-L05-PROSE-01": "L05",
    "M2a-R1-L05-QUIZ-01": "L05", "M2a-R1-L05-CARD-01": "card",
    "M2a-R1-L06-MATH-01": "L06", "M2a-R1-L06-MATH-02": "L06", "M2a-R1-L06-MATH-03": "L06",
    "M2a-R1-L06-LAB-01": "L06", "M2a-R1-L06-QUIZ-01": "L06",
}

NEW_EVID = {
    "M2a-R1-G01": "Re-run at e896b7a4: ledgers/M2/scripts/M2-a-r6/g01_check_pages.out = 'check_pages M2: PASS', EXIT 0.",
    "M2a-R1-G02": "Re-run at e896b7a4: g02_check_dag.out = 'check_dag M2: PASS', EXIT 0. check_dag checks concept links only (plans/M2-build-plan.md:331), so it does not detect the plain link added at L05.html:94; see M2a-R6-X-DEP-01.",
    "M2a-R1-G03": "Re-run at e896b7a4: g03_run_labs.out = 'run_labs M2: PASS (27/27)', EXIT 0.",
    "M2a-R1-G04": "Re-run at e896b7a4: g04_twins_isolated.out: python -I -W error exits 0 for tests/labs/M2/lab-M2-L01-1.py through lab-M2-L06-1.py. Page code equals twin and expected block equals output: test_labs (g05_pytest_labs.out) and run_labs (g03_run_labs.out).",
    "M2a-R1-G05": "Re-run at e896b7a4: pytest tests/test_labs.py -k 'M2 and (L01 or L02 or L03 or L04 or L05 or L06)' -> 6 passed, EXIT 0 (g05_pytest_labs.out; collect-only count 6).",
    "M2a-R1-G06": "Re-run at e896b7a4: tools/page_smoke.py --unit M2 --pages index L01 L02 L03 L04 L05 L06 --skip-sweep -> 'page_smoke M2: PASS', EXIT 0 (g06_page_smoke.out).",
    "M2a-R1-G07": "Re-run at e896b7a4: ruff check tests/labs/M2/ -> 'All checks passed!' (g07_ruff_check.out); ruff format --check tests/labs/M2/ -> '27 files already formatted' (g07_ruff_format.out); mypy --no-incremental on the six slice twins -> 'Success: no issues found in 6 source files' (g07_mypy.out); all EXIT 0.",
    "M2a-R1-G08": "Re-run at e896b7a4: verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' EXIT 0 (g08_verify_refs_offline.out); verify_refs.py --unit M2 -> 'live re-verification of M2: 2 of 560 entries, 0 problems' EXIT 0 (g08_verify_refs_live_M2.out).",
    "M2a-R1-G09": "Re-run at e896b7a4: tools/check_projects.py --unit M2 -> 'check_projects M2: PASS', EXIT 0 (g09_check_projects.out).",
    "M2a-R6-G10": "New gate row. Re-run at e896b7a4 because cards.json changed in the delta: tools/build_site.py --check -> 'site data current: 6 outputs', EXIT 0 (g10_build_site_check.out); pytest tests/test_build_site.py -> all passed, EXIT 0 (g10_pytest_build_site.out).",
    "M2a-R1-H01": "Re-verified at e896b7a4 (index.html:1-199; the only index.html hunk is line 130): eight section headings in order (On this page, Objectives, Prerequisites, Placement diagnostic, Lessons, The project ladder, Data status, Core reading); 24 distinct L01-L24 links; placement block has 8 items, 2 data-skill items, data-mastery 0.8 and 8 explain blocks (scripted count at e896b7a4).",
    "M2a-R3-H08": "Re-verified at e896b7a4: index.html:127 (data-answer 12.02, rung 2) and index.html:133 (data-answer 3.01, rung 1) are unchanged. Arithmetic recomputed: (1.1)^4 + (0.9)^4 - 2 = 0.1202, divided by 0.01 = 12.02 = 12 + 2h^2 at h = 0.1; central difference of x^3 at x = 1 is 3 + h^2 = 3.01. Rung labels match project.html:40-50 ('Rung 1 · Worked example', 'Rung 2 · Completion problem') and project.html:121 (Lab 2, completion problem). Two data-skill items: BUILDER_RULES 5.1 met. The explanation at line 130 changed this delta and is judged in M2a-R4-H08b.",
    "M2a-R4-H08b": "Re-verified at e896b7a4. index.html:130 now reads: 'Lesson 13 writes out the expansions of f(x + h) and f(x - h) with their remainders and subtracts them for the first difference. Adding them, as the rung 2 completion problem does, gives 2f(x) + h^2 f''(x) plus remainder terms, and subtracting 2f(x) leaves h^2 f''(x) plus remainder terms.' L13.html:91-92 writes the two expansions with remainders; L13.html:93 says 'Subtract the second from the first' for the first difference. project.html:121 says 'Lesson 13 writes them and subtracts them for the first difference; here they are added', which agrees with the hub sentence. Algebra recomputed: the order-two Taylor expansions with remainders sum to 2f(x) + h^2 f''(x) plus remainder terms, so subtracting 2f(x) leaves h^2 f''(x) plus remainder terms. The hub sentence now describes the lesson it cites. PASS.",
    "M2a-R1-X01": "Re-scanned at e896b7a4 with ledgers/M2/scripts/M2-a-r6/prose_scan_a_r6.py (banned phrases, process words, questions, scope words) on index.html and L01-L06. Hits: 'fixed' in ordinary math prose (fixed number, fixed epsilon, fixed sign); 'grader' in index.html (the autograder, unchanged line); learner quiz prompts. The changed sentences (index.html:130; L01.html:154-163; L05.html:94; L05.html:307-309) contain no banned phrase; the 'every' in Proposition 3.1 is backed by its proof (L01.html:163).",
    "M2a-R1-X02": "Structure and number checks PASS at e896b7a4: cards.json has 398 cards (396 at dde0486b plus M2-c424 (L01) and M2-c425 (L09)); no duplicate id or front; 83 slice cards (L01-L06); every Definition/Proposition/Corollary/Example/Theorem/Assumption/Problem/Lab/Section token and every decimal in a slice card back appears in its lesson (ledgers/M2/scripts/M2-a-r6/cards_check.py; the 21 'Section N' and 'Misconception N' flags are section-number markup and list positions, checked by hand). Changed slice cards re-read against the lesson text: M2-c002, M2-c008, M2-c390 and M2-c424 agree with L01.html:59-62, 154-163 (see M2a-R1-L01-CARD-01). FAIL: M2-c064 (cards.json:451, lesson L06) says 'every result that uses it begins its statement with \"Assuming Assumption 2.1\"', with no scope. L06.html:73 and L06.html:325 scope the same claim to Lesson 6 ('every result below', 'every result in section 2 and section 3'). Lessons outside L06 have T-graded key-result rows that use Assumption 2.1 without that opening: L10.html:387 ('\\(\\int_0^1 dx/(1+x)^2 = 1/2\\), under Assumption 2.1 of Lesson 6'), L10.html:390, L11.html:362, L11.html:365, L12.html:376, L12.html:380. A scope word needs a computation or an explicit hypothesis (VERIFIER rule 4); the card is false as written.",
    "M2a-R1-X03": "Re-verified at e896b7a4 (scripted search of the slice pages and cards): K appears in L01.html only as the tail index and the Proposition 3.1 bound (L01.html:154-163); kappa appears in L05.html only as the constant term of p(x) at lines 307 and 309, defined in the problem statement; no kappa or K in the cards with another meaning (card scan). notation/notation.json (8 symbols, 26 macros, unchanged in the delta) registers neither K, kappa nor delta, and its 'about' field makes conventionally local letters per-lesson. No registered symbol is used with another meaning in the slice pages: T appears only as the grade label; Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, mathbb{Q}, Prob, E and Var do not appear; the macro \\R is used for the real line. Greek letters alpha, beta, gamma, eta are local (L05.html R1 and L05.html:186). The round-5 LOW note on delta reused as a constant is resolved: the constant is now kappa.",
    "M2a-R1-X04": "Re-verified at e896b7a4 (index.html:69-137; the delta changed line 130 only, in an explain block): 8 items, 2 data-skill (lines 127 and 133) with data-answer 12.02 and 3.01 and tolerance 1e-6, data-mastery 0.8, 8 explain blocks. Mastery arithmetic: 80 percent of 8 is 6.4, so at least 7 correct; 6/8 = 75 percent, 7/8 = 87.5 percent (index.html:71).",
    "M2a-R1-X05": "Re-counted at e896b7a4 within section#quiz of each slice lesson: L01 9 items and 9 explain blocks; L02 9 and 9; L03 8 and 8; L04 9 and 9; L05 9 and 9; L06 9 and 9 (all within 8 to 15). No quiz line changed in the delta.",
    "M2a-R1-X-CARD-IDS": "Re-verified at e896b7a4: cards.json has 398 cards, 0 duplicate ids and 0 duplicate fronts (scripted). The new M2-c424 (L01, convergent and divergent by Definition 2.1) duplicates no other card; the other convergence cards (M2-c011, c012, c019, c165, c176, c179, c376) ask different questions. Near-duplicate notes from round 5 remain LOW notes. M2-c425 (L09) and M2-c113, c135, c233 are outside the slice.",
    "M2a-R1-X-DEP-01": "FAIL. check_dag M2 passes (g02), but check_dag checks concept links only (plans/M2-build-plan.md:331), and this defect is a plain page link. The delta turned the prose pointer at L05.html:94 into a link: '(higher derivatives are defined in <a href=\"L07.html#s1\">Lesson 7, section 1</a>)'. Assumption 1.4 (L05.html:93-94) relies on a third derivative f''' that is defined later: L07.html:54 (h2 id s1, 'Higher derivatives') and L07.html:59 (Definition 1.1). L01-L05 never define f'' or f''' (scripted search for 'second derivative', 'third derivative', 'higher derivative', f'' and f''' in L01-L05; the only hits are L05.html:94 and L05.html:219). L05.html:219, 282 and 284 then use f''' and p'''. The plan forbids this: plans/M2-build-plan.md:101 'Ordering check (no lesson links a later definition)' and plans/M2-build-plan.md:363 'Define before use ... the lesson never relies on a later definition'. Round 5 recorded this as a LOW prose-only note; the new link makes an explicit link to a later lesson.",
    "M2a-R1-L01-MATH-01": "Re-read in full at e896b7a4 (L01.html:55-189, every line): Definition 2.1 (L01.html:59-62); Proposition 2.2 and proof with epsilon/2 thresholds and the triangle inequality (L01.html:66-78); Example 2.3: a_n - 2 = -1/(n+1), and N > 1/epsilon gives 1/(n+1) < epsilon (L01.html:80-83); Lab 1 predictions and narrative (L01.html:87-150, expected block L01.html:140-148 checked against run_labs); Section 3 with K (L01.html:152-166): tail from index K, Proposition 3.1 with hypothesis c_n = a_n for n >= K and the first K-1 terms unrestricted, proof with N' = max(N, K) and c_n = a_n for n >= N'; Section 4: Example 4.1 (the triangle chain 2 <= |1-L| + |L+1| < 2 is false, L01.html:174) and Proposition 4.2 with B = max(|a_1|, ..., |a_{N-1}|, |L|+1), checked for n < N and n >= N (L01.html:177-186). All recomputed by hand; no error found.",
    "M2a-R1-L01-CARD-01": "Re-verified at e896b7a4: changed cards M2-c002 (cards.json:12), M2-c008 (cards.json:51-52) and M2-c390 (cards.json:2629-2630) and new M2-c424 (cards.json:2774-2786) against L01.html: Definition 2.1 (L01.html:59-62, with the convergent and divergent sentence at L01.html:61); Section 3 (L01.html:152-154, 'from index K'); Proposition 3.1 (L01.html:156-159, K and K-1). The other 13 L01 cards (M2-c001, c003-c007, c009-c013, c376, c391) are byte-identical since dde0486b and carried.",
    "M2a-R1-L05-MATH-02": "Re-verified at e896b7a4 (L05.html:91-95; line 94 changed): the displayed expansion (f(x+h) - f(x-h))/(2h) = f'(x) + h^2 f'''(x)/6 + o(h^2) is the correct central-difference expansion (Taylor to third order gives f(x+h) - f(x-h) = 2h f' + h^3 f'''/3 + o(h^3)). It is labelled an assumption and not proved (L05.html:93-94). Every use begins with 'Assuming Assumption 1.4' (L05.html:99, 105, 219, 282, 284; scanned at e896b7a4). The forward pointer to Lesson 7 is a DAG defect, recorded as M2a-R6-X-DEP-01 (FAIL), not a mathematical defect.",
    "M2a-R1-L05-MATH-03": "Re-verified at e896b7a4 (L05.html:307-309, changed lines): p(x) = alpha x^3 + beta x^2 + gamma x + kappa. Central differences: the linear term gives gamma; the quadratic gives ((x+h)^2 - (x-h)^2)/(2h) = 2x, so 2 beta x; the cubic gives ((x+h)^3 - (x-h)^3)/(2h) = 3x^2 + h^2, so alpha(3x^2 + h^2); the constant cancels. Sum = 3 alpha x^2 + 2 beta x + gamma + alpha h^2 = p'(x) + alpha h^2, for every x and h != 0. The solution text matches the statement (L05.html:309). Key rows L05.html:338-339 and the rest of 224-343 are byte-identical since dde0486b and carried.",
    "M2a-R1-L06-CARD-01": "FAIL. M2-c064 (cards.json:451, lesson L06) changed this delta and is re-verified: its back says 'every result that uses it begins its statement with \"Assuming Assumption 2.1\"', unscoped, while L06.html:73 and L06.html:325 scope the claim to Lesson 6. Counterexamples in L10.html:387, L10.html:390, L11.html:362, L11.html:365, L12.html:376 and L12.html:380 (T-graded key-result rows that use Assumption 2.1 without the opening). Full evidence in M2a-R1-X02. The other 14 L06 cards (M2-c062, c063, c065-c074, c394, c414) are byte-identical since dde0486b and carried from round 5.",
}

FIX = {
    "M2a-R1-X02": "Scope M2-c064 to this lesson in cards.json:451, for example 'In Lesson 6, every result that uses it begins its statement with \"Assuming Assumption 2.1\"', which matches L06.html:73 and L06.html:325; or rewrite the key-result rows L10.html:387-390, L11.html:362-365 and L12.html:376-380 so that each begins with 'Assuming Assumption 2.1'. Then re-run the card check.",
    "M2a-R1-X-DEP-01": "Remove the link and the forward dependency at L05.html:94: define f'' and f''' inside Lesson 5 (as the derivative of f' and of f'') before Assumption 1.4, or move Assumption 1.4 and its uses in L05.html:99, 105, 219, 282 and 284 to a lesson after Lesson 7. Then re-verify the DAG row.",
    "M2a-R1-L06-CARD-01": "Same fix as M2a-R1-X02: scope M2-c064 (cards.json:451) to Lesson 6 or make the cited key-result rows begin with 'Assuming Assumption 2.1'.",
}

rows = []
for rid, r in old.items():
    pass

order = [r["id"] for r in R5["rows"]]
order.insert(order.index("M2a-R1-G09") + 1, "M2a-R6-G10")
for rid in order:
    if rid == "M2a-R6-G10":
        base = {"id": rid, "check": "2.9 build_site --check and test_build_site for the changed cards.json (gate)",
                "location": "tools/build_site.py --check; tests/test_build_site.py"}
    else:
        base = {k: old[rid][k] for k in ("id", "check", "location")}
    if rid in FIX and rid != "M2a-R1-X02" and rid != "M2a-R1-L06-CARD-01" and rid != "M2a-R1-X-DEP-01":
        pass
    if rid in NEW_EVID:
        ev = NEW_EVID[rid]
    elif rid in CARRY:
        ev = PFX[CARRY[rid]] + old[rid]["evidence"]
        if rid == "M2a-R1-L06-ASSUME-01":
            pass
    elif rid == "M2a-R1-L06-ASSUME-01":
        ev = PFX["L06"] + old[rid]["evidence"] + " Re-scanned at e896b7a4: every statement block naming Assumption 2.1 begins 'Assuming Assumption 2.1' (Theorem 2.2 L06.html:78, Theorem 2.3 L06.html:88, Corollary 3.1 L06.html:103, remark L06.html:111, key rows L06.html:322-324); the remaining uses are proof sentences, problem prompts and the scope sentence L06.html:325."
    else:
        raise SystemExit(f"no treatment for {rid}")
    status = "FAIL" if rid in ("M2a-R1-X02", "M2a-R1-X-DEP-01", "M2a-R1-L06-CARD-01") else "PASS"
    if status == "PASS" and rid in old and old[rid]["status"] == "FAIL" and rid != "M2a-R4-H08b":
        raise SystemExit(f"status regression check for {rid}")
    row = dict(base)
    row["status"] = status
    row["evidence"] = ev
    if status != "PASS":
        row["fix"] = FIX[rid]
    rows.append(row)

LOC_OVERRIDE = {
    "M2a-R1-X02": "course/modules/M/M2/cards.json (83 slice cards, lessons L01-L06; changed entries M2-c002, c008, c064, c390, new c424)",
    "M2a-R1-X-DEP-01": "course/modules/M/M2/L05.html:94 (new link to L07.html#s1), L05.html:219, 282, 284; L01.html-L05.html (no definition of higher derivatives); index.html; L01-L06.html",
    "M2a-R1-L06-CARD-01": "course/modules/M/M2/cards.json:451 (M2-c064) and the other L06 cards (M2-c062 to c074, c394, c414)",
}
for r in rows:
    if r["id"] in LOC_OVERRIDE:
        r["location"] = LOC_OVERRIDE[r["id"]]
# H08b keeps its id and check from round 5 (now PASS)
for r in rows:
    if r["id"] == "M2a-R4-H08b":
        r["check"] = old["M2a-R4-H08b"]["check"]
        r["location"] = old["M2a-R4-H08b"]["location"]

counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"

frag = {
    "unit": "M2",
    "slice": "a",
    "round": 6,
    "verifier": "independent verifier (Haiku 5.5), unit M2 slice a, round 6 (delta verification, ruling 30)",
    "pin": "e896b7a4 (detached checkout HEAD)",
    "base": "Round-5 fragment /Users/billyribeiro/.fanout/frags/S-M2-a.round5.json (verified at pin dde0486b). Delta dde0486b..e896b7a4 over the slice: course/modules/M/M2/index.html:130; L01.html:154, 158, 163; L05.html:94, 307, 309; cards.json entries M2-c002 (line 12), c008 (51-52), c064 (451), c390 (2629-2630) and added M2-c424 (2774-2786). Outside the slice and only noted: L10.html:79 and 390, cards M2-c113, c135, c233 and added c425 (L09). Unchanged in the delta: L02, L03, L04, L06 pages, the six slice twins, project.html, tools/, references/, curriculum/, notation/, BUILDER_RULES.md, VERIFIER_RULES.md, the M1 pages. Every round-5 row id is kept; M2a-R6-G10 is new.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS6-M2-a",
    "scratch": "ledgers/M2/scripts/M2-a-r6/",
    "verified_at": "2026-11-09",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice a is a lesson slice, not a project slice: no project grader is in scope and no mutants are required (verifier rules; ruling 26 on mutation of project graders only). mutants is empty by design.",
        "LOW, not FAIL kinds: near-duplicate slice cards M2-c010/c013, c044/c048/c049, c063/c071, c017/c018 (unchanged since round 5).",
        "LOW: 23 slice cards carry no grade key (round 5 counted 22; M2-c424 is a definition card and has none, like M2-c002). Card style, unchanged.",
        "LOW: L04.html:156 forward pointer to Lesson 13 (unchanged since round 3).",
        "Resolved since round 5: the constant in L05.html R1 reused delta (a threshold elsewhere in the same lesson); it is now kappa (L05.html:307, 309).",
        "Outside the slice, seen only through the delta and noted for the owners of the other slices: L10.html:79 now says 'Continuity of f is not a hypothesis of the theorem', consistent with the hypotheses of Theorem 2.1 at L10.html:76-79; L10.html:390 key-result row changed; cards M2-c113 (L08), c135 (L10), c233 (L15) changed and M2-c425 (L09) added; M2-c425 restates a Riemann-sum topic that M2-c122 also covers.",
        "Not checked: lessons L07-L24, project.html, the project grader and the other slice twins (other slices); no browser screenshot of the hub or the lessons (page_smoke only); the live verify_refs run covers the two M2 entries it re-checks, as in earlier rounds.",
        "The committed ledgers/M2/M2-a.json in the checkout held a fragment from a different round and pin; this round overwrote that file in the verifier checkout only (not committed).",
    ],
    "summary": (
        f"M2 slice a, round 6 (delta verification at e896b7a4). {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
        f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Three FAIL rows, all introduced or made explicit by the delta: "
        "M2a-R1-X-DEP-01 (L05.html:94 now links a later lesson, Lesson 7, for the third derivative that Assumption 1.4 uses; plans/M2-build-plan.md:101 and :363); "
        "M2a-R1-X02 and M2a-R1-L06-CARD-01 (card M2-c064 scope: 'every result that uses it' is contradicted by key-result rows in L10-L12). "
        "M2a-R4-H08b (round-5 FAIL) is now PASS: index.html:130 agrees with L13.html:93 and project.html:121. "
        "Gates re-run at e896b7a4 all PASS: check_pages, check_dag, run_labs 27/27, twins isolated, test_labs 6, page_smoke, ruff, ruff format, mypy, verify_refs offline and live M2, check_projects, build_site --check, test_build_site."
    ),
}

out = ROOT / "ledgers/M2/M2-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, len(rows))
