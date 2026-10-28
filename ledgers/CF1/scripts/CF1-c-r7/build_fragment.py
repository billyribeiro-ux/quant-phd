import json, datetime
R6 = json.load(open('/tmp/fanout-frags/CF1-c.round6.json'))
PREV = 'd57df1e'
rows_in = {r['id']: r for r in R6['rows']}
FRESH = {
 'CF1-c-prose-L05-many-firms': 'L05.html why-it-matters (line 52, changed in this delta) re-read: "the evidence section quotes no passage from the registered paper and states no finding about use". Section 4 (line 233) states no finding and quotes no passage, so the sentence is supported. Lab 1 is SIMULATED, as the sentence says.',
 'CF1-c-why-matters-L05-evidence-promise': 'L05.html line 52 re-read (changed). The phrase "states no finding about use" matches Section 4 (lines 231-233): no finding and no passage from the registered paper are stated.',
 'CF1-c-lab-L05-interpretation': 'L05.html Lab 1 interpretation (line 202, changed from "confirms" to "agrees with"). Numbers 2.750, 3.469, 121251.71, 693692.91 match the lab output (tests/labs/CF1/lab-CF1-L05-1.py run this round, output in /tmp/cf1-v/CF1-c-r7/L05.out). Project B discounted cumulative flow recomputed (-96168.29 after year 3, zero flows after) and stays negative. Sentence "the same argument applied to the discounted flows gives the discounted one" is the Section 1 paragraph argument.',
 'CF1-c-num-L05-E1-range': 'L05.html E1 solution (line 316, changed). Recomputed: 693692.91 - 121251.71 = 572441.20 cents = 5724.41 currency units (python -I ledgers/CF1/scripts/CF1-c-r7/r7_check.py, output E1 range 572441.2). Payback distinct values 1 each (lab output line "distinct_simple_payback 1", "distinct_discounted_payback 1").',
 'CF1-c-prose-L05-E1-section2-locator': 'L05.html E1 solution (line 316): the locator now reads "discounted analogue in Section 1". Section 1 (line 70, the paragraph after Definition 1.2) states that the argument of Proposition 2.1 applies to the discounted sums D_t in the same way. Section 2 states only Propositions 2.1, 2.2 and their proofs. Round-6 FAIL resolved.',
 'CF1-c-grade-L05': 'L05.html key-results table (lines ~363-374 now): the "Open" row is removed. Every remaining grade cell is T or C (grep data-grade over the table), all on the BLUEPRINT section 3 scale, each with a source cell. Round-6 FAIL resolved.',
 'CF1-c-grade-L06': 'L06.html key-results table (lines ~363-370): the "Open" row is removed. Every remaining grade cell is T or C, on the BLUEPRINT section 3 scale. grep for "Open" in L05.html and L06.html: no hits. Round-6 FAIL resolved.',
 'CF1-c-attrib-L05-graham': 'L05.html Section 4 fifth-defect paragraph (line 233, changed). Attribution "Graham and Harvey (2001) is the registered source whose title names corporate finance practice" checked against references/references.json key graham2001theory: title "The theory and practice of corporate finance: evidence from the field", authors Graham, John R and Harvey, Campbell R, year 2001, container Journal of Financial Economics 60(2-3), status "verified" (DOI 10.1016/s0304-405x(01)00044-7). Title names corporate finance practice: confirmed. The passage locator is not confirmed and the claim is graded C with that basis. The paper itself was not read (no fetch attempted).',
 'CF1-c-cards-L05': 'cards.json L05 cards CF1-c062 to c074 and c096 to c098 (16 cards), read against the current lesson text. Basis fields checked: Definition 1.1/1.2, Proposition 2.1/2.2/3.1, Problem R2, Lab 1, Section 4, Section 5 first and second misconception, Section 1 interpolation: each basis appears in the lesson (Problem R2 is problem R2 in Section 6; Section 5 misconceptions are the first and second items, lines 239-255). FAIL on c065: its front and back ("For conventional flows and a rate of zero or more ... The discounted year is the same or later") omit the hypothesis of Proposition 2.2 that both paybacks exist (see CF1-c-scope-L05-prop22-existence). Basis "Proposition 2.2, proved in Section 2" is correct.',
 'CF1-c-cards-L06': 'cards.json L06 cards CF1-c075 to c087 and c099, c100 (15 cards), read against the current lesson text. Basis fields checked: Definition 1.1/1.2, Propositions 2.1-2.3, Problem P2, Lab 1 (seed 6), Remark 2.4, Section 5 first and second misconceptions (L06 lines 236-251), Remark 3.1, Section 3. Each cited locator exists. Card texts match the lesson and the lab output (c081 79,216.82 vs 79,078.68; c082 1.0008; c083 0.0552 and 0.0010).',
 'CF1-c-cards-duplicates': 'cards.json (all 100 cards): python -I check: 100 cards, 100 distinct ids, every card has a basis field, grades only T and C. Output in /tmp/cf1-v/CF1-c-r7/cards_expected.out.',
 'CF1-c-struct-L05': 'L05.html whole page re-read: sections s1 to s9 in order, Lab 1 section with hypothesis, twin output block and interpretation, key-results table (7 rows, T or C), eight quiz items plus the numeric items, references list, lesson-nav. Pre-existing structure unchanged apart from the rewritten sentences above.',
 'CF1-c-struct-L06': 'L06.html whole page re-read: sections s1 to s9 in order, Lab 1 section, key-results table (7 rows, T or C), quiz, references, lesson-nav. Only change in this delta: one key-results row removed.',
 'CF1-c-banned-scan': 'grep -i -E over L05.html and L06.html for build, builder, round, verifier, REQUESTS, unit report, TODO, TBD, lorem, roughly half, historically, studies show, it is important to note, for brevity, beyond the scope, can be shown: no learner-text hits. One hit for "unrounded" at L05.html line 273 (arithmetic term in M2 solution, not a process word).',
 'CF1-c-prose-process-path': 'Same grep as CF1-c-banned-scan for process words over both learner texts and cards.json L05/L06 cards: no hits.',
 'CF1-c-cmd-pin': 'git rev-parse HEAD in /tmp/verify7-CF1-c: de53f7e (detached). Delta from previous pin d57df1e: git diff --stat d57df1e de53f7e -- L05.html L06.html cards.json and both twins: L05.html 11 lines, L06.html 1 line, cards.json 165 lines; twins empty.',
 'CF1-c-cmd-check_pages': 'tools/check_pages.py --all (run this round): output includes "check_pages CF1: PASS", exit 0.',
 'CF1-c-cmd-check_dag': 'tools/check_dag.py --all (run this round): output includes "check_dag CF1: PASS". Concepts: payback-period defined once (L05 line 58 dfn), monte-carlo-npv once (L06 line 63 dfn).',
 'CF1-c-cmd-run_labs': 'tools/run_labs.py --unit CF1 (run this round): "run_labs CF1: PASS (9/9)", exit 0.',
 'CF1-c-cmd-page_smoke': 'tools/page_smoke.py --unit CF1 --pages L05 L06 (run this round): L05 PASS, L06 PASS, "page_smoke CF1: PASS".',
 'CF1-c-cmd-ruff-mypy-labs': 'Run this round: ruff check tests/labs/CF1/ "All checks passed!"; ruff format --check tests/labs/CF1/ "9 files already formatted"; mypy --no-incremental on lab-CF1-L05-1.py and lab-CF1-L06-1.py "Success: no issues found in 2 source files".',
 'CF1-c-cmd-verify_refs': 'tools/verify_refs.py --offline (run this round): "offline integrity: 560 entries, 0 problems". tools/verify_refs.py --unit CF1 (run this round): "live re-verification of CF1: 2 of 560 entries, 0 problems". Live run for the full registry not repeated.',
 'CF1-c-cmd-twin-vs-page': 'Run this round: python -I -W error on both twins exit 0. Script ledgers/CF1/scripts/CF1-c-r7/r7_cards_expected.py: L05 expected block 10 lines, output 10 lines, identical True; L06 12 lines, identical True.',
 'CF1-c-lab-L05-1-run': 'python -I -W error tests/labs/CF1/lab-CF1-L05-1.py: exit 0, 10 lines printed, identical to the page expected block (identical True). Twin unchanged in this delta (git diff empty).',
 'CF1-c-lab-L06-1-run': 'python -I -W error tests/labs/CF1/lab-CF1-L06-1.py: exit 0, 12 lines, identical to the page expected block (identical True). Twin unchanged in this delta.',
 'CF1-c-twin-freshness': 'git diff --stat d57df1e de53f7e -- tests/labs/CF1/lab-CF1-L05-1.py tests/labs/CF1/lab-CF1-L06-1.py: empty (0 lines). Both twins unchanged in this delta, so the lab runs above are the runs of the current twins.',
 'CF1-c-hours': 'data-hours="8" on L05.html and L06.html (grep this round); index.html data-hours-lessons="48" (6 x 8), data-hours-project="12"; project.html data-hours-project="12". Arithmetic consistent. Pace not judged (architect ruling).',
 'CF1-c-concepts': 'L05.html line 58 dfn payback-period and L06.html line 63 dfn monte-carlo-npv: one dfn each (grep this round). check_dag CF1 PASS.',
}
NEW = {
 'id': 'CF1-c-scope-L05-prop22-existence',
 'check': 'Proposition 2.2 hypothesis (both paybacks exist) carried into the key-results row, quiz item L05q4 and card CF1-c065',
 'location': 'L05.html key-results row (line 368); quiz item L05q4 (lines 404-406); cards.json CF1-c065',
 'status': 'FAIL',
 'evidence': 'Proposition 2.2 (L05.html lines 85-88) reads "suppose tau_S and tau_D exist. Then tau_D >= tau_S". The Section 4 bullet (line 229) was fixed this round to state "when both paybacks exist". The key-results row says "For conventional flows and a rate of zero or more, the discounted payback year is at least the simple payback year (Proposition 2.2)", the quiz option says "It is the same or later", and card CF1-c065 says "The discounted year is the same or later" with no existence condition. Recomputed (python -I ledgers/CF1/scripts/CF1-c-r7/r7_check.py is the arithmetic; the counterexample search used 200000 random conventional vectors): 0 counterexamples to tau_D >= tau_S where both paybacks exist, so the claim is true with the condition and the omission is a scope defect, not a false number. Where the discounted payback is none the comparison is undefined, so the statement needs the condition.',
 'fix': 'Add "when both paybacks exist" to the key-results row (L05.html line 368), to the quiz option at line 406 (for example "It is the same or later when both paybacks exist, because ..."), and to the front and back of cards.json CF1-c065 (and regenerate cards only through the source; cards.json is generated per CLAUDE.md rule 1 if the source is a yaml, otherwise edit the source that produces it).',
}
rows = []
for rid, r in rows_in.items():
    row = dict(r)
    if rid in FRESH:
        row['evidence'] = FRESH[rid]
        row['status'] = 'PASS'
    if rid == 'CF1-c-cards-L05':
        row['status'] = 'FAIL'
        row['evidence'] = FRESH['CF1-c-cards-L05']
        row['fix'] = 'See CF1-c-scope-L05-prop22-existence: add the existence condition to card CF1-c065.'
    if rid == 'CF1-c-prose-L05-E1-section2-locator' or rid in FRESH:
        pass
    elif row['status'] == 'PASS' and not row['evidence'].startswith('Carried from round'):
        pass
    elif row['status'] == 'PASS':
        rest = row['evidence'].split('): ', 1)[1] if row['evidence'].startswith('Carried from round') else row['evidence']
        row['evidence'] = ('Carried from round 6 (course/modules/CF/CF1/L05.html, L06.html, tests/labs/CF1/lab-CF1-L05-1.py and lab-CF1-L06-1.py byte-identical since the previous pin d57df1e for the cited span; the cited span did not change in the d57df1e..de53f7e delta): ' + rest)
    if row['status'] == 'FAIL' and 'fix' not in row:
        row['fix'] = 'see evidence'
    rows.append(row)
