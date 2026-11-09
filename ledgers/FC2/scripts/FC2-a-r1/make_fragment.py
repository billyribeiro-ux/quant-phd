import json
BASE = json.load(open('/Users/billyribeiro/.fanout/frags/S-FC2-a.round9.json', encoding='utf-8'))
S = 'ledgers/FC2/scripts/FC2-a-r1/'

GEN = ("Carried from round 9 (course/modules/FC/FC2/L01.html, L02.html, L03.html, index.html, project.html, "
       "grader/ and the FC2 twins tests/labs/FC2/lab-FC2-L01-1.py, L02-1, L03-1 and lab-FC2-project-1..3 "
       "byte-identical since the previous pin 95f3f8cb; git diff --quiet 95f3f8cb HEAD exit 0 in round 1):")
CARDS = ("Carried from round 9 (the cited cards.json entries are byte-identical since the previous pin 95f3f8cb: "
         "a per-id JSON comparison in round 1 changed only FC2-c179, c192, c201; the cited lesson pages are "
         "byte-identical, git diff --quiet exit 0 in round 1):")

# rows re-verified from scratch in round 1 (subject changed, or non-PASS base row, or a gate)
FRESH = {
 'FC2a-cmd-check_pages': "Round 1 at 2a805c83: `.venv/bin/python tools/check_pages.py --unit FC2` printed 'check_pages FC2: PASS', exit 0 (ledgers/FC2/scripts/FC2-a-r1/gates_1.txt).",
 'FC2a-cmd-check_dag': "Round 1 at 2a805c83: `.venv/bin/python tools/check_dag.py --unit FC2` printed 'check_dag FC2: PASS', exit 0 (gates_1.txt).",
 'FC2a-cmd-check_projects': "Round 1 at 2a805c83: `.venv/bin/python tools/check_projects.py --unit FC2` printed 'check_projects FC2: PASS', exit 0 (gates_1.txt). Project gate; not judged in slice a.",
 'FC2a-cmd-run_labs': "Round 1 at 2a805c83: `.venv/bin/python tools/run_labs.py --unit FC2` printed 'run_labs FC2: PASS (11/11)', exit 0 (ledgers/FC2/scripts/FC2-a-r1/labs_1.txt).",
 'FC2a-cmd-twin-direct': "Round 1: `.venv/bin/python -I -W error` on lab-FC2-L01-1, L02-1, L03-1 exited 0 each (labs_1.txt; twin-L0*.out, .err empty); lab-FC2-project-1, -2, -3 exited 0 each under the same flags (project-twin-*.out).",
 'FC2a-cmd-page_smoke': "Round 1: `.venv/bin/python tools/page_smoke.py --unit FC2 --pages index.html L01.html L02.html L03.html --skip-sweep` printed 'page_smoke FC2: PASS', exit 0 (ledgers/FC2/scripts/FC2-a-r1/smoke_pytest_1.txt).",
 'FC2a-cmd-ruff-mypy': "Round 1: `ruff check tests/labs/FC2/` printed 'All checks passed!' exit 0; `ruff format --check tests/labs/FC2/` printed '11 files already formatted' exit 0; `mypy --no-incremental` on the six FC2 twins printed 'Success: no issues found in 6 source files' exit 0 (labs_1.txt, mypy_6.txt).",
 'FC2a-cmd-pytest': "Round 1: `.venv/bin/python -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_curriculum.py tests/test_docs_figures.py -q` exit 0, all dots, no failures (smoke_pytest_1.txt).",
 'FC2a-cmd-verify_refs': "Round 1: `.venv/bin/python tools/verify_refs.py --offline` printed 'offline integrity: 560 entries, 0 problems', exit 0 (gates_1.txt).",
 'FC2a-r5-build-site': "Round 1: `.venv/bin/python tools/build_site.py --check` printed 'site data current: 6 outputs', exit 0 (gates_1.txt). Re-run because cards.json changed.",
 'FC2a-hub-hours': "Re-derived round 1: data-hours L01..L08 = 6, 8, 9, 7, 8, 8, 8, 6, sum 60, equal to index.html:29 data-hours-lessons=60; data-hours-project=30 unchanged. `git diff 95f3f8cb..HEAD -- course/modules/FC/FC2 | grep -c data-hours` = 0.",
 'FC2a-r9-delta-scope': "Round 1: `git diff --quiet 95f3f8cb HEAD --` on L01.html, L02.html, L03.html, index.html and the three slice-a twins exits 0 (byte-identical); project.html, grader/ and the project twins exit 0; L05.html and L06.html exit 0. The FC2 delta within course/modules/FC/FC2 and tests/labs/FC2 is two files: L04.html (one line, 84) and cards.json (three cards).",
 'FC2a-r9-delta-hunks': "Round 1: every hunk of `git diff 95f3f8cb..HEAD` for the slice subjects was read. cards.json has three hunks: @@ -1165 (FC2-c179 front and back), @@ -1250 (FC2-c192 back), @@ -1285 (FC2-c201 front and back). No hunk in L01-L03, index.html, the slice-a twins, project.html or the grader. The only page hunk in the delta is L04.html:84 (Remark 1.3), outside slice a and read for the c179 row.",
 'FC2a-r9-cards-changed-L04-L08': "Round 1: the changed cards were re-read against their current lessons. c179 vs L04 Lemma 1.2 (text lines 32-35) and Remark 1.3 (text lines 36-37, 'the payoff of buying the underlying at the strike K at expiry'): matches. c192 vs L04 Definition 1.1 (text line 30, 'let K > 0 be the strike'): matches. c201 vs L05 Theorem 1.2 and its proof (L05 text lines 26-28, 'Under A1, A2, A3, A4 and A5'): the zero payoff uses A1 (no income), A2 (short sale and lending), A4 (lent cash returns K), A5 (European payoffs at expiry) and Lemma 1.2 of Lesson 4; A3 excludes both signs. The other cards in the row (c051, c062, c083, c187, c193-c200, c205-c207) are byte-identical to 95f3f8cb and are carried: " + CARDS,
 'FC2a-r9-card-c179-dag': "Re-verified from scratch. Base (95f3f8cb): c179 read 'a long forward on the underlying' and L04.html:84 read the same. At 2a805c83: c179 front and back (cards.json lines 1168-1169) read 'buying the underlying at the strike'; `grep -i forward` on the c179 entry is empty; L04.html:84 reads 'the payoff of buying the underlying at the strike K at expiry'. L04's Uses line (L04.html:37) lists only present value and continuous compounding; plans/FC2-build-plan.md:122 says L04 uses L01 and M1 for nothing else; forward-contract is defined in L02 (plan:103). 'underlying' is not a registered concept id (curriculum/curriculum.json: 0 hits). So c179 names no concept outside L04's prerequisite closure. Gate: check_dag PASS (gates_1.txt). Row PASS. Observation for the L04 owner (not a row of this slice, not a ruling-26 kind): L04.html:463 (retrieval-quiz explanation, text line 274) still says 'Their difference is the payoff of a forward (Remark 1.3).'",
 'FC2a-cards-accuracy': "Re-verified round 1: the three changed cards c179, c192, c201 were compared with the current lesson text (L04 text lines 30, 33-37; L05 text lines 26-30) and each matches. Every other card is byte-identical per id (only c179, c192, c201 differ from 95f3f8cb). The L01-L03 lesson pages are byte-identical, so the L01-L03 card comparisons of round 9 stand under the carry prefix of this row's pages.",
 'FC2a-cards-coverage': "Re-derived round 1 from course/modules/FC/FC2/cards.json at 2a805c83: lesson counts L01 22, L02 24, L03 23 (total for L01-L03 69; all lessons L04 25, L05 27, L06 31, L07 24, L08 18; total 194). Ids unique (194), fronts unique. No card added or removed since 95f3f8cb.",
 'FC2a-cards-trivia': "Re-read round 1: c192 is a definition card ('What is the strike of an option?', answer: the number K > 0 that the payoffs are measured from), which is the one permitted bare definition. c179 asks for an argued payoff identity and c201 for the reason parity holds (Theorem 1.2). Other cited cards (c021, c046, c024, c027, c190) are byte-identical per id and are carried under CARDS.",
 'FC2a-cards-hypotheses': "Re-verified round 1: c201 'Under A1 to A5' matches the hypotheses of Theorem 1.2 (L05 text line 26: 'Under A1, A2, A3, A4 and A5'). Its proof (L05 lines 27-28) uses A1, A2, A4, A5 for the zero payoff and A3 for the sign; the card's back lists exactly those. c179 needs no hypothesis beyond the identity of Lemma 1.2 (L04 text line 33: 'For every real s and every K'). Other cited cards (c006, c027, c043, c046, c144, c178, c186, c207) are byte-identical per id: carried under CARDS.",
 'FC2a-grades': "Re-derived round 1 from cards.json: grade counts T 112, C 13, absent 69 (definition cards). c179 T: basis Lemma 1.2, proved on the page (L04 text line 35). c201 T: basis Theorem 1.2 proof on the page (L05 text line 28). c192 has no grade (definition card). The changed grade fields are unchanged from 95f3f8cb. Key-results tables (L01.html:430-435, L02.html:411-417, L03.html:422-427) are byte-identical: carried under GEN.",
 'FC2a-notation': "Re-derived round 1: symbols used by the changed cards are C, P, S, K, X (portfolio, L05 text line 28), D = e^{-r tau} (defined L05 text line 22) and the English article 'a'. notation/notation.json symbols are T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}; its macros register no C, P, S, D, K or X. No conflict. Other card symbols carried under CARDS.",
 'FC2a-r9-card-numbers': "Re-run round 1: `.venv/bin/python -I ledgers/FC2/scripts/FC2-a-r1/card_numbers_r9_copy.py ALL` printed 'checked 194 missing 1' and ('FC2-c100', 'L07', '1/2'), the same single substring miss as round 9 (L07 writes \\tfrac12 in Lemma 1.1). c179, c192 and c201 contain no numeral beyond K > 0 and the labels A1-A5, Lemma 1.2, Theorem 1.2 (all present in their lessons). Not a defect (card_numbers_all.txt).",
 'FC2a-r9-card-duplicates': "Re-run round 1 over all 194 cards (ledgers/FC2/scripts/FC2-a-r1/card_scan_r1.txt): ids unique, fronts unique. Front similarity above 0.8: c139/c187 0.981, c168/c169 0.974, c160/c162 0.961, c024/c177 0.907, c005/c154 0.884, c192/c193 0.862, c084/c163 0.852, c001/c189 0.835, and others. The pair c192 ('What is the strike') and c193 ('What is the premium') at 0.862 asks different questions. Changed c179 and c201 have nearest fronts at 0.49 (c048, c161). No duplicate.",
 'FC2a-r9-card-registry-symbols': "Re-derived round 1: see FC2a-notation. The changed cards use no registered symbol with another meaning: R_f, Q, Phi, T, gamma_3, gamma_4, R^* and R^{e*} do not occur in c179, c192 or c201. No conflict.",
 'FC2a-r9-card-scope-words': "Re-read round 1 for scope words in the changed cards: c179 'same' (the same strike and expiry, the hypothesis of the identity, L04 text line 37 'with the same strike and expiry'); c201 'every' ('zero payoff in every state', the proof's conclusion, L05 text line 28); c192 none. Each occurrence has a hypothesis or a proof on the page.",
 'FC2a-r9-card-grades': "Re-derived round 1 with FC2a-grades: c179 T with Lemma 1.2 proved on the page (L04 text line 35); c201 T with Theorem 1.2 proved on the page (L05 text line 28); c192 is a definition card with no grade; C grades on c046, c049, c050 unchanged per id and carried under CARDS.",
 'FC2a-r4-card-c025-c172-overlap': "Re-run round 1 with the 194-card similarity scan (card_scan_r1.txt): c025 and c172 are not in the >0.8 list. c025 asks for the value of a long forward at date t; c172 asks at which spot a forward priced at F* is worth zero. Different questions.",
}

