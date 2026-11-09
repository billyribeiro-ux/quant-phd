# CS2-c round 6 (delta verification) fragment builder. Carries round-5 rows only where the cited subject is byte-identical.
import json, subprocess
from datetime import datetime, timezone

ROOT = '/Users/billyribeiro/.fanout/wt/verifyS6-CS2-c'
PREV = json.load(open('/Users/billyribeiro/.fanout/frags/S-CS2-c.round5.json'))
R5 = {r['id']: r for r in PREV['rows']}
PIN = subprocess.check_output(['git', '-C', ROOT, 'rev-parse', 'HEAD'], text=True).strip()
S = 'ledgers/CS2/scripts/CS2-c-r6/'
PFX = 'Carried from round 5 ({f}, byte-identical since the previous pin dde0486b): '
PART = '{t} Carried from round 5 for {f} (byte-identical since dde0486b): '

# id -> (mode, text/files, location-override or None)
# mode: fresh (re-run or re-read this round), carry (whole subject unchanged), partial (changed items fresh, rest carried), fail
M = {}
def fresh(i, text, loc=None): M[i] = ('fresh', text, loc)
def carry(i, files, loc=None): M[i] = ('carry', files, loc)
def partial(i, text, files, loc=None): M[i] = ('partial', (text, files), loc)
def fail(i, text, loc=None): M[i] = ('fail', text, loc)

