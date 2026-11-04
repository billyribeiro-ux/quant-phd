import json, sys
sys.path.insert(0, 'tools')
import ledger

OUT = 'ledgers/E4/scripts/E4-b-r2/outputs'
C = 'Carried from round 1 (course/modules/E/E4/L04.html, L05.html, L06.html byte-identical since the previous pin 1c1645f3; no hunk of 1c1645f3..67c47689 touches the cited lines, see scripts/E4-b-r2/changed_hunks_new_side.diff):'
RR = 'Re-verified in round 2 from scratch: '

rows = {}
def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    rows[rid] = r

# commands (re-run on pin 67c47689)
row("E4b-cmd-check_pages", "tools/check_pages.py --unit E4", "course/modules/E/E4/L04.html, L05.html, L06.html", "PASS",
    f"Re-run: check_pages E4: PASS, exit 0 ({OUT}/check_pages.txt).")
row("E4b-cmd-check_dag", "tools/check_dag.py --unit E4", "E4 DAG (L04-L06 links)", "PASS",
    f"Re-run: check_dag E4: PASS, exit 0 ({OUT}/check_dag.txt).")
row("E4b-cmd-check_projects", "tools/check_projects.py --unit E4", "E4 project (out of slice, unit gate)", "PASS",
    f"Re-run: check_projects E4: PASS, exit 0 ({OUT}/check_projects.txt).")
row("E4b-cmd-run_labs", "tools/run_labs.py --unit E4 (and --page L04, L05, L06)", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", "PASS",
    f"Re-run: run_labs E4: PASS (12/12) ({OUT}/run_labs_unit.txt); per page L04, L05, L06 each PASS (1/1) ({OUT}/run_labs_L04.txt, run_labs_L05.txt, run_labs_L06.txt).")
row("E4b-cmd-twins-isolated", "python -I -W error on each twin", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", "PASS",
    f"Re-run: exit 0 for all three; stderr 0 bytes for each ({OUT}/twin_L04.err, twin_L05.err, twin_L06.err). Outputs in twin_L0x.out.")
row("E4b-cmd-page-code-equals-twin", "page lab code byte-identical to twin", "course/modules/E/E4/L04.html:120-240, L05.html:123-252, L06.html:239-452", "PASS",
    f"run_labs (byte-identity is part of its check) PASS for L04, L05, L06 at 67c47689 ({OUT}/run_labs_L0x.txt). The L06 units docstring was edited on both sides and still matches, so the failure is in the text, not the embed.")
row("E4b-cmd-expected-equals-output", "page expected block equals twin output", "course/modules/E/E4/L04.html:242-258, L05.html:254-279, L06.html:454-472", "PASS",
    f"run_labs PASS for L04, L05, L06 (numbers within tolerance, other tokens exact). Output of each twin compared to its expected block ({OUT}/twin_L0x.out).")
row("E4b-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on the three twins", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", "PASS",
    f"ruff check: exit 0; ruff format --check: 3 files already formatted; mypy --no-incremental: Success, no issues in 3 source files ({OUT}/ruff.txt, mypy.txt).")
row("E4b-cmd-pytest-labs", "pytest tests/test_labs.py tests/test_run_labs.py -k 'E4 or L04 or L05 or L06'", "tests/test_labs.py, tests/test_run_labs.py", "PASS",
    f"Re-run: exit 0 ({OUT}/pytest_labs_E4.txt). test_labs.py collects 359 tests; subset run covers E4 labs.")
row("E4b-cmd-page_smoke", "tools/page_smoke.py --unit E4 --pages L04 L05 L06", "course/modules/E/E4/L04.html, L05.html, L06.html", "PASS",
    f"Re-run: page_smoke modules/E/E4/L04.html, L05.html, L06.html: PASS each; page_smoke E4: PASS, exit 0 ({OUT}/page_smoke_L04-06.txt).")
row("E4b-cmd-verify_refs-live", "tools/verify_refs.py (offline run this round; live run not repeated)", "references/references.json (muth1961rational, mascolell1995microeconomic, milgrom1982information; used_by E4)", "PASS",
    f"Re-run offline: 'offline integrity: 560 entries, 0 problems', exit 0 ({OUT}/verify_refs_offline.txt). Live run not repeated: git diff 1c1645f3..67c47689 -- references/ is empty (0 lines), so the round-1 live result (muth1961rational title, verified_by crossref) still holds. Muth title re-read in references/references.json: 'Rational Expectations and the Theory of Price Movements'.")

# lab twins and labs
row("E4b-lab-L04-1", "Lab 1 of L04: twin reads, runs, output matches", "course/modules/E/E4/L04.html:117-260", "PASS",
    RR + "twin re-read (line 123 docstring change 'one common payoff unit' is accurate: whole-number entries); run_labs and twin isolation PASS; printed Parts A-E re-derived in ledgers/E4/scripts/E4-b-r2/independent_checks.py (rank 2 and 3, attainability verdicts, redundancy weights 1,2,3).")
