import json, sys
R7 = "Carried from round 7 ("
P = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    P.append(r)

S = "ledgers/M2/scripts/M2-d-r8/"
# ---- gates, run in this round on pin ce7b382 ----
row("G-check-pages", "check_pages gate for M2", "tools/check_pages.py --unit M2 and --all", "PASS",
    S + "check_pages.out: 'check_pages M2: PASS', exit 0; " + S + "check_pages_all.out: 'check_pages M2: PASS', exit 0")
row("G-check-dag", "check_dag gate for M2", "tools/check_dag.py --unit M2", "PASS", S + "check_dag.out: 'check_dag M2: PASS', exit 0")
row("G-check-projects", "check_projects gate for M2 (listed, not the project slice)", "tools/check_projects.py --unit M2", "PASS",
    S + "check_projects.out: 'check_projects M2: PASS', exit 0")
for p in ["L19", "L20", "L21", "L22", "L23", "L24"]:
    row("G-run-labs-" + p, "run_labs: lab of %s matches twin; twin output equals page expected block" % p,
        "tools/run_labs.py --unit M2 --page %s; course/modules/M/M2/%s.html <pre class=expected>" % (p, p), "PASS",
        S + "run_labs_%s.out: 'run_labs M2: PASS (1/1)', exit 0; exact line comparison (ledgers/M2/scripts/M2-d-r7/exact_expected.py, run on twin_%s.out with the appended exit line removed): EXACT, %s lines" % (p, p, {"L19":10,"L20":8,"L21":5,"L22":9,"L23":11,"L24":25}[p]))
row("G-twins-isolated", "Each slice twin alone under python -I -W error, no stderr", "tests/labs/M2/lab-M2-L19-1.py .. lab-M2-L24-1.py", "PASS",
    S + "twin_L19..L24.err all 0 bytes; command 'python -I -W error <twin>' exit 0 for all six (rechecked this round)")
row("G-page-smoke", "page_smoke on the six slice pages", "tools/page_smoke.py --unit M2 --pages L19 L20 L21 L22 L23 L24", "PASS",
    S + "page_smoke.out: 'page_smoke M2: PASS', exit 0")
row("G-ruff", "ruff check and ruff format --check on six slice twins", "tests/labs/M2/lab-M2-L19..L24-1.py", "PASS",
    S + "ruff.out: 'All checks passed!', '6 files already formatted', exit 0")
row("G-mypy", "mypy --no-incremental on six slice twins and full repo", "tests/labs/M2/lab-M2-L19..L24-1.py; full mypy", "PASS",
    S + "mypy.out: 'Success: no issues found in 6 source files'; " + S + "mypy_full.out: 'Success: no issues found in 255 source files'")
row("G-pytest-labs", "pytest tests/test_labs.py -k M2", "tests/test_labs.py", "PASS", S + "pytest_labs_M2.out: 27 dots, exit 0")
row("G-pytest-docs-figures", "pytest tests/test_docs_figures.py", "tests/test_docs_figures.py", "PASS", S + "pytest_docs.out: 14 dots, exit 0")
row("G-verify-refs", "verify_refs --offline integrity", "tools/verify_refs.py --offline", "PASS", S + "verify_refs.out: 'offline integrity: 560 entries, 0 problems', exit 0")
row("G-build-site", "build_site --check (site data current)", "tools/build_site.py --check", "PASS", S + "build_site.out: 'site data current: 6 outputs', exit 0")

# ---- L19 ----
row("L19-math-def-ex", "Definition and examples, lines ~50-80 and ~330-360", "course/modules/M/M2/L19.html", "PASS",
    R7 + "course/modules/M/M2/L19.html lines ~50-80 and ~330-360 byte-identical since pin 7aa909e; the only delta hunk in L19.html is line 372): round-7 re-derivation stands.")
row("L19-math-thm21", "Theorem 2.1 and proof", "course/modules/M/M2/L19.html Theorem 2.1 and proof", "PASS",
    R7 + "L19.html Theorem 2.1 block byte-identical since 7aa909e; delta hunk at line 372 is outside it).")
row("L19-math-ex22", "Example 2.2", "course/modules/M/M2/L19.html lines ~70-80", "PASS",
    R7 + "L19.html Example 2.2 block byte-identical since 7aa909e; delta hunk at line 372 is outside it).")
