import json, re, sys
src = json.load(open('/tmp/fanout-frags/M1-b.round22.json'))
PIN_NEW = '503d13980b2ad23201063107a2d6844e00b23d6d'
PREFIX_OLD = re.compile(r'^Carried from round 21 \(.*?none cited by this row\): ', re.S)
PREFIX_NEW = ('Carried from round 22 (course/modules/M/M1/L04.html cited lines, L05.html and cards.json '
              'byte-identical since the previous pin d160ac3; the round-23 delta changes only L04.html line 79, '
              'which no carried row cites): ')
FRESH_LINE79 = {'M1-b-2.9-structure-prose', 'M1-b-2.9-DAG', 'M1-b-r4-term-before-def-L04',
                'M1-b-r20-E-scope-remarks', 'M1-b-r21-E-list-complete', 'M1-b-r22-delta', 'M1-b-r22-E-lab1-dropped'}
CMD = {'M1-b-cmd-pin', 'M1-b-cmd-run_labs', 'M1-b-cmd-twins', 'M1-b-cmd-page_smoke', 'M1-b-cmd-check_pages_dag',
       'M1-b-cmd-lint-types', 'M1-b-cmd-refs', 'M1-b-cmd-pytest'}
fresh = {
 'M1-b-cmd-pin': ('repository HEAD; course/modules/M/M1/L04.html, L05.html, cards.json; tests/labs/M1/',
   'PASS', 'git rev-parse HEAD = 503d13980b2ad23201063107a2d6844e00b23d6d (out/pin.txt). Delta d160ac3..503d139 for the M1 slice: git diff --stat lists only course/modules/M/M1/L04.html (2 lines, +1 -1, line 79). L05.html, cards.json, tests/labs/M1 and tools are unchanged (git diff --quiet on tests/labs/M1 and tools: unchanged).'),
 'M1-b-cmd-run_labs': ('tools/run_labs.py --unit M1; course/modules/M/M1/L04.html; L05.html', 'PASS',
   'Command: .venv/bin/python tools/run_labs.py --unit M1, exit 0: "run_labs M1: PASS (11/11)" (out/run_labs.txt).'),
 'M1-b-cmd-twins': ('tests/labs/M1/lab-M1-L04-1.py; lab-M1-L05-1.py; course/modules/M/M1/L04.html <pre class=expected>; L05.html <pre class=expected>', 'PASS',
   'Each twin run from /tmp as /tmp/verify23-M1-b/.venv/bin/python -I -W error: exit 0, stderr 0 bytes (out/twin_L04.err, twin_L05.err). ledgers/M1/scripts/M1-b-r21/embed_cmp.py against the embedded blocks: "expected==twin: True 27 27" (L04) and "expected==twin: True 13 13" (L05). tests/labs/M1 unchanged in the delta.'),
 'M1-b-cmd-page_smoke': ('tools/page_smoke.py --unit M1 --pages L04 L05', 'PASS',
   'Exit 0: "page_smoke modules/M/M1/L05.html: PASS" and "page_smoke M1: PASS" (out/page_smoke.txt; the L04 line is in the same output file).'),
 'M1-b-cmd-check_pages_dag': ('tools/check_pages.py --unit M1; tools/check_dag.py --unit M1; tools/check_projects.py --unit M1', 'PASS',
   '"check_pages M1: PASS" (exit 0), "check_dag M1: PASS" (exit 0), "check_projects M1: PASS" (exit 0) (out/check_pages.txt, check_dag.txt, check_projects.txt).'),
 'M1-b-cmd-lint-types': ('tests/labs/M1/ (ruff, 11 files); lab-M1-L04-1.py, lab-M1-L05-1.py (mypy)', 'PASS',
   'ruff check tests/labs/M1: "All checks passed!" (exit 0). ruff format --check tests/labs/M1: "11 files already formatted" (exit 0). mypy --no-incremental on the two twins: "Success: no issues found in 2 source files" (exit 0). out/ruff_check.txt, ruff_format.txt, mypy.txt.'),
 'M1-b-cmd-refs': ('references/references.json; tools/verify_refs.py; L04.html:459-462; L05.html:472-475', 'PASS',
   'verify_refs.py --offline (exit 0): "offline integrity: 560 entries, 0 problems". verify_refs.py --unit M1 (exit 0): "live re-verification of M1: 1 of 560 entries, 0 problems". The references paragraphs at L04.html:460 and L05.html:473 cite no registry key (out/vr_offline.txt, vr_live.txt).'),
 'M1-b-cmd-pytest': ('tests/test_run_labs.py; tests/test_page_checks.py; tests/test_labs.py', 'PASS',
   'pytest -q on the three files: exit 0, one progress line of 30 dots, no F or E (out/pytest.txt).'),
 'M1-b-r22-E-lab1-dropped': ('course/modules/M/M1/L04.html:79 (list); line 117 (Lab 1 hypothesis)', 'PASS',
   'Resolved. Round-22 defect: "Lab 1" was dropped from the list. The round-23 edit (git diff d160ac3 503d139, L04.html line 79) inserts "the Lab 1 hypothesis" in the list. Line 117 names "Propositions 2.1 and 2.2", so the insertion is correct. Proposition 2.2 names on this page (grep "Proposition 2.2", "Remark 2.3", "Proposition 2.2"): line 75 (section 2 introduction), 101 (statement), 107 (its proof, uses Assumption E at x = r/m), 112 (Remark 2.3), 117 (Lab 1 hypothesis), 261 (misconception in s5, section 5 at line 249), 358 (R2), 378 (key results, section 7 at line 372), 425 (quiz item L04q5, section 8 at 387), 460 (references, section 9 at 459). All entries in the list are at those lines.'),
 'M1-b-r22-delta': ('course/modules/M/M1/L04.html:79; L05.html; cards.json; tests/labs/M1', 'PASS',
   'Delta d160ac3..503d139 (git diff --stat, M1 entries only): course/modules/M/M1/L04.html | 2 +- (line 79 only). No other M1 file changed in the delta (cards.json, L05.html, tests/labs/M1, tools/ unchanged). The AC1, AC4 and CF1 entries in the same stat are other slices and are not in this slice.'),
 'M1-b-2.9-structure-prose': ('course/modules/M/M1/L04.html and L05.html (changed line 79 re-read in full; full-page grep)', 'PASS',
   'Full-page grep -i over both pages (out/scan_words.txt) for roughly half, about 6%, historically, ellipsis, builder, verifier, round, REQUESTS, unit report, build, typically, usually, always, only, all: no banned phrase and no process word. Hits are code (ROUND_HALF_EVEN, lines 133/154 and 161/187), a quoted misconception (L04 260, "always add value"), and scope words already present: L04.html:79 "only through A1 to A3" (describes L03, which states the exponential through A1 to A3 at L03.html:56-63; L03.html:63 "Every proposition below follows from A1 to A3"), L04:218, L04:340, L05:243-353 and L05:464 ("but only at t = 1" in a quiz item, not changed). Line 79 contains no banned phrase or process word.'),
 'M1-b-2.9-DAG': ('tools/check_dag.py --unit M1 (re-run); L04.html:79 (changed line, no data-concept attribute)', 'PASS',
   'check_dag M1: PASS (exit 0, out/check_dag.txt). The changed L04.html:79 carries no data-concept attribute (sed -n 79p | grep -c data-concept = 0). Concept definitions are unchanged in the delta.'),
 'M1-b-r4-term-before-def-L04': ('course/modules/M/M1/L04.html:75 (first mention), 78-80 (Assumption E block), 52, 54-56, 59', 'PASS',
   'Assumption E is first named at line 75 ("stated as Assumption E in the next block"), a signpost to the block at 78-79. Line 79 (changed) uses Proposition 2.2 (statement at 101), Remark 2.3 (111), Lab 1 (116), Problem R2 (354), R3 (361), sections 5, 7, 9 and quiz item 5 as places to look. These are signposts to later definitions, not undefined terms. PASS.'),
 'M1-b-r21-E-list-complete': ('course/modules/M/M1/L04.html:79 (list), 75 and 460', 'PASS',
   'Round-21 row. Its residual Lab 1 omission is resolved (see M1-b-r22-E-lab1-dropped). The remaining list entries are checked by M1-b-r23-E-list-R3 below.'),
 'M1-b-r20-E-scope-remarks': ('L04.html:79 (list, Remark 2.3 entry), 112 (Remark 2.3); L05.html:127', 'PASS',
   'Remark 2.3 at line 112 ("Under Assumption E, Proposition 2.2 says that they stay below e^r") is in the list at line 79 and names Proposition 2.2 and Assumption E, consistent with the list. L05.html:127 unchanged in the delta.'),
}
fresh['M1-b-r23-E-list-R3'] = None
out_rows = []
for r in src['rows']:
    rid = r['id']
    if rid in fresh:
        loc, st, ev = fresh[rid]
        out_rows.append({'id': rid, 'check': r['check'], 'location': loc, 'status': st, 'evidence': ev})
        continue
    row = dict(r)
    if rid not in FRESH_LINE79 and rid not in CMD:
        ev = row['evidence']
        m = PREFIX_OLD.match(ev)
        if m:
            row['evidence'] = PREFIX_NEW + ev[m.end():]
        elif ev.startswith('Carried from round 21'):
            raise SystemExit('unmatched carry prefix: ' + rid)
    out_rows.append(row)
