"""Build the round-1 fragment for M3 slice d from the verified evidence (no content is invented here)."""

import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD1-M3-d")
OUT = ROOT / "ledgers/M3/M3-d.json"
OUTDIR = "ledgers/M3/scripts/M3-d-r1/out/"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# --- gates (commands run by the verifier on pin d0f39c0; outputs in scripts/M3-d-r1/out/)
row("gate-check-pages", "gate: tools/check_pages.py --all (M3 lines)", "course/modules/M/M3/*", "PASS",
    OUTDIR + "check_pages.out: 'check_pages M3: PASS', exit 0.")
row("gate-check-dag", "gate: tools/check_dag.py --all (M3 line)", "course/modules/M/M3/*", "PASS",
    OUTDIR + "check_dag.out: 'check_dag M3: PASS', exit 0.")
row("gate-check-projects", "gate: tools/check_projects.py --all (M3 line)", "course/modules/M/M3/project.html", "PASS",
    OUTDIR + "check_projects.out: 'check_projects M3: PASS', exit 0.")
row("gate-run-graders", "gate: tools/run_graders.py --unit M3 --seeds 0-49", "course/modules/M/M3/grader/", "PASS",
    OUTDIR + "run_graders.out: 'run_graders M3: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0.")
row("gate-run-labs", "gate: tools/run_labs.py --unit M3 (twins, page code = twin, expected = output)",
    "course/modules/M/M3/L0*.html, project.html", "PASS",
    OUTDIR + "run_labs.out: 'run_labs M3: PASS (12/12)', exit 0.")
row("gate-page-smoke", "gate: tools/page_smoke.py --unit M3 --pages (project.html alone, then L01-L09 and index alone)",
    "course/modules/M/M3/*.html", "PASS",
    OUTDIR + "page_smoke_*.out: 'page_smoke M3: PASS' for project.html, each of L01..L09 and index, exit 0 each.")
row("gate-ruff", "gate: ruff check and ruff format --check on grader and tests/labs/M3",
    "course/modules/M/M3/grader/, tests/labs/M3/", "PASS", OUTDIR + "ruff.out: 'All checks passed!', '16 files already formatted', exit 0.")
row("gate-mypy", "gate: mypy --no-incremental on reference.py, instance.py, starter.py",
    "course/modules/M/M3/grader/", "PASS", OUTDIR + "mypy.out: 'Success: no issues found in 3 source files', exit 0.")
row("gate-verify-refs", "gate: tools/verify_refs.py --offline", "references/references.json (M3 pages cite none)", "PASS",
    OUTDIR + "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. Live run not performed (offline gate only, no reference change in slice).")
row("gate-collect-only", "grader test count equals the page's stated count",
    "course/modules/M/M3/project.html line 237 vs grader/test_project.py", "PASS",
    OUTDIR + "collect_only.out: '155 tests collected'; project.html line 237 states '155 tests'.")
row("gate-mutate-m3", "tools/mutate_graders.py --unit M3 --seeds 0-9 over all 128 mutant files",
    "ledgers/M3/mutants/*.py", "PASS",
    OUTDIR + "mutate_M3_seeds0-9.out: 'mutate_graders M3: PASS (128/128 killed)', exit 0.")
row("gate-alternatives", "six alternative correct implementations pass the grader on seeds 0-9",
    "ledgers/M3/alternatives/alt1..alt6", "PASS",
    OUTDIR + "sources_seeds0-9.out: alt1..alt6 each 'PPPPPPPPPP'.")
row("gate-reference-starter", "reference passes and starter fails on seeds 0-9",
    "course/modules/M/M3/grader/reference.py, starter.py", "PASS",
    OUTDIR + "sources_seeds0-9.out: reference.py 'PPPPPPPPPP', starter.py 'FFFFFFFFFF'.")
