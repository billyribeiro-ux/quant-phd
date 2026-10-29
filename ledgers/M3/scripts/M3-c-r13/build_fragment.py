import json
G = "ledgers/M3/scripts/M3-c-r13/"
P = "course/modules/M/M3/"
rows = []
def r(id_, check, location, status, evidence, fix=None):
    row = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

GATE_LOG = G + "gates.log"
r("GATE-01", "tools/check_pages.py", "tools/check_pages.py", "PASS",
  "check_pages.py --unit M3 -> 'check_pages M3: PASS' (" + GATE_LOG + "); --all last line 'check_pages AP1: PASS'.")
r("GATE-02", "tools/check_dag.py", "tools/check_dag.py", "PASS",
  "check_dag.py --unit M3 -> 'check_dag M3: PASS' (" + GATE_LOG + ").")
r("GATE-03", "tools/build_site.py --check", "tools/build_site.py", "PASS",
  "build_site.py --check -> 'site data current: 6 outputs' (" + GATE_LOG + ").")
r("GATE-04", "render_curriculum.py then git diff --exit-code CURRICULUM.md curriculum/curriculum.json", "tools/render_curriculum.py", "PASS",
  "render_curriculum.py run; git diff --exit-code returned rc=0 (" + GATE_LOG + ").")
r("GATE-05", "run_labs.py --unit M3 --page L07/L08/L09", "tools/run_labs.py", "PASS",
  "'run_labs M3: PASS (1/1)' printed for each of L07, L08, L09 (" + GATE_LOG + ").")
r("GATE-06", "page_smoke.py --unit M3 --pages L07.html L08.html L09.html", "tools/page_smoke.py", "PASS",
  "'page_smoke M3: PASS' for the three pages together and each page alone (" + GATE_LOG + ").")
r("GATE-07", "ruff check . and ruff format --check .", "pyproject.toml", "PASS",
  "'All checks passed!' and '362 files already formatted' (" + GATE_LOG + ").")
r("GATE-08", "mypy --no-incremental (strict)", "pyproject.toml", "PASS",
  "'Success: no issues found in 255 source files' (" + GATE_LOG + ").")
r("GATE-09", "pytest -q -k M3 (narrow selection, not the full suite)", "tests/", "PASS",
  "12 dots, [100%], no failures (" + GATE_LOG + "). Full suite not run (targeted rule).")
r("GATE-10", "verify_refs.py --offline", "tools/verify_refs.py", "PASS",
  "'offline integrity: 560 entries, 0 problems' (" + GATE_LOG + ").")
r("GATE-11", "fetch_data.py --check", "tools/fetch_data.py", "PASS",
  "'fetch_data: 3 datasets, 0 problems' (" + GATE_LOG + ").")

TW = "tests/labs/M3/lab-M3-L0{n}-1.py"
r("TWIN-01", "Twins run under python -I -W error with empty stderr", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py", "PASS",
  "python -I -W error on each twin: rc=0, stderr 0 bytes (" + G + "twin-L07.err, twin-L08.err, twin-L09.err); outputs saved as twin-L0n.out.")
r("TWIN-02", "Page code equals twin; expected block equals twin output", P + "L07.html, L08.html, L09.html", "PASS",
  "Python extraction of the data-run block and the class=expected block: code==twin True for 07, 08, 09 (trailing newline only differs in length); expected==output True for 07, 08, 09.")

r("MATH-L07-01", "Theorem 1.2 (a)-(c), Theorem 1.3, Remark 1.4 statements and proofs", P + "L07.html:63-96", "PASS",
  "Read L07.html:63-96. Checked (a) G=A^TA symmetric, x^TGx=||Ax||^2>0, eigenvalues positive, inverse via spectral theorem; (b) beta=G^-1A^Ty gives A^T(y-p)=0; uniqueness by ||p'-p||^2=0; (c) P^T=P, P^2=P by G^-1 algebra; Thm 1.3 expansion; Remark 1.4 with w=0. All valid under the stated F1-F4 marker.")
r("MATH-L07-02", "Theorem 2.2 (a)-(c) and the proof; Problem R2, R3 solutions", P + "L07.html:107-121, 319-331", "PASS",
  "Read L07.html:107-121 and R2/R3 (L07.html:319-331). Argument for (a)-(c) and normal equations is sound; R2 linearity and R3 Q^2=Q, A^TQy=0, Qy=0 iff y in W verified algebraically.")
