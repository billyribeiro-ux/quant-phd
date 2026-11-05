"""Writes ledgers/SC1/SC1-b.json (round 8, slice b) from the rows below. Evidence cites the scripts and outputs
under ledgers/SC1/scripts/SC1-b-r8/. Run from the checkout root with: python3 -I <this script>."""
import json
from datetime import datetime, timezone

S = "ledgers/SC1/scripts/SC1-b-r8/out/"
G = "course/modules/SC/SC1/"
rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates and tooling (re-run this round on 0dee921)
row("b-check-pages", "2.9 structure (check_pages)", G + "L04.html, L05.html, L06.html", "PASS",
    "Re-run this round: .venv/bin/python tools/check_pages.py --unit SC1 -> 'check_pages SC1: PASS', exit 0 (" + S + "check_pages.txt).")
row("b-check-dag", "2.9 DAG (check_dag)", G + "L04.html, L05.html, L06.html", "PASS",
    "Re-run: tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS', exit 0 (" + S + "check_dag.txt).")
row("b-run-labs", "2.5 labs (run_labs, page by page)", "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py", "PASS",
    "Re-run: tools/run_labs.py --unit SC1 --page L04, L05, L06 -> each 'run_labs SC1: PASS (1/1)', exit 0 (" + S + "run_labs_L04.txt, run_labs_L05.txt, run_labs_L06.txt).")
row("b-twin-match", "2.5 labs: page code equals twin; twin runs under python -I -W error; expected equals stdout",
    G + "L04.html (lab-SC1-L04-1), L05.html (lab-SC1-L05-1), L06.html (lab-SC1-L06-1)", "PASS",
    "ledgers/SC1/scripts/SC1-b-r8/twin_match_r8.py (" + S + "twin_match_r8.txt): for each page the data-run code equals the twin "
    "(compared after removing the final newline, which embed_labs strips); expected block equals `python3 -I -W error` stdout; exit 0, empty stderr, "
    "no @@LAB/@@OUT markers left; 'ALL PASS'. Twin sha256 79a56370..., 744046b7..., 8d01822e... (" + S + "twin_sha256_r8.txt), unchanged since round 7.")
row("b-lab-lint", "2.5 labs (ruff check, ruff format --check, mypy --no-incremental)", "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py", "PASS",
    "ruff check tests/labs/SC1: 'All checks passed!' (" + S + "ruff_check.txt); ruff format --check: '11 files already formatted' (" + S + "ruff_format.txt); "
    "mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' (" + S + "mypy_labs.txt).")
row("b-page-smoke", "2.9 page_smoke (run on the three pages)", G + "L04.html, L05.html, L06.html", "PASS",
    "Re-run: tools/page_smoke.py --unit SC1 --pages L04 L05 L06 (full run, figure sweep included) -> 'page_smoke SC1: PASS', exit 0 (" + S + "page_smoke.txt).")
row("b-pytest-tooling", "2.5 tooling pytest (labs and page checks)", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
    "Re-run: .venv/bin/pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q -> all dots, exit 0 (" + S + "pytest_tooling.txt).")
row("b-verify-refs", "2.1 citations (offline integrity and unit re-verification)", "references/references.json (shreve2004stochastic)", "PASS",
    "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (" + S + "verify_refs_offline.txt); "
    "tools/verify_refs.py --unit SC1 -> 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0 (" + S + "verify_refs_unit.txt).")
row("b-attribution-references", "2.1 attribution: no passage, locator or theorem number attributed to an unread source",
    G + "L04.html:468, L05.html:514, L06.html:536", "PASS",
    "Each References section names shreve2004stochastic only as the record and attributes no passage. The registry record (references/references.json:20732, title 'Stochastic Calculus for Finance II', 2004, status verified) matches the curriculum string 'Shreve, Stochastic Calculus for Finance II (2004)' (curriculum/03-markets.yaml, SC1 sources). The second string (Karatzas & Shreve) has no registry record and is not cited anywhere in the slice (grep). Assumptions A3/A4 and A4 of L05 are stated without attribution.")
row("b-cross-L04", "2.9 cross-references into L01 and L03", G + "L04.html:37, 65, 117-124, 126", "PASS",
    "L04:37 links def-brownian-motion (L01.html:58 Definition 1.1, (D1)-(D3)) and the L03 quadratic-variation definition; L04:65 cites (D1), (D3) of Lesson 1 (L01.html:58-63) and Assumption 3.2(a) of Lesson 3, which is the statement about functions g_k(X_k) of single independent variables (L03.html:70-76); L04:119 cites Lemma 2.2 of Lesson 3 for E[X^4]=3 Delta^2 (L03.html:89-96). Checked by reading those lines.")
row("b-cross-L05-L06", "2.9 cross-references into L01, L02, L03, L06, L08 and M6", G + "L05.html:56, 267, 278, 285-288; L06.html:52, 102", "PASS",
    "L05:56 Definition 1.1 of Lesson 1 = L01.html:58 (D1)-(D3); L05 M3 cites Proposition 1.2 (Cov=min) = L01.html:84 and A1(c) (zero covariance of jointly normal coordinates => independent) = L01.html:72-82; L05:267 'M6 Lesson 9, Definition 9.1' = course/modules/M/M6/L09.html:59 (Definition 9.1 stopping time); L05:278 'Lesson 6, Section 2' defines tau_a (L06.html:100-102); L05:285-288 'Lesson 1, Section 4' = L01.html:212-216 (discontinuous paths); L06:102 Lesson 2 Theorem 2.5 (H2: A2 and Assumption 2.1, L02.html:289-296), Remark 2.6 (H2: A1(a), A1(b), A1(e), A2, Assumption 2.1, L02.html:303-307), A2 (L02.html:282); L06:52, 102 'Lesson 8' (L08.html:77-92: Corollary 1.3 law of tau_a, Corollary 1.4 finite with probability one); L04:232 'Lesson 8 of M6' = course/modules/M/M6/L08.html 'Filtrations and discrete-time martingales'.")
row("b-num-L04", "2.1 numbers in prose re-derived from unrounded values", G + "L04.html:224, 314, 321, 328, 380-452 (quiz)", "PASS",
    "ledgers/SC1/scripts/SC1-b-r8/recompute_r8.py (" + S + "recompute_r8.txt): e^1=2.718281828, e^(1/4)=1.284025417, e^4=54.598150033, e^8=2980.957987 (6 dp), |e-2.718281828|=4.6e-10 (<=1e-9 tolerance, quiz), |e^4-54.598150033|=1.4e-10, E[B_3^2]=3, E[B_3^4]=27, E[(B_t^2-t)^2]=2t^2 at t=1,2,3, and E[W^2]=e^{theta^2 h}, E[W]=1 by Simpson at theta=0.7, h=1.3 (residuals below 1e-13).")
row("b-num-L05", "2.1 numbers in prose re-derived from unrounded values", G + "L05.html:262, 305, 319, 326-367, 372-381, 498", "PASS",
    "recompute_r8.py (" + S + "recompute_r8.txt): 1/(2 sqrt pi)=0.2820947918 = p_2(0,0) (M1); p_1(0,0)=0.39894228 -> 0.3989 (quiz); Phi(-1/sqrt2)=0.2397500611 -> 0.23975 (quiz, tolerance 1e-5); E1 ratio 5.55e-16/3.81e-29 = 1.4567e13 -> 1.5e13 to two significant figures (basis: printed three-figure values); E2 printed 1.0000000000 supports |error|<=5e-11; E3 |gap|/eps = 1.374 ~ 1.4.")
