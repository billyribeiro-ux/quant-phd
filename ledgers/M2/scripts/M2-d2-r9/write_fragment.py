import json, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD9-M2-d2/tools")
S = "ledgers/M2/scripts/M2-d2-r9"
R = []
def row(i, check, loc, ev, status="PASS"):
    R.append({"id": i, "check": check, "location": loc, "status": status, "evidence": ev})

row("G-check-pages", "2.9 structure: tools/check_pages.py --unit M2 --page L22/L23/L24, and unit-wide",
    "course/modules/M/M2/L22.html, L23.html, L24.html",
    f"{S}/gates_pages_dag_labs.out: 'check_pages M2 L22: PASS', 'L23: PASS', 'L24: PASS' (rc 0 each); 'check_pages M2: PASS' rc 0.")
row("G-check-dag", "2.9 DAG: tools/check_dag.py --unit M2", "course/modules/M/M2/L22.html..L24.html",
    f"{S}/gates_pages_dag_labs.out: 'check_dag M2: PASS' rc 0.")
row("G-run-labs", "2.5 labs: tools/run_labs.py --unit M2 --page L22/L23/L24",
    "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py",
    f"{S}/gates_pages_dag_labs.out: 'run_labs M2: PASS (1/1)' for each of the three pages, rc 0.")
row("G-twin-isolated", "2.5 labs: each twin under python -I -W error from an empty scratch cwd",
    "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py",
    f"Run by me: cd /tmp/m2d2r9_<L> && .venv/bin/python -I -W error <twin>; rc=0 and stderr 0 bytes for L22, L23, L24 ({S}/twin_L2x_stderr.txt); stdout saved in {S}/twin_L2x_stdout.txt.")
row("G-page-code-equals-twin", "2.5 labs: embedded code block equals the twin",
    "course/modules/M/M2/L22.html:100-221, L23.html:91-214, L24.html:137-217",
    f"{S}/extract_compare.out: 'code==twin (modulo trailing newline): True' for L22, L23, L24 (strict byte equality differs only by the final newline, as run_labs allows).")
row("G-expected-equals-live", "2.5 labs: expected block equals live stdout, exact text",
    "course/modules/M/M2/L22.html:222-230, L23.html:215-225, L24.html:218-242",
    f"{S}/extract_compare.out: 'expected==live stdout: True' for L22, L23, L24 (after trailing-newline normalization); live stdout in {S}/twin_L2x_stdout.txt.")
row("G-page-smoke-L22", "2.9 page_smoke, L22 alone", "course/modules/M/M2/L22.html",
    f"{S}/page_smoke_r9.out: 'page_smoke modules/M/M2/L22.html: PASS' rc 0 (command tools/page_smoke.py --unit M2 --pages L22).")
row("G-page-smoke-L23", "2.9 page_smoke, L23 alone", "course/modules/M/M2/L23.html",
    f"{S}/page_smoke_r9.out: 'page_smoke modules/M/M2/L23.html: PASS' rc 0.")
row("G-page-smoke-L24", "2.9 page_smoke, L24 alone", "course/modules/M/M2/L24.html",
    f"{S}/page_smoke_r9.out: 'page_smoke modules/M/M2/L24.html: PASS' rc 0.")
row("G-ruff-mypy-twins", "tooling: ruff check, ruff format --check, mypy --no-incremental on the three twins",
    "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py",
    f"{S}/gates_tooling_r9.out: 'All checks passed!', '3 files already formatted', 'Success: no issues found in 3 source files'.")
row("G-pytest-labs-M2", "tooling: pytest tests/test_labs.py -q -k M2", "tests/test_labs.py",
    f"{S}/pytest_labs_M2_r9.out: 27 passed; {S}/pytest_rc.txt: 'pytest rc=0'.")
row("G-verify-refs-offline", "2.1 citations: tools/verify_refs.py --offline (whole registry)", "references/references.json",
    f"{S}/verify_refs_offline_r9.out: 'offline integrity: 560 entries, 0 problems', rc 0. The live run needs the network and was not run; the slice cites no key with a locator.")
row("G-links-anchors", "2.9 structure: every internal href and fragment on L22-L24 resolves", "course/modules/M/M2/L22.html, L23.html, L24.html",
    f"{S}/links_check.py (run by me): 26 internal hrefs and fragments checked, 0 missing files or ids.")
