import json, sys
from datetime import datetime, timezone
ROOT = "/Users/billyribeiro/.fanout/wt/verifyB7-M2-d"
prev = {r["id"]: r for r in json.load(open("/Users/billyribeiro/.fanout/frags/B-M2-d.round6.json"))["rows"]}
S = "ledgers/M2/scripts/M2-d-r7"
CARRY = "Carried from round 6 (course/modules/M/M2/L19.html, L20.html, L21.html, L22.html, L23.html, L24.html and tests/labs/M2 twins: the cited subject is byte-identical since the previous pin 44f1eb6; the page as a whole changed, the cited block did not, per git diff 44f1eb6..7aa909e): "
def carry(rid, files=None, note=""):
    p = prev[rid]
    ev = CARRY + p["evidence"] + (" " + note if note else "")
    return {"id": rid, "check": p["check"], "location": p["location"], "status": "PASS", "evidence": ev}
def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r
R = []
# ---- gates, run by this verifier on pin 7aa909e (outputs in S/)
R.append(row("G-check-pages", "check_pages gate for M2", "tools/check_pages.py --all", "PASS", f"{S}/check_pages.out: 'check_pages M2: PASS', exit 0"))
R.append(row("G-check-dag", "check_dag gate for M2", "tools/check_dag.py --all", "PASS", f"{S}/check_dag.out: 'check_dag M2: PASS', exit 0"))
R.append(row("G-check-projects", "check_projects gate for M2 (listed, not the project slice)", "tools/check_projects.py --all", "PASS", f"{S}/check_projects.out: 'check_projects M2: PASS', exit 0"))
for L in ["19", "20", "21", "22", "23", "24"]:
    R.append(row(f"G-run-labs-L{L}", f"run_labs: lab of L{L} matches twin and twin output matches page expected block", f"tools/run_labs.py --unit M2 --page L{L}; course/modules/M/M2/L{L}.html <section class=\"lab\">", "PASS",
        f"{S}/run_labs_L{L}.out: 'run_labs M2: PASS (1/1)', exit 0; exact line comparison of page expected block vs twin output: {S}/exact_expected.py -> EXACT (L{L})"))
R.append(row("G-twins-isolated", "Each slice twin alone under python -I -W error, no stderr", "tests/labs/M2/lab-M2-L19-1.py .. lab-M2-L24-1.py", "PASS", f"{S}/twin_L19..L24.err all 0 bytes; exit 0 for all six"))
R.append(row("G-page-smoke", "page_smoke on the six slice pages (Chromium)", "tools/page_smoke.py --unit M2 --pages L19 L20 L21 L22 L23 L24", "PASS", f"{S}/page_smoke.out: 'page_smoke M2: PASS', exit 0"))
R.append(row("G-ruff", "ruff check and ruff format --check on six slice twins", "tests/labs/M2/lab-M2-L19-1.py, lab-M2-L20..L24-1.py", "PASS", f"{S}/ruff.out: 'All checks passed!', '6 files already formatted'"))
R.append(row("G-mypy", "mypy --no-incremental on six slice twins and full repo", "tests/labs/M2/lab-M2-L19..L24-1.py; mypy full", "PASS", f"{S}/mypy.out: 'Success: no issues found in 6 source files'; {S}/mypy_full.out: 'Success: no issues found in 255 source files'"))
R.append(row("G-pytest-labs", "pytest tests/test_labs.py -k M2", "tests/test_labs.py", "PASS", f"{S}/pytest_labs_M2.out: pytest -q output is all dots, exit 0"))
R.append(row("G-pytest-docs-figures", "pytest tests/test_docs_figures.py (quoted figures in docs)", "tests/test_docs_figures.py", "PASS", f"{S}/pytest_docs.out: pytest -q output is all dots, exit 0"))
R.append(row("G-verify-refs", "verify_refs --offline integrity", "tools/verify_refs.py --offline", "PASS", f"{S}/verify_refs.out: 'offline integrity: 560 entries, 0 problems', exit 0"))
R.append(row("G-build-site", "build_site --check (site data current)", "tools/build_site.py --check", "PASS", f"{S}/build_site.out: 'site data current: 6 outputs', exit 0"))

