"""Build ledgers/M2/M2-d2.json (round 2) from the verifier's observed results. Every row cites a script, a command, or a locator."""
import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD2-M2-d2")
S = "ledgers/M2/scripts/M2-d2-r2"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates (command rows, run on the pin)
row("G-check-pages", "tools/check_pages.py --unit M2", "tools/check_pages.py", "PASS",
    f"{S}/check_pages.out: 'check_pages M2: PASS', exit 0 (run this round on c737272).")
row("G-check-dag", "tools/check_dag.py --unit M2 and --all", "tools/check_dag.py", "PASS",
    f"{S}/check_dag.out: 'check_dag M2: PASS' exit 0; {S}/check_dag_all.out: all units PASS, exit 0.")
row("G-check-projects", "tools/check_projects.py --unit M2", "tools/check_projects.py", "PASS",
    f"{S}/check_projects.out: 'check_projects M2: PASS', exit 0 (hub-level; no project page in this slice).")
row("G-run-labs", "tools/run_labs.py --unit M2 --page L22 / L23 / L24", "tools/run_labs.py", "PASS",
    f"{S}/run_labs_L22.out, run_labs_L23.out, run_labs_L24.out: each 'run_labs M2: PASS (1/1)', exit 0. Page code is byte-identical to its twin (run_labs checks this).")
row("G-twins-isolated", "twins under python -I -W error, CPython 3.14.8", "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", "PASS",
    f"`.venv/bin/python -I -W error lab-M2-Lxx-1.py` in a scratch directory: exit 0 for all three, stderr 0 bytes ({S}/twin_L22/L23/L24.stderr); stdout kept in {S}/twin_L2x.stdout.")
row("G-expected-blocks", "expected block equals twin stdout (pages L22, L23, L24)", "course/modules/M/M2/L22.html:222-230, L23.html:215-225, L24.html:218-242", "PASS",
    f"{S}/expected_compare.py output ({S}/expected_compare.out): 'L22 expected==stdout: True lines 9 9', 'L23 ... True lines 11 11', 'L24 ... True lines 25 25'.")
row("G-page-smoke", "tools/page_smoke.py --unit M2 --pages L22 L23 L24", "tools/page_smoke.py", "PASS",
    f"{S}/page_smoke_L22_L24.out: each page PASS (light and dark, 360 px), lab runs in the Pyodide runtime in 0.0 s, 'page_smoke M2: PASS', exit 0.")
row("G-ruff", "ruff check and ruff format --check on the three twins", "tests/labs/M2/lab-M2-L22-1.py, L23-1.py, L24-1.py", "PASS",
    f"{S}/ruff.out: 'All checks passed!', '3 files already formatted', exit 0.")
row("G-mypy", "mypy --no-incremental on the three twins", "tests/labs/M2/lab-M2-L22-1.py, L23-1.py, L24-1.py", "PASS",
    f"{S}/mypy.out: 'Success: no issues found in 3 source files', exit 0.")
row("G-pytest-labs", "pytest tests/test_labs.py for the three slice labs", "tests/test_labs.py", "PASS",
    f"{S}/pytest_labs_slice.out: three parametrized cases (lab-M2-L22-1, L23-1, L24-1), exit 0.")
row("G-pytest-checks", "pytest tests/test_page_checks.py tests/test_run_labs.py", "tests/test_page_checks.py, tests/test_run_labs.py", "PASS",
    f"{S}/pytest_m2_checks.out: all tests pass, exit 0.")
row("G-verify-refs", "tools/verify_refs.py --offline (all) and --unit M2 (live)", "tools/verify_refs.py; references/references.json", "PASS",
    f"{S}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'; {S}/verify_refs_live_M2.out: 'live re-verification of M2: 2 of 560 entries, 0 problems' (keys spivak2008calculus, hubbard2015vector).")
row("G-cards-scan", "full scan of cards.json (393 cards)", "course/modules/M/M2/cards.json", "PASS",
    f"{S}/cards_scan.py -> {S}/cards_scan.out: 393 cards, 393 distinct ids, no duplicate ids; no card number cited in a card is missing from its lesson; every lesson key has a page; every grade C/D card has a basis. Near-duplicate pairs printed by the scan all differ in substance (other slices' template cards differ only by lesson number).")