row("G-cards-dup-scan", "2.7 cards: unit-wide duplicate scan of cards.json (395 cards)", "course/modules/M/M2/cards.json",
    f"{S}/cards_dupscan.out: 395 cards; no duplicate ids; no duplicate backs; the only normalized-front collision is cards c342 and c343, a false positive of the normalization (the primes in P'(y0) and P''(y0) are stripped).")
row("G-notation", "3.2 notation: every macro against notation/notation.json; no registered symbol reused",
    "course/modules/M/M2/L22.html, L23.html, L24.html",
    "Macros used on the three pages: \\R (registered, 4 uses on L22), \\hat, \\tilde, \\mathcal, \\tfrac and other standard LaTeX; no \\mathbb{R} (count 0 on each page). Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q are not used as math symbols on the pages (the bare T is the grade label). The remainder R(Delta) and the price P are not registered symbols.")
row("N-L22-xhat-error", "2.2 numbers (rule 1): x-hat printed error, displayed digits vs unrounded values, sqrt(eps), 3.3e-17",
    "course/modules/M/M2/L22.html:231 (interpretation), :279 (misconception 3), :342 (E1)",
    f"Round-8 defect now fixed. Twin output (tests/labs/M2/lab-M2-L22-1.py, {S}/twin_L22_stdout.txt): x_hat printed 0.50000001, 1.00000001, 1.99999999, 2.99999998 for a=1.5,2,3,4, so the printed errors are 1e-8, 1e-8, 1e-8, 2e-8. Unrounded errors computed by me ({S}/l22_unrounded.py): 1.3663e-8, 0.7059e-8, -0.7235e-8, -2.1738e-8, which round to the page's 1.37, 0.71, 0.72, 2.17 (x1e-8). f_a(x_hat,1.5)-ln(1.5) = 9.109e-9 (page: last digit differs). f_xx = -0.6666667 and 0.5*0.6667*1e-16 = 3.33e-17 (page: 3e-17).")
row("N-L22-partB-5.4e-12", "2.2 numbers: Part B central differences agree with a/2 to within 5.4e-12; naive partial prints 0",
    "course/modules/M/M2/L22.html:231, card M2-c329",
    f"{S}/twin_L22_stdout.txt: errors 1.9e-13, 1.0e-12, 5.4e-12 at a=1,2,3; naive partial 0.00000000 (lab code line 114 uses frozen_product, zero derivative).")
row("N-L22-partA-ln", "2.2 numbers: Part A central differences equal ln a to eight decimals", "course/modules/M/M2/L22.html:231, card M2-c328",
    f"{S}/twin_L22_stdout.txt: central differences 0.40546511, 0.69314718, 1.09861229, 1.38629436 equal ln a to 8 decimals; exact V' from V=a ln a-(a-1) equals ln a (checked in l22_unrounded.py).")
row("N-L23-price-cents", "2.2 numbers: unrounded price 108110.895779, integer 108111; P'(y0), P''(y0) and their central-difference differences",
    "course/modules/M/M2/L23.html:226, expected block :216-219, cards M2-c341..c343, c382",
    f"{S}/l23_check.py (60-digit Decimal): P(0.04)=108110.8957793550, rounds to 108111; P'(0.04)=-851466.7395286, P''(0.04)=8376648.5119195; these match the twin output and the page. Central-difference differences 1.6e-3 and 1.9 are as printed.")
row("N-L23-ratios-and-shifts", "2.2 numbers: first- and second-order errors, ratios 3.9279/7.8807 and 3.9634/7.9396",
    "course/modules/M/M2/L23.html:51, :226, :281; cards M2-c345, c346, c384, c385",
    f"{S}/l23_check.py: errors e1 = 4.037716e+02, 1.027970e+02, 2.593632e+01; e2 = -1.506081e+01, -1.911100e+00, -2.407040e-01; ratios 3.9279, 7.8807, 3.9634, 7.9396 (recomputed).")
row("N-L23-cents-minus15-plus16", "2.2 numbers: exact minus second-order expansion; whole cents -15 and +16; unrounded -15.06",
    "course/modules/M/M2/L23.html:51, :226, :281; cards M2-c352, c383",
    f"{S}/l23_check.py: unrounded second-order error at +0.01 = -15.060810 cents; integer: exact 100000 - expansion 100015 = -15; at -0.01 exact 117060.41 -> 117060, expansion 117044, difference +16.")
