"""Round-10 fragment for SC1 slice b (L04-L06 and twins). Writes ledgers/SC1/SC1-b.json; validates via tools/ledger.py."""
import json, subprocess, sys
from datetime import datetime, timezone

CK = "checkout /Users/billyribeiro/.fanout/wt/verifyE10-SC1-b (pin 00a84795)"
R = {}  # id -> (check, location, status, evidence, fix)

def P(i, check, loc, ev):
    R[i] = (check, loc, "PASS", ev, "")

# gates (re-run this round)
P("b-check-pages", "2.9 structure (check_pages)", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "tools/check_pages.py --unit SC1 -> 'check_pages SC1: PASS' exit 0 (out/check_pages.txt); per page --page L04/L05/L06 each 'PASS' exit 0 (out/check_pages_L04.txt, _L05, _L06).")
P("b-check-dag", "2.9 DAG (check_dag)", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS' exit 0 (out/check_dag.txt). Link review in b-dag-D1-D9.")
P("b-run-labs", "2.5 labs (run_labs, page by page)", "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py",
  "tools/run_labs.py --unit SC1 --page L04 / L05 / L06 -> 'run_labs SC1: PASS (1/1)' exit 0 each (out/run_labs_L04.txt, _L05, _L06).")
P("b-twin-match", "2.5 page code == twin; expected == stdout; twin under python -I -W error",
  "course/modules/SC/SC1/L04.html:150-215, L05.html:172-253, L06.html:199-279; tests/labs/SC1/lab-SC1-L0[456]-1.py",
  "ledgers/SC1/scripts/SC1-b-r9/twin_match_r9.py run with python3 -I this round (out/twin_match_r10.txt): L04/L05/L06 page code == twin True; expected == stdout True; exit 0; stderr 0 bytes; markers_left 0; sha256 79a56370..., 744046b7..., 8d01822e... (same as round 9); 'ALL PASS'. git diff c93dd52..HEAD is empty for tests/labs/SC1.")
P("b-lab-lint", "2.5 ruff and mypy on the three twins", "tests/labs/SC1/",
  "ruff check tests/labs/SC1 -> 'All checks passed!' exit 0; ruff format --check -> '11 files already formatted' exit 0; mypy --no-incremental on the three twins -> 'Success: no issues found in 3 source files' exit 0 (out/ruff_check.txt, ruff_format.txt, mypy_labs.txt).")
P("b-page-smoke", "2.5/2.9 page_smoke", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "tools/page_smoke.py --unit SC1 --pages L04 L05 L06 -> 'page_smoke SC1: PASS' exit 0 (out/page_smoke.txt); each page run alone -> PASS exit 0 (out/page_smoke_L04.txt, _L05, _L06).")
P("b-pytest-tooling", "pytest (tooling for labs, run_labs, page checks)", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
  "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q -> 46 dots, exit 0 (out/pytest_tooling.txt).")
P("b-verify-refs", "2.6 registry (verify_refs)", "references/references.json",
  "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' exit 0; tools/verify_refs.py --unit SC1 -> 'live re-verification of SC1: 1 of 560 entries, 0 problems' exit 0 (out/verify_refs_offline.txt, verify_refs_unit.txt).")
P("b-attribution-references", "2.2 attribution: references only from the registry, no passage read",
  "course/modules/SC/SC1/L04.html:468, L05.html:515, L06.html:536",
  "curriculum/03-markets.yaml:522-524 lists 'Shreve, Stochastic Calculus for Finance II (2004)' and 'Karatzas & Shreve ... (1991)'. references/references.json has key shreve2004stochastic (Stochastic Calculus for Finance II, 2004) and no Karatzas key. The three pages cite no passage and say the second source has no admissible record.")
R["b-cross-L04"] = ("2.8 cross-lesson reference: L04 'Uses' line", "course/modules/SC/SC1/L04.html:37", "FAIL",
  "L04.html:37 says the quadratic variation is 'of Lesson 3 (in the remark after Proposition 2.3)'. course/modules/SC/SC1/L03.html contains no 'Proposition 2.3' (grep -c = 0) and no 'Remark' block (grep -c = 0). The only unlabelled paragraph after the proof of Theorem 2.3 is at L03.html:115. The locator names an item that does not exist. The mean-t statement it refers to is the Conclusion of Theorem 2.3 (L03.html:99-107).",
  "In course/modules/SC/SC1/L04.html:37 replace 'in the remark after Proposition 2.3' with 'in Theorem 2.3'. (Source file is outside this slice; reported, not edited.)")
P("b-cross-L05-L06", "2.8 cross-lesson references (L05, L06)", "L05.html:268, 279, 288; L06.html:102, 127, 305",
  "L05:268 'M6 Lesson 9, Definition 9.1' = course/modules/M/M6/L09.html id def-stopping-time. L05:279 'Lesson 6, Section 2' defines tau_a (L06.html:102). L05:288 'Lesson 8' studies the hitting time (L08 'First-Passage Times'). L06:102 Lesson 2 Theorem 2.5, Remark 2.6, Assumption 2.1 and A2 exist in L02.html (lines 289, 303, 93, 282). L06:127 A3 of Lesson 5 is at L05.html:271. L06:305 Lesson 8 exists.")

# numbers (re-derived this round, ledgers/SC1/scripts/SC1-b-r10/recompute_r10.py -> out/recompute_r10.txt)
RECOMP = "recomputed by ledgers/SC1/scripts/SC1-b-r10/recompute_r10.py (own code, out/recompute_r10.txt)"
P("b-num-L04", "1 prose numbers vs unrounded values (L04)", "course/modules/SC/SC1/L04.html:218-224, 271, 314, 321, 328, 420, 452",
  "e^1=2.718281828, e^0.25=1.284025417, e^4=54.598150033, e^8=2980.9579870417 (rounds to 2980.957987). " + RECOMP + ".")
P("b-num-L05", "1 prose numbers vs unrounded values (L05)", "course/modules/SC/SC1/L05.html:263, 368, 375, 382, 399, 458, 499",
  "5.55e-16/3.81e-29=1.4567e13 (E1 '1.457e13', '1.5e13' to 2 sf). 5.55e-16/2.22e-16=2.50 ('about 2.5'). 3.05e-16/2.22e-16=1.37 ('about 1.4'). Phi(-1/sqrt2)=0.2397500611 (5 dp 0.23975). p_1(0,0)=0.3989422804. Printed 1.0000000000 = erf(6)=1 to 17 dp. " + RECOMP + ".")
P("b-num-L06", "1 prose numbers vs unrounded values (L06)", "course/modules/SC/SC1/L06.html:290-296, 316, 320, 393, 400, 479, 511, 520",
  "Independent DP: #{M_N>=a,S_N=b} vs #{S_N=2a-b}: 1014 of 1014 triples; tail identity 78 of 78 pairs; N=12,a=3: 1588 of 4096, 495, 495; N=10,a=2: 281/512, 11/64 (so 2P=11/32), 105/512 = binom(10,6)/1024. erfc(1/sqrt2)=0.317310507863; P(B_1>1)=0.158655253931 (printed 0.1586552539 = rounding of the unrounded half). |0.3173105079-0.3173|=1.05e-5 < 1e-4; |P(B_1>=1)-0.1587|=4.5e-5 < 1e-4. " + RECOMP + ".")
P("b-lab-L04-hypothesis", "2.5 lab hypothesis matches code", "course/modules/SC/SC1/L04.html:147; tests/labs/SC1/lab-SC1-L04-1.py",
  "Hypothesis: t=2, theta in {-1,0.5,2}, relative 1e-9 (twin TOL=1e-9 relative for E[exp]), absolute 1e-9 for E[Z_t] (twin abs check). Matches twin lines 169-208.")
P("b-lab-L04-interpretation", "2.5 lab interpretation vs output", "course/modules/SC/SC1/L04.html:224, 230-232",
  "Printed 2.718281828, 1.284025417, 54.598150033 = e^1, e^(1/4), e^4 (checked). Each E[Z_t] prints 1.000000000. Says it does not prove the martingale property for other theta, t (Prop 2.4 does).")
P("b-lab-L04-docstring", "2.4 twin docstring vs code", "tests/labs/SC1/lab-SC1-L04-1.py:1-20",
  "Docstring: 'numerical, not simulated', 'Nothing is random', composite Simpson with PANELS on [-LIMIT, LIMIT], 'does not compute the mass beyond LIMIT': all match the code (lines 169-216).")
P("b-lab-L05-docstring-quadrature", "2.4 twin docstring vs code", "tests/labs/SC1/lab-SC1-L05-1.py:1-14, 214-229",
  "Docstring: composite Simpson on [-12,12], mass for 12<=|z|<=40 computed and printed (tail_mass), 'exact identity is proved on the page': matches code lines 186-253.")
P("b-lab-L05-hypothesis-interpretation", "2.5 lab hypothesis and interpretation vs output", "course/modules/SC/SC1/L05.html:170, 263, 306",
  "225 cases = 3*3*5*5 (checked). Printed largest gap 5.55e-16 < 1e-6 (tolerance 1e-6 in twin). Tail mass 3.81e-29 far below gap. Interpretation '2.5 times eps' and 'digits show no error larger than 5e-11' checked (see b-num-L05).")
P("b-lab-L06-claims", "2.5 lab claims vs output", "course/modules/SC/SC1/L06.html:186, 297",
  "Hypothesis: enumerates all 2^N for N=1..12; Part A no unequal triple; Part B no unequal pair; Part C 495/495; Part D 281/512 and 105/512; Part E erfc(1/sqrt2). Output (expected block 280-296) matches recomputation (1014, 78, 495/495, 281/512). Interpretation matches.")
P("b-lab-L06-docstring-exact-fraction", "2.4 twin docstring vs code", "tests/labs/SC1/lab-SC1-L06-1.py:1-14",
  "Docstring: 'Nothing is random', 2**N enumeration N=1..12, Part E closed form in floating point, b>=-N, 1<=a<=N: matches main() ranges (range(-n, a), range(1, n+1)).")

# math (re-read in full this round)
P("b-math-L04-lemma-2.1", "3 mathematics: Lemma 2.1 (MGF of normal)", "course/modules/SC/SC1/L04.html:81-89",
  "Completing the square: theta*y - y^2/(2h) = theta^2 h/2 - (y-theta h)^2/(2h) (checked). Density integrates to 1. Degenerate h=0 excluded by hypothesis h>0.")
P("b-math-L04-prop-2.2", "3 mathematics: Prop 2.2", "course/modules/SC/SC1/L04.html:93-105",
  "(H1),(H2) carry Assumptions 4.1, 4.2; E[B_t|F_s]=B_s + E[Y|F_s] = B_s via 4.2(a),(c),(d). Correct.")
P("b-math-L04-prop-2.3", "3 mathematics: Prop 2.3", "course/modules/SC/SC1/L04.html:109-123",
  "E[(B_t^2-t)^2]=3t^2-2t^2+t^2=2t^2 (checked). E[B_t^2|F_s]=B_s^2+h, E[B_t^2-t|F_s]=B_s^2-s (checked). Uses Lemma 2.2 of Lesson 3 (E X^4=3 Delta^2).")
P("b-math-L04-prop-2.4", "3 mathematics: Prop 2.4", "course/modules/SC/SC1/L04.html:129-149",
  "E[Z_t^2]=e^{-th^2}E[e^{2 theta B_t}]=e^{theta^2 t} (checked). E[W^2]=e^{theta^2 h} and E[W]=1 (checked). Conditional step by 4.2(c),(d) and Lemma 2.1.")
P("b-math-L04-A4.1-sketch", "3 sketch labelled as sketch, names skipped steps", "course/modules/SC/SC1/L04.html:65",
  "Labelled 'Sketch, not a proof'. Names the pi-system and pi-lambda steps it skips. (D1),(D3) cited correctly (Lesson 1 Definition 1.1).")
P("b-math-L04-misconception-1", "3 misconception 1 (mean zero is not martingale)", "course/modules/SC/SC1/L04.html:241",
  "E[B_t^3]=0; E[X_t|F_s]=B_s^3+3(t-s)B_s (checked by expansion, E[Y]=E[Y^3]=0, E[Y^2]=t-s). Differs from B_s^3 when B_s != 0 (s<t). Assumption use stated.")
P("b-math-L04-misconception-2", "3 misconception 2 (exp(theta B) not martingale)", "course/modules/SC/SC1/L04.html:244-245",
  "E[e^{theta B_t}]=e^{theta^2 t/2} changes with t when theta != 0; a martingale has constant expectation by 4.2(b) (P2). Correct.")
P("b-math-L04-R1-R3", "3 research problems R1-R3", "course/modules/SC/SC1/L04.html:336-353",
  "R1: k=t-g(t) deterministic martingale is constant, g=t+c (checked). R2: e^{c^2 h/2}=1 iff c=0 (checked, Z_s>0). R3: conditional variance t-s (checked).")
P("b-math-L04-M1-M3", "3 mechanics problems M1-M3", "course/modules/SC/SC1/L04.html:261-279",
  "M1 E[B^2]=t, E[B^4]=3t^2. M2 E[e^{B_2}]=e, E[Z_2]=1 (checked). M3 Var(Z_t)=e^{theta^2 t}-1, zero at theta=0 (checked).")
P("b-math-L04-E1-E3", "3 empirical problems E1-E3", "course/modules/SC/SC1/L04.html:311-328",
  "E1 e^{0.25}=1.284025417 (printed value). E2 e^8=2980.957987 (6 dp, rounds correctly). E3 e^{4*4/2}=e^8 (checked). E2 names Assumptions 4.1 and 4.2 (fixed).")
P("b-assumed-L04-E2", "2.1 item 6 'Assuming' rule: E2 solution names its assumption", "course/modules/SC/SC1/L04.html:321",
  "Round 9 FAIL is fixed. L04.html:321 now reads 'Assuming Assumptions 4.1 and 4.2, Proposition 2.4 gives E[Z_t^2]=e^{theta^2 t}=e^{4*2}=e^8'. Value re-derived (e^8=2980.9579870417).")
P("b-math-L05-lemma-1.3", "3 mathematics: Lemma 1.3 (independence of future increment)", "course/modules/SC/SC1/L05.html:89-103",
  "Proof uses D3 on partition 0=r_0<...<r_k=s<t, B_0=0 gives B_{r_j} as sums of increments, A4(f) grouping, pi-system closed under intersection, generates F_s, A4(a) extension. s=0 and s=t cases handled. Correct.")
P("b-math-L05-thm-1.4", "3 mathematics: Theorem 1.4 (Markov property)", "course/modules/SC/SC1/L05.html:105-123",
  "Apply A4(b) with f(z,y)=g(z+y); bar f(z)=E g(z+B_t-B_s); substitution y=z+w gives p_{t-s}(z,y) (since phi_u(y-z)=p_u(z,y)). s=t case: psi=g. Hypotheses A4(a),(b),(f) stated. Correct.")
P("b-math-L05-lemma-2.2-thm-2.1", "3 mathematics: Lemma 2.2 and Theorem 2.1 (Chapman-Kolmogorov)", "course/modules/SC/SC1/L05.html:135-165",
  "Lemma 2.2 re-derived: (z-x)^2/u+(y-z)^2/v = (u+v)/(uv)(z-m)^2+(y-x)^2/(u+v) with m=(vx+uy)/(u+v) (checked by expansion and cancellation). Theorem 2.1: constant (2pi)^{-1/2}(u+v)^{-1/2} from (2pi)^{-1}(uv)^{-1/2}(2 pi uv/(u+v))^{1/2}; hypothesis A4(e) stated. Correct.")
P("b-math-L05-A4i-statement", "3 numbered assumptions A4(a)-(i)", "course/modules/SC/SC1/L05.html:69, 327, 444; cards SC1-c214",
  "A4(i) is used only in M2 (L05.html:327) and the quiz explain (L05.html:444); grep of A4(i) shows no other use. Statement matches the use.")
P("b-math-L05-A3-sketch", "3 A3 sketch and steps skipped", "course/modules/SC/SC1/L05.html:271-281",
  "A3 stated (bounded rho). Sketch: rho_n=ceil(2^n rho)/2^n; countably many values; continuity gives convergence; names skipped steps (i) and (ii). Step (ii) needs A cap {rho_n=q} in F_q via F_rho subset F_{rho_n}: correct.")
P("b-math-L05-R3", "3 research problem R3 (dyadic approximation)", "course/modules/SC/SC1/L05.html:403-406",
  "ceil(x)<x+1 gives rho<=rho_n<rho+2^{-n}. {rho_n<=r}={rho<=floor(2^n r)/2^n} (checked). Correct.")
P("b-math-L05-problems", "3 problem set M1-M3, P1-P3, E1-E3, R1-R2", "course/modules/SC/SC1/L05.html:317-400",
  "M1 integral 1/(2 sqrt pi)=p_2(0,0) (checked). M2 psi(x)=x^2+2, x^3+6x (checked). M3 covariance 0. P1 Lemma 2.2 at u=1,v=3,x=0,y=1 (checked). P2 Phi formula. P3 normalisation. E2 error bound 5e-11 from 10 dp rounding. R1 counterexample paths: path 1 eta*=1/4, path 2 eta*=3/4 (checked). R2: F_s is contained in F_rho for the constant rho=s, and A3 applied to rho gives independence of B_t-B_s from F_s (checked).")
P("b-math-L05-misconceptions", "3 misconceptions L05", "course/modules/SC/SC1/L05.html:297-306",
  "Misconception 2: N(x,t-s)=N(0,t) iff x=0 and s=0 (checked). Misconception 3 states Theorem 2.1 hypotheses (checked).")
P("b-math-L05-def-1.1-st-case", "3 definitions (Markov, transition density) and s=t case", "course/modules/SC/SC1/L05.html:75-78, 122",
  "Def 1.1 quantifies over bounded Borel g with psi; Def 1.2 p_u matches integral normalisation (P3). s=t case: psi=g, E[g(B_t)|F_t]=g(B_t).")
P("b-math-L05-E1-E3", "3 empirical problems E1-E3 (L05)", "course/modules/SC/SC1/L05.html:365-382",
  "E1 ratio 1.457e13 vs printed values (checked). E2 unrounded interval [0.99999999995, 1.00000000005]. E3 |3.05e-16|/2.22e-16 = 1.37 ('about 1.4').")
P("b-scope-L05-E1-tail", "4 scope words in E1 solution", "course/modules/SC/SC1/L05.html:368",
  "'so that part of the tail cannot account for the gaps' (mass 3.81e-29 < gap 5.55e-16 on 12<=|z|<=40). Says explicitly 'this page makes no claim' for |z|>40.")
P("b-math-L05-quiz-Q7", "3 quiz Q7 (A3 sketch gap)", "course/modules/SC/SC1/L05.html:479-485",
  "Correct option names the two skipped steps (matches the sketch at L05.html:281). Explanation consistent.")
P("b-quiz-L05-Q7", "2.9 quiz L05 Q7 explanation", "course/modules/SC/SC1/L05.html:479-485",
  "Explanation 'proves the fixed-time case, sums over countably many values ..., names two skipped steps' matches L05.html:281.")
P("b-assumed-L05-quiz-Q9", "2.1 item 6 'Assuming' rule: quiz Q9 answer", "course/modules/SC/SC1/L05.html:497-499",
  "Round 9 FAIL is fixed. L05.html:499 now reads 'Under Assumptions A4(a), A4(b) and A4(f), Problem P2 gives Phi(-1/sqrt2)=0.23975006...'. Theorem 1.4 (L05.html:111) needs exactly A4(a),(b),(f). Value 0.2397500611 re-derived; tolerance 1e-5 satisfied.")
P("b-assumed-L05-quiz-M2", "2.1 item 6 'Assuming' rule: quiz Q2 answer", "course/modules/SC/SC1/L05.html:444",
  "Round 9 FAIL is fixed. L05.html:444 now reads '(Problem M2, under A4(a), A4(f) and A4(i))', matching the M2 solution at L05.html:327.")
P("b-scope-L05-canonical", "4 scope words in canon-breaks section", "course/modules/SC/SC1/L05.html:284-289",
  "'the strong Markov property at a stopping time that may be infinite is not covered by A3 as stated' and 'Lesson 8 ... finiteness is a result there' are accurate; A3 is stated for rho<=c.")
P("b-notation-L05-Phi-varphi", "5 notation: Phi and varphi vs notation/notation.json", "course/modules/SC/SC1/L05.html:121, 349-351",
  "Notation registry: '\\Phi' = standard normal CDF (module M4). L05 P2 uses Phi as the standard normal CDF (consistent). varphi_u is a local density (not registered); used only in the proof of Theorem 1.4.")
P("b-notation-L05-X-n", "5 notation: local symbols X^(n), rho_n", "course/modules/SC/SC1/L05.html:61-69, 281",
  "Symbols are local and defined where used (X^{(n)} defined in the sketch at L05.html:281). No registry symbol reused with another meaning.")
P("b-notation-M-clash", "5 notation: M_t, M_N running maximum", "course/modules/SC/SC1/L05.html:52, 268; L06.html:56, 112",
  "M_t and M_N denote the running maximum throughout L05-L06 (L06.html:56 defines M_N; L06.html:107 defines M_t). 'M' in problem labels M1-M3 is a label, not a symbol. No registry symbol uses M.")
P("b-scope-L05-D1D3", "4 scope: Sections 1 and 2 use (D1)-(D3) and A4(a),(b),(e),(f)", "course/modules/SC/SC1/L05.html:56",
  "Checked: Lemma 1.3 uses A4(a),(f); Thm 1.4 uses A4(b); Thm 2.1 uses A4(e); Lemma 2.2 uses none. The list is accurate.")
P("b-term-almost-surely", "5 term 'almost surely' defined before use", "course/modules/SC/SC1/L05.html:76, 122, 465; L06.html:170",
  "'almost surely' first appears in Definition 1.1 (L05.html:76) with '(that is, with probability one)' gloss in L06.html:144. Used consistently.")
P("b-math-L06-facts-unnumbered", "3 unnumbered facts in L06 section 2", "course/modules/SC/SC1/L06.html:102-130",
  "Facts from Lesson 2 are cited by number (Theorem 2.5, Remark 2.6, Assumption 2.1) and their hypotheses are named. None is used unnamed.")
P("b-math-L06-prop-1.3-cor-1.4", "3 mathematics: Proposition 1.3 and Corollary 1.4", "course/modules/SC/SC1/L06.html:75-97",
  "Bijection via Lemma 1.2 (checked: S'_N=2a-S_N, kappa'=kappa); endpoints b<a map to 2a-b>a and every sequence with S_N=2a-b has kappa<=N since S_0=0<a<2a-b. Corollary 1.4 counts: DP confirms 78/78 pairs and 1014/1014 triples. Correct.")
P("b-math-L06-prop-2.3-thm-2.5", "3 mathematics: Lemma 2.1, Prop 2.3, Theorem 2.5", "course/modules/SC/SC1/L06.html:123-170",
  "Proposition 2.3 hypotheses name A3 for rho=tau_a^t, A4(b),(c),(g),(h), all used in the proof (checked). Equal law by symmetry of N(0,u). Theorem 2.5: E = {W_t>a} (checked). Correct.")
P("b-math-L06-def-2.2-remark-2.4", "3 Definition 2.2 and Remark 2.4 (what is not proved)", "course/modules/SC/SC1/L06.html:118-121, 149",
  "Definition 2.2 states the path-level statement and says it is not asserted (A3 covers bounded stopping times only). Remark 2.4 says Proposition 2.3 is a one-time statement. Plan wording (plans/SC1-build-plan.md:261-263) says 'Assuming A3' for the path-level statement; see notes.")
P("b-math-L06-cor-2.6", "3 Corollary 2.6 (erfc closed form)", "course/modules/SC/SC1/L06.html:174-181",
  "2P(B_t>a)=erfc(a/sqrt(2t)) by substitution z=sqrt2 w (checked). erfc(1/sqrt2)=0.317310507863 matches Lab 1 Part E.")
P("b-math-L06-R1-R3", "3 research problems R1-R3 (L06)", "course/modules/SC/SC1/L06.html:407-424",
  "R1 parity argument (checked). R2 reflection of B: min B_s <= -a iff max(-B)_s >= a, then Theorem 2.5 (checked). R3 2x>x for x>0 (checked).")
P("b-math-L06-E1-E3", "3 empirical problems E1-E3 (L06)", "course/modules/SC/SC1/L06.html:383-400",
  "E1 78 = 1+...+12 (checked). E2 105/512 = 210/1024 = binom(10,6)/1024 (checked). E3 erfc(1/sqrt2)/2 = 0.15865525393..., printed 0.1586552539 (checked).")
P("b-math-L06-M-P-problems", "3 mechanics and proof problems (L06)", "course/modules/SC/SC1/L06.html:335-376",
  "M1 5 of 8, Corollary 1.4 gives 4+1 (checked). M2 1/4 (checked). M3 path S=(0,1,2,1,0,1), kappa=2, reflected S'=(0,1,2,3,4,3) (checked). P1 involution (checked). P2 (ii),(iii) from continuity (checked). P3 (checked).")
P("b-scope-L06-only-events", "4 scope words in L06", "course/modules/SC/SC1/L06.html",
  "'only' and 'exactly' uses in L06 are backed by a computation or a stated hypothesis (e.g. 'only the sequence (+1,+1) reaches 2', checked).")
P("b-scope-L06-N12-every-case", "4 scope: 'every case' with N<=12", "course/modules/SC/SC1/L06.html:297",
  "'every case with N<=12 and 1<=a<=N' matches the enumeration ranges in the twin (checked). Not claimed beyond N=12; the page says Section 1 proves it for all N.")
P("b-rounding-L06-misconception", "2.5/4 rounding claim", "course/modules/SC/SC1/L06.html:316",
  "0.3173 and 0.1587 are 4 dp roundings of 0.317310507863 and 0.158655253931 (checked).")
P("b-plan-L06-pathlevel", "2.8 plan vs page: path-level reflection", "course/modules/SC/SC1/L06.html:118-121, 149; plans/SC1-build-plan.md:261-263",
  "Page proves the fixed-time form only and says so (Definition 2.2, Remark 2.4, the hub lede). Plan line 261 specifies the path-level statement 'Assuming A3'. A3 is stated for bounded stopping times (L05.html:273-276) and tau_a is not shown bounded (L06.html:119), so the page's narrower claim is the one the stated assumptions support. Recorded as an architect decision in notes; not a page defect.")
P("b-causal-L06-symmetry-last-step", "7 causal claim: factor 2 and symmetry", "course/modules/SC/SC1/L06.html:306",
  "'The factor 2 comes from adding two events of equal probability': P(tau<=t)=P(B_t>=a)+P(W_t>a), equal by Prop 2.3 (checked). Symmetry used at h_-=h_+ (checked).")
P("b-l06-assumption-scope", "2.1 item 6: L06 assumptions named", "course/modules/SC/SC1/L06.html:307",
  "'Theorem 2.5 is conditional on A3 and A4 of Lesson 5, which are stated and not proved there.' Accurate (L05.html:270-277, A4 list at L05.html:58-72).")
P("b-l06-canon-symmetry-attribution", "2.1/3 attribution in canon section", "course/modules/SC/SC1/L06.html:300-307",
  "No external attribution; statements are proved or named as assumptions. Accurate.")
P("b-causal-L06-remark-2.4", "7 causal claim: Remark 2.4", "course/modules/SC/SC1/L06.html:149",
  "'Proposition 2.3 is a statement about one time' and 'does not show that the whole reflected path W is a standard BM' — accurate (only fixed-time law proved).")
P("b-hyp-L06-102-lesson2-hypotheses", "2.1 hypotheses of the Lesson 2 results cited", "course/modules/SC/SC1/L06.html:102",
  "Lesson 2 Theorem 2.5 (H2: A2 and Assumption 2.1; L02.html:289-292) and Remark 2.6 (A1(a),(b),(e), A2, Assumption 2.1; L02.html:547) match the page's description.")
P("b-ivt-observation", "3 IVT use in Lemma 2.1", "course/modules/SC/SC1/L06.html:112, 114",
  "IVT on [0,s*] and [0,t] with B_0=0<a: correct. Continuity used (Lemma 2.1 requires continuous paths; hypothesis listed).")
P("b-quiz-L06-Q8", "2.9 quiz L06 Q8", "course/modules/SC/SC1/L06.html:509-511",
  "P(B_1>=1)=erfc(1/sqrt2)/2=0.15865525393 -> 0.1587 (checked). 'B_1 has no atom' stated and true (normal law).")
P("b-lab-L05-gap-carry", "2.5 lab output carries gap values to the page", "course/modules/SC/SC1/L05.html:256-262",
  "Expected block lines 255-262 equal the twin output (twin_match_r10: expected == stdout True for L05).")

# cards (all 86 slice cards re-read this round; changed cards c084, c086, c087, c102, c117, c118, c193 re-verified)
P("b-cards-c061-c072", "2.7 cards c061-c072 vs lesson text", "course/modules/SC/SC1/cards.json (c061-c072)",
  "Read in full (out/cards_L04_06.txt). Each card matches Definition 1.1, Assumption 4.1, Definition 1.2, Lemma 2.1, Props 2.2-2.4, Lab 1 numbers. c071 'e^(theta^2 t)' and c072 '54.598150033', '1.000000000' match the lab output.")
P("b-cards-c073-c085", "2.7 cards c073-c085 vs lesson text", "course/modules/SC/SC1/cards.json (c073-c085)",
  "Read in full. c076 formula E[X_t|F_s]=B_s^3+3(t-s)B_s and c077 match the misconceptions. c084 (Definition 1.2) matches L05.html:82-84 after the change.")
P("b-cards-c086-c097", "2.7 cards c086-c097 vs lesson text", "course/modules/SC/SC1/cards.json (c086-c097)",
  "c086 (changed; pi-system gloss) and c087 (changed; 'transition density') re-read and match L05.html:101 and :115. c088 matches Remark 1.5. c093-c097 match A3, stopping time, R1-R3.")
P("b-cards-c098-c110", "2.7 cards c098-c110 vs lesson text", "course/modules/SC/SC1/cards.json (c098-c110)",
  "c102 (changed; 'floating-point rounding') matches L05.html:306 and the 225-case statement. c106-c110 match Section 1 of L06.")
P("b-cards-c111-c122", "2.7 cards c111-c122 vs lesson text", "course/modules/SC/SC1/cards.json (c111-c122)",
  "c111 1014, c112 78, c113 281/512, 11/32, 105/512, c114 495/495 and 2a-b=4: all match the expected block (L06.html:280-296). c117 and c118 (changed hypotheses) match Lemma 2.1 hypotheses at L06.html:106.")
P("b-cards-c123-c133", "2.7 cards c123-c133 vs lesson text", "course/modules/SC/SC1/cards.json (c123-c133)",
  "c123-c124 match Theorem 2.5 and Corollary 2.6. c126-c133 match misconceptions, problems M1, R1-R3 and A3 bound c=t.")
P("b-cards-duplicates", "2.7 duplicate cards", "course/modules/SC/SC1/cards.json (slice L04-L06, 86 cards)",
  "Script misc_checks_r10.py: no duplicate card ids (206 total, c219 added), no duplicate fronts or backs among slice cards.")
P("b-cards-c193-c204", "2.7 cards c193-c204 vs lesson text", "course/modules/SC/SC1/cards.json (c193-c204, c214, c216, c217)",
  "c193 (changed) matches A4(a); c194-c200 match A4(b)-(h) statements in L05.html:58-72; c202-c204 match Assumption 4.2(b)-(d). c216 5.55e-16 and 2.2e-16 scale match L05.html:263. c217 matches Proposition 2.3 hypotheses.")
P("b-cards-c079-c088-c100-c119", "2.7 spot cards c079, c088, c100, c119", "course/modules/SC/SC1/cards.json (c079, c088, c100, c119)",
  "c079 g(t)=t+c and c088 (discontinuous process allowed) and c100 (conditional law) and c119 (A3 covers bounded only) match the lesson text.")
P("b-cards-c103-c104-hypothesis", "2.7 cards c103, c104 hypotheses", "course/modules/SC/SC1/cards.json (c103, c104)",
  "c103 names A4(a),(f),(i) (matches L05.html:327); c104 names A4(a),(b),(f) (matches L05.html:111, 349).")
P("b-cards-ellipsis", "2.2 ellipsis in cards (plan 2.2 wording)", "cards c086, c106, c112 ",
  "Ellipses appear in finite index lists (0=r_0<...<r_k=s<t; e_1,...,e_N; 1+2+...+12) as unicode U+2026 in card text. Plan 2.2 wording bans 'any ellipsis outside code'; check_pages.py bans only '...' and BUILDER_RULES 1.3 bans 'an ellipsis standing for omitted content'. Not counted as FAIL (ambiguity), see notes.")

# structure, DAG, process words
P("b-dag-D1-D9", "2.8 DAG (prerequisite closure)", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "check_dag PASS (out/check_dag.txt). Every concept linked from L04-L06 exists in course/concepts.html (conditional-expectation-l2, moment-generating-function, independence, martingale, filtration, stopping-time, markov-property, reflection-principle, continuous-time-martingale, quadratic-variation: all present).")
P("b-process-words", "1/12 process words in learner text", "course/modules/SC/SC1/L04.html, L05.html, L06.html, cards.json",
  "Scan (misc_checks_r10.py) for round, verifier, agent, builder, ledger, batch, fragment in visible text and cards: no hit.")
P("b-banned-phrases", "2.9/3 banned phrases", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "check_pages PASS; separate scan finds no 'clearly', 'obviously', 'it is important to note', 'studies show', TODO, TBD in the three pages or the slice cards.")
P("b-hours-L04-L06", "2.8 hours arithmetic", "course/modules/SC/SC1/index.html:150-159; L04-L06 headers",
  "data-hours=9 for all eight lessons (grep), hub card '9 h' for each; 8 x 9 = 72; module 100 hours; 100 - 72 = 28 project hours, matching the hub text ('28 project hours').")
P("b-structure-sections", "2.9 structure sections", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "check_pages PASS; section order why-it-matters, core, canon-breaks, misconceptions, problems, key-results, quiz, references present in all three pages.")
P("b-struct-why-it-matters", "2.9 why-it-matters word count (<=120)", "course/modules/SC/SC1/L04.html:51, L05.html:52, L06.html:52",
  "Word counts from misc_checks_r10.py: L04 79, L05 116, L06 118 (all <= 120; LaTeX spans counted as one word).")
P("b-observation-transition-terms", "5 term consistency: transition density", "course/modules/SC/SC1/L05.html:115, 419; cards SC1-c087",
  "All three now say 'transition density' (L05.html:115 'the transition density is p_{t-s}', L05.html:419 table row, c087 back). No 'transition function' remains in L04-L06 (grep).")
P("b-quiz-L04-L06", "2.9 quiz items vs lesson text", "course/modules/SC/SC1/L04.html:377-465, L05.html:429-512, L06.html:450-530",
  "Each numeric answer checked: L04 2.718281828, 27, 3, 54.598150033; L05 3, 0.3989, 0.23975; L06 0.25, 0.3173, 0.1587. Each MC explanation matches the lesson text.")
P("b-quiz-L04-Q8-explain", "2.9 quiz L04 Q8 (round-9 FAIL, fixed)", "course/modules/SC/SC1/L04.html:432-438",
  "Round 9 FAIL is fixed. The Q8 prompt at L04.html:432 now reads 'Under Assumptions 4.1 and 4.2, is B_t + t a martingale?'. Explanation cites P1, which is stated under the same assumptions (L04.html:287-289).")
P("b-delta-L04-L06-hunks", "2.8 delta c93dd52..HEAD: every hunk in L04-L06 and cards re-read and re-derived",
  "course/modules/SC/SC1/L04.html (hunks 319-323, 430-434, 466-468); L05.html (52, 417-419, 442-444, 497-499); L06.html (64-68); index.html (31, 52, 64, 72, 136, 153-155, 182); cards.json (c084, c086, c087, c102, c117, c118, c193)",
  "git diff -U2 c93dd52 HEAD read in full for these files. Each hunk re-derived: L04:321 Assumptions named; L04:432 Q8 named; L05:444 and :499 named; L05:52 wording; L05:419 'transition density'; L06:66 kappa'=min{k:S'_k=a}, consistent with Lemma 1.2; hub hunks consistent with lesson text. The L04:37 cross-reference is not in the delta and is a separate FAIL (b-cross-L04).")
P("b-delta-cross-lessons", "2.8 delta: cross-lesson effects on slice", "git diff c93dd52 HEAD (L02.html 488, L03.html 50, 381)",
  "Delta changes outside the slice: L02.html:488 (explain text), L03.html:50 (why-it-matters), L03.html:381 (solution text). None changes a result, hypothesis or label that L04-L06 cite (Lemma 2.2, Assumption 3.2(a), Theorem 2.3, Theorem 2.5, Remark 2.6 in L02 unchanged).")
P("b-delta-twins-and-scripts", "2.8 delta: twins and scripts", "tests/labs/SC1/lab-SC1-L04-1.py, L05-1.py, L06-1.py",
  "git diff c93dd52 HEAD -- tests/labs/SC1 is empty; the changed twins are outside SC1 (BK4, E4, LX1, M3, M4, M7), not in this slice.")
P("b-scope-words-r5", "4 scope words in L04-L06", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "Scope words re-read in full this round; each 'only/all/every/always/exactly/same' is backed by a computation or a stated hypothesis (see rows b-scope-*).")
P("b-notation-r5", "5 notation (full pass)", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "Macros used: \\E, \\Prob, \\Var, \\Cov, \\R, \\indic, \\Normal, \\Phi (all registered or LaTeX builtins). No registered symbol reused (see b-notation-*).")
P("b-recompute-r5", "1 recomputation (independent)", "ledgers/SC1/scripts/SC1-b-r10/recompute_r10.py",
  RECOMP + ": closed forms, CK constants, tail masses, DP counts for Parts A-D, Part E erfc. All match the printed values.")
P("b-verify-refs-r5", "2.6 registry (round-5 row, re-run)", "references/references.json",
  "verify_refs --offline: 560 entries, 0 problems (out/verify_refs_offline.txt).")
P("b-l04-problem-set-E-intro", "2.1 problem-set intro", "course/modules/SC/SC1/L04.html:256",
  "'E2 and E3 ask about values that Lab 1 does not print': true (Lab 1 prints e^{theta^2 t/2} only for t=2, theta in {-1,0.5,2}; E2 is e^8 at theta=2,t=2 and E3 is t=4).")
P("b-prose-L04-R2-title", "2.9 prose: R2 title and statement", "course/modules/SC/SC1/L04.html:343-346",
  "Title 'When the exponential exp(cB_t) is a martingale' matches the statement and solution.")
P("b-prose-L04-remark-numbering", "2.9 prose: remark labels", "course/modules/SC/SC1/L04.html:37, 126",
  "L04 'Remark (the link with Lesson 3)' at L04.html:126 is unnumbered; L04:37 locator is the defect (b-cross-L04).")
P("b-scope-L04-footer", "4 footer claim", "course/modules/SC/SC1/L04.html:479",
  "Footer: 'Lab 1 is a numerical check and is labelled as one.' Accurate (expected block and the 'numerical' label in the lab docstring).")
P("b-math-L05-problems-title", "2.9 prose: problem titles L05", "course/modules/SC/SC1/L05.html:341, 355",
  "P1 title 'Verify Lemma 2.2 at one point, then in general' matches content; P3 title 'Normalisation of the transition density' matches content.")
P("b-prose-L05-P3-title", "2.9 prose: L05 P3 title", "course/modules/SC/SC1/L05.html:355",
  "Title matches the solution (integral of p_u(x,y) over y is 1).")
P("b-prose-L06-P2-title", "2.9 prose: L06 P2 title", "course/modules/SC/SC1/L06.html:366",
  "Title 'Parts (ii) and (iii) of Lemma 2.1 from continuity' matches the solution (checked).")
P("b-prose-L04-P3-title", "2.9 prose: L04 P3 title", "course/modules/SC/SC1/L04.html:300",
  "Title 'The product moment of a martingale at two times' matches E[Z_s Z_t]=E[Z_s^2].")
P("b-math-degenerate-L04-lemma-2.1", "3 degenerate cases: Lemma 2.1 with h>0 and t=0", "course/modules/SC/SC1/L04.html:81-82, 139-140",
  "Lemma 2.1 requires h>0. Prop 2.4 proof handles t=0 separately (Z_0=1, E[Z_0^2]=1=e^0). Correct.")
P("b-math-L04-quiz-degenerate", "3 quiz degenerate case Z_0", "course/modules/SC/SC1/L04.html:423-429",
  "Z_0 = exp(0) = 1 by (D1) B_0=0 (checked). Options consistent.")
P("b-math-L05-P2-hypothesis", "2.1 hypotheses of P2", "course/modules/SC/SC1/L05.html:349-351",
  "P2 solution names A4(a),(b),(f) (matches Theorem 1.4 hypotheses). Correct.")
P("b-hub-L06-objective", "2.9 hub objective L06 vs lesson", "course/modules/SC/SC1/index.html:54; L06.html:118-121",
  "Hub now reads 'Prove the fixed-time reflection identity for Brownian motion (Lesson 6, Theorem 2.5), under Assumptions A3 and A4'. Theorem 2.5 is that identity and the page proves only the fixed-time form (Remark 2.4). Consistent (round-9 observation resolved).")
P("b-ck-independent-L05", "3 independent check of Chapman-Kolmogorov numbers", "course/modules/SC/SC1/L05.html:255-262; tests/labs/SC1/lab-SC1-L05-1.py",
  "Own code recomputation (recompute_r10.py): quadrature of the CK integrals is not re-run beyond the twin; printed values checked: erf(6)=1 for the mass; gap scale 2.5 eps; 'the largest gap below 1e-6: True'. Twin run this round gives the same expected block (twin_match_r10).")
R["b-hub-L04-description"] = ("2.9 hub card text describes L04 content", "course/modules/SC/SC1/index.html:155 vs L04.html:232", "PASS",
  "Round-9 FAIL is fixed. index.html:155 now reads 'The filtration of Brownian motion, the martingales B_t, B_t^2-t and the exponential martingale.' No optional stopping promised; L04.html:232 says the lesson makes no optional-stopping claim. Consistent.", "")

P("b-math-L06-lemma-2.1", "3 mathematics: Lemma 2.1 (running maximum and first visit)", "course/modules/SC/SC1/L06.html:105-115",
  "(i) M_t>=a iff tau_a<=t: IVT on [0,s*] and closedness of {s: B_s=a} (checked). (ii) B_t>=a implies tau_a<=t by IVT on [0,t] (checked). (iii) On {tau_a>t}, B_s<=a on [0,t] and B_s != a for s<tau_a, so B_t<a (checked). Hypotheses (continuous paths, B_0=0, a>0, t>0) are the ones used.")
P("b-assumed-facts-statement", "2.1 item 6 'Assuming' rule: statements that use a numbered Assumption say so", "course/modules/SC/SC1/L04.html, L05.html, L06.html",
  "Every result statement and proof re-read. Statements that use an Assumption name it: L04 Props 2.2-2.4 (L04:98, 114, 134), L04 M2, M3, P1-P3, R1-R3 and quiz Q5, Q8, Q9, L04 E2 (L04:321, fixed); L05 Lemma 1.3 (L05:95), Thm 1.4 (L05:111), Thm 2.1 (L05:147), A3 (L05:271-279), M2 (L05:327), P2 (L05:349), R2 (L05:399), quiz M2 (L05:444, fixed), quiz Q9 (L05:499, fixed); L06 Prop 2.3 and Thm 2.5 (L06:126-130, 159), Cor 2.6 (L06:176), R2-R3 (L06:415, 422). Results that need no assumption (L04 Lemma 2.1, L05 Lemma 2.2, L06 Lemma 2.1, L06 Prop 1.3 and Cor 1.4) state none. The round-9 defects at L04:321, L04:432-438, L05:444 and L05:497-499 are fixed.")

ids9 = [r["id"] for r in json.load(open("/Users/billyribeiro/.fanout/frags/E-SC1-b.round9.json"))["rows"]]
missing = [i for i in ids9 if i not in R]
extra = [i for i in R if i not in ids9]
print("missing:", missing)
print("extra:", extra)

rows = []
for i in ids9:
    check, loc, status, ev, fix = R[i]
    rows.append({"id": i, "check": check, "location": loc, "status": status, "evidence": ev, "fix": fix})
counts = {"PASS": sum(r["status"] == "PASS" for r in rows), "FAIL": sum(r["status"] == "FAIL" for r in rows),
          "UNVERIFIABLE": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
frag = {
    "unit": "SC1",
    "slice": "b",
    "round": 10,
    "verifier": "independent verifier (Haiku 5.5), round 10",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (round-9 pin); delta c93dd52..00a8479 (commits 47a36d8c, 00a84795)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-SC1-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE10-SC1-b/ledgers/SC1/scripts/SC1-b-r10",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b is lessons L04-L06 with their lab twins and the hub/cards rows that cite them. No project grader is in the slice, so no student-error mutant is counted and mutants is empty (same ruling as round 9; plan 2.1 item 11 and FINAL-ARCHITECT-RULINGS 9 do not apply).",
        "Round-10 delta c93dd52..00a8479 touches L04.html (3 hunks), L05.html (4), L06.html (1), index.html (8), cards.json (7 slice cards). Every hunk was read and re-derived. Carry-forward was not used: every page was re-read in full this round, so each row carries fresh evidence.",
        "Round-9 FAIL rows b-assumed-L04-E2, b-assumed-L05-quiz-Q9, b-assumed-L05-quiz-M2, b-hub-L04-description, b-quiz-L04-Q8-explain, b-delta-L04-L06-hunks and b-assumed-facts-statement are fixed in 00a8479 and re-verified PASS.",
        "New FAIL found this round: b-cross-L04. L04.html:37 cites 'the remark after Proposition 2.3' of Lesson 3; Lesson 3 has no Proposition 2.3 and no Remark block. The round-9 PASS row for that line (b-cross-L04) was wrong. Fix is one phrase in L04.html:37 (outside this slice; reported, not edited).",
        "Observation (architect): plans/SC1-build-plan.md:261-263 specifies the L06 path-level reflection as 'Assuming A3'. The page proves only the fixed-time form (Definition 2.2, Remark 2.4) because A3 covers bounded stopping times and tau_a is not shown bounded. The page's narrower claim is the one the stated assumptions support, so no row fails; the plan wording should be reconciled.",
        "Observation (architect, plan 2.2 vs BUILDER_RULES 1.3): plan 2.2 bans 'any ellipsis outside code'; check_pages.py bans only '...'; BUILDER_RULES 1.3 bans 'an ellipsis standing for omitted content'. Slice uses unicode ellipses in finite index lists in cards c086, c106, c112 and LaTeX \\dots in finite sequences on L05.html:101, L06.html:56. Not counted as FAIL; the architect should settle the wording (same open item as round 9).",
        "Observation: L05 M1 and P3 cite 'the Gaussian integral' and 'the standard normal density integrates to 1' without the A4(e) label. Both are A4(e) facts, named by description. Not counted.",
        "Observation: card c127 is graded C although its claim is established by Corollary 1.4 (T) and the lab is only an instance. Conservative, not a defect.",
        "Observation: L04.html:147 and L05.html:170 and L06.html:186 use 'Predicted before running' / 'Prediction:'. Read as pedagogy, not build-process wording; process-word scan (misc_checks_r10.py) found no build-process term.",
        "Not checked: the whole-repository gate (whole ruff/mypy, full pytest, render_curriculum, build_site --check, fetch_data --check, check_pages/check_dag/check_projects --all, verify_refs over the registry); only slice-scoped commands were run. run_graders and mutate_graders were not run (no project grader in slice). embed_labs --refresh was not run (twin_match_r10 checks page code == twin and expected == stdout instead). No browser screenshot. Shreve (2004) and Karatzas & Shreve (1991) were not read; no passage is attributed to either. Verify_refs --unit SC1 performs a live check on the registry; it returned 0 problems and was run with the repository tool only.",
    ],
    "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"], "mutants": 0, "mutants_killed": 0},
}
out = "ledgers/SC1/SC1-b.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("wrote", out, frag["verdict"], frag["summary"])
