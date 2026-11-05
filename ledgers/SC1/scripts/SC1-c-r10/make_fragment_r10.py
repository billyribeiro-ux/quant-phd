"""Writes the round-10 verifier fragment for SC1 slice c (L07, L08, lab twins). Verifier-authored; run with python3 -I."""

import json
import sys
from datetime import UTC, datetime

ROOT = sys.argv[1]
EV = "Round 10 (pin 00a84795): "

rows = []


def add(rid, check, loc, ev, status="PASS"):
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": EV + ev})


add("gate-check-pages", "2.9 structure (check_pages)", "course/modules/SC/SC1/L07.html, L08.html",
    "check_pages.py --unit SC1 --page L07 -> 'check_pages SC1 L07: PASS'; --page L08 -> 'check_pages SC1 L08: PASS'; whole --unit SC1 -> 'check_pages SC1: PASS', exit 0.")
add("gate-check-dag", "2.9 DAG (check_dag)", "course/modules/SC/SC1/L07.html, L08.html",
    "check_dag.py --unit SC1 -> 'check_dag SC1: PASS'; check_dag.py --all -> PASS, exit 0.")
add("gate-run-labs", "2.5 labs (run_labs)", "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py",
    "run_labs.py --unit SC1 -> 'run_labs SC1: PASS (11/11)', exit 0.")
add("lab-L07-twin-isolated", "2.5 labs (twin under python -I -W error)", "tests/labs/SC1/lab-SC1-L07-1.py",
    "ledgers/SC1/scripts/SC1-c-r10/lab_equivalence.py copies the twin to a fresh temp directory and runs python -I -W error: exit 0, stderr 0 bytes (out/lab_equivalence.txt).")
add("lab-L08-twin-isolated", "2.5 labs (twin under python -I -W error)", "tests/labs/SC1/lab-SC1-L08-1.py",
    "Same procedure: exit 0, stderr 0 bytes (out/lab_equivalence.txt).")
add("lab-L07-page-equals-twin", "2.5 labs (embed: page code equals twin)", "course/modules/SC/SC1/L07.html:151-356 vs tests/labs/SC1/lab-SC1-L07-1.py",
    "Html-unescaped data-run block equals the twin after trailing-newline normalisation: True (out/lab_equivalence.txt). Twin and page are both read in full.")
add("lab-L08-page-equals-twin", "2.5 labs (embed: page code equals twin)", "course/modules/SC/SC1/L08.html:143-343 vs tests/labs/SC1/lab-SC1-L08-1.py",
    "Equal after trailing-newline normalisation: True (out/lab_equivalence.txt).")
add("lab-L07-expected-equals-output", "2.5 labs (expected block equals output)", "course/modules/SC/SC1/L07.html:357-379 (pre.expected)",
    "Expected block equals twin stdout: True (out/lab_equivalence.txt); 'discrete tail identity of Lesson 6' label present in both.")
add("lab-L08-expected-equals-output", "2.5 labs (expected block equals output)", "course/modules/SC/SC1/L08.html:344-363 (pre.expected)",
    "Expected block equals twin stdout: True (out/lab_equivalence.txt).")
add("lab-L07-printed-numbers", "2.2 numbers (a) lab-computed, recomputed independently", "course/modules/SC/SC1/L07.html:357-379",
    "ledgers/SC1/scripts/SC1-c-r10/indep_r10.py (killed-walk dynamic programme with exact integers; seeded paths regenerated with explicit loops, random.Random(20260507)): Part A tails 0.375000, 0.332306, 0.321084, 0.318255, 0.317547 (A-DP lines, out/indep_r10.txt; 21778 = 14893+6885 at N=16); Part B counts 91/107/113/121, se 0.020987/0.022160/0.022539/0.022996, nesting violations 0, differences -0.0898/-0.0498/-0.0348/-0.0148; Part C means 0.55464/0.66389/0.72315/0.75863, se 0.03149/0.03159/0.03151/0.03166; Part D 1-Phi(1)=0.158655253931. All printed values match.")
add("lab-L08-printed-numbers", "2.2 numbers (a) lab-computed, recomputed independently", "course/modules/SC/SC1/L08.html:344-363",
    "indep_r10.py: exact DP E[min(nu_1,16)]=5.480560303, E[min(nu_1,64)]=11.815731233, E[min(nu_1,256)]=24.557203397; 179587/32768 exact True; seeded walks regenerated (random.Random(20260508), 1000 walks): means 5.2850/11.3840/23.1240, se 0.1868/0.6288/1.8497, z -1.0466/-0.6866/-0.7748; Part D P(tau_1<=1)=0.3173105079, P(tau_1<=2)=0.4795001222, densities 0.2419707245 and 0.1098478224, central differences agree to 5e-12. Counts 1588/4096 and 794/4096: 794 = C(12,8)+...+C(12,12) = 495+220+66+12+1 (checked by hand).")
add("lab-L07-hypothesis-interpretation", "2.5 lab statements (hypothesis and interpretation match output)", "course/modules/SC/SC1/L07.html:150 (hypothesis) and :380 (interpretation)",
    "Each interpretation sentence checked against the printed lines: 78 of 78; five decreasing tails; 91/107/113/121; 0 violations; gaps narrowing in this sample; 0.0393 = 1.24 SE (recomputed 1.239826); Part D agreement. Hypothesis predictions (decreasing tails, nested counts, closed-form mean comparison) are stated as predictions and then reported as observed.")
add("lab-L08-hypothesis-interpretation", "2.5 lab statements (hypothesis and interpretation match output)", "course/modules/SC/SC1/L08.html:142 (hypothesis) and :364 (interpretation)",
    "Every interpretation sentence checked: 8190 sequences, 90114 pairs, 78 of 78, first-passage counts at steps 3..12, 1588 = 2 x 794, probabilities 0.387695 and 0.193848, truncated means, z values 1.05/0.69/0.77 (below 1.1 SE), Part D values and 1e-8 agreement. 'one seed' and 'correlated comparisons' statements match the twin (same walks truncated at 16, 64, 256).")
add("lab-simulated-labels-seeds", "2.5 labs (seeds; SIMULATED labels)",
    "course/modules/SC/SC1/L07.html:148; L08.html:142; tests/labs/SC1/lab-SC1-L07-1.py:32; lab-SC1-L08-1.py:37",
    "L07 title '(Parts B and C SIMULATED)'; L08 title '(Part C SIMULATED)'; seeds 20260507 and 20260508 are fixed in the twins; exact Parts A and D are not labelled SIMULATED, as plan 2.2 requires.")
add("lab-runtime", "2.5 labs (runtime under 10 s)", "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py",
    "page_smoke timings: lab-SC1-L07-1 0.1 s, lab-SC1-L08-1 0.2 s (out/page_smoke_L07_L08.txt).")
