"""Verifier r4: writes the slice c fragment (ledgers/M3/M3-c.json) from the rows checked in this round."""
import json
import sys
from datetime import UTC, datetime

S = "ledgers/M3/scripts/M3-c-r4"
L = f"{S}/"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


row("GATE-01", "2.9-gate", "tools/check_pages.py --unit M3 (and --page L07, L08, L09)", "PASS",
    f"'check_pages M3: PASS' EXIT=0 ({L}check_pages_M3.log); 'check_pages M3 L07|L08|L09: PASS' ({L}check_pages_L07.log, _L08.log, _L09.log), each EXIT=0.")
row("GATE-02", "2.9-gate", "tools/check_dag.py --unit M3", "PASS",
    f"'check_dag M3: PASS' EXIT=0 ({L}check_dag_M3.log).")
row("GATE-03", "2.6-gate", "tools/check_projects.py --unit M3", "PASS",
    f"'check_projects M3: PASS' EXIT=0 ({L}check_projects_M3.log). Project content is slice d and is not read here.")
row("GATE-04", "2.5-labs", "tools/run_labs.py --unit M3 and --unit M3 --page L07/L08/L09", "PASS",
    f"'run_labs M3: PASS (12/12)' EXIT=0 ({L}run_labs_M3.log); '(1/1)' PASS for L07, L08, L09 ({L}run_labs_L07.log, _L08.log, _L09.log).")
row("GATE-05", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py run alone", "PASS",
    f"Each twin run as `python -I -W error <twin>` from an empty tempdir under /private/tmp: exit 0, stderr 0 bytes, stdout equals the page's expected block (rstrip) for all three ({L}twin_vs_page_r4.log).")
row("GATE-06", "2.5-labs", "ruff check and ruff format --check tests/labs/M3", "PASS",
    f"'All checks passed!' EXIT=0 ({L}ruff_check.log); '12 files already formatted' EXIT=0 ({L}ruff_format.log).")
row("GATE-07", "2.5-labs", "mypy --no-incremental (repository configuration)", "PASS",
    f"'Success: no issues found in 331 source files' EXIT=0 ({L}mypy.log).")
row("GATE-08", "2.9-smoke", "tools/page_smoke.py --unit M3 --page L07, then L08, then L09 (each alone)", "PASS",
    f"'page_smoke M3: PASS' EXIT=0 for each page run alone ({L}page_smoke_L07.log, _L08.log, _L09.log); lab timings 0.0 s.")
row("GATE-09", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
    f"'offline integrity: 560 entries, 0 problems' EXIT=0 ({L}verify_refs_offline.log). No reference changed in slice c, so no live run.")
row("GATE-10", "2.5-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k 'M3 or run_labs or page'", "PASS",
    f"Progress shows 269 tests (72+72+72+53 dots), no F or E, EXIT=0 ({L}pytest_slice.log). The summary line is suppressed in this repository's pytest configuration.")
row("GATE-11", "2.6-gate", "tools/run_graders.py --unit M3 --seeds 0-49", "PASS",
    f"'run_graders M3: PASS (reference 50/50 seeds, slowest 0.2 s)' EXIT=0 ({L}run_graders_M3.log). Grader is slice d.")
row("LAB-L07-EMBED", "2.5-labs", "course/modules/M/M3/L07.html section#lab-M3-L07-1 vs tests/labs/M3/lab-M3-L07-1.py", "PASS",
    f"Page code element with data-run equals the twin (rstrip): True; page pre.expected equals the twin's stdout: True ({L}twin_vs_page_r4.log; twin sha256 prefix 80a6f3948f31023f, page L07 re-read at pin 4eb6788).")
row("LAB-L08-EMBED", "2.5-labs", "course/modules/M/M3/L08.html section#lab-M3-L08-1 vs tests/labs/M3/lab-M3-L08-1.py", "PASS",
    f"Page code equals twin (rstrip): True; page expected equals twin stdout: True ({L}twin_vs_page_r4.log; twin sha256 prefix c96726bfd2b00865).")
row("LAB-L09-EMBED", "2.5-labs", "course/modules/M/M3/L09.html section#lab-M3-L09-1 vs tests/labs/M3/lab-M3-L09-1.py", "PASS",
    f"Page code equals twin (rstrip): True; page expected equals twin stdout: True ({L}twin_vs_page_r4.log; twin sha256 prefix ed06fb04314e6c58).")