r("MATH-L07-03", "Problem solutions M1-M3, P1-P3, R1, E1-E3 mathematics", P + "L07.html:231-308 and 312-318", "PASS",
  "M1 P=(1/2)[[1,1],[1,1]], p=(1,1), residual (1,-1) orthogonal to A (" + G + "l07_check.py output). M2 beta=(7/6,1/2), fitted 7/6,5/3,13/6, residuals -1/6,1/3,-1/6 summing to 0 and orthogonal to x. M3 25=9+16. R1 existence chain: Theorem 3.7 of L01 (L01.html:161) gives length <= n; W=={0} case correct. E2 A^Ty = (18.3797, 3.0959, -17.6035) matches stated (18.38, 3.10, -17.60).")

r("NUM-L07-01", "Lab 1 printed numbers: coefficients, residual norm, rank", P + "L07.html:190-199 and interpretation L07.html:200; cards M3-c125, c126, c177", "PASS",
  "Independent NumPy recomputation (" + G + "l07_check.py, default_rng(7)): beta=(1.33251885, 0.84881149, -0.41196372) -> 1.3325 0.8488 -0.4120; residual norm 0.8951275 -> 0.8951. Rank of duplicated-column Gram is 2 of 3 (twin output).")
r("NUM-L07-02", "E2 prediction A^T y approx (18.38, 3.10, -17.60)", P + "L07.html:298 (E2 solution)", "PASS",
  "l07_check.py: A^T y = [18.3797, 3.0959, -17.6035] -> 18.38, 3.10, -17.60.")
r("NUM-L07-03", "E3 intercept and generator values 1.5, 0.8, -0.4", P + "L07.html:303-305; lab-M3-L07-1.py generator lines 149-154", "PASS",
  "Code generator: intercept 1.5, slopes 0.8 and -0.4 (lab-M3-L07-1.py:154). Printed intercept 1.3325 (twin output line 7). Fitted value at x1=x2=0 equals beta_0 by the first column of ones (E3 argument correct).")

r("MATH-L08-01", "Propositions 1.1, 1.2, Theorem 1.4, Theorem 2.1, Corollary 2.2, Proposition 2.3, Remark 2.4 proofs", P + "L08.html:56-133", "PASS",
  "Read L08.html:56-133 line by line. Prop 1.2 trace identity checked; Thm 1.4 Z=X~V and Z^TZ=(T-1)Lambda; Thm 2.1 alpha-coordinates and equality case; Cor 2.2; Prop 2.3 c^2 scaling. Remark 2.4 (changed hunk, lines 131-133): M' = D M D with D=diag(..,c,..); M_jj>=0 from x=e_j, then M_jj!=0 by the 2tM_jl+t^2M_ll argument; kappa=c forced by off-diagonal, then M_jj(c^2-c)=0 contradiction. Ordering in the delta is now correct.")
r("MATH-L08-02", "Problem solutions M1-M3, P1-P3, R1-R3, E1-E3 mathematics", P + "L08.html:323-416", "PASS",
  "M1: centred rows (-2,-3),(0,-1),(2,4); M=[[4,7],[7,13]]; trace 17; det 3; eigenvalues (17 +- sqrt 277)/2 (recomputed). M2 shares 2/3,1/6,1/6. M3 9M, shares 2/3,1/3. P1 column sums zero. P3 via Theorem 2.1(a) with e_1. E1 bound = 100 M11/(S0+99 M11) = 0.948346 (independent run, " + G + "l08_check.py not needed; recomputed in shell: 0.9483461). E2 4M. R1 eigenspace argument. R2 centring. R3 algebra (W=BQ, MW=W Gamma) correct; the complement-completion step uses F3 without marker (see ASSUME-03).")

r("NUM-L08-01", "Lab 1 shares, rescale 0.7587 -> 0.9791, M11, trace, E1 bound", P + "L08.html:270-285 and E1 solution L08.html:377", "PASS",
  "Independent recomputation with the twin generator (seed 8): shares 0.75872815, 0.18088840, 0.05161927; rescaled first share 0.9791449; M11 13.681775; trace 88.202753; bound 0.9483461. Printed values 75.9/18.1/5.2, 0.7587/0.9791, 13.6818, 88.2028, 0.9483 all reproduce.")
