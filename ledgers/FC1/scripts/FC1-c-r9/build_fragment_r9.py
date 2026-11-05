"""Verifier FC1-c round 9: write the fragment ledgers/FC1/FC1-c.json from this round's evidence."""
import json, re, datetime, pathlib

ROOT = pathlib.Path('/Users/billyribeiro/.fanout/wt/verifyD9-FC1-c')
S = 'ledgers/FC1/scripts/FC1-c-r9'
O = f'{S}/out'
mut_lines = (ROOT / O / 'mutate_graders_0_19_r9_final.out').read_text(encoding='utf-8').splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r'^(KILLED|SURVIVED) (\S+)\.py: (.*) -> (.*)$', line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    entry = {'id': name, 'description': desc.strip(), 'killed_by': None if killed.strip() == 'None' else killed.strip()}
    mutants.append(entry)

P = 'PASS'
F = 'FAIL'
rows = []
def row(rid, check, location, status, evidence, fix=None):
    r = {'id': rid, 'check': check, 'location': location, 'status': status, 'evidence': evidence}
    if status != P:
        r['fix'] = fix
    rows.append(r)

# --- project page and labs (fresh evidence this round)
row('proj-check-projects', '2.6-structure', 'course/modules/FC/FC1/project.html', P,
    f'tools/check_projects.py --unit FC1 -> "check_projects FC1: PASS", exit 0 ({O}/check_projects.out).')
row('proj-check-pages', '2.9-structure', 'course/modules/FC/FC1/project.html', P,
    f'tools/check_pages.py --unit FC1 -> "check_pages FC1: PASS", exit 0 ({O}/check_pages.out).')
row('proj-check-dag', '2.9-dag', 'project.html; curriculum/curriculum.json concepts', P,
    f'tools/check_dag.py --unit FC1 -> "check_dag FC1: PASS", exit 0 ({O}/check_dag.out). Concept links present-value and discount-factor resolve (project.html line 178).')
row('proj-run-labs', '2.5-labs', 'project.html Labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py', P,
    f'tools/run_labs.py --unit FC1 --page project -> "run_labs FC1: PASS (3/3)", exit 0 ({O}/run_labs_project.out); each twin run with python -I -W error exits 0 ({O}/labs_r9.out).')
row('proj-page-smoke', '2.9-smoke', 'course/modules/FC/FC1/project.html', P,
    f'tools/page_smoke.py --unit FC1 --pages project -> "page_smoke modules/FC/FC1/project.html: PASS"; in-browser grader "All 82 tests pass on seed 1052776526" ({O}/page_smoke_project.out).')
row('proj-run-graders', '2.6-autograde-reference', 'grader/reference.py, test_project.py, instance.py, starter.py', P,
    f'tools/run_graders.py --unit FC1 --seeds 0-49 -> "run_graders FC1: PASS (reference 50/50 seeds, slowest 0.2 s)", exit 0 ({O}/run_graders_0_49.out).')
row('proj-lint-types', '2.6-lint', 'course/modules/FC/FC1/grader/*.py; tests/labs/FC1/; ledgers/FC1', P,
    f'ruff check . -> "All checks passed!" ({O}/ruff_check.out); ruff format --check on FC1 pages, labs and ledgers -> "12 files already formatted" ({O}/ruff_format.out); mypy --no-incremental -> "Success: no issues found in 385 source files" ({O}/mypy.out).')
row('proj-lab1-numbers', '2.2-numbers', 'project.html lines 58, 97-100 (Lab 1)', P,
    f'{O}/numbers_r9.out: exact present value 225796875/2197 = 102775.09103322713 cents; "%.6f" gives 102775.091033; half-away price 102775. Lab 1 expected block equals twin output ({O}/labs_r9.out).')
row('proj-lab2-blanks', '2.5-labs', 'project.html lines 133, 140 (Lab 2)', P,
    f'{O}/labs_r9.out: page code differs from tests/labs/FC1/lab-FC1-project-2.py at exactly two lines, the exponent ___ and the trade ___ (the completion blanks); twin exit 0; expected block equals output. The blanks are the Rung 2 convention (Architect ruling 11).')
row('proj-lab3-fixture-values', '2.2-numbers', 'project.html lines 198-275 (Lab 3)', P,
    f'{O}/numbers_r9.out recomputes fixtures A-G: A [(1,10500)] price 10000; B 210000/19 = 11052.6316, price 11053; C [(1,5001),(2,15002)]; D [(1,2)]; rounding events [(1,500),(2,500),(3,10500)], price 10278 once, 10277 term by term; E (2,-98500); F [(1,1)] price 1; G [(1,10001)] price 5001. {O}/labs_r9.out: Lab 3 page code equals twin (0 differing lines); expected equals output.')
row('proj-rounding-fixture-terms', '2.2-numbers', 'project.html line 193; grader/test_project.py lines 396-403', P,
    f'{O}/numbers_r9.out: exact 10277.509103322713 rounds once to 10278; terms 480.769231, 462.278107, 9334.461766 round one by one to 481+462+9334 = 10277; the page prints 10277.509103 (six decimals, correct).')
row('proj-lab3-claim-using-functions', '2.5-labs', 'project.html line 198 vs tests/labs/FC1/lab-FC1-project-3.py', P,
    f'{O}/labs_r9.out: Lab 3 page code equals its twin (0 differing lines); the twin defines bond_events, bond_price and term_by_term_price as the hypothesis states.')
row('proj-expected-equals-output', '2.5-labs', 'project.html expected blocks lines 97-100, 145-148, 263-275', P,
    f'{O}/labs_r9.out: expected block == twin output True for lab-FC1-project-1, -2 and -3.')
