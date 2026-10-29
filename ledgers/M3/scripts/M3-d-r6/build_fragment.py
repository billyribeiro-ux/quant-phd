import json, re, datetime, pathlib
S = 'ledgers/M3/scripts/M3-d-r6/'
mut_lines = [l for l in open(S + 'mutate_M3_0-49_r6.out', encoding='utf-8') if re.match(r'^(KILLED|SURVIVED) ', l)]
mutants = []
for l in mut_lines:
    m = re.match(r'^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$', l.rstrip('\n'))
    status, name, desc, killed = m.group(1), m.group(2), m.group(3), m.group(4)
    if status == 'KILLED':
        killed_by = killed.strip()
    else:
        killed_by = None
    mutants.append({'name': name, 'description': desc, 'killed_by': killed_by,
                    'note': ('Survived all seeds 0-49. Not a FAIL: page.html Exemplar B states the suite checks the result, not the stopping rule, and no contract sentence states the stopping rule. See notes.' if killed_by is None else '')})
for m in mutants:
    if not m['note']:
        del m['note']
PASS = 'PASS'
rows = []
def row(i, check, loc, status, evidence, fix=None):
    r = {'id': i, 'check': check, 'location': loc, 'status': status, 'evidence': evidence}
    if status != PASS:
        r['fix'] = fix
    rows.append(r)
row('M3-d-R01', 'Lab 1 (project rung 1): twin output equals page expected block; page code equals twin',
    'course/modules/M/M3/project.html section#lab-M3-project-1; tests/labs/M3/lab-M3-project-1.py',
    PASS, 'python3 -I -W error tests/labs/M3/lab-M3-project-1.py exit 0; output saved as ledgers/M3/scripts/M3-d-r6/lab_p1.out; expected block and code compared programmatically (equal); tools/run_labs.py --unit M3 --page project: PASS 3/3 (scripts/M3-d-r6/run_labs_M3_project.out)')
row('M3-d-R02', 'Lab 2 (completion): blanks are the Step 3 comparison and Step 5 divisor; twin is the completed solution; twin output equals expected block',
    'project.html section#lab-M3-project-2 (blanks at Step 3 and Step 5); tests/labs/M3/lab-M3-project-2.py',
    PASS, 'Diff of page code against twin shows exactly the two blanks (smallest >= -1e-10 and math.sqrt(d[i]*d[j])); twin output scripts/M3-d-r6/lab_p2.out equals expected block; run_labs PASS')
row('M3-d-R03', 'Lab 3 printed numbers (eigenvalue, two distances, gap, entry difference, diagonal deviations, determinant, input weights)',
    'project.html section#lab-M3-project-3 expected block; tests/labs/M3/lab-M3-project-3.py',
    PASS, 'Twin output equals expected block and page code equals twin (programmatic compare, scripts/M3-d-r6/lab_p3.out). Independent numpy recomputation (scripts/M3-d-r6/indep_lab3.py): min eig -0.142113; clip dist 0.176573; proj dist 0.175003; gap 0.001570; entry diff 0.011516; weights 1.778929 -1.096718 -0.255613 0.573402; det -0.261600; diag dev 0')
row('M3-d-R04', 'Lab 3 hypothesis sentence (smallest eigenvalue negative; projection nearer by positive distance; diagonals within 5e-7; det nonzero; weights sum to 1)',
    'project.html Lab 3 p.hypothesis', PASS, 'Each clause checked against printed output scripts/M3-d-r6/lab_p3.out (min eig -0.142113 negative; gap 0.001570 > 0; diagonal deviations print 0.000000; det -0.261600; sum 1.000000)')
row('M3-d-R05', 'Lab 1 and Lab 2 interpretation prose numbers (rebuilt diagonals, repaired entries, verdicts, deviations)',
    'project.html p.interpretation after Lab 1 and Lab 2', PASS, 'Lab 1 rebuilt diagonal 1.096064 1.104409 1.074824, repaired 0.636095 -0.382551 0.469578 match scripts/M3-d-r6/lab_p1.out; Lab 2 rebuilt 1.060165 1.075224 1.068322 match lab_p2.out; "False" verdict for input in both match')
