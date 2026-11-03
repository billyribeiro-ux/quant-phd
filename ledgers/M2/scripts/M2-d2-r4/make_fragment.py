import json, datetime
S = "ledgers/M2/scripts/M2-d2-r4"
rows = []
def R(id_, check, loc, status, ev):
    rows.append({"id": id_, "check": check, "location": loc, "status": status, "evidence": ev})

# ---- gates (run on pin 4eb6788 this round) ----
R("G-check-pages", "tools/check_pages.py --unit M2 (exit 0) and --page L22/L23/L24", "course/modules/M/M2/L22.html, L23.html, L24.html and hub", "PASS",
  f"{S}/check_pages.out: 'check_pages M2: PASS' rc 0; {S}/check_pages_each.out: 'check_pages M2 L22: PASS', 'L23: PASS', 'L24: PASS' (rc 0 each).")
R("G-check-dag", "tools/check_dag.py --unit M2 and --all", "curriculum DAG; M2 pages' Uses rows and concept links", "PASS",
  f"{S}/check_dag_M2.out: 'check_dag M2: PASS' rc 0; {S}/check_dag_all.out: 21 'PASS' lines, 0 'FAIL' lines.")
R("G-check-projects", "tools/check_projects.py --unit M2", "M2 hub and project (hub-level check for this slice)", "PASS",
  f"{S}/check_projects.out: 'check_projects M2: PASS' rc 0.")
R("G-run-labs", "tools/run_labs.py --unit M2 --page L22 / L23 / L24, and --unit M2", "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", "PASS",
  f"{S}/run_labs_pages.out: 'run_labs M2: PASS (1/1)' for each page; {S}/run_labs_M2.out: 'run_labs M2: PASS (27/27)'.")
R("G-twins-isolated", "each twin alone: .venv/bin/python -I -W error <twin> from an empty temporary directory", "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", "PASS",
  f"{S}/twins_alone.out: 'L22 rc=0 stderr_bytes=0', 'L23 rc=0 stderr_bytes=0', 'L24 rc=0 stderr_bytes=0' (run in /tmp/m2d2r4, an empty directory). Stdout saved as {S}/twin_L22.stdout, twin_L23.stdout, twin_L24.stdout.")
R("G-expected-blocks", "expected block of each page equals the twin's stdout", "course/modules/M/M2/L22.html:222-230; L23.html:215-225; L24.html:218-242", "PASS",
  f"{S}/compare_twins.py (run with -I) prints 'expected==stdout modulo final newline: True' for L22, L23, L24; strict comparison False only because the HTML block ends with one fewer newline (the embedding convention).")
R("G-page-code-equals-twin", "page data-run code equals the twin file", "course/modules/M/M2/L22.html:100-221; L23.html:91-214; L24.html:137-217", "PASS",
  f"{S}/compare_twins.py prints 'code==twin modulo final newline: True' for all three; strict False only by the final newline (121/122, 123/124, 80/81 lines).")
R("G-page-smoke", "tools/page_smoke.py --unit M2 --pages L22 L23 L24 (alone)", "L22.html, L23.html, L24.html", "PASS",
  f"{S}/page_smoke.out: 'page_smoke modules/M/M2/L22.html: PASS' (and L23, L24); 'page_smoke M2: PASS' rc 0.")
R("G-ruff", ".venv/bin/python -m ruff check and ruff format --check on the three twins", "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", "PASS",
  f"{S}/ruff.out: 'All checks passed!' and '3 files already formatted', rc 0.")
R("G-mypy", ".venv/bin/python -m mypy --no-incremental on the three twins", "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", "PASS",
  f"{S}/mypy.out: 'Success: no issues found in 3 source files', rc 0.")
R("G-pytest-labs", "pytest tests/test_labs.py -k 'L22 or L23 or L24'", "tests/test_labs.py (three parametrised cases for the M2 twins)", "PASS",
  f"{S}/pytest_M2_labs.out: '3 passed, 302 deselected'.")
R("G-pytest-checks", "pytest tests/test_page_checks.py tests/test_run_labs.py", "tests/test_page_checks.py, tests/test_run_labs.py", "PASS",
  f"{S}/pytest_checks.out: '47 passed', rc 0.")
