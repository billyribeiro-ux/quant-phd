import json, subprocess, datetime
ROOT = "/Users/billyribeiro/.fanout/wt/verifyD5-M2-d2"
S = "ledgers/M2/scripts/M2-d2-r5"
rows = []
def row(id_, check, location, status, evidence, fix=""):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

P = "PASS"; F = "FAIL"
# ---- gates
row("G-check-pages", "tools/check_pages.py --unit M2 and --unit M2 --page L22/L23/L24", "course/modules/M/M2/L22.html, L23.html, L24.html", P,
    f"{S}/check_pages_M2.out 'check_pages M2: PASS' rc 0; {S}/check_pages_L22.out, _L23.out, _L24.out each 'check_pages M2 Lnn: PASS' rc 0.")
row("G-check-dag", "tools/check_dag.py --unit M2 and --all", "curriculum DAG; M2 pages' Uses rows and concept links", P,
    f"{S}/check_dag_M2.out 'check_dag M2: PASS' rc 0; {S}/check_dag_all.out: 22 lines, 0 FAIL lines, rc 0.")
row("G-check-projects", "tools/check_projects.py --unit M2", "M2 hub and project (hub-level; no project page in this slice)", P,
    f"{S}/check_projects_M2.out 'check_projects M2: PASS' rc 0.")
row("G-run-labs", "tools/run_labs.py --unit M2 (and --page per lesson)", "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", P,
    f"{S}/run_labs_M2.out 'run_labs M2: PASS (27/27)' rc 0; {S}/run_labs_L22.out, _L23.out, _L24.out 'PASS (1/1)' rc 0.")
row("G-twins-isolated", "each twin run alone: python -I -W error tests/labs/M2/lab-M2-Lnn-1.py from the repo", "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", P,
    f"Run in checkout: rc 0 for all three; stderr empty ({S}/twin_L22.stderr, twin_L23.stderr, twin_L24.stderr 0 bytes); stdout saved as {S}/twin_L2x.stdout.")
row("G-expected-blocks", "expected block equals twin stdout", "L22.html:222-230; L23.html:215-225; L24.html:218-242", P,
    f"{S}/compare_twins.py -> {S}/compare_twins.out: 'expected==stdout ... modulo final newline: True' for L22, L23, L24 (strict equality fails only on the trailing newline, the embedding convention).")
row("G-page-code-equals-twin", "page code equals twin", "L22.html:100-221; L23.html:91-214; L24.html:137-217", P,
    f"{S}/compare_twins.out: 'code==twin ... modulo final newline: True' for L22 (121 lines), L23 (123), L24 (80).")
row("G-page-smoke", "tools/page_smoke.py --unit M2 --pages L22 L23 L24 (Chromium, both themes, 360 px, labs in Pyodide)", "L22.html, L23.html, L24.html", P,
    f"{S}/page_smoke_L22-L24.out: each page 'PASS' with runtime boot and lab steps; 'page_smoke M2: PASS' rc 0.")
row("G-ruff", "ruff check and ruff format --check on the three twins", "tests/labs/M2/lab-M2-L22-1.py, L23, L24", P,
    f"{S}/ruff_check.out 'All checks passed!' rc 0; {S}/ruff_format.out '3 files already formatted' rc 0.")
row("G-mypy", "mypy --no-incremental on the three twins", "tests/labs/M2/lab-M2-L22-1.py, L23, L24", P,
    f"{S}/mypy_twins.out 'Success: no issues found in 3 source files' rc 0.")
row("G-pytest-labs", "pytest tests/test_labs.py -k M2 (targeted, as part of a combined run)", "tests/test_labs.py (M2 cases for the slice twins)", P,
    f"{S}/pytest_targeted.out: 'pytest tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py -k \"M2 or page or run_labs\"' 341 passing tests (count of progress-line results), rc 0.")
row("G-pytest-checks", "pytest tests/test_page_checks.py and tests/test_run_labs.py (same run)", "tests/test_page_checks.py, tests/test_run_labs.py", P,
    f"{S}/pytest_targeted.out rc 0 (same command as G-pytest-labs).")
