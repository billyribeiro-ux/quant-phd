"""Writes the round-10 E4-b fragment (ledgers/E4/E4-b.json). Every row's evidence cites a file, line or output kept in this checkout."""

import json
from pathlib import Path

OUT = "ledgers/E4/scripts/E4-b-r10/outputs"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---- gates (run by the verifier; outputs under ledgers/E4/scripts/E4-b-r10/outputs/)
row("E4b10-cmd-check_pages", "2.9-structure", "tools/check_pages.py", "PASS",
    f"`tools/check_pages.py --unit E4` and `--unit E4 --page L04|L05|L06`: 'check_pages E4: PASS' and per-page PASS, exit 0 ({OUT}/check_pages_*.txt).")
row("E4b10-cmd-check_dag", "2.9-dag", "tools/check_dag.py", "PASS",
    f"`check_dag.py --unit E4`: 'check_dag E4: PASS'; `check_dag.py --all` exit 0 ({OUT}/check_dag_E4.txt, check_dag_all.txt).")
row("E4b10-cmd-check_projects", "2.6-projects", "tools/check_projects.py", "PASS",
    f"`check_projects.py --unit E4`: 'check_projects E4: PASS', exit 0 (outside the L04-L06 slice, run for completeness; {OUT}/check_projects_E4.txt).")
row("E4b10-cmd-run_labs", "2.5-labs", "tools/run_labs.py", "PASS",
    f"`run_labs.py --unit E4`: 'run_labs E4: PASS (12/12)', exit 0 ({OUT}/run_labs_E4.txt). run_labs.py has no --page option (it requires --unit or --all); the per-lab results are the 12 lab results of the unit.")
row("E4b10-cmd-twins-isolated", "2.5-labs", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", "PASS",
    f"Each twin run alone as `python -I -W error <twin>` from its own directory: exit 0 and 0 bytes of stderr for L04, L05 and L06 ({OUT}/twin_L04.txt, twin_L05.txt, twin_L06.txt and *_stderr.txt). stdout is 17 lines for L04, 26 for L05 and 19 for L06.")
row("E4b10-cmd-page-code-equals-twin", "2.5-labs", "course/modules/E/E4/L04.html:120-240, L05.html:123-253, L06.html:241-459", "PASS",
    f"`ledgers/E4/scripts/E4-b-r10/page_twin_check.py` (output {OUT}/page_twin_check.txt): the data-run code of each lab equals its twin source, byte for byte after removing the one trailing newline that tools/embed_labs.py strips (embed_labs.py:117). Strict equality differs only by that newline.")
row("E4b10-cmd-expected-equals-output", "2.5-labs", "course/modules/E/E4/L04.html:242-258, L05.html:255-280, L06.html:461-479", "PASS",
    f"page_twin_check.py: each `pre.expected` block equals the stdout of its twin run alone, modulo the trailing newline (stdout 17, 26 and 19 lines; the page block has one fewer trailing newline; {OUT}/page_twin_check.txt).")
row("E4b10-cmd-ruff", "gates", "tests/labs/E4 twins; whole repository", "PASS",
    f"`ruff check` on the three twins and `ruff check .` (repository): 'All checks passed!'. `ruff format --check` on the three twins: '3 files already formatted' ({OUT}/ruff_check.txt, ruff_format.txt, ruff_repo.txt).")
row("E4b10-cmd-mypy", "gates", "whole repository; tests/labs/E4 twins", "PASS",
    f"`mypy --no-incremental` over the repository: 'Success: no issues found in 385 source files'. Twins alone: 'Success: no issues found in 3 source files' ({OUT}/mypy_full.txt, mypy_twins.txt).")
row("E4b10-cmd-pytest-labs", "gates", "tests/test_labs.py, tests/test_run_labs.py", "PASS",
    f"`pytest tests/test_labs.py tests/test_run_labs.py -rA`: 365 PASSED, 0 FAILED or ERROR, exit 0 ({OUT}/pytest_labs_full.txt).")
row("E4b10-cmd-pytest-page", "gates", "tests/test_page_checks.py, tests/test_page_smoke.py", "PASS",
    f"`pytest tests/test_page_checks.py tests/test_page_smoke.py -rA`: 49 PASSED, 0 FAILED or ERROR, exit 0 ({OUT}/pytest_page_checks.txt).")
row("E4b10-cmd-page_smoke", "2.9-page", "tools/page_smoke.py --unit E4 --pages L04 L05 L06", "PASS",
    f"'page_smoke modules/E/E4/L04.html: PASS', L05 PASS, L06 PASS, 'page_smoke E4: PASS', exit 0; lab timings 0.0 to 0.1 s ({OUT}/page_smoke_E4.txt).")
row("E4b10-cmd-verify_refs-offline", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
    f"'offline integrity: 560 entries, 0 problems', exit 0 ({OUT}/verify_refs_offline.txt).")
row("E4b10-cmd-verify_refs-live", "2.1-citations", "tools/verify_refs.py --unit E4 (live Crossref)", "PASS",
    f"'live re-verification of E4: 3 of 560 entries, 0 problems', exit 0 ({OUT}/verify_refs_unit_E4_live.txt).")
row("E4b10-cmd-render-diff", "gates", "tools/render_curriculum.py; CURRICULUM.md; curriculum/curriculum.json", "PASS",
    f"`render_curriculum.py` ('curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h') then `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`: exit 0, no tracked change ({OUT}/render.txt, render_diff.txt). E4 hours in curriculum.json are 100 (tier M, prereqs E2, E3, M7).")

