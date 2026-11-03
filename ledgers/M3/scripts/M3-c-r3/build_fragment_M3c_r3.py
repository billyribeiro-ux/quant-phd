# Writes ledgers/M3/M3-c.json (round 3, slice c). Rows are the verifier's own findings; evidence cites the
# scripts and logs under ledgers/M3/scripts/M3-c-r3/ that back them.
import datetime, json, sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
S = "ledgers/M3/scripts/M3-c-r3/"
P = "course/modules/M/M3/"
rows = []

def row(id_, check, location, status, evidence, fix=""):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})

# ---- gates (run by this verifier on pin a007712f) ----
row("GATE-01", "2.9-gate", "tools/check_pages.py --unit M3 (and --page L07, L08, L09)", "PASS",
    "'check_pages M3: PASS' EXIT=0 (" + S + "check_pages_M3_unit.log); 'check_pages M3 L07/L08/L09: PASS' (" + S + "check_pages_L07-L09.log, check_pages_L08.log, check_pages_L09.log)")
row("GATE-02", "2.9-gate", "tools/check_dag.py --unit M3", "PASS", "'check_dag M3: PASS' EXIT=0 (" + S + "check_dag_M3.log)")
row("GATE-03", "2.6-gate", "tools/check_projects.py --unit M3", "PASS",
    "'check_projects M3: PASS' EXIT=0 (" + S + "check_projects_M3_r3.log). Project content is slice d; not re-read here")
row("GATE-04", "2.5-labs", "tools/run_labs.py --unit M3 and --page L07, L08, L09", "PASS",
    "'run_labs M3: PASS (12/12)' (" + S + "run_labs_M3_all.log); 'PASS (1/1)' for each of L07, L08, L09 (" + S + "run_labs_L07.log, run_labs_L08.log, run_labs_L09.log); all EXIT=0")
row("GATE-05", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py run alone", "PASS",
    "each run alone as python -I -W error from an empty scratch dir (/private/tmp/verifyD3-twin-07, -08, -09): exit 0, stderr 0 bytes, stdout equal to the page's <pre class=\"expected\"> block (" + S + "twin_expected_r3.py, " + S + "twin_expected_r3.log)")
row("GATE-06", "2.5-labs", "ruff check and ruff format --check on the three twins", "PASS",
    "'All checks passed!' EXIT=0 (" + S + "ruff_check_r3.log); '3 files already formatted' EXIT=0 (" + S + "ruff_format_r3.log)")
row("GATE-07", "2.5-labs", "mypy --no-incremental (repository configuration)", "PASS",
    "'Success: no issues found in 331 source files' EXIT=0 (" + S + "mypy_r3.log)")
row("GATE-08", "2.9-smoke", "tools/page_smoke.py --unit M3 --pages L07, then L08, then L09 (each alone)", "PASS",
    "'page_smoke M3: PASS' EXIT=0 for each page alone (" + S + "page_smoke_L07.log, page_smoke_L08.log, page_smoke_L09.log)")
row("GATE-09", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
    "'offline integrity: 560 entries, 0 problems' EXIT=0 (" + S + "verify_refs_offline_r3.log). Live run not performed (no reference changed in slice c)")
row("GATE-10", "2.5-labs", "pytest tests/test_labs.py -k M3; tests/test_run_labs.py; tests/test_page_checks.py", "PASS",
    "pytest exit 0 (" + S + "pytest_labs_M3_r3.log; " + S + "pytest_run_labs_page_checks_r3.log: exit 0 with no F or E marks in the progress line)")
row("GATE-11", "2.6-gate", "tools/run_graders.py --unit M3 --seeds 0-49", "PASS",
    "'run_graders M3: PASS (reference 50/50 seeds, slowest 0.2 s)' EXIT=0 (" + S + "run_graders_M3_r3.log). Grader is slice d")

