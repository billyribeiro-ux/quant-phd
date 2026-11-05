"""Writes ledgers/SC1/SC1-b.json (round 12). Rows are evidence written by the verifier from this round's reads and runs."""

import datetime
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE12-SC1-b")
OUT_DIR = "ledgers/SC1/scripts/SC1-b-r12/out"
S = "scripts/SC1-b-r12"

R = []


def row(rid, check, location, status, evidence, fix=""):
    R.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# ---- gates and tools (run this round)
row("b-check-pages", "2.9 structure (check_pages)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", "PASS",
    f"check_pages.py --unit SC1 -> 'check_pages SC1: PASS' (exit 0); --page L04, L05, L06 each PASS. Outputs {OUT_DIR}/check_pages_*.txt, run by {S}/run_gates.sh.")
row("b-check-dag", "2.9 DAG (check_dag)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", "PASS",
    f"check_dag.py --unit SC1 -> 'check_dag SC1: PASS'; check_dag.py --all -> PASS for all 27 units including SC1 ({OUT_DIR}/check_dag_unit.txt, check_dag_all.txt).")
row("b-run-labs", "2.5 labs (run_labs)", "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py", "PASS",
    f"run_labs.py --unit SC1 -> 'run_labs SC1: PASS (11/11)'; --page L04, L05, L06 each 'PASS (1/1)' (exit 0). {OUT_DIR}/run_labs_*.txt.")
row("b-twin-match", "2.5 page code == twin; expected == twin stdout; twin under python -I -W error",
    "course/modules/SC/SC1/L04.html (data-run block and pre.expected); L05.html; L06.html; tests/labs/SC1/lab-SC1-L0[456]-1.py", "PASS",
    f"{S}/checks_b_r12.py ({OUT_DIR}/checks_b_r12.txt): for L04, L05, L06 the twin exits 0 under python -I -W error with 0 stderr bytes, the page code equals the twin (True), and the expected block equals the twin stdout (True). Twin stdout saved as {OUT_DIR}/twin_L04.stdout, twin_L05.stdout, twin_L06.stdout.")
row("b-lab-lint", "2.5 lab twins: ruff and mypy strict", "tests/labs/SC1/ (three slice twins)", "PASS",
    f"ruff check tests/labs/SC1 -> 'All checks passed!'; ruff format --check tests/labs/SC1 -> '11 files already formatted'; mypy --no-incremental on the three twins -> 'Success: no issues found in 3 source files'. Outputs {OUT_DIR}/ruff_labs.txt, ruff_format_labs.txt, mypy_twins.txt.")
row("b-page-smoke", "2.5/2.9 page_smoke (Chromium, both themes, 360 px)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", "PASS",
    f"page_smoke.py --unit SC1 --pages L04.html L05.html L06.html -> 'page_smoke SC1: PASS', exit 0, run twice; the second run had no other process running ({OUT_DIR}/page_smoke_L04_L06_alone.txt). I did not take a screenshot.")
row("b-pytest-tooling", "pytest: lab tooling for SC1 twins", "tests/test_labs.py -k SC1", "PASS",
    f"pytest tests/test_labs.py -q -k SC1 -> 11 dots, exit 0; pytest --co -q -k SC1 -> 'tests/test_labs.py: 11' ({OUT_DIR}/pytest_labs_SC1.txt).")
row("b-verify-refs", "2.1/2.6 registry (verify_refs)", "references/references.json; shreve2004stochastic", "PASS",
    f"verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (exit 0). verify_refs.py --unit SC1 (live re-fetch) -> 'live re-verification of SC1: 1 of 560 entries, 0 problems' ({OUT_DIR}/verify_refs_offline.txt, verify_refs_unit_live.txt). The tool rejects --offline with --unit (exit 2, verify_refs_unit_offline.txt), so the live unit run is the unit check.")
row("b-attribution-references", "2.2 attribution: no passage attributed to a registry source",
    "course/modules/SC/SC1/L04.html (section 8 References); L05.html (section 9); L06.html (section 8)", "PASS",
    "Read in full this round. L04: 'This lesson cites no passage from a registry source'; L05 and L06 give no locator and attribute nothing to shreve2004stochastic. grep for 'Karatzas' in L04, L05, L06 -> no hits (Karatzas & Shreve is not cited).")
row("b-check-projects", "2.6 gate run (check_projects --unit SC1; slice b has no project page)", "course/modules/SC/SC1/project.html (not in slice b)", "PASS",
    f"check_projects.py --unit SC1 -> 'check_projects SC1: PASS' ({OUT_DIR}/check_projects_unit.txt). Reported for completeness; no slice-b row depends on it.")

# ---- cross-lesson references and delta
row("b-cross-L04", "2.8 cross-lesson reference (L04 'Uses' line)", "course/modules/SC/SC1/L04.html:37; L03.html:99-109", "PASS",
    "L04.html:37 reads 'the quadratic variation of Lesson 3 (in Theorem 2.3)'. L03.html:99 is Theorem 2.3 (mean-square limit of the sums of squared increments); its proof (L03.html:109) gives the mean sum t, which the L04 remark (L04.html:126) uses.")
row("b-cross-L05-L06", "2.8 cross-lesson references (L05, L06)", "L05.html:268, 279, 288; L06.html:102, 127, 305", "PASS",
    "L05:268 'M6 Lesson 9, Definition 9.1' = course/modules/M/M6/L09.html:59 (Definition 9.1, stopping time). L05:279 tau_a 'defined in Lesson 6, Section 2' = L06.html section 2 (tau_a defined there). L05:288 finiteness 'a result there' = L08.html:87 (Corollary 1.4, finite with probability one). L06:102 cites Lesson 2 Theorem 2.5 and Remark 2.6 (L02.html:289, 303) with A2 and Assumption 2.1 (L02.html:289-291, 303-308) and Lesson 1 A1(a),(b),(e) (L01.html:72-82). L06:305 'Lesson 8 does' = L08 Corollary 1.3 (L08.html:77) and Corollary 1.5 (L08.html:108).")
row("b-delta-L04-L06-hunks", "2.8 delta 11d7077..5db69a9: every hunk in the slice read and re-derived",
    "L04.html:51, 70, 103, 119, 140, 230, 241, 289, 339; L05.html:52; index.html:69; cards.json c072, c095, c096, c203 (changed), c222, c226, c227, c228 (added)", "PASS",
    "git diff -U0 11d7077 5db69a9 on the slice: nine single-line hunks in L04.html (51 why-it-matters, 70 Assumption 4.2 with new part (e), 103 and 119 proof wording now citing (e), 140 martingale identity, 230 and 241 canon-breaks and misconception wording, 289 P1, 339 R1), one in L05.html (52 why-it-matters), one in index.html (69 hub sentence on labelled standard facts). All read and re-derived this round (rows b-math-L04-*, b-math-L05-*, b-hub-*, b-cards-*). L06.html and the three slice twins have no hunk (byte-identical).")
row("b-delta-cross-lessons", "2.8 delta: effects of other units' hunks on the slice",
    "git diff 11d7077 5db69a9 (whole repository)", "PASS",
    "Outside the slice: curriculum/02-economics-finance-core.yaml and course/assets/data/program.json (FC/Arbitrage scanner brief 'embedded' -> 'SIMULATED'; curriculum/curriculum.json mirrors it); plans/FINAL-ARCHITECT-RULINGS.md ruling 13 (applied to the slice in b-ruling-13-check); cards changed c026, c027, c028, c032, c051, c149, c150, c207; cards added c223-c225, c229, c230 (L02, L03, L07); card removed c219 (L01); other units' tests/labs and ledgers. references/ and notation/ and tools/ have no delta, and no lesson of the slice shares text with these hunks.")
row("b-delta-twins-and-scripts", "2.8 delta: twins",
    "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py", "PASS",
    "git diff 11d7077 5db69a9 -- the three twins is empty; the twins are byte-identical (checks_b_r12 'byte-identical', sizes 2961, 3372, 4133 bytes). The twin outputs in this round are the ones cited below.")

