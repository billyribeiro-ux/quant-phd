"""Round 10, slice E4-c: build ledgers/E4/E4-c.json from the round-9 row ids (ids kept) with round-10 evidence."""
import json
from pathlib import Path

BASE = Path("/Users/billyribeiro/.fanout/wt/verifyE10-E4-c")
OLD = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-E4-c.round9.json").read_text(encoding="utf-8"))
OUT = "ledgers/E4/scripts/E4-c-r10/out/"
SCR = "ledgers/E4/scripts/E4-c-r10/"
SUBJ = "L07.html, L08.html, L09.html, lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py (sha256 identical to the round-9 pin c93dd526)"
RD = "re-read in full this round"

ev = {
    "E4c-r4-delta-read": f"Round 10 delta c93dd526..00a84795: no diff in {SUBJ}. Changed slice hunks read: L06.html:86,143,147,225; index.html:38,167; cards.json (E4-c181..c188, c201, c223, c224, c226, c228, c244, c247, c248); lab-E4-L06-1.py docstring. See E4c10-delta-read.",
    "E4c-r4-recheck-numbers": f"Every printed and quoted number in L07/L08/L09 {RD}; recomputed by {SCR}independent_L07_L08.py, {SCR}independent_L09.py and {SCR}independent_L08_partA.py (outputs in {OUT}).",
    "E4c-cmd-check-pages": f"Run this round: check_pages.py --unit E4 --page L07, --page L08, --page L09 each printed PASS ({OUT}check_pages_L07.out, check_pages_L08.out, check_pages_L09.out, exit 0).",
    "E4c-cmd-check-dag": f"Run this round: check_dag.py --all printed 'check_dag E4: PASS' ({OUT}check_dag.out, exit 0). Concept closure also checked in E4c10-dag-closure.",
    "E4c-cmd-check-projects": f"Run this round: check_projects.py --all printed 'check_projects E4: PASS' ({OUT}check_projects.out, exit 0).",
    "E4c-cmd-run-labs": f"Run this round: run_labs.py --unit E4 --page L07, L08, L09 each printed 'run_labs E4: PASS (1/1)' ({OUT}run_labs_L07.out, run_labs_L08.out, run_labs_L09.out).",
    "E4c-cmd-twins-standalone": f"Run this round: each twin run as python -I -W error from an empty scratch directory exited 0 ({OUT}twin_L07.out, twin_L08.out, twin_L09.out).",
    "E4c-expected-equals-output": f"Run this round: {SCR}expected_vs_output.py compares each page's expected block with the standalone twin stdout line for line: L07 28/28, L08 20/20, L09 18/18 identical ({OUT}expected_vs_output.out).",
    "E4c-cmd-page-smoke": f"Run this round: page_smoke.py --unit E4 --pages L07 L08 L09 printed PASS for each page and 'page_smoke E4: PASS'; lab L09 5.0 s under the 10 s limit ({OUT}page_smoke_L07-9.out, exit 0).",
    "E4c-cmd-ruff-mypy-twins": f"Run this round: ruff check and ruff format --check on tests/labs/E4 passed (12 files formatted); mypy --no-incremental on the three twins: no issues; repo-wide ruff check . passed and mypy --no-incremental over 385 files passed ({OUT}ruff_twins.out, mypy_twins.out, ruff_check_repo.out, mypy_repo.out).",
    "E4c-cmd-pytest-labs": f"Run this round: pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k E4: 13 passed ({OUT}pytest_E4.out, exit 0).",
    "E4c-cmd-verify-refs": f"Run this round: verify_refs.py --offline: 560 entries, 0 problems; verify_refs.py --unit E4 (live): 3 of 560 entries, 0 problems ({OUT}verify_refs_offline.out, verify_refs_unit_E4.out).",
    "E4c-cmd-run-graders": f"Run this round: run_graders.py --unit E4: 'reference 50/50 seeds' PASS ({OUT}run_graders_E4.out). Not a slice subject; recorded because grader/test_project.py changed this round.",
    "E4c-L07-structure": f"L07.html {RD} (lines 1-614): header, lesson sections 1-8, lab, canon-breaks, misconceptions, problem set (M1-M3, P1-P3, E1-E3, R1-R3), key results, quiz, references, lesson-nav. check_pages L07 PASS ({OUT}check_pages_L07.out).",
    "E4c-L07-hours": "L07.html:2 data-hours=\"8\" and L07.html:34 eyebrow '8 study hours'; index.html:147 card 'L07 · 8 h'.",
    "E4c-L07-def-correlation-noise-volume": f"L07.html:55-58 (Definition 7.1) and L07.html:37 link; {RD}. Corr and noise-volume definitions match Lemma 7.3 and the L06 noise supply (L06.html:56-60).",
    "E4c-L07-lemma-7.3-7.4": f"L07.html:70-87 {RD}. Discriminant argument (Lemma 7.3) and residual-variance argument (Lemma 7.4) re-derived by hand: E(X-bY)^2 = Var X - 2b Cov + b^2 Var Y; minimiser b = Cov/Var Y; residual Var X - Cov^2/Var Y.",
    "E4c-L07-prop-7.6": f"L07.html:96-108 {RD}. Closed form rho^2 = sigma_v^2/(sigma_v^2+sigma_eta^2) re-derived: Y = p/theta_s = v + eta, eta = eps - kappa u, Corr(v,Y)^2 = sigma_v^2/(sigma_v^2+sigma_eta^2); kappa = a sigma_e^2/lambda re-derived from the market-clearing coefficients (s-coefficient gives theta_s = tau_bar/(tau_v+tau_bar); u-coefficient gives kappa lambda tau_e = a). Numerically confirmed: independent_L07_L08.py solves clearing and matches closed form to 1e-12.",
    "E4c-L07-prop-7.7": f"L07.html:111-118 {RD}. Signs: D = sigma_v^2 + sigma_e^2 + chi sigma_u^2 with chi = a^2 sigma_e^4/lambda^2; each partial sign re-derived; lab sweeps in Parts C and D agree (independent_L07_L08.out 'lam' and 'a' rows).",
    "E4c-L07-remark-7.8": f"L07.html:121-123 {RD}. rho0^2 = Corr(v,s)^2 = sigma_v^2/(sigma_v^2+sigma_e^2) re-derived; independent sweep at sd 0.01 gives rho^2 0.4999 below benchmark 0.5.",
    "E4c-L07-remark-7.9-varp": f"L07.html:127 and :379 {RD}. Var(p) = theta_s^2(sigma_v^2+sigma_e^2)+theta_u^2 sigma_u^2 re-derived; independent var_p column (0.504848, 0.551020, 0.843750, 2.156805, 7.483757) matches 729/1444, 27/49, 27/32, 729/338, 35937/4802.",
    "E4c-L07-lab1-values": f"course/modules/E/E4/L07.html:130-372 {RD}; page code equals twin (TVP); expected block equals standalone twin stdout (EVO: 28 lines identical). Values recomputed independently (independent_L07_L08.out).",
    "E4c-L07-lab1-partF": f"L07.html:132 and :359-362 {RD}; twin Part F (seed 7, 20000 draws, tolerance 0.02). Independent replay with random.Random(7) gives sample rho^2 0.330625 (independent_L07_L08.out 'L07 Part F').",
    "E4c-L07-hypothesis-scope": f"L07.html:132 hypothesis and :363 interpretation {RD}; the hypothesis claims (exact Fraction Parts A-E, sweeps, tolerance 0.02) match the twin and output.",
    "E4c-L07-misc-claims-1-3": f"L07.html:379, 383, 387 {RD}: misconception 1 (729/1444 to 35937/4802, 4/9 to 1/66), misconception 2 (tau_eta = 1/2, rho^2 = 1/3, tau_v = 1), misconception 3 (rho^2 = 1/66 at sigma_u = 4) all match output and independent recomputation.",
    "E4c-L07-misc-4": f"L07.html:391-394 {RD}: kappa = a sigma_e^2/lambda falls with lambda; rho^2 at lambda 1/4, 1/2, 3/4 = 1/6, 1/3, 9/22 (independent_L07_L08.out).",
    "E4c-L07-problems-M-P": f"L07.html:403-448 {RD}. M1 (1/6), M2 (9/22), M3 (2/7, derivative 5/(sv2+5)^2 > 0), P1 (discriminant, Var(Y)=0 case), P2 (residual variance), P3 (scaling) re-derived.",
    "E4c-L07-problems-E1": f"L07.html:459 {RD}: 1/3 - 0.330625 = 13/4800 = 0.0027083; /0.02 = 13/96 = 0.1354; re-derived by hand.",
    "E4c-L07-problems-E3-R": f"L07.html:463-499 {RD}: E2 (sigma_eta^2 = 3, sigma_u^2 = 1/2, sigma_u = 0.7071), R1 (limit via chi growth), R2 (sigma_u = sqrt((sv2+se2)/chi) = 1/sqrt2 with chi = 4, rho^2 = 1/4 check: D = 4, rho^2 = 1/4), R3 (derivative -sv2 chi/D^2; ratio -chi/D).",
    "E4c-L07-quiz": f"L07.html:522-597 {RD}: ten items; numeric answers 0.3333, 5, 0.4091, 0.5, 0.7071 and option keys re-derived; tolerances hold (e.g. |0.7071 - sqrt(1/2)| = 7e-6).",
    "E4c-L07-key-results": f"L07.html:504-520 {RD}: grades T for Lemma 7.3, 7.4, Prop 7.6, 7.7, Remark 7.8; C for the finite-check rows and the SIMULATED row.",
    "E4c-L07-canon-volume": f"L07.html:373 {RD}: a strictly increasing reparametrisation (sigma_u^2) keeps the sign of the sigma_u response; statement is a logical consequence.",
    "E4c-L07-canon-linear-witness": f"L07.html:369 {RD}: v ~ N(0,1), p = v^2: Var p = E v^4 - 1 = 2, Cov(v,p) = E v^3 - E v E v^2 = 0 by symmetry, so rho^2 = 0; p determines |v|.",
    "E4c-L07-cents-docstring": f"tests/labs/E4/lab-E4-L07-1.py:16-18 and :182 {RD}; the twin docstring and population float conversion match the printed expected block (EVO). 'cents' does not appear in the lab text.",
    "E4c-L07-notation-c": f"L07.html:81, 86-87, 117, 122, 488, 495 {RD}; notation/notation.json has no conflicting macro (NS: registered macros used: Corr, Cov, E, Normal, Var).",
    "E4c-L07-E2-population": "L07.html:463-466 (E2 solution): the 'treat R^2 as rho^2' assumption is stated, and the inversion 1/(1+sigma_eta^2) = 1/4 gives sigma_eta^2 = 3; re-derived.",
    "E4c-L07-simulated-labels": f"L07.html:132 hypothesis text, :360-362 expected block 'Part F: SIMULATED sample check' and twin Part F docstring (lab-E4-L07-1.py) {RD}; SIMULATED label present where seeded draws are used.",
    "E4c-L07-dag": "L07.html:37-38 links: random-variable, expectation, variance, correlation, least-squares-projection (M3/M4), noisy-rational-expectations-equilibrium (E4 L06 anchor exists at L06.html:169); all in the E4 prerequisite closure (E4c10-dag-closure).",
    "E4c-L07-define-before-use": f"L07.html:37, 57-62 {RD}: price informativeness defined (Def 7.2) before Lemma 7.3 and Remark 7.5 use it; noise volume defined (Def 7.1) before Prop 7.6.",
    "E4c-L07-process-and-banned": f"L07.html body {RD}; grep for process words and banned phrases (BUILDER_RULES 1.3-1.4) returns none (E4c10-banned-phrases).",
    "E4c-L08-structure": f"L08.html {RD} (lines 1-813): model, Lemmas 2.1-2.5, Prop 3.1, Cor 3.2, Lemma 3.3, Prop 4.1-4.4, Lemma 4.5, Def 4.6, Prop 5.1-5.2, A4, Section 5.1, lab, canon, misconceptions, problems, key results, quiz, references. check_pages L08 PASS.",
    "E4c-L08-hours": "L08.html:2 data-hours=\"8\"; L08.html:34 '8 study hours'; index.html:148 card 'L08 · 8 h'.",
    "E4c-L08-lemma-2.1-2.2-fact-2.3": f"L08.html:85-113 {RD}. Lemma 2.1 x* = (m-p)/(aV) and value re-derived (f(x*) = -(m-p)^2/(2V)); Lemma 2.2 (1+sigma^2/V)^(-1/2) re-derived from the Gaussian integral; Fact 2.3 re-derived.",
    "E4c-L08-cor-2.4-lemma-2.5": f"L08.html:122-146 {RD}. Corollary 2.4(a) V_I = 1/(tau_v+tau_e), (b) b_y = tau_eta/(tau_v+tau_eta), V_U; Lemma 2.5 proof (r_v independent of (s,u)) checked step by step.",
    "E4c-L08-prop-3.1": f"L08.html:151-170 {RD}. Proof coefficient matching re-derived: alpha = (1-beta') v-bar, beta_p = beta', kappa' (A' - (1-lambda) tau_eta') = a with A' - (1-lambda)tau_eta' = lambda tau_e gives kappa' = kappa. Numerically: the clearing price at the Example 1.1 parameters (lambda 0.5 and 1) and at two other parameter sets equals the closed form to 1e-12 (out/independent_L07_L08.out, out/independent_example11_price.out).",
    "E4c-L08-cor-3.2-lemma-3.3": f"L08.html:173-200 {RD}. Corr^2 = tau_eta/(tau_v+tau_eta) = sigma_v^2/(sigma_v^2+sigma_e^2+kappa^2 sigma_u^2) re-derived; Lemma 3.3(a)-(c) proofs re-derived; lambda sweep (independent_L07_L08.out: 0.013061 .. 0.166667) consistent.",
    "E4c-L08-prop-4.1-4.2-4.4": f"L08.html:204-246 {RD}. D_I = (b_s-beta)(s-v-bar)+kappa beta u; D_U = (b_y-beta)(y-v-bar) re-derived; Var formulas and Prop 4.2 closed forms re-derived; Prop 4.4 'EU_I >= EU_U iff c <= G' re-derived (divide by negative, logs).",
    "E4c-L08-lambda0-citation": f"L08.html:221, 240, 275 {RD}: references to Lemma 4.5 and Prop 4.4 are to in-page results; no registry citation.",
    "E4c-L08-lemma-4.5": f"L08.html:249-261 {RD}. G(0) = (1/2a) ln(1+q), q = sigma_v^2/sigma_e^2 re-derived term by term (X0 = a^2 sigma_u^2 sigma_v^2, 1/V_I identity); independent G(0) = ln2/4 = 0.173287 (independent_L07_L08.out).",
    "E4c-L08-prop-5.1": f"L08.html:284-301 {RD}. (a) tau_eta = tau_e, A = tau_e, beta = b_s, G = 0; (b) and (c) case analysis against Def 4.6 re-checked; independent sigma_u^2 = 0 grid max |G| = 0.",
    "E4c-L08-prop-5.2": f"L08.html:304-332 {RD}. (a) limit re-derived (kappa beta -> a sigma_v^2; Var(D_U)/V_U -> a^2 sigma_u^2 sigma_v^2); numerically G(1e-5) - G(0) = -6.25e-12 (independent_L07_L08.out). (c) uses A4 only; interior root not claimed unique (L08.html:333).",
    "E4c-L08-A5": f"L08.html:57-80 (A1-A3), :313-332 (A4), :573-580 {RD}. A4 is stated as an assumption; no proof is claimed; lines 51 and 800 say which results use it.",
    "E4c-L08-line51-zero-cost": f"L08.html:51 {RD}: 'no informed fraction ... is an equilibrium at cost c with 0 < c < G(0) (Prop 5.1(b))' matches Prop 5.1(b) and Def 4.6.",
    "E4c-L08-line51-existence": f"L08.html:51 {RD}: 'equilibria exist outside (G(1), G(0))' matches Prop 5.2(b) and (c); 'Only Proposition 5.2(c) and Section 5.1's bisection use A4' matches L08.html:309, 320, 337 and 800.",
    "E4c-L08-G1-derivation": f"L08.html:673-675, 719 and Emp 3 at :679 {RD}: G(1) = (1/4) ln(5/3) re-derived with V_I = 1/2, b_y = 1/6, V_U = 5/6, Var(D_I) = 1, Var(D_U) = 2/3; numerically 0.127706406 (independent_L07_L08.out).",
    "E4c-L08-lab1-part-A": f"L08.html:336 hypothesis and expected block :544-547 {RD}; twin Part A lines 81-126 of lab-E4-L08-1.py; expected lines identical (EVO); sample slope 0.1595 vs formula 0.160494 reproduced independently (independent_L08_partA.out).",
    "E4c-L08-lab1-part-B": f"L08.html:548-551 {RD}: gain(0) 0.173287, gain(0.5) 0.158997, gain(1) 0.127706, gain(1e-6)-gain(0) = -6.25e-14; independent G values match (independent_L07_L08.out).",
    "E4c-L08-lab1-part-C": f"L08.html:552-558 {RD}: lam* 1, 0.965625410, 0.815032329, 0.657828572, 0.480567912, 0.231615819, 0 with gaps < 1e-13 at interior roots and boundary gaps 7.71e-03, -6.71e-03; independent bisection reproduces every lam* to 9 decimals (independent_L07_L08.out).",
    "E4c-L08-lab1-part-D-docstring": f"lab-E4-L08-1.py:181-182 {RD} and L08.html:564; the docstring 'gain is zero on the interior grid' matches output 0.0e+00; independent sigma_u^2 = 0 grid max |G| = 0.",
    "E4c-L08-misc-claims": f"L08.html:583-600 {RD}: 'G(1) = ln(5/3)/4 > 0', 'at cost 0.15 lambda* = 0.658', 'Corr^2 from 0.013061 to 0.166667', 'the fraction falls from 1 to 0' all match the printed output.",
    "E4c-L08-canon-finite-traders": f"L08.html:577 {RD}: a statement that the derivation does not cover finite trader counts; no result claimed.",
    "E4c-L08-canon-A5-limit": f"L08.html:571-579 {RD}: noise traders exogenous; Prop 5.1(b)/5.2 contrast correctly stated; cost-in-wealth point matches Prop 4.4.",
    "E4c-L08-emp-1-2": f"L08.html:658-667 {RD}: Emp 1 (N(lambda*) = 1.83e-15; cost 0.15 between G(1)=0.1277 and G(0)=0.1733) and Emp 2 (0.231615819 at cost 0.17, the sixth of seven costs; Corr 0.013061; 0.480567912 at 0.16) match output.",
    "E4c-L08-res-1": f"L08.html:683-687 {RD}: Res 1 is Prop 5.1(b)/(c); the variance argument (sigma_u = 0 gives Var(p) = 0) is correct.",
    "E4c-L08-res-2-crossref": f"L08.html:690-692 {RD}: Res 2 limit of Var(D_U)/V_U = a^2 sigma_u^2 sigma_v^2 re-derived (same as L08.html:325-328).",
    "E4c-L08-res-3": f"L08.html:697-699 {RD}: G(1) -> 0 as sigma_u^2 -> 0 re-derived (Var(D_I) = kappa^2 b_s^2 sigma_u^2 -> 0; b_y -> b_s).",
    "E4c-L08-mech-1-3": f"L08.html:607-624 {RD}: Mech 1 kappa = 4, tau_eta = 1/17; Mech 2 x* = 1/12 and exponent -1/16; Mech 3 (1+4)^(-1/2) = 0.447214 and Jensen bound exp(-2) = 0.135 re-computed.",
    "E4c-L08-proof-1-3": f"L08.html:632-651 {RD}: Proof 1 (coefficient of s), Proof 2 (strict monotonicity of tau_eta), Proof 3 (N strictly decreasing in c, one cost per fraction) re-derived.",
    "E4c-L08-emp-3": f"L08.html:671-679 {RD}: G(0) = ln(2)/4 and G(1) = ln(5/3)/4 with each intermediate (V_I = 1/2, b_y = 1/6, V_U = 5/6, A = 1, beta = 1/2, Var(D_I) = 1, Var(D_U) = 2/3) re-derived.",
    "E4c-L08-quiz-items": f"L08.html:730-795 {RD}: numeric answers 4 (kappa), 0.1732868 (G(0)), 0.0555556 (Corr^2 at lambda 1/2 = 1/18), 0.6578 (rounding of 0.657828572), 0.4472136 (1/sqrt5) and option keys re-derived.",
    "E4c-L08-quiz-6-uniqueness": f"L08.html:762-770 {RD}: 'If c >= G(0), fraction 0 is an equilibrium' is the correct option; the explanation cites Def 4.6(i) and Prop 5.2(b), consistent with L08.html:269, 289-290.",
    "E4c-L08-key-results": f"L08.html:710-728 {RD}: T grades for Lemma 2.1, Lemma 2.2, Prop 3.1, Cor 3.2/Lemma 3.3, Prop 4.4, Lemma 4.5, Prop 5.1, Prop 5.2 (A4 marked), and G(1) (arithmetic in Emp 3).",
    "E4c-L08-footer": f"L08.html:811 footer 'E4 · General Equilibrium & Information in Markets ...' {RD}. Round-9 locator 806 was stale; the text is unchanged.",
    "E4c-L08-notation-gamma": f"L08.html:140, 154, 161, 165, 168, 635 {RD}: varpi and beta local; no registered symbol reused (NS, notation.json).",
    "E4c-L08-define-posterior": f"L08.html:123, 161, 257-258 and L06.html:96 (posterior definition sentence) {RD}: 'posterior' is defined in L06 before L08 uses it.",
    "E4c-L08-hub-title": "index.html:148 card title 'The Grossman–Stiglitz Paradox' equals L08.html:35 h1 'The Grossman–Stiglitz Paradox'. The round-9 locator index.html:136 was stale.",
    "E4c-L08-DAG": f"L08.html:37-38 links (price-informativeness, expected-utility, certainty-equivalent, arrow-pratt-risk-aversion, competitive-equilibrium, derivative, normal-distribution, conditional-expectation-elementary, correlation) all in the E4 prerequisite closure (E4c10-dag-closure).",
    "E4c-L08-simulated": f"L08.html:341 hypothesis span.simulated-label 'SIMULATED' and expected line 'part A (SIMULATED draws)' {RD}; the seeded draws are labelled.",
    "E4c-L08-process-banned": f"L08.html body {RD}; grep for process words and banned phrases returns none (E4c10-banned-phrases).",
    "E4c-L09-structure": f"L09.html {RD} (lines 1-525): Assumptions B1-B3, Def 1.1-1.2, Thm 2.1, Def 2.2, Cor 2.3, Example 2.4, lab, canon-breaks, misconceptions, problems, key results, quiz, references. check_pages L09 PASS.",
    "E4c-L09-hours": "L09.html:2 data-hours=\"8\"; L09.html:34 '8 study hours'; index.html:149 card 'L09 · 8 h'.",
    "E4c-L09-theorem-2.1": f"L09.html:86-100 {RD}. Proof re-derived: S1 = sum_D pi(D) g1(D) over P1 cells inside M, S2 = -S1 over P2 cells, both >= 0 forces zero; the same argument for g2.",
    "E4c-L09-cor-2.3-def-2.2": f"L09.html:102-115 {RD}: Cor 2.3 follows from Thm 2.1 by contradiction; Def 2.2 restates Thm 2.1 and says nothing about prices (L09.html:104).",
    "E4c-L09-example-2.4": f"L09.html:118-120 {RD}: M(1) = {{1,2,3}}, x = (-1,2,-2,-2,-2,-2): g1(1) = 1/2, g2(1) = 1/3, g1(3) = -2 re-derived by hand and by ledgers/E4/scripts/E4-c-r10/independent_L09.py.",
    "E4c-L09-meet-definition-canon": f"L09.html:79 (Def 1.2) vs L09.html:298 canon-break: the meet is the smallest union of cells of both partitions; the description matches.",
    "E4c-L09-misc-1-no-trade-overclaim": f"L09.html:307 {RD}: Cor 2.3 implies a state of the meet with a negative posterior; 500 strict bets and none on the meet (independent_L09.out).",
    "E4c-L09-misc-2-3": f"L09.html:311 and :315 {RD}: E = {{w1,w2}} example: M(w1) = {{w1,w2,w3}} not contained in E (re-derived); posterior-not-realised-payoff example: trader 1 posterior 1/2 at state 1 and x(3) = -2.",
    "E4c-L09-mech-1-3": f"L09.html:327-342 {RD}: Mech 1 g1 = 1, 1, 3/2, 3/2; Mech 2 M(1) = Omega; Mech 3 expected receipts 0.4 and 0.2 re-derived.",
    "E4c-L09-proof-1-2": f"L09.html:352-363 {RD}: Proof 1 identity and Proof 2 (meet of a state inside a common-knowledge event) re-derived.",
    "E4c-L09-proof-3-statement": f"L09.html:367-369 {RD}: trivial partitions give g1 = E[x], g2 = -E[x]; the hypothesis forces E[x] = 0.",
    "E4c-L09-emp-1-3": f"L09.html:377-394 {RD}: Emp 1 (500 strict, 625 nonnegative, intersection 0), Emp 2 (printed witness posteriors 1/2, 1/2, -2 and 1/3 re-derived), Emp 3 (zero-posterior bets: x(3) = 0 and x(2) = -x(1), count 5*5^3 = 625; independent_L09.out gives 625).",
    "E4c-L09-res-1": f"L09.html:405 {RD}: Res 1 (transaction cost k > 0) derivation re-checked: S1 >= 0 and -S1 - k pi(M) >= 0 sum to -k pi(M) >= 0, a contradiction.",
    "E4c-L09-res-2": f"L09.html:409-412 {RD}: Res 2 algebra re-derived: x(H) = 1, x(L) = -t, theta = t/(1+t); trader 1 receipt (1+t)(nu1-theta), trader 2 receipt (1+t)(theta-nu2); theta = (nu1+nu2)/2 works.",
    "E4c-L09-res-3": f"L09.html:416-419 {RD}: Res 3 (any E that is a union of cells of both partitions) follows from the same B1 argument.",
    "E4c-L09-canon-prior-example": f"L09.html:295 {RD}: trivial-partition example q1(H) = 0.7, q2(H) = 0.4, x = (1,-1): receipts 0.4 and 0.2 re-derived.",
    "E4c-L09-lab1-counts": f"L09.html:264-281 expected block identical to twin stdout (EVO, 18 lines); counts 500 strict at states 1 and 4, 625 nonnegative on the meet, 0 on both; independent recount reproduces all four counts and both witness bets (independent_L09.out).",
    "E4c-L09-lab1-hypothesis-interpretation": f"L09.html:128 hypothesis and :282 interpretation {RD}: 'the lab illustrates Theorem 2.1 and does not prove it' is accurate; the hypothesis claims match the output.",
    "E4c-L09-quiz": f"L09.html:442-508 {RD}: nine items; numeric answers 0.5, 0.3333333, 0.2, 15625, 0.5 re-derived; option keys correct (Def 1.2 for item 1; Assumption B1 for item 4; meet {{1,2,3}} for item 8).",
    "E4c-L09-key-results": f"L09.html:426-440 {RD}: T rows (Proof 1, Theorem 2.1, Cor 2.3, Misconception 2, Example in Section 4 and Res 2) and one C row (Lab 1 Parts B and C, one model).",
    "E4c-L09-references": f"L09.html:510-514 {RD}; references/references.json:17291-17315 (milgrom1982information, title, JET 26(1), pages 17-27, 1982, verified_by crossref); Crossref metadata fetched by plain curl matches (out/crossref_milgrom.json).",
    "E4c-L09-footer": f"L09.html:523 footer {RD}; Round-9 note: the line moved from 522 to 523 when a row was added upstream; text unchanged.",
    "E4c-L09-hub-title": "index.html:149 card 'The No-Trade Theorem' equals L09.html:35 h1 'The No-Trade Theorem'. The round-9 locator index.html:137 was stale.",
    "E4c-L09-dag": f"L09.html:37-38 links (arrow-debreu-equilibrium: L02 anchor L02.html#def-arrow-debreu-equilibrium exists; pareto-efficiency E1; conditional-expectation-elementary M4; adverse-selection E2 contrast) all in the E4 prerequisite closure (E4c10-dag-closure).",
    "E4c-L09-process-banned": f"L09.html body {RD}; grep for process words and banned phrases returns none (E4c10-banned-phrases).",
    "E4c-L09-simulated": f"L09.html:128 'The lab uses exact fractions and no random draws, so no SIMULATED label applies'; twin imports are fractions and itertools only (lab-E4-L09-1.py:15-16), so there are no draws.",
    "E4c-twin-L07-1": f"tests/labs/E4/lab-E4-L07-1.py {RD} (202 lines); docstring lines 16-18 and code; standalone run exit 0 with -I -W error; page code identical (TVP).",
    "E4c-twin-L08-1": f"tests/labs/E4/lab-E4-L08-1.py {RD} (207 lines); gain_at_zero docstring lines 65-66 match Lemma 4.5 (p* = v-bar - a sigma_v^2 u); standalone run exit 0; page code identical (TVP).",
    "E4c-twin-L09-1": f"tests/labs/E4/lab-E4-L09-1.py {RD} (135 lines); exact Fraction arithmetic, no draws; standalone run exit 0; page code identical (TVP).",
    "E4c-notation-registered": f"NS: registered macros used in L07-L09 are Corr, Cov, E, Normal, R, Var (notation/notation.json:macros); 'N', 'S' are local per the registry note; no registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, Q) appears.",
    "E4c-dag-unlinked": f"L07-L09 {RD}: plan D1 (Bayes) is prose-only in L09 (no 'Bayes' string); D3 absent from L08; D7 CARA and D8 common knowledge are plain prose (no data-concept).",
    "E4c-no-mutants-slice": "Lab twins are demonstrations; mutation testing applies to project graders only (verifier rules ruling). No mutants are listed for this slice, and no grader mutant is claimed.",
    "E4c-r2-delta-read": f"Round 10 delta read (E4c10-delta-read): L07, L08, L09 pages and twins unchanged since c93dd526; index.html changed only in the data sentences (lines 38, 167) and L06 changed only in lines 86, 143, 147, 225.",
    "E4c-L08-dfn-duplicates": f"L08.html:66, 71 and L06.html:66-72 and 245, 673 {RD}: no <dfn> term is defined twice across L06-L09 (scan: 26 distinct dfn terms, each once).",
    "E4c-L08-G-before-definition": f"L08.html:51, 79 {RD}: G(lambda) is written with the reference 'Definition 4.3' in the forward pointer at :51 and defined at :232-235; no use of G before its definition in a claim.",
    "E4c-L09-state-labels-c-a": f"L09.html:311 {RD}: misconception 2 uses omega_1..omega_3, E, P_1, P_2 consistently with Def 1.2.",
    "E4c-r3-first-use-before-definition": f"L08.html:66, 71 and L06.html:72, 245, 673 {RD}: the forward references are explicit ('Definition 6.2 of Lesson L06'); no term is used in a claim before its definition.",
    "E4c-r4-L08-assumption-numbering": f"L08.html:58, 65, 70, 314, 319-332, 573 {RD}: A1-A4 numbered, each stated once; Prop 5.2(c) cites A4 (L08.html:309).",
    "E4c-r4-L09-partition-common-knowledge": f"L09.html:62 {RD}: 'Both partitions are common knowledge' is an assumption (B2), matching Def 1.2.",
    "E4c-r5-recheck-L07-prop-7.6": f"L07.html:97-118 {RD}: Props 7.6, 7.7 and proofs re-derived (see E4c10 rows); independent_L07_L08.py confirms the sign pattern on the sweeps.",
    "E4c-r5-recheck-L08-gains": f"L08.html:336, 544-563, 564, 587, 591, 595 {RD}: gains and root values match independent_L07_L08.out to the printed digits.",
    "E4c-r5-recheck-L09-counts": f"L09.html:118-120, 126, 264-281, 435 {RD}: counts 15625, 500, 625 and 0 match independent_L09.out.",
    "E4c-r5-L07-docstring-exact-fraction": f"lab-E4-L07-1.py:16-18 and :182 {RD}: docstring 'Parts A to E print exact Fraction population values; Part F converts ... to float' matches the code (Fraction in Parts A-E).",
    "E4c-r5-cards-duplicates": f"cards.json (243 cards): no duplicate ids, fronts or backs (out/cards_check_r10.out); per-lesson counts L07 21, L08 43, L09 23.",
    "E4c-r5-cards-L07": f"cards.json E4-c130..E4-c150 (21 cards) {RD}: each answer matches L07 text and output (e.g. c142 4/9, 1/3, 1/6, 1/18, 1/66; c146 0.330625; c148 tau_eta = 1/2).",
    "E4c-r5-cards-L08": f"cards.json E4-c151..E4-c188, c222..c224, c245, c246 {RD}: changed cards c181..c185, c187, c188, c223, c224 re-read against L08 text and Lab 1 output; c179 (A4 conditional) matches L08.html:333 and :320.",
    "E4c-r5-cards-L09": f"cards.json E4-c189..E4-c211, c232 {RD}; changed card c201 (merged c233) re-read: 500 and 0 at states 1 and 4 match L09 lab output; card numbers appear in the lesson (625 at L09.html:394; 15625 at :264-281).",
    "E4c-r5-milgrom-record": "references/references.json:17290-17315 (milgrom1982information): title, authors (Milgrom, Stokey), 1982, JET 26(1) pages 17-27, doi 10.1016/0022-0531(82)90046-1, verified_by crossref; matches L09.html:512 and Crossref (out/crossref_milgrom.json).",
    "E4c-r5-notation-scan": f"NS (out/notation_scan_r10.out) over L07-L09 math spans: 405, 827, 382 spans; only registered macros used with registered meanings.",
    "E4c-r5-figures": "No figure or SVG in L07-L09 (grep for svg in the three pages returns none); page_smoke has no figure sweep for these pages.",
    "E4c-r5-lab-sim-labels": f"lab-E4-L07-1.py Part F, lab-E4-L08-1.py Part A (printed 'SIMULATED draws'), L09 has no random draws {RD}.",
    "E4c-r6-L08-why-it-matters": f"L08.html:51 {RD}: the paragraph's forward references (Definition 6.2 of L06, Definition 4.3, Lemma 4.5, Prop 5.1(a), Assumption A3, Definition 4.6, Prop 5.1(b), Prop 5.2(c), Section 5.1) all resolve.",
    "E4c-r6-L08-example-1.1": f"L08.html:79 {RD}: Example 1.1 parameters a = 2, unit variances, v-bar = 0; Lab 1 part B prints G(0), G(1); both values match.",
    "E4c-r6-L08-definition-6.2-link": f"L08.html:51, 59 and L06.html:66-68 (Definition 6.2 CARA utility) {RD}: the link resolves and matches the CARA definition.",
    "E4c8-L08-misc3-printed-range": f"L08.html:595-596 {RD}: 'Lab 1 prints values from 0.013061 to 0.166667' matches the twin's printed Corr values at costs 0.17 and 0.12.",
    "E4c8-delta-read": f"Round 10 delta (E4c10-delta-read): no hunk touches L07-L09 pages or twins; cards and hub hunks read in full.",
    "E4c8-twin-page-equal": f"TVP (out/twin_vs_page.out): page data-run code equals the twin line for line for L07, L08, L09 (201, 206, 134 page lines against 202, 207, 135 twin lines including the trailing newline).",
    "E4c8-rederive-numbers": f"Every printed and quoted number in L07-L09 re-derived this round (independent_L07_L08.out, independent_L09.out, independent_L08_partA.out).",
    "E4c8-scope-banned-dfn-notation": f"L07-L09 {RD}: scope words located by grep and each sentence read in the full read; the ones that carry a universal claim are backed by a computation, a stated hypothesis, or the exhaustive L09 enumeration; banned phrases none (E4c10-banned-phrases); dfn ids unique; notation (NS) clean.",
    "E4c8-cards-L07-L09": f"cards.json E4-c130..E4-c211, c222..c224, c232, c245, c246 {RD}; no duplicates (CC); every answer re-derived (see E4c-r5-cards rows).",
    "E4c8-registry-milgrom": "L09.html:512 cites the registry key only for the lesson topic; references.json:17291-17315 record matches Crossref (out/crossref_milgrom.json).",
    "E4c9-delta-read": f"Round 10 delta read (E4c10-delta-read) covers the round-9 fixes in L07-L09 (none in this round's delta: pages unchanged).",
    "E4c9-L08-line333-prop5.2-prose": f"L08.html:333 {RD}: 'G(1) = ln(5/3)/4 ~ 0.127706' and 'the page does not show that the gain is positive at every lambda' match the page's claims and the lab's grid.",
    "E4c9-independent-recompute": f"Round 10 independent recomputation: {SCR}independent_L07_L08.py, independent_L09.py, independent_L08_partA.py (outputs in {OUT}); all printed numbers in L07-L09 reproduced.",
    "E4c9-L09-milgrom-no-claim": "L09.html:512 states 'The page states no result of that paper'; the page contains no claim from Milgrom and Stokey (grep for 'Milgrom' in L09.html returns only the reference line). The abstract was not readable with plain curl (Crossref has no abstract; doi.org returned HTTP 302 and was not followed), so no abstract-level claim is made or checked.",
    "E4c9-L08-no-grossman-stiglitz-cite": f"L08.html:800 {RD}: 'The attribution of the model and of the paradox to a published source is not made here' and no registry key is cited in L08 (data-references empty).",
    "E4c9-scope-words": f"L07-L09 {RD}: scope words located by grep and each sentence read in the full read; each universal claim is backed by a computation, a stated hypothesis, or the exhaustive L09 enumeration.",
    "E4c9-L06-statements-used": f"L06.html:56-98 (Def 6.1, 6.2, A1-A4, G), :173-200 (Prop 6.7), :213-225 (Cor 6.8), :234-236 (Remark 6.10) {RD} this round; changed lines 86, 143, 147, 225 do not change any statement that L07-L08 use; numerically confirmed (independent_L07_L08.out).",
}

