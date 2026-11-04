"""Writes the round-6 E4-b fragment (ledgers/E4/E4-b.json) from the evidence recorded during this round.

Every evidence string cites a script or output kept in ledgers/E4/scripts/E4-b-r6/ or a file:line in the checkout.
Run from the repo root: .venv/bin/python ledgers/E4/scripts/E4-b-r6/write_fragment.py
"""

import json

P = "PASS"
F = "FAIL"
OUT = "ledgers/E4/scripts/E4-b-r6/outputs"
SC = "ledgers/E4/scripts/E4-b-r6"
ICK = f"{SC}/independent_checks.py"
EVO = f"{SC}/expected_vs_output.py"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)


CARRY_HUB = "Carried from round 5 (course/modules/E/E4/index.html byte-identical since the previous pin 7376a5e, checked by git diff --stat 7376a5e 4bd8cb9): "

# ---- commands, all re-run at 4bd8cb9 by run_gates.sh (outputs in OUT) ----
row("E4b-cmd-check_pages", "tools/check_pages.py --unit E4", "course/modules/E/E4/L04.html, L05.html, L06.html", P,
    f"run at 4bd8cb9: 'check_pages E4: PASS', exit 0 ({OUT}/check_pages_E4.txt; runner {SC}/run_gates.sh).")
row("E4b-cmd-check_dag", "tools/check_dag.py --unit E4", "E4 DAG: L04-L06 links and concept uses", P,
    f"'check_dag E4: PASS' exit 0 ({OUT}/check_dag_E4.txt). Unlinked uses re-read: vector-space, linear-map (M3), "
    "expectation, random-variable, normal-distribution, conditional-expectation-elementary, independence, "
    "multivariate-normal, least-squares-projection (M3/M4), expected-utility, crra-utility, competitive-equilibrium (E1/E3) "
    "all have owners in curriculum/curriculum.json 'concepts' inside the E4 closure; arrow-debreu-security links L01.html; "
    "E4-owned concepts link their defining lesson (L05.html#def-rational-expectations-equilibrium, L06 uses L05 anchor).")
row("E4b-cmd-check_projects", "tools/check_projects.py --unit E4", "E4 project (out of slice, unit gate)", P,
    f"'check_projects E4: PASS' exit 0 ({OUT}/check_projects_E4.txt). Out of slice.")
row("E4b-cmd-run_labs", "tools/run_labs.py --unit E4 (and --page L04, L05, L06)", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", P,
    f"'run_labs E4: PASS (12/12)'; per page 'run_labs E4: PASS (1/1)' for L04, L05, L06 ({OUT}/run_labs_E4.txt, run_labs_L04/L05/L06.txt); all exit 0.")
row("E4b-cmd-twins-isolated", "python -I -W error on each twin", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", P,
    f"exit 0 for each (twin_L04/L05/L06 outputs). {EVO} reports stderr_bytes=0 for each run.")
row("E4b-cmd-page-code-equals-twin", "page lab code byte-identical to twin", "L04.html lab block, L05.html lab block, L06.html lab block", P,
    f"{EVO} output: code_equals_twin=True for L04 (122 lines), L05 (132 lines), L06 (219 lines), after strip()/unescape of the page <pre> block.")
row("E4b-cmd-expected-equals-output", "expected block equals run stdout", "course/modules/E/E4/L04.html:242-258, L05.html:255-280, L06.html:460-478", P,
    f"{EVO}: expected_equals_output=True for L04, L05, L06.")
row("E4b-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on twins", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", P,
    f"ruff check: 'All checks passed!'; ruff format --check: '12 files already formatted'; mypy: 'Success: no issues found in 3 source files' ({OUT}/ruff_check.txt, ruff_format.txt, mypy_twins.txt).")
row("E4b-cmd-pytest-labs", "pytest -k E4 tests/test_labs.py tests/test_run_labs.py", "tests/test_labs.py, tests/test_run_labs.py", P,
    f"'13 passed, 352 deselected' ({OUT}/pytest_E4.txt).")
row("E4b-cmd-page_smoke", "tools/page_smoke.py --unit E4 --pages L04 L05 L06 (run alone)", "course/modules/E/E4/L04.html, L05.html, L06.html", P,
    f"'page_smoke modules/E/E4/L04.html: PASS', L05 PASS, L06 PASS, 'page_smoke E4: PASS' ({OUT}/page_smoke_E4.txt). Lab timings 0.1 s.")
row("E4b-cmd-verify_refs-live", "tools/verify_refs.py --unit E4 (live)", "references/references.json (E4 entries, incl. muth1961rational)", P,
    f"'live re-verification of E4: 3 of 560 entries, 0 problems', exit 0 ({OUT}/verify_refs_unit_E4.txt).")
row("E4b-cmd-verify_refs-offline", "tools/verify_refs.py --offline", "references/references.json", P,
    f"'offline integrity: 560 entries, 0 problems', exit 0 ({OUT}/verify_refs_offline.txt).")

# ---- labs ----
row("E4b-lab-L04-1", "lab twin L04 hypothesis and interpretation", "course/modules/E/E4/L04.html:119, 259; tests/labs/E4/lab-E4-L04-1.py", P,
    "Hypothesis (L04.html:119): two-security rank 2 below 3 states (incomplete), four-security rank 3 (complete), (1,2,3) attainable, (0,0,1) and (5,0,0) not, fourth row = 1,2,3 combination. Printed output (L04.html:243-258) matches; re-derived by hand (Examples 2.2, 2.3) and by "
    f"{ICK} (ranks, augmented ranks). Docstring inputs (twin lines 3-5) match the matrices in the code (twin lines 35-36).")
