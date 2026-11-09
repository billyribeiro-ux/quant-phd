"""Write ledgers/LX1/LX1-b.json (round 23) from the round-21 row ids. Row ids are kept; statuses and evidence come from
this round's commands and reads (see out/ and the *_r23.py scripts). Carried rows name the cited subject that is
byte-identical since the previous pin 6d22ff56."""
import json
import sys
from datetime import datetime, timezone

ROOT = sys.argv[1]
OUT = f"{ROOT}/ledgers/LX1/LX1-b.json"
R21 = json.load(open("/Users/billyribeiro/.fanout/frags/E-LX1-b.round21.json", encoding="utf-8"))
old = {r["id"]: r for r in R21["rows"]}
S = "ledgers/LX1/scripts/LX1-b-r23/out/"
CAR = "Carried from round 21 ({subj} byte-identical since the previous pin 6d22ff56): "

RE = {}  # id -> (status, location or None, evidence)
def rerun(i, ev, loc=None):
    RE[i] = ("PASS", loc, ev)
def carry(i, subj, loc=None):
    RE[i] = ("PASS", loc, CAR.format(subj=subj) + old[i]["evidence"])
def reverify(i, ev, loc=None, status="PASS"):
    RE[i] = (status, loc, ev)

# ---- gates re-run on the pin dde0486b
rerun("lx1b-check-pages", f"tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS', exit 0 ({S}check_pages.out)")
rerun("lx1b-check-dag", f"tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS', exit 0 ({S}check_dag.out)")
rerun("lx1b-check-projects", f"tools/check_projects.py --unit LX1 -> 'check_projects LX1: PASS', exit 0 ({S}check_projects.out)")
rerun("lx1b-run-graders", f"tools/run_graders.py --unit LX1 -> 'no autograder (grading: rubric)', exit 0 ({S}run_graders.out)")
rerun("lx1b-run-labs", f"tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)', exit 0 ({S}run_labs.out)")
for L in ("L01", "L03", "L04"):
    rerun(f"lx1b-twin-alone-{L}", f"cd /tmp/lx1b-r23-{L} && python -I -W error tests/labs/LX1/lab-LX1-{L}-1.py -> exit 0, empty stderr ({S}twin_{L}.out, twin_{L}.err)")
    rerun(f"lx1b-page-smoke-{L}", f"tools/page_smoke.py --unit LX1 --pages modules/LX/LX1/{L}.html -> 'page_smoke LX1: PASS', exit 0 ({S}page_smoke_{L}.out)")
