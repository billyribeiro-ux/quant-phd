import json, sys
sys.path.insert(0, 'tools')
import ledger

S = 'ledgers/M2/scripts/M2-d2-r10/'
O = S + 'out/'
C9 = ('Carried from round 9 (course/modules/M/M2/L22.html, L23.html, L24.html and tests/labs/M2/lab-M2-L22-1.py, '
      'lab-M2-L23-1.py, lab-M2-L24-1.py byte-identical since the previous pin 1e272e5a; sha256 in ' + O + 'hash_subjects.txt): ')
CN = ('Carried from round 9 (L22-L24 html and notation/ byte-identical or unchanged since the previous pin 1e272e5a; ' + O + 'hash_subjects.txt): ')
CC = ('Carried from round 9 (the 57 slice cards other than M2-c352 are byte-identical since the previous pin 1e272e5a; ' + O + 'cards_delta.txt): ')

rows = []
def row(id, check, location, evidence, status='PASS'):
    rows.append({'id': id, 'check': check, 'location': location, 'status': status, 'evidence': evidence})

# ---- gates run fresh this round
row('G-check-pages', '2.9 structure: check_pages.py --unit M2 --page L22/L23/L24, --unit M2, --all',
    'course/modules/M/M2/L22.html, L23.html, L24.html',
    f'Fresh: "check_pages M2 L22: PASS", "check_pages M2 L23: PASS", "check_pages M2 L24: PASS", "check_pages M2: PASS", exit 0 each; --all PASS for every unit (exit 0). Evidence {O}check_pages_L22.txt, _L23, _L24, _unit.txt, check_pages_all.txt; command list in {S}run_gates.sh.')
row('G-check-dag', '2.9 DAG: check_dag.py --unit M2 and --all',
    'course/modules/M/M2/L22.html..L24.html',
    f'Fresh: "check_dag M2: PASS" (exit 0); --all: every unit PASS, exit 0. Evidence {O}check_dag_M2.txt, check_dag_all.txt.')
row('G-run-labs', '2.5 labs: run_labs.py --unit M2 --page L22/L23/L24',
    'tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py',
    f'Fresh: "run_labs M2: PASS (1/1)" for each page, exit 0. Evidence {O}run_labs_L22.txt, _L23, _L24.')
row('G-twin-isolated', '2.5 labs: each twin under python -I -W error from an empty temp directory',
    'tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py',
    f'Fresh: L22 exit 0 stderr 0 bytes 9 stdout lines; L23 exit 0 stderr 0 bytes 11 lines; L24 exit 0 stderr 0 bytes 25 lines. Evidence {O}lab_equalities.txt (re-runs each twin in a fresh tempdir) and {O}twins_isolated.txt.')
row('G-page-code-equals-twin', '2.5 labs: embedded code block equals the twin',
    'course/modules/M/M2/L22.html:100-221, L23.html:91-214, L24.html:137-217',
    f'Fresh: {S}lab_equalities.py unescapes each <pre><code class="language-python" data-run> block and compares with the twin (trailing newlines aside): L22 True, L23 True, L24 True. Output {O}lab_equalities.txt.')
row('G-expected-equals-live', '2.5 labs: expected block equals live stdout, exact text',
    'course/modules/M/M2/L22.html:222-230, L23.html:215-225, L24.html:218-242',
    f'Fresh: {S}lab_equalities.py compares the unescaped <pre class="expected"> block with the live stdout of the isolated twin run: exact equality for L22 (9 lines), L23 (11 lines), L24 (25 lines). Output {O}lab_equalities.txt.')
for L in ['L22', 'L23', 'L24']:
    row(f'G-page-smoke-{L}', f'2.9 page_smoke, {L} alone', f'course/modules/M/M2/{L}.html',
        f'Fresh: "page_smoke modules/M/M2/{L}.html: PASS", "page_smoke M2: PASS", exit 0 (Chromium light/dark, 360 px sweep included). Evidence {O}page_smoke_{L}.txt.')
row('G-ruff-mypy-twins', 'tooling: ruff check, ruff format --check, mypy --no-incremental on the three twins',
    'tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py',
    f'Fresh: ruff check "All checks passed!"; ruff format --check "3 files already formatted"; mypy --no-incremental "Success: no issues found in 3 source files". Evidence {O}ruff_check.txt, ruff_format.txt, mypy_twins.txt.')
