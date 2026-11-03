import json
S = "ledgers/E5/scripts/E5-b-r2/"
R = []
def row(i, check, loc, status, ev, fix=""):
    d = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)

# ---- commands ----
row("E5b-r1-cmd-run-labs", "2.5 run_labs --unit E5 (all 11 E5 labs incl. L04-L06)",
    "tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py; tools/run_labs.py",
    "PASS", f"Ran .venv/bin/python tools/run_labs.py --unit E5: 'run_labs E5: PASS (11/11)', exit 0 ({S}d2_run_labs_E5.out).")
row("E5b-r1-cmd-twin-expected", "2.5 twins alone under python -I -W error; stdout equals page expected block",
    "course/modules/E/E5/L04.html, L05.html, L06.html expected blocks; twins",
    "PASS", f"{S}d2_page_vs_twin.py (output {S}d2_page_vs_twin.out): each twin exit=0, stderr_bytes=0, and the expected block equals stdout exactly; FAILURES 0.")
row("E5b-r1-cmd-page-eq-twin", "2.5 page lab code equals its twin",
    "L04.html, L05.html, L06.html <pre><code data-run>",
    "PASS", f"{S}d2_page_vs_twin.out: 'page code equals twin (rstrip newline): True' for L04, L05 and L06 (html.unescape of the code block).")
row("E5b-r1-cmd-check-pages", "2.9 check_pages --unit E5 --page L04/L05/L06",
    "course/modules/E/E5/L04.html, L05.html, L06.html",
    "PASS", f"{S}d2_static_checks.out: 'check_pages E5 L04: PASS', 'check_pages E5 L05: PASS', 'check_pages E5 L06: PASS'.")
row("E5b-r1-cmd-check-dag", "2.9 check_dag --unit E5 and --all",
    "concept links and dfn in L04-L06",
    "PASS", f"{S}d2_static_checks.out 'check_dag E5: PASS'; {S}d2_check_dag_all.out ends 'check_dag AP1: PASS' with 'exit=0'.")
row("E5b-r1-cmd-page-smoke", "2.9 page_smoke --unit E5 --pages L04 L05 L06 (Chromium, Pyodide labs, both themes, 360 px)",
    "course/modules/E/E5/L04.html, L05.html, L06.html",
    "PASS", f"{S}d2_page_smoke_L04-L06.out: 'page_smoke modules/E/E5/L04.html: PASS' (and L05, L06); 'page_smoke E5: PASS'; lab runtime 0.0 s each; exit=0.")
row("E5b-r1-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on the three twins",
    "tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py",
    "PASS", f"{S}d2_ruff_mypy.out: 'All checks passed!', '3 files already formatted', 'Success: no issues found in 3 source files'.")
row("E5b-r1-cmd-pytest-labs", "pytest tests/test_labs.py -k E5 -q",
    "tests/test_labs.py",
    "PASS", f"{S}d2_pytest_labs_E5.out: 11 tests passed, exit 0.")
row("E5b-r1-cmd-verify-refs", "verify_refs --unit E5 (live) and the offline integrity run",
    "references/references.json (hicks1937mr at line 12484, phelps1968money at line 19130)",
    "PASS", f"{S}d2_verify_refs_live.out: 'live re-verification of E5: 4 of 560 entries, 0 problems'; {S}d2_verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'.")
row("E5b-r1-cmd-rederive", "3 independent Fraction re-derivation of every number in L04-L06 prose, quiz, lab and Part B path",
    f"{S}d2_rederive.py",
    "PASS", f"{S}d2_rederive.py (own formulas, substitution checks, seeded path from random.Random(20261028)); output {S}d2_rederive.out: 116 checks 'OK', 'FAIL COUNT 0 []'.")

# ---- citations ----
row("E5b-r1-ref-hicks", "2.1 citation hicks1937mr (paper level, no attributed result)",
    "course/modules/E/E5/L04.html:567; references/references.json:12484",
    "PASS", "L04.html:567 cites via data-cite 'hicks1937mr' and says the lesson has not read the paper and attributes no result to it; key present in references.json:12484; verify_refs live 0 problems (d2_verify_refs_live.out).")
row("E5b-r1-ref-phelps", "2.1 citation phelps1968money (paper level, no attributed result)",
    "course/modules/E/E5/L06.html:525; references/references.json:19130",
    "PASS", "L06.html:525 data-cite 'phelps1968money', no locator, no result attributed; key present at references.json:19130; verify_refs live 0 problems.")

# ---- L04 ----
row("E5b-r1-l04-why", "2.9 why-it-matters length and cross-references", "course/modules/E/E5/L04.html:52",
    "PASS", f"{S}d2_text_scans.out 'L04: words=120' (limit 120). Cross-references Definition 1.1, Definition 2.1, Proposition 3.2, Remark 4.4, Definition 4.1 exist (L04.html:59,74,117,172,132). Strict inequality below 1/(1-c) under b>0, d>0 is Proposition 4.3 (L04.html:156-162).")
row("E5b-r1-l04-s1", "2.4 Section 1: Definition 1.1 and Remark 1.2", "course/modules/E/E5/L04.html:56-66",
    "PASS", "Read line by line. Definition 1.1 'Neither says how large ... or what causes them' is a definition. Remark 1.2 makes no statistical claim; no number is stated.")