# carried rows whose span moved only by line number
for r in rows:
    if r['id'] == 'CF1-c-num-L05-gap':
        r['evidence'] = r['evidence'] + ' Row text unchanged this round; it now sits at key-results line ~370 after the "Open" row was removed.'
rows.append(NEW)
for r in rows:
    if r['status'] != 'FAIL' or r.get('fix') is None:
        r.pop('fix', None)
ids = [r['id'] for r in rows]
assert len(ids) == len(set(ids))
summary = {'rows': len(rows), 'PASS': sum(r['status']=='PASS' for r in rows), 'FAIL': sum(r['status']=='FAIL' for r in rows), 'UNVERIFIABLE': sum(r['status']=='UNVERIFIABLE' for r in rows)}
frag = {
 'unit': 'CF1', 'slice': 'CF1-c', 'round': 7,
 'verifier': 'independent verifier (Haiku), CF1 slice c (L05, L06 and their lab twins), round 7; did not build CF1; shares no context with the builders or the round 1 to 6 verifiers',
 'pin': 'de53f7e', 'base': 'd57df1e',
 'checkout': '/tmp/verify7-CF1-c (detached worktree at de53f7e; .venv symlinked)',
 'scratch': '/tmp/cf1-v/CF1-c-r7',
 'verified_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
 'verdict': 'FAIL' if summary['FAIL'] else 'PASS',
 'verdict_basis': 'FAIL: CF1-c-scope-L05-prop22-existence (Proposition 2.2 stated without its existence condition in the key-results row, quiz item L05q4 and card CF1-c065) and CF1-c-cards-L05 (same card). All three round-6 FAIL rows are resolved (CF1-c-grade-L05, CF1-c-grade-L06, CF1-c-prose-L05-E1-section2-locator).',
 'rows': rows,
 'mutants': [],
 'registry_flags': R6.get('registry_flags', []),
 'freshness_flags': [],
 'notes': [
  'Delta d57df1e..de53f7e for this slice: L05.html hunks at lines 52, 199-202 (interpretation), 226-229 (Section 4 bullet), 233 (fifth-defect paragraph), 313-316 (E1 solution), 371-374 (key-results "Open" row removed); L06.html one key-results row removed (line 368-371); cards.json: a basis field added to most cards (CF1-c062 to c100) and a trailing comma on grade lines. Twins unchanged. All other rows carried with the byte-identical prefix.',
  'Lesson-only slice (no grader, no project): no student-error mutants and no alternative-implementation runs, as in rounds 3 to 6. The twins were run as they are. Random-search check of Proposition 2.2 (200000 conventional vectors, rates 0 to 1.5) was a scratch check of the claim, not a grader run.',
  'Not checked: Graham and Harvey (2001) was not read (no fetch was attempted; no access restriction was tested). Glasserman (2003) was not read. Attribution rows rest on the registry record and the pages own statements.',
  'Not checked: the symbol-by-symbol notation conformity with notation/notation.json was not redone this round.',
  'Not checked: the full live verify_refs run (only CF1 live, 2 of 560 entries, as the tool reports).',
  'Not checked: pytest suite; the card-basis script reports "NOT FOUND" for three basis labels that are not literal lesson strings (Problem R2, Section 5 misconception labels); these were checked by reading the lesson (R2 is the problem with that id in Section 6; the misconceptions are the first and second items of Section 5).',
  'Not checked: index.html, project.html and the AC1/M1/AC4 files changed in the delta are outside slice c.',
 ],
 'summary': summary,
}
json.dump(frag, open('/tmp/verify7-CF1-c/ledgers/CF1/CF1-c.json', 'w'), indent=1, ensure_ascii=False)
print(summary, frag['verdict'])
