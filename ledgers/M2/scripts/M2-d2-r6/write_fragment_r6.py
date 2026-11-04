"""Writes the round-6 fragment ledgers/M2/M2-d2.json from the rows the verifier recorded (this round's evidence)."""
import json
import sys

S = "ledgers/M2/scripts/M2-d2-r6"
P = "PASS"
F = "FAIL"
rows = []


def row(id_, check, location, status, evidence, fix=""):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)


# ---- gates (run this round on pin 142ecfc2) ----
row("G-check-pages", "tools/check_pages.py --unit M2 and --page L22, L23, L24", "course/modules/M/M2/L22.html, L23.html, L24.html", P,
    f"{S}/check_pages_M2.out: 'check_pages M2: PASS'; check_pages_L22.out, _L23.out, _L24.out: 'check_pages M2 Lnn: PASS' (rc 0).")
row("G-check-dag", "tools/check_dag.py --unit M2 and --all", "curriculum DAG; M2 pages' Uses rows", P,
    f"{S}/check_dag_M2.out 'check_dag M2: PASS'; {S}/check_dag_all.out: 21 PASS lines, 0 FAIL lines (grep -c FAIL = 0), rc 0.")
row("G-check-projects", "tools/check_projects.py --unit M2", "M2 hub and project (no project page in this slice)", P,
    f"{S}/check_projects_M2.out 'check_projects M2: PASS' (rc 0).")
row("G-run-labs", "tools/run_labs.py --unit M2 and --unit M2 --page L22/L23/L24", "tests/labs/M2/lab-M2-L22-1.py, L23-1, L24-1", P,
    f"{S}/run_labs_M2.out 'run_labs M2: PASS (27/27)'; run_labs_L22.out, _L23.out, _L24.out each 'PASS (1/1)'; rc 0.")
row("G-twins-isolated", "twin run alone under python -I -W error", "tests/labs/M2/lab-M2-L22-1.py, L23-1, L24-1", P,
    f"Command: .venv/bin/python -I -W error tests/labs/M2/lab-M2-Lnn-1.py, rc 0 for all three; stdout saved as {S}/twin_L22.out, twin_L23.out, twin_L24.out (no warning text in them).")
row("G-expected-blocks", "page expected block equals twin stdout", "L22.html:222-230; L23.html:215-225; L24.html:218-242", P,
    f"{S}/compare_twins_r6.py -> compare_twins_r6.out: 'page expected == twin stdout (modulo final newline): True' for L22, L23, L24.")
row("G-page-code-equals-twin", "page code block equals twin file", "L22.html:100-221; L23.html:91-214; L24.html:137-217", P,
    f"{S}/compare_twins_r6.out: 'page code == twin (modulo final newline): True' for L22, L23, L24.")
row("G-page-smoke", "tools/page_smoke.py --unit M2 --pages Lnn, one page per run", "L22.html, L23.html, L24.html", P,
    f"{S}/page_smoke_L22.out, _L23.out, _L24.out each end 'page_smoke modules/M/M2/Lnn.html: PASS' and 'page_smoke M2: PASS'; {S}/page_smoke_rc.out rc 0 for each.")
row("G-ruff", "ruff check and ruff format --check on the three twins", "tests/labs/M2/lab-M2-L22-1.py, L23-1, L24-1", P,
    f"{S}/ruff_check.out 'All checks passed!' rc 0; {S}/ruff_format.out '3 files already formatted' rc 0.")
row("G-mypy", "mypy --no-incremental on the three twins", "tests/labs/M2/lab-M2-L22-1.py, L23-1, L24-1", P,
    f"{S}/mypy_twins.out 'Success: no issues found in 3 source files' rc 0.")
row("G-pytest-labs", "pytest tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py -k 'M2 or page or run_labs'", "tests/test_labs.py, tests/test_page_checks.py, tests/test_run_labs.py", P,
    f"Command output saved as {S}/pytest_targeted_r6.out: all progress lines are dots, rc 0 (341 tests, same selection as round 5).")
row("G-pytest-checks", "same targeted pytest run as G-pytest-labs", "tests/test_page_checks.py, tests/test_run_labs.py", P,
    f"{S}/pytest_targeted_r6.out, rc 0.")
row("G-verify-refs", "tools/verify_refs.py --offline", "references/references.json (spivak2008calculus, hubbard2015vector)", P,
    f"{S}/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' rc 0. The live (network) run was not made. references/ is unchanged between pins 440ed3c8 and 142ecfc2 (git diff --stat empty for references/), so the round-5 live result still stands for these keys.")