row("b-num-L06", "2.1 numbers in prose re-derived from unrounded values", G + "L06.html:296, 316, 320, 384-400, 436-442, 511", "PASS",
    "recompute_r8.py (" + S + "recompute_r8.txt): erfc(1/sqrt2)=0.3173105079; P(B_1>1)=0.15865525393 -> 0.1586552539 (printed) and half of the printed 0.3173105079 = 0.15865525395 (E3 explanation consistent); 4 dp: P(B_1>=1)=0.1587, 2P=0.3173; exact counts A 1014 triples, B 78 pairs, C 1588 of 4096 and 495 = 495, D 281/512, 11/32, 105/512 (decimals 0.548828, 0.343750, 0.205078), all reproduced by an enumeration written independently of the lab.")
row("b-lab-L04-hypothesis", "2.5 labs: hypothesis states what the lab prints and checks", G + "L04.html:147 (hypothesis of Lab 1)", "PASS",
    "Hypothesis: t=2, theta in {-1, 0.5, 2}, quadrature to relative 1e-9 (code tolerance TOL*closed, L04.html lines 207) and absolute 1e-9 for E[Z_t] (L04.html line 208), via Lemma 2.1 with h=t. Matches the code (THETAS, TIME, TOL). Observation, not a row failure: the sentence attributes E[Z_t]=1 to 'Proposition 2.4 at s=0' without restating Proposition 2.4's hypotheses (Assumptions 4.1 and 4.2); the lab itself is numerical.")
row("b-lab-L04-interpretation", "2.5 labs: interpretation names only what the printed numbers show", G + "L04.html:224", "PASS",
    "The interpretation names the printed E[exp(theta B_t)] values 2.718281828, 1.284025417, 54.598150033 as e^1, e^(1/4), e^4 (verified in recompute_r8.txt) and the printed E[Z_t]=1.000000000 (expected block lines 218-223). It states the check uses t=2 and three theta values and does not prove other cases.")
row("b-lab-L04-docstring", "2.5 labs: docstring claims match the code", "tests/labs/SC1/lab-SC1-L04-1.py lines 1-14, 148-162", "PASS",
    "Docstring: 'Numerical, not simulated. Nothing is random and nothing is read from a file'; code has no random module import and no file read (L04.html lines 164-173); composite Simpson with PANELS panels on [-LIMIT, LIMIT] (lines 181-198); 'lab does not compute the mass beyond LIMIT' matches the code.")
row("b-lab-L05-docstring-quadrature", "2.5 labs: docstring and card agree with the printed gaps", "tests/labs/SC1/lab-SC1-L05-1.py lines 1-9 (docstring); cards SC1-c091, c092", "PASS",
    "Docstring: 'the gaps are at the scale of double-precision rounding, not exact values' matches the printed largest gap 5.55e-16 (expected block line 255). Observation: an independent Simpson run at 20000 intervals (recompute_r8.txt) gives a worst gap 2.7e-15, so the printed magnitude depends on INTERVALS=2000 and the summation order; the page quotes only the printed output, so no claim fails.")
row("b-lab-L05-hypothesis-interpretation", "2.5 labs: hypothesis and interpretation match code and output", G + "L05.html:169 (hypothesis), 262 (interpretation)", "PASS",
    "225 cases = 3*3*5*5 (code TIMES, POINTS loops; expected line 254); tolerance 1e-6 (code TOLERANCE); 'mass for 12<=|z|<=40 is far below the largest gap': 3.81e-29 vs 5.55e-16 (line 257); integrals equal 1 to ten printed digits (lines 259-261); 'the printed digits show no error larger than 5e-11' follows from the rounding of 1.0000000000 (E2). The interpretation's 'about 2.5 times the machine epsilon' is 5.55e-16/2.22e-16=2.5.")
row("b-lab-L06-claims", "2.5 labs: hypothesis and interpretation match code and output", G + "L06.html:186 (hypothesis), 297 (interpretation)", "PASS",
    "Part A: 1014 triples with b in [-N, a-1], all equal (expected line 281); Part B: 78 pairs, all equal (line 284); Part C: 1588 of 4096 with M_12>=3, 495 with M_12>=3 and S_12=2, 495 with S_12=4 (lines 286-288); Part D: 281/512, 11/32, 105/512 and the equality True (lines 290-293); Part E: erfc(1/sqrt2) and half (lines 295-296). The hypothesis says 'N from 1 to 12' and the code uses MAX_N=12 (line 208).")
row("b-lab-L06-docstring-exact-fraction", "2.5 labs: docstring claims match the code", "tests/labs/SC1/lab-SC1-L06-1.py lines 1-16, 187-199", "PASS",
    "Docstring: 'enumerates all 2**N step sequences for each N from 1 to 12' matches summaries() (itertools.product over (1,-1) repeat n, line 223); 'every count is an exact integer and every probability in Parts A to D is an exact fraction' matches Fraction use in Part D (lines 265-267); Part E is floating point (math.erfc, line 274), as the docstring says.")
row("b-math-L04-lemma-2.1", "2.1 mathematics: Lemma 2.1 derivation", G + "L04.html:80-90", "PASS",
    "Completing the square: theta*y - y^2/(2h) = theta^2 h/2 - (y - theta h)^2/(2h); expanding the right side gives theta^2 h/2 - y^2/(2h) + theta y - theta^2 h/2, equal to the left side. The shifted density integrates to 1, so E[e^{theta Y}] = e^{theta^2 h/2}.")
row("b-math-L04-prop-2.2", "2.1 mathematics: Proposition 2.2 with its hypotheses", G + "L04.html:92-106", "PASS",
    "Statement lists H1 (B standard BM, F_t satisfies Assumption 4.1) and H2 (Assumption 4.2) and concludes 'assuming Assumptions 4.1 and 4.2'. Proof: (ii) E[B_t^2]=t by (D2); (iii) E[B_t | F_s] = B_s + E[Y | F_s] by 4.2(a),(c), with E[Y|F_s]=E[Y]=0 by 4.1 and 4.2(d) and (D2).")
row("b-math-L04-prop-2.3", "2.1 mathematics: Proposition 2.3", G + "L04.html:108-124", "PASS",
    "E[(B_t^2-t)^2] = 3t^2 - 2t^2 + t^2 = 2t^2 (recompute_r8.txt: ratio 2 at t=1,2,3), using E[B_t^4]=3t^2 (Lemma 2.2 of L03). Conditional step: E[B_t^2 | F_s] = B_s^2 + h with h=t-s, so E[B_t^2 - t | F_s] = B_s^2 - s (line 122). Hypotheses stated and used.")
row("b-math-L04-prop-2.4", "2.1 mathematics: Proposition 2.4", G + "L04.html:128-143", "PASS",
    "E[Z_t^2] = e^{-theta^2 t} E[e^{2 theta B_t}] = e^{-theta^2 t} e^{2 theta^2 t} = e^{theta^2 t} (Lemma 2.1 with 2 theta). W=exp(theta Y - theta^2 h/2): E[W^2] = e^{theta^2 h} and E[W]=1, checked by Simpson in recompute_r8.txt (residuals ~1e-14). 4.2(c) pull-out and 4.1 with 4.2(d) for E[W|F_s]=E[W] are cited and their hypotheses named.")
row("b-math-L04-A4.1-sketch", "2.1 sketches name the steps they skip", G + "L04.html:65", "PASS",
    "The sketch is labelled 'Sketch, not a proof'. It names the two skipped steps: that the cylinder sets form a pi-system generating F_s, and the pi-lambda extension The parenthetical is the pi-lambda theorem and is correct.")
row("b-math-L04-misconception-1", "2.1 misconception: X_t=B_t^3 computation", G + "L04.html:241", "PASS",
    "(B_s+Y)^3 = B_s^3 + 3 B_s^2 Y + 3 B_s Y^2 + Y^3; with E[Y]=E[Y^3]=0 (symmetric normal, D2) and E[Y^2]=t-s, E[X_t|F_s] = B_s^3 + 3(t-s) B_s, which differs from X_s=B_s^3 iff B_s != 0 (t>s). Hypotheses 4.1, 4.2(a),(c),(d) named.")