row('M3-d-R06', 'Lab 3 interpretation prose (distance gap, entry gap, sign pattern, A4 hypothesis not printed, Sigma invertibility by det Sigma = (prod v)^2 det C)',
    'project.html p.interpretation after Lab 3', PASS, 'Numbers match lab_p3.out; identity det(DCD) = (prod v_i)^2 det C checked algebraically; statement that Lab 3 prints no repair weights matches lab output; claim that A4 hypothesis is not printed is accurate (no diagonal-positivity line printed)')
row('M3-d-R07', 'Spec constants: 150 tests; PSD tolerances -1e-9 (clipping) and -1e-8 (projection); ValueError conditions named; 120 s browser limit',
    'project.html section#spec (Constraints, Grading mode, Conventions); grader/test_project.py; course/assets/js/python.js TIMEOUT_MS',
    PASS, 'pytest --collect-only: 150 tests collected (QF_SEED=0 run); test_clip_repair_is_positive_semidefinite uses -1e-9; test_projection_repair_is_a_valid_repair uses -1e-8; the four named conditions match the tests (non-square, asymmetry > 1e-9, volatility <= 0, length mismatch); python.js line 4 TIMEOUT_MS = 120000')
row('M3-d-R08', 'Convention and appendix math: clipping, rescaling, weights formula, A1 (clipping gives PSD), A2 (rescaling keeps PSD and gives unit diagonal), A3 (two-asset closed form, scaling), A4 (clipped matrix singular, weights undefined)',
    'project.html section#spec Conventions; Appendix A (exemplar-b passage)', PASS, 'Re-derived by hand: A1 z^T X z = sum max(L_ii,f)(V^T z)_i^2; A2 z^T Y z = w^T X w; A3 det Sigma = a^2 b^2 (1-rho^2), normalised numerator b(b-rho a), a(a-rho b), sum a^2+b^2-2 rho a b = (a-b)^2+2ab(1-rho); A4 X v_i = 0. Numerically: A3 closed form vs solve, 1000 random (a,b,rho): max error 1.2e-14 (scripts/M3-d-r6/indep_lab3.py)')
row('M3-d-R09', 'Rubric: five criteria, four levels; official scores of Exemplars A and B agree with their annotations',
    'project.html table#rubric; article#exemplar-a (data-scores 2,2,2,1,2); article#exemplar-b (data-scores 4,4,4,3,3)',
    PASS, 'Each official score matches the annotations: A C2 meets 2, misses 3; C3 meets 2, misses 3; C4 meets 1 (level-2 miss); C1 meets 2, misses 3; C5 meets 2, misses 3. B C1 meets 3 and 4; C2 meets 3 and 4; C3 meets 3 and 4; C4 meets 3 and no level-4 meet; C5 meets 3, misses 4. Scores are consistent with the rubric rule.')
row('M3-d-R10', 'Exemplar prose numbers (distances, gap, entry difference, weights, eigenvalue, deviations) equal Lab 3 printed output',
    'project.html article#exemplar-a and article#exemplar-b passages', PASS, 'Exemplar B: -0.142113, 0.176573, 0.175003, 0.001570, 0.011516, 1.778929 -1.096718 -0.255613 0.573402 all equal lab_p3.out. Exemplar A deliberately rounded (1.78, -1.10, -0.26, 0.57) and annotated as missing level 3; its claim that clipping is not PSD is annotated as contradicting A1')
row('M3-d-R11', 'Hours arithmetic: project 2+3+14+8+12+6 = 45; hub 105 lesson + 45 project = 150; lesson data-hours sum 105; 45/150 = 30%',
    'project.html table#hours; course/modules/M/M3/index.html data-hours-lessons/project; L01-L09 data-hours', PASS, 'Lesson hours 12+11+12+12+12+11+11+12+12 = 105 (grep of data-hours); project table sums to 45; index.html states 150 hours and 30 percent')