row("G-verify-refs", "tools/verify_refs.py --offline", "references/references.json (keys spivak2008calculus, hubbard2015vector)", P,
    f"{S}/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' rc 0. The live (network) run was not made by this verifier.")
row("G-cards-scan", "cards.json: the 56 cards of L22-L24 are read in full and counted", "course/modules/M/M2/cards.json", P,
    f"{S}/cards_L22_L24.txt (56 cards: L22 15, L23 24, L24 17); {S}/cards_scan_r5.out: 391 cards, 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs.")
# ---- structure / prose
row("S-hours", "data-hours and the hub split", "L22.html:2, L23.html:2, L24.html:2 (data-hours=10); hub index.html data-hours-lessons=240, data-hours-project=60", P,
    f"Page attributes read; {S}/check_pages_M2.out PASS (the 6-12 h rule and the hub sum).")
row("S-structure", "template sections in BUILDER_RULES 4.2 order; minimum counts", "L22.html:53-482; L23.html:53-501; L24.html:53-481", P,
    f"Read in full. Order: why it matters, numbered core sections, lab, where the canon breaks, misconceptions (3), problem set (3 per tier, each with a solution), key results table, quiz (8 items each), references. {S}/check_pages_L2x.out PASS.")
row("S-banned", "banned phrases in visible prose (BUILDER_RULES 1.3-1.4)", "L22.html, L23.html, L24.html visible text", P,
    f"{S}/scan_prose_r5.out: 0 hits for TODO, TBD, lorem, for brevity, beyond the scope, left as an exercise, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, and others.")
row("S-process-words", "no process words in learner text", "visible text of L22-L24", P,
    f"{S}/scan_prose_r5.out: 0 hits for builder, verifier, round N, fixed in, corrected, revision, erratum, previous draft.")
row("S-simulated", "SIMULATED label on every simulated input", "L22.html:99; L23.html:90 (and twin line 3); L24.html:136 (and twin line 3)", P,
    "Hypothesis paragraphs begin with SIMULATED in each lesson; the twin docstrings repeat it (tests/labs/M2/lab-M2-L22-1.py:3, lab-M2-L23-1.py:3, lab-M2-L24-1.py:3).")
row("S-external", "no external request, CDN, font or tracker", "L22.html, L23.html, L24.html; the three twins", P,
    f"{S}/scan_prose_r5.out: no src/href to http(s) and 0 'http' strings in the three pages; twins import only __future__, math, fractions and collections.abc.")
# ---- DAG
row("DAG-links", "concept links point to earlier lessons or prerequisites", "L22.html:37 and 374-376 (R2 links); L23.html:37 and 379 (R1 link); L24.html:37 and 373 (R3 link)", P,
    "Uses rows: L22 derivative L04, partial L16, gradient L17, Hessian L19, IFT L21; L23 Taylor L08, derivative L04, IFT L21, present value and discount factor (M1 L05, def-present-value, def-discount-factor), geometric series (M1 L06, def-geometric-series); L24 finite-difference L13, derivative L04, Taylor L08, AD L14. All are earlier or prerequisite; check_dag PASS.")
row("DAG-defined-once", "each dfn defined once; the slice owns only envelope-theorem", "L22.html:59 (def-envelope-theorem); no dfn on L23 or L24", P,
    "grep of <dfn in the three pages: one element, the envelope theorem (L22.html). Matches plan section 3 (L23 and L24 own no concept).")
row("DAG-later-names", "later-module concepts used by name only as prose, never as links or dfn", "L22.html (continuity, matrix); L23.html:7, 51, 90 (duration, convexity, FI1 preview); L24.html R2 (Lipschitz)", P,
    "Continuity and Lipschitz are prose (undeclared in curriculum.json concepts, Q5-Q7); duration and convexity appear only as preview names (Q8, plan section 9, FI1 owns them at curriculum/03-markets.yaml:19-38). No link to any later concept; check_dag PASS.")