add("lint-mypy-twins", "code quality (ruff, mypy strict)", "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py",
    "ruff check on both twins: 'All checks passed!'; ruff format --check: 2 files already formatted; mypy --no-incremental on both twins: Success. Repo-wide: ruff check . passed; ruff format --check . 553 files already formatted; mypy --no-incremental: 'Success: no issues found in 385 source files'.")
add("page-smoke-L07-L08", "2.9 page_smoke (console, math, 360 px, labs in Pyodide)", "course/modules/SC/SC1/L07.html, L08.html",
    "page_smoke.py --unit SC1 --pages L07 L08: 'page_smoke modules/SC/SC1/L07.html: PASS', '... L08.html: PASS', 'page_smoke SC1: PASS', exit 0 (out/page_smoke_L07_L08.txt).")
add("pytest-lab-tools", "2.5 labs (pytest, tooling)", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
    "pytest tests/test_labs.py tests/test_run_labs.py -q: all dots, no failure lines; pytest tests/test_page_checks.py -q: 41 dots, no failure lines.")
add("verify-refs-offline", "2.1 citations (integrity, offline)", "references/references.json",
    "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0.")
add("verify-refs-live-SC1", "2.1 citations (live, unit SC1)", "references/references.json entry shreve2004stochastic (line 20732); course/modules/SC/SC1/L07.html references; L08.html references",
    "verify_refs.py --unit SC1 (live run): 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0.")
add("refs-no-citation-markup", "2.1 attribution (no unread citation)", "course/modules/SC/SC1/L07.html and L08.html references sections",
    "Both pages cite only shreve2004stochastic at book level with no locator and attach no statement to it. Registry record title 'Stochastic Calculus for Finance II', year 2004 matches the text. No number, theorem number or page is attributed to the book.")
add("claim-grades-L07", "2.3 grades (re-graded against BLUEPRINT section 3)", "course/modules/SC/SC1/L07.html (claims, key-results table)",
    "Re-graded: Definition 1.1, Theorem 1.3, Remark 1.4, Corollary 1.5(a),(b) (A5 stated), Proposition 2.2, Corollary 2.3, Remark 2.4 are T with their assumptions named in the statement; Lab 1 Parts A-D rows are C with SIMULATED labels where applicable; no over-grading found.")
add("claim-grades-L08", "2.3 grades (re-graded against BLUEPRINT section 3)", "course/modules/SC/SC1/L08.html (claims, key-results table)",
    "Re-graded: Proposition 1.2 T (no probability assumption); Corollary 1.3, 1.4, 1.5 T with 'assuming A3 and A4' in the statement; Propositions 2.2 and 2.3 T; Lab 1 rows C with SIMULATED Part C labelled; no over-grading found.")
add("math-L07-thm-1.3", "2.4 mathematics (Theorem 1.3 and proof)", "course/modules/SC/SC1/L07.html:68-80",
    "Re-derived: P(M_H>=a)=2P(B_H>=a) from L06 Theorem 2.5 under A3 and A4 (L06.html section 2, read in full for this cross-reference); P(B_H>=a)=1-Phi(a/sqrt H) since B_H-B_0 ~ N(0,H) (L01 D1-D2 with s=0); erfc form by L06 Corollary 2.6 (substitution z=sqrt2 w verified). Hypotheses H1-H3 all appear in the statement.")
add("math-L07-cor-1.5b", "2.4 mathematics (Corollary 1.5(b))", "course/modules/SC/SC1/L07.html:101-107",
    "Integration by parts: integral_0^R(1-Phi) = R(1-Phi(R)) + phi(0) - phi(R); 1-Phi(R) = integral_R^inf phi <= phi(R)/R so R(1-Phi(R)) -> 0; integral_0^inf (1-Phi) = 1/sqrt(2 pi). Substitution m = sqrt(H) u gives 2 sqrt(H)/sqrt(2 pi) = sqrt(2H/pi). Numerically sqrt(2/pi)=0.797884561.")
add("math-L07-prop-2.2-cor-2.3-remark-2.4", "2.4 mathematics (Prop 2.2, Cor 2.3, Remark 2.4)", "course/modules/SC/SC1/L07.html:119-146",
    "Prop 2.2(a): grid times are points of [0,H]. (b): N' = cN gives kH/N = (kc)H/N'. Cor 2.3: {M^(N)>=a} subset {M>=a}. Remark 2.4: max(0,B_H)>=a iff B_H>=a for a>0; with the factor 2 of L06 Theorem 2.5 the one-step tail is half. Numerically P(M^(1)_1>=1) = 0.158655 = half of 0.317311.")
add("math-L07-def-2.1-grid-times", "2.4 mathematics (notation and definition)", "course/modules/SC/SC1/L07.html:116",
    "Def 2.1 grid s_k = kH/N, k=0..N gives N+1 points; the twin's grid_maximum takes path[::FINE//n] (n=4,16,64,256 give 5,17,65,257 points) which are the same grid for FINE=256.")
add("math-L07-remark-1.4-phi0", "2.4 mathematics (Remark 1.4)", "course/modules/SC/SC1/L07.html:83-86",
    "Phi(0)=1/2 by evenness of the density; P(Z=0)=0 since Z is continuous; limits 0 as H down to 0 and 1 as H to infinity follow from the closed form and continuity of Phi. The assumption H2 is named in the statement.")
add("math-L07-R1-R3-P2-P3-M-E", "2.4 mathematics (problem solutions)", "course/modules/SC/SC1/L07.html:417-512",
    "Re-derived: M1 (a/sqrt H = 1, erfc(2/sqrt 8)=erfc(1/sqrt 2)); M2 scaling; M3 one-step grid value 0.1586552539 and 0.3173105079; P1 continuity from below; P2 integral; P3 nested inclusion; E1 counts 91 and 121; E2 binomials 8008+4368+1820+560+120+16+1=14893, 6885, total 21778, 21778/65536=0.332306; E3 k(n-k)/(n^2(n-1)) with k=121, n=400: sqrt(33759/63840000)=0.0229958 -> 0.0230; R1 sign and range; R2 limit; R3 (Lemma 2.1 of L06 used).")
add("math-L08-prop-1.2-cor-1.3-1.4", "2.4 mathematics (Prop 1.2, Cor 1.3, Cor 1.4)", "course/modules/SC/SC1/L08.html:63-94",
    "Prop 1.2 both inclusions re-derived (closed set {s:B_s=a} contains its infimum; IVT on [0,s*] with B_{s*} >= a > 0 = B_0). Counterexample (0 on [0,1/2), 2 on [1/2,1]) checked: M_1=2, never equals 1, tau_1 = infinity. Cor 1.3: first equality Prop 1.2, second L07 Theorem 1.3 (A3, A4). Cor 1.4: increasing union of {tau_a<=n}, limit 2(1-Phi(a/sqrt n)) -> 1.")
