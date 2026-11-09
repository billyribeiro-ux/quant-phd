"""Builds ledgers/M4/M4-a.json (closing delta, rulings 30 and 37) from the base fragment.

Every base row id is kept. Re-verified rows carry fresh evidence; carried rows keep the base
evidence under the carry prefix, and only where the cited files are byte-identical since 2a805c83.
"""
import json
import re
import sys

BASE = "/Users/billyribeiro/.fanout/frags/G-M4-a.round1.json"
OUT = sys.argv[1]
base = json.load(open(BASE, encoding="utf-8"))
PIN = "d9de2fe5eea982d14cd9f922a61676b847506fbc"
PREV = "2a805c831410ab77c38c227f7e121e8537193ce9"
S = "ledgers/M4/scripts/M4-a-r1/"

FRESH = {
 "A-G01": ("2.9 structure gate", "tools/check_pages.py --unit M4",
  "Re-run at d9de2fe5: exit 0, 'check_pages M4: PASS' (" + S + "c_check_pages.out)."),
 "A-G02": ("2.9 DAG gate", "tools/check_dag.py --unit M4",
  "Re-run at d9de2fe5: exit 0, 'check_dag M4: PASS' (" + S + "c_check_dag.out)."),
 "A-G03": ("2.6 projects gate (command row; project.html outside slice a)", "tools/check_projects.py --unit M4",
  "Re-run at d9de2fe5: exit 0, 'check_projects M4: PASS' (" + S + "c_check_projects.out). project.html is byte-identical since 2a805c83."),
 "A-G04": ("2.5 labs", "tools/run_labs.py --unit M4",
  "Re-run at d9de2fe5: exit 0, 'run_labs M4: PASS (13/13)' (" + S + "c_run_labs.out). run_labs checks each page lab byte-identical to its twin (tools/run_labs.py:87-88) and the expected output against the twin output."),
 "A-G05": ("2.5 twins alone; page code equals twin; expected equals output", "tests/labs/M4/lab-M4-L01-1.py .. lab-M4-L04-1.py vs course/modules/M/M4/L01..L04.html",
  "Twins run alone: `.venv/bin/python -I -W error tests/labs/M4/lab-M4-L0N-1.py` exit 0 for N = 1..4 (L01 output " + S + "c_twin_L01.out: Q(3/5) = 0, Q(61/100) = 1, Q(99/100) = 3, '100 of 100'). Page-code-equals-twin and expected-equals-output are the run_labs checks of A-G04 (exit 0). L01.html lab block (lines 138-271) unchanged in the delta."),
 "A-G06": ("2.9 page_smoke (pages alone)", "tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04",
  "Re-run at d9de2fe5: exit 0, 'page_smoke M4: PASS' (" + S + "c_page_smoke.out)."),
 "A-G07": ("ruff", "ruff check tests/labs/M4 course/modules/M/M4; ruff format --check tests/labs/M4",
  "Re-run: 'All checks passed!' and '13 files already formatted', exit 0 (" + S + "c_ruff.out)."),
 "A-G08": ("mypy strict", "mypy --no-incremental",
  "Re-run: 'Success: no issues found in 386 source files', exit 0 (" + S + "c_mypy.out). Repository-wide gate; 105 .py files changed in other units in 2a805c83..HEAD, none under M4."),
 "A-G09": ("repository state", "git status after all gate runs",
  "git status at d9de2fe5 after the runs: no tracked file of the course, tests or tools modified; untracked entries are the .venv symlink and this round's scratch files under " + S + ". The fragment ledgers/M4/M4-a.json is the only tracked file this round writes; it is not committed."),
 "A-G10": ("relevant pytest", "tests/test_page_checks.py test_page_smoke.py test_run_labs.py test_docs_figures.py test_curriculum.py test_labs.py",
  "Re-run: '443 passed in 51.08s' (" + S + "c_pytest_full.out). test_labs.py, test_run_labs.py, test_page_checks.py, test_page_smoke.py, test_curriculum.py, test_docs_figures.py; the -k subset gave the same 443."),
 "A-G11": ("2.1 registry", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M4 (live Crossref)",
  "Offline re-run at d9de2fe5: exit 0, '560 entries, 0 problems' (" + S + "c_verify_refs_offline.out). The live Crossref half is NOT repeated this round; it is carried from round 1 because references/ is byte-identical since 2a805c83 (git diff empty)."),
 "A-G12": ("2.7 card numbers; no dangling card ids", "course/modules/M/M4/cards.json vs L01..L04.html",
  "Re-run by " + S + "c_cards_check.py: 219 cards, ids unique, 90 slice cards (L01 24, L02 20, L03 27, L04 19), no exact or front duplicates, M4-c014/c028/c065 absent, no M4 page names a card id, grades in {T, C} (" + S + "c_cards_check.out)."),
 "A-G13": ("2.8 generated site data (not edited)", "tools/build_site.py --check",
  "Re-run: exit 0, 'site data current: 6 outputs' (" + S + "c_build_site_check.out)."),
 "A-G14": ("2.8 data manifest", "tools/fetch_data.py --check",
  "Re-run: exit 0, 'fetch_data: 3 datasets, 0 problems' (" + S + "c_fetch_data_check.out)."),
 "A-G15": ("generated curriculum current", "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json",
  "Re-run: render exit 0, then git diff --exit-code exit 0 (" + S + "c_render_curriculum.out, " + S + "c_render_diff.out)."),
 "A-H01": ("2.9 structure: hub", "course/modules/M/M4/index.html:29-184",
  "Tag-level diff of index.html against 2a805c83 (" + S + "c_tagdiff_index.out): the only change is one text token inside the explain paragraph at index.html:135; the element structure is identical. check_pages M4 PASS (A-G01)."),
 "A-H05": ("DAG: no M3 concept by name", "course/modules/M/M4/index.html (whole file)",
  "Subject changed at index.html:135. The new sentences name only M4 Lesson 1 terms (distribution function, Proposition 3.2, Proposition 3.4, rung 1, sorted losses, project.html); no M3 concept name. The rest of the file is byte-identical to 2a805c83 and was scanned at round 1. check_dag M4 PASS (A-G02)."),
 "A-H06": ("placement structure", "course/modules/M/M4/index.html:68-143",
  "Changed line 135 is inside the placement block. The tag-level diff (" + S + "c_tagdiff_index.out) shows no tag, attribute or data-* change, so the structure is unchanged; check_pages PASS."),
 "A-H09": ("2.9 placement skill check 1 (rung 1) key", "course/modules/M/M4/index.html:133-135",
  "Subject changed (index.html:135). Key re-derived: values 0, 1, 2 with probabilities 1/4, 1/2, 1/4; F(0) = 1/4 < 1/2 <= 3/4 = F(1); the 0.5 quantile is 1 (Definition 3.1). index.html:133 data-answer=\"1\" data-tolerance=\"0\" matches. The values are distinct, so Proposition 3.2 applies to them. The explain paragraph no longer asserts the rung-1 rank equals the Definition 3.1 quantile (see A-H16)."),
 "A-H16": ("hub claim: rung 1 worked example (round-1 FAIL; closing delta)", "course/modules/M/M4/index.html:135",
  "Re-verified from scratch. The round-1 residual sentence ('The same convention as rung 1 applies: the quantile is the least value whose distribution function reaches the level') is deleted (diff in " + S + "c_delta_index.diff). The paragraph now says Rung 1 takes the rank ceil(0.99 n) of its sorted losses (project.html, Rungs 1 and 2: project.html:61 and :109 use the 1-based rank ceil(0.99 n)), that Proposition 3.4 proves that rank for distinct values only (L01.html:119 states 'distinct real numbers'), that the whole-cent losses can repeat, and that this lesson therefore does not prove the rank for repeated values. Repeats are real: rung-1 code (project.html data-run, extracted and run with python -I, " + S + "rung1_block.py) gives 616 extra copies in the Gaussian sample and 680 in the Student-t sample (" + S + "c_rung1_dups.out). No identity is asserted. PASS."),
 "L01-MATH": ("2.4 mathematics", "L01.html:80-135 (Props 2.2, 3.2, Remark 3.3, Prop 3.4, Examples 3.5, 3.6)",
  "Re-verified from scratch. Proposition 2.2 (a)-(d), Proposition 3.2 proof, Remark 3.3 proof, Proposition 3.4 proof and Example 3.6 values (F(-1)=3/10, F(0)=3/5, F(1)=4/5, Q(1/2)=0, Q(3/5)=0, Q(61/100)=1) re-derived and correct. FAIL on Example 3.5 (L01.html:130): it applies the index of Proposition 3.4 to n = 150 and n = 200 values and states 'the quantile is the 149th (198th) smallest value' without the distinct-values hypothesis of Proposition 3.4 (L01.html:119). This is the same defect as L01-P34-HYP; the base PASS of this row is withdrawn for that sentence."),
 "L01-PROBLEMS": ("2.4 worked solutions", "L01.html:302-404",
  "Re-verified from scratch, all of 302-404 read. M1 (Q(1/2)=0 for the parity law; Proposition 3.2 applies, values distinct), M2 (F(5)=7/10, Q(7/10)=5, Q(71/100)=7), M3 (40 distinct values: index 36 and 37), P1 (nondecreasing, weights nonnegative), P2, P3 (Q(1)=x_m), E1 (F(2)=9/10 < 99/100 <= 1 gives 3; matches twin output Q(99/100) = 3), E2 (matches twin output at x = 0, eps line), E3 (100 of 100), R1 (Q^s(3/5)=1 and agreement elsewhere, re-derived), R2 (left and right limits at 3/5: 0 and 1), R3 (the changed sentence at L01.html:401 now reads 'every table with positive weights and distinct values', which is the hypothesis of Proposition 3.2 at L01.html:103-105). All numbers recomputed; the twin outputs are in " + S + "c_twin_L01.out."),
 "L01-P34-HYP": ("every use of Proposition 3.4 states or meets its distinct-values hypothesis (the Prop 3.4 hypothesis is the subject changed by this delta)",
  "course/modules/M/M4/L01.html:130 (Example 3.5); L01.html:278 (canon-breaks bullet 2); Prop 3.4 statement at L01.html:119",
  "Re-verified from scratch over every use. The delta fix at L01.html:296-297 (misconception 3, now 'for 150 distinct equally likely values') and at :277, :280, :326 ('forty distinct values'), :416, :452, :457 and cards M4-c010, c011, c015 (cards.json lines 68, 75, 96-97) all state distinctness. Two uses still omit it: (1) Example 3.5 at L01.html:130, 'Take n = 200 ... the quantile is the 198th smallest value. Take n = 150 ... The quantile is the 149th smallest value', applies the Proposition 3.4 index to unspecified n values; (2) canon-breaks bullet 2 at L01.html:278, 'Example 3.5 gives 149 for n = 150 and p = 0.99 ... the 148th value has distribution function 148/150', which presupposes distinct equally likely values. Card M4-c011 (lines 75-76) carries 'distinct' while its lesson example does not. Ruling 26 kind: missing hypothesis. Verdict FAIL."),
 "CARDS-DUP": ("2.7 duplicate cards (full scan of the cards file)", "course/modules/M/M4/cards.json",
  "Re-run by " + S + "c_cards_check.py (" + S + "c_cards_check.out): 219 cards, 219 unique ids, 0 exact front+back duplicate pairs, 0 duplicate fronts. The changed card M4-c079 is unique."),
 "CARDS-DELTA": ("delta: cards changed or added in this range", "course/modules/M/M4/cards.json (git diff 2a805c83..d9de2fe5)",
  "Re-verified: " + S + "c_cards_delta.out shows the 219 ids identical in order to 2a805c83 and exactly one changed object, M4-c079 (the back loses the word 'only'). No card added or removed in this range; the L09 and L10 cards of the base delta are at HEAD and outside slice a."),
 "DELTA-CARD-C079": ("delta: card M4-c079 (lesson L05) text", "course/modules/M/M4/cards.json (M4-c079); L05.html:118, :281, :293, :422, :483",
  "Re-verified. Back now reads 'No. Remark 1.8 gives Y = X^2 with X uniform on {-1, 0, 1}: the correlation is 0, while Y is a function of X. Correlation measures linear association.' Remark 1.8 title (L05.html:118) is '(correlation measures linear association)'; the example at L05.html:293 is the same pair; E[X] = 0 and E[XY] = E[X^3] = 0 give Cov = 0 and correlation 0. The grade T matches L05.html:422. 'only' is removed, so the scope word carries no claim beyond the title."),
 "DELTA-CARD-REMOVALS": ("delta: removed duplicate cards M4-c028 and M4-c065", "course/modules/M/M4/cards.json",
  "Re-verified: M4-c014, M4-c028 and M4-c065 are absent from cards.json at d9de2fe5 (" + S + "c_cards_check.out), and no id was removed in 2a805c83..d9de2fe5 (" + S + "c_cards_delta.out)."),
 "NOTATION-A": ("2.4 / notation registry (changed lines)", "course/modules/M/M4/index.html:135; L01.html:296-297, :401; cards.json M4-c079; notation/notation.json",
  "Re-verified on the changed lines. Symbols: F, Q, p, n, y_j, \\lceil \\rceil, \\tfrac, \\ge, \\le, \\dots, \\varepsilon, X. None is a registered program-wide symbol given another meaning (notation/notation.json has 8 symbol entries and 26 macros; notation.json is byte-identical since 2a805c83). Observation, unchanged from the base and not a row defect: \\lceil and \\rceil have no notation.json entry at either pin; they are KaTeX delimiters, not registered symbols, and no registered symbol is reused."),
 "NOTATION-MACRO": ("registered macros only (changed lines)", "course/modules/M/M4/index.html:135; L01.html:296-297, :401",
  "Re-verified on the changed lines: no macro outside the KaTeX built-ins already used on the page (\\lceil, \\rceil, \\tfrac, \\ge, \\le, \\dots); no \\mathbb{R}; no unregistered program macro."),
 "PROCESS-A": ("2.9 process words in learner text (changed text)", "course/modules/M/M4/index.html:135; L01.html:296-297, :401; cards.json M4-c079",
  "Re-verified: grep of the added lines of the delta for build, agent, verifier, round (as a process word), ruling, delta, check-list returns none (the one 'rounds down' is the learner's wrong claim at L01.html:296)."),
 "SCOPE-A": ("scope words (changed text)", "course/modules/M/M4/index.html:135; L01.html:296-297, :401; cards.json M4-c079",
  "Re-verified: added scope words are 'every table with positive weights and distinct values' (L01.html:401, the hypothesis of Proposition 3.2 with its proof for an arbitrary p, L01.html:103-112), 'any other p' and 'for all p' (L01.html:401, the grid check does not cover all p, the proof does), 'for distinct values only' (index.html:135, Proposition 3.4 states distinct values, L01.html:119), 'only' removed from M4-c079. Each is backed by a stated hypothesis or proof."),
 "NUM-A": ("2.2 numbers in prose (changed text)", "course/modules/M/M4/index.html:135; L01.html:296-297; cards M4-c079",
  "Re-verified: index.html:135 F(0) = 1/4 < 1/2, F(1) = 3/4 >= 1/2, quantile 1. L01.html:296-297: 0.99 x 150 = 148.5, ceiling 149, floor 148; the 149th value's F is 149/150 = 0.9933 >= 0.99 and the 148th's is 148/150 = 0.9867 < 0.99 (L01.html:278). M4-c079: correlation 0 for Y = X^2 with X uniform on {-1, 0, 1}. All re-derived."),
 "GRADE-A": ("2.3 grades (re-graded)", "index.html; L01..L04.html; cards.json (slice)",
  "Re-verified: the delta changes no data-grade attribute and no 'grade' field (grep of the +/- lines of the M4 delta (" + S + "c_delta_L01_cards.diff and index diff): 0 lines contain 'grade'; M4-c079 keeps grade T)."),
 "STRUCT-A": ("2.9 lesson structure", "course/modules/M/M4/L01..L04.html",
  "Re-verified: tag-level diff of L01.html against 2a805c83 is empty (" + S + "c_tagdiff_L01.out, 0 lines), so the section, block and problem structure is unchanged; L02-L04 byte-identical; check_pages PASS."),
 "DAG-A": ("2.9 DAG and definitions once", "check_dag.py --unit M4; L01..L04.html dfn tags",
  "check_dag M4 re-run PASS (A-G02). The delta adds no dfn or data-concept tag (grep of +/- lines: 0 matches)."),
}

