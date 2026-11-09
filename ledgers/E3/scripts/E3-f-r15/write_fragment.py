import json, sys, datetime
root = sys.argv[1]
prev = json.load(open('/Users/billyribeiro/.fanout/frags/D-E3-f.round14.json'))
prev_rows = {r['id']: r for r in prev['rows']}
cards = {c['id']: c for c in json.load(open(f'{root}/course/modules/E/E3/cards.json', encoding='utf-8'))}
rows = []
def add(id_, check, location, status, evidence, fix=None):
    r = {'id': id_, 'check': check, 'location': location, 'status': status, 'evidence': evidence}
    if status != 'PASS':
        r['fix'] = fix
    rows.append(r)

CARRY = 'Carried from round 14 (cards.json card object and its cited lesson block byte-identical since 1431aa1d): '
R15 = 'Re-verified in round 15 at pin dde0486b: '

# ---- commands (re-run this round)
add('E3f-cmd-check_pages', '2.9-structure', 'tools/check_pages.py --unit E3', 'PASS',
    'Round 15 output ledgers/E3/scripts/E3-f-r15/out/check_pages_unit.out: "check_pages E3: PASS".')
add('E3f-cmd-check_dag', '2.9-define-before-use', 'tools/check_dag.py --unit E3', 'PASS',
    'Round 15 output out/check_dag_unit.out: "check_dag E3: PASS".')
add('E3f-cmd-check_projects', '2.6-projects', 'tools/check_projects.py --unit E3', 'PASS',
    'Round 15 output out/check_projects_unit.out: "check_projects E3: PASS" (project slice owns the content).')
add('E3f-cmd-page_smoke', '2.9-structure', 'tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04 (run alone)', 'PASS',
    'Round 15 output out/page_smoke.out: "page_smoke modules/E/E3/L04.html: PASS" and "page_smoke E3: PASS"; the gate script ran it as one command, sequentially, with no other gate in parallel.')
add('E3f-cmd-pytest-labs', '2.5-labs', "pytest -q tests -k 'E3 or lab'", 'PASS',
    'Round 15 out/pytest_e3.out: all dots, 100 percent, rc=0 (out/_rc.txt "pytest_e3 rc=0").')
add('E3f-cmd-pytest-cards-notation', '2.5-labs', "pytest -q tests -k 'card or notation or review or concept'", 'PASS',
    'Round 15 run in checkout: six dots, no failure, exit status 0.')
add('E3f-cmd-ruff-labs', '2.5-labs', 'ruff check tests/labs/E3 course/modules/E/E3/grader; ruff format --check tests/labs/E3', 'PASS',
    'Round 15 out/ruff_check.out "All checks passed!"; out/ruff_format.out "11 files already formatted" (rc=0 both).')
add('E3f-cmd-mypy-twins', '2.5-labs', 'mypy --no-incremental (repository configuration)', 'PASS',
    'Round 15 out/mypy.out: "Success: no issues found in 385 source files" (rc=0).')
add('E3f-cmd-verify_refs', '2.1-citations', 'tools/verify_refs.py --offline', 'PASS',
    'Round 15 out/verify_refs_offline.out: "offline integrity: 560 entries, 0 problems" (rc=0). Live E3 re-check not repeated: references/, notation/ and tools/ are byte-identical across the delta (git diff --stat empty).')
add('E3f-cmd-build_site-render', '2.9-structure', 'tools/build_site.py --check; tools/render_curriculum.py; git diff --stat -- CURRICULUM.md curriculum/curriculum.json', 'PASS',
    'Round 15 out/build_site_check.out "site data current: 6 outputs"; out/render_curriculum.out regenerated identical bytes; out/render_diff.out empty (no tracked change).')
add('E3f-cmd-pytest-docs', '2.1-citations', 'pytest tests/test_docs_figures.py tests/test_refs.py', 'PASS',
    'Round 15 out/pytest_docs.out: all dots, rc=0.')
add('E3f-cmd-run_labs-L01-L04', '2.5-labs', 'tools/run_labs.py --unit E3 --page L01..L04', 'PASS',
    'Round 15 out/run_labs_L01..L04.out: each "run_labs E3: PASS (1/1)" (rc=0).')
add('E3f-cmd-fetch_data', '2.5-labs', 'tools/fetch_data.py --check', 'PASS',
    'Round 15 out/fetch_data_check.out: "fetch_data: 3 datasets, 0 problems" (rc=0).')
add('E3f-cmd-grader-not-in-slice', '2.11-grader', 'course/modules/E/E3/grader/* and tests/labs/E3/lab-E3-project-*.py', 'PASS',
    'No project grader is in slice f. The grader files changed in the delta (grader/reference.py, grader/test_project.py) belong to the project slice; run_graders and mutate_graders were not run here and no mutant is claimed.')

