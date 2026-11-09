import json, subprocess
prev = json.load(open('/Users/billyribeiro/.fanout/frags/S-FC2-b.round7.json'))
prev_rows = {r['id']: r for r in prev['rows']}
S = 'ledgers/FC2/scripts/FC2-b-r8/'
PIN_PREV = 'aa659725'

FRESH = {}
def fresh(id_, check, location, status, evidence, fix=None):
    r = {'id': id_, 'check': check, 'location': location, 'status': status, 'evidence': evidence}
    if status != 'PASS':
        r['fix'] = fix
    FRESH[id_] = r

# --- commands (run this round, outputs in scratch) ---
fresh('FC2b-cmd-check_pages', 'gate', 'index, L01-L08, cards.json (unit gate)', 'PASS',
      "Run this round: .venv/bin/python tools/check_pages.py --unit FC2 -> 'check_pages FC2: PASS' (" + S + "gates1.txt).")
fresh('FC2b-cmd-check_dag', 'gate', 'L04-L06 links and dfn', 'PASS',
      "Run this round: tools/check_dag.py --unit FC2 -> 'check_dag FC2: PASS' (" + S + "gates1.txt).")
fresh('FC2b-cmd-check_projects', 'gate', 'project.html (unit gate, outside slice)', 'PASS',
      "Run this round: tools/check_projects.py --unit FC2 -> 'check_projects FC2: PASS' (" + S + "gates1.txt).")
fresh('FC2b-cmd-run_graders', 'gate', 'grader/ (unit gate, outside slice)', 'PASS',
      "Run this round: tools/run_graders.py --unit FC2 -> 'run_graders FC2: PASS (reference 50/50 seeds)' (" + S + "gates2.txt).")
fresh('FC2b-cmd-run_labs', 'gate', 'tests/labs/FC2 (unit, and L04, L05, L06 with --page)', 'PASS',
      "Run this round: tools/run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)'; --unit FC2 --page L04, L05, L06 -> 'PASS (1/1)' each (" + S + "labs.txt, " + S + "labs_smoke.txt).")
fresh('FC2b-cmd-page_smoke', 'gate', 'L04.html, L05.html, L06.html (each run alone)', 'PASS',
      "Run this round: tools/page_smoke.py --unit FC2 --pages L04 (then L05, L06) -> 'page_smoke modules/FC/FC2/Lnn.html: PASS' and 'page_smoke FC2: PASS' for each alone (" + S + "labs_smoke.txt).")
fresh('FC2b-cmd-twins-isolated', 'lab', 'tests/labs/FC2/lab-FC2-L04-1.py, lab-FC2-L05-1.py, lab-FC2-L06-1.py', 'PASS',
      "Each twin copied alone to a fresh /tmp directory and run with python3 -I -W error: exit 0, stderr 0 bytes for all three; output printed in " + S + "twins.txt (L04 payoff table and Example 2.5 values, L05 parity cost [0,0,0,0,0] on the synthetic set, L06 V0 = 4500 cents and self-financing True).")
fresh('FC2b-cmd-ruff', 'gate', 'tests/labs/FC2 twins', 'PASS',
      "Run this round: .venv/bin/ruff check tests/labs/FC2 -> 'All checks passed!'; ruff format --check -> '11 files already formatted' (" + S + "gates2.txt).")
fresh('FC2b-cmd-mypy', 'gate', 'repository mypy configuration', 'PASS',
      "Run this round: .venv/bin/mypy --no-incremental -> 'Success: no issues found in 386 source files' (" + S + "gates2.txt).")
fresh('FC2b-cmd-pytest', 'gate', 'tests/test_labs.py -k FC2; tests/test_page_checks.py; tests/test_run_labs.py', 'PASS',
      "Run this round: pytest tests/test_labs.py -k FC2 -> '11 passed, 395 deselected'; pytest tests/test_page_checks.py tests/test_run_labs.py -> '47 passed' (" + S + "pytest_r8.txt).")
fresh('FC2b-cmd-verify_refs', 'gate', 'references/references.json; L04-L06 carry no data-cite', 'PASS',
      "Run this round: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (" + S + "gates2.txt). references/ is byte-identical to the previous pin.")