# ---- L19
R.append(carry("L19-math-def-ex", note="Definition 1.1 and Example 1.2 text unchanged in the diff."))
R.append(carry("L19-math-thm21", note="Theorem 2.1 statement and proof unchanged in the diff (only Remark 3.2 and misconception 2 changed)."))
R.append(carry("L19-math-ex22"))
R.append(carry("L19-math-thm31"))
R.append(carry("L19-math-prop33"))
R.append(row("L19-math-remark-R2-R3", "Remark 3.2 (changed this round), Research R2 and R3",
    "course/modules/M/M2/L19.html Remark 3.2 (line ~112); Research R2, R3", "PASS",
    "Remark 3.2 now writes d^T H d = d1^2 f_xx + d1 d2 (f_xy + f_yx) + d2^2 f_yy, which is correct (d^T H d expands with H_12 = f_xy and H_21 = f_yx). With f_xy = f_yx it is d1 d2 * 2 f_xy, as stated. Theorem 2.1's hypotheses hold for the smooth Lab-1 f = e^x y + x y^2 (checked: f_xy = e^x + 2y, f_yx = e^x + 2y, see tests/labs/M2/lab-M2-L19-1.py line 26-39). Research R2 and R3 unchanged in diff."))
R.append(row("L19-prose-lab-numbers", "Prose numbers in Lab 1 interpretation vs printed output", "course/modules/M/M2/L19.html lab expected block and interpretation; twin output", "PASS",
    f"Exact line comparison of the page expected block with {S}/twin_L19.out: EXACT (10 lines). Lab interpretation unchanged in the diff; its numbers (2.26e-11, 1.94e-11) are the printed values of the expected block."))
R.append(carry("L19-scope-words", note="Interpretation and E1 unchanged in the diff."))
R.append(row("L19-canon-misconception-quiz", "Canon breaks, misconceptions, quiz answers (changed misconception 2 re-verified)", "course/modules/M/M2/L19.html sections 4, 5, 8; misconception 2", "PASS",
    "Misconception 2 (changed): cross term present when f_xy(p) != 0; f_xy(0.5, 0.25) = e^0.5 + 0.5 = 2.148721 (independent: exp(0.5)+0.5 = 2.1487213); the two mixed entries equal for the smooth f by Theorem 2.1. Other misconceptions and quiz answers unchanged in the diff."))

# ---- L20
R.append(carry("L20-math-thm12"))
R.append(carry("L20-math-prop22"))
R.append(carry("L20-math-prop24"))
R.append(carry("L20-math-ex31"))
R.append(row("L20-prose-lab", "Lab 1 prose vs output (exact errors -1/6, -1/24, -1/96; six n values; odd-square identity)", "course/modules/M/M2/L20.html lab interpretation; expected block", "PASS",
    f"Exact line comparison of the page expected block with {S}/twin_L20.out: EXACT (8 lines). Lab interpretation unchanged in the diff (lab_L20 values reproduced by the twin)."))