R("G-verify-refs", "tools/verify_refs.py --offline", "references/references.json (keys spivak2008calculus, hubbard2015vector used by the slice pages)", "PASS",
  f"{S}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc 0. No live run: the slice cites no new registry key and no external fact.")
R("G-cards-scan", "cards.json: cards of L22, L23, L24 read in full; numbers in each card checked against its lesson text", "course/modules/M/M2/cards.json (L22: 15 cards, L23: 24, L24: 17; 394 cards in file)", "PASS",
  "Counts from json: L22 15, L23 24, L24 17. Script check (inline, run this round): every number token in each card's front/back appears literally in the lesson's visible text, except generic 0/1-6/10. All card records re-read: see CARD-L22, CARD-L23, CARD-L24.")

# ---- structure / prose ----
R("S-hours", "hours arithmetic: lesson hours vs hub split", "L22.html:2, 34; L23.html:2, 34; L24.html:2, 34; hub index.html data-hours-lessons=240, data-hours-project=60, 'Tier F · 300 hours'", "PASS",
  "Each page: data-hours=\"10\" and eyebrow '10 study hours'. 24 lessons x 10 = 240 = data-hours-lessons; 240 + 60 = 300 = hub title; hub card labels 'L22 · 10 h', 'L23 · 10 h', 'L24 · 10 h'.")
R("S-structure", "section template and section numbering", "L22.html:53-482 (s1-s7); L23.html:53-501 (s1-s9); L24.html:53-482 (s1-s10)", "PASS",
  "Section ids and numbers read in full: L22 s1 l.53, s2 l.235, s3 l.267, s4 l.285, s5 l.390, s6 l.405, s7 l.471; L23 s1 l.53 ... s9 l.487; L24 s1 l.53 ... s10 l.467. Lab section, expected block, problem tiers (mechanics/proof/empirical/research), key-results table and quiz present on all three.")
R("S-banned", "BUILDER_RULES §1.3-1.4 banned strings and filler (TODO, TBD, lorem, ellipsis, for brevity, it is important to note, obviously, clearly, it can be shown, roughly half, historically)", "L22.html, L23.html, L24.html visible text; three twins", "PASS",
  "Scan of visible text (tags stripped) for each banned pattern: no hits in prose. The only '...' hits are Python tuple type annotations inside the lab code.")
R("S-process-words", "no process words in learner text (draft, verifier, builder, round, ledger, fragment, fixed, TODO)", "visible text of L22.html, L23.html, L24.html", "PASS",
  "Case-insensitive grep over the three pages: no hits.")
R("S-simulated", "every lab and bond/test function labelled SIMULATED", "L22.html:99; L23.html:90 (and page code docstring line 93); L24.html:136 (and page code docstring line 139); twins lines 1-3", "PASS",
  "Lab hypothesis paragraphs begin with 'SIMULATED' or 'The bond is SIMULATED'; docstrings line 3 (L22), line 3 (L24), lines 1-3 (L23) say SIMULATED. No market data is read.")
R("S-external", "no external data or network use", "L22.html, L23.html, L24.html; twins imports", "PASS",
  "Twin imports: math, collections.abc, fractions only. Pages cite no URL and read no dataset.")

# ---- DAG / notation / references ----
R("DAG-links", "BUILDER_RULES §4: concepts from earlier lessons are linked and listed in the Uses row", "L22.html:37 and 374-376; L23.html:37, 53, 98 and 379; L24.html:37, 111, 156 and 373", "PASS",
  "Uses rows now list gradient (L17), Hessian (L19) for L22; implicit-function theorem (L21) for L23; automatic differentiation (L14) for L24. The round-3 uncovered names are linked: L22 R2 l.374,376 (gradient, hessian); L23 R1 l.379 (implicit-function-theorem); L24 R3 l.373 (automatic-differentiation). Anchors exist: L17.html#def-gradient, L19.html#def-hessian, L21.html#def-implicit-function-theorem, L14.html#def-automatic-differentiation. Other body mentions of listed concepts stay unlinked, as in round 3 (names are covered by the Uses row).")
