# Round-5 row decisions for slice CS2-b (exec'd by build_fragment_r5.py). Evidence is from this round's commands
# (outputs under /tmp/CS2-v/CS2-b-r5) and the scripts in this folder.
NOTES = ("Lesson slice with two lab twins (L06, L08) and no grader: mutants empty (architect ruling: lab twins are "
         "demonstrations; mutation testing applies to project graders only). Delta since 2657ab5: L06.html lines 52 and 137; "
         "L07.html lines 63, 179, 210, 703, 706; L08.html lines 56, 131, 176, 546, 626-627, 675-677; tests/labs/CS2/lab-CS2-L06-1.py "
         "line 12 and lab-CS2-L08-1.py lines 5-7. cards.json, L05.html, references/references.json and lab-CS2-L05-1.py are byte-identical. "
         "Re-run this round: run_labs CS2 14/14; each twin under python -I -W error (rc 0); embedded code blocks equal the twins and the "
         "expected blocks equal the runs (ledgers/CS2/scripts/CS2-b-r5/cmp.py); page_smoke, check_pages, check_dag, check_projects, "
         "verify_refs --offline, ruff; witness and stale-read experiments (ledgers/CS2/scripts/CS2-b-r5/witness.py, stale_read_experiment.py); "
         "independent LCS and coin counts (l07_indep.py). Not checked: a live verify_refs run this round (references unchanged; round-4 live "
         "result carried); a Pyodide run beyond page_smoke; ruff/mypy on the whole repo; no outside source was cited, so no publisher or "
         "bot-protected site was contacted.")

# ---- commands and reproduction (re-run this round)
new('CS2b-cmd-pin', 'checkout pin and delta', 'git checkout /tmp/verifyB5-CS2-b', 'PASS',
    'git log -1 --oneline: 09b8751 Batch 2: fixes for independent verification round 4; git status --short: clean; '
    'git diff --stat 2657ab5 09b8751 -- course/modules/CS/CS2 tests/labs/CS2 shows changes only to L01-L04, L06-L11, grader, index, project '
    'and to the L06 and L08 lab twins; L05.html, L07 twin, cards.json, references.json byte-identical in the slice.')
new('CS2b-cmd-run_labs', 'tools/run_labs.py --unit CS2', 'tools/run_labs.py', 'PASS',
    "'run_labs CS2: PASS (14/14)' (output in /tmp/CS2-v/CS2-b-r5/run_labs.txt).")
new('CS2b-cmd-lab-cpython-W-error', 'twins run alone under python -I -W error', 'tests/labs/CS2/lab-CS2-L05-1.py, L06-1, L07-1, L08-1', 'PASS',
    'each exit code 0; outputs 31, 17, 10, 15 lines (/tmp/CS2-v/CS2-b-r5/lab-L05..L08.out); ledgers/CS2/scripts/CS2-b-r5/cmp.py: '
    'embedded code == twin True for L05, L06, L07, L08; <pre class="expected"> == run output True for all four.')
new('CS2b-cmd-page_smoke', 'tools/page_smoke.py --unit CS2', 'tools/page_smoke.py', 'PASS',
    "'page_smoke CS2: PASS' (re-run this round).")
new('CS2b-cmd-check_pages', 'tools/check_pages.py and tools/check_projects.py --unit CS2', 'tools/check_pages.py, tools/check_projects.py', 'PASS',
    "'check_pages CS2: PASS' and 'check_projects CS2: PASS' (re-run this round, rc 0).")
new('CS2b-cmd-check_dag', 'tools/check_dag.py --unit CS2', 'curriculum/curriculum.json CS2 entry', 'PASS',
    "'check_dag CS2: PASS' (re-run this round); no new data-concept link in the changed lines.")
new('CS2b-cmd-lint', 'ruff check and ruff format --check on the CS2 twins', 'tests/labs/CS2/', 'PASS',
    "ruff check tests/labs/CS2/: 'All checks passed!'; ruff format --check: '14 files already formatted' (re-run this round).")
new('CS2b-cmd-verify_refs', 'tools/verify_refs.py offline (live run carried)', 'references/references.json; tools/verify_refs.py', 'PASS',
    "offline re-run this round: 'integrity: 560 entries, 0 problems'. references/references.json is byte-identical since 2657ab5; "
    "the round-4 live run ('1 of 560 entries, 0 problems') is carried, not repeated.")
carry('CS2b-cit-cormen', 'references/references.json and course/modules/CS/CS2/L05.html:648, L06.html:591')