row('M3-d-R12', 'Reference solution passes the whole suite on seeds 0-49 under the browser flags',
    'course/modules/M/M3/grader/reference.py; tools/run_graders.py --unit M3 --seeds 0-49', PASS, 'run_graders M3: PASS (reference 50/50 seeds, slowest 0.2 s) (scripts/M3-d-r6/run_graders_M3_0-49.out); starter fails suite per run_graders checks')
row('M3-d-R13', 'Existing 79 mutants (earlier rounds) all killed on seeds 0-49; new mutants counted',
    'ledgers/M3/mutants/*.py; tools/mutate_graders.py --unit M3 --seeds 0-49', PASS, 'Output scripts/M3-d-r6/mutate_M3_0-49_r6.out: 82 of 83 killed; the only survivor is the new r6d_m04 (see R15)')
row('M3-d-R14', 'Six alternative correct implementations (numpy eigh, numpy solve, Dykstra with other stop rule, Jacobi with other cutoffs, Cholesky bisection min, numpy linalg) pass the suite on seeds 0-49',
    'ledgers/M3/alternatives/alt1..alt6; scripts/M3-d-r6/alts_run.py', PASS, 'Each of the six files passes all 50 seeds (scripts/M3-d-r6/alts_run.py); no over-constraint found')
row('M3-d-R15', 'Four new student-error mutants written by this verifier: three killed; one survives and is not a grader FAIL under the ruling',
    'ledgers/M3/mutants/r6d_m01..m04; scripts/M3-d-r6/make_r6_mutants.py', PASS,
    'r6d_m01 clip sorts values not vectors: KILLED (test_clip_repair_leaves_positive_definite_unit_matrix_unchanged seed 0). r6d_m02 comparison Sigma row-scaled twice: KILLED (test_lab3_reference_numbers_are_matched seed 0). r6d_m03 symmetry check skips last column pair: KILLED (test_asymmetry_beyond_tolerance_is_refused seed 0). r6d_m04 projection stops on gap only: SURVIVED all 50 seeds. Not a FAIL: project.html Exemplar B text states "the suite checks the result, not the stopping rule", and no contract sentence states the stopping rule (spec gives only the signature tol=1e-10, max_iter=500). Recorded as a known, documented gap.')
row('M3-d-R16', 'Grader test docstrings and instance docstring agree with code (instance ranges, margin 0.02, tests named on the page exist)',
    'course/modules/M/M3/grader/instance.py docstring; test_project.py docstrings; project.html Exemplar B names test_projection_repair_is_no_farther_than_clipping',
    PASS, 'instance.py: k in {3,4,5}; vols [0.05,0.40] rounded 4dp; off-diagonal [-0.95,0.95]; redraw unless min eig < -0.02; spectrum [-0.6,1.4]; psd_spectrum first entry 0 (other entries drawn in [0.1,2.0], a subset of the docstring range [0,2]); all as stated. Test names resolve (collect-only lists test_projection_repair_is_no_farther_than_clipping)')
row('M3-d-R17', 'Test is_psd boundary at exactly -tol: docstring says the test does not depend on rounding',
    'grader/test_project.py test_is_psd_accepts_eigenvalue_exactly_at_minus_tol', PASS, 'Note only: the test takes tol = -min_eigenvalue(a) and requires is_psd to accept an equality at the boundary, which depends on the rounding of is_psd. Six independent implementations (R14) all pass, so this is not an over-constraint in practice; the docstring claim is slightly stronger than the test supports.')
row('M3-d-R18', 'Notation: no registered symbol used with another meaning (notation/notation.json; macros)',
    'course/modules/M/M3/project.html; notation/notation.json', PASS, 'Registry symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (AP1/M4/S1). None appears on project.html. Macros used (\\diag, \\top, \\det, \\lVert, \\rVert, \\mathbf) are registered or standard TeX. Local letters (v for volatility vector and for eigenvector v_i inside A4) are not registry symbols; noted only.')