row('proj-hours-arithmetic', '2.9-hours', 'project.html table#hours lines 286-293; data-hours-project line 34', P,
    'Components 1+2+5+4+2+3+3 = 20 = data-hours-project="20" (line 34) = total cell line 293. Hub index.html line 29 data-hours-lessons="50" + data-hours-project="20" = 70 (line 31 "70 hours"); curriculum/02-economics-finance-core.yaml line 366 "hours: 70". Consistent.')
row('proj-hours-rationale-rows', '2.9-hours', 'project.html table#hours lines 286-293', P,
    'Each component row has a rationale; row 290 "Eight conditions" equals the eight named conditions of project.html lines 165-167 (Bond 3, bond_price_cents 1, CashTrade 4); side refused on 0, 2, -2, 3, -3 and accepted on +1, -1 matches test_project.py lines 621-652.')
row('proj-hours-verifier-estimate', '2.9-hours', 'project.html table#hours rows 291-292', P,
    'Rows "Local suite on seeds 0 to 9 and Lab 3 fixtures" (3 h) and "Self-check against the conventions block" (3 h) are design-target hours (Architect ruling: hours are design targets; only arithmetic is graded). Arithmetic consistent with row total 20.')
row('proj-ladder', '2.9-structure', 'project.html lines 41-50, 52-151, 153-172, 312-319', P,
    f'Rung text matches sections; anchors #conventions, #spec, #grader-section, #stretch and index.html#placement (index.html line 67 id="placement") exist; check_pages PASS ({O}/check_pages.out).')
row('proj-spec-interface', '2.6-spec', 'project.html line 161; grader/starter.py lines 16-40', P,
    'Names and signatures on page line 161 (Bond(face_cents, coupon_bps, periods).events(); bond_price_cents(bond, yield_bps); CashTrade(quantity, price_cents, side, settlement_day).events()) equal starter.py lines 16-40.')
row('proj-named-conditions', '2.6-conditions', 'project.html lines 163-167; reference.py lines 42-47, 64-65, 81-88; test_project.py', P,
    'Eight named conditions (periods<1, face<=0, coupon<0, yield<=-10000, quantity<1, price<0, side not in {+1,-1}, settlement_day<1) each have refusal and boundary tests on both sides (test_project.py lines 215-260, 499-520, 559-661, 654-669, 509-512, 265, 221-249). No unnamed refusal exists in reference.py; no test requires a refusal the page does not name.')
row('proj-test-count', '2.9-count', 'project.html line 171; grader/test_project.py', P,
    f'pytest --collect-only on the reference with the suite: "82 tests collected" ({O}/collect_only_r9.out); page line 171 says 82 checks.')
row('proj-starter-fails', '2.6-starter', 'grader/starter.py', P,
    f'starter.py as instruments.py, QF_SEED=0, pytest -q -p no:cacheprovider --assert=plain -W error: 80 failed, 2 passed (the two that pass accept any exception or return). run_graders starter check PASS ({O}/starter_run_r9.out).')
row('proj-instances', '2.6-instances', 'grader/instance.py, seeds 0-49', P,
    f'make_instance is deterministic; 50 distinct instances over seeds 0-49; periods 1-8, yield 66-889 bps, settlement 1-5 ({O}/instance_seeds_r9.out). Within the 50-to-900 yield range that test_project.py line 485 relies on.')
row('proj-silence-purity', '2.6-silence', 'grader/test_project.py lines 693-734', P,
    'test_the_module_prints_nothing and test_refused_inputs_print_nothing_before_they_raise run on the reference (50/50 seeds PASS). Their listed inputs match the docstring (line 694-696).')
row('proj-same-suite-pyodide-pytest', '2.6-same-file', 'grader/test_project.py; project.html line 309', P,
    'The same file runs in-browser (page_smoke, 82 pass) and under local pytest with the page flags (alternatives runner, identical command). Pyodide itself was not run beyond page_smoke.')
row('proj-local-command', '2.6-docs', 'project.html line 308; grader/starter.py line 6', P,
    'The command QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py was run with the reference and all alternatives (ledgers/FC1/scripts/FC1-c-r9/out/alternatives_0_19_r9.out).')
row('proj-scope-words', '2.6-prose', 'project.html lines 163, 171, 176-186', P,
    'Scope words checked: "every named condition" (171) matches the boundary tests; "Each events() call returns the same list" (180) matches test_repeated_events_calls_agree; "Any other invalid input may raise any exception or return" (163) matches the must_raise-only-for-named rule (test_project.py lines 9-13).')
row('proj-terms-before-definition', '2.6-terms', 'project.html lines 54-56, 161', P,
    'holder, event, settlement period are defined in line 54 before use; side is used in line 106 with a link to Conventions (line 179 defines it); present value and discount factor are linked concepts.')
row('proj-prose-banned-phrases', '2.6-prose', 'project.html; cards.json; grader/*.py; labs', P,
    'Grep for process words (verifier, builder, round N, TODO, draft, placeholder, fixed in, regenerated, as the orchestration) returns no learner-facing hit in project.html, cards.json, grader/*.py or the three labs.')
row('proj-process-words', '2.6-prose', 'project.html; cards.json; labs', P,
    'Same grep as proj-prose-banned-phrases; "a reviewer reads it" (line 161, 163) is a learner-facing reference to the reviewer of the work, not a process word.')
row('proj-notation', '2.6-notation', 'notation/notation.json; FC1 pages, cards, labs', P,
    'notation.json holds 8 symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}). Grep of FC1 pages, cards and labs finds none of them used. Plain Q (volume of a closed sequence, L03 Definition 2.1 and card FC1-c131) is a different symbol from \\mathbb{Q}; noted for the registry owner, not a reuse.')