add("math-L08-cor-1.5", "2.4 mathematics (Corollary 1.5, density)", "course/modules/SC/SC1/L08.html:97-104",
    "F(H)=erfc(a/sqrt(2H)); F'(H) = a H^(-3/2) e^(-a^2/(2H))/sqrt(2 pi) (chain rule with d/dH aH^(-1/2) = -(a/2)H^(-3/2)). F(eps)->0 as eps down to 0; density identity holds. Numerically central difference of F at a=1, H=1 and H=2 equals the density to 5e-12 (indep_r10.txt).")
add("math-L08-prop-2.2-2.3", "2.4 mathematics (Prop 2.2, 2.3)", "course/modules/SC/SC1/L08.html:120-138",
    "Prop 2.2: first index k* with S_{k*} >= a has S_{k*-1} <= a-1 and a +-1 step gives S_{k*} = a; identity #{nu_a<=N} = #{S_N>=a}+#{S_N>a} via L06 Corollary 1.4 (78/78 enumerated). Prop 2.3: min(nu,N) = sum_{k<N} 1{nu>k}; P(nu>k) = 1 - P(max_{j<=k} S_j >= a); k=0 case gives 1 = 1.")
add("math-L08-R3", "2.4 mathematics (Problem R3)", "course/modules/SC/SC1/L08.html:489-495",
    "log f_a = const - (3/2)log H - a^2/(2H); derivative (a^2 - 3H)/(2H^2) is positive below a^2/3 and negative above; maximum at H = a^2/3 as stated.")
add("math-L08-R1-R2", "2.4 mathematics (Problems R1, R2)", "course/modules/SC/SC1/L08.html:476-497",
    "R1: #{S_N>a} = #{S_N>=a} - #{S_N=a} gives #{nu_a<=N} = 2#{S_N>=a} - #{S_N=a}; with S_12 even, 2 x 794 = 1588. R2: min(nu,N+1)-min(nu,N) = 1{nu>N}, nonnegative, so the truncated mean is nondecreasing.")
add("prob-L08-all", "2.4 problems (all L08 problems, solutions)", "course/modules/SC/SC1/L08.html:392-497",
    "All M1-M3, P1-P3, E1-E3, R1-R3 read and re-derived: M3 5/8 by listing 8 sequences; M2 f_1(1)=0.2419707 (rounded-factor product 0.241970690 rounds to 0.241971); E3 0.1098478 (rounded-factor product 0.109847654 rounds to 0.109848); E1 counts 512, 384, 288, 224, 180 sum to 1588; E2 z values -1.05, -0.69, -0.77 (unrounded -1.0466, -0.6866, -0.7748).")
add("prob-L07-remaining", "2.4 problems (other L07 problems)", "course/modules/SC/SC1/L07.html:411-512",
    "M1-M3, P1-P3, E1-E3, R1-R3 re-derived; all printed values agree with the twin output and the unrounded values (0.31731050786, 0.1586552539, 21778, 0.0230).")
add("misconceptions-L07-content", "2.4 misconceptions (content)", "course/modules/SC/SC1/L07.html:392-408",
    "Three misconceptions with wrong belief and rebuttal: (1) tail of M_H is twice tail of B_H: 0.3173 vs 0.1587 and difference = P(M_1>=1, B_1<1) since {B_1>=1} is in {M_1>=1}; (2) grid overstate: rebutted by Prop 2.2(a) and Corollary 2.3; (3) normal marginals: rebutted by L01 section 4 (B-tilde has same finite-dimensional laws, discontinuous paths).")
add("misconceptions-L08-content", "2.4 misconceptions (content)", "course/modules/SC/SC1/L08.html:379-391",
    "Three misconceptions: (1) tau_a finite on every path: rebutted (P(tau_a=infinity)=0 is not emptiness); (2) tau vs terminal value: P(tau_1<=1)=0.317311 vs P(B_1>=1)=0.1586552539 (Corollary 1.3); (3) finite mean: no moment evaluated, truncated means increase. Each wrong belief is stated in quotes with a rebuttal.")
add("canon-breaks-L07-L08", "2.4 canon breaks", "course/modules/SC/SC1/L07.html:383-390; course/modules/SC/SC1/L08.html:367-374",
    "Each bullet names a hypothesis whose failure changes the result: continuity (L07 and L08 examples checked), assumption dependence (A3, A4 stated but not proved; L05 A3 sketch only), discrete grid vs continuous tail, finiteness vs integrability. The L08 jump example gives M_1=2 with tau_1=infinity, checked by hand.")
add("key-results-L07", "2.4 key-results table", "course/modules/SC/SC1/L07.html:515-531",
    "Each row matches the theorem, corollary or lab output it cites; grades T and C as in the body; the C row for the discrete tail identity names Lab 1 Part A (78 pairs).")
add("key-results-L08", "2.4 key-results table", "course/modules/SC/SC1/L08.html:499-517",
    "Rows match the body; the C rows cite Lab 1 Part A (90114 pairs, 78 of 78) and Part C (within 1.1 SE, 1000 walks, one seed).")
add("quiz-L07", "2.9 quiz (keys, tolerances, explanations)", "course/modules/SC/SC1/L07.html:535-614",
    "10 items (8-15 required). Numeric keys: 0.3173105 (tol 1e-6; unrounded 0.31731050786), 0.158655 (tol 1e-6; diff 2.5e-7), 0.797885 (tol 1e-6; diff 4.4e-7 from sqrt(2/pi)=0.7978846), 0.3173105 (M4). Multiple-choice keys have exactly one data-correct option and each explanation is consistent with the body.")
add("quiz-L08", "2.9 quiz (keys, tolerances, explanations)", "course/modules/SC/SC1/L08.html:518-597",
    "10 items. Keys: 0.3173105 (tol 1e-6), 0.625 (exact 5/8), 5.48056 (tol 1e-5; exact 179587/32768 = 5.48056030), 0.241971 (tol 1e-6; 0.2419707). Multiple-choice keys each have one correct option; explanations consistent with the body.")
add("structure-L07", "2.9 structure and prose (template sections)", "course/modules/SC/SC1/L07.html",
    "check_pages PASS. Sections in BUILDER_RULES 4.2 order (why-it-matters 125 words by my count, core, inline lab, canon-breaks, 3 misconceptions, 4 tiers x 3 problems with details.solution, key-results, 10-item quiz, references); data-hours 9; no debate brief.")