row("N-L23-E3-offset", "2.2 numbers: float 0.04+0.01 vs 1/20, offset 2.78e-18; P'(0.05); price move -2.1e-12",
    "course/modules/M/M2/L23.html:368 (E3 solution)",
    f"{S}/l23_check.py: float(0.04)+float(0.01) == 0.05 is True; its exact value minus 1/20 = 2.7756e-18 (page 2.78e-18); P'(0.05) = -772173.49 (page -7.72e5); P'(0.05)*offset = -2.14e-12 (page -2.1e-12); float price at that yield rounds to 100000.")
row("N-L23-previews", "2.2 numbers: preview -P'/P = 7.875864 and P''/P = 77.482001 (printed only)",
    "course/modules/M/M2/L23.html:90 (hypothesis), :226",
    f"{S}/l23_check.py (decimal): -P'/P = 7.8758643, P''/P = 77.4820008; twin prints 7.875864 and 77.482001.")
row("N-L23-two-cash-flows", "2.2 numbers: quiz explanation P'(0.04) = -1777.07 for c1 = -1, c2 = 1000",
    "course/modules/M/M2/L23.html:481 (quiz Q8 explanation)",
    f"{S}/l23_check.py: -(1*(-1)/1.04^2 + 2*1000/1.04^3) = -1777.0682, which rounds to -1777.07.")
row("N-L23-M1-M3", "2.2 numbers: M1 price 50/1.05 + 1050/1.05^2 = 1000.000; M3 zero-coupon derivative formula",
    "course/modules/M/M2/L23.html:304 (M1 solution), :318 (M3 solution), quiz :463",
    f"{S}/l23_check.py: 50/1.05 + 1050/1.05^2 = 1000.000000 exact; M3 P(y)=100(1+y)^-2 gives P'=-200(1+y)^-3, P'(0.04)=-200/1.04^3.")
row("N-L24-remark44-numbers", "2.2 numbers: exact forward error +1.359e-8 at h=1e-8; computed error -6.603e-9",
    "course/modules/M/M2/L24.html:129 (Remark 4.4), :243, card M2-c365",
    f"{S}/l24_check.py: exact forward error at 1e-8 = +1.3591409e-8 (decimal); computed forward quotient signed error at 1e-8 = -6.602751e-09 (python float, same formula as the twin); twin prints magnitude 6.603e-09.")
row("N-L24-E3-unrounded", "2.2 numbers: unrounded central quotient errors 5.858691e-11 (1e-5) and 5.858736e-11 (1e-7)",
    "course/modules/M/M2/L24.html:348 (E3 solution)",
    f"{S}/l24_check.py: central(1,1e-5)-e = 5.858691309867936e-11; central(1,1e-7)-e = 5.858735718788921e-11 (six-digit rounding 5.858691, 5.858736 as the page states).")
row("N-L24-E3-difference", "2.2 numbers (rule 1, unrounded vs displayed digits): unrounded difference of the two errors",
    "course/modules/M/M2/L24.html:348 (E3 solution), :243",
    f"{S}/l24_check.py: difference = -4.440892e-16 = 2^-51 (one ulp of values in [2,4)); page 4.4e-16 with 'one unit in the last place'; the six-digit values differ by 4.5e-16, explained by rounding as the page says.")
row("N-L24-E3-exact-and-grid", "2.2 numbers: exact central error e(sinh h/h - 1) at 1e-5, 1e-6, 1e-7; grid spacing 2.2e-16/h; round-off about 1.3e-11",
    "course/modules/M/M2/L24.html:348",
    f"{S}/l24_check.py: exact central error 4.530470e-11 (1e-5), 4.530470e-13 (1e-6), 4.530470e-15 (1e-7); printed 5.858691e-11 minus exact = 1.3282e-11 (page about 1.3e-11); spacing ulp(e)/(2h) = 2.22e-16/h gives 2.2e-11 at 1e-5 and 2.2e-9 at 1e-7.")
row("N-L24-minimizers", "2.2 numbers: predicted minimizers 2 sqrt(delta/e) = 1.8e-8 and (3 delta/e)^(1/3) = 6.3e-6",
    "course/modules/M/M2/L24.html:136 (hypothesis), :346-348, card M2-c370",
    f"{S}/l24_check.py: 2*sqrt(2.22e-16/e) = 1.8074e-8; (3*2.22e-16/e)^(1/3) = 6.2574e-6 (page 6.3e-6).")