row("E4b-lab-L05-1", "Lab 1 of L05: twin reads, runs, output matches, statements about it", "course/modules/E/E4/L05.html:120-281", "PASS",
    RR + "after the gamma -> varsigma rename, the twin and page are consistent (grep: no gamma/lambda left in L05 page or twin). Every printed value (fixed point (4,-3/10), error ratios -1/4, -1, -3/2, path 0,5 alternation, damped weight 4/5, identities True) matches an independent Fraction re-derivation (independent_checks.py, all PASS). Interpretation paragraph (L05.html:281) matches the printed lines and the stated scope.")
row("E4b-lab-L06-1-outputs", "Lab 1 of L06: printed outputs equal the expected block and the text about them", "course/modules/E/E4/L06.html:236-474", "PASS",
    RR + "run_labs PASS and twin isolation PASS. Printed values (kappa 2, sig_eta2 2, tau_eta 1/2, tau_bar 3/4, theta_s 3/7, theta_u 6/7, var_p 27/49, cov 3/7, slope 7/9, posterior var 2/3, rho^2 1/3, 16/16 zero residuals, informed demand 1/7, alt residual -9/85, sample slopes within tolerance) re-derived in independent_checks.py (PASS). Interpretation paragraph (L06.html:473) matches output.")
row("E4b-lab-L06-1-units", "L06 lab docstring units statement is dimensionally consistent with the model", "tests/labs/E4/lab-E4-L06-1.py:17-20 and course/modules/E/E4/L06.html:257-260", "FAIL",
    "Round-2 text says 'The coefficients kappa and theta_u have units of price per unit of the asset, because theta_u * u is a price.' With s and p in price per unit of the asset and u in units of the asset (the page's own convention), Y = p/theta_s = s - kappa*u forces kappa in (price per unit asset)/(asset) = price per unit of asset SQUARED; theta_u * u is a price per unit of asset, so theta_u is likewise price per unit of asset squared. Independent exponent check in independent_checks.py: kappa = a*sig_e2/lam has exponents P^1 Q^-2 (a in 1/P from CARA utility, sig_e2 in (P/Q)^2), printed as FAIL-by-docstring. The variance clause 'squared price units' is ambiguous for the same reason.",
    fix="Replace the sentence at lab-E4-L06-1.py:17-20 and at L06.html:257-260 with: 'The coefficients kappa and theta_u have units of price per unit of the asset squared, because kappa times u and theta_u times u are prices per unit of the asset and u is in units of the asset; theta_s is dimensionless.' Also say the variances are in squared price-per-asset units. Edit the twin, then run tools/embed_labs.py L06.html --refresh lab-E4-L06-1 and re-run run_labs --page L06.")
row("E4b-lab-L06-1-residual-docstring", "residual() docstring matches its formulas", "tests/labs/E4/lab-E4-L06-1.py:88-89 (page L06.html:326-327)", "PASS",
    RR + "docstring now says E[v|s,p] = omega*s with omega = sig_v2/(sig_v2+sig_e2) and Var(v|s,p) = V_I (Lemma 6.3, any price coefficients). Lemma 6.3 proof uses only that p is a function of (s,u), which holds for any theta_s, theta_u, so the claim is correct; code lines 88-106 use exactly these formulas.")
row("E4b-lab-L06-1-hypothesis-xref", "hypothesis paragraph cross-references and values", "course/modules/E/E4/L06.html:238", "PASS",
    RR + "the hypothesis now names 'Part C, with A4 and Proposition 6.7' and 'An alternative price coefficient theta_s = 1/2' (Part D uses ALT_SLOPE = 1/2 for theta_s and holds theta_u): residual -9/85 at (1,0) confirmed. Other values (kappa 2, sig_eta2 2, tau_eta 1/2, tau_bar 3/4, theta 3/7 and 6/7, slope 7/9, posterior var 2/3, 16 grid points) confirmed.")

# L04 math
row("E4b-L04-math-sec1", "Section 1 definitions, A1-A3, Definition 1.3, Lemma 1.2", "course/modules/E/E4/L04.html:64-96", "PASS",
    C + " Lemma 1.2 and Definition 1.3 re-read; Lemma 1.2 proof is correct (linear image, theta^T A = sum of rows).")
row("E4b-L04-math-lemma21", "Lemma 2.1 (elimination counts the rank)", "course/modules/E/E4/L04.html:100-104", "PASS",
    C + " Proof re-read: pivot argument (smallest index with c_i != 0; column p_i) is valid.")