# ---- numbers
new('CS2b-num-L05-lab', 'L05 Lab 1 printed values vs interpretation', 'course/modules/CS/CS2/L05.html:414; lab-CS2-L05-1 output', 'PASS',
    "L05 lab output re-run this round (31 lines) and compared with the expected block (equal). L05.html and the L05 twin are byte-identical "
    "since 2657ab5, so the round-4 comparison of each printed value with line 414 is carried.")
carry('CS2b-num-L05-derived', 'course/modules/CS/CS2/L05.html lines 99, 414, 440, 519, 544 (R3)')
new('CS2b-num-L06', 'L06 Lab 1 numbers vs page', 'course/modules/CS/CS2/L06.html:362, 388; lab-CS2-L06-1 output', 'PASS',
    "re-run this round: 'reachable_pairs_checked 772 unreachable_pairs 308', 'graphs 40 sources_checked 200', "
    "'vertex_pairs_checked 440', 'vertices 200 edges 619', 'adjacency_entries_inspected 1238', "
    "'list_work_enqueues_plus_inspections 1438', 'matrix_row_reads_for_same_search 40000'. Pages L06:362 and L06:388 unchanged. "
    "Part C printed lines 'to a: bfs_path s-a hops 1 weight 10 | lightest_path s-b-a hops 2 weight 2', 'to b: ... s-b ... s-b', "
    "'to c: s-a-c ... s-b-a-c' agree with L06.html:137 (new text: differ for a and c, coincide for b).")
new('CS2b-num-L07', 'L07 Lab 1 numbers vs page', 'course/modules/CS/CS2/L07.html:210, 507, 603-611, 622, 653-656, 697-711', 'PASS',
    "re-run this round: 'LCS length = 3', 'table cells filled = 49', 'memo subproblems stored = 28', 'memo calls = 47', "
    "'recursion with no memo table makes 183 calls', 'fewest coins = 5', 'memo calls = 56', '20736 calls'. Independent recomputation "
    "(ledgers/CS2/scripts/CS2-b-r5/l07_indep.py): LCS (3, 47, 28), no-memo 183, table 7*7=49, coin f(20)=5, memo calls 56, no-memo 20736. "
    "The lab prints 'amounts stored = 20'; my memo dictionary holds 21 keys because it also stores base amount 0, so the printed count is "
    "the lab's own convention and the page does not state it.")
new('CS2b-num-L08', 'L08 Lab 1 numbers vs page', 'course/modules/CS/CS2/L08.html:546, 572, 637, 689; lab-CS2-L08-1 output', 'PASS',
    "re-run this round: 'messages applied: 400; cancels: 102; new orders: 298', 'messages that traded: 117; executions: 177', "
    "'final best bid 9980, best ask 9989, resting orders 10', 'orders added: 298; queue steps: 7', 'price levels created: 185; removed: 177', "
    "'binary searches: 362; largest comparison count: 4'. Each figure at L08.html:546 and 689 matches. The lab twin's Part B and Part C code "
    "is unchanged except a docstring; the independent stream recomputation of round 4 (recompute_r4.py) is carried.")

# ---- grades
carry('CS2b-grade-L05', 'course/modules/CS/CS2/L05.html lines 556-560')
carry('CS2b-grade-L06', 'course/modules/CS/CS2/L06.html lines 504-508')
carry('CS2b-grade-L07', 'course/modules/CS/CS2/L07.html lines 648-656')
carry('CS2b-grade-L08', 'course/modules/CS/CS2/L08.html line 689 and lines 693-694')

# ---- math
carry('CS2b-math-L05-proofs', 'course/modules/CS/CS2/L05.html lines 76-100 and 106-114')
carry('CS2b-math-L05-problems', 'course/modules/CS/CS2/L05.html lines 453-544')
carry('CS2b-math-L06-proofs', 'course/modules/CS/CS2/L06.html lines 68-121')
new('CS2b-math-L07-proofs', 'L07 proofs: Theorem 2.2, Corollary 2.3, Example 2.4, Lemma 3.2, Theorem 3.3, Corollary 3.4, Proposition 3.5, Proposition 4.2',
    'course/modules/CS/CS2/L07.html 72-112, 170-203', 'PASS',
    "Proposition 3.5 (L07.html:179 changed this round from 'running time' to 'operation count'): the claim 'computes exactly mn entries, uses (m+1)(n+1) stored entries, "
    "performs at most c*mn elementary operations' is the row count of Corollary 3.4 (m*n cells, each O(1)), so the count is O(mn) by the definition at L01. "
    "Re-derived the rest of the round-4 subject: Theorem 2.2 upper/lower/infinite cases, Corollary 2.3 strong induction (lines 101, 106), Example 2.4 f(6)=2 vs 3 coins, "
    "Lemma 3.2 one-step bounds, Theorem 3.3 cases, Corollary 3.4 induction on i+j, Proposition 4.2 with A+1 > 2^(b-1) (L07.html:195-198). Lines 72-112 and 191-203 unchanged since 2657ab5.")
