import json, datetime
prev = json.load(open('/tmp/fanout-frags/B-M2-a.round3.json'))
C = 'Carried from round 3 (%s byte-identical since the previous pin): '
F = {}  # id -> (status, evidence) overrides for re-verified rows
R = {}  # id -> carry file list
rerun = {
 'M2-a-cmd-pin': 'Re-run: HEAD 2657ab5 (= pin); git diff aa3c26c..2657ab5 touches M2 files: index.html L01 L03 L05 L06 cards.json grader/test_project.py project.html L07-L24 and lab-M2-L06/L07/L08/L09/L11/L21 twins; the slice-a delta is index.html line 149, L01.html lines 51/146-152/335, L03.html line 51, L05.html line 51, L06.html (rewritten Section 2 and Uses), cards M2-c064..066, lab-M2-L06-1.py docstring.',
 'M2-a-cmd-check_pages': 'tools/check_pages.py --unit M2 -> "check_pages M2: PASS" (exit 0).',
 'M2-a-cmd-check_dag': 'tools/check_dag.py --all -> all modules PASS incl. "check_dag M2: PASS".',
 'M2-a-cmd-run_labs': 'tools/run_labs.py --unit M2 -> "run_labs M2: PASS (27/27)". Each twin also run alone: python -I -W error exit 0 for lab-M2-L01..L06-1.py.',
 'M2-a-cmd-page_smoke': 'tools/page_smoke.py --unit M2 --pages index L01 L03 L05 L06 -> "page_smoke M2: PASS" (each page PASS). L02 and L04 not re-run; their bytes are unchanged (carried).',
 'M2-a-cmd-ruff': 'ruff check tests/labs/M2 -> "All checks passed!"; ruff format --check -> "27 files already formatted".',
 'M2-a-cmd-mypy': 'mypy --no-incremental tests/labs/M2 -> "Success: no issues found in 27 source files".',
 'M2-a-cmd-refs': 'tools/verify_refs.py --offline -> "offline integrity: 560 entries, 0 problems"; tools/verify_refs.py --unit M2 (live) -> "2 of 560 entries, 0 problems".',
 'M2-a-cmd-pytest': 'pytest -q tests/test_labs.py tests/test_run_labs.py -k "M2 or L06 or twin" -> 47 passed. Only a subset was run (the lab delta is one docstring); the full suite was not repeated this round.',
 'M2-a-lab-twins-match': 'Re-run: each page embedded code block equals tests/labs/M2/lab-M2-L0N-1.py for L01..L06 (scripts/M2-a-r4/checks_r4.py: all True). L06 embedded docstring includes "under Assumption 2.1,".',
 'M2-a-lab-L01': 'Re-run: lab-M2-L01-1.py output lines 81-82 (1000; 1.000000e-03 at n=999; 9.990010e-04 at n=1000) match L01.html interpretation (line 84) and key-results row (line 335) and E1-E3 solutions (text lines 144-155). Interpretation now cites the identity |a_n-2|=1/(n+1) of Example 2.3, which is the identity printed in Example 2.3 (a_n-2 = -1/(n+1)).',
 'M2-a-lab-L06': 'Re-run: lab-M2-L06-1.py prints 4 lines (True / 8 of 16 / 16 of 16 / f(-1)=2; f(1)=-2) identical to the page output block; 17 grid points, 16 intervals, 4+4 increasing intervals: all match the page.',
 'M2-a-lab-L03': 'Re-run: run_labs PASS and lab-M2-L03-1.py exit 0; lab file lines 1-13 and 120 byte-identical since the previous pin. L03.html changed only at line 51 (why-it-matters); its lab output block is unchanged.',
 'M2-a-lab-L05': 'L05.html changed only at line 51 (why-it-matters: discount factor now written 1/(1+r)^t for t periods, a correct statement); the cited lines 93-168 are byte-identical; lab-M2-L05-1.py byte-identical.',
 'M2-a-num-L01': 'Re-derived: L01.html interpretation (line 84) and E1 (1/1001 = 0.000999000999..., printed 9.990010e-04 at six places: 9.99000999 rounds up to 9.990010), E2 (1.000000e-03 equals 0.001), E3 (1/10000 = 1.000000e-4 at n=9999), a_1000 = 2001/1001 = 1.999000999... -> 1.999001 at six places; the card M2-c005 threshold formula is consistent.',
 'M2-a-num-L06': 'Re-derived: 3c^2=4 on [0,2] gives c=2/sqrt(3)=1.1547005...; 3c^2=1 on [0,1] gives c=1/sqrt(3)=0.5773502...; 8 of 16 grid intervals; f(-1)=2, f(1)=-2; f(2)=-3 for x^2-4x+1; 1/(1+r)^t (L05). Displayed digits agree with the unrounded values.',
 'M2-a-math-L06': 'Re-derived this round from the L06 text: Prop 1.1 proof (Q(h) signs for h>0 and h<0; limit gives f\'(c)=0); Rolle proof (M != f(a) case, c in (a,b)); MVT proof (g(x)=f(x)-f(a)-s(x-a), g(a)=g(b)=0, Rolle on g, which applies because Assumption 2.1 is stated for every continuous f); Corollary 3.1 (i)-(iii) via Theorem 2.3; M1, M2, M3, P1-P3, R1-R3 solutions; E3 midpoint argument (odd multiples of 1/8 versus critical points +-1 = +-8/8). No gap found.',
 'M2-a-hyp-quiz-L06q5': 'Re-verified: the L06 quiz item "Which hypothesis does Rolle\'s theorem need besides f(a)=f(b)?" (L06.html line 346) lists "Continuity on [a,b] and differentiability on (a,b)", matching Theorem 2.2 as written; the other quiz items (Assumption 2.1, Corollary 3.1(ii), M2 mean-value point, the midpoint item) match the lesson text.',
 'M2-a-grade-labs': 'Re-derived: L06 key-results rows T for Prop 1.1, Rolle, MVT and Cor 3.1 each with proof on the page and Assumption 2.1 named; the Assumption row not graded; lab row C with basis Lab 1. L01 row (line 335) now C with basis Lab 1 and the identity of Example 2.3. L03 Prop 2.2 row is consistent with its statement.',
 'M2-a-prose-L01-lab-would-print': 'Re-read this round: L01 E1-E3 (text lines 144-155) and interpretation (line 84) state what Lab 1 prints; all agree with lab output lines 81-82 and 79-80.',
 'M2-a-prose-L06-exactly': 'Re-read this round: L06 why-it-matters (line 51, rewritten to "If a differentiable function has a maximum or a minimum at a point inside an interval ... its derivative vanishes there (§1 proves this and defines the terms)") matches Prop 1.1 and §1 definitions; key-results row and Lab 1 interpretation match the code.',
 'M2-a-prose-L06-each-hypothesis': 'Re-read this round: §4 canon-breaks (continuity counterexample x on [0,1) with f(1)=0; |x| on [-1,1]; x^3 at 0) each name the hypothesis dropped and the check is correct (left limit at 1 is 1; |x| has no derivative at 0).',
 'M2-a-hub-structure': 'Re-read this round: index.html visible text in full (text dump, 115 lines): objectives, prerequisites, placement arithmetic (6/8=75%, 7/8=87.5%, 80% bar means at least 7 of 8), lesson list (L01-L24, 10 h each), project ladder, data status. Hours: data-hours-lessons=240, data-hours-project=60, sum 300, project 20% (in 10-40%).',
 'M2-a-hub-reading-claim': 'Re-read: index.html reading section ("Core reading", text line 113): no passage locator confirmed; "the results of Lesson 6 that use the mean value argument are proved only under Assumption 2.1" is consistent with L06 (Theorems 2.2, 2.3, Cor 3.1 begin "Assuming Assumption 2.1"). Title "Vector Calculus, Linear Algebra, and Differential Forms" matches references.json hubbard2015vector.title.',
 'M2-a-hub-banned': 'Re-scanned this round: index, L01, L03, L05, L06 visible text for roughly half / about 6% / historically / ellipsis / process words (build, builder, round, verifier, REQUEST): no hit in learner prose.',
 'M2-a-cards-dup-scan': 'Re-run: cards.json 376 cards, 0 duplicate ids, 0 duplicate fronts (case-insensitive).',
 'M2-a-cards-L01-L06': 'Changed cards in L01-L06 since aa3c26c: M2-c064, M2-c065, M2-c066 (lines of cards.json). c064 and c065 re-checked and match L06 (Assumption 2.1; Theorem 2.2). M2-c066 back text: "Hypotheses: as in Rolle\'s theorem, with Assumption 2.1 taken as given." Rolle\'s theorem includes f(a)=f(b); L06.html Theorem 2.3 (line text "as in Theorem 2.2 without the condition f(a)=f(b)") removes it. The card therefore states a hypothesis the mean value theorem does not need, which contradicts the lesson. Other L01-L06 cards (c001-c063, c067-c074) carried; the numbers in M2-c055..c058 and c069/c070 re-derived (95.0625; 32.0625; 29/49; 2 and -2) and match. Card M2-c066 is FAIL.',
 'M2-a-claim-L01-ex23-1000': 'Re-verified: key-results row (L01.html line 335) and interpretation (line 84) now attribute the value 1000 to the identity |a_n-2| = 1/(n+1) in Example 2.3 (which is printed as a_n - 2 = -1/(n+1)), and the 1001 remark matches N > 1/eps with eps=0.001. The round-3 FAIL is cured.',
 'M2-a-xref-L06-uses': 'Re-verified: L06 Uses row now links "the product and quotient rules (Lesson 5, §1)" and "the chain rule (Lesson 5, §2)"; L05.html section 1 is "Limit laws ... the product and quotient rules" and section 2 is "The chain rule". The round-3 FAIL is cured.',
 'M2-a-dag-slice': 'Re-run: tools/check_dag.py --all -> "check_dag M2: PASS"; data-concept links in index and L01-L06 checked by the DAG tool; L06 new Section 2 uses only L04/L05 and M2 prose terms, no new concept link.',
 'M2-a-defuse-L01-L03': 'Re-run this round on the current text dumps: the word "derivative" occurs in L01 and L02 zero times and in L03 only inside the Next-link title "The Derivative as a Limit" (a navigation link, not a use). L01 and L03 use no derivative before its definition in L04. The only term used in L03 before any definition is "continuity" in the Corollary 1.4 title, which is prose-only (Q5).',
 'M2-a-refs-spivak-hubbard': 'Re-run: verify_refs --offline and --unit M2 live: 0 problems; spivak2008calculus and hubbard2015vector entries unchanged (references/references.json not in delta).',
}
carry = {
 'M2-a-lab-L02': ['course/modules/M/M2/L02.html', 'tests/labs/M2/lab-M2-L02-1.py'],
 'M2-a-lab-L04': ['course/modules/M/M2/L04.html', 'tests/labs/M2/lab-M2-L04-1.py'],
 'M2-a-num-L02': ['course/modules/M/M2/L02.html'],
 'M2-a-num-L03': ['course/modules/M/M2/L03.html (cited lines; only line 51 changed)'],
 'M2-a-num-L04': ['course/modules/M/M2/L04.html'],
 'M2-a-num-L05': ['course/modules/M/M2/L05.html (cited lines 95, 167, 176-293; only line 51 changed)'],
 'M2-a-num-L05-lab-size': ['course/modules/M/M2/L05.html (line 214; only line 51 changed)'],
 'M2-a-num-hub': ['course/modules/M/M2/index.html (lines 69-71; only line 149 changed)'],
 'M2-a-num-hub-hours': ['course/modules/M/M2/index.html (line 29)'],
 'M2-a-math-L01': ['course/modules/M/M2/L01.html (cited Def 2.1, Prop 2.2, Prop 3.1 lines; hunks at 51, 146-152, 335 only)'],
 'M2-a-math-L02': ['course/modules/M/M2/L02.html'],
 'M2-a-math-L03': ['course/modules/M/M2/L03.html (cited lines; only line 51 changed)'],
 'M2-a-math-L04': ['course/modules/M/M2/L04.html'],
 'M2-a-math-L05': ['course/modules/M/M2/L05.html (cited lines; only line 51 changed)'],
 'M2-a-hyp-quiz-L01q6-card-c011': ['course/modules/M/M2/L01.html (quiz L01q6 lines 383-389)', 'course/modules/M/M2/cards.json (M2-c011)'],
 'M2-a-prose-unproved-claims': ['course/modules/M/M2/L01.html (line 214)', 'course/modules/M/M2/L02.html (line 206)', 'cards M2-c012'],
 'M2-a-prose-L04-only-meaning': ['course/modules/M/M2/L04.html'],
 'M2-a-prose-L05-misc-h2': ['course/modules/M/M2/L05.html (misconception 3, line 214; only line 51 changed)'],
 'M2-a-prose-scope-L02-why': ['course/modules/M/M2/L02.html'],
 'M2-a-prose-frequency-claims': ['course/modules/M/M2/index.html (line 33)', 'course/modules/M/M2/L02.html (line 51)'],

 'M2-a-xref-L03-keyrow': ['course/modules/M/M2/L03.html (key-results rows 319-324; only line 51 changed)'],
 'M2-a-xref-M1-locators': ['course/modules/M/M2/index.html (lines 80, 89, 98, 107, 116-125; only line 149 changed)', 'course/modules/M/M2/L01.html (line 189)'],
 'M2-a-xref-L13-rounding': ['course/modules/M/M2/L04.html (canon-breaks line 156)'],
 'M2-a-hours': ['course/modules/M/M2/L01-L06.html (eyebrow/hours lines; no hunk touches them)'],
 'M2-a-scope': [],
}
rows = []
for r in prev['rows']:
    rid = r['id']
    if rid in rerun:
        status = 'FAIL' if rid == 'M2-a-cards-L01-L06' else 'PASS'
        ev = rerun[rid]
        if rid == 'M2-a-cards-L01-L06':
            status = 'FAIL'
        rows.append({'id': rid, 'check': r['check'], 'location': r['location'], 'status': status, 'evidence': ev, **({'fix': "In course/modules/M/M2/cards.json, card M2-c066 back: replace 'Hypotheses: as in Rolle's theorem, with Assumption 2.1 taken as given.' with 'Hypotheses: f is continuous at each point of [a, b] with a < b, differentiable at each point of (a, b), and Assumption 2.1 holds for f on [a, b]; the condition f(a) = f(b) is not needed.' (the lesson's Theorem 2.3 says exactly this). Then re-run tools/build_site.py --check if cards are site data."} if status != 'PASS' else {})})
    elif rid in carry:
        rows.append({'id': rid, 'check': r['check'], 'location': r['location'], 'status': 'PASS',
                     'evidence': C % ('; '.join(carry[rid]) if carry[rid] else 'subject') + r['evidence']})
    else:
        rows.append({'id': rid, 'check': r['check'], 'location': r['location'], 'status': r['status'], 'evidence': r['evidence'] if r['status']=='PASS' else r['evidence']})