fresh('C-01', 'Re-run on pin e896b7a4: tools/check_pages.py --unit CS2 -> "check_pages CS2: PASS" (exit 0); --unit CS2 --pages L09 / L10 / L11 -> PASS each; --all -> 27 PASS lines, 0 FAIL, exit 0 (ledgers/CS2/scripts/CS2-c-r6/check_pages_unit.txt, check_pages_L09/L10/L11.txt, check_pages_all.txt).')
fresh('C-02', 'Re-run: tools/check_dag.py --unit CS2 -> "check_dag CS2: PASS"; --all 27 PASS, 0 FAIL (check_dag.txt, check_dag_all.txt); tools/build_site.py --check -> "site data current: 6 outputs", exit 0 (build_site_check.txt). Links unchanged: L09.html:38,65; L10.html:38-39,67; L11.html:38-39,76 (the only changed lines of the slice pages are the ones listed under C-11 to C-14).')
fresh('C-03', 'Re-run: tools/run_labs.py --unit CS2 -> "run_labs CS2: PASS (14/14)", exit 0 (run_labs_unit.txt). That run checks each inline lab (L09.html:119-219, L10.html:118-212, L11.html:142-260) against its twin byte-for-byte and its expected block against the output, under the page rule. The hypothesis and interpretation text changed (rows C-11 to C-14) and is re-read below.')
fresh('C-04', 'Re-run: .venv/bin/python -I -W error tests/labs/CS2/lab-CS2-L09-1.py, lab-CS2-L10-1.py, lab-CS2-L11-1.py -> exit 0 each, stderr 0 bytes (twin_L09.out, twin_L10.out, twin_L11.out, *.err). The three twins are byte-identical to dde0486b (git diff --quiet).')
fresh('C-05', 'Re-run: tools/page_smoke.py --unit CS2 --pages L09 / L10 / L11 each alone -> "page_smoke CS2: PASS", exit 0 (page_smoke_L09.txt, page_smoke_L10.txt, page_smoke_L11.txt).')
fresh('C-06', 'Re-run: .venv/bin/ruff check on the three twins -> "All checks passed!" exit 0; ruff format --check -> "3 files already formatted", exit 0 (ruff.txt).')
fresh('C-07', 'Re-run: .venv/bin/mypy --no-incremental -> "Success: no issues found in 385 source files", exit 0 (ledgers/CS2/scripts/CS2-c-r6/mypy.txt).')
fresh('C-08', 'Re-run: pytest tests/test_labs.py -k "CS2 and (L09 or L10 or L11)" -> exit 0 (pytest_labs_cs2_l09_l11.txt); pytest tests/test_docs_figures.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_build_site.py tests/test_curriculum.py -> exit 0 (pytest_misc.txt).')
fresh('C-09', 'Re-run: tools/verify_refs.py --offline -> "offline integrity: 560 entries, 0 problems", exit 0 (verify_refs_offline.txt). The three slice pages cite no registry key: each has an empty <ol data-references></ol> (L09.html:447, L10.html:446, L11.html:496), and the lesson-level sentence "This lesson cites no registry key" is unchanged. references/ is byte-identical since dde0486b.')
fresh('C-10', 'Hours: data-hours L09=10 (L09.html line 2), L10=8 (L10.html line 2), L11=7 (L11.html line 2); eyebrow lines 35 agree. Hub index.html:153-155 shows L09 10 h, L10 8 h, L11 7 h. Sum of lesson hours L01-L08 (8+9+10+10+9+9+10+10 = 75, index.html) plus L09-L11 (25) = 100, which equals the "100 lesson hours" stated at index.html:143. Arithmetic consistent.')
fresh('C-11', 'Re-read this round. L09.html:121 hypothesis: "at offset 0 ... each of the three methods is below 1e-14" (twin_L09.out: 9.258e-16, 2.819e-17, 7.286e-15); "two-pass ... most accurate at each of the three offsets" (2.819e-17 < 9.258e-16 and 7.286e-15; 4.357e-17 < 8.852e-11 and 1.418e-02; 1.269e-14 < 7.449e-08 and 1.000); "naive rises from about 7e-15 to 1" (7.286e-15 -> 1.000e+00); "naive exactly zero at 1e9" (0.000000e+00); "Welford below naive at each offset" (9.258e-16 < 7.286e-15; 8.852e-11 < 1.418e-02; 7.449e-08 < 1.000); reference is an exact Fraction variance (twin exact_variance). Interpretation L09.html:218: 8.604302e-02 at 1e6 and 0.000000e+00 at 1e9 printed; header 0.087281 at all offsets; sum of squares 2000 x (1e9)^2 = 2e21 is a calculation from n and the offset; 2^70 <= 2e21 < 2^71 so the spacing is 2^(70-52) = 2^18 = 262144 (math.ulp not needed); half-spacing 131072; (n-1) x 0.087281 = 174.47 ~ 174.5; Welford 9.26e-16 -> 7.45e-8 matches output. No unprinted value remains (grep: no 2.0000000020427, 3.2e6, 0.0872811009, 174.4749, 9.2581 in the three pages).')
fresh('C-12', 'Re-read this round. L10.html:120 hypothesis: twin lab-CS2-L10-1.py:60-76 asserts rolling min/max equal brute force at every position (raise AssertionError) and asserts no deque exceeds the window size (line 76); it does not assert the operation bound (no assert on 2N); N = 200 is the twin N (line 1-9 docstring and series length). Output: 396-399 totals, bound 2N = 400. L10.html:211 interpretation: totals 396-399 below 400 for each of the five windows; largest single-insertion removals equal the window size for windows 1, 2, 5 (output 1, 2, 5) and are 6 for windows 13 and 30 (output: "largest single-push removals 6" for both); largest deque size 10 for window 30 (output).')
fresh('C-13', 'Re-read docstring lines of tests/labs/CS2/lab-CS2-L10-1.py (lines 1-9, 21-26). The twin is byte-identical to dde0486b (git diff --quiet), so the round-5 evidence stands: ' + R5['C-13']['evidence'], None)
M['C-13'] = ('carry', 'tests/labs/CS2/lab-CS2-L10-1.py (whole file)', None)
fresh('C-14', 'Re-read this round. L11.html:144 hypothesis: twin lab-CS2-L11-1.py:99-108 raises AssertionError unless below <= qN + eps N and at_or_below >= qN - eps N, i.e. both inequalities of Definition 1.2 for each probe (both checked); printed "largest excess ... = 0.0212 N" and "0.0442 N" and "largest deficit ... = 0.0000 N" (twin_L11.out). "N = 5000" and "each of nine probe quantiles" match the twin. L11.html:259-260 (expected block and interpretation) unchanged; twin byte-identical.')
M['C-15'] = ('carry', 'course/modules/CS/CS2/L09.html:72-80', None)
M['C-16'] = ('carry', 'course/modules/CS/CS2/L09.html:84-95', None)
M['C-17'] = ('carry', 'course/modules/CS/CS2/L09.html:97-105; course/modules/M/M1/L06.html:60,64', None)
M['C-18'] = ('carry', 'course/modules/CS/CS2/L09.html:107-115; tests/labs/CS2/lab-CS2-L09-1.py:36-39 (twin byte-identical)', None)
partial('C-19', 'E1 (L09.html:308) and E2 (L09.html:315) re-verified this round: E1 mechanism uses 2000 x (1e9)^2 = 2e21, spacing 262144, 1999 x 0.087281 = 174.5 (no unprinted digits); E2 product 9.258e-16 x 0.087281 = 8.08e-17 (calculation from printed values, matches the solution text).', 'course/modules/CS/CS2/L09.html:254-304 and 316-352 (M1-M3, P1-P3, E3, R1-R3)')
M['C-20'] = ('carry', 'course/modules/CS/CS2/L10.html:72-92', None)
M['C-21'] = ('carry', 'course/modules/CS/CS2/L10.html:96-114', None)
M['C-22'] = ('carry', 'course/modules/CS/CS2/L10.html:247-341', None)
M['C-23'] = ('carry', 'course/modules/CS/CS2/L11.html:95-104', None)
M['C-24'] = ('carry', 'course/modules/CS/CS2/L11.html:84-127 (L11 changed lines are 144 and 356 only)', None)
M['C-25'] = ('carry', 'course/modules/CS/CS2/L11.html:129-137', None)
partial('C-26', 'E2 (L11.html:356) re-verified this round: capacities k_h = 2 ceil((h+1)(h+2)/(2 eps)) with eps = 1/20 give 40, 120, 240, 400, 600 (= 20(h+1)(h+2), an integer); floors 125, 20, 5, 1, 0 sum to 151 = printed compactions (twin_L11.out "compactions 151"); the sentence on the count depending only on n and eps is supported by the deterministic buffer rule.', 'course/modules/CS/CS2/L11.html:289-352 and 357-392 (other problems)')
fresh('C-27', 'Re-read this round: L09.html:52 (no number beyond n-values prose; no claim checked against output); 117 (mant_dig 53: sys.float_info.mant_dig = 53 here and CPython float is binary64; pyproject.toml:5 requires-python = ">=3.14", so 3.14 is the minimum the repository requires); 218, 225, 235, 239, 308, 315 (see C-11, C-19, C-28); 309 and 322 (322 labelled as a hypothesis about mechanism, 2000 steps consistent with N = 2000 in the twin); 366 (7.45e-08, matches twin_L09.out). No unrounded value (13-digit exact variance, 2.0000000020427e21, 3.2e6, 174.4749, unrounded relative error) remains on the page.')
fresh('C-28', 'Re-read this round: L09.html:239 misconception 2 ratios from printed relative errors 7.286e-15/9.258e-16 = 7.87 (about 8), 1.418e-02/8.852e-11 = 1.60e8, 1.000/7.449e-08 = 1.34e7 (about 1.3e7); each printed to the stated digits; all inputs are in twin_L09.out.')
fresh('C-29', 'Re-read this round: L10.html:52 (2n bound from Theorem 2.4; w-1 comparisons prose), 61 (w-1 comparisons, two operations per value on average, Corollary 2.5(a)), 120 and 211 (see C-12), 228 (largest single-push removal 5 for window 5 = window size; output), 232 (10 for window 30 < 30; output), 356 (396 to 399 against 400; largest size 10; output), 397 (396 to 399 below 400; output). Quiz L10.html:375-397: "2n - 1 = 19" for a strictly decreasing series (10 appends, 9 removals, any window, each entry removed at most once) checked by hand; "window at 4 is {2,3,4}, with values 4,1,5" (series 3,1,4,1,5, w = 3) matches; "2n = 400" for n = 200 matches Theorem 2.4.')
fresh('C-30', 'Re-read this round: L11.html:52, 137, 259, 265-267, 276, 280, 299, 313, 349, 354, 364, 390, 406, 442, 447, 477 unchanged; L11.html:356 (E2) re-verified under C-26. Printed values match twin_L11.out (151 compactions, 500 and 220 stored items, 0.0212 N and 0.0442 N, 0.0000 N deficit).')
M['C-31'] = ('carry', 'course/modules/CS/CS2/L09.html:73,85,98,108,362-366 (unchanged lines)', None)
M['C-32'] = ('carry', 'course/modules/CS/CS2/L10.html:73,85,97,107,352-356 (L10 changed lines are 120 and 211 only)', None)
M['C-33'] = ('carry', 'course/modules/CS/CS2/L11.html:85,96,107,118,130,402-406 (L11 changed lines are 144 and 356 only)', None)
M['C-34'] = ('carry', 'course/modules/CS/CS2/L09.html:73', None)
M['C-35'] = ('carry', 'course/modules/CS/CS2/L11.html:96', None)
M['C-36'] = ('carry', 'course/modules/CS/CS2/L09.html:38,60,65,104; L10.html:38,67,94,108; L11.html:38,62-63,76 (none changed)', None)
fresh('C-37', 'Re-run this round against notation/notation.json (8 entries: T, Phi/Phi^-1, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). grep of L09.html, L10.html, L11.html for \\Phi, gamma_3, gamma_4, R_f, R^*, \\mathbb{Q}, and bare T symbol: 0 hits in symbol use (T occurs only as the grade label). The changed text introduces N (L10.html:120 "N = 200", L11.html:144 "N = 5000") and E (L11 Theorem 2.4) and S_n with the same meanings the lesson already gives (number of values; compaction error total; sum of squared deviations). No registry symbol is reused with another meaning. Note (observation, not a row fail): L09 uses n = 2000 and L10/L11 use N for the number of values.')
partial('C-38', 'Changed lines contain no citation. Unchanged cross-unit citations re-read: L09.html:104 and L10.html:79 unchanged; M1/L06.html:60,64 unchanged (course/modules/M/M1 byte-identical).', 'course/modules/CS/CS2/L09.html:104; L10.html:79')
partial('C-39', 'Process-word grep on L09.html, L10.html, L11.html and the L09-L11 card text (verifier, fixer, round, ruling, builder, TODO, TBD): 0 hits. Changed lines re-read: no unfinished text; terms used before definition checked for the new text (relative error defined in L09.html:121 and 218; Fraction reference defined in twin docstring; doubles introduced at L09.html:117).', 'course/modules/CS/CS2/L09.html, L10.html, L11.html; cards.json (L09-L11)')
partial('C-40', 'Scope words on the changed lines re-read: "every position" (L10.html:120) is backed by the twin loop over all 200 positions; "the bounds are the same for every stream" and "the count 151 depends only on n and eps" (L11.html:356, E2) are backed by the deterministic buffer rule (compaction at k_h items; pushes into each level depend only on n); "any method is stable" (L09.html:218) is a disclaimer, not a claim. Other scope sentences carried from round 5.', 'course/modules/CS/CS2/L09.html:52-238 (unchanged lines), L10.html:61-231, L11.html:52-275')
M['C-41'] = ('carry', 'course/modules/CS/CS2/L09.html section order and counts (no section, count or quiz added or removed in the delta: changed lines are sentences inside existing sections)', None)
M['C-42'] = ('carry', 'course/modules/CS/CS2/L10.html section order and counts (delta changed lines 120 and 211 only)', None)
M['C-43'] = ('carry', 'course/modules/CS/CS2/L11.html section order and counts (delta changed lines 144 and 356 only)', None)
M['C-44'] = ('carry', 'cards.json entry CS2-c116 (entry unchanged)', 'course/modules/CS/CS2/cards.json:785 (CS2-c116)')
M['C-45'] = ('carry', 'cards.json entry CS2-c126 (entry unchanged)', 'course/modules/CS/CS2/cards.json:842 (CS2-c126)')
M['C-46'] = ('carry', 'cards.json entry CS2-c135 (entry unchanged)', 'course/modules/CS/CS2/cards.json:905 (CS2-c135)')
fresh('C-47', 'Sample card CS2-c200 (changed this delta): front "How does the largest excess ... compare with epsilon", back "0.0212 N at epsilon 1/20 and 0.0442 N at epsilon 1/10, each below its epsilon. Theorem 2.5 bounds the excess by E <= epsilon n". Both numbers are printed in twin_L11.out; Theorem 2.5 in L11.html:84-127 reads R^-(v) <= qn + E <= qn + eps n, so the excess over qn is at most E <= eps n. Correct. Triviality is judged under C-63.', 'course/modules/CS/CS2/cards.json:1218 (CS2-c200)')
M['C-48'] = ('carry', 'cards.json entry CS2-c205 (entry unchanged)', 'course/modules/CS/CS2/cards.json:1226 (CS2-c205)')
fresh('C-49', 'Card CS2-c207 (round-2 hypothesis check) was deleted in e896b7a4 as the duplicate of CS2-c148 (C-53). Confirmed absent: cards_scan_r6.out "absent CS2-c207 True". Nothing left to check; the restatement is removed.', 'course/modules/CS/CS2/cards.json (CS2-c207 absent)')
M['C-50'] = ('carry', 'cards.json entries CS2-c151, CS2-c235, CS2-c217 (entries unchanged)', 'course/modules/CS/CS2/cards.json:1010 (c151), 1356 (c235), 1304 (c217)')
M['C-51'] = ('carry', 'cards.json entry CS2-c138 (entry unchanged)', 'course/modules/CS/CS2/cards.json:919 (CS2-c138)')
M['C-52'] = ('carry', 'cards.json: CS2-c225 absent (state unchanged since round 5)', 'course/modules/CS/CS2/cards.json (CS2-c225 absent)')
fresh('C-53', 'Re-run whole-deck scan on e896b7a4 (ledgers/CS2/scripts/CS2-c-r6/cards_scan_r6.py -> cards_scan_r6.out): 197 cards, 197 unique ids; difflib pairs (ratio > 0.55 or front > 0.7) = 34 across the deck; pairs involving a L09-L11 card: only (CS2-c143, CS2-c226) and (CS2-c146, CS2-c149), which ask different facts (what compaction does vs what add does; compactions at level h vs items stored). CS2-c148 and CS2-c207 no longer both present (c207 deleted). No duplicate remains in the slice.', 'course/modules/CS/CS2/cards.json (L09-L11 cards)')
fresh('C-54', 'Scan of every number in the back of the 47 L09-L11 cards against the text of its lesson page (cards_scan_r6.py): no number missing from its lesson. Changed cards CS2-c125, c194, c200, c231, c234 use values printed in twin_L09.out / twin_L10.out / twin_L11.out and the lesson text.', 'course/modules/CS/CS2/cards.json (L09-L11 cards)')
fresh('C-55', 'Changed cards re-checked against the CURRENT lesson text: c125 (L09.html:218, 235: "prints 0.000000e+00 for ... 0.087281" matches), c194 (L09.html:226 and 366: 7.45e-08 and 1.27e-14 match), c200 (L11 Theorem 2.5 and twin_L11.out: 0.0212, 0.0442 match), c231 (L10.html:356, 397: 396-399 and 2n = 400 match; Theorem 2.4 is "at most 2n"), c234 (L10.html:232: largest size 10 for window 30 matches; Theorem 2.2 statement matches). Unchanged cards carried; no card contradicts its lesson. Key-result grades C on L09.html:366, L10.html:356, L11.html:402-406 match the card grades C.', 'course/modules/CS/CS2/cards.json (L09-L11 cards); L09.html:218, 226, 366; L10.html:232, 356, 397; L11.html:84-127')
M['C-56'] = ('carry', 'course/modules/CS/CS2/L09.html:52,452-453; L10.html:52,451-452; L11.html:52,500-502; index.html:153-155 (unchanged)', None)
M['C-57'] = ('carry', 'cards.json entry CS2-c236 (entry unchanged)', 'course/modules/CS/CS2/cards.json:1363 (CS2-c236)')
M['C-58'] = ('carry', 'course/modules/CS/CS2/L11.html:267, 335-338 (unchanged)', None)
M['C-59'] = ('carry', 'cards.json: CS2-c195 absent (state unchanged)', None)
M['C-60'] = ('carry', 'cards.json: CS2-c199 absent (state unchanged)', None)
M['C-61'] = ('carry', 'course/modules/CS/CS2/L11.html:65 (unchanged)', None)
M['C-62'] = ('carry', 'course/modules/CS/CS2/L11.html:140 (unchanged)', None)
fail('C-63', 'Trivia (BUILDER_RULES 8, "Do not make cards of trivia"). Re-verified from scratch over all 47 L09-L11 cards. Removed or fixed since round 5: CS2-c124 deleted; CS2-c231 and CS2-c234 rewritten so the answer is a mechanism (Theorem 2.4 bound; Theorem 2.2 candidate set) with the printed value as support: PASS. CS2-c198 (store far fewer items): answer gives the buffer-capacity mechanism (k_h - 1 per level, Corollary 2.6): PASS. Still a single printed reading of Lab 1 with no mechanism as the answer: CS2-c194 (front asks for the offset-1e9 Welford and two-pass relative errors; answer is 7.449e-08 and 1.269e-14; the added Section 3 caveat is not the answer) and CS2-c200 (front asks how the printed excess compares with epsilon; answer is 0.0212 N and 0.0442 N, and the Theorem 2.5 sentence only confirms them). Each value is correct (C-47, C-27); only the card style fails. LOW.', 'course/modules/CS/CS2/cards.json:1202 (CS2-c194), 1218 (CS2-c200)')
partial('C-64', 'No project grader in this slice (mutation testing applies to project graders only). Twins tests/labs/CS2/lab-CS2-L09-1.py, L10, L11 are byte-identical to dde0486b, so the round-5 statement stands.', 'tests/labs/CS2/lab-CS2-L09-1.py, lab-CS2-L10-1.py, lab-CS2-L11-1.py')
fresh('C-65', 'Re-read this round: CS2-c150 (cards.json:1003) capacities for eps = 1/20: 40, 120, 240 and for eps = 1/10: 20, 60, 120 from k_h = 2 ceil((h+1)(h+2)/(2 eps)): h=0: 2 ceil(20)=40 and 2 ceil(10)=20; h=1: 2 ceil(60)=120 and 2 ceil(30)=60; h=2: 2 ceil(120)=240 and 2 ceil(60)=120. Recomputed in Python. Grade T: a computation from Definition 2.1 (the epsilon = 1/10 values are worked in Problem M1). L11.html:356 (E2) gives k_h = 20(h+1)(h+2) for eps = 1/20, consistent. Verified.', 'course/modules/CS/CS2/cards.json:1003 (CS2-c150); L11.html:75, 299, 356')
M['C-66'] = ('carry', 'cards.json:1010 (CS2-c151) entry and L11.html:52, 131, 137 (unchanged)', None)
M['C-67'] = ('carry', 'cards.json entry CS2-c135 (entry unchanged)', 'course/modules/CS/CS2/cards.json:905 (CS2-c135)')
M['C-68'] = ('carry', 'cards.json: CS2-c225 absent; CS2-c118 entry unchanged', 'course/modules/CS/CS2/cards.json:799 (CS2-c118); CS2-c225 absent')
fresh('C-69', 'Re-read L09.html:218 (interpretation): "SIMULATED data, not market data" present; no data-files on L09-L11 pages (grep); twin docstrings state SIMULATED (lab-CS2-L09-1.py:1-12; L10 and L11 twins unchanged).')
partial('C-70', 'L09 canon-break bullets re-read this round: bullet 1 (Welford relative error 7.45e-8 at offset 1e9 against 1.27e-14 two-pass: matches twin_L09.out), bullet 2 (S_n = (n-1)s^2 about 1999 x 0.087281 about 174.5 against doubles spaced 262144 apart: matches), bullet 3 (n = 1 error: Definition 1.1 requires n >= 2 for the sample variance).', 'course/modules/CS/CS2/L10.html:217-219; L11.html:265-267')
partial('C-71', 'L09 misconceptions 1 and 2 re-read (L09.html:235, 239): checked under C-28 and C-11.', 'course/modules/CS/CS2/L09.html:233-244 (misconception 3 and the others); L10.html:226-236; L11.html:274-285')
partial('C-72', 'L09.html:218 and L10.html:211 interpretation sentences re-read this round against twin output: no overreach (they state the lab shows one stream and one seed; they do not claim stability or tightness).', 'course/modules/CS/CS2/L11.html:259')
M['C-73'] = ('carry', 'course/modules/CS/CS2/L09.html:372-442; L10.html:362-440; L11.html:412-491 (unchanged lines)', None)
fresh('C-74', 'Re-verified: the unprinted values were removed. grep of L09.html, L10.html, L11.html for 2.0000000020427, 3.2 x 10^6, 0.08728110 / 0.0872811009, 174.4749, 9.25811, 8.080587e-17 and 0.0872811 (7 significant digits): no hits. Remaining numbers are printed in twin_L09.out (0.087281, 9.258e-16, 7.286e-15, 1.418e-02, 8.852e-11, 7.449e-08, 1.269e-14, 1.000e+00, 0.000000e+00, 8.604302e-02) or are calculations from printed values (2000 x (1e9)^2 = 2e21; 2^18 = 262144; 1999 x 0.087281 = 174.5; 9.258e-16 x 0.087281 = 8.08e-17; the three ratios 7.87, 1.60e8, 1.34e7). Verified against L09.html:218, 225, 235, 239, 308, 315.')