carry('CS2b-math-L08-lemmas', 'course/modules/CS/CS2/L08.html lines 70-86, 108-122, 133-172 (line 131 changed, outside every cited range)')

# ---- labs
new('CS2b-lab-L05', 'L05 lab hypothesis and interpretation', 'tests/labs/CS2/lab-CS2-L05-1.py; course/modules/CS/CS2/L05.html Lab 1 paragraph (123) and interpretation (414)', 'PASS',
    'twin and L05.html byte-identical since 2657ab5; re-run this round (31 lines, equal to the expected block). Round-4 evidence carried: hypothesis matches code (500 seeded keys, sorted 1..64, N(h) for h=1..12).')
new('CS2b-lab-L07', 'L07 lab expected result', 'tests/labs/CS2/lab-CS2-L07-1.py; course/modules/CS/CS2/L07.html Lab 1 paragraph (210), interpretation (507)', 'PASS',
    "L07.html:210 changed this round and re-checked against the run (10 lines): 'For 30 seeded LCS pairs and 30 seeded coin instances ... agree' matches 'part A/B ... agree on all of them'; "
    "'For every LCS pair the table has exactly mn computed cells' matches the lab's check 'cells != len(x) * len(y)' (twin line 234); "
    "'denominations (1, 3, 4) and amount 6 ... 3 coins ... 2' matches 'largest-coin-first uses 3 coins, optimum uses 2'; "
    "'table has 49 computed cells, memoized recursion stores 28 subproblems and makes 47 calls, no memo table makes 183 calls' matches part C. "
    "L07.html:507 unchanged.")
new('CS2b-lab-L08', 'L08 lab hypothesis and interpretation (page text)', 'course/modules/CS/CS2/L08.html Lab 1 paragraph (176) and interpretation (546); twin lines 1-19 (docstring checked in CS2b5-lab-L08-reference-key)', 'PASS',
    "L08.html:176 'a reference that sorts the crossing candidates on every match' matches Reference.submit (twin lines 218-238, sort at 222 and 225); "
    "L08.html:546 Part A hand trace matches the output (5 at 10000 from order 1, 2 at 10000 from order 2; cancel of order 3; 1 at 10000 from order 2; best bid 10000, best ask 10010); "
    "Part B 'the lab compares the book with the reference on this one stream only' matches the single seed in part_b; "
    "Part C numbers match the output. Docstring error is a separate FAIL row.")
new('CS2b-L06-lab-exhaustive', 'brute_min_hops is an exhaustive search over simple paths', 'tests/labs/CS2/lab-CS2-L06-1.py lines 60-76; course/modules/CS/CS2/L06.html:125', 'PASS', "Read this round: brute_min_hops DFS over simple paths (on_path set, line 63-73) updates best[u] when length+1 is smaller; every simple path is visited, so the minimum is exact. Twin code lines 60-76 unchanged; only the docstring line 12 changed. "
"Run this round: 'bfs_mismatches_against_brute_force 0' over 40 graphs and 200 sources (lab output in /tmp/CS2-v/CS2-b-r5/lab-L06.out). L06.html:125 unchanged.")

# ---- cards
new('CS2b-cards-dupe-scan', 'card id and front duplicate scan', 'course/modules/CS/CS2/cards.json (167 cards, all lessons)', 'PASS',
    "re-run this round: 167 cards, no duplicate id, no duplicate front (case-insensitive).")
carry('CS2b-cards-coverage', 'course/modules/CS/CS2/cards.json (byte-identical); lesson grade C bases')
new('CS2b-cards-consistency', 'every card of CS2-c056..c115 against the CURRENT lesson text', 'course/modules/CS/CS2/cards.json CS2-c056..c115 (60 cards)', 'FAIL',
    'cards.json is byte-identical since 2657ab5. Re-checked the L05-L08 cards against the current lesson text. Mismatches: CS2-c080 (CS2b4-cards-c080), '
    'CS2-c084 (CS2b4-cards-c084), CS2-c060/c061/c088/c092 notation (CS2b4-cards-notation-T), CS2-c093 (CS2b5-card-c093), CS2-c102 (CS2b5-card-c102), '
    'CS2-c114 (CS2b5-card-c114). All other cards in the range agree with the current text.',
    fix='fix each card named in the separate FAIL rows CS2b4-cards-c080, CS2b4-cards-c084, CS2b4-cards-notation-T, CS2b5-card-c093, CS2b5-card-c102 and CS2b5-card-c114, then re-check this aggregate')