CARRIED = {
 "A-H02": "course/modules/M/M4/index.html:29 and the data-hours attributes of L01..L10",
 "A-H03": "course/modules/M/M4/index.html:48-56",
 "A-H04": "course/modules/M/M4/index.html:58-66; curriculum/01-foundations.yaml",
 "A-H07": "course/modules/M/M4/index.html:73-131",
 "A-H08": "course/modules/M/M4/index.html:140; L06.html:59, :158",
 "A-H10": "course/modules/M/M4/index.html:147-160 and L01..L04.html headings",
 "A-H11": "course/modules/M/M4/index.html:70, :164; project.html:42",
 "A-H12": "course/modules/M/M4/index.html:37, :175, :187; L02.html:146, :507; L03.html:122, :477",
 "A-H13": "course/modules/M/M4/index.html:181-183; references/references.json",
 "A-H14": "curriculum/01-foundations.yaml:190-194",
 "A-H15": "course/modules/M/M4/index.html:162-170; project.html:42-47",
 "L01-PROSE": "course/modules/M/M4/L01.html:51-99",
 "DELTA-L01-P34-DISTINCT": "course/modules/M/M4/L01.html:277 and :280",
 "L01-DELTA-86": "course/modules/M/M4/L01.html:85-86",
 "L01-QUIZ": "course/modules/M/M4/L01.html:424-494",
 "L01-GRADES": "course/modules/M/M4/L01.html:43-48, :103, :113, :119, :413-418",
 "L01-FWD": "course/modules/M/M4/L01.html:37-38, :95, :505",
 "L01-LAB": "course/modules/M/M4/L01.html:138-271; tests/labs/M4/lab-M4-L01-1.py",
 "L02-PROSE": "course/modules/M/M4/L02.html:51-101",
 "L02-MATH": "course/modules/M/M4/L02.html:63-142",
 "L02-LAB": "course/modules/M/M4/L02.html:144-263; tests/labs/M4/lab-M4-L02-1.py",
 "L02-PROBLEMS": "course/modules/M/M4/L02.html:298-401",
 "L02-QUIZ": "course/modules/M/M4/L02.html:421-492",
 "L02-CANON": "course/modules/M/M4/L02.html:269-272",
 "L02-MISC": "course/modules/M/M4/L02.html:279-296",
 "L02-FWD-COVARIANCE": "course/modules/M/M4/L02.html:345-347",
 "L02-FOOTER-SCOPE": "course/modules/M/M4/L02.html:494-507",
 "L03-PROSE": "course/modules/M/M4/L03.html:51-76",
 "L03-MATH": "course/modules/M/M4/L03.html:57-134",
 "L03-LAB": "course/modules/M/M4/L03.html:120-239; tests/labs/M4/lab-M4-L03-1.py",
 "L03-NUMBERING": "course/modules/M/M4/L03.html:53-110",
 "L03-STD-NORMAL-DUP": "course/modules/M/M4/L03.html (whole page)",
 "L03-CANON": "course/modules/M/M4/L03.html:241-250",
 "L03-MISC": "course/modules/M/M4/L03.html:252-268",
 "L03-PROBLEMS": "course/modules/M/M4/L03.html:270-373",
 "L03-QUIZ": "course/modules/M/M4/L03.html:392-462",
 "L03-GRADES": "course/modules/M/M4/L03.html:42-49, :381-388, :401-407",
 "L03-FOOTER-SCOPE": "course/modules/M/M4/L03.html:464-477",
 "L03-PROP28-SCOPE": "course/modules/M/M4/L03.html:89-101",
 "L04-PROSE": "course/modules/M/M4/L04.html:52-70, :137-145",
 "L04-TERM-ORDER": "course/modules/M/M4/L04.html:52, :59, :65, :98, :131, :139",
 "L04-REMARK-1-3": "course/modules/M/M4/L04.html:70; tests/labs/M4/lab-M4-L04-1.py",
 "L04-MATH": "course/modules/M/M4/L04.html:73-169",
 "L04-DELTA-53": "course/modules/M/M4/L04.html:52-53",
 "L04-PROBLEMS": "course/modules/M/M4/L04.html:331-434",
 "L04-QUIZ": "course/modules/M/M4/L04.html:453-527",
 "L04-CANON-MISC": "course/modules/M/M4/L04.html:303-329",
 "L04-FOOTER": "course/modules/M/M4/L04.html:530-543",
 "L04-FWD": "course/modules/M/M4/L04.html:52, :99, :539",
 "L04-LAB": "course/modules/M/M4/L04.html:172-301; tests/labs/M4/lab-M4-L04-1.py",
 "CARDS-L01": "course/modules/M/M4/cards.json (the 24 L01 cards)",
 "CARDS-L02": "course/modules/M/M4/cards.json (the 20 L02 cards)",
 "CARDS-L03": "course/modules/M/M4/cards.json (the 27 L03 cards)",
 "CARDS-L04": "course/modules/M/M4/cards.json (the 19 L04 cards)",
 "CARDS-NUMBERS": "course/modules/M/M4/cards.json (90 slice cards) vs L01..L04.html",
 "CARD-M4-c219": "course/modules/M/M4/cards.json (M4-c219)",
 "DELTA-CARD-C258": "course/modules/M/M4/cards.json (M4-c258); L04.html:168-172, :326",
 "DELTA-CARD-C263": "course/modules/M/M4/cards.json (M4-c263); L01.html:134-137",
 "DELTA-CARD-C023": "course/modules/M/M4/cards.json (M4-c023)",
 "NOTATION-REG": "course/modules/M/M4/L03.html:75-86; notation/notation.json",
 "ASSUMP-A": "course/modules/M/M4/index.html:138-140; L01..L04.html",
 "DAG-HUB-PREVIEW": "course/modules/M/M4/index.html:147-160",
 "DAG-L02-L04-USES": "course/modules/M/M4/L02..L04.html meta lines 37-39",
 "DAG-SD-TWICE": "course/modules/M/M4/L05.html:79-80; L02.html:100-101",
 "DELTA-L01-META": "course/modules/M/M4/L01.html:7",
 "DELTA-HUB-LADDER-LINK": "course/modules/M/M4/index.html:70",
 "DATA-A": "course/modules/M/M4/index.html:37, :175, :187; L02.html:146, :507; L03.html:122, :477",
}