row("E4b-lab-L05-1", "lab twin L05 hypothesis, docstring and output", "course/modules/E/E4/L05.html:122, 125-137, 255-280; tests/labs/E4/lab-E4-L05-1.py:14-15", P,
    f"Hypothesis (L05.html:122): base c0*=4, c1*=-3/10, residual 0, ratio -1/4, ς=β ratio -1 with path 0,5, ς=3 ratio -3/2, damped weight 4/5 reaches c*. "
    f"Printed values match; recomputed in {ICK} (L05 rows). Docstring 136-137 ('each parameter set that Parts B to D iterate is checked by check_params') matches show() calling check_params (twin line 87) before iterate (twin line 89).")
row("E4b-lab-L06-1-outputs", "lab twin L06 printed output and prose", "course/modules/E/E4/L06.html:460-478, 479-485; tests/labs/E4/lab-E4-L06-1.py", P,
    f"Output block equals run stdout ({EVO}). Prose at L06.html:479 quotes Var(s)=2, Var(p)=27/49, Cov=3/7, slope 7/9, posterior 2/3, 16 grid points, residual-free, 1/7, -9/85, sample slopes 0.426617/0.761928 with tolerances 0.006497/0.023538: all match the printed lines; recomputed by {ICK}.")
row("E4b-lab-L06-1-units", "lab docstring units paragraph", "tests/labs/E4/lab-E4-L06-1.py:17-20", P,
    "Units: theta_s dimensionless (p and s both price per asset); kappa and theta_u price per unit of asset squared, consistent with kappa = a*sig_e2/lam, a in 1/price, u in asset units and x = (m-p)/(aV) in asset units (dimension bookkeeping by hand).")
row("E4b-lab-L06-1-residual-docstring", "lab residual() docstring vs code", "tests/labs/E4/lab-E4-L06-1.py:78-106", P,
    "Docstring (informed mean omega*s, Var(v|s,p)=V_I via Lemma 6.3, uninformed slope Cov/Var(p), residual variance Var(v)-slope*Cov) matches the code lines 96-106 one for one; Lemma 6.3 holds for any price coefficients as stated.")
row("E4b-lab-L06-1-hypothesis-xref", "lab hypothesis cross-reference", "course/modules/E/E4/L06.html:238-240", P,
    "Hypothesis cites Proposition 6.7 and Example 6.9 values (kappa=2, sig_eta^2=2, tau_eta=1/2, taubar=3/4, theta_s=3/7, theta_u=6/7); Part D alternative theta_s=1/2 gives residual -9/85 (checked exactly in " + ICK + "); Part E is SIMULATED, seed 6, 20 000 draws (twin lines 37-38).")

# ---- L04 ----
row("E4b-L04-math-sec1", "Definitions 1.1, 1.3; Lemma 1.2; Theorem 1.4; Proposition 1.5; Corollary 1.6", "course/modules/E/E4/L04.html:65-95", P,
    "Re-read every line; Lemma 1.2 linearity and row-space argument, Theorem 1.4 full-dimension argument, Prop 1.5 subspace-containment argument and Cor 1.6 span bound are each complete under A1 to A3. Assumptions A1-A3 stated before use (L04.html:56-60).")
row("E4b-L04-math-lemma21", "Lemma 2.1 (elimination counts rank)", "course/modules/E/E4/L04.html:101-104", P,
    "Row operations preserve row space; echelon pivots are linearly independent (proof L04.html:103 covers the independence by smallest index argument) and span, so count = rank.")
row("E4b-L04-math-examples", "Examples 2.2 and 2.3", "course/modules/E/E4/L04.html:107-115", P,
    f"Rank 2 with 2<3 (incomplete); (1,2,3)=r1+r2 attainable; (0,0,1) augmented rank 3 not attainable; rows e1,e2,e3,(1,2,3) rank 3 complete; re-derived in {ICK}.")
row("E4b-L04-math-remark31", "Remark 3.1 (one security per state)", "course/modules/E/E4/L04.html:265-268", P,
    "rank(I_S)=S, complete by Theorem 1.4; zeta = xi gives zeta^T I_S = xi (checked by hand).")
row("E4b-L04-math-remark32", "Remark 3.2 (redundancy and kernel)", "course/modules/E/E4/L04.html:270-272", P,
    f"Kernel of zeta -> zeta^T A from R^J to R^S has dimension J - rank(A) (rank-nullity); replicating set is zeta + kernel. Checked: 4 - rank(com)=1 in {ICK}; every attainable payoff has a translate of portfolios as stated.")
row("E4b-L04-math-sec4", "Proposition 4.1 (no finite market complete with infinitely many states)", "course/modules/E/E4/L04.html:277-288", P,
    "Proof: J+1 distinct states exist; indicator functions 1_{omega_i} are linearly independent (evaluate at omega_k); a subspace of dimension at most J cannot contain them or equal R^Omega. Complete.")
row("E4b5-L04-prop42-symbols", "Proposition 4.2 statement symbols (round-5 FAIL: undefined x, y)", "course/modules/E/E4/L04.html:291-292", P,
    "Re-verified at 4bd8cb9: the statement now introduces xi and eta as two elements of C(A) and uses a*xi + b*eta. The round-5 undefined x, y are gone. The proof linkage of zeta, phi to xi, eta is a separate defect: see E4b6-L04-prop42-proof-link.")
