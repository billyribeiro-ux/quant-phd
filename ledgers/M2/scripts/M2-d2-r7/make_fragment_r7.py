"""Build the M2-d2 round-7 verifier fragment (rows, evidence and verdict) from the verifier's findings.

Every evidence string cites a script or command output under ledgers/M2/scripts/M2-d2-r7/ or a repository locator.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

CHECKOUT = Path("/Users/billyribeiro/.fanout/wt/verifyD7-M2-d2")
S = "ledgers/M2/scripts/M2-d2-r7"
P = "course/modules/M/M2"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---- gates and tools (run by the verifier on pin 9373ef39) ----
row("G-check-pages", "2.9 structure: tools/check_pages.py --unit M2 --page L22/L23/L24", f"{P}/L22.html, L23.html, L24.html", "PASS",
    f"{S}/gates_r7.out: 'check_pages M2 L22: PASS', 'check_pages M2 L23: PASS', 'check_pages M2 L24: PASS'.")
row("G-check-dag", "2.9 DAG: tools/check_dag.py --unit M2", "course/modules/M/M2/L22.html..L24.html", "PASS",
    f"{S}/gates_r7.out: 'check_dag M2: PASS' (unit-wide).")
row("G-run-labs", "2.5 labs: tools/run_labs.py --unit M2 --page L22/L23/L24", "lab-M2-L22-1, lab-M2-L23-1, lab-M2-L24-1", "PASS",
    f"{S}/gates_r7.out: 'run_labs M2: PASS (1/1)' three times, one per page.")
row("G-twin-isolated", "2.5 labs: each twin under python -I -W error, scratch cwd", "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", "PASS",
    f"{S}/twin_vs_page.out: twin exit=0 and stderr='' for all three twins (run with python -I -W error).")
row("G-page-code-equals-twin", "2.5 labs: embedded code block equals the twin", f"{P}/L22.html:100-221, L23.html:91-214, L24.html:137-217", "PASS",
    f"{S}/twin_vs_page.out: 'page code == twin (modulo trailing newline): True' for L22, L23 and L24.")
row("G-expected-equals-live", "2.5 labs: expected block equals live stdout, exact text", f"{P}/L22.html:222-230, L23.html:215-225, L24.html:218-242", "PASS",
    f"{S}/twin_vs_page.out: 'exact stdout == expected block: True' for L22, L23 and L24; live output printed in the same file.")
row("G-page-smoke-L22", "2.9 page_smoke, L22 alone", f"{P}/L22.html", "PASS",
    f"{S}/page_smoke_r7.out: 'page_smoke modules/M/M2/L22.html: PASS' (command: tools/page_smoke.py --unit M2 --pages L22).")
row("G-page-smoke-L23", "2.9 page_smoke, L23 alone", f"{P}/L23.html", "PASS",
    f"{S}/page_smoke_r7.out: 'page_smoke modules/M/M2/L23.html: PASS'.")
row("G-page-smoke-L24", "2.9 page_smoke, L24 alone", f"{P}/L24.html", "PASS",
    f"{S}/page_smoke_r7.out: 'page_smoke modules/M/M2/L24.html: PASS'.")
row("G-ruff-mypy-twins", "tooling: ruff check, ruff format --check, mypy --no-incremental on the three twins", "tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py", "PASS",
    f"{S}/gates_r7.out: 'All checks passed!', '3 files already formatted', 'Success: no issues found in 3 source files'.")
row("G-pytest-labs-M2", "tooling: pytest tests/test_labs.py -k M2", "tests/test_labs.py", "PASS",
    f"{S}/pytest_labs_M2.out: all M2 tests passed, rc=0 (command: .venv/bin/python -m pytest tests/test_labs.py -q -k M2).")
row("G-verify-refs-offline", "2.1 citations: tools/verify_refs.py --offline (whole registry; --unit needs the live run, not run)", "references/references.json", "PASS",
    f"{S}/gates_r7.out: 'offline integrity: 560 entries, 0 problems', exit 0. The registry is unchanged between pins 142ecfc2 and 9373ef39 (git diff lists only the four slice files).")
row("G-links-anchors", "2.9 structure: every internal href and fragment on L22-L24 resolves", f"{P}/L22.html, L23.html, L24.html", "PASS",
    f"{S}/links_and_terms.out: 'broken internal links or anchors in L22-L24: []'.")
row("G-cards-dup-scan", "2.7 cards: full duplicate scan of cards.json (394 cards)", f"{P}/cards.json", "PASS",
    f"{S}/cards_scan.out: no duplicate ids, no duplicate backs; one normalized-front collision (M2-c342 P'(y0) vs M2-c343 P''(y0)) which are different derivatives, not duplicates.")
row("G-notation", "3.2 notation: every macro against notation/notation.json; no registered symbol reused", f"{P}/L22.html, L23.html, L24.html", "PASS",
    f"{S}/links_and_terms.out: L22 uses the registered \\R only; no \\mathbb anywhere in the three pages; L23 and L24 use no registered macro. Bare letters (P, R(Delta), M, H, F, V, D^+_h) are not registered symbols; registered T, Phi, gamma_3, gamma_4, R^*, R^(e*), R_f, Q do not occur in the slice (grep).")

# ---- prose numbers (one row per number group; each re-derived) ----
row("N-L22-xhat-error", "2.2 numbers: x_hat printed 0.50000001 (error about 1e-8), sqrt(eps) comparison, 3.3e-17 objective change",
    f"{P}/L22.html:231 (interpretation), :279 (misconception 3)", "PASS",
    f"{S}/twin_vs_page.out prints x_hat 0.50000001 for a=1.5; {S}/consts.out: sys.float_info.epsilon = 2.220446e-16, sqrt = 1.490e-08, 0.5*0.666667*(1e-8)^2 = 3.33e-17, f_xx = -0.6667 at a=1.5, x=0.5.")
row("N-L22-partB-5.4e-12", "2.2 numbers: Part B central differences agree with a/2 to within 5.4e-12 at a=1,2,3; naive partial prints 0",
    f"{P}/L22.html:231, :329 (c329)", "PASS", f"{S}/twin_vs_page.out Part B lines: errors 1.9e-13, 1.0e-12, 5.4e-12; naive partial 0.00000000.")
row("N-L22-partA-ln", "2.2 numbers: central differences 0.40546511, 0.69314718, 1.09861229, 1.38629436 equal ln a to eight decimals",
    f"{P}/L22.html:231, card M2-c328", "PASS", f"{S}/twin_vs_page.out Part A lines; ln(1.5)=0.405465108..., ln 2, ln 3, ln 4 recomputed by the twin code.")
row("N-L23-price-cents", "2.2 numbers: unrounded price 108110.895779 cents, integer 108111; P'(y0) -851466.739529 and P''(y0) 8376648.511919; differences 1.6e-03 and 1.9",
    f"{P}/L23.html:226, cards M2-c341..c343, c382", "PASS",
    f"{S}/l23_numbers.out: P(0.04)=108110.89577935502, P'(0.04)=-851466.7395285615, P''(0.04)=8376648.51191949; the lab output in twin_vs_page.out prints the same digits.")
row("N-L23-ratios-and-shifts", "2.2 numbers: second-order errors -15.06 (+0.01), -1.911 (+0.005), -0.2407 (+0.0025); first-order errors; ratios 3.9279/7.8807 and 3.9634/7.9396",
    f"{P}/L23.html:51, :226, :281; cards M2-c345, c346, c384, c385", "PASS",
    f"{S}/l23_numbers.out: dy=+0.01 second -1.506081e+01; ratio first 0.01/0.005 = 3.927854, second 7.880704; ratio first 0.005/0.0025 = 3.963438, second 7.939627 (page prints 3.9279, 7.8807, 3.9634, 7.9396 after truncation to four decimals).")
row("N-L23-cents-minus15-plus16", "2.2 numbers: exact minus second-order rounded to whole cents: -15 at +0.01 and +16 at -0.01; unrounded -15.06 and +16.01",
    f"{P}/L23.html:51, :226, :281, card M2-c352", "PASS",
    f"{S}/l23_numbers.out: unrounded second-order error at -0.01 is +16.010073; twin prints 100000 vs 100015 and 117060 vs 117044 (twin_vs_page.out).")
row("N-L23-E3-offset", "2.2 numbers: float 0.04+0.01 differs from 1/20 by 2.78e-18; P'(0.05) = -7.72e5; price moves -2.1e-12 cents",
    f"{P}/L23.html:368 (E3 solution)", "PASS",
    f"{S}/l23_numbers.out: offset float(0.04+0.01)-1/20 = 2.7755575615628915e-18; P'(0.05) = -772173.49 (so -7.72e5); P'*offset = -2.1432e-12.")
row("N-L23-previews", "2.2 numbers: -P'/P = 7.875864 and P''/P = 77.482001 (printed only)", f"{P}/L23.html:90 (hypothesis), :226", "PASS",
    f"{S}/l23_numbers.out: -P'/P = 7.875864253926185, P''/P = 77.48200078755711; twin_vs_page.out prints the same.")
row("N-L23-two-cash-flows", "2.2 numbers: quiz explanation P'(0.04) = -1777.07 for c1=-1, c2=1000", f"{P}/L23.html:481", "PASS",
    f"{S}/l23_numbers.out: two-cash-flow P'(0.04) = -1777.068161.")
row("N-L23-M1-M3", "2.2 numbers: M1 price 50/1.05 + 1050/1.05^2 = 1000.000; M3 zero-coupon P'(0)=-200", f"{P}/L23.html:304, :311, quiz 463", "PASS",
    f"{S}/l23_numbers.out: M1 price = 999.9999999999999 (equals 1000 to display); zero-coupon P'(0) = -200.0.")
row("N-L24-remark44-numbers", "2.2 numbers: exact forward error +1.359e-8 at h=1e-8; computed error -6.603e-9", f"{P}/L24.html:129, :243, card M2-c365", "PASS",
    f"{S}/l24_numbers.out: exact forward quotient minus e at 1e-8 = +1.3591409e-08; float forward quotient minus float e = -6.6027508e-09.")
row("N-L24-E3-unrounded", "2.2 numbers: unrounded central quotient errors 5.858691e-11 at 1e-5 and 5.858736e-11 at 1e-7", f"{P}/L24.html:348", "PASS",
    f"{S}/l24_numbers.out: k=5 signed central error +5.85869131e-11; k=7 +5.85873572e-11.")
row("N-L24-E3-difference", "2.2 numbers (rule 1, unrounded vs displayed digits): the unrounded values differ by 4.4e-16, not 4.5e-16",
    f"{P}/L24.html:348 (E3 solution, sentence 'They differ by \\(4.5 \\times 10^{-16}\\)')", "FAIL",
    f"{S}/l24_numbers.out: 'difference c7 - c5 = 4.440892e-16  ulp(e) = 4.440892098500626e-16'. The unrounded difference is 4.44e-16; 4.5e-16 is the difference of the six-digit displayed values 5.858736 - 5.858691. The same page's interpretation (L24.html:243) correctly says 4.4e-16, so the two passages disagree.",
    fix="L24.html line 348: change 'They differ by \\(4.5 \\times 10^{-16}\\)' to 'They differ by \\(4.4 \\times 10^{-16}\\)' (one ulp of e is 4.44e-16). Do not change the displayed 6-digit values. Regenerate nothing; the lab code is unchanged.")
row("N-L24-E3-exact-and-grid", "2.2 numbers: exact central error e(sinh h/h - 1) = 4.530e-11, 4.530e-13, 4.530e-15; grid spacing ulp(e)/(2h) = 2.2e-11 and 2.2e-9",
    f"{P}/L24.html:348", "PASS",
    f"{S}/l24_numbers.out: e*(sinh h/h-1) = 4.530470e-11 at 1e-5, 4.530470e-13 at 1e-6, 4.530470e-15 at 1e-7 (Decimal, precision 60); ulp(e)/(2h) = 2.220e-11 and 2.220e-09.")
row("N-L24-minimizers", "2.2 numbers: predicted minimizers 2 sqrt(delta/e) = 1.8e-8 and (3 delta/e)^(1/3) = 6.3e-6 with delta = 2.22e-16",
    f"{P}/L24.html:136 (hypothesis), card M2-c370", "PASS",
    f"{S}/l24_numbers.out: 2*sqrt(2.22e-16/e) = 1.807e-08; (3*2.22e-16/e)^(1/3) = 6.257e-06.")
row("N-L24-E2-roundoff-bound", "2.2 numbers: round-off bound 2 delta/h = 0.444 at h=1e-15; printed error 0.390", f"{P}/L24.html:341 (E2)", "PASS",
    f"{S}/l24_numbers.out: 2*2.22e-16/1e-15 = 0.444; page table prints 3.903e-01 at 1e-15 (twin_vs_page.out).")
row("N-L24-half-ulp", "2.2 numbers: delta = 2.22e-16 described as half a unit in the last place of values near e", f"{P}/L24.html:136", "PASS",
    f"{S}/l24_numbers.out: ulp(e)=4.44e-16, half ulp = 2.22e-16 (math.ulp).")
row("N-L24-decade-ratios", "2.2 numbers: printed fall from 1e-4 to 1e-5 is about 77; central errors fall by 100 per decade to 1e-4; exact central at 1e-5 = 4.530e-11",
    f"{P}/L24.html:243", "PASS", f"{S}/twin_vs_page.out Part B: 4.531e-09 / 5.859e-11 = 77.3; 4.533e-03 -> 4.530e-05 -> 4.530e-07 -> 4.531e-09 (factor 100); exact 4.530470e-11 (l24_numbers.out).")
row("N-L24-M3-numbers", "2.2 numbers: M3 forward quotient 12.61, error 0.61, bound 0.63 with M_2 = 12.6", f"{P}/L24.html:298 (M3 solution)", "PASS",
    "Recomputed by hand: (2.1^3 - 8)/0.1 = 12.61; M_2 = sup |6x| on [2, 2.1] = 12.6; 0.5*12.6*0.1 = 0.63 (arithmetic only).")

# ---- labs: statements vs code and output ----
row("LAB-L22-statements", "2.5 labs: L22 hypothesis, docstring, interpretation and E-problems vs code and output",
    f"{P}/L22.html:99, :100-112, :231", "PASS",
    f"{S}/twin_vs_page.out. Hypothesis: golden-section on [0,10] (code: golden_max(...,0.0,10.0)); h=1e-4; Part B x*(a-x) on [0,a]; printed naive partial 0. Docstring: 'Standard library only; no randomness'. The phrase 'the lab checks two problems ... tests no other objectives' matches Part A (4 values) and Part B (3 values).")
row("LAB-L23-statements", "2.5 labs: L23 hypothesis, docstring and interpretation vs code and output",
    f"{P}/L23.html:90, :91-107, :226", "PASS",
    f"{S}/twin_vs_page.out and l23_numbers.out. Part B has three positive shifts (0.01, 0.005, 0.0025); Part C prints two (+0.01, -0.01); previews printed only, as the page says; FI1 title 'Bond Math & Curve Construction' and Macaulay/convexity placement read from curriculum/curriculum.json (FI1).")
row("LAB-L24-statements", "2.5 labs: L24 hypothesis, docstring and interpretation vs code and output",
    f"{P}/L24.html:136, :137-149, :243", "PASS",
    f"{S}/twin_vs_page.out Part A six steps all +1/-1/0; Part B decade grid k=1..15 and printed minima 10^-8 (forward), 10^-5 (central). Every printed error in the interpretation equals the output table; the signed claims are in l24_numbers.out.")
row("LAB-L22-L24-expected", "2.5 labs: run_labs expected blocks and tolerance", f"{P}/L22.html:222, L23.html:215, L24.html:218", "PASS",
    f"{S}/gates_r7.out (run_labs PASS) and twin_vs_page.out (exact match).")

# ---- grades (one row per claim span class) ----
row("GR-L22-T", "2.3 grades: Lemma 1.2, Theorem 1.3, Proposition 2.1 and the Example 2.3 kink graded T",
    f"{P}/L22.html:63, :73, :239, :256, key results :395-398", "PASS",
    "Each T claim has a complete proof on the page (see M-L22 rows). Remark 1.4 and Example 1.5 are ungraded and say which assumption they use (Assumption 1.1, IVT and EVT from L21 and L06).")
row("GR-L23-T", "2.3 grades: Propositions 2.1, 2.2, 3.2, 3.3, Theorem 3.1 graded T", f"{P}/L23.html:67, :79, :232, :242, :252, key results :405-409", "PASS",
    "Each has a complete proof (M-L23 rows). Lab results are graded C naming Lab 1 on the cards (M2-c341..c346, c352, c382..c385, c407).")
row("GR-L24-T", "2.3 grades: Theorem 2.1, Propositions 3.1, 3.2, 4.2, 4.3 graded T", f"{P}/L24.html:60, :74, :84, :106, :116, key results :385-389", "PASS",
    "Each has a complete proof under its stated hypotheses (M-L24 rows); the round-error results are conditional on Definition 4.1, stated as such.")

# ---- mathematics: derivations and key formulas, re-derived by hand and numerically ----
row("M-L22-lemma-thm", "2.4 math: Lemma 1.2 and Theorem 1.3 proofs (chain rule and first-order condition)", f"{P}/L22.html:63-83", "PASS",
    "Read every line; the first-order condition uses differentiability of phi on open J (H1); the chain-rule step needs f differentiable (H1) and x_hat differentiable (H3), both stated. No hidden hypothesis.")
row("M-L22-remark14", "2.4 math: Remark 1.4 (local (H3) from the implicit-function theorem applied to G(a,x)=f_x(x,a))", f"{P}/L22.html:88", "PASS",
    f"Checked against L21.html:69-75: L21 Theorem 1.3 gives a unique zero g(x) in J for each x in I and F_y != 0 on I x J, so the zero of f_x(.,a) in K is unique, as the remark says; G is C^1 because f is C^2. Assumption 1.2 (IVT) is L21 Assumption 1.2 (L21.html:63-64).")
row("M-L22-example15", "2.4 math: Example 1.5, f_x = a/(1+x)-1, x_hat = a-1, V = a ln a - (a-1), V' = ln a", f"{P}/L22.html:91-95", "PASS",
    "f_x zero at a-1 (a/(1+x)=1); f_xx = -a/(1+x)^2 < 0; V(a) = a ln(a) - (a-1); V'(a) = ln a + a(1/a) - 1 = ln a (hand). Assumption 1.1 is named and stated as assumed.")
row("M-L22-prop21", "2.4 math: Proposition 2.1 (constraint solved for one variable): proof via Theorem 1.3 applied to F and the chain rule", f"{P}/L22.html:240-246", "PASS",
    "F_a = g_y c_a + g_a by the chain rule (g C^1 on U containing the graph); V = max_x F. Hypotheses (H1)-(H3) on F are stated as assumed. The proof is complete.")
row("M-L22-example22-23", "2.4 math: Example 2.2 (xy on x+y=a, V=a^2/4) and Example 2.3 (max ax on [0,1])", f"{P}/L22.html:250-257", "PASS",
    "F=x(a-x): F_x=a-2x, x_hat=a/2, F_xx=-2; V=a^2/4; g_y c_a + g_a = a/2 (hand). Example 2.3: one-sided derivatives 1 and 0 at a=0 (hand: (V(h)-V(0))/h=1 for h>0, 0 for h<0 side).")
row("M-L22-problems", "2.4 math: problem set solutions M1-M3, P1-P3, E1-E3, R1-R3 (L22)", f"{P}/L22.html:290-386", "PASS",
    "Each solution recomputed: M1 V=a^2/2, V'=a, f_a=a; M2 x_hat=a+3/2, V=3a+9/4, V'=3; M3 F=x(a-x)/2, V=a^2/8, V'=a/4 (quiz 0.25 at a=1); P2 V=max(a,0); R1 Remark 1.4; R2 vector form labelled as not proved; R3 Example 2.3.")
row("M-L23-prop21-22", "2.4 math: Proposition 2.1 derivatives and sign results; Proposition 2.2 (price equals face at yield = coupon rate)", f"{P}/L23.html:69-85", "PASS",
    "Derivative formulas by term-by-term differentiation of (1+y)^(-t) (hand). Prop 2.2: v=1/(1+r), 1-v=rv, sum v^t = (1-v^N)/r, so the price is F(1-v^N)+Fv^N = F; r=0 case treated. Geometric series cited to M1 L06 (verified present: M1/L06.html, 'Geometric series and proof by induction').")
row("M-L23-thm31-prop32", "2.4 math: Theorem 3.1 (remainder bound with M), Proposition 3.2 (sign of R = (1/6)P'''(theta) Delta^3 with P'''<0)", f"{P}/L23.html:233-248", "PASS",
    "P''' = -sum t(t+1)(t+2)c_t(1+y)^(-t-3) (hand, d/dy of (1+y)^(-t-2)). Lagrange remainder of order 2 from L08 Theorem 2.1 (L08.html proves it from Rolle, lines 'Proof'). EVT assumption used for M. Complete.")
row("M-L23-prop33", "2.4 math: Proposition 3.3 (first-order error = (1/2)P''(theta)Delta^2 >= 0)", f"{P}/L23.html:252-258", "PASS",
    f"{S}/l23_numbers.out: first-order errors +403.8, +102.8, +25.9 at +0.01, +0.005, +0.0025 and +434.8 at -0.01 (all >= 0), consistent with the proof.")
row("M-L23-problems", "2.4 math: L23 problem set M1-M3, P1-P3, E1-E3, R1-R3", f"{P}/L23.html:300-395", "PASS",
    "M1 par 1000 (Prop 2.2); M2 P''=2c(1+y)^-3; M3 P'(0.04)=-200/1.04^3 (-177.80, not printed on the page); P1 uses Corollary 3.1 (ii) on -P and on P' (L06.html:102-103, requires continuity on [a,b] and differentiability on (a,b): satisfied); P3 Lagrange order one; E1 signs consistent with output; E2 limits 4 and 8; E3 offset 2.78e-18 and -2.1e-12 (l23_numbers.out); R1 dy/dP = 1/P' from L21 Theorem 2.1 (L21.html:87); R2 Theorem 3.1 applies to Delta=0.5.")
row("M-L24-thm21-prop31-32", "2.4 math: Theorem 2.1 (|x| quotients), Propositions 3.1 and 3.2 (truncation bounds), proofs", f"{P}/L24.html:60-93", "PASS",
    "Theorem 2.1: forward 1, backward -1, central 0 for every h>0; limit does not exist (hand). Prop 3.1 from Taylor order one with f''. Prop 3.2 subtraction gives (1/12)h^2(f'''(xi1)+f'''(xi2)), bound (1/6)M_3 h^2 (hand). Taylor order two is L08 Theorem 2.1.")
row("M-L24-prop42-43", "2.4 math: Proposition 4.2 and 4.3 (bound functions and minimizers h*=2 sqrt(delta/M_2) and (3 delta/M_3)^(1/3)), proofs",
    f"{P}/L24.html:107-123", "PASS",
    "g(h)=Ah+B/h minimized at sqrt(B/A): A=M_2/2, B=2delta gives 2 sqrt(delta/M_2); value 2 sqrt(AB)=2 sqrt(M_2 delta). Prop 4.3: h^3=B/(2C)=3delta/M_3. Round-off terms 2delta/h (forward) and delta/h (central) from Definition 4.1 (hand). Hypothesis H stated in each statement.")
row("M-L24-remark44-assumption", "2.4 math (round-6 FAIL re-verified): Remark 4.4 claims about the bound at h* and H",
    f"{P}/L24.html:129; card M2-c365", "PASS",
    "Round 6 failed the sentence 'the true error at h* is at most the bound only if h* is in H'. The page now reads 'The bound is guaranteed at h* only if h* is in H ... When h* is not in H, Proposition 4.2 says nothing about the error at h*'. This states what Proposition 4.2 guarantees, which is what the proposition's own statement says, and it no longer claims the error exceeds the bound outside H. The round-6 counterexample (f=x^2 at 0, M_2=1.5, delta=1: error 1.633 <= bound 2.449 with h* not in H) is therefore not contradicted. Note the round-6 suggested sentence ('the true error ... can be at most the bound without that') was not copied verbatim; the page's next sentence covers the point. PASS.")
row("M-L24-problems", "2.4 math: L24 problem set M1-M3, P1-P3, E1-E3, R1-R3", f"{P}/L24.html:281-375", "PASS",
    "M1 x^2 quotients (h, -h, 0 errors); M2 |x| at 0 with h=0.5 gives 0 and 1; M3 12.61 (hand); P1 kink; P2 Prop 3.1 proof; P3 rewrite identity; E1 constancy by algebra; E2 round-off bound 0.444 vs printed 0.390; E3 see N-L24-E3-difference (FAIL row); R1 M_2 overestimated by 100: step one tenth and round-off 10 sqrt(M_2 delta) (hand); R2 Lipschitz bound (hand); R3 cites L14 automatic differentiation (L14.html:59 Definition 1.1 defines it; Section 2 gives the forward mode).")

# ---- cards ----
row("CARD-L22", "2.7 cards: all 15 L22 cards (M2-c323..c337, c404) against the current L22 text and card-to-page numbers",
    f"{P}/cards.json (lesson L22)", "PASS",
    "Each card read; the numbers in M2-c328/c329/c336 are in the lab output; c326 names the L21 Assumption 1.2 and L06 Assumption 2.1 used by L22 (L21.html:63, L06.html:72); card hypotheses for c331 and c325 match the statements; misconception references (c334, c335, c336) match the page.")
row("CARD-L23", "2.7 cards: all 24 L23 cards (M2-c338..c357, c382..c386, c407) against the current L23 text",
    f"{P}/cards.json (lesson L23)", "PASS",
    "Each card read; numbers (108110.895779, 108111, 117060, 100000, -851466.739529, 8376648.511919, 3.9279/3.9634, 7.8807/7.9396, -15/+16, 4.037716e+02, -1.506081e+01) match the output; grades C name Lab 1; the card hypotheses (Prop 3.2, 3.3, Theorem 3.1) match the statements.")
row("CARD-L24", "2.7 cards: all 18 L24 cards (M2-c358..c373, c375, c387, c405, c410) against the current L24 text",
    f"{P}/cards.json (lesson L24), M2-c365 at cards.json:2564", "PASS",
    "Round-6 CARD-L24 re-verified: M2-c365's back now says 'The bound is guaranteed at h* only if h* is in H ... When h* is not in H, Proposition 4.2 says nothing about the error at h*', matching the page (L24.html:129). The other L24 cards match their pages (c370 numbers 1.8e-8 and 6.3e-6; c371 'Misconception 1'; c372 and c373 Theorem 2.1).")
row("CARD-DUP", "2.7 cards: no duplicate card in L22-L24 and none across the unit", f"{P}/cards.json", "PASS",
    f"{S}/cards_scan.out: 394 cards, no duplicate ids or backs; the one front collision is P'(y0) vs P''(y0).")

# ---- structure, prose, DAG, hours ----
row("S-L22-L24-structure", "2.9 structure: section order, quiz of 8 items per lesson (numeric and multiple choice), references, lesson nav",
    f"{P}/L22.html, L23.html, L24.html", "PASS",
    f"{S}/gates_r7.out (check_pages PASS for each page); quiz item counts read from the pages: L22 8 items, L23 8 items, L24 8 items.")
row("S-banned-phrases", "2.9 banned phrases (BUILDER_RULES 1.3-1.4): TODO, TBD, lorem, ellipsis, for brevity, beyond the scope, left as an exercise, important to note, studies show, well known, obviously, clearly",
    f"{P}/L22.html, L23.html, L24.html", "PASS",
    f"{S}/prose_scan.out: 'banned hits: []' and 'ellipsis hits: []' for all three pages (visible prose, scripts and expected blocks removed).")
row("S-process-words", "2.9 no process words in learner text (round, builder, verifier, architect, fixed, revised)", f"{P}/L22.html, L23.html, L24.html", "PASS",
    f"{S}/prose_scan.out: 'process' hits are only 'fixed x' and 'fixed at' (mathematical sense) and 'round-off' (technical term); no builder, verifier, architect or revision word.")
row("S-scope-words", "4 scope words (only, all, always, every, any, same, exactly, most, small, about, never): each has a computation or a stated hypothesis",
    f"{P}/L22.html, L23.html, L24.html", "PASS",
    f"{S}/prose_scan.out gives the counts (L22 26, L23 55, L24 71 scope-word hits). Each was read in context: 'every c_t > 0' etc. are hypotheses; 'about 1e-8' is backed by the printed output; 'small yield change' is backed by the Part B shifts; 'the lab checks two problems ... tests no other objectives' matches the code; 'Lab 1 establishes this for these shifts only' is limited to the printed shifts."),
row("DAG-prerequisites", "2.9 DAG: L22-L24 use only concepts of M2 lessons up to their own, M1 (present value, discount factor, geometric series), P0.1 and prose-only later terms",
    f"{P}/L22.html:37, L23.html:37, L24.html:37", "PASS",
    f"{S}/gates_r7.out: check_dag M2 PASS. Links: L04 def-derivative, L08 def-taylor-theorem, L13, L14 def-automatic-differentiation, L16, L17, L19 def-hessian, L21 def-implicit-function-theorem (all ids exist, links_and_terms.out). M1 concepts present-value, discount-factor, geometric-series exist in concepts.html (m1_refs.out). Later-module terms appear only in prose: 'call option' (L23 Section 4), 'duration' and 'convexity' as previews (L23 lab docstring and meta description, per architect Q8), 'Lipschitz' (L24 R2), as allowed by architect rulings Q5-Q8.")
row("DAG-no-later-definitions", "2.9 DAG: no concept defined twice; no later-module dfn or link (Fubini, continuity, Riemann-Stieltjes, Lebesgue, Lagrange multiplier, epsilon-delta)", f"{P}/L22.html, L23.html, L24.html", "PASS",
    f"{S}/prose_scan.out: 'later-module hits: []' on all three pages for Lagrange multiplier, Lagrangian, Fubini, Riemann-Stieltjes, Lebesgue, epsilon-delta, linear map, vector space, positive-semidefinite. 'Lagrange form' refers to the L08 Taylor remainder, not to a multiplier concept.")
row("H-hours", "2.9 hours: data-hours=10 and '10 study hours' on each of L22, L23, L24; lesson total is the hub's business", f"{P}/L22.html:2, L23.html:2, L24.html:2", "PASS",
    f"{S}/gates_r7.out: check_pages PASS for each page (declares 10 h, the 6-12 h rule).")
row("REF-cross-lesson", "2.1 attributions: L22 and L23 and L24 cross-references to L06 Assumption 2.1 and Theorem 2.3, L21 Theorem 1.3, Theorem 2.1 and Assumption 1.2, L08 Theorem 2.1, M1 L05 and L06 read in the source lessons",
    f"{P}/L22.html:473, L23.html:488, L24.html:468", "PASS",
    "L06.html:72-73 (Assumption 2.1 = extreme value theorem, assumed); L06.html:87-88 (Theorem 2.3 = mean value theorem, assuming Assumption 2.1); L06.html:102-103 (Corollary 3.1 (i)-(iii)); L21.html:63-64 (Assumption 1.2 = IVT); L21.html:68-75 (Theorem 1.3 proof: uniqueness by IVT, differentiability by MVT); L21.html:86-87 (Theorem 2.1 slope formula); L08.html Theorem 2.1 (Lagrange remainder, stated with Assumption 1.1 = EVT, proved from Rolle); M1 L05 'Present value and the discount factor', M1 L06 'Geometric series and proof by induction'. No bibliographic data is typed on these pages; the two registry keys are named without a locator, as the pages say.")
row("REG-registry-flags", "2.1 registry: no key cited with a locator on L22-L24; nothing to flag", f"{P}/L22.html:473, L23.html:488, L24.html:468", "PASS",
    f"{S}/gates_r7.out: verify_refs --offline 560 entries 0 problems. Live verify_refs --unit M2 was not run (network; the live run is the scheduled job's).")

# ---- lab-only slice: no grader, no mutants (architect ruling 9) ----
mutants = []

fragment = {
    "unit": "M2",
    "slice": "d2",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for M2-d2, round 7 (did not build M2; no context shared with the builders).",
    "pin": "9373ef398589097500ea849e30ff9da423b98943",
    "base": "142ecfc2bd27061de18bd67e83df81e69f5c249d (round-6 pin). Delta 142ecfc2..9373ef39 touches only course/modules/M/M2/L22.html, L23.html, L24.html and cards.json (git diff --stat: 4 files, 24 insertions, 18 deletions). Every hunk was read (git diff output in the verifier transcript). All 69 round-6 rows were re-verified from scratch on this pin; no PASS row is carried forward.",
    "checkout": str(CHECKOUT),
    "scratch": f"{CHECKOUT}/{S}",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Lab-only slice: no project grader is in L22-L24, so mutate_graders.py is not applicable and mutants is empty (architect ruling 9). "
        "Not run: verify_refs --unit M2 (live, network); repository-wide gates (check_pages --all, build_site --check, render_curriculum, run_graders); "
        "the other slices of M2. Alternative correct implementations are not applicable (no grader). "
        "Round-6 non-PASS rows: MATH-L24-remark44-assumption and CARD-L24 are PASS now (wording changed on the page and card; see rows). "
        "The one new defect is a regression introduced in round 6: L24.html:348 states the unrounded difference as 4.5e-16 (it is 4.44e-16; the interpretation at L24.html:243 says 4.4e-16). "
        "Round-6 observations (a)-(c) carried as observations: L22 lab hypothesis points to Example 2.2 and L23 lab hypothesis points to Theorem 3.1 before those statements (pointers, not undefined terms); L22 Problem M3 does not restate the open intervals (the solution takes a > 0). Not defects. "
        "Open item 4 in plans/M2-open-items.md ('Fact 2.1') is out of date: L06 names the EVT as Assumption 2.1 and the pages cite it that way (L06.html:72), so no page is wrong."
    ),
    "summary": (
        "slice d2 round 7: rows=%d, pass=%d, fail=%d, unverifiable=0. Mutants 0 (lab-only slice). "
        "Single non-PASS row: N-L24-E3-difference (L24.html:348, '4.5e-16' should be '4.4e-16')."
        % (len(rows), sum(1 for r in rows if r["status"] == "PASS"), sum(1 for r in rows if r["status"] == "FAIL"))
    ),
}

out = CHECKOUT / "ledgers/M2/M2-d2.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "fail", sum(1 for r in rows if r["status"] == "FAIL"))