row("b-math-L04-R1-R3", "2.1 mathematics: research problems R1-R3 solutions", G + "L04.html:339, 346, 353", "PASS",
    "R1: B_t^2-g(t) = (B_t^2-t) + k(t), k(t)=t-g(t) deterministic; martingale iff k is, and a deterministic martingale is constant (4.2(c) and condition (iii)), so g(t)=t+c. R2: E[Z_t | F_s] = Z_s e^{c^2 h/2}, equal to Z_s iff c=0 (Lemma 2.1). R3: conditional mean t-s, conditional mean of the increment 0. All correct.")
row("b-prose-L04-R2-title", "2.4 prose: problem titles match solutions", G + "L04.html:343-346", "PASS",
    "Title 'When the exponential exp(cB_t) is a martingale' matches the solution, which concludes c=0.")
row("b-prose-L04-remark-numbering", "2.4 prose: remark and cross-reference numbering", G + "L04.html:37, 126", "PASS",
    "The remark at line 126 is unnumbered and is referenced by name in the lesson's meta row (line 37, 'in the remark after Proposition 2.3'); no numbered reference is broken.")
row("b-scope-L04-footer", "2.4 scope of the footer claim", G + "L04.html:479", "PASS",
    "Footer: 'Propositions 2.2 to 2.4 are proved on the page from Assumptions 4.1 and 4.2, which are stated and not proved here'. Proofs of 2.2-2.4 use only 4.1, 4.2 and (D1)-(D3)/Lemma 2.1 (checked in the proof text).")
row("b-math-L05-lemma-1.3", "2.1 mathematics: Lemma 1.3 proof (independence of the future increment)", G + "L05.html:94-101", "PASS",
    "Partition 0=r_0<...<r_k=s<t is admissible in (D3); B_{r_j} are functions of Delta_1..Delta_k (B_0=0); A4(f) groups them; the cylinder events form a pi-system generating F_s (closed under intersection by merging time sets, and enlarging the set of times does not change an event), so A4(a) gives independence. Case s=0 and s=t handled. Statement 'Assuming A4(a) and A4(f)' matches.")
row("b-math-L05-thm-1.4", "2.1 mathematics: Theorem 1.4 (Markov property at fixed times) and its statement", G + "L05.html:104-122", "FAIL",
    "Proof is correct: A4(b) with Z=B_s, Y=B_t-B_s, f(z,y)=g(z+y) gives E[g(B_t)|F_s]=E[g(z+B_t-B_s)] at z=B_s, and the substitution y=z+w gives p_{t-s}. The defect is in the statement, line 110: 'Assuming A4(a), A4(b) and A4(f) (the last two through Lemma 1.3)'. The 'last two' are A4(b) and A4(f), so the parenthetical says A4(b) is used through Lemma 1.3. It is not: the proof applies A4(b) directly (line 119), and A4(a) and A4(f) are the parts used through Lemma 1.3 (Lemma 1.3 assumes A4(a) and A4(f), line 92).",
    "Replace the parenthetical at L05.html:110 with '(A4(a) and A4(f) through Lemma 1.3, and A4(b) directly)'. No other change is needed.")
row("b-math-L05-lemma-2.2-thm-2.1", "2.1 mathematics: Lemma 2.2 and Theorem 2.1", G + "L05.html:133-165", "PASS",
    "Lemma 2.2 identity: multiplying by uv, both sides expand to (u+v)z^2 - 2(vx+uy)z + vx^2 + uy^2 after the constant terms are matched; (u+v)(vx^2+uy^2) - (vx+uy)^2 = uv(y-x)^2 checked symbolically; recompute_r8.txt: identity holds on a grid. Theorem 2.1: Gaussian integral of e^{-c(z-m)^2/2} = (2 pi uv/(u+v))^{1/2}, and the powers of 2 pi and uv cancel to p_{u+v}. CK gap by independent Simpson: 2.7e-15 (recompute_r8.txt).")
row("b-math-L05-A3-sketch", "2.1 sketches name the steps they skip", G + "L05.html:280", "PASS",
    "Sketch labelled 'Sketch, not a proof'. Names the skipped steps (i) the extension from finitely many increments to the whole path via A4(a) and the pi-system of cylinder events, and (ii) the limit passage in E[f(X^(n)) 1_A] for A in F_rho, which needs A cap {rho_n=q} in F_q. Statement 'Problem R3 shows rho <= rho_n <= rho+2^-n' is consistent with R3 (strict on the right).")
row("b-math-L05-R3", "2.1 mathematics: Problem R3 (dyadic approximation from above)", G + "L05.html:403-405", "PASS",
    "x <= ceil(x) < x+1 with x=2^n rho gives rho <= rho_n < rho+2^-n. {rho_n<=r} = {rho <= k/2^n} with k = floor(2^n r), using ceil(2^n rho) <= m iff 2^n rho <= m for integer m; {rho <= k/2^n} lies in F_{k/2^n} subset F_r. Correct.")
row("b-math-L05-problems", "2.1 mathematics: problem set solutions M1-M3, P1-P3, R1-R2, E1-E3", G + "L05.html:315-408", "PASS",
    "M1: integral = 1/(2 sqrt pi) = p_2(0,0) (recompute_r8.txt). M2: psi_2=x^2+2, psi_3=x^3+6x (Z~N(0,2)). M3: Cov(B_2-B_1,B_1)=0, joint normality and A1(c). P1: Lemma 2.2 at u=1,v=3,x=0,y=1 gives (4z^2-2z+1)/3 on both sides, m=1/4, (u+v)/(uv)=4/3. P2: Phi((c-x)/sqrt(t-s)). P3: substitution gives (2 pi)^{-1/2} * integral = 1. E1/E2/E3 numbers verified. R1: a path-wise argument with A4(d), counterexample checked by hand (values 1/4 and 3/4). R2: deterministic time with F_s subset F_rho.")
row("b-math-L05-misconceptions", "2.1 misconceptions: L05 section 5", G + "L05.html:296-307", "PASS",
    "Misconception 1: conditional law N(B_s, t-s) under the stated assumptions (P2), mean B_s depends on the past. Misconception 2: p_{t-s}(x,.) = marginal of B_t only when x=0 and s=0 (N(x,t-s)=N(0,t) forces x=0 and t-s=t). Misconception 3: 225 points is not a proof; Theorem 2.1 holds for all u,v>0, x,y.")
row("b-scope-L05-D1D3", "2.4 scope: the list of facts used in Sections 1 and 2", G + "L05.html:56", "PASS",
    "Grep of A4 labels in Sections 1-2 (lines 56-165): A4(a), A4(b), A4(f) in Lemma 1.3 and Theorem 1.4; A4(e) in Theorem 2.1; (D1)-(D3) in Lemma 1.3 and Remark 1.5. A4(c), A4(d), A4(g), A4(h) appear only in Section 3 and Proposition 2.3 of L06. The sentence at line 56 is accurate.")
row("b-notation-L05-Phi-varphi", "2.3 notation: Phi and the Gaussian density symbols against notation/notation.json", G + "L05.html:120, 348, 350, 498; notation/notation.json", "PASS",
    "notation.json lists '\\Phi, \\Phi^{-1}' as the standard normal CDF and its inverse; the page uses \\Phi only as the standard normal CDF (lines 348, 350, 498). \\phi_u is the Gaussian density, which plan 2.3 permits (\\varphi for the density). \\Normal is registered.")