# ---- numbers
row("b-num-L04", "2.2 numbers in prose (L04)", "course/modules/SC/SC1/L04.html (lab output 217-224; M2, E1-E3; quiz items)", "PASS",
    f"{S}/recompute_b_r12.py ({OUT_DIR}/recompute_b_r12.txt, own code): e^1=2.718281828459, e^(1/4)=1.284025416688, e^4=54.598150033144, e^8=2980.957987041728. |e-2.718281828|=4.59e-10 and |e^4-54.598150033|=1.44e-10, inside the 1e-9 quiz tolerances. Simpson on [-14,14] with 60000 nodes gives E[exp(theta B_2)] and E[Z_2]=1.000000000 for theta in {-1,0.5,2}. E[Z_t^2] by quadrature equals exp(theta^2 t) for (theta,t) in {(0.5,1),(2,2),(-1,3)}.")
row("b-num-L05", "2.2 numbers in prose (L05)", "course/modules/SC/SC1/L05.html (lab output 255-262; E1-E3 at 364-384; M2; P2; quiz)", "PASS",
    f"{OUT_DIR}/recompute_b_r12.txt: 5.55e-16/3.81e-29 = 1.4567e13 (E1 'about 1.5x10^13 to two significant figures' is correct); 5.55e-16/2.22e-16 = 2.500 ('about 2.5'); 3.05e-16/2.22e-16 = 1.374 ('about 1.4'); 1/(2 sqrt pi) = 0.2820948; p_1(0,0) = 0.3989423 (quiz 0.3989); Phi(-1/sqrt2) = 0.5 erfc(1/2) = 0.2397500611 (quiz 0.23975). Independent own-code Simpson (6000 intervals) over the 225 cases gives largest gap 1.22e-15; the page's 5.55e-16 is the twin's printed value and the page claims only that value and its rounding scale.")
row("b-num-L06", "2.2 numbers in prose (L06)", "course/modules/SC/SC1/L06.html (lab output 280-296; misconceptions 316-320; E1-E3; quiz)", "PASS",
    f"{OUT_DIR}/recompute_b_r12.txt (own brute force): triples (N,a,b) = 1014 with all equal; pairs (N,a) = 78 = 1+...+12, all equal; N=12, a=3: 1588, 495, 495; N=10, a=2: P(M>=2)=281/512, 2P(S>2)=11/32, P(S=2)=105/512 = C(10,6)/1024, difference equals P(S=2): True; N=3, a=1: 5 of 8; N=2, a=2: 1/4; erfc(1/sqrt2)=0.3173105079, half 0.15865525393 (prints 0.1586552539); half of the printed 0.3173105079 is 0.15865525395 (E3 explanation correct); Corollary 2.6 by quadrature agrees with erfc to 9 decimals at (t,a) in {(1,1),(2,0.5),(0.5,1.5)}; M3 walk S=(0,1,2,1,0,1), kappa=2, S'=(0,1,2,3,4,3), 4-S_k = (2,3,4,3).")

# ---- labs
row("b-lab-L04-hypothesis", "2.5 lab hypothesis matches code", "course/modules/SC/SC1/L04.html:147; tests/labs/SC1/lab-SC1-L04-1.py", "PASS",
    "Hypothesis: t=2, theta in {-1,0.5,2}; relative 1e-9 for E[e^(theta B_t)] against e^(theta^2 t/2); absolute 1e-9 for E[Z_t] against 1; Lemma 2.1 with h=t is the closed form. Twin: THETAS=(-1.0, 0.5, 2.0), TIME=2.0, TOL=1e-9, 'mgf_ok = abs(mgf - closed) <= TOL * closed', 'martingale_ok = abs(martingale - 1.0) <= TOL'. Matches.")
row("b-lab-L04-interpretation", "2.5 lab interpretation vs output", "course/modules/SC/SC1/L04.html:224", "PASS",
    "Printed lines (expected block and twin_L04.stdout): 2.718281828, 1.284025417, 54.598150033 = e^1, e^(1/4), e^4 for theta = -1, 0.5, 2 (theta^2 t/2 = 1, 0.25, 4); E[Z_t] prints 1.000000000 each. The text says the check is numerical at one time and three thetas and does not prove the martingale property for other theta and t; Proposition 2.4 is the proof. Consistent.")
row("b-lab-L04-docstring", "2.4 twin docstring vs code", "tests/labs/SC1/lab-SC1-L04-1.py (module docstring; main())", "PASS",
    "Docstring: B_t normal with mean 0 and variance t; composite Simpson with PANELS panels on [-LIMIT, LIMIT]; the mass beyond LIMIT is not computed; finite computations are not a proof. main() prints a header and two checks per theta with the tolerances stated; nothing else is printed (twin_L04.stdout, 7 lines). Consistent.")
row("b-lab-L05-docstring-quadrature", "2.4 twin docstring vs code", "tests/labs/SC1/lab-SC1-L05-1.py (docstring; tail_mass; chapman_kolmogorov_gap; main)", "PASS",
    "Docstring: Simpson on [-12,12], 225 cases, mass for 12<=|z|<=40 computed and printed, gaps at rounding scale, the exact identity is proved on the page. Code: INTERVALS=2000, TOLERANCE=1e-6; tail_mass integrates [12,40] and [-40,-12]; main prints the case count, the largest gap, the largest tail mass, one example gap and the three integrals. Consistent.")
row("b-lab-L05-hypothesis-interpretation", "2.5 lab hypothesis and interpretation vs output", "course/modules/SC/SC1/L05.html:170, 263, 306", "PASS",
    "Hypothesis constants match the twin: TIMES (0.5,1,2) and POINTS (-1,-0.25,0,0.5,1), 3*3*5*5 = 225 cases, tolerance 1e-6. Printed: 225 cases, largest gap 5.55e-16 (True below 1e-06), largest tail mass 3.81e-29, integrals 1.0000000000 at t = 0.5, 1, 2. Interpretation limited to the 225 points and the printed values; the identity is attributed to Theorem 2.1 (not the lab). Consistent.")
row("b-lab-L05-gap-carry", "2.5 lab output carried into prose", "course/modules/SC/SC1/L05.html:256-262", "PASS",
    "The figures quoted (5.55e-16, 3.81e-29, the ten-digit integrals, the -3.05e-16 example) equal the printed expected block (twin_L05.stdout).")
row("b-lab-L06-claims", "2.5 lab claims vs output", "course/modules/SC/SC1/L06.html:186, 297", "PASS",
    "Printed (twin_L06.stdout): 'triples (N, a, b) checked: 1014; equal: 1014'; 'pairs (N, a) checked: 78; equal: 78'; Part C 1588, 495, 495; Part D 281/512, 11/32, 105/512, True; Part E 0.3173105079 and 0.1586552539. The hypothesis (L06:186) and interpretation (L06:297) describe exactly these printed results.")
row("b-lab-L06-docstring-exact-fraction", "2.4 twin docstring vs code", "tests/labs/SC1/lab-SC1-L06-1.py (docstring; main())", "PASS",
    "Docstring: N from 1 to 12 with 1<=a<=N and b<a with b>=-N; code loops range(1, n+1) for n, range(1, n+1) for a, range(-n, a) for b. Counts are exact integers; Part D uses Fraction; Part E is floating point. Consistent.")
row("b-ck-independent-L05", "2.5 lab reproduced by an independent method", "course/modules/SC/SC1/L05.html:255-263; tests/labs/SC1/lab-SC1-L05-1.py", "PASS",
    f"{OUT_DIR}/recompute_b_r12.txt: own Simpson with 6000 intervals on [-14,14] over the same 225 cases: largest gap 1.22e-15 (below 1e-6), i.e. at rounding scale as the page says. Lemma 2.2 identity exact in Fractions on sampled rational points: True.")