r("NUM-L08-02", "Planted-shape absolute cosines and component matches", P + "L08.html:277-280 and interpretation L08.html:284", "PASS",
  "Twin output lines 277-280 (0.9994, 0.9985, 0.9990; PC1, PC2, PC3; three distinct). Output equals expected block (see TWIN-02). Interpretation text matches.")
r("NUM-L08-03", "E3 rounding bound", P + "L08.html:389-391", "PASS",
  "Each printed share is rounded to 0.1 percentage point, so each differs by at most 0.05; sum of printed values 75.9+18.1+5.2 = 99.2; bound 0.15 correct.")

r("MATH-L09-01", "Lemma 1.3, Propositions 3.2 to 3.5, Example 2.3, Example 3.6 proofs and numbers", P + "L09.html:73-181", "PASS",
  "Lemma 1.3 trace proof verified. Prop 3.2 eigenvalues max(lambda,eps), PSD, positive definiteness with ||y||=||x|| from QQ^T=I. Prop 3.3(a) via Lemma 1.3. Prop 3.4 congruence; c_ii=1. Prop 3.5 x=e_i+t e_j with delta=|b_ij|/(1+b_jj) gives x^TBx<0. Example 3.6: eigenvalues 2.2 and -0.2, A_0=[[1.1,1.1],[1.1,1.1]], R=[[1,1],[1,1]], ||A-A_0||^2=0.04, ||A-R||^2=0.08. Example 2.3: x^TC0x=-2.4 recomputed.")
r("NUM-L09-01", "Example 2.3 witness value and C0 eigenvalues", P + "L09.html:104-107, 329-331", "PASS",
  "Twin output: C0 eigenvalues -0.800000 1.900000 1.900000 (trace 3, sums to 3) and witness -2.400000. Independent hand calculation 3 + 2(-2.7) = -2.4.")
r("NUM-L09-02", "R entries and ||C0-B||_F^2 = sum of squared negative eigenvalues", P + "L09.html:334-338, 342", "PASS",
  "Twin output: R rows (1,.5,.5),(.5,1,-.5),(.5,-.5,1); ||C0-B||_F^2 = 0.6400000000 = (-0.8)^2 = 0.64.")
r("NUM-L09-03", "E2 distance ||C0 - R||_F", P + "L09.html:438-440; quiz q9 (L09.html:559-562)", "PASS",
  "Differences from R: off-diagonal 0.4, 0.4, -0.4 each in two positions: 6*0.16 = 0.96; sqrt(0.96)=0.9797959 -> 0.9798.")
r("NUM-L09-04", "40-matrix experiment counts and first-instance distances", P + "L09.html:341 and interpretation L09.html:342", "PASS",
  "Twin output: 40 matrices, 23 non-PSD, 23 of 23 correlation within 1e-8, 23 of 23 strictly closer, index-0 distances 0.175527 (R) and 0.163280 (W). Matches printed expected block.")
r("NUM-L09-05", "Example 3.6 squared norms and distances", P + "L09.html:177-180", "PASS",
  "Computed: A-A_0 entries -0.1, 0.1 -> 0.04; A-R off-diagonal 0.2 -> 0.08; formula (0+0.2)^2=0.04.")
r("NUM-L09-06", "Problem numbers: M2 4.88, M3 rescaling, E1 term sum, E3 0.25 and 0.5", P + "L09.html:387-449", "PASS",
  "M2 squared entries 1+1.44+1.44+1=4.88 and 2.2^2+0.2^2=4.88. M3 eigenvalues (13 +- sqrt 41)/2 >0, C12=1/3. E1 terms -1.8,-1.8,-1.8, total -2.4. E3 squared distance 0.25, norm 0.5.")

r("NOTATION-01", "Registered symbols and macros used with registered meaning", "notation/notation.json; " + P + "L07.html, L08.html, L09.html", "PASS",
  "Macros \\tr and \\diag (notation.json) used with matrix trace/diagonal meaning; \\R, \\lVert not conflicting. T used as number of observations in L08 (registry: T = number of return observations) and never with another meaning. No registered symbol (R^\\ast, \\gamma_3, \\Phi, ...) appears in the slice.")
r("NOTATION-02", "Local letters reused across lessons", P + "L07.html, L08.html, L09.html", "PASS",
  "Letters Q, W, B, C, M, G, V, Lambda, Z, S0 are defined locally in each lesson (notation.json 'about': locally defined letters are allowed). No registered symbol is reused.")

