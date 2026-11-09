# Writes ledgers/CS2/CS2-a.json (round 6). Carried rows take the round-5 evidence text under the carry prefix.
import json, sys
R5 = json.load(open('/Users/billyribeiro/.fanout/frags/S-CS2-a.round5.json'))
r5 = {r['id']: r for r in R5['rows']}
S = 'ledgers/CS2/scripts/CS2-a-r6'
PIN6 = 'e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a'
PIN5 = 'dde0486beeb0312e4ac1cc03aaa02e56644adb24'

def carry(rid, files):
    base = r5[rid]
    return {'id': rid, 'check': base['check'], 'location': base['location'], 'status': 'PASS',
            'evidence': f"Carried from round 5 ({files} byte-identical since the previous pin {PIN5}, git diff --quiet {PIN5} {PIN6}): " + base['evidence']}

def row(rid, check, location, status, evidence, fix=None):
    d = {'id': rid, 'check': check, 'location': location, 'status': status, 'evidence': evidence}
    if status != 'PASS':
        d['fix'] = fix
    return d

rows = []
HUB = 'course/modules/CS/CS2/index.html'
rows.append(carry('SA-HUB-01', HUB))
rows.append(row('SA-HUB-02', r5['SA-HUB-02']['check'], r5['SA-HUB-02']['location'], 'PASS',
    'Re-verified round 6: check_pages --unit CS2 PASS and check_dag --unit CS2 PASS (' + S + '/check_pages.txt, check_dag.txt); index.html byte-identical since '
    + PIN5 + '; the L04 target cited here (L04.html:38, meta row) lies outside every changed hunk of L04.html (git diff -U0 hunks 56,60,98,110,131,134,143,426,446,500,550).'))
rows.append(carry('SA-HUB-03', HUB))
rows.append(carry('SA-HUB-04', HUB))
rows.append(carry('SA-HUB-05', HUB + ', curriculum/01-foundations.yaml, curriculum/curriculum.json'))
rows.append(row('SA-HUB-06', r5['SA-HUB-06']['check'], r5['SA-HUB-06']['location'], 'PASS',
    'Re-verified round 6: L04 eyebrow (L04.html:35, "10 study hours") and data-hours (L04.html:2 = 10) lie outside the changed hunks; index.html:145-148 unchanged; L01-L03 carried.'))
rows.append(row('SA-HUB-07', r5['SA-HUB-07']['check'], r5['SA-HUB-07']['location'], 'PASS',
    'Re-verified round 6: L04.html:155 (lab hypothesis paragraph, SIMULATED labels) is outside every changed hunk; index.html:37,172 unchanged; L01-L03 carried.'))
rows.append(row('SA-HUB-08', r5['SA-HUB-08']['check'], r5['SA-HUB-08']['location'], 'PASS',
    'Re-verified round 6: L04.html:652 (references paragraph) lies outside every changed hunk; the registry key cormen2022introduction exists (references/references.json line 5964; pages null, so the page statement that the record has no page locator is accurate); L01-L03 references carried.'))
rows.append(carry('SA-HUB-LEDE', HUB))
rows.append(carry('SA-L01-STRUCT', 'course/modules/CS/CS2/L01.html'))
rows.append(carry('SA-L02-STRUCT', 'course/modules/CS/CS2/L02.html'))
rows.append(carry('SA-L03-STRUCT', 'course/modules/CS/CS2/L03.html'))
rows.append(row('SA-L04-STRUCT', r5['SA-L04-STRUCT']['check'], 'L04.html:52 (why), 54-90, 92-125, 127-151, 153-421 (Lab 4), 423-431, 433-449, 451-554, 556-572, 574-648, 650-654', 'PASS',
    'Re-verified round 6: the delta changes eleven single lines (git diff -U0 hunks at L04.html 56, 60, 98, 110, 131, 134, 143, 426, 446, 500, 550), each a one-for-one replacement of a <p> or <li> text line; no section, problem, item, table or lab tag is added or removed, so the section order and counts are those of round 5 (Sections 1-9, Problems M1-M3, P1-P3, E1-E3, R1-R3, quiz items 1-10).'))