R("DAG-defined-once", "each concept defined once with dfn and linked elsewhere", "L22.html:59 (only dfn on the three pages); links at L22.html:37, L23.html:37, L24.html:37", "PASS",
  "grep '<dfn' count: L22 1 (def-envelope-theorem), L23 0, L24 0. Upstream anchors present: L04 def-derivative, L08 def-taylor-theorem, L13 def-finite-difference-derivative, L16 def-partial-derivative, L17 def-gradient, L19 def-hessian, L21 def-implicit-function-theorem, L14 def-automatic-differentiation; concepts.html has present-value, discount-factor, geometric-series.")
R("DAG-later-names", "concepts named before their lesson", "L23.html:55 (M1 L05), L23.html:80 and 85 (M1 L06 geometric series); L23.html:51 and 90 (forward pointers to Section 3 results)", "PASS",
  "M1 L05 title 'Present value and the discount factor'; M1 L06 title 'Geometric Series and Proof by Induction' (anchor def-geometric-series). Forward pointers to numbered results in the same lesson are not counted as uses before definition (round-3 ruling, row FWD-L23-lab-prediction).")
R("NOT-notation", "every symbol vs notation/notation.json; only registered macros", "L22.html, L23.html, L24.html math; notation/notation.json", "PASS",
  "Macros used: \\R, \\hat, \\tilde, \\nabla, \\mathcal, \\tfrac, \\bigl, \\bigr etc. Only \\R is a registered macro and it is used as \\R. No \\mathbb, \\Phi, \\gamma, \\ast, \\mathbb{Q}, \\R_f or T used. Symbols N (cash-flow years; defined L23.html:55, conventionally local) and R (remainder, L23.html:233) are not registered symbols. Per-lesson letters (M, G, F, c, V, P, delta, xi, theta) are local.")
R("REF-keys", "cited registry keys exist in references/references.json", "L22.html:473; L23.html:488; L24.html:468", "PASS",
  "spivak2008calculus and hubbard2015vector each occur exactly once in references/references.json. Curriculum sources for M2 (curriculum/01-foundations.yaml:146-147) name Spivak and Hubbard & Hubbard, so 'the curriculum names ... as sources for this unit' is supported.")
R("REF-internal", "internal cross-references (lesson, section, remark, problem numbers) resolve", "L22.html:88, 93, 473; L23.html:233, 238, 379, 488; L24.html:75, 85, 107, 117, 132, 373", "PASS",
  "L21 Thm 1.3 (IFT) l.68, Assumption 1.2 (IVT) l.63, Thm 2.1 l.86; L06 Assumption 2.1 (EVT) l.72, Thm 2.3 (MVT) l.87; L08 Assumption 1.1 (= L06 Assumption 2.1) l.61, Thm 2.1 (Lagrange) l.90; L24 Assumption 4.1 l.132; L23 Problem R3, Remark 3.4, Section 4 all exist. The L22 reference paragraph's proof chain (L21 Thm 1.3 proved with MVT and IVT) matches L21 l.75-92.")
R("GRADE-theorems", "every theorem/proposition/lemma block carries a grade", "L22.html:63, 73, 239; L23.html:67, 79, 232, 242, 251; L24.html:60, 74, 84, 106, 116", "PASS",
  "Every block-title claim span has data-grade (grep for claim spans without data-grade: none). Grades: L22 Lemma 1.2 T, Thm 1.3 T, Prop 2.1 T; L23 Prop 2.1 T, Prop 2.2 T, Thm 3.1 T, Prop 3.2 T, Prop 3.3 T; L24 Thm 2.1 T, Prop 3.1 T, Prop 3.2 T, Prop 4.2 T, Prop 4.3 T. Key-results tables carry matching grades.")

# ---- mathematics ----
R("MATH-L22-lemma-thm", "Lemma 1.2 and Theorem 1.3 with proofs", "L22.html:62-84", "PASS",
  "Lemma 1.2 proof (l.69) checked: one-sided quotient argument uses J open. Theorem 1.3 proof (l.79-83): f_x=0 from Lemma 1.2 for each a; chain rule with (H1),(H3) gives V' = f_a. Hypotheses (H1)-(H3) match Proposition/Theorem statement l.74-75 and are used.")
