"""Builds ledgers/SC1/SC1-b.json (round 13, slice b: L04-L06 and lab twins).

Row ids and check/location labels are those of the round-12 fragment
(/Users/billyribeiro/.fanout/frags/E-SC1-b.round12.json); every status and evidence string below is from
this round's own reading and this round's commands (outputs under ledgers/SC1/scripts/SC1-b-r13/out/).
"""

import json
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE13-SC1-b")
PREV = json.load(open("/Users/billyribeiro/.fanout/frags/E-SC1-b.round12.json"))
prev_rows = {r["id"]: r for r in PREV["rows"]}

OUT = "ledgers/SC1/scripts/SC1-b-r13/out/"
SCR = "ledgers/SC1/scripts/SC1-b-r13/"
RECOMP = SCR + "recompute_b_r13.py (output " + OUT + "recompute_b_r13.txt)"
FULL_READ = "read in full this round (L04.html 1-481, L05.html 1-528, L06.html 1-549, twins line by line)"

ev = {}
fix = {}

# ---- tooling (this round's command outputs) ----
ev["b-check-pages"] = "check_pages.py --unit SC1 printed 'check_pages SC1: PASS', exit 0 (" + OUT + "check_pages_unit.txt). Section order, hours (9 each), why-it-matters word counts 83/116/118 (<=120), quiz 11/10/10 items each with an explanation, 3 misconceptions and 4 tiers of 3 problems each, checked by script and by reading."
ev["b-check-dag"] = "check_dag.py --unit SC1 printed 'check_dag SC1: PASS', exit 0 (" + OUT + "check_dag_unit.txt). Out-of-closure names searched in L04-L06 (Ito, SDE, Ornstein, Euler, Girsanov, Feynman-Kac, Poisson, Levy, Black-Scholes, barrier, Monte Carlo, bias, estimator, change of measure): none. Plain-word uses of 'transition density', 'strong Markov', 'almost surely', 'Gaussian process' are defined or flagged in place (see b-r13-define-before-use-L05-why, b-r13-gaussian-process-term)."
ev["b-run-labs"] = "run_labs.py --unit SC1 printed 'run_labs SC1: PASS (11/11)', exit 0 (" + OUT + "run_labs_unit.txt). Per-page calls (" + OUT + "run_labs_L04.txt, _L05, _L06) also PASS; the --page flag does not narrow the count, so the unit count is the one recorded."
ev["b-twin-match"] = "run_labs.py --unit SC1 includes byte-identity of page code with tests/labs/SC1/lab-SC1-L04-1.py, L05-1, L06-1 and equality of pre.expected with stdout: PASS. Twins run alone from /tmp as 'python -I -W error' (exit 0; stderr 0 bytes; stdout 7, 8, 17 lines: " + OUT + "twin_L04/L05/L06.stdout|stderr)."
ev["b-lab-lint"] = "ruff check tests/labs/SC1: 'All checks passed!' (" + OUT + "ruff_check_labs.txt). ruff format --check: '11 files already formatted' (" + OUT + "ruff_format_labs.txt). mypy --no-incremental on the three slice twins: 'Success: no issues found in 3 source files' (" + OUT + "mypy_labs_b.txt)."
ev["b-page-smoke"] = "page_smoke.py --unit SC1 --pages L04 L05 L06 (run alone): 'page_smoke modules/SC/SC1/L04.html: PASS', L05 PASS, L06 PASS, 'page_smoke SC1: PASS', exit 0 (" + OUT + "page_smoke_L04-L06.txt). Lab timings 0.1 s, 1.4 s, 0.0 s."
ev["b-pytest-tooling"] = "pytest tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py -k 'SC1 or lab or page': exit 0, no failures (" + OUT + "pytest_labs_pages.txt; the run prints dots only, so the count is the collected selection)."
ev["b-verify-refs"] = "verify_refs.py --unit SC1: 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0; verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 (" + OUT + "verify_refs_unit.txt, verify_refs_offline.txt). shreve2004stochastic is the only key cited in the slice."
ev["b-attribution-references"] = "L04 section 8, L05 section 9 and L06 section 8 (read in full) state that no passage is attributed to a registry source; shreve2004stochastic appears at book level only. grep -rl Karatzas course/modules/SC/SC1/: no hits."
ev["b-check-projects"] = "check_projects.py --unit SC1 printed 'check_projects SC1: PASS', exit 0 (" + OUT + "check_projects_unit.txt). Slice b has no project page; the project belongs to slice e."

# ---- cross-lesson references ----
ev["b-cross-L04"] = "FAIL, re-verified. L04.html:37 (Uses row) lists 'the quadratic variation of Lesson 3 (in Theorem 2.3)'. L03.html:99 'Theorem 2.3' is the mean-square limit of the sums of squared increments. L04.html:126 (Remark) says the proof of Proposition 2.3 'does not use the mean-square limit of Lesson 3', and no other passage of L04 uses the quadratic variation (grep: one 'quadratic' hit in L04). The Uses row contradicts the Remark. L03 links (def-quadratic-variation, L03.html:59) and L03 Lemma 2.2 (E X^4=3 Delta^2, used at L04.html:119 and M1) are correct."
fix["b-cross-L04"] = "Delete the quadratic-variation item and its '(in Theorem 2.3)' from the Uses row at L04.html:37 (the page uses no quadratic-variation result; L03 Lemma 2.2 is cited in the proof, which is a separate reference). Keep the Remark at L04.html:126 as written."
ev["b-cross-L05-L06"] = "L05.html:268 'M6 Lesson 9, Definition 9.1' verified: course/modules/M/M6/L09.html:59 'Definition 9.1 (stopping time)'. L05.html:279 'tau_a ... defined in Lesson 6, Section 2' verified: L06.html:102 defines tau_a in Section 2. L05.html:288 'Lesson 8 ... finiteness is a result there' verified: L08.html:87 Corollary 1.4 'finite with probability one'. L06.html:102, 127, 305 verified: L02.html:289-292 and 303-306 (Theorem 2.5 and Remark 2.6 hypotheses), L08.html:58-59 (first-passage time definition), L08.html:87 (finiteness)."
ev["b-hyp-L06-102-lesson2-hypotheses"] = "L06.html:102 hypotheses match L02.html:289-292 (Theorem 2.5 (H2): 'Assuming A2 and Assumption 2.1') and L02.html:303-306 (Remark 2.6 (H2): 'Assuming A1(a), A1(b), A1(e), A2 and Assumption 2.1'). Both read this round."
ev["b-prose-L04-remark-numbering"] = "FAIL, re-verified. The numbering inside L04 is consistent (Lemma 2.1, Proposition 2.2-2.4, Remark at L04.html:126, Problems R1-R3). The cross-reference at L04.html:37 'Theorem 2.3' names no theorem of L04 (L04 has no Theorem 2.3; its only Theorem 2.3 is L03.html:99). Same defect as b-cross-L04."
fix["b-prose-L04-remark-numbering"] = "Same change as b-cross-L04: remove 'in Theorem 2.3' at L04.html:37."
ev["b-cross-L04"] = ev["b-cross-L04"]