row("N-L24-E2-roundoff-bound", "2.2 numbers: round-off bound 2 delta/h = 0.444 at h = 1e-15; printed error 0.390",
    "course/modules/M/M2/L24.html:341 (E2 solution), expected block :240",
    f"2*2.22e-16/1e-15 = 0.444 ({S}/l24_check.py); twin output 3.903e-01 at k=15 (expected block line 240). 0.390 <= 0.444, consistent with the stated model.")
row("N-L24-half-ulp", "2.2 numbers: delta = 2.22e-16 described as half a unit in the last place of values near e",
    "course/modules/M/M2/L24.html:136",
    f"{S}/l24_check.py: ulp for [2,4) = 2^-51 = 4.44e-16, half = 2.22e-16.")
row("N-L24-decade-ratios", "2.2 numbers: central errors fall x100 per decade to 1e-4; 4.531e-9 / 5.859e-11 = 77",
    "course/modules/M/M2/L24.html:243 (interpretation)",
    f"Twin output: central errors 4.533e-03, 4.530e-05, 4.530e-07, 4.531e-09 (ratios 100.07, 100.0, 100.0); {S}/l24_check.py: 4.531e-9/5.859e-11 = 77.33.")
row("N-L24-M3-numbers", "2.2 numbers: M3 forward quotient 12.61, error 0.61, bound 0.63 with M2 = 12.6",
    "course/modules/M/M2/L24.html:298 (M3 solution)",
    "(2.1^3 - 2^3)/0.1 = 12.61 exactly; error 12.61 - 12 = 0.61; sup|6x| on [2,2.1] = 12.6; 0.5*12.6*0.1 = 0.63 >= 0.61.")
row("LAB-L22-statements", "2.5 labs: L22 hypothesis, docstring, interpretation and E-problems vs code and output",
    "course/modules/M/M2/L22.html:99, :100-112 (twin docstring), :231",
    "Read the twin source line by line (tests/labs/M2/lab-M2-L22-1.py:1-13 docstring, :26-48 golden search, :56-63 maximizers, :106-119 Part B). Claims checked: maximizer a-1, V=a ln a-(a-1), step 1e-4, naive partial zero, substitution y=a-x on [0,a], 4 and 3 parameter values; each matches the code and the printed output.")
row("LAB-L23-statements", "2.5 labs: L23 hypothesis, docstring and interpretation vs code and output",
    "course/modules/M/M2/L23.html:90, :91-107, :226",
    "Twin docstring (tests/labs/M2/lab-M2-L23-1.py:1-18): Fraction arithmetic, round half to even via Fraction round(), sensitivities rounded once to float, previews only printed. Part B steps 0.01, 0.005, 0.0025 (:30, :105-113); Part C shifts +-0.01 (:115-121). Each claim matches the code and output.")
row("LAB-L24-statements", "2.5 labs: L24 hypothesis, docstring and interpretation vs code and output",
    "course/modules/M/M2/L24.html:136, :137-149, :243",
    "Twin docstring (tests/labs/M2/lab-M2-L24-1.py:1-13): kink quotients +1/-1/0 at six steps (:20, :35-53); e^x at x0=1 with k=1..15 and decade grid (:21-22, :68-78). Printed minima 1e-8 (forward) and 1e-5 (central) follow from the printed table, as the page states.")
row("LAB-L22-L24-expected", "2.5 labs: run_labs expected blocks and tolerance",
    "course/modules/M/M2/L22.html:222, L23.html:215, L24.html:218",
    f"{S}/extract_compare.out and {S}/gates_pages_dag_labs.out: expected blocks equal live stdout, data-tolerance 1e-6 declared; no tolerance-dependent claim in the prose.")
row("GR-L22-T", "2.3 grades: Lemma 1.2, Theorem 1.3, Proposition 2.1 and Example 2.3 graded T",
    "course/modules/M/M2/L22.html:63, :73, :239, :256, key results :395-398",
    "Each T-graded claim has a proof on the page (Lemma 1.2 :67-70; Theorem 1.3 :78-84; Proposition 2.1 :240-246 with its proof; Example 2.3 computed directly). Example 1.5 and Example 2.2 are not graded T in the page, consistent with the key-results table.")