# ---- structure, banned phrases, notation, DAG, references
row("S-hours", "hours arithmetic and lesson header", "L22.html:2, 34; L23.html:2, 34; L24.html:2, 34", "PASS",
    "data-hours=\"10\" on each page; eyebrows '10 study hours'; 24 lessons x 10 h = 240 h matches the hub split checked by check_pages (G-check-pages).")
row("S-structure", "section order and navigation (BUILDER_RULES 4)", "L22.html:53-482; L23.html:53-501; L24.html:53-482", "PASS",
    "Sections in order (L22 §1-§7, L23 §1-§9, L24 §1-§10), key-results table, quiz with data-cards=\"cards.json\" (L22.html:404, L23.html:415, L24.html:395), references, Previous/Next links to L21/L23, L22/L24, L23/project.")
row("S-banned", "banned phrases and scope words (BUILDER_RULES 1.3-1.4)", "L22.html, L23.html, L24.html visible text", "PASS",
    f"{S}/extract_text.py -> {S}/extract_text.out and text_L2x.txt: zero hits for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'well known', 'obviously', 'clearly', 'it can be shown'. Every scope word hit (every, any, only, exactly, always, all, most, small, roughly) was read in context and is backed by a proof, a computed printout, or a quoted hypothesis.")
row("S-process-words", "no process words in learner text", f"{S}/text_L22.txt, text_L23.txt, text_L24.txt", "PASS",
    "grep for builder, verif, ledger, twin, fragment, architect, planner, REQUEST, agent, orchestrat, campaign, batch in the visible text: no hits.")
row("S-simulated", "SIMULATED labels where synthetic data is used", "L22.html:99, L22.html:102 (twin); L23.html:20, 62, 90, 93; L24.html:136, 139", "PASS",
    "Each lab's hypothesis and twin docstring carries 'SIMULATED'. The labs use generated bond specifications and test functions (curriculum has no calculus dataset; plan §6.1).")
row("S-external", "no external requests or runtime dependencies", "course/modules/M/M2/L22.html, L23.html, L24.html", "PASS",
    "page_smoke (G-page-smoke) reports zero requests to any host other than the local server; the twins import only fractions, math, collections.abc, __future__ (lab sources).")
row("DAG-links", "every concept link resolves to a single definition, prerequisite first", "L22.html:37; L23.html:37; L24.html:37", "PASS",
    "L22 links: derivative (L04.html#def-derivative), partial-derivative (L16.html#def-partial-derivative), implicit-function-theorem (L21.html#def-implicit-function-theorem). L23 links: taylor-theorem (L08.html#def-taylor-theorem), derivative (L04), present-value and discount-factor (M1 L05 def-present-value, def-discount-factor, course/modules/M/M1/L05.html), geometric-series (M1 L06 def-geometric-series, M1/L06.html). L24 links: finite-difference-derivative (L13.html#def-finite-difference-derivative), derivative (L04), taylor-theorem (L08). All targets exist and precede the links in the sequence; check_dag PASS.")
row("DAG-defined-once", "no concept defined twice; dfn only where the plan assigns it", "L22.html:59; L23.html (no dfn); L24.html (no dfn)", "PASS",
    "The only <dfn> in the three pages is def-envelope-theorem (L22.html:59, envelope-theorem, M2's own). 'Introduces' lines for L23 and L24 say none in the index, matching the absence of <dfn>. Concept ids def-* are unique across L01-L24 (grep of course/modules/M/M2/L*.html).")
row("DAG-later-names", "concepts from later modules used by name or link", f"L23.html:7, 51, 90, 91-107 (text_L23.txt); curriculum/curriculum.json topological_order", "PASS",
    "'Duration' and 'convexity' appear only as a named preview in the description, the lab hypothesis and the lab docstring, with no dfn and no link (Architect Q8). The concepts are FI1's (curriculum/03-markets.yaml:37-38 under the FI1 block; topological_order index FI1=18 > M2=5, verified by script), so 'a later unit' is true. 'bond', 'cash flow', 'option', 'convex', 'matrix', 'Lagrange remainder' appear as prose (Architect Q5-Q7) with no link. 'Lagrange' in L23/L24 means the remainder form from L08, not the multiplier.")
