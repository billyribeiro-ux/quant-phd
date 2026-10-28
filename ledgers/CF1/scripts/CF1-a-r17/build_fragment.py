"""Build ledgers/CF1/CF1-a.json for round 17 from the prior fragment (carry rule applied per row)."""
import json, pathlib

ROOT = pathlib.Path('/tmp/verify17-CF1-a')
prior = json.loads(pathlib.Path('/tmp/fanout-frags/CF1-a.round16.json').read_text())
CARRY = ('Carried from round 16 (course/modules/CF/CF1/L01.html, L02.html, tests/labs/CF1/lab-CF1-L01-1.py, '
         'lab-CF1-L02-1.py, notation/notation.json and the cited cards entries byte-identical since the previous pin '
         '91946cf; the round-16 fragment file records that pin):')
OUT = 'ledgers/CF1/scripts/CF1-a-r17/out/'

over = {
    'CF1-a-gate-check-pages': ('PASS', f'{OUT}gates1.out: "check_pages CF1: PASS" (tools/check_pages.py --unit CF1, rc 0)'),
    'CF1-a-gate-check-dag': ('PASS', f'{OUT}gates1.out: check_dag AC1, AC2, AC4, CF1, AP1 all PASS (tools/check_dag.py --all)'),
    'CF1-a-gate-run-labs': ('PASS', f'{OUT}gates1.out: "run_labs CF1: PASS (9/9)"; twins run alone: {OUT}L01.out and {OUT}L02.out, python -I -W error, rc 0'),
    'CF1-a-gate-page-smoke': ('PASS', f'{OUT}gates1.out: index, L01, L02 page_smoke PASS; "page_smoke CF1: PASS"'),
    'CF1-a-gate-lint-types': ('PASS', 'ruff check tests/labs/CF1: All checks passed; ruff format --check: 9 files already formatted; mypy --no-incremental tests/labs/CF1: no issues in 9 files; ruff check . rc 0'),
    'CF1-a-gate-pytest': ('PASS', 'pytest -q tests/test_labs.py tests/test_page_checks.py tests/test_refs.py: rc 0 (all dots, no failures)'),
    'CF1-a-cite-verify-refs': ('PASS', 'tools/verify_refs.py --offline: 560 entries, 0 problems; tools/verify_refs.py --unit CF1: 2 of 560 entries, 0 problems'),
    'CF1-a-hub-lesson-map': ('PASS', 'index.html lines 138-139 (L01 and L02 cards) byte-identical since 91946cf; their titles equal the h1 of L01.html line 35 and L02.html line 35; the L05 card (line 142) is the separate row CF1-a-hub-L05-card'),
    'CF1-a-hub-ladder-worked-example': ('PASS', 'index.html line 151 (changed in this delta): "Lab 1 on the project page: a three-year project labelled SIMULATED (written for the module and describing no real company), ... NPV of 926.00 dollars at 10 percent (step 7)". project.html line 44 (rung 1 "Lab 1 below"), line 54 (Lab 1 heading), line 58 ("SIMULATED: a three-year machine project ... not any company\'s project"), line 128 output "step 7, NPV at 0.10: 926.00 dollars". Each step is printed on its own line (8 step prints in the lab code). index.html line 152 (rung 2): "Lab 2 on the project page ... three blanks": project.html lines 136 and 141-170 show three "___" blanks (lines 29-31 of the lab code, i.e. tax, operating, working_capital), and line 136 says the output matches the expected output when the three blanks are right. Not stated: any claim beyond these'),
    'CF1-a-hub-L05-card': ('FAIL', 'index.html line 142 (changed in this delta; title now "Payback and Its Discounted Form", equal to L05.html line 36 h1: PASS). Body: "...what payback ignores after the cut-off..." L05.html line 228 says payback "ignores flows after its year" (Proposition 2.1), and line 231 defines "the cut-off" as the number of years the firm sets for acceptance ("The payback rule accepts a project when its payback is below a number of years that the firm sets"). So the card uses "cut-off" for the payback year, a different meaning from L05 line 231'),
    'CF1-a-hub-scope-simulated': ('PASS', 'Carried from round 16 (course/modules/CF/CF1/index.html line 161 byte-identical since 91946cf): carried; L01.html and L02.html lines unchanged'),
    'CF1-a-scope-words': ('PASS', 'index.html lines 151-152 (changed): scope words "each", "including", "that same project" (project.html line 139: "the same three-year machine project as the worked example", true); no only/all/always/as much as/drives/offsets/raises; L02.html line 508 unchanged since 91946cf'),
    'CF1-a-L01-banned-process': ('PASS', 'index.html lines 151-152 (changed) scanned: grep for roughly half, about 6%, historically, ellipsis, build, builder, round, verifier, REQUESTS, unit report, returned no match (exit 1 for the scan). L01.html and L02.html unchanged since 91946cf'),
    'CF1-a-cards-L01-L02': ('PASS', 'course/modules/CF/CF1/cards.json, entries of L01 and L02 compared by id with 91946cf: changed CF1-c023 and CF1-c027, new CF1-c101 and CF1-c104 (all L02). Re-verified: c023 back equals L02.html line 106 (Corollary 2.3, "adds over and above the after-tax EBITDA"); c027 "534.24" printed by Lab 2 line 269 and "sunk study, paid in every scenario" at L02.html line 153 and 379; c101 "-1,465.76" printed by lab line 270, difference 2000.00 (line 88 output "difference, in dollars: 2000.00"), L02.html line 296 "That figure is the study cost, not a future cash effect"; c104 "adds no cash of its own" L02.html line 106. No duplicate fronts or backs in cards.json (109 cards). Unchanged entries CF1-c001..c022, c024..c026, c028..c032, c089, c090: Carried from round 16 (byte-identical entries since 91946cf)'),
    'CF1-a-mutants': ('PASS', 'ledgers/CF1/scripts/CF1-a-r17/run_mut.py run on 59 prior lab mutants (CF1-a-r7..r11, 57 killed, 2 survive: CF1-a-r9 r9_m07 and CF1-a-r11 n05, both out of scope, see CF1-a-r11-survivors) and 4 new mutants (CF1-a-r17), all killed; the probe r17_probe survives and is out of scope (see CF1-a-r17-new-mutants)'),
    'CF1-a-r11-survivors': ('PASS', 'Carried from round 16 for r9_m07 and n05 (unchanged files): out of scope; re-run in ' + OUT + 'mutants_prior.out. The new probe r17_probe_l02_identity_exact_equality also survives and is out of scope: exact float equality prints True for this seeded data, so its output is equivalent, and the page claims nothing about the tolerance'),
    'CF1-a-r11-alt-implementations': ('PASS', 'tests/labs/CF1/lab-CF1-L02-1.py and the three alternatives in ledgers/CF1/scripts/CF1-a-r17/alts/ (1e-9 identity tolerance, Horner-form NPV, 1e-4 shield tolerance): each prints output identical to the twin (run with python -I -W error, see the tool output in the round-17 notes)'),
}
for r in prior['rows']:
    if r['id'] in over:
        status, ev = over[r['id']]
        r['status'] = status
        r['evidence'] = ev
        r['check'] = r['check']
        if status == 'FAIL':
            r['fix'] = ('Change the L05 card body in course/modules/CF/CF1/index.html line 142 to say "what payback ignores after its payback year" '
                        '(the payback year, as in L05.html line 228), or define the term cut-off first; regenerate with tools/build_site.py '
                        'if the hub is generated, and re-run tools/build_site.py --check')
    else:
        r['evidence'] = CARRY + ' ' + r['evidence']

