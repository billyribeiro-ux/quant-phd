import json, sys
BASE = '/Users/billyribeiro/.fanout/frags/S-E1-c.round5.json'
base = json.load(open(BASE))
base_rows = {r['id']: r for r in base['rows']}
S = 'ledgers/E1/scripts/E1-c-r1/out/'
PIN_NEW = '95f3f8cb'
CARRY_PAGES = 'course/modules/E/E1/L07.html, L08.html, L09.html and tests/labs/E1/lab-E1-L07-1.py, L08-1.py, L09-1.py'
def carry(rid, files):
    r = base_rows[rid]
    ev = ('Carried from round 5 (' + files + ' byte-identical since the previous pin dde0486b; sha256 in '
          + S + 'sha256_pages_twins.out): ' + r['evidence'])
    return {'id': rid, 'check': r['check'], 'location': r['location'], 'status': 'PASS', 'evidence': ev}
FRESH = {}
def fresh(rid, check, location, evidence):
    FRESH[rid] = {'id': rid, 'check': check, 'location': location, 'status': 'PASS', 'evidence': evidence}
# --- gate commands, re-run on 95f3f8cb
fresh('E1-c-cmd-check-pages', 'tools/check_pages.py --unit E1', 'course/modules/E/E1/L07.html; L08.html; L09.html; cards.json (check_pages reads cards.json)',
      'Re-run on 95f3f8cb: "check_pages E1: PASS", exit 0 (' + S + 'check_pages_E1.out). cards.json is read by tools/check_pages.py (grep), so the card delta is inside this gate.')
fresh('E1-c-cmd-check-dag', 'tools/check_dag.py --unit E1', 'course/modules/E/E1/L07.html:38-39; L08.html:38-39; L09.html:38-39',
      'Re-run on 95f3f8cb: "check_dag E1: PASS", exit 0 (' + S + 'check_dag_E1.out).')
fresh('E1-c-cmd-check-projects', 'tools/check_projects.py --unit E1', 'course/modules/E/E1/project.html',
      'Re-run on 95f3f8cb: "check_projects E1: PASS", exit 0 (' + S + 'check_projects_E1.out). project.html changed in the delta (the interpretation paragraph of the Lab 2 output, and the lede); the project is outside slice c and is not verified here.')
fresh('E1-c-cmd-run-labs', 'tools/run_labs.py --unit E1 --page L07 / L08 / L09, and --unit E1', 'tests/labs/E1/lab-E1-L07-1.py; lab-E1-L08-1.py; lab-E1-L09-1.py',
      'Re-run on 95f3f8cb: "run_labs E1: PASS (1/1)" for each of L07, L08, L09 (' + S + 'run_labs_L07.out, _L08.out, _L09.out) and "run_labs E1: PASS (12/12)" for the unit (' + S + 'run_labs_E1.out).')
fresh('E1-c-cmd-twin-isolated', 'twins alone under python -I -W error', 'tests/labs/E1/lab-E1-L07-1.py; lab-E1-L08-1.py; lab-E1-L09-1.py',
      'Re-run on 95f3f8cb from /tmp with env -i: "python -I -W error tests/labs/E1/lab-E1-L0{7,8,9}-1.py" exit 0 each, stderr 0 bytes; stdout in ' + S + 'twin_L07.out, twin_L08.out, twin_L09.out.')
fresh('E1-c-lab-code-equals-twin', 'page code equals twin (run_labs byte-identity check)', 'course/modules/E/E1/L07.html:140-296; L08.html:149-304; L09.html:142-262',
      'run_labs E1 PASS on 95f3f8cb (' + S + 'run_labs_E1.out), whose check is that the unescaped lab code is byte-identical to the twin. Page and twin sha256 unchanged since dde0486b (' + S + 'sha256_pages_twins.out; git diff --quiet on the twin and page paths).')
fresh('E1-c-lab-expected-equals-output', 'expected block equals twin output (exact)', 'course/modules/E/E1/L07.html:297-308; L08.html:305-325; L09.html:263-276',
      'Exact string comparison of each page pre.expected with the twin stdout (ledgers/E1/scripts/E1-c-r1/expected_eq_r1.py, output ' + S + 'expected_eq_r1.out): L07 block 0 matches (12 lines), L08 block 0 matches (21 lines), L09 block 0 matches (14 lines).')