row("NOT-notation", "symbols against notation/notation.json", "L22.html, L23.html, L24.html", "PASS",
    "Only the registered macro \\R is used (no \\mathbb in the three pages, grep count 0). Registered symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}, \\E, \\Prob) are not used in the slice. Local letters (N, M, F, c_t, P, V, g, G, R(Delta), D^+_h, D^-_h, D^0_h, delta, h*) are defined on the page that uses them (e.g. L23.html:55, 238; L24.html:55, 102).")
row("REF-keys", "registry keys cited, locator and attribution", "L22.html:473; L23.html:488; L24.html:468", "PASS",
    "Each page names spivak2008calculus and hubbard2015vector by key, states that no locator is confirmed, and attributes no statement to either. Live verify_refs for M2 keys: 0 problems (G-verify-refs).")
row("REF-internal", "cross-lesson theorem and assumption citations", "L22.html:88, 473; L23.html:233, 238, 379, 488; L24.html:75, 85, 107, 117, 468", "PASS",
    "Verified against the cited pages: L21 Theorem 1.3 (IFT, unique zero in J, C^1 g, L21.html:68-75) and L21 Assumption 1.2 (IVT, L21.html:63-64); L21 Theorem 2.1 slope formula (L21.html:86-87); L06 Assumption 2.1 (EVT, L06.html:83), L06 Theorem 2.3 (MVT, L06.html:87-88); L08 Theorem 2.1 Lagrange form for general n (L08.html:90-91) and L08 Assumption 1.1 = L06 Assumption 2.1 (L08.html:61, 82); L08 orders used: n=1 (L24 Prop 3.1), n=2 (L24 Prop 3.2, L23 Thm 3.1), n=1 (L23 Prop 3.3); M1 L05/L06 definitions exist as cited.")
row("GRADE-theorems", "grades of T claims (BLUEPRINT 3)", "L22.html:63, 73, 239, 396-398; L23.html:67, 79, 232, 242, 251, 405-409; L24.html:60, 74, 84, 107, 116, 385-389", "PASS",
    "Every displayed theorem, lemma, proposition is graded T with a proof on the page or a cited Assumption (L22 Thm 1.3 and Lemma 1.2 proved; L22 Prop 2.1 proved under its stated (H1)-(H3) hypothesis for F; L23 Props 2.1, 2.2, 3.2, 3.3 proved, Thm 3.1 proved from L08; L24 Thm 2.1 and Props 3.1, 3.2, 4.2, 4.3 proved). No C-level or lab result is graded T in the prose; lab-derived statements carry no grade span in the pages.")

# ---- mathematics
row("MATH-L22-lemma-thm", "Lemma 1.2 and Theorem 1.3, every step", "L22.html:63-83", "PASS",
    "Lemma 1.2: the one-sided quotient argument (L22.html:69) is correct. Theorem 1.3 (L22.html:74-83): f_x(x_hat,a)=0 from Lemma 1.2 for every a; chain rule V'=f_x x_hat'+f_a; first term vanishes. Re-derived by hand; no gap.")
row("MATH-L22-remark14", "Remark 1.4 (where H3 comes from)", "L22.html:88", "PASS",
    "Re-derived: G(a,x)=f_x(x,a), dG/dx=f_xx != 0 at (a0, x_hat(a0)); L21 Thm 1.3 gives a C^1 g on an interval I with values in J and a unique zero of G(a,.) in J (L21.html:75 'exactly one zero'); x_hat(a) lies in J for a near a0 by continuity and f_x(x_hat(a),a)=0 by Lemma 1.2 (which uses that x_hat(a) maximizes f(.,a), the Section 1 setup (H2)). The remark is ungraded and its conclusion is stated as local, matching Theorem 1.3's (H3). Not a defect.")