row("b-notation-L05-X-n", "2.3 notation: local symbols defined before use", G + "L05.html:274-280", "PASS",
    "X_r is defined at line 275 (A3's conclusion) before the sketch; X^(n)_r is defined at line 280 in the sketch where first used, and rho_n is defined in the same sentence.")
row("b-notation-M-clash", "2.3 notation: M used for two processes", G + "L04.html, L05.html, L06.html", "PASS",
    "M_t and M_N denote the running maximum only in L06 (Lemma 2.1, Proposition 1.3). No M is used for another object in the slice. 'M6' in prose is the module code.")
row("b-quiz-L05-Q7", "2.4 quiz: correct option and explanation", G + "L05.html:478-484", "PASS",
    "Correct option names the two skipped steps of the A3 sketch (extension of independence to the whole shifted path; limit passage in E[f(X^(n)) 1_A]), which match L05:280. The explanation says the sketch 'proves the fixed-time case, sums over the countably many values of the dyadic approximation, and then names two skipped steps', which matches the sketch.")
row("b-scope-L05-canonical", "2.4 scope: the canonical path space used in R1", G + "L05.html:389", "PASS",
    "Text: 'Take Omega to be the space of continuous paths with B the coordinate process, a choice made for this problem only'. The restriction is stated and the argument uses only A4(d).")
row("b-term-almost-surely", "2.5 terms defined at first use", G + "L05.html:62 (first use), 75, 99", "PASS",
    "L05:62 (A4(b)) defines 'almost surely (that is, with probability one)' at first use; later uses (lines 75, 120) follow it.")
row("b-scope-L05-E1-tail", "2.1 E1 claim and rounding basis", G + "L05.html:365-367 (E1)", "PASS",
    "5.55e-16/3.81e-29 = 1.4567e13 (recompute_r8.txt), printed as 1.5e13 to two significant figures; basis: the printed values, each to three significant figures (the ratio lies in [1.4536e13, 1.4600e13]). The truncation conclusion is limited to |z| in [12,40] and states that |z|>40 is not computed.")
row("b-math-L06-facts-unnumbered", "2.1 unnumbered facts in the Proposition 2.3 proof", G + "L06.html:102, 135-144", "PASS",
    "The proof names A4(c) (hitting time is a stopping time), A4(h) (measurability at rho), A4(g) (joint measurability), A4(b) (freezing with G=F_rho), A3 (X is BM independent of F_rho) and the symmetry of N(0,u). Each is named where used. The intermediate value theorem appears in Lemma 2.1 and is handled as a classical theorem (see b-ivt-observation).")
row("b-math-L06-prop-1.3-cor-1.4", "2.1 mathematics: Proposition 1.3 and Corollary 1.4", G + "L06.html:76-98", "PASS",
    "Reflection after the first visit to a maps {kappa<=N, S_N=b} bijectively onto {kappa<=N, S_N=2a-b}; for b<a, S_N=2a-b > a so every sequence with S_N=2a-b has kappa<=N, so the second set is {S_N=2a-b}. Corollary 1.4 via b -> 2a-b mapping integers below a onto integers above a. Checked by exact enumeration (recompute_r8.txt, A and B).")
row("b-math-L06-lemma-2.1", "2.1 mathematics: Lemma 2.1 (i)-(iii)", G + "L06.html:104-115", "PASS",
    "(i) M_t >= a gives s* <= t with B_{s*} >= a > 0 = B_0, IVT gives tau_a <= s* <= t; converse by closedness of {s: B_s=a}. (ii) IVT on [0,t]. (iii) if B_s > a for some s <= t then IVT gives a time in (0,s) with B=a, contradicting tau_a > t; so B_s <= a and B_t != a, B_t < a. All correct under continuity and B_0=0.")
row("b-math-L06-prop-2.3-thm-2.5", "2.1 mathematics: Proposition 2.3 and Theorem 2.5", G + "L06.html:122-171", "PASS",
    "Prop 2.3: rho=tau_a wedge t is a bounded stopping time (A4(c), closed set {a}); W_t = B_t on {tau_a>t}, 2a-B_t on {tau_a<=t}; A3 gives X=B_{rho+.}-B_rho BM independent of F_rho; A4(b) with f_-=g(x-y_u), f_+=g(x+y_u); symmetry of X_u gives h_-=h_+; law of W_t equals law of B_t. Theorem 2.5: E = {tau_a<=t, B_t<a} = {W_t > a} by Lemma 2.1(iii); P(W_t>a)=P(B_t>a) by Prop 2.3; no atom at a. All hypotheses named in the statements.")
row("b-math-L06-cor-2.6", "2.1 mathematics: Corollary 2.6 substitution", G + "L06.html:173-182", "PASS",
    "Substitution z = sqrt2 w: (1/sqrt(2pi)) * sqrt2 * int_{a/sqrt(2t)}^inf e^{-w^2} dw = (1/sqrt pi) int ...= (1/2) erfc(a/sqrt(2t)); times 2 gives erfc(a/sqrt(2t)). Numerically erfc(1/sqrt2)=0.3173105079 (recompute_r8.txt).")
row("b-math-L06-R1-R3", "2.1 mathematics: research problems R1-R3", G + "L06.html:406-426", "PASS",
    "R1: S_N has the parity of N; both sides vanish when b and N differ in parity; the proof uses no parity. R2: B'=-B is a standard BM with continuous paths (D1-D3 preserved under sign change); min B <= -a iff max B' >= a; Theorem 2.5 gives 2P(B'_t>a)=2P(B_t<-a). R3: 2x > x for x=P(B_t>=a)>0 and positivity of the normal tail. Correct.")
row("b-math-L06-E1-E3", "2.1 mathematics: L06 empirical problems E1-E3", G + "L06.html:384-400", "PASS",
    "E1: 1+...+12 = 78 pairs; the code does not check a>N (lab lines 233 and 246). E2: 281/512 - 11/32 = 105/512 = P(S_10=2) = C(10,6)/1024 (recompute_r8.txt). E3: halving 0.3173105079 gives 0.15865525395; the unrounded half 0.15865525393 prints as 0.1586552539 (recompute_r8.txt).")
row("b-scope-L06-only-events", "2.4 scope: 'need the path only on [0,t]'", G + "L06.html:102", "PASS",
    "Lemma 2.1 uses the path on [0,t]; Proposition 2.3 uses rho=tau_a wedge t <= t and X_{t-rho} with t-rho in [0,t]; Theorem 2.5 uses the Proposition and Lemma 2.1 only. The sentence is consistent with the proofs.")
row("b-scope-L06-N12-every-case", "2.4 scope: 'every case' claims against the enumeration domain", G + "L06.html:186, 194, 296-297, 441-442", "PASS",
    "Lab claims are limited to N<=12 and 1<=a<=N (line 297: 'the cases the code enumerates'; key-results row 442). The 'every' in line 186 refers to every 2^N step sequence for N=1..12 (code loops over n in range(1, MAX_N+1)).")
row("b-rounding-L06-misconception", "2.1 rounding of printed values", G + "L06.html:316", "PASS",
    "0.3173105079 rounds to 0.3173 and P(B_1>=1)=0.15865525393 rounds to 0.1587 at four decimal places (recompute_r8.txt: round(...,4)).")
row("b-plan-L06-pathlevel", "2.6 plan deviation recorded, not silent (plan section 3 L06 says the reflected path is a BM, Assuming A3)", G + "L06.html:119 (Definition 2.2), 149 (Remark 2.4)", "PASS",
    "The page states that the path-level claim is not proved (line 119, Definition 2.2) and Remark 2.4 says it is not used and not claimed (line 149). This is a recorded deviation from plan section 3, not a silent one. Observation outside the slice: plans/SC1-open-items.md:3-9 still says the claim is 'labelled as a conjecture of that page', which the current L06 Definition 2.2 no longer says; the file was not edited.")