# Previous rows that were FRESH_LINE79 but not overridden above must be re-verified; stop if any remain
left = [r['id'] for r in out_rows if r['id'] in FRESH_LINE79 and r['evidence'].startswith('Carried')]
assert not left, left
out_rows.append({'id': 'M1-b-r23-E-list-R3', 'check': '2.9 scope, Assumption E list on L04.html:79 (named entries)',
  'location': 'course/modules/M/M1/L04.html:79 (list entry "the solution to Problem R3"); 361-367 (R3 solution)',
  'status': 'FAIL',
  'evidence': 'Line 79 says E "is used in Proposition 2.2 and in each other place on this page that names Proposition 2.2: ... the solution to Problem R3, ...". The R3 solution (lines 361-367) does not name Proposition 2.2: the text at 365-367 contains "A2", "A1", "x -> x^m", "e^{r/m} - 1 > r/m" and no "Proposition 2.2" (grep "Proposition 2.2" over the page lists lines 75, 101, 107, 112, 117, 261, 358, 378, 425, 460). The R3 solution uses Assumption E directly at x = r/m (line 367, "e^{r/m} - 1 > r/m"), which the closing sentence of line 79 states ("It is used directly in Problem R3"). So the entry is in a list the sentence defines as places that NAME Proposition 2.2, and R3 does not name it. Fix: remove "the solution to Problem R3," from the colon-list at line 79 (the closing sentence already covers R3), or change "names" to "uses". Witness: grep -n "Proposition 2.2" course/modules/M/M1/L04.html, with the sed -n 361,368p output (out/ in ledgers/M1/scripts/M1-b-r23/).'})
