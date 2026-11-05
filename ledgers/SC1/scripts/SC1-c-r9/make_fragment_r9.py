"""Writes the round-9 fragment ledgers/SC1/SC1-c.json (SC1 slice c: L07, L08, lab twins). Run from the checkout root."""

from __future__ import annotations

import json
from pathlib import Path

S = "ledgers/SC1/scripts/SC1-c-r9/out/"
GATES = "Round 9 (pin c93dd52): "

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---- gates and tooling (re-run this round) ----
row(
    "gate-check-pages",
    "2.9 structure (check_pages)",
    "course/modules/SC/SC1/L07.html, L08.html",
    "PASS",
    GATES + ".venv/bin/python tools/check_pages.py --unit SC1 --page L07 and --page L08 -> 'check_pages SC1 L07: PASS' and "
    "'check_pages SC1 L08: PASS' (" + S + "check_pages_L07.txt, check_pages_L08.txt).",
)
row(
    "gate-check-dag",
    "2.9 DAG (check_dag)",
    "course/modules/SC/SC1/L07.html, L08.html",
    "PASS",
    GATES + ".venv/bin/python tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS' (" + S + "check_dag_SC1.txt).",
)
row(
    "gate-run-labs",
    "2.5 labs (run_labs)",
    "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py",
    "PASS",
    GATES + ".venv/bin/python tools/run_labs.py --unit SC1 -> 'run_labs SC1: PASS (11/11)', exit 0 (" + S + "run_labs_SC1.txt).",
)
row(
    "lab-L07-twin-isolated",
    "2.5 labs (twin under python -I -W error)",
    "tests/labs/SC1/lab-SC1-L07-1.py",
    "PASS",
    GATES + "ledgers/SC1/scripts/SC1-c-r9/lab_equivalence.py copies the twin to a fresh temporary directory and runs "
    "python -I -W error on it: exit 0, stderr 0 bytes, stdout equal to the page's expected block (" + S + "lab_equivalence.txt).",
)
row(
    "lab-L08-twin-isolated",
    "2.5 labs (twin under python -I -W error)",
    "tests/labs/SC1/lab-SC1-L08-1.py",
    "PASS",
    GATES + "same procedure via lab_equivalence.py: exit 0, stderr 0 bytes (" + S + "lab_equivalence.txt).",
)
row(
    "lab-L07-page-equals-twin",
    "2.5 labs (embed: page code equals twin)",
    "course/modules/SC/SC1/L07.html:151-356 vs tests/labs/SC1/lab-SC1-L07-1.py",
    "PASS",
    GATES + "lab_equivalence.py: the html-unescaped data-run block equals the twin after the trailing newline that run_labs "
    "also strips (run_labs.py:74-75); result True (" + S + "lab_equivalence.txt). The delta hunk at twin :51-54 and :74-88 is embedded.",
)
row(
    "lab-L08-page-equals-twin",
    "2.5 labs (embed: page code equals twin)",
    "course/modules/SC/SC1/L08.html:143-343 vs tests/labs/SC1/lab-SC1-L08-1.py",
    "PASS",
    GATES + "lab_equivalence.py: equal after trailing-newline normalisation, result True (" + S + "lab_equivalence.txt).",
)
row(
    "lab-L07-expected-equals-output",
    "2.5 labs (expected block equals output)",
    "course/modules/SC/SC1/L07.html:357-379 (pre.expected)",
    "PASS",
    GATES + "the expected block equals the twin's stdout (lab_equivalence.py, True). The renamed Part A line "
    "'discrete tail identity of Lesson 6' is in both (L07.html:357, twin :88).",
)
row(
    "lab-L08-expected-equals-output",
    "2.5 labs (expected block equals output)",
    "course/modules/SC/SC1/L08.html:344-363 (pre.expected)",
    "PASS",
    GATES + "lab_equivalence.py: expected block equals twin stdout, True (" + S + "lab_equivalence.txt).",
)
row(
    "lab-L07-printed-numbers",
    "2.2 numbers (a) lab-computed, recomputed independently",
    "course/modules/SC/SC1/L07.html:357-379",
    "PASS",
    GATES + "ledgers/SC1/scripts/SC1-c-r9/indep_r9.py recomputes every printed value by a different algorithm: Part A tails by a "
    "killed-walk DP (0.375000, 0.332306, 0.321084, 0.318255, 0.317547); the identity holds for 78 pairs; Part B nesting violations 0, "
    "proportions 0.2275/0.2675/0.2825/0.3025, SEs 0.0210/0.0222/0.0225/0.0230 (regenerated with the same RNG draw order, "
    "same counts 91/107/113/121); Part C means and SEs 0.5546/0.6639/0.7232/0.7586, SEs 0.0315-0.0317; Part D 0.1586552539 by "
    "erfc and by Simpson (" + S + "indep_r9.txt).",
)
row(
    "lab-L08-printed-numbers",
    "2.2 numbers (a) lab-computed, recomputed independently",
    "course/modules/SC/SC1/L08.html:344-363",
    "PASS",
    GATES + "indep_r9.py: 1588 = 512+384+288+224+180 (DP first passage), 4096, 794 = #{S_12>=3} by binomials; P(nu_3<=12)=0.387695, "
    "P(S_12>=3)=0.193848; sum 2^n = 8190 and sum n 2^n = 90114; E[min(nu_1,N)] = 5.480560303, 11.815731233, 24.557203397 "
    "(exact Fraction DP; 179587/32768 equal); z = -1.0466, -0.6866, -0.7748 from a regenerated 1000-walk sample; Part D 0.317310508, "
    "0.241970725, 0.479500122, 0.109847822 and central differences equal (" + S + "indep_r9.txt).",
)
row(
    "lab-L07-hypothesis-interpretation",
    "2.5 lab statements (hypothesis and interpretation match output)",
    "course/modules/SC/SC1/L07.html:150 (hypothesis) and :380 (interpretation)",
    "PASS",
    GATES + "every sentence checked against the printed lines: five decreasing tails; 91/107/113/121 counts; gaps 0.0898/0.0498/0.0348/0.0148; "
    "finest gap 0.0393 = 1.24 SE (text says 1.2); 2 x 0.1586552539 = 0.3173105078. Observation, not a defect: the hypothesis says the last "
    "Part A tail 'is compared' with 2(1-Phi(1)); the lab prints no such comparison in Part A, and the comparison is made in the "
    "interpretation at L07.html:380, which names the closed form and its hypotheses.",
)
row(
    "lab-L08-hypothesis-interpretation",
    "2.5 lab statements (hypothesis and interpretation match output)",
    "course/modules/SC/SC1/L08.html:142 (hypothesis) and :364 (interpretation)",
    "PASS",
    GATES + "each printed statement matched: 8190 and 90114; 78 of 78 pairs; first-passage counts zero at even steps (S_k parity); "
    "1588 = 2 x 794; z values -1.05, -0.69, -0.77 and 'less than 1.1 SE'; Part D values.",
)
row(
    "lab-simulated-labels-seeds",
    "2.5 labs (seeds; SIMULATED labels)",
    "course/modules/SC/SC1/L07.html:148-149; L08.html:141; tests/labs/SC1/lab-SC1-L07-1.py:32; lab-SC1-L08-1.py:37",
    "PASS",
    GATES + "L07 SEED = 20260507 (twin :32) and L08 SEED = 20260508 (twin :37), both through random.Random(SEED). L07 heading "
    "'(Parts B and C SIMULATED)' and Part B header 'SIMULATED'; L08 heading '(Part C SIMULATED)' and Part C header 'SIMULATED'. Exact parts "
    "carry no label, and they use no random draws (twin docstrings).",
)
row(
    "lab-runtime",
    "2.5 labs (runtime under 10 s)",
    "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py",
    "PASS",
    GATES + "tools/page_smoke.py --unit SC1 --pages L07 L08 (run alone): lab-SC1-L07-1 0.1 s, lab-SC1-L08-1 0.2 s in Pyodide (" + S + "page_smoke_L07_L08.txt).",
)
row(
    "lint-mypy-twins",
    "code quality (ruff, mypy strict)",
    "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py",
    "PASS",
    GATES + "ruff check on both twins: 'All checks passed!'; ruff format --check: '2 files already formatted'; mypy --no-incremental on both "
    "twins: 'Success: no issues found in 2 source files' (" + S + "ruff_check_twins.txt, mypy_twins.txt). Whole-repo ruff/mypy not run "
    "(no file outside the two twins changed in this slice).",
)
row(
    "page-smoke-L07-L08",
    "2.9 page_smoke (console, math, 360 px, labs in Pyodide)",
    "course/modules/SC/SC1/L07.html, L08.html",
    "PASS",
    GATES + "tools/page_smoke.py --unit SC1 --pages L07 L08, run alone: 'page_smoke modules/SC/SC1/L07.html: PASS', "
    "'page_smoke modules/SC/SC1/L08.html: PASS', 'page_smoke SC1: PASS' (" + S + "page_smoke_L07_L08.txt).",
)
row(
    "pytest-lab-tools",
    "2.5 labs (pytest, tooling)",
    "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
    "PASS",
    GATES + "pytest -q on the three files with -k 'SC1 or run_labs or page_checks or lab': 100% dots, exit 0 (" + S + "pytest_lab_tools.txt).",
)
row(
    "verify-refs-offline",
    "2.1 citations (integrity, offline)",
    "references/references.json",
    "PASS",
    GATES + ".venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (" + S + "verify_refs_offline.txt).",
)
row(
    "verify-refs-live-SC1",
    "2.1 citations (live, unit SC1)",
    "references/references.json entry shreve2004stochastic (line 20732); L07.html:618; L08.html:601",
    "PASS",
    GATES + "tools/verify_refs.py --unit SC1 (live) -> 'live re-verification of SC1: 1 of 560 entries, 0 problems' (" + S + "verify_refs_SC1_live.txt). "
    "references/ and tools/ are unchanged between 0dee921 and c93dd52 (git diff empty).",
)
row(
    "refs-no-citation-markup",
    "2.1 attribution (no unread citation)",
    "course/modules/SC/SC1/L07.html:616-618, L08.html:599-601",
    "PASS",
    GATES + "grep -c data-cite = 0 in both pages; each References section states that no passage is cited from shreve2004stochastic "
    "and gives no locator. The only claim that uses a source is the curriculum's own book-level attribution.",
)