row("b-causal-L06-symmetry-last-step", "2.7 causal claim: symmetry used at h_- = h_+ (last step)", G + "L06.html:306 (canon break), 141-144 (proof)", "PASS",
    "The claim 'symmetry of N(0,u) is used at the step h_- = h_+' matches the proof at L06:144 (h_-(x,u)=h_+(x,u) because -X_u has the same law as X_u).")
row("b-quiz-L04-Q8-explain", "2.4 quiz: explanation of the B_t+t item", G + "L04.html:432-438", "PASS",
    "Correct option 'No: its conditional expectation is B_s + t, which is not B_s + s'; explanation cites Problem P1 and states E[X_t|F_s]=B_s+t differs from X_s=B_s+s for s<t. Matches P1 (L04:289).")
row("b-quiz-L04-L06", "2.4 quiz: item counts, explanations, numeric answers and tolerances", G + "L04.html:376-464, L05.html:427-510, L06.html:449-531", "PASS",
    "Item counts: L04 11, L05 10, L06 10 (8-15 required). Numeric answers and tolerances re-derived: L04 E[B_3^2]=3 (tol 0), E[B_3^4]=27 (tol 0), e (tol 1e-9; gap 4.6e-10), e^4 (tol 1e-9; gap 1.4e-10); L05 3 (tol 1e-4), p_1(0,0)=0.39894 for 0.3989 (tol 1e-4), Phi(-1/sqrt2)=0.2397500611 for 0.23975 (tol 1e-5); L06 P(M_2>=2)=0.25 (tol 1e-4), erfc(1/sqrt2)=0.31731 for 0.3173 (tol 1e-4), P(B_1>=1)=0.15865 for 0.1587 (tol 1e-4). All explanations match the lesson text.")
row("b-plan-coverage-L04-L05", "2.9 lesson content plan coverage (plan section 3)", G + "L04.html, L05.html, L06.html", "PASS",
    "L04: filtration, continuous-time martingale definition, B_t and B_t^2-t, exponential martingale with E[Z_t^2]=e^{theta^2 t} (T), optional stopping not used. L05: Markov property, Gaussian transition density, Chapman-Kolmogorov (T), strong Markov property as numbered A3 with sketch. L06: discrete reflection (exact, Lab 1), fixed-time reflection of the Brownian path under A3, P(M_t>=a)=2P(B_t>=a), path-level claim stated and not proved (recorded deviation).")
row("b-hours-L04-L06", "2.2 hours arithmetic", G + "L04.html:2, L05.html:2, L06.html:2; index.html", "PASS",
    "data-hours=9 on L01-L08 (grep); index data-hours-lessons=72 and data-hours-project=28 (" + S + "dag_names_and_hours_r8.txt); 8 x 9 = 72; 72 + 28 = 100 = the curriculum figure.")
row("b-dag-D1-D9", "2.9 DAG: plan section 4 out-of-closure names used by slice pages", G + "L04.html, L05.html, L06.html", "PASS",
    "check_dag SC1 PASS. Grep of the slice prose (outside pre blocks) for the D1-D9 names (Ito, SDE, Euler/Milstein, Girsanov, Feynman-Kac, Kolmogorov equations, Poisson, Levy, Black-Scholes, barrier, Monte Carlo, bias-variance, Donsker, LIL, change of measure): zero hits (" + S + "dag_names_and_hours_r8.txt). 'stopping time', 'martingale', 'filtration' are in the closure via M6.")
row("b-process-words", "2.12 learner text: no process words", G + "L04.html, L05.html, L06.html; cards.json", "PASS",
    "prose_scan_r8.py (" + S + "prose_scan_r8.txt): process-word pattern (build, builder, round, verifier, ledger, agent, audit, TODO, TBD, pending) finds no hit in L04 or L06 prose and in the 83 slice cards. L05 has one hit for 'rounds' in 'The printed value rounds to ten decimal places' (ordinary usage, not a process word).")
row("b-cards-c061-c072", "2.10 cards: agree with the current lesson text (L04 cards c061-c072)", G + "cards.json (SC1-c061 to SC1-c072)", "PASS",
    "All 12 cards re-read against L04:57-75, 80-90, 92-106, 108-124, 128-143 and the lab text (ledgers/SC1/scripts/SC1-b-r8/cards_L04_06.txt). Hypotheses match each Proposition (H1, H2). c072's numbers match the printed lab values.")
row("b-cards-c073-c085", "2.10 cards: agree with the current lesson text (L04 cards c073-c084, c085 absent)", G + "cards.json (SC1-c073 to SC1-c082, c202-c204)", "PASS",
    "Cards c073-c082 re-read against L04:230-251, 254-300, 300-355, 360-374. c085 is absent (a gap, no text removed). c076 and c077 match the misconception text (L04:241, 245); c079 now uses k(t) and matches R1 (L04:339). c081-c082 match P2 and P3 with their hypotheses.")
row("b-cards-c086-c097", "2.10 cards: agree with the current lesson text (L05 cards c086-c097)", G + "cards.json (SC1-c086 to SC1-c097)", "PASS",
    "c086 (Lemma 1.3, A4(a) and A4(f)), c087 (Theorem 1.4; hypotheses 'standard BM, Lemma 1.3, A4(b)' match the Theorem's own list at L05:107-108), c088 (Remark 1.5; changed this round, now 'Assuming A4(a), A4(b) and A4(f)' and consistent with the remark), c089-c090 (Lemma 2.2, Theorem 2.1), c091-c092 (lab numbers), c093-c097 (A3, stopping time, R2, R3, R1 with A4(d)). Re-read at L05:62-98, 103-165, 265-290, 296-307, 331-405.")
row("b-cards-c098-c110", "2.10 cards: agree with the current lesson text (L05 cards c098-c105, L06 cards c106-c110)", G + "cards.json (SC1-c098 to SC1-c110)", "PASS",
    "c098 (B-tilde not covered by A3), c099 (unbounded time not covered), c100 (changed this round to 'Assuming A4(a), A4(b) and A4(f)'; matches L05:297), c101-c102, c103-c105 (M2, P2, M3). L06 cards c106-c110 (SRW, reflected walk, Lemma 1.2, Proposition 1.3, Corollary 1.4) match L06:56-98.")
row("b-cards-c111-c122", "2.10 cards: agree with the current lesson text (L06 cards c111-c122)", G + "cards.json (SC1-c111 to SC1-c122)", "PASS",
    "c111 (1014 triples), c112 (78 pairs, 1+2+...+12), c113 (281/512, 11/32, 105/512), c114 (495, 495, 2a-b=4), c115 (erfc(1/sqrt2) = 0.3173, Theorem 2.5 and Corollary 2.6), c116-c118 (Lemma 2.1 (i)-(iii)), c119 (changed this round; now 'Only the fixed-time form (Proposition 2.3, under A3 and A4 of Lesson 5) is established', matching L06:119), c120-c122 (Prop 2.3, explicit form, Remark 2.4).")
row("b-cards-c123-c133", "2.10 cards: agree with the current lesson text (L06 cards c123-c133)", G + "cards.json (SC1-c123 to SC1-c133)", "PASS",
    "c123 (Theorem 2.5), c124 (Corollary 2.6), c126 (misconception, 0.3173 vs 0.1587), c127 (105/512), c128 (round-6 FAIL closed earlier; matches L06:306-307 and Section 4), c129 (M1), c130 (R1), c131 (R2), c132 (R3), c133 (bounded rho = t; finiteness not used). Re-read against L06:56-182, 184-298, 300-327, 336-426.")