CARRY_FILES = {
 "A-H02": "course/modules/M/M4/index.html:29 and the data-hours attributes (the delta's index.html hunk is :135 only)",
 "A-H03": "course/modules/M/M4/index.html:48-56",
 "A-H04": "course/modules/M/M4/index.html:58-66 (lines unchanged); curriculum/01-foundations.yaml",
 "A-H07": "course/modules/M/M4/index.html:73-131",
 "A-H08": "course/modules/M/M4/index.html:140 (line unchanged); course/modules/M/M4/L06.html",
 "A-H10": "course/modules/M/M4/index.html:147-160 and the L01..L04 heading lines (unchanged)",
 "A-H11": "course/modules/M/M4/index.html:70, :164 (lines unchanged); course/modules/M/M4/project.html:42",
 "A-H12": "course/modules/M/M4/index.html:37, :175, :187 (lines unchanged); L02.html and L03.html",
 "A-H13": "course/modules/M/M4/index.html:181-183 (lines unchanged); references/references.json",
 "A-H14": "curriculum/01-foundations.yaml:190-194",
 "A-H15": "course/modules/M/M4/index.html:162-170 (lines unchanged); course/modules/M/M4/project.html:42-47",
 "L01-PROSE": "course/modules/M/M4/L01.html:51-99",
 "L01-DELTA-86": "course/modules/M/M4/L01.html:85-86",
 "L01-QUIZ": "course/modules/M/M4/L01.html:424-494",
 "L01-GRADES": "course/modules/M/M4/L01.html:43-48, :103, :113, :119, :413-418",
 "L01-FWD": "course/modules/M/M4/L01.html:37-38, :95, :505",
 "L01-LAB": "course/modules/M/M4/L01.html:138-271 (lab block unchanged); tests/labs/M4/lab-M4-L01-1.py",
 "DELTA-L01-P34-DISTINCT": "course/modules/M/M4/L01.html:277 and :280",
 "CARDS-L01": "the 24 L01 card objects in course/modules/M/M4/cards.json (the delta changes M4-c079 only)",
 "CARDS-L02": "the 20 L02 card objects in course/modules/M/M4/cards.json (the delta changes M4-c079 only)",
 "CARDS-L03": "the 27 L03 card objects in course/modules/M/M4/cards.json (the delta changes M4-c079 only)",
 "CARDS-L04": "the 19 L04 card objects in course/modules/M/M4/cards.json (the delta changes M4-c079 only)",
 "CARDS-NUMBERS": "the 90 slice card objects in course/modules/M/M4/cards.json and L01..L04.html",
 "CARD-M4-c219": "the M4-c219 card object in course/modules/M/M4/cards.json",
 "DELTA-CARD-C258": "the M4-c258 card object; course/modules/M/M4/L04.html:168-172, :326 (unchanged)",
 "DELTA-CARD-C263": "the M4-c263 card object; course/modules/M/M4/L01.html:134-137 (unchanged)",
 "DELTA-CARD-C023": "the M4-c023 card object in course/modules/M/M4/cards.json",
 "NOTATION-REG": "course/modules/M/M4/L03.html and notation/notation.json",
 "ASSUMP-A": "course/modules/M/M4/index.html:138-140 (lines unchanged); L02.html, L03.html, L04.html",
 "DAG-HUB-PREVIEW": "course/modules/M/M4/index.html:147-160",
 "DAG-L02-L04-USES": "course/modules/M/M4/L02.html, L03.html, L04.html",
 "DAG-SD-TWICE": "course/modules/M/M4/L05.html:79-80 (outside the delta) and L02.html:100-101",
 "DELTA-L01-META": "course/modules/M/M4/L01.html:7 (line unchanged)",
 "DELTA-HUB-LADDER-LINK": "course/modules/M/M4/index.html:70 (line unchanged)",
 "DATA-A": "course/modules/M/M4/index.html:37, :175, :187 (lines unchanged); L02.html:146, :507 and L03.html:122, :477",
}