# rows whose subject is byte-identical since 95f3f8cb and that cite cards
CARD_CARRY = {'FC2a-r3-ex34-hypothesis', 'FC2a-r3-card-c037-remark14', 'FC2a-r4-card-c007-scope',
              'FC2a-r4-proposition-numbering', 'FC2a-r4-card-c027-hypothesis', 'FC2a-r5-delta-hunks',
              'FC2a-r9-cards-L01', 'FC2a-r9-cards-L02', 'FC2a-r9-cards-L03', 'FC2a-r9-numbers-cards',
              'FC2a-dag-closure'}
# rows about project files (byte-identical since 95f3f8cb) are carried under GEN, which names project.html

rows = []
for r in BASE['rows']:
    rid = r['id']
    if rid in FRESH:
        status = 'PASS'
        evidence = FRESH[rid]
    else:
        assert r['status'] == 'PASS', rid
        prefix = CARDS if rid in CARD_CARRY else GEN
        status = 'PASS'
        evidence = prefix + ' Round-9 evidence (base row): ' + r['evidence']
    if rid == 'FC2a-dag-closure':
        evidence += ' Round 1 note: the card-level row FC2a-r9-card-c179-dag is re-verified PASS in round 1 (c179 no longer names forward-contract).'
    rows.append({'id': rid, 'check': r['check'], 'location': r['location'], 'status': status, 'evidence': evidence})

