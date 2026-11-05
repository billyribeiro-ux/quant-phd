"""Writes ledgers/SC1/SC1-b.json (round 11, slice b) from the rows below. Standard library only.

Run: python -I -W error make_fragment_r11.py
"""
import json
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE11-SC1-b")
OUT = "out/"
S = "ledgers/SC1/scripts/SC1-b-r11/"

rows = []


def R(i, check, loc, ev, fix="", status="PASS"):
    rows.append({"id": i, "check": check, "location": loc, "status": status, "evidence": ev, "fix": fix})


# ---- gates and tooling (commands run by the verifier; outputs under scripts/SC1-b-r11/out/)
R("b-check-pages", "2.9 structure (check_pages)", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "check_pages.py --unit SC1 -> 'check_pages SC1: PASS', exit 0 (out/check_pages_unit.txt); --page L04, L05, L06 each PASS, exit 0 (out/check_pages_L04.txt, _L05.txt, _L06.txt). Run by scripts/SC1-b-r11/run_gates.sh.")
R("b-check-dag", "2.9 DAG (check_dag)", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "check_dag.py --unit SC1 -> 'check_dag SC1: PASS', exit 0 (out/check_dag.txt).")
R("b-run-labs", "2.5 labs (run_labs)", "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py",
  "run_labs.py --unit SC1 --page L04 / L05 / L06 -> 'run_labs SC1: PASS (1/1)' each, exit 0 (out/run_labs_L04.txt, _L05.txt, _L06.txt).")
R("b-twin-match", "2.5 page code == twin; expected == twin stdout; twin under python -I -W error",
  "course/modules/SC/SC1/L04.html:148-223; L05.html:171-262; L06.html:187-296; tests/labs/SC1/lab-SC1-L0[456]-1.py",
  "scripts/SC1-b-r11/checks_b_r11.py (out/checks_b_r11.txt): for L04, L05, L06 exit 0, stderr 0 bytes, code==twin True, expected==stdout True. Also out/twin_L0x.stdout captured from python -I -W error.")
R("b-lab-lint", "2.5 lab twins: ruff and mypy strict", "tests/labs/SC1/ (three twins)",
  "ruff check tests/labs/SC1/ -> 'All checks passed!'; ruff format --check -> 11 files already formatted; mypy --no-incremental on the three L04-L06 twins -> 'Success: no issues found in 3 source files'. Output in this round's terminal log (not saved as a file).")
R("b-page-smoke", "2.5/2.9 page_smoke (Chromium, both themes, 360 px)", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "page_smoke.py --unit SC1 --pages L04.html L05.html L06.html -> 'page_smoke SC1: PASS', exit 0 (out/page_smoke_L04_L06.txt). The tool prints only a unit-level line; the run was restricted to these three pages.")
R("b-pytest-tooling", "pytest: lab tooling for SC1 twins", "tests/test_labs.py -k SC1",
  "pytest tests/test_labs.py -q -k SC1 -> 11 passed, exit 0 (out/pytest_labs_SC1.txt).")
R("b-verify-refs", "2.6 registry (verify_refs)", "references/references.json",
  "verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline.txt). verify_refs.py --unit SC1 (live re-fetch) -> '1 of 560 entries, 0 problems', exit 0 (out/verify_refs_unit_live.txt). The round-11 registry delta changes only generated_at and used_by of BK1/BK4 and E9/LX1 entries; shreve2004stochastic is unchanged.")
R("b-attribution-references", "2.2 attribution: no passage attributed to a registry source",
  "course/modules/SC/SC1/L04.html:468; L05.html:515; L06.html:536",
  "Each references section states no locator and attributes no claim to shreve2004stochastic (L04:468 'This lesson cites no passage'; L05:515; L06:536). Karatzas & Shreve is not cited. Read in full this round.")
R("b-check-projects", "2.6 gate run (check_projects --unit SC1; slice b has no project page)", "course/modules/SC/SC1/project.html (not in slice b)",
  "check_projects.py --unit SC1 -> 'check_projects SC1: PASS', exit 0 (out/check_projects_SC1.txt). Reported for completeness only; no slice-b row depends on it.")

# ---- cross-lesson and delta
R("b-cross-L04", "2.8 cross-lesson reference (L04 'Uses' line, round-10 FAIL)", "course/modules/SC/SC1/L04.html:37",
  "Round-10 FAIL is fixed in 11d7077: L04.html:37 now reads 'the quadratic variation of Lesson 3 (in Theorem 2.3)'. L03.html:99-104 is 'Theorem 2.3 (mean-square limit of the sums of squared increments)', and its proof (L03.html:109) gives the mean sum t that the L04 remark at L04.html:126 uses. Re-derived this round; no 'Proposition 2.3' of Lesson 3 is referenced any more.")
R("b-cross-L05-L06", "2.8 cross-lesson references (L05, L06)",
  "L05.html:268, 279, 288; L06.html:102, 127, 305",
  "L05:268 'M6 Lesson 9, Definition 9.1' = course/modules/M/M6/L09.html:59 (Definition 9.1 stopping time) PASS. L05:279 tau_a 'defined in Lesson 6, Section 2' = L06.html:102 PASS. L05:288 finiteness 'a result there' = L08.html:87 (Corollary 1.4, finite with probability one) PASS. L06:102 Lesson 2 Theorem 2.5 / Remark 2.6 / A2 / Assumption 2.1 and L01 A1(a),(b),(e) = L02.html:93, 282, 289-291, 303-308 and L01.html:72-82 PASS. L06:305 'Lesson 8 does' state the law = L08.html Corollaries 1.3 and 1.5 PASS.")
R("b-delta-L04-L06-hunks", "2.8 delta 00a8479..11d7077: every hunk in the slice read and re-derived",
  "L04.html:37, 396; L05.html:52, 60, 63, 65-69, 127, 263, 306, 467; index.html:52-54, 155-157; cards.json c115, c116",
  "git diff 00a8479 11d7077 read hunk by hunk. L04:37 (Theorem 2.3) PASS; L04:396 (Assumption 4.1 explanation) PASS; L05:52, 60, 63, 65-69 (hypothesis wording 'defined in Section 3 of this lesson', 'Freezing ... (i)') PASS; L05:127 'assuming A4' PASS; L05:263 'Theorem 2.1, assuming A4(e)' PASS (A4(e) is the Gaussian integral used at L05:160); L05:306 PASS; L05:467 PASS; index.html:52-54 objectives PASS; index.html:155-157 card text (L05 'completing the square' matches L05:162-166) PASS; cards c115 and c116 re-read (c116 back 'They are equal. The proof uses the intermediate value theorem.' matches L06:112) PASS.")
R("b-delta-cross-lessons", "2.8 delta: effects on the slice from other units' hunks",
  "git diff 00a8479 11d7077 (whole repository)",
  "Changed files outside the slice: L01/L02/L07/L08 cards (ids c011-c013, c029, c030, c140, c162, c165, c171, c201, c206-c210, and new c220, c221); references.json used_by; ledgers/SC1 mutants and scripts. git diff --stat for tools/, notation/, curriculum/, course/assets/ and course/concepts.html is empty, so no gate script or shared asset changed. None of the non-slice hunks touches L04-L06 content.")