row('G-pytest-labs-M2', 'tooling: pytest tests/test_labs.py -q -k M2',
    'tests/test_labs.py',
    f'Fresh: 27 dots, 27 passed, exit 0. Evidence {O}pytest_labs_M2.txt.')
row('G-verify-refs-offline', '2.1 citations: verify_refs.py --offline (whole registry)',
    'references/references.json',
    f'Fresh: "offline integrity: 560 entries, 0 problems", exit 0. Evidence {O}verify_refs_offline.txt.')
row('G-verify-refs-live-M2', '2.1 citations: verify_refs.py --unit M2 (live re-resolution, plain network)',
    'references/references.json (keys cited on L22-L24: spivak2008calculus, hubbard2015vector)',
    f'Fresh: "live re-verification of M2: 2 of 560 entries, 0 problems", exit 0. The two keys are the only registry keys the slice names (course/modules/M/M2/L22.html:473 region; same wording in L23 and L24), each with the statement that no locator is confirmed, so no slice claim is attributed to them. Evidence {O}verify_refs_live_M2.txt.')
row('G-cards-dup-scan', '2.7 cards: unit-wide duplicate scan of cards.json',
    'course/modules/M/M2/cards.json',
    f'Fresh: {S}cards_delta.py on 397 cards (395 at the round-9 pin): duplicate ids [], duplicate fronts [], duplicate backs [] (case and whitespace folded). The two added cards M2-c412 (L08) and M2-c413 (L15) are in the scan. Evidence {O}cards_delta.txt.')
row('G-cards-slice-unchanged', '2.7 cards: the 57 slice cards (L22 15, L23 24, L24 18) against the round-9 pin',
    'course/modules/M/M2/cards.json',
    f'Fresh: {S}cards_delta.py: slice cards changed vs the round-9 pin: [M2-c352] only; added in slice: none; removed: none. The other 56 are byte-identical (dict equality per id). M2-c352 is re-verified in CARD-L23 and N-L23-cents-minus15-plus16. Non-slice changes M2-c027 (L03), c047 (L04), c177 (L12), and added c412 (L08), c413 (L15) are outside this slice. Evidence {O}cards_delta.txt.')
row('G-delta-hunks', 'delta check: every hunk in the slice changed since the round-9 pin (1e272e5a..47a36d8c) read and re-verified',
    'course/modules/M/M2/cards.json:2445 (M2-c352); L22.html, L23.html, L24.html and the three twins unchanged',
    f'Fresh: git diff --name-only 1e272e5a 47a36d8c touches no slice html or twin (sha256 SAME, {O}hash_subjects.txt). The only slice hunk is cards.json M2-c352 (old back: "...differs from the second-order expansion by -15 cents (Misconception 1)"; new back: "...Lab 1 prints a nonzero difference ... at a shift of +0.01 (Misconception 1)"), read in full and re-verified in CARD-L23. Other hunks in the slice-adjacent files (M2 project.html, grader/test_project.py, curriculum M3 concept name, glossary/program/concepts generated data) are outside the slice.')
row('N-L23-price-cents', '2.2 numbers: unrounded price, integer price, P\'(y0), P\'\'(y0) and their checks',
    'course/modules/M/M2/L23.html:226, expected block :216-219; cards M2-c341..c343, c382',
    f'Fresh: {S}l23_numbers.py (exact Fractions): unrounded price 108110.89577935502 -> 108110.895779; half-even integer 108111; P\'(y0) = -851466.7395285616 -> -851466.739529; P\'\'(y0) = 8376648.51191949 -> 8376648.511919; float central difference of P\' = -851466.7410810943, difference 0.00155 -> 1.6e-03 cents per unit yield. The lab\'s P\'\' central difference 8376650.409250 (difference 1.9) is the lab\'s printed value, matched exactly by lab_equalities.py, not independently recomputed. Output {O}l23_numbers.txt.')
