import json, sys
PREV = '/Users/billyribeiro/.fanout/frags/E-SC1-a.round9.json'
OUT = '/Users/billyribeiro/.fanout/wt/verifyE10-SC1-a/ledgers/SC1/SC1-a.json'
prev = json.load(open(PREV, encoding='utf-8'))
CHANGED = ['index.html', 'L02.html', 'L03.html', 'cards.json']  # changed since c93dd52 in this slice
PREV_PIN = 'c93dd52'
FRESH_PREFIX = 'Round 10 FRESH (full re-read of the slice at 00a8479; line numbers of the slice files unchanged by the delta, which replaced lines one for one): '
CARRY_PREFIX = ('Carried from round 9 (course/modules/SC/SC1/L01.html and tests/labs/SC1/lab-SC1-L01-1.py '
                'byte-identical since the previous pin c93dd52): ')
GATE_IDS_RERUN = {'SC1a-gate-check-pages', 'SC1a-gate-check-dag', 'SC1a-gate-run-labs', 'SC1a-gate-page-smoke',
                  'SC1a-gate-lint-types-tests', 'SC1a-gate-verify-refs', 'SC1a-r7-gate-check-projects',
                  'SC1a-r7-katex-render', 'SC1a-r7-forward-refs-L01-s4'}
REPLACE = {}   # id -> (status, check, location, evidence, fix)

REPLACE['SC1a-hub-concept-list'] = (
    'FAIL', 'Hub From-M6 list covers every prerequisite concept the module links, and nothing else',
    'course/modules/SC/SC1/index.html:66 (From M6 list); course/modules/SC/SC1/L04.html:37 (Uses line)',
    'Round 10: the OST entry is gone from index.html:66, and no SC1 page links or names the optional-stopping theorem '
    '(grep for optional/stopping: L04.html:232 says it is not used; L03.html:260 is the word "optional" in "Independence is '
    'not optional"). That part now PASSES. A new gap remains: L04.html:37 links data-concept="conditional-expectation-l2" '
    '("the conditional expectation in L2 of M6"), which is M6-introduced (curriculum/01-foundations.yaml:278) and is not in '
    'the hub From-M6 list, although index.html:33 and :54 say the concepts the module uses are linked from that section. '
    'Checked: the other 22 data-concept targets of the hub and the 8 SC1-defined concepts (L01:59, L02:64-68, L03:59, L04, '
    'L05, L06, L07, L08 dfn tags) match curriculum SC1 introduces (curriculum/03-markets.yaml:513-524).',
    'Add "conditional expectation (conditional-expectation-l2)" to the From M6 list at index.html:66, with its concepts.html '
    'anchor; then rerun tools/check_dag.py --all and tools/check_pages.py --unit SC1.')

REPLACE['SC1a-r9-quiz-L02-q3-explanation'] = (
    'PASS', 'L02 quiz item 3 explanation: the bound stated is correct and matches Proposition 2.4 Step 2',
    'course/modules/SC/SC1/L02.html:489; L02.html:161 (Step 2)',
    'Round 10 FRESH: L02.html:489 now says Step 2 bounds M_m by sqrt(2 log 2) m r^m with r = 2^(-1/2) (matches L02.html:161 '
    'exactly), and that sqrt(m) 2^(-m/2) <= m r^m for m >= 1 (true: sqrt m <= m and r^m = 2^(-m/2)), so the constant 1 bound '
    'holds for the term. Round-9 FAIL cleared.')

REPLACE['SC1a-r9-hub-ost-card-L04'] = (
    'PASS', 'L04 card on the hub agrees with the current L04 text (no optional-stopping claim)',
    'course/modules/SC/SC1/index.html:155 (L04 card body); course/modules/SC/SC1/L04.html:51, :232',
    'Round 10 FRESH: card at index.html:155 is "The filtration of Brownian motion, the martingales B_t, B_t^2-t and the '
    'exponential martingale." L04.html:51 proves those three martingales; L04.html:232 says the optional-stopping theorem is '
    'not used. Card and lesson agree. Round-9 FAIL cleared.')