# ---- mathematics: Section 2 (L04)
row("b-math-L04-lemma-2.1", "2.4 mathematics: Lemma 2.1 (MGF of a normal)", "course/modules/SC/SC1/L04.html:81-89", "PASS",
    "Completing the square theta*y - y^2/(2h) = theta^2 h/2 - (y - theta h)^2/(2h) re-derived by expansion; the shifted density integrates to 1; grade T with h>0 stated.")
row("b-math-L04-prop-2.2", "2.4 mathematics: Proposition 2.2 (B is a martingale)", "course/modules/SC/SC1/L04.html:93-105 (proof line 103 changed this round)", "PASS",
    "(ii) E[B_t^2]=t by (D2) of Lesson 1 (L01.html:62). (iii) E[B_t | F_s] = B_s + E[Y | F_s] by Assumption 4.2(a), (c) and (e) (L04.html:103 now cites (e), which gives E[B_s | F_s] = B_s); E[Y | F_s] = E[Y] = 0 by Assumption 4.1 and 4.2(d) (E[Y]=0 by (D2)). Re-derived; the unlisted E[1|G]=1 is now Assumption 4.2(e).")
row("b-math-L04-prop-2.3", "2.4 mathematics: Proposition 2.3 (B_t^2 - t is a martingale)", "course/modules/SC/SC1/L04.html:109-123 (lines 119-121 changed this round)", "PASS",
    "E[B_t^4]=3t^2 from Lemma 2.2 of Lesson 3 (L03.html:89-97: E[X^4]=3Delta^2) ; E[(B_t^2-t)^2]=3t^2-2t^2+t^2=2t^2; E[B_t^2 | F_s] = B_s^2 + 2B_s*0 + h with 4.2(a),(c),(e); E[B_t^2 - t | F_s] = B_s^2 + h - t = B_s^2 - s. Re-derived.")
row("b-math-L04-prop-2.4", "2.4 mathematics: Proposition 2.4 (exponential martingale)", "course/modules/SC/SC1/L04.html:129-149 (line 140 changed this round)", "PASS",
    "E[Z_t^2] = e^(-theta^2 t) E[e^(2 theta B_t)] = e^(theta^2 t) by Lemma 2.1 with 2 theta. W = exp(theta Y - theta^2 h/2): E[W^2] = e^(theta^2 h) and E[W] = 1 by Lemma 2.1. The s=t case uses 4.2(c) and (e) with Y=1 (L04.html:140). Re-derived.")
row("b-math-L04-A4.1-sketch", "2.4 sketch labelled and names skipped steps", "course/modules/SC/SC1/L04.html:63-65", "PASS",
    "Labelled 'Sketch, not a proof, for the natural filtration of B'; names the pi-system of cylinder sets and the pi-lambda extension as skipped steps; cites L03 Assumption 3.2(a) (L03.html:71), which covers functions of single variables only.")
row("b-math-L04-misconception-1", "2.4 misconception 1 (mean zero is not a martingale)", "course/modules/SC/SC1/L04.html:241 (changed this round)", "PASS",
    "E[B_t^3]=0 by symmetry; (B_s+Y)^3 expansion gives E[X_t | F_s] = B_s^3 + 3(t-s)B_s using 4.2(a),(c),(d),(e); differs from B_s^3 iff B_s != 0 for s<t. Re-derived.")
row("b-math-L04-misconception-2", "2.4 misconception 2 (exp(theta B) is not a martingale)", "course/modules/SC/SC1/L04.html:245", "PASS",
    "E[e^(theta B_t)] = e^(theta^2 t/2) (Lemma 2.1) is not constant in t for theta != 0; a martingale has constant expectation by the tower property (4.2(b)). Re-derived.")
row("b-math-L04-R1-R3", "2.4 research problems R1-R3 (L04)", "course/modules/SC/SC1/L04.html:336-353 (line 339 changed this round)", "PASS",
    "R1: B_t^2 - g(t) = (B_t^2 - t) + k(t), k(t) = t - g(t); E[k(t) | F_s] = k(t) by 4.2(c),(e), so k is constant and g(t) = t + c. R2: E[Z_t | F_s] = Z_s e^(c^2 h/2), so c^2 h = 0 and c = 0. R3: conditional variance t - s. Re-derived.")
row("b-math-L04-M1-M3", "2.4 mechanics problems M1-M3 (L04)", "course/modules/SC/SC1/L04.html:261-279", "PASS",
    "M1 E[B_t^2]=t, E[B_t^4]=3t^2; M2 E[e^(B_2)] = e and E[Z_2] = 1 for Z_t = exp(B_t - t/2); M3 Var(Z_t) = e^(theta^2 t) - 1, zero at theta=0. Re-derived.")
row("b-math-L04-E1-E3", "2.4 empirical problems E1-E3 (L04)", "course/modules/SC/SC1/L04.html:311-328", "PASS",
    "E1 e^(0.25)=1.284025417 (printed value); E2 e^8 = 2980.957987 (six decimals); E3 theta=2, t=4 gives e^(4*4/2) = e^8. Lab 1 prints only t=2 (L04.html:256 says E2 and E3 are not printed). Re-derived.")
row("b-assumed-L04-E2", "2.1 item 6 ('Assuming') rule", "course/modules/SC/SC1/L04.html:321", "PASS",
    "E2 solution opens 'Assuming Assumptions 4.1 and 4.2, Proposition 2.4 gives E[Z_t^2] = e^(theta^2 t)'.")

# ---- mathematics: Section 1-3 (L05)
row("b-math-L05-lemma-1.3", "2.4 mathematics: Lemma 1.3 (future increment independent of past)", "course/modules/SC/SC1/L05.html:89-103", "PASS",
    "Proof re-derived: (D3) gives mutual independence over 0=r_0<...<r_k=s<t and t; A4(f) gives independence of (B_r1..B_rk) from B_t - B_s; cylinder events form a pi-system generating F_s (any finite time set is enlarged to contain 0 and s without changing the event); A4(a) extends. s=t and s=0 (F_0 generated by B_0=0) handled.")
row("b-math-L05-thm-1.4", "2.4 mathematics: Theorem 1.4 (Markov property at fixed times)", "course/modules/SC/SC1/L05.html:105-123", "PASS",
    "A4(b) with Z=B_s, Y=B_t-B_s, f(z,y)=g(z+y), bounded and jointly measurable; f-bar(z)=E[g(z+B_t-B_s)] = int g(y) p_{t-s}(z,y) dy by substitution y=z+w and phi_u(y-z)=p_u(z,y). s=t case: g(B_t) is F_t-measurable. Re-derived.")
row("b-math-L05-lemma-2.2-thm-2.1", "2.4 mathematics: Lemma 2.2 and Theorem 2.1 (Chapman-Kolmogorov)", "course/modules/SC/SC1/L05.html:134-166", "PASS",
    f"Lemma 2.2 identity re-derived by expansion (L05 proof) and checked exactly in Fractions on sampled rational points ({OUT_DIR}/recompute_b_r12.txt: True). Constants: (2pi)^(-1)(uv)^(-1/2)(2pi uv/(u+v))^(1/2) = (2pi(u+v))^(-1/2), and the powers of uv cancel.")
row("b-math-L05-A4i-statement", "2.4 A4(i) statement and use", "course/modules/SC/SC1/L05.html:69, 327, 444; cards.json SC1-c214", "PASS",
    "A4(i) stated at L05.html:69 with the finiteness condition on f-bar; used at L05:327 (Problem M2) and in the quiz explanation (L05:444); card c214 consistent.")
row("b-math-L05-A3-sketch", "2.4 A3 sketch labelled and names skipped steps", "course/modules/SC/SC1/L05.html:270-281", "PASS",
    "A3 is an Assumption (not proved). Sketch labelled 'Sketch, not a proof'; dyadic rho_n with rho <= rho_n <= rho + 2^-n (Problem R3, L05:402-408); the fixed-time case; the two skipped steps (i) extension of independence (A4(a)) and (ii) limit passage named; A cap {rho_n=q} in F_q via F_rho subset F_{rho_n}. The sketch states it does not check that the limit identifies the law. Re-derived.")