r("STRUCT-L07-01", "L07 structure: sections, grade legend, lab, canon breaks, misconceptions, problems, key results, quiz", P + "L07.html", "PASS",
  "Sections s1-s8 present (L07.html:54,98,203,213,231,336,352,424); grade legend L07.html:43-50; one lab section; data-hours=11 matches hub (index.html:154).")
r("STRUCT-L08-01", "L08 structure", P + "L08.html", "PASS",
  "Sections s1-s9 present; one lab; data-hours=12 matches hub (index.html:155).")
r("STRUCT-L09-01", "L09 structure", P + "L09.html", "PASS",
  "Sections s1-s10 present; one lab; data-hours=12 matches hub (index.html:156).")

r("DATA-L08-01", "Claim that the program does not embed a multi-tenor series with three or more tenors", P + "L08.html:291 (canon-breaks bullet 2)", "PASS",
  "course/assets/data/market/MANIFEST.json lists fx_daily, fx_monthly (currency series) and ust_daily; ust_daily.csv header 'date,tbill_3m,cmt_10y' has two tenor columns, so no series with three or more tenors is embedded.")
r("SIM-LABEL-01", "Every lab panel and matrix is labelled SIMULATED and generated in code", "tests/labs/M3/lab-M3-L07-1.py, L08-1.py, L09-1.py; page prose", "PASS",
  "Each twin docstring says SIMULATED with a seed (7, 8, 20261028); each lesson hypothesis and output label says SIMULATED; no data file read.")
r("DAG-01", "Concepts used outside the prerequisite closure", "tools/check_dag.py; L07-L09 meta-row links", "PASS",
  "check_dag.py --unit M3 PASS; meta-rows link L01 vector-space, L03 eigendecomposition, L04 spectral theorem, L05 PSD, L06 used via cross-reference only.")
r("CROSSREF-01", "Cross-lesson citations resolve to the cited result", P + "L07, L08, L09 cross-citations", "PASS",
  "L07: Theorem 3.7 of Lesson 1 = L01.html:161 (a spanning list has no longer independent list); Fact 1.2 of Lesson 6 = L06.html:64 (QQ^T=I); Theorem 2.3 of Lesson 4 = L04.html:130 (spectral theorem). L08: Lesson 7 Theorem 1.2 = L07.html:64 (projection onto column space); Lesson 4 Theorem 2.3; Lesson 5 PSD test; Lesson 6 sign freedom (L06.html:229). L09: Lesson 5 Theorem 2.1 = L05.html:108 (PSD iff eigenvalues nonnegative), used in M1 correctly. Corollary 2.5 is not cited in the slice.")
r("HOURS-01", "Lesson hours match hub split", P + "L07.html:2,35; L08.html:2,35; L09.html:2,35; index.html:154-156", "PASS",
  "data-hours 11 (L07), 12 (L08), 12 (L09) and headers '11 study hours', '12 study hours' x2; hub index.html shows L07 11 h, L08 12 h, L09 12 h.")
r("PROSE-01", "Prose about what a lab prints or checks matches the code and output", P + "L07.html:125-200; L08.html:146-284; L09.html:193-342", "PASS",
  "L07 'does not check that the fitted vector is unique without independent columns' matches code (only specific coefficient pair); L08 'shares computed from unrounded eigenvalues' (lab uses lam/np.sum(lam)); L09 '23 of 40' and '23 of 23' match code and output; 'the lab does not compute the true nearest matrix' matches code.")
r("GRADE-01", "Evidence grades match the basis of each claim", P + "L07.html:342-346; L08.html:428-434; L09.html:484-493; cards.json", "PASS",
  "Theorems/propositions are graded T and cite proofs; lab results graded C with the lab named (L07:346, L08:433-434, L09:492-493). No B or A claim is made.")