row('M3-d-R19', 'Concept links and DAG: eigendecomposition (L03), spectral-theorem (L04), positive-semidefinite-matrix (L05) anchors exist; DAG within prerequisites',
    'project.html concept links; course/modules/M/M3/L03.html L04.html L05.html', PASS, 'grep: id="def-eigendecomposition" in L03, id="def-spectral-theorem" in L04, id="def-positive-semidefinite-matrix" in L05; tools/check_dag.py --all: PASS')
row('M3-d-R20', 'Gates on this slice: check_projects, check_pages, page_smoke (project), run_labs (project), ruff, mypy strict, relevant pytest',
    'tools/check_projects.py, tools/check_pages.py, tools/page_smoke.py, tools/run_labs.py, tests/test_labs.py, tests/test_page_checks.py', PASS, 'check_projects --all: M3 PASS; check_pages --unit M3: PASS; page_smoke --unit M3 --pages project: PASS (in-browser grader 150 tests pass on seed 159042164); run_labs --unit M3 --page project: PASS 3/3; ruff check and ruff format --check on grader and tests/labs/M3: clean; mypy --strict on grader/reference/instance/starter and project labs: no issues; pytest tests/test_labs.py -k "M3 and project" and tests/test_page_checks.py: pass')
row('M3-d-R21', 'cards.json structure: 179 cards, unique ids, no duplicate fronts or backs, grade and basis consistent, lessons L01-L09',
    'course/modules/M/M3/cards.json', PASS, 'Python check: 179 ids unique; 0 duplicate fronts; 0 duplicate backs; every grade C has basis and no other card does; grades T 104, C 37, none 38; lesson counts L01 24, L02 20, L03 22, L04 16, L05 25, L06 15, L07 17, L08 17, L09 23')
row('M3-d-R22', 'Cards: every number and every Definition/Lemma/Proposition/Theorem/Corollary/Example/Remark/Problem reference appears in its own lesson text',
    'course/modules/M/M3/cards.json vs L01.html..L09.html', PASS, 'Automated check: 0 missing numbers; 0 missing labels. Only non-literal references are "Problem E3" (lesson shows "E3 · The eigenspace dimension for B") and "Section 1" (lesson heading "1 Orthogonal projection onto a subspace"), both resolvable. Snippets printed for each referenced label in L01-L02 and spot checked elsewhere')
row('M3-d-R23', 'Cards citing Lab output (37 grade-C cards): each printed count equals the twin output',
    'cards.json grade C; tests/labs/M3/lab-M3-L01-1.py..L09-1.py', PASS, 'Re-ran every L01-L09 twin with python -I -W error (L03/L04/L05/L08/L09 under .venv). Matches: c016 188/200; c017 198/200; c018 100/100; c019 0/200 and 100/100; c038/c039 50/50; c057 3/3; c058 det 6; c059 True; c074 200/200 x4; c075 1200/1200; c094 -2; c095 118/360; c096 500/500; c097 1; c100 True; c109 ten matrices; c110 2.2335 0.9250 0.3348; c111 2; c124 True; c125 1.3325 0.8488 -0.4120; c126 0.8951; c139 True; c140 0.9994 0.9985 0.9990; c141 0.7587 to 0.9791; c145 generator scales 8/4/2; c162 23 of 40; c163 23 of 23; c164 0.175527 and 0.163280; c171 True; c172 rank 1; c173 100000 of 100000; c174 75.9 18.1 5.2; c175 23 of 23; c176 -1.0000 3.0000; c177 rank 2; c179 True')
row('M3-d-R24', 'Cards: computed or theorem-level claims checked by hand (all 179 cards read)',
    'cards.json all lessons', PASS, 'Hand-checked: c003 subspace test; c012 dimension count; c020/c022 counterexamples ((1,1,2) = (1,0,1)+(0,1,1); (1,1)=(1,0)+(0,1)); c033/c037 matrix [[0,2],[1,0]]; c041 AN and NA products; c048 eigenvalues (7 +/- sqrt5)/2 = 4.6180, 2.3820; c049 det(R-lI)=l^2+1; c056 eigenvectors and det P = 6; c060 det(A-4I)=det(A-3I)=-1; c073 inner product 1/sqrt2; c085 form -2; c086 form x1^2+x2^2; c093 eigenvalues 0,1,3 and null vector (1,1,-1); c108 identity SVD; c112 A^TA = diag(0,1); c128 P=diag(1,0); c144 scaling by 4; c152 form -2.4 with the printed sign pattern; c156 identity; c160 clip [[1.1,1.1],[1.1,1.1]] and distance 0.04; c161 0.64. No defect found.')