row("G-cards-scan", "duplicate scan of course/modules/M/M2/cards.json", "course/modules/M/M2/cards.json (393 cards; 56 with lesson L22-L24)", P,
    f"{S}/slice_checks_r6.out '== cards': total 393, dup ids 0, dup fronts 0, dup backs 0; slice cards: 56.")

# ---- structure and prose ----
row("S-hours", "data-hours and hub arithmetic", "L22.html:2, L23.html:2, L24.html:2 (data-hours=10)", P,
    "Attributes read in the head of each page; tools/check_pages.py PASS (6-12 h rule and hub split 240+60) per G-check-pages.")
row("S-structure", "template order, minimum counts, quiz items, problem tiers", "L22.html:53-482; L23.html:53-501; L24.html:53-481", P,
    "Read in full this round. Each page: why-it-matters, numbered core sections, lab, canon-breaks, three misconceptions, problem set (three problems in each of Mechanics, Proof, Empirical, Research, each with a solution in details.solution), key-results table, quiz of eight items (L22 408-467, L23 419-482, L24 399-462), references. check_pages PASS.")
row("S-banned", "banned strings in visible text", "L22, L23, L24 visible text", P,
    f"{S}/slice_checks_r6.out '== banned and process-word hits': no hit for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, ellipsis, roughly-as-filler, historically, typically, in practice (script lines 'HARD').")
row("S-process-words", "process words in learner text", "L22, L23, L24 visible text", P,
    f"{S}/slice_checks_r6.out: no hit for builder, verifier, round N, fixed in, corrected, revision, erratum, previous draft, prerequisite calculus.")
row("S-simulated", "SIMULATED label where a simulated bond or function is used", "L22.html:99; L23.html:90 and twin line 3; L24.html:136 and twin line 3", P,
    "Lab hypothesis paragraphs begin with SIMULATED (L22 line 99 'Both objectives are SIMULATED'; L23 line 90 'The bond is SIMULATED'; L24 line 136 'SIMULATED: both functions'); twin docstrings repeat it (tests/labs/M2/lab-M2-L22-1.py:1-3 region, L23 line 3, L24 line 3).")
row("S-external", "no external requests, CDN, remote font or tracker", "L22.html, L23.html, L24.html", P,
    f"{S}/slice_checks_r6.out '== raw external references': no src/href with http(s), 0 'http' strings in each page.")

# ---- DAG and concepts ----
row("DAG-links", "concept links and Uses rows", "L22.html:37 and 374-376 (R2); L23.html:37 and 379 (R1); L24.html:37 and 373 (R3)", P,
    "Every link points to an earlier lesson or M1 concept (L04, L08, L13, L14, L16, L17, L19, L21, M1 L05 and L06 via concepts.html). Targets exist: def-derivative (L04), def-partial-derivative (L16), def-gradient (L17), def-hessian (L19), def-implicit-function-theorem (L21), def-taylor-theorem (L08), def-finite-difference-derivative (L13), def-automatic-differentiation (L14, grep of id=). check_dag PASS.")
row("DAG-defined-once", "each dfn defined once and only where assigned", "L22.html:59; no dfn in L23 or L24", P,
    f"{S}/slice_checks_r6.out '== dfn elements': L22 ['def-envelope-theorem'], L23 [], L24 []. Matches plan section 3 (L23 and L24 own no concept).")
row("DAG-later-names", "later-module concepts by name or link", "L22.html (continuity, matrix in R2); L23.html (duration, convexity: lab title only, meta attribute); L24.html R2 (Lipschitz, defined inline)", P,
    f"{S}/slice_checks_r6.out '== later-module concept names': only 'e-value' matches, which is the phrase 'the value e' (false match, not a concept). No later-module concept name appears in visible text. duration and convexity appear only as a preview in the lab docstring and meta description (architect Q8), with no dfn and no link. Lipschitz is defined in its own sentence at L24.html:364 and not linked.")
row("NOT-notation", "every symbol against notation/notation.json", "L22.html, L23.html, L24.html math", P,
    f"{S}/slice_checks_r6.out and scan_prose_r6.out: the only registered macro used is \\R (L22 Prop 2.1, R2); no \\mathbb, \\Phi, \\gamma, \\mathbb{{Q}} or R_f / R^\\ast in the three pages; plain R (remainder, L23) is not a registered symbol. notation/notation.json lists T, Phi, gamma_3, gamma_4, R^ast, R^{{e ast}}, R_f, Q only.")

# ---- references ----
row("REF-keys", "registry keys cited", "L22.html:473; L23.html:488; L24.html:468", P,
    "spivak2008calculus and hubbard2015vector are in references/references.json, status verified, used_by M2, source_strings as the curriculum (read this round). Paragraphs cite keys only, no locator, no bibliographic data typed.")