# ---- labs: embed and demonstration ----
for pg in ["07", "08", "09"]:
    row(f"LAB-L{pg}-EMBED", "2.5-labs", f"{P}L{pg}.html section#lab-M3-L{pg}-1 vs tests/labs/M3/lab-M3-L{pg}-1.py", "PASS",
        f"{S}twin_expected_r3.py: page <code> with data-run equals the twin (rstrip) True; page <pre class=expected> equals the twin's stdout True (" + S + "twin_expected_r3.log). Twin sha256 prefixes 1b027e067f39c7dd (L07), bc40bdd055c56da8 (L08), ed06fb04314e6c58 (L09)")
row("LABSTMT-L07", "2.5-labs", f"{P}L07.html Lab 1 hypothesis (line 125), interpretation (line 201), key-results row (line 347)", "PASS",
    "Every printed line (" + S + "twin_expected_r3.log) matches the statements: six True identities at 1e-9; coefficients 1.3325 0.8488 -0.4120 and residual norm 0.8951 (" + S + "independent_L07_r3.log recomputes 0.8951275 and the coefficients by QR and SVD); rank 2 of 3 (rank(dup^T dup)=2 recomputed); the generator constants 1.5, 0.8, -0.4, 0.3 and seed 7 equal the twin's lines 25-30. The 'finite example' sentence matches the code")
row("LABSTMT-L08", "2.5-labs", f"{P}L08.html line 146 (hypothesis) and line 158 (code docstring); tests/labs/M3/lab-M3-L08-1.py lines 11-12 (docstring) and line 96 (code)", "FAIL",
    "The hypothesis and docstring say each planted shape is matched 'to the component with the largest absolute cosine'. The code computes the argmax only over the first three components: twin line 96 is np.abs(v[:, :3].T @ shape). Nothing on the page or in the docstring restricts the search to PC1-PC3, so the claim is not what the lab checks. Numerically the claim also holds over all six components for this run (" + S + "independent_L08_r3.log: all-six argmax = PC1, PC2, PC3 with |cos| 0.9994, 0.9985, 0.9990), but the lab does not compute that",
    "Either extend the code to all six components (twin line 96: np.abs(v.T @ shape); the printed lines do not change) or restrict the wording to 'the first three components' in the hypothesis (page line 146), the docstring (twin lines 11-12 and page line 158). Then run tools/embed_labs.py course/modules/M/M3/L08.html --refresh lab-M3-L08-1 and re-run run_labs --page L08")
row("LABSTMT-L09", "2.5-labs", f"{P}L09.html Lab 1 hypothesis (line 193), interpretation (line 349), key-results rows (lines 499-500); twin lines 1-20 and 117-139", "PASS",
    "Counts 23/23/23 and index-0 distances 0.175527 and 0.163280 match " + S + "independent_L09_r3.log (own generator, 40 matrices, seed 20261028, 23 non-PSD, 23 of 23 correlation-feasible and strictly closer). Scope sentence ('R is not nearest in each instance where W passes ...') matches twin lines 125-128, where closer is counted inside the feasibility branch")
row("LABDOC-L09", "2.5-labs", "tests/labs/M3/lab-M3-L09-1.py lines 16-19 (docstring) and 125-128 (code)", "PASS",
    "Round-2 defect resolved: the closer counter is inside 'if is_correlation(alt)' (lines 125-128), and the docstring now says 'where W passes is_correlation and is strictly closer'. Verified by reading the twin and " + S + "independent_L09_r3.log ('closer without feasibility filter: 23' equals the feasible count, so no instance is lost or added)")
row("LABSTMT-L09-RUNTIME", "2.5-labs", "tests/labs/M3/lab-M3-L0{7,8,9}-1.py and page_smoke timings", "PASS",
    "imports are numpy (and numpy.typing) only; seeds 7, 8 and 20261028 fixed; no network; page_smoke lab timings in " + S + "page_smoke_L0*.log")

