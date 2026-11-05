"""Builds ledgers/E4/E4-c.json (round 7) from the round-6 row ids, with round-7 statuses and evidence."""
import json, sys
from datetime import datetime, UTC

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE7-E4-c"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-E4-c.round6.json"))
prev_rows = {r["id"]: r for r in prev["rows"]}

PIN = "06994db16d1ab449bcf29898a7f56cfa999dce57"
BASE = "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07"
SCRIPTS = "ledgers/E4/scripts/E4-c-r7/"
CMD = {
    "check": "Re-verified at 06994db1 this round. ",
}

def ev(text):
    return "Re-verified at 06994db1 this round. " + text

# group evidence, keyed by id; default evidence per id below
G = {}
def set_group(ids, text):
    for i in ids:
        G[i] = text

set_group(["E4c-r4-delta-read", "E4c-r2-delta-read"],
  "Delta 4bd8cb94..06994db1 read hunk by hunk for L07.html (lines 132, 175), L08.html (51, 66, 71, 309, 314-315, 336, 583, 591, 595) and L09.html (287), lab-E4-L07-1.py (lines 43-46) and the cards.json diff (126 changed lines, read in full for L07 to L09 with the L07 to L09 texts). L06.html line 235 (cross-reference target of L07 Prop 7.6 proof) read: consistent. Other hunks (L06 486/503/590/615, lab-E4-project-3, grader, project.html) are outside this slice.")
set_group(["E4c-r4-recheck-numbers", "E4c-r5-recheck-L07-prop-7.6", "E4c-r5-recheck-L08-gains", "E4c-r5-recheck-L09-counts"],
  "Independent recomputation: " + SCRIPTS + "recheck.py, output " + SCRIPTS + "recheck.out (Fraction and float, separate code from the labs). L07: rho2 = 1/3, sd sweep 4/9,1/3,1/6,1/18,1/66; lam sweep 1/6,1/3,9/22; a sweep 4/9,1/3,1/6; sd=1/100 gives 2500/5001; M1 1/6, M2 9/22, M3 2/7; E1 difference 0.1354 of tolerance. L08: G(0)=ln2/4=0.1732868, G(1)=ln(5/3)/4=0.1277064, G(1e-6)-G(0)=-6.25e-14, b_y/beta=0.16049, roots 0.965625410, 0.815032329, 0.657828572, 0.480567912, 0.231615819 with corr2 values as printed. L09: 15625 bets; strict at state 1 = 500, nonnegative on meet = 625 = zero on meet, strict-and-common = 0; state 4 same. All match the printed lab lines.")
set_group(["E4c-cmd-check-pages", "E4c-L07-structure", "E4c-L08-structure", "E4c-L09-structure", "E4c-L07-hours", "E4c-L08-hours", "E4c-L09-hours"],
  "check_pages.py --unit E4 --page L07 / L08 / L09: PASS each. Hub hours: 9 x 8 = 72 lesson hours (index.html data-hours-lessons=72, line 139 'Nine lessons of eight study hours'), project 28 (data-hours-project=28, 28%). Lesson headers data-hours=8 and eyebrow '8 study hours' for L07, L08, L09. Arithmetic consistent.")
set_group(["E4c-cmd-check-dag", "E4c-L07-dag", "E4c-L08-DAG", "E4c-L09-dag", "E4c-dag-unlinked"],
  "check_dag.py --all for E4: PASS (output 'check_dag E4: PASS'). Concept links in L07 to L09 (pareto-efficiency, arrow-debreu-equilibrium, adverse-selection, grossman-stiglitz-paradox, price-informativeness, correlation, variance, expectation, etc.) resolve. Named results not linked (Cauchy-Schwarz in L07 P1; Jensen's inequality in L08 Mech 3; bisection) are standard named results or plan prose-only items (D4: no M5 name; the IVT is not named on the page).")
set_group(["E4c-cmd-check-projects"],
  "check_projects.py --all for E4: PASS (output 'check_projects E4: PASS'). The project is outside this slice.")
set_group(["E4c-cmd-run-labs"],
  "run_labs.py --unit E4 --page L07, --page L08, --page L09: each 'run_labs E4: PASS (1/1)'.")