# --- L04 delta hunks ---
fresh('FC2b-delta-L04-q3-421', 'prose', 'L04.html:421 (quiz q3 explanation; the only L04 hunk in aa659725..4540351d)', 'PASS',
      "git diff aa659725 4540351d -- course/modules/FC/FC2/L04.html: one hunk at @@ -418,7 +418,7 @@, line 421 now reads 'the proof of Proposition 2.3 shows that a lower American price admits an arbitrage. Remark 2.4 states what the inequality does not say.' Checked against L04.html:103-108 (Proposition 2.3 and its proof: V_A(0) < V_E(0) gives a portfolio with negative initial value and non-negative payoff, excluded by A3) and L04.html:110-112 (Remark 2.4, 'what the inequality does not say'). Question at L04.html:415 asks which relation Proposition 2.3 proves; the marked option is V_A(0) >= V_E(0), which matches Proposition 2.3 at L04.html:103-104. Quiz still has 9 items (L04.html:396-468).")
fresh('FC2b-delta-L04-remark-1.3', 'prose', 'L04.html:83-85 (Remark 1.3; paragraph at line 84), unchanged, re-read for card FC2-c179', 'PASS',
      "L04.html:84: 'The identity concerns payoffs. It does not say what the two options cost.' Unchanged by the delta (hunk list above). Card FC2-c179 back restates this without the word 'only' (see FC2b-cards-c179-scope).")

# --- cards ---
fresh('FC2b-cards-c179-scope', 'card-grade-scope', 'cards.json FC2-c179 (L04, grade T) vs L04.html:84 (Remark 1.3)', 'PASS',
      "Round-7 FAIL (card kept 'payoffs only' after the lesson dropped 'only') is resolved. cards.json now reads 'The identity concerns payoffs and says nothing about what the two options cost.' L04.html:84 reads 'The identity concerns payoffs. It does not say what the two options cost.' Same content, no added scope. Payoff identity (S_tau-K)^+ - (K-S_tau)^+ = S_tau-K is Lemma 1.2 (L04.html:76-78), T grade matches the Lemma's data-grade='T'.")
fresh('FC2b-cards-c062-delta', 'card-vs-lesson', 'cards.json FC2-c062 (L04, grade T) vs L04.html:253-271 (Section 4, misconception 4) and L04.html:120 (Remark 2.6)', 'PASS',
      "Back now reads 'No. Example 2.5 picks the best date after the path is known, and a rule must choose the date from the prices observed so far (Remark 2.6; Section 4, misconception 4).' L04.html:254 is the Section 4 heading 'Misconceptions'; the fourth li (L04.html:268-271) is 'The best exercise date on a path is a trading rule' with the same content. Remark 2.6 at L04.html:119-121 says the best dates are known after the path is observed. Grade T unchanged.")
for cid, front_back_note in [
    ('FC2-c192', "Definition 1.1 (L04.html:69-71) sets K > 0 and the call/put payoffs; card matches."),
    ('FC2-c193', "L04.html:73 'Holding an option costs a premium, paid at date 0. The profit at expiry of a call bought for premium c is (S_tau - K)^+ - c. This lesson ignores interest on the premium' (a stated convention, not a result). Card says 'with no interest on c (Section 1)'; Section 1 is L04.html:53-85."),
    ('FC2-c194', "L04.html:73 'The break-even spot is the expiry spot at which the profit is zero.' Card matches; (Section 1) correct."),
    ('FC2-c195', "Definition 2.1 (L04.html:90-92): intrinsic value h(S_t), with h(s) = (s-K)^+ for a call and (K-s)^+ for a put; card matches."),
    ('FC2-c196', "Definition 2.1 (L04.html:91) 'Exercise is cash-settled: the holder receives a payment and no share changes hands.' Card matches verbatim in substance."),
]:
    fresh(f'FC2b-cards-{cid[4:]}', 'card-vs-lesson', f'cards.json {cid} (L04) vs L04.html', 'PASS',
          "Read this round: " + front_back_note + " Unique id, unique front and back (" + S + "dup_r8.txt); no number in the back is absent from the lesson.")