# ---- notation
row("NOT-notation", "every symbol against notation/notation.json; macros registered", "L22.html, L23.html, L24.html math", P,
    f"{S}/scan_prose_r5.out: the only registered macro used is \\R (L22 R2). None of T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}} appears. Plain R (L23 remainder) and N (L23 cash-flow count, defined in Section 1) are not registered symbols; M, P, F, G, K, U, c, d, e, h, s are local and defined where used.")
# ---- references
row("REF-keys", "cited keys exist in the registry", "L22.html:471-480; L23.html:486-495; L24.html:466-475 (References sections)", P,
    "spivak2008calculus and hubbard2015vector are in references/references.json (checked in Python, both True); the References paragraphs cite the keys only, with no locator and no bibliographic data typed.")
row("REF-internal", "cross-lesson attributions read in the cited lesson", "L22.html Remark 1.4 and reference paragraph; L23.html Theorem 3.1 proof and references; L24.html Props 3.1-3.2 and references", P,
    "Read: L21.html:68-70 (Theorem 1.3, IFT, under Assumption 1.2 and L06 Assumption 2.1) and L21.html:75-80 (its proof uses IVT and MVT); L06.html:72-73 (Assumption 2.1 is EVT, not proved); L06.html:87-88 (Theorem 2.3 MVT); L06.html:102-103 (Corollary 3.1); L08.html:61 (Assumption 1.1 = EVT) and L08.html:90-93 (Lagrange form); L04.html:57 (derivative is a two-sided limit); L13 def finite-difference; L14 def automatic-differentiation; M1 def-present-value and def-discount-factor in M1/L05, def-geometric-series in M1/L06; curriculum/03-markets.yaml:19-38 (FI1 title and its introduces: duration, convexity).")
# ---- grades and maths
row("GRADE-theorems", "every Theorem, Lemma, Proposition carries grade T and a proof or a cited proof", "L22.html:63, 73, 239; L23.html:67, 79, 232, 242, 251; L24.html:60, 74, 84, 106, 116", P,
    "Re-graded from BLUEPRINT section 3: each statement is a deduction on the page (Lemma 1.2, Theorem 1.3, Proposition 2.1, 2.2, Theorem 3.1, Propositions 3.2 and 3.3; Theorem 2.1, Propositions 3.1, 3.2, 4.2 and 4.3). Examples, remarks and misconceptions are derivations on the page (plan section 12). No under- or over-grading found.")
row("MATH-L22-lemma-thm", "Lemma 1.2 and Theorem 1.3, proofs and hypotheses", "L22.html:63-75 (lines 63-84)", P,
    "Read in full. Lemma 1.2 proof checked (quotient sign for t>0 and t<0). Theorem 1.3 states (H1)-(H3); chain-rule step V'=f_x x^'+f_a with f_x=0 re-derived.")
row("MATH-L22-remark14", "Remark 1.4 (where (H3) comes from): hypotheses suffice for its conclusion", "L22.html:86-89 (Remark 1.4, (H2) at l.88); l.473 reference paragraph; cards M2-c326", P,
    "Round-4 FAIL is cured. The suppositions now include (H2) for a near a0 (l.88), which is what Lemma 1.2 needs for f_x(x-hat(a),a)=0. Theorem 1.3 of L21 (L21.html:68-70) applies to G(a,x)=f_x(x,a): G is C^1 because f is C^2; G(a0,x-hat(a0))=0; the x-partial is f_xx != 0. Its open interval K contains x-hat(a0); continuity of x-hat gives x-hat(a) in K for a near a0; uniqueness of the zero in K is L21's uniqueness; so x-hat=x-tilde and (H3) holds locally. Reference paragraph and card c326 now state the same hypotheses.")
row("MATH-L22-example15", "Example 1.5 (logarithmic objective): critical point, global maximizer, V', f_a", "L22.html:92-95 (Example 1.5)", P,
    "Re-derived: f_x = a/(1+x) - 1 vanishes at x=a-1; f_xx = -a/(1+x)^2 < 0 so f_x is strictly decreasing and x=a-1 is the global maximizer on (-1,inf); V=a ln a-(a-1); V'=ln a by the product rule under Assumption 1.1; f_a(x-hat,a)=ln(1+x-hat)=ln a.")