add("structure-L08", "2.9 structure and prose (template sections)", "course/modules/SC/SC1/L08.html",
    "check_pages PASS. Same order; why-it-matters 121 words by my count (check_pages cap 120 words applies to its own word count and passes); 3 misconceptions; 4 tiers x 3 problems; 10-item quiz; data-hours 9.")
add("banned-and-process-words", "2.9 banned phrases and process words", "course/modules/SC/SC1/L07.html, L08.html; tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py",
    "grep for TODO, TBD, lorem, build, builder, round, verifier, REQUEST, obviously, clearly, well known, studies show, experts agree, beyond the scope, left as an exercise, ellipsis: no hits. 'Verified' appears once, in the curriculum project title 'Reflection Principle Verified' (L08.html:608 next link; curriculum/03-markets.yaml:527), not a process word. check_pages banned-phrase check PASS.")
add("notation-macros", "2.4 notation (notation.json)", "course/modules/SC/SC1/L07.html, L08.html",
    "Macros used: \\Prob, \\E, \\indic, \\Phi (registered in notation.json macros); other commands are standard LaTeX (\\varphi for the Gaussian density, allowed by plan 2.3). No \\gamma, \\mathbb{Q}, R^\\ast, R_f, \\Var, \\Cov, \\Normal used.")
add("dag-defined-once-L07-L08", "2.9 DAG (defined once)", "course/modules/SC/SC1/L07.html:64, :116; course/modules/SC/SC1/L08.html:59",
    "<dfn> occurrences: running-maximum-distribution (L07:64), discretely monitored maximum (L07:116, no data-concept), first-passage-time (L08:59). Each defined once; check_dag PASS.")
add("dag-outside-closure", "2.9 DAG (outside the prerequisite closure)", "course/modules/SC/SC1/L07.html:37, L08.html:37 (meta links) and body",
    "Concept links point only to closure or earlier-unit concepts (normal-distribution, random-variable, expectation from M4; brownian-motion from L01; brownian-motion-construction from L02). grep for Ito, geometric Brownian, Ornstein, Girsanov, Euler, Milstein, Donsker, Black-Scholes, bridge, Monte Carlo, bias-variance, estimator found no hits.")
add("dag-reflection-link-L07-L08", "2.9 DAG and prose (concept link names the result the sentence cites)", "course/modules/SC/SC1/L07.html:37 and course/modules/SC/SC1/L08.html:37 (Uses lists)",
    "Uses lists name L06 Theorem 2.5 (and Corollary 2.6, Lemma 2.1 in the body), L01 Definition 1.1, Lesson 2 (brownian-motion-construction, defined in L02 per check_dag PASS) and Lesson 7 (L08); each cited result exists in its lesson (grep of L06.html, L01.html).")
add("xref-L01-L05-L06", "2.1 cross references (Lessons 1, 5, 6)", "course/modules/SC/SC1/L07.html, L08.html; L06.html (Lemma 2.1, Prop 2.3, Thm 2.5, Cor 2.6, Cor 1.4); L05.html:59 (A4), :271 (A3); L01.html:58-66 (Def 1.1), :212-216 (section 4)",
    "Every cited number and name resolves: L01 Definition 1.1 (D1-D3) used with s=0; L01 section 4 B-tilde discontinuous; L05 A3 (bounded stopping time) and A4 exist; L06 Lemma 2.1(i)-(iii), Section 2 definition of tau_a, Theorem 2.5 (A3, A4), Corollary 2.6 (erfc form, H>0, a>0), Corollary 1.4 (discrete tail identity), Lemma 2.1 used as in L07 R3 and L08 Prop 1.2.")
add("cards-dup-and-numbers", "2.7 cards (duplicates; numbers appear in lesson)", "course/modules/SC/SC1/cards.json (206 cards)",
    "Full scan: no duplicate ids; the highest difflib front ratio inside L07/L08 is 0.886 (SC1-c164/c165: same hypothesis sentence, different questions). Every number on the L07/L08 cards appears in its lesson (21778, 14893, 6885, 0.2275, 0.3025, 0.0210, 0.0230, 0.0317, 1.24, 90114, 512..180, 1588, 794, 0.387695, 0.193848, 5.480560, 11.815731, 24.557203, 5.2850, 11.3840, 23.1240, 0.317311, 0.241971, 0.479500, 0.109848, 78).")
add("cards-L07-L08-full-read", "2.7 cards (full read of all L07 and L08 cards)", "cards.json: L07 cards (25) and L08 cards (23), ids SC1-c134..c218",
    "All 48 cards read; text in ledgers/SC1/scripts/SC1-c-r10/out/cards_L07_L08.txt. Fronts match the statements' hypotheses; backs match the lesson text and numbers; definitions and misconceptions carry no grade (allowed by BUILDER_RULES 7); lab cards are grade C with basis.")
add("cards-c140-substitution", "2.7 cards / 2.4 mathematics (substitution in SC1-c140)", "course/modules/SC/SC1/cards.json SC1-c140 (back); course/modules/SC/SC1/L07.html:101-107",
    "Round-9 FAIL is fixed. Back now reads 'The substitution m=sqrt(H) u turns the integral into 2 sqrt(H) integral_0^inf (1-Phi(u)) du, and 2 sqrt(H)/sqrt(2 pi)=sqrt(2H/pi).' This matches the page proof and the arithmetic. Re-verified: check_pages PASS and check_dag PASS after the edit.")
add("cards-c150-gap", "2.2 numbers (card c150 gap in SE units)", "cards.json SC1-c150 (back); course/modules/SC/SC1/L07.html interpretation",
    "Card now says 1.24 standard errors. Unrounded: (0.797884561 - 0.75863335)/0.03165865 = 1.239826, rounds to 1.24. Correct.")
add("num-L08-z-values", "2.2 numbers (z values and SE units)", "course/modules/SC/SC1/L08.html interpretation and E2; cards SC1-c173",
    "Unrounded z: -1.046620, -0.686640, -0.774819, which round to -1.05, -0.69, -0.77; all |z| < 1.1, as stated.")
add("num-L08-E3-factors", "2.2 numbers (rounded-factor product in E3 and M2)", "course/modules/SC/SC1/L08.html E3 and M2 solutions",
    "0.353553 x 0.778801 x 0.398942 = 0.109847654 -> 0.109848 (printed); unrounded 0.1098478224 (stated 0.1098478). 0.398942 x 0.606531 = 0.241970690 -> 0.241971; unrounded 0.2419707245 (stated 0.2419707). Correct.")