row("E5b-r1-l04-s2", "2.4 Section 2: Definition 2.1, A1-A4, Derivation 2.2", "course/modules/E/E5/L04.html:72-101",
    "PASS", "Re-derived: A = c0 - c*Tax + b0 + G; (1-c)Y + b i = A; dY - h i = mbar (Derivation 2.2). Assumptions A2 (0<c<1, b>=0, d>=0, h>0) are as used in Proposition 3.2.")
row("E5b-r1-l04-s3", "2.4 Definition 3.1 and Proposition 3.2 with its proof", "course/modules/E/E5/L04.html:107-127",
    "PASS", "D = h(1-c)+bd; determinant of [[1-c,b],[d,-h]] is -D (checked in Fractions in d2_rederive.py 'L04 Part A' checks); closed forms Y*=(hA+b mbar)/D and i*=(dA-(1-c)mbar)/D substitute back exactly (Proof, L04.html:126 and d2_rederive.py assertions).")
row("E5b-r1-l04-s4-prop42", "2.4 Proposition 4.2 partial derivatives and proof", "course/modules/E/E5/L04.html:137-154",
    "PASS", "All five derivatives re-derived from the closed forms: h/D, b/D, -ch/D, d/D, -(1-c)/D (d2_rederive.py 'L04 B', 'L04 C', 'L04 b/D', '-(1-c)/D' OK).")
row("E5b-r1-l04-s4-prop43", "2.4 Proposition 4.3 (h/D <= 1/(1-c) iff bd >= 0; equality iff bd = 0) and proof", "course/modules/E/E5/L04.html:156-168",
    "PASS", "h/D <= 1/(1-c) iff h(1-c) <= D iff 0 <= bd (multiply by D(1-c)>0); verified by d2_rederive.py 'L04 benchmark 1/(1-c)' and 'L04 h/D'.")
row("E5b-r1-l04-remarks", "2.4 Remark 4.4 (b=0 benchmark) and Remark 4.5 (di/dG = d/D >= 0; investment fall bd/D)", "course/modules/E/E5/L04.html:171-178",
    "PASS", "b=0: D=h(1-c), dY/dG=1/(1-c), dY/dmbar=0 (d2_rederive.py 'L04 D b=0 multiplier' = 4). Remark 4.5: dI/dG = -b d/D, zero iff bd=0 since D>0.")
row("E5b-r1-l04-lab", "2.5 Lab 1 (lab-E5-L04-1): code equals twin, expected equals output, hypothesis numbers", "course/modules/E/E5/L04.html:180-333; tests/labs/E5/lab-E5-L04-1.py",
    "PASS", f"{S}d2_page_vs_twin.out (code equal, exact stdout match). Hypothesis values 28/5, 4/5, 2/5, 8/5, -1/5, 4 reproduced by d2_rederive.py. Lab uses Fraction only, no random draws, twin ends with unconditional main() (line 305).")
row("E5b-r1-l04-interp", "2.5 Lab 1 interpretation paragraph (every number and printed token)", "course/modules/E/E5/L04.html:332",
    "PASS", "Each printed token checked against the expected block at L04.html:306-331: 28/5, 5.6000000000, 4/5, 0.8000000000, residuals 0, 2/25, 1/25, 4/5, 2/5, multiplier_below_cross True, 8/5, -1/10, -1/5, multiplier 4, equals_one_over_one_minus_c True. The 'checks' sentence matches printed closed forms in Parts B-D.")
row("E5b-r1-l04-canon", "2.9 Section 5 Where the canon breaks (4 bullets; bullet 1 changed at c737272)", "course/modules/E/E5/L04.html:338-342",
    "PASS", "Changed line 338 read: 'Output and the interest rate are then the two unknowns of the model' is accurate (system (1-c)Y+b i=A, dY-h i=mbar). Bullets 2-4 read in full: 'no path', 'money supply fixed by assumption', 'closed economy', 'linear behaviour' are consistent with Definition 2.1 and Remark 1.2.")
row("E5b-r1-l04-misc", "2.4 / 2.9 Section 6 Misconceptions (3): wrong belief, why wrong, evidence", "course/modules/E/E5/L04.html:359 (misconception 3); cards.json E5-c070 (line 502)",
    "FAIL", "L04.html:359 'Proposition 3.2 gives one equilibrium for each set of parameters'. Proposition 3.2 is stated under A1 to A4 (L04.html:118), and its proof needs D != 0, which A2 gives. Counterexample outside A2: h = 0 and d = 0 make the LM relation 0 = mbar, which has no solution for mbar = 2. The sentence drops the hypotheses. Misconceptions 1 and 2 (L04.html:351, 355) are verified: 4/5 vs 4, 4/5 and 2/5 match Lab 1 Part B.",
    "Replace L04.html:359 with: 'Under A1 to A4, Proposition 3.2 gives exactly one equilibrium for each admissible set of parameters, and the model has no dynamics (§5).' Make the same edit in cards.json E5-c070 back (see E5b-r1-cards-L04).")
row("E5b-r1-l04-prob-M", "2.4 Problem set Mechanics M1-M3 with worked solutions", "course/modules/E/E5/L04.html:370-390",
    "PASS", "M1: D=3, Y*=14/3, i*=5/6, IS check 4, LM check 3 (re-derived). M2: h/D=2/3, benchmark 2, ratio 1/3. M3: b/D=2/3, -(1-c)/D=-1/6. All in d2_rederive.py 'L04 M1'-'L04 M3' OK.")
