"""Writes the round-8 verifier fragment for SC1 slice c (L07, L08, lab twins). Data only; no computation."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE8-SC1-c")
OUT = "ledgers/SC1/scripts/SC1-c-r8/out"
S = "ledgers/SC1/scripts/SC1-c-r8"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---- gates and commands (run by this verifier at 0dee921) ----
row("gate-check-pages", "2.9 structure (check_pages)",
    "course/modules/SC/SC1/L07.html, L08.html", "PASS",
    f"Round 8: .venv/bin/python tools/check_pages.py --unit SC1 --page L07 -> exit 0 ({OUT}/check_pages_L07.txt); --page L08 -> exit 0 ({OUT}/check_pages_L08.txt); --unit SC1 -> exit 0, 'check_pages SC1: PASS' ({OUT}/check_pages_SC1.txt).")
row("gate-check-dag", "2.9 DAG (check_dag)",
    "course/modules/SC/SC1/L07.html, L08.html", "PASS",
    f"Round 8: .venv/bin/python tools/check_dag.py --unit SC1 -> exit 0, 'check_dag SC1: PASS' ({OUT}/check_dag_SC1.txt). Dfn ids def-running-maximum-distribution (L07:64) and def-first-passage-time (L08:59) each appear once.")
row("gate-run-labs", "2.5 labs (run_labs)",
    "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py", "PASS",
    f"Round 8: .venv/bin/python tools/run_labs.py --unit SC1 -> exit 0, 'run_labs SC1: PASS (11/11)' ({OUT}/run_labs_SC1.txt).")
row("lab-L07-twin-isolated", "2.5 labs (twin under python -I -W error)",
    "tests/labs/SC1/lab-SC1-L07-1.py", "PASS",
    f"Round 8: copied to a fresh mktemp directory, ran .venv/bin/python -I -W error lab-SC1-L07-1.py -> exit 0, stderr 0 bytes ({OUT}/twins/L07.stdout, L07.stderr).")
row("lab-L08-twin-isolated", "2.5 labs (twin under python -I -W error)",
    "tests/labs/SC1/lab-SC1-L08-1.py", "PASS",
    f"Round 8: same procedure -> exit 0, stderr 0 bytes ({OUT}/twins/L08.stdout, L08.stderr).")
row("lab-L07-page-equals-twin", "2.5 labs (embed: page code equals twin)",
    "course/modules/SC/SC1/L07.html:151-352 vs tests/labs/SC1/lab-SC1-L07-1.py", "PASS",
    "run_labs (gate-run-labs) compares each data-run block byte for byte with its twin; PASS in round 8.")
row("lab-L08-page-equals-twin", "2.5 labs (embed: page code equals twin)",
    "course/modules/SC/SC1/L08.html:143-343 vs tests/labs/SC1/lab-SC1-L08-1.py", "PASS",
    "run_labs compares each data-run block with its twin; PASS in round 8.")
row("lab-L07-expected-equals-output", "2.5 labs (expected block equals output)",
    "course/modules/SC/SC1/L07.html:353-375 (pre.expected)", "PASS",
    f"run_labs checks the expected block against the twin's stdout under the page's rule; PASS. Twin stdout in {OUT}/twins/L07.stdout.")
row("lab-L08-expected-equals-output", "2.5 labs (expected block equals output)",
    "course/modules/SC/SC1/L08.html:344-363 (pre.expected)", "PASS",
    f"run_labs PASS; twin stdout in {OUT}/twins/L08.stdout.")
row("lab-L07-printed-numbers", "2.2 numbers (a) lab-computed, recomputed independently",
    "course/modules/SC/SC1/L07.html:353-376", "PASS",
    f"Every printed value re-derived by {S}/indep_r8.py (output {OUT}/indep_r8.txt): DP tails 0.375000, 0.332306, 0.321084, 0.318255, 0.317547; counts 91/107/113/121; SEs 0.0210/0.0222/0.0225/0.0230; means 0.5546/0.6639/0.7232/0.7586 with SE 0.0315/0.0316/0.0315/0.0317; differences; Part D 0.1586552539 (erfc and Simpson agree).")
row("lab-L08-printed-numbers", "2.2 numbers (a) lab-computed, recomputed independently",
    "course/modules/SC/SC1/L08.html:344-364", "PASS",
    f"{S}/indep_r8.py (R5-R8): exact truncated means 5.480560, 11.815731, 24.557203 by an absorbing DP; first-passage counts 512,0,384,0,288,0,224,0,180,0 (sum 1588); S_12>=3 count 794; z -1.047/-0.687/-0.775; densities 0.241971 and 0.109848; P(tau_1<=2)=0.479500.")
row("lab-L07-hypothesis-interpretation", "2.5 lab statements (hypothesis and interpretation match output)",
    "course/modules/SC/SC1/L07.html:150 (hypothesis) and :376 (interpretation)", "PASS",
    "Hypothesis names Corollary 1.4 of Lesson 6 for Part A (page L06:87 is 'discrete tail identity'), the decreasing tails, Proposition 2.2 for the nested counts, and the Part D evaluation; each matches the printed lines. The printed label 'walk identity' is covered by term-walk-identity-L07.")
row("lab-L08-hypothesis-interpretation", "2.5 lab statements (hypothesis and interpretation match output)",
    "course/modules/SC/SC1/L08.html:142 (hypothesis) and :364 (interpretation)", "PASS",
    "Interpretation statements (8190 sequences; 90114 pairs; 512,0,...,180,0; 1588 = 2 x 794; z values; the 1.1-SE statement in the key results; Part D to 1e-8) match the output and the independent recomputation.")
row("lab-simulated-labels-seeds", "2.5 labs (seeds; SIMULATED labels)",
    "course/modules/SC/SC1/L07.html:149; L08.html:141; tests/labs/SC1/lab-SC1-L07-1.py:32; lab-SC1-L08-1.py:37", "PASS",
    "L07 SEED = 20260507 (twin line 32) and L08 SEED = 20260508 (twin line 37), both through random.Random(SEED). The L07 heading says Parts B and C are SIMULATED (page line 149); the L08 heading says Part C is SIMULATED (page line 141). L07 Parts A and D and L08 Parts A, B and D use no randomness, as their twin docstrings say.")
row("lab-runtime", "2.5 labs (runtime under 10 s)",
    "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py", "PASS",
    f"page_smoke (round 8) reports lab lab-SC1-L07-1 0.1 s and lab-SC1-L08-1 0.2 s in Pyodide ({OUT}/page_smoke_L07_L08.txt).")
row("lint-mypy-twins", "code quality (ruff, mypy strict)",
    "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py; whole repo", "PASS",
    f"Round 8: ruff check . -> 'All checks passed!' (exit 0); ruff format --check . -> '553 files already formatted' (exit 0); mypy --no-incremental -> 'Success: no issues found in 385 source files' (exit 0). Outputs in {OUT}/ruff_full.txt, ruff_format_full.txt, mypy_full.txt.")
row("page-smoke-L07-L08", "2.9 page_smoke (console, math, 360 px, labs in Pyodide)",
    "course/modules/SC/SC1/L07.html, L08.html", "PASS",
    f"Round 8: .venv/bin/python tools/page_smoke.py --unit SC1 --pages L07 L08 -> exit 0, both PASS, 'page_smoke SC1: PASS' ({OUT}/page_smoke_L07_L08.txt).")
row("pytest-lab-tools", "2.5 labs (pytest, tooling)",
    "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
    f"Round 8: pytest with -k 'SC1 or run_labs or page_checks or lab' over the three files -> exit 0, 334 progress dots, no failures ({OUT}/pytest_lab_tools.txt). The -q summary line was not printed in the captured output.")
row("verify-refs-offline", "2.1 citations (integrity, offline)",
    "references/references.json", "PASS",
    f"Round 8: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' ({OUT}/verify_refs_offline.txt).")
row("verify-refs-live-SC1", "2.1 citations (live, unit SC1)",
    "references/references.json entry shreve2004stochastic (line 20732); L07.html:614; L08.html:601", "PASS",
    f"Round 8: .venv/bin/python tools/verify_refs.py --unit SC1 (live) -> 'live re-verification of SC1: 1 of 560 entries, 0 problems' ({OUT}/verify_refs_SC1_live.txt). The registry title 'Stochastic Calculus for Finance II', author Shreve and year 2004 match the lesson sentence.")
row("refs-no-citation-markup", "2.1 attribution (no unread citation)",
    "course/modules/SC/SC1/L07.html:614, L08.html:601", "PASS",
    "Both reference sections say no passage is cited from the registry source; no data-locator, no theorem number from it, no page number. Every theorem number used (Theorem 2.5, Corollary 2.6, Lemma 2.1, Corollary 1.4 of Lesson 6; Definition 1.1 of Lesson 1; Theorem 1.3, Corollary 1.5 of this lesson) is an internal cross-reference, checked against L06.html:63-174, L01.html:58, L05.html:270-288.")

# ---- claim grades, mathematics, problems, key results, quiz, structure ----
row("claim-grades-L07", "2.3 grades (re-graded against BLUEPRINT section 3)",
    "course/modules/SC/SC1/L07.html:68-146, 511-529", "PASS",
    "Theorem 1.3, Corollaries 1.5(a),(b), Proposition 2.2, Corollary 2.3, Remark 2.4 are T with complete proofs (read in full); lab-computed results are C with the basis named; the Assumption A5 is labelled as a numbered assumption (L07.html:97-99).")
row("claim-grades-L08", "2.3 grades (re-graded against BLUEPRINT section 3)",
    "course/modules/SC/SC1/L08.html:63-138, 499-516", "PASS",
    "Proposition 1.2, Corollaries 1.3, 1.4, 1.5 are T with proofs read in full; Proposition 2.2, 2.3 are T; the enumerated lab results are C; Remark 1.6 states no value for E[tau_a].")
row("math-L07-thm-1.3", "2.4 mathematics (Theorem 1.3 and proof)",
    "course/modules/SC/SC1/L07.html:68-82", "PASS",
    "Re-derived: 2(1-Phi(a/sqrt H)) = erfc(a/sqrt(2H)) (identity erfc(x/sqrt2)=2(1-Phi(x))); the proof's step through Theorem 2.5 of Lesson 6 (L06.html:152-171) and Corollary 2.6 (L06.html:173-183) matches; the atom-free step is valid. Numeric check: indep_r8.py R3/R9.")
row("math-L07-cor-1.5b", "2.4 mathematics (Corollary 1.5(b))",
    "course/modules/SC/SC1/L07.html:101-107", "PASS",
    "Integration by parts: int_0^R (1-Phi) = R(1-Phi(R)) + phi(0) - phi(R); bound 0 <= R(1-Phi(R)) <= phi(R) -> 0; int_0^inf (1-Phi) = 1/sqrt(2pi); E[M_H] = 2 sqrt(H) / sqrt(2pi) = sqrt(2H/pi). Numeric sqrt(2/pi)=0.797884561 (indep_r8.py R3).")
row("math-L07-prop-2.2-cor-2.3-remark-2.4", "2.4 mathematics (Prop 2.2, Cor 2.3, Remark 2.4)",
    "course/modules/SC/SC1/L07.html:119-146", "PASS",
    "Prop 2.2(b): s_k = kH/N = (kc)H/N' when N' = cN, so the N-grid is a subset of the N'-grid; the max over a subset is at most the max over the set. Corollary 2.3 inclusion correct. Remark 2.4: max(0,B_H) >= a iff B_H >= a for a>0; factor 2 from Theorem 2.5 of Lesson 6.")
row("math-L07-def-2.1-grid-times", "2.4 mathematics (notation and definition)",
    "course/modules/SC/SC1/L07.html:116", "PASS",
    "s_k = kH/N for k = 0..N, and M^(N)_H = max over k of B_{s_k}; consistent with the twin's grid_maximum (stride FINE//n, n+1 points).")
row("math-L07-remark-1.4-phi0", "2.4 mathematics (Remark 1.4)",
    "course/modules/SC/SC1/L07.html:83-86", "PASS",
    "Limits: a/sqrt(H) -> inf as H->0 gives tail -> 0; -> 0 as H->inf gives 2(1-1/2)=1; Phi(0)=1/2 by evenness; Pr(Z>=0)+Pr(Z<=0) = 1 + Pr(Z=0) with Pr(Z=0)=0.")
row("math-L07-R1-R3-P2-P3-M-E", "2.4 mathematics (problem solutions)",
    "course/modules/SC/SC1/L07.html:411-508", "PASS",
    "M1 (erfc(2/sqrt8)=erfc(1/sqrt2): checked), M2, M3 (Remark 2.4), P1, P2 (integration by parts re-derived), P3 (Prop 2.2(b)), E1 (91, 121, both integers), E2 (14893 + 6885 = 21778; 21778/65536 = 0.332306, checked), E3 (k(n-k)/(n^2(n-1)) = 33759/63840000; sqrt = 0.022996, printed 0.0230), R1 (signs and Phi evenness), R2 (events increase, continuity), R3 (tau_a <= H iff M_H >= a by Lemma 2.1 of Lesson 6, limit checked).")
row("math-L08-prop-1.2-cor-1.3-1.4", "2.4 mathematics (Prop 1.2, Cor 1.3, Cor 1.4)",
    "course/modules/SC/SC1/L08.html:63-94", "PASS",
    "Prop 1.2 both inclusions re-derived (IVT on [0,s*] with B_0=0 < a; closed set {s: B_s=a}); Cor 1.3 chain of equalities cites the right results (Prop 1.2; Theorem 1.3 of Lesson 7; Corollary 2.6 of Lesson 6); Cor 1.4 limit of 2(1-Phi(a/sqrt n)) -> 1 is valid.")
row("math-L08-cor-1.5", "2.4 mathematics (Corollary 1.5, density)",
    "course/modules/SC/SC1/L08.html:97-106", "PASS",
    "F(H)=2(1-Phi(a H^{-1/2})); F'(H) = a H^{-3/2} phi(a H^{-1/2}) = a e^{-a^2/(2H)}/(sqrt(2pi) H^{3/2}); F(0+)=0 since a/sqrt(eps) -> inf; so F = integral of f_a. Numeric: f_1(1)=0.2419707245, central difference agrees to 5e-12 (indep_r8.py R8). Remark 1.6 asymptotic f_a H^{3/2} sqrt(2pi) -> a checked at H=1e6.")
row("math-L08-prop-2.2-2.3", "2.4 mathematics (Prop 2.2, 2.3)",
    "course/modules/SC/SC1/L08.html:116-138", "PASS",
    "Prop 2.2: first index with S_k >= a equals a since steps are +-1 (re-derived; brute force 90114 of 90114 pairs in indep_r8.py R1). Prop 2.3: min(nu,N) = sum of indicators; for k=0 both sides 1 since S_0 = 0 < a and nu >= 1; exact truncated means by absorbing DP (indep_r8.py R5) match the printed values.")
row("math-L08-R3", "2.4 mathematics (Problem R3)",
    "course/modules/SC/SC1/L08.html:489-495", "PASS",
    "log f_a(H) derivative (a^2 - 3H)/(2H^2); mode at H = a^2/3 (re-derived). Assumptions stated (A3, A4 through Corollary 1.5).")
row("math-L08-R1-R2", "2.4 mathematics (Problems R1, R2)",
    "course/modules/SC/SC1/L08.html:476-487", "PASS",
    "R1: #{nu<=N} = #{S_N>=a} + #{S_N>a} = 2#{S_N>=a} - #{S_N=a} (re-derived); 1588 = 2*794 checked (indep_r8.py R6). R2: min(nu,N+1) - min(nu,N) = 1{nu > N}.")
row("prob-L08-all", "2.4 problems (all L08 problems, solutions)",
    "course/modules/SC/SC1/L08.html:399-497", "PASS",
    "Read every L08 problem and solution: M1 (erfc(1/sqrt2) = 0.317311, checked), M2 (f_1(1)=0.241971, unrounded 0.2419707, checked), M3 (5/8 by listing 8 sequences: +1 start gives 4, -1 start gives 1 via (-1,+1,+1)), P1-P3, E1-E3, R1-R3 as above.")
row("prob-L07-remaining", "2.4 problems (other L07 problems)",
    "course/modules/SC/SC1/L07.html:411-508", "PASS",
    "All L07 problems M1-M3, P1-P3, E1-E3, R1-R3 read with solutions; each solution matches the lesson and the printed numbers.")
row("misconceptions-L07-content", "2.4 misconceptions (content)",
    "course/modules/SC/SC1/L07.html:390-402", "PASS",
    "Three misconceptions, each with a correct explanation: 2x tail (0.3173105 and 0.1586553 to seven decimals, checked); grid tail below closed form (Prop 2.2(a), Cor 2.3); normal marginals do not fix the tail (L01 Section 4 tilde-B, Lemma 2.1 of Lesson 6 needs continuity).")
row("misconceptions-L08-content", "2.4 misconceptions (content)",
    "course/modules/SC/SC1/L08.html:379-391", "PASS",
    "Three misconceptions: finite on every path (probability vs outcome, Cor 1.4); first passage equal to terminal value (factor 2; 0.317311 vs 0.1586552539; walk 0.387695 vs 0.193848 with parity); finiteness implies finite mean (Remark 1.6). All checked.")
row("canon-breaks-L07-L08", "2.4 canon breaks",
    "course/modules/SC/SC1/L07.html:379-386; course/modules/SC/SC1/L08.html:367-374", "PASS",
    "Each lesson names a hypothesis whose failure breaks the result: continuity (both; L08 jump example 0 on [0,1/2), 2 after, verified: M_1 = 2, path never equals 1), A3/A4 conditionality, grid discreteness (L07), finiteness vs integrability (L08). The L07 remark 'a sketch for A3 only' matches L05.html:278-288 (A3 has a sketch, A4 does not).")
row("key-results-L07", "2.4 key-results table",
    "course/modules/SC/SC1/L07.html:511-529", "PASS",
    "Each row's grade and source checked against the sections; the lab row grades C, the mean row C, the discrete-tail row C (enumerated 78 pairs, the identity itself is T at L06.html:87-94).")
row("key-results-L08", "2.4 key-results table",
    "course/modules/SC/SC1/L08.html:499-516", "PASS",
    "Each row's grade and source checked. The 90114-pair row is C and cites Lab 1 Part A; the 1.1-SE row is C and cites Lab 1 Part C (z values -1.05, -0.69, -0.77, all below 1.1).")
row("quiz-L07", "2.9 quiz (keys, tolerances, explanations)",
    "course/modules/SC/SC1/L07.html:531-610", "PASS",
    "10 items; keys checked: Q2 0.3173105 vs 0.31731050786 (diff 7.9e-9, tol 1e-6), Q4 0.158655 vs 0.1586552539 (diff 2.5e-7, tol 1e-6), Q6 0.797885 vs 0.7978845608 (diff 4.4e-7, tol 1e-6), Q8 0.3173105; mc keys Q3, Q5 (2*Phi(0)-1=0), Q7, Q9, Q10 agree with the lesson; each explanation names the result it uses.")
row("quiz-L08", "2.9 quiz (keys, tolerances, explanations)",
    "course/modules/SC/SC1/L08.html:518-597", "PASS",
    "10 items. Q2 0.3173105 (diff 7.9e-9); Q3 0.625 exact (5/8); Q5 5.48056 with tol 1e-5 vs exact 179587/32768 = 5.4805603 (verified exact: indep_r8.py R5, equal True); Q6 0.241971 (diff 2.7e-7, tol 1e-6); mc keys Q1, Q4, Q7, Q8, Q9, Q10 agree with the lesson.")
row("structure-L07", "2.9 structure and prose (template sections)",
    "course/modules/SC/SC1/L07.html", "PASS",
    "Order: why-it-matters (117 whitespace tokens including math; 110 outside math), s1, s2 with lab, canon-breaks, misconceptions (3), problems (3 per tier, 12 total, each with details.solution), key-results, quiz (10), references. Study hours 9 in eyebrow and data-hours.")
row("structure-L08", "2.9 structure and prose (template sections)",
    "course/modules/SC/SC1/L08.html", "PASS",
    "Same order; misconceptions (3); problems 3 per tier; quiz 10 items; references; study hours 9.")
row("banned-and-process-words", "2.9 banned phrases and process words",
    "course/modules/SC/SC1/L07.html, L08.html; twins", "PASS",
    "grep over both pages and both twins for the BUILDER_RULES banned strings and process words (builder, verifier, round, fixer, planner, architect, ruling, precedent, TODO, TBD, lorem, obviously, clearly, ellipses): no hits; check_pages banned-string check PASS.")
row("notation-macros", "2.4 notation (notation.json)",
    "course/modules/SC/SC1/L07.html, L08.html", "PASS",
    "Macros used on the two pages: \\Prob, \\E, \\Phi, \\indic (Proposition 2.3 proof in L08), \\Normal (once in L08). \\se is registered but does not occur on these pages. \\varphi is the local Gaussian density, which the plan allows. No unregistered macro was found in a grep of both pages.")
row("dag-defined-once-L07-L08", "2.9 DAG (defined once)",
    "course/modules/SC/SC1/L07.html:64, :115-117; course/modules/SC/SC1/L08.html:59", "PASS",
    "Dfn ids: running-maximum-distribution once (L07:64); first-passage-time once (L08:59); the discretely monitored maximum and first passage of the walk are plain dfn without data-concept.")
row("dag-outside-closure", "2.9 DAG (outside the prerequisite closure)",
    "course/modules/SC/SC1/L07.html:37, L08.html:37 (meta links)", "PASS",
    "The concept links are brownian-motion, brownian-motion-construction, normal-distribution, random-variable, expectation, running-maximum-distribution, first-passage-time: all in SC1's prerequisite closure or SC1's own. Grep for D1-D9 names (Ito/SDE/Euler/Girsanov/Feynman/Poisson/Levy/Black-Scholes/barrier/Monte Carlo/stopping/martingale): no concept use in either page; 'monitoring' and 'option' hits are plain-English or HTML class names.")
row("xref-L01-L05-L06", "2.1 cross references (Lessons 1, 5, 6)",
    "course/modules/SC/SC1/L07.html, L08.html; L06.html:63-183; L05.html:270-288; L01.html:58-68, 215", "PASS",
    "Every cross-reference checked: Definition 1.1 of Lesson 1 (L01.html:58) for D2 with s=0; Lesson 1 Section 4 tilde-B (L01.html:212-216); Theorem 2.5 and Corollary 2.6 and Lemma 2.1 of Lesson 6; Corollary 1.4 of Lesson 6 (discrete tail identity); A3 and A4 of Lesson 5; Lesson 5 Section 1 and 3 not cited by these pages.")
row("cards-dup-and-numbers", "2.7 cards (duplicates; numbers appear in lesson)",
    "course/modules/SC/SC1/cards.json (193 cards)", "PASS",
    f"{S}/dup_scan.py over all 193 cards: ids unique; no exact duplicate front or back; two near-duplicate fronts exist outside this slice (SC1-c011/c012 at 0.862, SC1-c067/c068 at 0.918), judged distinct questions. Every number on a card (21778, 14893, 6885, 0.2275, 0.3025, 0.0210, 0.0230, 0.7586, 0.0317, 0.797885, 0.1586552539, 0.317311, 1588, 794, 0.387695, 0.193848, 5.480560, 11.815731, 24.557203, the z values, 0.241971, 0.109848) appears in its lesson or the twin output, checked by reading each card against its lesson.")
row("cards-L07-L08-full-read", "2.7 cards (full read of all L07 and L08 cards)",
    "cards.json: SC1-c134..c159 and c191 (L07, 25 cards), SC1-c161..c205 (L08, 22 cards)", "PASS",
    "All 47 cards in the slice read in full (L07: c134-c159 and c191, 25 cards; L08: c161-c205, 22 cards). Each back was checked against the current lesson text for the cited result, hypotheses and number. The lab-output cards (c148-c150, c170-c174) were checked against out/indep_r8.txt. Card c205 is new and correct. Card c166 was removed; the content it carried (no value for E[tau_a]) is still covered by c178 and by Remark 1.6 (L08.html:107-110).")
row("proof-L07-cor-1.5a-continuity-direction", "2.4 mathematics (continuity from below)",
    "course/modules/SC/SC1/L07.html:103", "PASS",
    "The events {M_H >= b} increase as b decreases to m, and their union over b>m is {M_H>m}; continuity from below then gives Pr(M_H>m) = lim Pr(M_H>=b). Cards c157 uses the same direction with a+1/n (checked).")
row("prob-L07-P1-continuity", "2.4 problems (P1 continuity step)",
    "course/modules/SC/SC1/L07.html:441", "PASS",
    "P1 uses the same continuity step and states the assumptions (H1, H2, H3).")
row("prob-L07-R2-continuity", "2.4 problems (R2 continuity step)",
    "course/modules/SC/SC1/L07.html:498", "PASS",
    "R2 solution: {M_H>=b} increase as b decreases to a; union {M_H>a}; Pr(M_H>a) = 2(1-Phi(a/sqrt H)) = Pr(M_H>=a); difference 0 (checked).")
row("num-rounding-0.3173105078", "2.2 numbers (rounding of the closed form)",
    "course/modules/SC/SC1/L07.html:376, :393, :416, :547, :589; course/modules/SC/SC1/L08.html:404, :411, :534", "PASS",
    "2(1-Phi(1)) = 0.31731050786 (unrounded, checked by erfc and erf). 0.3173105 to seven decimals and 2 x 0.1586552539 = 0.3173105078 on printed digits, as stated in each place.")
row("notation-T-first-passage-index", "2.4 notation (T and nu)",
    "course/modules/SC/SC1/L07.html:59; course/modules/SC/SC1/L08.html; notation/notation.json:112", "PASS",
    "T appears in L07 only in the sentence reserving T for return observations (notation.json T is S1's meaning). L08 uses nu_a and tau_a; no T as a horizon.")
row("dag-simple-random-walk-defined-twice", "2.9 DAG (no second definition of a term)",
    "course/modules/SC/SC1/L07.html:150; course/modules/SC/SC1/L08.html:113", "PASS",
    "The simple random walk is defined in L06 (dfn at L06.html:53) and used by name in L07 and L08 without a second definition.")
row("prose-L08-same-events", "2.9 prose (events)",
    "course/modules/SC/SC1/L08.html:51, :63-70, :77-81", "PASS",
    "'Coincide on every continuous path' is the claim of Prop 1.2, proved for each path; no almost-sure wording is used for it.")
row("prose-L08-first-passage-name", "2.9 prose (naming)",
    "course/modules/SC/SC1/L08.html:59, :116-117", "PASS",
    "'First-passage time' is defined in §1 and 'first-passage index nu_a' in §2 (Definition 2.1). The two names are distinct and each is defined before use in its section.")
row("lab-L07-docstring-exact-fractions", "2.5 lab docstring vs code",
    "tests/labs/SC1/lab-SC1-L07-1.py:1-23 (module docstring)", "PASS",
    "Docstring statements checked against code: Part A exact integer counts over 2**N, Part B divisor PATHS-1, Part D Simpson on [1,13] with SIMPSON_INTERVALS intervals, grids nested. The phrase 'walk identity' in the docstrings is covered by term-walk-identity-L07, not here.")
row("scope-L07-assumption-phrase", "2.4 scope (assumption phrasing)",
    "course/modules/SC/SC1/L07.html:55, :68-82, :83-86, :91-92, :103, :134-146, :376, :511-529", "PASS",
    "Every scope sentence was read (see scope-words-full-scan-r8). 'Every result below that uses them says so' holds: each result that uses the closed form names A3/A4 or H2.")
row("scope-L08-everything-after", "2.4 scope (assumption phrasing)",
    "course/modules/SC/SC1/L08.html:55, :63-81, :87-90, :97-106, :371", "PASS",
    "The uses of 'every' and 'always' on L08 are on enumerated pairs or on continuous paths for Prop 1.2; Corollary 1.4 is stated as a probability and the page says so.")
row("notation-kappa-redefined", "2.4 notation (kappa)",
    "course/modules/SC/SC1/L07.html, L08.html", "PASS",
    "kappa does not appear in either page (L06 uses it for the first visit; SC1-c-r8 grep: 0 hits).")
row("math-L08-prop-2.3-denominator", "2.4 mathematics (Prop 2.3 denominator)",
    "course/modules/SC/SC1/L08.html:132", "PASS",
    "P(nu_a > k) is an integer over 2^k (complement of a count over 2^k); exact denominators are powers of two (indep_r8.py R5, 'fraction_denominator_power2=True').")
row("prob-L07-P1-assumptions", "2.4 problems (P1 assumptions)",
    "course/modules/SC/SC1/L07.html:441", "PASS",
    "P1 states H1, H2, H3 and the use of H3 at each level b>0.")
row("notation-horizon-H", "2.4 notation (architect decision: H is the horizon symbol)",
    "course/modules/SC/SC1/L07.html:59", "PASS",
    "H is the horizon throughout both lessons; the reservation of T is stated once in L07 Definition 1.1.")
row("lab-L08-twin-docstring-PATHS", "2.5 lab docstring vs code",
    "tests/labs/SC1/lab-SC1-L08-1.py:1-28 (module docstring) and :40-42 (constants)", "PASS",
    "Module docstring: Part A enumerates n = 1..12 with all levels a <= n (code: range(1, MAX_ENUM+1), range(1, n+1)); Part B exact truncated means by the stated identity; Part C SIMULATED with 1000 walks of 256 steps (SIM_PATHS, SIM_STEPS); Part D formulas and central difference (DIFFERENCE_STEP 1e-5). The docstring says 'discrete tail identity of Lesson 6' and the code's check uses the same identity.")
row("cards-L07-misconception-same-law", "2.7 cards (misconception coverage, L07)",
    "cards.json SC1-c191; course/modules/SC/SC1/L07.html:392-393", "PASS",
    "c191 agrees with misconception 1 (P(M_H<=0)=0 by Corollary 1.5(a), m=0; P(B_H<=0)=1/2 by Remark 1.4).")
row("lab-L08-partA-printed-label", "2.5 lab output label (sequences vs pairs)",
    "tests/labs/SC1/lab-SC1-L08-1.py (Part A prints); course/modules/SC/SC1/L08.html:344-352", "PASS",
    "The printed labels distinguish 8190 sequences from 90114 (sequence, level) pairs and the 78 (n, a) pairs; checked by indep_r8.py R1. The label 'walk identity' inside these lines names the Proposition 2.2 identity defined on L08; the term is consistent within L08 (see term-walk-identity-L08).")
row("rounding-rule-lab-printed-figures", "2.2 numbers (rounding rule stated for rounded lab figures)",
    "course/modules/SC/SC1/L07.html:376; course/modules/SC/SC1/L08.html:364", "PASS",
    "Both interpretation paragraphs state the rounding rule; the twin formats (.6f, .4f, .2f, .10f) match the rule; differences are computed from unrounded values (confirmed by the independent recomputation's unrounded differences).")
row("math-L07-cor-1.5a-H3-reading", "2.4 mathematics (Corollary 1.5(a), H3 reading)",
    "course/modules/SC/SC1/L07.html:91, :103", "PASS",
    "Corollary 1.5(a)'s m>=0 case uses Theorem 1.3 at levels b>0 (H3 is applied at each b); the m=0 case is handled by the same limit; no level a is needed beyond that.")
row("recompute-walk-dp-L07-L08", "2.2 numbers (independent algorithm)",
    f"{S}/indep_r8.py; {OUT}/indep_r8.txt", "PASS",
    "Walk tails by a DP over positions (not binomials): N = 4, 16, 64, 256, 1024 give 0.375000, 0.332306, 0.321084, 0.318255, 0.317547; brute force over 2^n sequences for n <= 12 gives 78/78 identities and 90114/90114 pathwise agreements; first-passage counts for n=12, a=3 match; truncated means by absorbing DP match.")
row("recompute-sim-L07-B-C-L08-C", "2.2 numbers (simulated figures, independent code)",
    f"{S}/indep_r8.py; {OUT}/indep_r8.txt", "PASS",
    "The seeded simulations were regenerated with the same RNG draw order and independent statistics: L07 proportions 0.2275/0.2675/0.2825/0.3025 with SEs 0.0210/0.0222/0.0225/0.0230 and 0 violations; L07 means and SEs; L08 means 5.2850/11.3840/23.1240 with SEs 0.1868/0.6288/1.8497 and z -1.047/-0.687/-0.775. All agree with the printed output.")
row("remark-1.4-title-L07", "2.4 mathematics / 2.9 prose (title claim)",
    "course/modules/SC/SC1/L07.html:83-84", "PASS",
    "The title 'limits in the horizon' matches the content (H -> 0 and H -> inf limits of Pr(M_H>=a)).")
row("term-walk-identity-L07", "2.4 notation/terms (term used before definition; attribution to Lesson 6)",
    "course/modules/SC/SC1/L07.html:353 (pre.expected, 'Part A: walk identity (maximum >= a) = ...'); L07.html:204 and :223 and :236 (code mirrored from the twin); tests/labs/SC1/lab-SC1-L07-1.py:54 (docstring 'By the walk identity'), :73 (docstring 'Check the walk identity by enumeration'), :86 (print 'walk identity')", "FAIL",
    "Round 7 FAIL is partly fixed: the prose of L07 (L07.html:51, :150) now calls the result the 'discrete tail identity of Lesson 6' (Corollary 1.4 at L06.html:87) and no longer attributes 'walk identity' to Lesson 6. But the printed output label, the expected block and the twin/page docstrings still say 'walk identity', a name that L07 never defines. The name is defined only later, as the title of Proposition 2.2 in L08 (L08.html:121). The reader sees the printed label before any definition.",
    "Rename the L07 labels to the Lesson 6 name: in tests/labs/SC1/lab-SC1-L07-1.py change the docstrings at lines 54 and 73 and the print at line 86 from 'walk identity' to 'discrete tail identity of Lesson 6' (and the mirrored lines in the L07 code block), then re-embed with tools/embed_labs.py course/modules/SC/SC1/L07.html --refresh lab-SC1-L07-1 so the expected block at L07.html:353 is regenerated, and re-run run_labs --unit SC1. Builder-owned: the lesson and twin are not edited by the verifier.")
row("dag-reflection-link-L07-L08", "2.9 DAG and prose (concept link names the result the sentence cites)",
    "course/modules/SC/SC1/L07.html:37 and course/modules/SC/SC1/L08.html:37 (meta 'Uses' lists)", "PASS",
    "Round-7 FAIL fixed: the reflection identity is now a plain link to L06.html#s2 ('Theorem 2.5 of Lesson 6'), with no reflection-principle concept link (the concept of L06 Definition 2.2 is the path-level statement, which these pages do not use). Re-verified against L06.html:117-120 and :152-171.")
row("structure-why-it-matters-word-cap", "2.9 structure (why it matters: at most 120 words, BUILDER_RULES 4.2 item 1)",
    "course/modules/SC/SC1/L07.html:51; course/modules/SC/SC1/L08.html:51", "PASS",
    "Round-7 FAIL fixed. Current text: 117 whitespace tokens in each page (including math); 110 outside math in each; alphabetic words 96 (L07) and 100 (L08). Round 7 counted 122 (L07) and 121 (L08) on the old text; a whitespace split of the old L07 text gives 120, so the old text was at the limit under that count. On the new text every counting method tried is at most 120.")

# ---- new rows for round-8 subjects ----
row("delta-round8-hunks", "1 inventory (delta since round-7 pin 06994db)",
    "course/modules/SC/SC1/L07.html (20 lines), L08.html (14), cards.json (c149, c150, c055-c056 out of slice, c166 removed, c205 added), tests/labs/SC1/lab-SC1-L07-1.py (10), lab-SC1-L08-1.py (6)", "PASS",
    "git diff 06994db 0dee921 for the slice (L07 and L08 pages, both twins, cards.json). L07: the reflection citation in the meta line (now plain Theorem 2.5 of Lesson 6), the why-it-matters sentence (Lab 1 wording), the Lab 1 hypothesis (discrete tail identity), the Part A docstring, the E2 solution wording, and the key-results row. L08: the meta line, the why-it-matters sentence, the section 2 wording (exact integers), the lab docstring, and the M3 prompt. Cards: c149 and c150 backs, c166 removed, c205 added (other changed cards are outside slice c). Every changed subject was re-verified from fresh evidence; no row was carried.")
row("cards-c205-new", "2.7 cards (new card SC1-c205)",
    "course/modules/SC/SC1/cards.json SC1-c205 (L08)", "PASS",
    "Corollary 1.3 hypotheses and both equalities checked against L08.html:63-81 (Proposition 1.2 and Corollary 1.3) and L07.html:68-82 (Theorem 1.3); P(tau<=H)=P(M_H>=a)=2(1-Phi(a/sqrt H))=erfc(a/sqrt(2H)); grade T; Proposition 1.2 needs no probability assumption (true).")
row("defs-numbering-L08", "2.9 structure (numbering of definitions, propositions, corollaries)",
    "course/modules/SC/SC1/L08.html:58, :63, :77, :87, :97, :107, :116, :121, :131", "PASS",
    "Definition 1.1 appears once in L08 (first-passage time; the L01 block printed by grep is in L01); Proposition 1.2, Corollaries 1.3, 1.4, 1.5 and Remark 1.6 in §1; Definition 2.1, Propositions 2.2, 2.3 in §2. No number is used twice.")
row("notation-star-superscript-L08", "2.4 notation (superscript star in L08)",
    "course/modules/SC/SC1/L08.html (s^\\ast, k^\\ast; 19 occurrences of \\ast); notation/notation.json (R^\\ast, x^\\ast entries)", "PASS",
    "L08 uses the star only as a marker for a maximiser (s^\\ast in Proposition 1.2 and its proof, k^\\ast in Proposition 2.2). The registered symbols R^\\ast and R^{e\\ast} (notation.json, AP1) are not used in SC1, and x^\\ast is AP1's symbol, not SC1's. No registered symbol is given a second meaning; noted, not a collision.")
row("notation-n-steps-L08", "2.4 notation (local convention, plan section 2.3)",
    "course/modules/SC/SC1/L08.html §2 and lab (n for walk length); L07.html Part A (N for walk length)", "PASS",
    "The plan's convention (N for a number of steps, n for a grid index) is not followed in L08's lab and §2, which use n for walk length. No collision: n is never a grid index in SC1-c and N is the truncation in Proposition 2.3. Observation only.")
row("scope-words-full-scan-r8", "2.4 scope (every, all, always, never, any, surely, exactly, only) full sentence scan",
    f"course/modules/SC/SC1/L07.html, L08.html (prose, outside pre blocks); {S}", "PASS",
    "Scripted scan of every sentence containing a scope word in both pages (prose and solutions, outside pre blocks), each mapped to a computation or a proof: 'every continuous path' (Prop 1.2, proved per path), 'every grid time' (Prop 2.2(b), proved), 'every step sequence' and '90114 pairs' (enumerated), 'for every real a' (Cor 2.3 inclusion, proved), 'almost surely' (only in a negative sentence, L07.html:376). No unsupported scope claim found.")
row("dag-plain-bias-L08", "2.9 DAG (plain-English 'bias' in L08)",
    "course/modules/SC/SC1/L08.html:461", "PASS",
    "The single occurrence of 'bias' is plain English ('it cannot show a bias either way'), not the S1 concept estimator-bias-variance. No concept use; noted.")
row("terms-used-before-defined-L07-L08", "2.4 terms used before definition (full scan)",
    "course/modules/SC/SC1/L07.html, L08.html", "PASS",
    "Checked: 'discretely monitored maximum' (why-it-matters points to Definition 2.1); 'Assumption A5' (forward reference 'stated below' in Corollary 1.5, then stated); 'simple random walk' (L06 dfn); 'first-passage index' (Definition 2.1 of L08, used in Remark 1.6 with a forward pointer); 'walk identity' (L08 Proposition 2.2 title; undefined in L07 - see term-walk-identity-L07). Only the L07 instance fails.")
row("term-walk-identity-L08", "2.4 terms (consistency of 'walk identity' within L08)",
    "course/modules/SC/SC1/L08.html:121 (Prop 2.2 title), :142, :364, :418 (M3 solution), :433 (P2 title), :511; tests/labs/SC1/lab-SC1-L08-1.py:51, :88, :102", "PASS",
    "In L08 the name is defined at Proposition 2.2 (its title, before any use) and used consistently for that count identity. The M3 prompt (L08.html:416) says 'discrete tail identity of Lesson 6' and its solution says 'The walk identity gives'; the two names refer to the same identity (Corollary 1.4 of Lesson 6 and Proposition 2.2 here). Not a defect in meaning; recorded as an observation for the builder.")
row("cards-no-A5-L05-lesson-scope", "2.7 cards (assumption labels cite the right lesson)",
    "cards.json SC1-c149, SC1-c150, SC1-c174 and others citing A3/A4/A5", "PASS",
    "Every card in slice c that cites an assumption names A3 and A4 of Lesson 5 correctly; the one exception (A5 attributed to Lesson 5 on c150) is reported under cards-basis-A3-dependence. Cards outside slice c were not reviewed for this row.")
row("freshness-L07-L08", "2.1 freshness (2025-2026 work for a debate brief)",
    "course/modules/SC/SC1 (L07, L08)", "PASS",
    "No debate key in SC1 (curriculum 03-markets.yaml:505-512, plan section 0.1). The results are classical; no 2025-2026 flag raised.")

# ---- the card-basis row: the subject changed, FAIL with the new evidence ----
row("cards-basis-A3-dependence", "2.7 cards (closed-form cards name the A3/A4 dependence)",
    "course/modules/SC/SC1/cards.json: SC1-c149 (back), SC1-c150 (back)", "FAIL",
    "Round-7 defect fixed for SC1-c149 (back now reads 'against the closed form 0.3173 of Theorem 1.3 (assuming A3 and A4 of Lesson 5)'). SC1-c150 back now reads '... the value of E[M_H] at H=1 from Corollary 1.5(b) (assuming A3, A4 and A5 of Lesson 5)'. Assumption A5 is not a Lesson 5 assumption: it is defined in L07 as 'Assumption A5 (tail formula for a nonnegative variable)' (course/modules/SC/SC1/L07.html:97-99, 'of this lesson'). Lesson 5 defines only A1-A4 (grep of L05.html).",
    "In course/modules/SC/SC1/cards.json, SC1-c150 back: replace 'assuming A3, A4 and A5 of Lesson 5' with 'assuming A3 and A4 of Lesson 5 and A5 of this lesson (Lesson 7)'. Builder F owns cards.json; the verifier does not edit it.")

# ---- mutants: none (no grader in this slice; lab twins are not mutation-tested) ----

fragment = {
    "unit": "SC1",
    "slice": "c",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-c (L07, L08, lab twins), round 8; did not build SC1",
    "pin": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3",
    "base": "06994db16d1ab449bcf29898a7f56cfa999dce57 (round-7 pin; round-7 fragment /Users/billyribeiro/.fanout/frags/E-SC1-c.round7.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE8-SC1-c (detached at 0dee921; .venv symlinked)",
    "scratch": "ledgers/SC1/scripts/SC1-c-r8/out/",
    "verified_at": "2026-11-05T02:10:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since the round-7 pin 06994db for this slice: course/modules/SC/SC1/L07.html, L08.html, tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py, and cards.json (c149, c150 changed; c166 removed; c205 added; c055 and c056 are L03 and out of slice). Every hunk read. All rows were re-verified from fresh evidence at 0dee921; no row was carried.",
        "Every L07 and L08 line of prose, every printed line of the two expected blocks, all 47 cards of the slice, and both twins were read in full. The page code blocks were checked byte-for-byte by run_labs.",
        "Re-derivations: ledgers/SC1/scripts/SC1-c-r8/indep_r8.py (output out/indep_r8.txt) recomputes every printed number and every quoted closed-form value by independent code (DP, brute force, Simpson, erfc/erf, absorbing DP); dup_scan.py (output out/dup_scan.txt) checks duplicates on cards.json; make_fragment.py writes this fragment.",
        "Mutants: none. This slice has no grader; lab twins are demonstrations and are not mutation-tested (FINAL-ARCHITECT-RULINGS 9; verifier rulings). tools/mutate_graders.py was not run for this slice.",
        "Two FAIL rows, both low severity and wording/attribution-level: term-walk-identity-L07 (a term undefined in L07 appears in the printed lab label and docstrings) and cards-basis-A3-dependence (card SC1-c150 attributes Assumption A5 to Lesson 5; A5 is Lesson 7's). No mathematical, numerical, lab-output or grade defect was found.",
        "Not checked in this slice: L01-L06 and the project, the grader, the hub index, and the other cards (outside slice c), except the cross-references L07/L08 make to them; the whole-registry verify_refs run (only the unit's live run and the offline integrity run were made); render_curriculum, build_site, fetch_data, check_projects, run_graders and mutate_graders (not in slice c); pytest over the whole suite (only the lab and page-check subset was run). page_smoke was run only for L07 and L08 (alone), as the slice requires.",
        "The lab labels 'walk identity' inside L08 are consistent with that page's Proposition 2.2 name; recorded as an observation (term-walk-identity-L08), not a FAIL.",
        "Observation only: the plan's convention (N for steps, n for grid index) is not followed in L08's section 2 and lab, where n is the walk length; no notation.json collision results (notation-n-steps-L08).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "mutants_killed": 0,
        "mutants": 0,
        "top_failures": [
            "term-walk-identity-L07: 'walk identity' printed in L07 Lab 1 Part A output (L07.html:353) and in twin docstrings (lab-SC1-L07-1.py:54, :73, :86) is undefined on L07; L07 prose says 'discrete tail identity'. Fix: rename and --refresh the embed.",
            "cards-basis-A3-dependence: card SC1-c150 cites 'A5 of Lesson 5'; A5 is Lesson 7's Assumption A5. Fix: 'A3 and A4 of Lesson 5 and A5 of this lesson'.",
        ],
    },
}

# Keep the round-7 row ids: every id of the previous fragment must be present.
previous = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-SC1-c.round7.json").read_text())
prev_ids = [r["id"] for r in previous["rows"]]
now_ids = {r["id"] for r in rows}
missing = [i for i in prev_ids if i not in now_ids]
assert not missing, f"round-7 ids missing: {missing}"
assert len(now_ids) == len(rows), "duplicate row id in round 8"

(ROOT / "ledgers/SC1/SC1-c.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", fragment["summary"]["pass"], "fail", fragment["summary"]["fail"])
