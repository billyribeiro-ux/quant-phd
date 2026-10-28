import json
from datetime import datetime, UTC

S = "ledgers/FC2/scripts/FC2-c-r1/"
L7 = "course/modules/FC/FC2/L07.html"
L8 = "course/modules/FC/FC2/L08.html"
T7 = "tests/labs/FC2/lab-FC2-L07-1.py"
T8 = "tests/labs/FC2/lab-FC2-L08-1.py"
CARDS = "course/modules/FC/FC2/cards.json"

rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---------- commands and labs (PASS) ----------
row("C2c-cmd-check-dag", "2.8-dag", "tools/check_dag.py (unit FC2)", "PASS",
    "Run on pin 55b5634: `.venv/bin/python tools/check_dag.py --unit FC2` -> 'check_dag FC2: PASS' (exit 0). "
    "Links used on L07/L08 resolve to defined concepts; FC2-owned concepts are defined in L05-L08.")
row("C2c-cmd-check-pages", "2.9-structure", "tools/check_pages.py (unit FC2)", "PASS",
    "Run: `.venv/bin/python tools/check_pages.py --unit FC2` -> 'check_pages FC2: PASS' (exit 0). Covers hours, "
    "section template, cards, grades and registry keys for the whole unit.")
row("C2c-cmd-check-projects", "2.9-structure", "tools/check_projects.py (unit FC2)", "PASS",
    "Run: `.venv/bin/python tools/check_projects.py --unit FC2` -> 'check_projects FC2: PASS' (exit 0). "
    "Project page is outside this slice; the command was run as the unit gate.")
row("C2c-cmd-run-labs", "2.5-labs", "tools/run_labs.py --unit FC2", "PASS",
    "Run: `.venv/bin/python tools/run_labs.py --unit FC2` -> 'run_labs FC2: PASS (11/11)' (exit 0). "
    "Includes lab-FC2-L07-1 and lab-FC2-L08-1.")
row("C2c-lab-twin-identity", "2.5-labs", f"{L7} lines 152-252; {L8} lines 126-246 vs {T7}, {T8}", "PASS",
    "Extracted the data-run block with " + S + "extract_embedded_lab.py and diffed against the twins: the only "
    "difference is the final newline (the page block has none). Embedded code equals the twin.")
row("C2c-lab-isolated-run", "2.5-labs", f"{T7}, {T8}", "PASS",
    "`.venv/bin/python -I -W error tests/labs/FC2/lab-FC2-L07-1.py` exit 0, no stderr; same for L08. "
    "stdout compared with the embedded expected blocks (output saved in " + S + "out-L07.txt, out-L08.txt): "
    "identical except the trailing newline of the expected block.")
row("C2c-lab-static", "2.5-labs", f"{T7}, {T8}", "PASS",
    "`ruff check` on both twins: 'All checks passed!'; `ruff format --check`: '2 files already formatted'; "
    "`mypy --no-incremental` on both: 'Success: no issues found in 2 source files'.")
row("C2c-cmd-page-smoke", "2.5-labs", f"{L7}, {L8} (page_smoke --unit FC2 --pages L07 L08 --skip-sweep)", "PASS",
    "Chromium run: 'page_smoke modules/FC/FC2/L07.html: PASS', 'page_smoke modules/FC/FC2/L08.html: PASS', "
    "'page_smoke FC2: PASS'. Lab runtime 0.0 s each after boot 1.2 s (under 10 s).")
row("C2c-cmd-refs-offline", "2.1-citations", "tools/verify_refs.py --offline; " + L7 + " line 439; " + L8 + " line 439",
    "PASS",
    "`.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems'. Neither "
    "lesson cites a registry key (L07 line 439 and L08 line 439 each say so; both footers say so). The live "
    "`--unit` run is not applicable to this slice (no keys cited); the `--unit` flag requires a live run and was not run.")
row("C2c-cites-attribution", "2.1-citations", f"{T7} lines 154-155 (docstring 'Cox-Ross-Rubinstein style')", "PASS",
    "Name only, no key and no bibliographic data on the page. Registry record read in references/references.json "
    "entry cox1979option: authors Cox, Ross, Rubinstein; title 'Option pricing: A simplified approach'; 1979; "
    "JFE vol 7 issue 3; verified_by crossref. The label matches the registry; no locator is quoted.")

