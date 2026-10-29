"""Writes the round-6 verifier fragment for M3 slice a (rows are the verifier's findings; no fixes applied)."""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB6-M3-a")
PASS, FAIL, UNV = "PASS", "FAIL", "UNVERIFIABLE"
M3 = "course/modules/M/M3"

rows = [
    # hub
    dict(id="a6-hub-structure", check="2.9 structure", location=f"{M3}/index.html:29-182",
         status=PASS, evidence="check_pages.py --unit M3: PASS (run). Hub has objectives (45-57), prerequisites (59-66), placement quiz with 9 items (68-142), lesson map of 9 cards (144-158), ladder with 4 rungs (160-169), data status (171-174), core reading (176-182)."),
    dict(id="a6-hub-hours", check="2.9 hours arithmetic", location=f"{M3}/index.html:29,40,42,148-156; L01-L03 <html data-hours>",
         status=PASS, evidence="Card kickers 12+11+12+12+12+11+11+12+12 = 105 = data-hours-lessons (29). Project 45 = data-hours-project. 105+45 = 150 = curriculum hours (curriculum/01-foundations.yaml:160). 45/150 = 30%, inside 10-40%. Bar widths 70%/30% (40) match. L01 data-hours 12, L02 11, L03 12 equal their card kickers and page eyebrows."),
    dict(id="a6-hub-placement", check="2.9 placement arithmetic and keyed answers", location=f"{M3}/index.html:68-142",
         status=PASS, evidence="Items: 7 M1 + 2 skill checks = 9. 80% of 9 = 7.2, so 8 needed; 7/9 = 77.8%, 8/9 = 88.9% (line 70 matches). Keys re-derived: 1+1/2+1/4+1/8 = 1.875; 100/1.05^2 = 90.70295 -> 90.703 (tolerance 1e-4 accepts it); sum_{k<n} q^k = (1-q^n)/(1-q); induction step; contrapositive is 'not Q implies not P'; skill 1 dim span{(1,0,1),(0,1,1),(1,1,2)} = 2; skill 2 C = D^-1 Sigma D^-1."),
    dict(id="a6-hub-data-claims", check="2.8 data status; 2.9 prose", location=f"{M3}/index.html:37,173; course/assets/data/market/MANIFEST.json:78-79; tests/labs/M3/lab-M3-L08-1.py:6,21",
         status=PASS, evidence="MANIFEST ust_daily columns tbill_3m and cmt_10y only (two series), as line 173 says. L08 twin defines six tenors 0.25,0.5,1,2,5,10 (line 21) and labels SIMULATED (line 1). grep: no data-files attribute on index/L01/L02/L03 (0 hits), so no lab in these pages reads a data file. Hub line 37 'worked labs ... labelled SIMULATED' is read as the project's three worked labs (data-status line 173 says that exactly); the project page is slice d."),
    dict(id="a6-hub-m1-refs", check="2.9 cross-references", location=f"{M3}/index.html:70,79,84,89,98,107,116; {M3}/L01.html:37",
         status=PASS, evidence="M1 L01 is 'Sets, Quantifiers and Logical Statements' with Theorem 3.1 on negation (course/modules/M/M1/L01.html); M1 L02 'Direct Proof...'; M1 L05 'Present value...'; M1 L06 'Geometric Series and Proof by Induction'. Each cited number matches its title."),
    dict(id="a6-hub-cards", check="2.9 lesson cards vs pages", location=f"{M3}/index.html:148-150 vs L01-L03 h1",
         status=PASS, evidence="Card titles equal the h1 of L01 'Vector Spaces, Spans, Bases and Dimension', L02 'Linear Maps and Their Matrices', L03 'Eigendecomposition'; card descriptions (linear maps, kernel/image, change of basis; eigenvalues, diagonalization, residuals) match page content."),
    # L01
    dict(id="a6-L01-defs-props-1", check="2.4 mathematics (Def 1.1, Lemma 1.3, Prop 1.4)", location=f"{M3}/L01.html:55-86",
         status=PASS, evidence="Re-derived by hand: 0v = 0 from (iv); (-1)v = -v with uniqueness of inverse; subspace test both directions; all steps cite axioms correctly."),
    dict(id="a6-L01-span-prop", check="2.4 mathematics (Prop 2.2, Ex 2.3)", location=f"{M3}/L01.html:96-109",
         status=PASS, evidence="Prop 2.2 proof checks (a),(b),(c) and minimality. Ex 2.3 statement correct (span(e1,e2) = {(a,b,0)}). The use of e1,e2 before their definition is a separate FAIL row."),
    dict(id="a6-L01-indep-rank-thms", check="2.4 mathematics (Def 3.3, Lemma 3.4, Prop 3.5, Cor 3.6, Thm 3.7, Thm 3.8)", location=f"{M3}/L01.html:126-180",
         status=PASS, evidence="Each proof re-derived: free-variable construction in Lemma 3.4; pivot-column argument j_i = i in Prop 3.5 (distinct increasing j_1<...<j_k<=k forces j_i=i); Cor 3.6 from Lemma 3.4 with m=n; Thm 3.7 coefficient computation; Thm 3.8 from Thm 3.7 in both directions. Hypotheses listed for each statement."),
    dict(id="a6-L01-prop312", check="2.4 mathematics (Prop 3.12)", location=f"{M3}/L01.html:363-371",
         status=PASS, evidence="Map phi: N(A) -> R^F is linear, injective (back substitution from last pivot row), surjective (free unknowns arbitrary, zero rows impose nothing); basis of N(A) of size k-p; Theorem 3.8 applied; p independent of echelon form. Argument complete for the stated hypotheses."),
    dict(id="a6-L01-examples", check="2.4 numbers in examples", location=f"{M3}/L01.html:188-190",
         status=PASS, evidence="Ex 3.10: v1+v2 = (1,1,2) = v3; span of v1,v2 = {(a,b,a+b)}; dimension 2. Planted v4 = 2v1 - v2 + v3 is a dependent list of the same kind (checked: entries in range)."),
    dict(id="a6-L01-lab-twin-page", check="2.5 labs: twin vs page, expected vs output, -I -W error, runtime", location="tests/labs/M3/lab-M3-L01-1.py; L01.html:195-355; ledgers/M3/scripts/M3-a-r6/twin_vs_page.py",
         status=PASS, evidence="twin_vs_page.py: page code == twin (True, 147 lines); `python -I -W error lab-M3-L01-1.py` exit 0; expected block == run output (True); runtime 0.05 s. run_labs.py --unit M3 --page L01 PASS. Stdlib only, declares no packages (correct)."),
    dict(id="a6-L01-lab-numbers", check="2.5 labs: numbers re-derived", location="ledgers/M3/scripts/M3-a-r6/recount.py",
         status=PASS, evidence="Independent numpy.linalg.matrix_rank recount with the same LCG: R^3 3-vectors 188/200, R^3 4-vectors 0/200, R^4 4-vectors 198/200, R^4 5-vectors 0/200; planted: dependent 100/100, independent triples 100/100, rank-3 100/100. Matches printed output exactly."),
    dict(id="a6-L01-lab-claims", check="2.5 labs: hypothesis and interpretation vs output", location=f"{M3}/L01.html:194,355",
         status=PASS, evidence="Predictions 0 of 200 (Cor 3.6), 100 of 100 (Prop 3.5 planted), rank-3 count = triple count, 100 of 100 membership test: all agree with printed lines 343-354. 'Not predicted' counts are exactly the R^3 3-vector and R^4 4-vector lines. The 188 of 200 figure is stated as run-specific (matches output)."),
    dict(id="a6-L01-problems", check="2.4 worked solutions (M1-M3, P1-P3, E1-E3, R1-R3)", location=f"{M3}/L01.html:408-503",
         status=PASS, evidence="All solutions re-derived. M1 u+v=w; M2 xy=0 not closed under addition ((1,0)+(0,1)); M3 basis p,q; P1 intersection; P2 independence extension; P3 span removal; E2 rank 2 (rows (1,2,0),(2,4,1),(3,6,1) reduced); R1; R2 degree argument; R3 2x2 pivot 1e-12 example (exact det 1e-12 != 0). E1/E3 statements match output."),
    dict(id="a6-L01-quiz", check="2.9 retrieval quiz keys and explanations", location=f"{M3}/L01.html:527-610",
         status=PASS, evidence="10 items, each with explanation. Keys re-checked: e1+e2 dependence; dim 2; four vectors in R^3 dependent; (1,0),(0,1),(1,1) dependent; rank of [e1,e2,e3,(1,1,1)] = 3; first-coordinate-zero set is the subspace; 0v = zero vector; basis of plane z=0; dim R^5 = 5; planted count is for the draws, the all-draws claim is Prop 3.5."),
    dict(id="a6-L01-key-results", check="2.3 grades", location=f"{M3}/L01.html:513-521",
         status=PASS, evidence="Proved results graded T with 'Proved in' locators on the page; lab-derived count graded C naming Lab 1 (matches BLUEPRINT grade use)."),
    dict(id="a6-L01-structure-prose", check="2.9 structure and prose: banned phrases, process words, length, external requests", location=f"{M3}/L01.html (whole page)",
         status=PASS, evidence="why-it-matters 95 words (<=120). 3 misconceptions, 4 problem tiers with 3 problems each, quiz 10, key-results table, canon-breaks section present. grep for TODO/TBD/lorem/brevity/omitted/beyond the scope/well known/obviously/clearly/it can be shown/studies show: 0 hits. 'e1, ..., e4' in lab code is mathematical list notation, not omission. No process words (architect, builder, verifier, round, ledger). No http(s) URLs in index/L01/L02/L03."),
    dict(id="a6-L01-misconceptions", check="2.9 misconceptions", location=f"{M3}/L01.html:384-400",
         status=PASS, evidence="Misconception 1 (three non-zero vectors in R^3 need not be a basis): Ex 3.10 correct. Misconception 2 (four vectors in R^3): Cor 3.6 correct. Misconception 3 (pairwise non-proportional is not sufficient): (1,1)=(1,0)+(0,1) correct; the stated direction (independent pair => not proportional) is correct."),
    # L02
    dict(id="a6-L02-maps-matrices", check="2.4 mathematics (Def 1.1 to Thm 2.4, Prop 3.1)", location=f"{M3}/L02.html:55-149",
         status=PASS, evidence="Lemma 1.2, Prop 1.4, Prop 2.2, Thm 2.4, Prop 3.1 proofs re-derived; column-convention matrix definitions consistent; Remark 2.5 argument correct; Ex 1.5 (L(x,y)=(x+y,x-y)) and Ex 2.6 matrix [[0,2],[1,0]] recomputed."),
    dict(id="a6-L02-change-of-basis", check="2.4 mathematics (Thm 4.1, Cor 4.2, Ex 4.3)", location=f"{M3}/L02.html:151-178",
         status=PASS, evidence="Thm 4.1 proof: z = P^{-1}AP y, Pz = Ax, uniqueness gives [Ax]_B = z; columns agree. Cor 4.2 algebra correct. Ex 4.3: AP = [[1,2],[1,0]], P^{-1}AP = [[0,2],[1,0]] recomputed."),
    dict(id="a6-L02-lab-twin-page", check="2.5 labs: twin vs page, expected vs output, -I -W error", location="tests/labs/M3/lab-M3-L02-1.py; L02.html:183-357; M3-a-r6/twin_vs_page.py",
         status=PASS, evidence="Page code == twin (True, 165 lines); twin exit 0 under -I -W error; expected block == output (True); runtime 0.03 s; run_labs --unit M3 --page L02 PASS; stdlib only."),
    dict(id="a6-L02-lab-numbers", check="2.5 labs: numbers re-derived", location="ledgers/M3/scripts/M3-a-r6/recount.py",
         status=PASS, evidence="numpy recount: 7 singular draws rejected; coordinate formula 50/50; composition 50/50; first-pair matrix [[3,-17.5,12.333],[0,5,-1.667],[-2,8,-6]] equals printed 3 -35/2 37/3 / 0 5 -5/3 / -2 8 -6. Float check bound 1e-12 relative to max(1,|entry|) per hypothesis line 182."),
    dict(id="a6-L02-lab-claims", check="2.5 labs: hypothesis and interpretation vs output", location=f"{M3}/L02.html:182,358",
         status=PASS, evidence="'Should be 50 of 50' (x2) and 'the 7 rejected draws', 'row 1 is 3, -35/2, 37/3' all match printed lines 349-357. Interpretation says counts are for listed pairs only, matching the code's docstring scope."),
    dict(id="a6-L02-misconceptions-problems", check="2.4 misconceptions, problem solutions", location=f"{M3}/L02.html:372-493",
         status=PASS, evidence="AN=[[2,1],[1,1]] vs NA=[[1,1],[1,2]] correct; coordinates of (1,1) in basis (1,0),(1,1) = (0,1) correct; M1 matrix [[2,-1],[1,0]]; M2 coordinates (2,1); M3 kernel/image; P1-P3; E2 hand product [[0,2],[1,0]]; R1 change-of-basis composition; R2 set description (converse flagged as unproved); R3 derivative matrix [[0,1,0,0],[0,0,2,0],[0,0,0,3],[0,0,0,0]] and action (c1, 2c2, 3c3, 0) correct."),
    dict(id="a6-L02-quiz-keyresults", check="2.9 quiz keys; 2.3 grades", location=f"{M3}/L02.html:495-596",
         status=PASS, evidence="10 items with explanations; keys re-checked (x+y,0) linear; row2 col1 = 1; S o L = [S][L]; P B P^{-1} = A; first coordinate 2; kernel = {(0,y)}; (x+y,x-y) row1 col2 = 1; S o L linear always. Key results: proved items T, lab item C."),
    dict(id="a6-L02-structure-prose", check="2.9 structure, banned phrases, process words, length", location=f"{M3}/L02.html (whole page)",
         status=PASS, evidence="why-it-matters 112 words (<=120). 3 misconceptions; 4 tiers x 3 problems; quiz 10; canon-breaks present; no banned-phrase hits; no process words; no external URLs."),
    # L03
    dict(id="a6-L03-assumption-defs", check="2.4 mathematics (F1, Def 1.1, 1.2, Prop 1.3, 1.4, Def 1.5)", location=f"{M3}/L03.html:55-103",
         status=PASS, evidence="F1 stated as assumption with 'Assuming F1' labels on every dependent result (checked: Prop 1.4, Def 1.5, Prop 2.2, 2.3, 2.6, Ex 2.5). Prop 1.3 proof correct and needs no F1. Prop 1.4 proof correct under F1."),
    dict(id="a6-L03-example-numbers", check="2.2 numbers and mathematics (Ex 1.6, Remark 1.7, Ex 2.5)", location=f"{M3}/L03.html:97,101-103,144",
         status=PASS, evidence="Ex 1.6: p_A = lambda^2 - 7 lambda + 11; roots (7 +- sqrt5)/2 = 4.6180, 2.3820 (recomputed); eigenvector (1, lambda-4) checked symbolically. Remark 1.7: det(R - lambda I) = lambda^2+1. Ex 2.5 eigenvectors (1,0,0),(1,1,0),(1,3,6) checked; det P = 6 (cofactor). The independence step is a separate FAIL row."),
    dict(id="a6-L03-decomp-props", check="2.4 mathematics (Def 2.1, Prop 2.2, 2.3, 2.4, 2.6)", location=f"{M3}/L03.html:107-155",
         status=PASS, evidence="Prop 2.2 proof (AP=PD, independence gives invertibility under F1) correct; Prop 2.3 converse correct; Prop 2.4 induction correct; Prop 2.6: det(B - lambda I) = (1-lambda)^2, E_1 = {(x,0)}, dimension 1 via Lesson 1 Theorem 3.7 correct."),
    dict(id="a6-L03-lab-twin-page", check="2.5 labs: twin vs page, expected vs output, -I -W error, numpy declared", location="tests/labs/M3/lab-M3-L03-1.py; L03.html:157-253; M3-a-r6/twin_vs_page.py",
         status=PASS, evidence="Page code == twin (True, 82 lines); twin exit 0 under -I -W error (numpy available in .venv); expected block (tolerance 1e-9) == output (True); data-packages=\"numpy\" declared; runtime 0.06 s; run_labs --unit M3 --page L03 PASS; run_labs --unit M3 12/12 PASS."),
    dict(id="a6-L03-lab-claims", check="2.5 labs: hypothesis, interpretation and key-results vs output", location=f"{M3}/L03.html:159,252,402",
         status=PASS, evidence="Printed lines 243-251 match the hypothesis (3 of 3; AP=PD; det 6; eigenvalues 2,3,5; B double root, rank 1, dimension 1 below 2). Lab docstring says it prints verdicts, rounded eigenvalues and rank, not raw residuals: matches code lines 231-239."),
    dict(id="a6-L03-problems", check="2.4 worked solutions (M1-M3, P1-P3, E1-E3, R1-R3)", location=f"{M3}/L03.html:290-387",
         status=PASS, evidence="M1 eigen (3,1) and vectors (1,0),(1,-1) checked; M2 eigenvalues 0,5 with (2,-1),(1,2) checked; M3 P D P^{-1} = [[1,2],[2,4]] recomputed; P1 independence proof; P2 inverse proof uses F1 correctly; P3 eigenvalue of inverse; E1/E2/E3 match output; R2 rotation argument correct; R3 A^3 = [[27,26],[0,1]] by two routes (P D^3 P^{-1} and direct)."),
    dict(id="a6-L03-quiz-keyresults", check="2.9 quiz keys; 2.3 grades", location=f"{M3}/L03.html:389-487",
         status=PASS, evidence="10 items with explanations; keys re-checked (diag(3,5) larger eigenvalue 5; 4.6180 within tolerance 5e-5 of exact 4.618034; I_2 has basis of eigenvectors; B has no basis of eigenvectors; dim E_1 = 1; rotation has no real eigenvalue; det P = 6; A^2 = P D^2 P^{-1}). Key results: proved items T under F1, lab item C."),
    dict(id="a6-L03-misconceptions", check="2.9 misconceptions", location=f"{M3}/L03.html:266-282",
         status=PASS, evidence="Misconception 1: det(A-4I) = -1 and det(A-3I) = -1 recomputed, so 4 and 3 are not eigenvalues of [[4,1],[1,3]]. Misconception 2: I_2 has basis of eigenvectors. Misconception 3: B has real eigenvalue 1 but no eigenbasis."),
    dict(id="a6-L03-structure-prose", check="2.9 structure, banned phrases, process words, length", location=f"{M3}/L03.html (whole page)",
         status=PASS, evidence="why-it-matters 77 words. 3 misconceptions; 4 tiers x 3 problems; quiz 10; canon-breaks present; no banned-phrase hits; no process words; no external URLs. 'Assumption F1' is named in the why-it-matters paragraph before Section 1 introduces it; the name is a label and the definition follows in the first block, so no separate row."),
    # cross-slice
    dict(id="a6-dag-concepts", check="2.9 DAG: check_dag, links, definitions", location="course/modules/M/M3/{index,L01,L02,L03}.html",
         status=PASS, evidence="check_dag.py --unit M3: PASS (run). Definitions: vector-space (L01 dfn), linear-map (L02 dfn), eigendecomposition (L03 dfn), each once. Links to quantifiers and direct-proof (M1, concepts.html), mathematical-induction (M1), vector-space and linear-map (earlier lessons). No later-lesson concept linked. Terms basis, span, rank, determinant, eigenvalue, singular value are plain prose (architect decision Q4), not linked."),
    dict(id="a6-citations", check="2.1 citations in slice", location=f"{M3}/index.html:179; {M3}/L0[1-3].html references sections",
         status=PASS, evidence="Only keys axler2024linear and strang2023introduction appear and no statement is attributed to them; references say no passage locator is confirmed. check_pages.py --unit M3 PASS validates keys. No data-locator in slice."),
    dict(id="a6-notation-registry", check="3.1-3.2 notation registry", location="notation/notation.json; L01-L03 macros",
         status=PASS, evidence="Macros used in slice: \\R (registered), \\diag (registered, L03 Prop 2.2 onward), standard KaTeX commands otherwise. Registered meanings (T = number of observations, R^*, Phi, gamma_3 ...) are not used in slice. Symbol S overload is a separate FAIL row."),
    dict(id="a6-gates-lint-types", check="gates: ruff, mypy, pytest (lab tests)", location="tests/labs/M3; repo",
         status=PASS, evidence="ruff check . : All checks passed. ruff check tests/labs/M3 and ruff format --check tests/labs/M3 : passed (12 files formatted). mypy --no-incremental : Success, 255 source files. pytest tests/test_labs.py -k M3 : 12 passed. Note: the unfiltered tests/test_labs.py run fails for E3 project labs (missing twins under tests/labs/E3 in this checkout), outside slice a."),
    dict(id="a6-render-page-smoke", check="2.9 page_smoke (console errors, KaTeX rendering, no external requests, no horizontal scroll at 360 px)", location="tools/page_smoke.py --unit M3",
         status=UNV, evidence="tools/page_smoke.py --unit M3 could not start: Playwright Chromium headless shell not installed (BrowserType.launch: Executable doesn't exist at /Users/billyribeiro/Library/Caches/ms-playwright/chromium_headless_shell-1248/...). Not installed by the verifier (toolchain policy). Static substitute: no external URLs in slice; all macros registered or standard KaTeX. Rendering, console errors and 360 px layout are unchecked.",
         fix="Install the Playwright Chromium build for the pinned runtime through the user's own mise/playwright setup, then run `.venv/bin/python tools/page_smoke.py --unit M3` on a quiet machine and record its output in this fragment."),
    # FAIL rows
    dict(id="a6-L01-defuse-e-i", check="2.9 / BUILDER 1.5 define before use", location=f"{M3}/L01.html:108 (Example 2.3) vs :184 (Example 3.9)",
         status=FAIL, evidence="Example 2.3 (line 108) uses e_1 and e_2 ('span(e_1, e_2) is the set of vectors (a,b,0)'). The symbol e_i is defined only in Example 3.9 (line 184: 'Let e_i be the vector in R^n with 1 in position i'). Used before definition.",
         fix="Move the definition of e_i (and the standard unit vectors) into Section 2 before Example 2.3, or define e_1, e_2 inside Example 2.3; leave Example 3.9 as the basis statement."),
    dict(id="a6-L01-dag-simple-return", check="2.9 / BUILDER 1.10 DAG: concept used outside closure", location=f"{M3}/L01.html:51",
         status=FAIL, evidence="The why-it-matters paragraph names 'simple return of a portfolio' and 'simple returns of its assets'. In curriculum.json concepts, 'simple-return' is owned by CS1, which is not in M3's closure (M3 prereqs [M1]; M1 prereqs P0.1). Not in the plan's B1-B4 list.",
         fix="Reword the sentence without the concept name, e.g. 'a portfolio's return is a weighted sum of its assets' returns, with weights equal to the starting value shares', or report a DAG_DEFECT to the architect."),
    dict(id="a6-L01-lab-docstring-claim-b", check="2.5 labs: docstring claims vs code", location="tests/labs/M3/lab-M3-L01-1.py:201-202 (also L01.html:195-201)",
         status=FAIL, evidence="Docstring claim (b): 'on the seeded lists, every list of more than n vectors in R^n is dependent'. The code draws only lists of exactly n+1 vectors (count_independent calls at (3,3),(3,4),(4,4),(4,5) in main, lines 313-316). Lists with more than n+1 vectors are not drawn, so the claim overstates what the lab checks.",
         fix="Edit the docstring claim (b) to 'on the seeded lists of n+1 vectors in R^n, the count of independent lists is 0 (Corollary 3.6 gives this for every list)'; then run tools/embed_labs.py course/modules/M/M3/L01.html --refresh lab-M3-L01-1."),
    dict(id="a6-L02-notation-S", check="3.2 notation: one symbol, one meaning within a lesson", location=f"{M3}/L02.html:138 (S : W -> Z linear) vs :182, :185, :448-464 (S invertible matrix)",
         status=FAIL, evidence="Proposition 3.1 (line 138) and Problem R1 use S for a linear map W -> Z. The hypothesis (line 182), the lab docstring (twin lines 185-188), Problem E1 (line 448) and E3 (line 462) use S for an invertible integer matrix in S^{-1}AS. The same letter has two meanings in the lesson. Not a registry symbol, but the page never says which is meant in the lab text.",
         fix="Rename the matrix in the lab text and its hypothesis/E1/E3 (for example Q, with Q^{-1}AQ), or state 'here S is a matrix' at line 182; then refresh the lab with embed_labs.py if the twin changes."),
    dict(id="a6-L03-ex25-independence", check="2.4 mathematics: justification gap", location=f"{M3}/L03.html:144",
         status=FAIL, evidence="Example 2.5: 'Proposition 2.2 applies, because the columns are independent (the determinant of P is 6, so, assuming F1, P is invertible)'. The text gives invertibility, not independence, and the step from invertibility to independence (F1: Px = 0 only trivially) is not written. The stated reason does not directly support the stated conclusion.",
         fix="Write the chain: det P = 6 != 0, so under F1 P is invertible, so under F1 Px = 0 forces x = 0, so the columns are independent."),
    dict(id="a6-L01-lab-generated-inputs-label", check="2.8 SIMULATED label where inputs are generated", location=f"{M3}/L01.html:193-194; {M3}/L02.html:181-182",
         status=PASS, evidence="L01 and L02 labs draw seeded integer matrices (L01 line 194 'drawn by a fixed generator'; L02 docstring 'seeded'). They are exact linear-algebra inputs, not data presented as real, and no SIMULATED label is attached (contrast L04-L08). Recorded as a consistency note only; not a fail."),
]