row("E4b-L04-math-examples", "Examples 2.2 and 2.3", "course/modules/E/E4/L04.html:106-115", "PASS",
    C + " Example 2.2: (1,2,3) = r1 + r2 and (0,0,1) not attainable (rank 3 vs 2) re-derived; Example 2.3 r4 = 1*e1 + 2*e2 + 3*e3 checked exactly.")
row("E4b-L04-math-remark31", "Remark 3.1 (one security per state)", "course/modules/E/E4/L04.html:264-267", "PASS",
    C + " theta = x satisfies theta^T I_S = x; rank(I_S) = S.")
row("E4b-L04-math-remark32", "Remark 3.2 (redundancy and the kernel)", "course/modules/E/E4/L04.html:270-271", "PASS",
    RR + "the round-1 FAIL (unproved 'in general' claim) is fixed: theta -> theta^T A has rank rank(A), rank-nullity gives kernel dim J - rank(A) = 1 here (independent_checks.py 'rank-nullity kernel dim = 1'); a nonzero kernel makes every attainable payoff replicated by a translate, so payoffs do not determine portfolios. Family (1-t, 2-2t, 3-3t, t) replicates (1,2,3) for t = 0, 1, -3, 7/5 (exact).")
row("E4b-L04-math-sec4", "Section 4: Assumption A4, Proposition 4.1, Proposition 4.2", "course/modules/E/E4/L04.html:278-294", "PASS",
    C + " Proposition 4.1 proof re-read: J+1 indicator functions independent, dimension of M(A) at most J. Proposition 4.2: C(I_2) = nonnegative quadrant, (-1,0) attainable under A3 only.")
row("E4b-L04-misconceptions", "Misconceptions section (L04)", "course/modules/E/E4/L04.html:297-317", "PASS",
    C + " Content unchanged; statements re-read against Theorem 1.4 and Proposition 1.5.")
row("E4b-L04-problems", "Problem set (L04), changed items re-verified", "course/modules/E/E4/L04.html:319-421", "PASS",
    RR + "E2 solution (L04.html:386) now gives theta = (1-t, 2-2t, 3-3t, t) for every real t; checked exactly. Unchanged problems re-read and consistent with Theorem 1.4 and Corollary 1.6.")
row("E4b-L04-quiz-q4", "Quiz item L04q4 (portfolios replicating (1,2,3))", "course/modules/E/E4/L04.html:467-475", "PASS",
    RR + "keyed option 'The family (1-t, 2-2t, 3-3t, t) for every real t' is the complete replicating set (verified exact, t = 0,1,-3,7/5); distractors 'Only (1,2,3,0)' and 'Exactly the two portfolios' are wrong (infinitely many); explanation consistent with Remark 3.2.")
row("E4b-L04-quiz-rest", "Quiz items L04q1-q8, changed and unchanged", "course/modules/E/E4/L04.html:441-508", "PASS",
    RR + "q1 keyed rank(A)=S (Theorem 1.4); q2 keyed five (Corollary 1.6, I_5 by Remark 3.1); q5 keyed rank([A;x])=rank(A) (Proposition 1.5); q7 keyed 'incomplete for every finite set' (Proposition 4.1); q8 keyed 'No' under theta>=0 with A=I_2 (Proposition 4.2). Unchanged q3 (rank 1) and q6 re-read. All keyed answers match the proofs.")
row("E4b-L04-why-empirical", "why-it-matters (L04) claims", "course/modules/E/E4/L04.html:51", "PASS",
    RR + "the sentence 'Real markets trade fewer securities than there are states' is removed and replaced with 'In the model of this lesson, whether a payoff can be bought depends on the rank...'. The remaining claims (exact test, no tolerance in verdict, last section on infinite states) match Theorem 1.4 and Proposition 4.1.")
row("E4b-grades-L04", "L04 grades and theorem titles", "course/modules/E/E4/L04.html:429-436 and 81-96", "PASS",
    C + " Grade T on Theorem 1.4, Proposition 1.5, Corollary 1.6, Proposition 4.1 and 4.2 matches the proofs given.")
row("E4b-struct-L04", "L04 structure, nav, header", "course/modules/E/E4/L04.html:2, 34-520", "PASS",
    RR + "header and section order unchanged; nav 'Next: Rational-Expectations Equilibrium' matches L05.html:35 h1 exactly.")

# L05
row("E4b-L05-math-sec1-2", "L05 Section 1-2: A1-A3, Definitions 1.1-1.2, Lemma 2.1, Proposition 2.2", "course/modules/E/E4/L05.html:64-98", "PASS",
    RR + "after the rename gamma -> varsigma and the supply relabel (q = varsigma m(z) + delta z + eta), Lemma 2.1 formula E[p|z] = (alpha - varsigma(c0+c1 z) - delta z)/beta and its conditional variance (sig_u^2+sig_eta^2)/beta^2 re-derived. Proposition 2.2 fixed point c0* = alpha/(beta+varsigma), c1* = -delta/(beta+varsigma) re-derived (independent_checks.py, 200 random parameter draws). Definition 1.2 defines the REE before use.")