# ---------- L07 mathematics ----------
row("C2c-L07-lemma-1.1", "2.4-math", f"{L7} lines 62-68", "PASS",
    "Substitution t = sqrt(2) s: phi(t) dt = e^{-s^2}/sqrt(pi) ds, limit x/sqrt(2); integral over (-inf,0] = sqrt(pi)/2. "
    "Re-derived by hand. Numeric check: " + S + "check_L07_L08_numbers.py gives max|Phi(x)+Phi(-x)-1| = 0.0 at "
    "0, 0.35, 1.7, 3 (Lemma 1.2 consequence).")
row("C2c-L07-lemma-1.2", "2.4-math", f"{L7} lines 70-76", "PASS",
    "phi even, total integral 1; substitution t -> -t gives Phi(-x) = 1 - Phi(x). Re-derived; numeric check as above.")
row("C2c-L07-prop-1.4", "2.4-math", f"{L7} lines 89-102", "PASS",
    "C - S + K e^{-rτ} = -S(1-Phi(d1)) + K e^{-rτ}(1-Phi(d2)) = K e^{-rτ}Phi(-d2) - S Phi(-d1). Re-derived. The lab "
    "checks the same identity numerically (parity True, tolerance 1e-9, output line 15). Hypotheses A1-A5 and A7 match "
    "the parity step (L05 Theorem 1.2 uses A1-A4 plus the no-arbitrage step) and the formula.")
row("C2c-L07-prop-1.5", "2.4-math", f"{L7} lines 104-110", "PASS",
    "d1 = [ln(S/K)+rτ]/(σ√τ) + σ√τ/2 (algebra checked: both sides equal [ln(S/K)+(r+σ²/2)τ]/(σ√τ)); C uses only "
    "ln(S/K), rτ, σ√τ and Ke^{-rτ}. The proof text says 'divide numerator and denominator by √τ', which does not "
    "produce the displayed equation; the displayed equation itself is correct. Statement T is supported.")
row("C2c-L07-def-2.1-A6", "2.4-math", f"{L7} line 116", "FAIL",
    "Definition 2.1 says 'A6 holds at each node by Lemma 2.2' without a condition. Lemma 2.2 (line 121) is an "
    "equivalence that needs r > 0 and h < σ²/r²; A6 at each node therefore holds only when that condition holds, "
    "and the definition does not say so.",
    "Replace with 'A6 holds at each node whenever r > 0 and h < σ²/r² (Lemma 2.2)', or move the sentence after Theorem 2.3.")
row("C2c-L07-lemma-2.2", "2.4-math", f"{L7} lines 119-125", "PASS",
    "Re-derived: d<R iff -σ√h < rh (always for r>0); R<u iff rh < σ√h iff h < σ²/r². Numeric check "
    "(" + S + "thm23_check.py): for n=1,2,5,10 with r=0.05, σ=0.2, τ=1, 0<d<R<u is True and h<σ²/r² is True.")
row("C2c-L07-thm-2.3-formula", "2.4-math", f"{L7} lines 127-136", "PASS",
    "Closed binomial sum (Theorem 2.3) recomputed for n=1,2,5,20,100 (" + S + "thm23_check.py): equals backward induction "
    "to 2e-14. Discount factor (R^{(n)})^{-n} = e^{-rτ} since nh = τ. Proof cites Theorem 3.3 of L06, whose "
    "statement (L06 lines 140-144: A1,A2,A3,A5,A6,A6', V(0,0) = R_f^{-N} sum binom q^k(1-q)^{N-k} f(...)) matches.")
row("C2c-L07-thm-2.3-hypotheses", "2.4-math", f"{L7} lines 127-132", "FAIL",
    "Theorem 2.3 states 'when h < σ²/r²' but omits r > 0. The proof uses Lemma 2.2, which requires r > 0. At r = 0 the "
    "stated condition divides by zero: " + S + "thm23_check.py prints 'r=0 -> ZeroDivisionError in h < sigma^2/r^2'. "
    "(For r = 0 the tree is still valid, but the theorem as written does not say so.)",
    "Add 'r > 0' to the hypotheses of Theorem 2.3 (Lemma 2.2 needs it), and say what happens at r = 0.")