# ---- twins and labs
add('E3f-lab-twin-equality', '2.5-labs', 'course/modules/E/E3/L01..L04.html lab blocks vs tests/labs/E3/lab-E3-L0{1..4}-1.py', 'PASS',
    'ledgers/E3/scripts/E3-f-r15/out/check_twin_equality.out: for L01-L04 page_code_equals_twin=True, expected_equals_stdout=True, rc=0, stderr empty under python -I -W error.')
add('E3f-lab-L01', '2.5-labs', 'course/modules/E/E3/L01.html lab block; tests/labs/E3/lab-E3-L01-1.py (changed in the delta)', 'PASS',
    R15 + 'twin renamed to rho, u_tilde and order_tilde; page code equals twin byte for byte; expected block equals stdout of the twin under python -I -W error (rc 0). Lines checked: "rho 1/3 utility quadratic mixture_eu 40000 linear_combination 40000 equal True" (E2 quotes it), six "equal True" lines (card E3-c017), Part C six "same True" lines, all_affine_orders_preserved True. The twin states and uses no random draws (docstring line 15), and imports only typing, collections.abc and fractions.')
add('E3f-lab-L02', '2.5-labs', 'course/modules/E/E3/L02.html lab block; tests/labs/E3/lab-E3-L02-1.py (twin unchanged)', 'PASS',
    R15 + 'page code equals twin and expected block equals stdout (check_twin_equality.out). Lab printed values unchanged by the delta.')
add('E3f-lab-L03', '2.5-labs', 'course/modules/E/E3/L03.html lab block; tests/labs/E3/lab-E3-L03-1.py (twin unchanged)', 'PASS',
    R15 + 'page code equals twin and expected block equals stdout (check_twin_equality.out).')
add('E3f-lab-L04', '2.5-labs', 'course/modules/E/E3/L04.html lab block; tests/labs/E3/lab-E3-L04-1.py (twin unchanged)', 'PASS',
    R15 + 'page code equals twin and expected block equals stdout (check_twin_equality.out).')

# ---- numbers
add('E3f-lesson-numbers-L01', '2.2-numbers', 'course/modules/E/E3/L01.html (Definition 2.1 and later numbers; M3; E2; R3; quiz)', 'PASS',
    R15 + 'ledgers/E3/scripts/E3-f-r15/out/check_L01_L02_numbers.out re-derives 150, 45000, 59, 4030, 50, 175, 37500, 25000, 22500, 5/12. Hand check of changed M3: E X=20, E Y=30; under tilde u=5+3x, tilde u(10)=35, tilde u(30)=95, E tilde u(X)=65=5+3*20, E tilde u(Y)=95=5+3*30. Lab values 40000 (E2) and the six True lines match the output.')
add('E3f-lesson-numbers-L02', '2.2-numbers', 'course/modules/E/E3/L02.html (Example 2.3, Section 3, Lab 1 interpretation, misconception, E1-E3, quiz)', 'PASS',
    R15 + 'out/check_L01_L02_numbers.out: sqrt sum 9.743416, CE 94.934165 (squaring printed 9.743416 gives 94.934155), premium 5.065835, 11.17 percent of exact premium (0.11169629), 12.57 percent of approximation, eps=0.01 premium over eps^2 4.500046, gap 0.000046, E1 ratio 6.31, var 1800, r_A(100)=0.005.')
add('E3f-lesson-numbers-L03', '2.2-numbers', 'course/modules/E/E3/L03.html (Example 2.5, Lab 1 prints, Remark 2.8, E2, M1-M3)', 'PASS',
    R15 + 'out/check_L03_numbers.out: CE 11250.0000, 10931.7733, 10615.8009, 10000.0000, 8888.8889, 7337.6161 (rounded 11250, 10932, 10616, 10000, 8889, 7338); 80000/9; Example 2.5 gamma 2 = 1600, gamma 1 = 2000; E1 10615.8009 -> 10616.')
add('E3f-lesson-numbers-L04', '2.2-numbers', 'course/modules/E/E3/L04.html (Lemma 1.2, Examples 1.7, 2.5, 2.6, misconceptions, M1-M3, E1-E2, R1, lab named pairs)', 'PASS',
    R15 + 'out/check_L04_theorems.out re-run (400 pairs, 36 equal-mean pairs); the L04 change is a quiz distractor only, so all carried numbers are byte-identical.')
