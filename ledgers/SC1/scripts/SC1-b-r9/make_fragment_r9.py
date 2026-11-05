"""Round-9 SC1 slice b fragment writer (L04-L06 and lab twins). Writes ledgers/SC1/SC1-b.json.

Usage (from the checkout root): python3 -I ledgers/SC1/scripts/SC1-b-r9/make_fragment_r9.py
Evidence commands and their outputs are in ledgers/SC1/scripts/SC1-b-r9/ and its out/ directory.
"""
import json
import sys

OUT = "ledgers/SC1/SC1-b.json"
P = "PASS"
F = "FAIL"
R = []


def row(rid, check, location, status, evidence, fix=""):
    R.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# ---- gates (commands run on pin c93dd52; outputs in ledgers/SC1/scripts/SC1-b-r9/out/)
row("b-check-pages", "2.9 structure (check_pages)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", P,
    "tools/check_pages.py --unit SC1 -> 'check_pages SC1: PASS', exit 0 (ledgers/SC1/scripts/SC1-b-r9/out/check_pages.txt).")
row("b-check-dag", "2.9 DAG (check_dag)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", P,
    "tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS', exit 0 (out/check_dag.txt). Independent link review in b-dag-D1-D9.")
row("b-run-labs", "2.5 labs (run_labs, page by page)", "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py", P,
    "tools/run_labs.py --unit SC1 --page L04, L05, L06 -> each 'run_labs SC1: PASS (1/1)', exit 0 (out/run_labs_L04.txt, run_labs_L05.txt, run_labs_L06.txt).")
row("b-twin-match", "2.5 page code == twin; expected block == twin stdout; twin under python -I -W error", "course/modules/SC/SC1/L04.html:150-215, L05.html:172-253, L06.html:199-279; tests/labs/SC1/*-1.py", P,
    "ledgers/SC1/scripts/SC1-b-r9/twin_match_r9.py (python3 -I): L04/L05/L06 page code == twin True; expected == stdout True; exit 0; stderr 0 bytes; markers_left 0; sha256 79a56370..., 744046b7..., 8d01822e... (identical to round 8, out/twin_match_r9.txt, out/twin_sha256_r8.txt). 'ALL PASS'.")
row("b-lab-lint", "2.5 ruff and mypy on the three twins", "tests/labs/SC1/", P,
    "ruff check tests/labs/SC1 -> 'All checks passed!' exit 0; ruff format --check -> '11 files already formatted' exit 0; mypy --no-incremental on the three twins -> 'Success: no issues found in 3 source files' exit 0 (out/ruff_check.txt, ruff_format.txt, mypy_labs.txt).")
row("b-page-smoke", "2.5/2.9 page_smoke: zero console errors, math rendered, no external requests, lab runtime under 10 s", "course/modules/SC/SC1/L04.html, L05.html, L06.html", P,
    "tools/page_smoke.py --unit SC1 --pages L04 L05 L06 -> PASS for each page, 'page_smoke SC1: PASS', exit 0. Lab timings: L04 0.1 s, L05 1.4 s, L06 0.0 s (out/page_smoke.txt).")
row("b-pytest-tooling", "pytest (tooling for labs, run_labs and page checks)", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", P,
    "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q -> all dots, exit 0 (out/pytest_tooling.txt).")
row("b-verify-refs", "2.1 verify_refs (offline and SC1 unit)", "references/references.json", P,
    "verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0; verify_refs.py --unit SC1 -> 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0 (out/verify_refs_offline.txt, verify_refs_unit.txt).")
row("b-attribution-references", "2.1 attribution and registry keys", "course/modules/SC/SC1/L04.html:468, L05.html:515, L06.html:536", P,
    "references/references.json key shreve2004stochastic: title 'Stochastic Calculus for Finance II', 2004, status verified, used_by SC1; matches curriculum SC1 sources[0] (curriculum/curriculum.json, unit SC1). Pages cite it at book level with no locator. Karatzas & Shreve (1991): grep of references/*.json and *.yaml for 'karatzas' returns 0 matches, so 'no admissible registry record' is accurate and nothing is cited to it. Book not read; no passage attributed.")
row("b-cross-L04", "2.9/2.4 cross-lesson references in L04", "course/modules/SC/SC1/L04.html:37, 65, 119, 126, 232", P,
    "L01 (D1)-(D3) and Definition 1.1 (L01.html:58-63); L03 Assumption 3.2(a) (L03.html:71); L03 Lemma 2.2 gives E[X^4]=3 Delta^2 (L03.html Lemma 2.2, re-derived); L03 Theorem 2.3 mean t (L03.html:109); M4 moment-generating function (course/modules/M/M4/L06-L08 mention it); M6 Lesson 8 introduces filtration and martingale (course/modules/M/M6/L08.html header).")
row("b-cross-L05-L06", "2.9/2.4 cross-lesson references in L05 and L06", "course/modules/SC/SC1/L05.html:52, 268, 279, 288; L06.html:102, 127, 305", P,
    "M6 Lesson 9 Definition 9.1 stopping time (course/modules/M/M6/L09.html:59); L01 Section 4 discontinuous B~ (L01.html:216, 234); L02 Theorem 2.5 (H2) 'Assuming A2 and Assumption 2.1', Remark 2.6 (H2) 'Assuming A1(a), A1(b), A1(e), A2 and Assumption 2.1' (L02.html:289-306); L01 A1(a),(b),(c),(d),(e) present; L08 Corollary 1.4 finiteness with probability one (course/modules/SC/SC1/L08.html:87-88).")
row("b-num-L04", "2.2 numbers in L04 prose", "course/modules/SC/SC1/L04.html:218-224, 271, 314, 321, 328, 420, 452", P,
    "e^1=2.718281828, e^(1/4)=1.284025417, e^4=54.598150033, e^8=2980.957987 (6 dp; 10 dp 2980.9579870417), recomputed by ledgers/SC1/scripts/SC1-b-r9/recompute_r9.py (out/recompute_r9.txt). Printed lab lines 218-223 match by twin_match_r9.py.")
row("b-num-L05", "2.2 numbers in L05 prose", "course/modules/SC/SC1/L05.html:263, 368, 375, 382, 399, 458, 499", P,
    "1/(2 sqrt pi)=0.2820947918; (2pi)^(-1/2)=0.39894228 (quiz 0.3989); Phi(-1/sqrt2)=0.2397500611 (quiz 0.23975); E1 ratio 5.55e-16/3.81e-29=1.457e13 (stated 1.5e13 to 2 sf); E2 half-width 5e-11; E3 3.05e-16/2.2e-16=1.37 (stated about 1.4). Recomputed in recompute_r9.py; independent trapezoid run ck_independent_r9.py gives tail mass 3.812e-29 and printed integrals 1.0000000000 (out/ck_independent_r9.txt).")