row("L19-math-thm31", "Theorem 3.1 and proof", "course/modules/M/M2/L19.html line 99-107 (Theorem 3.1 and proof)", "PASS",
    R7 + "L19.html lines 99-107 byte-identical since 7aa909e; delta hunk at line 372 is outside them; ω(r) = sup{max|H_ij(p+q)-H_ij(p)| : |q| <= r} at line 100).")
row("L19-math-prop33", "Proposition 3.3", "course/modules/M/M2/L19.html Proposition 3.3", "PASS",
    R7 + "L19.html Proposition 3.3 block byte-identical since 7aa909e; delta hunk at line 372 is outside it).")
row("L19-math-remark-R2-R3", "Remark 3.2; Research R2 (three-variable extension) and R3",
    "course/modules/M/M2/L19.html line 372 (R2 solution); line 100 (Theorem 3.1 definition of omega); Remark 3.2 and R3 unchanged",
    "FAIL",
    "R2 solution (line 372) was changed in this delta, only by the HTML escape of '<' to '&lt;' (html.unescape diff against 7aa909e: 0 lines differ). Its mathematics re-derived: (sum|h_i|)^2 = sum h_i^2 + 2 sum_{i<j}|h_i||h_j| <= sum h_i^2 + sum_{i<j}(h_i^2+h_j^2) = n|h|^2 (2|h_i||h_j| <= h_i^2+h_j^2 is correct); so |R(h)| <= (1/2) n |h|^2 max|dH| <= n|h|^2 omega, a valid bound. DEFECT: the same sentence says 'with omega defined by the maximum over the entries of H'. Theorem 3.1 (line 100) defines omega(r) = sup{max_ij |H_ij(p+q) - H_ij(p)| : |q| <= r}, a modulus of the change in H over |q| <= r, which tends to 0. The R2 wording, read alone, defines omega as the maximum entry of H, which neither tends to 0 nor depends on |h|. Remark 3.2 and R3 are byte-identical since 7aa909e.",
    "In L19.html line 372, replace 'with \\(\\omega\\) defined by the maximum over the entries of \\(H\\)' with 'with \\(\\omega\\) as in Theorem 3.1, the largest change in an entry of \\(H\\) over \\(|q| \\le |h|\\)'.")
row("L19-prose-lab-numbers", "Lab expected block, interpretation and twin output",
    "course/modules/M/M2/L19.html lab expected block and interpretation; twin output " + S + "twin_L19.out", "PASS",
    "Exact line comparison of page expected block with " + S + "twin_L19.out: EXACT (10 lines). Interpretation numbers (ratios 3.9750/7.9429 at step 0.025 etc.) match twin output lines.")
row("L19-scope-words", "Scope words in interpretation and E1", "course/modules/M/M2/L19.html interpretation and E1", "PASS",
    R7 + "L19.html interpretation and E1 blocks byte-identical since 7aa909e; delta hunk at line 372 is in the R2 solution, which contains no scope word beyond 'every' in the Hessian entries sentence checked above).")
row("L19-canon-misconception-quiz", "Sections 4, 5, 8 and Misconception 2",
    "course/modules/M/M2/L19.html sections 4, 5, 8; misconception 2", "PASS",
    R7 + "L19.html sections 4, 5, 8 and misconception 2 byte-identical since 7aa909e; delta hunk at line 372 is outside them).")

# ---- L20 ----
for rid, chk, loc in [
    ("L20-math-thm12", "Theorem 1.2 (iterated sums)", "course/modules/M/M2/L20.html Theorem 1.2"),
    ("L20-math-prop22", "Proposition 2.2 and proof", "course/modules/M/M2/L20.html Proposition 2.2 and proof"),
    ("L20-math-ex31", "Example 3.1 (domain, integrand, Assumption 3.1 values)", "course/modules/M/M2/L20.html lines 208-212 (Example 3.1 block) and lines 125-127 region"),
]:
    row(rid, chk, loc, "PASS",
        R7 + "L20.html lines outside 199 and 330 byte-identical since 7aa909e; the delta hunks are at 199 (escape only) and 330 (R2 solution, see L20-problems-res2)). Example 3.1 re-derived in this round: d/dy[y/(x^2+y^2)] = (x^2-y^2)/(x^2+y^2)^2 gives inner integral 1/(1+x^2) and outer pi/4; the other order gives -pi/4 (checked line 209 block).")