R.append(carry("L20-quiz-misc", note="Section 7 and misconceptions unchanged in the diff."))
R.append(row("L20-problems-res2", "Research R2 solution (rewritten this round): the scope and hypothesis claims about Example 3.1",
    "course/modules/M/M2/L20.html line 330 (R2 solution); line 215 (Example 3.1 domain statement); line 125-127 (Example 3.1, Assumption 3.1)", "FAIL",
    "The new solution says 'Example 3.1 shows that the equality cannot hold for every integrand on a rectangle' and that 'any proof of the general statement must use a hypothesis that rules out Example 3.1'. The page itself says (line 215) that the domain of Example 3.1 is the half-open square (0,1]^2 and 'is not a closed rectangle'; the general statement of Remark 2.3 is about a continuous integrand on a rectangle, so Example 3.1 lies outside the scope the solution is reasoning about. The solution also states that the two orders disagree as a fact, without the qualifier that Example 3.1 gives under Assumption 3.1 (the arctangent facts), which the page states at line 125 and 127 (rule 9: assumed facts need a named assumption).",
    "Qualify the disagreement with 'under Assumption 3.1', and state that Example 3.1 is on (0,1]^2, not a closed rectangle, so it shows that a bare integrability or boundedness-free hypothesis is insufficient on half-open rectangles rather than that every proof must rule out it. Or reword to: 'Example 3.1, under Assumption 3.1, shows that the equality can fail for an unbounded integrand on a half-open square; the closed-rectangle statement of Remark 2.3 is not refuted by it.'"))

# ---- L21
R.append(carry("L21-math-thm12", note="Theorem 1.2 statement and proof unchanged in the diff."))
R.append(carry("L21-math-thm21-ex22"))
R.append(carry("L21-math-ex31-32"))
R.append(row("L21-prose-lab", "Lab 1 slopes and residuals vs independent bisection root and formula", "course/modules/M/M2/L21.html lab interpretation and expected block", "PASS",
    f"Exact line comparison of the page expected block with {S}/twin_L21.out: EXACT (5 lines). Only the references paragraph changed in L21 (see REF-registry)."))
R.append(carry("L21-problems", note="Problem set unchanged in the diff."))

# ---- L22
R.append(carry("L22-math-lemma-thm13", note="Lemma 1.2 and Theorem 1.3 statement and proof unchanged in the diff."))
R.append(row("L22-math-remark14", "Remark 1.4 (changed): the function and symbol used to apply L21 Theorem 1.2",
    "course/modules/M/M2/L22.html line 88 (Remark 1.4) and line 465 (quiz explanation)", "FAIL",
    "Remark 1.4 (changed this round) now names the function G(a, x) = f_x(x, a), but in the same sentence says 'where the partial derivative of F in x is f_xx'. F is not defined in Remark 1.4 (F is introduced only in Proposition 2.1, line 239). The quiz explanation at line 465 says 'apply Theorem 1.2 of L21 to F = f_x'. The argument is otherwise correct: G_x = f_xx (chain of L21 Theorem 1.2 with a as the independent variable).",
    "Replace 'the partial derivative of F in x' with 'the partial derivative of G in x' in line 88, and make the quiz explanation at line 465 use G = f_x, matching Remark 1.4."))
R.append(row("L22-math-ex15-prop21", "Example 1.5, Proposition 2.1 (changed), Examples 2.2-2.3, Mechanics M1-M3, Proposition 2.1 formula", "course/modules/M/M2/L22.html Example 1.5, Proposition 2.1 and proof, Example 2.2, M3", "PASS",
    "Re-derived: Prop 2.1 with C^1 g and c, F = g(x, c(x,a), a) satisfying (H1)-(H3) of Theorem 1.3 (J, I open intervals are set in §1); chain rule gives F_a = g_y c_a + g_a; V' = g_y c_a + g_a at x_hat. Example 2.2: F = x(a-x), F_x = a-2x, x_hat = a/2, V = a^2/4, V' = a/2 = (a/2)(1) + 0. M3: F = x(a-x)/2, x_hat = a/2, F_xx = -1, V = a^2/8, V' = a/4 = (a/2)(1/2). Example 1.5: V = a ln a - (a-1), V' = ln a. All agree."))
R.append(carry("L22-math-ex23-P2", note="Example 2.3 and proof P2 unchanged in the diff."))
R.append(row("L22-prose-lab", "Lab 1 prose numbers (1e-8 location error, f_xx=-0.666667, 3.3e-17, Part B 5.4e-12) vs printed output", "course/modules/M/M2/L22.html lab interpretation; expected block", "PASS",
    f"Exact line comparison of the page expected block with {S}/twin_L22.out: EXACT (9 lines). ln(1.5)=0.405465108 printed as 0.40546511 (all four Part A rows match ln a to eight decimals). Part B errors 1.9e-13, 1.0e-12, 5.4e-12; largest 5.4e-12. f_xx=-a/(1+x)^2 at a=1.5, x=0.5 is -0.6667. Half times 0.667 times 1e-16 = 3.3e-17."))