row("E4b6-L04-prop42-proof-link", "Proposition 4.2 proof: portfolios zeta, phi not linked to xi, eta", "course/modules/E/E4/L04.html:293 (Proof of Proposition 4.2)", F,
    "The statement (L04.html:292) takes xi and eta as two elements of C(A) = {zeta^T A : zeta >= 0}. The proof (L04.html:293) begins 'If zeta, phi >= 0 and a, b >= 0' and concludes a zeta^T A + b phi^T A = (a zeta + b phi)^T A, but never says xi = zeta^T A and eta = phi^T A. The portfolios zeta and phi are not introduced in relation to xi and eta, so the step from the proof to a*xi + b*eta in C(A) is not stated. The same undefined-symbol class was the round-5 FAIL.",
    "In the proof of Proposition 4.2 (L04.html:293), insert before 'If zeta, phi >= 0': 'Let zeta, phi >= 0 with xi = zeta^T A and eta = phi^T A.' Nothing else changes.")
row("E4b-L04-misconceptions", "L04 misconceptions 1 to 4", "course/modules/E/E4/L04.html:297-317", P,
    "Misconception 1 (Example 2.3 complete, rank 3); 2 (rows (1,1,1),(1,1,1),(0,1,2) have rank 2, Corollary 1.6 not converse); 3 (two portfolios (1,2,3,0), (0,0,0,1), Lab Part E); 4 (Definition 1.3 uses only A). Each re-derived.")
row("E4b-L04-problems", "L04 problem set M1-M3, P1-P3, E1-E3, R1-R3", "course/modules/E/E4/L04.html:319-421", P,
    f"M1 rank 1; M2 zeta=(1,1), (0,0,1) not attainable; M3 r3=r1+r2, r4=2r1+r2, rank 2; P1, P2, P3 steps valid; E1 (zeta1=5, zeta2=-5, 5-10 != 0); E2 family (1-t,2-2t,3-3t,t); E3 rank 2; R1 Cor 1.6; R2 I_S; R3 construction t=max(0,-x1,-x2) checked on a grid in {ICK}.")
row("E4b-L04-quiz-q4", "L04 quiz: replicating portfolios of (1,2,3)", "course/modules/E/E4/L04.html:467-475", P,
    "Correct option is the family (1-t, 2-2t, 3-3t, t); explanation (L04.html:474) matches Remark 3.2; wrong options checked.")
row("E4b-L04-quiz-rest", "L04 quiz items", "course/modules/E/E4/L04.html:441-508", P,
    "Answers correct: Theorem 1.4 rank condition; five securities needs J>=5 (Cor 1.6, Remark 3.1); rank of (1,1,1),(1,1,1),(0,1,2) is 2; Prop 1.5 criterion; rank of (1,2,0),(2,4,0) is 1; infinite states incomplete (Prop 4.1); (-1,0) not attainable under zeta>=0 (Prop 4.2).")
row("E4b-L04-why-empirical", "L04 'illustrative numbers' statements", "course/modules/E/E4/L04.html:51, 321; L04.html:259", P,
    "States that matrices are illustrative numbers and that the printed ranks say nothing about any market (L04.html:259). Consistent with the lab (twin line 3).")
row("E4b-grades-L04", "L04 grades (legend and key results)", "course/modules/E/E4/L04.html:42-49, 81-96, 427-436", P,
    "Results with a proof are T; finite hand examples graded T with the basis named (Example 2.2 by hand; Lab 1 Part A); no lab-only claim is graded T without a basis. Grade legend consistent.")
row("E4b-struct-L04", "L04 structure, order, footer", "course/modules/E/E4/L04.html:2, 34-524", P,
    "Header, meta line (8 study hours, L04 of 9), sections 1-9 in order, prev L03 / next L05 labels (L04.html:519-520), footer L04.html:524. check_pages PASS.")

# ---- L05 ----
row("E4b-L05-math-sec1-2", "Definitions 1.1, 1.2; Lemma 2.1; Proposition 2.2; Corollary 2.3", "course/modules/E/E4/L05.html:65-97", P,
    "Clearing price p_m = (alpha - varsigma m - delta z + u - upsilon)/beta re-derived; Lemma 2.1 mean and variance; Psi(c0,c1) and fixed point (alpha/(beta+varsigma), -delta/(beta+varsigma)) re-derived; Cor 2.3 variance of p = (c1*)^2 sig_z^2 + (sig_u^2+sig_upsilon^2)/beta^2 re-derived.")
row("E4b-L05-math-sec3", "Lemma 3.1; Proposition 3.2; Proposition 3.3", "course/modules/E/E4/L05.html:103-118", P,
    "Error recursion e_{k+1} = -(varsigma/beta) e_k re-derived; damped weight nu=beta/(beta+varsigma) gives factor 1-nu(1+varsigma/beta)=0 (checked: nu(1+varsigma/beta)=1).")
row("E4b-L05-prop32", "Proposition 3.2 statement and proof", "course/modules/E/E4/L05.html:109-111", P,
    "varsigma<beta: |varsigma/beta|<1 so error -> 0 from every start; varsigma=beta: absolute error constant; varsigma>beta: grows. Statement and proof agree.")