REPLACE['SC1a-r9-hub-reflection-assumptions'] = (
    'PASS', 'Hub lede and L06 card state the reflection assumptions as the L06 text does (A3 and A4, fixed time only)',
    'course/modules/SC/SC1/index.html:33 (lede), :157 (L06 card); course/modules/SC/SC1/L06.html:118-119 (Definition 2.2), :123 '
    '(Proposition 2.3), :148 (Remark 2.4), :153 (Theorem 2.5)',
    'Round 10 FRESH: L06.html:118-119 says the path-level reflection is not proved and that A3 covers bounded times only; Proposition '
    '2.3 (L06.html:123) is the fixed-time law statement under A3 and A4(b),(c),(g),(h); Theorem 2.5 (L06.html:153) is the '
    'fixed-time tail identity under A3 and A4; Remark 2.4 (L06.html:148) says the path-level statement is not claimed. The hub '
    'lede (index.html:33) and L06 card (index.html:157) say exactly that. Round-9 FAIL cleared.')

REPLACE['SC1a-r9-hub-objective-reflection-proof'] = (
    'PASS', 'Hub objective 6 names the fixed-time identity it proves, with its lesson locator',
    'course/modules/SC/SC1/index.html:54 (objective 6); course/modules/SC/SC1/L06.html:153',
    'Round 10 FRESH: index.html:54 says "Prove the fixed-time reflection identity for Brownian motion (Lesson 6, Theorem 2.5), '
    'under Assumptions A3 and A4"; L06.html:153 is that Theorem 2.5. Round-9 FAIL cleared.')

REPLACE['SC1a-r10-card-L05-ck-wording'] = (
    'FAIL', 'Hub L05 card agrees with the L05 text on how Chapman-Kolmogorov is proved',
    'course/modules/SC/SC1/index.html:156 (L05 card body); course/modules/SC/SC1/L05.html:7 (meta description), :52 (why it '
    'matters), :146-150 (Theorem 2.1 proof)',
    'The card says the identity is "proved by Gaussian convolution". The lesson says "proved by completing the square" (L05.html:7 '
    'and :52) and its Theorem 2.1 proof (L05.html:146-150) completes the square and applies A4(e). The word "convolution" does '
    'not occur in L05.html (grep, 0 hits). The card and the lesson disagree on the method.',
    'Change index.html:156 to "...the Chapman-Kolmogorov identity proved by completing the square..." (the cards.json entry for '
    'the L05 quiz, if any, should match).')

REPLACE['SC1a-r10-A1-attribution-M4'] = (
    'FAIL', 'Assumption A1 is attributed to M4; each part is one M4 states',
    'course/modules/SC/SC1/L01.html:71 (block title "facts from M4, used without proof"), :74-78 (parts a-e); '
    'ledgers/SC1/scripts/SC1-a-r10/ (search); cards.json entries for A1 (c206-c210)',
    'Round 10 search of course/modules/M/M4/L01-L10.html for the statements of A1 parts: (a) general integrable independence: '
    'M4/L04.html states E[XY]=E[X]E[Y] only for finitely-valued variables (Proposition 1.5, "finitely many values" 10 hits; '
    '"integrable" 0 hits in L04); (c) jointly normal, zero covariance, then independent: no statement found (M4/L08 uses '
    '"uncorrelated" for marginal normal coordinates and says zero covariance does not give independence); (d) pointwise limit of '
    'random variables on a measurable event is a random variable: no statement found ("measurable" 0 hits in M4 L01-L10); (e) '
    'functions of disjoint subfamilies of an independent family are independent: no statement found ("disjoint subfamil" 0 hits, '
    '"grouping" only in regrouping finite sums). Part (b) was not checked. The page itself says (d) is a measurability fact and (e) a '
    'fact about independent families, so the M4 title is not supported for (a), (c), (d), (e) as stated. This is a search of the M4 '
    'text, not a full read of M4.',
    'Retitle A1 so that each part names its source (M4 for the finite-valued product rule and the multivariate normal part '
    'where M4 states it; measure theory or a numbered Assumption for (d) and (e)), or state the integrable and jointly normal '
    'forms as numbered Assumptions with no M4 attribution. Regenerate cards c206-c210 from the same text.')

