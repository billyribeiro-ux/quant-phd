"""Writes the round 2 fragment for FC2 slice c (L07-L08 and their lab twins). Data only; no judgement is computed here."""
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
P = "PASS"
F = "FAIL"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)


# ---- commands and labs
row("C2c-cmd-check-dag", "2.8-dag", "tools/check_dag.py (unit FC2)", P,
    "Run on e22feb3: `.venv/bin/python tools/check_dag.py --unit FC2` -> 'check_dag FC2: PASS' (exit 0).")
row("C2c-cmd-check-pages", "2.9-structure", "tools/check_pages.py (unit FC2)", P,
    "Run: `.venv/bin/python tools/check_pages.py --unit FC2` -> 'check_pages FC2: PASS' (exit 0).")
row("C2c-cmd-check-projects", "2.9-structure", "tools/check_projects.py (unit FC2)", P,
    "Run: `.venv/bin/python tools/check_projects.py --unit FC2` -> 'check_projects FC2: PASS' (exit 0). The project is outside this slice.")
row("C2c-cmd-run-labs", "2.5-labs", "tools/run_labs.py --unit FC2", P,
    "Run: `.venv/bin/python tools/run_labs.py --unit FC2` -> 'run_labs FC2: PASS (11/11)' (exit 0).")
row("C2c-lab-twin-identity", "2.5-labs", "course/modules/FC/FC2/L07.html and L08.html data-run blocks vs tests/labs/FC2/lab-FC2-L07-1.py, lab-FC2-L08-1.py", P,
    "ledgers/FC2/scripts/FC2-c-r2/embed_identity.py: embedded code equals the twin for L07 and L08 (True, True). The embedded expected blocks equal a fresh `python -I -W error` stdout exactly (True, True).")
row("C2c-lab-isolated-run", "2.5-labs", "tests/labs/FC2/lab-FC2-L07-1.py, lab-FC2-L08-1.py", P,
    "`.venv/bin/python -I -W error <twin>` exit 0 for both, no stderr. Outputs saved to /tmp/fc2c_l07.out and /tmp/fc2c_l08.out; page_smoke lab runtime 0.0 s each.")
row("C2c-lab-static", "2.5-labs", "tests/labs/FC2/lab-FC2-L07-1.py, lab-FC2-L08-1.py", P,
    "`ruff check`: 'All checks passed!'; `ruff format --check`: '2 files already formatted'; `mypy --no-incremental` on both: 'Success: no issues found in 2 source files'.")
row("C2c-cmd-page-smoke", "2.5-labs", "page_smoke --unit FC2 --pages L07 L08 --skip-sweep", P,
    "Run: 'page_smoke modules/FC/FC2/L07.html: PASS', 'page_smoke modules/FC/FC2/L08.html: PASS', 'page_smoke FC2: PASS' (log /tmp/fc2c_smoke.log). The sweep was skipped, as in round 1.")
row("C2c-cmd-refs-offline", "2.1-citations", "tools/verify_refs.py --offline; --unit FC2 (live); L07/L08 contain no data-cite", P,
    "`verify_refs.py --offline`: 'offline integrity: 560 entries, 0 problems'. Live `verify_refs.py --unit FC2`: '3 of 560 entries, 0 problems'. grep: 0 data-cite in L07.html and L08.html.")
row("C2c-cites-attribution", "2.1-citations", "tests/labs/FC2/lab-FC2-L07-1.py lines 154-155 (docstring 'Cox-Ross-Rubinstein style')", P,
    "Name only, no key and no bibliographic data on the page. Registry record references/references.json key cox1979option: authors Cox, Ross, Rubinstein; 1979; Journal of Financial Economics 7(3). The lesson makes no claim about the paper's content.")

# ---- L07 mathematics
row("C2c-L07-lemma-1.1", "2.4-math", "course/modules/FC/FC2/L07.html lines 63-68", P,
    "Substitution t = sqrt(2) s re-derived by hand; integral over (-inf, 0] = sqrt(pi)/2; the lab's norm_cdf (twin line 189) uses the same identity.")
