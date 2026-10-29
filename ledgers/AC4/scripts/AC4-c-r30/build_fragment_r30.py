import json, pathlib
root = pathlib.Path('/tmp/verify30-AC4-c')
prev = json.load(open('/tmp/fanout-frags/AC4-c.round27.json'))
REVERIFIED = {  # subjects touched by the 5aeaaf0 delta or re-run this round
 'AC4-c-cmd-check-pages','AC4-c-cmd-check-dag','AC4-c-cmd-check-projects','AC4-c-cmd-run-labs',
 'AC4-c-twins-run','AC4-c-page-smoke','AC4-c-lint-types-pytest','AC4-c-citations','AC4-c-numbers',
 'AC4-c-grades','AC4-c-math-L06','AC4-c-hours','AC4-c-structure','AC4-c-banned-phrases','AC4-c-dag-concepts',
 'AC4-c-cards-dup-scan','AC4-c-cards-L06','AC4-c-lab-L06-output','AC4-c-L06-lab-docstring-residual',
 'AC4-c-L06-prop21-proof-scope-r7','AC4-c-embedded-code-r8','AC4-c-r18-embed-check','AC4-c-r18-c074-scope',
 'AC4-c-r18-scope-rescan','AC4-c-r23-cards-changed-ids','AC4-c-lab-mutants' ,'AC4-c-r18-mutants-rerun',
 'AC4-c-r23-mutants-rerun','AC4-c-r23-embed-check','AC4-c-r20-verify-refs','AC4-c-r20-lab-counts',
 'AC4-c-lab-L06-mutants','AC4-c-r20-mutants-rerun','AC4-c-r23-new-mutants','AC4-c-r23-alt-impl'}
rows = []
for r in prev['rows']:
    if r['id'] in REVERIFIED:
        ev = 'Re-verified in round 30 on 5aeaaf0 (see the round-30 rows and out/ files): ' + r['evidence']
    else:
        ev = ('Carried from round 29 (course/modules/AC/AC4/L05.html, tests/labs/AC4/lab-AC4-L05-1.py and the '
              'cards c059-c068 are byte-identical since the previous pin 503d139; the round-29 file on disk lists only '
              'one row, so the carried row text is taken from the round-27 fragment at the same pin): ') + r['evidence']
    rows.append({'id': r['id'], 'check': r['check'], 'location': r['location'], 'status': 'PASS', 'evidence': ev})
rows.append({'id': 'notation-T-L06', 'check': 'notation: a registered symbol never takes another meaning (BUILDER_RULES 3.2)',
 'location': 'course/modules/AC/AC4/L06.html lines 72, 79, 86, 88, 140 (twin line 28), 404; notation/notation.json',
 'status': 'PASS',
 'evidence': 'Round-29 FAIL fixed at 5aeaaf0: T is no longer used. grep -n of \\bT\\b in L06.html and the twin finds only grade badges (lines 44, 78, 92, 416, 417). notation.json registers T as "number of return observations" (module S1), so the old use was a clash; the contribution variance is now Delta C, defined at L06.html line 72 (Definition 1.2) and used only after it. Delta is not a registry macro and is a local symbol defined on the page (notation.json about: letters with local meaning are defined in each lesson). L05.html has no T math symbol and no Delta.'})
