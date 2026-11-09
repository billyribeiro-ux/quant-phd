"""Round-7 delta fragment for M2 slice a (pin aa659725). Builds ledgers/M2/M2-a.json from the round-6 base rows."""
import json
import sys

ROOT = sys.argv[1].rstrip('/')
base = json.load(open('/Users/billyribeiro/.fanout/frags/S-M2-a.round6.json', encoding='utf-8'))
base_rows = {r['id']: r for r in base['rows']}

PREF_IDX = ("Carried from round 6 (course/modules/M/M2/index.html, project.html and L13.html byte-identical since the "
            "previous pin e896b7a4; git diff e896b7a4..aa659725 over course/modules/M/M2 lists only L04.html, L05.html "
            "and cards.json):")
PREF_L01 = "Carried from round 6 (course/modules/M/M2/L01.html and tests/labs/M2/lab-M2-L01-1.py byte-identical since e896b7a4):"
PREF_L02 = "Carried from round 6 (course/modules/M/M2/L02.html and tests/labs/M2/lab-M2-L02-1.py byte-identical since e896b7a4):"
PREF_L03 = "Carried from round 6 (course/modules/M/M2/L03.html and tests/labs/M2/lab-M2-L03-1.py byte-identical since e896b7a4):"
PREF_L06 = "Carried from round 6 (course/modules/M/M2/L06.html and tests/labs/M2/lab-M2-L06-1.py byte-identical since e896b7a4):"
PREF_L04L = ("Carried from round 6 (cited lines of course/modules/M/M2/L04.html byte-identical since e896b7a4: the only L04 "
             "hunks are 1-for-1 replacements at lines 51, 202 and 263, none inside the cited range):")
PREF_L05S = ("Carried from round 6 (cited L05 content byte-identical since e896b7a4: the only L05 change is a 2-line insertion "
             "after old line 91 and old line 94 rewritten as new line 96; old line n is new line n+2 for n >= 92, verified by "
             "diff of the two files. Line numbers below are the e896b7a4 numbers):")
PREF_CARDS = ("Carried from round 6 (cited cards byte-identical since e896b7a4, verified per id by "
              "ledgers/M2/scripts/M2-a-r7/cards_delta_r7.out):")
PREF_H07 = ("Carried from round 6 (cited lines byte-identical since e896b7a4: course/modules/M/M2/L04.html:156 lies outside "
            "all three L04 hunks, and L13.html and index.html are unchanged):")

def carry(rid, pref):
    r = base_rows[rid]
    return {'id': rid, 'check': r['check'], 'location': r['location'], 'status': 'PASS',
            'evidence': pref + ' ' + r['evidence']}

over = {}

# ---- gates: re-run at aa659725 ----
over['M2a-R1-G01'] = ('check_pages --unit M2', 'tools/check_pages.py --unit M2', 'PASS',
    'Re-run at aa659725: ledgers/M2/scripts/M2-a-r7/g01_check_pages.out = "check_pages M2: PASS", EXIT 0.')
over['M2a-R1-G02'] = ('2.9 DAG gate: check_dag --unit M2', 'tools/check_dag.py --unit M2', 'PASS',
    'Re-run: g02_check_dag.out = "check_dag M2: PASS", EXIT 0. check_dag checks concept links only (plans/M2-build-plan.md:331), '
    'so it would not detect the plain link to Lesson 7 that round 6 flagged (M2a-R1-X-DEP-01); that link is now removed (see X-DEP-01).')
over['M2a-R1-G03'] = ('2.5 labs: run_labs --unit M2', 'tools/run_labs.py --unit M2', 'PASS',
    'Re-run: g03_run_labs.out = "run_labs M2: PASS (27/27)", EXIT 0.')
over['M2a-R1-G04'] = ('2.5 twins alone under python -I -W error; page code equals twin; expected block equals output',
    'tests/labs/M2/lab-M2-L01-1.py .. lab-M2-L06-1.py; course/modules/M/M2/L01.html .. L06.html', 'PASS',
    'Re-run: g04_twin_L01.out .. g04_twin_L06.out, each EXIT 0 with the expected values printed. twin_compare_r7.py (run on aa659725) '
    'prints "L0n code==twin True expected==stdout True exit 0 stderr_bytes 0" for n = 1..6 (twin_compare_r7.out). The round-6 '
    'comparison script had a hard-coded path to another checkout, so a parameterised copy was used.')