row("C2c-L07-lemma-1.2", "2.4-math", "course/modules/FC/FC2/L07.html lines 70-76", P,
    "Re-derived (t -> -t and phi even). Lab check of Phi(x)+Phi(-x)=1 at 0, 0.35, 1.7, 3.0 prints True (twin lines 242-247).")
row("C2c-L07-prop-1.4", "2.4-math", "course/modules/FC/FC2/L07.html lines 89-102", P,
    "C - S + K e^{-r tau} = -S(1-Phi(d1)) + K e^{-r tau}(1-Phi(d2)) = K e^{-r tau}Phi(-d2) - S Phi(-d1) re-derived. Hypotheses A1-A5 and A7 match L05 (A1-A5 of Lesson 4) and Definition 1.3. Parity lab check prints True.")
row("C2c-L07-prop-1.5", "2.4-math", "course/modules/FC/FC2/L07.html lines 104-110", P,
    "d1 = (ln(S/K)+r tau)/(sigma sqrt tau) + sigma sqrt tau/2 re-derived. Numeric (ledgers/FC2/scripts/FC2-c-r2/recompute.py): bs_call(100,100,0.0125,4,0.1) = 10.450583572 = bs_call(100,100,0.05,1,0.2).")
row("C2c-L07-def-2.1-A6", "2.4-math", "course/modules/FC/FC2/L07.html line 116", P,
    "Now reads 'A6 holds at each node whenever r > 0 and h < sigma^2/r^2 (Lemma 2.2)'. Lemma 2.2 (line 121) states exactly those hypotheses.")
row("C2c-L07-lemma-2.2", "2.4-math", "course/modules/FC/FC2/L07.html lines 119-125 (proof line 124)", F,
    "Proof line 124: 'Dividing by sqrt(h) > 0 gives r sqrt(h) < sigma, that is h < sigma^2/r^2.' The step from r sqrt(h) < sigma to h < sigma^2/r^2 is squaring two positive sides, which needs r > 0; the proof does not say so. Grid check (ledgers/FC2/scripts/FC2-c-r2/thm23_lemma22.py): 0 mismatches for r>0 apart from one float-boundary case at h = sigma^2/r^2 (0.04 vs 0.04000000000000001), so the statement is correct.",
    "In the proof, write 'Both sides are positive because r > 0, so squaring gives r^2 h < sigma^2, that is h < sigma^2/r^2.'")
row("C2c-L07-thm-2.3-formula", "2.4-math", "course/modules/FC/FC2/L07.html lines 127-136", P,
    "ledgers/FC2/scripts/FC2-c-r2/thm23_lemma22.py: closed binomial sum vs backward induction, n in {1,2,5,20,100} and three parameter sets: max abs difference 1.05e-13. The discount identity (R)^{-n} = e^{-r tau} follows from n h = tau.")
row("C2c-L07-thm-2.3-hypotheses", "2.4-math", "course/modules/FC/FC2/L07.html lines 127-132 and 138", P,
    "Theorem 2.3 now states 'with r > 0 and h < sigma^2/r^2' (line 129); line 138 says the theorem is not stated for r = 0. The round 1 gap is closed.")
row("C2c-L07-sec4-A7-sentence", "2.4-math", "course/modules/FC/FC2/L07.html lines 55, 129, 138", P,
    "A7 is listed among Theorem 2.3's hypotheses; the proof (line 135) uses only Lemma 2.2 and Theorem 3.3 of Lesson 6, whose hypotheses are A1, A2, A3, A5, A6, A6' (L06 line 141). 'Says nothing about A7' is consistent with that.")
row("C2c-L07-lab1-prose-147", "2.2-numbers", "course/modules/FC/FC2/L07.html line 147", P,
    "Now: the error column 'can differ by one cent from the difference of the two printed price columns'; 'in the nine printed rows it does not differ'. Printed rows: tree - closed equals error in all nine rows (lab output lines 257-265). Witness for 'can': tree 10.004 and closed 10.006 give cents 1000 and 1001 (difference -1) while the error -0.002 rounds to 0.")