def carry_files(rid):
    if rid in CARRY_FILES:
        return CARRY_FILES[rid]
    for pre, f in (("L02", "course/modules/M/M4/L02.html"), ("L03", "course/modules/M/M4/L03.html"),
                   ("L04", "course/modules/M/M4/L04.html")):
        if rid.startswith(pre + "-"):
            extra = " and tests/labs/M4/lab-M4-%s-1.py" % pre if rid.endswith("LAB") else ""
            return f + extra + ""
    raise SystemExit("no cited subject for carried row " + rid)

def strip_carry(ev):
    while ev.startswith("Carried from round"):
        i = ev.find("): ")
        if i < 0:
            break
        ev = ev[i + 3:]
    return ev

rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in FRESH:
        check, location, evidence = FRESH[rid]
        status = "PASS"
        if rid == "L01-P34-HYP" or rid == "L01-MATH":
            status = "FAIL"
        row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    elif rid == "A-G11":
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
               "evidence": FRESH["A-G11"][2]}
    elif rid == "A-H16":
        check, location, evidence = FRESH["A-H16"]
        row = {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}
    elif rid in CARRIED:
        files = carry_files(rid)
        row = {"id": rid, "check": r["check"], "location": CARRIED[rid], "status": "PASS",
               "evidence": f"Carried from round 1 ({files}; byte-identical since the previous pin {PREV}): "
                           + strip_carry(r["evidence"])}
    else:
        raise SystemExit("unhandled row " + rid)
    rows.append(row)

