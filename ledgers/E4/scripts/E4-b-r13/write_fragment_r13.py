"""Round-13 fragment writer for E4 slice b. Carries every round-12 row id; re-verified rows get round-13 evidence."""
import datetime
import json

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE13-E4-b"
OUT = "/tmp/_E4b_r13_scratch.json"
r12 = json.load(open("/Users/billyribeiro/.fanout/frags/E-E4-b.round12.json", encoding="utf-8"))
old = {r["id"]: r for r in r12["rows"]}
O = "ledgers/E4/scripts/E4-b-r13/outputs"
S = "ledgers/E4/scripts/E4-b-r13"

CMD = {
    "E4b11-cmd-check_pages": ("PASS", f"Re-run on e919577: tools/check_pages.py --unit E4 -> '{{check_pages E4: PASS}}' ({O}/check_pages_E4.txt); --page L04, L05, L06 each PASS ({O}/check_pages_L04.txt, _L05.txt, _L06.txt)."),
    "E4b11-cmd-check_dag": ("PASS", f"Re-run: tools/check_dag.py --unit E4 -> 'check_dag E4: PASS' ({O}/check_dag_E4.txt); --all -> every unit PASS ({O}/check_dag_all.txt)."),
    "E4b11-cmd-check_projects": ("PASS", f"Re-run: tools/check_projects.py --unit E4 -> 'check_projects E4: PASS' ({O}/check_projects_E4.txt)."),
    "E4b11-cmd-run_labs": ("PASS", f"Re-run: tools/run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)' ({O}/run_labs_E4.txt); L04, L05, L06 twins included."),
    "E4b11-cmd-twins-isolated": ("PASS", f"Re-run: env -i PATH=/usr/bin:/bin python -I -W error tests/labs/E4/lab-E4-L0{{4,5,6}}-1.py: exit 0, stderr 0 bytes ({O}/twins_isolated_W_error.txt, _L05.txt, _L06.txt; exit codes in {O}/_exit_codes.txt)."),
    "E4b11-cmd-page-code-equals-twin": ("PASS", f"Round-13 script {S}/twin_page_check_r13.py ({O}/twin_page_check_r13.txt): page code == twin for L04, L05, L06 except the final newline, which the embed omits; {S}/outputs/twin_trailing_newline_r13.txt shows page code == twin.rstrip('\\n') for all three."),
    "E4b11-cmd-expected-equals-output": ("PASS", f"{S}/twin_page_check_r13.py: 'expected block == stdout: True' for L04 (17 lines), L05 (26 lines), L06 (19 lines) ({O}/twin_page_check_r13.txt)."),
    "E4b11-cmd-ruff": ("PASS", f"ruff check on the three twins and on the repo: 'All checks passed!' ({O}/ruff_twins.txt, {O}/ruff_repo.txt); ruff format --check: 3 twins and 559 files already formatted ({O}/ruff_format_twins.txt, {O}/ruff_format_repo.txt)."),
    "E4b11-cmd-mypy": ("PASS", f"mypy --no-incremental (repo): 'Success: no issues found in 385 source files' ({O}/mypy_full.txt)."),
    "E4b11-cmd-pytest-labs": ("PASS", f"pytest tests/test_labs.py tests/test_run_labs.py: 365 PASSED, 0 FAILED ({O}/pytest_labs.txt)."),
    "E4b11-cmd-pytest-page": ("PASS", f"pytest tests/test_page_checks.py tests/test_page_smoke.py: 49 PASSED, 0 FAILED ({O}/pytest_page.txt)."),
    "E4b11-cmd-page_smoke": ("PASS", f"tools/page_smoke.py --unit E4 --pages L04 L05 L06: 'page_smoke modules/E/E4/L04.html: PASS', L05 PASS, L06 PASS (lab times 0.0, 0.0, 0.1 s); 'page_smoke E4: PASS' ({O}/page_smoke_E4.txt)."),
    "E4b11-cmd-verify_refs-offline": ("PASS", f"tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' ({O}/verify_refs_offline.txt)."),
    "E4b11-cmd-verify_refs-live": ("PASS", f"tools/verify_refs.py --unit E4 (plain requests by the tool): 'live re-verification of E4: 3 of 560 entries, 0 problems' ({O}/verify_refs_unit_E4_live.txt)."),
    "E4b11-cmd-render-diff": ("PASS", f"tools/render_curriculum.py exit 0, then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json exit 0 with empty output ({O}/render_diff.txt, _exit_codes.txt). git status after the battery shows no tracked change."),
}