row("E4b-L05-sec5-wording", "L05 section 5 'Where the canon breaks'", "course/modules/E/E4/L05.html:292-296", P,
    "'converges ... only when varsigma<beta' is the necessity direction of Prop 3.2; 'the result is a property of this model, not of rational expectations in general' is a scope statement supported by A2 and Remark 4.1. No unwitnessed universal claim.")
row("E4b-L05-prop34-remark41", "Proposition 3.3 proof; Remark 4.1", "course/modules/E/E4/L05.html:115-118, 286-288", P,
    "Damped-step error factor derived (L05.html:117); Remark 4.1 correctly states Prop 2.2 gives exactly one affine REE, not that no non-affine REE exists.")
row("E4b-L05-notation-gamma", "notation: no registered or conflicting symbol in L05", "course/modules/E/E4/L05.html (all), notation/notation.json", P,
    "grep for gamma, Phi, Prob, indic, mathbb{Q}, R_f in L04-L06: 0 hits. notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (AP1/M4/S1); none is used in L05. Supply response is varsigma, demand slope beta, all defined in A1.")
row("E4b-L05-notation-s", "notation: local symbols q, z, s, c_k, e_k", "course/modules/E/E4/L05.html:66, 73, 104; course/modules/E/E4/L06.html:57", P,
    "L05 supply is q (L05.html:66), public signal z (A2/A3); s is the signal only in L06 (L06.html:57). Each local symbol is defined in its lesson before use (c_k and e_k at L05.html:104).")
row("E4b-L05-muth-markup", "Muth citation markup", "course/modules/E/E4/L05.html:296", P,
    "data-cite='muth1961rational' data-locator='title'; the registry record (references/references.json, key muth1961rational) has title 'Rational Expectations and the Theory of Price Movements', Econometrica 29(3), 1961, verified_by crossref; the phrase 'rational expectations' appears in the title.")
row("E4b-L05-math-muth-scope", "Muth scope sentence", "course/modules/E/E4/L05.html:295-296", P,
    "'The model here is a stated special case, and this lesson uses no result from that paper' is consistent with the lesson using only the title.")
row("E4b-L05-misconceptions", "L05 misconceptions 1 to 3", "course/modules/E/E4/L05.html:300-314", P,
    "1: conditional variance (sig_u^2+sig_upsilon^2)/beta^2 is zero only when both variances vanish, matching A3 (sig^2 >= 0). 2: Lab Part C c0*=5/2 with alternating iterates (printed). 3: at base c1*=-3/10, E p = c0* by the fixed point (derived).")
row("E4b-L05-problems", "L05 problems M1-M3, P1-P3, E1-E3, R1-R3", "course/modules/E/E4/L05.html:316-419", P,
    f"M1 c*=(3,-1/2); M2 Psi(0,0)=(4,-2/3), ratios -1/3; M3 variance 5/4; P1-P3 steps valid; E1 e_5=1/256, c0 path[5]=1025/256 (sixth printed entry), |e_4|=1/64>0.01; E2 Psi(5/2)=5/2; E3 errors -2,3,-9/2,27/4, ratio -3/2; R1 nu=1/2 gives 5/2; R2 delta=0 gives c1*=0; R3 argument. All in {ICK}.")
row("E4b-L05-quiz", "L05 retrieval quiz", "course/modules/E/E4/L05.html:437-500", P,
    "Answers correct: c0*=alpha/(beta+varsigma); c0*=4 at base; varsigma<beta; ratio -1/4; varsigma=beta error sign alternates; nu=beta/(beta+varsigma); variance 5/4; delta=0 gives constant forecast.")
row("E4b-grades-L05", "L05 grades", "course/modules/E/E4/L05.html:295, 423-432", P,
    "Propositions with proofs graded T; base-parameter values graded T as exact closed-form arithmetic with the lab named as reproduction; the Muth claim is graded and bounded to the title.")
row("E4b-struct-L05", "L05 structure", "course/modules/E/E4/L05.html:2, 34-516", P,
    "Header, meta (8 hours, L05 of 9), sections 1-9 in order; prev L04 / next L06 labels (L05.html:511-512). check_pages PASS.")
row("E4b3-L05-footer-muth", "L05 footer and Muth line", "course/modules/E/E4/L05.html:515, 295", P,
    "Footer 'Each graded result carries a proof or a lab result' present; Muth line as in E4b-L05-muth-markup.")
row("E4b3-L05-why-it-matters", "L05 why-it-matters", "course/modules/E/E4/L05.html:51", P,
    "Motivational paragraph states the model, the fixed point and the convergence condition, each defined or proved later in the lesson; no unproved claim about any market (last sentence of L05.html:51).")
row("E4b3-L05-definition12-traders", "Definition 1.2 traders' knowledge", "course/modules/E/E4/L05.html:73, 294-295", P,
    "Definition 1.2 is the fixed-point condition on the conditional expectation (L05.html:73); L05.html:295 states the traders know the price rule, shocks and supply response, consistent with Definition 1.1.")
row("E4b4-muth-crossref", "Muth registry and live check", "course/modules/E/E4/L05.html:295; references/references.json muth1961rational", P,
    f"verify_refs --unit E4 live run PASS (3 of 560 entries, 0 problems, {OUT}/verify_refs_unit_E4.txt); registry title matches the phrase used on the page.")