row("b-num-L06", "2.2 numbers in L06 prose", "course/modules/SC/SC1/L06.html:290-296, 316, 320, 393, 400, 479, 511, 520", P,
    "Independent exhaustive enumeration in recompute_r9.py (itertools.product, n<=12): 1014 triples, 78 pairs, #{M12>=3}=1588, #{M12>=3,S12=2}=495, #{S12=4}=495, P(M10>=2)=281/512, 2P(S10>2)=11/32, P(S10=2)=105/512, difference 105/512 (all as printed). erfc(1/sqrt2)=0.3173105079; half 0.1586552539 (unrounded 0.15865525393). All printed numbers match.")
# ---- lab claims
row("b-lab-L04-hypothesis", "2.5 lab hypothesis matches code and output", "course/modules/SC/SC1/L04.html:147; tests/labs/SC1/lab-SC1-L04-1.py", P,
    "Hypothesis: relative 1e-9 match of E[e^{theta B_t}] to e^{theta^2 t/2} (code: mgf_ok = abs(mgf-closed) <= TOL*closed) and absolute 1e-9 for E[Z_t] = 1 (code: martingale_ok = abs(martingale-1.0) <= TOL). The 'assuming Assumptions 4.1 and 4.2' phrase (round-8 edit) is consistent with Proposition 2.4 at s=0.")
row("b-lab-L04-interpretation", "2.5 lab interpretation names only what is printed", "course/modules/SC/SC1/L04.html:224, 230-232", P,
    "Printed 2.718281828, 1.284025417, 54.598150033 equal e^1, e^(1/4), e^4 (recomputed); E[Z_t] prints 1.000000000 for each theta. Text says three thetas at one time; not a proof for other theta, t. Consistent with code and output.")
row("b-lab-L04-docstring", "2.5 lab docstring matches code", "tests/labs/SC1/lab-SC1-L04-1.py:1-20", P,
    "Docstring 'Numerical, not simulated', 'Nothing is random', 'the lab does not compute the mass beyond LIMIT', 'finite computations ... not a proof' all match code (no random calls; LIMIT=12, PANELS=20000, Simpson on [-LIMIT, LIMIT]).")
row("b-lab-L05-docstring-quadrature", "2.5 lab docstring matches code (quadrature and tail)", "tests/labs/SC1/lab-SC1-L05-1.py:1-14, 214-229", P,
    "Docstring 'mass of the integrand for 12 <= |z| <= 40 is computed and printed' matches tail_mass (Simpson on [12,40] and [-40,-12]). Gap wording 'at the scale of double-precision rounding' matches printed 5.55e-16 (output lines 256-258).")
row("b-lab-L05-hypothesis-interpretation", "2.5 lab hypothesis and interpretation match output", "course/modules/SC/SC1/L05.html:170, 263, 306", P,
    "Hypothesis: gaps at rounding, far below 1e-6; tail mass far below largest gap; integral 1 to ten digits. Output: 'largest gap below the stated tolerance 1e-06: True', tail mass 3.81e-29, gap 5.55e-16, integrals 1.0000000000. Interpretation 'Theorem 2.1 proves the identity for all of them' is a proof reference, not a lab claim.")
row("b-lab-L06-claims", "2.5 lab claims match output", "course/modules/SC/SC1/L06.html:186, 297", P,
    "Prediction and interpretation match output lines 281-296: Part A 1014 of 1014 equal; Part B 78 of 78; Part C 495 and 495 with 2a-b = 4; Part D 281/512, 11/32, 105/512 and difference True; Part E erfc(1/sqrt2) = 0.3173105079 and P(B_1>1) = 0.1586552539.")
row("b-lab-L06-docstring-exact-fraction", "2.5 lab docstring (exact counts and fractions, ranges)", "tests/labs/SC1/lab-SC1-L06-1.py:1-14", P,
    "Docstring 'every count is an exact integer' and Fraction for Part D match code; Parts A-C print integer counts, so 'every probability in Parts A to D is an exact fraction' holds (A-C print no probabilities). 'every integer a with 1 <= a <= N' and 'b >= -N' match range(1, n+1) and range(-n, a).")
# ---- math (round-8 rows re-derived, plus new)
row("b-math-L04-lemma-2.1", "2.4 mathematics: Lemma 2.1 (mgf of a normal)", "course/modules/SC/SC1/L04.html:81-89", P,
    "Completing the square theta y - y^2/(2h) = theta^2 h/2 - (y - theta h)^2/(2h) re-derived; hypothesis h>0 stated; proof correct.")
row("b-math-L04-prop-2.2", "2.4 mathematics: Proposition 2.2 (B is a martingale)", "course/modules/SC/SC1/L04.html:93-105", P,
    "E[B_t|F_s]=B_s via Assumption 4.2(a),(c) and (d) with E Y = 0 (D2); E B_t^2 = t finite; statement 'assuming Assumptions 4.1 and 4.2' at L04:98.")
row("b-math-L04-prop-2.3", "2.4 mathematics: Proposition 2.3 (B_t^2 - t martingale)", "course/modules/SC/SC1/L04.html:109-123", P,
    "E[(B_t^2-t)^2] = 3t^2 - 2t^2 + t^2 = 2t^2 (L04:119); E[B_t^2|F_s] = B_s^2 + h; E[B_t^2 - t|F_s] = B_s^2 - s. Re-derived; hypotheses at L04:111-114.")
row("b-math-L04-prop-2.4", "2.4 mathematics: Proposition 2.4 (exponential martingale)", "course/modules/SC/SC1/L04.html:129-149", P,
    "E[Z_t^2] = e^{-theta^2 t} E[e^{2 theta B_t}] = e^{theta^2 t} (Lemma 2.1 with 2 theta); E[W^2] = e^{theta^2 h} and E[W] = 1 with W = exp(theta Y - theta^2 h/2) re-derived; Z_t = Z_s W identity re-derived; hypotheses at L04:131-134.")
row("b-math-L04-A4.1-sketch", "2.4 Assumption 4.1 sketch (names skipped steps)", "course/modules/SC/SC1/L04.html:65", P,
    "Labelled 'Sketch, not a proof'; names the pi-system and pi-lambda steps as skipped; cites L03 Assumption 3.2(a) (L03.html:71) for single-variable functions. The block grouping step is named as a standard fact the sketch does not prove (not numbered; observation only, see notes).")
row("b-math-L04-misconception-1", "2.4 misconception 1 (mean zero is not a martingale)", "course/modules/SC/SC1/L04.html:241", P,
    "E[B_t^3]=0; E[X_t|F_s] = B_s^3 + 3(t-s)B_s re-derived (E[Y]=E[Y^3]=0, E[Y^2]=t-s); differs from B_s^3 on {B_s != 0}; assumptions 4.1 and 4.2(a),(c),(d) named in the text.")
row("b-math-L04-misconception-2", "2.4 misconception 2 (exp(theta B) is not a martingale)", "course/modules/SC/SC1/L04.html:244-245", P,
    "E[e^{theta B_t}] = e^{theta^2 t/2} changes with t for theta != 0; the assumption is named ('assuming Assumption 4.2'). Correct.")