rerun("lx1b-twin-equals-page-code", f"own script ledgers/LX1/scripts/LX1-b-r23/twin_page_compare_r23.py: page code block == twin file (trailing newline aside) for L01, L03, L04; expected block == twin stdout for L01, L03, L04; 'ALL True' ({S}twin_page_compare_r23.out)")
rerun("lx1b-ruff-mypy", f"ruff check tests/labs/LX1 -> 'All checks passed!'; ruff format --check -> '7 files already formatted'; mypy --no-incremental on the three LX1 twins -> 'Success: no issues found in 3 source files' ({S}ruff_check.out, ruff_format.out, mypy.out)")
rerun("lx1b-pytest", f"python -m pytest tests/test_labs.py -q -k LX1 -> 7 passed, exit 0 ({S}pytest_labs_LX1.out)")
rerun("lx1b-verify-refs", f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}verify_refs_offline.out). The live run was not repeated this round: references/references.json and tools/verify_refs.py are byte-identical since 6d22ff56")
rerun("lx1b-fetch-check", f"tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems', exit 0 ({S}fetch_check.out)")
rerun("lx1b-r20-licence-page-curl", f"plain curl https://www.federalreserve.gov/disclaimer.htm -> HTTP 200 (ledgers/LX1/scripts/LX1-b-r23/out/fed_disclaimer_r23.html, 47503 chars); the page reads 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.', the same words as MANIFEST fx_monthly licence")
rerun("lx1b-structure", f"check_pages LX1 PASS and page_smoke PASS for L01, L03, L04 (re-run); section and template structure of the three pages read through the delta ({S}check_pages.out)")
rerun("lx1b-r20-dfn-anchors", f"check_dag and check_pages re-run PASS; no <dfn> was added or removed in the delta (the only dfn lines in changed hunks, L04:59, are unchanged in form)")
rerun("lx1b-cards-l01-l03-l04", "cards.json re-counted per lesson: L01 17, L03 32, L04 24 (73 cards; 90 total, unchanged). Card records compared with 6d22ff56: only LX1-c070 differs")
rerun("lx1b-mutants-none", "run_graders LX1 -> 'no autograder (grading: rubric)'. LX1 is rubric-graded, so no grader mutants exist; twins are demonstrations (rulings). Re-read the delta: no grader or twin mutant applies in slice b. project.html is slice a, not read here")
rerun("lx1b-banned-phrases", f"own scan ledgers/LX1/scripts/LX1-b-r23/prose_scan_r23.py over L01/L03/L04 and their cards: BUILDER_RULES 1.3-1.4 phrases. Only 2 hits, both '...' in list notation 'for t = 0, 1, ..., H' (L03:162) and 'f_0, ..., f_H' (L03:254 docstring), not omitted content ({S}prose_scan_r23.out)")
rerun("lx1b-process-words", f"own scan (prose_scan_r23.py): no builder, verifier, round, ledger, ruling or fix talk in learner text. The 31 hits are the symbol delta and the word 'round' in rounding sense ({S}prose_scan_r23.out)")
rerun("lx1b-r20-scope-words-readthrough", f"own scope-word scan (prose_scan_r23.py) over the three pages and cards; the sentences added by the delta, L01:445, L04:59, :110, :122-123, :326, :333, :448 and cards LX1-c070, add no claim with a scope word that lacks an evidence line: 'exchange-rate columns only' is shown by the CSV header AUD..SEK (fx_monthly.csv line 1) and the MANIFEST columns list")
rerun("lx1b-scope-words", f"own scope-word scan (prose_scan_r23.py): 241 hits, all in lines that predate the delta or are evidenced; the delta adds none without evidence ({S}prose_scan_r23.out)")