row('N-L23-ratios-and-shifts', '2.2 numbers: first- and second-order errors at 0.01, 0.005, 0.0025; ratios 3.9279/7.8807 and 3.9634/7.9396',
    'course/modules/M/M2/L23.html:51, :226, :281; cards M2-c345, c346, c384, c385',
    f'Fresh: {O}l23_numbers.txt: first-order errors 403.77162, 102.79701, 25.93632 (printed 4.037716e+02, 1.027970e+02, 2.593632e+01); second-order -15.060810, -1.9110996, -0.2407040 (printed -1.506081e+01, -1.911100e+00, -2.407040e-01); error ratios 3.9278538 -> 3.9279, 7.8807039 -> 7.8807, 3.9634380 -> 3.9634, 7.9396267 -> 7.9396. Lesson "approaching 4 and 8" consistent with these values.')
row('N-L23-cents-minus15-plus16', '2.2 numbers: exact minus second-order expansion; whole cents -15 and +16; unrounded -15.06; card M2-c352 re-verified',
    'course/modules/M/M2/L23.html:51, :226, :281, :352-354; expected :224-225; card M2-c352 (cards.json:2445)',
    f'Fresh: {O}l23_numbers.txt: at +0.01 exact 100000.000 cents, second-order 100015.0608, difference -15.0608 (whole cents -15); at -0.01 exact 117060.4057, second-order 117044.3956, difference +16.0100 (whole cents +16). Expected block lines 224-225 match. Card M2-c352 new back ("Lab 1 prints a nonzero difference ... at a shift of +0.01 (Misconception 1)") is true (-15 cents at +0.01 is printed at L23.html:224) and agrees with the lesson misconception 1 (L23.html:281). It names no number, so no rounding claim is made. Grade C with basis "Lab 1 (SIMULATED bond)" matches the lab-read claim.')
row('N-L23-E3-offset', '2.2 numbers: float 0.04+0.01 vs 1/20; offset 2.78e-18; P\'(0.05); price move -2.1e-12',
    'course/modules/M/M2/L23.html:368 (E3 solution)',
    f'Fresh: {O}l23_numbers.txt: 0.04+0.01 == 0.05 True; float(F(0.04+0.01) - 1/20) = 2.7755575615628915e-18 -> 2.78e-18; P(float 0.05) - P(1/20) = -2.1432e-12 cents -> -2.1e-12.')
row('N-L23-previews', '2.2 numbers: preview -P\'/P = 7.875864 and P\'\'/P = 77.482001 (printed only)',
    'course/modules/M/M2/L23.html:90 (hypothesis), :226',
    f'Fresh: {O}l23_numbers.txt: -P\'/P = 7.875864253926185 -> 7.875864; P\'\'/P = 77.4820007875571 -> 77.482001. Expected block line 219 prints the same digits.')
row('N-L23-two-cash-flows', '2.2 numbers: quiz explanation P\'(0.04) = -1777.07 for c1 = -1, c2 = 1000',
    'course/modules/M/M2/L23.html:481 (quiz explanation)',
    f'Fresh: {O}l23_numbers.txt: P\'(0.04) = -1777.068161128812 -> -1777.07; negative as stated.')
row('N-L23-M1-M3', '2.2 numbers: M1 price 50/1.05 + 1050/1.05^2 = 1000.000; M3 zero-coupon derivative formula',
    'course/modules/M/M2/L23.html:304 (M1 solution), :318 (M3 solution), quiz :463',
    CN + 'the M3 formula is carried; the M1 price is re-derived this round: ' + O + 'l23_numbers.txt gives 1000.0.')
row('N-L24-remark44-numbers', '2.2 numbers: exact forward error +1.359e-8 at h=1e-8; computed (signed) error -6.603e-9; printed magnitude 6.603e-9',
    'course/modules/M/M2/L24.html:129 (Remark 4.4), :243; card M2-c365 (cards.json:2564)',
    f'Fresh: {O}l24_numbers.txt: exact forward error e*((e^h-1)/h - 1) at h=1e-8 = 1.3591e-08 -> +1.359e-8; signed float forward quotient error at h=1e-8 = -6.6028e-09 -> -6.603e-9. The lab twin prints abs(...) (tests/labs/M2/lab-M2-L24-1.py lines 70-72), and the lesson says so (L24.html:129, :243). Printed value 6.603e-09 at k=8 (expected block).')