rows.append(carry('SA-L01-MATH', 'course/modules/CS/CS2/L01.html'))
rows.append(carry('SA-L02-MATH', 'course/modules/CS/CS2/L02.html'))
rows.append(carry('SA-L03-MATH', 'course/modules/CS/CS2/L03.html'))
rows.append(row('SA-L04-MATH', r5['SA-L04-MATH']['check'], 'L04.html:56-151, 388-389, 419-554 (whole mathematics, after the P3, R3 and comparison-sort edits)', 'PASS',
    'Re-derived round 6 from scratch: read every line of L04.html 1-665. Lemma 1.2 (L04:70) proof and Prop 1.3 induction (L04:80-84) re-checked with a <= 2^(K-1) < n; Remark 1.4 (L04:89) closed forms checked for n < 60 and n = 2^k, k <= 10 (rederive_l04_r6.py); Prop 2.1 leaf argument (L04:103-105) and Cor 2.2 (L04:115-119) with exact integers for n <= 1000 (no failures); Remark 2.3 (L04:124); Def 3.1 returns lo (L04:131); Prop 3.2 (L04:143-145) sizes floor(s/2) and floor((s-1)/2) and the halving count; P3 (L04:500) checked for n < 300; R3 (L04:550) identity ceil(log2(n+1)) = bit_length(n) for n < 100000, returned lo = number of keys below y for n <= 40; R1 (L04:536) new sizes floor(s/2) and floor((s-1)/2) re-derived; P2 (L04:493); numbers 262431/8886 = 29.533 (L04:511), 5120/8770 = 0.5838 (L04:525), 14-13 = 1, 21-13 = 8 (L04:518), 8770, 8529.3980, 4482.8921 (log2 1000!, 500 log2 500), 501500 = sum(n+1). Outputs: rederive_l04_r6.txt.'))
rows.append(row('SA-L04-CHECKS', r5['SA-L04-CHECKS']['check'], 'L04.html:155, 420; tests/labs/CS2/lab-CS2-L04-1.py', 'PASS',
    'Re-verified round 6: run_labs --unit CS2 --page L04 PASS (' + S + '/run_labs_L04.txt). Hypothesis (L04:155): Part A counts on 8, 64, 256, 1024 keys and sorted 1024; Part B every permutation of 2-7; Part C 2-1000; Part D every gap, n = 1-1000; Part E 2000 pairs of lengths 1-8 with keys 0-19 (1089 of 2000 pairs contain a tie, ties_check_r6.txt). Interpretation (L04:420): 262431, 8886, 29.53, 8770, 5120/8770 = 0.58, 21, 14, 13, margin 1 at n = 2 (confirmed the minimum of the float margin over 2..1000 in rederive_l04_r6.txt), 501500 gaps, 983 equal pairs; all equal the twin output. The lab does not check a successful search and measures no time, as stated.'))
rows.append(carry('SA-L01-HYP-01', 'course/modules/CS/CS2/L01.html and tests/labs/CS2/lab-CS2-L01-1.py'))
rows.append(row('SA-LAB-L01', r5['SA-LAB-L01']['check'], r5['SA-LAB-L01']['location'], 'PASS',
    'Re-verified round 6: run_labs --unit CS2 --page L01 PASS (' + S + '/run_labs_L01.txt); page code equals twin (run_labs byte-identity check).'))
rows.append(row('SA-LAB-L02', r5['SA-LAB-L02']['check'], r5['SA-LAB-L02']['location'], 'PASS',
    'Re-verified round 6: run_labs --unit CS2 --page L02 PASS (' + S + '/run_labs_L02.txt).'))
rows.append(row('SA-LAB-L03', r5['SA-LAB-L03']['check'], r5['SA-LAB-L03']['location'], 'PASS',
    'Re-verified round 6: run_labs --unit CS2 --page L03 PASS (' + S + '/run_labs_L03.txt).'))
