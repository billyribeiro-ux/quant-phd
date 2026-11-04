"""Builds ledgers/SC1/SC1-c.json (round 6) from the round-5 row list and the round-6 evidence below.

Every row id of round 5 is kept. Each row was re-verified in round 6 (no PASS row is carried), because
L07.html, L08.html and cards.json changed between the round-5 pin 7376a5e and the round-6 pin 4bd8cb9.
Run from the checkout root: python3 -I ledgers/SC1/scripts/SC1-c-r6/build_fragment_r6.py
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(".").resolve()
R5 = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-SC1-c.round5.json").read_text(encoding="utf-8"))
OUT = "ledgers/SC1/scripts/SC1-c-r6/out/"
RECOMP = "ledgers/SC1/scripts/SC1-c-r6/recompute_r6.py -> out/recompute_r6.out"
STRUCT = "ledgers/SC1/scripts/SC1-c-r6/structure_checks_r6.py -> out/structure_checks_r6.out"
TWIN = "ledgers/SC1/scripts/SC1-c-r6/twin_page_check_r6.py -> out/twin_page_check_r6.out"

P = "PASS"
E: dict[str, str] = {
    "gate-check-pages": f"Re-run at pin 4bd8cb9: check_pages.py --unit SC1 --page L07 -> 'check_pages SC1 L07: PASS' (exit 0); --page L08 -> PASS (exit 0). ({OUT}check_pages_L07_L08.out)",
    "gate-check-dag": f"Re-run check_dag.py --unit SC1 -> 'check_dag SC1: PASS', exit 0 ({OUT}check_dag.out). Defined-once and outside-closure reviewed separately in dag-* rows.",
    "gate-run-labs": f"Re-run run_labs.py --unit SC1 --page L07 -> 'run_labs SC1: PASS (1/1)', exit 0; --page L08 -> PASS (1/1), exit 0 ({OUT}run_labs_L07.out, run_labs_L08.out).",
    "lab-L07-twin-isolated": f"python3 -I -W error on tests/labs/SC1/lab-SC1-L07-1.py from /tmp: exit 0, empty stderr ({TWIN}).",
    "lab-L08-twin-isolated": f"python3 -I -W error on tests/labs/SC1/lab-SC1-L08-1.py from /tmp: exit 0, empty stderr ({TWIN}).",
    "lab-L07-page-equals-twin": f"HTML-unescaped <code data-run> of L07.html equals the twin text (trailing whitespace aside): True ({TWIN}).",
    "lab-L08-page-equals-twin": f"HTML-unescaped <code data-run> of L08.html equals the twin text: True ({TWIN}).",
    "lab-L07-expected-equals-output": f"Unescaped <pre class=expected> (23 lines) equals the twin stdout (23 lines) exactly: True ({TWIN}).",
    "lab-L08-expected-equals-output": f"Unescaped <pre class=expected> (20 lines) equals the twin stdout (20 lines) exactly: True ({TWIN}).",
    "lab-L07-printed-numbers": f"Independent recomputation (own code, no twin import): Part A tails 0.375000, 0.332306, 0.321084, 0.318255, 0.317547 (binomial sums, cross-checked by a Fraction DP for N=16, 64); identity 78 of 78; Part B counts 91, 107, 113, 121 and SE 0.0210, 0.0222, 0.0225, 0.0230 (sqrt(k(n-k)/(n^2(n-1)))); gaps -0.0898, -0.0498, -0.0348, -0.0148; Part D Simpson 0.158655253928 vs erfc 0.158655253931 ({RECOMP}). Part C/B simulated values reproduced exactly by the twin run, not re-derived with another RNG.",
    "lab-L08-printed-numbers": f"Recomputed: nu_3 counts 512,0,384,0,288,0,224,0,180,0 (sum 1588); S12>=3 count 794; 90114 pairs and 90114 agreements; E[min(nu_1,16/64/256)] = 5.480560303, 11.815731233, 24.557203397 by Fraction DP; Part D P(tau<=1)=0.3173105079, density 0.2419707245 (H=1), P(tau<=2)=0.4795001222, density 0.1098478224 (H=2); z from printed means -1.0469, -0.6866, -0.7748 ({RECOMP}).",
    "lab-L07-hypothesis-interpretation": "Hypothesis (L07.html line 150) states the Part A exact tails at N<=1024, the Part B 400-path grid estimates with the nesting prediction, Part C against sqrt(2/pi), Part D by erfc and Simpson: each matches the twin's code and printed output (twin lines 36-170). Interpretation (line 376) names only printed numbers; its rounding rule (added in this round) matches the printed digits.",
    "lab-L08-hypothesis-interpretation": "Hypothesis (L08.html line 142) states Parts A-D as the twin implements them (enumeration n<=12, first-passage counts n=12 a=3, exact truncated means N=16,64,256, 1000 seeded walks of 256 steps, Part D densities). Interpretation (line 364) names only printed values; rounding rule matches the printed digits.",
    "lab-simulated-labels-seeds": "L07 header 'Parts B and C SIMULATED' and L08 header 'Part C SIMULATED' match the code; SEED=20260507 (L07) and SEED=20260508 (L08) are the only RNG seeds (random.Random(SEED)); no network, no file reads (grep); Part A and D are exact or formula-only.",
    "lab-runtime": f"page_smoke (Pyodide): lab-SC1-L07-1 0.1 s, lab-SC1-L08-1 0.2 s ({OUT}page_smoke_L07_L08.out); both far below 10 s.",
    "lint-mypy-twins": f"ruff check and ruff format --check on both twins: 'All checks passed!' / '2 files already formatted'; mypy --no-incremental on both twins: 'Success: no issues found in 2 source files' ({OUT}ruff.out, mypy.out).",
    "page-smoke-L07-L08": f"page_smoke.py --unit SC1 --pages L07 L08 (with the figure sweep, Chromium, light and dark, 360 px and desktop): 'page_smoke modules/SC/SC1/L07.html: PASS', 'page_smoke modules/SC/SC1/L08.html: PASS', 'page_smoke SC1: PASS', exit 0 ({OUT}page_smoke_L07_L08.out).",
    "pytest-lab-tools": f"pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k 'SC1 or sc1 or lab' -q: all passed, exit 0 ({OUT}pytest_labs_r6.out).",
    "verify-refs-offline": f"verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 ({OUT}verify_refs_offline.out).",
    "verify-refs-live-SC1": f"verify_refs.py --unit SC1 (live): 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0 ({OUT}verify_refs_live_SC1.out). Entry shreve2004stochastic: Open Library book record, title and author match the citation string.",
    "refs-no-citation-markup": f"data-cite count is 0 in L07.html and L08.html (grep, {STRUCT}); both pages state they cite no passage from the registry; no key is cited.",
    "claim-grades-L07": "Re-graded against BLUEPRINT section 3: Theorem 1.3, Corollary 1.5(a)/(b) (A5 is a numbered Assumption, stated), Proposition 2.2, Corollary 2.3 and Remark 2.4 are proofs on the page (T); Lab 1 Part A/B/C results are C with the basis named; Remark 1.4 is unlabelled and proved on the page.",
    "claim-grades-L08": "Proposition 1.2, Corollaries 1.3-1.5, Proposition 2.2 and 2.3 are T and proved on the page (Corollary 1.3's closed form assumes A3/A4 through Lesson 7); Lab 1 Part A/B/C results C with basis; Part D formula evaluation not graded as a theorem.",
    "math-L07-thm-1.3": "Lines 67-80 re-read. Proof uses Theorem 2.5 of Lesson 6 (P(M_H>=a)=2P(B_H>=a) under A3, A4; checked against L06 lines 100-300), B_H ~ N(0,H) from L01 D2 with s=0 and B_0=0 (L01 D1), no atoms of the normal law. erfc identity: erfc(a/sqrt(2H)) = 2(1-Phi(a/sqrt H)); at a=1,H=1 both 0.3173105079 (recompute_r6.out).",
    "math-L07-cor-1.5b": f"Lines 101-107 re-derived by hand: integration by parts gives int_0^R(1-Phi)=R(1-Phi(R))+phi(0)-phi(R); bound 1-Phi(R)<=phi(R)/R; numerical int_0^40(1-Phi)=0.3989422804=1/sqrt(2pi); E[M_1]=2*int=0.7978845608=sqrt(2/pi) ({RECOMP}).",
    "math-L07-prop-2.2-cor-2.3-remark-2.4": "Re-verified. Line 123 (H2) now reads N>=1 and N'>=1, N divides N'; the proof's c=N'/N is then a positive integer (line 131). Definition 2.1 (line 116) requires N>=1, so the previously missing hypothesis is now stated. Corollary 2.3 (inclusion and bound) and Remark 2.4 (N=1: max(0,B_H), tail exactly half of the continuous tail) re-derived and correct.",
    "math-L07-def-2.1-grid-times": "Line 116: N an integer >=1, H>0, s_k=kH/N for k=0..N, M^(N)_H = max_{0<=k<=N} B_{s_k}; consistent with Proposition 2.2 (line 123+) and card SC1-c142.",
    "math-L07-remark-1.4-phi0": "Line 84: Phi(0)=1/2 by evenness; P(Z>=0)+P(Z<=0)=1+P(Z=0), P(Z=0)=0. Limits at a=1 recomputed this round: 2(1-Phi(1/sqrt H)) = 0.0 at H=1e-6 and 0.999202 at H=1e6 (tending to 1), consistent with Remark 1.4.",
    "math-L07-R1-R3-P2-P3-M-E": f"Problem solutions re-solved (lines 412-504): M1 erfc(2/sqrt8)=erfc(1/sqrt2)=0.3173105079; M2; M3 1-Phi(1)=0.1586552539 exactly half; P1 (H1-H3 applied per level b>0, m=0 by limit); P2 integration by parts; P3 now states N>=1 and N'>=1 (line 453), which is the fix; E1 0.2275*400=91, 0.3025*400=121; E2 14893+6885=21778, 21778/65536=0.332306; E3 sqrt(33759/63840000)=0.0229958 printed 0.0230; R1 a<0 gives 2(1-Phi(-1))=1.6827>1; R2 no atoms; R3 limit 0 ({RECOMP}).",
    "math-L08-prop-1.2-cor-1.3-1.4": "Lines 62-94: Proposition 1.2 both inclusions re-derived (IVT on the continuous path; closed set {s: B_s=a} contains its infimum tau_a); H2 a>0 and H>=0 used exactly where needed; Corollary 1.3 chain; Corollary 1.4 limit of 2(1-Phi(a/sqrt n)) to 1 (n integer, H>0). Counterexample for B_0 != 0 not needed: the statement is about paths of B, for which B_0=0 by L01 D1.",
    "math-L08-cor-1.5": f"Lines 96-104: F(H)=2(1-Phi(aH^{{-1/2}})), F'(H)=a H^{{-3/2}} e^{{-a^2/(2H)}}/sqrt(2pi) re-derived; FTC on (0,H]; F(0+)=0. Numerically the density matches the central difference of the distribution function to 4.7e-12 at a=1, H=1 and 2 ({RECOMP}).",
    "math-L08-prop-2.2-2.3": f"Lines 120-138: walk identity {{nu_a<=N}}={{max S_k>=a}} verified exhaustively for 90114 (sequence, level) pairs; Proposition 2.3 identity E[min(nu_1,N)] = sum_{{k<N}} P(nu_1>k) verified against an exact Fraction DP (P(nu_1>k)=C(k,floor(k/2))/2^k checked at k=10) ({RECOMP}).",
    "math-L08-prop-2.3-denominator": "Proposition 2.3 (page line ~121-130): each P(nu_a>k) is an integer divided by 2^k for k>=0 (count of sequences with running maximum below a); k=0 gives 1; checked by enumeration in recompute_r6.py.",
    "math-L08-R3": "Lines 489-495: d/dH log f_a = (a^2-3H)/(2H^2), positive below a^2/3, negative above; grid argmax of f_1 found at 0.3333 = a^2/3 ({RECOMP}).",
    "math-L08-R1-R2": "Lines 476-487: #{nu_a<=N} = 2#{S_N>=a} - #{S_N=a} re-derived; for N=12, a=3 the count 1588 = 2*794 with #{S_12=3}=0 (enumeration, recompute_r6.out). R2 increment 1{nu_a>N} re-derived by cases.",
    "prob-L08-all": f"Lines 400-496: M1 (0.317311, 0.3173105 erfc); M2 (f_1(1) = 0.2419707, unrounded 0.2419707245); M3 (5/8, enumeration of 3-step walk); P1-P3 proofs re-derived; E1 (odd-step counts 512, 384, 288, 224, 180 sum 1588) by enumeration; E2 (z = -1.05, -0.69, -0.77 from printed means); E3 (0.109848 recomputed); R1-R3 re-derived ({RECOMP}).",
    "prob-L07-remaining": "Problems M1-M3, P2, P3 (now stated with N>=1, N'>=1), E1-E3, R1-R3 re-solved in this round; each solution correct and each statement carries its hypotheses (lines 412-504).",
    "misconceptions-L07-content": "Lines 391-402: (1) same law as B_H refuted by factor 2 with printed values 0.3173 and 0.1587 (seven decimals 0.3173105, 0.1586553 recomputed); (2) grid tail above closed form refuted by Proposition 2.2(a); (3) normal one-time marginals refuted with L01 Section 4 B-tilde (verified in L01.html lines 212-216).",
    "misconceptions-L08-content": "Lines 379-389: (1) finite on every path refuted via Corollary 1.4 probability statement; (2) P(tau<=H)=P(B_H>=a) refuted by factor 2 (values 0.317311 and 0.1586552539 match the lab); (3) finiteness does not bound the mean, refuted by the H^{-3/2} tail (Remark 1.6, recomputed limit 0.99999950).",
    "canon-breaks-L07-L08": "L07 Section 3 (lines 379-386): continuity needed (L06 Lemma 2.1 (i)); closed form conditional on A3, A4 (L05 A3 is a sketch, not a proof; A4 standard facts without proof, L05 lines 59, 270-288); grid maximum a different variable (Remark 2.4). L08 Section 3 (lines 366-370): jump counterexample re-checked (M_1=2, path never equals 1, tau_1=infinity).",
    "key-results-L07": "Lines 517-525: six T rows and three C rows; each T row matches a theorem or proposition on the page (Theorem 1.3, Corollary 1.5(a), Corollary 1.5(b) under the named assumption A5, Proposition 2.2, Remark 2.4); each C row names the lab and basis (Part A exact enumeration; Part B/C one seed, 400 paths, SIMULATED).",
    "key-results-L08": "Lines 505-512: T rows match Proposition 1.2, Corollary 1.3, Corollary 1.4, Corollary 1.5, Proposition 2.2 and 2.3; C rows name Lab 1 Part A (90114 pairs; 78 pairs) and Part C (one seed, 1000 walks). Row 1 states the identity on every continuous path with a>0; B is a standard Brownian motion, so B_0=0 holds for its paths (L01 D1), and the proposition itself states B_0=0 (line 63-68).",
    "quiz-L07": "Lines 531-610: 10 items; the six multiple-choice keys are right (Theorem 2.5 factor 2; grid maximum at most running maximum; P(M_H<=0)=0; nested-grid reason; theorem for a>0 only; single-step grid max(0,B_H)); numeric keys within stated tolerance of the unrounded values (0.3173105 vs 0.31731050786; 0.158655 vs 0.15865525; 0.797885 vs 0.79788456; 0.3173105 for M_4).",
    "quiz-L08": f"Lines 518-597: 10 items; keys right (continuous paths with B_0=0; finite with probability one; the walk factor 2 by S_12 even; odd steps; jump example); numeric keys: 0.3173105 (unrounded 0.31731050786), 0.625 exact, 5.48056 (exact 5.4805603, |diff| 3e-7 < 1e-5), 0.241971 (unrounded 0.2419707245, |diff| 3e-7 < 1e-6) ({RECOMP}).",
    "structure-L07": f"12 problems (M1-M3, P1-P3, E1-E3, R1-R3) each with details.solution; 3 misconceptions; 10 quiz items with explain blocks; key-results and references sections; hours data-hours=9 (curriculum 100 = 72 + 28); why-it-matters 115 tokens (approximate, markup stripped) ({STRUCT}).",
    "structure-L08": f"12 problems each with details.solution; 3 misconceptions; 10 quiz items; key-results; references; data-hours=9; why-it-matters approx 118 tokens ({STRUCT}).",
    "banned-and-process-words": f"Grep of L07/L08 text for the BUILDER_RULES 1.3-1.4 phrases (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown) and process words (builder, verifier, fixer, ledger, REQUEST, round N): none ({STRUCT}).",
    "notation-macros": "Macros used on both pages: \\Prob, \\E, \\indic (registered in notation/notation.json macros); \\Phi (registered symbol: standard normal CDF); all other commands are KaTeX built-ins. No unregistered custom macro (structure_checks_r6.out).",
    "dag-defined-once-L07-L08": "check_dag PASS. Each concept defined once: def-running-maximum-distribution only in L07.html (line 64); def-first-passage-time only in L08.html (line 59). Plain <dfn> without data-concept for 'discretely monitored maximum' (L07 Def 2.1) is not a concept definition.",
    "dag-outside-closure": "check_dag PASS. SC1 prerequisite is M6 (curriculum.json entry SC1, prereqs [M6]). L07 links normal-distribution, random-variable and expectation to M4/M6 concepts, which lie in the closure; L08 links first-passage/brownian/running-maximum/reflection only from L01, L06, L07 (earlier in the unit).",
    "xref-L01-L05-L06": "Re-read: L06 writes the horizon as t (section 2 intro); L06 Lemma 2.1(i) = {M_t>=a}={tau_a<=t} under continuity; tau_a=inf{s>=0: B_s=a} (L06 section 2); Theorem 2.5 (2P(B_t>a)=2P(B_t>=a) under A3, A4); Corollary 2.6 (2P(B_t>a)=erfc(a/sqrt(2t)), erfc defined there); Corollary 1.4 (discrete tail identity); L01 Definition 1.1 (D1 B_0=0, D2 normal increments variance t-s); L01 section 4 B-tilde with discontinuous paths; L05 A3 (sketch, not a proof) and A4 (standard facts).",
    "cards-dup-and-numbers": f"194 cards: no duplicate ids and no duplicate fronts; all numbers in the 47 L07/L08 card backs appear in their lesson pages ({STRUCT}).",
    "proof-L07-cor-1.5a-continuity-direction": "Line 103: as b decreases to m the events {M_H>=b} increase; union over b>m is {M_H>m}; continuity from below; Theorem 1.3 at each b>0; limit 2(1-Phi(m/sqrt H)). Direction correct.",
    "prob-L07-P1-continuity": "Line 441 solution: continuity from below, Theorem 1.3 for b>0, Phi continuous; hypotheses H1-H3 stated.",
    "prob-L07-R2-continuity": "Line 498 solution: events {M_H>=b} increase as b down to a; union {M_H>a}; continuity gives P(M_H>a)=2(1-Phi(a/sqrt H)); subtraction gives 0.",
    "num-rounding-0.3173105078": "2*0.1586552539 = 0.3173105078 on printed digits (L07 lines 376, 393, 416; quiz explain); unrounded 2(1-Phi(1))=0.31731050786 (recompute_r6.out). Every use states which is which.",
    "notation-T-first-passage-index": "L08 uses nu_a for the walk's first-passage index and tau_a for the Brownian time; T is not used as an index on L07/L08 (grep). Registry: T = number of return observations (module S1); L07 Definition 1.1 says so.",
    "dag-simple-random-walk-defined-twice": "'Simple random walk' is defined only in L06 section 1; L07 lab hypothesis (line 150) and L08 section 2 (intro) use it in plain words with a pointer to Lesson 6; no second dfn.",
    "prose-L08-same-events": "Proposition 1.2 hypotheses H1 (continuous, B_0=0) and H2 (a>0, H>=0) (line 63-68); proof (line 74-79) uses both; why-it-matters and Section 1 refer to paths of the standard Brownian motion B, for which B_0=0 by L01 D1; no claim for paths with B_0 != 0 is made.",
    "prose-L08-first-passage-name": "Definition 1.1 (first-passage time, dfn at line 59) and Definition 2.1 (first-passage index of the walk, line 116) use the name consistently; the two objects are distinguished by tau_a and nu_a.",
    "lab-L07-docstring-exact-fractions": "Twin docstring (lines 1-20) says exact integer counts divided by 2**N, printed as floats to six decimals; code uses max_at_least(n,m)/2**n and prints with :.6f; output consistent.",
    "scope-L07-assumption-phrase": "Lines 55, 67-75, 92, 135, 145, 518-522: each closed-form use names A3/A4 or H2; 'every result below that uses them says so' (line 55) holds on re-read; Lab 1 interpretation disclaims A3/A4 and any all-paths or almost-sure statement.",
    "scope-L08-everything-after": "Lines 55, 78, 88, 98, 371: Corollaries 1.3-1.5 name A3/A4; Section 2 does not; Corollary 1.4 is a probability statement (line 88-95 proof says so); canon-breaks line 371 repeats it.",
    "notation-kappa-redefined": "No \\kappa on L07 or L08 (grep); kappa is a Lesson 6 symbol only (L06 section 1).",
    "math-L08-prop-2.3-denominator": "Proposition 2.3 statement: each probability in the sum is an integer divided by 2^k; holds for k>=0 (k=0: 1/1). Verified by enumeration in recompute_r6.py.",
    "prob-L07-P1-assumptions": "Line 441: P1 solution lists H1, H2, H3 and fixed H>0; m=0 by the same limit with H3 at each b>0.",
    "cards-L07-L08-full-read": "All 47 L07/L08 cards read in full (L07 c134-c159 and c191; L08 c161-c183 and c201). Checked against current lesson text: c144 now states N>=1 and N'>=1 (fixed); c147 and c192 removed; c201 added. Overlap noted, not a duplicate: c166 and c172 both state that the truncated means are not E[tau_a]; their fronts test different facts. Some definition/misconception cards carry no grade; BUILDER_RULES 7 requires a grade only for graded results.",
    "cards-basis-A3-dependence": "Cards with a closed form name A3/A4 in front or basis: c137-c140, c145, c153, c155, c157, c164, c165, c174, c183, c191, c201 (A5 for c140). c162 (event identity) names no assumption, correctly. c192 (the old basis card) is removed.",
    "notation-horizon-H": "H is the horizon throughout L07/L08 (Definition 1.1 of L07, line 59), consistent with the architect decision that H is the horizon symbol.",
    "lab-L08-twin-docstring-PATHS": "Twin docstring (lines 1-17) names SIM_PATHS seeded walks of length SIM_STEPS; constants SIM_PATHS=1000, SIM_STEPS=256 (twin lines 38-42) match the page text.",
    "cards-L07-misconception-same-law": "Card c191 back: P(M_H<=0)=2Phi(0)-1=0 by Corollary 1.5(a) with m=0; P(B_H<=0)=Phi(0)=1/2 by Remark 1.4; consistent with L07 Q5 explanation and the misconception text.",
    "lab-L08-partA-printed-label": "Twin Part A prints 'P(nu_3 <= 12) = 1588 / 4096 = 0.387695' and 'P(S_12 >= 3) = 794 / 4096 = 0.193848' (twin Part A lines); the page expected block contains the same lines (exact compare, TWIN check).",
    "rounding-rule-lab-printed-figures": "FIXED since round 5. L07 interpretation (line 376) states its rounding rule (Part A 6 dp; Part D 10 dp; Part B proportions, SEs and closed form 4 dp, each proportion a multiple of 1/400; Part C means and SEs 4 dp and sqrt(2/pi) 6 dp; each difference from unrounded values). L08 interpretation (line 364) states its rule (Part A, B, D 6 dp; Part C means and SEs 4 dp, z 2 dp). Every printed figure of both labs checked against the rule.",
    "math-L07-cor-1.5a-H3-reading": "Lines 91, 103: H3 (a>0, H>0 fixed) is used for each b>0 in the limit; m=0 handled by the b down to 0 limit, giving P(M_H>0)=1.",
    "recompute-walk-dp-L07-L08": f"{RECOMP}: Fraction DP over (position, running maximum) equals the binomial count for N=16 and N=64 (exact equality True); L08 DP for truncated means matches printed values to 6 dp.",
    "recompute-sim-L07-B-C-L08-C": f"Simulated values are reproduced exactly by running the twins (TWIN check); z-values and SEs recomputed from the printed means and exact values (L08: -1.0469, -0.6866, -0.7748 -> -1.05, -0.69, -0.77). The seeded RNG draws were not re-derived with a different generator (that would produce different numbers by construction).",
}
NEW = {
    "remark-1.4-title-L07": (
        "FAIL",
        "course/modules/SC/SC1/L07.html line 83: 'Remark 1.4 (limits in the horizon and the level)'. The remark (lines 84) takes a>0 fixed and computes only the limits as H down to 0 and H up to infinity; no limit in the level a is stated or derived.",
        "Change the title on line 83 to '(limits in the horizon)'. Content is correct; only the title overclaims.",
    ),
}
NOTES = [
    "Slice SC1-c: course/modules/SC/SC1/L07.html (627 lines), L08.html (614 lines), tests/labs/SC1/lab-SC1-L07-1.py and lab-SC1-L08-1.py (202 and 201 lines), and all 47 L07/L08 cards of cards.json. Every line of both pages and both twins was read in round 6; every L07/L08 card was read.",
    "Delta since the round-5 pin 7376a5e: L07.html (hunks at lines 52, 59, 123, 150, 376, 393, 453), L08.html (hunks at lines 84, 104, 364), cards.json (L07/L08 cards: c136 and c144 fronts, c147 and c192 removed, c162 front and c201 back changed; L01-L02 cards edited in other slices, out of scope), and the L02 twin (outside this slice). The L07 and L08 twins are byte-identical to 7376a5e. No PASS row is carried from round 5: every row was re-verified in round 6 because L07.html and L08.html changed.",
    "Round-5 FAIL rows, all fixed and re-verified PASS: math-L07-prop-2.2-cor-2.3-remark-2.4 (N'>=1 now in H2 line 123, card c144, Problem P3 line 453), math-L07-R1-R3-P2-P3-M-E (P3 fixed), rounding-rule-lab-printed-figures (rounding rules in L07 line 376 and L08 line 364).",
    "New FAIL this round: remark-1.4-title-L07 (title overclaims a level limit). Low severity; one-word fix.",
    "Observations, not failures: (a) card c174 and c173 and c149 bundle several printed values from one lab part into one card; accepted as one lab result, not split. (b) Definition 1.2 (line 63-66) says 'Section 1 computes this function in closed form' without restating A3/A4 in that sentence; the closed form is conditional and Theorem 1.3 states the assumption, so this is a pointer, not a claim. (c) Card c166 and c172 both state that the truncated means are not E[tau_a]; their fronts test different facts. (d) Proposition 2.2 title names only part (a); not an overclaim.",
    "Mutants: none listed. A lesson-page slice has no grader; lab twins are demonstrations, not mutation-tested (architect ruling 9; plan section 2.1 item 11). Verified by the twin-versus-page exact check and by reproduction of every printed number.",
    "Not checked in this slice: index.html; L01-L06 content except the lines cited for cross-references; project.html, grader, cards of other lessons; render_curriculum.py, build_site.py --check, fetch_data.py --check (data is not used by SC1 labs); full-repository pytest and full ruff/mypy (ran on the two twins and the relevant pytest subsets only); verify_refs live over the whole registry (only the SC1 entry, 1 of 560, was re-verified live); the seeded simulation values were not re-derived with an independent RNG; no figures on these pages, so the figure sweep applies only through page_smoke's own sweep, which passed.",
    "Plan deviation noted, not failed: the L08 Part B/C truncated mean is the simple-random-walk E[min(nu_1,N)] (exact) and its simulation uses the same walk; the page labels it as a walk quantity (Remark 1.6, card c172), so scope is correct.",
    "Card-level grade is absent on some definition and misconception cards; BUILDER_RULES section 7 requires a grade only for graded results, so this is not a failure.",
]

rows = []
for r in R5["rows"]:
    rid = r["id"]
    if rid in E:
        status, evidence, fix = P, E[rid], None
    else:
        raise SystemExit(f"no round-6 evidence for {rid}")
    row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence}
    rows.append(row)

# evidence overrides for rows whose round-5 status was FAIL and is now PASS (already set above as PASS)
# new rows
for rid, (status, evidence, fix) in NEW.items():
    rows.append({"id": rid, "check": "2.4 mathematics / 2.9 prose (title claim)", "location": "course/modules/SC/SC1/L07.html line 83",
                 "status": status, "evidence": evidence, "fix": fix})

counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
fragment = {
    "unit": "SC1",
    "slice": "c",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-c (L07, L08, lab twins), round 6; did not build SC1",
    "pin": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07",
    "base": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f (round-5 pin; round-5 fragment /Users/billyribeiro/.fanout/frags/E-SC1-c.round5.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE6-SC1-c (detached at 4bd8cb9; .venv symlinked; vendor copied)",
    "scratch": "ledgers/SC1/scripts/SC1-c-r6/out/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": f"SC1-c round 6: {len(rows)} rows: PASS {counts['PASS']}, FAIL {counts['FAIL']}, UNVERIFIABLE {counts['UNVERIFIABLE']}. The three round-5 FAIL rows are fixed and re-verified PASS. One new FAIL: remark-1.4-title-L07 (title overclaims a level limit).",
}
out = ROOT / "ledgers/SC1/SC1-c.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), counts, verdict)
print("written", out)