row('proj-footer-claim', '2.6-claim', 'project.html line 341; course/assets/js/grader.js; store.js; python.js', P,
    'grader.js performs one fetch, a GET of the unit\'s own grader files (grader.js line 18); store.js uses IndexedDB only; no POST, beacon or socket in grader.js, store.js or python.js. Pyodide loads its runtime; the learner\'s code is not sent.')
row('proj-saved-as-you-type', '2.6-claim', 'project.html line 301; course/assets/js/grader.js lines 33-79; store.js', P,
    'grader.js line 61 saves the editor value to store.put("files", draftKey) after each edit (400 ms debounce); store.js opens IndexedDB (line 17). Matches "saved in this browser as you type".')
row('proj-references-reading-list', '2.6-references', 'project.html lines 321-328; references/references.json', P,
    'The reading list cites mishkin2021economics and harris2002trading; both keys exist in references/references.json (lines 11536 and 17488). The page states no year.')
row('proj-cited-year-conflicts', '2.6-references', 'project.html reading list; references/references.json; curriculum/02-economics-finance-core.yaml lines 384-385', P,
    'Registry year for harris2002trading is 2002 (references.json line 11536 onward); curriculum line 385 says (2003). Registry year for mishkin2021economics is 2021; curriculum line 384 says 13th ed. (2022). The project page states no year, so the page is consistent; the conflict is recorded in registry_flags for the curriculum owner.')
row('proj-data-simulated', '2.6-data', 'project.html lines 45, 54, 159; grader/instance.py lines 3-6, 31; tests/labs/FC1/lab-FC1-project-*.py', P,
    'Every bond and trade is SIMULATED and labelled so (project.html lines 45, 54, 159; instance.py label line 31); no file is read in the labs (lab twins contain no open() call).')
row('proj-lab3-autograder-coverage-note', '2.5-labs', 'project.html line 276 (note after Lab 3); grader/test_project.py', P,
    'The note says the autograder checks fixture A events and price (one-period tests), B price (negative-yield test), C and D events (half-cent tests), E events (buyer and seller tests), F events and price (one-cent-face and exact-half tests), G price (exact-half test) and the rounding price (rounding test); G events and the rounding-case events are not checked as lists. Each listed check exists (test_project.py: fixture A events 174-179, B price 376-382, C and D events 189-202, E events 536-549, F events 242-247 and price 406-412, G price 415-420, rounding price 396-403); no list check exists for G or the rounding case.')
row('proj-page-grading-description', '2.6-claims', 'project.html line 171; grader/test_project.py', P,
    'Line 171 lists: 82 checks (collect-only 82); bonds of 13-15, 24, 40, 100, 1001 and 5001 periods (tests at lines 281, 304, 318, 791, 806, 862); exact-half cases (434, 839, 415, 406, 459); boundaries of each named condition; yields at 150 %, 300 %, 2000 % (515, 822, 849); trades settling in 100, 1000, 5001 (672, 831, 872); silence and purity (693, 719). Each claim has its test.')
row('proj-page-hypothesis-sides', '2.6-claims', 'project.html line 106 (Lab 2 hypothesis)', P,
    'The added parenthesis "side is +1 for a buyer and -1 for a seller" matches Conventions line 179 and reference.py line 11 and the trade event in Lab 2 (line 140).')
row('proj-page-constraints-silence', '2.6-claims', 'project.html line 163 (round 9 wording)', P,
    'The narrowed wording "On the inputs the suite checks for silence (...), no function prints or warns" is true of the suite: the silence tests cover exactly the listed inputs (test_project.py lines 694-712, 720-730).')
row('proj-docstring-float-claim', '2.2-numbers', 'grader/test_project.py lines 423-427, 451-452, 459-462', P,
    f'{O}/numbers_r9.out: Bond(1704285,179,1) at 496 bps exact 3305625/2 = 1652812.5, rounds to 1652813; float form 1652812.4999999998; Bond(13,0,1) at 400 bps exact 25/2; float (1+0.04)**-1*13 = 12.499999999999998, rounds to 12; Bond(300075005,0,3) at 1 bps equals 299985000 + 1/2 - 1/(2*1000300030001) exactly (True).')
row('proj-test-docstring-hand-numbers', '2.2-numbers', 'grader/test_project.py docstrings', P,
    f'{O}/numbers_r9.out re-derives every number in the new docstrings: 10**10+1 -> 5000000001 and 10**12+1 -> 500000000001; 10**40+1 -> 5*10**39+1; 10500/21 = 500; 10500/4 = 2625; 10500/2.5 = 4200; 10**17+4999 coupon rounds to 10**13; 2**40+1 times 9851 > 2**53. A decimal context of 10 significant digits gives 5000000000 (drops the half), as the docstring says.')
row('proj-named-error-message-values', '2.6-messages', 'grader/test_project.py lines 75-93, 693-734', P,
    'must_raise and must_accept messages name the condition only; no expected value is printed (line 13 docstring holds).')
row('proj-failure-messages', '2.6-messages', 'grader/test_project.py lines 693-734, 770-788', P,
    'Failure messages state the property (e.g. "a valid input must print nothing", "the page requires a ValueError for this input"); _named_when_unimplemented names the property with pytrace=False.')
row('proj-starter-message-leaks-answer', '2.6-messages', 'grader/test_project.py lines 822-828', P,
    'The docstring of the 300 % test states the rule ("the price is the discounted event") and no number other than the stated yield; the expected value 2625 sits in the assertion, not the docstring.')
row('proj-starter-unwrapped-new-tests', '2.6-wrapper', 'grader/test_project.py lines 881-884', P,
    'The wrapper loop at the end of the file wraps every test_ name in globals(), including the four tests added this round (lines 849-878); the starter run names the missing implementation rather than printing a traceback.')