row("GR-L23-T", "2.3 grades: Propositions 2.1, 2.2, 3.2, 3.3 and Theorem 3.1 graded T",
    "course/modules/M/M2/L23.html:67, :79, :232, :242, :252, key results :405-409",
    "Each has a proof on the page (Prop 2.1 :73-76; Prop 2.2 :83-86; Thm 3.1 :233-248; Prop 3.2 :242-248; Prop 3.3 :252-258). Hypotheses (Assumption 2.1 of L06 where used) are stated.")
row("GR-L24-T", "2.3 grades: Theorem 2.1, Propositions 3.1, 3.2, 4.2, 4.3 graded T",
    "course/modules/M/M2/L24.html:60, :74, :84, :106, :116, key results :385-389",
    "Each has a proof on the page (Thm 2.1 :62-67; Prop 3.1 :76-80; Prop 3.2 :86-93; Prop 4.2 :107-113; Prop 4.3 :117-123). Assumption 2.1 of L06 cited in each.")
row("M-L22-lemma-thm", "2.4 math: Lemma 1.2 and Theorem 1.3 proofs", "course/modules/M/M2/L22.html:63-83",
    "Lemma 1.2 quotient argument checked; Theorem 1.3 chain-rule step and V'=f_a at x-hat checked; the hypotheses (H1)-(H3) are used where needed.")
row("M-L22-remark14", "2.4 math: Remark 1.4 (local (H3) from the implicit-function theorem)", "course/modules/M/M2/L22.html:88",
    "G(a,x)=f_x(x,a), partial in x is f_xx != 0; L21 Theorem 1.3 (IFT) gives a differentiable local solution; uniqueness of zero in K from L21's 'exactly one zero'; Lemma 1.2 applies by (H2). Cross-lesson numbering verified in course/modules/M/M2/L21.html (Assumption 1.2 = IVT, Theorem 1.3 = IFT).")
row("M-L22-example15", "2.4 math: Example 1.5 (logarithmic objective)", "course/modules/M/M2/L22.html:91-95",
    "f_x = a/(1+x)-1 zero at a-1; f_xx = -a/(1+x)^2 < 0; V = a ln a-(a-1); V' = ln a; f_a = ln(1+x-hat) = ln a (checked by hand and numerically, l22_unrounded.py).")
row("M-L22-prop21", "2.4 math: Proposition 2.1 (a constraint solved for one variable)", "course/modules/M/M2/L22.html:240-246",
    "Hypotheses (g C1 on open U in R^3; c C1; F satisfies H1-H3) stated; chain rule F_a = g_y c_a + g_a; Theorem 1.3 applied to F. No gap found.")
row("M-L22-example22-23", "2.4 math: Example 2.2 (xy on x+y=a) and Example 2.3 (max ax on [0,1])", "course/modules/M/M2/L22.html:251, :256",
    "Example 2.2: F = x(a-x), x-hat = a/2, V = a^2/4, g_y c_a = a/2. Example 2.3: V = max(a,0); one-sided derivatives 1 and 0 at a=0; the kink statement is correct.")
row("M-L22-problems", "2.4 math: problem-set solutions M1-M3, P1-P3, E1-E3, R1-R3 (L22)", "course/modules/M/M2/L22.html:290-386",
    "Each solution re-derived: M1 (x-hat=a, V=a^2/2, V'=a), M2 (x-hat=a+3/2, V=3a+9/4, V'=3), M3 (y=(a-x)/2, c_a=1/2, V=a^2/8, V'=a/4), P2 (V=max(a,0)), E1-E3 claims match the lab output, R1-R3 statements correct and hedged where unproved.")
row("M-L23-prop21-22", "2.4 math: Proposition 2.1 derivatives and sign; Proposition 2.2 (price at face)", "course/modules/M/M2/L23.html:69-85",
    "P', P'' closed forms re-derived by differentiating the sum; signs argued term by term; Prop 2.2 geometric-series computation 1-v = rv re-derived; r=0 case handled.")
row("M-L23-thm31-prop32", "2.4 math: Theorem 3.1 (remainder bound) and Proposition 3.2 (sign of the remainder)", "course/modules/M/M2/L23.html:233-248",
    "Lagrange remainder R = P'''(theta) Delta^3/6; P''' = -sum t(t+1)(t+2) c_t (1+y)^(-t-3) re-derived; sign of R equals sign of -Delta. M finite by Assumption 2.1 of L06 (EVT).")
row("M-L23-prop33", "2.4 math: Proposition 3.3 (first-order expansion lies below the price)", "course/modules/M/M2/L23.html:252-258",
    "P - P1 = P''(theta) Delta^2 / 2 >= 0 since P'' > 0 (Prop 2.1). No gap.")