R("b-delta-twins-and-scripts", "2.8 delta: twins and scripts", "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py",
  "git diff 00a8479 11d7077 -- tests/labs/SC1 is empty for the three twins, so the expected blocks and code are the ones run in this round (out/twin_L0x.stdout).")

# ---- numbers (VERIFIER 2.2)
R("b-num-L04", "2.2 numbers in prose (L04)", "course/modules/SC/SC1/L04.html:218-224, 271, 314, 321, 328, 420, 452",
  "scripts/SC1-b-r11/recompute_b_r11.py (out/recompute_b_r11.txt): e^1=2.718281828, e^(1/4)=1.284025417, e^4=54.598150033, e^8=2980.957987 (six places); |e-2.718281828|=4.6e-10 and |e^4-54.598150033|=1.4e-10, both inside the 1e-9 tolerance of the quiz items; trapezoid check on [-14,14] with 60000 nodes reproduces E[exp(theta B_2)] and E[Z_2]=1.000000000 for theta in {-1, 0.5, 2}.")
R("b-num-L05", "2.2 numbers in prose (L05)", "course/modules/SC/SC1/L05.html:263, 320, 368, 375, 382, 458, 499",
  "recompute_b_r11.py and ck_independent_r11.py (out/*.txt): 5.55e-16/3.81e-29 = 1.457e13 (E1 'about 1.5x10^13 to two significant figures' PASS); 5.55e-16/2.2204e-16 = 2.50 (interpretation 'about 2.5' PASS); 3.05e-16/2.2204e-16 = 1.37 (E3 'about 1.4' PASS); 1/(2 sqrt pi) = (4 pi)^(-1/2) = 0.2820948 (M1 PASS); p_1(0,0) = 0.3989423 (quiz 0.3989 PASS); Phi(-1/sqrt2) = 0.5 erfc(1/2) = 0.2397500611 (quiz 0.23975 PASS); independent trapezoid gives max gap 1.11e-15 and tail mass 3.813e-29 (page 3.81e-29 PASS).")
R("b-num-L06", "2.2 numbers in prose (L06)", "course/modules/SC/SC1/L06.html:290-296, 316, 320, 393, 400, 479, 511, 520",
  "recompute_b_r11.py: exact binomial route and enumeration agree: P(M10>=2)=281/512, 2P(S10>2)=11/32, P(S10=2)=105/512; N<=12 enumeration gives 1014 triples and 78 pairs; M12>=3 count 1588, M12>=3 and S12=2 count 495, S12=4 count 495. erfc(1/sqrt2)=0.3173105079; half 0.158655253931 (E3 unrounded value 0.15865525393 PASS). Corollary 2.6 trapezoid check: |2P(B1>1)-erfc(1/sqrt2)| = 1.2e-10.")

# ---- labs (VERIFIER 2.5)
R("b-lab-L04-hypothesis", "2.5 lab hypothesis matches code", "course/modules/SC/SC1/L04.html:147; tests/labs/SC1/lab-SC1-L04-1.py",
  "Hypothesis: relative 1e-9 for E[e^{theta B_t}] vs e^{theta^2 t/2} (code: abs(mgf-closed) <= TOL*closed, twin line 207), absolute 1e-9 for E[Z_t] vs 1 (code line 208), t=2, theta in {-1,0.5,2} (twin lines 169-170). Lemma 2.1 with h=t is the closed form used (twin line 204). PASS.")
R("b-lab-L04-interpretation", "2.5 lab interpretation vs output", "course/modules/SC/SC1/L04.html:224, 230-232",
  "Printed (expected block L04:217-223, equal to out/twin_L04.stdout): 2.718281828, 1.284025417, 54.598150033 for theta = -1, 0.5, 2, equal to e^1, e^(1/4), e^4 (theta^2 t/2 = 1, 0.25, 4); E[Z_t] prints 1.000000000 for each theta. The text says the check is numerical at one time and three thetas and does not prove the martingale property (L04:224). PASS.")
R("b-lab-L04-docstring", "2.4 twin docstring vs code", "tests/labs/SC1/lab-SC1-L04-1.py (module docstring; main())",
  "Docstring: B_t normal with variance t, Simpson with PANELS on [-LIMIT, LIMIT], two checks per theta, truncation not computed beyond LIMIT, finite computations not a proof. main() prints the two checks per theta with those tolerances and nothing else. PASS.")
R("b-lab-L05-docstring-quadrature", "2.4 twin docstring vs code", "tests/labs/SC1/lab-SC1-L05-1.py (module docstring; tail_mass; chapman_kolmogorov_gap)",
  "Docstring: Simpson on [-12,12], 225 cases, mass for 12<=|z|<=40 computed and printed, gaps at rounding scale, exact identity on the page. Code: INTERVALS=2000, TOLERANCE=1e-6, tail_mass uses [12,40] and [-40,-12], main() prints the 225-case count, largest gap, tail mass. PASS.")
R("b-lab-L05-hypothesis-interpretation", "2.5 lab hypothesis and interpretation vs output", "course/modules/SC/SC1/L05.html:170, 263, 306",
  "225 = 3*3*5*5 (TIMES x TIMES x POINTS x POINTS, twin lines 189-190); printed largest gap 5.55e-16 below 1e-06 (True); largest tail mass 3.81e-29; integrals 1.0000000000 for t in {0.5,1,2} (out/twin_L05.stdout). Independent trapezoid recheck (ck_independent_r11.py) agrees. PASS.")
R("b-lab-L05-gap-carry", "2.5 lab output carried into prose", "course/modules/SC/SC1/L05.html:256-263", 
  "The three figures quoted in the interpretation (5.55e-16, 3.81e-29, the ten-digit integrals) are the printed values at L05.html:256-262 (out/twin_L05.stdout). PASS.")
R("b-lab-L06-claims", "2.5 lab claims vs output", "course/modules/SC/SC1/L06.html:186, 297",
  "Parts A-E in out/twin_L06.stdout: 'triples 1014; equal 1014', 'pairs 78; equal 78', Part C 1588, 495, 495; Part D 281/512, 11/32, 105/512, True; Part E 0.3173105079 and 0.1586552539. The hypothesis (L06:186) and interpretation (L06:297) describe exactly these printed results. PASS.")
R("b-lab-L06-docstring-exact-fraction", "2.4 twin docstring vs code", "tests/labs/SC1/lab-SC1-L06-1.py (module docstring; main())",
  "Docstring: N from 1 to 12, 1<=a<=N, b<a with b>=-N (code range(1,n+1) and range(-n,a)); exact integers and Fractions (Part D uses Fraction); Part E closed form in floating point. PASS.")
R("b-ck-independent-L05", "2.5 lab reproduced by an independent method", "course/modules/SC/SC1/L05.html:255-263; tests/labs/SC1/lab-SC1-L05-1.py",
  "ledgers/SC1/scripts/SC1-b-r11/ck_independent_r11.py (out/ck_independent_r11.txt): trapezoid on [-14,14] with 6000 nodes over the same 225 cases gives largest gap 1.110e-15 (< 1e-6), tail mass 3.813e-29, and integrals 1.0000000000 for t in {0.5,1,2}. The page's numbers (5.55e-16, 3.81e-29) are the twin's, and the gap scale differs only by method (both at rounding scale). Lemma 2.2 identity separately verified in exact Fractions at 2000 rational points (recompute_b_r11.py). PASS.")