row("gate-named-conditions", "tests demand ValueError only for the four named conditions",
    "course/modules/M/M3/grader/test_project.py lines 130-205, 646-700", "PASS",
    "must_raise is used only in non-square tests (lines 172) and asymmetry-beyond-1e-9 tests (lines 185, 661, 695) and "
    "volatility/length tests; grep of 'raises' and 'must_raise' shows no other exception assertion. Matches project.html "
    "Constraints and Conventions (four ValueError conditions).")
row("grader-instance", "instance.py matches its docstring and the page's contract",
    "course/modules/M/M3/grader/instance.py (read in full)", "PASS",
    "k in {3,4,5}; corr unit diagonal, redrawn until min eigenvalue < -0.02 (line 'if _min_eigenvalue(corr) >= -_MARGIN'); "
    "psd_corr normalised Gram matrix; psd_spectrum first entry exactly 0.0; deterministic random.Random seeded per seed.")
row("grader-test-count-and-purity", "grader purity, mutation and repeat-call tests",
    "grader/test_project.py lines 744-790 (read)", "PASS",
    "test_functions_print_nothing, test_inputs_are_not_mutated (asymmetric-within-tolerance input), test_repeated_calls_agree "
    "present and asserting the contract; 155 collected.")
row("mutants-new-student-errors", "at least three new student-error mutants written and run (verifier's own)",
    "ledgers/M3/mutants/vd1_01..vd1_05", "PASS",
    "vd1_01 comparison_weights refuses non-PSD C (spec: formula does not require PSD) killed by test_lab3_reference_numbers_are_matched; "
    "vd1_02 clip_repair refuses negative floor killed by test_clip_repair_negative_floor_keeps_eigenvalue_above_it; "
    "vd1_03 is_psd False on zero diagonal killed by test_non_square_is_refused[three_rows_two_columns-is_psd] via IndexError "
    "(kill reason is an artifact of its unvalidated indexing, recorded honestly); vd1_04 symmetry checked only in row 0 "
    "killed by test_asymmetry_beyond_tolerance_is_refused; vd1_05 (validated variant of vd1_03) killed by test_is_psd_one_by_one "
    "on seed 0 (is_psd([[0.0]]) must be True).")
row("equivalent-r11d-m02", "ruling: r11d_m02_projection_stops_on_step_only survives; ruled non-violation",
    "ledgers/M3/equivalent/r11d_m02_projection_stops_on_step_only.py; project.html line on projection_repair", "PASS",
    "Survives 10 seeds (sources_seeds0-9.out). project.html states projection_repair 'stops after at most max_iter alternating "
    "steps' and gives no stop criterion; the mutant changes only the stop test (step <= tol) and still meets the grader's "
    "tolerances (unit diagonal 1e-8, PSD 1e-8, nearness +1e-6). Ruling CONFIRMED.")
row("equivalent-r6d-m04", "ruling: r6d_m04_projection_stops_on_gap_only survives; ruled non-violation",
    "ledgers/M3/equivalent/r6d_m04_projection_stops_on_gap_only.py", "PASS",
    "Survives 10 seeds. Same reading of project.html's projection_repair contract; the stop test is the only change. Ruling CONFIRMED.")
row("equivalent-r15d-m03-label", "ledger label of ruled-equivalent r15d_m03 matches the file",
    "ledgers/M3/equivalent/r15d_m03_projection_repair_no_final_symmetry.py and equivalent/README.md", "FAIL",
    "The file's only code change versus reference.py is line 126: 'if gap <= tol and step <= tol and False:', so the loop never "
    "stops early and always runs max_iter steps. Nothing about final symmetry is changed (diff against grader/reference.py). "
    "The survival ruling is still correct (the output still meets every grader tolerance, and project.html states no stop "
    "criterion), but the name, docstring and README label 'no final symmetry' describe a different mutant.",
    fix="Relabel the file and its README entry as 'projection_repair never stops before max_iter' (or rename the file), keeping "
        "the existing ruling; do not change the grader.")