rows.append(row('SA-LAB-L04', r5['SA-LAB-L04']['check'], r5['SA-LAB-L04']['location'], 'PASS',
    'Re-verified round 6: run_labs --unit CS2 --page L04 PASS (run_labs_L04.txt). Extracted the page code and expected block with extract_l04.py: diff against tests/labs/CS2/lab-CS2-L04-1.py differs only by the final newline; python -I -W error on the twin exits 0 with empty stderr (l04_twin_err.txt) and its stdout equals the page expected block up to the final newline (diff of l04_twin_out.txt and l04_page_expected.txt).'))
rows.append(row('SA-LAB-EXPECTED', r5['SA-LAB-EXPECTED']['check'], r5['SA-LAB-EXPECTED']['location'], 'PASS',
    'Re-verified round 6: run_labs PASS for L01-L04 (expected blocks equal the twin output under the page rule); L04 expected block checked byte-for-byte (trailing newline aside, l04_twin_out.txt vs l04_page_expected.txt).'))
rows.append(row('SA-LAB-SEEDED', r5['SA-LAB-SEEDED']['check'], r5['SA-LAB-SEEDED']['location'], 'PASS',
    'Re-verified round 6: run_labs PASS for L01-L04; page_smoke PASS for index, L01, L02, L03 (page_smoke_index_L01-L03.txt) and for L04 (page_smoke_L04.txt); L04 twin seeds at twin line 24 (SEED = 20261028); no network calls in the L04 twin (standard library only, twin lines 20-22; grep for socket, urllib, requests, http finds nothing).'))
rows.append(carry('SA-CARDS-L01', 'the L01 card records (CS2-c001..c012, c165, c218, c241)'))
rows.append(carry('SA-CARDS-L02', 'the L02 card records (CS2-c013..c025, c155..c158, c209..c212)'))
rows.append(carry('SA-CARDS-L03', 'the L03 card records (CS2-c026..c039, c159, c172..c175, c213, c219)'))
rows.append(row('SA-CARDS-L04', r5['SA-CARDS-L04']['check'], 'cards.json CS2-c040..c055, c176, c177, c208, c214 (20 L04 records)', 'PASS',
    'Re-verified round 6: all 20 L04 records read (cards_check_r6.txt). c040 now matches the corrected definition at L04.html:56 (decides its next step only from comparison outcomes; copies not counted). c047 and c055 now state hypothesis (2) as control flow, matching Prop 2.1 (1)-(6) at L04.html:98. c050 states the returned lo, matching Def 3.1 at L04.html:131 and R3. The other 16 records are unchanged since the round-5 pin and their values (21, 14, 13, 5120, 1023, 8770, 3 probes, 4 probes) match the twin output (cards_record_diff_r6.txt).'))
rows.append(row('SA-CARDS-DUP', r5['SA-CARDS-DUP']['check'], 'course/modules/CS/CS2/cards.json (197 records)', 'PASS',
    'Re-verified round 6: cards_check_r6.txt: 197 records, duplicate ids [], duplicate fronts []. Round-6 delta removes CS2-c077 (L06), c124 (L09) and c207 (L11), which are outside slice a.'))
rows.append(row('SA-CARDS-GRADE', r5['SA-CARDS-GRADE']['check'], 'cards.json (all records)', 'PASS',
    'Re-verified round 6 over the whole file (cards_check_r6.txt): 158 T and 39 C (round 5: 160 and 40, less the three removed records c077 T, c124 C, c207 T); every C record has basis; no T record has basis or cite; grade set = {T, C}. L04 C cards c052, c053, c176, c177, c214 cite Lab 4 parts.'))