row("b-math-L05-R3", "2.4 mathematics: Problem R3 (dyadic approximation)", "course/modules/SC/SC1/L05.html:402-408", "PASS",
    "x <= ceil(x) < x+1 gives rho <= rho_n < rho + 2^-n; {rho_n <= r} = {rho <= k/2^n} with k = floor(2^n r), which lies in F_{k/2^n} subset F_r. Re-derived.")
row("b-math-L05-problems", "2.4 mathematics and labs: L05 problem set", "course/modules/SC/SC1/L05.html:316-400", "PASS",
    "M1 integral 1/(2 sqrt pi) and p_2(0,0)=1/(2 sqrt pi); M2 psi(x)=x^2+2 and x^3+6x from E Z=0, E Z^2=2, E Z^3=0; M3 Cov(B_2-B_1,B_1)=0 with Proposition 1.2 of Lesson 1 and A1(c) of Lesson 1 (L01.html:76); P1 identity at u=1,v=3,x=0,y=1 gives (4z^2-2z+1)/3 on both sides; P2 Phi((c-x)/sqrt(t-s)); P3 substitution; R1 the two paths agree on [0,1/2] with eta* = 1/4 and 3/4, and A4(d) rules out membership in F_{1/2}; R2 F_s subset F_rho for a constant rho and A3 gives independence. Re-derived.")
row("b-math-L05-misconceptions", "2.4 misconceptions (L05)", "course/modules/SC/SC1/L05.html:297-306", "PASS",
    "Misconception 1: P2 gives N(B_s, t-s), mean B_s. Misconception 2: p_{t-s}(x,.) centred at x with variance t-s coincides with p_t(0,.) only when x=0 and s=0. Misconception 3: 225 cases do not prove Chapman-Kolmogorov. Re-derived.")
row("b-math-L05-def-1.1-st-case", "2.4 Definition 1.1 covers s=t", "course/modules/SC/SC1/L05.html:75-78, 122", "PASS",
    "Definition 1.1 is stated for 0<=s<=t; the s=t case in Theorem 1.4 uses that g(B_t) is F_t-measurable, so E[g(B_t) | F_t] = g(B_t) (standard property of conditional expectation, named in the sentence).")
row("b-math-L05-E1-E3", "2.4 / 2.2 problems E1-E3 (L05) numbers", "course/modules/SC/SC1/L05.html:364-384", "PASS",
    "E1: 5.55e-16 vs 3.81e-29 (printed), ratio 1.457e13 ('about 1.5x10^13' to two significant figures; basis: printed values to three significant figures, stated). E2: ten printed decimals give an error bound of 5e-11. E3: 3.05e-16 is 1.37 times the machine epsilon 2.22e-16. Recomputed in recompute_b_r12.txt.")
row("b-scope-L05-E1-tail", "2.2 scope of E1 claim", "course/modules/SC/SC1/L05.html:368", "PASS",
    "'so that part of the tail cannot account for the gaps' is backed by the printed 3.81e-29 vs 5.55e-16; the page declines any claim about |z| > 40 ('makes no claim that it is small').")
row("b-math-L05-quiz-Q7", "2.5 quiz item (sketch step)", "course/modules/SC/SC1/L05.html:479-485", "PASS",
    "Correct option names the extension of independence to the whole shifted path and the passage to the limit, matching the sketch at L05.html:281.")
row("b-quiz-L05-Q7", "2.5 quiz explanation", "course/modules/SC/SC1/L05.html:485", "PASS",
    "Explanation: the sketch proves the fixed-time case, sums over countably many dyadic values, and names two skipped steps; matches L05.html:281.")
row("b-assumed-L05-quiz-Q9", "2.1 item 6 (assumed facts in quiz)", "course/modules/SC/SC1/L05.html:496-499", "PASS",
    "Numeric item answer 0.23975 (tolerance 1e-5): Phi(-1/sqrt2) = 0.2397500611 (recomputed). Explanation cites A4(a), A4(b), A4(f) and Problem P2 (Theorem 1.4 with the indicator).")
row("b-assumed-L05-quiz-M2", "2.1 item 6 (assumed facts in quiz)", "course/modules/SC/SC1/L05.html:441 (quiz numeric item 2)", "PASS",
    "Numeric item answer 3 = B_1^2 + 2 with B_1 = 1 (M2 solution); explanation cites A4(a), A4(f), A4(i).")
row("b-scope-L05-canonical", "2.2 canon-breaks scope claim", "course/modules/SC/SC1/L05.html:284-289", "PASS",
    "'Unbounded stopping times' bullet: A3 requires rho <= c; finiteness of tau_a is a result of Lesson 8 (L08.html:87, Corollary 1.4).")
row("b-notation-L05-Phi-varphi", "2.2 notation: Phi and varphi", "course/modules/SC/SC1/L05.html (P2 solution; quiz item 9; Theorem 1.4 proof)", "PASS",
    "Phi is used only as the standard normal distribution function (registered symbol '\\Phi, \\Phi^{-1}': standard normal CDF and its inverse, notation/notation.json). varphi_u is a local Gaussian density in the Theorem 1.4 proof, not a registered symbol.")
row("b-notation-L05-X-n", "2.2 notation: local symbols", "course/modules/SC/SC1/L05.html:281", "PASS",
    "X^(n) and rho_n are defined at L05.html:281 before use and are not registered symbols.")
row("b-notation-M-clash", "2.2 notation: M symbols", "course/modules/SC/SC1/L05.html (no M_t symbol: grep count 0); course/modules/SC/SC1/L06.html:52, Lemma 2.1, Section 1", "PASS",
    "Corrected citation (round 11 cited L05.html:52 and 268 for M_t; neither contains M_t). M_t is defined in L06 (why-it-matters L06.html:52; Lemma 2.1) and M_N in L06 Section 1. Neither is a registered symbol. Problem labels M1-M3 are labels.")
row("b-scope-L05-D1D3", "2.9 A4 parts used in Sections 1-2", "course/modules/SC/SC1/L05.html (Section 1 intro; Lemma 1.3; Theorem 1.4; Theorem 2.1)", "PASS",
    "Sections 1 and 2 use A4(a), (b), (e), (f): Lemma 1.3 uses A4(a),(f); Theorem 1.4 uses A4(b); Theorem 2.1 uses A4(e). No other A4 part is used in Sections 1-2.")
row("b-term-almost-surely", "2.5 undefined term before use", "course/modules/SC/SC1/L05.html:62, 76; L06.html:144", "PASS",
    "'almost surely' is defined in place in A4(b) ('that is, with probability one') before its first use in Definition 1.1 (L05.html:76).")

# ---- mathematics: L06 (byte-identical page)
row("b-math-L06-facts-unnumbered", "2.4 facts used without proof are named", "course/modules/SC/SC1/L06.html:102-130", "PASS",
    "Section 2 facts are Lesson 2 results (Remark 2.6, Theorem 2.5) and the numbered A3 and A4 of Lesson 5, each named as an assumption at L06.html:102 and 126-128. None is presented as proved here.")
row("b-math-L06-prop-1.3-cor-1.4", "2.4 mathematics: Proposition 1.3 and Corollary 1.4", "course/modules/SC/SC1/L06.html:74-98", "PASS",
    f"M_N >= a iff kappa <= N (the walk moves by +-1 from 0 < a); the reflection of Lemma 1.2 maps {{kappa<=N, S_N=b}} to {{S_N=2a-b}}; the sum over b<a maps onto the integers above a, giving #{{S_N>a}}. Exact counts confirm ({OUT_DIR}/recompute_b_r12.txt).")