# ---- numbers ----
row("NUM-L07", "2.2-numbers", f"{P}L07.html E2 solution (line 299): A^T y approximately (18.38, 3.10, -17.60)", "FAIL",
    "The vector is not printed by Lab 1 (the page says so), it is not a registry quote, and no calculation on the page derives it. Recomputed value (" + S + "independent_L07_r3.log: A^T y = [18.37969697, 3.09586336, -17.60349772]) matches to two decimals, so the number is correct but unsourced under BUILDER_RULES 1.2. The other L07 numbers pass: M1 (1,1)/(1,-1); M2 coefficients 7/6, 1/2, fitted 7/6, 5/3, 13/6, residuals -1/6, 1/3, -1/6 (exact); M3 25 = 9 + 16; E1 0.8951 printed; E3 1.3325 printed",
    "Delete the vector from the E2 solution and derive the prediction from printed quantities: the lab prints beta = (1.3325, 0.8488, -0.4120) (non-zero), A^T y = G beta with G invertible (Theorem 1.2(a)), so A^T y is non-zero and the check prints False. Or add a print of A^T y to the twin, re-embed with tools/embed_labs.py, and cite that output")
row("NUM-L08", "2.2-numbers", f"{P}L08.html printed shares (line 284), cosines, E1 bound (line 377), E3 (line 391), key rows (433-434)", "PASS",
    "Recomputed by " + S + "independent_L08_r3.py (" + S + "independent_L08_r3.log): unrounded shares 0.75872815, 0.18088840, 0.05161927 round to 75.9, 18.1, 5.2; eigenvalues by eigh and by SVD agree to 3e-14; M11 13.681775 -> 13.6818, trace 88.202753 -> 88.2028; bound 100 M11/(trace+99 M11) = 0.948346 -> 0.9483 (below the rescaled share 0.979145 -> 0.9791, above 0.7587); printed sum 75.9+18.1+5.2 = 99.2 against unrounded 99.1236, difference 0.076 within the 0.15 bound of E3; doubled-panel shares equal (0.0)")
row("NUM-L09", "2.2-numbers", f"{P}L09.html witness (line 106), E1, E2 (line 447), interpretation (line 349), R entries", "PASS",
    "Recomputed by " + S + "independent_L09_r3.py: x^T C0 x = -2.4; C0 eigenvalues -0.8, 1.9, 1.9; ||C0-B||_F^2 = 0.64 = sum of squared negative eigenvalues; R = [[1,.5,.5],[.5,1,-.5],[.5,-.5,1]]; ||C0-R||_F = sqrt(0.96) = 0.9798; first non-PSD matrix distances 0.17552672 and 0.16328044 (printed 0.175527, 0.163280); 23 of 40 non-PSD; 40-23 = 17 PSD derived correctly")
row("NUM-L07-M", "2.2-numbers", f"{P}L07.html line 219 (residual norm 0.8951), E3 (1.3325)", "PASS",
    "printed by the lab; " + S + "independent_L07_r3.log: residual norm 0.8951275..., beta0 1.33251885")

# ---- mathematics ----
row("MATH-L07", "2.4-mathematics", f"{P}L07.html Definition 1.1, Theorems 1.2, 1.3, 2.2, Remark 1.4, lines 63-121", "PASS",
    "Every proof read line by line and re-derived: G symmetric with x^T G x = ||Ax||^2 > 0 gives invertibility via the spectral theorem (Lesson 4 Thm 2.3) and VV^T = I (Lesson 6 Fact 1.2, verified at L06.html line 64); existence and uniqueness of the projection; P symmetric and idempotent; closest-point strict inequality; Pythagorean identity with w = 0 (0 in W); Theorem 2.2(b) uniqueness step 'By the uniqueness in (a), beta = beta-hat' is valid because beta is a minimiser when A beta = p. " + S + "independent_L07_r3.log: P symmetric to 0.0, P^2-P 1.1e-16, residual orthogonal to 5e-15")
