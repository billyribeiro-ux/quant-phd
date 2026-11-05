"""Writes the round-11 E4 slice-b fragment to ledgers/E4/E4-b.json (checkout-relative paths)."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE11-E4-b")
OUT = "ledgers/E4/scripts/E4-b-r11/outputs/"
S = "ledgers/E4/scripts/E4-b-r11/"
rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- commands (all run this round at 11d7077) ----
row("E4b11-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit E4 (and --page L04, L05, L06; --all)", "PASS",
    f"{OUT}check_pages_E4.txt: 'check_pages E4: PASS'; check_pages_L04/L05/L06.txt: PASS per page; check_pages_all.txt exit 0 (see {S}run_commands_r11.sh, _exit_codes.txt).")
row("E4b11-cmd-check_dag", "2.9-dag", "tools/check_dag.py --unit E4 / --all", "PASS",
    f"{OUT}check_dag_E4.txt: 'check_dag E4: PASS'; check_dag_all.txt exit 0. Concept owners of every data-concept used on L04-L06 checked against curriculum.json concepts (module in closure E1,E2,E3,M1-M4,M7,P0.1,E4): all 23 page-concept pairs have owners in closure (dag_owner_check_r11.py).")
row("E4b11-cmd-check_projects", "2.6-projects (context)", "tools/check_projects.py --unit E4", "PASS",
    f"{OUT}check_projects_E4.txt: 'check_projects E4: PASS', exit 0.")
row("E4b11-cmd-run_labs", "2.5-labs", "tools/run_labs.py --unit E4", "PASS",
    f"{OUT}run_labs_E4.txt: 'run_labs E4: PASS (12/12)', exit 0.")
row("E4b11-cmd-twins-isolated", "2.5-labs", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", "PASS",
    f"{S}twin_page_check_r11.py (run with python -I): each twin run alone as `python -I -W error <copy>` from a scratch directory: exit 0, stderr 0 bytes; stdout 17, 26 and 19 lines (outputs/twin_L04_stdout.txt, twin_L05_stdout.txt, twin_L06_stdout.txt, twin_page_check_r11.txt).")
row("E4b11-cmd-page-code-equals-twin", "2.5-labs", "course/modules/E/E4/L04.html:125-246, L05.html:123-254, L06.html:241-460", "PASS",
    f"{S}twin_page_check_r11.py: data-run code equals its twin modulo the single trailing newline removed by embed_labs (code_equal_modulo_trailing_newline=True for L04, L05, L06; strict equality False only for that newline, twin_trailing_newline=True, page_code_trailing_newline=False).")
row("E4b11-cmd-expected-equals-output", "2.5-labs", "course/modules/E/E4/L04.html:247-263, L05.html:255-280, L06.html:461-479", "PASS",
    f"{S}twin_page_check_r11.py: each pre.expected equals the stdout of its twin run alone modulo the trailing newline (expected_equal_modulo_trailing_newline=True for all three).")
row("E4b11-cmd-ruff", "gates", "ruff check, ruff format --check: the three twins and the repository", "PASS",
    f"{OUT}ruff_twins.txt 'All checks passed!'; ruff_format_twins.txt '3 files already formatted'; ruff_repo.txt 'All checks passed!'; ruff_format_repo.txt exit 0.")
row("E4b11-cmd-mypy", "gates", "mypy --no-incremental (repository; twins alone)", "PASS",
    f"{OUT}mypy_full.txt 'Success: no issues found in 385 source files'; mypy_twins.txt 'Success: no issues found in 3 source files'.")
row("E4b11-cmd-pytest-labs", "gates", "pytest tests/test_labs.py tests/test_run_labs.py", "PASS",
    f"{OUT}pytest_labs.txt: 365 PASSED, 0 FAILED or ERROR, exit 0.")
row("E4b11-cmd-pytest-page", "gates", "pytest tests/test_page_checks.py tests/test_page_smoke.py", "PASS",
    f"{OUT}pytest_page.txt: 49 PASSED, 0 FAILED or ERROR, exit 0.")
row("E4b11-cmd-page_smoke", "2.9-page", "tools/page_smoke.py --unit E4 --pages L04 L05 L06", "PASS",
    f"{OUT}page_smoke_E4.txt: 'page_smoke modules/E/E4/L04.html: PASS', L05 PASS, L06 PASS, 'page_smoke E4: PASS'; lab timings 0.0 to 0.1 s after a 1.1 s runtime boot.")
row("E4b11-cmd-verify_refs-offline", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
    f"{OUT}verify_refs_offline.txt: 'offline integrity: 560 entries, 0 problems'.")
row("E4b11-cmd-verify_refs-live", "2.1-citations", "tools/verify_refs.py --unit E4 (live Crossref)", "PASS",
    f"{OUT}verify_refs_unit_E4_live.txt: 'live re-verification of E4: 3 of 560 entries, 0 problems'.")
row("E4b11-cmd-render-diff", "gates", "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json", "PASS",
    f"{OUT}render_curriculum.txt ('curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h'); render_diff.txt empty, exit 0 (tracked files unchanged). fetch_data_check.txt 'fetch_data: 3 datasets, 0 problems'; build_site_check.txt 'site data current: 6 outputs'.")
row("E4b11-muth-attribution", "2.1-citations", "course/modules/E/E4/L05.html:296 (data-cite muth1961rational, data-locator title); references/references.json key muth1961rational", "PASS",
    f"Claim: 'The phrase rational expectations appears in the title of Muth (1961).' Plain curl https://api.crossref.org/works/10.2307/1909635 returned HTTP 200 with title 'Rational Expectations and the Theory of Price Movements', container Econometrica, volume 29, issue 3, page 315, author Muth (outputs/crossref_muth_r11.json). The registry record of muth1961rational is unchanged since 00a84795 (references.json diff touches only BK4 and LX1 keys). Article body not read; the claim is title-only, as the page says.")
row("E4b11-no-B1-B3-attribution", "2.1-citations", "L04.html, L05.html, L06.html; cards.json (L04-L06 cards)", "PASS",
    "grep: no Grossman-Stiglitz, Mas-Colell, Milgrom or Whinston string in the three pages or the 100 slice cards; the only data-cite in the slice is muth1961rational.")

# ---- independent re-derivation and structure ----
row("E4b11-rederive-numbers", "2.2-numbers, 2.4-math", f"{S}rederive_r11.py", "PASS",
    f"Independent exact Fraction script: 85 of 85 checks OK ({OUT}rederive_r11.txt). Covers L04 ranks, augmented ranks, E2 family, R3 construction on a grid; L05 base/equal/large paths and ratios (-1/4, -1, -3/2), fixed points, E1 (1025/256 - 4 = 1/256), E3 errors, damped weight 4/5, Lemma 3.1 identity grid; L06 Example 6.9 (kappa 2, sig_eta^2 2, tau_eta 1/2, tau_bar 3/4, theta 3/7 and 6/7, Var(p) 27/49, Cov 3/7, slope 7/9, V_U 2/3, x_I 1/7, x_U -1/7), 16 grid residuals zero, Part D residual -9/85, M1 to M3, P2, P3, R1 identity at four lambdas, R2 monotonicity, E1 0.44, E2 -0.30 and -0.90, quiz tolerances, and a random-instance check of Prop 6.7 (60 instances x 16 points clear; perturbed theta_s leaves a residual).")
row("E4b11-L06-part-e-replica", "2.8-simulated labels / 2.5-labs", "course/modules/E/E4/L06.html:478-479; tests/labs/E4/lab-E4-L06-1.py part_e", "PASS",
    f"{S}rederive_r11.py replays random.Random(6) with the twin's draw order (v, eps, u) over 20000 draws: p_on_s slope 0.426617 tolerance 0.006497; v_on_p slope 0.761928 tolerance 0.023538. Matches the printed page block. Labelled SIMULATED on the page (L06.html:240, 255, 480).")
row("E4b11-structure-scan", "2.9 structure, 2.9 prose counts", f"{S}structure_scan_r11.py; L04.html:51, L05.html:51, L06.html:51", "PASS",
    f"why-it-matters words 96 (L04), 120 (L05, at the limit), 117 (L06); lessons data-hours=8 each; misconceptions 4, 3, 4; quiz items 8, 8, 12 (8-15); problem tiers Mechanics/Proof/Empirical/Research each 3 problems on all three pages; key-results rows 8, 7, 7; references present; latex macros used are registered (\\E, \\Var, \\Cov, \\Corr, \\R, \\Normal, \\indic) or standard. Banned-phrase scan: the only '...' hits are Python type hints inside lab code (L04 twin ... Row, L05 twin tuple[Fraction, ...]), outside prose.")
row("E4b11-solutions-length", "2.9 problem sets", f"{S}solutions_len_r11.py -> {OUT}solutions_len_r11.txt", "PASS",
    "Solutions per page 12; word counts (html.parser, tags stripped) min 36 (L04), 33 (L05), 50 (L06); every problem has a worked solution in details.solution.")
row("E4b11-dag-closure", "2.9 DAG", "concept links in L04, L05, L06 (data-concept attributes)", "PASS",
    "curriculum.json concepts: owner modules of every linked concept are in the E4 closure {E1,E2,E3,M1,M2,M3,M4,M7,P0.1,E4}: L04 arrow-debreu-security (E4 L01), linear-map (M3), vector-space (M3), market-completeness (E4); L05 conditional-expectation-elementary, expectation, normal-distribution, random-variable (M4), rational-expectations-equilibrium (E4); L06 competitive-equilibrium (E1), crra-utility and expected-utility (E3), independence, moment-generating-function, multivariate-normal, variance, normal-distribution, random-variable, expectation, conditional-expectation-elementary (M4), least-squares-projection (M3), noisy-rational-expectations-equilibrium (E4). Script ledgers/E4/scripts/E4-b-r11/dag_owner_check_r11.py, output outputs/dag_owner_check_r11.txt: 23 page-concept pairs, 0 out of closure.")
row("E4b11-notation", "2.4 / notation 13", "L04.html, L05.html, L06.html (all \\( \\) and \\[ \\] content)", "PASS",
    "notation/notation.json registered symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. grep: none of these appear in the three pages (zero hits for T as a symbol, \\Phi, \\gamma, R^\\ast, \\mathbb). Macros used: \\E, \\Var, \\Cov, \\Corr, \\R, \\Normal, \\indic (all registered). L06 Step 3 of Prop 6.7 uses a local Q (L06.html:196-202) which is a coefficient, not the registered measure \\mathbb{Q}; allowed by the plan's local-symbol list.")
row("E4b11-define-before-use", "2.9 / BUILDER 1.x define-before-use", "L04.html:51, 66, 77; L05.html:59, 73; L06.html:57, 67, 96, 169", "PASS",
    "L04 'payoff matrix', 'complete' are pointed forward at L04:51 ('Section 1 defines the terms ... Definitions 1.1 and 1.3') and first defined at :66 and :77. L05 'affine' and 'public signal' first appear in Assumption A2 where they are defined. L06 'noise trader', 'signal', 'informed fraction', 'precisions' (Def 6.1, :57), 'CARA' (Def 6.2, :67), 'posterior' (:96) are defined at first use. Forward references (Remark 6.5 in A4, Step 3 in A4) name the place explicitly.")
row("E4b11-scope-words", "2.4 / BUILDER 1.4 scope", "L04-L06 prose", "PASS",
    "Every scope word read in context: 'every start' (L05 why-it-matters) is Prop 3.2 both directions; 'no finite set ... completes' (L04:293) is Prop 4.1; 'for every pair' (L06 A4) is the clearing condition used in Prop 6.7; 'every graded result' (L06 references) is the table of §7 with proof or lab.")
row("E4b11-simulated-labels", "2.8 SIMULATED", "L06.html:240, 255, 480 (lab); L06.html:633-634 (key results); cards E4-c124, E4-c125", "PASS",
    "Part E of the L06 lab is labelled SIMULATED in the lab docstring, the hypothesis and the interpretation; the L06 key-results rows grade it C with the SIMULATED basis. Exact population parts are not labelled SIMULATED.")
row("E4b11-grades", "2.3 grades", "L04.html, L05.html, L06.html claim spans and key-results tables", "PASS",
    "Claim spans: L04 6 (T), L05 6 (T), L06 5 (T). Key-results: L04 all T (rows 1-8); L05 all T; L06 T for Lemma 6.3, Lemma 6.4, Prop 6.7, Cor 6.8 and base values; C for the 16-point finite check and the SIMULATED Part E. Re-graded against BLUEPRINT section 3 legend: each T carries a proof on the page; each C names its finite check or its seeded lab.")
row("E4b11-structure-order", "2.9 structure / BUILDER 4.2", "L04.html, L05.html, L06.html", "PASS",
    "Order: why it matters, numbered core sections, lab inline before 'Where the canon breaks', misconceptions, problem set (Mechanics, Proof, Empirical, Research), key results, quiz, references, complete button, lesson nav. Previous/next links L03-L04-L05-L06-L07 correct.")
row("E4b11-lab-twin-structure", "2.5 labs / BUILDER 6.1", "tests/labs/E4/lab-E4-L04-1.py, L05-1, L06-1; page section ids", "PASS",
    "Lab ids lab-E4-L04-1, lab-E4-L05-1, lab-E4-L06-1 match the page sections. Each twin calls main() at top level (L04 line 122, L05 line 132, L06 line 220) with no __name__ guard; twins unchanged since 00a84795 (git diff empty). Hypotheses state the printed results before the expected block (checked against outputs).")
row("E4b11-lab-l06-docstring", "2.5 lab statements vs code", "tests/labs/E4/lab-E4-L06-1.py (module docstring lines 1-23; part_d line 168; main line 211)", "PASS",
    "Twin module docstring (lines 1-23) says Part A uses theta_s and theta_u from closed_form(); closed_form() is at twin line 65 and returns them. Part C docstring: every residual zero (printed 'grid_points 16 zero_residuals 16 all_zero True'). Part D (twin line 168, part_d) evaluates only (1,0). Part E: SEED 6, N_DRAWS 20000 (module constants SEED at twin line 38 and N_DRAWS at line 39). Matches the round-10 defect fix at lines 8-9 of the docstring.")
row("E4b11-lab-l05-docstring", "2.5 lab statements vs code", "tests/labs/E4/lab-E4-L05-1.py module docstring; check_params line 40; show line 85; main line 132", "PASS",
    "Twin docstring: fixed point unique in the family, error recursion e_{k+1} = -(varsigma/beta) e_k, iteration-path rule. check_params (twin line 40) is called inside show() (twin line 85) before every iteration of Parts B-D. Parts A-F match the printed output. Interpretation (L05.html:281) says the lab does not simulate prices or check Corollary 2.3's variance; true of the code.")
row("E4b11-lab-l04-docstring", "2.5 lab statements vs code", "tests/labs/E4/lab-E4-L04-1.py module docstring (lines 1-22); rank() line 54; attainable() line 79; main() line 122; L04.html:119, 259", "PASS",
    "Docstring Parts A-E and the 'no random draws' sentence match main() (twin line 122). The rank() docstring (twin line 54: Gauss-Jordan elimination with exact Fractions, no tolerance) matches the code.")

# ---- lessons: content rows ----
row("E4b11-L04-lemma21-assumptions", "2.4 / Plan 2.1 item 6 (numbered Assumptions before Lemma statements)", "course/modules/E/E4/L04.html:100-108", "PASS",
    "Re-verified at 11d7077 (round-10 FAIL cleared). Assumption A0 (real entries) is listed at L04.html:100-103 before Lemma 2.1 (L04.html:105-108); the proof's first sentence cites it ('Under A0 every entry is real').")
row("E4b11-L04-lemma21-proof", "2.4 mathematics", "course/modules/E/E4/L04.html:108", "PASS",
    "Row operations preserve the row space (swap; add multiple with i != l, recovered by subtraction). Echelon reduction finite. Independence of nonzero rows by the smallest index i argument: column q_i entry equals c_i times the pivot of r_i, nonzero. Re-read line by line.")
row("E4b11-L04-sec1-statements", "2.4 mathematics", "course/modules/E/E4/L04.html:62-96", "PASS",
    "A1-A3 (:58-60); Def 1.1 (:66); Lemma 1.2 with proof (:70-72); Def 1.3 (:76-77); Thm 1.4 with proof (:81-83), full-dimension argument correct; Prop 1.5 proof (:89): row(A) contained in row([A;xi]) and equal dimensions; Cor 1.6 (:93-95). Each proof re-read.")
row("E4b11-L04-examples", "2.4 / 2.2 examples", "course/modules/E/E4/L04.html:111-115", "PASS",
    "Example 2.2 (rank 2, S=3, (1,2,3)=r1+r2 with zeta (1,1), (0,0,1) not attainable, augmented rank 3). Example 2.3 (rank 3, r4=(1,2,3)=e1+2e2+3e3). Re-derived in rederive_r11.py.")
row("E4b11-L04-lab-1", "2.5 labs", "course/modules/E/E4/L04.html:117-265", "PASS",
    "Hypothesis (:123-124) names rank 2 and 3, completeness False and True, (1,2,3) attainable, (0,0,1) and (5,0,0) not, redundant fourth row. Printed lines (:247-263) equal the run output. Interpretation (:264) names only the printed matrices.")
row("E4b11-L04-remarks", "2.4 remarks", "course/modules/E/E4/L04.html:269-277", "PASS",
    "Remark 3.1 (A = I_S; zeta = xi); Remark 3.2 (redundancy; (1,2,3,0) and (0,0,0,1); kernel dimension J - rank(A) by rank-nullity, nonzero when rank < J) all re-derived.")
row("E4b11-L04-canon-breaks", "2.4 / 2.2 scope", "course/modules/E/E4/L04.html:279-300", "PASS",
    "A4 (:283-284); Prop 4.1 (:288-290) with proof (J+1 independent indicators; dim M(A) <= J); Prop 4.2 (:296-298), cone not subspace, A = I_2 example re-derived. The statement 'no finite set of securities completes the market' is scoped to A4.")
row("E4b11-L04-misconceptions", "2.9 / 2.2", "course/modules/E/E4/L04.html:302-321", "PASS",
    "Four misconceptions, each with a re-derived example: (1,1,1),(1,1,1),(0,1,2) has rank 2 (:311); (1,2,3,0) and (0,0,0,1) (:315); completeness uses only A (:319).")
row("E4b11-L04-problems", "2.4 / 2.9 problem set", "course/modules/E/E4/L04.html:324-427", "PASS",
    "Three per tier, each with a worked solution. Re-derived: M1 rank 1; M2 (1,1,2) attainable with (1,1), (0,0,1) not; M3 rank 2 with r3=r1+r2, r4=2r1+r2; P1-P3; E1 equations give inconsistency 5-10 = -5; E2 family (1-t, 2-2t, 3-3t, t); E3 rank 2; R1 dimension argument; R2 I_S; R3 construction (zeta3=t, zeta1=xi1+t, zeta2=xi2+t) checked on a grid.")
row("E4b11-L04-key-results", "2.4 / 2.9 key-results table vs statement", "course/modules/E/E4/L04.html:440 (row 7); statement at L04.html:288-289", "FAIL",
    "Key-results row 7 reads 'Proposition 4.1, under A2 and A4' (L04.html:440). The statement of Proposition 4.1 reads 'Under A2 to A4' (L04.html:289). The proof uses A3 too: 'The set M(A) is spanned by the J rows of A' needs unrestricted holdings (A3, L04.html:60). So the table lists a smaller hypothesis set than the proposition states.",
    "Change L04.html:440 from 'Proposition 4.1, under A2 and A4' to 'Proposition 4.1, under A2 to A4'. No other change.")
row("E4b11-L04-quiz", "2.9 quiz", "course/modules/E/E4/L04.html:446-514", "PASS",
    "8 items, each with an explanation; mc items have one data-correct option; numeric answers 2 and 1 (tolerance 1e-6) re-derived; Q4 correct option is the family (1-t, 2-2t, 3-3t, t), re-derived; Q7 and Q8 explanations match Prop 4.1 and Prop 4.2.")
row("E4b11-L04-why-it-matters", "2.9 / BUILDER 4.2 (<=120 words)", "course/modules/E/E4/L04.html:51", "PASS",
    "96 words (structure_scan_r11.py). Claims match the lesson: rank test (Theorem 1.4) and the finite test not carrying to infinitely many states (Prop 4.1).")
row("E4b11-L04-references", "2.1 / 2.9", "course/modules/E/E4/L04.html:516-520", "PASS",
    "'This lesson cites no source.' and an empty data-references list; no data-cite on the page.")
row("E4b11-L05-why-it-matters", "2.9 / 2.2", "course/modules/E/E4/L05.html:51", "PASS",
    "120 words (at the limit). Claims: fixed point and the error-ratio lab; convergence from every start only when varsigma < beta matches Prop 3.2 (both directions). Definition 1.1 defines varsigma (supply response) and beta (demand slope in d(p) = alpha - beta p + u).")
row("E4b11-L05-model", "2.4 / 2.2", "course/modules/E/E4/L05.html:58-74", "PASS",
    "A1-A3 and Def 1.1: clearing price p_m = (alpha - varsigma m(z) - delta z + u - upsilon)/beta re-derived. Def 1.2 (:73): the conditional expectation is the function of z given by Lemma 2.1; it is stated without an explicit 'version' sentence (the round-11 edit). Non-blocking note: Lemma 2.1 supplies that explicit function, so the definition is read against it.")
row("E4b11-L05-lemma21-prop22-cor23", "2.4 mathematics", "course/modules/E/E4/L05.html:78-98", "PASS",
    "Lemma 2.1 formula and conditional law (variance (sigma_u^2 + sigma_upsilon^2)/beta^2) re-derived; proof uses independence of (u - upsilon)/beta from z (A3). Prop 2.2: fixed point c0* = alpha/(beta+varsigma), c1* = -delta/(beta+varsigma), uniqueness by beta+varsigma > 0 (A1). Cor 2.3 variances re-derived. Hypotheses listed (A1-A3).")
row("E4b11-L05-lemma31-proof", "2.4 mathematics", "course/modules/E/E4/L05.html:102-106", "PASS",
    "Lemma 3.1 (Under A1 so that beta > 0): e_{k+1} = -(varsigma/beta) e_k for both components re-derived. Proof lines 105 correct.")
row("E4b11-L05-lemma31-hypothesis", "2.4 / Plan 2.1 item 6", "course/modules/E/E4/L05.html:103-104", "PASS",
    "Round-10 FAIL cleared: the statement opens 'Under A1 (so that beta > 0)', and the division by beta is after that hypothesis.")
row("E4b11-L05-prop32-33", "2.4 mathematics", "course/modules/E/E4/L05.html:108-118", "PASS",
    "Prop 3.2: converges from every start when varsigma < beta; fails from some start when varsigma >= beta (equal: constant error; greater: growth); re-derived. Prop 3.3: damped step error factor 1 - nu(1 + varsigma/beta), zero at nu = beta/(beta+varsigma) (= 4/5 at the base); re-derived.")
row("E4b11-L05-psi0-notation", "2.9 / notation", "course/modules/E/E4/L05.html:402", "PASS",
    "Round-10 FAIL cleared: 'The first entry of Psi(0,0) is 10/2 = 5' (R1 solution). No Psi_0 remains in L05 (grep). Damped step gives 5/2 = c0* (re-derived).")
row("E4b11-L05-lab-1", "2.5 labs", "course/modules/E/E4/L05.html:120-282", "PASS",
    "Hypothesis (:122) states the fixed point (4, -3/10), zero residual, ratio -1/4 from (0,0), ratio -1 with the 0/5 alternation at varsigma = beta = 2, ratio -3/2 at varsigma = 3, damped weight 4/5 in one step, five-point identity. All printed lines (:255-280) equal the twin's output and match the re-derivation.")
row("E4b11-L05-remark-canon-muth", "2.1 / 2.2 attribution scope", "course/modules/E/E4/L05.html:292-296", "PASS",
    "Canon-break text (affine by construction; convergence; forecast correct by construction) is consistent with Prop 2.2, Prop 3.2, Prop 3.3 and Remark 4.1. Muth sentence limited to the title (Crossref row above). Non-blocking note: this title-only sentence carries data-cite but no class='claim' data-grade, so it is not graded; the plan says the title use is not a result.")
row("E4b11-L05-misconceptions", "2.9 / 2.2", "course/modules/E/E4/L05.html:299-315", "PASS",
    "Three misconceptions: Cor 2.3 variance zero only when both shocks are zero variance (A3 allows positive); Lab Part C at varsigma = beta has c0* = 5/2 with the 0/5 alternation (printed); unconditional mean c0* versus forecast c0* + c1* z with c1* = -3/10 printed.")
row("E4b11-L05-problems", "2.4 / 2.9 problem set", "course/modules/E/E4/L05.html:317-420", "PASS",
    "M1 (c* = (3,-1/2) at (12,3,1,2)); M2 (ratios -1/3 in both components, Psi(0,0) = (4,-2/3)); M3 (5/4); P1, P2, P3 proofs complete; E1 (|e_k| = 4/4^k, k = 5, 1025/256 - 4 = 1/256); E2 (ratio -1; 5/2 fixed); E3 (errors -2, 3, -9/2, 27/4; ratio -3/2; c0* = 2); R1 (nu = 1/2, 5/2); R2 (delta = 0 gives c1* = 0); R3 explanation consistent with Props 2.2 and 3.2. All re-derived in rederive_r11.py.")
row("E4b11-L05-key-results-quiz", "2.9 / 2.4 key results and quiz", "course/modules/E/E4/L05.html:422-502", "PASS",
    "Key results: 7 rows, all T with sources. Quiz: 8 items (mc 1, 3, 5, 6, 8 options with one correct; numeric 2, 4, 7 answers 4, -0.25, 1.25 with tolerance 1e-6 match). Explanations checked against the lesson and Lab 1 printed lines.")
row("E4b11-L05-references", "2.1 / 2.9", "course/modules/E/E4/L05.html:504-507", "PASS",
    "Empty data-references list (repository convention, the same empty list appears on E3 pages; check_pages requires only the element). Cited key muth1961rational is in the registry and was re-resolved live (verify_refs --unit E4).")
row("E4b11-L06-why-it-matters", "2.9 / BUILDER 4.2 (<=120 words)", "course/modules/E/E4/L06.html:51", "PASS",
    "117 words (structure_scan_r11.py). The changed sentence (round-11 edit) cites 'Definitions 6.1 and 6.2, Assumptions A1 to A4 and G'; each is on the page (Def 6.1 :56, Def 6.2 :66, A1 :61, A2 :71, A3 :76, A4 :81, G :90).")
row("E4b11-L06-model", "2.4 / notation 13", "course/modules/E/E4/L06.html:56-92", "PASS",
    "Def 6.1 (primitives; u > 0 means noise traders sell); A1 normal primitives with sigma_v^2, sigma_eps^2, sigma_u^2 > 0; Def 6.2 CARA with a > 0 and wealth w = w_0 + x(v - p); A2 (lambda in (0,1)); A3 (price taking, linear rule); A4 (clearing at every pair) with its residual argument (linear, no constant term, a line has probability zero, nondegenerate normal (s,u)) re-checked; G (i) and (ii) with the MGF note.")
row("E4b11-L06-lemma62-proof", "2.4 mathematics", "course/modules/E/E4/L06.html:99-125", "PASS",
    "MGF formula E e^{tZ} = e^{t mu + t^2 V/2} (completing the square re-checked); expected utility -e^{-a w0} e^{g(x)} with g(x) = -a x (m - p) + a^2 V x^2 / 2; maximizer x* = (m - p)/(aV) re-derived. Needs a != 0 for the quadratic; a > 0 is standing in Def 6.2.")
row("E4b11-L06-lemma62-hypotheses", "2.4 / Plan 2.1 item 6", "course/modules/E/E4/L06.html:98-104", "PASS",
    "Carried from round 10 (L06.html:98-104 byte-identical since 00a84795; Definition 6.2 at :66-68 byte-identical): the statement lists A3 and V > 0; the CARA utility with a > 0 is the object of Definition 6.2 and the block title 'CARA demand under normal beliefs'. Non-blocking note: the statement does not restate the utility or a > 0.")
row("E4b11-L06-lemma63-proof", "2.4 mathematics", "course/modules/E/E4/L06.html:129-144", "PASS",
    "Round-10 FAIL cleared (Cov(s,u)=0 and G applied to the triple). Re-derived: Cov(e,s) = 0 for e = v - omega s; Cov(e,u) = 0; (e,s,u) jointly normal (A1, G(i)); G(ii) gives e independent of (s,u), hence of (s,p); E[v|s,p] = omega s; Var(e) = sigma_v^2 (1 - omega) = V_I. Identities 1/V_I = tau_v + tau_eps and omega/V_I = tau_eps checked.")
row("E4b11-L06-lemma64", "2.4 mathematics", "course/modules/E/E4/L06.html:146-158", "PASS",
    "Assume A1 and G with (theta_s, theta_u) != 0 so Var(p) > 0; b = Cov/Var; Cov(v,p) = theta_s sigma_v^2 (Cov(v,u)=0); e = v - bp uncorrelated with p, independent by G; Var(v|p) = sigma_v^2 - b Cov(v,p). Re-derived.")
row("E4b11-L06-remark-65-610", "2.4 / 2.9", "course/modules/E/E4/L06.html:160-163; 233-236", "PASS",
    "Remark 6.5: x_U = (bp - p)/(aV_U), x_I = (omega s - p)/(aV_I), both linear in (s,p). Remark 6.10: Y = s - kappa u = v + eta with eta = eps - kappa u; sigma_eta^2 >= sigma_eps^2 > 0; larger sigma_u^2 raises sigma_eta^2 (kappa > 0 independent of sigma_u).")
row("E4b11-L06-prop67", "2.4 mathematics", "course/modules/E/E4/L06.html:172-209", "PASS",
    "Prop 6.7 (a) existence and (b) uniqueness re-derived. (b) Step 1 (theta_s != 0; uses lambda tau_eps / a != 0 at (s,0)); Step 2 (Y = p/theta_s = v + eta, E[v|p] = (tau_eta'/P_U')Y, V_U = 1/P_U'); Step 3 (A4 gives lambda tau_eps s - Q p = a u with Q as defined; evaluated at (1,0) and (0,1)); Step 4 (kappa' = kappa, tau' = tau_eta, tbar' = tbar, theta_s = tbar/(tau_v + tbar)). (a) existence: Q theta_s* = lambda tau_eps and Q theta_u* = a. Random check: 60 instances x 16 points clear exactly (rederive_r11.py). Assumption a > 0 comes from Def 6.2 (standing).")
row("E4b11-L06-cor68-slope-step", "2.4 mathematics", "course/modules/E/E4/L06.html:211-226", "PASS",
    "Round-10 FAIL cleared: the proof (L06.html:225) now states that Lemma 6.4 gives E[v|p] = bp, that Var(p) > 0 because theta_s* != 0, and compares the coefficient of p with the first formula to get b = tau_eta/(theta_s*(tau_v + tau_eta)). Checked: b = 7/9 at the base instance; formula holds on 40 random instances (rederive_r11.py).")
row("E4b11-L06-example69", "2.2 numbers", "course/modules/E/E4/L06.html:228-231", "PASS",
    "Every number: kappa 2, sigma_eta^2 2, tau_eta 1/2, tbar 3/4, theta_s 3/7, theta_u 6/7, b 7/9, V_U 2/3, x_I 1/7 at s=1, u=0, x_U -1/7, p 3/7, clearing 1/2 (1/7) + 1/2 (-1/7) = 0. Printed-versus-unprinted statement (lab prints kappa, sig_eta2, tau_eta, tbar, theta_s, theta_u, 7/9, 2/3, 1/7; does not print tau_v, 3/7, -1/7) checked against the printed lab output.")
row("E4b11-L06-lab-1", "2.5 labs", "course/modules/E/E4/L06.html:238-481", "PASS",
    "Hypothesis (:240) values (kappa 2, sigma_eta^2 2, tau_eta 1/2, tbar 3/4, theta 3/7, 6/7, slope 7/9, posterior 2/3, residual zero at 16 points, alternative theta_s = 1/2 nonzero residual, Part E SIMULATED seed 6, 20000 draws, 3 standard errors) matches the printed output (:461-479) and the interpretation (:480). Part D residual -9/85 re-derived.")
row("E4b11-L06-canon-breaks", "2.4 / 2.2 scope", "course/modules/E/E4/L06.html:483-493", "PASS",
    "Normality, utility, exogenous information, independent supply (Cov(v,p) = theta_s sigma_v^2 - theta_u Cov(v,u) re-derived), price taking, one period and one asset: each limit is consistent with the proofs.")
row("E4b11-L06-misconceptions", "2.9 / 2.2", "course/modules/E/E4/L06.html:495-515", "PASS",
    "Four misconceptions; each figure traced to Lab 1 printed lines or Remark 6.10 (sigma_eta^2 = 2, slope 3/7 versus 7/9, posterior variance 2/3 below prior 1).")
row("E4b11-L06-R1-corr-identity", "2.4 / 2.9 problem set (proof gap)", "course/modules/E/E4/L06.html:598-602 (R1)", "PASS",
    "Round-10 FAIL cleared: the solution now derives Var(p) = (theta_s*)^2 (sigma_v^2 + sigma_eta^2) and Cov(v,p) = theta_s* sigma_v^2 (using theta_u* = kappa theta_s*), hence Corr^2 = sigma_v^2/(sigma_v^2 + sigma_eta^2). Re-derived at four lambdas (rederive_r11.py). Limit steps (kappa to infinity, tau_eta to 0, theta_s* to 0) re-derived.")
row("E4b11-L06-problems", "2.4 / 2.9 problem set", "course/modules/E/E4/L06.html:521-594", "PASS",
    "M1 (kappa 4, sigma_eta^2 5, tau_eta 1/5, tbar 3/5, theta_s* 3/8, theta_u* 3/2); M2 (Var(p) 27/32, b 4/9, Var(v|p) 5/6, corr^2 1/6, cross-checked by 1/(tau_v+tau_eta) and sigma_v^2/(sigma_v^2+sigma_eta^2)); M3 (p = -3/4, x_I 7/4, x_U 1/4, clearing 1); P1 (lemma 6.3 with theta_s = 0 allowed); P2 (difference lambda tau_eps / a at (s,0) and (s+1,0) with the same supply u = 0); P3 (identity); E1 (0.80 - 7/9 over 0.05 = 0.44); E2 (-0.001954; -0.30 of tolerance; -0.90 SE); E3 interpretive; R2 (monotone, re-derived on a grid); R3 (four facts; G used in Lemmas 6.3 and 6.4).")
row("E4b11-L06-key-results-quiz", "2.9 / 2.4 key results and quiz", "course/modules/E/E4/L06.html:622-725", "PASS",
    "Key results: 7 rows (T rows: Lemma 6.3, Lemma 6.4, Prop 6.7, Cor 6.8, base values; C rows: 16-point check, Part E seeded). Quiz 12 items (8-15): numeric answers 0.4286, 4, 2, 0.5, 0.1429, 0.7778, 0.6667 with tolerances re-derived; mc correct options: L06q4 (v - omega s uncorrelated), q6 (rises), q8 (slope differs), q10 (exactly one), q11 (line has probability zero). Explanations checked.")
row("E4b11-L06-references", "2.1 / 2.9", "course/modules/E/E4/L06.html:727-731", "PASS",
    "'This lesson cites no source.' and an empty data-references list; the statement that G is used without proof matches Assumption G.")
row("E4b11-L06-part-d-alt", "2.5 labs / 2.4", "course/modules/E/E4/L06.html:474-475; tests/labs/E4/lab-E4-L06-1.py part_d", "PASS",
    "Part D residual -9/85 at (1,0) with theta_s = 1/2 re-derived by hand (slope 49/67, V_U 85/134, demand_unf -18/85) and by rederive_r11.py.")

# ---- cards ----
row("E4b11-cards-L04", "2.7 cards (all 33 L04 cards)", "course/modules/E/E4/cards.json: E4-c053-c073, c215, c217, c218, c226, c227, c228, c234-c236, c239, c240, c249", "PASS",
    "Every L04 card read in full (outputs/cards_L04_L06_r11.txt). Each front and back checked against L04 text and the lab output. Assumption and definition cards carry no grade (definitions); result cards carry T with a basis naming the lemma, proposition or lab part. Card E4-c249 (A0) matches the lesson's Assumption A0.")
row("E4b11-cards-L05", "2.7 cards (all 31 L05 cards)", "course/modules/E/E4/cards.json: E4-c074-c099, c219, c229, c241-c243", "PASS",
    "Every L05 card read (outputs/cards_L04_L06_r11.txt, from extract_slice_cards_r11.py). Cards match Lemma 2.1, Prop 2.2, Cor 2.3, Lemma 3.1, Prop 3.2, Prop 3.3, Remark 4.1, the three misconceptions, the Lab 1 printed ratios and paths (-1/4; 0,5,0,5; 0,5,-5/2,35/4; -3/2) and the Muth title-only card E4-c099 (cite key present).")
row("E4b11-cards-L06", "2.7 cards (all 36 L06 cards)", "course/modules/E/E4/cards.json: E4-c100-c129, c220, c230, c231, c244, c247, c250", "PASS",
    "Every L06 card read. Values 3/7, 6/7, 7/9, 2/3, 1/7, -1/7, 2, 16 grid points, -9/85, sample slopes 0.426617 and 0.761928 with tolerances all match Lab 1 printed lines. Basis strings name a lab part, a proposition step or a lemma. SIMULATED cards are grade C (E4-c124, c125).")
row("E4b11-cards-numbers-in-lesson", "2.7 cards vs lesson text", "cards E4-c092, c093, c094, c118, c122, c123, c124, c125, c243", "PASS",
    "Each numeric front or back appears in the corresponding lesson and lab output: c0 paths and ratios in the L05 lab Part B-D lines; 16 residuals and -9/85 in Part C-D; sample slopes and tolerances in Part E; base values in Part A-B.")
row("E4b11-cards-duplicate-scan", "2.7 duplicates", "cards.json: all 100 slice cards; ids unique across all 244 cards (outputs/cards_scan_r11.txt)", "PASS",
    "No duplicate ids. Near-duplicate scan (front Jaccard >= 0.6, or front >= 0.4 and back >= 0.6) gives 15 pairs; each pair asks a different question (c124/c125 two sample slopes; c116/c117 slope vs variance; c120/c220 x_I vs x_U; c084/c085 conditional vs unconditional variance; c077/c241 demand vs supply; c090/c219 two parameter sets; c092/c093 Part C vs Part D; c064/c217 complete vs redundant security; c062/c064 two examples; c066/c240 complete vs portfolio; c096/c098 two misconceptions; c111/c112 mean vs variance; c114/c115/c117 different results; c062/c063 rank vs attainability). The round-10 duplicate pairs are cleared: c248 (complete-or-incomplete) was removed; c055 now asks 'What is an attainable payoff' (definition), c059 asks the rank criterion.")
row("E4b11-cards-process-words", "2.9 no process words", "cards E4-c053..c250 (slice); lesson pages", "PASS",
    "grep for builder, verifier, round, REQUEST, planner, fixer in the slice pages and cards: no hits (the only 'round' hit is 'rounding' at L05.html:281).")
row("E4b11-cards-c120-basis", "2.7 basis", "cards.json E4-c120 and E4-c220", "PASS",
    "Round-10 cards-basis item re-verified: E4-c120 basis names Example 6.9, Lemma 6.2 and 6.3 formulas and Lab 1 Part C; x_I = (omega s - p)/(a V_I) uses Lemma 6.3 for omega and V_I and Lemma 6.2 for CARA demand; Lemma 6.4 is not used.")

# ---- notes ----
notes = [
    "Round-11 full verification of slice b (L04.html, L05.html, L06.html, the three lab twins, and the 100 L04-L06 cards in cards.json). Nothing carried from round 10: every row was re-run or re-read at 11d7077. The round-10 non-PASS rows (L04 Lemma 2.1 assumption, L06 Cor 6.8 slope step, L06 R1 correlation identity, cards c058/c248 and c055/c059) were re-verified and are now PASS. The round-9 items were also rechecked.",
    "Delta since the round-10 pin 00a84795 (git diff 00a84795 11d7077): L04.html 97-109 (Assumption A0 added, Lemma 2.1 proof edited); L05.html 73-74 (Def 1.2 wording); L06.html 51 (why-it-matters wording), 225 (Cor 6.8 proof), 599-602 (R1 solution); cards.json (about 66 changed lines, all 100 slice cards read in full); references.json (BK4, LX1 used_by and generated_at only; muth1961rational record unchanged); index.html (L06 added to the exact-labs sentence at lines 38 and 167, read; outside the slice). Twins lab-E4-L04-1, L05-1, L06-1: no change since 00a84795.",
    "Not a row but recorded: L06 Lemma 6.2 statement does not restate the CARA utility or a > 0; they come from Definition 6.2 and the block title. Proposition 6.7 likewise relies on a > 0 from Definition 6.2 (the division by a in Step 1). Both kept PASS as in round 10.",
    "Not a row but recorded: the Muth sentence (L05.html:296) carries data-cite but no class='claim' data-grade. It is a title-only reference (no result), so it is not graded. Non-blocking.",
    "Not a row but recorded: L05 Def 1.2 (L05.html:73) states m(z) = E[p_m | z] for every real z without the explicit 'version' sentence used in round 10. Lemma 2.1 supplies the explicit function, so the definition is read against it. Non-blocking, but the builder may restore the version sentence.",
    "Hub index.html (outside the slice) now lists L06 among the exact-Fraction labs (Parts A to D), matching L06.html:240. Round-10 note on this point is closed.",
    "Mutants: none. This slice is lab twins and lesson text, not a project grader; per the ruling, lab twins are demonstrations and mutation testing applies to project graders only. The structure of ledgers/E4/mutants is not touched by this slice.",
    "Not checked: the Muth (1961) article body (only the title and the Crossref metadata were read, as the page claims only the title); the Pyodide execution beyond what page_smoke reports (no browser run was done by hand); lessons L01-L03, L07-L09, the hub's other sentences, the project, the grader and the other slice's cards (only their id uniqueness was checked); the Muth citation's grade marking (see the note above). The MANIFEST and snapshot checks are outside the slice; fetch_data --check passed. No bot check, login or paywall was touched; the Crossref request carried no personal data.",
]

ledger = {
    "unit": "E4",
    "slice": "b",
    "round": 11,
    "verifier": "Haiku independent verifier, E4-b round 11 (did not build E4; no shared context with builders)",
    "pin": "11d7077a290f7960b183d3a5a6631af4773888f9 (detached; checkout /Users/billyribeiro/.fanout/wt/verifyE11-E4-b)",
    "base": "00a84795f276456fce19d4181373cc4efba11a36 (round-10 pin; round-10 fragment /Users/billyribeiro/.fanout/frags/E-E4-b.round10.json was context only, no PASS row carried)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE11-E4-b",
    "scratch": "ledgers/E4/scripts/E4-b-r11/ (run_commands_r11.sh, twin_page_check_r11.py, rederive_r11.py, structure_scan_r11.py, cards_scan_r11.py, write_fragment_r11.py; outputs/ holds every command output)",
    "verified_at": "2026-11-05T11:10:00Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
ledger["summary"] = f"FAIL E4-b round 11: rows={len(rows)} (pass={n_pass}, fail={n_fail}, unverifiable=0). Non-PASS: E4b11-L04-key-results (L04.html:440, hypothesis list 'A2 and A4' vs statement 'A2 to A4'). Every command gate passes at 11d7077. Round-10 non-PASS rows re-verified as PASS."
(ROOT / "ledgers/E4/E4-b.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", len(rows), "rows", n_pass, "pass", n_fail, "fail")