row("b-math-L06-lemma-2.1", "2.4 mathematics: Lemma 2.1 (running maximum and first visit)", "course/modules/SC/SC1/L06.html:104-115", "PASS",
    "(i) {M_t>=a} = {tau_a<=t} by IVT and closedness of {s : B_s=a}; (ii) IVT on [0,t]; (iii) IVT on (0,s) for B_s>a, then B_t != a since t < tau_a. Re-derived.")
row("b-math-L06-prop-2.3-thm-2.5", "2.4 mathematics: Proposition 2.3 and Theorem 2.5", "course/modules/SC/SC1/L06.html:122-171", "PASS",
    "rho = tau_a ^ t is a stopping time by A4(c) and {rho<=r} = {tau_a<=r} for r<t; W_t = B_rho - X_{t-rho}; A4(b) with f_(-/+) gives E[g(W_t)|F_rho] = h_-(B_rho,t-rho) and E[g(B_t)|F_rho] = h_+(B_rho,t-rho); symmetry of N(0,u) gives h_- = h_+. Theorem 2.5: E = {W_t > a} (on {tau_a>t}, W_t = B_t < a), so P(tau_a<=t) = P(B_t>=a) + P(B_t>a) = 2P(B_t>a), with P(B_t=a)=0. Re-derived.")
row("b-math-L06-def-2.2-remark-2.4", "2.4 Definition 2.2 and Remark 2.4 scope", "course/modules/SC/SC1/L06.html:117-121, 147-150", "PASS",
    "Definition 2.2 states the path-level reflection and says it is not asserted from A3 (bounded stopping times only) and not proved here; Remark 2.4 says Proposition 2.3 is about one time at a time. The page is internally consistent. Whether the plan requires the path-level claim is row b-plan-L06-pathlevel.")
row("b-math-L06-cor-2.6", "2.4 mathematics: Corollary 2.6 (closed form)", "course/modules/SC/SC1/L06.html:173-182", "PASS",
    "z = sqrt2 w substitution gives 2P(B_t>a) = erfc(a/sqrt(2t)); recomputed by quadrature at three (t,a) pairs to 9 decimals (recompute_b_r12.txt).")
row("b-math-L06-R1-R3", "2.4 research problems R1-R3 (L06)", "course/modules/SC/SC1/L06.html:406-426", "PASS",
    "R1 parity: S_N has the parity of N, both sides vanish otherwise, and 2a-b = b mod 2. R2: min B <= -a iff max(-B) >= a; Theorem 2.5 for -B gives 2P(B_t<-a). R3: 2x > x for x > 0 and the normal law gives positive mass to half-lines. Re-derived.")
row("b-math-L06-E1-E3", "2.4 empirical problems E1-E3 (L06)", "course/modules/SC/SC1/L06.html:382-402", "PASS",
    "E1: 1+...+12 = 78. E2: 281/512 - 352/1024 = 210/1024 = 105/512 = C(10,6)/1024. E3: half of 0.3173105079 is 0.15865525395; the unrounded half 0.15865525393 prints as 0.1586552539 (recompute_b_r12.txt).")
row("b-math-L06-M-P-problems", "2.4 mechanics and proof problems (L06)", "course/modules/SC/SC1/L06.html:334-378", "PASS",
    "M1: 5 of 8 sequences, and Corollary 1.4 gives 4+1 (recomputed). M2: P(M_2>=2) = 1/4. M3: S=(0,1,2,1,0,1), kappa=2, S'=(0,1,2,3,4,3), S'_k = 4-S_k for k>=2. P1 involution; P2 Lemma 2.1 (ii),(iii) from continuity; P3 Corollary 1.4 from Proposition 1.3. Re-derived.")
row("b-scope-L06-only-events", "2.2 scope words (L06)", "course/modules/SC/SC1/L06.html:52, 297, 302-309", "PASS",
    "'only', 'exactly' and 'every' are used with computations or with the enumerated range (N<=12, 1<=a<=N). The 'Discrete grid' and 'Symmetry' canon bullets make no claim beyond the stated cases.")
row("b-scope-L06-N12-every-case", "2.2 scope: every N and a checked", "course/modules/SC/SC1/L06.html:297; tests/labs/SC1/lab-SC1-L06-1.py", "PASS",
    f"Parts A and B loop over every N in 1..12 and every a in 1..N: 1014 and 78 cases, all equal ({OUT_DIR}/twin_L06.stdout; recompute_b_r12.txt agrees).")
row("b-rounding-L06-misconception", "2.2 rounding of prose numbers", "course/modules/SC/SC1/L06.html:316", "PASS",
    "2P(B_1>1) = 0.31731 -> 0.3173 and P(B_1>=1) = 0.158655 -> 0.1587, both to four places as stated.")
row("b-plan-L06-pathlevel", "2.9 plan conformance: L06 mandatory content (plans/SC1-build-plan.md section 3)",
    "course/modules/SC/SC1/L06.html:118-121 (Definition 2.2), 149 (Remark 2.4); plans/SC1-build-plan.md section 3 (L06 line); plans/SC1-open-items.md", "FAIL",
    "The plan's binding L06 content is 'the reflected path after tau_a is a Brownian motion (Assuming A3)'. The page does not prove it: Remark 2.4 says the path-level statement is not used and not claimed, and the builder's open-items file records it as a deviation with 'Status: open'. Rounds 10 and 11 recorded this as an observation; this round treats it as an unmet plan requirement under VERIFIER 2.9. The mathematics that the page does state is correct (rows b-math-L06-*).",
    "Either (a) prove the path-level statement once the finiteness of tau_a is available, i.e. as a result placed after Lesson 8 Corollary 1.4 with a forward reference from L06 stated as such, or (b) the architect rules in writing that the path-level statement is an agreed gap for SC1 and amends plans/SC1-build-plan.md section 3 and closes the open item. Until one of these is recorded, this row stays FAIL.")
row("b-causal-L06-symmetry-last-step", "2.2 causal wording (factor 2)", "course/modules/SC/SC1/L06.html:306; L06.html:144, 169-170", "PASS",
    "'The factor 2 comes from adding two events of equal probability': P(tau_a<=t) = P(B_t>=a) + P(E), with P(E) = P(B_t>a) (L06.html:169-170); the symmetry step h_- = h_+ (L06.html:144) uses only the symmetry of N(0,u).")
row("b-l06-assumption-scope", "2.4 assumption scope statement", "course/modules/SC/SC1/L06.html:307, 159-160", "PASS",
    "'Theorem 2.5 is conditional on A3 and A4 of Lesson 5, which are stated and not proved there' matches the Theorem 2.5 statement (L06.html:159-160).")
row("b-l06-canon-symmetry-attribution", "2.2 attribution in canon section", "course/modules/SC/SC1/L06.html:300-307", "PASS",
    "The canon section attributes nothing to an external source and gives no theorem number of one.")
row("b-causal-L06-remark-2.4", "2.2 causal wording (path-level)", "course/modules/SC/SC1/L06.html:130, 149", "PASS",
    "Remark 2.4 says Proposition 2.3 is about one time at a time and that the path-level statement is not used and not claimed; consistent with L06.html:130.")
row("b-hyp-L06-102-lesson2-hypotheses", "2.9 cross-lesson hypotheses (L06 -> L02)", "course/modules/SC/SC1/L06.html:102; L02.html:289-291, 303-308", "PASS",
    "Carried from round 11 (course/modules/SC/SC1/L02.html and L06.html:102 byte-identical since 11d7077; L02.html is not in the delta): Lesson 2 Theorem 2.5 hypothesis 'Assuming A2 and Assumption 2.1' (L02.html:289-291) and Remark 2.6 hypothesis 'Assuming A1(a), A1(b), A1(e), A2 and Assumption 2.1' (L02.html:303-308) match L06:102.")
row("b-ivt-observation", "2.4 IVT hypotheses", "course/modules/SC/SC1/L06.html:104, 112, 114", "PASS",
    "IVT applied on [0,s*] and on [0,t] with B_0 = 0 < a; continuity is named as a hypothesis (L06.html:104).")