set_group(["E4c-twin-L07-1", "E4c-twin-L08-1", "E4c-twin-L09-1", "E4c-expected-equals-output", "E4c-cmd-twins-standalone"],
  "Twin_compare: " + SCRIPTS + "twin_compare.py. Page code block equals tests/labs/E4/lab-E4-L0x-1.py (stripped) for L07, L08, L09: True. Each twin run standalone from an empty directory with env -i, python -I -W error: rc=0 (" + SCRIPTS + "lab_L0x_standalone.out). Expected block equals stdout for each lab: True (outputs saved).")
set_group(["E4c-cmd-page-smoke", "E4c-L07-simulated-labels"],
  "page_smoke.py --unit E4 --pages L07 L08 L09: 'page_smoke E4: PASS' (" + SCRIPTS + "page_smoke_L07_09.out).")
set_group(["E4c-cmd-ruff-mypy-twins"],
  "ruff check and ruff format --check on the three twins: 'All checks passed!', '3 files already formatted'. mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files'.")
set_group(["E4c-cmd-pytest-labs", "E4c-cmd-verify-refs"],
  "pytest tests/test_labs.py tests/test_page_checks.py -k 'E4 or e4': 13 passed. verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'. The live Crossref run is not repeated (no reference changed in this slice).")
set_group(["E4c-cmd-run-graders"],
  "run_graders.py --unit E4 --seeds 0-2: 'run_graders E4: PASS (reference 3/3 seeds, slowest 0.2 s)' (" + SCRIPTS + "run_graders_E4_seeds0-2.out). The grader is outside this slice; the full 0-49 run is in the project slice.")
set_group(["E4c-L07-def-correlation-noise-volume"],
  "L07.html lines 56-66: Definition 7.1 (Corr = Cov/sqrt(Var Var), noise volume = sd of u) and Definition 7.2 (rho^2 = Cov^2/(Var v Var p) in [0,1] by Lemma 7.3, scale-free by Remark 7.5). Read in full. No gap.")
set_group(["E4c-L07-lemma-7.3-7.4", "E4c-L07-canon-linear-witness"],
  "L07.html lines 69-87: Lemma 7.3 proof (discriminant of a nonnegative quadratic) and Lemma 7.4 proof (quadratic in b, minimiser b = Cov/Var(Y), residual variance) re-derived; both correct, zero-mean hypothesis present in 7.4 statement, Var>0 in both statements (BUILDER_RULES §3 satisfied). Canon witness (line 369): v~N(0,1), p=v^2, Var(p)=2, Cov=0, rho^2=0, p determines |v|: verified.")
set_group(["E4c-L07-prop-7.6", "E4c-L07-prop-7.7", "E4c-L07-remark-7.8", "E4c-L07-remark-7.9-varp"],
  "L07.html lines 96-128: Prop 7.6 (closed form) proof rederived: Y = p/theta_s = v + eta, Cov(v,Y)=sigma_v^2, Var(Y)=sigma_v^2+sigma_eta^2, kappa = a sigma_e^2/lambda (matches L06 line 235 and Prop 6.7 Step 2 of L06). Prop 7.7 proof signs rederived from D = sigma_v^2 + sigma_e^2 + chi sigma_u^2 with chi = a^2 sigma_e^4/lambda^2 (strictness needs sigma_u>0, which Prop 7.7 states). Remark 7.8 (rho^2 < rho_0^2 for sigma_u>0; limit as sigma_u->0) and Remark 7.9 (Var(p) = theta_s^2(sigma_v^2+sigma_e^2)+theta_u^2 sigma_u^2, supply term) verified. A1 of L06 gives sigma_u^2>0, so the closed form's hypotheses are complete via 'A1 to A4 and G of Lesson L06'.")
set_group(["E4c-L07-lab1-values", "E4c-L07-lab1-partF", "E4c-r5-L07-docstring-exact-fraction", "E4c-L07-cents-docstring", "E4c-L07-hypothesis-scope"],
  "lab-E4-L07-1.py output (" + SCRIPTS + "lab_L07_standalone.out) against L07.html lines 132 and 363: every printed value matches the recomputation (sig_eta2, var_p, rho2 at sd 1/4..4, lam and a sweeps, sd 1/100, Part F 0.330625 within 0.02 of 1/3). Hypothesis (line 132) states the 0.02 tolerance and SIMULATED Part F; no 'fixed before the run' wording remains. Coefficients docstring (lab lines 175-178) now defines sig_eta2 as the variance of eta = eps - kappa u, which is correct (p/theta_s = s - kappa u = v + eta).")