fresh('E1-c-cmd-page-smoke', 'tools/page_smoke.py --unit E1 --pages L07 L08 L09', 'course/modules/E/E1/L07.html; L08.html; L09.html',
      'Re-run on 95f3f8cb: "page_smoke modules/E/E1/L07.html: PASS", L08 PASS, L09 PASS, "page_smoke E1: PASS", exit 0 (' + S + 'page_smoke_L07-L09.out).')
fresh('E1-c-cmd-ruff', 'ruff check and ruff format --check on the slice twins', 'tests/labs/E1/lab-E1-L07-1.py; lab-E1-L08-1.py; lab-E1-L09-1.py',
      '.venv/bin/ruff check tests/labs/E1: "All checks passed!", exit 0 (' + S + 'ruff_check.out). .venv/bin/ruff format --check tests/labs/E1: "12 files already formatted", exit 0 (' + S + 'ruff_format.out). Whole-repository ruff not run (targeted per the change table).')
fresh('E1-c-cmd-mypy', 'mypy --no-incremental on the slice twins', 'tests/labs/E1/lab-E1-L07-1.py; lab-E1-L08-1.py; lab-E1-L09-1.py',
      '.venv/bin/mypy --no-incremental on the three twins: "Success: no issues found in 3 source files", exit 0 (' + S + 'mypy_twins.out). Whole-repository mypy not run.')
fresh('E1-c-cmd-pytest', 'pytest tests/test_labs.py and tests/test_page_checks.py', 'tests/test_labs.py; tests/test_page_checks.py',
      'tests/test_page_checks.py: all tests pass, "[100%]", exit 0 (' + S + 'pytest_page_checks.out). tests/test_labs.py full file: "[100%]", exit 0 (' + S + 'pytest_test_labs_full.out). Neither file was changed in the delta (git diff --name-only dde0486b HEAD).')
fresh('E1-c-cmd-verify-refs', 'tools/verify_refs.py --offline', 'references/references.json',
      'Re-run on 95f3f8cb: "offline integrity: 560 entries, 0 problems", exit 0 (' + S + 'verify_refs_offline.out). references/ is byte-identical to dde0486b, so the offline result is unchanged; the live run was not executed (no citation in slice c).')
# --- rows whose subject includes cards.json or a scan over the delta
fresh('E1-c-dag', 'check_dag and unlinked concept uses', 'course/modules/E/E1/L07.html:38-39,60,82; L08.html:38-39,72,79; L09.html:38-39,60,122',
      'check_dag E1 PASS on 95f3f8cb (' + S + 'check_dag_E1.out). The concept links on these lines are in byte-identical pages; the new card text adds no concept link (no <a class="concept"> in cards.json, grep).')
fresh('E1-c-notation', 'notation registry against slice symbols (pages and cards)', 'notation/notation.json; course/modules/E/E1/L07.html; L08.html; L09.html; cards.json',
      'notation/notation.json byte-identical to dde0486b (git diff --quiet). Scan of all 160 cards (cards_scan_r1.py) for the registry symbols Phi, gamma_3, gamma_4, R^ast, R^(e ast), R_f, mathbb{Q}, \\ast and for a bare T symbol: 0 hits in card text (the only "T" is the grade field). Cards use the local symbols Q, d, a, b, c, p, s, n, DWL, CS, PS, W, which the pages define (L06 Definition 1.1, L07 Definition 1.1 and 1.3, L03 Setting).')
fresh('E1-c-process-words', 'process words in learner text and code comments', 'course/modules/E/E1/L07.html; L08.html; L09.html; tests/labs/E1 twins; cards.json',
      'Case-insensitive scan of all 160 cards for verif, round, ledger, builder, draft, fixer, slice, audit, sweep, finding, erratum, correction (cards_scan_r1.out): 2 regex hits, both not process words: E1-c136 "around" (L05, substring), E1-c165 "rounds half up" (the arithmetic word). Pages and twins are byte-identical (carried evidence in the prior row text).')
fresh('E1-c-banned-strings', 'BUILDER_RULES 1.3-1.4 banned strings (pages and cards)', 'course/modules/E/E1/L07.html; L08.html; L09.html; cards.json',
      'Scan of all 160 card fronts and backs for TODO, TBD, lorem, for brevity, beyond the scope, omitted, roughly, historically, you can add more, left as an exercise, it can be shown, clearly, obvious, well known, important to note, studies show, experts agree: 0 hits (cards_scan_r1.out). Pages carry the round-5 result (0 matches, BUILDER_RULES.md:45-52, 116).')