row("M-L23-problems", "2.4 math: L23 problem set M1-M3, P1-P3, E1-E3, R1-R3", "course/modules/M/M2/L23.html:300-395",
    "M1 1000.000 (checked), M2 single cash flow derivatives (checked), M3 zero-coupon P'(0.04) = -200/1.04^3 (checked); P1 via Corollary 3.1(ii) of L06 (checked: L06 Corollary 3.1 (ii) says f' > 0 implies increasing); P2, P3 correct; E1-E3 consistent with the printed output; R1 (IFT with dy/dP = 1/P'), R2, R3 correct.")
row("M-L24-thm21-prop31-32", "2.4 math: Theorem 2.1, Propositions 3.1 and 3.2", "course/modules/M/M2/L24.html:60-93",
    "|x| quotients +1/-1/0 re-derived; Prop 3.1 Lagrange order one; Prop 3.2 Taylor order two with the two Lagrange remainders; difference divided by 2h gives 1/12 h^2 (f'''(xi1)+f'''(xi2)), bound 1/6 M3 h^2. Correct.")
row("M-L24-prop42-43", "2.4 math: Propositions 4.2 and 4.3 (bound functions and minimizers)", "course/modules/M/M2/L24.html:107-123",
    "Prop 4.2: g = A h + B/h with A=M2/2, B=2 delta; h* = sqrt(B/A) = 2 sqrt(delta/M2); g(h*) = 2 sqrt(M2 delta) (checked). Prop 4.3: C=M3/6, B=delta; h^3 = B/(2C) = 3 delta/M3 (checked).")
row("M-L24-remark44-assumption", "2.4 math (round-6 FAIL re-verified): Remark 4.4 claims about the bound at h* and the error",
    "course/modules/M/M2/L24.html:129; card M2-c365",
    "Re-verified from scratch: the bound is guaranteed at h* only if h* in H (Prop 4.2 statement); the signed exact and computed errors at 1e-8 have opposite signs (see N-L24-remark44-numbers); the page now says the computed magnitude only is printed. Correct.")
row("M-L24-problems", "2.4 math: L24 problem set M1-M3, P1-P3, E1-E3, R1-R3", "course/modules/M/M2/L24.html:281-375",
    "M1 (h, -h, 2 exact), M2 (0 and 1), M3 (12.61, 0.61, 0.63); P1 (kink) and P2 (Prop 3.1 proof) correct; P3 rewrite x/(sqrt(1+x)+1) re-derived; E1-E3 numbers match the output and the unrounded checks; R1 (overestimate by 100 gives ten times the round-off term: 2 delta/h = 10 sqrt(M2 delta)) re-derived; R2 Lipschitz bound correct; R3 correct.")
row("CARD-L22", "2.7 cards: all 15 L22 cards (M2-c323..c337 present ids, c404) against the current L22 text",
    "course/modules/M/M2/cards.json (lesson L22)",
    f"{S}/cards_slice.txt: every L22 card read; each agrees with the current L22 text (Def 1.1, Lemma 1.2, Thm 1.3, Remark 1.4, Ex 1.5, lab values c328/c329/c336, Ex 2.2, Prop 2.1 hypotheses, Ex 2.3, Misconceptions 1-3, Section 2). Card c326 says Assumption 1.2 and 2.1 of L6 are 'assumed there and not proved', consistent with L21 and L06.")
row("CARD-L23", "2.7 cards: all 24 L23 cards (M2-c338..c357, c382..c386, c407) against the current L23 text",
    "course/modules/M/M2/cards.json (lesson L23)",
    f"{S}/cards_slice.txt: all 24 read. Numbers in c341-c346, c352, c382-c385, c407 appear in the L23 text or expected block; c340 Prop 2.2 hypotheses stated; c348-c350 Theorem 3.1 and Props 3.2, 3.3 carry their hypotheses (Assumption 2.1 of L06, y0 > -1); c347 and c351 'not defined / no size' match Remark 3.4 and the preview sentence.")
row("CARD-L24", "2.7 cards: all 18 L24 cards (M2-c358..c373, c375, c387, c405, c410) against the current L24 text",
    "course/modules/M/M2/cards.json (lesson L24), M2-c365 at cards.json:2564",
    f"{S}/cards_slice.txt: all 18 read. c365 matches the current Remark 4.4 (the signed-sign claim is about the exact value and the computed error; the card says 'Lab 1 Part B at h = 10^-8' without asserting a printed sign). c367-c370 numbers appear in L24 text; c370 hypotheses (delta assumed, M2 and M3 approximately e) match the lab hypothesis.")