row("E5b-r1-l04-prob-P", "2.4 Problem set Proof P1-P3", "course/modules/E/E5/L04.html:395-416",
    "PASS", "P1 derivation of (1-c)Y+b i=A re-checked line by line. P2: D>=h(1-c)>0; strict inequality iff bd>0. P3: IS slope -(1-c)/b<0, LM slope d/h>0 (i = (dY - mbar)/h).")
row("E5b-r1-l04-prob-E", "2.4 Problem set Empirical E1-E3", "course/modules/E/E5/L04.html:421-440",
    "PASS", "E1: ratio (1/25)/(2/25)=1/2 = d/h (d2_rederive 'L04 E1'). E2: -1/10 over 1/2 = -1/5 = -(1-c)/D. E3: 0.8/4 = 1/5 = h(1-c)/D. Prose 'the basis is the printed values' is consistent with Parts B-D output.")
row("E5b-r1-l04-prob-R", "2.4 Problem set Research R1-R3", "course/modules/E/E5/L04.html:446-466",
    "PASS", "R1: d=0 gives D=h(1-c), dY/dG=1/(1-c), di/dG=0, LM i=-mbar/h horizontal. R2: b=0 gives dY/dmbar=0 and output A/(1-c). R3: di/dG=d/D>=0, zero iff d=0.")
row("E5b-r1-l04-keyres", "2.9 Key-results table (4 rows, grades and sources)", "course/modules/E/E5/L04.html:474-478",
    "PASS", "Four rows, all graded T; sources match Derivation 2.2, Proposition 3.2, Proposition 4.2 and Proposition 4.3 with Lab 1 Parts B and C as stated.")
row("E5b-r1-l04-quiz", "2.9 Retrieval quiz (10 items; keys and explanations)", "course/modules/E/E5/L04.html:484-563",
    "PASS", "Ten items. Numeric keys 5.6, 0.8, 4, -0.2 recomputed (d2_rederive 'L04 Q3' and 'L04 Part A'). Multiple-choice keys: Definition 1.1, exactly one equilibrium, strictly smaller multiplier, negative di/dmbar, IS slopes down, A3 fixes prices, all consistent with the page.")
row("E5b-r1-l04-refs", "2.1 / 2.4 Section 10 references paragraph (method sentence)", "course/modules/E/E5/L04.html:567",
    "FAIL", "L04.html:567: 'The results in §3 and §4 are derived on this page (grade T) from Definition 2.1 and Assumptions A1 to A4, using only linear algebra.' Proposition 4.2's proof differentiates the closed form (L04.html:153, 'Differentiate') and Proposition 4.3 uses an inequality argument (L04.html:167). Neither is linear algebra. The citation and the statement that the lesson has not read hicks1937mr are correct.",
    "Replace 'using only linear algebra' in L04.html:567 with 'using linear algebra, differentiation of the closed form, and elementary inequalities'.")

# ---- L05 ----
row("E5b-r1-l05-why", "2.9 why-it-matters length and cross-references", "course/modules/E/E5/L05.html:52",
    "PASS", f"{S}d2_text_scans.out 'L05: words=119'. Cross-references Definition 1.1, Proposition 2.1, 2.2, 3.1 exist. 'Lab 1 checks the formulas exactly' matches exact_match True (L05.html:231).")
row("E5b-r1-l05-model", "2.4 Section 1: A1-A3, Definition 1.1, Remark 1.2", "course/modules/E/E5/L05.html:58-81",
    "PASS", "A1 Y^d=a-eta P (eta>0), A2 Y^s=Ybar+nu(P-P^e) (nu>0), A3 P^e=P, Definition 1.1 with A3 for long run. Remark 1.2: IS-LM output affine in mbar=M/P, hence affine in 1/P; linear in P only if the slope b/D is zero, i.e. b=0 (Lesson 4 Remark 4.4, L04.html:171-172): correct.")
row("E5b-r1-l05-prop21", "2.4 Proposition 2.1 and proof", "course/modules/E/E5/L05.html:85-97",
    "PASS", "P*=(a-Ybar+nu P^e)/(eta+nu), Y*=a-eta P*, Y*-Ybar=nu(P*-P^e) re-derived; numbers at Lab inputs: P*=6/5, Y*=1040 (d2_rederive 'L05 A P*', 'L05 A Y*'). Unique because eta+nu>0.")
row("E5b-r1-l05-prop22", "2.4 Proposition 2.2, proof, Remark 2.3", "course/modules/E/E5/L05.html:99-116",
    "PASS", "dP=da/(eta+nu), dY=nu da/(eta+nu) re-derived; bounds 0<nu/(eta+nu)<1 from eta,nu>0. Remark 2.3: limit 1 as nu grows (nu/(eta+nu)=1/(1+eta/nu)); d2_rederive 'L05 Remark2.3 identity' OK.")
row("E5b-r1-l05-lab", "2.5 Lab 1 (lab-E5-L05-1): code equals twin, expected equals output, hypothesis numbers", "course/modules/E/E5/L05.html:118-232; tests/labs/E5/lab-E5-L05-1.py",
    "PASS", f"{S}d2_page_vs_twin.out: code equal; stdout equals expected block exactly. Hypothesis numbers 1.2, 1040, 0.1, 20, 1.6, 1.9 and Part D shares/prices reproduced in d2_rederive.py 'L05 A'-'L05 D' rows (all OK).")
