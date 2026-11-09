"""Writes the round-4 E1-b fragment (ledgers/E1/E1-b.json). Row evidence cites scripts under ledgers/E1/scripts/E1-b-r4/."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/E1/scripts/E1-b-r4/"
C5 = "Carried from round 3 (course/modules/E/E1/L05.html and tests/labs/E1/lab-E1-L05-1.py byte-identical since the previous pin 8196077d, git diff --quiet at edbb7aa8): "
CL5 = "Carried from round 3 (course/modules/E/E1/cards.json card objects E1-c054 to E1-c066, E1-c136, E1-c144, E1-c145 byte-identical since 8196077d): "
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

P = "PASS"
row("E1-b-check-pages", "2.9-structure/cards", "course/modules/E/E1/L04.html, L05.html, L06.html, cards.json", P,
    "Re-run at pin edbb7aa8: `.venv/bin/python tools/check_pages.py --unit E1` -> 'check_pages E1: PASS', rc=0 (includes check_cards and banned strings).")
row("E1-b-check-dag", "2.9-DAG", "course/modules/E/E1/L04.html, L05.html, L06.html", P,
    "Re-run: `.venv/bin/python tools/check_dag.py --unit E1` -> 'check_dag E1: PASS', rc=0. Internal anchors re-resolved by " + S + "cross_lesson_r4.py: L04 11, L05 6, L06 11 anchors, 0 problems.")
row("E1-b-run-labs", "2.5-labs", "tests/labs/E1/lab-E1-L04-1.py, lab-E1-L05-1.py, lab-E1-L06-1.py", P,
    "Re-run: `tools/run_labs.py --unit E1 --page L04`, `--page L05`, `--page L06`: each 'run_labs E1: PASS (1/1)', rc=0.")
row("E1-b-twin-isolated", "2.5-labs", "tests/labs/E1/lab-E1-L04-1.py, lab-E1-L05-1.py, lab-E1-L06-1.py", P,
    "Each twin copied alone to a fresh directory and run with `/Users/billyribeiro/.fanout/wt/verifyS4-E1-b/.venv/bin/python -I -W error twin.py`: L04 rc=0, 18 stdout lines, 0 stderr bytes; L05 rc=0, 12 lines, 0 bytes; L06 rc=0, 25 lines, 0 bytes.")
row("E1-b-page-twin-identity", "2.5-labs", "course/modules/E/E1/L04.html lines 137-250; L05.html 125-235; L06.html 199-386", P,
    S + "twin_identity_r4.py output: 'L04: rc=0 stderr_bytes=0 page_code_equals_twin=True expected_equals_stdout=True stdout_lines=18'; 'L05: ... True True ... 12'; 'L06: ... True True ... 25'; 'ALL OK'.")
row("E1-b-lint-types", "2.5-labs", "tests/labs/E1/lab-E1-L04-1.py, lab-E1-L05-1.py, lab-E1-L06-1.py", P,
    "`.venv/bin/python -m ruff check` on the three twins: 'All checks passed!'; `ruff format --check`: '3 files already formatted'; `.venv/bin/python -m mypy --no-incremental` on the three twins: 'Success: no issues found in 3 source files'.")
row("E1-b-pytest-labs", "2.5-labs", "tests/test_labs.py", P,
    "`.venv/bin/python -m pytest -q tests/test_labs.py -k 'E1 and (L04 or L05 or L06)' -p no:cacheprovider` -> '...  [100%]' (3 passed); `--collect-only` count 3.")
row("E1-b-page-smoke", "2.9-smoke", "course/modules/E/E1/L04.html, L05.html, L06.html", P,
    "`.venv/bin/python tools/page_smoke.py --unit E1 --pages L04 L05 L06` -> 'page_smoke modules/E/E1/L04.html: PASS', 'L05.html: PASS', 'L06.html: PASS', 'page_smoke E1: PASS'; lab-E1-L06-1 runs in 0.1 s.")
row("E1-b-verify-refs", "2.1-citations", "references/references.json; the three pages cite no key", P,
    "`.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems'. No live run (no network use). The References paragraphs of the three pages are outside every delta hunk (see E1-b-attribution).")
row("E1-b-hours", "2.9-hours", "course/modules/E/E1/L04.html:2,35; L05.html:2,35; L06.html:2,35", P,
    "Carried from round 3 (these lines and the hub are byte-identical since 8196077d; no delta hunk touches them): re-grep this round gives data-hours=\"10\" on each of the three html elements and the hub split is unchanged in the delta (git diff --stat 8196077d edbb7aa8 lists no hub or hours file for E1-b).")
row("E1-b-numbers-L04", "2.2-numbers", "course/modules/E/E1/L04.html lines 52, 64, 269-272 (changed), 134, 231-248, 249, 277, 282, 288, 309, 374, 381, 426 (carried)", P,
    "Changed prose re-derived this round with " + S + "numbers_L04_L06_r4.py: p(120)=10; dp/da - 1/22 = 0E-60; (a/p)(dp/da) - 6/11 = -0E-60; p''(120) = -1/5324 True; p'''(120) = 3/1288408 True; (1+a)^(3/2)=1331 and (1+a)^(5/2)=161051 True; eps(10) = -1/5, eps(40) = -2 (Example 1.3); Remark 2.5 dp/da = -1/2. Line 52 'for 0 < p < a/b ... exceeds 1 exactly above a/(2b)' matches Proposition 1.4 (L04 line 88-93). Unchanged numbers on lines 231-249, 277-426 are carried from round 3 (byte-identical since 8196077d).")
row("E1-b-numbers-L05", "2.2-numbers", "course/modules/E/E1/L05.html prose", P,
    C5 + "round-3 row E1-b-numbers-L05 stands; `.venv/bin/python tools/run_labs.py --unit E1 --page L05` re-run PASS this round.")
row("E1-b-numbers-L06", "2.2-numbers", "course/modules/E/E1/L06.html lines 142, 370-384, 385, 394-409 (changed table prose), 430, 438, 492-517, 554-560 (changed row 555)", P,
    "Re-derived this round with " + S + "numbers_L04_L06_r4.py (exact Fractions): d=100; monopoly 50 / 70 / 2500; Cournot each d/3=100/3, total 200/3, fee 160/3, each profit 10000/9 = 1111.11 (whole cents 1111), industry 20000/9 = 2222.22 (whole cents 2222); Bertrand 100 / 20 / 0; Prop 4.1 differences d/6, d/3, d^2/(36b) True. Table (line 409) prints 66.67, 53.33, 2222 and the stated convention (whole cents) rounds 20000/9 to 2222 correctly. Proposition 2.8: closed form equals the iteration for t=0..30 (True); x_30 - d/3 = -25/805306368 (True); first t with error <= 1e-6 is 25 (reference), 25 (90,3,10), 26 (200,4,5), matching Lab Part B. Part C undercut and sharing values (474.909999/237.5, 1874.949999/937.5, 2499.999999/1250, 1875.049999/937.5) match the lab output. Card c088 disagreement is recorded on E1-b-cards-L06, not here.")
row("E1-b-math-L04", "2.4-mathematics", "course/modules/E/E1/L04.html line 64 (Definition 1.1), 52, 269-272 (Taylor proof), 83, 88-93, 300-301, 338, 347, 356, 363, 399, 425, 447, 461", P,
    "Round-3 FAIL is fixed: line 64 now reads 'At every p > 0, a demand curve that slopes down has eps(p) < 0' (card E1-c038 matches). Every sign statement on the page was read (grep of plain text): none is unqualified. Taylor proof re-derived: p(a+-h) expansion to h^4/24 p'''' + O(h^5) is correct; forward quotient p' + h/2 p'' + O(h^2); central quotient p' + h^2/6 p''' + O(h^4) from the difference coefficient 2h^5/120 consistent with O(h^5) remainder. Proposition 1.4 proof (lines 88-93) re-read: |eps| = bp/(a-bp) > 1 iff p > a/(2b), with 0 < p < a/b.")
row("E1-b-math-L05", "2.4-mathematics", "course/modules/E/E1/L05.html lines 67-123, 350-366", P,
    C5 + "round-2 row E1-b-math-L05 stands (round-3 row carried).")
row("E1-b-math-L06", "2.4-mathematics", "course/modules/E/E1/L06.html lines 59-65 (Def 1.1-1.2), 68-156 (Lemma 1.3 to Prop 2.8), 157-190 (Def 3.1, Lemma 3.2, Thm 3.3, Remark 3.4), 391-400 (Prop 4.1), 430-438", P,
    "Changed text re-read in full: Def 2.3 (line 109, 'or best response to x'); Prop 2.8 statement and proof (lines 146-157): base P(0); x_t in [0, d/2] since rho^t in [-1/2,1]; Lemma 2.4 applies because d - x_t >= d/2 > 0; algebra (d/2)(2/3 + rho^t/3) = (d/3)(1 + rho^t/2) = (d/3)(1 - rho^(t+1)) verified; error -(d/3) rho^t, |error| = (d/3)(1/2)^t; line 158 'absolute error halves ... sign alternating' is correct for d > 0. Def 3.1 (line 165) undercut sentence matches Theorem 3.3 Step 3 and Remark 3.4. Theorem 3.3 Steps 1-4 re-read: Case B uses only s_i < 1, so the proof holds for any tie rule. Prop 4.1 proof (line 399) re-derived (script). Hypothesis cross-check: the Lesson 3 cost C(q)=F+cq+kq^2 with k>0 (L03 page, Proposition 2.2 context) matches the L06 sentence that this lesson has no quadratic term.")
row("E1-b-lab-L04", "2.5-labs", "course/modules/E/E1/L04.html lines 137-250 (line 240 expected, 249 interpretation); tests/labs/E1/lab-E1-L04-1.py", P,
    "Twin unchanged since 8196077d (git diff --quiet on lab-E1-L04-1.py); page code equals twin and expected block equals stdout (twin_identity_r4.py, 18 lines); line 249 'elasticity ... 0.5454545455, which is (a/p*)(dp*/da) = 12/22 = 6/11' re-derived (numbers script: 6/11 - 0E-60).")
row("E1-b-lab-L05", "2.5-labs", "course/modules/E/E1/L05.html lines 125-235; tests/labs/E1/lab-E1-L05-1.py", P,
    C5 + "round-2 row E1-b-lab-L05 stands; run_labs and twin identity re-run this round (twin_identity_r4.py L05: True True, 12 lines).")
row("E1-b-lab-L06", "2.5-labs", "course/modules/E/E1/L06.html lines 199-386; tests/labs/E1/lab-E1-L06-1.py", P,
    "Twin unchanged since 8196077d (git diff --quiet). Page code equals twin and expected block (25 lines) equals stdout (twin_identity_r4.py). Part A, B and C figures re-derived by numbers_L04_L06_r4.py (grid and closed-form statements are exact; Part B first-step values 25/25/26 match). The lab's 'four rival fees, three cases' (Remark 3.4) matches the output.")
row("E1-b-grades", "2.3-grades", "course/modules/E/E1/L04.html, L05.html, L06.html (claim tags, key-results tables); cards.json", P,
    "Re-read this round: Prop 1.4 (L04), Prop 2.3, Prop 3.1 unchanged; L06 table row 555 (Prop 2.8, now 'absolute error halving') graded T with basis Proposition 2.8, a proved statement: T correct. Card E1-c072 now has no grade (a definition, like E1-c073 and E1-c074): round-3 FAIL fixed. C-graded cards cite Lab 1 (c051, c066, c084, c085, c133, c143-c148). Newly added definitional cards E1-c153, c155, c156 carry no grade.")
row("E1-b-key-results-L04", "2.3-grades", "course/modules/E/E1/L04.html lines 419-434 (table rows 425-430)", P,
    "Carried from round 3 (lines 419-434 byte-identical since 8196077d; the delta hunks at 49, 61-64, 269-272 do not touch them). Round-3 fix to row 426 stands.")
row("E1-b-key-results-L05", "2.3-grades", "course/modules/E/E1/L05.html lines 372-388 (rows 378-384)", P,
    C5 + "round-2 fix to row 382 stands.")
row("E1-b-key-results-L06", "2.3-grades", "course/modules/E/E1/L06.html lines 548-564 (rows 554-560)", P,
    "Row 555 (Prop 2.8, now 'with the absolute error halving each step') re-read against Proposition 2.8 and re-derived (numbers script). Rows 554, 556-560 re-derived this round against Lemma 1.3, Proposition 1.4, Lemma 2.4, Theorem 2.5, Theorem 3.3 and Proposition 4.1 (numbers script: d/2, 2d/3, d; fees; profits 2500, 10000/9, 20000/9, 0).")
row("E1-b-cards-L04", "2.7-cards", "course/modules/E/E1/cards.json: E1-c038 to E1-c053, E1-c133, E1-c143, E1-c153, E1-c154, E1-c155 (21 cards)", P,
    "Round-3 FAIL is fixed: E1-c038 back now reads 'negative at every p > 0 for a demand curve that slopes down'. All 21 L04 slice cards read this round; " + S + "cards_scan_r4.py (all labelled citations exist in L04; no duplicate ids or normalised fronts) and " + S + "card_numbers_r4.py (every number token appears in L04 text). E1-c155 matches L04 line 64 and Definition 1.1; E1-c153 matches the supply elasticity in Definition 1.1 (line 61-62). E1-c155 is not a duplicate of E1-c041 (c041 is the linear-demand case).")
row("E1-b-cards-L05", "2.7-cards", "course/modules/E/E1/cards.json: E1-c054 to E1-c066, E1-c136, E1-c144, E1-c145 (16 cards)", P,
    CL5 + "round-3 row E1-b-cards-L05 stands (card E1-c062 front reads 'With positive marginal cost, does a monopolist price where demand is unit elastic?'). cards_scan_r4.py: no missing citations for these cards this round.")
row("E1-b-cards-L06", "2.7-cards", "course/modules/E/E1/cards.json: E1-c088 (line 586-589 region), E1-c089 to E1-c091, E1-c156, plus E1-c067 to E1-c070, c072 to c087, c146 to c148", "FAIL",
    "Card E1-c088 back states 'Cournot: ... 20000/9 cents (2222.22) ... (Proposition 4.1 and its reference-case table)'. Round 4 changed the table row (course/modules/E/E1/L06.html line 409) to read '2222 (exact 20000/9)' under the whole-cent rule that the same paragraph states; the card now shows a decimal the table no longer prints. The string 2222.22 occurs in L06 only in a quiz explanation (line 605), not in Proposition 4.1 or its table. Both numbers are correct values. Severity LOW (presentation, ruling 26).",
    "In course/modules/E/E1/cards.json, card E1-c088 back: replace '20000/9 cents (2222.22)' with '20000/9 cents (2222, rounded half up to the whole cent)', so the card matches the table at L06 line 409. Re-run tools/check_pages.py --unit E1.")
row("E1-b-cards-dup-scan", "2.7-cards", "course/modules/E/E1/cards.json (all 154 cards)", P,
    S + "cards_scan_r4.py: total 154 cards, 0 duplicate ids, 0 duplicate normalised fronts; 65 slice cards (L04 21, L05 16, L06 28). Manual reading of new cards: E1-c155 (general elastic/inelastic classification) vs E1-c041 (linear demand) differ in scope; E1-c156 (undercut definition) vs E1-c080 (Bertrand definition) differ in question.")
row("E1-b-cards-locators", "2.7-cards", "course/modules/E/E1/cards.json (65 slice cards)", P,
    S + "cards_scan_r4.py: every labelled citation (Definition, Proposition, Theorem, Lemma, Corollary, Remark, Example, Assumption) in the 65 slice cards is present in its own lesson page; " + S + "card_numbers_r4.py: every number token in the 65 slice cards appears in the lesson text (E1-c088's 2222.22 appears only at L06 line 605, see E1-b-cards-L06).")
row("E1-b-cards-grades", "2.7-cards", "course/modules/E/E1/cards.json E1-c072 (grade removed) and the other slice cards", P,
    "E1-c072 no longer carries grade T (round-3 FAIL fixed). Grades on the 65 slice cards read in cards_scan_r4.py output: T and C only where the card makes a result or a Lab 1 claim.")
row("E1-b-quiz-keys", "2.9-prose", "course/modules/E/E1/L04.html 436-515; L05.html 390-465; L06.html 566-641", P,
    "Carried from round 3 (quiz blocks byte-identical since 8196077d; the L06 delta hunk at line 555 is above the quiz block at 566; the L04 hunks at 49-64, 269-272 are above 436). Quiz keys re-checked against the changed Proposition 2.8 and Definition 1.1 (answer keys unchanged in substance).")
row("E1-b-process-words", "2.9-prose", "course/modules/E/E1/L04.html, L05.html, L06.html (learner text, lab docstrings)", P,
    "Round-4 scan (" + S + "cross_lesson_r4.py): no hit for obviously, clearly, TODO, lorem, TBD, builder, verifier, 'round N' or agent in the visible text of the three pages. Changed sentences (L06 lines 109, 157-158, 165, 399, 555) contain no process words. check_pages PASS.")
row("E1-b-banned-phrases", "2.9-prose", "course/modules/E/E1/L04.html, L05.html, L06.html", P,
    "check_pages E1 PASS (banned strings, BUILDER_RULES 1.3-1.4); " + S + "cross_lesson_r4.py: 0 hits for obviously, clearly, TODO, lorem, TBD.")
row("E1-b-scope-words", "2.9-prose", "course/modules/E/E1/L04.html, L05.html, L06.html", P,
    "Words added or changed in the delta read in context: 'exactly' (L04 line 52: 'exactly above the midpoint' under 0 < p < a/b, true by Proposition 1.4); 'every' (L06 line 165 'every tie rule' in Definition 3.1 and Theorem 3.3, proof covers any shares); 'each' (L06 line 158 'halves at every step', true for every t >= 0); 'only' (card E1-c089 'Only under Bertrand competition', supported by Proposition 4.1 ordering; card E1-c090 'the reaction only to a rival that trades nothing', true since R(x) = d/2 iff x = 0).")
row("E1-b-notation", "2.4-notation", "notation/notation.json; L04, L05, L06 math", P,
    "notation.json registers 8 symbols (T; Phi and Phi^-1; gamma_3; gamma_4; R^ast; R^{e ast}; R_f; Q). grep of plain text on each page: Phi, gamma, R^ast, R_f, mathbb{Q} count 0; no math-mode symbol T in L04-L06 (0 segments). New local symbol rho (L06 Prop 2.8 proof, lines 153-154) is not registered and is not used elsewhere in E1 (grep). Note (not a registry row): R denotes revenue in L04 and the reaction function in L06 Def 2.3; the registry does not cover R, and the two lessons do not share a proof.")
row("E1-b-dag", "2.9-DAG", "course/modules/E/E1/L04.html, L05.html, L06.html", P,
    "check_dag E1 PASS (re-run). Cross-lesson anchors resolve (" + S + "cross_lesson_r4.py).")
row("E1-b-cross-lesson", "2.9-DAG", "course/modules/E/E1/L04.html line 52; L05.html lines 38, 52, 140, 241-244; L06.html lines 52, 82, 192, 649-652", P,
    "Anchors re-resolved this round (" + S + "cross_lesson_r4.py: L04 11, L05 6, L06 11 internal anchors, 0 problems). L06 claim 'the competitive equilibrium of Lesson 3 ... derived for a cost with a quadratic term, k > 0' matches L03 cost C(q) = F + cq + kq^2 with k > 0 (cross_lesson_r4.py output).")
row("E1-b-attribution", "2.1-attribution", "course/modules/E/E1/L04.html line 519; L05.html line 469; L06.html line 645", P,
    "Carried from round 3 (the three References paragraphs are outside every delta hunk and byte-identical since 8196077d): each states that the lesson cites no outside source, consistent with the three pages having no citation key.")
row("E1-b-figures", "2.8-figures", "course/modules/E/E1/L04.html, L05.html, L06.html", P,
    "Re-grep this round: data-files count 0 and svg count 0 on each page. All numbers come from exact labs (Decimal or Fraction), so no SIMULATED label or dataset is required.")
row("E1-b-structure", "2.9-structure", "course/modules/E/E1/L04.html, L05.html, L06.html", P,
    "check_pages E1 PASS (re-run this round, rc=0). Section order and minimum counts unchanged by the delta (the delta adds no section or block).")
row("E1-b-footer-claim", "2.9-prose", "course/modules/E/E1/L04.html line 530, L05.html line 480, L06.html line 656 (footer)", P,
    "Carried from round 3 (footer lines outside every delta hunk, byte-identical since 8196077d): 'Each result is proved on the page, proved under a stated assumption ...' remains true for the changed Proposition 2.8 and Definition 3.1, which are proved on the page.")
row("E1-b-r2-delta", "2.9-delta", "git diff 8196077d edbb7aa8 for course/modules/E/E1/{L04,L05,L06}.html, cards.json, tests/labs/E1/lab-E1-L0{4,5,6}-1.py", P,
    "Delta read hunk by hunk: L04.html lines 49, 61-64, 269-272; L06.html lines 109, 146-157, 165, 399, 555; cards.json cards E1-c038 (back), E1-c072 (grade removed), E1-c089, E1-c090, E1-c091 (hypotheses), E1-c155 and E1-c156 (new), plus cards of L02, L07, L08 and L09 (other slices). L05.html, lab-E1-L04-1.py, lab-E1-L05-1.py, lab-E1-L06-1.py are byte-identical (git diff --quiet). Every hunk in the slice was read and re-verified.")
row("E1-b-r2-changed-prose", "2.9-prose", "L04.html lines 118, 305, 374; L05.html lines 366, 382; L06.html lines 385, 438", P,
    "Carried from round 3 (these lines are outside every 8196077d..edbb7aa8 hunk, so byte-identical since the previous pin): round-2 row E1-b-r2-changed-prose stands.")

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
non_pass = [r for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "E1",
    "slice": "b",
    "round": 4,
    "verifier": "independent verifier, Haiku 5.5 (claude-haiku-5-5); did not build E1; checkout pinned at edbb7aa8",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "8196077d5f56c3919d33e69888176d197d378ad4 (round-3 pin). Round-3 fragment: /Users/billyribeiro/.fanout/frags/S-E1-b.round3.json",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS4-E1-b",
    "scratch": "/tmp/e1b4",
    "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Scope: L04, L05, L06 pages; lab twins lab-E1-L04-1, lab-E1-L05-1, lab-E1-L06-1; the 65 cards with lesson L04, L05 or L06 in course/modules/E/E1/cards.json. "
        "Delta 8196077d..edbb7aa8 read hunk by hunk for the slice. L05.html and all three twins are byte-identical to the previous pin and are carried where marked. "
        "Round-3 FAILs (E1-b-math-L04, E1-b-cards-L04, E1-b-cards-grades) are fixed and re-verified. "
        "Mutation testing: not applicable (lab twins are demonstrations; the slice has no project grader, ruling on lab twins). No mutants are listed and no alternative implementations were run. "
        "Not run, with reason: check_projects, run_graders, mutate_graders (no project in this slice); build_site --check and render_curriculum (architect gate, not this slice); verify_refs without --offline (no network use). "
        "Full re-read of the unchanged lines of L04, L05 and L06 was not repeated this round; unchanged text is carried from round 3 under the verifier-rules carry clause. "
        "Not checked: the hub index.html and lessons L01-L03, L07-L09, project.html (other slices); cards of other slices in the shared cards.json (c104 L07, c114 L08, c128 L09, c157-c158 L08); a pixel-level visual diff beyond page_smoke; the L04 quiz and L06 quiz items were carried, not re-read. "
        "Ruling 26 classification: the one non-PASS row (E1-b-cards-L06, card E1-c088) is LOW (presentation: both values are correct; the card does not match the current table digits). No row is a false or unproved statement, a missing hypothesis, a wrong number, an over-graded claim, a failing gate, a surviving non-equivalent mutant, or an unsupported lab statement. Under ruling 26 this round raises no blocking row for E1-b; the LOW row is deferrable to plans/KNOWN-ISSUES.md with id E1-b-cards-L06 if the fixer does not change the card. "
        "Judgement call: the 'R' letter is revenue in L04 and the reaction function in L06 (not a registry symbol); noted, not a row. "
        "Line numbers for L06 changed text refer to the checkout at edbb7aa8."
    ),
    "summary": (
        f"E1-b round 4 (pin edbb7aa8): {len(rows)} rows, {len(rows) - len(non_pass)} PASS, {len(non_pass)} non-PASS. "
        "The one non-PASS row is LOW: card E1-c088 back shows 2222.22 for the Cournot industry profit, while the L06 reference table now prints 2222 under the whole-cent rule. "
        "The round-3 FAILs are fixed: L04 line 64 and card E1-c038 now state the sign of the elasticity only for p > 0, and card E1-c072 no longer carries grade T. "
        "Gates re-run on the pin all pass: check_pages, check_dag, run_labs (L04, L05, L06), isolated twins under -I -W error, page_smoke, ruff, mypy, pytest test_labs E1 subset, verify_refs --offline. Mutants: none (no project grader in this slice)."
    ),
}
out = ROOT / "ledgers/E1/E1-b.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "non-PASS", [r["id"] for r in non_pass])
