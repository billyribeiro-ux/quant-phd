"""Writes ledgers/E4/E4-b.json (round 8). Run from the checkout root: .venv/bin/python <this file>."""
import json
import subprocess
from datetime import UTC, datetime

S = "ledgers/E4/scripts/E4-b-r8/outputs/"
OK = "PASS"
rows = []


def r(rid, check, location, status, evidence, fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != OK:
        row["fix"] = fix
    rows.append(row)


# ---- command gates, all re-run at pin 0dee921a this round (outputs in ledgers/E4/scripts/E4-b-r8/outputs/)
r("E4b-cmd-check_pages", "tools/check_pages.py --unit E4", "tools/check_pages.py --unit E4", OK,
  f"'check_pages E4: PASS' ({S}check_pages_E4.txt, exit 0, run_gates.sh).")
r("E4b-cmd-check_dag", "tools/check_dag.py --unit E4", "tools/check_dag.py --unit E4", OK,
  f"'check_dag E4: PASS' ({S}check_dag_E4.txt, exit 0).")
r("E4b-cmd-check_projects", "tools/check_projects.py --unit E4", "unit gate, outside slice b, run for completeness", OK,
  f"'check_projects E4: PASS' ({S}check_projects_E4.txt, exit 0).")
r("E4b-cmd-run_labs", "tools/run_labs.py --unit E4 and --page L04, L05, L06", "tools/run_labs.py", OK,
  f"'run_labs E4: PASS (12/12)'; per page 'PASS (1/1)' for L04, L05, L06 ({S}run_labs_*.txt, exit 0).")
r("E4b-cmd-twins-isolated", "python -I -W error on each twin, alone", "tests/labs/E4/lab-E4-L04-1.py, L05-1.py, L06-1.py", OK,
  f"Exit 0 for all three ({S}twin_L04.txt, twin_L05.txt, twin_L06.txt; _summary.txt). L06 Part E 'within True' twice, Part C 'all_zero True'.")
r("E4b-cmd-page-code-equals-twin", "page lab code byte-identical to twin", "L04.html, L05.html, L06.html lab blocks", OK,
  f"ledgers/E4/scripts/E4-b-r8/expected_vs_output.py: 'code_equals_twin=True' for L04, L05, L06 ({S}expected_vs_output.txt).")
r("E4b-cmd-expected-equals-output", "expected block equals run stdout", "L04.html, L05.html, L06.html expected blocks", OK,
  f"Same script: 'expected_equals_output=True' for L04, L05, L06; exit 0, stderr empty ({S}expected_vs_output.txt).")
r("E4b-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on the twins", "tests/labs/E4/*", OK,
  f"'All checks passed!'; '12 files already formatted'; 'Success: no issues found in 3 source files' ({S}ruff_check.txt, ruff_format.txt, mypy_twins.txt).")
r("E4b-cmd-pytest-labs", "pytest -k E4 tests/test_labs.py tests/test_run_labs.py", "tests/test_labs.py, tests/test_run_labs.py", OK,
  f"'13 passed, 352 deselected' ({S}pytest_E4.txt).")
r("E4b-cmd-page_smoke", "tools/page_smoke.py --unit E4 --pages L04 L05 L06 (alone)", "tools/page_smoke.py", OK,
  f"'page_smoke modules/E/E4/L04.html: PASS', L05 PASS, L06 PASS, 'page_smoke E4: PASS' ({S}page_smoke_E4.txt).")
r("E4b-cmd-verify_refs-live", "tools/verify_refs.py --unit E4 (live)", "tools/verify_refs.py --unit E4", OK,
  "Re-run this round: 'live re-verification of E4: 3 of 560 entries, 0 problems', exit 0 "
  f"({S}verify_refs_unit_E4_live.txt). Plain tool invocation.")
r("E4b-cmd-verify_refs-offline", "tools/verify_refs.py --offline", "tools/verify_refs.py --offline", OK,
  f"'offline integrity: 560 entries, 0 problems' ({S}verify_refs_offline.txt).")

# ---- lab twins and hypotheses
r("E4b-lab-L04-1", "lab twin L04 hypothesis and interpretation", "course/modules/E/E4/L04.html:119, 259; tests/labs/E4/lab-E4-L04-1.py", OK,
  "Read L04.html:119 and 259 this round against the printed block L04.html:243-258. Hypothesis (two securities rank 2 incomplete; four securities rank 3 complete; (1,2,3) attainable; (0,0,1), (5,0,0) not) matches output. Independently re-derived: ledgers/E4/scripts/E4-b-r8/outputs/indep_rederive.txt L04 section (minors).")
r("E4b-lab-L05-1", "lab twin L05 hypothesis, docstring and output", "course/modules/E/E4/L05.html:122, 125-137, 255-280; tests/labs/E4/lab-E4-L05-1.py:14-15", OK,
  "L05.html:122 hypothesis (c0*=4, c1*=-3/10, ratio -1/4, ς=β ratio -1 path 0,5, ς=3 ratio -3/2, weight 4/5) matches the printed block and indep_rederive.txt L05 section. Twin lines 14-15 (check_params sentence) match show() calling check_params before iterate.")
r("E4b-lab-L06-1-outputs", "lab twin L06 printed output and prose", "course/modules/E/E4/L06.html:460-478, 479-485; tests/labs/E4/lab-E4-L06-1.py", OK,
  "Output block equals run stdout (expected_vs_output.py). Prose L06.html:479 quotes Var(s)=2, Var(p)=27/49, Cov=3/7, slope 7/9, posterior 2/3, 16 grid points all zero, informed demand 1/7, residual -9/85, sample slopes 0.426617 / 0.761928, tolerances 0.006497 / 0.023538. All re-derived this round (indep_rederive.txt L06 section; Part B closed-form slope 7/9 and posterior 2/3 by Gaussian conditioning).")
r("E4b-lab-L06-1-units", "lab docstring units paragraph", "tests/labs/E4/lab-E4-L06-1.py:17-21", OK,
  "Read twin lines 17-21 this round. Dimension bookkeeping by hand: a in 1/price, sig_e2 in (price/asset)^2, kappa = a*sig_e2/lam in price/asset^2, theta_u*u in price/asset, theta_s dimensionless; x=(m-p)/(aV) in asset units. Consistent.")
r("E4b-lab-L06-1-residual-docstring", "lab residual() docstring vs code", "tests/labs/E4/lab-E4-L06-1.py:78-106", OK,
  "Read lines 78-106 this round: docstring (informed mean omega*s, Var(v|s,p)=V_I, uninformed slope Cov/Var(p), residual variance Var(v)-slope*Cov) matches code lines one for one; returns lam*demand_inf+(1-lam)*demand_unf-u, i.e. demand minus supply.")
r("E4b-lab-L06-1-hypothesis-xref", "lab hypothesis cross-reference", "course/modules/E/E4/L06.html:238-240", OK,
  "Hypothesis cites Prop 6.7 and Example 6.9 values (kappa=2, sig_eta2=2, tau_eta=1/2, taubar=3/4, theta_s=3/7, theta_u=6/7): match. Alternative theta_s=1/2 gives residual -9/85 at (1,0), recomputed by hand and by indep_rederive.txt (value -9/85, nonzero). Part E seed 6, 20 000 draws (twin lines 36-38) matches.")

# ---- L04 mathematics
r("E4b-L04-math-sec1", "Definitions 1.1, 1.3; Lemma 1.2; Theorem 1.4; Proposition 1.5; Corollary 1.6", "course/modules/E/E4/L04.html:65-95", OK,
  "Read every line this round. Lemma 1.2 linearity and row-space argument; Theorem 1.4 full-dimension argument; Prop 1.5 subspace containment with equal dimensions; Cor 1.6 span bound. All complete under A1-A3 (A1-A3 stated at L04.html:56-60).")
r("E4b-L04-math-lemma21", "Lemma 2.1 (elimination counts rank)", "course/modules/E/E4/L04.html:101-104 (proof line 103)", OK,
  "Proof line 103 read in full: swap/add-multiple steps preserve row space (line 102); echelon reduction terminates; independence of nonzero echelon rows by smallest-index argument (rows below have zeros in column q_i since q_l > q_i; rows above have c_l=0 by minimality). Count argument valid.")
r("E4b-L04-math-examples", "Examples 2.2 and 2.3", "course/modules/E/E4/L04.html:107-115", OK,
  "Example 2.2: rank 2 < 3; (1,2,3)=r1+r2 attainable with zeta=(1,1); (0,0,1) augmented rank 3. Example 2.3: r4=(1,2,3)=e1+2e2+3e3, rank 3, complete. Re-derived by minors in indep_rederive.txt.")
r("E4b-L04-math-remark31", "Remark 3.1 (one security per state)", "course/modules/E/E4/L04.html:265-268", OK,
  "rank(I_S)=S, complete by Theorem 1.4; zeta = xi gives zeta^T I_S = xi, checked by hand.")
r("E4b-L04-math-remark32", "Remark 3.2 (redundancy and kernel)", "course/modules/E/E4/L04.html:270-272 (line 271)", OK,
  "Line 271 kernel {zeta: zeta^T A = 0} has dimension J - rank(A) (rank-nullity). indep_rederive.txt: J=4, rank 3, kernel dim 1. Family (1-t,2-2t,3-3t,t) checked at t=1/3 giving (1,2,3). Translate-of-kernel claim holds.")
r("E4b-L04-math-sec4", "Proposition 4.1 (no finite market complete with infinitely many states)", "course/modules/E/E4/L04.html:277-288", OK,
  "Proof: dim M(A) <= J; J+1 distinct states; indicator functions independent (evaluate at omega_k); a subspace of dimension <= J cannot contain them or equal R^Omega. Complete.")
r("E4b5-L04-prop42-symbols", "Proposition 4.2 statement symbols", "course/modules/E/E4/L04.html:291-292", OK,
  "Statement introduces xi, eta in C(A) and a*xi+b*eta with a,b>=0; (-1,0) not in C(I_2) since it has a negative entry; (-1,0) attainable under A3 via zeta=(-1,0).")
r("E4b6-L04-prop42-proof-link", "Proposition 4.2 proof: portfolios zeta, phi linked to xi, eta", "course/modules/E/E4/L04.html:293", OK,
  "Line 293 begins 'Let zeta, phi >= 0 with xi = zeta^T A and eta = phi^T A': linked. Closure a*xi+b*eta=(a zeta+b phi)^T A checked line by line.")
r("E4b-L04-misconceptions", "L04 misconceptions 1 to 4", "course/modules/E/E4/L04.html:297-317", OK,
  "Misconception 1 (Example 2.3 complete, Lab prints complete True); 2 (rows (1,1,1),(1,1,1),(0,1,2) rank 2, Cor 1.6 is not the converse); 3 (two portfolios, Lab Part E prints equals_fourth_row True; unique portfolio requires independent rows); 4 (Def 1.3 and Thm 1.4 use only A). Each re-derived.")
r("E4b-L04-problems", "L04 problem set M1-M3, P1-P3, E1-E3, R1-R3", "course/modules/E/E4/L04.html:319-421", OK,
  "M1 rank 1; M2 zeta=(1,1) for (1,1,2), (0,0,1) not attainable; M3 r3=r1+r2, r4=2r1+r2, rank 2 (indep_rederive.txt M1/M3 ranks). P1-P3 valid. E1 zeta1=5, zeta2=-5, 5-10 != 0 (checked). E2 family (1-t,2-2t,3-3t,t) verified. E3 rank 2 (indep_rederive). R1 Cor 1.6; R2 I_S; R3 t=max(0,-x1,-x2) checked by hand.")
r("E4b-L04-quiz-q4", "L04 quiz: replicating portfolios of (1,2,3)", "course/modules/E/E4/L04.html:467-475", OK,
  "Correct option is the family (1-t,2-2t,3-3t,t); explanation at line 474 derives it from (zeta1+zeta4, zeta2+2zeta4, zeta3+3zeta4)=(1,2,3) and matches Remark 3.2. Wrong options checked.")
r("E4b-L04-quiz-rest", "L04 quiz items", "course/modules/E/E4/L04.html:441-508", OK,
  "Answers re-checked: Thm 1.4 rank condition; five states needs J>=5 (I_5 attains, Remark 3.1); rank 2 for the repeated-row matrix; Prop 1.5 criterion; rank 1 for (1,2,0),(2,4,0); infinite states incomplete (Prop 4.1); (-1,0) not attainable under zeta>=0 (Prop 4.2).")
r("E4b-L04-why-empirical", "L04 'illustrative numbers' statements", "course/modules/E/E4/L04.html:51, 259, 321", OK,
  "Matrices are described as illustrative numbers (L04.html:321), and the printed ranks are said to say nothing about any market (L04.html:259). Consistent with lab docstring (twin lines 3-5).")
r("E4b-grades-L04", "L04 grades (legend and key results)", "course/modules/E/E4/L04.html:42-49, 81-96, 427-436", OK,
  "Legend T/A/B/C/D/X matches the BLUEPRINT §3 grade letters; C is used for 'single study or finite check', the plan's finite-enumeration precedent. Key results: T with a proof on the page or 'Example 2.2 by hand; Lab 1 Part A'. Consistent.")
r("E4b-struct-L04", "L04 structure, order, footer", "course/modules/E/E4/L04.html (sections, order, footer line 524)", OK,
  "Sections 1-9 in order (1 Attainable payoffs; 2 Rank by elimination; 3 Arrow-Debreu and redundancy; 4 Where the canon breaks; 5 Misconceptions; 6 Problem set; 7 Key results; 8 Retrieval quiz; 9 References). Footer at line 524. Nav links L03/L05 at lines 519-520.")

# ---- L05 mathematics
r("E4b-L05-math-sec1-2", "L05 Definitions 1.1-1.2, Lemma 2.1, Proposition 2.2, Corollary 2.3", "course/modules/E/E4/L05.html:65-97", OK,
  "Read in full. Demand d=alpha-beta p+u; supply q=varsigma m+delta z+upsilon; p_m=(alpha - varsigma m - delta z + u - upsilon)/beta: checked. Lemma 2.1 mean and variance (sig_u^2+sig_upsilon^2)/beta^2 checked. Prop 2.2 Psi fixed point c0*=alpha/(beta+varsigma), c1*=-delta/(beta+varsigma): checked by substitution. Cor 2.3 Var(p) formula checked.")
r("E4b-L05-math-sec3", "L05 Lemma 3.1 and its proof", "course/modules/E/E4/L05.html:103-118", OK,
  "e_{k+1}=-(varsigma/beta) e_k for each component: checked by subtracting fixed-point identities (both components). Induction gives the power formula. Prop 3.3 error factor 1-nu(1+varsigma/beta) with nu=beta/(beta+varsigma) is zero: checked.")
r("E4b-L05-prop32", "Proposition 3.2 (when iteration converges)", "course/modules/E/E4/L05.html:109-111", OK,
  "varsigma<beta: error factor |varsigma/beta|^k -> 0. varsigma=beta: constant magnitude; varsigma>beta: grows. Statement and proof agree; 'from every starting point' requires varsigma<beta, as stated.")
r("E4b-L05-sec5-wording", "L05 section 5 wording", "course/modules/E/E4/L05.html:292-296 (line 295)", OK,
  "Line 295 (traders know the price rule, shock distribution and supply response) matches Def 1.2 construction. Line 294 matches Prop 3.2 ('converges from every starting point only when varsigma<beta'). No overclaim found.")
r("E4b-L05-prop34-remark41", "Proposition 3.3 and Remark 4.1", "course/modules/E/E4/L05.html:115-118, 286-288", OK,
  "Prop 3.3 proof recomputed. Remark 4.1: Prop 2.2 shows the affine family contains exactly one REE, and does not exclude non-affine forecasts: consistent with Prop 2.2's uniqueness within the affine family.")
r("E4b-L05-notation-gamma", "L05 registry symbols (gamma, Phi, R*, R_f, Q, T)", "course/modules/E/E4/L05.html (all), notation/notation.json", OK,
  "No registered symbol (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, mathbb Q) appears in L05 math (notation_scan.sh output). Macros used (\\E, \\R, \\Var, \\Cov, \\Normal) are registered.")
r("E4b-L05-notation-s", "L05 symbol s / z / upsilon usage", "course/modules/E/E4/L05.html:66, 73, 104; course/modules/E/E4/L06.html:57", OK,
  "Symbols are local to each lesson (notation.json says conventionally local letters are defined where used); no registry conflict. L05 uses z for the public signal, L06 uses s for the signal, defined at L06.html:57.")
r("E4b-L05-muth-markup", "L05 citation markup and registry record", "course/modules/E/E4/L05.html:296; references/references.json (key muth1961rational)", OK,
  "data-cite='muth1961rational' with data-locator='title' resolves to the registry record: title 'Rational Expectations and the Theory of Price Movements', Muth, John F., 1961, Econometrica 29(3). The sentence wording is covered by E4b8-process-registry-page (FAIL).")
r("E4b-L05-math-muth-scope", "L05 Muth scope: no result used", "course/modules/E/E4/L05.html:295-296", OK,
  "The page uses the title only and states it uses no result from the paper; the lesson's results are derived on the page (Props 2.2, 3.2, 3.3). Scope is accurate.")
r("E4b-L05-misconceptions", "L05 misconceptions", "course/modules/E/E4/L05.html:300-314", OK,
  "M1 'exact': Cor 2.3 variance (sig_u^2+sig_upsilon^2)/beta^2, zero only when both variances zero; unbiased given z. M2: Prop 2.2 existence for all beta>0, varsigma>=0; Lab Part C alternates 0,5 with fixed point 5/2. M3: c1*=-delta/(beta+varsigma), c0* is the unconditional mean, checked: E p = c0* since E z = E u = E upsilon = 0.")
r("E4b-L05-problems", "L05 problem set M1-M3, P1-P3, E1-E3, R1-R3", "course/modules/E/E4/L05.html:316-419", OK,
  "M1 c0*=3, c1*=-1/2, Psi fixed (checked). M2 Psi(0,0)=(4,-2/3), error ratios -1/3 both (checked). M3 variance 5/4 (checked). P1-P3 valid. E1 e_5=1/256 and printed 1025/256 (checked). E2 path stays put at 5/2 (checked). E3 e=(-2,3,-9/2,27/4), ratio -3/2 (checked). R1 weight 1/2 gives 5/2 (checked). R2 delta=0 gives constant forecast (checked). R3 argument valid.")
r("E4b-L05-quiz", "L05 quiz items", "course/modules/E/E4/L05.html:437-500", OK,
  "Answers re-checked: Prop 2.2 c0*=alpha/(beta+varsigma); c0*=4 at base; convergence when varsigma<beta; ratio -1/4; ratio -1 at varsigma=beta; damped weight beta/(beta+varsigma); 5/4; delta=0 gives constant forecast.")
r("E4b-grades-L05", "L05 grades (legend and key results)", "course/modules/E/E4/L05.html:42-49, 295, 423-433", OK,
  "Legend identical to L04 and L06 (lines 42-49). Key results grade T with proof references (Lemma 2.1, Prop 2.2, Cor 2.3, Lemma 3.1, Props 3.2-3.3) and the one lab-based row (Lab 1 Parts A and B) is backed by Lemma 3.1.")
r("E4b-struct-L05", "L05 structure, order, footer", "course/modules/E/E4/L05.html (sections, order, footer line 516)", OK,
  "Sections 1-10 in order; footer at line 516; nav Previous L04, Next L06 at lines 511-512.")

# ---- L05 footer and Muth lines
r("E4b3-L05-footer-muth", "L05 footer and Muth line", "course/modules/E/E4/L05.html footer (line 516); :296", OK,
  "Footer present (line 516). Muth line at :296 read; citation markup valid (see E4b-L05-muth-markup).")
r("E4b3-L05-why-it-matters", "L05 'why it matters' paragraph", "course/modules/E/E4/L05.html:51", OK,
  "Read: the fixed point (Prop 2.2), iteration convergence only when varsigma<beta (Prop 3.2), lab checks fixed point and error ratios (Lemma 3.1). Consistent with the sections.")
r("E4b3-L05-definition12-traders", "L05 Definition 1.2 and traders' knowledge", "course/modules/E/E4/L05.html:73, 294, 295", OK,
  "Def 1.2 (m(z) = E[p_m | z] for every real z) and the Lemma 2.1 version of the conditional expectation: consistent with 294-295 (traders know the price rule and supply response, a stated modelling choice).")
r("E4b4-muth-crossref", "Muth registry record matches the page", "course/modules/E/E4/L05.html:296; references/references.json key muth1961rational", OK,
  "Record fields: title 'Rational Expectations and the Theory of Price Movements', authors Muth John F., year 1961, Econometrica volume 29 issue 3 (JSTOR), status verified. Page uses the title only, which is the locator named by the record.")
r("E4b4-L05-lab-validation-note", "L05 lab validation note", "tests/labs/E4/lab-E4-L05-1.py:14-15; course/modules/E/E4/L05.html:125-137", OK,
  "check_params is called in show() before iteration (twin line 209 of the page code); raises ValueError for beta<=0 or varsigma<0 (checked). Parts B-D iterate via show(); Part E uses no iteration; statement is accurate.")

# ---- L06 mathematics
r("E4b-L06-math-model", "L06 Definition 6.1, Definition 6.2, Assumptions A1-A4, G", "course/modules/E/E4/L06.html:56-92", OK,
  "Read in full. A1 normal primitives with positive variances; A2 lambda in (0,1); A3 price rule linear; A4 clearing at every pair (s,u) with the three-point argument at Step 3 (proof of Prop 6.7, lines 194-202). The probability-one remark is a valid argument for a residual that is linear without constant term. G stated and used without proof, as declared.")
r("E4b-L06-lemma62", "Lemma 6.2 (CARA demand)", "course/modules/E/E4/L06.html:99-126", OK,
  "E e^{tZ} = e^{t mu + t^2 V/2} proof: completing the square checked term by term. Expected utility = -e^{-a w0} e^{g(x)}, g(x) = -ax(m-p)+a^2 V x^2/2; minimizer x*=(m-p)/(aV). Checked.")
r("E4b-L06-lemma63", "Lemma 6.3 (informed beliefs)", "course/modules/E/E4/L06.html:129-144", OK,
  "omega, V_I, 1/V_I = tau_v+tau_eps, omega/V_I = tau_eps checked by algebra. Proof: Cov(e,s)=0 and Cov(e,u)=0 by independence; G gives independence; Var(e)=sig_v^2(1-omega)=V_I (checked).")
r("E4b-L06-lemma64", "Lemma 6.4 (uninformed beliefs are a linear projection)", "course/modules/E/E4/L06.html:147-156", OK,
  "b=Cov(v,p)/Var(p), Cov(v,p)=theta_s sig_v^2, E[v|p]=bp, Var(v|p)=sig_v^2 - b Cov(v,p) (checked; b^2 Var(p) = b Cov).")
r("E4b-L06-prop67-uniqueness", "Proposition 6.7 (b): uniqueness, Steps 1-4", "course/modules/E/E4/L06.html:190-204", OK,
  "Step 1: theta_s=0 forces lambda*tau_eps*s/a=0 at u=0, contradiction at s=1. Step 2: Y=p/theta_s, Var(v|p) and E[v|p] via Lemma 6.4 with P_U'. Step 3: clearing identity and Q; evaluation at (1,0),(0,1) gives Q theta_s=lambda tau_eps, Q theta_u=a (the (0,0) point is redundant; harmless). Step 4 solves to theta_s*, theta_u*. Checked line by line.")
r("E4b-L06-prop67-existence", "Proposition 6.7 (a): existence", "course/modules/E/E4/L06.html:207-209", OK,
  "theta_s*>0 since taubar>0; Y=s-kappa u with variance sig_eta^2; Q theta_s*=lambda tau_eps and Q theta_u*=kappa lambda tau_eps = a. Clearing expression reduces to a u for every (s,u). Checked.")
r("E4b-L06-cor68", "Corollary 6.8", "course/modules/E/E4/L06.html:211-227", OK,
  "E[v|p]=tau_eta p/(theta_s*(tau_v+tau_eta)), Var(v|p)=1/(tau_v+tau_eta)=sig_v^2 sig_eta^2/(sig_v^2+sig_eta^2), slope b equal (checked). Numerically: 7/9 and 2/3 at base (indep_rederive.txt).")
r("E4b-L06-example69-remark610", "Example 6.9 and Remark 6.10", "course/modules/E/E4/L06.html:228-236 (line 235)", OK,
  "Example 6.9 numbers recomputed: kappa=2, sig_eta^2=2, tau_eta=1/2, taubar=3/4, theta_s=3/7, theta_u=6/7, b=7/9, V_U=2/3, x_I=1/7, x_U=-1/7 (checked by hand; x_U=((7/9)(3/7)-3/7)/(2/3)=-1/7). Remark 6.10: Y=v+eta, sig_eta^2>=sig_eps^2>0, larger sig_u^2 lowers tau_eta: checked.")
r("E4b-L06-misconceptions", "L06 misconceptions 1 to 4", "course/modules/E/E4/L06.html:493-513 (line 503)", OK,
  "M1: Y=s-kappa u=v+eta, sig_eta^2=2 at base (Lab Part A). M2: noise trader is a random supply independent of payoff (Def 6.1, A1). M3: slope of p on s is 3/7, slope of v on p is 7/9 (Lab Parts A, B). M4: Var(v|p)=2/3 < 1 (Lab Part B; Cor 6.8). All consistent with the printed lab output.")
r("E4b-L06-problems-M", "L06 problem set M1-M3", "course/modules/E/E4/L06.html:520-541", OK,
  "M1: kappa=4, sig_eta^2=5, tau_eta=1/5, taubar=3/5, theta_s=3/8, theta_u=3/2 (re-derived, indep_rederive.txt 'M1 instance'). M2: Var(p)=27/32, b=4/9, Var(v|p)=5/6, squared correlation 1/6 (checked by hand). M3: p=-3/4, x_I=7/4, Y=-2, x_U=1/4, clearing gives 1 = u (checked).")
r("E4b-L06-problems-P", "L06 problem set P1-P3", "course/modules/E/E4/L06.html:546-566", OK,
  "P1 informed belief independent of theta (Lemma 6.3 uses only A1, G, and the covariance zeros). P2 theta_s != 0 from A4 at (s,0) and (s+1,0): difference lambda tau_eps/a != 0, supply equal. P3 identity sig_v^2 - sig_v^4/(sig_v^2+sig_eta^2) = sig_v^2 sig_eta^2/(sig_v^2+sig_eta^2) = 1/(tau_v+tau_eta): checked.")
r("E4b-L06-problems-E", "L06 problem set E1-E3", "course/modules/E/E4/L06.html:571-591 (line 590)", OK,
  "E1: 0.80-7/9=0.0222, /0.05=0.44 SE (checked); invented numbers labelled. E2: -0.001954 difference; -0.30 of tolerance; SE 0.002166; -0.90 SE (checked to 3 s.f.). E3 reasoning consistent with the seeded-sample design. Line 590 reads as a sampling statement, consistent with the code.")
r("E4b-L06-problems-R", "L06 problem set R1-R3", "course/modules/E/E4/L06.html:596-616", OK,
  "R1 limits: kappa->inf, tau_eta->0, theta_s*->0, Corr^2 = sig_v^2/(sig_v^2+sig_eta^2) -> 0 (checked; Corr^2 formula re-derived). A2 excludes lambda=0 (checked). R2 monotone argument valid (kappa>0). R3 lists the four facts needed; no claim beyond them.")
r("E4b-L06-quiz-q12", "L06 quiz item 12 (probability-one clearing)", "course/modules/E/E4/L06.html:714-722", OK,
  "Correct option: a nonzero linear function vanishes only on a line, which has probability zero under the normal law of (s,u). Explanation at line 721 matches A4 and Step 3.")
r("E4b-L06-A4-section3", "A4 clearing in section 3 proof", "course/modules/E/E4/L06.html:82-86, 194-202", OK,
  "Step 3 at line 202 evaluates at (0,0), (1,0), (0,1); the (0,0) evaluation adds no information (0=0), the other two give the coefficients. Statement is correct; the extra point is harmless.")
r("E4b-L06-quiz-rest", "L06 quiz items 1-11", "course/modules/E/E4/L06.html:644-709", OK,
  "Answers re-checked: theta_s*=3/7 (3/4 over 7/4); kappa=4 at a=2; sig_eta^2=2; the informed-belief correct option; V_I=1/2; sig_eta^2 rises with sig_u^2; x_I=1/7; b=7/9; regression-slope option; Var(v|p)=2/3; exactly one LNREE.")
r("E4b-L06-why-uninformed-trading", "L06 'why uninformed trading' paragraph", "course/modules/E/E4/L06.html:51", OK,
  "Read: the price absorbs supply and does not reveal the payoff exactly; uninformed investors learn through a linear projection; coefficients used by L07. Consistent with sections 2-3.")
r("E4b-L06-dfn-informed-fraction-posterior", "L06 dfn terms (informed fraction, posterior)", "course/modules/E/E4/L06.html:57, 96", OK,
  "Definitions are plain <dfn> with the fraction defined in Def 6.1 (line 57) and posterior at line 96, before first use in Lemma 6.2 (line 99). No data-concept links outside the closure.")
r("E4b-L06-grades", "L06 grades and key results", "course/modules/E/E4/L06.html:621-637", OK,
  "Key results: T for Lemmas 6.3-6.4, Prop 6.7, Cor 6.8 (proved on the page); base values T (exact arithmetic reproduced by Lab Parts A-B); residual zero at 16 points and the nonzero residual at slope 1/2 are C (finite check, Lab Parts C-D); seeded sample slopes are C (SIMULATED, one seed). Consistent with the plan's finite-check rule.")
r("E4b-struct-L06", "L06 structure, order, footer", "course/modules/E/E4/L06.html (sections, order, footer line 739)", OK,
  "Sections 1-9 in order; footer at line 739; nav Previous L05, Next L07 at lines 734-735.")
r("E4b3-L06-A4-linearity", "A4 linearity and the residual", "course/modules/E/E4/L06.html:82-86; tests/labs/E4/lab-E4-L06-1.py:78-106", OK,
  "Residual is linear in (s,u) without a constant term: demands are linear in (s,p) and p is linear in (s,u); verified in the code (residual returns a linear combination, no constant).")
r("E4b3-L06-A2-informed-observe", "A2 informed investors observe s and p", "course/modules/E/E4/L06.html:72, 243-246", OK,
  "A2 (L06.html:72): informed investors observe s and p; uninformed observe p. Lab docstring (243-246) matches.")
r("E4b5-L06-negative-claims", "L06 negative claims (utility, supply, price taking)", "course/modules/E/E4/L06.html:486 (utility), 500 (misconception), 615 (R3 solution)", OK,
  "The CRRA statement (line 486) is hedged ('need not'). Line 500 (misconception 1) and line 615 (R3) claim only what Lemmas 6.3-6.4 need under G, and say the lesson makes no claim about other payoff laws. No overclaim found.")

# ---- hub titles (lines 139-146 of the hub read this round)
r("E4b-hub-titles", "hub lesson titles match lesson pages", "course/modules/E/E4/index.html:144-146 vs L04.html:35, L05.html:35, L06.html:35", OK,
  "Hub: 'L04 · 8 h Complete and Incomplete Markets', 'L05 · 8 h Rational-Expectations Equilibrium', 'L06 · 8 h Noisy rational-expectations equilibrium'. Match the H1 of each lesson.")
r("E4b-page-width-360", "page width at 360 px, no horizontal scroll", "tools/page_smoke.py --unit E4 --pages L04 L05 L06", OK,
  f"page_smoke PASS for all three pages ({S}page_smoke_E4.txt).")
r("E4b-nav-labels", "previous/next lesson labels", "course/modules/E/E4/L04.html:519-520, L05.html:511-512, L06.html:734-735", OK,
  "L04: Previous L03 'The first welfare theorem', Next L05 'Rational-Expectations Equilibrium'. L05: Previous L04 'Complete and Incomplete Markets', Next L06 'Noisy rational-expectations equilibrium'. L06: Previous L05, Next L07 'Price informativeness'. Titles match.")
r("E4b-simulated-labels", "SIMULATED labels on seeded draws", "course/modules/E/E4/L06.html (SIMULATED labels); L04.html and L05.html (no random draws)", OK,
  "L06 Part E labelled SIMULATED in the lab docstring, the printed output and the key-results row; L04 and L05 use no random draws (twin code has no random import; L06 is the only twin with random).")
r("E4b-concept-definitions", "concept definitions and links", "course/modules/E/E4/L04.html:77, 102, 292; L05.html:59, 73; L06.html:57, 67, 96, 169", OK,
  "dfn terms read: L04 'complete' has data-concept market-completeness (E4 concept); CARA and noise traders are plain dfn without data-concept (plan D6, D7). L05 'rational-expectations equilibrium' has data-concept (E4). L06 'noisy REE' has data-concept (E4). No link to an out-of-closure concept.")
r("E4b-notation-registry", "notation registry use in slice", "course/modules/E/E4/L04.html, L05.html, L06.html; notation/notation.json", OK,
  "Registered symbols T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, mathbb Q do not appear in slice math (notation_scan.sh). Registered macros \\E \\R \\Var \\Cov \\Corr \\Normal used with registered meanings. The grade letter 'T' in tables is not the symbol T.")
r("E4b-dag-closure", "DAG: concepts used by name or link within the closure", "L04-L06 text, math and links; curriculum.json", OK,
  "check_dag E4 PASS. Links used: arrow-debreu-security (E4 L01), vector-space and linear-map (M3), market-completeness, rational-expectations-equilibrium, noisy-rational-expectations-equilibrium (E4), crra-utility and expected-utility (E3, in closure), M4 random-variable, expectation, normal-distribution, conditional-expectation-elementary, variance, independence, multivariate-normal, least-squares-projection. 'convex cone', 'CARA', 'noise traders', 'posterior', 'public signal' are plain prose or plain dfn (no curriculum concept). Bayes/S1 not used.")
r("E4b-banned-process-words", "banned process words in learner text (builder, verifier, round, fragment, pin, ledger, twin, architect)", "L04.html:513; L05.html:296; L06.html:728; cards.json", "FAIL",
  "Learner text contains the reader-facing bookkeeping term 'registry' at three places: L04.html:513 ('This lesson cites no registry source.'), L05.html:296 ('That registry record is used for the title only.'), L06.html:728 ('This lesson cites no registry source.'). The same template phrase appears on other course pages (PC3, SC1, AC1), so this is a house-wide wording question; no other banned word found in the slice. Found this round; the round-7 PASS on this row was wrong.",
  "Replace the three sentences with plain wording, e.g. 'This lesson cites no source.' (L04.html:513, L06.html:728) and 'Muth's title is the only part of that work used here, and no result of the paper is used.' (L05.html:296). Architect to decide whether the house template changes on all units.")
r("E4b7-scan-process-banned", "process-word scan of L04-L06 pages and cards (round-7 scan)", "L04.html, L05.html, L06.html, cards.json", "FAIL",
  "Same finding as E4b-banned-process-words: the round-7 scan missed 'registry' (scan_list did not include it). Confirmed this round by notation_scan.sh (process-word section): L04 line 513, L05 line 296, L06 line 728, and cards.json line 753 (E4-c099 front).",
  "Apply the fix in E4b-banned-process-words and add 'registry' to the scan list if the architect rules it a process word.")
r("E4b-cmd-page_smoke-alone", "page_smoke run alone", "tools/page_smoke.py", OK, f"Re-run alone: 'page_smoke E4: PASS' ({S}page_smoke_E4.txt).") if False else None

# ---- cards (all 91 slice cards read this round)
r("E4b4-cards-L04-L06", "cards.json: all slice cards agree with the current lesson text", "course/modules/E/E4/cards.json: L04 30, L05 28, L06 33 cards", OK,
  "All 91 slice cards read this round against the lesson text. The round-7 count 'L04 27' is stale: E4-c234, c235, c236 were added after 06994db; L04 now has 30 cards. Checked against L04.html:58-60 (A1-A3), 278-279 (A4), and the proposition statements.")
r("E4b4-grade-legend-variant", "grade legend variant (C = single study or finite check)", "course/modules/E/E4/L04.html:42-49; L05.html:42-49; L06.html:42-49", OK,
  "Legend identical across the three pages. The C definition extends BLUEPRINT's 'single-sample evidence' to 'finite check', as the plan's finite-enumeration rule allows (plan line 217).")
r("E4b4-notation-eta", "notation: eta, tau, kappa in Prop 6.7 and Corollary 6.8", "course/modules/E/E4/L06.html:179-235 (eta in Prop 6.7, Step 2 line 193, Cor 6.8, Remark 6.10)", OK,
  "eta is local to L06 (noise in Y=v+eta); not a registry symbol. kappa, tau, sig_eta used consistently with Def in Prop 6.7.")
r("E4b4-notation-s", "notation: s (signal) in L04", "course/modules/E/E4/L04.html (all); L06.html:57", OK,
  "L04 uses S for the number of states (not the signal); L06 uses s for the signal; no reuse conflict within a lesson.")
r("E4b4-notation-x", "notation: x for portfolio and demand", "course/modules/E/E4/L04.html (all); L06.html:66, 82, 162, 169, 192, 230, 682", OK,
  "L04 math uses zeta (portfolios) and xi (payoffs); the lowercase x in L04 occurs only inside the embedded code block. L06 uses x for the risky holding (Def 6.2). No registry conflict.")
r("E4b5-hub-lede-lesson-map", "hub lesson-map lede vs lessons", "course/modules/E/E4/index.html:139-146", OK,
  "Read hub lines 139-146: 'Nine lessons of eight study hours each, which is 72 hours in total'. L04-L06 each 8 h. Lesson map consistent with lesson pages.")
r("E4b6-delta-review", "delta since previous pin in slice", "git diff 06994db..0dee921a for L04-L06, twins, cards", OK,
  "Slice HTML and twins are byte-identical since 06994db (git diff empty). Only cards.json changed for slice cards (E4-c053, c055, c114, c218, c228 text; c234, c235, c236 new). All re-read this round.")
r("E4b6-cards-changed", "cards changed in the slice (round-6 to round-7 delta)", "course/modules/E/E4/cards.json: E4-c086, c107, c121, c123, c218", OK,
  "Each re-read this round: c086 (Lemma 3.1 error recursion, matches L05.html:103-105), c107 (probability-one clearing, matches L06.html:82-86 and quiz 714-721), c121 (Remark 6.10), c123 (residual -9/85, verified), c218 (kernel dimension J-rank(A) matches L04.html:271).")
r("E4b6-in-general-scan", "general scan of slice for scope words and sign errors", "course/modules/E/E4/L04.html:271, 386; course/modules/E/E4/L05.html:292", OK,
  "Scope words (only, all, every, always, exactly, any, same) scanned in the three pages: each use is a stated result or a definition (e.g. 'every attainable payoff' with nonzero kernel; 'exactly one' from Prop 2.2). No unsupported scope found.")
r("E4b7-cards-changed", "cards changed in the round-7 delta (slice)", "course/modules/E/E4/cards.json: E4-c065, c090, c094, c103, c104, c120, c122, c124, c125, c219", OK,
  "Each re-read this round against its lesson text (c065 augmented ranks 2,3,3 match Lab Part C; c090/c094 match Lab Parts A and E; c103/c104 match Def 6.2 and A2; c120/c122/c124/c125 match Lab Parts C and E; c219 matches Lab Part C).")
r("E4b7-cards-new", "cards new in the slice", "course/modules/E/E4/cards.json: E4-c226, c227, c228 (L04); c229 (L05); c230, c231 (L06)", OK,
  "Read this round. c226 augmented rank (Prop 1.5); c227 echelon form and pivot (Lemma 2.1); c228 convex cone (Prop 4.2); c229 public signal (A2, A3); c230 signal (Def 6.1); c231 posterior (L06 line 96). Each matches its lesson.")
r("E4b7-twin-lab-L04-L06-hunks", "twin hunks in the slice", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", OK,
  "Twins are byte-identical since 4bd8cb9 (git diff --stat empty for these files). No new hunk to review.")
r("E4b7-struct-delta-prose-only", "structure of changed prose lines", "course/modules/E/E4/L04.html, L05.html, L06.html (headings, section tags, footers)", OK,
  "Headings, section numbering and footers are unchanged; the changed lines in the delta are paragraph bodies (read this round).")

# ---- round-8 new rows
r("E4b8-indep-rederive-L04", "independent re-derivation of L04 numbers (minors, not elimination)", "ledgers/E4/scripts/E4-b-r8/indep_rederive.py; outputs/indep_rederive.txt", OK,
  "Rank 2 (incomplete) and 3 (complete) by maximal nonzero minor; augmented ranks (1,2,3):2, (0,0,1):3, (5,0,0):3 for incomplete and 3 for all three in complete; M1 rank 1, M3 rank 2, E3 rank 2, Misc2 rank 2, Remark 3.2 kernel dim 1. All match the printed output at L04.html:243-258.")
r("E4b8-indep-rederive-L05", "independent re-derivation of L05 numbers (closed form vs iteration)", "outputs/indep_rederive.txt L05 section", OK,
  "c* = (4,-3/10), (5/2,-3/16), (2,-3/20); iteration paths and error ratios -1/4, -1, -3/2 match the printed lab; psi(c*)=c* for all three; damped weight 4/5 gives c* exactly.")
r("E4b8-indep-rederive-L06", "independent re-derivation of L06 numbers (Gaussian conditioning)", "outputs/indep_rederive.txt L06 section", OK,
  "kappa=2, sig_eta^2=2, tau_eta=1/2, taubar=3/4, theta=(3/7,6/7); Var(p)=27/49, Cov=3/7, slope 7/9, posterior 2/3, rho^2 1/3; 16/16 grid residuals zero; residual at (1,0) with theta_s=1/2 is -9/85; M1 instance kappa 4, sig_eta^2 5, tau_eta 1/5, taubar 3/5, theta (3/8, 3/2). Part E numbers verified by the printed tolerance arithmetic (E2 of L06).")
r("E4b8-cards-L04-read", "all 30 L04 cards read against the lesson", "course/modules/E/E4/cards.json (L04)", OK,
  "Read this round. New cards E4-c234 (A1 text = L04.html:58), c235 (A2 = L04.html:59), c236 (A4 = L04.html:278-279) match. Cards with 'Assume A1 to A3' etc. carry the assumption they use. No duplicate fronts (cards_scan.txt).")
r("E4b8-cards-L05-read", "all 28 L05 cards read against the lesson", "course/modules/E/E4/cards.json (L05)", OK,
  "Read this round. c091-c093 ratios and paths match Lab Parts B-D; c094 damped step (4,-3/10); c095 Remark 4.1; c096-c098 misconceptions; c219 fixed point (5/2,-3/16) matches Lab Part C. Cards grade T with lab basis: the basis names the lab and Lemma 3.1 backs the general claim.")
r("E4b8-cards-L06-read", "all 33 L06 cards read against the lesson", "course/modules/E/E4/cards.json (L06)", OK,
  "Read this round. c114 closed form (L06.html:176-185, incl. tau_eta = 1/sig_eta^2), c115 uniqueness steps, c118-c120 base values, c122 16 grid points, c123 -9/85, c124/c125 SIMULATED sample values match Lab Part E printed output, c220 x_U=-1/7 (checked), c230 signal, c231 posterior.")
r("E4b8-cards-scan", "card scan: ids, fronts, lesson membership, numbered references", "ledgers/E4/scripts/E4-b-r8/cards_scan.py; outputs/cards_scan.txt", OK,
  "232 cards, no duplicate ids or fronts. Eight refs flagged: L04 'Assumption A1/A2/A3', L05 'Assumption A1/A2/A3' (the page labels these items 'A1 (...)' under 'Assumptions', so the scan's literal pattern misses them; the cited assumptions exist at L04.html:58-60 and L05.html:58-60); L09 'Problem Res 1/3' and E4-c233 (outside slice b).")
r("E4b8-card-c099-registry", "card E4-c099 learner wording (registry key)", "course/modules/E/E4/cards.json: E4-c099 front (line 753)", "FAIL",
  "Front reads 'Which registry key does L05 cite, and what is it used for?'. 'Registry key' is internal bookkeeping vocabulary in a learner card; the card's content (muth1961rational, title use only) is correct.",
  "Rewrite the front as 'Which source does L05 cite, and for what purpose?' with the same back text (the back names the title only and is correct).")
r("E4b8-notation-registry-symbols", "registry symbols absent from slice math", "L04.html, L05.html, L06.html (math); notation/notation.json", OK,
  "notation_scan.sh: no mathbb, no Phi, gamma_3/4, R^ast, R^{e ast}, R_f or mathbb Q in slice math; T only as the grade letter. Registered macros used as registered.")
r("E4b8-hours", "hours arithmetic: lesson hours vs hub split", "course/modules/E/E4/L04.html:34, L05.html:34, L06.html:34; index.html:139 (72 h), index.html:31 (100 h)", OK,
  "Each slice lesson states 8 study hours; nine lessons x 8 h = 72 h as the hub states; module 100 h (curriculum/02-economics-finance-core.yaml hours 100). Arithmetic consistent.")
r("E4b8-plan-L04-efficiency", "plan ruling: no unproved efficiency claim for incomplete markets", "course/modules/E/E4/L04.html:288; plans/E4-build-plan.md §7 (line 691, §12 Q18)", OK,
  "L04.html:288: 'The lesson does not state whether equilibrium allocations are efficient in an incomplete market, and no such claim is made here.' Consistent with the plan's recommendation to remove the claim.")
r("E4b8-plan-L05-muth", "plan ruling: Muth (1961) cited at paper level, no empirical claim", "course/modules/E/E4/L05.html:296; plans/E4-build-plan.md lines 98, 283-285", OK,
  "L05 cites muth1961rational at title level only and states no empirical claim about rational expectations. Consistent with plan lines 283-285.")
r("E4b8-plan-L06-muth", "plan line 586: muth1961rational on L05 and L06 for an attributed claim", "course/modules/E/E4/L06.html (no data-cite); plans/E4-build-plan.md lines 537, 586", OK,
  "Note, not a claim defect: the plan asks for the Muth key on L06 only where L06 makes an attributed claim. L06 makes no Muth-attributed claim (its 'References' section says it cites no source). Architect may want a paper-level citation there; no L06 result depends on it.")
r("E4b8-lab-docstring-code", "lab docstrings and in-code claims vs code and output", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py (module docstrings and rank/show/residual functions)", OK,
  "L04 rank docstring (pivots, above and below elimination) matches the code; Part list matches output. L05 check_params call order and 'exact Fractions' statement match code. L06 residual docstring matches code. L06 Part B docstring 'computed from the moments' is accurate for slope and posterior (the closed-form theta enters only as the input to Var(p)).")
r("E4b8-scope-words", "scope words (only, all, every, always, exactly, any, same) in slice prose", "L04.html, L05.html, L06.html", OK,
  "Each occurrence checked: 'every attainable payoff' (L04.html:271, nonzero kernel); 'exactly one' (L05 Prop 2.2, Remark 4.1); 'every real z' (Def 1.2); 'only when' (L05 line 51, 294, Prop 3.2 agrees); 'exactly one' (L06 quiz, Prop 6.7(b)) and 'every real z' (L05 Def 1.2). No unsupported scope.")
r("E4b8-terms-before-definition", "terms used before definition", "L04.html, L05.html, L06.html", OK,
  "'payoff matrix', 'attainable', 'rank' defined in Defs 1.1 and 1.3 before theorem use; 'augmented rank', 'echelon form', 'pivot' defined before Lemma 2.1 use; L05 'affine' (A2), 'damped step' (Prop 3.3 before Lab 1); L06 'noise trader', 'precisions', 'signal', 'informed fraction' (Def 6.1), 'posterior' (L06.html:96 before Lemma 6.2), 'CARA' (Def 6.2, forward reference in Def 6.1 flagged as such). No undefined term found.")
r("E4b8-quiz-answers", "quiz answers in slice", "L04.html:441-508; L05.html:437-500; L06.html:640-721", OK,
  "Every correct option and explanation re-checked this round (see E4b-L04-quiz-rest, E4b-L05-quiz, E4b-L06-quiz-rest).")
r("E4b8-L06-R1-limit", "L06 R1 'what the limit means for the price'", "course/modules/E/E4/L06.html:598-601", OK,
  "The solution shows kappa->inf, tau_eta->0, theta_s*->0, Corr^2->0 and states that the correlation between payoff and price tends to zero (the price stops transmitting the signal). The limit lies outside A2 (lambda in (0,1)). Answers the question as asked.")
r("E4b8-L06-step3-redundant-point", "L06 Step 3 evaluates the residual at (0,0), (1,0), (0,1)", "course/modules/E/E4/L06.html:202", OK,
  "The (0,0) evaluation gives 0=0 and adds nothing; the two other points give Q theta_s=lambda tau_eps and Q theta_u=a. Statement is still correct; noted only.")
r("E4b8-process-words-hub-note", "process words in slice pages besides 'registry'", "L04.html, L05.html, L06.html, cards.json (builder, verifier, round, fragment, pin, ledger, twin, architect, plan, mutant)", OK,
  "No hit for builder, verifier, round, fragment, pin, ledger, twin, architect, plan or mutant in learner text (notation_scan.sh process-word section lists only 'registry').")


r("E4b3-L04-footer", "L04 footer", "course/modules/E/E4/L04.html:524", OK,
  "Footer 'E4 · General Equilibrium & Information in Markets · Each graded result carries a proof or a lab result.' present at the end of the page (grep, line 524).")
r("E4b4-independent-checks", "round-6 independent checks re-derived", "ledgers/E4/scripts/E4-b-r8/indep_rederive.py; outputs/indep_rederive.txt", OK,
  "The round-6 script was not relied upon. This round's own script recomputes every number the round-6 row covered (L04 ranks, L05 fixed points and ratios, L06 closed form, residual -9/85, grid zeros, M1 instance, Var(p), slope, posterior, correlation). All agree with the printed lab output.")

# ---- drop out-of-slice row
# E4b3-hub-pq3 (index.html:81-84, hub quiz item) is outside slice b (hub belongs to slice a) and was not re-verified here.

assert len({r_["id"] for r_ in rows}) == len(rows), "duplicate ids"
for row in rows:
    assert row["status"] in {"PASS", "FAIL", "UNVERIFIABLE"}
    if row["status"] != "PASS":
        assert row.get("fix")
n_pass = sum(1 for x in rows if x["status"] == "PASS")
n_fail = sum(1 for x in rows if x["status"] == "FAIL")
frag = {
    "unit": "E4",
    "slice": "b",
    "round": 8,
    "verifier": "Haiku independent verifier, E4-b round 8 (did not build E4)",
    "pin": "0dee921a (detached at this pin)",
    "base": "06994db1 (round-7 pin); round-7 fragment /Users/billyribeiro/.fanout/frags/E-E4-b.round7.json, context only, its PASS rows were not trusted",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE8-E4-b",
    "scratch": "ledgers/E4/scripts/E4-b-r8/ (run_gates.sh, expected_vs_output.py, strip_view.py, cards_scan.py, notation_scan.sh, indep_rederive.py, write_fragment.py, outputs/)",
    "verified_at": datetime.now(UTC).date().isoformat(),
    "verdict": "FAIL" if n_fail else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b is L04 to L06 and their three lab twins. Not a project slice: no grader mutants or alternatives are written here.",
        "Mutation testing: not applicable to lab twins (verifier rules ruling). Ten-mutant and five-alternative duties belong to the project slice.",
        "Slice HTML, twins and cards.json for L04 to L06 were re-read in full this round. The only delta since 06994db for the slice is cards.json (E4-c053, c055, c114, c218, c228 text; c234, c235, c236 new).",
        "Round-7 PASS rows were not carried; each row was re-verified this round from the current bytes. One round-7 row (E4b3-hub-pq3, hub quiz item at index.html:81-84) is outside slice b and was dropped from this fragment, not carried.",
        "One finding, three FAIL rows, all process-word wording: 'registry' in learner text at L04.html:513, L05.html:296, L06.html:728 and card E4-c099. The phrase is a house template on other course pages, so the architect should rule on it.",
        "Plan-conformance note (not a row FAIL): plan line 586 asks for muth1961rational on L06 when an attributed claim is made; L06 makes none.",
    ],
    "summary": f"{'FAIL' if n_fail else 'PASS'} E4-b round 8: rows={len(rows)} (pass={n_pass}, fail={n_fail}, unverifiable=0). Targeted gates re-run at 0dee921a: all PASS. Three FAIL rows, one finding: 'registry' wording in learner text (L04.html:513, L05.html:296, L06.html:728) and card E4-c099 front.",
}
out = "ledgers/E4/E4-b.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(frag, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("wrote", out, "rows", len(rows), "pass", n_pass, "fail", n_fail)