row('N-L24-E3-unrounded', '2.2 numbers (rule 1): unrounded central quotient errors 5.858691e-11 (1e-5) and 5.858736e-11 (1e-7)',
    'course/modules/M/M2/L24.html:348 (E3 solution)',
    f'Fresh: {O}l24_numbers.txt: float central-quotient errors 5.858691310e-11 -> 5.858691e-11 (h=1e-5) and 5.858735719e-11 -> 5.858736e-11 (h=1e-7).')
row('N-L24-E3-difference', '2.2 numbers (rule 1): unrounded difference of the two errors 4.4e-16; six-digit values differ by 4.5e-16',
    'course/modules/M/M2/L24.html:348 (E3 solution), :243',
    f'Fresh: {O}l24_numbers.txt: |err(1e-5)-err(1e-7)| unrounded = 4.440892e-16 -> 4.4e-16; 5.858736 - 5.858691 = 4.5e-16 (six-digit values, as the lesson says).')
row('N-L24-E3-exact-and-grid', '2.2 numbers: exact central error e(sinh h/h - 1) at 1e-5, 1e-6, 1e-7; grid spacing 2.2e-16/h; round-off about 1.3e-11',
    'course/modules/M/M2/L24.html:348',
    f'Fresh: {O}l24_numbers.txt: exact central errors 4.5305e-11 (1e-5) -> 4.530e-11, 4.5305e-13 (1e-6) -> 4.530e-13, 4.5305e-15 (1e-7) -> 4.530e-15; ulp(e) = 4.441e-16 so the quotient grid is ulp/(2h) = 2.22e-16/h (2.2e-11 at 1e-5, 2.2e-9 at 1e-7); printed 5.859e-11 minus exact 4.530e-11 = 1.33e-11 -> about 1.3e-11.')
row('N-L24-minimizers', '2.2 numbers: predicted minimizers 2 sqrt(delta/e) = 1.8e-8 and (3 delta/e)^(1/3) = 6.3e-6',
    'course/modules/M/M2/L24.html:136 (hypothesis), :346-348, card M2-c370',
    f'Fresh: {O}l24_numbers.txt: delta = 2^-52 = 2.220e-16; 2 sqrt(delta/e) = 1.808e-08 -> 1.8e-8; (3 delta/e)^(1/3) = 6.258e-06 -> 6.3e-6 (two significant figures).')
row('N-L24-E2-roundoff-bound', '2.2 numbers: round-off bound 2 delta/h = 0.444 at h = 1e-15; printed error 0.390',
    'course/modules/M/M2/L24.html:341 (E2 solution), expected block :240',
    f'Fresh: {O}l24_numbers.txt: 2*delta/1e-15 = 0.444; printed "forward error 3.903e-01" at k=15 (expected block) -> 0.390.')
row('N-L24-half-ulp', '2.2 numbers: delta = 2.22e-16 described as half a unit in the last place of values near e',
    'course/modules/M/M2/L24.html:136',
    f'Fresh: {O}l24_numbers.txt: math.ulp(e) = 4.441e-16, half = 2.220e-16 = delta.')
row('N-L24-decade-ratios', '2.2 numbers: central errors fall x100 per decade to 1e-4; 4.531e-9 / 5.859e-11 = 77',
    'course/modules/M/M2/L24.html:243 (interpretation)',
    f'Fresh: {O}l24_numbers.txt: exact central error ratio 1e-4 to 1e-5 = 100.0000000495; printed ratio 4.531e-9 / 5.859e-11 = 77.33 -> about 77.')
row('N-L24-M3-numbers', '2.2 numbers: M3 forward quotient 12.61, error 0.61, bound 0.63 with M2 = 12.6',
    'course/modules/M/M2/L24.html:298 (M3 solution)',
    f'Fresh: {S}m3_numbers.py: D+_h f(2) = (2.1^3 - 2^3)/0.1 = 12.61; error 0.61; sup|f\'\'| on [2, 2.1] = 12.6; (1/2)(12.6)(0.1) = 0.63; 0.61 <= 0.63. Output {O}m3_numbers.txt.')

