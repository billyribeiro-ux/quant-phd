import json
C = "course/modules/M/M3/"
S = "ledgers/M3/scripts/M3-c-r9/"
rows = []
def r(id_, check, location, status, evidence):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

r("GATE-01", "check_pages.py --all (M3 subset)", "tools/check_pages.py", "PASS", S + "check_pages.log: 'check_pages M3: PASS', exit 0")
r("GATE-02", "check_dag.py --all", "tools/check_dag.py", "PASS", S + "check_dag.log: 'check_dag M3: PASS', exit 0")
r("GATE-03", "build_site.py --check", "tools/build_site.py", "PASS", S + "build_site.log: 'site data current: 6 outputs', exit 0")
r("GATE-04", "render_curriculum.py then git diff --exit-code CURRICULUM.md curriculum/curriculum.json", "tools/render_curriculum.py", "PASS", S + "render.log: 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h'; render_diff.log exit 0 (no diff)")
r("GATE-05", "run_labs.py --unit M3", "tools/run_labs.py", "PASS", S + "run_labs_M3.log: 'run_labs M3: PASS (12/12)', exit 0")
r("GATE-06", "page_smoke.py --unit M3 --pages L07.html L08.html L09.html", "tools/page_smoke.py", "PASS", S + "page_smoke.log: 'page_smoke M3: PASS', exit 0 (the --pages filter was passed; the tool's per-page scope was not separately confirmed)")
r("GATE-07", "ruff check . and ruff format --check .", "pyproject.toml", "PASS", S + "ruff.log: exit 0 for both, '362 files already formatted'")
r("GATE-08", "mypy --no-incremental (strict, repo config)", "pyproject.toml", "PASS", S + "mypy.log: 'Success: no issues found in 255 source files', exit 0")
r("GATE-09", "pytest tests -k M3 (tooling and lab tests selected by name)", "tests/", "PASS", S + "pytest_M3.log: exit 0; the -k selection is narrow, so this is not the full suite")
r("GATE-10", "verify_refs.py --offline", "tools/verify_refs.py", "PASS", S + "verify_refs.log: 'offline integrity: 560 entries, 0 problems', exit 0")
r("GATE-11", "fetch_data.py --check", "tools/fetch_data.py", "PASS", S + "fetch_data.log: '3 datasets, 0 problems', exit 0")
r("TWIN-01", "Twins run under python -I -W error with no stderr", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py", "PASS", "Each exits 0 under -I -W error (" + S + "twin-L0*.err empty); stdout compared with the page expected block by run_labs (GATE-05)")
r("TWIN-02", "Page lab code byte-identical to twin; expected block equals output", C + "L07.html, L08.html, L09.html", "PASS", "run_labs M3 checks code identity and output match (GATE-05); twin output for L07 re-run and read against L07.html lines 236-245 of the stripped text")
r("MATH-L07-01", "Theorem 1.2 (a)-(c) proofs and the Theorem 1.2 statement", C + "L07.html:81-104", "PASS", "Re-read L07.txt lines 26-36. (a) G symmetric, x^T G x = ||Ax||^2 > 0, G V Lambda^-1 V^T = I; (b) A^T(y-p)=0 and uniqueness via p'-p orthogonal to itself; (c) P symmetric, P^2=P. All re-derived by hand. Statement carries 'Assuming F1 to F4 of Lesson 4' (L07.html:81)")
r("MATH-L07-02", "Theorem 1.3, Remark 1.4, Theorem 2.2 (a)-(c) proofs", C + "L07.html:110-162", "PASS", "Re-derived: ||y-w||^2 = ||y-p||^2 + ||p-w||^2 for w in W; Pythagorean identity with w=0; normal equations equivalence. No gap found")
r("MATH-L07-03", "Problem solutions M1-M3, P1-P3, R1-R3 and E1-E3 mathematics", C + "L07.html:306-575", "PASS", "M2 by hand: A^T A=[[3,3],[3,5]], A^T y=(5,6), beta=(7/6,1/2), fitted 7/6,5/3,13/6, residuals -1/6,1/3,-1/6. M1, M3 checked. R1 existence cites Theorem 3.7 of Lesson 1 (L01 line 67 'Theorem 3.7 (a vector space that is spanned by a list has no longer independent list)'), which matches the use")
r("NUM-L07-01", "Lab 1 printed numbers: coefficients, residual norm, rank", C + "L07.html:242-245 and 464; cards M3-c125, c126, c177", "PASS", "Independent numpy run (scratch, this round): coefficients 1.3325, 0.8488, -0.4120; residual norm 0.8951; rank of A^T A with duplicated column 2 of 3; all match")
r("NUM-L07-02", "E2 prediction A^T y approx (18.38, 3.10, -17.60)", C + "L07.html:392", "PASS", "Independent recompute: A^T y = [18.38, 3.10, -17.60]")
r("NUM-L07-03", "E3 intercept interpretation and 'generator 1.5, 0.8, -0.4' statements", C + "L07.html:402, 118, 246", "PASS", "Generator coefficients 1.5, 0.8, -0.4 and noise sd 0.3 read from the lab source lines 200 and 199 of L07.txt; claims match")
r("MATH-L08-01", "Prop 1.1, Prop 1.2, Theorem 1.4, Theorem 2.1, Corollary 2.2, Prop 2.3 proofs", C + "L08.html:83-169", "PASS", "Re-derived each proof. Theorem 1.4: Z^T Z = (T-1)V^T M V = (T-1) Lambda. Theorem 2.1 (a),(b) via c = V^T u and the sum of nonnegative terms. Prop 2.3: M -> c^2 M. No gap found")
r("MATH-L08-02", "Problem solutions M1-M3, P1-P3, R1-R3, E1-E3", C + "L08.html:400-560", "PASS", "M1: M=[[4,7],[7,13]], trace 17, det 3, eigenvalues (17 +- sqrt(277))/2 (sum 17, product 3). M2 shares 2/3,1/6,1/6. M3 eigenvalues 18,9, shares 2/3,1/3. R1 tie gives eigenspace maximizers. R3 algebra verified. E1 bound algebra verified")
r("NUM-L08-01", "Lab 1 shares 75.9/18.1/5.2, rescale 0.7587->0.9791, M11 13.6818, trace 88.2028, bound 0.9483", C + "L08.html:327, 334-336, 476; cards M3-c141, c174", "PASS", "Independent SVD-based recompute (scratch, this round): shares 75.873, 18.089, 5.162 percent (print 75.9, 18.1, 5.2); rescaled first share 0.97914; M11 13.68177, trace 88.20275; bound 0.94835 (prints 0.9483)")
r("NUM-L08-02", "Planted-shape absolute cosines 0.9994, 0.9985, 0.9990 and PC matches", C + "L08.html:329-332, 189, 368; cards M3-c140", "PASS", "Independent SVD recompute: level 0.9994 (PC1), slope 0.9985 (PC2), curvature 0.9990 (PC3)")
r("NUM-L08-03", "E3 rounding bound: sum 99.2, at most 0.15 points from unrounded sum", C + "L08.html:492-496", "PASS", "Each rounded value within 0.05 of its share, so the sum of three is within 0.15; 75.9+18.1+5.2 = 99.2 arithmetic checked")
r("MATH-L09-01", "Lemma 1.3, Prop 3.2-3.5, Example 2.3, Example 3.6 proofs and numbers", C + "L09.html:94-245", "PASS", "Lemma 1.3 proof re-derived (trace cyclicity). Prop 3.5 quadratic-form argument re-derived: x^T B x = delta(-2|b_ij| + delta b_jj) < 0. Example 3.6: eigenvalues 2.2 and -0.2, A0 = 1.1 J, R = J, ||A-A0||_F^2 = 0.04, ||A-R||_F^2 = 0.08, ||A||_F^2 = 4.88 all re-derived")
r("NUM-L09-01", "Example 2.3 witness value and C0 eigenvalues", C + "L09.html:137-138; lab output lines 402-403", "PASS", "x^T C0 x = 3 - 5.4 = -2.4 by hand; eigenvalues -0.8, 1.9, 1.9 by symmetric eigensolver (eigh) with orthonormal eigenvectors")
r("NUM-L09-02", "R entries (0.5, 0.5, -0.5 off-diagonal) and squared distance 0.64 for C0", C + "L09.html:219, 408-410, 405; cards M3-c161", "PASS", "Recomputed with eigh: B = clip(C0) has ||C0-B||_F^2 = 0.64 and R with entries 0.5, 0.5, -0.5 (unit diagonal). Note: a first attempt used np.linalg.eig, which returns non-orthogonal eigenvectors for the repeated eigenvalue 1.9; that was a scratch-script error, not a course error")
r("NUM-L09-03", "E2 distance ||C0 - R||_F = sqrt(0.96) = 0.9798", C + "L09.html:561", "PASS", "C0 - R off-diagonal differences 0.4, 0.4, -0.4; 6 * 0.16 = 0.96; numeric sqrt 0.9797959, printed to four decimals 0.9798")
r("NUM-L09-04", "40-matrix experiment: 23 non-PSD, 23 of 23 feasible, 23 of 23 closer; first matrix distances 0.175527 and 0.163280", C + "L09.html:219, 411-414, 641-643; cards M3-c162, c163, c164, c175", "PASS", "Independent scratch loop with its own alternating-projection code (eigh clipping, diagonal set to one, 500 steps, tol 1e-12, feasibility to 1e-8): nonPSD 23, feasible 23, closer 23, first index 0 with distances 0.175527 (R) and 0.163280 (W), matching the lab")
r("NUM-L09-05", "Example 3.6 squared norms and distance statements", C + "L09.html:245, 639", "PASS", "||A - A0||_F^2 = 4 * 0.01 = 0.04 and formula (0 - (-0.2))^2 = 0.04; ||A - R||_F^2 = 2 * 0.04 = 0.08 match")
r("NUM-L09-06", "Problem and canon numbers: M2 4.88, M3 R entries, E1 2.4 term sum, E3 0.25 and 0.5, R2 diag(1,1)", C + "L09.html:242, 246-247, 551, 571, 597", "PASS", "All recomputed by hand: 1+1.44+1.44+1 = 4.88; c12 = 2/6 = 1/3; E1 terms -1.8 each sum -5.4; E3 (0 - (-0.5))^2 = 0.25; R2 C = diag(1,1)")
r("NOTATION-01", "Registered symbols (T, R^*, R^{e*}, R_f, Phi, gamma_3, gamma_4, Q) used with registered meaning or not at all", "notation/notation.json; " + C + "L07.html, L08.html, L09.html", "PASS", "T used in L08 only as the number of observations, which matches the registry meaning 'number of return observations (periods) in a sample'. No R^*, R^{e*}, R_f, Phi, gamma_3, gamma_4 or Q(probability) used in the slice")
r("NOTATION-02", "Local letters M, V, Lambda, Q, W, C, R, D, P, Z, B and tau/iota reuse", C + "L07.html, L08.html, L09.html", "PASS", "Letters are defined on the page where used (for example Q in L09 Lemma 1.3 and Definition 3.1, W in L07 for a subspace and in L09 for the alternating-projection output, which are local to each lesson). None collides with a registered program-wide symbol")
r("STRUCT-L07-01", "L07 structure: sections, grades legend, lab, problems, quiz, references", C + "L07.html", "PASS", "Structure present in L07.txt lines 9-241; grade legend lines 49-59; Lab 1 at line 168; problem set and quiz present")
r("STRUCT-L08-01", "L08 structure", C + "L08.html", "PASS", "Structure present in L08.txt lines 9-309; Lab 1 at line 195; quiz and problem set present")
r("STRUCT-L09-01", "L09 structure", C + "L09.html", "PASS", "Structure present in L09.txt lines 9-355; Lab 1 at line 263; quiz and problem set present")
r("DATA-L08-01", "Claim that the program does not embed a multi-tenor yield series with three or more tenors", C + "L08.html:347", "PASS", "course/assets/data/market/MANIFEST.json: ust_daily has columns tbill_3m and cmt_10y only; no series with three or more tenors. The claim is true")
r("SIM-LABEL-01", "Every lab panel and matrix is labelled SIMULATED and generated in code", C + "L07.html:170-184; L08.html:197-204; L09.html:265-284", "PASS", "Generators seeded (7, 8, 20261028) in the lab source; no data files are read; each lab and claim carries the SIMULATED label")
r("DAG-01", "Concepts used outside the prerequisite closure", "tools/check_dag.py; " + C + "L07.html:41-43, L08.html:41-43, L09.html:41-43", "PASS", "check_dag M3 PASS. Uses are Lessons 1, 3, 4, 5, 6 and 7 and are in the prerequisite closure of each lesson's 'Uses' line")
r("CROSSREF-01", "Cross-lesson citations resolve to the cited result", C + "L07.html:31, 69, 176; L08.html:58, 104; L09.html:69, 147", "PASS", "L04 Theorem 2.3 spectral theorem and F1-F4 (L04.txt lines 55-69); L06 Fact 1.2 (L06.txt line 81); L05 Theorem 2.1 eigenvalue test (L05.txt line 143); L01 Theorem 3.7 and 3.8 (L01.txt lines 67, 73); L07 Theorem 1.2 cited in L08 Definition 3.1 (see ASSUME-02)")
r("HOURS-01", "Lesson hours match hub split", C + "L07.html:36, L08.html:36, L09.html:36; " + C + "index.html:154-156", "PASS", "Page headers 11, 12, 12 study hours; hub lists L07 11 h, L08 12 h, L09 12 h. Arithmetic consistent")
r("PROSE-01", "Prose about what a lab prints or checks matches the code and output", C + "L07.html:170, 246, 255, 259; L08.html:197, 336; L09.html:265, 415", "PASS", "Each lab sentence checked against the lab source and output: check lists, tolerances (1e-9, 1e-8, 1e-12), 500-step cap, seeds, 40 and 750 sizes, and the printed shares. No mismatch found. Process words scan: none found in learner text")
r("GRADE-01", "Evidence grades match the basis of each claim", C + "L07.html:49-59, 462-464; L08.html:553-562; L09.html:641-643", "PASS", "T rows are proved on the page; C rows cite the lab or name the simulated run (for example M3-c124, c139, c141, c161, c163, c164, c175). No T row rests on a lab alone")
r("CARD-C161", "Card M3-c161 numbers and eigenvalues", "course/modules/M/M3/cards.json id M3-c161", "PASS", "0.6400000000 and eigenvalues -0.800000, 1.900000, 1.900000 match lab output (L09.html:402-405)")
r("CARD-HYP-01", "Cards carry the F1 to F4 hypothesis when the statement uses it", "course/modules/M/M3/cards.json ids M3-c117 to c123, c134 to c137, c144, c154 to c157, c168", "PASS", "Each of these cards begins 'Assuming F1 to F4 of Lesson 4' or 'Under F1 to F4', matching the statements of Theorem 1.2, 1.3, Remark 1.4, Theorem 2.2, Theorem 1.4, Theorem 2.1, Corollary 2.2, Proposition 2.3, Proposition 3.2, Proposition 3.3")
r("CARD-HYP-02", "Cards that depend on Definition 3.1 (L08) or the spectral decomposition in Definition 3.1 (L09) carry F1 to F4", "course/modules/M/M3/cards.json ids M3-c142 (L08 Definition 3.1 orthonormal shapes) and M3-c153 (L09 Definition 3.1 clipping)", "FAIL", "M3-c142 says the shapes are orthonormal by construction, which L08.html:184-189 derives via Lesson 7 Theorem 1.2 (now stated under F1 to F4). M3-c153 presupposes the spectral decomposition A = Q Lambda Q^T (L09.html:152), which needs the spectral theorem (F1 to F4). Neither card states the assumption. See ASSUME-02")
r("CARD-OK-01", "All 57 cards for L07, L08, L09 agree with the current lesson text", "course/modules/M/M3/cards.json", "PASS", "ledgers/M3/scripts/M3-c-r9/cards.txt (57 cards) read in full against the lesson text; theorem numbers and values verified")
r("CARD-DUP-01", "No duplicate cards in L07-L09", "course/modules/M/M3/cards.json", "PASS", "57 cards with distinct fronts; near-similar pairs (for example c137 and c144, c162 and c175) ask different facts")
r("CARD-C130", "Card M3-c130 states mean-zero of columns of X~, not of M", "course/modules/M/M3/cards.json id M3-c130", "PASS", "Round-8 fix applied (back now reads 'Every column of X~ has mean zero (Section 1)'), consistent with L08.html:69")
r("ASSUME-01", "Results using F1 to F4 say so in their statement (round-8 finding)", C + "L07.html:81, 111, 145; L08.html:99-106 (now 131), 155, 162; L09.html:161", "PASS", "Theorem 1.2, 1.3, 2.2 (L07), Theorem 2.1 (L08) and Remark 1.4 now carry 'Assuming F1 to F4 of Lesson 4'. Round-8 finding is fixed. Remaining undeclared uses are recorded in ASSUME-02")
r("ASSUME-02", "Definitions and presuppositions that use F1 to F4 must say so (same class as ASSUME-01)", C + "L08.html:184-189 (Definition 3.1, via Lesson 7 Theorem 1.2); " + C + "L09.html:50 and 152 (Definition 3.1 and the Section 3 introduction, spectral decomposition presupposed)", "FAIL", "L08 Definition 3.1 asserts that f_1, f_2, f_3 are orthonormal by construction, using the orthogonal projection of Lesson 7 Theorem 1.2, which is stated under F1 to F4. L09 Definition 3.1 and the Section 3 introduction presuppose the spectral decomposition A = Q Lambda Q^T, which exists only under F1 to F4 (Lesson 4, Theorem 2.3 at L04.html line 55). L08 Definition 1.3 was already fixed with the sentence 'Assuming F1 to F4 of Lesson 4, such a decomposition exists', so the same convention applies here. The problems R1 (L09) and R3 (L08) also start from a given decomposition and are only as strong as their definitions")

verdict = "FAIL" if any(x["status"] != "PASS" for x in rows) else "PASS"
frag = {
  "unit": "M3", "slice": "c", "round": 9,
  "verifier": "independent Haiku verifier, fresh checkout verifyB9-M3-c",
  "pin": "b6865c7d10020e31b9858a49edf751f4b814c031",
  "base": "ce7b3821c288da3dbba5dd4c90fb87dfd6d30089",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyB9-M3-c",
  "scratch": "/Users/billyribeiro/.fanout/wt/verifyB9-M3-c/ledgers/M3/scripts/M3-c-r9",
  "verified_at": "2026-10-28",
  "verdict": verdict,
  "slice_files": ["course/modules/M/M3/L07.html", "course/modules/M/M3/L08.html", "course/modules/M/M3/L09.html",
                  "tests/labs/M3/lab-M3-L07-1.py", "tests/labs/M3/lab-M3-L08-1.py", "tests/labs/M3/lab-M3-L09-1.py",
                  "course/modules/M/M3/cards.json (57 cards for L07, L08, L09)"],
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": ("Delta from ce7b382 to b6865c7 for this slice: L07 Theorems 1.2, 1.3, 2.2 and Remark 1.4 gained 'Assuming F1 to F4 of Lesson 4'; "
            "L08 Definition 1.3, Theorems 1.4, 2.1, Corollary 2.2, Proposition 2.3 gained the same, the L08 'can depend on units' wording changed, and the L09 Proposition 3.2 gained it; "
            "cards changed: M3-c014 is outside the slice (L01), M3-c117 to c123, c130, c134 to c137, c138 unchanged, c141, c144, c151, c154 to c157, c167, c168 changed. "
            "Every row was re-verified from scratch on this pin; no PASS row is carried forward. "
            "Mutation testing and alternative implementations were not run: the slice has no project grader, and lab twins are demonstrations per the ruling. "
            "Not run: run_graders, mutate_graders, check_projects, the full pytest suite, the live verify_refs, and the page_smoke per-page light/dark/360px detail beyond its PASS line. "
            "Possible minor point not written as a row: L07.html:255 says the lesson 'makes no claim' about fitted-vector uniqueness without independent columns, while R1 (L07.html:176) proves uniqueness of the orthogonal projection in any subspace. The sentence is literally true, so no row was raised."),
  "summary": ("Slice M3-c, round 9, pin b6865c7. Gates re-run and PASS (check_pages, check_dag, build_site, render diff, run_labs 12/12, page_smoke, ruff, mypy, verify_refs, fetch_data, pytest -k M3). "
              "All numbers re-derived with independent scripts (regression, PCA shares/SVD, cosines, C0 clipping and rescaling, 40-matrix experiment). "
              "Round-8 findings CARD-C130 and ASSUME-01 are fixed. One new defect class: ASSUME-02 (and CARD-HYP-02) where a definition or card presupposes F1 to F4 without saying so. Verdict FAIL."),
}
json.dump(frag, open(S.replace("scripts/M3-c-r9/", "") + "M3-c.json", "w"), indent=1, ensure_ascii=False)
print(verdict, len(rows), sum(1 for x in rows if x["status"]=="PASS"))
