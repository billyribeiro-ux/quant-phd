"""Writes the round-1 fragment for SC1 slice b (L04-L06 and lab twins). Every row cites a file and line, or a command output kept under out/."""
import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
P = "course/modules/SC/SC1/"

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
    row("b-check-pages", "2.9 structure", P + "L04.html, L05.html, L06.html", "PASS",
        "tools/check_pages.py --unit SC1 -> 'check_pages SC1: PASS' (out/check_pages.txt). Counted by script on the pages: why-it-matters 85, 97, 119 words (limit 120); misconceptions 3/3/3; problems 3 per tier per page; quiz items 11/10/10; data-hours=9 on each page."),
    row("b-check-dag", "2.9 DAG", P + "L04.html, L05.html, L06.html", "PASS",
        "tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS' (out/check_dag.txt). Cross-lesson links point to earlier definitions only: L04 L01.html#def-brownian-motion and L03.html#def-quadratic-variation; L05 L01.html#def-brownian-motion; L06 L01.html#def-brownian-motion. Plan section 4 names D1-D9 (Ito, GBM, OU, Euler, Girsanov, Feynman-Kac, Poisson/Levy, Black-Scholes/barrier, Monte Carlo, bias): grep on the three pages finds none of them used as concepts (only English 'option', 'drift' in a canon-break, and the \\blacksquare macro)."),
    row("b-run-labs", "2.5 labs", "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py", "PASS",
        "tools/run_labs.py --unit SC1 -> 'run_labs SC1: PASS (11/11)' (out/run_labs.txt)."),
    row("b-twin-match", "2.5 labs (page code = twin; expected = output)", P + "L04.html:145-224, L05.html:163-258, L06.html:184-296", "PASS",
        "ledgers/SC1/scripts/SC1-b-r1/twin_match.py (out/twin_match.txt, 'ALL MATCH'): the <code data-run> block of each page equals its twin byte-for-byte after trimming; each twin runs under 'python -I -W error' with exit 0; stdout equals the page's expected block for all three labs."),
    row("b-lab-lint", "2.5 labs (ruff, mypy)", "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py", "PASS",
        "ruff check: 'All checks passed!'; ruff format --check: '3 files already formatted'; mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' (out/ruff.txt, out/mypy.txt). Imports are standard library only (math, collections, fractions, itertools, __future__)."),
    row("b-page-smoke", "2.9 page_smoke (alone)", P + "L04.html, L05.html, L06.html", "PASS",
        "tools/page_smoke.py --unit SC1 --pages L04 L05 L06, run alone -> 'page_smoke modules/SC/SC1/L04.html: PASS', L05 PASS, L06 PASS, 'page_smoke SC1: PASS' (out/page_smoke.txt). Lab runtimes 0.0 s, 1.3 s, 0.0 s."),
    row("b-pytest-tooling", "2.5 tooling pytest", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
        "python -m pytest -q on the three files: 100% passed, exit 0 (out/pytest.txt)."),
    row("b-verify-refs", "2.1 citations (live)", "registry key shreve2004stochastic, cited by name only in " + P + "L04.html:467, L05.html:510, L06.html:534", "PASS",
        "tools/verify_refs.py --unit SC1 (live, plain run): 'live re-verification of SC1: 1 of 560 entries, 0 problems' (out/verify_refs.txt). The three pages carry no data-cite attribute (grep), and each references paragraph states that no passage is attributed to the key."),
    row("b-cross-L04", "2.9 cross-references", P + "L04.html:37, 55-75, 116-119, 126", "PASS",
        "L01.html:61-63 defines (D1) B_0=0, (D2) increment law, (D3) independence, as L04 uses them. L03.html:70 Assumption 3.2(a) matches L04.html:65 (functions of single variables). L03.html:89-95 Lemma 2.2 gives E[X^4]=3 Delta^2, matching L04.html:119, 263, 405 (3t^2 at t=3 is 27). L03.html:109 Theorem 2.3 mean step matches L04 Remark at line 126. L03.html:59 defines quadratic-variation at the anchor L04 links."),
    row("b-cross-L05-L06", "2.9 cross-references", P + "L05.html:56, 329, 282; " + P + "L06.html:102, 127-136", "PASS",
        "L01.html Proposition 1.2 (covariance) matches L05.html:327. L01.html:72-76 Assumption A1(c) matches L05.html:329. L01.html section 4 (tilde B, lines 210-215) matches L05.html:282 and L06.html:302. L02 Theorem 2.5, Assumption A2 and Remark 2.6 (titles in L02.html) match L06.html:102. SC1 L08.html h1 'First-Passage Times' matches L06.html:102 and L05.html:283. M6 L08 h1 'Filtrations and discrete-time martingales' matches L04.html:231. L05 A3 and A4(b),(c) (L05.html:58-68, 265-272) match L06.html:127-128."),
    row("b-num-L04", "2.2 numbers", P + "L04.html:223, 216-222, 313, 320, 327, 417-451", "PASS",
        "ledgers/SC1/scripts/SC1-b-r1/recompute.py (out/recompute.txt): e^1=2.718281828, e^0.25=1.284025417, e^4=54.598150033, e^8=2980.957987. The twin output (out/twin_match.txt) reproduces the three E[exp(theta B_t)] values. The line-223 claim that they are e^1, e^(1/4), e^4 is correct since theta^2 t/2 = 1, 1/4, 4 at t=2."),
    row("b-num-L05", "2.2 numbers", P + "L05.html:165, 250-258, 363, 368-370, 453, 494", "PASS",
        "recompute.py: p_1(0,0)=(2 pi)^(-1/2)=0.3989422804, printed 0.3989 (quiz tolerance 1e-4 met). Phi(-1/sqrt2)=0.2397500611, printed 0.23975 (tolerance 1e-5 met). E1 ratio 5.55e-16/3.81e-29 = 1.4567e13, written 'about 1.5x10^13' (two significant figures). E2 bound 5e-11 is the half-unit of the tenth decimal. Lab gap and tail values come from the twin run (out/twin_match.txt)."),
    row("b-num-L06", "2.2 numbers", P + "L06.html:288-294, 295, 318, 336, 343, 350, 384-398, 477, 509", "PASS",
        "recompute.py (out/recompute.txt), independent walk enumeration: Part A 1014 triples, 1014 equal; Part B 78 pairs; Part C M12>=3: 1588 of 4096, with S12=2: 495, S12=4: 495; Part D P(M10>=2)=281/512, 2P(S10>2)=11/32=352/1024, P(S10=2)=105/512=210/1024=C(10,6)/1024, identity holds; Part E erfc(1/sqrt2)=0.317310507863 and half=0.158655253931 (printed 0.1586552539). E1 arithmetic and E2 arithmetic check."),
    row("b-math-L04-lemma-2.1", "2.4 maths", P + "L04.html:81-90", "PASS",
        "Completing the square theta*y - y^2/(2h) = theta^2 h/2 - (y - theta h)^2/(2h) verified by expansion; normalisation of the shifted density used correctly."),
    row("b-math-L04-prop-2.2", "2.4 maths", P + "L04.html:92-106", "PASS",
        "H1 and H2 are used where stated. E[B_t|F_s] = B_s + E[Y|F_s] = B_s using 4.2(a), (c) with B_s F_s-measurable, Assumption 4.1 for independence and 4.2(d) for E[Y|F_s]=E[Y]=0. Each step checked."),
    row("b-math-L04-prop-2.3", "2.4 maths (proof gap)", P + "L04.html:117-124, proof part (ii) at line 119", "FAIL",
        "Parts (i) and (iii) are correct. Part (ii) shows only E[B_t^4]=3t^2 < infinity. Definition 1.2(ii) needs E[(B_t^2 - t)^2] < infinity, which equals E[B_t^4] - 2t E[B_t^2] + t^2 = 3t^2 - 2t^2 + t^2 = 2t^2; the page never computes it. Reviewed by hand; no numerical check needed."),
    row("b-math-L04-prop-2.4", "2.4 maths", P + "L04.html:129-143", "PASS",
        "E[e^(2 theta B_t)] = e^(2 theta^2 t) by Lemma 2.1 gives E[M_t^2] = e^(theta^2 t). W = exp(theta Y - theta^2 h/2): E[W^2] = e^(theta^2 h), E[W] = 1. M_t = M_s W holds. Verified by hand."),
    row("b-math-L04-A4.1-sketch", "2.4 maths (labelled sketch)", P + "L04.html:63-66", "PASS",
        "Labelled 'Sketch, not a proof' and names the two skipped steps (pi-system, pi-lambda extension). Its appeal to Assumption 3.2(a) of Lesson 3 is correct (L03.html:70)."),
    row("b-math-L04-misconception-1", "2.4 maths (undeclared assumptions)", P + "L04.html:240", "FAIL",
        "The derivation of E[B_t^3 | F_s] = B_s^3 + 3(t-s)B_s uses E[Y|F_s]=E[Y], E[Y^3|F_s]=E[Y^3] and E[Y^2|F_s]=t-s, which rest on Assumptions 4.1 and 4.2(a),(c),(d). The sentence states neither assumption. The result is correct."),
    row("b-math-L04-R1-R3", "2.4 maths (problems)", P + "L04.html:336-352", "PASS",
        "R1 (B_t^2 - g(t) is a martingale iff g(t) = t + c), R2 (c^2 h = 0 with Z_s > 0), R3 (conditional variance = t - s) re-derived by hand; the logic and the 'Assuming' statements are sound."),
    row("b-prose-L04-R2-title", "2.9 prose accuracy", P + "L04.html:342-343", "FAIL",
        "The title 'The only power of the exponential that is a martingale' claims more than the problem proves. Proposition 2.4 (L04.html:129-135) shows exp(theta B_t - theta^2 t/2) is a martingale for every theta. The problem itself concerns exp(cB_t) with no drift term."),
    row("b-prose-L04-remark-numbering", "2.9 structure", P + "L04.html:109, 126, 37", "FAIL",
        "Two items carry the number 2.3: Proposition 2.3 (line 109) and Remark 2.3 (line 126). Line 37 refers to 'Remark 2.3' for the quadratic-variation remark."),
    row("b-scope-L04-footer", "2.9 scope", P + "L04.html:478", "FAIL",
        "The footer says 'Every theorem is proved on the page'. The propositions are proved only from Assumptions 4.1 and 4.2, which the page states and does not prove (L04.html:64-70)."),
    row("b-lab-L04-hypothesis", "2.5 lab claims", P + "L04.html:147", "FAIL",
        "The hypothesis says the integral of M_t against the density 'should equal M_0 = 1 ... which is Proposition 2.4 at s = 0'. Proposition 2.4 at s=0 gives E[M_t | F_0] = M_0, and E[M_t] = 1 also needs the tower property (Assumption 4.2(b)), which the sentence omits. The code and output match the prediction."),
    row("b-lab-L04-interpretation", "2.5 lab claims", P + "L04.html:223", "PASS",
        "The printed values 2.718281828, 1.284025417, 54.598150033 and E[M_t] = 1.000000000 match the twin output. The statement that the check does not prove the martingale property for other theta or t is correct."),
    row("b-math-L05-lemma-1.3", "2.4 maths (unnumbered fact)", P + "L05.html:96", "FAIL",
        "The proof uses 'functions of disjoint groups of mutually independent variables are independent' (grouping lemma). This is not one of A4(a)-(e) (L05.html:59-67) and is not labelled as an assumption or a sketch."),
    row("b-math-L05-thm-1.4", "2.4 maths", P + "L05.html:100-118", "PASS",
        "Proof verified: Assumption A4(b) with Z = B_s, Y = B_t - B_s, and the density substitution y = z + w gives psi(z) = integral of g(y) p_u(z,y) dy. The notation problem with the symbol Phi is a separate row."),
    row("b-math-L05-lemma-2.2-thm-2.1", "2.4 maths", P + "L05.html:129-161", "PASS",
        "Lemma 2.2 expansion and the constant-term cancellation verified by hand; P1 numeric check at u=1, v=3, x=0, y=1 reproduced (recompute.py, out/recompute.txt). Theorem 2.1 constants: (2 pi)^(-1) (uv)^(-1/2) times (2 pi uv/(u+v))^(1/2) = (2 pi (u+v))^(-1/2); uv cancels."),
    row("b-math-L05-A3-sketch", "2.4 maths (sketch citation)", P + "L05.html:276", "FAIL",
        "The sketch says 'the Markov property at the fixed time q (Theorem 1.4) gives the conclusion of A3 for rho_n on {rho_n = q}'. Theorem 1.4 gives only the conditional law psi(B_s) (L05.html:107-111). The A3 conclusion (B_{q+.} - B_q is a standard Brownian motion independent of F_q) needs Lemma 1.3 for independence and (D1)-(D3) for the law."),
    row("b-math-L05-R3", "2.4 maths", P + "L05.html:399-401", "FAIL",
        "The R3 proof starts 'For any real x' and so does not cover rho = infinity, which the stopping-time definition allows (values in [0,infinity], L05.html:263). The inequalities rho <= rho_n <= rho + 2^-n are then undefined on {rho = infinity}."),
    row("b-math-L05-problems", "2.4 maths and 2.5 empirical", P + "L05.html:309-405", "PASS",
        "M1 (1/(2 sqrt pi) and p_2(0,0)), M2 (B_1^2+2 and B_1^3+6B_1 with Z ~ N(0,2)), M3 (covariance 0), P1 (Lemma 2.2 at u=1, v=3), P2 (CDF formula), P3 (normalisation), R1 (sigma* is not a stopping time), R2 (deterministic time), E1-E3 (numbers and claims) re-derived by hand or by recompute.py."),
    row("b-math-L05-misconceptions", "2.9 prose and maths", P + "L05.html:291-303", "PASS",
        "Misconceptions 1-3 are correct: the conditional law is N(B_s, t-s); the marginal density is p_t(0,.) and the two agree only at x=0, s=0; the 225-case check is not a proof (Theorem 2.1 is)."),
    row("b-scope-L05-D1D3", "2.9 scope", P + "L05.html:56", "FAIL",
        "'Sections 1 and 2 use only (D1) to (D3)' is false: Section 1 uses Assumption A4(a) (Lemma 1.3, L05.html:89) and A4(b) (Theorem 1.4, L05.html:105); Section 2 uses A4(e) (Theorem 2.1, L05.html:142)."),
    row("b-notation-L05-Phi-varphi", "2.4 notation", P + "L05.html:62, 116, 117, 276, 477", "FAIL",
        "notation/notation.json and plan section 2.3 (plans/SC1-build-plan.md:219) register \\Phi as the standard normal CDF. L05 uses \\Phi for a generic bounded function in A4(b) (line 62), the Theorem 1.4 proof (line 116), the A3 sketch (line 276) and quiz Q7 (line 477). \\varphi(z) is used for an expectation (lines 62, 116), while plan section 2.3 restricts \\varphi to the Gaussian density. The correct uses in P2 (line 344-346) are fine."),
    row("b-notation-L05-X-n", "2.4 notation (undefined symbol)", P + "L05.html:276, 477", "FAIL",
        "X^{(n)} appears in the A3 sketch and in quiz Q7 but is defined nowhere on the page."),
    row("b-notation-M-clash", "2.4 notation (local symbol)", P + "L04.html:75, 134, 140-147, 380; " + P + "L06.html:107, 112-114", "FAIL",
        "Plan section 2.3 (plans/SC1-build-plan.md:223-224) binds M_t to the running maximum max_{s<=t} B_s, and L06 Lemma 2.1 uses it that way. L04 uses the same symbol for a continuous-time martingale (Definition 1.2, line 75; Proposition 2.4, line 134; lab hypothesis, line 147; quiz Q1, line 380). The same symbol carries two meanings in SC1."),
    row("b-quiz-L05-Q7", "2.9 quiz (notation)", P + "L05.html:477", "FAIL",
        "The correct option is right and its explanation matches the sketch. The option text uses \\Phi as a generic function and X^{(n)} undefined (see b-notation-L05-Phi-varphi and b-notation-L05-X-n)."),
    row("b-scope-L05-canonical", "2.9 term definition", P + "L05.html:387", "FAIL",
        "'the canonical space of continuous paths' is used but is not defined on the page or in the curriculum (NOT IN CURRICULUM per plan section 4)."),
    row("b-term-almost-surely", "2.9 term definition", P + "L05.html:62 (first use); also L06.html:144", "FAIL",
        "'almost surely' first appears in Assumption A4(b) with no plain-words gloss, though plan section 2.1(5) requires non-curriculum terms to be glossed at first use."),
    row("b-math-L06-facts-unnumbered", "2.4 maths (unnumbered fact)", P + "L06.html:140-144", "FAIL",
        "The proof applies Assumption A4(b), which is stated for a random variable Y, to the process X. It also uses that (u, omega) -> X_u(omega) is jointly measurable, stated only as a remark, not as a numbered fact."),
    row("b-math-L06-prop-1.3-cor-1.4", "2.4 maths", P + "L06.html:75-98", "PASS",
        "Reflection bijection (Lemma 1.2) verified; the set equality for tau <= N uses that the walk moves by +-1; Corollary 1.4 sum over b < a maps onto the integers above a. Problems M1-M3, P3 and the lab counts (1014, 78, 495) agree."),
    row("b-math-L06-lemma-2.1", "2.4 maths", P + "L06.html:104-115", "PASS",
        "(i), (ii), (iii) checked: closedness of {s: B_s = a} gives B_{tau_a} = a; IVT arguments on [0,t] and [0,s] are valid. P2 proves (ii) and (iii) without (i)."),
    row("b-math-L06-prop-2.3-thm-2.5", "2.4 maths", P + "L06.html:122-171", "PASS",
        "Explicit form of W_t, the stopping time property of tau_a (A4(c)), the law equality via A3, A4(b) and symmetry, and the event identity E = {W_t > a} with P(B_t = a) = 0 re-derived; hypotheses are declared (L06.html:124-129, 153-158). The joint-measurability step is a separate row."),
    row("b-math-L06-cor-2.6", "2.4 maths", P + "L06.html:173-182", "PASS",
        "Substitution z = sqrt(2) w with lower limit a/sqrt(2t) and the factor 1/sqrt(pi) gives 2P(B_t > a) = erfc(a/sqrt(2t)) by the definition of erfc. Verified by hand and numerically (erfc(1/sqrt2)/2 = 0.158655253931 = P(B_1 > 1))."),
    row("b-math-L06-R1-R3", "2.4 maths (problems)", P + "L06.html:404-424", "PASS",
        "R1 parity argument (every S_N has the parity of N) correct. R2 uses -B, which satisfies (D1)-(D3), and Theorem 2.5 for -B. R3 uses 2x > x for x > 0 and positivity of the normal law. Verified by hand."),
    row("b-math-L06-E1-E3", "2.5 empirical", P + "L06.html:380-400", "PASS",
        "E1 (78 = sum of N over N = 1..12; a > N not checked, stated honestly), E2 (281/512 - 11/32 = 105/512 = 210/1024), E3 (half of 0.3173105079 = 0.15865525395 vs printed 0.1586552539) verified by recompute.py."),
    row("b-scope-L06-only-events", "2.9 scope", P + "L06.html:102", "FAIL",
        "'This lesson uses only the events {tau_a <= t}' is inaccurate: Proposition 2.3 uses the random time rho = tau_a ^ t, the variable B_rho and the process W (L06.html:127-136)."),
    row("b-scope-L06-N12-every-case", "2.5 lab scope and 2.2 claims", P + "L06.html:295, 440", "FAIL",
        "Both say the identities hold 'on every case with N <= 12'. The twin's Part A loops over a in range(1, n+1) (a <= N) and Part B over a in range(1, n+1). Cases a > N are not computed, and the page itself says so (L06.html:384). Restrict the claim to 1 <= a <= N."),
    row("b-lab-L06-claims", "2.5 lab claims", P + "L06.html:186, 295 (Parts C, D, E)", "PASS",
        "Part C (495 = 495, 1588 of 4096), Part D (281/512, 11/32, 105/512 and the difference identity) and Part E (erfc(1/sqrt2)) claims match the twin output and recompute.py. The 'Parts A and B' scope is a separate row."),
    row("b-rounding-L06-misconception", "2.2 rounding rule", P + "L06.html:314", "FAIL",
        "'Corollary 2.6 gives erfc(1/sqrt2) = 0.3173, while P(B_1 >= 1) = 0.1587' shows rounded figures without a rounding rule (plan section 2.1(1) requires one). The rounded values are correct."),
    row("b-plan-L06-pathlevel", "2.4 plan coverage", P + "L06.html:117-120, 148-150; plans/SC1-build-plan.md:261-262", "FAIL",
        "Plan section 3 lists for L06: the reflected path after tau_a is a Brownian motion (assuming A3). The page defines the reflection principle (Definition 2.2) and proves only the fixed-time form (Proposition 2.3), stating the path-level claim is not proved (Remark 2.4). The page is honest but deviates from the plan."),
    row("b-plan-coverage-L04-L05", "2.4 and 2.9 plan coverage", P + "L04.html, L05.html", "PASS",
        "L04 covers filtration, continuous-time martingale definition, B_t, B_t^2 - t, exponential martingale (T), the quadrature lab (C). L05 covers the Markov property, the Gaussian transition density, Chapman-Kolmogorov (T, completing the square) and A3 stated with a sketch that names the skipped step. Canon-break sections exist on each page."),
    row("b-hours-L04-L06", "2.9 hours", P + "L04.html:2, L05.html:2, L06.html:2", "PASS",
        "data-hours=9 on each page, inside the 6-12 range (tools/check_pages.py rule). The hub split is outside this slice."),
    row("b-quiz-L04-L06", "2.9 quiz (L04, L06 and L05 except Q7)", P + "L04.html:375-462, L05.html:423-506, L06.html:447-530", "PASS",
        "Every correct option and explanation checked against the page's lemmas and the lab output. Numeric answers checked against tolerance: L04 Q6 (2.718281828 vs e^1, error 4.6e-10 < 1e-9), L05 Q4 (0.3989 vs 0.398942), L05 Q9 (0.23975 vs 0.2397500611), L06 Q2 (0.25), Q4 (0.3173 vs 0.317311), Q8 (0.1587 vs 0.158655). Only L05 Q7 fails (separate row)."),
]