# ---- rows carried from round 9 (subject byte-identical)
row('G-links-anchors', '2.9 structure: every internal href and fragment on L22-L24 resolves', 'course/modules/M/M2/L22.html, L23.html, L24.html',
    C9 + 'round-9 evidence stands. This round check_pages (PASS, out/check_pages_L2x.txt) re-ran the page contract on the same bytes.')
row('G-notation', '3.2 notation: every macro against notation/notation.json; no registered symbol reused', 'course/modules/M/M2/L22.html, L23.html, L24.html',
    CN + 'notation/ and notation.json unchanged since the previous pin.')
row('N-L22-xhat-error', '2.2 numbers (rule 1): x-hat printed error, displayed digits vs unrounded values, sqrt(eps), 3.3e-17',
    'course/modules/M/M2/L22.html:231 (interpretation), :279 (misconception 3), :342 (E1)', C9 + 'the printed twin output (run_labs and lab_equalities.py, this round) equals the expected block.')
row('N-L22-partB-5.4e-12', '2.2 numbers: Part B central differences agree with a/2 to within 5.4e-12; naive partial prints 0',
    'course/modules/M/M2/L22.html:231, card M2-c329', C9 + 'live Part B output this round shows error 5.4e-12 at a = 3.0 and naive partial 0.00000000.')
row('N-L22-partA-ln', '2.2 numbers: Part A central differences equal ln a to eight decimals', 'course/modules/M/M2/L22.html:231, card M2-c328',
    C9 + 'live Part A output this round prints V\' central difference equal to ln(a) to eight decimals for a = 1.5, 2, 3, 4.')
row('N-L24-E3-unrounded-dummy', 'placeholder', 'placeholder', 'placeholder', 'PASS')
rows.pop()  # placeholder removed (no such row in round 9)
row('LAB-L22-statements', '2.5 labs: L22 hypothesis, docstring, interpretation and E-problems vs code and output',
    'course/modules/M/M2/L22.html:99, :100-112 (twin docstring), :231', C9 + 'the twin prints the nine lines of the expected block exactly (lab_equalities.py this round).')
row('LAB-L23-statements', '2.5 labs: L23 hypothesis, docstring and interpretation vs code and output',
    'course/modules/M/M2/L23.html:90, :91-107, :226',
    f'Fresh: hypothesis (L23.html:90) "100000 cents at yield 0.05" is the printed "exact price 100000 cents" at shift +0.01 (expected :224); P\'<0 and P\'\'>0 (printed -851466.74, 8376648.51); ratios near 4 and 8 (printed 3.9279..7.9396). Docstring (twin lines 91-107): SIMULATED bond, parts A-C, STEPS 0.01/0.005/0.0025 and two shifts in Part C match the code and output. Halves-to-even rounding matches price_cents. Evidence {O}l23_numbers.txt, {O}lab_equalities.txt.')
row('LAB-L24-statements', '2.5 labs: L24 hypothesis, docstring and interpretation vs code and output',
    'course/modules/M/M2/L24.html:136, :137-149, :243',
    f'Fresh: docstring (twin lines 1-14) and code: Part A prints +1/-1/0 at six steps (expected :219-224); Part B prints abs() errors (twin lines 70-72), decade grid k=1..15, smallest per quotient (lines 73-78), matching "prints only the magnitude" in L24.html:129 and :243. Output {O}lab_equalities.txt, {O}l24_numbers.txt.')
row('LAB-L22-L24-expected', '2.5 labs: run_labs expected blocks and tolerance', 'course/modules/M/M2/L22.html:222, L23.html:215, L24.html:218',
    f'Fresh: run_labs PASS for all three (out/run_labs_L2x.txt); exact equality of expected block and live stdout (out/lab_equalities.txt). The declared data-tolerance 1e-6 is looser than the exact match.')