row("b-math-L04-R1-R3", "2.4 research problems R1-R3", "course/modules/SC/SC1/L04.html:336-353", P,
    "R1: B_t^2 - g(t) martingale iff g(t) = t + c (k = t - g deterministic martingale must be constant), re-derived; R2: exp(cB_t) martingale only for c = 0 (Z_s e^{c^2 h/2} = Z_s), re-derived; R3: conditional variance t - s, re-derived. Each states 'Assume Assumptions 4.1 and 4.2'.")
row("b-math-L04-M1-M3", "2.4 mechanics problems M1-M3 (round-8 M2 defect fixed)", "course/modules/SC/SC1/L04.html:261-279", P,
    "M1: E B_t^2 = t, E B_t^4 = 3t^2 (L03 Lemma 2.2). M2: E[e^{B_2}] = e, E[Z_2] = 1; the hypothesis now reads 'assuming Assumptions 4.1 and 4.2' (L04:271), which fixes the round-8 FAIL b-prob-L04-M2-hypothesis. M3: 'Assuming Assumptions 4.1 and 4.2' at L04:278; Var(Z_t) = e^{theta^2 t} - 1 re-derived.")
row("b-math-L04-E1-E3", "2.4 empirical problems E1 and E3 (E2 separate)", "course/modules/SC/SC1/L04.html:311-328", P,
    "E1: e^{0.25} = 1.284025417 printed (output line 220). E3: e^{theta^2 t/2} at theta=2, t=4 equals e^8 = 2980.957987 re-derived; labelled as prediction, not printed. The E2 defect is row b-assumed-L04-E2.")
row("b-assumed-L04-E2", "2.1 item 6 / 'Assuming' rule: solution E2 cites Proposition 2.4 for E[Z_t^2]", "course/modules/SC/SC1/L04.html:321", F,
    "E2 solution: 'Proposition 2.4 gives E[Z_t^2] = e^{theta^2 t} = e^8'. Proposition 2.4 is stated 'Conclusion: assuming Assumptions 4.1 and 4.2, ...' (L04:134), and E2 names no assumption. The same defect class was ruled a FAIL for the M2 solution in round 8 (b-prob-L04-M2-hypothesis). The value itself is correct (Lemma 2.1 with 2 theta gives it with no assumption).",
    "In the E2 solution (L04.html:321) change 'Proposition 2.4 gives' to 'Assuming Assumptions 4.1 and 4.2, Proposition 2.4 gives', or cite the second-moment computation as following from Lemma 2.1 alone.")
row("b-math-L05-lemma-1.3", "2.4 mathematics: Lemma 1.3 (future increment independent of past)", "course/modules/SC/SC1/L05.html:89-103", P,
    "Cases s=t, s=0 (F_0 = sigma(B_0), B_0 = 0), s<t with finite partitions (D3), A4(f) grouping, pi-system of cylinder events generating F_s, A4(a) extension; each step re-derived.")
row("b-math-L05-thm-1.4", "2.4 mathematics: Theorem 1.4 statement and proof (round-8 FAIL)", "course/modules/SC/SC1/L05.html:105-123", P,
    "Re-verified: statement at L05:111 reads 'Assuming A4(a), A4(b) and A4(f) (A4(a) and A4(f) through Lemma 1.3, and A4(b) directly)', which matches the proof (Lemma 1.3 at L05:120; A4(b) applied at L05:120). Density substitution y = z + w and p_u(z,y) identity re-derived (L05:121). s=t case at L05:122 correct. Fixes round-8 FAIL b-math-L05-thm-1.4.")
row("b-math-L05-lemma-2.2-thm-2.1", "2.4 mathematics: Lemma 2.2 and Theorem 2.1 (Chapman-Kolmogorov)", "course/modules/SC/SC1/L05.html:135-165", P,
    "Lemma 2.2 identity re-derived (uv expansion; (u+v)(vx^2+uy^2) - (vx+uy)^2 = uv(y-x)^2, checked; P1 check at u=1, v=3, x=0, y=1 re-derived: both sides (4z^2-2z+1)/3). Theorem 2.1 constants (2 pi)^(-1)(2 pi)^(1/2) = (2 pi)^(-1/2), uv cancel: re-derived. A4(e) named.")
row("b-math-L05-A4i-statement", "2.1 item 6: new numbered Assumption A4(i) (delta)", "course/modules/SC/SC1/L05.html:69, 327, 444; cards SC1-c214", P,
    "A4(i) (freezing for integrable functions) is a standard extension of A4(b) and is stated as an assumption with its side condition (E|f(Z,Y)| < infinity and finite fbar(z)). grep shows A4(i) is used only at L05:327 (M2 solution) and L05:444 (quiz answer), so the sentence 'the page uses it only for the unbounded polynomials of Problem M2' (L05:69) is accurate.")
row("b-math-L05-A3-sketch", "2.4 A3 sketch names the skipped step", "course/modules/SC/SC1/L05.html:271-281", P,
    "A3 is stated for continuous paths and rho <= c; sketch labelled 'Sketch, not a proof'; skipped steps (i) extension of independence to the whole path and (ii) limit passage named; the dyadic bounds rely on R3 (L05:406) which is re-derived.")
row("b-math-L05-R3", "2.4 research problem R3 (dyadic approximation)", "course/modules/SC/SC1/L05.html:403-406", P,
    "x <= ceil(x) < x+1 gives rho <= rho_n < rho + 2^-n; {rho_n <= r} = {rho <= k/2^n} with k = floor(2^n r) re-derived; event lies in F_{k/2^n} subset F_r.")
row("b-math-L05-problems", "2.4 L05 problems M1-M3, P1-P3, E1-E3, R1-R3", "course/modules/SC/SC1/L05.html:317-400", P,
    "M1 integral 1/(2 sqrt pi) (Gaussian integral with c=2) re-derived; M2 handled in b-assumed-L05-quiz-M2 and row b-math-L05-A4i-statement; M3 covariance 0 and A1(c) citation (L01 A1(c) exists); P2 Phi form and P3 normalisation re-derived; R1 eta* not a stopping time (two paths) re-derived; R2 deterministic time re-derived.")
row("b-math-L05-misconceptions", "2.4 L05 misconceptions", "course/modules/SC/SC1/L05.html:297-306", P,
    "Three misconceptions with wrong belief and correction; conditional law N(B_s, t-s) (depends on B_s); p_{t-s}(x,.) vs p_t(0,.) coincide only when x=0 and s=0 (re-derived: mean x and variance t-s must match 0 and t).")
row("b-math-L05-def-1.1-st-case", "2.4 Definition 1.1 and the s=t case of Theorem 1.4", "course/modules/SC/SC1/L05.html:75-78, 122", P,
    "Definition 1.1 quantifies over 0<=s<=t and bounded Borel g with psi(B_s); s=t case psi=g and F_t-measurability of B_t (L05:122) correct.")