# ---- mathematics (VERIFIER 2.4)
R("b-math-L04-lemma-2.1", "2.4 mathematics: Lemma 2.1 (MGF of a normal)", "course/modules/SC/SC1/L04.html:81-89",
  "Completing the square theta*y - y^2/(2h) = theta^2 h/2 - (y - theta h)^2/(2h) re-derived by expansion; the shifted density integrates to 1. Grade T with h>0 stated. PASS.")
R("b-math-L04-prop-2.2", "2.4 mathematics: Proposition 2.2 (B is a martingale)", "course/modules/SC/SC1/L04.html:93-105",
  "(ii) E[B_t^2]=t from (D2) (L01.html:62); (iii) E[Y|F_s]=E[Y]=0 by Assumption 4.1 and 4.2(d). The step E[B_s|F_s]=B_s uses the closing sentence of Assumption 4.2 (L04.html:70), which needs E[1|G]=1 that Assumption 4.2 does not list: see b-math-L04-A4.2-E1G. The result is therefore correct under the listed facts plus E[1|G]=1. PASS as to the proposition; the gap is recorded on the assumption row.")
R("b-math-L04-prop-2.3", "2.4 mathematics: Proposition 2.3 (B_t^2 - t is a martingale)", "course/modules/SC/SC1/L04.html:109-123",
  "E[B_t^4]=3t^2 from L03.html:89-97 (Lemma 2.2, E[X^4]=3 Delta^2) PASS; E[(B_t^2-t)^2]=3t^2-2t^2+t^2=2t^2 PASS; E[B_t^2|F_s]=B_s^2+h then minus t gives B_s^2 - s PASS. Same E[1|G] dependence as Prop 2.2 (E[B_s^2|F_s]=B_s^2), see b-math-L04-A4.2-E1G.")
R("b-math-L04-prop-2.4", "2.4 mathematics: Proposition 2.4 (exponential martingale)", "course/modules/SC/SC1/L04.html:129-149",
  "E[Z_t^2]=e^{-theta^2 t} E[e^{2 theta B_t}] = e^{-theta^2 t} e^{2 theta^2 t}=e^{theta^2 t} re-derived; Z_t = Z_s W with W = exp(theta Y - theta^2 h/2) (exponents add to theta B_t - theta^2 t/2); E[W^2]=e^{theta^2 h}, E[W]=1 by Lemma 2.1. Square integrability and the s=t case are covered. PASS.")
R("b-math-L04-A4.1-sketch", "2.4 sketch labelled and names skipped steps", "course/modules/SC/SC1/L04.html:63-65",
  "Labelled 'Sketch, not a proof, for the natural filtration of B'; names the pi-system of cylinder sets and the pi-lambda extension as skipped steps; cites L03 Assumption 3.2(a) (L03.html:71) for single-variable functions only. PASS.")
R("b-math-L04-misconception-1", "2.4 misconception 1 (mean zero is not a martingale)", "course/modules/SC/SC1/L04.html:241",
  "E[B_t^3]=0 by symmetry (E[Y]=E[Y^3]=0); (B_s+Y)^3 expansion gives E[X_t|F_s]=B_s^3+3(t-s)B_s; differs from B_s^3 iff B_s != 0 for s<t. Re-derived. PASS.")
R("b-math-L04-misconception-2", "2.4 misconception 2 (exp(theta B) is not a martingale)", "course/modules/SC/SC1/L04.html:245",
  "E[e^{theta B_t}]=e^{theta^2 t/2} (Lemma 2.1) equals 1 only at t=0 when theta != 0; a martingale has constant expectation by 4.2(b) (P2 L04.html:296). PASS.")
R("b-math-L04-R1-R3", "2.4 research problems R1-R3 (L04)", "course/modules/SC/SC1/L04.html:336-353",
  "R1: B_t^2-g(t) = (B_t^2-t)+k(t), k deterministic martingale constant, g(t)=t+c. R2: E[Z_t|F_s]=Z_s e^{c^2 h/2}, so c^2 h=0, c=0. R3: conditional variance t-s. Each re-derived. PASS.")
R("b-math-L04-M1-M3", "2.4 mechanics problems M1-M3 (L04)", "course/modules/SC/SC1/L04.html:261-279",
  "M1 E[B_t^2]=t, E[B_t^4]=3t^2; M2 E[e^{B_2}]=e, E[Z_2]=1; M3 Var(Z_t)=e^{theta^2 t}-1, zero at theta=0. All re-derived. PASS.")
R("b-math-L04-E1-E3", "2.4 empirical problems E1-E3 (L04)", "course/modules/SC/SC1/L04.html:311-328",
  "E1 e^{0.25}=1.284025417 (printed value); E2 e^8=2980.957987 (exact e^8, decimal six places); E3 theta=2, t=4 gives e^{4*4/2}=e^8 (Lab 1 prints only t=2). All re-derived. PASS.")
R("b-assumed-L04-E2", "2.1 item 6 ('Assuming') rule", "course/modules/SC/SC1/L04.html:321",
  "E2 solution opens 'Assuming Assumptions 4.1 and 4.2, Proposition 2.4 gives E[Z_t^2]=e^{theta^2 t}'. PASS.")
R("b-math-L05-lemma-1.3", "2.4 mathematics: Lemma 1.3 (future increment independent of past)", "course/modules/SC/SC1/L05.html:89-103",
  "Proof re-derived: (D3) on the partition 0=r_0<...<r_k=s<t gives mutual independence; A4(f) gives independence of (B_r1..B_rk) from the last increment; cylinder events form a pi-system generating F_s (any finite time set enlarges to contain 0 and s without changing the event); A4(a) extends. Cases s=t and s=0 handled. PASS.")
R("b-math-L05-thm-1.4", "2.4 mathematics: Theorem 1.4 (Markov property at fixed times)", "course/modules/SC/SC1/L05.html:105-123",
  "A4(b) with Z=B_s, Y=B_t-B_s, f(z,y)=g(z+y) bounded and jointly measurable; f-bar(z)=E[g(z+B_t-B_s)]; substitution y=z+w gives phi_u(y-z)=p_u(z,y), so psi(z)=int g(y)p_u(z,y)dy. s=t case handled. PASS.")
R("b-math-L05-lemma-2.2-thm-2.1", "2.4 mathematics: Lemma 2.2 and Theorem 2.1 (Chapman-Kolmogorov)", "course/modules/SC/SC1/L05.html:134-166",
  "Lemma 2.2 identity (z-x)^2/u+(y-z)^2/v = (u+v)/(uv)(z-m)^2 + (y-x)^2/(u+v) verified in exact Fractions at 2000 random rational points (recompute_b_r11.py: True) and by the expansion on the page. Theorem 2.1 constants: (2 pi)^(-1)(uv)^(-1/2)(2 pi uv/(u+v))^(1/2) = (2 pi (u+v))^(-1/2). PASS.")
R("b-math-L05-A4i-statement", "2.4 named numbered assumption A4(i) (used only in M2)", "course/modules/SC/SC1/L05.html:69, 327, 444; cards.json SC1-c214",
  "A4(i) stated at L05.html:69 with the finiteness condition; used at L05.html:327 (M2) and quiz explanation L05.html:444; card c214 consistent. PASS.")