row("b-cards-duplicates", "2.10 cards: no duplicate cards, every card id unique", G + "cards.json (all 193 cards)", "PASS",
    "prose_scan_r8.py (" + S + "prose_scan_r8.txt): 193 cards, 0 duplicate ids, 0 duplicate fronts. The lesson-level counts changed this round (c055 and c166 removed, c205 added in other lessons); none of the slice cards duplicate another.")
row("b-cards-c193-c204", "2.10 cards: new cards added in the delta agree with their lesson text", G + "cards.json (SC1-c193 to SC1-c200, c202 to c204)", "PASS",
    "A4(a)-(h) cards match L05:61-68 item by item (A4(e) integral; A4(h) measurability at rho<=c, 'defined in Section 3'). A4 cards are assumed, not proved, and say so. SC1-c204 states Assumption 4.2(d) with 'h(Y)'; the lesson's 4.2(d) now uses 'f' (L04:70, changed this round). The content is identical; renaming the card's symbol to f is an optional consistency edit, not a defect.")
row("b-math-L05-def-1.1-st-case", "2.1 mathematics: Definition 1.1 covers s=t", G + "L05.html:75, 121", "PASS",
    "Definition 1.1 states 0<=s<=t, and L05:121 proves the s=t case with psi=g, which is the case the Theorem's statement (0<=s<t) excludes.")
row("b-hyp-L06-102-lesson2-hypotheses", "2.6 cross-lesson hypotheses: Lesson 2 results cited at L06:102 carry the hypotheses the page states", G + "L06.html:102; L02.html:289-318", "PASS",
    "L06:102 states the Lesson 2 hypotheses: A2 and Assumption 2.1 for Theorem 2.5 (L02 H2), and A1(a), A1(b), A1(e), A2 and Assumption 2.1 for Remark 2.6 (L02 H2). Observation: Theorem 2.5 and Remark 2.6 also carry the construction's own hypotheses H1 (coefficients), which are the setting of Lesson 2 and are not restated at L06:102.")
row("b-prose-L05-P3-title", "2.4 prose: problem titles match their problems", G + "L05.html:354-357", "PASS",
    "Title 'Normalisation of the transition density' matches the problem (integral of p_u(x,y) dy = 1) and its solution.")
row("b-prose-L06-P2-title", "2.4 prose: problem titles match their problems", G + "L06.html:366-369", "PASS",
    "Title 'Parts (ii) and (iii) of Lemma 2.1 from continuity' matches the problem and the solution, which prove (ii) and (iii) from continuity without part (i).")
row("b-prose-L04-P3-title", "2.4 prose: problem titles match their problems", G + "L04.html:300-303", "PASS",
    "Title 'The product moment of a martingale at two times' matches E[Z_s Z_t]=E[Z_s^2].")
row("b-math-degenerate-L04-lemma-2.1", "2.1 mathematics: Lemma 2.1 hypothesis h>0 is respected where applied", G + "L04.html:82, 140-142", "PASS",
    "Lemma 2.1 is applied with h = t-s > 0 in the s<t case (L04:140-142). The s=t case of Proposition 2.4 is handled separately by the last sentence of Assumption 4.2 (L04:140).")
row("b-delta-L04-L06-hunks", "2.8 delta: every changed hunk in L04-L06 read and re-derived (delta 06994db..0dee921)", G + "L04.html (16 changed lines), L05.html (18 changed lines), L06.html (4 changed lines)", "FAIL",
    "Every hunk read in full and re-derived (diff of 06994db..0dee921): L04 Assumption 4.1 sketch (pi-lambda parenthetical, correct); L04 Assumption 4.2(d) h->f (consistent); L04 lab interpretation (correct); L04 canon-break drift (correct); L04 misconception 2 (correct); L04 problem-set intro (correct, see b-l04-problem-set-E-intro); L04 M2 solution (FAILS, see b-prob-L04-M2-hypothesis); L04 M3 (correct); L05 why-it-matters (correct); L05 Theorem 1.4 statement (FAILS, see b-math-L05-thm-1.4); L05 misconception 1 and M2, P2 solutions (correct); L05 E1, E3 solutions (correct); L05 key-results row (correct); L05 quiz q10 (correct); L06 why-it-matters (correct); L06 quiz q8 explanation (correct).",
    "Fix the two hunks named in b-prob-L04-M2-hypothesis and b-math-L05-thm-1.4; every other hunk is correct.")
row("b-delta-cross-lessons", "2.8 delta in lessons cited by the slice (L01, L02, L03, L08, index) read for cross-references", G + "L01.html, L02.html, L03.html, L08.html; index.html", "PASS",
    "The delta changed L01 (the 'Standard' remark and two canon-break items), L02 (2 lines), L03 (8 lines) and L08 (the Uses line and wording). Every cross-reference used by L04-L06 (D1-D3, Proposition 1.2, A1(a),(b),(c),(e) of L01; Theorem 2.5, Remark 2.6, A2 and Assumption 2.1 of L02; Lemma 2.2 and Assumption 3.2(a) of L03; Corollaries 1.3 and 1.4 of L08) still names the same statement.")
row("b-delta-twins-and-scripts", "2.8 delta in lab twins and gate scripts", "tests/labs/SC1/lab-SC1-L04-1.py, L05, L06; tools/", "PASS",
    "git diff 06994db..0dee921 touches only tests/labs/SC1/lab-SC1-L07-1.py and L08-1.py under tests/labs/SC1 (see git diff --stat); the three slice twins are byte-identical (sha256 79a56370..., 744046b7..., 8d01822e...). No file under tools/ changed in the SC1 scope.")
row("b-scope-words-r5", "2.4 scope words (every, all, any, only, always, exactly, never) in the slice prose", G + "L04.html, L05.html, L06.html", "PASS",
    "Scope words counted by prose_scan_r8.py (L04 21, L05 53, L06 54). Each scope word in the slice prose was checked against the proof or the enumeration domain; each is backed by the stated proof or enumeration.")
row("b-notation-r5", "2.3 notation: every macro and registered symbol used in the slice", G + "L04.html, L05.html, L06.html; notation/notation.json", "PASS",
    "Macros used by the slice (LaTeX scan, recorded in this round's review): \\E, \\Prob, \\Var, \\Cov, \\R, \\indic, \\Normal, \\Phi (registered); no use of \\dto, \\se or \\emgamma. The registered symbol T is not used anywhere in the slice; no use of R^*, gamma_3, gamma_4, R_f or \\mathbb{Q}.")
row("b-recompute-r5", "2.1 independent recomputation of all printed and quoted numbers (this round)", G + "L04.html, L05.html, L06.html", "PASS",
    "ledgers/SC1/scripts/SC1-b-r8/recompute_r8.py (" + S + "recompute_r8.txt), independent of the lab code, reproduces every printed and quoted number in the slice (see the num-, lab- and quiz rows).")
row("b-verify-refs-r5", "2.1 citation registry live check (this round)", "references/references.json (shreve2004stochastic)", "PASS",
    "tools/verify_refs.py --unit SC1 (live): 1 of 560 entries, 0 problems (" + S + "verify_refs_unit.txt); the record matches the curriculum string (see b-attribution-references).")
row("b-assumed-facts-statement", "2.1 / plan 2.1 item 6 and fixer rule: a result that uses a numbered Assumption says 'Assuming ...' in its statement", G + "L04.html:70, 98, 114, 134, 271, 289, 300-303; L05.html:94, 110, 147, 297, 326, 350; L06.html:127-130, 159", "FAIL",
    "Statements checked: L04 Propositions 2.2-2.4 say 'assuming Assumptions 4.1 and 4.2' (pass); L04 P2 and P3 say 'assuming Assumption 4.2' (pass); L05 Lemma 1.3 'Assuming A4(a) and A4(f)' (pass); L05 Theorem 2.1 'Assuming A4(e)' (pass); L06 Proposition 2.3 and Theorem 2.5 'Assuming A3 and A4' (pass). Two defects of the same kind: L05 Theorem 1.4 names A4(b) as used through Lemma 1.3 (see b-math-L05-thm-1.4), and L04 M2 cites the martingale of Proposition 2.4 under Assumption 4.2 only (see b-prob-L04-M2-hypothesis).",
    "Apply the two fixes named in b-math-L05-thm-1.4 and b-prob-L04-M2-hypothesis.")