row("b-math-L05-E1-E3", "2.4 L05 empirical problems E1-E3 (round-8 rows carried in b-scope-L05-E1-tail)", "course/modules/SC/SC1/L05.html:365-382", P,
    "E1 ratio 1.457e13 and 'the mass for |z|>40 is not computed' (L05:368) re-derived; E2 error bound 5e-11 from ten printed digits re-derived; E3 3.05e-16/2.22e-16 = 1.37 re-derived.")
row("b-scope-L05-E1-tail", "2.4 scope: E1 tail claim", "course/modules/SC/SC1/L05.html:368", P,
    "E1 says the printed mass covers 12<=|z|<=40 only and 'this page makes no claim that it is small' for |z|>40; the lab computes only that window (tail_mass). Consistent.")
row("b-math-L05-quiz-Q7", "2.4 quiz item 7 (A3 sketch) answer", "course/modules/SC/SC1/L05.html:479-485", P,
    "Answer 'the extension of independence ... and the passage to the limit' matches the sketch steps (i) and (ii) at L05:281.")
row("b-quiz-L05-Q7", "2.4 quiz L05 Q7 (A3 sketch unproved step)", "course/modules/SC/SC1/L05.html:479-485", P,
    "Same as b-math-L05-quiz-Q7: answer names the two steps the sketch skips (L05:281).")
row("b-assumed-L05-quiz-Q9", "2.1 item 6 / 'Assuming' rule: quiz Q9 answer cites Problem P2", "course/modules/SC/SC1/L05.html:497-499", F,
    "Q9 answer: 'By Problem P2 the value is Phi(-1/sqrt2) = 0.23975006...'. The value is correct (Phi(-1/sqrt2) = 0.2397500611; 0.23975 to five places). But Problem P2 is proved 'using Theorem 1.4' and Theorem 1.4 needs Assumptions A4(a), A4(b), A4(f) (L05:111), and the answer names no assumption. The misconception at L05:298 states its hypotheses, which shows the page's practice.",
    "In the Q9 answer (L05.html:499) write 'Under Assumptions A4(a), A4(b) and A4(f), Problem P2 gives the value Phi(-1/sqrt2) = 0.23975006..., which is 0.23975 to five decimal places.'")
row("b-assumed-L05-quiz-M2", "2.1 item 6 / 'Assuming' rule: quiz Q2 answer names only A4(i) (delta hunk)", "course/modules/SC/SC1/L05.html:444", F,
    "Changed in round 8's delta: 'E[B_3^2|F_1] = B_1^2 + 2 = 3 (Problem M2, under A4(i)).' The M2 solution (L05:327) uses A4(a), A4(f) and A4(i) (A4(a) and A4(f) enter through Lemma 1.3). The answer names only A4(i), so it is incomplete.",
    "Change L05.html:444 to '(Problem M2, under A4(a), A4(f) and A4(i))'.")
row("b-scope-L05-canonical", "2.9 canon-breaks section names failing hypotheses", "course/modules/SC/SC1/L05.html:284-289", P,
    "Canon breaks name dependent increments (D3), discontinuous paths (B~, A3 not asserted), unbounded stopping times (A3 does not cover them) and the A3 sketch's unproved steps; each is a hypothesis whose failure is named, as required by plan section 3.")
row("b-notation-L05-Phi-varphi", "2.3 notation: Phi and varphi", "course/modules/SC/SC1/L05.html:121, 349-351", P,
    "Phi appears only as the standard normal distribution function (P2, L05:349-351), its registered meaning (notation/notation.json and plan 2.3). varphi_u appears only for the Gaussian density (L05:121), as plan 2.3 requires.")
row("b-notation-L05-X-n", "2.3 notation: X and n", "course/modules/SC/SC1/L05.html:61-69, 281", P,
    "X is a generic process or variable (A4(b), A3 conclusion) and n is a grid index in the sketch (rho_n); no registered macro or symbol conflict (plan 2.3 registers no X or n meaning).")
row("b-notation-M-clash", "2.3 notation: M_t and M_N", "course/modules/SC/SC1/L05.html:52, 268; L06.html:56, 112", P,
    "M_t is the running maximum of B and M_N the running maximum of S_k; both mean the running maximum of their own process, not a clash. Observation only.")
row("b-scope-L05-D1D3", "2.3 scope: which parts of A4 Sections 1-2 use", "course/modules/SC/SC1/L05.html:56", P,
    "Sentence 'Sections 1 and 2 use (D1) to (D3) and A4(a), A4(b), A4(e), A4(f)': Lemma 1.3 uses A4(a),(f); Theorem 1.4 uses A4(b); Theorem 2.1 uses A4(e). A4(c),(d),(g),(h) appear only in Section 3 and in problems; A4(i) only in M2 (grep). Accurate.")
row("b-term-almost-surely", "2.5 terms outside the 8 concepts: almost surely, Gaussian process, transition density", "course/modules/SC/SC1/L05.html:76, 122, 465; L06.html:170", P,
    "'almost surely' appears in words (L05:76, 122; L06:170); 'Gaussian process' appears only as a distractor (L05:465); 'transition density' has a plain dfn in L05 Definition 1.2 with no data-concept link. Plain-word use as plan section 4 allows.")
row("b-math-L06-facts-unnumbered", "2.1 item 6: facts used in L06 are numbered or cited", "course/modules/SC/SC1/L06.html:102-130", P,
    "Facts used are A3, A4(b),(c),(g),(h) of Lesson 5 and A1, A2 and Assumption 2.1 of Lessons 1-2, each named; IVT used by name and not attributed (L06:112, 114).")
row("b-math-L06-prop-1.3-cor-1.4", "2.4 mathematics: Proposition 1.3 and Corollary 1.4", "course/modules/SC/SC1/L06.html:75-97", P,
    "Reflection bijection re-derived (b<a so 2a-b > a); Corollary 1.4 sum over b<a maps to #{S_N>a}; probability form 2P(S_N>a)+P(S_N=a) re-derived. Enumeration of all n<=12 confirms (recompute_r9.txt).")
row("b-math-L06-lemma-2.1", "2.4 mathematics: Lemma 2.1 (i)-(iii)", "course/modules/SC/SC1/L06.html:105-115", P,
    "(i) by IVT on the continuous path and closedness of {B_s = a}; (ii) IVT; (iii) argument re-derived, with s = t < tau_a giving B_t != a and therefore B_t < a.")
row("b-math-L06-prop-2.3-thm-2.5", "2.4 mathematics: Proposition 2.3 and Theorem 2.5", "course/modules/SC/SC1/L06.html:123-170", P,
    "W_t explicit form on {tau_a <= t} and {tau_a > t} re-derived; freezing with f_-, f_+ and h_- = h_+ by symmetry re-derived; Theorem 2.5 chain (E = {W_t > a}, P(B_t = a) = 0) re-derived. Assumptions at L06:127-130 and L06:156-157 are stated.")
row("b-math-L06-def-2.2-remark-2.4", "2.4 Definition 2.2 and Remark 2.4 (path level not proved)", "course/modules/SC/SC1/L06.html:118-121, 149", P,
    "Definition 2.2 states the path-level reflection and says 'On this page the path-level statement is not proved'; Remark 2.4 says the path-level statement is not used or claimed. Consistent with Proposition 2.3 and with the card SC1-c122.")