fresh('E1-c-attribution', 'attributions and citations (pages and cards)', 'course/modules/E/E1/L07.html:535; L08.html:555; L09.html:503; cards.json',
      'Re-read of L07.html:535 (unchanged) and a token scan of all cards for years, "et al", "Ref." and "SEC": no bibliographic token. "Theorem n" and "Proposition n" tokens in the cards name in-unit results (L06 Theorem 3.3, Proposition 4.1 at L06.html:179, 391; L03 Proposition 1.3 at L03.html:73). The card tokens are in-unit only.')
fresh('E1-c-scope-words', 'scope words (only, all, every, always, any, same, drives, exactly) in slice prose and cards', 'course/modules/E/E1/L07.html; L08.html; L09.html; cards.json',
      'Pages: carried from round 5 (byte-identical). Cards: the 48 slice cards (L07-L09) and all 13 changed or new cards were scanned (' + S + 'cards_scan_r1.out and inline scan). Scope words in the changed cards: "unique" in E1-c018 and E1-c056 (L02 Proposition 1.3 and L05 Proposition 5.2 state uniqueness, L02.html:73-76, L05.html:67-70); "exactly" in E1-c030 (L03 Proposition 1.3 says "exactly one", L03.html:74). E1-c101, c160, c161-c166 use no scope word; E1-c039 uses none beyond the Assumption wording. Slice cards L07 "only" and "every" are in byte-identical objects (base round 5).')
fresh('E1-c-cards-coverage', 'cards cover every definition, theorem, key formula, key result and misconception of L07-L09', 'course/modules/E/E1/cards.json',
      'L07 coverage re-checked on 95f3f8cb: Definition 1.1 (E1-c092), Definition 1.3 (E1-c094), Theorem 1.2 (c093), Lemma 1.4 (c095), Theorem 1.5 (c096), Corollary 2.1 (c097-c099), Example 2.2 (c100), Proposition 2.3 (c101 orderings; c166 the shares), three misconceptions (c102-c104), Lab 1 (c105). The round-5 coverage of c101 (shares) moved to c166, which covers the monopoly and Cournot shares 1/4 and 1/9 (L07.html:127). L08 and L09 cards are byte-identical (cards_scan_r1.out).')
fresh('E1-c-cards-sample', 'card sample and full read of the slice cards (L07 15, L08 17, L09 16)', 'course/modules/E/E1/cards.json (E1-c092..E1-c105, E1-c106..E1-c158, E1-c166)',
      'The 48 slice cards were compared with the lesson text: the 46 unchanged objects are byte-identical to the round-5 pin (cards_delta_r1.out lists the changed ids: c018, c023, c030, c039, c056, c101 and the removed c088, c159; the new cards c161-c166); c101 and c166 were read against L07.html:122-135 and 139-140 (see E1-c-cards-agree-L07). The L08 and L09 objects are byte-identical (cards_scan_r1.out, "byte-identical objects ... True").')
fresh('E1-c-cards-full-scan', 'full scan for duplicate cards', 'course/modules/E/E1/cards.json',
      'Re-run on 95f3f8cb (cards_delta_r1.py, output ' + S + 'cards_delta_r1.out): 160 cards, 160 unique ids, 0 duplicate fronts, 0 duplicate backs. Near-duplicate check of each changed card against all others (near_dup_r1.out): the new splits c018/c161 (Jaccard 0.643), c023/c018 (0.630), c030/c163 (0.595), c162/c023 (0.562) ask different questions (output versus marginal cost; formula versus nondecreasing; equilibrium price versus quantity). No other pair reaches 0.5.')