# grades, math, cards and prose carried from round 9
for id_, chk, loc in [
    ('GR-L22-T', '2.3 grades: Lemma 1.2, Theorem 1.3, Proposition 2.1 and Example 2.3 graded T', 'course/modules/M/M2/L22.html:63, :73, :239, :256, key results :395-398'),
    ('GR-L23-T', '2.3 grades: Propositions 2.1, 2.2, 3.2, 3.3 and Theorem 3.1 graded T', 'course/modules/M/M2/L23.html:67, :79, :232, :242, :252, key results :405-409'),
    ('GR-L24-T', '2.3 grades: Theorem 2.1, Propositions 3.1, 3.2, 4.2, 4.3 graded T', 'course/modules/M/M2/L24.html:60, :74, :84, :106, :116, key results :385-389'),
    ('M-L22-lemma-thm', '2.4 math: Lemma 1.2 and Theorem 1.3 proofs', 'course/modules/M/M2/L22.html:63-83'),
    ('M-L22-remark14', '2.4 math: Remark 1.4 (local (H3) from the implicit-function theorem)', 'course/modules/M/M2/L22.html:88'),
    ('M-L22-example15', '2.4 math: Example 1.5 (logarithmic objective)', 'course/modules/M/M2/L22.html:91-95'),
    ('M-L22-prop21', '2.4 math: Proposition 2.1 (a constraint solved for one variable)', 'course/modules/M/M2/L22.html:240-246'),
    ('M-L22-example22-23', '2.4 math: Example 2.2 (xy on x+y=a) and Example 2.3 (max ax on [0,1])', 'course/modules/M/M2/L22.html:251, :256'),
    ('M-L22-problems', '2.4 math: problem-set solutions M1-M3, P1-P3, E1-E3, R1-R3 (L22)', 'course/modules/M/M2/L22.html:290-386'),
    ('M-L23-prop21-22', '2.4 math: Proposition 2.1 derivatives and sign; Proposition 2.2 (price at face)', 'course/modules/M/M2/L23.html:69-85'),
    ('M-L23-thm31-prop32', '2.4 math: Theorem 3.1 (remainder bound) and Proposition 3.2 (sign of the remainder)', 'course/modules/M/M2/L23.html:233-248'),
    ('M-L23-prop33', '2.4 math: Proposition 3.3 (first-order expansion lies below the price)', 'course/modules/M/M2/L23.html:252-258'),
    ('M-L23-problems', '2.4 math: L23 problem set M1-M3, P1-P3, E1-E3, R1-R3', 'course/modules/M/M2/L23.html:300-395'),
    ('M-L24-thm21-prop31-32', '2.4 math: Theorem 2.1, Propositions 3.1 and 3.2', 'course/modules/M/M2/L24.html:60-93'),
    ('M-L24-prop42-43', '2.4 math: Propositions 4.2 and 4.3 (bound functions and minimizers)', 'course/modules/M/M2/L24.html:107-123'),
    ('M-L24-remark44-assumption', '2.4 math: Remark 4.4 claims about the bound at h* and the error', 'course/modules/M/M2/L24.html:129; card M2-c365'),
    ('M-L24-problems', '2.4 math: L24 problem set M1-M3, P1-P3, E1-E3, R1-R3', 'course/modules/M/M2/L24.html:281-375'),
    ('CARD-L22', '2.7 cards: all 15 L22 cards against the current L22 text', 'course/modules/M/M2/cards.json (lesson L22)'),
    ('CARD-L24', '2.7 cards: all 18 L24 cards against the current L24 text', 'course/modules/M/M2/cards.json (lesson L24), M2-c365 at cards.json:2564'),
    ('REF-cross-lesson', '2.1 attributions: cross-lesson references in L22, L23, L24 resolve to the stated results', 'course/modules/M/M2/L22.html:88, :369, :473; L23.html:488; L24.html:468'),
    ('S-banned-phrases', '2.9 banned phrases (BUILDER_RULES 1.3-1.4)', 'course/modules/M/M2/L22.html, L23.html, L24.html'),
    ('S-process-words', '2.9 no process words in learner text', 'course/modules/M/M2/L22.html, L23.html, L24.html'),
    ('S-scope-words', '2.9 scope words (only, all, always, every, any, same, exactly, never, none)', 'course/modules/M/M2/L22.html, L23.html, L24.html'),
    ('S-L22-L24-structure', '2.9 structure: section order, quiz of 8 items per lesson, misconceptions, problem tiers', 'course/modules/M/M2/L22.html, L23.html, L24.html'),
    ('H-hours', '2.9 hours: data-hours=10 on each of L22, L23, L24; hub split arithmetic', 'course/modules/M/M2/L22.html:2, L23.html:2, L24.html:2; index.html:29, :142'),
]:
    carry = C9
    extra = ''
    if id_ == 'CARD-L22':
        carry = CC
    if id_ == 'CARD-L24':
        carry = CC
    if id_ == 'S-banned-phrases':
        extra = ' Fresh: check_pages.py enforces the banned strings on the same bytes (PASS, out/check_pages_L2x.txt).'
    if id_ == 'H-hours':
        extra = (' Fresh: grep shows data-hours="10" on L22, L23, L24 and index.html cards read "L22 · 10 h", "L23 · 10 h", "L24 · 10 h"; '
                 'curriculum/curriculum.json changed between the pins only in the name of the M3 concept level-slope-curvature, not in any M2 hours (' + O + 'hash_subjects.txt).')
    if id_ == 'DAG-prerequisites':
        extra = ''
    row(id_, chk, loc, carry + 'round-9 evidence stands.' + extra)