# ---- independent re-derivation, attribution, delta
row("E4b10-rederive-numbers", "2.2-numbers, 2.4-math", "ledgers/E4/scripts/E4-b-r10/rederive_r10.py", "PASS",
    f"Independent script (stdlib, Fractions): 54 checks OK, 0 FAIL ({OUT}/rederive_r10.txt). L04: ranks 2, 3, 2, 1; augmented ranks for (1,2,3), (0,0,1), (5,0,0); replication family (1-t,2-2t,3-3t,t); R3 construction. L05: fixed points (4,-3/10), (5/2,-3/16), (2,-3/20); base path 0,5,15/4,65/16,...; ratios -1/4, -1, -3/2; E1 k=5 and 1025/256; M1 (3,-1/2), M2 -1/3, M3 5/4. L06: Example 6.9 (kappa 2, sigma_eta^2 2, tau_eta 1/2, tau_bar 3/4, theta 3/7 and 6/7, slope 7/9, V_U 2/3, x_I 1/7, x_U -1/7); clearing exact at 16 points; alternative slope residual -9/85; M1 to M3 (4, 5, 1/5, 3/5, 3/8, 3/2; Var(p) 27/32; b 4/9; 5/6; 1/6; price -3/4; x_I 7/4; x_U 1/4); clearing exact on 20 random instances; Part E re-simulated with random.Random(6) reproducing 0.426617 (tol 0.006497) and 0.761928 (tol 0.023538); E1 0.44; E2 -0.30 and -0.90.")
row("E4b10-muth-attribution", "2.1-citations", "course/modules/E/E4/L05.html:296; references/references.json (key muth1961rational)", "PASS",
    f"Claim (L05.html:296): 'the phrase rational expectations appears in the title of Muth (1961)', title-only use. Registry title 'Rational Expectations and the Theory of Price Movements', Muth, 1961, Econometrica 29(3). Plain curl to https://api.crossref.org/works/10.2307/1909635 returned HTTP 200 with the same title, container Econometrica, volume 29, issue 3, page 315, author Muth ({OUT}/crossref_muth.json, crossref_muth_summary.txt). The article body was not read; the claim is limited to the title, as the page says.")
row("E4b10-no-B1-B3-attribution", "2.1-citations", "L04.html, L05.html, L06.html; cards.json (L04-L06 cards)", "PASS",
    "No Grossman-Stiglitz, Mas-Colell, Milgrom or Whinston citation in the three pages or in the L04-L06 cards (grep). The only data-cite is muth1961rational (L05.html, data-locator 'title'). The Grossman card is E4-c (cards.json:1310, lesson L08), outside this slice.")
row("E4b10-delta-review", "delta since round-9 pin c93dd52", "git diff c93dd52 HEAD (slice files, twin, cards); tools/ notation/ references/", "PASS",
    "Hunks read in full: L04.html:51, 285; L05.html:51, 104, 402; L06.html:86, 143, 150, 225, 245-249 (twin docstring copy); tests/labs/E4/lab-E4-L06-1.py:8-9; cards.json E4-c055, c057, c069, c086, c120, c226, c228, c244, c248 (new) and the L04-L06 ranges. The tools/, notation/ and references/ trees have zero diff since c93dd52 (git diff output length 0). Hunks in other lessons (L01-L03, L07-L09, hub) are outside this slice.")

# ---- round-9 FAIL rows, re-verified at HEAD
row("E4b10-L04-define-before-use", "2.9 / BUILDER 1.x define-before-use", "course/modules/E/E4/L04.html:51 (round-9 FAIL location)", "PASS",
    "Round-9 FAIL carried. Line 51 no longer uses 'attainable', 'portfolio' or 'complete' informally. It names the terms and points forward explicitly: 'Section 1 defines the terms used here (the payoff matrix, portfolios, attainable payoffs, rank and complete markets, in Definitions 1.1 and 1.3)'. The first dfn sites are L04.html:66 (payoff matrix) and :77 (complete).")
row("E4b10-L04-indicator", "2.4 / notation 13", "course/modules/E/E4/L04.html:285", "PASS",
    "Round-9 FAIL carried. Line 285 now writes \\(\\indic\\{\\omega\\}\\), the registered macro \\indic (notation/notation.json macros list). No raw \\mathbf{1} remains in L04-L06 (grep).")
row("E4b10-L05-lemma31-hypothesis", "2.4 / Plan 2.1 item 6", "course/modules/E/E4/L05.html:103-104", "PASS",
    "Round-9 FAIL carried. Lemma 3.1 now opens 'Under A1 (so that β > 0), let c* ...', and its proof divides by β only after that hypothesis. Checked: the identity e_{k+1} = -(ς/β)e_k holds for any start (proof lines 105).")
row("E4b10-L05-psi0-notation", "2.9 / notation", "course/modules/E/E4/L05.html:402", "PASS",
    "Round-9 FAIL carried. Line 402 now reads 'The first entry of Ψ(0,0) is 10/2 = 5', defined by Proposition 2.2 (L05.html:88-89). No Ψ_0 remains in L05.html (grep). The damped step gives 5/2 = c0* (re-derived).")
row("E4b10-L06-lemma63-proof", "2.4 / Plan 2.1 item 3", "course/modules/E/E4/L06.html:143", "PASS",
    "Round-9 FAIL carried. The proof now shows Cov(s,u)=0 (s = v + ε, independent of u by A1) before applying G to the triple (e, s, u), so G(ii) applies to all three components. Var(e) identity re-derived: σ_v²−2ωσ_v²+ω²(σ_v²+σ_ε²) = σ_v²(1−ω) = V_I.")
row("E4b10-L06-lab-docstring-names", "2.5 / lab statements vs code", "tests/labs/E4/lab-E4-L06-1.py:8-9; course/modules/E/E4/L06.html:248-249", "PASS",
    "Round-9 FAIL carried. The twin docstring now reads 'the linear price p = theta_s * s - theta_u * u, with theta_s and theta_u from closed_form()'. No THETA_S or THETA_U remains (grep). closed_form() exists at twin line 65 and returns theta_s and theta_u at line 76.")
row("E4b10-cards-c120-basis", "2.7 cards", "course/modules/E/E4/cards.json, id E4-c120", "PASS",
    "Round-9 FAIL carried. The basis now reads 'Example 6.9 (Lemma 6.2 and Lemma 6.3 formulas); Lab 1, Part C'. x_I = (ωs − p)/(aV_I) uses Lemma 6.3 for ω and V_I and Lemma 6.2 for the CARA demand. Lemma 6.4 is not used.")