GATE_ROWS = []
def gate(id_, check, location, evidence):
    GATE_ROWS.append({'id': id_, 'check': check, 'location': location, 'status': 'PASS', 'evidence': evidence})

gate('SC1a-r10-cmd-check_pages', 'tools/check_pages.py --unit SC1', 'index, L01-L03, cards.json, project.html',
     'Round 10 FRESH at 00a8479: .venv/bin/python tools/check_pages.py --unit SC1 -> "check_pages SC1: PASS", exit 0 '
     '(ledgers/SC1/scripts/SC1-a-r10/check_pages_SC1.out).')
gate('SC1a-r10-cmd-check_dag', 'tools/check_dag.py --all', 'index, L01-L03',
     'Round 10 FRESH: "check_dag SC1: PASS" and all units PASS, exit 0 (ledgers/SC1/scripts/SC1-a-r10/check_dag.out).')
gate('SC1a-r10-cmd-check_projects', 'tools/check_projects.py --unit SC1', 'project.html (unit gate)',
     'Round 10 FRESH: "check_projects SC1: PASS", exit 0 (check_projects_SC1.out).')
gate('SC1a-r10-cmd-run_labs', 'tools/run_labs.py --unit SC1', 'lab-SC1-L01-1, L02-1, L03-1 (and project labs)',
     'Round 10 FRESH: "run_labs SC1: PASS (11/11)", exit 0 (run_labs_SC1.out).')
gate('SC1a-r10-cmd-page_smoke', 'tools/page_smoke.py --unit SC1 --pages index L01 L02 L03', 'index, L01, L02, L03',
     'Round 10 FRESH, run alone: index, L01, L02, L03 each PASS (zero console errors, zero unrendered math, labs match in '
     'Pyodide, figure sweep), "page_smoke SC1: PASS", exit 0 (page_smoke_a.out).')
gate('SC1a-r10-cmd-twins-python-I-W-error', 'python3 -I -W error on each L01-L03 twin', 'tests/labs/SC1/lab-SC1-L01-1.py, L02-1, L03-1',
     'Round 10 FRESH: all three twins exit 0 with empty stderr (twin_L01/L02/L03.err are 0 bytes; the stdout equals the page '
     'expected block by exact comparison, see mutant_kill_r10.out baseline lines).')
gate('SC1a-r10-cmd-verify_refs', 'tools/verify_refs.py --offline', 'course/modules/SC/SC1/index.html:182 (data-cite)',
     'Round 10 FRESH: "offline integrity: 560 entries, 0 problems", exit 0 (verify_refs_offline.out).')
gate('SC1a-r10-cmd-ruff-mypy', 'ruff check and ruff format --check tests/labs/SC1; mypy --no-incremental on the L01-L03 twins',
     'tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py',
     'Round 10 FRESH: "All checks passed!", "11 files already formatted", "Success: no issues found in 3 source files" (ruff.out, mypy.out).')
gate('SC1a-r10-cmd-pytest-SC1', 'pytest -q tests/test_labs.py tests/test_page_checks.py -k SC1',
     'tests/test_labs.py, tests/test_page_checks.py (SC1 cases)',
     'Round 10 FRESH: 11 passed, exit 0 (pytest_SC1.out).')