R("b-math-L05-A3-sketch", "2.4 A3 sketch: labelled, steps skipped named", "course/modules/SC/SC1/L05.html:270-281",
  "A3 stated as Assumption (not proved). Sketch labelled 'Sketch, not a proof'; dyadic approximation rho_n with rho <= rho_n <= rho+2^-n (Problem R3, L05.html:404-406); fixed-time case; skipped steps (i) extension of independence (A4(a)) and (ii) limit passage named; F_rho subset F_{rho_n} justifies A cap {rho_n=q} in F_q (re-derived). PASS.")
R("b-math-L05-R3", "2.4 problem R3 (dyadic approximation from above)", "course/modules/SC/SC1/L05.html:402-408",
  "x <= ceil(x) < x+1 gives rho <= rho_n < rho+2^-n; {rho_n <= r} = {rho <= k/2^n}, k = floor(2^n r), in F_{k/2^n} subset F_r. Re-derived. PASS.")
R("b-math-L05-problems", "2.4 problem set M1-M3, P1-P3, R1-R2 (L05)", "course/modules/SC/SC1/L05.html:316-400",
  "M1: integral 1/(2 sqrt pi) and p_2(0,0)=1/(2 sqrt pi) (out/recompute). M2: psi(x)=x^2+2 and x^3+6x from E[Z^2]=2, E[Z^3]=0 (exact). M3: Cov(B_2-B_1,B_1)=0 and A1(c) of Lesson 1 (L01.html:76). P1: exact identity at u=1,v=3,x=0,y=1 (recompute: True). P2: Phi((c-x)/sqrt(t-s)). P3: substitution. R1: the two paths of the solution (path 1 max at 1/4, path 2 max at 3/4, equal on [0,1/2]) are continuous and valid. R2: deterministic time, F_s subset F_rho. All re-derived. PASS.")
R("b-math-L05-misconceptions", "2.4 misconceptions (L05)", "course/modules/SC/SC1/L05.html:297-306",
  "Misc 1: P2 gives N(B_s,t-s), mean B_s (PASS). Misc 2: transition density centred at x with variance t-s; coincides with p_t(0,.) only when x=0 and s=0 (PASS). Misc 3: 225 grid points do not prove CK (PASS).")
R("b-math-L05-def-1.1-st-case", "2.4 definitions and the s=t case (L05)", "course/modules/SC/SC1/L05.html:75-78, 122",
  "Markov property defined for 0<=s<=t (Definition 1.1); the s=t case in the proof of Theorem 1.4 (L05:122) uses that g(B_t) is F_t-measurable, so E[g(B_t)|F_t]=g(B_t) (standard property of conditional expectation, named in the sentence). PASS.")
R("b-math-L05-E1-E3", "2.4/2.5 empirical problems E1-E3 (L05)", "course/modules/SC/SC1/L05.html:364-384",
  "E1: 5.55e-16 vs 3.81e-29 (printed), ratio 1.457e13 (basis: printed values at three significant figures, stated). E2: ten printed decimals give error bound 5e-11 (PASS). E3: 3.05e-16 is 1.37 times machine epsilon (PASS).")
R("b-scope-L05-E1-tail", "2.4 scope words in E1 solution", "course/modules/SC/SC1/L05.html:368",
  "'so that part of the tail cannot account for the gaps' is backed by the printed 3.81e-29 vs 5.55e-16; the page explicitly declines any claim for |z|>40 ('makes no claim that it is small'). PASS.")
R("b-math-L05-quiz-Q7", "2.4 quiz Q7 (A3 sketch gap)", "course/modules/SC/SC1/L05.html:479-485",
  "Correct option names the extension of independence to the whole shifted path and the passage to the limit, matching the sketch at L05.html:281. PASS.")
R("b-quiz-L05-Q7", "2.9 quiz L05 Q7 explanation", "course/modules/SC/SC1/L05.html:485",
  "Explanation says the sketch proves the fixed-time case, sums over countably many dyadic values, and names two skipped steps: matches L05.html:281. PASS.")
R("b-assumed-L05-quiz-Q9", "2.1 item 6 ('Assuming') rule, quiz Q9", "course/modules/SC/SC1/L05.html:497-499",
  "Answer 0.23975 = Phi(-1/sqrt2) = 0.2397500611 (recompute, PASS); explanation cites A4(a),(b),(f) and Problem P2. PASS.")
R("b-assumed-L05-quiz-M2", "2.1 item 6 ('Assuming') rule, quiz Q2", "course/modules/SC/SC1/L05.html:441-444",
  "Answer 3 = B_1^2 + 2 with B_1 = 1 (M2 solution); explanation cites A4(a), A4(f), A4(i). PASS.")
R("b-scope-L05-canonical", "4 scope words in L05 canon-breaks", "course/modules/SC/SC1/L05.html:284-289",
  "'Unbounded stopping times' bullet: A3 requires rho<=c; finiteness of tau_a is a result of Lesson 8 (L08.html:87, Corollary 1.4). PASS.")
R("b-notation-L05-Phi-varphi", "5 notation: Phi and varphi vs notation/notation.json", "course/modules/SC/SC1/L05.html:121, 349-351, 499",
  "Phi is used only as the standard normal distribution function (P2 L05.html:349-351, quiz L05.html:499), the registered meaning (notation.json symbols: '\\Phi, \\Phi^{-1}' standard normal CDF and inverse). varphi is a local Gaussian density in the proof at L05.html:121, not a registered symbol. PASS.")
R("b-notation-L05-X-n", "5 notation: local symbols X^(n) and rho_n", "course/modules/SC/SC1/L05.html:61-69, 281",
  "X^(n) and rho_n are defined at L05.html:281 before use and are not registered symbols. PASS.")
R("b-notation-M-clash", "5 notation: M_t and M_N running maxima", "course/modules/SC/SC1/L05.html:52, 268; L06.html:56, 104, 112",
  "M_t and M_N are local running maxima defined where used (L06.html:56 defines M_N; L06.html:104 defines M_t). Problem labels M1-M3 are labels, not symbols. No registered symbol is reused. PASS.")
R("b-scope-L05-D1D3", "4 scope: Sections 1 and 2 use (D1)-(D3) and A4(a),(b),(e),(f)", "course/modules/SC/SC1/L05.html:56",
  "Lemma 1.3 uses A4(a),(f) (L05:95); Theorem 1.4 uses A4(b) (L05:120); Theorem 2.1 uses A4(e) (L05:147-160); no other A4 part is used in Sections 1-2. PASS.")
R("b-term-almost-surely", "5 term 'almost surely' defined before use", "course/modules/SC/SC1/L05.html:62, 76, 111, 122, 465; L06.html:144",
  "Defined in place at A4(b) (L05:62, '(that is, with probability one)') before the first use in Definition 1.1 (L05:76). PASS.")
R("b-math-L06-facts-unnumbered", "3 unnumbered facts in L06 section 2", "course/modules/SC/SC1/L06.html:102-130",
  "Facts used in Section 2 are the results of Lesson 2 (Remark 2.6, Theorem 2.5) and the numbered A3, A4 of Lesson 5, each named as an assumption at L06.html:102 and L06.html:126-128. None is presented as proved here. PASS.")