FIX = {
 "L01-P34-HYP": "In course/modules/M/M4/L01.html:130 state the hypothesis before Example 3.5, e.g. 'Let X take n equally likely distinct values, as in Proposition 3.4', so that both quantile claims apply Proposition 3.4 as stated. In L01.html:278 change 'Example 3.5 gives 149 for n = 150 and p = 0.99' to 'Example 3.5 gives 149 for n = 150 distinct equally likely values and p = 0.99'. Then re-run check_pages --unit M4, page_smoke --unit M4 --pages L01, run_labs --unit M4 and delta-verify L01.html:130 and :278.",
 "L01-MATH": "Same edit as L01-P34-HYP: L01.html:130 (Example 3.5) must state that its n values are distinct and equally likely, as Proposition 3.4 requires; L01.html:278 likewise. No other line of 80-135 changes. Then delta-verify.",
}
for r in rows:
    if r["status"] != "PASS":
        r["fix"] = FIX[r["id"]]

ids = [r["id"] for r in base["rows"]]
assert [r["id"] for r in rows] == ids

# L01-PROBLEMS was in CARRIED? it is in FRESH; L01-P34-HYP and L01-MATH are FAIL.
for r in rows:
    if r["id"] in ("L01-PROBLEMS",):
        r["status"] = "PASS"