row('proj-alternatives', '2.6-alternatives', 'ledgers/FC1/alternatives/a1-a5 (grader suite seeds 0-19)', P,
    f'run_alts_r9.sh: a1..a5 pass=20 fail=0 on seeds 0-19 ({O}/alternatives_0_19_r9.out).')
row('proj-alternatives-r4-new', '2.6-alternatives', 'ledgers/FC1/scripts/FC1-c-r4/alt/alt6', P,
    f'alt6_r4_pow_fraction_floor.py pass=20 fail=0 on seeds 0-19 ({O}/alternatives_0_19_r9.out).')
row('proj-alternatives-r6-new', '2.6-alternatives', 'ledgers/FC1/scripts/FC1-c-r6/alt/alt7..alt9', P,
    f'alt7, alt8, alt9 each pass=20 fail=0 on seeds 0-19 ({O}/alternatives_0_19_r9.out).')
row('proj-alternatives-r7-new', '2.6-alternatives', 'ledgers/FC1/scripts/FC1-c-r7/alt/alt10..alt12', P,
    f'alt10, alt11, alt12 each pass=20 fail=0 on seeds 0-19 ({O}/alternatives_0_19_r9.out).')
row('proj-alternatives-r8-new', '2.6-alternatives', 'ledgers/FC1/scripts/FC1-c-r8/alt/alt13..alt15', P,
    f'alt13, alt14, alt15 each pass=20 fail=0 on seeds 0-19 ({O}/alternatives_0_19_r9.out).')
row('proj-alternatives-fixed-suite-r9', '2.6-over-constraint', 'ledgers/FC1/scripts/FC1-c-r9/proposed_fix_test_project_r9.py (scratch, not applied)', P,
    f'All 15 alternatives pass the proposed fixed suite on seeds 0-19 ({O}/alternatives_fixed_suite_r9.out); the fix adds only accepted-input tests, so no over-constraint appears.')

# --- mutant rows: the 116 round-8 mutants are all killed on seeds 0-19 now
def killed(name):
    for m in mutants:
        if m['id'] == name:
            return m['killed_by']
    raise KeyError(name)
row('proj-mutants-all', '2.6-mutants', 'ledgers/FC1/mutants/*.py (124 files)', F,
    f'tools/mutate_graders.py --unit FC1 --seeds 0-19 -> "mutate_graders FC1: FAIL (120/124 killed)" ({O}/mutate_graders_0_19_r9_final.out). All 120 earlier mutants are killed; the four new r9c mutants survive (rows proj-mutant-r9c-*).',
    'Add accepted-input tests at the largest values the page leaves unbounded, as in ledgers/FC1/scripts/FC1-c-r9/proposed_fix_test_project_r9.py (10**6 bps, 100001 periods events-only, 10**6 settlement period, 10**30 quantity). With them, all four mutants are killed and the reference passes 86/86.')
for grp, label in [('v1c_', 'v1c'), ('r2c_', 'r2c'), ('r3c_', 'r3c'), ('v4c_', 'v4c'), ('r4c_', 'r4c'), ('r5c_', 'r5c'), ('r6c_', 'r6c'), ('r7c_', 'r7c')]:
    ids = [m['id'] for m in mutants if m['id'].startswith(grp)]
    kills = all(m['killed_by'] for m in mutants if m['id'].startswith(grp))
    rid = {'v1c': 'proj-mutants-v1c-new', 'r2c': 'proj-mutants-v2c-new', 'r3c': 'proj-mutants-r3c-killed', 'v4c': 'proj-mutants-v4c-new', 'r4c': 'proj-mutants-r4c-new', 'r5c': 'proj-mutants-r5c-new', 'r6c': 'proj-mutants-r6c-killed', 'r7c': 'proj-mutants-r7c-new'}[label]
    row(rid, '2.6-mutants', f'ledgers/FC1/mutants/{grp}*.py ({len(ids)} files)', P if kills else F,
        f'All {len(ids)} {grp}* mutants killed on seeds 0-19 ({O}/mutate_graders_0_19_r9_final.out).')

row('proj-mutant-schedule-cap-thirty-survivor', '2.6-mutants', 'grader/test_project.py lines 318-329 (40-period test)', P,
    f'r4c_schedule_stops_at_thirty_periods killed by {killed("r4c_schedule_stops_at_thirty_periods")} ({O}/mutate_graders_0_19_r9_final.out).')
row('proj-mutant-exponent-cap-thirty-survivor', '2.6-mutants', 'grader/test_project.py lines 318-329', P,
    f'r4c_discount_exponent_capped_at_thirty killed by {killed("r4c_discount_exponent_capped_at_thirty")}.')
row('proj-mutant-schedule-cap-survivor', '2.6-mutants', 'grader/test_project.py lines 304-315 (24-period test)', P,
    f'r3c_schedule_stops_at_twenty_periods killed by {killed("r3c_schedule_stops_at_twenty_periods")}.')
row('proj-mutant-price-digits-survivor', '2.6-mutants', 'grader/test_project.py lines 434-445', P,
    f'r3c_price_ten_significant_digits killed by {killed("r3c_price_ten_significant_digits")}.')
row('proj-mutant-price-cache-survivor', '2.6-mutants', 'grader/test_project.py lines 483-496', P,
    f'r2c_price_cached_on_first_yield killed by {killed("r2c_price_cached_on_first_yield")}.')
row('proj-mutant-price-epsilon-survivor', '2.6-mutants', 'grader/test_project.py lines 459-466', P,
    f'r5c_price_rounded_with_epsilon killed by {killed("r5c_price_rounded_with_epsilon")}.')