row("REF-internal", "internal citations of results to earlier lessons", "L22.html Remark 1.4 and reference paragraph; L23.html Theorem 3.1 proof and references; L24.html Propositions 3.1-3.2 and references", P,
    "L21.html:68-70 (Theorem 1.3, IFT, under Assumption 1.2 and L06 Assumption 2.1, unique g); L21.html:75-80 (Theorem 1.3 proof: existence by IVT via Assumption 1.2, differentiability by the mean value theorem); L06.html Assumption 2.1 (EVT, unproved), Theorem 2.3 (MVT), Corollary 3.1 (ii) (strict increase from f' > 0); L08.html:61-62 (Assumption 1.1 = EVT, not proved here), Theorem 2.1 (Lagrange form, n >= 0, f^(n+1) on the open interval). All cited results exist with those hypotheses.")
row("GRADE-theorems", "grade of each theorem, proposition and lemma", "L22.html:63, 73, 239; L23.html:67, 79, 232, 242, 251; L24.html:60, 74, 84, 106, 116", P,
    "Re-graded from BLUEPRINT section 3 this round. Each statement is a deduction on the page from stated hypotheses (Lemma 1.2, Theorem 1.3, Proposition 2.1; Propositions 2.1, 2.2, Theorem 3.1, Propositions 3.2, 3.3; Theorem 2.1, Propositions 3.1, 3.2, 4.2, 4.3). T is correct for each. Assumed results are labelled Assumption and carry no grade.")

# ---- mathematics ----
row("MATH-L22-lemma-thm", "Lemma 1.2 and Theorem 1.3 proofs", "L22.html:62-84", P,
    "Read in full. Lemma 1.2 proof checked for both signs of the derivative (quotient argument with t>0 and t<0). Theorem 1.3: (H1)-(H3) used; f_x(x-hat,a)=0 from Lemma 1.2, chain rule V' = f_x x-hat' + f_a re-derived.")
row("MATH-L22-remark14", "Remark 1.4 (where H3 comes from)", "L22.html:86-89 (l.88 carries H2)", P,
    "Subject lines 86-89 are byte-identical to round 5 (git diff hunks of 440ed3c8..142ecfc2 do not touch them). Re-read: G(a,x)=f_x(x,a), partial in x is f_xx; L21 Theorem 1.3 gives unique g on I with values in J; (H2) gives f_x(x-hat(a),a)=0 by Lemma 1.2; uniqueness of zero in K gives x-hat = x-tilde. Round-5 PASS confirmed.")
row("MATH-L22-example15", "Example 1.5 (logarithmic objective)", "L22.html:92-94", P,
    "Re-derived: f_x = a/(1+x) - 1 zero at x = a-1; f_xx = -a/(1+x)^2 < 0 so f_x strictly decreasing and x = a-1 is the global maximizer on (-1, inf) (H2); V = a ln a - (a-1) (recheck_numbers_r6.out: V(1.5)=0.1082); V' = ln a + a(1/a) - 1 = ln a under Assumption 1.1 (product rule); f_a = ln(1+x-hat) = ln a.")
row("MATH-L22-prop21-ex22-ex23", "Proposition 2.1, Examples 2.2 and 2.3", "L22.html:238-257", P,
    "Prop 2.1 chain-rule step re-derived: F_a = g_y c_a + g_a at x-hat. Ex 2.2: F_x = a-2x, x-hat = a/2, F_xx = -2, V = a^2/4, g_y c_a = a/2. Ex 2.3: V(a) = max(a,0); V'(0+) = 1 and V'(0-) = 0 from the one-sided difference quotients (the parenthetical added this round is the definition of those one-sided derivatives, correct).")
row("MATH-L22-exercises", "Problems M1-M3, P1-P3, E1-E3, R1-R3 and their solutions", "L22.html:290-385 and 406-466", P,
    "Every solution re-derived. M1 V = a^2/2, V' = a; M2 x-hat = a+3/2, V = 3a+9/4, V' = 3 = f_a; M3 with x+2y=a: c_a = 1/2, F = x(a-x)/2, x-hat = a/2, y* = a/4, V = a^2/8, V' = a/4 (recheck_numbers_r6.out). P2 V = max(a,0). E1 and E3 consistent with the printed values (see N-L22). R1 and R3 correct under Remark 1.4 and Example 2.3.")
row("MATH-L23-prop21-22", "Proposition 2.1 and 2.2 with proofs", "L23.html:67-86", P,
    "P' and P'' re-derived term by term from c_t(1+y)^(-t) (the sign claims follow). Prop 2.2: v = 1/(1+r); r = 0 gives F; r != 0 uses 1 - v = rv and sum v^t = (1 - v^N)/r (M1 L06 geometric series, def-geometric-series), so the price is F.")