R("b-math-L06-prop-1.3-cor-1.4", "2.4 mathematics: Proposition 1.3 and Corollary 1.4", "course/modules/SC/SC1/L06.html:74-98",
  "M_N >= a iff kappa <= N (walk moves by +-1 from 0 < a); reflection bijection of Lemma 1.2 maps {kappa<=N, S_N=b} to {S_N=2a-b}; sum over b<a maps onto integers above a, giving #{S_N>a}. Re-derived; exact counts confirm (out/recompute_b_r11.txt). PASS.")
R("b-math-L06-lemma-2.1", "2.4 mathematics: Lemma 2.1 (running maximum and first visit)", "course/modules/SC/SC1/L06.html:104-115",
  "(i) {M_t>=a}={tau_a<=t} via IVT and closedness of {s: B_s=a}; (ii) IVT on [0,t]; (iii) IVT on (0,s) for B_s>a, then B_t != a since t < tau_a. Re-derived. PASS.")
R("b-math-L06-prop-2.3-thm-2.5", "2.4 mathematics: Proposition 2.3 and Theorem 2.5", "course/modules/SC/SC1/L06.html:122-171",
  "rho=tau_a^t is a stopping time by A4(c) and {rho<=r}=(tau_a<=r) for r<t; W_t = B_rho - X_{t-rho}; A4(b) with f_(-/+) gives E[g(W_t)|F_rho]=h_-(B_rho,t-rho) and E[g(B_t)|F_rho]=h_+; symmetry of N(0,u) gives h_-=h_+. Theorem 2.5: E={W_t>a} (since on {tau_a>t}, W_t=B_t<a) so P(tau_a<=t)=P(B_t>=a)+P(B_t>a)=2P(B_t>a), P(B_t=a)=0. Re-derived. PASS.")
R("b-math-L06-def-2.2-remark-2.4", "2.4 Definition 2.2 and Remark 2.4 (what is not proved)", "course/modules/SC/SC1/L06.html:117-121, 147-150",
  "Definition 2.2 states the path-level reflection and says it is not asserted from A3 (bounded only) and not proved; Remark 2.4 says Proposition 2.3 is one-time-only. Consistent with the proof of Prop 2.3 (L06.html:135-144). PASS.")
R("b-math-L06-cor-2.6", "2.4 mathematics: Corollary 2.6 (erfc closed form)", "course/modules/SC/SC1/L06.html:173-182",
  "Substitution z=sqrt2 w gives 2P(B_t>a)=erfc(a/sqrt(2t)) (re-derived). Trapezoid recheck of 2P(B1>1) agrees with erfc(1/sqrt2) to 1.2e-10 (recompute_b_r11.py). PASS.")
R("b-math-L06-R1-R3", "2.4 research problems R1-R3 (L06)", "course/modules/SC/SC1/L06.html:406-426",
  "R1 parity argument: S_N has parity of N, both sides vanish otherwise, 2a-b = b mod 2 (PASS). R2 sign change: min B <= -a iff max(-B) >= a; Theorem 2.5 for -B gives 2P(B_t<-a) (PASS). R3: 2x > x for x>0, and normal law gives positive mass to half-lines (PASS).")
R("b-math-L06-E1-E3", "2.4 empirical problems E1-E3 (L06)", "course/modules/SC/SC1/L06.html:382-402",
  "E1: 78 = 12*13/2 pairs (PASS). E2: 281/512 - 352/1024 = 210/1024 = 105/512 (PASS). E3: half of 0.3173105079 is 0.15865525395 and the unrounded half 0.158655253931 prints as 0.1586552539 (PASS).")
R("b-math-L06-M-P-problems", "2.4 mechanics and proof problems (L06)", "course/modules/SC/SC1/L06.html:334-378",
  "M1: 5 of 8 sequences and Corollary 1.4 gives 4+1 (PASS). M2: P(M_2>=2)=1/4 (PASS). M3: S=(0,1,2,1,0,1), kappa=2, S'=(0,1,2,3,4,3), S'_k=4-S_k for k>=2 (PASS). P1 (involution), P2 (Lemma 2.1 ii and iii from continuity), P3 (Corollary 1.4 from Proposition 1.3) re-derived. PASS.")
R("b-scope-L06-only-events", "4 scope words in L06 (only, exactly, every)", "course/modules/SC/SC1/L06.html:52, 297, 302-309",
  "'only' and 'exactly' are used with computations or with the enumerated range (N<=12, 1<=a<=N). The 'Discrete grid' and 'Symmetry' canon bullets make no claim beyond the stated cases. PASS.")
R("b-scope-L06-N12-every-case", "4 scope: 'every case with N<=12'", "course/modules/SC/SC1/L06.html:297",
  "Parts A and B loop over every N in 1..12 and every a in 1..N (checks_b_r11 / out/twin_L06.stdout: 1014 and 78 cases, all equal). PASS.")
R("b-rounding-L06-misconception", "2.5/4 rounding claim", "course/modules/SC/SC1/L06.html:316",
  "2P(B_1>1)=0.31731 -> 0.3173 and P(B_1>=1)=0.158655 -> 0.1587 as stated (both to four places). PASS.")
R("b-plan-L06-pathlevel", "2.8 plan vs page: path-level reflection", "course/modules/SC/SC1/L06.html:118-121, 149; plans/SC1-build-plan.md:261-263",
  "The plan (line 261-263) specifies the path-level reflection 'Assuming A3'. The page proves only the fixed-time form, because A3 covers bounded stopping times and tau_a is not shown bounded (L06:119). The page's narrower claim is the one the stated assumptions support; no row fails. Observation for the architect (carried from round 10).")
R("b-causal-L06-symmetry-last-step", "7 causal claim: factor 2 and symmetry", "course/modules/SC/SC1/L06.html:306",
  "'The factor 2 comes from adding two events of equal probability': P(tau_a<=t) = P(B_t>=a)+P(E) with P(E)=P(B_t>a) (L06:169-170). The symmetry step h_-=h_+ (L06:144) uses only the symmetry of N(0,u). PASS.")
R("b-l06-assumption-scope", "2.1 item 6: L06 assumptions named", "course/modules/SC/SC1/L06.html:307",
  "'Theorem 2.5 is conditional on A3 and A4 of Lesson 5, which are stated and not proved there' matches the statement at L06.html:159-160. PASS.")
R("b-l06-canon-symmetry-attribution", "2.1/3 attribution in L06 canon section", "course/modules/SC/SC1/L06.html:300-307",
  "No passage or theorem number of an external source is attributed in the canon section. PASS.")
R("b-causal-L06-remark-2.4", "7 causal claim: Remark 2.4", "course/modules/SC/SC1/L06.html:149",
  "Remark 2.4 says Proposition 2.3 is about one time at a time, and that the path-level statement is not used and not claimed. Consistent with L06.html:130 and 149. PASS.")
R("b-hyp-L06-102-lesson2-hypotheses", "2.1 hypotheses of Lesson 2 results cited", "course/modules/SC/SC1/L06.html:102",
  "Theorem 2.5 of Lesson 2 has H2 'Assuming A2 and Assumption 2.1' (L02.html:289-291); Remark 2.6 has H2 'Assuming A1(a), A1(b), A1(e), A2 and Assumption 2.1' (L02.html:303-308). L06:102 cites both correctly. PASS.")