row("C2c-L07-sec4-A7-sentence", "2.4-math", f"{L7} lines 55, 127-138", "PASS",
    "Theorem 2.3 lists A7 among its hypotheses, and line 138 says the theorem 'says nothing about A7'. The two are "
    "compatible: A7 is a hypothesis the proof does not use and the conclusion does not assert it. Checked, no conflict.")
row("C2c-L07-lab1-prose-147", "2.2-numbers/2.5-labs", f"{L7} line 147", "FAIL",
    "Line 147 says: 'A column of errors is therefore not exactly the difference of the two printed price columns.' In the "
    "nine printed rows the error column equals the printed price difference exactly: 1216-1045=171 (err 171), "
    "954-1045=-91 (-91), 1081-1045=36 (36), 1025-1045=-20 (-20), 1052-1045=7 (7), 1041-1045=-4 (-4), 1043-1045=-2 (-2), "
    "1044-1045=-1 (-1), 1045-1045=0 (0). The sentence is an overstated claim about what Lab 1 prints. "
    "(The lab docstring line 163 correctly says 'can differ by one cent'.)",
    "Say 'can differ by one cent in general (rounding of the unrounded difference); in the nine printed rows it does not'.")
row("C2c-L07-lab1-sign-400", "2.2-numbers/2.5-labs", f"{L7} lines 151, 282, 324, 328; card FC2-c111", "FAIL",
    "The 400-step error prints as 0 (lab output line 265). The unrounded error is -0.0049977 currency units = -0.4998 cents "
    "(recomputed: -0.004997731). Line 282 says 'The sign pattern is in the printed values', which is false for the 400-step row, "
    "whose printed value is 0. E2 (line 328) counts six negative errors, one of them 400 steps, from the unrounded value only. "
    "Card FC2-c111 repeats the printed-values claim.",
    "Say the sign at 400 steps is visible only in the unrounded value (-0.4998 cents), not in the printed table; "
    "remove 'in the printed values' from line 282 and card FC2-c111, and state E2's basis (unrounded).")
row("C2c-L07-misconception-same-rtau", "2.4-math/2.6-scope", f"{L7} line 284", "FAIL",
    "'Two inputs with the same rτ and σ√τ give the same price, whatever the expected return.' Prop 1.5 needs S and K "
    "to be the same as well. Counterexample (" + S + "check_L07_L08_numbers.py): S=100, K=100, r=0.05, τ=1, σ=0.2 gives 10.450584; "
    "S=110 with the same rτ and σ√τ gives 17.662954.",
    "Write 'with the same S, K, rτ and σ√τ'.")
row("C2c-L07-line275-rule", "2.9-prose/cross-ref", f"{L7} line 275", "FAIL",
    "'An American call ... its tree value needs the rule of Lesson 4, which this lesson does not state.' Lesson 4 gives no "
    "tree rule. It gives the exercise payment h(S_t) (L04 Definition 2.1, line 91) and the bounds V_A >= h and "
    "V_A(0) >= V_E(0) (Propositions 2.2 and 2.3). The reference points to a rule that Lesson 4 does not contain.",
    "Replace 'the rule of Lesson 4' with 'the exercise payment of Lesson 4 (Definition 2.1) inside a backward recursion', "
    "or state that the recursion is not taught in FC2.")
row("C2c-L07-problem-set", "2.4-math/2.2-numbers", f"{L7} lines 293-348", "PASS",
    "M1 d1=0.35, d2=0.15 (recomputed). M2 P=5.573526, 557 cents (recomputed 5.573526022). M3 u=1.105171, d=0.904837, "
    "R=1.012578, q=0.537808, h=0.25<16 (recomputed). P1-P3 re-derived. E1 unrounded -0.0049977 (recomputed -0.00499773). "
    "E3 V1=12.1623, 1216 cents (recomputed 12.162285). R1 correct: 9 step counts cannot decide a limit. "
    "R2: τ=4, σ=0.1, r=0.0125 gives σ√τ=0.2, rτ=0.05 and the same price 10.450584 (recomputed 10.450583572); "
    "R3 makes no market claim.")