row("b-quiz-L06-Q8", "2.5 quiz numeric item", "course/modules/SC/SC1/L06.html:508-511", "PASS",
    "Answer 0.1587 (tolerance 1e-4) against P(B_1>=1) = 0.1586552539 (recomputed). Explanation: half of erfc(1/sqrt2) = 0.15865..., and P(B_1>1) = P(B_1>=1) because B_1 has no atom.")

# ---- cards
row("b-cards-c061-c072", "2.7 cards (sampled, 1 per 10, L04)", "course/modules/SC/SC1/cards.json c061-c072", "PASS",
    "c061-c065 match L04.html:59 (Definition 1.1), 64 (Definition 1.1 filtration/natural filtration), 70 (Assumption 4.1/4.2 blocks), 75 (Definition 1.2). c066 Lemma 2.1 (L04:82); c067 Proposition 2.2 (L04:98); c068 Proposition 2.3 (L04:114, 122-123); c069 remark (L04:126); c070 Proposition 2.4 (L04:134, 140-142); c071 second moment (L04:139). c072 changed this round: front now asks for theta = 2 only; back '54.598150033 for E[e^(2B_2)], equal to e^4 within 1e-9' matches the expected block (L04:217-223). Grades and bases agree with the key-results table (Lab 1 row graded C).")
row("b-cards-c073-c085", "2.7 cards (L04 and L05, sampled)", "course/modules/SC/SC1/cards.json c073-c084 (no c085)", "PASS",
    "c073 (L04:230, canon break; the card does not depend on the changed sentence), c074 (L04 section 3), c075 (L04 section 3, optional stopping), c076 (L04:241), c077 (L04:245), c078 (L04 misconception 3, L04:249), c079 (L04:336-339), c080 (L04:343-346), c081 (L04:296), c082 (L04:303), c083 (L05 Definition 1.1), c084 (L05 Definition 1.2). Each agrees with its passage. No card c085 exists (c084 is followed by c086).")
row("b-cards-c086-c097", "2.7 cards (L05, sampled)", "course/modules/SC/SC1/cards.json c086-c097", "PASS",
    "c086 (L05:89-96), c087 (L05:105-116), c088 (L05:125-128), c089 (L05:134-138), c090 (L05:146-152), c091 and c092 (lab output L05:255-262; grade C, basis Lab 1), c093 (L05:270-277), c094 (L05:268), c095 changed this round (R2 solution, L05 R2), c096 changed this round (R3 bounds only, L05:402-408), c097 (L05 R1, A4(d)). Each agrees with the current text.")
row("b-cards-c098-c110", "2.7 cards (L05 and L06, sampled)", "course/modules/SC/SC1/cards.json c098-c110", "PASS",
    "c098 (L05:287), c099 (L05:288), c100 (L05:298), c101 (L05:302), c102 (L05:305-306; 'rounding' in the card is floating-point rounding, not a process word), c103 (L05:327), c104 (L05:349-351), c105 (L05:334), c106 (L06:56), c107 (L06:60), c108 (L06:66), c109 (L06:76-84), c110 (L06:89-92). Each agrees with its passage.")
row("b-cards-c111-c122", "2.7 cards (L06 lab and proof cards)", "course/modules/SC/SC1/cards.json c111-c122", "PASS",
    "c111 (1014 triples, lab grade C); c112 (78 pairs, grade C); c113 (281/512, 11/32, 105/512; grade C); c114 (495, 495 with 2a-b=4; grade C); c115 (erfc(1/sqrt2) = 0.3173 = 2P(B_1>=1); grade T); c116-c118 (Lemma 2.1 (i)-(iii), T, L06:104-115); c119 (Definition 2.2, which form is proved); c120 (Proposition 2.3, T); c121 (explicit form, T); c122 (Remark 2.4: 'No'). Each agrees with its passage and with the Lab 1 printed values (recompute_b_r12.txt).")
row("b-cards-c123-c133", "2.7 cards (L06 theorem, misconception, problem cards)", "course/modules/SC/SC1/cards.json c123-c133 (c125 absent)", "PASS",
    "c123 (Theorem 2.5, T), c124 (Corollary 2.6, T), c126 (misconception, T, 0.3173 vs 0.1587), c127 (grade C, Corollary 1.4 and Lab 1 Part D: 105/512), c128 (T), c129 (M1: 5 of 8, T), c130 (R1 parity, T), c131 (R2 min via -B, T), c132 (R3 strict inequality, T), c133 (rho bounded by t, T). c125 is not present. Each agrees with its passage.")
row("b-cards-duplicates", "2.7 full scan for duplicates", "course/modules/SC/SC1/cards.json", "PASS",
    "216 cards, 0 duplicate ids. Slice cards (lesson L04, L05, L06): 90 (L04 27, L05 35, L06 28). Relative to the round-11 pin: c222, c226, c227, c228 added to the slice; c219 (L01) removed. No duplicate statements among the slice cards.")
row("b-cards-ellipsis", "2.9 ellipses (observation)", "L05.html:100; L06.html:56, 386; cards c086, c106, c112", "PASS",
    "Unicode and LaTeX ellipses appear only in finite index lists ('0=r_0<...<r_k=s<t', 'e_1,...,e_N', '1+2+...+12'), not as omitted content. check_pages.py bans only the ellipsis outside code and passes. Same architect item as rounds 9 to 11 (plan 2.2 vs BUILDER_RULES 1.3); recorded as an observation, not a FAIL.")
row("b-dag-D1-D9", "2.9 DAG: concepts outside the closure used by name", "course/modules/SC/SC1/L04.html, L05.html, L06.html and their slice cards", "PASS",
    "check_dag.py PASS. Name scan (grep, case-insensitive) over the three pages and the 90 slice cards for Ito, geometric Brownian, Ornstein, Euler, Milstein, Girsanov, Feynman, Black-Scholes, barrier, Monte Carlo, Donsker, Levy, Poisson, SDE, change of measure, risk-neutral, bridge: no hits.")
row("b-process-words", "2.9 process words in learner text", "course/modules/SC/SC1/L04.html, L05.html, L06.html; slice cards", "PASS",
    "grep for builder, verifier, round (as a word), REQUEST, planner, architect, fixer, unit report over the pages and the slice cards: no hits (the only regex hit, card c102, is the word 'rounding').")
row("b-banned-phrases", "2.9 banned phrases", "course/modules/SC/SC1/L04.html, L05.html, L06.html", "PASS",
    "grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly: no hits. check_pages PASS.")
row("b-hours-L04-L06", "2.9 hours arithmetic", "course/modules/SC/SC1/index.html:29; L04.html, L05.html, L06.html data-hours", "PASS",
    "index.html:29 data-hours-lessons=72, data-hours-project=28 (sum 100 = curriculum figure). Eight lessons with data-hours 9 each (72); L04, L05, L06 each declare 9.")
row("b-hub-L04-description", "2.9 hub description of slice lessons", "course/modules/SC/SC1/index.html:150; cards in index 155-157; index:52-54", "PASS",
    "index.html:150: 'Lesson 4 covers continuous-time martingales. Lesson 5 covers the Markov property. Lessons 6 to 8 cover the reflection principle, the running maximum and first-passage times.' Matches the pages. The changed hub sentence at index.html:69 (labelled standard facts, e.g. Lesson 1 A1) matches L01.html:72 ('standard facts, stated without proof').")
row("b-structure-sections", "2.9 template sections (order and counts)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", "PASS",
    "Order: why-it-matters, core content, inline lab, canon-breaks, misconceptions, problem set (mechanics, proof, empirical, research), key results, retrieval quiz, references. Each page: 3 misconceptions, 12 problems with 12 worked solutions (3 per tier), quiz 11 / 10 / 10 items each with an explanation.")
row("b-struct-why-it-matters", "2.9 why-it-matters length (<=120 words)", "course/modules/SC/SC1/L04.html:51; L05.html:52; L06.html:52", "PASS",
    f"{OUT_DIR}/checks_b_r12.txt: 83 words (L04), 116 (L05, changed line), 118 (L06), math replaced by a placeholder.")