carry('CS2b4-cards-L05', 'course/modules/CS/CS2/cards.json CS2-c056..c069 and L05.html')
new('CS2b4-cards-L08', 'cards CS2-c100..c115 against L08 text', 'course/modules/CS/CS2/cards.json CS2-c100..c115', 'FAIL',
    'L08.html:56, 176 and 546 changed this round. Re-checked: c100, c101, c103-c113, c115 agree with the current text; c113 basis ("Lab 1, Parts B and C") and c115 agree with the lab output (185, 177, 362, 4). '
    'CS2-c102 (CS2b5-card-c102) and CS2-c114 (CS2b5-card-c114) disagree with the current L08.html:56 and L08.html:176.',
    fix='fix CS2-c102 and CS2-c114 as in CS2b5-card-c102 and CS2b5-card-c114')
new('CS2b4-cards-L07-R-part', 'cards CS2-c089..c099 against L07 text', 'course/modules/CS/CS2/cards.json CS2-c089..c099', 'FAIL',
    'L07.html:179 changed this round. c089, c090, c091, c095, c096, c097, c098, c099 re-checked and agree; c093 says "Its running time is O(mn)" while the current L07.html:179 says "Its operation count is therefore O(mn)" (CS2b5-card-c093).',
    fix='fix CS2-c093 as in CS2b5-card-c093')
new('CS2b4-cards-c080', 'card CS2-c080 vs L06.html:380', 'course/modules/CS/CS2/cards.json CS2-c080 vs course/modules/CS/CS2/L06.html:380', 'FAIL',
    "card back still reads 'BFS returns the first path'. L06.html:380 (unchanged this round) reads 'BFS returns the path with the fewest edges, here the direct edge from s to a'. Card and lesson disagree.",
    fix="replace the final sentence of the card back with: 'BFS returns the path with the fewest edges, here the direct edge from s to a.'")
new('CS2b4-cards-c084', 'card CS2-c084 vs its front and L07 Definition 1.1', 'course/modules/CS/CS2/cards.json CS2-c084 vs course/modules/CS/CS2/L07.html:56-61', 'FAIL',
    "front asks 'what are its two forms?'; back gives the three steps only. L07.html:61 (Definition 1.1, unchanged) names the two forms: memoized recursion and table fill.",
    fix="add to the back: 'Two forms: memoized recursion (a function calls itself and returns the stored value after the first call) and table fill (values written in an order where each entry depends only on entries already written).'")
new('CS2b4-cards-notation-T', 'symbol T in cards vs notation/notation.json', 'course/modules/CS/CS2/cards.json CS2-c060, c061, c088, c092', 'FAIL',
    "notation/notation.json line 112 registers T as 'number of return observations (periods) in a sample' (module S1). cards c060 and c061 use T for an AVL tree, c088 and c092 for the coin table and the LCS table. L05.html and L07.html do not define T as a math symbol (grep of \\(T: 0 hits in L05.html; L07.html hits are code only).",
    fix='rename the symbol in the four cards to a letter the registry does not use for another meaning (for example H for the tree, F for the coin table, Tbl for the LCS table), keeping the same definitions')
carry('CS2b4-cards-notation-c068', 'course/modules/CS/CS2/cards.json CS2-c068 and L05.html:436')

# ---- quiz, misconceptions, problems, R3
new('CS2b4-quiz-L05-L08', 'quiz answers vs lesson', 'course/modules/CS/CS2/L05.html..L08.html quiz sections', 'FAIL',
    "L05-L08 quiz answers re-checked: L07 Q6 (L07.html:703-706, changed this round) marks as correct 'They touch different subproblems, and their answers agree on the seeded instances of Lab 1'. "
    "The claim 'they touch different subproblems' is not true in general: for denominations {1} and amount 3, memoized recursion touches {0, 1, 2, 3} and the table fills {0, 1, 2, 3} (ledgers/CS2/scripts/CS2-b-r5/witness.py). The other quiz answers were checked in round 4 and their lines are unchanged this round (L05, L06, L08 quizzes unchanged; L07 Q6 is the only changed item).",
    fix="replace the correct option with 'They can touch different subproblems, and their answers agree on the seeded instances of Lab 1' and say in the explanation that for some recurrences both touch the same subproblems")