r("ASSUME-01", "Results using F1 to F4 say so in their statement, including why-it-matters, canon-breaks and misconception sentences that restate them",
  P + "L07.html:52 (why-it-matters: 'This lesson proves both facts when the columns ... are independent'); " + P + "L08.html:52 (why-it-matters: 'This lesson proves that the first direction carries the largest squared movement'); " + P + "L07.html:218 (misconception 1: 'Remark 1.4 gives the squared residual norm ...'); " + P + "L08.html:308 (misconception 2: 'The shares are unchanged, by Proposition 2.3 with c = 2'); " + P + "L09.html:350 (canon-breaks bullet 3: 'Clipping at a positive floor avoids this (Proposition 3.2(b))'); " + P + "L09.html:360 (misconception 1: 'The result is PSD (Proposition 3.2(a))')",
  "FAIL",
  "Each sentence states, as an unconditional fact, a result whose proof needs F1-F4 (Thm 1.2 and 2.2 via the spectral theorem; Thm 2.1 and Cor 2.2 via Definition 1.3; Remark 1.4; Prop 2.3; Prop 3.2(a) and (b)). The same results carry 'Assuming F1 to F4 of Lesson 4' in their own statements and in the matching cards (cards M3-c143, c144, c165, c181 and others), so the restatements are inconsistent with the rule. Fixed hunks in the delta (L07.html:206, L08.html:137, L09.html:52, L09.html:98, L09.html:342, L09.html:447) show the builder knows the rule.",
  "Prefix each restating sentence with 'Assuming F1 to F4 of Lesson 4,' at: L07.html:52, L08.html:52, L07.html:218, L08.html:308, L09.html:350, L09.html:360. Re-embed nothing (no code change). Then re-run check_pages and page_smoke for the three pages.")
r("ASSUME-02", "Definitions and presuppositions that use F1-F4 must say so", P + "L08.html:140-141 (Definition 3.1); " + P + "L09.html:98, 116, 123, 139, 185, 187, 342, 447", "PASS",
  "Definition 3.1 (L08) and Definition 3.1 (L09 clipping) both begin 'Assuming F1 to F4'; Remark 2.2 and Method 1/2 carry the marker (L09:98, 185, 187); Propositions 3.2 and 3.3 statements carry it (L09:123, 139); lab interpretation L09:342 and E3 solution L09:447 carry it. L08 Section 3 orthogonalization sentence L08.html:137 carries it.")

r("CARD-HYP-01", "Cards carry the F1 to F4 hypothesis when the statement uses it", P + "cards.json ids M3-c117 to c123, c134 to c137, c143 to c145, c153 to c157, c161, c165, c168, c183", "PASS",
  "Each listed card's back begins with or contains 'Assuming F1 to F4 of Lesson 4' where its result needs F; c183 now carries it (delta fix). Cards on Prop 3.4 (c158, c166) do not need it because Prop 3.4's proof uses no F.")
r("CARD-HYP-02", "Cards that depend on Definition 3.1 (L08) or the spectral decomposition in L09 Definition 3.1", P + "cards.json ids M3-c142, M3-c153, M3-c158", "PASS",
  "c142 and c153 carry 'Assuming F1 to F4 of Lesson 4'; c158 states Prop 3.4 whose hypotheses are PSD and positive diagonal, which needs no F marker.")
r("CARD-C183", "Card M3-c183 carries the hypothesis of the proposition it cites", P + "cards.json id M3-c183", "PASS",
  "Back now reads 'Assuming F1 to F4 of Lesson 4, Proposition 3.3(a) gives (0 - (-0.2))^2 = 0.04, and the entries of A - A_0 are -0.1 and 0.1 (Example 3.6).' Round-12 defect fixed. Value 0.04 verified (Example 3.6).")
r("CARD-C161", "Card M3-c161 numbers and eigenvalues", P + "cards.json id M3-c161", "PASS",
  "0.6400000000 and eigenvalues -0.800000, 1.900000, 1.900000 match twin output lines 2 and 4 of the L09 lab; sum of squared negative eigenvalues 0.64.")
r("CARD-C130", "Card M3-c130 states mean-zero of columns of X~, not of M", P + "cards.json id M3-c130", "PASS",
  "Back: 'Every column of X~ has mean zero (Section 1)'; the lesson (L08.html:56) states the same for X~ and not for M.")
r("CARD-C138", "Card M3-c138: c = 1 case and the 'not a multiple of M' claim", P + "cards.json id M3-c138; " + P + "L08.html Remark 2.4 (lines 131-133)", "PASS",
  "Back: 'For c = 1 nothing changes' and 'no single number kappa gives M' = kappa M' match the Remark 2.4 proof and its hypothesis M_jl != 0 (card states 'has a nonzero off-diagonal entry in its row'). Consistent with the remark after the delta.")