row("E4b-L05-math-sec3", "L05 Section 3: Lemma 3.1 (error recursion)", "course/modules/E/E4/L05.html:102-118", "PASS",
    RR + "e_{k+1} = -(varsigma/beta) e_k for both components, re-derived exactly; base ratio -1/4, equal case -1, large case -3/2 (independent_checks.py).")
row("E4b-L05-prop32", "Proposition 3.2 (when iteration converges)", "course/modules/E/E4/L05.html:108-112", "PASS",
    RR + "statement and proof correct: converges from every start if varsigma < beta; if varsigma >= beta the error does not vanish (equal case alternates, large case grows).")
row("E4b-L05-sec5-wording", "L05 Section 5 wording about convergence", "course/modules/E/E4/L05.html:293", "PASS",
    RR + "'converges from every starting point only when varsigma < beta' is exactly the contrapositive of Proposition 3.2 (varsigma >= beta gives a starting point that fails).")
row("E4b-L05-prop34-remark41", "Proposition 3.4 slot and Remark 4.1 wording", "course/modules/E/E4/L05.html:284-287", "PASS",
    C + " Remark 4.1 read: Proposition 2.2 shows exactly one equilibrium in the affine family; does not exclude non-affine ones.")
row("E4b-L05-notation-gamma", "gamma no longer used for supply response (notation)", "course/modules/E/E4/L05.html:66-68, 111 and tests/labs/E4/lab-E4-L05-1.py", "PASS",
    RR + "grep finds no gamma and no lambda in L05 page or twin; supply response is varsigma, defined in Definition 1.1 ('The parameter varsigma is the supply response') and in A1. Registry (notation/notation.json) contains no varsigma, gamma (plain) or nu symbol, so no registry collision; the emgamma macro is unused here.")
row("E4b-L05-notation-s", "symbol s not reused with another meaning (L05 vs L06)", "course/modules/E/E4/L05.html:66 (supply q), L06.html:57 (signal s)", "PASS",
    RR + "L05 supply is now q, so s is not used in L05 for supply; L06 s = v + eps is local to L06 and defined there (Definition 6.1). No registry symbol s.")
row("E4b-L05-muth-markup", "attribution claim about Muth (1961) title", "course/modules/E/E4/L05.html:295", "PASS",
    RR + "the sentence is now a graded T claim with data-cite=muth1961rational and data-locator=title. The registry record (references/references.json, key muth1961rational, verified_by crossref) has title 'Rational Expectations and the Theory of Price Movements', so the phrase 'rational expectations' is in the title as stated.")
row("E4b-L05-math-muth-scope", "scope of the Muth claim (no result used)", "course/modules/E/E4/L05.html:295", "PASS",
    RR + "'That registry record is used for the title only... no result of that paper is used or reproduced' matches the page's content (no result of Muth is stated or proved).")
row("E4b-L05-misconceptions", "L05 misconceptions", "course/modules/E/E4/L05.html:298-314", "PASS",
    RR + "Misconception 1 cites Lab 1 Part C (c0* = 5/2, alternating 0 and 5), correct. Misconception 2: unconditional mean of p is c0* because E z = E u = E eta = 0 (A3), correct; c1* = -delta/(beta+varsigma) = -3/10 at base, as printed.")
row("E4b-L05-problems", "L05 problem set, changed items", "course/modules/E/E4/L05.html:316-419", "PASS",
    RR + "M1 (c0*=3, c1*=-1/2 at alpha 12, beta 3, varsigma 1, delta 2) and M2 (Psi(0,0)=(4,-2/3), error ratios -1/3) re-derived; P1, P2 (uniqueness (beta+varsigma)c = ...), P3 (error recursion); E2 (c0 path stays put at 5/2), E3 (c0 path 0,5,-5/2,35/4; errors -2,3,-9/2,27/4; ratio -3/2); R1 (weight 1/2, one step to 5/2); R2 (delta=0 gives c1*=0); R3 all re-derived exactly.")
row("E4b-L05-quiz", "L05 quiz, changed and unchanged items", "course/modules/E/E4/L05.html:437-500", "PASS",
    RR + "q1 keyed alpha/(beta+varsigma); q2 numeric 4 (10/(2+1/2)); q3 keyed varsigma<beta; q4 numeric -1/4; q5 keyed 'size stays the same, sign alternates'; q6 keyed nu = beta/(beta+varsigma) and explanation 1-nu(1+varsigma/beta); q7 numeric 1.25 = (4+1)/4; q8 keyed c0* constant when delta = 0. All consistent with proofs.")