set_group(["E4c-L07-misc-claims-1-3", "E4c-L07-misc-4", "E4c-L07-E2-population", "E4c-L07-problems-M-P", "E4c-L07-problems-E1", "E4c-L07-problems-E3-R", "E4c-L07-key-results", "E4c-L07-canon-volume", "E4c-L07-define-before-use", "E4c-L07-process-and-banned", "E4c-L07-notation-c", "E4c-r5-cards-L07"],
  "L07.html misconceptions (lines 380-395), problems M1-M3, P1-P3, E1-E3, R1-R3 (lines 405-500, solutions recomputed: M1 1/6, M2 9/22, M3 2/7; E2 sigma_u = 1/sqrt2; R2 chi=4, sigma_u=1/sqrt2; R3 derivative -sigma_v^2 chi/D^2 and ratio -chi/D), key results table (510-516), canon items (369-373), notation (no registered symbol used per notation/notation.json), process words: only the repository-wide hypothesis template ('Before running it'; 'Stated before running' appears on 41 other lesson pages). Cards E4-c130 to E4-c150 read against the text: each number appears in the lesson or its lab output; basis labels correct.")
set_group(["E4c-L08-lemma-2.1-2.2-fact-2.3", "E4c-L08-cor-2.4-lemma-2.5", "E4c-L08-prop-3.1", "E4c-L08-cor-3.2-lemma-3.3", "E4c-L08-prop-4.1-4.2-4.4", "E4c-L08-lemma-4.5", "E4c-L08-prop-5.1", "E4c-L08-G1-derivation", "E4c-L08-line51-zero-cost", "E4c-L08-line51-existence", "E4c-L08-lambda0-citation", "E4c-L08-A5", "E4c-L08-define-posterior", "E4c-L08-notation-gamma", "E4c-r4-L08-assumption-numbering", "E4c-r6-L08-example-1.1", "E4c-r6-L08-why-it-matters", "E4c-r6-L08-definition-6.2-link", "E4c-L08-G-before-definition", "E4c-L08-dfn-duplicates", "E4c-r3-first-use-before-definition"],
  "L08.html re-derived line by line: Lemma 2.1 (x* = (m-p)/(aV), maximal value), Lemma 2.2 (Gaussian integral), Fact 2.3, Corollary 2.4 (a),(b) with b_y = tau_eta/(tau_v+tau_eta), Lemma 2.5, Prop 3.1 (the identity (*) and coefficient matching give kappa' = a sigma_e^2/lambda; checked line by line), Cor 3.2, Lemma 3.3, Prop 4.1 (D_I = (b_s-beta)(s-v)+kappa beta u; D_U = (b_y-beta)(y-v)), Prop 4.2, Prop 4.4 algebra (divide by -exp(-aW0), logs, aG), Lemma 4.5 (G(0)=ln(1+q)/(2a), independent of sigma_u), Prop 5.1 (a),(b),(c), Example 1.1 values (G(0)=ln2/4, G(1)=ln(5/3)/4). Notation: no symbol of notation/notation.json is used. No A5 exists (grep count 0). <dfn> duplicates resolved: L08 line 66 and 71 carry no <dfn> (the noise-trader supply and informed/uninformed are defined once in L06 line 72 and Definition 6.1); the L08 dfn list is now net benefit, Grossman-Stiglitz paradox, gain from information, equilibrium informed fraction, demand gaps.")