row("MATH-L22-prop21-ex22-ex23", "Proposition 2.1 and Examples 2.2, 2.3", "L22.html:238-282", P,
    "Prop 2.1: F_a = g_y c_a + g_a at x-hat, chain rule re-derived. Ex 2.2: F_x = a-2x, x-hat=a/2, V=a^2/4, g_y c_a + g_a = a/2 (g_a=0). Ex 2.3: V(a)=max(a,0), one-sided derivatives 1 and 0 at a=0; formula f_a(1,a)=1 and f_a(0,0)=0 match.")
row("MATH-L22-exercises", "problem set M1-M3, P1-P3, E1-E3, R1-R3 and their solutions; quiz answers", "L22.html:290-385 and 406-466", P,
    "Every solution re-derived. M1 V=a^2/2, V'=a=f_a; M2 x-hat=a+3/2, V=3a+9/4, V'=3=f_a; M3 y*=a/4, V=a^2/8, V'=a/4; P2 V=max(a,0); E1 order-t^2 argument; E2 and E3 consistent with Lab 1 output; R1 now matches Remark 1.4 (l.369); R2 vector form is labelled as not proved; R3 consistent with Example 2.3. Round-4 R1 defect is cured.")
row("MATH-L23-prop21-22", "Proposition 2.1 (derivatives and signs) and Proposition 2.2 (price at face)", "L23.html:66-86; L23.html:72-86 proofs", P,
    "P' and P'' formulas re-derived term by term; sign claims follow. Prop 2.2: v=1/(1+r); r=0 case gives F; r!=0 uses 1-v=rv and sum v^t=(1-v^N)/r (geometric series, M1 L06), so the price is F.")
row("MATH-L23-thm31-prop32-33", "Theorem 3.1 (remainder), Proposition 3.2 (sign of remainder), Proposition 3.3 (first-order error sign)", "L23.html:231-264", P,
    "Lagrange remainder (1/6)P'''(theta)Delta^3 with L08 Theorem 2.1 (n=2) re-derived; P'''=-sum t(t+1)(t+2)c_t(1+y)^(-t-3) recomputed; Prop 3.3 uses (1/2)P''(theta)Delta^2 >= 0. Hypotheses listed (Assumption 2.1 of L06 for the maximum M).")
row("MATH-L24-thm21", "Theorem 2.1 (quotients of |x| at 0)", "L24.html:60-67", P,
    "Re-derived for h>0 and h<0: forward (|h|)/h = 1; backward -1; central 0; the one-sided limits differ, so no derivative (L04 Definition 1.1 is a two-sided limit, L04.html:57).")
row("MATH-L24-prop31-32", "Proposition 3.1 (forward truncation) and Proposition 3.2 (central truncation)", "L24.html:74-94", P,
    "Lagrange order-1 gives D+ - f' = (1/2) h f''(xi); order-2 expansions at x+h and x-h give D0 - f' = (1/12) h^2 (f'''(xi1)+f'''(xi2)); bounds (1/2) M2 h and (1/6) M3 h^2 follow. Re-derived by hand; no sign error.")
row("MATH-L24-prop42-43", "proof of Proposition 4.2 and 4.3: the bound and its minimizer (algebra)", "L24.html:106-123", P,
    "g(h)=Ah+B/h: g'=A-B/h^2, h*=sqrt(B/A)=2 sqrt(delta/M2), g(h*)=2 sqrt(AB)=2 sqrt(M2 delta) with A=M2/2, B=2 delta. g(h)=Ch^2+B/h with C=M3/6, B=delta: h^3=B/(2C)=3 delta/M3. Re-derived. The statement's hypothesis gap is row HYP-L24-prop42-43.")