carry('CS2b4-misconceptions-L05-L08', 'course/modules/CS/CS2/L05.html:430-442, L06.html:378-390, L07.html:522-534, L08.html:562-574')
new('CS2b4-problems-L06-L08', 'problem solutions L06 M1-R3, L07 M1-R3, L08 M1-R2, P1-P3, E1-E3', 'course/modules/CS/CS2/L06.html 399-492; L07.html 543-638; L08.html 585-670', 'PASS',
    'L08.html:626-627 (P3 proof) changed this round and re-derived: the loop ends either with remaining quantity 0 (total q, q <= Q because the traded amount never exceeds Q) or with no live crossing quantity left while the remaining quantity is still positive (total Q, and Q < q because q - Q > 0); in both cases the total is min{q, Q}. '
    'Other problems re-derived in round 4 are carried (their lines are unchanged).')
new('CS2b4-L08-R3', 'R3 problem and solution vs lab code', 'course/modules/CS/CS2/L08.html:673-677; twin lines 165-190', 'PASS',
    "The problem (new text) asks what a stale read of the old best ask raises. Ran the twin's Book on the solution's book (asks 1 at 10000 and 5 at 10005, buy 3 at 10010): correct trades (1, 10000, order 1), (2, 10005, order 2). "
    "With the loop reading best once (variant in ledgers/CS2/scripts/CS2-b-r5/stale_read_experiment.py): 'stale raised KeyError 10000', raised at the line self.levels[opposite][best] (twin line 176). "
    "The solution's statement that the stale read 'produces no trade' is true of the stale iteration; the first 1-share fill has already changed the book before the error (noted, not a FAIL: the answer does not say otherwise).")
new('CS2b4-L07-memo-correct', 'L07 Definition 1.1 paragraph: correctness claim for memoized recursion', 'course/modules/CS/CS2/L07.html:63', 'PASS',
    "The paragraph now says the memoized form is 'not proved here' to store the recurrence's value and that Lab 1 checks agreement on 60 seeded instances (grade C, key-results row at L07.html:655). "
    "The round-4 claim 'both forms are correct when the recurrence is correct' is gone. The remaining generic clause 'differ in which subproblems they touch' is a separate FAIL row CS2b5-L07-differ-generic.")
new('CS2b4-L08-any-stream', 'L08 Lab 1 Part B interpretation: scope of Proposition 2.2', 'course/modules/CS/CS2/L08.html:546; L08.html:112-114', 'PASS',
    "New text: 'Under Assumptions 1 and 2 of Proposition 2.2, at each submission the fills are the sorted-scan fills. The lab checks this on one stream only, and the lab does not check the assumptions.' "
    "The proposition statement (L08.html:111-115) reads 'Assuming Assumptions 1 and 2' and lists the arrival-order hypothesis as item 1 (standing, structural: an order is appended when it rests); "
    "the 'for any stream' wording is gone and the one-stream scope is stated. Checked that the lab does not check the assumptions (no assert on queue order or head position in part_b).")
new('CS2b4-L08-three-counts', 'L08 counts paragraph vs Counts class', 'course/modules/CS/CS2/L08.html:131 vs tests/labs/CS2/lab-CS2-L08-1.py class Counts (twin lines 80-87)', 'PASS',
    "L08.html:131 now says 'four kinds of count: orders added, queue steps, level creations and removals, and binary-search tests, which it logs'. "
    "Counts has orders_added, queue_steps, levels_created, levels_removed (lines 84-87) and Book.search_log holds the binary-search tests (line 108). The four kinds match (level creations and removals count as one kind).")
new('CS2b3-L08-scope-words', 'L08 scope words: floats, prices and quantities', 'course/modules/CS/CS2/L08.html:56 and lab docstring (twin lines 4-6)', 'PASS',
    "L08.html:56 now says 'The book's prices and quantities are never floats; Part A passes one float to show that it is refused.' check_order refuses any non-int type (twin line 92, type(price) is not int); "
    "twin line 275 passes cast(int, 100.5) and the output line 'a float price is refused: prices must be integer cents and quantities integer shares' shows the refusal; grep for '/' in the twin finds only the integer floor division '//' at line 121 and docstring or message text (lines 5, 6, 277); no float value is produced by any code path.")