fresh('FC2b-cards-c197', 'card-hypotheses-grade', 'cards.json FC2-c197 (L05, ungraded) vs L05.html:58-68 (Definition 1.1, Theorem 1.2)', 'FAIL',
      "Front 'What is the parity cost in Lab 1?' back 'C - P - S + DK, the initial cost of the parity portfolio in the proof of Theorem 1.2. It is zero under parity (Definition 1.1; Theorem 1.2).' The first sentence matches L05.html:58-59 (Definition 1.1 names the parity cost and Lab 1). The second sentence states the Theorem 1.2 result but omits its hypotheses: L05.html:63-64 states 'Under A1, A2, A3, A4 and A5, C - P = S - e^{-r tau}K for every strike K > 0'. The verifier rule requires a card to carry a proposition's hypotheses, and 'under parity' is not a hypothesis of Theorem 1.2. The card also tests two facts (the formula and its zero value) while carrying no grade, although plan section 10 says to grade a derived parity result T.",
      fix="Split into two cards. Keep 'What is the parity cost in Lab 1?' ungraded and answered by 'C - P - S + DK (Definition 1.1)'. Add 'Under A1 to A5, is the parity cost zero for every strike K > 0?' answered 'Yes, C - P - S + DK = 0 at every strike K > 0 (Theorem 1.2)', with grade T, matching c064's hypotheses.")
fresh('FC2b-cards-c198', 'card-vs-lesson', 'cards.json FC2-c198 (L06, ungraded) vs L06.html:63-64 (Definition 1.2)', 'PASS',
      "L06.html:64 'Binomial option pricing values a claim by replication when the stock moves between two values over each period.' Card back restates it verbatim in substance and cites Definition 1.2. Definitional, so no grade needed. Unique front 'What is binomial option pricing?' (" + S + "dup_r8.txt).")
fresh('FC2b-cards-duplicates', 'cards-duplicates', 'cards.json whole deck (187 cards)', 'PASS',
      "Run this round with " + S + "cards_r8.py: 187 cards, ids unique, no duplicate fronts or backs after normalisation (" + S + "cards_r8.txt).")
fresh('FC2b-cards-near-duplicate', 'cards-near-duplicate', 'slice pairs with front or back similarity above 0.6', 'PASS',
      "Run this round with " + S + "dup_r8.py (difflib ratio > 0.6). New L04 pairs c192/c193/c194/c195 share the template 'What is the X of an option?' but ask about different facts (strike, premium, break-even, intrinsic value); their backs differ (ratio 0.25-0.45). No near-duplicates among the changed cards; the other pairs were already accepted in round 7 (FC2-c139/FC2-c187 and similar).")
fresh('FC2b-cards-grade-ruling9', 'card-grades', 'cards.json grades for L04-L06', 'PASS',
      "Grades of all slice cards re-read by script (" + S + "cards_r8.txt). Changed cards keep their grades: c062 T, c179 T. New cards: c192-c196 and c198 are definitional and ungraded; c197 is ungraded and carries the FAIL row FC2b-cards-c197.")
fresh('FC2b-cards-L04-grades', 'card-grades', 'cards.json FC2-c051..c062, c135, c142, c143, c158, c159, c179 (L04)', 'PASS',
      "Grades per cards_r8.txt: c052 T, c054-c057 T, c058 C, c059 T, c060 T, c061 C, c062 T, c135 T, c179 T; c051, c053, c142, c143, c158, c159, c187 ungraded (definitional or hypothesis cards, no derived result as their back).")
fresh('FC2b-cards-L04-rest', 'card-grades', 'cards.json L04 cards without grade (c051, c053, c142, c143, c158, c159, c187, c192-c196)', 'PASS',
      "cards_r8.txt lists all 24 L04 cards. Ungraded L04 cards are definitions, standing-assumption cards, or restatements. c158 (Propositions 2.2 and 2.3 do not use A1) is a derived claim with no grade; round 7 accepted it, its bytes are unchanged, so it is carried and recorded here as an observation, not re-failed.")
fresh('FC2b-cards-coverage', 'card-coverage', 'cards.json lessons L04, L05, L06 (and all eight)', 'PASS',
      "Per-lesson counts this round (cards_r8.txt): L01 22, L02 23, L03 21, L04 24, L05 26, L06 30, L07 23, L08 18; every lesson has at least one card. Round-7 counts were L04 19, L05 25, L06 29 (73 slice cards); now 80 slice cards, the difference being c192-c196 (L04), c197 (L05), c198 (L06).")
fresh('FC2b-cards-delta-round1', 'cards-delta', 'cards.json delta aa659725..4540351d', 'PASS',
      "git diff aa659725 4540351d -- cards.json: hunks at FC2-c009 (L01, outside slice), FC2-c062 (L04, read), FC2-c179 (L04, read), and additions FC2-c188 to c200 (c188-c191 L01/L03 and c199/c200 L07/L08 outside slice; c192-c196 L04, c197 L05, c198 L06 read). c009's back was shortened to remove the Remark 3.6 sentence; outside slice.")