row("E4b4-L05-lab-validation-note", "L05 lab validation note and docstring", "tests/labs/E4/lab-E4-L05-1.py:14-15; course/modules/E/E4/L05.html:125-137", P,
    "Changed this round (delta 7376a5e..4bd8cb9, twin lines 14-15). New text: 'Each parameter set that Parts B to D iterate is checked by check_params before the iteration runs: beta must be positive and varsigma nonnegative, otherwise the lab raises ValueError.' Verified: show() calls check_params (twin line 87) for BASE, EQUAL, LARGE; Part E does not iterate via show; page code equals twin (code_equals_twin=True).")

# ---- L06 ----
row("E4b-L06-math-model", "Definition 6.1, Definition 6.2, A1-A4, Assumption G", "course/modules/E/E4/L06.html:56-92", P,
    "Primitives, CARA wealth, information structure and clearing condition (A4 quantified over every (s,u)) re-read. G is labelled 'Assumption G' with a letter, not a number; the plan's named-assumption device, accepted in round 5 and unchanged in this delta (L06.html:90-91).")
row("E4b-L06-lemma62", "Lemma 6.2 (CARA demand)", "course/modules/E/E4/L06.html:99-126", P,
    "MGF identity e^{tZ} = e^{t mu + t^2 V/2} re-derived by completing the square; g(x) = -a x (m-p) + a^2 V x^2/2; minimiser x=(m-p)/(aV). Hypothesis V>0 stated.")
row("E4b-L06-lemma63", "Lemma 6.3 (informed beliefs)", "course/modules/E/E4/L06.html:129-144", P,
    "omega = sig_v^2/(sig_v^2+sig_e^2), V_I = sig_v^2 sig_e^2/(sig_v^2+sig_e^2); Cov(e,s)=0 and Cov(e,u)=0 by independence; G gives independence; Var(e)=sig_v^2(1-omega)=V_I (re-derived); 1/V_I=tau_v+tau_e and omega/V_I=tau_e (checked).")
row("E4b-L06-lemma64", "Lemma 6.4 (uninformed beliefs)", "course/modules/E/E4/L06.html:147-156", P,
    "b=Cov(v,p)/Var(p), Cov(v,p)=theta_s sig_v^2; Var(v|p)=sig_v^2 - b Cov(v,p) re-derived; (theta_s,theta_u) != (0,0) gives Var(p)>0 under A1 (sig_u^2>0).")
row("E4b-L06-prop67-uniqueness", "Proposition 6.7 (b) uniqueness, Steps 1 to 4", "course/modules/E/E4/L06.html:190-204", P,
    "Step 1 (theta_s != 0) re-derived. Step 2 (Y=s-kappa' u, eta independent of v) re-derived. Step 3 gives lam tau_e s - Q p = a u with Q = tau_v + taubar' - (1-lam) tau_eta'/theta_s; substitution and evaluation at (1,0),(0,1) give Q theta_s = lam tau_e and Q theta_u = a (the evaluation at (0,0) is vacuous, not false). Step 4 gives kappa, theta_s*, theta_u*.")
row("E4b-L06-prop67-existence", "Proposition 6.7 (a) existence", "course/modules/E/E4/L06.html:207-209", P,
    "Q theta_s* = lam tau_e and Q theta_u* = a verified algebraically (kappa lam tau_e = a); A4 identity follows.")
row("E4b-L06-cor68", "Corollary 6.8", "course/modules/E/E4/L06.html:211-227", P,
    "E[v|p] = tau_eta p/(theta_s*(tau_v+tau_eta)); Var(v|p) = 1/(tau_v+tau_eta) = sig_v^2 sig_eta^2/(sig_v^2+sig_eta^2); slope b equals the same coefficient (re-derived from Step 2 and Problem P3).")
row("E4b-L06-example69-remark610", "Example 6.9 and Remark 6.10", "course/modules/E/E4/L06.html:228-236", P,
    "Round-5 FAIL re-verified: kappa=2, sig_eta^2=2, tau_eta=1/2, taubar=3/4, theta_s=3/7, theta_u=6/7, b=7/9, V_U=2/3, x_I=1/7, x_U=-1/7, clearing 0 (all recomputed in " + ICK + "). The prose 'It does not print tau_v = tau_e = 1, the price 3/7 at (1,0), or the uninformed demand -1/7' matches the printed output (Parts A-C). Remark 6.10 correct (eta variance >= sig_e^2 for sig_u >= 0).")
row("E4b-L06-misconceptions", "L06 misconceptions 1 to 4", "course/modules/E/E4/L06.html:493-513", P,
    "1: uninformed observe Y=v+eta with var 2 (Part A); 2: noise trader has no beliefs (Definition 6.1, A2); 3: slope of p on s is 3/7 and of v on p is 7/9 (Parts A, B); 4: Var(v|p)=2/3 < 1 (Part B, Cor 6.8). Each matches printed output.")
row("E4b-L06-problems-M", "L06 Mechanics M1-M3", "course/modules/E/E4/L06.html:520-541", P,
    f"M1 kappa=4, sig_eta^2=5, tau_eta=1/5, taubar=3/5, theta_s=3/8, theta_u=3/2; M2 Var(p)=27/32, b=4/9, Var(v|p)=5/6, rho^2=1/6 (= sig_v^2/(sig_v^2+sig_eta^2)); M3 p=-3/4, x_I=7/4, x_U=1/4, clearing 1 = u. All recomputed in {ICK}.")