R("MATH-L22-remark14", "Remark 1.4 ('where (H3) comes from') hypotheses suffice for its conclusion", "L22.html:86-89 (Remark 1.4); L22.html:473 (reference paragraph repeats the claim); cards.json M2-c326 (see CARD-L22)", "FAIL",
  "The proof sentence 'f_x(x-hat(a),a)=0 by Lemma 1.2' (l.88) needs x-hat(a) to maximize f(.,a), which is (H2). (H2) is not among the Remark's suppositions (l.88 lists only f twice continuously differentiable, f_x=0 and f_xx != 0 at a0, x-hat continuous at a0). Counterexample: f(x,a)=-x^2/2, a0=0, x-hat(a)=|a|. The suppositions hold (f_x(0,0)=0, f_xx=-1, x-hat continuous at 0), but x-hat is not a maximizer for a != 0 and is not differentiable at 0 (difference quotients +1 and -1 from the two sides; ledgers/M2/scripts/M2-d2-r4/remark14_counterexample.out). So the Remark's conclusion '(H3) locally' does not follow as stated. The reference paragraph l.473 repeats the unsupported 'supplied in Remark 1.4'.")
R("MATH-L22-example15", "Example 1.5: maximizer, value function, V'(a), envelope check", "L22.html:91-95", "PASS",
  "f_x = a/(1+x) - 1 vanishes at x = a-1; f_xx = -a/(1+x)^2 < 0; V(a) = a ln a - (a-1); V' = ln a + a(1/a) - 1 = ln a; f_a(x-hat,a) = ln(1+x-hat) = ln a. Assumption 1.1 (d/da ln a = 1/a) stated at l.94 and used.")
R("MATH-L22-prop21-ex22-ex23", "Proposition 2.1 (constraint), Example 2.2 (xy on x+y=a), Example 2.3 (corner), bullets, misconceptions", "L22.html:238-263 and 266-282", "PASS",
  "Prop 2.1 hypotheses (g C^1 on open U containing graph; c C^1; F satisfies (H1)-(H3)); proof chain rule F_a = g_y c_a + g_a checked. Example 2.2: F = x(a-x), F_x = a-2x, x-hat = a/2, V = a^2/4, V' = a/2 = g_y c_a = (a/2)(1). Example 2.3: V = a (a>0), 0 (a<0), V(0)=0; one-sided derivatives 1 and 0; J closed so Thm 1.3 does not apply. Misconception 3 arithmetic: f_xx(1.5) = -0.666667; 0.5 x 0.666667 x 1e-16 = 3.3e-17 (l.279).")
R("MATH-L22-exercises", "problem set M1-M3, P1-P3, E1-E3, R1-R3 and their solutions; quiz answers", "L22.html:290-385 and 406-466", "FAIL",
  "All solutions checked (M1 V=a^2/2, V'=a; M2 x-hat=a+3/2, V=3a+9/4, V'=3; M3 F=x(a-x)/2, y*=a/4, V=a^2/8, V'=a/4; P2 V=max(a,0); E1 a^2-order argument; E2; E3). FAIL at R1 (l.369): 'By Remark 1.4, the condition f_xx(x-hat(a0),a0) != 0 at a point of continuity of x-hat gives it [(H3)]' overstates the Remark. Remark 1.4 gives (H3) only locally, on an interval I around a0, and it needs f twice continuously differentiable and (H2) for a near a0 (see MATH-L22-remark14). Fix: 'gives (H3) locally, on an interval around a0, when f is C^2, x-hat maximizes f(.,a) for a near a0, and x-hat is continuous at a0.'")
R("MATH-L23-prop21-22", "Proposition 2.1 (derivatives) and Proposition 2.2 (price at face)", "L23.html:66-86", "PASS",
  "P' and P'' formulas from term-by-term differentiation (l.75). Signs for positive c_t (l.75). Prop 2.2: v = 1/(1+r), 1-v = rv; sum v^t = (1-v^N)/r; rF sum = F(1-v^N); price F(1-v^N)+Fv^N = F. Case r=0 handled (l.85). Checked numerically: P(0.05) exact rounds to 100000 (recheck output).")