# ---- grades and mathematics ----
row(
    "claim-grades-L07",
    "2.3 grades (re-graded against BLUEPRINT section 3)",
    "course/modules/SC/SC1/L07.html:68-134, 515-531",
    "PASS",
    GATES + "Theorem 1.3, Corollary 1.5, Proposition 2.2, Corollary 2.3 are T and have complete proofs (read in full). Remark 1.4 and "
    "Remark 2.4 are unmarked proof-level remarks. Lab-computed and enumerated results are C with the lab named. The key-results table grades "
    "agree with the sections.",
)
row(
    "claim-grades-L08",
    "2.3 grades (re-graded against BLUEPRINT section 3)",
    "course/modules/SC/SC1/L08.html:63-121, 499-517",
    "PASS",
    GATES + "Proposition 1.2, Corollaries 1.3, 1.4, 1.5 and Propositions 2.2, 2.3 are T with proofs read in full; enumerated and "
    "simulated results are C; key-results grades match.",
)
row(
    "math-L07-thm-1.3",
    "2.4 mathematics (Theorem 1.3 and proof)",
    "course/modules/SC/SC1/L07.html:68-80",
    "PASS",
    GATES + "2(1-Phi(a/sqrt H)) = erfc(a/sqrt(2H)) re-derived (erfc(x/sqrt2) = 2(1-Phi(x)), with x = a/sqrt H); the proof's standard-normal "
    "step has no atoms; the Lesson 6 Theorem 2.5 hypothesis (A3, A4) is named.",
)
row(
    "math-L07-cor-1.5b",
    "2.4 mathematics (Corollary 1.5(b))",
    "course/modules/SC/SC1/L07.html:101-107",
    "PASS",
    GATES + "Integration by parts: int_0^R (1-Phi) = R(1-Phi(R)) + phi(0) - phi(R); 0 <= R(1-Phi(R)) <= phi(R) via v/R >= 1; limit "
    "1/sqrt(2 pi) (indep_r9.py: 1/sqrt(2pi) = 0.3989422804). Substitution m = sqrt(H) u gives 2 sqrt(H) times the integral, "
    "so E[M_H] = 2 sqrt(H)/sqrt(2 pi) = sqrt(2H/pi) (line 107). Card SC1-c140 omits the factor: see cards-c140-substitution.",
)
row(
    "math-L07-prop-2.2-cor-2.3-remark-2.4",
    "2.4 mathematics (Prop 2.2, Cor 2.3, Remark 2.4)",
    "course/modules/SC/SC1/L07.html:119-146",
    "PASS",
    GATES + "Prop 2.2(b): s_k = kH/N = (kc)H/N' with N' = cN, so the N-grid is a subset of the N'-grid (checked numerically: "
    "indep_r9.py nesting violations 0 on 400 paths). Cor 2.3 inclusion holds for every real a. Remark 2.4: M^(1) = max(0,B_H), "
    "and {max(0,B_H) >= a} = {B_H >= a} for a > 0.",
)
row(
    "math-L07-def-2.1-grid-times",
    "2.4 mathematics (notation and definition)",
    "course/modules/SC/SC1/L07.html:116",
    "PASS",
    GATES + "s_k = kH/N, k = 0..N, and M^(N)_H = max_k B_{s_k}; consistent with the twin's grid_maximum (stride FINE // n, n + 1 points).",
)
row(
    "math-L07-remark-1.4-phi0",
    "2.4 mathematics (Remark 1.4)",
    "course/modules/SC/SC1/L07.html:83-86",
    "PASS",
    GATES + "a/sqrt H -> infinity as H -> 0 and -> 0 as H -> infinity; Phi(0) = 1/2 by evenness; Pr(Z >= 0) + Pr(Z <= 0) = 1 with no atoms.",
)
row(
    "math-L07-R1-R3-P2-P3-M-E",
    "2.4 mathematics (problem solutions)",
    "course/modules/SC/SC1/L07.html:417-512",
    "PASS",
    GATES + "All M1-M3, P1-P3, E1-E3, R1-R3 read with solutions. M1: a/sqrt H = 1, erfc(2/sqrt 8) = erfc(1/sqrt 2) (value 0.31731050786). "
    "E2: 14893 + 6885 = 21778 = 21778/2^16 = 0.332306 (indep_r9.py). E3: sqrt(121*279/(400^2*399)) = 0.022996, printed 0.0230 (indep_r9.py). "
    "R1: Pr = 1 for a <= 0 and the form exceeds 1 for a < 0. R2: continuity from below. R3: tau_a <= H iff M_H >= a on continuous paths (Lemma 2.1(i) of Lesson 6).",
)
row(
    "math-L08-prop-1.2-cor-1.3-1.4",
    "2.4 mathematics (Prop 1.2, Cor 1.3, Cor 1.4)",
    "course/modules/SC/SC1/L08.html:63-94",
    "PASS",
    GATES + "Prop 1.2 both inclusions re-derived (IVT on [0, s*] with B_0 = 0 < a; closed set {s: B_s = a}). Cor 1.3 chain cites Prop 1.2, "
    "Lesson 7 Theorem 1.3 and Lesson 6 Corollary 2.6 correctly. Cor 1.4: union of increasing events {tau_a <= n}; limit 2(1-1/2) = 1.",
)
row(
    "math-L08-cor-1.5",
    "2.4 mathematics (Corollary 1.5, density)",
    "course/modules/SC/SC1/L08.html:97-104",
    "PASS",
    GATES + "F(H) = 2(1-Phi(a H^{-1/2})); F'(H) = a H^{-3/2} phi(a H^{-1/2}) = a e^{-a^2/(2H)}/(sqrt(2 pi) H^{3/2}) (re-derived); "
    "F(0+) = 0; numeric check: indep_r9.py central differences equal the density to 1e-9 at H = 1 and 2.",
)
row(
    "math-L08-prop-2.2-2.3",
    "2.4 mathematics (Prop 2.2, 2.3)",
    "course/modules/SC/SC1/L08.html:120-138",
    "PASS",
    GATES + "Prop 2.2: first index with S_k >= a equals a since steps are +-1 (indep_r9.py: first-passage total equals the killed-walk max count for all 78 (n,a) pairs). "
    "Prop 2.3: min(nu, N) = sum of indicators; P(nu > k) = integer/2^k (killed-walk DP, indep_r9.py).",
)
row(
    "math-L08-R3",
    "2.4 mathematics (Problem R3)",
    "course/modules/SC/SC1/L08.html:489-495",
    "PASS",
    GATES + "log f_a(H) derivative (a^2 - 3H)/(2H^2) re-derived; mode H = a^2/3 (indep_r9.py grid search: argmax 0.3333 for a = 1).",
)
row(
    "math-L08-R1-R2",
    "2.4 mathematics (Problems R1, R2)",
    "course/modules/SC/SC1/L08.html:476-497",
    "PASS",
    GATES + "R1: #{nu <= N} = #{S_N >= a} + #{S_N > a} = 2#{S_N >= a} - #{S_N = a} re-derived; 1588 = 2 x 794 (indep_r9.py). "
    "R2: min(nu,N+1) - min(nu,N) = 1{nu > N}.",
)
row(
    "prob-L08-all",
    "2.4 problems (all L08 problems, solutions)",
    "course/modules/SC/SC1/L08.html:392-497",
    "PASS",
    GATES + "Every L08 problem read with its solution. M1 0.317311 (2(1-Phi(1)) = 0.31731050786), M2 f_1(1) = 0.2419707 (indep_r9.py 0.2419707245), "
    "M3 5/8 (listing and walk identity), E1 parity, E2 z values, E3 0.109848 (indep_r9.py 0.109847822; from printed factors 0.109847654). "
    "Proof problems P1-P3 re-derived.",
)
row(
    "prob-L07-remaining",
    "2.4 problems (other L07 problems)",
    "course/modules/SC/SC1/L07.html:411-512",
    "PASS",
    GATES + "All L07 problems M1-M3, P1-P3, E1-E3, R1-R3 read with solutions; the round-9 delta additions 'Assuming A3 and A4' "
    "(P1 :443, E1 :470) match their hypotheses (Corollary 1.5(a) uses H2 = A3, A4). Printed numbers match indep_r9.py.",
)
row(
    "misconceptions-L07-content",
    "2.4 misconceptions (content)",
    "course/modules/SC/SC1/L07.html:392-408",
    "PASS",
    GATES + "Three misconceptions, each correct: 2x tail (0.3173105 and 0.1586553 to seven decimals; difference equals P(B_1 >= 1) by reflection); "
    "grid tail below closed form (Prop 2.2(a), Cor 2.3, printed 0.2275 and 0.3025 below 0.3173105); normal one-time marginals (Lemma 2.1 needs continuity).",
)
row(
    "misconceptions-L08-content",
    "2.4 misconceptions (content)",
    "course/modules/SC/SC1/L08.html:379-391",
    "PASS",
    GATES + "Three misconceptions: finite on every path (probability vs outcome, Cor 1.4); first passage equal to terminal value (factor 2; "
    "0.317311 vs 0.1586552539; walk ratio 1588/794 = 2 with parity); finiteness implies finite mean (no moment evaluated, truncated means increase).",
)
row(
    "canon-breaks-L07-L08",
    "2.4 canon breaks",
    "course/modules/SC/SC1/L07.html:383-390; course/modules/SC/SC1/L08.html:367-374",
    "PASS",
    GATES + "Each lesson names a hypothesis whose failure breaks the result. L08 jump example re-checked: path 0 on [0,1/2), 2 from 1/2 on gives "
    "M_1 = 2 >= 1 and never equals 1, so tau_1 = infinity. L07 names continuity, A3/A4 conditionality, and the grid-vs-continuous gap.",
)
row(
    "key-results-L07",
    "2.4 key-results table",
    "course/modules/SC/SC1/L07.html:515-531",
    "PASS",
    GATES + "Each row's grade and source checked against the sections; the enumeration row (C, 78 pairs) and the simulated rows (C, one seed) match Lab 1.",
)
row(
    "key-results-L08",
    "2.4 key-results table",
    "course/modules/SC/SC1/L08.html:499-517",
    "PASS",
    GATES + "Each row's grade and source checked; the 90114-pair row is C (Lab 1, Part A); the 1.1-SE row is C (Lab 1, Part C; z values -1.05, -0.69, -0.77).",
)
row(
    "quiz-L07",
    "2.9 quiz (keys, tolerances, explanations)",
    "course/modules/SC/SC1/L07.html:535-614",
    "PASS",
    GATES + "10 items, each with an explanation. Keys: Q2 0.3173105 vs 0.31731050786 (diff 7.9e-9, tol 1e-6); Q4 0.158655 vs 0.1586552539 "
    "(diff 2.5e-7, tol 1e-6); Q6 0.797885 vs 0.79788456 (diff 4.4e-7, tol 1e-6); Q8 0.3173105 (diff 7.9e-9). Q5 P(M_H<=0)=0 and Q9 are correct.",
)
row(
    "quiz-L08",
    "2.9 quiz (keys, tolerances, explanations)",
    "course/modules/SC/SC1/L08.html:518-597",
    "PASS",
    GATES + "10 items, each with an explanation. Q2 0.3173105 (diff 7.9e-9); Q3 0.625 exact (5/8); Q5 5.48056 tol 1e-5 vs 179587/32768 = "
    "5.4805603 (diff 3e-7); Q6 0.241971 tol 1e-6 vs 0.24197072 (diff 3e-7). Q7 'no mean' and Q9 jump example are correct.",
)
row(
    "structure-L07",
    "2.9 structure and prose (template sections)",
    "course/modules/SC/SC1/L07.html",
    "PASS",
    GATES + "Order: why-it-matters (117 whitespace tokens including math, 110 outside math; at most 120 words), s1, s2 with inline lab, "
    "canon-breaks, misconceptions (3), problems (3 per tier: mechanics, proof, empirical, research), key-results, quiz (10 items), references. "
    "data-hours 9; hub split 72 + 28 (index.html:29, and the hub statement at :150). check_pages PASS.",
)
row(
    "structure-L08",
    "2.9 structure and prose (template sections)",
    "course/modules/SC/SC1/L08.html",
    "PASS",
    GATES + "Same order; why-it-matters 117 tokens (110 outside math); misconceptions (3); problems 3 per tier; quiz 10 items; "
    "references; data-hours 9. check_pages PASS.",
)
row(
    "banned-and-process-words",
    "2.9 banned phrases and process words",
    "course/modules/SC/SC1/L07.html, L08.html; tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py",
    "PASS",
    GATES + "grep (case-insensitive) for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, "
    "it is important to note, studies show, experts agree, it is well known, obviously, clearly, and ellipses: 0 hits in both pages and twins. "
    "Process words (builder, verifier, round, fixer, planner, architect, ruling, REQUEST, plan): no hit except 'rounded'/'Rounding rule' (rounding, not a process word).",
)
row(
    "notation-macros",
    "2.4 notation (notation.json)",
    "course/modules/SC/SC1/L07.html, L08.html",
    "PASS",
    GATES + "Macros on the pages: \\Prob, \\E, \\indic, \\Normal (registered in notation/notation.json macros); \\Phi (registered symbol: standard "
    "normal CDF, the meaning used); \\varphi used only for the Gaussian density (L07 :104-107; L08 :103); tau_a and nu_a are local. "
    "\\se is registered but does not occur on these pages.",
)
row(
    "dag-defined-once-L07-L08",
    "2.9 DAG (defined once)",
    "course/modules/SC/SC1/L07.html:64, :116; course/modules/SC/SC1/L08.html:59",
    "PASS",
    GATES + "dfn: running-maximum-distribution once (L07:64, data-concept); first-passage-time once (L08:59, data-concept); "
    "discretely monitored maximum (L07:116) is a plain dfn with no data-concept (allowed by plan 2.1 item 5).",
)
row(
    "dag-outside-closure",
    "2.9 DAG (outside the prerequisite closure)",
    "course/modules/SC/SC1/L07.html:37, L08.html:37 (meta links)",
    "PASS",
    GATES + "Concept links are brownian-motion (L01), brownian-motion-construction (L02), normal-distribution, random-variable, expectation "
    "(M4/M6, in the closure), running-maximum-distribution (L07), first-passage-time (L08, own). No SC2-SC5 or outside-closure concept is linked. check_dag PASS.",
)
row(
    "xref-L01-L05-L06",
    "2.1 cross references (Lessons 1, 5, 6)",
    "course/modules/SC/SC1/L07.html, L08.html; L06.html:54-99, 100-175; L05.html:56-66, 268-289; L01.html:58-68",
    "PASS",
    GATES + "Lesson 6 Corollary 1.4 (discrete tail identity, L06:87-99) matches the lab identity; Theorem 2.5 (L06:153-171), Corollary 2.6 "
    "(L06:174), Lemma 2.1 (L06:105-115) and tau_a (L06:102) match the cites; Lesson 5 A3 (L05:271-281) and A4 (L05:59-66) with the sketch only for A3; "
    "Lesson 1 Definition 1.1 (D1)-(D3) (L01:58-68) for B_H ~ N(0,H).",
)
row(
    "cards-dup-and-numbers",
    "2.7 cards (duplicates; numbers appear in lesson)",
    "course/modules/SC/SC1/cards.json (205 cards)",
    "PASS",
    GATES + "ledgers/SC1/scripts/SC1-c-r9/dup_scan_r9.py over all 205 cards: ids unique; no exact duplicate front or back; same-lesson near-duplicate "
    "fronts (Jaccard >= 0.6) checked: in this slice SC1-c170 and SC1-c218 share wording but ask different counts (90114 pairs vs 78 pairs), "
    "and c138/c139/c146/c157 and c164/c165 test different results (output " + S + "dup_scan_r9.txt). Every card number in the slice appears in its lesson or expected block.",
)
row(
    "cards-L07-L08-full-read",
    "2.7 cards (full read of all L07 and L08 cards)",
    "cards.json: L07 cards SC1-c134..c159, c191, c215 (25); L08 cards SC1-c161..c183, c201, c205, c218 (23)",
    "PASS",
    GATES + "All 48 cards of the slice read in full and each checked against its lesson text. Exception: SC1-c140 (substitution step), "
    "reported in row cards-c140-substitution. Others: SC1-c157 R2 event limit correct (a+1/n); SC1-c191 P(B_H<=0)=1/2 and P(M_H<=0)=0; "
    "SC1-c170 90114 and SC1-c171 values; SC1-c172 exact means; SC1-c174 values; SC1-c218 78 pairs; SC1-c179-c183 problem answers.",
)
row(
    "proof-L07-cor-1.5a-continuity-direction",
    "2.4 mathematics (continuity from below)",
    "course/modules/SC/SC1/L07.html:103",
    "PASS",
    GATES + "The events {M_H >= b} increase as b decreases to m and their union over b > m is {M_H > m}; continuity from below gives Pr(M_H > m) = lim Pr(M_H >= b). Line unchanged since the round-8 pin.",
)
row(
    "prob-L07-P1-continuity",
    "2.4 problems (P1 continuity step)",
    "course/modules/SC/SC1/L07.html:445",
    "PASS",
    GATES + "P1 uses the same continuity step and now states 'Assuming A3 and A4' in the problem text; its solution names H1, H2 and H3 (checked).",
)
row(
    "prob-L07-R2-continuity",
    "2.4 problems (R2 continuity step)",
    "course/modules/SC/SC1/L07.html:502",
    "PASS",
    GATES + "R2 solution: {M_H >= b} increase as b decreases to a; union {M_H > a}; Pr(M_H > a) = 2(1-Phi(a/sqrt H)) = Pr(M_H >= a); difference 0.",
)
row(
    "num-rounding-0.3173105078",
    "2.2 numbers (rounding of the closed form)",
    "course/modules/SC/SC1/L07.html:380, :397, :420, :551, :593; course/modules/SC/SC1/L08.html:404, :411, :534",
    "PASS",
    GATES + "2(1-Phi(1)) = 0.31731050786 (indep_r9.py, erfc). 0.3173105 to seven decimals and 2 x 0.1586552539 = 0.3173105078 on printed digits, as stated. "
    "L08 E3 printed density 0.109848 (unrounded 0.1098478) and M2 0.241971 (unrounded 0.2419707) agree.",
)
row(
    "notation-T-first-passage-index",
    "2.4 notation (T and nu)",
    "course/modules/SC/SC1/L07.html:59; course/modules/SC/SC1/L08.html; notation/notation.json:112",
    "PASS",
    GATES + "T appears in L07 only in the reservation sentence (L07:59) that T is the registered S1 meaning and H is the horizon. L08 uses nu_a and tau_a; no T.",
)
row(
    "dag-simple-random-walk-defined-twice",
    "2.9 DAG (no second definition of a term)",
    "course/modules/SC/SC1/L07.html:150; course/modules/SC/SC1/L08.html:113",
    "PASS",
    GATES + "The simple random walk is defined in L06 (dfn at L06.html:53) and used by name in L07 and L08 without a second definition.",
)
row(
    "prose-L08-same-events",
    "2.9 prose (events)",
    "course/modules/SC/SC1/L08.html:51, :63-70, :77-81",
    "PASS",
    GATES + "'Coincide on every continuous path' is the claim of Prop 1.2, proved for each path; no almost-sure wording is used for it.",
)
row(
    "prose-L08-first-passage-name",
    "2.9 prose (naming)",
    "course/modules/SC/SC1/L08.html:59, :116-121",
    "PASS",
    GATES + "'First-passage time' (Definition 1.1, L08:59) and 'first-passage index nu_a' (Definition 2.1, L08:116) are distinct and each is defined before use.",
)
row(
    "lab-L07-docstring-exact-fractions",
    "2.5 lab docstring vs code",
    "tests/labs/SC1/lab-SC1-L07-1.py:1-23 (module docstring)",
    "PASS",
    GATES + "Docstring: Part A exact integer counts over 2**N (code: end_at_least, math.comb); Part B divisor PATHS - 1 (code :154-160); Part D "
    "Simpson on [1,13] with SIMPSON_INTERVALS (code :189-195). Unchanged in this round's delta.",
)
row(
    "scope-L07-assumption-phrase",
    "2.4 scope (assumption phrasing)",
    "course/modules/SC/SC1/L07.html:55, :68-82, :83-86, :91-92, :103, :134-146, :380, :511-530",
    "PASS",
    GATES + "Every scope sentence read (see scope-words-full-scan-r8 row, re-run this round). 'Every result below that uses them says so' holds: each result that uses the closed form either says 'Assuming A3 and A4' or names H2. The round-9 additions (P1 :443, E1 :470) carry the assumption.",
)
row(
    "scope-L08-everything-after",
    "2.4 scope (assumption phrasing)",
    "course/modules/SC/SC1/L08.html:55, :63-81, :87-90, :97-106, :367-374",
    "PASS",
    GATES + "'every' and 'always' on L08 are on enumerated pairs or on continuous paths for Prop 1.2; Corollary 1.4 is stated as a probability (L08:88) and the proof says so (L08:93).",
)
row(
    "notation-kappa-redefined",
    "2.4 notation (kappa)",
    "course/modules/SC/SC1/L07.html, L08.html",
    "PASS",
    GATES + "grep -c kappa: 0 hits in L07.html and L08.html this round (kappa is a Lesson 6 symbol only).",
)
row(
    "math-L08-prop-2.3-denominator",
    "2.4 mathematics (Prop 2.3 denominator)",
    "course/modules/SC/SC1/L08.html:132",
    "PASS",
    GATES + "P(nu_a > k) is 1 minus a count over 2^k, so an integer over 2^k; exact denominators are powers of two (indep_r9.py Fraction denominators).",
)
row(
    "prob-L07-P1-assumptions",
    "2.4 problems (P1 assumptions)",
    "course/modules/SC/SC1/L07.html:443-445",
    "PASS",
    GATES + "P1 states 'Assuming A3 and A4' in its text and names H1, H2, H3 in its solution; H3 applied at each level b > 0 (checked).",
)
row(
    "notation-horizon-H",
    "2.4 notation (architect decision: H is the horizon symbol)",
    "course/modules/SC/SC1/L07.html:59",
    "PASS",
    GATES + "H is the horizon throughout both lessons; the reservation of T is stated once in L07 Definition 1.1 (line 59).",
)
row(
    "lab-L08-twin-docstring-PATHS",
    "2.5 lab docstring vs code",
    "tests/labs/SC1/lab-SC1-L08-1.py:1-28 (docstring) and :37-42 (constants)",
    "PASS",
    GATES + "Docstring: Part A enumerates n = 1..12 with all levels a <= n (code: range(1, MAX_ENUM+1), range(1, n+1)); Part B exact truncated means "
    "from the identity (code: survive/tail Fractions); Part C SIM_PATHS = 1000 and SIM_STEPS = 256 (constants :40-41); Part D central difference step 1e-5 (:42).",
)
row(
    "cards-L07-misconception-same-law",
    "2.7 cards (misconception coverage, L07)",
    "cards.json SC1-c191; course/modules/SC/SC1/L07.html:397",
    "PASS",
    GATES + "c191 agrees with misconception 1 (P(M_H<=0) = 0 by Corollary 1.5(a), m = 0; P(B_H<=0) = 1/2 by Remark 1.4 and the normal law).",
)
row(
    "lab-L08-partA-printed-label",
    "2.5 lab output label (sequences vs pairs)",
    "tests/labs/SC1/lab-SC1-L08-1.py:88-102 (Part A prints); course/modules/SC/SC1/L08.html:344-352",
    "PASS",
    GATES + "The printed labels distinguish 8190 sequences from 90114 (sequence, level) pairs and the 78 (n, a) pairs; checked by indep_r9.py (sum 2^n and sum n 2^n).",
)
row(
    "rounding-rule-lab-printed-figures",
    "2.2 numbers (rounding rule stated for rounded lab figures)",
    "course/modules/SC/SC1/L07.html:380; course/modules/SC/SC1/L08.html:364",
    "PASS",
    GATES + "Both interpretation paragraphs state the rounding rule; the twin formats (.6f, .4f, .2f, .10f) match the rule; differences computed from unrounded values (re-checked in indep_r9.py).",
)
row(
    "math-L07-cor-1.5a-H3-reading",
    "2.4 mathematics (Corollary 1.5(a), H3 reading)",
    "course/modules/SC/SC1/L07.html:91, :103",
    "PASS",
    GATES + "Corollary 1.5(a)'s m >= 0 case uses Theorem 1.3 at levels b > 0 (H3 applied at each b); the m = 0 case is the same limit.",
)
row(
    "recompute-walk-dp-L07-L08",
    "2.2 numbers (independent algorithm)",
    "ledgers/SC1/scripts/SC1-c-r9/indep_r9.py; ledgers/SC1/scripts/SC1-c-r9/out/indep_r9.txt",
    "PASS",
    GATES + "Walk tails by a killed-walk DP (not binomials): N = 4, 16, 64, 256, 1024 give 0.375000, 0.332306, 0.321084, 0.318255, 0.317547; the "
    "identity holds on all 78 pairs by DP; first-passage counts by absorbing DP match the enumeration; truncated means exact Fraction DP.",
)
row(
    "recompute-sim-L07-B-C-L08-C",
    "2.2 numbers (simulated figures, independent code)",
    "ledgers/SC1/scripts/SC1-c-r9/indep_r9.py; ledgers/SC1/scripts/SC1-c-r9/out/indep_r9.txt",
    "PASS",
    GATES + "The seeded simulations were regenerated with the same RNG draw order and independent statistics: L07 proportions and SEs, L07 means and SEs, "
    "L08 sample means, SEs and z values (-1.0466, -0.6866, -0.7748) all match the printed values.",
)
row(
    "remark-1.4-title-L07",
    "2.4 mathematics / 2.9 prose (title claim)",
    "course/modules/SC/SC1/L07.html:83-84",
    "PASS",
    GATES + "The title 'limits in the horizon' matches the content (H -> 0 and H -> infinity limits of Pr(M_H >= a)).",
)
row(
    "term-walk-identity-L07",
    "2.4 notation/terms (term used before definition; attribution to Lesson 6)",
    "course/modules/SC/SC1/L07.html:150, :357, :380; tests/labs/SC1/lab-SC1-L07-1.py:54, :74, :88",
    "PASS",
    GATES + "Round-8 FAIL resolved. The phrase 'walk identity' no longer occurs in L07.html or the L07 twin (grep: 0 hits). The result is named "
    "'discrete tail identity of Lesson 6' in the hypothesis (:150), the printed line (:357), the interpretation (:380) and the twin "
    "docstrings and print (twin :54, :74, :88). That name is the title-level name of Corollary 1.4 of Lesson 6 (L06.html:87-99, 'discrete tail identity'). "
    "The twin output equals the expected block (lab_equivalence.py, True).",
)
row(
    "dag-reflection-link-L07-L08",
    "2.9 DAG and prose (concept link names the result the sentence cites)",
    "course/modules/SC/SC1/L07.html:37 and course/modules/SC/SC1/L08.html:37 (meta 'Uses' lists)",
    "PASS",
    GATES + "The reflection identity is a plain link to L06.html#s2 ('Theorem 2.5 of Lesson 6'); no reflection-principle concept link; anchor s2 exists in L06.html:100.",
)
row(
    "structure-why-it-matters-word-cap",
    "2.9 structure (why it matters: at most 120 words, BUILDER_RULES 4.2 item 1)",
    "course/modules/SC/SC1/L07.html:51; course/modules/SC/SC1/L08.html:51",
    "PASS",
    GATES + "117 whitespace tokens in each page including math; 110 outside math (python count this round).",
)
row(
    "delta-round8-hunks",
    "1 inventory (delta since round-8 pin 0dee921)",
    "course/modules/SC/SC1/L07.html, L08.html, cards.json (c149, c150, c151, c170, c218), tests/labs/SC1/lab-SC1-L07-1.py",
    "PASS",
    GATES + "Round-8 hunks re-read in the new delta (see delta-round9-hunks). Round-8 rows are re-verified from fresh evidence this round; none carried.",
)
row(
    "cards-c205-new",
    "2.7 cards (new card SC1-c205)",
    "course/modules/SC/SC1/cards.json SC1-c205 (L08)",
    "PASS",
    GATES + "Corollary 1.3 hypotheses and both equalities checked against L08.html:76-84 and L07.html:68-80.",
)
row(
    "defs-numbering-L08",
    "2.9 structure (numbering of definitions, propositions, corollaries)",
    "course/modules/SC/SC1/L08.html:58, :63, :77, :87, :97, :107, :116, :121, :131",
    "PASS",
    GATES + "Definition 1.1 once (L08:58); Proposition 1.2, Corollaries 1.3, 1.4, 1.5, Remark 1.6; Definition 2.1; Propositions 2.2, 2.3 numbered in order.",
)
row(
    "notation-star-superscript-L08",
    "2.4 notation (superscript star in L08)",
    "course/modules/SC/SC1/L08.html (s^\\ast at :73, :127; k^\\ast at :127, :429-436 problem solutions)",
    "PASS",
    GATES + "L08 uses the star only on local indices s^\\ast and k^\\ast as maximiser markers. The registry's starred symbols R^\\ast and R^{e\\ast} (notation.json:132, :137) "
    "are not used, and no registered meaning is reused.",
)
row(
    "notation-n-steps-L08",
    "2.4 notation (local convention, plan section 2.3)",
    "course/modules/SC/SC1/L08.html §2 and lab (n for walk length); L07.html Part A (N for walk length)",
    "PASS",
    GATES + "Observation: plan 2.3 asks for N for a step count and n for a grid index; L08's lab and Lesson 8 section 2 use n for walk length. No collision with notation.json (n is not registered) and no grid index in L08. Not a registry FAIL.",
)
row(
    "scope-words-full-scan-r8",
    "2.4 scope (every, all, always, never, any, surely, exactly, only) full sentence scan",
    "course/modules/SC/SC1/L07.html, L08.html (prose, outside pre blocks); ledgers/SC1/scripts/SC1-c-r9",
    "PASS",
    GATES + "grep -o of scope words: L07 45, L08 48 occurrences, plus twin docstrings. Each sentence in the round-9 delta read; the scope sentences in the unchanged prose were read in full this round (see scope-L07/L08 rows). No new unsupported scope claim.",
)
row(
    "dag-plain-bias-L08",
    "2.9 DAG (plain-English 'bias' in L08)",
    "course/modules/SC/SC1/L08.html:461",
    "PASS",
    GATES + "The single 'bias' (E2 solution: 'it cannot show a bias either way') is plain English, not the S1 concept.",
)
row(
    "terms-used-before-defined-L07-L08",
    "2.4 terms used before definition (full scan)",
    "course/modules/SC/SC1/L07.html, L08.html",
    "PASS",
    GATES + "'discretely monitored maximum' is pointed to Definition 2.1 in the why-it-matters; 'Assumption A5' is stated in Corollary 1.5 with 'stated below' and defined at L07:97; 'walk identity' in L08 is defined at Prop 2.2 (L08:121) before its first use (L08:142).",
)
row(
    "term-walk-identity-L08",
    "2.4 terms (consistency of 'walk identity' within L08)",
    "course/modules/SC/SC1/L08.html:121 (Prop 2.2 title), :142, :364, :418, :433, :511; tests/labs/SC1/lab-SC1-L08-1.py:51, :88, :102",
    "PASS",
    GATES + "The name is introduced by the title of Proposition 2.2 (L08:121) before any use and used consistently for that identity; the twin's uses name the same identity.",
)
row(
    "cards-no-A5-L05-lesson-scope",
    "2.7 cards (assumption labels cite the right lesson)",
    "cards.json SC1-c149, SC1-c150, SC1-c174, SC1-c215 and others citing A3/A4/A5",
    "PASS",
    GATES + "c150 now reads 'assuming A3 and A4 of Lesson 5 and Assumption A5 of Lesson 7', which matches L07.html:97 (A5 is Lesson 7's). c215 is the Lesson 7 A5 statement (L07.html:97-98). No card attributes A5 to Lesson 5.",
)
row(
    "freshness-L07-L08",
    "2.1 freshness (2025-2026 work for a debate brief)",
    "course/modules/SC/SC1 (L07, L08)",
    "PASS",
    GATES + "No debate key in SC1 (curriculum has none); the results are classical (reflection, first passage, the closed forms); no 2025-2026 flag raised.",
)
row(
    "cards-basis-A3-dependence",
    "2.7 cards (closed-form cards name the A3/A4 dependence)",
    "course/modules/SC/SC1/cards.json: SC1-c149 (back), SC1-c150 (back), SC1-c137, SC1-c140, SC1-c145",
    "PASS",
    GATES + "Round-8 FAIL resolved. SC1-c149 back: 'against the closed form 0.3173 of Theorem 1.3 (assuming A3 and A4 of Lesson 5)'. SC1-c150 back: 'assuming A3 and A4 of Lesson 5 and Assumption A5 of Lesson 7'. Closed-form cards c137, c145, c155 also name the dependence.",
)