row("dag-linked-concepts", "every linked concept on M3 pages is in the closure (M1 or M3 owned) and defined before use",
    "course/modules/M/M3/*.html data-concept links", "PASS",
    "check_dag M3: PASS. Linked concepts: quantifiers, direct-proof, mathematical-induction (M1); vector-space, linear-map, "
    "eigendecomposition, spectral-theorem, positive-semidefinite-matrix, orthogonal-projection, least-squares-projection, "
    "singular-value-decomposition, principal-component-analysis, level-slope-curvature, eigenvalue-clipping, "
    "nearest-correlation-matrix (all M3).")
row("dag-m4-concepts-by-name", "concepts owned outside the closure (M4 covariance-matrix, correlation, variance, normal-distribution) "
    "used by name on M3 pages", "course/modules/M/M3/L09.html (78 uses of 'correlation', definition at line 39); "
    "project.html lines 6, 36-37, 229 ('Covariance-matrix doctor', 'covariance matrix must be positive semidefinite', "
    "'covariance matrix'); grader/starter.py docstring of comparison_weights ('inverse covariance matrix'); "
    "L07.html line 201 and L09.html line 203 ('standard deviation'); L04.html line 204 ('Gaussian')", "FAIL",
    "Curriculum concepts: 'correlation' = M4 'Covariance and correlation'; 'covariance-matrix' = M4; 'variance' = M4; "
    "'normal-distribution' = M4 (curriculum/curriculum.json concepts). plans/M3-build-plan.md section 9 B1 (blocking for L08, L09 "
    "and the project) requires an architect decision; plans/M3-open-items.md line 31 records option (a) only for L06 to L08 "
    "and calls the L09 title the unit's own concept. No recorded decision covers the L09 definition 'correlation matrix', the "
    "project's covariance wording, or the starter docstring. Under the rule that a concept used outside the closure by name is a "
    "defect unless the architect's decision says it is prose-only, this is not cleared.",
    fix="Architect to record a B1 decision for L09, project.html and starter.py: either rename to 'symmetric PSD unit-diagonal "
        "matrix' and 'matrix of pairwise estimates' (option a), or add M4 to the closure (option b), or approve a DAG_DEFECT (option c). "
        "Then re-run check_pages and check_dag.")
row("cards-id-sequence", "card ids run <UNIT>-c001 upward without gaps (BUILDER_RULES section 7)",
    "course/modules/M/M3/cards.json", "FAIL",
    "200 unique ids, but they are not sequential: ids 102, 148 and 191 are absent (cards_check.out lists 'missing ids [102, 148, 191]'), "
    "and ids are out of lesson order (M3-c169, c170 in L01; c184, c187 in L02; c171, c172 in L03; c173, c176, c179, c180 in L05; "
    "c168 in L07; c174, c186 in L08; c178 in L06; c188-c203 interleaved). Content is correct; numbering is not upward.",
    fix="Renumber cards.json to M3-c001..M3-c200 in lesson order (no card content change). A grep of course, tools, curriculum, "
        "notation and references finds no other reference to M3-c ids, so only cards.json changes.")

# --- cards: every card read against its lesson text
row("cards-structure", "cards.json: 200 cards, unique ids and fronts/backs, required fields, card numbers present in lesson",
    "course/modules/M/M3/cards.json", "PASS",
    OUTDIR + "cards_check.out: count 200; unique ids; no duplicate fronts or backs; no empty fields; every number on every card "
    "appears in its lesson text (L01-L09 each reported 'absent: []'). Grades: 114 T, 39 C, 47 ungraded (definitions).")