R.append(row("L22-lab-naive-partial", "Lab 1 Part B: the naive partial is computed, not asserted", "tests/labs/M2/lab-M2-L22-1.py lines 77-86, 106-113; course/modules/M/M2/L22.html line 99", "PASS",
    "Round-6 FAIL is fixed: the naive partial is now naive_partial = central_difference(frozen_product(x_star, a - x_star), a, STEP), a central difference of a function that does not depend on a, so the printed 0 is a computed value (zero by construction of the frozen function; the page says 'computed as zero' in the twin comment and 'prints the naive partial ... which is zero' on line 99). Printed output matches the page (exact comparison, twin_L22.out). Reduced partial is computed by central_difference(reduced_objective(x_star), a, STEP) and matches a/2."))
R.append(row("L22-prop21-hypothesis", "Proposition 2.1 states every hypothesis explicitly", "course/modules/M/M2/L22.html Proposition 2.1 (line ~239)", "PASS",
    "Round-6 FAIL is fixed: the statement now names J and I (open intervals as in Theorem 1.3), U open in R^3 containing {(x,c(x,a),a)}, c C^1 on J x I, F = g(x,c(x,a),a) satisfying (H1)-(H3) of Theorem 1.3 on J x I with maximizer x_hat(a), and y*(a) = c(x_hat(a), a). The proof needs these: C^1 of F follows from C^1 g and c; the constrained max equals max_x F. Without the hypothesis list the claim is unverifiable; with it the proof is complete."))

# ---- L23
R.append(carry("L23-math-prop21", note="Proposition 2.1 statement and proof unchanged in the diff; P' < 0 when every c_t > 0 re-checked."))
R.append(row("L23-math-prop22", "Proposition 2.2 (changed: coupon rate r) and proof", "course/modules/M/M2/L23.html Proposition 2.2 and proof (line ~80-86)", "PASS",
    "Proof re-derived: v = 1/(1+r); 1 - v = r v; sum_{t=1}^N v^t = v(1-v^N)/(1-v) = (1-v^N)/r; rF * that = F(1-v^N); price = F(1-v^N) + F v^N = F. r = 0 case: coupons zero, v = 1, price F. Statement and proof use r consistently after the rename."))
R.append(row("L23-math-thm31-prop32-33", "Theorem 3.1, Propositions 3.2 (changed: hypothesis y0 > -1) and 3.3 (changed)", "course/modules/M/M2/L23.html §3 (lines ~225-250)", "PASS",
    "Theorem 3.1: P_1 and P_2 defined; R = P - P_2 with |R| <= (1/6) M |Delta|^3 (Lagrange, three derivatives; the proof cites L08). Prop 3.2: P''' = -sum t(t+1)(t+2) c_t (1+y)^(-t-3) < 0 when c_t > 0, so R = P'''(theta) Delta^3 / 6 has the sign of -Delta. Independent check: unrounded second-order error at +0.01 is -1.506081e+01 (negative, the sign of -Delta; see L23-prose-numbers). Prop 3.3: P - P_1 = P''(theta) Delta^2 / 2 >= 0 since P'' > 0. Both hypotheses y0 > -1 added are the ones the proofs need."))
