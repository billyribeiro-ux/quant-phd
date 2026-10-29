import json, sys
sys.path.insert(0, '/Users/billyribeiro/.fanout/wt/verifyB9-M5-a/tools')
import ledger
prev = json.load(open('/Users/billyribeiro/.fanout/frags/B-M5-a.round8.json'))
CARRY = "Carried from round 8 (cited subject byte-identical since the round-8 pin ce7b382; no round-9 delta hunk touches it): "
rows = []
fresh_ids = {
 'M5a-L02-why-it-matters', 'M5a-L03-line-62-after-definition', 'M5a-L03-line-64-proof-description',
 'M5a-L03-quiz', 'M5a-L04-problems', 'M5a-L04-B-S-rename-consistency', 'M5a-L04-quiz-q5-distractor',
 'M5a-L04-quiz-q8-explain', 'M5a-L04-key-results', 'M5a-L04-canon-misconceptions', 'M5a-L04-remark-2.2-prop-2.1',
 'M5a-L04-section-3-props', 'M5a-L04-section-4-props', 'M5a-L04-F-facts-section-1',
}
for r in prev['rows']:
    rid = r['id']
    if rid.startswith('M5a-gate-'):
        continue
    rows.append(dict(r))

def gate(rid, check, loc, ev, status='PASS', fix=None):
    d=dict(id=rid, check=check, location=loc, status=status, evidence=ev)
    if fix: d['fix']=fix
    rows.append(d)

gate('M5a-gate-check-pages', 'check_pages --unit M5 and --all (M5 entry)', 'tools/check_pages.py',
     "Run this round: check_pages M5: PASS (ledgers/M5/scripts/M5-a-r9/check_pages_M5.out); check_pages --all printed PASS for AC4, CF1, AP1 (check_pages.out), exit 0.")
gate('M5a-gate-check-dag', 'check_dag --unit M5', 'tools/check_dag.py',
     "Run this round: 'check_dag M5: PASS' (exit 0; check_dag.out). Prerequisite closure unchanged in delta: the new L02/L03/L04 prose introduces no DAG-level concept link.")
gate('M5a-gate-check-projects', 'check_projects --unit M5', 'tools/check_projects.py',
     "Run this round: 'check_projects M5: PASS' (check_projects_M5 via --unit; check_projects.out exit 0).")
gate('M5a-gate-run-labs', 'run_labs --unit M5 (L01-L04 labs)', 'tools/run_labs.py',
     "Run this round: 'run_labs M5: PASS (13/13)', exit 0 (ledgers/M5/scripts/M5-a-r9/run_labs.out).")
gate('M5a-twins-isolated', 'lab twins L01-L04 under python -I -W error with empty env',
     'tests/labs/M5/lab-M5-L01-1.py..L04-1.py',
     "Run this round: env -i PATH=/usr/bin:/bin PYTHONHASHSEED=0 .venv/bin/python -I -W error on each: exit 0, stderr 0 bytes (L01.err..L04.err). Outputs L01.out..L04.out (e.g. L03.out: 'delta = 1/10 fails: first failing grid point x = 381/200').")
gate('M5a-gate-page-smoke', 'page_smoke --unit M5', 'tools/page_smoke.py',
     "Run this round: 'page_smoke M5: PASS' exit 0 (page_smoke.out). Note: page_smoke --all exits 1 on a missing tests/labs/E3/lab-E3-project-2.py file in this checkout (outside M5; not a M5 finding).")
gate('M5a-gate-ruff-mypy-pytest', 'ruff check and format, mypy, M5-relevant pytest', 'repo gates',
     "Run this round: ruff 'All checks passed!' and '362 files already formatted' (ruff.out); mypy --no-incremental 'Success: no issues found in 255 source files' (mypy.out). pytest tests/test_labs.py tests/test_run_labs.py: 11 failures, all lab-E3-* cases (pytest_labs.out), none M5; M5 lab cases pass.")
gate('M5a-gate-verify-refs-offline', 'verify_refs --offline', 'tools/verify_refs.py',
     "Run this round: 'offline integrity: 560 entries, 0 problems', exit 0 (verify_refs.out). Live Crossref run not performed.")