row("b-math-L06-cor-2.6", "2.4 mathematics: Corollary 2.6 (erfc closed form)", "course/modules/SC/SC1/L06.html:174-181", P,
    "Substitution z = sqrt2 w gives (1/sqrt pi) int_{a/sqrt(2t)}^inf e^{-w^2} dw = erfc/2 re-derived; the statement's own assumptions t>0, a>0 are unconditional; the 'Assuming A3 and A4' clause applies only to the identification with P(M_t >= a).")
row("b-math-L06-R1-R3", "2.4 L06 research problems R1-R3", "course/modules/SC/SC1/L06.html:407-424", P,
    "R1 parity identity re-derived; R2 min of B via B' = -B and Theorem 2.5 re-derived (2P(B_t < -a)); R3 strict inequality re-derived (2x > x for x > 0).")
row("b-math-L06-E1-E3", "2.4 L06 empirical problems E1-E3", "course/modules/SC/SC1/L06.html:383-400", P,
    "E1: 78 = 1+...+12 with the lab's exhaustive loop; E2: 281/512 - 352/1024 = 210/1024 = C(10,6)/1024; E3: unrounded half 0.15865525393 vs printed 0.1586552539 explained (first value rounded). All re-derived.")
row("b-math-L06-M-P-problems", "2.4 L06 mechanics M1-M3 and proof P1-P3", "course/modules/SC/SC1/L06.html:335-376", P,
    "M1 count 5 of 8 and Corollary 1.4 check (4 + 1 = 5) re-derived; M2 1/4 re-derived; M3 path S = (0,1,2,1,0,1), kappa = 2, reflected S' = (0,1,2,3,4,3) re-derived; P1 involution re-derived; P2 Lemma 2.1 (ii),(iii) from continuity re-derived; P3 Corollary 1.4 from Proposition 1.3 re-derived.")
row("b-scope-L06-only-events", "2.3 scope words 'only' in L06", "course/modules/SC/SC1/L06.html", P,
    "Occurrences of 'only' (e.g. 'only its fixed-time form is proved' L06:119; 'only the bound rho <= t is needed' SC1-c217) each match the proof as written; no 'only' claim without a computation.")
row("b-scope-L06-N12-every-case", "2.3 scope: 'every case' for N<=12", "course/modules/SC/SC1/L06.html:297", P,
    "'Parts A and B confirm Proposition 1.3 and Corollary 1.4 on every case with N<=12 and 1<=a<=N' is backed by the exhaustive loops in the lab (n in 1..12, a in 1..n), and the page says it does not prove other N (L06:297, section 1 proof).")
row("b-rounding-L06-misconception", "2.2 rounding in L06 misconception", "course/modules/SC/SC1/L06.html:316", P,
    "0.3173 (erfc(1/sqrt2) = 0.31731) and 0.1587 (P(B_1 >= 1) = 0.15866) are rounded to four places as stated; 'Part E prints the first value to ten decimal places' = 0.3173105079.")
row("b-plan-L06-pathlevel", "2.2 plan rule: L06 path-level claim", "course/modules/SC/SC1/L06.html:118-121, 149; plans/SC1-build-plan.md section 3", P,
    "Plan section 3 names the path-level reflected Brownian motion for L06, but the page proves only the fixed-time law and says so (Definition 2.2, Remark 2.4), with the reason (tau_a need not be bounded). The page is correct; plans/SC1-open-items.md:3-9 is stale ('labelled as a conjecture'), outside this slice, noted only.")
row("b-causal-L06-symmetry-last-step", "2.9 causal claims: symmetry and factor 2 (round-8 delta bullet)", "course/modules/SC/SC1/L06.html:306", P,
    "The factor 2 comes from E = {W_t > a} having P(E) = P(B_t > a), and P(B_t = a) = 0 makes the two tails equal. The symmetry step h_- = h_+ uses the symmetry of N(0,u); the claim makes no statement about asymmetric increments. Re-derived.")
row("b-l06-assumption-scope", "2.1 Theorem 2.5 assumption scope", "course/modules/SC/SC1/L06.html:307", P,
    "'Theorem 2.5 is conditional on A3 and A4 of Lesson 5, which are stated and not proved there' matches Theorem 2.5's assumptions (L06:157).")
row("b-l06-canon-symmetry-attribution", "2.1 attribution in L06 canon-breaks", "course/modules/SC/SC1/L06.html:300-307", P,
    "No theorem, page or equation number attributed to any book; references section at L06:536 cites only the registry key at book level.")
row("b-causal-L06-remark-2.4", "2.9 causal claims: Remark 2.4", "course/modules/SC/SC1/L06.html:149", P,
    "'Proposition 2.3 is a statement about one time t at a time' matches its statement; the claim about the whole path is not made.")
row("b-hyp-L06-102-lesson2-hypotheses", "2.1 Lesson 2 hypotheses cited in L06", "course/modules/SC/SC1/L06.html:102", P,
    "Theorem 2.5 (H2) of L02 is 'Assuming A2 and Assumption 2.1'; Remark 2.6 (H2) is 'Assuming A1(a), A1(b), A1(e), A2 and Assumption 2.1'; the L06 text cites exactly these (verified L02.html:289-306).")
row("b-ivt-observation", "2.9 IVT named not attributed", "course/modules/SC/SC1/L06.html:112, 114", P,
    "The intermediate value theorem is used by name only; no source is attributed (observation).")
row("b-quiz-L06-Q8", "2.9 quiz L06 Q8 (P(B_1 >= 1))", "course/modules/SC/SC1/L06.html:509-511", P,
    "Answer 0.1587 = 0.5 erfc(1/sqrt2) = 0.15866 rounded; 'B_1 has no atom' is the reason P(B_1 > 1) = P(B_1 >= 1). Correct.")
# ---- labs round-8 ids
row("b-lab-L05-gap-carry", "2.5 Lab 1 (L05) output carried: gap and tail wording", "course/modules/SC/SC1/L05.html:256-262", P,
    "Output lines 256-262 are reproduced by the twin (run_labs and twin_match_r9); the wording 'at the scale of double-precision rounding' is supported by 5.55e-16 vs epsilon 2.2e-16.")
# ---- cards
row("b-cards-c061-c072", "2.7 cards SC1-c061..c072 (L04)", "course/modules/SC/SC1/cards.json", P,
    "All 12 read in full against L04 text: filtration, natural filtration, Assumption 4.1, 4.2(a), Def 1.2, Lemma 2.1, Prop 2.2, Prop 2.3 (B_t^2-t, E B^4 = 3t^2), remark (E[(B_t-B_s)^2|F_s] = t-s), Prop 2.4, E[Z_t^2] (c071), Lab 1 numbers (c072). All agree.")
row("b-cards-c073-c085", "2.7 cards SC1-c073..c085 (L04 and L05)", "course/modules/SC/SC1/cards.json", P,
    "c073-c082 (L04 Q/misconceptions, R1, R2, P2, P3) and c083-c084 (L05 Def 1.1, Def 1.2) read in full; all consistent with lesson text; c084 formula matches Def 1.2.")