row("LABSTMT-L07", "2.5-labs", "L07.html Lab 1 hypothesis (line 125), interpretation (line 204), key-results row (line 350), E2 (line 302)", "PASS",
    f"Every printed line (twin_vs_page_r4.log) matches the statements: six True identities at 1e-9; coefficients 1.3325 0.8488 -0.4120; residual norm 0.8951; A^T y 18.38 3.10 -17.60 (the vector the hypothesis now lists); dup rank 2 of 3 and null-direction equality True. Independent QR and SVD recomputation ({L}independent_numbers_r4.log): beta 1.33251885 0.84881149 -0.41196372, residual 0.8951276, A^T y 18.37970, 3.09586, -17.60350.")
row("LABSTMT-L08", "2.5-labs", "L08.html Lab 1 hypothesis (line 146) and Definition 3.1 (line 141); tests/labs/M3/lab-M3-L08-1.py lines 11-12 and 96", "PASS",
    f"Round-3 FAIL resolved. Code line 96 is now np.abs(v.T @ shape) (all six components), matching the hypothesis 'largest absolute cosine' and the docstring. Printed cosines 0.9994, 0.9985, 0.9990 and 'three matches distinct: True' are reproduced by an independent SVD computation ({L}independent_numbers_r4.log: |cos| level 0.999381 at PC1, slope 0.998544 at PC2, curvature 0.999019 at PC3, next-largest 0.0321 or less).")
row("LABSTMT-L09", "2.5-labs", "L09.html Lab 1 hypothesis (line 193), interpretation (line 349), key-results rows (lines 499-500); twin lines 1-20 and 117-139", "PASS",
    f"Counts 23/23/23 and distances 0.175527 and 0.163280 reproduced by an independent implementation (eigh-free clipping, own loop; {L}independent_numbers_r4.log: 23 non-PSD, 23 W feasible, 23 closer, first index 0). 'Up to that tolerance' qualifiers are on the page (lines 349, 375).")
row("LABDOC-L09", "2.5-labs", "tests/labs/M3/lab-M3-L09-1.py lines 16-19 (docstring) and 125-128 (code)", "PASS",
    f"Round-2 defect remains resolved: the closer counter is inside 'if is_correlation(alt):' (twin lines 125-128) and the docstring says 'where W passes is_correlation and is strictly closer'. Subject unchanged since round 3 (no delta line in {L}delta_slice_c_a007712_to_4eb6788.diff); re-derived this round.")
row("LABDOC-L09-TOL", "2.5-labs", "tests/labs/M3/lab-M3-L09-1.py lines 16-19 (docstring); compare course/modules/M/M3/L09.html line 349 and twin lines 71-76", "FAIL",
    f"The docstring says the lab 'shows that R is not the nearest correlation matrix to A in each instance where W passes is_correlation and is strictly closer to A than R', with no tolerance. is_correlation (twin lines 71-76) checks symmetry and unit diagonal to 1e-12 and smallest eigenvalue at least -1e-8, so W is only approximately a correlation matrix; the nearest-matrix conclusion holds to that tolerance, as page line 349 says ('So, to that tolerance, R is not the nearest correlation matrix'). The margin in the 23 instances is 3.86e-05 (min of ||A-R||_F - ||A-W||_F in {L}independent_numbers_r4.log), so the claim is true in practice but the docstring omits the qualifier.",
    fix="In twin lines 16-19 change 'It shows that R is not the nearest correlation matrix to A in each instance where ...' to 'It shows, to the tolerance of is_correlation, that R is not the nearest correlation matrix to A in each instance where ...'. Then re-embed with tools/embed_labs.py course/modules/M/M3/L09.html --refresh lab-M3-L09-1 and rerun run_labs --unit M3 --page L09.")
row("LABSTMT-L09-RUNTIME", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py (imports, seeds, runtime)", "PASS",
    "Imports are numpy (and numpy.typing) only; seeds 7, 8 and 20261028 are fixed; no network calls in the twins; page_smoke lab timings 0.0 s each ({L}page_smoke_L07.log, _L08.log, _L09.log).")