R("b-ivt-observation", "3 IVT use in Lemma 2.1", "course/modules/SC/SC1/L06.html:112, 114",
  "IVT applied on [0,s*] and [0,t] with B_0=0 < a; continuity is named (L06:104 hypotheses). PASS.")
R("b-quiz-L06-Q8", "2.9 quiz L06 Q8", "course/modules/SC/SC1/L06.html:508-511",
  "Answer 0.1587 with tolerance 1e-4 against P(B_1>=1)=0.1586552539 (recompute). Explanation: 1/2 erfc(1/sqrt2)=0.15865..., and P(B1>1)=P(B1>=1) because B_1 has no atom: correct. PASS.")

# ---- cards (VERIFIER 2.7)
R("b-cards-c061-c072", "2.7 cards c061-c072 vs lesson text", "course/modules/SC/SC1/cards.json (c061-c072)",
  "Definitions c061-c065 match L04.html:59, 64, 70, 75; c066 Lemma 2.1 (L04:82); c067 Prop 2.2 (L04:98); c068 Prop 2.3 (L04:114, 122-123); c069 remark (L04:126) and R3; c070 Prop 2.4 (L04:134, 140-142); c071 second moment (L04:139); c072 lab output (L04:217-223). All checked against the page text this round. PASS.")
R("b-cards-c073-c085", "2.7 cards c073-c084 vs lesson text (c085 absent from cards.json)", "course/modules/SC/SC1/cards.json (c073-c084)",
  "c073 (L04:230), c074 (L04:231), c075 (L04:232), c076 (L04:241), c077 (L04:245), c078 (L04:248), c079 (L04:337-339), c080 (L04:344-346), c081 (L04:294-296), c082 (L04:301-303), c083 (L05:75-77), c084 (L05:79-86). Each matches its lesson text. No card id c085 exists; the range is recorded as present ids c073-c084.")
R("b-cards-c086-c097", "2.7 cards c086-c097 vs lesson text", "course/modules/SC/SC1/cards.json (c086-c097)",
  "c086 (L05:89-96), c087 (L05:105-116), c088 (L05:125-128), c089 (L05:134-138), c090 (L05:146-152), c091 and c092 (lab output L05:255-262), c093 (L05:270-277), c094 (L05:268), c095 (L05:399), c096 (L05:406), c097 (L05:390-392; A4(d) L05:64). All re-read this round. PASS.")
R("b-cards-c098-c110", "2.7 cards c098-c110 vs lesson text", "course/modules/SC/SC1/cards.json (c098-c110)",
  "c098 (L05:287), c099 (L05:288), c100 (L05:298), c101 (L05:302), c102 (L05:305-306), c103 (L05:327), c104 (L05:349-351), c105 (L05:334), c106 (L06:56), c107 (L06:60), c108 (L06:66), c109 (L06:76-84), c110 (L06:89-92). PASS.")
R("b-cards-c111-c122", "2.7 cards c111-c122 vs lesson text (c115, c116 changed this round)", "course/modules/SC/SC1/cards.json (c111-c122)",
  "c111 1014 (out/twin_L06.stdout), c112 78, c113 281/512, 11/32, 105/512, c114 495, 495, 1588 (L06:286-288). c115 changed this round: front now defines M_t; back erfc(1/sqrt2)=0.3173 matches L06:173-182 and L06:479. c116 changed this round: front defines M_t and tau_a; back 'They are equal. The proof uses the intermediate value theorem.' matches L06:112. c117 (L06:114), c118 (L06:114), c119 (L06:118-120), c120 (L06:130), c121 (L06:130, 135), c122 (L06:148-149). PASS.")
R("b-cards-c123-c133", "2.7 cards c123-c133 vs lesson text", "course/modules/SC/SC1/cards.json (c123-c133; c125 absent)",
  "c123 (L06:161), c124 (L06:179-181), c126 (L06:316), c127 (L06:320), c128 (L06:323-324), c129 (L06:338-339), c130 (L06:410), c131 (L06:417), c132 (L06:424), c133 (L06:130 and A3 of L05:276). c125 is not present in cards.json. PASS.")
R("b-cards-duplicates", "2.7 duplicate cards (full scan)", "course/modules/SC/SC1/cards.json (all 208 cards; 86 slice cards)",
  "scripts/SC1-b-r11/checks_b_r11.py (out/checks_b_r11.txt): 208 cards, 0 duplicate ids, 86 slice cards (lessons L04-L06). Full read of the 86 slice cards this round. No duplicate statements among the slice cards.")
R("b-cards-c193-c204", "2.7 assumption cards (A4 items, A3, and 4.2 items)", "course/modules/SC/SC1/cards.json (c193-c200, c202-c204, c214)",
  "c193-c200 match the A4(a)-(h) items at L05.html:58-72; c214 matches A4(i) (L05:69); c202 matches 4.2(b) (L04:70); c203 repeats the 4.2 closing sentence 'Taking Y=1, E[X|G]=X' that depends on the unlisted fact E[1|G]=1 (see b-math-L04-A4.2-E1G); c204 matches 4.2(d). PASS for card-to-text agreement; the dependency is on the FAIL row.")
R("b-cards-c079-c088-c100-c119", "2.7 spot cards c079, c088, c100, c119", "course/modules/SC/SC1/cards.json (c079, c088, c100, c119)",
  "c079 R1 (L04:337-339), c088 Remark 1.5 (L05:125-128), c100 misconception (L05:298), c119 Definition 2.2 (L06:118-120). All agree with the text. PASS.")
R("b-cards-c103-c104-hypothesis", "2.7 hypotheses on cards c103, c104", "course/modules/SC/SC1/cards.json (c103, c104)",
  "c103 states A4(a), A4(f), A4(i) (L05:327 M2 hypotheses); c104 states A4(a), A4(b), A4(f) (L05:349 P2 hypotheses). PASS.")
R("b-cards-ellipsis", "2.2/1.3 ellipsis check (finite index lists)", "cards c086, c106, c112; L05.html:100, L06.html:56, L06.html:386",
  "Unicode and LaTeX ellipses appear only in finite index lists ('0=r_0<...<r_k=s<t', 'e_1,...,e_N', '1+2+...+12'), not as omitted content. check_pages.py bans only '...' and passes. Same architect open item as round 9 (plan 2.2 vs BUILDER_RULES 1.3): recorded as an observation, not a FAIL.")

# ---- structure and prose
R("b-dag-D1-D9", "2.8 DAG: out-of-closure concepts used by name", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "check_dag.py PASS. Name scan over the three pages and their cards for the planned D1-D9 concepts (Ito, GBM, Ornstein-Uhlenbeck, Euler-Maruyama, Milstein, Girsanov, Feynman-Kac, Black-Scholes, barrier, Monte Carlo, bias, Donsker, Levy, Poisson, SDE, change of measure, risk-neutral, bridge): no hits. PASS.")
R("b-process-words", "1/12 process words in learner text", "course/modules/SC/SC1/L04.html, L05.html, L06.html; cards.json (slice)",
  "checks_b_r11.py: process-word hits [] (builder, verifier, round, REQUEST, planner, architect, fixer, unit report). PASS.")