R.append(row("L23-prose-numbers", "Prose numbers in L23 (108110.895779, -851466.74, 8376648.51, 1.9, 7.875864, 77.482001, error ratios, -15/+16 cents)", "course/modules/M/M2/L23.html why-it-matters, lab interpretation, misconceptions, quiz; twin output", "PASS",
    f"Independent Decimal(60-digit) re-derivation: {S}/indep/bond_check.py prints P(y0)=108110.895779, integer 108111, P1=-851466.739529, P2=8376648.511919, second-order errors -1.506081e+01 / -1.911100e+00 / -2.407040e-01, first-order errors 4.037716e+02 / 1.027970e+02 / 2.593632e+01, ratio1 3.927854 and 3.963438 (printed 3.9279, 3.9634), ratio2 7.880704 and 7.939627 (printed 7.8807, 7.9396), cents at +0.01 exact 100000 second 100015 diff -15, at -0.01 exact 117060 second 117044 diff 16, -P'/P = 7.875864, P''/P = 77.482001. Page expected block equals twin output exactly ({S}/twin_L23.out, EXACT, 11 lines). Central-difference numbers are float checks (page expected block shows -851466.741081, the twin output matches)."))
R.append(row("L23-problems-quiz", "Mechanics M1-M3, Research R1 (changed: G), quiz answers (changed: explanation L23q2)", "course/modules/M/M2/L23.html problem set, research R1, quiz", "PASS",
    "M1 (changed: coupon rate r): F=1000, r=0.05, N=2, coupon 50, price 1000 by Proposition 2.2; direct check 50/1.05 + 1050/1.05^2 = 47.619 + 952.381 = 1000.000. R1 (changed symbol G(P0,y) = P(y) - P0): G_{P0} = -1, G_y = P'(y), dy/dP0 = -G_{P0}/G_y = 1/P'(y) < 0 since P'(y) < 0 (Proposition 2.1). E3 solution: unrounded price 100000 at yield 0.05 rounds to 100000 cents (Prop 2.2 exact at yield 0.05; the float yield 0.04+0.01 differs from 0.05 by ~1e-18, price difference ~2e-12 cents, rounding unaffected). Quiz explanation L23q2 now 'yield equal to coupon rate r = 0.05' consistent."))
R.append(row("L23-cards-meta-introduces", "Introduces meta line vs Definition 1.1 and 'at par' wording (round-6 FAIL)", "course/modules/M/M2/L23.html line 38", "PASS",
    "Round-6 FAIL is fixed: line 38 now reads 'none in the concept index (Definition 1.1 and the term at par are prose definitions with no index entry)'. Definition 1.1 (line ~58) and 'A bond priced at its face value is said to be at par' (line ~62) are the two prose definitions named. Check_pages and check_dag pass (G-check-pages, G-check-dag)."))
R.append(row("L23-notation-F", "NOTATION: symbol F used with one meaning per lesson (round-6 FAIL)", "course/modules/M/M2/L23.html Proposition 2.2 (F = face), M1, R1; lab twin", "PASS",
    "Round-6 FAIL is fixed: F now means only the face value (Prop 2.2 lines 80-85, M1 line ~300); the R1 function is G (line ~361); the lab twin uses no F. Remaining uses of 'F' in L23 are all face value (grep of rendered text)."))
R.append(row("L23-money-int-cents", "Money: bond price in integer cents, no float money (round-6 FAIL, architect Q12 and plan line 365)", "course/modules/M/M2/L23.html Definition 1.1, Section 4 bullet, E3; tests/labs/M2/lab-M2-L23-1.py price, taylor_first, taylor_second, round", "PASS",
    "Round-6 FAIL is fixed: price(y), price_first_derivative, price_second_derivative and taylor_first/second now return fractions.Fraction (exact); the only rounding is price_cents = round(price(y)) (Fraction round is round-half-even), which returns int. The float appears only in printed values and central-difference checks. Reported price is int cents (108111, 100000, 117060 printed as integers). Note for the architect (not a row FAIL): plan Q12 says sensitivities are floats with a stated tolerance; the lab keeps sensitivities as exact rationals, which the E3 solution states honestly. Recorded in notes."))