row("NUM-L07", "2.2-numbers", "L07.html E2 solution (line 302) quoting A^T y", "PASS",
    f"Round-3 FAIL resolved. The vector is now stated as the value Lab 1 prints ('the lab prints A^T y = (18.38, 3.10, -17.60) to two decimals', twin_vs_page_r4.log line 'A^T y, printed to 2 decimals: 18.38 3.10 -17.60'). Independent recomputation gives 18.379697, 3.095863, -17.603498 ({L}independent_numbers_r4.log), which round to the printed values.")
row("NUM-L08", "2.2-numbers", "L08.html printed shares (line 284), cosines, E1 bound (line 375-377), E3 (line 391), key rows (433-434), Remark 2.4 (line 132), misconception (line 304)", "PASS",
    f"Unrounded shares 0.75872815, 0.18088840, 0.05161927 round to 75.9, 18.1, 5.2 ({L}independent_numbers_r4.log). First share after tenor-1 column x10: 0.97914488, rounds to 0.9791; before 0.75872815 rounds to 0.7587. M11 13.681775 rounds to 13.6818; trace 88.202753 rounds to 88.2028. Bound 100 M11/(trace+99 M11) = 0.9483461 rounds to 0.9483, and the rounded inputs 13.6818 and 88.2028 give 0.9483462. Shares 75.9+18.1+5.2 = 99.2 vs unrounded top-three sum 99.1236; difference 0.076, within the 0.15 bound of E3. Cosines 0.999381, 0.998544, 0.999019 round to 0.9994, 0.9985, 0.9990. Doubled-panel shares agree to 1.1e-16.")
row("NUM-L09", "2.2-numbers", "L09.html witness (line 106), Example 2.3, E1, E2 (line 447), interpretation (line 349), R entries", "PASS",
    f"Recomputed in {L}independent_numbers_r4.log: x^T C0 x = -2.4; C0 eigenvalues -0.8, 1.9, 1.9; ||C0-B||_F^2 = 0.64 = sum of squared negative eigenvalues; R = [[1,.5,.5],[.5,1,-.5],[.5,-.5,1]]; ||C0-R||_F = sqrt(0.96) = 0.9798; first non-PSD distances 0.175527 (R) and 0.163280 (W).")
row("NUM-L07-M", "2.2-numbers", "L07.html line 222 (residual norm 0.8951), E3 (intercept 1.3325)", "PASS",
    f"Independent QR recomputation: residual norm 0.8951275..., beta0 1.33251885 ({L}independent_numbers_r4.log).")
row("MATH-L07", "2.4-mathematics", "L07.html Definition 1.1, Theorems 1.2, 1.3, 2.2, Remark 1.4, Proofs lines 73-121; Problems lines 236-338", "PASS",
    "Each proof re-derived line by line: G symmetric with x^T G x = ||Ax||^2 > 0 gives invertibility via the spectral theorem (L04 Theorem 2.3) and VV^T = I (L06 Fact 1.2, L06.html line 64); existence (b) and uniqueness of the projection; P symmetric and idempotent; closest-point strict inequality; Pythagorean identity; least squares equals projection. Numeric check of P symmetry and idempotence to 1e-16 in independent_numbers_r4.log.")
row("MATH-L08", "2.4-mathematics", "L08.html Propositions 1.1, 1.2, 2.3, Theorems 1.4, 2.1(a)(b), Corollary 2.2, Remark 2.4; lines 60-133", "PASS",
    "Every proof re-derived: M symmetric PSD; trace identity; Z^T Z = (T-1) Lambda; Rayleigh bounds with equality cases; (b) by the coefficient identity; Corollary 2.2; scaling by c^2 (c != 0); Remark 2.4 (M_jj > 0 from the 2t M_jl + t^2 M_ll test, then kappa = c forces c^2 = c, false for c != 0,1). Definition 3.1 uses a maximum that needs uniqueness (see DEF-L08-MATCH).")
row("MATH-L09", "2.4-mathematics", "L09.html Lemma 1.3, Propositions 3.2(a)(b), 3.3(a)(b), 3.4, 3.5, Examples 2.3 and 3.6; lines 73-181", "PASS",
    "Every proof re-derived: Lemma 1.3 (trace-cyclicity step checked index by index); Prop 3.2 eigenvalues and quadratic form >= eps ||x||^2; Prop 3.3(a) squared distance formula including the lambda_i < eps branch; Prop 3.4 congruence argument; Prop 3.5 with delta = |b_ij|/(1+b_jj) and the bracket bound; Example 3.6 eigenpairs, A_0 = 1.1 times the all-ones 2x2 matrix, R = all-ones, ||A-A_0||_F^2 = 0.04, ||A-R||_F^2 = 0.08.")