over['M2a-R1-G05'] = ('2.5 test_labs for the six M2 twins', "tests/test_labs.py -k 'M2 and (L01 or L02 or L03 or L04 or L05 or L06)'", 'PASS',
    'Re-run: g05_pytest_labs.out shows six passing tests and EXIT 0.')
over['M2a-R1-G06'] = ('2.9 page_smoke for the slice pages', 'tools/page_smoke.py --unit M2 --pages index L01 L02 L03 L04 L05 L06 --skip-sweep', 'PASS',
    'Re-run: g06_page_smoke.out = "page_smoke M2: PASS" with PASS lines for index.html and L01..L06, EXIT 0.')
over['M2a-R1-G07'] = ('ruff, ruff format, mypy --no-incremental on the six slice twins', 'tests/labs/M2/lab-M2-L0[1-6]-1.py', 'PASS',
    'Re-run: g07_ruff_check.out "All checks passed!"; g07_ruff_format.out "27 files already formatted"; g07_mypy.out '
    '"Success: no issues found in 6 source files"; all EXIT 0.')
over['M2a-R1-G08'] = ('2.9 verify_refs offline and unit M2', 'tools/verify_refs.py --offline; tools/verify_refs.py --unit M2', 'PASS',
    'Re-run: g08_verify_refs_offline.out "offline integrity: 560 entries, 0 problems", EXIT 0; g08_verify_refs_unit_M2.out '
    '"live re-verification of M2: 2 of 560 entries, 0 problems", EXIT 0 (the tool\'s own live check; no bot check or access block touched).')
over['M2a-R1-G09'] = ('2.9 check_projects --unit M2', 'tools/check_projects.py --unit M2', 'PASS',
    'Re-run: g09_check_projects.out = "check_projects M2: PASS", EXIT 0.')
over['M2a-R6-G10'] = ('build_site --check and tests/test_build_site.py', 'tools/build_site.py --check; tests/test_build_site.py', 'PASS',
    'Re-run: g10_build_site_check.out = "site data current: 6 outputs", EXIT 0; g10_pytest_build_site.out shows 31 passing tests, EXIT 0.')

# ---- X01, X03: prose and math of index and L01-L06 (subject includes the changed L04 and L05 text) ----
over['M2a-R1-X01'] = ('visible prose of index.html and L01-L06 (rule 2, rule 4 scope words, process words)',
    'index.html and L01-L06.html visible prose', 'PASS',
    'Re-verified for the changed text: ledgers/M2/scripts/M2-a-r7/prose_scan_r7.out (round-6 scanner on aa659725) shows no new '
    'banned hit in L04 or L05. The changed sentences are L04.html:51 ("defines it precisely"), L04.html:199-202 (M3 solution), '
    'L04.html:260-263 (R1 solution), and L05.html:92-93 (definitions of f\'\' and f\'\'\'), all plain prose. The scope words added '
    '("every point of an open interval containing x", L05.html:92) are definitional hypotheses. Remaining scanner hits are '
    'carried from round 6 in unchanged text (index "held fixed", "grader"; L01 "fixed numbers"; L06 "fixed sign").')
over['M2a-R1-X03'] = ('math of index and L01-L06 (rule 1 and rule 13 notation)', 'index.html and L01-L06.html math', 'PASS',
    'Re-verified for the changed math: L04 M3 (L04.html:199-202) and R1 (L04.html:260-263) re-derived exactly '
    '(ledgers/M2/scripts/M2-a-r7/l05_l04_exact_r7.out: Q(h)+1/4 = h/(4(2+h)), |Q+1/4| < |h|/4 for |h|<1, Q(h)=|h| for x|x|). '
    'The L05 definitions (L05.html:92) use the notation f\'\', f\'\'\' of L07.html:59 with the same values. L05 numbers at L05.html:221, '
    '286 re-derived exactly: p\'(1.5)=32.0625, q\'(1.5)=29/49, c\'(1.5)=95.0625, p\'\'\'(1.5)=141, h^2 p\'\'\'/6 = 2.35e-07, and the '
    'exact central-difference errors 2.350000001e-07, 3.33e-10, 8.55e-07 (same script). Notation: grep of notation/notation.json finds no entry for f\'\' or f\'\'\' '
    '(no registered meaning to conflict with), and no other meaning of these symbols occurs in L01-L06.')