add('E3f-r14-L04-theorems', '2.4-mathematics', 'course/modules/E/E3/L04.html Theorem 1.5, Lemma 1.6, Proposition 1.8, Lemma 2.2, Theorem 2.3, Remark 2.4', 'PASS',
    R15 + 'out/check_L04_theorems.out: 0 proven FOSD dominances refuted, 0 proven SOSD refuted, 0 support-point vs grid disagreements on 36 equal-mean pairs. The converse of Theorem 1.5 is now checked exactly: ledgers/E3/scripts/E3-f-r15/check_L04_converse.py (out/check_L04_converse.out) finds 317 of 317 non-dominance pairs (F_X(t) > F_Y(t) for some t) refuted by the nondecreasing utility 1{x > t}, which gives E u(X) = 1 - F_X(t) < 1 - F_Y(t) = E u(Y). The round-14 claim "four converse-sample cases resolved" is not reproduced by the old script (its two loops draw different samples, and the second found 2 cases); it is superseded by this exact check.')

# ---- mathematics
add('E3f-r14-L02-prop31-proof', '2.4-mathematics', 'course/modules/E/E3/L02.html:199 (Proposition 3.1 proof, last sentence)', 'PASS',
    R15 + 'the round-14 FAIL is fixed. Line 199 now reads "Hence z(eps) -> (1/2) u\'\'(w) s^2 / (-u\'(w)) = (1/2) r_A(w) s^2"; z(eps) = pi(eps)/eps^2 is defined on line 195. grep finds 0 occurrences of q(eps) in L02.html. The rest of the proof was re-derived (Step 3 identity and limit).')
add('E3f-r14-L02-prop31-limit', '2.4-mathematics', 'course/modules/E/E3/L02.html:173-199 (Proposition 3.1) and Remark 3.2', 'PASS',
    R15 + 'the statement is unchanged; the limit -u\'\' / u\' and the factor 1/2 re-derived; numerical limit 4.5000 and gap rows in out/check_L01_L02_numbers.out.')
add('E3f-r14-L01-proofs', '2.4-mathematics', 'course/modules/E/E3/L01.html Propositions 2.2, 2.3, 3.1, 3.3 and Problems P1, P2, P3, R1, R3', 'PASS',
    R15 + 'changed hunks re-read and re-derived: Prop 2.2 and its proof (weights non-negative, sum to 1 with rho); Prop 2.3 proof (finite split); Prop 3.3 proof (E tilde u(L) - E tilde u(M) = b(E u(L) - E u(M))); P1 (weight on x is rho); P2 (b<0 reverses); P3 (countable counterexample 2^i, 2^-i unchanged); R3 values 25000 and 22500. Unchanged: Prop 3.1, R1.')
add('E3f-r14-L02-proofs', '2.4-mathematics', 'course/modules/E/E3/L02.html Proposition 1.1, 1.3 (a)(b), 2.2, Example 2.3, Problems P1-P3, R1-R3', 'PASS',
    R15 + 'Prop 2.2 (tilde u, r_A^{tilde u} = r_A^u since b cancels), Example 2.3 (r_A = 1/(2w), r_R = 1/2, tilde u = -2 + 2u with b = 2 > 0), quiz q7 (e^u gives r_A^u - u\'), P1 solution (r_R = nu w; tilde u = 5 + 2u) re-derived. Carried from round 14 for the unchanged Prop 1.1, 1.3, P2, P3, R1-R3 (byte-identical since 1431aa1d).')
add('E3f-r14-L03-proofs', '2.4-mathematics', 'course/modules/E/E3/L03.html Propositions 1.2, 1.4, 1.7, 2.4, 2.6, 2.7, Theorem 2.1, Remark 2.8, Problems R1, P1-P3', 'PASS',
    R15 + 'mathematics re-derived for the changed hunks: Thm 2.1 proof (g = ln u\' + gamma ln w constant; u\' = K w^-gamma; (u - K u_gamma)\' = 0); Prop 2.7 and P1 (phi u(c) + varsigma = phi E u(X) + varsigma gives u(c) = E u(X)). The mathematics is correct; the symbol clash in the Theorem 2.1 proof is a separate FAIL row (E3f-r15-notation-tilde-L03). Carried for the unchanged Prop 1.2, 1.4, 1.7, 2.4, 2.6, Remark 2.8, R1, P1-P3 (byte-identical).')
add('E3f-r14-L04-proofs', '2.4-mathematics', 'course/modules/E/E3/L04.html Problems P1-P3, R1-R3 and Example 2.6', 'PASS',
    CARRY + 'the delta changes only the quiz option L04q4 (line 666); the proofs and example are byte-identical. The new distractor "Nonincreasing utilities with u\'\' >= 0" is wrong because it is nonincreasing; the correct option (nondecreasing concave on S) matches Theorem 2.3.')

# ---- notation
add('E3f-notation', '2.13-notation', 'course/modules/E/E3/L01.html-L04.html vs notation/notation.json', 'PASS',
    R15 + 'no raw \\mathbb in L01-L04 (grep count 0); only \\E and \\R are used from the registry; registry symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q do not occur in L01-L04 (scan: 0 hits for \\mathrm{T}, T =, \\Phi, R_f, \\mathbb{Q}, \\gamma_3, R^\\ast, R^{e). notation/ is unchanged in the delta.')