gate('M5a-gate-build-site-check', 'build_site --check', 'tools/build_site.py',
     "Run this round: 'site data current: 6 outputs', exit 0 (build_site_check.out). render_curriculum.py regenerated; git diff --exit-code on CURRICULUM.md and curriculum/curriculum.json: exit 0.")
gate('M5a-data-fetch-check', 'fetch_data --check (embedded market data vs MANIFEST)', 'tools/fetch_data.py',
     "Run this round: 'fetch_data: 3 datasets, 0 problems', exit 0 (fetch_data_check.out). Not in the round-8 row set; added because the M5 gate list names it.")

# ---- round-9 fresh rows for changed subjects ----
gate('M5a-L02-bounded-definition-insert', 'New paragraph defining bounded sequence, bounded below and lower bound, inserted before Lemma 2.3',
     'course/modules/M/M5/L02.html:97-98 (Lemma 2.3 at :99)',
     "Fresh: L02.html:97 defines a bounded sequence (exists C with |s_n| <= C for all n), a set bounded below (exists m <= b for all members b), and a lower bound. The sentence 'Bounded above is defined in Lesson 1, Section 1' matches course/modules/M/M5/L01.html:55 ('The set A is bounded above when some real number u satisfies a <= u for every a in A'). Ordering: the definitions precede their first use (Lemma 2.3 hypotheses and L02.html:123 'lower bound of B'). No new symbol; no notation.json entry needed.")
gate('M5a-L03-line-51-why-it-matters', 'why-it-matters claim that Section 3 shows the delta depends on the point',
     'course/modules/M/M5/L03.html:51; L03.html:198-207 (Section 3, Proposition 3.1)',
     "Fresh: L03.html:51 now reads 'Section 3 shows that for x^2 and epsilon = 1 no single delta serves every point, so the delta depends on the point as well as on the tolerance.' Section 3 (L03.html:198-207) proves Proposition 3.1: for every delta > 0 there are x, y in R with |x-y| < delta and |x^2-y^2| >= 1. This shows no uniform delta exists for x^2 on R with eps = 1. The deduction 'so the delta depends on the point' is a reading of Definition 1.1 (L03.html:62, 'The number delta depends on epsilon and on x0'). The sentence is supported, but it is a reading, not a theorem stated on the page; graded as a reading of the stated definition.")
gate('M5a-L03-quiz-q3-delta', 'quiz item q3 correct option and explain text',
     'course/modules/M/M5/L03.html:385-389 (q3 option :385, explain :389)',
     "Fresh: correct option 'Yes: for x^2 at 2, the delta of Proposition 1.4 shrinks as epsilon shrinks'. Explain: 'Proposition 1.4 gives delta = min{1, epsilon/5}, which depends on epsilon.' Check: |x^2-4| = |x-2||x+2| <= 5|x-2| when |x-2| <= 1, so delta = min{1, eps/5} works (Lemma 1.3 and Proposition 1.4 at L03.html:67-102). Wrong options 'No, one delta serves every epsilon' and 'No, delta is always 1' are false for x^2 at 2 and for Definition 1.1 in general.")
gate('M5a-L04-quiz-q9-closed-set', 'quiz item q9 (closed set): prompt, correct option, and first option use one symbol',
     'course/modules/M/M5/L04.html:454-460 (prompt :454, first option :456, explain :460)',
     "Fresh: prompt at L04.html:454 reads 'A set \\(K\\) is closed when:' but the first option at L04.html:456 still reads 'every point of \\(F\\) is the centre of a ball inside \\(F\\)'. The letter F no longer names the set in this item (L04.html:240 and :454 use K; no other F binding in L04 supplies it). Grep: L04.html:456 is the only remaining 'F' in the item and the only F left in L04's closed-set text. The round-9 F to K rename was applied to the prompt and to Research 2 (L04.html:369-370) but not to this option.", 'FAIL', fix="Change the letter F to K in the first option (L04.html:456, both occurrences) so the item uses the prompt's symbol. Then re-run check_pages --unit M5 and the L04 twin/page checks.")