row("E4b10-cards-round9-duplicate-c059-c226", "2.7 duplicates", "cards.json E4-c059, E4-c226", "PASS",
    "Round-9 concern carried. E4-c226 now asks 'what is the augmented rank of a payoff ξ' (answer: the rank of [A; ξ]). It no longer asks when a payoff is attainable, so it is not a duplicate of E4-c059. Their answers overlap (Jaccard 0.7) but the questions differ. The remaining duplicate pairs are the two rows below.")

# ---- lesson rows: L04
row("E4b10-L04-why-it-matters", "2.9 / BUILDER 4.2", "course/modules/E/E4/L04.html:51", "PASS",
    "96 words (limit 120, counted with ledgers/E4/scripts/E4-b-r10/structure_scan_r10.py). Claims match the lesson: the finite completeness test is the rank (Theorem 1.4, L04.html:82) and the finite test does not carry over to infinitely many states (Proposition 4.1, L04.html:283-285).")
row("E4b10-L04-sec1-proofs", "2.4 mathematics", "course/modules/E/E4/L04.html:55-95", "PASS",
    "A1 to A3 (:58-60), Definition 1.1 (:65-66), Lemma 1.2 (:70-72), Definition 1.3 (:76-77), Theorem 1.4 (:81-83), Proposition 1.5 (:87-89), Corollary 1.6 (:93-95). Each proof re-read line by line. Theorem 1.4 uses the full-dimension argument correctly; Proposition 1.5 uses row(A) ⊆ row([A;ξ]) and equal dimensions correctly; every statement lists its assumptions (Under A1 to A3).")
row("E4b10-L04-lemma21-proof", "2.4 mathematics", "course/modules/E/E4/L04.html:101-103", "PASS",
    "Row operations preserve the row space; the echelon count is an independence argument on the pivot columns q_1 < ... < q_m (lines 103). Re-read and checked: if sum c_i r_i = 0 with smallest nonzero c_i, the column q_i entry is c_i times a nonzero pivot, a contradiction.")
row("E4b10-L04-lemma21-assumptions", "2.4 / Plan 2.1 item 6 (numbered Assumptions for every Lemma)", "course/modules/E/E4/L04.html:101-102", "FAIL",
    "Lemma 2.1 (elimination counts the rank) lists no numbered Assumption before its statement, and its proof cites none. Plan §2.1 item 6 (binding) states that every Theorem, Proposition, Lemma and Derivation block lists numbered Assumptions (A1, A2, ...) before the statement and that its proof cites them by number. The round-9 waiver ('needs none') is not in the plan. Lemma 2.1 is stated for a real matrix A, and that hypothesis is not written.",
    "Insert before the statement at L04.html:101 a numbered line, e.g. 'Assumption A0 (real matrix). A is a real matrix with J rows and S columns, with real entries.', and have the proof cite A0 in its first sentence (L04.html:103).")
row("E4b10-L04-examples", "2.4 / 2.2 examples", "course/modules/E/E4/L04.html:107-115", "PASS",
    "Example 2.2: rank 2 with S = 3 (:108); (1,2,3) = r1 + r2 attainable with ζ = (1,1); (0,0,1) not attainable (augmented rank 3). Example 2.3: rows e1, e2, e3, r4 = (1,2,3) give rank 3 and r4 = 1 e1 + 2 e2 + 3 e3 (:114). All re-derived (rederive_r10.py, L04 block).")
row("E4b10-L04-lab-1", "2.5 labs", "course/modules/E/E4/L04.html:117-260; tests/labs/E4/lab-E4-L04-1.py", "PASS",
    f"Hypothesis (L04.html:119) names rank 2 and 3, completeness False and True, (1,2,3) attainable, (0,0,1) and (5,0,0) not, and the redundant fourth row. Printed lines 243-258 match (page_twin_check.txt). Interpretation (:259) names only the printed matrices and says it does not test any market. Lab 1 Part E 'equals_fourth_row True' supports misconception 3 (L04.html:310).")
row("E4b10-L04-remarks", "2.9 / 2.4", "course/modules/E/E4/L04.html:265-271", "PASS",
    "Remark 3.1 (A = I_S, ζ = ξ, rank S); Remark 3.2: attainable set and rank unchanged by a redundant row; (1,2,3) by (1,2,3,0) and (0,0,0,1); kernel dimension J - rank(A) by rank-nullity, which is nonzero when rank(A) < J (re-checked).")
row("E4b10-L04-canon-breaks", "2.4 / 2.2 scope", "course/modules/E/E4/L04.html:274-295", "PASS",
    "Assumption A4 (:278-279); Proposition 4.1 (:283-285): J+1 indicator payoffs are independent in R^Ω, dim M(A) ≤ J, so M(A) ≠ R^Ω; hypotheses A2 to A4 listed; M(A) is defined for the infinite Ω by the same rows. Proposition 4.2 (:291-293): C(A) is a convex cone (closure under a,b ≥ 0), not R^S, example A = I_2 and (-1,0) re-derived. The statement 'no finite set of securities completes the market' is scoped to A4 (:435).")
row("E4b10-L04-misconceptions", "2.9 / 2.2", "course/modules/E/E4/L04.html:297-317", "PASS",
    "Four misconceptions, each with a worked example re-derived: rank of (1,1,1),(1,1,1),(0,1,2) = 2 (:306); two portfolios for (1,2,3) (:310); completeness uses only A (:314).")
row("E4b10-L04-problems", "2.4 / 2.9 problem set", "course/modules/E/E4/L04.html:319-421", "PASS",
    "Three per tier (M1-M3, P1-P3, E1-E3, R1-R3), each with a details.solution of 13 or more words (structure_scan_r10.txt: min 36 words). Every solution re-derived: M1 rank 1; M2 (1,1,2) with ζ=(1,1), (0,0,1) not attainable; M3 rank 2; P1 augmented rank; P2; P3 identity; E1 (5,0,0) equations; E2 ζ = (1-t,2-2t,3-3t,t); E3 rank 2; R1 J < S incomplete; R2 J = S; R3 construction (ζ3 = t, ζ1 = ξ1+t, ζ2 = ξ2+t).")