row("L20-math-prop24", "Proposition 2.4 and proof (midpoint identities)", "course/modules/M/M2/L20.html line 199 (proof, facts (i) and (ii)) and Proposition 2.4", "PASS",
    "Line 199 changed in this delta only by '<' -> '&lt;' (html.unescape diff: the only other changed line is 330). Re-derived: (i) sum_i x_i (1/n) = (1/(2n^2)) n^2 = 1/2; (ii) sum_{i<n}(2i+1)^2 = n(4n^2-1)/3, induction step n(4n^2-1)+3(2n+1)^2 = 4n^3+12n^2+11n+3 = (n+1)(4(n+1)^2-1); sum_i x_i^2 (1/n) = (1/(4n^3)) n(4n^2-1)/3 = 1/3 - 1/(12 n^2). Twin output line 'n = 32 ... predicted error -1/(6 n^2) ... match True' agrees.")
row("L20-prose-lab", "Lab interpretation and expected block", "course/modules/M/M2/L20.html lab interpretation (line 189) and expected block", "PASS",
    "Exact line comparison with " + S + "twin_L20.out: EXACT (8 lines). Line 189 numbers (n = 1..32, error -1/(6 n^2)) match twin output.")
row("L20-quiz-misc", "Section 7 and misconceptions", "course/modules/M/M2/L20.html section 7 and misconceptions", "PASS",
    R7 + "L20.html section 7 and misconception blocks byte-identical since 7aa909e; delta hunks at 199 and 330 are outside them).")
row("L20-problems-res2", "R2 solution: scope of 'Example 3.1 is not a counterexample' and the hypothesis claim",
    "course/modules/M/M2/L20.html line 330 (R2 solution); line 209 (Example 3.1 block); line 212; line 215 (domain bullet)", "FAIL",
    "Line 330 (changed in this delta) now says: 'Under Assumption 3.1, Example 3.1 shows that the two iterated integrals can differ ... That square is not a closed rectangle, so the example does not refute the closed-rectangle statement. Any hypothesis under which the equality holds for every integrand must fail for the integrand of Example 3.1'. The example is on (0,1]^2 (line 209) and line 215 says its domain is not a closed rectangle, so the integrand is outside the class to which a closed-rectangle hypothesis applies. A hypothesis on that class is therefore not shown to 'fail' for this integrand; the sentence asserts a necessity the page does not establish. Its wording 'any ... must fail' is a universal scope claim with no argument. Values re-derived: pi/4 and -pi/4 (correct). The defect is the necessity claim, not the arithmetic.",
    "Replace the last sentence of line 330 with: 'Example 3.1 shows that the statement is false for integrands unbounded on (0,1]^2, which is not a closed rectangle; so a general statement over that class needs some hypothesis, and this example does not show which hypothesis is necessary for the closed-rectangle statement, which this page does not prove.'")
row("L20-prose-lab-interp", "Lab interpretation numbers", "course/modules/M/M2/L20.html interpretation at line 189", "PASS",
    "Covered by L20-prose-lab: EXACT expected block and twin output; n = 1, 2, 4, 8, 16, 32 errors -1/(6 n^2) match twin output (n=32: error -1/6144 = -1/(6*32^2)).")

# ---- L21 (unchanged file) ----
for rid, chk, loc in [
    ("L21-math-thm12", "Theorem 1.2 and proof", "course/modules/M/M2/L21.html Theorem 1.2"),
    ("L21-math-thm21-ex22", "Theorem 2.1 and Example 2.2", "course/modules/M/M2/L21.html Theorem 2.1, Example 2.2"),
    ("L21-math-ex31-32", "Examples 3.1, 3.2 and Section 3", "course/modules/M/M2/L21.html Examples 3.1, 3.2"),
    ("L21-problems", "Problem set", "course/modules/M/M2/L21.html problem set"),
]:
    row(rid, chk, loc, "PASS", R7 + "course/modules/M/M2/L21.html byte-identical since pin 7aa909e (no delta hunk in L21.html)); cards delta for L21 is M2-c310 and was checked in CARDS-slice.")