rows = []
for rid in [f'C-{i:02d}' for i in range(1, 75)]:
    mode, payload, loc_override = M[rid]
    r5 = R5[rid]
    loc = loc_override or r5['location']
    if mode == 'fresh':
        status, ev = 'PASS', payload
    elif mode == 'carry':
        status, ev = 'PASS', PFX.format(f=payload) + r5['evidence']
    elif mode == 'partial':
        text, files = payload
        status, ev = 'PASS', PART.format(t=text, f=files) + r5['evidence']
    elif mode == 'fail':
        status, ev = 'FAIL', payload
    rows.append({'id': rid, 'check': r5['check'], 'location': loc, 'status': status, 'evidence': ev})
    if status == 'FAIL':
        rows[-1]['fix'] = ('Rewrite each as a mechanism question or delete it. CS2-c194: ask why the offset-1e9 Welford error is larger than the offset-0 error (L09 Section 3), or delete. '
                           'CS2-c200: ask why the excess is bounded by E <= eps n (Theorem 2.5), or delete. Keep basis and grade C. Round-5 fixes to c124, c207, c231, c234 verified.')

fails = [r for r in rows if r['status'] == 'FAIL']
counts = {'PASS': sum(r['status'] == 'PASS' for r in rows), 'FAIL': len(fails)}
verdict = 'PASS' if not fails else 'FAIL'
summary = (f'CS2 slice c, round 6 (delta verification from round-5 pin dde0486b to e896b7a4). 74 rows: PASS {counts["PASS"]}, FAIL {counts["FAIL"]} '
           f'(C-63, LOW: two printed-reading cards, CS2-c194 and CS2-c200). Round-5 FAIL rows: C-53 (duplicate c207) now PASS (c207 deleted, rescan clean); '
           f'C-74 (unprinted numbers in L09 prose) now PASS (rewritten to printed values and calculations). C-63 is FAIL for c194 and c200; c124 was deleted and c231, c234 rewritten to a mechanism. '
           f'Every gate re-run on the pin passes: check_pages, check_dag, check_projects, build_site --check, run_labs CS2 14/14, twins under -I -W error, page_smoke L09/L10/L11, ruff, mypy 385 files, pytest subsets, verify_refs --offline (560, 0). '
           f'No mutants (no project grader in this slice). Verdict FAIL only because of C-63 (LOW); no blocking row (false or unproved statement, missing hypothesis, wrong number, over-grade, failing gate, surviving mutant, unsupported lab statement) was found.')

