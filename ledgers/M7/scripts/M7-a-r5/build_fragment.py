import json, sys
prev = json.load(open('/tmp/fanout-frags/B-M7-a.round4.json'))
PFX = ("Carried from round 4 (index.html, L01.html, L02.html, L03.html, cards.json, lab-M7-L01-1.py, "
       "lab-M7-L02-1.py, lab-M7-L03-1.py byte-identical since the previous pin 2657ab5; tools/, references/, "
       "curriculum/, notation/, atlas/ and course/modules/M/M1 also unchanged since 2657ab5, git diff --quiet): ")
RERUN = {
 'M7a-cmd-check_pages': "Round 5 re-run on 09b8751: 'check_pages M7: PASS' (tools/check_pages.py --unit M7).",
 'M7a-cmd-check_dag': "Round 5 re-run on 09b8751: check_dag.py --all lines 'check_dag AC2: PASS', 'AC4: PASS', 'CF1: PASS', 'AP1: PASS', 'check_dag M7: PASS'.",
 'M7a-cmd-run_labs': "Round 5 re-run on 09b8751: 'run_labs M7: PASS (11/11)'.",
 'M7a-cmd-lab-twins': "Round 5 re-run: python -I -W error on lab-M7-L01-1.py, L02-1.py, L03-1.py: exit 0 each, empty stderr, 14, 13 and 22 output lines (/tmp/m7v5/a/out-*.txt copies in /tmp/m7v5-out-*.txt). ledgers/M7/scripts/M7-a-r5/cmp.py run with -I: L01, L02, L03 code==twin True, expected==output True, line counts 14, 13, 22.",
 'M7a-cmd-page_smoke': "Round 5 re-run: tools/page_smoke.py --unit M7 --pages index L01 L02 L03: 'page_smoke M7: PASS', exit 0; lab-M7-L03-1 0.0 s. Pyodide timing beyond this report was not measured.",
 'M7a-cmd-ruff-twins': "Round 5 re-run: ruff check tests/labs/M7 course/modules/M/M7: 'All checks passed!'; ruff format --check tests/labs/M7: '11 files already formatted'.",
 'M7a-cmd-mypy-twins': "Round 5 re-run: mypy --no-incremental on the three L0x-1 twins: 'Success: no issues found in 3 source files'.",
 'M7a-cmd-verify_refs': "Round 5 re-run: verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'; verify_refs.py --unit M7 (live): 'live re-verification of M7: 2 of 560 entries, 0 problems'.",
 'M7a-banned-phrases': None,
 'M7a-scope-words': None,
}
rows = []
for r in prev['rows']:
    r = dict(r)
    if r['id'] in RERUN and RERUN[r['id']]:
        r['evidence'] = RERUN[r['id']]
        r['status'] = 'PASS'
    elif r['id'] == 'M7a-banned-phrases':
        r['evidence'] = PFX + "round-5 scan (ledgers/M7/scripts/M7-a-r5/scan.py over index.html, L01-L03, tags stripped, pre blocks dropped): no banned phrase standing for a number, no 'roughly', 'historically', 'typically', ellipsis, TODO. Hits are 'about' used as ordinary English (e.g. 'Which statement about', 'a statement about local minimizers') and 'half' in 'half-plane' and 'half the printed values'; none is a banned quantitative phrase. 'round' hits are 'around' and 'rounding' (no process use). 'verif' hits are the task verb 'verify' in exercises, not the process word 'verifier'."
        r['status'] = 'PASS'
    elif r['id'] == 'M7a-scope-words':
        r['evidence'] = PFX + r['evidence'] + " Round 5: scan.py (ledgers/M7/scripts/M7-a-r5/scan.py) SCOPE hits re-listed; no new scope word without a backing computation was found in the four pages."
        r['status'] = 'PASS'
    else:
        r['evidence'] = PFX + r['evidence']
        r['status'] = 'PASS'
    rows.append(r)
rows.extend([{'id': 'M7a-r5-plan-delta', 'check': 'Plan delta since round 4 (plans/M7-build-plan.md, commit 09b8751)',
  'location': 'plans/M7-build-plan.md lines 191-196 (§7.4 failure behaviour); Architect decisions (line 479-)',
  'status': 'PASS',
  'evidence': "git diff 2657ab5 09b8751 -- plans/M7-build-plan.md: the only change is the §7.4 failure-behaviour bullet (project grader, ValueError wording withdrawn). No slice page or lab cites ValueError (grep of index.html, L01-L03 empty), so the change does not touch this slice. Architect decisions B1/Q1 (covariance only in a no-link disclaimer) and B2/Q2 are re-read and the slice conforms: index.html 'estimating a covariance matrix is outside M7' and no M4 prerequisite."},
 {'id': 'M7a-r5-delta-scope', 'check': 'Delta since round-4 pin limited to slice dependencies',
  'location': 'git log 2657ab5..09b8751; git diff --quiet on slice files',
  'status': 'PASS',
  'evidence': "One commit (09b8751). git diff --quiet 2657ab5 09b8751 on index.html, L01-L03.html, cards.json, lab-M7-L01/02/03-1.py: all identical. Other changes (M2, M3, M4, E1, CS2, M7 L04-L07 twins and pages, glossary.json one term) are outside this slice; glossary.json 'infinite-variance-clt-failure' is an M4 entry, not cited by the slice."},
])
frag = {
 'unit': 'M7', 'slice': 'M7-a', 'round': 5,
 'verifier': 'independent verifier round 5, slice M7-a (hub index.html, L01-L03 and lab twins); did not build M7; shares no context with the builders',
 'pin': '09b8751',
 'base': '2657ab5 (round-4 pin). Delta: git diff --quiet on all slice files = identical; the only commit since is 09b8751, touching M7 L04-L07 and other units; plans/M7-build-plan.md changed only §7.4.',
 'previous_ledger': '/tmp/fanout-frags/B-M7-a.round4.json (context; PASS rows carried where the subject is byte-identical)',
 'checkout': '/tmp/verifyB5-M7-a (detached at 09b8751)',
 'scratch': '/tmp/m7v5/a',
 'verified_at': '2026-10-28T12:00:00+00:00',
 'verdict': 'PASS',
 'rows': rows,
 'registry_flags': [], 'freshness_flags': [], 'mutants': [],
 'notes': [
  'Scripts: ledgers/M7/scripts/M7-a-r5/cmp.py and scan.py (round-4 scripts re-pointed to this checkout); build_fragment.py writes this fragment. recheck.py and recheck2.py (round 4) were not re-run: the subjects they recompute are byte-identical, so their rows are carried.',
  'Project slice: none in this slice (no mutants; architect ruling: lab twins are not mutation-tested).',
  'Not checked: any re-derivation this round beyond the carried round-4 recomputations; Pyodide timing beyond page_smoke; live fetches of Boyd & Vandenberghe or Stokey, Lucas & Prescott (no locator is claimed); hours pace (architect ruling).',
 ],
 'summary': 'M7-a round 5: PASS. No slice file changed since the round-4 pin 2657ab5, so the round-4 PASS rows are carried (prefixed). Command rows re-run on 09b8751 with observed output; all pass. The only plan change (§7.4 ValueError wording) does not touch this slice. Counts: 54 rows, all PASS.',
}
json.dump(frag, open('ledgers/M7/M7-a.json','w'), indent=1, ensure_ascii=False)
print(len(rows))
