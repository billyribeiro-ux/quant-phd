import json, sys
S = "ledgers/M3/scripts/M3-c-r16"
from datetime import date
R = "Carried from round 15 (course/modules/M/M3/L08.html, L08 twin, notation, registry byte-identical since the previous pin 448548f): "
RV = "Re-verified in round 16 (hunks 5e88c50 vs 448548f read): "
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# gates
row("GATE-01", "2.9-gate", "tools/check_pages.py", "PASS", "check_pages.py --all: 'check_pages M3: PASS', exit 0 (log " + S + "/check_pages.log)")
row("GATE-02", "2.9-gate", "tools/check_dag.py", "PASS", "check_dag.py --all: 'check_dag M3: PASS', exit 0 (" + S + "/check_dag.log)")
row("GATE-03", "2.9-gate", "tools/build_site.py", "PASS", "build_site.py --check: 'site data current: 6 outputs', exit 0 (" + S + "/build_site.log)")
row("GATE-04", "2.9-gate", "tools/render_curriculum.py", "PASS", "render_curriculum.py exit 0; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json exit 0 (" + S + "/render_diff.log)")
row("GATE-05", "2.5-labs", "tools/run_labs.py --unit M3", "PASS", "run_labs M3: PASS (12/12), exit 0 (" + S + "/run_labs_M3.log)")
row("GATE-06", "2.9-gate", "tools/page_smoke.py --unit M3 --pages L07 L08 L09", "PASS", "page_smoke M3: PASS; each of L07, L08, L09 PASS with lab timing under 1 s (" + S + "/page_smoke.log)")
row("GATE-07", "gate-ruff", "pyproject.toml", "PASS", "ruff check . exit 0; ruff format --check: '358 files already formatted' (" + S + "/ruff.log)")
row("GATE-08", "gate-mypy", "pyproject.toml", "PASS", "mypy --no-incremental: 'Success: no issues found in 255 source files', exit 0 (" + S + "/mypy.log)")
row("GATE-09", "gate-pytest", "tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_docs_figures.py tests/test_page_smoke.py", "PASS", "pytest on the five suites: 0 failures (" + S + "/pytest_labs.log, " + S + "/pytest_docs.log). Only the lab-related suites were run; the full suite was not run (targeted gate for a lab-twin and lesson-text delta)")
row("GATE-10", "2.1-citations", "tools/verify_refs.py --offline", "PASS", "offline integrity: 560 entries, 0 problems, exit 0 (" + S + "/verify_refs.log)")
row("GATE-11", "2.8-data", "tools/fetch_data.py --check", "PASS", "fetch_data: 3 datasets, 0 problems, exit 0 (" + S + "/fetch_data.log)")
row("GATE-12", "2.6-projects", "tools/check_projects.py --all", "PASS", "check_projects M3: PASS, exit 0 (" + S + "/check_projects.log)")