# ---- round-9 additions ----
row(
    "delta-round9-hunks",
    "1 inventory (delta 0dee921..c93dd52 for the slice)",
    "course/modules/SC/SC1/L07.html (hunks at :201-236, :354-357, :380, :443, :470); L08.html (:466); lab-SC1-L07-1.py (:54-55, :74, :86-88); cards.json (c140 unchanged; c150, c151 removed, c170, c215, c218 new)",
    "PASS",
    GATES + "git diff 0dee921a c93dd526 for the slice: L07 (16 lines), L08 (2 lines), lab-SC1-L07-1.py (10 lines, L08 twin unchanged), cards.json (c087, c091, c103, c104, c214, c216 are L05 and c118, c133, c217 are L06, out of slice; in-slice: c150, c151 removed, c170, c215, c218). Every hunk read and re-verified below.",
)
row(
    "cards-c140-substitution",
    "2.7 cards / 2.4 mathematics (substitution in SC1-c140)",
    "course/modules/SC/SC1/cards.json SC1-c140 (back); course/modules/SC/SC1/L07.html:107",
    "FAIL",
    GATES + "SC1-c140 back says 'The substitution m=√H u reduces the integral to ∫_0^∞(1-Φ(u)) du.' L07.html:107 gives the substituted integral as 2√H ∫_0^∞(1-Φ(u)) du, so the card omits the factor 2√H and states an equality that is false. Low severity (the card's result √(2H/π) is correct).",
    "Edit the back of SC1-c140 in course/modules/SC/SC1/cards.json to: 'The substitution m=√H u turns the integral into 2√H ∫_0^∞(1-Φ(u)) du, and 2√H/√(2π)=√(2H/π).' Then re-run check_pages --unit SC1 and check_dag --unit SC1.",
)
row(
    "cards-c151-removed-coverage",
    "2.7 cards (removal of SC1-c151 keeps coverage)",
    "cards.json (SC1-c151 removed; was L07 'Section 3: does the tail formula apply to B̃?')",
    "PASS",
    GATES + "The removed card's fact (no tail formula for the discontinuous B̃) remains on L07.html:386 (canon break) and is tested by SC1-c154 (misconception). No lesson claim loses its card.",
)
row(
    "cards-c215-A5-card",
    "2.7 cards (new Lesson 7 Assumption A5 card)",
    "cards.json SC1-c215; course/modules/SC/SC1/L07.html:97-98",
    "PASS",
    GATES + "The card states E[X] = ∫_0^∞ P(X>m) dm with values in [0, ∞], matching the Assumption A5 text. Not a grade-bearing card (assumption), so no grade or basis field is required.",
)
row(
    "cards-c218-new",
    "2.7 cards (new L08 card SC1-c218)",
    "cards.json SC1-c218; course/modules/SC/SC1/L08.html:511 and :344-363",
    "PASS",
    GATES + "'All 78 pairs' matches the printed 'counts agree with the walk identity for 78 of 78' (L08.html:344; twin :88). Grade C with basis 'Lab 1, Part A (exact enumeration)' is correct.",
)
row(
    "assume-A3-A4-additions",
    "2.4 scope/assumptions (round-9 'Assuming A3 and A4' phrasing additions)",
    "course/modules/SC/SC1/L07.html:443 (P1), :470 (E1); course/modules/SC/SC1/L08.html:466 (E3)",
    "PASS",
    GATES + "P1 asks for Corollary 1.5(a), whose hypotheses include H2 = A3 and A4 (L07.html:91); E1 adds the assumption to a statement about the closed form; E3 asks for the density from Corollary 1.5, which assumes A3 and A4 (L08.html:97-98). Each addition is correct.",
)
row(
    "twin-docstring-identity-rename",
    "2.5 lab docstrings and print lines vs the expected block (rename)",
    "tests/labs/SC1/lab-SC1-L07-1.py:54, :74, :88; course/modules/SC/SC1/L07.html:357",
    "PASS",
    GATES + "The rename is applied consistently: twin docstrings, the printed line, the page code (lab_equivalence.py True) and the expected block (True). "
    "The printed line still reads 'Part A: discrete tail identity of Lesson 6 (maximum >= a) = (endpoint >= a) + (endpoint > a): 78 of 78', which is the code's output.",
)
row(
    "cards-c150-c170-changed-text",
    "2.7 cards (changed backs: SC1-c150, SC1-c170)",
    "cards.json SC1-c150, SC1-c170",
    "PASS",
    GATES + "c150 back: A3/A4 of Lesson 5 and A5 of Lesson 7 (correct, see cards-basis-A3-dependence). c170 back: the removed 'walk identity' sentence leaves '90114 pairs ... 78 pairs ... all 2^n sequences', which matches L08.html:344-363.",
)