row("HYP-L24-prop42-43", "Propositions 4.2 and 4.3: hypotheses for every step at which the bound is used", "L24.html:106-107 (Prop 4.2), L24.html:116-117 (Prop 4.3), key results L24.html:388-389, cards M2-c363, M2-c364", F,
    "The hypotheses are 'those of Proposition 3.1' (f'' bounded by M2 on [x, x+h]) and 'those of Proposition 3.2' (f''' bounded by M3 on [x-h, x+h]), and both are indexed by the step h. The statements then assert that 'the bound is minimized at h*' and 'the bound' applies at h*, but no statement says the hypothesis holds on the interval used at h*. The minimization of g on (0,inf) is correct as a function fact; the hypothesis needed for the bound to hold at h* is not stated.",
    "State the bound 'for every h>0 such that f is twice differentiable on an open interval containing [x,x+h] and |f''| <= M2 on [x,x+h]' (and '|f'''| <= M3 on [x-h,x+h]' for Prop 4.3), say that the minimizer is the minimizer of the bound function over those h, and make the same change in the key-results rows (L24.html:388-389) and in cards M2-c363 and M2-c364.")
row("MATH-L24-remark44-assumption", "Remark 4.4 (a bound is not the error): the guarantee at h*", "L24.html:128-130 (Remark 4.4; sentence at l.129)", F,
    "Remark 4.4 says 'the true error at h* is only guaranteed to be at most the bound'. That guarantee at h* needs |f''| <= M2 on [x,x+h*] (Prop 3.1 at h*), which the page never establishes. Same root cause as HYP-L24-prop42-43.",
    "Replace the sentence at L24.html:129 with: 'Proposition 4.2 gives an upper bound at every step where its hypothesis holds; if |f''| <= M2 on [x, x+h*], the true error at h* is at most the bound.' The Assumption 4.1 attribution is a separate row, ATTR-L24-assumption-4.1.")
row("MATH-L24-canon-bullet3", "canon bullet on cancellation and the rewrite sqrt(1+x)-1 (Problem P3)", "L24.html:247-256 (canon bullets); P3 at L24.html:319-323", P,
    "Numerator error at most 2 delta and quotient error 2 delta/h re-derived; P3 identity (sqrt(1+x)-1)(sqrt(1+x)+1)=x verified; denominator positive for x>-1.")
row("ATTR-L22-assumption-1.1", "attribution of Assumption 1.1 (derivative of ln a) to a source", "L22.html:94 (Assumption 1.1); cards.json M2-c404 (line 2716)", F,
    "L22.html:94 says 'This page takes the fact from the prerequisite calculus'. The prerequisite closure of M2 has no such calculus: M1 is 'Precalculus & Mathematical Reasoning' (curriculum/01-foundations.yaml:87-88) and its eight lesson pages contain no derivative or differentiation (scan_prose_r5.out: 0 hits in M1 L01-L08); P0.1 is 'How to Study This Program' (01-foundations.yaml:6-7). The attribution points to nothing that exists. The sentence in M2 L16 ('This page assumes it and does not prove it') is the honest form. Card M2-c404 repeats the wrong attribution.",
    "Replace L22.html:94 'This page takes the fact from the prerequisite calculus and does not prove it.' with 'This page assumes it and does not prove it.' Replace the back of card M2-c404 with 'For a > 0, the derivative of ln a is 1/a. It is assumed here, not proved; Example 1.5 uses it.'")
row("ATTR-L24-assumption-4.1", "attribution of Assumption 4.1 (derivative of e^x) to a source", "L24.html:132 (Assumption 4.1), L24.html:136 (Lab 1 hypothesis), cards.json M2-c405 (line 2722)", F,
    "L24.html:132 and L24.html:136 say the fact is 'taken from the prerequisite calculus'. As in ATTR-L22-assumption-1.1, no prerequisite unit teaches the derivative of exp (M1 is precalculus with no derivative content; P0.1 is study skills). Card M2-c405 repeats it.",
    "L24.html:132: replace the sentence with 'This page assumes it and does not prove it.' L24.html:136: replace 'taken from the prerequisite calculus and not proved on this page' with 'assumed here and not proved on this page'. Card M2-c405 back: 'For every real x, the derivative of e^x is e^x. It is assumed, not proved; the value e at x0 = 1 relies on it.'")