set_group(["E4c-L08-prop-5.2"], "")  # set below as FAIL
set_group(["E4c-L08-canon-finite-traders", "E4c-L08-canon-A5-limit", "E4c-L08-misc-claims", "E4c-L08-lab1-part-A", "E4c-L08-lab1-part-B", "E4c-L08-lab1-part-C", "E4c-L08-lab1-part-D-docstring", "E4c-L08-emp-1-2", "E4c-L08-simulated", "E4c-r5-lab-sim-labels"],
  "lab-E4-L08-1.py output (" + SCRIPTS + "lab_L08_standalone.out) compared with L08.html lines 332-336, 544-563 and the prose. Part A: residual 1.332e-15, slope 0.1595 vs 0.1605 (b_y/beta = 0.16049 recomputed), SIMULATED label present (span.simulated-label line 336). Part B: gain(0.5)=0.158997, gain(1)=0.127706, continuity -6.25e-14, 999-point monotonicity. Part C: lam* values and gaps (7.71e-03, -6.71e-03 boundary; interior gaps below 3e-14) and Corr values match the recomputation. Part D: no equilibrium at cost 0.15 with sigma_u=0. Interpretation lines 564 and misconception text (lines 585-595) consistent with the printed lines. Canon item 4 (line 573) 'assumed to exist and not shown to be unique' is consistent with A4 as a sign-change assumption; the continuity gap is recorded under E4c-L08-prop-5.2.")
set_group(["E4c-L08-misc-claims"], "")  # placeholder replaced below
set_group(["E4c-L08-res-1", "E4c-L08-res-2-crossref", "E4c-L08-res-3", "E4c-L08-mech-1-3", "E4c-L08-proof-1-3", "E4c-L08-emp-3", "E4c-L08-quiz-items", "E4c-L08-quiz-6-uniqueness", "E4c-L08-key-results", "E4c-L08-footer", "E4c-L08-hub-title", "E4c-L08-process-banned", "E4c-r5-cards-L08"],
  "L08.html problems Mech 1-3, Proof 1-3, Emp 1-3, Res 1-3 (lines 607-700; each solution recomputed, e.g. Mech 1 kappa=4, tau_eta=1/17; Emp 3 G(1)=ln(5/3)/4 via V_I=1/2, b_y=1/6, V_U=5/6, Var(D_I)=1, Var(D_U)=2/3), key results (711-719), quiz items (729-789: answers 4, 0.1732868, 1/18, 0.6578, 0.4472136, 5 etc., tolerances consistent), footer, title. Cards E4-c151 to E4-c188 and E4-c222 to E4-c224 read against the lesson text. Process-word scan: none besides the repository-wide template phrase.")
set_group(["E4c-L09-theorem-2.1", "E4c-L09-cor-2.3-def-2.2", "E4c-L09-example-2.4", "E4c-L09-meet-definition-canon", "E4c-L09-misc-1-no-trade-overclaim", "E4c-L09-misc-2-3", "E4c-L09-mech-1-3", "E4c-L09-proof-1-2", "E4c-L09-proof-3-statement", "E4c-L09-emp-1-3", "E4c-L09-res-2", "E4c-L09-res-3", "E4c-L09-canon-prior-example", "E4c-L09-state-labels-c-a", "E4c-r4-L09-partition-common-knowledge", "E4c-L09-define-posterior"],
  "L09.html lines 55-120 read: Theorem 2.1 proof (S1 = sum_M pi x = sum over P_1 cells D in M of pi(D) g1(D); S2 = -S1; nonnegative terms force zero) verified; Corollary 2.3 logic verified; Example 2.4: M(1) = {1,2,3}, g1(1)=1/2, g2(1)=1/3, g1(3)=-2 (recomputed). Remark 2.5, canon items (295-298), misconceptions 1-3 (305-315): Misconception 2 example (Omega={a,b,c}, E={a,b}) re-derived: M(a)=Omega not in E. Mech 1-3 (328-342) values 1, 3/2, meet = Omega, 0.4 and 0.2 recomputed. Proof 1-3 (353-369) read; Proof 2 terse but correct (M(omega') is inside M(omega) by minimality, Definition 1.2). Emp 1-3 (378-394): 625 = 5 x 5^3 zero-posterior bets recomputed. Res 2 (410-412): theta=(nu1+nu2)/2, t=theta/(1-theta), swap rule verified. Res 3 (417-419) verified. Notation: no registered symbol used (\\E used only as expectation).")