r("CARD-OK-01", "All L07, L08, L09 cards agree with the current lesson text (60 cards: 17 L07, 17 L08, 26 L09)", P + "cards.json", "PASS",
  "All 60 cards read against current lesson text (Python filter on lesson field, output in session). Every card number (e.g. 1.3325, 0.8488, -0.4120, 0.8951, 0.7587, 0.9791, 0.6400000000, 0.175527, 0.163280, 0.9798, 75.9, 18.1, 5.2, 0.9994, 0.9985, 0.9990, 0.08, 0.04, 2, 17, 0.5, 2/3) appears in its lesson; the only stale card (c183) was fixed in the delta.")
r("CARD-DUP-01", "No duplicate ids or duplicate cards in L07-L09", P + "cards.json", "PASS",
  "Python check: 0 duplicate ids across the file; 0 duplicate fronts and 0 duplicate backs among the 60 L07-L09 cards (lowercased, stripped).")

r("CLAIM-L07-01", "L07 canon-breaks bullet 1: the sentence about fitted-vector uniqueness", P + "L07.html:206", "PASS",
  "'The lab does not check that the fitted vector is unique without independent columns' is true of the code (it checks only two coefficient vectors). The sentence is consistent with the proof.")
r("CLAIM-L07-02", "L07 canon-breaks bullet 1: 'the fitted vector is unique there too' for dependent columns", P + "L07.html:206; Theorem 1.3 proof L07.html:90; Problem R1 L07.html:316", "PASS",
  "Minimizer of ||y-w|| over W is unique by Theorem 1.3's expansion, and the projection's uniqueness follows from R1's argument, which needs no F; existence of the minimizer for any A is stated with the Assuming F1 to F4 marker in the same sentence (L07.html:206). Fitted vector unique; coefficients not unique for dependent columns (Lab 1 duplicated column, twin output line 10).")
r("CLAIM-L07-03", "L07 canon-breaks bullet 1: the R1 existence claim carries its F1-F4 marker", P + "L07.html:206 (sentence 'Problem R1 shows ... exists and is unique')", "PASS",
  "The sentence now reads 'Assuming F1 to F4 of Lesson 4, Problem R1 shows that an orthogonal projection onto any subspace exists and is unique'. R1 (L07.html:316) states that its existence argument uses Theorem 1.2, which requires F1-F4. Round-12 defect fixed.")

r("REMARK-L08-01", "L08 Remark 2.4: multiplying one column by c 'changes M in a way that is not a multiple of M'", P + "L08.html:131-133", "PASS",
  "Recomputed: centring commutes with column scaling, so X~' = X~ D and M' = D M D with D=diag(1,..,c,..,1). Diagonal M_jj -> c^2 M_jj, row/column j off-diagonal -> c M_jl. Not a multiple of M when M_jl != 0 and c != 0,1.")
r("REMARK-L08-02", "L08 Remark 2.4: 'so no single number kappa gives M' = kappa M' needs M_jj != 0", P + "L08.html:131-133", "PASS",
  "Sentence order is now: Taking x=e_j gives M_jj>=0; we show M_jj!=0 next so M_jj>0; then the lemma's negative-quadratic-form argument; then kappa=c and M_jj(c^2-c)=0 contradicts M_jj>0 and c^2!=c. The positivity is established before use.")
r("REMARK-L08-03", "L08 Remark 2.4: positivity of M_jj asserted before its nonnegativity step", P + "L08.html:131-133", "PASS",
  "Round-12 defect fixed: the text now derives M_jj>=0 from Proposition 1.1 with x=e_j before using M_jj>0. Ordering verified by reading the hunk. Sentence 'We show M_jj != 0 next, so M_jj > 0' is a forward reference to the next argument, which is valid.")

r("PROSE-02", "Scope words ('onto any subspace', 'every', 'any', 'always', 'only') in slice prose", P + "L07.html:206, 316; L08.html:132, 137, 282-284; L09.html:98, 118, 147, 349", "PASS",
  "Each scope word checked against its computation or hypothesis: 'onto any subspace' (L07:206) now carries Assuming F1 to F4; 'every' in L08:132 (every column/row) and L09:147 (every term) are local and proved; 'the results below hold for any choice' (L09:118) is proved for arbitrary Q in the proofs; 'the proposition covers every nonzero c' (L08 E2) matches Prop 2.3's statement.")
r("PROCESS-01", "No process words in learner text", P + "L07.html, L08.html, L09.html", "PASS",
  "Grep for round, builder, verifier, audit, reviewer, todo, placeholder, architect, erratum, corrected, previous version: no hits in the three pages.")