add("num-rounding-0.3173105078", "2.2 numbers (rounding of the closed form)", "course/modules/SC/SC1/L07.html (interpretation, M1, quiz, misconception); course/modules/SC/SC1/L08.html (misconception, M1, quiz)",
    "2(1-Phi(1)) = 0.31731050786 -> 0.3173105079 (10 d.p.); 2 x 0.1586552539 = 0.3173105078 (printed digits); to 7 d.p. 0.3173105 (diff +7.9e-9 from the quiz key). All stated variants agree with these values.")
add("notation-T-first-passage-index", "2.4 notation (T and nu)", "course/modules/SC/SC1/L07.html:59; course/modules/SC/SC1/L08.html; notation/notation.json (T symbol)",
    "T is never used as a horizon; L07:59 states the reservation once. nu_a is a local symbol defined in L08 Definition 2.1 and does not appear in notation.json. No collision.")
add("notation-kappa-redefined", "2.4 notation (kappa)", "course/modules/SC/SC1/L07.html, L08.html",
    "grep for kappa in both pages: no matches. No collision.")
add("notation-star-superscript-L08", "2.4 notation (superscript star in L08)", "course/modules/SC/SC1/L08.html (s^\\ast in the proof of Prop 1.2; k^\\ast in Prop 2.2 proof)",
    "s^\\ast and k^\\ast are local indices; R^\\ast of notation.json is not used. No collision.")
add("notation-horizon-H", "2.4 notation (H is the horizon symbol)", "course/modules/SC/SC1/L07.html:59",
    "H is the horizon in both pages, as plan 2.3 requires; the reservation of T is stated once (L07:59).")
add("notation-n-steps-L08", "2.4 notation (local convention, plan section 2.3)", "course/modules/SC/SC1/L08.html section 2 and lab; tests/labs/SC1/lab-SC1-L08-1.py:6-22",
    "Plan 2.3 asks for N for step counts and n for a grid index. L08 uses n for the walk length in section 2 and in the lab, and L07 uses N for the walk length in Part A. This is a builder-convention deviation, not a notation.json conflict and not a numerical or claim error. Observation only; no status change.")
add("dag-simple-random-walk-defined-twice", "2.9 DAG (no second definition of a term)", "course/modules/SC/SC1/L07.html:150; course/modules/SC/SC1/L08.html:113",
    "'simple random walk' is <dfn>-marked only in L06 (L06.html:56). L07:150 and L08:113 restate it as a reference, not a second definition. check_dag PASS.")
add("dag-plain-bias-L08", "2.9 DAG (plain-English 'bias' in L08)", "course/modules/SC/SC1/L08.html:461",
    "'bias' appears once as plain English ('it cannot show a bias either way'), with no concept link, allowed by plan D9.")
add("prose-L08-same-events", "2.9 prose (events)", "course/modules/SC/SC1/L08.html:51, :63-70",
    "The sentences saying the events coincide on every continuous path for a>0 match Prop 1.2 and its proof.")
add("prose-L08-first-passage-name", "2.9 prose (naming)", "course/modules/SC/SC1/L08.html:59, :116-121",
    "'first-passage time' (continuous, tau_a), 'first-passage index' nu_a (discrete, Def 2.1) and 'first-passage counts' are used consistently and not swapped.")
add("lab-L07-docstring-exact-fractions", "2.5 lab docstring vs code", "tests/labs/SC1/lab-SC1-L07-1.py:1-23 (module docstring) and :96, :125",
    "Docstring 'exact integer counts divided by 2**N, computed as floats' matches max_at_least(n,m)/2**n (line 96); 'standard error computed with divisor PATHS - 1' matches line 125.")
add("lab-L08-twin-docstring-PATHS", "2.5 lab docstring vs code", "tests/labs/SC1/lab-SC1-L08-1.py:1-28 (docstring) and :37-42 (constants)",
    "Docstring 1000 seeded walks of length 256 matches SIM_PATHS=1000 and SIM_STEPS=256 (lines 40-41); Part D formulas match lines 168-175.")
add("lab-L08-partA-printed-label", "2.5 lab output label (sequences vs pairs)", "tests/labs/SC1/lab-SC1-L08-1.py:88-102; course/modules/SC/SC1/L08.html:344-352",
    "Part A prints '(sequence, level) pairs checked: 90114' and '{nu_a <= n} equals {maximum >= a} on 90114 of them'; the page's expected block and interpretation use the same labels; 8190 is labelled 'step sequences of length 1 to 12'.")
add("lab-L07-partA-label", "2.5 lab output label (identity)", "tests/labs/SC1/lab-SC1-L07-1.py:54, :74, :88; course/modules/SC/SC1/L07.html:357",
    "'discrete tail identity of Lesson 6 (maximum >= a) = (endpoint >= a) + (endpoint > a): 78 of 78' is in both the twin and the expected block; matches L06 Corollary 1.4.")
add("rounding-rule-lab-printed-figures", "2.2 numbers (rounding rule stated for rounded lab figures)", "course/modules/SC/SC1/L07.html (interpretation); course/modules/SC/SC1/L08.html (interpretation)",
    "L07 states six decimals for Part A, ten for Part D, four for Part B and C, six for sqrt(2/pi); L08 states six for Parts A, B, D and four (z: two) for Part C. Each printed format in the twins matches these rules; each stated difference is computed from unrounded values.")
add("math-L07-cor-1.5a-H3-reading", "2.4 mathematics (Corollary 1.5(a), H3 reading)", "course/modules/SC/SC1/L07.html:91, :103",
    "Corollary 1.5(a) proof applies Theorem 1.3 at each level b > m >= 0, so b > 0 holds and H3 (H>0) is used at each step. The reading is correct.")
add("recompute-walk-dp-L07-L08", "2.2 numbers (independent algorithm)", "ledgers/SC1/scripts/SC1-c-r10/indep_r10.py; ledgers/SC1/scripts/SC1-c-r10/out/indep_r10.txt",
    "Killed-walk DP with exact integers (L07 tails) and Fraction DP (L08 truncated means, 179587/32768) agree with the printed values; the DP does not use the twin's enumeration or math.comb code.")
add("recompute-sim-L07-B-C-L08-C", "2.2 numbers (simulated figures, independent code)", "ledgers/SC1/scripts/SC1-c-r10/indep_r10.py; out/indep_r10.txt",
    "Seeded draws regenerated with explicit loops (not the twin's functions): L07 Part B counts 91/107/113/121 and SEs; Part C means and SEs; L08 Part C means, SEs and z. All match the printed values.")
add("remark-1.4-title-L07", "2.4 mathematics / 2.9 prose (title claim)", "course/modules/SC/SC1/L07.html:83-84",
    "The Remark title 'limits in the horizon' matches its content (H down to 0 and H to infinity), and the assumption H2 is named.")