R("b-banned-phrases", "2.9/3 banned phrases", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "checks_b_r11.py: banned hits [] for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly. check_pages PASS. PASS.")
R("b-hours-L04-L06", "2.8 hours arithmetic", "course/modules/SC/SC1/index.html:29; L04.html:34, L05.html:35, L06.html:35",
  "index.html:29 data-hours-lessons=72, data-hours-project=28 (sum 100 = curriculum 100). Eight lessons x 9 h = 72; L04, L05, L06 each data-hours=9. PASS.")
R("b-hub-L04-description", "2.9 hub card text vs lesson content (L04-L06)", "course/modules/SC/SC1/index.html:52-54, 150, 155-157",
  "index.html:150 'Lesson 4 covers continuous-time martingales. Lesson 5 covers the Markov property. Lessons 6 to 8 cover the reflection principle...' matches the pages. Cards at index.html:155-157 match L04-L06 titles and content (L05 card 'completing the square' matches L05:162-166). PASS.")
R("b-structure-sections", "2.9 template sections in order (BUILDER_RULES 4.2)", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "Order checked by reading each page in full: why-it-matters, core content, inline lab, canon-breaks, misconceptions, problem set (tiers mechanics, proof, empirical, research), key results, retrieval quiz, references. Each lesson has 3 misconceptions, 12 problems with worked solutions, 10-11 quiz items with explanations. PASS.")
R("b-struct-why-it-matters", "2.9 why-it-matters word count (<=120)", "course/modules/SC/SC1/L04.html:51, L05.html:52, L06.html:52",
  "checks_b_r11.py: 79, 111, 118 words (text with math replaced). PASS.")
R("b-quiz-L04-Q8-explain", "2.9 quiz L04 Q8 explanation (round-9 FAIL, fixed)", "course/modules/SC/SC1/L04.html:432-438",
  "Answer 'No: its conditional expectation is B_s+t, which is not B_s+s' with explanation at L04:438 (Problem P1). PASS.")
R("b-quiz-L04-L06", "2.9 quiz items vs lesson text (L04-L06)", "course/modules/SC/SC1/L04.html:377-464; L05.html:428-511; L06.html:449-531",
  "Each answer re-checked: L04 q3 = 3, q4 = 27, q6 = 2.718281828, q10 = 54.598150033; L05 q2 = 3, q4 = 0.3989, q9 = 0.23975; L06 q2 = 0.25, q4 = 0.3173, q8 = 0.1587. Counts: 11, 10, 10 items, each with an explanation (checks_b_r11.py). PASS.")
R("b-observation-transition-terms", "5 term consistency: transition density", "course/modules/SC/SC1/L05.html:79-86, 115, 419; cards.json SC1-c084, c087",
  "'Gaussian transition density' is defined at L05:79-86 and used consistently as p_u(x,y) in Theorem 1.4, Theorem 2.1 and the cards. PASS.")
R("b-l04-problem-set-E-intro", "2.9 problem-set intro (L04)", "course/modules/SC/SC1/L04.html:256",
  "'Problem E1 uses the output of Lab 1; E2 and E3 ask about values that Lab 1 does not print.' E2 (e^8) and E3 (t=4) are not printed (L04:319-328). PASS.")
R("b-prose-L04-R2-title", "2.9 prose: R2 title and statement (L04)", "course/modules/SC/SC1/L04.html:343-346",
  "Title 'When the exponential exp(cB_t) is a martingale' and statement 'only when c = 0' agree with the solution (L04:346). PASS.")
R("b-prose-L04-remark-numbering", "2.9 prose: remark labels (L04)", "course/modules/SC/SC1/L04.html:37, 126",
  "The remark at L04:126 is unnumbered and is referred to only by content; L04:37 now points to Theorem 2.3 of Lesson 3 (no stale 'remark after Proposition 2.3'). PASS.")
R("b-scope-L04-footer", "4 footer claim (L04)", "course/modules/SC/SC1/L04.html:479",
  "Footer: Propositions 2.2 to 2.4 are proved from Assumptions 4.1 and 4.2 (stated, not proved); Lab 1 labelled a numerical check. Consistent with the page. PASS.")
R("b-math-L05-problems-title", "2.9 prose: problem titles (L05)", "course/modules/SC/SC1/L05.html:341, 355",
  "P1 'Verify Lemma 2.2 at one point, then in general' and P3 'Normalisation of the transition density' match their solutions. PASS.")
R("b-prose-L05-P3-title", "2.9 prose: L05 P3 title", "course/modules/SC/SC1/L05.html:355", "As above. PASS.")
R("b-prose-L06-P2-title", "2.9 prose: L06 P2 title", "course/modules/SC/SC1/L06.html:366",
  "'Parts (ii) and (iii) of Lemma 2.1 from continuity' matches the solution, which proves (ii) and (iii) without (i). PASS.")
R("b-prose-L04-P3-title", "2.9 prose: L04 P3 title", "course/modules/SC/SC1/L04.html:300",
  "'The product moment of a martingale at two times' matches the solution (E[Z_s Z_t]=E[Z_s^2]). PASS.")
R("b-math-degenerate-L04-lemma-2.1", "3 degenerate cases: Lemma 2.1 (h>0) and t=0", "course/modules/SC/SC1/L04.html:81-82, 139-140",
  "Lemma 2.1 requires h>0 (L04:82); the proof of Proposition 2.4 treats t=0 separately (L04:139: 'At t = 0 both E[Z_0^2] and e^0 equal 1'). PASS.")
R("b-math-L04-quiz-degenerate", "3 quiz degenerate case Z_0", "course/modules/SC/SC1/L04.html:423-429",
  "Z_0 = exp(0) = 1 from B_0 = 0 (D1, L01.html:61). PASS.")
R("b-math-L05-P2-hypothesis", "2.1 hypotheses of P2 (L05)", "course/modules/SC/SC1/L05.html:349-351",
  "P2 states A4(a), A4(b), A4(f), the hypotheses of Theorem 1.4 with g = indicator (bounded). PASS.")
R("b-hub-L06-objective", "2.9 hub objective vs L06 content", "course/modules/SC/SC1/index.html:54; L06.html:118-121",
  "Objective 'Prove the fixed-time reflection identity for Brownian motion (Lesson 6, Theorem 2.5), under Assumptions A3 and A4, derive the tail ... and name every assumption' matches Theorem 2.5, Proposition 2.3 and the stated assumptions. PASS.")

# ---- scans and notation (round 11)
R("b-scope-words-r11", "4 scope words in L04-L06 (every, all, always, any, never, only, exactly, same, almost surely, converges, for all, each, must, cannot)",
  "course/modules/SC/SC1/L04.html, L05.html, L06.html (lines listed in out/scope_scan_r11.txt)",
  "scripts/SC1-b-r11/scope_scan_r11.py: 50 L06 lines, plus L04 and L05 lines, each read in context. Each scope word is backed by a proof on the page, a finite computation printed by the lab (N<=12, t in {0.5,1,2}, the 225 cases), a definition, or an explicit hypothesis. 'Predicted before running' (L04:147, L05:170, L06:186) is a stated prediction, checked against the printed output. PASS.")