over['M2a-R1-X02'] = ('2.7 cards: ids, structure, numbers, duplicates, agreement with lesson text (slice cards)',
    'course/modules/M/M2/cards.json:451 (M2-c064); course/modules/M/M2/L06.html:73 and 326 (key-results row); L06.html:325', 'FAIL',
    'Re-verified from scratch. Structure and numbers PASS: cards.json has 393 cards, 0 duplicate ids, 0 duplicate fronts (ledgers/M2/scripts/M2-a-r7/cards_struct_r7.out); '
    'the id-level diff against e896b7a4 changes slice cards M2-c013, c044, c064, c394, c414 and removes M2-c048 (cards_delta_r7.out); '
    'cards_check.py (round-6 script at aa659725) flags only the Section/Misconception tokens already checked by hand, and the changed cards '
    'were checked by hand: c013 vs L01.html:196 (Section 5 bullet, lines 192-201); c044 vs L04.html Misconception 1 and Example 3.1; c414 vs '
    'L06.html:55 (critical point defined in Section 1); c394 vs L06.html:307 (Lipschitz named in prose in R3). '
    'FAIL on the scope of M2-c064 (cards.json:451: "In Lesson 6, every result that uses it begins its statement with \\"Assuming Assumption 2.1\\""): '
    'the Lesson 6 results that use Assumption 2.1 are Theorem 2.2 (L06.html:77-78), Theorem 2.3 (L06.html:87-88), Corollary 3.1 (L06.html:102-103) '
    'and key-results rows L06.html:322-324, and each begins "Assuming Assumption 2.1". But key-results row L06.html:326 (grade C: "For x^3 - 3x, 8 of the 16 grid '
    'intervals on [-2, 2] increase, and f(-1) = 2, f(1) = -2") has as its source "the monotone intervals follow from the derivative on the page, '
    'assuming Assumption 2.1 (Corollary 3.1)" and does not begin with the required phrase. L06.html:73 says "Every result below that uses it begins '
    'its statement with ...", which L06.html:326 contradicts; L06.html:325 says "every result in §2 and §3". The round-6 counterexamples '
    'in L10-L12 are outside "In Lesson 6" and no longer apply. Defect of ruling 26 kind (false scope statement; missing hypothesis in a result).',
    'Either (a) narrow the rule to the scope the page already states: L06.html:73 "Every result in Sections 2 and 3 that uses it begins ..." and '
    'cards.json:451 "In Sections 2 and 3 of Lesson 6, every result that uses it begins its statement with ..."; or (b) rewrite L06.html:326 so that its '
    'statement begins "Assuming Assumption 2.1," (split the Lab 1 count from the monotone claim). Then re-run check_pages, check_dag, build_site --check, '
    'and delta-verify.')
over['M2a-R1-X-CARD-IDS'] = ('2.7 cards: ids, duplicate facts across the unit', 'course/modules/M/M2/cards.json (393 cards)', 'PASS',
    'Re-verified at aa659725: cards_struct_r7.out: 393 cards, 0 duplicate ids, 0 duplicate fronts. Removed in the delta: M2-c048 (slice, L04, the '
    'near-duplicate of M2-c044 on |x|; its content is covered by the new c044), and c129, c160, c208, c419 (outside slice). No new duplicate front. '
    'M2-c013 has lost its grade key (see notes). Near-duplicate notes from round 5 remain LOW notes.')
over['M2a-R1-X-DEP-01'] = ('2.9 and 14 DAG: no concept used before its definition; nothing defined twice in the slice',
    'course/modules/M/M2/L05.html:92-96 (definitions and Assumption 1.4); L05.html:101, 107, 221, 284, 286; L01.html-L04.html (no higher-derivative term)', 'PASS',
    'Re-verified: L05.html:92 now defines f\'\' (derivative of f\') and f\'\'\' (derivative of f\'\') before Assumption 1.4 at L05.html:95-96, which is the first '
    'use of f\'\'\'. The Lesson 7 link is removed: grep for "L07" or "Lesson 7" in L05.html returns nothing. grep for "second derivative", "third derivative", '
    '"higher derivative" and f\'\' over L01-L04 returns nothing (index.html:130 is the phrase "second difference", not a derivative). Uses of f\'\'\' '
    '(L05.html:221, 284, 286) come after the definition. check_dag PASS (g02). The round-6 DAG defect is therefore resolved. '
    'LOW, not ruling-26 kinds: (i) L07.html:59 (Definition 1.1, higher derivative) defines the same notations later; the values agree, and L05 '
    'uses a stronger hypothesis (f\' differentiable on an interval) than L07 (f^(k-1) exists on an interval and the derivative exists at x), so no contradiction; '
    '(ii) L05.html:38 "Introduces: no new concept" no longer lists the notations f\'\' and f\'\'\' that L05 now introduces (wording of the header only).')