row("MATH-L22-example15", "Example 1.5 (log objective) and Assumption 1.1", "L22.html:93-94", "PASS",
    "f_x = a/(1+x)-1 vanishes at x=a-1 (a/(1+a-1)-1=0); f_xx=-a/(1+x)^2<0; x_hat=a-1 in J=(-1,inf) for a>0; V=a ln a-(a-1); V'=ln a+a(1/a)-1=ln a = f_a(x_hat,a)=ln(1+x_hat). All re-derived.")
row("MATH-L22-prop21-ex22-ex23", "Proposition 2.1, Examples 2.2 and 2.3", "L22.html:240-251, 256", "PASS",
    "Prop 2.1: chain rule F_a=g_y c_a+g_a, with V'=F_a(x_hat,a) from Thm 1.3 applied to F. Ex 2.2: F=x(a-x), F_x=a-2x, x_hat=a/2, F_xx=-2, V=a^2/4, V'=a/2 = g_y c_a + g_a = (a/2)(1)+0. Ex 2.3: V=max(a,0) on [0,1]; V'(0+)=1, V'(0-)=0; not differentiable at 0; (H2)-(H3) fail for the closed domain as the bullets say. Verified.")
row("MATH-L22-exercises", "problems M1-M3, P1-P3, E1-E3, R1-R3 and quiz answers", "L22.html:290-385, 406-466", "PASS",
    "M1: x_hat=a, V=a^2/2, V'=a=f_a. M2: x_hat=a+3/2, V=3a+9/4, V'=3=f_a. M3: y=(a-x)/2, c_a=1/2, F_x=(a-2x)/2, x_hat=a/2, y*=a/4, V=a^2/8, V'=a/4 (q7 numeric 0.25 at a=1 correct). Quiz numeric answers 2.5, 0.5 re-derived. The E1 solution's 'about 10^-16' is the order-of-magnitude value of 3.3e-17 (see N-L22); PASS with that reading.")
row("MATH-L23-prop21-22", "Proposition 2.1 (derivative formulas and signs) and Proposition 2.2 (price at face)", "L23.html:67-86", "PASS",
    "d/dy(1+y)^-t=-t(1+y)^-t-1, second derivative t(t+1)(1+y)^-t-2: re-derived; positive cash flows give P'<0 and P''>0. Prop 2.2: v=1/(1+r), 1-v=rv for r!=0, sum v^t=(1-v^N)/r, so rF*sum+Fv^N=F; r=0 gives coupons 0 and v=1, price F. Both cases re-derived.")
row("MATH-L23-thm31-prop32-33", "Theorem 3.1, Propositions 3.2 and 3.3, Remark 3.4", "L23.html:231-263", "PASS",
    "Thm 3.1: Lagrange form with n=2 (L08 Thm 2.1, L08.html:90-91) gives R=(1/6)P'''(theta)Delta^3 and |R|<=(1/6)M|Delta|^3 with M the max of |P'''| on the closed interval (compact, inside (-1,inf)). P'''=-sum t(t+1)(t+2)c_t(1+y)^-t-3<0, so sign(R)=sign(-Delta) (Prop 3.2). Prop 3.3: n=1 gives (1/2)P''(theta)Delta^2>=0. Numerical signs confirmed by the printed -15/+16 cents (N-L23).")
row("MATH-L24-thm21", "Theorem 2.1 (|x| quotients)", "L24.html:59-66", "PASS",
    "D+_h|x|(0)=|h|/h=1, D-_h=(0-|-h|)/h=-1, D0_h=(|h|-|-h|)/(2h)=0 for every h>0; one-sided limits differ, so no derivative (the limit over both signs does not exist). Re-derived; also reproduced by the twin's Part A printout (twin_L24.stdout lines 2-7).")
row("MATH-L24-prop31-32", "Propositions 3.1 and 3.2 (truncation)", "L24.html:73-94", "PASS",
    "Prop 3.1 proof: Taylor order one gives f(x+h)=f(x)+hf'(x)+(1/2)h^2 f''(xi), xi in (x,x+h); quotient error (1/2)h f''(xi). Prop 3.2 proof: order two at x+h and x-h; the cubic terms have opposite signs, subtraction gives 2hf'+(1/6)h^3(f'''(xi1)+f'''(xi2)); divide by 2h: (1/12)h^2(...), bounded by (1/6)M3 h^2. Hypotheses (open interval containing the closed interval) are sufficient for the Lagrange form. Verified.")