row("L21-prose-lab", "Lab interpretation and expected block", "course/modules/M/M2/L21.html lab interpretation and expected block", "PASS",
    "Exact line comparison with " + S + "twin_L21.out: EXACT (5 lines). Residuals and F_y values match twin output.")

# ---- L22 ----
row("L22-math-lemma-thm13", "Lemma 1.2 and Theorem 1.3", "course/modules/M/M2/L22.html lines 63-80", "PASS",
    R7 + "L22.html lines 63-80 byte-identical since 7aa909e; delta hunks at lines 88, 456, 465 are outside them).")
row("L22-math-remark14", "Remark 1.4 (where H3 comes from) and the two quiz explanations that cite it",
    "course/modules/M/M2/L22.html line 88 (Remark 1.4); line 456 (Problem M3 explanation); line 465 (L22q8 explanation)", "PASS",
    "Round-7 FAIL is fixed. Line 88 now reads 'where the partial derivative of G in x is f_xx != 0' with G(a,x) = f_x(x,a) defined in the same sentence; F no longer appears in Remark 1.4. Hypotheses checked against L21 Theorem 1.2 (line 63-65 of L21.html): f C^2 gives G C^1; G(a0, xhat(a0)) = f_x(xhat(a0), a0) = 0 by Lemma 1.2 (L22 line 63); partial of G in x at that point is f_xx != 0. Line 465 now reads 'apply Theorem 1.2 of L21 to G(a, x) = f_x(x, a), whose partial in x is f_xx'. Line 456 now reads 'V'(1) = 1/4' for V(a) = a^2/8 (max of xy s.t. x+2y=a: y=(a-x)/2, x=a/2, value a^2/8, V' = a/4 at a=1 gives 0.25, matching data-answer 0.25).")
row("L22-math-ex15-prop21", "Example 1.5, Proposition 2.1 and proof, Example 2.2, M3", "course/modules/M/M2/L22.html Example 1.5 and Proposition 2.1 (lines 238-250) and Example 2.2", "PASS",
    R7 + "L22.html Example 1.5, Proposition 2.1 and proof (lines 238-250 and the Example 2.2 block) byte-identical since 7aa909e; delta hunks at 88, 456, 465 are outside them). Prop 2.1 formula V' = g_y c_a + g_a re-derived in round 7 and unchanged.")
row("L22-math-ex23-P2", "Example 2.3 and P2", "course/modules/M/M2/L22.html Example 2.3, P2", "PASS",
    R7 + "L22.html Example 2.3 and P2 byte-identical since 7aa909e; delta hunks outside them).")
row("L22-prose-lab", "Lab interpretation and expected block", "course/modules/M/M2/L22.html lab interpretation; expected block", "PASS",
    "Exact line comparison with " + S + "twin_L22.out: EXACT (9 lines). V' values 1.00000001, 1.50000001 and central differences 1.00000000, 1.50000000 match the twin output lines.")
row("L22-lab-naive-partial", "Lab twin naive partial", "tests/labs/M2/lab-M2-L22-1.py lines 77-86, 106-113; course/modules/M/M2/L22.html line 99", "PASS",
    R7 + "tests/labs/M2/lab-M2-L22-1.py and L22.html line 99 byte-identical since 7aa909e).")
row("L22-prop21-hypothesis", "Proposition 2.1 statement (open intervals J, I and open U)", "course/modules/M/M2/L22.html Proposition 2.1 (line 239)", "PASS",
    R7 + "L22.html line 239 byte-identical since 7aa909e).")

# ---- L23 ----
row("L23-math-prop21", "Proposition 2.1 and proof", "course/modules/M/M2/L23.html Proposition 2.1 and proof", "PASS",
    R7 + "L23.html Proposition 2.1 block byte-identical since 7aa909e; the only delta hunk is line 222).")
row("L23-math-prop22", "Proposition 2.2 and proof (lines ~80-86)", "course/modules/M/M2/L23.html lines ~80-86", "PASS",
    R7 + "L23.html lines ~80-86 byte-identical since 7aa909e; the only delta hunk is line 222).")