row("C2c-L07-lab1-hypothesis-and-output", "2.5-labs", f"{L7} lines 151-268", "PASS",
    "Stated expected result matches the run: error column positive at 1,5,25; negative at 2,10,50,100,200; 0 at 400. "
    "Closed form 1045 cents (10.450584). Four Phi points checked (code lines 242-244). "
    "Interpretation line 268: five sign changes across the nine printed values (+,-,+,-,+,-,-,-,0) and |error| strictly "
    "decreasing (171,91,36,20,7,4,2,1,0) are both true of the printed table.")
row("C2c-L07-key-results", "2.3-grades", f"{L7} lines 350-364", "PASS",
    "Six T rows match Lemma 1.1, 1.2, Proposition 1.4, 1.5, Lemma 2.2 and Theorem 2.3 (each with proof on the page). "
    "Line 363 states the lab comparison is not graded.")
row("C2c-L07-quiz", "2.7-cards/2.2-numbers", f"{L7} lines 366-435", "PASS",
    "Keys verified: Q1 r; Q2 d2=0.15; Q3 557 cents (recomputed 557.35); Q4 1-Phi(x); Q5 u=1.2214 (1.221403); Q6 "
    "h<σ²/r²; Q7 1216 cents; Q8 0 cents (the explanation uses the unprinted -0.4998, which is recomputed); Q9 "
    "convergence is not established; Q10 1045 cents.")
row("C2c-L07-lab-card-content", "2.7-cards", f"{CARDS} FC2-c099..c108, c112..c116, c118", "PASS",
    "Each card checked against its lesson paragraph: c099 (A7 text line 59), c100-c108 (Lemma 1.1-2.3, Prop 1.4-1.5, "
    "Def 2.1-3.1), c112-c113 (Prop 1.5, Prop 1.4), c114-c116 (M1, M3, E3), c118 (M2). Numbers in cards appear in the lesson. "
    "Duplicates and grades are reported in separate rows.")

# ---------- L08 mathematics ----------
row("C2c-L08-lemma-2.1", "2.4-math", f"{L8} lines 67-84", "PASS",
    "d1-d2 derivative difference = √τ (both partials recomputed); S φ(d1) = K e^{-rτ} φ(d2) by log identity with "
    "d1²-d2² = 2a; dC/dσ = S φ(d1) √τ > 0. Numeric vega ATM: 37.524035 (the page's 37.52 is correct).")
row("C2c-L08-lemma-2.2", "2.4-math", f"{L8} lines 86-93", "PASS",
    "Three cases re-derived: a>0 gives S-Ke^{-rτ}=L; a<0 gives 0=L; a=0 gives S/2-Ke^{-rτ}/2=0=L. "
    "Numeric: C(1e-6)=0.0 at K=120 (= L) and C(10)=99.99993875 (-> S).")
row("C2c-L08-thm-2.3", "2.4-math", f"{L8} lines 95-104", "PASS",
    "Existence by IVT on the continuous C (C differentiable by Lemma 2.1) with limits from Lemma 2.2; uniqueness by strict "
    "monotonicity; non-existence outside (L,S) from monotonicity and the limits. Re-derived. The proof says 'strict "
    "monotonicity' without naming Lemma 2.1; it is on the page.")
row("C2c-L08-prop-3.2-count", "2.4-math/2.2-numbers", f"{L8} lines 113-116; M3 lines 298-301", "PASS",
    "For W > τ the first k with W/2^k <= τ is ceil(log2(W/τ)). With W = 10 - 1e-6 and τ = 1e-10: log2(W/τ) = 36.54, "
    "k = 37. At k = 36 the width is 1.455e-10 > τ (page: 1.46e-10, correct to 3 s.f.). Error bound τ/2: recomputed "
    "from the lab output, errors 1.74e-11 <= 5e-11.")