# ---- re-verified (subject changed)
reverify("lx1b-quiz-explanations", "L01.html:439-445 (quiz 6): prompt lists d_1 > 0, 1 + g > 0, r > -1, g >= r. Explanation now reads 'Since g >= r and r > -1, q = (1 + g)/(1 + r) >= 1, so each discounted term d_1 q^{k-1}/(1 + r) is at least d_1/(1 + r) > 0, and the partial sums tend to +infinity (Proposition 1.4).' Check: 1 + g >= 1 + r > 0 gives q >= 1; q^{k-1} >= 1 for k >= 1; d_1 > 0 (prompt); so each term >= d_1/(1+r) > 0 and S_N >= N d_1/(1+r) -> infinity (Proposition 1.4 proof, L01:96). Re-derived with Fraction in quiz_numbers_r23.py (g=9%, g=10%, q >= 1, term bound True). Other quiz explanations read in full this round: L01:405-483 (F0 6666.67 -> 6667 ; F2 7072.67 -> 7073 ; q = 103/109 = 0.944954 ; g* = 0.023333 ; witness 5000 / 20000/3 and gaps +1000, -2000/3 ; L01:463 ; L01:472 (A0), (A1)), L03:552-636 (2.69 %, 3.4260, 1274345.2124 -> 1274345, 8 periods, first maximal t = 12, depths 9.20 / 2.69 ; quiz_numbers_r23.out), and L04:483-567 (A2, zero months 1976-07, 2012-07, 2019-11, 321 changes, s1 0.027935, ln 1.1 = 0.0953101798, bound 0.1358 at h = 0.0678, MANIFEST start 2000-01-03 for fx_daily and ust_daily). Every quoted number matches the own re-derivation ({S}quiz_numbers_r23.out). Ruling 26 kinds: no false statement, missing hypothesis or wrong number remains.", "L01.html:439-445 (quiz 6); L01.html:405-483; L03.html:552-636; L04.html:483-567")
reverify("lx1b-L01-prop14-hypotheses", "L01.html:99, :313, :324, :399, :439 read: each names the hypotheses of Proposition 1.4 (d_1 > 0, 1 + g > 0, r > -1, g >= r) or a subset used in context. :445 (changed line) now names g >= r, r > -1 and d_1 > 0 and the proof step q >= 1 that needs them. The hypotheses are sufficient for the bound at :445 (1 + r > 0 and d_1 > 0 are both used).")
reverify("lx1b-L04-window-two-wording", "L04.html:110 (Section 3 intro), now: 'Window one is the whole file: the changes dated 1971-02 to 2026-09, which start from the first month of the snapshot, 1971-01. Window two is the changes dated 2000-01 to 2026-09; its first change uses the rate of 1999-12, and 2000-01 is the first month in which the other two embedded snapshots have data.' Check: fx_monthly.csv first month 1971-01 (line 2), last 2026-09 (line 670), 669 rows; 1999-12 row at line 349 (GBP 1.6150) and 2000-01 at line 350 (GBP 1.6182); MANIFEST fx_daily and ust_daily first = 2000-01-03 (datasets[0] and [2]). So the first month in which both have data is 2000-01, and the window-two base month is 1999-12. Re-derived with own code: w2 first change 2000-01, n = 321, n1 = 668. The round-21 wording gap is closed. Not a ruling-26 FAIL kind in any case.", "L04.html:110")
reverify("lx1b-dag-outside-closure", "Round-21 basis removed: L04 no longer names 'forward rate' (no 'forward' in L01, L03, L04 or the twins: grep) and no longer names 'p-value' (R1 solution at L04:448 now says 'tail probability' with an inline definition). Own name scan (ledgers/LX1/scripts/LX1-b-r23/dag_name_scan_r23.py) against curriculum/curriculum.json concept names of modules outside the closure {E1, E5, FC1, M1, M2, P0.1}: 4 hits: 'safe asset' (L01:51, E8, generic prose), 'balance sheet' (L03:51, :65, :90, :414, AC1, generic prose), 'independence' (L04:448, M4, generic statistical sense), 'spot rate' (L04:333, FI1 'spot-rate' is the zero-coupon rate; here it is the FX spot rate of the data register note, a different object, LOW). None is linked or defined; the plan's D1-D15 table lists none of them. Under ruling 26 a DAG name use is not a FAIL kind; recorded as LOW in notes.", "L04.html:333, :448; L01.html:51; L03.html:51")
reverify("lx1b-L04-manifest-note", "L04.html:117-123 read (changed lines 122-123). Now: 'The file holds exchange-rate columns only: it has no interest-rate column and no column of exchange rates agreed now for delivery at a later date.' Check: fx_monthly.csv header is month,AUD,CAD,CHF,DKK,EUR,GBP,JPY,NOK,NZD,SEK (all exchange rates, no interest column; MANIFEST columns list identical); MANIFEST fx_monthly retrieved 2026-10-19, rows 669, first 1971-01, last 2026-09, transform inverts CAD, CHF, DKK, JPY, NOK, SEK (verified in MANIFEST.json and read from the file). L04:112 and :114 unchanged.", "L04.html:112-123")
reverify("lx1b-math-L04", "L04.html:57-107 read in full. Changed line :59 (Definition 1.1) now says 'Let x_t > 0 be a rate at each month t; this positivity is Assumption (A1), which Proposition 1.2 uses.' Proposition 1.2 (L04:85-87) states 'Assuming (A1): the rates x_t are positive for every month t from a to b', and its proof uses it at each ratio x_t / x_{t-1}; the sum over a+1..b has b-a terms and telescopes to ln(x_b/x_a) (re-checked: the proof is complete). Definition 2.1, Proposition 2.2 and Remark 1.3 unchanged.", "L04.html:57-107")
reverify("lx1b-math-problems", "L01.html:330-389 and L03.html:431-532 and L04.html:355-470: byte-identical except the R1 solution at L04:448 (inside 355-470). R1 now: 'no tail probability (the probability, under the null distribution, of a result at least as extreme as the one observed) is reported here' and 'A test that reports such a tail probability needs the null distribution derived or cited'. The statement makes no numerical claim and computes no test; the ratio of sample variances is named as a statistic without a null claim. The other problems are carried (L04:355-447, 449-470 unchanged).", "L01.html:330-389; L03.html:431-532; L04.html:355-470")
reverify("lx1b-scope-start", "L04.html:110 (re-checked above: 'first change uses the rate of 1999-12' and 2000-01 as first month of both other snapshots); L04.html:326 (same claim, 321 changes, first change from 1999-12, start 2000-01-03 in both MANIFEST entries); L04.html:387 and :462 unchanged; card LX1-c063 unchanged; lab docstring window-two text (twin lines 14-17) unchanged and consistent with the code (ells keyed by month, window two = months >= 2000-01, base 1999-12 from the CSV).", "L04.html:110, :326, :387, :462; cards LX1-c063; lab docstring")
reverify("lx1b-notation", f"Every symbol in the changed lines was compared token by token with the previous pin (own script, math spans): L04:59, :110, :122-123, :326, :333, :448 add no symbol; L01:445 adds q, g, k and \\ge, all already defined in L01 (Theorem 1.3 defines q = (1+g)/(1+r), Proposition 1.4 uses d_1, r, g). notation/notation.json holds 8 cross-unit symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}}); none is used in LX1 with another meaning in the changed lines.", "L01.html:445; L04.html:59, :110, :122-123, :326, :333, :448")
reverify("lx1b-notation-P", "The changed lines add no P_t or price symbol (token diff above). P_t is the L03 price index only (L03.html:58-59, :116, :157-163, :211, :464-473 unchanged). L01 whole page: no P introduced by the delta.", "L01.html (whole page); L03.html:58-59, :116, :157-163")
reverify("lx1b-notation-registered", "Token diff over changed lines (see lx1b-notation): q, g, k, \\ge at L01:445 are symbols defined earlier in L01; no new symbol in L04. Registry check unchanged in substance.", "L01.html; L03.html; L04.html")
reverify("lx1b-notation-check-math-spans", "Own token diff (math spans in changed lines) against the previous pin, output in the transcript of this round; no unbalanced or unregistered macro introduced in the changed lines (\\ge is standard, \\(...\\) spans well formed; check_pages PASS).", "L01.html; L03.html; L04.html math spans")
reverify("lx1b-r20-L04-lab-replay", f"tests/labs/LX1/lab-LX1-L04-1.py changed only at lines 8-9 (docstring). Re-ran alone under python -I -W error from an empty scratch dir with data/fx_monthly.csv: exit 0, stderr empty; stdout equals the expected block at L04.html:306-322 ({S}twin_L04.out, twin_page_compare_r23.out).")
reverify("lx1b-r20-sampled-cards", "All 73 L01/L03/L04 cards: 72 records byte-identical to 6d22ff56 (only LX1-c070 differs, per JSON comparison of the 90 records). LX1-c070 read in full: front 'Does the embedded fx_monthly.csv hold any interest-rate column, or any column of exchange rates agreed now for delivery at a later date?', back 'No. It holds exchange-rate columns only, so the lab cannot test a relation between interest rates and exchange rates.' Agrees with L04.html:122-123 and the CSV header; no number on the card; no process word.")
reverify("lx1b-cards-c052-c053", "cards.json LX1-c052, c053, c059, c083 records compared with 6d22ff56: byte-identical (only LX1-c070 differs). The lesson lines they cite (L04.html:84-94) are outside every hunk.", "cards.json LX1-c052, c053, c059, c083; L04.html:84-94")
reverify("lx1b-delta-hunks", "git diff 6d22ff56 dde0486b over the slice paths (course/modules/LX/LX1, tests/labs/LX1, plans/LX1-*, plans/FINAL-ARCHITECT-RULINGS.md, plans/KNOWN-ISSUES.md, notation, references, tools, curriculum, course/assets/data, course/concepts.html): changed files L01.html (1 line, :445), L04.html (7 lines: :59, :110, :122-123, :326, :333, :448), cards.json (1 line, :581, LX1-c070), tests/labs/LX1/lab-LX1-L04-1.py (2 lines, :8-9), plans/FINAL-ARCHITECT-RULINGS.md (rulings 27-29 appended; ruling 26 text unchanged), plans/KNOWN-ISSUES.md (new; E3 items only), project.html (slice a, 1 line). Every slice-b hunk read and re-verified in the rows above. Outside the slice: project.html C1 criterion row (slice a, not verified here).", "git diff 6d22ff56 dde0486b (slice b paths)")
reverify("lx1b-delta-r21", "The current delta (6d22ff56..dde0486b) for slice b is read in full (see lx1b-delta-hunks). The round-21 FAIL items are the subject of: lx1b-quiz-explanations (fixed and re-verified), lx1b-dag-outside-closure (name uses removed, re-verified), lx1b-L04-window-two-wording (fixed and re-verified). Ruling 26 added at 6d22ff56; its text is unchanged at dde0486b (plans/FINAL-ARCHITECT-RULINGS.md lines 74-80 identical).", "git diff 6d22ff56 dde0486b; plans/FINAL-ARCHITECT-RULINGS.md:74-80")