row("E4b10-L04-key-results-quiz", "2.9 / 2.4 key results and quiz", "course/modules/E/E4/L04.html:424-508", "PASS",
    "Key-results table: 8 rows, each graded T with its source (L04.html:429-436). Quiz: 8 items with explanations; answers checked (rank criterion; least J = 5; rank of (1,1,1),(1,1,1),(0,1,2) = 2; the replication family; Proposition 1.5; M1 rank 1; infinite states incomplete; (-1,0) not attainable under ζ ≥ 0).")
row("E4b10-L04-references", "2.1 / 2.9", "course/modules/E/E4/L04.html:511-524", "PASS",
    "'This lesson cites no source.' with an empty data-references list; no data-cite on the page; footer at :524.")

# ---- lesson rows: L05
row("E4b10-L05-why-it-matters", "2.9 / 2.2", "course/modules/E/E4/L05.html:51", "PASS",
    "120 words (at the limit of 120, counted with structure_scan_r10.py). 'converges from every start only when ς < β' matches Proposition 3.2 (both directions: convergence for ς < β, and failure from some start when ς ≥ β, L05.html:110). The lab checks match Lemma 3.1 and Parts A and B.")
row("E4b10-L05-model", "2.4 mathematics", "course/modules/E/E4/L05.html:55-73", "PASS",
    "A1 (β > 0, ς ≥ 0), A2 (affine forecasts), A3 (independent mean-zero normal shocks, σ_z² > 0). Definition 1.1: d(p) = α - βp + u, q = ς m(z) + δz + υ; p_m = (α - ς m(z) - δz + u - υ)/β (:67) re-derived from d(p) = q. Definition 1.2 (:72-73) and its dfn site (:73).")
row("E4b10-L05-lemma21-prop22-cor23", "2.4 mathematics", "course/modules/E/E4/L05.html:79-97", "PASS",
    "Lemma 2.1: E[p_m | z] = (α - ς(c0 + c1 z) - δz)/β and conditional variance (σ_u² + σ_υ²)/β² re-derived (:83). Proposition 2.2: Ψ and c0* = α/(β+ς), c1* = -δ/(β+ς) re-derived, uniqueness from β + ς > 0 (:91). Corollary 2.3: forecast error variance and unconditional variance (c1*)²σ_z² + (σ_u² + σ_υ²)/β² re-derived (:97).")
row("E4b10-L05-lemma31-proof", "2.4 mathematics", "course/modules/E/E4/L05.html:103-105", "PASS",
    "Round-9 FAIL carried (see E4b10-L05-lemma31-hypothesis). The recursion e_{k+1} = -(ς/β) e_k is re-derived for both components (line 105); the closed form for e_k follows by induction.")
row("E4b10-L05-lemma31-hypothesis", "2.4 / Plan 2.1 item 6", "course/modules/E/E4/L05.html:103-104", "PASS",
    "Round-9 FAIL carried and fixed: the statement now carries 'Under A1 (so that β > 0)', which is the hypothesis the proof's division by β needs.")
row("E4b10-L05-prop32-33", "2.4 mathematics", "course/modules/E/E4/L05.html:109-117", "PASS",
    "Proposition 3.2: convergence for ς < β; non-convergence for ς ≥ β when the start differs from c* (proof :111, the ς = β case keeps the error constant, ς > β grows). Proposition 3.3: error factor 1 - ν(1 + ς/β); zero at ν = β/(β+ς) (re-derived, :117).")
row("E4b10-L05-lab-1", "2.5 labs", "course/modules/E/E4/L05.html:121-281; tests/labs/E4/lab-E4-L05-1.py", "PASS",
    "Hypothesis (L05.html:122): c0* = 4, c1* = -3/10, ratio -1/4, ratio -1 with the path 0, 5, ratio -3/2, damped weight 4/5, and the identity at five z; all printed at lines 256-280 (page_twin_check.txt). show() calls check_params before iterating (twin line 87), as the docstring (L05.html:136-137) says. Interpretation (:281) states what the checks do not test.")
row("E4b10-L05-remark-canon-muth", "2.9 / 2.4 scope", "course/modules/E/E4/L05.html:286-296", "PASS",
    "Remark 4.1 (family contains exactly one REE; non-affine forecasts not excluded). 'Where the canon breaks' lists three limits (:293-295); the Muth paragraph (:296) is a fourth note with title-only use (see E4b10-muth-attribution).")
row("E4b10-L05-misconceptions", "2.9 / 2.2", "course/modules/E/E4/L05.html:300-316", "PASS",
    "Three misconceptions: conditional variance (σ_u² + σ_υ²)/β² zero only when both variances vanish (:304); Part C fixed point 5/2 with alternating path (:308); the forecast is c0* + c1* z, with mean c0* (:312). All numbers re-derived.")
row("E4b10-L05-problems", "2.4 / 2.9 problem set", "course/modules/E/E4/L05.html:318-419", "PASS",
    "M1 (3, -1/2), M2 ratio -1/3, M3 variance 5/4, P1 to P3 proofs, E1 (k = 5, 1/256), E2 (5/2 stays put), E3 (e3 = 27/4; ratio -3/2), R1 (weight 1/2, first component 5/2; Ψ_0 notation fixed at :402), R2 (δ = 0 gives constant forecast and variance), R3 prose (existence versus convergence). Each solution re-derived (rederive_r10.py L05 block).")
row("E4b10-L05-key-results-quiz", "2.9 / 2.4", "course/modules/E/E4/L05.html:422-502", "PASS",
    "Key results: 7 rows, each graded T with source (L05.html:427-433). Quiz: 8 items with explanations; answers checked (α/(β+ς); c0* = 4; ratio -1/4; ς < β; ς = β error keeps size; ν = β/(β+ς); variance 5/4; δ = 0 gives constant).")