row("C2c-L08-prop-3.2-edge", "2.4-math", f"{L8} lines 107-110 (Definition 3.1) and lines 113-116 (Proposition 3.2)", "FAIL",
    "Definition 3.1 says 'Repeat: ... Stop when σhi - σlo <= τ_tol', which reads as at least one halving. Proposition 3.2 "
    "says the procedure 'stops after the smallest k with W/2^k <= τ_tol', which is k = 0 when W <= τ_tol. The lab "
    "code (" + T8 + " lines 207-213, a while-loop test before each step) does zero halvings in that case. Witness: "
    "bracket [0.2, 0.2+1e-11], τ_tol = 1e-10: the Definition as written takes one step, the Proposition says k = 0.",
    "Rewrite Definition 3.1 as 'While σhi - σlo > τ_tol: ...' so that it matches Proposition 3.2 and the lab.")
row("C2c-L08-lab-numbers", "2.2-numbers/2.5-labs", f"{L8} lines 247-259 (output) vs run", "PASS",
    "Rerun reproduces every row: prices 2391, 2459, 2898, 680, 1045, 1802, 46, 325, 1081 cents; sigma_recovered "
    "0.10000000/0.20000000/0.40000000; halvings 37; abs_error 1.73e-11, 5.73e-12, 1.74e-11; largest 1.74e-11 (<1e-10); "
    "lower bound 4.8771 (4.877057549928594). Four rejections match. Lab asserts pass (exit 0).")
row("C2c-L08-lab-expected-bracket-claim", "2.5-labs", f"{L8} line 121 and {T8} lines 205-213", "FAIL",
    "Line 121 says the code 'raises a named error when the price is too close to the lower bound for the bracket to contain "
    "the root'. The code's second check (line 203-204) raises the same message when C(10) < price, i.e. for prices close to "
    "the spot. Probe " + S + "near_spot_probe.py: K=80, price 99.999975 (strictly between L=23.9016 and S=100) gives "
    "'ValueError: price too close to the lower bound: the bisection bracket has no sign change', although C(10)=99.9999500 is "
    "below it, so the root lies above 10 and exists by Theorem 2.3. The same happens for K=100 (price 99.99997204) and K=120 "
    "(price 99.99996938). The error names the wrong condition for these valid prices; the lab's 'accepted' set is "
    "correctly limited but the message is wrong.",
    "Either widen the bracket (HIGH_SIGMA) with a check that C(HIGH) >= price, or change the message to say the "
    "volatility bracket [1e-6, 10] does not contain the root (both lower and upper cases), and say so on line 121.")
row("C2c-L08-docstring-locator", "2.1-citations/2.9-prose", f"{T8} line 130", "FAIL",
    "Docstring: 'strictly increasing in sigma (Lesson 8, Theorem 2.2)'. L08 has no Theorem 2.2 (grep: only Theorem 2.3 "
    "appears). The monotonicity result is Lemma 2.1 (vega > 0). Learner-facing locator is wrong.",
    "Change to 'Lesson 8, Lemma 2.1'.")
row("C2c-L08-canon-defined-only", "2.6-scope", f"{L8} line 270", "FAIL",
    "'The implied volatility is defined only under A7, which fixes one volatility for every strike.' Definition 1.1 defines "
    "it for any observed price relative to a stated price function; the page itself says (line 272) that other price "
    "functions exist. 'Defined only under A7' is an overstated scope claim.",
    "Say: 'In this lesson the implied volatility is defined relative to the A7 formula C(σ)'.")
row("C2c-L08-R2-rounding-basis", "2.2-numbers", f"{L8} lines 337-339", "PASS",
    "0.01/37.52 = 0.00026652, which gives the displayed 0.000267 from the displayed vega. From the unrounded vega 37.524035 "
    "the quotient is 0.00026650 (6 d.p. 0.000266). The page's quotient is from displayed digits and the basis is stated "
    "(it writes 0.01/37.52). Both give 'about 0.027 volatility points'. Accepted with this note.")
row("C2c-L08-E-numbers", "2.2-numbers", f"{L8} lines 321-329", "PASS",
    "E1: largest error 1.74e-11 in the σ=0.40 rows; 1.74/10 = 0.174 of tolerance, shown as 0.17. E2: 120e^{-0.05} = 114.15; "
    "L = 0; price at σ=0.10 is 46.2497 cents (printed 46). E3: implied vol 0.10207696 after 37 halvings (page 0.102077, "
    "correct); bracket sign change: C(1e-6)=0.0 < 0.5 < C(10)=99.99994; prices at strike 120 rejected only at <=0 or >=100.")