row("b-cards-c086-c097", "2.7 cards SC1-c086..c097 (L05)", "course/modules/SC/SC1/cards.json", P,
    "Read in full: c086 Lemma 1.3, c087 Theorem 1.4 (updated hypothesis wording matches L05:111), c088 Remark 1.5, c089 Lemma 2.2, c090 Theorem 2.1, c091 (updated to count only), c092 integrals, c093 A3, c094, c095 R2, c096 R3, c097 R1. c086 contains an ellipsis inside a finite index sequence (see b-cards-ellipsis).")
row("b-cards-c098-c110", "2.7 cards SC1-c098..c110 (L05 misconceptions and problems, L06 start)", "course/modules/SC/SC1/cards.json", P,
    "Read in full; c098-c104 match L05 text; c103 (M2) and c104 (P2) now carry 'Assuming A4(a), A4(f) and A4(i)' and 'Assuming A4(a), A4(b) and A4(f)' (matching L05:327 and 349); c105 M3; c106-c110 (L06 SRW, reflected walk, Lemma 1.2, Prop 1.3, Cor 1.4) match.")
row("b-cards-c111-c122", "2.7 cards SC1-c111..c122 (L06)", "course/modules/SC/SC1/cards.json", P,
    "Read in full: c111 (1014 triples, all equal), c112 (78 pairs), c113 (281/512, 11/32, 105/512), c114 (495, 495), c115 (erfc 0.3173), c116-c118 (Lemma 2.1; c118 updated, consistent with L06:114), c119 (Def 2.2), c120-c122 (Prop 2.3, Remark 2.4). All match.")
row("b-cards-c123-c133", "2.7 cards SC1-c123..c133 (L06)", "course/modules/SC/SC1/cards.json", P,
    "Read in full: c123 Theorem 2.5, c124 Corollary 2.6 (erfc substitution), c126-c132 misconceptions and problems (values checked: 0.3173 vs 0.1587; 105/512; 0.3173/0.1587 as P(M>=a)>P(B>=a)>0; 2P(B_t<-a)); c133 (updated: 'bounded by t'). All match.")
row("b-cards-duplicates", "2.7 full scan for duplicate cards", "course/modules/SC/SC1/cards.json", P,
    "ledgers/SC1/scripts/SC1-b-r9/prose_scan_r9.py: 205 cards in the unit, 0 duplicate ids, 0 duplicate fronts; the 86 slice cards (L04 25, L05 33, L06 28) are unique. Near pairs (c091 vs c102; c115 vs c126) ask different questions.")
row("b-cards-c193-c204", "2.7 cards SC1-c193..c204 (L05 A4 facts, L04 A4.2(b)-(d))", "course/modules/SC/SC1/cards.json", P,
    "Read in full: A4(a)-(h) statements match L05:61-68 (A4(e) integral and A4(f) grouping included); c202-c204 match Assumption 4.2(b)-(d) at L04:70. Each card says 'standard fact, not proved here'.")
row("b-cards-c079-c088-c100-c119", "2.7 cards SC1-c079, c088, c100, c119", "course/modules/SC/SC1/cards.json", P,
    "c079 (R1 answer g(t)=t+c), c088 (Remark 1.5 with A4 named), c100 (misconception with assumption named), c119 (Definition 2.2 with 'not asserted from A3') all agree with lesson text.")
row("b-cards-c103-c104-hypothesis", "2.7 cards SC1-c103, c104 hypotheses", "course/modules/SC/SC1/cards.json", P,
    "Round-8 note said both cards cite 'A4(b) and Lemma 1.3'; the cards now cite the explicit assumptions of their solutions (c103: A4(a), A4(f), A4(i); c104: A4(a), A4(b), A4(f)), which match L05:327 and L05:349.")
row("b-cards-ellipsis", "2.9 ellipsis outside code (BUILDER_RULES 1.3 vs plan 2.2)", "course/modules/SC/SC1/cards.json: SC1-c086, SC1-c106, SC1-c112", P,
    "Three cards contain U+2026 inside finite index sequences (r_0<...<r_k, e_1,...,e_N, 1+2+...+12). BUILDER_RULES 1.3 bans 'an ellipsis standing for omitted content', which these are not. Plan 2.2 says 'any ellipsis outside code', which is stricter; the pages use \\dots in math in the same way. Not failed; the architect should settle the wording (notes).")
row("b-dag-D1-D9", "2.9 DAG independent review: out-of-closure names", "course/modules/SC/SC1/L04.html, L05.html, L06.html", P,
    "Visible-text grep (ledgers/SC1/scripts/SC1-b-r9/ view) for Ito, SDE, geometric Brownian motion, Ornstein, Girsanov, Feynman, Kolmogorov equations, Poisson, Levy, Black-Scholes, barrier, Monte Carlo, Euler, Milstein, Donsker, iterated logarithm, Schauder, discrete-monitored, change of measure: no hits in L04-L06 (the only hits are the Lemma 'Gaussian process' distractor, plain). data-concept links: L04 brownian-motion, conditional-expectation-l2, filtration, independence, martingale, moment-generating-function, probability-space, quadratic-variation; L05 brownian-motion, filtration, markov-property, normal-distribution, sigma-algebra, stopping-time; L06 brownian-motion, normal-distribution, reflection-principle, stopping-time. All in closure or earlier SC1.")
row("b-process-words", "2.9 process words in learner text", "course/modules/SC/SC1/L04.html, L05.html, L06.html, cards.json", P,
    "prose_scan_r9.py: process hits L04 0, L05 1 ('rounds' in 'The printed value rounds to ten decimal places', a numeric rounding use, not a process word), L06 0; cards 0.")
row("b-banned-phrases", "2.9 banned phrases (BUILDER_RULES 1.3-1.4; check_pages list)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", P,
    "prose_scan_r9.py: banned hits 0 in L04, L05, L06 and in the 86 slice cards; ellipsis hits in prose 0 (see b-cards-ellipsis for cards).")
row("b-hours-L04-L06", "2.9 hours arithmetic", "course/modules/SC/SC1/index.html:150-159; L04-L06 headers", P,
    "Each of L04, L05, L06 declares 9 study hours (data-hours). Hub: 8 lessons x 9 = 72 h (index.html:150); project 28 h (plan 5.3); total 100 h equals curriculum hours (curriculum/curriculum.json SC1 hours 100).")
row("b-hub-L04-description", "2.9 hub card text describes L04 content", "course/modules/SC/SC1/index.html:155 vs L04.html:232", F,
    "Hub card for L04 says it covers 'the optional stopping theorem for a bounded stopping time'. L04.html:232 says 'Optional stopping is not used... the optional-stopping theorem is not restated here. This lesson makes no claim about E[B_tau] or E[Z_tau]'. The card promises content the lesson disclaims. (The plan section 3 allows optional stopping only 'with a bounded stopping time and the assumption named'; the lesson uses none.)",
    "Remove 'and the optional stopping theorem for a bounded stopping time' from index.html:155 (the hub is outside this slice; reported, not edited).")