fragment = {
    "unit": "SC1",
    "slice": "b",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-b, round 1 (did not build SC1; covers L04, L05, L06 and their three lab twins)",
    "pin": "1c1645f",
    "base": "none (first verification of this slice)",
    "checkout": str(ROOT),
    "scratch": str(ROOT / "ledgers/SC1/scripts/SC1-b-r1"),
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": None,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice b = course/modules/SC/SC1/L04.html, L05.html, L06.html and tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py. "
        "Every rule of verifier-rules.md applied to this slice. Targeted commands run on the pin: check_pages, check_dag, run_labs, twin match, page_smoke (alone, three pages), ruff, mypy, pytest (three tooling files), verify_refs (live, 1 entry), and an independent recomputation (recompute.py). "
        "Lab twins are demonstrations, so no mutation testing applies to them (architect ruling); no project grader is in this slice, so no student-error mutants were written. "
        "Not checked: retrieval cards (cards.json, builder F), L01-L03 and L07-L08 beyond the cross-references above, the hub and project pages, and the full gate (not run: this slice did not touch deps, build or CI)."
    ),
    "summary": "",
}
statuses = [r["status"] for r in rows]
counts = {s: statuses.count(s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment["verdict"] = "PASS" if counts["PASS"] == len(rows) else "FAIL"
fragment["summary"] = (
    f"SC1-b round 1: verdict {fragment['verdict']}. {len(rows)} rows: pass={counts['PASS']} fail={counts['FAIL']} "
    f"unverifiable={counts['UNVERIFIABLE']}. No mutants (lab twins only)."
)
out = ROOT / "ledgers/SC1/SC1-b.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out, fragment["verdict"], len(rows), counts)