# ---- numbers
row("N-L22", "numbers in L22 prose vs printed output and derivations", "L22.html:223-231 (interpretation l.231); l.279 (misconception 3); l.344, l.358 (E1, E3)", P,
    f"Printed values checked against {S}/twin_L22.stdout: central differences equal ln a to 8 decimals; x-hat 0.50000001 at a=1.5; Part B errors 1.9e-13, 1.0e-12, 5.4e-12 (largest). Recomputed with exact arithmetic in {S}/recheck_L23_L22.py -> recheck_L23_L22.out: f_xx(1.5, x=0.5) = -0.66667; half times that times (1e-8)^2 = 3.3e-17; sqrt(eps)=1.49e-8.")
row("N-L23", "numbers in L23 prose vs printed output and derivations (E3 calculation now shown)", "L23.html:51, 90, 226, 271, 308, 318, 343, 366, 368 (E3 l.368), 481", P,
    f"Round-4 FAIL at E3 is cured: l.368 now states float 0.04+0.01 minus 0.05 = 2.78e-18 (exact), P'(0.05) = -7.72e5, effect about -2.1e-12 cents. {S}/recheck_L23_L22.out reproduces each: P(0.04)=108110.895779 (rounds 108111); P'=-851466.7395; P''=8376648.5119; -P'/P=7.875864; P''/P=77.482001; errors -15.0608 and +16.0101 (diff -15, +16 cents); ratios 3.9279, 3.9634, 7.8807, 7.9396; offset 2.7756e-18; P'(0.05)=-772173.49 (so -7.72e5); effect -2.1432e-12; two-cash-flow P'(0.04)=-1777.0682 (-1777.07).")
row("N-L24", "numbers in L24 prose vs printed output and derivations", "L24.html:136, 243, 341, 348, 359", P,
    f"{S}/recheck_L24.out reproduces: forward/central errors at k=1..15; central errors 5.858691310e-11 (1e-5) and 5.858735719e-11 (1e-7), difference 4.440892e-16 = ulp(e); 2 sqrt(delta/e)=1.807e-8; (3 delta/e)^(1/3)=6.257e-6; 2 delta/1e-15=0.444 vs printed 0.3903; half e h at 1e-5 = 1.3591e-5; 4.531e-9/5.859e-11 = 77.3; log10(6.3e-6) = -5.20 (closer to 1e-5).")
row("N-L22-L23-L24-quiz", "retrieval quiz answers and explanations", "L22.html:417-457; L23.html:415-463; L24.html:395-441", P,
    "L22: answers 2.5 (a^2=5), 0.5 (V'(1) of Ex 2.2), 0.25 (M3 at a=1); correct options checked. L23: answer 1000 (Problem M1), -200 (zero-coupon at y=0; P'=-200(1+y)^-3), option 'sign of -Delta' correct, R(Delta)=(1/6)P'''(theta)Delta^3. L24: answer 2 (central quotient of x^2), answer 1 (h*=2 sqrt(0.5/2)). Explanations consistent with the propositions.")
# ---- labs
row("LAB-L22", "Lab 1 of L22: hypothesis, code, output, interpretation", "L22.html:97-232; tests/labs/M2/lab-M2-L22-1.py", P,
    "Code equals twin modulo final newline; output equals twin stdout (G-expected-blocks); hypothesis matches the code (Part A Example 1.5 on [0,10], step 1e-4; Part B constrained problem of Example 2.2; prints the naive partial 0). Interpretation statements checked against the printed output (N-L22). Lab does not print V's error and the page says so.")
row("LAB-L23", "Lab 1 of L23: hypothesis, code, output, interpretation", "L23.html:88-227; tests/labs/M2/lab-M2-L23-1.py:1-17 and 88-122", P,
    "Code equals twin; output equals twin stdout; hypothesis predictions (100000 at yield 0.05; P'<0, P''>0; error ratios near 4 and 8) match output; preview numbers printed but not defined, as the page states.")
row("LAB-L24", "Lab 1 of L24: hypothesis, code, output, interpretation", "L24.html:134-244; tests/labs/M2/lab-M2-L24-1.py:1-13", P,
    "Code equals twin; output equals twin stdout; Part A prints +1, -1, 0 at six steps (Theorem 2.1); Part B decade table and minima match the page text; interpretation values re-derived (N-L24).")