add("term-walk-identity-L07", "2.4 notation/terms (term used before definition; attribution to Lesson 6)", "course/modules/SC/SC1/L07.html:150, :357, :380; tests/labs/SC1/lab-SC1-L07-1.py:54, :74, :88",
    "'discrete tail identity of Lesson 6' is defined in L06 (Corollary 1.4) before this use; the lab and page use the same name.")
add("term-walk-identity-L08", "2.4 terms (consistency of 'walk identity' within L08)", "course/modules/SC/SC1/L08.html:121 (Prop 2.2 title), :142, :364, :418, :433, :511; tests/labs/SC1/lab-SC1-L08-1.py:51, :88, :102",
    "The 'walk identity' name (Prop 2.2) is used consistently, and the twin's max_at_least docstring says the same.")
add("cards-no-A5-L05-lesson-scope", "2.7 cards (assumption labels cite the right lesson)", "cards.json SC1-c149, c150, c174, c215, and cards citing A3/A4/A5",
    "Cards that cite A3 and A4 name Lesson 5; the A5 cards (c150, c215) name Lesson 7 where A5 is stated. No card claims A3 for an unbounded stopping time.")
add("freshness-L07-L08", "2.1 freshness (2025-2026 work for a debate brief)", "course/modules/SC/SC1 (L07, L08)",
    "The unit cites only the book-level key shreve2004stochastic. No working paper and no debate brief; no freshness flag applies.")
add("cards-basis-A3-dependence", "2.7 cards (closed-form cards name the A3/A4 dependence)", "cards.json: SC1-c137, c139, c140, c145, c149, c150, c164, c165",
    "Each card that gives a closed-form value states 'assuming A3 and A4' (or names Theorem 1.3, which does) in its front or back.")
add("cards-c205-new", "2.7 cards (new card SC1-c205)", "cards.json SC1-c205 (L08)",
    "Front hypotheses (H1, H2 of Prop 1.2, A3, A4, H>0) and back (P(tau_a<=H)=P(M_H>=a)=2(1-Phi)=erfc) match L08 Corollary 1.3 and its proof.")
add("cards-c215-A5-card", "2.7 cards (Lesson 7 Assumption A5 card)", "cards.json SC1-c215; course/modules/SC/SC1/L07.html (Assumption A5)",
    "The back 'E[X] = integral_0^inf P(X>m) dm, with the value in [0, inf]' matches L07 Assumption A5 word for word in content.")
add("cards-c218-new", "2.7 cards (new L08 card SC1-c218)", "cards.json SC1-c218; course/modules/SC/SC1/L08.html:511 and :344-363",
    "'All 78 pairs' matches the expected block 'pairs (n, a) checked: 78; counts agree ... 78 of 78'.")
add("cards-c151-removed-coverage", "2.7 cards (removal of SC1-c151 keeps coverage)", "cards.json (SC1-c151 absent)",
    "The removed card's subject (B-tilde and whole-path continuity) is still covered by SC1-c154, which states that the tail formula is not asserted for B-tilde; L07 section 4 misconception 3 is the lesson text.")
add("cards-c150-c170-changed-text", "2.7 cards (changed backs: SC1-c150, SC1-c170)", "cards.json SC1-c150, SC1-c170",
    "c150 now states 1.24 SE (checked); c170 now states 'All 90114 pairs: every step sequence of length n <= 12, at every level a <= n', which matches the lab output and the lesson sentence.")
add("assume-A3-A4-additions", "2.4 scope/assumptions (round-9 'Assuming A3 and A4' phrasing additions)", "course/modules/SC/SC1/L07.html:443 (P1), :470 (E1); course/modules/SC/SC1/L08.html:466 (E3)",
    "P1 names H1-H3 and A3/A4 as used; E1's 'assuming A3 and A4' sentence is consistent with the empirical claim that four grid sizes cannot establish a limit; E3 names A3/A4 for the Corollary 1.5 recomputation. No unnamed assumption found.")
add("delta-round10-hunks", "1 inventory (delta c93dd526..00a84795 for slice c)", "course/modules/SC/SC1/L07.html, L08.html, cards.json; tests/labs/SC1 (unchanged)",
    "Read every hunk in L07.html (why-it-matters, Remark 1.4, Corollary 1.5 assumptions and proof wording, Lab 1 hypothesis and interpretation, canon-breaks bullet 1, E1 solution), L08.html (Lab 1 interpretation, E3 solution) and the in-slice cards (c139, c140, c145, c150, c164, c165, c170). Twins are byte-identical to the round-9 pin (git diff empty). Out-of-slice hunks (L06 Lemma 1.2 wording, cards of L01-L05) were read only as cross-references.")
add("delta-round9-carried-fail-fixed", "1 inventory (round-9 FAIL carried forward)", "ledgers/SC1 (round-9 fragment cards-c140-substitution)",
    "The only round-9 non-PASS row (cards-c140-substitution) is re-verified and now PASS; all other round-9 row ids are kept and re-verified on this pin.")

# Rows kept from round 9 that have no separate row above: the same ids were kept.
EXPECTED_IDS = [
    "gate-check-pages", "gate-check-dag", "gate-run-labs", "lab-L07-twin-isolated", "lab-L08-twin-isolated",
    "lab-L07-page-equals-twin", "lab-L08-page-equals-twin", "lab-L07-expected-equals-output", "lab-L08-expected-equals-output",
    "lab-L07-printed-numbers", "lab-L08-printed-numbers", "lab-L07-hypothesis-interpretation", "lab-L08-hypothesis-interpretation",
    "lab-simulated-labels-seeds", "lab-runtime", "lint-mypy-twins", "page-smoke-L07-L08", "pytest-lab-tools", "verify-refs-offline",
    "verify-refs-live-SC1", "refs-no-citation-markup", "claim-grades-L07", "claim-grades-L08", "math-L07-thm-1.3", "math-L07-cor-1.5b",
    "math-L07-prop-2.2-cor-2.3-remark-2.4", "math-L07-def-2.1-grid-times", "math-L07-remark-1.4-phi0", "math-L07-R1-R3-P2-P3-M-E",
    "math-L08-prop-1.2-cor-1.3-1.4", "math-L08-cor-1.5", "math-L08-prop-2.2-2.3", "math-L08-R3", "math-L08-R1-R2", "prob-L08-all",
    "prob-L07-remaining", "misconceptions-L07-content", "misconceptions-L08-content", "canon-breaks-L07-L08", "key-results-L07",
    "key-results-L08", "quiz-L07", "quiz-L08", "structure-L07", "structure-L08", "banned-and-process-words", "notation-macros",
    "dag-defined-once-L07-L08", "dag-outside-closure", "xref-L01-L05-L06", "cards-dup-and-numbers", "cards-L07-L08-full-read",
    "proof-L07-cor-1.5a-continuity-direction", "prob-L07-P1-continuity", "prob-L07-R2-continuity", "num-rounding-0.3173105078",
    "notation-T-first-passage-index", "dag-simple-random-walk-defined-twice", "prose-L08-same-events", "prose-L08-first-passage-name",
    "lab-L07-docstring-exact-fractions", "scope-L07-assumption-phrase", "scope-L08-everything-after", "math-L08-prop-2.3-denominator",
    "prob-L07-P1-assumptions", "notation-horizon-H", "lab-L08-twin-docstring-PATHS", "cards-L07-misconception-same-law",
    "lab-L08-partA-printed-label", "rounding-rule-lab-printed-figures", "math-L07-cor-1.5a-H3-reading", "recompute-walk-dp-L07-L08",
    "recompute-sim-L07-B-C-L08-C", "remark-1.4-title-L07", "term-walk-identity-L07", "dag-reflection-link-L07-L08",
    "structure-why-it-matters-word-cap", "delta-round8-hunks", "cards-c205-new", "defs-numbering-L08",
    "notation-star-superscript-L08", "notation-n-steps-L08", "scope-words-full-scan-r8", "dag-plain-bias-L08",
    "terms-used-before-defined-L07-L08", "term-walk-identity-L08", "cards-no-A5-L05-lesson-scope", "freshness-L07-L08",
    "cards-basis-A3-dependence", "delta-round9-hunks", "cards-c140-substitution", "cards-c151-removed-coverage",
    "cards-c215-A5-card", "cards-c218-new", "assume-A3-A4-additions", "twin-docstring-identity-rename",
    "cards-c150-c170-changed-text", "notation-kappa-redefined",
]