row('proj-mutant-yield-100-survivor', '2.6-mutants', 'grader/test_project.py lines 515-521', P,
    f'r5c_yield_above_one_hundred_percent_refused killed by {killed("r5c_yield_above_one_hundred_percent_refused")}.')
row('proj-mutant-schedule-cap-forty-survivor', '2.6-mutants', 'grader/test_project.py lines 791-803 (100-period test)', P,
    f'r6c_schedule_stops_at_forty_periods killed by {killed("r6c_schedule_stops_at_forty_periods")}.')
row('proj-mutant-exponent-cap-forty-survivor', '2.6-mutants', 'grader/test_project.py lines 791-803', P,
    f'r6c_discount_exponent_capped_at_forty killed by {killed("r6c_discount_exponent_capped_at_forty")}.')
row('proj-mutant-yield-200-survivor', '2.6-mutants', 'grader/test_project.py lines 822-828', P,
    f'r6c_yield_above_two_hundred_percent_refused killed by {killed("r6c_yield_above_two_hundred_percent_refused")}.')
row('proj-mutant-settlement-cap-100-survivor', '2.6-mutants', 'grader/test_project.py lines 672-679 and 831-836', P,
    f'r6c_settlement_day_above_one_hundred_refused killed by {killed("r6c_settlement_day_above_one_hundred_refused")}.')
row('proj-mutant-decimal-40-digits-survivor', '2.6-mutants', 'grader/test_project.py lines 839-846', P,
    f'r6c_price_decimal_forty_significant_digits killed by {killed("r6c_price_decimal_forty_significant_digits")}.')
row('proj-mutant-decimal-28-digits-kill', '2.6-mutants', 'grader/test_project.py lines 839-846', P,
    f'r6c_price_default_decimal_28_digits killed by {killed("r6c_price_default_decimal_28_digits")}.')
row('proj-mutant-periods-cap-1000-survivor', '2.6-mutants', 'grader/test_project.py lines 806-819', P,
    f'r7c_periods_refused_above_one_thousand killed by {killed("r7c_periods_refused_above_one_thousand")}.')
row('proj-mutant-r7c-coupon-half-even', '2.6-mutants', 'grader/test_project.py lines 189-194', P,
    f'r7c_coupon_rounded_half_even killed by {killed("r7c_coupon_rounded_half_even")}.')
row('proj-mutant-r7c-discount-float', '2.6-mutants', 'grader/test_project.py lines 423-431', P,
    f'r7c_discount_factor_float_then_exact killed by {killed("r7c_discount_factor_float_then_exact")}.')
row('proj-mutant-r7c-price-cap-1m', '2.6-mutants', 'grader/test_project.py lines 347-349', P,
    f'r7c_price_refused_above_one_million_cents killed by {killed("r7c_price_refused_above_one_million_cents")}.')
row('proj-mutant-r7c-hard-coded-answer', '2.6-mutants', 'grader/test_project.py lines 318-329', P,
    f'r7c_price_is_seed_zero_answer_constant killed by {killed("r7c_price_is_seed_zero_answer_constant")}.')
row('proj-mutant-yield-1000-survivor', '2.6-mutants', 'grader/test_project.py lines 849-859 and 515-521', P,
    f'r8c_yield_refused_above_one_thousand_percent killed by {killed("r8c_yield_refused_above_one_thousand_percent")}.')
row('proj-mutant-settlement-5000-survivor', '2.6-mutants', 'grader/test_project.py lines 872-878', P,
    f'r8c_settlement_day_refused_above_five_thousand killed by {killed("r8c_settlement_day_refused_above_five_thousand")}.')
row('proj-mutant-periods-5000-survivor', '2.6-mutants', 'grader/test_project.py lines 862-869', P,
    f'r8c_periods_refused_above_five_thousand killed by {killed("r8c_periods_refused_above_five_thousand")}.')
row('proj-mutant-face-int64-kill', '2.6-mutants', 'grader/test_project.py lines 434-446 and 839-846', P,
    f'r8c_face_refused_above_int64 killed by {killed("r8c_face_refused_above_int64")}.')
row('proj-mutants-r8c-new', '2.6-mutants', 'ledgers/FC1/mutants/r8c_*.py (4 files)', P,
    'All four r8c mutants killed on seeds 0-19 (the three round-8 survivors are killed by the round-8 accepted-input tests).')

row('proj-mutants-r9c-new', '2.6-mutants', 'ledgers/FC1/mutants/r9c_*.py (4 new student-error mutants, this round)', F,
    'Four new student-error mutants written this round: r9c_yield_refused_above_two_thousand_percent, r9c_periods_refused_above_ten_thousand, r9c_settlement_day_refused_above_ten_thousand, r9c_quantity_refused_above_two_to_the_fifty. All four SURVIVE seeds 0-19 (mutate_graders_0_19_r9_final.out).',
    'See the four proj-mutant-r9c-* rows; the proposed accepted-input tests kill all four (proposed_fix_test_project_r9.py run: 1 failed each).')
row('proj-mutant-r9c-yield-2000-survivor', '2.6-mutants', 'grader/test_project.py lines 849-859 (yield test at 200000 bps only); project.html line 171', F,
    'r9c_yield_refused_above_two_thousand_percent (refuses yield_bps > 200000) survives seeds 0-19. project.html line 171 states: "a yield above 100 % per period, which the page does not refuse (checked at 150 %, at 300 % and at 2000 %)". The suite checks 200000 bps and no larger yield, so a refusal above 2000 % goes undetected.',
    'Add an accepted-input test at yield_bps = 1_000_000 (price 10500 / 101 = 104 cents, computed and verified: bond_price_cents returns 104). Verified scratch: the mutant fails it.')