# ---- cards
row("CARD-L22", "every L22 card (15): grade and basis, hypotheses carried, numbers appear in the lesson", "course/modules/M/M2/cards.json: M2-c323..c337 and M2-c404 (15 cards)", F,
    f"{S}/cards_L22_L24.txt read in full. c326 (Remark 1.4) now carries (H2) and matches the Remark: round-4 FAIL cured. c328, c329 numbers appear at L22.html:223-231. c336 basis Lab 1 part A correct. c334 (uniqueness not assumed; interiority) is consistent with Theorem 1.3. c404 repeats the wrong attribution 'taken from prerequisite calculus' (see ATTR-L22-assumption-1.1): FAIL on that card only.",
    "Replace the back of card M2-c404 as in ATTR-L22-assumption-1.1 (delete the 'prerequisite calculus' attribution).")
row("CARD-L23", "every L23 card (24): grade, basis, numbers, hypotheses", "course/modules/M/M2/cards.json: M2-c338..c357, c382..c386, c407 (24 cards)", P,
    f"{S}/cards_L22_L24.txt read in full. Numbers 108110.895779, 108111, -851466.739529, 8376648.511919, 4.037716e+02, 3.9279/3.9634, 7.8807/7.9396, -15, 117060, -1.506081e+01, 100000 (yield 0.05) all appear in L23 and match the twin output. Theorem 3.1 and Props 3.2, 3.3 hypotheses carried (Assumption 2.1 of L06). Card c347 and c386 consistent with Section 1 and Section 4.")
row("CARD-L24", "every L24 card (17): grade, basis, hypotheses, numbers", "course/modules/M/M2/cards.json: M2-c358..c373, c375, c387, c405 (17 cards)", F,
    f"{S}/cards_L22_L24.txt read in full. c359-c361 and c363-c364 hypotheses carried (c363 and c364 inherit the HYP-L24-prop42-43 gap: their hypothesis wording must change with the statement). c370 graded C with its basis and the assumed delta and M2, M3 (matches the hypothesis at L24.html:136). c405 repeats the wrong attribution (ATTR-L24-assumption-4.1): FAIL on that card.",
    "Replace the back of card M2-c405 as in ATTR-L24-assumption-4.1; restate the hypotheses of M2-c363 and M2-c364 as in HYP-L24-prop42-43.")
row("CARD-scan-dup", "duplicate scan of all cards.json", "course/modules/M/M2/cards.json (391 cards)", P,
    f"{S}/cards_scan_r5.out: 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs.")
row("CARDS-dup", "duplicate cards by content across lessons", "course/modules/M/M2/cards.json", P,
    f"{S}/cards_scan_r5.out: no duplicate front or back among the 391 cards; ids need not be sequential (architect ruling 2).")
row("L24-prop-3.1-hypothesis", "Proposition 3.1 hypotheses explicit", "L24.html:74-81", P,
    "The statement lists the open interval containing [x,x+h], f twice differentiable, and the bound M2 on [x,x+h]; Assumption 2.1 named. (The step quantifier is a separate row for Propositions 4.2-4.3.)")
row("L24-prop-3.2-hypothesis", "Proposition 3.2 hypotheses explicit", "L24.html:84-94", P,
    "Three times differentiable on an open interval containing [x-h,x+h]; f''' bounded by M3; Assumption 2.1 named.")
row("L24-simulated-label", "SIMULATED label for L24 test functions", "L24.html:136; tests/labs/M2/lab-M2-L24-1.py:3", P,
    "Hypothesis begins 'SIMULATED: both functions are test functions chosen for this lab, not market data'; twin docstring line 3 says the same.")
row("L23-P3-order", "problem P3 of L23 uses only earlier results", "L23.html:339-345 (P3); Proposition 3.3 at L23.html:252", P,
    "P3 cites Taylor's theorem and the sign of P'' from Proposition 2.1 and gives Proposition 3.3; both are earlier in the lesson.")
row("L24-cards", "L24 cards M2-c360 and M2-c361 hypotheses and grades", "cards.json M2-c360, M2-c361", P,
    "Both are T with the Assumption 2.1 hypothesis stated; their hypotheses match Propositions 3.1 and 3.2 on the page (the step-quantifier gap is in HYP-L24-prop42-43, not in these cards).")