row("MATH-L08", "2.4-mathematics", f"{P}L08.html Proposition 1.1, Proposition 1.2, Theorem 1.4, Theorem 2.1(a)(b), Corollary 2.2, Proposition 2.3, Remark 2.4, lines 60-133", "PASS",
    "Every proof re-derived: M symmetric PSD; trace identity; Z^T Z = (T-1) Lambda; Rayleigh bounds with equality cases (a), and (b) by the coefficient identity u^T M u = sum_{i>=k} lambda_i alpha_i^2; Corollary 2.2; scaling by c^2 (c != 0); Remark 2.4 argument (M_jj > 0 from the 2 t M_jl + t^2 M_ll test; no kappa with M' = kappa M because c^2 != c). Definition 3.1 is not a proof and is handled in DEF-L08-CLOSE")
row("MATH-L09", "2.4-mathematics", f"{P}L09.html Lemma 1.3, Propositions 3.2(a)(b), 3.3(a)(b), 3.4, 3.5, Examples 2.3 and 3.6, lines 73-181", "PASS",
    "Every proof re-derived: Lemma 1.3 (trace-cyclicity step checked index by index); Prop 3.2 eigenvalues and quadratic form >= eps ||x||^2; Prop 3.3(a) squared distance formula including the lambda_i < eps branch; Prop 3.4 congruence argument; Prop 3.5 with delta = |b_ij|/(1+b_jj) and the bracket bound delta*b_jj < |b_ij| (strict since b_jj/(1+b_jj) < 1); Example 2.3 sum 3 + 2(-2.7) = -2.4; Example 3.6 eigenvalues 2.2, -0.2, A_0 = [[1.1,1.1],[1.1,1.1]], R = all ones, distances 0.04 and 0.08")

# ---- problems (every worked solution) ----
row("PROB-L07", "2.2-problems", f"{P}L07.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (lines 236-335)", "PASS",
    "All twelve worked solutions read and recomputed: M1 P=(1/2)[[1,1],[1,1]], p=(1,1); M2 fit 7/6 + x/2 (exact fractions); M3 P=diag(1,0), 25=9+16; P1-P3 proofs valid; E1 reading of the residual; E3 intercept as fitted value at zero regressors (correct); R1 uniqueness argument and existence via a maximal independent list with Lesson 1 Theorem 3.7 (cross-checked at L01.html line 161-170); R2 linearity; R3 Q^2 = Q and Qy orthogonal to W")
row("PROB-L08", "2.2-problems", f"{P}L08.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (lines 323-419)", "PASS",
    "All twelve solutions re-derived: M1 centred rows (-2,-3),(0,-1),(2,4), M = [[4,7],[7,13]], trace 17 = (13+1+20)/2, det 3, eigenvalues (17 +- sqrt277)/2; M2 shares 2/3, 1/6, 1/6; M3 18/27, 9/27; P1-P3 valid (P3 via Theorem 2.1(a) at e_1); E1 bound algebra; E2; E3 0.15 bound; R1 eigenspace characterisation; R2 column-shift invariance; R3 factor identity and rank argument")
row("PROB-L09", "2.2-problems", f"{P}L09.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (lines 386-481)", "PASS",
    "All twelve solutions re-derived: M1 eigenvalues 1.6, 0.4; M2 4.88 = 2.2^2 + 0.2^2; M3 characteristic polynomial lambda^2-13 lambda+32, discriminant 41, C entries 1, 1/3; P1 |C_ij| <= 1 by the t = +-1 test; P2 kernel argument; P3 convexity; E1 -2.4 term by term (-1.8 x 3 = -5.4); E2 sqrt(0.96); E3 0.25 -> 0.5; R1 split A = A_+ + A_-; R2 diag(1,4) -> identity; R3 norm identity")

# ---- grades, citations, cross-references ----
row("GRADE-L07", "2.3-grades", f"{P}L07.html grade spans and key-results table (lines 64, 84, 108, 347)", "PASS",
    "Theorems 1.2, 1.3, 2.2 and Remark 1.4 are graded T and proved on the page; the seeded-design row (line 347) is graded C and names 'Lab 1 output (finite numerical check ... not the proof)'")