# ---- L24
R.append(carry("L24-math-thm21", note="Theorem 2.1 statement and proof unchanged in the diff."))
R.append(carry("L24-math-prop31-32", note="Propositions 3.1, 3.2 and proofs unchanged in the diff."))
R.append(row("L24-math-prop42-43", "Propositions 4.2, 4.3, Assumption 4.1 (new), lab hypothesis (changed), interpretation", "course/modules/M/M2/L24.html Proposition 4.2 and 4.3 with proofs; lab hypothesis line ~59; Assumption 4.1 line ~53", "PASS",
    "Re-derived: Prop 4.2 bound 1/2 M2 h + 2 delta/h, min at h* = 2 sqrt(delta/M2), value 2 sqrt(M2 delta). Prop 4.3 bound 1/6 M3 h^2 + delta/h, min at h^3 = 3 delta/M3. Numerics from the page: 2 sqrt(2.22e-16/e) = 1.8074e-8 (page 1.8e-8); (3 * 2.22e-16 / e)^(1/3) = 6.2574e-6 (page 6.3e-6). Assumption 4.1 (d/dx e^x = e^x) is named and is used as a stated assumption. Lab hypothesis now writes 'Assuming Assumption 4.1' (rule 9)."))
R.append(row("L24-prose-lab-table", "Lab 1 Part B prose (changed interpretation) vs printed table", "course/modules/M/M2/L24.html interpretation; ledgers/M2/scripts/M2-d-r7/twin_L24.out", "PASS",
    f"Exact line comparison of page expected block with {S}/twin_L24.out: EXACT (25 lines). Independent recomputation ({S}/indep/l24_check.py, IEEE double, the lab's formula): central error at 1e-5 = 5.858691309868e-11 and at 1e-7 = 5.858735718789e-11, difference 4.44e-16 = one ulp of e (math.ulp, 4.4409e-16); the printed 5.859e-11 at both is the rounding. Central errors at 1e-4 = 4.530566e-09 (page 4.531e-09 reads as the printed table). Forward error at 1e-8 printed 6.603e-09 and at 1e-9 2.154e-07 match the table."))
R.append(row("L24-problems-quiz", "Mechanics, Proof, Empirical E1-E3 (changed E3 solution), Research R1 (changed to 2 delta/h ratio), quiz", "course/modules/M/M2/L24.html problem set and quiz", "PASS",
    "E3 solution (changed): unrounded errors 5.858691e-11 at 1e-5 and 5.858736e-11 at 1e-7 (recomputed above); they differ by 4.4e-16, one ulp of values near e. R1 solution (changed): h = 2 sqrt(delta/(100 M2)) = h*/10; round-off 2 delta/h = 10 * 2 delta/h* = 10 sqrt(M2 delta), i.e. ten times the round-off term at h*, which is sqrt(M2 delta) since 2 delta/h* = sqrt(M2 delta). Correct. Quiz answers unchanged in the diff."))
R.append(row("L24-meta-introduces", "Introduces meta line vs Definition 4.1 and 'cancellation' (round-6 FAIL)", "course/modules/M/M2/L24.html line 38", "PASS",
    "Round-6 FAIL is fixed: line 38 now reads 'none in the concept index (cancellation and the error hypothesis, Definition 4.1, are prose definitions with no index entry)'. Definition 4.1 (the error hypothesis) at line ~44 and 'this loss is called cancellation' at line ~43 are the prose definitions named. G-check-dag passes."))
R.append(carry("L24-AD-link", note="Research R3 unchanged in the diff."))