row("MATH-L24-prop42-43", "Propositions 4.2 and 4.3 (computed quotients and balancing step)", "L24.html:105-123", "PASS",
    "Prop 4.2: computed-minus-exact quotient is at most 2delta/h; total bound (1/2)M2 h+2delta/h; g(h)=Ah+B/h with A=M2/2, B=2delta: minimum at sqrt(B/A)=2 sqrt(delta/M2), value 2 sqrt(AB)=2 sqrt(M2 delta). Prop 4.3: error <= delta/h; g=Ch^2+B/h with C=M3/6, B=delta: h^3=B/(2C)=3delta/M3. Re-derived; the M3 example at delta=2^-52 and M2=e is in N-L24.")
row("MATH-L24-remark44-assumption", "Remark 4.4, Assumption 4.1 and the Section 5 claims", "L24.html:125-132, 248-252", "PASS",
    "Remark 4.4 is stated as an upper-bound caveat, consistent with Prop 4.2. Assumption 4.1 is named and labelled as assumed (not proved). The Section 5 claim that M2 is not computed by the lab is true (twin computes no M2).")

# ---- numbers (prose vs unrounded)
row("N-L22", "numbers in prose vs unrounded values (L22)", "L22.html:231, 279, 344, 358; twin_L22.stdout", "PASS",
    "Printed x_hat 0.50000001 etc. and expected block match twin output (G-expected-blocks). 'about 10^-8' vs sqrt(2.2e-16)=1.49e-8: consistent. '0.666667' = 1.5/2.25; the change 0.5*0.666667*(1e-8)^2 = 3.33e-17 (misconception 3, L22.html:279 '3.3 x 10^-17' correct). E1's 'about 10^-16' (L22.html:344) is 3.3e-17 rounded to the nearest power of ten (log10 = -16.48); accepted as an order-of-magnitude statement with the exact figure given in L22.html:279. Part B's 'largest printed error 5.4e-12' matches the expected block. Part A 'eight printed decimals' matches.")
row("N-L23", "numbers in prose vs unrounded values (L23)", "L23.html:51, 90, 226, 271, 308, 366, 304, 318, 421, 463-481; numbers_L23_L24.out; float_offset_L23.out", "PASS",
    "Re-derived: unrounded price 108110.895779 (rounds to 108111); second-order error at +0.01 = -15.060810 and at -0.01 = +16.010073 (so '15.06 and 16.01 unrounded', 'off by 15 and 16 whole cents' and integer differences -15 and +16 all correct); P'(y0)=-851466.7395, P''(y0)=8376648.5119 (match the printout, so '851466.74' and '8376648.51' are correct); FD differences 1.6e-03 and 1.9 as printed; ratios 3.9279, 3.9634, 7.8807, 7.9396 as printed; float yield 0.05 minus exact 5% = 2.776e-18 ('about 2.8e-18') and P'(0.05)*that = -2.14e-12 ('about 2.1e-12 cents'), integer price 100000 (float_offset_L23.out); quiz q8 explanation P'(0.04)=-1777.068 for c1=-1, c2=1000 ('-1777.07', re-derived with Fraction); preview -P'/P=7.875864, P''/P=77.482001 as printed; M1 solution 47.619+952.381=1000.000 and 50/1.05=47.619, 1050/1.1025=952.381 (re-derived).")