row("MATH-L23-thm31-prop32-33", "Theorem 3.1, Propositions 3.2 and 3.3, Remark 3.4", "L23.html:231-264", P,
    "Lagrange remainder of order two (L08 Theorem 2.1, n = 2) gives R = (1/6) P'''(theta) Delta^3; P''' = -sum t(t+1)(t+2) c_t (1+y)^(-t-3) re-derived; Prop 3.2 sign of -Delta; Prop 3.3 uses (1/2) P''(theta) Delta^2 >= 0 (Lagrange order one). Hypotheses listed in each statement (EVT assumed).")
row("MATH-L23-R1-solution", "R1 solution (new this round): dy/dP-bar = 1/P'(y), sign negative", "L23.html:377-380 (prompt 377, solution 379)", P,
    "G(P-bar, y) = P(y) - P-bar; G_{P-bar} = -1; G_y = P'(y); -G_{P-bar}/G_y = 1/P'(y) (L21 Theorem 2.1 slope formula, Assumption 1.2 and L06 Assumption 2.1 as stated). Every cash flow positive gives P'(y) < 0 (Prop 2.1), so dy/dP-bar < 0. Correct; the IFT link at L23.html:379 points to L21.html#def-implicit-function-theorem.")
row("MATH-L23-canon-bullet1-tangent", "canon-breaks bullet 1 (new hypothesis): tangent never overstates the price", "L23.html:270", P,
    "Prop 3.3 (P - P1 >= 0 for positive cash flows, EVT assumed) gives that the tangent line lies below the price, so a linear approximation never overstates the price for y0 + Delta > -1. Matches the new wording.")
row("MATH-L24-thm21", "Theorem 2.1 (quotients of |x| at 0)", "L24.html:59-67", P,
    "Re-derived for h > 0 and h < 0: forward (|h|-0)/h = 1; backward (0-|-h|)/h = -1; central 0 (average of the two). One-sided limits differ, so no derivative under the two-sided definition of L04 (L04.html:57). Lab twin prints +1, -1, 0 at k = 1..6 (twin_L24.out).")
row("MATH-L24-prop31-32", "Propositions 3.1 and 3.2 with proofs", "L24.html:73-94", P,
    "Lagrange order one: D+ - f' = (1/2) h f''(xi), so |.| <= (1/2) M2 h. Lagrange order two at x+h and x-h: D0 - f' = (1/12) h^2 (f'''(xi1) + f'''(xi2)), so |.| <= (1/6) M3 h^2. Re-derived by hand; the L08 Theorem 2.1 instances match (xi strictly between the points).")
row("MATH-L24-prop42-43", "Propositions 4.2 and 4.3: minimizers and minimum values", "L24.html:106-123", P,
    "g(h) = Ah + B/h with A = M2/2, B = 2 delta: h* = sqrt(B/A) = 2 sqrt(delta/M2), g(h*) = 2 sqrt(AB) = 2 sqrt(M2 delta) (recheck: 2 sqrt(0.3*2)... = 2*sqrt(M2 delta) verified in recheck_numbers_r6.out, R1 line: 2 delta/h* = sqrt(M2 delta)). Prop 4.3: g(h) = (1/6)M3 h^2 + delta/h, g' = (M3/3) h - delta/h^2 = 0 at h^3 = 3 delta/M3, g convex on (0, inf). Both are minima over h > 0. Correct.")
row("HYP-L24-prop42-43", "hypotheses of Propositions 4.2 and 4.3 (round-5 FAIL, step quantifier)", "L24.html:106-107, 116-117; cards M2-c363, M2-c364", P,
    "Cured: the statements now define H as the set of steps h > 0 at which the Proposition 3.1 (resp. 3.2) hypotheses hold, the bound holds for every h in H, the minimizer is taken over all h > 0, and 'if h* in H the bound at h* is this minimum'. The step quantifier is fixed in both the page and the cards (c363, c364 read this round).")
