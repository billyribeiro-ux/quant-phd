import json, sys
ROOT = sys.argv[1]
base = json.load(open('/Users/billyribeiro/.fanout/frags/S-M2-c.round4.json'))
S = 'ledgers/M2/scripts/M2-c-r1/'
PREFIX = ("Carried from round 4 (course/modules/M/M2/L13.html to L18.html and tests/labs/M2/lab-M2-L13-1.py to "
          "lab-M2-L18-1.py byte-identical since the previous pin edbb7aa8; cards outside the carried card objects unchanged): ")
fresh = {
 'M2c-gate-check-pages': f"Fresh this round: {S}g01_check_pages_M2.out 'check_pages M2: PASS', rc=0 (tools/check_pages.py --unit M2 at 95f3f8cb).",
 'M2c-gate-check-dag': f"Fresh this round: {S}g02_check_dag_M2.out 'check_dag M2: PASS', rc=0.",
 'M2c-gate-run-labs': f"Fresh this round: {S}g04_run_labs_L13.out .. g04_run_labs_L18.out each 'run_labs M2: PASS (1/1)', rc=0 (one call per page).",
 'M2c-gate-check-projects': f"Fresh this round: {S}g03_check_projects_M2.out 'check_projects M2: PASS', rc=0.",
 'M2c-gate-page-smoke': f"Fresh this round: {S}g05_page_smoke_L13_L18.out 'page_smoke modules/M/M2/L13.html ... L18.html: PASS' (six) and 'page_smoke M2: PASS', rc=0.",
 'M2c-gate-pytest': f"Fresh this round: {S}g09_pytest_labs_M2.out 'pytest tests/test_labs.py -k M2': 27 passed, rc=0; collect-only count 27.",
 'M2c-verify-refs': f"Fresh this round: {S}g10_verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' rc=0; {S}g11_verify_refs_unit_M2_live.out 'live re-verification of M2: 2 of 560 entries, 0 problems' rc=0. references/ byte-identical to edbb7aa8 (git diff --quiet).",
 'M2c-labs-lint': f"Fresh this round: {S}g07_ruff_mypy_twins.out: ruff check 'All checks passed!' (rc 0), ruff format --check '6 files already formatted' (rc 0), mypy --no-incremental 'Success: no issues found in 6 source files' (rc 0), on the six twins as separate arguments.",
 'M2c-labs-data': f"Fresh this round: {S}s02_banned_and_process_r1.out: twin file/network tokens [] for all six twins; data-files, data-chart, figure, svg markup 0 on L13 to L18.",
 'M2c-data-figures': f"Fresh this round: {S}s02_banned_and_process_r1.out ('data/figure markup: 0' on L13 to L18) and {S}s06_notation_hours_hub_r1.out ('data-files/data-chart/figure/svg: 0' on all six pages).",
 'M2c-notation': f"Fresh this round: {S}s06_notation_hours_hub_r1.out: registry-symbol and mathbb hits 0 on L13 to L18 (Phi, gamma, ast, mathbb, Q_bb, R_f, R_e_star, SR); notation/ byte-identical to edbb7aa8. The changed cards M2-c187, M2-c233, M2-c263 use only symbols the pages already use (M_3, h^*, delta, h_0, f, g, r, sin, cos).",
 'M2c-banned-scan': f"Fresh this round: {S}s02_banned_and_process_r1.out: 0 banned-phrase hits on the six pages, six twins and the slice cards, except the '...' in the L15 Lab 1 docstring (angles 0, 2 pi/count, 4 pi/count, ...), which is a listed sequence and not a placeholder (observation carried from round 4).",
 'M2c-process-words': f"Fresh this round: {S}s02_banned_and_process_r1.out: 0 process-word hits on the six pages, six twins and the slice cards (includes the changed cards).",
 'M2c-hours': f"Fresh this round: course/modules/M/M2/index.html line 29 data-hours-lessons=\"240\", data-hours-project=\"60\" (240+60=300); the index.html delta hunks are at lines 71 and 130 only (git diff -U0), so line 29 is unchanged; L13..L18 data-hours=\"10\" each (24 x 10 = 240). {S}s06_notation_hours_hub_r1.out.",
 'M2c-cards-sample-01': "Fresh this round (M2-c187 changed): cards M2-c181..M2-c190 read in full and checked against L13 Definition 1.1 (line 58-61), Theorem 2.1 (72-75), Theorem 2.2 (83-86), Definition 3.1 (110-113), Proposition 3.2 (115-118), Corollary 4.1 (133-135, B(h) and h*=2 sqrt(delta/M), B(h*)=2 sqrt(M delta) re-derived), M2-c187 (line 143 and P3 solution line 303, B_c'' = M3/3 + 2delta/h^3 > 0), Example 2.3 (line 102: 0.0135914 = e*0.005, 0.0137280 = e^1.01*0.005; line 102 central 4.4854e-5 and 4.5760e-5 re-derived), ratio bounds 9.990/10.101 and 98.91/101.11 (line 314, 222). All hold. Card M2-c187 (grade T, Problem P3 proves it) checked in full.",
 'M2c-cards-sample-03': "Fresh this round (M2-c208 removed; it duplicates M2-c206, which gives f(2)=15.232760911 and f'(2)=21.731770522, matching L14 line 109 and Lab 1 output line 251): cards M2-c201 (L13 Section 5 corner |t| at line 232), M2-c380 (Assumption 1 list, line 98), M2-c381 (Lab 1 values 2.154e-7 and 1.548e-6, line 222 and twin_L13.stdout), M2-c202..M2-c207 read in full against L14 Definition 1.1, Definition 2.1, Proposition 3.1 (line 80-92, hypotheses and Assumption 1), Example 4.1 (line 109), Lab 1 output (twin_L14.stdout: grid points 251, below 1e-12 True).",
 'M2c-cards-sample-06': "Fresh this round (M2-c233 changed): cards M2-c229..M2-c238 read in full. M2-c229 (line 229 example: g along (1/k,1/k) is 1/2), M2-c230 (Prop 3.5, line 136-137), M2-c231 (Prop 3.6), M2-c232 (360 angles, 1-degree grid contains pi/4), M2-c233 changed: 0.3849 at each radius (L15 lines 218-223 and twin_L15.stdout); 2/(3 sqrt3) = 0.3849001795 rounds to 0.3849002 (E1 line 321; quiz line 456); sampled max of |cos^2 sin| over 360 degrees = 0.3848756 at 325 degrees, strictly below 0.3849001795 (checked with python -I in /tmp/m2c_r1), so 'the sample lies below it' is correct. M2-c234 (E3 line 332-336: f(1/n,1/n)=1/(2n)), M2-c235 (Misconception 1, lines 246-249), M2-c236 (Misconception 2, lines 250-253), M2-c237 and M2-c238 (Section 4, lines 234-243 bullets 1 and 3).",
 'M2c-cards-sample-09': "Fresh this round (M2-c263 changed): cards M2-c261..M2-c270 read in full. M2-c261 (L17 twin t=1e-6, 'below 1e-6: True'), M2-c262 (Misconception 1, L17 line 213-218), M2-c263 changed: L17 line 201 (partial derivatives of g at origin are both 0 by Proposition 3.1 of Lesson L16; directional derivative exists only in the four axis directions) and Misconception 2 (line 217); M2-c264 (Misconception 3; sup-norm corner (1,1) for gradient (1, 1.8776): u1+1.8776 u2 maximal at (1,1)), M2-c265 (Jacobian definition, L18 lines 61-64): statement correct, but the front reads 'F = (F_1, F_2 up to F_m)' where the lesson writes (F_1, ..., F_m) (line 62). This is a LOW wording defect, not a false statement, carried as an observation (see notes), M2-c266 (Definition 3.1 lines 73-77), M2-c267 (Prop 3.2, line 82), M2-c268 (Prop 3.3), M2-c269 (Theorem 4.1, line 105-107, statement matches the card), M2-c270 (Example 4.2: J=[[2,-4],[4,2]] and remainder (s1^2-s2^2, 2 s1 s2) of length |h|^2 re-derived by hand).",
 'M2c-cards-sample-11': "Fresh this round (M2-c419 removed; it duplicates M2-c229, g along (1/k,1/k) equals 1/2): cards M2-c406 (L14 Definition 2.1 rules for exp and sin of dual numbers), M2-c413 (L15 Section 3 continuity definition, lines 99 and onward), M2-c415 (printed values f = 0.050000000 at n = 10 and 0.000050000 at n = 10000 at L15 lines 225 and 228; f(1/n,1/n)=1/(2n) re-derived).",
 'M2c-cards-duplicates': f"Fresh this round: {S}c01_cards_slice_delta.out (cards.json at HEAD vs edbb7aa8): 0 duplicate ids and 0 exact duplicate fronts unit-wide (398 cards); slice near-duplicate fronts (ratio >= 0.80): c182/c183, c188/c189, c191/c192, c194/c195, c228/c229, c232/c233; each pair is a distinct fact (checked). c234/c419 pair gone (c419 removed). Changed cards M2-c187, M2-c233, M2-c263 have no near-duplicate >= 0.70 unit-wide except c232 vs c233 (0.786, distinct).",
 'M2c-cards-numbers': f"Fresh this round: numbers in changed cards checked against lesson text: M2-c187 has no decimal numbers; M2-c233 has 0.3849 (L15 lines 218-223), 0.3849002 (E1 line 321), 360 angles (L15 line 163); {S}c01_cards_slice_delta.out. Other slice cards: see sample rows.",
 'M2c-cards-grades': f"Fresh this round: {S}c01_cards_slice_delta.out: slice cards L13..L18 = 101 (was 103): T 65, C 21, no grade 15. Removed M2-c208 (C) and M2-c419 (T) account for the difference. Every C card has a basis; no T card has a basis (cards.json keys: back, basis, front, grade, id, lesson).",
 'M2c-cards-coverage': f"Fresh this round: L13..L18 blocks (definitions, theorems, misconceptions, problems, labs) unchanged between the pins (pages byte-identical). The two removed slice cards are duplicates: M2-c208 (L14 Lab 1 f1(2), f1'(2)) is covered by M2-c206 (T, L14 line 109); M2-c419 (g along the diagonal = 1/2) is covered by M2-c229 (T). The changed cards M2-c187 (Corollary 4.1 companion, P3), M2-c233 (E1) and M2-c263 (Section 4) cover the same lesson statements as before. No card id references the removed ids (grep for M2-c208 / M2-c419 under course/ returns 0 lines).",
 'M2c-delta-cards-slice': f"Fresh this round: slice-card delta at 95f3f8cb vs edbb7aa8 (cards.json by id): changed M2-c187 (L13), M2-c233 (L15), M2-c263 (L17); removed M2-c208 (L14), M2-c419 (L15); added none in L13..L18 (added M2-c422..c430 belong to L01, L05, L07..L10, L24 and are outside the slice). Each changed card re-verified: M2-c187 (P3 and Corollary 4.1 computed), M2-c233 (0.3849002 / sample below exact, checked numerically), M2-c263 (L17 Section 4 and Misconception 2 match). {S}c01_cards_slice_delta.out.",
 'M2c-L13-lab1': f"Fresh this round: twin run alone under python -I -W error: {S}twin_L13.stdout (rc 0, stderr 0 bytes) is byte-identical to the round-4 twin output (cmp).",
 'M2c-L14-lab1': f"Fresh this round: {S}twin_L14.stdout (rc 0, stderr 0 bytes): 'grid points: 251', 'below 1e-12: True' for f1 and f2, f1(2)=15.2327609113, f1'(2)=21.7317705218 (dual and closed form), f2'(1)=2.5067615350; byte-identical to round-4 twin output.",
 'M2c-L15-lab1': f"Fresh this round: {S}twin_L15.stdout (rc 0, stderr 0 bytes) reproduces the sampled-maximum table 0.500000 / 0.3849 at 1e-01..1e-06; byte-identical to round-4 twin output.",
 'M2c-L16-lab1': f"Fresh this round: {S}twin_L16.stdout (rc 0, stderr 0 bytes); byte-identical to round-4 twin output.",
 'M2c-L17-lab1': f"Fresh this round: {S}twin_L17.stdout (rc 0, stderr 0 bytes): 'below 1e-6: True', gradient (1.000000, 1.877583), magnitude 2.127279, 61.96 degrees; byte-identical to round-4 twin output.",
 'M2c-L18-lab1': f"Fresh this round: {S}twin_L18.stdout (rc 0, stderr 0 bytes); byte-identical to round-4 twin output.",
 'M2c-L13-lab-embed': f"Fresh this round: {S}g04_run_labs_L13.out PASS (run_labs compares page code with the twin and the expected block with the printed output).",
 'M2c-L14-lab-embed': f"Fresh this round: {S}g04_run_labs_L14.out PASS.",
 'M2c-L15-lab-embed': f"Fresh this round: {S}g04_run_labs_L15.out PASS.",
 'M2c-L16-lab-embed': f"Fresh this round: {S}g04_run_labs_L16.out PASS.",
 'M2c-L17-lab-embed': f"Fresh this round: {S}g04_run_labs_L17.out PASS.",
 'M2c-L18-lab-embed': f"Fresh this round: {S}g04_run_labs_L18.out PASS.",
}
extra_carry_note = {}
rows = []
for r in base['rows']:
    rid = r['id']
    if rid in fresh:
        ev = fresh[rid]
    else:
        ev = PREFIX + r['evidence']
    rows.append({'id': rid, 'check': r['check'], 'location': r['location'], 'status': 'PASS', 'evidence': ev})