row('CARD-L23', '2.7 cards: all 24 L23 cards against the current L23 text (M2-c352 re-verified this round)',
    'course/modules/M/M2/cards.json (lesson L23), M2-c352 at cards.json:2445',
    f'Fresh for M2-c352 (the only slice card changed since the pin): new back states that Lab 1 prints a nonzero difference at +0.01 (true: -15 cents, L23.html:224) and matches misconception 1 (L23.html:281); no number, grade C with lab basis. The other 23 L23 cards are byte-identical to the round-9 pin ({O}cards_delta.txt) and carry the round-9 verification.')
row('CARD-DUP', '2.7 cards: no duplicate card in L22-L24 and none across the unit', 'course/modules/M/M2/cards.json',
    f'Fresh: {S}cards_delta.py: no duplicate ids, fronts or backs across 397 cards; the new cards M2-c412 (L08) and M2-c413 (L15) duplicate none. Evidence {O}cards_delta.txt.')
row('DAG-prerequisites', '2.9 DAG: L22-L24 use only concepts of M2 lessons up to their own, M1 and P0.1, plus prose terms', 'course/modules/M/M2/L22.html:37, L23.html:37, L24.html:37',
    C9 + 'round-9 evidence stands. Fresh: check_dag M2 PASS; the M3 concept rename in curriculum.json (level-slope-curvature) is not used on any L22-L24 page (grep count 0, this round).')
row('DAG-no-later-definitions', '2.9 DAG: no concept defined twice; no later-module dfn or link (Fubini, continuity, Lagrange multipliers)', 'course/modules/M/M2/L22.html, L23.html, L24.html',
    C9 + 'round-9 evidence stands. Fresh: check_dag M2 PASS.')
row('REG-registry-flags', '2.1 registry: no key cited with a locator on L22-L24; nothing to flag', 'course/modules/M/M2/L22.html:473, L23.html:488, L24.html:468',
    f'Fresh: grep for data-locator on L22-L24 returns 0; the two keys named (spivak2008calculus, hubbard2015vector) pass offline (560 entries) and live M2 (2 entries) re-verification. Nothing to flag. Evidence {O}verify_refs_offline.txt, {O}verify_refs_live_M2.txt.')

# repo-wide gates, fresh
row('G-repo-ruff-mypy', 'tooling: ruff check ., ruff format --check ., mypy --no-incremental (repo)', 'repository',
    f'Fresh: ruff check "All checks passed!"; ruff format --check "553 files already formatted"; mypy --no-incremental "Success: no issues found in 385 source files". Evidence {O}ruff_check_repo.txt, ruff_format_repo.txt, mypy_repo.txt.')
row('G-render-curriculum-diff', 'gate: render_curriculum.py then git diff --exit-code CURRICULUM.md curriculum/curriculum.json', 'CURRICULUM.md; curriculum/curriculum.json',
    f'Fresh: render_curriculum "curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)"; git diff --exit-code exit 0 (no regenerated change). Evidence {O}render_curriculum.txt, render_diff.txt.')