assert len(rows) == 69 and len({r['id'] for r in rows}) == 69
assert set(FRESH) <= {r['id'] for r in BASE['rows']}

registry = [("Carried from round 9 (not re-verified in round 1): " + f) for f in BASE['registry_flags']]

notes = [
 "Delta: 95f3f8cb..2a805c83 (HEAD). Within the slice paths the delta changes course/modules/FC/FC2/cards.json (cards c179, c192, c201 only; 194 ids before and after; no card added or removed) and course/modules/FC/FC2/L04.html line 84 (Remark 1.3, cited by c179). L01.html, L02.html, L03.html, index.html, the three slice-a twins, project.html, grader/ and the project twins are byte-identical to 95f3f8cb (git diff --quiet exit 0). L05.html and L06.html are byte-identical too.",
 "Fragment base: S-FC2-a.round9.json (pin 95f3f8cb), whose only non-PASS row was FC2a-r9-card-c179-dag (DAG: 'forward' named the L02 concept inside L04). That subject changed in this delta and is re-verified PASS: c179 and Remark 1.3 now name 'buying the underlying at the strike K at expiry'.",
 "Ruling 37: no new mutants written. Slice a has no grader; mutants: [].",
 "Ruling 26 FAIL kinds: every row here was checked against the kinds (false or unproved math, missing hypothesis, wrong number, over-graded claim, failing gate, surviving non-equivalent mutant, lab statement the code does not support). None found.",
 "Observation, not a row (ruling 30: no hunt outside the rows; outside slice a; not a ruling-26 kind): course/modules/FC/FC2/L04.html:463 (retrieval-quiz explanation of 'What does the payoff identity of Lemma 1.2 say?', text line 274) still reads 'Their difference is the payoff of a forward (Remark 1.3).' by name. It is the same forward-contract naming that c179 had. L04 owner should route it under the DAG rule (plans/FC2-build-plan.md:122). Not counted in this verdict.",
 "Gate outputs: check_pages PASS, check_dag PASS, check_projects PASS, build_site --check PASS, verify_refs --offline PASS (560 entries, 0 problems), run_labs PASS (11/11), page_smoke PASS, ruff check and format PASS, mypy PASS (6 twins), pytest (5 files) PASS, twins under -I -W error exit 0 (3 slice-a twins, 3 project twins). Scripts and outputs in ledgers/FC2/scripts/FC2-a-r1/.",
 "Not re-run in round 1 (carried under the prefix, bytes identical): the L01-L03 lab expected-block vs output comparisons, the page-vs-twin code comparisons, the L01-L03 mathematics and problem-set re-reads, the hub prose and placement arithmetic, and the project page-vs-twin and expected-vs-output blocks. Blind exemplar scoring is not applicable: slice a has no rubric.",
 "Carried registry flags (unit-level, not slice defects): hull2021options, stoll1969relationship and cox1979option records carry no edition, volume or issue (plans/FC2-build-plan.md section 7 Q5); the curriculum brief for FC2 project says 'Given an embedded option-chain snapshot', which conflicts with the SIMULATED-chain decision (plans/FC2-open-items.md D1). Flagged for the curriculum owner.",
]

frag = {
 'unit': 'FC2',
 'slice': 'a',
 'round': 1,
 'verifier': 'Haiku independent verifier, FC2-a round 1 closing delta (ruling 30; did not build FC2)',
 'pin': '2a805c831410ab77c38c227f7e121e8537193ce9',
 'base': '95f3f8cb21c2cd9fc904430bd30a6b734d01f672',
 'checkout': '/Users/billyribeiro/.fanout/wt/verifyG1-FC2-a (detached at 2a805c83, .venv symlinked, vendor copied)',
 'scratch': 'ledgers/FC2/scripts/FC2-a-r1/',
 'verified_at': '2026-11-09',
 'verdict': 'PASS',
 'rows': rows,
 'mutants': [],
 'registry_flags': registry,
 'freshness_flags': [],
 'notes': notes,
 'summary': {'rows': len(rows), 'pass': sum(1 for r in rows if r['status'] == 'PASS'), 'fail': 0, 'unverifiable': 0},
}
json.dump(frag, open('ledgers/FC2/FC2-a.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', len(rows), 'rows; verdict', frag['verdict'])