rows.append(row('SA-DERIVE', r5['SA-DERIVE']['check'], S + '/rederive_l04_r6.py; ' + S + '/ties_check_r6.py; ' + S + '/cards_check_r6.py', 'PASS',
    'Independent re-derivation this round with own code (python3 -I rederive_l04_r6.py, output rederive_l04_r6.txt, exit 0): insertion and merge counts for seeded permutations of 8/64/256/1024 keys (21/15, 920/303, 16056/1735, 262431/8886), sorted 1024 (1023, 5120), ceil(log2 1024!) = 8770, all permutations n = 2-7 (max insertion = n(n-1)/2; merge max 1,3,5,8,11,14 within [lower, upper]), Part C exact-integer inequality (no failures for 2-1000), Part D 501500 gaps and all absent integers for n <= 60, Part E 2000 pairs (0 above, 983 equal) and exhaustive Lemma 1.2 over a, b <= 4 with values 0-2 (max excess 0).'))
rows.append(carry('SA-L03-RATIOS', 'course/modules/CS/CS2/L03.html'))
rows.append(row('SA-NOTATION', r5['SA-NOTATION']['check'], 'notation/notation.json; course/modules/CS/CS2/index.html, L01-L04', 'PASS',
    'Re-verified round 6: notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} and macros; grep of index.html and L01-L04 for these symbols finds none. The new L04 letters (beta, f, C(n), K, a, b, t, h, k, c_k, lo, hi, mid, sigma, gap j) are lesson-local (notation.json "about" field: only program-wide symbols are registered).'))
rows.append(row('SA-DAG-LESSON', r5['SA-DAG-LESSON']['check'], 'L01.html:59,99; L02.html:37,57,94; L03.html:37,57,82,90-93; L04.html:38,56,94,131,134', 'PASS',
    'Re-verified round 6: check_dag --unit CS2 PASS (check_dag.txt); the delta changes L04 text only: the eleven changed lines add no data-concept or concept link (git diff -U0 shows the existing dfn ids at 56 and 131 only).'))
rows.append(row('SA-PROSE-BANNED', r5['SA-PROSE-BANNED']['check'], 'index.html, L01-L04', 'PASS',
    'Re-verified round 6: case-insensitive grep of L04.html for can be shown, beyond the scope, for brevity, details omitted, left as an exercise, you can add, well known, important to note, studies show, experts agree, TODO, TBD, lorem, obviously, clearly, it is easy, one can check, process words (ruling, verif, architect, round, delta, blind, rubric, fragment): no hit in prose. Ellipses are mathematical (L04.html:56, 115, 134; twin line 252). index.html and L01-L03 carried.'))
rows.append(row('SA-PROSE-SCOPE', r5['SA-PROSE-SCOPE']['check'], 'L04.html scope words (lines 52, 56, 70, 89, 98, 103, 124, 138, 143, 150, 155, 420, 426, 438, 446, 500, 525, 536, 550, 568, 652); L01-L03 carried', 'PASS',
    'Re-verified round 6: each scope word in L04 is backed by a computation or a definition: every (lines 52, 124, 155, 420, 652) names the lab part that checks it and the lab output confirms (every permutation of 2-7, every n 2-1000, every gap, 2000 pairs); "every count below" (L04:56) covers the comparison counts of Section 1 only; "only" (L04:426, 525, 70) is the stated hypothesis or the proof step. Line 652 "on deterministic lists" is vague wording (note, not a row).'))