fresh('E1-c-cards-agree-L07', 'cards E1-c092..E1-c105 and E1-c166 agree with lesson text, carry hypotheses, numbers in lesson', 'course/modules/E/E1/cards.json: E1-c101, E1-c166 (changed or new); E1-c092..E1-c105; L07.html:122-135, 139-140',
      'E1-c101 back: "Under the hypotheses of Definition 1.1 of Lesson 6 (b > 0, c > 0, a > bc): 0 < DWL_C < DWL_M and DWL_B = 0. CS_M < CS_C < CS_B, PS_M > PS_C > PS_B = 0 and W_M < W_C < W_B (Proposition 2.3)". Matches L07.html:127 (Proposition 2.3 statement, which includes these orderings; the shares move to E1-c166) and L06.html:60 (Definition 1.1, d = a - bc). E1-c166 front and back: shares 1/4 (monopoly, d^2/(8b) against d^2/(2b)) and 1/9 (Cournot, d^2/(18b) against d^2/(2b)); L07.html:127 says "one quarter" and "one ninth", and L07.html:122 gives d^2/(2b) = 5000 cents. Exact check (recompute_cards_r1.out): (d^2/(8b))/(d^2/(2b)) = 1/4 and (d^2/(18b))/(d^2/(2b)) = 1/9 for three parameter sets. Other L07 cards are byte-identical to the round-5 verified objects.')
fresh('E1-c-cards-ids-grades', 'ids and grade fields', 'course/modules/E/E1/cards.json',
      '160 unique ids (cards_delta_r1.out). No card has a missing id, lesson, front or back. Every new card (E1-c161..c166) is a claim with grade T and a cited proposition, as the other claim cards (cards_delta_r1.out, grade counts T 101, C 27, none 32).')
fresh('E1-c-card-duplicate-c128-c131', 'duplicate check for E1-c128 and E1-c131', 'course/modules/E/E1/cards.json (E1-c128, E1-c131)',
      'E1-c128 and E1-c131 are byte-identical to dde0486b (cards_delta_r1.out does not list them). The whole-deck exact scan (0 duplicates) and the near-duplicate scan (near_dup_r1.out, which shows no changed card with either as its nearest neighbour) find no duplicate of either.')
fresh('E1-c-card-numbers-r2', 'every number in a slice card back appears in its lesson', 'course/modules/E/E1/cards.json (48 slice cards; 13 changed or new cards from any lesson)',
      'cards_scan_r1.py: every multi-digit number (two or more digits, fractions included) in the back of each slice card and each changed card appears in its own lesson text (tags stripped, HTML unescaped): "none" missing (cards_scan_r1.out). Single-digit values and formulas in the changed cards were read by hand (E1-c-cards-agree-L07 and the row below).')
fresh('E1-c-card-duplicates-r2', 'duplicate cards over the whole deck', 'course/modules/E/E1/cards.json (160 cards)',
      'cards_delta_r1.py on 95f3f8cb: 160 cards, 0 exact duplicate fronts, 0 exact duplicate backs, 0 duplicate ids (cards_delta_r1.out).')
fresh('E1-c-recompute-exact-r2', 'exact recomputation of numbers on L07-L09 and of the changed cards', 'course/modules/E/E1/L07.html; cards.json (E1-c101, E1-c160, E1-c161..c166, E1-c018, E1-c023, E1-c030, E1-c039, E1-c056)',
      'L07 page numbers: the page is byte-identical to dde0486b, so the round-5 recomputation (recompute_L07_r5.py, ALL_OK, 64 checks) carries. L08 and L09 numbers carry from round 4 by byte-identity. New in this round: recompute_cards_r1.py with exact Fraction arithmetic (output ' + S + 'recompute_cards_r1.out, ALL_OK): Assumption M p_m, Q_m and pi_m for four parameter sets; Cournot n = 2 reference case Q = 200/3, fee 160/3, two-exchange profit 20000/9 rounding half up to 2222; Cournot DWL d^2/(18b) = 5000/9 and share 1/9; monopoly DWL d^2/(8b) = W_C - W_M; Bertrand volume d, fee c, profit 0; L03 equilibrium Q* = s(p*-c) = a - bp* > 0 and p*-c = (a-bc)/(b+s) over 500 random cases; L03 Example 1.5 values p* = 110/7, Q* = 480/7, per-firm 48/7.')