row("L23-math-thm31-prop32-33", "Theorem 3.1, Propositions 3.2 and 3.3", "course/modules/M/M2/L23.html section 3 (lines ~225-250)", "PASS",
    R7 + "L23.html section 3 byte-identical since 7aa909e; line 222 is in Lab 1 interpretation, above section 3).")
row("L23-prose-numbers", "Lab 1 interpretation (line 222) numbers, ratios, differences, twin output",
    "course/modules/M/M2/L23.html line 222 (lab interpretation); expected block; " + S + "twin_L23.out", "PASS",
    "Line 222 changed in this delta (new sentence on ratio definition and the 15/16-cent differences). Checked against " + S + "twin_L23.out: 108110.895779 -> 108111 (integer price) OK; P'(y0) -851466.739529 (|.| 851466.74 OK), difference 1.6e-03 OK; P''(y0) 8376648.511919 (8376648.51 OK), difference 1.9 OK; ratios 3.9279, 3.9634 (first) and 7.8807, 7.9396 (second) OK; '-15' at +0.01 (100000 vs 100015) and '16' at -0.01 (117060 vs 117044) OK; code computes ratio as previous_error / current_error (lab line 'ratios' = float(previous/e1)), which is the definition the new sentence gives; preview 7.875864 = -P'/P and 77.482001 = P''/P printed by code, not defined in lesson (stated). Independent check of prices in " + S + "indep/ (Decimal 60-digit recomputation) is in round 7 and the lab code is unchanged since 7aa909e.")
row("L23-problems-quiz", "Problem set, research R1, quiz", "course/modules/M/M2/L23.html problem set, research R1, quiz", "PASS",
    R7 + "L23.html problem set, R1 and quiz byte-identical since 7aa909e; the only delta hunk is line 222).")
row("L23-cards-meta-introduces", "Line 38 meta sentence", "course/modules/M/M2/L23.html line 38", "PASS",
    R7 + "L23.html line 38 byte-identical since 7aa909e).")
row("L23-notation-F", "Symbol F in Proposition 2.2, M1, R1 and lab twin", "course/modules/M/M2/L23.html Proposition 2.2, M1, R1; tests/labs/M2/lab-M2-L23-1.py", "PASS",
    R7 + "L23.html Proposition 2.2 (F = face), M1, R1 and lab-M2-L23-1.py byte-identical since 7aa909e).")
row("L23-money-int-cents", "Money as integer cents; Definition 1.1, Section 4 bullet, E3, lab price and taylor", "course/modules/M/M2/L23.html Definition 1.1, Section 4, E3; tests/labs/M2/lab-M2-L23-1.py price, taylor", "PASS",
    R7 + "L23.html Definition 1.1, Section 4, E3 and tests/labs/M2/lab-M2-L23-1.py byte-identical since 7aa909e; line 222 change does not touch them). Lab output integer cents: 108111, 100000, 117060 match.")

# ---- L24 (unchanged file) ----
row("L24-math-thm21", "Theorem 2.1 and proof", "course/modules/M/M2/L24.html Theorem 2.1 and proof", "PASS",
    R7 + "L24.html byte-identical since 7aa909e; no delta hunk in L24.html).")
row("L24-math-prop31-32", "Propositions 3.1, 3.2 and proofs", "course/modules/M/M2/L24.html Propositions 3.1, 3.2", "PASS",
    R7 + "L24.html byte-identical since 7aa909e).")
row("L24-math-prop42-43", "Propositions 4.2, 4.3, lab hypothesis, Assumption 4.1", "course/modules/M/M2/L24.html Propositions 4.2, 4.3 and Assumption 4.1", "PASS",
    R7 + "L24.html byte-identical since 7aa909e).")
row("L24-prose-lab-table", "Lab interpretation, expected block and table", "course/modules/M/M2/L24.html interpretation; " + S + "twin_L24.out", "PASS",
    "Exact line comparison with " + S + "twin_L24.out: EXACT (25 lines). Twin outputs 6.603e-09 (forward, h=1e-8) and 5.859e-11 (central, h=1e-5) match the page.")
row("L24-problems-quiz", "Problem set and quiz", "course/modules/M/M2/L24.html problem set and quiz", "PASS",
    R7 + "L24.html byte-identical since 7aa909e).")