row("E5b-r1-l05-interp", "2.5 Lab 1 interpretation paragraph", "course/modules/E/E5/L05.html:231",
    "PASS", "Values 1.200000, 1040.000000, residuals 0.000000, 0.100000, 20.000000, exact_match True, 1.6/1.9, 1000 in both states, long_run_is_short_run_fixed_point True, Part D 0.333333 to 0.888889 and 0.200000 to 0.033333 all match expected lines 210-230.")
row("E5b-r1-l05-prop31", "2.4 Proposition 3.1, proof, Remark 3.2", "course/modules/E/E5/L05.html:236-253",
    "PASS", "P_LR=(a-Ybar)/eta and Y_LR=Ybar from A1-A3; fixed-point algebra (a-Ybar)(1+nu/eta)/(eta+nu)=(a-Ybar)/eta re-checked; 1.6 and 1.9 and change 0.3 (d2_rederive 'L05 C').")
row("E5b-r1-l05-canon", "2.9 Section 4 Where the canon breaks (4 bullets)", "course/modules/E/E5/L05.html:258-261",
    "PASS", "Bullet 2 formulas dP=(da+nu dPe)/(eta+nu), dY=nu(da-eta dPe)/(eta+nu) re-derived. Bullet 3: a=1190, Pe=1, nu=200, eta=100 gives P*=1.3, Y*=1060, i.e. 60 above potential (d2_rederive 'L05 R3 output gap').")
row("E5b-r1-l05-misc", "2.4 Section 5 Misconceptions (3)", "course/modules/E/E5/L05.html:269-279",
    "PASS", "Demand 1160-100*1=1060 and 1160-100*1.6=1000 (drop 60 for a rise of 0.6); Proposition 2.2 output share 200/300 = two thirds of the 30 shift = 20 (Part B output change 20.000000); long-run output 1000 for every a under A3 (Proposition 3.1 derivation, no positivity restriction needed for the output claim).")
row("E5b-r1-l05-prob-M", "2.4 Problem set Mechanics", "course/modules/E/E5/L05.html:291-308",
    "PASS", "M1: P*=1.05, Y*=995, supply check 995 (d2_rederive 'L05 M1'). M2: share 3/4, dY=30, dP=0.2. M3: P_LR 1 and 1.4, output 1000 (check 1140-140=1000).")
row("E5b-r1-l05-prob-P", "2.4 Problem set Proof", "course/modules/E/E5/L05.html:316-332",
    "PASS", "P1 uniqueness: (eta+nu)(P2-P1)=0 re-derived. P2: 1-nu/(eta+nu)=eta/(eta+nu)>0. P3: P*=(a-Ybar)/eta when Pe=(a-Ybar)/eta re-derived.")
row("E5b-r1-l05-prob-E", "2.4 Problem set Empirical", "course/modules/E/E5/L05.html:341-358",
    "PASS", "E1: share 4/5, dY=24, dP=0.06 (d2_rederive 'L05 E1'). E2: printed outputs 10,15,20,24,26.666667; increments 5,5,4,8/3 (30*(8/9-4/5)=8/3). E3: 1.9-1.6=0.3 gives da=30; 8/5 and 19/10 exact at six decimals.")
row("E5b-r1-l05-prob-R", "2.4 Problem set Research", "course/modules/E/E5/L05.html:366-384",
    "PASS", "R1: H(P)=F(P)-Ybar-nu(P-Pe) continuous, strictly decreasing, limits +inf at 0 and -inf at infinity; IVT and monotonicity give exactly one zero. R2: P*=450/300=1.5, Y*=1040. R3: A3 needed; output gap 1060-1000=60 with Pe=1.")
row("E5b-r1-l05-keyres", "2.9 Key-results table (5 rows)", "course/modules/E/E5/L05.html:394-398",
    "PASS", "Five rows, all graded T, sources Proposition 2.1, 2.2, 3.1 and Lab 1 Parts A, B, D (exact), consistent with the page.")
row("E5b-r1-l05-quiz", "2.9 Retrieval quiz (10 items)", "course/modules/E/E5/L05.html:409-481",
    "PASS", "Keys 1.2, 1040, slope -eta, 20, 0.1, share strictly between 0 and 1, larger nu flatter supply, 0.3, output at Ybar, A3 all recomputed. Explanations match Propositions 2.1, 2.2, 3.1 and Remark 2.3.")
row("E5b-r1-l05-refs", "2.1 references paragraph (L05 cites no source)", "course/modules/E/E5/L05.html:485-489",
    "PASS", "grep: L05.html has 0 data-cite attributes. The paragraph says hicks1937mr is not cited because the lesson has not read it (text in a code element). Round-1 citation of L05.html:487 is withdrawn: no citation markup exists in L05.")

# ---- L06 ----
row("E5b-r1-l06-why", "2.9 why-it-matters length and cross-references", "course/modules/E/E5/L06.html:52",
    "PASS", f"{S}d2_text_scans.out 'L06: words=117'. Adaptive-expectation claim 'inflation changes exactly when unemployment differs from the natural rate' matches Corollary 3.2 (beta>0).")