rows.append(row('SA-TOOL-CHECKPAGES', r5['SA-TOOL-CHECKPAGES']['check'], 'tools/check_pages.py --unit CS2', 'PASS', 'Re-run round 6: "check_pages CS2: PASS" (' + S + '/check_pages.txt, exit 0).'))
rows.append(row('SA-TOOL-DAG', r5['SA-TOOL-DAG']['check'], 'tools/check_dag.py --unit CS2', 'PASS', 'Re-run round 6: "check_dag CS2: PASS" (' + S + '/check_dag.txt, exit 0).'))
rows.append(row('SA-TOOL-RUNLABS', r5['SA-TOOL-RUNLABS']['check'], 'tools/run_labs.py --unit CS2 --page L01..L04', 'PASS', 'Re-run round 6, one page per call (the tool keeps only the last --page): L01, L02, L03, L04 each "run_labs CS2: PASS (1/1)", exit 0 (run_labs_L0x.txt).'))
rows.append(row('SA-TOOL-PAGESMOKE', r5['SA-TOOL-PAGESMOKE']['check'], 'tools/page_smoke.py --unit CS2 (index, L01-L04; run alone)', 'PASS', 'Re-run round 6: --pages index L01 L02 L03 "page_smoke CS2: PASS" (page_smoke_index_L01-L03.txt); --pages L04 alone "page_smoke CS2: PASS" (page_smoke_L04.txt).'))
rows.append(row('SA-TOOL-LINT', r5['SA-TOOL-LINT']['check'], 'tests/labs/CS2/lab-CS2-L01..L04-1.py', 'PASS', 'Re-run round 6: ruff check and ruff format --check on the four twins: "All checks passed!", "4 files already formatted" (ruff_twins.txt); mypy --no-incremental on the four twins: "Success: no issues found in 4 source files" (mypy_twins.txt).'))
rows.append(row('SA-TOOL-PYTEST', r5['SA-TOOL-PYTEST']['check'], 'tests/test_labs.py -k CS2; tests/test_run_labs.py; tests/test_docs_figures.py', 'PASS', 'Re-run round 6: pytest tests/test_labs.py -k CS2 exit 0 (14 tests, 14 progress marks); tests/test_run_labs.py exit 0 (6 tests); tests/test_docs_figures.py exit 0 (14 tests) (pytest_labs_CS2.txt, pytest_run_labs.txt, pytest_docs_figures.txt).'))
rows.append(row('SA-TOOL-REFS', r5['SA-TOOL-REFS']['check'], 'tools/verify_refs.py --offline', 'PASS', 'Re-run round 6: "offline integrity: 560 entries, 0 problems", exit 0 (verify_refs_offline.txt).'))
rows.append(row('SA-TOOL-PROJECTS', r5['SA-TOOL-PROJECTS']['check'], 'tools/check_projects.py --unit CS2', 'PASS', 'Re-run round 6: "check_projects CS2: PASS" (check_projects.txt, exit 0).'))
rows.append(carry('SA-LIVE-CURRICULUM', 'curriculum/01-foundations.yaml, curriculum/curriculum.json and course/modules/CS/CS2/index.html'))
rows.append(row('SA-DELTA-READ', r5['SA-DELTA-READ']['check'], 'git diff dde0486b e896b7a4 for slice a: course/modules/CS/CS2/L04.html, cards.json, tests/labs/CS2 (L01-L04 twins unchanged)', 'PASS',
    'Delta read this round: L04.html (eleven one-line hunks, all read against the whole page); cards.json (ten changed ids, of which four are slice-a L04 records c040, c047, c050, c055 and were read in full; c077, c124 and c207 removed, outside slice a); plans/FINAL-ARCHITECT-RULINGS.md ruling 26 and ruling 30 and plans/KNOWN-ISSUES.md read (ruling 26 makes wording and presentation LOW rows deferrable, but a lab statement the code does not support is blocking). Changed files outside slice a (L05-L11, L06/L07 twins, M5, M7, FC2, E3, M7 and LX1 ledgers, tests) are not in slice a and are not verified here.'))
rows.append(row('SA-TOOL-GRADERS', r5['SA-TOOL-GRADERS']['check'], 'tools/run_graders.py --unit CS2 --seeds 0-49', 'PASS', 'Re-run round 6: "run_graders CS2: PASS (reference 50/50 seeds, slowest 0.3 s)" (run_graders_CS2_0-49.txt, exit 0). No grader file is in the delta.'))
rows.append(row('SA-PY314-TWINS', r5['SA-PY314-TWINS']['check'], 'tests/labs/CS2/lab-CS2-L01..L04-1.py', 'PASS', 'Re-run round 6: CPython 3.14.8 (.venv); ast.parse with feature_version (3, 14) of the four twins succeeds (printed "py314 parse ok"); each twin ran under python -I -W error (L04 exit 0, empty stderr).'))
rows.append(carry('SA-CARDS-HYP', 'the proposition-stating cards carried by id (c042, c043, c048, c051 unchanged)').__class__ and row('SA-CARDS-HYP', r5['SA-CARDS-HYP']['check'], r5['SA-CARDS-HYP']['location'], 'PASS',
    'Re-verified round 6 against the current lessons: c042 (Lemma 1.2 hypotheses) and c043 (Prop 1.3 hypotheses) match L04.html:65 and 75; c047 and c055 state hypotheses (1)-(6) of Prop 2.1 as now written at L04.html:98 (control flow, output determined by outcomes); c051 states Prop 3.2 hypotheses (n >= 1, strictly increasing, absent key, probes as comparisons) matching L04.html:138; the L01 Prop 1.6 cards c006 and c218 are carried (L01.html unchanged; records unchanged by id).'))