row("L24-meta-introduces", "Line 38 meta sentence", "course/modules/M/M2/L24.html line 38", "PASS", R7 + "L24.html line 38 byte-identical since 7aa909e).")
row("L24-AD-link", "Research R3 and L14 link", "course/modules/M/M2/L24.html research R3; L14.html Definition 1.1", "PASS",
    R7 + "L24.html R3 and L14.html byte-identical since 7aa909e).")

# ---- cards ----
row("CARDS-slice", "Slice cards (96 cards in L19-L24) after the delta", "course/modules/M/M2/cards.json (slice lessons)", "PASS",
    "Delta vs 7aa909e (" + S + "cards_delta.py, cards_r7.json vs cards_r8.json): removed M2-c290 (L19), M2-c344 and M2-c356 (L23); changed slice cards M2-c310 (L21), M2-c330 and M2-c335 (L22). Round-7 FAIL on M2-c330/c335 is fixed: 'f_y c_a' -> 'g_y c_a', matching Proposition 2.1 (L22.html line 245/250: g_y c_a + g_a); with g_y = x = a/2 and c_a = 1 the term is a/2 (correct). M2-c310 hypotheses match L21 Theorem 1.2 (L21.html line 63-65) and the slope formula line 82. Numbers: " + S + "cards_numbers_r8.py finds every number in every slice card's front and back in its lesson (0 missing; 96 slice cards; 0 duplicate ids or fronts). Unchanged slice cards are byte-identical since 7aa909e.")
row("CARDS-c299-uses-nowhere", "Card M2-c299 (Remark 2.3) says the lesson 'uses it nowhere'", "course/modules/M/M2/cards.json line 2121 (M2-c299); course/modules/M/M2/L20.html lines 214, 330, 420", "FAIL",
    "Card back: 'No. This lesson does not prove that general statement, gives it no grade, and uses it nowhere.' L20.html cites Remark 2.3 as a hypothesis or referent at line 214 ('Remark 2.3 leaves the general case unproved'), line 330 (solution: 'the hypothesis in the general statement of Remark 2.3') and line 420 (explanation). No proof on the page depends on it, so the defect is the absolute 'nowhere', a scope word contradicted by the text.",
    "In cards.json M2-c299 replace 'and uses it nowhere' with 'and no proof on this page depends on it' (this is a source edit: the card comes from course/modules/M/M2/cards.json as the builder's source; regenerate per the unit's card pipeline).")

# ---- DAG / structure / registry ----
row("DAG-prereq-use", "Prerequisite-closure use of concepts in L19..L24 prose", "course/modules/M/M2/L19..L24 prose", "PASS",
    R7 + "L19-L24 prose byte-identical except the delta hunks listed here; check_dag PASS this round (" + S + "check_dag.out)).")
row("DAG-links-anchors", "Concept links and anchors", "course/modules/M/M2/L19..L24 concept links", "PASS",
    "check_dag M2 PASS this round (" + S + "check_dag.out); check_pages M2 PASS (" + S + "check_pages.out) covers anchors.")
row("DAG-architect-decisions", "Architect decisions on prose-only concepts", "course/modules/M/M2/L20.html Remark 2.3; L22.html; L23.html lab docstring", "PASS",
    "grep -i multiplier course/modules/M/M2/L22.html: 0 matches (this round). L20 Remark 2.3 block unchanged; L23 lab docstring unchanged since 7aa909e.")
row("HOURS", "Hours arithmetic on hub split", "course/modules/M/M2/L19..L24.html line 2; course/modules/M/M2/index.html line 29", "PASS",
    R7 + "line 2 of L19..L24 and index.html line 29 byte-identical since 7aa909e; no delta hunk there).")
row("STRUCT-process-words", "No process words in learner text", "course/modules/M/M2/L19..L24.html (rendered text)", "PASS",
    "grep -n -i -E 'round [0-9]|verifier|builder|draft|TODO|placeholder|corrected|revised|reviewer|this round|previous version' over L19..L24.html: 0 matches (this round).")