REVER = {
    "E4b11-muth-attribution": ("PASS", "Re-verified: course/modules/E/E4/L05.html:296 cites muth1961rational with data-locator=\"title\" and says the phrase 'rational expectations' appears in the title. references/references.json:17660 record: title 'Rational Expectations and the Theory of Price Movements', year 1961, status verified. The title claim holds. Live verify_refs --unit E4 gave 0 problems ({O}/verify_refs_unit_E4_live.txt). Body of the article not read (title-only use, per the page)."),
    "E4b11-no-B1-B3-attribution": ("PASS", f"Re-verified: regex \\bB[13]\\b over the visible text of L04, L05, L06 gives 0 hits ({O}/prose_scans_r13.txt, 'B1/B3 hits: 0' for each lesson); no card in the slice cites B1 or B3."),
    "E4b11-rederive-numbers": ("PASS", f"Re-derived in exact Fractions with {S}/rederive_r13.py ({O}/rederive_r13.txt): Example 6.9 kappa=2, sig_eta2=2, tau_eta=1/2, tau_bar=3/4, theta_s=3/7, theta_u=6/7, Var(p)=27/49, Cov=3/7, b=7/9, V_U=2/3; grid 16 zeros 16; residual at (1,0) for slope 1/2 = -9/85; M1-M3 (a=2) give kappa 4, sig_eta2 5, theta_s 3/8, theta_u 3/2, Var(p)=27/32, b=4/9, Var(v|p)=5/6, corr^2=1/6, x_I=7/4, x_U=1/4, clearing 1. Part E: (0.426617 - 3/7)/(0.006497/3) = -0.902 SE and -0.301 of tolerance; hypothetical E1: (0.80-7/9)/0.05 = 0.444. Random exact instances: {S}/random_identities_r13.py 300 of 300 pass the V_U, Lemma 6.3, Cor 6.8 and clearing identities ({O}/random_identities_r13.txt)."),
    "E4b11-structure-scan": ("PASS", f"check_pages PASS for L04, L05, L06 ({O}/check_pages_L04.txt etc.). Section order re-read: L04 sections 1-9 (canon-breaks, misconceptions, problem-set, key-results, quiz, references); L06 sections 1-9 in the same order. Hours: data-hours=8 on L04 and L06 (and L05); the hub index.html:139 says nine lessons of eight hours = 72, and data-hours-lessons=72 + data-hours-project=28 = 100 (index.html:29, 31)."),
    "E4b11-solutions-length": ("PASS", f"{S}/prose_scans_r13.py ({O}/prose_scans_r13.txt): 12 problems and 12 solutions in each of L04, L05, L06; the four tiers (mechanics, proof, empirical, research) are present in each; solution word counts min 13 / max 91 (L04), 33 / 99 (L05), 50 / 136 (L06). BUILDER_RULES sets no solution length limit."),
    "E4b11-dag-closure": ("PASS", f"check_dag --unit E4 and --all PASS (outputs above). The round-13 L06 hunk (L06.html:149-152) adds no data-concept link: L06 data-concept count is 15 at 5db69a9 and at e919577 (git show). Concept links in L04 (5), L05 (6), L06 (15) read in this round."),
    "E4b11-notation": ("PASS", f"{S}/prose_scans_r13.py: no math in L04, L05 or L06 uses a registered symbol with another meaning. notation/notation.json lists T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f and \\mathbb{{Q}}; none appears in the slice math. Every macro used is registered (\\E, \\Var, \\Cov, \\Corr, \\R, \\indic, \\Normal) or standard LaTeX. Plain Q in the Prop 6.7 proof (L06.html:196-208) is not \\mathbb{{Q}}; it is a local letter defined at L06.html:200 and redefined in the existence proof at L06.html:208, same expression at theta_s^*. V_U, b, omega, kappa, eta, mu, pi are local letters defined in their lessons."),
    "E4b11-define-before-use": ("PASS", "Round 13: V_U first occurs at L06.html:152, where it is defined by '=:' in the Lemma 6.4 statement, and then at 157 (proof), 162, 169, 193, 230, 616. b is defined at L06.html:150 before its first use at 152. omega first occurs at L06.html:132 inside the Lemma 6.3 statement and is defined by 'where' in the display at 136 (same statement; style only). The round-12 defect (E4b12-L06-VU-use-before-definition) is fixed at line 152 in e919577."),
    "E4b11-scope-words": ("PASS", f"{S}/prose_scans_r13.py: scope-word counts L04 61, L05 50, L06 48. L04 and L06 hits were read in context this round; each is a quantified statement under a proof or a stated hypothesis, or a sentence that says 'only the price'/'only noise' with its computation (L06.html:240, 480). L05 hits carried from round 12 (L05.html byte-identical since 5db69a9). The L06 hunk at 149-152 adds no scope word."),
    "E4b11-simulated-labels": ("PASS", "L06.html:240 (lab hypothesis: 'Part E is SIMULATED ... seed 6'), L06.html:255 (Part E docstring), L06.html:480 (interpretation: 'Part E is SIMULATED'), key-results L06.html:634 with grade C and 'SIMULATED: Lab 1, Part E, one seed'. Cards E4-c124 and E4-c125 carry grade C and basis 'SIMULATED'. Exact parts (A to D) are labelled exact and graded T or C finite check."),
    "E4b11-grades": ("PASS", "Independent re-grade of each claim span in L04, L05, L06 and key-results tables against BLUEPRINT §3 and the legend at L04.html:46 (C = single study or finite check). Results proved on the page are T; the L06 finite grid and the SIMULATED sample are C (L06.html:633-634). Card E4-c065 changed from T to C in this delta; see row E4b13-delta-c065-grade."),
    "E4b11-structure-order": ("PASS", "Re-read this round: L04.html sections 1-9 (lines 53-520), L05.html sections 1-10, L06.html sections 1-9 (lines 53-731). Each has why-it-matters, the lesson sections, the lab section, misconceptions, problem set (Mechanics, Proof, Empirical, Research), key results table, quiz, references, completion button and lesson nav. check_pages PASS."),
    "E4b11-lab-twin-structure": ("PASS", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py: module docstring, constants, functions, main() called at module end; the page section ids lab-E4-L04-1 (L04.html:122), lab-E4-L05-1 (L05.html:120), lab-E4-L06-1 (L06.html:238) match the twin names. Page code equals twin (outputs/twin_page_check_r13.txt)."),
    "E4b11-lab-l06-docstring": ("PASS", "tests/labs/E4/lab-E4-L06-1.py module docstring (lines 1-23 of the twin) against the code and output: Parts A-E as described; Part C grid of 16 points (GRID_S x GRID_U) with all residuals zero; Part D residual nonzero; Part E SIMULATED, seed 6, 20000 draws, tolerance three standard errors (ols and part_e); units paragraph consistent (theta_s dimensionless; kappa, theta_u price per asset squared). Printed values match rederive_r13.txt."),
    "E4b11-lab-l05-docstring": ("PASS", "tests/labs/E4/lab-E4-L05-1.py docstring: Parts A-F match the code; ratio -varsigma/beta at every step (Part B: -1/4); Part C ratio -1 and no convergence; Part D grows; Part E damped step weight beta/(beta+varsigma) = 4/5 reaches (4,-3/10); check_params raises ValueError for beta<=0 or varsigma<0. Output in twin_page_check_r13.txt and twins_isolated_L05.txt."),
    "E4b11-lab-l04-docstring": ("PASS", "tests/labs/E4/lab-E4-L04-1.py docstring: Parts A-E match the code and output; Parts B and E claims ('complete' for the four-security matrix; weighted sum equals the fourth row) match lines 'complete True' and 'equals_fourth_row True' in the output; no random draws, as stated."),
    "E4b11-L04-lemma21-assumptions": ("PASS", "L04.html:100-108: Assumption A0 (real entries) and Lemma 2.1 statement (row operations preserve row space; pivots count rank). Re-read this round; the statements agree with the proof."),
    "E4b11-L04-lemma21-proof": ("PASS", "L04.html:108: proof of Lemma 2.1 (independence of the nonzero echelon rows via the smallest index with c_i nonzero; pivot column argument). Re-read; each step checked."),
    "E4b11-L04-sec1-statements": ("PASS", "L04.html:62-96: Definitions 1.1 and 1.3, Lemma 1.2 (row space), Theorem 1.4 (rank criterion), Proposition 1.5 (augmented rank), Corollary 1.6 (J >= S). Proofs re-read; each step holds."),
    "E4b11-L04-examples": ("PASS", "L04.html:111-119: Example 2.2 (rank 2, incomplete; (1,2,3) = r1+r2; (0,0,1) not attainable) and Example 2.3 (rank 3, complete; r4 = e1+2e2+3e3). Recomputed by hand this round."),
    "E4b11-L04-lab-1": ("PASS", "L04.html:122-265: lab code (lines 125-246) equals tests/labs/E4/lab-E4-L04-1.py; expected block (247-263) equals run output; hypothesis paragraph (124) and interpretation (264) match the printed values."),
    "E4b11-L04-remarks": ("PASS", "L04.html:269-277: Remark 3.1 (A = I_S, complete) and Remark 3.2 (redundancy; kernel dimension J - rank(A)). Re-derived."),
    "E4b11-L04-canon-breaks": ("PASS", "L04.html:279-300: Proposition 4.1 (proper subspace under infinitely many states; J+1 independent indicators) and Proposition 4.2 (nonnegative holdings give a convex cone; A=I_2 counterexample). Both proofs re-read."),
    "E4b11-L04-misconceptions": ("PASS", "L04.html:302-321: four misconceptions; each numerical claim (Example 2.3 rank 3; rows (1,1,1),(1,1,1),(0,1,2) rank 2; two portfolios (1,2,3,0) and (0,0,0,1); price-free rank) checked."),
    "E4b11-L04-problems": ("PASS", "L04.html:324-427: M1 (rank 1), M2 (attainability; (1,1,2) with zeta=(1,1); (0,0,1) not attainable), M3 (rank 2, r3=r1+r2, r4=2r1+r2), P1-P3, E1 (augmented rank 3; equations), E2 ((1-t,2-2t,3-3t,t) family), E3 (rank 2), R1-R3 (R3 holdings (xi1+t, xi2+t, t)). Re-derived each."),
    "E4b11-L04-key-results": ("PASS", "L04.html:440 (row 7): 'With infinitely many states, no finite set of securities is complete', source 'Proposition 4.1, under A2 to A4'. Prop 4.1 is stated under A2 to A4 at L04.html:289. Matches (round-11 FAIL fixed)."),
    "E4b11-L04-quiz": ("PASS", "L04.html:446-514: eight items (q1 rank criterion; q2 five; numeric 2; q4 family (1-t,2-2t,3-3t,t); q5 rank test; numeric 1; q7 incomplete; q8 no). Each correct option and explanation checked."),
    "E4b11-L04-why-it-matters": ("PASS", "L04.html:51: 96 words (prose_scans_r13.txt), within the 120-word limit. No banned phrase."),
    "E4b11-L04-references": ("PASS", "L04.html:516-520: 'This lesson cites no source' and an empty data-references list; no data-cite in L04."),
    "E4b11-L05-why-it-matters": ("PASS", "L05.html:51: 120 words, within the limit. Claim 'converges from every start only when varsigma < beta' matches Proposition 3.2 (sufficiency and the failure for varsigma >= beta)."),
    "E4b11-L05-model": ("PASS", "L05.html:55-74: A1-A3, Definition 1.1 (demand alpha - beta p + u; supply varsigma m(z) + delta z + upsilon; clearing price p_m), Definition 1.2. Re-derived p_m."),
    "E4b11-L05-lemma21-prop22-cor23": ("PASS", "L05.html:78-98: Lemma 2.1 (conditional mean and variance); Proposition 2.2 (fixed point c0* = alpha/(beta+varsigma), c1* = -delta/(beta+varsigma)); Corollary 2.3 (error variance and unconditional variance). Re-derived; proofs complete."),
    "E4b11-L05-lemma31-proof": ("PASS", "L05.html:102-106: Lemma 3.1 proof; both components give e_{k+1} = -(varsigma/beta) e_k. Re-derived."),
    "E4b11-L05-lemma31-hypothesis": ("PASS", "L05.html:103-104: Lemma 3.1 hypothesis 'Under A1 (so that beta > 0)'. Only A1 is used in the proof."),
    "E4b11-L05-prop32-33": ("PASS", "L05.html:108-118: Proposition 3.2 (convergence iff varsigma < beta, with failure for varsigma >= beta) and Proposition 3.3 (damped step weight beta/(beta+varsigma) with error factor 1 - nu(1+varsigma/beta) = 0). Re-derived."),
    "E4b11-L05-lab-1": ("PASS", "L05.html:120-282: lab code (lines 123-254) equals tests/labs/E4/lab-E4-L05-1.py (check above); expected block (255-280) equals the twin's output (26 lines); c0 paths and ratios printed match the hand computations in the card checks."),
    "E4b11-L05-remark-canon-muth": ("PASS", "L05.html:287 (Remark 4.1: the search is restricted to affine forecasts) and L05.html:292-296 (canon breaks; Muth title-only use). Re-read this round."),
    "E4b11-L05-misconceptions": ("PASS", "L05.html:299-315: three misconceptions; Lab 1 Part C has varsigma = beta with fixed point 5/2 and alternating iterates; base c1* = -3/10. Re-read this round."),
    "E4b11-L06-why-it-matters": ("PASS", "L06.html:51: 117 words, within the limit; the section pointer (Definitions 6.1 and 6.2, Assumptions A1 to A4 and G) matches the page."),
    "E4b11-L06-model": ("PASS", "L06.html:56-92: Definition 6.1, A1-A4, G. Re-read this round; A4 paragraph (L06.html:86) argument checked (linear residual vanishes only on a line of probability zero)."),
    "E4b11-L06-lemma62-proof": ("PASS", "L06.html:106-126: Lemma 6.2 proof (MGF of a normal; completing the square checked; x* = (m-p)/(aV) checked)."),
    "E4b11-L06-lemma62-hypotheses": ("PASS", "L06.html:98-104: Lemma 6.2 statement ('Assume A3'); hypotheses (normal with V > 0) used in the proof."),
    "E4b11-L06-lemma63-proof": ("PASS", "L06.html:129-144: Lemma 6.3 statement and proof. Re-derived: Cov(e,s)=0, Cov(e,u)=0, Var(e)=sigma_v^2(1-omega)=V_I, 1/V_I = tau_v+tau_eps, omega/V_I = tau_eps (checked in random_identities_r13.py)."),
    "E4b11-L06-lemma64": ("PASS", "L06.html:146-158 (changed hunk at 149-152 re-read): the statement now defines b = Cov(v,p)/Var(p) and V_U := sigma_v^2 - b Cov(v,p) before the proof uses V_U at 157; the proof (Cov(e,p)=0, E[v|p]=bp, Var(v|p)=sigma_v^2-b Cov(v,p), V_U = sigma_v^2(theta_s^2 sigma_eps^2 + theta_u^2 sigma_u^2)/Var(p) > 0) re-derived (random_identities_r13.py: V_U formula holds for 300 random instances)."),
    "E4b11-L06-remark-65-610": ("PASS", "L06.html:160-163 (Remark 6.5: x_U = (bp-p)/(aV_U), x_I = (omega s - p)/(aV_I)) and 233-236 (Remark 6.10: Y = s - kappa u = v + eta, sigma_eta^2 >= sigma_eps^2). Re-derived."),
    "E4b11-L06-prop67": ("PASS", "L06.html:172-209: Proposition 6.7 statement, uniqueness proof Steps 1-4 and existence proof. Re-derived each step: Step 1 (theta_s = 0 contradicts A4 at (s,0)); Step 2 (Y = p/theta_s, V_U = 1/P_U'); Step 3 (Q theta_s = lambda tau_eps, Q theta_u = a); Step 4 (kappa, tau_bar, theta_s*). Existence check (c.f. rederive_r13.py, random_identities_r13.py)."),
    "E4b11-L06-cor68-slope-step": ("PASS", "L06.html:211-226: Corollary 6.8 (E[v|p] = tau_eta p/(theta_s*(tau_v+tau_eta)), Var(v|p) = 1/(tau_v+tau_eta)); proof uses the Step 2 formulas. Verified numerically (random_identities_r13.py)."),
    "E4b11-L06-example69": ("PASS", "L06.html:228-231: Example 6.9. Every value re-derived (rederive_r13.txt): kappa 2, sigma_eta^2 2, tau_eta 1/2, tau_bar 3/4, theta_s 3/7, theta_u 6/7, b 7/9, V_U 2/3, x_I 1/7, x_U -1/7; the lab prints kappa, sig_eta2, tau_eta, tau_bar, theta_s, theta_u, slope 7/9, posterior variance 2/3, informed demand 1/7; its Part A header prints the variances sig_v2 1 and sig_e2 1, and no tau_v line, as the example's 'does not print' sentence says."),
    "E4b11-L06-lab-1": ("PASS", "L06.html:238-481: hypothesis (240), code (241-460) equal to tests/labs/E4/lab-E4-L06-1.py (outputs/twin_page_check_r13.txt), expected block (461-479) equal to the twin's output, and interpretation (480) matches the printed values (Part B: Var(s)=2, Var(p)=27/49, Cov=3/7; slope 7/9; posterior 2/3; Part C 16/16; Part D -9/85; Part E sample values)."),
    "E4b11-L06-canon-breaks": ("PASS", "L06.html:483-493: normality, CARA utility, exogenous lambda, independent supply (Cov(v,p) = theta_s sigma_v^2 - theta_u Cov(v,u), checked), price taking, one period. Claims are hedged ('need not', 'does not follow from this proof')."),
    "E4b11-L06-misconceptions": ("PASS", "L06.html:495-515: four misconceptions (sigma_eta^2 = 2 at base; noise trader is a primitive; slopes 3/7 and 7/9; posterior variance 2/3 < 1). Numbers checked."),
    "E4b11-L06-R1-corr-identity": ("PASS", "L06.html:598-602: R1 (lambda -> 0: kappa to infinity, tau_eta to 0, theta_s* to 0, Corr(v,p)^2 = sigma_v^2/(sigma_v^2+sigma_eta^2) to 0). Re-derived; lambda = 1/10 gives 1/27 = sigma_v^2/(sigma_v^2+sigma_eta^2) (rederive_r13.txt)."),
    "E4b11-L06-problems": ("PASS", "L06.html:521-594: M1-M3, P1-P3, E1-E3, R1-R3 re-derived (M1 kappa 4, sigma_eta^2 5, tau_eta 1/5, tau_bar 3/5, theta_s 3/8, theta_u 3/2; M2 Var(p)=27/32, b=4/9, Var(v|p)=5/6, corr^2=1/6; M3 p=-3/4, x_I=7/4, x_U=1/4, clearing 1; E2 -0.90 SE; E1 0.44 SE; R2 monotone (checked numerically, [0.6, 0.667, 0.75, 0.833])). P2 uses A4 at (s,0) and (s+1,0) correctly."),
    "E4b11-L06-key-results-quiz": ("PASS", "L06.html:622-725: key-results table rows (T for Lemma 6.3, Lemma 6.4, Prop 6.7, Cor 6.8, base values reproduced by Lab 1 Parts A and B; C for the grid and SIMULATED rows). Quiz items q1-q12 (numeric answers 0.4286, 4, 2, 0.5, 0.1429, 0.7778, 0.6667; MC answers checked). Re-read this round."),
    "E4b11-L06-references": ("PASS", "L06.html:727-731: 'cites no source'; the Gaussian fact G is used without proof and is labelled as such (L06.html:91)."),
    "E4b11-L06-part-d-alt": ("PASS", "L06.html:474-475 and the twin Part D: alternative slope 1/2 at (1,0) gives -9/85 (rederive_r13.txt; twins_isolated_L06.txt). Hypothesis paragraph (240) and interpretation (480) state the same value."),
    "E4b11-L06-part-e-replica": ("PASS", "L06.html:478-479 and 480: Part E replica values 0.426617 vs 3/7 (tolerance 0.006497) and 0.761928 vs 7/9 (tolerance 0.023538) match twins_isolated_L06.txt, and both are labelled SIMULATED. The label says one seed and no data."),
    "E4b11-cards-L04": ("PASS", f"Re-read this round: all 33 L04 cards in course/modules/E/E4/cards.json (E4-c053 to c073, c215, c217, c218, c226, c227, c228, c234 to c236, c239, c240, c249). Each front and back checked against L04 text and the lab output. Only E4-c065 changed in this delta (see E4b13-delta-c065-grade)."),
    "E4b11-cards-L05": ("PASS", f"Re-read this round: all 33 L05 cards (E4-c074 to c099, c219, c229, c241 to c243, c251, c252). Each checked against L05.html:58-117 (A1-A3, Def 1.1-1.2, Lemma 2.1, Prop 2.2, Cor 2.3, Lemma 3.1, Prop 3.2, Prop 3.3), the lab output (ratios -1/4, -1, -3/2; paths 0,5,15/4,65/16; 0,5,0,5; 0,5,-5/2,35/4; damped step (4,-3/10)) and Remark 4.1. E4-c076 now reads 'affine forecasts', matching L05.html:59 (round-12 FAIL fixed). E4-c099 Muth title-only card matches L05.html:296 and the registry."),
    "E4b11-cards-L06": ("PASS", f"Re-read this round: all 36 L06 cards (E4-c100 to c129, c220, c230, c231, c244, c247, c250, c253). Values 3/7, 6/7, 7/9, 2/3, 1/7, -1/7, 2, 16 grid points, -9/85, 0.426617, 0.761928 match the lab output and rederive_r13.txt. E4-c106 front now reads 'market clearing at every pair (s, u)', matching L06.html:81 (round-12 FAIL fixed). E4-c118 basis and E4-c129 basis updated and checked. E4-c121 removed (Remark 6.10 still covered by c126 and c244); c254/c255 removed (their content is in c116/c117 and c119/c129)."),
    "E4b11-cards-numbers-in-lesson": ("PASS", f"{S}/cards_scan_r13.py ({O}/cards_scan_r13.txt): every number token in the front or back of the 102 slice cards appears in its own lesson text (including the lab output); 0 NUMBER NOT IN LESSON lines."),
    "E4b11-cards-duplicate-scan": ("PASS", f"{S}/cards_scan_r13.py: 250 cards, 250 unique ids, 0 duplicate fronts, 0 duplicate backs ({O}/cards_scan_r13.txt). Slice cards: L04 33, L05 33, L06 36 (102)."),
    "E4b11-cards-process-words": ("PASS", "Regex (agent|fragment|workflow|script|this slice|verifier|builder|ledger|round) over the 102 slice cards and over the visible text of L04, L05, L06: 0 hits (prose_scans_r13.txt)."),
    "E4b11-cards-c120-basis": ("PASS", "Re-read: E4-c120 back 'x_I = 1/7 (Lab 1, Part C)' with basis 'Example 6.9 (Lemma 6.2 and Lemma 6.3 formulas); Lab 1, Part C' names Lemmas 6.2 and 6.3 for the demand and omega/V_I, and does not use Lemma 6.4. E4-c220 (x_U = -1/7) basis names Lemma 6.4 and Remark 6.5, which it does use. Both objects unchanged in this delta."),
    "E4b12-card-c076": ("PASS", "course/modules/E/E4/cards.json (E4-c076) front now 'Assumption A2 (affine forecasts) of the L05 model'; L05.html:59 reads '<strong>A2 (affine forecasts).</strong>' (grep for 'linear forecast' in L05.html and cards.json: no hit). Round-12 FAIL fixed."),
    "E4b12-card-c106": ("PASS", "course/modules/E/E4/cards.json (E4-c106) front now 'Assumption A4 (market clearing at every pair (s, u))'; L06.html:81 reads the same title. Round-12 FAIL fixed."),
    "E4b12-L06-VU-use-before-definition": ("PASS", "L06.html:152 now defines V_U in the Lemma 6.4 statement ('... = sigma_v^2 - b Cov(v,p) =: V_U'); first occurrence of V_U in L06 is at character 14363, line 152 (prose_scans_r13.txt, 'first V_U at ... line 152'); the proof use at L06.html:157 is after it. Round-12 FAIL fixed."),
    "E4b12-cards-split-review": ("PASS", "cards.json pairs: E4-c081/c251 (E[p_m|z] vs conditional law), E4-c083/c252 (fixed point vs price), E4-c113/c253 (E[v|p] vs Var(v|p)). The pairs E4-c116/c254 and E4-c119/c255 are no longer pairs because c254 and c255 were removed in this delta; c116 (E[v|p] at equilibrium) and c119 (base slope) remain single-question cards, and their backs agree with L06.html:215 and 230. No duplicate front or back in cards_scan_r13.txt."),
    "E4b12-L06-research-R2-R3": ("PASS", "L06.html:606-616 re-read this round: R2 (Var(v|p) strictly increasing in sigma_u^2, via sigma_eta^2 increasing and kappa independent of sigma_u; monotone numeric check [0.6, 0.667, 0.75, 0.833]); R3 (names the G steps of Lemmas 6.3 and 6.4, the four facts of Prop 6.7 and the fifth fact of Lemma 6.2; no claim for other payoff laws). Both correct."),
}

CARRY_FILES = {
    "E4b11-L05-problems": "course/modules/E/E4/L05.html",
    "E4b11-L05-key-results-quiz": "course/modules/E/E4/L05.html",
    "E4b11-L05-references": "course/modules/E/E4/L05.html",
    "E4b11-L05-psi0-notation": "course/modules/E/E4/L05.html",
}

rows = []
for rid, r in old.items():
    base = {"id": rid, "check": r["check"], "location": r["location"]}
    if rid in CMD:
        st, ev = CMD[rid]
    elif rid in REVER:
        st, ev = REVER[rid]
    elif rid in CARRY_FILES:
        st = "PASS"
        ev = (f"Carried from round 12 ({CARRY_FILES[rid]} byte-identical since the previous pin 5db69a9): "
              f"{r['evidence']} Not re-read in full this round (L05 problem set, key results, quiz, references and line 402 not re-read).")
    else:
        raise SystemExit(f"unmapped round-12 row {rid}")
    base.update({"status": st, "evidence": ev})
    rows.append(base)

NEW = [
    {"id": "E4b13-delta-c065-grade", "check": "2.7-cards / 2.3-grades",
     "location": "course/modules/E/E4/cards.json (E4-c065, L04 card about the augmented rank in Lab 1 Part C)",
     "status": "PASS",
     "evidence": f"git diff 5db69a9..e919577: E4-c065 grade T -> C and basis 'L04 lab, Part C' -> 'Lab 1, Part C (exact Fraction elimination)'. Its values (2, 3, 3) match the Lab 1 Part C output ({O}/twins_isolated_W_error.txt: '(1,2,3) ... augmented_rank 2', '(0,0,1) ... 3', '(5,0,0) ... 3'). The page also proves (1,2,3) and (0,0,1) by hand (L04.html:113-114), so T with a by-hand basis would also be correct. C is the legend's grade for a finite check (L04.html:46) and the card names the lab, so the downgrade is conservative and accepted."},
    {"id": "E4b13-delta-removed-cards", "check": "2.7-cards",
     "location": "course/modules/E/E4/cards.json (E4-c121, E4-c254, E4-c255 removed)",
     "status": "PASS",
     "evidence": f"card_delta_r13.py ({O}/card_delta.txt) lists REMOVED E4-c121, E4-c254, E4-c255. grep over course/modules/E/E4/ and tests/ and tools/ finds no reference to these ids. Their content is covered by E4-c126 and E4-c244 (noise variance), E4-c116/c117 (uninformed projection and variance) and E4-c119/c129 (slope, posterior variance)."},
    {"id": "E4b13-delta-card-basis-edits", "check": "2.7-cards / 2.4-mathematics",
     "location": "course/modules/E/E4/cards.json (E4-c118 basis; E4-c129 basis)",
     "status": "PASS",
     "evidence": "card_delta_r13.py: E4-c118 basis now 'Example 6.9, derived by hand from Proposition 6.7' (values 3/7, 6/7, p, sigma_eta^2 = 2, tau_bar = 3/4 are derived at L06.html:230 and by rederive_r13.py); E4-c129 basis now 'Corollary 6.8; Example 6.9' (Var(v|p) = 2/3 at L06.html:230). Both bases name what the card uses."},
    {"id": "E4b13-delta-L06-hunk", "check": "2.4-mathematics / 2.9-prose",
     "location": "course/modules/E/E4/L06.html:149-152 (Lemma 6.4 statement; the only hunk in slice b since 5db69a9)",
     "status": "PASS",
     "evidence": "git diff 5db69a9..e919577 -- course/modules/E/E4/L06.html: one hunk, 2 lines (line 152): 'Var(v | p) = sigma_v^2 - b Cov(v, p) =: V_U'. The added definition is correct (Var(e) = sigma_v^2 - 2b Cov + b^2 Var(p) = sigma_v^2 - b Cov) and precedes every use of V_U."},
    {"id": "E4b13-twins-unchanged", "check": "2.5-labs",
     "location": "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py",
     "status": "PASS",
     "evidence": "git diff --quiet 5db69a9 e919577 -- each of the three twin files: identical (no change in this delta), so the round-12 lab results carry for the twins; they were re-run anyway (E4b11-cmd rows)."},
]
rows += NEW

pin = "e919577b (detached)"
frag = {
    "unit": "E4",
    "slice": "b",
    "round": 13,
    "verifier": "Haiku independent verifier, E4-b round 13 (did not build E4; no shared context with builders)",
    "pin": pin + " in /Users/billyribeiro/.fanout/wt/verifyE13-E4-b",
    "base": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0 (round-12 pin; round-12 fragment /Users/billyribeiro/.fanout/frags/E-E4-b.round12.json used as context only; its PASS rows carried only where the subject is byte-identical, otherwise re-verified; its FAIL rows E4b11-cards-L05, E4b11-cards-L06, E4b12-card-c076, E4b12-card-c106, E4b12-L06-VU-use-before-definition re-verified and now PASS)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE13-E4-b",
    "scratch": "ledgers/E4/scripts/E4-b-r13/ (run_commands_r13.sh, twin_page_check_r13.py, rederive_r13.py, random_identities_r13.py, cards_scan_r13.py, prose_scans_r13.py, card_delta_r13.py, write_fragment_r13.py; outputs/ holds every command output)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 5db69a9..e919577 for slice b: L06.html:149-152 (V_U definition); cards.json: E4-c065 (grade and basis), c076 and c106 (fronts), c118 and c129 (bases), c121, c254, c255 removed. L04.html, L05.html, the three twins, notation.json, references.json, index.html, tools/data_sources.yaml byte-identical in that range. Every changed hunk in the slice was read; every changed card was checked against its lesson text.",
        "Full read this round: L04.html (lines 1-531) and L06.html (lines 1-731). L05.html lines 50-330 read in full (model, lemmas, propositions, lab, remark, canon breaks, misconceptions); lines 420-430 and 496-510 read in part. The L05 problem set (lines 331-419), most of the L05 key results and quiz (431-495) and the page end were not re-read; carried from round 12 on byte-identity.",
        "Not a row: the L06 ordering of omega in Lemma 6.3 (used at line 132 inside the statement and defined by 'where' at 136) is style, not a defect.",
        "Not a row: plain Q in the Prop 6.7 proof (L06.html:196-208) is a local letter, not the registered \\mathbb{Q}; it is defined at L06.html:200 and redefined for theta_s* at 208 with the same expression.",
        "Not a row: the page code equals the twin except for the final newline (the embed omits it); see outputs/twin_trailing_newline_r13.txt.",
        "Not a row: lab naming differs across cards ('L04 lab, Part A' vs 'Lab 1, Part C'); both name the same L04 lab.",
        "Not a row: L06 lab docstring says 'The coefficient theta_s is dimensionless' and 'kappa and theta_u ... price per unit of the asset squared'; the unit algebra checks (p and s in price per asset, u in asset units).",
        "Mutants: none. Slice b is lesson text, cards and lab twins; per the ruling, mutation testing applies to project graders only (slice d). run_graders and mutate_graders were not run for slice b.",
        "Access: verify_refs --unit E4 used the tool's own requests (no bot check, login or paywall touched). The Muth (1961) article body was not read; the title is checked against the registry record and the live run.",
    ],
    "summary": "",
}
n = len(rows)
npass = sum(1 for r in rows if r["status"] == "PASS")
frag["summary"] = (f"PASS E4-b round 13 at e919577: rows={n} (pass={npass} fail={n-npass} unverifiable=0). "
                   "All command gates exit 0 on the pin. The five round-12 non-PASS rows are re-verified PASS. "
                   "Round-12 PASS rows are carried only where the subject is byte-identical, except the L06 and cards rows, which were re-verified this round.")
json.dump(frag, open(f"{ROOT}/ledgers/E4/E4-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", f"{ROOT}/ledgers/E4/E4-b.json", "rows", n, "pass", npass)