row("PROB-L07", "2.2-problems", "L07.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (lines 241-336)", "PASS",
    "All twelve worked solutions re-derived: M1 P=(1/2)[[1,1],[1,1]], p=(1,1); M2 beta=(7/6,1/2), fitted 7/6, 5/3, 13/6, residuals -1/6, 1/3, -1/6; M3 25=9+16; P1-P3 valid; E1-E3 correct (E2 by the printed vector; E3 intercept as fitted value at zero regressors); R1 uniqueness and existence via a maximal independent list, length bound by L01 Theorem 3.7 (L01.html line 161); R2 linearity; R3 projection identities.")
row("PROB-L08", "2.2-problems", "L08.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (lines 324-418)", "PASS",
    "All twelve solutions re-derived: M1 centred rows (-2,-3),(0,-1),(2,4), M=[[4,7],[7,13]], trace 17, det 3, eigenvalues (17 +- sqrt277)/2; M2 2/3, 1/6, 1/6; M3 18/27, 9/27; P1-P3 valid; E1 bound algebra (100 M11/(S0+99 M11)); E2; E3 (sum 99.2, +-0.15); R1 tie maximisers equal the eigenspace; R2 column shift; R3 spectral decomposition of M = B G B^T with W = BQ.")
row("PROB-L09", "2.2-problems", "L09.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (lines 386-481)", "PASS",
    "All twelve re-derived: M1 eigenvalues 1.6, 0.4; M2 4.88 = 1+1.44+1.44+1 = 2.2^2+0.2^2; M3 characteristic polynomial lambda^2-13 lambda+32, roots (13 +- sqrt41)/2 both positive, C entries 1/3; P1 |C_ij|<=1 by t = +-1; P2 trivial null space; P3 convexity; E1 -2.4 term by term (-1.8 x 3 = -5.4); E2 sqrt(0.96) = 0.9798; E3 0.25 and 0.5; R1 split of the squared norm; R2 diag(1,4) to identity; R3 norm identity.")
row("GRADE-L07", "2.3-grades", "L07.html grade spans and key-results table (lines 64, 84, 108, 346-350)", "PASS",
    "Theorems 1.2, 1.3, 2.2 and Remark 1.4 graded T and proved on the page; the seeded-design row (line 350) is graded C and names 'Lab 1 output (finite numerical check ... not the proof)'.")
row("GRADE-L08", "2.3-grades", "L08.html grade spans and key-results table (lines 61, 71, 85, 100, 121, 428-434)", "PASS",
    "Propositions 1.1, 1.2, 2.3, Theorems 1.4 and 2.1, Corollary 2.2 graded T with proofs; the simulated-panel rows (lines 433-434) are graded C and name Lab 1 output.")
row("GRADE-L09", "2.3-grades", "L09.html grade spans and key-results table (lines 73-160, 491-500)", "PASS",
    "Lemma 1.3, Propositions 3.2 to 3.5, Example 3.6 graded T; the seeded 23-of-40 and distance rows (lines 499-500) are graded C and name Lab 1 output.")
row("CITE-L07-L09", "2.1-citations", "L07.html, L08.html, L09.html (data-cite, data-locator, author or source names)", "PASS",
    f"grep count of data-cite and data-locator: 0 in each page; no author or source name (Litterman, Higham, Eckart, Nelson, Strang, Axler, Gurkaynak absent) ({L}prose_and_tie_r4.log). L07 line 430 and L08 line 518 state that no outside source is used; L09 has an empty reference list.")
row("XREF-EARLIER", "2.4-mathematics", "L07, L08, L09 cross-references to earlier lessons", "PASS",
    "Each target read in its earlier lesson: L01 Theorem 3.7 (L01.html line 161, spanned list); L01 subspace test Prop 1.4; L03 Definition 1.1 (eigenvalue); L04 Assumptions F1-F4 and Theorem 2.3 (spectral theorem, L04.html line 130); L04 null space (L04.html line 62); L05 Theorem 2.1 (eigenvalue test for PSD, L05.html line 108, matches the L09 M1 solution); L05 Definition 1.4 (dfn at L05.html line 72); L06 Definition 1.1 and Fact 1.2 (QQ^T = I, L06.html line 64); L06 inner product and orthogonality (L06.html line 56); L06 Remark 2.5 sign freedom; L07 Theorem 1.2 (L07.html line 64) cited by L08.")