row("E4b10-L05-references", "2.1 / 2.9", "course/modules/E/E4/L05.html:504-516", "PASS",
    "One data-cite (muth1961rational, data-locator title), resolved in the registry; footer at :516.")

# ---- lesson rows: L06
row("E4b10-L06-why-it-matters", "2.9 / 2.2", "course/modules/E/E4/L06.html:51", "PASS",
    "113 words (limit 120). Cross-references Definition 6.1 (L06.html:57), A2 (:72) and A3 (:77) exist. 'some investors who observe more than the price' is consistent with A2.")
row("E4b10-L06-model", "2.4 / Plan 2.1 item 6", "course/modules/E/E4/L06.html:56-92", "PASS",
    "Definition 6.1 primitives; Definition 6.2 CARA with a > 0 (:67); A1 (:61-62); A2 (:72); A3 (:77); A4 (:82-85) with the clearing residual argument (:86): the residual is linear in (s, u) with no constant term, zero on a line, which has probability zero under the nondegenerate normal law of (s, u) (σ_v² + σ_ε² > 0, σ_u² > 0). G (:91) states the two facts used without proof, and says the mgf is proved in Lemma 6.2.")
row("E4b10-L06-lemma62-proof", "2.4 mathematics", "course/modules/E/E4/L06.html:107-125", "PASS",
    "Mgf identity E e^{tZ} = e^{tμ + t²V/2} and the completed-square identity re-derived. g(x) = -a x (m-p) + (a²V/2) x² (:123) re-derived; minimising g maximises -e^{-aw0}e^{g} (:125); x* = (m-p)/(aV).")
row("E4b10-L06-lemma62-hypotheses", "2.4 / Plan 2.1 item 6", "course/modules/E/E4/L06.html:99-101", "PASS",
    "Lemma 6.2 says 'Assume A3 (price taking)' and states V > 0. The coefficient a > 0 is the standing parameter of Definition 6.2 (:67) for the investor the lemma describes, and the formula divides by a. Checked: the maximiser is unique for every a ≠ 0, so the lemma needs no hypothesis beyond the definition. Recorded as a note, not a defect.")
row("E4b10-L06-lemma63-proof", "2.4 / Plan 2.1 item 3", "course/modules/E/E4/L06.html:129-143", "PASS",
    "Round-9 FAIL carried and fixed: the proof at :143 now shows that (e, s, u) has pairwise zero covariances (e with s and u; s with u, since s = v + ε is independent of u under A1), so G applies. Statement (:130-138): ω, V_I and 1/V_I = τ_v + τ_ε, ω/V_I = τ_ε re-derived.")
row("E4b10-L06-lemma64", "2.4 mathematics", "course/modules/E/E4/L06.html:147-158", "PASS",
    "Cov(v, p) = θ_s σ_v² uses Cov(v, u) = 0 (:150, now stated). Proof (:157): e = v - bp uncorrelated with p, (e, p) is a linear image of (v, s, u), G gives independence, E[v|p] = bp and Var(v|p) = σ_v² - b Cov(v,p) re-derived.")
row("E4b10-L06-remark-65-610", "2.9 / 2.4", "course/modules/E/E4/L06.html:161-163, 233-236", "PASS",
    "Remark 6.5: x_U = (bp - p)/(aV_U) and x_I = (ωs - p)/(aV_I) linear in (s, p) (re-derived). Remark 6.10: Y = p/θ_s* = s - κu = v + η, η = ε - κu, σ_η² = σ_ε² + κ²σ_u² ≥ σ_ε² > 0 for every σ_u² ≥ 0 (:235); larger σ_u² raises σ_η² and lowers τ_η.")
row("E4b10-L06-prop67", "2.4 mathematics", "course/modules/E/E4/L06.html:173-226", "PASS",
    "Proposition 6.7 (a) existence: θ_s* ≠ 0 since τ̄ > 0; Y = s - κu; Q θ_s* = λτ_ε and Q θ_u* = a with Q = τ_v + τ̄ - (1-λ)τ_η/θ_s*; the clearing identity holds for every (s, u) (:208-211). (b) uniqueness: Step 1 θ_s ≠ 0 (A4 at (s,0) and (s+1,0) with u = 0, :192); Step 2 Y = p/θ_s with η independent of v (:193); Step 3 clearing (:194-202); Step 4 κ' = κ, θ_s = θ_s* (:203). All re-derived by hand; the exact check of part (a) on 20 random instances passed (rederive_r10.py).")
row("E4b10-L06-cor68-slope-step", "2.4 mathematics", "course/modules/E/E4/L06.html:212-225", "FAIL",
    "Corollary 6.8 states 'The slope b of Lemma 6.4 equals τ_η/(θ_s*(τ_v+τ_η))' (:220). The proof (:225) derives E[v|p] = (τ_η/P_U) Y and the first displayed formula, and the variance identity, but never states the comparison that gives b: Lemma 6.4 gives E[v|p] = b p, and Var(p) > 0 because θ_s* ≠ 0, so b is the coefficient of p in the first formula. The formula itself is true: b = 7/9 at the base instance (rederive_r10.py), so this is a missing step, not a false claim.",
    "Append to the proof at L06.html:225: 'Lemma 6.4 gives E[v | p] = b p, and Var(p) > 0 because θ_s* ≠ 0. Comparing the coefficient of p with the first formula gives b = τ_η/(θ_s*(τ_v + τ_η)).'")
row("E4b10-L06-example69", "2.2 numbers, 2.4", "course/modules/E/E4/L06.html:229-231", "PASS",
    "Base instance (σ_v² = σ_ε² = a = 1, λ = 1/2, σ_u² = 1/4): κ = 2, σ_η² = 2, τ_η = 1/2, τ̄ = 3/4, θ_s* = 3/7, θ_u* = 6/7, b = 7/9, V_U = 2/3, x_I = 1/7, x_U = -1/7, clearing 1/2·1/7 + 1/2·(-1/7) = 0. All re-derived (rederive_r10.py, L06 block). The statement that Lab 1 prints the listed values and not τ_v, the price at (1,0), or x_U is checked against the lab output (L06.html:461-479).")