add('E3f-notation-kappa', '2.13-notation', 'course/modules/E/E3/L02.html (M3, P1, quiz); cards.json', 'PASS',
    R15 + 'no kappa in L01-L04 pages or in any card (scan of cards.json: 0 hits).')
add('E3f-notation-alpha', '2.13-notation', 'course/modules/E/E3/L01.html; lab-E3-L01-1.py; cards c005-c017', 'PASS',
    R15 + 'no alpha in L01, its twin or cards E3-c005..c017 (scan). L02 F6 uses alpha as a real exponent, the same meaning as the power exponent of L06 Definition 1.2.')
add('E3f-r14-notation-tau', '2.13-notation', 'course/modules/E/E3/L01.html Definition 2.1 (mixture weight, now rho); L08 Definition 1.2 (tau)', 'PASS',
    R15 + 'the L01 mixture weight is now rho: 0 uses of tau in L01, its twin and cards c005-c017; rho occurs only in L01 (50 uses), its twin (15) and cards E3-c005, c007, c008, c017. tau now has one meaning in E3 (L08 ambiguity weight, 37 uses). Resolved.')
add('E3f-r14-notation-eps', '2.13-notation', 'course/modules/E/E3/L02.html Section 3 (varepsilon, 91 uses) vs course/modules/E/E3/L05.html Definition 2.1 and card E3-c083', 'PASS',
    R15 + 'L05 no longer uses varepsilon (symbol scan: 0 uses in L05); the EIS is now written EIS := d ln(c1/c0)/d ln MRS and EIS = psi in Proposition 2.2 (L05.html lines 107, 116, 119; card E3-c083 matches). varepsilon now has one meaning in E3 (the gamble scale). Resolved. Caveat for the L05 slice: ruling 29 asked for psi; the page writes the acronym EIS as the symbol and equates it with psi.')
add('E3f-r14-notation-eta', '2.13-notation', 'course/modules/E/E3/L03.html Proposition 2.7 and proof (now varsigma); course/modules/E/E3/L07.html (eta, 24 uses)', 'PASS',
    R15 + 'L03 has no eta (varsigma occurs only in L03, 9 uses, and cards E3-c049); eta now occurs only in L07 (weighting parameter, 24 uses). Resolved.')
add('E3f-r15-notation-tilde-L03', '2.13-notation', 'course/modules/E/E3/L03.html Theorem 2.1 proof (line 131-134: "Let \\tilde u = K u_gamma" and the lines that use it) vs L03.html Proposition 2.7 (line 174), its proof (line 179) and P1 solution (line 393)', 'FAIL',
    'In one lesson the symbol \\tilde u names two different objects: in the Theorem 2.1 proof it is K u_gamma (a positive multiple of the CRRA utility), and in Proposition 2.7 and P1 it is phi u + varsigma (a generic affine transform of u). The round-14 rename of v to \\tilde u (ruling 29) created this reuse. Rule: one meaning per symbol across the unit (BUILDER_RULES 2.1 item 7; notation registry "never takes another meaning").',
    'In course/modules/E/E3/L03.html, rename the Theorem 2.1 proof\'s \\tilde u (the paragraph at about line 134) to \\check u: a scan of E3 finds 0 uses of \\check (\\hat is used 3 times in project.html, so it is not free). Keep \\tilde u for Proposition 2.7 and P1. Nothing else in the proof changes.')
add('E3f-r15-notation-cross-lesson', '2.13-notation', 'E3 symbols used in L01-L04 and in other lessons (nu, alpha, gamma, psi, delta, lambda, beta, rho, varsigma, tilde u)', 'PASS',
    R15 + 'symbol scan (ledgers/E3/scripts/E3-f-r15/symscan.py): nu in L02 (exponential coefficient, P1 constant r_A) and L08 Problem set line 598 (u = -e^{-nu w}): same meaning; alpha in L02 F6 and L06/L07 (exponents): same meaning; gamma in L03 (CRRA), L05 and L08 (risk aversion): same meaning; psi in L05 and L08 (EIS parameter, a = 1 - 1/psi): same meaning; delta and lambda in L06 and L08 Model 2 (prospect parameters): same meaning; beta in L05 and L08 (discount factor): same meaning; rho, varsigma each used in one lesson only; tilde u in L01-L02 is always an affine transform of u (the L03 clash is its own FAIL row).')

# ---- DAG and prose
add('E3f-dag-L02-crra-forward-use', '2.9-define-before-use', 'course/modules/E/E3/L02.html; L03.html; L04.html (concept links and forward uses)', 'PASS',
    R15 + 'check_dag E3 PASS; the delta adds no concept link, and no new term outside the closure (the only "convexity" in L02 is the A2 sentence that defines concavity by u\'\'). Forward references unchanged.')
