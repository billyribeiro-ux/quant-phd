import json, subprocess
S = "ledgers/M3/scripts/M3-c-r10/"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

GATE = "ledgers/M3/scripts/M3-c-r10/"
row("GATE-01", "check_pages.py --all", "tools/check_pages.py", "PASS", GATE + "check_pages.log: 'check_pages M3: PASS', exit 0 (run this round)")
row("GATE-02", "check_dag.py --all", "tools/check_dag.py", "PASS", GATE + "check_dag.log: 'check_dag M3: PASS', exit 0")
row("GATE-03", "build_site.py --check", "tools/build_site.py", "PASS", GATE + "build_site.log: 'site data current: 6 outputs', exit 0")
row("GATE-04", "render_curriculum.py then git diff --exit-code CURRICULUM.md curriculum/curriculum.json", "tools/render_curriculum.py", "PASS", GATE + "render.log: 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h'; render_diff.log exit 0")
row("GATE-05", "run_labs.py --unit M3 --page L07 / L08 / L09", "tools/run_labs.py", "PASS", GATE + "run_labs_L07.log, run_labs_L08.log, run_labs_L09.log: each 'run_labs M3: PASS (1/1)', exit 0")
row("GATE-06", "page_smoke.py --unit M3 --pages L07.html L08.html L09.html", "tools/page_smoke.py", "PASS", GATE + "page_smoke.log: 'page_smoke M3: PASS', exit 0")
row("GATE-07", "ruff check . and ruff format --check .", "pyproject.toml", "PASS", GATE + "ruff.log: check exit 0; '362 files already formatted', exit 0")
row("GATE-08", "mypy --no-incremental (strict)", "pyproject.toml", "PASS", GATE + "mypy.log: 'Success: no issues found in 255 source files', exit 0")
row("GATE-09", "pytest -q -k M3", "tests/", "PASS", GATE + "pytest_M3.log: 12 tests, exit 0 (narrow -k selection, not the full suite)")
row("GATE-10", "verify_refs.py --offline", "tools/verify_refs.py", "PASS", GATE + "verify_refs.log: 'offline integrity: 560 entries, 0 problems', exit 0")
row("GATE-11", "fetch_data.py --check", "tools/fetch_data.py", "PASS", GATE + "fetch_data.log: '3 datasets, 0 problems', exit 0")
row("TWIN-01", "Twins run under python -I -W error with empty stderr", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py", "PASS", GATE + "twin-L07.err, twin-L08.err, twin-L09.err: exit 0, stderr empty; outputs in twin-L0*.out (10, 14, 13 lines)")
row("TWIN-02", "Page lab code identical to twin; expected block equals twin output", "course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", "Extracted data-run code and expected blocks with a script: page code equals twin modulo the single trailing newline; expected block equals twin stdout line for line for all three labs (10, 14, 13 lines)")
row("MATH-L07-01", "Theorem 1.2 (a)-(c) statement and proofs", "course/modules/M/M3/L07.html:81-104", "PASS", "Re-derived: G V Lambda^-1 V^T = V V^T = I (uses L06 Fact 1.2 under F1); uniqueness via p'-p orthogonal to itself; P^T=P, P^2=P. Statement carries 'Assuming F1 to F4 of Lesson 4'")
row("MATH-L07-02", "Theorem 1.3, Remark 1.4, Theorem 2.2 (a)-(c) proofs", "course/modules/M/M3/L07.html:110-162", "PASS", "Re-derived the expansion ||y-w||^2 = ||y-p||^2 + ||p-w||^2 and the normal-equation equivalence; every statement carries the F1 to F4 marker")
row("MATH-L07-03", "Problem solutions M1-M3, P1-P3, R1-R3, E1-E3 mathematics", "course/modules/M/M3/L07.html (problem set, section 5)", "PASS", "By hand: M1 P=(1/2)[[1,1],[1,1]], p=(1,1), residual (1,-1); M2 A^TA=[[3,3],[3,5]], A^Ty=(5,6), beta=(7/6,1/2), fitted 7/6,5/3,13/6, residuals -1/6,1/3,-1/6; M3 p=(3,0); R1 existence via L01 Theorem 3.7 (checked at L01.html:161); R2 linearity; R3 Q^2=Q. No gap found")
row("NUM-L07-01", "Lab 1 printed numbers: coefficients, residual norm, rank", "course/modules/M/M3/L07.html expected block and interpretation; cards M3-c125, c126, c177", "PASS", GATE + "indep.py (numpy lstsq and QR, -I -W error): beta = 1.332519, 0.848811, -0.411964; residual norm 0.8951276; rank(A^TA with duplicated column) = 2")
row("NUM-L07-02", "E2 prediction A^T y", "course/modules/M/M3/L07.html E2 solution", "PASS", GATE + "indep.py: A^T y = (18.379697, 3.095863, -17.603498), i.e. (18.38, 3.10, -17.60) to two decimals as printed")
row("NUM-L07-03", "E3 intercept interpretation and 'generator 1.5, 0.8, -0.4' statements", "course/modules/M/M3/L07.html E3 solution, Lab 1 interpretation", "PASS", "Generator y = 1.5 + 0.8 x1 - 0.4 x2 + noise(sd 0.3) at indep.py; first column of A is ones so the fitted value at zero regressors is beta_0")
row("MATH-L08-01", "Propositions 1.1, 1.2, Theorem 1.4, Theorem 2.1, Corollary 2.2, Proposition 2.3 proofs", "course/modules/M/M3/L08.html (sections 1 and 2)", "PASS", "Re-derived: Z^TZ=(T-1)V^TMV=(T-1)Lambda; Theorem 2.1 equality case via c_i=0 for lambda_i<lambda_1; Corollary 2.2 identity; Prop 2.3 eigenvalues scale by c^2 with order kept. Remark 2.4 is handled in REMARK-L08-01, not here")
row("MATH-L08-02", "Problem solutions M1-M3, P1-P3, R1-R3, E1-E3", "course/modules/M/M3/L08.html (problem set, section 6)", "PASS", "M1 by hand: X~ rows (-2,-3),(0,-1),(2,4); M=[[4,7],[7,13]]; trace 17; det 3; eigenvalues (17 +- sqrt 277)/2. M2 shares 2/3,1/6,1/6. M3 eigenvalues 18,9. E1 bound 100*M11/(S0+99*M11) = 0.94835 (independent). E3 rounding bound 0.15 correct. R3 identity re-derived. No gap found")
row("NUM-L08-01", "Lab 1 shares, rescale 0.7587->0.9791, M11, trace, E1 bound", "course/modules/M/M3/L08.html expected block and interpretation; cards M3-c141, c174", "PASS", GATE + "indep.py (svd and eigh agree to 3e-14): shares 75.8728, 18.0888, 5.1619 percent -> 75.9, 18.1, 5.2; M11 13.681775, trace 88.202753, bound 0.948346 (printed 0.9483, inputs 13.6818 and 88.2028); rescaled first share 0.979145 -> 0.9791")
row("NUM-L08-02", "Planted-shape absolute cosines and component matches", "course/modules/M/M3/L08.html expected block and interpretation; cards M3-c140", "PASS", GATE + "indep.py: level->PC1 0.999381 (printed 0.9994), slope->PC2 0.998544 (0.9985), curvature->PC3 0.999019 (0.9990); three distinct components")
row("NUM-L08-03", "E3 rounding bound", "course/modules/M/M3/L08.html E3 solution", "PASS", "99.2 is the sum of 75.9+18.1+5.2; each rounding error is at most 0.05 points, so the sum is within 0.15 of the unrounded sum; arithmetic verified")
row("MATH-L09-01", "Lemma 1.3, Propositions 3.2 to 3.5, Example 2.3, Example 3.6 proofs and numbers", "course/modules/M/M3/L09.html (sections 1 to 4)", "PASS", "Re-derived: Lemma 1.3 trace argument; Prop 3.2(b) bound; Prop 3.3(a) diagonal Frobenius norm; Prop 3.4 congruence; Prop 3.5 delta = |b_ij|/(1+b_jj) gives x^TBx < 0; Example 3.6 eigenvalues 2.2 and -0.2, A_0 = [[1.1,1.1],[1.1,1.1]], ||A-A_0||^2 = 0.04, ||A-R||^2 = 0.08. Example 2.3 value -2.4 re-computed")
row("NUM-L09-01", "Example 2.3 witness value and C0 eigenvalues", "course/modules/M/M3/L09.html lab expected block and E1", "PASS", GATE + "indep_l09.py: C0 eigenvalues -0.8, 1.9, 1.9; x^TC0x = -2.4 (E1 terms 3 and -5.4 re-added)")
row("NUM-L09-02", "R entries and ||C0-B||_F^2 = sum of squared negative eigenvalues", "course/modules/M/M3/L09.html lab expected block and interpretation; card M3-c161", "PASS", GATE + "indep_l09.py: R = [[1,.5,.5],[.5,1,-.5],[.5,-.5,1]]; ||C0-B||^2 = 0.6400 and sum of squared negative eigenvalues = 0.6400")
row("NUM-L09-03", "E2 distance ||C0 - R||_F", "course/modules/M/M3/L09.html E2 solution; quiz q9", "PASS", "Off-diagonal differences 0.4, 0.4, -0.4; six entries; squared norm 0.96; sqrt = 0.979796 -> 0.9798 (hand and python)")
row("NUM-L09-04", "40-matrix experiment counts and first-instance distances", "course/modules/M/M3/L09.html lab expected block, interpretation, key results; cards M3-c162, c163, c164, c175", "PASS", GATE + "indep_l09.py (own clip via eigh, own rescale, own alternating projection, seed 20261028): 23 non-PSD (cutoff -1e-9), 23 feasible to 1e-8, 23 strictly closer, first instance ||A-R|| 0.175527 and ||A-W|| 0.163280. Eigenvalue margin check: no minimum eigenvalue lies within 1e-6 of zero, so the -1e-9 cutoff is not borderline; 17 PSD matrices")
row("NUM-L09-05", "Example 3.6 squared norms and distances", "course/modules/M/M3/L09.html Example 3.6 and key results", "PASS", "Hand-verified: A - A_0 = [[-0.1,0.1],[0.1,-0.1]] gives 0.04; A - R off-diagonal 0.2 gives 0.08; formula (0-(-0.2))^2 = 0.04")
row("NUM-L09-06", "Problem numbers: M2 4.88, M3 rescaling, E1 term sum, E3 0.25 and 0.5", "course/modules/M/M3/L09.html problem set", "PASS", "M2 squared entries 1+1.44+1.44+1 = 4.88 and 2.2^2+0.2^2 = 4.88; M3 eigenvalues (13 +- sqrt 41)/2 and C = [[1,1/3],[1/3,1]]; E1 3 - 5.4 = -2.4; E3 2^0.5 spectrum gives 0.25 and 0.5")
row("NOTATION-01", "Registered symbols and macros used with registered meaning", "notation/notation.json; course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", "notation.json: T = number of observations (L08 uses T as row count, consistent); \\tr and \\diag are registered macros (L09 uses them); R^*, R^{e*}, R_f, Phi, gamma_3, gamma_4 do not occur in the slice; the registered \\mathbb{Q} (measure) does not occur, plain Q is the orthogonal matrix. \\mathbb{R} is the expansion of the registered \\R. No registered symbol is given another meaning")
row("NOTATION-02", "Local letters reused across lessons", "course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", "W is a subspace in L07 and an output matrix in L09; Q, V, C, R, D, P, Z, B, M are local and defined in each lesson; notation.json states that these letters are lesson-local")
row("STRUCT-L07-01", "L07 structure: sections, grade legend, lab, canon breaks, misconceptions, problems, key results, quiz, references", "course/modules/M/M3/L07.html", "PASS", "Structure present in the file (checked by reading); check_pages M3 PASS")
row("STRUCT-L08-01", "L08 structure", "course/modules/M/M3/L08.html", "PASS", "Structure present; quiz has 9 items; check_pages M3 PASS")
row("STRUCT-L09-01", "L09 structure", "course/modules/M/M3/L09.html", "PASS", "Structure present; quiz has 11 items; check_pages M3 PASS")
row("DATA-L08-01", "Claim that the program does not embed a multi-tenor series with three or more tenors", "course/modules/M/M3/L08.html canon-breaks bullet 2", "PASS", "course/assets/data/market/MANIFEST.json lists fx_daily, fx_monthly and ust_daily (columns tbill_3m, cmt_10y): the only rate series with two columns, so no series with three or more tenors is embedded. Claim true")
row("SIM-LABEL-01", "Every lab panel and matrix is labelled SIMULATED and generated in code", "tests/labs/M3/lab-M3-L07-1.py, L08-1.py, L09-1.py; page prose", "PASS", "Each twin docstring says SIMULATED with a seed (7, 8, 20261028); no data file is read")
row("DAG-01", "Concepts used outside the prerequisite closure", "tools/check_dag.py; L07-L09 meta-row links", "PASS", GATE + "check_dag.log: 'check_dag M3: PASS'; uses are eigendecomposition (L03), spectral theorem (L04), PSD (L05), vector space (L01), Frobenius norm (L06)")
row("CROSSREF-01", "Cross-lesson citations resolve to the cited result", "L07 (L01 Thm 3.7, L06 Fact 1.2, L04 Thm 2.3), L08 (L07 Thm 1.2, L04 Thm 2.3, L06 sign freedom), L09 (L04 Thm 2.3, L05 PSD, L03)", "PASS", "L01.html:161 'Theorem 3.7 (a vector space that is spanned by a list has no longer independent list)'; L06.html:64 'Fact 1.2 (orthonormal columns of a square matrix)'; L04.html:130 'Theorem 2.3 (the spectral theorem)'; L05.html:108 'Theorem 2.1 (eigenvalue test)'; L06.html:229 sign freedom")
row("HOURS-01", "Lesson hours match hub split", "course/modules/M/M3/L07.html, L08.html, L09.html headers; course/modules/M/M3/index.html:154-156", "PASS", "Headers: L07 11 h, L08 12 h, L09 12 h; hub cards read L07 11 h, L08 12 h, L09 12 h. Hub split is 105 lesson hours; no arithmetic inconsistency found")
row("PROSE-01", "Prose about what a lab prints or checks matches the code and output", "course/modules/M/M3/L07.html lab and canon/E2; L08.html lab, E1, E3; L09.html lab and interpretation", "PASS", "Each sentence on what the lab checks, prints or counts was compared with the twin code and the printed output (see NUM rows). E2 of L07 'False exactly when some entry of A^Ty has absolute value at least 1e-9' matches the tolerance test; L09 'the lab says nothing about the 17 PSD matrices' is consistent with 40-23")
row("GRADE-01", "Evidence grades match the basis of each claim", "course/modules/M/M3/L07.html key results; L08.html key results; L09.html key results", "PASS", "Theorem-based rows are T and cite theorems; lab-output rows are C and name the lab and say SIMULATED")
row("ASSUME-01", "Results using F1 to F4 say so in their statement", "course/modules/M/M3/L07.html Thm 1.2, 1.3, Rem 1.4, Thm 2.2, key results; L08.html Def 1.3, Thm 1.4, Thm 2.1, Cor 2.2, Prop 2.3, Def 3.1, P3, R1; L09.html Sec 3 intro, Def 3.1, Prop 3.2, 3.3, Method 1, Method 2, P2, R1", "PASS", "Grep and reading: every statement that uses the spectral theorem carries 'Assuming F1 to F4 of Lesson 4' or 'Assuming F1'. Prop 3.4 and Prop 3.5 do not use the spectral decomposition and need no marker")
row("ASSUME-02", "Definitions and presuppositions that use F1 to F4 must say so (round-9 FAIL)", "course/modules/M/M3/L08.html:141 (Def 3.1), L09.html:112 (Sec 3 intro), L09.html:138 (Prop 3.3), L09.html:185 (Method 1, 2)", "PASS", "Round-9 defect fixed at e8b10b8: L08 Def 3.1 now begins 'Assuming F1 to F4 of Lesson 4'; L09 Sec 3 intro now says 'Assuming F1 to F4 ... such a decomposition exists'; L09 Def 3.1 and Prop 3.3 carry the marker; L08 Def 1.3 carries it. Verified by reading the diff b6865c7..e8b10b8")
row("CARD-HYP-01", "Cards carry the F1 to F4 hypothesis when the statement uses it", "course/modules/M/M3/cards.json (M3-c117 to c123, c134 to c137, c144, c154 to c157, c168)", "PASS", "Read each card: c117-c123, c133-c137, c142, c153-c157, c166, c168 begin with 'Assuming F1 to F4 of Lesson 4' or state the independence hypothesis")
row("CARD-HYP-02", "Cards that depend on Definition 3.1 (L08) or the spectral decomposition in Definition 3.1 (L09) carry the hypothesis (round-9 FAIL)", "course/modules/M/M3/cards.json ids M3-c142 and M3-c153", "PASS", "Round-9 defect fixed: M3-c142 back is 'Assuming F1 to F4 of Lesson 4, three shapes ...'; M3-c153 back is 'Assuming F1 to F4 of Lesson 4, with A = Q Lambda Q^T a spectral decomposition ...'")
row("CARD-C161", "Card M3-c161 numbers and eigenvalues", "course/modules/M/M3/cards.json id M3-c161", "PASS", "0.6400000000 and -0.800000, 1.900000, 1.900000 appear in the L09 expected block; independent recomputation agrees")
row("CARD-C130", "Card M3-c130 states mean-zero of columns of X~, not of M", "course/modules/M/M3/cards.json id M3-c130", "PASS", "Back: 'Every column of X~ has mean zero (Section 1).' Matches L08.html Section 1 and P1")
row("CARD-C138", "Card M3-c138 answers 'No' for every multiplier c", "course/modules/M/M3/cards.json id M3-c138", "FAIL", "Front: 'Does multiplying one column of the data by c change M by a multiple of M?' Back: 'No.' For c = 1 the data and M do not change, and M = 1 * M is a multiple of M. The 'No' holds only for c not in {0, 1} and a column with nonzero entries in its row (derivation: M'_jl = c M_jl and M'_jj = c^2 M_jj force k = c and c^2 = c)", "Change the back to: 'Not for c not in {0, 1} when that column has nonzero entries: the diagonal entry is multiplied by c^2 and the off-diagonal entries in its row and column by c, so no single factor k gives M' = kM and the shares can change (Remark 2.4). For c = 1 nothing changes.'")
row("CARD-OK-01", "All 58 cards for L07, L08, L09 agree with the current lesson text", "course/modules/M/M3/cards.json (17 L07, 17 L08, 24 L09)", "FAIL", "Every card was read against its lesson text. All agree except M3-c138 (see CARD-C138), which repeats the over-general Remark 2.4 claim", "Fix M3-c138 as in CARD-C138; then re-run this check")
row("CARD-DUP-01", "No duplicate ids or duplicate cards in L07-L09", "course/modules/M/M3/cards.json", "PASS", "No duplicate ids (python check); overlapping questions M3-c137/c144 and c162/c163/c175 ask different things (shares under scaling, counts)")
row("CLAIM-L07-01", "L07 canon-breaks sentence 'this lesson makes no claim' about uniqueness of the fitted vector without independent columns", "course/modules/M/M3/L07.html canon-breaks bullet 1 (the sentence ending 'and this lesson makes no claim of it'); compare Research R1 (same file)", "FAIL", "R1 proves that an orthogonal projection of y onto any subspace W is unique ('The argument uses only the subspace property and the definition, so it proves uniqueness in any subspace'). Definition 2.1 identifies the least-squares projection with the fitted vector, which is that projection (Theorem 1.3 argument). So the lesson does make the claim that the fitted vector is unique without independent columns, and the canon sentence is false as written", "Replace the sentence with: 'The lab does not check that the fitted vector is unique without independent columns; Research R1 proves that an orthogonal projection onto any subspace is unique, so the fitted vector is unique there too, while the coefficients are not (Lab 1).'")
row("REMARK-L08-01", "L08 Remark 2.4: 'Multiplying one column of X by a number c changes M in a way that is not a multiple of M'", "course/modules/M/M3/L08.html Remark 2.4 (section 2)", "FAIL", "For c = 1 the matrix is unchanged, and M = 1 * M is a multiple of M, so the sentence is false for c = 1. The sentence is a general claim over 'a number c' with no hypothesis (rule 4 scope word). The correct content holds for c not in {0, 1} when the column's row has a nonzero off-diagonal entry, by the entry comparison M'_jl = c M_jl, M'_jj = c^2 M_jj", "Add the hypothesis: 'Multiplying one column of X by a number c other than 0 or 1 changes M in a way that is not a multiple of M, when that column has nonzero off-diagonal entries (the diagonal entry scales by c^2 and the off-diagonal entries by c). For c = 1 nothing changes.'")
row("PROSE-02", "Scope words and 'every'/'any' claims in slice prose", "course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", "Spot-checked 'every', 'any', 'always', 'exactly', 'only' claims: L07 'exactly one orthogonal projection', L08 'every real symmetric matrix', L09 'any choice' of spectral decomposition, 'every correlation matrix' in Def 2.1: each is backed by a proof or an explicit hypothesis. The rescaling claim in REMARK-L08-01 is the one that failed")
row("PROCESS-01", "No process words in learner text", "course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", "grep for builder, verifier, round, draft, todo, placeholder, fixed, correction, agent, reviewer, audit: only substring matches inside 'appending' and 'lay' (L07.html:316); no process words")

frag = {
    "unit": "M3",
    "slice": "c",
    "round": 10,
    "verifier": "independent Haiku verifier, fresh checkout verifyB10-M3-c",
    "pin": "e8b10b8110923bd88c3b4bd0e36e1571be3e6725",
    "base": "b6865c7d10020e31b9858a49edf751f4b814c031",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB10-M3-c",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyB10-M3-c/ledgers/M3/scripts/M3-c-r10",
    "verified_at": "2026-10-29",
    "verdict": "FAIL",
    "slice_files": [
        "course/modules/M/M3/L07.html",
        "course/modules/M/M3/L08.html",
        "course/modules/M/M3/L09.html",
        "tests/labs/M3/lab-M3-L07-1.py",
        "tests/labs/M3/lab-M3-L08-1.py",
        "tests/labs/M3/lab-M3-L09-1.py",
        "course/modules/M/M3/cards.json (58 cards for L07, L08, L09)",
    ],
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta from b6865c7 to e8b10b8 for this slice: L07 key-results rows and Theorem statements, L08 Def 3.1, P3, R1 and key results, "
        "L09 Section 3 intro, Def 3.1, Props 3.2-3.4, canon and misconception text, P2, R1, key results; cards M3-c138 unchanged in text but "
        "re-read against Remark 2.4; M3-c142, c153 now carry the hypothesis; M3-c181 added. Every row was re-verified on this pin from scratch "
        "(no PASS row carried forward). Two new defects: CLAIM-L07-01 (canon sentence contradicts R1) and REMARK-L08-01 / CARD-C138 (c = 1 "
        "counterexample). Mutation testing not applicable: the slice has no project grader; lab twins are demonstrations per the ruling. "
        "Not run: run_graders, mutate_graders, check_projects was run (PASS) but its per-unit output was only checked for M3 lines, full pytest suite, "
        "live verify_refs, the rendered-page visual check in a browser."
    ),
    "summary": (
        "Slice M3-c, round 10, pin e8b10b8. All gates re-run and PASS (check_pages, check_dag, check_projects, build_site, render diff, "
        "run_labs per page, page_smoke, ruff, mypy, pytest -k M3, verify_refs, fetch_data). Twins pass -I -W error with empty stderr and "
        "match the page code and expected blocks. All numbers re-derived by independent scripts. Round-9 FAILs CARD-HYP-02 and ASSUME-02 are fixed. "
        "New FAILs: CLAIM-L07-01 (L07 canon sentence says the lesson makes no claim about fitted-vector uniqueness; R1 proves it), "
        "REMARK-L08-01 and CARD-C138 (the 'not a multiple of M' claim fails at c = 1), with CARD-OK-01 failing on the card. Verdict FAIL."
    ),
}
json.dump(frag, open("ledgers/M3/M3-c.json", "w"), indent=2, ensure_ascii=False)
print("rows", len(rows), "non-PASS", [r["id"] for r in rows if r["status"] != "PASS"])