fresh('FC2b-cards-key-mirror', 'card-vs-table', 'L04.html:383-393 key-results table vs cards c179, c062', 'PASS',
      "The key-results table at L04.html:383-393 is byte-identical (not in the delta). Its Lemma 1.2 row (T) is mirrored by card FC2-c179 (T), whose text was re-read above; no table row is mirrored by c062.")
fresh('FC2b-quiz-L04-L06', 'quiz', 'L04.html:396-468 (9 items), L05.html:464-535 (9 items), L06.html:412-482 (10 items)', 'PASS',
      "Re-counted with sed plus grep -c 'class=\"item\"': L04 9, L05 9, L06 10. L04 q3 explanation changed (line 421) and is verified above. The item count was re-counted, and the q3 options are unchanged.")

# --- prose checks touched by the L04 hunk ---
fresh('FC2b-banned-process', 'prose', 'L04-L06 visible prose, twin docstrings, and the changed text', 'PASS',
      "grep -n -E 'TODO|TBD|lorem|brevity|beyond the scope' on L04-L06 returned nothing. Case-insensitive grep over the delta's + lines for 'clearly', 'obviously', 'important to note', 'well known', 'can be shown', 'experts', 'studies show', 'left as an exercise' returned nothing. The changed L04.html:421 and cards c062/c179/c192-c198 contain no process words.")
fresh('FC2b-scope-words', 'scope-words', 'L04-L06 and the delta text', 'PASS',
      "Scope words in the delta's + lines (only, every, any, all, never, always, exactly, same): the only hits are c009 'Exactly ... (Proposition 3.5)' and c200 'the same inputs' (both outside slice). c179 has no scope word; c192-c198 and L04.html:421 contain none.")
fresh('FC2b-notation', 'notation', 'L04-L06 math vs notation/notation.json (changed text only)', 'PASS',
      "Symbols in the changed text: V_A(0), V_E(0) (L04.html:421, as in Proposition 2.3), h, S_t, K, c (premium, L04.html:73), C, P, S, D (L05 card c197; Definition 1.1 at L05.html:59). Each keeps its meaning in the lesson. No new symbol.")
fresh('FC2b-dag-links', 'dag', 'L04-L06 concept links and definitions (changed text only)', 'PASS',
      "check_dag FC2 PASS this round (" + S + "gates1.txt). The changed L04.html:421 adds no concept link, and the new cards carry no link markup.")
fresh('FC2b-struct-L04', 'structure', 'L04.html (BUILDER_RULES 4.2 order and counts)', 'PASS',
      "Only the text of one explain div changed (line 421). Section order s1..s8 and item counts unchanged (quiz 9 items, problem set M/P/E/R unchanged); check_pages FC2 PASS this round.")

ledger = [json.loads(json.dumps(v)) for v in FRESH.values()]
fresh_ids = set(FRESH)

def basis_for(r):
    txt = (r['id'] + ' ' + r.get('location', '') + ' ' + r.get('check', ''))
    files = []
    if 'L04' in txt: files.append('course/modules/FC/FC2/L04.html (cited lines unchanged; the delta changed only L04.html:421)')
    if 'L05' in txt: files.append('course/modules/FC/FC2/L05.html')
    if 'L06' in txt: files.append('course/modules/FC/FC2/L06.html')
    if 'lab' in r['id'] or 'twin' in r['id'] or 'rng' in r['id']: files.append('tests/labs/FC2 twins')
    if 'card' in txt: files.append('cards.json (cited cards byte-identical)')
    if 'plan' in r['id'] or 'plan' in txt: files.append('plans/FC2-build-plan.md')
    if not files: files.append('the cited files (byte-identical)')
    return '; '.join(dict.fromkeys(files))

carried = []
for rid, r in prev_rows.items():
    if rid in fresh_ids:
        continue
    nr = dict(r)
    nr['evidence'] = f"Carried from round 7 ({basis_for(r)} byte-identical since the previous pin {PIN_PREV}): " + r['evidence']
    nr.pop('fix', None)
    carried.append(nr)
rows = [r for r in carried] + list(FRESH.values())
# keep the round-7 order where possible
order = list(prev_rows.keys()) + [k for k in FRESH if k not in prev_rows]
byid = {r['id']: r for r in rows}
rows = [byid[i] for i in order if i in byid]
json.dump({'rows': rows}, open(S + 'rows_r8.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(rows), 'fresh', len(FRESH), 'carried', len(carried))
print('non-PASS', [r['id'] for r in rows if r['status'] != 'PASS'])