row("MATH-L24-remark44-assumption", "Remark 4.4 (a bound is not the error): the claimed necessity", "L24.html:129 (Remark 4.4); round-5 subject, now re-read", F,
    f"Sentence at L24.html:129: 'so the true error at h* is at most the bound only if h* is in H, that is, only if |f''| <= M2 on [x, x+h*]'. This is a false necessity claim. Counterexample, {S}/remark44_counterexample_r6.py -> remark44_counterexample_r6.out: f(x)=x^2 at x=0, f~ = f (Definition 4.1 holds for any delta), M2 = 1.5, delta = 1. h* = 1.632993, D+ = 1.632993, true error 1.632993, bound g(h*) = 2.449490, so the error is at most the bound; yet |f''| = 2 > M2, so H is empty and h* is not in H. The proposition guarantees the bound at h* only when h* is in H; it does not say the error exceeds the bound otherwise.",
    "At L24.html:129 replace the sentence with: 'so the bound is guaranteed at h* only if h* is in H, that is, only if f is twice differentiable on an open interval containing [x, x+h*] and |f''| <= M2 on [x, x+h*]; the true error at h* can be at most the bound without that.' Make the same change in card M2-c365 (cards.json, line 2567): 'it is guaranteed at h* only if h* is in H ... and the true error can be at most the bound without that.'")
row("MATH-L24-canon-bullet3", "canon-breaks bullet 3, round-off 2 delta/h and P3", "L24.html:252, 319-325", P,
    "Numerator error at most 2 delta, quotient error at most 2 delta/h re-derived. P3 identity (sqrt(1+x)-1)(sqrt(1+x)+1) = x verified; denominator positive for x > -1.")
row("MATH-L24-misconception1", "misconception 1 (new wording: 'where its hypothesis holds')", "L24.html:261", P,
    f"Bound (1/2) M2 h + 2 delta/h increases as h falls below h*: derivative (1/2) M2 - 2 delta/h^2 < 0 for h < h*. Lab Part B values 6.603e-09 at 1e-8 and 2.154e-07 at 1e-9 (twin_L24.out lines k=8, k=9). Correct.")
row("ATTR-L22-assumption-1.1", "attribution of Assumption 1.1 (round-5 FAIL: 'prerequisite calculus')", "L22.html:94; cards M2-c404 (line ~2716)", P,
    "Cured: the text now reads 'This page assumes it and does not prove it.' No prerequisite unit is named, and no attribution is made. The fact (d/da ln a = 1/a) is a named numbered Assumption, so it needs no grade.")
row("ATTR-L24-assumption-4.1", "attribution of Assumption 4.1 (round-5 FAIL: 'prerequisite calculus')", "L24.html:132, 136; cards M2-c405 (line ~2722)", P,
    "Cured: 'This page assumes it and does not prove it' at L24.html:132 and in the lab hypothesis at line 136; card M2-c405 matches. No prerequisite unit is named.")

# ---- numbers in prose and labs ----
row("N-L22", "numbers in L22 lab interpretation and text", "L22.html:223-231 (interpretation 231); 279; 344; 358", P,
    f"{S}/recheck_numbers_r6.out: central differences 0.4054651074, 0.6931471801, 1.0986122885, 1.3862943610 round to the printed 0.40546511, 0.69314718, 1.09861229, 1.38629436 at 8 decimals; x-hat errors 1.37e-8, 7.1e-9, -7.2e-9, -2.2e-8 ('off by about 1e-8'); f_xx(1.5, 0.5) = -0.6667 and 0.5 |f_xx| 1e-16 = 3.3e-17; f_a - ln a at a = 1.5 is 9.1e-9 (last digit differs, as printed); Part B errors 1.9e-13, 1.0e-12, 5.4e-12 (twin_L22.out). Recomputed from unrounded values.")
row("N-L23", "numbers in L23 lab interpretation, text and E3", "L23.html:51, 226, 289, 368", P,
    f"{S}/recheck_numbers_r6.out: P(y0) = 108110.895779, integer 108111, P'(y0) = -851466.7395, P''(y0) = 8376648.5119, -P'/P = 7.875864, P''/P = 77.482001, ratios 3.9279 7.8807 and 3.9634 7.9396, e1 = 403.7716 (+0.01), e2 = -15.06081 (+0.01); unrounded errors -15.0608 (+0.01) and +16.0101 (-0.01), signs match -Delta. E3 offset: {S}/recheck_float_offsets_r6.out: stored float 0.04+0.01 minus 1/20 = 2.7756e-18 (2.78e-18), P'(0.05) = -772173, effect -2.14e-12 cents (about -2.1e-12). Correct to the printed digits.")
row("N-L24", "numbers in L24 lab interpretation, Remark text and E2/E3", "L24.html:136, 243, 341, 348, 359, 261, 252", P,
    f"{S}/recheck_numbers_r6.out: 2 sqrt(delta/e) = 1.807e-8 (about 1.8e-8); (3 delta/e)^(1/3) = 6.257e-6 (about 6.3e-6); ulp(e) = 4.44e-16, half ulp = 2.22e-16 = assumed delta; 1/2 e h at h = 1e-5 is 1.359e-5 (matches 1.359e-5 to four digits); 2 delta/h at 1e-15 = 0.444 (printed 0.390 consistent). {S}/recheck_float_offsets_r6.out: unrounded central errors 5.858691310e-11 (h=1e-5) and 5.858735719e-11 (h=1e-7), difference 4.440892e-16 = ulp(e). Decade table, factor 100 per decade (4.533e-3 -> 4.530e-5 -> 4.530e-7 -> 4.531e-9), factor 77 (4.531e-9/5.859e-11), 2.154e-7 at 1e-9, 3.263e-5 at 1e-11, 3.903e-1 at 1e-15 all match twin_L24.out.")