row("N-L24", "numbers in prose vs unrounded values (L24)", "L24.html:136, 231-243, 341, 348, 359, 298, 384-391; numbers_L23_L24.out", "PASS",
    "Re-derived with the twin's functions: central errors at 1e-5 and 1e-7 are 5.8586913e-11 and 5.8587357e-11, difference 4.44e-16 ('about 4.4e-16'; one ulp of e is 4.44e-16); 4.531e-9/5.859e-11=77.3 ('about 77'); central errors fall by a factor of 100.07, 100.0, 100.0 per decade from 1e-1 to 1e-4 (printout); predicted minimizers 2 sqrt(delta/e)=1.807e-8 ('about 1.8e-8') and (3 delta/e)^(1/3)=6.257e-6 ('about 6.3e-6'); half-ulp of e = 2^-52 = 2.22e-16; 2 delta/1e-15 = 0.444 ('0.444'); printed 0.390 <= 0.444 + (1/2)M2 h consistent; (1/2) e h at 1e-5 = 1.359e-5 matches the printed forward error; M3 example 2.1^3=9.261, 12.61, error 0.61 <= (1/2)(12.6)(0.1)=0.63; R1 factor 10 and 10 sqrt(M2 delta) re-derived; forward errors 6.603e-9, 2.154e-7, 3.263e-5, 3.903e-1 match the printout.")
row("N-L22-L23-L24-quiz", "quiz numeric answers and explanations", "L22.html:417-457; L23.html:437-463; L24.html:417-453", "PASS",
    "L22 q2 2.5, q3 0.5, q7 0.25; L23 q3 1000 (Prop 2.2), q6 -200 (P'(0)=-200); L24 q3 2, q7 h*=2 sqrt(0.5/2)=1. All correct and tolerance 0 is exact for these values.")

# ---- labs
row("LAB-L22", "lab L22: hypothesis, twin docstring, code, output, interpretation", "L22.html:97-232; tests/labs/M2/lab-M2-L22-1.py", "PASS",
    "Run and compared (G-run-labs, G-expected-blocks). Hypothesis (L22.html:99) describes the printed quantities (x_hat, central difference of V at 1e-4, f_a, the naive partial, a/2) and the golden-section bracket [0,10]; the twin docstring (lines 100-111) and functions match the code (STEP=1e-4, PARAMETERS_A/B, golden_max, reduced and frozen objectives, main prints). Interpretation (L22.html:231) statements about printed values verified against output. Lab checks two problems (4 and 3 parameter values) and tests no other objective: stated correctly.")
row("LAB-L23", "lab L23: hypothesis, twin docstring, code, output, interpretation", "L23.html:88-227; tests/labs/M2/lab-M2-L23-1.py", "FAIL",
    "Output, expected block, the predicted price 100000 at yield 0.05 and the interpretation numbers are correct (G-run-labs, N-L23). The twin docstring line 96 says 'so no rounding enters before the price is reported' while the same docstring (lines 97-99) and the code (taylor_first, line 163: Fraction(price_first_derivative(y0)); taylor_second, line 168) round the two sensitivities to doubles before the Taylor polynomials are formed. The lab-displayed sentence is therefore false for the Taylor polynomials.",
    fix="In tests/labs/M2/lab-M2-L23-1.py line 96 replace 'The price and its Taylor polynomials are exact rational arithmetic (Fraction) on the float yields, so no rounding enters before the price is reported.' with 'The price is exact rational arithmetic (Fraction) on the float yields, so no rounding enters the price before it is reported; the Taylor polynomials are exact given their two float sensitivities (next lines).' Then run tools/embed_labs.py course/modules/M/M2/L23.html --refresh lab-M2-L23-1 and rerun run_labs --unit M2 --page L23.")
row("LAB-L24", "lab L24: hypothesis, twin docstring, code, output, interpretation", "L24.html:134-244; tests/labs/M2/lab-M2-L24-1.py", "FAIL",
    "Output, expected block and interpretation numbers are correct (G-run-labs, N-L24). The twin docstring (lines 140-143, shown on L24.html:137-149) says 'they show that the quotients converge to different limits (+1 and -1 for the one-sided quotients, 0 for the central quotient) instead of to one derivative'. The lab evaluates the quotients at six step sizes and prints the constant triples (+1, -1, 0); no printout or computation shows a limit. The limits come from the algebra of Theorem 2.1 (L24.html:59-66), not from the lab.",
    fix="In tests/labs/M2/lab-M2-L24-1.py lines 140-143 replace 'they show that the quotients converge to different limits (+1 and -1 for the one-sided quotients, 0 for the central quotient) instead of to one derivative.' with 'they print +1 for the forward quotient, -1 for the backward quotient and 0 for the central quotient at each of the six steps; Theorem 2.1 gives their limits.' Then run tools/embed_labs.py course/modules/M/M2/L24.html --refresh lab-M2-L24-1 and rerun run_labs --unit M2 --page L24.")