# Rows whose location text needs the corrected locator
loc_fix = {
    "E4c-L08-footer": "course/modules/E/E4/L08.html:811",
    "E4c-L08-hub-title": "index.html:148 vs L08.html:35",
    "E4c-L09-hub-title": "index.html:149 vs L09.html:35",
    "E4c-L07-hours": "L07.html:2, :34; index.html:147",
    "E4c-L08-hours": "L08.html:2, :34; index.html:148",
    "E4c-L09-hours": "L09.html:2, :34; index.html:149",
    "E4c-r5-cards-duplicates": "course/modules/E/E4/cards.json (243 cards)",
    "E4c-r5-cards-L07": "course/modules/E/E4/cards.json E4-c130..E4-c150",
    "E4c-r5-cards-L08": "course/modules/E/E4/cards.json E4-c151..E4-c188, c222..c224, c245, c246",
    "E4c-r5-cards-L09": "course/modules/E/E4/cards.json E4-c189..E4-c211, c232",
    "E4c-L09-footer": "course/modules/E/E4/L09.html:523",
}

rows = []
for r in OLD["rows"]:
    rid = r["id"]
    if rid not in ev:
        raise SystemExit("no round-10 evidence written for " + rid)
    rows.append({
        "id": rid,
        "check": r["check"],
        "location": loc_fix.get(rid, r["location"]),
        "status": "PASS",
        "evidence": "Round 10: " + ev[rid],
    })