add('E3f-dag-other-links', '2.9-define-before-use', 'course/modules/E/E3/L01.html-L04.html (Uses and Introduces lines; concept links)', 'PASS',
    R15 + 'no concept link added or removed in L01-L04 by the delta; check_dag PASS.')
add('E3f-banned-and-process', '1.3-1.4-banned', 'course/modules/E/E3/L01.html-L04.html (visible prose)', 'PASS',
    R15 + 'ledgers/E3/scripts/E3-f-r15/banned_scan.py: no TODO, TBD, lorem, "for brevity", "beyond the scope", "obviously", "clearly", builder, verifier, REQUESTS. Six benign hits: two "concavity or convexity" in the L02 A2 definition sentence; three "round" and one "this unit reports it in whole cents" describing the rounding convention (not process words).')
add('E3f-banned-cards', '1.3-1.4-banned', 'course/modules/E/E3/cards.json', 'PASS',
    R15 + 'banned_scan.py over all 178 cards: no hits.')
add('E3f-hours', '2.12-hours', 'course/modules/E/E3/L01.html..L04.html data-hours; index.html hub split', 'PASS',
    R15 + 'data-hours="7" in each of L01-L04; no data-hours attribute changed in the delta (index.html delta touches prose only); check_pages PASS.')

# ---- references
add('E3f-references', '2.1-citations', 'course/modules/E/E3/L02.html:616 (pratt1964risk); references/references.json', 'PASS',
    CARRY + 'the L02 references paragraph (line 616) and references/ are byte-identical; verify_refs offline 0 problems.')
add('E3f-L03-references', '2.1-citations', 'course/modules/E/E3/L03.html:564 (references paragraph); course/modules/M/M1/L03.html', 'PASS',
    CARRY + 'the L03 references paragraph is not in the delta; references/ unchanged.')

# ---- cards: global
add('E3f-cards-integrity', '2.10-cards', 'course/modules/E/E3/cards.json (178 cards)', 'PASS',
    R15 + 'check_cards_structure.py: 178 cards, 178 distinct ids, id format ok; c188 (L03) added; the cards for L01-L04 are 91; lessons L01 18, L02 22, L03 27 (incl. c188), L04 24, L05 22, L06 19, L07 18, L08 28. Grade-C cards without basis are c134, c157, c158, which carry a registry cite (BUILDER_RULES 7 allows cite instead of basis; check_pages accepts them). No cited key is missing from the registry.')
add('E3f-cards-near-duplicates', '2.10-cards', 'course/modules/E/E3/cards.json (full pairwise scan of changed cards)', 'PASS',
    R15 + 'ledgers/E3/scripts/E3-f-r15/out/near_dup.out: the only pair above 0.7 among changed cards is E3-c037 / E3-c188 (front 0.74-0.76, back 0.67): c037 is the powers-of-powers rule (w^a)^b = w^(ab), c188 the product rule (xy)^c = x^c y^c of the same Proposition 1.2; distinct facts, not duplicates. Full check_cards_structure near-duplicate list was run; the pre-existing pairs are unchanged.')
add('E3f-cards-xrefs', '2.10-cards', 'course/modules/E/E3/cards.json (Definition, Proposition, Example, Remark, Problem and Assumption locators)', 'PASS',
    R15 + 'check_cards_structure flags "locator not found" for E3-c055 (L03 "Problem E2") and E3-c187 (L07 "Problem E2"). Both targets exist: L03.html line 422 "E2 · Checking the exact gamma 2 value" and L07.html line 409 id="E2". These are checker format flags, not wrong locators.')
add('E3f-cards-numbers', '2.2-numbers', 'course/modules/E/E3/cards.json (numbers in card backs)', 'PASS',
    R15 + 'ledgers/E3/scripts/E3-f-r15/check_cards_numbers.py re-run: c123 2*omega(3/10)=0.5715817698, c125 ratio 0.7304544982 vs thresholds 2/3 and 0.5857864376, c127 Gamma(A) 42.8686 and Gamma(B) 39.1251 (alpha 1), 4.8788 and 3.9125 (alpha 1/2), c132 49.8328 vs 50.5, c187 unrounded difference 3.7435557 (rounds to 3.7436), c149-c152, c166, c096 CE1 2.25, 1.6, 1.3720, c095 U and V0, c116 threshold 1.2910 and W = -8.6835, c113 lambda_R = sqrt(2)/2; all match the cards.')