cards_by_lesson = [
    ("cards-L01", "L01 (24 cards) read against L01 text", "M3-c001..c022, c169, c170",
     "Lemma 1.3, Prop 1.4, Def 2.1, Prop 2.2, Ex 2.3, Def 3.1-3.3, Lemma 3.4, Prop 3.5, Cor 3.6, Thm 3.7, Thm 3.8, Ex 3.9, Ex 3.10, "
     "Prop 3.12 all match. Lab 1 counts 188/200, 198/200, 100/100, 0/200, 100/100 match run output. R3 pivot 1.00009e-12 re-computed."),
    ("cards-L02", "L02 (22 cards) read against L02 text", "M3-c023..c042, c184, c187",
     "Lemma 1.2, Def 1.3, Prop 1.4, Ex 1.5, Def 2.1-2.3, Thm 2.4, Prop 3.1, Thm 4.1, Cor 4.2, Ex 2.6, Ex 4.3 recomputed: "
     "[[0,2],[1,0]], AP=[[1,2],[1,0]], composition AN=[[2,1],[1,1]] vs NA=[[1,1],[1,2]]. Lab 1 50/50, 50/50, 50/50 and 7 rejections match."),
    ("cards-L03", "L03 (23 cards) read against L03 text", "M3-c043..c062, c171, c172, c188",
     "Ex 1.6 eigenvalues (7 +- sqrt5)/2 = 4.6180, 2.3820 re-computed; Remark 1.7 det = lambda^2+1; Ex 2.5 eigenvectors and det P = 6 re-computed; "
     "B=[[1,1],[0,1]] eigenspace dimension 1 re-computed. Lab counts 3 of 3, det 6, rank 1 match output."),
    ("cards-L04", "L04 (19 cards) read against L04 text", "M3-c063..c078, c189, c190, c192",
     "Lemma 1.3, Lemma 1.4, Lemma 2.1, Lemma 2.2, Thm 2.3, Prop 2.4, Cor 2.5, Remark 2.7 (inner product 1/sqrt2 re-computed), "
     "Ex 2.6 decomposition re-computed. Lab counts 200/200 x4, 1200 pairs, 1200/1200 match output."),
    ("cards-L05", "L05 (28 cards) read against L05 text", "M3-c079..c100, c173, c176, c179, c180, c193, c203",
     "Ex 1.7 form -2 re-computed; Remark 1.8 form x1^2+x2^2 and eigenvalues 1 +- i re-computed; Remark 3.2 eigenvalues 0,1,3 and "
     "eigenvector (1,1,-1) re-computed; grid count 118 = 59+59 re-derived. Lab outputs (118/360, 4 zeros, 500/500, 100000/100000) match."),
    ("cards-L06", "L06 (14 cards) read against L06 text", "M3-c101..c114, c178",
     "Prop 2.1, Thm 2.2, Thm 2.3, Prop 2.4, Remark 2.5, Lemma 1.3 cited correctly; Remark 2.5 I_2 example [[0,1],[1,0]] re-checked; "
     "A=[[0,1],[0,0]] singular values 1,0 re-computed. Lab values 2.2335, 0.9250, 0.3348 and rank count 2 match output."),
    ("cards-L07", "L07 (20 cards) read against L07 text", "M3-c115..c129, c168, c177, c194..c196",
     "Thm 1.2(a)-(c), Thm 1.3, Remark 1.4, Thm 2.2(a)-(c) match; P=diag(1,0) for A=(1,0)^T re-computed; Lab numbers 1.3325, 0.8488, -0.4120, "
     "residual 0.8951, rank 2 match output; A^T y = (18.38, 3.10, -17.60) re-computed for E2."),
    ("cards-L08", "L08 (23 cards) read against L08 text", "M3-c130..c145, c174, c186, c197..c201",
     "Prop 1.1, 1.2, Def 1.3, Thm 1.4, Thm 2.1(a)(b), Cor 2.2, Prop 2.3, Remark 2.4 match; Lab 75.9/18.1/5.2, cosines 0.9994/0.9985/0.9990, "
     "0.7587 -> 0.9791 match output; c145 claim (generator scale 8 on level) matches code."),
    ("cards-L09", "L09 (27 cards) read against L09 text", "M3-c146..c167, c175, c181..c183, c185, c202",
     "Def 1.1, 1.2, Lemma 1.3, Def 2.1, Remark 2.2, Ex 2.3 (x^TC0x=-2.4), Def 3.1, Prop 3.2-3.5, Ex 3.6 (A0 = 1.1 block; clip distance 0.04; "
     "R-distance 0.08) re-computed; C0 clip distance 0.64 and R entries 0.5 re-computed; lab counts 23/40, 23/23 and 0.175527/0.163280 match output."),
]
for rid, check, ids, text in cards_by_lesson:
    row(rid, check, ids, "PASS", text)

