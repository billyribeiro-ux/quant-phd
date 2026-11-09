"""Round-5 slice-a fragment builder: carries round-4 PASS rows with a prefix, replaces re-verified rows.

Usage: python3 -I build_fragment_a_r5.py <checkout-root> <base-fragment.json>
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
base = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
S = "ledgers/M2/scripts/M2-a-r5/"
OUT = {"l01": "course/modules/M/M2/L01.html"}

P_FILE = ("Carried from round 4 ({f} byte-identical since the previous pin edbb7aa8; "
          "git diff --stat edbb7aa8..dde0486b does not list it): ")
P_RANGE = ("Carried from round 4 (cited lines {r} of {f} byte-identical since the previous pin edbb7aa8; "
           "no hunk of git diff -U0 edbb7aa8..dde0486b touches them, hunks are at index.html 71 and 130, "
           "L02.html 51, L03.html 218, L05.html 94/307/309, L06.html 64): ")

carry_file = {
    "M2a-R1-L01-MATH-01": "course/modules/M/M2/L01.html", "M2a-R1-L01-MATH-02": "course/modules/M/M2/L01.html",
    "M2a-R1-L01-LAB-01": "course/modules/M/M2/L01.html", "M2a-R1-L01-GRADE-01": "course/modules/M/M2/L01.html",
    "M2a-R1-L01-PROSE-01": "course/modules/M/M2/L01.html", "M2a-R4-L01-PROSE-02": "course/modules/M/M2/L01.html",
    "M2a-R1-L01-QUIZ-01": "course/modules/M/M2/L01.html", "M2a-R1-L01-CARD-02": "course/modules/M/M2/L01.html",
    "M2a-R1-L04-MATH-01": "course/modules/M/M2/L04.html", "M2a-R1-L04-MATH-02": "course/modules/M/M2/L04.html",
    "M2a-R1-L04-LAB-01": "course/modules/M/M2/L04.html", "M2a-R1-L04-QUIZ-01": "course/modules/M/M2/L04.html",
}
carry_range = {
    "M2a-R1-H04": ("index.html", "133-135"), "M2a-R1-H05": ("index.html", "61-65"),
    "M2a-R1-H06": ("index.html", "80, 89, 98, 107"), "M2a-R1-H07": ("course/modules/M/M2/L04.html", "156"),
    "M2a-R3-H09": ("index.html", "164"), "M2a-R1-X05": ("L01-L06.html", "quiz blocks 341-411, 335-408, 330-395, 298-368, 345-414, 332-406"),
    "M2a-R1-X-GRADE-01": ("course/modules/M/M2/L05.html", "338-339"),
    "M2a-R1-X-REF-01": ("index.html; L02.html 411-426; L03.html 397-412; L05.html 417-432; L06.html 408-423", "187-194 and References sections"),
    "M2a-R1-L02-MATH-01": ("course/modules/M/M2/L02.html", "55-176"),
    "M2a-R1-L02-MATH-02": ("course/modules/M/M2/L02.html", "178-333"),
    "M2a-R1-L02-LAB-01": ("course/modules/M/M2/L02.html", "76-152"),
    "M2a-R1-L02-PROSE-01": ("course/modules/M/M2/L02.html", "159-160"),
    "M2a-R1-L02-E-01": ("course/modules/M/M2/L02.html", "269-291"),
    "M2a-R1-L02-QUIZ-01": ("course/modules/M/M2/L02.html", "335-408"),
    "M2a-R1-L03-MATH-01": ("course/modules/M/M2/L03.html", "53-108"),
    "M2a-R1-L03-MATH-02": ("course/modules/M/M2/L03.html", "87-206"),
    "M2a-R1-L03-PROSE-01": ("course/modules/M/M2/L03.html", "210 and 278-284"),
    "M2a-R1-L03-LAB-01": ("course/modules/M/M2/L03.html", "112-173"),
    "M2a-R1-L03-QUIZ-01": ("course/modules/M/M2/L03.html", "330-395"),
    "M2a-R1-L05-MATH-01": ("course/modules/M/M2/L05.html", "53-89, 175-187"),
    "M2a-R1-L05-LAB-01": ("course/modules/M/M2/L05.html", "97-173"),
    "M2a-R1-L05-PROSE-01": ("course/modules/M/M2/L05.html", "218-219"),
    "M2a-R1-L05-QUIZ-01": ("course/modules/M/M2/L05.html", "345-414"),
    "M2a-R1-L06-MATH-02": ("course/modules/M/M2/L06.html", "182-208"),
    "M2a-R1-L06-MATH-03": ("course/modules/M/M2/L06.html", "210-330"),
    "M2a-R1-L06-LAB-01": ("course/modules/M/M2/L06.html", "113-180"),
    "M2a-R1-L06-ASSUME-01": ("course/modules/M/M2/L06.html", "71-73, 77-78, 86-88, 102-103, 111, 115, 277, 324-326"),
    "M2a-R1-L06-QUIZ-01": ("course/modules/M/M2/L06.html", "332-406"),
    "M2a-R1-L03-CARD-01": ("course/modules/M/M2/cards.json", "L03 cards c027-c039, c392 (none in the hunk list)"),
    "M2a-R1-L02-CARD-01": ("course/modules/M/M2/cards.json", "L02 cards c014-c026 (none in the hunk list)"),
}

re_verified = {}
re_verified["M2a-R1-H01"] = (
    "2.9 hub sections (index.html:1-199). Re-verified at dde0486b: ledgers/M2/scripts/M2-a-r5/checks_r5.out shows 7 objective "
    "items in lines 40-60, 4 ladder rung titles, placement block with 8 items (2 data-skill, data-mastery 0.8, 8 explain blocks), "
    "and 24 distinct L-page links. The only hunks in index.html are lines 71 and 130 (re-verified in M2a-R1-H03, M2a-R1-X04, "
    "M2a-R3-H08, M2a-R4-H08b). check_pages M2 PASS (G01).")
re_verified["M2a-R1-H02"] = (
    "2.9 hours. checks_r5.out: index.html data-hours-lessons=240 and data-hours-project=60; project.html:33 data-hours-project=60 "
    "(unchanged line; project hunk is line 121); all 24 lesson pages data-hours=10. 240 + 60 = 300 = curriculum M2 hours; "
    "60/300 = 1/5 = 20 percent, inside 10-40 percent.")
re_verified["M2a-R1-H03"] = (
    "2.9 placement arithmetic (index.html:71, changed this round: the parenthetical 'the four-rung ladder is defined under The project "
    "ladder, below' is added). The heading 'The project ladder' exists at index.html:172 and lists four rungs (lines 174-179). "
    "Eight items: 0.8 x 8 = 6.4, so at least 7 correct; 6/8 = 75 percent, 7/8 = 87.5 percent (checks_r5.out). Numbers unchanged and correct.")
re_verified["M2a-R3-H08"] = (
    "2.9 and 5.1. Items at index.html:127 (data-answer 12.02, labelled rung 2) and 133 (data-answer 3.01, labelled rung 1) are unchanged. "
    "Exact arithmetic (checks_r5.out): second difference of x^4 at 1 with h = 0.1 is 601/50 = 12.02 = 12 + 2h^2; "
    "central difference of x^3 is 301/100 = 3 + h^2. Rung labels match project.html:44-45 (rung 1 worked example, rung 2 completion with "
    "the second difference blanked) and project.html:121. BUILDER_RULES 5.1 requires at least two data-skill items testing rung 1-2 skills: "
    "met (lines 127 and 133). The explanation at line 130 was rewritten this round; its content claim is judged in M2a-R4-H08b, which FAILS.")
re_verified["M2a-R4-H08b"] = (
    "FAIL (persists). index.html:130 (explain block of the rung 2 skill check) now reads: 'The rung 2 completion problem asks for this second "
    "difference. Lesson 13 writes out the expansions of f(x + h) and f(x - h) with their remainders, and adding them and subtracting 2f(x) "
    "leaves h^2 f''(x) plus remainder terms.' Lesson 13 writes the two expansions (course/modules/M/M2/L13.html:91-92) but does not add them "
    "or subtract 2f(x): L13.html:93 says 'Subtract the second from the first' and cancels the f(x) and f''(x) terms to get the central first "
    "difference. A search of L13.html for '2f(x)', 'f(x + h) + f(x - h)' and 'second difference' finds no such computation. The project page "
    "says the opposite about Lesson 13: project.html:121 reads 'Lesson 13 writes them and subtracts them for the first difference; here they "
    "are added'. The arithmetic in the item (12.02) and the algebra (sum minus 2f(x) = h^2 f''(x) plus remainder) are correct; the claim that "
    "Lesson 13 contains that sum is false.")
fail_fix = ("Replace the second sentence of index.html:130 with: 'Lesson 13 writes out the expansions of f(x + h) and f(x - h) with their "
            "remainders (L13.html:91-92) and subtracts them for the first difference (L13.html:93). Adding them, as the rung 2 problem does "
            "(project.html:121), gives 2f(x) + h^2 f''(x) plus remainder terms; subtracting 2f(x) leaves h^2 f''(x) plus remainder terms.' "
            "Or add that sum to Lesson 13 and keep the sentence. Then re-run check_pages --unit M2 and page_smoke for index.")
re_verified["M2a-R1-X01"] = (
    "2.9 banned phrases, process words, scope words (ledgers/M2/scripts/M2-a-r5/prose_scan_a_r5.out, re-run on index.html and L01-L06). "
    "The changed sentences were read: index.html:71 and 130, L02.html:51 ('in §3'), L03.html:218 ('Any smaller positive delta also "
    "works'), L05.html:94 and 307-309, L06.html:64 ('Shrinking delta if necessary ... because I is open'). None contains a banned phrase or "
    "a process word. The 'fixed'/'grader' hits are ordinary prose (checked in context in round 4; unchanged lines). No new scope word is unsupported.")
re_verified["M2a-R1-X02"] = (
    "2.7 slice cards. ledgers/M2/scripts/M2-a-r5/card_numbers_a_r5.out: 82 slice cards (L01 16, L02 13, L03 14, L04 11, L05 13, L06 15), "
    "0 number tokens missing from their lesson. Changed slice cards re-read against the current lesson text: M2-c009 (L01) back "
    "'2 = |1 - (-1)| <= |1 - L| + |L - (-1)| < 2' equals L01.html Example 4.1 text (L01.html:173-189); M2-c048 (L04) matches Example 3.1 "
    "and Misconception 1 (L04.html:144-165, and the misconception block at 163-165); M2-c068 (L06) matches Misconception 2 (L06.html:201, "
    "a direct proof with no assumption) and Corollary 3.1 (ii) (L06.html:103, 111). Cards with no grade key: 22 in the slice (pre-existing card "
    "style, note).")
re_verified["M2a-R1-X03"] = (
    "3 notation (ledgers/M2/scripts/M2-a-r5/macros_slice_a_r5.out). Every macro in index.html and L01-L06 is standard KaTeX or registered; "
    "no \\mathbb is used in the slice. The new Greek letters in L05.html:307-309 (alpha, beta, gamma) are conventionally local per the "
    "notation.json 'about' field ('alpha, beta, gamma ... are defined in each lesson where used'), and L05.html:307 defines them in the "
    "problem statement. Registered \\gamma_3 and \\gamma_4 (notation.json symbols, M4) are not used in M2. delta is not registered in "
    "notation.json (grep: no delta entry). Note (LOW, not a FAIL kind): in L05 delta now also denotes a constant coefficient (L05.html:307, "
    "309) in the same lesson where delta is the epsilon-delta threshold (L05.html:62, 64, 76, 186). eta at L05.html:186 is a local threshold. "
    "The Q(h) glyph and the registry \\mathbb{Q} remain distinct (round-4 note).")
re_verified["M2a-R1-X04"] = (
    "2.2 placement quiz structure (index.html:69-137). checks_r5.out: 8 items, 2 with data-skill, data-mastery 0.8, 8 explain blocks. "
    "Numeric keys recomputed exactly: 12.02 (601/50) and 3.01 (301/100). The placement intro text changed (line 71) but the item count and "
    "the mastery arithmetic did not.")
re_verified["M2a-R1-X-DEP-01"] = (
    "2.9 and 14 DAG. check_dag M2 PASS (G02). Ordering scan of the changed sentences: L02.html:51 (why-it-matters) points forward to Remark 3.1 in §3 "
    "(L02.html:178-186), a same-lesson pointer in the preview paragraph, not a use of an undefined term; "
    "L06.html:64 uses the open interval I of L06.html:55 (defined before Proposition 1.1); index.html:71 points to the hub's own section "
    "'The project ladder' (index.html:172). L05.html:94 now names 'Lesson 7, §1' for higher derivatives without a link (L07.html:54 is "
    "'Higher derivatives'): a forward reference in prose only. plans/M2-build-plan.md:101 requires that no lesson link a later definition, "
    "which holds; the named forward pointer is recorded as a LOW note (ruling 26), not a FAIL. L04.html:156 forward pointer to Lesson 13 unchanged (note).")
re_verified["M2a-R1-X-HRS-01"] = (
    "4.2 why-it-matters word counts (checks_r5.out, counted by checks_r5.py): L01 91, L02 87 (the change adds the two words 'in §3'), "
    "L03 96, L04 72, L05 93, L06 84. All at most 120 (BUILDER_RULES 4.2). Section order unchanged. data-hours=10 on each page (checks_r5.out).")
re_verified["M2a-R1-X-CARD-IDS"] = (
    "2.7 card ids and fronts (checks_r5.out): 396 cards in cards.json (was 394; M2-c422 L07 and M2-c423 L09 appended this delta), "
    "no duplicate id and no duplicate front. Within the slice, near-duplicates are kept as LOW notes: M2-c010/c013; M2-c044/c048/c049 "
    "(|x| at 0; c048 front changed this delta); M2-c063/c071; M2-c017/c018. M2-c422 (L07) and M2-c423 (L09) are outside this slice; "
    "M2-c423 restates a topic that M2-c129 (L09, rewritten this delta) also covers and is for slice d/e to check.")
re_verified["M2a-R1-L01-CARD-01"] = (
    "2.7 cards of L01: 16 cards (checks_r5.out counts: L01 16). M2-c009 changed this delta and is re-verified: its back equals "
    "L01.html:173-189 (Example 4.1 triangle-inequality chain). The other 15 L01 cards are byte-identical and their lesson text is unchanged.")
re_verified["M2a-R1-L02-PROSE-02"] = (
    "4.2 why-it-matters (course/modules/M/M2/L02.html:51, changed). The added phrase '(Remark 3.1, in §3)' is correct: Remark 3.1 is the "
    "block 'Remark 3.1 (the quotient needs a limit away from zero)' at L02.html:181 under the section heading '3 Quotients and the nonzero "
    "hypothesis' (L02.html:178). Remark 3.1 gives a_n = 1, b_n = 1/n, so a_n/b_n = n diverges (L02.html:185, 202). 87 words, at most 120.")
re_verified["M2a-R1-L03-MATH-03"] = (
    "2.4 problem set (L03.html:208-328, changed at line 218). M1 (L03.html:215-218): f(x) = 2x - 1, a = 3, L = 5 (f(3) = 5), epsilon = 0.02. "
    "|f(x) - 5| = |2x - 6| = 2|x - 3| < 0.02 iff |x - 3| < 0.01, so delta = 0.01 works (strict inequality; any x with |x - 3| < 0.01 gives "
    "2|x - 3| < 0.02). 'Any smaller positive delta also works' is true, since any x with |x - 3| < delta' <= 0.01 gives 2|x - 3| < 0.02. The edit "
    "removed a redundant sentence and is correct. Other problems in 208-328 are byte-identical and were verified in round 4 (carried in the "
    "same subject range, no hunk).")
re_verified["M2a-R1-L04-CARD-01"] = (
    "2.7 cards about |x| and the quotient (cards.json). M2-c048 changed this delta and is re-verified: 'The formula f(x) = |x| has no "
    "derivative at 0, because its one-sided difference quotients have different limits there (Example 3.1, Misconception 1)'. "
    "L04.html:144-165 gives Example 3.1 (f = |x|, one-sided quotients differ) and the first misconception block (L04.html:163-165, "
    "'Every function given by a formula has a derivative at every point'), so the cross-reference is correct. M2-c044, c049 and c050 are "
    "byte-identical cards whose lesson subjects are unchanged; their round-4 evidence is carried.")
re_verified["M2a-R1-L04-CARD-02"] = (
    "2.7 cards of L04: 11 cards (c040-c050; checks_r5.out lesson count 11). M2-c048 re-verified as above; the other ten are byte-identical "
    "and carried from round 4.")
re_verified["M2a-R1-L05-MATH-02"] = (
    "2.4 Assumption 1.4 (L05.html:91-95, changed at line 94). The wording changed from a link to 'higher derivatives are defined in Lesson 7, "
    "§1'. The assumed expansion (f(x+h) - f(x-h))/(2h) = f'(x) + h^2 f'''(x)/6 + o(h^2) is the standard central-difference expansion for f with "
    "f''' at x; it is labelled 'assumed here and not proved' and every use begins with 'Assuming Assumption 1.4' (L05.html:99, 105, 282, 284). "
    "Lesson 7 §1 is 'Higher derivatives' (L07.html:54), so the pointer is accurate. Named, not linked: LOW forward-reference note (ruling 26).")
re_verified["M2a-R1-L05-MATH-03"] = (
    "2.4 problem set and key rows of L05 (L05.html:224-343, changed at lines 307 and 309). R1 (L05.html:307-309) now uses alpha, beta, gamma, "
    "delta: p(x) = alpha x^3 + beta x^2 + gamma x + delta; central difference equals p'(x) + alpha h^2. Recomputed: linear term gives gamma "
    "(exactly), quadratic gives 2 beta x, cubic gives alpha(3x^2 + h^2), constant cancels; sum = 3 alpha x^2 + 2 beta x + gamma + alpha h^2 = "
    "p'(x) + alpha h^2 (exact, for every x and h != 0). The solution text matches the statement. Key rows 338-339 unchanged (carried).")
re_verified["M2a-R1-L05-CARD-01"] = (
    "2.7 cards of L05 (13 cards: c051-c061, c379, c393). M2-c393 ('What does Assumption 1.4 state...') back: 'For f with a third derivative "
    "near x, (f(x + h) - f(x - h))/(2h) = f'(x) + h^2 f'''(x)/6 + o(h^2) as h tends to 0. It is assumed and not proved.' matches "
    "L05.html:94 after this delta. M2-c058 (grade C) matches the Lab 1 output line 'composite c, 95.062500000, 95.062500855, 8.55e-07' "
    "(L05.html:171). Cards without a grade key in L05: c379, c393 (card style, LOW note; unchanged).")
re_verified["M2a-R1-L06-MATH-01"] = (
    "2.4 Proposition 1.1 and its proof (L06.html:55-109, changed at line 64). Hypotheses: f defined on an open interval I, c in I, f differentiable "
    "at c, local extremum at c (L06.html:55-62). The changed proof adds 'Shrinking delta if necessary, we may assume (c - delta, c + delta) "
    "subset I, which is possible because I is open'. This is the missing step (the inclusion needed for the one-sided inequalities of the "
    "numerator) and it is correct. The rest of the proof (Q(h) <= 0 on the right, >= 0 on the left, Q(h) -> f'(c), contradiction with f'(c)/2) "
    "is correct. Corollary, Theorems and Misconceptions unchanged.")
re_verified["M2a-R1-L06-CARD-01"] = (
    "2.7 cards of L06 (15 cards: M2-c062 to c074, c394, c414; checks_r5.out). M2-c068 changed this delta and is re-verified: "
    "'f(x) = x^3 is strictly increasing on the real line, a fact proved directly with no assumption, yet f'(0) = 0. Corollary 3.1 (ii) gives "
    "only a sufficient condition, and it applies under Assumption 2.1' matches L06.html:200-201 (direct proof: y^3 - x^3 = (y - x)(y^2 + xy + x^2), "
    "with y^2 + xy + x^2 = (x + y/2)^2 + 3y^2/4 > 0 for x < y) and L06.html:103, 111. The other 14 L06 cards are byte-identical and carried from round 4.")

gates = {
    "M2a-R1-G01": "Re-run at dde0486b: ledgers/M2/scripts/M2-a-r5/g01_check_pages.out = 'check_pages M2: PASS', EXIT 0.",
    "M2a-R1-G02": "Re-run: g02_check_dag.out = 'check_dag M2: PASS', EXIT 0.",
    "M2a-R1-G03": "Re-run: g03_run_labs.out = 'run_labs M2: PASS (27/27)', EXIT 0.",
    "M2a-R1-G04": "Re-run with python -I -W error from an empty temporary directory (ledgers/M2/scripts/M2-a-r5/lab_slice_a_r5.py, output g04_twins_isolated.out): L01..L06 each exit 0, stderr 0 bytes, stdout equal to the page expected block, page code equal to the twin; 'ALL PASS', EXIT 0. The six twins are byte-identical to the round-4 pin (git diff lists only lab-M2-L07-1.py).",
    "M2a-R1-G05": "Re-run: g05_pytest_labs.out = six dots, EXIT 0 (tests/test_labs.py -k 'M2 and (L01 or ... or L06)').",
    "M2a-R1-G06": "Re-run: g08_page_smoke.out 'page_smoke M2: PASS', EXIT 0 (index, L01-L06, --skip-sweep).",
    "M2a-R1-G07": "Re-run: g06_ruff.out 'All checks passed!', '6 files already formatted'; g07_mypy.out 'Success: no issues found in 6 source files'; EXIT 0 both.",
    "M2a-R1-G08": "Re-run: g10_verify_refs_offline.out 'offline integrity: 560 entries, 0 problems'; g11_verify_refs_live_M2.out 'live re-verification of M2: 2 of 560 entries, 0 problems'; EXIT 0 both. references/ and tools/ unchanged in the delta.",
    "M2a-R1-G09": "Re-run: g09_check_projects.out 'check_projects M2: PASS', EXIT 0 (unit level; slice a has no project rows).",
}

new_rows = []
for row in base["rows"]:
    rid = row["id"]
    if rid in gates:
        r = dict(row)
        r["status"] = "PASS"
        r["evidence"] = gates[rid]
    elif rid in re_verified:
        r = dict(row)
        r["evidence"] = re_verified[rid]
        if rid == "M2a-R4-H08b":
            r["status"] = "FAIL"
            r["fix"] = fail_fix
        else:
            r["status"] = "PASS"
    elif rid in carry_file:
        r = dict(row)
        r["evidence"] = P_FILE.format(f=carry_file[rid]) + row["evidence"]
    elif rid in carry_range:
        f, rng = carry_range[rid]
        r = dict(row)
        r["evidence"] = P_RANGE.format(r=rng, f=f) + row["evidence"]
    else:
        raise SystemExit(f"row {rid} not classified")
    if rid == "M2a-R1-X-CARD-IDS":
        r["evidence"] = r["evidence"]
    new_rows.append(r)

ids = [r["id"] for r in new_rows]
assert len(ids) == len(set(ids)) == len(base["rows"]), "row ids must be kept and unique"
statuses = [r["status"] for r in new_rows]
n_pass = statuses.count("PASS")
n_fail = statuses.count("FAIL")
fragment = {
    "unit": "M2",
    "slice": "a",
    "round": 5,
    "verifier": "independent verifier (Haiku 5.5), unit M2 slice a, round 5 (delta verification, ruling 26 amended)",
    "pin": "dde0486b (detached checkout HEAD)",
    "base": ("Round-4 fragment /Users/billyribeiro/.fanout/frags/S-M2-a.round4.json (verified in full at pin edbb7aa8). "
             "Delta edbb7aa8..dde0486b over the slice: index.html 71 and 130; L02.html 51; L03.html 218; L05.html 94, 307, 309; "
             "L06.html 64; cards.json (slice cards c009, c048, c068; new M2-c422 L07 and M2-c423 L09 outside the slice; c085, c129, "
             "c137, c293 outside the slice). project.html 121 (outside the slice) is cited by M2a-R4-H08b. L01.html, L04.html, the twins "
             "of L01-L06 and tests/labs/M2/lab-M2-L0[1-6]-1.py are byte-identical to edbb7aa8. tools/, references/, curriculum/, notation/, "
             "BUILDER_RULES.md, VERIFIER_RULES.md and M1 pages are unchanged in the delta. Every round-4 row id is kept."),
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS5-M2-a",
    "scratch": "ledgers/M2/scripts/M2-a-r5/",
    "verified_at": "2026-11-09",
    "verdict": "FAIL" if n_fail else "PASS",
    "rows": new_rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice a is not a project slice: no grader, no mutants (ruling 26 and verifier rules section on project slices). mutants is empty by design.",
        "LOW (not FAIL kinds under ruling 26), recorded for plans/KNOWN-ISSUES.md if the owner wants them: (1) L05.html:94 names 'Lesson 7, §1' without a link (forward reference in prose); (2) L05.html:307-309 reuses delta as a constant coefficient in the same lesson where delta is the epsilon-delta threshold (L05.html:62, 64, 76, 186); rename the constant to a symbol used nowhere else in M2; (3) 22 slice cards have no grade key (card style; e.g. M2-c393, M2-c379); 78 cards unit-wide; (4) near-duplicate slice cards M2-c010/c013, c044/c048/c049, c063/c071, c017/c018; (5) L04.html:156 forward pointer to Lesson 13 (unchanged since round 3).",
        "Outside this slice, seen only through the cards and hunks, for the owners of slices b-e: M2-c085 (L07) changed from C to T and M2-c422 (L07, C) now carries the printed-decimal check of the same error; M2-c423 (L09, C) restates a Riemann-sum topic that M2-c129 (L09, rewritten) also covers; the L07 twin lab-M2-L07-1.py and project.html changed in the delta.",
        "plans/FINAL-ARCHITECT-RULINGS.md gained rulings 27-29 (E3 only) and plans/KNOWN-ISSUES.md is new (E3 only); ruling 26 text is unchanged in the delta.",
        "Not checked: lessons and cards outside the slice (L07-L24, project.html grader, other twins); live verify_refs covers only the 2 M2 entries it re-checks (as in round 4); no browser screenshot of the hub (page_smoke PASS only).",
    ],
    "summary": (f"M2 slice a, round 5 (delta verification). {len(new_rows)} rows: {n_pass} PASS, {n_fail} FAIL, 0 UNVERIFIABLE. "
                "The FAIL is M2a-R4-H08b, index.html:130: the explanation still says Lesson 13 adds the two expansions and subtracts 2f(x); "
                "L13.html:93 subtracts them and project.html:121 says 'here they are added'. Gates re-run at dde0486b: all PASS "
                "(check_pages, check_dag, run_labs 27/27, twins isolated, pytest 6, ruff, mypy, page_smoke, check_projects, verify_refs offline and live)."),
}
out = root / "ledgers/M2/M2-a.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(new_rows), "PASS", n_pass, "FAIL", n_fail)