# ---- delta (5db69a9..e919577) ----
ev["b-delta-L04-L06-hunks"] = "Delta 5db69a9..e919577 for slice b: L05.html:69 (A4(i) gains 'and for the quiz explanation that cites that problem (Section 8)'; the quiz explanation at L05.html:444 cites M2 under A4(i): verified) and L05.html:320 (M1 solution now 'Gaussian integral of Assumption A4(e) with c=2': re-derived, (2pi)^-1 sqrt(pi) = 1/(2 sqrt pi) = 0.2820947918 both ways). index.html:54 wording change re-read. cards.json: c126 (back now 'twice the tail', re-derived) changed; c201 (L08) and c231 (L07) are outside slice b. L04.html, L06.html and the three slice twins are byte-identical since 5db69a9 (git diff --stat empty)."
ev["b-delta-cross-lessons"] = "Delta hunks in other lessons read: L01.html (line 67 wording of (D1); Section 4 unchanged), L02.html (Consequence and Remark 2.6 proof wording; Theorem 2.5, Remark 2.6 statements and A2 unchanged), L03.html (why-it-matters and Assumption 3.2 wording; Lemma 2.2, Theorem 2.3 unchanged), L07/L08 (index-letter and wording changes; the L08 finiteness and first-passage claims cited by L05/L06 unchanged in substance)."
ev["b-delta-twins-and-scripts"] = "git diff 5db69a9..e919577 -- tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py: no change (only lab-SC1-project-1.py changed, outside slice b). Twins re-run this round (run_labs PASS)."

# ---- numbers (independent recomputation this round) ----
ev["b-num-L04"] = "Recomputed in " + RECOMP + ": e^1 = 2.718281828459, e^(1/4) = 1.284025416688 (prints as 1.284025417), e^4 = 54.598150033144; |54.598150033 - e^4| = 1.4e-10 and |2.718281828 - e| = 4.6e-10 (both inside the quiz tolerance 1e-9); e^8 = 2980.957987041728 (E2/E3, six places 2980.957987); Var(Z_t) = e^(theta^2 t) - 1 at the M3 values. All L04 prose numbers and quiz answers agree."
ev["b-num-L05"] = "Recomputed in " + RECOMP + ": largest CK gap 5.551e-16 (2.50 x 2^-52, page 'about 2.5 times eps'); largest tail mass 3.811e-29; example gap -3.053e-16 (1.375 x eps, page 'about 1.4'); ratio 5.55e-16/3.81e-29 = 1.4567e13 (page 1.457e13, 'about 1.5e13'); integrals 1.000000000000 with printed-digit interval [0.99999999995, 1.00000000005]; Phi(-1/sqrt2) = 0.2397500611 (quiz 0.23975, tol 1e-5); 1/sqrt(2pi) = 0.3989422804 (quiz 0.3989); P(B_1>=1) = 0.1587 (quiz tol 1e-4)."
ev["b-num-L06"] = "Recomputed in " + RECOMP + " by a DP over (position, hit) states and by binomial counts: Part A 1014/1014, Part B 78/78, Part C 1588 of 4096 with M>=3 and S=2 giving 495 and S=4 giving C(12,8)=495, Part D P(M_10>=2)=281/512, 2P(S_10>2)=11/32, P(S_10=2)=105/512 (decimals 0.548828, 0.343750, 0.205078), E2 binomial 210/1024; M1 5 of 8; M2 1 of 4; M3 walk S=(0,1,2,1,0,1), kappa=2, S'=(0,1,2,3,4,3); erfc(1/sqrt2)=0.3173105079 and P(B_1>1)=0.158655253931 (E3); Simpson check of Corollary 2.6 agrees to 10 places."

# ---- lab rows ----
ev["b-lab-L04-hypothesis"] = "L04.html:147 predictions: tolerance 1e-9 relative for E[e^(theta B_t)] against e^(theta^2 t/2) and 1e-9 absolute for E[Z_t] against 1 match twin lines 204-208 (mgf_ok relative, martingale_ok absolute, TOL=1e-9). THETAS and TIME=2 match. Output checked by run_labs PASS."
ev["b-lab-L04-interpretation"] = "L04.html:224 quotes values 2.718281828, 1.284025417, 54.598150033 = e^1, e^(1/4), e^4 (recomputed); expected block L04.html:217-223 equals twin stdout (" + OUT + "twin_L04.stdout). 'uses one time, t=2, three values of theta' matches THETAS and TIME."
ev["b-lab-L04-docstring"] = "Twin docstring lines 148-162 (numerical, not simulated; nothing random; three theta values, one t; 'not a proof for all theta and t') matches code: THETAS=(-1,0.5,2), TIME=2, LIMIT=12, PANELS=20000, simpson(), main() called at top level (line 216)."
ev["b-lab-L05-docstring-quadrature"] = "Twin docstring lines 171-179 matches code: composite Simpson on [-12,12] (simpson, LOWER/UPPER), INTERVALS=2000, 225 cases (3x3x5x5 loops in main), mass for 12<=|z|<=40 by tail_mass on [12,40] and [-40,-12], 'gaps at scale of double-precision rounding' consistent with output 5.55e-16."
ev["b-lab-L05-hypothesis-interpretation"] = "L05.html:170: 225 cases (s,t in {0.5,1,2}, x,y in 5 points: 3x3x5x5=225), tolerance 1e-6 (TOLERANCE), 'mass far below the largest gap' (3.81e-29 vs 5.55e-16), 'integral equals 1 to ten printed digits' (1.0000000000). L05.html:263: 5.55e-16 = 2.5 x eps; 3.81e-29; 5e-11 bound from ten digits; 'does not show the sign'. L05.html:306: 'checks 225 grid points' matches code. All match output (" + OUT + "twin_L05.stdout)."
ev["b-lab-L05-gap-carry"] = "L05.html:256-262 printed values (225; 5.55e-16; True; 3.81e-29; -3.05e-16; 1.0000000000 x3) equal the twin's stdout and the recomputation (" + OUT + "twin_L05.stdout; " + RECOMP + ")."
ev["b-lab-L06-claims"] = "L06.html:186 hypothesis: Parts A-E as printed (prediction 'no unequal triple' holds: 1014/1014; Part B 78/78; Part C 495 and 495; Part D 281/512, 11/32, 105/512; Part E erfc). L06.html:297 interpretation: 'every case with N<=12, 1<=a<=N' matches twin loops (range(1,13), range(1,n+1), range(-n,a)); 'Part C ... 495 ... S_12=4=2*3-2' matches output (" + OUT + "twin_L06.stdout)."
ev["b-lab-L06-docstring-exact-fraction"] = "Twin docstring lines 189-199 (exact integers and fractions; 2**N enumeration; Parts A-E; 'Part D shows the term...') matches code: integer counts, Fraction in Part D, floating point only in Part E, main() called at top level (line 279)."
ev["b-ck-independent-L05"] = "The CK gaps and integrals were recomputed in " + RECOMP + " from the density formula by a separate script (no import of the twin): max |gap| 5.551e-16 and the tail and integral values match the printed lines. The identity itself is proved on the page (Theorem 2.1), not by the lab."