row("b-structure-sections", "2.9 template sections, misconceptions, problems, key results, quiz", "course/modules/SC/SC1/L04.html, L05.html, L06.html", P,
    "check_pages PASS. Misconceptions 3 per lesson (L04 240/244/248; L05 297/301/305; L06 315/319/323). Problems: each lesson has M1-M3, P1-P3, E1-E3, R1-R3 (at least 3 per tier). Key-results tables present. References section present.")
row("b-struct-why-it-matters", "2.9 why-it-matters at most 120 words", "course/modules/SC/SC1/L04.html:51, L05.html:52, L06.html:52", P,
    "check_pages word rule (tools/check_pages.py:243): all three pass (L04 85 words, L05 118, L06 120 by raw whitespace count).")
row("b-quiz-L04-Q8-explain", "2.9 quiz L04 Q8 explanation (round 8 PASS, re-derived)", "course/modules/SC/SC1/L04.html:432-438", F,
    "Q8 asks 'Is B_t + t a martingale?' with no assumption in the question, and the explanation cites Problem P1 (L04.html:438). P1 is 'Assuming Assumptions 4.1 and 4.2' (L04.html:287-289). Q5 (L04.html:409) and Q6 state the assumptions, so Q8 is inconsistent with the page's own practice. The answer 'No' is correct under those assumptions.",
    "Change the Q8 prompt (L04.html:432) to 'Under Assumptions 4.1 and 4.2, is B_t + t a martingale?' (or name the assumptions in the explanation).")
row("b-quiz-L04-L06", "2.9 quiz: 8-15 items, explanations, answers", "course/modules/SC/SC1/L04.html:377-465, L05.html:429-512, L06.html:450-530", P,
    "Item counts L04 11, L05 10, L06 10 (within 8-15). All 31 answers re-derived as correct. Explanations present. Assumption-wording defects are rows b-quiz-L04-Q8-explain, b-assumed-L05-quiz-Q9 and b-assumed-L05-quiz-M2.")
row("b-observation-transition-terms", "2.9 terminology: transition density vs transition function", "course/modules/SC/SC1/L05.html:115, 419; cards SC1-c087", P,
    "Theorem 1.4 says 'the transition density is p_{t-s}' (L05:115); the key-results row (L05:419) and card SC1-c087 say 'transition function'. Mathematically the same object; wording inconsistency only.")
row("b-delta-L04-L06-hunks", "2.8 delta 0dee921..c93dd52: every changed hunk read and re-derived", "course/modules/SC/SC1/L04.html (lab hypothesis 147, M2 271); L05.html (52, 69, 111, 115, 121, 279, 327, 341, 368, 375, 399, 444, 476); L06.html (306); cards.json (c087, c091, c103, c104, c118, c133, c214, c216, c217)", F,
    "Every hunk in the delta was read in full and re-derived (git diff 0dee921 c93dd52). All hunks are correct except L05.html:444, which names only A4(i) for Problem M2 while the M2 solution uses A4(a), A4(f) and A4(i).",
    "Change L05.html:444 to '(Problem M2, under A4(a), A4(f) and A4(i))'.")
row("b-delta-cross-lessons", "2.9 delta effects on other lessons", "git diff 0dee921 c93dd52", P,
    "Other changes (L01, L03, L07, L08 pages, project.html, index.html rung text, cards c150/c151, curriculum M3 concept rename) are outside slice b. Checked only that none changes an L04-L06 cross-reference: L01 (D1)-(D3), Prop 1.2, A1, Section 4 are unchanged.")
row("b-delta-twins-and-scripts", "2.5 delta: lab twins", "tests/labs/SC1/lab-SC1-L04-1.py, L05-1.py, L06-1.py", P,
    "No lab twin for L04-L06 is in the diff 0dee921..c93dd52 (only lab-SC1-L07-1.py changed). sha256 identical to round 8 (twin_sha256_r8.txt).")
row("b-scope-words-r5", "2.3 scope words in L04-L06 prose", "course/modules/SC/SC1/L04.html, L05.html, L06.html", P,
    "prose_scan_r9.py scope-word counts: L04 21, L05 55, L06 54. Each occurrence of every/all/any/always/never/exactly/only/same checked against the proof or computation it refers to. New delta scope phrases ('for every z' in A4(i); 'for every outcome' in the A3 sketch; 'for every r and every outcome' with continuity) are backed by the stated arguments.")
row("b-notation-r5", "2.3 notation (round-5 list)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", P,
    "No T used as horizon (grep); no R^*, R_f, gamma_3, gamma_4, mathbb{Q} in the slice; Phi only as CDF; varphi only as Gaussian density; \\indic, \\Normal, \\Var, \\Cov, \\E, \\Prob used with registered meanings.")
row("b-recompute-r5", "2.2 independent recomputation", "ledgers/SC1/scripts/SC1-b-r9/recompute_r9.py", P,
    "Output in out/recompute_r9.txt (all L04-L06 numbers) and ck_independent_r9.py (out/ck_independent_r9.txt).")
row("b-verify-refs-r5", "2.1 verify_refs (carried gate)", "references/references.json", P,
    "See b-verify-refs: offline 560 entries 0 problems; SC1 live 1 of 560, 0 problems.")
row("b-assumed-facts-statement", "2.1 item 6 / 'Assuming' rule: statements that use a numbered Assumption say so", "course/modules/SC/SC1/L04.html, L05.html, L06.html", F,
    "Re-derived. Statements that carry their assumptions: L04 Props 2.2-2.4 (L04:98, 114, 134), L04 Lemma 2.1 (no assumption needed), L05 Lemma 1.3 (L05:95), L05 Thm 1.4 (L05:111, fixed in round 8), L05 Thm 2.1 (L05:147), L05 A3 (L05:271-276), L05 A4(i) (L05:69), L06 Prop 2.3 and Thm 2.5 (L06:127-130, 159). Round-8 defect L04 M2 is fixed (L04:271). Three uses of a conditional result without its assumption remain: L04:321 (E2), L04:432-438 (Q8), L05:497-499 (Q9); and L05:444 names only A4(i) for M2. These are rows b-assumed-L04-E2, b-quiz-L04-Q8-explain, b-assumed-L05-quiz-Q9 and b-assumed-L05-quiz-M2.",
    "Apply the four fixes in those rows: add 'assuming Assumptions 4.1 and 4.2' at L04.html:321; state 'under Assumptions 4.1 and 4.2' in the L04 Q8 prompt (L04.html:432); add 'under A4(a), A4(b) and A4(f)' to the L05 Q9 answer (L05.html:499); change L05.html:444 to 'under A4(a), A4(f) and A4(i)'.")
row("b-l04-problem-set-E-intro", "2.9 L04 problem-set intro", "course/modules/SC/SC1/L04.html:256", P,
    "'Problem E1 uses the output of Lab 1; E2 and E3 ask about values that Lab 1 does not print.' Checked: E1 uses printed 1.284025417 (output line 220); E2 and E3 values are not printed.")