over['M2a-R1-X-HRS-01'] = ('2.4 hours: headers and why-it-matters paragraphs of L01-L06', 'L01.html..L06.html headers and why-it-matters paragraphs', 'PASS',
    'Re-verified: git diff -U0 e896b7a4..aa659725 touches no header line of L01-L06; the only why-it-matters change is L04.html:51 ("defines it precisely" '
    'replaces "defines it exactly"). Its claims are supported by the lesson: Proposition 2.1 (L04.html:129, derivative implies continuity) and Example 3.1 '
    '(L04.html:144-150, |x| at 0). No hour figure changed in the slice; hub split rows H02/H03 carry.')
over['M2a-R1-X05'] = None  # carried below
over['M2a-R1-X-GRADE-01'] = None
over['M2a-R1-X-REF-01'] = None

# ---- L01 cards: subject changed (M2-c013) ----
over['M2a-R1-L01-CARD-01'] = ('2.7 cards of L01', 'course/modules/M/M2/cards.json (lesson L01: c001-c013, c376, c390, c391, c424)', 'PASS',
    'Re-verified at aa659725. M2-c013 changed: "Does Definition 2.1 produce a limit, or only check a proposed one?" / "It only checks a proposed L. It does '
    'not produce L. A method is to compute a candidate and then prove it, as Example 2.3 does with the candidate 2 (Section 5)." Checked against '
    'L01.html:196 (Section 5 "Where the canon breaks", bullet "Definition 2.1 tests a proposed L. It does not produce L. One method is to compute a candidate '
    'and then prove it, as Example 2.3 does with the candidate 2"); Example 2.3 has limit 2 (L01.html:81-89). The card has no grade key now (notes). '
    'M2-c002, c008, c390, c424 are byte-identical to e896b7a4 and were re-read this round: c002 vs Definition 2.1 (L01.html:60-62); c008 vs Proposition 3.1 '
    '(L01.html:157-159); c390 vs Section 3 (L01.html:152-154); c424 vs Definition 2.1 (convergent and divergent sentence, L01.html:62). The other L01 cards are byte-identical.')
over['M2a-R1-L01-CARD-02'] = None

# ---- L04 changed subjects ----
over['M2a-R1-L04-MATH-02'] = ('2.4 problem set, displayed chains and key rows of L04 (M3 proof and R1 wording changed)',
    'course/modules/M/M2/L04.html:199-202 (M3), 260-263 (R1), 178-296 (rest)', 'PASS',
    'Re-verified from scratch at aa659725. M3 (L04.html:199-202): f(x)=1/x, Q(h) = -1/(2(2+h)) (exact); Q(h)+1/4 = h/(4(2+h)) (exact, ledgers/M2/scripts/M2-a-r7/l05_l04_exact_r7.out); '
    'for |h|<1, |2+h|>1 so |Q(h)+1/4| < |h|/4; given eps>0, delta = min(1, 4 eps) gives |Q(h) - (-1/4)| < eps for 0<|h|<delta. f\'(2) = -1/4 is correct and the proof '
    'is complete with no gap. R1 (L04.html:260-263): x|x| has Q(h) = h|h|/h = |h| for h != 0 (exact check); delta = eps gives f\'(0)=0. The new sentence '
    '"the quotient here has the same limit from both sides, because the factor h cancels from the numerator and the denominator and leaves |h|, which tends to 0 from '
    'either side" is correct; it contrasts with |x| in Example 3.1 (L04.html:144-150, quotients +1 and -1). Other problems, P3 at line 227 and key row 292, are byte-identical '
    'to e896b7a4 (hunks at 51, 202, 263 only) and carried from round 6.')
over['M2a-R1-L04-CARD-01'] = ('2.7 cards of L04 about |x| and the quotient', 'course/modules/M/M2/cards.json (M2-c044, M2-c049, M2-c050; M2-c048 removed)', 'PASS',
    'Re-verified at aa659725. M2-c044 changed: front "Does f(x) = |x| have a derivative at 0, although it is given by one formula?", back "No. Q(h) = |h|/h equals 1 for h > 0 and '
    '-1 for h < 0, so the two-sided limit does not exist (Example 3.1). A formula does not guarantee a derivative at every point (Misconception 1)." Checked against L04.html:144-150 '
    '(Example 3.1) and the first item of L04.html section 5 (Misconception 1, "Every function given by a formula has a derivative at every point", answered by Example 3.1). Grade T is the '
    'proved fact in Example 3.1. M2-c048 (removed) was a duplicate of this card. M2-c049 and c050 are byte-identical and carried.')