row('M3-d-R25', 'Reading section attributions: Axler (2024, 4th ed.) and Strang (2023, 6th ed.) against the registry records cited by key',
    'course/modules/M/M3/project.html lines 666, 668-669 (section#reading); references/references.json records axler2024linear (line ~1208) and strang2023introduction (line ~21415)',
    'FAIL',
    'Registry records carry no edition field (keys: key, doi, url, verified_by, type, title, authors, year, container, volume, issue, pages, isbn, publisher, status). Crossref api.crossref.org/works/10.1007/978-3-031-41026-0: edition-number null, published 2024. Open Library openlibrary.org/books/OL46576100M.json: edition_name null, publish_date 2023. The editions appear only in curriculum/01-foundations.yaml sources (quoted in the plan). Editions are published facts that cannot be read from the cited registry records, so the page attributes data it cannot verify.',
    'Either record the edition from the publisher page through tools/add_reference.py so references.json carries an edition field and the page can cite it, or remove "4th ed." and "6th ed." from project.html lines 666, 668 and 669 and keep the attribution to the curriculum source list only.')
frag = {
    'unit': 'M3', 'slice': 'd', 'round': 6,
    'verifier': 'independent verifier (Claude Haiku 5.5), unit M3 slice d, round 6',
    'pin': '44f1eb6a417ce687a9b88c7ee917e72566b29892',
    'base': 'none: round-5 fragment /Users/billyribeiro/.fanout/frags/B-M3-d.round5.json does not exist; every row verified from scratch',
    'checkout': '/Users/billyribeiro/.fanout/wt/verifyB6-M3-d',
    'scratch': 'ledgers/M3/scripts/M3-d-r6/',
    'verified_at': datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    'verdict': 'FAIL',
    'rows': rows,
    'mutants': mutants,
    'registry_flags': ['references.json records axler2024linear and strang2023introduction carry no edition field, while project.html Reading section states 4th and 6th editions (R25)'],
    'freshness_flags': ['round-5 fragment path given in the task is absent; no delta could be computed, so every row was re-verified'],
    'notes': 'Verdict FAIL is driven by R25 only. The ledger tool will also report a mutant-count mismatch (82 of 83 killed) from r6d_m04, which survived all 50 seeds; per the verifier rules that survivor is not a grader FAIL because project.html Exemplar B states the suite checks the result, not the stopping rule, and no contract sentence states the stopping rule. Could not check: browser execution of the grader panel in a real browser (page_smoke runs it under Pyodide-equivalent harness only); full line-by-line proof check of lesson-level theorem hypotheses for every card in L04-L09 (cards were checked by label presence, by the printed snippet for the referenced statements in L01-L03, by hand on the computed claims, and by re-running every lab-number card); rendered page appearance; the hub index.html placement and lesson pages were only read for anchors and hours, not verified (other slices).',
    'summary': 'M3 slice d (project.html rubric and exemplars, grader, project labs, cards.json). 25 rows: 24 PASS, 1 FAIL (R25 edition attribution). Grader gates pass (150 tests; reference 50/50 seeds; 6 alternatives pass; 82/83 mutants killed, the survivor is documented and not a finding). Three new student-error mutants killed.'
}
mut_fail = [m for m in mutants if m['killed_by'] is None]
frag['mutant_survivors'] = [m['name'] for m in mut_fail]
out = pathlib.Path('ledgers/M3/M3-d.json')
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('wrote', out, len(rows), 'rows', len(mutants), 'mutants')