row('proj-mutant-r9c-periods-10000-survivor', '2.6-mutants', 'grader/test_project.py lines 806-819 and 862-869 (largest accepted periods 5001); project.html lines 163-165', F,
    'r9c_periods_refused_above_ten_thousand survives seeds 0-19. project.html line 165 names periods less than 1 as the only Bond refusal for periods, and line 163 says each named condition raises and nothing else is named. The largest accepted period count tested is 5001, so a refusal of 10001 periods is not detected. Same class as the round-7 (1000) and round-8 (5000) survivors.',
    'Add an events-only accepted-input test at 100001 periods (reference runs it in 0.02 s); the mutant fails. Price tests at that size are too slow to run, so the events list is the check.')
row('proj-mutant-r9c-settlement-10000-survivor', '2.6-mutants', 'grader/test_project.py lines 872-878 (largest tested settlement 5001); project.html line 171', F,
    'r9c_settlement_day_refused_above_ten_thousand survives seeds 0-19. project.html line 171 states: "trades settling in periods 100, 1000 and 5001, which the page does not bound". The suite does not test a settlement period above 5001.',
    'Add an accepted-input test at settlement_day = 10**6 (one event at period 10**6); the mutant fails.')
row('proj-mutant-r9c-quantity-2pow50-survivor', '2.6-mutants', 'grader/test_project.py lines 577-605 (largest tested quantity 2**40+1); project.html line 167', F,
    'r9c_quantity_refused_above_two_to_the_fifty survives seeds 0-19. project.html line 167 names quantity less than 1 as the only CashTrade quantity refusal and line 163 names nothing else; the suite accepts up to 2**40+1 and no larger quantity.',
    'Add an accepted-input test at quantity = 10**30 (event (2, -10**30 * 9850)); the mutant fails.')

row('proj-cards-scan-duplicates', '2.6-cards', 'course/modules/FC/FC1/cards.json (151 cards)', P,
    'Script ledgers/FC1/scripts/FC1-c-r9/cards_cites_r9.py and inline checks: 151 unique ids, 0 duplicate fronts, 0 duplicate backs. Near-duplicate fronts (SequenceMatcher > 0.8) are the distinct assumption cards (A1/A2/A3, B1/B2/B3/B4, bid/ask). id FC1-c134 is absent from the sequence (a gap, not a duplicate; noted).')
row('proj-cards-numbers-in-lessons', '2.6-cards', 'cards.json vs ledgers/FC1/scripts/FC1-c-r9/lessons_text/L01-L05.txt (regenerated from the checkout)', P,
    'Every number in every card back (except 0-12) appears in the card\'s own lesson text (script output: 0 missing).')
row('proj-cards-numbered-references', '2.6-cards', 'cards.json citations vs lesson headings', P,
    'Each cited Definition/Proposition/Remark/Example/Corollary/Section/Problem resolves to a heading in its own lesson; assumption cards cite "Assumptions A1 to A3" (L03 line 31) and "Assumptions B1 to B4" (L03 line 55) with labels "A1 (", "B1 (" etc. Misconception items 1-4 resolve to the Misconceptions section (L01 lines 201-206, L02 161, L03 206, L04 260, L05 292).')
row('proj-cards-sample', '2.6-cards', 'course/modules/FC/FC1/cards.json (all 151 cards read in full)', P,
    'All 151 cards read this round in full (front, back, grade, basis); no sampling.')
row('proj-cards-changed-subjects', '2.6-cards', 'cards.json FC1-c005, c008, c009, c041, c049, c071, c073', P,
    'Changed since the previous pin (git diff 2d755599..1e272e5a): c005 (Section 2 and Assumption 2.0 match lesson lines 27-35), c008 (Remark 3.2: rho = 0 gives D_t = d, S_n = (n+1)d), c009 (A2-prime, rest held as cash, 0 < rho <= 1 hypothesis stated, Prop 3.5), c041 (Prop 2.3 under A1 to A3, one h), c049 (Definition 3.1 under B1 to B4), c071 (misconception 2: stop fills at prices on the opposite side; Example 1.4), c073 (Definition 1.1 clearing: confirms quantity, price, instrument and counterparties).')
row('proj-cards-new-c143-c151', '2.6-cards', 'cards.json FC1-c143 to FC1-c151 (added since the previous pin)', P,
    'c143 resting order = Remark 1.2 (L04 line 28); c144 netting = Definition 1.1 (L05 line 23); c145 novation = Definition 1.1; c146 stage = Section 2 (L01 line 28); c147 S_n = Section 2 sum (L01 line 38); c148 balance sheet = Section 1 (L01 line 22); c149 market = Section 1 (L02 line 21); c150 instrument = lesson introduction (L02 line 19); c151 Prop 2.3 for any finite sequence, closed or not (L03 lines 39-41), grade T matches key results (L03 line 269).')
row('proj-cards-c152-hypotheses', '2.6-cards', 'course/modules/FC/FC1/cards.json FC1-c152 back (grade T)', F,
    'FC1-c152 says "Under leakage ... d/(1 - phi(1 - rho)) is at most d/rho ... (Proposition 3.5)" and omits Proposition 3.5\'s hypotheses: A2-prime replaces A2 with 0 <= phi <= 1; A1 with 0 < rho <= 1 (needed for d/rho to be defined); the no-withdrawal and no-repayment parts of A3 (L01 line 58; Proposition 3.5 statement). Card FC1-c009 carries these hypotheses; c152 does not.',
    'Change the back of FC1-c152 to: "Under A2-prime with 0 <= phi <= 1, A1 with 0 < rho <= 1 and the no-withdrawal and no-repayment parts of A3, d/(1 - phi(1 - rho)) is at most d/rho, with equality if and only if phi = 1 or rho = 1 (Proposition 3.5)."')