row('G-build-site-fetch-data', 'gates: build_site.py --check and fetch_data.py --check', 'course/assets/data/; course/index.html; course/concepts.html; course/assets/data/market/',
    f'Fresh: "site data current: 6 outputs" (build_site --check, exit 0); "fetch_data: 3 datasets, 0 problems" (exit 0). Evidence {O}build_site_check.txt, fetch_data_check.txt.')
row('G-check-projects-all', 'gate: check_projects.py --all (M2 included; project page changed at 47a36d8c, outside this slice)', 'course/modules/M/M2/project.html',
    f'Fresh: "check_projects M2: PASS" and every unit PASS, exit 0. Evidence {O}check_projects_all.txt, check_projects_M2.txt.')

notes = (
 'Lab-only slice (L22, L23, L24 and their twins); no grader and no mutants in the slice, so mutants is empty. '
 'Delta: the slice pages and twins are byte-identical to the round-9 pin 1e272e5a (sha256 SAME). Only one slice card changed: M2-c352 (cards.json:2445). Re-verified from the lesson text and a fresh recomputation of every L23 number it rests on. '
 'Rows marked "Carried from round 9" cite subjects that are byte-identical, per the rules; their evidence is the round-9 evidence, re-confirmed where a gate or script covers the same claim. '
 'Outside this slice, and not rows here: the M2 project (project.html, grader/test_project.py changed at 47a36d8c). Ran for context: run_graders.py --unit M2 --seeds 0-49 PASS (reference 50/50); mutate_graders.py --unit M2 --seeds 0-9 PASS (166/166 killed); ' + O + 'run_graders_M2.txt, mutate_graders_M2.txt. Cards M2-c027 (L03), c047 (L04), c177 (L12), and added c412 (L08), c413 (L15) changed; they are outside this slice and were scanned for duplication only. '
 'Not run: verify_refs live over the whole registry (other slices and the scheduled job); the full pytest suite (only tests/test_labs.py -k M2 is relevant to the slice); the Pyodide run of the other units. '
 'Observation: L24 Remark 4.4 and L24.html:243 state the signed computed error -6.603e-9, which the lab does not print (it prints abs); the lesson says so explicitly, and the signed value was re-derived (l24_numbers.py). Not a defect.'
)

frag = {
  'unit': 'M2', 'slice': 'd2', 'round': 10,
  'verifier': 'Claude Haiku 5.5, independent verifier for M2-d2, round 10 (did not build M2; no context shared with the builders).',
  'pin': '47a36d8c78633793ccc762ae19dcd5e19b780d19',
  'base': '1e272e5a641f18412703b37778a44db6f7391a69 (round-9 pin, the last PASS for this slice). Delta 1e272e5a..47a36d8c touches in the slice only course/modules/M/M2/cards.json (M2-c352). L22.html, L23.html, L24.html and the three twins are byte-identical to the round-9 pin.',
  'checkout': '/Users/billyribeiro/.fanout/wt/verifyD10-M2-d2',
  'scratch': '/Users/billyribeiro/.fanout/wt/verifyD10-M2-d2/ledgers/M2/scripts/M2-d2-r10',
  'verified_at': '2026-11-05T05:50:00+00:00',
  'verdict': 'PASS',
  'rows': rows,
  'mutants': [],
  'registry_flags': [],
  'freshness_flags': [],
  'notes': notes,
  'summary': f'slice d2 round 10: rows={len(rows)}, pass={sum(r["status"]=="PASS" for r in rows)}, fail=0, unverifiable=0. Mutants 0 (lab-only slice). Fresh this round: all gates (check_pages, check_dag, run_labs, twins isolated, page_smoke, ruff, mypy, pytest -k M2, verify_refs offline and live M2, build_site, fetch_data, repo ruff/mypy, render_curriculum diff, check_projects --all), card M2-c352 and every L23 number it rests on, L24 numbers, L23 numbers, lab code/expected equality. Carried from round 9: content rows whose subject bytes are unchanged.',
}
problems = ledger.validate(frag, 'M2-d2')
print('validate:', problems)
json.dump(frag, open('ledgers/M2/M2-d2.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
open('ledgers/M2/M2-d2.json', 'a').write('\n')
print('rows', len(rows), 'pass', sum(r['status']=='PASS' for r in rows))