row("b-prose-L04-R2-title", "2.9 L04 research problem titles", "course/modules/SC/SC1/L04.html:343-346", P,
    "R2 title 'When the exponential exp(cB_t) is a martingale' matches its solution (c=0 only).")
row("b-prose-L04-remark-numbering", "2.9 L04 remark numbering and cross-reference", "course/modules/SC/SC1/L04.html:37, 126", P,
    "The unnumbered 'Remark (the link with Lesson 3)' at L04:126 is the remark that the header (L04:37) cites as 'the remark after Proposition 2.3'.")
row("b-scope-L04-footer", "2.9 L04 footer claim", "course/modules/SC/SC1/L04.html:479", P,
    "Footer: 'Propositions 2.2 to 2.4 are proved on the page from Assumptions 4.1 and 4.2 ... Lab 1 is a numerical check'. Consistent with the body.")
row("b-math-L05-problems-title", "2.9 L05 problem titles", "course/modules/SC/SC1/L05.html:341, 355", P,
    "P1 title 'Verify Lemma 2.2 at one point, then in general' (round-8 delta) matches its solution; P3 'Normalisation of the transition density' matches the solution.")
row("b-prose-L05-P3-title", "2.9 L05 P3 title", "course/modules/SC/SC1/L05.html:355", P,
    "'P3 · Normalisation of the transition density' matches the solution (integral of p_u over y equals 1).")
row("b-prose-L06-P2-title", "2.9 L06 P2 title", "course/modules/SC/SC1/L06.html:366", P,
    "'P2 · Parts (ii) and (iii) of Lemma 2.1 from continuity' matches its solution (369).")
row("b-prose-L04-P3-title", "2.9 L04 P3 title", "course/modules/SC/SC1/L04.html:300", P,
    "'P3 · The product moment of a martingale at two times' matches E[Z_s Z_t] = E[Z_s^2].")
row("b-math-degenerate-L04-lemma-2.1", "2.4 degenerate cases (Lemma 2.1 with h = 0; P2 with s = t)", "course/modules/SC/SC1/L04.html:81-82, 139-140", P,
    "h > 0 is a hypothesis of Lemma 2.1 and h = 0 (s = t) is handled separately in the martingale identity (L04:140) and in Proposition 2.4's second-moment step at t = 0 (L04:139).")
row("b-math-L04-quiz-degenerate", "2.4 quiz degenerate checks", "course/modules/SC/SC1/L04.html:423-429", P,
    "Z_0 = 1 by B_0 = 0 (D1); t=0 cases handled.")
row("b-math-L05-P2-hypothesis", "2.4 P2 solution hypotheses", "course/modules/SC/SC1/L05.html:349-351", P,
    "Statement uses Theorem 1.4 without the word 'Assuming', but the solution at L05:351 states 'Assuming A4(a), A4(b) and A4(f)'. Accepted as stated in the solution (the page's practice for M2 in round 8).")
row("b-hub-L06-objective", "2.9 hub objectives vs L06 scope", "course/modules/SC/SC1/index.html:54; L06.html:118-121", P,
    "Hub objective 'Prove the reflection principle ... (Lessons 6 to 8)' versus L06's fixed-time scope. The project (project.html ladder) asks students to prove it, so the objective is covered there. Observation for the architect, not a slice FAIL.")
row("b-ck-independent-L05", "2.5 independent numeric check of L05 Chapman-Kolmogorov", "ledgers/SC1/scripts/SC1-b-r9/ck_independent_r9.py", P,
    "Independent trapezoid (6000 intervals, different algorithm): worst gap 1.5e-15 (rounding scale, matches the page's 'rounding scale' wording; the printed 5.55e-16 is the lab's Simpson run), tail mass 3.812e-29 (matches 3.81e-29), integrals 1.0000000000 (out/ck_independent_r9.txt).")

# ---- top-level
out = {
    "unit": "SC1",
    "slice": "b",
    "round": 9,
    "verifier": "independent verifier (Haiku 5.5), round 9",
    "pin": "c93dd526025c6dffd34c54cd2c89eb62a890f885",
    "base": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3 (round-8 pin); delta 0dee921..c93dd52",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE9-SC1-b",
    "scratch": "/Users/billyribeiro/.fanout/scratch/SC1-b-r9",
    "verified_at": "2026-11-05T05:30:00Z",
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b is lessons L04-L06 and lab twins. No project grader is in this slice, so mutate_graders.py and the mutation rules (plan 2.1 item 11; FINAL-ARCHITECT-RULINGS 9) do not apply; mutants is empty and no mutant is counted.",
        "Gates run on c93dd52 with outputs in ledgers/SC1/scripts/SC1-b-r9/out/. run_graders is not run: it covers project graders, which are outside this slice.",
        "Scripts: run_gates.sh, twin_match_r9.py, recompute_r9.py, prose_scan_r9.py, ck_independent_r9.py, make_fragment_r9.py in ledgers/SC1/scripts/SC1-b-r9/.",
        "Round-8 FAIL rows b-math-L05-thm-1.4 and b-prob-L04-M2-hypothesis are fixed in this pin and re-verified PASS.",
        "Round-8 PASS rows were not carried: every page in the slice changed or was re-read in full this round, and all 86 slice cards were re-read.",
        "Observation (not a FAIL): plan 2.2 bans 'any ellipsis outside code' while BUILDER_RULES 1.3 bans an ellipsis standing for omitted content. Cards SC1-c086, c106, c112 use an ellipsis in finite index sequences; the architect should settle the wording.",
        "Observation: plans/SC1-open-items.md:3-9 says Definition 2.2 is 'labelled as a conjecture'; the current page says 'not proved'. Outside the slice.",
        "Observation: L05 uses 'transition density' (L05:115) and 'transition function' (L05:419, card SC1-c087) for the same object.",
        "Observation: the L04 sketch (L04:65) takes the grouping of independent blocks as a standard fact without numbering it, while L05 numbers the same fact as A4(f). The sketch labels itself as a sketch.",
        "Observation: the unit's hub outcome at index.html:54 says 'Prove the reflection principle'; L06 proves the fixed-time form only. The project asks for the proof; see b-hub-L06-objective.",
        "Not checked: the full repository gate (whole-repo ruff and mypy, full pytest, render_curriculum, build_site --check, fetch_data --check, check_pages/check_dag/check_projects --all, verify_refs over the whole registry); only the slice-scoped commands above were run. Shreve (2004) and Karatzas & Shreve (1991) were not read and no passage is attributed to either. Pyodide-specific timing is taken from page_smoke only; no browser screenshot was taken. Lab twins are demonstrations, so no lab mutation testing was done, per the ruling.",
    ],
    "summary": {},
}
counts = {"rows": len(R), "pass": sum(r["status"] == P for r in R), "fail": sum(r["status"] == F for r in R),
          "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in R)}
out["summary"] = counts
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print(json.dumps(counts))