row("E4b-grades-L05", "L05 key-results grades", "course/modules/E/E4/L05.html:423-432", "PASS",
    RR + "each T row (Lemma 2.1, Proposition 2.2, Corollary 2.3, Lemma 3.1, Proposition 3.2, Proposition 3.3, base-instance row) is proved on the page or read off Lab 1 Parts A-B exactly; no C or D row needed.")
row("E4b-struct-L05", "L05 structure and nav", "course/modules/E/E4/L05.html:2, 34-516", "PASS",
    RR + "nav Previous 'Complete and Incomplete Markets' matches L04.html:35 h1; Next 'Noisy rational-expectations equilibrium' matches L06.html:35 h1 exactly.")

# L06
row("E4b-L06-math-model", "L06 Section 1: Definitions 6.1-6.2, A1-A4, Assumption G", "course/modules/E/E4/L06.html:55-92", "PASS",
    RR + "A4 'Clearing is required at each pair (s,u)' is correct; its sentence 'clearing with probability one forces the same coefficients (Section 3, after Proposition 6.7)' has a dangling pointer, graded as its own FAIL row (E4b-L06-A4-section3). Definition 6.1 'informed fraction' now defined in place (L06.html:57). G states both facts used (linear image jointly normal; uncorrelated -> independent), both standard.")
row("E4b-L06-lemma62", "Lemma 6.2 (CARA demand under normal beliefs), proof", "course/modules/E/E4/L06.html:96-124", "PASS",
    RR + "hypothesis now 'Assume A3 (price taking)' (A3 is price taking; the round-1 label A2 was wrong). Proof re-derived: E e^{tZ} = exp(t mu + t^2 V/2); g(x) = -a x (m-p) + a^2 V x^2/2; unique minimiser x* = (m-p)/(aV). MGF proof is inside the lemma as G states.")
row("E4b-L06-lemma63", "Lemma 6.3 (informed beliefs)", "course/modules/E/E4/L06.html:128-144", "PASS",
    C + " Re-derived: Cov(e,s)=0 and Cov(e,u)=0 for e = v - omega s; G gives independence; Var(v|s,p) = sig_v^2(1-omega) = V_I; 1/V_I = tau_v+tau_eps and omega/V_I = tau_eps.")
row("E4b-L06-lemma64", "Lemma 6.4 (uninformed beliefs are a linear projection)", "course/modules/E/E4/L06.html:146-156", "PASS",
    C + " Re-derived: b = Cov(v,p)/Var(p), Var(p) > 0 under A1 whenever (theta_s,theta_u) != 0; Var(v|p) = sig_v^2 - b Cov(v,p).")
row("E4b-L06-prop67-uniqueness", "Proposition 6.7(b) uniqueness and Definition 6.6 convention", "course/modules/E/E4/L06.html:167-202", "PASS",
    RR + "the round-1 gap (Lemma 6.4 needs Var(p) > 0, so pair (0,0) was undefined) is closed by the Definition 6.6 convention: p = 0 gives b = 0 and V_U = sig_v^2. Step 1 (theta_s = 0 impossible) then covers (0,0) and every theta_u. Steps 2-4 re-derived exactly, including the pointwise coefficient extraction at (0,0), (1,0), (0,1) and kappa' = kappa.")
row("E4b-L06-prop67-existence", "Proposition 6.7(a) existence", "course/modules/E/E4/L06.html:206-209", "PASS",
    C + " Re-derived: Q theta_s* = lambda tau_eps and Q theta_u* = a, so the clearing identity holds for every (s,u).")
row("E4b-L06-cor68", "Corollary 6.8 (uninformed projection at equilibrium)", "course/modules/E/E4/L06.html:211-227", "PASS",
    C + " E[v|p] = tau_eta p/(theta_s*(tau_v+tau_eta)) and Var(v|p) = 1/(tau_v+tau_eta) re-derived; 100 random parameter draws in independent_checks.py confirm the variance equality with sig_v^2 sig_eta^2/(sig_v^2+sig_eta^2).")
row("E4b-L06-example69-remark610", "Example 6.9 and Remark 6.10", "course/modules/E/E4/L06.html:228-236", "PASS",
    C + " Example 6.9 values re-derived exactly: kappa 2, sig_eta^2 2, tau_eta 1/2, tau_bar 3/4, theta 3/7, 6/7, b 7/9, V_U 2/3, x_I 1/7, x_U -1/7, clearing 1/2*(1/7) + 1/2*(-1/7) = 0. Remark 6.10 (sig_eta^2 >= sig_eps^2 > 0) correct.")
