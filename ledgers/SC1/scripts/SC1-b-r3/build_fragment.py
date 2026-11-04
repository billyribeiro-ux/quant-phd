"""Writes the round-3 verifier fragment for SC1 slice b from the round-2 row ids and this round's evidence.

Run from the checkout root: python3 -I -W error ledgers/SC1/scripts/SC1-b-r3/build_fragment.py
Evidence strings cite the scripts and output files under ledgers/SC1/scripts/SC1-b-r3/ and the page locators.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PREV = Path("/Users/billyribeiro/.fanout/frags/E-SC1-b.round2.json")
OUT = ROOT / "ledgers/SC1/SC1-b.json"
OUTS = "ledgers/SC1/scripts/SC1-b-r3/out"

EVIDENCE: dict[str, tuple[str, str]] = {
    "b-check-pages": (
        "PASS",
        f"tools/check_pages.py --unit SC1 on 67a2d13e: 'check_pages SC1: PASS', exit 0 ({OUTS}/check_pages.txt). "
        "Hand count: misconceptions 3/3/3; problem tiers 3 each on L04, L05, L06; quiz items 11/10/10; data-hours 9 each.",
    ),
    "b-check-dag": (
        "PASS",
        f"tools/check_dag.py --unit SC1: 'check_dag SC1: PASS', exit 0 ({OUTS}/check_dag.txt). Linked concepts on L04:37, "
        "L05:38, L06:38 all have anchors in course/concepts.html. Each data-concept dfn appears once: "
        "continuous-time-martingale (L04:75), markov-property (L05:75), reflection-principle (L06:119).",
    ),
    "b-run-labs": (
        "PASS",
        f"tools/run_labs.py --unit SC1 --page L04, --page L05, --page L06: each 'run_labs SC1: PASS (1/1)', exit 0 "
        f"({OUTS}/run_labs_L04.txt, run_labs_L05.txt, run_labs_L06.txt).",
    ),
    "b-twin-match": (
        "PASS",
        "ledgers/SC1/scripts/SC1-b-r3/twin_match.py run as python -I -W error: for L04, L05, L06 code_equals_twin=True, "
        f"exit 0, stderr empty, expected_equals_output=True; 'ALL MATCH' ({OUTS}/twin_match.txt).",
    ),
    "b-lab-lint": (
        "PASS",
        "ruff check on the three twins: 'All checks passed!'; ruff format --check: '3 files already formatted'; "
        f"mypy --no-incremental (pyproject strict = true) on the three twins: 'Success: no issues found in 3 source files' "
        f"({OUTS}/ruff_check.txt, ruff_format.txt, mypy.txt).",
    ),
    "b-page-smoke": (
        "PASS",
        "tools/page_smoke.py --unit SC1 --pages L04 L05 L06, run alone: each page 'PASS', 'page_smoke SC1: PASS', exit 0; "
        f"lab runtimes 0.1 s, 1.3 s, 0.0 s ({OUTS}/page_smoke.txt).",
    ),
    "b-pytest-tooling": (
        "PASS",
        "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py: exit 0, 100% dots, no failures "
        f"({OUTS}/pytest.txt).",
    ),
    "b-verify-refs": (
        "PASS",
        "tools/verify_refs.py --unit SC1 (live, plain HTTP): 'live re-verification of SC1: 1 of 560 entries, 0 problems', "
        f"exit 0 ({OUTS}/verify_refs_unit_live.txt). The unit's only key is shreve2004stochastic, cited at book level.",
    ),
    "b-attribution-references": (
        "PASS",
        "grep of L04, L05, L06 for karatzas, shreve, billingsley, williams, data-cite, data-locator: the only hits are the "
        "shreve2004stochastic key in each References section (L04:468, L05:513, L06:536), each stating no locator and no "
        "claim attributed to it. No data-cite or data-locator attribute appears on any of the three pages.",
    ),
    "b-cross-L04": (
        "PASS",
        "L04:37 links and L04:65 Assumption 4.1 sketch cite checked against L01.html:58-66 (def-brownian-motion, (D1)-(D3)), "
        "L03.html:70 (Assumption 3.2(a), functions of independent variables), L03.html:89 (Lemma 2.2, E[X^4]=3 Delta^2), "
        "L03.html:109 (mean of Q equals t), L03 id def-quadratic-variation, and the M6 Lesson 8 title "
        "'Filtrations and discrete-time martingales' (course/modules/M/M6/L08.html h1, cited in the L04:232 canon bullet).",
    ),
    "b-cross-L05-L06": (
        "PASS",
        "L05:56 (D1)-(D3) vs L01.html:61-63; M3 at L05:332 cites A1(c), matching L01.html:76; L05:285 and L06:304 "
        "discontinuous B-tilde vs L01.html:211-216 (Section 4); L02.html:274-288 Theorem 2.5 (H2: Assuming A2, on [0,1]) and "
        "Remark 2.6 vs L06:102; L08.html Corollary 1.4 (finite a.s.) and Corollary 1.5 (density) vs L05:286 and L06:102, 305; "
        "M6 L09.html:58-60 stopping time {tau<=k} in F_k vs L05:266 ('the definition of M6's stopping time').",
    ),
    "b-num-L04": (
        "PASS",
        f"ledgers/SC1/scripts/SC1-b-r3/recompute_numbers.py section 2 ({OUTS}/recompute_numbers.txt): e^(1/4)=1.284025416688 "
        "(L04:314 and printed 1.284025417); e^1=2.718281828459 (L04:420); e^4=54.598150033144 (L04:224, L04:452); "
        "e^8=2980.957987041728, so 2980.957987 to six decimals (L04:321, L04:328). Lab output equals the expected block (twin_match).",
    ),
    "b-num-L05": (
        "PASS",
        f"recompute_numbers.py section 1 at 60 digits ({OUTS}/recompute_numbers.txt): 225 cases; largest |Simpson - exact| "
        "3.811e-29 at (2,2,1,1), equal to the largest tail mass for 12<=|z|<=40 (3.811e-29); integrals 1.000000000000000. "
        "Section 2: 5.55e-16/3.81e-29 = 1.4567e13 (E1 'about 1.5e13' at L05:366); 5.55e-16/eps = 2.499 (L05:261 'about 2.5'); "
        "3.05e-16/eps = 1.374 (E3 'about 1.4' at L05:380); Phi(-1/sqrt2) = 0.2397500611 (quiz 0.23975); (2 pi)^(-1/2) = 0.3989422804 (quiz 0.3989).",
    ),
    "b-num-L06": (
        "PASS",
        f"recompute_numbers.py section 3 ({OUTS}/recompute_numbers.txt), binomial law: #{{M_12>=3}}=1588 of 4096; #{{S_12=4}}=495; "
        "P(M_10>=2)=281/512; 2P(S_10>2)=11/32; P(S_10=2)=105/512; 78 (N,a) pairs; 1014 triples. Section 2: erfc(1/sqrt2)/2 = 0.158655253931 "
        "(unrounded half cited at L06:400); P(B_1>=1)=0.1587 at L06:316 and the quiz.",
    ),
    "b-math-degenerate-L04-lemma-2.1": (
        "PASS",
        "Round-2 FAIL closed. L04:140 now reads 'Let 0 <= s < t, Y = B_t - B_s and h = t - s > 0' and treats s = t separately "
        "(Z_t is F_t-measurable), so Lemma 2.1 (h > 0, L04:82) is applied only with h > 0 in the proof of Proposition 2.4.",
    ),
    "b-math-L04-lemma-2.1": (
        "PASS",
        "Re-derived by hand from L04:87-89: theta*y - y^2/(2h) = theta^2 h/2 - (y - theta h)^2/(2h) is an identity; the shifted "
        "density integrates to 1. Hypothesis h>0 stated at L04:82.",
    ),
    "b-math-L04-prop-2.2": (
        "PASS",
        "Re-derived L04:101-106: E[B_t^2]=t by (D2); B_t=B_s+Y with Y independent of F_s (Assumption 4.1); pull-out (4.2(c)) "
        "with B_s F_s-measurable; E[Y|F_s]=E[Y]=0 by 4.2(d). Each use matches the hypotheses.",
    ),
    "b-math-L04-prop-2.3": (
        "PASS",
        "Re-derived L04:117-124: E[B_t^4]=3t^2 (L03 Lemma 2.2); E[(B_t^2-t)^2]=3t^2-2t^2+t^2=2t^2; B_t^2=B_s^2+2B_sY+Y^2 with "
        "E[Y|F_s]=0, E[Y^2|F_s]=E[Y^2]=h gives E[B_t^2-t|F_s]=B_s^2-s.",
    ),
    "b-math-L04-prop-2.4": (
        "PASS",
        "Re-derived L04:137-143: E[e^{2 theta B_t}]=e^{2 theta^2 t} by Lemma 2.1 with 2 theta; E[Z_t^2]=e^{theta^2 t}; "
        "Z_t=Z_s W with W=exp(theta Y - theta^2 h/2) (checked algebraically); E[W^2]=e^{theta^2 h}; E[W]=1 by Lemma 2.1 with h>0. "
        "The case 0<=s<t is proved (L04:140) and s=t is handled separately; the round-2 degenerate-h gap is closed.",
    ),
    "b-math-L04-A4.1-sketch": (
        "PASS",
        "L04:65 is labelled 'Sketch, not a proof' and names both skipped steps (pi-system of cylinder sets; pi-lambda extension). "
        "Its cited L03 Assumption 3.2(a) (L03.html:70) is the single-variable grouping statement the sketch says it covers.",
    ),
    "b-math-L04-misconception-1": (
        "PASS",
        "Re-derived L04:240: (B_s+Y)^3 = B_s^3+3B_s^2 Y+3B_s Y^2+Y^3; conditional mean B_s^3+3(t-s)B_s, which differs from "
        "B_s^3 for s<t exactly when B_s is nonzero.",
    ),
    "b-math-L04-R1-R3": (
        "PASS",
        "Re-derived solutions L04:339 (h(t)=t-g(t) must be constant, so g(t)=t+c), L04:346 (e^{c^2 h/2}=1 forces c=0 for h>0), "
        "L04:353 (conditional variance t-s, constant). Each step follows from the cited results.",
    ),
    "b-prose-L04-R2-title": (
        "PASS",
        "L04:343 title 'R2 · When the exponential exp(cB_t) is a martingale' matches its solution at L04:346.",
    ),
    "b-prose-L04-remark-numbering": (
        "PASS",
        "L04:126 is an unnumbered 'Remark (the link with Lesson 3)', and the L04:37 uses cite it correctly as 'the remark after Proposition 2.3'.",
    ),
    "b-scope-L04-footer": (
        "PASS",
        "L04:479 footer: Propositions 2.2 to 2.4 proved from Assumptions 4.1 and 4.2, stated and not proved here; Lab 1 labelled "
        "numerical. Matches L04:55-70 and L04:145-147.",
    ),
    "b-lab-L04-hypothesis": (
        "PASS",
        "L04:147 predictions (relative 1e-9 for the integral of e^{theta sqrt(t) z} against phi equal to e^{theta^2 t/2}; absolute "
        "1e-9 for E[Z_t]=1) match the twin's TOL checks (tests/labs/SC1/lab-SC1-L04-1.py) and the expected block (twin_match).",
    ),
    "b-lab-L04-interpretation": (
        "PASS",
        "L04:224 values 2.718281828, 1.284025417, 54.598150033 are e^1, e^{1/4}, e^4 (recompute_numbers.py section 2), and "
        "E[Z_t] prints 1.000000000, as in the expected block.",
    ),
    "b-lab-L04-docstring": (
        "PASS",
        "Twin docstring (lines 1-14) and page L04:150-161: numerical, no randomness, no file read, three theta at t=2, 'the lab "
        "does not compute the mass beyond LIMIT'. Matches the code (LIMIT=12.0, PANELS=20000, no RNG).",
    ),
    "b-math-L05-lemma-1.3": (
        "PASS",
        "L05:99-100 now argue s=t (B_t-B_s=0 is a constant, independent of every sigma-field), s=0 (F_0 generated by the "
        "constant B_0=0), and 0<s<t: (D3) applied to 0=r_0<...<r_k=s<t, A4(f) grouping, then extension from the pi-system P "
        "with A4(a). I checked that the r_j are admissible in (D3), that P is a pi-system, and that enlarging a time set with "
        "C=R does not change an event. The round-2 s=t gap is closed.",
    ),
    "b-math-L05-thm-1.4": (
        "PASS",
        "L05:110-121 for 0<=s<t: psi(x)=int g(y)p_{t-s}(x,y)dy; A4(b) with Z=B_s, Y=B_t-B_s, f(z,y)=g(z+y); the substitution "
        "y=z+w gives phi_u(y-z)=p_u(z,y) (L05:120). The s=t case is a separate row (b-math-L05-def-1.1-st-case).",
    ),
    "b-math-L05-lemma-2.2-thm-2.1": (
        "PASS",
        "Re-derived Lemma 2.2 (L05:140: multiply by uv, compare z-coefficients, constant terms reduce to uv(y-x)^2) and "
        "Theorem 2.1 (L05:154-163: (2 pi)^{-1}(uv)^{-1/2}(2 pi uv/(u+v))^{1/2} = (2 pi (u+v))^{-1/2}, exponent unchanged).",
    ),
    "b-math-L05-A3-sketch": (
        "PASS",
        "L05:279 sketch: rho_n = ceil(2^n rho)/2^n with bounds from R3; the fixed-time case from the argument of Lemma 1.3 applied "
        "to finitely many increments; the two skipped steps are named: (i) extension to the whole shifted path via A4(a) on the "
        "pi-system, (ii) passage to the limit; the sketch is labelled 'Sketch, not a proof'. Round-2 fix applied.",
    ),
    "b-math-L05-R3": (
        "PASS",
        "L05:404: x <= ceil(x) < x+1 gives rho <= rho_n < rho+2^{-n}; {rho_n <= r} = {rho <= floor(2^n r)/2^n} lies in F_r.",
    ),
    "b-math-L05-problems": (
        "PASS",
        "Re-derived M1 (1/(2 sqrt pi) and p_2(0,0)), M2 (psi(x)=x^2+2 and x^3+6x for Z~N(0,2)), M3 (Cov=0, A1(c) of L01), P1 "
        "(Lemma 2.2 at u=1,v=3,x=0,y=1: both sides (4z^2-2z+1)/3), P2 (Phi((c-x)/sqrt(t-s))), P3; E1-E3 values match "
        "recompute_numbers.py; R1 counterexample paths checked (sigma*=1/4 vs 3/4); R2 (F_rho=F_s); R3 ceiling inequality.",
    ),
    "b-math-L05-misconceptions": (
        "PASS",
        "L05:296-304 checked: conditional law N(B_s,t-s) by P2; p_{t-s}(x,.) and p_t(0,.) coincide iff x=0 and s=0; the 225-case "
        "misconception matches the lab output (recompute_numbers.py section 1).",
    ),
    "b-scope-L05-D1D3": (
        "PASS",
        "L05:56 lists the dependencies of Sections 1-2 as (D1)-(D3), A4(a), A4(b), A4(e), A4(f). The proofs use exactly these: "
        "Lemma 1.3 uses D1, D3, A4(a), A4(f); Theorem 1.4 uses D2, A4(b); Theorem 2.1 uses A4(e).",
    ),
    "b-notation-L05-Phi-varphi": (
        "PASS",
        "Phi appears only as the standard normal CDF (L05:349 P2; quiz L05:495-497), the registered meaning in "
        "notation/notation.json symbols; phi_u is the Gaussian density (L05:120). No conflicting use.",
    ),
    "b-notation-L05-X-n": (
        "PASS",
        "X_r and X^{(n)} (L05:274, L05:279) are local symbols; no registered macro or symbol uses X. Defined at first use.",
    ),
    "b-notation-M-clash": (
        "PASS",
        "M_N (walk, L06:56) and M_t (Brownian, L06:52, L06:107) are the running maximum of two processes; no registered symbol "
        "M exists; the martingale is Z_t (L04:75-147), so no clash. Symbol scan of L04-L06 against notation/notation.json: "
        "no T used for a horizon, no R^ast, Q or gamma.",
    ),
    "b-quiz-L05-Q7": (
        "PASS",
        "L05:477-483: the correct option names the extension of independence and the limit passage, which are the two steps "
        "the sketch skips (L05:279); the explanation is accurate.",
    ),
    "b-scope-L05-canonical": (
        "PASS",
        "L05:389 (R1 solution): the path space is chosen for this problem only, and A4(d) is applied correctly.",
    ),
    "b-term-almost-surely": (
        "PASS",
        "'almost surely' is first used at L05:62 (A4(b)), where it is defined as 'that is, with probability one'; later uses "
        "(L05:75, L06:144) are consistent.",
    ),
    "b-scope-L05-E1-tail": (
        "PASS",
        "L05:366 now restricts the comparison to 12<=|z|<=40 and says the mass for |z|>40 is not computed. Recompute: the 60-digit "
        "Simpson error (3.8e-29) equals the computed tail mass, so the printed comparison is right as stated.",
    ),
    "b-lab-L05-docstring-quadrature": (
        "PASS",
        "Twin docstring (tests/labs/SC1/lab-SC1-L05-1.py:7-8) now says 'The gaps are at the scale of double-precision rounding, "
        "not exact values'; page code equals the twin (twin_match). 60-digit recompute: Simpson error 3.8e-29, far below the "
        "gaps 5.55e-16. Card SC1-c091 back now reads 'double-precision rounding error'.",
    ),
    "b-lab-L05-hypothesis-interpretation": (
        "PASS",
        "L05:168 hypothesis (225 cases; s,t in {0.5,1,2}; x,y in {-1,-0.25,0,0.5,1}; tolerance 1e-6; tail mass far below the gap) "
        "matches the twin constants and functions; L05:261 interpretation matches the expected block (run_labs, twin_match).",
    ),
    "b-math-L06-facts-unnumbered": (
        "PASS",
        "A4(h) at L05:68 gives X_rho and rho F_rho-measurable for rho<=c; L06:102 restates F_t=sigma(B_r: 0<=r<=t) and F_rho; "
        "L06:135 computes {rho<=r}={tau_a<=r} in F_r (r<t) and Omega (r>=t); L06:140 cites A4(h) and A4(g).",
    ),
    "b-math-L06-prop-1.3-cor-1.4": (
        "PASS",
        "Re-derived L06:80-97: Prop 1.3 bijection through Lemma 1.2; {kappa<=N, S_N=2a-b} equals {S_N=2a-b} because "
        "S_0=0<a<2a-b (b<a); Cor 1.4: sum over b<a of #{S_N=2a-b} equals #{S_N>a}.",
    ),
    "b-math-L06-lemma-2.1": (
        "PASS",
        "Re-derived L06:110-114: IVT on [0,t]; {s: B_s=a} closed, so B_{tau_a}=a; (iii) t<tau_a gives B_t != a and B_s<=a, so B_t<a.",
    ),
    "b-math-L06-prop-2.3-thm-2.5": (
        "PASS",
        "Re-derived Prop 2.3 (L06:135-144): rho=tau_a^t bounded stopping time; W_t=B_rho-X_{t-rho}; freezing with Z=(B_rho,t-rho), "
        "Y=X; h_- = h_+ by symmetry of N(0,u). Thm 2.5 (L06:167-170): E={W_t>a}, P(W_t>a)=P(B_t>a), P(B_t=a)=0.",
    ),
    "b-math-L06-cor-2.6": (
        "PASS",
        "L06:181: z=sqrt2 w; lower limit a/sqrt(2t); prefactor sqrt2/sqrt(2 pi)=1/sqrt pi; erfc definition gives one half erfc.",
    ),
    "b-math-L06-R1-R3": (
        "PASS",
        "R1 parity argument (L06:410); R2 by Theorem 2.5 applied to -B (L06:417); R3 (L06:424).",
    ),
    "b-math-L06-E1-E3": (
        "PASS",
        "E1: 1+...+12 = 78 (L06:386). E2: 281/512 - 11/32 = 210/1024 = 105/512 (L06:393). E3: half of the printed value gives "
        "0.15865525393..., as stated (L06:400). Recomputed in recompute_numbers.py.",
    ),
    "b-scope-L06-only-events": (
        "PASS",
        "L06:102 'need the path only on [0,t]' and the events of Lemma 2.1 and Theorem 2.5 match the proofs; no scope overreach found.",
    ),
    "b-scope-L06-N12-every-case": (
        "PASS",
        "L06:186, L06:195 and L06:297 scope (N<=12, 1<=a<=N, b>=-N) match the enumeration domain in the code (range(1,13), "
        "range(1,n+1), range(-n,a)); the 'every case' wording is limited to that domain.",
    ),
    "b-lab-L06-claims": (
        "PASS",
        "L06:186 hypothesis (2^N enumeration; Parts A-E outputs) and L06:297 interpretation match the code and expected block "
        "(run_labs, twin_match).",
    ),
    "b-lab-L06-docstring-exact-fraction": (
        "PASS",
        "Twin docstring (tests/labs/SC1/lab-SC1-L06-1.py:4-5) and page L06:189-190 now say 'every probability in Parts A to D is "
        "an exact fraction; Part E evaluates a closed form in floating point'; Part E uses math.erfc.",
    ),
    "b-rounding-L06-misconception": (
        "PASS",
        "L06:316: P(M_1>=1)=0.3173 and P(B_1>=1)=0.1587 at four decimals (recompute: 0.3173105079 and 0.1586552539); "
        "Part E prints ten decimals as stated.",
    ),
    "b-plan-L06-pathlevel": (
        "PASS",
        "Recorded gap, not a silent deviation: L06 Definition 2.2 (L06:118-119) and Remark 2.4 (L06:148-149) state that the "
        "path-level statement is not proved here, and plans/SC1-open-items.md records the deviation from plans/SC1-build-plan.md "
        "section 3 with its reason and open status. Note for the architect (not a row failure): Definition 2.2 calls the "
        "statement 'a conjecture'; the open-items entry says it can be proved once tau_a<infinity is established, so 'not proved "
        "on this page' is the accurate wording.",
    ),
    "b-causal-L06-symmetry-last-step": (
        "PASS",
        "L06:306 canon break locates the factor 2 in the two equal-probability events of Theorem 2.5, and the symmetry at h_- = h_+ "
        "in Proposition 2.3; quiz L06:523-529 asks which symmetry is used at h_- = h_+; both match the proof at L06:144.",
    ),
    "b-quiz-L04-Q8-explain": (
        "PASS",
        "L04:438 explanation now reads E[X_t|F_s]=B_s+t, which differs from X_s=B_s+s when s<t (matches P1 at L04:289).",
    ),
    "b-quiz-L04-L06": (
        "PASS",
        "Quiz counts: L04 11 items, L05 10, L06 10 (8-15 rule). Each item has an explain block. Numeric answers checked: "
        "3, 27, 2.718281828 (tolerance 1e-9; |e-2.718281828|=4.6e-10), 54.598150033 (tolerance 1e-9), 3 (L05), 0.3989 (tolerance 1e-4), "
        "0.23975 (tolerance 1e-5; Phi(-1/sqrt2)=0.2397500611), 0.25, 0.3173 (tolerance 1e-4), 0.1587 (tolerance 1e-4).",
    ),
    "b-plan-coverage-L04-L05": (
        "PASS",
        "Plan section 3 content checked: L04 (filtration, martingale definition, B_t and B_t^2-t, exponential martingale with "
        "derivations, optional stopping not used); L05 (Markov at fixed times, Gaussian transition density, Chapman-Kolmogorov, A3 as "
        "a numbered assumption with a sketch). The Markov-definition s=t gap is a separate row.",
    ),
    "b-hours-L04-L06": (
        "PASS",
        "data-hours=9 on L04, L05, L06 (line 2 of each); index.html:29 data-hours-lessons=72 and data-hours-project=28; 8 x 9 = 72 and "
        "72 + 28 = 100.",
    ),
    "b-dag-D1-D9": (
        "PASS",
        "Grep of L04, L05, L06 and their twins for the D1-D9 names (Ito, geometric Brownian motion, Ornstein-Uhlenbeck, SDE, Euler, "
        "Milstein, Girsanov, Feynman-Kac, Kolmogorov equations, Poisson, Levy, Black-Scholes, barrier, Monte Carlo, bias, iterated "
        "logarithm, Donsker, continuity correction, change of measure): none found. M6 optional stopping is named in prose without a link (L04:232).",
    ),
    "b-process-words": (
        "PASS",
        "grep of L04-L06 and the three twins for builder, verifier, fixer, architect, planner, plan, REQUESTS, round, open item, TODO, "
        "TBD, lorem, for brevity, beyond the scope, left as an exercise, you can add, important to note, studies show, experts agree, "
        "well known, obviously, clearly and ellipses: no learner-visible hit; check_pages banned-string check PASS.",
    ),
    "b-cards-c061-c072": (
        "PASS",
        "cards.json read in full for SC1-c061 to c072 (L04): each checked against L04 text and numbers (c066 Lemma 2.1; c068 "
        "E[B_t^4]=3t^2; c070 E[W]=1; c072 lab numbers 54.598150033 and 1.000000000, grade C).",
    ),
    "b-cards-c073-c085": (
        "PASS",
        "cards.json SC1-c073 to c085 checked against L04 (P1, Section 3, misconceptions, R1-R2, P2-P3) and L05 Definition 1.1, "
        "1.2 and A4 (c085 matches parts (a) to (h) at L05:61-68).",
    ),
    "b-cards-c086-c097": (
        "PASS",
        "cards.json SC1-c086 to c097 checked. c091 back now says 'double-precision rounding error' (round-2 defect fixed). c093 "
        "states the A3 conclusion and 'assumed, not proved', which matches L05:274 and L05:279; the round-2 wording request "
        "concerned the sketch, not the statement. c086, c087, c088, c089, c090, c092, c094-c097 match their lesson text.",
    ),
    "b-cards-c098-c110": (
        "PASS",
        "cards.json SC1-c098 to c110 checked: c098 (B-tilde, L05:285), c099 (unbounded tau, L05:286), c100-c102 (misconceptions, "
        "L05:296-304), c103-c105 (M2, P2, M3 with A1(c) of L01:76), c106-c110 (L06 walk and Prop 1.3, Cor 1.4).",
    ),
    "b-cards-c111-c122": (
        "PASS",
        "cards.json SC1-c111 to c122 checked: c111 (1014 triples; run_labs output), c112 (78 pairs), c113 (281/512, 11/32, 105/512), "
        "c114 (495, 495, with 2a-b = 6-2 = 4), c115 (0.3173), c116-c118 (Lemma 2.1), c119 (Def 2.2 proved form), c120-c122 (Prop 2.3, Remark 2.4).",
    ),
    "b-cards-c123-c133": (
        "PASS",
        "cards.json SC1-c123 to c133 checked: c123 (Thm 2.5), c124 (Cor 2.6), c125 (jump example), c126 (0.3173 vs 0.1587), "
        "c127 (105/512), c128 (continuity and A3), c129 (5 of 8), c130-c132 (R1-R3), c133 (bounded rho = t).",
    ),
    "b-cards-duplicates": (
        "PASS",
        f"ledgers/SC1/scripts/SC1-b-r3/cards_scan.py: 187 cards, 187 unique ids, no duplicate fronts; L04-L06 cards 74 "
        f"(L04 22, L05 24 including SC1-c189, L06 28) ({OUTS}/cards_scan.txt).",
    ),
}

NEW_ROWS = [
    {
        "id": "b-math-L05-def-1.1-st-case",
        "check": "2.4 mathematics: Definition 1.1 (Markov property for all 0<=s<=t) is covered by Theorem 1.4 and its conclusion",
        "location": "course/modules/SC/SC1/L05.html:75 (Definition 1.1), :110 (Theorem 1.4 statement 'For 0<=s<t'), :114 ('So B has the Markov property of Definition 1.1')",
        "status": "FAIL",
        "evidence": (
            "Definition 1.1 requires E[g(B_t)|F_s]=psi(B_s) almost surely for all 0<=s<=t. Theorem 1.4 states and proves it only for "
            "0<=s<t (proof at L05:119-120), and L05:114 concludes 'So B has the Markov property of Definition 1.1' without the s=t case. "
            "The s=t case is trivial (B_t is F_t-measurable, so psi=g and E[g(B_t)|F_t]=g(B_t)), but the page does not say so. This is the "
            "same kind of gap as the s=t case of Lemma 1.3, which this round's fix closed."
        ),
        "fix": (
            "In L05.html after Theorem 1.4's proof, add: 'For s = t take psi = g: B_t is F_t-measurable, so E[g(B_t) | F_t] = g(B_t) "
            "almost surely.' Then the sentence at L05:114 holds for all 0 <= s <= t."
        ),
    }
]

SCRIPTS = [
    "ledgers/SC1/scripts/SC1-b-r3/twin_match.py",
    "ledgers/SC1/scripts/SC1-b-r3/cards_scan.py",
    "ledgers/SC1/scripts/SC1-b-r3/recompute_numbers.py",
    "ledgers/SC1/scripts/SC1-b-r3/build_fragment.py",
]


def main() -> None:
    prev = json.loads(PREV.read_text(encoding="utf-8"))
    rows = []
    for old in prev["rows"]:
        rid = old["id"]
        status, evidence = EVIDENCE[rid]
        row = {"id": rid, "check": old["check"], "location": old["location"], "status": status, "evidence": evidence}
        rows.append(row)
    extra_ids = set(EVIDENCE) - {r["id"] for r in rows}
    assert not extra_ids, extra_ids
    rows.extend(NEW_ROWS)
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
    verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
    fragment = {
        "unit": "SC1",
        "slice": "b",
        "round": 3,
        "verifier": "Claude Haiku 5.5, independent verifier for SC1-b, round 3 (did not build SC1)",
        "pin": "67a2d13e",
        "base": "67c4768 (round-2 pin; delta read hunk by hunk for L04, L05, L06, the three twins, cards.json, and L01-L03, L08, M6 cross-references)",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyE3-SC1-b",
        "scratch": "ledgers/SC1/scripts/SC1-b-r3",
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "verdict": verdict,
        "counts": counts,
        "rows": rows,
        "mutants": [],
        "registry_flags": [],
        "freshness_flags": [],
        "scripts": SCRIPTS,
        "notes": (
            "Round 3 full verification of SC1 slice b (L04, L05, L06, the three lab twins, and the cards with lesson L04-L06). "
            "Every round-2 FAIL row was re-checked on pin 67a2d13e: the 10 closed rows now PASS with the cited fixes. The round-2 "
            "row b-plan-L06-pathlevel passes on the recorded open-items entry. One new FAIL row is raised: Definition 1.1's s=t case "
            "is not covered (b-math-L05-def-1.1-st-case). Out of slice (for the project slice verifier): project.html:240 applies "
            "A3 'for the first hitting time tau_a', but L05.html:277 and :286 state that A3 is stated only for bounded rho and does "
            "not extend to unbounded tau_a. Not checked: hub index.html and project.html content beyond hours; cards for L01-L03 and "
            "L07-L08; Shreve (2004) and Karatzas-Shreve were not read, so no locator is claimed; the full repository gate (no "
            "dependency, build or CI change, so the targeted run was used); mutate_graders.py and mutants (no project grader in "
            "slice b; lab twins are demonstrations by architect ruling); page_smoke run once, alone."
        ),
        "summary": (
            f"SC1-b round 3: verdict {verdict}. Rows: pass={counts['PASS']} fail={counts['FAIL']} "
            f"unverifiable={counts['UNVERIFIABLE']} ({len(rows)} rows). Non-PASS: b-math-L05-def-1.1-st-case."
        ),
    }
    OUT.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} rows={len(rows)} counts={counts} verdict={verdict}")


if __name__ == "__main__":
    main()