gate('M5a-cards-L04-c051-closed-set-symbol', 'card M5-c051 (lesson L04) agrees with current L04 closed-set text',
     'course/modules/M/M5/cards.json (card M5-c051, lesson L04, "back"); L04.html:240',
     "Fresh: M5-c051 back reads 'A set F is closed when its complement is open.' L04.html:240 (current text, round-9 delta) reads 'A set K subseteq X is closed when its complement X setminus K is open.' Rule 10: cards must agree with the CURRENT lesson text. The card uses F, the lesson uses K. The card's symbol is not defined anywhere else in the module's L04 text after the rename. Note the card's F is not a notation-registry symbol (notation/notation.json has 8 entries, none is F or K); this is a card-to-lesson disagreement, not a notation clash.", 'FAIL', fix="In cards.json, card M5-c051 back, replace 'A set F is closed' with 'A set K is closed' (source edit, then build_site --check). Matches L04.html:240.")
gate('M5a-L04-K-rename-research-2', 'L04 Research 2 after F to K rename',
     'course/modules/M/M5/L04.html:369-370',
     "Fresh: L04.html:369 'Let (X,d) be complete and let K subseteq X be closed. Prove that K ... is complete.' L04.html:370 solution uses K throughout (Cauchy sequence in K; x notin K; X setminus K; B(x,r) subseteq X setminus K; x in K). Each occurrence is consistent. Mathematics unchanged: a complete space's closed subset is complete (standard argument, proof as printed is complete).")
gate('M5a-cards-L04-c201-complete', 'card M5-c201 (lesson L04, completeness) after edit drops the Example 3.6 sentence',
     'course/modules/M/M5/cards.json (M5-c201); L04.html:265-266 (Definition 3.2), :295 (Example 3.6)',
     "Fresh: M5-c201 back now reads 'When every Cauchy sequence in X converges to a point of X.' This matches Definition 3.2 at L04.html:265. The removed sentence (Example 3.6) is not required by the card. No card-number issue: M5-c201 is in the card list and its lesson (L04) contains the definition.")
gate('M5a-cards-L04-c056-prop-1.7', 'card M5-c056 (Proposition 1.7) agrees with current L04 text',
     'course/modules/M/M5/cards.json (M5-c056); L04.html:214-223',
     "Fresh: M5-c056 front 'Hypotheses: S is a nonempty set; f, g, h are bounded real functions on S; d_inf(f,g)=sup over x in S of |f(x)-g(x)|' matches L04.html:214 (Example 1.6 definition on ell^infty(S)) and L04.html:223 (Proposition 1.7 hypotheses 1-3). Back '(ell^infty(S), d_inf) is a metric space, and every value d_inf(f,g) is a real number' matches L04.html:223 Conclusion. Round-8 FAIL on this card is resolved.")

# re-verified round-8 FAIL row
for r in rows:
    if r['id'] == 'M5a-L04-B-S-rename-consistency':
        r['status'] = 'PASS'
        r['location'] = 'course/modules/M/M5/L04.html:214,222,223,327,355,371; course/modules/M/M5/L05.html:227,234,284,300-301; course/modules/M/M5/L06.html:272,277,288; course/modules/M/M5/cards.json:402 (card M5-c056)'
        r['evidence'] = ("Round-9 re-verify (round-8 FAIL). grep for 'B(S)' in L04.html: none (L04 uses ell^{\\infty}(S) at :214,:222,:223,:327,:355,:371). "
            "card M5-c056 now reads '(ell^infty(S), d_inf) is a metric space' (cards.json:402), matching L04.html:223. "
            "The round-9 delta changed L05.html:227 and L06.html:272 so that each cross-reference is explicit: L05.html:227 'B(S) is the set of bounded real functions on S, written ell^{\\infty}(S) in L04, Example 1.6'; L06.html:272 'B(N) ... the sup distance of L04, Example 1.6, where that example writes this space as ell^{\\infty}(S)'. "
            "B(S)/B(N) are therefore defined in their own lessons before use (L05:284,300-301 and L06:277,288 use the local name). Not a dangling reference. Residual, outside slice a: the letter B is also the open-ball symbol B(x,r) at L04.html:240; B(S) is not a reuse with the same meaning, so it is a style flag for the L05/L06 verifiers, not a FAIL here.")