row("E4b-L06-misconceptions", "L06 misconceptions (changed item 3 and others)", "course/modules/E/E4/L06.html:493-513", "PASS",
    RR + "Misconception 1 (variance of eta = 2 at base, Lab 1 Part A), 3 (slopes 3/7 and 7/9, Lab 1 Parts A and B), 4 (posterior variance 2/3 below prior 1, Lab 1 Part B; Corollary 6.8) re-checked against the printed output.")
row("E4b-L06-problems-M", "L06 problem set, Mechanics M1-M3", "course/modules/E/E4/L06.html:521-541", "PASS",
    C + " M1 (kappa 4, sig_eta^2 5, tau_eta 1/5, tau_bar 3/5, theta_s 3/8, theta_u 3/2), M2 (Var(p) 27/32, b 4/9, Var(v|p) 5/6, rho^2 1/6), M3 (price -3/4, x_I 7/4, x_U 1/4, clears to u = 1) re-derived exactly in independent_checks.py.")
row("E4b-L06-problems-P", "L06 problem set, Proof P1-P3", "course/modules/E/E4/L06.html:546-566", "PASS",
    C + " P2's argument (at (s,0) and (s+1,0) the clearing values differ by lambda tau_eps/a with the same u) is valid; P3 identity re-derived.")
row("E4b-L06-problems-E", "L06 problem set, Empirical E1-E3", "course/modules/E/E4/L06.html:571-591", "PASS",
    C + " E1 arithmetic: (0.80 - 7/9)/0.05 = 0.44 SE. E2 arithmetic: (0.426617 - 3/7) = -0.001954; /0.006497 = -0.30 tolerance; SE = 0.002166; -0.90 SE. Re-computed.")
row("E4b-L06-problems-R", "L06 problem set, Research R1-R3 (R1 changed)", "course/modules/E/E4/L06.html:596-616", "PASS",
    RR + "R1 limit: kappa = a sig_eps^2/lambda to infinity, tau_eta to 0, theta_s* to 0, Corr(v,p)^2 = sig_v^2/(sig_v^2+sig_eta^2) to 0, all checked numerically (independent_checks.py, monotone in lambda). The outside-A2 remark is correct (A2 requires lambda in (0,1)). R2 (Var(v|p) strictly increasing in sig_u^2) and R3 (G used in Lemmas 6.3 and 6.4; four facts needed) re-read and correct.")
row("E4b-L06-quiz-q12", "Quiz item L06q11 (clearing with probability one vs pointwise)", "course/modules/E/E4/L06.html:714-720", "PASS",
    RR + "the round-1 keyed answer (probability-one requirement would not identify coefficients) was false; the new item asks why probability-one clearing gives the same coefficients, keyed answer 'a nonzero linear function of (s,u) vanishes only on a line, which has probability zero under the normal law of (s,u)' is correct given sig_u^2 > 0 and Var(s) > 0 (A1). Explanation correct; Step 3 of Proposition 6.7 evaluates at three points (confirmed).")
row("E4b-L06-A4-section3", "A4 cross-reference for probability-one clearing", "course/modules/E/E4/L06.html:82-86", "FAIL",
    "A4 says 'clearing with probability one forces the same coefficients (Section 3, after Proposition 6.7).' Section 3 contains no such discussion: grep for 'probability' in L06.html finds only A4 (line 86) and the quiz item and its explanation (lines 714-720). The pointer is dangling; the argument exists only in the quiz explanation.",
    fix="Replace '(Section 3, after Proposition 6.7)' at L06.html:86 with an inline one-sentence argument (the residual is linear in (s,u) with no constant term; a nonzero one vanishes only on a line, which has probability zero because (s,u) has a nondegenerate normal law under A1), or point to the quiz explanation by name. Do not leave a pointer to content that is not there.")
row("E4b-L06-quiz-rest", "L06 quiz, changed and unchanged items", "course/modules/E/E4/L06.html:637-716", "PASS",
    RR + "q1 0.4286 (3/7), q2 kappa 4, q3 sig_eta^2 2, q4 keyed 'v - omega s uncorrelated with s and u ... independent of (s,p)' (correct, G), q5 V_I 0.5, q6 'rises' (sig_eta^2 increasing in sig_u^2), q7 x_I 0.1429 (1/7), q8 b 0.7778 (7/9), q9 keyed 'differs from slope of p on s' (3/7 vs 7/9), q10 Var(v|p) 0.6667, q11 keyed 'Exactly one' (Proposition 6.7). All numeric tolerances contain the exact values.")
row("E4b-L06-why-uninformed-trading", "why-it-matters (L06) claims", "course/modules/E/E4/L06.html:51", "PASS",
    RR + "the sentence 'absorbs the supply that uninformed trading brings' is replaced with 'absorbs a supply of the asset that carries no payoff information', which matches Definition 6.1 (noise traders as a random net supply u). The remaining claims match Lemma 6.4 and Corollary 6.8.")