row("E5b-r1-l06-defs", "2.4 Section 1: variables, A1-A3, Definitions 1.1 and 1.2 (line 60 changed at c737272)", "course/modules/E/E5/L06.html:56-85",
    "PASS", "Changed line 60 read: 'The seeded draws in Lab 1 generate an unemployment path for illustration; they are not part of the model' matches the twin (tests/labs/E5/lab-E5-L06-1.py: random.Random(SEED).randint draws the unemployment gap, line ~191). P^e_t=P_{t-1}(1+pi^e_t) re-derived. A2 slope kappa per unit of u, A3 pi^e=pi_{t-1}, Definition 1.2 unique natural rate (kappa>0) all correct.")
row("E5b-r1-l06-prop21", "2.4 Proposition 2.1 and proof", "course/modules/E/E5/L06.html:89-105",
    "PASS", "P_t - P^e_t=(Y_t-Ybar)/nu; P_t=P^e_t-(kappa/nu)(u_t-u^n); divide by P_{t-1}: pi_t=pi^e_t - kappa/(nu P_{t-1}) (u_t-u^n) re-derived; hypotheses nu, kappa, P_{t-1} > 0 stated.")
row("E5b-r1-l06-remark22", "2.4 Remark 2.2 (slope depends on P_{t-1}; kappa=nu=200 gives beta=1/P)", "course/modules/E/E5/L06.html:107-110",
    "PASS", "beta=1 at P=1 and 5/6 at P=6/5 (d2_rederive 'L06 beta at P=6/5', 'L06 beta at P=1', 'L06 R1 ratio').")
row("E5b-r1-l06-lab-A", "2.5 Lab 1 Part A: one period, Phillips form vs levels, u=0.06", "course/modules/E/E5/L06.html:112-263 (Part A); tests/labs/E5/lab-E5-L06-1.py",
    "PASS", f"Expected block lines 230-233: expected_price 1.236000, price 1.226000, both inflation 0.021667 = 13/600 (d2_rederive 'L06 A levels' and 'L06 A Phillips' OK), beta 0.833333.")
row("E5b-r1-l06-lab-B", "2.5 Lab 1 Part B: 12-period seeded SIMULATED path (identity, changes, signs, zero counts)", "course/modules/E/E5/L06.html:112-263 (Part B); lab-E5-L06-1.py",
    "PASS", f"Path reproduced by d2_rederive.py from random.Random(20261028).randint(-100,100): 12 identity checks OK; positive gaps 9, negative gaps 3; all changes opposite in sign; no zero gap; no unchanged inflation (expected lines 235-249 match). SIMULATED label present (L06.html:114, twin docstring line ~117).")
row("E5b-r1-l06-lab-C", "2.5 Lab 1 Part C: one-period change grid at P=6/5, zero at u=5%", "course/modules/E/E5/L06.html:212-261",
    "PASS", "Expected lines 250-261: 0.016667 at 3% ... -0.016667 at 7%, 0.000000 at 5%; d2_rederive 'L06 E1 change at 4%' = 1/120; sign rule True.")
row("E5b-r1-l06-lab-code", "2.5 Lab 1 code equals twin; expected equals output; docstring and hypothesis match code", "tests/labs/E5/lab-E5-L06-1.py; L06.html:115-261",
    "PASS", f"{S}d2_page_vs_twin.out: code equal, stdout equals expected exactly. Docstring 'Part B ... checks the identity exactly' matches the code (form check line ~197); 'Part C ... zero at the natural rate' matches the grid code.")
row("E5b-r1-l06-prop31", "2.4 Proposition 3.1 and proof", "course/modules/E/E5/L06.html:267-275",
    "PASS", "pi_t - pi^e_t = -beta_t(u_t-u^n) with beta_t>0; zero iff u=u^n iff Y=Ybar (A2 gives Y-Ybar=-kappa(u-u^n)). Re-derived.")
row("E5b-r1-l06-cor32", "2.4 Corollary 3.2 and proof", "course/modules/E/E5/L06.html:277-285",
    "PASS", "Under A3, pi^e_t=pi_{t-1}; pi_t-pi_{t-1}=-beta_t(u_t-u^n) holds for each period; zero iff u=u^n since beta_t>0. The 'every period' scope is derived in the proof, not assumed.")
row("E5b-r1-l06-remark33", "2.9 Remark 3.3 (natural rate is not measured; not a floor, cross-ref to §5)", "course/modules/E/E5/L06.html:287-290",
    "PASS", "'Only unemployment rate at which the curve gives inflation equal to expected inflation' is Proposition 3.1 (iff). 'Not a floor, as §5 explains' points to misconception 2 (L06.html:310-311), which says nothing in A1 or A2 makes u^n a lower bound.")
row("E5b-r1-l06-canon", "2.9 Section 4 Where the canon breaks (4 bullets)", "course/modules/E/E5/L06.html:295-298",
    "PASS", "Bullet 2 shock formula u^n+v/beta re-derived (v=0.01 gives 0.062, d2_rederive 'L06 R2 u'); the problem L06-R2 exists (L06.html:409). Bullets 1, 3, 4 accurate against Corollary 3.2, Remark 2.2 and Definition 1.2.")
row("E5b-r1-l06-misc", "2.4 Section 5 Misconceptions (3) with numbers", "course/modules/E/E5/L06.html:306-316",
    "PASS", "Gap -0.01 at beta=5/6 gives +1/120 = 0.008333 (d2_rederive 'L06 misc1 change at gap -0.01'); 3% gives 1/60 = 0.016667 (d2_rederive 'L06 misc2'); Part C prints 0.008333 at 4% and 0.016667 at 3%; Part B has 12 nonzero changes (expected lines 235-246).")