row("GRADE-L08", "2.3-grades", f"{P}L08.html grade spans and key-results table (lines 79-93, 428-434)", "PASS",
    "Propositions 1.1, 1.2, 2.3, Theorems 1.4 and 2.1, Corollary 2.2 graded T with proofs; the simulated-panel rows (lines 433-434) are graded C and name Lab 1 output")
row("GRADE-L09", "2.3-grades", f"{P}L09.html grade spans and key-results table (lines 73-160, 491-500)", "PASS",
    "Lemma 1.3, Propositions 3.2 to 3.5 and Examples 2.3 and 3.6 graded T; the seeded 23-of-40 and distance rows (lines 499-500) are graded C and name Lab 1 output")
row("CITE-L07-L09", "2.1-citations", f"{P}L07.html, L08.html, L09.html (data-cite, data-locator, author names)", "PASS",
    "No data-cite or data-locator attribute and no author or source name in the three pages (" + S + "prose_scan_r3.log: attribution tokens [] for each page). L07 line 427 and L08 line 518 state that no outside source is used. L09 has an empty reference list and no statement; it attributes nothing (Method 2 is the lesson's own procedure), so this is recorded, not failed")
row("XREF-EARLIER", "2.4-mathematics", f"{P}L07.html, L08.html, L09.html cross-references", "PASS",
    "Each target read in its earlier lesson (" + S + "prose_scan_r3.log): L04 F1-F4 (lines 59-62) and Theorem 2.3 spectral theorem (line 130); L01 subspace test Prop 1.4 (line 80) and Theorem 3.7 (line 161, spanned list); L05 Theorem 2.1 eigenvalue test (line 108); L06 inner product (line 56), Fact 1.2 (line 64), sign freedom (lines 148, 212, 223); L03 eigendecomposition anchor (line 109); L07 Theorem 1.2 cited from L08 line 137 (read). Only the statements named were read, not every line of L01, L03, L04, L05 and L06")

# ---- notation ----
row("NOTATION-R", "2.4-notation", f"{P}L07.html, L08.html, L09.html", "PASS",
    "No \\mathbb in the three pages (" + S + "prose_scan_r3.log); \\R used 13, 6 and 0 times; notation/notation.json /macros/\\R is registered")
row("NOTATION-OPNAME", "2.4-notation", f"{P}L07.html, L08.html, L09.html", "PASS",
    "Round-2 defect resolved: raw \\operatorname{tr} and \\operatorname{diag} count 0 in all three pages (" + S + "prose_scan_r3.log); \\tr and \\diag used. The one remaining \\operatorname{span} (L08 line 402) has no registered macro and is not a registered symbol")
row("NOTATION-T", "2.4-notation", f"{P}L08.html section 1 (T x n matrix, T >= 2, T = 750)", "PASS",
    "notation.json symbol T means 'number of return observations (periods) in a sample'; in L08 T is the number of observations (rows) of the panel, the same meaning")
row("NOTATION-AST", "2.4-notation", f"{P}L09.html line 93 (C^{{\\ast}})", "PASS",
    "notation.json R^\\ast (AP1 SDF return) is a different symbol; L09 writes C^{\\ast} for a nearest correlation matrix; no collision")
row("NOTATION-Q", "2.4-notation", f"{P}L07.html, L09.html (orthogonal Q)", "PASS",
    "Plain Q (orthogonal matrix) is not the registered \\mathbb{Q} (AP1 probability measure); M3 pages contain no \\mathbb")
row("NOTATION-OTHER", "2.4-notation", "all control sequences in L07-L09 math", "PASS",
    "Control sequences are standard TeX or KaTeX (\\top, \\hat, \\lVert, \\lt, \\gt, \\varepsilon, \\tfrac) or registered (\\R, \\tr, \\diag). Plain gamma is used for coefficient vectors (L07, 17 uses) and is not a registered symbol; the registry note on \\emgamma reserves plain gamma for risk aversion, which M3 does not use. Recorded in notes, not failed")