row("E4b-L06-dfn-informed-fraction-posterior", "informed fraction and posterior defined before first use", "course/modules/E/E4/L06.html:57 and 96", "PASS",
    RR + "'informed fraction' is defined at L06.html:57 (first use of the phrase in the page); 'posterior' is defined at L06.html:96, and no earlier use exists (grep). The defined term is used after its definition in Lemma 6.2 and Section 2.")
row("E4b-L06-grades", "L06 key-results grades", "course/modules/E/E4/L06.html:621-627", "PASS",
    C + " T rows are proved on the page (Lemma 6.3, Lemma 6.4, Proposition 6.7, Corollary 6.8) or exact arithmetic reproduced by Lab 1; C rows name Lab 1 Parts C-E and SIMULATED Part E.")
row("E4b-struct-L06", "L06 structure, header, nav", "course/modules/E/E4/L06.html:2, 34-731", "PASS",
    RR + "header data-hours=8 matches the hub (8 h per lesson); h1 'Noisy rational-expectations equilibrium' matches hub card and L05 nav. Previous nav 'Rational-Expectations Equilibrium' matches L05.html:35 h1. The Next nav label is the subject of row E4b-nav-labels.")

# hub, cross-slice and global rows
row("E4b-hub-titles", "hub card titles vs the page h1s they link to (L04-L06)", "course/modules/E/E4/index.html:132-133 vs L04.html:35 and L05.html:35", "FAIL",
    "index.html:132 card title 'Complete and incomplete markets' vs L04.html:35 h1 'Complete and Incomplete Markets' (case differs). index.html:133 card title 'Rational-expectations equilibrium' vs L05.html:35 h1 'Rational-Expectations Equilibrium' (case differs). L06 card title (index.html:134) equals its h1 exactly. Round-1 cited the same two rows and the L05/L06 nav lines; the navs now match the h1s.",
    fix="Set index.html:132 to 'Complete and Incomplete Markets' and index.html:133 to 'Rational-Expectations Equilibrium' so each card title equals the page h1. Re-run check_pages E4 afterwards.")
row("E4b-nav-labels", "navigation labels use one convention within the slice", "course/modules/E/E4/L06.html:734 vs L06.html:733, L05.html:510-511, L04.html:520", "FAIL",
    "L06.html:734 Next label is 'L07 · Price informativeness' (prefixed with the lesson number); the other slice navigation labels are bare titles equal to the h1 (L06.html:733 'Rational-Expectations Equilibrium', L05.html:510-511, L04.html:520). New row, found while re-reading the L06 nav block in round 2. Out-of-slice note: L07.html:603-604 uses the prefix convention on both its nav links, so the unit has no single convention.",
    fix="Set L06.html:734 to 'Price informativeness' so the slice uses one convention, or decide one convention for the whole unit (including L07.html:603-604) and apply it everywhere.")
row("E4b-dag-closure", "concepts used in L04-L06 are in the prerequisite closure or are prose-only", "L04-L06 text, math and labels", "PASS",
    RR + "check_dag E4 PASS. The only concept link in the slice is crra-utility (L06.html:485), which check_dag resolves. Forward references to L07 and L08 are prose navigation, not prerequisites.")
row("E4b-concept-definitions", "concept definitions in the module the curriculum assigns", "L04.html:38,77; L05.html:73; L06.html:57-67, 96, 167", "PASS",
    RR + "plain <dfn> terms (affine, public signal, informed fraction, precisions, posterior) are not curriculum concept IDs (grep of curriculum/*.yaml finds no posterior or public-signal concept assigned elsewhere); concept IDs market-completeness, rational-expectations-equilibrium and noisy-rational-expectations-equilibrium are defined once with id and data-concept.")
row("E4b-notation-registry", "every symbol vs notation/notation.json and local definitions", "L04-L06 math segments", "PASS",
    RR + "registry symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f and Q (measure) do not occur in L04-L06 math (scan of 1,210 math segments). Macros used (E, Var, Cov, Corr, R, Normal) are registered. Local letters (alpha, beta, varsigma, nu, lambda, omega, kappa, theta, tau, eta, sigma, epsilon, Y, Z, Q, P_U, P_I) are each defined in their lesson before use.")
row("E4b-simulated-labels", "SIMULATED labels and grade C for simulated results", "L06.html:238, 252, 469-473, 627", "PASS",
    RR + "Part E is labelled SIMULATED in the hypothesis, docstring and interpretation; key-results row graded C 'SIMULATED: Lab 1, Part E, one seed'. L04 and L05 contain no simulation.")