row("N-L22-E1-E3", "numbers and claims in the new L22 E1 text and solution", "L22.html:342, 344, 358", P,
    "E1 asks why the location error is about 1e-8 and why the value is more accurate; the answer's order-t^2 argument is an explanation the lab does not test, and the page says so (L22.html:342). Value error near 1e-16 (t about 1e-8, squared) is a calculation, not a printed value. E3 numbers consistent with the printed columns (0.40546511 vs 0.40546512).")
row("N-L22-L23-L24-quiz", "quiz answers and explanations", "L22.html:417-466; L23.html:419-482; L24.html:399-462", P,
    f"{S}/recheck_numbers_r6.out: L22 Q2 a^2/2 with a^2 = 5 gives 2.5; Q3 V'(1) = 1/2; Q7 V'(1) = 1/4 (M3). L23 Q3 1000 (Problem M1 and Prop 2.2), Q6 P'(0) = -200, Q8 explanation P'(0.04) = -1777.07 with c1 = -1, c2 = 1000 (recomputed -1777.068). L24 Q3 central quotient of x^2 is 2 for every h, Q7 h* = 1 for delta = 0.5 and M2 = 2. All options and explanations consistent with the pages.")

# ---- labs ----
row("LAB-L22", "lab L22: hypothesis, code, output, interpretation", "L22.html:97-232; tests/labs/M2/lab-M2-L22-1.py", P,
    "G-page-code-equals-twin and G-expected-blocks PASS; twin output matches the printed block; hypothesis (Part A on [0,10], step 1e-4, Part B = Example 2.2 with four and three parameter values) matches the code (PARAMETERS_A has 4 values, PARAMETERS_B has 3, STEP = 1e-4); naive partial printed as 0 (frozen_product). Predicted values match the output.")
row("LAB-L22-hypothesis-line99", "new text of the L22 lab hypothesis (line 99): explicit central difference", "L22.html:99", P,
    "The new formula (V(a+h)-V(a-h))/(2h) with h = 1e-4 matches central_difference(value_a, a, STEP) in the twin (line 198). Correct.")
row("LAB-L23", "lab L23: hypothesis, code, output, interpretation", "L23.html:88-227; tests/labs/M2/lab-M2-L23-1.py:1-17 and 88-122", P,
    "G-page-code-equals-twin and G-expected-blocks PASS. Predictions: price at 0.05 is 100000 (printed 'exact price 100000 cents'); P' < 0 and P'' > 0 (printed -851466.74 and 8376648.51); error ratios near 4 and 8 (printed 3.9279..3.9634 and 7.8807..7.9396). Preview numbers printed and not defined.")
row("LAB-L23-hypothesis-line90", "new text of the L23 lab hypothesis: closed forms checked against central differences", "L23.html:90", P,
    "The twin computes central_difference(lambda y: float(price(y)), y0, 1e-5) and central_difference(price_first_derivative, y0, 1e-4) (lines 96-97) and prints both (twin_L23.out lines 3-4). Matches the sentence.")
row("LAB-L24", "lab L24: hypothesis, code, output, interpretation", "L24.html:134-244; tests/labs/M2/lab-M2-L24-1.py:1-13", P,
    "G-page-code-equals-twin and G-expected-blocks PASS; Part A is |x| at 0, six steps (KINK_EXPONENTS 1..6); Part B is exp at 1 for k = 1..15 (SMOOTH_EXPONENTS range 1..15), decade minimum chosen by strict < (first minimum kept). Output and interpretation consistent (N-L24).")
row("LAB-L24-hypothesis-line136", "new text of the L24 lab hypothesis (assumed, not proved; delta and M2, M3 assumed)", "L24.html:136", P,
    "Says the values of delta, M2, M3 are assumed here, not measured: the twin measures none of them (it prints only decade errors, lines 65-78 of the twin). Consistent.")

# ---- cards ----
row("CARD-L22", "cards of L22 (c323-c337, c404)", "course/modules/M/M2/cards.json (L22 cards)", P,
    f"{S}/slice_checks_r6.out lists the 15 L22 cards; each read against L22.html: c326 (H3 locally, under L21 Assumption 1.2 and L06 Assumption 2.1), c327 (Assumption 1.1 in the card), c328 and c329 numbers at L22.html:223-230, c330 and c332 (Example 2.2 and 2.3), c334 (uniqueness not assumed; interior via (H2)), c336 (location error), c404 (updated wording; round-5 FAIL cured). No card repeats another.")
