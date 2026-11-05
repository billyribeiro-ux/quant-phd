"""Write the round-9 fragment ledgers/E4/E4-b.json for unit E4, slice b (L04 to L06 and their twins).

Every row cites a file and line, a command with its observed output file, or a script in this directory.
Run from the checkout root: python3 -I ledgers/E4/scripts/E4-b-r9/write_fragment.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/E4/scripts/E4-b-r9"
O = f"{S}/outputs"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---------------- gates (run by the verifier at the pin) ----------------
row("E4b9-cmd-check_pages", "tools/check_pages.py --unit E4 and --page L04, L05, L06", "tools/check_pages.py",
    "PASS", f"'check_pages E4: PASS' exit 0; per page 'check_pages E4 L04: PASS' (see {O}/check_pages_*.txt).")
row("E4b9-cmd-check_dag", "tools/check_dag.py --unit E4", "tools/check_dag.py", "PASS",
    f"'check_dag E4: PASS' exit 0 ({O}/check_dag_E4.txt).")
row("E4b9-cmd-check_projects", "tools/check_projects.py --unit E4 (outside slice, run for completeness)",
    "tools/check_projects.py", "PASS", f"'check_projects E4: PASS' exit 0 ({O}/check_projects_E4.txt).")
row("E4b9-cmd-run_labs", "tools/run_labs.py --unit E4 and --page L04, L05, L06", "tools/run_labs.py", "PASS",
    f"'run_labs E4: PASS (12/12)'; each page 'PASS (1/1)' (see {O}/run_labs_*.txt).")
row("E4b9-cmd-twins-isolated", "python -I -W error on each twin, run alone", "tests/labs/E4/lab-E4-L04-1.py, L05-1.py, L06-1.py",
    "PASS", f"exit 0 and zero bytes on stderr for all three ({O}/twin_L04.txt, twin_L05.txt, twin_L06.txt and *_stderr.txt).")
row("E4b9-cmd-page-code-equals-twin", "page data-run code equals twin", "L04.html, L05.html, L06.html lab blocks; "
    f"{S}/expected_vs_output.py", "PASS",
    "code_equals_twin=True for L04, L05, L06 after removing the one trailing newline that tools/embed_labs.py strips "
    "(embed_labs.py:117, rstrip) (" + O + "/expected_vs_output.txt).")
row("E4b9-cmd-expected-equals-output", "expected block equals the stdout of the twin run alone",
    "L04.html:242-258, L05.html:255-280, L06.html:460-478; " + f"{S}/expected_vs_output.py", "PASS",
    "Equal after the same trailing-newline convention (loose=True for all three; strict equality differs only by the final newline "
    "that embed_labs strips). L04, L05, L06 printed lines re-read against " + O + "/twin_*.txt.")
row("E4b9-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on the three twins",
    "tests/labs/E4/lab-E4-L04-1.py, L05-1.py, L06-1.py", "PASS",
    f"'All checks passed!', 'Success: no issues found in 3 source files' ({O}/ruff_check.txt, ruff_format.txt, mypy_twins.txt).")
row("E4b9-cmd-pytest", "pytest -k E4 tests/test_labs.py tests/test_run_labs.py", "tests/test_labs.py, tests/test_run_labs.py",
    "PASS", f"13 passed (dots, {O}/pytest_E4.txt; exit 0).")
row("E4b9-cmd-page_smoke", "tools/page_smoke.py --unit E4 --pages L04 L05 L06 (run alone)", "tools/page_smoke.py", "PASS",
    f"'page_smoke modules/E/E4/L04.html: PASS', L05 PASS, L06 PASS, 'page_smoke E4: PASS'; lab timings 0.0 to 0.1 s ({O}/page_smoke_E4.txt).")
row("E4b9-cmd-verify_refs-offline", "tools/verify_refs.py --offline", "tools/verify_refs.py", "PASS",
    f"'offline integrity: 560 entries, 0 problems' ({O}/verify_refs_offline.txt).")
row("E4b9-cmd-verify_refs-live", "tools/verify_refs.py --unit E4 (live Crossref)", "tools/verify_refs.py", "PASS",
    f"'live re-verification of E4: 3 of 560 entries, 0 problems', exit 0 ({O}/verify_refs_unit_E4_live.txt). "
    "Covers the muth1961rational title used at L05.html:296.")

# ---------------- independent re-derivation and structure scans ----------------
row("E4b9-indep-rederive", "Independent re-derivation of every printed and prose number (L04 minors, L05 closed forms and "
    "paths, L06 closed form, moments, clearing, Part D, M1 to M3, E1, E2)", f"{S}/indep_rederive.py",
    "PASS", f"84 checks OK, FAILURES: [] ({O}/indep_rederive.txt). Part E re-simulated with random.Random(6): "
    "p_on_s 0.426617 tol 0.006497, v_on_p 0.761928 tol 0.023538, identical to the printed lines.")
row("E4b9-structure-scan", "Word counts, minimums, banned strings, scope words, concept links",
    f"{S}/structure_scan.py; {S}/outputs/scope_words.txt", "PASS",
    "why_it_matters words 112 (L04), 117 (L05), 113 (L06), all <=120; quiz items 8, 8, 12; misconceptions 4, 3, 4; "
    "3 problems per tier; no banned string (the one 'round' hit is 'rounding', L05.html:281). Scope words: 136 contexts read.")
row("E4b9-delta-review", "Delta since round-8 pin 0dee921a for the slice files and the shared tooling",
    "git diff 0dee921a..HEAD -- course/modules/E/E4/{L04,L05,L06}.html cards.json tests/labs/E4 tools tests notation references plans",
    "PASS", "Slice hunks: L04.html why-it-matters (51), R1 solution (404), references (513); L05.html Muth sentence (296), "
    "six fieldset style attributes (443-477); L06.html why-it-matters (51), Assumption G link (91), references (728). "
    "cards.json: 144 changed lines. tools, tests, notation, references and plans: no change since 0dee921a (empty diff). "
    "Every changed hunk was read and re-verified in its row below.")
row("E4b9-prev-registry-fixed", "Round-8 FAIL rows: 'registry' in learner text (L04:513, L05:296, L06:728) and card E4-c099",
    "L04.html, L05.html, L06.html, cards.json:751", "PASS",
    "grep -niE 'registry|builder|verifier|round|fragment|ledger|twin|architect|plan|mutant|REQUEST|verif' on the three pages: "
    "the only hits are 'rounding' (L05.html:281) and 'Verify' (L05.html:389, an exercise verb); L04.html:513 now reads 'This lesson cites no source.'; "
    "E4-c099 front reads 'Which source does L05 cite, and for what purpose?'.")

# ---------------- L04 ----------------
row("E4b9-L04-why-it-matters", "Why it matters: <=120 words, claims match the lesson",
    "course/modules/E/E4/L04.html:51", "PASS",
    "112 words; 'exact test ... rank of the payoff matrix' (Thm 1.4); 'finite test does not carry over' (Prop 4.1).")
row("E4b9-L04-define-before-use", "Terms used before their dfn: attainable, portfolio, complete in Why it matters",
    "course/modules/E/E4/L04.html:51 vs dfn at :66 (payoff matrix, portfolio, attainable) and :77 (complete)", "FAIL",
    "Line 51 uses 'attainable', 'portfolio' and 'complete' in informal definitional sentences with no <dfn>; the first <dfn> "
    "for each is at L04.html:66 and :77 (the sentence at :51 already points to Definitions 1.1 and 1.3).",
    "Either remove the two definitional sentences from line 51 (keep the pointer 'Definitions 1.1 and 1.3 in Section 1 define the "
    "terms used here') or mark the first use with the <dfn> it will be defined by, so that the first appearance is the definition.")
row("E4b9-L04-sec1", "Assumptions A1 to A3, Def 1.1, Lemma 1.2, Def 1.3, Thm 1.4, Prop 1.5, Cor 1.6 (statements, proofs)",
    "course/modules/E/E4/L04.html:55-96", "PASS",
    "Each proof re-read; Thm 1.4 and Prop 1.5 are correct as stated (row-space and subspace dimension arguments). "
    "Hypotheses listed before each statement (A1 to A3).")
row("E4b9-L04-lemma21", "Lemma 2.1 (elimination counts the rank): statement, proof, hypothesis list",
    "course/modules/E/E4/L04.html:100-104", "PASS",
    "Proof checked line by line: the column-q_i argument gives independence; the count gives m = rank. The statement concerns "
    "any real matrix and cites no assumption; no assumption is needed beyond the matrix being real.")
row("E4b9-L04-examples", "Example 2.2 and Example 2.3 values and claims", "course/modules/E/E4/L04.html:107-115", "PASS",
    "Rank 2 with S=3, (1,2,3)=r1+r2, (0,0,1) not attainable; four rows of rank 3, r4=e1+2e2+3e3 (rank checked by "
    f"{S}/indep_rederive.py via minors).")
row("E4b9-L04-lab-1", "Lab 1: hypothesis, code, output, interpretation", "course/modules/E/E4/L04.html:117-260; "
    "tests/labs/E4/lab-E4-L04-1.py", "PASS",
    "Hypothesis (119) matches the printed Parts A to E (242-258): rank 2 and 3, complete False/True, (1,2,3) attainable, "
    "(0,0,1) and (5,0,0) not in the incomplete market, all attainable in the complete market, weighted sum equals the fourth "
    "row. Interpretation (259) names only the two matrices. Code/docstring checked (rank and attainable docstrings are accurate).")
row("E4b9-L04-remarks", "Remark 3.1 (identity), Remark 3.2 (redundancy, kernel)", "course/modules/E/E4/L04.html:264-271", "PASS",
    "zeta = xi attains xi for A = I_S; (1,2,3,0) and (0,0,0,1) both attain (1,2,3); kernel dimension J - rank(A) by rank-nullity.")
row("E4b9-L04-canon-breaks", "Where the canon breaks: Prop 4.1 (no finite complete market with infinitely many states), Prop 4.2 "
    "(cone)", "course/modules/E/E4/L04.html:274-295", "PASS",
    "Prop 4.1 proof: J+1 independent indicators vs dim <= J (checked). Prop 4.2 example (-1,0) not in the nonnegative quadrant "
    "and attainable under A3 (checked). The incomplete-market efficiency claim is absent (plan §12 Q18).")
row("E4b9-L04-prop41-hypotheses", "Prop 4.1 statement lists its hypotheses (A2 to A4) and the object M(A) it uses",
    "course/modules/E/E4/L04.html:283-285", "PASS",
    "M(A) is defined in Def 1.1 for every portfolio zeta in R^J, so the row-span argument does not need A3 separately. Statement consistent.")
row("E4b9-L04-misconceptions", "Misconceptions (4): wrong belief, reason, evidence", "course/modules/E/E4/L04.html:297-317", "PASS",
    "Each example checked: 4 securities in 3 states rank 3; rows (1,1,1),(1,1,1),(0,1,2) rank 2; two portfolios for (1,2,3); "
    "no price in the rank.")
row("E4b9-L04-problems", "Problem set: 3 per tier with solutions; every solution re-derived", "course/modules/E/E4/L04.html:319-421",
    "PASS", "M1-M3, P1-P3, E1-E3, R1-R3 re-derived (ranks 1, 2, 2; attainability by the two equations; R3 construction "
    "zeta=(xi1+t, xi2+t, t) with t=max(0,-xi1,-xi2) checked numerically). Tool word count >=15 for all 12.")
row("E4b9-L04-key-results-quiz", "Key-results table (8 rows, all T with sources) and quiz (8 items, answers, explanations)",
    "course/modules/E/E4/L04.html:424-508", "PASS",
    "Quiz answers checked: Thm 1.4 (rank), five-state minimum J=5, numeric rank 2, family (1-t,2-2t,3-3t,t), Prop 1.5, rank 1, "
    "infinite-state market incomplete, (-1,0) not attainable under ζ>=0. Explanations cite existing items.")
row("E4b9-L04-references-footer", "References sentence and footer", "course/modules/E/E4/L04.html:511-524", "PASS",
    "'This lesson cites no source.' with an empty <ol data-references>; the page has no data-cite; footer 524.")

# ---------------- L05 ----------------
row("E4b9-L05-why-it-matters", "Why it matters: <=120 words, claims match", "course/modules/E/E4/L05.html:51", "PASS",
    "117 words; 'converges for every start only when the supply response is smaller than the demand slope' matches Prop 3.2 "
    "(only-when is the correct direction).")
row("E4b9-L05-model", "Assumptions A1 to A3, Def 1.1 (clearing price), Def 1.2 (REE)", "course/modules/E/E4/L05.html:55-74", "PASS",
    "p_m = (alpha - varsigma m(z) - delta z + u - upsilon)/beta re-derived from d(p)=q; unique because beta>0.")
row("E4b9-L05-lemma21-prop22-cor23", "Lemma 2.1, Prop 2.2, Cor 2.3: formulas and proofs", "course/modules/E/E4/L05.html:78-98", "PASS",
    "E[p|z] formula, conditional variance (sigma_u^2+sigma_v^2)/beta^2, fixed point alpha/(beta+varsigma), -delta/(beta+varsigma), "
    "unconditional variance of p re-derived (indep_rederive.py L05/L06 sections).")
row("E4b9-L05-lemma31-hypothesis", "Lemma 3.1 states its hypotheses; its proof divides by beta",
    "course/modules/E/E4/L05.html:103-105", "FAIL",
    "The statement of Lemma 3.1 has no assumption list. Its proof divides by beta (the first and second component formulas "
    "-(varsigma/beta)(c-c*)), so it needs beta > 0 from A1; the statement only refers to 'the fixed point of Proposition 2.2'. "
    "Math itself verified (e_k = (-varsigma/beta)^k e_0).",
    "Start the statement with 'Under A1 (so that beta > 0),' and keep the reference to Proposition 2.2.")
row("E4b9-L05-prop32-33", "Prop 3.2 (convergence iff varsigma<beta, for some start) and Prop 3.3 (damped weight)",
    "course/modules/E/E4/L05.html:108-118", "PASS",
    "Error factor 1-nu(1+varsigma/beta) is zero at nu=beta/(beta+varsigma) (checked algebraically and at 4/5, base parameters).")
row("E4b9-L05-lab-1", "Lab 1: hypothesis, code, output, interpretation", "course/modules/E/E4/L05.html:120-281; "
    "tests/labs/E4/lab-E4-L05-1.py", "PASS",
    "Hypothesis (122): c0*=4, c1*=-3/10, ratio -1/4, ratio -1 with path 0,5, ratio -3/2, damped weight 4/5, identity at five z. "
    "All printed (255-280) reproduced by indep_rederive.py (paths and ratios for base, equal and large). Twin docstring lines "
    "136-137 agree with show() calling check_params before iterate.")
row("E4b9-L05-remark41-canon", "Remark 4.1 and 'Where the canon breaks' (three limits)", "course/modules/E/E4/L05.html:286-297",
    "PASS", "Three limits listed (293-295); Muth paragraph (296) is a fourth note, not a limit; 'exactly one' equilibrium in the family "
    "is Prop 2.2 (checked).")
row("E4b9-L05-muth-citation", "Muth (1961) attribution: title-only use, key and locator", "course/modules/E/E4/L05.html:296; "
    "references/references.json (key muth1961rational)", "PASS",
    "data-cite='muth1961rational' data-locator='title'; registry title 'Rational Expectations and the Theory of Price Movements', "
    "author Muth, 1961, Econometrica 29(3), verified by Crossref (verify_refs live, 0 problems). The sentence uses no result of the paper; "
    "the paper itself was not read (not fetched here), and the claim is limited to its title.")
row("E4b9-L05-misconceptions", "Misconceptions (3)", "course/modules/E/E4/L05.html:299-315", "PASS",
    "Forecast error variance zero only if both shocks have zero variance; Part C fixed point 5/2 with alternating path; mean "
    "of forecast c0* with E z = 0 (all checked).")
row("E4b9-L05-problems", "Problem set: 3 per tier; every solution re-derived", "course/modules/E/E4/L05.html:317-419", "PASS",
    "M1 c0*=3, c1*=-1/2; M2 ratio -1/3; M3 variance 5/4; P1-P3; E1 k>=5 with 1025/256 - 4 = 1/256; E2 fixed point 5/2 path stays; "
    "E3 e_3 = 27/4 and ratio -3/2; R1 nu=1/2 gives 5/2; R2 zero slope; R3 existence argument. Notation issue in R1 is a separate row.")
row("E4b9-L05-psi0-notation", "Subscript notation Psi_0 used without definition in R1 solution",
    "course/modules/E/E4/L05.html:402", "FAIL",
    "'The map sends 0 to Psi_0(0) = 10/2 = 5': Psi is defined (Prop 2.2, L05.html:89) as a pair-valued map, and Psi_0 is not defined anywhere. "
    "The number is right (first entry of Psi(0,0) = (5, -3/8)).",
    "Replace 'Psi_0(0) = 10/2 = 5' with 'the first entry of Psi(0,0) is 10/2 = 5'.")
row("E4b9-L05-key-results-quiz", "Key-results table (7 rows, T, sources) and quiz (8 items)", "course/modules/E/E4/L05.html:422-502",
    "PASS", "Quiz answers checked: c0* = alpha/(beta+varsigma) (base 4), ratio -1/4, conditional variance 1.25, delta=0 gives a constant forecast; correct options q1, q3, q5, q6, q8 as marked; explanations cite existing results.")
row("E4b9-L05-references-footer", "References and footer", "course/modules/E/E4/L05.html:504-516", "PASS",
    "Empty data-references list; the single data-cite is resolved; footer 516.")

# ---------------- L06 ----------------
row("E4b9-L06-why-it-matters", "Why it matters: <=120 words, claims match", "course/modules/E/E4/L06.html:51", "PASS",
    "113 words; 'some investors who observe more than the price' is consistent with A2 (line 72); 'Definition 6.1, Assumptions A2 and A3' "
    "cross-reference exists.")
row("E4b9-L06-model", "Def 6.1, Def 6.2, A1 to A4, G (primitives, CARA, information, price rule, clearing, normal facts)",
    "course/modules/E/E4/L06.html:55-92", "PASS",
    "A4 justification re-derived: residual linear without constant term, zero on a line has probability zero under the nondegenerate "
    "normal law of (s,u) (line 86). G: both facts are standard and are labelled as assumed without proof.")
row("E4b9-L06-lemma62", "Lemma 6.2 (CARA demand) and its proof", "course/modules/E/E4/L06.html:98-126", "PASS",
    "E e^{tZ} = exp(t mu + t^2 V/2) and g(x) = -a x (m-p) + a^2 V x^2/2 re-derived; x* = (m-p)/(aV).")
row("E4b9-L06-lemma63-proof", "Lemma 6.3 (informed beliefs): proof needs Cov(s,u)=0 before applying G to (e,s,u)",
    "course/modules/E/E4/L06.html:141-143", "FAIL",
    "The proof checks Cov(e,s)=0 and Cov(e,u)=0 and then says 'By G, e is independent of (s, u)'. G(ii) applies to the whole vector "
    "(e,s,u) only if every pair is uncorrelated, and Cov(s,u)=0 is never stated. It follows from A1 (v, eps, u mutually independent, "
    "so s=v+eps is independent of u), but the proof does not cite it. Formulas for omega, V_I, 1/V_I = tau_v + tau_eps verified.",
    "In L06.html:143 insert 'and Cov(s, u) = 0 because s = v + eps is independent of u by A1' before 'By G, e is independent of (s, u)'.")
row("E4b9-L06-lemma64", "Lemma 6.4 (uninformed beliefs are a linear projection) and its proof", "course/modules/E/E4/L06.html:146-158",
    "PASS", "Cov(e,p)=0, joint normality of (e,p), G for one pair, Var(v|p)=sigma_v^2 - b Cov(v,p) (checked).")
row("E4b9-L06-remark65-610", "Remarks 6.5 and 6.10 (demands; price as noisy signal, sigma_eta^2 monotone in sigma_u^2)",
    "course/modules/E/E4/L06.html:161-163, 233-236", "PASS",
    "x_I=(omega s-p)/(aV_I) by Lemmas 6.2 and 6.3; x_U by Lemmas 6.2 and 6.4 (checked). sigma_eta^2 = sigma_eps^2 + kappa^2 sigma_u^2 with "
    "kappa independent of sigma_u (so the monotone claim holds).")
row("E4b9-L06-prop67", "Prop 6.7 (existence and uniqueness, Steps 1 to 4) and Cor 6.8", "course/modules/E/E4/L06.html:172-226",
    "PASS", "Step 1 (theta_s != 0), Step 2 (Y = s - kappa' u, eta independent of v), Step 3 (Q and the identity lambda tau_eps s - Q p = a u), "
    "Step 4 (kappa'=kappa, theta_s = tau_bar/(tau_v+tau_bar)); existence (a); Cor 6.8 slope and posterior variance re-derived.")
row("E4b9-L06-example69", "Example 6.9 base instance (all values and the clearing check)", "course/modules/E/E4/L06.html:228-231",
    "PASS", "kappa=2, sigma_eta^2=2, tau_eta=1/2, tau_bar=3/4, theta_s=3/7, theta_u=6/7, slope 7/9, V_U=2/3, x_I=1/7, x_U=-1/7 "
    "(indep_rederive.py). Lab output lists exactly the items that the sentence says it prints.")
row("E4b9-L06-lab-1", "Lab 1: hypothesis, code, output, interpretation (Parts A to E)", "course/modules/E/E4/L06.html:238-480; "
    "tests/labs/E4/lab-E4-L06-1.py", "PASS",
    "Hypothesis (240): kappa, sigma_eta^2, tau_eta, tau_bar, theta_s, theta_u, slope 7/9, posterior 2/3, 16 grid points, "
    "theta_s=1/2 residual nonzero at (1,0): all reproduced (indep_rederive.py; Part D residual -9/85 recomputed). Part E is labelled "
    "SIMULATED in the output (475) and the interpretation (479), and re-simulated to the same digits.")
row("E4b9-L06-lab-docstring-names", "Twin docstring agrees with the code (names and units)",
    "tests/labs/E4/lab-E4-L06-1.py:8 (page copy at course/modules/E/E4/L06.html:248)", "FAIL",
    "Docstring line 8 says 'the closed-form coefficients of the linear price p = THETA_S * s - THETA_U * u'. No THETA_S or THETA_U "
    "exists in the twin; the price is computed from theta_s and theta_u returned by closed_form(). The sentence is about the code, "
    "and its names do not match it.",
    "In tests/labs/E4/lab-E4-L06-1.py line 8 change 'p = THETA_S * s - THETA_U * u' to 'p = theta_s * s - theta_u * u, with theta_s and theta_u "
    "from closed_form()', then re-embed with tools/embed_labs.py course/modules/E/E4/L06.html --refresh lab-E4-L06-1.")
row("E4b9-L06-canon-breaks", "Where the canon breaks: normality, utility, exogenous lambda, supply correlation, price taking, one period",
    "course/modules/E/E4/L06.html:482-492", "PASS",
    "Cov(v,p) = theta_s sigma_v^2 - theta_u Cov(v,u) (line 488) re-derived; 'need not' hedges used for other utilities.")
row("E4b9-L06-misconceptions", "Misconceptions (4)", "course/modules/E/E4/L06.html:494-514", "PASS",
    "sigma_eta^2=2 at base (Part A); b=7/9 and theta_s=3/7; posterior 2/3 below prior 1 (Corollary 6.8, Part B).")
row("E4b9-L06-problems", "Problem set: 3 per tier; every solution re-derived", "course/modules/E/E4/L06.html:516-619", "PASS",
    "M1 kappa=4, sigma_eta^2=5, theta_s*=3/8, theta_u*=3/2; M2 Var(p)=27/32, b=4/9, Var(v|p)=5/6, rho^2=1/6; M3 (2,1): p=-3/4, "
    "x_I=7/4, x_U=1/4, clears; P1 to P3; E1 0.44 SE; E2 -0.30 of tolerance and -0.90 SE (both recomputed); E3; R1 limit; R2 monotone; R3.")
row("E4b9-L06-key-results-quiz", "Key-results table (7 rows) and quiz (12 items)", "course/modules/E/E4/L06.html:621-724", "PASS",
    "Numeric answers and tolerances checked: 3/7 vs 0.4286 (tol 0.0005), kappa 4, sigma_eta^2 2, V_I 0.5, x_I 0.1429, b 0.7778, "
    "Var(v|p) 0.6667. Option items L06q4, q6, q8, q10, q11 are correct as marked and their explanations match the lesson.")
row("E4b9-L06-references-footer", "References and footer", "course/modules/E/E4/L06.html:726-739", "PASS",
    "'This lesson cites no source.' and an empty data-references; footer 739.")

# ---------------- cards ----------------
row("E4b9-cards-L04", "Retrieval cards for L04 (32 cards read in full)", "course/modules/E/E4/cards.json", "PASS",
    "Each card checked against its lesson text; grades and basis fields match Theorem and Lemma titles; numbers appear in the lesson.")
row("E4b9-cards-L05", "Retrieval cards for L05 (31 cards read in full)", "course/modules/E/E4/cards.json", "PASS",
    "Each card checked: Lemma 3.1, Props 2.2, 3.2, 3.3, base, equal and large lab values (c091 to c093, c219, c243) reproduced by "
    "indep_rederive.py; E4-c099 cites muth1961rational only.")
row("E4b9-cards-L06", "Retrieval cards for L06 (35 cards read in full, except as noted)", "course/modules/E/E4/cards.json", "PASS",
    "Each card checked, including SIMULATED cards c124 and c125 (grade C, one seed) and finite-check cards c122 and c123 (grade C).")
row("E4b9-cards-c120-basis", "Card E4-c120 basis attributes x_I to Lemma 6.4", "course/modules/E/E4/cards.json:902-906", "FAIL",
    "basis 'Example 6.9 (Lemma 6.2 and Lemma 6.4 formulas); Lab 1, Part C'. The informed demand x_I = (omega s - p)/(a V_I) uses Lemma 6.2 "
    "(CARA demand) and Lemma 6.3 (E[v|s,p]=omega s, V_I). Lemma 6.4 is the uninformed belief; Remark 6.5 (L06.html:162) says so.",
    "In cards.json for E4-c120 set basis to 'Example 6.9 (Lemma 6.2 and Lemma 6.3 with Remark 6.5); Lab 1, Part C'.")
row("E4b9-cards-duplicate-scan", "Full duplicate scan of the L04 to L06 cards", "course/modules/E/E4/cards.json:443 (E4-c059), :1648 (E4-c226)",
    "FAIL",
    "E4-c059 'When is a payoff xi attainable (Proposition 1.5)? If and only if rank([A; xi]) = rank(A)' and E4-c226 'what is the augmented "
    "rank of a payoff xi (Proposition 1.5)? ... attainable exactly when this equals rank(A)' test the same criterion with the same answer. "
    "No other pair of L04 to L06 cards repeats a fact (checked by reading all 98).",
    "Delete E4-c226, or reword it to test only the definition of [A; xi] (for example 'what matrix has its rank taken, and how many rows does it have?').")
row("E4b9-cards-numbers-in-lesson", "Every number on a card appears in its lesson (text, output or key-results)",
    "cards.json (L04 to L06)", "PASS", "Spot check of all 98: e.g. 1/7, -1/7, 65/16, -9/85, 16 grid points, 27/4, 5/2 and -3/16 all appear in the printed lab output or the prose.")
row("E4b9-cards-grades", "Card grades agree with lesson grades (T for theorems, C for finite and SIMULATED results)", "cards.json (L04 to L06)",
    "PASS", "E4-c122, c123, c124, c125 are C, matching key-results rows L06.html:632-633; theorem-derived cards are T.")
row("E4b9-cards-process-words", "No process words or planning references in cards or pages", "cards.json; L04 to L06 pages", "PASS",
    "Scan of the 98 slice cards for builder, verifier, round, fragment, ledger, twin, architect, plan, mutant, REQUEST and registry: "
    "no learner-visible hit.")

# ---------------- notation, DAG, prose ----------------
row("E4b9-notation-macros", "Every macro used in the three pages is a registered macro or a KaTeX builtin, with no reuse of "
    "registered symbols", "L04.html, L05.html, L06.html; notation/notation.json", "PASS",
    "Macros used include \\E, \\Var, \\Cov, \\Corr, \\R, \\Normal (registered); no \\mathbb{E} (0 hits); no T, \\Phi, \\gamma_3, R^\\ast, "
    "R^{e\\ast}, R_f, \\mathbb{Q} (0 hits). The indicator is the only deviation (next row).")
row("E4b9-L04-indicator", "Indicator of a state written with the registered macro \\indic (plan §2.3)",
    "course/modules/E/E4/L04.html:285", "FAIL",
    "Prop 4.1 proof writes \\mathbf{1}_{\\omega} (raw KaTeX). Plan §2.3 and notation.json:33-36 register \\indic for 'indicators of states' "
    "(meaning identical, but the binding plan rule is missed).",
    "Replace '\\mathbf{1}_{\\omega}' in L04.html:285 with '\\indic\\{\\omega\\}' (both occurrences in that sentence) and re-run check_pages.")
row("E4b9-dag-closure", "Concepts linked from L04 to L06 are owned inside the prerequisite closure or by E4 itself",
    "L04.html:37; L05.html:37; L06.html:37, 91, 486", "PASS",
    "curriculum.json owners: moment-generating-function M4, independence M4, multivariate-normal M4, least-squares-projection M3, "
    "orthogonal-projection M3, crra-utility E3, expected-utility E3, competitive-equilibrium E1, vector-space M3, linear-map M3, all others M4 or E4; check_dag PASS.")
row("E4b9-dag-plan-terms", "Out-of-closure terms (plan §4 D1 to D10) absent from the slice", "L04.html, L05.html, L06.html", "PASS",
    "Counts 0 for Bayes, state price, stochastic discount, law of one price, martingale, Banach, intermediate value, common knowledge, "
    "Walras, two-fund, diagnostic, determinacy, Lagrange, Bellman, Kyle, Grossman, Stiglitz, Milgrom, Pareto (the 'efficient' hits are inside 'coefficient').")
row("E4b9-define-before-use-rest", "Other terms defined at first use: affine, public signal, row space, pivot, convex cone, posterior, CARA, precisions, "
    "informed fraction, noise trader, rational-expectations equilibrium",
    "L04.html:58-102, 292; L05.html:55-73; L06.html:57-96", "PASS",
    "First body uses of these terms are their <dfn> sites (line numbers above). 'rational-expectations equilibrium' at L05.html:51 "
    "points to Definition 1.2 explicitly.")
row("E4b9-banned-strings", "Banned strings (BUILDER_RULES §1.3-1.4, check_pages BANNED) absent from prose",
    "L04.html, L05.html, L06.html", "PASS", "check_pages PASS and structure_scan.py: no TODO, TBD, lorem, 'for brevity', "
    "'it is important to note', 'clearly', 'obviously', 'studies show', 'experts agree', 'it is well known'. The only substring hits are 'rounding' (L05.html:281) and 'Verify' (L05.html:389, an exercise verb).")
row("E4b9-scope-words", "Scope words (every, all, only, same, exactly, any, never) backed by a computation or hypothesis",
    f"{O}/scope_words.txt (136 contexts)", "PASS",
    "Each non-math context read. Examples: 'converges for every start only when' (Prop 3.2, direction checked); 'the price reveals the payoff "
    "only with noise' (sigma_eta^2 >= sigma_eps^2 > 0); 'every real z' (identity over z, proved); 'Each graded result carries a proof or a lab result' (footer).")
row("E4b9-process-words-prose", "No process words in learner prose (round, builder, verifier, REQUEST, unit report)",
    "L04.html, L05.html, L06.html", "PASS", "grep for these terms: no learner-visible hit.")
row("E4b9-grades-claims", "Theorem and key-result grades re-graded independently against BLUEPRINT §3 (no over-grading)",
    "L04.html:81-101, 429-436; L05.html:79-118, 427-433; L06.html:99-212, 627-633", "PASS",
    "Each derived result is T under its stated assumptions; the finite rank test (C where it is a single finite check) and the "
    "seeded check (C, SIMULATED) are graded C; no under-grading of a theorem found.")
row("E4b9-simulated-labels", "SIMULATED label present wherever data are generated", "L06.html:240, 475-479, 633; cards c124, c125",
    "PASS", "The only random draw is L06 Part E; every mention carries SIMULATED. L04 and L05 labs have no random draws (twins).")
row("E4b9-hours", "Lesson hours and hub split", "L04.html:34, L05.html:34, L06.html:34; index.html:29",
    "PASS", "data-hours=8 on each lesson (6 to 12 range); hub data-hours-lessons=72 = 9 x 8 (9 lessons), data-hours-project=28; 72+28=100 (curriculum figure).")
row("E4b9-quiz-and-problem-counts", "Quiz 8 to 15 items; problems 3 per tier; misconceptions at least 3",
    "L04.html:441-508; L05.html:438-500; L06.html:639-724", "PASS",
    "Quiz items 8, 8, 12; problems 3 per tier in each lesson; misconceptions 4, 3, 4; every problem has a details.solution (tool word count >=15; "
    "L06 M1 has 11 prose words once the math tokens are removed, but check_pages counts them and passes).")
row("E4b9-structure-order", "Lesson section order of BUILDER_RULES §4.2", "L04.html, L05.html, L06.html", "PASS",
    "Why it matters, numbered core sections, inline lab, where the canon breaks, misconceptions, problem set, key-results, quiz, "
    "references (no debate block: E4 has no debate key).")
row("E4b9-plan-conformance", "Plan §3 and §7 conformance: no B1/B3 attribution, paper-level Muth only, no figures or data files",
    "plans/E4-build-plan.md §3, §6, §7; L04 to L06 pages", "PASS",
    "No Grossman-Stiglitz, Mas-Colell or Milgrom citation in the three pages; Muth cited at paper level (title); no data-files, "
    "data-chart, <img> or <svg>; L04 has no incomplete-market efficiency claim (§12 Q18); Lab twins ids match §1 table.")

# ---------------- write ----------------
fragment = {
    "unit": "E4",
    "slice": "b",
    "round": 9,
    "verifier": "Haiku independent verifier, E4-b round 9 (did not build E4)",
    "pin": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (detached; checkout /Users/billyribeiro/.fanout/wt/verifyE9-E4-b)",
    "base": "0dee921a (round-8 pin); round-8 fragment /Users/billyribeiro/.fanout/frags/E-E4-b.round8.json, context only, its PASS rows were not carried",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE9-E4-b",
    "scratch": f"{S}/ (expected_vs_output.py, structure_scan.py, indep_rederive.py, write_fragment.py, outputs/)",
    "verified_at": "2026-11-04",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b is L04 to L06 and their three lab twins, plus the L04 to L06 cards in cards.json. It is not a project slice: no grader mutants or "
        "alternatives are written here. Lab twins are demonstrations (ruling), so no mutation rows.",
        "Every row was re-verified this round from the current bytes at c93dd52. No PASS row was carried from round 8.",
        "Round-8 FAIL rows on 'registry' wording (L04.html:513, L05.html:296, L06.html:728, card E4-c099) are resolved at this pin.",
        "Not checked: the Muth (1961) article itself (the paper was not fetched; the title is confirmed by live Crossref through verify_refs "
        "and the claim is limited to the title). Mas-Colell and Grossman-Stiglitz are not cited in this slice, so B1 and B3 do not apply.",
        "Hub index.html and cards outside L04 to L06 are outside slice b; only the hub hours split was read, for arithmetic.",
        "The page-to-twin comparison ignores the single trailing newline that tools/embed_labs.py strips (embed_labs.py:117), by design of the tool.",
        "Plan-conformance note (not a row): plan §2.1 item 6 asks every Lemma to list its assumptions; L04 Lemma 2.1 states none and needs none beyond a real matrix, so no row fails on it.",
    ],
    "summary": ("FAIL E4-b round 9: rows=%d (pass=%d, fail=%d, unverifiable=0). Gates re-run at c93dd52 all PASS (check_pages, check_dag, "
                "check_projects, run_labs 12/12, twins under python -I -W error, ruff, mypy, pytest 13, page_smoke L04-L06, verify_refs offline and live). "
                "Eight FAIL rows, all minor: L04 why-it-matters defines before <dfn> (L04.html:51); raw \\mathbf in place of \\indic (L04.html:285); "
                "Lemma 3.1 hypothesis (L05.html:103-105); Psi_0 undefined (L05.html:402); Lemma 6.3 proof omits Cov(s,u)=0 (L06.html:143); "
                "twin docstring names THETA_S/THETA_U that do not exist (tests/labs/E4/lab-E4-L06-1.py:8); card E4-c120 basis cites Lemma 6.4 for x_I; "
                "card E4-c226 duplicates E4-c059.") % (
        len(rows), sum(1 for r in rows if r["status"] == "PASS"), sum(1 for r in rows if r["status"] == "FAIL")),
}

out = ROOT / "ledgers/E4/E4-b.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "fail", sum(1 for r in rows if r["status"] == "FAIL"))