rows = prior['rows']
new_rows = [
    {'id': 'CF1-a-r17-delta', 'check': 'Delta since the previous pin 91946cf for every slice file (hub, L01, L02, twins, notation, cards, plan)',
     'location': 'git diff --stat 91946cf fefbf8b on course/modules/CF/CF1/{index,L01,L02}.html, tests/labs/CF1/lab-CF1-L01-1.py, lab-CF1-L02-1.py, notation/, cards.json',
     'status': 'PASS',
     'evidence': 'Changed slice files: index.html lines 142 (L05 card title and body unchanged except title), 151-152 (ladder rungs 1 and 2); cards.json entries CF1-c023, c027 (changed), CF1-c101, c104 (new L02). L01.html, L02.html, both L01/L02 twins and notation/notation.json: no diff. Out of slice and not judged here: L03..L06, project.html, grader, cards of other lessons, plans/CF1-build-plan.md section 12, tests/labs/AC1 and CF1-L05 twins.'},
    {'id': 'CF1-a-r17-new-mutants', 'check': 'At least three new student-error mutants of the L02 twin, and the mutant set re-run',
     'location': 'ledgers/CF1/mutants/CF1-a-r17/r17_m01..r17_m04 (killed), r17_probe (survives, out of scope); ledgers/CF1/scripts/CF1-a-r17/make_new.py',
     'status': 'PASS',
     'evidence': 'Four new student-error mutants, each a single replacement asserted to match once, all KILLED by run_mut.py (stdout differs from the twin): r17_m01 study charged at its present value (NPV line -1465.76 changes), r17_m02 shield printed in cents (line "depreciation shield per year" shows 75000.00 instead of 750.00), r17_m03 difference sign flipped (line shows -2000.00), r17_m04 cost draw range off by one (draws change). The exact-equality probe survives because the printed True stays True for this seeded data; it is an equivalent output, not a student error that the page describes, so it is out of scope.'},
    {'id': 'CF1-a-r17-alt-implementations', 'check': 'Three correct alternative implementations of the L02 lab functions print the twin output',
     'location': 'ledgers/CF1/scripts/CF1-a-r17/alts/alt_r17_a_tolerance_1e9.py, alt_r17_b_horner_npv.py, alt_r17_c_shield_from_difference_tolerance_1e4.py',
     'status': 'PASS',
     'evidence': 'Run with python -I -W error: rc 0 and stdout identical to the L02 twin for all three (different tolerances 1e-9 and 1e-4; Horner-form NPV).'},
    {'id': 'CF1-a-r17-gate-tests-wide', 'check': 'Full ruff check and pytest for the three relevant test files',
     'location': 'ruff check . ; pytest tests/test_labs.py tests/test_page_checks.py tests/test_refs.py',
     'status': 'PASS',
     'evidence': 'ruff check . rc 0; pytest rc 0. The full repository mypy and the full pytest suite were not run (only the CF1 lab twins under mypy).'},
    {'id': 'CF1-a-r17-changed-card-numbers', 'check': 'Every number in the new and changed L02 cards appears in L02.html or in the printed Lab 2 output',
     'location': 'cards.json CF1-c023, c027, c101, c104; L02.html line 269-270, 296, 153, 106; ledgers/CF1/scripts/CF1-a-r17/out/L02.out',
     'status': 'PASS',
     'evidence': 'Printed Lab 2 output: "NPV at 0.08 of the incremental flows, in dollars: 534.24", "...charged...: -1465.76", "difference, in dollars: 2000.00", "depreciation shield per year, in dollars: 750.00". 534.24 - 2000.00 = -1465.76 (arithmetic checked).'},
    {'id': 'CF1-a-r17-hub-prose-scope', 'check': 'Hub ladder rung text names the right lab and project page',
     'location': 'index.html lines 151-152; project.html lines 44-45, 54, 58, 128, 135-136',
     'status': 'PASS',
     'evidence': 'Rung 1 and rung 2 name Lab 1 and Lab 2 "on the project page", which is project.html (its own labs are "Lab 1 below" and "Lab 2 below"). The rung text gives no number beyond 926.00, which is printed at project.html line 128.'},
]
rows = rows + new_rows
# Rows changed in the hub previously referenced "Lab 2 prints the later years" - no longer present (checked by grep).

