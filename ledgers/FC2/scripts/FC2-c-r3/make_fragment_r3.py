"""Writes the FC2 slice c round-3 verifier fragment from the rows checked this round (verifier output, not a builder file).

Run from the checkout root: .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r3/make_fragment_r3.py
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/FC2/scripts/FC2-c-r3/"
P = "PASS"
F = "FAIL"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        item["fix"] = fix
    rows.append(item)


# ---- gates (commands run this round) ----
row("c-gate-check-pages", "2.9-structure-prose", "tools/check_pages.py --unit FC2; --page L07; --page L08", P,
    f"Run this round: 'check_pages FC2: PASS', 'check_pages FC2 L07: PASS', 'check_pages FC2 L08: PASS' (exit 0). "
    f"Outputs {S}check_pages_unit.out, {S}check_pages_L07.out, {S}check_pages_L08.out.")
row("c-gate-check-dag", "dag-14", "tools/check_dag.py --unit FC2", P,
    f"Run this round: 'check_dag FC2: PASS' (exit 0; {S}check_dag.out). Judgments the tool does not make (names used by "
    f"name) are in c-dag-L07 and c-dag-L08.")
row("c-gate-check-projects", "2.6-project-gate", "tools/check_projects.py --unit FC2", P,
    f"Run this round: 'check_projects FC2: PASS' (exit 0; {S}check_projects.out). Project pages are outside slice c.")
row("c-gate-run-labs", "2.5-labs", "tools/run_labs.py --unit FC2 --page L07; --page L08; --unit FC2", P,
    f"Run this round: 'run_labs FC2: PASS (1/1)' for L07 and for L08, and 'run_labs FC2: PASS (11/11)' for the unit "
    f"(exit 0; {S}run_labs_L07.out, {S}run_labs_L08.out, {S}run_labs_FC2.out).")
row("c-gate-pytest-labs", "2.5-labs", "tests/test_labs.py -k 'FC2 and (L07 or L08)' -rA", P,
    f"Run this round: PASSED test_lab_runs_and_matches_its_page[lab-FC2-L07-1] and [lab-FC2-L08-1]; exit 0 "
    f"({S}pytest_labs_L07_L08.out).")
row("c-gate-pytest-tooling", "2.9-structure-prose", "tests/test_page_checks.py tests/test_run_labs.py", P,
    f"Run this round: 47 tests passed, exit 0 (progress line of 47 dots, -q; the summary line was not printed by -q "
    f"here; {S}pytest_tooling.out).")
row("c-gate-ruff", "gates", "ruff check . ; ruff format --check .", P,
    f"Run this round: 'All checks passed!' (exit 0; {S}ruff_check_all.out) and '553 files already formatted' "
    f"(exit 0; {S}ruff_format_all.out).")
row("c-gate-mypy", "gates", "mypy --no-incremental (full) and the two twins", P,
    f"Run this round: 'Success: no issues found in 385 source files' ({S}mypy_all.out); on the two twins "
    f"'Success: no issues found in 2 source files' ({S}mypy_twins.out).")
row("c-gate-verify-refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit FC2 (live); plain curl", P,
    f"Offline: 'offline integrity: 560 entries, 0 problems' ({S}verify_refs_offline.out). Live: 'live re-verification of "
    f"FC2: 4 of 560 entries, 0 problems' ({S}verify_refs_unit_FC2_live.out). Plain curl "
    f"https://api.crossref.org/works/10.1086/260062 (exit 0) returned title 'The Pricing of Options and Corporate "
    f"Liabilities', container 'Journal of Political Economy', volume 81, issue 3, pages 637-654, authors Black and Scholes, "
    f"issued 1973-05 ({S}crossref_black1973.json).")
row("c-gate-page-smoke-L07", "2.5-labs", "tools/page_smoke.py --unit FC2 --pages L07 L08 (Chromium)", P,
    f"Run this round: 'page_smoke modules/FC/FC2/L07.html: PASS' and 'page_smoke FC2: PASS' (exit 0); lab "
    f"lab-FC2-L07-1 ran in Pyodide, 0.0 s ({S}page_smoke_L07_L08.out).")
row("c-gate-page-smoke-L08", "2.5-labs", "tools/page_smoke.py --unit FC2 --pages L07 L08 (Chromium)", P,
    f"Run this round: 'page_smoke modules/FC/FC2/L08.html: PASS' and 'page_smoke FC2: PASS'; lab lab-FC2-L08-1 ran in "
    f"Pyodide, 0.0 s ({S}page_smoke_L07_L08.out).")

# ---- labs ----
row("c-lab-L07-1-twin", "2.5-labs", "tests/labs/FC2/lab-FC2-L07-1.py; course/modules/FC/FC2/L07.html lines 157-258", P,
    f"python -I -W error tests/labs/FC2/lab-FC2-L07-1.py: exit 0, stderr 0 bytes, 15 stdout lines "
    f"({S}twin_lab-FC2-L07-1.out, .err). {S}check_lab_pages.py: page code block equals the twin file (code_equal_twin=True) "
    f"and the expected block (L07.html lines 259-273) equals the twin's stdout (expected_equal_stdout=True) "
    f"({S}check_lab_pages.out). The twin has no RNG, no network, no file read, and ends with an unconditional main().")
row("c-lab-L08-1-twin", "2.5-labs", "tests/labs/FC2/lab-FC2-L08-1.py; course/modules/FC/FC2/L08.html lines 126-268", P,
    f"python -I -W error tests/labs/FC2/lab-FC2-L08-1.py: exit 0, stderr 0 bytes, 18 stdout lines "
    f"({S}twin_lab-FC2-L08-1.out, .err). {S}check_lab_pages.out: code_equal_twin=True, expected_equal_stdout=True "
    f"(expected block L08.html lines 251-268). The twin's assert len(CASES)==9 and worst<=TOL hold (exit 0).")
row("c-lab-L07-1-hypothesis", "2.5-labs", "L07.html line 156 (hypothesis)", P,
    f"Closed form 1045 cents: unrounded 10.4505835722 ({S}recompute_numbers.out, 'L07 C unrounded'). Twin lines 248-254 "
    f"check Phi(x)+Phi(-x)=1 at 0.0, 0.35, 1.7, 3.0 and the parity put to 1e-9 (twin lines 92-98), as the hypothesis says. Expected sign "
    f"pattern (+ at 1, 5, 25; - at 2, 10, 50, 100, 200; 0 at 400) matches the output and the unrounded errors "
    f"({S}recompute_numbers.out, 'L07 n=' lines).")
row("c-lab-L08-1-hypothesis", "2.5-labs", "L08.html line 125 (hypothesis)", P,
    f"37 halvings in every row (twin output, column halvings); largest recovery error 1.74e-11 < 1e-10 (twin output). "
    f"Prices 0.00, 4.00, 100.00, 120.00 at strike 100 rejected with the bounds message (twin output lines 'rejected'; "
    f"{S}twin_claims.out). Lower bound printed 4.8771 (twin output line 2).")
row("c-lab-L07-1-interpretation", "2.5-labs", "L07.html line 274 (interpretation); line 152", P,
    f"Unrounded signs (+,-,+,-,+,-,-,-,-): 5 sign changes; |error| strictly decreasing over the nine step counts "
    f"({S}recompute_numbers.out, 'sign changes' and '|err| decreasing: True'). STEPS is a fixed nine-item tuple (twin "
    f"line 28), so the lab does not extend the list. The claims about what the lab does not show are true of the code.")
row("c-lab-L08-1-interpretation", "2.5-labs", "L08.html line 269 (interpretation)", P,
    f"Prop 3.2 bound 5e-11 (= tol/2) against printed errors 5.73e-12 to 1.74e-11 (twin output): 'at most 5e-11' and 'lie "
    f"inside that bound' are correct. The twin's main() calls price = bs_call(...) unrounded (twin main, line "
    f"'price = bs_call(SPOT, strike, RATE, TAU, sigma_true)'), and cents() is applied only for printing, as the sentence says.")
row("c-lab-L07-rounding", "2.5-labs", "L07.html line 152 and line 166-169 (docstring); twin lines 10-13 and 31-34", P,
    f"cents() is sign*floor(|x|*100+0.5), i.e. half away from zero, the rule the page states for the error column. "
    f"Checked on unrounded errors: -91.008223 -> -91, -19.717453 -> -20, -3.989203 -> -4 ({S}recompute_numbers.out). "
    f"Positive prices are rounded half up, which is the same rule for positive numbers.")
row("c-lab-L08-bracket-claim", "2.5-labs", "L08.html line 121 (lower-end and upper-end sentences); twin lines 70 and 78-82", P,
    f"Round-2 FAIL re-verified and now resolved. (a) Lower end: at K=80, 100, 120, C(1e-6) equals L as doubles "
    f"(23.901646039942875, 4.877057549928594, 0.0), so the window (L, C(1e-6)] is empty for Lab 1's strikes ({S}limits_check.out, "
    f"{S}twin_claims.out 'window nonempty=False'). At K=S e^(r tau)=105.12710963760242, L=0.0 and C(1e-6)=3.989422803e-05; "
    f"the twin's own implied_volatility(0.00001, K) raises ValueError 'the volatility bracket [1e-06, 10.0] does not contain "
    f"the root ... or below the lower end' ({S}twin_claims.out). The page's 'at or below C(10^{{-6}})' and '≈ 0.0000399' are "
    f"correct. (b) Upper end: C(10)=99.9999440858 at K=100, and the twin rejects 99.99995 with the same bracket message "
    f"({S}recompute_numbers.out, {S}twin_claims.out). The bracket condition holds in every accepted case (twin line 78).")

# ---- numbers ----
row("c-num-L07-M1-M2", "2.2-numbers", "L07.html lines 299-306 (M1, M2)", P,
    f"d1=0.350000000, d2=0.150000000 ({S}recompute_numbers.out). K e^(-r tau)=95.122942450. C=10.4505835722 (1045 cents). "
    f"P by formula 5.5735260223 and by parity 5.5735260223 (diff 0.0) -> 557 cents. Page values 0.35, 0.15, 10.450584, "
    f"10.4505836, 95.122942, 5.573526, 557 all match.")
row("c-num-L07-lab-table", "2.2-numbers", "L07.html lines 259-273 (lab expected block); line 152", P,
    f"All nine rows recomputed independently ({S}recompute_numbers.out, 'L07 n=' lines): tree cents 1216, 954, 1081, 1025, "
    f"1052, 1041, 1043, 1044, 1045; printed errors 171, -91, 36, -20, 7, -4, -2, -1, 0; unrounded errors +171.170139, "
    f"-91.008223, +35.535035, -19.717453, +7.038205, -3.989203, -1.997191, -0.999231, -0.499773 cents. Printed binomial minus "
    f"printed closed form equals the printed error in every row ('printed-cents row diffs equal printed errors: True').")
row("c-num-L07-misconceptions-E1-E2", "2.2-numbers", "L07.html lines 288, 330, 334", P,
    f"400 steps: unrounded -0.499773 cents = -0.0049977 currency units, printed 0. 200 steps: -0.999231 cents (E1 'next "
    f"smallest'). Positive unrounded: 171.17, 35.54, 7.04 (3). Negative: -91.01, -19.72, -3.99, -2.00, -1.00, -0.50 (6). "
    f"Printed: 3 positive, 5 negative, 1 zero ({S}recompute_numbers.out).")
row("c-num-L07-M3", "2.2-numbers", "L07.html line 310 (M3 solution)", P,
    f"h=0.25; u=1.1051709181, d=0.9048374180, R=1.0125784515; q=0.5378083720 -> 0.537808 (page: 0.5378084 and 0.537808). From "
    f"the six-place printed inputs 0.5378068625 -> 0.537807 (page's 0.107741/0.200334 = 0.537807). sigma^2/r^2 = 16. "
    f"({S}recompute_numbers.out, 'L07 M3' lines).")
row("c-num-L07-E3", "2.2-numbers", "L07.html line 338 (E3 solution)", P,
    f"u=1.22140276, d=0.81873075, R=1.05127110, q=0.57749320; up payoff 22.14027582; V1 = e^(-0.05) q 22.14027582 = "
    f"12.1622849646 -> 12.1623 and 1216 cents ({S}recompute_numbers.out, 'L07 E3' lines).")
row("c-num-L07-R2", "2.2-numbers", "L07.html lines 345-348 (R2 solution)", P,
    f"tau=4, sigma=0.1, r=0.0125: sigma*sqrt(tau)=0.2 and r*tau=0.05; call 10.4505835722 equals Lab 1's closed form "
    f"(recompute_numbers.out, 'L07 R2 call'). Proposition 1.5 is the stated reason.")
row("c-num-L08-L-M1", "2.2-numbers", "L08.html lines 297 (M1), 57 (L formula), 251-252 (lab output), 329 (E2)", P,
    f"L = 100 - 100e^(-0.05) = 4.877057550 (page 4.8771 at four places; unrounded 4.877058). 100e^(-0.05) = 95.122942 "
    f"(page 95.1229). 120e^(-0.05) = 114.14753 -> 114.15 (E2), so L(120) = 0 ({S}recompute_numbers.out, 'L08 L(K=100)' and "
    f"'L08 K=120 L').")
row("c-num-L08-table", "2.2-numbers", "L08.html lines 252-263 (lab expected block)", P,
    f"Every row recomputed ({S}recompute_numbers.out, 'L08 table' lines): unrounded cents 2390.9978, 2458.8835, 2897.6408, "
    f"680.4958, 1045.0584, 1802.2951, 46.2497, 324.7477, 1080.5974 -> printed 2391, 2459, 2898, 680, 1045, 1802, 46, 325, "
    f"1081 (all equal the expected block). Recovery errors and 37 halvings equal the twin output.")
row("c-num-L08-E2-E3", "2.2-numbers", "L08.html lines 329 (E2), 333 (E3)", P,
    f"E2: unrounded price at K=120, sigma 0.10 = 0.4624965106 currency units = 46.2497 cents ({S}recompute_numbers.out). "
    f"E3: price 0.50 at K=120 is accepted by the twin's own function, sigma = 0.10207696 after 37 halvings ({S}twin_claims.out); "
    f"C(1e-6)=0 and C(10)=99.99993875 at K=120 (sign change, as the text says). The bounds message is raised only for a price "
    f"at or below L=0 or at or above S=100 at this strike (twin_claims.out).")
row("c-num-L08-M3-halvings", "2.2-numbers", "L08.html line 305 (M3); line 269", P,
    f"log2(W/tol) = log2(9.999999e10) = 36.5412 (page 36.54). 10/2^36 = 1.4552e-10 (page 1.46e-10). W/2^37 = 7.276e-11 <= 1e-10. "
    f"First k with W/2^k <= tol is 37 ({S}recompute_numbers.out, 'L08 M3 halvings').")
row("c-num-L08-R2", "2.2-numbers", "L08.html lines 341-343 (R2 and solution)", P,
    f"100 phi(0.35) = 37.524035 (page 37.5240). 0.01/37.52 = 0.00026652 -> 0.000267 (page). 0.01/37.5240 = 0.00026650 "
    f"(page's parenthetical 0.000266 at six places; the exact value is 0.00026650 - 4e-9, rounds to 0.000266). 0.000267 is "
    f"0.0267 volatility points (1 point = 0.01) ({S}recompute_numbers.out, 'L08 R2' and 'vega=100 phi' lines).")

# ---- mathematics ----
row("c-math-L07-lemmas-1", "2.3-math", "L07.html lines 63-76 (Lemma 1.1, 1.2 and proofs); P1 solution line 316", P,
    f"Lemma 1.1: substitution t = sqrt2 s re-derived; max |Phi(x) - (1+erf(x/sqrt2))/2| = 1.1e-16 at 7 points "
    f"({S}recompute_numbers.out, 'Lemma1.1' line). Lemma 1.2: t -> -t with phi even; Phi(x)+Phi(-x)-1 = 0.0 at test points. "
    f"P1 solution (g' = phi(x) - phi(-x) = 0) re-derived.")
row("c-math-L07-prop1.4-1.5", "2.3-math", "L07.html lines 95-115 (Prop 1.4, 1.5 and proofs)", P,
    f"Prop 1.4: the two forms C-S+K e^(-rt) and K e^(-rt) Phi(-d2) - S Phi(-d1) agree to 2.1e-14 over K in {{80,100,120}}, "
    f"sigma in {{0.1,0.2,0.4}} ({S}recompute_numbers.out, 'Prop1.4' line). Prop 1.5: d1 = (ln(S/K)+r tau)/(sigma sqrt tau) + "
    f"sigma sqrt tau/2 re-derived; residual 5.6e-17 ('Prop1.5 d1 identity').")
row("c-math-L07-tree-lemma2.2-thm2.3", "2.3-math", "L07.html lines 119-141 (Def 2.1, Lemma 2.2, Thm 2.3); L06.html lines 128-141", P,
    f"Lemma 2.2: 200000 random (r, sigma, h) triples with r>0: 0 mismatches between 0<d<R<u and h<sigma^2/r^2 "
    f"({S}recompute_numbers.out, 'Lemma2.2 random'). Thm 2.3: explicit sum equals backward induction (assert in "
    f"recompute_numbers.py tree_call) for n in {{1,2,5,10,25,50,100,200,400}}. Hypotheses cited to L06 Thm 3.3 (L06.html line "
    f"141: 'Under A1, A2, A3, A5, A6 and A6′'); L07's A1-A5, A7, r>0 and h<sigma^2/r^2 supply them, A4 gives constant R. "
    f"R^(-n) = e^(-r tau) because nh = tau.")
row("c-math-L07-cross-refs", "2.3-math", "L07.html lines 55, 103, 140, 281; L04.html lines 58-64, 90; L05.html line 63-64; L06.html lines 55-63, 110-141, 320", P,
    f"L04.html 'Standing assumptions (A1 to A5)' lines 58-64: A1 no income, A2 no frictions, A3 no arbitrage, A4 constant "
    f"continuously compounded rate with discount e^(-r(tau-t)), A5 European exercise; L07 line 55 paraphrases these "
    f"consistently. L05.html Theorem 1.2 (line 64): 'Under A1, A2, A3, A4 and A5'. L04.html Definition 2.1 (line 90) is "
    f"American and European exercise. L06.html Definition 3.2 (line 132) is backward induction; Theorem 3.3 (line 140) and A6′ "
    f"(line 320) as cited. L06 A6 (Definition 1.2) is 0<d<R_f<u.")

row("c-math-L08-lemma2.1", "2.3-math", "L08.html lines 67-84 (Lemma 2.1 and proof)", P,
    f"d1-d2 derivative difference = sqrt(tau); S phi(d1) = K e^(-r tau) phi(d2) re-derived via logs and d1^2-d2^2 = 2a; "
    f"finite-difference check over K in {{80,100,120}}, sigma in {{0.05,0.1,0.2,0.4}}: worst abs error 6.26e-9 "
    f"({S}recompute_numbers.out, 'Lemma2.1 finite-difference').")
row("c-math-L08-lemma2.2", "2.3-math", "L08.html lines 86-93 (Lemma 2.2 and proof)", P,
    f"Three cases a>0, a<0, a=0 re-derived. C(1e3) = 100.0 at K=80, 100, 120, 105.127 and C(1e-6) = L as doubles at K=80, 100, "
    f"120 ({S}limits_check.out; {S}twin_claims.out).")
row("c-math-L08-thm2.3", "2.3-math", "L08.html lines 95-104 (Theorem 2.3, proof lines 99-101; line 104)", P,
    f"Proof re-derived: C(sigma/2^k) decreases to L, C(2^k sigma) increases to S (so L < C(sigma) < S); C continuous by Lemma 2.1; "
    f"sigma_1 < sigma_2 from C(sigma_1) < C* < C(sigma_2) and strict monotonicity; IVT; uniqueness by strict monotonicity. "
    f"Line 104 restates it correctly.")
row("c-math-L08-prop3.2-bisection", "2.3-math", "L08.html lines 108-119 (Def 3.1, Prop 3.2 and proof)", P,
    f"Def 3.1 equals the twin loop (twin lines 84-92: while high-low > TOL; middle; gap<0 -> low). Stop at k=37 for W=9.999999, "
    f"tol=1e-10; ceil(log2(W/tol))=37. |sigma_hat - sigma*| <= tol/2 on 1854 random well-conditioned cases (vega >= 1e-2, bracket "
    f"condition checked): worst ratio 0.7273 ({S}recompute_numbers.out, 'Prop3.2' lines). Cases with vega < 1e-2 are outside "
    f"the claim.")
row("c-math-L08-canon-and-scope", "2.3-math", "L08.html lines 273-276 (Section 4), line 121", P,
    f"'Each implied volatility is unique by Theorem 2.3' is applied per fixed strike, as Theorem 2.3 states. 'The bracket "
    f"condition of Definition 3.1 holds in every case the lab accepts' holds by construction (twin line 78 raises otherwise). "
    f"'A price on a model's bounds has no implied volatility' matches Theorem 2.3. Section 4's two-quote argument is valid: "
    f"uniqueness per strike and one common sigma under A7 would force sigma_1 = sigma_2.")

# ---- grades ----
row("c-grade-L07", "2.4-grades", "L07.html lines 361-366 (key results), 86 (Def 1.3 claim), 369", P,
    f"Six T spans (Lemma 1.1, 1.2, Prop 1.4, 1.5, Lemma 2.2, Thm 2.3) each have a proof on the page or a cited L06 theorem; "
    f"they equal the six key-results rows. Def 1.3's attribution is C with data-cite black1973pricing (the single-study "
    f"grade). Lab 1 values are not graded (line 369).")
row("c-grade-L08", "2.4-grades", "L08.html lines 356-359 (key results), 55 (C attribution), 362", P,
    f"Four T spans (Lemma 2.1, 2.2, Thm 2.3, Prop 3.2) each have a proof on the page and equal the four key-results rows. "
    f"Section 1 attribution is C with data-cite black1973pricing. Lab 1 not graded (line 362).")
row("c-grade-lab-values", "2.4-grades", "L07.html line 369; L08.html line 362", P,
    f"Both pages state that Lab 1 is not a row of the key-results table and carry no grade for it, consistent with ruling 9 for "
    f"values that appear only in lab output.")

# ---- notation, DAG, prose, structure ----
row("c-notation-L07-L08", "13-notation", "L07.html and L08.html math segments; notation/notation.json (symbols and macros)", P,
    f"Symbols read: Phi (registered as standard normal CDF) used only with that meaning; T appears once, as 'not \\(T\\)' "
    f"(L07 line 55), a negation; R_f, Q, R^*, gamma_3, gamma_4 not used; no registered macro is redefined; no raw \\mathbb{{E}}. "
    f"Local, unregistered: phi (density), h, u, d, q, R^(n) = e^(rh), L, W, m, a, s, C, P, S, K, V_n, e_n. R^(n) is the "
    f"gross return that L06 calls R_f under a different local symbol (L06 line 320 and Def 1.1 use R_f); it is not a "
    f"meaning collision, so it is not a FAIL. L07 cites the L06 result 'with gross return R^(n)', so the mapping is explicit. "
    f"Recommendation for the architect, not a verifier FAIL: consider one symbol for the concept. Check via grep of both pages.")
row("c-dag-L07", "dag-14", "L07.html meta row (line 37), dfn (line 80), links (lines 37, 80, 103, 281)", P,
    f"Anchors exist: L04.html id def-option-payoff; L05.html def-put-call-parity; L06.html def-binomial-option-pricing and "
    f"def-risk-neutral-probability; L07 defines def-black-scholes-formula (grep-confirmed, only in L07). discount-factor, "
    f"continuous-compounding, normal-distribution, limit are closure concepts (check_dag PASS). 'lognormal' is a plain dfn "
    f"(plan 0.2). Forward mentions of Lesson 8 are prose only. The FC1 prerequisite is in the curriculum now "
    f"(curriculum.json FC2 prereqs M4, CF1, FC1).")
row("c-dag-L08", "dag-14", "L08.html lines 37, 51-69, 341, 395-404; both twins; cards.json FC2-c120", P,
    f"Round-2 FAIL re-verified and resolved. 'vega' is absent from the visible text of L08 and L07 (grep returned 0), from both "
    f"twins and from every card (python scan, cards_check.out). The derivative is written dC/dsigma (Lemma 2.1 title "
    f"'Derivative of the price in volatility'). option-greeks (DV1) is not used. 'bisection' and 'root-finding' are plain prose "
    f"(plan 0.2, no link).")
row("c-prose-scope-words", "4-scope-words", "L07.html, L08.html (every, all, only, exactly, same, any, each, unique, whatever, in every case)", P,
    f"Every scope word read in context. Universal claims are backed: A7 'for every strike' (hypothesis); 'for every real x' "
    f"(Lemma 1.2); 'every case the lab accepts' (twin line 78 guard); '37 halvings in every row' and 'every row' (nine printed "
    f"rows); 'exactly one' (Thm 2.3); 'the sign changes ... only in the unrounded value' (400-step row); 'the same' statements "
    f"in Prop 1.5 and R2 are the proposition. No unbacked 'always' or 'all'.")
row("c-prose-process-banned", "2.9-structure-prose", "L07.html, L08.html visible prose and lab docstrings", P,
    f"Process-word scan (verifier, builder, ledger, round, fragment, TODO, TBD, lorem, placeholder, draft, fixed in, previous "
    f"round, builder) over visible text: none. 'Previous' appears only as the lesson-nav link label and 'the previous item' "
    f"(L08 line 382, a quiz prompt). check_pages banned-string check PASS.")
row("c-struct-L07", "2.9-structure-prose", "L07.html (whole page, read in full, lines 1-458)", P,
    f"Order: why it matters (<=120 words; check_pages PASS); sections 1-3 with Lab 1 inline in Section 3; section 4 canon-breaks; "
    f"section 5 misconceptions (3); section 6 problem set (M1-M3, P1-P3, E1-E3, R1-R3: 12 problems, 12 solutions); section 7 "
    f"key results (6 rows); section 8 quiz (10 items, 10 explain blocks); section 9 references. data-hours=8 matches the "
    f"eyebrow '8 study hours'.")
row("c-struct-L08", "2.9-structure-prose", "L08.html (whole page, read in full, lines 1-456)", P,
    f"Same order: why it matters; sections 1-3 with Lab 1 inline in Section 3; section 4; section 5 (3 misconceptions); section 6 "
    f"(12 problems, 12 solutions); section 7 key results (4 rows); section 8 quiz (10 items, 10 explain blocks); section 9 "
    f"references. data-hours=6 matches the eyebrow '6 study hours'. Lesson nav: L07 previous, project.html next.")
row("c-hours-L07-L08", "2.9-hours", "course/modules/FC/FC2/index.html lines 29, 41, 133-142; L07.html lines 2, 34; L08.html lines 2, 34", P,
    f"Hub: L01 6 + L02 8 + L03 9 + L04 7 + L05 8 + L06 8 + L07 8 + L08 6 = 60 = data-hours-lessons=60; project 30; 60+30 = 90 "
    f"(curriculum.json FC2 hours 90); 30/90 = 33.3%, in 10-40%. L07 8 and L08 6 agree with their eyebrows and data-hours.")

# ---- cards ----
row("c-card-01-c099-c108", "2.10-cards", "course/modules/FC/FC2/cards.json FC2-c099..c108 (L07)", P,
    f"Each card checked against the current L07 text: c099 A7 (line 58-59); c100 Lemma 1.1; c101 Lemma 1.2 (proof uses even "
    f"density and total integral 1); c102 Def 1.3; c103 Prop 1.4; c104 Prop 1.5; c105 Def 2.1; c106 Lemma 2.2; c107 Thm 2.3 "
    f"(e^(-r tau)=R^(-n) because nh=tau); c108 Def 3.1. Card objects unchanged since 9294b914 (cards_delta.out: only FC2-c120 "
    f"changed among L07/L08 cards).")
row("c-card-02-c109-c117", "2.10-cards", "course/modules/FC/FC2/cards.json FC2-c113 (L07); other cards in c109-c117 checked",
    F,
    f"Eight of nine cards in c109-c117 pass (c109 C basis Lab 1; c110 C; c111 C; c112 T Prop 1.5; c114 T basis M1; c115 T "
    f"basis M3; c116 T basis E3; c117 C basis Lab 1 and E1). FC2-c113 fails: grade T and no 'basis' key "
    f"({S}cards_delta.out, 'FC2-c113 has basis key: False'), but its back says 'parity holds for the closed-form put in Lab 1 "
    f"(Proposition 1.4; Lab 1)'. That is a numerical check printed by Lab 1 (L07.html line 273: 'put-call parity holds for the "
    f"closed-form put to 1e-9: True'). plans/FC2-build-plan.md section 10 requires basis to name the lab or problem for a derived "
    f"result with a numerical check; ruling 9 reads lab-output claims as C. The round-2 note that the basis names the lab was "
    f"wrong: the card is byte-identical to the 9294b914 version.",
    "In course/modules/FC/FC2/cards.json, FC2-c113: either delete the clause 'and parity holds for the closed-form put in Lab 1' "
    "from its back (the T fact is Proposition 1.4, which stands alone), or split it into a C card with basis 'Lab 1 (printed "
    "parity check)'. Then run tools/check_pages.py --unit FC2.")
row("c-card-03-c118", "2.10-cards", "cards.json FC2-c118 (L07): grade and basis", P,
    f"Grade C, basis 'Lab 1 (call value); Problem M2 (parity)'. The call 10.450584 rests on Lab 1 output (L07.html line 306: "
    f"'Lab 1, unrounded value 10.4505836'), so the card grade names the lab. Arithmetic 10.450584 - 100 + 95.122942 = "
    f"5.573526 -> 557 cents ({S}recompute_numbers.out).")
row("c-card-04-c119-c131", "2.10-cards", "cards.json FC2-c119..c131 (L08)", P,
    f"c119 Def 1.1 (definitional; no grade); c120 Lemma 2.1 (now 'derivative dC/dsigma'; vega wording removed in this pin); c121 Lemma 2.2; "
    f"c122 Thm 2.3; c123 Prop 3.2 halving formula; c124 Def 3.1 update rule; c125 37 halvings (T with basis M3 and Lab 1); "
    f"c126 L=4.8771 (basis M1); c127 M2; c128 scope of inversion check (Section 5; no numerical claim, so no basis needed); "
    f"c129 rejected prices (C, basis Lab 1); c130 historical volatility (Def 1.1); c131 L at K=120 = 0 (basis E2).")
row("c-card-05-c145-c151-c152-c167", "2.10-cards", "cards.json FC2-c145 (L07), FC2-c151, FC2-c152, FC2-c167 (L08)", P,
    f"c145 'not derived' matches L07 Section 4 and A8 (line 279 and 91). c151 (T, Prop 3.2 within tol/2) matches Prop 3.2. "
    f"c152 (T, bracket condition) matches Def 3.1. c167 (stop rule and report) matches Def 3.1 (loop end reports the midpoint).")
row("c-card-numbers", "2.10-cards", "cards.json, all 37 L07/L08 cards vs visible text of their own lesson", P,
    f"{S}cards_check.py: every numeric token in the 37 card fronts and backs appears in its own lesson's visible text "
    f"('numeric tokens not found in own lesson text: none'; {S}cards_check.out).")
row("c-card-duplicates", "2.10-cards", "cards.json (all 165 cards; L07/L08 37 cards)", P,
    f"165 cards, 165 unique ids, 0 duplicate ids ({S}cards_check.out). Near-duplicate fronts (difflib ratio >= 0.75) that touch "
    f"L07/L08: c102/c145 (0.82), c114/c126 (0.77), c124/c152 (0.77), c124/c167 (0.78), c126/c131 (0.83). Each pair asks "
    f"different facts (formula vs its derivation status; d1,d2 vs lower bound; update rule vs bracket vs stop rule; L at K=100 "
    f"vs K=120).")
row("c-card-coverage", "2.10-cards", "cards.json L07 (21 cards) and L08 (16 cards) vs BUILDER 7 / plan section 10", P,
    f"Definitions: A7 (c099), Def 1.3 (c102), Def 2.1 (c105), Def 3.1 (c108, c124, c152, c167), Def 1.1 (c119). Theorems and "
    f"lemmas: L07 Lemmas 1.1, 1.2, 2.2 (c100, c101, c106), Props 1.4, 1.5 (c103, c104, c112), Thm 2.3 (c107); L08 Lemmas 2.1, "
    f"2.2, Thm 2.3, Prop 3.2 (c120, c121, c122, c123, c151). Misconceptions: L07 three (c111, c104, c113); L08 three (c130, "
    f"c128, c129). Key formulas and lab results carded with grade C where lab-only (c109, c110, c117, c118).")

# ---- references ----
row("c-ref-L07-L08-black1973", "2.1-citations", "L07.html lines 7 (meta), 86 and 445; L08.html lines 55 and 443; references/references.json black1973pricing", P,
    f"Registry: black1973pricing used_by now lists DV1 and FC2 (references.json). verify_refs --unit FC2 (live) and --offline "
    f"PASS. Live Crossref record matches the citation (title, authors Black and Scholes, year 1973, JPE 81(3), 637-654). "
    f"Attribution 'Black and Scholes (1973) is the source of this formula': the paper's body and abstract were not readable. "
    f"Crossref has no abstract field (crossref_black1973.json). The publisher landing page https://www.journals.uchicago.edu/doi/"
    f"10.1086/260062 returned HTTP 403 to plain curl (reproduced; {S}jpe_landing.html). Per the access rule, the recorded URL and "
    f"plain-curl 403 are the access statement; the claim is supported by the registry identity only. Note (not a FAIL): "
    f"L07.html meta description (line 7) calls the tree 'Cox–Ross–Rubinstein tree'; the visible text and the footer cite only "
    f"black1973pricing. That is a naming of a method, not a claim, and cox1979option is a registry key for FC2; optional change: "
    f"say 'binomial tree' in the meta description.")

# ---- assemble ----
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row ids"
n_pass = sum(1 for r in rows if r["status"] == P)
n_fail = sum(1 for r in rows if r["status"] == F)
n_unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
verdict = "PASS" if n_pass == len(rows) else "FAIL"

fragment = {
    "unit": "FC2",
    "slice": "c",
    "round": 3,
    "round_note": "Final full verification of L07-L08 with twins and cards; round-2 FAIL rows re-verified (c-lab-L08-bracket-claim now PASS, c-dag-L08 now PASS); c-card-02 FAIL is new (FC2-c113 basis).",
    "verifier": "claude-haiku-5-5, independent verifier (round 3; did not build FC2; checkout pinned at 8196077d; no shared context with the builders)",
    "pin": "8196077d5f56c3919d33e69888176d197d378ad4",
    "base": "9294b914a51647c66d2dee62c4a112c76ba04900 (round-2 pin; delta read for slice c: L07.html, L08.html, both twins, cards.json, L04/L05/L06 cross-referenced hunks)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS3-FC2-c",
    "scratch": "/tmp (only /tmp/fc2c_cards_prev.json, a git show copy; the scripts recreate it); all scripts and outputs in ledgers/FC2/scripts/FC2-c-r3/",
    "verified_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Carried rows: none. Every row was re-verified from scratch this round, because L07.html, L08.html, both twins and FC2-c120 changed since round 2 and the cited locators moved.",
        "Delta read (every hunk of git diff 9294b914 HEAD for slice c): course/modules/FC/FC2/L07.html (hunks at lines 51, 55, 143, 156, 159), L08.html (hunks at lines 51, 68-69, 121, 130, 274-275, 305, 341-343, 356, 392, 401-404), tests/labs/FC2/lab-FC2-L07-1.py (docstring), tests/labs/FC2/lab-FC2-L08-1.py (docstring), cards.json (FC2-c120 only among L07/L08 cards). Read in full: both pages (458 and 456 lines), both twins, all 37 L07/L08 cards. Cross-referenced L04, L05, L06 read at the cited lines (their deltas are wording only and do not touch the cited items).",
        "Lab twins are demonstrations (ruling): no mutants were run; the slice has no grader. Mutation testing does not apply.",
        "Process note: one file (check_lab_pages.py) was first written to the primary repo path by mistake; it was removed at once and git status of the primary repo was restored (only the pre-existing untracked tests/test_lx1_project_lab3.py). All evidence in this round is in the checkout.",
        "Pre-existing untracked files in ledgers/FC2/scripts/FC2-c-r3/ (created 00:54 with the checkout, not by this verifier: recheck_L07_L08.py, recheck_L08_bounds.py, recheck_L08_E3.py, out/) were neither cited nor relied on.",
        "No-arbitrage and bounds statements in L08 Section 4 and E3 were checked on the twin's own functions (twin_claims.py loads the twin without its trailing main()).",
        "Round-2 note on FC2-c113 (basis names the lab) was incorrect; corrected in c-card-02-c109-c117.",
    ],
    "summary": {"rows": len(rows), "pass": n_pass, "fail": n_fail, "unverifiable": n_unv},
}

out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "ledgers/FC2/FC2-c.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(out, "rows", len(rows), "pass", n_pass, "fail", n_fail, "verdict", verdict)