row("FWD-L23-lab-prediction", "forward-pointing predictions in the L23 and L22 pages match the output", "L23.html:51 and 90; L22.html:51", P,
    f"L23.html:90 predicts the printed price at yield 0.05 is 100000 cents; {S}/twin_L23.stdout prints 'exact price 100000 cents' at +0.01 shift. L22.html:51 forward pointer to the envelope theorem (Definition 1.1) is consistent.")
row("CURRIC-FI1-title", "unit name quoted from the curriculum", "course/modules/M/M2/L23.html:90 ('Bond Math &amp; Curve Construction')", P,
    "curriculum/03-markets.yaml:19-20 gives FI1 the title 'Bond Math & Curve Construction'; the page now uses the same title (HTML entity &amp; renders as &). Round-4 FAIL cured. FI1 introduces duration and convexity (03-markets.yaml:37-38), consistent with the preview.")

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
counts = {"PASS": sum(r["status"] == "PASS" for r in rows), "FAIL": sum(r["status"] == "FAIL" for r in rows)}
frag = {
    "unit": "M2",
    "slice": "d2",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for M2-d2, round 5 (did not build M2). Full read of L22, L23, L24 and the three twins (every sentence, every card, every problem solution); every row re-derived on pin 440ed3c8; no round-4 PASS row was carried without re-checking.",
    "pin": "440ed3c8",
    "base": "4eb6788 (round-4 pin). Delta 4eb6788..440ed3c touches this slice in L22.html (Remark 1.4 with (H2), Remark reference paragraph, R1 solution, quiz Q8 explanation), L23.html (lab hypothesis FI1 title, P1 solution, E3 solution) and cards.json (in slice: M2-c326 and M2-c358; outside slice: c379, c068, c072, c230 edited and c388, c389, c396 removed). The three twins and L24.html did not change; delta saved as ledgers/M2/scripts/M2-d2-r5/delta_r4_r5_slice.diff.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-M2-d2 (detached at 440ed3c8; .venv symlinked)",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyD5-M2-d2/ledgers/M2/scripts/M2-d2-r5",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if counts["FAIL"] else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 5 on 440ed3c8. Round-4 FAIL rows MATH-L22-remark14, MATH-L22-exercises, N-L23, CARD-L22 (c326 part) and CURRIC-FI1-title are cured and re-verified PASS. "
        "Four new non-PASS findings are raised for the authors: two attributions to 'prerequisite calculus' (no such prerequisite teaches the derivative of ln or exp: M1 is precalculus with no derivative content, P0.1 is study skills), a step-quantifier gap in Propositions 4.2 and 4.3 and the 'guaranteed' sentence of Remark 4.4, and the two cards that repeat the attribution. "
        "No grader and no project mutant applies to this lab-only slice (architect ruling: mutation testing applies to project graders only); mutants = 0. "
        "Not run: verify_refs live (network); run_graders and mutate_graders (no grader in this slice); page_smoke was run once for the three pages together, not one invocation per page; repository-wide gates (check_pages --all, build_site, render_curriculum) are outside this slice. "
        "Minor observations, not findings: the M3 problem of L22 does not restate the open intervals J and I that Proposition 2.1 requires (its solution takes J=I=(0,inf) implicitly); E1 of L22 argues that the value of the maximum is accurate (an order-t^2 argument) although the lab does not print V's error, and the page says so in the interpretation. The printed central errors at 1e-5 and 1e-7 in L24 E3 (5.858691 and 5.858736) differ by 4.5e-16 as displayed; the unrounded difference is 4.44e-16, as the page says."
    ),
    "summary": f"slice d2 round 5: {len(rows)} rows, {counts['PASS']} PASS, {counts['FAIL']} FAIL, 0 UNVERIFIABLE. Mutants 0 (no grader in slice).",
}
path = f"{ROOT}/ledgers/M2/M2-d2.json"
with open(path, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("rows", len(rows), counts, frag["verdict"])