rows = out_rows
n_pass = sum(1 for r in rows if r['status'] == 'PASS'); n_fail = sum(1 for r in rows if r['status'] == 'FAIL')
frag = {
 'unit': 'M1', 'slice': 'M1-b', 'round': 23,
 'verifier': 'independent verifier (Haiku), round 23',
 'pin': PIN_NEW,
 'base': 'd160ac3 (round 22 pin; delta: course/modules/M/M1/L04.html line 79 only)',
 'previous_fragment': '/tmp/fanout-frags/M1-b.round22.json',
 'checkout': '/tmp/verify23-M1-b',
 'scratch': '/tmp/M1-v/M1-b-r23',
 'verified_at': '2026-10-28T12:00:00+00:00',
 'verdict': 'FAIL' if n_fail else 'PASS',
 'rows': rows,
 'mutants': [],
 'registry_flags': src.get('registry_flags', []),
 'freshness_flags': src.get('freshness_flags', []),
 'notes': [
  'Slice b is lessons L04 and L05 with their lab twins, not a project slice: no student-error mutants or alternative implementations apply (architect ruling, as in rounds 16-22). ledgers/M1/mutants/ holds the project mutants of slices a and c and is unchanged in this delta.',
  'Delta d160ac3..503d139 for slice b: course/modules/M/M1/L04.html line 79 only (git diff --stat). L05.html, cards.json, tests/labs/M1, tools and references are unchanged.',
  'Carried rows cite lines that are byte-identical to the previous pin (the delta touches only L04.html line 79, which no carried row cites). Rows citing L04.html:79 or whole-page L04 scans were re-verified fresh this round.',
  'Not checked: a full line-by-line re-read of every unchanged line of L04.html and L05.html (carried by byte-identity of the cited lines, as in rounds 16-22). Every command row was re-run this round on the 503d139 checkout.',
  'No external source is cited or read in this slice; the registry check is a live sample (1 of 560 entries) plus the full offline integrity pass.',
  'Round-22 FAIL row M1-b-r22-E-lab1-dropped is resolved (PASS). A new FAIL row M1-b-r23-E-list-R3 covers the R3 entry in the line 79 list, which does not name Proposition 2.2.'
 ],
 'summary': {'rows': len(rows), 'pass': n_pass, 'fail': n_fail, 'unverifiable': 0},
}
json.dump(frag, open('/tmp/fanout-frags/M1-b.round23.json', 'w'), indent=1, ensure_ascii=False)
print('rows', len(rows), 'pass', n_pass, 'fail', n_fail, 'verdict', frag['verdict'])