row("notation-registry", "every symbol vs notation/notation.json (T, R^*, Phi, gamma_3, gamma_4, R_f, Q-blackboard, macros)",
    "course/modules/M/M3/*.html", "PASS",
    "T used as the number of observations of a sample (L08), consistent with the registered meaning; no registered symbol "
    "(Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, mathbb Q) is used in M3. Registered macros used (\\R, \\diag, \\tr) keep their meanings. "
    "Lesson-local letters (P, Q, V, M, C, D, L, S) are defined where used and are not registered. Standard TeX operators (\\ker, \\dim, \\langle) "
    "are not registry macros and were not treated as violations.")
row("hours-arithmetic", "hub split and lesson hours (rulings: hours are design targets; fail only arithmetic inconsistency)",
    "course/modules/M/M3/index.html; L01..L09 data-hours; project.html data-hours-project", "PASS",
    "Lessons 12+11+12+12+12+11+11+12+12 = 105 = index data-hours-lessons; project 45; total 150. Project time-budget table components "
    "2+3+14+8+12+6 = 45 (project.html time budget).")

# --- lesson prose and mathematics (text read in full)
lesson_rows = [
    ("prose-L01", "L01 prose, proofs, quiz and lab claims", "course/modules/M/M3/L01.html",
     "Lab 1 claims (a)-(e) and 'Predicted' statements match counts; Lemma 1.3, Prop 3.5, Thm 3.7/3.8, Prop 3.12 proofs checked; M1-M3, P1-P3, E2 solutions re-computed; quiz answers correct."),
    ("prose-L02", "L02 prose, proofs, quiz and lab claims", "course/modules/M/M3/L02.html",
     "Ex 4.3 AP and P^-1AP re-computed; identity-map matrix [[1,-1],[0,1]] re-computed; M1 matrix [[2,-1],[1,0]], M2 coordinates (2,1), R3 differentiation matrix re-computed; lab 50/50 counts and 7 rejections match the printed output."),
    ("prose-L03", "L03 prose, proofs, quiz and lab claims", "course/modules/M/M3/L03.html",
     "Ex 1.6, Remark 1.7, Ex 2.5, Prop 2.6, misconceptions, M1-M3, P1-P3, E2, R2, R3 (A^3=[[27,26],[0,1]]) re-computed; Lab eigenvalues 2,3,5 and rank 1 match output."),
    ("prose-L04", "L04 prose, proofs, quiz and lab claims", "course/modules/M/M3/L04.html",
     "Theorem 2.3 induction, Lemma 2.1 symmetry step, Prop 2.4, Cor 2.5, Ex 2.6 (x^TAx=2), Remark 2.7, M1-M3 (M3 value 6), R1 z=(1,-i) re-computed; lab counts match."),
    ("prose-L05", "L05 prose, proofs, quiz and lab claims", "course/modules/M/M3/L05.html",
     "Ex 1.7, Remark 1.8, Thm 2.1/2.2 proofs, Prop 2.3, Ex 2.5 (B^TB=A), Ex 2.6, Remark 3.2, M1-M3, E1-E3, R1-R3 re-computed; grid argument (120 deg, 59+59=118, 0.3278) re-derived. "
     "Minor, not a FAIL: quiz 'Which of these is PSD' answer does not name the correct option explicitly (infers from 'Its eigenvalues are 1 and 3')."),
    ("prose-L06", "L06 prose, proofs, quiz and lab claims", "course/modules/M/M3/L06.html",
     "Theorem 2.2 Steps 1-5, Thm 2.3 similarity argument, Prop 2.4 trace identity, Remark 2.5, M1 (diag(3,4) SVD), M2, M3, E2 (rank <= 2), E3 (sigma=5), R1 proof, R3 re-computed."),
    ("prose-L07", "L07 prose, proofs, quiz and lab claims", "course/modules/M/M3/L07.html",
     "Thm 1.2(a)-(c), Thm 1.3, Thm 2.2, M2 normal equations (beta=(7/6,1/2)), fitted values and residuals re-computed; P1-P3, R1-R3 proofs correct; lab print values match."),
    ("prose-L08", "L08 prose, proofs, quiz and lab claims", "course/modules/M/M3/L08.html",
     "M1 (4,7;7,13; trace 17; det 3; eigen (17 +- sqrt277)/2), M2, M3, P1-P3, E1 bound 100*13.6818/(88.2028+99*13.6818) = 0.9483 re-computed, E3 sum 99.2 bound 0.15, R1-R3 proofs re-derived; shares 75.9/18.1/5.2 match output."),
    ("prose-L09", "L09 prose, proofs, quiz and lab claims", "course/modules/M/M3/L09.html",
     "Lemma 1.3, Prop 3.2-3.5, Ex 2.3, Ex 3.6, Method 2 description matches code, M1-M3 (M3: 4,2;2,9 eigen (13 +- sqrt41)/2; C12=1/3), P1-P3, E2 (sqrt0.96=0.9798), E3 (0.5), R1-R3 re-computed. "
     "Defect logged under dag-m4-concepts-by-name (definition uses the M4 concept 'correlation' by name)."),
    ("project-numbers", "project.html Lab 3 reference numbers and every printed value quoted in the brief, exemplars and lab prose",
     "course/modules/M/M3/project.html lines for Lab 3, Exemplars A and B, Appendix", "PASS",
     "Lab 3 run output (run_labs twin): smallest eigenvalue -0.142113; distances 0.176573 / 0.175003 / gap 0.001570; max entry diff 0.011516; "
     "diagonal deviations 0.000000; determinant -0.261600; weights 1.778929, -1.096718, -0.255613, 0.573402 summing to 1.000000. "
     "Every quoted value in the lab prose, Exemplar B and the Appendix equals the output; Exemplar A's 0.99 sum (1.78-1.10-0.26+0.57) re-computed."),
    ("project-proof-A1", "project Appendix A1 (clipping gives PSD)", "project.html Appendix A1", "PASS",
     "Spectral decomposition, X = V diag(max(Lambda_ii,f)) V^T, z^TXz = sum max(Lambda_ii,f)(V^Tz)_i^2 >= 0 for f >= 0; hypothesis F1-F4 and Theorem 2.3 of L04 (exists, L04 line 130) named."),
    ("project-proof-A2", "project Appendix A2 (rescaling keeps PSD and gives unit diagonal)", "project.html Appendix A2", "PASS",
     "Y_ii = X_ii/(sqrt(d_i))^2 = 1; q = D^{-1/2} z gives z^TYz = q^TXq >= 0; positivity of d_i named as the hypothesis of the division."),
    ("project-proof-A3", "project Appendix A3 (two-asset weights and scaling)", "project.html Appendix A3", "PASS",
     "Sigma diag a^2,b^2, off rho ab, det = a^2b^2(1-rho^2) > 0 for |rho|<1, a,b>0; Sigma^{-1}iota = (b(b-rho a), a(a-rho b))/det; sum a^2+b^2-2rho ab = (a-b)^2+2ab(1-rho) > 0; "
     "scaling by c^2 cancels. All re-derived."),
    ("project-proof-A4", "project Appendix A4 (clipped matrix singular; rescaled and Sigma singular)", "project.html Appendix A4", "PASS",
     "X u_i = V Lambda_0 e_i = 0 for lambda_i < 0 (u_i column of V); z = D^{1/2}u_i gives Yz = 0 under positive diagonal; Sigma S^{-1}z = S Y z = 0. Hypotheses named."),
    ("project-rung-labs", "project rungs 1-2: Lab 1 worked example and Lab 2 completion check",
     "project.html Lab 1, Lab 2; course/modules/M/M3/project.html twins", "PASS",
     "Lab 1 printed eigenvalues -0.275297, 1.463830, 1.811467 and repaired row values match the prose; Lab 2 fill-ins (sqrt(d_i d_j) and smallest >= -1e-10) produce the stated verdict on the second matrix (eigenvalue -0.203711). run_labs PASS for project twins."),
    ("project-spec-grader", "project specification and conventions match the grader's assertions",
     "project.html Rung 3 Specification, Conventions; grader/test_project.py", "PASS",
     "PSD tolerances -1e-9 (clip) and -1e-8 (projection) match tests at lines 386 and 466; symmetry 1e-9; weights formula and singular/zero-sum cases unspecified and untested; "
     "ValueError set as in Constraints; 155 tests match page; reference passes 50/50 seeds; starter fails."),
    ("project-exemplars", "project Exemplars A and B: quoted numbers, rubric scoring", "project.html Two exemplars",
     "PASS",
     "Quoted numbers and rounding remarks checked against the lab output (see project-numbers). The official scores (A: 2,2,2,1,2; B: 4,4,4,3,3) were NOT independently re-scored by this verifier; the rubric's descriptors were read. Honest gap, not a finding."),
    ("project-hours", "project hours: budget sums to the hub's 45 and the 150 module total",
     "project.html time budget; index.html", "PASS", "2+3+14+8+12+6 = 45; index hub project 45; lessons 105; 105+45 = 150."),
    ("project-references", "project reading list names no passage locator", "project.html Reading", "PASS",
     "Axler (2024) and Strang (2023) with 'No passage locator ... has been confirmed'; registry keys checked by verify_refs --offline (0 problems)."),
]
for entry in lesson_rows:
    if len(entry) == 4:
        rid, check, loc, text = entry
        row(rid, check, loc, "PASS", text)
    else:
        rid, check, loc, status, text = entry
        row(rid, check, loc, status, text)