carry('CS2b4-L08-E-problems', 'course/modules/CS/CS2/L08.html lines 633-652')
new('CS2b4-L08-P-problems', 'L08 P1-P3 solutions', 'course/modules/CS/CS2/L08.html P1-P3 (608-627)', 'PASS',
    'P3 solution (lines 626-627) re-derived this round (see CS2b4-problems-L06-L08). P1 bound n(floor(log2 n)+1) with k-1 <= n and P2 trade price a <= p from the stop test are unchanged lines and carry the round-4 check.')
new('CS2b-struct-template', 'template structure of L05-L08 (sections, lists, labels, blocks, pre, tables)', 'course/modules/CS/CS2/L05.html..L08.html', 'PASS', "L05 unchanged. Element counts of L06, L07 and L08 at 2657ab5 and 09b8751 are identical (grep -o of h2, h3, section, ol, ul, li, label, fieldset, pre, table, div.block): L06 10 h2, 7 section, 27 li, 2 pre, 1 table; L07 11 h2, 7 section, 43 li, 2 pre, 1 table; L08 10 h2, 7 section, 38 li, 3 pre, 1 table. "
"Only paragraph and code-line text changed. The template order of each page is unchanged.")
new('CS2b-prose-banned', 'banned phrases in CS2 L05-L08 prose', 'course/modules/CS/CS2/L05.html..L08.html', 'PASS',
    "re-run this round: grep -i -E 'roughly half|about 6%|historically' L05..L08: 0 hits; ellipsis hits are only inside code blocks (L07.html:385, a Python docstring; tuple[int, ...] type hints).")
new('CS2b-prose-process-words', 'process words in CS2 L05-L08 prose', 'course/modules/CS/CS2/L05.html..L08.html', 'PASS',
    "re-run this round: grep -i -E 'build|builder|verifier|round|REQUEST|unit report' L05..L08: 0 hits.")
new('CS2b-dag-closure', 'DAG: concepts used by L05-L08 vs prerequisite closure', 'course/modules/CS/CS2/L05.html..L08.html data-concept links', 'PASS',
    "check_dag CS2 PASS this round; the changed lines add no data-concept link (L07.html:179 keeps its existing link to big-o-complexity, now stated as 'operation count'). Prerequisite closure unchanged (CS1, M1 per round 4).")
new('CS2b-hours', 'hours: data-hours vs hub and sum', 'course/modules/CS/CS2/L05..L08 data-hours; course/modules/CS/CS2/index.html:145-155', 'PASS',
    'data-hours L05 9, L06 9, L07 10, L08 10 equal the hub cards (index.html:149-152); all 11 lessons sum to 100 (L01 8, L02 9, L03 10, L04 10, L05 9, L06 9, L07 10, L08 10, L09 10, L10 8, L11 7) = data-hours-lessons 100; project 30; total 130 (index.html:29, 31, 42). Pace not judged (architect ruling).')
new('CS2b-figures', 'figures in L05-L08', 'course/modules/CS/CS2/L05.html..L08.html', 'PASS',
    "re-run this round: grep -c '<img|<svg|<figure' returns 0 on each of the four pages.")
carry('CS2b-L05-key-h2', 'course/modules/CS/CS2/L05.html:557')
carry('CS2b-L05-def-2.2', 'course/modules/CS/CS2/L05.html:71-72 and tests/labs/CS2/lab-CS2-L05-1.py min_nodes docstring')
carry('CS2b-L05-E3', 'course/modules/CS/CS2/L05.html:517-519')
carry('CS2b-L06-M3', 'course/modules/CS/CS2/L06.html:415-417')
new('CS2b-L06-intro-scope', 'L06 why-it-matters scope claim', 'course/modules/CS/CS2/L06.html:52', 'PASS',
    "new text: 'This lesson proves both properties. Lab 1 checks the BFS property against exhaustive search, and the DFS property, on seeded graphs.' Both properties are proved on the page (Proposition 2.2 BFS distances, Proposition 3.2 parenthesis property) and the lab checks each (Part A and Part B) on seeded graphs.")
new('CS2b-L07-def1.1', 'L07 paragraph after Definition 1.1', 'course/modules/CS/CS2/L07.html:63', 'FAIL',
    "The sentence 'The two forms differ in which subproblems they touch and in how many calls they make' is a general claim with no computation behind it: for denominations {1} and amount 3, memoized recursion touches {0, 1, 2, 3} and the table fills {0, 1, 2, 3} (ledgers/CS2/scripts/CS2-b-r5/witness.py), so they do not differ in which subproblems they touch there. The other sentences of the paragraph are verified (CS2b4-L07-memo-correct).",
    fix="change to: 'The two forms differ in how many calls they make and in how many subproblems they store. On the LCS pair of Lab 1, Part C, the memoized recursion stores 28 of the 49 cells the table fills; on some instances they touch the same subproblems.'")