# ---- math L04 ----
ev["b-math-L04-lemma-2.1"] = "L04.html:81-89 re-derived by hand: theta*y - y^2/(2h) = theta^2 h/2 - (y - theta h)^2/(2h) (expansion checked); the integrand is the N(theta h, h) density; h>0 is in the statement. Lemma and proof correct."
ev["b-math-L04-prop-2.2"] = "L04.html:93-105 re-derived: (ii) E[B_t^2] = t finite; (iii) E[B_t|F_s] = B_s + E[Y|F_s] with Y indep of F_s (Assumption 4.1 and 4.2(d)), E[Y]=0 by (D2). Hypotheses H1, H2 are the ones used. Correct."
ev["b-math-L04-prop-2.3"] = "L04.html:109-123 re-derived: E[(B_t^2-t)^2] = 3t^2 - 2t^2 + t^2 = 2t^2 (uses L03 Lemma 2.2: E X^4 = 3 Delta^2, L03.html:89-96), E[B_t^2|F_s] = B_s^2 + (t-s), so E[B_t^2 - t | F_s] = B_s^2 - s. Correct."
ev["b-math-L04-prop-2.4"] = "L04.html:129-143 re-derived: E[Z_t^2] = e^(-theta^2 t) E[e^(2 theta B_t)] = e^(-theta^2 t) e^(2 theta^2 t) = e^(theta^2 t); E[W^2] = e^(theta^2 h); E[W] = 1; Z_t = Z_s W (exponents add to theta B_t - theta^2 t/2). Correct for s<t; s=t and t=0 cases handled."
ev["b-math-L04-A4.1-sketch"] = "L04.html:63-65 is labelled 'Sketch, not a proof'; it names the skipped steps (pi-system of cylinder sets; pi-lambda extension) and cites L03 Assumption 3.2(a) which covers functions of single variables only (L03.html:70-75 read)."
ev["b-math-L04-misconception-1"] = "L04.html:241 re-derived: E[(B_s+Y)^3|F_s] = B_s^3 + 3B_s E[Y^2] = B_s^3 + 3(t-s)B_s (E[Y]=E[Y^3]=0 by symmetry); differs from B_s^3 iff B_s != 0 for s<t. Correct."
ev["b-math-L04-misconception-2"] = "L04.html:245: E[exp(theta B_t)] = exp(theta^2 t/2) by Lemma 2.1, not constant in t for theta != 0; P2 gives constant expectation for martingales. Correct."
ev["b-math-L04-R1-R3"] = "L04.html:336-353 re-derived: R1 k(t)=t-g(t) must be constant so g(t)=t+c; R2 e^(c^2 h/2)=1 forces c=0; R3 conditional variance t-s (independence, (D2)). Correct."
ev["b-math-L04-M1-M3"] = "L04.html:261-279 re-derived: M1 E[B_t^2]=t, E[B_t^4]=3t^2 (L03 Lemma 2.2); M2 E[e^(B_2)]=e and E[Z_2]=1 with Z_2=e^(B_2)e^(-1); M3 E[Z]=1, E[Z^2]=e^(theta^2 t), Var=e^(theta^2 t)-1 (0 at theta=0). Correct."
ev["b-math-L04-E1-E3"] = "L04.html:311-328: e^(0.25) = 1.284025416688, prints as 1.284025417 (E1); e^8 = 2980.957987... (E2, E3) with six-place rounding as stated. Recomputed in " + RECOMP + "."
ev["b-assumed-L04-E2"] = "L04.html:321 (E2 solution) reads 'Assuming Assumptions 4.1 and 4.2, Proposition 2.4 gives E[Z_t^2]=e^(theta^2 t)': the assumption is named where the result is used (item 6 rule)."