row("E4b-L06-problems-P", "L06 Proof P1-P3", "course/modules/E/E4/L06.html:546-566", P,
    "P1: Lemma 6.3 does not use theta, uses A1 (Cov(e,u)=0 by independence) and G; mean zero of e from A1. P2: theta_s=0 gives uninformed demand -p/(a sig_v^2) depending only on u; clearing at (s,0) and (s+1,0) differs by lam tau_e/a != 0 (A4 hypothesis used at points (s,0),(s+1,0)). P3: common-denominator and reciprocal identities, hypotheses sig_v^2>0, sig_eta^2>0 stated.")
row("E4b-L06-problems-E", "L06 Empirical E1-E3", "course/modules/E/E4/L06.html:571-591", P,
    "E1: (0.80-7/9)/0.05 = 0.44 SE (invented numbers, labelled as such). E2: diff -0.001954, /tol -0.30, SE 0.002166, -0.90 SE (checked). E3: sample is generated by the model, so the check tests the estimator under the model, not observed prices.")
row("E4b-L06-problems-R", "L06 Research R1-R3", "course/modules/E/E4/L06.html:596-616", P,
    "R1: kappa -> infinity as lam -> 0, tau_eta -> 0, theta_s* -> 0, Corr^2 -> 0 with Corr^2 = sig_v^2/(sig_v^2+sig_eta^2) (valid since p/theta_s = v + eta). R2: monotonicity sign steps correct (kappa>0 independent of sig_u). R3: see E4b5-L06-negative-claims.")
row("E4b-L06-quiz-q12", "L06 quiz 12 (probability-one clearing)", "course/modules/E/E4/L06.html:714-722", P,
    "Correct option: a nonzero linear function of (s,u) vanishes only on a line, which has probability zero under the normal law of (s,u); Step 3 uses three points. Matches the A4 justification (L06.html:86).")
row("E4b-L06-A4-section3", "A4 probability-one remark and Step 3", "course/modules/E/E4/L06.html:82-86, 194-202", P,
    "A4 statement quantified over every (s,u) (L06.html:82); the justification at L06.html:86 is consistent with Step 3 (L06.html:202), which evaluates at three pairs including (0,0) as stated.")
row("E4b-L06-quiz-rest", "L06 quiz items", "course/modules/E/E4/L06.html:644-709", P,
    "Answers correct: theta_s*=3/7; kappa=4 at a=2; sig_eta^2=2; omega reason; V_I=1/2; rising sig_u^2 raises sig_eta^2; x_I=1/7; b=7/9; 'the price reveals v exactly' is false; exactly one equilibrium; probability-one reason.")
row("E4b-L06-why-uninformed-trading", "L06 why-it-matters", "course/modules/E/E4/L06.html:51", P,
    "States the random supply, the linear projection, the closed form and the L07 link; each is proved or defined later in the lesson.")
row("E4b-L06-dfn-informed-fraction-posterior", "L06 definitions of informed fraction and posterior", "course/modules/E/E4/L06.html:57, 96", P,
    "lambda is the informed fraction (A2 at L06.html:72); posterior defined at L06.html:96 before first use in Lemma 6.2.")
row("E4b-L06-grades", "L06 grades", "course/modules/E/E4/L06.html:621-637", P,
    "Lemma 6.3, 6.4, Prop 6.7, Cor 6.8 graded T with proof; base values T as exact arithmetic reproduced by Lab Parts A and B; clearing residual C (finite check, Parts C-D); sample slopes C (SIMULATED, one seed). Consistent with BLUEPRINT grades.")
row("E4b-struct-L06", "L06 structure", "course/modules/E/E4/L06.html:2, 34-731", P,
    "Header, meta (8 hours, L06 of 9), sections 1-9 in order, prev L05 / next L07 labels (L06.html:734-735). check_pages PASS.")
row("E4b3-L06-A4-linearity", "A4 linear residual claim", "course/modules/E/E4/L06.html:82-86; tests/labs/E4/lab-E4-L06-1.py:78-106", P,
    "With p = theta_s s - theta_u u substituted, the residual is linear in (s,u) without constant term (both demands and price are linear); Part C residual function (twin 74-106) is linear; checked by independent_checks.")
row("E4b3-L06-A2-informed-observe", "A2 informed observation vs lab", "course/modules/E/E4/L06.html:72, 243-246", P,
    "A2: informed observe s and p; the lab's docstring (L06.html:243-246) says a mass LAM observes s and p, the rest only p, consistent.")
row("E4b5-L06-negative-claims", "L06 negative and 'need not' claims (round-5 FAIL)", "course/modules/E/E4/L06.html:486 (Utility bullet), 500 (misconception), 615 (R3 solution)", P,
    "Round-5 FAILs re-verified: 'linear in general' replaced by 'need be linear' (L06.html:615) and the CRRA sentence now says demand 'need not be the expression of Lemma 6.2' (L06.html:486), a hedge with no universal claim; the page now asserts nothing that is not derived. L06.html:500 now cites 'Definition 6.1 and A2'.")

# ---- cross-cutting ----
row("E4b-hub-titles", "hub lesson titles vs L04-L06 h1", "course/modules/E/E4/index.html:144-146 vs L04.html:35, L05.html:35, L06.html:35", P,
    "Titles match exactly ('Complete and Incomplete Markets', 'Rational-Expectations Equilibrium', 'Noisy rational-expectations equilibrium'). index.html unchanged since 7376a5e.")