NEW = [
    {"id": "E4c10-delta-read", "check": "delta", "location": "git diff c93dd526..00a84795 over course/modules/E/E4, tests/labs/E4, notation, references, tools, curriculum",
     "status": "PASS",
     "evidence": "git diff --stat: L07.html, L08.html, L09.html, lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py, notation/, references/, tools/, curriculum/ have NO diff since c93dd526 (sha256 recorded in notes). Changed hunks in the wider unit that touch this slice: L06.html:86, 143, 147, 225 (read; Prop 6.7 and Cor 6.8 unchanged in substance); index.html:38, 167 (read; see E4c10-hub-data-arithmetic); cards.json cards E4-c181..c188, c201, c223, c224 (read in full), and c226, c228, c244, c247, c248 (outside L07-L09, not verified here); lab-E4-L06-1.py docstring (L06 twin, outside slice)."},
    {"id": "E4c10-hub-data-arithmetic", "check": "2.8-data / 2.9-prose", "location": "course/modules/E/E4/index.html:38 and :167",
     "status": "FAIL",
     "evidence": "Both data-status sentences list the exact-Fraction labs as L01, L02, L04, L05 and L09 plus L03 Part A, and the double-precision parts as L03 Part B and L08 Parts B to D. They omit L06 (Parts A to D exact Fractions: L06.html:240 hypothesis, lab-E4-L06-1.py docstring) and L07 (Parts A to E exact Fractions: L07.html:132 hypothesis and :149, lab-E4-L07-1.py docstring and Parts A to E code; Part F double precision). A reader cannot place the arithmetic of L06 or L07 from the hub.",
     "fix": "In index.html:38 and :167 add L06 (Parts A to D) and L07 (Parts A to E) to the exact-Fraction list, e.g. 'Labs L01, L02, L04, L05, L06 (Parts A to D), L07 (Parts A to E) and L09, and Part A of the L03 lab, use exact Fraction arithmetic.' Leave Part F of L07 and Part E of L06 in the seeded-simulation sentence."},
    {"id": "E4c10-milgrom-abstract", "check": "2.1-citations", "location": "course/modules/E/E4/L09.html:512; references/references.json:17291-17315; ledgers/E4/scripts/E4-c-r10/out/crossref_milgrom.json",
     "status": "PASS",
     "evidence": "Crossref (plain curl, api.crossref.org/works/10.1016/0022-0531(82)90046-1) returns title 'Information, trade and common knowledge', container 'Journal of Economic Theory', volume 26, issue 1, pages 17-27; matches the registry record. Crossref carries no abstract for this DOI, and doi.org returned HTTP 302 to plain curl, which was not followed further (no bot-check bypass). L09 attributes no result to the paper (L09.html:512 says so; grep 'Milgrom' finds only the reference line), so no abstract-level attribution is made or checked. Recorded as could-not-check for the abstract."},
    {"id": "E4c10-independent-L07-L08", "check": "2.2-numbers / 2.4-mathematics", "location": "ledgers/E4/scripts/E4-c-r10/independent_L07_L08.py; out/independent_L07_L08.out",
     "status": "PASS",
     "evidence": "Own solver (Newton on the clearing residual at (1,0),(0,1), uninformed posterior from Cov/Var of (v,p)) gives theta_s = 3/7 and theta_u = 6/7 at the base instance and 0.368165249, 1.570838396 at an alternative parameter set, equal to the closed form; max |residual| 8.9e-16 over 400 (s,u) points. rho^2 sweeps: 4/9, 1/3, 1/6, 0.055556, 0.015152 (sd), 1/6, 1/3, 9/22 (lambda), 4/9, 1/3, 1/6 (a); Part F sample 0.330625. L08: G(1) = 0.127706406, G(0) = 0.173286795, G(1e-5)-G(0) = -6.25e-12; lam* at costs 0.12..0.18 match the lab to 9 decimals with gaps below 1e-13."},
    {"id": "E4c10-independent-L08-partA", "check": "2.2-numbers / 2.5-labs", "location": "ledgers/E4/scripts/E4-c-r10/independent_L08_partA.py; out/independent_L08_partA.out",
     "status": "PASS",
     "evidence": "Replay of L08 Part A with random.Random(20261103), 20000 draws, lambda 0.5: sample slope 0.1595 against formula b_y/beta = 0.160494 (printed as 0.1605), difference 0.0010 < 0.02; matches the expected block."},
    {"id": "E4c10-independent-L09", "check": "2.2-numbers / 2.5-labs", "location": "ledgers/E4/scripts/E4-c-r10/independent_L09.py; out/independent_L09.out",
     "status": "PASS",
     "evidence": "Own integer enumeration of the 15625 bets: state 1 and state 4 each have 500 bets strictly positive for both traders and 625 bets nonnegative on the meet, all with zero posteriors (0 nonzero); first witness bets (-1,2,-2,-2,-2,-2) and (-2,-2,-2,-2,1,2) equal the printed ones; no strict bet is nonnegative on the meet (theorem check)."},
    {"id": "E4c10-twin-equals-page", "check": "2.5-labs", "location": "course/modules/E/E4/L07.html, L08.html, L09.html data-run blocks vs tests/labs/E4/lab-E4-L0{7,8,9}-1.py; out/twin_vs_page.out",
     "status": "PASS",
     "evidence": "ledgers/E4/scripts/E4-c-r10/twin_vs_page.py: page data-run code equals the twin (trailing newline ignored) for L07, L08, L09 (one block each)."},
    {"id": "E4c10-expected-equals-stdout", "check": "2.5-labs", "location": "L07.html:335-362; L08.html:549-568; L09.html:264-281 (expected blocks)",
     "status": "PASS",
     "evidence": "ledgers/E4/scripts/E4-c-r10/expected_vs_output.py: expected block (one per page) equals standalone twin stdout line for line: L07 28 lines, L08 20 lines, L09 18 lines, rc 0 for each (out/expected_vs_output.out)."},
    {"id": "E4c10-L06-statements-used", "check": "2.4-mathematics", "location": "course/modules/E/E4/L06.html:56-98, 173-200, 212-225, 234-236",
     "status": "PASS",
     "evidence": "Re-read this round. Definitions 6.1 and 6.2, A1 (normal primitives, sigma_u^2 > 0), A2 (lambda in (0,1)), A3, A4 (clearing, residual sentence changed at :86), G; Prop 6.7 closed form (kappa = a sigma_e^2/lambda, tau_bar, theta_s, theta_u = kappa theta_s); Cor 6.8 (proof sentence changed at :225, same formula); Remark 6.10 (sigma_eta^2 >= sigma_e^2 > 0). L07 and L08 use exactly these statements; the changed sentences add justification and do not change a result. Lab-E4-L06-1 Part A prints kappa 2, tau_eta 1/2, theta_s 3/7 (L06 expected block), which L07 cites."},
    {"id": "E4c10-dag-closure", "check": "2.9-dag", "location": "L07.html:37-38; L08.html:37-38; L09.html:37-38 (concept links); curriculum/curriculum.json (E4 prereqs E2, E3, M7 and their closure)",
     "status": "PASS",
     "evidence": "Closure of E4 computed from curriculum.json parts[].modules[].prereqs: {E1,E2,E3,E4,M1,M2,M3,M4,M7,P0.1}. All 19 concept names used with data-concept in L07-L09 belong to modules in this closure or to E4 (arrow-debreu-equilibrium, grossman-stiglitz-paradox, no-trade-theorem, noisy-rational-expectations-equilibrium, price-informativeness). The 14 concepts.html anchors used by L07-L09 all exist (grep)."},
    {"id": "E4c10-banned-phrases", "check": "2.9-prose", "location": "L07.html, L08.html, L09.html, cards.json, lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py",
     "status": "PASS",
     "evidence": "grep (case-insensitive) for TODO, TBD, lorem, beyond the scope, for brevity, details omitted, can be shown, it is important, well known, studies show, experts agree, obviously, clearly, left as an exercise, you can add, round N, this round, verif, builder: no hits in prose, cards or lab text (only Python type hints contain '...'). BUILDER_RULES 1.3-1.4 clean."},
    {"id": "E4c10-cards-count-and-changed", "check": "2.7-cards", "location": "course/modules/E/E4/cards.json (243 cards; changed E4-c181..c188, c201, c223, c224)",
     "status": "PASS",
     "evidence": "ledgers/E4/scripts/E4-c-r10/cards_check_r10.py (out/cards_check_r10.out): 243 cards, no duplicate ids, fronts or backs; L07 21, L08 43, L09 23 cards in this slice. Each changed card was re-read against the lesson text and Lab 1 output this round; card numbers (0.657828572, 0.088941, 1.83e-15, 7.71e-03, -6.71e-03, 0.013061, 0.166667, 500, 625, 15625, 1.332e-15, 0.1595, 0.1605, 0.330625) all appear in their lesson or its expected block. Card id gaps (E4-c202, c212, c213, c216, c233, c249, c250) are not defects; c233 was merged into c201."},
    {"id": "E4c10-notation-scan", "check": "2.4-mathematics / notation", "location": "L07.html, L08.html, L09.html math spans (405, 827, 382); notation/notation.json",
     "status": "PASS",
     "evidence": "ledgers/E4/scripts/E4-c-r10/notation_scan_r10.py (out/notation_scan_r10.out): registered macros used are Corr, Cov, E, Normal, R, Var, each with its registered meaning (Normal(mu, sigma^2) as used in L08 A2 and Mech 3). No T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. Bare N (L08) and S (L09) are local per the registry note. The 's'-hit for '\\N' is a substring of \\Normal, not a use of the natural-number macro."},
    {"id": "E4c10-ruff-mypy-repo", "check": "2.5-labs / tooling", "location": "repo: ruff check ., mypy --no-incremental, pytest -k E4",
     "status": "PASS",
     "evidence": "ruff check . 'All checks passed!'; mypy --no-incremental 'Success: no issues found in 385 source files'; ruff format --check tests/labs/E4 '12 files already formatted'; pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k E4: 13 passed (out/ruff_check_repo.out, mypy_repo.out, ruff_twins.out, pytest_E4.out)."},
]