# DELTA-L01-P34-DISTINCT and L01-LAB and others are carry/PASS.

counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"

registry = list(base["registry_flags"])
freshness = list(base["freshness_flags"]) + [
    "Closing delta round 2 (pin d9de2fe5): live Crossref verify_refs run not repeated; offline run 560 entries, 0 problems; live half carried from round 1 (references/ byte-identical since 2a805c83)."
]

notes = (
 "Closing delta (rulings 30, 37, 26 kinds only, 38a, 39, 40) of slice a from the base fragment G-M4-a.round1.json (pin 2a805c831410ab77c38c227f7e121e8537193ce9) to d9de2fe5eea982d14cd9f922a61676b847506fbc. "
 "git diff 2a805c83..HEAD over course/modules/M/M4, tests/labs/M4, notation, references, tools, curriculum, course/assets: three files changed in slice a: L01.html (lines 296-297, the misconception 3 wording; line 401, the R3 solution sentence), index.html (line 135, the rung-1 skill-check explain paragraph; tag-level structure unchanged) and cards.json (M4-c079 back loses 'only'). No test, lab twin, notation, reference, tool or curriculum file changed under M4; project.html is byte-identical. "
 "Re-verified from scratch: every base non-PASS row (A-H16, L01-P34-HYP), every row whose subject changed (A-G01..A-G15 gates re-run, A-H01, A-H05, A-H06, A-H09, L01-PROBLEMS, DELTA-CARD-C079, CARDS-DUP, CARDS-DELTA, DELTA-CARD-REMOVALS, NOTATION-A, NOTATION-MACRO, PROCESS-A, SCOPE-A, NUM-A, GRADE-A, STRUCT-A, DAG-A), and L01-MATH, whose PASS is withdrawn because its Example 3.5 is inside the scope of L01-P34-HYP. "
 "A-H16 is fixed: the residual 'same convention as rung 1' equivalence is deleted and the paragraph states that the rank for repeated values is not proved on this lesson (repeats verified: 616 and 680 extra copies, c_rung1_dups.out). "
 "L01-P34-HYP remains FAIL on the ruling-26 'missing hypothesis' kind: Proposition 3.4 is applied without the distinct-values hypothesis in Example 3.5 (L01.html:130) and in canon-breaks bullet 2 (L01.html:278). The delta fix at L01.html:297 is correct and the other uses (L01 :277, :280, :326, :416, :452, :457, cards c010, c011, c015) are distinct. "
 "Fix for the FAIL rows: in course/modules/M/M4/L01.html:130 prefix the example with 'Let X take n equally likely distinct values, as in Proposition 3.4' (or 'For n equally likely distinct values'); in L01.html:278 change 'Example 3.5 gives 149 for n = 150 and p = 0.99' to 'Example 3.5 gives 149 for n = 150 distinct equally likely values and p = 0.99'. Then re-run check_pages --unit M4, page_smoke for L01, run_labs --unit M4 and this delta on L01.html:130 and :278. "
 "Scope not checked this round: L05..L10 pages and cards except M4-c079 (outside slice a), M4-c259..c262 (L09, L10 cards, outside slice a), project.html content, and the live Crossref half of verify_refs. "
 "Rulings: 38a, 39 and 40 do not apply to slice a (no E3 or CS2 content). Ruling 37: no new mutants were written; slice a has no grader and the standing mutant set for slice a is empty. "
 "Observations (notes, not rows): \\lceil and \\rceil have no notation.json entry at either pin; the base's observation on that is unchanged. The byte-identical cards in the M4 slice were not re-read line by line this round (carried under ruling 30). The round-1 scratch outputs under " + S + " are the base's; this round's outputs are the c_* files and build_fragment_verifyH1.py."
)