row("b-quiz-L04-Q8-explain", "2.5 quiz explanation (L04)", "course/modules/SC/SC1/L04.html quiz item 'Under Assumptions 4.1 and 4.2, is B_t + t a martingale?'", "PASS",
    "Correct option 'No: its conditional expectation is B_s + t, which is not B_s + s'; explanation cites Problem P1.")
row("b-quiz-L04-L06", "2.5 quiz answers (L04, L05, L06)", "course/modules/SC/SC1/L04.html:398, 403, 417, 449; L05.html:441, 455, 496; L06.html:462, 476, 508", "PASS",
    "Recomputed: L04 answers 3, 27, 2.718281828 (|e - 2.718281828| = 4.59e-10 < 1e-9), 54.598150033 (|e^4 - 54.598150033| = 1.44e-10 < 1e-9), Z_0 = 1. L05 answers 3, 0.3989 (1/sqrt(2 pi) = 0.39894, tolerance 1e-4), 0.23975 (Phi(-1/sqrt2) = 0.2397500611, tolerance 1e-5). L06 answers 0.25, 0.3173 (erfc(1/sqrt2) = 0.3173105, tolerance 1e-4), 0.1587 (0.1586553, tolerance 1e-4). Item counts 11, 10, 10, each with an explanation.")
row("b-observation-transition-terms", "2.2 terms used before definition / consistency", "course/modules/SC/SC1/L05.html:79-86, 115, 419; cards SC1-c084, c087", "PASS",
    "'Gaussian transition density' is defined at L05:79-86 and used consistently as p_u(x,y) in Theorem 1.4, Theorem 2.1 and the cards.")
row("b-l04-problem-set-E-intro", "2.5 lab/problem cross-statement (L04)", "course/modules/SC/SC1/L04.html:256", "PASS",
    "'Problem E1 uses the output of Lab 1; E2 and E3 ask about values that Lab 1 does not print.' E2 (e^8) and E3 (t=4) are not printed by the twin (which prints t=2 only).")
row("b-prose-L04-R2-title", "2.2 prose title vs solution (L04)", "course/modules/SC/SC1/L04.html:343-346", "PASS",
    "Title 'When the exponential exp(cB_t) is a martingale' and statement 'only when c = 0' agree with the solution.")
row("b-prose-L04-remark-numbering", "2.2 cross-reference numbering (L04)", "course/modules/SC/SC1/L04.html:37, 126", "PASS",
    "The remark at L04:126 is unnumbered and is referred to by content only; L04:37 points to Theorem 2.3 of Lesson 3 (no stale remark reference).")
row("b-scope-L04-footer", "2.2 footer claims (L04)", "course/modules/SC/SC1/L04.html footer", "PASS",
    "Footer: Propositions 2.2 to 2.4 are proved from Assumptions 4.1 and 4.2, which are stated and not proved; Lab 1 is labelled a numerical check. Consistent with the page.")
row("b-math-L05-problems-title", "2.2 prose title vs solution (L05)", "course/modules/SC/SC1/L05.html (P1 and P3 headings)", "PASS",
    "P1 'Verify Lemma 2.2 at one point, then in general' and P3 'Normalisation of the transition density' match their solutions.")
row("b-prose-L05-P3-title", "2.2 prose title vs solution (L05, P3)", "course/modules/SC/SC1/L05.html (P3)", "PASS",
    "As for b-math-L05-problems-title: P3 heading and solution agree.")
row("b-prose-L06-P2-title", "2.2 prose title vs solution (L06)", "course/modules/SC/SC1/L06.html (P2)", "PASS",
    "P2 'Parts (ii) and (iii) of Lemma 2.1 from continuity' matches its solution, which proves (ii) and (iii) without (i).")
row("b-prose-L04-P3-title", "2.2 prose title vs solution (L04, P3)", "course/modules/SC/SC1/L04.html:300", "PASS",
    "P3 'The product moment of a martingale at two times' matches its solution (E[Z_s Z_t] = E[Z_s^2]).")
row("b-math-degenerate-L04-lemma-2.1", "2.4 degenerate cases (t = 0; h > 0)", "course/modules/SC/SC1/L04.html:81-82, 139-140", "PASS",
    "Lemma 2.1 requires h > 0 (L04:82); the proof of Proposition 2.4 treats t = 0 separately (L04:139: 'At t = 0 both E[Z_0^2] and e^0 equal 1').")
row("b-math-L04-quiz-degenerate", "2.4 degenerate case in quiz (Z_0)", "course/modules/SC/SC1/L04.html quiz item 'What is Z_0'", "PASS",
    "Z_0 = exp(0) = 1 from B_0 = 0 (D1, L01.html:61); explanation matches.")
row("b-math-L05-P2-hypothesis", "2.5 hypotheses of Problem P2 (L05)", "course/modules/SC/SC1/L05.html:347-351", "PASS",
    "P2 states A4(a), A4(b), A4(f) as the hypotheses of Theorem 1.4 with g = indicator of (-infty, c] (bounded).")
row("b-hub-L06-objective", "2.9 hub objective vs lesson content", "course/modules/SC/SC1/index.html:54; L06.html:118-121, Theorem 2.5, Proposition 2.3", "PASS",
    "Objective 'Prove the fixed-time reflection identity for Brownian motion (Lesson 6, Theorem 2.5), under Assumptions A3 and A4, derive the tail of the running maximum and the first-passage identity, and name every assumption' matches Theorem 2.5, Proposition 2.3 and the stated assumptions (the objective names the fixed-time form, not the path-level one).")
row("b-scope-words-r11", "2.2 scope words (all three pages)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", "PASS",
    "Every scope word (every, all, only, exactly, always, almost surely, converges, any) was read in context this round across the three pages. Each is backed by a proof on the page, a printed finite enumeration with its range (N<=12; the 225 cases), a definition, or an explicit hypothesis. 'Predicted before running' (L04:147, L05:170, L06:186) is a stated prediction checked against the printed output.")
row("b-notation-r11", "2.2 notation registry (all three pages)", "course/modules/SC/SC1/L04.html, L05.html, L06.html; notation/notation.json", "PASS",
    "Macros used: \\E, \\Prob, \\Var, \\Cov, \\R, \\Normal, \\indic, \\Phi (standard normal CDF only), all registered with their registry meanings; \\Normal(0, t-s) uses the variance as the second argument. T is never a math symbol; H is not used; \\mathbb{Q}, \\gamma_3, \\gamma_4, R^\\ast, R_f are not used (eta^\\ast in L05 R1 is a local symbol). Local Greek letters (rho, tau, kappa, theta, psi, varphi, eta) are unregistered and defined where used.")
row("b-recompute-r11", "2.2 recomputation (all slice numbers)", f"{S}/recompute_b_r12.py", "PASS",
    f"Own code, run with python -I -W error: {OUT_DIR}/recompute_b_r12.txt reproduces every number cited in the rows above.")
row("b-verify-refs-r11", "2.6 registry (verify_refs) repeat", "references/references.json", "PASS",
    "Same run as b-verify-refs: offline 560 entries 0 problems; live SC1 1 entry 0 problems.")
row("b-assumed-facts-statement", "2.1 item 6: assumed facts are listed", "course/modules/SC/SC1/L04.html:93, 109, 129; L05.html:89, 105, 146, 270; L06.html:122-130, 153-160, 173-177", "PASS",
    "Every result in L04-L06 that uses Assumption 4.1, 4.2, A3, A4(x) or a Lesson 1-3 fact states 'Assuming ...' or lists it as a hypothesis. The one fact unlisted in round 11 (E[1|G]=1) is now Assumption 4.2(e) (L04.html:70) and is cited where used.")
row("b-notation-r5", "2.2 notation registry (repeat)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", "PASS",
    "Same evidence as b-notation-r11 (re-read this round).")