row("CARD-DUP", "2.7 cards: no duplicate card in L22-L24 and none across the unit", "course/modules/M/M2/cards.json",
    f"{S}/cards_dupscan.out: no duplicate ids; no duplicate backs; fronts unique except a normalization false positive (c342/c343).")
row("G-cards-slice-unchanged", "2.7 cards: the 57 slice cards are byte-identical to the round-8 pin (2d755599)", "course/modules/M/M2/cards.json",
    "Run by me: json records with lesson in {L22,L23,L24} at HEAD 1e272e5a equal those at 2d755599 (python comparison, 57 == 57, identical). The file changed only at c086 (L07) and added c411 (L10), both outside this slice.")
row("G-delta-hunks", "delta check: every hunk changed since the round-8 pin (2d755599..1e272e5a) inside the slice read",
    "course/modules/M/M2/L22.html:231; L23.html:269; L24.html:129, :243, :261",
    "git diff 2d755599 1e272e5a for L22/L23/L24 read in full: L22 :231 (x-hat error sentence, re-verified, N-L22-xhat-error); L23 :269 (preview sentence, FI1 link verified in curriculum/03-markets.yaml:19-38 and curriculum/01-foundations.yaml:148); L24 :129 (Remark 4.4), :243 (interpretation), :261 (misconception 1), each re-verified numerically. Non-slice hunks (cards c086, c411; project.html; grader) out of scope.")
row("S-L22-L24-structure", "2.9 structure: section order, quiz of 8 items per lesson, misconceptions, problem tiers",
    "course/modules/M/M2/L22.html, L23.html, L24.html",
    "Each page: sections 1-7 (L22), 1-9 (L23), 1-10 (L24); quiz of 8 items each (counted in the HTML); 3 misconceptions each; problem tiers mechanics/proof/empirical/research with M1-M3, P1-P3, E1-E3, R1-R3 each; key-results table present; lesson-nav links to L21/L23/L24/project.")
row("S-banned-phrases", "2.9 banned phrases (BUILDER_RULES 1.3-1.4): TODO, TBD, lorem, ellipsis, for brevity, etc.",
    "course/modules/M/M2/L22.html, L23.html, L24.html",
    "tools/check_pages.py --unit M2 --page L22/L23/L24: PASS (banned strings are a check in check_pages); grep of the three pages for TODO, TBD, lorem, 'for brevity', 'etc.' returned none in learner prose.")
row("S-process-words", "2.9 no process words in learner text (round, builder, verifier, architect, fixed, request tags)",
    "course/modules/M/M2/L22.html, L23.html, L24.html",
    "grep -i for builder, verifier, architect, fixed/fixes, previous round, request, 'round <n>': no hits in the three pages. 'fixed' occurs only as the math term 'held fixed' in cards.json.")
row("S-scope-words", "2.9 scope words (only, all, always, every, any, same, exactly, never, none)",
    "course/modules/M/M2/L22.html, L23.html, L24.html",
    "Every scope word in learner prose was located by grep and each claim checked: 'Lab 1 Part B prints only the magnitude' (code prints abs), 'the lab uses decade steps only' (SMOOTH_EXPONENTS 1..15), 'tests no other objectives/specification' (one bond, two functions), 'every x in [0,1] is a maximizer at a=0' (Example 2.3), 'has no minimum at any step' (exact central error monotone). No unbacked scope claim found.")
row("DAG-prerequisites", "2.9 DAG: L22-L24 use only concepts of M2 lessons up to their own, M1 and P0.1, plus prose terms",
    "course/modules/M/M2/L22.html:37, L23.html:37, L24.html:37",
    "tools/check_dag.py --unit M2: PASS (gates_pages_dag_labs.out). Linked concepts exist: derivative (L04), partial (L16), gradient (L17), Hessian (L19), implicit-function (L21), Taylor (L08), finite-difference (L13), automatic-differentiation (L14), present value and discount factor and geometric series (M1 L05, L06; course/modules/M/M1/L05.html:def-present-value, def-discount-factor; L06.html def-geometric-series).")