R("b-notation-r11", "5 notation: registry macros and symbols (full pass)", "course/modules/SC/SC1/L04.html, L05.html, L06.html; notation/notation.json",
  "Custom macros used: \\E, \\Prob, \\Var, \\Cov, \\R, \\Normal, \\indic (checks_b_r11.py). Registry meanings respected: \\Normal(mu, sigma^2) with variance as second argument (L05:85, 121; L06:144 'Normal(0,u)'); \\indic as indicator (L05:349). \\Phi only as standard normal CDF. Symbol T is never a math symbol (grade letters only) and H is not used as a horizon. \\mathbb{Q}, \\gamma_3, \\gamma_4, R^\\ast, R_f not used. PASS.")
R("b-recompute-r11", "2.2/3 independent recomputation (round 11)", "ledgers/SC1/scripts/SC1-b-r11/recompute_b_r11.py; ck_independent_r11.py",
  "Both scripts run with python -I -W error; outputs in out/recompute_b_r11.txt and out/ck_independent_r11.txt. Every number cited in the rows above was reproduced by these scripts (not copied from the page).")
R("b-verify-refs-r11", "2.6 registry (round-11 re-run)", "references/references.json", "Same runs as b-verify-refs (offline 560/0; live SC1 1/0). PASS.")
R("b-assumed-facts-statement", "2.1 item 6: statements using an unproved fact say so", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "Every result in L04-L06 that uses A4.1, A4.2, A3, A4(x) or Lesson 1-3 facts states 'Assuming ...' or lists them as hypotheses (L04:93, 109, 129; L05:89, 105, 146, 270; L06:122-130, 153-160, 173-177). The one unlisted fact is E[1|G]=1 (row b-math-L04-A4.2-E1G).")

# ---- ids retained from round 10 whose subject is re-verified above
R("b-notation-r5", "5 notation (full pass, retained id)", "course/modules/SC/SC1/L04.html, L05.html, L06.html; notation/notation.json",
  "Same evidence as b-notation-r11: custom macros and registry meanings checked in this round (checks_b_r11.py output). PASS.")
R("b-recompute-r5", "1 recomputation (retained id)", "ledgers/SC1/scripts/SC1-b-r11/recompute_b_r11.py",
  "Same evidence as b-recompute-r11: recompute_b_r11.py and ck_independent_r11.py rerun in round 11 (out/*.txt). PASS.")
R("b-scope-words-r5", "4 scope words in L04-L06 (retained id)", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "Same evidence as b-scope-words-r11: scope_scan_r11.py output (out/scope_scan_r11.txt) read in context. PASS.")
R("b-verify-refs-r5", "2.6 registry (retained id)", "references/references.json",
  "Same evidence as b-verify-refs: offline 560 entries 0 problems; live SC1 1 entry 0 problems (out/verify_refs_*.txt). PASS.")

# ---- the one new non-PASS row
R("b-math-L04-A4.2-E1G", "2.4 assumptions are complete: Assumption 4.2 lists (a)-(d) but its closing sentence uses E[1|G]=1",
  "course/modules/SC/SC1/L04.html:70 (Assumption 4.2); used at L04.html:103, 119-121, 339; cards.json SC1-c203",
  "Assumption 4.2 lists (a) linearity, (b) tower, (c) pull-out, (d) independence. Its closing sentence, 'Taking Y = 1, a G-measurable X satisfies E[X | G] = X', follows from (c) only if E[1 | G] = 1, and that property is not listed among (a)-(d) nor derived. The same unlisted fact is used without mention in the proof of Proposition 2.2 (L04.html:103, E[B_s | F_s] = B_s), in Proposition 2.3 (L04.html:119-121, E[B_s^2 | F_s] = B_s^2), in the canon-breaks bullet (L04.html:230, E[t | F_s] = t), and in R1's solution (L04.html:339, E[k(t) | F_s] = k(t)). Card SC1-c203 repeats the sentence. Verified by reading the full page and re-deriving each use; the mathematics is correct, but the assumption list is incomplete under VERIFIER 2.4 ('assumptions are complete').",
  "Add the property to Assumption 4.2 as a numbered part, for example '(e) E[1 | G] = 1', and change the closing sentence to 'Taking Y = 1 in (c) and using (e), a G-measurable X satisfies E[X | G] = X.' Then re-run check_pages and the card check for SC1-c203 (its back must match the new wording).",
  status="FAIL")

fragment = {
    "unit": "SC1",
    "slice": "b",
    "round": 11,
    "verifier": "independent verifier (Haiku 5.5), round 11",
    "pin": "11d7077a290f7960b183d3a5a6631af4773888f9",
    "base": "00a84795f276456fce19d4181373cc4efba11a36 (round-10 pin); delta 00a8479..11d7077 (commit 11d7077a, batch 4 round 10 fixes)",
    "checkout": str(ROOT),
    "scratch": str(ROOT / "ledgers" / "SC1" / "scripts" / "SC1-b-r11"),
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b = L04, L05, L06 pages, their three lab twins, the hub rows and cards that cite them (plan section 13 slice L05-L06 was re-cut per the task: L04-L06). No project grader is in the slice, so no student-error mutant is counted and mutants is empty (same ruling as round 10).",
        "Round-10 FAIL b-cross-L04 is fixed in 11d7077 (L04.html:37 now cites Theorem 2.3 of Lesson 3, which exists and states the mean sum t). Re-derived PASS.",
        "Round-11 delta read hunk by hunk (L04.html x2, L05.html x9, index.html hub lines, cards c115 and c116). L06.html and the three twins are byte-identical to the round-10 pin. Because every page of the slice was re-read in full this round, no row is carried forward; each row carries evidence from this round.",
        "New FAIL: b-math-L04-A4.2-E1G. Assumption 4.2 uses E[1|G]=1 without listing it. Mathematics correct; assumption list incomplete. Fix is in the L04 page (add a numbered part), which is outside this verifier's permission to edit.",
        "Observation (not a row): plans/SC1-build-plan.md:261-263 says 'Assuming A3' for the path-level reflection; the page proves only the fixed-time form (Remark 2.4), which the stated assumptions support. Architect to reconcile the plan wording.",
        "Observation (not a row): unicode and LaTeX ellipses in finite index lists (cards c086, c106, c112; L05.html:100, L06.html:56, L06.html:386). Same open architect item as round 9.",
        "Not checked: the whole-repository gate (repo-wide ruff/mypy, full pytest, render_curriculum, build_site --check, fetch_data --check, check_pages/check_dag/check_projects --all, verify_refs over the whole registry, the course-wide page_smoke). Only slice-scoped and unit-scoped commands were run. No screenshot was taken (page_smoke ran in Chromium and reported PASS). Shreve (2004) and Karatzas and Shreve (1991) were not read; no passage is attributed to either. embed_labs --refresh was not run; the page code was compared with the twin and the expected block with the twin stdout instead.",
    ],
    "summary": {},
}
fragment["summary"] = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == "PASS"),
    "fail": sum(1 for r in rows if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
    "mutants": 0,
    "mutants_killed": 0,
}
path = ROOT / "ledgers" / "SC1" / "SC1-b.json"
path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", path, fragment["summary"], fragment["verdict"])