row('proj-cards-c139-c142-new', '2.6-cards', 'cards.json FC1-c139 to FC1-c142', P,
    'c139: -1000 = (-1)(100)(10000-9990) (L03 Example 2.5 line 50). c140: -600 = 400 - 1000 = C (Example 2.5). c141: stops activate in arrival order and the check repeats (L04 Remark 1.2 line 28). c142: offsets_nondecreasing prints False when clearing offset > settlement lag (L05 line 26; twin lab-FC1-L05-1.py lines 226-240).')
row('proj-cards-c014-lab-true', '2.5-cards', 'cards.json FC1-c014; Lab 1 Part A', P,
    f'{O}/lab_L01.out: "the partial sums equal the closed form exactly for n = 0 to 10: True".')
row('proj-cards-c122-equity-after-loss', '2.6-cards', 'cards.json FC1-c122; L01 Proposition 4.1 (line 68-69)', P,
    'Proposition 4.1 under Assumption 4.0: equity after loss is E - lambda, nonnegative iff lambda <= E; card matches.')
row('proj-cards-citation-R3', '2.6-cards', 'cards.json FC1-c067; L04 Remark 2.4 and Problem R3', P,
    'Problem R3 resolves in L04 (heading R3); 60 shares contributes 120 to the filled sum (2 x 60, arithmetic checked).')
row('proj-cards-citation-R2', '2.6-cards', 'cards.json FC1-c068; L04 Problem R2 (line 313-314)', P,
    'Problem R2 (L04 line 313-314) starts from best bid 1005 and best ask 1000, which A1 excludes; the card matches the problem setup. The buy of 5 at 999 rests as a bid and leaves the book crossed.')
row('proj-cards-citation-scan', '2.6-cards', 'cards.json citations (all cards)', P,
    'Scripts ledgers/FC1/scripts/FC1-c-r9/cards_cites_r9.py and inline heading check: every citation resolves; the only misses were format labels (A1/B1 labels, Problem P2/P3/R2/R3 labels, Section numbers) which resolve on the heading form.')
row('proj-cards-grades', '2.6-cards', 'cards.json grade fields vs lesson key-results tables', P,
    'T grades checked against each lesson key-results table: Prop 2.2, 2.3, 2.5, 3.1, 3.2, 3.5, 4.1 are T there (L01 265-268, L03 269-271); lab-based T cards match the key-results line for Lab 1 (L01 270) and Lab 2 Part B (L02). Lab-SIMULATED cards are C (c052, c053, c069, c082-c088, c097, c098); c030, c033, c034 are C (hand reading and typed register). Example 1.4 (c037) and Example 3.6 (c011) are hand computations graded T.')

row('proj-spec-scope-vs-curriculum', '2.6-scope', 'project.html line 157 (unchanged text); curriculum/02-economics-finance-core.yaml lines 396-397', P,
    'Carried from round 8 (project.html line 157 and curriculum/02-economics-finance-core.yaml lines 396-397 byte-identical since the previous pin; the round-9 diff touches only project.html lines 106, 163 and 171): the scope sentence (futures, swaps and options are FC2) matches the curriculum.')
row('proj-terminology-short-holder', '2.6-terms', 'project.html line 54', P,
    'Carried from round 8 (project.html line 54 byte-identical since the previous pin): "holder (the party that owns the bond...)" is defined inline before its use in line 54.')
row('proj-ruff-repo-gate-note', '2.6-gates', 'repository gate (ruff check .)', P,
    f'ruff check . -> "All checks passed!" ({O}/ruff_check.out).')
row('proj-verify-refs-offline', '2.6-registry', 'references/references.json (offline)', P,
    f'tools/verify_refs.py --offline -> "offline integrity: 560 entries, 0 problems", exit 0 ({O}/verify_refs_offline.out).')
row('proj-pytest-fc1', '2.6-tests', 'repository pytest -k FC1', P,
    f'.venv/bin/pytest -q -p no:cacheprovider -k FC1 -> exit 0 ({O}/pytest_fc1_r9.out).')
row('proj-labs-twins-I-W-error', '2.5-labs', 'tests/labs/FC1/lab-FC1-L01..L05-1.py (lessons, for card citations)', P,
    f'Each twin run with python -I -W error exits 0 ({O}/lab_L01.out .. lab_L05.out).')
row('proj-reference-deployment', '2.6-deployment', 'BLUEPRINT.md line 401; grader/reference.py line 4; .github/workflows/ci.yml; repository root', F,
    'BLUEPRINT.md line 401: deployment "excludes every grader/reference.py". reference.py line 4 says no file in this repository enforces that. The repository has no deploy config (no vercel.json or railway config at the root; ci.yml has no publish step, only an artifact upload of screenshots at line 79), so the exclusion cannot be checked here. UNVERIFIABLE; repo-wide, applies to every unit.',
    'Implement the exclusion in the deploy pipeline (or amend BLUEPRINT.md to say the repository has no deploy step) and add a check that the published tree has no grader/reference.py.')

row('proj-starter-silence-scope', '2.6-starter', 'course/modules/FC/FC1/grader/starter.py lines 9-10; project.html line 163', F,
    'starter.py line 10 states an unscoped rule: "Nothing may print, warn or change its arguments." Round 9 narrowed the page (project.html line 163) to: silence is required "on the inputs the suite checks for silence", and "Any other invalid input may raise any exception or return". The starter is broader than the page, and "change its arguments" is not on the page or tested.',
    'Replace starter.py line 10 with the page wording: "On the inputs the suite checks, nothing prints or warns; nothing else is required." Drop "or change its arguments" unless the page states it and a test checks it.')