# ---- math L05 ----
ev["b-math-L05-lemma-1.3"] = "L05.html:89-103 re-derived: s=t trivial; s=0 with B_0=0 (F_0 trivial); for s>0 (D3) gives independence of the increments, A4(f) groups them, the pi-system of events {B_r1 in C1,...} generates F_s and A4(a) extends. Enlarging index sets does not change events. Hypotheses listed (B std BM; A4(a), A4(f)). Correct."
ev["b-math-L05-thm-1.4"] = "L05.html:105-123 re-derived: A4(b) with Z=B_s, Y=B_t-B_s, f(z,y)=g(z+y); substitution y=z+w gives psi(z)=integral g(y) p_(t-s)(z,y) dy; s=t case uses g(B_t) F_t-measurable. Hypotheses A4(a), A4(b), A4(f) stated. Correct."
ev["b-math-L05-lemma-2.2-thm-2.1"] = "Lemma 2.2 (L05.html:134-143) re-derived symbolically: z^2 coefficient (u+v)/(uv); z coefficient -2(vx+uy)/(uv) = -2(x/u+y/v); constant (vx^2+uy^2)/(uv) on both sides. Theorem 2.1 (L05.html:154-165): (2pi)^-1 (uv)^-1/2 (2 pi uv/(u+v))^1/2 = (2 pi (u+v))^-1/2, correct; c=(u+v)/(uv)>0 for A4(e). P1 example (L05.html:344, u=1,v=3,x=0,y=1) re-checked: both sides (4z^2-2z+1)/3."
ev["b-math-L05-A4i-statement"] = "Re-verified (subject changed 5db69a9..e919577 at L05.html:69). A4(i) states the freezing extension to Borel f with E|f(Z,Y)|<infinity and f-bar finite for every z, the standard extension; it is used only in M2 (L05.html:327, solution with psi(x)=x^2+2 and x^3+6x, re-derived) and in the quiz explanation L05.html:444 (Section 8), which is what the changed sentence says. cards SC1-c214 and c103 consistent."
ev["b-math-L05-A3-sketch"] = "L05.html:270-281 labelled 'Sketch, not a proof'. rho_n = ceil(2^n rho)/2^n with rho <= rho_n <= rho + 2^-n (R3 at L05.html:404-406 re-derived), countably many values, pathwise convergence by continuity, and names the two skipped steps (i) extension of independence to the whole path via A4(a), (ii) passage to the limit with A_rho-measurability. Correct and honest about the limit identification."
ev["b-math-L05-R3"] = "L05.html:402-408 re-derived: x <= ceil(x) < x+1 gives rho <= rho_n < rho + 2^-n; {rho_n <= r} = {rho <= floor(2^n r)/2^n} since ceil(y) <= m iff y <= m for integer m; the event lies in F_(k/2^n) inside F_r. Correct."
ev["b-math-L05-problems"] = "L05.html:316-400 re-derived: M1 (1/(2 sqrt pi) both sides, re-checked by script); M2 (x^2+2, x^3+6x); M3 (Cov = 0, jointly normal, A1(c) of L01); P1 (verified); P2 (CDF of N(x,t-s) by Theorem 1.4 with g=indicator); P3 (substitution); E1-E3 (see b-math-L05-E1-E3); R1 (eta* counterexample: path 1 gives eta*=1/4, path 2 gives 3/4; A4(d) argument valid); R2 (rho=s stopping time, F_s subset F_rho); R3 (see b-math-L05-R3)."
ev["b-math-L05-misconceptions"] = "L05.html:297-306 re-derived: P2 gives N(B_s,t-s) (mean B_s, so not independent); p_(t-s)(x,.) equals p_t(0,.) iff x=0 and s=0 (normal parameters); 225-case statement and 5.55e-16 match the lab output."
ev["b-math-L05-def-1.1-st-case"] = "L05.html:75-78 Definition 1.1 requires all 0<=s<=t; L05.html:122 handles s=t with psi=g and g(B_t) F_t-measurable. Correct."
ev["b-math-L05-E1-E3"] = "L05.html:364-384 re-derived by " + RECOMP + ": E1 ratio 5.55e-16/3.81e-29 = 1.4567e13, stated as 1.457e13 and 'about 1.5e13 to two significant figures' (correct rounding); E2 bound 5e-11 from ten printed digits (correct); E3 3.05e-16 = 1.375 eps, stated as 'about 1.4' (correct to two significant figures)."
ev["b-scope-L05-E1-tail"] = "L05.html:368 states the tail for |z|>40 is not computed and makes no claim that it is small; the scope matches the lab (tail_mass only to 40)."
ev["b-math-L05-quiz-Q7"] = "L05.html:479-485 quiz item: the sketch leaves the extension of independence to the whole path and the limit passage in E[f(X^(n)) 1_A]; matches L05.html:281 exactly."
ev["b-quiz-L05-Q7"] = "L05.html:485 explanation: the sketch proves the fixed-time case, sums over the countably many dyadic values, then names two skipped steps; consistent with L05.html:281."
ev["b-assumed-L05-quiz-Q9"] = "L05.html:496-499: answer 0.23975 with tolerance 1e-5 is Phi(-1/sqrt2) = 0.2397500611 (recomputed, |0.23975 - value| = 6e-8); explanation cites A4(a), A4(b), A4(f) as assumed. Correct."
ev["b-assumed-L05-quiz-M2"] = "L05.html:441-445 numeric item: answer 3 (B_1 = 1: B_1^2 + 2 = 3, Problem M2 under A4(a), A4(f), A4(i)); correct."
ev["b-scope-L05-canonical"] = "L05.html:284-289 canon-breaks: dependent increments (D3 used only in Lemma 1.3, L05.html:100); discontinuous paths (L01.html:215-216 and 234 give the process B-tilde of Lesson 1 Section 4 with discontinuous paths); unbounded stopping times (A3 stated for rho <= c; finiteness of tau_a is L08 Corollary 1.4). All verified."
ev["b-notation-L05-Phi-varphi"] = "Phi is used only as the standard normal CDF (L05.html:349-351, 499), which is the registered meaning (notation/notation.json symbols array, item '\\Phi, \\Phi^{-1}'). varphi_u (L05.html:121) is local to the Theorem 1.4 proof and is not registered; no collision."
ev["b-notation-L05-X-n"] = "X^(n) (L05.html:281) is a local symbol of the A3 sketch; not registered; no collision with a registered symbol."
ev["b-notation-M-clash"] = "M_t and M_N (running maxima, L06 and L05 text) are not registered (notation.json macros and symbols contain no M); T is not used as a horizon anywhere in L04-L06 (grep of math shows only grade labels); H is not used in the slice. No collision."
ev["b-scope-L05-D1D3"] = "L05.html:56 claims Sections 1 and 2 use (D1)-(D3) and A4(a), A4(b), A4(e), A4(f): verified by grep: A4(a)/(f) in Lemma 1.3, A4(b) in Theorem 1.4, A4(e) in Theorem 2.1; A4(c), (g), (h), (i) are not used in Sections 1-2 (they appear in L05 Section 3 and L06, and in M2/quiz); A4(d) is used only at R1. The claim is accurate."
ev["b-term-almost-surely"] = "'almost surely' is defined in words at L05.html:62 ('almost surely (that is, with probability one)') before its first use at L05.html:76; L06.html:144 repeats the same definition. No undefined use."
ev["b-math-L06-facts-unnumbered"] = "L06.html:102-130: facts used without proof are named by their numbers (Lesson 2 Theorem 2.5 and Remark 2.6 with A2 and Assumption 2.1; L05 A3, A4(b), A4(c), A4(g), A4(h)); 'Lesson 8 studies the law of this time' is a pointer to L08 (verified)."