# twins
row("TWIN-01", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py", "PASS", "python -I -W error on each twin: exit 0, empty stderr (" + S + "/twin_lab-M3-L0{7,8,9}-1.out). Changed twins L07 and L09 re-run; L08 twin byte-identical")
row("TWIN-02", "2.5-labs", "course/modules/M/M3/L07.html:126-200, L08.html, L09.html:194-345", "PASS", "twin_page_check.py: for L07, L08, L09 the data-run code equals the twin byte-for-byte after html.unescape, and the expected block equals the twin's stdout (" + S + "/twin_page_check.log)")

# L07 math and numbers
row("MATH-L07-01", "2.4-math", "course/modules/M/M3/L07.html:63-96", "PASS", RV + "Theorem 1.2 (a)-(c), Theorem 1.3 and Remark 1.4 proofs re-derived line by line. (a) G V Lambda^-1 V^T = V V^T = I checked; (b) A^T(y-p)=0 checked; (c) P^2 = P checked. Hypotheses carried by 'Assuming F1 to F4' at lines 65, 85, 95")
row("MATH-L07-02", "2.4-math", "course/modules/M/M3/L07.html:107-121, 322-331", "PASS", RV + "Theorem 2.2 (a)-(c) and proof re-read; uniqueness via Theorem 1.3 and invertibility of G are valid. Hypothesis line 109 carries F1-F4; R2 (line 322) and R3 (line 329) proofs re-derived (Q^2 = Q, A^T Q y = 0)")
row("MATH-L07-03", "2.4-math", "course/modules/M/M3/L07.html:232-310, 313-319", "PASS", RV + "M1 (P=(1/2)[[1,1],[1,1]], p=(1,1), residual (1,-1)), M2 (A^T A=[[3,3],[3,5]], A^T y=(5,6), beta=(7/6,1/2), fitted 7/6,5/3,13/6, residuals -1/6,1/3,-1/6), M3 (P=diag(1,0), p=(3,0), 25=9+16), P1-P3, E1-E3 and R1 re-derived; numbers from " + S + "/nums_L07_r16.log: M1 Py=(1,1), M2 beta=(1.16666667,0.5), M3 Py=(3,0)")
row("NUM-L07-01", "2.2-numbers", "course/modules/M/M3/L07.html:191-200; tests/labs/M3/lab-M3-L07-1.py", "PASS", RV + "Printed coefficients 1.3325 0.8488 -0.4120 and residual norm 0.8951 recomputed unrounded: beta=(1.33251885, 0.84881149, -0.41196372), ||r||=0.8951275537738198 (" + S + "/nums_L07_r16.log). Rank 2 of 3 recomputed")
row("NUM-L07-02", "2.2-numbers", "course/modules/M/M3/L07.html:299", "PASS", RV + "E2 claim A^T y approx (18.38, 3.10, -17.60): recomputed (18.3797, 3.0959, -17.6035) (" + S + "/nums_L07_r16.log)")
row("NUM-L07-03", "2.2-numbers", "course/modules/M/M3/L07.html:305-306; tests/labs/M3/lab-M3-L07-1.py", "PASS", RV + "E3: first column of A is ones so fitted value at zero regressors is beta_0 = 1.3325 (recomputed 1.33251885); generator intercept 1.5 (line 155 of the twin)")

# L08 carried
row("MATH-L08-01", "2.4-math", "course/modules/M/M3/L08.html:56-133", "PASS", "Carried from round 15 (L08.html byte-identical since 448548f): Propositions 1.1, 1.2, Theorem 1.4, Theorem 2.1, Corollary 2.2, Proposition 2.3 proofs")
row("MATH-L08-02", "2.4-math", "course/modules/M/M3/L08.html:323-416", "PASS", "Carried from round 15 (L08.html byte-identical since 448548f): worked solutions and Remark 2.4 cross-checks")
row("NUM-L08-01", "2.2-numbers", "course/modules/M/M3/L08.html:270-285, 377", "PASS", "Carried from round 15 (L08.html byte-identical; L08 twin output re-run this round and equals the page expected block by twin_page_check.log): printed values match")
row("NUM-L08-02", "2.2-numbers", "course/modules/M/M3/L08.html:277-280, 284", "PASS", "Carried from round 15 (L08.html byte-identical since 448548f). Shares 75.9 18.1 5.2 match the L08 twin output (" + S + "/twin_lab-M3-L08-1.out)")
row("NUM-L08-03", "2.2-numbers", "course/modules/M/M3/L08.html:389-391", "PASS", "Carried from round 15 (L08.html byte-identical since 448548f)")

# L09 math and numbers
row("MATH-L09-01", "2.4-math", "course/modules/M/M3/L09.html:73-181", "PASS", RV + "Lemma 1.3 (tr(XY)=tr(YX) argument), Prop 3.2(a)(b), Prop 3.3(a)(b), Prop 3.4, Prop 3.5 (x=e_i+t e_j, delta=|b_ij|/(1+b_jj)), Example 3.6 (eigenvalues 2.2, -0.2; A_0 = [[1.1,1.1],[1.1,1.1]]; R=[[1,1],[1,1]]; 0.04 and 0.08) re-derived. Lines 73-181 of L09 are byte-identical to 448548f")
row("NUM-L09-01", "2.2-numbers", "course/modules/M/M3/L09.html:52, 98, 346", "PASS", RV + "C0 witness -2.4, eigenvalues -0.8, 1.9, 1.9, squared distance 0.64 = sum of squared negative eigenvalues, R entries 0.5/-0.5 re-derived against " + S + "/twin_lab-M3-L09-1.out")
row("NUM-L09-02", "2.2-numbers", "course/modules/M/M3/L09.html:333-345", "PASS", RV + "Expected block (lines 333-345) equals twin output line for line (twin_page_check.log); 40 matrices, 23 non-PSD, 23 of 23 passing is_correlation, 23 of 23 strictly closer, first matrix index 0 with 0.175527 and 0.163280 all reproduced by running the twin")
row("NUM-L09-03", "2.2-numbers", "course/modules/M/M3/L09.html:441-444 (E2), 563-566 (quiz)", "PASS", RV + "C0-R off-diagonal differences 0.4, 0.4, -0.4; squared norm 6*0.16 = 0.96; sqrt(0.96) = 0.9798 (0.97979...) recomputed")
row("NUM-L09-04", "2.2-numbers", "course/modules/M/M3/L09.html:339-341 (R entries), 346", "PASS", RV + "R entries printed 1.0000, 0.5000, -0.5000 match the output of the twin (" + S + "/twin_lab-M3-L09-1.out)")
row("NUM-L09-05", "2.2-numbers", "course/modules/M/M3/L09.html:180", "PASS", RV + "Example 3.6: ||A-A_0||_F^2 = 0.04 and ||A-R||_F^2 = 0.08 re-derived by hand (A-A_0 = [[-0.1,0.1],[0.1,-0.1]], A-R = [[0,0.2],[0.2,0]])")
row("NUM-L09-06", "2.2-numbers", "course/modules/M/M3/L09.html:387-449, 491-497", "PASS", RV + "M1 eigenvalues 1.6, 0.4; M2 squared norm 4.88 = 4.84+0.04; M3 B eigenvalues (13 +- sqrt 41)/2 positive, C12=1/3; E3 0.5 from eigenvalues 2, 0.5, -0.5; R2 eigenvalues {1,4} vs {1,1}: all re-derived")

# notation, structure, data, sim, dag, crossref, hours, prose, grades
row("NOTATION-01", "2.9-notation", "notation/notation.json; course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", RV + "Registry symbols checked: T (number of observations) used in L08 as T = 750 days (consistent); R^\\ast, \\Phi, \\gamma_3, \\gamma_4, R_f, \\mathbb{Q} not used in L07-L09 (grep). L09 uses R for the rescaled matrix and C^\\ast for the nearest correlation matrix: no registry collision")
row("NOTATION-02", "2.9-notation", "course/modules/M/M3/L07.html, L09.html", "PASS", RV + "Symbol reuse within the slice: W is the column space (L07) and the alternating-projection output (L09), in different lessons, each defined where used; no symbol defined twice within a page")
row("STRUCT-L07-01", "2.9-structure", "course/modules/M/M3/L07.html", "PASS", RV + "Read in full: why-it-matters, s1 to s8 in order, canon-breaks, misconceptions, problem tiers mechanics/proof/empirical/research, key results, quiz (9 items), references, complete button, nav")
row("STRUCT-L08-01", "2.9-structure", "course/modules/M/M3/L08.html", "PASS", "Carried from round 15 (L08.html byte-identical since 448548f)")
row("STRUCT-L09-01", "2.9-structure", "course/modules/M/M3/L09.html", "PASS", RV + "Read in full: why-it-matters, s1 to s10 in order, canon-breaks, misconceptions, problem tiers, key results, quiz (11 items), references, nav")
row("DATA-L08-01", "2.8-data", "course/modules/M/M3/L08.html:291", "PASS", "Carried from round 15 (L08.html byte-identical since 448548f)")
row("SIM-LABEL-01", "2.8-data", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py; L07.html:128, L09.html:193-196", "PASS", RV + "Each of the three labs states SIMULATED in its docstring; the L07 and L09 pages show SIMULATED in the lab prose")
row("DAG-01", "2.9-dag", "tools/check_dag.py; L07 meta-row line 38-39; L09 meta-row line 38-39", "PASS", "check_dag M3: PASS (" + S + "/check_dag.log). Links used in L09 (L03 eigendecomposition, L04 spectral theorem, L05 positive-semidefinite) resolve to dfn anchors L03.html:109, L04.html:130 and L05.html:72 (verified by grep)")
row("CROSSREF-01", "2.9-prose", "course/modules/M/M3/L07.html:75, 207, 317; L09.html:56, 387, 112", "PASS", RV + "Cross-citations checked against the cited lessons: Theorem 3.7 of Lesson 1 (L01.html:161, spanning list bound used in R1); Fact 1.2 of Lesson 6 (L06.html:64, VV^T=I); F1-F4 of Lesson 4 (L04.html:56-62); spectral theorem Theorem 2.3 (L04.html:130); Lemma 1.3 of Lesson 4 (L04.html:78); Lesson 5 Theorem 2.1 (L05.html:108, PSD iff eigenvalues nonnegative, used in L09 M1)")
row("HOURS-01", "2.9-hours", "course/modules/M/M3/L07.html:2,35; L08.html:2,35; L09.html:2,35; index.html:154-156", "PASS", "Carried from round 15: data-hours and eyebrow lines are unchanged in this delta (hunks at L07 128, 216-223 and L09 203-208, 320-345 do not touch lines 2 or 35)")
row("PROSE-01", "2.2-numbers", "course/modules/M/M3/L07.html:125-200; L08.html:146-284; L09.html:193-342", "PASS", RV + "Every prose number in the changed hunks recomputed (L07: 0.8951, 1.3325, 0.8488, -0.4120, 0.8951, 18.38/3.10/-17.60; L09: 23, 40, 17, 0.6400000000, 0.175527, 0.163280, 0.9798). L08 prose carried from round 15")
row("GRADE-01", "2.3-grades", "course/modules/M/M3/L07.html:342-346; L08.html:428-434; L09.html:484-497; cards.json", "PASS", RV + "L07 key results: T rows marked 'Assuming F1 to F4'; C row is Lab 1 output. L09 key results: T rows (Props 3.2, 3.3, 3.4, 3.5, Example 3.6 by hand) and C rows (23 of 40 seeded; 0.175527 one instance). Grades match BLUEPRINT evidence grades as applied in the lessons")

# assumptions
row("ASSUME-01", "2.4-math", "course/modules/M/M3/L07.html:209, 292, 299; course/modules/M/M3/L08.html:290", "PASS", RV + "Round-14 sites now carry the marker: L07:209 'Assuming F1 to F4 of Lesson 4, Theorem 2.2(c) holds'; L07:292 'Assuming F1 to F4 ... by Theorem 2.2(c)'; L07:299 'assuming F1 to F4 ... by Theorem 2.2'; L08:290 unchanged since 448548f")
row("ASSUME-02", "2.4-math", "course/modules/M/M3/L08.html:140-141; course/modules/M/M3/L09.html:98, 116, 123, 139, 185, 187, 364, 417, 451, 460", "PASS", RV + "Each F1-F4 use in L09 carries the marker (grep 'Assuming F1' L09.html returns these lines). L08 lines carried from round 15")
row("ASSUME-03", "2.4-math", "course/modules/M/M3/L08.html:357, 414-416", "PASS", "Carried from round 15 (L08.html byte-identical since 448548f)")
row("ASSUME-04", "2.4-math", "course/modules/M/M3/L07.html:265, 272 (P1, P2), 317 (R1 solution); course/modules/M/M3/L09.html:449 (E3), 460 (R1)", "PASS", RV + "R1 and E3 markers present (L09:449, 460); L07 P1 (265), P2 (272) and R1 solution (317) carry 'Assuming F1 to F4'")
row("ASSUME-05", "2.4-math", "course/modules/M/M3/L07.html:218-219", "PASS", RV + "Previous FAIL resolved. L07:219 now reads 'Assuming F1 to F4 of Lesson 4, the residual is orthogonal to the columns of A, not zero', so the orthogonality claim carries its hypothesis (previously unmarked at line 218)")
row("ASSUME-06", "2.4-math", "course/modules/M/M3/L07.html:201", "FAIL", "Interpretation paragraph of Lab 1 (line 201), unchanged since 448548f and not previously flagged: 'The lab checks a finite example; the proofs above cover every full-column-rank design.' The proofs above (Theorem 1.2(a) via the spectral theorem, Theorem 2.2) are stated under 'Assuming F1 to F4 of Lesson 4' (lines 65, 109), so the sentence states a scope claim ('every') without the hypothesis. Verified by reading the proof of Theorem 1.2(a) at line 75, which cites the spectral theorem (Lesson 4).", "In course/modules/M/M3/L07.html line 201 change 'the proofs above cover every full-column-rank design' to 'assuming F1 to F4 of Lesson 4, the proofs above cover every full-column-rank design'. The sentence is page prose only; the twin is unaffected.")

# cards
row("CARD-HYP-01", "2.7-cards", "course/modules/M/M3/cards.json ids M3-c117 to c123, c134 to c137, c143 to c145, c153 to c157, c161, c165, c168", "PASS", "Carried from round 15 (ids unchanged; only c126 and c127 changed in this delta). Card-level grep for 'Assuming F1' confirms markers on these ids")
row("CARD-HYP-02", "2.7-cards", "course/modules/M/M3/cards.json ids M3-c142, M3-c153, M3-c158", "PASS", "Carried from round 15 (ids unchanged; M3-c153 and M3-c142 back text starts with 'Assuming F1 to F4 of Lesson 4')")
row("CARD-C183", "2.7-cards", "course/modules/M/M3/cards.json id M3-c183", "PASS", "Carried from round 15 (id unchanged)")
row("CARD-C161", "2.7-cards", "course/modules/M/M3/cards.json id M3-c161", "PASS", "Carried from round 15 (id unchanged)")
row("CARD-C130", "2.7-cards", "course/modules/M/M3/cards.json id M3-c130", "PASS", "Carried from round 15 (id unchanged)")
row("CARD-C138", "2.7-cards", "course/modules/M/M3/cards.json id M3-c138; course/modules/M/M3/L08.html:131-133", "PASS", "Carried from round 15 (id unchanged; L08 byte-identical)")
row("CARD-OK-01", "2.7-cards", "course/modules/M/M3/cards.json (L07, L08, L09 cards)", "PASS", RV + "cards_check_r16.py: 186 cards, no duplicate ids, no duplicate fronts; every L07-L09 card has its lesson field; decimals in L07-L09 card backs appear in their lesson, including 0.8951 in c126 and c127 (" + S + "/cards_check_r16.log)")
row("CARD-HYP-03", "2.7-cards", "course/modules/M/M3/cards.json id M3-c127 (back)", "PASS", RV + "Previous FAIL resolved. c127 back: 'False. Assuming F1 to F4 of Lesson 4, the residual is orthogonal to the columns of A, not zero' and 'Assuming F1 to F4 ... Remark 1.4' (both marked). c126 (grade C) also marked")
row("CARD-DUP-01", "2.7-cards", "course/modules/M/M3/cards.json", "PASS", RV + "Full scan: 186 ids unique, 186 fronts unique (cards_check_r16.py)")

# claims
row("CLAIM-L07-01", "2.3-grades", "course/modules/M/M3/L07.html:219", "PASS", RV + "Claim 'the residual is orthogonal to the columns of A' is graded T in Theorem 2.2(c) and now carries 'Assuming F1 to F4'")
row("CLAIM-L07-02", "2.3-grades", "course/modules/M/M3/L07.html:65, 90, 316", "PASS", RV + "Theorem 1.2 projection claim: hypothesis line 65; proof line 75-80; R1 line 317 proof uses only the subspace property plus existence via Theorem 1.2 (statement at 65 carries F1-F4)")
row("CLAIM-L07-03", "2.3-grades", "course/modules/M/M3/L07.html:109, 112, 120", "PASS", RV + "Normal equations claim graded T in Theorem 2.2(b) (line 112), hypothesis at line 109")
row("REMARK-L08-01", "2.4-math", "course/modules/M/M3/L08.html:131-133", "PASS", "Carried from round 15 (L08.html byte-identical since 448548f)")
row("REMARK-L08-02", "2.4-math", "course/modules/M/M3/L08.html:131-133", "PASS", "Carried from round 15 (L08.html byte-identical since 448548f)")
row("REMARK-L08-03", "2.4-math", "course/modules/M/M3/L08.html:131-133", "PASS", "Carried from round 15 (L08.html byte-identical since 448548f)")
row("PROSE-02", "2.9-prose", "course/modules/M/M3/L07.html:131-135, 201, 207-209, 219, 223; course/modules/M/M3/L09.html:52, 98, 187, 193, 346, 352-353, 372, 496-497", "PASS", RV + "Prose about lab and theorems rechecked against twin code and output. Exceptions: L07:201 scope sentence, recorded as ASSUME-06. The L09 lab docstring phrase 'W is feasible for the instances counted' (twin lines 210-211) is defined by the is_correlation tolerance stated in the same docstring (line 206), so it is treated as PASS; the page states the tolerance at L09.html:187")
row("PROCESS-01", "2.9-prose", "course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", "Grep for banned filler and process words (TODO, TBD, lorem, for brevity, beyond the scope, obviously, clearly, it is well known, roughly, historically, we, our, round, verifier): no hits in learner text. Ellipses at L07:395,409 and L09:527,536 are quiz-stem completions, not omitted content")
row("REG-01", "2.9-registry", "notation/notation.json; course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", RV + "notation.json unchanged since 448548f; verify_refs --offline: 560 entries, 0 problems (" + S + "/verify_refs.log)")

frag = {
  "unit": "M3", "slice": "c", "round": 16,
  "verifier": "independent Haiku verifier, checkout verifyB16-M3-c",
  "pin": "5e88c5085716527995791d30120edf4facd3cf5a",
  "base": "448548f997b7957f7b1d418a28d47f50d4a80fa0",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyB16-M3-c",
  "scratch": "/Users/billyribeiro/.fanout/wt/verifyB16-M3-c/ledgers/M3/scripts/M3-c-r16",
  "verified_at": date.today().isoformat(),
  "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": "Delta 448548f..5e88c50 read hunk by hunk: L07.html 131 (lab prose), 218-223 (misconceptions), L09.html 203-208 (lab docstring), 320-345 (expected block), cards.json c126, c127, lab twins L07 and L09. Re-derived all L07 and L09 numbers and proofs (full read of L07.html and L09.html; L08 byte-identical and carried). No project grader in slice c, so no mutation run. Labs are demonstrations, so no lab mutation run. Not checked: full pytest suite (targeted lab and docs suites only, per the changed-only rule); L08 page not re-read (carried by byte identity); verify_refs --unit M3 (only --offline run); no live Crossref or published-source check (no citation in L07-L09 requires one beyond registry keys)."
  ,
  "summary": ""
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
frag["summary"] = f"M3-c round 16: {len(rows)} rows, {n_pass} PASS, {n_fail} FAIL (ASSUME-06: unmarked 'every full-column-rank design' scope sentence at L07.html:201). ASSUME-05 and CARD-HYP-03 from round 15 now PASS. All gates PASS fresh."
json.dump(frag, open(sys.argv[1], "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(rows), "pass", n_pass, "fail", n_fail, frag["verdict"])