add('E3f-cards-grades', '2.10-cards', 'course/modules/E/E3/cards.json E3-c106 (now grade T, basis "Example 2.3") vs course/modules/E/E3/L06.html Example 2.3, Proposition 2.1', 'PASS',
    R15 + 'round-14 FAIL (grade C) is resolved. The three values follow by substitution into Proposition 2.1 (alpha = delta = 1): W(lambda) = p g - (1-p) lambda l = 500 - 300 lambda, so W(1) = 200 = EV, W(3/2) = 50, W(2) = -100, and lambda* = pg/((1-p)l) = 5/3. Proposition 2.1 is graded T and proved on the page. Recommendation (LOW, not a FAIL): cite Proposition 2.1 as the basis, since Example 2.3 only states the values.')
add('E3f-cards-slice-scan', '2.10-cards', 'course/modules/E/E3/cards.json, all 91 cards of L01-L04', 'PASS',
    R15 + 'all 91 L01-L04 cards were read this round (ledgers/E3/scripts/E3-f-r15/out/cards_L01_L04.txt); the changed ones are re-verified below, the rest are carried from round 14 under the byte-identical rule.')
add('E3f-coverage-cards', '2.10-cards', 'course/modules/E/E3/L01.html-L04.html (labelled Definition, Proposition, Theorem, Lemma, Remark, Example blocks)', 'PASS',
    CARRY + 'no labelled block was added or removed in L01-L04 by the delta (the diff changes text only); card E3-c188 adds coverage of the product rule of Proposition 1.2.')
add('E3f-E3-r7-independent-rederivation', '2.4-mathematics', 'ledgers/E3/scripts/E3-f-r15/*.py', 'PASS',
    R15 + 'independent rederivation scripts run on the pin: check_L01_L02_numbers.py, check_L03_numbers.py, check_L04_theorems.py, check_L04_converse.py, check_cards_numbers.py (outputs in out/).')
add('E3f-r15-delta', '2.4-mathematics', 'git diff 1431aa1d..dde0486b: L01-L04 pages, lab-E3-L01-1.py, cards.json, plans/FINAL-ARCHITECT-RULINGS.md ruling 29', 'PASS',
    R15 + 'every hunk in L01-L04 (about 200 changed lines) and in cards.json (the 16 changed cards, the new card c188, and the L05-L08 card hunks) was read; hunks are classified as re-verified or carried in the rows of this fragment. Hunks in L05-L08 pages, grader/, project.html and index.html belong to other slices and are cited only where a card or a notation row depends on them.')

# ---- cards L01-L04 individual rows
RE = {'E3-c005','E3-c007','E3-c008','E3-c009','E3-c011','E3-c012','E3-c017','E3-c025','E3-c026','E3-c027','E3-c028','E3-c029','E3-c030','E3-c037','E3-c043','E3-c049','E3-c052','E3-c173','E3-c188'}
RE_EV = {
 'E3-c005': 'mixture definition (Definition 2.1, rho) matches the card front and back.',
 'E3-c007': 'Proposition 2.2 (rho in [0,1]) matches the card; weights non-negative and sum to one.',
 'E3-c008': 'Proposition 2.3 with rho; the displayed identity matches the card.',
 'E3-c009': 'Proposition 2.3 is still an identity about the formula of Definition 1.3; Remark 2.4 unchanged.',
 'E3-c011': 'Proposition 3.3 with tilde u = a + b u, b > 0: the card claim holds (E tilde u(L) = a + b E u(L)).',
 'E3-c012': 'Problem P2 solution: b < 0 reverses the ranking; the card claim matches.',
 'E3-c017': 'Part B of Lab 1: three rho values x two utilities = six lines, all "equal True" in the expected block.',
 'E3-c025': 'Proposition 2.2 with tilde u; the b cancels in r_A; matches the card.',
 'E3-c026': 'Example 2.3: r_A = 1/(2w), r_R = 1/2, r_A(100)=0.005 (script check_L01_L02_numbers.out); text changed only by the tilde rename.',
 'E3-c027': 'Proposition 3.1 statement unchanged; proof now uses z(eps) consistently (L02.html line 199 fixed).',
 'E3-c028': 'Remark 3.2 unchanged; the asymptotic-only statement matches the card.',
 'E3-c029': 'variance 1800, half-variance 900, Pratt limit 4.5 (script out check_L01_L02_numbers.out: limit 4.5000).',
 'E3-c030': 'Definition 2.1 and Example 2.3: r_A = 0.005 per CU and r_R = 0.5 at w = 100.',
 'E3-c037': 'Proposition 1.2 (powers of powers): (w^a)^b = w^(ab) for w>0, real a, b; the card states this exactly.',
 'E3-c043': 'Theorem 2.1 statement (A3, A4) unchanged; u = K u_gamma + C with K > 0 matches the card (the proof was re-read; see the notation FAIL row).',
 'E3-c049': 'Proposition 2.7 with phi > 0 and varsigma real: the card names the same constant, and the proof conclusion matches.',
 'E3-c052': 'L01 Proposition 3.3 with a positive affine transform (b=1 for u_0 = w - 1): ranking preserved; matches the card.',
 'E3-c173': 'Definition: b = 0 gives E tilde u(L) = a for every lottery, so every pair ties (section 5, third misconception).',
 'E3-c188': 'new card: Proposition 1.2 second claim (xy)^c = x^c y^c for positive x, y and real c; statement matches the lesson.',
}
for cid in sorted(cards):
    if cards[cid]['lesson'] not in ('L01','L02','L03','L04'):
        continue
    rid = 'E3f-E3-' + cid.split('-')[1]
    if cid in RE:
        add(rid, '2.9-cards', f'course/modules/E/E3/cards.json ({cid}); course/modules/E/E3/{cards[cid]["lesson"]}.html', 'PASS',
            R15 + RE_EV[cid])
    else:
        if rid in prev_rows and prev_rows[rid]['status'] == 'PASS':
            add(rid, prev_rows[rid]['check'], prev_rows[rid]['location'], 'PASS', CARRY + prev_rows[rid]['evidence'])
        else:
            raise SystemExit('missing previous PASS row for ' + cid)