over['M2a-R1-L04-CARD-02'] = ('2.7 cards of L04 (lesson L04 cards c040-c050)', 'course/modules/M/M2/cards.json (lesson L04 cards, M2-c048 removed, M2-c044 changed)', 'PASS',
    'Re-verified at aa659725: the L04 card set is the e896b7a4 set minus M2-c048 (cards_delta_r7.out) with M2-c044 rewritten (checked in M2a-R1-L04-CARD-01). The other L04 cards '
    '(c040, c041, c043, c049, c050) are byte-identical per id and carried from round 6 (ledgers/M2/scripts/M2-a-r7/cards_struct_r7.out lists the L04 no-grade cards c040, c041).')

# ---- L05 definitions: subject changed ----
over['M2a-R1-L05-MATH-02'] = ('2.4 Assumption 1.4 (central-difference expansion) and its uses; the new definitions of f\'\' and f\'\'\' (L05.html:92)',
    'course/modules/M/M2/L05.html:92-96; uses at L05.html:101, 107, 221, 284, 286', 'PASS',
    'Re-verified from scratch at aa659725. Definitions (L05.html:92): f\'\'(x) = (f\')\'(x) when f\' is differentiable on an open interval containing x; f\'\'\'(x) = (f\'\')\'(x) when f\'\' is differentiable on an open interval containing x. These agree with L07.html:59 (Definition 1.1) in value. '
    'Assumption 1.4 (L05.html:95-96) is labelled an assumption and "not proved". The displayed expansion (f(x+h)-f(x-h))/(2h) = f\'(x) + h^2 f\'\'\'(x)/6 + o(h^2) is the third-order Taylor expansion '
    'f(x+h)-f(x-h) = 2h f\'(x) + h^3 f\'\'\'(x)/3 + o(h^3) divided by 2h. Every use begins its statement with "Assuming Assumption 1.4": L05.html:101 ("Assuming Assumption 1.4, the central difference has error of order h^2"), '
    'L05.html:107 ("Assuming Assumption 1.4, the central difference..."), L05.html:221, 284, 286 (sentence-level). The key-results table (L05.html:334-343) uses no Assumption 1.4. '
    'Numbers re-derived exactly (l05_l04_exact_r7.out): central-difference errors 2.350000001e-07 (p), 3.33e-10 (q), 8.55e-07 (c), all within 1e-6; p\'\'\'(1.5)=141; h^2 p\'\'\'/6 = 2.35e-07. '
    'LOW, not ruling-26 kinds: L05.html:92 says "These are the second and third derivatives used below", but f\'\' is used below only inside the definition of f\'\'\' (no later use); wording only.')
over['M2a-R1-L05-MATH-01'] = None
over['M2a-R1-L05-CARD-01'] = None

# ---- L06 card scope ----
over['M2a-R1-L06-CARD-01'] = ('2.7 cards of L06 (M2-c064 scope changed; M2-c394 and M2-c414 changed)',
    'course/modules/M/M2/cards.json:451 (M2-c064), cards.json (M2-c394, M2-c414, M2-c062 to c074)', 'FAIL',
    'Re-verified from scratch at aa659725. M2-c064: the scope defect is the one in M2a-R1-X02 (key-results row L06.html:326 uses Assumption 2.1 without the opening that the card asserts for every Lesson 6 result). '
    'M2-c394 (changed): "For a fixed constant M, f is Lipschitz with constant M when |f(x) - f(y)| <= M|x - y| for all x and y. The name is given in prose in Problem R3." '
    'Checked: L06.html:307 (R3) says "A function with this property is called Lipschitz with constant M, and the name is given here in prose", so the claim is true. The round-6 phrase "in the domain" is dropped; in R3 f is on R, so the quantifier is read on the domain (LOW). '
    'M2-c414 (changed): "A point c with f\'(c) = 0 (Section 1)." Checked: L06.html:55 defines a critical point of a differentiable function as a point c with f\'(c)=0. '
    'M2-c062, c063, c065-c074 are byte-identical and carried. FAIL for the same reason as X02.',
    'Same as M2a-R1-X02: scope the card to Sections 2 and 3 (matching L06.html:325) or make L06.html:326 begin with "Assuming Assumption 2.1," and then re-verify.')