fresh('E1-c-delta-r1', 'delta dde0486b..95f3f8cb for slice c subjects', 'course/modules/E/E1/cards.json; course/modules/E/E1/project.html (outside slice c); L07.html, L08.html, L09.html, tests/labs/E1/*, notation/, references/, tools/, tests/test_labs.py, tests/test_page_checks.py',
      'git diff --name-only dde0486b HEAD over slice paths: only course/modules/E/E1/cards.json and course/modules/E/E1/project.html. Pages L07-L09, the twins, notation/, references/, the gate tools and the two pytest files are unchanged (git diff --quiet, exit 0). cards.json: 6 changed (c018, c023, c030, c039, c056, c101), 2 removed (c088, L06; c159, L06), 6 added (c161-c166), c160 byte-identical; all verified in the rows above. No card of L08 or L09 changed. Ruling 37 (closing round writes no mutants): no mutants written, none in the slice. Ruling 30 scope: the base round-5 rows were re-checked from scratch (non-PASS rows: none) and every row whose subject changed was re-verified; the other rows carry.')
# --- rows carried from round 5 (subjects byte-identical)
CARRY_MATH = {
 'E1-c-math-L07-closed-forms': 'course/modules/E/E1/L07.html',
 'E1-c-math-L07-corollary-prop23': 'course/modules/E/E1/L07.html',
 'E1-c-math-L07-example-2-2': 'course/modules/E/E1/L07.html',
 'E1-c-math-L07-R-problems': 'course/modules/E/E1/L07.html',
 'E1-c-math-L08-grid': 'course/modules/E/E1/L08.html',
 'E1-c-math-L08-proofs': 'course/modules/E/E1/L08.html',
 'E1-c-math-L08-improvements': 'course/modules/E/E1/L08.html',
 'E1-c-math-L08-problems': 'course/modules/E/E1/L08.html',
 'E1-c-math-L09-closed-forms': 'course/modules/E/E1/L09.html',
 'E1-c-math-L09-public-good': 'course/modules/E/E1/L09.html',
 'E1-c-math-L09-numbers': 'course/modules/E/E1/L09.html',
 'E1-c-prose-numbers-L07': 'course/modules/E/E1/L07.html',
 'E1-c-prose-numbers-L08': 'course/modules/E/E1/L08.html',
 'E1-c-prose-numbers-L09': 'course/modules/E/E1/L09.html',
 'E1-c-grades-L07': 'course/modules/E/E1/L07.html',
 'E1-c-grades-L08': 'course/modules/E/E1/L08.html',
 'E1-c-grades-L09': 'course/modules/E/E1/L09.html',
 'E1-c-problems-L07': 'course/modules/E/E1/L07.html',
 'E1-c-problems-L08': 'course/modules/E/E1/L08.html',
 'E1-c-problems-L09': 'course/modules/E/E1/L09.html',
 'E1-c-quiz-L07': 'course/modules/E/E1/L07.html',
 'E1-c-quiz-L08': 'course/modules/E/E1/L08.html',
 'E1-c-quiz-L09': 'course/modules/E/E1/L09.html',
 'E1-c-misconceptions': 'course/modules/E/E1/L07.html; L08.html; L09.html',
 'E1-c-define-before-use-L07': 'course/modules/E/E1/L07.html',
 'E1-c-define-before-use-L08': 'course/modules/E/E1/L08.html',
 'E1-c-define-before-use-L09-L82': 'course/modules/E/E1/L08.html; L09.html',
 'E1-c-cross-refs': 'course/modules/E/E1/L07.html; L08.html; L09.html',
 'E1-c-structure': 'course/modules/E/E1/L07.html; L08.html; L09.html',
 'E1-c-figures-data': 'course/modules/E/E1/L07.html; L08.html; L09.html',
 'E1-c-hours-titles': 'course/modules/E/E1/L07.html; L08.html; L09.html; index.html (unchanged since dde0486b)',
 'E1-c-prose-number-L09-E2-2500': 'course/modules/E/E1/L09.html',
 'E1-c-lab-statements-r2': 'course/modules/E/E1/L07.html; L08.html; L09.html; tests/labs/E1 twins',
}
CARRY_CARDS = {
 'E1-c-cards-agree-L08': 'course/modules/E/E1/L08.html and the 17 L08 card objects (cards_scan_r1.out: "byte-identical objects for L08/L09 cards ... True")',
 'E1-c-cards-agree-L09': 'course/modules/E/E1/L09.html and the 16 L09 card objects (cards_scan_r1.out)',
 'E1-c-card-grade-c118': 'the E1-c118 card object (cards_delta_r1.out does not list it) and L08.html',
 'E1-c-card-c149-self-contained': 'the E1-c149 card object (cards_delta_r1.out does not list it) and L08.html/L09.html',
 'E1-c-card-new-c157-c158': 'the E1-c157 and E1-c158 card objects (cards_delta_r1.out does not list them) and L08.html',
 'E1-c-dwl-benchmark-L09': 'L07.html:81-84 (byte-identical), E1-c123 (not in cards_delta_r1.out), L09.html:38, 99-105',
 'E1-c-delta-r4': 'historical round-4 row; c104, c114, c128, c157, c158 are not in cards_delta_r1.out; L08.html and L09.html byte-identical',
 'E1-c-delta-r5': 'historical round-5 row for the edbb7aa8..dde0486b delta; its named hunks (L07.html:422-428, index.html:42) are byte-identical at 95f3f8cb',
}
rows = []
for rid in base_rows:
    if rid in FRESH:
        rows.append(FRESH[rid])
    elif rid in CARRY_MATH:
        rows.append(carry(rid, CARRY_MATH[rid]))
    elif rid in CARRY_CARDS:
        rows.append(carry(rid, CARRY_CARDS[rid]))
    else:
        raise SystemExit('unmapped base row ' + rid)