row("E4b10-L06-lab-1", "2.5 labs", "course/modules/E/E4/L06.html:238-480; tests/labs/E4/lab-E4-L06-1.py", "PASS",
    "Hypothesis (L06.html:240): κ 2, σ_η² 2, τ_η 1/2, τ̄ 3/4, θ 3/7 and 6/7, slope 7/9, posterior 2/3, 16 grid residuals zero, alternative slope 1/2 gives a nonzero residual at (1,0). Printed lines 461-479 match (page_twin_check.txt). Part D residual -9/85 re-derived. Part E sample slopes 0.426617 and 0.761928 with tolerances 0.006497 and 0.023538 reproduced by re-simulation with random.Random(6) (rederive_r10.py). Interpretation (:480) matches the printed values and says what Part E does not test.")
row("E4b10-L06-lab-docstring-names", "2.5 lab statements vs code", "tests/labs/E4/lab-E4-L06-1.py:8-9", "PASS",
    "Round-9 FAIL carried and fixed: the docstring names theta_s and theta_u from closed_form(), and the code uses those names (closed_form, Price tuple). Units paragraph (:258-262) matches the algebra: κ and θ_u carry price per asset squared, θ_s is dimensionless (re-derived from κ = aσ_ε²/λ).")
row("E4b10-L06-canon-breaks", "2.9 / 2.4 scope", "course/modules/E/E4/L06.html:484-491", "PASS",
    "Five limits (normality, utility, exogenous λ, independent supply, price taking, one period). Claims are hedged ('need not'); the independent-supply claim Cov(v,p) = θ_s σ_v² - θ_u Cov(v,u) (:489) is re-derived.")
row("E4b10-L06-misconceptions", "2.9 / 2.2", "course/modules/E/E4/L06.html:496-514", "PASS",
    "Four misconceptions with numbers checked: σ_η² = 2 (Part A); b = 7/9 and θ_s = 3/7 (Parts A and B); posterior 2/3 below prior 1 (Corollary 6.8, Part B); the noise trader carries no beliefs (Definition 6.1).")
row("E4b10-L06-R1-corr-identity", "2.4 / 2.9 problem set (proof gap)", "course/modules/E/E4/L06.html:599-602 (R1)", "FAIL",
    "R1 asks to show Corr(v,p)² → 0 as λ → 0. The solution (:602) asserts 'The squared correlation is σ_v²/(σ_v²+σ_η²) → 0' without deriving it. The identity is true (checked on two instances, rederive_r10.py), and M2 (:534) verifies it at one instance only, but the general identity is not derived anywhere in the lesson.",
    "Insert in the R1 solution before the limit: 'Since θ_u* = κθ_s*, Var(p) = θ_s*²(σ_v² + σ_ε² + κ²σ_u²) = θ_s*²(σ_v² + σ_η²) and Cov(v,p) = θ_s*σ_v², so Corr(v,p)² = σ_v²/(σ_v²+σ_η²).'")
row("E4b10-L06-problems", "2.4 / 2.9 problem set", "course/modules/E/E4/L06.html:516-619", "PASS",
    "M1 (κ 4, σ_η² 5, τ_η 1/5, τ̄ 3/5, θ_s* 3/8, θ_u* 3/2); M2 (Var(p) 27/32, b 4/9, Var(v|p) 5/6, Corr² 1/6); M3 (p = -3/4, x_I = 7/4, x_U = 1/4, clearing 1); P1 (Lemma 6.3 with θ = 0 allowed); P2 (θ_s ≠ 0 with (s,0),(s+1,0)); P3 identity; E1 (0.44 standard errors); E2 (-0.30 tolerance, -0.90 SE); E3 (what the seeded check tests); R2 (Var(v|p) strictly increasing in σ_u²); R3 (non-normal payoff: named hypotheses). Each re-derived. R1 is FAIL (E4b10-L06-R1-corr-identity).")
row("E4b10-L06-key-results-quiz", "2.9 / 2.4", "course/modules/E/E4/L06.html:621-724", "PASS",
    "Key results: 7 rows (T for Lemmas 6.3, 6.4, Proposition 6.7, Corollary 6.8 and base values; C for the finite check and the SIMULATED check, L06.html:632-634). Quiz: 12 items; numeric answers checked (θ_s* 3/7; κ 4; σ_η² 2; V_I 1/2; x_I 1/7; b 7/9; Var(v|p) 2/3; uniqueness; clearing residual, L06.html:716-722).")
row("E4b10-L06-references", "2.1 / 2.9", "course/modules/E/E4/L06.html:726-739", "PASS",
    "'This lesson cites no source.' with an empty data-references list; footer at :739.")

# ---- cards
row("E4b10-cards-L04", "2.7 cards", "course/modules/E/E4/cards.json (lesson L04, 33 cards)", "PASS",
    "All 33 L04 cards read in full (outputs/cards_L04_L06.txt). Each front and back checked against the lesson text and the attached basis. Cards E4-c226 and E4-c228 carry no grade and no basis: they are definitional, state no empirical claim, and the schema permits the omission (71 of 243 cards have no grade).")
row("E4b10-cards-L05", "2.7 cards", "cards.json (lesson L05, 31 cards)", "PASS",
    "All 31 L05 cards read in full. E4-c086 (ς, β hypothesis) matches Lemma 3.1; E4-c099 (Muth, title only) matches L05.html:296; E4-c219 and E4-c243 values match the printed lab lines 266 and 272-276; E4-c094 matches Part E (line 278).")
row("E4b10-cards-L06", "2.7 cards", "cards.json (lesson L06, 35 cards)", "PASS",
    "All 35 L06 cards read in full. Grades: finite checks and SIMULATED cards (E4-c122, c123, c124, c125) are C and match L06.html:632-634. E4-c244 (σ_η² ≥ σ_ε² for every σ_u² ≥ 0) matches Remark 6.10. E4-c248 has lesson L04 and is discussed in the duplicate row below.")