r("ASSUME-03", "Problem statements and solutions that use F1-F4 or F3 say so in their statement",
  P + "L08.html:414-416 (Problem R3 statement and solution); " + P + "L08.html:359 (Problem P2 solution)", "FAIL",
  "R3 (L08.html:414-416): the completion of W to an orthonormal eigenbasis of M needs an orthonormal basis of the complement of col(B), which is F3 (Lesson 4), and the rank-3 invertibility of G needs F1; neither the statement nor the solution marks this. P2 (L08.html:359): the solution asserts that v_1..v_n is an orthonormal eigenbasis of M, which the statement ('if M has eigenvalues lambda_k with eigenvectors v_k') does not supply and which needs the spectral theorem (F1-F4).",
  "R3 statement: prefix 'Assuming F1 to F4 of Lesson 4,'. P2 statement: prefix 'Assuming F1 to F4 of Lesson 4, let M = V Lambda V^T with V orthogonal,' and state the eigenvector hypothesis as given. Re-run check_pages for L08 and page_smoke.")

r("ASSUME-04", "Research and proof problems whose solutions use F1-F4 without the marker (L07 and L09 problem set)",
  P + "L07.html:316 (R1) and L09.html:447 (E3)", "PASS",
  "R1 of L07 already carries the marker in its solution text ('Assuming F1 to F4 of Lesson 4, existence uses a basis'); E3 of L09 carries it in the solution. No defect.")

r("REG-01", "Registry/notation: symbols used by the slice have registered meaning or are local", "notation/notation.json; " + P + "L07.html, L08.html, L09.html", "PASS",
  "Program-wide registry lists T (observations), \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. Slice uses T only as observation count (L08) and the macros \\tr, \\diag, \\R. No other registered symbol appears.")

fragment = {
  "unit": "M3",
  "slice": "c",
  "round": 13,
  "verifier": "independent Haiku verifier, fresh checkout verifyB13-M3-c",
  "pin": "fca6bb104984c6a724fc214d8073158e610e995a",
  "base": "ff388424d9d056b7a57868dab5ae7f7cdeef60f6",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyB13-M3-c",
  "scratch": "/Users/billyribeiro/.fanout/wt/verifyB13-M3-c/ledgers/M3/scripts/M3-c-r13",
  "verified_at": "2026-10-29",
  "verdict": "FAIL",
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": "Slice: course/modules/M/M3/L07.html, L08.html, L09.html; tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py; cards with lesson L07, L08, L09 in course/modules/M/M3/cards.json (60 cards). Delta ff38842..fca6bb1 for the slice: L07.html lines 206 and 316; L08.html lines 132 and 137; L09.html lines 52, 98, 342, 447; cards.json lines 1280 (M3-c183) and 1287 (M3-c184, L02, out of slice). project.html in the delta is outside this slice. Mutation testing not applicable: lab twins are demonstrations and the slice has no project grader (ruling). All gates re-run on the pin. Rows whose subject changed were re-verified from the page text this round; no PASS row is carried by prefix. Scope of ASSUME-01 and ASSUME-03: statements, why-it-matters, canon-breaks, misconception and problem statements that restate an F1-F4 result. Citations inside solutions and quiz explanations were not graded one by one; the verifier checked that the claims they carry are proved or marked.",
  "summary": "M3 slice c round 13 on fca6bb1: all gates PASS (check_pages, check_dag, check_projects, build_site --check, render diff, run_labs x3, page_smoke x4, ruff, mypy, pytest -k M3, verify_refs --offline, fetch_data --check). All three twins run clean under python -I -W error and match page code and expected blocks. Round-12 FAILs ASSUME-01 (canon-breaks R1 sentence), CLAIM-L07-03, REMARK-L08-03, CARD-C183 and CARD-OK-01 are fixed and PASS. The new delta is re-verified line by line. Non-PASS: ASSUME-01 (six restating sentences in why-it-matters, canon-breaks and misconceptions lack the F1-F4 marker that their results carry elsewhere), ASSUME-03 (L08 Problem R3 and P2 use F1/F3 or an orthonormal eigenbasis without the marker). Verdict FAIL.",
}
out = "ledgers/M3/M3-c.json"
json.dump(fragment, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", len(rows), "non-PASS", [r_["id"] for r_ in rows if r_["status"] != "PASS"])