row("CARD-L23", "cards of L23 (c338-c357, c382-c386, c407)", "course/modules/M/M2/cards.json (L23 cards)", P,
    f"{S}/slice_checks_r6.out lists 24 L23 cards; read against L23.html. Numbers: 108110.895779, 108111, -851466.739529, 8376648.511919, 4.037716e+02, 3.9279/3.9634, 7.8807/7.9396, -15 and 16 cents, 100000 at 0.05, 117060 at -0.01 all match the printed output. Hypotheses in c348-c350 match Theorem 3.1 and Props 3.2-3.3 (EVT named).")
row("CARD-L24", "cards of L24 (c358-c373, c375, c387, c405)", "course/modules/M/M2/cards.json:2567 (back of M2-c365)", F,
    "Card M2-c365 (cards.json line 2567) repeats the Remark 4.4 claim: 'it holds at h* only if h* is in H, that is, only if |f''| <= M_2 on [x, x + h*]'. That is the same false necessity claim (counterexample in MATH-L24-remark44-assumption, remark44_counterexample_r6.out). The other 16 L24 cards match their pages (c363, c364 hypotheses now carry the H set; c370 numbers 1.8e-8, 6.3e-6 verified; c371 and c372 and c373 correct).",
    "Replace the back of M2-c365 with: 'No. It is an upper bound. It is guaranteed at h* only if h* is in H, that is, only if f is twice differentiable on an open interval containing [x, x + h*] and |f''| <= M_2 on [x, x + h*] (Proposition 4.2). The true error can be at most the bound without that, and the truncation and round-off errors can have opposite signs. Lab 1 does not measure delta or M_2.' (Same fix as MATH-L24-remark44-assumption.)")
row("CARD-L24-c363-c364", "cards M2-c363 and M2-c364 (round-5 FAIL, step quantifier)", "course/modules/M/M2/cards.json:2553 and 2560", P,
    "Read this round: each back now states the H set and 'If h* is in H, the bound at h* is this minimum', matching the page statements at L24.html:107 and 117. Hypotheses and grade [T] are correct.")
row("CARD-scan-dup", "duplicate scan of all cards (393)", "course/modules/M/M2/cards.json", P,
    f"{S}/slice_checks_r6.out '== cards': total 393, dup ids 0, dup fronts 0, dup backs 0. Ids need not be sequential (architect ruling 2).")
row("CARDS-dup", "duplicate content across all cards", "course/modules/M/M2/cards.json", P,
    "Same scan: no duplicate front and no duplicate back among the 393 cards. The two cards added this round (M2-c408 for L08 and M2-c409 for L16) are not in this slice and were checked only against their source lessons: L08.html:61-62 (Assumption 1.1 = EVT, not proved) and L16.html:68 (Assumption 1, derivative of exp, Example 1.3, Lab 1, Problems M2, E1, E3), both consistent with the cards.")
row("L24-prop-3.1-hypothesis", "Proposition 3.1 hypotheses", "L24.html:73-81", P,
    "Statement lists EVT (Assumption 2.1 of L06), twice differentiable on an open interval containing [x, x+h], f'' bounded by M2 on [x, x+h]. Proof uses Lagrange order one (L08). No quantifier gap.")
row("L24-prop-3.2-hypothesis", "Proposition 3.2 hypotheses", "L24.html:83-94", P,
    "Three times differentiable on an open interval containing [x-h, x+h]; f''' bounded by M3; EVT named. Proof uses Lagrange order two at x+h and x-h.")
row("L24-simulated-label", "SIMULATED label of the L24 lab", "L24.html:136; tests/labs/M2/lab-M2-L24-1.py:3", P,
    "Hypothesis begins 'SIMULATED: both functions are test functions chosen for this lab, not market data'; twin docstring line 3 says the same.")
row("L23-P3-order", "order of results cited in L23 P3 and misconception", "L23.html:339-345; Proposition 3.3 at L23.html:251-254", P,
    "P3 cites Proposition 2.1 and Taylor's theorem (L08) and asks for the sign that is Proposition 3.3, stated earlier in the same lesson, so no later result is used before its statement.")
row("L24-cards", "cards c360, c361 hypotheses and c367-c375 numbers", "cards M2-c360, M2-c361, M2-c367, M2-c368, M2-c370", P,
    "c360 and c361 carry the Assumption 2.1 hypothesis and the same hypotheses as Propositions 3.1 and 3.2. c367 1.406e-1 to 1.359e-5 and c368 3.263e-5 at 1e-11 and 3.903e-1 at 1e-15 match twin_L24.out.")