row("C2c-L08-E2-every-positive-vol", "2.6-scope", f"{L8} line 325", "PASS",
    "'The call is then worth something positive for every positive volatility.' Follows from Lemma 2.1 (strictly "
    "increasing) and Lemma 2.2 (limit L = 0 as σ -> 0+); the solution does not cite them, but both are on the page. Accepted.")
row("C2c-L08-R1-R3-M1-M2-P-quiz", "2.4-math/2.7-cards", f"{L8} lines 290-343, 361-435", "PASS",
    "M1 L=4.877058 (recomputed). M2 price 4.90 is the only one of {4.00, 4.90, 100} strictly in (L,S). P1 identity "
    "re-derived; P2 limit; P3 invariant re-derived from C strictly increasing. R1-R3 correct. Quiz keys verified: "
    "Q1 exactly one; Q2 L=4.8771; Q3 4.90; Q4 37; Q5 positive; Q6 vega 37.52 (37.5240, tolerance 0.01); "
    "Q7 inversion tests code; Q8 L=0 at K=120; Q9 correct option; Q10 yes.")
row("C2c-L08-key-results", "2.3-grades", f"{L8} lines 347-359", "PASS",
    "Four T rows match Lemma 2.1, Lemma 2.2, Theorem 2.3, Proposition 3.2. The inversion table is not graded (line 358).")
row("C2c-L08-cards-content", "2.7-cards", f"{CARDS} FC2-c119..c131", "PASS",
    "Each card checked against its lesson text. c120-c123 match Lemma 2.1, 2.2, Theorem 2.3, Proposition 3.2; c125/c126/c127/c131 "
    "numbers appear in M1-M3, E2 and the lab output; c119, c124, c128, c130 match Definition 1.1, Definition 3.1, Section 5, Section 1.")

# ---------- cards (FAIL) ----------
row("C2c-cards-grades-lab", "2.3-grades/2.7-cards", f"{CARDS} FC2-c109, FC2-c110, FC2-c111, FC2-c117", "FAIL",
    "Cards grade lab-read values T: c109 (closed form 1045 cents, 'basis Lab 1'), c110 (1216 cents; 400-step error), "
    "c111 (sign pattern), c117 (smallest error). The lesson says the lab comparison is not graded (" + L7 + " line 363). "
    "The lab is a model computation with no proof on the page; results read off it are grade C with the lab as basis "
    "(BRIEF rule 9). c111 also answers 'No' to whether the binomial price approaches from one side, a claim about the "
    "limit that nine step counts cannot establish (Problem R1).",
    "Grade c109, c110, c111, c117 as C with basis 'Lab 1 (nine step counts)'; rewrite c111's answer as 'the printed nine "
    "values have both signs; this lesson does not decide the limit'.")
row("C2c-cards-duplicates", "2.7-cards", f"{CARDS} FC2-c110/c116/c117; FC2-c104/c112; FC2-c122/c129; FC2-c127/c129", "FAIL",
    "Duplicate facts: c110 and c116 both state the one-step tree price 1216 cents; c110 and c117 both state the 400-step "
    "error -0.0049977; c104 and c112 both state that C depends only on S, K, rτ, σ√τ; c122 and c129 both state that an "
    "implied volatility exists only for L < C* < S; c127 and c129 both state that 4.00 and 100.00 at strike 100 have no "
    "volatility. BUILDER_RULES card rule: one fact per card.",
    "Merge or remove the duplicates (keep c116 and c117 for different facts, keep c122 for the existence theorem, keep c127 "
    "for the worked choice, keep c104 and drop the restatement in c112).")
row("C2c-cards-L08-grades-ok", "2.3-grades", f"{CARDS} FC2-c120..c131", "PASS",
    "Grades T on lemma, theorem and proposition cards match the lesson; the lab inversion is not graded and no card grades it. "
    "c125 (T, Problem M3 exact) and c131 (T, Problem E2 exact) are derivations on the page.")