row("E4b10-cards-numbers-in-lesson", "2.7 cards", "cards.json (L04 to L06)", "PASS",
    "Every number on the 99 slice cards appears in its lesson's prose, key results or printed lab output. Spot checks: 1/7 and -1/7 (L06.html:230, 461-479), 16 grid points (:472), 27/4 (structure of E3 solution, L05.html:391), 5/2 and -3/16 (L05.html:266), 0.426617 (L06.html:478).")
row("E4b10-cards-process-words", "2.9 / 2.7", "cards.json (L04 to L06); pages", "PASS",
    "Scan of the 99 slice cards and three pages for builder, verifier, round, fragment, ledger, twin, architect, plan, mutant, REQUEST, registry, unit report: no learner-visible hit (structure_scan_r10.txt).")
row("E4b10-cards-id-unique", "2.7 cards", "course/modules/E/E4/cards.json", "PASS",
    "243 cards, 243 unique ids; every card has id, lesson, front and back (structure_scan_r10.txt).")
row("E4b10-cards-duplicate-scan", "2.7 duplicates (full scan)", "cards.json, all 99 slice cards (pairs with front-token Jaccard ≥ 0.35 read in full)", "PASS",
    "Full pairwise scan (structure_scan_r10.py, output outputs/structure_scan_r10.txt). The pairs read and judged NOT duplicates (different question): E4-c124/c125, c092/c093, c090/c219, c120/c220, c111/c113, c077/c241, c080/c109, c082/c095, c109/c115, c116/c117, c084/c085, c066/c240, c062/c064, c057/c215, c059/c226, c093/c243. The two real duplicates are separate rows below.")
row("E4b10-cards-dup-c058-c248", "2.7 duplicates", "course/modules/E/E4/cards.json, E4-c058 (line 435) and E4-c248 (line 1802)", "FAIL",
    "E4-c058 'Assume A1 to A3. When is the market with payoff matrix A complete (Theorem 1.4)?' and E4-c248 'When is a market with payoff matrix A complete or incomplete (Definition 1.3)?' ask the same question with the same answer (complete iff rank = S, or iff M(A) = R^S). E4-c248 was added in this round and duplicates E4-c058.",
    "Delete E4-c248 from cards.json. If the 'otherwise incomplete' wording is wanted, add it to the back of E4-c058 instead.")
row("E4b10-cards-dup-c055-c059", "2.7 duplicates", "course/modules/E/E4/cards.json, E4-c055 (line 415) and E4-c059 (line 443)", "FAIL",
    "E4-c055 'When is a payoff ξ in R^S attainable (Definition 1.1)?' and E4-c059 'Assume A1 to A3. When is a payoff ξ attainable (Proposition 1.5)?' ask the same question. Both answers characterise attainability (ξ = ζ^T A, or the rank test), so the same question is carded twice.",
    "Delete E4-c055, or change its front to a question it answers uniquely, e.g. 'What is the attainable payoff of a portfolio ζ (Definition 1.1)?' (cards.json line 415-417).")

# ---- notation, DAG, prose, structure
row("E4b10-notation", "2.4 notation / plan 2.3", "course/modules/E/E4/L04.html, L05.html, L06.html; notation/notation.json", "PASS",
    "Macros used inside math (structure_scan_r10.txt): L04 R, indic; L05 E, Normal, R, Var; L06 Corr, Cov, E, R, Var. All registered. No \\mathbb (0 hits). No registry symbol T, Φ, γ_3, γ_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} (0 hits). Plain Q appears as a scalar in the Step 3 proof of Proposition 6.7 (L06.html:194-203). The registry symbol is \\mathbb{Q}, so plain Q is not a collision; noted only.")
row("E4b10-dag-closure", "2.9 DAG / plan §4", "L04.html:37-38; L05.html:37-38; L06.html:37-38, 91, 487", "PASS",
    "Concepts linked or named: arrow-debreu-security (L01, earlier lesson, :37 links L01.html#def), market-completeness (E4 L04 own dfn :77), rational-expectations-equilibrium (E4 L05 own dfn :73; L06 links L05.html#def), noisy-rational-expectations-equilibrium (own dfn L06:169), linear-map, vector-space, least-squares-projection (M3); conditional-expectation-elementary, expectation, normal-distribution, random-variable, variance, independence, multivariate-normal, moment-generating-function (M4); competitive-equilibrium (E1); expected-utility, crra-utility (E3). Owners read from curriculum/curriculum.json concepts: all in the closure {E1, E2, E3, M1-M4, M7, P0.1} or earlier E4 lessons. check_dag E4 PASS.")
row("E4b10-dag-plan-terms", "2.9 DAG (plan §4 D1-D10)", "L04.html, L05.html, L06.html", "PASS",
    "Grep for D1-D10 terms (Bayes, state price, stochastic discount, law of one price, fundamental theorem, informationally efficient, martingale, Banach, intermediate value, noise-trader risk, two-fund, diagnostic, determinacy, common knowledge, Walras, informed trading): 0 hits. 'noise trader' (L06.html:57) and CARA utility (:67) are plain dfn with no data-concept, as D6 and D7 require.")
row("E4b10-banned-process", "2.9 banned phrases", "L04.html, L05.html, L06.html", "PASS",
    "Banned strings (TODO, TBD, lorem, obviously, clearly, studies show, experts agree, well known, for brevity, beyond the scope, left as an exercise, it is important to note, details omitted, you can add more) and ellipses outside code: none (structure_scan_r10.txt). check_pages BANNED passes.")