R("MATH-L23-thm31-prop32-33", "Theorem 3.1 (second-order expansion), Proposition 3.2 (sign of remainder), Proposition 3.3 (first-order below price), Remark 3.4", "L23.html:231-264", "PASS",
  "Thm 3.1: Lagrange remainder of order two (L08 Thm 2.1 with n=2), M = max |P'''| on the closed interval, EVT from L06 Assumption 2.1 used for the max. Prop 3.2: P''' = -sum t(t+1)(t+2)c_t(1+y)^(-t-3) < 0, so R has sign of -Delta. Prop 3.3: P - P1 = (1/2)P''(theta)Delta^2 >= 0. Numerically at 0.04: P''' sign consistent with the output (first-order error +403.77, second-order -15.06 at +0.01).")
R("MATH-L24-thm21", "Theorem 2.1 (quotients of |x| at 0)", "L24.html:59-67", "PASS",
  "Forward (|h|-0)/h = 1, backward (0-|-h|)/h = -1, central (|h|-|-h|)/(2h) = 0 for h>0. For h<0 the forward quotient equals -1, so the two one-sided limits differ. Definition of derivative (L04 Def 1.1 l.57, two-sided limit of Q(h)) gives no derivative.")
R("MATH-L24-prop31-32", "Proposition 3.1 (forward truncation) and Proposition 3.2 (central truncation)", "L24.html:73-94", "PASS",
  "Prop 3.1: Taylor order one, D+ - f' = (1/2) h f''(xi), bound (1/2) M2 h. Prop 3.2: expansions at x+h and x-h with xi1, xi2; difference gives D0 - f' = (1/12) h^2 (f'''(xi1)+f'''(xi2)), bounded by (1/6) M3 h^2. Checked both signs in the expansions (l.91-93).")
R("MATH-L24-prop42-43", "Proposition 4.2 (forward bound, minimizer), Proposition 4.3 (central bound, minimizer)", "L24.html:105-123", "PASS",
  "Numerator error <= 2 delta, so quotient error <= 2 delta/h (l.112). g(h)=Ah+B/h with A=M2/2, B=2 delta: h*=sqrt(B/A)=2 sqrt(delta/M2), g=2 sqrt(AB)=2 sqrt(M2 delta). Prop 4.3: quotient error delta/h; g(h)=Ch^2+B/h, C=M3/6, B=delta; g'=0 at h^3 = B/(2C) = 3 delta/M3 (l.122).")
R("MATH-L24-remark44-assumption", "Remark 4.4 and Assumption 4.1", "L24.html:125-132", "PASS",
  "Remark 4.4 says the bound is an upper bound and the true error can be smaller; Lab 1 does not measure delta or M2. Assumption 4.1 (d/dx e^x = e^x) is numbered, stated, and labelled as not proved.")
R("MATH-L24-canon-bullet3", "Section 5 bullet 3: source of the round-off term", "L24.html:252", "PASS",
  "Text now reads: the round-off term 2 delta/h bounds the error of the computed quotient; the numerator error is at most 2 delta; dividing by h gives 2 delta/h. This matches Definition 4.1 and the Prop 4.2 proof (l.112: (delta+delta)/h = 2 delta/h). Round-3 FAIL is fixed.")

# ---- numbers ----
R("N-L22", "numbers in L22 prose vs printed output and derivations", "L22.html:223-231, 279, 344, 358; twin_L22.stdout", "PASS",
  "Printed central differences 0.40546511, 0.69314718, 1.09861229, 1.38629436 equal printed ln a to 8 decimals (l.223-226). x-hat 0.50000001 (l.223). Part B errors 1.9e-13, 1.0e-12, 5.4e-12 (l.228-230; 5.4e-12 is the largest). Derived: f_xx(1.5)=-0.6667; 1/2 x 0.6667 x 1e-16 = 3.3e-17 (l.279). Lab prints no error of V (checked against the lab code).")