gate('SC1a-r10-lab-mutants-4of4', 'Four student-error lab mutants of the L01-L03 twins, each compared with the page expected block',
     'ledgers/SC1/mutants/SC1-a-r10/mut-L01-1.py, mut-L02-1.py, mut-L03-1.py, mut-L03-2.py',
     'Round 10 FRESH: baseline twins match their page expected blocks exactly (rc 0). Killed 4 of 4: L01 covariance uses '
     't/2**(n+1) (first diff "sum to 1/2" vs "sum to 1"); L02 level scale 2**(-m/2) (grid-supremum line False); L03 se divisor '
     'n+1 (z = 2.40 vs 2.39); L03 exact sum offset 1e-9 (closed-form matches False). Lab mutants are demonstrations, not graded.')

NEWPASS = []
def newpass(id_, check, location, evidence):
    NEWPASS.append({'id': id_, 'check': check, 'location': location, 'status': 'PASS', 'evidence': evidence})

newpass('SC1a-r10-L02-E3-unrounded', 'L02 E3: unrounded |xi_(1,1)| and the level-1 bound',
        'course/modules/SC/SC1/L02.html:421 (E3); tests/labs/SC1/lab-SC1-L02-1.py',
        'Round 10 FRESH: recomputed with the lab seed (random.Random(20260101), xi0 then coefficients): |xi_(1,1)| = 0.23317868947886533, '
        'so the level-1 sup = 0.11658934..., printed 0.116589; twice the unrounded value 0.2331787 rounds to 0.233179, while twice '
        'the printed digits gives 0.233178 (the prose at :421 is right). sqrt(4 log 2)/2 = 0.8325546 -> 0.832555 (printed bound).')
newpass('SC1a-r10-L02-quiz-q3-math', 'L02 quiz item 3 and the explanation sqrt(m)2^(-m/2) <= m r^m',
        'course/modules/SC/SC1/L02.html:483-489',
        'Round 10 FRESH: sqrt(m) <= m for m >= 1 and r^m = 2^(-m/2), so sqrt(m) 2^(-m/2) <= m r^m; Step 2 at L02.html:161 bounds M_m by '
        'sqrt(2 log 2) m r^m; sum m r^m = r/(1-r)^2 finite. Correct option at L02.html:486 holds.')
newpass('SC1a-r10-L03-key-results-14pct', 'L03 key-results row: se agrees with H sqrt(2/N)/20 within 14 percent; largest gap 13.2 percent at H=2, N=1',
        'course/modules/SC/SC1/L03.html:398; tests/labs run output (run_labs_SC1.out, twin_L03.out)',
        'Round 10 FRESH, computed from the printed se values and H sqrt(2/N)/20: H=2,N=1: 0.1601/0.141421 = 1.1320 (+13.2 percent, largest); '
        'the other gaps are between -6.6 and +9.2 percent (H=2) and between -1.6 and +7.6 percent (H=1). Within 14 percent holds.')
newpass('SC1a-r10-L03-why-sample-means', 'L03 why-it-matters says the lab prints sample means with standard errors',
        'course/modules/SC/SC1/L03.html:51; tests/labs/SC1/lab-SC1-L03-1.py:69-74',
        'Round 10 FRESH: the twin prints "mean ... over 400 simulated paths" and "mean {mean}, se {se}" (lines 69 and 74); the '
        'sentence at L03.html:51 says sample means with standard errors. Matches.')
newpass('SC1a-r10-L03-R3-hypothesis', 'L03 R3 solution names the failing hypothesis (H1) consistently with Theorem 2.3',
        'course/modules/SC/SC1/L03.html:382 (R3 solution), :99-103 (Theorem 2.3 hypotheses)',
        'Round 10 FRESH: L03.html:382 says Hypothesis (H1) fails (increments not independent, so not standard BM) and (H2) does not '
        'apply; Theorem 2.3 (L03.html:101-102) has (H1) standard BM and (H2) Assumption 3.2. Var(Q)=2t^2 (Lemma 2.2) is right.')