rerun("lx1b-num-L01-lab-output", f"course/modules/LX/LX1/L01.html:244-282 expected block == twin stdout (twin_page_compare_r23.py: L01 expected==stdout True; twin re-run exit 0) ({S}twin_page_compare_r23.out)")

# ---- carried (subject byte-identical since 6d22ff56, lines outside every hunk)
carry("lx1b-citations-L01", "course/modules/LX/LX1/L01.html:304, :489 (outside the :445 hunk) and references/references.json", "L01.html:304, :489")
carry("lx1b-citations-L03", "course/modules/LX/LX1/L03.html")
carry("lx1b-citations-L04", "course/modules/LX/LX1/L04.html:569-575 (outside every hunk) and references/references.json")
carry("lx1b-fx-rebuild", "course/assets/data/market/fx_monthly.csv, course/assets/data/market/MANIFEST.json and tools/fetch_data.py")
carry("lx1b-fx-licence", "tools/data_sources.yaml fx_monthly entry and MANIFEST licence_url")
carry("lx1b-fx-guard", "tests/labs/LX1/lab-LX1-L04-1.py load_column and parse_rate (the only twin hunk is the docstring at lines 8-9)")
carry("lx1b-fx-gbp-clean", "course/assets/data/market/fx_monthly.csv")
carry("lx1b-honest-data", "course/modules/LX/LX1/L03.html:76 and L01.html:131-133 (files identical) and L04.html:112-114 (outside every hunk)")
carry("lx1b-L04-simulated-label", "course/modules/LX/LX1/L04.html:113-114 and the twin docstring outside lines 8-9")
carry("lx1b-open-items-missing", "plans/LX1-open-items.md")
carry("lx1b-plan-coverage", "plans/LX1-build-plan.md and plans/FINAL-ARCHITECT-RULINGS.md rulings 14 and 16 (the delta only appends rulings 27-29)")
carry("lx1b-hours", "L01.html:2, :34; L03.html:2, :34; L04.html:2, :34 (outside every hunk) and course/modules/LX/LX1/index.html:31")
carry("lx1b-num-L01-closed-form", "course/modules/LX/LX1/L01.html:132, :87, :282, :396-399, :417-435 (outside the :445 hunk)")
carry("lx1b-num-L01-prose", "course/modules/LX/LX1/L01.html:282, :363, :367, :370-371, :378, :400")
carry("lx1b-num-L01-witness", "course/modules/LX/LX1/L01.html:114, :120, :321, :462")
carry("lx1b-num-L01-s5-example", "course/modules/LX/LX1/L01.html:310, :322, :417-421")
carry("lx1b-num-L03-depth", "course/modules/LX/LX1/L03.html")
carry("lx1b-num-L03-path", "course/modules/LX/LX1/L03.html")
carry("lx1b-num-L03-M-E-Q", "course/modules/LX/LX1/L03.html")
carry("lx1b-num-L04-stats", "course/modules/LX/LX1/L04.html:306-322 expected block (twin stdout unchanged), :323, :476-477")
carry("lx1b-num-L04-display-diff", "course/modules/LX/LX1/L04.html:323 and :476")
carry("lx1b-num-L04-derived", "course/modules/LX/LX1/L04.html:354, :373, :380, :387, :430, :455, :541, :564")
carry("lx1b-math-L01", "course/modules/LX/LX1/L01.html:57-99")
carry("lx1b-math-L01-prop22", "course/modules/LX/LX1/L01.html:104-121")
carry("lx1b-math-L03", "course/modules/LX/LX1/L03.html")
carry("lx1b-grades", "course/modules/LX/LX1/L01.html:397-401, L03.html:542-546, L04.html:474-477 (outside every hunk)")
carry("lx1b-notation-A", "course/modules/LX/LX1/L01.html:105, :114, :119-120, :143-144, :377, :450 and cards LX1-c006")
carry("lx1b-notation-K", "course/modules/LX/LX1/L03.html and cards LX1-c027, c071, c082")
carry("lx1b-notation-P-L03", "course/modules/LX/LX1/L03.html")
carry("lx1b-notation-N", "course/modules/LX/LX1/L01.html:67, :74, :82-83, :87 (outside every hunk)")
carry("lx1b-dag-links", "course/modules/LX/LX1/L01.html:37, L03.html (identical), L04.html:37, :105, :336")
carry("lx1b-concepts-defs", "course/modules/LX/LX1/L01.html:105, :290; L03.html:87, :390; L04.html:86")
carry("lx1b-concept-index-title", "course/concepts.html:631-636")
carry("lx1b-L04-bretton-definition", "course/modules/LX/LX1/L04.html:38, :86, :337, :358, :553-557")
carry("lx1b-L03-remark42-solvency", "course/modules/LX/LX1/L03.html")
carry("lx1b-L03-ratio-claims", "course/modules/LX/LX1/L03.html")
carry("lx1b-L03-r1-no-result", "course/modules/LX/LX1/L03.html")
carry("lx1b-L03-lab-checks-overreach", "course/modules/LX/LX1/L03.html and tests/labs/LX1/lab-LX1-L03-1.py")
carry("lx1b-L03-misconception-scope", "course/modules/LX/LX1/L03.html")
carry("lx1b-cards-L01-hypotheses", "cards.json LX1-c002..c007, c013, c085, c086, c092, c093")
carry("lx1b-cards-L03-hypotheses", "cards.json LX1-c030..c036, c079, c082, c087")
carry("lx1b-cards-c092-hypothesis", "cards.json LX1-c092")
carry("lx1b-L01-misc3-closed-form", "course/modules/LX/LX1/L01.html:324 and card LX1-c092")
carry("lx1b-L01-benchmark-finite-hypothesis", "course/modules/LX/LX1/L01.html:99")
carry("lx1b-r20-L03-independent-derivation", "course/modules/LX/LX1/L03.html Lemma 3.1, Prop 3.2, Cor 3.3-3.4 (file identical); re-derived this round in quiz_numbers_r23.py")
carry("lx1b-r20-L04-R2-band", "course/modules/LX/LX1/L04.html:452-455 and quiz 541-564 (outside every hunk)")
carry("lx1b-r20-L04-proof-P2-P3", "course/modules/LX/LX1/L04.html:393-418 (outside every hunk)")
carry("lx1b-r20-L03-M-proof-P1-P3", "course/modules/LX/LX1/L03.html:431-520 (file identical)")
carry("lx1b-r20-fail-loud-L04", "tests/labs/LX1/lab-LX1-L04-1.py load_column (outside the docstring hunk)")
carry("lx1b-r20-L01-lab-replay", "tests/labs/LX1/lab-LX1-L01-1.py (byte-identical)")