R("N-L23", "numbers in L23 prose vs printed output and derivations", "L23.html:51, 90, 226, 271, 308, 318, 343, 366, 368, 481", "FAIL",
  "Printed values and derivations check: P(0.04)=108110.895779 (rounds to 108111); P'=-851466.7395; P''=8376648.5119; -P'/P=7.875864; P''/P=77.482001; second-order error at +0.01 = -15.0608; exact-expansion at -0.01 = +16.010; first-order error 403.77; ratios 3.9279, 3.9634, 7.8807, 7.9396; card example -1777.07. FAIL at L23.html:368 (E3 solution): 'the float yield the lab uses differs from 5 percent by about 2.8e-18, which moves the unrounded price by about 2.1e-12 cents'. The sentence gives no calculation and cites nothing (the round-4 delta removed the earlier 'both are computed here with Fraction'). The values are right (independent Decimal recomputation: float 0.04+0.01 minus 0.05 = 2.78e-18; P'(0.05) x offset = -2.14e-12; ledgers/M2/scripts/M2-d2-r4/recheck_L24_L23_numbers.out), but the page must show them. Fix: state the calculation, e.g. 'the float 0.04 + 0.01 differs from 0.05 by 2.78e-18 (exact arithmetic); P'(0.05) = -7.72e5 cents per unit of yield, so the price moves by about -2.1e-12 cents.'")
R("N-L24", "numbers in L24 prose vs printed output and derivations (including the unprinted E3 values)", "L24.html:136, 243, 341, 348, 359", "PASS",
  "Printed errors checked against twin_L24.stdout (forward 1.406e-01 to 1.359e-05; 6.603e-09; 2.154e-07; 3.263e-05; 3.903e-01; central 4.531e-09, 5.859e-11, 1.635e-10). Recomputed (recheck output): E3 unrounded central errors 5.858691310e-11 at 1e-5 and 5.858735719e-11 at 1e-7, difference 4.440892e-16 = exactly one ulp of e (2^-51). Half ulp of e = 2.22e-16 = delta, as L24.html:136 says. 2 sqrt(delta/e) = 1.8074e-8; (3 delta/e)^(1/3) = 6.2574e-6. E2 bound 2 delta/1e-15 = 0.444 vs printed 0.390. 4.531e-9/5.859e-11 = 77.3. 1/2 e h at 1e-5 = 1.3591e-5.")
R("N-L22-L23-L24-quiz", "quiz numeric answers and their explanations", "L22.html:417-457; L23.html:437-463; L24.html:417-453", "PASS",
  "L22: V=a^2/2 at a^2=5 gives 2.5; Example 2.2 V'(1)=1/2; M3 V'(1)=1/4. L23: price 1000 (Prop 2.2); P'(0)=-200 for 100(1+y)^-2. L24: central quotient of x^2 = 2; h* with delta=0.5, M2=2 equals 1 (2 sqrt(0.25)). All match.")

# ---- labs ----
R("LAB-L22", "lab page code, expected block and interpretation", "course/modules/M/M2/L22.html:97-232; tests/labs/M2/lab-M2-L22-1.py", "PASS",
  "Twin read in full (122 lines); golden-section, objective, central differences, naive partial all match the docstring and the prose (l.99, 231). Expected block equals twin stdout (G-expected-blocks). Twin run alone under -I -W error: rc 0, no stderr.")
R("LAB-L23", "lab page code, expected block and interpretation", "course/modules/M/M2/L23.html:88-227; tests/labs/M2/lab-M2-L23-1.py:1-17 and 88-122", "PASS",
  "Twin read in full (124 lines). Docstring claims (Fraction arithmetic, float sensitivities with relative error 2^-53, round-half-even via Fraction round, Part A/B/C structure, previews not defined) match the code. Interpretation (l.226) matches stdout; numbers rechecked in Decimal.")
R("LAB-L24", "lab page code, expected block and interpretation", "course/modules/M/M2/L24.html:134-244; tests/labs/M2/lab-M2-L24-1.py:1-13", "PASS",
  "Twin read in full (81 lines). Docstring: Part A prints +1, -1, 0 at six steps (matches stdout); Part B decade grid k=1..15 (matches stdout); 'The lab computes no limit'. Page prose (l.243) matches stdout values. Hypothesis (l.136) matches the lab (delta is an assumption).")