row("E4b-dag-closure", "DAG: concepts used in L04-L06 are in the prerequisite closure or earlier E4 lessons", "L04-L06 text, math and links", P,
    "Owners from curriculum/curriculum.json 'concepts': M3 (vector-space, linear-map, least-squares-projection, orthogonal-projection), M4 (expectation, variance, independence, normal-distribution, multivariate-normal, random-variable, conditional-expectation-elementary), E1 (competitive-equilibrium), E3 (expected-utility, crra-utility), E4 (arrow-debreu-security in L01; rational-expectations-equilibrium in L05; noisy-rational-expectations-equilibrium in L06). All are in the E4 closure or defined earlier.")
row("E4b-concept-definitions", "concept definitions in the assigned lessons", "course/modules/E/E4/L04.html:77; L05.html:73; L06.html:169", P,
    "<dfn data-concept> for market-completeness (L04.html:77), rational-expectations-equilibrium (L05.html:73), noisy-rational-expectations-equilibrium (L06.html:169); each defined once, in its assigned lesson.")
row("E4b-notation-registry", "notation registry: macros and symbols in L04-L06", "course/modules/E/E4/L04.html, L05.html, L06.html; notation/notation.json", P,
    "Macros used: \\E, \\Var, \\Cov, \\Corr, \\R, \\Normal, all registered. \\mathbb{R} count 0 in all three pages (ruling 1). No registered program-wide symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) appears (grep count 0).")
row("E4b-simulated-labels", "SIMULATED labels", "course/modules/E/E4/L06.html:238, 252, 254, 469-475, 627", P,
    "Part E is labelled SIMULATED in the hypothesis (L06.html:238), in the docstring (twin line 14), and in the output header (L06.html:475); Key results grade C with 'SIMULATED' (L06.html:633).")
row("E4b-banned-process-words", "banned phrases and process words", "L04-L06 visible prose and code docstrings", P,
    "grep -i for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, simply, trivially, of course, round N, verifier, builder, fixer, we will, let us, in this section we: zero hits in the stripped text of L04, L05, L06 (/tmp views regenerated by strip_view.py).")
row("E4b-page-width-360", "no horizontal scroll at 360 px", "course/modules/E/E4/L04.html, L05.html, L06.html", P,
    f"page_smoke PASS for L04, L05, L06 at 360 px (zero horizontal-scroll failures; {OUT}/page_smoke_E4.txt).")
row("E4b-nav-labels", "previous/next nav labels", "course/modules/E/E4/L04.html:519-520, L05.html:511-512, L06.html:734-735", P,
    "Labels match the h1 of the adjacent lessons (L03 title in L04 prev is out of slice; L04 next 'L05 · Rational-Expectations Equilibrium' matches L05 h1).")
row("E4b3-L04-footer", "L04 footer", "course/modules/E/E4/L04.html:524", P,
    "Footer 'Each graded result carries a proof or a lab result.' present.")
row("E4b3-hub-pq3", "hub Pq3 (out-of-slice observation)", "course/modules/E/E4/index.html:81-84", P,
    CARRY_HUB + "no L04-L06 subject; recorded as an out-of-slice note in round 5 (zeta used as a Lagrange multiplier in the hub versus a portfolio in L04).")
row("E4b4-independent-checks", "independent recomputation of prose numbers", f"{ICK}", P,
    f"Exact-Fraction recomputation of every L04-L06 number checked in this round (L05 fixed point, ratios, paths, E1-E3, M1-M3, R1; L06 Example 6.9, Part B-D values, M1-M3, E1-E2; L04 ranks, remarks, R3 construction). Output: ALL OK ({SC}/outputs/independent_checks.txt).")
row("E4b4-cards-L04-L06", "retrieval cards for L04-L06 (full scan)", "course/modules/E/E4/cards.json (82 cards: L04 c053-c073, c215, c217, c218; L05 c074-c099, c219; L06 c100-c129, c220)", P,
    "Full scan of all 82 L04-L06 cards: ids unique, no duplicate fronts, each card matches the current lesson text and the printed lab values, every card number appears in its lesson. Changed cards re-verified: c086 (Lemma 3.1 now 'Under A1 to A3'), c107 (A1 and A4 of L06), c121 (Assuming A1 to A4 and G), c123 (alternative theta_s=1/2, residual -9/85 printed at L06.html:474), c218 (kernel dimension J - rank(A), nonzero when rank < J).")
row("E4b4-grade-legend-variant", "grade legend and the variant labels", "course/modules/E/E4/L04.html:42-49; L05.html:42-49; L06.html:42-49", P,
    "Legend lists T, A, B, C, D, X with the same meanings in all three pages; the grades used are in the legend.")
row("E4b4-notation-eta", "eta in L05 and L06", "course/modules/E/E4/L05.html:58-60; L06.html:179-203, 235", P,
    "L05 uses no eta; L06 uses eta only as the price-noise variable eta = epsilon - kappa u (L06.html:235) and sigma_eta^2 defined at L06.html:179 before use. Consistent.")
row("E4b4-notation-s", "s as signal", "course/modules/E/E4/L04.html (all); L06.html:57", P,
    "L04 has no math variable s (the only lowercase s in the L04 text is the possessive in 'security's payoff', L04.html:271); L06 defines s = v + eps at L06.html:57 before use.")
