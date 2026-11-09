import json

BASE = json.load(open('/Users/billyribeiro/.fanout/frags/S-M2-a.round8.json'))
PIN = '2a805c83'
PREV = '4540351d'
CARRY_PAGES = ('Carried from round 8 (course/modules/M/M2 pages, index.html and tests/labs/M2 byte-identical since '
               '4540351d: `git diff --stat 4540351d..2a805c83` over these paths prints nothing; the only slice-path change '
               'is course/modules/M/M2/cards.json): ')
CARRY_CARDS = ('Carried from round 8 (the cited M2 card records are byte-identical since 4540351d: the per-id comparison '
               'in ledgers/M2/scripts/M2-a-r1/card_checks.py prints only M2-c064 as differing among the 84 L01-L06 cards; '
               'the cited lesson pages and twins are byte-identical): ')

RE = {
 'M2a-R1-G01': ('check_pages --unit M2', 'tools/check_pages.py --unit M2',
   'Re-run at 2a805c83 (cards.json changed): ledgers/M2/scripts/M2-a-r1/g01_check_pages.out = "check_pages M2: PASS", EXIT 0.'),
 'M2a-R1-G02': ('2.9 DAG gate: check_dag --unit M2', 'tools/check_dag.py --unit M2',
   'Re-run at 2a805c83: g02_check_dag.out = "check_dag M2: PASS", EXIT 0.'),
 'M2a-R1-G03': ('2.5 labs: run_labs --unit M2', 'tools/run_labs.py --unit M2',
   'Re-run at 2a805c83: g03_run_labs.out = "run_labs M2: PASS (27/27)", EXIT 0.'),
 'M2a-R1-G04': ('2.5 twins alone under python -I -W error; page code equals twin; expected block equals output',
   'tests/labs/M2/lab-M2-L01-1.py .. lab-M2-L06-1.py; course/modules/M/M2/L01.html .. L06.html',
   'Re-run at 2a805c83: each twin under `.venv/bin/python -I -W error` exits 0 with empty stderr (g04_twin_L01..L06.out/.err; '
   'exit3.txt). Page-code-equals-twin and expected-block-equals-output: the six pages and twins are byte-identical since 4540351d '
   '(empty `git diff --stat`), and the expected blocks are checked again by run_labs (G03). Carried from round 8 for that part: '
   'page code equals twin for all six (the one-character difference is the trailing newline).'),
 'M2a-R1-G05': ('2.5 test_labs for the six M2 twins', "tests/test_labs.py -k 'M2 and (L01 or ... or L06)'",
   'Re-run at 2a805c83: g05_test_labs_M2.out shows six passed dots, EXIT 0.'),
 'M2a-R1-G06': ('2.9 page_smoke for the slice pages', 'tools/page_smoke.py --unit M2 --pages index L01 ... L06 --skip-sweep',
   'Re-run at 2a805c83 (cards.json changed): g06_page_smoke.out ends "page_smoke modules/M/M2/L06.html: PASS" and "page_smoke M2: PASS", EXIT 0.'),
 'M2a-R1-G07': ('ruff, ruff format, mypy --no-incremental on the six slice twins', 'tests/labs/M2/lab-M2-L0[1-6]-1.py',
   'Re-run at 2a805c83: g07_ruff.out "All checks passed!"; g07_ruff_format.out "6 files already formatted"; '
   'g07_mypy.out "Success: no issues found in 6 source files"; all EXIT 0.'),
 'M2a-R1-G08': ('2.9 verify_refs offline and unit M2', 'tools/verify_refs.py --offline; tools/verify_refs.py --unit M2',
   'Re-run at 2a805c83: g08_verify_refs_offline.out "offline integrity: 560 entries, 0 problems", EXIT 0; g08_verify_refs_unit.out '
   '"live re-verification of M2: 2 of 560 entries, 0 problems", EXIT 0.'),
 'M2a-R1-G09': ('2.9 check_projects --unit M2', 'tools/check_projects.py --unit M2',
   'Re-run at 2a805c83: g09_check_projects.out = "check_projects M2: PASS", EXIT 0.'),
 'M2a-R6-G10': ('build_site --check and tests/test_build_site.py', 'tools/build_site.py --check; tests/test_build_site.py',
   'Re-run at 2a805c83 because cards.json changed: g10_build_site_check.out "site data current: 6 outputs", EXIT 0; '
   'g10_pytest_build_site.out 31 passed dots, EXIT 0.'),
 'M2a-R1-X02': ('2.7 cards: ids, structure, numbers, duplicates, agreement with lesson text (slice cards)',
   'course/modules/M/M2/cards.json:440-443 (M2-c064, back at line 443); course/modules/M/M2/L06.html:73 and 326 (key-results row); L06.html:325',
   'Re-verified from scratch at 2a805c83 because M2-c064 changed (`git diff 4540351d..2a805c83 -- cards.json`, hunk @@ -440 +440). '
   'The new back text: (a) "No. It is assumed: a function continuous at each point of [a, b] with a < b attains a maximum and a minimum on [a, b]. '
   'No grade is given." matches L06.html:72-73 (Assumption 2.1, "no grade is given to it"); no grade key on the card, matching the page. '
   '(b) "In Sections 2 and 3 of Lesson 6, every result that uses it begins its statement with \\"Assuming Assumption 2.1\\"": '
   'Theorem 2.2 L06.html:78, Theorem 2.3 L06.html:88, Corollary 3.1 L06.html:103 begin with "Assuming Assumption 2.1"; the remark at L06.html:111 too; '
   'Section 1 (L06.html:53-67) cites no Assumption (grep "Assum" finds none there). (c) "Lesson 8 states the same assumption as its Assumption 1.1 (Section 1), with no grade": '
   'L08.html:54 is Section 1 ("Setting and the tool"), L08.html:61-62 is the block "Assumption 1.1 ... Let phi be continuous on a closed interval [p, q] with p < q. '
   'Then phi attains a maximum value and a minimum value on [p, q]. ... No grade is given to it here." Same content; the page has no data-grade on it (L08.html:60-63). '
   'Key row L06.html:325 "Assumption 2.1 ... not graded" and L06.html:326 (C, Lab 1) agree (see M2a-R7-L06-KEYROW-326). '
   'Slice cards L01-L06: 84, all with no change except M2-c064. Card count and duplicates: see M2a-R1-X-CARD-IDS. '
   'Removed cards M2-c417, c428, c429 have no references in course/, tests/, tools/ or plans/ (grep, empty).'),
 'M2a-R1-X-CARD-IDS': ('2.7 cards: ids, duplicate facts across the unit', 'course/modules/M/M2/cards.json (395 cards)',
   'Re-verified at 2a805c83: ledgers/M2/scripts/M2-a-r1/card_checks.py prints "cards 395 unique ids 395", "duplicate fronts []", '
   '"duplicate backs []", per-lesson counts (L01 18, L02 13, L03 14, L04 10, L05 14, L06 15, ...). Delta from 4540351d (398 cards, card_delta.py): '
   'removed M2-c417, c428, c429 (none added); changed M2-c064 and 27 cards outside L01-L06 (not verified in this slice). '
   'Correction to the base location: the base wrote "(393 cards)", but its own evidence and the JSON at 4540351d give 398, and 395 now. '
   'Id gaps (48, 129, 144, 160, 164, 208, 243, 250, ... 417, 419, 428, 429) are not referenced anywhere in course/, tests/, tools/, plans/.'),
 'M2a-R7-L06-KEYROW-326': ('2.4 scope of Assumption 2.1 in the key-results table (rule 13: missing hypothesis in a result)',
   'course/modules/M/M2/L06.html:326 against L06.html:73 and L06.html:325',
   'Re-verified at 2a805c83 (page unchanged since 4540351d): L06.html:326 "8 of the 16 grid intervals on [-2, 2] increase, and f(-1) = 2, f(1) = -2", C, Lab 1. '
   'Twin output g04_twin_L06.out: "grid intervals on which f increases: 8 of 16", "f(-1) = 2; f(1) = -2". Independent exact-fraction recomputation '
   '(ledgers/M2/scripts/M2-a-r1/independent_L06_check.py): 8 of 16, f(-1) = 2, f(1) = -2, f\' = 3(x-1)(x+1) at all 17 grid points. '
   'Grade C matches the lab-only fact; the monotone-interval claim is tied to the derivative (L06.html:326) and to Assumption 2.1 at L06.html:73 and 325.'),
 'M2a-R1-L06-CARD-01': ('2.7 cards of L06 (M2-c064 scope changed; M2-c394 and M2-c414 changed)',
   'course/modules/M/M2/cards.json:440-443 (M2-c064), cards.json (M2-c394, M2-c414, M2-c062 to c074)',
   'Re-verified at 2a805c83 for M2-c064 (see M2a-R1-X02): back text agrees with L06.html:72-73, 77-78, 88, 103, 111 and L08.html:61-62. '
   'The other 14 L06 cards (M2-c062, c063, c065 to c074, c394, c414) are byte-identical since 4540351d per id (card_checks.py), so their round-8 evidence carries (L06.html:55, 57-59, 67, 77-78, 87-89, 94, 102-103, 111, 186, 196-205, 307, 99, and the lab output).'),
}