fragment = {
    "unit": "SC1",
    "slice": "c",
    "round": 9,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-c (L07, L08, lab twins), round 9; did not build SC1",
    "pin": "c93dd526 (detached, /Users/billyribeiro/.fanout/wt/verifyE9-SC1-c)",
    "base": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3 (round-8 pin; round-8 fragment /Users/billyribeiro/.fanout/frags/E-SC1-c.round8.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE9-SC1-c (detached at c93dd526; .venv symlinked)",
    "scratch": "ledgers/SC1/scripts/SC1-c-r9/out/",
    "verified_at": "2026-11-05T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since round-8 pin 0dee921: read every hunk in L07.html, L08.html, lab-SC1-L07-1.py and cards.json (in-slice cards). The round-8 FAIL rows term-walk-identity-L07 and cards-basis-A3-dependence are re-verified and now PASS.",
        "Every line of both pages was read: prose, the two expected blocks, the twins (in full), all 10 quiz items and both key-results tables, and all 48 L07/L08 cards. Page code blocks were compared with the twins by lab_equivalence.py.",
        "Mutants: none. SC1-c has no grader; lab twins are demonstrations and are not mutation-tested (FINAL-ARCHITECT-RULINGS 9; verifier rulings). tools/mutate_graders.py was not run for this slice.",
        "Scripts: ledgers/SC1/scripts/SC1-c-r9/ (lab_equivalence.py, indep_r9.py, dup_scan_r9.py, make_fragment_r9.py); outputs in out/.",
        "Only failing row: cards-c140-substitution (card text omits the factor 2 sqrt(H) in the substitution step). Everything else is PASS.",
        "Observation (not a row defect): the L07 hypothesis (L07.html:150) says the last Part A tail 'is compared' with the closed form; the comparison is made in the interpretation (L07.html:380), not printed by the lab.",
        "Observation: the notation convention of plan 2.3 (N for steps, n for grid index) is not followed in L08's lab and section 2 (n for walk length). No registry collision.",
        "Not checked in this slice: the rest of the unit (L01-L06, project, grader, hub, cards outside L07/L08); render_curriculum, build_site, fetch_data, check_projects and run_graders (not in slice c); whole-repo ruff/mypy and whole pytest suite (only the lab and page-check subset); the Lesson 5-6 proofs themselves beyond the statements the slice cites (read only as far as the cross-references needed).",
    ],
    "summary": {},
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = {
    "rows": len(rows),
    "pass": counts["PASS"],
    "fail": counts["FAIL"],
    "unverifiable": counts["UNVERIFIABLE"],
    "mutants_killed": 0,
    "mutants": 0,
    "top_failures": ["cards-c140-substitution: SC1-c140 back omits the factor 2 sqrt(H) in the substitution step (cards.json)"],
}
Path("ledgers/SC1/SC1-c.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), counts)