over['M2a-R1-L06-ASSUME-01'] = ('2.4 Assumption 2.1 (extreme value theorem): the scope rule at L06.html:73 and every use',
    'course/modules/M/M2/L06.html:71-73, 77-78, 86-88, 102-103, 111, 115, 277, 322-326', 'FAIL',
    'Re-verified; the round-6 PASS is withdrawn. L06.html:73 says "Every result below that uses it begins its statement with \\"Assuming Assumption 2.1\\"". '
    'Results that use it and begin with the phrase: Theorem 2.2 (L06.html:77-78), Theorem 2.3 (L06.html:87-88), Corollary 3.1 (L06.html:102-103), key-results rows L06.html:322-324. '
    'Counterexample: key-results row L06.html:326 (grade C, "For x^3 - 3x, 8 of the 16 grid intervals on [-2, 2] increase, and f(-1) = 2, f(1) = -2"), whose source '
    'says "the monotone intervals follow from the derivative on the page, assuming Assumption 2.1 (Corollary 3.1)"; its statement does not begin with the phrase, and it lies below L06.html:73. '
    'L06.html:325 limits the same rule to "every result in §2 and §3", so the page states two scopes. Row 326 is byte-identical since e896b7a4; round 6 passed this row by reading L06.html:325 as the scope. '
    'Other uses are sentence-level or are not results: the Theorem 2.2 proof (L06.html:83), the lab docstring (tests/labs/M2/lab-M2-L06-1.py:9), problem prompts (L06.html:218, 232, "under Assumption 2.1", LOW, problems are not results), '
    'and solutions and quiz prompts begin "Assuming Assumption 2.1" (sentences beginning "Assuming Assumption 2.1" at L06.html:220, 234, 243, 250, 257, 277, 355, 369). Assumption 2.1 is not graded (L06.html:73, 325).',
    'Either narrow L06.html:73 to "Every result in Sections 2 and 3 that uses it begins its statement with ..." (matching L06.html:325), or rewrite the key-results row at L06.html:326 so that its statement begins "Assuming Assumption 2.1,". Then re-verify.')
over['M2a-R1-L06-MATH-03'] = None

# ---- row H07: carry with line evidence ----
# carried rows handled below

PREF_BY_ID = {}
for rid in base_rows:
    if rid.startswith('M2a-R1-H') or rid.startswith('M2a-R3-H') or rid.startswith('M2a-R4-H'):
        PREF_BY_ID[rid] = PREF_IDX
PREF_BY_ID['M2a-R1-H07'] = PREF_H07
PREF_BY_ID['M2a-R3-H08'] = PREF_IDX
PREF_BY_ID['M2a-R4-H08b'] = PREF_IDX
PREF_BY_ID['M2a-R1-X04'] = PREF_IDX
PREF_BY_ID['M2a-R1-X05'] = ("Carried from round 6 (quiz blocks byte-identical since e896b7a4 for L01, L02, L03, L04, L06; "
                            "L05 quiz moved from old lines 345-414 to new lines 347-416 with identical content):")
PREF_BY_ID['M2a-R1-X-GRADE-01'] = PREF_L05S
PREF_BY_ID['M2a-R1-X-REF-01'] = ("Carried from round 6 (index.html and L01-L04, L06 References sections byte-identical since e896b7a4; "
                                 "the L05 References section moved by +2 lines with identical content):")
for rid in ['M2a-R1-L01-MATH-01', 'M2a-R1-L01-MATH-02', 'M2a-R1-L01-LAB-01', 'M2a-R1-L01-GRADE-01', 'M2a-R1-L01-PROSE-01',
            'M2a-R4-L01-PROSE-02', 'M2a-R1-L01-QUIZ-01']:
    PREF_BY_ID[rid] = PREF_L01
PREF_BY_ID['M2a-R1-L01-CARD-02'] = PREF_CARDS
for rid in ['M2a-R1-L02-MATH-01', 'M2a-R1-L02-MATH-02', 'M2a-R1-L02-LAB-01', 'M2a-R1-L02-PROSE-01', 'M2a-R1-L02-PROSE-02',
            'M2a-R1-L02-E-01', 'M2a-R1-L02-QUIZ-01']:
    PREF_BY_ID[rid] = PREF_L02
PREF_BY_ID['M2a-R1-L02-CARD-01'] = PREF_CARDS
for rid in ['M2a-R1-L03-MATH-01', 'M2a-R1-L03-MATH-02', 'M2a-R1-L03-MATH-03', 'M2a-R1-L03-PROSE-01', 'M2a-R1-L03-LAB-01',
            'M2a-R1-L03-QUIZ-01']:
    PREF_BY_ID[rid] = PREF_L03