# ---------- structure, DAG, notation, prose ----------
row("C2c-dag-links", "2.8-dag", f"{L7} line 37, 98; {L8} line 37", "PASS",
    "Concept links used on the slice: binomial-option-pricing, risk-neutral-probability (L06), put-call-parity, "
    "option-payoff, option-arbitrage-bounds, american-option (FC2 L04-L05), discount-factor, continuous-compounding, "
    "normal-distribution, limit, derivative (M1, M2, M4 in the closure). Plain prose for lognormal, bisection and "
    "no-arbitrage (no link). check_dag PASS.")
row("C2c-hours", "2.9-hours", "index.html data-hours-lessons=60; L07 data-hours=8; L08 data-hours=6", "PASS",
    "Lesson hours L01..L08 = 6+8+9+7+8+8+8+6 = 60 = hub data-hours-lessons; project 30; total 90. Plan §2 agrees. "
    "Pace not assessed (architect ruling).")
row("C2c-notation", "2.4-notation", f"{L7}, {L8}, {T7}, {T8} (notation/notation.json)", "PASS",
    "Registered symbols: T (no use in slice; L07 line 55 says 'not T'); Φ used as the standard normal CDF, registered "
    "meaning (M4). R_f, R^*, Q, gamma not used. Local symbols: φ (density), q, u, d, h, R^{(n)}, V_n, e_n, C, P, L, W, "
    "τ_tol (tolerance; the page says τ is kept for maturity). None is a registered program symbol with another meaning.")
row("C2c-prose-banned", "2.9-prose", f"{L7}, {L8}", "PASS",
    "Scanned for roughly/typically/historically/ellipsis/'about'. 'about' occurrences are on computed values with the basis "
    "shown (L07 line 328 about -0.5 from -0.4998; L08 line 321 about 0.17 from 1.74/10; L08 line 337 about 37.52 from "
    "37.524). No process words (build, builder, verifier, round, request) in learner text or cards.")
row("C2c-scope-words", "2.6-scope", f"{L7}, {L8}", "PASS",
    "'every'/'all'/'only' occurrences checked: L07 line 59 (model assumption), L07 line 274 (model assumption), "
    "L07 line 268-274 (nine values), L08 line 121 (lab bracket), L08 line 125 (37 in every row, verified), "
    "L08 line 280 misconception. The scope failures are reported above (L07 line 284, L08 line 270).")
row("C2c-mutants-not-applicable", "2.6-mutants", "ledgers/FC2/mutants/ (project grader only)", "PASS",
    "Architect ruling: lab twins are demonstrations; mutation testing applies to project graders only. No mutant is run "
    "for this slice. Not a row of the slice's evidence.")

fragment = {
    "unit": "FC2",
    "slice": "FC2-c",
    "round": 1,
    "verifier": "Haiku independent verifier, round 1, slice FC2-c (L07-L08 and their lab twins). Did not build FC2 and "
                "shares no context with its builders.",
    "pin": "55b5634",
    "base": "none",
    "checkout": "/tmp/verifyC1-FC2-c (detached at 55b5634; .venv symlinked)",
    "scratch": "/tmp/FC2-v/c",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Pin: the task names 55b5634; the brief's example pin b4590f6 was not used.",
        "Slice has no project grader, so no mutants and no alternative implementations were run (architect ruling on lab twins).",
        "verify_refs --unit FC2 (live) was not run: it needs network and the slice cites no key; --offline run for integrity only.",
        "Not checked: the other lessons L01-L06 and the project (other slices), and the page_smoke sweep (--skip-sweep; the pages have no figures).",
        "Hours: pace not assessed; only lesson-vs-hub arithmetic.",
        "The two lab twins run under python -I -W error with exit 0; the embedded expected blocks equal the observed output.",
    ],
    "summary": {},
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
fragment["summary"] = {"rows": len(rows), "pass": n_pass, "fail": n_fail, "unverifiable": 0,
                       "fail_ids": [r["id"] for r in rows if r["status"] != "PASS"]}
with open("/tmp/verifyC1-FC2-c/ledgers/FC2/FC2-c.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "pass", n_pass, "fail", n_fail)