# ---- math L06 ----
ev["b-math-L06-prop-1.3-cor-1.4"] = "L06.html:74-98 re-derived: reflection after the first visit kappa is an involution (Lemma 1.2) and a bijection between {M_N>=a, S_N=b} and {S_N=2a-b} (b<a gives 2a-b>a, so every such walk visits a by step N). Corollary 1.4 sum over b<a maps to c=2a-b>a. Hypotheses listed. Numerically confirmed for all N<=12 (Part A, B). Correct."
ev["b-math-L06-lemma-2.1"] = "L06.html:104-115 re-derived: (i) M_t>=a iff tau_a<=t via IVT and the closed set {s: B_s=a}; (ii) IVT on [0,t] with B_0=0<a; (iii) B_s<a for s<tau_a, so B_t<a on {tau_a>t}. Correct; continuity and B_0=0 in the hypotheses."
ev["b-math-L06-prop-2.3-thm-2.5"] = "L06.html:122-171 re-derived: rho=tau_a^t bounded stopping time (A4(c)); W_t = 2a - B_t on {tau_a<=t}, B_t on {tau_a>t}; X_r = B_(rho+r) - B_rho independent of F_rho (A3); W_t = B_rho - X_(t-rho); A4(b) with h_-(x,u)=h_+(x,u) by symmetry of N(0,u); Theorem 2.5: E = {W_t>a} via Lemma 2.1(iii), P(B_t=a)=0. Correct under the stated assumptions."
ev["b-math-L06-def-2.2-remark-2.4"] = "L06.html:118-121 and 147-150: Definition 2.2 states the path-level reflection and says it is not asserted from A3 (A3 covers only bounded stopping times; tau_a is not shown bounded); Remark 2.4 says it is not proved and not used. Honest on the page; the plan requirement is the separate FAIL row b-plan-L06-pathlevel."
ev["b-math-L06-cor-2.6"] = "L06.html:173-182 re-derived: z = sqrt(2) w, dz = sqrt(2) dw, z^2/2 = w^2, lower limit a/sqrt(2t), (1/sqrt(pi)) integral = erfc/2. Numerically: 2P(B_1>1) by Simpson = 0.3173105079 = erfc(1/sqrt2); 2P(B_3>2) = erfc(2/sqrt6) = 0.2482130790. Correct."
ev["b-math-L06-R1-R3"] = "L06.html:406-426 re-derived: R1 parity of S_N (sum of N terms +-1) makes both sides zero when b and N have different parity; R2 sign flip preserves BM, min/max identity, Theorem 2.5 applied to -B; R3 2x > x for x>0 with positivity of the normal tail. Correct."
ev["b-math-L06-E1-E3"] = "L06.html:382-402 re-derived: E1 78 = sum of 1..12 (pairs with 1<=a<=N); E2 281/512 - 11/32 = 105/512 = P(S_10=2) = 210/1024 (binomial C(10,6)); E3 halving 0.3173105079 gives 0.15865525395 whose unrounded value 0.158655253931 prints as 0.1586552539 (correct explanation of the last digit)."
ev["b-math-L06-M-P-problems"] = "L06.html:334-378 re-derived: M1 5 of 8 (list and Corollary 1.4 counts 4+1 re-checked); M2 1/4 and Corollary 1.4 count 1+0; M3 S=(0,1,2,1,0,1), kappa=2, S'=(0,1,2,3,4,3), 2a-S_k = 2,3,4,3 (script output recompute); P1 involution; P2 IVT parts (ii),(iii); P3 subtraction from Proposition 1.3. Correct."
ev["b-scope-L06-only-events"] = "Scope words in L06.html:52, 297, 302-309 checked: 'only' in 'the path only on [0,t]' and 'the tail of a process whose increments are not symmetric' are restrictions, not claims; 'the reflected value at a fixed time' is Proposition 2.3's claim. No unsupported scope."
ev["b-scope-L06-N12-every-case"] = "L06.html:297 'every case with N<=12 and 1<=a<=N': the twin enumerates exactly n in 1..12, a in 1..n (Part B) and b in -n..a-1 (Part A), so the claim matches the code; the page says the proof for all N is Section 1."
ev["b-rounding-L06-misconception"] = "L06.html:316: 0.3173 = 0.31731 rounded to four places and 0.1587 = 0.158655 rounded to four places (both correct); 'Part E prints the first value to ten decimal places' matches the output 0.3173105079."
ev["b-causal-L06-symmetry-last-step"] = "L06.html:306 'the factor 2 comes from adding two events of equal probability' is the proof's structure (P(B_t>=a) = P(B_t>a) because P(B_t=a)=0, L06.html:170); no causal claim beyond the proof."
ev["b-plan-L06-pathlevel"] = "FAIL, re-verified this round. plans/SC1-build-plan.md section 3 (L06 bullet) requires 'the reflection principle for B at tau_a ... the reflected path after tau_a is a Brownian motion (Assuming A3)'. L06.html:118-121 (Definition 2.2) and L06.html:149 (Remark 2.4) decline it: 'the path-level statement is not proved here'. The page's own A3 is stated for rho <= c only, so 'Assuming A3' cannot license the path statement with unbounded tau_a. The page is honest, but the plan item is unmet, and the open-items file records it as an open deviation."
fix["b-plan-L06-pathlevel"] = "Either (a) prove the path-level statement in L06: for each T > 0 apply A3 to the bounded time tau_a^T and show the glued process (B up to rho, then 2a minus B, equal in law to -X after rho by symmetry) is a standard BM on [0,T]; consistency in T then gives [0,infinity) with continuous paths; or (b) the architect records in writing (FINAL-ARCHITECT-RULINGS or plans/SC1-open-items.md) that the path-level reflection is an agreed gap for SC1 and amends plans/SC1-build-plan.md section 3 accordingly. Until one of these, this row cannot pass."
ev["b-causal-L06-remark-2.4"] = "L06.html:130 (Proposition 2.3 statement: 'W_t has the same law as B_t', one fixed t) and L06.html:149 (Remark 2.4: not used, not claimed). No causal or path-level overreach in the text."
ev["b-l06-assumption-scope"] = "L06.html:159-160 (Theorem 2.5: 'Assuming A3 and A4') and L06.html:307 (canon-breaks: conditional on A3 and A4, path-level not proved) are consistent with the proof, which uses A3 only through Proposition 2.3 (L06.html:127)."
ev["b-l06-canon-symmetry-attribution"] = "L06.html:300-307 canon-breaks items: discrete grid (Part D of the lab shows the term), path continuity (jump counterexample correct), infinite hitting times (rho bounded; Lesson 8), symmetry (h_-=h_+), assumptions. No attribution to any source; each item is correct."
ev["b-ivt-observation"] = "L06.html:104, 112, 114: Lemma 2.1 uses continuity (IVT) and B_0=0 < a; the jump counterexample in L06.html:304 and quiz L06.html:488 match."
ev["b-quiz-L06-Q8"] = "L06.html:508-511: answer 0.1587 (tolerance 1e-4) against P(B_1>=1) = 0.158655253931 (recomputed); |difference| = 4.5e-5 is inside tolerance; explanation names Lab 1 Part E and the no-atom argument."