# ---- cards L05-L08: sampled and unsampled
add('E3f-r14-cards-sample-L05', '2.10-cards', 'cards.json E3-c078, c084, c085, c086, c087, c089, c091, c094, c095, c169, c170, c184, c185 vs L05.html', 'PASS',
    R15 + 'c084, c085, c091, c184 (Prop 2.2 statement unchanged, proof wording changed to EIS = psi): re-verified; c094 and c184 lab values in the expected block (EIS estimates 0.5000, 2.0000, 0.2500; MRS True); c095 (U(4,4) = -0.25, U(1,10) = -0.55, V0 = 4.0 and 4.3311) by script; c169 (U = -49/80) and c170 (CE1 = 8/5) and c185 (mean 5/2) by hand. c078, c086, c087, c089 carried from round 14 (blocks byte-identical).')
add('E3f-r14-cards-sample-L06', '2.10-cards', 'cards.json E3-c102, c104, c105, c107, c108, c110, c111, c112, c113, c116, c117 vs L06.html', 'PASS',
    R15 + 'c101, c106, c111, c112, c113, c117 re-verified against the changed L06 text (Proposition 1.4, Example 2.3, Remark 3.2, misconception 1, lab hypothesis). c102, c104, c105, c107, c108, c110 and c116 carried (cited blocks byte-identical; the lab lines c116 quotes are unchanged).')
add('E3f-r14-cards-sample-L07', '2.10-cards', 'cards.json E3-c121, c122, c123, c124, c125, c126, c127, c128, c132, c133, c135, c187 vs L07.html', 'PASS',
    R15 + 'c123 and c130 re-verified against the changed Remark 1.6 (0.57158177 vs 0.39125077, weights need not sum to one). c121 (omega closed form and values 0.28579088, 0.39125077, 0.35355339 recomputed), c125 (threshold 2/3 and 0.58578644; ratio 0.73045450), c126 (60 vs 45), c124 (F_A(50)=7/10, F_B(50)=2/5) re-derived. c122, c127, c128, c132, c133, c135, c187 carried (cited blocks and lab lines unchanged; c187 difference 3.7435557 rounds to 3.7436).')
add('E3f-r14-cards-sample-L08', '2.10-cards', 'cards.json E3-c137, c138, c139, c141, c142, c143, c144, c148, c149, c150, c151, c152, c153, c155, c164, c165, c166, c172, c179, c182 vs L08.html', 'PASS',
    R15 + 'L08 blocks cited by these cards are byte-identical (the one changed L08 block is the section 6 first misconception, cited by card E3-c154). Carried from round 14; the numbers in c149-c152 and c166 were re-run by check_cards_numbers.py.')
add('E3f-r14-cards-unsampled', '2.10-cards', 'cards.json: the 29 L05-L08 cards not sampled in round 14 (c079, c080, c081, c082, c083, c088, c090, c093, c096, c098, c099, c100, c103, c109, c118, c119, c120, c129, c130, c134, c136, c140, c145, c146, c147, c154, c157, c158, c163)', 'PASS',
    R15 + 'all 29 were read this round against their cited blocks: c079 (Remark 1.2), c080 (Theorem 1.3), c081 (Corollary 1.4 and section 5 third misconception), c082 (Remark 1.5), c083 (Definition 2.1, changed to EIS), c088 (Corollary 3.3), c090 (Corollary 3.3, Remark 3.4), c093 (Problem E1: V0 = 80/49 recomputed), c096 (CE1 2.25, 1.6, 1.3720), c098-c100 and c103 (Definitions 1.1, 1.2, 1.3, 1.6), c109 and c163 (Remark 2.5), c118-c120 (Definitions 1.1, 1.2, Remark 1.3), c129 (Lesson 4 Theorem 1.5 direction), c130 (Remark 1.6, changed), c134, c157, c158 (registry titles: kahneman1979prospect "Prospect Theory: An Analysis of Decision under Risk" 1979; ellsberg1961risk "Risk, Ambiguity, and the Savage Axioms" 1961; gilboa1989maxmin "Maxmin expected utility with non-unique prior" 1989), c136 (Definition 1.1), c140 (Definition 2.1), c145 (Definition 3.1), c146 (Proposition 3.2, A1-A5), c147 (Remark 3.3), c154 (Proposition 2.4 A1-A3, changed misconception). All 29 match; the round-14 UNVERIFIABLE row is closed.')