# ---- cards ----
R("CARD-L22", "every L22 card: grade and basis match the claim; hypotheses carried; numbers appear in the lesson", "course/modules/M/M2/cards.json: M2-c323..c337 and M2-c404 (15 cards); c326 is the failing card", "FAIL",
  "All 15 cards read in full. Numbers in c328 (0.40546511, 0.69314718, 1.09861229, 1.38629436) and c329 (0.5, 1.0, 1.5; 5.4e-12) appear in L22.html:223-231. c324, c325, c327, c330, c331, c332, c335 match the statements (Prop 2.1 hypotheses carried in c331). FAIL at M2-c326 (ungraded): 'It can be obtained locally from Theorem 1.3 of Lesson 21 when f is twice continuously differentiable, f_x = 0 and f_xx is not 0 at the optimum, and x_hat is continuous' omits (H2), which the proof uses (see MATH-L22-remark14). Fix: add 'and x_hat(a) maximizes f(., a) for a near the point (H2)'.")
R("CARD-L23", "every L23 card: grade and basis match; hypotheses carried; numbers appear in the lesson", "course/modules/M/M2/cards.json: M2-c338..c357, c382..c386, c407 (24 cards)", "PASS",
  "All 24 read in full. Lab-number cards (c341, c342, c343, c345, c346, c382-c385, c407) carry grade C with basis naming Lab 1 and their numbers appear in L23.html:215-225 or l.226 (108110.895779, -851466.739529, 1.6e-03, 8376648.511919, 1.9, 4.037716e+02, 3.9279, 3.9634, 108111, 117060, -1.506081e+01, 7.8807, 7.9396, 100000). T cards c339, c340, c348, c349, c350, c353, c354 carry no lab numbers and state the lesson's hypotheses (c349 and c350 carry Assumption 2.1 of L06). c353 and c354 no longer carry lab numbers (round-3 FAIL fixed).")
R("CARD-L24", "every L24 card: grade and basis match the claim; hypotheses carried; numbers appear in the lesson", "course/modules/M/M2/cards.json: M2-c358..c373, c375, c387, c405 (17 cards); M2-c370 regraded", "PASS",
  "All 17 read in full. M2-c370 is now grade C with basis 'Lab 1 Part B prediction (assumed delta; M_2 and M_3 approximately e; not measured)'; its front and back say approximately e and assumed delta, and the lesson (l.136, l.251) calls them model inputs, so the round-3 FAIL is resolved. c360 and c361 carry the Prop 3.1/3.2 hypotheses; c363 and c364 carry the Prop 4.2/4.3 hypotheses and the minimizers; c367 and c368 numbers appear at L24.html:226-243. c362 matches Definition 4.1.")
R("CARD-scan-dup", "duplicate card ids and fronts in cards.json", "course/modules/M/M2/cards.json (394 cards)", "PASS",
  "No duplicate id among the 56 slice cards. One normalised-front collision reported by the script is 'P'(y0)' vs 'P''(y0)' (M2-c342, M2-c343), which are different questions, not duplicates.")
R("CARDS-dup", "duplicate cards across the three lessons", "course/modules/M/M2/cards.json", "PASS",
  "No card in the slice repeats another card's question or claim. c407 restates the lab's printed price at 0.05 (not the theorem), so it is not a duplicate of c353.")
R("L24-prop-3.1-hypothesis", "Proposition 3.1 hypotheses on the page", "course/modules/M/M2/L24.html:74-81", "PASS", "Statement l.75: twice differentiable on an open interval containing [x,x+h]; f'' bounded by M2; EVT assumed (L06 Assumption 2.1). Used in the proof by Lagrange order one.")
R("L24-prop-3.2-hypothesis", "Proposition 3.2 hypotheses on the page", "course/modules/M/M2/L24.html:84-94", "PASS", "Statement l.85: three times differentiable on an open interval containing [x-h,x+h]; f''' bounded by M3. Proof uses order-two Lagrange remainder at x+h and x-h (l.90-93).")
R("L24-simulated-label", "SIMULATED label for the exp function", "course/modules/M/M2/L24.html:136; tests/labs/M2/lab-M2-L24-1.py:3", "PASS", "Lab hypothesis: 'SIMULATED: both functions are test functions chosen for this lab, not market data.' Twin docstring line 3 says the same.")
R("L23-P3-order", "proof order in L23 problem set P3 and Prop 3.3", "course/modules/M/M2/L23.html:343", "PASS", "P3 solution uses Lagrange form of order one with P''(theta)>0 and gives Prop 3.3; order of results consistent with L23.html:252-259.")
R("L24-cards", "L24 cards M2-c360 and M2-c361 vs Propositions 3.1 and 3.2", "course/modules/M/M2/cards.json: M2-c360, M2-c361", "PASS", "c360 states Prop 3.1 hypotheses and the bound (1/2) M2 h; c361 states Prop 3.2 hypotheses and (1/6) M3 h^2; both match L24.html:74-94.")
R("FWD-L23-lab-prediction", "forward pointers in the lab prediction and why-it-matters", "course/modules/M/M2/L23.html:51 and 90; L22.html:51", "PASS",
  "Pointers name results in the same lesson (Theorem 3.1, Proposition 3.2, Section 3). Per the round-3 ruling they are not counted as uses before definition.")