# ---- quiz (L04 Q8, L04-L06 answers) ----
ev["b-quiz-L04-Q8-explain"] = "L04.html quiz item 'is B_t + t a martingale' (option 'No: its conditional expectation is B_s + t') and explanation (L04.html:438) match P1 (L04.html:289): E[X_t|F_s] = B_s + t, which differs from X_s = B_s + s."
ev["b-quiz-L04-L06"] = "Quiz answers recomputed: L04 numeric items 3 (E[B_3^2]=3), 27 (E[B_3^4]=27), 2.718281828 (e to 1e-9), 54.598150033 (e^4 to 1e-9); L05 items 3 (B_1^2+2), 0.3989 ((2pi)^-1/2), 0.23975 (Phi(-1/sqrt2)); L06 items 0.25, 0.3173 (erfc(1/sqrt2)=0.31731), 0.1587. Multiple-choice keys read: each data-correct option agrees with the page (e.g. L04 q5 yes by Proposition 2.3, L06 q10 symmetry of N(0,u)). All within stated tolerances."

# ---- cards ----
ev["b-cards-c061-c072"] = "cards.json c061-c072 (L04, 12 cards, read in full this round via " + OUT + "../cards_L04-06.txt): each agrees with L04 text (filtration definition, natural filtration, Assumption 4.1, 4.2(a), Definition 1.2, Lemma 2.1, Propositions 2.2-2.4, Lab 1 value e^4 at theta=2 (c072: 54.598150033 is what the quadrature prints; graded C naming Lab 1, per ruling 13))."
ev["b-cards-c073-c085"] = "cards.json c073-c084 (L04 and L05; read in full): match L04 Section 3-4 misconceptions and Problems P1, P2, E2; L05 Definitions 1.1 and 1.2. No card id c085 exists in the deck (ids need not be sequential, FINAL-ARCHITECT-RULINGS 2)."
ev["b-cards-c086-c097"] = "cards.json c086-c097 (L05; read in full): Lemma 1.3 (basis names A4(a),(f)), Theorem 1.4 (basis names A4(a),(b),(f)), Remark 1.5, Lemma 2.2, Theorem 2.1 (basis A4(e)), Lab 1 counts (225; 1.0000000000 and 5e-11), A3, stopping-time definition, R2, R3, R1 (eta* example: 1/4 and 3/4 values correct). Each agrees with the text."
ev["b-cards-c098-c110"] = "cards.json c098-c110 (L05 and L06; read in full): c098 (A3 not asserted for B-tilde, matches L05.html:287), c099 (A3 requires rho<=c), c100 and c101 (misconceptions, correct), c102 (225 cases), c103 and c104 (Problem M2 and P2 correct), c105 (M3 correct), c106-c110 (simple random walk, reflected walk, Lemma 1.2, Proposition 1.3, Corollary 1.4) match the L06 text."
ev["b-cards-c111-c122"] = "cards.json c111-c122 (L06; read in full): c111 (1014, all 1014), c112 (78), c113 (281/512, 11/32, 105/512), c114 (495 and 495, 2a-b=4), c115 (erfc(1/sqrt2) ~ 0.3173, basis Theorem 2.5 and Corollary 2.6), c116-c118 (Lemma 2.1 parts), c119 (Definition 2.2, honest: only the fixed-time form), c120-c121 (Proposition 2.3), c122 (Remark 2.4). Values re-derived; matches."
ev["b-cards-c123-c133"] = "Re-verified (c126 changed at e919577). cards.json c123 (Theorem 2.5), c124 (Corollary 2.6 closed form, no A3 needed, correct), c126 (new back 'twice the tail of the endpoint' matches Theorem 2.5; basis names Section 4), c127 (105/512, Lab 1 Part D, grade C), c128 (continuity and A3 in the reflection argument), c129 (5 of 8), c130 (parity), c131 (2P(B_t<-a)), c132 (P(M_t>=a)>P(B_t>=a)>0), c133 (rho bounded by t). c125 is absent (ids need not be sequential)."
ev["b-cards-duplicates"] = "Full scan of all 217 cards in cards.json this round: no duplicate normalised fronts or backs. Prefix collisions: c072/c226 (checked: E[e^(theta B_t)] at theta=2 vs E[Z_t] at each theta, distinct questions); c011-c013, c032/c224, c149/c230 are outside slice b and were not re-judged here."
ev["b-cards-ellipsis"] = "Ellipses in L05.html:100 (0=r_0<...<r_k), L06.html:56 (e_1,...,e_N), L06.html:386 (1+...+12) and cards c086, c106, c112 are mathematical sequences inside math, not prose ellipses; check_pages.py (PASS) would flag a prose ellipsis."
ev["b-dag-D1-D9"] = "Searched L04-L06 text and slice cards for D1-D9 names (Ito, geometric Brownian motion, Ornstein-Uhlenbeck, Euler-Maruyama, Milstein, Girsanov, forward measure, Feynman-Kac, Kolmogorov equations, Poisson, Levy, compound Poisson, Black-Scholes, barrier, Monte Carlo, pseudo-random, bias-variance, change of measure): none present. 'Gaussian process' appears only in L05.html:465 (a wrong quiz option, plain words); 'transition density' and 'strong Markov' are plain-word uses defined in place."
ev["b-process-words"] = "Scan of L04-L06 learner text and slice cards for builder, verifier, round, REQUEST, unit report, TODO, TBD: no hits (scripted)."
ev["b-banned-phrases"] = "grep (case-insensitive) of L04.html, L05.html, L06.html for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly: 0 hits each (" + OUT + "../cards_L04-06.txt scanned too)."
ev["b-hours-L04-L06"] = "index.html:29 data-hours-lessons=72, data-hours-project=28 (sum 100 with the project); L04.html, L05.html, L06.html data-hours=9 each; 8 x 9 = 72 matches the hub. No arithmetic inconsistency."
ev["b-hub-L04-description"] = "index.html:150 ('Lesson 4 covers continuous-time martingales. Lesson 5 covers the Markov property. Lessons 6 to 8 cover the reflection principle...') and the cards at index.html:155-157 (L04 martingales B_t, B_t^2-t and exponential; L05 Gaussian transition density, CK by completing the square, strong Markov as A3; L06 fixed-time reflection identity under A3 and A4, tail, discrete identity) match the lesson content."
ev["b-structure-sections"] = "L04, L05, L06 section order (read in full): why-it-matters, s1 core, lab, canon-breaks (s3/s4), misconceptions, problem set (mechanics, proof, empirical, research), key results, quiz, references, lesson-nav. 3 misconceptions each; 4 tiers each with 3 problems; 11/10/10 quiz items each with explanations; 9 hours each."
ev["b-struct-why-it-matters"] = "why-it-matters word counts (script, LaTeX tokens counted as one word): L04 83, L05 116, L06 118; all <=120 words."