row("STRUCT-scope-words", "Scope words in changed sentences", "course/modules/M/M2/L20.html line 330; L19.html line 372; L22.html lines 88, 456, 465; L23.html line 222", "FAIL",
    "Every changed sentence was read. Line 330 introduces 'Any hypothesis under which the equality holds for every integrand must fail for the integrand of Example 3.1': a universal scope claim with no argument and outside the closed-rectangle class the hypothesis governs (see L20-problems-res2). Line 372 changes are escape-only except the omega definition (see L19-math-remark-R2-R3). L22 lines 88, 456, 465 contain no unsupported scope word. L23 line 222 'Each ratio is ...', 'the lab does not establish any accuracy beyond these two shifts' are backed by the code and twin output.",
    "Rewrite the line 330 sentence as stated under L20-problems-res2 so that it claims no necessity the page does not prove.")
row("STRUCT-define-before-use", "Symbols defined before use in L19..L24", "course/modules/M/M2/L22.html lines 88 and 465; L19..L24", "PASS",
    "Round-7 FAIL is fixed: F no longer appears in L22 Remark 1.4 (line 88) or the L22q8 explanation (line 465); G(a,x) = f_x(x,a) is defined in the sentence that uses it. Other F uses in L22 (lines 107, 208, 239, 250, 307) are defined in place: F(x,a) = x(a-x) (107, 250), F(x,a) = g(x, c(x,a), a) (239), F(x,a) = x(a-x)/2 (307). L21 F is defined in Theorem 1.2. No new undefined symbol in changed text.")
row("REF-registry", "References sections and registry keys", "course/modules/M/M2/L19..L24.html references sections; references/references.json", "PASS",
    R7 + "references sections byte-identical since 7aa909e; " + S + "verify_refs.out: 0 problems).")
row("NOTATION-registry", "Symbols against notation/notation.json", "notation/notation.json vs L19..L24", "PASS",
    R7 + "notation/notation.json unchanged since 7aa909e; no new reserved symbol introduced by the delta: G, F, V, J, I, g, c used in L22 are not registry symbols).")

frag = {
 "unit": "M2", "slice": "d", "round": 8,
 "verifier": "Haiku 5.5 independent verifier, slice d (L19-L24), round 8",
 "pin": "ce7b382", "base": "7aa909e",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB8-M2-d",
 "scratch": "/Users/billyribeiro/.fanout/wt/verifyB8-M2-d/ledgers/M2/scripts/M2-d-r8",
 "verified_at": "2026-10-28T23:00:00+00:00",
 "verdict": "FAIL" if any(r["status"] != "PASS" for r in P) else "PASS",
 "rows": P,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Delta 7aa909e..ce7b382 for slice d: L19.html line 372 (R2 solution: escape only plus omega definition wording), L20.html line 199 (escape only), L20.html line 330 (R2 solution, new necessity sentence), L22.html lines 88, 456, 465 (Remark 1.4 and quiz wording; F -> G and V'(1) wording), L23.html line 222 (lab interpretation), cards.json (M2-c290, c344, c356 removed; c310, c330, c335 changed). Twins lab-M2-L19..L24 unchanged in this delta.",
  "Mutants: none required; lab twins are demonstrations (VERIFIER_RULES ruling). No grader in this slice.",
  "Not checked: the M2 project slice (not in this slice); rendered visual layout beyond page_smoke; the L19 R3 solution and Remark 3.2 were carried as byte-identical (their diff hunks are absent); the cards generator source was not located (cards.json is edited directly in this repo at this pin, so the M2-c299 fix must go to whatever source the card pipeline reads).",
  "Money note from round 7 stands: L23 keeps P', P'' and Taylor terms exact (Fraction) and prints floats; the page (E3, Section 4) says so; the plan Q12 tolerance wording is the architect's call."
 ],
 "summary": ""
}
frag["summary"] = "Slice d (L19-L24), round 8 at ce7b382: verdict %s. %d rows; %d non-PASS: L20-problems-res2 (necessity sentence on the half-open square, low), STRUCT-scope-words (same sentence, low), L19-math-remark-R2-R3 (omega defined as max entry of H, low), CARDS-c299-uses-nowhere (absolute 'uses it nowhere' contradicted by L20 lines 214/330/420, low). Round-7 FAILs L22-math-remark14, STRUCT-define-before-use and CARDS-slice re-verified PASS." % (frag["verdict"], len(P), sum(1 for r in P if r["status"] != "PASS"))
json.dump(frag, open("ledgers/M2/M2-d.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(P), "non-PASS", [r["id"] for r in P if r["status"] != "PASS"])