row("b-l06-assumption-scope", "2.6 assumption scope: the L06 statement of the main identity names every assumption its theorem uses", G + "L06.html:52, 153-161", "PASS",
    "Theorem 2.5 names A3 (applied in Proposition 2.3) and A4 of Lesson 5, and its proof uses only Lemma 2.1 (i)-(iii) and Proposition 2.3. The why-it-matters sentence names A3 and A4 too.")
row("b-l06-canon-symmetry-attribution", "2.6 causal attribution in the L06 canon-break 'Symmetry' bullet", G + "L06.html:306; proof at L06:170", "PASS",
    "The factor 2 is attributed to adding two events of equal probability (E and {B_t>=a}); the symmetry is attributed to the step h_-=h_+ of Proposition 2.3. Both match the proof of Theorem 2.5 (L06:168-170).")
row("b-causal-L06-remark-2.4", "2.6 causal claims: Remark 2.4 and Definition 2.2 scope", G + "L06.html:119, 149", "PASS",
    "Remark 2.4 states that Proposition 2.3 is a one-time statement and does not show that the whole reflected path is a standard BM. Definition 2.2 says the path-level statement is not asserted from A3 because A3 covers bounded stopping times only. Both consistent with the proofs.")
row("b-ivt-observation", "2.6 unnumbered classical theorem (intermediate value theorem) in Lemma 2.1 and its problem P2", G + "L06.html:104-115, 367-369", "PASS",
    "Observation, not a FAIL (as in rounds 5 to 7): the intermediate value theorem is used by name and is a standard theorem of real analysis, not a claim about a source; no locator or theorem number is attributed to it.")
row("b-r6-delta-hunks", "2.8 delta: every changed hunk of L04-L06, cards.json and the cross-read pages (round-6 carry-over, re-run this round)", G + "L04.html, L05.html, L06.html; cards.json", "PASS",
    "Every hunk of the round-7-to-round-8 delta was read and re-derived; the defects found are the two rows with FAIL status (b-prob-L04-M2-hypothesis, b-math-L05-thm-1.4) and the rows that cite them (b-delta-L04-L06-hunks, b-assumed-facts-statement). This row is PASS for its own check (the card hunks: c079, c088, c100, c119 re-verified; c204 symbol observation only).")
row("b-r6-twin-page-equality", "2.5 labs: page code equals twin; expected block equals twin stdout", G + "L04.html, L05.html, L06.html; tests/labs/SC1/*.py", "PASS",
    "twin_match_r8.py (" + S + "twin_match_r8.txt): 'ALL PASS' (see b-twin-match).")
row("b-r6-run-labs", "2.5 labs (run_labs, page by page)", G + "L04.html, L05.html, L06.html", "PASS",
    "run_labs --unit SC1 --page L04 / L05 / L06: 'run_labs SC1: PASS (1/1)' each, exit 0 (" + S + "run_labs_L0x.txt).")
row("b-r6-page-smoke", "2.9 page_smoke for the three pages (run alone, full run including the figure sweep)", G + "L04.html, L05.html, L06.html", "PASS",
    "page_smoke --unit SC1 --pages L04 L05 L06: 'page_smoke SC1: PASS', exit 0 (" + S + "page_smoke.txt).")
row("b-r6-check-gates", "2.9 check_pages, check_dag, check_projects for SC1", "tools/check_pages.py, check_dag.py, check_projects.py --unit SC1", "PASS",
    "All three: PASS, exit 0 (" + S + "check_pages.txt, check_dag.txt, check_projects_sc1.txt).")
row("b-r6-lint-typecheck-twins", "2.5 labs: ruff check, ruff format --check and mypy on the three twins", "tests/labs/SC1/lab-SC1-L04-1.py, L05, L06", "PASS",
    "ruff check, ruff format --check and mypy --no-incremental: all exit 0 (" + S + "ruff_check.txt, ruff_format.txt, mypy_labs.txt).")
row("b-r6-pytest-tooling", "2.5 tooling pytest (labs, run_labs, page checks)", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
    "pytest on the three files: all passed, exit 0 (" + S + "pytest_tooling.txt). The full repository suite was not run (see notes).")
row("b-r6-verify-refs", "2.1 citations: offline integrity of the whole registry and live check of the unit's entries", "references/references.json (shreve2004stochastic); tools/verify_refs.py", "PASS",
    "--offline: 560 entries, 0 problems, exit 0; --unit SC1 live: 1 of 560 entries, 0 problems, exit 0 (" + S + "verify_refs_offline.txt, verify_refs_unit.txt).")
row("b-r6-recompute", "2.1 numbers in prose and quiz answers recomputed independently (stdlib, Fraction, enumeration, Simpson)", G + "L04.html, L05.html, L06.html", "PASS",
    "ledgers/SC1/scripts/SC1-b-r8/recompute_r8.py (" + S + "recompute_r8.txt). Covers every number in the slice prose and quiz.")
row("b-r6-cards-full-scan", "2.10 cards: full scan of L04-L06 cards (fronts and backs), duplicate scan of all 193 cards", G + "cards.json", "PASS",
    "All 83 slice cards read in full (ledgers/SC1/scripts/SC1-b-r8/cards_L04_06.txt): ids c061-c084, c086-c133, c189, c193-c204 (c085 absent). Duplicate scan: 0 duplicate ids, 0 duplicate fronts (prose_scan_r8.txt).")
row("b-r6-notation", "2.3 notation: every math symbol on the three pages against notation/notation.json", G + "L04.html, L05.html, L06.html; notation/notation.json", "PASS",
    "Symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q: Phi used only with its registered meaning (L05:348, 350, 498); T and the others unused in the slice. Local symbols (h, k, f, W, M, rho, tau, kappa) are defined before use and do not collide with registered meanings.")
row("b-r6-process-words", "2.12 learner text: process words", G + "L04.html, L05.html, L06.html, cards.json", "PASS",
    "No process word in prose, twins or slice cards (prose_scan_r8.txt; see b-process-words).")
row("b-r6-hours", "2.2 hours arithmetic", G + "L04.html:2, L05.html:2, L06.html:2; index.html", "PASS",
    "data-hours 9 on each slice page; index data-hours-lessons=72; 8 x 9 = 72; total 72 + 28 = 100 (see b-hours-L04-L06).")
row("b-r6-open-items-observation", "2.6 plan deviation recorded, not silent (outside the slice; observation only)", "plans/SC1-open-items.md:3-9 versus course/modules/SC/SC1/L06.html", "PASS",
    "Observation, not a row failure: plans/SC1-open-items.md still says the path-level claim is 'labelled as a conjecture' in Definition 2.2. The current L06 Definition 2.2 states the path-level claim as not proved. The open-items file is outside the slice and was not edited.")
row("b-l04-problem-set-E-intro", "2.4 prose: a sentence about what a lab output supports matches the problems it introduces", G + "L04.html:256 (intro sentence) and problems E1-E3 (L04:310-330)", "PASS",
    "The round-7 FAIL is closed. The intro now reads 'Problem E1 uses the output of Lab 1; E2 and E3 ask about values that Lab 1 does not print.' E1 uses the printed 1.284025417 (expected block, L04.html line 220). E2 asks e^8 for E[Z_t^2] and E3 predicts the value at t=4; neither value is printed by the lab (expected block, L04.html lines 218-223, contains only theta in {-1, 0.5, 2} at t=2). The sentence matches the problems.")