R("CURRIC-FI1-title", "unit name quoted from the curriculum", "course/modules/M/M2/L23.html:90 ('unit FI1 of the curriculum (Bond Math and Curve Construction)')", "FAIL",
  "curriculum/03-markets.yaml:19-21 gives FI1 the title 'Bond Math & Curve Construction'. The page writes 'and'. The FI1 content claim itself holds: its core lists duration and convexity (03-markets.yaml:22-24). Fix: write 'Bond Math & Curve Construction'.")

rows_sorted = rows
fail = sum(1 for r in rows if r["status"] == "FAIL")
passn = sum(1 for r in rows if r["status"] == "PASS")
unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
frag = {
  "unit": "M2",
  "slice": "d2",
  "round": 4,
  "verifier": "Claude Haiku 5.5, independent verifier for M2-d2, round 4 (did not build M2). Full read of L22, L23, L24 and the three twins; no round-3 PASS row carried; every row re-derived on pin 4eb6788.",
  "pin": "4eb6788",
  "base": "a007712 (round-3 pin). Delta a007712..4eb6788 touches this slice in L22.html (meta description l.7, Uses row l.37, why-it-matters, L22 remark 3 bullet l.27, R2 l.36-40), L23.html (Uses row l.37, why-it-matters l.51, Def 1.1 l.59, lab hypothesis l.79-80, E3 solution l.87-89, R1 l.97), L24.html (Uses row l.110, proof of Thm 2.1 l.120, interpretation l.128-129, canon bullet 3 l.137-138, E2 l.146, R3 l.155) and cards.json (c296-c319 are L20/L21; c370 regraded). The three twins and plans/M2-build-plan.md did not change in the delta.",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyD4-M2-d2 (detached at 4eb6788; .venv symlinked)",
  "scratch": "/Users/billyribeiro/.fanout/wt/verifyD4-M2-d2/ledgers/M2/scripts/M2-d2-r4",
  "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "verdict": "FAIL" if (fail or unv) else "PASS",
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": "Round 4 on 4eb6788. Full read of L22, L23, L24 (every sentence, every card, every problem solution) and of the three twins (every line). No round-3 PASS row was carried: all rows re-derived. Gates run on the pin: check_pages (M2 and per page), check_dag (M2 and --all), check_projects, run_labs (per page and M2), twins alone under python -I -W error, page_smoke for the three pages alone, ruff check and format on the twins, mypy --no-incremental on the twins, pytest for test_labs (M2 cases) and test_page_checks/test_run_labs, verify_refs --offline. No grader in this slice: run_graders, mutate_graders and project mutants are not applicable (rulings: lab twins are demonstrations; mutation testing applies to project graders only). Page lab code equals the twin and expected blocks equal stdout, modulo the final newline (HTML embedding convention). Four FAIL rows come from defects in this round's pin: Remark 1.4 omits (H2) (counterexample reproduced), so R1, the exercises row and card c326 inherit it; the E3 numbers sentence (L23.html:368) has lost its calculation; the FI1 unit title differs from the curriculum. Round-3 FAIL rows DAG-links, MATH-L24-canon-bullet3 and CARD-L24 are fixed and re-verified PASS (DAG links now in the Uses rows and at the problem sites; the bullet matches Definition 4.1; c370 is graded C with its basis).",
  "summary": f"slice d2: {len(rows)} rows, {passn} PASS, {fail} FAIL, {unv} UNVERIFIABLE. Mutants 0 (no grader in this slice)."
}
path = "ledgers/M2/M2-d2.json"
json.dump(frag, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "pass", passn, "fail", fail, "unv", unv, "verdict", frag["verdict"])