row('proj-test-name-two-thousand-percent', '2.6-tests', 'course/modules/FC/FC1/grader/test_project.py line 849', F,
    'The test named test_bond_yield_of_one_thousand_percent_per_period_is_accepted checks yield_bps = 200000, which is 2000 % per period (its own docstring line 850 says 2000 %). The name says 1000 %.',
    'Rename to test_bond_yield_of_two_thousand_percent_per_period_is_accepted. Name and docstring then agree.')

# --- the round-8 PASS rows that are carried or re-verified are above; add round-9 rows not in round 8
row('proj-alternatives-r9-fresh', '2.6-alternatives', 'ledgers/FC1/alternatives/a1..a5 and alt6..alt15', P,
    'Duplicate guard row: see proj-alternatives.')
rows.pop()

counts = {'PASS': sum(1 for r in rows if r['status'] == 'PASS'), 'FAIL': sum(1 for r in rows if r['status'] == 'FAIL')}
fragment = {
    'unit': 'FC1',
    'slice': 'c',
    'round': 9,
    'verifier': 'Claude Haiku 5.5, independent verifier for FC1-c, round 9 (did not build FC1)',
    'pin': '1e272e5a641f18412703b37778a44db6f7391a69',
    'base': '2d755599d8d74df292e3e43025f0458c4053802e (round-8 pin of this slice)',
    'checkout': str(ROOT),
    'scratch': f'{S}/ (labs_r9.py, numbers_r9.py, cards_cites_r9.py, make_mutants_r9.py, run_alts_r9.sh, run_alts_fixed_r9.sh, build_fragment_r9.py; proposed fix ledgers/FC1/scripts/FC1-c-r9/proposed_fix_test_project_r9.py, not applied)',
    'verified_at': datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    'verdict': 'FAIL',
    'rows': rows,
    'mutants': mutants,
    'registry_flags': [
        'harris2002trading: registry year 2002 (references/references.json line 11536 onward, crossref); curriculum/02-economics-finance-core.yaml line 385 says (2003). The project page cites the key only. For the curriculum owner.',
        'mishkin2021economics: registry year 2021 (references/references.json line 17488 onward, openlibrary); curriculum line 384 says 13th ed. (2022). Not checked online (offline only). The project page cites the key only. For the curriculum owner.',
        'notation: plain Q (volume of a closed sequence, L03 Definition 2.1 and FC1-c131) is not the registry symbol \\mathbb{Q} (a probability measure, AP1). Not a reuse of the registry symbol; noted for the notation owner.',
    ],
    'freshness_flags': [],
    'notes': [
        f'Round 9 on 1e272e5. Delta from 2d75559 (git diff) in this slice: project.html (lines 106, 163, 171), grader/test_project.py (docstrings at 693, 806, 822; new tests 849-878; wrapper at 881-884), cards.json (changed FC1-c005, c008, c009, c041, c049, c071, c073; added FC1-c143 to c152), mutants/c2n01 (docstring), plus the four r8c mutants that the pin adds (ledgers/FC1/mutants/r8c_*.py), and the docstring of c2n01 changed. Labs, reference.py, instance.py, starter.py and the alternatives are byte-identical to 2d75559 except as stated; all were re-run this round.',
        'The round-8 fragment described the cards delta as c139-c142 added and c134 removed; the actual git diff 2d755599..1e272e5a shows c143-c152 added and no removal. c134 is absent in both pins (an id gap, not a removal in this delta). The round-8 description is not relied on.',
        'Mutants: 124 files (120 earlier plus 4 new r9c). tools/mutate_graders.py --unit FC1 --seeds 0-19: 120 killed, 4 survive (all four are r9c). All 120 earlier mutants are killed, including the three round-8 survivors (now killed by the 5001-period, 5001-settlement and 200000-bps tests).',
        'Alternatives: a1-a5, alt6-alt12, alt13-alt15 each pass the suite on seeds 0-19 (out/alternatives_0_19_r9.out) and all 15 pass the proposed fixed suite (out/alternatives_fixed_suite_r9.out).',
        'Test count: 82 collected (out/collect_only_r9.out) equals project.html line 171 "82 checks".',
        'The proposed fix (scratch only, not applied; verifier rule: report, do not fix) adds four accepted-input tests: yield 10**6 bps (price 104), 100001 periods (events only), settlement period 10**6, quantity 10**30. On it, the reference passes 86/86 and each of the four r9c mutants fails (1 failed each, seed 0).',
        'Labs: the page code equals each twin except Lab 2 blanks (Architect ruling 11); twins pass under python -I -W error; expected blocks equal output for Labs 1-3.',
        'Numbers: every number in project.html prose, the Lab 1-3 expected blocks, the grader docstrings and the card backs was re-derived with exact Fractions or read off a lab output (out/numbers_r9.out, out/labs_r9.out, out/lab_L0x.out).',
        'Lessons L01-L05 were not in this slice; their text was regenerated from the checkout (ledgers/FC1/scripts/FC1-c-r9/lessons_text/) and read only as far as the cards and project page cite them.',
        'Could not check: the deployed site (no deploy config; proj-reference-deployment); live Crossref and publisher checks (offline only, no network); the full repository pytest (only -k FC1); a Pyodide run of the proposed-fix tests (local pytest only); a browser run of the r9c mutants; the Pyodide CDN runtime (not learner data); hours are design targets (Architect ruling); the full text of every T-graded lesson proof (only the cited statements were read).',
    ],
    'summary': {
        'rows': len(rows),
        'pass': counts['PASS'],
        'fail': counts['FAIL'],
        'unverifiable': 0,
        'mutants_killed': sum(1 for m in mutants if m['killed_by']),
        'mutants': len(mutants),
    },
}
out = ROOT / 'ledgers/FC1/FC1-c.json'
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('rows', len(rows), counts, 'mutants', len(mutants))