carry('CS2b-L07-canon-row', 'course/modules/CS/CS2/L07.html:515')
carry('CS2b-L07-intro-often', 'course/modules/CS/CS2/L07.html:52')
carry('CS2b-L08-prop1.3', 'course/modules/CS/CS2/L08.html:84')
new('CS2b-L08-every-stream', 'L08 Part B sentence: scope of "for every stream"', 'course/modules/CS/CS2/L08.html:546', 'PASS',
    "grep: the phrase 'for every stream' is absent from L08.html:546; the scope now is 'one stream only' (checked by the sentence). The remaining scope issue of that sentence is CS2b4-L08-any-stream, which is PASS.")
new('CS2b-L08-limit-order-book', 'L08 why-it-matters and Section 1 definitions', 'course/modules/CS/CS2/L08.html:52, 56', 'PASS',
    "L08:52 unchanged. L08:56 re-checked (CS2b3-L08-scope-words): prices and quantities are integer, the book refuses a float (check_order), Part A demonstrates the refusal.")
carry('CS2b-L05-heavy-child', 'course/modules/CS/CS2/L05.html:104 and uses at 462, 530, 605')
carry('CS2b-L06-adjacency-matrix', 'course/modules/CS/CS2/L06.html:56, 103, 125, 139, 362, 387-388')
carry('CS2b-L07-R1-about', 'course/modules/CS/CS2/L07.html:622, 719-725')
new('CS2b-L08-prop2.2-hyp', 'L08 Proposition 2.2 hypotheses and proof', 'course/modules/CS/CS2/L08.html:60, 112-114, 121, 546', 'PASS',
    "L08.html:112-114 hypotheses, 121 proof and 546 interpretation re-read this round; the interpretation names Assumptions 1 and 2 as the proposition's statement does (see CS2b4-L08-any-stream). Head and dead entry defined at 60 before first use (unchanged).")
carry('CS2b3-card-c082', 'course/modules/CS/CS2/cards.json CS2-c082 and course/modules/CS/CS2/L06.html:388')
carry('CS2b3-card-c094', 'course/modules/CS/CS2/cards.json CS2-c094 and course/modules/CS/CS2/L07.html:195-198')
carry('CS2b3-L05-remark3.2', 'course/modules/CS/CS2/L05.html:104, 118, 123')
carry('CS2b3-L05-rotation-rule', 'course/modules/CS/CS2/L05.html:104')
carry('CS2b3-L06-weighted', 'course/modules/CS/CS2/L06.html:368, 388 and lab-CS2-L06-1 Part C output (run this round, unchanged)')
carry('CS2b3-L06-row-reads', 'course/modules/CS/CS2/L06.html:125, 388 and lab-CS2-L06-1 line 207')
carry('CS2b3-L06-misconception-2', 'course/modules/CS/CS2/L06.html:384')
carry('CS2b3-L07-prop4.2', 'course/modules/CS/CS2/L07.html:192-203')
carry('CS2b3-L07-quiz9', 'course/modules/CS/CS2/L07.html:654 and 719-725')
carry('CS2b3-L07-greedy-def', 'course/modules/CS/CS2/L07.html:111')
new('CS2b3-L07-hyp-expected', 'L07 Lab 1 expected-result paragraph vs output', 'course/modules/CS/CS2/L07.html:210', 'PASS',
    "L07.html:210 changed this round; re-checked as CS2b-lab-L07 (49 cells, 28 stored, 47 calls, 183 no-memo calls, 3 vs 2 coins, 30+30 instances).")
carry('CS2b3-L08-def-head', 'course/modules/CS/CS2/L08.html:60')
carry('CS2b3-L08-pigeonhole', 'course/modules/CS/CS2/L08.html:572')
new('CS2b3-L08-part-C-bound', 'L08 Part C sentences vs bound', 'course/modules/CS/CS2/L08.html:546 (Part C sentences)', 'PASS',
    "re-derived: a search with 4 comparisons needs floor(log2 L)+1 >= 4, so L >= 8; a list of 7 has bit_length 3. The lab asserts comparisons <= bit_length (twin line 340) and prints 'largest comparison count: 4'.")