PREF_BY_ID['M2a-R1-L03-CARD-01'] = PREF_CARDS
PREF_BY_ID['M2a-R1-L04-MATH-01'] = PREF_L04L
PREF_BY_ID['M2a-R1-L04-LAB-01'] = PREF_L04L
PREF_BY_ID['M2a-R1-L04-QUIZ-01'] = PREF_L04L
PREF_BY_ID['M2a-R1-L05-MATH-01'] = PREF_L05S
PREF_BY_ID['M2a-R1-L05-MATH-03'] = PREF_L05S
PREF_BY_ID['M2a-R1-L05-LAB-01'] = PREF_L05S
PREF_BY_ID['M2a-R1-L05-PROSE-01'] = PREF_L05S
PREF_BY_ID['M2a-R1-L05-QUIZ-01'] = PREF_L05S
PREF_BY_ID['M2a-R1-L05-CARD-01'] = PREF_CARDS
PREF_BY_ID['M2a-R1-L06-MATH-01'] = PREF_L06
PREF_BY_ID['M2a-R1-L06-MATH-02'] = PREF_L06
PREF_BY_ID['M2a-R1-L06-MATH-03'] = PREF_L06
PREF_BY_ID['M2a-R1-L06-LAB-01'] = PREF_L06
PREF_BY_ID['M2a-R1-L06-QUIZ-01'] = PREF_L06

rows = []
for rid, r in base_rows.items():
    pass
ordered = [r['id'] for r in base['rows']]
for rid in ordered:
    if rid in over and over[rid] is not None:
        check, location, status, evidence, *fix = over[rid]
        row = {'id': rid, 'check': check, 'location': location, 'status': status, 'evidence': evidence}
        if fix:
            row['fix'] = fix[0]
        rows.append(row)
    elif rid == 'M2a-R1-L06-MATH-03':
        c = carry(rid, PREF_BY_ID[rid])
        c['evidence'] += (' Re-checked this round for the row at L06.html:326 inside this range: the count of 8 of 16 increasing grid intervals '
                          'and f(-1) = 2, f(1) = -2 match Lab 1 (g04_twin_L06.out); the mathematics is correct. Its scope defect (the rule at '
                          'L06.html:73) is recorded in M2a-R1-L06-ASSUME-01 and M2a-R7-L06-KEYROW-326, not here.')
        rows.append(c)
    elif rid in PREF_BY_ID:
        rows.append(carry(rid, PREF_BY_ID[rid]))
    else:
        raise SystemExit('no treatment for ' + rid)

# new row for the defect located in the key-results table
rows.insert(ordered.index('M2a-R1-L06-ASSUME-01') + 1 if False else len(rows), {
    'id': 'M2a-R7-L06-KEYROW-326', 'check': '2.4 scope of Assumption 2.1 in the key-results table (rule 13: missing hypothesis in a result)',
    'location': 'course/modules/M/M2/L06.html:326 against L06.html:73 and L06.html:325',
    'status': 'FAIL',
    'evidence': 'New row for the defect shared by M2a-R1-X02, M2a-R1-L06-CARD-01 and M2a-R1-L06-ASSUME-01. Key-results row L06.html:326 is a result (grade C, Lab 1 count and f(-1), f(1)) whose source '
                'says the monotone intervals follow "assuming Assumption 2.1 (Corollary 3.1)"; its statement does not begin with "Assuming Assumption 2.1". The page states the rule as "every result below" '
                '(L06.html:73) and as "every result in §2 and §3" (L06.html:325). Byte-identical since e896b7a4 (the row is unchanged by the delta), so this is a defect that round 6 missed. '
                'Lab 1 facts behind the row: g04_twin_L06.out "grid intervals on which f increases: 8 of 16", "f(-1) = 2; f(1) = -2" (exact). The count itself is correct.',
    'fix': 'Make the statement carry its hypothesis: rewrite L06.html:326 as "Assuming Assumption 2.1, the monotone intervals ..." with the Lab 1 count split out as a C row without the assumption, '
           'or narrow the rule at L06.html:73 to Sections 2 and 3 and the card to match. Then re-run the L06 gates and delta-verify.'})