newpass('SC1a-r10-hub-prereq-curriculum', 'Hub prerequisite chain and closure match the curriculum',
        'course/modules/SC/SC1/index.html:35, :58-68; curriculum/01-foundations.yaml:87-91, :122-126, :190-194, :230-234, :265; curriculum/03-markets.yaml:509',
        'Round 10 FRESH: SC1 prereqs [M6]; M6 prereqs [M4, M5]; M4 prereqs [M2]; M5 prereqs [M2]; M2 prereqs [M1]; M1 prereqs [P0.1]. '
        'Closure M1, M2, M4, M5, M6, P0.1 as the hub states.')
newpass('SC1a-r10-hub-concept-count', 'Hub: SC1 defines eight concepts, each once, in the assigned lesson',
        'course/modules/SC/SC1/L01.html:59, L02.html:68, L03.html:59, L04-L08 dfn tags; curriculum/03-markets.yaml:513-524',
        'Round 10 FRESH: eight dfn tags, one each: brownian-motion (L01), brownian-motion-construction (L02), quadratic-variation (L03), '
        'continuous-time-martingale (L04), markov-property (L05), reflection-principle (L06), running-maximum-distribution (L07), '
        'first-passage-time (L08). Curriculum introduces lists the same eight, in the same lesson order.')
newpass('SC1a-r10-hub-rung2-count', 'Hub skill check 2 explanation: the rung-2 check prints 29 for n=6, a=2',
        'course/modules/SC/SC1/index.html:143; course/modules/SC/SC1/project.html:206; tests/labs/SC1/lab-SC1-project-2.py',
        'Round 10 FRESH: enumeration of 2^6 walks gives max>=2: 29; ends>=2: 22; ends>=3: 7; 22+7 = 29 (python -I). The hub '
        '(index.html:143) and project.html:206 both print 29.')
newpass('SC1a-r10-hub-hours-sum', 'Hub hours: 8 lessons x 9 h = 72, project 28 = sum of rung hours',
        'course/modules/SC/SC1/index.html:29, :39-42, :150; L01-L08 data-hours; project.html:272-280',
        'Round 10 FRESH: data-hours="9" on each of L01..L08 (grep); 8 x 9 = 72 = data-hours-lessons; project time table rows 2+3+10+8+3+2 = 28 '
        '(project.html:272-280) = data-hours-project = the hub "28 h project" (index.html:29).')
newpass('SC1a-r10-hub-lede-path-level', 'Hub lede: reflection proved in fixed-time form only; path-level not proved',
        'course/modules/SC/SC1/index.html:33; course/modules/SC/SC1/L06.html:118-119, :148',
        'Round 10 FRESH: L06.html:118-119 (Definition 2.2) "On this page the path-level statement is not proved. Only its fixed-time form is '
        'proved"; L06.html:148 (Remark 2.4) says the path-level statement is not claimed. Hub lede matches.')
newpass('SC1a-r10-notation-collisions', 'SC1 slice symbols against notation/notation.json (T, Phi, R_f, R^ast, Q) and macros',
        'course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html; notation/notation.json',
        'Round 10 FRESH: no slice use of T, Phi, gamma_3, gamma_4, R_f, R^ast, R^{e ast} or \\mathbb{Q}. L03 uses Q for the quadratic '
        'variation and R as an integration bound (L03.html:84) with no registry entry. Registered macros used: \\E, \\Prob, \\Var, '
        '\\Cov, \\Normal, \\indic; other LaTeX commands are standard. \\mathbb Z at L02.html:71 is a standard integer symbol with no collision.')
newpass('SC1a-r10-process-words', 'No process words in learner text of the four slice pages',
        'course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html',
        'Round 10 FRESH: grep for round, verifier, builder, reviewer, audit, revised, previous version, TODO, placeholder: 0 hits.')