row("E4b10-scope-words", "2.9 / BUILDER 4 scope words", "L04.html:51, 271, 288, 435; L05.html:51, 294, 296; L06.html:86, 235, 240", "PASS",
    "Each changed scope word read in context: 'the exact test' (L04:51) is the rank computation of Theorem 1.4; 'does not carry over' (L04:51, 288) is Proposition 4.1; 'only when ς < β' (L05:51, 294) is the contrapositive of Proposition 3.2; 'with probability one forces ... every pair' (L06:86) is backed by the line argument; 'reveals the payoff only with noise' (L06:235) is backed by σ_η² ≥ σ_ε² > 0.")
row("E4b10-simulated-labels", "2.5 / 2.8 SIMULATED", "L06.html:240, 255, 475-480, 633-634; cards.json E4-c124, E4-c125", "PASS",
    "The only random draw in the slice is L06 Part E (random.Random(6), 20000 draws), labelled SIMULATED at L06.html:240, 255, 475 and 633-634. L04 and L05 twins contain no random draws (grep for random: none). Cards c124 and c125 are graded C with the SIMULATED label.")
row("E4b10-grades", "2.3 grades", "L04.html:429-436; L05.html:427-433; L06.html:628-634", "PASS",
    "Grades re-graded against BLUEPRINT §3. T for the theorems, lemmas and propositions with complete proofs (L04:429-436, L05:427-433, L06:628-632) and for the exact base-instance values (L06:632). C for the finite grid check (L06:633) and the seeded SIMULATED check (L06:634). No over-grading found.")
row("E4b10-hours", "2.9 hours", "L04.html:34, L05.html:34, L06.html:34; index.html:29", "PASS",
    "data-hours 8 on each lesson (6 to 12 range); hub data-hours-lessons 72 = 9 × 8; data-hours-project 28; 72 + 28 = 100 = curriculum.json E4 hours (100). No arithmetic conflict.")
row("E4b10-structure-order", "2.9 structure", "L04.html, L05.html, L06.html", "PASS",
    "Section order: why it matters, numbered core sections, inline lab before 'where the canon breaks', misconceptions, problem set (3 per tier, 12 solutions per lesson), key results, quiz (8, 8, 12 items), references (structure_scan_r10.txt; check_pages PASS).")
row("E4b10-hub-titles", "2.9 structure", "index.html:144-146 vs L04.html:35, L05.html:35, L06.html:35", "PASS",
    "Hub lesson titles equal each lesson's h1: 'Complete and Incomplete Markets', 'Rational-Expectations Equilibrium', 'Noisy rational-expectations equilibrium'. Hub text describes L06 as a seeded sample check labelled SIMULATED; out-of-slice note in notes.")
row("E4b10-lab-twin-structure", "2.5 labs", "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", "PASS",
    "Each twin ends with an unconditional main() call (lab-E4-L04-1.py line 122, L05 line 132, L06 line 220); no __name__ guard (grep). Standard library only (fractions, math, random, typing, __future__); no network; each runs under 0.1 s (page_smoke timings). Seeds: L06 random.Random(6) only.")

out = {
    "unit": "E4",
    "slice": "b",
    "round": 10,
    "verifier": "Haiku independent verifier, E4-b round 10 (did not build E4; no shared context with builders)",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36 (detached; checkout /Users/billyribeiro/.fanout/wt/verifyE10-E4-b)",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (round-9 pin). Round-9 fragment /Users/billyribeiro/.fanout/frags/E-E4-b.round9.json was context only; no round-9 PASS row was carried, every row was re-verified at the pin.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-E4-b",
    "scratch": "ledgers/E4/scripts/E4-b-r10/ (html_lines.py, page_twin_check.py, rederive_r10.py, structure_scan_r10.py, write_fragment_r10.py, run_commands_r10.sh, outputs/)",
    "verified_at": "2026-11-05",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b is L04.html, L05.html, L06.html, the three lab twins lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py, and the L04-L06 cards in cards.json (99 cards). It is not a project slice: no grader mutants or alternatives are written here, and lab twins are demonstrations (ruling), so the mutants list is empty.",
        "All 8 round-9 FAIL rows are fixed at the pin and re-verified: L04.html:51, L04.html:285, L05.html:104, L05.html:402, L06.html:143, tests/labs/E4/lab-E4-L06-1.py:8-9, card E4-c120, and the c059/c226 duplicate (c226 now asks a different question). The round-8 'registry' wording is also clean at the pin. The new FAIL rows are two card duplicates (c058/c248, c055/c059) and three minor proof or statement gaps (L04 Lemma 2.1 assumption list, L06 Corollary 6.8 slope step, L06 R1 correlation identity).",
        "Lemma 6.2 (L06.html:99-101) does not list a > 0; checked and recorded as a note, not a defect, because a > 0 is the standing parameter of Definition 6.2 and the unique-maximiser claim holds for every a ≠ 0.",
        "Hub index.html:38 and :167 list the exact-Fraction labs as L01, L02, L04, L05 and L09 and omit L06, whose Parts A to D are exact (L06.html:240). The hub is outside slice b; a hub owner should add L06 to that sentence. Not a row of this slice.",
        "Not checked: the Muth (1961) article body (only the title and Crossref metadata were read, as the page claims only the title). The project grader, mutants and alternatives belong to slice a/d, not this slice. The rest of the cards.json (L01-L03, L07-L09) and their lessons are outside slice b; only their id uniqueness and the L04-L06 cards were read.",
        "Plain curl only; no bot check, login or paywall was touched. The Crossref request carries no personal data.",
    ],
    "summary": "",
}
fails = [r["id"] for r in rows if r["status"] != "PASS"]
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
out["summary"] = (f"FAIL E4-b round 10: rows={len(rows)} (pass={counts['PASS']}, fail={counts['FAIL']}, "
                  f"unverifiable={counts['UNVERIFIABLE']}). Non-PASS: {', '.join(fails)}. "
                  "All gates re-run at 00a84795 pass (check_pages, check_dag, check_projects, run_labs 12/12, twins under python -I -W error, page code and expected blocks equal the twins, ruff, mypy, pytest 365 + 49, page_smoke, verify_refs offline and live, render diff clean).")
Path("ledgers/E4/E4-b.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("written", len(rows), counts)