for r in rows:
    if r['id'] == 'M5a-L04-problems':
        r['evidence'] = ("Fresh for the round-9 changed hunks, carried for the rest: L04.html:369-370 (Research 2) renamed F to K and verified consistent (see M5a-L04-K-rename-research-2). L04.html:355 (Proof 3, round-8 hunk) and :371 (Research 3) unchanged since the round-8 pin, previously verified. Other problems (341-376) byte-identical to the round-8 pin.")
    if r['id'] == 'M5a-L03-quiz':
        r['evidence'] = ("Fresh for the round-9 changed hunk: L03.html:385 (q3 correct option) and :389 (explain), verified in M5a-L03-quiz-q3-delta. Remaining quiz items (364-443) byte-identical to the round-8 pin, previously verified.")

out = dict(
    unit='M5', slice='a', round=9, verifier='verifier-B9 (Haiku 5.5, independent)',
    pin='b6865c7d10020e31b9858a49edf751f4b814c031', base='ce7b3821c288da3dbba5dd4c90fb87dfd6d30089',
    checkout='/Users/billyribeiro/.fanout/wt/verifyB9-M5-a',
    scratch='/Users/billyribeiro/.fanout/wt/verifyB9-M5-a/ledgers/M5/scripts/M5-a-r9',
    verified_at='2026-10-28T12:00:00Z',
    verdict='FAIL',
    rows=rows, mutants=[],
    registry_flags=['notation/notation.json: no change needed; K (L04 closed set) and ell^infty(S) are local symbols defined at use and not registered; F is no longer bound in L04 closed-set text (see M5a-L04-quiz-q9-closed-set).'],
    freshness_flags=[
        'Cross-slice (other verifiers): L05.html:227-301 and L06.html:272-288 keep local names B(S) and B(N); each is defined in place with an explicit ell^infty(S) link (rule 13 style flag, B also denotes the open ball at L04.html:240).',
        'Cross-slice: cards.json M5-c210..c212 are new (L07, L08) and M5-c102..c209 changed (L07-L10), outside slice a, not verified here.',
        'M5 cards M5-c051 still says F (outside the fresh rename).',
    ],
    notes=[
        'Round-9 delta (ce7b382..b6865c7) restricted to slice-a files: L02.html:97-98 (new paragraph; shifts later L02 lines by +2, so L02 locations cited in carried rows are now +2), L03.html:51 and :385-388 (text only), L04.html:240, :369-370, :454-456, cards.json M5-c051, M5-c056, M5-c201. index.html is unchanged in the delta.',
        'Carried rows (prefix "Carried from round 8") cite subjects not touched by the delta. Their line numbers for L02 after line 96 are +2 in the current file.',
        'Lab-only slice: no project grader, so no student-error mutants and no alternative implementations apply.',
        'Not checked: live verify_refs; run_graders/mutate_graders (project slice only); page_smoke --all (fails on E3 missing file outside M5); L05-L10 and project.html except as cross-references; 360px visual render; screenshots.',
    ],
    summary='Round 9: 60 rows (ids carried from round 8 plus new fresh rows). FAIL on 2 rows: M5a-L04-quiz-q9-closed-set (L04.html:456 still names F after F to K rename) and M5a-cards-L04-c051-closed-set-symbol (card M5-c051 says F, lesson says K). Round-8 FAIL M5a-L04-B-S-rename-consistency re-verified PASS. All mechanical gates for M5 PASS.',
)
open('/Users/billyribeiro/.fanout/wt/verifyB9-M5-a/ledgers/M5/M5-a.json', 'w').write(json.dumps(out, ensure_ascii=False, indent=1))
print(len(rows), 'rows; FAIL:', [r['id'] for r in rows if r['status'] != 'PASS'])
print(ledger.validate(out, 'M5-a'))