# ---- cross-cutting
R.append(row("CARDS-slice", "Cards for L19-L24 (cards.json, 99 slice cards (lesson L19..L24) M2-c280..c387) agree with the current lesson text; ids and fronts unique; every card number appears in its lesson",
    "course/modules/M/M2/cards.json lines 2325 (M2-c330) and 2360 (M2-c335)", "FAIL",
    "18 slice cards changed since 44f1eb6; re-checked each against the current text. Ids and fronts unique (python check); card numbers (108110.895779, 108111, 117060, 100015, 4.037716e+02, -1.506081e+01, 3.9279/3.9634, 7.8807/7.9396, 5.4e-12, 0.5/1.0/1.5, pi/4, -pi/4) appear in the lessons. STALE: M2-c330 back says 'misses the term f_y c_a = a/2 (Proposition 2.1)' and M2-c335 back says 'Proposition 2.1 shows the missing term f_y c_a'. Proposition 2.1 on the current page (L22.html line ~239-247) is written with g: the term is g_y c_a. Rule 10 (cards agree with current text).",
    "Edit course/modules/M/M2/cards.json (via the card source, then regenerate per the repo's generator if one exists) so M2-c330 and M2-c335 read g_y c_a instead of f_y c_a, matching Proposition 2.1 and Example 2.2 on the page. Note: cards.json is listed as a generated-from-source file in some units; check the source before editing."))
R.append(carry("DAG-prereq-use", note="Prerequisite lessons (L06, L08, L09, L10, M1 geometric series) used in text unchanged in the diff."))
R.append(row("DAG-links-anchors", "Every concept link anchor in L19-L24 resolves to a def id on the target page", "course/modules/M/M2/L19..L24 concept links", "PASS", f"G-check-dag M2 PASS ({S}/check_dag.out) covers concept anchors; L23/L24 meta lines changed text only."))
R.append(row("DAG-architect-decisions", "Architect decisions: Fubini prose-only (L20 Remark 2.3), no multiplier concept (L22), duration and convexity unlinked preview (L23)", "course/modules/M/M2/L20.html Remark 2.3; L22.html (grep 'multiplier' = 0); L23.html lab docstring line 91", "PASS",
    "L20 Remark 2.3 unchanged; L22 contains no 'multiplier' (grep count 0); L23 lab docstring says 'Duration and convexity are previewed, not defined' and the preview numbers are printed only, with no link. Plan Q8 and Q3 satisfied."))
R.append(carry("HOURS", note="data-hours=\"10\" on each slice page and hub card lines unchanged for L19..L24 (index.html diff touches only the L11 card title)."))
R.append(row("STRUCT-process-words", "No process words in learner text", "course/modules/M/M2/L19..L24.html (rendered text)", "PASS", "grep -E 'round [0-9]|verifier|builder|draft|TODO|placeholder|corrected|revised|reviewer|this round|previous round' over tag-stripped L19..L24: no matches."))
R.append(row("STRUCT-scope-words", "Scope words (only, all, always, every, any, same, drives, exactly, small, smooth) used only with a computation", "course/modules/M/M2/L19..L24.html changed sentences", "PASS",
    "Every changed hunk was read for scope words. The only unsupported scope claim introduced this round is 'cannot hold for every integrand on a rectangle' in L20 R2 (row L20-problems-res2, FAIL). Other new scope words ('exact', 'every', 'for every y > -1') are backed by the proofs or the derivative formula on the page. Full-page re-scan not repeated; rows whose blocks are unchanged carry round-6 PASS."))
R.append(row("STRUCT-define-before-use", "Terms defined or linked at first appearance; symbols defined before use", "course/modules/M/M2/L22.html lines 88 and 465; L19..L24", "FAIL",
    "F is used in L22 Remark 1.4 (line 88) as 'the partial derivative of F in x' with no definition there (the sentence defines G, not F), and in the quiz explanation (line 465) as 'F = f_x'. F is first defined in Proposition 2.1 (line 239) with a different meaning (F(x,a) = g(x,c(x,a),a)). Same defect as row L22-math-remark14.",
    "Use G in Remark 1.4 and the explanation at line 465 (see L22-math-remark14)."))