frag = {
    'unit': 'CS2', 'slice': 'c', 'round': 6,
    'verifier': 'Haiku independent verifier, CS2-c round 6 (delta verification; did not build CS2; no builder context)',
    'pin': PIN,
    'base': 'dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-5 pin; round-5 fragment /Users/billyribeiro/.fanout/frags/S-CS2-c.round5.json, read as context only)',
    'checkout': ROOT + ' (detached at e896b7a4; .venv symlinked; vendor copied)',
    'scratch': S + ' (every script and output that backs a row is kept there)',
    'verified_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00'),
    'verdict': verdict,
    'rows': rows,
    'mutants': [],
    'registry_flags': [],
    'freshness_flags': [
        'ledgers/CS2/scripts/CS2-c-r6/ already contained embed_compare.py, raw_lt.py, recheck_L10_L11_claims.py, recheck_L11_small.py, recheck_numbers.py and strip.py (mtime before this verifier started) that this verifier did not write; no row cites them. Observation for the orchestrator.',
    ],
    'notes': ('Delta from dde0486b to e896b7a4 for the slice: L09.html lines 117, 121, 218, 225, 235, 239, 308, 315; L10.html lines 120, 211; L11.html lines 144, 356; cards.json: CS2-c124 and c207 deleted, c125, c194, c200, c231, c234 changed. '
              'Twins L09-L11, references/, notation/, tools/ and course/modules/M/M1 are byte-identical to dde0486b. Other changes (L04-L08, L06/L07 twins, cards of L04/L06/L08, FINAL-ARCHITECT-RULINGS.md, KNOWN-ISSUES.md) are outside the slice. '
              'Not checked: the live verify_refs run (network; the slice cites no key); render_curriculum.py --check (not in this slice\'s gate list); pytest full suite (subsets only); visual screenshots (page_smoke geometry only; no figures on these pages); lessons L01-L08 and other slices. '
              'Observation (not a row): L09 uses n = 2000 while L10 and L11 use N for the number of values; the notation registry has no entries for these symbols, so there is no clash.'),
    'summary': summary,
}
json.dump(frag, open(ROOT + '/ledgers/CS2/CS2-c.json', 'w'), indent=2, ensure_ascii=False)
print('written', verdict, counts)