newpass('SC1a-r10-cards-dup-hypotheses', 'Cards for L01-L03: no duplicate, hypotheses carried, numbers appear in lesson',
        'course/modules/SC/SC1/cards.json (ids c001-c060, c184-c188, c206-c213, c219); lessons',
        'Round 10 FRESH: no duplicate ids or fronts; token-overlap scan (Jaccard > 0.45) finds no duplicate pair in L01-L03 cards '
        '(its only high pairs are in L04-L08 cards). Hypotheses named on Proposition/Lemma/Theorem cards (c007, c009, c021-c023, '
        'c025-c026, c029, c032, c034-c035, c046-c049, c053). Card numbers 216, 81, 8 of 8, 2.39, 1.84, 13.2 percent, 0.625, '
        '2.65625, 0.0125 appear in the lessons.')
newpass('SC1a-r10-lab-L01-L02-L03-claims', 'Lab docstrings and the lessons say only what the code and output show',
        'tests/labs/SC1/lab-SC1-L01-1.py:1-9; lab-SC1-L02-1.py:1-8; lab-SC1-L03-1.py:1-14; L01.html:136, :208; L02.html:170, :278; L03.html:133, :253',
        'Round 10 FRESH: L01 twin prints the 3 dyadic lines, count 15 of 15, the covariance line and count 81 of 81 (run output); '
        'L02 prints 216 of 216, True, eight levels within bound, and 0.348139 / 1.309399; L03 prints means, se, z (max |z| 2.39) and '
        '16 exact sums with closed-form True. Each page sentence about these matches the code and output.')

fresh_ids_extra = set()
rows = []
for r in prev['rows']:
    rid = r['id']
    if rid in REPLACE:
        t = REPLACE[rid]
        status, check, loc, ev = t[0], t[1], t[2], t[3]
        row = {'id': rid, 'check': check, 'location': loc, 'status': status, 'evidence': ev}
        if status != 'PASS':
            row['fix'] = t[4]
        rows.append(row)
        continue
    if rid in GATE_IDS_RERUN or any(f in r['location'] for f in CHANGED):
        new = {'id': rid, 'check': r['check'], 'location': r['location'], 'status': r['status'], 'evidence': FRESH_PREFIX + r['evidence']}
        if r['status'] != 'PASS':
            raise SystemExit('unexpected non-PASS previous row ' + rid)
        rows.append(new)
    else:
        if r['status'] != 'PASS':
            raise SystemExit('unexpected non-PASS previous row ' + rid)
        rows.append({'id': rid, 'check': r['check'], 'location': r['location'], 'status': 'PASS', 'evidence': CARRY_PREFIX + r['evidence']})
rows.extend(GATE_ROWS)
rows.extend(NEWPASS)
# new FAIL rows
for k in ['SC1a-r10-card-L05-ck-wording', 'SC1a-r10-A1-attribution-M4']:
    status, check, loc, ev, fix = REPLACE[k]
    rows.append({'id': k, 'check': check, 'location': loc, 'status': status, 'evidence': ev, 'fix': fix})
ids = [r['id'] for r in rows]
assert len(ids) == len(set(ids)), 'duplicate ids'
prev_ids = [r['id'] for r in prev['rows']]
missing = [i for i in prev_ids if i not in ids]
assert not missing, missing
nonpass = [r['id'] for r in rows if r['status'] != 'PASS']
counts = {'PASS': sum(r['status'] == 'PASS' for r in rows), 'FAIL': sum(r['status'] == 'FAIL' for r in rows),
          'UNVERIFIABLE': sum(r['status'] == 'UNVERIFIABLE' for r in rows)}