# ---- cards
row("CARD-L22", "cards for L22 (15 cards): correctness, grades, basis", "course/modules/M/M2/cards.json: M2-c323..c337, M2-c404", "PASS",
    "All 15 cards read. Each agrees with the current L22 text (Def 1.1, Lemma 1.2, Thm 1.3, Remark 1.4, Ex 1.5, Ex 2.2, Ex 2.3, Prop 2.1, Misconceptions 1-3, Assumption 1.1). Lab cards c328, c329, c336 are graded C with basis Lab 1 and match the output. Hypotheses carried for Prop 2.1 (c331) and Thm 1.3 (c325).")
row("CARD-L23", "cards for L23 (23 cards): correctness, grades, basis, atomicity", "course/modules/M/M2/cards.json: M2-c338..c357, c382..c386", "FAIL",
    "All 23 cards read. Cards c338-c357 and c382-c386 agree with the lesson text and carry the Prop 2.1, 2.2, Thm 3.1, Prop 3.2, Prop 3.3 hypotheses. Two cards are not atomic and carry a lab result inside a T grade: M2-c353 (T) answers with Proposition 2.2 and also 'Lab 1 prints 100000 cents at the yield 0.05'; M2-c354 (T) answers with Proposition 2.1 and also 'Lab 1 prints P'(y0) = -851466.74 cents per unit of yield'. The lab print is a C result (BLUEPRINT 3, cards C with basis).",
    fix="Split each card: keep the T claim (Prop 2.2 for c353; Prop 2.1 for c354) and move the printed number into its own card graded C with basis 'Lab 1 (SIMULATED bond)', or delete the printed number from the T card's back.")
row("CARD-L24", "cards for L24 (17 cards): correctness, grades, basis", "course/modules/M/M2/cards.json: M2-c358..c375, c387, c405", "FAIL",
    "All 17 cards read. Cards c358-c375, c387, c405 agree with the current text and carry hypotheses (c360, c361, c363, c364 list them). M2-c370 is graded C with basis 'Propositions 4.2 and 4.3 with M_2 and M_3 approximately e and delta = 2^-52 (Lab 1 values)'. The page states these inputs are assumed, not measured (L24.html:136 'The values of delta and M_2 are assumed here, not measured'), and the lab prints neither minimizer. The predicted minimizers are arithmetic on the assumed inputs (re-derived: 1.807e-8 and 6.257e-6), not lab results.",
    fix="Change M2-c370 to grade T with the condition stated on the card (under the assumed delta = 2^-52 and M_2 = M_3 = e, Propositions 4.2 and 4.3 give the step ...) and basis 'Propositions 4.2 and 4.3; delta and M_2 are assumed (L24 Lab 1 hypothesis), not measured'. Keep the approximate values.")
row("CARD-scan-dup", "duplicate and near-duplicate cards across the whole file", "course/modules/M/M2/cards.json", "PASS",
    f"{S}/cards_scan.out: no duplicate ids; no substantive duplicate fronts or backs among M2-c323..c405 (the pairs c342/c343, c345/c384, c346/c385, c360/c361, c363/c364 ask distinct questions). Round-1 duplicate M2-c333 is gone (no card with that id).")

# ---- round-1 rows re-verified from scratch (ids kept)
row("L24-prop-3.1-hypothesis", "round-1 row: Prop 3.1 hypothesis (re-verified)", "course/modules/M/M2/L24.html:75, 90", "PASS",
    "Statement now assumes f twice differentiable on an open interval containing [x,x+h] with f'' bounded on [x,x+h]; the proof uses Taylor order one with xi in (x,x+h), which needs exactly these hypotheses (checked against L08 Thm 2.1 hypotheses).")
row("L24-prop-3.2-hypothesis", "round-1 row: Prop 3.2 hypothesis (re-verified)", "course/modules/M/M2/L24.html:85, 90-93", "PASS",
    "Statement now assumes f three times differentiable on an open interval containing [x-h,x+h] with f''' bounded there; the proof's order-two Taylor expansions at x+h and x-h use exactly this (checked).")