fragment = {
    'unit': 'M2', 'slice': 'a', 'round': 7,
    'verifier': 'independent verifier (Haiku 5.5), unit M2 slice a, round 7 (delta verification, ruling 30)',
    'pin': 'aa659725 (detached checkout HEAD; slice delta e896b7a4..aa659725)',
    'base': 'Round-6 fragment /Users/billyribeiro/.fanout/frags/S-M2-a.round6.json (verified at pin e896b7a4).',
    'checkout': ROOT,
    'scratch': 'ledgers/M2/scripts/M2-a-r7/',
    'verified_at': '2026-11-09',
    'verdict': 'FAIL',
    'rows': rows,
    'mutants': [],
    'registry_flags': [],
    'freshness_flags': [],
    'notes': [
        'Lesson slice: no project grader is in scope, so no mutants are required (ruling 26 mutation applies to project graders). mutants is empty by design.',
        'Slice diff e896b7a4..aa659725 over the slice: L04.html (lines 51, 202, 263), L05.html (lines 92-93 inserted, 94 rewritten), cards.json (slice cards M2-c013, c044, c048 removed, c064, c394, c414). index.html, L01-L03, L06 pages and all six twins are unchanged.',
        'Outside the slice, seen only through the cards diff: M2-c161, c169, c176, c187, c263, c334, c421, c422, c423, c425 changed; M2-c129, c160, c208, c419 removed. Not verified here.',
        'LOW (not ruling-26 kinds): slice cards without a grade key rose from 23 to 24 (M2-c013 lost its grade T). Card style.',
        'LOW: near-duplicate slice cards from round 5 (M2-c010/c013, c063/c071, c017/c018) unchanged; M2-c048 removal reduces the c044/c048/c049 cluster.',
        'LOW: L05.html:38 header "Introduces: no new concept" no longer lists the notations f\'\' and f\'\'\' that L05.html:92 now introduces.',
        'LOW: L05.html:92 "These are the second and third derivatives used below": f\'\' is used below only inside the definition of f\'\'\'.',
        'LOW: L07.html:59 (Definition 1.1, higher derivative) defines the same notations later; values agree, no contradiction, but the concept is defined twice in the unit.',
        'LOW: M2-c394 drops "in the domain" from the Lipschitz condition; in R3 f is on R.',
        'LOW: problem prompts at L06.html:218 and 232 say "under Assumption 2.1" rather than "Assuming"; problems are not results (ruling of the L06 rule).',
        'LOW carried: L04.html:156 forward pointer to Lesson 13 (unchanged since round 3).',
        'Round-6 rows withdrawn: M2a-R1-L06-ASSUME-01 was PASS in round 6 but its scope claim at L06.html:73 is contradicted by L06.html:326 (unchanged since e896b7a4); now FAIL.',
        'Round-6 FAIL M2a-R1-X-DEP-01 is PASS now (the link to Lesson 7 is removed and the notations are defined in L05).',
        'Round-6 FAIL M2a-R1-X02 and M2a-R1-L06-CARD-01 remain FAIL: the card scope is narrowed to Lesson 6 (the L10-L12 counterexamples no longer apply), but the in-lesson counterexample L06.html:326 remains.',
        'Not checked: lessons L07-L24, project.html, the project grader, the other slices; no browser screenshot (page_smoke only); the live verify_refs run covers the two M2 entries it re-checks.',
        'Pre-existing tracked files in ledgers/M2/scripts/M2-a-r7/ (l05_exact.py, l06_grid.py, make_fragment.py, twin_compare.py) were not read or modified by this round; this round\'s scripts have distinct names.',
        'The round-6 twin_compare.py has a hard-coded path to another checkout; it was not used.',
    ],
    'summary': '',
}
n_pass = sum(1 for r in rows if r['status'] == 'PASS')
n_fail = sum(1 for r in rows if r['status'] == 'FAIL')
fragment['summary'] = (f'M2 slice a, round 7 (delta verification at aa659725, ruling 30). {len(rows)} rows: {n_pass} PASS, {n_fail} FAIL, 0 UNVERIFIABLE. '
                       'FAIL rows (ruling 26 kind: false scope statement / missing hypothesis in a result): M2a-R1-X02, M2a-R1-L06-CARD-01, M2a-R1-L06-ASSUME-01, '
                       'M2a-R7-L06-KEYROW-326, all one defect: key-results row L06.html:326 uses Assumption 2.1 without the opening that L06.html:73 requires. '
                       'Re-verified and PASS: M2a-R1-X-DEP-01, L04-MATH-02, L05-MATH-02, L01-CARD-01, L04-CARD-01, L04-CARD-02, X-CARD-IDS, X01, X03, X-HRS-01, and all gates G01-G10 re-run.')
json.dump(fragment, open(ROOT + '/ledgers/M2/M2-a.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('rows', len(rows), 'PASS', n_pass, 'FAIL', n_fail)