ids21 = [r["id"] for r in R21["rows"]]
assert set(ids21) == set(RE), (set(ids21) ^ set(RE))
rows = []
for r in R21["rows"]:
    st, loc, ev = RE[r["id"]]
    row = {"id": r["id"], "check": r["check"], "location": loc or r["location"], "status": st, "evidence": ev}
    rows.append(row)

frag = {
    "unit": "LX1",
    "slice": "b",
    "round": 23,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b (L01, L03, L04, lab twins, LX1 cards), round 23 (delta verification, ruling 26)",
    "pin": "dde0486b (E3: ties, estimator range, notation and rubric calibration fixes), detached; .venv symlinked; vendor present",
    "base": "6d22ff56 (round 21 pin; base fragment ~/.fanout/frags/E-LX1-b.round21.json, verdict FAIL with 3 non-PASS rows)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE23-LX1-b",
    "scratch": "/tmp/lx1b-r23-L01, /tmp/lx1b-r23-L03, /tmp/lx1b-r23-L04 (created per twin run and removed)",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": R21["registry_flags"],
    "freshness_flags": [],
    "notes": [
        "Round 23 delta: git diff 6d22ff56..dde0486b over the slice paths. Changed slice-b subjects: L01.html:445 (quiz 6 explanation); L04.html:59, :110, :122-123, :326, :333, :448; cards.json LX1-c070 (line 581); tests/labs/LX1/lab-LX1-L04-1.py docstring lines 8-9. Everything else in the slice is byte-identical to 6d22ff56 and its rows are carried with the prefix.",
        "The base fragment named for this round, ~/.fanout/frags/E-LX1-b.round22.json, does not exist. The base used is round 21 (6d22ff56), as the task states.",
        "Ruling 26 (FAIL kinds only) applied. Round-21 row lx1b-quiz-explanations (missing hypothesis in a proof-bearing explanation) is a ruling-26 kind and is fixed and re-verified. Round-21 row lx1b-dag-outside-closure (a DAG name use) and lx1b-L04-window-two-wording (wording, LOW) are not ruling-26 kinds; both were resolved in the delta and are re-verified as PASS.",
        "LOW, not a ruling-26 kind, recorded for the builder (not a FAIL): L04.html:333 uses the words 'spot rate' for the FX spot rate of the data register note. The concept spot-rate (FI1, curriculum.json) is the zero-coupon rate, a different object. A wording change (for example 'FX spot rate') would remove the collision. Not in KNOWN-ISSUES.md; the verifier does not edit plans.",
        "LOW, not a ruling-26 kind: L04.html:59 labels the positivity of Definition 1.1 as Assumption (A1), a label first stated in Proposition 1.2 (L04.html:85). The definition states the positivity itself, so no claim is unsupported. Forward label only.",
        "Re-derivations this round are in ledgers/LX1/scripts/LX1-b-r23/quiz_numbers_r23.py (own Fraction and Decimal code; no lab imports) with output in out/quiz_numbers_r23.out. Page code and expected blocks compared with the twins by twin_page_compare_r23.py.",
        "Gates run on the pin dde0486b, each with its exit code in out/: check_pages, check_dag, check_projects, run_graders (rubric), run_labs (7/7), page_smoke for L01, L03, L04, the three twins alone under python -I -W error, ruff check and format, mypy --no-incremental on the twins, pytest tests/test_labs.py -k LX1 (7 passed), verify_refs --offline, fetch_data --check. Plain curl of the Federal Reserve disclaimer returned HTTP 200 and the licence sentence.",
        "Out of slice: plans/FINAL-ARCHITECT-RULINGS.md rulings 27-29 and plans/KNOWN-ISSUES.md (E3 items) and course/modules/LX/LX1/project.html (slice a, C1 criterion row) changed in the delta. Not verified by this slice; the project row is slice a's.",
        "registry_flags are carried from round 21 unchanged (registry files byte-identical since 6d22ff56; not re-resolved this round).",
        "Not repeated: verify_refs --live (references and verifier byte-identical since 6d22ff56); the builder's own gates beyond those listed; the full ruff and mypy workspace runs (twins and LX1 files only).",
    ],
    "summary": "",
}
pass_n = sum(1 for r in rows if r["status"] == "PASS")
frag["summary"] = (
    f"LX1-b round 23 (delta verification, pin dde0486b, base 6d22ff56): verdict PASS. Rows: {len(rows)} (pass={pass_n} fail=0 unverifiable=0). "
    "The three round-21 non-PASS rows are re-verified: lx1b-quiz-explanations (L01:445 now gives the q >= 1 step), lx1b-L04-window-two-wording (L04:110 now states 1999-12 base and 2000-01 first common month) and lx1b-dag-outside-closure (forward rate and p-value names removed). "
    "Every changed slice-b subject was re-read; the rest carried with byte-identity prefixes. Mutants: none (rubric unit)."
)
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", OUT, len(rows), "rows", pass_n, "PASS")
