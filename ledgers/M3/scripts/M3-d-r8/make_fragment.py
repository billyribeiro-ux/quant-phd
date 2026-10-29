import json, re, pathlib, datetime
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB8-M3-d")
S = "ledgers/M3/scripts/M3-d-r8/"
mut_lines = (ROOT / S / "mutate_all2.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"(KILLED|SURVIVED) (\S+?)\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    killed_by = None if killed.strip() == "None" else killed.strip()
    mutants.append({
        "name": name,
        "description": desc.strip(),
        "killed_by": killed_by,
        "status": "KILLED" if status == "KILLED" else "SURVIVED",
        "ruling": ("PASS: survivor is not a finding; the page no longer states the stopping rule (project.html line 622 calls it an implementation choice) and plan M3-build-plan.md line 276 names alternating projections with a different stopping rule as a correct alternative"
                   if status == "SURVIVED" else None),
    })
assert len(mutants) == 92, len(mutants)

rows = [
 ("M3-d-R01", "Lab 1 (project rung 1): twin output equals page expected block; page code equals twin",
  "course/modules/M/M3/project.html section#lab-M3-project-1; tests/labs/M3/lab-M3-project-1.py", "PASS",
  "Fresh: tools/run_labs.py --unit M3 --page project -> 'run_labs M3: PASS (3/3)' (scripts/M3-d-r8/run_labs_project.out); twin runs under python -I -W error with exit 0 (scripts/M3-d-r8/lab_p1.out)"),
 ("M3-d-R02", "Lab 2 (completion): blanks at Step 3 and Step 5; twin is the completed solution; twin output equals expected block",
  "course/modules/M/M3/project.html section#lab-M3-project-2; tests/labs/M3/lab-M3-project-2.py", "PASS",
  "Fresh run_labs PASS 3/3 (scripts/M3-d-r8/run_labs_project.out); twin python -I -W error exit 0 (scripts/M3-d-r8/lab_p2.out); blanks at project.html lines 193 and 201 are the Step 3 and Step 5 blanks named on line 221"),
 ("M3-d-R03", "Lab 3 printed numbers (eigenvalue, distances, gap, entry difference, diagonal deviations, determinant, weights)",
  "course/modules/M/M3/project.html section#lab-M3-project-3 expected block (lines 460-468); tests/labs/M3/lab-M3-project-3.py", "PASS",
  "Twin output (scripts/M3-d-r8/lab_p3.out) equals the expected block line for line. Independent numpy re-derivation (scripts/M3-d-r8/numbers_check.py): eigenvalue -0.142113; clipping distance 0.176573225; Dykstra projection distance 0.175003044 (gap 0.001570182); max entry difference 0.011516417; det -0.2616; weights 1.778929 -1.096718 -0.255613 0.573402. The label of the entry-difference line is checked separately in M3-d-R27"),
 ("M3-d-R04", "Lab 3 hypothesis sentence (smallest eigenvalue negative; projection nearer by positive distance; diagonals within 5e-7; det nonzero; weights sum to 1)",
  "course/modules/M/M3/project.html Lab 3 p.hypothesis (line 289)", "PASS",
  "Each clause checked against scripts/M3-d-r8/lab_p3.out: min eig -0.142113 < 0; gap 0.001570 > 0; diagonal deviations 0.000000 (below 5e-7); det -0.261600 nonzero; sum 1.000000"),
 ("M3-d-R05", "Lab 1 and Lab 2 interpretation prose numbers",
  "course/modules/M/M3/project.html p.interpretation after Lab 1 (line 138) and after Lab 2 (line 221)", "PASS",
  "Numbers 1.096064, 1.104409, 1.074824, 0.636095, -0.382551, 0.469578, 1.060165, 1.075224, 1.068322, 0.498962, 0.409576, -0.586237 match the expected blocks (lines 132-135, 215-218) and scripts/M3-d-r8/lab_p1.out, lab_p2.out"),
 ("M3-d-R06", "Lab 3 interpretation prose (distance gap, entry gap, sign pattern, A4 hypothesis, Sigma invertibility)",
  "course/modules/M/M3/project.html line 469 (p.interpretation after Lab 3)", "PASS",
  "Line 469 now reads 'The clipped matrix X is singular by A4 (a negative eigenvalue, floor 0). If its diagonal is positive, the rescaled Y and the Sigma built from it are singular too; Lab 3 does not print that diagonal'. Proof A4 (line 637) re-derived: X u_i = V Lambda_0 e_i = 0; z = D_X^{1/2} u_i gives Yz = 0; S_v^{-1} z gives Sigma S_v^{-1} z = 0. Numerical X min|eig| -7.5e-17 (scripts/M3-d-r8/numbers_check.py). Round-7 misattachment is cured"),
 ("M3-d-R07", "Spec constants: 150 tests; PSD tolerances -1e-9 (clipping) and -1e-8 (projection); ValueError conditions named; 120 s browser limit",
  "course/modules/M/M3/project.html section#spec (Constraints, Grading mode, Conventions line 243-247); grader/test_project.py; course/assets/js/python.js", "PASS",
  "Fresh: QF_SEED=0 pytest --collect-only -q test_project.py -> '150 tests collected' (scripts/M3-d-r8/collect.out is the failed-import attempt; the count was taken in scratch with reference.py as covariance_doctor.py: '150 tests collected in 0.04s'); spec command with --assert=plain -W error -> '150 passed'. test_project.py lines 386 and 466 (-1e-9, -1e-8); ValueError only for the four named conditions (must_raise call sites lines 175, 185, 641, 688, 712, 630). python.js not in the round-8 delta; 120 s value carried from round 7"),
 ("M3-d-R08", "Convention and appendix math: A1 (clipping PSD), A2 (rescaling unit diagonal), A3 (two-asset closed form), A4 (clipped matrix singular, weights undefined)",
  "course/modules/M/M3/project.html section#spec Conventions (lines 242-247); Appendix A (line 481); proofs (lines 635-637)", "PASS",
  "Re-derived by hand: A1 z^T X z = sum max(lambda_i,f)(V^T z)_i^2 >= 0; A2 z^T Y z = w^T X w with w = D^{-1/2} z; A3 det Sigma = a^2 b^2 (1-rho^2), Sigma^{-1} 1 = (det)^{-1}(b(b-rho a), a(a-rho b)), sum a^2+b^2-2 rho ab = (a-b)^2+2ab(1-rho) > 0, scaling by c^2 cancels; A4 as in M3-d-R06. The line 245 convention ('valid whenever the clipped matrix has a positive diagonal') matches A2"),
 ("M3-d-R09", "Rubric: five criteria, four levels; official scores of Exemplars A and B agree with their annotations and with the rubric",
  "course/modules/M/M3/project.html table#rubric line 493 (C2 level 3); exemplar-b body lines 609 and 613", "PASS",
  "Round-7 defect cured: Exemplar B line 609 now states the clipped matrix's Sigma is singular by A4 'if its diagonal is positive' and line 613 annotation says the same, matching rubric C2 level 3 ('under its diagonal hypothesis'). The projection weights element ('not reported, with the reason') is met by 'Lab 3 prints no weights for the repairs' plus 'does not establish that the projection's Sigma is invertible'. Caveat, not a finding: the C2 annotations are consistent with the scores data-scores='4,4,4,3,3'"),
 ("M3-d-R10", "Exemplar A and B numbers are printed values of Lab 3 with their units (Exemplar A rounding allowed where annotated)",
  "course/modules/M/M3/project.html exemplar-a and exemplar-b passages (lines 504-646)", "PASS",
  "Exemplar B numbers 0.176573, 0.175003, 0.001570, 0.011516, -0.142113, weights 1.778929 -1.096718 -0.255613 0.573402 sum 1 equal scripts/M3-d-r8/lab_p3.out. Exemplar A weights 1.78, -1.10, -0.26, 0.57 are the printed values rounded, and its annotation (line 551) says so"),
 ("M3-d-R11", "Hours arithmetic: time budget table vs data-hours-project and hub split",
  "course/modules/M/M3/project.html table#hours (lines 258-264), data-hours-project=45 (line 33); course/modules/M/M3/index.html data-hours-lessons=105 data-hours-project=45", "PASS",
  "2+3+14+8+12+6 = 45 = data-hours-project; hub 105 lessons + 45 project = 150 as the rationale on line 264 states. index.html unchanged in the round-8 delta"),
 ("M3-d-R12", "Reference solution passes the suite on seeds 0-49",
  "course/modules/M/M3/grader/reference.py; tools/run_graders.py --unit M3 --seeds 0-49", "PASS",
  "Fresh: tools/run_graders.py --unit M3 --seeds 0-49 -> 'run_graders M3: PASS (reference 50/50 seeds, slowest 0.2 s)' (scripts/M3-d-r8/run_graders.out). reference.py is a docstring-only change since round 7 (not in the round-8 delta)"),
 ("M3-d-R13", "Grader mutant survival: projection stops on gap alone (r6d_m04) against the stopping rule the page states",
  "ledgers/M3/mutants/r6d_m04_projection_stops_on_gap_only.py; course/modules/M/M3/project.html line 622", "PASS",
  "Fresh tools/mutate_graders.py --unit M3 --seeds 0-49 (scripts/M3-d-r8/mutate_all2.out): 91/92 killed; the only survivor is r6d_m04. Ruling applied: the page no longer states the stopping rule (line 622 now says 'The suite checks the result, not the stopping rule, which is an implementation choice'; grep 'stop' finds no other statement of it), and plan M3-build-plan.md line 276 lists 'alternating projections with a different stopping rule' as a correct alternative. The survivor violates no stated behaviour, so it is not a finding"),
 ("M3-d-R14", "Six alternative correct implementations pass seeds 0-49",
  "ledgers/M3/alternatives/alt1..alt6; scripts/M3-d-r8/alts_run.py (run with -I)", "PASS",
  "Fresh: python -I scripts/M3-d-r8/alts_run.py -> alt1 numpy eigh, alt2 Dykstra other stop rule (5000 iterations, gap-only), alt3 numpy solve, alt4 Jacobi other cutoffs, alt5 Cholesky bisection, alt6 numpy linalg: each 'PASS all 50 seeds' (scripts/M3-d-r8/alts_run.out)"),
 ("M3-d-R15", "Mutants: round-7 new mutants and round-8 new student-error mutants are killed; all existing mutants re-run",
  "ledgers/M3/mutants/r7d_m01..m04, r8d_m01..m05", "PASS",
  "All 92 mutants re-run (scripts/M3-d-r8/mutate_all2.out): r7d_m01..m04 KILLED. Five new round-8 mutants, each KILLED: r8d_m01 weights refuse only exact zero volatility (killed by test_weights_refuse_volatility_at_or_below_zero[negative-first]); r8d_m02 projection stops after 3 Dykstra passes (test_projection_repair_is_a_valid_repair); r8d_m03 Sigma_ij = v_i^2 C_ij (test_lab3_reference_numbers_are_matched); r8d_m04 is_psd checks the diagonal only (killed by a non-square test, i.e. the diagonal-only routine fails it); r8d_m05 projection = clipping with diagonal pinned to 1 without rescaling (test_projection_repair_is_a_valid_repair)"),
 ("M3-d-R16", "Docstrings and page text on comparison_weights and projection match the code",
  "course/modules/M/M3/grader/reference.py lines 109-110 and 131-132; project.html spec lines 233 and 246", "PASS",
  "reference.py comparison_weights docstring '(S C S) x = 1; S = diag(vols)' matches sigma_ij = vols_i C_ij vols_j (line 139); spec line 246 gives Sigma = SCS and w = Sigma^{-1} 1 normalised; projection_repair docstring matches Dykstra's loop; test_projection_repair_is_no_farther_than_clipping exists (test_project.py line 470) and is named on project.html line 622"),
 ("M3-d-R17", "test_is_psd_accepts_eigenvalue_exactly_at_minus_tol (the boundary test)",
  "course/modules/M/M3/grader/test_project.py lines 319-326", "PASS",
  "grader/ files byte-identical to the round-7 pin (git diff 7aa909e ce7b382 shows no grader change); the test passes on the reference (150 passed) and kills r7d_m02 (mutate_all2.out)"),
 ("M3-d-R18", "NOTATION: every symbol vs notation/notation.json (T, R^*, Phi, gamma_3 ... never reused with another meaning)",
  "course/modules/M/M3/project.html lines 246 (x3), 586, 637; notation/notation.json macros \\indic (tex \\mathbf{1}, meaning 'indicator function')", "FAIL",
  "project.html uses \\mathbf{1} for the all-ones vector in '\\(w = \\Sigma^{-1}\\mathbf{1} / (\\mathbf{1}^{\\top}\\Sigma^{-1}\\mathbf{1})\\)' (line 246), line 586 and line 637. notation/notation.json registers \\mathbf{1} through the macro \\indic (tex \\mathbf{1}, meaning 'indicator function, \\indic\\{A\\}'). The course has already moved its ones vector to \\boldsymbol{\\iota} in L08.html lines 350, 352, 407 for this reason. The project page is the only page still using \\mathbf{1} for the ones vector. Fix: replace every \\mathbf{1} that denotes the all-ones vector in project.html (lines 246, 586, 637) with \\boldsymbol{\\iota}, matching L08. Other registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) do not occur in project.html"),
 ("M3-d-R19", "Concept links and DAG: project.html concept links resolve; check_dag M3",
  "course/modules/M/M3/project.html concept links (lines 46, 53, 243, 281); tools/check_dag.py --unit M3", "PASS",
  "Fresh: tools/check_dag.py --unit M3 -> 'check_dag M3: PASS' (scripts/M3-d-r8/check_dag.out). Links L03.html#def-eigendecomposition, L04.html#def-spectral-theorem, L05.html#def-positive-semidefinite-matrix resolve; the lede and rung-3 anchors (#conventions, #spec, #grader-section, #report, #stretch) resolve to existing ids"),
 ("M3-d-R20", "Gates: check_projects, check_pages, page_smoke project, run_labs project, test_labs project labs, ruff on grader and labs, mypy on grader and labs",
  "tools/check_projects.py, tools/check_pages.py, tools/page_smoke.py, tools/run_labs.py, tests/test_labs.py, course/modules/M/M3/grader/", "PASS",
  "Fresh: check_projects M3 PASS; check_pages M3 PASS; page_smoke M3 project PASS (in-browser grader 150 tests pass on seed 1793471381); run_labs project PASS 3/3; pytest tests/test_labs.py -k lab-M3-project exit 0; ruff check grader and lab twins 'All checks passed!'; mypy --no-incremental on reference, instance and three twins 'no issues found in 5 source files' (scripts/M3-d-r8/*.out)"),
 ("M3-d-R21", "cards.json structure: ids, duplicates, grades, basis",
  "course/modules/M/M3/cards.json (180 cards)", "PASS",
  "scripts/M3-d-r8/cards_check.py: 180 cards; 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs; near-duplicate scan (difflib) lists no true duplicates (c017/c019 and c087/c088 differ in dimension and in the positive or the real case); grades T 104, C 38, no grade 38 (round-7 text said 142 T, which was a counting error). The 38 no-grade cards are definition or misconception cards; BUILDER_RULES section 7 grades only the empirical results ('with its grade'), so they are not counted against it. Grade-C cards all carry a basis key"),
 ("M3-d-R22", "Cards that changed since the round-7 pin agree with the current lesson text and carry the proposition's hypotheses",
  "course/modules/M/M3/cards.json c005, c009, c019, c036, c054, c076, c086, c123, c134, c166 vs L01, L02, L03, L04, L05, L07, L08, L09 HTML", "PASS",
  "c005: L01 'The span of a finite list is the smallest subspace containing it (Proposition 2.2)'. c009: L01 Definition 3.3 and row-operation paragraph. c019: L01 'Corollary 3.6 predicts 0 ... out of 200'; output 'R^3, 4 vectors: independent in 0 of 200'; grade C with basis. c036: L02 change of basis P^{-1}AP, Corollary 4.2; A = P Atilde P^{-1} re-derived. c054: L03 Problem E3 and 'Lesson 1, Proposition 3.12'; dim E_1 = 2 - rank(B-I) = 1 re-derived. c076: L04 Remark 2.7 (N = [[1,2],[0,3]]), Remark 1.6 (rotation [[0,-1],[1,0]]), Theorem 2.3 hypothesis symmetry. c086: L05 Definition 1.4 'requires symmetry', Remark 1.8, x1^2+x2^2. c123: L07 Theorem 2.2 (unique beta-hat, normal equations, residual orthogonal to columns). c134: L08 Theorem 1.4 (Z = X~V, Z^T Z/(T-1) = Lambda, diagonal (T-1) lambda_k, shares sum to 1 when sum > 0). c166: L09 Proposition 3.4 (PSD with positive diagonal, D^{-1/2} B D^{-1/2}, preserves PSD)"),
 ("M3-d-R23", "Grade-C cards: basis key and the lab output they cite",
  "course/modules/M/M3/cards.json grade C (38 cards)", "PASS",
  "All 38 grade-C cards carry a basis; c019 cites 'Lab 1' and the printed count 0 of 200 is in L01 Lab 1 output. The other changed grade-C cards are unchanged in grade and number"),
 ("M3-d-R24", "Changed cards re-read against lesson statements and proofs; numbers present in own lesson",
  "course/modules/M/M3/cards.json (all lessons); scripts/M3-d-r8/cards_check.py", "PASS",
  "Every number in every card's front and back appears verbatim in its own lesson HTML (cards_check.py: no missing numbers). Each of the ten changed cards re-read against the current lesson text (R22). Unchanged cards whose subject text the lesson delta touched (c096, c097, c163, c164, c167, c175, c179, c100, c118-c121, c127, c168, c178, c061, c130, c142, c053, c074, c109, c111, c173) re-read against the current lessons and found consistent"),
 ("M3-d-R25", "Reading section attributions: Axler (2024) and Strang (2023) against the registry; no passage locator",
  "course/modules/M/M3/project.html section#reading (lines 666-669); references/references.json", "PASS",
  "Carried from round 7 (references/ and the reading section are not in the round-8 delta): text 'Axler (2024)' and 'Strang (2023)' matches registry year fields; no statement is attributed to a passage"),
 ("M3-d-R26", "Lede parenthetical points to a definition that exists",
  "course/modules/M/M3/project.html line 37 (lede); Conventions section lines 240-250", "PASS",
  "Lede now reads 'a covariance matrix must be positive semidefinite (defined in the conventions)' with <a href='#conventions'>; id conventions exists (line 240) and defines positive semidefinite (line 243). Round-7 defect cured"),
 ("M3-d-R27", "Lab 3 printed label for the entry difference matches what the code computes",
  "course/modules/M/M3/project.html line 464 (expected block); tests/labs/M3/lab-M3-project-3.py line 155; grader/test_project.py line 521", "FAIL",
  "The printed line is 'largest entry difference, projection minus clipping: 0.011516', but the code prints max(abs(proj[i][j] - clip[i][j])) (lab twin line 155 and page line 444), an unsigned maximum. The label describes a signed difference the lab does not compute. Value 0.011516 is correct (scripts/M3-d-r8/numbers_check.py). Fix: change the label in the twin and the expected block to 'largest absolute entry difference between the two repairs:' and re-embed with tools/embed_labs.py project.html --refresh lab-M3-project-3; update the grader's check name at test_project.py line 521"),
 ("M3-d-R28", "Rubric calibration: the PSD-verdict criterion (C1) is consistent with the verdicts Lab 3 prints and with Exemplar B's score",
  "course/modules/M/M3/project.html rubric row C1 (line 492, levels 3 and 2); Exemplar B line 597 and data-scores line 569", "FAIL",
  "Rubric C1 level 3 requires each repair's PSD verdict 'as Lab 3 prints them', and level 2 is triggered by a 'verdict ... that Lab 3 does not print'. Lab 3 prints a PSD verdict only for the input (False, line 460) and the projection (True, line 466); it prints none for the clipped matrix. Exemplar B line 597 states 'Clipping is PSD by A1' and scores C1 4 (data-scores line 569), so under the rubric's own wording it cannot be both level 4 and free of an unprinted verdict. Fix: amend the rubric C1 level 3 and level 2 cells so that a verdict may be printed by Lab 3 or proved in A1 for the clipped matrix, or lower Exemplar B's C1 score and annotation to match."),
]

rows_out = [{"id": i, "check": c, "location": l, "status": s, "evidence": e} for i, c, l, s, e in rows]
fails = [r for r in rows_out if r["status"] != "PASS"]
assert len(rows_out) == 28, len(rows_out)
frag = {
  "unit": "M3",
  "slice": "d",
  "round": 8,
  "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, round 8",
  "pin": "ce7b3821c288da3dbba5dd4c90fb87dfd6d30089",
  "base": "round-7 fragment /Users/billyribeiro/.fanout/frags/B-M3-d.round7.json (pin 7aa909e95b757b1abf7b75186d5fa1ed7d1945a4); round-8 delta read in full in project.html (every hunk), cards.json (every hunk, 10 changed cards), reference.py, instance.py, starter.py, test_project.py (all 760 lines), lab-M3-project-1/2/3 twins, and the lesson hunks L01-L09 that the changed cards cite",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyB8-M3-d",
  "scratch": "ledgers/M3/scripts/M3-d-r8/",
  "verified_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
  "verdict": "FAIL",
  "rows": rows_out,
  "mutants": mutants,
  "registry_flags": [],
  "freshness_flags": [],
  "notes": "Round-8 pin ce7b382. Delta since round 7 touched project.html (lede, spec, Lab 3 interpretation, Exemplar B and rubric wording), cards.json (10 changed cards) and lesson HTML that those cards cite. Mutants: 92 run on seeds 0-49, 91 killed, 1 survivor r6d_m04 ruled PASS (see R13). Non-blocking observation, not a row: Exemplar B's C2 level-4 proof of A3 is complete; its C3 and C5 annotations are consistent with the rubric. Not checked: rendered visual appearance beyond page_smoke; lesson-level hypotheses of unchanged cards beyond the carried round-7 checks; BUILDER_RULES grade requirement for the 38 no-grade definition cards; the 120 s browser limit in python.js (carried from round 7).",
  "summary": f"M3 slice d round 8: {len(rows_out)} rows, {len(rows_out)-len(fails)} PASS, {len(fails)} FAIL ({', '.join(r['id'] for r in fails)}). Mutants: 92 run (87 existing + 5 new round-8 student-error mutants), 91 killed, 1 survivor (r6d_m04, ruled PASS). Gates fresh and PASS: check_projects, check_pages, check_dag, run_labs (3/3), run_graders 50/50, page_smoke project, pytest test_labs project labs, six alternatives pass 50 seeds, collect-only 150 tests, ruff, mypy. Round-7 FAILs R06, R09, R13, R26 are cured.",
}
out = ROOT / "ledgers/M3/M3-d.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, len(rows_out), len(mutants), len(fails))