row("E5b-r1-l06-prob-M", "2.4 Problem set Mechanics", "course/modules/E/E5/L06.html:326-346",
    "PASS", "M1: beta=0.5, pi=0.03. M2: beta=0.8, pi=0.048. M3: pi_{t-1}=0.02; at u^n pi unchanged; at u^n+0.03 pi=0.005 (falls 0.015). Re-derived.")
row("E5b-r1-l06-prob-P", "2.4 Problem set Proof", "course/modules/E/E5/L06.html:353-371",
    "PASS", "P1 derivative -beta_t; P2 equal denominators (P_{t-1}) so pi_t=pi^e_t iff P_t=P^e_t iff Y_t=Ybar; P3 uniqueness of u^n from kappa>0. Re-derived.")
row("E5b-r1-l06-prob-E", "2.4 Problem set Empirical (uses seeded Part B and Part C prints)", "course/modules/E/E5/L06.html:376-396",
    "PASS", "E1: 1/120 = 0.008333 (Part C). E2: 9 positive-gap and 3 negative-gap periods in the printed Part B lines, every change opposite in sign (recounted from the 12 printed lines). E3: gap 58 bp gives change -29/6000 = -0.004833 (d2_rederive 'L06 E3 period-1 change'); 5.5% row -1/240 = -0.004167.")
row("E5b-r1-l06-prob-R", "2.4 Problem set Research", "course/modules/E/E5/L06.html:401-421",
    "PASS", "R1 beta ratio 6/5 equals 1.2/1 (beta proportional to 1/P). R2 u=0.05+0.012=0.062 (d2_rederive 'L06 R2 u'). R3 gives no numerical value, as the prompt requires.")
row("E5b-r1-l06-keyres", "2.9 Key-results table (6 rows; Part B row graded C)", "course/modules/E/E5/L06.html:431-436",
    "PASS", "Rows graded T for Propositions 2.1, 3.1, Corollary 3.2 and Lab 1 Parts A and C (exact); Part B graded C with 'Lab 1, Part B (SIMULATED, one seed)' as basis, as BUILDER_RULES §7 requires.")
row("E5b-r1-l06-quiz", "2.9 Retrieval quiz (10 items)", "course/modules/E/E5/L06.html:446-520",
    "PASS", "Keys: natural rate definition, beta=1, negative sign above u^n, 0.008333, pi^e=pi_{t-1}, 0.021667, no shock term, beta proportional to 1/P_{t-1}, 0.048; check explanation for no_change_only_at_natural_rate matches printed zero counts. All recomputed.")
row("E5b-r1-l06-refs", "2.1 references paragraph (phelps1968money)", "course/modules/E/E5/L06.html:523-527",
    "PASS", "One data-cite (line 525), no locator, no attributed result. 'Propositions 2.1 and 3.1 and Corollary 3.2 are derived on this page (grade T)' is accurate.")

# ---- cards ----
row("E5b-r1-cards-L04", "2.7 cards for L04: every card against the current lesson text; hypotheses carried; card numbers appear in the lesson",
    "course/modules/E/E5/cards.json: E5-c053-c070 (c060, c069, c070 changed at c737272), E5-c134; back of E5-c068 at line 486, back of E5-c070 at line 502",
    "FAIL", f"All 19 L04 cards read against L04.html. Two defects. (a) E5-c068 back (cards.json:486): 'so bd = 1 > 0', and the number bd = 1 appears nowhere in L04.html (grep for 'bd = 1' is empty; the lesson gives b = 2 and d = 1/2 only in the Lab 1 hypothesis). (b) E5-c070 back (cards.json:502): 'Proposition 3.2 gives one equilibrium for each set of parameters' drops A1 to A4, the same defect as L04.html:359. The other 17 L04 cards are correct (see {S}d2_text_scans.out and this row's reading): c053, c054, c055-c058, c059, c060 (fixed), c061-c067, c069, c134.",
    "(a) cards.json E5-c068 back: change 'so bd = 1 > 0' to 'so bd > 0'. (b) cards.json E5-c070 back: change 'Proposition 3.2 gives one equilibrium for each set of parameters' to 'Under A1 to A4, Proposition 3.2 gives one equilibrium for each admissible set of parameters'.")
row("E5b-r1-cards-L05", "2.7 cards for L05 (c071-c087, c137, c139, c140), every card against L05.html",
    "course/modules/E/E5/cards.json (20 cards, L05)",
    "PASS", "All 20 L05 cards read against L05.html. Numbers 1060, 1000, 20.000000, 0.3, 1040, 1.2, 0.1, 0.333333 to 0.888889 and 0.200000 to 0.033333 each appear in the lesson text or expected block. Hypotheses carried ('Under A1 and A2', 'Under A1 to A3'). c085 cites §5 correctly (misconception 1).")
row("E5b-r1-cards-L06", "2.7 cards for L06 (c088-c104, c136, c138), every card against L06.html",
    "course/modules/E/E5/cards.json (19 cards, L06; c093 changed at c737272)",
    "PASS", "All 19 L06 cards read against L06.html. c093 now matches Definition 1.1 (one slope per period). c103 graded C with SIMULATED basis. c099, c100, c101 cite §5 correctly. Numbers 0.021667, 13/600, 1.236, 1.226, 0.008333, 0.016667, 0.833333, 6/5 all appear in the lesson.")