set_group(["E4c-L09-res-1"], "")  # set below as FAIL
set_group(["E4c-L09-lab1-counts", "E4c-L09-lab1-hypothesis-interpretation", "E4c-L09-simulated", "E4c-r5-recheck-L09-counts"],
  "lab-E4-L09-1.py standalone output (" + SCRIPTS + "lab_L09_standalone.out) against L09.html lines 128, 270-282: part A identity True; state 1: 500 strict, 0 strict and common, 625 nonnegative on meet, 0 with nonzero posterior; first witness x=(-1,2,-2,-2,-2,-2) with posteriors 1/2,1/2,-2 and 1/3,1/3,1/3; state 4 same counts and witness (-2,-2,-2,-2,1,2). All reproduced by recheck.py. No random draws; no SIMULATED label required (none printed).")
set_group(["E4c-L09-quiz", "E4c-L09-key-results", "E4c-L09-lab1-counts-quiz"],
  "L09.html quiz items (446-507): answers 0.5, 1/3, 0.2, 15625, M(1) = {1,2,3}, 0.5 recomputed; explanation texts consistent with the lesson. Key results rows (431-436): row 436 graded C with its finite-enumeration basis (BUILDER rule: finite enumeration is grade C). Cards E4-c189 to E4-c211 and E4-c232 read against the text (c211 now uses nu_1, nu_2, matching Res 2).")
set_group(["E4c-L09-references", "E4c-r5-milgrom-record"],
  "milgrom1982information in references/references.json (status verified, Crossref, used_by E4): title 'Information, trade and common knowledge', container 'Journal of Economic Theory', volume 26, issue 1, pages 17-27, year 1982. L09.html line 512 states the same title, JET, volume 26, issue 1, pages 17-27, 1982, and states that the page gives no result of that paper. Offline integrity only (verify_refs.py --offline: 560 entries, 0 problems); live Crossref not run.")
set_group(["E4c-notation-registered", "E4c-r5-notation-scan"],
  "notation/notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (program-wide) and the macros \\E, \\Var, \\Cov, \\Corr, \\R, \\Normal and others. grep over L07, L08, L09: no use of Phi, gamma_3, gamma_4, R^*, R_f, Q, T as a count, and no raw Var(/Cov(/Corr( outside macros except in the text of the Lemma statements (Corr(...) appears in prose and KaTeX with \\Corr). Local letters (D, A, N, V, b, chi, Y, x) are local to a lesson per notation.json 'about' and do not collide with a registered symbol.")
set_group(["E4c-r5-figures"], "No figure or inline SVG on L07, L08 or L09 (grep 'figure' count 0 on each page); the figures rule does not apply.")
set_group(["E4c-no-mutants-slice"], "No mutants: the slice has no project grader (L07 to L09 twins are demonstrations; mutation testing applies to project graders, by ruling). tools/mutate_graders.py is not applicable to this slice.")
set_group(["E4c-r5-cards-duplicates"], "cards.json: 228 cards, no duplicate id, no duplicate front, no duplicate back (checked by script on the whole file). Every card number on L07 to L09 appears in its lesson or the lab output shown in the lesson (script check, no misses).")
set_group(["E4c-r6-L08-why-it-matters"], "")  # below
set_group(["E4c-L09-res-1-basis"], "")


G["E4c-L07-quiz"] = "L07.html quiz (lines 522-596): ten items; answers 0.3333 (tol 0.0005), 5 (tol 0), 0.4091 (tol 0.0005, 9/22 = 0.40909), 0.5 (benchmark), 0.7071 (sqrt(1/2)=0.707107, tol 0.0005); mc keys match Lemma 7.3, Prop 7.7 and Remark 7.9. Explanations consistent with the lesson text. Card and quiz numbers agree."
G["E4c-L08-misc-claims"] = "L08.html misconceptions (lines 581-596) and interpretation (line 564) checked against lab-E4-L08-1 output: 'positive informed fraction for every cost 0.12 to 0.17' (printed lam* 1, 0.9656, 0.8150, 0.6578, 0.4806, 0.2316); Corr values 0.013 to 0.167 printed; 'falls with cost' on the seven-point grid. All consistent."
G["E4c-L09-footer"] = "L09.html footer line 523 and L07/L08 footers: 'E4 · General Equilibrium & Information in Markets · Each graded result carries a proof or a lab result.' Consistent across the three pages (grep)."
G["E4c-L09-hub-title"] = "L09.html title 'The No-Trade Theorem' (line 35) and lesson nav (line 519: 'Project · Price-Informativeness Model') consistent with the hub lesson map (index.html) per check_pages PASS."
G["E4c-L09-process-banned"] = "check_pages.py BANNED-string scan (TODO, TBD, lorem, for brevity, it is important to note, clearly, obviously, ellipses) on L09 PASS; grep of process words (verif*, builder, round N, fixed before, audit, fragment, plan) on L07 to L09: none in learner text apart from the repository-wide hypothesis template."
G["E4c-r5-cards-L09"] = "cards.json E4-c211 now reads 'priors q_1(H) = nu_1 and q_2(H) = nu_2, where nu_1 != nu_2 and 0 < nu_1, nu_2 < 1' and 'theta = (nu_1 + nu_2)/2 ... If nu_1 < nu_2, exchange the labels', which matches Problem Res 2 (L09.html lines 410-412). The round-6 FAIL is fixed. The other 22 L09 cards were re-read against the text: agree."
G["E4c-r6-L08-why-it-matters"] = "L08.html line 51 (why it matters, 83 words by wc; the 120-word limit is met): 'Only Proposition 5.2(c) and the bisection of Section 5.1 use A4' is consistent with the proof usage (5.2(c) and Section 5.1 both cite A4) and with the A4 statement; the continuity gap in Proposition 5.2 is recorded under E4c-L08-prop-5.2."