# ---- structure/prose remaining ----
ev["b-l04-problem-set-E-intro"] = "L04.html:256: 'Problem E1 uses the output of Lab 1; E2 and E3 ask about values that Lab 1 does not print': E1 uses the printed 1.284025417 (L04.html:311-316); E2 (e^8) and E3 (e^8 at t=4) are not printed (lab prints t=2 only). Correct."
ev["b-prose-L04-R2-title"] = "L04.html:343-346: R2 title 'When the exponential exp(cB_t) is a martingale' and the solution proves 'only when c=0' with the converse; consistent."
ev["b-math-L05-problems-title"] = "L05.html problem titles (M1 'Chapman-Kolmogorov at the origin', M2, M3, P1 'Verify Lemma 2.2', P2, P3, E1-E3, R1-R3) match their solutions read this round."
ev["b-prose-L05-P3-title"] = "L05.html P3 title 'Normalisation of the transition density' matches the solution (integral equals 1 by substitution)."
ev["b-prose-L06-P2-title"] = "L06.html:366-369: P2 title 'Parts (ii) and (iii) of Lemma 2.1 from continuity' and the solution proves exactly (ii) and (iii) without (i)."
ev["b-prose-L04-P3-title"] = "L04.html:300-304: P3 'The product moment of a martingale at two times' and the solution gives E[Z_s Z_t] = E[Z_s^2] by Assumption 4.2(c) and the tower property."
ev["b-math-degenerate-L04-lemma-2.1"] = "L04.html:81-82 needs h>0 (stated); t=0 handled in Proposition 2.4 (L04.html:139: both sides 1 at t=0); Lemma 2.1 with h=0 is not claimed."
ev["b-math-L04-quiz-degenerate"] = "L04 quiz 'What is Z_0' (L04.html:423-429): Z_0 = exp(0) = 1 from B_0 = 0 (D1); correct."
ev["b-math-L05-P2-hypothesis"] = "L05.html:347-351: P2 states 0 <= s < t and c real, uses Theorem 1.4 (hypotheses A4(a), A4(b), A4(f) named in the solution); the indicator g is bounded Borel. Correct."
ev["b-hub-L06-objective"] = "Re-verified (index.html:54 changed at e919577). Hub objective 'Prove the fixed-time reflection identity for Brownian motion (Lesson 6, Theorem 2.5), under Assumptions A3 and A4, derive the tail ... name the assumptions each one uses (Lessons 6 to 8)' matches L06 Theorem 2.5 (fixed-time identity under A3, A4), L07 (tail) and L08 (first passage). Correct."
ev["b-scope-words-r11"] = "Every occurrence of every, all, any, only, always, never, almost surely, converges, exactly, same in L04-L06 text was read (scripted listing): each is either a proved universal (e.g. 'for every real theta' in Lemma 2.1, 'for every t' in Proposition 2.4), a finite computation the lab enumerates, or a misconception statement. No unsupported scope."
ev["b-notation-r11"] = "Notation: slice uses \\Prob, \\E, \\Var, \\Cov, \\R, \\indic, \\Normal (all registered in notation.json macros) and \\Phi as the registered CDF; no symbol with a registered different meaning (T, R^*, R_f, gamma_3, gamma_4, Q not used). Checked against notation/notation.json."
ev["b-recompute-r11"] = "Recomputation of every slice number: " + RECOMP + "; outputs in " + OUT + "recompute_b_r13.txt."
ev["b-verify-refs-r11"] = "verify_refs.py --offline: 560 entries, 0 problems; --unit SC1 live: 1 of 560 entries, 0 problems (" + OUT + "verify_refs_*.txt)."
ev["b-assumed-facts-statement"] = "Results that use an assumption say so in their statement: L04 Propositions 2.2-2.4 'assuming Assumptions 4.1 and 4.2' (L04.html:98, 114, 134); L05 Lemma 1.3, Theorem 1.4 (L05.html:95, 111), Theorem 2.1 (L05.html:148), problems; L06 Proposition 2.3 (L06.html:130), Theorem 2.5 (L06.html:159), Corollary 2.6 (L06.html:176), R2, R3. All checked this round."
ev["b-notation-r5"] = ev["b-notation-r11"]
ev["b-recompute-r5"] = ev["b-recompute-r11"]
ev["b-scope-words-r5"] = ev["b-scope-words-r11"]
ev["b-verify-refs-r5"] = ev["b-verify-refs-r11"]
ev["b-math-L04-A4.2-E1G"] = "L04.html:70 Assumption 4.2(e) E[1|G] = 1 is stated and used: Proposition 2.4 martingale identity and Proposition 2.2 (L04.html:103), the s=t case (L04.html:140), and misconception 1 (L04.html:241). Assumption list complete for each use."
ev["b-cards-c193-c204"] = "cards.json c193-c200 (L05 A4(a)-(h), read this round), c202-c204 (L04 A4.2(b),(c),(d)), c214 (A4(i)): each matches the stated assumption text (L05.html:58-72; L04.html:70). c214 consistent with the changed L05.html:69."
ev["b-cards-c079-c088-c100-c119"] = "c079 (L04 R1: g(t)=t+c, matches L04.html:339), c088 (Remark 1.5, matches L05.html:127), c100 (Markov misconception, matches L05.html:298), c119 (Definition 2.2, matches L06.html:119). All correct."
ev["b-cards-c103-c104-hypothesis"] = "c103 (Problem M2 hypotheses A4(a),(f),(i); L05.html:325-327) and c104 (Problem P2 hypotheses A4(a),(b),(f); L05.html:349-351): hypotheses match the solutions."
ev["b-cards-r12-changed"] = "cards c072 (L04, lab card), c095 (R2 constant time is a stopping time), c096 (R3 bounds), c203 (A4.2(c) pull-out with Y=1): all re-read; each agrees with the current text."
ev["b-cards-r12-added"] = "cards c222 (A4.2(e) E[1|G]=1), c226 (E[Z_t]=1 at each theta; the lab prints 1.000000000, L04.html:220-223), c227 (F_s subset F_rho for constant rho; L05.html:399), c228 (R3 stopping-time proof; L05.html:406). All correct."
ev["b-ruling-13-check"] = "FINAL-ARCHITECT-RULINGS 13 (plans/FINAL-ARCHITECT-RULINGS.md:28-30): values derived by hand in a numbered proof are T (L06 Corollary 2.6 P(M_1>=1)=erfc(1/sqrt2) graded T, card c115 T); values that appear only in lab output are C naming the lab (L04 key-results row, L05 key-results row, L06 key-results row, cards c072, c091, c092, c111-c114, c127, c216, c226). Consistent."