ids = [r['id'] for r in rows]
print('rows', len(rows), 'unique', len(set(ids)), 'prev', len(prev['rows']))
for r in rows:
    if r['status'] != 'PASS': print('NON-PASS', r['id'], r['status'])
missing = [r['id'] for r in prev['rows'] if r['id'] not in ids]
print('missing', missing)
json.dump({'unit':'M2','slice':'M2-a','round':4,'verifier':'round-4 independent verifier (Haiku), slice M2-a (hub index.html, L01-L06 and their lab twins); did not build M2 and shares no context with the builders','pin':'2657ab5','base':'none','previous_ledger':'/tmp/fanout-frags/B-M2-a.round3.json (round 3, pin aa3c26c)','checkout':'/tmp/verifyB4-M2-a (detached at 2657ab5; .venv symlinked; vendor present)','scratch':'/tmp/M2-v/a-r4','verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),'verdict':'FAIL','rows':rows,'mutants':[],'registry_flags':[],'freshness_flags':[],'notes':prev.get('notes',[])+['Round 4 delta from aa3c26c: index.html line 149; L01.html lines 51, 146-152, 335; L03.html line 51; L05.html line 51; L06.html rewritten Sections 1-3 and Uses; cards M2-c064..066; lab-M2-L06-1.py docstring. Scripts: ledgers/M2/scripts/M2-a-r4/. Architect ruling on lab mutants applied: no mutation testing for lab twins; no project slice in this slice, so mutants is empty.'],'summary':{'rows':len(rows),'pass':sum(r['status']=='PASS' for r in rows),'fail':sum(r['status']=='FAIL' for r in rows),'unverifiable':sum(r['status']=='UNVERIFIABLE' for r in rows)}}, open('/tmp/verifyB4-M2-a/ledgers/M2/M2-a.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