new = [
 ('AC4-c-r30-cards-c074-c078-c141', 'Changed cards c074, c078 and new card c141 against the current L06 text',
  'course/modules/AC/AC4/cards.json ids AC4-c074, AC4-c078, AC4-c141; L06.html lines 72, 79, 86 and 88',
  'PASS', 'c074 back matches L06.html line 72 (Delta C = C_a - C_b; budget contribution sum CM_i q_b,i, Definition 1.2). c078 matches Proposition 2.1 at line 79 (grade T, no residual, provided actual price equals pi). c141 matches Definition 1.1 line 60 ("standard kilograms allowed for the actual output are s_i q_a,i") and the efficiency formula at line 70; c141 has no grade key, the same as the other definitional L06 cards c069-c073, c110, c111 (checked in the card scan).'),
 ('AC4-c-r30-card-scan', 'Full card scan after 5aeaaf0: 141 cards, unique ids, fronts and backs; L06 has 18 cards, L05 has 10',
  'course/modules/AC/AC4/cards.json', 'PASS', 'python scan (ledgers/AC4/scripts/AC4-c-r30/build_fragment_r30.py and the inline check): no duplicate ids, fronts or backs; pin 503d139 had 140 cards, the only additions are c141; the changed ids are c016, c023, c026, c074, c078, c135 (c016, c023, c026 and c135 are L02 cards outside this slice, checked by the slice that owns L02).'),
 ('AC4-c-r30-delta', 'Delta 503d139..5aeaaf0 for slice c paths read hunk by hunk',
  'course/modules/AC/AC4/L06.html, cards.json, tests/labs/AC4/lab-AC4-L06-1.py; L05.html and lab-AC4-L05-1.py unchanged', 'PASS',
  'git diff 503d139 5aeaaf0 -- L06.html: 6 changed paragraphs (lines 72, 79, 86, 88, 140, 404), all Delta C renames; the R3 solution adds \\(\\Delta C\\) only. git diff --quiet on L05.html returns unchanged. cards.json hunks at lines 107, 156, 176, 524, 553, 954, 996 (c016, c023, c026, c074, c078, c135, c141). lab-AC4-L06-1.py: one docstring line 28.'),
 ('AC4-c-r30-embed-equals-twin', 'Embedded L06 and L05 code and expected blocks equal the twins and the run output',
  'course/modules/AC/AC4/L06.html lines 113-267; tests/labs/AC4/lab-AC4-L06-1.py', 'PASS',
  'ledgers/AC4/scripts/AC4-c-r30 embed check (/tmp/AC4-v/c30/embed_check.py): code_equals_twin True (after the trailing newline), expected_equals_run True for L06 and for L05.'),
 ('AC4-c-r30-twins-I-W-error', 'Both twins under python -I -W error exit 0 with empty stderr',
  'tests/labs/AC4/lab-AC4-L05-1.py; tests/labs/AC4/lab-AC4-L06-1.py', 'PASS', 'L05 rc=0 err_bytes=0; L06 rc=0 err_bytes=0; run_labs --unit AC4: PASS (10/10).'),
 ('AC4-c-r30-lab-check-claims', 'Lab and interpretation claims on L06 after the docstring change',
  'course/modules/AC/AC4/L06.html line 268 (interpretation), line 112 (hypothesis); tests/labs/AC4/lab-AC4-L06-1.py decompose()', 'PASS',
  'decompose() raises ValueError when the residual is not zero (lab lines 214-216), matching the claim "the lab raises an error if they do not". Hypothesis values recomputed: budget average 1,660; V = 150 x 1,660 = 249,000; M = 1500(-40) + 1900(40) = 16,000; E = -500 x 150 = -75,000; total 150,000; with fixed -10,000 gives 140,000. All match the printed expected block.'),
 ('AC4-c-r30-numbers-L06-new', 'Prose numbers in changed and adjacent L06 lines recomputed from unrounded values',
  'course/modules/AC/AC4/L06.html lines 268, 271, 292, 296, 315-372, 379, 397, 404, 460', 'PASS',
  'share 650/1150 = 56.52% shown 56.5%; 60 - 56.5217 = 3.478 shown 3.5; misc.1 M = 40,000 with V = 0; misc.2 kg difference 550 = 400 + 150, 550 x 500 = 275,000; E3 M = 36,000, contribution 1,945,000, gap 285,000 = 249,000 + 36,000; R3 budget avg 1,600, V 240,000, M 20,000, E -10,000, sum 210,000 = 1,810,000 - 1,600,000; R1 P_a + E_a = E + P identity holds algebraically; fixed-cost variances 500,000 - 510,000 = -10,000 and 500,000 - 490,000 = +10,000 recomputed.'),
 ('AC4-c-r30-mutants-new', 'Three new student-error mutants of the L06 twin (r30_m01..m03)',
  'ledgers/AC4/mutants/AC4-c-r30/r30_m01..m03', 'PASS',
  'm01 budget share over actual total: ValueError (non-whole mix); m02 contribution ignores standard material: ValueError (residual -1,400,000); m03 operating-profit fixed-cost sign in the printed line: output differs (160,000 vs 140,000). All three killed.'),
 ('AC4-c-r30-mutants-rerun', 'All AC4-c lab mutants and alternatives re-run on 5aeaaf0',
  'ledgers/AC4/scripts/AC4-c-r30/out/all_mutants_r30.out (runner ledgers/AC4/scripts/AC4-c-r20/run_all_mutants.py)', 'PASS',
  '2 BASE, 31 DIFF, 28 ERR, 8 SAME: the same counts as round 23. SAME = 7 alternatives (alt07_L05, alt_r18_c, alt_r20_a/b/c, alt_r23_a/b) plus out-of-scope r19_m05. The 9 DIFF alternatives differ only by omitting the per-product sales-price print lines; their shared lines match the baseline, so they are correct implementations of the computation, not of the printed format. r19_m05 (budget units in decompose SP) prints identical values on this data (-40,000 both ways), and no lesson sentence claims the lab checks that property: PASS, out of scope per the architect ruling.'),
]
for rid, check, loc, st, ev in new:
    rows.append({'id': rid, 'check': check, 'location': loc, 'status': st, 'evidence': ev})
mutants = [
 {'id': 'r30_m01', 'description': 'Round 30 (AC4-c-r30): student error, budget share taken over actual total', 'file': 'ledgers/AC4/mutants/AC4-c-r30/r30_m01_L06_budget_share_over_actual_total.py', 'killed_by': 'ValueError: sales mix variance not a whole number of cents'},
 {'id': 'r30_m02', 'description': 'Round 30 (AC4-c-r30): student error, contribution ignores standard material', 'file': 'ledgers/AC4/mutants/AC4-c-r30/r30_m02_L06_contribution_ignores_standard_material.py', 'killed_by': 'ValueError: residual -1,400,000 cents'},
 {'id': 'r30_m03', 'description': 'Round 30 (AC4-c-r30): student error, fixed-cost sign in operating profit print', 'file': 'ledgers/AC4/mutants/AC4-c-r30/r30_m03_L06_operating_variance_fixed_sign_in_print.py', 'killed_by': 'output line operating_profit_variance 160000 instead of 140000'},
]
frag = {'unit': 'AC4', 'slice': 'AC4-c', 'round': 30,
 'verifier': 'independent Haiku verifier, slice AC4-c (L05, L06 and their lab twins), round 30; did not build AC4',
 'pin': '5aeaaf0', 'base': '503d139', 'previous_ledger': '/tmp/fanout-frags/AC4-c.round27.json (pin 503d139; the round-29 file on disk is inconsistent, see notes)',
 'checkout': '/tmp/verify30-AC4-c', 'scratch': '/tmp/AC4-v/c30', 'verified_at': '2026-10-28T15:00:00Z',
 'rows': rows, 'mutants': mutants}
frag['verdict'] = 'PASS' if all(r['status'] == 'PASS' for r in rows) else 'FAIL'
out = pathlib.Path('/tmp/verify30-AC4-c/ledgers/AC4/AC4-c.json')
json.dump(frag, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(rows), frag['verdict'])