# ---- new FAIL rows of this round
new('CS2b5-L07-differ-generic', 'L07 generic claim about subproblems touched (L07:63) and quiz Q6 correct option', 'course/modules/CS/CS2/L07.html:63 and L07.html:703', 'FAIL',
    "Witness (ledgers/CS2/scripts/CS2-b-r5/witness.py): denominations {1}, amount 3: memoized recursion touches {0,1,2,3}; table fill computes {0,1,2,3}. Denominations {1,3,4}, amount 6: both touch {0..6}. "
    "So 'they differ in which subproblems they touch' and the quiz's correct option are false as general statements.",
    fix="see CS2b-L07-def1.1 and CS2b4-quiz-L05-L08 (replace both sentences with the LCS example and an explicit 'can')")
new('CS2b5-card-c093', 'card CS2-c093 vs L07.html:179 (Proposition 3.5)', 'course/modules/CS/CS2/cards.json CS2-c093 vs course/modules/CS/CS2/L07.html:179', 'FAIL',
    "card back: 'Its running time is O(mn) (Proposition 3.5).' Current L07.html:179: 'Its operation count is therefore O(mn)'. The lesson changed this round to operation counts (architect Q3: counts, never wall-clock time); the card does not agree.",
    fix="replace 'Its running time is O(mn)' with 'Its operation count is O(mn)' in CS2-c093")
new('CS2b5-card-c102', 'card CS2-c102 vs L08.html:56 and grade', 'course/modules/CS/CS2/cards.json CS2-c102 vs course/modules/CS/CS2/L08.html:56', 'FAIL',
    "card (grade T): 'The code raises an error for any other type and never uses floating point (Section 1).' Current L08.html:56: 'The book's prices and quantities are never floats; Part A passes one float to show that it is refused.' "
    "The card's wording is not the current lesson's and it is graded T for a claim about the lab code, which the page does not prove (the refusal is shown by Part A; the absence of floats is a reading of the code).",
    fix="change the back to: 'Prices are integer cents, so 10000 is 100.00 currency units. Quantities are integer shares. The book's prices and quantities are never floats: Part A of Lab 1 shows a float price refused with a TypeError.' and grade it C with basis 'Lab 1, Part A'")
new('CS2b5-card-c114', 'card CS2-c114 vs L08.html:176 (Lab 1 Part B)', 'course/modules/CS/CS2/cards.json CS2-c114 vs course/modules/CS/CS2/L08.html:176', 'FAIL',
    "card back: 'a reference that sorts its resting orders on every match'. Current L08.html:176 and the twin (Reference, lines 212-238) say the reference sorts the crossing candidates on every match. The card's wording is the old text.",
    fix="change the card back to: 'After every message, the trades, the best bid and the best ask of the book match a reference that sorts the crossing candidates on every match.'")
new('CS2b5-lab-L08-reference-key', 'twin docstring: the reference sort key', 'tests/labs/CS2/lab-CS2-L08-1.py lines 12-14 (docstring) vs lines 213, 222, 225', 'FAIL',
    "docstring: 'a reference that keeps a flat list of resting orders and sorts the crossing candidates by (price, arrival number) on every match'. "
    "The code sorts ask-side candidates by (-price, oid) (line 225): the highest bid first, then arrival. The docstring is wrong for the ask side. The page's L08.html:176 text is correct; the embedded code block contains the same docstring, so the fix must be followed by tools/embed_labs.py --refresh for lab-CS2-L08-1 and a re-run of run_labs.",
    fix="change the docstring to 'sorts the crossing candidates by price (lowest ask first, highest bid first) and then by arrival number', then re-embed the L08 lab with tools/embed_labs.py course/modules/CS/CS2/L08.html --refresh lab-CS2-L08-1 and re-run run_labs and the L08 lab output check")
new('CS2b4-L06-twin-docstring', 'L06 twin docstring Part C vs output', 'tests/labs/CS2/lab-CS2-L06-1.py:12 (docstring); course/modules/CS/CS2/L06.html:137', 'PASS',
    "docstring now: 'The two paths differ for a and c; for b they coincide.' Output this round: 'to a: bfs_path s-a hops 1 weight 10 | lightest_path s-b-a hops 2 weight 2' (differ), "
    "'to b: bfs_path s-b hops 1 weight 1 | lightest_path s-b hops 1 weight 1' (coincide), 'to c: bfs_path s-a-c hops 2 weight 11 | lightest_path s-b-a-c hops 3 weight 3' (differ). The page L06.html:137 has the same sentence and the embedded block equals the twin.")