row("NOTATION-R", "2.4-notation", "L07, L08, L09 math", "PASS",
    f"No \\mathbb in the three pages ({L}prose_and_tie_r4.log macro lists). \\R used via the registered macro (notation.json macros: \\R -> \\mathbb{{R}}).")
row("NOTATION-OPNAME", "2.4-notation", "L08.html line 402 (\\operatorname{span}); L09.html line 171 (\\mathrm{sign}); \\tr and \\diag throughout", "PASS",
    "Registered macros \\tr and \\diag are used. \\operatorname and \\mathrm are standard TeX commands, not project macros; neither produces a registered symbol. The reading that the registry binds project macros only is the one the registry itself uses (\\top, \\lVert, \\cos are unregistered and used throughout).")
row("NOTATION-T", "2.4-notation", "L08.html Section 1 (T x n matrix, T >= 2, T = 750)", "PASS",
    "notation.json symbol T means 'number of return observations (periods) in a sample'; in L08 T is the number of observations (rows) of the panel, the same meaning.")
row("NOTATION-AST", "2.4-notation", "L09.html line 93 (C^{\\ast})", "PASS",
    "Registered symbol is R^{\\ast} (AP1 SDF return), a different letter; C^{\\ast} collides with no registered symbol.")
row("NOTATION-Q", "2.4-notation", "L07.html and L09.html (orthogonal Q)", "PASS",
    "Plain Q (orthogonal matrix) is not the registered \\mathbb{Q} (AP1 probability measure); no \\mathbb in the three pages.")
row("NOTATION-OTHER", "2.4-notation", "all control sequences in L07-L09 math (macro counts in prose_and_tie_r4.log)", "PASS",
    "Control sequences are standard TeX or KaTeX or registered (\\R, \\tr, \\diag). Local letters (gamma, alpha, beta, tau, iota, kappa, delta, Gamma, Lambda) are conventionally local and are defined where used (notation.json 'about'); gamma for the column-space coefficient is defined in L07 line 56 ('{A gamma : gamma in R^k}'); no registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}) is given another meaning.")
row("DEF-L08-CLOSE", "2.9-structure", "L08.html Definition 3.1 (line 141), quiz item L08q9 (line 505) and explanation (line 511)", "PASS",
    "Round-3 FAIL resolved. The label is now the principal direction that attains the largest |cos(v_k, f_j)|, with no undefined threshold. The quiz stem, the correct option and the explanation (line 511) use the same definition.")
row("DEF-L08-MATCH", "2.9-structure", "L08.html Definition 3.1 (line 141): 'the principal direction v_k with the largest |cos(v_k, f_j)|'; canon-break line 292; quiz explanation line 511",
    "FAIL",
    f"Definition uses the definite article, so it presumes a unique maximiser, which is not guaranteed. Counterexample ({L}prose_and_tie_r4.log, 'tie check'): M = diag(3, 2, 1) with principal directions e1, e2, e3 and shape f = (e1+e2)/sqrt(2): |cos(v1,f)| = |cos(v2,f)| = 0.70710678 is the maximum, attained by two directions, so the match and the 'level-like' / 'slope-like' / 'curvature-like' label are undefined. The lab's planted shapes have no tie (best cosines 0.9994 vs next 0.0321), so the printed results are unaffected; the defect is in the definition, which is applied to real data in canon-break line 292.",
    fix="In Definition 3.1 replace 'The match of f_j is the principal direction v_k with the largest ...' by: 'f_j has a match when exactly one principal direction attains the largest |cos(v_k, f_j)|; in that case the match is that direction, and otherwise f_j has no match and no label is given.' Make the same condition explicit in the explanation of L08q9 (line 511).")
row("DAG-LINKS", "2.9-structure", "L07.html, L08.html, L09.html lines 38-39; dfn ids", "PASS",
    f"check_dag M3 PASS ({L}check_dag_M3.log). Targets exist: L01.html#def-vector-space (line 57), L03.html#def-eigendecomposition (line 109), L04.html#def-spectral-theorem (line 130), L05.html#def-positive-semidefinite-matrix (line 72). The dfn ids of the three pages are unique ({L}prose_and_tie_r4.log: def-orthogonal-projection, def-least-squares-projection, def-principal-component-analysis, def-level-slope-curvature, def-nearest-correlation-matrix, def-eigenvalue-clipping).")