row("C2c-L07-lab1-sign-400", "2.2-numbers", "course/modules/FC/FC2/L07.html lines 151, 282; lab output line 265", P,
    "Unrounded error at 400 steps (recompute.py): -0.499773 cents = -0.00499773 currency units, printed 0. Text says -0.4998 cents (line 282) and -0.0049977 currency units (line 324): both consistent.")
row("C2c-L07-misconception-same-rtau", "2.4-math", "course/modules/FC/FC2/L07.html line 284", P,
    "Now 'Two inputs with the same S, K, r tau and sigma sqrt(tau) give the same price': Proposition 1.5 needs ln(S/K) to agree as well, and the sentence includes S and K.")
row("C2c-L07-line275-rule", "2.4-math", "course/modules/FC/FC2/L07.html line 275", P,
    "'exercise payment of Lesson 4 (Definition 2.1)': L04.html line 91 defines the payment h(S_t) on exercise. 'backward induction of Lesson 6 (Definition 3.2)': L06.html line 132. The page says it does not apply the recursion to American exercise.")
row("C2c-L07-problem-set", "2.2-numbers/2.4-math", "course/modules/FC/FC2/L07.html lines 293-348", P,
    "Recomputed (recompute.py): M1 d1=0.35, d2=0.15. M2 P=5.573526022 -> 557 cents, unrounded C = 10.45058357. M3 u=1.1051709, d=0.9048374, R=1.0125785, q=0.5378084 (page 1.105171, 0.904837, 1.012578, 0.537808); 0.25 < 16. E1: 400 steps -0.499773, next 200 steps -0.999231 cents. E2 unrounded 171.17, 35.54, 7.04, -91.01, -19.72, -3.99, -2.00, -1.00, -0.50 (page matches). E3 V1 = 12.16228 -> 1216 cents, u=1.221403, q=0.577493. R2 gives 10.450584. P1-P3 re-derived.")
row("C2c-L07-lab1-hypothesis-and-output", "2.5-labs", "course/modules/FC/FC2/L07.html lines 151-268; lab output", P,
    "Expected result in line 151 (positive at 1, 5, 25; negative at 2, 10, 50, 100, 200; 0 at 400) matches the fresh run. Printed Black-Scholes d1 0.350000, d2 0.150000, call 10.450584 = 1045 cents. The interpretation (line 268) says the sign changes 'five times': recomputed from unrounded errors, 5 changes.")
row("C2c-L07-key-results", "2.3-grades", "course/modules/FC/FC2/L07.html line 359 (table lines 355-360)", F,
    "Row 'The tree's parameters satisfy 0 < d < R < u if and only if h < sigma^2/r^2' is graded T with no hypothesis. Lemma 2.2 (line 121) requires r > 0 and sigma > 0. At r = 0 the right side is undefined. The Theorem 2.3 row (line 360) carries r > 0; this row does not.",
    "Change row text to 'For r > 0 and sigma > 0, 0 < d < R < u if and only if h < sigma^2/r^2'.")
row("C2c-L07-quiz", "2.4-math", "course/modules/FC/FC2/L07.html lines 366-435", P,
    "Keys: Q1 r; Q2 d2 = 0.15 (tolerance 1e-4); Q3 put 5.573526 -> 557 cents; Q4 1 - Phi(x); Q5 u = 1.221403 (answer 1.2214 within 1e-4); Q6 h < sigma^2/r^2; Q7 1216; Q8 0 cents (unrounded -0.4998); Q9 convergence not established by the lab; Q10 1045. All verified.")
row("C2c-L07-lab-card-content", "2.7-cards", "course/modules/FC/FC2/cards.json FC2-c099 to FC2-c118 against L07.html", F,
    "Card c102 ('What is the Black-Scholes call formula, and is it derived in this lesson?') is graded T. The formula is stated and not derived (L07 line 86 and Section 4, line 273); the plan's section 5.1 item 7 grades it T only if derived, otherwise C. Card c107 front 'Under A1 to A5 and A7, with h < sigma^2/r^2' drops r > 0, which Theorem 2.3 states (line 129). The other L07 cards match their lesson text; c109-c111 and c117 are graded C with basis 'Lab 1', and the numbers match the run.",
    "Remove the T grade from c102 (ungraded definition card, or C with basis) and add 'r > 0 and' to the c107 front.")