rows.append(carry('SA-L01-PROP16-HYP', 'L01.html:98-104 and the cards CS2-c006, CS2-c218'))
rows.append(carry('SA-L03-PROP16-PROOF', 'course/modules/CS/CS2/L03.html'))
rows.append(row('SA-L04-LEMMA-SORTED', r5['SA-L04-LEMMA-SORTED']['check'], 'L04.html:65 (Lemma 1.2), 70 (proof), 75 and 80 (Prop 1.3 applies the lemma)', 'PASS',
    'Re-verified round 6: L04.html:65, 70, 75 and 80 are outside the changed hunks; the merge of Definition 1.1 used by Lemma 1.2 (ties to the left, line 60 now only changes the insertion text) is the merge in the twin (merge_count, twin lines 44-60, <= at twin line 52).'))
rows.append(row('SA-L04-COMPSORT-DEF', r5['SA-L04-COMPSORT-DEF']['check'], 'L04.html:56, 60, 98, 426, 446; cards CS2-c040, c047, c055', 'PASS',
    'Fixed in e896b7a4 and re-verified: L04.html:56 now says a comparison sort decides its next step only from comparison outcomes and may copy key values (copies not counted); L04.html:60 insertion sort (key = a[i] at twin line 32 is a copy, which the definition allows); L04.html:98 hypothesis (2) control flow; L04.html:426 Section 4 bullet and L04.html:446 misconception use the same wording; cards c040, c047, c055 match. The proof of Prop 2.1 (L04.html:103) uses only that control flow depends on outcomes, as before.'))
rows.append(row('SA-L04-R3-REPORT', r5['SA-L04-R3-REPORT']['check'], 'L04.html:131 (Definition 3.1), 134 (gap j), 550 (R3 solution); card CS2-c050', 'PASS',
    'Fixed in e896b7a4 and re-verified: Definition 3.1 (L04.html:131) now says the empty-range stop reports that y is absent and returns lo; L04.html:134 defines gap j and says lo is the index of the gap that holds y; the R3 solution (L04.html:550) proves it by the invariant (keys before lo below y, keys after hi above y, lo = hi + 1 at the stop). Checked by rederive_l04_r6.py: returned lo equals the number of keys below y for every absent integer y, n <= 40. Card CS2-c050 agrees.'))
rows.append(row('SA-L04-P3-FALSE', r5['SA-L04-P3-FALSE']['check'], 'L04.html:498 (P3 statement), 500 (P3 solution)', 'PASS',
    'Fixed in e896b7a4 and re-verified: L04.html:500 now says the right part "still holds only keys smaller than the search key, so the search key is still above every key of the range", which is true (the first probe is at floor((n-1)/2) and finds a key below y, so lo = mid + 1). The induction on the right part of floor(n/2) keys is valid. Checked: top-gap probe count equals n.bit_length() for n < 300 (rederive_l04_r6.txt).'))
rows.append(row('SA-GRADE-PAGES', r5['SA-GRADE-PAGES']['check'], 'L01.html:63,73,83,98,108,213,229,241,378-384; L02.html:66,76,98,108,242,385-389; L03.html:61,310,326,488-492; L04.html grade spans (44-48, 64, 73, 97, 109, 137, 420, 562-568)', 'PASS',
    'Re-verified round 6: L04 grade spans re-read: Lemma 1.2, Prop 1.3, Prop 2.1, Cor 2.2, Prop 3.2 T (lines 64, 73, 97, 109, 137); L04.html:420 C (lab-based claims, labelled); key results rows 562-568 all T with proof or lab source; remark and problem texts ungraded. L01-L03 carried (byte-identical).'))