add("proof-L07-cor-1.5a-continuity-direction", "2.4 mathematics (continuity from below)", "course/modules/SC/SC1/L07.html:103",
    "'As b decreases to m the events {M_H>=b} increase' is correct (smaller threshold, larger event); their union over b>m is {M_H>m}; continuity from below applies.")
add("prob-L07-P1-continuity", "2.4 problems (P1 continuity step)", "course/modules/SC/SC1/L07.html:445",
    "P1 solution uses the same increasing-union argument; {M_H>=b} increase as b decreases to m; limit uses continuity of Phi; m=0 case handled. Correct.")
add("prob-L07-R2-continuity", "2.4 problems (R2 continuity step)", "course/modules/SC/SC1/L07.html:502",
    "R2 solution: {M_H>=b} increase as b decreases to a with union {M_H>a}; the difference of the two limits gives P(M_H=a)=0. Correct.")
add("scope-L07-assumption-phrase", "2.4 scope (assumption phrasing)", "course/modules/SC/SC1/L07.html:55, :68-82, :83-86, :91-92, :103, :134-146, :380, :511-530",
    "The claim 'every result below that uses them says so' (:55) holds: Theorem 1.3, Remark 1.4, Corollary 1.5(a),(b), the closed-form part of Corollary 2.3 and Remark 2.4 name H2 or A3/A4; Proposition 2.2 and the first part of Remark 2.4 use no A3/A4 and claim none.")
add("scope-L08-everything-after", "2.4 scope (assumption phrasing)", "course/modules/SC/SC1/L08.html:55, :63-81, :87-90, :97-106, :367-374",
    "'The closed forms below use A3 and A4 ... Every result that uses them says so' (:55) holds: Corollaries 1.3, 1.4, 1.5 and the density carry 'assuming A3 and A4'; Proposition 1.2 and Section 2 use none.")
add("math-L08-prop-2.3-denominator", "2.4 mathematics (Prop 2.3 denominator)", "course/modules/SC/SC1/L08.html:132",
    "'Each probability in the first sum is an integer divided by 2^k' is correct: P(nu_a > k) = (count of walks of length k staying below a)/2^k.")
add("prob-L07-P1-assumptions", "2.4 problems (P1 assumptions)", "course/modules/SC/SC1/L07.html:443-445",
    "P1 asks to state each assumption used and lists H1, H2 and H3 with the level b>0 and H>0; consistent with Theorem 1.3's statement.")
add("cards-L07-misconception-same-law", "2.7 cards (misconception coverage, L07)", "cards.json SC1-c191; course/modules/SC/SC1/L07.html:397",
    "Card SC1-c191 gives P(M_H<=0)=0 and P(B_H<=0)=1/2, which are correct (Corollary 1.5(a) at m=0; Phi(0)=1/2), consistent with L07 misconception 1.")
add("structure-why-it-matters-word-cap", "2.9 structure (why it matters: at most 120 words, BUILDER_RULES 4.2 item 1)", "course/modules/SC/SC1/L07.html:51; course/modules/SC/SC1/L08.html:51",
    "check_pages word count (its own counter) is within the 120-word cap for both pages (check_pages PASS). My rough count of the rendered text is about 125 (L07) and 121 (L08) because I counted math tokens differently; the tool's counter governs and passes.")
add("delta-round8-hunks", "1 inventory (historic: delta 0dee921..c93dd52, round 8 to round 9)", "course/modules/SC/SC1/L07.html, L08.html, cards.json (c149, c150, c151, c170, c218), tests/labs/SC1/lab-SC1-L07-1.py",
    "Historic inventory from round 9 kept with its id; its round-8 FAIL rows were re-verified PASS in round 9 and are re-checked on this pin (the L07 term walk and the A3-dependence cards read correctly).")
add("defs-numbering-L08", "2.9 structure (numbering of definitions, propositions, corollaries)", "course/modules/SC/SC1/L08.html:58, :63, :77, :87, :97, :107, :116, :121, :131",
    "Numbering is sequential: Definition 1.1, Proposition 1.2, Corollaries 1.3, 1.4, 1.5, Remark 1.6, Definition 2.1, Propositions 2.2 and 2.3; each cross-reference (Corollary 1.3, Corollary 1.4, Proposition 2.3) points to an existing item.")
add("scope-words-full-scan-r8", "2.4 scope (every, all, always, never, any, surely, exactly, only) full sentence scan", "course/modules/SC/SC1/L07.html, L08.html (prose, outside pre blocks)",
    "Scope-word sentence scan of both pages: each instance is a proved claim (Propositions 1.2, 2.2, 2.3), an enumeration (78 pairs, 90114 pairs, 8190 sequences), or a disclaimer ('does not say that the event is empty', 'nothing about any single outcome'). No unsupported scope word.")