row("L24-simulated-label", "round-1 row: SIMULATED label on the L24 lab (re-verified)", "course/modules/M/M2/L24.html:136; tests/labs/M2/lab-M2-L24-1.py:139", "PASS",
    "Hypothesis begins 'SIMULATED: both functions are test functions chosen for this lab'; twin docstring begins 'SIMULATED: the two functions are test functions chosen for this lab'.")
row("L23-P3-order", "round-1 row: order of Taylor remainder in L23 P3 (re-verified)", "course/modules/M/M2/L23.html:343", "PASS",
    "P3 now says 'Lagrange remainder of order one' for P(y0+Delta)-P1(Delta)=(1/2)P''(theta)Delta^2, which is the n=1 case of L08 Thm 2.1 and matches the Proposition 3.3 proof's 'two derivatives' (L23.html:258). Consistent.")
row("L24-cards", "round-1 row: L24 cards M2-c360 and M2-c361 (re-verified)", "course/modules/M/M2/cards.json: M2-c360, M2-c361", "PASS",
    "Both cards now carry the Proposition 3.1 / 3.2 hypotheses (open interval containing the closed interval; f'' or f''' bounded there) and the Assumption 2.1 of L06; they agree with L24.html:73-94.")
row("CARDS-dup", "round-1 row: duplicate cards M2-c333 and M2-c335 (re-verified)", "course/modules/M/M2/cards.json", "PASS",
    "No duplicate ids (393 distinct); M2-c333 is absent; M2-c335 ('When a constraint depends on a, is the derivative of the value the partial of the objective in a?') differs from M2-c330 (Example 2.2 value) and cites Misconception 1.")

# ---- non-fail points recorded for the record
row("FWD-L23-lab-prediction", "forward pointer: lab hypothesis cites Theorem 3.1 and Proposition 3.2 (Section 3)", "course/modules/M/M2/L23.html:90, 51", "PASS",
    "The prediction in the Section 2 lab hypothesis names Theorem 3.1 and Proposition 3.2, stated later. This is a pointer to a later result, not a term used before its definition (the term 'remainder' is covered by the L08 link and 'Taylor's theorem' is defined in L08). Noted, not a fail under BUILDER_RULES 12 as written.")

fragment = {
    "unit": "M2",
    "slice": "d2",
    "round": 2,
    "verifier": "Haiku 5.5 independent verifier, slice d2 (L22, L23, L24 and lab twins), round 2",
    "pin": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "base": "9f5d9865 (previous round's pin, inferred from the round-1 fragment's findings)",
    "checkout": str(ROOT),
    "scratch": str(ROOT / S),
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Full verification, no carry-forward: every page sentence of L22, L23, L24 read, every twin line read, every card read (55 cards), and all gate commands re-run on the pin.",
        "No grader in this slice, so no mutation testing applies (ruling; plan 5.1 covers only the project). mutants is empty.",
        "Round-1 rows L24-prop-3.1-hypothesis, L24-prop-3.2-hypothesis, L24-simulated-label, L23-P3-order, L24-cards and CARDS-dup are re-verified and PASS.",
        "Four rows FAIL: LAB-L23 (twin docstring rounding claim), LAB-L24 (twin docstring convergence claim), CARD-L23 (T cards with lab results), CARD-L24 (M2-c370 basis). Each is a wording or grade fix; no numeric value is wrong.",
        "Other slices' cards c380 and c399-c401 are template questions that differ only by lesson number; outside this slice, not defects here.",
    ],
    "summary": "M2-d2 round 2: gates PASS (check_pages, check_dag, check_projects, run_labs for L22-L24, twins under python -I -W error with empty stderr, expected blocks equal stdout, page_smoke, ruff, mypy, test_labs for the three labs, test_page_checks, test_run_labs, verify_refs offline and live for M2 keys). Every number re-derived PASS. FAIL on four rows: two lab docstrings overstate what the code and printout show, one T card carries lab output, one card's basis credits assumed inputs to the lab.",
}

out = ROOT / "ledgers/M2/M2-d2.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows))