row("E4b-banned-process-words", "no process words in learner text (BUILDER_RULES)", "L04-L06 visible prose and code docstrings", "PASS",
    RR + "tools/check_pages.py (banned phrases) PASS for L04-L06; the new 'Step 3 of Proposition 6.7' is proof-structure language, not a process word; manual read of changed prose found none.")
row("E4b-page-width-360", "no horizontal scroll at 360 px", "L04.html, L05.html, L06.html", "PASS",
    RR + "page_smoke PASS for the three pages at 360 px in light and dark themes (no horizontal scroll, no console errors, no unrendered KaTeX).")

# carry check on cmd rows
expected_ids = [r for r in json.load(open('/Users/billyribeiro/.fanout/frags/E-E4-b.round1.json'))['rows']]
ids_r1 = [r['id'] for r in expected_ids]
missing = [i for i in ids_r1 if i not in rows]
extra = [i for i in rows if i not in ids_r1]
print('missing from round 2:', missing)
print('new ids:', extra)
ordered = [rows[i] for i in ids_r1 if i in rows] + [rows[i] for i in extra]
statuses = {}
for r in ordered:
    statuses[r['status']] = statuses.get(r['status'], 0) + 1
frag = {
  "unit": "E4",
  "slice": "E4-b",
  "round": 2,
  "round_note": "Round 2 of E4-b, independent verifier (did not build E4). Pin 67c47689 (detached). Previous round-1 pin 1c1645f3 (fragment /Users/billyribeiro/.fanout/frags/E-E4-b.round1.json used as context only). Delta 1c1645f3..67c47689 read in full for L04, L05, L06, index.html and the three twins (scripts/E4-b-r2/slice_delta_1c1645f3_67c47689.diff). Round-1 rows re-verified where the subject changed; carried where byte-identical.",
  "verifier": "Haiku independent verifier, E4-b round 2",
  "pin": "67c47689",
  "base": "1c1645f3 (round-1 pin; round-1 fragment is context only)",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyE2-E4-b",
  "scratch": "/tmp/e4b-r2/ (delta.diff, u0.diff) and ledgers/E4/scripts/E4-b-r2/outputs/ (command outputs, copied)",
  "verified_at": "2026-11-04",
  "verdict": "FAIL",
  "rows": ordered,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Mutants: none. Lab twins are demonstrations and mutation testing applies to project graders only (verifier rules ruling). No mutant files written under ledgers/E4/mutants/.",
    "Full read: the round-2 delta for L04, L05, L06, index.html and the three twins was read hunk by hunk (about 970 diff lines). Unchanged content carried by the new-side hunk map (changed_hunks_new_side.diff); changed content re-verified.",
    "Independent numbers: ledgers/E4/scripts/E4-b-r2/independent_checks.py (Fraction-only, standard library, run with -I; outputs/independent_checks.txt). All numeric and proof claims pass except the units exponent (L06 docstring), recorded as FAIL row E4b-lab-L06-1-units.",
    "Round-1 non-PASS rows: 17. Round 2 flips 14 to PASS with re-verification; 3 remain FAIL (E4b-lab-L06-1-units, E4b-L06-A4-section3, E4b-hub-titles); E4b-nav-labels is new.",
    "Not checked: cards.json entries for L04-L06 (assigned to a separate check in the plan); index.html objectives and L01 card (out of slice); L07.html and L08 pages (out of slice). Out-of-slice observation for the slice owner: index.html:136 L08 card title 'The Grossman–Stiglitz Paradox' differs in case from the nav text at L07.html:604 'L08 · The Grossman–Stiglitz paradox'.",
    "Not checked: the paper Muth (1961) itself (not read; the page claims only the title, which matches the registry record). Live verify_refs not repeated (references/ unchanged since the pin).",
    "Observation (not a row): L05 uses varsigma (U+03C2) for the supply response beside sigma (sigma_z, sigma_u, sigma_eta) in the same equations. Glyphs are close, though no registry or definition conflict exists.",
    "Units row: the page and twin share one docstring; the fix must edit the twin and re-embed with tools/embed_labs.py before run_labs will pass again."
  ],
  "summary": f"E4-b round 2: FAIL. {len(ordered)} rows: {statuses.get('PASS',0)} PASS, {statuses.get('FAIL',0)} FAIL, 0 unverifiable. FAIL rows: E4b-lab-L06-1-units (docstring units wrong for kappa and theta_u), E4b-L06-A4-section3 (dangling Section 3 pointer), E4b-hub-titles (two hub card titles differ from h1), E4b-nav-labels (L06 next nav prefix convention). 14 round-1 FAILs now PASS."
}
json.dump(frag, open('ledgers/E4/E4-b.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ordered), statuses)
print('validate:', ledger.validate(json.load(open('ledgers/E4/E4-b.json')), 'E4-b'))