row("C2c-scope-words", "2.4-math/2.6-scope", "course/modules/FC/FC2/L07.html line 274; L08 lines 121, 125, 273-275, 324, 328, 332, 338", F,
    "L07 line 274: 'Assumption A7 takes one volatility sigma for every strike and every maturity.' A7 (line 59) says sigma is constant over the life of the option and 'the same sigma applies to every strike'. It says nothing about maturities. Other scope words checked and backed: L07 lines 59, 268, 282, 284, 324, 338; L08 line 121 (every case the lab accepts: the accept condition gives the bracket), 125 (37 halvings in every case: 9 rows, all 37), 273 (one volatility for every strike, as A7 says), 324 (every row within tolerance: largest 1.74e-11), 328 (every positive volatility: Lemma 2.1 plus Lemma 2.2), 332 (bounds message only at 0 or >= 100 for strike 120: L = 0), 338 (only price function covered).",
    "Replace 'for every strike and every maturity' with 'for every strike' (the wording of A7).")
row("C2c-L07-lab-title-note", "2.5-labs", "course/modules/FC/FC2/L07.html line 149 heading", P,
    "Heading 'Binomial price converging to Black-Scholes' is the curriculum's lab name (plan section 2). The lab does not show convergence (line 268, R1, Q9). Recorded as a note for the architect, not a defect of the lab.")

# ---- L08
row("C2c-L08-lemma-2.1", "2.4-math", "course/modules/FC/FC2/L08.html lines 67-84", P,
    "d1-d2 derivative difference = sqrt(tau); S phi(d1) = K e^{-r tau} phi(d2) by logs with d1^2 - d2^2 = 2a; dC/dsigma = S phi(d1) sqrt(tau) > 0 re-derived. Numeric: vega = 100 phi(0.35) = 37.524035 (recompute.py).")
row("C2c-L08-lemma-2.2", "2.4-math", "course/modules/FC/FC2/L08.html lines 86-93", P,
    "Three cases (a>0, a<0, a=0) re-derived. Numeric: C(1e-6) = 4.877057549928594 = L at K = 100 (recompute.py).")
row("C2c-L08-thm-2.3", "2.4-math", "course/modules/FC/FC2/L08.html lines 95-104", P,
    "Existence by IVT with the limits of Lemma 2.2; uniqueness by strict monotonicity; non-existence outside (L,S) by the bounds C(sigma) in (L,S). Assumptions A1-A5 and A7 in force by line 55. Re-derived.")
row("C2c-L08-prop-3.2-count", "2.2-numbers", "course/modules/FC/FC2/L08.html lines 113-116; M3 lines 298-301", P,
    "W = 10 - 1e-6, tau = 1e-10: log2(W/tau) = 36.5412, ceil 37. Width after 36 halvings (10-1e-6)/2^36 = 1.4552e-10 (1.46e-10 to 3 s.f.), after 37: 7.276e-11. Recomputed in recompute.py.")
row("C2c-L08-prop-3.2-edge", "2.4-math", "course/modules/FC/FC2/L08.html lines 109-119", P,
    "Definition 3.1 now reads 'While sigma_hi - sigma_lo > tau, repeat ... When the loop ends, report'. A bracket already within tau takes no step, so the count of 'smallest k with W/2^k <= tau' (k = 0 when W <= tau) is consistent with the proposition. Invariant and midpoint bound re-derived.")
row("C2c-L08-lab-numbers", "2.5-labs", "course/modules/FC/FC2/L08.html lines 247-267 vs fresh run", P,
    "Fresh run output equals the embedded block exactly: prices 2391, 2459, 2898, 680, 1045, 1802, 46, 325, 1081 cents; sigma_recovered 0.10000000 / 0.20000000 / 0.40000000; 37 halvings every row; largest 1.74e-11; four prices rejected.")