row("DAG-M4", "2.9-structure", "L07.html, L08.html, L09.html (covariance, variance, correlation, Gaussian, standard deviation wording)", "PASS",
    "No link to an M4 concept on the three pages. 'correlation' (L09), 'standard deviation' (L07 lines 204, 295) and 'Gaussian' (L09 twin docstring) appear as plain prose, which FINAL-ARCHITECT-RULINGS item 3 allows; 'covariance' does not appear (L08 uses the centred cross-product matrix M).")
row("DAG-PSD-REDEF", "2.9-structure", "L09.html line 56 (Section 1 restates the definition of positive semidefinite) versus L05.html line 72 (dfn)",
    "FAIL",
    "L09.html line 56 says 'a symmetric C is positive semidefinite, written PSD, when x^T C x >= 0 for every vector x (Lesson 5)'. The registered concept positive-semidefinite-matrix is defined in L05 with <dfn id=\"def-positive-semidefinite-matrix\">, and L09 already links it in its Uses line (L09.html line 38). BUILDER_RULES 1.10 says: if a prerequisite already defines a concept, link to that definition instead of redefining it. This is a second definition in prose, and the why-it-matters paragraph (line 52) says PSD is 'defined in Section 1'. (Restatements of symmetric and trace are not registered concepts and are not counted.)",
    fix="Delete the PSD definition from L09 Section 1 (line 56) and link the concept: <a class=\"concept\" data-concept=\"positive-semidefinite-matrix\" href=\"L05.html#def-positive-semidefinite-matrix\">positive semidefinite</a>. Change 'PSD, defined in Section 1' in the why-it-matters paragraph (line 52) to 'PSD, defined in Lesson 5'.")
row("DEFINE-BEFORE-USE", "2.9-structure", "first uses of tenor, trace, cosine, subspace, column space, orthogonal, null space, PSD, eigenvalue clipping", "PASS",
    "tenor defined L08 line 56 before use; trace defined L08 line 58 before Prop 1.2 and again L09 line 56; cosine defined L08 line 137 before Def 3.1; subspace and column space in L07 line 56; orthogonal matrix in L06 Definition 1.1 (earlier) and L09 Definition 1.2a; null space defined in L04 (L04.html line 62) before its use in L07 P3 and L09 P2; PSD defined in L05 Definition 1.4 (see DAG-PSD-REDEF for the restatement); eigenvalue clipping defined L09 Definition 3.1 before use.")
row("PROSE-PROCESS", "2.9-structure", "L07.html, L08.html, L09.html learner text", "PASS",
    f"prose_and_tie_r4.log: 0 hits for builder, verifier, architect, round, pin, TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly.")
row("PROSE-ELLIPSIS", "2.9-structure", "quiz stems ending in an ellipsis (L07 lines 398 and 412; L08 lines 445, 459, 505; L09 lines 530 and 539)", "PASS",
    "Each ellipsis ends a multiple-choice or numeric stem whose options follow ('the matrix A^T A is...'); it stands for the answer the options supply and omits no text. Not the banned omitted-content ellipsis.")
row("PROSE-SCOPE", "2.2-scope", "scope words in L07-L09: every, all, always, any, only, exactly, for all", "PASS",
    "Each checked against a proof or finite check: 'every full-column-rank design' (L07 Theorem 1.2 proof); 'for any A' (L07 canon-break via R1, any subspace); 'every nonzero c' and 'every data matrix' (L08 Proposition 2.3); 'for all 23' (L09 counts 23 of 23, independent_numbers_r4.log); 'always' appears only in wrong options (L07 quiz 'always invertible', L08 quiz 'always diagonal', 'always the first eigenvector').")
row("STRUCT-WHY", "2.9-structure", "L07, L08, L09 why-it-matters", "PASS",
    "check_pages M3 L07/L08/L09 PASS, which enforces the 120-word limit ({L}check_pages_L0*.log).")
row("STRUCT-ORDER", "2.9-structure", "L07, L08, L09 section order and counts", "PASS",
    "check_pages PASS (order and minimum counts). Read by hand: each page has why-it-matters, numbered sections, a lab with hypothesis, code, expected, interpretation, canon-breaks, three misconceptions, a problem set with three problems in each of the four tiers, each with a details.solution, a key-results table, and a quiz of 9, 9 and 11 items (8 to 15 allowed).")