verdict = 'PASS' if not nonpass else 'FAIL'
frag = {
    'unit': 'SC1', 'slice': 'a', 'round': 10,
    'round_note': 'Round 10, independent verifier (Haiku), did not build SC1. Previous pin c93dd52 (round 9).',
    'verifier': 'Claude Haiku 5.5, independent verifier SC1-a round 10',
    'pin': '00a84795f276456fce19d4181373cc4efba11a36',
    'base': 'c93dd526025c6dffd34c54cd2c89eb62a890f885',
    'checkout': '/Users/billyribeiro/.fanout/wt/verifyE10-SC1-a',
    'scratch': '/Users/billyribeiro/.fanout/wt/verifyE10-SC1-a/ledgers/SC1/scripts/SC1-a-r10',
    'verified_at': '2026-11-05T08:36:54Z',
    'verdict': verdict,
    'rows': rows,
    'mutants': [
        {'id': 'SC1a-r10-lab-mut1-L01-width', 'description': 'lab-SC1-L01-1: dyadic width t/2**(n+1) instead of t/2**n; the sums print 1/2 not 1.',
         'killed_by': 'exact diff against L01.html expected block (ledgers/SC1/scripts/SC1-a-r10/mutant_kill_r10.out)'},
        {'id': 'SC1a-r10-lab-mut2-L02-scale', 'description': 'lab-SC1-L02-1: level scale 2**(-m/2) instead of 2**(-(m+1)/2); the grid-supremum line prints False.',
         'killed_by': 'exact diff against L02.html expected block (mutant_kill_r10.out)'},
        {'id': 'SC1a-r10-lab-mut3-L03-se-divisor', 'description': 'lab-SC1-L03-1: standard error divides by n+1 not n; z for N=2 prints 2.40, not 2.39.',
         'killed_by': 'exact diff against L03.html expected block (mutant_kill_r10.out)'},
        {'id': 'SC1a-r10-lab-mut4-L03-exact-offset', 'description': 'lab-SC1-L03-1: exact t-squared sum offset by 1e-9; closed-form matches prints False.',
         'killed_by': 'exact diff against L03.html expected block (mutant_kill_r10.out)'},
    ],
    'registry_flags': [
        'A1 attribution to M4 (L01.html:71) not located for parts (a) integrable form, (c), (d), (e); see row SC1a-r10-A1-attribution-M4.'
    ],
    'freshness_flags': [
        'Changed since c93dd52 in this slice: index.html (lede, objective 6, placement explanation, L05/L06 cards), L02.html:489, L03.html:51 and :379, cards.json.',
        'Unchanged since c93dd52: L01.html, tests/labs/SC1/lab-SC1-L01-1.py, L02/L03 twins, project.html. Rows citing only these are carried; all others re-verified (FRESH).'
    ],
    'notes': [
        'Full line-by-line read of index.html (190 lines), L01.html (446), L02.html (560), L03.html (504) at 00a8479, and the three lab twins. Delta read hunk by hunk (git diff c93dd52 HEAD -- slice files).',
        'Gates run: check_pages, check_dag, check_projects, run_labs, page_smoke (index, L01-L03, alone), verify_refs --offline, ruff, mypy --no-incremental, pytest -k SC1, twins under python -I -W error.',
        'Not run: run_graders and mutate_graders (project graders; outside slice a). Alternative correct implementations not applicable (lab twins are demonstrations, not graders).',
        'Not checked in full: L04-L08 and project.html content (only the hub cards and cross-references to them were checked); M4 pages were searched by term, not read in full; Assumption A1(b) M4 attribution not checked.',
        'Cards L04-L08 not verified beyond the hub card text; cards.json entries for L04-L08 are outside slice a.'
    ],
    'summary': {
        'text': 'SC1-a round 10 at 00a8479: verdict ' + verdict + '. ' + str(len(rows)) + ' rows: ' + str(counts['PASS']) + ' PASS, ' +
                str(counts['FAIL']) + ' FAIL, ' + str(counts['UNVERIFIABLE']) + ' UNVERIFIABLE. Round-9 FAIL rows SC1a-hub-concept-list (still FAIL: OST gone, but the conditional-expectation-l2 gap remains), SC1a-r9-hub-ost-card-L04, SC1a-r9-hub-reflection-assumptions, SC1a-r9-hub-objective-reflection-proof and SC1a-r9-quiz-L02-q3-explanation now PASS.',
        'counts': counts,
        'non_pass_ids': nonpass,
    },
}
json.dump(frag, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('rows', len(rows), counts, verdict, nonpass)