mutants = prior['mutants'] + [
    {'id': 'm03-r17-' + n, 'file': f'ledgers/CF1/mutants/CF1-a-r17/{f}', 'description': d, 'killed_by': 'round 17 run_mut.py: stdout differs from twin (killed)'}
    for n, f, d in [
        ('m01', 'r17_m01_l02_study_charged_at_present_value.py', 'L02 lab: sunk study charged at its present value, not its face value (new, round 17)'),
        ('m02', 'r17_m02_l02_shield_printed_in_cents.py', 'L02 lab: depreciation shield printed in cents, not dollars (new, round 17)'),
        ('m03', 'r17_m03_l02_difference_sign_flipped.py', 'L02 lab: difference line subtracts the incremental NPV from the charged NPV (new, round 17)'),
        ('m04', 'r17_m04_l02_cost_draw_range_off_by_one.py', 'L02 lab: operating-cost draws use randrange(20, 30), excluding the top value (new, round 17)'),
    ]
]
fragment = {
    'unit': 'CF1', 'slice': 'CF1-a', 'round': 17,
    'verifier': 'independent Haiku verifier, round 17, slice CF1-a (hub index.html, L01, L02 and their lab twins); did not build CF1 and shares no context with the builders',
    'pin': 'fefbf8b',
    'base': '91946cf (last verified pin of this slice; the file /tmp/fanout-frags/CF1-a.round16.json records that pin and round 11 content, not round 16, so it was used as the base). Delta: git diff 91946cf fefbf8b for the slice files, see row CF1-a-r17-delta.',
    'previous_fragment': '/tmp/fanout-frags/CF1-a.round16.json (context only; PASS rows carried only where the cited subject is byte-identical since 91946cf; changed subjects re-verified)',
    'checkout': '/tmp/verify17-CF1-a',
    'scratch': 'ledgers/CF1/scripts/CF1-a-r17/out (outputs of this round)',
    'verified_at': '2026-10-28T12:00:00+00:00',
    'verdict': 'FAIL',
    'rows': rows,
    'mutants': mutants,
    'registry_flags': [],
    'freshness_flags': [],
    'notes': [
        'Round 17 FAIL: one row, CF1-a-hub-L05-card (index.html line 142): the card says payback "ignores after the cut-off", but L05 uses "the cut-off" for the acceptance threshold and says payback ignores flows after its payback year (L05.html lines 228, 231).',
        'Mutants: 59 prior lab files re-run: 57 killed, 2 out-of-scope survivors (r9_m07 no tax credit, n05 identity check stubbed to True; both recorded in CF1-a-r11-survivors). 4 new student-error mutants killed. 1 probe (exact float equality) survives and is equivalent for this data.',
        'Not checked in this round: the full read of L01.html and L02.html (unchanged since 91946cf, carried by the byte-identical rule); the full repository mypy and pytest suite; the live reference check was run for CF1 only; no learner trial; hour figures were not re-judged (architect ruling).',
        'Out of this slice and not judged: L03..L06 cards and pages, project.html, the grader, plans/CF1-build-plan.md section 12 wording, AC1 lab twin (lab-AC1-L03-1.py) and CF1 L05 twin.',
    ],
    'summary': 'Slice CF1-a round 17 (pin fefbf8b, delta from 91946cf): FAIL, one row (CF1-a-hub-L05-card). All gates re-run PASS. Changed subjects re-verified: hub ladder rungs (lines 151-152), cards c023, c027, c101, c104. Mutants: 64 lab files run, 61 killed, 3 out-of-scope survivors.',
}
out = ROOT / 'ledgers/CF1/CF1-a.json'
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + '\n')
print('rows', len(rows), 'mutants', len(mutants))