row("HOURS", "2.9-structure", "L07.html (data-hours 11), L08.html (12), L09.html (12); hub data-hours-lessons 105, data-hours-project 45", "PASS",
    "data-hours of L01..L09 = 12+11+12+12+12+11+11+12+12 = 105 = hub data-hours-lessons; project 45; total 150 = curriculum M3 hours. Plan section 2.2 lists the same values for L07-L09.")
row("DATA-CLAIM", "2.8-data", "L08.html canon-break (line 291) and Lab 1 heading", "PASS",
    f"'the program does not yet embed a multi-tenor series from which three or more tenors can be read': course/assets/data/market/MANIFEST.json datasets: fx_daily (AUD..JPY), fx_monthly (10 currencies), ust_daily (columns tbill_3m, cmt_10y). Only two Treasury series; no tenor series of three or more. Claim verified.")
row("HONEST-GAP", "2.8-data", "L08.html canon-break (line 291) and the lab heading", "PASS",
    "The page says the curriculum's Treasury lab is not run and a SIMULATED six-tenor panel is used; consistent with the MANIFEST listing above. No data-files attribute on L07, L08 or L09.")
row("SIMULATED-LABELS", "2.8-data", "L07 lines 125 and 128; L08 lines 146 and 149; L09 lines 52, 193 and twin docstring lines 9-10", "PASS",
    "Each lab that generates data says SIMULATED in its hypothesis, its docstring and its key-results rows; the L09 matrix C0 is a hand example, not data.")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
fragment = {
    "unit": "M3",
    "slice": "c",
    "round": 4,
    "verifier": "independent Haiku verifier, checkout verifyD4-M3-c",
    "pin": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b",
    "base": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD4-M3-c",
    "scratch": "/private/tmp (empty tempdirs created per twin run and removed; /private/tmp/v4-indep)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice c (L07-L09 pages and lab twins L07, L08, L09), round 4 at pin 4eb6788. Delta read in full: "
        "the round-3 pin a007712f to 4eb6788 changed L07.html (two hunks), L08.html (four hunks) and L09.html (seven hunks), "
        "tests/labs/M3/lab-M3-L07-1.py (+2 lines) and lab-M3-L08-1.py (one line); the diff is archived at "
        f"{L}delta_slice_c_a007712_to_4eb6788.diff. lab-M3-L09-1.py is byte-identical since a007712f. "
        "All three pages were read in full, line by line (L07 443 lines, L08 531, L09 606); both twins were read in full. "
        "Every row was re-derived this round; no round-3 PASS row was carried forward. Round-3 FAIL rows LABSTMT-L08, NUM-L07 and DEF-L08-CLOSE are "
        "now PASS (fixes verified). New FAIL rows: DEF-L08-MATCH, LABDOC-L09-TOL, DAG-PSD-REDEF. "
        "Mutants: none, because slice c is lab and page content and VERIFIER ruling says lab twins are demonstrations; "
        "tools/mutate_graders.py was not run for this slice. Cards.json, project.html, grader/ and the M3 index are other slices and are not checked here."
    ),
    "summary": "",
}
n = len(rows)
npass = sum(1 for r in rows if r["status"] == "PASS")
nfail = sum(1 for r in rows if r["status"] == "FAIL")
nunv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
fragment["summary"] = (
    f"Slice c round 4 at pin 4eb6788: {n} rows, {npass} PASS, {nfail} FAIL, {nunv} UNVERIFIABLE. "
    "All gates pass (check_pages, check_dag, check_projects, run_labs, twins alone under python -I -W error, page code and expected blocks equal the twins, "
    "ruff, mypy strict, page_smoke per page, verify_refs offline, run_graders, pytest slice). "
    "Failures: DEF-L08-MATCH (ties make the 'largest cosine' match undefined; counterexample diag(3,2,1)), LABDOC-L09-TOL (twin docstring omits the is_correlation tolerance), "
    "DAG-PSD-REDEF (L09 Section 1 restates the L05 definition of PSD)."
)
out = "ledgers/M3/M3-c.json"
sys.path.insert(0, "tools")
import ledger  # noqa: E402

problems = ledger.validate(fragment, "M3-c")
print("validate:", problems)
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("wrote", out, "rows", n, "pass", npass, "fail", nfail, "verdict", verdict)