# --- mutants and alternatives summary entries
mutants = [
    {"id": "vd1_01_comparison_weights_refuses_non_psd_correlation", "description": "comparison_weights refuses a correlation matrix that is not PSD, though the formula does not need PSD (conventions: 'The formula does not require C to be PSD').",
     "killed_by": "seed 0: test_lab3_reference_numbers_are_matched"},
    {"id": "vd1_02_clip_repair_refuses_negative_floor", "description": "clip_repair raises ValueError for a negative floor; the signature allows any floor and the page names no such condition.",
     "killed_by": "seed 0: test_clip_repair_negative_floor_keeps_eigenvalue_above_it"},
    {"id": "vd1_03_is_psd_refuses_zero_diagonal_entry", "description": "is_psd returns False whenever a diagonal entry is exactly zero, although diag(0,1,1) is PSD by the page's definition.",
     "killed_by": "seed 0: test_non_square_is_refused[three_rows_two_columns-is_psd] (artifact: IndexError from unvalidated indexing, not the zero-diagonal rule)"},
    {"id": "vd1_04_min_eigenvalue_uses_only_upper_triangle_for_symmetry", "description": "_as_matrix checks symmetry only for pairs in row 0, so asymmetry in later rows is accepted.",
     "killed_by": "seed 0: test_asymmetry_beyond_tolerance_is_refused[1-2-1.0-min_eigenvalue]"},
    {"id": "vd1_05_is_psd_zero_diagonal_checked_after_validation", "description": "is_psd returns False for an exactly zero diagonal entry after validation (fair version of vd1_03); the rule itself is wrong.",
     "killed_by": "seed 0: test_is_psd_one_by_one (is_psd([[0.0]]) must be True)"},
    {"id": "equivalent-r11d_m02_projection_stops_on_step_only", "description": "ruled-equivalent: projection_repair stops on the step alone; SURVIVES grader seeds 0-9; ruling confirmed (project.html names no stop criterion).",
     "killed_by": "SURVIVES (ruled equivalent; confirmed)"},
    {"id": "equivalent-r6d_m04_projection_stops_on_gap_only", "description": "ruled-equivalent: projection_repair stops on the gap alone; SURVIVES seeds 0-9; ruling confirmed.",
     "killed_by": "SURVIVES (ruled equivalent; confirmed)"},
    {"id": "equivalent-r15d_m03_projection_repair_no_final_symmetry", "description": "ruled-equivalent by its file: projection_repair never stops before max_iter (the file's only change is 'and False' in the stop test), not 'no final symmetry' as its name says; SURVIVES seeds 0-9; ruling confirmed, label wrong (see equivalent-r15d-m03-label).",
     "killed_by": "SURVIVES (ruled equivalent; confirmed; label FAIL)"},
    {"id": "suite-existing-123", "description": "The 123 pre-existing mutant files in ledgers/M3/mutants (rounds 2-18) re-run on seeds 0-9: all killed.",
     "killed_by": "mutate_graders M3 seeds 0-9: 128/128 killed in total including the five new files"},
]