row("C2c-L08-lab-expected-bracket-claim", "2.5-labs", "course/modules/FC/FC2/L08.html line 121; tests/labs/FC2/lab-FC2-L08-1.py lines 203-207", P,
    "Line 121 now says the check fails when [1e-6, 10] does not contain the root, 'when the price is too close to the lower bound or to the spot'. Code (lines 203-207) raises ValueError on 'not gap(LOW) < 0 <= gap(HIGH)'. Witness for the spot case: C(10) = 99.9999440858 at K = 100 (recompute.py), so price 99.99995 is strictly between L and S, passes the bounds check and is rejected by the bracket check, though sigma* exists (Theorem 2.3).")
row("C2c-L08-docstring-locator", "2.1-citations", "tests/labs/FC2/lab-FC2-L08-1.py lines 128-130", P,
    "Docstring now cites 'Lesson 8, Lemma 2.1'. Lemma 2.1 (line 68) is the vega identity and positivity. grep: L08 has no Theorem 2.2.")
row("C2c-L08-canon-defined-only", "2.4-math/2.6-scope", "course/modules/FC/FC2/L08.html line 273", P,
    "Now: 'the implied volatility is defined relative to the A7 formula C(sigma)'. Definition 1.1 (line 62) defines it for any observed price C*, relative to the model. Consistent.")
row("C2c-L08-why-often", "2.1-citations/2.9-prose", "course/modules/FC/FC2/L08.html line 51", F,
    "'A quoted option price is often read as a volatility.' This is an empirical claim about practice with no grade, no data-cite and no computation (BUILDER_RULES 2.1 requires a grade on each substantive claim). No registry key in the slice supports it.",
    "Replace with the claim the lesson can support: 'Under the formula of Lesson 7, a price can be read back as a volatility.'")
row("C2c-L08-R2-rounding-basis", "2.2-numbers", "course/modules/FC/FC2/L08.html lines 340-342", P,
    "Vega 37.52 = 100 phi(0.35) = 37.524035 rounds to 37.52. 0.01/37.52 = 0.00026652 -> 0.000267 (displayed basis). 0.01/37.524035 = 0.00026650 -> 0.000266 (6 dp), as the page says. 0.000267 = 0.0267 vol points = 0.027 to three decimals.")
row("C2c-L08-E-numbers", "2.2-numbers", "course/modules/FC/FC2/L08.html lines 321-332", P,
    "E1: largest 1.74e-11; 1.74e-11/1e-10 = 0.174 of tolerance (printed error basis). E2: 120 e^{-0.05} = 114.1475 -> 114.15; unrounded price at 0.10 = 46.24965 cents -> 46.2497. E3: recovered sigma at price 0.50, strike 120 = 0.10207696 -> 0.102077, 37 halvings (run in recompute.py), accepted.")
row("C2c-L08-E2-every-positive-vol", "2.4-math/2.6-scope", "course/modules/FC/FC2/L08.html line 328", P,
    "'worth something positive for every positive volatility': C strictly increasing (Lemma 2.1) and C -> L = 0 as sigma -> 0+ (Lemma 2.2), so C(sigma) > 0 for every sigma > 0. Valid.")
row("C2c-L08-R1-R3-M1-M2-P-quiz", "2.4-math", "course/modules/FC/FC2/L08.html lines 290-343, 361-435", P,
    "M1 L = 4.877058. M2: of 4.00, 4.90, 100.00 only 4.90 lies in (L, S). M3 37. P1 identity; P2 limit; P3 invariant re-derived. Quiz keys: L08q1 exactly one; q2 4.8771 within 1e-4; q3 4.90; q4 37; q5 positive; q6 37.52 within 0.01 (100 phi(0.35) = 37.524); q8 0; q10 yes. R1, R3 make no claim about a market.")