row("DAG-no-later-definitions", "2.9 DAG: no concept defined twice; no later-module dfn or link (Fubini, continuity, Lagrange multipliers)",
    "course/modules/M/M2/L22.html, L23.html, L24.html",
    "check_dag PASS; grep for Fubini, Lagrange multiplier, continuity dfn in the three pages: no concept link or dfn to a later module. The 'Lagrange form of Taylor's theorem' is prose (not a concept link) and is attributed to L08.")
row("H-hours", "2.9 hours: data-hours=10 on each of L22, L23, L24; hub split arithmetic", "course/modules/M/M2/L22.html:2, L23.html:2, L24.html:2; index.html:29, :142",
    "data-hours=\"10\" on each page; hub data-hours-lessons=240 = 24 x 10 and project 60; curriculum/01-foundations.yaml M2 hours 300 = 240 + 60. Arithmetic consistent.")
row("REF-cross-lesson", "2.1 attributions: cross-lesson references in L22, L23, L24 resolve to the stated results",
    "course/modules/M/M2/L22.html:88, :369, :473; L23.html:488 (R1 of L23 at :373-383); L24.html:468",
    "L21 Theorem 1.3 = implicit-function theorem with Assumption 1.2 (IVT) and Assumption 2.1 of L06 (course/modules/M/M2/L21.html:51, :68-69); L21 Theorem 2.1 gives g' = -F_x/F_y (L21.html:87-97); L06 Theorem 2.3 = mean value theorem (L06.html:87-88); L06 Assumption 2.1 = extreme value theorem (L06.html:72-73); L08 Assumption 1.1 = EVT named as L06 Assumption 2.1 (L08.html:61-62); L06 Corollary 3.1(ii) (L06.html:102-103); M1 L06 title 'Geometric Series and Proof by Induction'; M1 L05 'Present value and the discount factor'; FI1 'Bond Math & Curve Construction' (curriculum/03-markets.yaml:19-20) covers duration and convexity (:25, :37-38).")
row("REG-registry-flags", "2.1 registry: no key cited with a locator on L22-L24; nothing to flag",
    "course/modules/M/M2/L22.html:473, L23.html:488, L24.html:468",
    "The only keys named are spivak2008calculus and hubbard2015vector, both present in references/references.json (checked by python); both pages state that no locator was confirmed and attribute no statement to them. curriculum/01-foundations.yaml:146-147 names the same two sources.")

frag = {
    "unit": "M2",
    "slice": "d2",
    "round": 9,
    "verifier": "Claude Haiku 5.5, independent verifier for M2-d2, round 9 (did not build M2; no context shared with the builders).",
    "pin": "1e272e5a641f18412703b37778a44db6f7391a69",
    "base": "2d755599d8d74df292e3e43025f0458c4053802e (round-8 pin). Delta 2d755599..1e272e5a touches L22.html:231, L23.html:269, L24.html:129, :243, :261 in the slice, plus cards c086 and c411 (outside the slice), project.html and grader/test_project.py (outside the slice). Every slice hunk was read and re-verified; the slice cards are unchanged. No PASS row is carried forward; every row was re-derived this round.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD9-M2-d2",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyD9-M2-d2/ledgers/M2/scripts/M2-d2-r9",
    "verified_at": "2026-11-04T23:00:00+00:00",
    "verdict": "PASS",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Lab-only slice (L22-L24, twins and pages). No project grader is in the slice, so run_graders, mutate_graders and alternative correct implementations are not applicable; mutants is empty. Not run: run_graders/mutate_graders for M2 (no grader in the slice); verify_refs --unit M2 live (network); repository gates outside the slice (check_pages --all, build_site --check, render_curriculum, fetch_data --check, run_graders --all); the other M2 slices; check_projects was not run this round. Observation, not a defect: the L23 lab hypothesis and misconception 2 describe the output at 'yield 0.05', which the code reaches as the float 0.04+0.01; the float equals 0.05 exactly as a float (0.04+0.01 == 0.05 is True) and the printed price is 100000 either way (E3 explains the 2.78e-18 offset).",
    "summary": "",
}
n = len(R)
frag["summary"] = f"slice d2 round 9: rows={n}, pass={sum(r['status']=='PASS' for r in R)}, fail=0, unverifiable=0. Mutants 0 (lab-only slice). Round-8 non-PASS row N-L22-xhat-error is now PASS (L22.html:231 re-verified against twin output and unrounded recomputation)."
json.dump(frag, open("ledgers/M2/M2-d2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", n)