row("b-recompute-r5", "2.2 recomputation (repeat)", f"{S}/recompute_b_r12.py", "PASS",
    "Same evidence as b-recompute-r11.")
row("b-scope-words-r5", "2.2 scope words (repeat)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", "PASS",
    "Same evidence as b-scope-words-r11 (re-read this round).")
row("b-verify-refs-r5", "2.6 registry (repeat)", "references/references.json", "PASS",
    "Same evidence as b-verify-refs (offline 560 entries 0 problems; live SC1 1 entry 0 problems).")
row("b-math-L04-A4.2-E1G", "2.4 assumptions complete (Assumption 4.2 and E[1|G])", "course/modules/SC/SC1/L04.html:70; uses at L04.html:103, 119-121, 139-140, 230, 241, 289, 339; cards SC1-c203, SC1-c222", "PASS",
    "Round-11 FAIL resolved. Assumption 4.2 now lists (e) E[1|G]=1 (L04.html:70), and the closing sentence 'Taking Y = 1 in (c) and using (e)' is correct. Every use that needed E[1|G]=1 now cites (e). Card SC1-c203 back is updated; card SC1-c222 states (e). check_pages PASS (fresh).",
    "")

row("b-cards-c193-c204", "2.7 cards (L05 assumptions A4(a)-(i), and L04 Assumption 4.2(b),(c),(d))", "course/modules/SC/SC1/cards.json c193-c200, c202-c204, c214; L05.html:58-72; L04.html:70", "PASS",
    "c193-c200 match the A4(a)-(h) items at L05.html:58-72 (block unchanged this round); c214 matches A4(i) (L05.html:69); c202 matches Assumption 4.2(b) (L04.html:70); c203 (4.2(c)) now states the (e) step, matching L04.html:70 after this round's change; c204 matches 4.2(d). Card-to-text agreement holds; the earlier dependency on E[1|G]=1 is closed by Assumption 4.2(e).")
row("b-cards-c079-c088-c100-c119", "2.7 cards (sampled from L04-L06)", "cards c079 (L04:336-339), c088 (L05:125-128), c100 (L05:298), c119 (L06:118-120)", "PASS",
    "c079 is Problem R1 (L04:336-339, with the (c),(e) step); c088 is Remark 1.5 (L05:125-128, continuity not used); c100 is the misconception on the Markov property (L05:298); c119 is Definition 2.2 (L06:118-120, path-level statement not asserted). Each agrees with its passage.")
row("b-cards-c103-c104-hypothesis", "2.7 cards: stated hypotheses", "cards c103 (L05:327), c104 (L05:349-351)", "PASS",
    "c103 states A4(a), A4(f), A4(i) as the hypotheses of Problem M2 (L05:327); c104 states A4(a), A4(b), A4(f) as those of Problem P2 (L05:349-351). Both match.")

# ---- rows new this round
row("b-cards-r12-changed", "2.7 changed cards (round 12)", "course/modules/SC/SC1/cards.json c072, c095, c096, c203", "PASS",
    "c072: front limited to theta=2; back matches L04.html:217-223. c095: front/back limited to 'constant time is a stopping time' (matches L05 R2 solution). c096: back limited to the bounds (matches L05 R3). c203: back now uses (e) (matches L04.html:70). Each agrees with its page passage.")
row("b-cards-r12-added", "2.7 added cards (round 12)", "course/modules/SC/SC1/cards.json c222, c226, c227, c228", "PASS",
    "c222 (Assumption 4.2(e), E[1|G]=1, assumed); c226 (Lab 1 prints E[Z_t]=1.000000000 for each theta; grade C, basis Lab 1, matching L04.html:223); c227 (F_s subset F_rho for a constant rho; Problem R2 solution); c228 (rho_n is a stopping time; Problem R3 solution). Grades and bases consistent with key-results rows.")
row("b-ruling-13-check", "FINAL-ARCHITECT-RULINGS 13: T versus C for worked values", "course/modules/SC/SC1/L04.html, L05.html, L06.html key-results tables and slice cards", "PASS",
    "Lab-only values are graded C naming the lab: L04 key-results row and c072, c226; L05 key-results row and c091, c092, c216; L06 key-results row and c111-c114, c127. Values derived by hand in numbered results are graded T with the result as basis: L04 Lemma 2.1 and Propositions 2.2-2.4 (c066-c071); L05 Lemma 1.3, Theorem 1.4, Theorem 2.1 (c086-c090); L06 Proposition 1.3, Corollary 1.4, Lemma 2.1, Proposition 2.3, Theorem 2.5, Corollary 2.6 (c108-c124). Key-results rows and cards carry the same grade and basis.")

verdict = "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL"
summary_counts = {
    "rows": len(R),
    "pass": sum(r["status"] == "PASS" for r in R),
    "fail": sum(r["status"] == "FAIL" for r in R),
    "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in R),
    "mutants_killed": 0,
    "mutants": 0,
}

frag = {
    "unit": "SC1",
    "slice": "b",
    "round": 12,
    "verifier": "independent verifier (Haiku 5.5), round 12",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0",
    "base": "11d7077a290f7960b183d3a5a6631af4773888f9 (round-11 pin); delta 11d7077..5db69a9 (commits ccaeeaf4 round-10 fixes and 5db69a9 round-11 fixes)",
    "checkout": str(ROOT),
    "scratch": str(ROOT / "ledgers/SC1/scripts/SC1-b-r12"),
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": R,
    "mutants": [],
    "registry_flags": [
        "Karatzas & Shreve (1991, 2nd ed.), the second curriculum source of SC1 (curriculum/03-markets.yaml:524), has no admissible registry record (plans/SC1-build-plan.md B2). No slice-b page cites it; no action for slice b.",
    ],
    "freshness_flags": [],
    "notes": [
        "Slice b = L04, L05, L06 pages, their three lab twins, the hub sentences and rows that cite them, and the cards whose subject is those lessons (90 cards). No project grader is in this slice, so no student-error mutant is counted and mutants is empty (same ruling as rounds 10 and 11).",
        "Round-11 FAIL b-math-L04-A4.2-E1G is resolved in 5db69a9: Assumption 4.2(e) lists E[1|G]=1 and every use cites it (rows re-verified).",
        "Every slice page was read in full this round, line by line, with the math re-derived by own code (recompute_b_r12.py, checks_b_r12.py). Rows citing a passage in a changed hunk were re-verified; the other rows were re-verified too, because the pages were re-read in full.",
        "The only non-PASS row is b-plan-L06-pathlevel: the binding plan requires the path-level reflection claim in L06 (plans/SC1-build-plan.md section 3). The page declines it and the builder's open-items file records it as open. This is a plan-conformance item for the architect, separate from the correctness of the mathematics on the page.",
        "Shared-file checks: check_pages, check_dag (unit and all), check_projects (unit), run_labs (unit and per page), verify_refs (offline and live unit), ruff, mypy and pytest for the slice, and page_smoke for the three pages were all run this round; the full repository gate was not run (only slice-scoped and unit-scoped commands; the architect runs the full gate before a merge).",
        "Not checked: the full repository gate (repo-wide ruff/mypy, full pytest, render_curriculum, build_site --check, fetch_data --check, check_pages/check_dag --all for pages other than SC1, verify_refs over the whole registry live); no screenshot was taken (page_smoke ran in Chromium and reported PASS); Shreve (2004) and Karatzas & Shreve (1991) were not read and no passage is attributed to either; embed_labs --refresh was not run (the page code was compared with the twin and the expected block with the twin stdout instead); the lab twins' runtime under Pyodide is covered only by page_smoke.",
        "Observations (not rows): the ellipsis item from round 9 is still open for the architect; out-of-slice cards changed or removed in the delta (c219 removed in L01) belong to other slices.",
    ],
    "summary": summary_counts,
}

path = ROOT / "ledgers/SC1/SC1-b.json"
path.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", path, "rows", len(R), "verdict", verdict, summary_counts)