R.append(carry("REF-registry", note="Changed references paragraphs re-checked below; the rest carried."))
R[-1] = row("REF-registry", "Cited registry keys exist; no locator attributed from memory; theorem numbers cited from other lessons exist", "course/modules/M/M2/L19..L24.html references sections; references/references.json", "PASS",
    "Registry keys spivak2008calculus and hubbard2015vector are cited without locator (unchanged rule). Cross-lesson theorem numbers in the changed references paragraphs were read: L06 Theorem 2.3 is the mean value theorem (L06.html line ~87); L08 Theorem 2.1 is Taylor's theorem with the Lagrange remainder (L08.html line ~90); L21 Theorem 1.2 is the implicit-function theorem and its proof uses the mean value theorem (L21.html line 32). verify_refs --offline: 560 entries, 0 problems (G-verify-refs).")
R.append(row("NOTATION-registry", "Registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) not reused with another meaning in L19..L24", "notation/notation.json vs L19..L24", "PASS",
    "notation/notation.json has 8 symbol entries (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). grep over L19..L24 finds none of them as symbols. R is used as the Taylor remainder (L19 Theorem 3.1 region, L23 Theorem 3.1), which is not a registered symbol. F and G used as local symbols are per-lesson and now single-meaning except the F defect in row L22-math-remark14."))

out = {
    "unit": "M2", "slice": "d", "round": 7,
    "verifier": "Haiku 5.5 independent verifier, slice d (L19-L24), round 7",
    "pin": "7aa909e", "base": "44f1eb6",
    "checkout": ROOT, "scratch": ROOT + "/" + S,
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}
fails = [r for r in R if r["status"] != "PASS"]
out["verdict"] = "PASS" if not fails else "FAIL"
out["rows"] = R
out["mutants"] = []
out["registry_flags"] = []
out["freshness_flags"] = []
out["notes"] = (
    "Round 7 delta from 44f1eb6 to 7aa909e for slice d: changed L19 (Remark 3.2, misconception 2, refs), L20 (R2 solution), L21 (refs), L22 (Remark 1.4, Proposition 2.1 now with g, Example 2.2, M3, P3, E2, table, quiz explanation, refs, lab naive partial and reduced partial, tests/labs/M2/lab-M2-L22-1.py), L23 (Fraction exact arithmetic in tests/labs/M2/lab-M2-L23-1.py, Definition 1.1, Prop 2.2 with r, Prop 3.2/3.3 hypotheses, canon breaks, M1, E3, R1 with G, quiz explanation, meta), L24 (Assumption 4.1, lab hypothesis, interpretation, E3, R1, meta), cards.json (18 slice cards). Every changed hunk in the six pages and the two twins was read. Round-6 FAIL rows L22-lab-naive-partial, L22-prop21-hypothesis, L23-cards-meta-introduces, L23-notation-F, L23-money-int-cents, L24-meta-introduces are re-verified PASS. Unchanged math rows carried with prefix. "
    "Money note (not a row FAIL): plan Q12 says sensitivities are floats with a stated tolerance; the L23 lab keeps P', P'' and Taylor terms as exact Fraction values and prints them as floats. The page (E3, Section 4) says so. The architect should confirm this is acceptable. "
    "Lab twins are demonstrations; no grader mutation rows (mutation testing is for project graders, not in this slice). Mutants: none run; none required for lab twins. "
    "Could not check: the M2 project slice (not in this slice); rendered visual layout beyond page_smoke; the exact Remark 3.2 wording against any printed value (none printed); the cards generator (whether cards.json is regenerated from a source file; I did not determine the source)."
)
out["summary"] = (f"Slice d (L19-L24), round 7 at 7aa909e: verdict {out['verdict']}. {len(R)} rows, {len(fails)} non-PASS: "
    "L20-problems-res2 (R2 solution scope and Assumption 3.1 qualifier, low), L22-math-remark14 (F used for G in Remark 1.4 and quiz explanation, low), STRUCT-define-before-use (same F defect, low), CARDS-slice (M2-c330 and M2-c335 still say f_y c_a, low). All round-6 FAIL rows are re-verified PASS.")
json.dump(out, open(ROOT + "/ledgers/M2/M2-d.json", "w"), indent=1, ensure_ascii=False)
print("rows", len(R), "fails", len(fails), [r["id"] for r in fails])