summary = (
 f"Closing delta round 1 for M4-a at d9de2fe5 (base 2a805c83): {len(rows)} rows; {counts.get('PASS',0)} PASS, {counts.get('FAIL',0)} FAIL, {counts.get('UNVERIFIABLE',0)} UNVERIFIABLE. "
 "FAIL: L01-P34-HYP (Proposition 3.4 applied without distinct values in Example 3.5 at L01.html:130 and canon-breaks bullet 2 at L01.html:278) and L01-MATH, which carries the same Example 3.5 defect. A-H16 is PASS (defect fixed at index.html:135). Verdict FAIL pending one ruling-26 fix and a delta re-verification of L01.html:130 and :278."
)

frag = {
 "unit": "M4",
 "slice": "a",
 "round": 1,
 "verifier": "Claude Haiku 5.5 independent verifier (verifyH1-M4-a), closing delta",
 "pin": PIN,
 "base": PREV + " (base fragment ~/.fanout/frags/G-M4-a.round1.json)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyH1-M4-a",
 "scratch": S,
 "verified_at": "2026-11-09",
 "verdict": verdict,
 "rows": rows,
 "mutants": [],
 "registry_flags": registry,
 "freshness_flags": freshness,
 "notes": notes,
 "summary": summary,
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), counts, verdict)