rows.extend(NEW)

fragment = {
    "unit": "E4",
    "slice": "c",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for E4-c round 10 (did not build E4)",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-E4-c",
    "scratch": "/tmp/e4c10_run (twins run from scratch dirs with python -I -W error); ledgers/E4/scripts/E4-c-r10/out/ for all outputs",
    "verified_at": "2026-11-05T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "grossman1980 / Grossman and Stiglitz (AER 1980): still no registry record (B1, REFERENCE_REQUEST R-E4-1). L08 cites no key, which is correct; the paradox is taught as a model result.",
        "mascolell1995microeconomic author conflict (B3) is outside this slice (L07 to L09 cite no Mas-Colell key).",
        "milgrom1982information: record matches L09.html:512 (title, JET 26(1), pages 17-27, 1982) and Crossref metadata fetched this round; abstract not readable with plain curl.",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 10. Pages and twins for L07, L08, L09 have sha256 identical to the round-9 pin: "
        "L07.html 7c32c928..., L08.html f89d8940..., L09.html 1c2286b8..., lab-E4-L07-1.py 87e161f2..., lab-E4-L08-1.py 9b9f371b..., lab-E4-L09-1.py d72ab42a.... "
        "The only FAIL is the hub data-status sentence (index.html:38, :167), which is outside the three pages but lists the arithmetic of L07 and L09 labs. "
        "Round-9 locators corrected: L08 footer 806 -> 811; hub titles index.html:136/137 -> 148/149; cards.json line ranges replaced by card ids (243 cards now). "
        "Row ids from round 9 are kept; every round-9 PASS row was re-checked this round against the unchanged subject, with fresh command output."
    ),
    "summary": "E4-c round 10: 147 round-9 rows kept, 8 new rows. One FAIL (hub data-status arithmetic list omits L06 and L07). All lesson math, labs, expected blocks, cards, notation and DAG rows PASS.",
    "could_not_check": (
        "(1) Milgrom and Stokey (1982) abstract: not readable with plain curl (Crossref has no abstract; doi.org 302 not followed). L09 attributes no result to it. "
        "(2) Grossman and Stiglitz (1980): no registry record (B1); L08 cites no key, so nothing to check. "
        "(3) Browser rendering beyond page_smoke: no figures on these pages. "
        "(4) Pyodide timing measured by page_smoke only (L09 lab 5.0 s, under 10 s). "
        "(5) Full repository pytest was not run (only the E4 subset and the three labs); full CI gate not run, slice scope only. "
        "(6) Project graders (grader/, project.html) and L01-L06 pages are other slices; L06 was read only at the locators cited by L07-L08."
    ),
}

import sys
sys.path.insert(0, str(BASE / "tools"))
import ledger
problems = ledger.validate(fragment, "E4-c")
print("validation problems:", problems)
Path(BASE / "ledgers/E4/E4-c.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
from collections import Counter
print("rows", len(rows), Counter(r["status"] for r in rows))