rows.append(row('SA-L04-LEMMA-HYP', r5['SA-L04-LEMMA-HYP']['check'], 'L04.html:60, 65, 75, 80; tests/labs/CS2/lab-CS2-L04-1.py:44-60', 'PASS',
    'Re-verified round 6: the hypotheses of Lemma 1.2 (two lists with a, b >= 1; no two keys compared except as fronts; ties to the left) hold for merge_count in the twin, and the bound a + b - 1 is checked on 2000 seeded pairs (Part E: 0 above, 983 equal) and exhaustively for a, b <= 4 with values 0-2 (max excess 0).'))
rows.append(row('SA-TERMS-SUMMARY', r5['SA-TERMS-SUMMARY']['check'], 'L01.html:51; L02.html:51; L03.html:51; L04.html:52', 'PASS',
    'Re-verified round 6: L04.html:52 lies outside the changed hunks; its terms (comparison sorting, Lemma, binary search, probe, gap) are defined at L04:56, 131, 134 before the summary uses them in later sections; L01-L03 summary lines carried (byte-identical).'))
rows.append(row('SA-MATH-LABCHECK', r5['SA-MATH-LABCHECK']['check'], 'L01.html:64, 84; L03.html:61, 304; L04.html:65; twins lab-CS2-L01-1.py, lab-CS2-L03-1.py, lab-CS2-L04-1.py', 'PASS',
    'Re-verified round 6: every key formula of L04 has a numerical check in Lab 4 (Lemma 1.2 Part E; Prop 1.3 Part B n <= 7; Remark 1.4 Part A and B; Cor 2.2 Part C; Prop 3.2 Part D); L01 and L03 entries carried (byte-identical).'))
rows.append(row('SA-LAB-PROSE-COUNT', 'twin module docstring and page code block: "Every count is a number of key comparisons" (lab-CS2-L04-1.py line 6; L04.html:161)', 'tests/labs/CS2/lab-CS2-L04-1.py line 6 (module docstring); course/modules/CS/CS2/L04.html:161 (the same line inside the Lab 4 code block)', 'FAIL',
    'The sentence is a statement about what the lab counts, and the code does not support it: the lab prints counts that are not comparison counts, namely "gaps_checked 501500" (Part D; expected block L04.html:413), "pairs checked: 2000" (Part E; L04.html:416) and the permutations column of the Part B table (L04.html:382-392). Found round 6 by reading the docstring against the output; not present in any earlier ledger row.',
    'Change the sentence to "Every cost count is a number of key comparisons; the other counts are of inputs, gaps and pairs." in the twin, then re-embed the page code block (embed_labs.py --refresh lab-CS2-L04-1 or equivalent) and re-run run_labs, pytest tests/test_labs.py -k CS2 and page_smoke for L04.'))