# ---- new rows (round 13) ----
NEW = {}
NEW["b-r13-define-before-use-L05-why"] = dict(
    check="2.2 define before use (why-it-matters)",
    location="course/modules/SC/SC1/L05.html:52",
    status="PASS",
    evidence="The why-it-matters paragraph uses 'Gaussian transition density' and 'Markov property' before their <dfn>s (L05.html:76, 80-81), with explicit pointers 'Definition 1.2 below' and 'Definition 1.1 below'. The forward pointer names the defining item, so no term is undefined for the reader. Passed as an observation; the builder may tighten it.",
)
NEW["b-r13-gaussian-process-term"] = dict(
    check="2.2 plain-word term (plan section 4)",
    location="course/modules/SC/SC1/L05.html:465; course/modules/SC/SC1/L01.html:115",
    status="PASS",
    evidence="'Gaussian process' is not a curriculum concept (plan section 4). It first appears in L01.html:115 (not in slice) and in L05.html:465 only as a wrong quiz option ('It is a Gaussian process with variance rho'), which is plain prose and not a link or a dfn. Plan section 4 allows plain prose.",
)
NEW["b-r13-plan-section3-coverage"] = dict(
    check="2.9 plan section 3 content (L04-L06)",
    location="plans/SC1-build-plan.md section 3 (L04, L05, L06 bullets); course/modules/SC/SC1/L04.html, L05.html, L06.html",
    status="PASS",
    evidence="L04: definition of continuous-time martingale, B_t and B_t^2-t martingales (T), exponential martingale (T), quadrature lab (numerical, not SIMULATED, tolerance stated), no optional stopping beyond the stated remark, 'where the canon breaks' names a failed hypothesis. L05: Markov property, Gaussian transition density, CK (T), A3 as numbered assumption with sketch naming the skipped steps, quadrature lab (numerical). L06: discrete reflection bijection (T), finite enumeration lab (C, basis named), continuous identity P(M_t>=a)=2P(B_t>=a) (T, assuming A3 and A4). The one unmet item (path-level reflection) is the separate FAIL row b-plan-L06-pathlevel.",
)
NEW["b-r13-delta-changed-hunks"] = dict(
    check="2.8 delta: hunks in the slice re-derived",
    location="course/modules/SC/SC1/L05.html:69 and :320; course/modules/SC/SC1/index.html:54; course/modules/SC/SC1/cards.json (SC1-c126)",
    status="PASS",
    evidence="Each changed hunk of the slice re-derived: L05.html:69 (A4(i) scope sentence, matches M2 and quiz explanation L05.html:444), L05.html:320 (M1 solution, value 1/(2 sqrt pi) re-derived), index.html:54 (hub wording, matches L06 Theorem 2.5), cards.json SC1-c126 (back 'twice the tail', matches Theorem 2.5). c201 (L08) and c231 (L07) are outside slice b.",
)
NEW["b-r13-numeric-recompute-script"] = dict(
    check="2.2 numbers recomputed by an independent script",
    location=SCR + "recompute_b_r13.py; " + OUT + "recompute_b_r13.txt",
    status="PASS",
    evidence="Standard-library script run with -I: every printed or quoted number in L04-L06 (lab outputs, E-problems, quiz tolerances, Phi and erfc values, Part A-E counts and fractions, the M3 walk, the Corollary 2.6 closed form by quadrature) reproduced to the stated precision. No discrepancy found.",
)


ev["b-observation-transition-terms"] = "L05.html:79-86 (Definition 1.2 Gaussian transition density, defined with a plain dfn), L05.html:115 (Theorem 1.4 names the transition density), L05.html:419 (key-results row), cards SC1-c084 (definition) and SC1-c087 (Theorem 1.4). The term is defined in place and used consistently with the same meaning p_u(x,y). Consistent; no DAG issue (plan section 4, plain prose)."
ev["b-scope-L04-footer"] = "L04.html footer (line 479): 'Propositions 2.2 to 2.4 are proved on the page from Assumptions 4.1 and 4.2, which are stated and not proved here; Lab 1 is a numerical check and is labelled as one.' Matches L04.html:145-147 (numerical, not simulated) and the propositions' hypotheses."

# ---- assemble ----
rows = []
for rid, r in prev_rows.items():
    status = "FAIL" if rid in fix else "PASS"
    if rid in ("b-cross-L04", "b-prose-L04-remark-numbering", "b-plan-L06-pathlevel"):
        status = "FAIL"
    e = ev[rid]
    row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": e}
    if status != "PASS":
        row["fix"] = fix[rid]
    rows.append(row)
for rid, d in NEW.items():
    row = {"id": rid, "check": d["check"], "location": d["location"], "status": d["status"], "evidence": d["evidence"]}
    rows.append(row)

assert all(r["status"] in ("PASS", "FAIL") for r in rows)
frag = {
    "unit": "SC1",
    "slice": "b",
    "round": 13,
    "verifier": "independent verifier (Haiku 5.5), round 13",
    "pin": "e919577b45b431ce68e1e6533b00b8a301277937",
    "base": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0 (round-12 pin); delta 5db69a9..e919577 (commit e919577 round-12 fixes)",
    "checkout": str(ROOT),
    "scratch": str(ROOT / SCR.rstrip("/")),
    "verified_at": "2026-11-05T17:33:11Z",
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": PREV["registry_flags"],
    "freshness_flags": [],
    "notes": [
        "Slice b = L04, L05, L06 pages, their three lab twins, the index.html rows that cite them, and the cards whose lesson is L04-L06 (90 cards). Every page was read in full, line by line, this round; every equation and every quiz answer was re-derived; every lab output was recomputed; every cross-reference was checked against the target file.",
        "Round-12 PASS rows were not carried: each was re-evaluated against this round's reading and commands. One round-12 PASS (b-cross-L04) is now FAIL: the Uses row at L04.html:37 cites Theorem 2.3 for the quadratic variation, which contradicts the Remark at L04.html:126.",
        "No grader or project is in slice b, so no student-error mutant is counted; mutants is empty (same ruling as rounds 10-12).",
        "run_graders, mutate_graders and the project-level alternatives were not run: they belong to slice e (project).",
        "The full repository gate was not run (only slice- and unit-scoped commands); the architect runs it before a merge.",
    ],
    "summary": {},
}
n_fail = sum(1 for r in rows if r["status"] != "PASS")
frag["summary"] = {"rows": len(rows), "pass": len(rows) - n_fail, "fail": n_fail, "unverifiable": 0, "mutants_killed": 0, "mutants": 0}
pathlib.Path(ROOT / "ledgers/SC1/SC1-b.json").write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "fail", n_fail, "verdict", frag["verdict"])