add('E3f-r15-cards-changed-L05-L08', '2.10-cards', 'cards.json E3-c083, c101, c106, c117, c154 (changed text in L05-L08)', 'PASS',
    R15 + 'each changed L05-L08 card re-verified: c083 (EIS := d ln(c1/c0)/d ln MRS), c101 (Proposition 1.4: v\'\' < 0 on x>0, v\'\' >= 0 on x<0), c106 (see E3f-cards-grades), c117 (grid lines "gain part concave ... True; loss part with v\'\' >= 0 (midpoint test) ... True", increasing True, |v(-x)|/v(x) = 2 True), c154 (Proposition 2.4 with A1-A3; worst priors P_0 and P_90).')

summary = {
    'rows': len(rows),
    'pass': sum(1 for r in rows if r['status'] == 'PASS'),
    'fail': sum(1 for r in rows if r['status'] == 'FAIL'),
    'unverifiable': sum(1 for r in rows if r['status'] == 'UNVERIFIABLE'),
}
verdict = 'PASS' if summary['fail'] == 0 and summary['unverifiable'] == 0 else 'FAIL'
frag = {
    'unit': 'E3',
    'slice': 'f',
    'round': 15,
    'verifier': 'Claude Haiku 5.5, independent verifier for E3-f, round 15 (did not build E3)',
    'pin': 'dde0486beeb0312e4ac1cc03aaa02e56644adb24',
    'base': '1431aa1d842a5d2d05fd5953c098500bf78a4307 (round-14 pin); delta 1431aa1d..dde0486b',
    'checkout': '/Users/billyribeiro/.fanout/wt/verifyD15-E3-f',
    'scratch': 'ledgers/E3/scripts/E3-f-r15/',
    'verified_at': datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    'verdict': verdict,
    'rows': rows,
    'mutants': [],
    'registry_flags': [],
    'freshness_flags': [],
    'notes': [
        'Slice scope: L01-L04 pages, their lab twins, and all 178 cards of course/modules/E/E3/cards.json (91 of them are L01-L04). The project grader, project.html, index.html and the L05-L08 pages belong to other slices and are cited only where a card or a notation row depends on them.',
        'No project grader is in this slice, so no mutants are claimed (mutants: []). Lab twins are demonstrations (ruling for project graders only).',
        'Round-14 non-PASS rows: E3f-r14-L02-prop31-proof (fixed, PASS), E3f-cards-grades (fixed, PASS), E3f-r14-notation-tau / -eps / -eta (resolved, PASS), E3f-r14-cards-unsampled (verified, PASS). The round-14 converse evidence was not reproducible and is superseded by check_L04_converse.py.',
        'New FAIL: E3f-r15-notation-tilde-L03 (one symbol, two meanings, in the Theorem 2.1 proof and Proposition 2.7). Fix named in the row (rename the proof symbol to \\hat u).',
        'Ruling-29 compliance notes for other slices (not FAIL here): (a) L05 writes the EIS symbol as the acronym EIS and equates it with psi, where ruling 29 asked for psi; (b) psi is also used in L08 with the same meaning (EZ elasticity parameter), so it does not appear "nowhere else in E3" as ruling 29 wrote. Both belong to the L05/L08 slice verifiers.',
        'Card E3-c106 is now graded T with basis "Example 2.3"; the value follows from Proposition 2.1 by substitution. Suggested basis: Proposition 2.1 (LOW).',
        'Not checked: the full text of L05-L08 pages (only the changed hunks and the blocks cited by cards); verify_refs --live for E3 (references/ unchanged); run_graders and mutate_graders (no grader in slice); the Pratt, Ellsberg, Gilboa-Schmeidler and Kahneman-Tversky papers themselves (registry records only, by design of the cards); the hub prose changes in index.html (other slice).',
        'Working-tree note: the checkout has untracked ledger scripts and the .venv symlink; no tracked file was edited (render_curriculum rewrote identical bytes; git diff --stat empty for CURRICULUM.md and curriculum/curriculum.json).',
    ],
    'summary': summary,
}
out = f'{root}/ledgers/E3/E3-f.json'
json.dump(frag, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('wrote', out, summary, verdict)