row("C2c-L08-key-results", "2.3-grades", "course/modules/FC/FC2/L08.html line 358 (table lines 355-359)", F,
    "Row 'Bisection to tolerance tau_tol is within tau_tol/2 of the implied volatility, after ceil(log2(W/tau_tol)) halvings' is graded T and omits two hypotheses of Proposition 3.2 (line 115): W > tau_tol (for W = tau/2 the formula gives -1 while the procedure takes 0 halvings) and L < C* < S (needed for sigma* to exist).",
    "Add 'for W > tau_tol and L < C* < S' to the row.")
row("C2c-L08-cards-content", "2.7-cards", "course/modules/FC/FC2/cards.json FC2-c119 to FC2-c131 against L08.html", F,
    "Card c123 ('For the bisection of Definition 3.1 with bracket width W and tolerance tau_tol, how many halvings ... and how close is the midpoint?') gives 'the midpoint is within tau/2 of sigma*'. sigma* exists only when L < C* < S (Theorem 2.3, Proposition 3.2 line 115); the card does not state it. Other cards c119-c122, c124-c127, c129-c131 match their lesson text, and their numbers appear in the lesson.",
    "Add 'with L < C* < S' to the front of c123.")
row("C2c-cards-L08-grades-ok", "2.3-grades/2.7-cards", "course/modules/FC/FC2/cards.json FC2-c120 to FC2-c131", F,
    "FC2-c128 ('Does a successful inversion check in Lab 1 show that a quoted price is right?') is graded T with no basis. Its content is a claim about what Lab 1's code tests. BUILDER_RULES 7 requires a result the lesson establishes by a lab to name it in basis, and L08 line 361 says the lab carries no grade. Other L08 grades are correct: T for Lemmas 2.1-2.2 and Theorem 2.3; c125 T with basis 'Problem M3 (exact); Lab 1'; c129 C with basis; c130 T is a reading of Definition 1.1.",
    "Grade c128 C with basis 'Lab 1 (inversion code and inputs)', or remove the grade.")
row("C2c-cards-grades-lab", "2.3-grades", "course/modules/FC/FC2/cards.json FC2-c109, c110, c111, c117", P,
    "Each is graded C with a basis naming Lab 1 (or Lab 1 and Problem E1). Numbers verified: c109 10.450584 = 1045 cents; c110 -91.008 cents (-91 printed); c111 signs and -0.4998 cents; c117 -0.0049977 currency units. Round 1 grade-T defect is fixed.")
row("C2c-cards-duplicates", "2.7-cards", "cards.json FC2-c111 and FC2-c117", F,
    "Both state the same fact about the 400-step error: c111 'At 400 steps the unrounded error is -0.4998 cents, which prints as 0'; c117 'unrounded error of -0.0049977 currency units, which is -0.4998 cents and shown as 0'. Checked other pairs: c104/c112 (dependence of C vs the d1 identity), c127/c129 (which prices have a volatility vs the rejection list), c122/c129, c109/c118 are distinct facts.",
    "Remove the 400-step fact from c117 and keep c111, or make c117 ask only for the step count and link to c111.")
row("C2c-dag-links", "2.8-dag", "L07.html lines 37, 98; L08.html line 37; curriculum.json", P,
    "Linked concepts: binomial-option-pricing, risk-neutral-probability (L06), put-call-parity, option-payoff (L04), option-arbitrage-bounds (L05), black-scholes-formula (L07), discount-factor, continuous-compounding (M1), normal-distribution (M4), limit and derivative (M2). FC2 prerequisite closure from curriculum.json (M4, CF1, FC1 and their closure: AC1, CF1, E1, FC1, M1, M2, M4, P0.1) contains all owners. Prose-only uses: 'continuous-time model', 'risk-neutral expectation' (L07 line 360), 'lognormal' (dfn without data-concept), 'bisection' (defined in L08 Section 3).")
row("C2c-hours", "2.9-hours", "index.html data-hours-lessons; L07 data-hours=8; L08 data-hours=6", P,
    "L01-L08 declared hours 6+8+9+7+8+8+8+6 = 60 = hub data-hours-lessons=60. Pace not assessed (architect ruling).")