row("E5b-r1-card-c060", "2.7 card E5-c060 'What is an equilibrium of IS-LM?' (scope word 'only')",
    "course/modules/E/E5/cards.json:425-427 (back line 427)",
    "PASS", "Back now reads 'In this lesson the word has that sense (Definition 3.1).' This matches L04.html:105 ('In this lesson the word has that sense'). The scope word 'only' is gone; d2_text_scans.out shows no 'only' in c060.")
row("E5b-r1-cards-dup", "2.7 full card scan for duplicates (139 cards, unit-wide)", "course/modules/E/E5/cards.json",
    "PASS", f"{S}d2_text_scans.out: 'cards total 139 unique ids 139', 'duplicate fronts: {{}}', 'duplicate backs: {{}}'. Id gap at c135 is not a defect (plan Architect ruling 2).")
row("E5b-r1-cards-coverage", "2.7 card coverage of definitions, theorems, key formulas, key results and misconceptions of L04-L06",
    "course/modules/E/E5/cards.json; L04-L06 pages",
    "PASS", "Each L04-L06 definition (Definitions 1.1, 1.2, 2.1, 3.1, 4.1; A3 in L06), Propositions 2.1, 2.2, 3.1, 3.2, 4.2, 4.3, Corollary 3.2, Remarks 2.2, 3.2, 3.3, 4.4, 4.5, the key-results rows and the 9 misconceptions has a card (cards c053-c104, c134, c136-c140).")
row("E5b-r1-struct", "2.9 structure and minimum counts for L04-L06", "course/modules/E/E5/L04.html, L05.html, L06.html",
    "PASS", "Section order matches BUILDER_RULES §4.2 (why, core, labs, canon breaks, misconceptions, problems, key results, quiz, references). Misconceptions 3 each; problem tiers M1-M3, P1-P3, E1-E3, R1-R3 in all three; quiz 10 items each; key-results rows 4, 5, 6. debate brief not required (no debate key).")
row("E5b-r1-banned", "2.9 banned phrases and placeholders (BUILDER_RULES §1.3-1.4)", "L04-L06 pages and twins",
    "PASS", f"{S}d2_text_scans.out 'banned scan' prints no hit for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly; no ellipsis outside code.")
row("E5b-r1-process", "2.9 no process words in learner text", "L04-L06 pages",
    "PASS", f"{S}d2_text_scans.out: process scan hits are only 'rounded/rounding' in the lab docstrings and the L05/L06 rounding rule (mathematical rounding). No build, builder, round-as-process, verifier, REQUEST, ledger or planning word in learner prose.")
row("E5b-r1-scope", "rule 4 scope words (only, all, always, every, any, same, exactly, drives) with a computation or stated hypothesis",
    "L04-L06 prose (sentences with scope words; list by grep in d2_text_scans.out and this round's reading)",
    "PASS", "Every scope sentence was read. Backed: 'every period' (Corollary 3.2 proof), 'for every value of a' (Proposition 3.1 algebra gives Y_LR=Ybar for any a), 'the only one' (Proposition 3.2 proof), 'exactly one' (determinant -D, D>0; IVT and monotonicity in L05-R1), 'exactly' in M3 (linearity), 'only if' statements. The one scope sentence without a computation or hypothesis is L04.html:567 'using only linear algebra', recorded under E5b-r1-l04-refs.")
row("E5b-r1-notation", "rule 13 notation: every symbol vs notation/notation.json",
    "L04-L06 math (315, 282, 250 segments)",
    "PASS", f"{S}d2_notation_scan.out: registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}} and the expectation macro \\E do not occur in L04-L06 math; local symbols (A, C, D, G, I, M, P, Y, b, c, d, h, i, m, F, H, a, s, e, t, u, v) carry no registered meaning. Expected inflation written pi^e_t, not \\E.")
row("E5b-r1-dag", "2.9 / rule 14 DAG: links, definitions once, no use before definition",
    "L04-L06 concept links and dfn",
    "PASS", f"{S}d2_static_checks.out 'check_dag E5: PASS'. Links: L04 to comparative-statics and competitive-equilibrium (E1 closure); L05 to L04#def-is-lm-model (earlier lesson) and L06 to L05#def-ad-as-model; L06 defines phillips-curve and natural-rate-of-unemployment. Unlinked prose: 'expected inflation' (L06, plain dfn), 'policy rate' (L04 canon bullet 2, forward signpost to L07 as the plan allows), 'output gap' (plain dfn from L04). No D1-D7 concept is linked.")
row("E5b-r1-hours", "2.9 / 4.3 hours arithmetic", "course/modules/E/E5/index.html:29; L04.html:2, L05.html:2, L06.html:2",
    "PASS", f"index.html:29 data-hours-lessons=80, data-hours-project=30 (sum 110); curriculum.json E5 hours 110 ({S}d2_text_scans.out 'hours'); each of L04, L05, L06 data-hours=10; 8 lessons x 10 = 80.")
row("E5b-r1-simulated", "2.8 SIMULATED labels and no data passed off as real", "L04-L06 labs and key results",
    "PASS", "L06 lab labelled SIMULATED (L06.html:114 hypothesis, twin docstring) and its key result graded C with the lab named. L04 and L05 labs are exact closed-form checks with 'illustrative parameters, not data' (L04.html:182, L05.html:120), not SIMULATED, as BUILDER/plan §2.2 allows.")