fragment = {
    "unit": "M3",
    "slice": "a",
    "round": 6,
    "verifier": "independent Haiku verifier (round 6), not a builder of M3",
    "pin": "44f1eb6",
    "base": "44f1eb6 (no round-5 fragment exists at /Users/billyribeiro/.fanout/frags/B-M3-a.round5.json; the fragments folder is empty, so no PASS row is carried)",
    "checkout": str(ROOT),
    "scratch": str(ROOT / "ledgers/M3/scripts/M3-a-r6"),
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice a = hub index.html, L01-L03 and their lab twins. Mutants are not required for a lesson slice (VERIFIER_RULES 2.6 applies to project slices). "
        "Counts re-derived with numpy (scripts/recount.py) and page-vs-twin-vs-output checked (scripts/twin_vs_page.py). "
        "Not checked: page_smoke (no Chromium; rendering, console, 360 px); Pyodide execution of the twins; verify_refs (no registry key in slice is re-resolved here; the scheduled job covers it); "
        "fixes were not applied (report-only). Rows are fresh for pin 44f1eb6 because no earlier fragment exists to carry."
    ),
    "summary": "",
}
counts = {s: sum(1 for r in rows if r["status"] == s) for s in (PASS, FAIL, UNV)}
fragment["summary"] = (
    f"{len(rows)} rows: {counts[PASS]} PASS, {counts[FAIL]} FAIL, {counts[UNV]} UNVERIFIABLE. "
    "FAIL: e_i used before definition (L01:108); 'simple return' is a CS1 concept (L01:51); lab docstring claim (b) overstates (L01 twin 201-202); "
    "S used for a map and a matrix (L02:138 vs 182); Example 2.5 independence step missing (L03:144). UNVERIFIABLE: page_smoke not runnable."
)
out = ROOT / "ledgers/M3/M3-a.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out, counts)