# ---- definitions, DAG, prose ----
row("DEF-L08-CLOSE", "2.9-structure", f"{P}L08.html Definition 3.1 (line 141), quiz item L08q9 (line 507) and its explanation (line 511)", "FAIL",
    "Definition 3.1 defines the labels by '|cos(v, f_j)| is close to 1' with no threshold, so the defined term has no precise meaning. The quiz repeats 'close to 1' as the correct option. The sentence that a label is given only when a computation shows the cosine does not supply a threshold. Lab 1 gives values 0.9994, 0.9985, 0.9990 (" + S + "twin_expected_r3.log), so a threshold such as 0.99 would pass the present run",
    "State a threshold (for example |cos| >= 0.99) or define the label as the largest |cos| among the first three components, as the code does; change the quiz option and explanation to the same wording; then re-run check_pages --page L08")
row("DAG-LINKS", "2.9-structure", f"{P}L07.html line 38-39; L08.html line 38-39; L09.html line 38-39 and dfn ids", "PASS",
    "check_dag M3 PASS (" + S + "check_dag_M3.log); links point to earlier anchors: def-vector-space (L01), def-eigendecomposition (L03.html:109), def-spectral-theorem (L04.html:130), def-positive-semidefinite-matrix (L05.html:72); the new dfn ids are unique (def-orthogonal-projection, def-least-squares-projection, def-principal-component-analysis, def-level-slope-curvature, def-nearest-correlation-matrix, def-eigenvalue-clipping)")
row("DAG-M4", "2.9-structure", f"{P}L07.html, L08.html, L09.html (covariance, variance, correlation, Gaussian, standard deviation wording)", "PASS",
    "No link to an M4 concept (covariance, correlation, variance, expectation) on the three pages. 'correlation' appears as plain prose in L09 and 'Gaussian' and 'standard deviation' in the L09 twin docstring and lab; FINAL-ARCHITECT-RULINGS item 3 allows this. L08 uses the centred cross-product matrix without naming covariance (architect decision B1)")
row("DEFINE-BEFORE-USE", "2.9-structure", "first uses of tenor, trace, cosine, subspace, column space, PSD, positive definite, eigenvalue clipping, orthogonal matrix", "PASS",
    "tenor defined L08 line 56 before use; trace defined L08 line 58 and L09 line 56, before Prop 1.2 and M1; cosine defined L08 line 137 before Def 3.1; subspace, column space and orthogonal matrix in L07 line 56 and L06 line 56-68; PSD defined in L05 Def 1.4 and cited L09 line 56; positive definite L05 Def 1.4 before L09 Prop 3.2(b); eigenvalue clipping defined L09 line 116 before use")
row("PROSE-PROCESS", "2.9-structure", f"{P}L07.html, L08.html, L09.html learner text", "PASS",
    "prose_scan_r3.log: 0 hits for builder, verifier, architect, round, pin; 0 hits for TODO, TBD, lorem, for brevity, beyond the scope, details omitted, left as an exercise, it is important to note, well known, obviously, clearly")
row("PROSE-ELLIPSIS", "2.9-structure", "quiz stems ending in an ellipsis (L07 line 395, L08 quiz, L09 quiz)", "PASS",
    "Each ellipsis ends a multiple-choice prompt whose options follow ('the matrix A^T A is...'); it stands for the answer the options supply and omits no text. Judged not to be the banned omitted-content ellipsis")
row("PROSE-SCOPE", "2.2-scope", "scope words in L07-L09: every, all, always, any, only, exactly, for every", "PASS",
    "each checked against a proof or a finite check: 'every full-column-rank design' (L07 Thm 1.2 proof); 'for any A' (L07 canon, via Thm 1.3, any W); 'every nonzero c' and 'every data matrix' (L08 Prop 2.3); 'for all 23' (L09 lab output 23 of 23); 'always invertible' appears only as a wrong option (L07 quiz, misconception 3)")
row("STRUCT-WHY", "2.9-structure", f"{P}L07.html, L08.html, L09.html why-it-matters", "PASS",
    "check_pages M3 PASS, which enforces the 120-word limit (" + S + "check_pages_M3_unit.log)")