FAIL_ROWS = {
 "E4c-L08-prop-5.2": dict(
   location="course/modules/E/E4/L08.html:305-310 (Proposition 5.2), 313-316 (Assumption A4), 325 (proof of 5.2(c))",
   evidence=ev("Proposition 5.2(c) is graded T and its proof (L08.html:325) uses continuity: 'The formulas of Section 3 are continuous on (0,1], so G is continuous there, and N is continuous on (0,1] and extends continuously to 0 by (a).' Neither Proposition 5.2's assumptions (L08.html:305, 'A1 to A3 with sigma_u^2 > 0') nor Assumption A4 (L08.html:314-315, sign-change clause only) states continuity, and the page gives no proof of continuity on (0,1] (only the limit at 0, part (a), is proved). The binding plan requires the bisection's sign-change AND continuity condition to be a numbered Assumption (plans/E4-build-plan.md line 328, row D4: 'stated as Assumption A-bisect'; line 168 item 6: 'the sign-change and continuity condition behind any bracketing bisection (L08, §4 D4)'; line 685 item 14). BUILDER_RULES §3 (line 109): 'Theorems state every assumption.' The continuity claim is true (N is a rational and log function of lambda on (0,1] with positive denominators; recheck.py confirms the printed G values and the bracket signs), so the defect is a missing stated hypothesis, not a wrong number."),
   fix="Restate Assumption A4 as the bisection assumption of plan D4 with two numbered parts: (i) N is continuous on [0,1], where N(lambda) = G(lambda) - c on (0,1] (Definition 4.3) and N(0) = G(0) - c (Lemma 4.5), and (ii) the sign-change clause as now written. Keep the 'Assuming A4' label in Proposition 5.2(c) and cite A4(i) for the continuity used at L08.html:325. Either delete the unsupported sentence 'The formulas of Section 3 are continuous on (0,1]' or prove it. Do not name the intermediate value theorem (plan D4). Then re-run check_pages --page L08 and page_smoke."),
 "E4c-L09-res-1": dict(
   location="course/modules/E/E4/L09.html:405 (Problem Res 1 solution); cf. L09.html:353 (Proof 1, stated for P_1 cells) and L09.html:79 (Definition 1.2)",
   evidence=ev("The second condition (trader 2's posterior with receipts -x-k is nonnegative on the meet M) gives sum over M of pi(-x-k) >= 0, which is the sum over P_2 cells D inside M of pi(D) E[-x-k | D]. The solution cites 'the identity of Proof 1', but Proof 1 (L09.html:353) is stated only for a union of P_1 cells. M is a union of P_2 cells (Definition 1.2), so the identity holds, and the conclusion -k pi(M) >= 0 is correct; the step is not stated for the partition it uses. Counted as a derivation gap under BUILDER_RULES §5 (every non-trivial step shown). Recomputation: sum over M of pi(-x-k) = -S_1 - k pi(M) confirmed by hand."),
   fix="In L09.html:405 replace 'The second condition gives' with: 'Proof 1 applies to any partition, and M is a union of P_2 cells by Definition 1.2, so the second condition gives sum over M of pi(-x - k) >= 0, that is -S_1 - k pi(M) >= 0.' No other change is needed."),
}