counts = {'PASS': sum(1 for r in rows if r['status'] == 'PASS'), 'FAIL': sum(1 for r in rows if r['status'] == 'FAIL')}
ids = [r['id'] for r in rows]
assert len(ids) == len(set(ids)), 'duplicate ids'
missing = [i for i in r5 if i not in ids]
assert not missing, missing
frag = {
  'unit': 'CS2', 'slice': 'a', 'round': 6,
  'round_note': 'Round 6 delta verification of CS2 slice a (hub index.html; L01-L04 pages, twins and the 77 L01-L04 cards), pinned at e896b7a4. Base: the round-5 pin dde0486b. Delta in slice a: L04.html (eleven one-line hunks: comparison-sort definition, insertion sort, Prop 2.1 hypothesis (2), Cor 2.2 remark, Def 3.1 and gap paragraph, Prop 3.2 proof, Section 4, misconception, P3, R3) and the cards CS2-c040, c047, c050, c055. The round-5 FAIL rows SA-L04-MATH, SA-CARDS-L04, SA-L04-COMPSORT-DEF, SA-L04-R3-REPORT and SA-L04-P3-FALSE are re-verified and now PASS. One new FAIL row (SA-LAB-PROSE-COUNT): a lab docstring sentence the code does not support. All round-5 row ids are kept; the only new id is SA-LAB-PROSE-COUNT.',
  'verifier': 'independent round-6 delta verifier (Haiku 5.5), fresh context; did not build CS2; round-5 fragment read as context only (its PASS rows were carried only where the cited subject is byte-identical, and every other PASS row was re-run or re-read)',
  'pin': PIN6,
  'base': PIN5 + ' (round-5 pin)',
  'checkout': '/Users/billyribeiro/.fanout/wt/verifyS6-CS2-a (detached at e896b7a4, .venv symlinked)',
  'scratch': '/Users/billyribeiro/.fanout/wt/verifyS6-CS2-a/' + S,
  'verified_at': '2026-11-09',
  'verdict': 'FAIL' if counts['FAIL'] else 'PASS',
  'rows': rows,
  'mutants': [],
  'registry_flags': [],
  'freshness_flags': [],
  'notes': [
    'Read in full this round: L04.html (665 lines, every line); the four L04 twin outputs (run and compared byte-for-byte with the page); the eleven L04 hunks and the four changed L04 cards read against the whole page; index.html, L01-L03 pages, twins L01-L03 and their cards carried under the byte-identical rule (git diff --quiet dde0486b e896b7a4 for each file).',
    'Scripts (ledgers/CS2/scripts/CS2-a-r6/): rederive_l04_r6.py (own implementation of the insertion sort, merge, binary search and counts; python3 -I; output rederive_l04_r6.txt), extract_l04.py (page code and expected block extraction), ties_check_r6.py, cards_check_r6.py, cards_record_diff_r6.txt, build_fragment_cs2a_r6.py (writes this fragment), and every tool log (check_pages.txt, check_dag.txt, check_projects.txt, run_labs_L01..L04.txt, page_smoke_*.txt, ruff_twins.txt, mypy_twins.txt, pytest_*.txt, verify_refs_offline.txt, run_graders_CS2_0-49.txt).',
    'Not a row (LOW, wording): L04.html:652 "Proposition 3.2 at every gap for n from 1 to 1000 on deterministic lists" is vague; the lab checks the single list with keys 2i for each n (Part D), so "on the lists with keys 2i" is the exact description. Suggested fix only.',
    'Not a row (LOW, applicability): Definition 3.1 probes have three outcomes (x_mid < y, = y, > y), while R3 hypothesis (2) requires two-outcome comparisons. R3 and its solution do not claim that Prop 2.1 or R3 applies to Definition 3.1: the sentence "so binary search meets this bound in the worst case" is the numerical equality ceil(log2(n+1)) = beta(n) (Prop 3.2 gives the upper bound). Suggested clarification: "restricted to absent keys, each probe has two outcomes, so R3 applies to that restriction". Not counted as a blocking defect.',
    'Not a row (LOW, edge case): Remark 1.4(a) "On sorted input of n keys ... exactly n - 1 comparisons" is false for n = 0 (count 0, formula -1); the lab and cards use n >= 1. Suggested fix: state n >= 1.',
    'Not in slice a and not verified here: the delta also changes cards CS2-c125, c194, c200, c223, c231, c234 (L08-L11 records), removes CS2-c077 (L06), c124 (L09) and c207 (L11), and changes L05-L11 pages and the L06/L07 twins; those belong to other CS2 slices.',
    'Mutation testing: not applicable to slice a (course lab twins, not project graders; ruling 9 and the verifier rules ruling on lab twins). No mutant was authored or run.'
  ],
  'summary': {'rows': len(rows), 'pass': counts['PASS'], 'fail': counts['FAIL'], 'unverifiable': 0, 'mutants_killed': 0, 'mutants': 0},
}
json.dump(frag, open('ledgers/CS2/CS2-a.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('wrote', len(rows), 'rows;', counts)