row("FWD-L23-lab-prediction", "L22 and L23 forward pointers and the L23 lab prediction", "L23.html:51, 90; L22.html:51", P,
    "L23.html:90 predicts the printed price at 0.05 is 100000 cents; twin_L23.out prints 'exact price 100000 cents' at +0.01 shift. L22.html:51 cites Definition 1.1 (earlier in the same lesson). L23.html:51 cites Theorem 3.1, Proposition 3.2 and Assumption 2.1 of L06; the first two are stated later in the same lesson (a preview, not a definition), and the assumption is from an earlier lesson.")
row("CURRIC-FI1-title", "FI1 title used on L23 (round-5 FAIL, cured)", "course/modules/M/M2/L23.html:90; curriculum/03-markets.yaml:19-20", P,
    "curriculum/03-markets.yaml line 20 gives FI1 the title 'Bond Math & Curve Construction'; L23.html:90 uses the same title ('&amp;' renders as '&'). FI1 introduces duration (line 37) and convexity (line 38), which L23 names only as a preview.")

out = {
    "unit": "M2",
    "slice": "d2",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for M2-d2, round 6 (did not build M2). Full read of L22, L23, L24 and the three twins on pin 142ecfc2; delta from round 5 (440ed3c8) read hunk by hunk (ledgers/M2/scripts/M2-d2-r6/delta_r5_r6_slice.diff); every round-5 non-PASS row re-verified from scratch; round-5 PASS rows re-derived where their subject was in the delta, and re-checked against the same text otherwise.",
    "pin": "142ecfc2bd27061de18bd67e83df81e69f5c249d",
    "base": "440ed3c8 (round-5 pin). Delta 440ed3c8..142ecfc2 touches this slice in L22.html (lines 94, 99, 256, 342, 344), L23.html (51, 90, 268, 270, 341, 377, 379, 452, 466), L24.html (107, 112, 117, 122, 129, 132, 136, 261, 388-389) and cards.json (2553, 2560, 2567, 2716, 2722; appended M2-c408 and M2-c409 after the end of the file, not in this slice). Twins, references and the hub are unchanged.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD6-M2-d2 (detached at 142ecfc2; .venv symlinked; vendor present)",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyD6-M2-d2/ledgers/M2/scripts/M2-d2-r6",
    "verified_at": "2026-11-04T02:47:05+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 6 on 142ecfc2. Two non-PASS rows: MATH-L24-remark44-assumption (L24.html:129, a false necessity claim about the bound at h*; counterexample f=x^2, x=0, M2=1.5, delta=1 with h* not in H and error below bound) and CARD-L24 (card M2-c365 repeats it). Round-5 FAIL rows HYP-L24-prop42-43, ATTR-L22-assumption-1.1, ATTR-L24-assumption-4.1, CARD-L22 and CURRIC-FI1-title are cured and re-verified PASS. "
        "Observations, not findings: (a) the L22 lab hypothesis (L22.html:99) cites Example 2.2 and the L23 lab hypothesis (L23.html:90) cites Theorem 3.1 before those are stated later; these are pointers to results, the terms are linked or defined at first use (the Taylor remainder is linked to L08 at L23.html:37), so no undefined term is used. "
        "(b) The M3 problem of L22 (L22.html:305-308) does not restate the open intervals of Proposition 2.1; its solution takes J = I = (0, inf) with a > 0 implicitly. Not a defect in the proof. "
        "(c) Cards M2-c408 (L08) and M2-c409 (L16) are outside this slice; they were checked against their source lessons only. "
        "Not run: verify_refs live (network); the registry is unchanged between the pins, so the round-5 live result stands. run_graders and mutate_graders: no grader in this lab-only slice (architect ruling 9: mutation testing applies to project graders only), so mutants = 0. Repository-wide gates (check_pages --all, build_site --check, render_curriculum) are outside the slice. page_smoke was run once per page (L22, L23, L24, each alone), not in one invocation."
    ),
    "summary": "slice d2 round 6: 69 rows, 67 PASS, 2 FAIL, 0 UNVERIFIABLE. Mutants 0 (lab-only slice, no grader). Fails: MATH-L24-remark44-assumption and CARD-L24 (the same false necessity sentence, page and card).",
}
path = sys.argv[1]
json.dump(out, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(path, "a", encoding="utf-8").write("\n")
print("rows", len(rows), "pass", sum(r["status"] == P for r in rows), "fail", sum(r["status"] == F for r in rows))