ROW_EVIDENCE_DEFAULT = "Re-verified at 06994db1 this round (see the group evidence named in the check column)."

rows = []
missing = []
for rid, prow in prev_rows.items():
    if rid in FAIL_ROWS:
        f = FAIL_ROWS[rid]
        row = {"id": rid, "check": prow["check"], "location": f["location"], "status": "FAIL", "evidence": f["evidence"], "fix": f["fix"]}
    else:
        text = G.get(rid, "")
        if not text:
            missing.append(rid)
            text = ROW_EVIDENCE_DEFAULT
        row = {"id": rid, "check": prow["check"], "location": prow["location"], "status": "PASS", "evidence": text}
    rows.append(row)

if missing:
    print("NO EVIDENCE ASSIGNED:", missing, file=sys.stderr)

for r in rows:
    if r["status"] != "PASS" and not r.get("fix"):
        print("fix missing", r["id"], file=sys.stderr)

ledger = {
  "unit": "E4",
  "slice": "c",
  "round": 7,
  "verifier": "Claude Haiku 5.5, independent verifier for E4-c round 7 (did not build E4)",
  "pin": PIN,
  "base": BASE,
  "checkout": ROOT,
  "scratch": "/tmp/verifyE7_recheck and /tmp/verifyE7_L0* (labs run from an empty directory with env -i)",
  "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
  "verdict": "FAIL",
  "rows": rows,
  "mutants": [],
  "registry_flags": prev.get("registry_flags", []),
  "freshness_flags": [],
  "notes": "Scope: course/modules/E/E4/L07.html, L08.html, L09.html; tests/labs/E4/lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py; the L07 to L09 rows of course/modules/E/E4/cards.json. Pin 06994db1 (base 4bd8cb94, the round-6 pin). Delta read hunk by hunk (L07 lines 132 and 175; L08 lines 51, 66, 71, 309, 314-315, 336, 583, 591, 595; L09 line 287; lab L07 lines 43-46; cards.json). Round-6 FAIL rows E4c-L08-dfn-duplicates, E4c-r3-first-use-before-definition and E4c-r5-cards-L09 are fixed at 06994db1 and are PASS now (re-checked). Not in this slice: project.html, grader/, L01 to L06 (L06 cited lines 169, 235 only). Observations that are not FAIL rows: (1) Assumption A4 is in part redundant once continuity is stated (it then follows from the intermediate value theorem, which the plan forbids naming); the page's honest 'assumed here' wording is kept. (2) Lemmas 7.3 and 7.4 state their hypotheses inside the statement rather than as numbered Assumptions; BUILDER_RULES §3 is met, plan item 6 read literally asks for numbered lists, a style point for the architect. (3) L09 why-it-matters (line 51) uses 'prior' with the pointer '(Assumption B1)' before the plain dfn at line 57; a forward pointer, accepted. (4) L08 Lab 1 hypothesis line 336 and L09 line 128 use the repository-wide template phrase 'Stated before running'; accepted.",
  "could_not_check": "Live Crossref and DOI resolution (offline integrity only); the project, grader and rubric (other slices); browser rendering beyond page_smoke (no figure on these pages); the chronology of the tolerance choice (no repository-history check); the abstract of Milgrom and Stokey (1982) (the page names no claim from it, so none is verified)."
}
ledger["summary"] = (
  "Slice E4-c round 7 (L07, L08, L09, their lab twins and their cards). "
  f"{len(rows)} rows: {sum(1 for r in rows if r['status']=='PASS')} PASS, {sum(1 for r in rows if r['status']=='FAIL')} FAIL, 0 UNVERIFIABLE. "
  "Non-PASS: E4c-L08-prop-5.2 (A4 omits the continuity condition that plan D4 requires and that the Proposition 5.2(c) proof uses) and E4c-L09-res-1 (the Proof 1 identity is applied to trader 2's partition without saying so)."
)
ledger["registry_flags"] = prev.get("registry_flags", [])

out = ROOT + "/ledgers/E4/E4-c.json"
json.dump(ledger, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out, len(rows))