for rid in FRESH:
    if rid not in base_rows:
        rows.append(FRESH[rid])
print('rows', len(rows), 'base rows', len(base_rows), 'new rows', [r['id'] for r in rows if r['id'] not in base_rows])
frag = {
 'unit': 'E1', 'slice': 'c', 'round': 1,
 'verifier': 'independent Haiku verifier, closing delta verification (ruling 30), slice c (L07-L09, lab twins, cards); did not build E1',
 'pin': '95f3f8cb21c2cd9fc904430bd30a6b734d01f672',
 'base': 'dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-5 fragment ~/.fanout/frags/S-E1-c.round5.json, all 68 rows PASS); delta git diff dde0486b..95f3f8cb',
 'checkout': '/Users/billyribeiro/.fanout/wt/verifyF11-E1-c (detached at 95f3f8cb; .venv symlink to /Users/billyribeiro/dev/quant-phd/.venv)',
 'scratch': 'ledgers/E1/scripts/E1-c-r1/',
 'verified_at': '2026-11-09T15:30:00+00:00',
 'verdict': 'PASS' if all(r['status'] == 'PASS' for r in rows) else 'FAIL',
 'rows': rows,
 'mutants': [],
 'registry_flags': [],
 'freshness_flags': [],
 'notes': [
  'Round field: the orchestrator asked for round=1 for this closing delta; the base fragment it is delta-verified from is round 5 (pin dde0486b). Carry prefixes cite round 5.',
  'Base round-5 fragment: all 68 rows PASS, 0 mutants, no registry or freshness flags. This round: 0 non-PASS rows; no FAIL row needed re-verification from scratch.',
  'Changed subjects re-verified: cards.json (6 changed, 2 removed, 6 added) and every row that cites the card set. project.html is outside slice c; its check_projects gate was re-run and PASS, but its content was not verified here.',
  'Observation (not a FAIL, slice-external): removing E1-c088 (L06 monopoly reference-case card: 50 units, 70 cents, 2500 cents) leaves no card for the monopoly reference-case numbers; L06 coverage belongs to another slice. Cards E1-c160 and E1-c165 now carry the Bertrand and Cournot reference-case values.',
  'Observation: E1-c018 and E1-c161 (Jaccard 0.643), E1-c023 and E1-c162, E1-c030 and E1-c163 are split questions with different answers, not duplicates; the reviewer may want to confirm this reading.',
  'Regex false positive: the process-word scan matched "around" (E1-c136) and "rounds" (E1-c165); neither is a process word.',
  'Ruling 37: this closing round wrote no mutants; the slice has no grader, so no standing mutant set applies (run_graders and mutate_graders not run).',
 ],
 'summary': 'Slice c closing delta dde0486b..95f3f8cb: PASS. 69 rows: 69 PASS, 0 non-PASS (68 base rows kept with ids, plus E1-c-delta-r1). Changed cards.json subjects re-verified from scratch; pages, twins, notation, references and gate tools byte-identical, carried with the carry prefix. All slice gates re-run on 95f3f8cb and PASS.',
}
json.dump(frag, open('ledgers/E1/E1-c.json', 'w'), indent=1, ensure_ascii=False)
print('written', frag['verdict'])