import re
CARRY_BOTH = ('Carried from round 8 (course/modules/M/M2 pages, index.html and tests/labs/M2 byte-identical since 4540351d; '
              'the cited M2 card records are byte-identical per id, ledgers/M2/scripts/M2-a-r1/card_checks.py, except M2-c064, '
              'which is re-verified in M2a-R1-X02): ')

def carry(row):
    loc = row['location']
    ev = row['evidence']
    if re.search(r'cards\.json|M2-c\d{3}|\bc\d{3}\b', loc + ' ' + ev):
        return CARRY_BOTH + ev
    return CARRY_PAGES + ev

rows = []
for r in BASE['rows']:
    rid = r['id']
    if rid in RE:
        check, loc, ev = RE[rid][0], RE[rid][1], RE[rid][2]
        rows.append({'id': rid, 'check': check, 'location': loc, 'status': 'PASS', 'evidence': ev})
    else:
        rows.append({'id': rid, 'check': r['check'], 'location': r['location'], 'status': 'PASS', 'evidence': carry(r)})

frag = {
  'unit': 'M2',
  'slice': 'a',
  'round': 1,
  'verifier': 'independent verifier (Haiku 5.5), unit M2 slice a, round 1 of the independent verification (closing delta, rulings 30 and 37)',
  'pin': '2a805c83 (detached checkout HEAD)',
  'base': 'Round-8 fragment /Users/billyribeiro/.fanout/frags/S-M2-a.round8.json (pin 4540351d, verified PASS). Slice delta 4540351d..2a805c83 over the slice paths: only course/modules/M/M2/cards.json (30 insertions, 51 deletions).',
  'checkout': '/Users/billyribeiro/.fanout/wt/verifyG1-M2-a',
  'scratch': 'ledgers/M2/scripts/M2-a-r1/',
  'verified_at': '2026-11-09',
  'verdict': 'PASS',
  'rows': rows,
  'mutants': [],
  'registry_flags': [],
  'freshness_flags': [],
  'notes': [
    'Scope (ruling 30): base round-8 rows re-verified from scratch where their subject changed (X02, X-CARD-IDS, L06-CARD-01, the M2-c064 card, KEYROW-326 re-derived); the gate rows G01-G10 re-run at 2a805c83; all other rows carried with the carry prefix because their cited pages, twins, index and L01-L05 card records are byte-identical since 4540351d.',
    'Ruling 37: no new mutants. The slice has no project grader, so mutants is empty, as in round 8. Ruling 26 kinds only: no new-defect hunting outside the changed rows.',
    'Card delta (card_delta.py): 398 cards at 4540351d, 395 at 2a805c83. Removed M2-c417, c428, c429. Changed M2-c064 (in slice) and 27 cards outside L01-L06 (M2-c096, c099, c102, c104, c107, c111-c114, c134, c143, c145-c147, c152, c161-c163, c169, c177, c178, c180, c265, c422, c423, c425, c430). Those outside the slice are not verified here and belong to the slices of L07, L08, L09, L10, L11, L12, L18 and L24.',
    'The base evidence for X-CARD-IDS said "393 cards" in its location; the correct count at the base was 398, and it is 395 now. This is a stale label in the base fragment, not a course defect.',
    'Not checked: the 27 changed cards outside L01-L06 and their lessons; lessons L07-L24 and project.html; a browser screenshot (page_smoke only); verify_refs live run covered 2 of 560 entries (the registry gate reports this itself), the other 558 offline only.',
  ],
  'summary': None,
}
ok = sum(1 for r in rows if r['status'] == 'PASS')
frag['summary'] = (f'M2 slice a, round 1 (closing delta at 2a805c83 over 4540351d). {len(rows)} rows: {ok} PASS, 0 FAIL, 0 UNVERIFIABLE. '
  'All gates G01-G10 re-run and pass; the one changed card in the slice (M2-c064) re-verified against L06 and L08; '
  'the other rows carried from round 8 with the carry prefix.')
json.dump(frag, open('ledgers/M2/M2-a.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('rows', len(rows), 'PASS', ok)