row("b-cards-ellipsis", "2.9 banned strings in learner text: ellipsis (BUILDER_RULES 1.3 bans 'an ellipsis standing for omitted content'; plan 2.2 says 'any ellipsis outside code')", "cards.json: SC1-c086 (back), SC1-c106 (back), SC1-c112 (back)", "PASS",
    "prose_scan_r8.txt: the three slice cards carry U+2026 inside plain-text mathematical sequences (0=r_0<...<r_k=s<t; e_1,...,e_N; 1+2+...+12). These are mathematical sequence ellipses, not omitted content, so BUILDER_RULES 1.3 is not breached. The plan's wording 'any ellipsis outside code' is stricter. Judgment call: left for the architect; the slice pages use \\dots inside math and have no ellipsis in prose (scan: 0 hits).")
row("b-cards-c079-c088-c100-c119", "2.10 cards changed this round: agree with the current lesson text", G + "cards.json (SC1-c079, c088, c100, c119)", "PASS",
    "c079 uses k(t)=t-g(t) as the R1 solution does (L04:339). c088 states the hypotheses A4(a), A4(b), A4(f) of Lesson 5, as the remark's proof requires (L05:126). c100 states 'Assuming A4(a), A4(b) and A4(f)', matching the misconception at L05:297. c119 matches L06:119 (fixed-time form under A3 and A4).")
row("b-cards-c103-c104-hypothesis", "2.10 cards: hypotheses against the current problem solutions (M2, P2 of L05)", G + "cards.json (SC1-c103, c104); L05.html:326, 350", "PASS",
    "Card c103 and c104 say 'Assuming A4(b) and Lemma 1.3 of Lesson 5'; the solutions now say 'Assuming A4(a), A4(b) and A4(f)'. The two are equivalent, because Lemma 1.3 holds under A4(a) and A4(f) (L05:92), and the card's wording is Theorem 1.4's own assumption list (L05:107-108). Observation: the card could repeat A4(a) and A4(f) to match the solution.")
row("b-prob-L04-M2-hypothesis", "2.1 mathematics: L04 problem M2 solution cites the martingale of Proposition 2.4 with its hypotheses", G + "L04.html:271 (M2 solution)", "FAIL",
    "The solution says: 'Problem P2 gives this constant expectation for the martingale of Proposition 2.4, assuming Assumption 4.2.' Proposition 2.4 is a martingale only under Assumptions 4.1 and 4.2 (its H1 includes 4.1, L04:131; conclusion at L04:134). Problem P2 needs Z to be a martingale, so P2 applied to this Z needs 4.1 as well. The solution's own direct computation (E[e^{B_2}]=e and E[Z_2]=1 by Lemma 2.1) is correct; only the hypothesis attached to the P2 step is incomplete. Problem M3 (L04:278) was corrected in the same round and states 'Assuming Assumptions 4.1 and 4.2'.",
    "At L04.html:271, change 'assuming Assumption 4.2' to 'assuming Assumptions 4.1 and 4.2'.")

notes = [
    "Round 8 on 0dee921 (pin). Delta 06994db..0dee921 read for every SC1-b file: L04.html (16 changed lines: Assumption 4.1 sketch, Assumption 4.2(d) h->f, Lab 1 interpretation, canon-break drift, misconception 2, problem-set intro, M2, M3), L05.html (18 changed lines: why-it-matters, Theorem 1.4 statement, misconception 1, M2, P2, E1, E3, key-results row, quiz q10), L06.html (4 changed lines: why-it-matters, quiz q8 explanation), cards.json (SC1-c079, c088, c100, c119 in slice; c005, c048, c053, c054, c056, c149, c150, c166, c205 outside). Every hunk was read in full and re-derived.",
    "No row was carried from round 7: every slice file was re-read in full (L04.html, L05.html, L06.html line by line including the lab code and expected blocks; the 83 L04-L06 cards read in full), and all gates were re-run on 0dee921. Round-7 FAIL b-l04-problem-set-E-intro is closed (PASS). Round-7 PASS rows for the Theorem 1.4 and M2 items are superseded by two new FAIL rows (b-math-L05-thm-1.4, b-prob-L04-M2-hypothesis), both introduced by the round-8 delta.",
    "Mutants: none. Slice b has no project grader; lab twins are demonstrations, and mutation testing does not apply (plan 2.1 item 11; FINAL-ARCHITECT-RULINGS 9). The grader and project slices are not in this slice.",
    "Observation (not a FAIL): tests/labs twins are byte-identical to round 7 (sha256 79a56370..., 744046b7..., 8d01822e...). The Chapman-Kolmogorov gap printed in L05 (5.55e-16) depends on INTERVALS=2000 and summation order; an independent 20000-interval run gives 2.7e-15. Both are at double-precision rounding scale, and the page quotes only the printed output.",
    "Observation (not a FAIL): L04 Lab 1 hypothesis (L04.html:147) attributes E[Z_t]=1 to 'Proposition 2.4 at s=0' without restating Proposition 2.4's hypotheses (Assumptions 4.1 and 4.2). The lab is numerical, so the sentence is a reference, not a claim about hypotheses.",
    "Observation (not a FAIL): card SC1-c204 names the independence function h(Y) while Assumption 4.2(d) now uses f (L04.html:70). Cards c103 and c104 say 'Assuming A4(b) and Lemma 1.3', which equals Theorem 1.4's own list. Both are equivalent in content.",
    "Observation (not a FAIL): 3 slice cards (SC1-c086, c106, c112) contain U+2026 inside plain-text mathematical sequences. BUILDER_RULES 1.3 bans an ellipsis standing for omitted content, which these are not; the plan's wording 'any ellipsis outside code' is stricter. Left to the architect.",
    "Observation (not a FAIL): plans/SC1-open-items.md:3-9 still describes the L06 path-level claim as 'labelled as a conjecture of that page'; the current L06 Definition 2.2 says it is not proved. Outside the slice; not edited.",
    "Observation (not a FAIL): L06:102 cites Lesson 2 Theorem 2.5 and Remark 2.6 under A2 and Assumption 2.1 (and A1(a),(b),(e) for the remark), without restating the construction's own hypothesis H1. H1 is the setting of Lesson 2, so the statement is accepted.",
    "Not checked: the full repository gate (ruff and mypy over the whole repo, the full pytest suite, render_curriculum, build_site --check, fetch_data --check, check_pages/check_dag/check_projects --all, verify_refs --unit for other units). Only the slice-scoped commands listed in the rows were run. Shreve (2004) and Karatzas & Shreve (1991) were not read; no passage is attributed to either. The intermediate value theorem is used by name and is not attributed.",
    "Not checked: the Pyodide timing of the three labs (page_smoke reports the twin timings: L04 0.03 s, L05 0.45 s, L06 0.03 s under CPython, all far below the 10 s limit). No browser check beyond page_smoke.",
]

fragment = {
    "unit": "SC1",
    "slice": "b",
    "round": 8,
    "verifier": "independent Haiku verifier, round 8 (slice b: L04-L06 and lab twins)",
    "pin": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3",
    "base": "06994db (round-7 pin); delta 06994db..0dee921 read for every SC1-b file",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE8-SC1-b",
    "scratch": "ledgers/SC1/scripts/SC1-b-r8",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": {
        "rows": len(rows),
        "pass": sum(r["status"] == "PASS" for r in rows),
        "fail": sum(r["status"] == "FAIL" for r in rows),
        "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows),
        "mutants_killed": 0,
        "mutants": 0,
    },
}

with open("ledgers/SC1/SC1-b.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "verdict", fragment["verdict"], fragment["summary"])