row("STRUCT-ORDER", "2.9-structure", f"{P}L07.html, L08.html, L09.html section order and counts", "PASS",
    "check_pages M3 PASS (section order and minimum counts). Read by hand: each page has why-it-matters, sections, lab with hypothesis, code, expected, interpretation, canon-breaks, three misconceptions, problem set in three tiers with worked solutions, key-results table, quiz of 9, 9 and 11 items, references")
row("HOURS", "2.9-structure", f"{P}L07.html (11), L08.html (12), L09.html (12); {P}index.html", "PASS",
    "data-hours 11, 12, 12 (" + S + "prose_scan_r3.log, equal to plan section 2.2). Lesson hours sum over L01-L09 = 12+11+12+12+12+11+11+12+12 = 105 = hub data-hours-lessons 105; project 45; total 150 = curriculum.json M3 hours 150")
row("DATA-CLAIM", "2.8-data", f"{P}L08.html canon-breaks (line 291)", "PASS",
    "'the program does not yet embed a multi-tenor series from which three or more tenors can be read' and 'a panel with two series has at most two principal components': " + S + "manifest_check_r3.log lists fx_daily (6 currencies), fx_monthly (10 currencies), ust_daily (tbill_3m, cmt_10y). No series with three tenors. Rank bound for two series is correct")
row("HONEST-GAP", "2.8-data", f"{P}L08.html canon-breaks (line 291) and lab heading", "PASS",
    "The page says the curriculum's Treasury lab is not run and a SIMULATED six-tenor panel is used; consistent with " + S + "manifest_check_r3.log (no data-files attribute on L07, L08 or L09)")
row("SIMULATED-LABELS", "2.8-data", f"{P}L07.html line 124-125; L08.html line 145-146; L09.html line 192-193 and lab docstrings", "PASS",
    "Each lab that generates data says SIMULATED in its hypothesis and docstring and in key-results rows; the L09 fixed matrix C0 is a hand example, not data")

# ---- notes ----
notes = (
    "Slice c (L07-L09 and lab twins), round 3, pin a007712f, base c737272f. Delta read: L07.html (two hunks: 'subspace (defined in Lesson 1)' and \\operatorname->\\diag), "
    "L08.html (tenor sentence reordered, \\tr and \\diag), L09.html (27 lines), tests/labs/M3/lab-M3-L09-1.py (19 lines: closer count nested in the feasibility branch and docstring). "
    "lab-M3-L07-1.py and lab-M3-L08-1.py are byte-identical to c737272. Cards.json and project/grader/labs project-1..3 are slice d and not checked here. "
    "No round-2 PASS row was carried: the three pages and the L09 twin changed, so each row was re-derived this round. "
    "Lab twins are demonstrations; no grader mutants apply (VERIFIER ruling), so mutants is empty. "
    "Round-2 non-PASS rows: LABDOC-L09 resolved (now PASS), NOTATION-OPNAME resolved (now PASS). New non-PASS rows in round 3: NUM-L07, LABSTMT-L08, DEF-L08-CLOSE."
)
registry_flags = []
freshness_flags = []
summary = None
fails = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "M3",
    "slice": "c",
    "round": 3,
    "verifier": "independent Haiku verifier, checkout verifyD3-M3-c",
    "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
    "base": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "checkout": str(ROOT),
    "scratch": "/private/tmp/verifyD3-twin-07, /private/tmp/verifyD3-twin-08, /private/tmp/verifyD3-twin-09 (empty directories used for the alone runs)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if not fails else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": registry_flags,
    "freshness_flags": freshness_flags,
    "notes": notes,
    "summary": (f"Slice c round 3: {len(rows)} rows, {len(rows)-len(fails)} PASS, {len(fails)} FAIL ({', '.join(fails)}), 0 UNVERIFIABLE. "
                "Gates all pass; the failures are one unsourced number in L07 E2, one label definition with an undefined threshold in L08, and one lab sentence whose search range is wider than the code."),
}
out = ROOT / "ledgers/M3/M3-c.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "fails", fails)