fragment = {
    "unit": "M3",
    "slice": "M3-d",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for M3-d, round 1 (did not build M3; share no context with the builders)",
    "pin": "d0f39c0",
    "base": "none: first independent verification of slice d in this round; the previous M3-d fragment (round 18, verdict FAIL, pin 8f80909) was backed up to /tmp/m3d_prev_fragment_round18.json before being replaced",
    "checkout": str(ROOT),
    "scratch": str(ROOT / "ledgers/M3/scripts/M3-d-r1"),
    "verified_at": "2026-11-02T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 1 on pin d0f39c0. Read in full: rules, project.html (text extract and raw HTML for Appendix A3/A4), grader instance.py, reference.py, starter.py, "
        "L01-L09 lesson text and cards (all 200 cards read against their lesson). Partly read: grader/test_project.py (named-condition, purity, count and "
        "mutation evidence, not every assertion line). Not independently recomputed: seeded simulation counts (L01 188/200 etc., L09 23/40, L08 shares) were "
        "confirmed by running the lab's own code (run_labs) and comparing with prose and cards, not by a separate implementation. Not re-scored: the rubric "
        "scores of Exemplars A and B. Not run: tools/render_curriculum.py, build_site.py --check, fetch_data.py --check, the whole pytest suite and "
        "verify_refs live (no curriculum, site-data, market or reference input changed; no live run requested). Non-PASS rows: dag-m4-concepts-by-name, "
        "cards-id-sequence, equivalent-r15d-m03-label. Minor, not rows: L05 quiz answer does not name its correct option; L02 Section 5 basis-order sentence "
        "is correct but compressed."
    ),
    "summary": (
        "M3-d round 1: verdict FAIL. Rows: %d total, %d PASS, %d FAIL. Gates (check_pages, check_dag, check_projects, run_graders 0-49, run_labs 12/12, "
        "page_smoke for project and all lessons, ruff, mypy, verify_refs offline, collect-only 155, mutate_graders 128/128 on seeds 0-9, six alternatives) all "
        "pass. Equivalent rulings r11d and r6d confirmed; r15d ruling holds but its label is wrong. FAILs: (1) M4 concepts 'correlation', 'covariance matrix', "
        "'standard deviation', 'Gaussian' used by name in L09, project.html and starter.py without a recorded architect decision (plan B1); (2) card ids not sequential "
        "(gaps 102, 148, 191; out-of-order ids)."
    ) % (len(rows), sum(1 for r in rows if r["status"] == "PASS"), sum(1 for r in rows if r["status"] != "PASS")),
}

OUT.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", OUT, len(rows), "rows")