assert len(rows) == 78 and len({r['id'] for r in rows}) == 78
# guard: every fresh key must be a base row id
assert set(fresh) <= {r['id'] for r in base['rows']}, set(fresh) - {r['id'] for r in base['rows']}
notes = [
 "Closing delta round (ruling 30) of slice c (L13-L18 pages, six lab twins, slice cards) from the round-4 full fragment at pin edbb7aa8 to HEAD 95f3f8cb. git diff edbb7aa8..HEAD: the six pages and six twins are byte-identical (git diff --quiet). Slice-card subjects changed: M2-c187, M2-c233, M2-c263 changed; M2-c208 and M2-c419 removed; none added in L13..L18. Rows whose subject changed were re-verified from scratch (sample-01, -03, -06, -09, -11, cards-duplicates, -numbers, -grades, -coverage, delta-cards-slice, the scan and gate rows). All other rows carried with the carry prefix. Round-4 had no non-PASS rows, so no previous FAIL needed re-verification.",
 "Ruling 37: no new mutants were written. Slice c has no project grader and no mutant set (the base has mutants: []), so the standing mutant set is empty and nothing was run for mutation testing.",
 "Observation, LOW, not blocking under ruling 26 (wording only): cards.json M2-c265 front reads 'F = (F_1, F_2 up to F_m)', while L18 Definition 2.1 (line 62) reads (F_1, ..., F_m). The meaning is unchanged. Suggested fix for the fixer: write 'F = (F_1, ..., F_m)' in the front (or list it in plans/KNOWN-ISSUES.md as a LOW presentation row). Not in the delta; present since before edbb7aa8 and missed by round 4.",
 "Observation, out of slice (not a row of slice c): the hub course/modules/M/M2/index.html line 130 (rung 2 explanation) changed in the delta and now says 'Lesson 13 writes out the expansions ... and subtracts them for the first difference. Adding them, as the rung 2 completion problem does, ...'. Lesson 13 lines 90-93 match that wording (subtraction at line 93); the hub verifier should confirm that the rung-2 attribution now holds (it does on this reading). The arithmetic (1.1^4 + 0.9^4 - 2)/0.01 = 12.02 holds.",
 "Observation: the ... sequence in the L15 Lab 1 docstring (line 193 and twin line 34) is flagged by the banned-token regex. It continues a computed pattern (angles 0, 2 pi/count, 4 pi/count, ...), so it is not a placeholder (carried from round 4).",
 "Not run: run_graders (no project grader in slice c), build_site --check, render_curriculum, the full pytest suite, the repository-wide ruff/mypy gate (only the six twins were linted and type-checked), full verify_refs live run for all 560 entries (only M2's 2 entries, as the round-4 gate), and visual/screenshot checks (the slice pages carry no figures). The existing ledgers/M2/M2-c.json in the checkout (a round-11 fragment at another pin) was overwritten by this fragment as instructed.",
]
summary = ("Slice c, closing delta (round 1 of verifier F21 under ruling 30): 78 rows, all PASS (fail 0, unverifiable 0). "
           "Re-verified fresh: 4 gate rows and 3 lint/ref rows (re-run), 6 twin rows, scan rows (banned, process, labs-data, data-figures, notation, hours), 5 changed-subject sample rows (sample-01, -03, -06, -09, -11), cards-duplicates, -numbers, -grades, -coverage, delta-cards-slice. "
           "Carried (page, twin and card objects byte-identical): all other rows with the carry prefix. "
           "Changed slice cards (M2-c187, M2-c233, M2-c263) verified by hand and numerically; removed duplicates M2-c208 and M2-c419 covered by M2-c206 and M2-c229. "
           "One LOW wording observation (M2-c265 'F_2 up to F_m') recorded in notes, not blocking.")
frag = {
 'unit': 'M2', 'slice': 'c', 'round': 1,
 'verifier': 'Haiku 5.5 independent verifier (fanout F21 slice c, closing delta under rulings 30 and 37)',
 'pin': '95f3f8cb21c2cd9fc904430bd30a6b734d01f672',
 'base': 'edbb7aa8de20e6d2f3035c463a79a318c22623c4 (round-4 fragment /Users/billyribeiro/.fanout/frags/S-M2-c.round4.json, verdict PASS, 78 rows, mutants []). Delta edbb7aa8..95f3f8cb (11 commits).',
 'checkout': ROOT,
 'scratch': ROOT + '/ledgers/M2/scripts/M2-c-r1',
 'verified_at': '2026-11-09',
 'verdict': 'PASS',
 'rows': rows,
 'mutants': [],
 'registry_flags': [],
 'freshness_flags': [],
 'notes': notes,
 'summary': summary,
}
json.dump(frag, open(ROOT + '/ledgers/M2/M2-c.json', 'w'), indent=2, ensure_ascii=False)
print('written', len(rows), 'rows; fresh', len(fresh))