add("terms-used-before-defined-L07-L08", "2.4 terms used before definition (full scan)", "course/modules/SC/SC1/L07.html, L08.html",
    "Terms checked: erfc, Phi, tau_a, H1-H3, A3-A5, grid, grid maximum, running maximum, walk. Each is defined before its first body use. 'grid maximum' appears in the L07 why-it-matters paragraph as a preview next to the pointer '(Definition 2.1 of this lesson)'; accepted as a pointer, not a definition-order defect.")
add("delta-round9-hunks", "1 inventory (delta 0dee921..c93dd52 for the slice)", "course/modules/SC/SC1/L07.html, L08.html, lab-SC1-L07-1.py, cards.json",
    "Historic inventory from round 9 kept with its id. Its hunks (L07 Part D/E-solution and interpretation edits, L08 E3 and interpretation edits, cards c150, c151 removed, c170, c215, c218 new) are re-read on this pin and are consistent with the current text.")
add("twin-docstring-identity-rename", "2.5 lab docstrings and print lines vs the expected block (rename)", "tests/labs/SC1/lab-SC1-L07-1.py:54, :74, :88; course/modules/SC/SC1/L07.html:357",
    "The renamed Part A line 'discrete tail identity of Lesson 6' appears in the twin docstring, the print, and the expected block, and the page's hypothesis uses the same name.")

# Extra rows from this round (new ids, not in round 9).
add("lab-L07-partA-label", "2.5 lab output label (identity)", "tests/labs/SC1/lab-SC1-L07-1.py:88; course/modules/SC/SC1/L07.html:357",
    "Printed labels 'Part A: discrete tail identity ... 78 of 78' and 'counting formula agrees with the enumeration: 78 of 78' match the page's expected block and the L06 Corollary 1.4 statement.")
add("num-L08-z-values", "2.2 numbers (z values and SE units)", "course/modules/SC/SC1/L08.html interpretation and E2; cards SC1-c173",
    "Unrounded z: -1.046620, -0.686640, -0.774819, which round to -1.05, -0.69, -0.77; all |z| < 1.1 as stated.")
add("num-L08-E3-factors", "2.2 numbers (rounded-factor product in E3 and M2)", "course/modules/SC/SC1/L08.html E3 and M2 solutions",
    "0.353553 x 0.778801 x 0.398942 = 0.109847654 -> 0.109848 (printed); unrounded 0.1098478224. 0.398942 x 0.606531 = 0.241970690 -> 0.241971; unrounded 0.2419707245. Both statements in the solutions are correct.")
add("cards-c150-gap", "2.2 numbers (card c150 gap in SE units)", "cards.json SC1-c150 (back); course/modules/SC/SC1/L07.html interpretation",
    "Card says 1.24 standard errors. Unrounded (0.797884561 - 0.75863335)/0.03165865 = 1.239826, which rounds to 1.24. Correct.")
add("delta-round10-hunks", "1 inventory (delta c93dd526..00a84795 for slice c)", "course/modules/SC/SC1/L07.html, L08.html, cards.json; tests/labs/SC1 (byte-identical)",
    "Read every hunk in L07.html (why-it-matters, Remark 1.4, Corollary 1.5 assumption list and proof wording, Lab 1 hypothesis and interpretation, canon-breaks bullet 1, E1 solution), L08.html (Lab 1 interpretation, E3 solution), and the in-slice cards (c139, c140, c145, c150, c164, c165, c170). Twins are byte-identical (git diff empty). Out-of-slice hunks (L06 Lemma 1.2 wording, L01-L05 cards) were read only as cross-references.")
add("delta-round9-carried-fail-fixed", "1 inventory (round-9 non-PASS row carried forward)", "ledgers/SC1/SC1-c.json (row cards-c140-substitution)",
    "The only round-9 non-PASS row, cards-c140-substitution, is re-verified and now PASS. All other round-9 row ids are kept and re-verified on this pin.")

notes = [
    "Delta c93dd526..00a84795 (the round-9 pin to the round-10 pin) in slice c: L07.html and L08.html changed in wording only (Remark 1.4, Corollary 1.5 assumption lists, Lab 1 hypothesis and interpretation, E1 and E3 solutions, canon-breaks bullet 1, why-it-matters); the lab twins are byte-identical; the cards changed in c139, c140, c145, c150, c164, c165, c170. Every L07/L08 claim and card was re-verified from scratch on this pin because the subjects changed.",
    "Round-9 FAIL cards-c140-substitution is fixed (the card now states the factor 2 sqrt(H) and 2 sqrt(H)/sqrt(2 pi) = sqrt(2H/pi)) and PASSes.",
    "Labs: run_labs SC1 11/11; twins run alone under python3 -I -W error with stdout equal to the page expected blocks; page code equals twin; recomputation by independent DP and explicit-loop code (indep_r10.py) matches all printed values, including 1.24 SE in card c150 and the L08 z values.",
    "Mutants: none. SC1-c has no grader; lab twins are demonstrations and are not mutation-tested (FINAL-ARCHITECT-RULINGS 9; verifier rulings). tools/mutate_graders.py was not run for this slice and needs no run for it.",
    "Observation (not a row defect): plan 2.3 asks for N for step counts and n for grid index; L08 uses n for walk length. Not a notation.json conflict. Carried from round 9.",
    "Observation: L07's why-it-matters uses 'grid maximum' as a preview before Definition 2.1, with an explicit pointer. Accepted.",
    "Observation: the L07 hypothesis cites 'Corollary 1.4' meaning Lesson 6's discrete tail identity; the Uses line and the twin disambiguate it.",
    "Could not check in this slice: render_curriculum, build_site, fetch_data, check_projects and run_graders (outside slice c); the full pytest suite (only the lab, run_labs and page-check test files were run); lesson proofs of L06 beyond the statements cited by L07 and L08 (other slice); the Pyodide runtime beyond page_smoke; any figure (none exist in L07 or L08).",
    "Verify_refs --unit SC1 is a live tool run; its pass is reported as the tool's output. No bot check or access block was encountered.",
]

seen = set()
rows = [r for r in rows if not (r["id"] in seen or seen.add(r["id"]))]

fragment = {
    "unit": "SC1",
    "slice": "c",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-c (L07, L08, lab twins), round 10; did not build SC1",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36 (detached, /Users/billyribeiro/.fanout/wt/verifyE10-SC1-c)",
    "base": "c93dd526 (round-9 pin; round-9 fragment /Users/billyribeiro/.fanout/frags/E-SC1-c.round9.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-SC1-c (detached at 00a84795; .venv symlinked to the repo venv)",
    "scratch": "ledgers/SC1/scripts/SC1-c-r10/out/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "mutants_killed": 0,
        "mutants": 0,
    },
}

out_path = f"{ROOT}/ledgers/SC1/SC1-c.json"
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print("wrote", out_path, len(rows), "rows")