row("E5b-r1-figures", "2.8 figures in L04-L06", "L04.html, L05.html, L06.html",
    "PASS", "grep -c '<svg|class=\"chart\"' returns 0 for each of the three pages, so no figure needs a title, desc, axis or source line. Labs print text only.")

# ---- round-2 delta and twins ----
row("E5b-r2-delta", "round 2 delta d0f39c09..c737272 read hunk by hunk for slice b",
    "course/modules/E/E5/L04.html:338; course/modules/E/E5/L06.html:60; course/modules/E/E5/cards.json E5-c053, c060, c069, c070, c093",
    "PASS", f"git diff d0f39c09 c737272 for the slice: L04.html line 338 (canon bullet 1), L06.html line 60 (one sentence), and cards E5-c053, c060, c069, c070, c093 (cards c012, c031, c044, c105, c110 belong to other slices and were read only for the diff). Each new text was checked against the lesson and the twin ({S}d2_delta_slice_b.out). Previous non-PASS row E5b-r1-card-c060 re-verified (PASS).")
row("E5b-r2-twins-unchanged", "round 2 delta: lab twins, notation and references unchanged since round 1",
    "tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py; notation/notation.json; references/references.json",
    "PASS", f"{S}d2_delta_slice_b.out: the git diff restricted to these paths is empty; the twins were nevertheless re-run in this round (E5b-r1-cmd-twin-expected).")

PASS = sum(1 for r in R if r["status"] == "PASS")
FAIL = sum(1 for r in R if r["status"] == "FAIL")
UNV = sum(1 for r in R if r["status"] == "UNVERIFIABLE")
frag = {
    "unit": "E5",
    "slice": "b",
    "round": 2,
    "round_note": ("Round 2 of this campaign for E5-b at pin c737272f (detached checkout /Users/billyribeiro/.fanout/wt/verifyD2-E5-b). "
                   "Delta from the round-1 pin d0f39c09 was read hunk by hunk (L04.html:338, L06.html:60, cards E5-c053/c060/c069/c070/c093). "
                   "Every round-1 row id is kept. Every command row was re-run on c737272 and no row is carried: each was re-checked from the source. "
                   "Round-1 FAIL E5b-r1-card-c060 is fixed and PASSes. Three new defects are FAIL rows under their existing ids."),
    "verifier": "Claude Haiku 5.5, independent verifier for E5-b round 2 (did not build E5 and did not write the round-1 fragment)",
    "pin": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "base": "d0f39c09598ffefaf0ec18d5d1077cfacd42998b (round-1 pin, read as context; its PASS rows were not trusted and were re-verified)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD2-E5-b (detached at c737272, .venv symlinked)",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyD2-E5-b/ledgers/E5/scripts/E5-b-r2/",
    "verified_at": "2026-11-02T22:05:01Z",
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [
        "hicks1937mr and phelps1968money: live verify_refs --unit E5 returned '4 of 560 entries, 0 problems' (ledgers/E5/scripts/E5-b-r2/d2_verify_refs_live.out); offline '560 entries, 0 problems'. No registry update needed."
    ],
    "freshness_flags": [],
    "notes": [
        "Slice read in full: course/modules/E/E5/L04.html (580 lines), L05.html (500), L06.html (538); tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py; the 58 L04-L06 cards of cards.json (plus the full-unit duplicate scan of 139 cards).",
        "Mutants: none. Ruling: lab twins are demonstrations and mutation testing applies to project graders only; slice b contains no grader. No student-error mutants were written and none are required here.",
        "Round-2 scripts: ledgers/E5/scripts/E5-b-r2/d2_page_vs_twin.py, d2_rederive.py, d2_text_scans.py, d2_notation_scan.py; outputs *.out in the same folder. Files cmp_r2.py, recompute_r2.py and build_fragment_r2.py already in that folder were not touched.",
        "Card locator (not a failure): E5-c053 back cites '(Remark 1.2)' for 'what causes them'; that clause is stated in Definition 1.1 (L04.html:60). The card is correct; the locator could read '(Definition 1.1; Remark 1.2)'.",
        "Ids of cards E5-c134, c136-c140 are out of order; check_pages does not require sequential ids (plan Architect ruling 2)."
    ],
    "summary": {"rows": len(R), "pass": PASS, "fail": FAIL, "unverifiable": UNV, "mutants": 0, "mutants_killed": 0,
                "counts": {"PASS": PASS, "FAIL": FAIL, "UNVERIFIABLE": UNV}},
    "what_could_not_be_checked": [
        "Rendered appearance at 360 px in light and dark by eye: page_smoke passed (headless Chromium), but no screenshot was inspected.",
        "The published content of Hicks (1937) and Phelps (1968): neither is read; the pages attribute no result to either, so no attribution was checked against the text.",
        "Hub, the other lessons (L01-L03, L07, L08) and the project: outside slice b. Only the unit-wide cards duplicate scan and the hub hours split were run.",
        "The full CI gate (ruff over the repo, mypy over the repo, the whole pytest suite, mutate_graders) was not run: it is not a targeted check for this slice."
    ]
}
import sys
sys.path.insert(0, "tools")
json.dump(frag, open("ledgers/E5/E5-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", len(R), "pass", PASS, "fail", FAIL)