row("E4b4-notation-x", "x as a holding (L06) vs L04", "course/modules/E/E4/L04.html (all); L06.html:82, 162, 169, 192, 230, 682", P,
    "L04 uses '\\times' only (J x S); no variable x. L06 uses x for the risky holding, defined in Definition 6.2 (L06.html:67) before the uses at L06.html:82 and later. No collision within a lesson.")
row("E4b5-hub-lede-lesson-map", "hub lede and lesson map (out-of-slice index.html)", "course/modules/E/E4/index.html:144-146", P,
    CARRY_HUB + "lede and lesson-map lines for L04-L06 match the lessons (L04 'exact rank computation on a complete and an incomplete' matches Lab 1).")

# ---- round-6 additions ----
row("E4b6-delta-review", "every hunk of the delta 7376a5e..4bd8cb9 in the slice", "L04.html:292; L05.html:136-137; L06.html:486, 500, 615; tests/labs/E4/lab-E4-L05-1.py:14-15; cards.json (c086, c107, c121, c123, c218)", P,
    "git diff 7376a5e 4bd8cb9 read hunk by hunk. Slice hunks: L04.html 1 hunk (Prop 4.2 wording, see E4b6-L04-prop42-proof-link FAIL), L05.html 1 hunk (check_params sentence), L06.html 3 hunks (utility bullet, misconception, R3 solution), lab-E4-L05-1.py 1 hunk (twin lines 14-15, docstring, identical to page). Card hunks in slice: c086, c107, c121, c123, c218. Out-of-slice card hunks (not verified here): c052 (L03), c139 (L07), c180 (L08), c185/c199/c209/c210 (L09). index.html and L06 twin unchanged in this delta.")
row("E4b6-cards-changed", "changed cards in the slice", "course/modules/E/E4/cards.json: E4-c086, c107, c121, c123, c218", P,
    "Each changed card checked against the current lesson text and the printed output: c086 (Lemma 3.1, A1 to A3), c107 (A4 probability-one), c121 (Remark 6.10), c123 (-9/85, L06.html:474), c218 (rank-nullity, J - rank). All true.")
row("E4b6-in-general-scan", "scope words 'in general' in L04-L06", "course/modules/E/E4/L04.html:271, 386; L05.html:292", P,
    "L04.html:271 'In general, the linear map ... has rank rank(A), so by rank-nullity its kernel has dimension J - rank(A)' is derived; L04.html:386 is the E2 solution's 'in general' (derived family); L05.html:292 is a negated scope statement supported by A2 and Remark 4.1. L06 has 0 'in general' hits.")

notes = [
    "Round 6 of E4-b (L04, L05, L06 and their three lab twins) at pin 4bd8cb9. Delta from 7376a5e read hunk by hunk (see E4b6-delta-review). Every line of L04.html, L05.html and L06.html was read (stripped text views with line numbers, regenerated by ledgers/E4/scripts/E4-b-r6/strip_view.py; math re-derived; numbers recomputed by independent_checks.py, 54 checks, ALL OK).",
    "The one defect this round is the Proposition 4.2 proof linkage (E4b6-L04-prop42-proof-link). It is a one-sentence fix. Every other row is PASS.",
    "Scripts: ledgers/E4/scripts/E4-b-r6/ (run_gates.sh, strip_view.py, expected_vs_output.py, independent_checks.py, write_fragment.py, outputs/). Previous round fragment: /Users/billyribeiro/.fanout/frags/E-E4-b.round5.json (context only).",
    "Mutants: none. This slice has no project grader; lab twins are demonstrations (verifier rules, lab-mutant ruling). Project-grader mutation testing is out of slice.",
    "Non-blocking observations (PASS, not rows): (a) L05.html:51 intro names 'the rational-expectations equilibrium (Definition 1.2)' before its definition at L05.html:73, as a forward pointer; (b) Assumption G in L06 is lettered, not numbered (plan named-assumption device, as in round 5); (c) L06.html:359-361 (Lab Part C) 'evaluating at (0,0), (1,0), (0,1)' in Step 3 of Prop 6.7 gives only two equations, the (0,0) point is vacuous, not false.",
    "Out-of-slice observations: L03 card E4-c052 now says 'Arrow-Debreu security prices' (not in my slice); L03.html:499 next-label case; out of scope for this slice.",
]

summary = (
    "FAIL E4-b round 6: rows=%d. Non-PASS: E4b6-L04-prop42-proof-link (L04.html:293, the Prop 4.2 proof never links zeta, phi to xi, eta). "
    "All command gates PASS at 4bd8cb9 (check_pages, check_dag, check_projects, run_labs 12/12 and per page, twins under python -I -W error, page code equals twin, expected equals output, ruff, mypy, pytest 13 passed, page_smoke, verify_refs live and offline). "
    "Round-5 FAILs E4b5-L04-prop42-symbols and E4b5-L06-negative-claims re-verified PASS."
) % len(rows)

fragment = {
    "unit": "E4",
    "slice": "b",
    "round": 6,
    "verifier": "Haiku independent verifier, E4-b round 6 (did not build E4)",
    "pin": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (4bd8cb9)",
    "base": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f (round-5 pin 7376a5e)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE6-E4-b",
    "scratch": "ledgers/E4/scripts/E4-b-r6/ (run_gates.sh, strip_view.py, expected_vs_output.py, independent_checks.py, write_fragment.py, outputs/)",
    "verified_at": "2026-11-04",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}

with open("ledgers/E4/E4-b.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "non-pass", [r["id"] for r in rows if r["status"] != P])