row("C2c-notation", "2.4-notation", "L07.html, L08.html, lab twins vs notation/notation.json", P,
    "T absent from the slice (L07 line 55 'not T'). Phi is the standard normal CDF (M4 meaning). R^* and R_f not used; L07 uses R^{(n)} = e^{rh} for the per-step gross return, the meaning of L06's R_f but a different symbol (not a conflict; noted). Q, gamma absent. phi is the density (not registered). L, W, V, C, P, h, u, d, q are local and not registered.")
row("C2c-prose-banned", "2.9-prose", "L07.html, L08.html", P,
    "grep for TODO, TBD, lorem, for brevity, omitted, beyond the scope, left as an exercise, it is important, well known, obviously, clearly, roughly, historically, about 6, studies show, experts agree, and for ellipses: no hits.")
row("C2c-scope-every-only-check", "2.4-math/2.6-scope", "L07.html, L08.html", P,
    "Scope words in L07 and L08 were checked one by one; see C2c-scope-words for the one that fails (line 274). The remaining occurrences are backed by a computation, a stated hypothesis, or a code check.")
row("C2c-mutants-not-applicable", "2.6-mutants", "ledgers/FC2/mutants/ (project grader only)", P,
    "Architect ruling: lab twins are demonstrations; mutation testing applies to project graders only. This slice has no grader, so no mutant was run and no alternative correct implementation of a grader was needed.")

fails = [r["id"] for r in rows if r["status"] != P]
summary = {"rows": len(rows), "pass": sum(1 for r in rows if r["status"] == P), "fail": len(fails),
           "unverifiable": 0, "fail_ids": fails}
frag = {
    "unit": "FC2",
    "slice": "FC2-c",
    "round": 2,
    "verifier": "Haiku independent verifier, round 2, slice FC2-c (L07-L08 and their lab twins). Did not build FC2 and shares no context with its builders.",
    "pin": "e22feb3",
    "base": "none",
    "checkout": "/tmp/verifyC2-FC2-c (detached at e22feb3; .venv symlinked)",
    "scratch": "/tmp/FC2-v/FC2-c",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since the round 1 pin 55b5634 (git diff 55b5634 e22feb3): changed for this slice are course/modules/FC/FC2/L07.html, L08.html, cards.json and tests/labs/FC2/lab-FC2-L08-1.py. The lab twin lab-FC2-L07-1.py is byte-identical, but its rows were re-run anyway. notation/, curriculum/, tools/, references/references.json and plans/ are unchanged in the diff.",
        "The brief lists prerequisites AC1, S0, S2. curriculum.json gives FC2 prerequisites M4, CF1, FC1 (closure AC1, CF1, E1, FC1, M1, M2, M4, P0.1); the DAG check used curriculum.json.",
        "No mutants and no alternative implementations: the slice has no project grader (architect ruling).",
        "Round 1 FAIL rows fixed and re-verified: C2c-L07-def-2.1-A6, C2c-L07-thm-2.3-hypotheses (theorem statement), C2c-L07-lab1-prose-147, C2c-L07-lab1-sign-400, C2c-L07-misconception-same-rtau, C2c-L07-line275-rule, C2c-L08-prop-3.2-edge, C2c-L08-lab-expected-bracket-claim, C2c-L08-docstring-locator, C2c-L08-canon-defined-only, C2c-cards-grades-lab. Still failing: C2c-cards-duplicates (c111/c117). Round 1 FAIL rows for the key results and cards are re-verified with new defects (C2c-L07-key-results, C2c-L08-key-results, C2c-L07-lab-card-content, C2c-L08-cards-content, C2c-cards-L08-grades-ok).",
        "Round 1 PASS rows were re-run on the changed subjects (L07.html, L08.html, cards.json); none was carried.",
        "pytest tests/test_labs.py -k FC2: 11 passed; tests/test_curriculum.py and tests/test_page_checks.py -k FC: 3 passed.",
        "page_smoke was run with --skip-sweep, as in round 1. Lab runtime 0.0 s per lab.",
    ],
    "summary": summary,
}
out = ROOT / "ledgers/FC2/FC2-c.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=1))
